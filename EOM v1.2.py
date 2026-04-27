#!/usr/bin/env python3
"""
eom_ghost_free.py
=================
Compute equations of motion from FLRW minisuperspace Lagrangians with
symbolic (undetermined) Greek coefficients, then solve for ghost-free
coefficient values by requiring all EOM to be at most second-order.

Pipeline (per Lagrangian):
  1. Read L = sqrt(-g) * [α·f₁ + β·f₂ + ...] from grammar masker v1.4
  2. Compute Ostrogradsky EL equations  E_N, E_a, E_φ
  3. Output raw EOM
  4. Identify terms with derivative order > 2
  5. Extract linear constraints on Greek coefficients by requiring
     those terms to vanish for ALL field configurations
  6. Solve the linear system → some coefficients determined, some free
  7. Assign log-uniform random values to free parameters
  8. Substitute, verify EOM ≤ 2nd order, gauge-fix N=1, output

Usage:
  Place this file alongside GR_grammar_masker_v1_4.py, then:
    python eom_ghost_free.py

  Or import and call process_lagrangian() directly.
"""

import sympy as sp
import sys
import os
import random
import time as _time
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

# ════════════════════════════════════════════════════════════════
#  Logging
# ════════════════════════════════════════════════════════════════

_log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')
os.makedirs(_log_dir, exist_ok=True)
_log_path = os.path.join(_log_dir, 'eom_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.log')
_log_fh = open(_log_path, 'w', encoding='utf-8')

class _Tee:
    def __init__(self, *streams):
        self.streams = streams
    def write(self, data):
        for s in self.streams:
            s.write(data)
    def flush(self):
        for s in self.streams:
            s.flush()

sys.stdout = _Tee(sys.__stdout__, _log_fh)
print(f"[EOM Log] Writing to: {_log_path}\n")

# ════════════════════════════════════════════════════════════════
#  Readable printer (same as v1.4 for consistent output)
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
#  SECTION 1 :  Ostrogradsky Euler–Lagrange Engine
# ════════════════════════════════════════════════════════════════
#
#  For a Lagrangian L(q, q', q'', ..., q^{(K)}), the higher-order
#  (Ostrogradsky) EL equation is:
#
#      E_q[L]  =  Σ_{k=0}^{K}  (-1)^k  (d/dt)^k  [∂L/∂q^{(k)}]
#
#  SymPy cannot directly differentiate w.r.t. Derivative(a(t),t),
#  so we temporarily replace  a(t), a'(t), a''(t), ...  with
#  independent dummy symbols, compute partial derivatives, then
#  restore function notation before applying d/dt.
# ════════════════════════════════════════════════════════════════

t_sym = sp.Symbol('t', real=True)

# Function *classes* (not instances) — used to match/replace in expressions
_N_cls   = sp.Function('N', positive=True)
_a_cls   = sp.Function('a', positive=True)
_phi_cls = sp.Function('phi')

DYN_FUNCS = [_N_cls, _a_cls, _phi_cls]
DYN_NAMES = ['N', 'a', 'phi']

# Greek coefficient symbols (must match v1.4 exactly)
_GREEK_COEFFS = [sp.Symbol(g) for g in
    [r'\alpha', r'\beta', r'\gamma', r'\delta',
     r'\epsilon', r'\zeta', r'\eta', r'\theta']]


def detect_max_order(expr, q_func, t_s=t_sym, max_scan=12):
    """Return the highest derivative order of q(t) appearing in expr, or -1."""
    q_t = q_func(t_s)
    for k in range(max_scan, -1, -1):
        target = q_t if k == 0 else sp.Derivative(q_t, (t_s, k))
        if expr.has(target):
            return k
    return -1


