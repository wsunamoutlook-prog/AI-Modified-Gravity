#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solver v5.2 — DES-SN + DESI-DR2 BAO numerical scan
==================================================

This file is the solve stage only.  It loads Builder's cached dimensionless
models, samples their numerical initial conditions/parameters, evaluates the
DES-SN + DESI-DR2 BAO likelihood, and writes ranked results.

The symbolic parsing/build stage belongs in Builder v5.2.py.  Solver keeps only
the symbols and dataclasses needed to unpickle Builder's cache and lambdify the
cached expressions.

Two scalar fields are supported with different rescalings:

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
import json
import math
import os
import signal
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

# =============================================================================
# Runtime configuration
# =============================================================================

REPO_ROOT = Path(__file__).resolve().parents[1]

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

SN_INTEGRATION_GRID = int(os.environ.get("SN_INTEGRATION_GRID", "2000"))
SN_DIR = Path(os.environ.get(
    "SN_DIR",
    str(REPO_ROOT / "data" / "SN data"),
))
BAO_DIR = Path(os.environ.get(
    "BAO_DIR",
    str(REPO_ROOT / "data" / "BAO data"),
))

N_SAMPLES_PER_MODEL = int(os.environ.get("N_SAMPLES_PER_MODEL", "3000"))  # samples per cached model
RANDOM_SEED = int(os.environ.get("RANDOM_SEED", "0"))
PARAMETER_SAMPLES_PATH = os.environ.get("PARAMETER_SAMPLES_PATH", "").strip()
AGENT_EARLY_STOP_CHI2 = float(os.environ.get("AGENT_EARLY_STOP_CHI2", "0") or "0")
SOLVER_SETUP_TIMEOUT_SECONDS = int(os.environ.get("SOLVER_SETUP_TIMEOUT_SECONDS", "0") or "0")

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

# Optional cap for quick solve-stage smoke tests.  The historical env name is
# kept so existing scripts do not break, but this slices cached models only.
MAX_MODELS_TO_BUILD = int(os.environ.get("MAX_MODELS_TO_BUILD", "0"))


@contextmanager
def _setup_wall_timeout(seconds: int, label: str):
    if seconds <= 0:
        yield
        return

    def _raise_timeout(signum, frame):
        raise TimeoutError(f"{label} exceeded {seconds}s wall time")

    old_handler = signal.getsignal(signal.SIGALRM)
    old_timer = signal.setitimer(signal.ITIMER_REAL, float(seconds))
    signal.signal(signal.SIGALRM, _raise_timeout)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, old_timer[0], old_timer[1])
        signal.signal(signal.SIGALRM, old_handler)

# Builder-setting echoes used only to warn when the loaded cache was created
# with different symbolic-build settings.  Solver does not rebuild equations.
BUILD_SIMPLIFY_MODE = os.environ.get("BUILD_SIMPLIFY_MODE", "fast").strip().lower()
USE_LINEAR_RHS_SOLVER = os.environ.get("USE_LINEAR_RHS_SOLVER", "1").strip().lower() not in {"0", "false", "no", "n", "off"}
ALLOW_GENERAL_SYMBOLIC_SOLVE = os.environ.get("ALLOW_GENERAL_SYMBOLIC_SOLVE", "1").strip().lower() not in {"0", "false", "no", "n", "off"}
RHS_SIMPLIFY_MODE = os.environ.get("RHS_SIMPLIFY_MODE", "cancel").strip().lower()

N_GRID = int(os.environ.get("N_GRID", "150"))
RTOL = float(os.environ.get("RTOL", "1e-6"))
ATOL = float(os.environ.get("ATOL", "1e-8"))
MAX_ABS_CONSTRAINT = float(os.environ.get("MAX_ABS_CONSTRAINT", "1e-4"))

