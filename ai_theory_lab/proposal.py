"""Compile agent proposal JSON into isolated pipeline inputs."""

from __future__ import annotations

import json
import pickle
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional

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


VALID_SCALAR_CONFIGS = {"none", "phi1_only", "phi2_only", "both"}
VALID_POTENTIALS = {"quadratic", "axion", None}
ROOT = Path(__file__).resolve().parents[1]


def load_proposal(path: Path) -> Dict[str, Any]:
    with path.expanduser().resolve().open(encoding="utf-8") as f:
        proposal = json.load(f)
    if not isinstance(proposal, dict):
        raise TypeError("proposal JSON must be an object")
    return proposal


def _candidate_catalog(max_derivatives: int = 2, dimensions=(2, 3, 4, 5, 6)) -> Dict[str, Any]:
    tensors = _build_tensors_dict()
    masker = GravityMasker(max_derivatives=max_derivatives)
    masker.collect_candidates(tensors, dims=dimensions)
    catalog: Dict[str, Any] = {}
    for cand in masker.all_candidates:
        for key in {cand.contraction_label, cand.general_label, cand.combo_label}:
            catalog[str(key)] = cand
    return {"masker": masker, "tensors": tensors, "candidates": catalog}


def _make_potential(tensors: Dict[str, Any], which: int, pot_type: str):
    phi = tensors["phi1"] if which == 1 else tensors["phi2"]
    if which == 1:
        m, f, m_str, f_str, phi_str = m1_phi, f1_axion, "m_1", "f_1", "φ1"
    else:
        m, f, m_str, f_str, phi_str = m2_phi, f2_axion, "m_2", "f_2", "φ2"

    if pot_type == "quadratic":
        return f"-½ {m_str}² {phi_str}²", sp.Rational(-1, 2) * m**2 * phi**2
    if pot_type == "axion":
        return f"-{m_str}² {f_str}² (1 - cos({phi_str}/{f_str}))", -m**2 * f**2 * (1 - sp.cos(phi / f))
    raise ValueError(f"Invalid potential type for phi{which}: {pot_type!r}")


def _fixed_matter_terms(tensors: Dict[str, Any], scalar_config: str, potential_types: Dict[str, Any]):
    include_phi1 = scalar_config in {"phi1_only", "both"}
    include_phi2 = scalar_config in {"phi2_only", "both"}
    t_coord = tensors["coords"][0]
    n_func = sp.Function("N", positive=True)(t_coord)
    pieces: List[str] = []
    substituted = sp.Integer(0)
    terms: List[Dict[str, Any]] = []

    if include_phi1:
        phi1_dot = sp.Derivative(tensors["phi1"], t_coord)
        kinetic_general = "-½ g^{μν} ∇_μφ1 ∇_νφ1"
        kinetic_value = sp.Rational(1, 2) * phi1_dot**2 / n_func**2
        pot_type = potential_types.get("phi1")
        pot_general, pot_value = _make_potential(tensors, 1, pot_type)
        pieces.extend([kinetic_general, pot_general])
        substituted += kinetic_value + pot_value
        terms.append({
            "coeff_symbol": "1", "coeff_token": "COEFF_FIXED_1",
            "candidate": kinetic_general, "mass_dim": 4, "lambda_power": 0,
            "fixed": True, "sector": "matter",
        })
        terms.append({
            "coeff_symbol": "1", "coeff_token": "COEFF_FIXED_1",
            "candidate": pot_general, "mass_dim": 4, "lambda_power": 0,
            "fixed": True, "sector": "matter", "potential_type": pot_type,
        })

    if include_phi2:
        phi2_dot = sp.Derivative(tensors["phi2"], t_coord)
        kinetic_general = "-½ g^{μν} ∇_μφ2 ∇_νφ2"
        kinetic_value = sp.Rational(1, 2) * phi2_dot**2 / n_func**2
        pot_type = potential_types.get("phi2")
        pot_general, pot_value = _make_potential(tensors, 2, pot_type)
        pieces.extend([kinetic_general, pot_general])
        substituted += kinetic_value + pot_value
        terms.append({
            "coeff_symbol": "1", "coeff_token": "COEFF_FIXED_1",
            "candidate": kinetic_general, "mass_dim": 4, "lambda_power": 0,
            "fixed": True, "sector": "matter",
        })
        terms.append({
            "coeff_symbol": "1", "coeff_token": "COEFF_FIXED_1",
            "candidate": pot_general, "mass_dim": 4, "lambda_power": 0,
            "fixed": True, "sector": "matter", "potential_type": pot_type,
        })

    return pieces, substituted, terms