def euler_lagrange(L, q_func, t_s=t_sym, max_order=None):
    """
    Compute the Ostrogradsky EL equation for L w.r.t. q.
    Returns an expression E such that E = 0 is the field equation.
    """
    if max_order is None:
        max_order = detect_max_order(L, q_func, t_s)
    if max_order < 0:
        return sp.Integer(0)

    q_t = q_func(t_s)

    # ── Build dummy symbols ──
    dummies = []
    fwd = {}        # Derivative → dummy
    rev = {}        # dummy → Derivative
    for k in range(max_order + 1):
        s = sp.Symbol(f'__{q_func.name}_{k}__')
        dummies.append(s)
        key = q_t if k == 0 else sp.Derivative(q_t, (t_s, k))
        fwd[key] = s
        rev[s]   = key

    # ── Substitute highest order first ──
    L_d = L
    for k in range(max_order, -1, -1):
        key = q_t if k == 0 else sp.Derivative(q_t, (t_s, k))
        L_d = L_d.subs(key, dummies[k])

    # ── Compute each term of the EL sum ──
    EL = sp.Integer(0)
    for k in range(max_order + 1):
        # ∂L/∂q^{(k)} in dummy space
        partial = sp.diff(L_d, dummies[k])
        if partial == 0:
            continue

        # Restore function notation
        partial_r = partial
        for s, original in rev.items():
            partial_r = partial_r.subs(s, original)

        # Apply (-1)^k · (d/dt)^k, simplifying after each step
        term = partial_r
        for _i in range(k):
            term = sp.diff(term, t_s)
            term = sp.cancel(term)          # faster than simplify, avoids blowup

        EL += ((-1) ** k) * term

    return sp.cancel(EL)


def compute_all_eom(L, t_s=t_sym):
    """
    Compute EOM for each dynamical variable (N, a, φ).
    Returns dict  {name: EOM expression}.
    """
    eoms = {}
    for name, func in zip(DYN_NAMES, DYN_FUNCS):
        order = detect_max_order(L, func, t_s)
        if order < 0:
            continue
        print(f"    E_{name}: max deriv order of {name} in L = {order}, computing EL ...")
        t0 = _time.time()
        eq = euler_lagrange(L, func, t_s, max_order=order)
        dt = _time.time() - t0
        if eq == 0:
            print(f"      → E_{name} = 0  (trivial, {dt:.1f}s)")
        else:
            eoms[name] = eq
            print(f"      → done  ({dt:.1f}s,  {sp.count_ops(eq)} ops)")
    return eoms


# ════════════════════════════════════════════════════════════════
#  SECTION 2 :  Ghost-constraint extraction & solving
# ════════════════════════════════════════════════════════════════
#
#  The EOM is *linear* in the Greek coefficients:
#
#      E_q  =  Σ_i  c_i · h_i(N, a, φ, derivatives)
#
#  where  h_i = ∂E_q/∂c_i  is fixed (no Greek symbols).
#
#  Ghost-freedom:  E_q must contain no derivative of order > 2.
#  For each high-order derivative D (e.g. a⁽⁴⁾), define
#
#      f_{i,D}  =  coeff of D in h_i        (a function of lower-order vars)
#
#  Constraint:  Σ_i  c_i · f_{i,D}  ≡  0   for ALL field configurations.
#
#  Since the f_{i,D} are generically independent functions of (a, ȧ, ä, N, …),
#  we evaluate at random test profiles to get a numerical homogeneous linear
#  system   A · c = 0   and solve for the null space.
# ════════════════════════════════════════════════════════════════

def find_high_order_derivs(expr, t_s=t_sym, max_allowed=2, max_scan=12):
    """Return [(func_name, order, Derivative)] for all derivs of order > max_allowed."""
    result = []
    for func in DYN_FUNCS:
        q_t = func(t_s)
        for k in range(max_scan, max_allowed, -1):
            dk = sp.Derivative(q_t, (t_s, k))
            if expr.has(dk):
                result.append((func.name, k, dk))
    return result


def _make_test_profile(coeffs_N, coeffs_a, coeffs_phi, t_s=t_sym):
    """Build a test profile from polynomial coefficient lists."""
    def _poly(cs):
        return sum(sp.Rational(c, 1) * t_s**k for k, c in enumerate(cs))
    return {
        _N_cls:   sp.Lambda(t_s, _poly(coeffs_N)),
        _a_cls:   sp.Lambda(t_s, _poly(coeffs_a)),
        _phi_cls: sp.Lambda(t_s, _poly(coeffs_phi)),
    }


