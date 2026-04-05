"""
General Tensor Index Contraction Engine for Modified Gravity
============================================================
Appended to Tensor_Contraction.py — uses all tensors already computed there.

Strategy:
  1. Each building block gets an IndexedTensor descriptor:
       - name, rank, index positions with up/down flags
       - reference to the actual computed nested-list tensor
  2. For a given operator combo (e.g. ('Ric', 'Rie')):
       - Collect all indices across all tensors in the product
       - Check total index count: if odd → discard
       - Enumerate ALL ways to fully pair the indices into contractions
         (each pair is contracted with g^{μν} if both down, g_{μν} if both up,
          or δ if one up one down)
       - Evaluate each contraction numerically on FLRW
  3. Return nonzero results with symbolic labels
"""

import sympy as sp
import itertools
from functools import reduce
from copy import deepcopy

# ─────────────────────────────────────────────
# Assume these are already computed and in scope:
#   n, coords, g, g_inv, Gamma, Riemann, Ricci, R_scalar,
#   phi (= sp.Function('phi')(t)), nabla_phi, cov_deriv,
#   two_contract, multi_contract, tex
# We re-derive the ones we need if running standalone.
# ─────────────────────────────────────────────

# =============================================
# PART A:  Index bookkeeping
# =============================================

class IndexSlot:
    """One index slot of a tensor."""
    __slots__ = ('name', 'up')
    def __init__(self, name: str, up: bool):
        self.name = name   # human-readable label, e.g. 'ρ'
        self.up = up       # True = contravariant, False = covariant
    def __repr__(self):
        arrow = '↑' if self.up else '↓'
        return f"{self.name}{arrow}"

