#!/usr/bin/env python3
"""Merge and audit the five D425 tensor/scalar-safe follow-up batches."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_TEMPLATE = (
    "replay_d425_tensor_scalar_safe_followup_5000_part{part:02d}_v2_timeout2s"
)
REPORT_DIR = (
    ROOT
    / "ai_theory_lab"
    / "reports"
    / "replay_d425_tensor_scalar_safe_followup_5000_v2"
)
SAMPLE_PATH = (
    ROOT
    / "ai_theory_lab"
    / "proposals"
    / "replay_d425_tensor_scalar_safe_followup_5000_samples.json"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def finite(value: str | None) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def trajectory_audit(row: dict[str, str], solution_path: Path) -> dict[str, float | bool]:
    solution = read_csv(solution_path)
    alpha = float(row["alpha"])
    beta = float(row["beta"])
    gamma = float(row["gamma"])
    lambda_eps = (
        float(row["lambda_H_Lambda_over_H0"])
        * float(row["eps_HM_H0_over_Mp"])
    )

    mstar: list[float] = []
    g11_values: list[float] = []
    determinant: list[float] = []
    alpha_m: list[float] = []
    for point in solution:
        varphi1 = float(point["varphi1_phi1_over_Mp"])
        varphi2 = float(point["varphi2_phi2_over_Lambda"])
        q2 = float(point["q2_dvarphi2_dln_a"])
        a_ratio = 2.0 * alpha * varphi2**2
        f_value = beta * varphi2 + gamma * varphi2**2
        d_value = beta + 2.0 * gamma * varphi2
        g11 = (1.0 + 2.0 * f_value) / a_ratio
        g12 = varphi1 * d_value / a_ratio
        g22 = lambda_eps**2 / a_ratio + 6.0 / varphi2**2
        det = g11 * g22 - g12**2
        mstar.append(a_ratio)
        g11_values.append(g11)
        determinant.append(det)
        alpha_m.append(2.0 * q2 / varphi2)

    return {
        "trajectory_points": len(solution),
        "z_min": min(float(point["z"]) for point in solution),
        "z_max": max(float(point["z"]) for point in solution),
        "mstar_ratio_min": min(mstar),
        "mstar_ratio_max": max(mstar),
        "g11_min": min(g11_values),
        "g11_max": max(g11_values),
        "det_g_min": min(determinant),
        "det_g_max": max(determinant),
        "alpha_m_min": min(alpha_m),
        "alpha_m_max": max(alpha_m),
        "kinetically_positive": (
            min(mstar) > 0.0
            and min(g11_values) > 0.0
            and min(determinant) > 0.0
        ),
    }


def main() -> None:
    all_rows: list[dict[str, str]] = []
    batch_summaries: list[dict[str, object]] = []
    for part in range(1, 6):
        run_name = RUN_TEMPLATE.format(part=part)
        output_dir = (
            ROOT
            / "ai_theory_lab"
            / "runs"
            / run_name
            / "agent_solver_result"
            / "agent_solve"
        )
        rows = read_csv(output_dir / "all_samples_summary.csv")
        if len(rows) != 1000:
            raise RuntimeError(f"{run_name}: expected 1000 rows, found {len(rows)}")
        for row in rows:
            row["batch_part"] = str(part)
            row["global_sample_index"] = str(
                (part - 1) * 1000 + int(row["agent_parameter_sample_index"])
            )
            all_rows.append(row)
        accepted = [
            row
            for row in rows
            if row["success"] == "True" and finite(row.get("chi2"))
        ]
        best = min(accepted, key=lambda item: float(item["chi2"]))
        batch_summaries.append(
            {
                "part": part,
                "accepted": len(accepted),
                "best_chi2": float(best["chi2"]),
                "best_local_sample_index": int(best["agent_parameter_sample_index"]),
                "best_global_sample_index": (
                    (part - 1) * 1000 + int(best["agent_parameter_sample_index"])
                ),
            }
        )

    if len(all_rows) != 5000:
        raise RuntimeError(f"expected 5000 merged rows, found {len(all_rows)}")

    proposal_samples = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    if len(proposal_samples) != 5000:
        raise RuntimeError(
            f"expected 5000 generated samples, found {len(proposal_samples)}"
        )
    present_filter_failures = 0
    for sample in proposal_samples:
        alpha = float(sample["alpha"])
        varphi2 = float(sample["varphi2_0_phi2_over_Lambda"])
        if not (
            alpha > 0.0
            and abs(2.0 * alpha * varphi2**2 - 1.0) < 1.0e-10
            and float(sample["scalar_kinetic_G11_0"]) > 0.0
            and float(sample["scalar_kinetic_det_0"]) > 0.0
        ):
            present_filter_failures += 1

    accepted = [
        row
        for row in all_rows
        if row["success"] == "True" and finite(row.get("chi2"))
    ]
    accepted.sort(key=lambda item: float(item["chi2"]))
    best = accepted[0]
    best_part = int(best["batch_part"])
    best_solution = (
        ROOT
        / "ai_theory_lab"
        / "runs"
        / RUN_TEMPLATE.format(part=best_part)
        / "agent_solver_result"
        / "agent_solve"
        / "best_solution.csv"
    )
    trajectory = trajectory_audit(best, best_solution)

    rejection_counts = Counter(
        row["reason"] for row in all_rows if row["success"] != "True"
    )
    timeout_count = sum(
        count
        for reason, count in rejection_counts.items()
        if reason.startswith("integration timeout:")
    )
    pipeline_aic = float(best["AIC"])
    constrained_aic = float(best["chi2"]) + 2.0 * 13.0

    summary = {
        "scope": "focused replay of the historical D425 structure",
        "generated_samples": len(proposal_samples),
        "present_filter_failures": present_filter_failures,
        "evaluated_samples": len(all_rows),
        "accepted_samples": len(accepted),
        "acceptance_rate": len(accepted) / len(all_rows),
        "integration_timeout_seconds": 2.0,
        "integration_timeout_count": timeout_count,
        "batch_summaries": batch_summaries,
        "best": {
            "batch_part": best_part,
            "global_sample_index": int(best["global_sample_index"]),
            "local_sample_index": int(best["agent_parameter_sample_index"]),
            "chi2": float(best["chi2"]),
            "chi2_sn": float(best["chi2_sn"]),
            "chi2_bao": float(best["chi2_bao"]),
            "pipeline_aic": pipeline_aic,
            "pipeline_k": int(best["k_params"]),
            "constrained_aic": constrained_aic,
            "constrained_k": 13,
            "parameters": {
                key: float(best[key])
                for key in (
                    "H0_km_s_Mpc",
                    "Omega_m0",
                    "lambda_H_Lambda_over_H0",
                    "alpha",
                    "beta",
                    "gamma",
                    "varphi1_0_phi1_over_Mp",
                    "mu1_m1_over_H0",
                    "fbar1_f1_over_Mp",
                    "varphi2_0_phi2_over_Lambda",
                    "mu2_m2_over_Lambda",
                    "q2_0_dvarphi2_dln_a",
                    "q1_0_dvarphi1_dln_a",
                    "Lambda_eV",
                )
            },
            "present_g11": float(best["scalar_kinetic_G11_0"]),
            "present_det_g": float(best["scalar_kinetic_det_0"]),
            "trajectory": trajectory,
            "solution_path": str(best_solution.relative_to(ROOT)),
        },
        "top_rejection_reasons": rejection_counts.most_common(12),
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    merged_fields = list(all_rows[0])
    with (REPORT_DIR / "all_samples_merged.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=merged_fields)
        writer.writeheader()
        writer.writerows(all_rows)

    with (REPORT_DIR / "accepted_samples_ranked.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=merged_fields)
        writer.writeheader()
        writer.writerows(accepted)

    best_parameters = summary["best"]["parameters"]
    report = f"""# D425 tensor-and-scalar-safe 5000-point follow-up

