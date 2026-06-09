"""Mini-batch cold-start agent runner.

Each wave proposes several grammar-legal Lagrangians, validates them together
through EOM -> Builder -> Solver, and records one memory attempt per Lagrangian.
Solver can then use its existing per-model multiprocessing to keep cluster CPUs
busy while memory is still updated between waves.
"""

from __future__ import annotations

import argparse
import csv
import json
import pickle
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from gr_grammar_masker_v3_2.runner import _register_dynamic_functions_for_pickle

from .cold_start_runner import (
    _build_token_level_context,
    _generate_token_level_entry,
    _load_summary,
    _parameter_samples,
    _proposal_for,
    _wall_timeout,
    _write_token_level_context_summary,
)
from .harness import ROOT, _run_stage, read_best_result, solver_feedback_paths, summarize_reject_reasons
from .memory import record_attempt
from .report import generate_report
from .validation_result import StageResult, ValidationResult


def _agent_run_dir(run_name: str, wave_index: int) -> Path:
    path = ROOT / "ai_theory_lab" / "runs" / f"{run_name}_wave_{wave_index:04d}"
    path.mkdir(parents=True, exist_ok=False)
    return path


def _group_lagrangians(entries: List[Dict[str, Any]]) -> Tuple[Dict[int, List[Dict[str, Any]]], Dict[int, str]]:
    grouped_pairs: Dict[int, List[Tuple[int, Dict[str, Any]]]] = {}
    for entry_index, entry in enumerate(entries):
        lagrangian = dict(entry["lagrangian"])
        n_terms = int(lagrangian["n_terms"])
        grouped_pairs.setdefault(n_terms, []).append((entry_index, lagrangian))

    grouped: Dict[int, List[Dict[str, Any]]] = {
        n_terms: [lagrangian for _, lagrangian in pairs]
        for n_terms, pairs in grouped_pairs.items()
    }
    lag_ids: Dict[int, str] = {}
    global_idx = 1
    for n_terms in sorted(grouped_pairs):
        for entry_index, _lagrangian in grouped_pairs[n_terms]:
            lag_ids[entry_index] = str(global_idx)
            global_idx += 1
    return grouped, lag_ids


def _write_batch_lagrangians(entries: List[Dict[str, Any]], path: Path) -> Dict[int, str]:
    payload, lag_ids = _group_lagrangians(entries)
    _register_dynamic_functions_for_pickle(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)
    return lag_ids


def _read_csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _best_by_lag_id(solver_output_dir: Path) -> Dict[str, Dict[str, str]]:
    rows = _read_csv_rows(solver_output_dir / "model_ranking.csv")
    best: Dict[str, Dict[str, str]] = {}
    for row in rows:
        lag_id = str(row.get("lag_id", ""))
        if not lag_id:
            continue
        current = best.get(lag_id)
        if current is None or (float(row["chi2"]), float(row.get("AIC", "inf"))) < (
            float(current["chi2"]),
            float(current.get("AIC", "inf")),
        ):
            best[lag_id] = row
    return best


def _rejects_for_lag_id(solver_output_dir: Path, lag_id: str) -> List[Dict[str, str]]:
    rows = [row for row in _read_csv_rows(solver_output_dir / "reject_reasons_by_model.csv") if str(row.get("lag_id")) == str(lag_id)]
    rows.sort(key=lambda row: int(row.get("count") or 0), reverse=True)
    return rows[:12]


def _metadata_for_entry(
    *,
    entry: Dict[str, Any],
    proposal_path: Path,
    batch_lagrangians_path: Path,
    parameter_samples_path: Path,
    lag_id: str,
) -> Dict[str, Any]:
    lagrangian = entry["lagrangian"]
    report_lagrangian = {
        "n_terms": lagrangian.get("n_terms"),
        "general": lagrangian.get("general"),
        "terms": lagrangian.get("terms") or [],
        "scalar_config": lagrangian.get("scalar_config"),
        "potential_types": lagrangian.get("potential_types"),
    }
    return {
        "proposal_path": str(proposal_path),
        "agent_lagrangians_path": str(batch_lagrangians_path),
        "agent_parameter_samples_path": str(parameter_samples_path),
        "proposal_id": f"batch_lag_{lag_id}",
        "source": "batch_token_level_grammar",
        "source_n_terms": int(entry["n_terms"]),
        "source_local_number": int(entry["local_number"]),
        "batch_lag_id": str(lag_id),
        "scalar_config": entry["scalar_config"],
        "potential_types": entry["potential_types"],
        "operators": entry["operators"],
        "operator_specs": entry["operator_specs"],
        "general": entry["general"],
        "lagrangian": report_lagrangian,
    }


