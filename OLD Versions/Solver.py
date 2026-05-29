#!/usr/bin/env python3
"""
eom_solver.py  (v1.0)
=====================
Solver for ghost-free modified gravity EOM produced by EOM_v1_7.py.

Two solving modes
-----------------
  A. **Power series** — Taylor expansion  a(t) = Σ aₙ tⁿ  with a₀, a₁ free.
     Coefficients a_{n≥2} are expressed symbolically in terms of free initial
     data (a₀, a₁) and theory parameters (α, β, …, M_p, m).
     Boundary conditions stay undetermined throughout.

  B. **Numerical IVP** — scipy.integrate.solve_ivp with concrete IC / param
     values, for plotting trajectories once parameters are chosen.

The EOM are assumed to be in N=1 gauge, at most 2nd order (ghost-free).
  • Dynamical equations:  E_a = 0  (and  E_φ = 0  if scalar present)
  • Constraint:           E_N = 0  (checked, not integrated)

Usage (standalone demo):
    python eom_solver.py

Usage (with v1.7):
    from eom_solver import power_series_solve, numerical_solve
    # result = process_lagrangian(...)       # from EOM_v1_7.py
    # eom = result['symbolic_gauged']        # or 'symbolic_gauged_matter'
    # coeffs, constraint, series = power_series_solve(eom)
"""

import sympy as sp
import time as _time
from typing import Dict, List, Tuple, Optional, Any

# ════════════════════════════════════════════════════════════════
#  Shared symbols  (must match EOM_v1_7.py exactly)
# ════════════════════════════════════════════════════════════════

t_sym = sp.Symbol('t', real=True)

_N_cls   = sp.Function('N', positive=True)
_a_cls   = sp.Function('a', positive=True)
_phi_cls = sp.Function('phi')

DYN_FUNCS = [_N_cls, _a_cls, _phi_cls]
DYN_NAMES = ['N', 'a', 'phi']

M_p    = sp.Symbol('M_p', positive=True)
m_sym  = sp.Symbol('m',   positive=True)
rho_m0 = sp.Symbol('rho_{m,0}', positive=True)


# ════════════════════════════════════════════════════════════════
#  Readable printer  (same as v1.7 for consistent output)
# ════════════════════════════════════════════════════════════════

from sympy.printing.str import StrPrinter

class ReadablePrinter(StrPrinter):
    def _print_Derivative(self, expr):
        func = expr.args[0]
        fname = func.func.__name__
        total_order = sum(int(order) for _, order in expr.args[1:])
        num = f"d^{total_order}{fname}" if total_order > 1 else f"d{fname}"
        parts = []
        for var, order in expr.args[1:]:
            order = int(order)
            parts.append(f"d{var}^{order}" if order > 1 else f"d{var}")
        return f"{num}/{''.join(parts)}"

_printer = ReadablePrinter()
def tex(expr):
    return _printer.doprint(expr)


# ════════════════════════════════════════════════════════════════
#  SECTION 1 :  Power Series Solver
# ════════════════════════════════════════════════════════════════
#
#  Algorithm
#  ---------
#  1. Build polynomial Lambdas:
#       a(t) = a_0 + a_1 t + … + a_K t^K
#       φ(t) = φ_0 + φ_1 t + … + φ_K t^K   (if present)
#
#  2. Substitute into each dynamical EOM via .replace(func_cls, Lambda).
#     Call .doit() to evaluate derivatives of the polynomial.
#
#  3. Taylor-expand the resulting expression in t around 0.
#     Coefficient of t^n = 0  gives one equation per EOM.
#
#  4. At each order n, solve for the unknowns {a_{n+2}, [φ_{n+2}]}
#     in terms of previously solved coefficients + free ICs.
#     The highest derivative (ä, φ̈) guarantees these appear linearly.
#
#  5. Substitute into E_N to extract the Friedmann constraint on ICs.
#
#  Requirement:  a_0 ≠ 0  (the expansion fails at the Big Bang
#  singularity).  Physically this means we expand around a time
#  when the scale factor is finite.
# ════════════════════════════════════════════════════════════════