PRIORS = {
    "H0_km_s_Mpc": (
        float(os.environ.get("H0_MIN", "60.0")),
        float(os.environ.get("H0_MAX", "75.0")),
    ),
    "Omega_m0": (
        float(os.environ.get("OMEGA_M0_MIN", "0.15")),
        float(os.environ.get("OMEGA_M0_MAX", "0.45")),
    ),
    "varphi1_0": (
        float(os.environ.get("VARPHI1_0_MIN", "-5")),
        float(os.environ.get("VARPHI1_0_MAX", "5")),
    ),
    "varphi2_0": (
        float(os.environ.get("VARPHI2_0_MIN", "-5")),
        float(os.environ.get("VARPHI2_0_MAX", "5")),
    ),
    "log10_mu1": (
        float(os.environ.get("LOG10_MU1_MIN", "-3.0")),
        float(os.environ.get("LOG10_MU1_MAX", "1.0")),
    ),
    "log10_mu2": (
        float(os.environ.get("LOG10_MU2_MIN", "-3.0")),
        float(os.environ.get("LOG10_MU2_MAX", "1.0")),
    ),
    "log10_fbar1": (
        float(os.environ.get("LOG10_FBAR1_MIN", "-2.0")),
        float(os.environ.get("LOG10_FBAR1_MAX", "2.0")),
    ),
    "log10_fbar2": (
        float(os.environ.get("LOG10_FBAR2_MIN", "-2.0")),
        float(os.environ.get("LOG10_FBAR2_MAX", "2.0")),
    ),
    "log10_lambda_H": (
        float(os.environ.get("LOG10_LAMBDA_H_MIN", "2.0")),
        float(os.environ.get("LOG10_LAMBDA_H_MAX", "5.0")),
    ),
    "log10_abs_c": (
        float(os.environ.get("LOG10_ABS_C_MIN", "-10.0")),
        float(os.environ.get("LOG10_ABS_C_MAX", "10.0")),
    ),
}

FIX_EH_COEFFICIENT = os.environ.get("FIX_EH_COEFFICIENT", "1").strip().lower() not in {"0", "false", "no"}
EH_COEFFICIENT_VALUE = float(os.environ.get("EH_COEFFICIENT_VALUE", "0.5"))
ENFORCE_EFT_CUTOFF = os.environ.get("ENFORCE_EFT_CUTOFF", "1").strip().lower() not in {"0", "false", "no"}
EFT_MAX_H_OVER_LAMBDA = float(os.environ.get("EFT_MAX_H_OVER_LAMBDA", "0.1"))

MAX_ABS_Q0 = float(os.environ.get("MAX_ABS_Q0", "20.0"))
PREFERRED_ABS_Q0 = float(os.environ.get("PREFERRED_ABS_Q0", "2.0"))
MAX_ABS_VARPHI_TRAJ = float(os.environ.get("MAX_ABS_VARPHI_TRAJ", "200.0"))
MAX_ABS_Q_TRAJ = float(os.environ.get("MAX_ABS_Q_TRAJ", "80.0"))
MAX_H_KM_S_MPC = float(os.environ.get("MAX_H_KM_S_MPC", "1500.0"))
MIN_H = float(os.environ.get("MIN_H", "1e-8"))
SOLVER_MAKE_PLOTS = os.environ.get("SOLVER_MAKE_PLOTS", "1").strip().lower() not in {"0", "false", "no", "n", "off"}
DENOM_EPS = 1e-12

MODE = os.environ.get("SOLVER_MODE", "eft").lower().strip()
if MODE == "physical":
    MODE = "eft"
if MODE == "effective":
    MODE = "phenomenological"

M_P_REDUCED_EV = 2.435e27
KM_S_MPC_TO_EV = 2.133119e-35
# =============================================================================
# DES-SN + DESI-DR2 likelihood
# =============================================================================

from .likelihood import (
    chi2_des_sn_from_grid,
    chi2_desi_bao_from_grid,
    load_current_likelihood_data as _load_current_likelihood_data,
)


def load_current_likelihood_data():
    return _load_current_likelihood_data(SN_DIR, BAO_DIR)


# =============================================================================
# Cached symbolic variables
# =============================================================================

