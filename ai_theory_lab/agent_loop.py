"""Reflection and prior updates for the cold-start agent loop."""

from __future__ import annotations

import csv
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Any, Dict, Iterable, List, Optional

from .config_p import PARAMETER_PRIOR_UPDATE
from .dataset import chi2_quality_tier, theory_features


REFLECTIONS_FILENAME = "agent_reflections.jsonl"
STRUCTURE_PRIOR_FILENAME = "structure_prior.json"
PARAMETER_PRIOR_FILENAME = "parameter_prior.json"


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

SCALAR_FAMILIES = ("none", "phi1_only", "phi2_only", "both")
MIN_SCALAR_FAMILY_EXPLORATION_PROBABILITY = 0.08


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _safe_float(value: Any) -> Optional[float]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _quantile(values: List[float], q: float) -> Optional[float]:
    if not values:
        return None
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round(q * (len(ordered) - 1)))))
    return ordered[index]


def _read_all_samples(path: Optional[str], limit: int = 5000) -> List[Dict[str, str]]:
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


def _accepted_sample_rows(attempts: Iterable[Dict[str, Any]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for attempt in attempts:
        for row in _read_all_samples(attempt.get("all_samples_summary_path")):
            chi2 = _safe_float(row.get("chi2"))
            if row.get("success") == "True" and chi2 is not None:
                item = dict(row)
                item["_attempt_loop_id"] = str(attempt.get("loop_id"))
                rows.append(item)
    rows.sort(key=lambda row: float(row.get("chi2", "inf")))
    return rows


def _reject_count(attempt: Dict[str, Any], patterns: Iterable[str]) -> int:
    total = 0
    needles = tuple(pattern.lower() for pattern in patterns)
    for row in attempt.get("top_reject_reasons") or []:
        if not isinstance(row, dict):
            continue
        reason = str(row.get("reason") or "").lower()
        if not any(needle in reason for needle in needles):
            continue
        try:
            total += int(row.get("count") or 0)
        except (TypeError, ValueError):
            continue
    return total


def _attempt_sample_counts(attempt: Dict[str, Any]) -> Dict[str, int]:
    rows = _read_all_samples(attempt.get("all_samples_summary_path"))
    accepted = 0
    q_root_failures = _reject_count(attempt, ("no acceptable real q", "_0 root"))
    no_scalar_failures = _reject_count(attempt, ("no-scalar constraint", "no scalar constraint"))
    constraint_drift = _reject_count(attempt, ("constraint drift",))
    integration_failure = _reject_count(attempt, ("solve_ivp failed", "integration failed", "ivp failed"))
    for row in rows:
        chi2 = _safe_float(row.get("chi2"))
        if row.get("success") == "True" and chi2 is not None:
            accepted += 1
    total = len(rows)
    if total <= 0:
        try:
            total = int(((attempt.get("theory") or {}).get("parameter_sample_count")) or 0)
        except (TypeError, ValueError):
            total = 0
    return {
        "total": total,
        "accepted": accepted,
        "q_initial_root_failure": q_root_failures,
        "no_scalar_constraint": no_scalar_failures,
        "constraint_drift": constraint_drift,
        "integration_failure": integration_failure,
    }


def _numeric_prior(
    values: List[float],
    *,
    log: bool = False,
    quantile_low: float = 0.15,
    quantile_high: float = 0.85,
) -> Optional[Dict[str, float]]:
    if not values:
        return None
    transformed = [math.log10(v) for v in values if log and v > 0] if log else list(values)
    if not transformed:
        return None
    lo = _quantile(transformed, quantile_low)
    hi = _quantile(transformed, quantile_high)
    center = median(transformed)
    if lo is None or hi is None:
        return None
    if lo == hi:
        spread = max(abs(center) * 0.1, 1e-3)
        lo -= spread
        hi += spread
    return {
        "low": float(lo),
        "high": float(hi),
        "center": float(center),
        "log10": bool(log),
        "count": len(transformed),
    }


def _parameter_prior_from_samples(rows: List[Dict[str, str]], attempt_count: int) -> Dict[str, Any]:
    min_attempts = int(PARAMETER_PRIOR_UPDATE["min_attempts_before_update"])
    min_accepted = int(PARAMETER_PRIOR_UPDATE["min_accepted_samples"])
    fixed_parameters = set(PARAMETER_PRIOR_UPDATE["fixed_parameters"])
    q_low = float(PARAMETER_PRIOR_UPDATE["quantile_low"])
    q_high = float(PARAMETER_PRIOR_UPDATE["quantile_high"])
    eligible = attempt_count >= min_attempts and len(rows) >= min_accepted

    top_rows = rows[: min(200, len(rows))]
    priors: Dict[str, Any] = {
        "source": "accepted_all_samples",
        "active": eligible,
        "attempt_count": attempt_count,
        "accepted_sample_count": len(rows),
        "min_attempts_before_update": min_attempts,
        "min_accepted_samples": min_accepted,
        "fixed_parameters": sorted(fixed_parameters),
        "parameters": {},
    }
    if not eligible:
        priors["message"] = "Parameter prior evidence is recorded, but defaults remain active until update thresholds are met."
        return priors

    for column in COMMON_PARAMETER_COLUMNS:
        if column in fixed_parameters:
            continue
        values = [_safe_float(row.get(column)) for row in top_rows]
        clean = [value for value in values if value is not None]
        if not clean:
            continue
        priors["parameters"][column] = _numeric_prior(
            clean,
            log=column.startswith("lambda_H") or column.startswith("mu") or column.startswith("fbar"),
            quantile_low=q_low,
            quantile_high=q_high,
        )

    coeff_values: List[float] = []
    signs = Counter()
    for row in top_rows:
        for key, value in row.items():
            if not key or key.startswith("coef:") or key.startswith("coefficient:"):
                continue
            if key.startswith("\\") or key in {"alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"}:
                number = _safe_float(value)
                if number is not None and number != 0:
                    coeff_values.append(abs(number))
                    signs["positive" if number > 0 else "negative"] += 1
    coeff_prior = _numeric_prior(coeff_values, log=True, quantile_low=q_low, quantile_high=q_high)
    if coeff_prior:
        priors["coefficient_log10_abs"] = coeff_prior
        total = max(1, signs["positive"] + signs["negative"])
        priors["coefficient_sign_weights"] = {
            "positive": signs["positive"] / total,
            "negative": signs["negative"] / total,
        }
    return priors


def _structure_prior_from_attempts(attempts: List[Dict[str, Any]], summary: Dict[str, Any]) -> Dict[str, Any]:
    accepted = [attempt for attempt in attempts if attempt.get("chi2") is not None]
    accepted.sort(key=lambda attempt: float(attempt["chi2"]))
    quality_accepted = [
        attempt
        for attempt in accepted
        if chi2_quality_tier(attempt.get("chi2")) in {"excellent", "competitive", "weak_accept"}
    ]
    scalar_counts = Counter()
    operator_counts = Counter()
    potential_counts = Counter()
    accepted_feature_counts = Counter()
    quality_counts = Counter(chi2_quality_tier(attempt.get("chi2")) for attempt in accepted)
    for attempt in quality_accepted[:10]:
        tier = chi2_quality_tier(attempt.get("chi2"))
        weight = {"excellent": 3.5, "competitive": 2.5, "weak_accept": 1.5}.get(tier, 0.0)
        if weight <= 0.0:
            continue
        theory = attempt.get("theory") or {}
        scalar_counts[str(theory.get("scalar_config"))] += weight
        potentials = theory.get("potential_types") if isinstance(theory.get("potential_types"), dict) else {}
        if potentials.get("phi1"):
            potential_counts[f"phi1:{potentials.get('phi1')}"] += weight
        if potentials.get("phi2"):
            potential_counts[f"phi2:{potentials.get('phi2')}"] += weight
        for operator in theory.get("operators") or []:
            operator_counts[str(operator)] += weight
        features = theory_features(theory)
        for name, value in features.items():
            if isinstance(value, bool) and value:
                accepted_feature_counts[name] += weight
            elif isinstance(value, str) and value not in {"None", ""}:
                accepted_feature_counts[f"{name}={value}"] += weight

    failed_tags = summary.get("failure_tag_counts") if isinstance(summary.get("failure_tag_counts"), dict) else {}
    failed_scalar_configs = Counter()
    failed_features = Counter()
    failed_operators = Counter()
    scalar_family_stats: Dict[str, Dict[str, Any]] = {
        family: {
            "attempts": 0,
            "validated_attempts": 0,
            "entered_solver_attempts": 0,
            "sample_count": 0,
            "accepted_sample_count": 0,
            "q_initial_root_failure_count": 0,
            "no_scalar_constraint_count": 0,
            "constraint_drift_count": 0,
            "integration_failure_count": 0,
            "q_not_determined_attempts": 0,
            "best_chi2": None,
            "chi2_values": [],
            "operator_family_counts": Counter(),
        }
        for family in SCALAR_FAMILIES
    }
    for attempt in attempts:
        theory = attempt.get("theory") or {}
        tags = set(attempt.get("failure_tags") or [])
        features = theory_features(theory)
        scalar_config = str(theory.get("scalar_config"))
        if scalar_config not in scalar_family_stats:
            scalar_family_stats[scalar_config] = {
                "attempts": 0,
                "validated_attempts": 0,
                "entered_solver_attempts": 0,
                "sample_count": 0,
                "accepted_sample_count": 0,
                "q_initial_root_failure_count": 0,
                "no_scalar_constraint_count": 0,
                "constraint_drift_count": 0,
                "integration_failure_count": 0,
                "q_not_determined_attempts": 0,
                "best_chi2": None,
                "chi2_values": [],
                "operator_family_counts": Counter(),
            }
        stats = scalar_family_stats[scalar_config]
        stats["attempts"] += 1
        if attempt.get("validated"):
            stats["validated_attempts"] += 1
        if attempt.get("entered_solver"):
            stats["entered_solver_attempts"] += 1
        chi2 = _safe_float(attempt.get("chi2"))
        if chi2 is not None:
            stats["chi2_values"].append(chi2)
            if stats["best_chi2"] is None or chi2 < float(stats["best_chi2"]):
                stats["best_chi2"] = chi2
        sample_counts = _attempt_sample_counts(attempt)
        stats["sample_count"] += sample_counts["total"]
        stats["accepted_sample_count"] += sample_counts["accepted"]
        stats["q_initial_root_failure_count"] += sample_counts["q_initial_root_failure"]
        stats["no_scalar_constraint_count"] += sample_counts["no_scalar_constraint"]
        stats["constraint_drift_count"] += sample_counts["constraint_drift"]
        stats["integration_failure_count"] += sample_counts["integration_failure"]
        if "q_not_determined" in tags:
            stats["q_not_determined_attempts"] += 1
        for name, value in features.items():
            if isinstance(value, bool) and value:
                stats["operator_family_counts"][name] += 1
            elif isinstance(value, str) and value not in {"None", ""}:
                stats["operator_family_counts"][f"{name}={value}"] += 1

        if attempt.get("validated"):
            continue
        operators = [str(operator) for operator in theory.get("operators") or []]
        if "q_initial_root_failure" in tags or "q_not_determined" in tags:
            failed_scalar_configs[scalar_config] += 1
            if features.get("has_phi1"):
                failed_features["has_phi1_with_q_failure"] += 1
            if features.get("has_phi2"):
                failed_features["has_phi2_with_q_failure"] += 1
            if features.get("has_both_scalars"):
                failed_features["has_both_scalars_with_q_failure"] += 1
        if "q_not_determined" in tags:
            for operator in operators:
                failed_operators[operator] += 1
            if features.get("has_derivative_operator"):
                failed_features["derivative_with_q_not_determined"] += 1
            if features.get("has_scalar_curvature") and features.get("has_derivative_operator"):
                failed_features["scalar_derivative_curvature_with_q_not_determined"] += 1
            if any(("φ" in op or "phi" in op) and ("∇" in op or "nabla" in op) for op in operators):
                failed_features["scalar_derivative_with_q_not_determined"] += 1
            if features.get("has_box_operator"):
                failed_features["box_operator_with_q_not_determined"] += 1
        if "no_scalar_constraint" in tags and scalar_config == "none":
            failed_scalar_configs["none"] += 1
            failed_features["is_no_scalar_with_constraint_failure"] += 1
        if scalar_config == "none" and "missing_ranking" in tags and "no_accepted_samples" in tags:
            failed_features["is_no_scalar_empty_ranking"] += 1
        if "constraint_drift" in tags or "integration_failure" in tags:
            if features.get("has_derivative_operator"):
                failed_features["derivative_with_numerical_failure"] += 1
            if features.get("has_high_curvature"):
                failed_features["high_curvature_with_numerical_failure"] += 1

    scalar_family_metrics: Dict[str, Dict[str, Any]] = {}
    for family, stats in scalar_family_stats.items():
        sample_count = int(stats["sample_count"])
        attempts_count = int(stats["attempts"])
        chi2_values = sorted(float(value) for value in stats["chi2_values"])
        scalar_family_metrics[family] = {
            "attempts": attempts_count,
            "validated_attempts": int(stats["validated_attempts"]),
            "entered_solver_attempts": int(stats["entered_solver_attempts"]),
            "validated_attempt_rate": (float(stats["validated_attempts"]) / attempts_count) if attempts_count else None,
            "entered_solver_attempt_rate": (float(stats["entered_solver_attempts"]) / attempts_count) if attempts_count else None,
            "sample_count": sample_count,
            "accepted_sample_count": int(stats["accepted_sample_count"]),
            "accepted_sample_rate": (float(stats["accepted_sample_count"]) / sample_count) if sample_count else None,
            "q_initial_root_failure_count": int(stats["q_initial_root_failure_count"]),
            "q_initial_root_failure_rate": (float(stats["q_initial_root_failure_count"]) / sample_count) if sample_count else None,
            "q_not_determined_attempts": int(stats["q_not_determined_attempts"]),
            "q_not_determined_attempt_rate": (float(stats["q_not_determined_attempts"]) / attempts_count) if attempts_count else None,
            "no_scalar_constraint_count": int(stats["no_scalar_constraint_count"]),
            "no_scalar_constraint_rate": (float(stats["no_scalar_constraint_count"]) / sample_count) if sample_count else None,
            "constraint_drift_count": int(stats["constraint_drift_count"]),
            "constraint_drift_rate": (float(stats["constraint_drift_count"]) / sample_count) if sample_count else None,
            "integration_failure_count": int(stats["integration_failure_count"]),
            "integration_failure_rate": (float(stats["integration_failure_count"]) / sample_count) if sample_count else None,
            "best_chi2": stats["best_chi2"],
            "median_chi2": median(chi2_values) if chi2_values else None,
            "chi2_quality_counts": dict(Counter(chi2_quality_tier(value) for value in chi2_values).most_common()),
            "operator_family_counts": dict(stats["operator_family_counts"].most_common(20)),
        }
    return {
        "source": "current_loop_feedback",
        "scalar_family_learning": {
            "principle": "same metrics and soft scoring are applied to none, phi1_only, phi2_only, and both; no scalar family is banned from exploration",
            "min_exploration_probability_per_family": MIN_SCALAR_FAMILY_EXPLORATION_PROBABILITY,
            "metrics": scalar_family_metrics,
        },
        "accepted_attempt_count": len(accepted),
        "quality_accepted_attempt_count": len(quality_accepted),
        "accepted_quality_counts": dict(quality_counts.most_common()),
        "preferred_scalar_configs": dict(scalar_counts.most_common()),
        "preferred_potentials": dict(potential_counts.most_common()),
        "preferred_operators": dict(operator_counts.most_common(20)),
        "preferred_features": dict(accepted_feature_counts.most_common(20)),
        "avoid_scalar_configs": dict(failed_scalar_configs.most_common()),
        "avoid_features": dict(failed_features.most_common()),
        "avoid_operators": dict(failed_operators.most_common(30)),
        "avoid_failure_tags": {
            key: value for key, value in failed_tags.items() if key in {"q_initial_root_failure", "q_not_determined", "no_scalar_constraint", "symbolic_timeout", "constraint_drift", "integration_failure"}
        },
        "best_chi2": summary.get("best_chi2"),
    }


def _reflection(attempts: List[Dict[str, Any]], summary: Dict[str, Any], parameter_prior: Dict[str, Any], structure_prior: Dict[str, Any]) -> Dict[str, Any]:
    last = attempts[-1] if attempts else {}
    tags = last.get("failure_tags") or []
    observations = [
        f"total_attempts={summary.get('total_attempts', 0)}",
        f"validated_count={summary.get('validated_count', 0)}",
        f"best_chi2={summary.get('best_chi2')}",
        f"last_loop_id={last.get('loop_id')}",
        f"last_tags={tags}",
    ]
    if structure_prior.get("preferred_scalar_configs"):
        observations.append(f"preferred_scalar_configs={structure_prior['preferred_scalar_configs']}")
    scalar_learning = structure_prior.get("scalar_family_learning") if isinstance(structure_prior.get("scalar_family_learning"), dict) else {}
    if scalar_learning.get("metrics"):
        observations.append(f"scalar_family_metrics={scalar_learning['metrics']}")
    if parameter_prior.get("accepted_sample_count"):
        observations.append(f"accepted_parameter_samples={parameter_prior['accepted_sample_count']}")

    next_actions: List[str] = []
    if structure_prior.get("preferred_scalar_configs"):
        next_actions.append("bias structure generation toward accepted scalar configurations and operators")
    if parameter_prior.get("parameters"):
        next_actions.append("sample common numerical parameters from accepted-sample quantile priors")
    if "q_not_determined" in tags:
        next_actions.append("avoid nearby scalar derivative structures that repeatedly fail q solving")
    if "q_initial_root_failure" in tags:
        next_actions.append("compare scalar-family root-success metrics and adjust the nearby structure/parameter prior without banning the family")
    if "no_scalar_constraint" in tags:
        next_actions.append("avoid no-scalar variants unless deliberately testing a constraint prior")
    if not next_actions:
        next_actions.append("continue exploration with learned policy score and duplicate cap")

    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "loop_id": last.get("loop_id"),
        "observations": observations,
        "next_actions": next_actions,
        "information_used": [
            "attempt_history.jsonl",
            "feedback_summary.json",
            "all_samples_summary.csv paths from current loop",
        ],
        "information_not_used": ["historical solver_result/top10 outputs"],
    }


def update_agent_loop_state(memory_dir: Path, summary: Dict[str, Any]) -> Dict[str, Any]:
    attempts = _load_jsonl(memory_dir / "attempt_history.jsonl")
    accepted_rows = _accepted_sample_rows(attempts)
    parameter_prior = _parameter_prior_from_samples(accepted_rows, len(attempts))
    structure_prior = _structure_prior_from_attempts(attempts, summary)
    reflection = _reflection(attempts, summary, parameter_prior, structure_prior)

    (memory_dir / PARAMETER_PRIOR_FILENAME).write_text(
        json.dumps(parameter_prior, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (memory_dir / STRUCTURE_PRIOR_FILENAME).write_text(
        json.dumps(structure_prior, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    with (memory_dir / REFLECTIONS_FILENAME).open("a", encoding="utf-8") as f:
        f.write(json.dumps(reflection, ensure_ascii=False) + "\n")

    return {
        "reflection_path": str(memory_dir / REFLECTIONS_FILENAME),
        "structure_prior_path": str(memory_dir / STRUCTURE_PRIOR_FILENAME),
        "parameter_prior_path": str(memory_dir / PARAMETER_PRIOR_FILENAME),
        "latest_reflection": reflection,
        "structure_prior": structure_prior,
        "parameter_prior": parameter_prior,
    }