def power_series_solve(
    eom_gauged: Dict[str, sp.Expr],
    t_s:        sp.Symbol = t_sym,
    order:      int       = 6,
    verbose:    bool      = True,
) -> Tuple[Dict, Optional[sp.Expr], Dict]:
    """
    Solve EOM via Taylor expansion around t = 0.

    Parameters
    ----------
    eom_gauged : dict  { 'N': E_N, 'a': E_a [, 'phi': E_φ] }
        EOM in N=1 gauge from v1.7.
    order : int
        Truncation order K.  Series includes t^0 … t^K.
        Higher ⟹ more coefficients solved, but slower (nonlinear algebra).
    verbose : bool
        Print progress and results.

    Returns
    -------
    solved_coeffs  : dict  { a_2: expr, a_3: expr, … }
        Each higher-order coefficient as a function of (a_0, a_1, …,
        Greek params, M_p, m).
    constraint     : sympy Expr or None
        The Friedmann constraint from E_N|_{t=0} = 0,
        already expressed in terms of free ICs and params.
    series_exprs   : dict  { 'a': truncated polynomial, ['phi': …] }
    """

    a_t   = _a_cls(t_s)
    phi_t = _phi_cls(t_s)

    has_a   = 'a'   in eom_gauged
    has_phi = 'phi' in eom_gauged

    if not has_a:
        raise ValueError("No E_a equation found in eom_gauged — nothing to solve")

    # ── 1. Create IC + coefficient symbols ──
    a_syms = [sp.Symbol(f'a_{n}') for n in range(order + 1)]
    a_poly = sum(a_syms[n] * t_s**n for n in range(order + 1))
    a_func = sp.Lambda(t_s, a_poly)

    phi_syms = None
    phi_func = None
    if has_phi:
        phi_syms = [sp.Symbol(f'phi_{n}') for n in range(order + 1)]
        phi_poly = sum(phi_syms[n] * t_s**n for n in range(order + 1))
        phi_func = sp.Lambda(t_s, phi_poly)

    if verbose:
        print(f"\n{'═' * 60}")
        print(f"  Power Series Solver  (truncation order K = {order})")
        print(f"{'═' * 60}")
        dyn_str = 'a' + (', φ' if has_phi else '')
        ic_str  = 'a_0, a_1' + (', phi_0, phi_1' if has_phi else '')
        print(f"  Dynamical variables : {dyn_str}")
        print(f"  Free ICs (BCs)      : {ic_str}")
        print(f"  Requirement         : a_0 ≠ 0")

    # ── 2. Substitute into each dynamical EOM & series-expand ──
    dyn_names = [n for n in ['a', 'phi'] if n in eom_gauged]
    expanded  = {}   # eom_name → {power: coeff_expr}

    for eom_name in dyn_names:
        eq = eom_gauged[eom_name]

        # Replace function classes with polynomial Lambdas
        eq = eq.replace(_a_cls, a_func)
        if phi_func is not None:
            eq = eq.replace(_phi_cls, phi_func)
        eq = eq.doit()      # evaluate derivatives of the polynomial

        if verbose:
            print(f"\n  Expanding E_{eom_name} as power series ...")
        t0 = _time.time()

        # Taylor-expand; we need coefficients t^0 … t^{K-2}
        n_coeffs = order - 1
        eq_series = sp.series(eq, t_s, 0, n=n_coeffs).removeO()
        eq_series = sp.expand(eq_series)

        dt = _time.time() - t0
        if verbose:
            print(f"    done  ({dt:.1f}s)")

        # Extract coefficient of each power of t
        coeff_dict = {}
        for n in range(n_coeffs):
            cn = eq_series.coeff(t_s, n)
            if cn != 0:
                coeff_dict[n] = cn
        expanded[eom_name] = coeff_dict

    # ── 3. Solve recursively, order by order ──
    solved = {}     # {a_2: expr, a_3: expr, phi_2: expr, …}

    if verbose:
        print(f"\n  {'─' * 56}")
        print(f"  Solving coefficients recursively")
        print(f"  {'─' * 56}")

    max_power = order - 2   # highest power of t we can extract from
    for n in range(max_power + 1):
        # Collect equations at order t^n from each dynamical EOM
        eqs_n = []
        for eom_name in dyn_names:
            cn = expanded[eom_name].get(n, sp.Integer(0))
            # Substitute previously solved coefficients
            for sym, val in solved.items():
                cn = cn.subs(sym, val)
            cn = sp.expand(cn)
            if cn != 0:
                eqs_n.append(cn)

        # Unknowns at this order: a_{n+2}  [and phi_{n+2}]
        unknowns_n = []
        if n + 2 <= order:
            unknowns_n.append(a_syms[n + 2])
        if has_phi and phi_syms is not None and n + 2 <= order:
            unknowns_n.append(phi_syms[n + 2])

        if not eqs_n or not unknowns_n:
            continue

        sol = sp.solve(eqs_n, unknowns_n, dict=True)
        if sol:
            for sym, val in sol[0].items():
                val_s = sp.simplify(val)
                solved[sym] = val_s
                if verbose:
                    print(f"    t^{n} :  {sym}  =  {val_s}")
        else:
            if verbose:
                print(f"    t^{n} :  ⚠ could not solve")
                for i, eq in enumerate(eqs_n):
                    print(f"           eq[{i}] = {eq}")

    # ── 4. Build truncated series expressions ──
    series_exprs = {}

    a_series = sp.Integer(0)
    for n in range(order + 1):
        coeff = solved.get(a_syms[n], a_syms[n])
        a_series += coeff * t_s**n
    series_exprs['a'] = sp.collect(sp.expand(a_series), t_s)

    if has_phi and phi_syms is not None:
        phi_series = sp.Integer(0)
        for n in range(order + 1):
            coeff = solved.get(phi_syms[n], phi_syms[n])
            phi_series += coeff * t_s**n
        series_exprs['phi'] = sp.collect(sp.expand(phi_series), t_s)

    # ── 5. Constraint from E_N ──
    constraint = None
    constraint_higher = []

    if 'N' in eom_gauged:
        eq_N = eom_gauged['N']
        eq_N = eq_N.replace(_a_cls, a_func)
        if phi_func is not None:
            eq_N = eq_N.replace(_phi_cls, phi_func)
        eq_N = eq_N.doit()

        if verbose:
            print(f"\n  Expanding E_N for constraint ...")
        n_coeffs_N = order - 1
        eq_N_series = sp.series(eq_N, t_s, 0, n=n_coeffs_N).removeO()
        eq_N_series = sp.expand(eq_N_series)

        # t^0 → Friedmann constraint on ICs
        c0 = eq_N_series.coeff(t_s, 0)
        for sym, val in solved.items():
            c0 = c0.subs(sym, val)
        constraint = sp.simplify(c0)

        if verbose:
            print(f"\n  {'─' * 56}")
            print(f"  Constraint from E_N  (= 0)")
            print(f"  {'─' * 56}")
            print(f"    t^0 :  {constraint}  =  0")

        # Higher-order consistency (should be auto-satisfied)
        for k in range(1, min(4, n_coeffs_N)):
            ck = eq_N_series.coeff(t_s, k)
            for sym, val in solved.items():
                ck = ck.subs(sym, val)
            ck = sp.simplify(ck)
            if ck != 0:
                constraint_higher.append((k, ck))
                if verbose:
                    print(f"    t^{k} :  {ck}  =  0   (consistency)")
            else:
                if verbose:
                    print(f"    t^{k} :  ✓  auto-satisfied")

    # ── 6. Summary ──
    if verbose:
        print(f"\n  {'─' * 56}")
        print(f"  Series solutions")
        print(f"  {'─' * 56}")
        for name, expr in series_exprs.items():
            print(f"\n    {name}(t)  =  {expr}")

    return solved, constraint, series_exprs


