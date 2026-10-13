#!/usr/bin/env python3
"""Finite-difference background identifiability diagnostics.

The audit works with a caller-supplied evaluator so it remains independent of
the Solver implementation.  It estimates the rank of the map from fitted
parameters to the accepted background trajectory.  Profiled likelihood
nuisance parameters are counted separately because they do not enter h(z).
"""
from __future__ import annotations

import math
from typing import Any, Callable, Dict, Iterable, Mapping, Sequence, Tuple

import numpy as np


FeatureEvaluator = Callable[[Mapping[str, float]], Tuple[bool, np.ndarray | None, str]]


_POSITIVE_LOG_PARAMETERS = {
    "H0_km_s_Mpc",
    "Omega_m0",
    "lambda_H_Lambda_over_H0",
    "mu1_m1_over_H0",
    "mu2_m2_over_Lambda",
    "fbar1_f1_over_Mp",
    "fbar2_f2_over_Lambda",
}

_LINEAR_PARAMETER_PREFIXES = (
    "varphi1_0_",
    "varphi2_0_",
    "chi_bar_0_",
    "q1_0_",
    "q2_0_",
    "qchi_0_",
)


def _parameter_key(sample: Mapping[str, float], name: str) -> str | None:
    """Locate a Solver parameter in a stored best-fit sample."""

    bare = str(name).replace("\\", "")
    candidates = [str(name), bare, f"\\{bare}"]
    for candidate in tuple(candidates):
        candidates.extend((f"coef:{candidate}", f"coefficient:{candidate}"))
    for candidate in candidates:
        if candidate in sample:
            return candidate
    return None


def _perturbed_values(name: str, value: float, relative_step: float) -> Tuple[float, float, float, str]:
    """Return plus, minus, and coordinate denominator for one parameter."""

    if name in _POSITIVE_LOG_PARAMETERS and value > 0.0:
        plus = value * math.exp(relative_step)
        minus = value * math.exp(-relative_step)
        return plus, minus, 2.0 * relative_step, "log"

    is_linear = name.startswith(_LINEAR_PARAMETER_PREFIXES)
    if not is_linear and value != 0.0:
        # Free Wilson coefficients are best conditioned in signed-log magnitude.
        plus = math.copysign(abs(value) * math.exp(relative_step), value)
        minus = math.copysign(abs(value) * math.exp(-relative_step), value)
        return plus, minus, 2.0 * relative_step, "signed_log"

    scale = max(abs(value), 1.0)
    delta = relative_step * scale
    return value + delta, value - delta, 2.0 * relative_step, "scaled_linear"


def _null_combinations(
    parameter_names: Sequence[str],
    vh: np.ndarray,
    rank: int,
    coefficient_floor: float = 0.1,
) -> list[Dict[str, float]]:
    combinations: list[Dict[str, float]] = []
    for vector in vh[rank:]:
        max_abs = float(np.max(np.abs(vector))) if vector.size else 0.0
        if max_abs <= 0.0:
            continue
        normalized = vector / max_abs
        combination = {
            name: float(value)
            for name, value in zip(parameter_names, normalized)
            if abs(float(value)) >= coefficient_floor
        }
        if combination:
            combinations.append(combination)
    return combinations


