"""Build learning records from agent validation attempts."""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .effective_corrections import diagnostics_for_attempt


DATASET_FILENAME = "training_dataset.jsonl"
POLICY_SUMMARY_FILENAME = "policy_summary.json"
EXCELLENT_CHI2 = 1650.0
COMPETITIVE_CHI2 = 1700.0
WEAK_ACCEPT_CHI2 = 2000.0
NON_EH_WEAK_POSITIVE_CHI2 = 3000.0
NON_EH_POOR_ACCEPT_CHI2 = 6000.0
NON_EH_WEAK_POSITIVE_REWARD = 1.0
NON_EH_MARGINAL_ACCEPT_REWARD = -0.25
NON_EH_VERY_POOR_ACCEPT_REWARD = -1.0
NON_EH_UNACCEPTED_REWARD_CEILING = -1.5
AIC_REFERENCE_K = 3


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


def aic_equivalent_chi2(aic: Any, *, reference_k: int = AIC_REFERENCE_K) -> Optional[float]:
    """Express AIC on the existing chi-square quality scale.

    Subtracting the constant ``2 * reference_k`` preserves the exact AIC
    ordering across Lagrangians while keeping the existing 1650/1700/2000
    quality thresholds interpretable. ``reference_k`` is the nominal effective
    flat-LCDM parameter count for the current profiled likelihood.
    """

    try:
        value = float(aic)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(value):
        return None
    return value - 2.0 * float(reference_k)


def structure_score_for_attempt(attempt: Dict[str, Any]) -> Optional[float]:
    score = aic_equivalent_chi2(attempt.get("aic"))
    if score is not None:
        return score
    # Backward compatibility for current-loop memories written before AIC was
    # propagated through ValidationResult.  New runs always take the AIC path.
    try:
        value = float(attempt.get("chi2"))
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def structure_quality_tier(attempt: Dict[str, Any]) -> str:
    return chi2_quality_tier(structure_score_for_attempt(attempt))


def _proposal_group(theory: Dict[str, Any]) -> str:
    return str(theory.get("proposal_group") or "")


def _non_eh_sector_accepted_reward(chi2: Any, fit_reward: float) -> float:
    """Reward non-EH accepted attempts by fit quality, not mere survivability."""

    try:
        value = float(chi2)
    except (TypeError, ValueError):
        return fit_reward
    if value <= WEAK_ACCEPT_CHI2:
        return fit_reward
    if value <= NON_EH_WEAK_POSITIVE_CHI2:
        return NON_EH_WEAK_POSITIVE_REWARD
    if value <= NON_EH_POOR_ACCEPT_CHI2:
        return NON_EH_MARGINAL_ACCEPT_REWARD
    return NON_EH_VERY_POOR_ACCEPT_REWARD


def parameter_reward_for_attempt(attempt: Dict[str, Any]) -> float:
    """Parameter-memory reward: raw fit quality within one fixed theory."""

    fit_reward = fit_reward_for_chi2(attempt.get("chi2"))
    return fit_reward if fit_reward is not None else failure_reward_for_attempt(attempt)


def structure_reward_for_attempt(attempt: Dict[str, Any]) -> float:
    """Structure-memory reward: AIC quality plus physical diagnostics."""

    structure_score = structure_score_for_attempt(attempt)
    fit_reward = fit_reward_for_chi2(structure_score)
    if fit_reward is not None:
        theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
        if _proposal_group(theory) == "non_eh":
            return _non_eh_sector_accepted_reward(structure_score, fit_reward)
        track = attempt.get("theory_track") or _theory_track(theory)
        if track == "eh_anchored":
            diagnostics = diagnostics_for_attempt(attempt)
            status = diagnostics.get("effective_correction_status")
            if status == "active":
                return fit_reward + 0.3
            if status == "moderate":
                return fit_reward + 0.1
            return fit_reward
        # Effective-correction status is defined relative to an EH reference
        # coefficient. For non-EH / non-gravity tracks there is no such anchor,
        # so do not use active/moderate/weak/tiny labels for reward shaping.
        return fit_reward

    reward = failure_reward_for_attempt(attempt)
    theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
    if _proposal_group(theory) == "non_eh":
        return min(reward, NON_EH_UNACCEPTED_REWARD_CEILING)
    return reward


def discovery_reward_for_attempt(attempt: Dict[str, Any]) -> float:
    return structure_reward_for_attempt(attempt)


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
    return structure_reward_for_attempt(attempt)


def validation_stage_for_attempt(attempt: Dict[str, Any]) -> str:
    explicit = attempt.get("validation_stage")
    if explicit:
        return str(explicit)
    loop_id = str(attempt.get("loop_id") or "")
    if "refine" in loop_id:
        return "refine"
    if "expanded" in loop_id:
        return "expanded"
    return "initial"


def structure_trial_id_for_attempt(attempt: Dict[str, Any]) -> str:
    explicit = attempt.get("structure_trial_id")
    if explicit:
        return str(explicit)
    loop_id = str(attempt.get("loop_id") or "")
    if loop_id:
        normalized = re.sub(r"_(?:expanded_refine|expanded|refine)(?=_|$)", "", loop_id)
        return normalized
    theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
    proposal_id = theory.get("proposal_id")
    if proposal_id:
        return str(proposal_id)
    return f"{attempt.get('timestamp')}|{attempt.get('family_key')}"


def _attempt_record_key(attempt: Dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(attempt.get("loop_id") or ""),
        str(attempt.get("timestamp") or ""),
        str(attempt.get("solver_output_dir") or ""),
    )