# ════════════════════════════════════════════════════════════════
#  SECTION 2 :  Extract Explicit ODE Right-Hand Side
# ════════════════════════════════════════════════════════════════
#
#  From implicit EOM   E_a(a, ȧ, ä, φ, φ̇, φ̈) = 0 ,
#  solve for highest derivatives:
#
#      ä  = f(a, ȧ, φ, φ̇)
#      φ̈ = g(a, ȧ, φ, φ̇)
#
#  The EOM from a Lagrangian are linear in the highest derivatives,
#  so this is always a linear solve.
# ════════════════════════════════════════════════════════════════

def extract_ode_rhs(
    eom_gauged: Dict[str, sp.Expr],
    t_s:        sp.Symbol = t_sym,
    verbose:    bool      = True,
) -> Dict[str, sp.Expr]:
    """
    Solve E_a = 0  (and E_φ = 0)  for ä  (and φ̈)  explicitly.

    Returns  { 'a': expr_for_ä,  ['phi': expr_for_φ̈] }
    where expr is in terms of  a(t), a'(t), [φ(t), φ'(t)]  and params.
    """

    a_t   = _a_cls(t_s)
    phi_t = _phi_cls(t_s)
    a_ddot   = sp.Derivative(a_t,   (t_s, 2))
    phi_ddot = sp.Derivative(phi_t, (t_s, 2))

    dyn_names = [n for n in ['a', 'phi'] if n in eom_gauged]

    # Dummy symbols for highest derivatives
    dum = {
        'a':   sp.Symbol('__addot__'),
        'phi': sp.Symbol('__phiddot__'),
    }
    orig = {
        'a':   a_ddot,
        'phi': phi_ddot,
    }

    # Substitute dummies into dynamical EOM
    eqs   = []
    dummies_used = []
    for name in dyn_names:
        eq = eom_gauged[name]
        for n2 in dyn_names:
            eq = eq.subs(orig[n2], dum[n2])
        eqs.append(eq)
        dummies_used.append(dum[name])

    # Solve linear system for highest derivatives
    sol = sp.solve(eqs, dummies_used, dict=True)
    if not sol:
        raise RuntimeError(
            "Could not solve EOM for highest derivatives — "
            "system may be degenerate or nonlinear in ä, φ̈")
    sol = sol[0]

    # Restore original derivative notation
    rhs = {}
    for name in dyn_names:
        expr = sol[dum[name]]
        for n2 in dyn_names:
            expr = expr.subs(dum[n2], orig[n2])
        rhs[name] = sp.simplify(expr)

    if verbose:
        print(f"\n  {'─' * 56}")
        print(f"  Explicit ODE system")
        print(f"  {'─' * 56}")
        for name, expr in rhs.items():
            deriv_name = "ä" if name == 'a' else "φ̈"
            print(f"    {deriv_name}  =  {tex(expr)}")

    return rhs


