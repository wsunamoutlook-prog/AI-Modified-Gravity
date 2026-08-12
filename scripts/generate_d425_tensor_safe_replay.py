#!/usr/bin/env python3
"""Build a reproducible tensor-safe replay scan for the historical D425 theory."""

from __future__ import annotations

import argparse
import copy
import json
import math
import random
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


DEFAULT_SOURCE = Path(
    "cluster_report/cmp2000_cheap_partial_v1_full/proposals/"
    "cmp2000_deepseek_ali_v4_pro_cheap_v1/"
    "task_000425_expanded_refine_slot_08_lag_1.json"
)
DEFAULT_OUTPUT = Path("ai_theory_lab/proposals/replay_d425_tensor_safe_5000.json")
DEFAULT_PARAMETER_OUTPUT = Path(
    "ai_theory_lab/proposals/replay_d425_tensor_safe_5000_samples.json"
)
DEFAULT_SOURCE_PKL = Path(
    "ai_theory_lab/proposals/replay_d425_tensor_safe_5000_source.pkl"
)

D425_OPERATORS = (
    "phi2 * phi2 * R",
    "phi1 * Box(phi1) * phi2",
    "phi1 * Box(phi1) * phi2 * phi2",
)
D425_OPERATOR_LABELS = (
    "φ2 · φ2 · R",
    "φ1 · ∇^{a}∇_{a}φ1 · φ2",
    "φ1 · ∇^{a}∇_{a}φ1 · φ2 · φ2",
)


def _set_coefficient(sample: dict[str, float], name: str, value: float) -> None:
    sample[name] = float(value)
    sample[f"\\{name}"] = float(value)


def _log_jitter(rng: random.Random, value: float, sigma: float) -> float:
    return float(value) * 10.0 ** rng.gauss(0.0, sigma)


def _normalized_sample(
    sample: dict[str, float],
    rng: random.Random,
    *,
    mode_code: float,
    alpha_m_limit: float,
) -> dict[str, float]:
    result = copy.deepcopy(sample)
    varphi2 = float(result["varphi2_0_phi2_over_Lambda"])
    if abs(varphi2) < 1.0e-8:
        varphi2 = math.copysign(1.0e-8, varphi2 or 1.0)
        result["varphi2_0_phi2_over_Lambda"] = varphi2

    # M_*^2/M_p^2 = 2 alpha (phi_2/Lambda)^2 = 1 at z=0.
    _set_coefficient(result, "alpha", 1.0 / (2.0 * varphi2 * varphi2))
    alpha_m0 = rng.uniform(-alpha_m_limit, alpha_m_limit)
    result["q2_0_dvarphi2_dln_a"] = 0.5 * alpha_m0 * varphi2
    result["tensor_scan_mode_code"] = mode_code
    result["tensor_alpha_M0_target"] = alpha_m0
    return result


def _focused_sample(
    anchor: dict[str, float], rng: random.Random, mode_code: float
) -> dict[str, float]:
    result = copy.deepcopy(anchor)
    result["H0_km_s_Mpc"] = min(74.0, max(58.0, rng.gauss(67.0, 2.5)))
    result["Omega_m0"] = min(0.40, max(0.22, rng.gauss(0.32, 0.035)))

    for key, sigma in (
        ("lambda_H_Lambda_over_H0", 0.25),
        ("varphi1_0_phi1_over_Mp", 0.18),
        ("mu1_m1_over_H0", 0.22),
        ("fbar1_f1_over_Mp", 0.22),
        ("mu2_m2_over_Lambda", 0.35),
        ("fbar2_f2_over_Lambda", 0.30),
    ):
        result[key] = _log_jitter(rng, float(anchor[key]), sigma)

    sign = -1.0 if rng.random() < 0.5 else 1.0
    varphi2 = sign * 10.0 ** rng.uniform(-3.0, -1.0)
    result["varphi2_0_phi2_over_Lambda"] = varphi2

    for name, preserve_probability in (("beta", 0.75), ("gamma", 0.75)):
        anchor_value = float(anchor[name])
        sign_value = math.copysign(1.0, anchor_value)
        if rng.random() > preserve_probability:
            sign_value *= -1.0
        _set_coefficient(
            result,
            name,
            sign_value * _log_jitter(rng, abs(anchor_value), 0.75),
        )

    return _normalized_sample(
        result,
        rng,
        mode_code=mode_code,
        alpha_m_limit=0.10,
    )


