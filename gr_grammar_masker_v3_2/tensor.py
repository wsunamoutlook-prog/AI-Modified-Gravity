#!/usr/bin/env python3
"""FLRW tensor construction and contraction utilities for GR grammar masker v3.2."""

import itertools
import time as _time

import sympy as sp
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


# ╔═══════════════════════════════════════════════════════════════════╗
# ║               SECTION 1–6: TENSOR COMPUTATION                     ║
# ║   (Christoffel, Riemann, Ricci, R_scalar — unchanged)             ║
# ╚═══════════════════════════════════════════════════════════════════╝

t, x, y, z = sp.symbols('t x y z', real=True)
coords = [t, x, y, z]
n = len(coords)

N = sp.Function('N', positive=True)(t)
a = sp.Function('a', positive=True)(t)

g = sp.Matrix([
    [-N**2,    0,      0,      0],
    [0,     a**2,      0,      0],
    [0,        0,   a**2,      0],
    [0,        0,      0,   a**2]
])
g_inv = sp.simplify(g.inv())

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

Ricci = [[sp.Integer(0) for _ in range(n)] for _ in range(n)]
for mu in range(n):
    for nu in range(n):
        expr = sp.Integer(0)
        for rho in range(n):
            expr += Riemann[rho][mu][rho][nu]
        Ricci[mu][nu] = sp.simplify(expr)

R_scalar = sp.Integer(0)
for mu in range(n):
    for nu in range(n):
        R_scalar += g_inv[mu, nu] * Ricci[mu][nu]
R_scalar = sp.simplify(R_scalar)


# ╔═══════════════════════════════════════════════════════════════════╗
# ║            SECTION 10: COVARIANT DERIVATIVE  (unchanged)          ║
# ╚═══════════════════════════════════════════════════════════════════╝

def cov_deriv(T, p, q):
    """
    Covariant derivative of a rank-(p, q) tensor T.
    Result index order: [up_1,...,up_p, down_1,...,down_q, rho]
    """
    rank = p + q

    def get(arr, idx):
        for i in idx:
            arr = arr[i]
        return arr

    def set_(arr, idx, val):
        for i in idx[:-1]:
            arr = arr[i]
        arr[idx[-1]] = val

    def make_zeros(depth):
        if depth == 0:
            return sp.Integer(0)
        return [make_zeros(depth - 1) for _ in range(n)]

    DT = make_zeros(rank + 1)

    for idx in itertools.product(range(n), repeat=rank):
        mu_up = idx[:p]
        nu_dn = idx[p:]
        for rho in range(n):
            expr = sp.diff(get(T, idx), coords[rho])
            for i in range(p):
                for lam in range(n):
                    contracted_idx = mu_up[:i] + (lam,) + mu_up[i+1:] + nu_dn
                    expr += Gamma[mu_up[i]][rho][lam] * get(T, contracted_idx)
            for j in range(q):
                for lam in range(n):
                    contracted_idx = mu_up + nu_dn[:j] + (lam,) + nu_dn[j+1:]
                    expr -= Gamma[lam][rho][nu_dn[j]] * get(T, contracted_idx)
            set_(DT, idx + (rho,), sp.simplify(expr))

    return DT


# ╔═══════════════════════════════════════════════════════════════════╗
# ║         SECTION 10b: DERIVATIVE CACHE  (two scalar fields)        ║
# ╚═══════════════════════════════════════════════════════════════════╝

print("\n--- Precomputing derivative tensors (cached) ---")
_t0 = _time.time()

# --- phi1 derivatives ---
_nabla_phi1_data  = [sp.diff(sp.Function('phi1')(t), c) for c in coords]
_nabla2_phi1_data = cov_deriv(_nabla_phi1_data, 0, 1)

# --- phi2 derivatives ---
_nabla_phi2_data  = [sp.diff(sp.Function('phi2')(t), c) for c in coords]
_nabla2_phi2_data = cov_deriv(_nabla_phi2_data, 0, 1)

# --- curvature derivatives (unchanged) ---
_nabla_R_data    = [sp.simplify(sp.diff(R_scalar, c)) for c in coords]
_nabla2_R_data   = cov_deriv(_nabla_R_data, 0, 1)
_nabla_Ric_data  = cov_deriv(Ricci, 0, 2)
_nabla_Rie_data  = cov_deriv(Riemann, 1, 3)

print(f"  All derivative tensors cached. ({_time.time()-_t0:.1f}s)\n")

