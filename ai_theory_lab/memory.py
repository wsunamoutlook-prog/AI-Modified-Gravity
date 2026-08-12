"""Agent-loop memory utilities.

This module records only facts produced by the current discovery loop. It does
not decide how the proposal agent should update its policy.
"""

from __future__ import annotations

from contextlib import contextmanager
import json
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .dataset import (
    DATASET_FILENAME,
    POLICY_SUMMARY_FILENAME,
    consolidate_structure_attempts,
    structure_score_for_attempt,
    summarize_policy,
    training_records_for_attempts,
    write_policy_summary,
    write_training_dataset,
)
from .validation_result import ValidationResult

try:
    import fcntl
except ImportError:  # pragma: no cover - non-Unix fallback
    fcntl = None


HISTORY_FILENAME = "attempt_history.jsonl"
SUMMARY_FILENAME = "feedback_summary.json"
REFLECTION_PROMPT_FILENAME = "reflection_prompt.md"


@contextmanager
def _memory_lock(memory_dir: Path):
    """Serialize memory rewrites when async validation tasks finish."""

    lock_path = memory_dir / ".memory.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a", encoding="utf-8") as lock_file:
        if fcntl is not None:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _read_json(path: Path) -> Optional[Any]:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _load_attempts(memory_dir: Path) -> List[Dict[str, Any]]:
    path = memory_dir / HISTORY_FILENAME
    if not path.exists():
        return []
    attempts: List[Dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                attempts.append(json.loads(line))
    return attempts


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _metadata_from_result(result: ValidationResult) -> Dict[str, Any]:
    diagnostics = result.diagnostics or {}
    metadata = diagnostics.get("agent_lagrangian")
    if isinstance(metadata, dict):
        return metadata

    run_dir = diagnostics.get("agent_run_dir")
    if not run_dir:
        return {}
    loaded = _read_json(Path(str(run_dir)) / "agent_lagrangian_metadata.json")
    return loaded if isinstance(loaded, dict) else {}


def _proposal_from_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    proposal_path = metadata.get("proposal_path")
    if not proposal_path:
        return {}
    proposal = _read_json(Path(str(proposal_path)))
    return proposal if isinstance(proposal, dict) else {}


def _parameter_sample_count(metadata: Dict[str, Any], proposal: Dict[str, Any]) -> Optional[int]:
    samples = proposal.get("parameter_samples")
    if isinstance(samples, list):
        return len(samples)
    sample_path = metadata.get("agent_parameter_samples_path")
    if sample_path:
        data = _read_json(Path(str(sample_path)))
        if isinstance(data, list):
            return len(data)
        if isinstance(data, dict) and isinstance(data.get("samples"), list):
            return len(data["samples"])
    return None


def _operator_labels(value: Any) -> Any:
    if not isinstance(value, list):
        return value
    labels: List[str] = []
    for item in value:
        if isinstance(item, dict):
            labels.append(str(item.get("candidate") or item.get("label") or item))
        else:
            labels.append(str(item))
    return labels


def _theory_track_from_operators(operators: Any) -> str:
    labels = _operator_labels(operators)
    if not isinstance(labels, list):
        labels = []
    if "R" in labels:
        return "eh_anchored"
    if any("R" in str(label) for label in labels):
        return "non_eh"
    return "non_gravity"


def _theory_from(metadata: Dict[str, Any], proposal: Dict[str, Any]) -> Dict[str, Any]:
    theory = proposal.get("theory")
    if not isinstance(theory, dict):
        theory = {}
    operators = _operator_labels(theory.get("operators", metadata.get("operators") or metadata.get("general")))
    track = (
        theory.get("theory_track")
        or proposal.get("theory_track")
        or metadata.get("theory_track")
        or _theory_track_from_operators(operators)
    )
    return {
        "proposal_id": proposal.get("proposal_id") or metadata.get("proposal_id"),
        "proposal_group": theory.get("proposal_group") or proposal.get("proposal_group") or metadata.get("proposal_group"),
        "source_n_terms": metadata.get("source_n_terms"),
        "source_local_number": metadata.get("source_local_number"),
        "scalar_config": theory.get("scalar_config", metadata.get("scalar_config")),
        "potential_types": theory.get("potential_types", metadata.get("potential_types")),
        "operators": operators,
        "theory_track": track,
        "parameter_sample_count": _parameter_sample_count(metadata, proposal),
    }


def _stage_tail(result: ValidationResult) -> Dict[str, Any]:
    if not result.stages:
        return {}
    last = result.stages[-1]
    return {
        "stage": last.stage,
        "returncode": last.returncode,
        "stdout_tail": last.stdout_tail,
        "stderr_tail": last.stderr_tail,
    }


def _reason_text(result: ValidationResult) -> str:
    diagnostics = result.diagnostics or {}
    parts: List[str] = []
    message = diagnostics.get("message")
    if message:
        parts.append(str(message))
    for row in diagnostics.get("top_reject_reasons") or []:
        if isinstance(row, dict):
            reason = row.get("reason")
            count = row.get("count")
            if reason:
                parts.append(f"{reason} (count={count})")
    if result.validated and not parts:
        return ""
    tail = _stage_tail(result)
    if tail.get("stderr_tail"):
        parts.append(str(tail["stderr_tail"]))
    if tail.get("stdout_tail"):
        parts.append(str(tail["stdout_tail"]))
    return "\n".join(parts)


def _failure_tags(result: ValidationResult) -> List[str]:
    text = _reason_text(result).lower()
    tags: List[str] = []
    patterns = [
        ("pre_sampling_timeout", r"pre[- ]sampling.*timeout|before sampling.*timeout|generation.*exceeded|setup/lambdify.*exceeded"),
        ("q_initial_root_failure", r"no acceptable real q[12]_0 root|q[12]_0 root from e_n"),
        ("no_scalar_constraint", r"no[- ]scalar|no scalar"),
        ("h_absurdly_large", r"h\(z\) absurdly large|absurdly large"),
        ("constraint_drift", r"constraint drift|constraint.*too large"),
        ("q_not_determined", r"q[12]_x not determined|not determined"),
        ("symbolic_timeout", r"symbolic build timeout|timeout"),
        ("missing_ranking", r"no model_ranking|missing model_ranking|could not read.*ranking"),
        ("no_accepted_samples", r"no accepted|accepted_samples=0"),
        ("integration_failure", r"integration failed|solve_ivp failed|ivp failed"),
    ]
    for tag, pattern in patterns:
        if re.search(pattern, text):
            tags.append(tag)
    return tags


def _family_key(theory: Dict[str, Any]) -> str:
    operators = theory.get("operators")
    if isinstance(operators, list):
        op_text = "+".join(str(op) for op in operators)
    else:
        op_text = str(operators)
    return (
        f"scalar={theory.get('scalar_config')}|"
        f"potential={theory.get('potential_types')}|"
        f"operators={op_text}"
    )


def _coarse_family_key(theory: Dict[str, Any]) -> str:
    operators = theory.get("operators") if isinstance(theory.get("operators"), list) else []
    joined = " ".join(str(op) for op in operators)
    potential_types = theory.get("potential_types") if isinstance(theory.get("potential_types"), dict) else {}
    buckets: List[str] = []
    if "R" in operators:
        buckets.append("R_anchor")
    if "∇" in joined or "nabla" in joined:
        buckets.append("derivative")
    if any(("R · R" in str(op)) or ("R^{ab}" in str(op)) or ("R_{ab}" in str(op)) for op in operators):
        buckets.append("high_curvature")
    if any(("φ" in str(op)) and ("R" in str(op)) for op in operators):
        buckets.append("scalar_curvature")
    if not buckets:
        buckets.append("plain")
    return (
        f"scalar={theory.get('scalar_config')}|"
        f"phi1_potential={potential_types.get('phi1')}|"
        f"phi2_potential={potential_types.get('phi2')}|"
        f"operator_bucket={'+'.join(sorted(buckets))}"
    )


def make_attempt_record(
    result: ValidationResult,
    loop_id: Optional[str] = None,
    *,
    attempt_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    metadata = _metadata_from_result(result)
    proposal = _proposal_from_metadata(metadata)
    theory = _theory_from(metadata, proposal)
    entered_stages = [stage.stage for stage in result.stages]
    context = attempt_context if isinstance(attempt_context, dict) else {}
    record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "loop_id": loop_id,
        "validated": result.validated,
        "failed_stage": result.failed_stage,
        "entered_stages": entered_stages,
        "entered_solver": "Solver" in entered_stages,
        "best_lag_id": result.best_lag_id,
        "chi2": result.chi2,
        "aic": result.aic,
        "bic": result.bic,
        "k_params": result.k_params,
        "k_parameter_names": list(result.k_parameter_names),
        "validation_stage": context.get("validation_stage"),
        "structure_trial_id": context.get("structure_trial_id"),
        "scheduler_task_id": context.get("scheduler_task_id"),
        "expanded_from_task_id": context.get("expanded_from_task_id"),
        "refine_from_task_id": context.get("refine_from_task_id"),
        "solver_output_dir": result.solver_output_dir,
        "model_ranking_path": result.model_ranking_path,
        "scan_report_path": result.scan_report_path,
        "theory": theory,
        "theory_track": theory.get("theory_track"),
        "proposal_group": theory.get("proposal_group"),
        "family_key": _family_key(theory),
        "coarse_family_key": _coarse_family_key(theory),
        "failure_tags": _failure_tags(result),
        "top_reject_reasons": (result.diagnostics or {}).get("top_reject_reasons") or [],
        "all_samples_summary_path": (result.diagnostics or {}).get("all_samples_summary_path"),
        "accepted_samples_summary_path": (result.diagnostics or {}).get("accepted_samples_summary_path"),
        "reject_reasons_by_model_path": (result.diagnostics or {}).get("reject_reasons_by_model_path"),
        "diagnostic_message": (result.diagnostics or {}).get("message"),
        "agent_lagrangian": (result.diagnostics or {}).get("agent_lagrangian"),
    }
    return record


def _counter_dict(counter: Counter) -> Dict[str, int]:
    return dict(counter.most_common())


def _summarize_by_family(attempts: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for attempt in attempts:
        grouped[str(attempt.get("family_key"))].append(attempt)

    rows: List[Dict[str, Any]] = []
    for family_key, items in grouped.items():
        chi2_values = [float(a["chi2"]) for a in items if a.get("chi2") is not None]
        aic_values = [float(a["aic"]) for a in items if a.get("aic") is not None]
        structure_scores = [score for a in items if (score := structure_score_for_attempt(a)) is not None]
        failed_stages = Counter(str(a.get("failed_stage")) for a in items if a.get("failed_stage"))
        tags = Counter(tag for a in items for tag in a.get("failure_tags", []))
        rows.append(
            {
                "family_key": family_key,
                "attempts": len(items),
                "validated": sum(1 for a in items if a.get("validated")),
                "entered_solver": sum(1 for a in items if a.get("entered_solver")),
                "failed_stage_counts": _counter_dict(failed_stages),
                "failure_tag_counts": _counter_dict(tags),
                "best_chi2": min(chi2_values) if chi2_values else None,
                "best_aic": min(aic_values) if aic_values else None,
                "best_structure_score": min(structure_scores) if structure_scores else None,
            }
        )
    rows.sort(key=lambda r: (-(r["attempts"]), r["best_chi2"] is None, r["best_chi2"] or 0.0))
    return rows


def _summarize_by_coarse_family(attempts: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for attempt in attempts:
        grouped[str(attempt.get("coarse_family_key"))].append(attempt)

    rows: List[Dict[str, Any]] = []
    for family_key, items in grouped.items():
        chi2_values = [float(a["chi2"]) for a in items if a.get("chi2") is not None]
        aic_values = [float(a["aic"]) for a in items if a.get("aic") is not None]
        structure_scores = [score for a in items if (score := structure_score_for_attempt(a)) is not None]
        failed_stages = Counter(str(a.get("failed_stage")) for a in items if a.get("failed_stage"))
        tags = Counter(tag for a in items for tag in a.get("failure_tags", []))
        rows.append(
            {
                "coarse_family_key": family_key,
                "attempts": len(items),
                "validated": sum(1 for a in items if a.get("validated")),
                "entered_solver": sum(1 for a in items if a.get("entered_solver")),
                "failed_stage_counts": _counter_dict(failed_stages),
                "failure_tag_counts": _counter_dict(tags),
                "best_chi2": min(chi2_values) if chi2_values else None,
                "best_aic": min(aic_values) if aic_values else None,
                "best_structure_score": min(structure_scores) if structure_scores else None,
            }
        )
    rows.sort(key=lambda r: (-(r["attempts"]), r["best_chi2"] is None, r["best_chi2"] or 0.0))
    return rows


def _summarize_by_track(attempts: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for attempt in attempts:
        theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
        track = attempt.get("theory_track") or theory.get("theory_track") or _theory_track_from_operators(theory.get("operators"))
        grouped[str(track)].append(attempt)

    summary: Dict[str, Any] = {}
    for track, items in grouped.items():
        chi2_values = [float(a["chi2"]) for a in items if a.get("chi2") is not None]
        aic_values = [float(a["aic"]) for a in items if a.get("aic") is not None]
        tags = Counter(tag for a in items for tag in a.get("failure_tags", []))
        summary[track] = {
            "attempts": len(items),
            "validated": sum(1 for a in items if a.get("validated")),
            "accepted_rate": sum(1 for a in items if a.get("validated")) / len(items) if items else 0.0,
            "best_chi2": min(chi2_values) if chi2_values else None,
            "best_aic": min(aic_values) if aic_values else None,
            "failure_tag_counts": _counter_dict(tags),
        }
    return summary


def _summarize_by_group(attempts: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for attempt in attempts:
        theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
        group = attempt.get("proposal_group") or theory.get("proposal_group") or "unknown"
        grouped[str(group)].append(attempt)

    summary: Dict[str, Any] = {}
    for group, items in grouped.items():
        chi2_values = [float(a["chi2"]) for a in items if a.get("chi2") is not None]
        aic_values = [float(a["aic"]) for a in items if a.get("aic") is not None]
        tags = Counter(tag for a in items for tag in a.get("failure_tags", []))
        summary[group] = {
            "attempts": len(items),
            "validated": sum(1 for a in items if a.get("validated")),
            "accepted_rate": sum(1 for a in items if a.get("validated")) / len(items) if items else 0.0,
            "best_chi2": min(chi2_values) if chi2_values else None,
            "best_aic": min(aic_values) if aic_values else None,
            "failure_tag_counts": _counter_dict(tags),
        }
    return summary


def summarize_attempts(attempts: List[Dict[str, Any]]) -> Dict[str, Any]:
    chi2_attempts = [a for a in attempts if a.get("chi2") is not None]
    failed_stages = Counter(str(a.get("failed_stage")) for a in attempts if a.get("failed_stage"))
    failure_tags = Counter(tag for a in attempts for tag in a.get("failure_tags", []))
    scalar_configs = Counter(str((a.get("theory") or {}).get("scalar_config")) for a in attempts)
    groups = Counter(str(a.get("proposal_group") or (a.get("theory") or {}).get("proposal_group") or "unknown") for a in attempts)
    accepted_groups = Counter(
        str(a.get("proposal_group") or (a.get("theory") or {}).get("proposal_group") or "unknown")
        for a in attempts
        if a.get("validated")
    )
    tracks = Counter(
        str(
            a.get("theory_track")
            or (a.get("theory") or {}).get("theory_track")
            or _theory_track_from_operators((a.get("theory") or {}).get("operators"))
        )
        for a in attempts
    )
    accepted_tracks = Counter(
        str(
            a.get("theory_track")
            or (a.get("theory") or {}).get("theory_track")
            or _theory_track_from_operators((a.get("theory") or {}).get("operators"))
        )
        for a in attempts
        if a.get("validated")
    )
    top_chi2 = sorted(chi2_attempts, key=lambda a: float(a["chi2"]))[:10]
    structure_attempts = consolidate_structure_attempts(attempts)
    top_structure = sorted(
        [attempt for attempt in structure_attempts if structure_score_for_attempt(attempt) is not None],
        key=lambda attempt: float(structure_score_for_attempt(attempt)),
    )[:10]

    training_records = training_records_for_attempts(attempts)
    policy_summary = summarize_policy(training_records)
    return {
        "total_attempts": len(attempts),
        "validated_count": sum(1 for a in attempts if a.get("validated")),
        "entered_solver_count": sum(1 for a in attempts if a.get("entered_solver")),
        "structure_trial_count": len(structure_attempts),
        "failed_stage_counts": _counter_dict(failed_stages),
        "failure_tag_counts": _counter_dict(failure_tags),
        "scalar_config_counts": _counter_dict(scalar_configs),
        "proposal_group_counts": _counter_dict(groups),
        "accepted_proposal_group_counts": _counter_dict(accepted_groups),
        "theory_track_counts": _counter_dict(tracks),
        "accepted_theory_track_counts": _counter_dict(accepted_tracks),
        "best_chi2": float(top_chi2[0]["chi2"]) if top_chi2 else None,
        "best_attempt": top_chi2[0] if top_chi2 else None,
        "top_chi2_attempts": top_chi2,
        "best_structure_score": structure_score_for_attempt(top_structure[0]) if top_structure else None,
        "best_structure_attempt": top_structure[0] if top_structure else None,
        "top_structure_attempts": top_structure,
        "by_family": _summarize_by_family(structure_attempts),
        "by_coarse_family": _summarize_by_coarse_family(structure_attempts),
        "by_proposal_group": _summarize_by_group(attempts),
        "by_theory_track": _summarize_by_track(attempts),
        "policy": policy_summary,
    }


def write_reflection_prompt(memory_dir: Path, summary: Dict[str, Any]) -> Path:
    path = memory_dir / REFLECTION_PROMPT_FILENAME
    prompt = f"""# Agent Reflection Input

Use only the current-loop facts below. Do not use historical `solver_result/`
outputs, old top-10 plots, or remembered best-fit parameters.

The harness is not telling you how to update your proposal policy. Your job is
to infer what to try next from the facts.

If successful low-AIC structure trials share features, such as `phi1_only`, an
`R` anchor, or a simple scalar-curvature coupling, explain whether you will
raise the sampling probability of those features. If the first 1000 samples for
a theory have no accepted chi-square and mostly structural rejection reasons
such as `no_scalar_constraint`, `q_not_determined`, pre-sampling timeout, or
symbolic timeout, explain why you will change structure instead of only adding
more parameter samples.

## Current-Loop Facts

```json
{json.dumps(summary, indent=2, ensure_ascii=False)}
```

## Required Reflection Output

Write a JSON object with these fields before generating the next proposal:

```json
{{
  "observations": ["facts noticed from the current-loop summary"],
  "hypotheses_about_failures": ["your own explanation of why failures happened"],
  "hypotheses_about_successes": ["your own explanation of why any successful low-AIC structures worked"],
  "next_proposal_plan": "what you will try next and why",
  "information_used": ["paths or facts used; must be current-loop only"],
  "information_not_used": ["confirm historical solver_result/top10 data was not used"]
}}
```
"""
    path.write_text(prompt, encoding="utf-8")
    return path


def record_attempt(
    result: ValidationResult,
    memory_dir: Path,
    *,
    loop_id: Optional[str] = None,
    attempt_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    memory_dir = memory_dir.expanduser().resolve()
    memory_dir.mkdir(parents=True, exist_ok=True)

    with _memory_lock(memory_dir):
        attempt = make_attempt_record(result, loop_id=loop_id, attempt_context=attempt_context)
        history_path = memory_dir / HISTORY_FILENAME
        with history_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(attempt, ensure_ascii=False) + "\n")

        attempts = _load_attempts(memory_dir)
        write_training_dataset(attempts, memory_dir / DATASET_FILENAME)
        training_records = training_records_for_attempts(attempts)
        policy_summary = write_policy_summary(training_records, memory_dir / POLICY_SUMMARY_FILENAME)
        summary = summarize_attempts(attempts)
        summary["policy"] = policy_summary
        from .agent_loop import update_agent_loop_state

        summary["agent_loop"] = update_agent_loop_state(memory_dir, summary)
        _write_json(memory_dir / SUMMARY_FILENAME, summary)
        reflection_prompt_path = write_reflection_prompt(memory_dir, summary)

    return {
        "memory_dir": str(memory_dir),
        "attempt_history_path": str(history_path),
        "feedback_summary_path": str(memory_dir / SUMMARY_FILENAME),
        "reflection_prompt_path": str(reflection_prompt_path),
        "attempt": attempt,
        "summary": summary,
    }
