#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_all_lagrangians_bao_solver.py  (v5.0 — two scalar fields)
===============================================================

One-file numerical scanner for all ghost-free FLRW Lagrangians.
Supports two scalar fields φ1 and φ2 with different rescalings:

    φ1 = Mₚ  · φ̃₁     (Planck-scale field)
    φ2 = Λ   · φ̃₂     (EFT-cutoff-scale field)

Core dimensionless variables:
    x  = ln a = -ln(1+z)
    h  = H/H₀
    φ̃₁ = φ₁/Mₚ        ,  q₁ = dφ̃₁/dx
    φ̃₂ = φ₂/Λ          ,  q₂ = dφ̃₂/dx
    λ_H = Λ/H₀         (dimensionless EFT cutoff ratio)
    ε   = H₀/Mₚ        (kept in physical EFT mode)
    μ₁  = m₁/H₀        ,  μ₂ = m₂/Λ
    f̄₁  = f₁/Mₚ        ,  f̄₂ = f₂/Λ

Nondimensionalization substitutions:
    a      → exp(x)
    ȧ      → H₀ exp(x) h
    ä      → H₀² exp(x) (h² + h hₓ)

    φ₁     → Mₚ φ̃₁
    φ̇₁     → Mₚ H₀ h q₁
    φ̈₁     → Mₚ H₀² h (hₓ q₁ + h q₁ₓ)

    φ₂     → H₀ λ_H φ̃₂
    φ̇₂     → H₀² λ_H h q₂
    φ̈₂     → H₀³ λ_H h (hₓ q₂ + h q₂ₓ)

    m₁     → H₀ μ₁   ,  m₂ → Λ μ₂ = H₀ λ_H μ₂
    f₁     → Mₚ f̄₁   ,  f₂ → H₀ λ_H f̄₂
    Λ      → H₀ λ_H
    ρ_{m,0}→ Mₚ² H₀² ρ̄