_deriv_cache = {
    ('nabla', 'phi1'):  _nabla_phi1_data,
    ('nabla2', 'phi1'): _nabla2_phi1_data,
    ('nabla', 'phi2'):  _nabla_phi2_data,
    ('nabla2', 'phi2'): _nabla2_phi2_data,
    ('nabla', 'R'):     _nabla_R_data,
    ('nabla2', 'R'):    _nabla2_R_data,
    ('nabla', 'Ric'):   _nabla_Ric_data,
    ('nabla', 'Rie'):   _nabla_Rie_data,
}


# ╔═══════════════════════════════════════════════════════════════════╗
# ║           SECTION 11: LEVI-CIVITA  (unchanged)                    ║
# ╚═══════════════════════════════════════════════════════════════════╝

def levi_civita_symbol(dim):
    def perm_sign(perm):
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

eps = levi_civita_symbol(n)
det_g   = sp.simplify(g.det())
sqrt_mg = sp.simplify(sp.sqrt(-det_g))

E_down = [[[[sp.simplify(sqrt_mg * eps[mu][nu][rho][sigma])
             for sigma in range(n)] for rho in range(n)]
           for nu in range(n)] for mu in range(n)]

E_up = [[[[sp.simplify(-eps[mu][nu][rho][sigma] / sqrt_mg)
           for sigma in range(n)] for rho in range(n)]
         for nu in range(n)] for mu in range(n)]


# ╔═══════════════════════════════════════════════════════════════════╗
# ║       CONTRACTION ENGINE: IndexSlot, TensorBlock, etc.            ║
# ║       (Parts A–F — updated for two scalar fields)                 ║
# ╚═══════════════════════════════════════════════════════════════════╝

# ── Part A: Index bookkeeping ──

class IndexSlot:
    __slots__ = ('name', 'up')
    def __init__(self, name: str, up: bool):
        self.name = name
        self.up = up
    def __repr__(self):
        arrow = '↑' if self.up else '↓'
        return f"{self.name}{arrow}"

class TensorBlock:
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
        if self.rank == 0:
            return self.label
        indices = []
        for s in self.slots:
            if s in slot_map:
                indices.append(slot_map[s])
            else:
                indices.append((s.name, s.up))
        up_str = ''.join(name for name, is_up in indices if is_up)
        dn_str = ''.join(name for name, is_up in indices if not is_up)

        if self.kind == 'Ric':
            if up_str and dn_str: return f"R^{{{up_str}}}_{{{dn_str}}}"
            elif up_str: return f"R^{{{up_str}}}"
            elif dn_str: return f"R_{{{dn_str}}}"
            else: return "R"
        elif self.kind == 'Rie':
            if up_str and dn_str: return f"R^{{{up_str}}}_{{{dn_str}}}"
            elif up_str: return f"R^{{{up_str}}}"
            elif dn_str: return f"R_{{{dn_str}}}"
            else: return "R"
        elif self.kind == 'nabla_scalar':
            # Determine base symbol: φ1, φ2, or R
            if 'φ1' in self.label:
                base = 'φ1'
            elif 'φ2' in self.label:
                base = 'φ2'
            else:
                base = 'R'
            name, is_up = indices[0]
            return f"∇^{{{name}}}{base}" if is_up else f"∇_{{{name}}}{base}"
        elif self.kind == 'nabla2_scalar':
            if 'φ1' in self.label:
                base = 'φ1'
            elif 'φ2' in self.label:
                base = 'φ2'
            else:
                base = 'R'
            n0, u0 = indices[0]
            n1, u1 = indices[1]
            s0 = f"^{{{n0}}}" if u0 else f"_{{{n0}}}"
            s1 = f"^{{{n1}}}" if u1 else f"_{{{n1}}}"
            return f"∇{s0}∇{s1}{base}"
        elif self.kind == 'nabla_Ric':
            ric_indices = indices[:2]
            nabla_idx = indices[2]
            ric_up = ''.join(n for n, u in ric_indices if u)
            ric_dn = ''.join(n for n, u in ric_indices if not u)
            nname, nup = nabla_idx
            ns = f"^{{{nname}}}" if nup else f"_{{{nname}}}"
            if ric_up and ric_dn: return f"∇{ns}R^{{{ric_up}}}_{{{ric_dn}}}"
            elif ric_up: return f"∇{ns}R^{{{ric_up}}}"
            elif ric_dn: return f"∇{ns}R_{{{ric_dn}}}"
            else: return f"∇{ns}R"
        elif self.kind == 'nabla_Rie':
            rie_indices = indices[:4]
            nabla_idx = indices[4]
            rie_up = ''.join(n for n, u in rie_indices if u)
            rie_dn = ''.join(n for n, u in rie_indices if not u)
            nname, nup = nabla_idx
            ns = f"^{{{nname}}}" if nup else f"_{{{nname}}}"
            if rie_up and rie_dn: return f"∇{ns}R^{{{rie_up}}}_{{{rie_dn}}}"
            elif rie_up: return f"∇{ns}R^{{{rie_up}}}"
            elif rie_dn: return f"∇{ns}R_{{{rie_dn}}}"
            else: return f"∇{ns}R"
        else:
            if up_str and dn_str: return f"{self.label}^{{{up_str}}}_{{{dn_str}}}"
            elif up_str: return f"{self.label}^{{{up_str}}}"
            elif dn_str: return f"{self.label}_{{{dn_str}}}"
            else: return self.label


