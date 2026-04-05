import sympy as sp
from functools import reduce
import sys
import os
from datetime import datetime

# =========================================
# Logging: redirect stdout to a timestamped log file
# =========================================
_log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')
os.makedirs(_log_dir, exist_ok=True)
_log_path = os.path.join(_log_dir, datetime.now().strftime('%Y%m%d_%H%M%S') + '.log')
_log_fh = open(_log_path, 'w', encoding='utf-8')

class _Tee:
    """Write to both original stdout and log file."""
    def __init__(self, *streams):
        self.streams = streams
    def write(self, data):
        for s in self.streams:
            s.write(data)
    def flush(self):
        for s in self.streams:
            s.flush()

sys.stdout = _Tee(sys.__stdout__, _log_fh)
print(f"[Log] Writing output to: {_log_path}\n")

# =========================================
# Readable printer: Derivative(N(t), t) -> dN/dt
# Use tex(expr) wherever a sympy expression is printed.
# =========================================
from sympy.printing.str import StrPrinter

class ReadablePrinter(StrPrinter):
    def _print_Derivative(self, expr):
        func = expr.args[0]          # e.g. N(t)
        fname = func.func.__name__   # e.g. 'N'
        total_order = sum(int(order) for _, order in expr.args[1:])
        # build numerator: d^n f
        num = f"d^{total_order}{fname}" if total_order > 1 else f"d{fname}"
        # build denominator: dt^n (for single variable)
        parts = []
        for var, order in expr.args[1:]:
            order = int(order)
            parts.append(f"d{var}^{order}" if order > 1 else f"d{var}")
        denom = ''.join(parts)
        return f"{num}/{denom}"

_printer = ReadablePrinter()

def tex(expr):
    """Print sympy expression with derivatives as dN/dt style."""
    return _printer.doprint(expr)

# =========================================
# 1. Coordinates (Cartesian)
# =========================================
t, x, y, z = sp.symbols('t x y z', real=True)
coords = [t, x, y, z]
n = len(coords)

# =========================================
# 2. metric g_{mu nu}
#    ADM FLRW metric in Cartesian coordinates (k=0, flat):
#    ds^2 = -N(t)^2 dt^2 + a(t)^2 (dx^2 + dy^2 + dz^2)
# =========================================
N = sp.Function('N', positive=True)(t)   # lapse function  (N > 0)
a = sp.Function('a', positive=True)(t)   # scale factor   (a > 0)

g = sp.Matrix([
    [-N**2,    0,      0,      0],
    [0,     a**2,      0,      0],
    [0,        0,   a**2,      0],
    [0,        0,      0,   a**2]
])

g_inv = sp.simplify(g.inv())

# =========================================
# 3. Christoffel symbols: Gamma^rho_{mu nu}
# =========================================
Gamma = [[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]

for rho in range(n):
    for mu in range(n):
        for nu in range(n):
            expr = sp.Integer(0)
            for sigma in range(n):
                expr += g_inv[rho, sigma] * (
                    sp.diff(g[sigma, nu], coords[mu]) +
                    sp.diff(g[sigma, mu], coords[nu]) -
                    sp.diff(g[mu, nu], coords[sigma])
                )
            Gamma[rho][mu][nu] = sp.simplify(sp.Rational(1, 2) * expr)

# =========================================
# 4. Riemann tensor: R^rho_{sigma mu nu}
#    Convention:
#    R^rho_{sigma mu nu}
#      = d_mu Gamma^rho_{nu sigma}
#      - d_nu Gamma^rho_{mu sigma}
#      + Gamma^rho_{mu lambda} Gamma^lambda_{nu sigma}
#      - Gamma^rho_{nu lambda} Gamma^lambda_{mu sigma}
# =========================================
Riemann = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]

for rho in range(n):
    for sigma in range(n):
        for mu in range(n):
            for nu in range(n):
                expr = sp.diff(Gamma[rho][nu][sigma], coords[mu]) - sp.diff(Gamma[rho][mu][sigma], coords[nu])
                for lam in range(n):
                    expr += Gamma[rho][mu][lam] * Gamma[lam][nu][sigma]
                    expr -= Gamma[rho][nu][lam] * Gamma[lam][mu][sigma]
                Riemann[rho][sigma][mu][nu] = sp.simplify(expr)

# =========================================
# 5. Ricci tensor: R_{mu nu} = R^rho_{mu rho nu}
# =========================================
Ricci = [[sp.Integer(0) for _ in range(n)] for _ in range(n)]

for mu in range(n):
    for nu in range(n):
        expr = sp.Integer(0)
        for rho in range(n):
            expr += Riemann[rho][mu][rho][nu]
        Ricci[mu][nu] = sp.simplify(expr)

# =========================================
# 6. Ricci scalar: R = g^{mu nu} R_{mu nu}
# =========================================
R_scalar = sp.Integer(0)
for mu in range(n):
    for nu in range(n):
        R_scalar += g_inv[mu, nu] * Ricci[mu][nu]
R_scalar = sp.simplify(R_scalar)

# =========================================
# 7. Print nonzero components
# =========================================
#print("Nonzero Christoffel symbols:")
for rho in range(n):
    for mu in range(n):
        for nu in range(n):
            if Gamma[rho][mu][nu] != 0:
                print(f"  Gamma^{coords[rho]}_{{{coords[mu]}{coords[nu]}}} =", tex(Gamma[rho][mu][nu]))


#print("\n--- Riemann tensor verification ---")
#print("R^x_{yxy} =", tex(Riemann[1][2][1][2]))
#print("R^t_{xtx} =", tex(Riemann[0][1][0][1]))

#print("\nNonzero Ricci tensor components:")
for mu in range(n):
    for nu in range(n):
        if Ricci[mu][nu] != 0:
            print(f"  R_{{{coords[mu]}{coords[nu]}}} =", tex(Ricci[mu][nu]))

#print("\nRicci scalar:")
#print("  R =", tex(R_scalar))



