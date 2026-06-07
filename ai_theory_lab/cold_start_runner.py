"""Run a cold-start proposal loop without historical Solver memory."""

from __future__ import annotations

import argparse
import json
import math
import os
import pickle
import random
import signal
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import sympy as sp

from gr_grammar_masker_v3_2.grammar import (
    GravityMasker,
    Lambda_eft,
    Mp,
    _GREEK_COEFFS,
    f1_axion,
    f2_axion,
    m1_phi,
    m2_phi,
)
from gr_grammar_masker_v3_2.runner import _build_tensors_dict, _register_dynamic_functions_for_pickle
from gr_grammar_masker_v3_2.tensor import sqrt_mg

from .config_p import CORRECTION_SAMPLING, COEFFICIENT_PRIOR, EH_R_COEFFICIENT, PARAMETER_PRIORS
from .harness import ROOT, validate_agent_sample_pipeline
from .memory import record_attempt
from .policy_model import score_entry_from_policy
from .validation_result import ValidationResult


STRUCTURAL_EXPANSION_SKIP_TAGS = {
    "no_scalar_constraint",
    "q_initial_root_failure",
    "q_not_determined",
    "pre_sampling_timeout",
    "symbolic_timeout",
}
MAX_DUPLICATE_FAMILY_ATTEMPTS = 10
COARSE_FAMILY_SOFT_CAP = 18
HIGH_COUNT_REJECT_FRACTION = 0.45
SCALAR_FAMILY_MIN_EXPLORATION = 0.08
TOKEN_CONTEXT_CACHE_VERSION = 1
TOKEN_CONTEXT_DIMS = (2, 3, 4, 5, 6)
TOKEN_CONTEXT_MAX_DERIVATIVES = 2
DIRECT_CANDIDATE_TOP_POOL = 36
DIRECT_CANDIDATE_PAIR_POOL = 26
DIRECT_CANDIDATE_R_PAIR_POOL = 16
DIRECT_MIN_OPERATOR_TERMS = int(os.environ.get("AGENT_MIN_OPERATOR_TERMS", "2"))
DIRECT_MAX_OPERATOR_TERMS = int(os.environ.get("AGENT_MAX_OPERATOR_TERMS", "12"))
DIRECT_RANDOM_CANDIDATES_PER_POTENTIAL = int(os.environ.get("AGENT_RANDOM_CANDIDATES_PER_POTENTIAL", "28"))


@contextmanager
def _wall_timeout(seconds: int, label: str):
    if seconds <= 0:
        yield
        return

    def _raise_timeout(signum, frame):
        raise TimeoutError(f"{label} exceeded {seconds}s wall time")

    old_handler = signal.getsignal(signal.SIGALRM)
    old_timer = signal.setitimer(signal.ITIMER_REAL, float(seconds))
    signal.signal(signal.SIGALRM, _raise_timeout)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, old_timer[0], old_timer[1])
        signal.signal(signal.SIGALRM, old_handler)


def _operator_labels(lagrangian: Dict[str, Any]) -> List[str]:
    labels: List[str] = []
    for term in lagrangian.get("terms", []):
        if not term.get("fixed"):
            labels.append(str(term.get("candidate")))
    return labels


def _operator_specs(lagrangian: Dict[str, Any]) -> List[Dict[str, str]]:
    specs: List[Dict[str, str]] = []
    for term in lagrangian.get("terms", []):
        if term.get("fixed"):
            continue
        candidate = str(term.get("candidate"))
        coeff_symbol = str(term.get("coeff_symbol"))
        if not candidate or not coeff_symbol or coeff_symbol == "1":
            continue
        specs.append({"candidate": candidate, "coefficient": coeff_symbol})
    return specs


def _potential_types(lagrangian: Dict[str, Any]) -> Dict[str, Any]:
    potentials = dict(lagrangian.get("potential_types") or {})
    potentials.setdefault("phi1", None)
    potentials.setdefault("phi2", None)
    return potentials


def _load_summary(memory_dir: Path) -> Dict[str, Any]:
    path = memory_dir / "feedback_summary.json"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _attempted_families(summary: Dict[str, Any]) -> set[str]:
    return {str(row.get("family_key")) for row in summary.get("by_family") or []}