def get_element(arr, idx_tuple):
    val = arr
    for i in idx_tuple:
        val = val[i]
    return val


# ── Part B: Perfect matchings ──

def all_perfect_matchings(indices):
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


# ── Part C: Index counter ──

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


# ── Part D: Build TensorBlocks (updated for two scalars) ──

def make_tensor_block(block_name, tensors_dict):
    if block_name == 'φ1':
        return TensorBlock('φ1', [], tensors_dict['phi1'], kind='scalar')
    elif block_name == 'φ2':
        return TensorBlock('φ2', [], tensors_dict['phi2'], kind='scalar')
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
    if target == 'φ1':
        if n_nabla == 1:
            idx = _fresh_idx()
            data = _deriv_cache[('nabla', 'phi1')]
            return TensorBlock(f'∇_{idx}φ1', [IndexSlot(idx, False)], data, kind='nabla_scalar')
        elif n_nabla == 2:
            a, b = _fresh_idx(), _fresh_idx()
            data = _deriv_cache[('nabla2', 'phi1')]
            return TensorBlock(f'∇_{a}∇_{b}φ1',
                               [IndexSlot(a, False), IndexSlot(b, False)], data, kind='nabla2_scalar')
        else:
            raise NotImplementedError(f"{n_nabla} derivatives on φ1")
    elif target == 'φ2':
        if n_nabla == 1:
            idx = _fresh_idx()
            data = _deriv_cache[('nabla', 'phi2')]
            return TensorBlock(f'∇_{idx}φ2', [IndexSlot(idx, False)], data, kind='nabla_scalar')
        elif n_nabla == 2:
            a, b = _fresh_idx(), _fresh_idx()
            data = _deriv_cache[('nabla2', 'phi2')]
            return TensorBlock(f'∇_{a}∇_{b}φ2',
                               [IndexSlot(a, False), IndexSlot(b, False)], data, kind='nabla2_scalar')
        else:
            raise NotImplementedError(f"{n_nabla} derivatives on φ2")
    elif target == 'R':
        if n_nabla == 1:
            idx = _fresh_idx()
            data = _deriv_cache[('nabla', 'R')]
            return TensorBlock(f'∇_{idx}R', [IndexSlot(idx, False)], data, kind='nabla_scalar')
        elif n_nabla == 2:
            a, b = _fresh_idx(), _fresh_idx()
            data = _deriv_cache[('nabla2', 'R')]
            return TensorBlock(f'∇_{a}∇_{b}R',
                               [IndexSlot(a, False), IndexSlot(b, False)], data, kind='nabla2_scalar')
        else:
            raise NotImplementedError(f"{n_nabla} derivatives on R")
    elif target == 'Ric':
        if n_nabla == 1:
            data = _deriv_cache[('nabla', 'Ric')]
            a, b, c = _fresh_idx(), _fresh_idx(), _fresh_idx()
            return TensorBlock(f'∇_{c}R_{{{a}{b}}}',
                               [IndexSlot(a, False), IndexSlot(b, False),
                                IndexSlot(c, False)], data, kind='nabla_Ric')
        else:
            raise NotImplementedError(f"{n_nabla} derivatives on Ric")
    elif target == 'Rie':
        if n_nabla == 1:
            data = _deriv_cache[('nabla', 'Rie')]
            a, b, c, d, e = [_fresh_idx() for _ in range(5)]
            return TensorBlock(f'∇_{e}R^{a}_{{{b}{c}{d}}}',
                               [IndexSlot(a, True), IndexSlot(b, False),
                                IndexSlot(c, False), IndexSlot(d, False),
                                IndexSlot(e, False)], data, kind='nabla_Rie')
        else:
            raise NotImplementedError(f"{n_nabla} derivatives on Rie")
    else:
        raise ValueError(f"∇ acting on unknown target: {target}")


