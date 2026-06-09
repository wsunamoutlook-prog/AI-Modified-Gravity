"""Effective correction diagnostics relative to the Einstein-Hilbert term."""

from __future__ import annotations

import csv
import math
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional


ACTIVE_RELATIVE_EFFECT = 1e-2
MODERATE_RELATIVE_EFFECT = 1e-4
WEAK_RELATIVE_EFFECT = 1e-6


def _float(value: Any, default: float = math.nan) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _read_csv_first(path: Path | None) -> Dict[str, str]:
    if not path or not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows[0] if rows else {}


def _read_csv_rows(path: Path | None) -> List[Dict[str, str]]:
    if not path or not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def coefficient_value(row: Dict[str, str], symbol: str) -> Optional[str]:
    if symbol in {"1", "COEFF_FIXED_1"}:
        return "1"
    bare_symbol = symbol.replace("\\", "")
    candidates = [
        symbol,
        bare_symbol,
        f"coef:{bare_symbol}",
        f"coefficient:{bare_symbol}",
    ]
    for key in candidates:
        if key in row and row[key] not in ("", None):
            return row[key]
    return None


def _solver_dir(attempt: Dict[str, Any]) -> Path | None:
    value = attempt.get("solver_output_dir")
    return Path(value) if value else None


def _run_dir(attempt: Dict[str, Any]) -> Path | None:
    solver_dir = _solver_dir(attempt)
    if not solver_dir:
        return None
    return solver_dir.parents[1]


def load_lagrangian_from_attempt(attempt: Dict[str, Any]) -> Dict[str, Any]:
    metadata = attempt.get("agent_lagrangian")
    if isinstance(metadata, dict):
        lagrangian = metadata.get("lagrangian")
        if isinstance(lagrangian, dict):
            return lagrangian
    run_dir = _run_dir(attempt)
    if not run_dir:
        return {}
    pkl_path = run_dir / "agent_lagrangians.pkl"
    if not pkl_path.exists():
        return {}
    with pkl_path.open("rb") as f:
        data = pickle.load(f)
    best_lag_id = str(attempt.get("best_lag_id") or "")
    if isinstance(data, dict):
        global_idx = 1
        for key in sorted(data, key=lambda value: int(value)):
            group = data.get(key) or []
            for item in group:
                if best_lag_id and str(global_idx) == best_lag_id:
                    return item if isinstance(item, dict) else {}
                global_idx += 1
        for group in data.values():
            if group:
                return group[0]
    if isinstance(data, list) and data:
        return data[0]
    return {}


def accepted_sample_row_from_attempt(attempt: Dict[str, Any]) -> Dict[str, str]:
    value = attempt.get("accepted_samples_summary_path")
    rows = _read_csv_rows(Path(value)) if value else []
    if not rows:
        return {}
    lag_id = str(attempt.get("best_lag_id") or "")
    if lag_id:
        rows = [row for row in rows if str(row.get("lag_id")) == lag_id] or rows
    attempt_chi2 = _float(attempt.get("chi2"))
    if not math.isnan(attempt_chi2):
        rows = sorted(rows, key=lambda row: abs(_float(row.get("chi2")) - attempt_chi2))
    return rows[0] if rows else {}


def _candidate(term: Dict[str, Any]) -> str:
    return str(term.get("candidate") or "")


def _sector(term: Dict[str, Any]) -> str:
    return str(term.get("sector") or "")


def _is_eh_term(term: Dict[str, Any]) -> bool:
    return (
        _candidate(term).strip() == "R"
        and _sector(term) in {"gravity", "non-minimal"}
        and int(term.get("lambda_power", 0) or 0) == 0
        and not bool(term.get("fixed", False))
    )


def _is_fixed_matter(term: Dict[str, Any]) -> bool:
    return bool(term.get("fixed", False)) and _sector(term) == "matter"


def _is_modified_gravity_correction(term: Dict[str, Any]) -> bool:
    candidate = _candidate(term)
    return "R" in candidate


def _field_factor(candidate: str, row: Dict[str, str]) -> float:
    phi1 = abs(_float(row.get("varphi1_0_phi1_over_Mp"), 1.0))
    phi2 = abs(_float(row.get("varphi2_0_phi2_over_Lambda"), 1.0))
    if math.isnan(phi1):
        phi1 = 1.0
    if math.isnan(phi2):
        phi2 = 1.0
    factor = 1.0
    factor *= max(phi1, 1e-12) ** candidate.count("φ1")
    factor *= max(phi2, 1e-12) ** candidate.count("φ2")
    return factor


def _relative_effect(
    term: Dict[str, Any],
    row: Dict[str, str],
    lambda_h: float,
    eh_coeff_abs: float,
) -> Optional[float]:
    symbol = str(term.get("coeff_symbol", ""))
    coeff_text = coefficient_value(row, symbol)
    coeff = _float(coeff_text)
    if math.isnan(coeff) or not math.isfinite(coeff):
        return None
    power = int(term.get("lambda_power", 0) or 0)
    try:
        lambda_factor = lambda_h**power
    except OverflowError:
        return 0.0 if power < 0 else math.inf
    return abs(coeff) / eh_coeff_abs * abs(lambda_factor) * _field_factor(_candidate(term), row)


