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

# ── Fast simplify: _simp is ~50x slower than cancel/expand ──
# Use cancel + powsimp as default; full simplify only in self-tests.
def _simp(expr):
    """Fast simplification: cancel → powsimp.  10-50x faster than _simp."""
    try:
        return sp.powsimp(sp.cancel(expr))
    except Exception:
        return sp.cancel(expr)

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
    enforce_constraint: bool = True,
    solve_for:  Optional[sp.Symbol] = None,
    verbose:    bool      = True,
) -> Tuple[Dict, Optional[sp.Expr], Dict, Optional[Dict]]:
    """
    Solve EOM via Taylor expansion around t = 0.

    Parameters
    ----------
    eom_gauged : dict  { 'N': E_N, 'a': E_a [, 'phi': E_φ] }
        EOM in N=1 gauge from v1.7.
    order : int
        Truncation order K.  Series includes t^0 … t^K.
    enforce_constraint : bool
        If True (default), solve E_N|_{t=0} = 0 for one IC and
        substitute back.  The constrained series lives on the
        Friedmann constraint surface.
    solve_for : Symbol or None
        Which IC to eliminate via the constraint.
        Default: a_1  (i.e. ȧ(0)).
    verbose : bool
        Print progress and results.

    Returns
    -------
    solved_coeffs  : dict  { a_2: expr, a_3: expr, … }
        Unconstrained coefficients (all ICs free).
    constraint     : sympy Expr or None
        The Friedmann constraint from E_N|_{t=0} = 0.
    series_exprs   : dict  { 'a': truncated polynomial, ['phi': …] }
        Unconstrained series.
    constrained    : dict or None
        If enforce_constraint is True and constraint is solvable:
          { 'solved':   constrained coefficients,
            'series':   constrained series expressions,
            'ic_subs':  { eliminated_IC: value },
            'all_solutions': list of all constraint solutions }
        Otherwise None.
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
                val_s = _simp(val)
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
        constraint = _simp(c0)

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
            ck = _simp(ck)
            if ck != 0:
                constraint_higher.append((k, ck))
                if verbose:
                    print(f"    t^{k} :  {ck}  =  0   (consistency)")
            else:
                if verbose:
                    print(f"    t^{k} :  ✓  auto-satisfied")

    # ── 6. Enforce Friedmann constraint ──
    constrained = None

    if constraint is not None and enforce_constraint and constraint != 0:
        # Which IC to eliminate?  Default: a_1  (= ȧ(0))
        target = solve_for if solve_for is not None else a_syms[1]

        con_sols = sp.solve(constraint, target)

        if con_sols:
            if verbose:
                print(f"\n  {'─' * 56}")
                print(f"  Enforcing Friedmann constraint")
                print(f"  {'─' * 56}")
                print(f"    {constraint} = 0   →   solve for {target} :")
                for i, cs in enumerate(con_sols):
                    print(f"      [{i+1}]  {target} = {cs}")

            # Use first solution as primary (keep all for user)
            ic_val = con_sols[0]

            # Substitute into all solved coefficients
            c_solved = {}
            for sym, val in solved.items():
                c_solved[sym] = _simp(val.subs(target, ic_val))

            # Build constrained series
            c_series = {}
            for name, expr in series_exprs.items():
                c_series[name] = sp.collect(
                    sp.expand(expr.subs(target, ic_val)), t_s)

            constrained = {
                'solved':         c_solved,
                'series':         c_series,
                'ic_subs':        {target: ic_val},
                'all_solutions':  [{target: cs} for cs in con_sols],
            }

            if verbose:
                remaining = [s for s in [a_syms[0]]
                             + ([phi_syms[0], phi_syms[1]]
                                if has_phi and phi_syms else [])
                             if s != target]
                print(f"\n    Remaining free ICs: {[str(s) for s in remaining]}")
                print(f"\n  ── Constrained series ──")
                for name, expr in c_series.items():
                    print(f"\n    {name}(t)  =  {expr}")
        else:
            if verbose:
                print(f"\n  ⚠  Could not solve constraint for {target}")

    # ── 7. Unconstrained summary ──
    if verbose:
        print(f"\n  {'─' * 56}")
        print(f"  Unconstrained series  (all ICs free)")
        print(f"  {'─' * 56}")
        for name, expr in series_exprs.items():
            print(f"\n    {name}(t)  =  {expr}")

    return solved, constraint, series_exprs, constrained


# ════════════════════════════════════════════════════════════════
#  SECTION 1a :  Padé Approximant
# ════════════════════════════════════════════════════════════════
#
#  Given Taylor coefficients c₀, c₁, …, c_K, build the [m/n]
#  Padé approximant  P_m(t) / Q_n(t)  that matches the series
#  to order m + n.
#
#  Rational functions approximate functions with poles, branch
#  cuts, and exponential growth FAR better than polynomials.
#  For the same number of coefficients the effective range of
#  approximation is typically 2–10× larger.
# ════════════════════════════════════════════════════════════════

def pade_approximant(
    series_or_coeffs,
    t_s:     sp.Symbol = t_sym,
    m:       Optional[int] = None,
    n:       Optional[int] = None,
    verbose: bool = True,
):
    """
    Build a [m/n] Padé approximant from a truncated Taylor series.

    Parameters
    ----------
    series_or_coeffs : sympy Expr  or  list
        Either a polynomial expression in t_s (from power_series_solve),
        or a list of coefficients [c_0, c_1, …, c_K].
    t_s : time symbol
    m, n : numerator/denominator degrees.
        Default: diagonal Padé  [K//2, K//2].

    Returns
    -------
    (P, Q) : numerator and denominator polynomials in t_s.
        The Padé approximant is  P(t) / Q(t).
    """

    # ── Extract coefficient list ──
    if isinstance(series_or_coeffs, (list, tuple)):
        coeffs = list(series_or_coeffs)
    else:
        # It's a sympy expression — extract coefficients of t^k
        expr = sp.Poly(sp.expand(series_or_coeffs), t_s)
        K = expr.degree()
        coeffs = [expr.nth(k) for k in range(K + 1)]

    K = len(coeffs) - 1

    # Default: diagonal Padé
    if m is None and n is None:
        m = K // 2
        n = K - m
    elif m is None:
        m = K - n
    elif n is None:
        n = K - m

    assert m + n <= K, f"Need ≥ {m+n+1} coefficients, have {K+1}"
    assert m >= 0 and n >= 0

    c = coeffs

    if verbose:
        print(f"\n  Building [{m}/{n}] Padé approximant from {K+1} Taylor coefficients")

    if n == 0:
        # Pure polynomial (Taylor truncation)
        P = sum(c[k] * t_s**k for k in range(m + 1))
        return P, sp.Integer(1)

    # ── Solve for denominator coefficients q_1, …, q_n ──
    #
    #  System:  c_{m+j} + Σ_{i=1}^{n} q_i · c_{m+j-i} = 0
    #           for  j = 1, …, n
    #
    A_mat = sp.zeros(n, n)
    b_vec = sp.zeros(n, 1)
    for j in range(n):
        row = m + 1 + j          # equation index: order m+1+j
        b_vec[j] = -c[row] if row <= K else sp.Integer(0)
        for i in range(n):
            idx = m + j - i      # coefficient index
            A_mat[j, i] = c[idx] if 0 <= idx <= K else sp.Integer(0)

    try:
        q_vec = A_mat.solve(b_vec)
    except Exception:
        if verbose:
            print(f"    ⚠  Padé system singular — falling back to [{m}/0]")
        P = sum(c[k] * t_s**k for k in range(m + 1))
        return P, sp.Integer(1)

    q = [_simp(q_vec[i]) for i in range(n)]

    # ── Compute numerator coefficients p_0, …, p_m ──
    p = []
    for k in range(m + 1):
        pk = c[k]
        for i in range(1, min(k, n) + 1):
            pk += q[i - 1] * c[k - i]
        p.append(_simp(pk))

    P = sum(p[k] * t_s**k for k in range(m + 1))
    Q = sp.Integer(1) + sum(q[i] * t_s**(i + 1) for i in range(n))

    if verbose:
        print(f"    P(t) = {P}")
        print(f"    Q(t) = {Q}")

    return P, Q


# ════════════════════════════════════════════════════════════════
#  SECTION 1c :  e-folds Hubble Solver   H(x)
# ════════════════════════════════════════════════════════════════
#
#  Motivation
#  ----------
#  Taylor expanding  a(t)  in t  fails at late times because
#  a(t) grows exponentially (de Sitter).  No polynomial
#  converges to  exp(Ht).
#
#  Fix: change independent variable to  x = ln a  ("e-folds").
#  Then  H(x) = ȧ/(a)  is bounded and smooth, and
#  the 2nd-order ODE for a(t) reduces to a 1st-order ODE
#  for H(x):
#
#      a  = e^N  (normalised),    ȧ = H·a,
#      ä  = (H·H' + H²)·a        where ' = d/dN
#
#  Substituting into  E_a = 0  and dividing out a^k  gives
#  an ODE in H(x) that can be Taylor- or Padé-expanded
#  with excellent convergence.
# ════════════════════════════════════════════════════════════════

# e-folds symbol
x_efold = sp.Symbol('x')
_H_cls  = sp.Function('H_x', positive=True)   # H(x)

def efolds_transform(
    eom_gauged: Dict[str, sp.Expr],
    t_s:        sp.Symbol = t_sym,
    verbose:    bool      = True,
) -> Dict[str, sp.Expr]:
    """
    Transform gauge-fixed EOM from  a(t)  to  H(x),  x = ln a.

    Substitution rules (N=1 gauge, no lapse derivatives):
      a(t)  →  exp(N)
      ȧ     →  H(x) · exp(N)
      ä     →  [H(x)·H'(x) + H(x)²] · exp(N)

    If scalar φ is present:
      φ(t)  →  φ(x)          [now a function of N]
      φ̇    →  H(x) · φ'(x)
      φ̈    →  H² φ'' + H H' φ'

    Returns
    -------
    eom_x : dict  { 'N': ..., 'a': ..., ['phi': ...] }
        EOM in terms of H(x), H'(x), [φ(x), φ'(x), φ''(x)].
    """

    x = x_efold
    H  = _H_cls(x)
    Hp = sp.Derivative(H, x)       # H'(x)

    a_t   = _a_cls(t_s)
    phi_t = _phi_cls(t_s)

    # φ as function of x
    _phi_x_cls = sp.Function('phi')
    phi_x = _phi_x_cls(x)
    phi_xp = sp.Derivative(phi_x, x)
    phi_xpp = sp.Derivative(phi_x, (x, 2))

    has_phi = 'phi' in eom_gauged

    if verbose:
        print(f"\n{'═' * 60}")
        print(f"  e-folds transformation :  x = ln a,  H(x) = ȧ/a")
        print(f"{'═' * 60}")

    eom_x = {}
    for eom_name, eq in eom_gauged.items():
        e = eq

        # ── a(t) substitutions (highest derivative first) ──
        e = e.subs(sp.Derivative(a_t, (t_s, 2)),
                   (H * Hp + H**2) * sp.exp(x))
        e = e.subs(sp.Derivative(a_t, t_s),
                   H * sp.exp(x))
        e = e.subs(a_t, sp.exp(x))

        # ── φ(t) substitutions ──
        if has_phi:
            e = e.subs(sp.Derivative(phi_t, (t_s, 2)),
                       H**2 * phi_xpp + H * Hp * phi_xp)
            e = e.subs(sp.Derivative(phi_t, t_s),
                       H * phi_xp)
            e = e.subs(phi_t, phi_x)

        e = _simp(e)

        # ── Factor out exp(x) powers ──
        # The EOM typically has overall a^k = exp(kx) factor
        try:
            e_reduced = sp.cancel(e * sp.exp(-x))
            if not e_reduced.has(sp.exp):
                e = e_reduced
            else:
                e_reduced2 = sp.cancel(e * sp.exp(-2*x))
                if not e_reduced2.has(sp.exp):
                    e = e_reduced2
                else:
                    e_reduced3 = sp.cancel(e * sp.exp(-3*x))
                    if not e_reduced3.has(sp.exp):
                        e = e_reduced3
                    else:
                        e = _simp(e)
        except Exception:
            pass

        eom_x[eom_name] = e

        if verbose:
            print(f"\n  E_{eom_name}(x)  =  {tex(e)}")

    return eom_x


def efolds_solve(
    eom_gauged: Dict[str, sp.Expr],
    t_s:        sp.Symbol = t_sym,
    order:      int       = 6,
    expand_at:  float     = 0,
    verbose:    bool      = True,
) -> Tuple[Dict, Optional[sp.Expr], Dict]:
    """
    Solve EOM via e-folds expansion  H(x) = H₀ + H₁ N + H₂ N² + …

    Steps:
      1. Transform EOM from a(t) to H(x)
      2. Use E_N (Friedmann constraint) as the dynamical equation for H
         (it's algebraic or 1st-order in H after transformation)
      3. Taylor-expand H(x) around N = expand_at
      4. Return coefficients as functions of H₀ and theory params

    Parameters
    ----------
    expand_at : float or Symbol
        Expansion point in N.  Default 0 (= today if a(t₀)=1).

    Returns
    -------
    solved_coeffs : { H_1: expr, H_2: expr, … }
    constraint    : algebraic relation on H₀ from E_a
    series_H      : { 'H': truncated series H(x) }
    """

    x = x_efold
    H_func = _H_cls

    # ── 1. Transform to e-folds ──
    eom_x = efolds_transform(eom_gauged, t_s, verbose=verbose)

    # ── 2. Build polynomial for H(x) ──
    H_syms = [sp.Symbol(f'H_{k}') for k in range(order + 1)]
    dx = x - expand_at
    H_poly = sum(H_syms[k] * dx**k for k in range(order + 1))
    H_lambda = sp.Lambda(x, H_poly)

    # Also handle φ(x) if present
    has_phi = 'phi' in eom_x
    phi_syms = None
    phi_lambda = None
    if has_phi:
        phi_syms = [sp.Symbol(f'phix_{k}') for k in range(order + 1)]
        phi_poly = sum(phi_syms[k] * dx**k for k in range(order + 1))
        phi_lambda = sp.Lambda(x, phi_poly)

    if verbose:
        print(f"\n  Expanding H(x) around x = {expand_at}, order {order}")
        ic_str = f"H_0 = H(x={expand_at})"
        if has_phi:
            ic_str += f",  phix_0 = φ(x={expand_at})"
        print(f"  Free ICs: {ic_str}")

    # ── 3. Choose which equation(s) to expand ──
    #  E_N is typically algebraic in H (no H') → gives constraint + series
    #  E_a involves H' → can use as dynamical equation
    #  Strategy: use E_a (which has H') for the power series solve

    # Substitute H(x) polynomial into the dynamical equation (E_a)
    target_eom = 'a' if 'a' in eom_x else list(eom_x.keys())[0]
    eq = eom_x[target_eom]
    eq = eq.replace(H_func, H_lambda)
    if has_phi and phi_lambda is not None:
        _phi_x_cls2 = sp.Function('phi')
        eq = eq.replace(_phi_x_cls2, phi_lambda)
    eq = eq.doit()

    # Series expand around N = expand_at
    n_terms = order - 1
    eq_series = sp.series(eq, x, expand_at, n=n_terms).removeO()
    eq_series = sp.expand(eq_series)

    # ── 4. Solve order by order ──
    solved = {}

    if verbose:
        print(f"\n  {'─' * 56}")
        print(f"  Solving H(x) coefficients")
        print(f"  {'─' * 56}")

    for k in range(n_terms):
        coeff_k = eq_series.coeff(dx, k) if expand_at == 0 else \
                  eq_series.coeff((x - expand_at), k)
        # Substitute previously solved
        for sym, val in solved.items():
            coeff_k = coeff_k.subs(sym, val)
        coeff_k = sp.expand(coeff_k)

        if coeff_k == 0:
            continue

        # Unknown at this order: H_{k+1}  (from H' contribution)
        unknowns = []
        if k + 1 <= order:
            unknowns.append(H_syms[k + 1])
        if has_phi and phi_syms and k + 1 <= order:
            unknowns.append(phi_syms[k + 1])

        if not unknowns:
            continue

        sol = sp.solve(coeff_k, unknowns[0])
        if sol:
            val = _simp(sol[0]) if isinstance(sol, list) else _simp(sol)
            solved[unknowns[0]] = val
            if verbose:
                print(f"    x^{k} :  {unknowns[0]} = {val}")
        else:
            if verbose:
                print(f"    x^{k} :  ⚠ could not solve ({coeff_k} = 0)")

    # ── 5. Constraint from E_N ──
    constraint = None
    if 'N' in eom_x and target_eom != 'N':
        eq_con = eom_x['N']
        eq_con = eq_con.replace(H_func, H_lambda)
        if has_phi and phi_lambda is not None:
            _phi_x_cls2 = sp.Function('phi')
            eq_con = eq_con.replace(_phi_x_cls2, phi_lambda)
        eq_con = eq_con.doit()
        eq_con_0 = _simp(eq_con.subs(x, expand_at))
        for sym, val in solved.items():
            eq_con_0 = eq_con_0.subs(sym, val)
        constraint = _simp(eq_con_0)
        if verbose:
            print(f"\n  Friedmann constraint at x={expand_at}:")
            print(f"    {constraint} = 0")

    # ── 6. Build H(x) series ──
    H_series = sp.Integer(0)
    for k in range(order + 1):
        coeff = solved.get(H_syms[k], H_syms[k])
        H_series += coeff * dx**k
    H_series = sp.collect(sp.expand(H_series), dx if expand_at == 0 else (x - expand_at))

    series_result = {'H': H_series}

    if verbose:
        print(f"\n  H(x) = {H_series}")

    # ── 7. Padé of H(x) ──
    H_coeffs = [solved.get(H_syms[k], H_syms[k]) for k in range(order + 1)]
    # Only build Padé if enough numeric-like coefficients were solved
    n_solved = sum(1 for k in range(order + 1) if H_syms[k] in solved)
    if n_solved >= 3:
        try:
            P, Q = pade_approximant(H_coeffs, x, verbose=verbose)
            series_result['H_pade'] = (P, Q)
            if verbose:
                print(f"\n  Padé approximant:  H(x) ≈ [{P}] / [{Q}]")
        except Exception:
            pass

    return solved, constraint, series_result


# ════════════════════════════════════════════════════════════════
#  SECTION 1b :  Closed-Form Analytical Solvers
# ════════════════════════════════════════════════════════════════
#
#  Three strategies for obtaining exact solutions with
#  undetermined integration constants:
#
#    A. sp.dsolve  — general-purpose ODE solver
#    B. Power-law ansatz   a(t) = A · t^p
#    C. Exponential ansatz a(t) = A · exp(H·t)
#
#  For FLRW cosmology the ansätze are the workhorses:
#    • p = 2/3  →  matter-dominated expansion
#    • p = 1/2  →  radiation-dominated expansion
#    • exp(Ht)  →  de Sitter (Λ-driven) expansion
# ════════════════════════════════════════════════════════════════

# ── A. Symbolic dsolve ─────────────────────────────────────────

def symbolic_dsolve(
    eom_gauged: Dict[str, sp.Expr],
    t_s:        sp.Symbol = t_sym,
    verbose:    bool      = True,
) -> Dict[str, Any]:
    """
    Attempt closed-form solution via sympy.dsolve.

    For a single dynamical variable (only E_a), calls dsolve directly.
    For a coupled system (E_a + E_φ), tries the system first,
    then falls back to solving each equation separately.

    Returns  { 'a': Eq(a(t), …),  ['phi': Eq(φ(t), …)] }
    or error strings where dsolve could not find a solution.
    """

    a_t   = _a_cls(t_s)
    phi_t = _phi_cls(t_s)

    has_a   = 'a'   in eom_gauged
    has_phi = 'phi' in eom_gauged
    results = {}

    if verbose:
        print(f"\n{'═' * 60}")
        print(f"  Analytical dsolve")
        print(f"{'═' * 60}")

    # ── Coupled system ──
    if has_a and has_phi:
        eq_a   = sp.Eq(eom_gauged['a'],   0)
        eq_phi = sp.Eq(eom_gauged['phi'], 0)

        if verbose:
            print(f"  Trying coupled system dsolve(E_a, E_φ) ...")

        try:
            sol = sp.dsolve([eq_a, eq_phi], [a_t, phi_t])
            if isinstance(sol, list):
                for s in sol:
                    if s.lhs == a_t:
                        results['a'] = s
                    elif s.lhs == phi_t:
                        results['phi'] = s
            else:
                results['system'] = sol
            if verbose:
                print(f"    ✓  System solved")
                for k, v in results.items():
                    print(f"    {k}: {v}")
            return results
        except Exception as e:
            if verbose:
                print(f"    ✗  System dsolve failed: {type(e).__name__}")

        # Fallback: try each independently
        if verbose:
            print(f"  Falling back to separate dsolve ...")

    # ── Single equations ──
    for name, func in [('a', a_t), ('phi', phi_t)]:
        if name not in eom_gauged:
            continue
        eq = sp.Eq(eom_gauged[name], 0)
        if verbose:
            print(f"  dsolve(E_{name} = 0, {name}(t)) ...")
        try:
            sol = sp.dsolve(eq, func)
            results[name] = sol
            if verbose:
                if isinstance(sol, list):
                    for s in sol:
                        print(f"    ✓  {s}")
                else:
                    print(f"    ✓  {sol}")
        except Exception as e:
            err_msg = f"{type(e).__name__}: {e}"
            results[name] = err_msg
            if verbose:
                print(f"    ✗  {err_msg}")

    return results


# ── B. Power-law ansatz ────────────────────────────────────────

def ansatz_power_law(
    eom_gauged: Dict[str, sp.Expr],
    t_s:        sp.Symbol = t_sym,
    verbose:    bool      = True,
) -> Dict[str, Any]:
    """
    Substitute  a(t) = A · t^p  [and  φ(t) = B · t^q]
    into the EOM.  Solve for the exponents and amplitudes.

    For FLRW Lagrangians built from curvature invariants,
    each term acquires the same power of t after substitution,
    so the equation reduces to an algebraic system in (p, A, …).

    Returns
    -------
    dict with keys:
      'p_solutions'  : list of dicts  { p: value, [q: value] }
      'A_relations'  : list of expressions relating A to params
      'constraint'   : E_N evaluated on the ansatz (= 0)
      'verified'     : whether each solution was verified symbolically
    """

    a_t   = _a_cls(t_s)
    phi_t = _phi_cls(t_s)

    has_a   = 'a'   in eom_gauged
    has_phi = 'phi' in eom_gauged

    # Ansatz symbols
    A_sym = sp.Symbol('A', positive=True)
    p_sym = sp.Symbol('p', real=True)
    a_ansatz = sp.Lambda(t_s, A_sym * t_s**p_sym)

    B_sym = sp.Symbol('B')
    q_sym = sp.Symbol('q', real=True)
    phi_ansatz = sp.Lambda(t_s, B_sym * t_s**q_sym)

    if verbose:
        print(f"\n{'═' * 60}")
        print(f"  Power-law ansatz :  a(t) = A·t^p"
              + ("  ,  φ(t) = B·t^q" if has_phi else ""))
        print(f"{'═' * 60}")

    # ── Substitute into each dynamical EOM ──
    dyn_eqs_at_1 = {}    # EOM evaluated at t = 1 (algebraic in A, p, …)
    dyn_eqs_full = {}    # full expression (for verification)

    for eom_name in ['a', 'phi']:
        if eom_name not in eom_gauged:
            continue

        eq = eom_gauged[eom_name]
        eq = eq.replace(_a_cls, a_ansatz)
        if has_phi:
            eq = eq.replace(_phi_cls, phi_ansatz)
        eq = eq.doit()
        eq = sp.powsimp(sp.expand(eq))

        dyn_eqs_full[eom_name] = eq
        dyn_eqs_at_1[eom_name] = _simp(eq.subs(t_s, 1))

    # ── Solve algebraic system at t = 1 ──
    unknowns = [p_sym]
    if has_phi:
        unknowns.append(q_sym)

    eqs_to_solve = list(dyn_eqs_at_1.values())

    if verbose:
        print(f"\n  Algebraic equations (at t = 1):")
        for name, eq in dyn_eqs_at_1.items():
            print(f"    E_{name}|_{{t=1}} :  {eq}  =  0")

    solutions_raw = sp.solve(eqs_to_solve, unknowns, dict=True)

    # ── Verify each solution against the full t-dependent expression ──
    results = {
        'p_solutions': [],
        'A_relations': [],
        'constraint':  None,
        'verified':    [],
    }

    if not solutions_raw:
        if verbose:
            print(f"\n  ⚠  No power-law solutions found")

        # Still try to extract if there's only one equation:
        # factorise in p symbolically
        if len(eqs_to_solve) == 1:
            eq0 = eqs_to_solve[0]
            # Try to factor out A
            try:
                eq_over_A = sp.cancel(eq0 / A_sym**2)
                p_sols = sp.solve(eq_over_A, p_sym)
                if p_sols:
                    solutions_raw = [{p_sym: pv} for pv in p_sols]
            except Exception:
                pass

    if verbose and solutions_raw:
        print(f"\n  Found {len(solutions_raw)} candidate solution(s)")

    for i, sol in enumerate(solutions_raw):
        p_val = sol.get(p_sym, p_sym)
        q_val = sol.get(q_sym, q_sym) if has_phi else None

        # Verify: substitute back into full expression, simplify
        verified = True
        for eom_name, eq_full in dyn_eqs_full.items():
            check = eq_full.subs(p_sym, p_val)
            if has_phi and q_val is not None:
                check = check.subs(q_sym, q_val)
            check = _simp(check)
            if check != 0:
                # Might be zero after factoring out t^something
                check = sp.powsimp(check)
                # Try dividing by t^(any power)
                if check.has(t_s):
                    # Extract coefficient: check = c(A,...) * t^e
                    as_pow = check.as_coeff_exponent(t_s)
                    if _simp(as_pow[0]) == 0:
                        check = sp.Integer(0)
                if check != 0:
                    verified = False

        sol_info = {'p': p_val}
        if has_phi:
            sol_info['q'] = q_val
        sol_info['verified'] = verified

        results['p_solutions'].append(sol_info)
        results['verified'].append(verified)

        if verbose:
            tag = "✓ verified" if verified else "⚠ unverified"
            line = f"    [{i+1}]  p = {p_val}"
            if has_phi:
                line += f",  q = {q_val}"
            line += f"    ({tag})"
            print(line)

    # ── Constraint from E_N on the ansatz ──
    if 'N' in eom_gauged:
        eq_N = eom_gauged['N']
        eq_N = eq_N.replace(_a_cls, a_ansatz)
        if has_phi:
            eq_N = eq_N.replace(_phi_cls, phi_ansatz)
        eq_N = eq_N.doit()
        con_at_1 = _simp(eq_N.subs(t_s, 1))
        results['constraint'] = con_at_1

        if verbose:
            print(f"\n  Constraint E_N|_{{t=1}} :  {con_at_1}  =  0")
            # Substitute each p solution
            for i, sol_info in enumerate(results['p_solutions']):
                con_sub = con_at_1.subs(p_sym, sol_info['p'])
                if has_phi and 'q' in sol_info:
                    con_sub = con_sub.subs(q_sym, sol_info['q'])
                con_sub = _simp(con_sub)
                print(f"    at p={sol_info['p']} :  {con_sub}  =  0")

    return results


# ── C. Exponential (de Sitter) ansatz ──────────────────────────

def ansatz_exponential(
    eom_gauged: Dict[str, sp.Expr],
    t_s:        sp.Symbol = t_sym,
    verbose:    bool      = True,
) -> Dict[str, Any]:
    """
    Substitute  a(t) = a₀ · exp(H·t)  [and  φ(t) = φ₀ + v_φ · t]
    into the EOM.  Solve for H (Hubble rate) and v_φ (rolling speed).

    This detects de Sitter solutions (exponential expansion).

    Returns
    -------
    dict with keys:
      'H_solutions'     : solutions for H
      'constraint'      : E_N on the ansatz
    """

    a_t   = _a_cls(t_s)
    phi_t = _phi_cls(t_s)

    has_a   = 'a'   in eom_gauged
    has_phi = 'phi' in eom_gauged

    # Ansatz symbols
    a0_sym = sp.Symbol('a_0', positive=True)
    H_sym  = sp.Symbol('H', real=True)
    a_exp  = sp.Lambda(t_s, a0_sym * sp.exp(H_sym * t_s))

    phi0_sym = sp.Symbol('phi_0')
    vphi_sym = sp.Symbol('v_phi', real=True)
    phi_lin  = sp.Lambda(t_s, phi0_sym + vphi_sym * t_s)

    if verbose:
        print(f"\n{'═' * 60}")
        print(f"  Exponential ansatz :  a(t) = a₀·exp(H·t)"
              + ("  ,  φ(t) = φ₀ + v_φ·t" if has_phi else ""))
        print(f"{'═' * 60}")

    # ── Substitute into each dynamical EOM ──
    dyn_results = {}
    for eom_name in ['a', 'phi']:
        if eom_name not in eom_gauged:
            continue
        eq = eom_gauged[eom_name]
        eq = eq.replace(_a_cls, a_exp)
        if has_phi:
            eq = eq.replace(_phi_cls, phi_lin)
        eq = eq.doit()
        eq = _simp(eq)

        # At t = 0: exp(H·0) = 1, so all exponentials vanish cleanly
        # and we get a pure algebraic equation in (H, a₀, v_φ, params).
        # This is valid because the original expression is
        #   f(H, a₀, …) · exp(k·H·t)  =  0
        # and  exp(k·H·t) > 0  ∀t,  so  f = 0  is the real condition.
        eq_alg = _simp(eq.subs(t_s, 0))

        dyn_results[eom_name] = eq_alg

    if verbose:
        print(f"\n  Reduced equations (exponentials cancelled):")
        for name, eq in dyn_results.items():
            print(f"    E_{name} :  {eq}  =  0")

    # ── Solve for H [and v_φ] ──
    unknowns = [H_sym]
    if has_phi:
        unknowns.append(vphi_sym)

    eqs_list = list(dyn_results.values())
    solutions = sp.solve(eqs_list, unknowns, dict=True)

    results = {
        'H_solutions': [],
        'constraint':  None,
    }

    if not solutions:
        # Try solving for H alone from E_a
        if 'a' in dyn_results:
            h_sols = sp.solve(dyn_results['a'], H_sym)
            if h_sols:
                solutions = [{H_sym: hs} for hs in h_sols]

    if verbose:
        if solutions:
            print(f"\n  Found {len(solutions)} solution(s):")
            for i, sol in enumerate(solutions):
                parts = [f"H = {sol.get(H_sym, '?')}"]
                if has_phi and vphi_sym in sol:
                    parts.append(f"v_φ = {sol[vphi_sym]}")
                print(f"    [{i+1}]  {',  '.join(parts)}")

                results['H_solutions'].append(sol)
        else:
            print(f"\n  ⚠  No exponential (de Sitter) solutions found")

    # ── Constraint from E_N ──
    if 'N' in eom_gauged:
        eq_N = eom_gauged['N']
        eq_N = eq_N.replace(_a_cls, a_exp)
        if has_phi:
            eq_N = eq_N.replace(_phi_cls, phi_lin)
        eq_N = eq_N.doit()
        eq_N_alg = _simp(eq_N.subs(t_s, 0))

        results['constraint'] = eq_N_alg

        if verbose:
            print(f"\n  Constraint E_N|_{{t=0}} :  {eq_N_alg}  =  0")
            for i, sol in enumerate(results['H_solutions']):
                con_sub = eq_N_alg
                for sym, val in sol.items():
                    con_sub = con_sub.subs(sym, val)
                con_sub = _simp(con_sub)
                print(f"    at H={sol.get(H_sym,'?')} :  {con_sub}  =  0")

    return results


# ── D. Unified analytical driver ───────────────────────────────

def analytical_solve(
    eom_gauged: Dict[str, sp.Expr],
    t_s:        sp.Symbol = t_sym,
    skip_dsolve: bool     = True,
    verbose:    bool      = True,
) -> Dict[str, Any]:
    """
    Run all analytical solvers and collect results.

    Parameters
    ----------
    skip_dsolve : bool
        If True (default), skip sympy dsolve — it rarely succeeds
        for nonlinear ODE and can hang for minutes.

    Returns dict with keys:
      'power_law'   : result of ansatz_power_law
      'exponential' : result of ansatz_exponential
      'dsolve'      : result of symbolic_dsolve  (if not skipped)
    """
    results = {}

    # 1. Power-law (most robust for FLRW)
    results['power_law'] = ansatz_power_law(eom_gauged, t_s, verbose)

    # 2. Exponential / de Sitter
    results['exponential'] = ansatz_exponential(eom_gauged, t_s, verbose)

    # 3. dsolve (slow, usually fails for nonlinear ODE)
    if skip_dsolve:
        if verbose:
            print(f"\n  (dsolve skipped — set skip_dsolve=False to enable)")
        results['dsolve'] = {'skipped': True}
    else:
        if verbose:
            print(f"\n  (dsolve may take a while for nonlinear ODE ...)")
        try:
            results['dsolve'] = symbolic_dsolve(eom_gauged, t_s, verbose)
        except Exception as e:
            results['dsolve'] = {'error': str(e)}
            if verbose:
                print(f"  dsolve raised: {e}")

    return results


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
        rhs[name] = _simp(expr)

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

    # ── Check Friedmann constraint at ICs ──
    if 'N' in eom_gauged:
        eq_N = eom_gauged['N']
        # Substitute parameters
        for p_key, val in param_vals.items():
            pk = sp.Symbol(p_key) if isinstance(p_key, str) else p_key
            eq_N = eq_N.subs(pk, val)
        # Substitute ICs: a(t₀)=a₀, ȧ(t₀)=v₀, etc.
        eq_N_ic = eq_N
        if has_a:
            eq_N_ic = eq_N_ic.subs(sp.Derivative(a_t, (t_s, 2)),
                                    rhs_exprs['a'])  # ä from RHS
            eq_N_ic = eq_N_ic.subs(sp.Derivative(a_t, t_s), y0[1])
            eq_N_ic = eq_N_ic.subs(a_t, y0[0])
        if has_phi:
            pi = 2 if has_a else 0
            if 'phi' in rhs_exprs:
                eq_N_ic = eq_N_ic.subs(sp.Derivative(phi_t, (t_s, 2)),
                                        rhs_exprs['phi'])
            eq_N_ic = eq_N_ic.subs(sp.Derivative(phi_t, t_s), y0[pi+1])
            eq_N_ic = eq_N_ic.subs(phi_t, y0[pi])
        # Substitute remaining parameters in ä expression
        for p_key, val in param_vals.items():
            pk = sp.Symbol(p_key) if isinstance(p_key, str) else p_key
            eq_N_ic = eq_N_ic.subs(pk, val)
        eq_N_ic = eq_N_ic.subs(t_s, t_span[0])
        try:
            residual = float(eq_N_ic)
            if verbose:
                if abs(residual) < 1e-10:
                    print(f"\n    ✓  Friedmann constraint satisfied:  |E_N| = {abs(residual):.2e}")
                else:
                    print(f"\n    ⚠  Friedmann constraint VIOLATED:  E_N = {residual:.6e}")
                    print(f"       The ICs do not lie on the constraint surface.")
                    print(f"       Solution will drift off the physical manifold.")
        except (TypeError, ValueError):
            if verbose:
                print(f"\n    (could not evaluate E_N at ICs — free symbols remain)")

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
        eq_N = _simp(eq_N)

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
    coeffs, constraint, series, constrained = power_series_solve(eom_gr, t, order=8)

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
    coeffs_d, constraint_d, series_d, constrained_d = power_series_solve(eom_dust, t, order=8)

    # Constraint: 3 M_p^2 a_0 a_1^2 - ρ_{m,0} = 0
    expected_d = 3 * M_p**2 * a_0 * a_1**2 - rho_m0
    assert sp.simplify(constraint_d - expected_d) == 0, \
        f"FAIL: {constraint_d} ≠ {expected_d}"
    print(f"\n  ✓  Constraint: 3 M_p² a_0 a_1² = ρ_{{m,0}}")

    # Verify constrained series eliminates a_1
    assert constrained_d is not None, "FAIL: constraint enforcement returned None"
    ic_sub = constrained_d['ic_subs']
    assert a_1 in ic_sub, f"FAIL: a_1 not eliminated, ic_subs = {ic_sub}"
    # a_1 should be sqrt(ρ/(3 M_p² a_0))
    a1_val = ic_sub[a_1]
    # Verify: substituting back into constraint gives 0
    check = constraint_d.subs(a_1, a1_val)
    assert sp.simplify(check) == 0, f"FAIL: constraint not satisfied: {check}"
    print(f"  ✓  Constrained: a_1 = {a1_val}")
    print(f"  ✓  Constrained series has a_0 as sole free IC")

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

    # ── Test 5: power-law ansatz (GR) ──
    print(f"\n{'─' * 60}")
    print("  Test 5 : Power-law ansatz (vacuum GR)")
    print(f"{'─' * 60}")
    pl_result = ansatz_power_law(eom_gr, t)
    p_vals = [s['p'] for s in pl_result['p_solutions']]
    # GR vacuum:  3 M_p² A² p (3p - 2) = 0  →  p = 0 or p = 2/3
    assert sp.Rational(2, 3) in p_vals or any(
        _simp(pv - sp.Rational(2, 3)) == 0 for pv in p_vals
    ), f"FAIL: p = 2/3 not found, got {p_vals}"
    print(f"  ✓  Found p = 2/3 (matter-dominated)")

    # ── Test 6: exponential ansatz (GR) ──
    print(f"\n{'─' * 60}")
    print("  Test 6 : Exponential ansatz (vacuum GR)")
    print(f"{'─' * 60}")
    exp_result = ansatz_exponential(eom_gr, t)
    # Vacuum GR has no de Sitter solution ⟹ only H = 0
    H_sym_test = sp.Symbol('H', real=True)
    h_vals = [s.get(H_sym_test, None) for s in exp_result['H_solutions']]
    assert 0 in h_vals or any(
        v is not None and _simp(v) == 0 for v in h_vals
    ), f"FAIL: H = 0 not found, got {h_vals}"
    print(f"  ✓  Only H = 0 (no de Sitter in vacuum GR, as expected)")

    # ── Test 7: dsolve (GR) ──
    print(f"\n{'─' * 60}")
    print("  Test 7 : Symbolic dsolve (vacuum GR)")
    print(f"{'─' * 60}")
    ds_result = symbolic_dsolve(eom_gr, t)
    if 'a' in ds_result and not isinstance(ds_result['a'], str):
        print(f"  ✓  dsolve returned: {ds_result['a']}")
    else:
        print(f"  (dsolve could not find closed form — expected for nonlinear ODE)")

    # ── Test 8: Padé approximant ──
    print(f"\n{'─' * 60}")
    print("  Test 8 : Padé approximant (vacuum GR)")
    print(f"{'─' * 60}")
    # Use the series from Test 1
    P, Q = pade_approximant(series['a'], t, verbose=True)
    # With vacuum constraint a_1=0, Padé should give a_0/1 = a_0
    P0 = P.subs(a_1, 0)
    Q0 = Q.subs(a_1, 0)
    ratio = _simp(P0 / Q0)
    assert sp.simplify(ratio - a_0) == 0, f"FAIL: Padé|_{{a1=0}} = {ratio}"
    print(f"  ✓  Padé([{sp.degree(sp.Poly(P,t))}/{sp.degree(sp.Poly(Q,t))}]) "
          f"with a_1=0 → a_0")

    # ── Test 9: e-folds solver (GR) ──
    print(f"\n{'─' * 60}")
    print("  Test 9 : e-folds solver  H(x)  (vacuum GR)")
    print(f"{'─' * 60}")
    ef_coeffs, ef_con, ef_series = efolds_solve(eom_gr, t, order=6)
    # GR vacuum: E_a → 2H' + 3H = 0 → H' = -3H/2
    # → H_1 = -3 H_0 / 2
    H_0 = sp.Symbol('H_0')
    H_1 = sp.Symbol('H_1')
    if H_1 in ef_coeffs:
        expected_H1 = sp.Rational(-3, 2) * H_0
        assert sp.simplify(ef_coeffs[H_1] - expected_H1) == 0, \
            f"FAIL: H_1 = {ef_coeffs[H_1]}, expected {expected_H1}"
        print(f"  ✓  H_1 = -3H_0/2  (matter-dominated Hubble law)")

    print(f"\n{'═' * 60}")
    print("  All self-tests passed.")
    print(f"{'═' * 60}\n")


# ════════════════════════════════════════════════════════════════
#  SECTION 7 :  Main — load v1.7 results and solve
# ════════════════════════════════════════════════════════════════

def _solve_one(args):
    """Worker function for multiprocessing: solve one Lagrangian."""
    result, series_order, skip_dsolve = args
    import io, sys

    idx     = result['index']
    L_data  = result.get('L_data', {})
    eom     = result.get('symbolic_gauged')
    n_terms = len(L_data.get('terms', []))

    # Capture stdout so it doesn't interleave
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf

    t0 = _time.time()

    print(f"\n{'━' * 60}")
    print(f"  Solving Lagrangian #{idx}  ({n_terms}-term)")
    print(f"{'━' * 60}")

    sol_record = {
        'index':   idx,
        'n_terms': n_terms,
        'L_data':  L_data,
    }

    try:
        # 1. Power series (vacuum)
        coeffs, con, series, constrained = power_series_solve(
            eom, order=series_order)
        sol_record['power_series'] = {
            'coeffs': coeffs, 'constraint': con,
            'series': series, 'constrained': constrained,
        }

        # 2. Padé (vacuum)
        if 'a' in series:
            try:
                P, Q = pade_approximant(series['a'], verbose=True)
                sol_record['pade'] = {'P': P, 'Q': Q}
            except Exception as e:
                sol_record['pade'] = {'error': str(e)}

        # 3. e-folds H(x)
        try:
            ef_coeffs, ef_con, ef_series = efolds_solve(
                eom, order=series_order)
            sol_record['efolds'] = {
                'coeffs': ef_coeffs, 'constraint': ef_con,
                'series': ef_series,
            }
        except Exception as e:
            sol_record['efolds'] = {'error': str(e)}

        # 4. Analytical (power-law, exponential, optionally dsolve)
        try:
            ana = analytical_solve(eom, skip_dsolve=skip_dsolve, verbose=True)
            sol_record['analytical'] = ana
        except Exception as e:
            sol_record['analytical'] = {'error': str(e)}

        # 5. With dust source
        eom_m = result.get('symbolic_gauged_matter')
        if eom_m and 'a' in eom_m:
            print(f"\n  ── With dust source ──")
            coeffs_m, con_m, series_m, con_m2 = power_series_solve(
                eom_m, order=series_order)
            sol_record['power_series_dust'] = {
                'coeffs': coeffs_m, 'constraint': con_m,
                'series': series_m, 'constrained': con_m2,
            }
            try:
                ef_c, ef_cn, ef_s = efolds_solve(eom_m, order=series_order)
                sol_record['efolds_dust'] = {
                    'coeffs': ef_c, 'constraint': ef_cn,
                    'series': ef_s,
                }
            except Exception:
                pass

        dt = _time.time() - t0
        print(f"\n  ── Lagrangian #{idx} done in {dt:.1f}s ──")

    except Exception as e:
        print(f"\n  ⚠  Lagrangian #{idx} failed: {type(e).__name__}: {e}")
        sol_record['error'] = str(e)

    sys.stdout = old_stdout
    return sol_record, buf.getvalue()


if __name__ == '__main__':
    import pickle, os, sys, datetime
    from multiprocessing import Pool, cpu_count
    import multiprocessing as _mp

    # macOS Python 3.8+ defaults to 'spawn' which re-imports modules;
    # 'fork' is faster and avoids re-import issues with sympy globals
    try:
        _mp.set_start_method('fork')
    except RuntimeError:
        pass  # already set

    _script_dir = os.path.dirname(os.path.abspath(__file__))

    # ── Output directory ──
    _out_dir = os.path.join(_script_dir, 'solver_results')
    os.makedirs(_out_dir, exist_ok=True)

    # ── Log file (tee stdout) ──
    _ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    _log_dir = os.path.join(_script_dir, 'log')
    os.makedirs(_log_dir, exist_ok=True)
    _log_path = os.path.join(_log_dir, f'solver_{_ts}.log')

    class _Tee:
        def __init__(self, *streams):
            self.streams = streams
        def write(self, data):
            for s in self.streams:
                s.write(data)
                s.flush()
        def flush(self):
            for s in self.streams:
                s.flush()

    _log_fh = open(_log_path, 'w', encoding='utf-8')
    sys.stdout = _Tee(sys.__stdout__, _log_fh)
    print(f"[Solver Log] Writing to: {_log_path}")

    # ── Run self-tests ──
    self_test()

    # ── Try loading v1.7 results ──
    pkl_candidates = [
        os.path.join(_script_dir, 'eom_results', 'eom_results.pkl'),
        os.path.join(_script_dir, 'eom_results.pkl'),
    ]
    pkl_path = None
    for p in pkl_candidates:
        if os.path.exists(p):
            pkl_path = p
            break

    if pkl_path is None:
        print(f"\n  No eom_results.pkl found.")
        print(f"  Searched:")
        for p in pkl_candidates:
            print(f"    {p}")
        print(f"\n  To generate it, run EOM_v1_7.py first:")
        print(f"       python EOM_v1_7.py")
        print(f"  Then re-run this solver:")
        print(f"       python eom_solver.py")
    else:
        print(f"\n{'═' * 60}")
        print(f"  Loading v1.7 results from: {pkl_path}")
        print(f"{'═' * 60}")

        with open(pkl_path, 'rb') as f:
            all_results = pickle.load(f)

        # ── Configuration ──
        MAX_TERMS    = 4     # only solve Lagrangians with ≤ this many terms
        SKIP_DSOLVE  = True  # skip slow dsolve (rarely works for nonlinear ODE)
        SERIES_ORDER = 6     # truncation order for power series / e-folds
        N_WORKERS    = 1     # parallel workers (1 = sequential, safest on macOS)
                             # set > 1 on Linux for speedup; macOS fork can deadlock

        print(f"\n  Config:  MAX_TERMS={MAX_TERMS}  ORDER={SERIES_ORDER}  "
              f"SKIP_DSOLVE={SKIP_DSOLVE}  WORKERS={N_WORKERS}")

        # ── Filter jobs ──
        jobs = []
        for result in all_results:
            if result.get('trivial'):
                continue
            eom = result.get('symbolic_gauged')
            if not eom or 'a' not in eom:
                continue
            n_terms = len(result.get('L_data', {}).get('terms', []))
            if n_terms > MAX_TERMS:
                continue
            jobs.append((result, SERIES_ORDER, SKIP_DSOLVE))

        print(f"  Jobs to solve: {len(jobs)}")

        # ── Solve ──
        t0_all = _time.time()
        all_solver_results = []

        if N_WORKERS > 1 and len(jobs) > 1:
            print(f"\n  ⚡ Launching {N_WORKERS} workers ...")
            with Pool(N_WORKERS) as pool:
                raw_results = pool.map(_solve_one, jobs)
            for sol_record, captured_output in raw_results:
                print(captured_output, end='')
                all_solver_results.append(sol_record)
        else:
            # Sequential: print each Lagrangian's output live
            for j in jobs:
                sol_record, captured_output = _solve_one(j)
                print(captured_output, end='')
                sys.stdout.flush()
                all_solver_results.append(sol_record)

        dt_all = _time.time() - t0_all

        print(f"\n  Total solving time: {dt_all:.1f}s  "
              f"({dt_all/max(len(jobs),1):.1f}s per Lagrangian)")

        # ── Processing summary ──
        n_total   = len(all_results)
        n_triv    = sum(1 for r in all_results if r.get('trivial'))
        n_skipped = sum(1 for r in all_results
                        if not r.get('trivial')
                        and len(r.get('L_data', {}).get('terms', [])) > MAX_TERMS)
        n_solved  = len(all_solver_results)
        print(f"\n{'═' * 60}")
        print(f"  Processing summary")
        print(f"{'═' * 60}")
        print(f"    Total EOM results   : {n_total}")
        print(f"    Trivial (all zero)  : {n_triv}")
        print(f"    Skipped (>{MAX_TERMS} terms) : {n_skipped}")
        print(f"    Solved              : {n_solved}")

        # ── Write summary text file ──
        summary_path = os.path.join(_out_dir, 'solver_summary.txt')
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"EOM Solver Results  ({_ts})\n")
            f.write(f"{'=' * 70}\n")
            f.write(f"Config:  MAX_TERMS={MAX_TERMS}  ORDER={SERIES_ORDER}  "
                    f"TIMEOUT={TIMEOUT_SEC}s\n")
            f.write(f"Solved: {n_solved}  Skipped: {n_skipped}  "
                    f"Trivial: {n_triv}  Total: {n_total}\n")
            f.write(f"{'=' * 70}\n\n")

            for r in all_solver_results:
                idx = r['index']
                L = r.get('L_data', {})
                f.write(f"{'━' * 70}\n")
                f.write(f"Lagrangian #{idx}\n")
                if L:
                    f.write(f"  General: {L.get('general_form', '?')}\n")
                f.write(f"{'━' * 70}\n\n")

                # Power series
                ps = r.get('power_series', {})
                if ps.get('series'):
                    f.write(f"  ── Power series (vacuum) ──\n")
                    for name, expr in ps['series'].items():
                        f.write(f"    {name}(t) = {expr}\n")
                    if ps.get('constraint') is not None:
                        f.write(f"    Constraint: {ps['constraint']} = 0\n")
                    if ps.get('constrained'):
                        f.write(f"    IC elimination: {ps['constrained']['ic_subs']}\n")
                        for name, expr in ps['constrained']['series'].items():
                            f.write(f"    {name}(t)|_constr = {expr}\n")
                    f.write(f"\n")

                # Padé
                pd = r.get('pade', {})
                if 'P' in pd:
                    f.write(f"  ── Padé approximant (vacuum) ──\n")
                    f.write(f"    P(t) = {pd['P']}\n")
                    f.write(f"    Q(t) = {pd['Q']}\n")
                    f.write(f"    a(t) ≈ P(t) / Q(t)\n\n")

                # e-folds
                ef = r.get('efolds', {})
                if ef.get('series'):
                    f.write(f"  ── e-folds  H(x)  (vacuum) ──\n")
                    for name, expr in ef['series'].items():
                        if name == 'H_pade':
                            P_h, Q_h = expr
                            f.write(f"    H_padé(x) = [{P_h}] / [{Q_h}]\n")
                        else:
                            f.write(f"    {name}(N) = {expr}\n")
                    if ef.get('constraint') is not None:
                        f.write(f"    Constraint: {ef['constraint']} = 0\n")
                    f.write(f"\n")

                # Analytical
                ana = r.get('analytical', {})
                if not isinstance(ana, dict) or 'error' not in ana:
                    pl = ana.get('power_law', {})
                    if pl.get('p_solutions'):
                        f.write(f"  ── Power-law ansatz ──\n")
                        for s in pl['p_solutions']:
                            v = "✓" if s.get('verified') else "?"
                            f.write(f"    p = {s['p']}  ({v})\n")
                        f.write(f"\n")

                    exp_r = ana.get('exponential', {})
                    if exp_r.get('H_solutions'):
                        f.write(f"  ── Exponential ansatz ──\n")
                        for s in exp_r['H_solutions']:
                            H_sym_r = sp.Symbol('H', real=True)
                            f.write(f"    H = {s.get(H_sym_r, s)}\n")
                        f.write(f"\n")

                # Dust versions
                ps_d = r.get('power_series_dust', {})
                if ps_d.get('series'):
                    f.write(f"  ── Power series (+dust) ──\n")
                    for name, expr in ps_d['series'].items():
                        f.write(f"    {name}(t) = {expr}\n")
                    if ps_d.get('constraint') is not None:
                        f.write(f"    Constraint: {ps_d['constraint']} = 0\n")
                    if ps_d.get('constrained'):
                        f.write(f"    IC elimination: {ps_d['constrained']['ic_subs']}\n")
                        for name, expr in ps_d['constrained']['series'].items():
                            f.write(f"    {name}(t)|_constr = {expr}\n")
                    f.write(f"\n")

                ef_d = r.get('efolds_dust', {})
                if ef_d.get('series'):
                    f.write(f"  ── e-folds  H(x)  (+dust) ──\n")
                    for name, expr in ef_d['series'].items():
                        if name == 'H_pade':
                            continue
                        f.write(f"    {name}(N) = {expr}\n")
                    f.write(f"\n")

                f.write(f"\n")

        print(f"\n  Summary saved to: {summary_path}")

        # ── Save pickle ──
        pkl_out = os.path.join(_out_dir, 'solver_results.pkl')
        with open(pkl_out, 'wb') as f:
            pickle.dump(all_solver_results, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"  Pickle saved to:  {pkl_out}")

    # ── Close log ──
    sys.stdout = sys.__stdout__
    _log_fh.close()
    print(f"[Solver Log] Done. Log saved to: {_log_path}")