# Solver only needs the dimensionless symbols that appear in Builder's cached
# constraint/RHS expressions.  Physical FLRW parsing symbols stay in Builder.
x_sym, h_sym = sp.symbols("x h", real=True)
varphi1_sym, q1_sym = sp.symbols("varphi1 q1", real=True)
varphi2_sym, q2_sym = sp.symbols("varphi2 q2", real=True)
mu1_sym = sp.Symbol("mu1", positive=True)
mu2_sym = sp.Symbol("mu2", positive=True)
fbar1_sym = sp.Symbol("fbar1", positive=True)
fbar2_sym = sp.Symbol("fbar2", positive=True)
rho_bar_sym = sp.Symbol("rho_bar", positive=True)
eps_HM_sym = sp.Symbol("eps_HM", positive=True)
lambda_H_sym = sp.Symbol("lambda_H", positive=True)


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
    chi2_hz: float = math.inf
    chi2_sn: float = 0.0
    chi2_bao: float = 0.0
    sn_offset_hat: Optional[float] = None
    bao_alpha_hat: Optional[float] = None
    n_sn: int = 0
    n_bao: int = 0
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
# Lambdify and numerical evaluation
# =============================================================================

def get_param_symbols(model: Model) -> List[sp.Symbol]:
    syms = list(model.free_symbols)
    if FIX_EH_COEFFICIENT and model.eh_symbol is not None:
        syms = [s for s in syms if s != model.eh_symbol]
    syms = sorted(set(syms), key=lambda s: s.name)
    return syms


AgentParameterSamples = Union[List[Dict[str, float]], Dict[str, List[Dict[str, float]]]]


def _normalize_parameter_sample_list(payload: Any, *, label: str) -> List[Dict[str, float]]:
    if not isinstance(payload, list):
        raise TypeError(f"{label} must be a JSON list of sample objects")
    samples: List[Dict[str, float]] = []
    for idx, item in enumerate(payload, 1):
        if not isinstance(item, dict):
            raise TypeError(f"{label} sample #{idx} must be an object, got {type(item).__name__}")
        sample: Dict[str, float] = {}
        for key, value in item.items():
            if value is None:
                continue
            sample[str(key)] = float(value)
        samples.append(sample)
    if not samples:
        raise ValueError(f"{label} contains no samples")
    return samples


def load_parameter_samples(path: str = PARAMETER_SAMPLES_PATH) -> Optional[AgentParameterSamples]:
    """Load agent-proposed numerical samples.

    The default Solver behavior is random sampling. If PARAMETER_SAMPLES_PATH is
    provided, each JSON object is treated as one complete agent-proposed sample.
    Missing required keys are reported by evaluate_sample instead of falling
    back to random values.
    """

    if not path:
        return None
    p = Path(path).expanduser().resolve()
    with p.open(encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, dict) and isinstance(payload.get("samples_by_lag_id"), dict):
        by_lag: Dict[str, List[Dict[str, float]]] = {}
        for lag_id, samples in payload["samples_by_lag_id"].items():
            by_lag[str(lag_id)] = _normalize_parameter_sample_list(
                samples,
                label=f"PARAMETER_SAMPLES_PATH samples_by_lag_id[{lag_id!r}]",
            )
        if not by_lag:
            raise ValueError(f"PARAMETER_SAMPLES_PATH contains empty samples_by_lag_id: {p}")
        return by_lag
    if isinstance(payload, dict):
        payload = payload.get("samples")
    if not isinstance(payload, list):
        raise TypeError(
            "PARAMETER_SAMPLES_PATH must contain a JSON list, an object with 'samples', "
            f"or an object with 'samples_by_lag_id': {p}"
        )
    return _normalize_parameter_sample_list(payload, label="PARAMETER_SAMPLES_PATH")


def _require_agent_value(sample: Dict[str, float], names: List[str]) -> float:
    for name in names:
        if name in sample:
            return float(sample[name])
    raise KeyError(" or ".join(names))


_GREEK_PARAMETER_ALIASES = {
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "zeta",
    "eta",
    "theta",
    "iota",
    "kappa",
    "lambda",
    "mu",
    "nu",
    "xi",
    "rho",
    "sigma",
    "tau",
}