# =======================================
# 8. Two-index contraction helper
#    Contracts tensor A (rank rankA) with tensor B (rank rankB)
#    over the given pairs of axes: contract_pairs = [(i_A, j_B), ...]
# =======================================
def two_contract(A, B, contract_pairs):
    A = sp.Array(A)
    B = sp.Array(B)
    rankA = len(A.shape)
    rankB = len(B.shape)

    for i, j in contract_pairs:
        if A.shape[i] != B.shape[j]:
            raise ValueError(
                f"Dimension mismatch: A axis {i} has size {A.shape[i]}, "
                f"but B axis {j} has size {B.shape[j]}"
            )

    TP = sp.tensorproduct(A, B)
    # B's indices are shifted by rankA in the tensor product
    contraction_axes = tuple((i, rankA + j) for i, j in contract_pairs)
    result = sp.tensorcontraction(TP, *contraction_axes)
    return sp.simplify(result)

#print("\ng contracted with Riemann on second index (g^{mu nu} R_{nu sigma rho kappa}):")
#print(tex(two_contract(g_inv, Riemann, [(1, 1)])))

# ====================================
# 9. Multi-tensor contraction helper
#    Contracts a list of tensors over the given global index pairs
#    contract_pairs refers to axes in the full tensor product
# ====================================
def multi_contract(tensors, contract_pairs):
    arrays = [sp.Array(T) for T in tensors]
    TP = reduce(sp.tensorproduct, arrays)
    result = sp.tensorcontraction(TP, *contract_pairs)
    return sp.simplify(result)

#print("\ng * Riemann * Riemann contraction shape:")
#mrr = multi_contract([g, Riemann, Riemann], [(0, 2), (1, 6)])
#print(mrr.shape)

# =========================================
# 10. Covariant derivative
#
#  For a general tensor T of type (p, q) — p upper, q lower indices —
#  stored as a nested list with index order [up_1,...,up_p, down_1,...,down_q]:
#
#  ∇_rho T^{mu1..mup}_{nu1..nuq}
#    = d_rho T^{mu1..mup}_{nu1..nuq}
#      + sum_{i=1}^{p}  Gamma^{mu_i}_{rho lam} T^{mu1..lam..mup}_{nu1..nuq}
#      - sum_{j=1}^{q}  Gamma^{lam}_{rho nu_j} T^{mu1..mup}_{nu1..lam..nuq}
#
#  Result index order: [up_1,...,up_p, down_1,...,down_q, rho]  (rho is the new lower index)
# =========================================

def cov_deriv(T, p, q):
    """
    Covariant derivative of a rank-(p, q) tensor T.

    Parameters
    ----------
    T    : nested list of shape [n]*p + [n]*q
           Index order: all p upper indices first, then q lower indices.
    p    : number of contravariant (upper) indices
    q    : number of covariant (lower) indices

    Returns
    -------
    DT   : nested list of shape [n]*(p+q+1)
           Same index order as T, with one extra lower index rho appended.
           DT[mu1]..[mup][nu1]..[nuq][rho] = ∇_rho T^{mu1..mup}_{nu1..nuq}
    """
    rank = p + q

    # Helper: get element from arbitrarily nested list by index tuple
    def get(arr, idx):
        for i in idx:
            arr = arr[i]
        return arr

    # Helper: set element in arbitrarily nested list by index tuple
    def set_(arr, idx, val):
        for i in idx[:-1]:
            arr = arr[i]
        arr[idx[-1]] = val

    # Build output tensor of shape [n]*(rank+1), initialised to 0
    def make_zeros(depth):
        if depth == 0:
            return sp.Integer(0)
        return [make_zeros(depth - 1) for _ in range(n)]

    DT = make_zeros(rank + 1)

    import itertools
    for idx in itertools.product(range(n), repeat=rank):
        mu = idx[:p]   # upper indices
        nu = idx[p:]   # lower indices
        for rho in range(n):
            # Partial derivative term
            expr = sp.diff(get(T, idx), coords[rho])

            # +Gamma terms: one for each upper index
            for i in range(p):
                for lam in range(n):
                    # replace mu[i] with lam in the index tuple
                    contracted_idx = mu[:i] + (lam,) + mu[i+1:] + nu
                    expr += Gamma[mu[i]][rho][lam] * get(T, contracted_idx)

            # -Gamma terms: one for each lower index
            for j in range(q):
                for lam in range(n):
                    # replace nu[j] with lam in the index tuple
                    contracted_idx = mu + nu[:j] + (lam,) + nu[j+1:]
                    expr -= Gamma[lam][rho][nu[j]] * get(T, contracted_idx)

            set_(DT, idx + (rho,), sp.simplify(expr))

    return DT


# ----- Examples -----

# Covariant derivative of a contravariant vector V^mu = delta^mu_1 (unit vector in x)
print("\n--- Covariant derivative examples ---")

V_up = [[sp.Integer(1) if mu == 1 else sp.Integer(0) for mu in range(n)]]
V_up = [sp.Integer(1) if mu == 1 else sp.Integer(0) for mu in range(n)]
DV_up = cov_deriv(V_up, p=1, q=0)
print("\n∇_rho V^mu  (V^mu = delta^mu_x):")
for mu in range(n):
    for rho in range(n):
        val = DV_up[mu][rho]
        if val != 0:
            print(f"  ∇_{coords[rho]} V^{coords[mu]} =", tex(val))

# Covariant derivative of a covariant vector W_mu = g_{mu 0} (first row of metric)
W_down = [g[mu, 0] for mu in range(n)]
DW_down = cov_deriv(W_down, p=0, q=1)
print("\n∇_rho W_mu  (W_mu = g_{mu t}):")
for mu in range(n):
    for rho in range(n):
        val = DW_down[mu][rho]
        if val != 0:
            print(f"  ∇_{coords[rho]} W_{coords[mu]} =", tex(val))

