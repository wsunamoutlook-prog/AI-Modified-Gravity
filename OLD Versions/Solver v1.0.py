#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_modified_gravity_bao_all_in_one.py
======================================

One-file numerical FLRW solver + random sampler for a ghost-free modified-GR
background model, using H(z) data from the screenshots in this conversation.

This script is intentionally self-contained:
  1. It defines the data arrays.
  2. It defines one concrete ghost-free final EOM model from the user's
     EOM summary: Lagrangian #523 after ghost-free reduction.
  3. It nondimensionalizes the system with x = ln a, h = H/H0,
     varphi = phi/Mp, q = d varphi / d ln a.
  4. It randomly samples all relevant free parameters within explicit priors.
  5. It solves the IVP numerically.
  6. It writes a text report and CSV outputs in the current directory.

Important physics conventions
-----------------------------
Natural units are used internally, but the solver does NOT directly put
M_p ~ 10^27 eV and H0 ~ 10^-33 eV inside the ODE.  Instead:

    H       = H0 * h(x)
    phi     = Mpred * varphi(x)
    q       = d varphi / dx
    m       = H0 * mu
    rho_m0  = Mpred^2 * H0^2 * rho_m0_bar
    rho_m0_bar = 3 Omega_m0

where x = ln a = -ln(1+z).  The output h and varphi are dimensionless.
Physical units are restored only when computing H_model = H0[km/s/Mpc] * h.

Model used here: ghost-free final EOM of Lagrangian #523
--------------------------------------------------------
Original reduced final EOM, including dust:

E_N = -rho_m0 + (6 Mp^4 gamma a adot^2
                 - 1/2 Mp^2 m^2 a^3 phi^2
                 - 1/2 Mp^2 a^3 phidot^2
                 + epsilon a^3 phi^2 phidot^2)/Mp^2 = 0

E_a = (12 Mp^4 gamma a addot + 6 Mp^4 gamma adot^2
       - 3/2 Mp^2 m^2 a^2 phi^2
       + 3/2 Mp^2 a^2 phidot^2
       - 3 epsilon a^2 phi^2 phidot^2)/Mp^2 = 0

E_phi = (-Mp^2 m^2 a^3 phi - Mp^2 a^3 phiddot
         - 3 Mp^2 a^2 adot phidot
         + 2 epsilon a^3 phi^2 phiddot
         + 2 epsilon a^3 phi phidot^2
         + 6 epsilon a^2 phi^2 adot phidot)/Mp^2 = 0

After nondimensionalization, the system is:

Constraint:
    C = 6 gamma h^2
        - 0.5 mu^2 varphi^2
        - 0.5 h^2 q^2
        + epsilon varphi^2 h^2 q^2
        - rho_m0_bar exp(-3x) = 0

Evolution:
    dh/dx = h_x from E_a = 0
    dvarphi/dx = q
    dq/dx = q_x from E_phi = 0

This script does not assume LambdaCDM in the solver.  A flat-LambdaCDM fit is
computed only as a reference benchmark in the report.

