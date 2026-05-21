#!/usr/bin/env python3
"""
cosmo_solver.py  (v1.0)
=======================
Dimensionless numerical cosmology solver for ghost-free modified-
gravity EOM from EOM_v1_7.py.  Fits BAO / H(z) data by integrating
the background in e-fold variable  x = ln a.

Nondimensionalization
---------------------
    H       = H0_phys · h(x)                h(0) = 1
    φ       = M_p · φ̃(x)                    φ̃ dimensionless
    q       = dφ̃/dx
    m       = H0_phys · μ
    ρ_{m,0} = M_p² H0² ρ̄                    ρ̄ = 3 Ω_{m0}
    ε       = H0_phys / M_p  ≈ 6.1e-61

    S_EH  = ∫ √-g (M_p²/2) R   →  standard GR has  α_EH = 1/2

Derivative substitutions (N = 1 gauge):
    a       → exp(x)
    ȧ       → H0 h exp(x)
    ä       → H0² exp(x) (h² + h h_x)

    φ       → M_p φ̃
    φ̇       → M_p H0 h q
    φ̈       → M_p H0² h (h_x q + h q_x)

Then:  H0 → ε M_p,  M_p → 1.

Two modes
---------
    "eft"       — keep ε in equations (Wilson coefficients O(1))
    "effective" — set ε = 1 (effective late-time couplings)

Usage
-----
    # From EOM_v1_7 output
    result = process_lagrangian(L_data, idx, ...)
    eom = result['symbolic_gauged_matter']  # includes dust in E_N

    # Build + solve
    from cosmo_solver import solve_dimensionless_bao_ivp
    fits = solve_dimensionless_bao_ivp(eom, mode="effective")
"""

import sympy as sp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import time as _time
import signal
import sys
import os
from typing import Dict, Tuple, Optional, Any, List

# ════════════════════════════════════════════════════════════════
#  Physical constants
# ════════════════════════════════════════════════════════════════

MPRED_EV       = 2.435e27          # reduced Planck mass [eV]
KM_S_MPC_TO_EV = 2.133119e-35     # 1 km/s/Mpc → eV
C_KM_S         = 299792.458       # speed of light [km/s]

# ════════════════════════════════════════════════════════════════
#  Symbols — must match EOM_v1_7.py
# ════════════════════════════════════════════════════════════════

t_sym    = sp.Symbol('t', real=True)
_a_cls   = sp.Function('a', positive=True)
_phi_cls = sp.Function('phi')

M_p_sym    = sp.Symbol('M_p', positive=True)
m_sym      = sp.Symbol('m',   positive=True)
rho_m0_sym = sp.Symbol('rho_{m,0}', positive=True)

# ── Dimensionless symbols ─────────────────────────────────────
x_s      = sp.Symbol('x')
h_s      = sp.Symbol('h',   positive=True)
h_x_s    = sp.Symbol('h_x')          # dh/dx
vp_s     = sp.Symbol('varphi')        # φ / M_p
q_s      = sp.Symbol('q')             # dφ̃/dx
q_x_s    = sp.Symbol('q_x')           # d²φ̃/dx²
mu_s     = sp.Symbol('mu',  positive=True)   # m / H0
rhobar_s = sp.Symbol('rho_bar', positive=True)  # ρ_m0 / (M_p² H0²)
eps_s    = sp.Symbol('eps', positive=True)       # H0 / M_p

def _simp(expr):
    try:    return sp.powsimp(sp.cancel(expr))
    except: return sp.cancel(expr)

# ════════════════════════════════════════════════════════════════
#  Default H(z) data  (OHD compilation — cosmic chronometers)
# ════════════════════════════════════════════════════════════════

DEFAULT_HZ = {
    'z': np.array([
        0.07,  0.09,  0.17,  0.179, 0.199, 0.27,  0.352, 0.3802,
        0.4004,0.4247,0.4497,0.4783,0.593, 0.68,  0.781, 0.875,
        0.9,   1.037, 1.3,   1.43,  1.53,  1.75,  1.965]),
    'H': np.array([
        69.0,  69.0,  83.0,  75.0,  75.0,  77.0,  83.0,  83.0,
        77.0,  87.1,  92.8,  80.9, 104.0,  92.0, 105.0, 125.0,
       117.0, 154.0, 168.0, 177.0, 140.0, 202.0, 186.5]),
    'sigma': np.array([
        19.6,  12.0,   8.0,   4.0,   5.0,  14.0,  14.0,  13.5,
        10.2,  11.2,  12.9,   9.0,  13.0,   8.0,  12.0,  17.0,
        23.0,  20.0,  17.0,  18.0,  14.0,  40.0,  50.4]),
}


# ════════════════════════════════════════════════════════════════
#  SECTION 1 :  Nondimensionalization
# ════════════════════════════════════════════════════════════════