"""
from __future__ import annotations

import csv
import math
import os
import re
import signal
import time
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

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

BASE_OUTPUT_DIR = Path(os.environ.get(
    "SOLVER_OUTPUT_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "solver_result"),
))


def make_timestamped_output_dir(base_dir: Path) -> Path:
    run_name = os.environ.get("SOLVER_RUN_NAME", "").strip()
    if run_name:
        return base_dir / run_name
    stamp = time.strftime("%Y%m%d_%H%M%S")
    candidate = base_dir / stamp
    suffix = 1
    while candidate.exists():
        candidate = base_dir / f"{stamp}_{suffix:02d}"
        suffix += 1
    return candidate


OUTPUT_DIR = make_timestamped_output_dir(BASE_OUTPUT_DIR)

DATA_CHOICE = "combined"

N_SAMPLES_PER_MODEL = int(os.environ.get("N_SAMPLES_PER_MODEL", "10"))
RANDOM_SEED = int(os.environ.get("RANDOM_SEED", "0"))

# Parallel / progress controls
# Auto policy:
#   - quick scans with <= PARALLEL_SAMPLE_THRESHOLD samples/model run serially
#     to avoid multiprocessing/spawn overhead on macOS.
#   - heavier scans with > PARALLEL_SAMPLE_THRESHOLD samples/model run in parallel.
# You can still force behavior with SOLVER_PARALLEL=1 or SOLVER_PARALLEL=0.
PARALLEL_SAMPLE_THRESHOLD = int(os.environ.get("PARALLEL_SAMPLE_THRESHOLD", "100"))
_SOLVER_PARALLEL_ENV = os.environ.get("SOLVER_PARALLEL", "auto").strip().lower()
if _SOLVER_PARALLEL_ENV in {"1", "true", "yes", "y", "on"}:
    SOLVER_PARALLEL = True
elif _SOLVER_PARALLEL_ENV in {"0", "false", "no", "n", "off"}:
    SOLVER_PARALLEL = False
else:
    SOLVER_PARALLEL = N_SAMPLES_PER_MODEL > PARALLEL_SAMPLE_THRESHOLD
_DEFAULT_WORKERS = max(1, (os.cpu_count() or 2) - 1)
N_WORKERS = int(os.environ.get("N_WORKERS", str(_DEFAULT_WORKERS)))
N_WORKERS = max(1, N_WORKERS)
PROGRESS_EVERY_SECONDS = float(os.environ.get("PROGRESS_EVERY_SECONDS", "10"))
PROGRESS_SAVE_EVERY_MODELS = int(os.environ.get("PROGRESS_SAVE_EVERY_MODELS", "25"))
# 0 disables worker-level messages. Set to e.g. 20 to print every 20 samples per model.
WORKER_SAMPLE_PROGRESS = int(os.environ.get("WORKER_SAMPLE_PROGRESS", "0"))

# Fast parser-level filters. These avoid sending obviously useless models into
# SymPy parsing / nondimensionalization / build. Set to 0 to keep every section
# for audit/debugging.
SKIP_TRIVIAL_DUST_MODELS = os.environ.get(
    "SKIP_TRIVIAL_DUST_MODELS", "1"
).strip().lower() not in {"0", "false", "no", "n", "off"}

# Optional model filters. These are applied before symbolic build, so they save
# the expensive SymPy preprocessing time.
#   SCALAR_CONFIG_FILTER=all                  -> all scalar configurations
#   SCALAR_CONFIG_FILTER=both                 -> only true two-field models
#   SCALAR_CONFIG_FILTER=phi1_only,both       -> selected configs
SCALAR_CONFIG_FILTER = os.environ.get("SCALAR_CONFIG_FILTER", "all").strip()
MAX_MODELS_TO_BUILD = int(os.environ.get("MAX_MODELS_TO_BUILD", "0"))

# Symbolic build controls. These do not change the equations being solved; they
# only control how aggressively SymPy tries to rewrite equivalent expressions.
# "fast" avoids global factorization, which is often the main build bottleneck.
# "cancel" is more canonical but slower. "full" reproduces the older cancel+factor behavior.
BUILD_SIMPLIFY_MODE = os.environ.get("BUILD_SIMPLIFY_MODE", "fast").strip().lower()
USE_LINEAR_RHS_SOLVER = os.environ.get("USE_LINEAR_RHS_SOLVER", "1").strip().lower() not in {"0", "false", "no", "n", "off"}
ALLOW_GENERAL_SYMBOLIC_SOLVE = os.environ.get("ALLOW_GENERAL_SYMBOLIC_SOLVE", "1").strip().lower() not in {"0", "false", "no", "n", "off"}
RHS_SIMPLIFY_MODE = os.environ.get("RHS_SIMPLIFY_MODE", "cancel").strip().lower()
SLOW_BUILD_SECONDS = float(os.environ.get("SLOW_BUILD_SECONDS", "5"))
# Per-model symbolic build wall-time limit. This is an engineering guard only:
# if SymPy spends too long building one model, mark that model as rejected and
# continue to the next one. Set BUILD_TIMEOUT_SECONDS=0 to disable.
BUILD_TIMEOUT_SECONDS = float(os.environ.get("BUILD_TIMEOUT_SECONDS", "60"))

N_GRID = 150
RTOL = 1e-6
ATOL = 1e-8
MAX_ABS_CONSTRAINT = 1e-4

PRIORS = {
    "H0_km_s_Mpc": (60.0, 75.0),
    "Omega_m0": (0.15, 0.45),
    "varphi1_0": (-5, 5),
    "varphi2_0": (-5, 5),
    "log10_mu1": (-3.0, 1.0),
    "log10_mu2": (-3.0, 1.0),
    "log10_fbar1": (-2.0, 2.0),
    "log10_fbar2": (-2.0, 2.0),
    "log10_lambda_H": (
        float(os.environ.get("LOG10_LAMBDA_H_MIN", "2.0")),
        float(os.environ.get("LOG10_LAMBDA_H_MAX", "5.0")),
    ),
    "log10_abs_c": (-10.0, 10.0),
}

# Default is OFF: do not automatically fix the coefficient of the plain EH term M_p^2 c R.
# Set FIX_EH_COEFFICIENT=1 if you want to force c -> EH_COEFFICIENT_VALUE, e.g. 1/2.
FIX_EH_COEFFICIENT = os.environ.get("FIX_EH_COEFFICIENT", "0").strip().lower() not in {"0", "false", "no", "n", "off"}
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

MODE = os.environ.get("SOLVER_MODE", "eft").lower().strip()
if MODE == "physical":
    MODE = "eft"
if MODE == "effective":
    MODE = "phenomenological"

M_P_REDUCED_EV = 2.435e27
KM_S_MPC_TO_EV = 2.133119e-35

# =============================================================================
# Data
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
# Symbolic setup — two scalar fields
# =============================================================================

# Physical FLRW variables (after N=1 gauge fixing in EOM)
a_sym, adot, addot = sp.symbols("a adot addot", real=True)
phi1, phi1dot, phi1ddot = sp.symbols("phi1 phi1dot phi1ddot", real=True)
phi2, phi2dot, phi2ddot = sp.symbols("phi2 phi2dot phi2ddot", real=True)
chi, chidot, chiddot = sp.symbols("chi chidot chiddot", real=True)

M_p = sp.Symbol("M_p", positive=True)
m1_sym = sp.Symbol("m_1", positive=True)
m2_sym = sp.Symbol("m_2", positive=True)
f1_sym = sp.Symbol("f_1", positive=True)
f2_sym = sp.Symbol("f_2", positive=True)
rho_m0 = sp.Symbol("rho_m0", positive=True)
Lambda_sym = sp.Symbol("Lambda_eft", positive=True)

# Greek coefficient symbols (12, matching masker v3.0)
alpha, beta, gamma, delta, epsilon, zeta, eta, theta = sp.symbols(
    "alpha beta gamma delta epsilon zeta eta theta", real=True)
iota_sym, kappa_sym, xi_sym, varpi_sym = sp.symbols(
    "iota kappa xi varpi", real=True)

# Dimensionless e-fold variables
x_sym, h_sym, hx_sym = sp.symbols("x h hx", real=True)
varphi1_sym, q1_sym, q1x_sym = sp.symbols("varphi1 q1 q1x", real=True)
varphi2_sym, q2_sym, q2x_sym = sp.symbols("varphi2 q2 q2x", real=True)
chi_bar_sym, qchi_sym, qchix_sym = sp.symbols("chi_bar qchi qchix", real=True)
H0_sym = sp.Symbol("H0", positive=True)
mu1_sym = sp.Symbol("mu1", positive=True)
mu2_sym = sp.Symbol("mu2", positive=True)
fbar1_sym = sp.Symbol("fbar1", positive=True)
fbar2_sym = sp.Symbol("fbar2", positive=True)
rho_bar_sym = sp.Symbol("rho_bar", positive=True)
eps_HM_sym = sp.Symbol("eps_HM", positive=True)
lambda_H_sym = sp.Symbol("lambda_H", positive=True)


LOCAL_DICT = {
    "a": a_sym, "adot": adot, "addot": addot,
    "phi1": phi1, "phi1dot": phi1dot, "phi1ddot": phi1ddot,
    "phi2": phi2, "phi2dot": phi2dot, "phi2ddot": phi2ddot,
    "chi": chi, "chidot": chidot, "chiddot": chiddot,
    "M_p": M_p, "m_1": m1_sym, "m_2": m2_sym,
    "f_1": f1_sym, "f_2": f2_sym,
    "rho_m0": rho_m0, "Lambda_eft": Lambda_sym,
    "alpha": alpha, "beta": beta, "gamma": gamma, "delta": delta,
    "epsilon": epsilon, "zeta": zeta, "eta": eta, "theta": theta,
    "iota": iota_sym, "kappa": kappa_sym, "xi": xi_sym, "varpi": varpi_sym,
}

BASE_SYMBOLS = {a_sym, adot, addot,
                phi1, phi1dot, phi1ddot,
                phi2, phi2dot, phi2ddot,
                chi, chidot, chiddot,
                M_p, Lambda_sym,
                m1_sym, m2_sym, f1_sym, f2_sym, rho_m0}

PARAM_SYMBOLS = [alpha, beta, gamma, delta, epsilon, zeta, eta, theta,
                 iota_sym, kappa_sym, xi_sym, varpi_sym]


@dataclass
class Model:
    lag_id: str
    general: str
    has_phi1: bool
    has_phi2: bool
    scalar_config: str       # "none", "phi1_only", "phi2_only", "both"
    gf_relations: str
    eom_strings: Dict[str, str]
    eom_exprs: Dict[str, sp.Expr]
    free_symbols: List[sp.Symbol]
    eh_symbol: Optional[sp.Symbol]
    dimless_exprs: Optional[Dict[str, sp.Expr]] = None
    rhs_exprs: Optional[Dict[str, sp.Expr]] = None
    reject_reason: Optional[str] = None
    has_scalaron: bool = False
    scalaron_F_expr: Optional[sp.Expr] = None
    scalaron_f_RR_expr: Optional[sp.Expr] = None
    scalaron_mass_squared_expr: Optional[sp.Expr] = None


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
    varphi1_grid: Optional[np.ndarray] = None
    q1_grid: Optional[np.ndarray] = None
    varphi2_grid: Optional[np.ndarray] = None
    q2_grid: Optional[np.ndarray] = None
    constraint_grid: Optional[np.ndarray] = None
    H_at_data: Optional[np.ndarray] = None


# =============================================================================
# Parsing helpers
# =============================================================================

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
        r"\iota": "iota",
        r"\kappa": "kappa",
        r"\xi": "xi",
        r"\varpi": "varpi",
        r"\Lambda": "Lambda_eft",
        "rho_{m,0}": "rho_m0",
        # Two-scalar derivatives: order matters (longest first)
        "d^2phi1/dt^2": "phi1ddot",
        "d^2phi2/dt^2": "phi2ddot",
        "d^2chi/dt^2": "chiddot",
        "d^2a/dt^2": "addot",
        "dphi1/dt": "phi1dot",
        "dphi2/dt": "phi2dot",
        "dchi/dt": "chidot",
        "da/dt": "adot",
        # Function notation → bare symbols
        "phi1(t)": "phi1",
        "phi2(t)": "phi2",
        "chi(t)": "chi",
        "a(t)": "a",
        # Legacy single-scalar format (backward compat)
        "d^2phi/dt^2": "phi1ddot",
        "dphi/dt": "phi1dot",
        "phi(t)": "phi1",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    # Handle legacy "m" symbol → m_1 when it's not part of m_1 or m_2
    # This is tricky; we skip it and let the local_dict handle it
    return s


def parse_eom_expr(s: str) -> sp.Expr:
    cs = clean_expr_string(s)
    # Extended local dict: also accept bare "m" as m_1 for legacy compat
    ld = dict(LOCAL_DICT)
    ld["m"] = m1_sym
    ld["phi"] = phi1   # legacy single-scalar
    ld["phidot"] = phi1dot
    ld["phiddot"] = phi1ddot
    return parse_expr(cs, local_dict=ld, evaluate=True)


# =============================================================================
# EOM summary loading and model parsing
# =============================================================================

def load_eom_summary() -> str:
    here = Path(__file__).resolve().parent
    candidates = [
        Path(os.environ["EOM_SUMMARY_PATH"]).expanduser()
        if os.environ.get("EOM_SUMMARY_PATH") else None,
        Path.cwd() / "eom_results" / "eom_summary.txt",
        Path.cwd() / "eom_summary.txt",
        here / "eom_results" / "eom_summary.txt",
        here / "eom_summary.txt",
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
                raise ValueError(f"EOM summary found but contains no Lagrangian sections: {p}")
            print(f"[INFO] Loading EOM summary from: {p}")
            return text
    raise FileNotFoundError(
        "No generated EOM summary found. Run EOM_v5_0.py first, then ensure "
        "eom_results/eom_summary.txt exists, or set EOM_SUMMARY_PATH.\n"
        "Tried:\n  " + "\n  ".join(tried)
    )


def extract_general(sec: str) -> str:
    m = re.search(r"^\s*General:\s*(.*)$", sec, flags=re.M)
    return m.group(1).strip() if m else ""


def extract_scalar_config(sec: str) -> str:
    """Extract scalar_config from EOM summary section.  Fall back to has_phi."""
    m = re.search(r"scalar_config:\s*(\w+)", sec)
    if m:
        return m.group(1).strip()
    # Legacy: check has_phi
    m2 = re.search(r"has_phi:\s*(\w+)", sec)
    if m2 and m2.group(1).strip().lower() == "true":
        return "phi1_only"
    return "none"


def extract_scalaron_expr(sec: str, label: str) -> Optional[sp.Expr]:
    """Parse one scalaron health expression emitted by the EOM stage."""
    match = re.search(rf"^\s*{re.escape(label)}:\s*(.*)$", sec, flags=re.M)
    if not match:
        return None
    return parse_eom_expr(match.group(1).strip())


def extract_gf(sec: str) -> str:
    m = re.search(r"Ghost-free coefficient relations:\n(.*?)Final EOM", sec, flags=re.S)
    if not m:
        return ""
    lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
    return "; ".join(lines)


def extract_final_eoms(sec: str) -> Dict[str, str]:
    """Extract the final metric, matter-scalar, and scalaron EOM."""
    out = {}
    m_block = re.search(
        r"Final EOM \(N=1 gauge, ghost-free, symbolic, \+dust\):\n(.*?)(?:\n\s*Ghost-free:|\Z)",
        sec, flags=re.S)
    if not m_block:
        return out
    block = m_block.group(1)
    for key in ["N", "a", "phi1", "phi2", "chi"]:
        m = re.search(rf"^\s*E_{key}\s*=\s*(.*)$", block, flags=re.M)
        if m:
            out[key] = m.group(1).strip()
    # Legacy: E_phi → treat as E_phi1
    if "phi1" not in out:
        m = re.search(r"^\s*E_phi\s*=\s*(.*)$", block, flags=re.M)
        if m:
            out["phi1"] = m.group(1).strip()
    return out


def _compact_eom_string(s: str) -> str:
    """Normalize an EOM string enough for cheap parser-level filtering."""
    return re.sub(r"\s+", "", str(s).strip())


def is_trivial_dust_eom(eom_strings: Dict[str, str]) -> bool:
    """
    True for sections whose final +dust EOM is only
        E_N = -rho_{m,0},  E_a = 0
    and that have no scalar equation.

    These models cannot define a nontrivial background IVP, so skipping them
    before SymPy parsing saves build time without changing viable results.
    """
    if any(k in eom_strings for k in ("phi", "phi1", "phi2", "chi")):
        return False
    en = _compact_eom_string(eom_strings.get("N", ""))
    ea = _compact_eom_string(eom_strings.get("a", ""))
    return en in {"-rho_{m,0}", "-rho_m0"} and ea in {"0", "0.0"}


def parse_models(text: str) -> List[Model]:
    models = []
    n_sections = 0
    n_missing_eom = 0
    n_trivial_dust_fast_skip = 0
    n_parse_failed = 0
    pattern = r"(?:^|\n)═{4,}.*?\nLagrangian #(\d+)\n(.*?)(?=\n═{4,}|\Z)"
    for mm in re.finditer(pattern, text, flags=re.S):
        n_sections += 1
        lag_id, sec = mm.group(1), mm.group(2)
        eom_strings = extract_final_eoms(sec)
        if not eom_strings or "N" not in eom_strings or "a" not in eom_strings:
            n_missing_eom += 1
            continue

        # Important speed-up: skip pure-dust trivial models before parse_expr()
        # and before build_dimless_model(). Many generated high-curvature terms
        # become exactly zero after ghost-free relations, leaving only dust.
        if SKIP_TRIVIAL_DUST_MODELS and is_trivial_dust_eom(eom_strings):
            n_trivial_dust_fast_skip += 1
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
            n_parse_failed += 1
            continue
        free = sorted(
            list(set().union(*(expr.free_symbols for expr in eom_exprs.values())) & set(PARAM_SYMBOLS)),
            key=lambda z: z.name)
        general = extract_general(sec)
        scalar_config = extract_scalar_config(sec)
        has_phi1 = scalar_config in ("phi1_only", "both") or "phi1" in eom_strings
        has_phi2 = scalar_config in ("phi2_only", "both") or "phi2" in eom_strings
        has_scalaron = "chi" in eom_strings or bool(
            re.search(r"scalaron:\s*(?:scalarizable|hybrid)", sec)
        )
        scalaron_F_expr = extract_scalaron_expr(sec, "scalaron_F") if has_scalaron else None
        scalaron_f_RR_expr = extract_scalaron_expr(sec, "scalaron_f_RR") if has_scalaron else None
        scalaron_mass_squared_expr = (
            extract_scalaron_expr(sec, "scalaron_mass_squared") if has_scalaron else None
        )

        # Detect EH coefficient
        eh_symbol = None
        if "M_p²" in general or "M_p^2" in general:
            _greek_map = {
                r"\alpha": alpha, r"\beta": beta, r"\gamma": gamma,
                r"\delta": delta, r"\epsilon": epsilon, r"\zeta": zeta,
                r"\eta": eta, r"\theta": theta,
                r"\iota": iota_sym, r"\kappa": kappa_sym,
                r"\xi": xi_sym, r"\varpi": varpi_sym,
            }
            for latex_name, sym in _greek_map.items():
                pat = re.escape(latex_name) + r"\s*·\s*R(?![_^{a-z])"
                if re.search(pat, general):
                    eh_symbol = sym
                    break
        models.append(Model(
            lag_id=lag_id,
            general=general,
            has_phi1=has_phi1,
            has_phi2=has_phi2,
            scalar_config=scalar_config,
            gf_relations=extract_gf(sec),
            eom_strings=eom_strings,
            eom_exprs=eom_exprs,
            free_symbols=free,
            eh_symbol=eh_symbol,
            has_scalaron=has_scalaron,
            scalaron_F_expr=scalaron_F_expr,
            scalaron_f_RR_expr=scalaron_f_RR_expr,
            scalaron_mass_squared_expr=scalaron_mass_squared_expr,
        ))
    print(
        f"[INFO] parse_models: total_sections={n_sections}, kept={len(models)}, "
        f"fast_skipped_trivial_dust={n_trivial_dust_fast_skip}, "
        f"missing_final_eom={n_missing_eom}, parse_failed={n_parse_failed}, "
        f"skip_trivial={SKIP_TRIVIAL_DUST_MODELS}",
        flush=True,
    )
    return models


# =============================================================================
# Nondimensionalization
# =============================================================================

def _simplify_for_build(expr: sp.Expr, mode: Optional[str] = None) -> sp.Expr:
    """Algebraically equivalent simplification used during symbolic build.

    This controls expression size only; it does not alter the physical equations.
    The previous solver effectively used global cancel+factor. For large two-field
    models, factorization can dominate the build time, so the default "fast" mode
    avoids it.
    """
    mode = (mode or BUILD_SIMPLIFY_MODE).strip().lower()
    if mode in {"0", "none", "off", "raw"}:
        return expr
    if mode in {"fast", "together"}:
        try:
            return sp.together(expr)
        except Exception:
            return expr
    if mode in {"cancel", "safe"}:
        try:
            return sp.cancel(expr)
        except Exception:
            return expr
    if mode in {"full", "factor"}:
        try:
            return sp.cancel(sp.factor(expr))
        except Exception:
            try:
                return sp.cancel(expr)
            except Exception:
                return expr
    # Unknown mode: fail safely by returning the raw expression.
    return expr


def _simplify_rhs_expr(expr: sp.Expr) -> sp.Expr:
    """Post-process RHS expressions before lambdify.

    Keeping a small amount of cancellation here is useful because lambdified RHS
    expressions are evaluated many times during integration. This is much cheaper
    than globally factorizing every dimensionless EOM before the RHS is known.
    """
    return _simplify_for_build(expr, RHS_SIMPLIFY_MODE)


def nondimensionalize_expr(expr: sp.Expr, mode: str = "eft") -> sp.Expr:
    """
    Convert a physical FLRW EOM into the solver's dimensionless variables.

    φ₁ = Mₚ φ̃₁  (Planck-scale rescaling)
    φ₂ = Λ  φ̃₂  (EFT-cutoff rescaling)
    """
    mode = mode.lower().strip()
    if mode == "physical":
        mode = "eft"
    if mode == "effective":
        mode = "phenomenological"

    subs = {
        a_sym: sp.exp(x_sym),
        adot: H0_sym * sp.exp(x_sym) * h_sym,
        addot: H0_sym**2 * sp.exp(x_sym) * (h_sym**2 + h_sym * hx_sym),
        # φ1 rescaled by Mp
        phi1: M_p * varphi1_sym,
        phi1dot: M_p * H0_sym * h_sym * q1_sym,
        phi1ddot: M_p * H0_sym**2 * h_sym * (hx_sym * q1_sym + h_sym * q1x_sym),
        # φ2 rescaled by Λ = H0 λ_H
        phi2: H0_sym * lambda_H_sym * varphi2_sym,
        phi2dot: H0_sym**2 * lambda_H_sym * h_sym * q2_sym,
        phi2ddot: H0_sym**3 * lambda_H_sym * h_sym * (hx_sym * q2_sym + h_sym * q2x_sym),
        # scalaron chi has curvature dimension two
        chi: H0_sym**2 * chi_bar_sym,
        chidot: H0_sym**3 * h_sym * qchi_sym,
        chiddot: H0_sym**4 * h_sym * (hx_sym * qchi_sym + h_sym * qchix_sym),
        # Masses
        m1_sym: H0_sym * mu1_sym,
        m2_sym: H0_sym * lambda_H_sym * mu2_sym,
        # Decay constants
        f1_sym: M_p * fbar1_sym,
        f2_sym: H0_sym * lambda_H_sym * fbar2_sym,
        # EFT cutoff
        Lambda_sym: H0_sym * lambda_H_sym,
        # Matter
        rho_m0: M_p**2 * H0_sym**2 * rho_bar_sym,
    }

    # Keep substitution algebraically exact. Avoid global factorization here;
    # it is extremely expensive for large two-field expressions and is not needed
    # for the physics or for linear RHS extraction.
    e = expr.subs(subs)
    e = _simplify_for_build(e)

    if mode == "phenomenological":
        e = e.subs({M_p: sp.Integer(1), H0_sym: sp.Integer(1)})
    elif mode == "eft":
        e = e.subs({M_p: sp.Integer(1), H0_sym: eps_HM_sym})
        e = e / eps_HM_sym**2
    else:
        raise ValueError("mode must be 'eft'/'physical' or 'phenomenological'/'effective'")
    return _simplify_for_build(e)


def _try_linear_rhs_solve(equations: List[sp.Expr], unknowns: List[sp.Symbol]) -> Optional[Dict[sp.Symbol, sp.Expr]]:
    """Solve the RHS extraction problem as a linear system when possible.

    The FLRW equations after the ghost-free reduction are expected to be linear
    in the highest e-fold derivatives h_x, q1_x, q2_x for the IVP form used by
    this scanner. Using linear algebra avoids SymPy's much heavier general
    symbolic solve and does not change the equations.
    """
    try:
        A, b = sp.linear_eq_to_matrix(equations, unknowns)
        if A.rows != len(unknowns) or A.cols != len(unknowns):
            return None
        sol_vec = A.LUsolve(b)
        return {u: sol_vec[i, 0] for i, u in enumerate(unknowns)}
    except Exception:
        return None


def _try_general_rhs_solve(equations: List[sp.Expr], unknowns: List[sp.Symbol]) -> Optional[Dict[sp.Symbol, sp.Expr]]:
    """Fallback to the original generic SymPy solve path."""
    try:
        sol = sp.solve(equations, unknowns, dict=True, simplify=False)
        if not sol:
            return None
        return sol[0]
    except Exception:
        return None



class BuildTimeoutError(BaseException):
    """Raised by SIGALRM when one model's symbolic build exceeds wall time."""


