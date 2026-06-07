"""LangGraph cold-start agent loop.

This is the LangGraph orchestration layer for theory discovery. It deliberately
reuses the existing cold-start generation, harness validation, and memory code
so the graph controls state and branching without reimplementing physics.
"""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict

from langgraph.graph import END, StateGraph

from .cold_start_runner import (
    _best_chi2,
    _build_token_level_context,
    _generate_token_level_entry,
    _load_summary,
    _parameter_samples,
    _proposal_for,
    _structural_expansion_skip_reason,
    _wall_timeout,
    _write_token_level_context_summary,
    _write_token_level_source,
)
from .harness import ROOT, validate_agent_sample_pipeline
from .memory import record_attempt
from .report import generate_report
from .validation_result import ValidationResult
from .dataset import chi2_quality_tier


class GraphAgentState(TypedDict, total=False):
    run_name: str
    proposal_dir: str
    memory_dir: str
    loop_count: int
    loop_index: int
    seed: int
    initial_parameter_samples: int
    expanded_parameter_samples: int
    expansion_chi2: float
    pre_sampling_timeout: int
    grammar_generation_timeout: int
    use_token_context_cache: bool
    proposal_mode: str
    llm_model: str
    llm_fallback: str
    llm_proposal_timeout: int
    llm_api_timeout: int
    proposal_memory_enabled: bool
    rng: Any
    token_context: Any
    entry: Dict[str, Any]
    source_path: str
    initial_record: Dict[str, Any]
    latest_record: Dict[str, Any]
    latest_reflection: Dict[str, Any]
    decision: Dict[str, Any]
    next_action: str
    skip_expansion_reason: Optional[str]
    fatal_stop: bool
    results: List[Dict[str, Any]]
    loop_traces: List[Dict[str, Any]]
    summary: Dict[str, Any]
    messages: List[str]


def _append(state: GraphAgentState, message: str) -> List[str]:
    return [*state.get("messages", []), message]


def _result_row(
    *,
    loop_index: int,
    stage: str,
    proposal_path: Path,
    source_path: Path,
    parameter_path: Path,
    result: ValidationResult,
    attempt: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "loop": loop_index,
        "stage": stage,
        "proposal_path": str(proposal_path),
        "source_lagrangians_path": str(source_path),
        "parameter_samples_path": str(parameter_path),
        "validated": result.validated,
        "failed_stage": result.failed_stage,
        "chi2": result.chi2,
        "family_key": attempt["family_key"],
        "coarse_family_key": attempt.get("coarse_family_key"),
        "failure_tags": attempt["failure_tags"],
        "top_reject_reasons": attempt["top_reject_reasons"],
        "solver_output_dir": result.solver_output_dir,
    }


def initialize_run(state: GraphAgentState) -> Dict[str, Any]:
    loop_count = int(state.get("loop_count", 20))
    seed = int(state.get("seed", 20260601))
    stamp = time.strftime("%Y%m%d_%H%M%S")
    run_name = state.get("run_name") or f"graph_agent_{loop_count}_{stamp}"
    proposal_dir = ROOT / "ai_theory_lab" / "proposals" / run_name
    memory_dir = ROOT / "ai_theory_lab" / "memory" / run_name
    proposal_dir.mkdir(parents=True, exist_ok=False)
    memory_dir.mkdir(parents=True, exist_ok=False)

    updates: Dict[str, Any] = {
        "run_name": run_name,
        "proposal_dir": str(proposal_dir),
        "memory_dir": str(memory_dir),
        "loop_index": 1,
        "rng": random.Random(seed),
        "results": [],
        "loop_traces": [],
        "summary": {},
        "messages": _append(state, f"Initialized LangGraph agent run {run_name}."),
    }
    if loop_count <= 0:
        return updates

    try:
        token_context = _build_token_level_context(
            int(state.get("grammar_generation_timeout", 0)),
            use_cache=bool(state.get("use_token_context_cache", True)),
        )
        _write_token_level_context_summary(token_context, proposal_dir / "operator_catalog_summary.json")
        updates["token_context"] = token_context
        updates["messages"] = [*updates["messages"], "Built token-level Grammar Masker context once for this run."]
    except Exception as exc:
        result = ValidationResult(
            validated=False,
            failed_stage="GrammarGeneration",
            diagnostics={
                "message": f"Initial independent-scalar discovery failed before loop sampling: {type(exc).__name__}: {exc}",
                "failure_kind": "pre_sampling_timeout" if isinstance(exc, TimeoutError) else "grammar_generation_failure",
            },
        )
        memory_info = record_attempt(result, memory_dir, loop_id="operator_discovery")
        updates["results"] = [
            {
                "stage": "operator_discovery",
                "validated": False,
                "failed_stage": "GrammarGeneration",
                "chi2": None,
                "diagnostic_message": result.diagnostics["message"],
            }
        ]
        updates["summary"] = memory_info["summary"]
        updates["fatal_stop"] = True
        updates["messages"] = [*updates["messages"], "Grammar generation failed; stopping graph run."]
    return updates