def _agent_parameter_name_aliases(sym: sp.Symbol) -> List[str]:
    bases = [str(sym), sym.name]
    out: List[str] = []
    for base in bases:
        if not base:
            continue
        bare = base.replace("\\", "")
        variants = [base, bare]
        if bare in _GREEK_PARAMETER_ALIASES:
            variants.append(f"\\{bare}")
        if "_{" in bare and bare.endswith("}"):
            variants.append(bare.replace("_{", "_").replace("}", ""))
        for variant in variants:
            if variant and variant not in out:
                out.append(variant)
    with_prefixes: List[str] = []
    for name in out:
        for candidate in (name, f"coef:{name}", f"coefficient:{name}"):
            if candidate not in with_prefixes:
                with_prefixes.append(candidate)
    return with_prefixes


def _optional_agent_value(sample: Dict[str, float], names: List[str]) -> Optional[float]:
    for name in names:
        if name in sample:
            return float(sample[name])
    return None


def _agent_or_random_linear(
    sample: Optional[Dict[str, float]],
    names: List[str],
    rng: np.random.Generator,
    prior_name: str,
) -> float:
    if sample is not None:
        return _require_agent_value(sample, names)
    return float(rng.uniform(*PRIORS[prior_name]))


def _agent_or_random_log10(
    sample: Optional[Dict[str, float]],
    value_names: List[str],
    log_names: List[str],
    rng: np.random.Generator,
    prior_name: str,
) -> float:
    if sample is not None:
        for name in value_names:
            if name in sample:
                return float(sample[name])
        for name in log_names:
            if name in sample:
                return 10.0 ** float(sample[name])
        raise KeyError(" or ".join(value_names + log_names))
    return 10.0 ** float(rng.uniform(*PRIORS[prior_name]))


def sample_parameter_values(
    model: Model,
    rng: np.random.Generator,
    mode: str,
    agent_sample: Optional[Dict[str, float]] = None,
) -> Dict[sp.Symbol, float]:
    vals: Dict[sp.Symbol, float] = {}
    for sym in get_param_symbols(model):
        if agent_sample is not None:
            vals[sym] = _require_agent_value(
                agent_sample,
                _agent_parameter_name_aliases(sym),
            )
        else:
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


def find_q0_root(
    C_func,
    base_args_without_q,
    q_range=(-MAX_ABS_Q0, MAX_ABS_Q0),
    n_scan=401,
    q_hint: Optional[float] = None,
    hint_window: Optional[float] = None,
) -> Optional[float]:
    q_min, q_max = q_range
    roots = []

    def scan_interval(a: float, b: float, scan_count: int) -> None:
        if not (np.isfinite(a) and np.isfinite(b)) or b <= a:
            return
        grid = np.linspace(a, b, max(3, int(scan_count)))
        vals = []
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
        vals_arr = np.array(vals)
        for i in range(len(grid) - 1):
            f1, f2 = vals_arr[i], vals_arr[i + 1]
            if not (np.isfinite(f1) and np.isfinite(f2)):
                continue
            if f1 == 0:
                roots.append(float(grid[i]))
            if f1 * f2 < 0:
                try:
                    root = brentq(
                        lambda qq: robust_float(C_func(*base_args_without_q(float(qq)))),
                        grid[i],
                        grid[i + 1],
                        maxiter=100,
                    )
                    if np.isfinite(root):
                        roots.append(float(root))
                except Exception:
                    pass

    finite_hint = q_hint is not None and np.isfinite(q_hint)
    if finite_hint:
        center = float(np.clip(float(q_hint), q_min, q_max))
        window = float(hint_window if hint_window is not None else PREFERRED_ABS_Q0)
        local_min = max(q_min, center - abs(window))
        local_max = min(q_max, center + abs(window))
        scan_interval(local_min, local_max, n_scan)
        if roots:
            roots_sorted = []
            for r in sorted(roots, key=lambda rr: abs(rr - center)):
                if not any(abs(r-r0) < 1e-6 for r0 in roots_sorted):
                    roots_sorted.append(r)
            return float(roots_sorted[0])

    scan_interval(q_min, q_max, n_scan)
    if not roots:
        return None
    roots_sorted = []
    sort_key = (lambda rr: abs(rr - float(q_hint))) if finite_hint else (lambda rr: abs(rr))
    for r in sorted(roots, key=sort_key):
        if not any(abs(r-r0) < 1e-6 for r0 in roots_sorted):
            roots_sorted.append(r)
    if finite_hint:
        return float(roots_sorted[0])
    preferred = [r for r in roots_sorted if abs(r) <= PREFERRED_ABS_Q0]
    return float((preferred or roots_sorted)[0])