def _build_timeout_handler(signum, frame):
    raise BuildTimeoutError("symbolic build wall-time limit exceeded")


def build_dimless_model_with_timeout(model: Model, mode: str = "eft", timeout_seconds: float = 0.0) -> Model:
    """
    Run build_dimless_model with a per-model wall-time limit.

    This does not alter the equations, rescaling, or numerical criteria.  It only
    prevents one pathological SymPy expression from blocking the full scan.
    timeout_seconds <= 0 disables the guard.
    """
    timeout_seconds = float(timeout_seconds or 0.0)
    if timeout_seconds <= 0:
        return build_dimless_model(model, mode=mode)

    # signal timers work on Unix/macOS and only in the main thread. The symbolic
    # build loop runs in the main process before the optional ProcessPool scan.
    if not hasattr(signal, "SIGALRM") or not hasattr(signal, "setitimer"):
        return build_dimless_model(model, mode=mode)

    old_handler = signal.getsignal(signal.SIGALRM)
    try:
        signal.signal(signal.SIGALRM, _build_timeout_handler)
        signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
        return build_dimless_model(model, mode=mode)
    except BuildTimeoutError:
        model.reject_reason = f"symbolic build timeout > {timeout_seconds:g}s"
        model.rhs_exprs = None
        try:
            setattr(model, "rhs_solve_method", "timeout")
        except Exception:
            pass
        return model
    finally:
        try:
            signal.setitimer(signal.ITIMER_REAL, 0.0)
        finally:
            signal.signal(signal.SIGALRM, old_handler)