def nondimensionalize_eom(eom_gauged, t_s=t_sym, mode="effective",
                          verbose=True):
    """
    Convert dimensional N=1 EOM to dimensionless e-fold form.

    Pipeline (applied term by term to each E_N, E_a, E_φ):
      1. ä → H0² exp(x)(h² + h h_x),  ȧ → H0 h exp(x),  a → exp(x)
         φ̈ → M_p H0² h(h_x q + h q_x),  φ̇ → M_p H0 h q,  φ → M_p φ̃
      2. m → H0 μ,   ρ_{m,0} → M_p² H0² ρ̄
      3. H0 → ε M_p
      4. M_p → 1           (all terms now ε^k × dimensionless)
      5. If mode="effective": ε → 1

    Returns  dict  {'N': expr, 'a': expr, ['phi': expr]}
    """
    _H0 = sp.Symbol('_H0_', positive=True)    # internal placeholder
    a_t   = _a_cls(t_s)
    phi_t = _phi_cls(t_s)
    has_phi = 'phi' in eom_gauged

    if verbose:
        print(f"\n  Nondimensionalizing  (mode={mode}, has_φ={has_phi})")

    dimless = {}
    for name, eq in eom_gauged.items():
        e = eq

        # ── Step 1: dynamical substitutions (highest derivative first) ──
        e = e.subs(sp.Derivative(a_t, (t_s, 2)),
                   _H0**2 * sp.exp(x_s) * (h_s**2 + h_s * h_x_s))
        e = e.subs(sp.Derivative(a_t, t_s),
                   _H0 * h_s * sp.exp(x_s))
        e = e.subs(a_t, sp.exp(x_s))

        if has_phi:
            e = e.subs(sp.Derivative(phi_t, (t_s, 2)),
                       M_p_sym * _H0**2 * h_s
                       * (h_x_s * q_s + h_s * q_x_s))
            e = e.subs(sp.Derivative(phi_t, t_s),
                       M_p_sym * _H0 * h_s * q_s)
            e = e.subs(phi_t, M_p_sym * vp_s)

        # ── Step 2: parameter substitutions ──
        e = e.subs(m_sym, _H0 * mu_s)
        e = e.subs(rho_m0_sym, M_p_sym**2 * _H0**2 * rhobar_s)

        # ── Step 3: H0 → ε M_p ──
        e = e.subs(_H0, eps_s * M_p_sym)

        # ── Step 4: M_p → 1 ──
        e = e.subs(M_p_sym, 1)

        # ── Step 5: effective mode ──
        if mode == "effective":
            e = e.subs(eps_s, 1)

        e = sp.expand(e)
        dimless[name] = e

        if verbose:
            s = str(e)
            if len(s) > 200:
                s = s[:200] + ' ...'
            print(f"    E_{name} = {s}")

    return dimless


# ════════════════════════════════════════════════════════════════
#  SECTION 2 :  RHS extraction (solve E_a [, E_φ] for h_x [, q_x])
# ════════════════════════════════════════════════════════════════

def extract_dimless_rhs(dimless_eom, has_phi=False, verbose=True):
    """
    Extract the ODE right-hand side from the dimensionless EOM.

    The EOM is (generically) linear in h_x and q_x because ä and φ̈
    are linear in them.  We solve the algebraic system for {h_x [, q_x]}.

    DAE index reduction:  if E_a is purely algebraic (no h_x, q_x —
    happens when ghost-free constraints kill the gravity coupling),
    differentiate E_a w.r.t. x to obtain a second ODE.

    Returns dict:
        { h_x_s: expr [, q_x_s: expr] }
        plus key 'algebraic_constraints': list of extra algebraic eqs
    """
    derivs = {h_x_s, q_x_s}

    if has_phi and 'phi' in dimless_eom:
        unknowns = [h_x_s, q_x_s]
        E_a   = dimless_eom['a']
        E_phi = dimless_eom['phi']

        # Check which equations contain h_x / q_x
        Ea_has_derivs  = bool(E_a.free_symbols & derivs)
        Ephi_has_derivs = bool(E_phi.free_symbols & derivs)

        alg_constraints = []

        if Ea_has_derivs and Ephi_has_derivs:
            # Normal case: both equations contain derivatives
            eqs = [E_a, E_phi]
        elif not Ea_has_derivs:
            # ── DAE index reduction ──────────────────────────
            # E_a is algebraic:  E_a(x, h, φ̃, q) = 0  for all x.
            # Differentiate w.r.t. x using chain rule:
            #   dE_a/dx = ∂E_a/∂x + (∂E_a/∂h)·h_x
            #           + (∂E_a/∂φ̃)·(dφ̃/dx) + (∂E_a/∂q)·q_x
            # with dφ̃/dx = q.
            if verbose:
                print(f"\n  ⚠  E_a has no derivatives — applying DAE index "
                      f"reduction (differentiating constraint)")
            dEa_dx = (_simp(sp.diff(E_a, x_s))
                      + _simp(sp.diff(E_a, h_s))  * h_x_s
                      + _simp(sp.diff(E_a, vp_s)) * q_s
                      + _simp(sp.diff(E_a, q_s))  * q_x_s)
            dEa_dx = _simp(dEa_dx)
            if verbose:
                s = str(dEa_dx)
                if len(s) > 120: s = s[:120] + ' ...'
                print(f"    dE_a/dx = {s}")
            if not (dEa_dx.free_symbols & derivs):
                raise RuntimeError(
                    "E_a is algebraic AND its x-derivative has no "
                    "h_x, q_x — system is degenerate.")
            eqs = [dEa_dx, E_phi]
            alg_constraints.append(E_a)
        elif not Ephi_has_derivs:
            # E_phi algebraic, E_a has derivs — swap roles
            if verbose:
                print(f"\n  ⚠  E_φ has no derivatives — applying DAE index "
                      f"reduction (differentiating constraint)")
            dEphi_dx = (_simp(sp.diff(E_phi, x_s))
                        + _simp(sp.diff(E_phi, h_s))  * h_x_s
                        + _simp(sp.diff(E_phi, vp_s)) * q_s
                        + _simp(sp.diff(E_phi, q_s))  * q_x_s)
            dEphi_dx = _simp(dEphi_dx)
            if not (dEphi_dx.free_symbols & derivs):
                raise RuntimeError(
                    "E_φ is algebraic AND its x-derivative has no "
                    "h_x, q_x — system is degenerate.")
            eqs = [E_a, dEphi_dx]
            alg_constraints.append(E_phi)
        else:
            eqs = [E_a, E_phi]
    else:
        # Pure gravity: only E_a, only h_x
        unknowns = [h_x_s]
        E_a = dimless_eom['a']
        if not (E_a.free_symbols & {h_x_s}):
            raise RuntimeError(
                "E_a contains no h_x — gravity sector is trivial on "
                "FLRW (ghost-free constraints killed all curvature "
                "couplings).")
        eqs = [E_a]
        alg_constraints = []

    if verbose:
        print(f"\n  Solving for RHS:  {[str(u) for u in unknowns]}")

    sol = sp.solve(eqs, unknowns, dict=True)
    if not sol:
        raise RuntimeError("Cannot solve EOM for highest derivatives — "
                           "Lagrangian may be degenerate.")

    rhs = {}
    for u in unknowns:
        if u not in sol[0]:
            raise RuntimeError(
                f"System is underdetermined: cannot isolate {u}. "
                f"The 2×2 system may still be degenerate after "
                f"index reduction.")
        rhs[u] = _simp(sol[0][u])
        if verbose:
            s = str(rhs[u])
            if len(s) > 120: s = s[:120] + ' ...'
            print(f"    {u} = {s}")

    rhs['algebraic_constraints'] = alg_constraints
    return rhs


