"""Structure-conditioned parameter memory for current-loop agent sampling."""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .dataset import chi2_quality_tier, fit_reward_for_chi2


JOINT_PARAMETER_PRIOR_FILENAME = "joint_parameter_prior.json"

COMMON_PARAMETER_COLUMNS = [
    "H0_km_s_Mpc",
    "Omega_m0",
    "lambda_H_Lambda_over_H0",
    "varphi1_0_phi1_over_Mp",
    "mu1_m1_over_H0",
    "fbar1_f1_over_Mp",
    "varphi2_0_phi2_over_Lambda",
    "q2_0_dvarphi2_dln_a",
    "mu2_m2_over_Lambda",
    "fbar2_f2_over_Lambda",
]
SAMPLE_MEMORY_COLUMNS = [
    *COMMON_PARAMETER_COLUMNS,
    "agent_correction_mode_code",
    "agent_sample_source_code",
]
RESULT_COLUMNS = {
    "success",
    "chi2",
    "chi2_total",
    "chi2_sn",
    "chi2_bao",
    "AIC",
    "BIC",
    "model_id",
    "lagrangian_id",
    "agent_parameter_sample_index",
    "reject_reason",
    "reason",
    "status",
    "message",
    "error",
}
COEFFICIENT_NAMES = {"alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"}
TOP_VECTOR_LIMIT = 80
BAD_VECTOR_LIMIT = 30
MAX_ROWS_PER_ATTEMPT = 6000