def evaluate_sample(model: Model, rng: np.random.Generator, mode: str,
                    compiled: Optional[Tuple[Any, Any, Any, Any, List[sp.Symbol]]] = None,
                    sn_data: Optional[dict] = None,
                    bao_data: Optional[dict] = None,
                    agent_sample: Optional[Dict[str, float]] = None,
                    agent_sample_index: Optional[int] = None) -> SampleResult:
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

    try:
        H0_km = _agent_or_random_linear(agent_sample, ["H0_km_s_Mpc", "H0"], rng, "H0_km_s_Mpc")
        Omega_m0 = _agent_or_random_linear(agent_sample, ["Omega_m0", "omega_m0"], rng, "Omega_m0")
        rho_bar = 3.0 * Omega_m0
        mu1 = (
            _agent_or_random_log10(
                agent_sample,
                ["mu1_m1_over_H0", "mu1"],
                ["log10_mu1"],
                rng,
                "log10_mu1",
            )
            if model.has_phi1 else 0.0
        )
        mu2 = (
            _agent_or_random_log10(
                agent_sample,
                ["mu2_m2_over_Lambda", "mu2"],
                ["log10_mu2"],
                rng,
                "log10_mu2",
            )
            if model.has_phi2 else 0.0
        )
        fbar1 = (
            _agent_or_random_log10(
                agent_sample,
                ["fbar1_f1_over_Mp", "fbar1"],
                ["log10_fbar1"],
                rng,
                "log10_fbar1",
            )
            if model.has_phi1 else 1.0
        )
        fbar2 = (
            _agent_or_random_log10(
                agent_sample,
                ["fbar2_f2_over_Lambda", "fbar2"],
                ["log10_fbar2"],
                rng,
                "log10_fbar2",
            )
            if model.has_phi2 else 1.0
        )
        varphi1_0 = (
            _agent_or_random_linear(
                agent_sample,
                ["varphi1_0_phi1_over_Mp", "varphi1_0"],
                rng,
                "varphi1_0",
            )
            if model.has_phi1 else 0.0
        )
        varphi2_0 = (
            _agent_or_random_linear(
                agent_sample,
                ["varphi2_0_phi2_over_Lambda", "varphi2_0"],
                rng,
                "varphi2_0",
            )
            if model.has_phi2 else 0.0
        )
        lambda_H = _agent_or_random_log10(
            agent_sample,
            ["lambda_H_Lambda_over_H0", "lambda_H"],
            ["log10_lambda_H"],
            rng,
            "log10_lambda_H",
        )
        pvals = sample_parameter_values(model, rng, mode, agent_sample=agent_sample)
    except KeyError as exc:
        return SampleResult(model.lag_id, False, f"agent parameter sample missing: {exc}")
    eps_HM = (H0_km * KM_S_MPC_TO_EV) / M_P_REDUCED_EV
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
            if model.has_phi2:
                try:
                    q2_0 = (
                        _require_agent_value(agent_sample, ["q2_0_dvarphi2_dln_a", "q2_0"])
                        if agent_sample is not None
                        else float(rng.uniform(-PREFERRED_ABS_Q0, PREFERRED_ABS_Q0))
                    )
                except KeyError as exc:
                    return SampleResult(model.lag_id, False, f"agent parameter sample missing: {exc}")
            else:
                q2_0 = 0.0
            def base_args(qtrial):
                return make_args(0.0, 1.0, varphi1_0, qtrial, varphi2_0, q2_0)
            q1_0 = find_q0_root(C_func, base_args)
            if q1_0 is None:
                return SampleResult(model.lag_id, False, "no acceptable real q1_0 root from E_N(x=0)=0")
        else:
            # phi2_only: solve for q2_0
            q1_0 = 0.0
            q2_hint = None
            if agent_sample is not None:
                q2_hint = _optional_agent_value(agent_sample, ["q2_0_dvarphi2_dln_a", "q2_0"])
            def base_args(qtrial):
                return make_args(0.0, 1.0, 0.0, 0.0, varphi2_0, qtrial)
            q2_0 = find_q0_root(C_func, base_args, q_hint=q2_hint)
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
    if sn_data is None or bao_data is None:
        return SampleResult(model.lag_id, False, "DES SN and DESI BAO data are required")
    z_max_required = max(float(np.max(sn_data["zHD"])), float(np.max(bao_data["z"])))
    xmin = -math.log1p(z_max_required)
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

    # ── DES-SN + DESI-DR2 BAO likelihood ──
    try:
        z_like_grid = np.linspace(0.0, z_max_required, SN_INTEGRATION_GRID)
        x_like_grid = -np.log1p(z_like_grid)
        y_like_grid = sol.sol(x_like_grid)
        h_like_grid = np.asarray(y_like_grid[idx_h], dtype=float)
    except Exception as exc:
        return SampleResult(model.lag_id, False, f"likelihood dense output failed: {type(exc).__name__}")
    if z_like_grid[-1] < float(np.max(sn_data["zHD"])) or z_like_grid[-1] < float(np.max(bao_data["z"])):
        return SampleResult(model.lag_id, False, "likelihood integration grid does not cover data")
    if not np.all(np.isfinite(h_like_grid)):
        return SampleResult(model.lag_id, False, "likelihood h_grid not finite")
    if np.any(h_like_grid <= MIN_H):
        return SampleResult(model.lag_id, False, "likelihood h_grid <= MIN_H")

    try:
        chi2_sn, sn_offset_hat = chi2_des_sn_from_grid(
            sn_data,
            z_grid=z_like_grid,
            h_grid=h_like_grid,
            H0_km_s_Mpc=H0_km,
        )
        chi2_bao, bao_alpha_hat = chi2_desi_bao_from_grid(
            bao_data,
            z_grid=z_like_grid,
            h_grid=h_like_grid,
        )
    except Exception as exc:
        return SampleResult(model.lag_id, False, f"DES-SN/DESI-BAO chi2 failed: {type(exc).__name__}: {exc}")
    chi2_hz = 0.0
    chi2 = chi2_sn + chi2_bao
    n = len(sn_data["mu"]) + len(bao_data["value"])

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
    k += 2  # DES-SN M_SN and DESI BAO alpha_BAO analytically profiled
    aic = chi2 + 2.0 * k
    bic = chi2 + k * math.log(n)

    params = {
        "agent_parameter_sample_index": agent_sample_index,
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
        "sn_offset_hat": sn_offset_hat,
        "bao_alpha_hat": bao_alpha_hat,
    }
    for s, v in pvals.items():
        params[str(s)] = float(v)

    return SampleResult(
        lag_id=model.lag_id, success=True, reason="ok", chi2=chi2,
        chi2_hz=chi2_hz, chi2_sn=chi2_sn, chi2_bao=chi2_bao,
        sn_offset_hat=sn_offset_hat, bao_alpha_hat=bao_alpha_hat,
        n_sn=len(sn_data["mu"]), n_bao=len(bao_data["value"]),
        chi2_per_point=chi2 / n, aic=aic, bic=bic, k_params=k,
        params=params, max_abs_constraint=maxC,
        x_grid=x_eval, z_grid=z_grid, h_grid=h_grid, H_grid=H_grid_phys,
        varphi1_grid=varphi1_grid, q1_grid=q1_grid,
        varphi2_grid=varphi2_grid, q2_grid=q2_grid,
        constraint_grid=C_vals, H_at_data=None,
    )