def start_loop(state: GraphAgentState) -> Dict[str, Any]:
    memory_dir = Path(str(state["memory_dir"]))
    summary = _load_summary(memory_dir)
    return {
        "summary": summary,
        "skip_expansion_reason": None,
        "entry": {},
        "source_path": "",
        "latest_record": {},
        "latest_reflection": {},
        "decision": {},
        "next_action": "",
        "messages": _append(state, f"Starting loop {state.get('loop_index')}/{state.get('loop_count')}."),
    }


def propose_theory(state: GraphAgentState) -> Dict[str, Any]:
    loop_index = int(state["loop_index"])
    seed = int(state["seed"])
    proposal_dir = Path(str(state["proposal_dir"]))
    memory_dir = Path(str(state["memory_dir"]))
    rng = state["rng"]
    summary = state.get("summary") or {}
    proposal_summary = summary if bool(state.get("proposal_memory_enabled", True)) else {}
    proposal_mode = str(state.get("proposal_mode") or "deterministic")
    llm_fallback = str(state.get("llm_fallback") or "deterministic")
    try:
        if proposal_mode == "llm":
            with _wall_timeout(int(state.get("llm_proposal_timeout", 600)), "LLM proposal generation"):
                try:
                    from .llm_agent import propose_entry_with_llm

                    entry = propose_entry_with_llm(
                        state["token_context"],
                        proposal_summary,
                        rng,
                        seed + loop_index * 7919,
                        model=str(state.get("llm_model") or "") or None,
                        api_timeout=float(state.get("llm_api_timeout", 120)),
                        debug_dir=proposal_dir / "llm_proposal_debug",
                        loop_id=f"loop_{loop_index:02d}",
                    )
                except Exception as llm_exc:
                    if llm_fallback == "fail":
                        raise RuntimeError(f"LLM proposal failed in strict mode: {type(llm_exc).__name__}: {llm_exc}") from llm_exc
                    print(
                        f"[{loop_index:02d}/{state['loop_count']}] "
                        f"LLM proposal failed; falling back to deterministic proposal: "
                        f"{type(llm_exc).__name__}: {llm_exc}",
                        flush=True,
                    )
                    entry = _generate_token_level_entry(
                        state["token_context"],
                        proposal_summary,
                        rng,
                        seed + loop_index * 7919,
                    )
                    entry["proposal_mode"] = "deterministic_fallback"
                    entry["llm_error"] = f"{type(llm_exc).__name__}: {llm_exc}"
        else:
            with _wall_timeout(int(state["pre_sampling_timeout"]), "Token-level proposal generation"):
                entry = _generate_token_level_entry(
                    state["token_context"],
                    proposal_summary,
                    rng,
                    seed + loop_index * 7919,
                )
                entry["proposal_mode"] = entry.get("proposal_mode", "direct_candidate_policy")
    except Exception as exc:
        strict_llm_failure = proposal_mode == "llm" and llm_fallback == "fail"
        result = ValidationResult(
            validated=False,
            failed_stage="LLMProposal" if strict_llm_failure else "GrammarGeneration",
            diagnostics={
                "message": f"Token-level proposal generation failed before validation: {type(exc).__name__}: {exc}",
                "failure_kind": (
                    "llm_proposal_failure"
                    if strict_llm_failure
                    else ("pre_sampling_timeout" if isinstance(exc, TimeoutError) else "grammar_generation_failure")
                ),
            },
        )
        memory_info = record_attempt(result, memory_dir, loop_id=f"loop_{loop_index:02d}")
        attempt = memory_info["attempt"]
        row = {
            "loop": loop_index,
            "stage": "grammar_generation",
            "proposal_path": None,
            "source_lagrangians_path": None,
            "parameter_samples_path": None,
            "validated": False,
            "failed_stage": result.failed_stage,
            "chi2": None,
            "family_key": attempt["family_key"],
            "coarse_family_key": attempt.get("coarse_family_key"),
            "failure_tags": attempt["failure_tags"],
            "top_reject_reasons": attempt["top_reject_reasons"],
            "solver_output_dir": None,
            "diagnostic_message": result.diagnostics["message"],
            "decision": {
                "loop": loop_index,
                "after_stage": "llm_proposal" if strict_llm_failure else "grammar_generation",
                "action": "stop" if strict_llm_failure else "next_theory",
                "reason": "token-level proposal generation failed before validation",
                "evidence": [result.diagnostics["message"]],
            },
        }
        return {
            "results": [*state.get("results", []), row],
            "summary": memory_info["summary"],
            "decision": row["decision"],
            "next_action": "stop" if strict_llm_failure else "skip_validation",
            "fatal_stop": bool(strict_llm_failure),
            "messages": _append(
                state,
                (
                    f"Strict LLM proposal failed for loop {loop_index}; stopping graph run."
                    if strict_llm_failure
                    else f"Proposal generation failed for loop {loop_index}; skipping validation."
                ),
            ),
        }
    source_path = proposal_dir / f"loop_{loop_index:02d}_token_lagrangians.pkl"
    _write_token_level_source(entry, source_path)
    return {
        "entry": entry,
        "source_path": str(source_path),
        "messages": _append(
            state,
            f"Proposed token-level legal theory for loop {loop_index} using {entry.get('proposal_mode', proposal_mode)} mode.",
        ),
    }