def build_dimless_model(model: Model, mode: str = "eft") -> Model:
    try:
        dim = {k: nondimensionalize_expr(v, mode=mode) for k, v in model.eom_exprs.items()}
        if model.has_scalaron:
            if model.scalaron_F_expr is None or model.scalaron_f_RR_expr is None:
                model.reject_reason = "scalaron health expressions missing from EOM summary"
                return model
            dim["scalaron_F"] = nondimensionalize_expr(model.scalaron_F_expr, mode=mode)
            dim["scalaron_f_RR"] = nondimensionalize_expr(model.scalaron_f_RR_expr, mode=mode)
            if model.scalaron_mass_squared_expr is not None:
                dim["scalaron_mass_squared"] = nondimensionalize_expr(
                    model.scalaron_mass_squared_expr, mode=mode
                )

        # Fix EH coefficient if detected. This is the same normalization as before.
        if FIX_EH_COEFFICIENT and model.eh_symbol is not None:
            dim = {k: _simplify_for_build(v.subs({model.eh_symbol: EH_COEFFICIENT_VALUE})) for k, v in dim.items()}
            model.free_symbols = [s for s in model.free_symbols if s != model.eh_symbol]
        model.dimless_exprs = dim

        # Trivial check. The parser already catches the common pure-dust case,
        # but keep this symbolic guard for non-standard formatting.
        try:
            if sp.simplify(dim["N"] + rho_bar_sym) == 0 and sp.simplify(dim.get("a", 0)) == 0:
                model.reject_reason = "trivial ghost-free final EOM: E_N=-rho_m only, E_a=0"
                return model
        except Exception:
            pass

        # Build the set of unknowns and equations for the IVP RHS.
        unknowns = [hx_sym]
        equations = [dim.get("a", 0)]
        if model.has_phi1 and "phi1" in dim:
            unknowns.append(q1x_sym)
            equations.append(dim["phi1"])
        if model.has_phi2 and "phi2" in dim:
            unknowns.append(q2x_sym)
            equations.append(dim["phi2"])
        if model.has_scalaron and "chi" in dim:
            unknowns.append(qchix_sym)
            equations.append(dim["chi"])

        if not any(eq.has(u) for eq in equations for u in unknowns):
            model.reject_reason = "no e-fold evolution equation for h_x/q_x"
            return model

        solve_method = None
        s0 = None
        if USE_LINEAR_RHS_SOLVER:
            s0 = _try_linear_rhs_solve(equations, unknowns)
            if s0 is not None:
                solve_method = "linear"

        if s0 is None and ALLOW_GENERAL_SYMBOLIC_SOLVE:
            s0 = _try_general_rhs_solve(equations, unknowns)
            if s0 is not None:
                solve_method = "general"

        if s0 is None:
            if USE_LINEAR_RHS_SOLVER and not ALLOW_GENERAL_SYMBOLIC_SOLVE:
                model.reject_reason = "could not extract linear IVP RHS; general symbolic solve disabled"
            else:
                model.reject_reason = "could not solve E_a/E_phi algebraically for h_x/q_x"
            return model

        rhs = {}
        if hx_sym in s0:
            rhs["hx"] = _simplify_rhs_expr(s0[hx_sym])
        else:
            model.reject_reason = "h_x not determined by dynamical EOM"
            return model
        if model.has_phi1 and "phi1" in dim:
            if q1x_sym not in s0:
                model.reject_reason = "q1_x not determined by coupled scalar EOM"
                return model
            rhs["q1x"] = _simplify_rhs_expr(s0[q1x_sym])
        if model.has_phi2 and "phi2" in dim:
            if q2x_sym not in s0:
                model.reject_reason = "q2_x not determined by coupled scalar EOM"
                return model
            rhs["q2x"] = _simplify_rhs_expr(s0[q2x_sym])
        if model.has_scalaron and "chi" in dim:
            if qchix_sym not in s0:
                model.reject_reason = "qchi_x not determined by coupled scalaron EOM"
                return model
            rhs["qchix"] = _simplify_rhs_expr(s0[qchix_sym])
        model.rhs_exprs = rhs
        # Attach a lightweight diagnostic without changing dataclass schema.
        try:
            setattr(model, "rhs_solve_method", solve_method or "unknown")
        except Exception:
            pass
        return model
    except Exception as exc:
        model.reject_reason = f"symbolic build failed: {type(exc).__name__}: {exc}"
        return model


# =============================================================================
# Lambdify and numerical evaluation
# =============================================================================