class TensorBlock:
    """
    A tensor building block in an operator product.
    
    Attributes
    ----------
    label : str          — e.g. 'Rie', 'Ric', 'R', '∇φ', 'φ'
    slots : list[IndexSlot]
    data  : nested list  — the actual numerical tensor components
                           index order must match slots order
    """
    def __init__(self, label, slots, data):
        self.label = label
        self.slots = list(slots)
        self.data  = data
    
    @property
    def rank(self):
        return len(self.slots)
    
    def __repr__(self):
        idx_str = ''.join(str(s) for s in self.slots)
        return f"{self.label}[{idx_str}]"


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
    into unordered pairs. len(indices) must be even.
    
    Returns list of tuples-of-pairs, e.g. for [0,1,2,3]:
      [((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))]
    """
    n = len(indices)
    if n == 0:
        return [()]
    if n % 2 != 0:
        return []  # impossible
    
    first = indices[0]
    rest = indices[1:]
    result = []
    for i, partner in enumerate(rest):
        remaining = rest[:i] + rest[i+1:]
        for sub in all_perfect_matchings(remaining):
            result.append(((first, partner),) + sub)
    return result


# =============================================
# PART C:  Build TensorBlocks from building-block names
# =============================================

# We need a global index counter to give unique names
_idx_counter = 0

def _fresh_idx():
    global _idx_counter
    greek = 'αβγδεζηθικλμνξοπρστυφχψω'
    name = greek[_idx_counter % len(greek)]
    if _idx_counter >= len(greek):
        name += str(_idx_counter // len(greek))
    _idx_counter += 1
    return name

def reset_idx_counter():
    global _idx_counter
    _idx_counter = 0


def make_tensor_block(block_name, tensors_dict):
    """
    Create a TensorBlock for a named building block.
    
    block_name: one of 'φ', '∇', 'R', 'Ric', 'Rie'
    tensors_dict: dict with keys 'Riemann', 'Ricci', 'R_scalar', 'phi',
                  'nabla_phi', 'g', 'g_inv', 'Riemann_down'
    
    For '∇', we DON'T create a standalone block — ∇ must act on something.
    The caller must handle ∇ specially (see make_operator_blocks).
    """
    if block_name == 'φ':
        # Scalar field φ(t): rank 0, no indices
        return TensorBlock('φ', [], tensors_dict['phi'])
    
    elif block_name == 'R':
        # Ricci scalar: rank 0, no indices
        return TensorBlock('R', [], tensors_dict['R_scalar'])
    
    elif block_name == 'Ric':
        # R_{μν}: rank (0,2), two lower indices
        a, b = _fresh_idx(), _fresh_idx()
        slots = [IndexSlot(a, False), IndexSlot(b, False)]
        return TensorBlock('R_{'+a+b+'}', slots, tensors_dict['Ricci'])
    
    elif block_name == 'Rie':
        # R^ρ_{σμν}: rank (1,3), one upper + three lower
        # Index order: [ρ(up), σ(down), μ(down), ν(down)]
        a, b, c, d = _fresh_idx(), _fresh_idx(), _fresh_idx(), _fresh_idx()
        slots = [IndexSlot(a, True), IndexSlot(b, False),
                 IndexSlot(c, False), IndexSlot(d, False)]
        return TensorBlock('R^'+a+'_{'+b+c+d+'}', slots, tensors_dict['Riemann'])
    
    else:
        raise ValueError(f"Unknown block: {block_name}")


def _combo_is_valid(combo):
    """
    Check that every ∇ in the combo has a non-∇ target after it.
    e.g. ('∇', 'φ') is valid, ('∇', '∇') is not, ('φ', '∇') is not.
    Reorders so that ∇'s come before their targets.
    Returns (is_valid, reordered_combo).
    """
    combo = list(combo)
    n_nabla = combo.count('∇')
    non_nabla = [b for b in combo if b != '∇']
    
    if n_nabla == 0:
        return True, tuple(combo)
    
    # We need at least one non-∇ block for ∇ to act on
    if len(non_nabla) == 0:
        return False, tuple(combo)
    
    # Strategy: attach ∇'s to the LAST non-∇ block
    # e.g. ('∇', 'φ') → ∇φ, ('∇', '∇', 'R') → ∇∇R
    # ('∇', 'Ric', 'φ') → we try ∇ acting on the first available target
    # Reorder: put all ∇'s right before the last non-∇ block
    # Actually, for generality: group consecutive ∇'s with the next non-∇
    # But the combos from generate_operators are sorted, so ('R', '∇') etc.
    
    # Simplest valid reorder: all ∇'s, then all non-∇ blocks
    # The ∇'s will act on the first non-∇ block
    reordered = ['∇'] * n_nabla + non_nabla
    
    # Check: max_derivatives per target is 2 (already enforced by generate_operators)
    # But also: n_nabla must not exceed what make_operator_blocks can handle
    if n_nabla > 2:
        return False, tuple(reordered)
    
    # If we have more than one non-∇ block, the ∇ only acts on the first one
    # The rest are standalone
    return True, tuple(reordered)


def make_operator_blocks(combo, tensors_dict):
    """
    Given a combo like ('∇', 'φ') or ('Ric',), build the list of TensorBlocks.
    
    Rules for ∇:
      - ∇ must act on the NEXT tensor in the combo.
      - ∇φ → ∂_μ φ, a rank-1 covector (one lower index)
      - ∇R → ∂_μ R, a rank-1 covector
      - ∇Ric → ∇_ρ R_{μν}, a rank-3 tensor (3 lower indices)
      - ∇Rie → ∇_ρ R^α_{βγδ}, a rank-5 tensor (1 up + 4 down)
      - ∇∇φ → ∇_μ∇_ν φ, rank-2 (2 lower)
    
    Returns list of TensorBlocks.
    """
    reset_idx_counter()
    blocks = []
    combo = list(combo)
    
    i = 0
    while i < len(combo):
        if combo[i] == '∇':
            # Count consecutive ∇'s
            n_nabla = 0
            while i < len(combo) and combo[i] == '∇':
                n_nabla += 1
                i += 1
            
            if i >= len(combo):
                # ∇ at end with nothing to act on — this is unphysical
                # but we handle it: ∇ acting on... nothing. 
                # Actually this shouldn't happen with valid combos.
                # Treat each bare ∇ as a 1-index covector (∂_μ of implicit scalar)
                for _ in range(n_nabla):
                    idx = _fresh_idx()
                    blocks.append(TensorBlock('∇_'+idx, 
                                             [IndexSlot(idx, False)],
                                             None))  # will be handled specially
            else:
                # ∇^n acting on the next block
                target = combo[i]
                i += 1
                
                if target == 'φ':
                    if n_nabla == 1:
                        # ∇_μ φ = ∂_μ φ : covector
                        idx = _fresh_idx()
                        nabla_phi = [sp.diff(tensors_dict['phi'], c) for c in tensors_dict['coords']]
                        blocks.append(TensorBlock('∇_'+idx+'φ',
                                                 [IndexSlot(idx, False)],
                                                 nabla_phi))
                    elif n_nabla == 2:
                        # ∇_μ∇_ν φ: use cov_deriv on ∇φ
                        nabla_phi = [sp.diff(tensors_dict['phi'], c) for c in tensors_dict['coords']]
                        # ∇_ν(∇_μ φ) — ∇φ is a (0,1) tensor
                        nabla2_phi = tensors_dict['cov_deriv'](nabla_phi, 0, 1)
                        idx_a, idx_b = _fresh_idx(), _fresh_idx()
                        blocks.append(TensorBlock('∇_'+idx_a+'∇_'+idx_b+'φ',
                                                 [IndexSlot(idx_a, False),
                                                  IndexSlot(idx_b, False)],
                                                 nabla2_phi))
                    else:
                        raise NotImplementedError(f"{n_nabla} derivatives on φ not implemented")
                
                elif target == 'R':
                    if n_nabla == 1:
                        # ∇_μ R: partial derivative of scalar
                        idx = _fresh_idx()
                        nabla_R = [sp.simplify(sp.diff(tensors_dict['R_scalar'], c)) 
                                   for c in tensors_dict['coords']]
                        blocks.append(TensorBlock('∇_'+idx+'R',
                                                 [IndexSlot(idx, False)],
                                                 nabla_R))
                    elif n_nabla == 2:
                        nabla_R = [sp.simplify(sp.diff(tensors_dict['R_scalar'], c)) 
                                   for c in tensors_dict['coords']]
                        nabla2_R = tensors_dict['cov_deriv'](nabla_R, 0, 1)
                        idx_a, idx_b = _fresh_idx(), _fresh_idx()
                        blocks.append(TensorBlock('∇_'+idx_a+'∇_'+idx_b+'R',
                                                 [IndexSlot(idx_a, False),
                                                  IndexSlot(idx_b, False)],
                                                 nabla2_R))
                    else:
                        raise NotImplementedError(f"{n_nabla} derivatives on R not implemented")
                
                elif target == 'Ric':
                    if n_nabla == 1:
                        # ∇_ρ R_{μν}: cov_deriv of (0,2) tensor
                        nabla_Ric = tensors_dict['cov_deriv'](tensors_dict['Ricci'], 0, 2)
                        idx_a, idx_b, idx_c = _fresh_idx(), _fresh_idx(), _fresh_idx()
                        # nabla_Ric[μ][ν][ρ] = ∇_ρ R_{μν}
                        # Reorder to put ∇ index first for clarity? 
                        # No — keep cov_deriv convention: original indices first, ∇ index last
                        blocks.append(TensorBlock('∇_'+idx_c+'R_{'+idx_a+idx_b+'}',
                                                 [IndexSlot(idx_a, False),
                                                  IndexSlot(idx_b, False),
                                                  IndexSlot(idx_c, False)],
                                                 nabla_Ric))
                    else:
                        raise NotImplementedError(f"{n_nabla} derivatives on Ric not implemented")
                
                elif target == 'Rie':
                    if n_nabla == 1:
                        # ∇_ρ R^α_{βγδ}: cov_deriv of (1,3) tensor
                        nabla_Rie = tensors_dict['cov_deriv'](tensors_dict['Riemann'], 1, 3)
                        idx_a, idx_b, idx_c, idx_d, idx_e = [_fresh_idx() for _ in range(5)]
                        # nabla_Rie[α][β][γ][δ][ρ] = ∇_ρ R^α_{βγδ}
                        blocks.append(TensorBlock('∇_'+idx_e+'R^'+idx_a+'_{'+idx_b+idx_c+idx_d+'}',
                                                 [IndexSlot(idx_a, True),
                                                  IndexSlot(idx_b, False),
                                                  IndexSlot(idx_c, False),
                                                  IndexSlot(idx_d, False),
                                                  IndexSlot(idx_e, False)],
                                                 nabla_Rie))
                    else:
                        raise NotImplementedError(f"{n_nabla} derivatives on Rie not implemented")
                
                else:
                    raise ValueError(f"∇ acting on unknown target: {target}")
        else:
            blocks.append(make_tensor_block(combo[i], tensors_dict))
            i += 1
    
    return blocks


# =============================================
# PART D:  Contract and evaluate
# =============================================

def contract_and_evaluate(blocks, tensors_dict, dim=4):
    """
    Given a list of TensorBlocks forming an operator product:
      1. Collect all index slots across all blocks
      2. If total number of slots is odd → return [] (cannot fully contract)
      3. Enumerate all perfect matchings of index slots
      4. For each matching, determine the metric insertion needed:
           - (up, up)   → need g_{ab} to contract  
           - (down, down) → need g^{ab} to contract
           - (up, down) or (down, up) → direct δ contraction (sum over index)
      5. Evaluate by explicit summation over all index values
      6. Return list of (label_str, value) for nonzero results
    
    Returns
    -------
    list of dict with keys: 'label', 'contraction', 'value'
    """
    n = dim
    g_mat = tensors_dict['g']
    g_inv_mat = tensors_dict['g_inv']
    
    # Collect all slots with their (block_index, slot_index_within_block)
    all_slots = []
    for bi, block in enumerate(blocks):
        for si, slot in enumerate(block.slots):
            all_slots.append((bi, si, slot))
    
    total_indices = len(all_slots)
    
    # Scalars (rank-0 tensors) — just multiply their values
    if total_indices == 0:
        # All blocks are scalars, just multiply
        val = sp.Integer(1)
        for block in blocks:
            val *= block.data
        val = sp.simplify(val)
        label = ' · '.join(b.label for b in blocks)
        return [{'label': label, 'contraction': 'none (all scalars)', 'value': val}]
    
    # Odd number of indices → discard
    if total_indices % 2 != 0:
        label = ' · '.join(b.label for b in blocks)
        return [{'label': label, 'contraction': 'DISCARDED (odd indices)', 'value': None}]
    
    # Enumerate all perfect matchings
    slot_indices = list(range(total_indices))
    matchings = all_perfect_matchings(slot_indices)
    
    results = []
    seen_values = {}  # to detect duplicates
    
    for matching in matchings:
        # Build contraction description
        contraction_parts = []
        for (i, j) in matching:
            si = all_slots[i][2]  # IndexSlot
            sj = all_slots[j][2]
            contraction_parts.append(f"({si.name}{'^' if si.up else '_'}, "
                                    f"{sj.name}{'^' if sj.up else '_'})")
        contraction_str = ', '.join(contraction_parts)
        
        # Evaluate by explicit summation
        # We assign each slot a summation index variable (0..n-1)
        # and loop over all combinations
        val = sp.Integer(0)
        
        for idx_vals in itertools.product(range(n), repeat=total_indices):
            # For each matching pair, compute the "glue" factor
            glue = sp.Integer(1)
            for (i, j) in matching:
                si = all_slots[i][2]
                sj = all_slots[j][2]
                vi = idx_vals[i]
                vj = idx_vals[j]
                
                if si.up and sj.up:
                    # Both up: need g_{vi vj} to lower and contract
                    glue *= g_mat[vi, vj]
                elif (not si.up) and (not sj.up):
                    # Both down: need g^{vi vj} to raise and contract
                    glue *= g_inv_mat[vi, vj]
                else:
                    # One up, one down: δ contraction — only nonzero when vi == vj
                    if vi != vj:
                        glue = sp.Integer(0)
                        break
            
            if glue == 0:
                continue
            
            # Compute the product of tensor components
            term = glue
            for bi, block in enumerate(blocks):
                if block.rank == 0:
                    term *= block.data
                else:
                    # Extract the index values for this block's slots
                    block_idx = tuple(
                        idx_vals[k] for k in range(total_indices)
                        if all_slots[k][0] == bi
                    )
                    term *= get_element(block.data, block_idx)
            
            val += term
        
        val = sp.simplify(val)
        
        # Build full label
        block_labels = ' · '.join(b.label for b in blocks)
        full_label = f"{block_labels}  contracted: {contraction_str}"
        
        # Check if we've already seen this value (avoid duplicates)
        val_key = str(val)
        if val_key in seen_values:
            # Still record it but mark as duplicate
            results.append({
                'label': full_label,
                'contraction': contraction_str,
                'value': val,
                'duplicate_of': seen_values[val_key]
            })
        else:
            seen_values[val_key] = full_label
            results.append({
                'label': full_label,
                'contraction': contraction_str,
                'value': val
            })
    
    return results


# =============================================
# PART E:  Main driver — process all combos for a given dim
# =============================================

def process_dimension(target_dim, tensors_dict, max_derivatives=2, verbose=True, tex_fn=None):
    """
    For a given target mass dimension:
      1. Generate all operator combos
      2. For each combo, build TensorBlocks, enumerate contractions, evaluate
      3. Collect and return all nonzero independent results
    
    Parameters
    ----------
    target_dim : int
    tensors_dict : dict with all precomputed tensors
    
    Returns
    -------
    all_results : list of dicts with 'combo', 'label', 'contraction', 'value'
    """
    from itertools import combinations_with_replacement
    
    # Resolve pretty-printer
    _tex = tex_fn if tex_fn is not None else str
    
    building_blocks = {
        'φ':   1,
        '∇':   1,
        'R':   2,
        'Ric': 2,
        'Rie': 2,
    }
    
    combos = generate_operators(target_dim, building_blocks, max_derivatives)
    
    all_results = []
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"PROCESSING DIMENSION {target_dim}")
        print(f"{'='*70}")
        print(f"Number of operator combos: {len(combos)}\n")
    
    for ci, combo in enumerate(combos):
        # Check if combo is valid (∇ has targets)
        valid, reordered = _combo_is_valid(combo)
        if not valid:
            combo_str = ' · '.join(combo)
            if verbose:
                print(f"--- Combo {ci+1}: {combo_str} ---")
                print(f"  SKIPPED: ∇ has no field to act on\n")
            continue
        combo = reordered
        combo_str = ' · '.join(combo)
        if verbose:
            print(f"--- Combo {ci+1}: {combo_str} ---")
        
        try:
            blocks = make_operator_blocks(combo, tensors_dict)
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
                    dup = f"  [duplicate]" if 'duplicate_of' in r else ""
                    print(f"    {r['contraction']}")
                    print(f"      = {_tex(r['value'])}{dup}")
            
            for r in nonzero:
                r['combo'] = combo
                r['combo_str'] = combo_str
            all_results.extend(nonzero)
        
        if verbose:
            print()
    
    # ── Summary ──
    if verbose:
        print(f"\n{'='*70}")
        print(f"SUMMARY: Dim-{target_dim} nonzero scalar contractions")
        print(f"{'='*70}")
        
        # Deduplicate by value
        unique = {}
        for r in all_results:
            found_match = False
            for key, ref in unique.items():
                ratio = sp.simplify(r['value'] / ref['value'])
                if ratio.is_number:
                    if verbose:
                        print(f"  {r['label']}")
                        print(f"    = {_tex(ratio)} × ({ref['label']})")
                    found_match = True
                    break
            if not found_match:
                unique[r['label']] = r
                if verbose:
                    print(f"  {r['label']}  — INDEPENDENT")
                    print(f"    = {_tex(r['value'])}")
        
        print(f"\n  Total independent dim-{target_dim} scalars: {len(unique)}")
        for label, r in unique.items():
            print(f"    • {r['combo_str']}  [{r['contraction']}]")
            print(f"      = {_tex(r['value'])}")
    
    return all_results


# =============================================
# PART F:  Helper to generate_operators (copied from original)
# =============================================

def generate_operators(target_dim, blocks=None, max_derivatives=2):
    from itertools import combinations_with_replacement
    if blocks is None:
        blocks = {
            'φ':   1, '∇':   1, 'R':   2, 'Ric': 2, 'Rie': 2,
        }
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


    # ── 打包所有已算好的张量 ──
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

# ── 运行 dim=2 并打印 ──
results = process_dimension(2, tensors_dict, verbose=True, tex_fn=tex)