def validate_initial(state: GraphAgentState) -> Dict[str, Any]:
    loop_index = int(state["loop_index"])
    proposal_dir = Path(str(state["proposal_dir"]))
    memory_dir = Path(str(state["memory_dir"]))
    source_path = Path(str(state["source_path"]))
    rng = state["rng"]
    entry = state["entry"]
    summary = state.get("summary") or {}
    proposal_summary = summary if bool(state.get("proposal_memory_enabled", True)) else {}

    samples = _parameter_samples(entry, rng, int(state["initial_parameter_samples"]), proposal_summary)
    proposal = _proposal_for(entry, loop_index, samples, "initial")
    proposal_path = proposal_dir / f"loop_{loop_index:02d}_initial.json"
    parameter_path = proposal_dir / f"loop_{loop_index:02d}_initial_parameter_samples.json"
    proposal_path.write_text(json.dumps(proposal, indent=2, ensure_ascii=False), encoding="utf-8")
    parameter_path.write_text(json.dumps(samples, indent=2, ensure_ascii=False), encoding="utf-8")

    result = validate_agent_sample_pipeline(
        source_lagrangians_path=source_path,
        source_n_terms=entry["n_terms"],
        source_local_number=1,
        parameter_samples_path=parameter_path,
        timeout_eom=int(state["pre_sampling_timeout"]),
        timeout_builder=int(state["pre_sampling_timeout"]),
        timeout_solver=600,
        extra_env={
            "SOLVER_SETUP_TIMEOUT_SECONDS": str(state["pre_sampling_timeout"]),
        },
    )
    memory_info = record_attempt(result, memory_dir, loop_id=f"loop_{loop_index:02d}")
    attempt = memory_info["attempt"]
    row = _result_row(
        loop_index=loop_index,
        stage="initial",
        proposal_path=proposal_path,
        source_path=source_path,
        parameter_path=parameter_path,
        result=result,
        attempt=attempt,
    )
    results = [*state.get("results", []), row]
    best = _best_chi2(result)
    skip_reason = _structural_expansion_skip_reason(attempt, best)
    status = "ok" if result.validated else f"fail:{result.failed_stage}"
    print(
        f"[{loop_index:02d}/{state['loop_count']}] initial {status} chi2={result.chi2} "
        f"family={attempt['family_key']} tags={attempt['failure_tags']}",
        flush=True,
    )
    if skip_reason:
        results[-1]["skip_expansion_reason"] = skip_reason
        print(f"[{loop_index:02d}/{state['loop_count']}] skip expanded sampling: {skip_reason}", flush=True)
    return {
        "results": results,
        "initial_record": row,
        "latest_record": row,
        "summary": memory_info["summary"],
        "skip_expansion_reason": skip_reason,
        "messages": _append(state, f"Initial validation completed for loop {loop_index}."),
    }