def _stage_specs(
    *,
    agent_dir: Path,
    batch_lagrangians_path: Path,
    parameter_samples_path: Path,
    solver_parallel: bool,
    n_workers: int,
    timeout_setup: int,
) -> List[Tuple[str, List[str], int, Dict[str, str]]]:
    eom_dir = agent_dir / "agent_eom_results"
    builder_output_dir = agent_dir / "agent_builder_result"
    solver_output_base = agent_dir / "agent_solver_result"
    build_cache_path = agent_dir / "agent_built_models_cache.pkl"
    common = {
        "SOLVER_SETUP_TIMEOUT_SECONDS": str(timeout_setup),
    }
    return [
        (
            "EOM",
            ["EOM v5.2.py"],
            timeout_setup,
            {
                **common,
                "EOM_LAGRANGIANS_PATH": str(batch_lagrangians_path),
                "EOM_OUTPUT_DIR": str(eom_dir),
                "EOM_MAX_TERMS": "all",
                "EOM_N_SAMPLES": "all",
                "EOM_RUN_SELF_TEST": "0",
            },
        ),
        (
            "Builder",
            ["Builder v5.2.py"],
            timeout_setup,
            {
                **common,
                "EOM_SUMMARY_PATH": str(eom_dir / "eom_summary.txt"),
                "SOLVER_OUTPUT_DIR": str(builder_output_dir),
                "SOLVER_RUN_NAME": "agent_build",
                "BUILD_CACHE_PATH": str(build_cache_path),
                "MAX_MODELS_TO_BUILD": "0",
            },
        ),
        (
            "Solver",
            ["Solver v5.2.py"],
            max(600, timeout_setup * 5),
            {
                **common,
                "BUILD_CACHE_PATH": str(build_cache_path),
                "SOLVER_OUTPUT_DIR": str(solver_output_base),
                "SOLVER_RUN_NAME": "agent_solve",
                "MAX_MODELS_TO_BUILD": "0",
                "SOLVER_MAKE_PLOTS": "0",
                "TOP_N": "0",
                "PARAMETER_SAMPLES_PATH": str(parameter_samples_path),
                "SOLVER_PARALLEL": "1" if solver_parallel else "0",
                "N_WORKERS": str(n_workers),
            },
        ),
    ]


def _validation_for_entry(
    *,
    lag_id: str,
    stages: List[StageResult],
    solver_output_dir: Path,
    metadata: Dict[str, Any],
) -> ValidationResult:
    best_rows = _best_by_lag_id(solver_output_dir)
    row = best_rows.get(str(lag_id))
    diagnostics = {
        "agent_run_dir": str(solver_output_dir.parents[1]),
        "agent_lagrangian": metadata,
        "top_reject_reasons": _rejects_for_lag_id(solver_output_dir, lag_id),
        **solver_feedback_paths(solver_output_dir),
    }
    if row is None:
        return ValidationResult(
            validated=False,
            failed_stage="Solver",
            best_lag_id=str(lag_id),
            solver_output_dir=str(solver_output_dir),
            stages=stages,
            diagnostics={**diagnostics, "message": f"No accepted ranking row for lag_id={lag_id}."},
        )
    return ValidationResult(
        validated=True,
        best_lag_id=str(lag_id),
        chi2=float(row["chi2"]),
        aic=float(row["AIC"]),
        bic=float(row["BIC"]),
        solver_output_dir=str(solver_output_dir),
        model_ranking_path=str(solver_output_dir / "model_ranking.csv"),
        scan_report_path=str(solver_output_dir / "scan_report.txt"),
        stages=stages,
        diagnostics=diagnostics,
    )