# Covariant derivative of the metric g_{mu nu} — should vanish (metric compatibility)
g_list = [[g[mu, nu] for nu in range(n)] for mu in range(n)]
Dg = cov_deriv(g_list, p=0, q=2)
#print("\n∇_rho g_{mu nu} (should be zero everywhere):")
all_zero = all(
    sp.simplify(Dg[mu][nu][rho]) == 0
    for mu in range(n) for nu in range(n) for rho in range(n)
)
#print("  Metric compatibility ∇g = 0:", all_zero)

# =========================================
# 11. Levi-Civita symbol and tensor
#
#  Levi-Civita SYMBOL (tensor density, no metric):
#    eps[mu][nu][rho][sigma] = +1 / -1 / 0
#    purely combinatorial, same in any coordinate system
#
#  Levi-Civita TENSOR (true tensor, includes metric):
#    covariant:     E_{mu nu rho sigma} = sqrt(-det g) * eps[mu][nu][rho][sigma]
#    contravariant: E^{mu nu rho sigma} = -1/sqrt(-det g) * eps[mu][nu][rho][sigma]
#    (the sign in E^{...} comes from the Lorentzian signature: g^{mu...} picks up
#     factors of g_inv, giving an overall factor of det(g_inv) = 1/det(g) < 0)
# =========================================

import itertools

def levi_civita_symbol(dim):
    """
    Return the Levi-Civita symbol as a nested list of shape [dim]*dim.
    eps[i0][i1]...[i_{dim-1}] = sign of the permutation (i0,...) of (0,...,dim-1),
    or 0 if any two indices coincide.
    """
    def perm_sign(perm):
        """Return the sign (+1/-1) of a permutation, or 0 if it has repeats."""
        perm = list(perm)
        if len(set(perm)) < len(perm):
            return 0
        sign = 1
        for i in range(len(perm)):
            while perm[i] != i:
                j = perm[i]
                perm[i], perm[j] = perm[j], perm[i]
                sign *= -1
        return sign

    # Build dim-dimensional nested list
    def make_eps(depth):
        if depth == 0:
            return sp.Integer(0)
        return [make_eps(depth - 1) for _ in range(dim)]

    eps = make_eps(dim)

    def set_(arr, idx, val):
        for i in idx[:-1]:
            arr = arr[i]
        arr[idx[-1]] = val

    for idx in itertools.product(range(dim), repeat=dim):
        set_(eps, idx, sp.Integer(perm_sign(idx)))

    return eps


# Build the symbol
eps = levi_civita_symbol(n)

# det(g) and sqrt(-det(g))  [for Lorentzian metric det(g) < 0]
det_g   = sp.simplify(g.det())
sqrt_mg = sp.simplify(sp.sqrt(-det_g))   # sqrt(-det g), real and positive

# Covariant Levi-Civita tensor: E_{mu nu rho sigma} = sqrt(-g) * eps
E_down = [[[[sp.simplify(sqrt_mg * eps[mu][nu][rho][sigma])
             for sigma in range(n)]
            for rho   in range(n)]
           for nu    in range(n)]
          for mu    in range(n)]

# Contravariant Levi-Civita tensor: E^{mu nu rho sigma} = -eps / sqrt(-g)
E_up = [[[[sp.simplify(-eps[mu][nu][rho][sigma] / sqrt_mg)
           for sigma in range(n)]
          for rho   in range(n)]
         for nu    in range(n)]
        for mu    in range(n)]

# ----- Print results -----
#print("\n--- Levi-Civita ---")
#print(f"det(g)      = {tex(det_g)}")
#print(f"sqrt(-det g)= {tex(sqrt_mg)}")

#print("\nNonzero components of Levi-Civita symbol eps[mu][nu][rho][sigma]:")
#for idx in itertools.product(range(n), repeat=4):
#    mu, nu, rho, sigma = idx
#    val = eps[mu][nu][rho][sigma]
#    if val != 0:
#        print(f"  eps[{mu}][{nu}][{rho}][{sigma}] = {val}")

#print("\nNonzero components of covariant tensor E_{mu nu rho sigma}:")
#for idx in itertools.product(range(n), repeat=4):
#    mu, nu, rho, sigma = idx
#    val = E_down[mu][nu][rho][sigma]
#    if val != 0:
#        print(f"  E_{{{coords[mu]}{coords[nu]}{coords[rho]}{coords[sigma]}}} = {tex(val)}")

#print("\nNonzero components of contravariant tensor E^{mu nu rho sigma}:")
#for idx in itertools.product(range(n), repeat=4):
#    mu, nu, rho, sigma = idx
#    val = E_up[mu][nu][rho][sigma]
#    if val != 0:
#        print(f"  E^{{{coords[mu]}{coords[nu]}{coords[rho]}{coords[sigma]}}} = {tex(val)}")

# =========================================
# Riemann tensor verification
# R^rho_{sigma mu nu} = Riemann[rho][sigma][mu][nu]
# coords: t=0, x=1, y=2, z=3
# =========================================

# =========================================
# Mass dimensions  (natural units: ℏ = c = 1, 4D spacetime)
#
# Derived from the action being dimensionless [S] = 0:
#   S = ∫ d^4x sqrt(-g) L   =>  [L] = 4  (Lagrangian density)
#
# From GR.txt GENEROR_Curvature_BLOCK:
#   g      : [g]   = 0   (metric is dimensionless)
#   Gamma  : [Γ]   = 1   (Christoffel = g^{-1} ∂g, one derivative)
#   R_iem  : [Rie] = 2   (Riemann  = ∂Γ + ΓΓ, two derivatives of g)
#   R_ic   : [Ric] = 2   (Ricci    = contraction of Riemann)
#   R      : [R]   = 2   (Ricci scalar)
#   ∇      : [∇]   = 1   (covariant derivative acts as one ∂)
#   □      : [□]   = 2   (Laplace-Beltrami = ∇∇)
#
# Scalar field φ:
#   Kinetic term (∂φ)^2 ⊂ L  =>  2[∂φ] = 4  =>  [φ] = 1
#   Equivalently: [∂] = 1 and [φ] = 1  =>  [∂φ] = 2  ✓
# =========================================