def make_operator_blocks_from_combo(structured_combo, tensors_dict):
    """Given a structured combo [(n_nabla, target), ...], build TensorBlocks."""
    reset_idx_counter()
    blocks = []
    for (n_nabla, target) in structured_combo:
        if n_nabla == 0:
            blocks.append(make_tensor_block(target, tensors_dict))
        else:
            blocks.append(_build_derivative_block(n_nabla, target, tensors_dict))
    return blocks


# ── Part F: Contract and evaluate (updated numeric probes for two scalars) ──

def contract_and_evaluate(blocks, tensors_dict, dim=4):
    nn = dim
    g_mat = tensors_dict['g']
    g_inv_mat = tensors_dict['g_inv']

    all_slots = []
    for bi, block in enumerate(blocks):
        for si, slot in enumerate(block.slots):
            all_slots.append((bi, si, slot))

    total_indices = len(all_slots)

    if total_indices == 0:
        val = sp.Integer(1)
        for block in blocks:
            val *= block.data
        val = sp.simplify(val)
        label = ' · '.join(b.label for b in blocks)
        return [{'label': label, 'contraction': 'none (all scalars)', 'value': val}]

    if total_indices % 2 != 0:
        label = ' · '.join(b.label for b in blocks)
        return [{'label': label, 'contraction': 'DISCARDED (odd indices)', 'value': None}]

    is_diagonal = all(g_mat[i, j] == 0 for i in range(nn) for j in range(nn) if i != j)
    g_diag = [g_mat[i, i] for i in range(nn)]
    g_inv_diag = [g_inv_mat[i, i] for i in range(nn)]

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

    block_slot_positions = {}
    for k in range(total_indices):
        bi = all_slots[k][0]
        block_slot_positions.setdefault(bi, []).append(k)

    matchings = all_perfect_matchings(list(range(total_indices)))

    def _symbolic_eval(matching):
        if is_diagonal:
            parent = list(range(total_indices))
            def _find(xx):
                while parent[xx] != xx:
                    parent[xx] = parent[parent[xx]]
                    xx = parent[xx]
                return xx
            def _union(xx, yy):
                rx, ry = _find(xx), _find(yy)
                if rx != ry: parent[rx] = ry
            for (i, j) in matching:
                _union(i, j)
            groups = {}
            for k in range(total_indices):
                r = _find(k)
                groups.setdefault(r, []).append(k)
            group_list = list(groups.values())

            val = sp.Integer(0)
            for free_vals in itertools.product(range(nn), repeat=len(group_list)):
                idx_vals = [0] * total_indices
                for gi, gslots in enumerate(group_list):
                    for s in gslots:
                        idx_vals[s] = free_vals[gi]
                glue = sp.Integer(1)
                for (i, j) in matching:
                    si = all_slots[i][2]
                    sj = all_slots[j][2]
                    vi = idx_vals[i]
                    if si.up and sj.up:
                        glue *= g_diag[vi]
                    elif (not si.up) and (not sj.up):
                        glue *= g_inv_diag[vi]
                if glue == 0:
                    continue
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
        return sp.cancel(val)

    # ── Numeric probe for matching dedup ──
    from sympy import Rational as _Rat
    _t_sym = tensors_dict['coords'][0]
    _sub1 = {
        sp.Function('N', positive=True): sp.Lambda(_t_sym, 2 + 3*_t_sym + 5*_t_sym**2),
        sp.Function('a', positive=True): sp.Lambda(_t_sym, 7 + 11*_t_sym + 13*_t_sym**2),
        sp.Function('phi1'): sp.Lambda(_t_sym, 17 + 19*_t_sym + 23*_t_sym**2),
        sp.Function('phi2'): sp.Lambda(_t_sym, 29 + 31*_t_sym + 37*_t_sym**2),
    }

    def _to_float(expr):
        if not hasattr(expr, 'subs'):
            return float(expr)
        e = expr
        for func_obj, lam in _sub1.items():
            e = e.replace(func_obj, lam)
        e = e.doit()
        e = e.subs(_t_sym, _Rat(17, 10))
        return float(e)

    _num_block_nz = []
    for bi, block in enumerate(blocks):
        if block.rank == 0:
            _num_block_nz.append(_to_float(block.data) if block.data != 0 else 0.0)
        elif block_nz[bi] is not None:
            nd = {}
            for idx, v in block_nz[bi].items():
                nd[idx] = _to_float(v)
            _num_block_nz.append(nd)
        else:
            _num_block_nz.append(None)

    _num_g_diag = [_to_float(g_diag[i]) for i in range(nn)]
    _num_g_inv_diag = [_to_float(g_inv_diag[i]) for i in range(nn)]

    def _numeric_eval(matching):
        parent = list(range(total_indices))
        def _f(xx):
            while parent[xx] != xx:
                parent[xx] = parent[parent[xx]]
                xx = parent[xx]
            return xx
        def _u(xx, yy):
            rx, ry = _f(xx), _f(yy)
            if rx != ry: parent[rx] = ry
        for (i, j) in matching:
            _u(i, j)
        groups = {}
        for k in range(total_indices):
            r = _f(k)
            groups.setdefault(r, []).append(k)
        group_list = list(groups.values())

        val = 0.0
        for free_vals in itertools.product(range(nn), repeat=len(group_list)):
            idx_vals = [0] * total_indices
            for gi, gslots in enumerate(group_list):
                for s in gslots:
                    idx_vals[s] = free_vals[gi]
            glue = 1.0
            for (i, j) in matching:
                si = all_slots[i][2]
                sj = all_slots[j][2]
                vi = idx_vals[i]
                if si.up and sj.up:
                    glue *= _num_g_diag[vi]
                elif (not si.up) and (not sj.up):
                    glue *= _num_g_inv_diag[vi]
            if abs(glue) < 1e-15:
                continue
            term = glue
            skip = False
            for bi, block in enumerate(blocks):
                if block.rank == 0:
                    term *= _num_block_nz[bi]
                else:
                    bidx = tuple(idx_vals[k] for k in block_slot_positions[bi])
                    nd_map = _num_block_nz[bi]
                    if bidx in nd_map:
                        term *= nd_map[bidx]
                    else:
                        skip = True
                        break
            if skip:
                continue
            val += term
        return val

    _tol = 1e-10
    mi_to_rep = {}
    num_groups = {}
    for mi, matching in enumerate(matchings):
        nv = _numeric_eval(matching)
        found = False
        for rep_mi, rep_nv in num_groups.items():
            if abs(nv - rep_nv) < _tol:
                mi_to_rep[mi] = rep_mi
                found = True
                break
        if not found:
            num_groups[mi] = nv
            mi_to_rep[mi] = mi

    symbolic_cache = {}
    results = []
    seen_values = {}

    for mi, matching in enumerate(matchings):
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

        rep_mi = mi_to_rep[mi]
        if rep_mi in symbolic_cache:
            val = symbolic_cache[rep_mi]
        else:
            val = _symbolic_eval(matching)
            symbolic_cache[rep_mi] = val

        full_label = contracted_expr
        val_key = str(val)
        if val_key in seen_values:
            results.append({'label': full_label, 'contraction': contraction_str,
                          'value': val, 'duplicate_of': seen_values[val_key]})
        else:
            seen_values[val_key] = full_label
            results.append({'label': full_label, 'contraction': contraction_str,
                          'value': val})

    return results


