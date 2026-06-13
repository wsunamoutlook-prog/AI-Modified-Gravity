"""Build learning records from agent validation attempts."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .effective_corrections import diagnostics_for_attempt


DATASET_FILENAME = "training_dataset.jsonl"
POLICY_SUMMARY_FILENAME = "policy_summary.json"
EXCELLENT_CHI2 = 1650.0
COMPETITIVE_CHI2 = 1700.0
WEAK_ACCEPT_CHI2 = 2000.0


def _operators(theory: Dict[str, Any]) -> List[str]:
    value = theory.get("operators")
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _theory_track(theory: Dict[str, Any]) -> str:
    explicit = theory.get("theory_track")
    if explicit:
        return str(explicit)
    operators = _operators(theory)
    if "R" in operators:
        return "eh_anchored"
    if any("R" in operator for operator in operators):
        return "non_eh"
    return "non_gravity"


def theory_features(theory: Dict[str, Any]) -> Dict[str, Any]:
    operators = _operators(theory)
    joined = " ".join(operators)
    scalar_config = str(theory.get("scalar_config"))
    potential_types = theory.get("potential_types") if isinstance(theory.get("potential_types"), dict) else {}
    has_scalar = scalar_config in {"phi1_only", "phi2_only", "both"}
    return {
        "scalar_config": scalar_config,
        "proposal_group": theory.get("proposal_group"),
        "theory_track": _theory_track(theory),
        "phi1_potential": potential_types.get("phi1"),
        "phi2_potential": potential_types.get("phi2"),
        "operator_count": len(operators),
        "operators": operators,
        "has_R_anchor": "R" in operators,
        "has_scalar": has_scalar,
        "has_phi1": scalar_config in {"phi1_only", "both"},
        "has_phi2": scalar_config in {"phi2_only", "both"},
        "has_both_scalars": scalar_config == "both",
        "is_no_scalar": scalar_config == "none",
        "has_scalar_curvature": has_scalar and ("R" in joined),
        "has_derivative_operator": ("∇" in joined) or ("nabla" in joined),
        "has_box_operator": "∇^{a}∇_{a}" in joined,
        "has_high_curvature": any(("R · R" in op) or ("R^{ab}" in op) or ("R_{ab}" in op) for op in operators),
        "has_pure_scalar_operator": any(("φ" in op) and ("R" not in op) for op in operators),
    }


def chi2_quality_tier(chi2: Any) -> str:
    try:
        value = float(chi2)
    except (TypeError, ValueError):
        return "none"
    if value <= EXCELLENT_CHI2:
        return "excellent"
    if value <= COMPETITIVE_CHI2:
        return "competitive"
    if value <= WEAK_ACCEPT_CHI2:
        return "weak_accept"
    return "poor_accept"


def fit_reward_for_chi2(chi2: Any) -> Optional[float]:
    try:
        value = float(chi2)
    except (TypeError, ValueError):
        return None
    if value <= EXCELLENT_CHI2:
        return max(10.0, 12.0 - max(0.0, value - 1600.0) / 70.0)
    if value <= COMPETITIVE_CHI2:
        return 9.0 - (value - EXCELLENT_CHI2) / 25.0
    if value <= WEAK_ACCEPT_CHI2:
        return 6.0 - (value - COMPETITIVE_CHI2) / 100.0
    return max(-4.0, -1.0 - (value - WEAK_ACCEPT_CHI2) / 400.0)


def discovery_reward_for_attempt(attempt: Dict[str, Any]) -> float:
    fit_reward = fit_reward_for_chi2(attempt.get("chi2"))
    if fit_reward is not None:
        theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
        track = attempt.get("theory_track") or _theory_track(theory)
        if track == "eh_anchored":
            diagnostics = diagnostics_for_attempt(attempt)
            status = diagnostics.get("effective_correction_status")
            if status == "active":
                return fit_reward + 0.3
            if status == "moderate":
                return fit_reward + 0.1
            return fit_reward
        diagnostics = diagnostics_for_attempt(attempt)
        status = diagnostics.get("effective_correction_status")
        if status == "eh_only":
            return fit_reward
        if status == "active":
            return fit_reward + 1.0
        if status == "moderate":
            return fit_reward
        if status == "weak":
            return fit_reward * 0.35
        if status in {"tiny", "eh_dominated"}:
            return -1.0
        return fit_reward

    return failure_reward_for_attempt(attempt)


def failure_reward_for_attempt(attempt: Dict[str, Any]) -> float:
    reward = -1.0
    if attempt.get("entered_solver"):
        reward += 0.5
    tags = set(attempt.get("failure_tags") or [])
    penalties = {
        "q_not_determined": -2.5,
        "q_initial_root_failure": -2.0,
        "no_scalar_constraint": -2.0,
        "symbolic_timeout": -2.5,
        "pre_sampling_timeout": -2.5,
        "constraint_drift": -1.5,
        "integration_failure": -1.5,
        "h_absurdly_large": -1.0,
        "no_accepted_samples": -0.5,
    }
    for tag, penalty in penalties.items():
        if tag in tags:
            reward += penalty
    return reward


def reward_for_attempt(attempt: Dict[str, Any]) -> float:
    return discovery_reward_for_attempt(attempt)


def _effective_diagnostics_for_record(attempt: Dict[str, Any]) -> Dict[str, Any]:
    if attempt.get("chi2") is None:
        return {}
    diagnostics = diagnostics_for_attempt(attempt)
    return {
        key: value
        for key, value in diagnostics.items()
        if key != "term_effects"
    }


def attempt_to_training_record(attempt: Dict[str, Any]) -> Dict[str, Any]:
    theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
    fit_reward = fit_reward_for_chi2(attempt.get("chi2"))
    effective_diagnostics = _effective_diagnostics_for_record(attempt)
    return {
        "loop_id": attempt.get("loop_id"),
        "timestamp": attempt.get("timestamp"),
        "family_key": attempt.get("family_key"),
        "features": theory_features(theory),
        "theory": theory,
        "result": {
            "validated": bool(attempt.get("validated")),
            "entered_solver": bool(attempt.get("entered_solver")),
            "failed_stage": attempt.get("failed_stage"),
            "failure_tags": attempt.get("failure_tags") or [],
            "chi2": attempt.get("chi2"),
            "chi2_quality_tier": chi2_quality_tier(attempt.get("chi2")),
            "aic": attempt.get("aic"),
            "bic": attempt.get("bic"),
            "fit_reward": fit_reward,
            "reward": reward_for_attempt(attempt),
            "discovery_reward": discovery_reward_for_attempt(attempt),
            "effective_correction": effective_diagnostics,
            "top_reject_reasons": attempt.get("top_reject_reasons") or [],
        },
        "paths": {
            "solver_output_dir": attempt.get("solver_output_dir"),
            "all_samples_summary_path": attempt.get("all_samples_summary_path"),
            "accepted_samples_summary_path": attempt.get("accepted_samples_summary_path"),
            "reject_reasons_by_model_path": attempt.get("reject_reasons_by_model_path"),
        },
    }


def write_training_dataset(attempts: Iterable[Dict[str, Any]], path: Path) -> Path:
    records = [attempt_to_training_record(attempt) for attempt in attempts]
    text = "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records)
    path.write_text(text, encoding="utf-8")
    return path


def _mean(values: List[float]) -> Optional[float]:
    return sum(values) / len(values) if values else None


def summarize_policy(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_feature: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
    by_operator: Dict[str, List[float]] = defaultdict(list)
    family_rewards: Dict[str, List[float]] = defaultdict(list)
    accepted_features = Counter()
    excellent_features = Counter()
    competitive_features = Counter()

    for record in records:
        reward = float((record.get("result") or {}).get("reward") or 0.0)
        features = record.get("features") if isinstance(record.get("features"), dict) else {}
        for name, value in features.items():
            if isinstance(value, (str, bool, int)) or value is None:
                by_feature[name][str(value)].append(reward)
        for operator in features.get("operators") or []:
            by_operator[str(operator)].append(reward)
        family_key = record.get("family_key")
        if family_key:
            family_rewards[str(family_key)].append(reward)
        result = record.get("result") or {}
        if result.get("validated") and result.get("chi2_quality_tier") in {"excellent", "competitive"}:
            for name, value in features.items():
                if isinstance(value, bool) and value:
                    accepted_features[name] += 1
                    if result.get("chi2_quality_tier") == "excellent":
                        excellent_features[name] += 1
                    else:
                        competitive_features[name] += 1
                elif isinstance(value, str) and value not in {"None", ""}:
                    accepted_features[f"{name}={value}"] += 1
                    if result.get("chi2_quality_tier") == "excellent":
                        excellent_features[f"{name}={value}"] += 1
                    else:
                        competitive_features[f"{name}={value}"] += 1

    return {
        "record_count": len(records),
        "global_mean_reward": _mean([float((r.get("result") or {}).get("reward") or 0.0) for r in records]),
        "by_feature": {
            name: {
                value: {"count": len(values), "mean_reward": _mean(values)}
                for value, values in values_by_value.items()
            }
            for name, values_by_value in by_feature.items()
        },
        "by_operator": {
            op: {"count": len(values), "mean_reward": _mean(values)}
            for op, values in by_operator.items()
        },
        "by_family": {
            family: {"count": len(values), "mean_reward": _mean(values)}
            for family, values in family_rewards.items()
        },
        "accepted_feature_counts": dict(accepted_features.most_common()),
        "excellent_feature_counts": dict(excellent_features.most_common()),
        "competitive_feature_counts": dict(competitive_features.most_common()),
    }


def write_policy_summary(records: List[Dict[str, Any]], path: Path) -> Dict[str, Any]:
    summary = summarize_policy(records)
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary
