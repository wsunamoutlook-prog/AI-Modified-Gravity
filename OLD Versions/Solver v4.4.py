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
# Symbolic setup — two scalar fields
# =============================================================================

# Physical FLRW variables (after N=1 gauge fixing in EOM)
a_sym, adot, addot = sp.symbols("a adot addot", real=True)
phi1, phi1dot, phi1ddot = sp.symbols("phi1 phi1dot phi1ddot", real=True)
phi2, phi2dot, phi2ddot = sp.symbols("phi2 phi2dot phi2ddot", real=True)

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
        "d^2a/dt^2": "addot",
        "dphi1/dt": "phi1dot",
        "dphi2/dt": "phi2dot",
        "da/dt": "adot",
        # Function notation → bare symbols
        "phi1(t)": "phi1",
        "phi2(t)": "phi2",
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


def extract_gf(sec: str) -> str:
    m = re.search(r"Ghost-free coefficient relations:\n(.*?)Final EOM", sec, flags=re.S)
    if not m:
        return ""
    lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
    return "; ".join(lines)


def extract_final_eoms(sec: str) -> Dict[str, str]:
    """Extract E_N, E_a, E_phi1, E_phi2 from the final EOM block."""
    out = {}
    m_block = re.search(
        r"Final EOM \(N=1 gauge, ghost-free, symbolic, \+dust\):\n(.*?)(?:\n\s*Ghost-free:|\Z)",
        sec, flags=re.S)
    if not m_block:
        return out
    block = m_block.group(1)
    for key in ["N", "a", "phi1", "phi2"]:
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
    if any(k in eom_strings for k in ("phi", "phi1", "phi2")):
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


def build_dimless_model(model: Model, mode: str = "eft") -> Model:
    try:
        dim = {k: nondimensionalize_expr(v, mode=mode) for k, v in model.eom_exprs.items()}

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

    # Build the argument list for lambdified functions
    # All functions receive: x, h, varphi1, q1, varphi2, q2, rho_bar, mu1, mu2, fbar1, fbar2, lambda_H, <params>, [eps_HM]
    args_common = [x_sym, h_sym, varphi1_sym, q1_sym, varphi2_sym, q2_sym,
                   rho_bar_sym, mu1_sym, mu2_sym, fbar1_sym, fbar2_sym,
                   lambda_H_sym] + param_syms
    if mode == "eft":
        args_common += [eps_HM_sym]

    C_expr = model.dimless_exprs["N"]
    hx_expr = model.rhs_exprs["hx"]
    q1x_expr = model.rhs_exprs.get("q1x")
    q2x_expr = model.rhs_exprs.get("q2x")

    C_func = sp.lambdify(args_common, C_expr, modules="numpy")
    hx_func = sp.lambdify(args_common, hx_expr, modules="numpy")
    q1x_func = sp.lambdify(args_common, q1x_expr, modules="numpy") if q1x_expr is not None else None
    q2x_func = sp.lambdify(args_common, q2x_expr, modules="numpy") if q2x_expr is not None else None

    return C_func, hx_func, q1x_func, q2x_func, param_syms


def robust_float(val: Any) -> float:
    arr = np.asarray(val, dtype=float)
    if arr.shape == ():
        return float(arr)
    return float(arr.item())


def find_q0_root(C_func, base_args_without_q, q_range=(-MAX_ABS_Q0, MAX_ABS_Q0), n_scan=401) -> Optional[float]:
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
                root = brentq(lambda qq: robust_float(C_func(*base_args_without_q(float(qq)))),
                              grid[i], grid[i+1], maxiter=100)
                if np.isfinite(root):
                    roots.append(float(root))
            except Exception:
                pass
    if not roots:
        return None
    roots_sorted = []
    for r in sorted(roots, key=lambda rr: abs(rr)):
        if not any(abs(r-r0) < 1e-6 for r0 in roots_sorted):
            roots_sorted.append(r)
    preferred = [r for r in roots_sorted if abs(r) <= PREFERRED_ABS_Q0]
    return float((preferred or roots_sorted)[0])


def evaluate_sample(model: Model, data: np.ndarray, rng: np.random.Generator, mode: str,
                    compiled: Optional[Tuple[Any, Any, Any, Any, List[sp.Symbol]]] = None) -> SampleResult:
    mode = "eft" if mode.lower().strip() in {"eft", "physical"} else "phenomenological"
    if model.reject_reason:
        return SampleResult(model.lag_id, False, model.reject_reason)
    if compiled is None:
        try:
            C_func, hx_func, q1x_func, q2x_func, param_syms = lambdify_model(model, mode)
        except Exception as exc:
            return SampleResult(model.lag_id, False, f"lambdify failed: {type(exc).__name__}: {exc}")
    else:
        C_func, hx_func, q1x_func, q2x_func, param_syms = compiled

    H0_km = float(rng.uniform(*PRIORS["H0_km_s_Mpc"]))
    Omega_m0 = float(rng.uniform(*PRIORS["Omega_m0"]))
    rho_bar = 3.0 * Omega_m0
    mu1 = 10.0 ** float(rng.uniform(*PRIORS["log10_mu1"])) if model.has_phi1 else 0.0
    mu2 = 10.0 ** float(rng.uniform(*PRIORS["log10_mu2"])) if model.has_phi2 else 0.0
    fbar1 = 10.0 ** float(rng.uniform(*PRIORS["log10_fbar1"])) if model.has_phi1 else 1.0
    fbar2 = 10.0 ** float(rng.uniform(*PRIORS["log10_fbar2"])) if model.has_phi2 else 1.0
    varphi1_0 = float(rng.uniform(*PRIORS["varphi1_0"])) if model.has_phi1 else 0.0
    varphi2_0 = float(rng.uniform(*PRIORS["varphi2_0"])) if model.has_phi2 else 0.0
    lambda_H = 10.0 ** float(rng.uniform(*PRIORS["log10_lambda_H"]))
    eps_HM = (H0_km * KM_S_MPC_TO_EV) / M_P_REDUCED_EV
    pvals = sample_parameter_values(model, rng, mode)
    pval_list = [pvals[s] for s in param_syms]

    def make_args(xx, hh, v1, qq1, v2, qq2):
        args = [xx, hh, v1, qq1, v2, qq2, rho_bar, mu1, mu2, fbar1, fbar2, lambda_H] + pval_list
        if mode == "eft":
            args.append(eps_HM)
        return args

    # ── Determine initial q1_0 from constraint E_N(x=0) = 0 ──
    has_any_scalar = model.has_phi1 or model.has_phi2
    if has_any_scalar and (q1x_func is not None or q2x_func is not None):
        # If model has phi1, solve for q1_0 at fixed q2_0=0 (or sampled q2_0)
        # If model has only phi2, solve for q2_0 at q1_0=0
        if model.has_phi1:
            # Sample q2_0 randomly if phi2 is present, then solve for q1_0
            q2_0 = float(rng.uniform(-PREFERRED_ABS_Q0, PREFERRED_ABS_Q0)) if model.has_phi2 else 0.0
            def base_args(qtrial):
                return make_args(0.0, 1.0, varphi1_0, qtrial, varphi2_0, q2_0)
            q1_0 = find_q0_root(C_func, base_args)
            if q1_0 is None:
                return SampleResult(model.lag_id, False, "no acceptable real q1_0 root from E_N(x=0)=0")
        else:
            # phi2_only: solve for q2_0
            q1_0 = 0.0
            def base_args(qtrial):
                return make_args(0.0, 1.0, 0.0, 0.0, varphi2_0, qtrial)
            q2_0 = find_q0_root(C_func, base_args)
            if q2_0 is None:
                return SampleResult(model.lag_id, False, "no acceptable real q2_0 root from E_N(x=0)=0")
    else:
        q1_0, q2_0 = 0.0, 0.0
        try:
            C0 = robust_float(C_func(*make_args(0.0, 1.0, 0.0, 0.0, 0.0, 0.0)))
            if not np.isfinite(C0) or abs(C0) > 1e-6:
                return SampleResult(model.lag_id, False,
                                    f"no-scalar constraint not satisfied at x=0: C0={C0:.3e}")
        except Exception as exc:
            return SampleResult(model.lag_id, False,
                                f"no-scalar constraint eval failed: {type(exc).__name__}")

    # ── Check RHS at initial point ──
    try:
        args0 = make_args(0.0, 1.0, varphi1_0, q1_0, varphi2_0, q2_0)
        hx0 = robust_float(hx_func(*args0))
        if not np.isfinite(hx0) or abs(hx0) > 1e6:
            return SampleResult(model.lag_id, False, "initial h_x is singular or absurd")
        if model.has_phi1 and q1x_func is not None:
            q1x0 = robust_float(q1x_func(*args0))
            if not np.isfinite(q1x0) or abs(q1x0) > 1e6:
                return SampleResult(model.lag_id, False, "initial q1_x is singular or absurd")
        if model.has_phi2 and q2x_func is not None:
            q2x0 = robust_float(q2x_func(*args0))
            if not np.isfinite(q2x0) or abs(q2x0) > 1e6:
                return SampleResult(model.lag_id, False, "initial q2_x is singular or absurd")
    except Exception as exc:
        return SampleResult(model.lag_id, False, f"initial RHS failed: {type(exc).__name__}")

    # ── Integration ──
    z_data = data[:, 0]
    H_obs = data[:, 1]
    sig = data[:, 2]
    zmax = float(np.max(z_data))
    xmin = -math.log(1.0 + zmax)
    x_eval = np.linspace(0.0, xmin, N_GRID)

    # Build state vector: [h, (varphi1, q1)?, (varphi2, q2)?]
    y0_list = [1.0]
    # Track index mapping
    idx_h = 0
    idx_v1 = idx_q1 = idx_v2 = idx_q2 = None
    ci = 1
    if model.has_phi1:
        y0_list.extend([varphi1_0, q1_0])
        idx_v1, idx_q1 = ci, ci + 1
        ci += 2
    if model.has_phi2:
        y0_list.extend([varphi2_0, q2_0])
        idx_v2, idx_q2 = ci, ci + 1
        ci += 2
    y0 = np.array(y0_list, dtype=float)
    n_state = len(y0)

    def rhs(xx, yy):
        try:
            hh = float(yy[idx_h])
            v1 = float(yy[idx_v1]) if idx_v1 is not None else 0.0
            qq1 = float(yy[idx_q1]) if idx_q1 is not None else 0.0
            v2 = float(yy[idx_v2]) if idx_v2 is not None else 0.0
            qq2 = float(yy[idx_q2]) if idx_q2 is not None else 0.0
            args = make_args(xx, hh, v1, qq1, v2, qq2)
            dydt = np.zeros(n_state, dtype=float)
            dydt[idx_h] = robust_float(hx_func(*args))
            if idx_v1 is not None:
                dydt[idx_v1] = qq1
                dydt[idx_q1] = robust_float(q1x_func(*args))
            if idx_v2 is not None:
                dydt[idx_v2] = qq2
                dydt[idx_q2] = robust_float(q2x_func(*args))
            return dydt
        except Exception:
            return np.full(n_state, np.nan, dtype=float)

    try:
        sol = solve_ivp(rhs, (0.0, xmin), y0, t_eval=x_eval, dense_output=True,
                        method="DOP853", rtol=RTOL, atol=ATOL)
    except Exception as exc:
        return SampleResult(model.lag_id, False, f"solve_ivp exception: {type(exc).__name__}: {exc}")
    if not sol.success:
        return SampleResult(model.lag_id, False, f"solve_ivp failed: {sol.message}")
    if not np.all(np.isfinite(sol.y)):
        return SampleResult(model.lag_id, False, "trajectory contains NaN/inf")

    h_grid = sol.y[idx_h]
    if np.any(h_grid <= MIN_H):
        return SampleResult(model.lag_id, False, "h(x)<=0 on trajectory")
    if ENFORCE_EFT_CUTOFF:
        max_h_over_lambda = float(np.max(np.abs(h_grid) / lambda_H))
        if max_h_over_lambda > EFT_MAX_H_OVER_LAMBDA:
            return SampleResult(model.lag_id, False,
                                f"EFT cutoff violated: max(h/lambda_H)={max_h_over_lambda:.3e}")

    varphi1_grid = sol.y[idx_v1] if idx_v1 is not None else None
    q1_grid = sol.y[idx_q1] if idx_q1 is not None else None
    varphi2_grid = sol.y[idx_v2] if idx_v2 is not None else None
    q2_grid = sol.y[idx_q2] if idx_q2 is not None else None

    if varphi1_grid is not None and np.max(np.abs(varphi1_grid)) > MAX_ABS_VARPHI_TRAJ:
        return SampleResult(model.lag_id, False, "|varphi1| trajectory too large")
    if q1_grid is not None and np.max(np.abs(q1_grid)) > MAX_ABS_Q_TRAJ:
        return SampleResult(model.lag_id, False, "|q1| trajectory too large")
    if varphi2_grid is not None and np.max(np.abs(varphi2_grid)) > MAX_ABS_VARPHI_TRAJ:
        return SampleResult(model.lag_id, False, "|varphi2| trajectory too large")
    if q2_grid is not None and np.max(np.abs(q2_grid)) > MAX_ABS_Q_TRAJ:
        return SampleResult(model.lag_id, False, "|q2| trajectory too large")

    z_grid = np.exp(-x_eval) - 1.0
    H_grid_phys = H0_km * h_grid
    if np.any(H_grid_phys > MAX_H_KM_S_MPC):
        return SampleResult(model.lag_id, False, "H(z) absurdly large")

    # ── Constraint residual along trajectory ──
    C_vals = []
    try:
        for i, xx in enumerate(x_eval):
            hh = float(h_grid[i])
            v1 = float(varphi1_grid[i]) if varphi1_grid is not None else 0.0
            qq1 = float(q1_grid[i]) if q1_grid is not None else 0.0
            v2 = float(varphi2_grid[i]) if varphi2_grid is not None else 0.0
            qq2 = float(q2_grid[i]) if q2_grid is not None else 0.0
            C_vals.append(robust_float(C_func(*make_args(float(xx), hh, v1, qq1, v2, qq2))))
        C_vals = np.array(C_vals, dtype=float)
    except Exception as exc:
        return SampleResult(model.lag_id, False, f"constraint monitor failed: {type(exc).__name__}")
    if not np.all(np.isfinite(C_vals)):
        return SampleResult(model.lag_id, False, "constraint residual NaN/inf")
    maxC = float(np.max(np.abs(C_vals)))
    if maxC > MAX_ABS_CONSTRAINT:
        return SampleResult(model.lag_id, False, f"constraint drift too large: max|C|={maxC:.3e}")

    # ── chi2 at data points ──
    try:
        x_data = -np.log1p(z_data)
        y_data = sol.sol(x_data)
        h_data = y_data[idx_h]
        H_model = H0_km * h_data
    except Exception as exc:
        return SampleResult(model.lag_id, False, f"dense output failed: {type(exc).__name__}")
    if not np.all(np.isfinite(H_model)):
        return SampleResult(model.lag_id, False, "H_model at data not finite")
    chi2 = float(np.sum(((H_model - H_obs) / sig) ** 2))
    n = len(z_data)

    # Count free sampled parameters
    uses_lambda = any(expr.has(lambda_H_sym) for expr in model.dimless_exprs.values())
    n_scalar_params = 0
    if model.has_phi1:
        n_scalar_params += 2  # varphi1_0, mu1
    if model.has_phi2:
        n_scalar_params += 2  # varphi2_0, mu2
    # fbar1/fbar2 only count if the dimless EOM actually uses them
    uses_fbar1 = any(expr.has(fbar1_sym) for expr in model.dimless_exprs.values())
    uses_fbar2 = any(expr.has(fbar2_sym) for expr in model.dimless_exprs.values())
    if uses_fbar1:
        n_scalar_params += 1
    if uses_fbar2:
        n_scalar_params += 1
    # In two-field models, q2_0 is sampled freely while q1_0 is solved from the constraint.
    # Count this extra initial-condition parameter in AIC/BIC.
    if model.has_phi1 and model.has_phi2:
        n_scalar_params += 1

    k = 2 + (1 if uses_lambda else 0) + len(param_syms) + n_scalar_params
    aic = chi2 + 2.0 * k
    bic = chi2 + k * math.log(n)

    params = {
        "H0_km_s_Mpc": H0_km,
        "Omega_m0": Omega_m0,
        "rho_bar": rho_bar,
        "mu1_m1_over_H0": mu1,
        "mu2_m2_over_Lambda": mu2,
        "fbar1_f1_over_Mp": fbar1,
        "fbar2_f2_over_Lambda": fbar2,
        "varphi1_0_phi1_over_Mp": varphi1_0,
        "varphi2_0_phi2_over_Lambda": varphi2_0,
        "q1_0_dvarphi1_dln_a": q1_0,
        "q2_0_dvarphi2_dln_a": q2_0,
        "eps_HM_H0_over_Mp": eps_HM,
        "lambda_H_Lambda_over_H0": lambda_H,
        "Lambda_eV": lambda_H * H0_km * KM_S_MPC_TO_EV,
    }
    for s, v in pvals.items():
        params[str(s)] = float(v)

    return SampleResult(
        lag_id=model.lag_id, success=True, reason="ok", chi2=chi2,
        chi2_per_point=chi2 / n, aic=aic, bic=bic, k_params=k,
        params=params, max_abs_constraint=maxC,
        x_grid=x_eval, z_grid=z_grid, h_grid=h_grid, H_grid=H_grid_phys,
        varphi1_grid=varphi1_grid, q1_grid=q1_grid,
        varphi2_grid=varphi2_grid, q2_grid=q2_grid,
        constraint_grid=C_vals, H_at_data=H_model,
    )


# =============================================================================
# LCDM reference
# =============================================================================

def lcdm_fit_reference(data: np.ndarray) -> Dict[str, float]:
    z, Hobs, sig = data[:, 0], data[:, 1], data[:, 2]
    best = {"chi2": math.inf}
    for H0 in np.linspace(55, 80, 501):
        for Om in np.linspace(0.05, 0.6, 551):
            h_l = np.sqrt(Om * (1 + z) ** 3 + (1 - Om))
            Hm = H0 * h_l
            c2 = float(np.sum(((Hm - Hobs) / sig) ** 2))
            if c2 < best["chi2"]:
                best = {"H0": float(H0), "Omega_m0": float(Om), "chi2": c2, "chi2_per_point": c2 / len(z)}
    k = 2
    n = len(z)
    best["AIC"] = best["chi2"] + 2 * k
    best["BIC"] = best["chi2"] + k * math.log(n)
    return best


# =============================================================================
# I/O helpers
# =============================================================================

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
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(data[:, 0], data[:, 1], yerr=data[:, 2], fmt="o", capsize=3, label=f"{DATA_CHOICE} H(z) data")
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
    rows = []
    for i in range(len(best.x_grid)):
        row = {
            "x_ln_a": float(best.x_grid[i]),
            "z": float(best.z_grid[i]),
            "h_dimensionless": float(best.h_grid[i]),
            "H_km_s_Mpc": float(best.H_grid[i]),
            "constraint_residual": float(best.constraint_grid[i]),
        }
        if best.varphi1_grid is not None:
            row["varphi1_phi1_over_Mp"] = float(best.varphi1_grid[i])
            row["q1_dvarphi1_dln_a"] = float(best.q1_grid[i])
        if best.varphi2_grid is not None:
            row["varphi2_phi2_over_Lambda"] = float(best.varphi2_grid[i])
            row["q2_dvarphi2_dln_a"] = float(best.q2_grid[i])
        rows.append(row)
    write_csv(path, rows)