def validate_expanded(state: GraphAgentState) -> Dict[str, Any]:
    loop_index = int(state["loop_index"])
    proposal_dir = Path(str(state["proposal_dir"]))
    memory_dir = Path(str(state["memory_dir"]))
    source_path = Path(str(state["source_path"]))
    rng = state["rng"]
    entry = state["entry"]
    summary = state.get("summary") or {}
    proposal_summary = summary if bool(state.get("proposal_memory_enabled", True)) else {}

    samples = _parameter_samples(entry, rng, int(state["expanded_parameter_samples"]), proposal_summary)
    proposal = _proposal_for(entry, loop_index, samples, "expanded")
    proposal_path = proposal_dir / f"loop_{loop_index:02d}_expanded.json"
    parameter_path = proposal_dir / f"loop_{loop_index:02d}_expanded_parameter_samples.json"
    proposal_path.write_text(json.dumps(proposal, indent=2, ensure_ascii=False), encoding="utf-8")
    parameter_path.write_text(json.dumps(samples, indent=2, ensure_ascii=False), encoding="utf-8")

    result = validate_agent_sample_pipeline(
        source_lagrangians_path=source_path,
        source_n_terms=entry["n_terms"],
        source_local_number=1,
        parameter_samples_path=parameter_path,
        timeout_eom=int(state["pre_sampling_timeout"]),
        timeout_builder=int(state["pre_sampling_timeout"]),
        timeout_solver=1200,
        extra_env={
            "SOLVER_SETUP_TIMEOUT_SECONDS": str(state["pre_sampling_timeout"]),
        },
    )
    memory_info = record_attempt(result, memory_dir, loop_id=f"loop_{loop_index:02d}_expanded")
    attempt = memory_info["attempt"]
    row = _result_row(
        loop_index=loop_index,
        stage="expanded",
        proposal_path=proposal_path,
        source_path=source_path,
        parameter_path=parameter_path,
        result=result,
        attempt=attempt,
    )
    results = [*state.get("results", []), row]
    status = "ok" if result.validated else f"fail:{result.failed_stage}"
    print(
        f"[{loop_index:02d}/{state['loop_count']}] expanded {status} chi2={result.chi2} "
        f"family={attempt['family_key']} tags={attempt['failure_tags']}",
        flush=True,
    )
    return {
        "results": results,
        "latest_record": row,
        "summary": memory_info["summary"],
        "messages": _append(state, f"Expanded validation completed for loop {loop_index}."),
    }


def reflect_after_validation(state: GraphAgentState) -> Dict[str, Any]:
    record = state.get("latest_record") or {}
    summary = state.get("summary") or {}
    tags = list(record.get("failure_tags") or [])
    chi2 = record.get("chi2")
    quality_tier = chi2_quality_tier(chi2)
    validated = bool(record.get("validated"))
    observations: List[str] = [
        f"loop={record.get('loop')}",
        f"stage={record.get('stage')}",
        f"validated={validated}",
        f"chi2={chi2}",
        f"chi2_quality_tier={quality_tier}",
        f"tags={tags}",
    ]
    if record.get("coarse_family_key"):
        observations.append(f"coarse_family={record.get('coarse_family_key')}")

    if validated and quality_tier == "excellent":
        interpretation = "excellent accepted Solver fit; strongly reinforce shared features"
    elif validated and quality_tier == "competitive":
        interpretation = "competitive accepted Solver fit; reinforce shared features moderately"
    elif validated:
        interpretation = "Solver accepted but chi-square is weak; record as viable but do not strongly reinforce"
    elif "q_initial_root_failure" in tags:
        interpretation = "initial scalar-velocity root did not exist for many samples"
    elif "q_not_determined" in tags:
        interpretation = "scalar RHS could not be determined by the EOM/Builder/Solver chain"
    elif "no_scalar_constraint" in tags:
        interpretation = "no-scalar initial constraint failed"
    elif "constraint_drift" in tags or "integration_failure" in tags:
        interpretation = "numerical trajectory was unstable under sampled parameters"
    elif record.get("failed_stage"):
        interpretation = f"failed at {record.get('failed_stage')}"
    else:
        interpretation = "no accepted sample and no dominant detailed reject reason"

    agent_loop = summary.get("agent_loop") if isinstance(summary.get("agent_loop"), dict) else {}
    structure_prior = agent_loop.get("structure_prior") if isinstance(agent_loop.get("structure_prior"), dict) else {}
    reflection = {
        "loop": record.get("loop"),
        "stage": record.get("stage"),
        "observations": observations,
        "failure_interpretation": interpretation,
        "prefer": {
            "scalar_configs": structure_prior.get("preferred_scalar_configs") or {},
            "features": structure_prior.get("preferred_features") or {},
        },
        "avoid": {
            "failure_tags": structure_prior.get("avoid_failure_tags") or {},
            "scalar_configs": structure_prior.get("avoid_scalar_configs") or {},
            "features": structure_prior.get("avoid_features") or {},
        },
        "information_used": [
            "current graph state",
            "latest harness attempt",
            "current-loop feedback summary",
        ],
        "information_not_used": ["historical solver_result/top10 outputs"],
    }
    return {
        "latest_reflection": reflection,
        "messages": _append(state, f"Reflected on {record.get('stage')} result for loop {record.get('loop')}."),
    }