# ════════════════════════════════════════════════════════════════
#  SECTION 3 :  Numerical IVP Solver
# ════════════════════════════════════════════════════════════════

def numerical_solve(
    eom_gauged:  Dict[str, sp.Expr],
    param_vals:  Dict,
    ics:         Dict[str, Tuple[float, float]],
    t_span:      Tuple[float, float] = (0.0, 10.0),
    n_points:    int                 = 500,
    t_s:         sp.Symbol           = t_sym,
    method:      str                 = 'RK45',
    verbose:     bool                = True,
    **ivp_kwargs,
):
    """
    Numerically integrate the EOM via scipy.integrate.solve_ivp.

    Parameters
    ----------
    eom_gauged : dict  from v1.7 (N=1 gauge)
    param_vals : dict  { symbol_or_str: float }
        Values for ALL free symbols (Greek coeffs, M_p, m, rho_{m,0}, …).
    ics : dict  { 'a': (a0, adot0),  ['phi': (phi0, phidot0)] }
    t_span : (t_start, t_end)
    n_points : number of output time points
    method : scipy IVP method  ('RK45', 'DOP853', 'Radau', 'BDF', …)

    Returns
    -------
    sol : scipy OdeResult   (sol.t, sol.y, sol.success, …)
         y layout:  [a, ȧ]  or  [a, ȧ, φ, φ̇]
    """
    import numpy as np
    from scipy.integrate import solve_ivp

    # ── Extract explicit RHS ──
    rhs_exprs = extract_ode_rhs(eom_gauged, t_s, verbose=verbose)

    has_a   = 'a'   in rhs_exprs
    has_phi = 'phi' in rhs_exprs

    a_t   = _a_cls(t_s)
    phi_t = _phi_cls(t_s)

    # ── State symbols for lambdify ──
    sa = sp.Symbol('_sa_')
    sv = sp.Symbol('_sv_')
    sp_ = sp.Symbol('_sp_')
    sw = sp.Symbol('_sw_')

    # ── Build lambdified RHS functions ──
    rhs_funcs = {}
    for name, expr in rhs_exprs.items():
        e = expr
        # Substitute parameter values
        for p, val in param_vals.items():
            if isinstance(p, str):
                p = sp.Symbol(p)
            e = e.subs(p, val)

        # Replace function notation → flat state symbols
        if has_a:
            e = e.subs(sp.Derivative(a_t, t_s), sv).subs(a_t, sa)
        if has_phi:
            e = e.subs(sp.Derivative(phi_t, t_s), sw).subs(phi_t, sp_)

        syms = [t_s]
        if has_a:   syms += [sa, sv]
        if has_phi: syms += [sp_, sw]

        rhs_funcs[name] = sp.lambdify(syms, e, modules='numpy')

    # ── scipy RHS ──
    def ode_rhs(t, y):
        args = [t]
        idx = 0
        if has_a:
            args += [y[idx], y[idx + 1]]
            idx += 2
        if has_phi:
            args += [y[idx], y[idx + 1]]

        dydt = []
        if has_a:
            dydt.append(y[1])                          # ȧ
            dydt.append(rhs_funcs['a'](*args))         # ä
        if has_phi:
            pi = 2 if has_a else 0
            dydt.append(y[pi + 1])                     # φ̇
            dydt.append(rhs_funcs['phi'](*args))       # φ̈
        return dydt

    # ── Initial condition vector ──
    y0 = []
    if has_a:
        y0.extend(ics.get('a', (1.0, 1.0)))
    if has_phi:
        y0.extend(ics.get('phi', (0.0, 0.0)))

    t_eval = np.linspace(t_span[0], t_span[1], n_points)

    if verbose:
        print(f"\n  {'─' * 56}")
        print(f"  Numerical integration  ({method})")
        print(f"  {'─' * 56}")
        print(f"    t ∈ [{t_span[0]}, {t_span[1]}],  {n_points} points")
        print(f"    y₀ = {y0}")

    t0 = _time.time()
    sol = solve_ivp(ode_rhs, t_span, y0, t_eval=t_eval,
                    method=method, dense_output=True, **ivp_kwargs)
    dt = _time.time() - t0

    if verbose:
        status = "✓ success" if sol.success else f"⚠ {sol.message}"
        print(f"    {status}  ({dt:.2f}s)")

    return sol


