#!/usr/bin/env python3
"""Generate a paste-ready PRD appendix from the cached operator catalog."""

from __future__ import annotations

import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ai_theory_lab.cold_start_runner import (
    DIRECT_MAX_OPERATOR_TERMS,
    DIRECT_MIN_OPERATOR_TERMS,
    TOKEN_CONTEXT_DIMS,
    TOKEN_CONTEXT_MAX_DERIVATIVES,
    _build_token_level_context,
    _candidate_allowed_for_scalar_config,
)


OUTPUT = ROOT / "paper_work" / "appendix_theory_space.tex"
SECTOR_TAG = {
    "gravity": r"\mathrm{G}",
    "non-minimal": r"\mathrm{NM}",
    "scalar": r"\mathrm{S}",
}


def _latex_atom(atom: str) -> str:
    replacements = {
        "∇^{a}∇_{a}φ1": r"\Box\phi_1",
        "∇^{a}∇_{a}φ2": r"\Box\phi_2",
        "∇^{a}∇_{a}R": r"\Box R",
        "φ1": r"\phi_1",
        "φ2": r"\phi_2",
        "∇": r"\nabla",
    }
    for old, new in replacements.items():
        atom = atom.replace(old, new)
    # Give mixed-index tensors an empty group so upper and lower indices do
    # not collide typographically in the paper tables.
    atom = re.sub(r"([A-Za-z]+)(\^\{[^{}]+\})_\{", r"\1\2{}_{", atom)
    return atom


def _operator_latex(label: str) -> str:
    atoms = label.split(" · ")
    compact: list[str] = []
    i = 0
    while i < len(atoms):
        atom = atoms[i]
        if atom in {"φ1", "φ2", "R"}:
            j = i + 1
            while j < len(atoms) and atoms[j] == atom:
                j += 1
            count = j - i
            rendered = _latex_atom(atom)
            compact.append(f"{rendered}^{{{count}}}" if count > 1 else rendered)
            i = j
            continue
        compact.append(_latex_atom(atom))
        i += 1
    return r"\,".join(compact)


def _op_id(global_number: int, dim: int, sector: str) -> str:
    return rf"$\mathcal{{O}}^{{({dim},{SECTOR_TAG[sector]})}}_{{{global_number:03d}}}$"


def _paired_rows(candidates: list[tuple[int, object]]) -> str:
    entries = [
        (
            _op_id(global_number, candidate.mass_dim, candidate.sector),
            rf"${_operator_latex(candidate.general_label)}$",
        )
        for global_number, candidate in candidates
    ]
    rows: list[str] = []
    midpoint = math.ceil(len(entries) / 2)
    left = entries[:midpoint]
    right = entries[midpoint:]
    for index, (left_id, left_op) in enumerate(left):
        if index < len(right):
            right_id, right_op = right[index]
        else:
            right_id, right_op = "", ""
        rows.append(f"{left_id} & {left_op} & {right_id} & {right_op} \\\\")
    return "\n".join(rows)


def _catalog_table(candidates: list[tuple[int, object]], caption: str, label: str) -> str:
    return rf"""
\begin{{table*}}[t]
\caption{{{caption}}}
\label{{{label}}}
\centering
\footnotesize
\renewcommand{{\arraystretch}}{{1.08}}
\setlength{{\tabcolsep}}{{3.5pt}}
\begin{{tabular}}{{@{{}}l p{{0.386\textwidth}} l p{{0.386\textwidth}}@{{}}}}
\toprule
ID & Operator & ID & Operator \\
\midrule
{_paired_rows(candidates)}
\bottomrule
\end{{tabular}}
\end{{table*}}
"""