def decide_after_initial(state: GraphAgentState) -> Dict[str, Any]:
    record = state.get("initial_record") or {}
    skip_reason = state.get("skip_expansion_reason")
    evidence: List[str] = []
    if skip_reason:
        action = "skip_expand"
        reason = str(skip_reason)
        evidence.append(str(skip_reason))
    else:
        chi2 = record.get("chi2")
        try:
            should_expand = chi2 is None or float(chi2) >= float(state["expansion_chi2"])
        except (TypeError, ValueError):
            should_expand = True
        if should_expand:
            action = "expand"
            reason = "initial result did not meet expansion chi-square threshold and was not a structural skip"
            evidence.append(f"chi2={chi2}, expansion_chi2={state.get('expansion_chi2')}")
        else:
            action = "next_theory"
            reason = "initial result is accepted below expansion threshold"
            evidence.append(f"chi2={chi2} < expansion_chi2={state.get('expansion_chi2')}")

    decision = {
        "loop": record.get("loop"),
        "after_stage": "initial",
        "action": action,
        "reason": reason,
        "evidence": evidence,
    }
    results = list(state.get("results", []))
    if results:
        results[-1] = {**results[-1], "decision": decision}
    return {
        "decision": decision,
        "next_action": action,
        "results": results,
        "messages": _append(state, f"Decision after initial: {action}."),
    }


def decide_after_expanded(state: GraphAgentState) -> Dict[str, Any]:
    record = state.get("latest_record") or {}
    action = "next_theory"
    reason = "expanded validation completed"
    decision = {
        "loop": record.get("loop"),
        "after_stage": "expanded",
        "action": action,
        "reason": reason,
        "evidence": [f"chi2={record.get('chi2')}"],
    }
    results = list(state.get("results", []))
    if results:
        results[-1] = {**results[-1], "decision": decision}
    return {
        "decision": decision,
        "next_action": action,
        "results": results,
        "messages": _append(state, f"Decision after expanded: {action}."),
    }


def write_loop_trace(state: GraphAgentState) -> Dict[str, Any]:
    loop_index = int(state.get("loop_index", 0))
    proposal_dir = Path(str(state["proposal_dir"]))
    loop_results = [row for row in state.get("results", []) if row.get("loop") == loop_index]
    trace = {
        "loop": loop_index,
        "entry_family": loop_results[0].get("family_key") if loop_results else None,
        "results": loop_results,
        "reflection": state.get("latest_reflection") or {},
        "decision": state.get("decision") or {},
        "summary_after_loop": {
            "total_attempts": (state.get("summary") or {}).get("total_attempts"),
            "validated_count": (state.get("summary") or {}).get("validated_count"),
            "best_chi2": (state.get("summary") or {}).get("best_chi2"),
            "failure_tag_counts": (state.get("summary") or {}).get("failure_tag_counts"),
        },
    }
    traces = [*state.get("loop_traces", []), trace]
    trace_path = proposal_dir / "loop_trace.jsonl"
    with trace_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(trace, ensure_ascii=False) + "\n")
    return {
        "loop_traces": traces,
        "messages": _append(state, f"Wrote loop trace for loop {loop_index}."),
    }