# ════════════════════════════════════════════════════════════════
#  SECTION 3 :  Pipeline builder (lambdification)
# ════════════════════════════════════════════════════════════════

def _find_free_greeks(dimless_eom, rhs_exprs):
    """Identify unknown Greek coefficients that must be sampled."""
    known = {x_s, h_s, h_x_s, vp_s, q_s, q_x_s,
             mu_s, rhobar_s, eps_s}
    free = set()
    for expr in list(dimless_eom.values()):
        free |= expr.free_symbols
    for k, v in rhs_exprs.items():
        if k == 'algebraic_constraints':
            for ac in v:
                free |= ac.free_symbols
        else:
            free |= v.free_symbols
    greeks = sorted(free - known, key=str)
    return greeks


def build_pipeline(eom_gauged, t_s=t_sym, mode="effective", verbose=True):
    """
    Full preparation: nondimensionalize → extract RHS → lambdify.

    Returns dict with callable rhs_func, constraint_func, and metadata.
    """
    has_phi = 'phi' in eom_gauged

    # 1. Nondimensionalize
    dimless = nondimensionalize_eom(eom_gauged, t_s, mode, verbose)

    # 2. Extract RHS
    rhs_exprs = extract_dimless_rhs(dimless, has_phi, verbose)

    # 3. Identify free Greeks
    free_greeks = _find_free_greeks(dimless, rhs_exprs)
    if verbose:
        print(f"\n  Free couplings to sample: {[str(g) for g in free_greeks]}")

    # 4. Build argument order for lambdify
    state_syms = [h_s, vp_s, q_s] if has_phi else [h_s]

    param_syms  = [rhobar_s]
    param_names = ['rho_bar']
    if has_phi:
        param_syms.append(mu_s);   param_names.append('mu')
    if mode == "eft":
        param_syms.append(eps_s);  param_names.append('eps')
    for g in free_greeks:
        param_syms.append(g);      param_names.append(str(g))

    all_syms = [x_s] + state_syms + param_syms

    # 5. Lambdify RHS
    if has_phi:
        rhs_expr_list = [rhs_exprs[h_x_s], q_s, rhs_exprs[q_x_s]]
    else:
        rhs_expr_list = [rhs_exprs[h_x_s]]

    rhs_lam = [sp.lambdify(all_syms, e, 'numpy') for e in rhs_expr_list]

    # 6. Lambdify constraint (E_N — Friedmann)
    con_expr = dimless.get('N', sp.Integer(0))
    con_lam  = sp.lambdify(all_syms, con_expr, 'numpy')

    # 6b. Lambdify algebraic constraints (from DAE index reduction)
    alg_con_exprs = rhs_exprs.get('algebraic_constraints', [])
    alg_con_lams  = [sp.lambdify(all_syms, e, 'numpy') for e in alg_con_exprs]

    # 7. Wrappers
    def rhs_func(x_val, y, params):
        args = [x_val] + list(y) + list(params)
        try:
            return [float(f(*args)) for f in rhs_lam]
        except (ValueError, ZeroDivisionError, OverflowError):
            return [np.nan] * len(rhs_lam)

    def constraint_func(x_val, y, params):
        args = [x_val] + list(y) + list(params)
        try:
            return float(con_lam(*args))
        except (ValueError, ZeroDivisionError, OverflowError):
            return np.nan

    def alg_constraint_func(x_val, y, params):
        """Evaluate algebraic constraints from DAE reduction. Returns max |residual|."""
        if not alg_con_lams:
            return 0.0
        args = [x_val] + list(y) + list(params)
        try:
            return max(abs(float(f(*args))) for f in alg_con_lams)
        except (ValueError, ZeroDivisionError, OverflowError):
            return np.nan

    if verbose:
        print(f"    param vector:  {param_names}")
        print(f"    state vector:  {['h'] if not has_phi else ['h','varphi','q']}")
        if alg_con_exprs:
            print(f"    algebraic constraints: {len(alg_con_exprs)} "
                  f"(from DAE index reduction)")

    return {
        'rhs_func':            rhs_func,
        'constraint_func':     constraint_func,
        'alg_constraint_func': alg_constraint_func,
        'param_names':         param_names,
        'param_syms':          param_syms,
        'free_greeks':         free_greeks,
        'has_phi':             has_phi,
        'mode':                mode,
        'dimless_eom':         dimless,
        'rhs_exprs':           rhs_exprs,
        'rhs_expr_list':       rhs_expr_list,
        'con_expr':            con_expr,
        'has_alg_constraints': len(alg_con_exprs) > 0,
    }


