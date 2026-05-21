#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_all_lagrangians_bao_solver.py
==================================

One-file numerical scanner for all ghost-free FLRW Lagrangians in the provided
EOM summary.  It uses only numerical IVP integration; no analytic/power-series
solver is used in the model-discovery pipeline.

Outputs are written to:
    /Users/sunwenrong/Desktop/AI Modified Gravity/TheoryGPT-main/Modify GR/solver_results_1
unless the environment variable SOLVER_OUTPUT_DIR is set.

Core variables:
    x = ln a = -ln(1+z)
    h = H/H0
    varphi = phi/Mpred
    q = d varphi / dx
    lambda_H = Lambda_EFT / H0   (dimensionless EFT cutoff ratio)
    eps_HM = H0 / Mpred          (kept in physical EFT mode)

The solver scans every Lagrangian section that has final ghost-free +dust EOM,
tries to construct a dimensionless e-fold IVP, samples the free parameters,
solves the background, computes chi2/AIC/BIC against the H(z) data embedded
from the screenshots, and ranks all viable models.

Important: the embedded H(z) BAO table is not the full DESI BAO covariance
likelihood.  For true DESI BAO inference, replace the likelihood with D_M/r_d,
D_H/r_d, D_V/r_d and the published covariance matrix.
"""
from __future__ import annotations

import csv
import math
import os
import re
import time
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import Counter, defaultdict

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

# =============================================================================
# User-editable configuration
# =============================================================================

OUTPUT_DIR = Path(os.environ.get(
    "SOLVER_OUTPUT_DIR",
    "/Users/sunwenrong/Desktop/AI Modified Gravity/TheoryGPT-main/Modify GR/solver_result_2",
))

# Choose "bao", "cc", or "combined".  The screenshot's BAO table is H(z)-style.
DATA_CHOICE = "combined"

# Sampling.  1000 samples gives ~1 expected hit in the LCDM-like region
# (alpha~0.5, mu~0.05, varphi0~25) per EH+scalar model.
N_SAMPLES_PER_MODEL = int(os.environ.get("N_SAMPLES_PER_MODEL", "200"))
RANDOM_SEED = int(os.environ.get("RANDOM_SEED", "0"))  # 0 = time-based (non-reproducible)

# Integration settings.
N_GRID = 500
RTOL = 1e-8
ATOL = 1e-10
MAX_ABS_CONSTRAINT = 1e-4

# Priors.  These are not LambdaCDM priors; Omega_m0 is only matter density.
PRIORS = {
    "H0_km_s_Mpc": (60.0, 75.0),
    "Omega_m0": (0.15, 0.45),
    "varphi0": (-0.5, 0.5),
    "log10_mu": (-3.0, 1.0),
    # EFT cutoff ratio lambda_H = Lambda/H0 (dimensionless).
    # Controlled EFT prior. lambda_H = Lambda/H0.
    # Default [10^2, 10^5] keeps H/Lambda small over the H(z) range.
    # For phenomenological low-cutoff scans, override with environment variables below.
    "log10_lambda_H": (
        float(os.environ.get("LOG10_LAMBDA_H_MIN", "5.0")),
        float(os.environ.get("LOG10_LAMBDA_H_MAX", "10.0")),
    ),
    # For all free couplings (including EH coefficient if present).
    "log10_abs_c": (-6.0, 1.0),
}

# Physical EFT consistency switches.
FIX_EH_COEFFICIENT = os.environ.get("FIX_EH_COEFFICIENT", "1").strip().lower() not in {"0", "false", "no"}
EH_COEFFICIENT_VALUE = float(os.environ.get("EH_COEFFICIENT_VALUE", "0.5"))
ENFORCE_EFT_CUTOFF = os.environ.get("ENFORCE_EFT_CUTOFF", "1").strip().lower() not in {"0", "false", "no"}
EFT_MAX_H_OVER_LAMBDA = float(os.environ.get("EFT_MAX_H_OVER_LAMBDA", "0.1"))

MAX_ABS_Q0 = 20.0
PREFERRED_ABS_Q0 = 2.0
MAX_ABS_VARPHI_TRAJ = 200.0
MAX_ABS_Q_TRAJ = 80.0
MAX_H_KM_S_MPC = 1500.0
MIN_H = 1e-8
DENOM_EPS = 1e-12

# Default mode is physical EFT scaling: after substituting
#   H = H0 h, phi = Mp varphi, Lambda = H0 lambda_H,
#   rho = Mp^2 H0^2 rho_bar,
# we set Mp=1 but keep eps_HM = H0/Mp in the equations.
# The equations are then divided by eps_HM^2, the natural EH/matter scale.
# This preserves the hierarchy H0 << Mp for non-minimal scalar operators.
# Set SOLVER_MODE=phenomenological (or effective) only for effective-coupling scans.
MODE = os.environ.get("SOLVER_MODE", "eft").lower().strip()
if MODE == "physical":
    MODE = "eft"
if MODE == "effective":
    MODE = "phenomenological"

M_P_REDUCED_EV = 2.435e27
KM_S_MPC_TO_EV = 2.133119e-35

# =============================================================================
# Data from the screenshots
# =============================================================================

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

# =============================================================================
# EOM summary input
# =============================================================================
# Do NOT embed EOM summaries in this source file.
# This solver reads the latest generated EOM summary from disk.
# Expected default path:
#     ./eom_results/eom_summary.txt
# or one of the explicit fallback paths in load_eom_summary().

# =============================================================================
# Symbolic setup
# =============================================================================

a, adot, addot = sp.symbols("a adot addot", real=True)
phi, phidot, phiddot = sp.symbols("phi phidot phiddot", real=True)
M_p, m_sym, rho_m0 = sp.symbols("M_p m rho_m0", positive=True)
Lambda_sym = sp.Symbol("Lambda_eft", positive=True)    # EFT cutoff Λ
alpha, beta, gamma, delta, epsilon, zeta, eta, theta = sp.symbols("alpha beta gamma delta epsilon zeta eta theta", real=True)

x, h, hx, varphi, q, qx = sp.symbols("x h hx varphi q qx", real=True)
H0_sym, mu_sym, rho_bar_sym, eps_HM_sym = sp.symbols("H0 mu rho_bar eps_HM", positive=True)
lambda_H_sym = sp.Symbol("lambda_H", positive=True)    # Λ/H0 (dimensionless)

LOCAL_DICT = {
    "a": a, "adot": adot, "addot": addot,
    "phi": phi, "phidot": phidot, "phiddot": phiddot,
    "M_p": M_p, "m": m_sym, "rho_m0": rho_m0,
    "Lambda_eft": Lambda_sym,
    "alpha": alpha, "beta": beta, "gamma": gamma, "delta": delta,
    "epsilon": epsilon, "zeta": zeta, "eta": eta, "theta": theta,
}

BASE_SYMBOLS = {a, adot, addot, phi, phidot, phiddot, M_p, Lambda_sym, m_sym, rho_m0}
PARAM_SYMBOLS = [alpha, beta, gamma, delta, epsilon, zeta, eta, theta]

@dataclass
class Model:
    lag_id: str
    general: str
    has_phi: bool
    gf_relations: str
    eom_strings: Dict[str, str]
    eom_exprs: Dict[str, sp.Expr]
    free_symbols: List[sp.Symbol]
    eh_symbol: Optional[sp.Symbol]
    dimless_exprs: Optional[Dict[str, sp.Expr]] = None
    rhs_exprs: Optional[Dict[str, sp.Expr]] = None
    reject_reason: Optional[str] = None

@dataclass
class SampleResult:
    lag_id: str
    success: bool
    reason: str
    chi2: float = math.inf
    chi2_per_point: float = math.inf
    aic: float = math.inf
    bic: float = math.inf
    k_params: int = 0
    params: Optional[Dict[str, float]] = None
    max_abs_constraint: Optional[float] = None
    x_grid: Optional[np.ndarray] = None
    z_grid: Optional[np.ndarray] = None
    h_grid: Optional[np.ndarray] = None
    H_grid: Optional[np.ndarray] = None
    varphi_grid: Optional[np.ndarray] = None
    q_grid: Optional[np.ndarray] = None
    constraint_grid: Optional[np.ndarray] = None
    H_at_data: Optional[np.ndarray] = None


def clean_expr_string(s: str) -> str:
    s = s.strip()
    replacements = {
        r"\alpha": "alpha",
        r"\beta": "beta",
        r"\gamma": "gamma",
        r"\delta": "delta",
        r"\epsilon": "epsilon",
        r"\zeta": "zeta",
        r"\eta": "eta",
        r"\theta": "theta",
        r"\Lambda": "Lambda_eft",
        "rho_{m,0}": "rho_m0",
        "a(t)": "a",
        "phi(t)": "phi",
        "d^2phi/dt^2": "phiddot",
        "d^2a/dt^2": "addot",
        "dphi/dt": "phidot",
        "da/dt": "adot",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    return s


def parse_eom_expr(s: str) -> sp.Expr:
    cs = clean_expr_string(s)
    return parse_expr(cs, local_dict=LOCAL_DICT, evaluate=True)


def load_eom_summary() -> str:
    """
    Load the generated ghost-free EOM summary from disk.

    This function intentionally has NO embedded EOM fallback. If no summary is
    found, we fail loudly instead of silently scanning a stale hard-coded summary.
    """
    here = Path(__file__).resolve().parent
    candidates = [
        Path(os.environ["EOM_SUMMARY_PATH"]).expanduser()
        if os.environ.get("EOM_SUMMARY_PATH") else None,
        Path.cwd() / "eom_results" / "eom_summary.txt",
        Path.cwd() / "eom_summary.txt",
        here / "eom_results" / "eom_summary.txt",
        here / "eom_summary.txt",
        # Legacy / exported names are deliberately lower priority.
        Path.cwd() / "eom_summary(4).txt",
        Path.cwd() / "eom_summary(3).txt",
        Path.cwd() / "eom_summary(2).txt",
        Path.cwd() / "eom_summary(1).txt",
        here / "eom_summary(4).txt",
        here / "eom_summary(3).txt",
        here / "eom_summary(2).txt",
        here / "eom_summary(1).txt",
    ]
    tried = []
    for p in candidates:
        if p is None:
            continue
        tried.append(str(p))
        if p.exists() and p.is_file():
            text = p.read_text(encoding="utf-8")
            if "Lagrangian #" not in text:
                raise ValueError(f"EOM summary found but does not contain any Lagrangian sections: {p}")
            print(f"[INFO] Loading EOM summary from: {p}")
            return text
    raise FileNotFoundError(
        "No generated EOM summary found. Run EOM v2.3.py first, then ensure "
        "eom_results/eom_summary.txt exists, or set EOM_SUMMARY_PATH=/path/to/eom_summary.txt.\n"
        "Tried:\n  " + "\n  ".join(tried)
    )


def extract_general(sec: str) -> str:
    m = re.search(r"^  General:\s*(.*)$", sec, flags=re.M)
    return m.group(1).strip() if m else ""


def extract_has_phi(sec: str) -> bool:
    m = re.search(r"^  has_phi:\s*(\w+)", sec, flags=re.M)
    return bool(m and m.group(1).strip().lower() == "true")


def extract_gf(sec: str) -> str:
    m = re.search(r"Ghost-free coefficient relations:\n(.*?)Final EOM", sec, flags=re.S)
    if not m:
        return ""
    lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
    return "; ".join(lines)


def extract_final_eoms(sec: str) -> Dict[str, str]:
    out = {}
    m_block = re.search(r"Final EOM \(N=1 gauge, ghost-free, symbolic, \+dust\):\n(.*?)(?:\n  Ghost-free:|\Z)", sec, flags=re.S)
    if not m_block:
        return out
    block = m_block.group(1)
    for key in ["N", "a", "phi"]:
        m = re.search(rf"^    E_{key} = (.*)$", block, flags=re.M)
        if m:
            out[key] = m.group(1).strip()
    return out


def parse_models(text: str) -> List[Model]:
    models = []
    pattern = r"(?:^|\n)════════.*?\nLagrangian #(\d+)\n(.*?)(?=\n════════|\Z)"
    for mm in re.finditer(pattern, text, flags=re.S):
        lag_id, sec = mm.group(1), mm.group(2)
        eom_strings = extract_final_eoms(sec)
        if not eom_strings or "N" not in eom_strings or "a" not in eom_strings:
            continue
        eom_exprs = {}
        ok = True
        for k, s in eom_strings.items():
            try:
                eom_exprs[k] = parse_eom_expr(s)
            except Exception:
                ok = False
                break
        if not ok:
            continue
        free = sorted(list((set().union(*(expr.free_symbols for expr in eom_exprs.values())) & set(PARAM_SYMBOLS))), key=lambda z: z.name)
        general = extract_general(sec)
        eh_symbol = None
        # Detect which Greek coefficient (if any) multiplies the plain R (EH) term.
        # New format: "M_p² ( α · R  +  β Λ^{-2} · R^{ab}·R_{ab}  + ... )"
        # EH term has NO Λ prefix and R is not followed by ^ or _ (plain scalar curvature).
        if "M_p²" in general:
            _greek_map = {
                r"\alpha": alpha, r"\beta": beta, r"\gamma": gamma,
                r"\delta": delta, r"\epsilon": epsilon, r"\zeta": zeta,
                r"\eta": eta, r"\theta": theta,
            }
            for latex_name, sym in _greek_map.items():
                # Match "α · R" where R is followed by space, +, ), or end — not ^ or _
                pat = re.escape(latex_name) + r"\s*·\s*R(?![_^{a-z])"
                if re.search(pat, general):
                    eh_symbol = sym
                    break
        models.append(Model(
            lag_id=lag_id,
            general=general,
            has_phi=extract_has_phi(sec),
            gf_relations=extract_gf(sec),
            eom_strings=eom_strings,
            eom_exprs=eom_exprs,
            free_symbols=free,
            eh_symbol=eh_symbol,
        ))
    return models


def nondimensionalize_expr(expr: sp.Expr, mode: str = "eft") -> sp.Expr:
    """
    Convert a physical FLRW EOM into the solver's dimensionless variables.

    Physical substitutions:
        a = exp(x)
        adot = H0 exp(x) h
        addot = H0^2 exp(x) (h^2 + h h_x)
        phi = Mp varphi
        phidot = Mp H0 h q
        phiddot = Mp H0^2 h (h_x q + h q_x)
        m = H0 mu
        Lambda = H0 lambda_H
        rho_m0 = Mp^2 H0^2 rho_bar

    Modes:
        eft / physical:
            set Mp=1, H0=eps_HM and divide the EOM by eps_HM^2,
            the natural EH/matter scale. This keeps the physical H0/Mp
            hierarchy in non-minimal scalar operators.

        phenomenological / effective:
            set Mp=H0=1. This is only an effective-coupling scan and should
            not be interpreted as physical Wilson coefficients.
    """
    mode = mode.lower().strip()
    if mode == "physical":
        mode = "eft"
    if mode == "effective":
        mode = "phenomenological"

    subs = {
        a: sp.exp(x),
        adot: H0_sym * sp.exp(x) * h,
        addot: H0_sym**2 * sp.exp(x) * (h**2 + h * hx),
        phi: M_p * varphi,
        phidot: M_p * H0_sym * h * q,
        phiddot: M_p * H0_sym**2 * h * (hx * q + h * qx),
        m_sym: H0_sym * mu_sym,
        rho_m0: M_p**2 * H0_sym**2 * rho_bar_sym,
        Lambda_sym: H0_sym * lambda_H_sym,
    }
    e = sp.cancel(expr.subs(subs))

    if mode == "phenomenological":
        e = e.subs({M_p: sp.Integer(1), H0_sym: sp.Integer(1)})
    elif mode == "eft":
        e = e.subs({M_p: sp.Integer(1), H0_sym: eps_HM_sym})
        # Normalize all EOMs by the common EH/matter scale Mp^2 H0^2.
        # After Mp=1, H0=eps_HM this is eps_HM^2.
        # Operators whose physical size is enhanced/suppressed relative to EH
        # correctly retain positive or negative powers of eps_HM after this division.
        e = sp.cancel(e / eps_HM_sym**2)
    else:
        raise ValueError("mode must be 'eft'/'physical' or 'phenomenological'/'effective'")
    return sp.cancel(sp.factor(e))

def build_dimless_model(model: Model, mode: str = "eft") -> Model:
    try:
        dim = {k: nondimensionalize_expr(v, mode=mode) for k, v in model.eom_exprs.items()}
        # Fix the Einstein-Hilbert normalization if a plain-R coefficient is present.
        # For L ~ Mp^2 * alpha * R, standard EH normalization is alpha = 1/2.
        if FIX_EH_COEFFICIENT and model.eh_symbol is not None:
            dim = {k: sp.cancel(v.subs({model.eh_symbol: EH_COEFFICIENT_VALUE})) for k, v in dim.items()}
            model.free_symbols = [s for s in model.free_symbols if s != model.eh_symbol]
        model.dimless_exprs = dim
        # Trivial/invalid model check.
        if sp.simplify(dim["N"] + rho_bar_sym * sp.exp(-3*x)) == 0 and sp.simplify(dim.get("a", 0)) == 0:
            model.reject_reason = "trivial ghost-free final EOM: E_N=-rho_m only, E_a=0"
            return model
        unknowns = [hx, qx] if model.has_phi and "phi" in dim else [hx]
        equations = [dim.get("a", 0)]
        if model.has_phi and "phi" in dim:
            equations.append(dim["phi"])
        # Must contain at least one unknown derivative to define evolution.
        if not any(eq.has(u) for eq in equations for u in unknowns):
            model.reject_reason = "no e-fold evolution equation for h_x/q_x"
            return model
        sol = sp.solve(equations, unknowns, dict=True, simplify=False)
        if not sol:
            model.reject_reason = "could not solve E_a/E_phi algebraically for h_x/q_x"
            return model
        s0 = sol[0]
        rhs = {}
        if hx in s0:
            rhs["hx"] = sp.cancel(s0[hx])
        else:
            model.reject_reason = "h_x not determined by dynamical EOM"
            return model
        if model.has_phi and "phi" in dim:
            if qx not in s0:
                model.reject_reason = "q_x not determined by coupled scalar EOM"
                return model
            rhs["qx"] = sp.cancel(s0[qx])
        model.rhs_exprs = rhs
        return model
    except Exception as exc:
        model.reject_reason = f"symbolic build failed: {type(exc).__name__}: {exc}"
        return model


def get_param_symbols(model: Model) -> List[sp.Symbol]:
    syms = list(model.free_symbols)
    if FIX_EH_COEFFICIENT and model.eh_symbol is not None:
        syms = [s for s in syms if s != model.eh_symbol]
    syms = sorted(set(syms), key=lambda s: s.name)
    return syms


def sample_parameter_values(model: Model, rng: np.random.Generator, mode: str) -> Dict[sp.Symbol, float]:
    vals: Dict[sp.Symbol, float] = {}
    for sym in get_param_symbols(model):
        lo, hi = PRIORS["log10_abs_c"]
        mag = 10.0 ** float(rng.uniform(lo, hi))
        sign = float(rng.choice([-1.0, 1.0]))
        vals[sym] = sign * mag
    return vals


def lambdify_model(model: Model, mode: str):
    mode = "eft" if mode.lower().strip() in {"eft", "physical"} else "phenomenological"
    assert model.dimless_exprs is not None and model.rhs_exprs is not None
    param_syms = get_param_symbols(model)
    args_common = [x, h, varphi, q, rho_bar_sym, mu_sym, lambda_H_sym] + param_syms
    if mode == "eft":
        args_common += [eps_HM_sym]
    C_expr = model.dimless_exprs["N"]
    hx_expr = model.rhs_exprs["hx"]
    qx_expr = model.rhs_exprs.get("qx")
    C_func = sp.lambdify(args_common, C_expr, modules="numpy")
    hx_func = sp.lambdify(args_common, hx_expr, modules="numpy")
    qx_func = sp.lambdify(args_common, qx_expr, modules="numpy") if qx_expr is not None else None
    return C_func, hx_func, qx_func, param_syms


def robust_float(val: Any) -> float:
    arr = np.asarray(val, dtype=float)
    if arr.shape == ():
        return float(arr)
    return float(arr.item())


def find_q0_root(C_func, base_args_without_q, q_range=(-MAX_ABS_Q0, MAX_ABS_Q0), n_scan=401) -> Optional[float]:
    # base_args_without_q should be a callable taking q -> args
    q_min, q_max = q_range
    grid = np.linspace(q_min, q_max, n_scan)
    vals = []
    roots = []
    for qq in grid:
        try:
            v = robust_float(C_func(*base_args_without_q(float(qq))))
            if not np.isfinite(v):
                v = np.nan
        except Exception:
            v = np.nan
        vals.append(v)
        if np.isfinite(v) and abs(v) < 1e-10:
            roots.append(float(qq))
    vals = np.array(vals)
    for i in range(len(grid)-1):
        f1, f2 = vals[i], vals[i+1]
        if not (np.isfinite(f1) and np.isfinite(f2)):
            continue
        if f1 == 0:
            roots.append(float(grid[i]))
        if f1 * f2 < 0:
            try:
                root = brentq(lambda qq: robust_float(C_func(*base_args_without_q(float(qq)))), grid[i], grid[i+1], maxiter=100)
                if np.isfinite(root):
                    roots.append(float(root))
            except Exception:
                pass
    if not roots:
        return None
    # Deduplicate and prefer small |q0|.
    roots_sorted = []
    for r in sorted(roots, key=lambda rr: abs(rr)):
        if not any(abs(r-r0) < 1e-6 for r0 in roots_sorted):
            roots_sorted.append(r)
    preferred = [r for r in roots_sorted if abs(r) <= PREFERRED_ABS_Q0]
    return float((preferred or roots_sorted)[0])


def evaluate_sample(model: Model, data: np.ndarray, rng: np.random.Generator, mode: str) -> SampleResult:
    mode = "eft" if mode.lower().strip() in {"eft", "physical"} else "phenomenological"
    if model.reject_reason:
        return SampleResult(model.lag_id, False, model.reject_reason)
    try:
        C_func, hx_func, qx_func, param_syms = lambdify_model(model, mode)
    except Exception as exc:
        return SampleResult(model.lag_id, False, f"lambdify failed: {type(exc).__name__}: {exc}")

    H0_km = float(rng.uniform(*PRIORS["H0_km_s_Mpc"]))
    Omega_m0 = float(rng.uniform(*PRIORS["Omega_m0"]))
    rho_bar = 3.0 * Omega_m0
    mu = 10.0 ** float(rng.uniform(*PRIORS["log10_mu"])) if model.has_phi else 0.0
    varphi0 = float(rng.uniform(*PRIORS["varphi0"])) if model.has_phi else 0.0
    lambda_H = 10.0 ** float(rng.uniform(*PRIORS["log10_lambda_H"]))
    eps_HM = (H0_km * KM_S_MPC_TO_EV) / M_P_REDUCED_EV
    pvals = sample_parameter_values(model, rng, mode)
    pval_list = [pvals[s] for s in param_syms]

    def make_args(xx, hh, vv, qq):
        args = [xx, hh, vv, qq, rho_bar, mu, lambda_H] + pval_list
        if mode == "eft":
            args.append(eps_HM)
        return args

    # Determine q0 or no-scalar constraint.
    if model.has_phi and qx_func is not None:
        def base_args(qtrial):
            return make_args(0.0, 1.0, varphi0, qtrial)
        q0 = find_q0_root(C_func, base_args)
        if q0 is None:
            return SampleResult(model.lag_id, False, "no acceptable real q0 root from E_N(x=0)=0")
    else:
        q0 = 0.0
        try:
            C0 = robust_float(C_func(*make_args(0.0, 1.0, 0.0, 0.0)))
            if not np.isfinite(C0) or abs(C0) > 1e-6:
                return SampleResult(model.lag_id, False, f"no-scalar constraint not satisfied at x=0: C0={C0:.3e}")
        except Exception as exc:
            return SampleResult(model.lag_id, False, f"no-scalar constraint evaluation failed: {type(exc).__name__}")

    # Check RHS at initial point.
    try:
        hx0 = robust_float(hx_func(*make_args(0.0, 1.0, varphi0, q0)))
        if not np.isfinite(hx0) or abs(hx0) > 1e6:
            return SampleResult(model.lag_id, False, "initial h_x is singular or absurd")
        if model.has_phi:
            qx0 = robust_float(qx_func(*make_args(0.0, 1.0, varphi0, q0)))
            if not np.isfinite(qx0) or abs(qx0) > 1e6:
                return SampleResult(model.lag_id, False, "initial q_x is singular or absurd")
    except Exception as exc:
        return SampleResult(model.lag_id, False, f"initial RHS failed: {type(exc).__name__}")

    z_data = data[:,0]
    H_obs = data[:,1]
    sig = data[:,2]
    zmax = float(np.max(z_data))
    xmin = -math.log(1.0 + zmax)
    x_eval = np.linspace(0.0, xmin, N_GRID)

    if model.has_phi:
        y0 = np.array([1.0, varphi0, q0], dtype=float)
    else:
        y0 = np.array([1.0], dtype=float)

    def rhs(xx, yy):
        try:
            if model.has_phi:
                hh, vv, qq = float(yy[0]), float(yy[1]), float(yy[2])
                dhdx = robust_float(hx_func(*make_args(xx, hh, vv, qq)))
                dqdx = robust_float(qx_func(*make_args(xx, hh, vv, qq)))
                return np.array([dhdx, qq, dqdx], dtype=float)
            else:
                hh = float(yy[0])
                dhdx = robust_float(hx_func(*make_args(xx, hh, 0.0, 0.0)))
                return np.array([dhdx], dtype=float)
        except Exception:
            return np.full_like(yy, np.nan, dtype=float)

    try:
        sol = solve_ivp(rhs, (0.0, xmin), y0, t_eval=x_eval, dense_output=True,
                        method="DOP853", rtol=RTOL, atol=ATOL)
    except Exception as exc:
        return SampleResult(model.lag_id, False, f"solve_ivp exception: {type(exc).__name__}: {exc}")
    if not sol.success:
        return SampleResult(model.lag_id, False, f"solve_ivp failed: {sol.message}")
    if not np.all(np.isfinite(sol.y)):
        return SampleResult(model.lag_id, False, "trajectory contains NaN/inf")

    h_grid = sol.y[0]
    if np.any(h_grid <= MIN_H):
        return SampleResult(model.lag_id, False, "h(x)<=0 on trajectory")
    if ENFORCE_EFT_CUTOFF:
        max_h_over_lambda = float(np.max(np.abs(h_grid) / lambda_H))
        if max_h_over_lambda > EFT_MAX_H_OVER_LAMBDA:
            return SampleResult(
                model.lag_id,
                False,
                f"EFT cutoff violated: max(h/lambda_H)={max_h_over_lambda:.3e} > {EFT_MAX_H_OVER_LAMBDA:.3e}",
            )
    varphi_grid = sol.y[1] if model.has_phi else None
    q_grid = sol.y[2] if model.has_phi else None
    if model.has_phi:
        if np.max(np.abs(varphi_grid)) > MAX_ABS_VARPHI_TRAJ:
            return SampleResult(model.lag_id, False, "|varphi| trajectory too large")
        if np.max(np.abs(q_grid)) > MAX_ABS_Q_TRAJ:
            return SampleResult(model.lag_id, False, "|q| trajectory too large")

    z_grid = np.exp(-x_eval) - 1.0
    H_grid = H0_km * h_grid
    if np.any(H_grid > MAX_H_KM_S_MPC):
        return SampleResult(model.lag_id, False, "H(z) absurdly large")

    # Constraint residual along trajectory.
    C_vals = []
    try:
        for i, xx in enumerate(x_eval):
            hh = float(h_grid[i])
            vv = float(varphi_grid[i]) if model.has_phi else 0.0
            qq = float(q_grid[i]) if model.has_phi else 0.0
            C_vals.append(robust_float(C_func(*make_args(float(xx), hh, vv, qq))))
        C_vals = np.array(C_vals, dtype=float)
    except Exception as exc:
        return SampleResult(model.lag_id, False, f"constraint monitor failed: {type(exc).__name__}")
    if not np.all(np.isfinite(C_vals)):
        return SampleResult(model.lag_id, False, "constraint residual NaN/inf")
    maxC = float(np.max(np.abs(C_vals)))
    if maxC > MAX_ABS_CONSTRAINT:
        return SampleResult(model.lag_id, False, f"constraint drift too large: max|C|={maxC:.3e}")

    # Evaluate model at data points.
    try:
        x_data = -np.log1p(z_data)
        y_data = sol.sol(x_data)
        h_data = y_data[0]
        H_model = H0_km * h_data
    except Exception as exc:
        return SampleResult(model.lag_id, False, f"dense output failed: {type(exc).__name__}")
    if not np.all(np.isfinite(H_model)):
        return SampleResult(model.lag_id, False, "H_model at data not finite")
    chi2 = float(np.sum(((H_model - H_obs) / sig)**2))
    n = len(z_data)
    # Count free sampled parameters: H0, Omega_m0, [lambda_H if used], symbols, plus scalar varphi0/mu if present.
    # lambda_H only counts if the model's dimensionless EOM actually involves lambda_H.
    uses_lambda = any(expr.has(lambda_H_sym) for expr in model.dimless_exprs.values())
    k = 2 + (1 if uses_lambda else 0) + len(param_syms) + (2 if model.has_phi else 0)
    aic = chi2 + 2.0 * k
    bic = chi2 + k * math.log(n)

    params = {
        "H0_km_s_Mpc": H0_km,
        "Omega_m0": Omega_m0,
        "rho_bar": rho_bar,
        "mu_m_over_H0": mu,
        "varphi0_phi_over_Mp": varphi0,
        "q0_dvarphi_dln_a": q0,
        "eps_HM_H0_over_Mp": eps_HM,
        "lambda_H_Lambda_over_H0": lambda_H,
        "Lambda_eV": lambda_H * H0_km * KM_S_MPC_TO_EV,
    }
    for s, v in pvals.items():
        params[str(s)] = float(v)
    return SampleResult(
        lag_id=model.lag_id, success=True, reason="ok", chi2=chi2,
        chi2_per_point=chi2/n, aic=aic, bic=bic, k_params=k,
        params=params, max_abs_constraint=maxC,
        x_grid=x_eval, z_grid=z_grid, h_grid=h_grid, H_grid=H_grid,
        varphi_grid=varphi_grid, q_grid=q_grid, constraint_grid=C_vals,
        H_at_data=H_model,
    )


def lcdm_fit_reference(data: np.ndarray) -> Dict[str, float]:
    # Simple grid reference: flat LCDM H=H0 sqrt(Om(1+z)^3 + 1-Om)
    z, Hobs, sig = data[:,0], data[:,1], data[:,2]
    best = {"chi2": math.inf}
    for H0 in np.linspace(55, 80, 501):
        for Om in np.linspace(0.05, 0.6, 551):
            h_l = np.sqrt(Om*(1+z)**3 + (1-Om))
            Hm = H0*h_l
            c2 = float(np.sum(((Hm-Hobs)/sig)**2))
            if c2 < best["chi2"]:
                best = {"H0": float(H0), "Omega_m0": float(Om), "chi2": c2, "chi2_per_point": c2/len(z)}
    k=2; n=len(z)
    best["AIC"] = best["chi2"] + 2*k
    best["BIC"] = best["chi2"] + k*math.log(n)
    return best


def result_row(r: SampleResult) -> Dict[str, Any]:
    row = {
        "lag_id": r.lag_id, "success": r.success, "reason": r.reason,
        "chi2": r.chi2, "chi2_per_point": r.chi2_per_point,
        "AIC": r.aic, "BIC": r.bic, "k_params": r.k_params,
        "max_abs_constraint": r.max_abs_constraint,
    }
    if r.params:
        row.update(r.params)
    return row


def write_csv(path: Path, rows: List[Dict[str, Any]]):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = []
    for row in rows:
        for k in row.keys():
            if k not in keys:
                keys.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def plot_best(data: np.ndarray, best: Optional[SampleResult], path: Path):
    if best is None or plt is None:
        return
    fig, ax = plt.subplots(figsize=(8,5))
    ax.errorbar(data[:,0], data[:,1], yerr=data[:,2], fmt="o", capsize=3, label=f"{DATA_CHOICE} H(z) data")
    order = np.argsort(best.z_grid)
    ax.plot(best.z_grid[order], best.H_grid[order], lw=2, label=f"Best L#{best.lag_id}")
    ax.set_xlabel("z")
    ax.set_ylabel("H(z) [km/s/Mpc]")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_best_solution(best: Optional[SampleResult], path: Path):
    if best is None:
        path.write_text("", encoding="utf-8")
        return
    rows=[]
    for i in range(len(best.x_grid)):
        row = {
            "x_ln_a": float(best.x_grid[i]),
            "z": float(best.z_grid[i]),
            "h_dimensionless": float(best.h_grid[i]),
            "H_km_s_Mpc": float(best.H_grid[i]),
            "constraint_residual": float(best.constraint_grid[i]),
        }
        if best.varphi_grid is not None:
            row["varphi_phi_over_Mp"] = float(best.varphi_grid[i])
            row["q_dvarphi_dln_a"] = float(best.q_grid[i])
        rows.append(row)
    write_csv(path, rows)


def run_numerical_scan():
    t0 = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = select_data(DATA_CHOICE)
    summary_text = load_eom_summary()
    models_raw = parse_models(summary_text)
    rng = np.random.default_rng(RANDOM_SEED if RANDOM_SEED != 0 else None)

    built_models = [build_dimless_model(m, mode=MODE) for m in models_raw]
    all_results: List[SampleResult] = []
    best_by_model: Dict[str, SampleResult] = {}
    reject_counts_by_model: Dict[str, Counter] = defaultdict(Counter)

    for mi, model in enumerate(built_models, 1):
        if model.reject_reason:
            reject_counts_by_model[model.lag_id][model.reject_reason] += N_SAMPLES_PER_MODEL
            continue
        for _ in range(N_SAMPLES_PER_MODEL):
            res = evaluate_sample(model, data, rng, MODE)
            if res.success:
                all_results.append(res)
                b = best_by_model.get(model.lag_id)
                if b is None or res.aic < b.aic:
                    best_by_model[model.lag_id] = res
            else:
                reject_counts_by_model[model.lag_id][res.reason] += 1

    accepted = sorted(all_results, key=lambda r: (r.aic, r.chi2))
    model_best_list = sorted(best_by_model.values(), key=lambda r: (r.aic, r.chi2))
    best = accepted[0] if accepted else None
    lcdm = lcdm_fit_reference(data)

    # Outputs
    write_csv(OUTPUT_DIR / "accepted_samples_summary.csv", [result_row(r) for r in accepted])
    write_csv(OUTPUT_DIR / "model_ranking.csv", [result_row(r) for r in model_best_list])
    write_best_solution(best, OUTPUT_DIR / "best_solution.csv")
    plot_best(data, best, OUTPUT_DIR / "best_fit_Hz.png")

    # Per top model solutions.
    for rank, r in enumerate(model_best_list[:10], 1):
        write_best_solution(r, OUTPUT_DIR / f"top_{rank:02d}_lagrangian_{r.lag_id}_solution.csv")

    # Rejection report csv.
    rej_rows=[]
    for lid, cnt in sorted(reject_counts_by_model.items(), key=lambda kv: int(kv[0])):
        total=sum(cnt.values())
        for reason, n in cnt.most_common(8):
            rej_rows.append({"lag_id": lid, "count": n, "total_rejected_or_skipped": total, "reason": reason})
    write_csv(OUTPUT_DIR / "reject_reasons_by_model.csv", rej_rows)

    # Text report.
    lines=[]
    lines.append("AI Modified Gravity: automatic ghost-free Lagrangian H(z) scan")
    lines.append("="*78)
    lines.append(f"Output directory: {OUTPUT_DIR}")
    lines.append(f"Run time: {time.time()-t0:.2f} s")
    lines.append(f"Mode: {MODE}")
    lines.append(f"Data choice: {DATA_CHOICE}; N_data={len(data)}; z_max={float(np.max(data[:,0])):.3f}")
    lines.append(f"Parsed Lagrangians: {len(models_raw)}")
    lines.append(f"Built nontrivial IVP models: {sum(1 for m in built_models if not m.reject_reason)}")
    lines.append(f"Samples per model: {N_SAMPLES_PER_MODEL}")
    lines.append(f"Accepted samples: {len(accepted)}")
    lines.append("")
    lines.append("Physics conventions")
    lines.append("- Uses x=ln(a)=-ln(1+z), h=H/H0, varphi=phi/Mpred, q=dvarphi/dln(a).")
    lines.append("- Default physical EFT mode keeps eps_HM=H0/Mpred in the dimensionless equations.")
    lines.append("- EOMs are normalized by Mp^2 H0^2 after substitution; relative eps_HM powers are retained.")
    lines.append("- EFT cutoff: lambda_H=Lambda/H0 (dimensionless), sampled log-uniformly.")
    lines.append(f"- EFT validity cut: max_x |h|/lambda_H < {EFT_MAX_H_OVER_LAMBDA:g} (enabled={ENFORCE_EFT_CUTOFF}).")
    lines.append(f"- EH coefficient fixed to {EH_COEFFICIENT_VALUE:g} when detected (enabled={FIX_EH_COEFFICIENT}).")
    lines.append("- a0 and h0 are fixed to 1. q0 is solved from E_N(x=0)=0 for scalar models.")
    lines.append("- rho_m0 is sampled as rho_bar=3 Omega_m0; no Omega_Lambda is assumed in the MG scan.")
    lines.append("- Mpred = 2.435e27 eV (physical reduced Planck mass, restored in output).")
    lines.append("- Physical Lambda [eV] = lambda_H * H0 [eV].")
    lines.append("- Ranking uses chi2 plus AIC/BIC penalties; AIC=chi2+2k, BIC=chi2+k ln N.")
    lines.append("")
    lines.append("Flat-LambdaCDM reference fit to the same H(z) table, for benchmark only")
    lines.append(f"  chi2={lcdm['chi2']:.6g}, chi2/N={lcdm['chi2_per_point']:.6g}, AIC={lcdm['AIC']:.6g}, BIC={lcdm['BIC']:.6g}")
    lines.append(f"  H0={lcdm['H0']:.6g}, Omega_m0={lcdm['Omega_m0']:.6g}")
    lines.append("")

    if best is None:
        lines.append("No accepted model sample was found.  Check reject_reasons_by_model.csv.")
    else:
        bm = next((m for m in built_models if m.lag_id == best.lag_id), None)
        lines.append("Best sample by AIC")
        lines.append(f"  Lagrangian #{best.lag_id}")
        lines.append(f"  chi2={best.chi2:.6g}, chi2/N={best.chi2_per_point:.6g}, AIC={best.aic:.6g}, BIC={best.bic:.6g}, k={best.k_params}")
        lines.append(f"  max |constraint|={best.max_abs_constraint:.3e}")
        if bm:
            lines.append(f"  General: {bm.general}")
            lines.append(f"  Ghost-free relations: {bm.gf_relations}")
            lines.append("  Free symbols in final EOM: " + ", ".join(str(s) for s in bm.free_symbols))
            if bm.eh_symbol is not None:
                if FIX_EH_COEFFICIENT:
                    lines.append(f"  EH coefficient detected: {bm.eh_symbol} and fixed to {EH_COEFFICIENT_VALUE:g}")
                else:
                    lines.append(f"  EH coefficient detected: {bm.eh_symbol} (sampled like other couplings)")
        lines.append("  Parameters:")
        for k,v in sorted(best.params.items()):
            lines.append(f"    {k} = {v:.12g}")
        lines.append("")
        lines.append("H(z) residuals at data points")
        for zi, Ho, sg, Hm in zip(data[:,0], data[:,1], data[:,2], best.H_at_data):
            lines.append(f"  z={zi:.4g}: H_obs={Ho:.6g}, sigma={sg:.6g}, H_model={Hm:.6g}, pull={(Hm-Ho)/sg:.4g}")

    lines.append("")
    lines.append("Top models by AIC")
    if not model_best_list:
        lines.append("  None")
    else:
        for rank, r in enumerate(model_best_list[:20], 1):
            lines.append(f"  {rank:02d}. L#{r.lag_id}: chi2={r.chi2:.6g}, AIC={r.aic:.6g}, BIC={r.bic:.6g}, k={r.k_params}, maxC={r.max_abs_constraint:.2e}")
            m = next((mm for mm in built_models if mm.lag_id == r.lag_id), None)
            if m:
                lines.append(f"      General: {m.general}")
                lines.append(f"      GF: {m.gf_relations}")
            pshort = ", ".join(f"{k}={v:.4g}" for k,v in sorted(r.params.items()) if k in ["H0_km_s_Mpc","Omega_m0","rho_bar","mu_m_over_H0","varphi0_phi_over_Mp","q0_dvarphi_dln_a"] or k in [str(s) for s in (m.free_symbols if m else [])])
            lines.append(f"      params: {pshort}")

    lines.append("")
    lines.append("Skipped / structurally rejected models")
    for m in sorted(built_models, key=lambda mm: int(mm.lag_id)):
        if m.reject_reason:
            lines.append(f"  L#{m.lag_id}: {m.reject_reason}")

    lines.append("")
    lines.append("Files written")
    for fn in ["scan_report.txt", "model_ranking.csv", "accepted_samples_summary.csv", "best_solution.csv", "best_fit_Hz.png", "reject_reasons_by_model.csv"]:
        lines.append(f"  {OUTPUT_DIR / fn}")
    (OUTPUT_DIR / "scan_report.txt").write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines[:40]))
    print(f"\nDone. Full report: {OUTPUT_DIR / 'scan_report.txt'}")



# =============================================================================
# Integrated Top-5 summary and plotting
# =============================================================================

def _find_lagrangian_pkl_for_summary() -> Optional[Path]:
    here = Path(__file__).resolve().parent
    candidates = [
        Path(os.environ["LAGRANGIANS_PKL_PATH"]).expanduser()
        if os.environ.get("LAGRANGIANS_PKL_PATH") else None,
        Path.cwd() / "lagrangians.pkl",
        Path.cwd() / "lagrangians(1).pkl",
        here / "lagrangians.pkl",
        here / "lagrangians(1).pkl",
    ]
    for p in candidates:
        if p is not None and p.exists() and p.is_file():
            return p.resolve()
    return None


def _load_lagrangian_map_from_pkl(pkl_path: Path) -> Dict[str, Dict[str, Any]]:
    import pickle
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)

    lag_map: Dict[str, Dict[str, Any]] = {}
    if isinstance(data, dict):
        counter = 0
        for key in sorted(data.keys()):
            items = data[key]
            if not isinstance(items, list):
                continue
            for item in items:
                counter += 1
                lag_map[str(counter)] = item
    elif isinstance(data, list):
        for i, item in enumerate(data, 1):
            lag_map[str(i)] = item
    else:
        raise TypeError(f"Unsupported pkl structure: {type(data)}")
    return lag_map


def _raw_lagrangian_string(lag_map: Dict[str, Dict[str, Any]], lag_id: str) -> str:
    item = lag_map.get(str(lag_id))
    if not item:
        return f"[not found in pkl for Lagrangian #{lag_id}]"
    return str(item.get("general", "[general form missing]"))


def _raw_terms_string(lag_map: Dict[str, Dict[str, Any]], lag_id: str) -> str:
    item = lag_map.get(str(lag_id))
    if not item:
        return ""
    terms = item.get("terms", [])
    if not isinstance(terms, list):
        return ""
    lines = []
    for j, term in enumerate(terms, 1):
        coeff = term.get("coeff_symbol", "?")
        cand = term.get("candidate", "?")
        md = term.get("mass_dim", "?")
        lp = term.get("lambda_power", "?")
        fixed = term.get("fixed", False)
        sector = term.get("sector", "gravity")
        fixed_s = ", fixed" if fixed else ""
        sector_s = f", {sector}" if sector != "gravity" else ""
        lines.append(f"    [{j}] coeff={coeff}, Λ^{lp}, dim={md}{fixed_s}{sector_s}: {cand}")
    return "\n".join(lines)


def _fmt(x, precision=8) -> str:
    try:
        if x is None or (isinstance(x, float) and not np.isfinite(x)):
            return "N/A"
        xf = float(x)
        if abs(xf) != 0 and (abs(xf) < 1e-4 or abs(xf) >= 1e5):
            return f"{xf:.{precision}e}"
        return f"{xf:.{precision}g}"
    except Exception:
        return str(x)


def _read_model_ranking_csv() -> List[Dict[str, str]]:
    ranking_path = OUTPUT_DIR / "model_ranking.csv"
    if not ranking_path.exists():
        raise FileNotFoundError(f"Missing ranking file: {ranking_path}")
    with open(ranking_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        raise RuntimeError(f"Ranking file exists but has no accepted models: {ranking_path}")
    return rows


def _float_from_row(row: Dict[str, str], key: str, default=np.nan) -> float:
    try:
        val = row.get(key, "")
        if val is None or val == "":
            return default
        return float(val)
    except Exception:
        return default


def _find_top_solution_csv(rank: int, lag_id: str) -> Optional[Path]:
    exact = OUTPUT_DIR / f"top_{rank:02d}_lagrangian_{lag_id}_solution.csv"
    if exact.exists():
        return exact
    matches = sorted(OUTPUT_DIR.glob(f"top_*_lagrangian_{lag_id}_solution.csv"))
    if matches:
        return matches[0]
    # Fallback: global best only if this is rank 1.
    if rank == 1 and (OUTPUT_DIR / "best_solution.csv").exists():
        return OUTPUT_DIR / "best_solution.csv"
    return None


def _read_solution_csv(path: Path) -> Dict[str, np.ndarray]:
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    cols = reader.fieldnames or []
    arr = {}
    for c in cols:
        vals = []
        for r in rows:
            try:
                vals.append(float(r[c]))
            except Exception:
                vals.append(np.nan)
        arr[c] = np.asarray(vals, dtype=float)
    return arr


def _plot_top_model(data: np.ndarray, rank: int, row: Dict[str, str], sol_path: Path, out_path: Path):
    if plt is None:
        return
    sol = _read_solution_csv(sol_path)
    if "z" not in sol or "H_km_s_Mpc" not in sol:
        return
    order = np.argsort(sol["z"])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(data[:, 0], data[:, 1], yerr=data[:, 2], fmt="o", capsize=3, label=f"{DATA_CHOICE} H(z) data")
    ax.plot(sol["z"][order], sol["H_km_s_Mpc"][order], lw=2.2, label=f"L#{row.get('lag_id')} numerical H(z)")
    ax.set_title(
        f"Top {rank}: Lagrangian #{row.get('lag_id')}\n"
        f"chi2={_float_from_row(row, 'chi2'):.4g}, AIC={_float_from_row(row, 'AIC'):.4g}, BIC={_float_from_row(row, 'BIC'):.4g}"
    )
    ax.set_xlabel("z")
    ax.set_ylabel("H(z) [km/s/Mpc]")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def _plot_top_overlay(data: np.ndarray, top_rows: List[Dict[str, str]], sol_paths: Dict[str, Path], out_path: Path):
    if plt is None:
        return
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.errorbar(data[:, 0], data[:, 1], yerr=data[:, 2], fmt="o", capsize=3, label=f"{DATA_CHOICE} H(z) data", zorder=5)
    for i, row in enumerate(top_rows, 1):
        lag_id = str(row.get("lag_id"))
        sol_path = sol_paths.get(lag_id)
        if sol_path is None:
            continue
        sol = _read_solution_csv(sol_path)
        if "z" not in sol or "H_km_s_Mpc" not in sol:
            continue
        order = np.argsort(sol["z"])
        ax.plot(sol["z"][order], sol["H_km_s_Mpc"][order], lw=1.8, label=f"#{i} L{lag_id}, chi2={_float_from_row(row, 'chi2'):.3g}")
    ax.set_title("Top fitted Lagrangians: numerical H(z)")
    ax.set_xlabel("z")
    ax.set_ylabel("H(z) [km/s/Mpc]")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def run_top5_summary(top_n: int = 5):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = _read_model_ranking_csv()
    top_rows = rows[:top_n]

    pkl_path = _find_lagrangian_pkl_for_summary()
    lag_map: Dict[str, Dict[str, Any]] = {}
    if pkl_path is not None:
        lag_map = _load_lagrangian_map_from_pkl(pkl_path)

    data = select_data(DATA_CHOICE)

    generated_plots: List[Path] = []
    sol_paths: Dict[str, Path] = {}
    for i, row in enumerate(top_rows, 1):
        lag_id = str(row.get("lag_id"))
        sol_path = _find_top_solution_csv(i, lag_id)
        if sol_path is None:
            continue
        sol_paths[lag_id] = sol_path
        plot_path = OUTPUT_DIR / f"top_{i:02d}_lagrangian_{lag_id}_Hz_fit.png"
        _plot_top_model(data, i, row, sol_path, plot_path)
        generated_plots.append(plot_path)

    overlay_path = OUTPUT_DIR / "top5_overlay_Hz_fit.png"
    _plot_top_overlay(data, top_rows, sol_paths, overlay_path)
    if overlay_path.exists():
        generated_plots.append(overlay_path)

    lines: List[str] = []
    lines.append("Top fitted Lagrangians: forms, initial conditions, and numerical-fit parameters")
    lines.append("=" * 92)
    lines.append("")
    lines.append(f"Output directory: {OUTPUT_DIR}")
    lines.append(f"EOM summary source: external file only; no embedded EOM fallback is used.")
    lines.append(f"Lagrangian pkl: {pkl_path if pkl_path is not None else '[not found]'}")
    lines.append(f"Ranking source: {OUTPUT_DIR / 'model_ranking.csv'}")
    lines.append("")
    lines.append("Numerical convention")
    lines.append("- Independent variable: x = ln(a) = -ln(1+z).")
    lines.append("- Dimensionless Hubble variable: h(x) = H(x) / H0.")
    lines.append("- Scalar variable: varphi(x) = phi(x) / Mpred.")
    lines.append("- Scalar slope: q(x) = d varphi / d ln(a).")
    lines.append("- EFT cutoff ratio: lambda_H = Lambda / H0  (dimensionless).")
    lines.append("- Universal initial conditions: x0 = 0, a0 = 1, h0 = 1.")
    lines.append("- Physical adot0 is not independently sampled; h0=1 is equivalent to adot0 = H0_phys.")
    lines.append("- Matter density in the code: rho_bar = rho_m0/(Mpred^2 H0^2) = 3 Omega_m0.")
    lines.append("- If scalar is present, q0 is selected by the Hamiltonian/Friedmann constraint E_N(x=0)=0.")
    lines.append("- Mpred is the reduced Planck mass, Mpred = 2.435e27 eV (PHYSICAL, not set to 1).")
    lines.append("- Physical EFT mode keeps eps_HM = H0/Mpred inside the equations.")
    lines.append(f"- EFT validity cut: max_x |h|/lambda_H < {EFT_MAX_H_OVER_LAMBDA:g} (enabled={ENFORCE_EFT_CUTOFF}).")
    lines.append(f"- EH coefficient fixed to {EH_COEFFICIENT_VALUE:g} when detected (enabled={FIX_EH_COEFFICIENT}).")
    lines.append("- Physical Lambda [eV] = lambda_H * H0 [eV].")
    lines.append("")

    standard_cols = {
        "lag_id", "success", "reason", "chi2", "chi2_per_point", "AIC", "BIC",
        "k_params", "max_abs_constraint", "H0_km_s_Mpc", "Omega_m0", "rho_bar",
        "mu_m_over_H0", "varphi0_phi_over_Mp", "q0_dvarphi_dln_a", "eps_HM_H0_over_Mp",
        "lambda_H_Lambda_over_H0", "Lambda_eV",
    }

    for i, row in enumerate(top_rows, 1):
        lag_id = str(row.get("lag_id"))
        H0 = _float_from_row(row, "H0_km_s_Mpc")
        mu = _float_from_row(row, "mu_m_over_H0")
        H0_eV = H0 * KM_S_MPC_TO_EV if np.isfinite(H0) else np.nan
        m_eV = mu * H0_eV if np.isfinite(mu) and np.isfinite(H0_eV) else np.nan
        varphi0_val = _float_from_row(row, "varphi0_phi_over_Mp")
        q0_val = _float_from_row(row, "q0_dvarphi_dln_a")

        lines.append("")
        lines.append("=" * 92)
        lines.append(f"Rank {i}: Lagrangian #{lag_id}")
        lines.append("=" * 92)
        lines.append("")
        lines.append("Raw Lagrangian from pkl")
        lines.append(_raw_lagrangian_string(lag_map, lag_id) if lag_map else "[pkl not found; raw Lagrangian unavailable]")
        terms = _raw_terms_string(lag_map, lag_id) if lag_map else ""
        if terms:
            lines.append("")
            lines.append("Raw terms")
            lines.append(terms)
        lines.append("")
        lines.append("Fit metrics")
        lines.append(f"  chi2            = {_fmt(_float_from_row(row, 'chi2'))}")
        lines.append(f"  chi2 per point  = {_fmt(_float_from_row(row, 'chi2_per_point'))}")
        lines.append(f"  AIC             = {_fmt(_float_from_row(row, 'AIC'))}")
        lines.append(f"  BIC             = {_fmt(_float_from_row(row, 'BIC'))}")
        lines.append(f"  k_params        = {_fmt(_float_from_row(row, 'k_params'), 0)}")
        lines.append(f"  max |E_N|       = {_fmt(_float_from_row(row, 'max_abs_constraint'))}")
        lines.append("")
        lines.append("Initial conditions and sampled/fitted values")
        lines.append("  x0 = ln(a0)                       = 0")
        lines.append("  a0                                = 1")
        lines.append("  h0 = H0/H0                        = 1")
        lines.append("  adot0 / H0_phys                   = 1")
        lines.append(f"  H0_phys [km/s/Mpc]                = {_fmt(H0)}")
        lines.append(f"  H0_phys [eV]                      = {_fmt(H0_eV)}")
        lines.append(f"  Mpred [eV]                        = {_fmt(M_P_REDUCED_EV)}")
        lines.append(f"  eps_HM = H0/Mpred                 = {_fmt(_float_from_row(row, 'eps_HM_H0_over_Mp'))}")
        lambda_H_val = _float_from_row(row, "lambda_H_Lambda_over_H0")
        Lambda_eV_val = _float_from_row(row, "Lambda_eV")
        lines.append(f"  lambda_H = Lambda/H0              = {_fmt(lambda_H_val)}")
        lines.append(f"  Lambda [eV]                       = {_fmt(Lambda_eV_val)}")
        lines.append(f"  Omega_m0                          = {_fmt(_float_from_row(row, 'Omega_m0'))}")
        lines.append(f"  rho_bar = rho_m0/(Mpred^2 H0^2)   = {_fmt(_float_from_row(row, 'rho_bar'))}")
        if np.isfinite(varphi0_val):
            lines.append(f"  varphi0 = phi0/Mpred              = {_fmt(varphi0_val)}")
            lines.append(f"  phi0 [eV]                         = {_fmt(varphi0_val * M_P_REDUCED_EV)}")
        if np.isfinite(q0_val):
            lines.append(f"  q0 = dvarphi/dln(a)|0             = {_fmt(q0_val)}")
            lines.append(f"  phidot0/(Mpred H0) = h0*q0        = {_fmt(q0_val)}")
        if np.isfinite(mu):
            lines.append(f"  mu = m/H0                         = {_fmt(mu)}")
            lines.append(f"  m [eV]                            = {_fmt(m_eV)}")
        extra = []
        for k, v in row.items():
            if k in standard_cols or k.startswith("Unnamed"):
                continue
            try:
                vv = float(v)
                if np.isfinite(vv):
                    extra.append((k, vv))
            except Exception:
                pass
        if extra:
            lines.append("")
            lines.append("Free coupling values used in this best numerical sample")
            for k, vv in sorted(extra):
                lines.append(f"  {k:<16} = {_fmt(vv)}")
        lines.append("")
        lines.append("Numerical solution file")
        lines.append(f"  {sol_paths.get(lag_id, '[not found]')}")

    lines.append("")
    lines.append("=" * 92)
    lines.append("Generated plots")
    lines.append("=" * 92)
    for p in generated_plots:
        lines.append(f"  {p}")
    lines.append("")
    lines.append("Interpretation reminder")
    lines.append("- These are numerical IVP solutions sampled over parameter priors, not analytic formulas.")
    lines.append("- In physical EFT mode, fitted coefficients are interpreted with the H0/Mp hierarchy retained.")
    lines.append("- Use SOLVER_MODE=phenomenological only if you intentionally want effective-coupling scans.")
    lines.append("- This single script first scans/fits models, then writes this top-5 summary.")
    lines.append("- Increase N_SAMPLES_PER_MODEL for a more stable random-search ranking.")
    lines.append("")

    report_path = OUTPUT_DIR / "top5_lagrangians_initial_conditions.txt"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    selected_csv = OUTPUT_DIR / "top5_selected_models.csv"
    with open(selected_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in top_rows:
            writer.writerow(row)

    print(f"\nTop-5 summary written to: {report_path}")
    print(f"Top-5 table written to:   {selected_csv}")
    for p in generated_plots:
        print(f"Top-5 plot written to:    {p}")


def main():
    run_numerical_scan()
    run_top5_summary(top_n=int(os.environ.get("TOP_N", "5")))


if __name__ == "__main__":
    main()