def effective_correction_diagnostics(
    terms: List[Dict[str, Any]],
    row: Dict[str, str],
) -> Dict[str, Any]:
    """Classify non-EH corrections by effective size relative to EH.

    Solver chi-square ranking remains independent of this diagnostic.
    """

    lambda_h = _float(row.get("lambda_H_Lambda_over_H0"))
    if math.isnan(lambda_h) or lambda_h <= 0:
        return {
            "effective_correction_status": "unclear",
            "effective_correction_reason": "missing lambda_H_Lambda_over_H0",
            "max_relative_effect_to_EH": None,
            "dominant_correction_term": "",
            "active_correction_terms": 0,
            "moderate_correction_terms": 0,
            "weak_correction_terms": 0,
            "tiny_correction_terms": 0,
            "correction_term_count": 0,
            "tiny_correction_fraction": None,
            "term_effects": [],
        }

    eh_terms = [term for term in terms if _is_eh_term(term)]
    if not eh_terms:
        return {
            "effective_correction_status": "unclear",
            "effective_correction_reason": "missing EH R reference term",
            "max_relative_effect_to_EH": None,
            "dominant_correction_term": "",
            "active_correction_terms": 0,
            "moderate_correction_terms": 0,
            "weak_correction_terms": 0,
            "tiny_correction_terms": 0,
            "correction_term_count": 0,
            "tiny_correction_fraction": None,
            "term_effects": [],
        }

    eh_values = [
        abs(_float(coefficient_value(row, str(term.get("coeff_symbol", "")))))
        for term in eh_terms
    ]
    eh_values = [value for value in eh_values if math.isfinite(value) and value > 0]
    if not eh_values:
        return {
            "effective_correction_status": "unclear",
            "effective_correction_reason": "missing EH coefficient value",
            "max_relative_effect_to_EH": None,
            "dominant_correction_term": "",
            "active_correction_terms": 0,
            "moderate_correction_terms": 0,
            "weak_correction_terms": 0,
            "tiny_correction_terms": 0,
            "correction_term_count": 0,
            "tiny_correction_fraction": None,
            "term_effects": [],
        }
    eh_coeff_abs = max(eh_values)

    effects: List[Dict[str, Any]] = []
    for term in terms:
        if _is_eh_term(term) or _is_fixed_matter(term):
            continue
        if not _is_modified_gravity_correction(term):
            continue
        value = _relative_effect(term, row, lambda_h, eh_coeff_abs)
        if value is None or not math.isfinite(value):
            effect_class = "unclear"
        elif value >= ACTIVE_RELATIVE_EFFECT:
            effect_class = "active"
        elif value >= MODERATE_RELATIVE_EFFECT:
            effect_class = "moderate"
        elif value >= WEAK_RELATIVE_EFFECT:
            effect_class = "weak"
        else:
            effect_class = "tiny"
        effects.append(
            {
                "candidate": _candidate(term),
                "coeff_symbol": term.get("coeff_symbol"),
                "coefficient": coefficient_value(row, str(term.get("coeff_symbol", ""))),
                "lambda_power": int(term.get("lambda_power", 0) or 0),
                "sector": term.get("sector"),
                "relative_effect_to_EH": value,
                "effect_class": effect_class,
            }
        )

    numeric_effects = [e for e in effects if isinstance(e.get("relative_effect_to_EH"), (int, float))]
    if not effects:
        return {
            "effective_correction_status": "eh_only",
            "effective_correction_reason": "no non-EH free correction terms",
            "max_relative_effect_to_EH": 0.0,
            "dominant_correction_term": "",
            "active_correction_terms": 0,
            "moderate_correction_terms": 0,
            "weak_correction_terms": 0,
            "tiny_correction_terms": 0,
            "correction_term_count": 0,
            "tiny_correction_fraction": None,
            "term_effects": [],
        }
    if not numeric_effects:
        return {
            "effective_correction_status": "unclear",
            "effective_correction_reason": "no numeric correction coefficient values",
            "max_relative_effect_to_EH": None,
            "dominant_correction_term": "",
            "active_correction_terms": 0,
            "moderate_correction_terms": 0,
            "weak_correction_terms": 0,
            "tiny_correction_terms": 0,
            "correction_term_count": len(effects),
            "tiny_correction_fraction": None,
            "term_effects": effects,
        }

    dominant = max(numeric_effects, key=lambda e: float(e["relative_effect_to_EH"]))
    counts = {
        "active": sum(1 for e in effects if e["effect_class"] == "active"),
        "moderate": sum(1 for e in effects if e["effect_class"] == "moderate"),
        "weak": sum(1 for e in effects if e["effect_class"] == "weak"),
        "tiny": sum(1 for e in effects if e["effect_class"] == "tiny"),
    }
    max_effect = float(dominant["relative_effect_to_EH"])
    if counts["active"]:
        status = "active"
    elif counts["moderate"]:
        status = "moderate"
    elif counts["weak"]:
        status = "weak"
    else:
        status = "eh_dominated" if eh_terms else "tiny"

    return {
        "effective_correction_status": status,
        "effective_correction_reason": "classified relative to EH coefficient and lambda_H powers",
        "max_relative_effect_to_EH": max_effect,
        "dominant_correction_term": dominant.get("candidate", ""),
        "active_correction_terms": counts["active"],
        "moderate_correction_terms": counts["moderate"],
        "weak_correction_terms": counts["weak"],
        "tiny_correction_terms": counts["tiny"],
        "correction_term_count": len(effects),
        "tiny_correction_fraction": counts["tiny"] / len(effects) if effects else None,
        "term_effects": effects,
    }


def diagnostics_for_attempt(attempt: Dict[str, Any]) -> Dict[str, Any]:
    lagrangian = load_lagrangian_from_attempt(attempt)
    row = accepted_sample_row_from_attempt(attempt)
    terms = lagrangian.get("terms") if isinstance(lagrangian, dict) else []
    if not isinstance(terms, list):
        terms = []
    return effective_correction_diagnostics(terms, row)
