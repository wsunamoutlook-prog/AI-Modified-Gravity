#!/usr/bin/env python3
"""Grammar-guided invariant and Lagrangian generation for masker v3.2."""

import random
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import sympy as sp

from .tensor import (
    contract_and_evaluate,
    make_operator_blocks_from_combo,
    sqrt_mg,
    tex,
)

GRAMMAR_TOKENS = ['BOS', 'EOS', 'NABLA', 'PHI1', 'PHI2', 'R_SCALAR', 'RIC', 'RIE']

TARGETS     = ['PHI1', 'PHI2', 'R_SCALAR', 'RIC', 'RIE']
TARGET_DIM  = {'PHI1': 1, 'PHI2': 1, 'R_SCALAR': 2, 'RIC': 2, 'RIE': 2}
TARGET_RANK = {'PHI1': 0, 'PHI2': 0, 'R_SCALAR': 0, 'RIC': 2, 'RIE': 4}

# Canonical ordering: φ1 < φ2 < R < Ric < Rie, within each target lower ∇ first
TARGET_ORDER = {'PHI1': 0, 'PHI2': 1, 'R_SCALAR': 2, 'RIC': 3, 'RIE': 4}

# Maps masker tokens back to the names used by make_tensor_block / _build_derivative_block
TOKEN_TO_BLOCK = {'PHI1': 'φ1', 'PHI2': 'φ2', 'R_SCALAR': 'R', 'RIC': 'Ric', 'RIE': 'Rie'}

token2id = {tok: i for i, tok in enumerate(GRAMMAR_TOKENS)}
id2token = {i: tok for i, tok in enumerate(GRAMMAR_TOKENS)}

# ML-only coefficient-slot tokens. These are intentionally separate from the
# low-level operator grammar vocabulary above.
MAX_COEFF_SLOTS = 64
COEFF_TOKENS = [f"COEFF_{i}" for i in range(MAX_COEFF_SLOTS)]
FIXED_COEFF_TOKENS = ["COEFF_FIXED_1"]
ML_COEFF_TOKENS = COEFF_TOKENS + FIXED_COEFF_TOKENS
ml_coeff_token2id = {tok: i for i, tok in enumerate(ML_COEFF_TOKENS)}
ml_coeff_id2token = {i: tok for i, tok in enumerate(ML_COEFF_TOKENS)}


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
Lambda_eft = sp.Symbol(r'\Lambda', positive=True)  # EFT cutoff scale (mass dim = 1)

# Two scalar field masses
m1_phi = sp.Symbol('m_1', positive=True)      # scalar field #1 mass
m2_phi = sp.Symbol('m_2', positive=True)      # scalar field #2 mass

# Two axion decay constants
f1_axion = sp.Symbol('f_1', positive=True)    # decay constant for φ1
f2_axion = sp.Symbol('f_2', positive=True)    # decay constant for φ2

_GREEK_COEFFS = [sp.Symbol(g) for g in
    [r'\alpha', r'\beta', r'\gamma', r'\delta',
     r'\epsilon', r'\zeta', r'\eta', r'\theta',
     r'\iota', r'\kappa', r'\xi', r'\varpi']]

@dataclass
class CandidateScalar:
    """One independent curvature/field invariant ready for Lagrangian use."""
    mass_dim: int              # mass dimension of this scalar
    combo_label: str           # human-readable e.g. 'Ric · Ric'
    contraction_label: str     # e.g. 'R^{ab}_{ab} · ...'
    symbolic_value: Any        # sympy expression (metric-substituted)
    general_label: str         # token/index notation (NOT substituted)
    sector: str = 'gravity'    # 'gravity' | 'non-minimal' | 'scalar'


# ── Masker ──