def _eval_at_profile(expr, profile, t_val, t_s=t_sym, extra_subs=None):
    """Replace function classes with Lambda test profiles, .doit(), eval at t_val."""
    e = expr
    for func_cls, lam in profile.items():
        e = e.replace(func_cls, lam)
    e = e.doit()
    if extra_subs:
        e = e.subs(extra_subs)
    return e.subs(t_s, t_val)


def extract_and_solve_ghost_constraints(
        eom_dict:     Dict[str, sp.Expr],
        greek_syms:   List[sp.Symbol],
        t_s:          sp.Symbol = t_sym,
        max_allowed:  int       = 2,
        seed:         int       = 42,
) -> Tuple[Dict[sp.Symbol, Any], List[sp.Symbol], bool]:
    """
    Analyse the EOM for ghost terms and solve for ghost-free coefficients.

    Returns
    -------
    full_solution : {greek_symbol: numerical_value}
    free_params   : list of unconstrained greek symbols
    is_trivial    : True ⟹ only solution is all-zero (no valid Lagrangian)
    """

    # ── 1. Catalogue every high-order derivative across all EOMs ──
    all_high = set()
    for name, eom in eom_dict.items():
        for info in find_high_order_derivs(eom, t_s, max_allowed):
            all_high.add(info)          # (func_name, order, Derivative)

    if not all_high:
        print("    ✓ No derivatives of order > 2 — already ghost-free")
        random.seed(seed)
        sol = {}
        for g in greek_syms:
            sol[g] = random.choice([-1, 1]) * 10 ** random.uniform(-5, 5)
        return sol, list(greek_syms), False

    print("    High-order derivatives detected:")
    for vn, order, _ in sorted(all_high):
        print(f"      {vn}^({order})")

    # ── 2. Decompose each EOM by Greek coefficient ──
    #    h_i[eom_name]  =  ∂E_{eom_name}/∂c_i
    per_greek = {}
    for g in greek_syms:
        per_greek[g] = {}
        for name, eom in eom_dict.items():
            h = sp.diff(eom, g)
            if h != 0:
                per_greek[g][name] = h

    # ── 3. For every (EOM, high-order deriv), extract coeff of D in each h_i ──
    #       Then evaluate at test profiles → numerical linear constraints.
    #
    #  Use degree-9 polynomial profiles so that derivatives up to 9th order
    #  are non-zero, guaranteeing that f_{i,D} ≢ 0 evaluates to non-zero.

    primes = [2,3,5,7,11,13,17,19,23,29,  31,37,41,43,47,53,59,61,67,71,
              73,79,83,89,97,101,103,107,109,113]
    profiles = [
        _make_test_profile(primes[0:10],  primes[10:20], primes[20:30], t_s),
        _make_test_profile(primes[5:15],  primes[15:25], primes[2:12],  t_s),
    ]
    t_vals = [sp.Rational(1, 10), sp.Rational(3, 17)]

    extra_subs = {sp.Symbol('M_p', positive=True): 1,
                  sp.Symbol('m', positive=True): 1}

    numerical_constraints = []

    for eom_name, eom in eom_dict.items():
        for (vn, order, dk) in sorted(all_high):
            if not eom.has(dk):
                continue

            # For each Greek symbol, extract coeff of dk in h_i
            dummy = sp.Symbol(f'_D{vn}{order}_')
            coeff_map = {}                          # greek → f_{i,D}
            for g in greek_syms:
                if eom_name not in per_greek[g]:
                    continue
                h_i = per_greek[g][eom_name]
                if not h_i.has(dk):
                    continue
                h_sub = h_i.subs(dk, dummy)
                f_iD  = sp.expand(h_sub).coeff(dummy)
                if f_iD != 0:
                    coeff_map[g] = f_iD

            if not coeff_map:
                continue

            # Evaluate at each (profile, t_val) → one numerical constraint
            for profile in profiles:
                for tv in t_vals:
                    constraint = sp.Integer(0)
                    ok = True
                    for g, f_iD in coeff_map.items():
                        f_num = _eval_at_profile(f_iD, profile, tv, t_s, extra_subs)
                        try:
                            f_float = float(f_num)
                        except (TypeError, ValueError):
                            ok = False
                            break
                        if abs(f_float) > 1e-15:
                            constraint += g * f_float
                    if ok and constraint != 0:
                        numerical_constraints.append(constraint)

    if not numerical_constraints:
        print("    ✓ All high-order-derivative coefficients vanish identically")
        random.seed(seed)
        sol = {}
        for g in greek_syms:
            sol[g] = random.choice([-1, 1]) * 10 ** random.uniform(-5, 5)
        return sol, list(greek_syms), False

    print(f"    → {len(numerical_constraints)} numerical constraints collected")

    # ── 4. Solve the homogeneous linear system ──
    #       numerical_constraints are expressions like  3.14·α − 2.71·β  = 0.

    solution_list = sp.solve(numerical_constraints, greek_syms, dict=True)

    if not solution_list:
        # No non-trivial null space → only solution is c = 0
        print("    ⚠  Only solution is all-zero — no ghost-free Lagrangian with these terms")
        return {g: sp.Integer(0) for g in greek_syms}, [], True

    sol_symbolic = solution_list[0]

    # ── 5. Identify free (unconstrained) parameters ──
    determined = set(sol_symbolic.keys())
    free_params = [g for g in greek_syms if g not in determined]

    print("    Symbolic solution:")
    for g, val in sol_symbolic.items():
        print(f"      {g}  =  {val}")
    if free_params:
        print(f"    Free parameters: {[str(g) for g in free_params]}")
    else:
        print("    (no free parameters — all determined)")

    # ── 6. Assign random values to free parameters ──
    random.seed(seed)
    free_vals = {}
    for g in free_params:
        free_vals[g] = random.choice([-1, 1]) * 10 ** random.uniform(-5, 5)

    # ── 7. Build full numerical solution ──
    full_solution = {}
    for g in greek_syms:
        if g in sol_symbolic:
            val = sol_symbolic[g]
            # val may involve other free greeks → substitute their random values
            for fp, fv in free_vals.items():
                if hasattr(val, 'subs'):
                    val = val.subs(fp, fv)
            # Also substitute any remaining dimensional symbols
            if hasattr(val, 'subs'):
                val = val.subs(extra_subs)
            full_solution[g] = float(val) if hasattr(val, '__float__') else val
        elif g in free_vals:
            full_solution[g] = free_vals[g]
        else:
            full_solution[g] = 0

    return full_solution, free_params, False


