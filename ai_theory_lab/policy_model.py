"""Lightweight learned proposal policy.

This is intentionally small and interpretable. It learns empirical rewards from
the current loop's training records instead of fine-tuning an LLM.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .dataset import theory_features


def _mean_reward(bucket: Dict[str, Any]) -> float:
    value = bucket.get("mean_reward") if isinstance(bucket, dict) else None
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _feature_delta(policy: Dict[str, Any], feature_name: str, value: Any) -> float:
    by_feature = policy.get("by_feature") if isinstance(policy.get("by_feature"), dict) else {}
    values = by_feature.get(feature_name) if isinstance(by_feature.get(feature_name), dict) else {}
    bucket = values.get(str(value)) if isinstance(values, dict) else None
    global_mean = float(policy.get("global_mean_reward") or 0.0)
    count = int((bucket or {}).get("count") or 0) if isinstance(bucket, dict) else 0
    if count <= 0:
        return 0.0
    confidence = min(1.0, count / 6.0)
    return confidence * (_mean_reward(bucket) - global_mean)


def _operator_delta(policy: Dict[str, Any], operator: str) -> float:
    by_operator = policy.get("by_operator") if isinstance(policy.get("by_operator"), dict) else {}
    bucket = by_operator.get(operator) if isinstance(by_operator, dict) else None
    if not isinstance(bucket, dict):
        return 0.0
    count = int(bucket.get("count") or 0)
    confidence = min(1.0, count / 4.0)
    global_mean = float(policy.get("global_mean_reward") or 0.0)
    return confidence * (_mean_reward(bucket) - global_mean)


def _entry_theory(entry: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "scalar_config": entry.get("scalar_config"),
        "potential_types": entry.get("potential_types"),
        "operators": entry.get("operators") or [],
    }


def score_entry_from_policy(entry: Dict[str, Any], policy: Dict[str, Any]) -> float:
    if not policy or int(policy.get("record_count") or 0) < 8:
        return 0.0

    features = theory_features(_entry_theory(entry))
    score = 0.0
    feature_names = [
        "scalar_config",
        "phi1_potential",
        "phi2_potential",
        "operator_count",
        "has_R_anchor",
        "has_scalar",
        "has_phi1",
        "has_phi2",
        "has_both_scalars",
        "is_no_scalar",
        "has_scalar_curvature",
        "has_derivative_operator",
        "has_box_operator",
        "has_high_curvature",
        "has_pure_scalar_operator",
    ]
    for name in feature_names:
        score += 0.18 * _feature_delta(policy, name, features.get(name))
    for operator in features.get("operators") or []:
        score += 0.03 * _operator_delta(policy, str(operator))

    accepted_counts = policy.get("excellent_feature_counts") or policy.get("accepted_feature_counts")
    if isinstance(accepted_counts, dict):
        accepted_total = max(1.0, sum(float(value) for key, value in accepted_counts.items() if key.startswith("scalar_config=")))
        scalar_key = f"scalar_config={features.get('scalar_config')}"
        score += 0.65 * min(1.0, float(accepted_counts.get(scalar_key, 0)) / accepted_total)
        for name in ["has_R_anchor", "has_phi1", "has_phi2", "has_both_scalars", "is_no_scalar", "has_scalar_curvature"]:
            if features.get(name):
                count = float(accepted_counts.get(name, 0))
                if count > 0:
                    score += 0.28 * min(1.0, count / accepted_total)
                elif int(policy.get("record_count") or 0) >= 20:
                    score -= 0.25
    return max(-2.0, min(2.0, score))


def explain_entry_policy_score(entry: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    features = theory_features(_entry_theory(entry))
    operators: List[str] = list(features.get("operators") or [])
    return {
        "score": score_entry_from_policy(entry, policy),
        "features": features,
        "operator_count": len(operators),
    }