def _coefficient_symbol(raw: Optional[str], index: int) -> sp.Symbol:
    if raw:
        return sp.Symbol(str(raw))
    if index < len(_GREEK_COEFFS):
        return _GREEK_COEFFS[index]
    return sp.Symbol(f"c_{{{index + 1}}}")


def _proposal_operator_labels(theory: Dict[str, Any]) -> List[str]:
    operator_specs = theory.get("operators")
    if not isinstance(operator_specs, list):
        raise TypeError("theory.operators must be a list")
    if not operator_specs:
        raise ValueError("theory.operators must contain at least one non-fixed Grammar Masker operator")
    labels = []
    for i, spec in enumerate(operator_specs):
        if not isinstance(spec, dict):
            raise TypeError(f"theory.operators[{i}] must be an object")
        key = str(spec.get("candidate") or spec.get("operator") or spec.get("general_label") or "")
        if not key:
            raise ValueError(f"theory.operators[{i}] must contain candidate/operator/general_label")
        labels.append(key)
    return labels


def _proposal_coefficients(theory: Dict[str, Any]) -> List[str]:
    operator_specs = theory.get("operators")
    if not isinstance(operator_specs, list):
        return []
    coeffs: List[str] = []
    for spec in operator_specs:
        if not isinstance(spec, dict):
            continue
        coeff = spec.get("coefficient")
        if coeff is not None:
            coeffs.append(str(coeff))
    return coeffs


def _coefficient_aliases(coeff: str) -> List[str]:
    canonical = coeff[1:] if coeff.startswith("\\") else coeff
    aliases = [
        coeff,
        canonical,
        f"\\{canonical}",
        f"coef:{canonical}",
        f"coefficient:{canonical}",
    ]
    return list(dict.fromkeys(aliases))


def _validate_parameter_samples(parameter_samples: Any, coeffs: List[str], scalar_config: str = "none") -> None:
    if parameter_samples is None:
        return
    if not isinstance(parameter_samples, list):
        raise TypeError("proposal.parameter_samples must be a list")
    for index, sample in enumerate(parameter_samples, 1):
        if not isinstance(sample, dict):
            raise TypeError(f"proposal.parameter_samples[{index}] must be an object")
        missing = [coeff for coeff in coeffs if not any(alias in sample for alias in _coefficient_aliases(coeff))]
        if missing:
            raise ValueError(
                f"proposal.parameter_samples[{index}] is missing non-fixed coefficient values: {missing}"
            )
        if scalar_config == "both" and not any(key in sample for key in ("q2_0_dvarphi2_dln_a", "q2_0")):
            raise ValueError(
                f"proposal.parameter_samples[{index}] is missing q2_0_dvarphi2_dln_a for two-scalar models"
            )