def _family_attempt_counts(summary: Dict[str, Any]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in summary.get("by_family") or []:
        family_key = row.get("family_key")
        if family_key is None:
            continue
        try:
            counts[str(family_key)] = int(row.get("attempts") or 0)
        except (TypeError, ValueError):
            counts[str(family_key)] = 0
    return counts


def _under_duplicate_limit(entry: Dict[str, Any], summary: Dict[str, Any]) -> bool:
    counts = _family_attempt_counts(summary)
    return counts.get(_family_key(entry), 0) < MAX_DUPLICATE_FAMILY_ATTEMPTS


def _family_key(entry: Dict[str, Any]) -> str:
    operators = "+".join(entry["operators"]) if entry["operators"] else "none"
    return (
        f"scalar={entry['scalar_config']}|"
        f"potential={entry['potential_types']}|"
        f"operators={operators}"
    )


def _coarse_family_key(entry: Dict[str, Any]) -> str:
    operators = entry["operators"]
    joined = " ".join(operators)
    potentials = entry["potential_types"] if isinstance(entry["potential_types"], dict) else {}
    buckets: List[str] = []
    if "R" in operators:
        buckets.append("R_anchor")
    if "∇" in joined or "nabla" in joined:
        buckets.append("derivative")
    if any(("R · R" in op) or ("R^{ab}" in op) or ("R_{ab}" in op) for op in operators):
        buckets.append("high_curvature")
    if any(("φ" in op) and ("R" in op) for op in operators):
        buckets.append("scalar_curvature")
    if not buckets:
        buckets.append("plain")
    return (
        f"scalar={entry['scalar_config']}|"
        f"phi1_potential={potentials.get('phi1')}|"
        f"phi2_potential={potentials.get('phi2')}|"
        f"operator_bucket={'+'.join(sorted(buckets))}"
    )


def _coarse_family_attempt_counts(summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    counts: Dict[str, Dict[str, Any]] = {}
    for row in summary.get("by_coarse_family") or []:
        key = row.get("coarse_family_key")
        if key is not None:
            counts[str(key)] = row
    return counts


def _theory_operator_labels(theory: Dict[str, Any]) -> List[str]:
    operators = theory.get("operators")
    if not isinstance(operators, list):
        return []
    labels: List[str] = []
    for operator in operators:
        if isinstance(operator, dict):
            labels.append(str(operator.get("candidate") or operator.get("label") or operator))
        else:
            labels.append(str(operator))
    return labels


def _operator_is_scalar_curvature_coupling(label: str) -> bool:
    return ("R" in label) and any(token in label for token in ("φ", "phi", "\\phi", "∇", "nabla"))


def _operator_is_scalar_derivative_coupling(label: str) -> bool:
    return any(token in label for token in ("φ", "phi", "\\phi")) and any(token in label for token in ("∇", "nabla"))


def _operator_is_scalar_derivative_curvature_coupling(label: str) -> bool:
    return "R" in label and _operator_is_scalar_derivative_coupling(label)


def _successful_attempts(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    attempts = []
    for attempt in summary.get("top_chi2_attempts") or []:
        try:
            chi2 = float(attempt.get("chi2"))
        except (TypeError, ValueError):
            continue
        if chi2 < 2000.0:
            attempts.append(attempt)
    return attempts


def _scalar_family_metrics(summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    agent_loop = summary.get("agent_loop") if isinstance(summary.get("agent_loop"), dict) else {}
    structure_prior = agent_loop.get("structure_prior") if isinstance(agent_loop.get("structure_prior"), dict) else {}
    scalar_learning = structure_prior.get("scalar_family_learning") if isinstance(structure_prior.get("scalar_family_learning"), dict) else {}
    metrics = scalar_learning.get("metrics") if isinstance(scalar_learning.get("metrics"), dict) else {}
    return {
        str(key): value
        for key, value in metrics.items()
        if isinstance(value, dict)
    }


def _float_metric(row: Dict[str, Any], key: str) -> Optional[float]:
    try:
        value = row.get(key)
        if value is None:
            return None
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _score_scalar_family_from_metrics(scalar_config: str, summary: Dict[str, Any]) -> float:
    """Apply the same soft evidence rules to every scalar family."""

    metrics = _scalar_family_metrics(summary).get(scalar_config)
    if not metrics:
        return 0.0
    try:
        attempts = int(metrics.get("attempts") or 0)
    except (TypeError, ValueError):
        attempts = 0
    if attempts < 3:
        return 0.0

    score = 0.0
    best_chi2 = _float_metric(metrics, "best_chi2")
    accepted_rate = _float_metric(metrics, "accepted_sample_rate")
    validated_rate = _float_metric(metrics, "validated_attempt_rate")
    q_root_rate = _float_metric(metrics, "q_initial_root_failure_rate")
    q_not_rate = _float_metric(metrics, "q_not_determined_attempt_rate")
    no_scalar_rate = _float_metric(metrics, "no_scalar_constraint_rate")
    drift_rate = _float_metric(metrics, "constraint_drift_rate")
    integration_rate = _float_metric(metrics, "integration_failure_rate")

    if best_chi2 is not None:
        if best_chi2 <= 1650.0:
            score += 1.4
        elif best_chi2 <= 1700.0:
            score += 1.0
        elif best_chi2 <= 2000.0:
            score += 0.55
        else:
            score -= min(0.8, (best_chi2 - 2000.0) / 5000.0)
    if accepted_rate is not None:
        if accepted_rate >= 0.25:
            score += 0.25
        elif accepted_rate <= 0.02:
            score -= 0.25
    if validated_rate is not None and validated_rate >= 0.4:
        score += 0.15
    for rate in (q_root_rate, q_not_rate, no_scalar_rate, drift_rate, integration_rate):
        if rate is None:
            continue
        if rate >= 0.45:
            score -= 0.35
        elif rate >= 0.20:
            score -= 0.15
    return score


def _underexplored_scalar_config(catalog: Sequence[Dict[str, Any]], summary: Dict[str, Any], rng: random.Random) -> Optional[str]:
    available = sorted({str(entry.get("scalar_config")) for entry in catalog if entry.get("operators")})
    if not available:
        return None
    counts = summary.get("scalar_config_counts") if isinstance(summary.get("scalar_config_counts"), dict) else {}
    total = sum(int(value or 0) for value in counts.values()) if counts else 0
    if total <= 0:
        return rng.choice(available)
    target_count = max(1.0, SCALAR_FAMILY_MIN_EXPLORATION * float(total))
    under = [
        scalar
        for scalar in available
        if float(counts.get(scalar, 0) or 0) < target_count
    ]
    if under:
        return rng.choice(under)
    return None


def _entry_score(entry: Dict[str, Any], summary: Dict[str, Any], rng: random.Random) -> float:
    """Rank legal catalog entries using current-loop facts only."""

    score = 0.0
    operators = entry["operators"]
    scalar_config = entry["scalar_config"]
    failed_stage_counts = summary.get("failed_stage_counts") or {}
    failure_tags = summary.get("failure_tag_counts") or {}

    # These are cold-start priors over grammar simplicity, not Solver-history priors.
    score -= 0.30 * len(operators)
    if "R" in operators:
        score += 1.0
    if scalar_config in {"phi1_only", "phi2_only"}:
        score += 0.6
    if scalar_config == "both":
        score += 0.2
    if scalar_config == "none":
        score -= 0.5

    # Current-loop feedback facts can influence future choice, but no historical data is read.
    if failed_stage_counts.get("Builder", 0) >= 2:
        score -= 0.25 * max(0, len(operators) - 1)
    if failure_tags.get("no_scalar_constraint", 0) >= 2 and scalar_config == "none":
        score -= 1.0
    if failure_tags.get("h_absurdly_large", 0) >= 2 and len(operators) > 1:
        score -= 0.3
    q_not_count = int(failure_tags.get("q_not_determined") or 0)
    if q_not_count >= 3:
        if any(_operator_is_scalar_derivative_coupling(label) for label in operators):
            score -= 0.35
        if any(_operator_is_scalar_derivative_curvature_coupling(label) for label in operators):
            score -= 0.45
        if any("∇^{a}∇_{a}φ" in label or "nabla^2 phi" in label for label in operators):
            score -= 0.35
        if len(operators) > 2:
            score -= 0.15 * (len(operators) - 2)

    successes = _successful_attempts(summary)
    if successes:
        success_scalar_configs = {
            (attempt.get("theory") or {}).get("scalar_config")
            for attempt in successes
        }
        success_operator_sets = [
            set(_theory_operator_labels(attempt.get("theory") or {}))
            for attempt in successes
        ]
        if scalar_config in success_scalar_configs:
            score += 0.8
        if "R" in operators and any("R" in op_set for op_set in success_operator_sets):
            score += 0.5
        if len(operators) <= 2:
            score += 0.25
        if any(_operator_is_scalar_curvature_coupling(label) for label in operators):
            score += 0.6
        overlap = max((len(set(operators) & op_set) for op_set in success_operator_sets), default=0)
        score += 0.25 * overlap

    if _family_key(entry) in _attempted_families(summary):
        score -= 1.5
    score += score_entry_from_policy(entry, summary.get("policy") or {})
    agent_loop = summary.get("agent_loop") if isinstance(summary.get("agent_loop"), dict) else {}
    structure_prior = agent_loop.get("structure_prior") if isinstance(agent_loop.get("structure_prior"), dict) else {}
    preferred_scalars = structure_prior.get("preferred_scalar_configs") if isinstance(structure_prior.get("preferred_scalar_configs"), dict) else {}
    preferred_ops = structure_prior.get("preferred_operators") if isinstance(structure_prior.get("preferred_operators"), dict) else {}
    preferred_features = structure_prior.get("preferred_features") if isinstance(structure_prior.get("preferred_features"), dict) else {}
    avoid_scalars = structure_prior.get("avoid_scalar_configs") if isinstance(structure_prior.get("avoid_scalar_configs"), dict) else {}
    avoid_features = structure_prior.get("avoid_features") if isinstance(structure_prior.get("avoid_features"), dict) else {}
    avoid_ops = structure_prior.get("avoid_operators") if isinstance(structure_prior.get("avoid_operators"), dict) else {}
    if preferred_scalars:
        score += 0.18 * float(preferred_scalars.get(scalar_config, 0))
    for operator in operators:
        score += 0.08 * float(preferred_ops.get(operator, 0))
        score -= 0.10 * min(8.0, float(avoid_ops.get(operator, 0)))
    if "R" in operators:
        score += 0.10 * float(preferred_features.get("has_R_anchor", 0))
    scalar_feature_key = f"scalar_config={scalar_config}"
    if "R" in operators:
        score += 0.18 * float(preferred_features.get(scalar_feature_key, 0))
    score -= 0.10 * min(8.0, float(avoid_scalars.get(scalar_config, 0)))
    if scalar_config in {"phi1_only", "both"}:
        score -= 0.08 * float(avoid_features.get("has_phi1_with_q_failure", 0))
    if scalar_config in {"phi2_only", "both"}:
        score -= 0.08 * float(avoid_features.get("has_phi2_with_q_failure", 0))
    score += _score_scalar_family_from_metrics(scalar_config, summary)
    if "∇" in " ".join(operators):
        score -= 0.06 * float(avoid_features.get("derivative_with_numerical_failure", 0))
    if any(_operator_is_scalar_derivative_coupling(label) for label in operators):
        score -= 0.06 * float(avoid_features.get("scalar_derivative_with_q_not_determined", 0))
    if any(_operator_is_scalar_derivative_curvature_coupling(label) for label in operators):
        score -= 0.08 * float(avoid_features.get("scalar_derivative_curvature_with_q_not_determined", 0))

    coarse_row = _coarse_family_attempt_counts(summary).get(_coarse_family_key(entry))
    if coarse_row:
        attempts = int(coarse_row.get("attempts") or 0)
        validated = int(coarse_row.get("validated") or 0)
        tag_counts = coarse_row.get("failure_tag_counts") if isinstance(coarse_row.get("failure_tag_counts"), dict) else {}
        if attempts >= COARSE_FAMILY_SOFT_CAP and validated == 0:
            score -= 1.2
        if scalar_config == "none" and int(tag_counts.get("no_scalar_constraint") or 0) >= 3:
            score -= 0.8
        if (
            int(tag_counts.get("q_initial_root_failure") or 0) + int(tag_counts.get("q_not_determined") or 0)
        ) >= 3:
            score -= 0.8
    score += rng.uniform(-0.15, 0.15)
    return score


def _choose_entry(catalog: Sequence[Dict[str, Any]], summary: Dict[str, Any], rng: random.Random) -> Dict[str, Any]:
    # Keep some explicit exploration so the loop does not collapse to one family.
    if summary.get("total_attempts", 0) < 5:
        scalar_order = ["phi1_only", "phi1_only", "phi2_only", "both", "none"]
        target = scalar_order[int(summary.get("total_attempts", 0))]
        candidates = [e for e in catalog if e["scalar_config"] == target and e["operators"]]
    elif rng.random() < SCALAR_FAMILY_MIN_EXPLORATION:
        target = _underexplored_scalar_config(catalog, summary, rng)
        candidates = [e for e in catalog if e["scalar_config"] == target and e["operators"]] if target else [e for e in catalog if e["operators"]]
    elif rng.random() < (0.12 if int(summary.get("total_attempts", 0) or 0) >= 30 else 0.20):
        candidates = [e for e in catalog if e["operators"]]
    else:
        candidates = list(catalog)
    if not candidates:
        candidates = list(catalog)
    under_limit = [entry for entry in candidates if _under_duplicate_limit(entry, summary)]
    if under_limit:
        candidates = under_limit
    return max(candidates, key=lambda entry: _entry_score(entry, summary, rng))


def _entry_from_lagrangian(lagrangian: Dict[str, Any], n_terms: int, local_number: int = 1) -> Dict[str, Any]:
    specs = _operator_specs(lagrangian)
    return {
        "n_terms": int(n_terms),
        "local_number": int(local_number),
        "scalar_config": lagrangian.get("scalar_config"),
        "potential_types": _potential_types(lagrangian),
        "operators": [spec["candidate"] for spec in specs],
        "operator_specs": specs,
        "coefficient_symbols": [spec["coefficient"] for spec in specs],
        "general": lagrangian.get("general"),
        "lagrangian": lagrangian,
    }


def _candidate_label(candidate: Any) -> str:
    return str(getattr(candidate, "contraction_label", "") or getattr(candidate, "general_label", ""))


def _candidate_sort_key(candidate: Any) -> tuple:
    label = _candidate_label(candidate)
    sector = str(getattr(candidate, "sector", ""))
    mass_dim = int(getattr(candidate, "mass_dim", 99))
    has_derivative = "∇" in label
    has_phi = "φ" in label
    has_curvature = "R" in label
    high_curvature = label.count("R") >= 2 or "R^{ab}" in label or "R_{ab}" in label
    exact_r = label == "R"
    sector_rank = {"gravity": 0, "non-minimal": 1, "scalar": 2}.get(sector, 3)
    return (
        0 if exact_r else 1,
        sector_rank,
        mass_dim,
        1 if has_derivative else 0,
        1 if high_curvature else 0,
        0 if has_curvature else 1,
        1 if has_phi else 0,
        label,
    )


def _candidate_allowed_for_scalar_config(candidate: Any, scalar_config: str) -> bool:
    involves_phi1 = GravityMasker._involves_phi1(candidate)
    involves_phi2 = GravityMasker._involves_phi2(candidate)
    if scalar_config == "none":
        return not involves_phi1 and not involves_phi2
    if scalar_config == "phi1_only":
        return not involves_phi2
    if scalar_config == "phi2_only":
        return not involves_phi1
    if scalar_config == "both":
        return True
    return False


def _potential_options_for_scalar_config(scalar_config: str) -> List[Dict[str, Any]]:
    if scalar_config == "none":
        return [{"phi1": None, "phi2": None}]
    if scalar_config == "phi1_only":
        return [{"phi1": pot1, "phi2": None} for pot1 in ("quadratic", "axion")]
    if scalar_config == "phi2_only":
        return [{"phi1": None, "phi2": pot2} for pot2 in ("quadratic", "axion")]
    if scalar_config == "both":
        return [
            {"phi1": pot1, "phi2": pot2}
            for pot1 in ("quadratic", "axion")
            for pot2 in ("quadratic", "axion")
        ]
    raise ValueError(f"Unknown scalar_config: {scalar_config}")


def _coefficient_symbol_for_index(index: int) -> sp.Symbol:
    if index < len(_GREEK_COEFFS):
        return _GREEK_COEFFS[index]
    return sp.Symbol(f"c_{{{index + 1}}}")


def _make_direct_potential(tensors: Dict[str, Any], which: int, pot_type: str) -> tuple[str, Any]:
    if which == 1:
        m, f, phi = m1_phi, f1_axion, tensors["phi1"]
        m_str, f_str, phi_str = "m_1", "f_1", "φ1"
    else:
        m, f, phi = m2_phi, f2_axion, tensors["phi2"]
        m_str, f_str, phi_str = "m_2", "f_2", "φ2"

    if pot_type == "quadratic":
        return f"-½ {m_str}² {phi_str}²", sp.Rational(-1, 2) * m**2 * phi**2
    if pot_type == "axion":
        return f"-{m_str}² {f_str}² (1 - cos({phi_str}/{f_str}))", -m**2 * f**2 * (1 - sp.cos(phi / f))
    raise ValueError(f"Invalid potential type for phi{which}: {pot_type!r}")


def _direct_fixed_matter_terms(
    tensors: Dict[str, Any],
    scalar_config: str,
    potential_types: Dict[str, Any],
) -> tuple[List[str], Any, List[Dict[str, Any]]]:
    include_phi1 = scalar_config in {"phi1_only", "both"}
    include_phi2 = scalar_config in {"phi2_only", "both"}
    t_coord = tensors["coords"][0]
    n_func = sp.Function("N", positive=True)(t_coord)
    general_parts: List[str] = []
    substituted = sp.Integer(0)
    term_info: List[Dict[str, Any]] = []

    if include_phi1:
        phi1_dot = sp.Derivative(tensors["phi1"], t_coord)
        kinetic_general = "-½ g^{μν} ∇_μφ1 ∇_νφ1"
        kinetic_value = sp.Rational(1, 2) * phi1_dot**2 / n_func**2
        pot_general, pot_value = _make_direct_potential(tensors, 1, str(potential_types.get("phi1")))
        general_parts.extend([kinetic_general, pot_general])
        substituted += kinetic_value + pot_value
        term_info.append({
            "coeff_symbol": "1",
            "coeff_token": "COEFF_FIXED_1",
            "candidate": kinetic_general,
            "mass_dim": 4,
            "lambda_power": 0,
            "fixed": True,
            "sector": "matter",
        })
        term_info.append({
            "coeff_symbol": "1",
            "coeff_token": "COEFF_FIXED_1",
            "candidate": pot_general,
            "mass_dim": 4,
            "lambda_power": 0,
            "fixed": True,
            "sector": "matter",
            "potential_type": potential_types.get("phi1"),
        })

    if include_phi2:
        phi2_dot = sp.Derivative(tensors["phi2"], t_coord)
        kinetic_general = "-½ g^{μν} ∇_μφ2 ∇_νφ2"
        kinetic_value = sp.Rational(1, 2) * phi2_dot**2 / n_func**2
        pot_general, pot_value = _make_direct_potential(tensors, 2, str(potential_types.get("phi2")))
        general_parts.extend([kinetic_general, pot_general])
        substituted += kinetic_value + pot_value
        term_info.append({
            "coeff_symbol": "1",
            "coeff_token": "COEFF_FIXED_1",
            "candidate": kinetic_general,
            "mass_dim": 4,
            "lambda_power": 0,
            "fixed": True,
            "sector": "matter",
        })
        term_info.append({
            "coeff_symbol": "1",
            "coeff_token": "COEFF_FIXED_1",
            "candidate": pot_general,
            "mass_dim": 4,
            "lambda_power": 0,
            "fixed": True,
            "sector": "matter",
            "potential_type": potential_types.get("phi2"),
        })

    return general_parts, substituted, term_info


def _compile_direct_lagrangian(
    tensors: Dict[str, Any],
    scalar_config: str,
    potential_types: Dict[str, Any],
    candidates: Sequence[Any],
) -> Dict[str, Any]:
    general_grav_parts: List[str] = []
    general_nm_parts: List[str] = []
    general_sc_parts: List[str] = []
    substituted_grav = sp.Integer(0)
    substituted_nm = sp.Integer(0)
    substituted_sc = sp.Integer(0)
    term_info: List[Dict[str, Any]] = []

    for index, candidate in enumerate(candidates):
        coeff = _coefficient_symbol_for_index(index)
        sector = str(getattr(candidate, "sector", "gravity"))
        mass_dim = int(getattr(candidate, "mass_dim"))
        lam_power = GravityMasker._pad_lambda(mass_dim, sector)
        lam_factor = Lambda_eft**lam_power if lam_power != 0 else sp.Integer(1)
        lam_str = f" Λ^{{{lam_power}}}" if lam_power != 0 else ""
        general_label = str(getattr(candidate, "general_label", _candidate_label(candidate)))
        part = f"{coeff}{lam_str} · {general_label}"
        symbolic_value = getattr(candidate, "symbolic_value")

        if sector == "gravity":
            general_grav_parts.append(part)
            substituted_grav += coeff * lam_factor * symbolic_value
        elif sector == "non-minimal":
            general_nm_parts.append(part)
            substituted_nm += coeff * lam_factor * symbolic_value
        elif sector == "scalar":
            general_sc_parts.append(part)
            substituted_sc += coeff * lam_factor * symbolic_value
        else:
            raise ValueError(f"Unknown candidate sector: {sector}")

        term_info.append({
            "coeff_symbol": str(coeff),
            "coeff_token": f"COEFF_{index}",
            "candidate": _candidate_label(candidate),
            "mass_dim": mass_dim,
            "lambda_power": lam_power,
            "sector": sector,
        })

    general_phi_parts, substituted_phi, fixed_terms = _direct_fixed_matter_terms(
        tensors,
        scalar_config,
        potential_types,
    )
    term_info.extend(fixed_terms)

    inner_parts: List[str] = []
    mp2_parts = general_grav_parts + general_nm_parts
    if mp2_parts:
        inner_parts.append("M_p² ( " + "  +  ".join(mp2_parts) + " )")
    if general_sc_parts:
        inner_parts.append("  +  ".join(general_sc_parts))
    if general_phi_parts:
        inner_parts.append("  +  ".join(general_phi_parts))
    general_str = "√(-g) [ " + "  +  ".join(inner_parts) + " ]"

    substituted_full = sqrt_mg * (
        Mp**2 * (substituted_grav + substituted_nm) + substituted_sc + substituted_phi
    )
    return {
        "n_terms": len(term_info),
        "general": general_str,
        "substituted": sp.simplify(substituted_full),
        "terms": term_info,
        "scalar_config": scalar_config,
        "potential_types": {"phi1": potential_types.get("phi1"), "phi2": potential_types.get("phi2")},
    }


def _direct_entry(
    *,
    tensors: Dict[str, Any],
    scalar_config: str,
    potential_types: Dict[str, Any],
    candidates: Sequence[Any],
    local_number: int,
) -> Dict[str, Any]:
    ordered = tuple(sorted(candidates, key=_candidate_sort_key))
    operator_specs = [
        {"candidate": _candidate_label(candidate), "coefficient": str(_coefficient_symbol_for_index(index))}
        for index, candidate in enumerate(ordered)
    ]
    lagrangian = _compile_direct_lagrangian(tensors, scalar_config, potential_types, ordered)
    return {
        "n_terms": int(lagrangian["n_terms"]),
        "local_number": int(local_number),
        "scalar_config": scalar_config,
        "potential_types": {"phi1": potential_types.get("phi1"), "phi2": potential_types.get("phi2")},
        "operators": [spec["candidate"] for spec in operator_specs],
        "operator_specs": operator_specs,
        "coefficient_symbols": [spec["coefficient"] for spec in operator_specs],
        "general": lagrangian.get("general"),
        "lagrangian": lagrangian,
        "construction_mode": "direct_candidate_combination",
    }


def _entry_skeleton(
    *,
    scalar_config: str,
    potential_types: Dict[str, Any],
    candidates: Sequence[Any],
    local_number: int,
) -> Dict[str, Any]:
    ordered = tuple(sorted(candidates, key=_candidate_sort_key))
    operator_specs = [
        {"candidate": _candidate_label(candidate), "coefficient": str(_coefficient_symbol_for_index(index))}
        for index, candidate in enumerate(ordered)
    ]
    n_fixed = 2 * int(scalar_config in {"phi1_only", "phi2_only"}) + 4 * int(scalar_config == "both")
    return {
        "n_terms": len(ordered) + n_fixed,
        "local_number": int(local_number),
        "scalar_config": scalar_config,
        "potential_types": {"phi1": potential_types.get("phi1"), "phi2": potential_types.get("phi2")},
        "operators": [spec["candidate"] for spec in operator_specs],
        "operator_specs": operator_specs,
        "coefficient_symbols": [spec["coefficient"] for spec in operator_specs],
        "_candidate_objects": ordered,
        "construction_mode": "direct_candidate_combination",
    }


def _sample_operator_count(rng: random.Random) -> int:
    low = max(1, int(DIRECT_MIN_OPERATOR_TERMS))
    high = max(low, int(DIRECT_MAX_OPERATOR_TERMS))
    return rng.randint(low, high)


def _direct_candidate_catalog(
    context: Dict[str, Any],
    *,
    rng: Optional[random.Random] = None,
    target_operator_count: Optional[int] = None,
) -> List[Dict[str, Any]]:
    candidates = sorted(getattr(context["masker"], "all_candidates", []) or [], key=_candidate_sort_key)
    catalog: List[Dict[str, Any]] = []
    seen: set[tuple] = set()
    local_number = 0
    local_rng = rng or random.Random(0)

    def add_entry(scalar_config: str, potential_types: Dict[str, Any], chosen: Sequence[Any]) -> None:
        nonlocal local_number
        labels = tuple(_candidate_label(candidate) for candidate in sorted(chosen, key=_candidate_sort_key))
        if not labels:
            return
        key = (scalar_config, potential_types.get("phi1"), potential_types.get("phi2"), labels)
        if key in seen:
            return
        seen.add(key)
        local_number += 1
        catalog.append(
            _entry_skeleton(
                scalar_config=scalar_config,
                potential_types=potential_types,
                candidates=chosen,
                local_number=local_number,
            )
        )

    for scalar_config in ("none", "phi1_only", "phi2_only", "both"):
        allowed = [candidate for candidate in candidates if _candidate_allowed_for_scalar_config(candidate, scalar_config)]
        if not allowed:
            continue
        r_anchor = next((_candidate for _candidate in allowed if _candidate_label(_candidate) == "R"), None)
        non_r = [_candidate for _candidate in allowed if _candidate is not r_anchor]
        sample_count = max(1, int(DIRECT_RANDOM_CANDIDATES_PER_POTENTIAL))

        for potential_types in _potential_options_for_scalar_config(scalar_config):
            for _ in range(sample_count):
                desired = int(target_operator_count) if target_operator_count is not None else _sample_operator_count(local_rng)
                desired = max(1, min(desired, len(allowed)))
                chosen: List[Any] = []
                if r_anchor is not None and desired >= 2 and local_rng.random() < 0.85:
                    chosen.append(r_anchor)
                    chosen.extend(local_rng.sample(non_r, min(desired - 1, len(non_r))))
                else:
                    chosen.extend(local_rng.sample(allowed, desired))
                add_entry(scalar_config, potential_types, tuple(chosen))

    return catalog


def _token_context_cache_path() -> Path:
    return ROOT / "ai_theory_lab" / "cache" / (
        f"token_context_v{TOKEN_CONTEXT_CACHE_VERSION}_"
        f"deriv{TOKEN_CONTEXT_MAX_DERIVATIVES}_"
        f"dims{'_'.join(str(dim) for dim in TOKEN_CONTEXT_DIMS)}.pkl"
    )


def _load_token_level_context_cache() -> Optional[Dict[str, Any]]:
    path = _token_context_cache_path()
    if not path.exists():
        return None
    try:
        import sympy as sp
        import sys

        main_module = sys.modules.get("__main__")
        if main_module is not None:
            for name in ("phi1", "phi2"):
                if not hasattr(main_module, name):
                    setattr(main_module, name, sp.Function(name))
        with path.open("rb") as f:
            payload = pickle.load(f)
    except Exception as exc:
        print(f"[TOKEN-CACHE] Could not load {path}: {type(exc).__name__}: {exc}; rebuilding.", flush=True)
        return None
    if not isinstance(payload, dict):
        return None
    if payload.get("version") != TOKEN_CONTEXT_CACHE_VERSION:
        return None
    if tuple(payload.get("dims") or ()) != TOKEN_CONTEXT_DIMS:
        return None
    if int(payload.get("max_derivatives") or -1) != TOKEN_CONTEXT_MAX_DERIVATIVES:
        return None
    context = payload.get("context")
    if not isinstance(context, dict) or "masker" not in context or "tensors" not in context:
        return None
    candidate_count = len(getattr(context["masker"], "all_candidates", []) or [])
    if candidate_count <= 0:
        return None
    print(f"[TOKEN-CACHE] Loaded {candidate_count} candidates from {path}", flush=True)
    return context


def _save_token_level_context_cache(context: Dict[str, Any]) -> None:
    path = _token_context_cache_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": TOKEN_CONTEXT_CACHE_VERSION,
        "dims": TOKEN_CONTEXT_DIMS,
        "max_derivatives": TOKEN_CONTEXT_MAX_DERIVATIVES,
        "context": context,
    }
    try:
        _register_dynamic_functions_for_pickle(context.get("tensors", {}))
        for candidate in getattr(context["masker"], "all_candidates", []) or []:
            _register_dynamic_functions_for_pickle(getattr(candidate, "symbolic_value", None))
            _register_dynamic_functions_for_pickle(getattr(candidate, "general_label", None))
        with path.open("wb") as f:
            pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as exc:
        print(f"[TOKEN-CACHE] Could not save {path}: {type(exc).__name__}: {exc}", flush=True)
        return
    candidate_count = len(getattr(context["masker"], "all_candidates", []) or [])
    print(f"[TOKEN-CACHE] Saved {candidate_count} candidates to {path}", flush=True)


def _build_token_level_context(timeout_seconds: int, use_cache: bool = True) -> Dict[str, Any]:
    if use_cache:
        cached = _load_token_level_context_cache()
        if cached is not None:
            return cached
    with _wall_timeout(timeout_seconds, "Token-level Grammar Masker generation"):
        tensors = _build_tensors_dict()
        masker = GravityMasker(max_derivatives=TOKEN_CONTEXT_MAX_DERIVATIVES)
        masker.collect_candidates(tensors, dims=TOKEN_CONTEXT_DIMS)
    context = {"tensors": tensors, "masker": masker}
    if use_cache:
        _save_token_level_context_cache(context)
    return context


def _write_token_level_context_summary(context: Dict[str, Any], path: Path) -> None:
    masker = context["masker"]
    rows = []
    for candidate in getattr(masker, "all_candidates", []):
        rows.append(
            {
                "candidate": str(candidate.contraction_label),
                "general_label": str(candidate.general_label),
                "mass_dim": int(candidate.mass_dim),
                "sector": str(candidate.sector),
            }
        )
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")


def _generate_token_level_entry(
    context: Dict[str, Any],
    summary: Dict[str, Any],
    rng: random.Random,
    seed: int,
) -> Dict[str, Any]:
    tensors = context["tensors"]
    target_operator_count = _sample_operator_count(random.Random(seed + 8191))
    skeletons = _direct_candidate_catalog(
        context,
        rng=random.Random(seed + 131071),
        target_operator_count=target_operator_count,
    )
    if not skeletons:
        raise RuntimeError("Token-level Grammar Masker candidate pool is empty")

    entries = [entry for entry in skeletons if _under_duplicate_limit(entry, summary)]
    if not entries:
        entries = skeletons

    # The agent chooses from legal Grammar Masker candidates directly. The seed
    # controls policy exploration; it no longer samples finished Lagrangians
    # from Grammar Masker's random batch generator.
    choice_rng = random.Random(seed + 104729)
    selected = _choose_entry(entries, summary, choice_rng)
    candidate_objects = selected.pop("_candidate_objects", None)
    if not candidate_objects:
        raise RuntimeError("Direct candidate proposal was missing candidate objects")

    compiled = _direct_entry(
        tensors=tensors,
        scalar_config=str(selected["scalar_config"]),
        potential_types=dict(selected["potential_types"]),
        candidates=candidate_objects,
        local_number=int(selected["local_number"]),
    )
    compiled["proposal_mode"] = "direct_candidate_policy"
    compiled["target_operator_count"] = target_operator_count
    return compiled


def _log_uniform(rng: random.Random, low: float, high: float) -> float:
    return 10 ** rng.uniform(math.log10(low), math.log10(high))


def _parameter_priors(summary: Dict[str, Any]) -> Dict[str, Any]:
    agent_loop = summary.get("agent_loop") if isinstance(summary.get("agent_loop"), dict) else {}
    prior = agent_loop.get("parameter_prior") if isinstance(agent_loop.get("parameter_prior"), dict) else {}
    return prior if isinstance(prior, dict) else {}


def _sample_prior_value(
    rng: random.Random,
    priors: Dict[str, Any],
    key: str,
    *,
    default_low: float,
    default_high: float,
    default_log: bool = False,
) -> float:
    spec = (priors.get("parameters") or {}).get(key) if isinstance(priors.get("parameters"), dict) else None
    if isinstance(spec, dict) and spec.get("count", 0) >= 3:
        low = float(spec.get("low"))
        high = float(spec.get("high"))
        if spec.get("log10"):
            return 10 ** rng.uniform(low, high)
        return rng.uniform(low, high)
    if default_log:
        return _log_uniform(rng, default_low, default_high)
    return rng.uniform(default_low, default_high)


def _coefficient_value(rng: random.Random, priors: Dict[str, Any]) -> float:
    coeff_prior = priors.get("coefficient_log10_abs") if isinstance(priors.get("coefficient_log10_abs"), dict) else None
    if coeff_prior and coeff_prior.get("count", 0) >= 3:
        mag = 10 ** rng.uniform(float(coeff_prior["low"]), float(coeff_prior["high"]))
        sign_weights = priors.get("coefficient_sign_weights") if isinstance(priors.get("coefficient_sign_weights"), dict) else {}
        positive_weight = float(sign_weights.get("positive", 0.5))
        sign = 1.0 if rng.random() < positive_weight else -1.0
        return sign * mag
    sign = rng.choice(COEFFICIENT_PRIOR["signs"])
    mag = 10 ** rng.uniform(float(COEFFICIENT_PRIOR["log10_abs_low"]), float(COEFFICIENT_PRIOR["log10_abs_high"]))
    return sign * mag


def _term_by_coefficient(entry: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    terms = ((entry.get("lagrangian") or {}).get("terms") or [])
    return {str(term.get("coeff_symbol")): term for term in terms if term.get("coeff_symbol")}


def _is_eh_operator(term: Dict[str, Any]) -> bool:
    return (
        str(term.get("candidate") or "").strip() == "R"
        and str(term.get("sector") or "") in {"gravity", "non-minimal"}
        and int(term.get("lambda_power", 0) or 0) == 0
        and not bool(term.get("fixed", False))
    )


def _is_modified_gravity_correction(term: Dict[str, Any]) -> bool:
    if _is_eh_operator(term) or bool(term.get("fixed", False)):
        return False
    return "R" in str(term.get("candidate") or "")


def _planned_field_factor(candidate: str, sample: Dict[str, Any]) -> float:
    phi1 = abs(float(sample.get("varphi1_0_phi1_over_Mp", 1.0) or 1.0))
    phi2 = abs(float(sample.get("varphi2_0_phi2_over_Lambda", 1.0) or 1.0))
    factor = 1.0
    factor *= max(phi1, 1e-12) ** candidate.count("φ1")
    factor *= max(phi2, 1e-12) ** candidate.count("φ2")
    return factor


def _correction_sampling_mode(entry: Dict[str, Any], index: int) -> str:
    terms = ((entry.get("lagrangian") or {}).get("terms") or [])
    if not any(_is_modified_gravity_correction(term) for term in terms):
        return "baseline"
    cycle = list(CORRECTION_SAMPLING.get("mode_cycle") or ["weak", "moderate"])
    return str(cycle[index % len(cycle)])


def _sample_target_relative_effect(mode: str, rng: random.Random) -> float:
    spec = (CORRECTION_SAMPLING.get("target_relative_effect") or {}).get(mode) or {}
    low = float(spec.get("low", 0.0))
    high = float(spec.get("high", 0.0))
    if low <= 0.0 or high <= 0.0:
        return 0.0
    if spec.get("log10"):
        return 10 ** rng.uniform(math.log10(low), math.log10(high))
    return rng.uniform(low, high)


def _coefficient_for_planned_effect(
    *,
    term: Dict[str, Any],
    sample: Dict[str, Any],
    mode: str,
    rng: random.Random,
    priors: Dict[str, Any],
) -> float:
    if mode == "baseline" or not _is_modified_gravity_correction(term):
        return _coefficient_value(rng, priors)

    target = _sample_target_relative_effect(mode, rng)
    if target <= 0.0:
        return _coefficient_value(rng, priors)

    lambda_h = max(float(sample.get("lambda_H_Lambda_over_H0", 1.0) or 1.0), 1e-12)
    power = int(term.get("lambda_power", 0) or 0)
    candidate = str(term.get("candidate") or "")
    field_factor = _planned_field_factor(candidate, sample)
    try:
        lambda_factor = abs(lambda_h**power)
    except OverflowError:
        lambda_factor = math.inf
    denom = max(lambda_factor * field_factor, 1e-300)
    magnitude = abs(EH_R_COEFFICIENT) * target / denom

    scatter = float(CORRECTION_SAMPLING.get("coefficient_log10_scatter", 0.0) or 0.0)
    if scatter > 0:
        magnitude *= 10 ** rng.uniform(-scatter, scatter)

    magnitude = min(
        float(CORRECTION_SAMPLING.get("coefficient_abs_max", 1e6)),
        max(float(CORRECTION_SAMPLING.get("coefficient_abs_min", 1e-10)), magnitude),
    )
    return rng.choice(COEFFICIENT_PRIOR["signs"]) * magnitude


def _parameter_sampling_policy_summary(entry: Dict[str, Any], count: int) -> Dict[str, Any]:
    mode_counts: Dict[str, int] = {}
    for index in range(count):
        mode = _correction_sampling_mode(entry, index)
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
    return {
        "strategy": "planned_relative_effect",
        "mode_counts": mode_counts,
        "target_relative_effect": CORRECTION_SAMPLING.get("target_relative_effect"),
        "coefficient_abs_min": CORRECTION_SAMPLING.get("coefficient_abs_min"),
        "coefficient_abs_max": CORRECTION_SAMPLING.get("coefficient_abs_max"),
        "notes": (
            "Non-EH curvature correction coefficients are sampled from a target effective size "
            "relative to the EH term using lambda_power and scalar field factors. EH R is fixed."
        ),
    }


def _default_prior(key: str) -> Dict[str, Any]:
    return PARAMETER_PRIORS[key]


def _sample_parameter(rng: random.Random, learned_priors: Dict[str, Any], key: str) -> float:
    default = _default_prior(key)
    return _sample_prior_value(
        rng,
        learned_priors,
        key,
        default_low=float(default["low"]),
        default_high=float(default["high"]),
        default_log=bool(default.get("log10")),
    )


def _parameter_sample(entry: Dict[str, Any], rng: random.Random, index: int, summary: Dict[str, Any]) -> Dict[str, Any]:
    scalar_config = entry["scalar_config"]
    priors = _parameter_priors(summary)
    term_by_coeff = _term_by_coefficient(entry)
    correction_mode = _correction_sampling_mode(entry, index)
    sample: Dict[str, Any] = {
        "H0_km_s_Mpc": _sample_parameter(rng, priors, "H0_km_s_Mpc"),
        "Omega_m0": _sample_parameter(rng, priors, "Omega_m0"),
        "lambda_H_Lambda_over_H0": _sample_parameter(rng, priors, "lambda_H_Lambda_over_H0"),
    }

    if scalar_config in {"phi1_only", "both"}:
        sample.update(
            {
                "varphi1_0_phi1_over_Mp": _sample_parameter(rng, priors, "varphi1_0_phi1_over_Mp"),
                "mu1_m1_over_H0": _sample_parameter(rng, priors, "mu1_m1_over_H0"),
                "fbar1_f1_over_Mp": _sample_parameter(rng, priors, "fbar1_f1_over_Mp"),
            }
        )
    if scalar_config in {"phi2_only", "both"}:
        sample.update(
            {
                "varphi2_0_phi2_over_Lambda": _sample_parameter(rng, priors, "varphi2_0_phi2_over_Lambda"),
                "mu2_m2_over_Lambda": _sample_parameter(rng, priors, "mu2_m2_over_Lambda"),
                "fbar2_f2_over_Lambda": _sample_parameter(rng, priors, "fbar2_f2_over_Lambda"),
            }
        )
    if scalar_config in {"phi2_only", "both"}:
        sample["q2_0_dvarphi2_dln_a"] = _sample_parameter(rng, priors, "q2_0_dvarphi2_dln_a")

    for spec in entry["operator_specs"]:
        label = spec["candidate"]
        coeff = spec["coefficient"]
        term = term_by_coeff.get(coeff, {"candidate": label})
        if _is_eh_operator(term) or label == "R":
            sample[coeff] = EH_R_COEFFICIENT
        else:
            sample[coeff] = _coefficient_for_planned_effect(
                term=term,
                sample=sample,
                mode=correction_mode,
                rng=rng,
                priors=priors,
            )

    if index > 0:
        # Local perturbations within the same cold-start prior, not copied from old results.
        sample["H0_km_s_Mpc"] += rng.uniform(-2.0, 2.0)
        sample["Omega_m0"] = min(0.45, max(0.18, sample["Omega_m0"] + rng.uniform(-0.03, 0.03)))
    return sample


def _parameter_samples(entry: Dict[str, Any], rng: random.Random, count: int, summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [_parameter_sample(entry, rng, i, summary) for i in range(count)]


def _proposal_for(
    entry: Dict[str, Any],
    loop_index: int,
    parameter_samples: List[Dict[str, Any]],
    stage: str,
) -> Dict[str, Any]:
    rationale = (
        "Cold-start proposal generated from token-level Grammar Masker and current-loop memory only. "
        "No historical solver_result, top-10 plot, or old best-fit parameter was used."
    )
    if entry.get("proposal_mode") == "llm":
        rationale = (
            "OpenAI API selected this proposal from a batch of token-level Grammar Masker legal candidates. "
            f"LLM rationale: {entry.get('llm_rationale')}"
        )
    elif entry.get("proposal_mode") == "deterministic_fallback":
        rationale = (
            "Deterministic fallback proposal generated after LLM selection was unavailable or invalid. "
            f"Fallback reason: {entry.get('llm_error', 'unknown')}"
        )
    return {
        "proposal_id": f"cold_start_token_loop_{loop_index:02d}_{stage}",
        "theory": {
            "scalar_config": entry["scalar_config"],
            "potential_types": entry["potential_types"],
            "operators": [
                {"coefficient": spec["coefficient"], "candidate": spec["candidate"]}
                for spec in entry["operator_specs"]
            ],
        },
        "parameter_samples": parameter_samples,
        "parameter_sampling_policy": _parameter_sampling_policy_summary(entry, len(parameter_samples)),
        "rationale": rationale,
        "cold_start": True,
        "source": "token_level_grammar",
        "proposal_mode": entry.get("proposal_mode", "deterministic"),
        "target_operator_count": entry.get("target_operator_count"),
        **(
            {
                "llm_model": entry.get("llm_model"),
                "llm_choice": entry.get("llm_choice"),
            }
            if entry.get("proposal_mode") == "llm"
            else {}
        ),
        "catalog_location": {
            "source_n_terms": entry["n_terms"],
            "source_local_number": entry["local_number"],
        },
    }


def _write_token_level_source(entry: Dict[str, Any], path: Path) -> None:
    payload = {entry["n_terms"]: [entry["lagrangian"]]}
    _register_dynamic_functions_for_pickle(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)


def _best_chi2(result) -> Optional[float]:
    return float(result.chi2) if result.chi2 is not None else None


def _top_reject_total(attempt: Dict[str, Any]) -> int:
    total = 0
    for row in attempt.get("top_reject_reasons") or []:
        if isinstance(row, dict):
            try:
                total += int(row.get("count") or 0)
            except (TypeError, ValueError):
                continue
    return total


def _reject_category_counts(attempt: Dict[str, Any]) -> Dict[str, int]:
    categories = {
        "q_initial_root_failure": 0,
        "q_not_determined": 0,
        "no_scalar_constraint": 0,
        "constraint_drift": 0,
        "integration_failure": 0,
        "h_absurdly_large": 0,
    }
    for row in attempt.get("top_reject_reasons") or []:
        if not isinstance(row, dict):
            continue
        reason = str(row.get("reason") or "").lower()
        try:
            count = int(row.get("count") or 0)
        except (TypeError, ValueError):
            count = 0
        if "no acceptable real q" in reason and "_0 root" in reason:
            categories["q_initial_root_failure"] += count
        elif "q1_x not determined" in reason or "q2_x not determined" in reason:
            categories["q_not_determined"] += count
        elif "no-scalar constraint" in reason or "no scalar constraint" in reason:
            categories["no_scalar_constraint"] += count
        elif "constraint drift" in reason:
            categories["constraint_drift"] += count
        elif "solve_ivp failed" in reason or "integration failed" in reason or "ivp failed" in reason:
            categories["integration_failure"] += count
        elif "absurdly large" in reason:
            categories["h_absurdly_large"] += count
    return categories


def _structural_expansion_skip_reason(attempt: Dict[str, Any], best: Optional[float]) -> Optional[str]:
    if best is not None:
        return None

    tags = set(attempt.get("failure_tags") or [])
    structural_tags = sorted(tags & STRUCTURAL_EXPANSION_SKIP_TAGS)
    theory = attempt.get("theory") or {}
    scalar_config = str(theory.get("scalar_config"))

    failed_stage = attempt.get("failed_stage")
    if failed_stage in {"GrammarGeneration", "EOM", "Builder", "AgentSample"}:
        return f"structural pre-sampling failure stage={failed_stage} tags={structural_tags}"

    if "no_scalar_constraint" in tags:
        return f"structural failure tags={structural_tags}; no accepted chi2"
    if scalar_config == "none" and "missing_ranking" in tags and "no_accepted_samples" in tags:
        return "no-scalar empty ranking after first 1000 samples; no expanded sampling"
    if ("constraint_drift" in tags or "integration_failure" in tags) and "no_accepted_samples" in tags:
        return f"numerical instability tags={sorted(tags & {'constraint_drift', 'integration_failure'})}; no expanded sampling"

    sample_count = theory.get("parameter_sample_count")
    reject_total = _top_reject_total(attempt)
    if sample_count is None:
        return f"structural failure tags={structural_tags}; no accepted chi2"
    try:
        sample_count_int = int(sample_count)
    except (TypeError, ValueError):
        return f"structural failure tags={structural_tags}; no accepted chi2"

    category_counts = _reject_category_counts(attempt)
    dominant_structural = {
        tag: count
        for tag, count in category_counts.items()
        if tag in {"q_initial_root_failure", "q_not_determined", "no_scalar_constraint"}
        and count >= int(HIGH_COUNT_REJECT_FRACTION * sample_count_int)
    }
    dominant_numerical = {
        tag: count
        for tag, count in category_counts.items()
        if tag in {"constraint_drift", "integration_failure"}
        and count >= int(HIGH_COUNT_REJECT_FRACTION * sample_count_int)
    }

    if dominant_structural:
        return f"structural rejection dominates {dominant_structural}; no expanded sampling"
    if dominant_numerical:
        return f"numerical rejection dominates {dominant_numerical}; no expanded sampling"
    if not structural_tags:
        return None
    if sample_count_int <= 0 or reject_total >= int(0.9 * sample_count_int):
        return f"structural failure tags={structural_tags}; rejected {reject_total}/{sample_count_int} samples"
    return None


def run(
    loop_count: int,
    seed: int,
    run_name: Optional[str] = None,
    initial_parameter_samples: int = 1000,
    expanded_parameter_samples: int = 3000,
    expansion_chi2: float = 2000.0,
    pre_sampling_timeout: int = 120,
    grammar_generation_timeout: int = 0,
    use_token_context_cache: bool = True,
) -> Dict[str, Any]:
    rng = random.Random(seed)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    name = run_name or f"cold_start_20_{stamp}"
    proposal_dir = ROOT / "ai_theory_lab" / "proposals" / name
    memory_dir = ROOT / "ai_theory_lab" / "memory" / name
    proposal_dir.mkdir(parents=True, exist_ok=False)
    memory_dir.mkdir(parents=True, exist_ok=False)

    try:
        token_context = _build_token_level_context(grammar_generation_timeout, use_cache=use_token_context_cache)
        _write_token_level_context_summary(token_context, proposal_dir / "operator_catalog_summary.json")
    except Exception as exc:
        result = ValidationResult(
            validated=False,
            failed_stage="GrammarGeneration",
            diagnostics={
                "message": f"Initial independent-scalar discovery failed before loop sampling: {type(exc).__name__}: {exc}",
                "failure_kind": "pre_sampling_timeout" if isinstance(exc, TimeoutError) else "grammar_generation_failure",
            },
        )
        record_attempt(result, memory_dir, loop_id="operator_discovery")
        output = {
            "run_name": name,
            "proposal_dir": str(proposal_dir),
            "memory_dir": str(memory_dir),
            "results": [
                {
                    "stage": "operator_discovery",
                    "validated": False,
                    "failed_stage": "GrammarGeneration",
                    "chi2": None,
                    "diagnostic_message": result.diagnostics["message"],
                }
            ],
            "summary": _load_summary(memory_dir),
        }
        (proposal_dir / "run_summary.json").write_text(
            json.dumps(output, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return output

    results: List[Dict[str, Any]] = []
    for loop_index in range(1, loop_count + 1):
        summary = _load_summary(memory_dir)
        try:
            with _wall_timeout(pre_sampling_timeout, "Token-level proposal generation"):
                entry = _generate_token_level_entry(
                    token_context,
                    summary,
                    rng,
                    seed + loop_index * 7919,
                )
        except Exception as exc:
            result = ValidationResult(
                validated=False,
                failed_stage="GrammarGeneration",
                diagnostics={
                    "message": f"Token-level Grammar Masker generation failed before sampling: {type(exc).__name__}: {exc}",
                    "failure_kind": "pre_sampling_timeout" if isinstance(exc, TimeoutError) else "grammar_generation_failure",
                },
            )
            memory_info = record_attempt(result, memory_dir, loop_id=f"loop_{loop_index:02d}")
            attempt = memory_info["attempt"]
            results.append(
                {
                    "loop": loop_index,
                    "stage": "grammar_generation",
                    "validated": False,
                    "failed_stage": "GrammarGeneration",
                    "chi2": None,
                    "family_key": attempt["family_key"],
                    "failure_tags": attempt["failure_tags"],
                    "diagnostic_message": result.diagnostics["message"],
                }
            )
            print(
                f"[{loop_index:02d}/{loop_count}] fail:GrammarGeneration "
                f"{type(exc).__name__}: {exc}",
                flush=True,
            )
            continue
        source_path = proposal_dir / f"loop_{loop_index:02d}_token_lagrangians.pkl"
        _write_token_level_source(entry, source_path)

        samples_1000 = _parameter_samples(entry, rng, initial_parameter_samples, summary)
        proposal = _proposal_for(entry, loop_index, samples_1000, "initial")
        proposal_path = proposal_dir / f"loop_{loop_index:02d}_initial.json"
        proposal_path.write_text(json.dumps(proposal, indent=2, ensure_ascii=False), encoding="utf-8")
        parameter_path = proposal_dir / f"loop_{loop_index:02d}_initial_parameter_samples.json"
        parameter_path.write_text(json.dumps(samples_1000, indent=2, ensure_ascii=False), encoding="utf-8")
        result = validate_agent_sample_pipeline(
            source_lagrangians_path=source_path,
            source_n_terms=entry["n_terms"],
            source_local_number=1,
            parameter_samples_path=parameter_path,
            timeout_eom=pre_sampling_timeout,
            timeout_builder=pre_sampling_timeout,
            timeout_solver=600,
            extra_env={
                "SOLVER_SETUP_TIMEOUT_SECONDS": str(pre_sampling_timeout),
            },
        )
        memory_info = record_attempt(result, memory_dir, loop_id=f"loop_{loop_index:02d}")
        attempt = memory_info["attempt"]
        loop_record = {
            "loop": loop_index,
            "stage": "initial",
            "proposal_path": str(proposal_path),
            "source_lagrangians_path": str(source_path),
            "parameter_samples_path": str(parameter_path),
            "validated": result.validated,
            "failed_stage": result.failed_stage,
            "chi2": result.chi2,
            "family_key": attempt["family_key"],
            "failure_tags": attempt["failure_tags"],
            "top_reject_reasons": attempt["top_reject_reasons"],
            "solver_output_dir": result.solver_output_dir,
        }
        results.append(loop_record)
        status = "ok" if result.validated else f"fail:{result.failed_stage}"
        print(
            f"[{loop_index:02d}/{loop_count}] initial {status} chi2={result.chi2} "
            f"family={attempt['family_key']} tags={attempt['failure_tags']}",
            flush=True,
        )

        best = _best_chi2(result)
        skip_expansion_reason = _structural_expansion_skip_reason(attempt, best)
        if skip_expansion_reason:
            loop_record["skip_expansion_reason"] = skip_expansion_reason
            print(
                f"[{loop_index:02d}/{loop_count}] skip expanded sampling: {skip_expansion_reason}",
                flush=True,
            )
            continue
        if best is None or best >= expansion_chi2:
            samples_3000 = _parameter_samples(entry, rng, expanded_parameter_samples, summary)
            expanded_proposal = _proposal_for(entry, loop_index, samples_3000, "expanded")
            expanded_proposal_path = proposal_dir / f"loop_{loop_index:02d}_expanded.json"
            expanded_proposal_path.write_text(json.dumps(expanded_proposal, indent=2, ensure_ascii=False), encoding="utf-8")
            expanded_parameter_path = proposal_dir / f"loop_{loop_index:02d}_expanded_parameter_samples.json"
            expanded_parameter_path.write_text(json.dumps(samples_3000, indent=2, ensure_ascii=False), encoding="utf-8")
            expanded_result = validate_agent_sample_pipeline(
                source_lagrangians_path=source_path,
                source_n_terms=entry["n_terms"],
                source_local_number=1,
                parameter_samples_path=expanded_parameter_path,
                timeout_eom=pre_sampling_timeout,
                timeout_builder=pre_sampling_timeout,
                timeout_solver=1200,
                extra_env={
                    "SOLVER_SETUP_TIMEOUT_SECONDS": str(pre_sampling_timeout),
                },
            )
            expanded_memory_info = record_attempt(expanded_result, memory_dir, loop_id=f"loop_{loop_index:02d}_expanded")
            expanded_attempt = expanded_memory_info["attempt"]
            results.append(
                {
                    "loop": loop_index,
                    "stage": "expanded",
                    "proposal_path": str(expanded_proposal_path),
                    "source_lagrangians_path": str(source_path),
                    "parameter_samples_path": str(expanded_parameter_path),
                    "validated": expanded_result.validated,
                    "failed_stage": expanded_result.failed_stage,
                    "chi2": expanded_result.chi2,
                    "family_key": expanded_attempt["family_key"],
                    "failure_tags": expanded_attempt["failure_tags"],
                    "top_reject_reasons": expanded_attempt["top_reject_reasons"],
                    "solver_output_dir": expanded_result.solver_output_dir,
                }
            )
            expanded_status = "ok" if expanded_result.validated else f"fail:{expanded_result.failed_stage}"
            print(
                f"[{loop_index:02d}/{loop_count}] expanded {expanded_status} chi2={expanded_result.chi2} "
                f"family={expanded_attempt['family_key']} tags={expanded_attempt['failure_tags']}",
                flush=True,
            )
    final_summary = _load_summary(memory_dir)
    output = {
        "run_name": name,
        "proposal_dir": str(proposal_dir),
        "memory_dir": str(memory_dir),
        "results": results,
        "summary": final_summary,
    }
    summary_path = proposal_dir / "run_summary.json"
    summary_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a cold-start agent proposal loop.")
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
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    output = run(
        args.loops,
        args.seed,
        args.run_name,
        initial_parameter_samples=args.initial_parameter_samples,
        expanded_parameter_samples=args.expanded_parameter_samples,
        expansion_chi2=args.expansion_chi2,
        pre_sampling_timeout=args.pre_sampling_timeout,
        grammar_generation_timeout=args.grammar_generation_timeout,
        use_token_context_cache=not args.no_token_context_cache,
    )
    print(json.dumps(output, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
