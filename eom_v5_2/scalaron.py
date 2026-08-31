#!/usr/bin/env python3
"""Classify and scalarize algebraic nonlinear-in-R sectors before EOM filtering."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import math
from typing import Any, Dict, Iterable, Optional, Tuple

import sympy as sp


t = sp.Symbol("t", real=True)
N = sp.Function("N", positive=True)(t)
a = sp.Function("a", positive=True)(t)
phi1 = sp.Function("phi1")(t)
phi2 = sp.Function("phi2")(t)
chi = sp.Function("chi")(t)

Mp = sp.Symbol("M_p", positive=True)
Lambda = sp.Symbol(r"\Lambda", positive=True)

sqrt_mg = N * a**3
R_flrw = 6 * (
    (N * sp.diff(a, t, 2) - sp.diff(N, t) * sp.diff(a, t)) * a
    + N * sp.diff(a, t) ** 2
) / (N**3 * a**2)


@dataclass(frozen=True)
class AlgebraicRMonomial:
    """One exact monomial phi1^p phi2^q R^n from the serialized grammar."""

    term_index: int
    phi1_power: int
    phi2_power: int
    r_power: int
    coefficient: sp.Expr
    lambda_power: int

    def evaluate(self, curvature: sp.Expr) -> sp.Expr:
        return (
            self.coefficient
            * Lambda**self.lambda_power
            * phi1**self.phi1_power
            * phi2**self.phi2_power
            * curvature**self.r_power
        )


def _normalize_factor(factor: str) -> str:
    value = factor.strip().replace(" ", "")
    replacements = {
        r"\phi_1": "phi1",
        r"\phi_2": "phi2",
        "phi_1": "phi1",
        "phi_2": "phi2",
        "φ1": "phi1",
        "φ2": "phi2",
    }
    return replacements.get(value, value)


def parse_algebraic_r_monomial(
    term: Dict[str, Any], term_index: int
) -> Optional[AlgebraicRMonomial]:
    """Return an exact algebraic-R monomial, rejecting tensors and derivatives."""
    if term.get("fixed") or term.get("sector") not in {"gravity", "non-minimal"}:
        return None

    label = str(term.get("candidate") or "")
    factors = [_normalize_factor(part) for part in label.split("·")]
    if not factors or any(part not in {"phi1", "phi2", "R"} for part in factors):
        return None

    r_power = factors.count("R")
    if r_power == 0:
        return None

    return AlgebraicRMonomial(
        term_index=term_index,
        phi1_power=factors.count("phi1"),
        phi2_power=factors.count("phi2"),
        r_power=r_power,
        coefficient=sp.Symbol(str(term["coeff_symbol"])),
        lambda_power=int(term.get("lambda_power", 0)),
    )


def classify_scalaron_sector(terms: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Classify a serialized theory without changing it."""
    term_list = list(terms)
    monomials = tuple(
        monomial
        for index, term in enumerate(term_list)
        if (monomial := parse_algebraic_r_monomial(term, index)) is not None
    )
    nonlinear = tuple(monomial for monomial in monomials if monomial.r_power >= 2)
    if not nonlinear:
        classification = "ordinary"
    else:
        algebraic_indices = {monomial.term_index for monomial in monomials}
        residual = [
            index
            for index, term in enumerate(term_list)
            if not term.get("fixed") and index not in algebraic_indices
        ]
        classification = "hybrid" if residual else "scalarizable"

    return {
        "classification": classification,
        "enabled": bool(nonlinear),
        "algebraic_term_indices": [item.term_index for item in monomials],
        "nonlinear_term_indices": [item.term_index for item in nonlinear],
        "monomials": monomials,
    }