def _normalize_parameter_samples(parameter_samples: List[Dict[str, Any]], coeffs: List[str]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for sample in parameter_samples:
        item = dict(sample)
        for coeff in coeffs:
            aliases = _coefficient_aliases(coeff)
            present = next((alias for alias in aliases if alias in item), None)
            if present is None:
                continue
            value = item[present]
            for alias in aliases:
                item.setdefault(alias, value)
        normalized.append(item)
    return normalized


def _compile_from_existing_catalog(
    *,
    theory: Dict[str, Any],
    scalar_config: str,
    potential_types: Dict[str, Any],
    source_lagrangians_path: Path,
) -> Optional[Dict[str, Any]]:
    """Find an existing grammar-generated Lagrangian with the proposed structure."""

    proposal_labels = sorted(_proposal_operator_labels(theory))
    with source_lagrangians_path.expanduser().resolve().open("rb") as f:
        data = pickle.load(f)

    for n_terms in sorted(data):
        for local_index, lagrangian in enumerate(data[n_terms], 1):
            if lagrangian.get("scalar_config") != scalar_config:
                continue
            if dict(lagrangian.get("potential_types") or {}) != {
                "phi1": potential_types.get("phi1"),
                "phi2": potential_types.get("phi2"),
            }:
                continue
            lag_labels = sorted(
                str(term.get("candidate"))
                for term in lagrangian.get("terms", [])
                if not term.get("fixed")
            )
            if lag_labels == proposal_labels:
                compiled = deepcopy(lagrangian)
                compiled["_proposal_match"] = {
                    "source_lagrangians_path": str(source_lagrangians_path.expanduser().resolve()),
                    "source_n_terms": int(n_terms),
                    "source_local_number": local_index,
                }
                return compiled
    return None


def compile_proposal_to_run(proposal_path: Path, run_dir: Path) -> Dict[str, Any]:
    proposal_path = proposal_path.expanduser().resolve()
    proposal = load_proposal(proposal_path)
    theory = proposal.get("theory")
    if not isinstance(theory, dict):
        raise TypeError("proposal must contain a 'theory' object")

    scalar_config = str(theory.get("scalar_config", "none"))
    if scalar_config not in VALID_SCALAR_CONFIGS:
        raise ValueError(f"Invalid scalar_config: {scalar_config!r}")

    potential_types = dict(theory.get("potential_types") or {})
    potential_types.setdefault("phi1", None)
    potential_types.setdefault("phi2", None)
    for key, value in potential_types.items():
        if key not in {"phi1", "phi2"}:
            raise ValueError(f"Invalid potential_types key: {key!r}")
        if value not in VALID_POTENTIALS:
            raise ValueError(f"Invalid potential type for {key}: {value!r}")
    if scalar_config in {"phi1_only", "both"} and potential_types.get("phi1") is None:
        raise ValueError("phi1 potential type is required for this scalar_config")
    if scalar_config in {"phi2_only", "both"} and potential_types.get("phi2") is None:
        raise ValueError("phi2 potential type is required for this scalar_config")

    source_lagrangians_path = Path(proposal.get("source_lagrangians_path") or ROOT / "lagrangians.pkl")
    matched_lagrangian = _compile_from_existing_catalog(
        theory=theory,
        scalar_config=scalar_config,
        potential_types=potential_types,
        source_lagrangians_path=source_lagrangians_path,
    )
    if matched_lagrangian is not None:
        match_info = dict(matched_lagrangian.pop("_proposal_match"))
        run_dir.mkdir(parents=True, exist_ok=True)
        lag_path = run_dir / "agent_lagrangians.pkl"
        payload = {matched_lagrangian["n_terms"]: [matched_lagrangian]}
        _register_dynamic_functions_for_pickle(payload)
        with lag_path.open("wb") as f:
            pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)

        metadata: Dict[str, Any] = {
            "proposal_path": str(proposal_path),
            "agent_lagrangians_path": str(lag_path),
            "proposal_id": proposal.get("proposal_id"),
            "source": "proposal_json_existing_catalog",
            "source_lagrangians_path": match_info["source_lagrangians_path"],
            "source_n_terms": match_info["source_n_terms"],
            "source_local_number": match_info["source_local_number"],
            "scalar_config": scalar_config,
            "potential_types": matched_lagrangian["potential_types"],
            "operators": _proposal_operator_labels(theory),
            "general": matched_lagrangian["general"],
        }

        parameter_samples = proposal.get("parameter_samples")
        if parameter_samples is not None:
            coeffs = _proposal_coefficients(theory)
            _validate_parameter_samples(parameter_samples, coeffs, scalar_config=scalar_config)
            parameter_samples = _normalize_parameter_samples(parameter_samples, coeffs)
            param_path = run_dir / "agent_parameter_samples.json"
            param_path.write_text(json.dumps(parameter_samples, indent=2, ensure_ascii=False), encoding="utf-8")
            metadata["agent_parameter_samples_path"] = str(param_path)

        (run_dir / "agent_lagrangian_metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return metadata

    raise ValueError(
        "Proposal theory was not found in the existing grammar-generated catalog. "
        "Use candidate labels already present in lagrangians.pkl, or generate/update the catalog first."
    )
