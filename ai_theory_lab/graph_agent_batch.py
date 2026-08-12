"""Mini-batch cold-start agent runner.

Each wave proposes several grammar-legal Lagrangians, splits them into runtime
validation buckets, and runs each bucket through EOM -> Builder -> Solver
separately. The default scheduler preserves the old wave-by-wave ordering. The
optional async schedulers keep validation tasks in flight, replenishing from
current-loop memory as soon as a task finishes.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import pickle
import random
import re
import sys
import time
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from gr_grammar_masker_v3_2.runner import _register_dynamic_functions_for_pickle

from .cold_start_runner import (
    _build_token_level_context,
    _generate_token_level_entry,
    _load_summary,
    _parameter_samples,
    _proposal_for,
    theory_track_from_operators,
    _wall_timeout,
    _write_token_level_context_summary,
)
from .harness import ROOT, _run_stage, read_best_result, solver_feedback_paths, summarize_reject_reasons
from .memory import record_attempt
from .report import generate_report
from .tracing import trace_event
from .validation_result import StageResult, ValidationResult


GROUP_SPECS: Dict[str, Dict[str, Any]] = {
    "open_search": {"track": None, "scalar_config": None},
    "non_eh": {"track": "non_eh", "scalar_config": None},
}
OPEN_ONLY_GROUP_MODES = {"open_only", "mixed"}

COMPLEXITY_BUCKET_ORDER = ("simple", "medium", "complex", "very_complex")
NON_EH_SCALAR_FAMILIES = ("phi1_only", "phi2_only", "both", "none")
OPEN_SEARCH_SCALAR_BASELINE_PER_FAMILY = 0.08
NON_EH_SCALAR_BASELINE_PER_FAMILY = 0.15
BATCH_PROPOSAL_TIMEOUT_SECONDS = int(os.environ.get("AGENT_PROPOSAL_TIMEOUT_SECONDS", "300"))
ASYNC_LANES = COMPLEXITY_BUCKET_ORDER
RUNTIME_PRIOR_FILENAME = "runtime_complexity_prior.json"
RUNTIME_PRIOR_MIN_EVIDENCE = 2.0
ASYNC_WAIT_POLL_SECONDS = float(os.environ.get("AGENT_ASYNC_WAIT_POLL_SECONDS", "30"))
ASYNC_SLOW_SIGNAL_INTERVAL_SECONDS = float(os.environ.get("AGENT_ASYNC_SLOW_SIGNAL_INTERVAL_SECONDS", "300"))
ASYNC_TARGET_POLICIES = ("balanced_lane_floors", "global_recorded_total")
DEFAULT_ASYNC_LANE_MIN_FRACTION = float(os.environ.get("AGENT_ASYNC_LANE_MIN_FRACTION", "0.20"))
DEFAULT_ASYNC_SLOT_COUNT = int(os.environ.get("AGENT_ASYNC_SLOT_COUNT", "0") or "0")
DEFAULT_ASYNC_SLOT_WORKERS = int(os.environ.get("AGENT_ASYNC_SLOT_WORKERS", "1") or "1")


def _agent_run_dir(run_name: str, wave_index: int, complexity_bucket: Optional[str] = None) -> Path:
    suffix = f"{run_name}_wave_{wave_index:04d}"
    if complexity_bucket and complexity_bucket != "mixed":
        suffix += f"_{complexity_bucket}"
    path = ROOT / "ai_theory_lab" / "runs" / suffix
    path.mkdir(parents=True, exist_ok=False)
    return path


def _async_agent_run_dir(run_name: str, task_id: str, lane: str) -> Path:
    path = ROOT / "ai_theory_lab" / "runs" / f"{run_name}_{task_id}_{lane}"
    path.mkdir(parents=True, exist_ok=False)
    return path


def _entry_operator_labels(entry: Dict[str, Any]) -> List[str]:
    return [str(operator) for operator in (entry.get("operators") or [])]


def _operator_has_derivatives(label: str) -> bool:
    markers = ("∇", "\\nabla", "Box", "\\Box", "□", "dφ", "partial", "\\partial")
    return any(marker in label for marker in markers)


def _operator_has_high_curvature(label: str) -> bool:
    markers = (
        "R · R",
        "R^2",
        "R_{",
        "R^{",
        "Riemann",
        "Ricci",
        "\\mathcal{R}",
        "\\mathrm{Riemann}",
    )
    return any(marker in label for marker in markers) or label.count("R") >= 2


def _entry_complexity_score(entry: Dict[str, Any]) -> float:
    labels = _entry_operator_labels(entry)
    lagrangian = entry.get("lagrangian") or {}
    terms = lagrangian.get("terms") or []
    n_terms = int(entry.get("n_terms") or lagrangian.get("n_terms") or len(terms) or 0)
    score = float(max(0, len(labels) - 1))
    score += 0.5 * max(0, n_terms - 4)
    if entry.get("scalar_config") == "both":
        score += 1.0

    for label in labels:
        if _operator_has_derivatives(label):
            score += 2.0
        if _operator_has_high_curvature(label):
            score += 1.5
        if "φ1" in label and "φ2" in label:
            score += 1.0
        elif label.count("φ") >= 2:
            score += 0.3

    for term in terms:
        try:
            lambda_power = abs(float(term.get("lambda_power") or 0.0))
        except (TypeError, ValueError):
            lambda_power = 0.0
        try:
            mass_dim = float(term.get("mass_dim") or 0.0)
        except (TypeError, ValueError):
            mass_dim = 0.0
        if lambda_power >= 4:
            score += 0.8
        elif lambda_power >= 3:
            score += 0.4
        if mass_dim >= 6:
            score += 0.5
    return round(score, 3)


def _entry_complexity_bucket(entry: Dict[str, Any]) -> str:
    labels = _entry_operator_labels(entry)
    lagrangian = entry.get("lagrangian") or {}
    n_terms = int(entry.get("n_terms") or lagrangian.get("n_terms") or 0)
    score = _entry_complexity_score(entry)
    has_derivatives = any(_operator_has_derivatives(label) for label in labels)
    has_high_curvature = any(_operator_has_high_curvature(label) for label in labels)
    if len(labels) <= 2 and n_terms <= 4 and not has_derivatives and not has_high_curvature and score < 3.0:
        return "simple"
    if score >= 6.0 or len(labels) >= 5 or n_terms >= 8 or (has_derivatives and has_high_curvature):
        return "complex"
    return "medium"


def _runtime_prior_path(memory_dir: Path) -> Path:
    return memory_dir / RUNTIME_PRIOR_FILENAME


def _load_runtime_prior(memory_dir: Path) -> Dict[str, Any]:
    path = _runtime_prior_path(memory_dir)
    if not path.exists():
        return {"version": 1, "stats": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"version": 1, "stats": {}}
    if not isinstance(data, dict):
        return {"version": 1, "stats": {}}
    data.setdefault("version", 1)
    data.setdefault("stats", {})
    return data


def _write_runtime_prior(memory_dir: Path, prior: Dict[str, Any]) -> None:
    path = _runtime_prior_path(memory_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    prior["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    path.write_text(json.dumps(prior, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")


def _count_bin(value: int, bins: Tuple[int, ...]) -> str:
    for edge in bins:
        if value <= edge:
            return f"<= {edge}"
    return f"> {bins[-1]}"


def _entry_runtime_feature_keys(entry: Dict[str, Any]) -> List[str]:
    labels = _entry_operator_labels(entry)
    lagrangian = entry.get("lagrangian") or {}
    terms = lagrangian.get("terms") or []
    n_terms = int(entry.get("n_terms") or lagrangian.get("n_terms") or len(terms) or 0)
    scalar_config = str(entry.get("scalar_config") or "unknown")
    track = str(entry.get("theory_track") or theory_track_from_operators(labels))
    potential_types = entry.get("potential_types") if isinstance(entry.get("potential_types"), dict) else {}
    has_derivatives = any(_operator_has_derivatives(label) for label in labels)
    has_high_curvature = any(_operator_has_high_curvature(label) for label in labels)
    keys = [
        f"track:{track}",
        f"scalar:{scalar_config}",
        f"operator_count:{_count_bin(len(labels), (1, 2, 4, 6))}",
        f"term_count:{_count_bin(n_terms, (2, 4, 6, 8))}",
        f"structural_bucket:{_entry_complexity_bucket(entry)}",
        f"has_derivatives:{has_derivatives}",
        f"has_high_curvature:{has_high_curvature}",
    ]
    if potential_types:
        keys.append(f"potential_phi1:{potential_types.get('phi1')}")
        keys.append(f"potential_phi2:{potential_types.get('phi2')}")
    if scalar_config == "both":
        keys.append("two_scalar:true")
    if any("φ1" in label and "φ2" in label for label in labels):
        keys.append("mixed_scalar_operator:true")
    for label in labels:
        keys.append(f"operator:{label}")
    return keys


def _add_runtime_sample(
    prior: Dict[str, Any],
    entry: Dict[str, Any],
    seconds_per_entry: float,
    *,
    signal: str,
    weight: float = 1.0,
) -> None:
    if not math.isfinite(seconds_per_entry) or seconds_per_entry <= 0 or weight <= 0:
        return
    stats = prior.setdefault("stats", {})
    target_group = str(entry.get("proposal_group") or "open_search")
    keys = [f"family:{_entry_family_key(target_group, entry)}", *_entry_runtime_feature_keys(entry)]
    alpha = 0.25
    for key in keys:
        stat = stats.setdefault(
            key,
            {
                "count": 0.0,
                "samples": 0,
                "total_weighted_seconds": 0.0,
                "ema_seconds": None,
                "last_seconds": None,
                "last_signal": None,
            },
        )
        old_count = float(stat.get("count") or 0.0)
        old_total = float(stat.get("total_weighted_seconds") or 0.0)
        old_ema = stat.get("ema_seconds")
        stat["count"] = old_count + weight
        stat["samples"] = int(stat.get("samples") or 0) + 1
        stat["total_weighted_seconds"] = old_total + seconds_per_entry * weight
        stat["mean_seconds"] = stat["total_weighted_seconds"] / max(float(stat["count"]), 1e-9)
        stat["ema_seconds"] = (
            seconds_per_entry
            if old_ema is None
            else (alpha * seconds_per_entry + (1.0 - alpha) * float(old_ema))
        )
        stat["last_seconds"] = seconds_per_entry
        stat["last_signal"] = signal


def _predict_runtime_seconds(entry: Dict[str, Any], runtime_prior: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not runtime_prior:
        return None
    stats = runtime_prior.get("stats")
    if not isinstance(stats, dict) or not stats:
        return None
    target_group = str(entry.get("proposal_group") or "open_search")
    weighted_seconds = 0.0
    evidence = 0.0
    sources: List[Dict[str, Any]] = []
    keys = [(f"family:{_entry_family_key(target_group, entry)}", 4.0)]
    keys.extend((key, 1.0) for key in _entry_runtime_feature_keys(entry))
    for key, base_weight in keys:
        stat = stats.get(key)
        if not isinstance(stat, dict):
            continue
        count = float(stat.get("count") or 0.0)
        if count <= 0:
            continue
        seconds = stat.get("ema_seconds")
        if seconds is None:
            seconds = stat.get("mean_seconds")
        try:
            seconds = float(seconds)
        except (TypeError, ValueError):
            continue
        if not math.isfinite(seconds) or seconds <= 0:
            continue
        weight = base_weight * min(3.0, max(0.25, count / 2.0))
        weighted_seconds += seconds * weight
        evidence += weight
        if len(sources) < 6:
            sources.append({"key": key, "seconds": round(seconds, 3), "count": round(count, 3)})
    if evidence < RUNTIME_PRIOR_MIN_EVIDENCE:
        return None
    return {
        "predicted_seconds": weighted_seconds / evidence,
        "evidence": evidence,
        "sources": sources,
    }


def _structural_runtime_fallback_seconds(entry: Dict[str, Any]) -> float:
    structural_bucket = str(entry.get("structural_complexity_bucket") or _entry_complexity_bucket(entry))
    score = float(entry.get("complexity_score") or _entry_complexity_score(entry))
    base = {"simple": 90.0, "medium": 300.0, "complex": 900.0, "very_complex": 1200.0}.get(
        structural_bucket, 300.0
    )
    return round(base + 18.0 * max(0.0, score), 3)


def _update_runtime_prior_from_entries(
    *,
    memory_dir: Path,
    entries: List[Dict[str, Any]],
    elapsed_sec: float,
    signal: str,
    weight: float = 1.0,
) -> None:
    if not entries or not math.isfinite(elapsed_sec) or elapsed_sec <= 0:
        return
    prior = _load_runtime_prior(memory_dir)
    seconds_per_entry = elapsed_sec / max(1, len(entries))
    for entry in entries:
        _add_runtime_sample(prior, entry, seconds_per_entry, signal=signal, weight=weight)
    prior["last_observation"] = {
        "signal": signal,
        "elapsed_sec": elapsed_sec,
        "entry_count": len(entries),
        "seconds_per_entry": seconds_per_entry,
    }
    _write_runtime_prior(memory_dir, prior)


def _update_runtime_prior_from_task(memory_dir: Path, task_result: Dict[str, Any]) -> None:
    elapsed_sec = float(task_result.get("elapsed_sec") or 0.0)
    entries = [
        item.get("entry")
        for item in (task_result.get("result_items") or [])
        if isinstance(item, dict) and isinstance(item.get("entry"), dict)
    ]
    _update_runtime_prior_from_entries(
        memory_dir=memory_dir,
        entries=entries,
        elapsed_sec=elapsed_sec,
        signal="completed",
        weight=1.0,
    )


def _annotate_entry_complexity(entry: Dict[str, Any], runtime_prior: Optional[Dict[str, Any]] = None) -> None:
    score = _entry_complexity_score(entry)
    structural_bucket = _entry_complexity_bucket(entry)
    entry["complexity_score"] = score
    entry["structural_complexity_bucket"] = structural_bucket
    entry["complexity_bucket"] = structural_bucket
    prediction = _predict_runtime_seconds(entry, runtime_prior)
    if prediction is None:
        entry["runtime_sort_seconds"] = _structural_runtime_fallback_seconds(entry)
        entry["runtime_sort_source"] = "structural_fallback"
        return
    predicted_seconds = float(prediction["predicted_seconds"])
    entry["runtime_predicted_seconds"] = round(predicted_seconds, 3)
    entry["runtime_prior_evidence"] = round(float(prediction["evidence"]), 3)
    entry["runtime_prior_sources"] = prediction["sources"]
    entry["runtime_sort_seconds"] = round(predicted_seconds, 3)
    entry["runtime_sort_source"] = "current_loop_runtime_prior"


def _assign_relative_runtime_buckets(entries: List[Dict[str, Any]]) -> None:
    if not entries:
        return
    for entry in entries:
        if "structural_complexity_bucket" not in entry:
            _annotate_entry_complexity(entry)
        if entry.get("runtime_sort_seconds") is None:
            entry["runtime_sort_seconds"] = _structural_runtime_fallback_seconds(entry)
            entry["runtime_sort_source"] = "structural_fallback"

    ranked = sorted(
        enumerate(entries),
        key=lambda item: (
            float(item[1].get("runtime_sort_seconds") or 0.0),
            float(item[1].get("complexity_score") or 0.0),
            item[0],
        ),
    )
    n_entries = len(ranked)
    bucket_order = COMPLEXITY_BUCKET_ORDER
    n_buckets = max(1, len(bucket_order))
    for rank_index, (_original_index, entry) in enumerate(ranked):
        bucket_index = min(n_buckets - 1, int(rank_index * n_buckets / max(1, n_entries)))
        bucket = bucket_order[bucket_index]
        entry["complexity_bucket"] = bucket
        entry["runtime_rank_in_pool"] = rank_index + 1
        entry["runtime_pool_size"] = n_entries
        entry["runtime_quantile_bucket_policy"] = "relative_runtime_quantiles"


def _complexity_batches(
    entries: List[Dict[str, Any]],
    entry_summaries: List[Dict[str, Any]],
    *,
    enabled: bool,
) -> List[Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]]:
    if not enabled:
        for entry in entries:
            entry["complexity_bucket"] = "mixed"
            entry["complexity_score"] = _entry_complexity_score(entry)
        return [("mixed", entries, entry_summaries)]

    buckets: Dict[str, List[Tuple[Dict[str, Any], Dict[str, Any]]]] = {
        bucket: [] for bucket in COMPLEXITY_BUCKET_ORDER
    }
    for entry in entries:
        if "structural_complexity_bucket" not in entry:
            _annotate_entry_complexity(entry)
    _assign_relative_runtime_buckets(entries)
    for entry, summary in zip(entries, entry_summaries):
        buckets.setdefault(str(entry["complexity_bucket"]), []).append((entry, summary))
    split_batches: List[Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]] = []
    for bucket in COMPLEXITY_BUCKET_ORDER:
        pairs = buckets.get(bucket) or []
        if pairs:
            split_batches.append((bucket, [entry for entry, _ in pairs], [summary for _, summary in pairs]))
    return split_batches


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
        "proposal_id": f"{entry.get('validation_wave') or 'batch'}_lag_{lag_id}",
        "source": "batch_token_level_grammar",
        "source_n_terms": int(entry["n_terms"]),
        "source_local_number": int(entry["local_number"]),
        "batch_lag_id": str(lag_id),
        "scalar_config": entry["scalar_config"],
        "potential_types": entry["potential_types"],
        "operators": entry["operators"],
        "operator_specs": entry["operator_specs"],
        "theory_track": entry.get("theory_track") or theory_track_from_operators(entry.get("operators") or []),
        "proposal_group": entry.get("proposal_group"),
        "validation_wave": entry.get("validation_wave"),
        "complexity_bucket": entry.get("complexity_bucket"),
        "structural_complexity_bucket": entry.get("structural_complexity_bucket"),
        "complexity_score": entry.get("complexity_score"),
        "runtime_predicted_seconds": entry.get("runtime_predicted_seconds"),
        "runtime_prior_evidence": entry.get("runtime_prior_evidence"),
        "runtime_sort_seconds": entry.get("runtime_sort_seconds"),
        "runtime_sort_source": entry.get("runtime_sort_source"),
        "runtime_rank_in_pool": entry.get("runtime_rank_in_pool"),
        "runtime_pool_size": entry.get("runtime_pool_size"),
        "runtime_quantile_bucket_policy": entry.get("runtime_quantile_bucket_policy"),
        "scheduler_task_id": entry.get("scheduler_task_id"),
        "scheduler_lane": entry.get("scheduler_lane"),
        "memory_snapshot_attempt_count": entry.get("memory_snapshot_attempt_count"),
        "memory_snapshot_timestamp": entry.get("memory_snapshot_timestamp"),
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
    chi2 = float(row["chi2"])
    aic = float(row["AIC"])
    try:
        k_params = int(float(row.get("k_params")))
    except (TypeError, ValueError):
        k_params = max(0, int(round((aic - chi2) / 2.0)))
    return ValidationResult(
        validated=True,
        best_lag_id=str(lag_id),
        chi2=chi2,
        aic=aic,
        bic=float(row["BIC"]),
        k_params=k_params,
        k_parameter_names=[
            name for name in str(row.get("k_parameter_names") or "").split(";") if name
        ],
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
    llm_provider: str,
    llm_model: str,
    llm_base_url: str,
    llm_api_key_env: str,
    llm_fallback: str,
    llm_api_timeout: int,
    debug_dir: Path,
    loop_id: str,
    track: Optional[str] = None,
    scalar_config: Optional[str] = None,
    required_operator_substring: Optional[str] = None,
    required_operator_contains_curvature: bool = False,
) -> Dict[str, Any]:
    if proposal_mode == "llm":
        try:
            from .llm_agent import propose_entry_with_llm

            return propose_entry_with_llm(
                context,
                summary,
                rng,
                seed,
                provider=llm_provider,
                model=llm_model or None,
                base_url=llm_base_url or None,
                api_key_env=llm_api_key_env or "",
                api_timeout=llm_api_timeout,
                debug_dir=debug_dir,
                loop_id=loop_id,
                track=track,
                scalar_config=scalar_config,
                required_operator_substring=required_operator_substring,
                required_operator_contains_curvature=required_operator_contains_curvature,
            )
        except Exception:
            if llm_fallback in {"fail", "skip"}:
                raise
    return _generate_token_level_entry(
        context,
        summary,
        rng,
        seed,
        track=track,
        scalar_config=scalar_config,
        required_operator_substring=required_operator_substring,
        required_operator_contains_curvature=required_operator_contains_curvature,
    )


def _summary_with_diversity(summary: Dict[str, Any], diversity_strength: float) -> Dict[str, Any]:
    out = dict(summary or {})
    try:
        strength = float(diversity_strength)
    except (TypeError, ValueError):
        strength = 0.0
    if not math.isfinite(strength):
        strength = 0.0
    out["_proposal_diversity_strength"] = min(1.0, max(0.0, strength))
    return out


def _track_targets(batch_size: int, track_mode: str, eh_track_fraction: float, rng: random.Random) -> List[Dict[str, Any]]:
    if track_mode == "mixed":
        return [{"group": "open_search", "track": None, "scalar_config": None} for _ in range(batch_size)]
    if batch_size <= 1:
        return [{"group": "eh_anchored", "track": "eh_anchored", "scalar_config": None}]
    eh_fraction = min(1.0, max(0.0, float(eh_track_fraction)))
    eh_count = int(round(batch_size * eh_fraction))
    eh_count = min(batch_size - 1, max(1, eh_count))
    targets: List[Dict[str, Any]] = (
        [{"group": "eh_anchored", "track": "eh_anchored", "scalar_config": None} for _ in range(eh_count)]
        + [{"group": "non_eh", "track": "non_eh", "scalar_config": None} for _ in range(batch_size - eh_count)]
    )
    rng.shuffle(targets)
    return targets


def _positive_scalar_reward_weights(summary: Dict[str, Any]) -> List[float]:
    policy = summary.get("policy") if isinstance(summary.get("policy"), dict) else {}
    by_feature = policy.get("by_feature") if isinstance(policy.get("by_feature"), dict) else {}
    scalar_stats = by_feature.get("scalar_config") if isinstance(by_feature.get("scalar_config"), dict) else {}
    rewards: List[float] = []
    for family in NON_EH_SCALAR_FAMILIES:
        bucket = scalar_stats.get(family) if isinstance(scalar_stats.get(family), dict) else {}
        try:
            count = int(bucket.get("count") or 0)
            mean_reward = float(bucket.get("mean_reward"))
        except (TypeError, ValueError):
            count = 0
            mean_reward = 0.0
        rewards.append(mean_reward if count > 0 and math.isfinite(mean_reward) and mean_reward > 0.0 else 0.0)
    if sum(rewards) <= 0.0:
        return [1.0 for _ in NON_EH_SCALAR_FAMILIES]
    peak = max(rewards)
    return [math.exp(1.5 * (reward - peak)) if reward > 0.0 else 1e-3 for reward in rewards]


def _scalar_target_with_baseline(summary: Dict[str, Any], rng: random.Random, baseline_per_family: float) -> str:
    baseline_mass = min(1.0, max(0.0, baseline_per_family) * len(NON_EH_SCALAR_FAMILIES))
    if rng.random() < baseline_mass:
        return rng.choice(list(NON_EH_SCALAR_FAMILIES))
    return rng.choices(
        list(NON_EH_SCALAR_FAMILIES),
        weights=_positive_scalar_reward_weights(summary),
        k=1,
    )[0]


def _open_search_scalar_target(summary: Dict[str, Any], rng: random.Random) -> str:
    return _scalar_target_with_baseline(summary, rng, OPEN_SEARCH_SCALAR_BASELINE_PER_FAMILY)


def _non_eh_scalar_target(summary: Dict[str, Any], rng: random.Random) -> str:
    return _scalar_target_with_baseline(summary, rng, NON_EH_SCALAR_BASELINE_PER_FAMILY)


def _group_targets(batch_size: int, group_mode: str, eh_track_fraction: float, rng: random.Random) -> List[Dict[str, Any]]:
    if group_mode in {"sector_split", "triad"}:
        names = list(GROUP_SPECS)
        base = batch_size // len(names)
        remainder = batch_size % len(names)
        targets: List[Dict[str, Any]] = []
        for index, name in enumerate(names):
            count = base + (1 if index < remainder else 0)
            spec = GROUP_SPECS[name]
            targets.extend(
                {
                    "group": name,
                    "track": spec.get("track"),
                    "scalar_config": spec.get("scalar_config"),
                    "required_operator_substring": spec.get("required_operator_substring"),
                    "required_operator_contains_curvature": bool(spec.get("required_operator_contains_curvature")),
                }
                for _ in range(count)
            )
        rng.shuffle(targets)
        return targets
    if group_mode == "track_split":
        return _track_targets(batch_size, "split", eh_track_fraction, rng)
    if group_mode not in OPEN_ONLY_GROUP_MODES:
        raise ValueError(f"Unknown proposal group mode: {group_mode}")
    targets = [
        {"group": "open_search", "track": None, "scalar_config": None}
        for _ in range(batch_size)
    ]
    rng.shuffle(targets)
    return targets


def _entry_family_key(target_group: str, entry: Dict[str, Any]) -> str:
    return json.dumps(
        {
            "proposal_group": target_group,
            "theory_track": entry.get("theory_track") or theory_track_from_operators(entry.get("operators") or []),
            "scalar_config": entry.get("scalar_config"),
            "potential_types": entry.get("potential_types"),
            "operators": entry.get("operators"),
        },
        sort_keys=True,
        ensure_ascii=False,
    )


def _target_scalar_for_group(
    target_group: str,
    target_scalar: Optional[str],
    proposal_summary: Dict[str, Any],
    rng: random.Random,
) -> Optional[str]:
    if target_group == "non_eh" and target_scalar in {None, "mixed"}:
        return _non_eh_scalar_target(proposal_summary, rng)
    if target_group == "open_search" and target_scalar in {None, "mixed"}:
        return _open_search_scalar_target(proposal_summary, rng)
    return target_scalar


def _generate_entries_for_batch(
    *,
    context: Dict[str, Any],
    summary: Dict[str, Any],
    group_summaries: Dict[str, Dict[str, Any]],
    group_mode: str,
    eh_track_fraction: float,
    rng: random.Random,
    seed: int,
    desired_count: int,
    proposal_mode: str,
    llm_provider: str,
    llm_model: str,
    llm_base_url: str,
    llm_api_key_env: str,
    llm_fallback: str,
    llm_api_timeout: int,
    debug_dir: Path,
    loop_prefix: str,
    target_complexity_bucket: Optional[str] = None,
    pending_families: Optional[set[str]] = None,
    attempt_multiplier: int = 5,
    runtime_prior: Optional[Dict[str, Any]] = None,
    diversity_strength: float = 0.0,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str], set[str]]:
    targets = _group_targets(desired_count, group_mode, eh_track_fraction, rng)
    entries: List[Dict[str, Any]] = []
    entry_summaries: List[Dict[str, Any]] = []
    messages: List[str] = []
    seen_families: set[str] = set()
    blocked_families = pending_families or set()
    attempts = 0
    max_attempts = max(desired_count, desired_count * max(1, attempt_multiplier))
    while len(entries) < desired_count and attempts < max_attempts:
        attempts += 1
        if target_complexity_bucket:
            target = targets[(attempts - 1) % len(targets)]
        else:
            target = targets[len(entries)] if len(entries) < len(targets) else {"group": "open_search", "track": None, "scalar_config": None}
        target_group = str(target.get("group") or "open_search")
        target_track = target.get("track")
        target_scalar = target.get("scalar_config")
        target_required = target.get("required_operator_substring")
        target_required_curvature = bool(target.get("required_operator_contains_curvature"))
        # Proposal learning uses the shared current-loop memory. Group memory is
        # still recorded for diagnostics, but sectors should not become isolated
        # agents during async lane scheduling.
        proposal_summary = _summary_with_diversity(summary, diversity_strength)
        target_scalar = _target_scalar_for_group(target_group, target_scalar, proposal_summary, rng)
        loop_id = (
            f"{loop_prefix}_try_{attempts:03d}_item_{len(entries) + 1:02d}"
            if target_complexity_bucket
            else f"{loop_prefix}_item_{len(entries) + 1:02d}"
        )
        try:
            with _wall_timeout(BATCH_PROPOSAL_TIMEOUT_SECONDS, "Batch proposal generation"):
                entry = _proposal_entry(
                    context=context,
                    summary=proposal_summary,
                    rng=rng,
                    seed=seed + attempts * 37,
                    proposal_mode=proposal_mode,
                    llm_provider=llm_provider,
                    llm_model=llm_model,
                    llm_base_url=llm_base_url,
                    llm_api_key_env=llm_api_key_env,
                    llm_fallback=llm_fallback,
                    llm_api_timeout=llm_api_timeout,
                    debug_dir=debug_dir,
                    loop_id=loop_id,
                    track=target_track,
                    scalar_config=target_scalar,
                    required_operator_substring=target_required,
                    required_operator_contains_curvature=target_required_curvature,
                )
        except Exception as exc:
            if proposal_mode == "llm" and llm_fallback == "fail":
                raise
            message = f"{loop_id} proposal skipped after {type(exc).__name__}: {exc}"
            print(f"[BatchProposal] {message}", flush=True)
            messages.append(message)
            continue

        entry_track = entry.get("theory_track") or theory_track_from_operators(entry.get("operators") or [])
        entry["theory_track"] = entry_track
        entry["proposal_group"] = target_group
        _annotate_entry_complexity(entry, runtime_prior=runtime_prior)
        family = _entry_family_key(target_group, entry)
        if family in seen_families or family in blocked_families:
            continue
        seen_families.add(family)
        entries.append(entry)
        entry_summaries.append(proposal_summary)
    _assign_relative_runtime_buckets(entries)
    if target_complexity_bucket:
        filtered_pairs = [
            (entry, summary)
            for entry, summary in zip(entries, entry_summaries)
            if entry.get("complexity_bucket") == target_complexity_bucket
        ]
        entries = [entry for entry, _summary in filtered_pairs]
        entry_summaries = [summary for _entry, summary in filtered_pairs]
    if len(entries) < desired_count:
        messages.append(
            f"{loop_prefix}: generated {len(entries)}/{desired_count} entries "
            f"for target_complexity_bucket={target_complexity_bucket} after {attempts} attempts."
        )
    returned_families = {_entry_family_key(str(entry.get("proposal_group") or "open_search"), entry) for entry in entries}
    return entries, entry_summaries, messages, returned_families


def _append_jsonl(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")


def _read_jsonl_rows(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    lines = [
        (line_number, line)
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        if line.strip()
    ]
    for index, (line_number, line) in enumerate(lines):
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            if index == len(lines) - 1:
                # A killed writer can leave one incomplete final record.
                continue
            raise ValueError(f"Malformed JSONL record at {path}:{line_number}") from exc
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _attempt_validation_stage(attempt: Dict[str, Any]) -> str:
    stage = str(attempt.get("validation_stage") or "").strip().lower()
    if stage:
        return stage
    loop_id = str(attempt.get("loop_id") or "").lower()
    if "_refine_" in loop_id or "_refine" in loop_id:
        return "refine"
    if "_expanded_" in loop_id or "_expanded" in loop_id:
        return "expanded"
    return "initial"


def _task_sequence_number(value: Any) -> int:
    match = re.search(r"task_(\d+)", str(value or ""))
    return int(match.group(1)) if match else 0


def _async_slot_resume_state(
    *,
    proposal_dir: Path,
    memory_dir: Path,
    group_names: Iterable[str],
) -> Dict[str, Any]:
    attempts = _read_jsonl_rows(memory_dir / "attempt_history.jsonl")
    events = _read_jsonl_rows(proposal_dir / "scheduler_tasks.jsonl")
    recorded_by_group = {str(group): 0 for group in group_names}
    stage_counts = {"initial": 0, "expanded": 0, "refine": 0}
    task_sequence = 0

    for attempt in attempts:
        stage = _attempt_validation_stage(attempt)
        stage_counts[stage] = stage_counts.get(stage, 0) + 1
        task_sequence = max(
            task_sequence,
            _task_sequence_number(attempt.get("scheduler_task_id")),
            _task_sequence_number(attempt.get("loop_id")),
        )
        if stage == "initial":
            theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
            group = str(attempt.get("proposal_group") or theory.get("proposal_group") or "open_search")
            recorded_by_group[group] = recorded_by_group.get(group, 0) + 1

    historical_submitted_total = stage_counts["initial"]
    expanded_submitted_total = stage_counts["expanded"]
    refine_submitted_total = stage_counts["refine"]
    failed_total = 0
    for event in events:
        task_sequence = max(task_sequence, _task_sequence_number(event.get("task_id")))
        historical_submitted_total = max(
            historical_submitted_total,
            int(event.get("submitted_total") or 0),
        )
        expanded_submitted_total = max(
            expanded_submitted_total,
            int(event.get("expanded_submitted_total") or 0),
        )
        refine_submitted_total = max(
            refine_submitted_total,
            int(event.get("refine_submitted_total") or 0),
        )
        failed_total = max(failed_total, int(event.get("failed_total") or 0))

    for path in proposal_dir.glob("task_*.json"):
        task_sequence = max(task_sequence, _task_sequence_number(path.name))

    return {
        # Only completed initial validations count toward the resumed target.
        "submitted_total": stage_counts["initial"],
        "recorded_total": stage_counts["initial"],
        "historical_submitted_total": historical_submitted_total,
        "expanded_submitted_total": expanded_submitted_total,
        "expanded_recorded_total": stage_counts["expanded"],
        "refine_submitted_total": refine_submitted_total,
        "refine_recorded_total": stage_counts["refine"],
        "failed_total": failed_total,
        "task_sequence": task_sequence,
        "submitted_by_group": dict(recorded_by_group),
        "recorded_by_group": dict(recorded_by_group),
        "attempt_count": len(attempts),
    }


def _validate_async_slot_resume_configuration(
    *,
    proposal_dir: Path,
    target_attempts: int,
    llm_provider: str,
    llm_model: str,
    llm_base_url: str,
    llm_api_key_env: str,
) -> None:
    events = _read_jsonl_rows(proposal_dir / "scheduler_tasks.jsonl")
    starts = [
        event
        for event in events
        if event.get("event") in {"scheduler_start", "scheduler_resume"}
    ]
    if not starts:
        return
    original = starts[0]
    expected = {
        "target_attempts": int(target_attempts),
        "llm_provider": str(llm_provider or ""),
        "llm_model": str(llm_model or ""),
        "llm_base_url": str(llm_base_url or "").rstrip("/"),
        "llm_api_key_env": str(llm_api_key_env or ""),
    }
    mismatches: List[str] = []
    for field, current in expected.items():
        previous = original.get(field)
        if previous is None:
            continue
        if field == "target_attempts":
            try:
                previous = int(previous)
            except (TypeError, ValueError):
                pass
        else:
            previous = str(previous or "")
            if field == "llm_base_url":
                previous = previous.rstrip("/")
        if previous != current:
            mismatches.append(f"{field}: existing={previous!r}, requested={current!r}")
    if mismatches:
        raise ValueError(
            "Resume configuration does not match the original scheduler: "
            + "; ".join(mismatches)
        )


def _log_scheduler_event(path: Path, payload: Dict[str, Any], *, run_name: str) -> None:
    _append_jsonl(path, payload)
    trace_event(
        f"ai_theory_lab.{payload.get('scheduler', 'scheduler')}.{payload.get('event', 'event')}",
        payload,
        run_name=run_name,
    )


def _estimated_bucket_seconds(entries: List[Dict[str, Any]]) -> float:
    if not entries:
        return 0.0
    base = {"simple": 90.0, "medium": 240.0, "complex": 720.0, "very_complex": 1080.0}
    bucket = str(entries[0].get("complexity_bucket") or "medium")
    score = sum(float(entry.get("complexity_score") or 0.0) for entry in entries)
    return round(base.get(bucket, 240.0) + 12.0 * score, 1)


def _run_validation_bucket_task(
    *,
    run_name: str,
    proposal_dir: Path,
    agent_dir: Path,
    validation_wave: str,
    complexity_bucket: str,
    entries: List[Dict[str, Any]],
    entry_summaries: List[Dict[str, Any]],
    initial_parameter_samples: int,
    timeout_setup: int,
    n_workers: int,
    rng_seed: int,
    group_mode: str,
    track_mode: str,
    complexity_split: bool,
) -> Dict[str, Any]:
    started_at = time.time()
    rng = random.Random(rng_seed)
    for entry in entries:
        entry["validation_wave"] = validation_wave
    batch_lagrangians_path = agent_dir / "agent_lagrangians.pkl"
    lag_ids = _write_batch_lagrangians(entries, batch_lagrangians_path)
    samples_by_lag_id: Dict[str, List[Dict[str, Any]]] = {}
    proposal_paths: Dict[int, Path] = {}
    parameter_samples_path = agent_dir / "agent_parameter_samples_by_lag_id.json"
    for entry_index, entry in enumerate(entries):
        lag_id = lag_ids[entry_index]
        samples = _parameter_samples(entry, rng, initial_parameter_samples, entry_summaries[entry_index])
        samples_by_lag_id[lag_id] = samples
        proposal_label = f"{validation_wave}_lag_{lag_id}"
        proposal = _proposal_for(
            entry,
            int(entry.get("batch_wave") or 0),
            samples,
            proposal_label,
            summary=entry_summaries[entry_index],
        )
        proposal["batch_wave"] = entry.get("batch_wave")
        proposal["batch_lag_id"] = lag_id
        proposal["validation_wave"] = validation_wave
        proposal["theory_track"] = entry.get("theory_track")
        proposal["proposal_group"] = entry.get("proposal_group")
        proposal["complexity_bucket"] = entry.get("complexity_bucket")
        proposal["structural_complexity_bucket"] = entry.get("structural_complexity_bucket")
        proposal["complexity_score"] = entry.get("complexity_score")
        proposal["runtime_predicted_seconds"] = entry.get("runtime_predicted_seconds")
        proposal["runtime_prior_evidence"] = entry.get("runtime_prior_evidence")
        proposal["runtime_sort_seconds"] = entry.get("runtime_sort_seconds")
        proposal["runtime_sort_source"] = entry.get("runtime_sort_source")
        proposal["runtime_rank_in_pool"] = entry.get("runtime_rank_in_pool")
        proposal["runtime_pool_size"] = entry.get("runtime_pool_size")
        proposal["runtime_quantile_bucket_policy"] = entry.get("runtime_quantile_bucket_policy")
        for key in (
            "scheduler_task_id",
            "scheduler_lane",
            "memory_snapshot_attempt_count",
            "memory_snapshot_timestamp",
        ):
            if entry.get(key) is not None:
                proposal[key] = entry.get(key)
        proposal_name = f"{validation_wave}_lag_{lag_id}.json"
        proposal_path = proposal_dir / proposal_name
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
    result_items = []
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
                    "message": (
                        f"{stage_failed} failed while validating batch task {validation_wave} "
                        f"complexity_bucket={complexity_bucket}."
                    ),
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
        loop_id = f"{validation_wave}_lag_{lag_id}"
        result_items.append(
            {
                "entry": entry,
                "loop_id": loop_id,
                "result": result,
                "family_key": _entry_family_key(str(entry.get("proposal_group") or "open_search"), entry),
            }
        )

    elapsed_sec = round(time.time() - started_at, 3)
    return {
        "run_name": run_name,
        "validation_wave": validation_wave,
        "complexity_split": complexity_split,
        "complexity_bucket": complexity_bucket,
        "batch_size": len(entries),
        "group_mode": group_mode,
        "group_targets": [entry.get("proposal_group") for entry in entries],
        "scalar_targets": [entry.get("proposal_scalar_constraint") or entry.get("scalar_config") for entry in entries],
        "track_mode": track_mode,
        "track_targets": [entry.get("theory_track") for entry in entries],
        "complexity_scores": [entry.get("complexity_score") for entry in entries],
        "agent_run_dir": str(agent_dir),
        "worker_count": n_workers,
        "estimated_elapsed_sec": _estimated_bucket_seconds(entries),
        "elapsed_sec": elapsed_sec,
        "result_items": result_items,
    }


def _record_validation_task_result(
    *,
    task_result: Dict[str, Any],
    memory_dir: Path,
    group_memory_dirs: Dict[str, Path],
    proposal_dir: Path,
    traces: List[Dict[str, Any]],
    update_runtime_prior: bool = True,
) -> List[Dict[str, Any]]:
    if update_runtime_prior:
        _update_runtime_prior_from_task(memory_dir, task_result)
    wave_records = []
    for item in task_result.get("result_items") or []:
        entry = item["entry"]
        scheduler_task_id = entry.get("scheduler_task_id")
        structure_trial_base = (
            entry.get("expanded_from_task_id")
            or entry.get("refine_from_task_id")
            or scheduler_task_id
            or item["loop_id"]
        )
        if entry.get("expanded_from_task_id"):
            structure_trial_base = entry.get("expanded_from_task_id")
        lag_id = item["result"].best_lag_id or "unknown"
        structure_trial_id = f"{structure_trial_base}|lag_{lag_id}"
        attempt_context = {
            "validation_stage": entry.get("validation_stage") or "initial",
            "structure_trial_id": structure_trial_id,
            "scheduler_task_id": scheduler_task_id,
            "expanded_from_task_id": entry.get("expanded_from_task_id"),
            "refine_from_task_id": entry.get("refine_from_task_id"),
        }
        memory_info = record_attempt(
            item["result"],
            memory_dir,
            loop_id=item["loop_id"],
            attempt_context=attempt_context,
        )
        entry_group = str(entry.get("proposal_group") or "open_search")
        group_dir = group_memory_dirs.get(entry_group)
        if group_dir is not None:
            record_attempt(
                item["result"],
                group_dir,
                loop_id=item["loop_id"],
                attempt_context=attempt_context,
            )
        wave_records.append(memory_info["attempt"])
    trace = {
        key: value
        for key, value in task_result.items()
        if key not in {"result_items"}
    }
    trace["records"] = wave_records
    traces.append(trace)
    with (proposal_dir / "wave_trace.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(trace, ensure_ascii=False, default=str) + "\n")
    return wave_records


def _auto_lane_batch_sizes(batch_size: int, requested: Dict[str, int]) -> Dict[str, int]:
    base = max(1, batch_size // len(ASYNC_LANES))
    remainder = max(0, batch_size - base * len(ASYNC_LANES))
    sizes: Dict[str, int] = {}
    for index, lane in enumerate(ASYNC_LANES):
        default = base + (1 if index < remainder else 0)
        sizes[lane] = max(1, int(requested.get(lane) or default))
    return sizes


def _resolve_async_lane_min_attempts(
    *,
    target_attempts: int,
    target_policy: str,
    lane_min_fraction: float,
    requested: Dict[str, int],
) -> Dict[str, int]:
    if target_policy not in ASYNC_TARGET_POLICIES:
        raise ValueError(f"Unknown async target policy: {target_policy}")
    if target_policy == "global_recorded_total":
        return {lane: 0 for lane in ASYNC_LANES}

    fraction = min(1.0, max(0.0, float(lane_min_fraction)))
    fraction_floor = max(0, int(max(0, target_attempts) * fraction))
    return {
        lane: max(fraction_floor, max(0, int(requested.get(lane) or 0)))
        for lane in ASYNC_LANES
    }


def _run_async_lane_scheduler(
    *,
    name: str,
    proposal_dir: Path,
    memory_dir: Path,
    group_memory_dirs: Dict[str, Path],
    context: Dict[str, Any],
    traces: List[Dict[str, Any]],
    target_attempts: int,
    batch_size: int,
    seed: int,
    initial_parameter_samples: int,
    timeout_setup: int,
    proposal_mode: str,
    llm_provider: str,
    llm_model: str,
    llm_base_url: str,
    llm_api_key_env: str,
    llm_fallback: str,
    llm_api_timeout: int,
    group_mode: str,
    track_mode: str,
    eh_track_fraction: float,
    lane_batch_sizes: Dict[str, int],
    lane_workers: Dict[str, int],
    async_target_policy: str,
    async_lane_min_fraction: float,
    lane_min_attempts: Dict[str, int],
    total_workers: int,
    diversity_strength: float = 0.0,
) -> List[str]:
    messages = [
        f"Starting async_lanes scheduler target_attempts={target_attempts}, "
        f"diversity_strength={diversity_strength}."
    ]
    scheduler_log = proposal_dir / "scheduler_tasks.jsonl"
    lane_batch_sizes = _auto_lane_batch_sizes(batch_size, lane_batch_sizes)
    target_attempts = max(0, int(target_attempts))
    lane_min_attempts = _resolve_async_lane_min_attempts(
        target_attempts=target_attempts,
        target_policy=async_target_policy,
        lane_min_fraction=async_lane_min_fraction,
        requested=lane_min_attempts,
    )
    lane_workers = {
        lane: max(1, int(lane_workers.get(lane) or 1))
        for lane in ASYNC_LANES
    }
    max_submit_overshoot = max(sum(lane_batch_sizes.values()), max(lane_batch_sizes.values()))
    max_submitted_total = max(target_attempts, sum(lane_min_attempts.values())) + max_submit_overshoot
    max_queue_per_lane = max(batch_size * 4, max(lane_batch_sizes.values()) * 4)
    worker_sum = sum(lane_workers.values())
    if worker_sum > max(1, total_workers):
        messages.append(
            f"Warning: async lane worker budget sums to {worker_sum}, "
            f"above total n_workers={total_workers}; cluster CPU oversubscription is possible."
        )
    _append_jsonl(
        scheduler_log,
        {
            "event": "scheduler_start",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "target_attempts": target_attempts,
            "target_policy": async_target_policy,
            "async_lane_min_fraction": async_lane_min_fraction,
            "lane_min_attempts": lane_min_attempts,
            "lane_batch_sizes": lane_batch_sizes,
            "lane_workers": lane_workers,
            "total_workers": total_workers,
            "max_submitted_total": max_submitted_total,
            "max_submit_overshoot": max_submit_overshoot,
            "max_queue_per_lane": max_queue_per_lane,
            "diversity_strength": diversity_strength,
            "llm_provider": llm_provider,
            "llm_model": llm_model,
            "llm_base_url": llm_base_url,
            "llm_api_key_env": llm_api_key_env,
        },
        run_name=name,
    )

    submitted_by_lane = {lane: 0 for lane in ASYNC_LANES}
    recorded_by_lane = {lane: 0 for lane in ASYNC_LANES}
    failed_by_lane = {lane: 0 for lane in ASYNC_LANES}
    exhausted_lanes: set[str] = set()
    reserved_families: set[str] = set()
    lane_queues: Dict[str, List[Tuple[Dict[str, Any], Dict[str, Any], str]]] = {
        lane: [] for lane in ASYNC_LANES
    }
    lane_empty_rounds = {lane: 0 for lane in ASYNC_LANES}
    futures: Dict[Future, Dict[str, Any]] = {}
    task_sequence = 0
    pool_sequence = 0

    def active_lane_names() -> set[str]:
        return {str(info["lane"]) for info in futures.values()}

    def queued_counts() -> Dict[str, int]:
        return {lane: len(lane_queues[lane]) for lane in ASYNC_LANES}

    def public_task_info(task_info: Dict[str, Any]) -> Dict[str, Any]:
        return {key: value for key, value in task_info.items() if not str(key).startswith("_")}

    def submitted_total() -> int:
        return sum(submitted_by_lane.values()) - sum(failed_by_lane.values())

    def recorded_total() -> int:
        return sum(recorded_by_lane.values())

    def lane_floor_shortfalls() -> Dict[str, int]:
        return {
            lane: max(0, int(lane_min_attempts.get(lane) or 0) - recorded_by_lane[lane])
            for lane in ASYNC_LANES
        }

    def lane_floors_met() -> bool:
        shortfalls = lane_floor_shortfalls()
        return all(shortfalls[lane] <= 0 or lane in exhausted_lanes for lane in ASYNC_LANES)

    def stop_ready() -> bool:
        return recorded_total() >= target_attempts and lane_floors_met()

    def submission_slots_remaining(lane: Optional[str] = None) -> int:
        if stop_ready():
            return 0
        if lane is not None:
            lane_shortfall = max(0, int(lane_min_attempts.get(lane) or 0) - recorded_by_lane[lane])
            if lane_shortfall > 0:
                return lane_shortfall
        if recorded_total() >= target_attempts:
            return 0
        return max(0, max_submitted_total - submitted_total())

    def record_slow_running_signals() -> None:
        now = time.monotonic()
        for task_info in futures.values():
            if str(task_info.get("validation_stage") or "initial") != "initial":
                continue
            submitted_at = float(task_info.get("_submitted_monotonic") or now)
            elapsed = now - submitted_at
            estimated = float(task_info.get("estimated_elapsed_sec") or 0.0)
            threshold = max(ASYNC_SLOW_SIGNAL_INTERVAL_SECONDS, estimated * 1.5)
            last_signal = float(task_info.get("_last_slow_signal_elapsed_sec") or 0.0)
            if elapsed < threshold or elapsed - last_signal < ASYNC_SLOW_SIGNAL_INTERVAL_SECONDS:
                continue
            entries = task_info.get("_entries")
            if not isinstance(entries, list) or not entries:
                continue
            _update_runtime_prior_from_entries(
                memory_dir=memory_dir,
                entries=[entry for entry in entries if isinstance(entry, dict)],
                elapsed_sec=elapsed,
                signal="running_lower_bound",
                weight=0.25,
            )
            task_info["_last_slow_signal_elapsed_sec"] = elapsed
            _append_jsonl(
                scheduler_log,
                {
                    "event": "runtime_slow_signal",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    **public_task_info(task_info),
                    "running_elapsed_sec": round(elapsed, 3),
                    "slow_signal_weight": 0.25,
                    "submitted_by_lane": dict(submitted_by_lane),
                    "recorded_by_lane": dict(recorded_by_lane),
                    "failed_by_lane": dict(failed_by_lane),
                    "queued_counts": queued_counts(),
                    "lane_floor_shortfalls": lane_floor_shortfalls(),
                    "submitted_total": submitted_total(),
                    "recorded_total": recorded_total(),
                    "target_attempts": target_attempts,
                },
            )

    def generate_pool(reason_lane: str) -> bool:
        nonlocal pool_sequence
        if stop_ready():
            return False
        pool_sequence += 1
        summary = _load_summary(memory_dir)
        group_summaries = {group: _load_summary(path) for group, path in group_memory_dirs.items()}
        runtime_prior = _load_runtime_prior(memory_dir)
        snapshot_count = int(summary.get("total_attempts") or 0)
        snapshot_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        pool_id = f"pool_{pool_sequence:06d}"
        entries, entry_summaries, proposal_messages, _families = _generate_entries_for_batch(
            context=context,
            summary=summary,
            group_summaries=group_summaries,
            group_mode=group_mode,
            eh_track_fraction=eh_track_fraction,
            rng=random.Random(seed + pool_sequence * 100003),
            seed=seed + pool_sequence * 1009,
            desired_count=batch_size,
            proposal_mode=proposal_mode,
            llm_provider=llm_provider,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
            llm_api_key_env=llm_api_key_env,
            llm_fallback=llm_fallback,
            llm_api_timeout=llm_api_timeout,
            debug_dir=proposal_dir / "llm_proposal_debug",
            loop_prefix=pool_id,
            pending_families=reserved_families,
            attempt_multiplier=5,
            runtime_prior=runtime_prior,
            diversity_strength=diversity_strength,
        )
        messages.extend(proposal_messages)
        bucket_counts = {lane: 0 for lane in ASYNC_LANES}
        skipped_exhausted_counts = {lane: 0 for lane in ASYNC_LANES}
        skipped_queue_full_counts = {lane: 0 for lane in ASYNC_LANES}
        for entry, entry_summary in zip(entries, entry_summaries):
            lane = str(entry.get("complexity_bucket") or "medium")
            if lane not in lane_queues:
                lane = "medium"
                entry["complexity_bucket"] = lane
            if lane in exhausted_lanes:
                skipped_exhausted_counts[lane] += 1
                continue
            if len(lane_queues[lane]) >= max_queue_per_lane:
                skipped_queue_full_counts[lane] += 1
                continue
            family = _entry_family_key(str(entry.get("proposal_group") or "open_search"), entry)
            if family in reserved_families:
                continue
            entry["memory_snapshot_attempt_count"] = snapshot_count
            entry["memory_snapshot_timestamp"] = snapshot_timestamp
            lane_queues[lane].append((entry, entry_summary, family))
            reserved_families.add(family)
            bucket_counts[lane] += 1
        _append_jsonl(
            scheduler_log,
            {
                "event": "proposal_pool_generated",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "pool_id": pool_id,
                "reason_lane": reason_lane,
                "generated": len(entries),
                "bucket_counts": bucket_counts,
                "skipped_exhausted_counts": skipped_exhausted_counts,
                "skipped_queue_full_counts": skipped_queue_full_counts,
                "queued_counts": queued_counts(),
                "lane_floor_shortfalls": lane_floor_shortfalls(),
                "submitted_total": submitted_total(),
                "recorded_total": recorded_total(),
                "target_attempts": target_attempts,
                "memory_snapshot_attempt_count": snapshot_count,
            },
        )
        return bool(entries)

    def launch_ready_lanes(executor: ThreadPoolExecutor) -> int:
        nonlocal task_sequence
        launched = 0
        if stop_ready():
            return launched
        for lane in ASYNC_LANES:
            if lane in exhausted_lanes or lane in active_lane_names():
                continue
            remaining = submission_slots_remaining(lane)
            if remaining <= 0:
                continue
            desired = min(lane_batch_sizes[lane], remaining)
            refill_attempts = 0
            while len(lane_queues[lane]) < desired and refill_attempts < 2:
                refill_attempts += 1
                if not generate_pool(lane):
                    break
            if not lane_queues[lane]:
                lane_empty_rounds[lane] += 1
                if lane_empty_rounds[lane] >= 3:
                    exhausted_lanes.add(lane)
                    event = "lane_exhausted"
                else:
                    event = "lane_waiting_for_entries"
                _append_jsonl(
                    scheduler_log,
                    {
                        "event": event,
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                        "lane": lane,
                        "reason": "no_entries_generated",
                        "global_submission_slots_remaining": remaining,
                        "empty_rounds": lane_empty_rounds[lane],
                        "queued_counts": queued_counts(),
                        "lane_floor_shortfalls": lane_floor_shortfalls(),
                        "submitted_total": submitted_total(),
                        "recorded_total": recorded_total(),
                        "target_attempts": target_attempts,
                    },
                )
                continue
            lane_empty_rounds[lane] = 0
            selected = [lane_queues[lane].pop(0) for _ in range(min(desired, len(lane_queues[lane])))]
            entries = [item[0] for item in selected]
            # Queued proposals may have been generated before recent lane
            # results updated memory. Structure can stay queued, but parameter
            # sampling must use the freshest current-loop evidence available at
            # validation launch time.
            launch_summary = _load_summary(memory_dir)
            entry_summaries = [launch_summary for _item in selected]
            families = {item[2] for item in selected}
            snapshot_count = min(
                int(entry.get("memory_snapshot_attempt_count") or 0)
                for entry in entries
            )
            snapshot_timestamp = min(
                str(entry.get("memory_snapshot_timestamp") or "")
                for entry in entries
            )
            task_sequence += 1
            task_id = f"task_{task_sequence:06d}"
            validation_wave = f"{task_id}_{lane}"
            for entry in entries:
                entry["scheduler_task_id"] = task_id
                entry["scheduler_lane"] = lane
                entry.setdefault("memory_snapshot_attempt_count", snapshot_count)
                entry.setdefault("memory_snapshot_timestamp", snapshot_timestamp)
                entry["batch_wave"] = task_sequence
            agent_dir = _async_agent_run_dir(name, task_id, lane)
            submitted_by_lane[lane] += len(entries)
            task_info = {
                "task_id": task_id,
                "lane": lane,
                "validation_wave": validation_wave,
                "batch_size": len(entries),
                "worker_count": lane_workers[lane],
                "agent_run_dir": str(agent_dir),
                "families": sorted(families),
                "memory_snapshot_attempt_count": snapshot_count,
                "memory_snapshot_timestamp": snapshot_timestamp,
                "parameter_memory_attempt_count": int(launch_summary.get("total_attempts") or 0),
                "estimated_elapsed_sec": _estimated_bucket_seconds(entries),
                "_entries": entries,
                "_submitted_monotonic": time.monotonic(),
                "_last_slow_signal_elapsed_sec": 0.0,
            }
            _append_jsonl(
                scheduler_log,
                {
                    "event": "submitted",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    **public_task_info(task_info),
                    "submitted_by_lane": dict(submitted_by_lane),
                    "recorded_by_lane": dict(recorded_by_lane),
                    "failed_by_lane": dict(failed_by_lane),
                    "queued_counts": queued_counts(),
                    "lane_floor_shortfalls": lane_floor_shortfalls(),
                    "submitted_total": submitted_total(),
                    "recorded_total": recorded_total(),
                    "target_attempts": target_attempts,
                    "max_submitted_total": max_submitted_total,
                },
            )
            future = executor.submit(
                _run_validation_bucket_task,
                run_name=name,
                proposal_dir=proposal_dir,
                agent_dir=agent_dir,
                validation_wave=validation_wave,
                complexity_bucket=lane,
                entries=entries,
                entry_summaries=entry_summaries,
                initial_parameter_samples=initial_parameter_samples,
                timeout_setup=timeout_setup,
                n_workers=lane_workers[lane],
                rng_seed=seed + task_sequence * 65537,
                group_mode=group_mode,
                track_mode=track_mode,
                complexity_split=True,
            )
            futures[future] = task_info
            launched += 1
        return launched

    with ThreadPoolExecutor(max_workers=len(ASYNC_LANES)) as executor:
        while True:
            if not stop_ready():
                launch_ready_lanes(executor)
            if not futures:
                if stop_ready():
                    break
                queued_work = any(lane_queues[lane] and lane not in exhausted_lanes for lane in ASYNC_LANES)
                unfinished_lanes = any(lane not in exhausted_lanes for lane in ASYNC_LANES)
                if queued_work or (unfinished_lanes and any(submission_slots_remaining(lane) > 0 for lane in ASYNC_LANES)):
                    continue
                break
            record_slow_running_signals()
            done, _pending = wait(
                futures.keys(),
                timeout=ASYNC_WAIT_POLL_SECONDS,
                return_when=FIRST_COMPLETED,
            )
            if not done:
                record_slow_running_signals()
                continue
            for future in done:
                task_info = futures.pop(future)
                lane = str(task_info["lane"])
                try:
                    task_result = future.result()
                    wave_records = _record_validation_task_result(
                        task_result=task_result,
                        memory_dir=memory_dir,
                        group_memory_dirs=group_memory_dirs,
                        proposal_dir=proposal_dir,
                        traces=traces,
                    )
                    recorded_by_lane[lane] += len(wave_records)
                    best = min((r.get("chi2") for r in wave_records if r.get("chi2") is not None), default=None)
                    message = (
                        f"Async lane {lane} {task_info['task_id']} complete; "
                        f"batch_size={len(wave_records)}; best_chi2={best}."
                    )
                    messages.append(message)
                    _append_jsonl(
                        scheduler_log,
                        {
                            "event": "recorded",
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                            **public_task_info(task_info),
                            "elapsed_sec": task_result.get("elapsed_sec"),
                            "record_count": len(wave_records),
                            "best_chi2": best,
                            "submitted_by_lane": dict(submitted_by_lane),
                            "recorded_by_lane": dict(recorded_by_lane),
                            "failed_by_lane": dict(failed_by_lane),
                            "queued_counts": queued_counts(),
                            "lane_floor_shortfalls": lane_floor_shortfalls(),
                            "submitted_total": submitted_total(),
                            "recorded_total": recorded_total(),
                            "target_attempts": target_attempts,
                        },
                    )
                except Exception as exc:
                    failed_by_lane[lane] += int(task_info.get("batch_size") or 0)
                    messages.append(
                        f"Async lane {lane} {task_info['task_id']} failed: {type(exc).__name__}: {exc}"
                    )
                    _append_jsonl(
                        scheduler_log,
                        {
                            "event": "failed",
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                            **public_task_info(task_info),
                            "error": f"{type(exc).__name__}: {exc}",
                            "submitted_by_lane": dict(submitted_by_lane),
                            "recorded_by_lane": dict(recorded_by_lane),
                            "failed_by_lane": dict(failed_by_lane),
                            "queued_counts": queued_counts(),
                            "lane_floor_shortfalls": lane_floor_shortfalls(),
                            "submitted_total": submitted_total(),
                            "recorded_total": recorded_total(),
                            "target_attempts": target_attempts,
                        },
                    )
                finally:
                    reserved_families.difference_update(task_info.get("families") or [])
        _append_jsonl(
            scheduler_log,
            {
                "event": "scheduler_complete",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "target_attempts": target_attempts,
                "target_policy": async_target_policy,
                "async_lane_min_fraction": async_lane_min_fraction,
                "lane_min_attempts": lane_min_attempts,
                "submitted_by_lane": dict(submitted_by_lane),
                "recorded_by_lane": dict(recorded_by_lane),
                "failed_by_lane": dict(failed_by_lane),
                "queued_counts": queued_counts(),
                "lane_floor_shortfalls": lane_floor_shortfalls(),
                "submitted_total": submitted_total(),
                "recorded_total": recorded_total(),
                "exhausted_lanes": sorted(exhausted_lanes),
            },
        )
    return messages


def _target_for_slot_group(
    *,
    group_mode: str,
    eh_track_fraction: float,
    submitted_by_group: Dict[str, int],
    rng: random.Random,
) -> Dict[str, Any]:
    if group_mode in {"sector_split", "triad"}:
        names = list(GROUP_SPECS)
        min_count = min(submitted_by_group.get(name, 0) for name in names)
        candidates = [name for name in names if submitted_by_group.get(name, 0) == min_count]
        name = rng.choice(candidates)
        spec = GROUP_SPECS[name]
        return {
            "group": name,
            "track": spec.get("track"),
            "scalar_config": spec.get("scalar_config"),
            "required_operator_substring": spec.get("required_operator_substring"),
            "required_operator_contains_curvature": bool(spec.get("required_operator_contains_curvature")),
        }
    if group_mode == "track_split":
        eh_fraction = min(1.0, max(0.0, float(eh_track_fraction)))
        total = sum(submitted_by_group.values())
        eh_target = total * eh_fraction
        eh_count = submitted_by_group.get("eh_anchored", 0)
        name = "eh_anchored" if eh_count <= eh_target else "non_eh"
        return {"group": name, "track": name, "scalar_config": None}
    if group_mode in OPEN_ONLY_GROUP_MODES:
        return {"group": "open_search", "track": None, "scalar_config": None}
    raise ValueError(f"Unknown proposal group mode: {group_mode}")


def _generate_slot_entry(
    *,
    context: Dict[str, Any],
    memory_dir: Path,
    group_memory_dirs: Dict[str, Path],
    group_mode: str,
    eh_track_fraction: float,
    submitted_by_group: Dict[str, int],
    proposal_dir: Path,
    proposal_mode: str,
    llm_provider: str,
    llm_model: str,
    llm_base_url: str,
    llm_api_key_env: str,
    llm_fallback: str,
    llm_api_timeout: int,
    seed: int,
    task_id: str,
    reserved_families: set[str],
    diversity_strength: float = 0.0,
    max_attempts: int = 20,
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], Optional[str], List[str]]:
    raw_summary = _load_summary(memory_dir)
    summary = _summary_with_diversity(raw_summary, diversity_strength)
    # Group summaries are kept for diagnostics/report compatibility. Proposal
    # learning intentionally uses the shared memory summary in this mode.
    _group_summaries = {group: _load_summary(path) for group, path in group_memory_dirs.items()}
    runtime_prior = _load_runtime_prior(memory_dir)
    snapshot_count = int(summary.get("total_attempts") or 0)
    snapshot_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    messages: List[str] = []
    rng = random.Random(seed)
    for attempt in range(1, max_attempts + 1):
        target = _target_for_slot_group(
            group_mode=group_mode,
            eh_track_fraction=eh_track_fraction,
            submitted_by_group=submitted_by_group,
            rng=rng,
        )
        target_group = str(target.get("group") or "open_search")
        target_track = target.get("track")
        target_scalar = _target_scalar_for_group(target_group, target.get("scalar_config"), summary, rng)
        loop_id = f"{task_id}_try_{attempt:03d}"
        try:
            with _wall_timeout(BATCH_PROPOSAL_TIMEOUT_SECONDS, "Async slot proposal generation"):
                entry = _proposal_entry(
                    context=context,
                    summary=summary,
                    rng=rng,
                    seed=seed + attempt * 37,
                    proposal_mode=proposal_mode,
                    llm_provider=llm_provider,
                    llm_model=llm_model,
                    llm_base_url=llm_base_url,
                    llm_api_key_env=llm_api_key_env,
                    llm_fallback=llm_fallback,
                    llm_api_timeout=llm_api_timeout,
                    debug_dir=proposal_dir / "llm_proposal_debug",
                    loop_id=loop_id,
                    track=target_track,
                    scalar_config=target_scalar,
                    required_operator_substring=target.get("required_operator_substring"),
                    required_operator_contains_curvature=bool(target.get("required_operator_contains_curvature")),
                )
        except Exception as exc:
            if proposal_mode == "llm" and llm_fallback == "fail":
                raise
            message = f"{loop_id} proposal skipped after {type(exc).__name__}: {exc}"
            print(f"[AsyncSlotProposal] {message}", flush=True)
            messages.append(message)
            continue

        entry_track = entry.get("theory_track") or theory_track_from_operators(entry.get("operators") or [])
        entry["theory_track"] = entry_track
        entry["proposal_group"] = target_group
        _annotate_entry_complexity(entry, runtime_prior=runtime_prior)
        family = _entry_family_key(target_group, entry)
        if family in reserved_families:
            continue
        entry["memory_snapshot_attempt_count"] = snapshot_count
        entry["memory_snapshot_timestamp"] = snapshot_timestamp
        return entry, summary, family, messages
    messages.append(f"{task_id}: generated no unique proposal after {max_attempts} attempts.")
    return None, None, None, messages


def _run_async_slot_scheduler(
    *,
    name: str,
    proposal_dir: Path,
    memory_dir: Path,
    group_memory_dirs: Dict[str, Path],
    context: Dict[str, Any],
    traces: List[Dict[str, Any]],
    target_attempts: int,
    seed: int,
    initial_parameter_samples: int,
    expanded_parameter_samples: int,
    expanded_chi2_threshold: float,
    refine_parameter_samples: int,
    refine_chi2_threshold: float,
    timeout_setup: int,
    proposal_mode: str,
    llm_provider: str,
    llm_model: str,
    llm_base_url: str,
    llm_api_key_env: str,
    llm_fallback: str,
    llm_api_timeout: int,
    group_mode: str,
    track_mode: str,
    eh_track_fraction: float,
    slot_count: int,
    slot_workers: int,
    total_workers: int,
    diversity_strength: float = 0.0,
    resume: bool = False,
) -> List[str]:
    scheduler_log = proposal_dir / "scheduler_tasks.jsonl"
    target_attempts = max(0, int(target_attempts))
    slot_count = max(1, int(slot_count or total_workers or 1))
    slot_workers = max(1, int(slot_workers or 1))
    messages = [
        f"Starting async_slots scheduler target_attempts={target_attempts}, "
        f"slot_count={slot_count}, slot_workers={slot_workers}, "
        f"initial_samples={initial_parameter_samples}, "
        f"expanded_samples={expanded_parameter_samples}, "
        f"expand_if_chi2_below={expanded_chi2_threshold}, "
        f"refine_samples={refine_parameter_samples}, "
        f"refine_if_expanded_chi2_below={refine_chi2_threshold}, "
        f"diversity_strength={diversity_strength}."
    ]
    worker_sum = slot_count * slot_workers
    if worker_sum > max(1, total_workers):
        messages.append(
            f"Warning: async slot worker budget sums to {worker_sum}, "
            f"above total n_workers={total_workers}; cluster CPU oversubscription is possible."
        )

    resume_state = (
        _async_slot_resume_state(
            proposal_dir=proposal_dir,
            memory_dir=memory_dir,
            group_names=group_memory_dirs,
        )
        if resume
        else {}
    )
    if resume:
        _validate_async_slot_resume_configuration(
            proposal_dir=proposal_dir,
            target_attempts=target_attempts,
            llm_provider=llm_provider,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
            llm_api_key_env=llm_api_key_env,
        )
    submitted_total = int(resume_state.get("submitted_total") or 0)
    recorded_total = int(resume_state.get("recorded_total") or 0)
    expanded_submitted_total = int(resume_state.get("expanded_submitted_total") or 0)
    expanded_recorded_total = int(resume_state.get("expanded_recorded_total") or 0)
    refine_submitted_total = int(resume_state.get("refine_submitted_total") or 0)
    refine_recorded_total = int(resume_state.get("refine_recorded_total") or 0)
    failed_total = int(resume_state.get("failed_total") or 0)
    task_sequence = int(resume_state.get("task_sequence") or 0)
    empty_generation_rounds = 0
    submitted_by_group = {
        group: int((resume_state.get("submitted_by_group") or {}).get(group) or 0)
        for group in group_memory_dirs
    }
    recorded_by_group = {
        group: int((resume_state.get("recorded_by_group") or {}).get(group) or 0)
        for group in group_memory_dirs
    }
    reserved_families: set[str] = set()
    available_slots = [f"slot_{index:02d}" for index in range(1, slot_count + 1)]
    futures: Dict[Future, Dict[str, Any]] = {}

    def public_task_info(task_info: Dict[str, Any]) -> Dict[str, Any]:
        return {key: value for key, value in task_info.items() if not str(key).startswith("_")}

    def active_slot_names() -> List[str]:
        return sorted(str(info["slot"]) for info in futures.values())

    if resume:
        messages.append(
            f"Resuming async_slots from recorded_total={recorded_total}, "
            f"historical_submitted_total={int(resume_state.get('historical_submitted_total') or 0)}, "
            f"next_task_sequence={task_sequence + 1}."
        )

    _log_scheduler_event(
        scheduler_log,
        {
            "event": "scheduler_resume" if resume else "scheduler_start",
            "scheduler": "async_slots",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "resume": resume,
            "resume_attempt_count": int(resume_state.get("attempt_count") or 0),
            "historical_submitted_total": int(resume_state.get("historical_submitted_total") or 0),
            "target_attempts": target_attempts,
            "slot_count": slot_count,
            "slot_workers": slot_workers,
            "total_workers": total_workers,
            "submitted_total": submitted_total,
            "recorded_total": recorded_total,
            "submitted_by_group": dict(submitted_by_group),
            "recorded_by_group": dict(recorded_by_group),
            "expanded_parameter_samples": expanded_parameter_samples,
            "expanded_chi2_threshold": expanded_chi2_threshold,
            "refine_parameter_samples": refine_parameter_samples,
            "refine_chi2_threshold": refine_chi2_threshold,
            "diversity_strength": diversity_strength,
            "llm_provider": llm_provider,
            "llm_model": llm_model,
            "llm_base_url": llm_base_url,
            "llm_api_key_env": llm_api_key_env,
            "group_mode": group_mode,
        },
        run_name=name,
    )

    def submit_validation_task(
        executor: ThreadPoolExecutor,
        *,
        task_info: Dict[str, Any],
        entries: List[Dict[str, Any]],
        entry_summaries: List[Dict[str, Any]],
        parameter_samples: int,
        rng_seed: int,
    ) -> None:
        future = executor.submit(
            _run_validation_bucket_task,
            run_name=name,
            proposal_dir=proposal_dir,
            agent_dir=Path(str(task_info["agent_run_dir"])),
            validation_wave=str(task_info["validation_wave"]),
            complexity_bucket=str(task_info.get("runtime_bucket") or "slot"),
            entries=entries,
            entry_summaries=entry_summaries,
            initial_parameter_samples=parameter_samples,
            timeout_setup=timeout_setup,
            n_workers=slot_workers,
            rng_seed=rng_seed,
            group_mode=group_mode,
            track_mode=track_mode,
            complexity_split=True,
        )
        futures[future] = task_info

    def launch_one(executor: ThreadPoolExecutor) -> bool:
        nonlocal submitted_total, task_sequence, empty_generation_rounds
        if submitted_total >= target_attempts or not available_slots:
            return False
        slot = available_slots.pop(0)
        task_sequence += 1
        task_id = f"task_{task_sequence:06d}"
        seed_for_task = seed + task_sequence * 100003 + int(slot.split("_")[-1]) * 1009
        entry, entry_summary, family, proposal_messages = _generate_slot_entry(
            context=context,
            memory_dir=memory_dir,
            group_memory_dirs=group_memory_dirs,
            group_mode=group_mode,
            eh_track_fraction=eh_track_fraction,
            submitted_by_group=submitted_by_group,
            proposal_dir=proposal_dir,
            proposal_mode=proposal_mode,
            llm_provider=llm_provider,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
            llm_api_key_env=llm_api_key_env,
            llm_fallback=llm_fallback,
            llm_api_timeout=llm_api_timeout,
            seed=seed_for_task,
            task_id=task_id,
            reserved_families=reserved_families,
            diversity_strength=diversity_strength,
        )
        messages.extend(proposal_messages)
        if entry is None or entry_summary is None or family is None:
            available_slots.append(slot)
            empty_generation_rounds += 1
            _log_scheduler_event(
                scheduler_log,
                {
                    "event": "slot_waiting_for_entry",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "slot": slot,
                    "task_id": task_id,
                    "empty_generation_rounds": empty_generation_rounds,
                    "submitted_total": submitted_total,
                    "recorded_total": recorded_total,
                    "target_attempts": target_attempts,
                    "active_slots": active_slot_names(),
                },
                run_name=name,
            )
            return False

        empty_generation_rounds = 0
        reserved_families.add(family)
        group = str(entry.get("proposal_group") or "open_search")
        submitted_by_group[group] = submitted_by_group.get(group, 0) + 1
        submitted_total += 1
        entry["scheduler_task_id"] = task_id
        entry["scheduler_lane"] = slot
        entry["scheduler_slot"] = slot
        entry["batch_wave"] = task_sequence
        validation_wave = f"{task_id}_{slot}"
        agent_dir = _async_agent_run_dir(name, task_id, slot)
        task_info = {
            "task_id": task_id,
            "slot": slot,
            "lane": slot,
            "validation_stage": "initial",
            "validation_wave": validation_wave,
            "batch_size": 1,
            "worker_count": slot_workers,
            "parameter_samples": initial_parameter_samples,
            "agent_run_dir": str(agent_dir),
            "family": family,
            "proposal_group": group,
            "theory_track": entry.get("theory_track"),
            "scalar_config": entry.get("scalar_config"),
            "runtime_bucket": entry.get("complexity_bucket"),
            "structural_complexity_bucket": entry.get("structural_complexity_bucket"),
            "runtime_sort_seconds": entry.get("runtime_sort_seconds"),
            "runtime_sort_source": entry.get("runtime_sort_source"),
            "memory_snapshot_attempt_count": entry.get("memory_snapshot_attempt_count"),
            "memory_snapshot_timestamp": entry.get("memory_snapshot_timestamp"),
            "parameter_memory_attempt_count": int((entry_summary or {}).get("total_attempts") or 0),
            "estimated_elapsed_sec": _estimated_bucket_seconds([entry]),
            "proposal_mode": entry.get("proposal_mode"),
            "llm_provider": entry.get("llm_provider"),
            "llm_model": entry.get("llm_model"),
            "llm_base_url": entry.get("llm_base_url"),
            "llm_api_key_env": entry.get("llm_api_key_env"),
            "llm_latency_sec": entry.get("llm_latency_sec"),
            "_entries": [entry],
            "_submitted_monotonic": time.monotonic(),
            "_last_slow_signal_elapsed_sec": 0.0,
        }
        _log_scheduler_event(
            scheduler_log,
            {
                "event": "submitted",
                "scheduler": "async_slots",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                **public_task_info(task_info),
                "submitted_total": submitted_total,
                "recorded_total": recorded_total,
                "expanded_submitted_total": expanded_submitted_total,
                "expanded_recorded_total": expanded_recorded_total,
                "refine_submitted_total": refine_submitted_total,
                "refine_recorded_total": refine_recorded_total,
                "failed_total": failed_total,
                "target_attempts": target_attempts,
                "submitted_by_group": dict(submitted_by_group),
                "recorded_by_group": dict(recorded_by_group),
                "active_slots": active_slot_names(),
            },
            run_name=name,
        )
        submit_validation_task(
            executor,
            task_info=task_info,
            entries=[entry],
            entry_summaries=[entry_summary],
            parameter_samples=initial_parameter_samples,
            rng_seed=seed + task_sequence * 65537,
        )
        return True

    def record_slow_running_signals() -> None:
        now = time.monotonic()
        for task_info in futures.values():
            if str(task_info.get("validation_stage") or "initial") != "initial":
                continue
            submitted_at = float(task_info.get("_submitted_monotonic") or now)
            elapsed = now - submitted_at
            estimated = float(task_info.get("estimated_elapsed_sec") or 0.0)
            threshold = max(ASYNC_SLOW_SIGNAL_INTERVAL_SECONDS, estimated * 1.5)
            last_signal = float(task_info.get("_last_slow_signal_elapsed_sec") or 0.0)
            if elapsed < threshold or elapsed - last_signal < ASYNC_SLOW_SIGNAL_INTERVAL_SECONDS:
                continue
            entries = task_info.get("_entries")
            if not isinstance(entries, list) or not entries:
                continue
            _update_runtime_prior_from_entries(
                memory_dir=memory_dir,
                entries=[entry for entry in entries if isinstance(entry, dict)],
                elapsed_sec=elapsed,
                signal="running_lower_bound",
                weight=0.25,
            )
            task_info["_last_slow_signal_elapsed_sec"] = elapsed
            _log_scheduler_event(
                scheduler_log,
                {
                    "event": "runtime_slow_signal",
                    "scheduler": "async_slots",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    **public_task_info(task_info),
                    "running_elapsed_sec": round(elapsed, 3),
                    "submitted_total": submitted_total,
                    "recorded_total": recorded_total,
                    "failed_total": failed_total,
                    "target_attempts": target_attempts,
                },
                run_name=name,
            )

    with ThreadPoolExecutor(max_workers=slot_count) as executor:
        while recorded_total < target_attempts or futures:
            while submitted_total < target_attempts and len(futures) < slot_count:
                if not launch_one(executor):
                    if empty_generation_rounds >= max(3, slot_count):
                        break
                    continue
            if not futures:
                break
            record_slow_running_signals()
            done, _pending = wait(
                futures.keys(),
                timeout=ASYNC_WAIT_POLL_SECONDS,
                return_when=FIRST_COMPLETED,
            )
            if not done:
                record_slow_running_signals()
                continue
            for future in done:
                task_info = futures.pop(future)
                slot = str(task_info["slot"])
                release_slot = True
                try:
                    task_result = future.result()
                    wave_records = _record_validation_task_result(
                        task_result=task_result,
                        memory_dir=memory_dir,
                        group_memory_dirs=group_memory_dirs,
                        proposal_dir=proposal_dir,
                        traces=traces,
                        update_runtime_prior=str(task_info.get("validation_stage") or "initial") == "initial",
                    )
                    record_count = len(wave_records)
                    validation_stage = str(task_info.get("validation_stage") or "initial")
                    if validation_stage == "expanded":
                        expanded_recorded_total += record_count
                    elif validation_stage == "refine":
                        refine_recorded_total += record_count
                    else:
                        recorded_total += record_count
                    group = str(task_info.get("proposal_group") or "open_search")
                    if validation_stage == "initial":
                        recorded_by_group[group] = recorded_by_group.get(group, 0) + record_count
                    best = min((r.get("chi2") for r in wave_records if r.get("chi2") is not None), default=None)
                    refine_threshold = float(refine_chi2_threshold)
                    refine_samples = int(refine_parameter_samples)
                    refine_policy_basis = "uniform_all_theory_tracks"
                    should_expand = (
                        validation_stage == "initial"
                        and expanded_parameter_samples > initial_parameter_samples
                        and expanded_chi2_threshold > 0.0
                        and best is not None
                        and float(best) < float(expanded_chi2_threshold)
                    )
                    should_refine = (
                        validation_stage == "expanded"
                        and refine_samples > expanded_parameter_samples
                        and refine_threshold > 0.0
                        and best is not None
                        and float(best) < float(refine_threshold)
                    )
                    messages.append(
                        f"Async slot {slot} {task_info['task_id']} {validation_stage} complete; "
                        f"best_chi2={best}."
                    )
                    _log_scheduler_event(
                        scheduler_log,
                        {
                            "event": "recorded",
                            "scheduler": "async_slots",
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                            **public_task_info(task_info),
                            "elapsed_sec": task_result.get("elapsed_sec"),
                            "record_count": record_count,
                            "best_chi2": best,
                            "refine_chi2_threshold_applied": refine_threshold,
                            "refine_parameter_samples_applied": refine_samples,
                            "refine_policy_basis": refine_policy_basis,
                            "expanded_triggered": should_expand,
                            "refine_triggered": should_refine,
                            "submitted_total": submitted_total,
                            "recorded_total": recorded_total,
                            "expanded_submitted_total": expanded_submitted_total,
                            "expanded_recorded_total": expanded_recorded_total,
                            "refine_submitted_total": refine_submitted_total,
                            "refine_recorded_total": refine_recorded_total,
                            "failed_total": failed_total,
                            "target_attempts": target_attempts,
                            "submitted_by_group": dict(submitted_by_group),
                            "recorded_by_group": dict(recorded_by_group),
                            "active_slots": active_slot_names(),
                        },
                        run_name=name,
                    )
                    if should_expand:
                        expanded_submitted_total += 1
                        expanded_task_id = f"{task_info['task_id']}_expanded"
                        expanded_validation_wave = f"{expanded_task_id}_{slot}"
                        expanded_entry = dict((task_info.get("_entries") or [{}])[0])
                        expanded_entry["scheduler_task_id"] = expanded_task_id
                        expanded_entry["scheduler_lane"] = slot
                        expanded_entry["scheduler_slot"] = slot
                        expanded_entry["validation_stage"] = "expanded"
                        expanded_entry["expanded_from_task_id"] = task_info["task_id"]
                        expanded_entry["batch_wave"] = expanded_entry.get("batch_wave") or 0
                        expanded_summary = _load_summary(memory_dir)
                        expanded_entry["memory_snapshot_attempt_count"] = int(expanded_summary.get("total_attempts") or 0)
                        expanded_entry["memory_snapshot_timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
                        expanded_agent_dir = _async_agent_run_dir(name, expanded_task_id, slot)
                        expanded_task_info = {
                            **{
                                key: value
                                for key, value in task_info.items()
                                if key
                                not in {
                                    "_entries",
                                    "_submitted_monotonic",
                                    "_last_slow_signal_elapsed_sec",
                                    "agent_run_dir",
                                    "validation_wave",
                                    "validation_stage",
                                    "parameter_samples",
                                }
                            },
                            "task_id": expanded_task_id,
                            "slot": slot,
                            "lane": slot,
                            "validation_stage": "expanded",
                            "expanded_from_task_id": task_info["task_id"],
                            "validation_wave": expanded_validation_wave,
                            "parameter_samples": expanded_parameter_samples,
                            "agent_run_dir": str(expanded_agent_dir),
                            "parameter_memory_attempt_count": int(expanded_summary.get("total_attempts") or 0),
                            "estimated_elapsed_sec": _estimated_bucket_seconds([expanded_entry]),
                            "_entries": [expanded_entry],
                            "_submitted_monotonic": time.monotonic(),
                            "_last_slow_signal_elapsed_sec": 0.0,
                        }
                        _log_scheduler_event(
                            scheduler_log,
                            {
                                "event": "expanded_submitted",
                                "scheduler": "async_slots",
                                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                                **public_task_info(expanded_task_info),
                                "trigger_best_chi2": best,
                                "expanded_chi2_threshold": expanded_chi2_threshold,
                                "submitted_total": submitted_total,
                                "recorded_total": recorded_total,
                                "expanded_submitted_total": expanded_submitted_total,
                                "expanded_recorded_total": expanded_recorded_total,
                                "refine_submitted_total": refine_submitted_total,
                                "refine_recorded_total": refine_recorded_total,
                                "failed_total": failed_total,
                                "target_attempts": target_attempts,
                                "submitted_by_group": dict(submitted_by_group),
                                "recorded_by_group": dict(recorded_by_group),
                                "active_slots": active_slot_names(),
                            },
                            run_name=name,
                        )
                        messages.append(
                            f"Async slot {slot} {task_info['task_id']} triggered expanded "
                            f"{expanded_parameter_samples} samples because best_chi2={best} "
                            f"< {expanded_chi2_threshold}."
                        )
                        submit_validation_task(
                            executor,
                            task_info=expanded_task_info,
                            entries=[expanded_entry],
                            entry_summaries=[expanded_summary],
                            parameter_samples=expanded_parameter_samples,
                            rng_seed=seed + (task_sequence + expanded_submitted_total) * 131071,
                        )
                        release_slot = False
                    elif should_refine:
                        refine_submitted_total += 1
                        refine_task_id = f"{task_info['task_id']}_refine"
                        refine_validation_wave = f"{refine_task_id}_{slot}"
                        refine_entry = dict((task_info.get("_entries") or [{}])[0])
                        refine_entry["scheduler_task_id"] = refine_task_id
                        refine_entry["scheduler_lane"] = slot
                        refine_entry["scheduler_slot"] = slot
                        refine_entry["validation_stage"] = "refine"
                        refine_entry["refine_from_task_id"] = task_info["task_id"]
                        refine_entry["expanded_from_task_id"] = task_info.get("expanded_from_task_id")
                        refine_entry["batch_wave"] = refine_entry.get("batch_wave") or 0
                        refine_summary = _load_summary(memory_dir)
                        refine_entry["memory_snapshot_attempt_count"] = int(refine_summary.get("total_attempts") or 0)
                        refine_entry["memory_snapshot_timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
                        refine_agent_dir = _async_agent_run_dir(name, refine_task_id, slot)
                        refine_task_info = {
                            **{
                                key: value
                                for key, value in task_info.items()
                                if key
                                not in {
                                    "_entries",
                                    "_submitted_monotonic",
                                    "_last_slow_signal_elapsed_sec",
                                    "agent_run_dir",
                                    "validation_wave",
                                    "validation_stage",
                                    "parameter_samples",
                                }
                            },
                            "task_id": refine_task_id,
                            "slot": slot,
                            "lane": slot,
                            "validation_stage": "refine",
                            "refine_from_task_id": task_info["task_id"],
                            "expanded_from_task_id": task_info.get("expanded_from_task_id"),
                            "validation_wave": refine_validation_wave,
                            "parameter_samples": refine_samples,
                            "agent_run_dir": str(refine_agent_dir),
                            "parameter_memory_attempt_count": int(refine_summary.get("total_attempts") or 0),
                            "estimated_elapsed_sec": _estimated_bucket_seconds([refine_entry]),
                            "_entries": [refine_entry],
                            "_submitted_monotonic": time.monotonic(),
                            "_last_slow_signal_elapsed_sec": 0.0,
                        }
                        _log_scheduler_event(
                            scheduler_log,
                            {
                                "event": "refine_submitted",
                                "scheduler": "async_slots",
                                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                                **public_task_info(refine_task_info),
                                "trigger_best_chi2": best,
                                "refine_chi2_threshold": refine_threshold,
                                "refine_parameter_samples": refine_samples,
                                "refine_policy_basis": refine_policy_basis,
                                "refine_chi2_threshold_default": refine_chi2_threshold,
                                "refine_parameter_samples_default": refine_parameter_samples,
                                "submitted_total": submitted_total,
                                "recorded_total": recorded_total,
                                "expanded_submitted_total": expanded_submitted_total,
                                "expanded_recorded_total": expanded_recorded_total,
                                "refine_submitted_total": refine_submitted_total,
                                "refine_recorded_total": refine_recorded_total,
                                "failed_total": failed_total,
                                "target_attempts": target_attempts,
                                "submitted_by_group": dict(submitted_by_group),
                                "recorded_by_group": dict(recorded_by_group),
                                "active_slots": active_slot_names(),
                            },
                            run_name=name,
                        )
                        messages.append(
                            f"Async slot {slot} {task_info['task_id']} triggered refine "
                            f"{refine_samples} samples because expanded best_chi2={best} "
                            f"< {refine_threshold} ({refine_policy_basis}, group={group})."
                        )
                        submit_validation_task(
                            executor,
                            task_info=refine_task_info,
                            entries=[refine_entry],
                            entry_summaries=[refine_summary],
                            parameter_samples=refine_samples,
                            rng_seed=seed + (task_sequence + refine_submitted_total) * 262147,
                        )
                        release_slot = False
                except Exception as exc:
                    failed_total += 1
                    messages.append(
                        f"Async slot {slot} {task_info['task_id']} failed: {type(exc).__name__}: {exc}"
                    )
                    _log_scheduler_event(
                        scheduler_log,
                        {
                            "event": "failed",
                            "scheduler": "async_slots",
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                            **public_task_info(task_info),
                            "error": f"{type(exc).__name__}: {exc}",
                            "submitted_total": submitted_total,
                            "recorded_total": recorded_total,
                            "expanded_submitted_total": expanded_submitted_total,
                            "expanded_recorded_total": expanded_recorded_total,
                            "refine_submitted_total": refine_submitted_total,
                            "refine_recorded_total": refine_recorded_total,
                            "failed_total": failed_total,
                            "target_attempts": target_attempts,
                            "submitted_by_group": dict(submitted_by_group),
                            "recorded_by_group": dict(recorded_by_group),
                            "active_slots": active_slot_names(),
                        },
                        run_name=name,
                    )
                finally:
                    if release_slot:
                        available_slots.append(slot)
                        available_slots.sort()
                    family = task_info.get("family")
                    if family and release_slot:
                        reserved_families.discard(str(family))
        _log_scheduler_event(
            scheduler_log,
            {
                "event": "scheduler_complete",
                "scheduler": "async_slots",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "target_attempts": target_attempts,
                "slot_count": slot_count,
                "slot_workers": slot_workers,
                "submitted_total": submitted_total,
                "recorded_total": recorded_total,
                "expanded_submitted_total": expanded_submitted_total,
                "expanded_recorded_total": expanded_recorded_total,
                "refine_submitted_total": refine_submitted_total,
                "refine_recorded_total": refine_recorded_total,
                "failed_total": failed_total,
                "submitted_by_group": dict(submitted_by_group),
                "recorded_by_group": dict(recorded_by_group),
                "active_slots": active_slot_names(),
            },
            run_name=name,
        )
    return messages


def run_batch_agent(
    *,
    waves: int,
    batch_size: int,
    seed: int,
    run_name: Optional[str],
    initial_parameter_samples: int,
    expanded_parameter_samples: int = 3000,
    expanded_chi2_threshold: float = 2000.0,
    refine_parameter_samples: int = 5000,
    refine_chi2_threshold: float = 1638.0,
    timeout_setup: int,
    proposal_mode: str,
    llm_provider: str = "openai",
    llm_model: str = "",
    llm_base_url: str = "",
    llm_api_key_env: str = "",
    llm_fallback: str,
    llm_api_timeout: int,
    use_token_context_cache: bool,
    n_workers: int,
    group_mode: str = "open_only",
    track_mode: str = "split",
    eh_track_fraction: float = 0.5,
    complexity_split: bool = True,
    scheduler: str = "wave",
    target_attempts: Optional[int] = None,
    lane_batch_size_simple: int = 2,
    lane_batch_size_medium: int = 2,
    lane_batch_size_complex: int = 2,
    lane_batch_size_very_complex: int = 2,
    lane_workers_simple: int = 2,
    lane_workers_medium: int = 2,
    lane_workers_complex: int = 2,
    lane_workers_very_complex: int = 2,
    async_target_policy: str = "balanced_lane_floors",
    async_lane_min_fraction: float = DEFAULT_ASYNC_LANE_MIN_FRACTION,
    lane_min_attempts_simple: int = 0,
    lane_min_attempts_medium: int = 0,
    lane_min_attempts_complex: int = 0,
    lane_min_attempts_very_complex: int = 0,
    slot_count: int = DEFAULT_ASYNC_SLOT_COUNT,
    slot_workers: int = DEFAULT_ASYNC_SLOT_WORKERS,
    diversity_strength: float = 0.0,
    resume: bool = False,
) -> Dict[str, Any]:
    name = run_name or f"graph_agent_batch_{waves}x{batch_size}_{time.strftime('%Y%m%d_%H%M%S')}"
    proposal_dir = ROOT / "ai_theory_lab" / "proposals" / name
    memory_dir = ROOT / "ai_theory_lab" / "memory" / name
    if scheduler in {"async_lanes", "async_slots"} and not complexity_split:
        raise ValueError(f"{scheduler} scheduler requires complexity_split; remove --no-complexity-split.")
    if resume:
        if scheduler != "async_slots":
            raise ValueError("--resume is supported only with --scheduler async_slots.")
        missing = [str(path) for path in (proposal_dir, memory_dir) if not path.is_dir()]
        if missing:
            raise FileNotFoundError(f"Cannot resume {name}; missing run directories: {', '.join(missing)}")
    else:
        proposal_dir.mkdir(parents=True, exist_ok=False)
        memory_dir.mkdir(parents=True, exist_ok=False)
    group_names = (
        list(GROUP_SPECS)
        if group_mode in {"sector_split", "triad"}
        else ["eh_anchored", "non_eh"]
        if group_mode == "track_split"
        else ["open_search"]
    )
    group_memory_dirs = {group: memory_dir / "groups" / group for group in group_names}
    for group_dir in group_memory_dirs.values():
        group_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    context = _build_token_level_context(0, use_cache=use_token_context_cache)
    _write_token_level_context_summary(context, proposal_dir / "operator_catalog_summary.json")
    messages = [f"Initialized batch run {name}."]
    traces: List[Dict[str, Any]] = []

    if scheduler == "wave":
        for wave_index in range(1, waves + 1):
            summary = _load_summary(memory_dir)
            group_summaries = {group: _load_summary(path) for group, path in group_memory_dirs.items()}
            runtime_prior = _load_runtime_prior(memory_dir)
            entries, entry_summaries, proposal_messages, _ = _generate_entries_for_batch(
                context=context,
                summary=summary,
                group_summaries=group_summaries,
                group_mode=group_mode,
                eh_track_fraction=eh_track_fraction,
                rng=rng,
                seed=seed + wave_index * 1009,
                desired_count=batch_size,
                proposal_mode=proposal_mode,
                llm_provider=llm_provider,
                llm_model=llm_model,
                llm_base_url=llm_base_url,
                llm_api_key_env=llm_api_key_env,
                llm_fallback=llm_fallback,
                llm_api_timeout=llm_api_timeout,
                debug_dir=proposal_dir / "llm_proposal_debug",
                loop_prefix=f"wave_{wave_index:04d}",
                runtime_prior=runtime_prior,
                diversity_strength=diversity_strength,
            )
            messages.extend(proposal_messages)
            if not entries:
                messages.append(f"Wave {wave_index}: no entries generated; stopping.")
                break

            wave_batches = _complexity_batches(entries, entry_summaries, enabled=complexity_split)
            for complexity_bucket, bucket_entries, bucket_summaries in wave_batches:
                validation_wave = (
                    f"wave_{wave_index:04d}_{complexity_bucket}"
                    if complexity_split
                    else f"wave_{wave_index:04d}"
                )
                for entry in bucket_entries:
                    entry["batch_wave"] = wave_index
                agent_dir = _agent_run_dir(
                    name,
                    wave_index,
                    complexity_bucket if complexity_split else None,
                )
                task_result = _run_validation_bucket_task(
                    run_name=name,
                    proposal_dir=proposal_dir,
                    agent_dir=agent_dir,
                    validation_wave=validation_wave,
                    complexity_bucket=complexity_bucket,
                    entries=bucket_entries,
                    entry_summaries=bucket_summaries,
                    initial_parameter_samples=initial_parameter_samples,
                    timeout_setup=timeout_setup,
                    n_workers=n_workers,
                    rng_seed=seed + wave_index * 65537 + len(traces),
                    group_mode=group_mode,
                    track_mode=track_mode,
                    complexity_split=complexity_split,
                )
                wave_records = _record_validation_task_result(
                    task_result=task_result,
                    memory_dir=memory_dir,
                    group_memory_dirs=group_memory_dirs,
                    proposal_dir=proposal_dir,
                    traces=traces,
                )
                best = min((r.get("chi2") for r in wave_records if r.get("chi2") is not None), default=None)
                messages.append(
                    f"Wave {wave_index}/{waves} bucket {complexity_bucket} complete; "
                    f"batch_size={len(bucket_entries)}; best_chi2={best}."
                )
    elif scheduler == "async_lanes":
        async_messages = _run_async_lane_scheduler(
            name=name,
            proposal_dir=proposal_dir,
            memory_dir=memory_dir,
            group_memory_dirs=group_memory_dirs,
            context=context,
            traces=traces,
            target_attempts=target_attempts or waves * batch_size,
            batch_size=batch_size,
            seed=seed,
            initial_parameter_samples=initial_parameter_samples,
            timeout_setup=timeout_setup,
            proposal_mode=proposal_mode,
            llm_provider=llm_provider,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
            llm_api_key_env=llm_api_key_env,
            llm_fallback=llm_fallback,
            llm_api_timeout=llm_api_timeout,
            group_mode=group_mode,
            track_mode=track_mode,
            eh_track_fraction=eh_track_fraction,
            lane_batch_sizes={
                "simple": lane_batch_size_simple,
                "medium": lane_batch_size_medium,
                "complex": lane_batch_size_complex,
                "very_complex": lane_batch_size_very_complex,
            },
            lane_workers={
                "simple": lane_workers_simple,
                "medium": lane_workers_medium,
                "complex": lane_workers_complex,
                "very_complex": lane_workers_very_complex,
            },
            async_target_policy=async_target_policy,
            async_lane_min_fraction=async_lane_min_fraction,
            lane_min_attempts={
                "simple": lane_min_attempts_simple,
                "medium": lane_min_attempts_medium,
                "complex": lane_min_attempts_complex,
                "very_complex": lane_min_attempts_very_complex,
            },
            total_workers=n_workers,
            diversity_strength=diversity_strength,
        )
        messages.extend(async_messages)
    elif scheduler == "async_slots":
        async_messages = _run_async_slot_scheduler(
            name=name,
            proposal_dir=proposal_dir,
            memory_dir=memory_dir,
            group_memory_dirs=group_memory_dirs,
            context=context,
            traces=traces,
            target_attempts=target_attempts or waves * batch_size,
            seed=seed,
            initial_parameter_samples=initial_parameter_samples,
            expanded_parameter_samples=expanded_parameter_samples,
            expanded_chi2_threshold=expanded_chi2_threshold,
            refine_parameter_samples=refine_parameter_samples,
            refine_chi2_threshold=refine_chi2_threshold,
            timeout_setup=timeout_setup,
            proposal_mode=proposal_mode,
            llm_provider=llm_provider,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
            llm_api_key_env=llm_api_key_env,
            llm_fallback=llm_fallback,
            llm_api_timeout=llm_api_timeout,
            group_mode=group_mode,
            track_mode=track_mode,
            eh_track_fraction=eh_track_fraction,
            slot_count=slot_count or n_workers,
            slot_workers=slot_workers,
            total_workers=n_workers,
            diversity_strength=diversity_strength,
            resume=resume,
        )
        messages.extend(async_messages)
    else:
        raise ValueError(f"Unknown scheduler: {scheduler}")

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
        "llm_provider": llm_provider,
        "llm_model": llm_model,
        "llm_base_url": llm_base_url,
        "llm_api_key_env": llm_api_key_env,
        "initial_parameter_samples": initial_parameter_samples,
        "expanded_parameter_samples": expanded_parameter_samples,
        "expanded_chi2_threshold": expanded_chi2_threshold,
        "refine_parameter_samples": refine_parameter_samples,
        "refine_chi2_threshold": refine_chi2_threshold,
        "group_mode": group_mode,
        "track_mode": track_mode,
        "eh_track_fraction": eh_track_fraction,
        "complexity_split": complexity_split,
        "scheduler": scheduler,
        "target_attempts": target_attempts or waves * batch_size,
        "async_target_policy": async_target_policy,
        "async_lane_min_fraction": async_lane_min_fraction,
        "lane_min_attempts": {
            "simple": lane_min_attempts_simple,
            "medium": lane_min_attempts_medium,
            "complex": lane_min_attempts_complex,
            "very_complex": lane_min_attempts_very_complex,
        },
        "lane_workers": {
            "simple": lane_workers_simple,
            "medium": lane_workers_medium,
            "complex": lane_workers_complex,
            "very_complex": lane_workers_very_complex,
        },
        "lane_batch_sizes": {
            "simple": lane_batch_size_simple,
            "medium": lane_batch_size_medium,
            "complex": lane_batch_size_complex,
            "very_complex": lane_batch_size_very_complex,
        },
        "slot_count": slot_count or n_workers,
        "slot_workers": slot_workers,
        "diversity_strength": diversity_strength,
        "resume": resume,
    }
    (proposal_dir / "run_summary.json").write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    return output


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run mini-batch cold-start theory discovery.")
    parser.add_argument("--waves", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260607)
    parser.add_argument("--run-name")
    parser.add_argument("--initial-parameter-samples", type=int, default=1000)
    parser.add_argument(
        "--expanded-parameter-samples",
        type=int,
        default=3000,
        help=(
            "For async_slots, rerun an initially promising theory with this many "
            "samples. Set <= initial samples to disable."
        ),
    )
    parser.add_argument(
        "--expanded-chi2-threshold",
        type=float,
        default=2000.0,
        help=(
            "For async_slots, trigger expanded sampling only when the initial "
            "validation has best chi2 below this threshold."
        ),
    )
    parser.add_argument(
        "--refine-parameter-samples",
        type=int,
        default=5000,
        help=(
            "For async_slots, rerun an expanded theory with this many samples "
            "when it passes the refine chi2 threshold. Set <= expanded samples to disable."
        ),
    )
    parser.add_argument(
        "--refine-chi2-threshold",
        type=float,
        default=1638.0,
        help=(
            "For async_slots, trigger 5000-sample refinement only when expanded "
            "validation has best chi2 below this threshold. This is the default "
            "threshold for theories not classified as non_eh."
        ),
    )
    parser.add_argument("--timeout-setup", type=int, default=1200)
    parser.add_argument("--proposal-mode", choices=("deterministic", "llm"), default="deterministic")
    parser.add_argument(
        "--llm-provider",
        choices=("openai", "openai_compatible", "anthropic"),
        default="openai",
        help=(
            "LLM API backend for --proposal-mode llm. openai uses the native "
            "OpenAI Responses API; anthropic uses the Claude Messages API; "
            "openai_compatible uses Chat Completions with --llm-base-url."
        ),
    )
    parser.add_argument("--llm-model", default="")
    parser.add_argument(
        "--llm-base-url",
        default="",
        help=(
            "Base URL for openai_compatible providers such as Gemini, DashScope/Qwen, "
            "Requesty, OpenRouter, DeepSeek, or Ollama. For anthropic this may point "
            "to an Anthropic-compatible /v1 endpoint."
        ),
    )
    parser.add_argument(
        "--llm-api-key-env",
        default="",
        help="Environment variable containing the API key for the selected LLM provider.",
    )
    parser.add_argument(
        "--llm-fallback",
        choices=("deterministic", "skip", "fail"),
        default="deterministic",
        help=(
            "After exhausted LLM retries: deterministic uses the local policy, skip omits "
            "that proposal and keeps filling the target, and fail aborts the run."
        ),
    )
    parser.add_argument("--llm-api-timeout", type=int, default=120)
    parser.add_argument("--no-token-context-cache", action="store_true")
    parser.add_argument("--n-workers", type=int, default=8)
    parser.add_argument(
        "--group-mode",
        choices=("open_only", "sector_split", "triad", "track_split", "mixed"),
        default="open_only",
        help=(
            "Proposal sector schedule. open_only sends every initial theory to unrestricted open_search; "
            "sector_split uses 50%% open_search and 50%% dedicated non_eh; mixed is a legacy alias for open_only."
        ),
    )
    parser.add_argument("--track-mode", choices=("split", "mixed"), default="split")
    parser.add_argument("--eh-track-fraction", type=float, default=0.5)
    parser.add_argument(
        "--scheduler",
        choices=("wave", "async_lanes", "async_slots"),
        default="wave",
        help=(
            "Validation scheduler. wave preserves old wave-by-wave order; "
            "async_lanes keeps runtime quantile lanes replenished independently; "
            "async_slots keeps independent batch=1 validation slots full."
        ),
    )
    parser.add_argument(
        "--target-attempts",
        type=int,
        default=0,
        help="Global completed initial-theory target for async schedulers. Defaults to waves * batch_size.",
    )
    parser.add_argument(
        "--async-target-policy",
        choices=ASYNC_TARGET_POLICIES,
        default="balanced_lane_floors",
        help=(
            "async_lanes stop policy. balanced_lane_floors keeps running until "
            "the global target and per-lane minimums are met; global_recorded_total "
            "reproduces throughput-only scheduling."
        ),
    )
    parser.add_argument(
        "--async-lane-min-fraction",
        type=float,
        default=DEFAULT_ASYNC_LANE_MIN_FRACTION,
        help=(
            "For balanced_lane_floors, require each lane to record at least this "
            "fraction of target_attempts unless an explicit per-lane minimum is larger."
        ),
    )
    parser.add_argument("--lane-batch-size-simple", type=int, default=2)
    parser.add_argument("--lane-batch-size-medium", type=int, default=2)
    parser.add_argument("--lane-batch-size-complex", type=int, default=2)
    parser.add_argument("--lane-batch-size-very-complex", type=int, default=2)
    parser.add_argument("--lane-workers-simple", type=int, default=2)
    parser.add_argument("--lane-workers-medium", type=int, default=2)
    parser.add_argument("--lane-workers-complex", type=int, default=2)
    parser.add_argument("--lane-workers-very-complex", type=int, default=2)
    parser.add_argument("--lane-min-attempts-simple", type=int, default=0)
    parser.add_argument("--lane-min-attempts-medium", type=int, default=0)
    parser.add_argument("--lane-min-attempts-complex", type=int, default=0)
    parser.add_argument("--lane-min-attempts-very-complex", type=int, default=0)
    parser.add_argument(
        "--slot-count",
        type=int,
        default=DEFAULT_ASYNC_SLOT_COUNT,
        help="For async_slots, number of independent validation slots. Defaults to --n-workers.",
    )
    parser.add_argument(
        "--slot-workers",
        type=int,
        default=DEFAULT_ASYNC_SLOT_WORKERS,
        help="For async_slots, Solver workers per validation slot. Use 1 for one CPU per slot.",
    )
    parser.add_argument(
        "--diversity-strength",
        type=float,
        default=0.0,
        help=(
            "Proposal-time anti-collapse strength in [0, 1]. "
            "Higher values down-rank exact/coarse families already explored in current-loop memory."
        ),
    )
    parser.add_argument(
        "--no-complexity-split",
        action="store_true",
        help="Disable runtime validation buckets and validate each proposal wave as one batch.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Resume an existing async_slots run in place. Completed initial attempts are "
            "recounted from attempt_history.jsonl; crash-boundary unrecorded tasks are replaced."
        ),
    )
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)
    output = run_batch_agent(
        waves=args.waves,
        batch_size=args.batch_size,
        seed=args.seed,
        run_name=args.run_name,
        initial_parameter_samples=args.initial_parameter_samples,
        expanded_parameter_samples=args.expanded_parameter_samples,
        expanded_chi2_threshold=args.expanded_chi2_threshold,
        refine_parameter_samples=args.refine_parameter_samples,
        refine_chi2_threshold=args.refine_chi2_threshold,
        timeout_setup=args.timeout_setup,
        proposal_mode=args.proposal_mode,
        llm_provider=args.llm_provider,
        llm_model=args.llm_model,
        llm_base_url=args.llm_base_url,
        llm_api_key_env=args.llm_api_key_env,
        llm_fallback=args.llm_fallback,
        llm_api_timeout=args.llm_api_timeout,
        use_token_context_cache=not args.no_token_context_cache,
        n_workers=args.n_workers,
        group_mode=args.group_mode,
        track_mode=args.track_mode,
        eh_track_fraction=args.eh_track_fraction,
        complexity_split=not args.no_complexity_split,
        scheduler=args.scheduler,
        target_attempts=args.target_attempts or None,
        lane_batch_size_simple=args.lane_batch_size_simple,
        lane_batch_size_medium=args.lane_batch_size_medium,
        lane_batch_size_complex=args.lane_batch_size_complex,
        lane_batch_size_very_complex=args.lane_batch_size_very_complex,
        lane_workers_simple=args.lane_workers_simple,
        lane_workers_medium=args.lane_workers_medium,
        lane_workers_complex=args.lane_workers_complex,
        lane_workers_very_complex=args.lane_workers_very_complex,
        async_target_policy=args.async_target_policy,
        async_lane_min_fraction=args.async_lane_min_fraction,
        lane_min_attempts_simple=args.lane_min_attempts_simple,
        lane_min_attempts_medium=args.lane_min_attempts_medium,
        lane_min_attempts_complex=args.lane_min_attempts_complex,
        lane_min_attempts_very_complex=args.lane_min_attempts_very_complex,
        slot_count=args.slot_count,
        slot_workers=args.slot_workers,
        diversity_strength=args.diversity_strength,
        resume=args.resume,
    )
    print(json.dumps(output, indent=2 if args.pretty else None, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