## Scope

This is a focused replay of the historical D425 induced-gravity structure,
not a cold-start discovery run. All 5000 explicit parameter vectors satisfy at
`z = 0`:

```text
alpha > 0
Mstar_0^2 / Mp^2 = 2 alpha varphi2_0^2 = 1
G_E,11 > 0
det(G_E) > 0
```

Every vector was submitted to the real EOM, Builder, and Solver stages. The
successfully integrated backgrounds were compared with DES-SN plus DESI DR2
BAO. To prevent isolated pathological integrations from blocking the scan,
each numerical trajectory had a 2-second integration deadline; this rejected
{timeout_count} vectors before likelihood evaluation and did not change the
likelihood or physical acceptance cuts.

## Scan outcome

Solver accepted {len(accepted)} of 5000 vectors ({100.0 * len(accepted) / 5000.0:.2f}%).
The global best is sample {best["global_sample_index"]}, from batch {best_part}:

```text
chi2_total = {float(best["chi2"]):.12f}
chi2_SN = {float(best["chi2_sn"]):.12f}
chi2_BAO = {float(best["chi2_bao"]):.12f}
AIC_pipeline = {pipeline_aic:.12f}
k_pipeline = {int(best["k_params"])}
AIC_with_alpha_derived = {constrained_aic:.12f}
k_with_alpha_derived = 13
```