def advance_loop(state: GraphAgentState) -> Dict[str, Any]:
    return {
        "loop_index": int(state.get("loop_index", 1)) + 1,
        "messages": _append(state, "Advancing to next loop."),
    }


def finalize_run(state: GraphAgentState) -> Dict[str, Any]:
    proposal_dir = Path(str(state["proposal_dir"]))
    memory_dir = Path(str(state["memory_dir"]))
    final_summary = _load_summary(memory_dir)
    messages = list(state.get("messages", []))
    report_dir = ROOT / "ai_theory_lab" / "reports" / str(state["run_name"])
    try:
        report_dir = generate_report(str(state["run_name"]), top_n=20, output_dir=report_dir)
        messages.append(f"Generated result report at {report_dir}.")
    except Exception as exc:
        messages.append(f"Result report generation failed: {exc}")
    output = {
        "run_name": state["run_name"],
        "proposal_dir": str(proposal_dir),
        "memory_dir": str(memory_dir),
        "report_dir": str(report_dir),
        "results": state.get("results", []),
        "loop_traces": state.get("loop_traces", []),
        "summary": final_summary,
        "messages": messages,
        "orchestrator": "langgraph",
    }
    (proposal_dir / "run_summary.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    messages.append("Wrote graph run summary.")
    return {"summary": final_summary, "messages": messages}


def route_after_initialize(state: GraphAgentState) -> str:
    if bool(state.get("fatal_stop")) or int(state.get("loop_count", 0)) <= 0:
        return "finalize_run"
    return "start_loop"


def route_after_proposal(state: GraphAgentState) -> str:
    if bool(state.get("fatal_stop")) or state.get("next_action") in {"skip_validation", "stop"}:
        return "write_loop_trace"
    return "validate_initial"


def route_after_initial_decision(state: GraphAgentState) -> str:
    if state.get("next_action") == "expand":
        return "validate_expanded"
    return "write_loop_trace"


def route_after_trace(state: GraphAgentState) -> str:
    if bool(state.get("fatal_stop")) or state.get("next_action") == "stop":
        return "finalize_run"
    return "advance_loop"


def route_after_loop(state: GraphAgentState) -> str:
    if int(state.get("loop_index", 1)) > int(state.get("loop_count", 0)):
        return "finalize_run"
    return "start_loop"


def build_graph():
    graph = StateGraph(GraphAgentState)
    graph.add_node("initialize_run", initialize_run)
    graph.add_node("start_loop", start_loop)
    graph.add_node("propose_theory", propose_theory)
    graph.add_node("validate_initial", validate_initial)
    graph.add_node("reflect_after_initial", reflect_after_validation)
    graph.add_node("decide_after_initial", decide_after_initial)
    graph.add_node("validate_expanded", validate_expanded)
    graph.add_node("reflect_after_expanded", reflect_after_validation)
    graph.add_node("decide_after_expanded", decide_after_expanded)
    graph.add_node("write_loop_trace", write_loop_trace)
    graph.add_node("advance_loop", advance_loop)
    graph.add_node("finalize_run", finalize_run)

    graph.set_entry_point("initialize_run")
    graph.add_conditional_edges("initialize_run", route_after_initialize)
    graph.add_edge("start_loop", "propose_theory")
    graph.add_conditional_edges("propose_theory", route_after_proposal)
    graph.add_edge("validate_initial", "reflect_after_initial")
    graph.add_edge("reflect_after_initial", "decide_after_initial")
    graph.add_conditional_edges("decide_after_initial", route_after_initial_decision)
    graph.add_edge("validate_expanded", "reflect_after_expanded")
    graph.add_edge("reflect_after_expanded", "decide_after_expanded")
    graph.add_edge("decide_after_expanded", "write_loop_trace")
    graph.add_conditional_edges("write_loop_trace", route_after_trace)
    graph.add_conditional_edges("advance_loop", route_after_loop)
    graph.add_edge("finalize_run", END)
    return graph.compile()


def run_graph_agent(
    *,
    loop_count: int,
    seed: int,
    run_name: Optional[str] = None,
    initial_parameter_samples: int = 1000,
    expanded_parameter_samples: int = 3000,
    expansion_chi2: float = 2000.0,
    pre_sampling_timeout: int = 120,
    grammar_generation_timeout: int = 0,
    use_token_context_cache: bool = True,
    proposal_mode: str = "deterministic",
    llm_model: str = "",
    llm_fallback: str = "deterministic",
    llm_proposal_timeout: int = 600,
    llm_api_timeout: int = 120,
    proposal_memory_enabled: bool = True,
) -> GraphAgentState:
    app = build_graph()
    initial: GraphAgentState = {
        "loop_count": loop_count,
        "seed": seed,
        "run_name": run_name or "",
        "initial_parameter_samples": initial_parameter_samples,
        "expanded_parameter_samples": expanded_parameter_samples,
        "expansion_chi2": expansion_chi2,
        "pre_sampling_timeout": pre_sampling_timeout,
        "grammar_generation_timeout": grammar_generation_timeout,
        "use_token_context_cache": use_token_context_cache,
        "proposal_mode": proposal_mode,
        "llm_model": llm_model,
        "llm_fallback": llm_fallback,
        "llm_proposal_timeout": llm_proposal_timeout,
        "llm_api_timeout": llm_api_timeout,
        "proposal_memory_enabled": proposal_memory_enabled,
        "messages": [],
    }
    return app.invoke(initial)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the LangGraph cold-start theory-discovery agent.")
    parser.add_argument("--loops", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260601)
    parser.add_argument("--run-name")
    parser.add_argument("--initial-parameter-samples", type=int, default=1000)
    parser.add_argument("--expanded-parameter-samples", type=int, default=3000)
    parser.add_argument("--expansion-chi2", type=float, default=2000.0)
    parser.add_argument("--pre-sampling-timeout", type=int, default=120)
    parser.add_argument(
        "--grammar-generation-timeout",
        type=int,
        default=0,
        help="Wall-time limit for token-level Grammar Masker generation. 0 disables this limit.",
    )
    parser.add_argument(
        "--no-token-context-cache",
        action="store_true",
        help="Rebuild token-level Grammar Masker candidate context instead of loading/saving the cache.",
    )
    parser.add_argument(
        "--proposal-mode",
        choices=("deterministic", "llm"),
        default="deterministic",
        help="Select theories deterministically or via OpenAI API choice from grammar-generated candidates.",
    )
    parser.add_argument(
        "--llm-model",
        default="",
        help="OpenAI model for --proposal-mode llm. Defaults to OPENAI_MODEL or gpt-5-mini.",
    )
    parser.add_argument(
        "--llm-fallback",
        choices=("deterministic", "fail"),
        default="deterministic",
        help="When LLM proposal fails, either fall back to deterministic proposal or stop the run.",
    )
    parser.add_argument(
        "--llm-proposal-timeout",
        type=int,
        default=600,
        help="Wall-time limit for LLM candidate generation plus API selection.",
    )
    parser.add_argument(
        "--llm-api-timeout",
        type=int,
        default=120,
        help="HTTP timeout for the OpenAI API candidate-selection call.",
    )
    parser.add_argument(
        "--no-proposal-memory",
        action="store_true",
        help="Do not feed current-loop memory summaries into Lagrangian proposal or parameter sampling.",
    )
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)

    state = run_graph_agent(
        loop_count=args.loops,
        seed=args.seed,
        run_name=args.run_name,
        initial_parameter_samples=args.initial_parameter_samples,
        expanded_parameter_samples=args.expanded_parameter_samples,
        expansion_chi2=args.expansion_chi2,
        pre_sampling_timeout=args.pre_sampling_timeout,
        grammar_generation_timeout=args.grammar_generation_timeout,
        use_token_context_cache=not args.no_token_context_cache,
        proposal_mode=args.proposal_mode,
        llm_model=args.llm_model,
        llm_fallback=args.llm_fallback,
        llm_proposal_timeout=args.llm_proposal_timeout,
        llm_api_timeout=args.llm_api_timeout,
        proposal_memory_enabled=not args.no_proposal_memory,
    )
    output = {
        "run_name": state.get("run_name"),
        "proposal_dir": state.get("proposal_dir"),
        "memory_dir": state.get("memory_dir"),
        "results": state.get("results", []),
        "loop_traces": state.get("loop_traces", []),
        "summary": state.get("summary", {}),
        "messages": state.get("messages", []),
        "orchestrator": "langgraph",
        "proposal_mode": args.proposal_mode,
        "llm_model": args.llm_model,
        "llm_fallback": args.llm_fallback,
        "proposal_memory_enabled": not args.no_proposal_memory,
    }
    print(json.dumps(output, indent=2 if args.pretty else None, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
