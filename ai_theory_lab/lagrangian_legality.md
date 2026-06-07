# Legal Lagrangian Contract

This document defines what counts as a legal agent-proposed Lagrangian for the
AI theory-discovery loop. The source of truth is the Grammar Masker
implementation in `gr_grammar_masker_v3_2/grammar.py`; this file restates the
contract for LLM proposal prompts, proposal validation, and reports.

An agent may propose theory structure, but it must not inject arbitrary
downstream SymPy expressions. A proposal is legal only if it can be represented
by Grammar Masker candidate invariants and compiled into the dimension-balanced
form below.

## Full Form

Every tested Lagrangian is a scalar density of the form:

```text
L = sqrt(-g) [
      M_p^2 ( sum_i c_i Lambda^(2-d_i) O_i
              + sum_j c_j Lambda^(2-d_j) N_j )
      + sum_k c_k Lambda^(4-d_k) S_k
      + fixed scalar matter terms
    ]
```

where:

- `O_i` are pure-gravity Grammar Masker invariants.
- `N_j` are non-minimal scalar-curvature Grammar Masker invariants.
- `S_k` are pure-scalar generated invariants.
- `d_i`, `d_j`, and `d_k` are the `mass_dim` values stored on each candidate.
- `c_i`, `c_j`, and `c_k` are explicit symbolic coefficients such as `\alpha`,
  `\beta`, or later coefficient slots.
- `Lambda` is the EFT cutoff scale.
- `M_p` is the Planck mass.
- The whole bracket is multiplied by `sqrt(-g)`.

The bracket must have total mass dimension 4. Since `sqrt(-g)` is dimensionless
in this convention, each term inside the bracket must be dimension 4 after its
sector prefactor and `Lambda` power are applied.

## Sector Rules

Grammar Masker classifies each non-fixed candidate invariant into one of three
generated sectors:

| Sector | Meaning | Prefactor | Lambda power |
|---|---|---|---|
| `gravity` | Pure curvature, no scalar fields | `M_p^2` | `2 - mass_dim` |
| `non-minimal` | Curvature times `phi1` and/or `phi2` | `M_p^2` | `2 - mass_dim` |
| `scalar` | Pure scalar/self/derivative scalar invariant | none | `4 - mass_dim` |

Fixed scalar matter terms are separate:

| Sector | Meaning | Prefactor | Lambda power |
|---|---|---|---|
| `matter` | Fixed kinetic and potential terms for active scalars | none | `0` |

Thus:

```text
gravity or non-minimal:
  sqrt(-g) M_p^2 c Lambda^(2-d) O_d

pure generated scalar:
  sqrt(-g) c Lambda^(4-d) S_d

fixed scalar matter:
  sqrt(-g) K_or_V
```

An operator list such as `["R", "phi1 * R"]` is not the full tested theory by
itself. The legal theory is the operator list plus its sector, coefficient,
`Lambda` power, `M_p^2` placement, fixed scalar terms, and outer `sqrt(-g)`.

## Grammar Candidate Rules

Generated candidates must come from the Grammar Masker invariant catalog:

- Allowed target tokens are `PHI1`, `PHI2`, `R_SCALAR`, `RIC`, and `RIE`.
- Derivative blocks use `NABLA`.
- The total mass dimension of each candidate is the target dimension generated
  by the masker.
- The default candidate dimensions are `2, 3, 4, 5, 6`.
- The default maximum total derivative count is `2`.
- Candidate blocks are canonically ordered, so reordering equivalent factors is
  not a new theory.
- Zero candidates and candidates proportional to earlier independent candidates
  are removed by the independence filter.

The current token context cache stores the independent candidate catalog only.
It does not contain Solver rankings, accepted chi-square values, or historical
best-fit parameters.

## Scalar Configuration Rules

Allowed scalar configurations are:

```text
none
phi1_only
phi2_only
both
```

Candidate compatibility follows the active scalar family:

- `none`: may use only candidates involving neither `phi1` nor `phi2`.
- `phi1_only`: may use candidates involving `phi1`, but not `phi2`.
- `phi2_only`: may use candidates involving `phi2`, but not `phi1`.
- `both`: may use any Grammar Masker candidate.

When a scalar is active, Grammar Masker adds fixed scalar matter terms:

```text
-1/2 g^{mu nu} nabla_mu phi_i nabla_nu phi_i
```

and one fixed potential:

```text
quadratic: -1/2 m_i^2 phi_i^2
axion:     -m_i^2 f_i^2 (1 - cos(phi_i / f_i))
```

These fixed matter terms use coefficient `1`, sector `matter`, `mass_dim=4`,
and `lambda_power=0`.

## Coefficient Rules

Every non-fixed generated candidate must have a symbolic coefficient. Existing
Grammar Masker terms use Greek coefficient symbols in order:

```text
\alpha, \beta, \gamma, \delta, ...
```

The coefficient is part of the physical theory. It must be included in every
explicit parameter sample unless the Solver fixes that coefficient by rule. In
the current sampling policy, the Einstein-Hilbert `R` coefficient is fixed to:

```text
\alpha = 0.5
```

for the `R` operator when it is present as the EH anchor.

Coefficient renaming, term reordering, or changing only coefficient labels does
not create a genuinely new structural theory.

## Proposal Interface Rules

Agent proposal JSON may list candidate operators compactly, but the compiler
must recover the full dimension-balanced Lagrangian from Grammar Masker
metadata. A legal proposal must include:

- `scalar_config`
- `potential_types`
- at least one non-fixed Grammar Masker operator
- exact candidate labels from the Grammar Masker catalog
- exact coefficient symbols for those candidates
- explicit numerical parameter samples

The proposal agent must not submit:

- arbitrary SymPy expressions
- bare `coefficient * operator` sums without sector balancing
- terms missing `sqrt(-g)`
- gravity or non-minimal terms missing the `M_p^2` prefactor
- generated terms missing the required `Lambda` power
- terms whose dimension-balanced contribution is not mass dimension 4
- scalar terms incompatible with the selected scalar configuration

## Report Rules

Accepted-theory reports must show the full validated Lagrangian from
`agent_lagrangians.pkl` or `lagrangians.pkl`, not only the operator list. For
each accepted representative, reports should include:

- raw `general` Lagrangian string with `sqrt(-g)`, `M_p^2`, and `Lambda` powers
- numerical best-fit coefficient-substituted form when available
- per-term `sector`
- per-term `mass_dim`
- per-term `lambda_power`
- fixed/non-fixed status
- coefficient values and scalar parameter values from the Solver row

This is required because the same candidate label can have a different physical
scale depending on its sector and `Lambda` power.