# ════════════════════════════════════════════════════════════════
#  SECTION 4 :  Constraint solvers (IC determination)
# ════════════════════════════════════════════════════════════════

def solve_constraint_q0(con_func, h0, varphi0, params, *,
                        q0_range=(-10, 10), n_scan=400, max_q0=1.0):
    """
    Solve E_N(x=0, h=h0, φ̃=φ̃₀, q=?) = 0  for q₀.

    Scans q0 ∈ [-10,10], finds sign changes, applies Brent's method.
    Returns q0 with smallest |q0| ≤ max_q0, or None.
    """
    def F(q0):
        return con_func(0.0, [h0, varphi0, q0], params)

    grid = np.linspace(q0_range[0], q0_range[1], n_scan)
    Fv   = np.array([F(q) for q in grid])

    roots = []
    for i in range(len(Fv) - 1):
        if np.isfinite(Fv[i]) and np.isfinite(Fv[i+1]) and Fv[i]*Fv[i+1] < 0:
            try:
                r = brentq(F, grid[i], grid[i+1], xtol=1e-12)
                if np.isfinite(r):
                    roots.append(r)
            except (ValueError, RuntimeError):
                pass
    # Also catch exact zeros
    for i, fv in enumerate(Fv):
        if np.isfinite(fv) and abs(fv) < 1e-12:
            roots.append(float(grid[i]))

    if not roots:
        return None
    roots.sort(key=lambda r: abs(r))
    for r in roots:
        if abs(r) <= max_q0:
            return r
    return roots[0]   # fallback: smallest |q0| even if > max_q0


def solve_constraint_coupling(con_func, h0, params, param_names,
                              free_greeks, search_range=(-50, 50)):
    """
    No-scalar case: solve E_N(x=0, h=1) = 0 for one free coupling.

    Tries each free Greek in order; returns updated params list
    or None if no solution found.
    """
    for g in free_greeks:
        gname = str(g)
        if gname not in param_names:
            continue
        idx = param_names.index(gname)

        def F(val):
            p = list(params); p[idx] = val
            return con_func(0.0, [h0], p)

        grid = np.linspace(search_range[0], search_range[1], 400)
        Fv = np.array([F(v) for v in grid])

        for i in range(len(Fv) - 1):
            if np.isfinite(Fv[i]) and np.isfinite(Fv[i+1]) and Fv[i]*Fv[i+1] < 0:
                try:
                    r = brentq(F, grid[i], grid[i+1])
                    if np.isfinite(r):
                        p_new = list(params); p_new[idx] = r
                        return p_new
                except (ValueError, RuntimeError):
                    pass
    return None


# ════════════════════════════════════════════════════════════════
#  SECTION 5 :  Single-sample IVP solver
# ════════════════════════════════════════════════════════════════