Limitations
-----------
The BAO H(z) data embedded below are the H(z)-style points shown in the user's
screenshots (BOSS/eBOSS/Lyman-alpha-style table).  This is not a full DESI BAO
likelihood with D_M/r_d, D_H/r_d, D_V/r_d and covariance.  To use real DESI BAO
properly, replace the likelihood block with the published DESI distance data and
covariance matrix.
"""

from __future__ import annotations

import csv
import math
import os
import time
import warnings
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import differential_evolution

# -----------------------------------------------------------------------------
# User-editable configuration
# -----------------------------------------------------------------------------

# Choose: "bao", "cc", or "combined".
DATA_CHOICE = "bao"

# Random sampling settings. Increase N_SAMPLES for a better random search.
N_SAMPLES = 10000
RANDOM_SEED = 123

# Numerical solver tolerances.
RTOL = 1e-8
ATOL = 1e-10
N_GRID = 500
MAX_ABS_CONSTRAINT = 1e-4

# Output files. They are written to the directory from which you run the script.
REPORT_TXT = "modified_gravity_fit_report.txt"
BEST_SOLUTION_CSV = "best_solution.csv"
ACCEPTED_SAMPLES_CSV = "accepted_samples_summary.csv"
BEST_FIT_PNG = "best_fit_Hz.png"

# Priors for the model.  These are intentionally not LambdaCDM priors.
# They are broad enough to allow the scalar/MG sector to supply the missing
# expansion budget while avoiding absurd values.
PRIORS = {
    "H0_km_s_Mpc": (60.0, 75.0),          # physical H0 scale for H(z) comparison
    "Omega_m0": (0.15, 0.45),             # matter sector only; no Omega_Lambda
    "gamma": (0.45, 0.55),                # EH coefficient; standard is gamma=0.5
    "varphi0": (-5.0, 5.0),               # phi0/Mp; allows mild super-Planckian values
    "log10_mu": (-3.0, 1.0),              # mu = m/H0
    "log10_abs_epsilon": (-6.0, 0.0),     # epsilon = sign * 10^u
}

# Hard sanity cuts.  These are not priors; they reject clearly unstable solutions.
MAX_ABS_Q0 = 10.0
MAX_ABS_VARPHI_TRAJ = 20.0
MAX_ABS_Q_TRAJ = 30.0
MAX_H_KM_S_MPC = 1000.0

# Physical constants for unit restoration/explanation.
M_P_REDUCED_EV = 2.435e27
KM_S_MPC_TO_EV = 2.133119e-35


# -----------------------------------------------------------------------------
# Data from the user's screenshots
# -----------------------------------------------------------------------------

# Cosmic chronometers: z, H(z), sigma_H [km/s/Mpc]
CC_DATA = np.array([
    [0.07,   69.0,  19.6],
    [0.09,   69.0,  12.0],
    [0.12,   68.6,  26.2],
    [0.17,   83.0,   8.0],
    [0.179,  75.0,   4.0],
    [0.199,  75.0,   5.0],
    [0.20,   72.9,  29.6],
    [0.27,   77.0,  14.0],
    [0.28,   88.8,  36.6],
    [0.352,  83.0,  14.0],
    [0.3802, 83.0,  13.5],
    [0.4,    95.0,  17.0],
    [0.4004, 77.0,  10.2],
    [0.4247, 87.1,  11.2],
    [0.4497, 92.8,  12.9],
    [0.47,   89.0,  49.6],
    [0.4783, 80.9,   9.0],
    [0.48,   97.0,  62.0],
    [0.593, 104.0,  13.0],
    [0.68,   92.0,   8.0],
    [0.75,   98.8,  33.6],
    [0.781, 105.0,  12.0],
    [0.8,   113.1,  25.22],
    [0.875, 125.0,  17.0],
    [0.88,   90.0,  40.0],
    [0.9,   117.0,  23.0],
    [1.037, 154.0,  20.0],
    [1.3,   168.0,  17.0],
    [1.363, 160.0,  33.6],
    [1.43,  177.0,  18.0],
    [1.53,  140.0,  14.0],
    [1.75,  202.0,  40.0],
    [1.965, 186.5,  50.4],
], dtype=float)

# BAO-style H(z) measurements from the screenshot: z, H(z), sigma_H [km/s/Mpc]
BAO_DATA = np.array([
    [0.38,  81.5,   1.9],
    [0.51,  90.4,   1.9],
    [0.61,  97.3,   2.1],
    [1.48, 153.81,  6.39],
    [2.33, 224.0,   8.0],
    [2.40, 226.0,   8.0],
], dtype=float)


def select_data(choice: str) -> np.ndarray:
    choice = choice.lower().strip()
    if choice == "bao":
        return BAO_DATA.copy()
    if choice == "cc":
        return CC_DATA.copy()
    if choice == "combined":
        return np.vstack([CC_DATA, BAO_DATA])
    raise ValueError("DATA_CHOICE must be 'bao', 'cc', or 'combined'.")


# -----------------------------------------------------------------------------
# Dimensionless model equations for Lagrangian #523
# -----------------------------------------------------------------------------

@dataclass
class Params:
    H0: float                 # km/s/Mpc
    Omega_m0: float
    rho_bar: float            # rho_m0/(Mp^2 H0^2) = 3 Omega_m0
    gamma: float              # EH coefficient; GR normalization is 0.5
    epsilon: float
    mu: float                 # m/H0
    varphi0: float            # phi0/Mp
    q0: float                 # dvarphi/dln a at x=0
    eps_HM: float             # H0_eV/Mp_eV


@dataclass
class FitResult:
    success: bool
    reason: str
    params: Optional[Params] = None
    chi2: Optional[float] = None
    chi2_per_point: Optional[float] = None
    max_abs_constraint: Optional[float] = None
    x_grid: Optional[np.ndarray] = None
    z_grid: Optional[np.ndarray] = None
    h_grid: Optional[np.ndarray] = None
    H_grid: Optional[np.ndarray] = None
    varphi_grid: Optional[np.ndarray] = None
    q_grid: Optional[np.ndarray] = None
    constraint_grid: Optional[np.ndarray] = None
    H_at_data: Optional[np.ndarray] = None


def constraint_C(x: float, h: float, varphi: float, q: float, p: Params) -> float:
    """Dimensionless Friedmann/Hamiltonian constraint C=0."""
    return (
        6.0 * p.gamma * h * h
        - 0.5 * p.mu * p.mu * varphi * varphi
        - 0.5 * h * h * q * q
        + p.epsilon * varphi * varphi * h * h * q * q
        - p.rho_bar * math.exp(-3.0 * x)
    )


def rhs_x(x: float, y: np.ndarray, p: Params) -> np.ndarray:
    """RHS for y=[h,varphi,q] using x=ln a as independent variable."""
    h, varphi, q = float(y[0]), float(y[1]), float(y[2])
    if not np.isfinite(h + varphi + q) or h <= 0.0:
        return np.array([np.nan, np.nan, np.nan])

    denom_h = 12.0 * p.gamma * h
    if abs(denom_h) < 1e-14:
        return np.array([np.nan, np.nan, np.nan])

    # E_a=0 solved for h_x = dh/dx.
    h_x = (
        -18.0 * p.gamma * h * h
        + 1.5 * p.mu * p.mu * varphi * varphi
        - 1.5 * h * h * q * q
        + 3.0 * p.epsilon * varphi * varphi * h * h * q * q
    ) / denom_h

    denom_q = (2.0 * p.epsilon * varphi * varphi - 1.0) * h * h
    if abs(denom_q) < 1e-10:
        return np.array([np.nan, np.nan, np.nan])

    # E_phi=0 solved for q_x = dq/dx.
    q_x = (
        h * h_x * q
        + 3.0 * h * h * q
        + p.mu * p.mu * varphi
        - 2.0 * p.epsilon * varphi * varphi * h * h_x * q
        - 2.0 * p.epsilon * varphi * h * h * q * q
        - 6.0 * p.epsilon * varphi * varphi * h * h * q
    ) / denom_q

    return np.array([h_x, q, q_x], dtype=float)


def draw_log_signed(rng: np.random.Generator, log10_low: float, log10_high: float) -> float:
    return float(rng.choice([-1.0, 1.0]) * 10.0 ** rng.uniform(log10_low, log10_high))


def draw_params_without_q0(rng: np.random.Generator) -> Dict[str, float]:
    """Draw all parameters except q0."""
    H0 = float(rng.uniform(*PRIORS["H0_km_s_Mpc"]))
    Omega_m0 = float(rng.uniform(*PRIORS["Omega_m0"]))
    gamma = float(rng.uniform(*PRIORS["gamma"]))
    # Draw epsilon and mu before varphi0; this ordering is deterministic for the fixed seed.
    epsilon = draw_log_signed(rng, *PRIORS["log10_abs_epsilon"])
    mu = float(10.0 ** rng.uniform(*PRIORS["log10_mu"]))
    varphi0 = float(rng.uniform(*PRIORS["varphi0"]))
    eps_HM = H0 * KM_S_MPC_TO_EV / M_P_REDUCED_EV
    return {
        "H0": H0,
        "Omega_m0": Omega_m0,
        "rho_bar": 3.0 * Omega_m0,
        "gamma": gamma,
        "epsilon": epsilon,
        "mu": mu,
        "varphi0": varphi0,
        "eps_HM": eps_HM,
    }


def solve_q0_from_constraint(d: Dict[str, float], rng: np.random.Generator) -> Optional[float]:
    """
    Solve C(x=0,h=1,varphi0,q0)=0 analytically for q0.

    Constraint at x=0:
        6 gamma - 0.5 mu^2 varphi0^2 - 0.5 q0^2
        + epsilon varphi0^2 q0^2 - rho_bar = 0.
    """
    varphi0 = d["varphi0"]
    A = d["epsilon"] * varphi0 * varphi0 - 0.5
    B = 6.0 * d["gamma"] - 0.5 * d["mu"] * d["mu"] * varphi0 * varphi0 - d["rho_bar"]
    if abs(A) < 1e-12:
        return None
    q2 = -B / A
    if not np.isfinite(q2) or q2 < 0.0:
        return None
    q_abs = math.sqrt(q2)
    if not np.isfinite(q_abs) or q_abs > MAX_ABS_Q0:
        return None
    return float(q_abs * rng.choice([-1.0, 1.0]))


def make_params(d: Dict[str, float], q0: float) -> Params:
    return Params(
        H0=d["H0"],
        Omega_m0=d["Omega_m0"],
        rho_bar=d["rho_bar"],
        gamma=d["gamma"],
        epsilon=d["epsilon"],
        mu=d["mu"],
        varphi0=d["varphi0"],
        q0=q0,
        eps_HM=d["eps_HM"],
    )


def solve_one(p: Params, data: np.ndarray) -> FitResult:
    z_data = data[:, 0]
    H_obs = data[:, 1]
    sigma = data[:, 2]
    x_data = -np.log1p(z_data)
    x_min = float(np.min(x_data))

    y0 = np.array([1.0, p.varphi0, p.q0], dtype=float)
    init_C = constraint_C(0.0, 1.0, p.varphi0, p.q0, p)
    if not np.isfinite(init_C) or abs(init_C) > 1e-6:
        return FitResult(False, f"initial constraint not satisfied: {init_C:.3e}", params=p)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sol = solve_ivp(
            fun=lambda x, y: rhs_x(x, y, p),
            t_span=(0.0, x_min),
            y0=y0,
            method="DOP853",
            dense_output=True,
            t_eval=np.linspace(0.0, x_min, N_GRID),
            rtol=RTOL,
            atol=ATOL,
        )

    if not sol.success:
        return FitResult(False, "ODE failed: " + str(sol.message), params=p)
    if sol.y.shape[0] != 3 or not np.all(np.isfinite(sol.y)):
        return FitResult(False, "ODE returned NaN/inf", params=p)

    h_grid = sol.y[0]
    varphi_grid = sol.y[1]
    q_grid = sol.y[2]
    if np.any(h_grid <= 0.0):
        return FitResult(False, "h<=0", params=p)
    if np.max(np.abs(varphi_grid)) > MAX_ABS_VARPHI_TRAJ:
        return FitResult(False, "|varphi| too large", params=p)
    if np.max(np.abs(q_grid)) > MAX_ABS_Q_TRAJ:
        return FitResult(False, "|q| too large", params=p)

    constraint_grid = np.array([
        constraint_C(float(x), float(h), float(v), float(q), p)
        for x, h, v, q in zip(sol.t, h_grid, varphi_grid, q_grid)
    ], dtype=float)
    if not np.all(np.isfinite(constraint_grid)):
        return FitResult(False, "constraint NaN/inf", params=p)
    max_abs_C = float(np.max(np.abs(constraint_grid)))
    if max_abs_C > MAX_ABS_CONSTRAINT:
        return FitResult(False, f"constraint drift {max_abs_C:.3e}", params=p)

    y_at_data = sol.sol(x_data)
    if y_at_data is None or not np.all(np.isfinite(y_at_data)):
        return FitResult(False, "dense output failed", params=p)
    h_at_data = y_at_data[0]
    H_model = p.H0 * h_at_data
    if np.any(H_model <= 0.0) or np.any(H_model > MAX_H_KM_S_MPC):
        return FitResult(False, "bad H_model", params=p)

    chi2 = float(np.sum(((H_model - H_obs) / sigma) ** 2))
    z_grid = np.exp(-sol.t) - 1.0
    H_grid = p.H0 * h_grid
    return FitResult(
        success=True,
        reason="accepted",
        params=p,
        chi2=chi2,
        chi2_per_point=chi2 / len(data),
        max_abs_constraint=max_abs_C,
        x_grid=sol.t,
        z_grid=z_grid,
        h_grid=h_grid,
        H_grid=H_grid,
        varphi_grid=varphi_grid,
        q_grid=q_grid,
        constraint_grid=constraint_grid,
        H_at_data=H_model,
    )


def run_random_search(data: np.ndarray) -> Tuple[Optional[FitResult], List[FitResult], Counter, float]:
    rng = np.random.default_rng(RANDOM_SEED)
    accepted: List[FitResult] = []
    rejected = Counter()
    t0 = time.time()

    for i in range(N_SAMPLES):
        d = draw_params_without_q0(rng)
        q0 = solve_q0_from_constraint(d, rng)
        if q0 is None:
            rejected["no real/acceptable q0 from constraint"] += 1
            continue
        p = make_params(d, q0)
        res = solve_one(p, data)
        if res.success:
            accepted.append(res)
        else:
            rejected[res.reason] += 1

    accepted.sort(key=lambda r: float("inf") if r.chi2 is None else r.chi2)
    elapsed = time.time() - t0
    best = accepted[0] if accepted else None
    return best, accepted, rejected, elapsed


# -----------------------------------------------------------------------------
# Reference flat LambdaCDM benchmark only; not used by the MG solver
# -----------------------------------------------------------------------------


def flat_lcdm_H(z: np.ndarray, H0: float, Om0: float) -> np.ndarray:
    return H0 * np.sqrt(Om0 * (1.0 + z) ** 3 + (1.0 - Om0))


def fit_reference_lcdm(data: np.ndarray) -> Tuple[float, float, float]:
    z = data[:, 0]
    Hobs = data[:, 1]
    sig = data[:, 2]

    def objective(theta: np.ndarray) -> float:
        H0, Om0 = theta
        if H0 <= 0 or Om0 <= 0 or Om0 >= 1:
            return 1e99
        Hm = flat_lcdm_H(z, H0, Om0)
        return float(np.sum(((Hm - Hobs) / sig) ** 2))

    res = differential_evolution(
        objective,
        bounds=[(50.0, 90.0), (0.05, 0.6)],
        seed=RANDOM_SEED,
        polish=True,
        tol=1e-8,
        updating="immediate",
        workers=1,
    )
    H0, Om0 = map(float, res.x)
    return H0, Om0, float(res.fun)


# -----------------------------------------------------------------------------
# Output helpers
# -----------------------------------------------------------------------------


def fmt(v: Optional[float], nd: int = 6) -> str:
    if v is None:
        return "None"
    if abs(v) >= 1e4 or (abs(v) > 0 and abs(v) < 1e-4):
        return f"{v:.{nd}e}"
    return f"{v:.{nd}f}"


def write_best_solution_csv(best: FitResult, path: str) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["z", "x_ln_a", "h_dimensionless", "H_km_s_Mpc", "varphi_phi_over_Mpred", "q_dvarphi_dln_a", "constraint_C"])
        # Sort by increasing z for readability.
        rows = list(zip(best.z_grid, best.x_grid, best.h_grid, best.H_grid, best.varphi_grid, best.q_grid, best.constraint_grid))
        rows.sort(key=lambda r: r[0])
        for row in rows:
            w.writerow([f"{float(v):.12e}" for v in row])


def write_accepted_samples_csv(accepted: List[FitResult], path: str, max_rows: int = 1000) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "chi2", "chi2_per_point", "max_abs_constraint", "H0", "Omega_m0", "rho_bar", "gamma", "epsilon", "mu", "varphi0", "q0", "eps_HM"])
        for i, r in enumerate(accepted[:max_rows], start=1):
            p = r.params
            assert p is not None
            w.writerow([
                i,
                r.chi2,
                r.chi2_per_point,
                r.max_abs_constraint,
                p.H0,
                p.Omega_m0,
                p.rho_bar,
                p.gamma,
                p.epsilon,
                p.mu,
                p.varphi0,
                p.q0,
                p.eps_HM,
            ])


def maybe_plot(best: FitResult, data: np.ndarray, path: str) -> bool:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return False

    z = data[:, 0]
    Hobs = data[:, 1]
    sig = data[:, 2]

    # Sort grid by z increasing for plotting.
    order = np.argsort(best.z_grid)
    z_grid = best.z_grid[order]
    H_grid = best.H_grid[order]

    plt.figure(figsize=(8, 5))
    plt.errorbar(z, Hobs, yerr=sig, fmt="o", label="data", capsize=3)
    plt.plot(z_grid, H_grid, label="best MG/scalar sample")
    plt.xlabel("z")
    plt.ylabel("H(z) [km/s/Mpc]")
    plt.title("Modified gravity numerical fit")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return True


def write_report(
    best: Optional[FitResult],
    accepted: List[FitResult],
    rejected: Counter,
    elapsed: float,
    data: np.ndarray,
    lcdm_ref: Tuple[float, float, float],
    plot_written: bool,
) -> None:
    H0_lcdm, Om_lcdm, chi2_lcdm = lcdm_ref
    with open(REPORT_TXT, "w", encoding="utf-8") as f:
        f.write("Modified-GR numerical background fit report\n")
        f.write("=" * 72 + "\n\n")
        f.write(f"Data choice: {DATA_CHOICE}\n")
        f.write(f"Number of H(z) points: {len(data)}\n")
        f.write(f"Random seed: {RANDOM_SEED}\n")
        f.write(f"Samples attempted: {N_SAMPLES}\n")
        f.write(f"Accepted samples: {len(accepted)}\n")
        f.write(f"Rejected samples: {sum(rejected.values())}\n")
        f.write(f"Runtime: {elapsed:.2f} s\n\n")

        f.write("Model and variables\n")
        f.write("-" * 72 + "\n")
        f.write("Model: ghost-free final EOM of Lagrangian #523 from the EOM summary.\n")
        f.write("Independent variable: x = ln(a) = -ln(1+z).\n")
        f.write("State variables: h=H/H0, varphi=phi/Mpred, q=dvarphi/dln(a).\n")
        f.write("Matter density parameter: rho_m0_bar = rho_m0/(Mpred^2 H0^2) = 3 Omega_m0.\n")
        f.write("No Omega_Lambda is used in the MG/scalar solver.\n")
        f.write(f"Reduced Planck mass used for unit explanation: {M_P_REDUCED_EV:.6e} eV.\n")
        f.write(f"1 km/s/Mpc = {KM_S_MPC_TO_EV:.6e} eV.\n\n")

        f.write("Priors used\n")
        f.write("-" * 72 + "\n")
        for k, v in PRIORS.items():
            f.write(f"{k}: {v}\n")
        f.write("q0 is not sampled directly; it is solved from E_N(x=0)=0.\n")
        f.write("epsilon is sampled as sign * 10^u using log10_abs_epsilon.\n\n")

        f.write("Reference only: flat LambdaCDM fit to the same H(z) table\n")
        f.write("-" * 72 + "\n")
        f.write("This is only a benchmark. It is not used by the MG/scalar solver.\n")
        f.write(f"Best reference H0 = {fmt(H0_lcdm)} km/s/Mpc\n")
        f.write(f"Best reference Omega_m0 = {fmt(Om_lcdm)}\n")
        f.write(f"Reference chi2 = {fmt(chi2_lcdm)}\n")
        f.write(f"Reference chi2 per point = {fmt(chi2_lcdm / len(data))}\n\n")

        if best is None or best.params is None:
            f.write("Result\n")
            f.write("-" * 72 + "\n")
            f.write("No accepted sample was found.\n")
            f.write("Most common rejection reasons:\n")
            for reason, count in rejected.most_common(20):
                f.write(f"  {count:6d}  {reason}\n")
            return

        p = best.params
        f.write("Best accepted modified-gravity/scalar sample\n")
        f.write("-" * 72 + "\n")
        f.write(f"chi2 = {fmt(best.chi2)}\n")
        f.write(f"chi2 per point = {fmt(best.chi2_per_point)}\n")
        f.write(f"max |constraint C| along trajectory = {fmt(best.max_abs_constraint, 3)}\n")
        f.write(f"H0 = {fmt(p.H0)} km/s/Mpc\n")
        f.write(f"H0 = {p.H0 * KM_S_MPC_TO_EV:.6e} eV\n")
        f.write(f"eps_HM = H0/Mpred = {p.eps_HM:.6e}\n")
        f.write(f"Omega_m0 = {fmt(p.Omega_m0)}\n")
        f.write(f"rho_m0_bar = {fmt(p.rho_bar)}\n")
        f.write(f"gamma = {fmt(p.gamma)}   (standard EH normalization is 0.5)\n")
        f.write(f"epsilon = {fmt(p.epsilon)}\n")
        f.write(f"mu = m/H0 = {fmt(p.mu)}\n")
        f.write(f"m = {p.mu * p.H0 * KM_S_MPC_TO_EV:.6e} eV\n")
        f.write(f"varphi0 = phi0/Mpred = {fmt(p.varphi0)}\n")
        f.write(f"phi0 = {p.varphi0 * M_P_REDUCED_EV:.6e} eV\n")
        f.write(f"q0 = dvarphi/dln(a)|0 = {fmt(p.q0)}\n")
        f.write(f"phidot0/(Mpred H0) = q0 because h0=1.\n\n")

        f.write("Predictions at data redshifts\n")
        f.write("-" * 72 + "\n")
        f.write(" z        H_obs      sigma      H_model    pull\n")
        for (z, Hobs, sig), Hm in zip(data, best.H_at_data):
            pull = (Hm - Hobs) / sig
            f.write(f"{z:6.3f}  {Hobs:9.3f}  {sig:8.3f}  {Hm:9.3f}  {pull:8.3f}\n")
        f.write("\n")

        f.write("Conclusion\n")
        f.write("-" * 72 + "\n")
        if best.chi2 is not None:
            if best.chi2_per_point is not None and best.chi2_per_point < 3.0:
                f.write("The sampled MG/scalar model can produce an H(z) curve in the broad vicinity of the supplied data.\n")
            else:
                f.write("The sampled MG/scalar model is numerically consistent but does not fit the supplied H(z) table very well under the current priors.\n")
        f.write("This conclusion is only for the embedded H(z)-style data and the selected Lagrangian #523 final EOM.\n")
        f.write("For actual DESI BAO, replace this H(z) likelihood with D_M/r_d, D_H/r_d or D_V/r_d and the published covariance matrix.\n")
        f.write("The CSV outputs contain the best trajectory and accepted sample summaries.\n")
        if plot_written:
            f.write(f"A plot was written to {BEST_FIT_PNG}.\n")

        f.write("\nMost common rejection reasons\n")
        f.write("-" * 72 + "\n")
        for reason, count in rejected.most_common(20):
            f.write(f"  {count:6d}  {reason}\n")


def main() -> None:
    print("Running one-file modified-GR numerical solver...")
    print(f"Data choice: {DATA_CHOICE}")
    print(f"Samples: {N_SAMPLES}, seed: {RANDOM_SEED}")
    data = select_data(DATA_CHOICE)

    best, accepted, rejected, elapsed = run_random_search(data)
    lcdm_ref = fit_reference_lcdm(data)

    plot_written = False
    if best is not None:
        write_best_solution_csv(best, BEST_SOLUTION_CSV)
        write_accepted_samples_csv(accepted, ACCEPTED_SAMPLES_CSV)
        plot_written = maybe_plot(best, data, BEST_FIT_PNG)

    write_report(best, accepted, rejected, elapsed, data, lcdm_ref, plot_written)

    print("Done.")
    print(f"Report: {os.path.abspath(REPORT_TXT)}")
    if best is None:
        print("No accepted sample. See rejection reasons in the report.")
    else:
        print(f"Best chi2: {best.chi2:.6g}")
        print(f"Best chi2 per point: {best.chi2_per_point:.6g}")
        print(f"Best H0: {best.params.H0:.4f} km/s/Mpc")
        print(f"Best Omega_m0: {best.params.Omega_m0:.4f}")
        print(f"Best solution CSV: {os.path.abspath(BEST_SOLUTION_CSV)}")
        print(f"Accepted sample CSV: {os.path.abspath(ACCEPTED_SAMPLES_CSV)}")
        if plot_written:
            print(f"Plot: {os.path.abspath(BEST_FIT_PNG)}")


if __name__ == "__main__":
    main()
