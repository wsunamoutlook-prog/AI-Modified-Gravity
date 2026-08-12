#!/usr/bin/env python3
"""Generate a D425 follow-up scan with positive tensor/scalar kinetics at z=0."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import math
import random
from pathlib import Path


DEFAULT_HISTORICAL = Path(
    "cluster_report/cmp2000_cheap_partial_v1_full/proposals/"
    "cmp2000_deepseek_ali_v4_pro_cheap_v1/"
    "task_000425_expanded_refine_slot_08_lag_1.json"
)
DEFAULT_PREVIOUS = Path(
    "ai_theory_lab/proposals/replay_d425_tensor_safe_5000.json"
)
DEFAULT_PREVIOUS_RANKING = Path(
    "ai_theory_lab/runs/replay_d425_tensor_safe_5000_v3/"
    "agent_solver_result/agent_solve/model_ranking.csv"
)
DEFAULT_OUTPUT = Path(
    "ai_theory_lab/proposals/replay_d425_tensor_scalar_safe_followup_5000.json"
)
DEFAULT_PARAMETER_OUTPUT = Path(
    "ai_theory_lab/proposals/"
    "replay_d425_tensor_scalar_safe_followup_5000_samples.json"
)


def _set_coefficient(sample: dict[str, float], name: str, value: float) -> None:
    sample[name] = float(value)
    sample[f"\\{name}"] = float(value)


def _log_jitter(rng: random.Random, value: float, sigma: float) -> float:
    return float(value) * 10.0 ** rng.gauss(0.0, sigma)


def _jitter_background(
    sample: dict[str, float], rng: random.Random, strength: float
) -> dict[str, float]:
    result = copy.deepcopy(sample)
    result["H0_km_s_Mpc"] = min(
        74.0,
        max(58.0, rng.gauss(float(sample["H0_km_s_Mpc"]), 2.0 * strength)),
    )
    result["Omega_m0"] = min(
        0.40,
        max(0.22, rng.gauss(float(sample["Omega_m0"]), 0.025 * strength)),
    )
    for key, sigma in (
        ("lambda_H_Lambda_over_H0", 0.20),
        ("varphi1_0_phi1_over_Mp", 0.14),
        ("mu1_m1_over_H0", 0.18),
        ("fbar1_f1_over_Mp", 0.18),
        ("mu2_m2_over_Lambda", 0.25),
        ("fbar2_f2_over_Lambda", 0.22),
    ):
        result[key] = _log_jitter(rng, float(sample[key]), sigma * strength)

    old_v2 = float(sample["varphi2_0_phi2_over_Lambda"])
    sign = math.copysign(1.0, old_v2 or (-1.0 if rng.random() < 0.5 else 1.0))
    if rng.random() < 0.15:
        sign *= -1.0
    magnitude = min(1.0e-1, max(1.0e-5, _log_jitter(rng, abs(old_v2), 0.25 * strength)))
    result["varphi2_0_phi2_over_Lambda"] = sign * magnitude
    return result


def _draw_f0(rng: random.Random, regime: str, historical_f0: float) -> float:
    if regime == "historical_large":
        center = max(1.0e2, abs(historical_f0))
        return min(1.0e7, max(1.0e1, _log_jitter(rng, center, 0.85)))
    if regime == "large":
        return 10.0 ** rng.uniform(1.0, 6.5)
    if regime == "moderate":
        return 10.0 ** rng.uniform(-2.0, 2.0)
    if regime == "near_zero":
        return rng.uniform(-0.45, 1.0)
    raise ValueError(f"unknown F0 regime: {regime}")


def _stabilize(
    sample: dict[str, float],
    rng: random.Random,
    *,
    mode_code: float,
    regime: str,
    historical_f0: float,
    alpha_m_limit: float,
) -> dict[str, float]:
    result = copy.deepcopy(sample)
    v1 = float(result["varphi1_0_phi1_over_Mp"])
    v2 = float(result["varphi2_0_phi2_over_Lambda"])
    if abs(v1) < 1.0e-4:
        v1 = math.copysign(1.0e-4, v1 or 1.0)
        result["varphi1_0_phi1_over_Mp"] = v1
    if abs(v2) < 1.0e-5:
        v2 = math.copysign(1.0e-5, v2 or 1.0)
        result["varphi2_0_phi2_over_Lambda"] = v2

    # Exact present-day tensor normalization: Mstar_0^2 / Mp^2 = 1.
    alpha = 1.0 / (2.0 * v2 * v2)
    _set_coefficient(result, "alpha", alpha)

    # Parameterize the integration-by-parts kinetic sector by
    # F0 = beta*v2 + gamma*v2^2 and D0 = beta + 2*gamma*v2.
    # With A0 = 2*alpha*v2^2 = 1, positivity requires
    # 1+2F0 > 0 and |v1*D0| < sqrt(6(1+2F0))/|v2|.
    f0 = _draw_f0(rng, regime, historical_f0)
    base = 1.0 + 2.0 * f0
    if base <= 0.0:
        raise AssertionError(f"non-positive scalar kinetic diagonal: {base}")
    dmax = math.sqrt(6.0 * base) / abs(v1 * v2)
    if rng.random() < 0.70:
        d_fraction = rng.uniform(-0.35, 0.35)
    else:
        d_fraction = rng.uniform(-0.88, 0.88)
    d0 = d_fraction * dmax
    gamma = (d0 * v2 - f0) / (v2 * v2)
    beta = (2.0 * f0 - d0 * v2) / v2
    _set_coefficient(result, "beta", beta)
    _set_coefficient(result, "gamma", gamma)

    alpha_m0 = rng.uniform(-alpha_m_limit, alpha_m_limit)
    result["q2_0_dvarphi2_dln_a"] = 0.5 * alpha_m0 * v2
    result["tensor_scan_mode_code"] = mode_code
    result["tensor_alpha_M0_target"] = alpha_m0
    result["scalar_kinetic_F0_target"] = f0
    result["scalar_kinetic_D_fraction_target"] = d_fraction

    lambda_h = float(result["lambda_H_Lambda_over_H0"])
    # Historical proposal JSON predates explicit eps_HM provenance. Omitting
    # its tiny positive contribution here is conservative for the determinant.
    eps_hm = float(result.get("eps_HM_H0_over_Mp", 0.0))
    a0 = 2.0 * alpha * v2 * v2
    g11 = base / a0
    g12 = v1 * d0 / a0
    g22 = (lambda_h * eps_hm) ** 2 / a0 + 6.0 / (v2 * v2)
    det = g11 * g22 - g12 * g12
    result["scalar_kinetic_G11_0"] = g11
    result["scalar_kinetic_det_0"] = det
    if not (a0 > 0.0 and g11 > 0.0 and det > 0.0):
        raise AssertionError((a0, g11, det))
    return result


def _ranking_anchor(
    previous_samples: list[dict[str, float]], ranking_path: Path
) -> dict[str, float]:
    ranking = next(csv.DictReader(ranking_path.open()))
    index = int(float(ranking["agent_parameter_sample_index"])) - 1
    return copy.deepcopy(previous_samples[index])


def build_samples(
    historical_samples: list[dict[str, float]],
    previous_samples: list[dict[str, float]],
    tensor_best: dict[str, float],
    seed: int,
) -> list[dict[str, float]]:
    rng = random.Random(seed)
    historical_anchor = min(
        historical_samples,
        key=lambda s: abs(float(s["alpha"]) + 7250.559597746297),
    )
    historical_f0 = (
        float(historical_anchor["beta"])
        * float(historical_anchor["varphi2_0_phi2_over_Lambda"])
        + float(historical_anchor["gamma"])
        * float(historical_anchor["varphi2_0_phi2_over_Lambda"]) ** 2
    )

    samples: list[dict[str, float]] = []

    regimes = ("near_zero", "moderate", "large", "historical_large")
    for _ in range(2000):
        base = _jitter_background(rng.choice(historical_samples), rng, 0.45)
        samples.append(
            _stabilize(
                base,
                rng,
                mode_code=3.0,
                regime=rng.choice(regimes),
                historical_f0=historical_f0,
                alpha_m_limit=0.50,
            )
        )

    for _ in range(1500):
        base = _jitter_background(historical_anchor, rng, 0.80)
        samples.append(
            _stabilize(
                base,
                rng,
                mode_code=4.0,
                regime="historical_large" if rng.random() < 0.7 else "large",
                historical_f0=historical_f0,
                alpha_m_limit=2.0,
            )
        )

    for _ in range(1000):
        base = _jitter_background(tensor_best, rng, 0.75)
        samples.append(
            _stabilize(
                base,
                rng,
                mode_code=5.0,
                regime=rng.choice(("moderate", "large", "historical_large")),
                historical_f0=historical_f0,
                alpha_m_limit=0.50,
            )
        )

    for _ in range(500):
        base = _jitter_background(rng.choice(previous_samples), rng, 0.30)
        samples.append(
            _stabilize(
                base,
                rng,
                mode_code=6.0,
                regime=rng.choice(("near_zero", "moderate")),
                historical_f0=historical_f0,
                alpha_m_limit=0.15,
            )
        )

    rng.shuffle(samples)
    return samples


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--historical", type=Path, default=DEFAULT_HISTORICAL)
    parser.add_argument("--previous", type=Path, default=DEFAULT_PREVIOUS)
    parser.add_argument(
        "--previous-ranking", type=Path, default=DEFAULT_PREVIOUS_RANKING
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--parameter-output", type=Path, default=DEFAULT_PARAMETER_OUTPUT
    )
    parser.add_argument("--seed", type=int, default=4255001)
    args = parser.parse_args()

    historical = json.loads(args.historical.read_text())
    previous = json.loads(args.previous.read_text())
    tensor_best = _ranking_anchor(previous["parameter_samples"], args.previous_ranking)
    samples = build_samples(
        historical["parameter_samples"],
        previous["parameter_samples"],
        tensor_best,
        args.seed,
    )
    proposal = {
        "proposal_id": "replay_d425_tensor_scalar_safe_followup_5000",
        "theory": historical["theory"],
        "parameter_samples": samples,
        "rationale": (
            "D425 replay with exact present tensor normalization and analytic "
            "positive-definite Einstein-frame scalar kinetic matrix at z=0."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(proposal, indent=2, ensure_ascii=False) + "\n")
    args.parameter_output.write_text(
        json.dumps(samples, indent=2, ensure_ascii=False) + "\n"
    )
    print(args.output)
    print(args.parameter_output)
    print(f"samples={len(samples)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