def solve_single(pipe, sample, z_data, H_obs, sigma_H):
    """
    Deterministic solve for one parameter sample.

    Returns dict with chi2, H_model, sol, or None on rejection.
    """
    rhs_func = pipe['rhs_func']
    con_func = pipe['constraint_func']
    has_phi  = pipe['has_phi']
    param_names = pipe['param_names']
    free_greeks = pipe['free_greeks']

    # ── Build params vector ──
    params = [sample['rho_bar']]
    if has_phi:
        params.append(sample['mu'])
    if pipe['mode'] == 'eft':
        params.append(sample['eps'])
    for g in free_greeks:
        params.append(sample[str(g)])

    h0 = 1.0

    # ── Constraint at x = 0 ──
    if has_phi:
        varphi0 = sample['varphi0']
        q0 = solve_constraint_q0(con_func, h0, varphi0, params)
        if q0 is None:
            return None
        # Verify RHS is finite
        y0 = [h0, varphi0, q0]
        dydt = rhs_func(0.0, y0, params)
        if any(not np.isfinite(d) for d in dydt):
            return None
        sample['q0'] = q0
    else:
        # Check constraint; if violated, solve for one coupling
        res0 = con_func(0.0, [h0], params)
        if not np.isfinite(res0) or abs(res0) > 1e-6:
            if free_greeks:
                new_p = solve_constraint_coupling(
                    con_func, h0, params, param_names, free_greeks)
                if new_p is None:
                    return None
                params = new_p
                # Write back solved coupling
                for g in free_greeks:
                    idx = param_names.index(str(g))
                    sample[str(g)] = params[idx]
            else:
                return None
        y0 = [h0]

    # ── Verify initial constraint ──
    res0 = con_func(0.0, y0, params)
    if not np.isfinite(res0) or abs(res0) > 1e-3:
        return None

    # ── Integration span ──
    z_max = z_data.max()
    x_min = -np.log(1 + z_max)

    # ── h > 0 event ──
    def h_zero(x, y):
        return y[0] - 1e-12
    h_zero.terminal  = True
    h_zero.direction = -1

    # ── Integrate ──
    try:
        sol = solve_ivp(
            lambda x, y: rhs_func(x, y, params),
            t_span=(0.0, x_min), y0=y0,
            method='DOP853', rtol=1e-8, atol=1e-10,
            dense_output=True, events=h_zero, max_step=0.05,
        )
    except Exception:
        return None

    if not sol.success or sol.t[-1] > x_min + 0.01:
        # Integration did not reach x_min (terminated early)
        if sol.t_events and len(sol.t_events[0]) > 0:
            return None   # h crossed zero
        if not sol.success:
            return None

    # ── Evaluate at data redshifts ──
    x_data = -np.log(1 + z_data)
    try:
        y_at = sol.sol(x_data)
    except Exception:
        return None

    h_at = y_at[0]
    if np.any(~np.isfinite(h_at)) or np.any(h_at <= 0):
        return None

    if has_phi:
        vp_at = y_at[1]; q_at = y_at[2]
        if (np.any(np.abs(vp_at) > 10) or np.any(np.abs(q_at) > 10) or
            np.any(~np.isfinite(vp_at)) or np.any(~np.isfinite(q_at))):
            return None

    # ── Constraint residual along trajectory ──
    x_check = np.linspace(0, x_min, 50)
    y_check = sol.sol(x_check)
    max_con = 0.0
    alg_con_func = pipe.get('alg_constraint_func')
    max_alg = 0.0
    for j in range(len(x_check)):
        cr = con_func(x_check[j], y_check[:, j], params)
        if np.isfinite(cr):
            max_con = max(max_con, abs(cr))
        else:
            return None
        # Check algebraic constraints from DAE reduction
        if alg_con_func is not None:
            acr = alg_con_func(x_check[j], y_check[:, j], params)
            if np.isfinite(acr):
                max_alg = max(max_alg, acr)
            else:
                return None

    # ── H_model and χ² ──
    H0_km   = sample['H0_km']
    H_model = H0_km * h_at

    if np.any(H_model > 1000) or np.any(H_model < 10):
        return None

    chi2 = float(np.sum(((H_model - H_obs) / sigma_H)**2))
    n_params = len(param_names) + (1 if has_phi else 0) + 1  # +H0
    dof = max(len(z_data) - n_params, 1)

    # Reject if algebraic constraint drifts too far
    if max_alg > 1e-2:
        return None

    return {
        'params':     dict(sample),
        'chi2':       chi2,
        'chi2_dof':   chi2 / dof,
        'H_model':    H_model,
        'h_at_data':  h_at,
        'max_con_res': max_con,
        'max_alg_res': max_alg,
        'constraint_residual_0': res0,
        'sol':        sol,
    }


# ════════════════════════════════════════════════════════════════
#  SECTION 6 :  Monte Carlo driver
# ════════════════════════════════════════════════════════════════

