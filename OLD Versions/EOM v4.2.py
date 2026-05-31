#!/usr/bin/env python3
"""
eom_ghost_free.py  (v5.0 — two scalar fields φ1, φ2)
=====================================================
Compute equations of motion from FLRW minisuperspace Lagrangians with
symbolic (undetermined) Greek coefficients, then solve for ghost-free
coefficient relations, keeping ALL remaining free parameters as symbols.

Now supports two scalar fields φ1(t), φ2(t) with independent masses
(m_1, m_2) and decay constants (f_1, f_2).  Potential types can be
quadratic (-½m²φ²) or axion (-m²f²(1-cos(φ/f))).

Pipeline (per Lagrangian):
  1. Read L from GR_grammar_masker_v3_0.py (via lagrangians.pkl)
  2. Compute Ostrogradsky EL equations  E_N, E_a, E_φ1, E_φ2
  3. Output raw EOM
  4. Identify terms with derivative order > 2
  5. Extract linear constraints on Greek coefficients by requiring
     those terms to vanish for ALL field configurations
  6. Solve the linear system → some coefficients determined, some free
  7. Substitute determined relations back into EOM
  8. Gauge-fix N=1, add dust source, output final symbolic EOM

Usage:
  Place this file alongside GR_grammar_masker_v3_0.py, then:
    python eom_ghost_free.py
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
#  Readable printer
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

def _simp(expr):
    """Fast simplify (cancel + powsimp, ~10-50x faster than sp.simplify)."""
    try:
        return sp.powsimp(sp.cancel(expr))
    except Exception:
        return sp.cancel(expr)


t_sym = sp.Symbol('t', real=True)

# Function *classes* — four dynamical variables: N, a, φ1, φ2
_N_cls    = sp.Function('N', positive=True)
_a_cls    = sp.Function('a', positive=True)
_phi1_cls = sp.Function('phi1')
_phi2_cls = sp.Function('phi2')

DYN_FUNCS = [_N_cls, _a_cls, _phi1_cls, _phi2_cls]
DYN_NAMES = ['N', 'a', 'phi1', 'phi2']

# Greek coefficient symbols (extended to 12 to match masker v3.0)
_GREEK_COEFFS = [sp.Symbol(g) for g in
    [r'\alpha', r'\beta', r'\gamma', r'\delta',
     r'\epsilon', r'\zeta', r'\eta', r'\theta',
     r'\iota', r'\kappa', r'\xi', r'\varpi']]

# Matter (dust) density — added to E_N as a source term after ghost analysis
rho_m0 = sp.Symbol('rho_{m,0}', positive=True)


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
    fwd = {}
    rev = {}
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
        partial = sp.diff(L_d, dummies[k])
        if partial == 0:
            continue

        # Restore function notation
        partial_r = partial
        for s, original in rev.items():
            partial_r = partial_r.subs(s, original)

        # Apply (-1)^k · (d/dt)^k
        term = partial_r
        for _i in range(k):
            term = sp.diff(term, t_s)
            term = sp.cancel(term)

        EL += ((-1) ** k) * term

    return sp.cancel(EL)


def compute_all_eom(L, t_s=t_sym):
    """
    Compute EOM for each dynamical variable (N, a, φ1, φ2).
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