def audit_background_identifiability(
    *,
    parameter_names: Iterable[str],
    base_sample: Mapping[str, float],
    baseline_feature: np.ndarray,
    evaluator: FeatureEvaluator,
    profiled_parameter_names: Iterable[str] = (),
    relative_step: float = 1.0e-3,
    rank_rtol: float = 1.0e-4,
    zero_response_tol: float = 1.0e-10,
    step_multipliers: Sequence[float] = (1.0, 3.0, 0.3, 10.0),
) -> Dict[str, Any]:
    """Estimate identifiable fit directions from the accepted h(z) trajectory.

    Failed perturbation directions are retained conservatively in the effective
    count.  The audit can therefore decline to reduce ``k``, but a stability
    boundary cannot spuriously make a model look simpler.
    """

    names = list(dict.fromkeys(str(name) for name in parameter_names))
    profiled = [name for name in names if name in set(profiled_parameter_names)]
    dynamic = [name for name in names if name not in set(profiled_parameter_names)]
    baseline = np.asarray(baseline_feature, dtype=float).reshape(-1)
    if baseline.size == 0 or not np.all(np.isfinite(baseline)):
        return {
            "status": "unavailable",
            "reason": "baseline feature is empty or non-finite",
            "k_nominal": len(names),
            "k_identifiable": len(names),
        }

    columns: list[np.ndarray] = []
    resolved_names: list[str] = []
    unresolved_names: list[str] = []
    zero_response_names: list[str] = []
    perturbation_details: Dict[str, Any] = {}
    evaluations = 0

    for name in dynamic:
        key = _parameter_key(base_sample, name)
        if key is None:
            unresolved_names.append(name)
            perturbation_details[name] = {"status": "missing_from_best_sample"}
            continue
        value = float(base_sample[key])
        if not math.isfinite(value):
            unresolved_names.append(name)
            perturbation_details[name] = {"status": "non_finite_best_value"}
            continue

        derivative = None
        detail: Dict[str, Any] = {}
        for multiplier in step_multipliers:
            step = float(relative_step) * float(multiplier)
            plus_value, minus_value, denominator, coordinate = _perturbed_values(name, value, step)
            plus_sample = dict(base_sample)
            minus_sample = dict(base_sample)
            plus_sample[key] = plus_value
            minus_sample[key] = minus_value
            plus_ok, plus_feature, plus_reason = evaluator(plus_sample)
            minus_ok, minus_feature, minus_reason = evaluator(minus_sample)
            evaluations += 2

            plus_array = np.asarray(plus_feature, dtype=float).reshape(-1) if plus_ok else None
            minus_array = np.asarray(minus_feature, dtype=float).reshape(-1) if minus_ok else None
            plus_valid = bool(
                plus_ok and plus_array is not None and plus_array.shape == baseline.shape
                and np.all(np.isfinite(plus_array))
            )
            minus_valid = bool(
                minus_ok and minus_array is not None and minus_array.shape == baseline.shape
                and np.all(np.isfinite(minus_array))
            )
            if plus_valid and minus_valid:
                derivative = (plus_array - minus_array) / denominator
                detail = {
                    "status": "central",
                    "coordinate": coordinate,
                    "relative_step": step,
                    "sample_key": key,
                }
                break
            if plus_valid:
                plus2_value, _, _, _ = _perturbed_values(name, value, 2.0 * step)
                plus2_sample = dict(base_sample)
                plus2_sample[key] = plus2_value
                plus2_ok, plus2_feature, plus2_reason = evaluator(plus2_sample)
                evaluations += 1
                plus2_array = (
                    np.asarray(plus2_feature, dtype=float).reshape(-1)
                    if plus2_ok else None
                )
                plus2_valid = bool(
                    plus2_ok and plus2_array is not None
                    and plus2_array.shape == baseline.shape
                    and np.all(np.isfinite(plus2_array))
                )
                if plus2_valid:
                    derivative = (-3.0 * baseline + 4.0 * plus_array - plus2_array) / denominator
                    stencil = "forward_second_order"
                else:
                    derivative = (plus_array - baseline) / (denominator / 2.0)
                    stencil = "forward"
                detail = {
                    "status": stencil,
                    "coordinate": coordinate,
                    "relative_step": step,
                    "sample_key": key,
                    "minus_failure": minus_reason,
                    "second_plus_failure": "" if plus2_valid else plus2_reason,
                }
                break
            if minus_valid:
                _, minus2_value, _, _ = _perturbed_values(name, value, 2.0 * step)
                minus2_sample = dict(base_sample)
                minus2_sample[key] = minus2_value
                minus2_ok, minus2_feature, minus2_reason = evaluator(minus2_sample)
                evaluations += 1
                minus2_array = (
                    np.asarray(minus2_feature, dtype=float).reshape(-1)
                    if minus2_ok else None
                )
                minus2_valid = bool(
                    minus2_ok and minus2_array is not None
                    and minus2_array.shape == baseline.shape
                    and np.all(np.isfinite(minus2_array))
                )
                if minus2_valid:
                    derivative = (3.0 * baseline - 4.0 * minus_array + minus2_array) / denominator
                    stencil = "backward_second_order"
                else:
                    derivative = (baseline - minus_array) / (denominator / 2.0)
                    stencil = "backward"
                detail = {
                    "status": stencil,
                    "coordinate": coordinate,
                    "relative_step": step,
                    "sample_key": key,
                    "plus_failure": plus_reason,
                    "second_minus_failure": "" if minus2_valid else minus2_reason,
                }
                break
            detail = {
                "status": "failed",
                "relative_step": step,
                "plus_failure": plus_reason,
                "minus_failure": minus_reason,
            }

        if derivative is None or not np.all(np.isfinite(derivative)):
            unresolved_names.append(name)
            perturbation_details[name] = detail
            continue

        norm = float(np.linalg.norm(derivative))
        detail["response_norm"] = norm
        perturbation_details[name] = detail
        if norm <= float(zero_response_tol):
            zero_response_names.append(name)
            columns.append(np.zeros_like(derivative))
        else:
            columns.append(derivative / norm)
        resolved_names.append(name)

    if columns:
        matrix = np.column_stack(columns)
        _, singular_values, vh = np.linalg.svd(matrix, full_matrices=True)
        largest = float(singular_values[0]) if singular_values.size else 0.0
        threshold = float(rank_rtol) * largest
        dynamic_rank = int(np.sum(singular_values > threshold)) if largest > 0.0 else 0
        smallest = float(singular_values[-1]) if singular_values.size else 0.0
        condition_number_infinite = bool(
            dynamic_rank < len(resolved_names) or smallest <= 0.0
        )
        condition_number = None if condition_number_infinite else largest / smallest
        null_combinations = _null_combinations(resolved_names, vh, dynamic_rank)
    else:
        singular_values = np.asarray([], dtype=float)
        dynamic_rank = 0
        threshold = 0.0
        condition_number = None
        condition_number_infinite = True
        null_combinations = []

    k_identifiable = dynamic_rank + len(unresolved_names) + len(profiled)
    k_identifiable = min(len(names), int(k_identifiable))
    status = "ok" if not unresolved_names else "partial_conservative"
    return {
        "status": status,
        "reason": "",
        "k_nominal": len(names),
        "k_identifiable": k_identifiable,
        "dynamic_parameter_count": len(dynamic),
        "dynamic_rank": dynamic_rank,
        "profiled_parameter_count": len(profiled),
        "profiled_parameter_names": profiled,
        "resolved_parameter_names": resolved_names,
        "unresolved_parameter_names": unresolved_names,
        "zero_response_parameter_names": zero_response_names,
        "singular_values": [float(value) for value in singular_values],
        "rank_threshold": threshold,
        "rank_rtol": float(rank_rtol),
        "relative_step": float(relative_step),
        "condition_number": condition_number,
        "condition_number_infinite": condition_number_infinite,
        "null_combinations": null_combinations,
        "perturbations": perturbation_details,
        "solver_evaluations": evaluations,
    }