# ════════════════════════════════════════════════════════════════
#  SECTION 3 :  Post-processing — substitute, verify, gauge-fix
# ════════════════════════════════════════════════════════════════

def substitute_solution(eom_dict, solution, t_s=t_sym):
    """Substitute numerical coefficient values into EOM and simplify."""
    final = {}
    for name, eom in eom_dict.items():
        e = eom
        for g, val in solution.items():
            e = e.subs(g, val)
        # Also substitute M_p=1, m=1 for final form
        e = e.subs(sp.Symbol('M_p', positive=True), 1)
        e = e.subs(sp.Symbol('m', positive=True), 1)
        e = sp.simplify(e)
        final[name] = e
    return final


def verify_max_order(eom_dict, max_allowed=2, t_s=t_sym):
    """Check that no EOM contains derivatives of order > max_allowed."""
    all_clean = True
    for name, eom in eom_dict.items():
        highs = find_high_order_derivs(eom, t_s, max_allowed)
        if highs:
            all_clean = False
            print(f"    ⚠  E_{name} still contains:")
            for vn, order, _ in highs:
                print(f"         {vn}^({order})")
        else:
            max_orders = {}
            for func, fn in zip(DYN_FUNCS, DYN_NAMES):
                o = detect_max_order(eom, func, t_s)
                if o >= 0:
                    max_orders[fn] = o
            order_str = ", ".join(f"{fn}≤{o}" for fn, o in max_orders.items())
            print(f"    ✓  E_{name}  clean  ({order_str})")
    return all_clean