# ╔═══════════════════════════════════════════════════════════════════╗
# ║                                                                   ║
# ║           GRAVITY MASKER — Grammar-Guided Generation              ║
# ║           (Updated for two scalar fields φ1, φ2)                  ║
# ║                                                                   ║
# ║  Token vocabulary:                                                ║
# ║    BOS        — begin of sequence                                 ║
# ║    EOS        — end of sequence (remaining_dim == 0)              ║
# ║    NABLA      — ∇  covariant derivative  (mass dim = 1)          ║
# ║    PHI1       — φ1 scalar field #1       (mass dim = 1)           ║
# ║    PHI2       — φ2 scalar field #2       (mass dim = 1)           ║
# ║    R_SCALAR   — R  Ricci scalar          (mass dim = 2)           ║
# ║    RIC        — R_{μν}  Ricci tensor     (mass dim = 2)           ║
# ║    RIE        — R^ρ_{σμν}  Riemann       (mass dim = 2)          ║
# ║                                                                   ║
# ║  Grammar:                                                        ║
# ║    sentence := BOS  block+  EOS                                  ║
# ║    block    := NABLA*  target                                    ║
# ║    target   := PHI1 | PHI2 | R_SCALAR | RIC | RIE                ║
# ║                                                                   ║
# ║  Constraints enforced by get_valid_tokens:                        ║
# ║    • Σ mass_dim(tokens) == target_dim                             ║
# ║    • total NABLA count ≤ max_derivatives                         ║
# ║    • blocks emitted in sorted order → no duplicate combos        ║
# ║    • total index count parity (odd → discard at eval stage)      ║
# ║                                                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝

# ── Vocabulary ──