# ════════════════════════════════════════════════════════════════
#  SECTION 4 :  Constraint Monitor
# ════════════════════════════════════════════════════════════════

def check_constraint(
    eom_gauged:  Dict[str, sp.Expr],
    param_vals:  Dict,
    ode_sol,
    t_s:         sp.Symbol = t_sym,
    verbose:     bool      = True,
):
    """
    Evaluate the Hamiltonian constraint  E_N = 0  along a numerical
    solution and return the residual.

    If E_N involves ä or φ̈, those are computed from the explicit RHS.

    Returns  (t_array, residual_array)  or None if no constraint.
    """
    import numpy as np

    if 'N' not in eom_gauged:
        if verbose:
            print("  No E_N constraint found.")
        return None

    eq_N = eom_gauged['N']
    has_a   = 'a'   in eom_gauged
    has_phi = 'phi' in eom_gauged

    a_t   = _a_cls(t_s)
    phi_t = _phi_cls(t_s)

    # If constraint involves ä or φ̈, we need the RHS
    rhs_exprs = None
    a_ddot   = sp.Derivative(a_t, (t_s, 2))
    phi_ddot = sp.Derivative(phi_t, (t_s, 2))
    if eq_N.has(a_ddot) or eq_N.has(phi_ddot):
        rhs_exprs = extract_ode_rhs(eom_gauged, t_s, verbose=False)
        # Substitute ä → RHS into constraint
        if has_a and 'a' in rhs_exprs:
            eq_N = eq_N.subs(a_ddot, rhs_exprs['a'])
        if has_phi and 'phi' in rhs_exprs:
            eq_N = eq_N.subs(phi_ddot, rhs_exprs['phi'])
        eq_N = sp.simplify(eq_N)

    # Substitute parameters
    for p, val in param_vals.items():
        if isinstance(p, str):
            p = sp.Symbol(p)
        eq_N = eq_N.subs(p, val)

    # Replace function notation
    sa = sp.Symbol('_sa_')
    sv = sp.Symbol('_sv_')
    sp_ = sp.Symbol('_sp_')
    sw = sp.Symbol('_sw_')

    e = eq_N
    if has_a:
        e = e.subs(sp.Derivative(a_t, t_s), sv).subs(a_t, sa)
    if has_phi:
        e = e.subs(sp.Derivative(phi_t, t_s), sw).subs(phi_t, sp_)

    syms = [t_s]
    if has_a:   syms += [sa, sv]
    if has_phi: syms += [sp_, sw]

    f_con = sp.lambdify(syms, e, modules='numpy')

    # Evaluate along solution
    t_arr = ode_sol.t
    residual = np.zeros_like(t_arr)
    for i, ti in enumerate(t_arr):
        args = [ti]
        idx = 0
        if has_a:
            args += [ode_sol.y[idx, i], ode_sol.y[idx + 1, i]]
            idx += 2
        if has_phi:
            args += [ode_sol.y[idx, i], ode_sol.y[idx + 1, i]]
        residual[i] = float(f_con(*args))

    if verbose:
        print(f"\n  Constraint |E_N| :  max = {np.max(np.abs(residual)):.2e}, "
              f"mean = {np.mean(np.abs(residual)):.2e}")

    return t_arr, residual