def _proposal_entry(
    *,
    context: Dict[str, Any],
    summary: Dict[str, Any],
    rng: random.Random,
    seed: int,
    proposal_mode: str,
    llm_model: str,
    llm_fallback: str,
    llm_api_timeout: int,
    debug_dir: Path,
    loop_id: str,
) -> Dict[str, Any]:
    if proposal_mode == "llm":
        try:
            from .llm_agent import propose_entry_with_llm

            return propose_entry_with_llm(
                context,
                summary,
                rng,
                seed,
                model=llm_model or None,
                api_timeout=llm_api_timeout,
                debug_dir=debug_dir,
                loop_id=loop_id,
            )
        except Exception:
            if llm_fallback == "fail":
                raise
    return _generate_token_level_entry(context, summary, rng, seed)


def run_batch_agent(
    *,
    waves: int,
    batch_size: int,
    seed: int,
    run_name: Optional[str],
    initial_parameter_samples: int,
    timeout_setup: int,
    proposal_mode: str,
    llm_model: str,
    llm_fallback: str,
    llm_api_timeout: int,
    use_token_context_cache: bool,
    n_workers: int,
) -> Dict[str, Any]:
    name = run_name or f"graph_agent_batch_{waves}x{batch_size}_{time.strftime('%Y%m%d_%H%M%S')}"
    proposal_dir = ROOT / "ai_theory_lab" / "proposals" / name
    memory_dir = ROOT / "ai_theory_lab" / "memory" / name
    proposal_dir.mkdir(parents=True, exist_ok=False)
    memory_dir.mkdir(parents=True, exist_ok=False)
    rng = random.Random(seed)
    context = _build_token_level_context(0, use_cache=use_token_context_cache)
    _write_token_level_context_summary(context, proposal_dir / "operator_catalog_summary.json")
    messages = [f"Initialized batch run {name}."]
    traces: List[Dict[str, Any]] = []

    for wave_index in range(1, waves + 1):
        summary = _load_summary(memory_dir)
        proposal_summary = summary
        entries: List[Dict[str, Any]] = []
        seen_families: set[str] = set()
        attempts = 0
        while len(entries) < batch_size and attempts < batch_size * 5:
            attempts += 1
            loop_id = f"wave_{wave_index:04d}_item_{len(entries) + 1:02d}"
            entry = _proposal_entry(
                context=context,
                summary=proposal_summary,
                rng=rng,
                seed=seed + wave_index * 1009 + attempts * 37,
                proposal_mode=proposal_mode,
                llm_model=llm_model,
                llm_fallback=llm_fallback,
                llm_api_timeout=llm_api_timeout,
                debug_dir=proposal_dir / "llm_proposal_debug",
                loop_id=loop_id,
            )
            family = json.dumps(
                {
                    "scalar_config": entry.get("scalar_config"),
                    "potential_types": entry.get("potential_types"),
                    "operators": entry.get("operators"),
                },
                sort_keys=True,
                ensure_ascii=False,
            )
            if family in seen_families:
                continue
            seen_families.add(family)
            entries.append(entry)
        if not entries:
            messages.append(f"Wave {wave_index}: no entries generated; stopping.")
            break

        agent_dir = _agent_run_dir(name, wave_index)
        batch_lagrangians_path = agent_dir / "agent_lagrangians.pkl"
        lag_ids = _write_batch_lagrangians(entries, batch_lagrangians_path)
        samples_by_lag_id: Dict[str, List[Dict[str, Any]]] = {}
        proposal_paths: Dict[int, Path] = {}
        parameter_samples_path = agent_dir / "agent_parameter_samples_by_lag_id.json"
        for entry_index, entry in enumerate(entries):
            lag_id = lag_ids[entry_index]
            samples = _parameter_samples(entry, rng, initial_parameter_samples, proposal_summary)
            samples_by_lag_id[lag_id] = samples
            proposal = _proposal_for(entry, wave_index, samples, f"batch_lag_{lag_id}")
            proposal["batch_wave"] = wave_index
            proposal["batch_lag_id"] = lag_id
            proposal_path = proposal_dir / f"wave_{wave_index:04d}_lag_{lag_id}.json"
            proposal_path.write_text(json.dumps(proposal, indent=2, ensure_ascii=False), encoding="utf-8")
            proposal_paths[entry_index] = proposal_path
        parameter_samples_path.write_text(
            json.dumps({"samples_by_lag_id": samples_by_lag_id}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        stages: List[StageResult] = []
        stage_failed: Optional[str] = None
        for stage, cmd, timeout, env in _stage_specs(
            agent_dir=agent_dir,
            batch_lagrangians_path=batch_lagrangians_path,
            parameter_samples_path=parameter_samples_path,
            solver_parallel=True,
            n_workers=n_workers,
            timeout_setup=timeout_setup,
        ):
            result = _run_stage(stage, cmd, python_executable=sys.executable, timeout_seconds=timeout, extra_env=env)
            stages.append(result)
            if not result.ok:
                stage_failed = stage
                break

        solver_output_dir = agent_dir / "agent_solver_result" / "agent_solve"
        wave_records = []
        for entry_index, entry in enumerate(entries):
            lag_id = lag_ids[entry_index]
            metadata = _metadata_for_entry(
                entry=entry,
                proposal_path=proposal_paths[entry_index],
                batch_lagrangians_path=batch_lagrangians_path,
                parameter_samples_path=parameter_samples_path,
                lag_id=lag_id,
            )
            if stage_failed and not (
                stage_failed == "Solver" and (solver_output_dir / "model_ranking.csv").exists()
            ):
                result = ValidationResult(
                    validated=False,
                    failed_stage=stage_failed,
                    best_lag_id=lag_id,
                    solver_output_dir=str(solver_output_dir),
                    stages=stages,
                    diagnostics={
                        "message": f"{stage_failed} failed while validating batch wave {wave_index}.",
                        "agent_run_dir": str(agent_dir),
                        "agent_lagrangian": metadata,
                    },
                )
            else:
                result = _validation_for_entry(
                    lag_id=lag_id,
                    stages=stages,
                    solver_output_dir=solver_output_dir,
                    metadata=metadata,
                )
            memory_info = record_attempt(result, memory_dir, loop_id=f"wave_{wave_index:04d}_lag_{lag_id}")
            wave_records.append(memory_info["attempt"])
        traces.append(
            {
                "wave": wave_index,
                "batch_size": len(entries),
                "agent_run_dir": str(agent_dir),
                "records": wave_records,
            }
        )
        with (proposal_dir / "wave_trace.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(traces[-1], ensure_ascii=False, default=str) + "\n")
        best = min((r.get("chi2") for r in wave_records if r.get("chi2") is not None), default=None)
        messages.append(f"Wave {wave_index}/{waves} complete; best_chi2={best}.")

    final_summary = _load_summary(memory_dir)
    report_dir = ROOT / "ai_theory_lab" / "reports" / name
    try:
        report_dir = generate_report(name, top_n=20, output_dir=report_dir)
        messages.append(f"Generated result report at {report_dir}.")
    except Exception as exc:
        messages.append(f"Result report generation failed: {type(exc).__name__}: {exc}")
    output = {
        "run_name": name,
        "proposal_dir": str(proposal_dir),
        "memory_dir": str(memory_dir),
        "report_dir": str(report_dir),
        "summary": final_summary,
        "wave_traces": traces,
        "messages": messages,
        "orchestrator": "batch",
        "batch_size": batch_size,
    }
    (proposal_dir / "run_summary.json").write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    return output


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run mini-batch cold-start theory discovery.")
    parser.add_argument("--waves", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260607)
    parser.add_argument("--run-name")
    parser.add_argument("--initial-parameter-samples", type=int, default=1000)
    parser.add_argument("--timeout-setup", type=int, default=1200)
    parser.add_argument("--proposal-mode", choices=("deterministic", "llm"), default="deterministic")
    parser.add_argument("--llm-model", default="")
    parser.add_argument("--llm-fallback", choices=("deterministic", "fail"), default="deterministic")
    parser.add_argument("--llm-api-timeout", type=int, default=120)
    parser.add_argument("--no-token-context-cache", action="store_true")
    parser.add_argument("--n-workers", type=int, default=8)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)
    output = run_batch_agent(
        waves=args.waves,
        batch_size=args.batch_size,
        seed=args.seed,
        run_name=args.run_name,
        initial_parameter_samples=args.initial_parameter_samples,
        timeout_setup=args.timeout_setup,
        proposal_mode=args.proposal_mode,
        llm_model=args.llm_model,
        llm_fallback=args.llm_fallback,
        llm_api_timeout=args.llm_api_timeout,
        use_token_context_cache=not args.no_token_context_cache,
        n_workers=args.n_workers,
    )
    print(json.dumps(output, indent=2 if args.pretty else None, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