def scalarize_lagrangian_data(L_data: Dict[str, Any]) -> Dict[str, Any]:
    """Return a scalaron-equivalent copy when an algebraic nonlinear-R sector exists.

    Ordinary theories are returned unchanged apart from a small classification
    record.  The transform is deliberately restricted to exact polynomial
    monomials in R, phi1, and phi2; every residual operator is preserved.
    """
    existing = L_data.get("scalaron") or {}
    if existing.get("enabled") and "raw_substituted" in L_data:
        return deepcopy(L_data)

    result = deepcopy(L_data)
    classification = classify_scalaron_sector(result.get("terms") or [])
    monomials: Tuple[AlgebraicRMonomial, ...] = classification.pop("monomials")

    result["scalaron"] = classification
    if not classification["enabled"]:
        return result

    raw_lagrangian = result["substituted"]
    raw_sector = sp.Add(*(item.evaluate(R_flrw) for item in monomials))
    auxiliary_sector = sp.Add(*(item.evaluate(chi) for item in monomials))
    F = sp.diff(auxiliary_sector, chi)
    U = sp.expand(chi * F - auxiliary_sector)
    scalarized_sector = sp.expand(F * R_flrw - U)
    pure_f_R = not (auxiliary_sector.has(phi1) or auxiliary_sector.has(phi2))
    scalaron_mass_squared = (
        sp.simplify(F / (3 * sp.diff(auxiliary_sector, chi, 2)) - chi / 3)
        if pure_f_R else None
    )
    scalarized_lagrangian = sp.expand(
        raw_lagrangian - sqrt_mg * Mp**2 * raw_sector
        + sqrt_mg * Mp**2 * scalarized_sector
    )

    result["raw_substituted"] = raw_lagrangian
    result["substituted"] = scalarized_lagrangian
    result["scalaron"].update({
        "field": "chi",
        "field_mass_dimension": 2,
        "f_auxiliary": auxiliary_sector,
        "F": F,
        "U": U,
        "f_RR": sp.diff(auxiliary_sector, chi, 2),
        "pure_f_R": pure_f_R,
        "scalaron_mass_squared": scalaron_mass_squared,
        "scalarized_sector": scalarized_sector,
        "raw_general": result.get("general"),
        "equivalence_condition": "chi = R",
    })
    return result


def verify_legendre_equivalence(L_data: Dict[str, Any]) -> bool:
    """Check that the transformed action reduces to the raw action at chi=R."""
    if not (L_data.get("scalaron") or {}).get("enabled"):
        return True
    difference = sp.expand(
        L_data["substituted"].subs(chi, R_flrw) - L_data["raw_substituted"]
    )
    return sp.simplify(difference) == 0


def evaluate_scalaron_health(
    L_data: Dict[str, Any], substitutions: Dict[sp.Expr, Any]
) -> Dict[str, Any]:
    """Evaluate local scalaron health conditions at one background point.

    ``F > 0`` keeps the effective Planck mass positive.  ``f_RR > 0`` is
    used as the invertible, Dolgov--Kawasaki-stable branch condition.  For
    pure f(R), the local scalaron mass is also checked.  Mixed f(R,phi_i)
    sectors require a full coupled scalar mass matrix, so no one-field mass
    claim is made here.
    """
    transformed = scalarize_lagrangian_data(L_data)
    scalaron = transformed.get("scalaron") or {}
    if not scalaron.get("enabled"):
        return {
            "applicable": False,
            "healthy": True,
            "reason": "ordinary theory: no nonlinear algebraic-R sector",
        }

    def _number(expr: sp.Expr) -> float:
        evaluated = sp.N(expr.subs(substitutions))
        if evaluated.free_symbols or evaluated.atoms(sp.Function):
            raise ValueError(f"Scalaron health expression is not fully specified: {evaluated}")
        value = float(evaluated)
        if not math.isfinite(value):
            raise ValueError(f"Scalaron health expression is non-finite: {evaluated}")
        return value

    F_value = _number(scalaron["F"])
    f_rr_value = _number(scalaron["f_RR"])
    depends_on_matter_scalars = bool(
        scalaron["f_auxiliary"].has(phi1) or scalaron["f_auxiliary"].has(phi2)
    )

    mass_squared = None
    mass_positive = None
    if not depends_on_matter_scalars:
        mass_squared = F_value / (3.0 * f_rr_value) - _number(chi) / 3.0
        mass_positive = mass_squared > 0.0

    healthy = F_value > 0.0 and f_rr_value > 0.0
    if mass_positive is not None:
        healthy = healthy and mass_positive

    return {
        "applicable": True,
        "healthy": healthy,
        "F": F_value,
        "f_RR": f_rr_value,
        "effective_planck_mass_positive": F_value > 0.0,
        "dolgov_kawasaki_stable": f_rr_value > 0.0,
        "pure_f_R": not depends_on_matter_scalars,
        "scalaron_mass_squared": mass_squared,
        "scalaron_mass_squared_positive": mass_positive,
    }