# ════════════════════════════════════════════════════════════════
#  SECTION 5 :  Plotting
# ════════════════════════════════════════════════════════════════

def plot_solution(ode_sol, eom_gauged=None, param_vals=None,
                  title='Modified Gravity Solution'):
    """
    Plot the numerical solution: a(t), ȧ(t), [φ(t), φ̇(t)].
    If eom_gauged and param_vals are given, also plot constraint residual.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    has_phi = ode_sol.y.shape[0] > 2

    n_panels = 2 + (1 if has_phi else 0) + (1 if eom_gauged else 0)
    fig, axes = plt.subplots(n_panels, 1, figsize=(9, 3 * n_panels),
                             sharex=True)
    t = ode_sol.t

    # a(t)
    ax = axes[0]
    ax.plot(t, ode_sol.y[0], 'b-', lw=1.5)
    ax.set_ylabel('a(t)')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)

    # ȧ(t)
    ax = axes[1]
    ax.plot(t, ode_sol.y[1], 'r-', lw=1.5)
    ax.set_ylabel("a'(t)")
    ax.grid(True, alpha=0.3)

    panel = 2
    if has_phi:
        ax = axes[panel]
        ax.plot(t, ode_sol.y[2], 'g-', lw=1.5, label='φ(t)')
        ax.plot(t, ode_sol.y[3], 'g--', lw=1.0, label="φ'(t)")
        ax.set_ylabel('φ(t)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        panel += 1

    if eom_gauged is not None and param_vals is not None:
        result = check_constraint(eom_gauged, param_vals, ode_sol,
                                  verbose=False)
        if result is not None:
            ax = axes[panel]
            ax.semilogy(result[0], np.abs(result[1]) + 1e-30, 'k-', lw=1.0)
            ax.set_ylabel('|E_N| (residual)')
            ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel('t')
    plt.tight_layout()
    plt.savefig('eom_solution.png', dpi=150)
    print(f"\n  Plot saved to: eom_solution.png")
    plt.show()


# ════════════════════════════════════════════════════════════════
#  SECTION 6 :  Self-Test / Demo
# ════════════════════════════════════════════════════════════════
#
#  Uses GR minisuperspace as a test case:
#    L = -3 M_p^2 a ȧ^2 / N    (+ dust source for E_N)
#
#  After N=1 gauge:
#    E_N =  3 M_p^2 a ȧ^2              (Friedmann constraint)
#    E_a =  6 M_p^2 a ä + 3 M_p^2 ȧ^2  (acceleration equation)
# ════════════════════════════════════════════════════════════════

def self_test():
    """Demo: solve GR Friedmann equations via power series."""

    print("=" * 60)
    print("  SELF-TEST / DEMO :  GR minisuperspace")
    print("=" * 60)

    t = t_sym
    a_t   = _a_cls(t)
    phi_t = _phi_cls(t)
    adot  = sp.Derivative(a_t, t)
    addot = sp.Derivative(a_t, (t, 2))

    # ── Build GR EOM (N=1 gauge) ──
    # L = -3 M_p^2 a ȧ^2 / N  → after EL and N=1:
    E_N = 3 * M_p**2 * a_t * adot**2
    E_a = 6 * M_p**2 * a_t * addot + 3 * M_p**2 * adot**2

    eom_gr = {'N': E_N, 'a': E_a}
    print(f"\n  E_N = {tex(E_N)}")
    print(f"  E_a = {tex(E_a)}")

    # ── Test 1: power series (vacuum) ──
    print(f"\n{'─' * 60}")
    print("  Test 1 : Power series solve (vacuum GR)")
    print(f"{'─' * 60}")
    coeffs, constraint, series = power_series_solve(eom_gr, t, order=8)

    # Verify: vacuum Friedmann ⟹ constraint is 3 M_p^2 a_0 a_1^2 = 0
    a_0 = sp.Symbol('a_0')
    a_1 = sp.Symbol('a_1')
    expected_constraint = 3 * M_p**2 * a_0 * a_1**2
    assert sp.simplify(constraint - expected_constraint) == 0, \
        f"FAIL: constraint = {constraint}, expected {expected_constraint}"
    print(f"\n  ✓  Constraint matches: 3 M_p² a_0 a_1² = 0")

    # In vacuum with a_1 = 0 (satisfying constraint), series should be a(t) = a_0
    a_check = series['a'].subs(a_1, 0)
    assert sp.simplify(a_check - a_0) == 0, \
        f"FAIL: a(t)|_{{a_1=0}} = {a_check}, expected a_0"
    print(f"  ✓  a_1=0 ⟹ a(t) = a_0  (Minkowski, as expected)")

    # ── Test 2: power series (with dust) ──
    print(f"\n{'─' * 60}")
    print("  Test 2 : Power series solve (GR + dust)")
    print(f"{'─' * 60}")
    eom_dust = {
        'N': E_N - rho_m0,       # Friedmann constraint with dust
        'a': E_a,                 # acceleration unchanged (dust enters only E_N)
    }
    coeffs_d, constraint_d, series_d = power_series_solve(eom_dust, t, order=8)

    # Constraint: 3 M_p^2 a_0 a_1^2 - ρ_{m,0} = 0
    expected_d = 3 * M_p**2 * a_0 * a_1**2 - rho_m0
    assert sp.simplify(constraint_d - expected_d) == 0, \
        f"FAIL: {constraint_d} ≠ {expected_d}"
    print(f"\n  ✓  Constraint: 3 M_p² a_0 a_1² = ρ_{{m,0}}")

    # ── Test 3: numerical solve (vacuum GR) ──
    print(f"\n{'─' * 60}")
    print("  Test 3 : Numerical solve (vacuum GR, a_1=0 ⟹ static)")
    print(f"{'─' * 60}")
    try:
        sol = numerical_solve(
            eom_gr,
            param_vals={M_p: 1},
            ics={'a': (1.0, 0.0)},       # a_0=1, ȧ_0=0 (vacuum → static)
            t_span=(0, 5),
            n_points=100,
        )
        import numpy as np
        # Should be a(t) ≈ 1 everywhere
        assert np.allclose(sol.y[0], 1.0, atol=1e-8), \
            f"FAIL: a(t) deviates from 1"
        print(f"  ✓  a(t) ≈ 1.0  (max deviation: {np.max(np.abs(sol.y[0]-1)):.2e})")
    except ImportError:
        print("  (scipy not available — skipping numerical test)")

    # ── Test 4: explicit RHS extraction ──
    print(f"\n{'─' * 60}")
    print("  Test 4 : Extract explicit ODE RHS")
    print(f"{'─' * 60}")
    rhs = extract_ode_rhs(eom_gr, t)
    # Expected: ä = -ȧ²/(2a)
    expected_rhs = -adot**2 / (2 * a_t)
    assert sp.simplify(rhs['a'] - expected_rhs) == 0, \
        f"FAIL: RHS = {rhs['a']}, expected {expected_rhs}"
    print(f"  ✓  ä = -ȧ²/(2a)  — correct")

    print(f"\n{'═' * 60}")
    print("  All self-tests passed.")
    print(f"{'═' * 60}\n")


# ════════════════════════════════════════════════════════════════
#  SECTION 7 :  Main — load v1.7 results and solve
# ════════════════════════════════════════════════════════════════
#
#  If run standalone, demonstrates on GR, then looks for v1.7
#  result pickle.  To chain with v1.7 programmatically:
#
#      from EOM_v1_7 import process_lagrangian
#      result = process_lagrangian(L_data, idx, ...)
#      eom = result['symbolic_gauged']          # vacuum
#      eom = result['symbolic_gauged_matter']   # with dust
#
#      from eom_solver import power_series_solve
#      coeffs, constraint, series = power_series_solve(eom, order=8)
# ════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import pickle, os

    # Run self-tests / demo
    self_test()

    # ── Try loading v1.7 results ──
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    pkl_path = os.path.join(_script_dir, 'eom_results.pkl')

    if not os.path.exists(pkl_path):
        print(f"  No eom_results.pkl found at: {pkl_path}")
        print(f"  To solve v1.7 Lagrangians, either:")
        print(f"    1. Save v1.7 results to eom_results.pkl, or")
        print(f"    2. Import both modules and chain them:")
        print(f"         from EOM_v1_7 import process_lagrangian")
        print(f"         from eom_solver import power_series_solve")
        print(f"         result = process_lagrangian(L_data, 1, ...)")
        print(f"         eom = result['symbolic_gauged']")
        print(f"         coeffs, con, series = power_series_solve(eom)")
    else:
        print(f"\n{'═' * 60}")
        print(f"  Loading v1.7 results from: {pkl_path}")
        print(f"{'═' * 60}")

        with open(pkl_path, 'rb') as f:
            all_results = pickle.load(f)

        for result in all_results:
            if result.get('trivial'):
                continue
            idx = result['index']
            eom = result.get('symbolic_gauged')
            if not eom:
                continue
            if 'a' not in eom:
                continue

            print(f"\n{'━' * 60}")
            print(f"  Solving Lagrangian #{idx}")
            print(f"{'━' * 60}")

            # Power series (vacuum)
            coeffs, con, series = power_series_solve(eom, order=6)

            # Power series (with dust, if available)
            eom_m = result.get('symbolic_gauged_matter')
            if eom_m and 'a' in eom_m:
                print(f"\n  ── With dust source ──")
                coeffs_m, con_m, series_m = power_series_solve(eom_m, order=6)