def build_samples(source_samples: list[dict[str, float]], seed: int) -> list[dict[str, float]]:
    rng = random.Random(seed)
    positive = [s for s in source_samples if float(s["alpha"]) > 0.0]
    if len(positive) < 2500:
        raise ValueError(f"expected at least 2500 alpha-positive samples, found {len(positive)}")

    broad = []
    for sample in rng.sample(positive, 2500):
        result = copy.deepcopy(sample)
        result["tensor_scan_mode_code"] = 0.0
        result["tensor_alpha_M0_target"] = 999.0
        broad.append(result)

    normalized_replay = [
        _normalized_sample(
            sample,
            rng,
            mode_code=1.0,
            alpha_m_limit=0.20,
        )
        for sample in rng.sample(source_samples, 1500)
    ]

    historical_anchor = min(
        source_samples,
        key=lambda s: abs(float(s["alpha"]) + 7250.559597746297),
    )
    normalized_focused = [
        _focused_sample(historical_anchor, rng, mode_code=2.0) for _ in range(1000)
    ]
    samples = broad + normalized_replay + normalized_focused
    rng.shuffle(samples)
    return samples


def build_token_level_source(path: Path) -> None:
    """Compile D425 from the legal cached token pool, without catalog replay."""
    from ai_theory_lab.cold_start_runner import (
        _build_token_level_context,
        _candidate_label,
        _direct_entry,
        _write_token_level_source,
    )

    context = _build_token_level_context(timeout_seconds=0, use_cache=True)
    candidates = list(context["masker"].all_candidates)
    by_label = {_candidate_label(candidate): candidate for candidate in candidates}
    missing = [label for label in D425_OPERATOR_LABELS if label not in by_label]
    if missing:
        raise KeyError(f"D425 operators missing from token cache: {missing}")

    entry = _direct_entry(
        tensors=context["tensors"],
        scalar_config="both",
        potential_types={"phi1": "axion", "phi2": "quadratic"},
        candidates=[by_label[label] for label in D425_OPERATOR_LABELS],
        local_number=1,
    )
    expected = list(D425_OPERATOR_LABELS)
    if entry["operators"] != expected:
        raise AssertionError(
            f"unexpected compiled operator order: {entry['operators']} != {expected}"
        )
    if entry["coefficient_symbols"] != ["\\alpha", "\\beta", "\\gamma"]:
        raise AssertionError(
            f"unexpected coefficient order: {entry['coefficient_symbols']}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_token_level_source(entry, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--parameter-output", type=Path, default=DEFAULT_PARAMETER_OUTPUT
    )
    parser.add_argument("--source-pkl", type=Path, default=DEFAULT_SOURCE_PKL)
    parser.add_argument("--seed", type=int, default=4252026)
    args = parser.parse_args()

    source = json.loads(args.source.read_text())
    samples = build_samples(source["parameter_samples"], args.seed)
    proposal = {
        "proposal_id": "replay_d425_tensor_safe_5000",
        "theory": source["theory"],
        "parameter_samples": samples,
        "rationale": (
            "Historical D425 replay with 2500 broad alpha-positive samples, "
            "1500 present-Planck-normalized replay samples, and 1000 focused "
            "present-Planck-normalized samples."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(proposal, indent=2, ensure_ascii=False) + "\n")
    args.parameter_output.parent.mkdir(parents=True, exist_ok=True)
    args.parameter_output.write_text(
        json.dumps(samples, indent=2, ensure_ascii=False) + "\n"
    )
    build_token_level_source(args.source_pkl)

    mode_counts: dict[int, int] = {}
    for sample in samples:
        mode = int(sample["tensor_scan_mode_code"])
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
        if float(sample["alpha"]) <= 0.0:
            raise AssertionError("tensor-safe scan contains alpha <= 0")
        if mode in (1, 2):
            ratio = (
                2.0
                * float(sample["alpha"])
                * float(sample["varphi2_0_phi2_over_Lambda"]) ** 2
            )
            if not math.isclose(ratio, 1.0, rel_tol=1.0e-12, abs_tol=1.0e-12):
                raise AssertionError(f"normalized sample has Mstar ratio {ratio}")

    print(args.output)
    print(args.parameter_output)
    print(args.source_pkl)
    print(f"samples={len(samples)} modes={mode_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