def solve_dimensionless_bao_ivp(
    eom_gauged,
    z_data=None, H_obs=None, sigma_H=None,
    n_samples=1000,
    priors=None,
    mode="effective",
    random_seed=123,
    verbose=True,
):
    """
    Main BAO / H(z) fitting pipeline.

    Parameters
    ----------
    eom_gauged : dict  {'N': E_N, 'a': E_a [, 'phi': E_φ]}
        Ghost-free, N=1 gauge EOM from EOM_v1_7.py.
        Use  result['symbolic_gauged_matter']  (includes dust in E_N).
    mode : "effective" or "eft"
    n_samples : int — MC draws
    priors : dict  — override any default prior range, e.g.
        {'H0_km': (67, 73), 'Omega_m0': (0.28, 0.35)}
        To FIX a parameter: set both bounds equal, e.g.
        {'Omega_m0': (1.0, 1.0)}

    Returns
    -------
    results : list of dicts sorted by χ²  (best first)
    """
    has_phi = 'phi' in eom_gauged

    if verbose:
        print(f"\n{'═' * 60}")
        print(f"  Dimensionless BAO/H(z) Solver  (mode={mode})")
        print(f"{'═' * 60}")

    # ── Build pipeline (symbolic, done once) ──
    t0_build = _time.time()
    pipe = build_pipeline(eom_gauged, mode=mode, verbose=verbose)
    dt_build = _time.time() - t0_build
    if verbose:
        print(f"  Pipeline built in {dt_build:.1f}s")

    free_greeks = pipe['free_greeks']

    # ── Data ──
    if z_data is None:
        z_data  = DEFAULT_HZ['z']
        H_obs   = DEFAULT_HZ['H']
        sigma_H = DEFAULT_HZ['sigma']
    z_data  = np.asarray(z_data, dtype=float)
    H_obs   = np.asarray(H_obs,  dtype=float)
    sigma_H = np.asarray(sigma_H,dtype=float)

    if verbose:
        print(f"\n  Data: {len(z_data)} H(z) points,  z_max = {z_data.max():.2f}")

    # ── Default priors ──
    P = {
        'H0_km':     (60.0, 75.0),
        'Omega_m0':  (0.15, 0.45),
    }
    if has_phi:
        P['varphi0']  = (-0.5, 0.5)
        P['log10_mu'] = (-2.0, 1.0)
    for g in free_greeks:
        gn = str(g)
        if mode == 'eft':
            P[gn] = (-100.0, 100.0)   # O(1) Wilson coeffs
        else:
            P[gn + '_log10'] = (-4.0, 0.0)   # log-uniform magnitude
    if priors:
        P.update(priors)

    # ── MC loop ──
    rng = np.random.default_rng(random_seed)
    results = []
    rej = {'constraint': 0, 'integration': 0, 'validity': 0}

    if verbose:
        print(f"  Running {n_samples} MC samples ...\n")

    t0_mc = _time.time()

    for i in range(n_samples):
        # Draw cosmological params
        lo, hi = P['H0_km']
        H0_km = lo if lo == hi else rng.uniform(lo, hi)

        lo, hi = P['Omega_m0']
        Om0 = lo if lo == hi else rng.uniform(lo, hi)

        rho_bar = 3.0 * Om0
        eps_val = (H0_km * KM_S_MPC_TO_EV) / MPRED_EV

        sample = {
            'H0_km': H0_km, 'Omega_m0': Om0,
            'rho_bar': rho_bar, 'eps': eps_val, 'mode': mode,
        }

        if has_phi:
            lo, hi = P['varphi0']
            sample['varphi0'] = lo if lo == hi else rng.uniform(lo, hi)
            lo, hi = P['log10_mu']
            sample['mu'] = 10.0 ** (lo if lo == hi else rng.uniform(lo, hi))

        # Greek couplings
        for g in free_greeks:
            gn = str(g)
            if gn in P:
                lo, hi = P[gn]
                sample[gn] = lo if lo == hi else rng.uniform(lo, hi)
            else:
                # log-uniform with random sign
                key = gn + '_log10'
                lo, hi = P.get(key, (-4.0, 0.0))
                sign = rng.choice([-1, 1])
                log_mag = lo if lo == hi else rng.uniform(lo, hi)
                sample[gn] = sign * 10.0 ** log_mag

        # Solve
        r = solve_single(pipe, sample, z_data, H_obs, sigma_H)

        if r is None:
            rej['constraint'] += 1
            continue

        results.append(r)

        if verbose and len(results) % 50 == 0:
            print(f"    accepted {len(results)} / {i+1}  "
                  f"(best χ²={min(r['chi2'] for r in results):.1f})")

    dt_mc = _time.time() - t0_mc
    results.sort(key=lambda r: r['chi2'])

    if verbose:
        print(f"\n  {'─' * 56}")
        print(f"  MC done: {dt_mc:.1f}s  "
              f"({dt_mc/max(n_samples,1)*1e3:.1f} ms/sample)")
        print(f"  Accepted: {len(results)} / {n_samples}  "
              f"({100*len(results)/max(n_samples,1):.0f}%)")
        for k, v in rej.items():
            if v: print(f"    rejected ({k}): {v}")
        if results:
            b = results[0]
            print(f"\n  ── Best fit ──")
            print(f"    χ² = {b['chi2']:.2f}  "
                  f"(χ²/dof = {b['chi2_dof']:.2f})")
            print(f"    H₀ = {b['params']['H0_km']:.2f} km/s/Mpc")
            print(f"    Ω_m0 = {b['params']['Omega_m0']:.4f}")
            if has_phi:
                print(f"    φ̃₀ = {b['params'].get('varphi0','?')}")
                print(f"    q₀ = {b['params'].get('q0','?')}")
                print(f"    μ = {b['params'].get('mu','?')}")
            for g in free_greeks:
                print(f"    {g} = {b['params'][str(g)]:.6e}")
            print(f"    max|E_N| = {b['max_con_res']:.2e}")
            if b.get('max_alg_res', 0) > 0:
                print(f"    max|E_a_alg| = {b['max_alg_res']:.2e}"
                      f"  (DAE constraint drift)")

    return results