# =============================================================================
# Parallel scan helpers
# =============================================================================

def _seed_for_model(base_seed: int, lag_id: str, fallback_seed: int) -> int:
    """Stable per-model seed. If RANDOM_SEED=0, fallback_seed is generated in main."""
    try:
        lid = int(lag_id)
    except Exception:
        lid = abs(hash(lag_id)) % 1_000_000
    seed0 = int(base_seed) if int(base_seed) != 0 else int(fallback_seed)
    return int((seed0 + 1_000_003 * lid) % (2**32 - 1))


def _format_seconds(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    if seconds < 60:
        return f"{seconds:.0f}s"
    if seconds < 3600:
        return f"{seconds/60:.1f}m"
    return f"{seconds/3600:.2f}h"


def _scan_single_model_worker(args: Tuple[Model, np.ndarray, str, int, int, int]) -> Dict[str, Any]:
    """Worker entry point: lambdify once, then evaluate many samples for one model."""
    model, data, mode, n_samples, seed, worker_sample_progress = args
    t_model = time.time()
    rejects = Counter()
    accepted: List[SampleResult] = []
    best: Optional[SampleResult] = None

    if model.reject_reason:
        rejects[model.reject_reason] += n_samples
        return {
            "lag_id": model.lag_id,
            "accepted": accepted,
            "best": best,
            "rejects": dict(rejects),
            "elapsed": time.time() - t_model,
            "samples": n_samples,
            "status": "skipped",
        }

    try:
        compiled = lambdify_model(model, mode)
    except Exception as exc:
        rejects[f"lambdify failed: {type(exc).__name__}: {exc}"] += n_samples
        return {
            "lag_id": model.lag_id,
            "accepted": accepted,
            "best": best,
            "rejects": dict(rejects),
            "elapsed": time.time() - t_model,
            "samples": n_samples,
            "status": "lambdify_failed",
        }

    rng = np.random.default_rng(seed)
    for i in range(n_samples):
        res = evaluate_sample(model, data, rng, mode, compiled=compiled)
        if res.success:
            accepted.append(res)
            if best is None or res.aic < best.aic:
                best = res
        else:
            rejects[res.reason] += 1

        if worker_sample_progress > 0 and (i + 1) % worker_sample_progress == 0:
            print(
                f"[worker] L#{model.lag_id}: {i+1}/{n_samples} samples, "
                f"accepted={len(accepted)}, elapsed={_format_seconds(time.time() - t_model)}",
                flush=True,
            )

    return {
        "lag_id": model.lag_id,
        "accepted": accepted,
        "best": best,
        "rejects": dict(rejects),
        "elapsed": time.time() - t_model,
        "samples": n_samples,
        "status": "done",
    }


def _write_partial_progress(output_dir: Path,
                            all_results: List[SampleResult],
                            best_by_model: Dict[str, SampleResult],
                            reject_counts_by_model: Dict[str, Counter],
                            label: str = "partial"):
    """Write lightweight CSV snapshots during a long scan."""
    try:
        accepted = sorted(all_results, key=lambda r: (r.aic, r.chi2))
        model_best_list = sorted(best_by_model.values(), key=lambda r: (r.aic, r.chi2))
        write_csv(output_dir / f"accepted_samples_summary_{label}.csv", [result_row(r) for r in accepted])
        write_csv(output_dir / f"model_ranking_{label}.csv", [result_row(r) for r in model_best_list])
        rej_rows = []
        for lid, cnt in sorted(reject_counts_by_model.items(), key=lambda kv: int(kv[0])):
            total = sum(cnt.values())
            for reason, n in cnt.most_common(8):
                rej_rows.append({"lag_id": lid, "count": n, "total_rejected_or_skipped": total, "reason": reason})
        write_csv(output_dir / f"reject_reasons_by_model_{label}.csv", rej_rows)
    except Exception as exc:
        print(f"[WARN] Failed to write partial progress files: {type(exc).__name__}: {exc}", flush=True)


def _merge_worker_output(out: Dict[str, Any],
                         all_results: List[SampleResult],
                         best_by_model: Dict[str, SampleResult],
                         reject_counts_by_model: Dict[str, Counter]):
    lag_id = str(out["lag_id"])
    for res in out.get("accepted", []):
        all_results.append(res)
    best = out.get("best")
    if best is not None:
        current = best_by_model.get(lag_id)
        if current is None or best.aic < current.aic:
            best_by_model[lag_id] = best
    for reason, n in out.get("rejects", {}).items():
        reject_counts_by_model[lag_id][reason] += int(n)

# =============================================================================
# Main scan
# =============================================================================

def run_numerical_scan():
    t0 = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = select_data(DATA_CHOICE)
    print(f"[START] Output directory: {OUTPUT_DIR}", flush=True)
    print(
        f"[START] N_SAMPLES_PER_MODEL={N_SAMPLES_PER_MODEL}, "
        f"parallel={SOLVER_PARALLEL}, workers={N_WORKERS}, "
        f"parallel_threshold={PARALLEL_SAMPLE_THRESHOLD}, "
        f"skip_trivial_dust={SKIP_TRIVIAL_DUST_MODELS}, "
        f"scalar_filter={SCALAR_CONFIG_FILTER}, "
        f"build_simplify={BUILD_SIMPLIFY_MODE}, "
        f"linear_rhs={USE_LINEAR_RHS_SOLVER}, general_solve={ALLOW_GENERAL_SYMBOLIC_SOLVE}",
        flush=True,
    )

    summary_text = load_eom_summary()
    models_raw = parse_models(summary_text)

    # Optional scalar-configuration filter before symbolic build.
    if SCALAR_CONFIG_FILTER.lower() not in {"", "all"}:
        allowed_configs = {s.strip() for s in SCALAR_CONFIG_FILTER.split(",") if s.strip()}
        before_filter = len(models_raw)
        models_raw = [m for m in models_raw if m.scalar_config in allowed_configs]
        print(
            f"[INFO] scalar_config filter={sorted(allowed_configs)}: "
            f"{before_filter} -> {len(models_raw)} models before build.",
            flush=True,
        )

    # Optional hard cap for quick debugging / chunked scans.
    if MAX_MODELS_TO_BUILD > 0 and len(models_raw) > MAX_MODELS_TO_BUILD:
        before_cap = len(models_raw)
        models_raw = models_raw[:MAX_MODELS_TO_BUILD]
        print(
            f"[INFO] MAX_MODELS_TO_BUILD={MAX_MODELS_TO_BUILD}: "
            f"{before_cap} -> {len(models_raw)} models before build.",
            flush=True,
        )

    print(f"[INFO] Parsed {len(models_raw)} Lagrangian sections from EOM summary.", flush=True)

    # Symbolic dimensionless build can also be slow; make it visible.
    built_models: List[Model] = []
    build_t0 = time.time()
    last_build_print = build_t0
    recent_build_times = []
    for i, m in enumerate(models_raw, 1):
        t_model = time.time()
        bm = build_dimless_model(m, mode=MODE)
        dt_model = time.time() - t_model
        built_models.append(bm)
        recent_build_times.append(dt_model)
        if len(recent_build_times) > 50:
            recent_build_times.pop(0)

        if dt_model >= SLOW_BUILD_SECONDS:
            method = getattr(bm, "rhs_solve_method", "rejected") if not bm.reject_reason else "rejected"
            print(
                f"[SLOW_BUILD] L#{m.lag_id}, scalar_config={m.scalar_config}, "
                f"elapsed={_format_seconds(dt_model)}, method={method}, "
                f"reject={bm.reject_reason}",
                flush=True,
            )

        now = time.time()
        if i == 1 or i == len(models_raw) or now - last_build_print >= PROGRESS_EVERY_SECONDS:
            elapsed = now - build_t0
            rate = i / max(elapsed, 1e-9)
            eta_avg = (len(models_raw) - i) / rate if rate > 0 else float("nan")
            if recent_build_times:
                med_recent = float(np.median(recent_build_times))
                eta_recent = (len(models_raw) - i) * med_recent
            else:
                eta_recent = eta_avg
            n_ready = sum(1 for mm in built_models if not mm.reject_reason)
            n_linear = sum(1 for mm in built_models if getattr(mm, "rhs_solve_method", None) == "linear")
            n_general = sum(1 for mm in built_models if getattr(mm, "rhs_solve_method", None) == "general")
            print(
                f"[BUILD] {i}/{len(models_raw)} models built "
                f"({100*i/max(len(models_raw),1):.1f}%), usable_so_far={n_ready}, "
                f"linear={n_linear}, general={n_general}, "
                f"elapsed={_format_seconds(elapsed)}, ETA_avg={_format_seconds(eta_avg)}, "
                f"ETA_recent={_format_seconds(eta_recent)}",
                flush=True,
            )
            last_build_print = now

    all_results: List[SampleResult] = []
    best_by_model: Dict[str, SampleResult] = {}
    reject_counts_by_model: Dict[str, Counter] = defaultdict(Counter)

    skipped = [m for m in built_models if m.reject_reason]
    active_models = [m for m in built_models if not m.reject_reason]
    for m in skipped:
        reject_counts_by_model[m.lag_id][m.reject_reason] += N_SAMPLES_PER_MODEL

    print(
        f"[INFO] Built models: total={len(built_models)}, active_IVP={len(active_models)}, "
        f"structurally_skipped={len(skipped)}",
        flush=True,
    )
    print(
        f"[INFO] Total numerical samples scheduled: {len(active_models) * N_SAMPLES_PER_MODEL:,}",
        flush=True,
    )

    # Stable random base seed for reproducibility. RANDOM_SEED=0 chooses a fresh base.
    fallback_seed = int(time.time_ns() % (2**32 - 1))
    scan_t0 = time.time()
    completed = 0
    last_progress_print = scan_t0

    if SOLVER_PARALLEL and len(active_models) > 1 and N_WORKERS > 1:
        ctx = mp.get_context("spawn")
        max_workers = min(N_WORKERS, len(active_models))
        print(f"[SCAN] Starting ProcessPoolExecutor with {max_workers} workers...", flush=True)
        worker_args = [
            (m, data, MODE, N_SAMPLES_PER_MODEL,
             _seed_for_model(RANDOM_SEED, m.lag_id, fallback_seed), WORKER_SAMPLE_PROGRESS)
            for m in active_models
        ]
        with ProcessPoolExecutor(max_workers=max_workers, mp_context=ctx) as ex:
            future_to_lag = {ex.submit(_scan_single_model_worker, arg): arg[0].lag_id for arg in worker_args}
            for fut in as_completed(future_to_lag):
                lag_id = future_to_lag[fut]
                try:
                    out = fut.result()
                except Exception as exc:
                    # Worker crashed. Count all samples as rejected for that model.
                    reject_counts_by_model[str(lag_id)][f"worker crashed: {type(exc).__name__}: {exc}"] += N_SAMPLES_PER_MODEL
                    out = {"lag_id": lag_id, "accepted": [], "best": None, "rejects": {}, "elapsed": 0.0, "samples": N_SAMPLES_PER_MODEL, "status": "crashed"}
                _merge_worker_output(out, all_results, best_by_model, reject_counts_by_model)
                completed += 1

                now = time.time()
                should_print = (now - last_progress_print >= PROGRESS_EVERY_SECONDS) or completed == len(active_models)
                if should_print:
                    elapsed = now - scan_t0
                    rate = completed / max(elapsed, 1e-9)
                    eta = (len(active_models) - completed) / rate if rate > 0 else float("nan")
                    accepted_count = len(all_results)
                    best_aic = min((r.aic for r in best_by_model.values()), default=math.inf)
                    print(
                        f"[PROGRESS] completed_models={completed}/{len(active_models)} "
                        f"({100*completed/max(len(active_models),1):.1f}%), "
                        f"accepted_samples={accepted_count}, best_AIC={best_aic:.6g}, "
                        f"elapsed={_format_seconds(elapsed)}, ETA={_format_seconds(eta)}",
                        flush=True,
                    )
                    last_progress_print = now

                if PROGRESS_SAVE_EVERY_MODELS > 0 and (completed % PROGRESS_SAVE_EVERY_MODELS == 0):
                    _write_partial_progress(OUTPUT_DIR, all_results, best_by_model, reject_counts_by_model, label="partial")
                    print(f"[CHECKPOINT] Partial CSVs written in {OUTPUT_DIR}", flush=True)
    else:
        print("[SCAN] Running serial scan with lambdify cached once per model...", flush=True)
        for m in active_models:
            seed = _seed_for_model(RANDOM_SEED, m.lag_id, fallback_seed)
            out = _scan_single_model_worker((m, data, MODE, N_SAMPLES_PER_MODEL, seed, WORKER_SAMPLE_PROGRESS))
            _merge_worker_output(out, all_results, best_by_model, reject_counts_by_model)
            completed += 1
            now = time.time()
            elapsed = now - scan_t0
            rate = completed / max(elapsed, 1e-9)
            eta = (len(active_models) - completed) / rate if rate > 0 else float("nan")
            best_aic = min((r.aic for r in best_by_model.values()), default=math.inf)
            print(
                f"[PROGRESS] completed_models={completed}/{len(active_models)} "
                f"({100*completed/max(len(active_models),1):.1f}%), "
                f"L#{m.lag_id} accepted={len(out.get('accepted', []))}, "
                f"best_AIC={best_aic:.6g}, elapsed={_format_seconds(elapsed)}, ETA={_format_seconds(eta)}",
                flush=True,
            )
            if PROGRESS_SAVE_EVERY_MODELS > 0 and (completed % PROGRESS_SAVE_EVERY_MODELS == 0):
                _write_partial_progress(OUTPUT_DIR, all_results, best_by_model, reject_counts_by_model, label="partial")
                print(f"[CHECKPOINT] Partial CSVs written in {OUTPUT_DIR}", flush=True)

    # Final checkpoint before report/plots.
    _write_partial_progress(OUTPUT_DIR, all_results, best_by_model, reject_counts_by_model, label="partial")

    accepted = sorted(all_results, key=lambda r: (r.aic, r.chi2))
    model_best_list = sorted(best_by_model.values(), key=lambda r: (r.aic, r.chi2))
    best = accepted[0] if accepted else None
    lcdm = lcdm_fit_reference(data)

    write_csv(OUTPUT_DIR / "accepted_samples_summary.csv", [result_row(r) for r in accepted])
    write_csv(OUTPUT_DIR / "model_ranking.csv", [result_row(r) for r in model_best_list])
    write_best_solution(best, OUTPUT_DIR / "best_solution.csv")
    plot_best(data, best, OUTPUT_DIR / "best_fit_Hz.png")

    for rank, r in enumerate(model_best_list[:10], 1):
        write_best_solution(r, OUTPUT_DIR / f"top_{rank:02d}_lagrangian_{r.lag_id}_solution.csv")

    rej_rows = []
    for lid, cnt in sorted(reject_counts_by_model.items(), key=lambda kv: int(kv[0])):
        total = sum(cnt.values())
        for reason, n in cnt.most_common(8):
            rej_rows.append({"lag_id": lid, "count": n, "total_rejected_or_skipped": total, "reason": reason})
    write_csv(OUTPUT_DIR / "reject_reasons_by_model.csv", rej_rows)

    lines = []
    lines.append("AI Modified Gravity: automatic ghost-free Lagrangian H(z) scan (v5.0 — two scalars)")
    lines.append("=" * 78)
    lines.append(f"Base output directory: {BASE_OUTPUT_DIR}")
    lines.append(f"Run output directory: {OUTPUT_DIR}")
    lines.append(f"Run time: {time.time() - t0:.2f} s")
    lines.append(f"Mode: {MODE}")
    lines.append(f"Data choice: {DATA_CHOICE}; N_data={len(data)}; z_max={float(np.max(data[:, 0])):.3f}")
    lines.append(f"Parsed Lagrangians: {len(models_raw)}")
    lines.append(f"Built nontrivial IVP models: {sum(1 for m in built_models if not m.reject_reason)}")
    lines.append(f"Samples per model: {N_SAMPLES_PER_MODEL}")
    lines.append(f"Parallel enabled: {SOLVER_PARALLEL}; workers={N_WORKERS if SOLVER_PARALLEL else 1}")
    lines.append(f"Parallel auto threshold: N_SAMPLES_PER_MODEL > {PARALLEL_SAMPLE_THRESHOLD}")
    lines.append(f"Parser fast-skip trivial dust models: {SKIP_TRIVIAL_DUST_MODELS}")
    lines.append(f"Scalar config filter: {SCALAR_CONFIG_FILTER}")
    lines.append(f"Build simplify mode: {BUILD_SIMPLIFY_MODE}")
    lines.append(f"Use linear RHS solver: {USE_LINEAR_RHS_SOLVER}; allow general solve: {ALLOW_GENERAL_SYMBOLIC_SOLVE}")
    lines.append(f"Accepted samples: {len(accepted)}")
    lines.append("")
    lines.append("Physics conventions")
    lines.append("- Uses x=ln(a)=-ln(1+z), h=H/H0.")
    lines.append("- Scalar field 1: varphi1=phi1/Mp, q1=dvarphi1/dx.  phi1 is Planck-scale.")
    lines.append("- Scalar field 2: varphi2=phi2/Lambda, q2=dvarphi2/dx.  phi2 is EFT-cutoff-scale.")
    lines.append("- Masses: mu1=m1/H0, mu2=m2/Lambda.")
    lines.append("- Decay constants: fbar1=f1/Mp, fbar2=f2/Lambda.")
    lines.append("- EFT cutoff: lambda_H=Lambda/H0.")
    lines.append("- Default physical EFT mode keeps eps_HM=H0/Mp in the dimensionless equations.")
    lines.append("- EOMs are normalized by Mp^2 H0^2 after substitution.")
    lines.append(f"- EFT validity cut: max_x |h|/lambda_H < {EFT_MAX_H_OVER_LAMBDA:g} (enabled={ENFORCE_EFT_CUTOFF}).")
    lines.append(f"- EH coefficient fixed to {EH_COEFFICIENT_VALUE:g} when detected (enabled={FIX_EH_COEFFICIENT}).")
    lines.append("- a0 and h0 are fixed to 1.")
    lines.append("- q1_0 is solved from E_N(x=0)=0 for phi1 models; q2_0 for phi2-only models.")
    lines.append("- rho_m0 is sampled as rho_bar=3 Omega_m0.")
    lines.append("- Mp = 2.435e27 eV (physical reduced Planck mass).")
    lines.append("")
    lines.append("Flat-LambdaCDM reference fit")
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
            lines.append(f"  Scalar config: {bm.scalar_config}")
            lines.append(f"  Ghost-free relations: {bm.gf_relations}")
            lines.append("  Free symbols: " + ", ".join(str(s) for s in bm.free_symbols))
        lines.append("  Parameters:")
        for kk, vv in sorted(best.params.items()):
            lines.append(f"    {kk} = {vv:.12g}")
        lines.append("")
        lines.append("H(z) residuals at data points")
        for zi, Ho, sg, Hm in zip(data[:, 0], data[:, 1], data[:, 2], best.H_at_data):
            lines.append(f"  z={zi:.4g}: H_obs={Ho:.6g}, sigma={sg:.6g}, H_model={Hm:.6g}, pull={(Hm - Ho) / sg:.4g}")

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
                lines.append(f"      Config: {m.scalar_config}")
                lines.append(f"      GF: {m.gf_relations}")

    lines.append("")
    lines.append("Skipped / structurally rejected models")
    for m in sorted(built_models, key=lambda mm: int(mm.lag_id)):
        if m.reject_reason:
            lines.append(f"  L#{m.lag_id}: {m.reject_reason}")

    lines.append("")
    lines.append("Files written")
    for fn in ["scan_report.txt", "model_ranking.csv", "accepted_samples_summary.csv",
               "best_solution.csv", "best_fit_Hz.png", "reject_reasons_by_model.csv",
               "accepted_samples_summary_partial.csv", "model_ranking_partial.csv", "reject_reasons_by_model_partial.csv"]:
        lines.append(f"  {OUTPUT_DIR / fn}")
    (OUTPUT_DIR / "scan_report.txt").write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines[:45]), flush=True)
    print(f"\nDone. Full report: {OUTPUT_DIR / 'scan_report.txt'}", flush=True)


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
        pot = term.get("potential_type", "")
        fixed_s = ", fixed" if fixed else ""
        sector_s = f", {sector}" if sector != "gravity" else ""
        pot_s = f", pot={pot}" if pot else ""
        lines.append(f"    [{j}] coeff={coeff}, Λ^{lp}, dim={md}{fixed_s}{sector_s}{pot_s}: {cand}")
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
        print(f"[INFO] No model ranking file found; skipping top-model summary: {ranking_path}", flush=True)
        return []
    with open(ranking_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        print(f"[INFO] Ranking file has no accepted models; skipping top-model summary: {ranking_path}", flush=True)
        return []
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
        f"chi2={_float_from_row(row, 'chi2'):.4g}, AIC={_float_from_row(row, 'AIC'):.4g}")
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
        ax.plot(sol["z"][order], sol["H_km_s_Mpc"][order], lw=1.8,
                label=f"#{i} L{lag_id}, chi2={_float_from_row(row, 'chi2'):.3g}")
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
    if not rows:
        return
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
    lines.append("Top fitted Lagrangians: forms, initial conditions, and numerical-fit parameters (v5.0)")
    lines.append("=" * 92)
    lines.append("")
    lines.append(f"Base output directory: {BASE_OUTPUT_DIR}")
    lines.append(f"Run output directory: {OUTPUT_DIR}")
    lines.append(f"Lagrangian pkl: {pkl_path if pkl_path is not None else '[not found]'}")
    lines.append(f"Ranking source: {OUTPUT_DIR / 'model_ranking.csv'}")
    lines.append("")
    lines.append("Numerical convention")
    lines.append("- Independent variable: x = ln(a) = -ln(1+z).")
    lines.append("- Dimensionless Hubble: h(x) = H(x) / H0.")
    lines.append("- Scalar 1: varphi1(x) = phi1(x) / Mp;  q1 = d varphi1 / dx.")
    lines.append("- Scalar 2: varphi2(x) = phi2(x) / Lambda;  q2 = d varphi2 / dx.")
    lines.append("- Masses: mu1 = m1/H0, mu2 = m2/Lambda.")
    lines.append("- Decay constants: fbar1 = f1/Mp, fbar2 = f2/Lambda.")
    lines.append("- EFT cutoff ratio: lambda_H = Lambda / H0.")
    lines.append("- a0 = 1, h0 = 1.  q1_0 solved from E_N(x=0)=0 (or q2_0 for phi2-only models).")
    lines.append("- Mp = 2.435e27 eV (physical reduced Planck mass).")
    lines.append("- Physical Lambda [eV] = lambda_H * H0 [eV].")
    lines.append("")

    standard_cols = {
        "lag_id", "success", "reason", "chi2", "chi2_per_point", "AIC", "BIC",
        "k_params", "max_abs_constraint", "H0_km_s_Mpc", "Omega_m0", "rho_bar",
        "mu1_m1_over_H0", "mu2_m2_over_Lambda",
        "fbar1_f1_over_Mp", "fbar2_f2_over_Lambda",
        "varphi1_0_phi1_over_Mp", "varphi2_0_phi2_over_Lambda",
        "q1_0_dvarphi1_dln_a", "q2_0_dvarphi2_dln_a",
        "eps_HM_H0_over_Mp", "lambda_H_Lambda_over_H0", "Lambda_eV",
    }

    for i, row in enumerate(top_rows, 1):
        lag_id = str(row.get("lag_id"))
        H0 = _float_from_row(row, "H0_km_s_Mpc")
        H0_eV = H0 * KM_S_MPC_TO_EV if np.isfinite(H0) else np.nan

        lines.append("")
        lines.append("=" * 92)
        lines.append(f"Rank {i}: Lagrangian #{lag_id}")
        lines.append("=" * 92)
        lines.append("")
        lines.append("Raw Lagrangian from pkl")
        lines.append(_raw_lagrangian_string(lag_map, lag_id) if lag_map else "[pkl not found]")
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
        lines.append("Initial conditions and sampled values")
        lines.append(f"  H0 [km/s/Mpc]            = {_fmt(H0)}")
        lines.append(f"  H0 [eV]                  = {_fmt(H0_eV)}")
        lines.append(f"  eps_HM = H0/Mp            = {_fmt(_float_from_row(row, 'eps_HM_H0_over_Mp'))}")
        lines.append(f"  lambda_H = Lambda/H0      = {_fmt(_float_from_row(row, 'lambda_H_Lambda_over_H0'))}")
        lines.append(f"  Lambda [eV]               = {_fmt(_float_from_row(row, 'Lambda_eV'))}")
        lines.append(f"  Omega_m0                  = {_fmt(_float_from_row(row, 'Omega_m0'))}")
        lines.append(f"  rho_bar                   = {_fmt(_float_from_row(row, 'rho_bar'))}")

        v1_0 = _float_from_row(row, "varphi1_0_phi1_over_Mp")
        q1_0 = _float_from_row(row, "q1_0_dvarphi1_dln_a")
        mu1_v = _float_from_row(row, "mu1_m1_over_H0")
        fbar1_v = _float_from_row(row, "fbar1_f1_over_Mp")
        if np.isfinite(v1_0) and v1_0 != 0:
            lines.append(f"  varphi1_0 = phi1_0/Mp     = {_fmt(v1_0)}")
        if np.isfinite(q1_0) and q1_0 != 0:
            lines.append(f"  q1_0 = dvarphi1/dx|0      = {_fmt(q1_0)}")
        if np.isfinite(mu1_v) and mu1_v != 0:
            lines.append(f"  mu1 = m1/H0               = {_fmt(mu1_v)}")
        if np.isfinite(fbar1_v) and fbar1_v != 1.0:
            lines.append(f"  fbar1 = f1/Mp              = {_fmt(fbar1_v)}")

        v2_0 = _float_from_row(row, "varphi2_0_phi2_over_Lambda")
        q2_0 = _float_from_row(row, "q2_0_dvarphi2_dln_a")
        mu2_v = _float_from_row(row, "mu2_m2_over_Lambda")
        fbar2_v = _float_from_row(row, "fbar2_f2_over_Lambda")
        if np.isfinite(v2_0) and v2_0 != 0:
            lines.append(f"  varphi2_0 = phi2_0/Lambda = {_fmt(v2_0)}")
        if np.isfinite(q2_0) and q2_0 != 0:
            lines.append(f"  q2_0 = dvarphi2/dx|0      = {_fmt(q2_0)}")
        if np.isfinite(mu2_v) and mu2_v != 0:
            lines.append(f"  mu2 = m2/Lambda           = {_fmt(mu2_v)}")
        if np.isfinite(fbar2_v) and fbar2_v != 1.0:
            lines.append(f"  fbar2 = f2/Lambda          = {_fmt(fbar2_v)}")

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
            lines.append("Free coupling values")
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