def gauge_fix_lapse(eom_dict, t_s=t_sym):
    """Set N(t)=1  (and all its derivatives to 0)  after variation."""
    N_t = _N_cls(t_s)
    fixed = {}
    for name, eom in eom_dict.items():
        e = eom
        # Replace derivatives highest-first
        for k in range(12, 0, -1):
            e = e.subs(sp.Derivative(N_t, (t_s, k)), 0)
        e = e.subs(N_t, 1)
        e = sp.simplify(e)
        fixed[name] = e
    return fixed


# ════════════════════════════════════════════════════════════════
#  SECTION 4 :  Main driver — process one Lagrangian end-to-end
# ════════════════════════════════════════════════════════════════

def process_lagrangian(L_data: dict, index: int, tex_fn=tex,
                       max_allowed: int = 2, seed: int = 42):
    """
    Full pipeline for a single Lagrangian from v1.4:
      raw EOM → ghost constraints → solve → verify → gauge-fix → output.

    Returns a result dict (or None if the Lagrangian is trivial).
    """
    print(f"\n{'═' * 70}")
    print(f"  LAGRANGIAN  #{index}")
    print(f"{'═' * 70}")
    print(f"  General:  {L_data['general']}")
    print(f"  FLRW:     {tex_fn(L_data['substituted'])}")
    print(f"  has_φ:    {L_data['has_phi']}")
    for i, tt in enumerate(L_data['terms']):
        print(f"    [{i+1}] {tt['coeff_symbol']:10s}  dim={tt['mass_dim']}  "
              f"Mp^{tt['mp_power']}  {tt['candidate']}")

    L = L_data['substituted']

    # Which Greek symbols are actually present in this Lagrangian?
    used = [g for g in _GREEK_COEFFS if L.has(g)]
    # Also check for fallback c_{i} symbols
    for tt in L_data['terms']:
        s = sp.Symbol(tt['coeff_symbol'])
        if s not in used and L.has(s):
            used.append(s)
    if not used:
        print("  (no symbolic coefficients — skipping)")
        return None

    print(f"\n  Coefficients: {[str(g) for g in used]}")

    # ─── Step 1: raw EOM ───
    print(f"\n  {'─'*60}")
    print(f"  Step 1 : Compute raw EOM via Ostrogradsky EL")
    print(f"  {'─'*60}")
    eoms = compute_all_eom(L, t_sym)
    if not eoms:
        print("    All EOM are trivially zero")
        return None

    print(f"\n  ── Raw EOM ──")
    for name, eq in eoms.items():
        print(f"\n  E_{name}  =")
        print(f"    {tex_fn(eq)}")
        for fn in DYN_NAMES:
            o = detect_max_order(eq, dict(zip(DYN_NAMES, DYN_FUNCS))[fn], t_sym)
            if o >= 0:
                print(f"    (max order of {fn} : {o})")

    # ─── Step 2: ghost-constraint analysis ───
    print(f"\n  {'─'*60}")
    print(f"  Step 2 : Ghost-free constraint analysis")
    print(f"  {'─'*60}")
    solution, free_params, is_trivial = extract_and_solve_ghost_constraints(
        eoms, used, t_sym, max_allowed=max_allowed, seed=seed)

    if is_trivial:
        print("\n  ⇒ This combination of terms has no ghost-free realisation.")
        return {'index': index, 'L_data': L_data, 'trivial': True}

    print(f"\n  ── Coefficient values ──")
    for g in used:
        val = solution[g]
        tag = " (free)" if g in free_params else " (determined)"
        if isinstance(val, float):
            print(f"    {g}  =  {val: .6e}{tag}")
        else:
            print(f"    {g}  =  {val}{tag}")

    # ─── Step 3: substitute & verify ───
    print(f"\n  {'─'*60}")
    print(f"  Step 3 : Substitute coefficients and verify")
    print(f"  {'─'*60}")
    final_eoms = substitute_solution(eoms, solution, t_sym)
    all_clean = verify_max_order(final_eoms, max_allowed, t_sym)

    if not all_clean:
        print("\n  ⚠  Ghost terms remain after substitution — attempting tighter solve")
        # Second pass: re-extract constraints from the *final* EOM
        # (this can happen if cross-terms between high-order derivatives
        #  were not fully captured by the first-round linear constraints)
        remaining_greeks = [g for g in used if isinstance(solution.get(g), sp.Basic)]
        if remaining_greeks:
            sol2, fp2, triv2 = extract_and_solve_ghost_constraints(
                eoms, remaining_greeks, t_sym, max_allowed, seed+1)
            solution.update(sol2)
            final_eoms = substitute_solution(eoms, solution, t_sym)
            all_clean = verify_max_order(final_eoms, max_allowed, t_sym)

    # ─── Step 4: gauge-fix N=1 ───
    print(f"\n  {'─'*60}")
    print(f"  Step 4 : Gauge-fix  N = 1")
    print(f"  {'─'*60}")
    gauged = gauge_fix_lapse(final_eoms, t_sym)

    print(f"\n  ── Final EOM  (N = 1 gauge) ──")
    for name, eq in gauged.items():
        print(f"\n  E_{name}  =")
        print(f"    {tex_fn(eq)}")
        for fn in DYN_NAMES:
            func = dict(zip(DYN_NAMES, DYN_FUNCS))[fn]
            o = detect_max_order(eq, func, t_sym)
            if o >= 0:
                print(f"    (max order of {fn} : {o})")

    return {
        'index':       index,
        'L_data':      L_data,
        'raw_eom':     eoms,
        'solution':    solution,
        'free_params': free_params,
        'final_eom':   final_eoms,
        'gauged_eom':  gauged,
        'is_clean':    all_clean,
        'trivial':     False,
    }