# ════════════════════════════════════════════════════════════════
#  SECTION 7 :  Self-tests
# ════════════════════════════════════════════════════════════════

def self_test():
    """Verify against GR + dust analytic solution."""
    print("=" * 60)
    print("  SELF-TEST :  Dimensionless cosmology solver")
    print("=" * 60)

    t = t_sym
    a_t   = _a_cls(t)
    adot  = sp.Derivative(a_t, t)
    addot = sp.Derivative(a_t, (t, 2))

    # ── GR + dust EOM ──
    E_N = 3 * M_p_sym**2 * a_t * adot**2 - rho_m0_sym
    E_a = 6 * M_p_sym**2 * a_t * addot + 3 * M_p_sym**2 * adot**2
    eom_gr = {'N': E_N, 'a': E_a}

    # ── Test 1: nondimensionalization ──
    print(f"\n{'─' * 56}")
    print("  Test 1 :  Nondimensionalization (GR+dust, effective)")
    print(f"{'─' * 56}")
    dimless = nondimensionalize_eom(eom_gr, t, mode="effective")

    E_N_expected = 3*h_s**2*sp.exp(3*x_s) - rhobar_s
    E_a_expected = sp.exp(2*x_s) * (9*h_s**2 + 6*h_s*h_x_s)
    assert sp.simplify(dimless['N'] - E_N_expected) == 0, \
        f"FAIL: E_N = {dimless['N']}"
    print(f"  ✓  E_N = 3 h² exp(3x) − ρ̄")
    assert sp.simplify(dimless['a'] - E_a_expected) == 0, \
        f"FAIL: E_a = {dimless['a']}"
    print(f"  ✓  E_a = exp(2x)(9h² + 6h h_x)")

    # ── Test 2: RHS extraction ──
    print(f"\n{'─' * 56}")
    print("  Test 2 :  RHS extraction")
    print(f"{'─' * 56}")
    rhs = extract_dimless_rhs(dimless, has_phi=False)
    expected_hx = sp.Rational(-3, 2) * h_s
    assert sp.simplify(rhs[h_x_s] - expected_hx) == 0, \
        f"FAIL: h_x = {rhs[h_x_s]}"
    print(f"  ✓  h_x = −3h/2  (matter-dominated)")

    # ── Test 3: constraint at x=0 ──
    print(f"\n{'─' * 56}")
    print("  Test 3 :  Constraint at x=0")
    print(f"{'─' * 56}")
    pipe = build_pipeline(eom_gr, mode="effective", verbose=False)
    # With h0=1, rho_bar=3 (Omega_m=1): constraint should be 0
    res = pipe['constraint_func'](0.0, [1.0], [3.0])
    assert abs(res) < 1e-12, f"FAIL: E_N(0) = {res}"
    print(f"  ✓  E_N(x=0, h=1, ρ̄=3) = {res:.2e}")

    # With rho_bar ≠ 3: constraint violated
    res2 = pipe['constraint_func'](0.0, [1.0], [0.9])
    assert abs(res2) > 1, f"FAIL: should be violated"
    print(f"  ✓  E_N(x=0, h=1, ρ̄=0.9) = {res2:.2f}  (violated, correct)")

    # ── Test 4: numerical integration ──
    print(f"\n{'─' * 56}")
    print("  Test 4 :  Numerical integration (GR+dust, Ω_m=1)")
    print(f"{'─' * 56}")
    H0_km = 70.0
    sample = {'H0_km': H0_km, 'Omega_m0': 1.0,
              'rho_bar': 3.0, 'eps': 0.0, 'mode': 'effective'}

    z_test = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    H_exact = H0_km * (1 + z_test)**1.5
    sigma_test = np.ones_like(z_test) * 10.0

    r = solve_single(pipe, sample, z_test, H_exact, sigma_test)
    assert r is not None, "FAIL: solve_single returned None"

    H_model = r['H_model']
    rel_err = np.max(np.abs(H_model - H_exact) / H_exact)
    assert rel_err < 1e-6, f"FAIL: max relative error = {rel_err:.2e}"
    print(f"  ✓  H(z) = H₀(1+z)^{{3/2}} reproduced  (max rel err = {rel_err:.2e})")
    print(f"    χ² = {r['chi2']:.2e}  (should be ~0)")
    print(f"    max|E_N| = {r['max_con_res']:.2e}")

    # ── Test 5: MC with fixed Omega_m0=1 ──
    print(f"\n{'─' * 56}")
    print("  Test 5 :  MC sampling (GR+dust, Ω_m=1 fixed)")
    print(f"{'─' * 56}")
    results = solve_dimensionless_bao_ivp(
        eom_gr, n_samples=100, mode="effective",
        priors={'Omega_m0': (1.0, 1.0), 'H0_km': (65, 75)},
        verbose=False,
    )
    assert len(results) > 0, "FAIL: all samples rejected"
    best = results[0]
    print(f"  ✓  {len(results)}/100 accepted")
    print(f"    Best χ² = {best['chi2']:.1f}  "
          f"(H₀ = {best['params']['H0_km']:.1f})")

    # ── Test 6: MC with Omega_m0 ≠ 1 should fail for pure GR ──
    print(f"\n{'─' * 56}")
    print("  Test 6 :  Pure GR + dust with Ω_m ≠ 1 → all rejected")
    print(f"{'─' * 56}")
    results2 = solve_dimensionless_bao_ivp(
        eom_gr, n_samples=50, mode="effective",
        priors={'Omega_m0': (0.2, 0.4)},
        verbose=False,
    )
    assert len(results2) == 0, f"FAIL: {len(results2)} accepted (should be 0)"
    print(f"  ✓  All 50 samples rejected (no dark energy in pure GR)")

    # ── Test 7: Degenerate scalar (ghost-killed gravity coupling) ──
    # This simulates the outcome of EOM_v1_7 when ghost constraints
    # kill the gravity coupling, leaving only kinetic + mass.
    # E_a should have no h_x → trigger DAE index reduction → singular.
    print(f"\n{'─' * 56}")
    print("  Test 7 :  Degenerate scalar (DAE index reduction)")
    print(f"{'─' * 56}")
    phi_t = _phi_cls(t)
    phidot = sp.Derivative(phi_t, t)
    phiddot = sp.Derivative(phi_t, (t, 2))

    # Free massive scalar without EH:
    # E_N = ½a³φ̇² - ½a³m²φ² - ρ_m0
    # E_a = (3/2)a²φ̇² - (3/2)a²m²φ²     ← no ȧ, no ä
    # E_phi = -a³φ̈ - 3a²ȧφ̇ - a³m²φ     ← has ä? No! ä doesn't appear.
    #   Actually E_phi has φ̈ and ȧ (from 3Hφ̇ term)
    eom_scalar_only = {
        'N':   sp.Rational(1, 2) * M_p_sym**2 * a_t**3 * phidot**2
               - sp.Rational(1, 2) * a_t**3 * m_sym**2 * phi_t**2
               - rho_m0_sym,
        'a':   sp.Rational(3, 2) * M_p_sym**2 * a_t**2 * phidot**2
               - sp.Rational(3, 2) * a_t**2 * m_sym**2 * phi_t**2,
        'phi': -M_p_sym**2 * a_t**3 * phiddot
               - 3 * M_p_sym**2 * a_t**2 * adot * phidot
               - a_t**3 * m_sym**2 * phi_t,
    }

    # Should detect E_a is algebraic, try DAE, then fail (singular)
    try:
        build_pipeline(eom_scalar_only, t, mode="effective", verbose=True)
        print("  ✗  Should have raised RuntimeError!")
        assert False, "FAIL: degenerate scalar should raise"
    except RuntimeError as e:
        msg = str(e)
        assert "KeyError" not in msg, f"FAIL: got KeyError instead of clear msg: {msg}"
        print(f"  ✓  Correctly detected degenerate system:")
        print(f"      \"{msg}\"")

    print(f"\n{'═' * 60}")
    print("  All self-tests passed.")
    print(f"{'═' * 60}\n")