# =============================================================================
# LCDM reference
# =============================================================================

def lcdm_fit_reference(sn_data: dict, bao_data: dict) -> Dict[str, float]:
    best = {"chi2": math.inf}
    zmax_required = max(float(np.max(sn_data["zHD"])), float(np.max(bao_data["z"])))
    z_grid = np.linspace(0.0, zmax_required * 1.001, 3000)
    Om_grid = np.linspace(0.05, 0.6, 551)
    n = len(sn_data["mu"]) + len(bao_data["value"])
    H0 = 70.0
    for Om in Om_grid:
        Om_f = float(Om)
        h_grid = np.sqrt(Om_f * (1.0 + z_grid) ** 3 + (1.0 - Om_f))
        chi2_bao, alpha_hat = chi2_desi_bao_from_grid(bao_data, z_grid, h_grid)
        # DES SN chi2 after additive-offset profiling is independent of the pure H0 shift.
        chi2_sn, M_hat = chi2_des_sn_from_grid(sn_data, z_grid, h_grid, H0)
        c2 = chi2_sn + chi2_bao
        if c2 < best["chi2"]:
            best = {
                "H0": H0,
                "Omega_m0": Om_f,
                "chi2": c2,
                "chi2_hz": 0.0,
                "chi2_sn": chi2_sn,
                "chi2_bao": chi2_bao,
                "sn_offset_hat": M_hat,
                "bao_alpha_hat": alpha_hat,
                "chi2_per_point": c2 / n,
            }
    k = 4  # H0, Omega_m0, DES-SN M_SN, DESI BAO alpha_BAO
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
        "chi2_hz": r.chi2_hz, "chi2_sn": r.chi2_sn, "chi2_bao": r.chi2_bao,
        "sn_offset_hat": r.sn_offset_hat, "bao_alpha_hat": r.bao_alpha_hat,
        "N_SN": r.n_sn, "N_BAO": r.n_bao,
        "AIC": r.aic, "BIC": r.bic, "k_params": r.k_params,
        "max_abs_constraint": r.max_abs_constraint,
    }
    if r.params:
        row.update(r.params)
    return row