# ════════════════════════════════════════════════════════════════
#  SECTION 5 :  Self-test (run without v1.4)
# ════════════════════════════════════════════════════════════════

def self_test():
    """Quick sanity checks on known Lagrangians."""
    print("=" * 60)
    print("  SELF-TEST : Ostrogradsky EL on known Lagrangians")
    print("=" * 60)

    N_t   = _N_cls(t_sym)
    a_t   = _a_cls(t_sym)
    phi_t = _phi_cls(t_sym)

    # ── Test 1: L = ½ φ'²  →  E_φ = -φ'' = 0 ──
    print("\n── Test 1: L = ½ φ'² ──")
    L1 = sp.Rational(1, 2) * sp.Derivative(phi_t, t_sym) ** 2
    eq1 = euler_lagrange(L1, _phi_cls, t_sym)
    expected1 = -sp.Derivative(phi_t, (t_sym, 2))
    assert sp.simplify(eq1 - expected1) == 0, f"FAIL: {eq1}"
    print(f"  E_φ = {tex(eq1)}   ✓")

    # ── Test 2: L = ½ (φ'')²  →  E_φ = φ⁽⁴⁾ = 0 ──
    print("\n── Test 2: L = ½ (φ'')² ──")
    L2 = sp.Rational(1, 2) * sp.Derivative(phi_t, (t_sym, 2)) ** 2
    eq2 = euler_lagrange(L2, _phi_cls, t_sym)
    expected2 = sp.Derivative(phi_t, (t_sym, 4))
    assert sp.simplify(eq2 - expected2) == 0, f"FAIL: {eq2}"
    print(f"  E_φ = {tex(eq2)}   ✓")

    # ── Test 3: GR minisuperspace  L = -3 a ȧ²/N  ──
    print("\n── Test 3: L = -3 a ȧ²/N ──")
    L3 = -3 * a_t * sp.Derivative(a_t, t_sym) ** 2 / N_t
    eom3 = compute_all_eom(L3, t_sym)
    # E_N: variation w.r.t. N → Friedmann constraint
    # After N=1:  3 a ȧ² = 0  →  H² = 0
    g3 = gauge_fix_lapse(eom3, t_sym)
    print(f"  E_N(N=1) = {tex(g3.get('N', 0))}")
    print(f"  E_a(N=1) = {tex(g3.get('a', 0))}")
    verify_max_order(g3, max_allowed=2, t_s=t_sym)

    # ── Test 4: Ghost detection  L = α φ'² + β (φ'')² ──
    print("\n── Test 4: ghost constraint  L = α φ'² + β (φ'')² ──")
    alpha, beta = sp.Symbol(r'\alpha'), sp.Symbol(r'\beta')
    L4 = alpha * sp.Derivative(phi_t, t_sym) ** 2 + beta * sp.Derivative(phi_t, (t_sym, 2)) ** 2
    eom4 = compute_all_eom(L4, t_sym)
    sol4, free4, triv4 = extract_and_solve_ghost_constraints(
        eom4, [alpha, beta], t_sym, max_allowed=2, seed=99)
    print(f"  Solution: α={sol4[alpha]}, β={sol4[beta]}")
    # β must be 0 (ghost), α is free
    assert abs(float(sol4[beta])) < 1e-12, f"FAIL: β should be 0, got {sol4[beta]}"
    assert abs(float(sol4[alpha])) > 1e-12, f"FAIL: α should be free"
    final4 = substitute_solution(eom4, sol4, t_sym)
    verify_max_order(final4, 2, t_sym)
    print("  ✓  β = 0 (ghost removed), α free")

    print("\n" + "=" * 60)
    print("  All self-tests passed.")
    print("=" * 60 + "\n")