# ════════════════════════════════════════════════════════════════
#  SECTION 8 :  Main — load v1.7 results and solve
# ════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import pickle, datetime

    self_test()

    # ── Try loading v1.7 results ──
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    pkl_candidates = [
        os.path.join(_script_dir, 'eom_results', 'eom_results.pkl'),
        os.path.join(_script_dir, 'eom_results.pkl'),
    ]
    pkl_path = None
    for p in pkl_candidates:
        if os.path.exists(p):
            pkl_path = p; break

    if pkl_path is None:
        print("  No eom_results.pkl found.")
        print("  Run EOM_v1_7.py first, then re-run this solver.")
    else:
        print(f"\n{'═' * 60}")
        print(f"  Loading from: {pkl_path}")
        print(f"{'═' * 60}")

        with open(pkl_path, 'rb') as f:
            all_eom = pickle.load(f)

        MAX_TERMS  = 4
        N_SAMPLES  = 500

        for res in all_eom:
            if res.get('trivial'):
                continue
            eom = res.get('symbolic_gauged_matter')
            if not eom or 'a' not in eom:
                continue
            n_terms = len(res.get('L_data', {}).get('terms', []))
            if n_terms > MAX_TERMS:
                continue

            idx = res['index']
            L_data = res.get('L_data', {})
            print(f"\n{'━' * 60}")
            print(f"  Lagrangian #{idx}  ({n_terms}-term)")
            if 'general' in L_data:
                print(f"  {L_data['general']}")
            print(f"{'━' * 60}")

            try:
                fits = solve_dimensionless_bao_ivp(
                    eom, n_samples=N_SAMPLES, mode="effective",
                    verbose=True,
                )
                if fits:
                    b = fits[0]
                    print(f"\n  Best: χ²={b['chi2']:.1f},  "
                          f"H₀={b['params']['H0_km']:.1f},  "
                          f"Ω_m={b['params']['Omega_m0']:.3f}")
            except Exception as e:
                print(f"  ⚠  Failed: {type(e).__name__}: {e}")