mass_dim = {
    "metric_g":              0,   # g_{μν}, g^{μν}  — dimensionless
    "christoffel":           1,   # Γ^ρ_{μν}  =  g^{-1} ∂g
    "riemann":               2,   # R^ρ_{σμν}
    "ricci_tensor":          2,   # R_{μν}
    "ricci_scalar":          2,   # R
    "covariant_derivative":  1,   # ∇_μ  (one power of momentum)
    "laplace_beltrami":      2,   # □ = g^{μν} ∇_μ ∇_ν
    "scalar_field":          1,   # φ  (from [L_kin] = 4 in 4D)
}

def dim_of(operator_name):
    """Return the mass dimension of a named operator/field."""
    if operator_name not in mass_dim:
        raise KeyError(f"Unknown operator '{operator_name}'. "
                       f"Available: {list(mass_dim.keys())}")
    return mass_dim[operator_name]

def dim_product(*operator_names):
    """
    Return the total mass dimension of a product of operators/fields.
    Example: dim_product('ricci_scalar', 'scalar_field', 'scalar_field') -> 4
    """
    return sum(dim_of(name) for name in operator_names)

# =========================================
# Generate all operators of a given mass dimension
# from building blocks {φ, Ric, Rie, R, ∇}
# (index contractions ignored at this stage)
#
# Building blocks and their mass dimensions:
#   φ    (scalar field)       : 1
#   ∇    (covariant deriv.)   : 1
#   R    (Ricci scalar)       : 2
#   Ric  (Ricci tensor)       : 2
#   Rie  (Riemann tensor)     : 2
# =========================================

from itertools import combinations_with_replacement

building_blocks = {
    'φ':   1,   # scalar field
    '∇':   1,   # covariant derivative
    'R':   2,   # Ricci scalar
    'Ric': 2,   # Ricci tensor
    'Rie': 2,   # Riemann tensor
}

def generate_operators(target_dim, blocks=building_blocks, max_derivatives=2):
    """
    Return all multisets of building blocks whose mass dimensions sum to target_dim,
    with the number of covariant derivatives (∇) <= max_derivatives.
    Each result is a tuple of block names (sorted), e.g. ('R',) or ('∇', 'φ').
    """
    names = list(blocks.keys())
    min_dim = min(blocks.values())
    max_objects = target_dim // min_dim

    results = []
    for n_objects in range(1, max_objects + 1):
        for combo in combinations_with_replacement(names, n_objects):
            if sum(blocks[b] for b in combo) == target_dim:
                if combo.count('∇') <= max_derivatives:
                    results.append(combo)
    return results

ops_dim2 = generate_operators(target_dim=2)

def print_operators(target_dim):
    ops = generate_operators(target_dim=target_dim)
    print(f"\n--- All dimension-{target_dim} operators (index structure ignored) ---")
    for i, combo in enumerate(ops, 1):
        expr = ' · '.join(combo)
        dim_str = ' + '.join(str(building_blocks[b]) for b in combo)
        total = sum(building_blocks[b] for b in combo)
        print(f"  {i:2d}.  {expr:30s}  dims: {dim_str} = {total}")
    print(f"  Total: {len(ops)} operators")

ops_dim2 = generate_operators(target_dim=2)
print_operators(2)

ops_dim3 = generate_operators(target_dim=3)
print_operators(3)

ops_dim4 = generate_operators(target_dim=4)
print_operators(4)

ops_dim5 = generate_operators(target_dim=5)
print_operators(5)

ops_dim6 = generate_operators(target_dim=6)
print_operators(6)

# =========================================
# 13. Contraction Engine v2
#
#  For every operator combination of a given mass-dimension:
#    (a) assign tensor indices following each factor's natural index type
#    (b) enumerate ALL ways to pair the free indices into contractions
#        - one upper + one lower  →  Kronecker delta (direct sum)
#        - both lower             →  insert g^{ab}  (raise with g_inv)
#        - both upper             →  insert g_{ab}  (lower with g)
#    (c) discard any term whose total free-index count is odd
#    (d) evaluate the resulting scalar in terms of a(t), N(t), φ(t)
#        and their derivatives
#
#  v2 changes:
#    - ∇ ordering:  (∇φ)(∇φ)  and  (∇∇φ)·φ  are distinct combos
#    - index labels: a, b, c, d, ... instead of Greek letters
#    - SUMMARY groups independent scalars properly, showing
#      all equivalent contractions (including same-combo ones)
# =========================================

import itertools
from copy import deepcopy

# =============================================
# PART A:  Index bookkeeping
# =============================================

class IndexSlot:
    """One index slot of a tensor."""
    __slots__ = ('name', 'up')
    def __init__(self, name: str, up: bool):
        self.name = name
        self.up = up
    def __repr__(self):
        arrow = '↑' if self.up else '↓'
        return f"{self.name}{arrow}"