class GravityMasker:
    """
    Grammar-guided masker for modified-gravity Lagrangian operators.
    Updated for two scalar fields φ1 and φ2.

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
        return (TARGET_ORDER[target_token], n_nabla)

    def _last_block_key(self, state: GravityState) -> Optional[Tuple[int, int]]:
        if not state.completed_blocks:
            return None
        n, blk_name = state.completed_blocks[-1]
        blk_to_tok = {v: k for k, v in TOKEN_TO_BLOCK.items()}
        return (TARGET_ORDER[blk_to_tok[blk_name]], n)

    def _block_ge_last(self, state: GravityState, n_nabla: int, target_token: str) -> bool:
        last = self._last_block_key(state)
        if last is None:
            return True
        return self._block_order_key(n_nabla, target_token) >= last

    def _target_fits(self, state: GravityState, target_token: str) -> bool:
        return TARGET_DIM[target_token] <= state.remaining_dim

    def _can_add_nabla(self, state: GravityState) -> bool:
        if state.total_nabla >= state.max_derivatives:
            return False
        if state.remaining_dim - 1 < 1:
            return False
        future_nabla = state.current_block_nabla + 1
        for t in TARGETS:
            if TARGET_DIM[t] <= state.remaining_dim - 1:
                if self._block_ge_last(state, future_nabla, t):
                    return True
        return False

    def _valid_block_starters(self, state: GravityState) -> List[str]:
        valid = []
        if self._can_add_nabla(state):
            valid.append('NABLA')
        for t in TARGETS:
            if self._target_fits(state, t) and self._block_ge_last(state, 0, t):
                valid.append(t)
        return valid

    # ────────────────────────────────────────
    #  Combo generation via DFS over the grammar
    # ────────────────────────────────────────

    def generate_all_combos(self, target_dim: int) -> List[List[Tuple[int, str]]]:
        results = []

        def _dfs(state: GravityState, token_seq: List[str]):
            last = state.last_token if state.last_token else 'BOS'
            valid = self.get_valid_tokens(state, last)

            for tok in valid:
                new_state = deepcopy(state)
                self.step(new_state, tok)

                if tok == 'EOS':
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

        # ── Independence analysis ──
        if verbose:
            groups = []

            from sympy import Rational as _Rat
            _t_sym_s = tensors_dict['coords'][0]
            _sub1_s = {
                sp.Function('N', positive=True): sp.Lambda(_t_sym_s, 2 + 3*_t_sym_s + 5*_t_sym_s**2),
                sp.Function('a', positive=True): sp.Lambda(_t_sym_s, 7 + 11*_t_sym_s + 13*_t_sym_s**2),
                sp.Function('phi1'): sp.Lambda(_t_sym_s, 17 + 19*_t_sym_s + 23*_t_sym_s**2),
                sp.Function('phi2'): sp.Lambda(_t_sym_s, 29 + 31*_t_sym_s + 37*_t_sym_s**2),
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
        _tex = tex_fn if tex_fn is not None else str
        from sympy import Rational as _Rat

        _t_sym_c = tensors_dict['coords'][0]
        _sub_c = {
            sp.Function('N', positive=True): sp.Lambda(_t_sym_c, 2 + 3*_t_sym_c + 5*_t_sym_c**2),
            sp.Function('a', positive=True): sp.Lambda(_t_sym_c, 7 + 11*_t_sym_c + 13*_t_sym_c**2),
            sp.Function('phi1'): sp.Lambda(_t_sym_c, 17 + 19*_t_sym_c + 23*_t_sym_c**2),
            sp.Function('phi2'): sp.Lambda(_t_sym_c, 29 + 31*_t_sym_c + 37*_t_sym_c**2),
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
                # Classify sector:
                #   'gravity'     — pure curvature, no φ1/φ2
                #   'non-minimal' — curvature × φ (both present)
                #   'scalar'      — pure φ operators (φ1², φ2², φ1·φ2, ∇φ1·∇φ2, …)
                combo = rep.get('combo', [])
                has_phi_in_combo  = any(target in ('φ1', 'φ2') for (_, target) in combo)
                has_curv_in_combo = any(target in ('R', 'Ric', 'Rie') for (_, target) in combo)
                if has_phi_in_combo and has_curv_in_combo:
                    sector = 'non-minimal'
                elif has_phi_in_combo:
                    sector = 'scalar'
                else:
                    sector = 'gravity'
                cands.append(CandidateScalar(
                    mass_dim=d,
                    combo_label=rep.get('combo_str', ''),
                    contraction_label=rep['label'],
                    symbolic_value=rep['value'],
                    general_label=rep['label'],
                    sector=sector,
                ))
            candidates_by_dim[d] = cands
            n_grav = sum(1 for c in cands if c.sector == 'gravity')
            n_nm   = sum(1 for c in cands if c.sector == 'non-minimal')
            n_sc   = sum(1 for c in cands if c.sector == 'scalar')
            print(f"  dim={d}: {len(cands)} independent candidates "
                  f"({n_grav} gravity, {n_nm} non-minimal, {n_sc} scalar)")

        self.candidates_by_dim = candidates_by_dim
        self.all_candidates = []
        for d in sorted(candidates_by_dim):
            self.all_candidates.extend(candidates_by_dim[d])
        print(f"\n  Total candidate pool: {len(self.all_candidates)} independent scalars\n")

        return candidates_by_dim

    # ────────────────────────────────────────
    #  Lagrangian generation — random sampling
    #  (updated for two scalar fields)
    # ────────────────────────────────────────

    @staticmethod
    def _random_coeff():
        log_val = random.uniform(-5, 5)
        sign = random.choice([-1, 1])
        return sign * 10**log_val

    @staticmethod
    def _pad_lambda(mass_dim_of_term: int, sector: str = 'gravity') -> int:
        """Power of Λ needed to make a term contribute correctly to mass-dim-4 Lagrangian.

        EFT convention (four sectors inside √(-g) [  ]):

        1. Pure gravity (sector='gravity'):
             Mp²  Σ c_i  Λ^{2-d_i}  O_{d_i}
           → Λ power = 2 - d.

        2. Non-minimal coupling (sector='non-minimal', curvature × φ):
             Mp²  Σ c_i  Λ^{2-d_i}  O_{d_i}
           → Λ power = 2 - d.  Same as gravity (Mp² prefactor).

        3. Pure scalar (sector='scalar', φ², φ³, φ□φ, ∇ᵃφ∇ₐφ, …):
             Σ c_i  Λ^{4-d_i}  O_{d_i}
           → Λ power = 4 - d.  NO Mp².

        4. Matter supplement (sector='matter', fixed kinetic + potential):
             Already mass-dim 4 by construction.  Λ^0.
        """
        if sector in ('gravity', 'non-minimal'):
            return 2 - mass_dim_of_term
        elif sector in ('scalar', 'matter'):
            return 4 - mass_dim_of_term
        else:
            raise ValueError(f"Unknown sector: {sector}")

    @staticmethod
    def _involves_phi1(cand):
        """Check whether a CandidateScalar involves φ1."""
        return 'φ1' in cand.combo_label or 'phi1' in str(cand.symbolic_value)

    @staticmethod
    def _involves_phi2(cand):
        """Check whether a CandidateScalar involves φ2."""
        return 'φ2' in cand.combo_label or 'phi2' in str(cand.symbolic_value)

    def generate_lagrangians(self, tensors_dict: dict,
                             n_terms_list: Tuple[int, ...] = (1,2,3,4,5,6,7,8,9,10,11,12),
                             n_samples: int = 100,
                             seed: int = 42) -> Dict[int, list]:
        """
        Generate random Lagrangians from the collected candidate pool.
        Must call collect_candidates() first.

        Each Lagrangian may include zero, one, or both scalar fields.
        When a scalar φ_i is active, two fixed matter terms are added:
          • kinetic:   -½ g^{μν} ∇_μφ_i ∇_νφ_i
          • potential:  randomly chosen from {quadratic, axion}
              quadratic:  -½ m_i² φ_i²
              axion:      -m_i² f_i² (1 - cos(φ_i / f_i))

        Scalar configurations:
          'none'       → 0 fixed matter terms
          'phi1_only'  → 2 fixed matter terms (kinetic1 + potential1)
          'phi2_only'  → 2 fixed matter terms (kinetic2 + potential2)
          'both'       → 4 fixed matter terms

        Returns dict: n_terms → list of Lagrangian dicts.
        """
        if not hasattr(self, 'all_candidates') or not self.all_candidates:
            raise RuntimeError("Call collect_candidates() before generate_lagrangians()")

        all_cands = self.all_candidates

        phi1_func = tensors_dict['phi1']
        phi2_func = tensors_dict['phi2']
        t_coord = tensors_dict['coords'][0]
        N_func = sp.Function('N', positive=True)(t_coord)

        phi1_dot = sp.Derivative(phi1_func, t_coord)
        phi2_dot = sp.Derivative(phi2_func, t_coord)

        # Pre-build kinetic terms (metric-substituted)
        kinetic1_value = sp.Rational(1, 2) * phi1_dot**2 / N_func**2
        kinetic1_general = "-½ g^{μν} ∇_μφ1 ∇_νφ1"
        kinetic2_value = sp.Rational(1, 2) * phi2_dot**2 / N_func**2
        kinetic2_general = "-½ g^{μν} ∇_μφ2 ∇_νφ2"

        # Potential term generators
        def _make_potential(which, pot_type):
            """Return (general_str, symbolic_value, label_for_term_info) for the chosen potential."""
            if which == 1:
                m, f, phi = m1_phi, f1_axion, phi1_func
                m_str, f_str, phi_str = 'm_1', 'f_1', 'φ1'
            else:
                m, f, phi = m2_phi, f2_axion, phi2_func
                m_str, f_str, phi_str = 'm_2', 'f_2', 'φ2'

            if pot_type == 'quadratic':
                val = sp.Rational(-1, 2) * m**2 * phi**2
                gen = f"-½ {m_str}² {phi_str}²"
            else:  # axion
                val = -m**2 * f**2 * (1 - sp.cos(phi / f))
                gen = f"-{m_str}² {f_str}² (1 - cos({phi_str}/{f_str}))"
            return gen, val

        # Scalar configuration probabilities
        SCALAR_CONFIGS = ['none', 'phi1_only', 'phi2_only', 'both']
        CONFIG_WEIGHTS = [0.3, 0.25, 0.25, 0.2]  # weighted random

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

                # ── Step 1: Choose scalar configuration ──
                config = random.choices(SCALAR_CONFIGS, weights=CONFIG_WEIGHTS, k=1)[0]
                include_phi1 = config in ('phi1_only', 'both')
                include_phi2 = config in ('phi2_only', 'both')
                n_fixed = 2 * (int(include_phi1) + int(include_phi2))
                n_curv = n_total - n_fixed

                if n_curv < 0:
                    continue

                # ── Step 2: Build candidate pool consistent with config ──
                if config == 'none':
                    pool = [c for c in all_cands
                            if not self._involves_phi1(c) and not self._involves_phi2(c)]
                elif config == 'phi1_only':
                    pool = [c for c in all_cands if not self._involves_phi2(c)]
                elif config == 'phi2_only':
                    pool = [c for c in all_cands if not self._involves_phi1(c)]
                else:  # both
                    pool = list(all_cands)

                # ── Step 3: Sample n_curv candidates from pool ──
                if n_curv == 0:
                    chosen = []
                elif n_curv <= len(pool):
                    chosen = random.sample(pool, n_curv)
                else:
                    if not pool:
                        continue
                    chosen = [random.choice(pool) for _ in range(n_curv)]

                # ── Step 4: Choose potential types ──
                pot1_type = random.choice(['quadratic', 'axion']) if include_phi1 else None
                pot2_type = random.choice(['quadratic', 'axion']) if include_phi2 else None

                # ── Dedup by structure ──
                fingerprint_parts = sorted(c.contraction_label for c in chosen)
                fp_key = (config, pot1_type, pot2_type, tuple(fingerprint_parts))
                if fp_key in seen_combos:
                    continue
                seen_combos.add(fp_key)

                # ── Assign symbolic coefficients ──
                coeffs = []
                for i in range(len(chosen)):
                    sym = (_GREEK_COEFFS[i] if i < len(_GREEK_COEFFS)
                           else sp.Symbol(f'c_{{{i+1}}}'))
                    coeffs.append(sym)

                # ── Build general and substituted forms ──
                # FOUR sectors:
                #   gravity    : Mp² (c_i Λ^{2-d} O_d + ...)     ← pure curvature
                #   non-minimal: Mp² (c_j Λ^{2-d} O_d + ...)     ← curvature × φ  (same Mp² prefactor)
                #   scalar     :       c_k Λ^{4-d} O_d + ...     ← pure φ (φ1², φ1·φ2, …)
                #   matter     :       kinetic + potential         ← fixed scalar terms
                general_grav_parts = []
                general_nm_parts   = []
                general_sc_parts   = []
                general_phi_parts  = []
                substituted_grav = sp.Integer(0)
                substituted_nm   = sp.Integer(0)
                substituted_sc   = sp.Integer(0)
                substituted_phi  = sp.Integer(0)
                term_info = []

                for i, cand in enumerate(chosen):
                    lam_power = self._pad_lambda(cand.mass_dim, cand.sector)
                    lam_factor = Lambda_eft**lam_power if lam_power != 0 else sp.Integer(1)
                    lam_str = f" Λ^{{{lam_power}}}" if lam_power != 0 else ""

                    if cand.sector == 'gravity':
                        general_grav_parts.append(f"{coeffs[i]}{lam_str} · {cand.general_label}")
                        substituted_grav += coeffs[i] * lam_factor * cand.symbolic_value
                    elif cand.sector == 'non-minimal':
                        general_nm_parts.append(f"{coeffs[i]}{lam_str} · {cand.general_label}")
                        substituted_nm += coeffs[i] * lam_factor * cand.symbolic_value
                    else:  # scalar
                        general_sc_parts.append(f"{coeffs[i]}{lam_str} · {cand.general_label}")
                        substituted_sc += coeffs[i] * lam_factor * cand.symbolic_value

                    term_info.append({
                        'coeff_symbol': str(coeffs[i]),
                        'coeff_token': f"COEFF_{i}",
                        'candidate': cand.contraction_label,
                        'mass_dim': cand.mass_dim,
                        'lambda_power': lam_power,
                        'sector': cand.sector,
                    })

                # ── Matter supplement: kinetic + potential for each active scalar ──
                if include_phi1:
                    general_phi_parts.append(kinetic1_general)
                    substituted_phi += kinetic1_value

                    pot1_gen, pot1_val = _make_potential(1, pot1_type)
                    general_phi_parts.append(pot1_gen)
                    substituted_phi += pot1_val

                    term_info.append({
                        'coeff_symbol': '1',
                        'coeff_token': 'COEFF_FIXED_1',
                        'candidate': kinetic1_general, 'mass_dim': 4, 'lambda_power': 0,
                        'fixed': True, 'sector': 'matter'})
                    term_info.append({
                        'coeff_symbol': '1',
                        'coeff_token': 'COEFF_FIXED_1',
                        'candidate': pot1_gen, 'mass_dim': 4, 'lambda_power': 0,
                        'fixed': True, 'sector': 'matter', 'potential_type': pot1_type})

                if include_phi2:
                    general_phi_parts.append(kinetic2_general)
                    substituted_phi += kinetic2_value

                    pot2_gen, pot2_val = _make_potential(2, pot2_type)
                    general_phi_parts.append(pot2_gen)
                    substituted_phi += pot2_val

                    term_info.append({
                        'coeff_symbol': '1',
                        'coeff_token': 'COEFF_FIXED_1',
                        'candidate': kinetic2_general, 'mass_dim': 4, 'lambda_power': 0,
                        'fixed': True, 'sector': 'matter'})
                    term_info.append({
                        'coeff_symbol': '1',
                        'coeff_token': 'COEFF_FIXED_1',
                        'candidate': pot2_gen, 'mass_dim': 4, 'lambda_power': 0,
                        'fixed': True, 'sector': 'matter', 'potential_type': pot2_type})

                # ── Assemble general form string ──
                # gravity + non-minimal both get Mp² prefactor
                mp2_parts = general_grav_parts + general_nm_parts
                inner_parts = []
                if mp2_parts:
                    inner_parts.append("M_p² ( " + "  +  ".join(mp2_parts) + " )")
                if general_sc_parts:
                    inner_parts.append("  +  ".join(general_sc_parts))
                if general_phi_parts:
                    inner_parts.append("  +  ".join(general_phi_parts))
                general_str = "√(-g) [ " + "  +  ".join(inner_parts) + " ]"

                # ── Substituted form: Mp² multiplies gravity + non-minimal sectors ──
                substituted_full = sqrt_mg * (
                    Mp**2 * (substituted_grav + substituted_nm) + substituted_sc + substituted_phi
                )

                lagrangians.append({
                    'n_terms': n_total,
                    'general': general_str,
                    'substituted': sp.simplify(substituted_full),
                    'terms': term_info,
                    'scalar_config': config,
                    'potential_types': {'phi1': pot1_type, 'phi2': pot2_type},
                })

            print(f"    → Generated {len(lagrangians)} unique Lagrangians "
                  f"(from {attempts} attempts)")
            results[n_total] = lagrangians

        return results


# ╔═══════════════════════════════════════════════════════════════════╗
# ║                         MAIN DRIVER                               ║
# ╚═══════════════════════════════════════════════════════════════════╝