def _make_test_profile(coeffs_N, coeffs_a, coeffs_phi1, coeffs_phi2, t_s=t_sym):
    """Build a test profile from polynomial coefficient lists."""
    def _poly(cs):
        return sum(sp.Rational(c, 1) * t_s**k for k, c in enumerate(cs))
    return {
        _N_cls:    sp.Lambda(t_s, _poly(coeffs_N)),
        _a_cls:    sp.Lambda(t_s, _poly(coeffs_a)),
        _phi1_cls: sp.Lambda(t_s, _poly(coeffs_phi1)),
        _phi2_cls: sp.Lambda(t_s, _poly(coeffs_phi2)),
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


def _first_primes(n: int) -> List[int]:
    """Return the first n prime numbers. Used only for generic test profiles."""
    primes = []
    x = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > x:
                break
            if x % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(x)
        x += 1
    return primes


def _generate_test_profiles(
        seed: int,
        t_s: sp.Symbol = t_sym,
        degree: int = 12,
        n_profiles: int = 4,
        n_t_vals: int = 4,
):
    """
    Generate deterministic but seed-dependent polynomial test profiles.

    Why this exists:
      - The ghost constraints are identities in N,a,phi1,phi2 and their derivatives.
      - We turn them into finite linear constraints on Greek coefficients by testing
        several generic polynomial backgrounds at several rational time values.
      - The profiles MUST change when the seed changes; otherwise retrying after a
        failed high-derivative check just repeats the same linear system.

    degree=12 matches find_high_order_derivs(..., max_scan=12), so derivatives up
    to the maximum scanned order are non-zero for generic profiles.
    """
    rng = random.Random(seed)

    # Enough small primes to build all coefficient lists with shuffle diversity.
    base_primes = _first_primes(max(200, 4 * n_profiles * (degree + 1) + 50))

    def _coeffs(positive: bool = True) -> List[int]:
        vals = []
        for _ in range(degree + 1):
            c = base_primes[rng.randrange(len(base_primes))]
            if not positive and rng.random() < 0.5:
                c = -c
            vals.append(c)
        return vals

    profiles = []
    for _ in range(n_profiles):
        # Keep N and a positive at positive t to avoid artificial zeros in denominators.
        coeffs_N = _coeffs(positive=True)
        coeffs_a = _coeffs(positive=True)
        # Scalar profiles can have signs; this makes cancellations less structured.
        coeffs_phi1 = _coeffs(positive=False)
        coeffs_phi2 = _coeffs(positive=False)
        profiles.append(_make_test_profile(
            coeffs_N, coeffs_a, coeffs_phi1, coeffs_phi2, t_s
        ))

    # Seed-dependent rational evaluation points. Keep them small and nonzero.
    t_vals = []
    while len(t_vals) < n_t_vals:
        num = rng.randint(1, 9)
        den = rng.randint(11, 47)
        tv = sp.Rational(num, den)
        if tv not in t_vals:
            t_vals.append(tv)

    return profiles, t_vals


def extract_and_solve_ghost_constraints(
        eom_dict:     Dict[str, sp.Expr],
        greek_syms:   List[sp.Symbol],
        t_s:          sp.Symbol = t_sym,
        max_allowed:  int       = 2,
        seed:         int       = 42,
) -> Tuple[Dict[sp.Symbol, Any], List[sp.Symbol], Dict[sp.Symbol, Any], bool]:
    """
    Analyse the EOM for ghost terms and solve for ghost-free coefficients.

    Returns
    -------
    full_solution : {greek_symbol: value}
    free_params   : list of unconstrained greek symbols
    extra_subs    : dimensional constant substitution dict
    is_trivial    : True ⟹ only solution is all-zero
    """

    extra_subs = {
        sp.Symbol('M_p', positive=True): 1,
        sp.Symbol(r'\Lambda', positive=True): 1,
        sp.Symbol('m_1', positive=True): 1,
        sp.Symbol('m_2', positive=True): 1,
        sp.Symbol('f_1', positive=True): 1,
        sp.Symbol('f_2', positive=True): 1,
    }

    # ── 1. Catalogue every high-order derivative across all EOMs ──
    all_high = set()
    for name, eom in eom_dict.items():
        for info in find_high_order_derivs(eom, t_s, max_allowed):
            all_high.add(info)

    if not all_high:
        print("    ✓ No derivatives of order > 2 — already ghost-free")
        sym_sol = {g: g for g in greek_syms}
        return sym_sol, list(greek_syms), extra_subs, False

    print("    High-order derivatives detected:")
    for vn, order, _ in sorted(all_high):
        print(f"      {vn}^({order})")

    # ── 2. Decompose each EOM by Greek coefficient ──
    per_greek = {}
    for g in greek_syms:
        per_greek[g] = {}
        for name, eom in eom_dict.items():
            h = sp.diff(eom, g)
            if h != 0:
                per_greek[g][name] = h

    # ── 3. For every (EOM, high-order deriv), extract coeff of D in each h_i ──
    # Use seed-dependent generic polynomial profiles. A retry with seed+... now
    # really changes the sampled backgrounds and time values.
    profiles, t_vals = _generate_test_profiles(
        seed=seed,
        t_s=t_s,
        degree=12,
        n_profiles=4,
        n_t_vals=4,
    )
    print(f"    Test profiles: seed={seed}, degree=12, "
          f"n_profiles={len(profiles)}, t_vals={[str(tv) for tv in t_vals]}")

    numerical_constraints = []

    for eom_name, eom in eom_dict.items():
        for (vn, order, dk) in sorted(all_high):
            if not eom.has(dk):
                continue

            dummy = sp.Symbol(f'_D{vn}{order}_')
            coeff_map = {}
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
        sym_sol = {g: g for g in greek_syms}
        return sym_sol, list(greek_syms), extra_subs, False

    print(f"    → {len(numerical_constraints)} numerical constraints collected")

    # ── 4. Solve the homogeneous linear system ──
    solution_list = sp.solve(numerical_constraints, greek_syms, dict=True)

    if not solution_list:
        print("    ⚠  Only solution is all-zero — no ghost-free Lagrangian with these terms")
        return {g: sp.Integer(0) for g in greek_syms}, [], {}, True

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

    # ── 6. Build symbolic solution ──
    symbolic_solution = {}
    for g in greek_syms:
        if g in sol_symbolic:
            symbolic_solution[g] = sol_symbolic[g]
        else:
            symbolic_solution[g] = g

    if not free_params:
        all_zero = all(
            v == 0 or v == sp.Integer(0)
            for v in symbolic_solution.values()
        )
        if all_zero:
            print("    ⚠  All coefficients are zero — no ghost-free Lagrangian with these terms")
            return symbolic_solution, free_params, {}, True

    return symbolic_solution, free_params, extra_subs, False


def assign_free_params(symbolic_solution, free_params, extra_subs=None, seed=42):
    """
    Assign random log-uniform values to free parameters and build a
    fully numerical solution dict.
    """
    if extra_subs is None:
        extra_subs = {}

    random.seed(seed)
    free_vals = {}
    for g in free_params:
        free_vals[g] = random.choice([-1, 1]) * 10 ** random.uniform(-5, 5)

    numerical_solution = {}
    for g, val in symbolic_solution.items():
        v = val
        for fp, fv in free_vals.items():
            if hasattr(v, 'subs'):
                v = v.subs(fp, fv)
        if hasattr(v, 'subs'):
            v = v.subs(extra_subs)
        numerical_solution[g] = float(v) if hasattr(v, '__float__') else v

    all_zero = all(
        (isinstance(v, (int, float)) and abs(v) < 1e-15)
        or v == 0
        for v in numerical_solution.values()
    )
    if all_zero:
        return numerical_solution, free_vals, True

    return numerical_solution, free_vals, False


# ════════════════════════════════════════════════════════════════
#  SECTION 3 :  Post-processing — substitute, verify, gauge-fix
# ════════════════════════════════════════════════════════════════

def substitute_solution(eom_dict, solution, t_s=t_sym, keep_dims=False):
    """Substitute coefficient values into EOM and simplify."""
    final = {}
    for name, eom in eom_dict.items():
        e = eom
        for g, val in solution.items():
            e = e.subs(g, val)
        if not keep_dims:
            e = e.subs(sp.Symbol('M_p', positive=True), 1)
            e = e.subs(sp.Symbol(r'\Lambda', positive=True), 1)
            e = e.subs(sp.Symbol('m_1', positive=True), 1)
            e = e.subs(sp.Symbol('m_2', positive=True), 1)
            e = e.subs(sp.Symbol('f_1', positive=True), 1)
            e = e.subs(sp.Symbol('f_2', positive=True), 1)
        e = _simp(e)
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
        for k in range(12, 0, -1):
            e = e.subs(sp.Derivative(N_t, (t_s, k)), 0)
        e = e.subs(N_t, 1)
        e = _simp(e)
        fixed[name] = e
    return fixed


def add_matter_source(eom_dict):
    """
    Add pressureless dust (matter) source to E_N.
    E_a, E_φ1, E_φ2 unchanged.
    """
    result = {}
    for name, eom in eom_dict.items():
        if name == 'N':
            result[name] = eom - rho_m0
        else:
            result[name] = eom
    return result


# ════════════════════════════════════════════════════════════════
#  SECTION 4 :  Main driver — process one Lagrangian end-to-end
# ════════════════════════════════════════════════════════════════

def process_lagrangian(L_data: dict, index: int, tex_fn=tex,
                       max_allowed: int = 2, seed: int = 42):
    """
    Full pipeline for a single Lagrangian from masker v3.0:
      raw EOM → ghost constraints → solve → verify → gauge-fix → output.
    """
    print(f"\n{'═' * 70}")
    print(f"  LAGRANGIAN  #{index}")
    print(f"{'═' * 70}")
    print(f"  General:        {L_data['general']}")
    print(f"  FLRW:           {tex_fn(L_data['substituted'])}")

    # Handle both old (has_phi) and new (scalar_config) format
    scalar_config = L_data.get('scalar_config', None)
    if scalar_config is not None:
        print(f"  scalar_config:  {scalar_config}")
        pot_types = L_data.get('potential_types', {})
        print(f"  potential_types: {pot_types}")
    else:
        print(f"  has_φ:          {L_data.get('has_phi', False)}")

    for i, tt in enumerate(L_data['terms']):
        tag = "  (fixed)" if tt.get('fixed') else ""
        sector_tag = f"  [{tt.get('sector', 'gravity')}]"
        pot_tag = f"  pot={tt['potential_type']}" if 'potential_type' in tt else ""
        print(f"    [{i+1}] {tt['coeff_symbol']:10s}  dim={tt['mass_dim']}  "
              f"Λ^{tt['lambda_power']}  {tt['candidate']}{tag}{sector_tag}{pot_tag}")

    L = L_data['substituted']

    # Which Greek symbols are actually present in this Lagrangian?
    used = [g for g in _GREEK_COEFFS if L.has(g)]
    # Also check for fallback c_{i} symbols
    for tt in L_data['terms']:
        if tt.get('fixed'):
            continue
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
    sym_solution, free_params, extra_subs, is_trivial = \
        extract_and_solve_ghost_constraints(
            eoms, used, t_sym, max_allowed=max_allowed, seed=seed)

    if is_trivial:
        print("\n  ⇒ This combination of terms has no ghost-free realisation.")
        return {'index': index, 'L_data': L_data, 'raw_eom': eoms, 'trivial': True}

    print(f"\n  ── Symbolic coefficient relations ──")
    for g in used:
        val = sym_solution[g]
        tag = " (free)" if g in free_params else " (determined)"
        print(f"    {g}  =  {val}{tag}")

    # ─── Step 3: symbolic EOM (free coefficients still symbolic) ───
    print(f"\n  {'─'*60}")
    print(f"  Step 3 : EOM with free coefficients (ghost-free, fully symbolic)")
    print(f"  {'─'*60}")
    symbolic_eoms = substitute_solution(eoms, sym_solution, t_sym, keep_dims=True)
    all_clean = verify_max_order(symbolic_eoms, max_allowed, t_sym)

    if not all_clean:
        print("\n  ⚠  Ghost terms remain after symbolic substitution — retrying with fresh profiles")
        # Important: retry the FULL coefficient system, not only the free leftovers.
        # If the first sampled linear system produced a wrong determined relation,
        # solving only the remaining free symbols cannot repair it.
        MAX_RETRY = 3
        for retry_id in range(1, MAX_RETRY + 1):
            retry_seed = seed + 1009 * retry_id
            print(f"\n  Retry {retry_id}/{MAX_RETRY}: solve all coefficients again "
                  f"with fresh profiles, seed={retry_seed}")
            sol2, fp2, _, triv2 = extract_and_solve_ghost_constraints(
                eoms, used, t_sym, max_allowed=max_allowed, seed=retry_seed)
            sym_solution = sol2
            free_params = fp2
            symbolic_eoms = substitute_solution(eoms, sym_solution, t_sym, keep_dims=True)
            all_clean = verify_max_order(symbolic_eoms, max_allowed, t_sym)
            if all_clean:
                print(f"  ✓ Retry {retry_id} succeeded: symbolic EOM are clean")
                break
        if not all_clean:
            print("  ⚠  All retries failed: this Lagrangian will be marked as still containing ghost terms")

    # ─── Step 4: gauge-fix N=1 (symbolic) ───
    print(f"\n  {'─'*60}")
    print(f"  Step 4 : Gauge-fix  N = 1  (symbolic)")
    print(f"  {'─'*60}")
    symbolic_gauged = gauge_fix_lapse(symbolic_eoms, t_sym)

    print(f"\n  ── Final EOM  (N = 1 gauge, symbolic, ghost-free) ──")
    for name, eq in symbolic_gauged.items():
        print(f"\n  E_{name}  =")
        print(f"    {tex_fn(eq)}")
        for fn in DYN_NAMES:
            func = dict(zip(DYN_NAMES, DYN_FUNCS))[fn]
            o = detect_max_order(eq, func, t_sym)
            if o >= 0:
                print(f"    (max order of {fn} : {o})")

    # Add matter source to E_N (symbolic)
    symbolic_gauged_matter = add_matter_source(symbolic_gauged)
    print(f"\n  ── Final EOM  (N = 1 gauge, symbolic, with dust source) ──")
    for name, eq in symbolic_gauged_matter.items():
        print(f"\n  E_{name}  =")
        print(f"    {tex_fn(eq)}")
        for fn in DYN_NAMES:
            func = dict(zip(DYN_NAMES, DYN_FUNCS))[fn]
            o = detect_max_order(eq, func, t_sym)
            if o >= 0:
                print(f"    (max order of {fn} : {o})")

    return {
        'index':                  index,
        'L_data':                 L_data,
        'raw_eom':                eoms,
        'sym_solution':           sym_solution,
        'free_params':            free_params,
        'symbolic_eom':           symbolic_eoms,
        'symbolic_gauged':        symbolic_gauged,
        'symbolic_gauged_matter': symbolic_gauged_matter,
        'is_clean':               all_clean,
        'trivial':                False,
    }


# ════════════════════════════════════════════════════════════════
#  SECTION 5 :  Self-test
# ════════════════════════════════════════════════════════════════

def self_test():
    """Quick sanity checks on known Lagrangians."""
    print("=" * 60)
    print("  SELF-TEST : Ostrogradsky EL on known Lagrangians")
    print("=" * 60)

    N_t    = _N_cls(t_sym)
    a_t    = _a_cls(t_sym)
    phi1_t = _phi1_cls(t_sym)
    phi2_t = _phi2_cls(t_sym)

    # ── Test 1: L = ½ φ1'²  →  E_φ1 = -φ1'' = 0 ──
    print("\n── Test 1: L = ½ φ1'² ──")
    L1 = sp.Rational(1, 2) * sp.Derivative(phi1_t, t_sym) ** 2
    eq1 = euler_lagrange(L1, _phi1_cls, t_sym)
    expected1 = -sp.Derivative(phi1_t, (t_sym, 2))
    assert sp.simplify(eq1 - expected1) == 0, f"FAIL: {eq1}"
    print(f"  E_φ1 = {tex(eq1)}   ✓")

    # ── Test 2: L = ½ (φ1'')²  →  E_φ1 = φ1⁽⁴⁾ = 0 ──
    print("\n── Test 2: L = ½ (φ1'')² ──")
    L2 = sp.Rational(1, 2) * sp.Derivative(phi1_t, (t_sym, 2)) ** 2
    eq2 = euler_lagrange(L2, _phi1_cls, t_sym)
    expected2 = sp.Derivative(phi1_t, (t_sym, 4))
    assert sp.simplify(eq2 - expected2) == 0, f"FAIL: {eq2}"
    print(f"  E_φ1 = {tex(eq2)}   ✓")

    # ── Test 3: GR minisuperspace  L = -3 a ȧ²/N  ──
    print("\n── Test 3: L = -3 a ȧ²/N ──")
    L3 = -3 * a_t * sp.Derivative(a_t, t_sym) ** 2 / N_t
    eom3 = compute_all_eom(L3, t_sym)
    g3 = gauge_fix_lapse(eom3, t_sym)
    print(f"  E_N(N=1) = {tex(g3.get('N', 0))}")
    print(f"  E_a(N=1) = {tex(g3.get('a', 0))}")
    verify_max_order(g3, max_allowed=2, t_s=t_sym)

    # ── Test 4: Ghost detection  L = α φ1'² + β (φ1'')² ──
    print("\n── Test 4: ghost constraint  L = α φ1'² + β (φ1'')² ──")
    alpha, beta = sp.Symbol(r'\alpha'), sp.Symbol(r'\beta')
    L4 = alpha * sp.Derivative(phi1_t, t_sym) ** 2 + beta * sp.Derivative(phi1_t, (t_sym, 2)) ** 2
    eom4 = compute_all_eom(L4, t_sym)
    sym_sol4, free4, extra4, triv4 = extract_and_solve_ghost_constraints(
        eom4, [alpha, beta], t_sym, max_allowed=2, seed=99)
    assert sym_sol4[beta] == 0 or abs(float(sym_sol4[beta])) < 1e-12, \
        f"FAIL: β should be 0, got {sym_sol4[beta]}"
    assert alpha in free4, f"FAIL: α should be free"
    num_sol4, _, triv_num4 = assign_free_params(sym_sol4, free4, extra4, seed=99)
    print(f"  Solution: α={num_sol4[alpha]}, β={num_sol4[beta]}")
    assert abs(float(num_sol4[beta])) < 1e-12, f"FAIL: β should be 0"
    assert abs(float(num_sol4[alpha])) > 1e-12, f"FAIL: α should be nonzero"
    final4 = substitute_solution(eom4, num_sol4, t_sym)
    verify_max_order(final4, 2, t_sym)
    print("  ✓  β = 0 (ghost removed), α free")

    # ── Test 5: Two-field decoupled  L = ½ φ1'² + ½ φ2'² ──
    print("\n── Test 5: L = ½ φ1'² + ½ φ2'² ──")
    L5 = (sp.Rational(1, 2) * sp.Derivative(phi1_t, t_sym) ** 2
        + sp.Rational(1, 2) * sp.Derivative(phi2_t, t_sym) ** 2)
    eom5 = compute_all_eom(L5, t_sym)
    assert 'phi1' in eom5, "FAIL: phi1 EOM missing"
    assert 'phi2' in eom5, "FAIL: phi2 EOM missing"
    eq5_1 = eom5['phi1']
    eq5_2 = eom5['phi2']
    assert sp.simplify(eq5_1 + sp.Derivative(phi1_t, (t_sym, 2))) == 0, \
        f"FAIL: E_phi1 = {eq5_1}"
    assert sp.simplify(eq5_2 + sp.Derivative(phi2_t, (t_sym, 2))) == 0, \
        f"FAIL: E_phi2 = {eq5_2}"
    print(f"  E_φ1 = {tex(eq5_1)}   ✓")
    print(f"  E_φ2 = {tex(eq5_2)}   ✓")

    # ── Test 6: Coupled  L = φ1 · φ2  →  E_φ1 = φ2, E_φ2 = φ1 ──
    print("\n── Test 6: L = φ1 · φ2  (coupling) ──")
    L6 = phi1_t * phi2_t
    eom6 = compute_all_eom(L6, t_sym)
    assert sp.simplify(eom6['phi1'] - phi2_t) == 0, f"FAIL: {eom6['phi1']}"
    assert sp.simplify(eom6['phi2'] - phi1_t) == 0, f"FAIL: {eom6['phi2']}"
    print(f"  E_φ1 = {tex(eom6['phi1'])}   ✓  (= φ2)")
    print(f"  E_φ2 = {tex(eom6['phi2'])}   ✓  (= φ1)")

    # ── Test 7: Axion potential  L = -m² f² (1-cos(φ1/f)) ──
    print("\n── Test 7: axion potential  L = -m² f² (1-cos(φ1/f)) ──")
    m_s = sp.Symbol('m_1', positive=True)
    f_s = sp.Symbol('f_1', positive=True)
    L7 = -m_s**2 * f_s**2 * (1 - sp.cos(phi1_t / f_s))
    eq7 = euler_lagrange(L7, _phi1_cls, t_sym)
    expected7 = -m_s**2 * f_s * sp.sin(phi1_t / f_s)
    assert sp.simplify(eq7 - expected7) == 0, f"FAIL: {eq7} vs {expected7}"
    print(f"  E_φ1 = {tex(eq7)}   ✓  (= -m²f sin(φ1/f))")

    print("\n" + "=" * 60)
    print("  All self-tests passed.")
    print("=" * 60 + "\n")


# ════════════════════════════════════════════════════════════════
#  SECTION 6 :  MAIN — read pickled Lagrangians, compute EOM
# ════════════════════════════════════════════════════════════════

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
        print("  Please run GR_grammar_masker_v3_0.py first to generate it:")
        print("    python GR_grammar_masker_v3_0.py")
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

    tex_fn = tex

    # ── Configuration ──
    N_SAMPLES = None
    MAX_TERMS = 12          # process all Lagrangians up to 12 terms

    # ── Summary of available Lagrangians ──
    print(f"\n  Available Lagrangians:")
    for nt in sorted(lagrangian_results.keys()):
        tag = "  ← skip" if nt > MAX_TERMS else ""
        print(f"    {nt}-term : {len(lagrangian_results[nt])} Lagrangians{tag}")
    print(f"\n  Config:  MAX_TERMS = {MAX_TERMS},  N_SAMPLES = {N_SAMPLES}")

    # ── Process samples ──
    all_results = []
    summary_lines = []

    _jobs = []
    for n_terms in sorted(lagrangian_results.keys()):
        if n_terms > MAX_TERMS:
            continue
        lags = lagrangian_results[n_terms]
        if not lags:
            continue
        for i, L_data in enumerate(lags[:N_SAMPLES]):
            global_idx = sum(len(lagrangian_results.get(k, []))
                             for k in sorted(lagrangian_results.keys()) if k < n_terms) + i + 1
            _jobs.append((L_data, global_idx, n_terms, 42 + i))

    print(f"\n  Jobs: {len(_jobs)} Lagrangians to process")

    from multiprocessing import Pool, cpu_count
    import multiprocessing as _mp
    import io
    try:
        _mp.set_start_method('fork')
    except RuntimeError:
        pass

    N_WORKERS = 1

    print(f"  Workers: {N_WORKERS}")

    def _process_one(args):
        L_data, global_idx, n_terms, seed = args
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        t0 = _time.time()
        result = process_lagrangian(L_data, global_idx, tex_fn,
                                    max_allowed=2, seed=seed)
        dt = _time.time() - t0
        sys.stdout = old
        summary = None
        if result is not None:
            if result.get('trivial'):
                summary = f"  #{global_idx:3d}  ({n_terms}-term)  TRIVIAL (all zero)  [{dt:.1f}s]"
            else:
                n_free = len(result['free_params'])
                n_det  = len([g for g in result['sym_solution']
                              if g not in result['free_params']])
                tag = "✓ CLEAN" if result['is_clean'] else "⚠ GHOST"
                sc = result['L_data'].get('scalar_config', '?')
                summary = (f"  #{global_idx:3d}  ({n_terms}-term, {sc})  "
                           f"det={n_det}  free={n_free}  {tag}  [{dt:.1f}s]")
        return result, summary, buf.getvalue()

    t0_all = _time.time()
    if N_WORKERS > 1 and len(_jobs) > 1:
        print(f"\n  ⚡ Parallel processing with {N_WORKERS} workers ...")
        with Pool(N_WORKERS) as pool:
            raw = pool.map(_process_one, _jobs)
    else:
        print(f"\n  Running sequentially ...")
        raw = [_process_one(j) for j in _jobs]
    dt_all = _time.time() - t0_all

    for result, summary, captured in raw:
        print(captured, end='')
        if result is not None:
            all_results.append(result)
        if summary is not None:
            summary_lines.append(summary)

    print(f"\n  Total EOM time: {dt_all:.1f}s  "
          f"({dt_all/max(len(_jobs),1):.1f}s per Lagrangian)")

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
        f.write("EOM Ghost-Free Analysis Results (v5.0 — two scalar fields)\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        for r in all_results:
            idx = r['index']
            f.write(f"{'═' * 60}\n")
            f.write(f"Lagrangian #{idx}\n")

            L_data = r.get('L_data')
            if L_data:
                f.write(f"  General:        {L_data['general']}\n")
                f.write(f"  FLRW:           {tex_fn(L_data['substituted'])}\n")
                sc = L_data.get('scalar_config', None)
                if sc is not None:
                    f.write(f"  scalar_config:  {sc}\n")
                    f.write(f"  potential_types: {L_data.get('potential_types', {})}\n")
                else:
                    f.write(f"  has_phi:        {L_data.get('has_phi', False)}\n")
                f.write(f"  Terms:\n")
                for ti, tt in enumerate(L_data['terms']):
                    tag = "  (fixed)" if tt.get('fixed') else ""
                    sector_tag = f"  [{tt.get('sector', 'gravity')}]"
                    pot_tag = f"  pot={tt['potential_type']}" if 'potential_type' in tt else ""
                    f.write(f"    [{ti+1}] {tt['coeff_symbol']:10s}  "
                            f"dim={tt['mass_dim']}  Λ^{tt['lambda_power']}  "
                            f"{tt['candidate']}{tag}{sector_tag}{pot_tag}\n")

            if r.get('raw_eom'):
                f.write(f"  Raw EOM:\n")
                for name, eq in r['raw_eom'].items():
                    f.write(f"    E_{name} = {tex_fn(eq)}\n")
                    for fn, fc in zip(DYN_NAMES, DYN_FUNCS):
                        o = detect_max_order(eq, fc, t_sym)
                        if o >= 0:
                            f.write(f"      max order of {fn}: {o}\n")

            if r.get('trivial'):
                f.write("  → TRIVIAL (all coefficients must be zero)\n\n")
                continue

            f.write(f"  Ghost-free coefficient relations:\n")
            sym_sol = r.get('sym_solution', {})
            for g, val in sym_sol.items():
                tag = "(free)" if g in r['free_params'] else "(determined)"
                f.write(f"    {g} = {val}  {tag}\n")

            if r.get('symbolic_gauged'):
                f.write(f"  Final EOM (N=1 gauge, ghost-free, symbolic):\n")
                for name, eq in r['symbolic_gauged'].items():
                    f.write(f"    E_{name} = {tex_fn(eq)}\n")
                    for fn, fc in zip(DYN_NAMES, DYN_FUNCS):
                        o = detect_max_order(eq, fc, t_sym)
                        if o >= 0:
                            f.write(f"      max order of {fn}: {o}\n")

            if r.get('symbolic_gauged_matter'):
                f.write(f"  Final EOM (N=1 gauge, ghost-free, symbolic, +dust):\n")
                for name, eq in r['symbolic_gauged_matter'].items():
                    f.write(f"    E_{name} = {tex_fn(eq)}\n")
                    for fn, fc in zip(DYN_NAMES, DYN_FUNCS):
                        o = detect_max_order(eq, fc, t_sym)
                        if o >= 0:
                            f.write(f"      max order of {fn}: {o}\n")

            f.write(f"  Ghost-free: {'YES' if r['is_clean'] else 'NO'}\n")
            f.write("\n")
    print(f"\n  Results saved to: {out_path}")

    # ── Save results as pickle ──
    pkl_out = os.path.join(_out_dir, 'eom_results.pkl')
    with open(pkl_out, 'wb') as f:
        pickle.dump(all_results, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"  Pickle saved to: {pkl_out}")

    # ── Close log ──
    sys.stdout = sys.__stdout__
    _log_fh.close()
    print(f"[EOM Log] Done. Log saved to: {_log_path}")