class TensorBlock:
    """A tensor building block in an operator product.
    
    kind: one of 'scalar', 'Ric', 'Rie', 'nabla_scalar', 'nabla2_scalar',
          'nabla_R', 'nabla2_R', 'nabla_Ric', 'nabla_Rie'
    """
    def __init__(self, label, slots, data, kind='scalar'):
        self.label = label
        self.slots = list(slots)
        self.data  = data
        self.kind  = kind

    @property
    def rank(self):
        return len(self.slots)

    def __repr__(self):
        idx_str = ''.join(str(s) for s in self.slots)
        return f"{self.label}[{idx_str}]"

    def format_contracted(self, slot_map):
        """
        Format this tensor with indices replaced according to slot_map.
        
        slot_map: dict mapping original IndexSlot → (new_name, new_is_up)
        
        Returns a string like 'R^{c}_{cad}' or '∇^{a}φ' etc.
        """
        if self.rank == 0:
            return self.label
        
        # Build list of (new_name, new_is_up) in slot order
        indices = []
        for s in self.slots:
            if s in slot_map:
                indices.append(slot_map[s])
            else:
                indices.append((s.name, s.up))
        
        up_str = ''.join(name for name, is_up in indices if is_up)
        dn_str = ''.join(name for name, is_up in indices if not is_up)
        
        # Format based on tensor kind
        if self.kind == 'Ric':
            # Ricci tensor: originally R_{ab}
            if up_str and dn_str:
                return f"R^{{{up_str}}}_{{{dn_str}}}"
            elif up_str:
                return f"R^{{{up_str}}}"
            elif dn_str:
                return f"R_{{{dn_str}}}"
            else:
                return "R"
        
        elif self.kind == 'Rie':
            # Riemann tensor: originally R^a_{bcd}
            if up_str and dn_str:
                return f"R^{{{up_str}}}_{{{dn_str}}}"
            elif up_str:
                return f"R^{{{up_str}}}"
            elif dn_str:
                return f"R_{{{dn_str}}}"
            else:
                return "R"
        
        elif self.kind == 'nabla_scalar':
            # ∇_a φ  or  ∇_a R
            base = 'φ' if 'φ' in self.label else 'R'
            name, is_up = indices[0]
            if is_up:
                return f"∇^{{{name}}}{base}"
            else:
                return f"∇_{{{name}}}{base}"
        
        elif self.kind == 'nabla2_scalar':
            # ∇_a ∇_b φ  or  ∇_a ∇_b R
            base = 'φ' if 'φ' in self.label else 'R'
            n0, u0 = indices[0]
            n1, u1 = indices[1]
            s0 = f"^{{{n0}}}" if u0 else f"_{{{n0}}}"
            s1 = f"^{{{n1}}}" if u1 else f"_{{{n1}}}"
            return f"∇{s0}∇{s1}{base}"
        
        elif self.kind == 'nabla_Ric':
            # ∇_c R_{ab}: slots = [a(dn), b(dn), c(dn)]
            # First two are Ricci indices, third is ∇ index
            ric_indices = indices[:2]
            nabla_idx = indices[2]
            
            ric_up = ''.join(n for n, u in ric_indices if u)
            ric_dn = ''.join(n for n, u in ric_indices if not u)
            nname, nup = nabla_idx
            ns = f"^{{{nname}}}" if nup else f"_{{{nname}}}"
            
            if ric_up and ric_dn:
                return f"∇{ns}R^{{{ric_up}}}_{{{ric_dn}}}"
            elif ric_up:
                return f"∇{ns}R^{{{ric_up}}}"
            elif ric_dn:
                return f"∇{ns}R_{{{ric_dn}}}"
            else:
                return f"∇{ns}R"
        
        elif self.kind == 'nabla_Rie':
            # ∇_e R^a_{bcd}: slots = [a(up), b(dn), c(dn), d(dn), e(dn)]
            rie_indices = indices[:4]
            nabla_idx = indices[4]
            
            rie_up = ''.join(n for n, u in rie_indices if u)
            rie_dn = ''.join(n for n, u in rie_indices if not u)
            nname, nup = nabla_idx
            ns = f"^{{{nname}}}" if nup else f"_{{{nname}}}"
            
            if rie_up and rie_dn:
                return f"∇{ns}R^{{{rie_up}}}_{{{rie_dn}}}"
            elif rie_up:
                return f"∇{ns}R^{{{rie_up}}}"
            elif rie_dn:
                return f"∇{ns}R_{{{rie_dn}}}"
            else:
                return f"∇{ns}R"
        
        else:
            # Fallback: generic format
            if up_str and dn_str:
                return f"{self.label}^{{{up_str}}}_{{{dn_str}}}"
            elif up_str:
                return f"{self.label}^{{{up_str}}}"
            elif dn_str:
                return f"{self.label}_{{{dn_str}}}"
            else:
                return self.label


def get_element(arr, idx_tuple):
    """Get element from nested list by index tuple."""
    val = arr
    for i in idx_tuple:
        val = val[i]
    return val


# =============================================
# PART B:  Enumerate all perfect matchings
# =============================================

def all_perfect_matchings(indices):
    """
    Given a list of items, return all ways to partition them
    into unordered pairs.  len(indices) must be even.
    """
    nn = len(indices)
    if nn == 0:
        return [()]
    if nn % 2 != 0:
        return []
    first = indices[0]
    rest = indices[1:]
    result = []
    for i, partner in enumerate(rest):
        remaining = rest[:i] + rest[i+1:]
        for sub in all_perfect_matchings(remaining):
            result.append(((first, partner),) + sub)
    return result


# =============================================
# PART C:  Index counter  (a, b, c, d, ...)
# =============================================

_idx_counter = 0