RESULT_SUMMARY_COLUMNS = [
    "lag_id", "success", "reason", "chi2", "chi2_per_point",
    "chi2_hz", "chi2_sn", "chi2_bao", "sn_offset_hat", "bao_alpha_hat",
    "N_SN", "N_BAO", "AIC", "BIC", "k_params", "max_abs_constraint",
]


def _attach_agent_sample_params(
    res: SampleResult,
    agent_sample: Optional[Dict[str, float]],
    agent_sample_index: Optional[int],
) -> SampleResult:
    if agent_sample is None:
        return res
    params = dict(res.params or {})
    params.setdefault("agent_parameter_sample_index", agent_sample_index)
    for key, value in agent_sample.items():
        params.setdefault(str(key), float(value))
    res.params = params
    return res


def write_csv(path: Path, rows: List[Dict[str, Any]]):
    if not rows:
        if path.name.startswith("accepted_samples_summary") or path.name.startswith("model_ranking"):
            with path.open("w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=RESULT_SUMMARY_COLUMNS).writeheader()
            return
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


def plot_best(best: Optional[SampleResult], path: Path):
    if best is None or plt is None:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    order = np.argsort(best.z_grid)
    ax.plot(best.z_grid[order], best.h_grid[order], lw=2, label=f"Best L#{best.lag_id}")
    ax.set_xlabel("z")
    ax.set_ylabel("h(z)=H/H0")
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


def _scan_single_model_worker(args: Tuple[Model, str, int, int, int, dict, dict, Optional[List[Dict[str, float]]]]) -> Dict[str, Any]:
    """Worker entry point: lambdify once, then evaluate many samples for one model."""
    model, mode, n_samples, seed, worker_sample_progress, sn_data, bao_data, agent_parameter_samples = args
    t_model = time.time()
    rejects = Counter()
    accepted: List[SampleResult] = []
    evaluated: List[SampleResult] = []
    best: Optional[SampleResult] = None
    samples_to_evaluate = agent_parameter_samples if agent_parameter_samples is not None else [None] * n_samples
    n_samples_actual = len(samples_to_evaluate)

    if model.reject_reason:
        rejects[model.reject_reason] += n_samples_actual
        return {
            "lag_id": model.lag_id,
            "accepted": accepted,
            "evaluated": evaluated,
            "best": best,
            "rejects": dict(rejects),
            "elapsed": time.time() - t_model,
            "samples": n_samples_actual,
            "status": "skipped",
        }

    try:
        with _setup_wall_timeout(SOLVER_SETUP_TIMEOUT_SECONDS, "Solver setup/lambdify"):
            compiled = lambdify_model(model, mode)
    except TimeoutError as exc:
        rejects[f"solver setup timeout before sampling: {exc}"] += n_samples_actual
        return {
            "lag_id": model.lag_id,
            "accepted": accepted,
            "evaluated": evaluated,
            "best": best,
            "rejects": dict(rejects),
            "elapsed": time.time() - t_model,
            "samples": n_samples_actual,
            "status": "setup_timeout",
        }
    except Exception as exc:
        rejects[f"lambdify failed: {type(exc).__name__}: {exc}"] += n_samples_actual
        return {
            "lag_id": model.lag_id,
            "accepted": accepted,
            "evaluated": evaluated,
            "best": best,
            "rejects": dict(rejects),
            "elapsed": time.time() - t_model,
            "samples": n_samples_actual,
            "status": "lambdify_failed",
        }

    rng = np.random.default_rng(seed)
    for i, agent_sample in enumerate(samples_to_evaluate):
        res = evaluate_sample(
            model,
            rng,
            mode,
            compiled=compiled,
            sn_data=sn_data,
            bao_data=bao_data,
            agent_sample=agent_sample,
            agent_sample_index=i + 1 if agent_sample is not None else None,
        )
        res = _attach_agent_sample_params(
            res,
            agent_sample,
            i + 1 if agent_sample is not None else None,
        )
        evaluated.append(res)
        if res.success:
            accepted.append(res)
            if best is None or (res.chi2, res.aic) < (best.chi2, best.aic):
                best = res
        else:
            rejects[res.reason] += 1

        if AGENT_EARLY_STOP_CHI2 > 0 and res.success and res.chi2 <= AGENT_EARLY_STOP_CHI2:
            print(
                f"[worker] L#{model.lag_id}: early stop at sample {i+1}/{n_samples_actual}, "
                f"chi2={res.chi2:.6g} <= {AGENT_EARLY_STOP_CHI2:.6g}",
                flush=True,
            )
            break

        if worker_sample_progress > 0 and (i + 1) % worker_sample_progress == 0:
            print(
                f"[worker] L#{model.lag_id}: {i+1}/{n_samples_actual} samples, "
                f"accepted={len(accepted)}, elapsed={_format_seconds(time.time() - t_model)}",
                flush=True,
            )

    return {
        "lag_id": model.lag_id,
        "accepted": accepted,
        "evaluated": evaluated,
        "best": best,
        "rejects": dict(rejects),
        "elapsed": time.time() - t_model,
        "samples": n_samples_actual,
        "status": "done",
    }


def _write_partial_progress(output_dir: Path,
                            all_results: List[SampleResult],
                            all_evaluated: List[SampleResult],
                            best_by_model: Dict[str, SampleResult],
                            reject_counts_by_model: Dict[str, Counter],
                            label: str = "partial"):
    """Write lightweight CSV snapshots during a long scan."""
    try:
        accepted = sorted(all_results, key=lambda r: (r.chi2, r.aic))
        model_best_list = sorted(best_by_model.values(), key=lambda r: (r.chi2, r.aic))
        write_csv(output_dir / f"accepted_samples_summary_{label}.csv", [result_row(r) for r in accepted])
        write_csv(output_dir / f"all_samples_summary_{label}.csv", [result_row(r) for r in all_evaluated])
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
                         all_evaluated: List[SampleResult],
                         best_by_model: Dict[str, SampleResult],
                         reject_counts_by_model: Dict[str, Counter]):
    lag_id = str(out["lag_id"])
    for res in out.get("accepted", []):
        all_results.append(res)
    for res in out.get("evaluated", []):
        all_evaluated.append(res)
    best = out.get("best")
    if best is not None:
        current = best_by_model.get(lag_id)
        if current is None or (best.chi2, best.aic) < (current.chi2, current.aic):
            best_by_model[lag_id] = best
    for reason, n in out.get("rejects", {}).items():
        reject_counts_by_model[lag_id][reason] += int(n)