def _safe_float(value: Any) -> Optional[float]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _read_all_samples(path: Optional[str], limit: int = MAX_ROWS_PER_ATTEMPT) -> List[Dict[str, str]]:
    if not path:
        return []
    csv_path = Path(path)
    if not csv_path.exists():
        return []
    rows: List[Dict[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
            if len(rows) >= limit:
                break
    return rows


def _is_success(row: Dict[str, str]) -> bool:
    return str(row.get("success", "")).strip().lower() == "true" and _safe_float(row.get("chi2")) is not None


def _failure_penalty(row: Dict[str, str]) -> float:
    text = " ".join(
        str(row.get(key) or "")
        for key in ("reject_reason", "reason", "status", "message", "error")
    ).lower()
    if "no acceptable real q" in text or "_0 root" in text:
        return -2.0
    if "not determined" in text:
        return -2.0
    if "constraint drift" in text:
        return -1.5
    if "solve_ivp" in text or "integration" in text:
        return -1.5
    if "h(z)" in text or "hubble" in text:
        return -1.0
    return -0.3


def _sample_reward(row: Dict[str, str]) -> Tuple[float, str]:
    chi2 = _safe_float(row.get("chi2"))
    if _is_success(row) and chi2 is not None:
        reward = fit_reward_for_chi2(chi2)
        value = float(reward if reward is not None else 0.0)
        status = str(row.get("effective_correction_status") or "").strip().lower()
        if status == "active":
            value += 1.0
        elif status == "moderate":
            value += 0.2
        elif status == "weak":
            value *= 0.35
        elif status in {"tiny", "eh_dominated"}:
            value = min(value, -1.0)
        return (value, chi2_quality_tier(chi2))
    return (_failure_penalty(row), "rejected")


def _is_coefficient_key(key: str) -> bool:
    if key.startswith("\\"):
        return True
    if key in COEFFICIENT_NAMES:
        return True
    return False


def _sample_vector(row: Dict[str, str]) -> Dict[str, float]:
    sample: Dict[str, float] = {}
    for key in SAMPLE_MEMORY_COLUMNS:
        number = _safe_float(row.get(key))
        if number is not None:
            sample[key] = float(number)
    for key, value in row.items():
        if key in RESULT_COLUMNS or key in sample:
            continue
        if not _is_coefficient_key(key):
            continue
        number = _safe_float(value)
        if number is not None:
            sample[key] = float(number)
    return sample


def _attempt_keys(attempt: Dict[str, Any]) -> List[Tuple[str, str]]:
    theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
    scalar_config = str(theory.get("scalar_config") or "unknown")
    keys = [
        ("exact", str(attempt.get("family_key") or "unknown")),
        ("coarse", str(attempt.get("coarse_family_key") or attempt.get("family_key") or "unknown")),
        ("scalar", scalar_config),
        ("global", "all"),
    ]
    return [(level, key) for level, key in keys if key and key != "None"]


def _new_group() -> Dict[str, Any]:
    return {
        "record_count": 0,
        "accepted_count": 0,
        "positive_reward_count": 0,
        "reward_sum": 0.0,
        "best_chi2": None,
        "best_reward": None,
        "top_vectors": [],
        "bad_vectors": [],
    }


def _add_record(group: Dict[str, Any], record: Dict[str, Any]) -> None:
    group["record_count"] += 1
    group["reward_sum"] += float(record["reward"])
    if record["success"]:
        group["accepted_count"] += 1
    if float(record["reward"]) > 0.0:
        group["positive_reward_count"] += 1
        group["top_vectors"].append(record)
    elif float(record["reward"]) < 0.0:
        group["bad_vectors"].append(record)
    chi2 = record.get("chi2")
    if chi2 is not None and (group["best_chi2"] is None or float(chi2) < float(group["best_chi2"])):
        group["best_chi2"] = float(chi2)
    if group["best_reward"] is None or float(record["reward"]) > float(group["best_reward"]):
        group["best_reward"] = float(record["reward"])


def _finalize_group(group: Dict[str, Any]) -> Dict[str, Any]:
    top_vectors = sorted(
        group["top_vectors"],
        key=lambda item: (-float(item["reward"]), float(item["chi2"]) if item.get("chi2") is not None else math.inf),
    )[:TOP_VECTOR_LIMIT]
    bad_vectors = sorted(group["bad_vectors"], key=lambda item: float(item["reward"]))[:BAD_VECTOR_LIMIT]
    record_count = int(group["record_count"])
    accepted_count = int(group["accepted_count"])
    return {
        "record_count": record_count,
        "accepted_count": accepted_count,
        "accepted_rate": (accepted_count / record_count) if record_count else None,
        "positive_reward_count": int(group["positive_reward_count"]),
        "average_reward": (float(group["reward_sum"]) / record_count) if record_count else None,
        "best_chi2": group["best_chi2"],
        "best_reward": group["best_reward"],
        "top_vectors": top_vectors,
        "bad_vectors": bad_vectors,
    }


def build_joint_parameter_prior(attempts: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Build a current-loop, structure-conditioned memory from sample outcomes."""

    groups: Dict[str, Dict[str, Dict[str, Any]]] = {
        "exact": defaultdict(_new_group),
        "coarse": defaultdict(_new_group),
        "scalar": defaultdict(_new_group),
        "global": defaultdict(_new_group),
    }
    attempts_seen = 0
    rows_seen = 0
    accepted_rows = 0
    positive_rows = 0

    for attempt in attempts:
        attempts_seen += 1
        keys = _attempt_keys(attempt)
        rows = _read_all_samples(attempt.get("all_samples_summary_path"))
        for row in rows:
            vector = _sample_vector(row)
            if not vector:
                continue
            rows_seen += 1
            reward, tier = _sample_reward(row)
            success = _is_success(row)
            if success:
                accepted_rows += 1
            if reward > 0.0:
                positive_rows += 1
            record = {
                "loop_id": attempt.get("loop_id"),
                "agent_parameter_sample_index": _safe_float(row.get("agent_parameter_sample_index")),
                "success": bool(success),
                "chi2": _safe_float(row.get("chi2")),
                "reward": float(reward),
                "quality_tier": tier,
                "sample": vector,
            }
            for level, key in keys:
                _add_record(groups[level][key], record)

    finalized: Dict[str, Dict[str, Any]] = {}
    for level, level_groups in groups.items():
        finalized[level] = {
            key: _finalize_group(group)
            for key, group in sorted(level_groups.items())
            if int(group["record_count"]) > 0
        }

    return {
        "source": "current_loop_all_samples_summary",
        "attempt_count": attempts_seen,
        "sample_row_count": rows_seen,
        "accepted_sample_row_count": accepted_rows,
        "positive_reward_sample_row_count": positive_rows,
        "min_positive_vectors_for_sampling": 1,
        "max_top_vectors_per_group": TOP_VECTOR_LIMIT,
        "levels": ["exact", "coarse", "scalar", "global"],
        "families": finalized,
        "notes": (
            "This memory stores sample-level parameter vectors grouped by theory identity. "
            "Sampling uses positive-reward vectors first and falls back to ordinary priors "
            "when a matching group has no positive current-loop evidence."
        ),
    }
