import sympy as sp
from functools import reduce
import sys
import os
from datetime import datetime
import itertools
import random
import time as _time
from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any

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
# =========================================
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
# ║         SECTION 10b: DERIVATIVE CACHE  (unchanged)                ║
# ╚═══════════════════════════════════════════════════════════════════╝

print("\n--- Precomputing derivative tensors (cached) ---")
_t0 = _time.time()

_nabla_phi_data  = [sp.diff(sp.Function('phi')(t), c) for c in coords]
_nabla2_phi_data = cov_deriv(_nabla_phi_data, 0, 1)
_nabla_R_data    = [sp.simplify(sp.diff(R_scalar, c)) for c in coords]
_nabla2_R_data   = cov_deriv(_nabla_R_data, 0, 1)
_nabla_Ric_data  = cov_deriv(Ricci, 0, 2)
_nabla_Rie_data  = cov_deriv(Riemann, 1, 3)

print(f"  All derivative tensors cached. ({_time.time()-_t0:.1f}s)\n")

_deriv_cache = {
    ('nabla', 'phi'):  _nabla_phi_data,
    ('nabla2', 'phi'): _nabla2_phi_data,
    ('nabla', 'R'):    _nabla_R_data,
    ('nabla2', 'R'):   _nabla2_R_data,
    ('nabla', 'Ric'):  _nabla_Ric_data,
    ('nabla', 'Rie'):  _nabla_Rie_data,
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
# ║       (Parts A–F from original — unchanged)                       ║
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
            base = 'φ' if 'φ' in self.label else 'R'
            name, is_up = indices[0]
            return f"∇^{{{name}}}{base}" if is_up else f"∇_{{{name}}}{base}"
        elif self.kind == 'nabla2_scalar':
            base = 'φ' if 'φ' in self.label else 'R'
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


# ── Part D: Build TensorBlocks ──

def make_tensor_block(block_name, tensors_dict):
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
    if target == 'φ':
        if n_nabla == 1:
            idx = _fresh_idx()
            data = _deriv_cache[('nabla', 'phi')]
            return TensorBlock(f'∇_{idx}φ', [IndexSlot(idx, False)], data, kind='nabla_scalar')
        elif n_nabla == 2:
            a, b = _fresh_idx(), _fresh_idx()
            data = _deriv_cache[('nabla2', 'phi')]
            return TensorBlock(f'∇_{a}∇_{b}φ',
                               [IndexSlot(a, False), IndexSlot(b, False)], data, kind='nabla2_scalar')
        else:
            raise NotImplementedError(f"{n_nabla} derivatives on φ")
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


# ── Part F: Contract and evaluate (unchanged) ──

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
        sp.Function('phi'): sp.Lambda(_t_sym, 17 + 19*_t_sym + 23*_t_sym**2),
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
# ║                                                                   ║
# ║  Token vocabulary:                                                ║
# ║    BOS        — begin of sequence                                 ║
# ║    EOS        — end of sequence (remaining_dim == 0)              ║
# ║    NABLA      — ∇  covariant derivative  (mass dim = 1)          ║
# ║    PHI        — φ  scalar field          (mass dim = 1)           ║
# ║    R_SCALAR   — R  Ricci scalar          (mass dim = 2)           ║
# ║    RIC        — R_{μν}  Ricci tensor     (mass dim = 2)           ║
# ║    RIE        — R^ρ_{σμν}  Riemann       (mass dim = 2)          ║
# ║                                                                   ║
# ║  Grammar:                                                        ║
# ║    sentence := BOS  block+  EOS                                  ║
# ║    block    := NABLA*  target                                    ║
# ║    target   := PHI | R_SCALAR | RIC | RIE                        ║
# ║                                                                   ║
# ║  Constraints enforced by get_valid_tokens:                        ║
# ║    • Σ mass_dim(tokens) == target_dim                             ║
# ║    • total NABLA count ≤ max_derivatives                         ║
# ║    • blocks emitted in sorted order → no duplicate combos        ║
# ║    • total index count parity (odd → discard at eval stage)      ║
# ║                                                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝

# ── Vocabulary ──

GRAMMAR_TOKENS = ['BOS', 'EOS', 'NABLA', 'PHI', 'R_SCALAR', 'RIC', 'RIE']

TARGETS     = ['PHI', 'R_SCALAR', 'RIC', 'RIE']
TARGET_DIM  = {'PHI': 1, 'R_SCALAR': 2, 'RIC': 2, 'RIE': 2}
TARGET_RANK = {'PHI': 0, 'R_SCALAR': 0, 'RIC': 2, 'RIE': 4}   # tensor rank (free indices)

# Canonical ordering index — used to enforce sorted blocks (no duplicate combos)
# Order mirrors the original: φ < R < Ric < Rie, and within each target lower ∇ first
TARGET_ORDER = {'PHI': 0, 'R_SCALAR': 1, 'RIC': 2, 'RIE': 3}

# Maps masker tokens back to the names used by make_tensor_block / _build_derivative_block
TOKEN_TO_BLOCK = {'PHI': 'φ', 'R_SCALAR': 'R', 'RIC': 'Ric', 'RIE': 'Rie'}

token2id = {tok: i for i, tok in enumerate(GRAMMAR_TOKENS)}
id2token = {i: tok for i, tok in enumerate(GRAMMAR_TOKENS)}


# ── State ──

@dataclass
class GravityState:
    """Tracks the sequential generation of one operator combo."""
    target_dim:         int              # the mass dimension we are building toward
    max_derivatives:    int = 2          # global cap on total ∇ count
    remaining_dim:      int = 0          # mass dimension budget left
    total_nabla:        int = 0          # ∇ used so far across all blocks
    current_block_nabla: int = 0         # ∇ accumulated in the block being built
    completed_blocks:   list = field(default_factory=list)   # [(n_nabla, target_name), ...]
    last_token:         Optional[str] = None
    length:             int = 0          # tokens generated so far

    def __post_init__(self):
        self.remaining_dim = self.target_dim


# ── Lagrangian building blocks ──

Mp = sp.Symbol('M_p', positive=True)          # Planck mass (mass dim = 1)
m_phi = sp.Symbol('m', positive=True)         # scalar field mass

_GREEK_COEFFS = [sp.Symbol(g) for g in
    [r'\alpha', r'\beta', r'\gamma', r'\delta',
     r'\epsilon', r'\zeta', r'\eta', r'\theta']]

@dataclass
class CandidateScalar:
    """One independent curvature/field invariant ready for Lagrangian use."""
    mass_dim: int              # mass dimension of this scalar
    combo_label: str           # human-readable e.g. 'Ric · Ric'
    contraction_label: str     # e.g. 'R^{ab}_{ab} · ...'
    symbolic_value: Any        # sympy expression (metric-substituted)
    general_label: str         # token/index notation (NOT substituted)


# ── Masker ──

class GravityMasker:
    """
    Grammar-guided masker for modified-gravity Lagrangian operators.

    Analogous to GrammarMasker in the BSM particle-physics project:
      • init_state(target_dim)  →  fresh GravityState
      • step(state, token)      →  updated GravityState  (state machine transition)
      • get_valid_tokens(state, token) → list[str]  (legal next tokens)
      • generate_all_combos(target_dim) → list of structured combos via DFS
      • process_dimension(target_dim, tensors_dict) → full evaluation pipeline
    """

    def __init__(self, max_derivatives=2):
        self.max_derivatives = max_derivatives

    # ────────────────────────────────────────
    #  State management
    # ────────────────────────────────────────

    def init_state(self, target_dim: int) -> GravityState:
        return GravityState(target_dim=target_dim, max_derivatives=self.max_derivatives)

    def step(self, state: GravityState, token: str) -> GravityState:
        """Advance the state machine by one token."""

        if token == 'BOS':
            pass  # nothing to update

        elif token == 'NABLA':
            state.current_block_nabla += 1
            state.total_nabla += 1
            state.remaining_dim -= 1

        elif token in TARGETS:
            # A target token finalises the current block
            state.remaining_dim -= TARGET_DIM[token]
            block = (state.current_block_nabla, TOKEN_TO_BLOCK[token])
            state.completed_blocks.append(block)
            state.current_block_nabla = 0

        elif token == 'EOS':
            pass  # sequence complete

        state.last_token = token
        state.length += 1
        return state

    # ────────────────────────────────────────
    #  Grammar mask
    # ────────────────────────────────────────

    def get_valid_tokens(self, state: GravityState, token: str) -> List[str]:
        """Return all tokens that are legal after `token` in the current state."""

        if token == 'BOS':
            return self._valid_block_starters(state)

        elif token == 'NABLA':
            # Can do more NABLA or commit a target
            valid = []
            # More NABLA?
            if self._can_add_nabla(state):
                valid.append('NABLA')
            # Targets that fit with current nabla count
            for t in TARGETS:
                if self._target_fits(state, t) and self._block_ge_last(state, state.current_block_nabla, t):
                    valid.append(t)
            return valid

        elif token in TARGETS:
            # Just completed a block.  Start next block or finish.
            if state.remaining_dim == 0:
                return ['EOS']
            return self._valid_block_starters(state)

        elif token == 'EOS':
            return []  # done

        return []

    # ────────────────────────────────────────
    #  Internal helpers
    # ────────────────────────────────────────

    def _block_order_key(self, n_nabla: int, target_token: str) -> Tuple[int, int]:
        """
        Canonical ordering key for a block (n_nabla, target).
        Matches the original aug_blocks enumeration order:
          for target in [φ, R, Ric, Rie]:
              for nd in [0, 1, 2, ...]:
                  ...
        So the sort key is (target_order, n_nabla).
        """
        return (TARGET_ORDER[target_token], n_nabla)

    def _last_block_key(self, state: GravityState) -> Optional[Tuple[int, int]]:
        """Order key of the most recently completed block, or None."""
        if not state.completed_blocks:
            return None
        n, blk_name = state.completed_blocks[-1]
        # blk_name is in original notation ('φ', 'R', 'Ric', 'Rie')
        # convert back to token
        blk_to_tok = {v: k for k, v in TOKEN_TO_BLOCK.items()}
        return (TARGET_ORDER[blk_to_tok[blk_name]], n)

    def _block_ge_last(self, state: GravityState, n_nabla: int, target_token: str) -> bool:
        """Is (n_nabla, target) >= the last completed block in canonical order?"""
        last = self._last_block_key(state)
        if last is None:
            return True
        return self._block_order_key(n_nabla, target_token) >= last

    def _target_fits(self, state: GravityState, target_token: str) -> bool:
        """Does the target's mass dimension fit in the remaining budget?"""
        return TARGET_DIM[target_token] <= state.remaining_dim

    def _can_add_nabla(self, state: GravityState) -> bool:
        """Can we add another NABLA?  Need: under budget, dim room for a target after."""
        if state.total_nabla >= state.max_derivatives:
            return False
        # After adding one more NABLA, remaining_dim drops by 1.
        # There must still be room for at least one target (min target dim = 1 for PHI).
        if state.remaining_dim - 1 < 1:
            return False
        # Also check that at least one valid block exists after adding NABLA
        future_nabla = state.current_block_nabla + 1
        for t in TARGETS:
            if TARGET_DIM[t] <= state.remaining_dim - 1:
                if self._block_ge_last(state, future_nabla, t):
                    return True
        return False

    def _valid_block_starters(self, state: GravityState) -> List[str]:
        """
        Tokens that can start a new block: NABLA or a direct TARGET.
        Enforces sorted-order and dimension constraints.
        """
        valid = []

        # NABLA to start a new block?
        if self._can_add_nabla(state):
            valid.append('NABLA')

        # Direct targets (n_nabla = 0 for the new block)
        for t in TARGETS:
            if self._target_fits(state, t) and self._block_ge_last(state, 0, t):
                valid.append(t)

        return valid

    # ────────────────────────────────────────
    #  Combo generation via DFS over the grammar
    # ────────────────────────────────────────

    def generate_all_combos(self, target_dim: int) -> List[List[Tuple[int, str]]]:
        """
        Generate all valid structured combos for the given target mass dimension.
        Returns list of [(n_nabla, block_name), ...] in original notation.

        Replaces _generate_structured_combos() from the original code,
        but uses the masker grammar to ensure correctness.
        """
        results = []

        def _dfs(state: GravityState, token_seq: List[str]):
            last = state.last_token if state.last_token else 'BOS'
            valid = self.get_valid_tokens(state, last)

            for tok in valid:
                new_state = deepcopy(state)
                self.step(new_state, tok)

                if tok == 'EOS':
                    # Completed — extract the structured combo
                    results.append(list(new_state.completed_blocks))
                else:
                    _dfs(new_state, token_seq + [tok])

        init = self.init_state(target_dim)
        self.step(init, 'BOS')
        _dfs(init, ['BOS'])

        return results

    # ────────────────────────────────────────
    #  Token sequence → structured combo
    # ────────────────────────────────────────

    def tokens_to_combo(self, token_seq: List[str]) -> List[Tuple[int, str]]:
        """Convert a token sequence [BOS, ..., EOS] to a structured combo."""
        state = self.init_state(0)  # target_dim doesn't matter for conversion
        combo = []
        current_nabla = 0
        for tok in token_seq:
            if tok == 'NABLA':
                current_nabla += 1
            elif tok in TARGETS:
                combo.append((current_nabla, TOKEN_TO_BLOCK[tok]))
                current_nabla = 0
        return combo

    def combo_to_tokens(self, combo: List[Tuple[int, str]]) -> List[str]:
        """Convert a structured combo to a token sequence."""
        blk_to_tok = {v: k for k, v in TOKEN_TO_BLOCK.items()}
        tokens = ['BOS']
        for (nd, target) in combo:
            tokens.extend(['NABLA'] * nd)
            tokens.append(blk_to_tok[target])
        tokens.append('EOS')
        return tokens

    # ────────────────────────────────────────
    #  Combo label (human-readable)
    # ────────────────────────────────────────

    @staticmethod
    def combo_label(structured_combo: List[Tuple[int, str]]) -> str:
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

    # ────────────────────────────────────────
    #  Full evaluation pipeline
    # ────────────────────────────────────────

    def process_dimension(self, target_dim: int, tensors_dict: dict,
                          verbose: bool = True, tex_fn=None) -> list:
        """
        For a given target mass dimension:
          1. Generate all structured combos via the grammar DFS
          2. For each combo: build TensorBlocks, enumerate contractions, evaluate
          3. Collect nonzero results and analyse independence

        Replaces process_dimension() from the original code.
        """
        _tex = tex_fn if tex_fn is not None else str

        combos = self.generate_all_combos(target_dim)

        all_results = []

        if verbose:
            print(f"\n{'='*70}")
            print(f"PROCESSING DIMENSION {target_dim}")
            print(f"  Generated {len(combos)} structured combos via grammar DFS")
            print(f"{'='*70}")

        for ci, scombo in enumerate(combos):
            clabel = self.combo_label(scombo)

            try:
                blocks = make_operator_blocks_from_combo(scombo, tensors_dict)
            except NotImplementedError:
                continue

            results = contract_and_evaluate(blocks, tensors_dict)
            nonzero = [r for r in results if r['value'] is not None and r['value'] != 0]

            if nonzero:
                for r in nonzero:
                    r['combo'] = scombo
                    r['combo_str'] = clabel
                all_results.extend(nonzero)

        # ── Independence analysis (same logic as original) ──
        if verbose:
            groups = []

            from sympy import Rational as _Rat
            _t_sym_s = tensors_dict['coords'][0]
            _sub1_s = {
                sp.Function('N', positive=True): sp.Lambda(_t_sym_s, 2 + 3*_t_sym_s + 5*_t_sym_s**2),
                sp.Function('a', positive=True): sp.Lambda(_t_sym_s, 7 + 11*_t_sym_s + 13*_t_sym_s**2),
                sp.Function('phi'): sp.Lambda(_t_sym_s, 17 + 19*_t_sym_s + 23*_t_sym_s**2),
            }
            def _val_to_float(expr):
                if expr == 0:
                    return 0.0
                e = expr
                for func_obj, lam in _sub1_s.items():
                    e = e.replace(func_obj, lam)
                e = e.doit().subs(_t_sym_s, _Rat(17, 10))
                return float(e)

            _num_results = [_val_to_float(r['value']) for r in all_results]
            _tol_s = 1e-10

            for ri, r in enumerate(all_results):
                nv = _num_results[ri]
                found = False
                for grp in groups:
                    ref_ri = all_results.index(grp['representative'])
                    ref_nv = _num_results[ref_ri]
                    if abs(ref_nv) < _tol_s:
                        continue
                    num_ratio = nv / ref_nv
                    if (abs(num_ratio - round(num_ratio)) < _tol_s or
                        abs(num_ratio * 2 - round(num_ratio * 2)) < _tol_s or
                        abs(num_ratio * 3 - round(num_ratio * 3)) < _tol_s or
                        abs(num_ratio * 4 - round(num_ratio * 4)) < _tol_s or
                        abs(num_ratio * 6 - round(num_ratio * 6)) < _tol_s or
                        abs(num_ratio * 12 - round(num_ratio * 12)) < _tol_s):
                        ratio = sp.cancel(r['value'] / grp['representative']['value'])
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
                print(f"  │  Expression:  {rep['label']}")
                print(f"  │  Value:       {_tex(rep['value'])}")
                print(f"  └{'─'*55}")

        return all_results

    # ────────────────────────────────────────
    #  Lagrangian generation — candidate collection
    # ────────────────────────────────────────

    def collect_candidates(self, tensors_dict: dict,
                           dims: Tuple[int, ...] = (2, 3, 4, 5, 6),
                           tex_fn=None) -> Dict[int, List[CandidateScalar]]:
        """
        Run process_dimension for each dim, do independence analysis,
        return dict: mass_dim → list of CandidateScalar.
        Also stores results in self.candidates_by_dim / self.all_candidates.
        """
        _tex = tex_fn if tex_fn is not None else str
        from sympy import Rational as _Rat

        _t_sym_c = tensors_dict['coords'][0]
        _sub_c = {
            sp.Function('N', positive=True): sp.Lambda(_t_sym_c, 2 + 3*_t_sym_c + 5*_t_sym_c**2),
            sp.Function('a', positive=True): sp.Lambda(_t_sym_c, 7 + 11*_t_sym_c + 13*_t_sym_c**2),
            sp.Function('phi'): sp.Lambda(_t_sym_c, 17 + 19*_t_sym_c + 23*_t_sym_c**2),
        }
        def _val(expr):
            if expr == 0: return 0.0
            e = expr
            for f, lam in _sub_c.items():
                e = e.replace(f, lam)
            return float(e.doit().subs(_t_sym_c, _Rat(17, 10)))

        candidates_by_dim = {}

        print("\n" + "="*70)
        print("COLLECTING CANDIDATE INVARIANTS FOR LAGRANGIAN GENERATION")
        print("="*70)

        for d in dims:
            all_results = self.process_dimension(d, tensors_dict,
                                                  verbose=False, tex_fn=_tex)
            # Independence filter
            groups = []
            num_vals = [_val(r['value']) for r in all_results]
            _tol = 1e-10
            for ri, r in enumerate(all_results):
                nv = num_vals[ri]
                found = False
                for grp in groups:
                    ref_ri = all_results.index(grp['rep'])
                    ref_nv = num_vals[ref_ri]
                    if abs(ref_nv) < _tol: continue
                    ratio = nv / ref_nv
                    if (abs(ratio - round(ratio)) < _tol or
                        abs(ratio*2 - round(ratio*2)) < _tol or
                        abs(ratio*3 - round(ratio*3)) < _tol or
                        abs(ratio*4 - round(ratio*4)) < _tol or
                        abs(ratio*6 - round(ratio*6)) < _tol or
                        abs(ratio*12 - round(ratio*12)) < _tol):
                        sym_ratio = sp.cancel(r['value'] / grp['rep']['value'])
                        if sym_ratio.is_number:
                            found = True
                            break
                if not found:
                    groups.append({'rep': r})

            cands = []
            for grp in groups:
                rep = grp['rep']
                if rep['value'] is None or rep['value'] == 0:
                    continue
                cands.append(CandidateScalar(
                    mass_dim=d,
                    combo_label=rep.get('combo_str', ''),
                    contraction_label=rep['label'],
                    symbolic_value=rep['value'],
                    general_label=rep['label'],
                ))
            candidates_by_dim[d] = cands
            print(f"  dim={d}: {len(cands)} independent candidates")

        self.candidates_by_dim = candidates_by_dim
        self.all_candidates = []
        for d in sorted(candidates_by_dim):
            self.all_candidates.extend(candidates_by_dim[d])
        print(f"\n  Total candidate pool: {len(self.all_candidates)} independent scalars\n")

        return candidates_by_dim

    # ────────────────────────────────────────
    #  Lagrangian generation — random sampling
    # ────────────────────────────────────────

    @staticmethod
    def _random_coeff():
        """Log-uniform random coefficient in [10^-5, 10^5], random sign."""
        log_val = random.uniform(-5, 5)
        sign = random.choice([-1, 1])
        return sign * 10**log_val

    @staticmethod
    def _pad_mp(mass_dim_of_term: int) -> int:
        """Power of Mp needed to bring a term to mass dim 4."""
        return 4 - mass_dim_of_term

    def generate_lagrangians(self, tensors_dict: dict,
                             n_terms_list: Tuple[int, ...] = (1,2,3,4,5,6,7,8),
                             n_samples: int = 100,
                             seed: int = 42) -> Dict[int, list]:
        """
        Generate random Lagrangians from the collected candidate pool.
        Must call collect_candidates() first.

        Returns dict: n_terms → list of Lagrangian dicts, each with:
          - 'general':     string with tokens/indices (no metric substitution)
          - 'substituted': sympy expression fully substituted into FLRW
          - 'terms':       list of individual term info
          - 'has_phi':     whether scalar-field kinetic/mass terms are included
        """
        if not hasattr(self, 'all_candidates') or not self.all_candidates:
            raise RuntimeError("Call collect_candidates() before generate_lagrangians()")

        all_cands = self.all_candidates
        phi_func = tensors_dict['phi']
        phi_dot = sp.Derivative(phi_func, tensors_dict['coords'][0])

        # Pre-built scalar-field supplement terms (metric-substituted)
        N_func = tensors_dict['g'][0, 0]   # = -N²;  N = sqrt(-g_00)
        kinetic_value = sp.Rational(-1, 2) * phi_dot**2 / sp.Function('N', positive=True)(tensors_dict['coords'][0])**2
        kinetic_general = "½ g^{μν} ∇_μφ ∇_νφ"
        mass_value = sp.Rational(-1, 2) * m_phi**2 * phi_func**2
        mass_general = "-½ m² φ²"

        random.seed(seed)
        results = {}

        for n_total in n_terms_list:
            print(f"\n{'─'*60}")
            print(f"  Generating {n_samples} Lagrangians with {n_total} total terms")
            print(f"{'─'*60}")

            lagrangians = []
            seen_combos = set()
            max_attempts = n_samples * 50

            attempts = 0
            while len(lagrangians) < n_samples and attempts < max_attempts:
                attempts += 1

                # Pick n_total candidate terms randomly
                if n_total <= len(all_cands):
                    chosen = random.sample(all_cands, n_total)
                else:
                    chosen = [random.choice(all_cands) for _ in range(n_total)]

                # Check if any term involves φ
                has_phi = any('φ' in c.combo_label or 'phi' in str(c.symbolic_value)
                              for c in chosen)

                if has_phi:
                    if n_total < 3:
                        # Not enough room for kinetic+mass; retry without φ
                        non_phi = [c for c in all_cands
                                   if 'φ' not in c.combo_label
                                   and 'phi' not in str(c.symbolic_value)]
                        if not non_phi:
                            continue
                        chosen = (random.sample(non_phi, n_total)
                                  if n_total <= len(non_phi)
                                  else [random.choice(non_phi) for _ in range(n_total)])
                        has_phi = False
                    else:
                        n_curv = n_total - 2
                        chosen = (random.sample(all_cands, n_curv)
                                  if n_curv <= len(all_cands)
                                  else [random.choice(all_cands) for _ in range(n_curv)])

                # Dedup by structure
                fingerprint = tuple(sorted(c.contraction_label for c in chosen))
                fp_key = (has_phi, fingerprint)
                if fp_key in seen_combos:
                    continue
                seen_combos.add(fp_key)

                # Assign coefficients
                coeffs = []
                coeff_vals = []
                for i in range(len(chosen)):
                    sym = (_GREEK_COEFFS[i] if i < len(_GREEK_COEFFS)
                           else sp.Symbol(f'c_{{{i+1}}}'))
                    coeffs.append(sym)
                    coeff_vals.append(self._random_coeff())

                # Build general and substituted forms
                general_parts = []
                substituted_expr = sp.Integer(0)
                term_info = []

                for i, cand in enumerate(chosen):
                    mp_power = self._pad_mp(cand.mass_dim)
                    mp_factor = Mp**mp_power if mp_power != 0 else sp.Integer(1)
                    mp_str = f" M_p^{mp_power}" if mp_power != 0 else ""

                    general_parts.append(f"{coeffs[i]}{mp_str} · {cand.general_label}")
                    substituted_expr += coeff_vals[i] * mp_factor * cand.symbolic_value

                    term_info.append({
                        'coeff_symbol': str(coeffs[i]),
                        'coeff_value': coeff_vals[i],
                        'candidate': cand.contraction_label,
                        'mass_dim': cand.mass_dim,
                        'mp_power': mp_power,
                    })

                # Scalar-field kinetic + mass supplement
                if has_phi:
                    idx_k = len(term_info)
                    idx_m = idx_k + 1
                    ck_sym = (_GREEK_COEFFS[idx_k] if idx_k < len(_GREEK_COEFFS)
                              else sp.Symbol(f'c_{{{idx_k+1}}}'))
                    cm_sym = (_GREEK_COEFFS[idx_m] if idx_m < len(_GREEK_COEFFS)
                              else sp.Symbol(f'c_{{{idx_m+1}}}'))
                    ck_val = self._random_coeff()
                    cm_val = self._random_coeff()

                    general_parts.append(f"{ck_sym} · {kinetic_general}")
                    general_parts.append(f"{cm_sym} · {mass_general}")
                    substituted_expr += ck_val * kinetic_value
                    substituted_expr += cm_val * mass_value

                    term_info.append({
                        'coeff_symbol': str(ck_sym), 'coeff_value': ck_val,
                        'candidate': kinetic_general, 'mass_dim': 4, 'mp_power': 0})
                    term_info.append({
                        'coeff_symbol': str(cm_sym), 'coeff_value': cm_val,
                        'candidate': mass_general, 'mass_dim': 4, 'mp_power': 0})

                # Wrap with √(-g)
                general_str = "√(-g) [ " + "  +  ".join(general_parts) + " ]"
                substituted_full = sqrt_mg * substituted_expr

                lagrangians.append({
                    'n_terms': n_total,
                    'general': general_str,
                    'substituted': sp.simplify(substituted_full),
                    'terms': term_info,
                    'has_phi': has_phi,
                })

            print(f"    → Generated {len(lagrangians)} unique Lagrangians "
                  f"(from {attempts} attempts)")
            results[n_total] = lagrangians

        return results


# ╔═══════════════════════════════════════════════════════════════════╗
# ║                         MAIN DRIVER                               ║
# ╚═══════════════════════════════════════════════════════════════════╝

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

masker = GravityMasker(max_derivatives=2)

# ── Quick grammar sanity check ──
print("\n--- Grammar sanity check ---")
for d in range(2, 7):
    combos = masker.generate_all_combos(d)
    print(f"  dim={d}: {len(combos)} combos")
    for c in combos:
        print(f"    {masker.combo_label(c):40s}  tokens: {masker.combo_to_tokens(c)}")
print()

# ── Run evaluations (verbose, for log) ──
for d in (2, 3, 4, 5, 6):
    masker.process_dimension(d, tensors_dict, verbose=True, tex_fn=tex)

# ── Collect independent candidates ──
masker.collect_candidates(tensors_dict, dims=(2, 3, 4, 5, 6), tex_fn=tex)

# ── Generate Lagrangians ──
lagrangian_results = masker.generate_lagrangians(
    tensors_dict,
    n_terms_list=(1, 2, 3, 4, 5, 6, 7, 8),
    n_samples=100,
    seed=42,
)

# ── Pretty-print a sample ──
print("\n" + "="*70)
print("SAMPLE LAGRANGIANS")
print("="*70)

for n_terms in sorted(lagrangian_results.keys()):
    lags = lagrangian_results[n_terms]
    if not lags:
        continue
    print(f"\n{'━'*70}")
    print(f"  {n_terms}-term Lagrangians: {len(lags)} generated")
    print(f"{'━'*70}")
    for i, L in enumerate(lags[:3]):
        print(f"\n  ── Sample #{i+1} ──")
        print(f"  General form:")
        print(f"    {L['general']}")
        print(f"  Substituted (FLRW):")
        print(f"    {tex(L['substituted'])}")
        print(f"  Terms:")
        for ti, tt in enumerate(L['terms']):
            print(f"    [{ti+1}] {tt['coeff_symbol']}={tt['coeff_value']:.4e}, "
                  f"dim={tt['mass_dim']}, Mp^{tt['mp_power']}, "
                  f"{tt['candidate']}")

# ── Save all Lagrangians to file ──
_out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lagrangians')
os.makedirs(_out_dir, exist_ok=True)

for n_terms in sorted(lagrangian_results.keys()):
    lags = lagrangian_results[n_terms]
    out_path = os.path.join(_out_dir, f'lagrangians_{n_terms}terms.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"# Lagrangians with {n_terms} terms\n")
        f.write(f"# Total: {len(lags)}\n\n")
        for i, L in enumerate(lags):
            f.write(f"[Lagrangian #{i+1}]\n")
            f.write(f"General:     {L['general']}\n")
            f.write(f"Substituted: {tex(L['substituted'])}\n")
            f.write(f"has_phi:     {L['has_phi']}\n")
            for ti, tt in enumerate(L['terms']):
                f.write(f"  term[{ti+1}]: coeff={tt['coeff_symbol']}={tt['coeff_value']:.6e}, "
                        f"dim={tt['mass_dim']}, Mp^{tt['mp_power']}, {tt['candidate']}\n")
            f.write("\n")
    print(f"  Saved: {out_path}")

# ── Close log ──
sys.stdout = sys.__stdout__
_log_fh.close()
print(f"[Log] Done. Output saved to: {_log_path}")