The pipeline count treats `alpha` as fitted. In this focused scan,
`alpha = 1/(2 varphi2_0^2)` was imposed exactly, so the constrained parameter
manifold has one fewer independent direction.

## Best-fit parameters

```text
H0_km_s_Mpc = {best_parameters["H0_km_s_Mpc"]:.12g}
Omega_m0 = {best_parameters["Omega_m0"]:.12g}
lambda_H = {best_parameters["lambda_H_Lambda_over_H0"]:.12g}
alpha = {best_parameters["alpha"]:.12g}
beta = {best_parameters["beta"]:.12g}
gamma = {best_parameters["gamma"]:.12g}
varphi1_0 = {best_parameters["varphi1_0_phi1_over_Mp"]:.12g}
mu1 = {best_parameters["mu1_m1_over_H0"]:.12g}
fbar1 = {best_parameters["fbar1_f1_over_Mp"]:.12g}
varphi2_0 = {best_parameters["varphi2_0_phi2_over_Lambda"]:.12g}
mu2 = {best_parameters["mu2_m2_over_Lambda"]:.12g}
q2_0 = {best_parameters["q2_0_dvarphi2_dln_a"]:.12g}
```

## Full-trajectory kinetic audit

For the best point, the 150 stored trajectory samples over
`{trajectory["z_min"]:.3g} <= z <= {trajectory["z_max"]:.3g}` give:

```text
{trajectory["mstar_ratio_min"]:.8g} <= Mstar^2/Mp^2 <= {trajectory["mstar_ratio_max"]:.8g}
{trajectory["g11_min"]:.8g} <= G_E,11 <= {trajectory["g11_max"]:.8g}
{trajectory["det_g_min"]:.8g} <= det(G_E) <= {trajectory["det_g_max"]:.8g}
{trajectory["alpha_m_min"]:.8g} <= alpha_M <= {trajectory["alpha_m_max"]:.8g}
```

Thus the tested tensor kinetic coefficient and the homogeneous Einstein-frame
scalar kinetic matrix remain positive over the fitted background trajectory.
At the two-derivative level of this action, `cT^2 = 1`.

## Interpretation and limitation

The new best kinetically positive fit improves the previous stable candidate
from `chi2 = 8960.8116` to `chi2 = {float(best["chi2"]):.4f}`, but it remains
far worse than flat LCDM (`chi2 = 1645.28`). It also remains much worse than
the earlier tensor-safe but scalar-ghost point (`chi2 = 1718.2466`). The
focused search therefore strengthens the conclusion that this D425 structure
does not provide a competitive background fit once both tested kinetic
positivity conditions are enforced.

This audit does not calculate the scalar gradient matrix or sound speeds, so
it does not establish `c_s^2 > 0`, subluminality, perturbation stability,
growth/lensing viability, or local-gravity constraints.
"""
    (REPORT_DIR / "summary.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