def _fresh_idx():
    global _idx_counter
    letters = 'abcdefghijklmnopqrstuvwxyz'
    name = letters[_idx_counter % len(letters)]
    if _idx_counter >= len(letters):
        name += str(_idx_counter // len(letters))
    _idx_counter += 1
    return name

def reset_idx_counter():
    global _idx_counter
    _idx_counter = 0


# =============================================
# PART D:  Build TensorBlocks
# =============================================

def make_tensor_block(block_name, tensors_dict):
    """Create a TensorBlock for a named building block (not ∇)."""
    if block_name == 'φ':
        return TensorBlock('φ', [], tensors_dict['phi'], kind='scalar')
    elif block_name == 'R':
        return TensorBlock('R', [], tensors_dict['R_scalar'], kind='scalar')
    elif block_name == 'Ric':
        a, b = _fresh_idx(), _fresh_idx()
        slots = [IndexSlot(a, False), IndexSlot(b, False)]
        return TensorBlock(f'R_{{{a}{b}}}', slots, tensors_dict['Ricci'], kind='Ric')
    elif block_name == 'Rie':
        a, b, c, d = _fresh_idx(), _fresh_idx(), _fresh_idx(), _fresh_idx()
        slots = [IndexSlot(a, True), IndexSlot(b, False),
                 IndexSlot(c, False), IndexSlot(d, False)]
        return TensorBlock(f'R^{a}_{{{b}{c}{d}}}', slots, tensors_dict['Riemann'], kind='Rie')
    else:
        raise ValueError(f"Unknown block: {block_name}")


def _build_derivative_block(n_nabla, target, tensors_dict):
    """
    Build a single TensorBlock for ∇^n acting on target.
    Supported: ∇φ, ∇∇φ, ∇R, ∇∇R, ∇Ric, ∇Rie
    """
    cov_d = tensors_dict['cov_deriv']

    if target == 'φ':
        if n_nabla == 1:
            idx = _fresh_idx()
            data = [sp.diff(tensors_dict['phi'], c) for c in tensors_dict['coords']]
            return TensorBlock(f'∇_{idx}φ', [IndexSlot(idx, False)], data, kind='nabla_scalar')
        elif n_nabla == 2:
            nabla_phi = [sp.diff(tensors_dict['phi'], c) for c in tensors_dict['coords']]
            data = cov_d(nabla_phi, 0, 1)
            a, b = _fresh_idx(), _fresh_idx()
            return TensorBlock(f'∇_{a}∇_{b}φ',
                               [IndexSlot(a, False), IndexSlot(b, False)], data, kind='nabla2_scalar')
        else:
            raise NotImplementedError(f"{n_nabla} derivatives on φ")

    elif target == 'R':
        if n_nabla == 1:
            idx = _fresh_idx()
            data = [sp.simplify(sp.diff(tensors_dict['R_scalar'], c))
                    for c in tensors_dict['coords']]
            return TensorBlock(f'∇_{idx}R', [IndexSlot(idx, False)], data, kind='nabla_scalar')
        elif n_nabla == 2:
            nabla_R = [sp.simplify(sp.diff(tensors_dict['R_scalar'], c))
                       for c in tensors_dict['coords']]
            data = cov_d(nabla_R, 0, 1)
            a, b = _fresh_idx(), _fresh_idx()
            return TensorBlock(f'∇_{a}∇_{b}R',
                               [IndexSlot(a, False), IndexSlot(b, False)], data, kind='nabla2_scalar')
        else:
            raise NotImplementedError(f"{n_nabla} derivatives on R")

    elif target == 'Ric':
        if n_nabla == 1:
            data = cov_d(tensors_dict['Ricci'], 0, 2)
            a, b, c = _fresh_idx(), _fresh_idx(), _fresh_idx()
            return TensorBlock(f'∇_{c}R_{{{a}{b}}}',
                               [IndexSlot(a, False), IndexSlot(b, False),
                                IndexSlot(c, False)], data, kind='nabla_Ric')
        else:
            raise NotImplementedError(f"{n_nabla} derivatives on Ric")

    elif target == 'Rie':
        if n_nabla == 1:
            data = cov_d(tensors_dict['Riemann'], 1, 3)
            a, b, c, d, e = [_fresh_idx() for _ in range(5)]
            return TensorBlock(f'∇_{e}R^{a}_{{{b}{c}{d}}}',
                               [IndexSlot(a, True), IndexSlot(b, False),
                                IndexSlot(c, False), IndexSlot(d, False),
                                IndexSlot(e, False)], data, kind='nabla_Rie')
        else:
            raise NotImplementedError(f"{n_nabla} derivatives on Rie")

    else:
        raise ValueError(f"∇ acting on unknown target: {target}")


# =============================================
# PART E:  Generate structured combos  (∇ ordering aware)
#
#  Each combo is a list of (n_nabla, target) tuples.
#  e.g.  [(1,'φ'), (1,'φ')]  =  (∇φ)(∇φ)
#         [(2,'φ'), (0,'φ')]  =  (∇∇φ)·φ       ← distinct!
# =============================================

def _generate_structured_combos(target_dim, max_derivatives=2):
    """
    Generate all STRUCTURED operator combos whose mass dimensions sum
    to target_dim.  Each combo is a sorted list of (n_nabla, target)
    tuples so that e.g. (∇φ)(∇φ) and (∇∇φ)·φ are separate entries.
    """
    block_dims = {'φ': 1, 'R': 2, 'Ric': 2, 'Rie': 2}
    block_names = list(block_dims.keys())

    # All possible "augmented blocks": (n_nabla, target, total_dim)
    aug_blocks = []
    for name in block_names:
        for nd in range(max_derivatives + 1):
            dim = block_dims[name] + nd
            if dim <= target_dim:
                aug_blocks.append((nd, name, dim))

    results = []

    def search(remaining_dim, start_idx, current, total_nabla):
        if remaining_dim == 0:
            if len(current) > 0:
                results.append(list(current))
            return
        if remaining_dim < 0:
            return
        for i in range(start_idx, len(aug_blocks)):
            nd, name, dim = aug_blocks[i]
            if dim > remaining_dim:
                continue
            if total_nabla + nd > max_derivatives:
                continue
            current.append((nd, name))
            search(remaining_dim - dim, i, current, total_nabla + nd)
            current.pop()

    search(target_dim, 0, [], 0)
    return results


def combo_label(structured_combo):
    """Human-readable label for a structured combo."""
    parts = []
    for (nd, target) in structured_combo:
        if nd == 0:
            parts.append(target)
        elif nd == 1:
            parts.append(f'∇{target}')
        elif nd == 2:
            parts.append(f'∇∇{target}')
        else:
            parts.append(f'∇^{nd}{target}')
    return ' · '.join(parts)


def make_operator_blocks_v2(structured_combo, tensors_dict):
    """
    Given a structured combo like [(1,'φ'), (1,'φ')],
    build the list of TensorBlocks.
    """
    reset_idx_counter()
    blocks = []
    for (n_nabla, target) in structured_combo:
        if n_nabla == 0:
            blocks.append(make_tensor_block(target, tensors_dict))
        else:
            blocks.append(_build_derivative_block(n_nabla, target, tensors_dict))
    return blocks


# =============================================
# PART F:  Contract and evaluate
# =============================================

def contract_and_evaluate(blocks, tensors_dict, dim=4):
    """
    Evaluate all possible full index contractions of a tensor product.

    Optimizations for diagonal metrics (like FLRW):
      - Union-find: each contraction pair forces equal indices,
        reducing the loop from 4^N to 4^(N_free_groups)
      - Precompute nonzero tensor components, skip zeros early
    """
    nn = dim
    g_mat = tensors_dict['g']
    g_inv_mat = tensors_dict['g_inv']

    all_slots = []
    for bi, block in enumerate(blocks):
        for si, slot in enumerate(block.slots):
            all_slots.append((bi, si, slot))

    total_indices = len(all_slots)

    # Scalars
    if total_indices == 0:
        val = sp.Integer(1)
        for block in blocks:
            val *= block.data
        val = sp.simplify(val)
        label = ' · '.join(b.label for b in blocks)
        return [{'label': label, 'contraction': 'none (all scalars)', 'value': val}]

    # Odd → discard
    if total_indices % 2 != 0:
        label = ' · '.join(b.label for b in blocks)
        return [{'label': label, 'contraction': 'DISCARDED (odd indices)', 'value': None}]

    # ── Precompute: check if metric is diagonal ──
    is_diagonal = all(g_mat[i, j] == 0 for i in range(nn) for j in range(nn) if i != j)
    g_diag = [g_mat[i, i] for i in range(nn)]
    g_inv_diag = [g_inv_mat[i, i] for i in range(nn)]

    # ── Precompute: nonzero components per block ──
    block_nz = []
    for bi, block in enumerate(blocks):
        if block.rank == 0:
            block_nz.append(None)
        else:
            nz = {}
            for idx in itertools.product(range(nn), repeat=block.rank):
                v = get_element(block.data, idx)
                if v != 0:
                    nz[idx] = v
            block_nz.append(nz)

    # ── Precompute: which slots belong to which block ──
    block_slot_positions = {}  # bi -> list of global slot indices
    for k in range(total_indices):
        bi = all_slots[k][0]
        if bi not in block_slot_positions:
            block_slot_positions[bi] = []
        block_slot_positions[bi].append(k)

    # Enumerate all perfect matchings
    matchings = all_perfect_matchings(list(range(total_indices)))

    results = []
    seen_values = {}

    for matching in matchings:
        # ── Build contraction description ──
        contraction_parts = []
        for (i, j) in matching:
            si = all_slots[i][2]
            sj = all_slots[j][2]
            if si.up and sj.up:
                contraction_parts.append(f"g_{{{si.name}{sj.name}}}")
            elif (not si.up) and (not sj.up):
                contraction_parts.append(f"g^{{{si.name}{sj.name}}}")
            else:
                up_s = si if si.up else sj
                dn_s = sj if si.up else si
                contraction_parts.append(f"g^{{{up_s.name}}}_{{{dn_s.name}}}")
        contraction_str = ' · '.join(contraction_parts)

        # ── Build contracted expression label ──
        slot_map = {}
        for (i, j) in matching:
            si = all_slots[i][2]
            sj = all_slots[j][2]
            if si.up and sj.up:
                slot_map[si] = (si.name, False)
                slot_map[sj] = (si.name, True)
            elif (not si.up) and (not sj.up):
                slot_map[si] = (si.name, True)
                slot_map[sj] = (si.name, False)
            else:
                up_s = si if si.up else sj
                dn_s = sj if si.up else si
                slot_map[up_s] = (dn_s.name, True)
                slot_map[dn_s] = (dn_s.name, False)
        block_exprs = [b.format_contracted(slot_map) for b in blocks]
        contracted_expr = ' · '.join(block_exprs)

        # ── Evaluate ──
        if is_diagonal:
            # Union-find: all contraction pairs force equal indices
            parent = list(range(total_indices))
            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x
            def union(x, y):
                rx, ry = find(x), find(y)
                if rx != ry:
                    parent[rx] = ry

            for (i, j) in matching:
                union(i, j)

            groups = {}
            for k in range(total_indices):
                r = find(k)
                groups.setdefault(r, []).append(k)
            group_list = list(groups.values())
            n_free = len(group_list)

            val = sp.Integer(0)
            for free_vals in itertools.product(range(nn), repeat=n_free):
                idx_vals = [0] * total_indices
                for gi, gslots in enumerate(group_list):
                    for s in gslots:
                        idx_vals[s] = free_vals[gi]

                # Metric glue
                glue = sp.Integer(1)
                for (i, j) in matching:
                    si = all_slots[i][2]
                    sj = all_slots[j][2]
                    vi = idx_vals[i]
                    if si.up and sj.up:
                        glue *= g_diag[vi]
                    elif (not si.up) and (not sj.up):
                        glue *= g_inv_diag[vi]
                    # mixed: factor = 1
                if glue == 0:
                    continue

                # Tensor components
                term = glue
                skip = False
                for bi, block in enumerate(blocks):
                    if block.rank == 0:
                        term *= block.data
                    else:
                        bidx = tuple(idx_vals[k] for k in block_slot_positions[bi])
                        nz = block_nz[bi]
                        if bidx in nz:
                            term *= nz[bidx]
                        else:
                            skip = True
                            break
                if skip:
                    continue
                val += term

        else:
            # Non-diagonal fallback
            val = sp.Integer(0)
            for idx_vals in itertools.product(range(nn), repeat=total_indices):
                glue = sp.Integer(1)
                for (i, j) in matching:
                    si = all_slots[i][2]
                    sj = all_slots[j][2]
                    vi, vj = idx_vals[i], idx_vals[j]
                    if si.up and sj.up:
                        glue *= g_mat[vi, vj]
                    elif (not si.up) and (not sj.up):
                        glue *= g_inv_mat[vi, vj]
                    else:
                        if vi != vj:
                            glue = sp.Integer(0)
                            break
                if glue == 0:
                    continue
                term = glue
                skip = False
                for bi, block in enumerate(blocks):
                    if block.rank == 0:
                        term *= block.data
                    else:
                        bidx = tuple(idx_vals[k] for k in block_slot_positions[bi])
                        v = get_element(block.data, bidx)
                        if v == 0:
                            skip = True
                            break
                        term *= v
                if skip:
                    continue
                val += term

        val = sp.simplify(val)
        full_label = f"{contracted_expr}  [{contraction_str}]"

        val_key = str(val)
        if val_key in seen_values:
            results.append({'label': full_label, 'contraction': contraction_str,
                          'value': val, 'duplicate_of': seen_values[val_key]})
        else:
            seen_values[val_key] = full_label
            results.append({'label': full_label, 'contraction': contraction_str,
                          'value': val})

    return results



# =============================================
# PART G:  Main driver — process all combos for a given dim
# =============================================

def process_dimension(target_dim, tensors_dict, max_derivatives=2, verbose=True, tex_fn=None):
    """
    For a given target mass dimension:
      1. Generate all structured combos (with proper ∇ ordering)
      2. For each, build TensorBlocks, enumerate contractions, evaluate
      3. Collect and return all nonzero results with independence analysis

    Parameters
    ----------
    target_dim : int
    tensors_dict : dict with all precomputed tensors

    Returns
    -------
    all_results : list of dicts with 'combo', 'label', 'contraction', 'value'
    """
    _tex = tex_fn if tex_fn is not None else str

    combos = _generate_structured_combos(target_dim, max_derivatives)

    all_results = []

    if verbose:
        print(f"\n{'='*70}")
        print(f"PROCESSING DIMENSION {target_dim}")
        print(f"{'='*70}")
        print(f"Number of structured combos: {len(combos)}\n")

    for ci, scombo in enumerate(combos):
        clabel = combo_label(scombo)
        if verbose:
            print(f"--- Combo {ci+1}: {clabel} ---")

        try:
            blocks = make_operator_blocks_v2(scombo, tensors_dict)
        except NotImplementedError as e:
            if verbose:
                print(f"  SKIPPED: {e}\n")
            continue

        if verbose:
            print(f"  Blocks: {blocks}")
            total_idx = sum(b.rank for b in blocks)
            print(f"  Total indices: {total_idx}")

        results = contract_and_evaluate(blocks, tensors_dict)

        nonzero = [r for r in results if r['value'] is not None and r['value'] != 0]
        discarded = [r for r in results if r['value'] is None]
        zero = [r for r in results if r['value'] is not None and r['value'] == 0]

        if discarded:
            if verbose:
                print(f"  → DISCARDED (odd number of indices)")
        elif not nonzero:
            if verbose:
                print(f"  → All {len(zero)} contractions = 0")
        else:
            if verbose:
                print(f"  → {len(nonzero)} nonzero / {len(zero)} zero contractions:")
                for r in nonzero:
                    dup = "  [duplicate]" if 'duplicate_of' in r else ""
                    print(f"    {r['contraction']}")
                    print(f"      = {_tex(r['value'])}{dup}")

            for r in nonzero:
                r['combo'] = scombo
                r['combo_str'] = clabel
            all_results.extend(nonzero)

        if verbose:
            print()

    # ── Summary with proper independence grouping ──
    if verbose:
        print(f"\n{'='*70}")
        print(f"SUMMARY: Dim-{target_dim} nonzero scalar contractions")
        print(f"{'='*70}")

        # Group by proportionality
        groups = []  # each: {'representative': r, 'proportional': [(ratio, r), ...]}

        for r in all_results:
            found = False
            for grp in groups:
                ref = grp['representative']
                ratio = sp.simplify(r['value'] / ref['value'])
                if ratio.is_number:
                    grp['proportional'].append((ratio, r))
                    found = True
                    break
            if not found:
                groups.append({'representative': r, 'proportional': []})

        print(f"\n{'='*70}")
        print(f"INDEPENDENT non-zero Dim-{target_dim} curvature invariant")
        print(f"{'='*70}")
        print(f"  Total independent dim-{target_dim} scalars: {len(groups)}\n")

        for idx, grp in enumerate(groups, 1):
            rep = grp['representative']
            print(f"  ┌─ Independent scalar #{idx}")
            print(f"  │  Combo:       {rep['combo_str']}")
            print(f"  │  Contraction: {rep['contraction']}")
            print(f"  │  Expression:  {rep['label']}")
            print(f"  │  Value:       {_tex(rep['value'])}")

            if grp['proportional']:
                print(f"  │")
                print(f"  │  Equivalent contractions ({len(grp['proportional'])}):")
                for ratio, r in grp['proportional']:
                    sign = f"{_tex(ratio)} ×" if ratio != 1 else "same"
                    same = (r.get('combo_str', '') == rep['combo_str'])
                    origin = "same combo" if same else f"from {r['combo_str']}"
                    print(f"  │    • [{origin}] {r['contraction']}  ({sign})")

            print(f"  └{'─'*55}")

    return all_results


tensors_dict = {
    'g': g,
    'g_inv': g_inv,
    'Gamma': Gamma,
    'Riemann': Riemann,
    'Ricci': Ricci,
    'R_scalar': R_scalar,
    'phi': sp.Function('phi')(t),
    'coords': coords,
    'cov_deriv': cov_deriv,
}


results = process_dimension(2, tensors_dict, verbose=True, tex_fn=tex)
results_dim3 = process_dimension(3, tensors_dict, verbose=True, tex_fn=tex)
results_dim4 = process_dimension(4, tensors_dict, verbose=True, tex_fn=tex)
results_dim5 = process_dimension(5, tensors_dict, verbose=True, tex_fn=tex)
results_dim6 = process_dimension(6, tensors_dict, verbose=True, tex_fn=tex)

# ── Close log file ──
sys.stdout = sys.__stdout__
_log_fh.close()
print(f"[Log] Done. Output saved to: {_log_path}")