def consolidate_structure_attempts(attempts: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return one structural learning record per initial/expanded/refine lineage."""

    grouped: Dict[tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for attempt in attempts:
        theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
        group = str(attempt.get("proposal_group") or theory.get("proposal_group") or "unknown")
        grouped[(group, structure_trial_id_for_attempt(attempt))].append(attempt)

    representatives: List[Dict[str, Any]] = []
    for (_group, trial_id), lineage in grouped.items():
        successful = [
            attempt
            for attempt in lineage
            if attempt.get("validated") and structure_score_for_attempt(attempt) is not None
        ]
        if successful:
            chosen = min(successful, key=lambda attempt: float(structure_score_for_attempt(attempt)))
        else:
            chosen = lineage[-1]
        representative = dict(chosen)
        representative["structure_trial_id"] = trial_id
        representative["structure_stage_count"] = len(lineage)
        representative["structure_validation_stages"] = dict(
            Counter(validation_stage_for_attempt(attempt) for attempt in lineage)
        )
        representative["structure_lineage_loop_ids"] = [attempt.get("loop_id") for attempt in lineage]
        representative["structure_representative_record_key"] = list(_attempt_record_key(chosen))
        representative["failure_tags"] = list(
            dict.fromkeys(tag for attempt in lineage for tag in (attempt.get("failure_tags") or []))
        )
        representative["entered_solver"] = any(bool(attempt.get("entered_solver")) for attempt in lineage)
        representatives.append(representative)
    return representatives


def _effective_diagnostics_for_record(attempt: Dict[str, Any]) -> Dict[str, Any]:
    if attempt.get("chi2") is None:
        return {}
    theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
    track = attempt.get("theory_track") or _theory_track(theory)
    if track != "eh_anchored":
        return {
            "effective_correction_status": "not_applicable_non_eh",
            "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
            "max_relative_effect_to_EH": None,
            "active_correction_terms": 0,
            "moderate_correction_terms": 0,
            "weak_correction_terms": 0,
            "tiny_correction_terms": 0,
            "correction_term_count": 0,
            "tiny_correction_fraction": None,
        }
    diagnostics = diagnostics_for_attempt(attempt)
    return {
        key: value
        for key, value in diagnostics.items()
        if key != "term_effects"
    }


def attempt_to_training_record(
    attempt: Dict[str, Any],
    *,
    is_structure_representative: bool = True,
) -> Dict[str, Any]:
    theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
    fit_reward = fit_reward_for_chi2(attempt.get("chi2"))
    structure_score = structure_score_for_attempt(attempt)
    structure_fit_reward = fit_reward_for_chi2(structure_score)
    structure_reward = structure_reward_for_attempt(attempt)
    effective_diagnostics = _effective_diagnostics_for_record(attempt)
    return {
        "loop_id": attempt.get("loop_id"),
        "timestamp": attempt.get("timestamp"),
        "family_key": attempt.get("family_key"),
        "structure_trial_id": structure_trial_id_for_attempt(attempt),
        "validation_stage": validation_stage_for_attempt(attempt),
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
            "k_params": attempt.get("k_params"),
            "k_parameter_names": attempt.get("k_parameter_names") or [],
            "fit_reward": fit_reward,
            "parameter_reward": parameter_reward_for_attempt(attempt),
            "structure_score": structure_score,
            "structure_metric": "AIC-2*k_LCDM" if attempt.get("aic") is not None else "chi2_fallback",
            "structure_reference_k": AIC_REFERENCE_K,
            "structure_quality_tier": structure_quality_tier(attempt),
            "structure_fit_reward": structure_fit_reward,
            "structure_reward": structure_reward,
            "is_structure_representative": bool(is_structure_representative),
            "reward": structure_reward,
            "discovery_reward": structure_reward,
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


def training_records_for_attempts(attempts: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    attempt_list = list(attempts)
    representative_keys = {
        tuple(attempt.get("structure_representative_record_key") or _attempt_record_key(attempt))
        for attempt in consolidate_structure_attempts(attempt_list)
    }
    return [
        attempt_to_training_record(
            attempt,
            is_structure_representative=_attempt_record_key(attempt) in representative_keys,
        )
        for attempt in attempt_list
    ]


def write_training_dataset(attempts: Iterable[Dict[str, Any]], path: Path) -> Path:
    records = training_records_for_attempts(attempts)
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

    structure_records = [
        record
        for record in records
        if (record.get("result") or {}).get("is_structure_representative", True)
    ]
    for record in structure_records:
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
        accepted_for_features = result.get("validated") and reward > 0.0
        if accepted_for_features:
            for name, value in features.items():
                if isinstance(value, bool) and value:
                    accepted_features[name] += 1
                    if result.get("structure_quality_tier") == "excellent":
                        excellent_features[name] += 1
                    elif result.get("structure_quality_tier") == "competitive":
                        competitive_features[name] += 1
                elif isinstance(value, str) and value not in {"None", ""}:
                    accepted_features[f"{name}={value}"] += 1
                    if result.get("structure_quality_tier") == "excellent":
                        excellent_features[f"{name}={value}"] += 1
                    elif result.get("structure_quality_tier") == "competitive":
                        competitive_features[f"{name}={value}"] += 1

    return {
        "record_count": len(structure_records),
        "raw_stage_record_count": len(records),
        "reward_metric": "AIC-2*k_LCDM",
        "aic_reference_k": AIC_REFERENCE_K,
        "global_mean_reward": _mean([float((r.get("result") or {}).get("reward") or 0.0) for r in structure_records]),
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