# ════════════════════════════════════════════════════════════════
#  SECTION 6 :  MAIN — read pickled Lagrangians, compute EOM
# ════════════════════════════════════════════════════════════════
#
#  Workflow:
#    1. Run  GR_grammar_masker_v1_4.py  once  →  produces lagrangians.pkl
#    2. Run  eom_ghost_free.py           (this file)  →  reads lagrangians.pkl
#
#  This avoids re-running the full tensor computation on every EOM run.

if __name__ == '__main__':
    import pickle

    # Run self-tests first
    self_test()

    # ── Locate and load pickle ──
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    pkl_path = os.path.join(_script_dir, 'lagrangians.pkl')

    if not os.path.exists(pkl_path):
        print("=" * 70)
        print("  ERROR: lagrangians.pkl not found")
        print(f"  Expected at: {pkl_path}")
        print()
        print("  Please run GR_grammar_masker_v1_4.py first to generate it:")
        print("    python GR_grammar_masker_v1_4.py")
        print("=" * 70)
        sys.stdout = sys.__stdout__
        _log_fh.close()
        sys.exit(1)

    print("=" * 70)
    print(f"  Loading Lagrangians from: {pkl_path}")
    print("=" * 70)

    t0_load = _time.time()
    with open(pkl_path, 'rb') as f:
        lagrangian_results = pickle.load(f)
    dt_load = _time.time() - t0_load

    total_count = sum(len(v) for v in lagrangian_results.values())
    print(f"  Loaded {total_count} Lagrangians in {dt_load:.2f}s")

    # Use our own printer (same format as v1.4)
    tex_fn = tex

    # ── Summary of available Lagrangians ──
    print(f"\n  Available Lagrangians:")
    for nt in sorted(lagrangian_results.keys()):
        print(f"    {nt}-term : {len(lagrangian_results[nt])} Lagrangians")

    # ── Process samples ──
    #  For each n_terms, process the first N_SAMPLES Lagrangians.
    #  EL computation is expensive for high-dimensional terms;
    #  adjust N_SAMPLES as needed.
    N_SAMPLES = 3

    all_results = []
    summary_lines = []

    for n_terms in sorted(lagrangian_results.keys()):
        lags = lagrangian_results[n_terms]
        if not lags:
            continue
        print(f"\n{'━' * 70}")
        print(f"  Processing {n_terms}-term Lagrangians  (first {min(N_SAMPLES, len(lags))})")
        print(f"{'━' * 70}")

        for i, L_data in enumerate(lags[:N_SAMPLES]):
            global_idx = sum(len(lagrangian_results.get(k, []))
                             for k in sorted(lagrangian_results.keys()) if k < n_terms) + i + 1
            result = process_lagrangian(L_data, global_idx, tex_fn,
                                        max_allowed=2, seed=42 + i)
            if result is not None:
                all_results.append(result)
                # One-line summary
                if result.get('trivial'):
                    summary_lines.append(
                        f"  #{global_idx:3d}  ({n_terms}-term)  TRIVIAL (all zero)")
                else:
                    n_free = len(result['free_params'])
                    n_det  = len([g for g in result['solution'] if g not in result['free_params']])
                    tag = "✓ CLEAN" if result['is_clean'] else "⚠ GHOST"
                    summary_lines.append(
                        f"  #{global_idx:3d}  ({n_terms}-term)  "
                        f"det={n_det}  free={n_free}  {tag}")

    # ── Final summary ──
    print(f"\n\n{'═' * 70}")
    print(f"  SUMMARY")
    print(f"{'═' * 70}")
    for line in summary_lines:
        print(line)
    print()

    n_clean   = sum(1 for r in all_results if r.get('is_clean'))
    n_trivial = sum(1 for r in all_results if r.get('trivial'))
    n_ghost   = sum(1 for r in all_results if not r.get('trivial') and not r.get('is_clean'))
    print(f"  Total processed : {len(all_results)}")
    print(f"  Ghost-free      : {n_clean}")
    print(f"  Trivial (all 0) : {n_trivial}")
    print(f"  Still has ghost : {n_ghost}")

    # ── Save results to file ──
    _out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eom_results')
    os.makedirs(_out_dir, exist_ok=True)
    out_path = os.path.join(_out_dir, 'eom_summary.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("EOM Ghost-Free Analysis Results\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        for r in all_results:
            idx = r['index']
            f.write(f"{'═' * 60}\n")
            f.write(f"Lagrangian #{idx}\n")

            # ── Lagrangian info ──
            L_data = r.get('L_data')
            if L_data:
                f.write(f"  General:     {L_data['general']}\n")
                f.write(f"  FLRW:        {tex_fn(L_data['substituted'])}\n")
                f.write(f"  has_phi:     {L_data['has_phi']}\n")
                f.write(f"  Terms:\n")
                for ti, tt in enumerate(L_data['terms']):
                    f.write(f"    [{ti+1}] {tt['coeff_symbol']:10s}  "
                            f"dim={tt['mass_dim']}  Mp^{tt['mp_power']}  "
                            f"{tt['candidate']}\n")

            if r.get('trivial'):
                f.write("  → TRIVIAL (all coefficients must be zero)\n\n")
                continue

            # ── Raw EOM (symbolic coefficients, before ghost removal) ──
            f.write(f"  Raw EOM (symbolic, before ghost removal):\n")
            for name, eq in r['raw_eom'].items():
                f.write(f"    E_{name} = {tex_fn(eq)}\n")
                for fn, fc in zip(DYN_NAMES, DYN_FUNCS):
                    o = detect_max_order(eq, fc, t_sym)
                    if o >= 0:
                        f.write(f"      max order of {fn}: {o}\n")

            # ── Solution ──
            f.write(f"  Ghost-free: {'YES' if r['is_clean'] else 'NO'}\n")
            f.write(f"  Coefficients:\n")
            for g, val in r['solution'].items():
                tag = "(free)" if g in r['free_params'] else "(determined)"
                if isinstance(val, float):
                    f.write(f"    {g} = {val: .6e}  {tag}\n")
                else:
                    f.write(f"    {g} = {val}  {tag}\n")

            # ── Final EOM ──
            f.write(f"  Final EOM (N=1 gauge):\n")
            for name, eq in r['gauged_eom'].items():
                f.write(f"    E_{name} = {tex_fn(eq)}\n")
            f.write("\n")
    print(f"\n  Results saved to: {out_path}")

    # ── Close log ──
    sys.stdout = sys.__stdout__
    _log_fh.close()
    print(f"[EOM Log] Done. Log saved to: {_log_path}")