def main() -> None:
    context = _build_token_level_context(0, use_cache=True)
    candidates = list(context["masker"].all_candidates)
    if len(candidates) != 141:
        raise RuntimeError(f"Expected 141 cached operators, found {len(candidates)}")

    numbered_candidates = list(enumerate(candidates, 1))
    by_dim = {
        dim: [
            (global_number, candidate)
            for global_number, candidate in numbered_candidates
            if candidate.mass_dim == dim
        ]
        for dim in TOKEN_CONTEXT_DIMS
    }
    dim_counts = Counter(candidate.mass_dim for candidate in candidates)
    sector_counts = Counter(candidate.sector for candidate in candidates)
    config_counts = {
        scalar_config: sum(
            _candidate_allowed_for_scalar_config(candidate, scalar_config)
            for candidate in candidates
        )
        for scalar_config in ("none", "phi1_only", "phi2_only", "both")
    }
    structure_count = (
        sum(math.comb(config_counts["none"], n) for n in range(DIRECT_MIN_OPERATOR_TERMS, DIRECT_MAX_OPERATOR_TERMS + 1))
        + 2 * sum(math.comb(config_counts["phi1_only"], n) for n in range(DIRECT_MIN_OPERATOR_TERMS, DIRECT_MAX_OPERATOR_TERMS + 1))
        + 2 * sum(math.comb(config_counts["phi2_only"], n) for n in range(DIRECT_MIN_OPERATOR_TERMS, DIRECT_MAX_OPERATOR_TERMS + 1))
        + 4 * sum(math.comb(config_counts["both"], n) for n in range(DIRECT_MIN_OPERATOR_TERMS, DIRECT_MAX_OPERATOR_TERMS + 1))
    )

    low_dim_candidates = by_dim[2] + by_dim[3] + by_dim[4]
    tex = rf"""% Paste this block after the main text.  The manuscript preamble already
% uses REVTeX and defines \Mp and \Lam.
\appendix
\section{{Grammar-defined theory space}}
\label{{app:theory-space}}

The proposal grammar is constructed from local scalar contractions of the
metric, the Riemann tensor and its contractions, and at most two real scalar
fields, $\phi_1$ and $\phi_2$.  We assign canonical dimensions
$[\phi_i]=1$, $[\nabla_\mu]=1$, and
$[R_{{\mu\nu\rho\sigma}}]=[R_{{\mu\nu}}]=[R]=2$.  The production catalog
contains operators of dimensions $2\leq d\leq6$ and permits at most
{TOKEN_CONTEXT_MAX_DERIVATIVES} explicit covariant derivatives in an operator.

For each dimension, the Grammar Masker constructs all legal index
contractions, substitutes the spatially flat FLRW ansatz
\begin{{equation}}
 ds^2=-N(t)^2dt^2+a(t)^2d\boldsymbol{{x}}^2,
 \qquad \phi_i=\phi_i(t),
\end{{equation}}
discards contractions that vanish, and groups expressions that differ by an
exact constant factor on that background.  A generic numerical substitution
is used only to identify possible proportionalities; each proposed relation is
then confirmed by requiring the symbolic ratio to be a number.  In this
precise, code-level sense, the resulting catalog contains 141
\emph{{FLRW-distinct scalar operators}}: {sector_counts['gravity']} pure-gravity
operators, {sector_counts['non-minimal']} scalar--curvature operators, and
{sector_counts['scalar']} pure-scalar operators.  Their dimension counts are
{dim_counts[2]}, {dim_counts[3]}, {dim_counts[4]}, {dim_counts[5]}, and
{dim_counts[6]} for $d=2,3,4,5,6$, respectively.

The qualifier ``FLRW-distinct'' is essential.  This catalog is the implemented
background-search basis, not a complete covariant EFT basis modulo Bianchi
identities, integration by parts, field redefinitions, or perturbative
degeneracy conditions.  Consequently, covariantly different contractions may
be equivalent on FLRW, while operators that differ by a total derivative can
both remain in the catalog.  Covariant viability beyond the homogeneous
background must therefore be checked separately.

\begin{{table}}[t]
\caption{{Composition of the FLRW-distinct operator catalog.  G, NM, and S
denote pure gravity, non-minimal scalar--curvature, and pure scalar sectors.}}
\label{{tab:operator-counts}}
\centering
\small
\begin{{ruledtabular}}
\begin{{tabular}}{{crrrr}}
$d$ & G & NM & S & Total \\
\hline
2 & 1 & 0 & 3 & 4 \\
3 & 0 & 2 & 6 & 8 \\
4 & 4 & 3 & 12 & 19 \\
5 & 0 & 18 & 18 & 36 \\
6 & 15 & 35 & 24 & 74 \\
\hline
All & 20 & 58 & 63 & 141 \\
\end{{tabular}}
\end{{ruledtabular}}
\end{{table}}

\subsection{{Assembly of candidate Lagrangians}}

Let $\mathcal G$, $\mathcal N$, and $\mathcal S$ denote the selected
pure-gravity, non-minimal, and pure-scalar subsets of the catalog.  A proposed
action is compiled as
\begin{{align}}
\mathcal L={{}}&\sqrt{{-g}}\Bigg\{{
 \Mp^2\!\sum_{{I\in\mathcal G\cup\mathcal N}}
 c_I\Lam^{{2-d_I}}\mathcal O_I
 +\sum_{{I\in\mathcal S}}c_I\Lam^{{4-d_I}}\mathcal O_I
 \nonumber\\[-2pt]
&\hspace{{2.2cm}}
 -\frac12\sum_{{i\in\mathcal A}}
 \nabla_\mu\phi_i\nabla^\mu\phi_i
 -\sum_{{i\in\mathcal A}}V_i(\phi_i)\Bigg\}},
\label{{eq:appendix-general-action}}
\end{{align}}
where $c_I$ is dimensionless, $d_I$ is the operator dimension,
$\mathcal A\subseteq\{{1,2\}}$ is the active-scalar set, and $\Lam$ is the EFT
scale.  The factors $\Lam^{{2-d_I}}$ and $\Lam^{{4-d_I}}$ make every term in
the braces dimension four in the conventions of the code.  Each active scalar
has a fixed canonical kinetic term and one of two potential families,
\begin{{equation}}
 V_i^{{\rm quad}}=\frac12m_i^2\phi_i^2,
 \qquad
 V_i^{{\rm ax}}=m_i^2f_i^2
 \left[1-\cos\!\left(\frac{{\phi_i}}{{f_i}}\right)\right].
\end{{equation}}

The allowed scalar configurations are no scalar, $\phi_1$ only, $\phi_2$
only, and both fields.  They admit 20, 52, 52, and 141 catalog operators,
respectively; the corresponding numbers of potential assignments are 1, 2,
2, and 4.  In the production search, the agent selects between
{DIRECT_MIN_OPERATOR_TERMS} and {DIRECT_MAX_OPERATOR_TERMS} nonfixed grammar
operators without replacement.  Activating one scalar adds two fixed terms
(kinetic plus potential), and activating both adds four.  A displayed
Lagrangian therefore contains at most {DIRECT_MAX_OPERATOR_TERMS + 4} terms,
although only the {DIRECT_MAX_OPERATOR_TERMS} selected grammar terms carry
independently proposed coefficients.  Before coefficient sampling, these
defaults define {structure_count:,} distinct scalar-configuration, potential,
and operator-subset choices; the agent samples and ranks a finite subset of
this combinatorial space in each loop rather than enumerating it exhaustively.

\subsection{{Complete operator catalog}}

Tables~\ref{{tab:operators-d2-d4}}--\ref{{tab:operators-d6}} list the exact
operator representatives stored in the production token-context cache.  The
identifier $\mathcal O_n^{{(d,X)}}$ gives the mass dimension $d$, the global
catalog index $n$, and the sector
$X\in\{{\mathrm{{G}},\mathrm{{NM}},\mathrm{{S}}\}}$.  We use
$\Box\equiv\nabla^\mu\nabla_\mu$ only as a typographical abbreviation.
"""

    tex += _catalog_table(
        low_dim_candidates,
        "FLRW-distinct operator representatives of dimensions $d=2,3,4$.  "
        "The dimension and sector are encoded in each operator ID.",
        "tab:operators-d2-d4",
    )
    tex += _catalog_table(
        by_dim[5],
        "FLRW-distinct operator representatives of dimension $d=5$.",
        "tab:operators-d5",
    )
    tex += _catalog_table(
        by_dim[6],
        "FLRW-distinct operator representatives of dimension $d=6$.",
        "tab:operators-d6",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(tex.strip() + "\n", encoding="utf-8")
    print(OUTPUT)
    print(f"operators={len(candidates)} structures={structure_count}")


if __name__ == "__main__":
    main()
