# EOM Stage

This stage first scalarizes eligible nonlinear algebraic-R sectors, then turns
the resulting representation into equations of motion and applies the FLRW
derivative-order constraints.

For a theory-generating agent, passing this stage means the theory is structurally eligible for numerical preparation. It is not yet a successful theory until the actual Builder code accepts it and the actual Solver code compares it against real data and writes a low `chi2`.

## Role In Pipeline

Input:

- `lagrangians.pkl` from `gr_grammar_masker_v3_2`
- For agent/single-theory validation: `agent_lagrangians.pkl` through `EOM_LAGRANGIANS_PATH`
- Run settings from `EOM v5.2.py`

Output:

- `eom_results/eom_summary.txt`
- `eom_results/eom_results.pkl`
- EOM logs under `log/`
- For agent/single-theory validation: isolated `agent_eom_results/eom_summary.txt`

Downstream consumer:

- `builder_v5_2` parses `eom_results/eom_summary.txt`

## Main Files

- `runner.py`: loads generated Lagrangians, processes them, writes summary and pickle outputs.
- `core.py`: performs symbolic EOM derivation, derivative-order detection, self-tests, and ghost-free coefficient solving.

## Physical Contract

This stage decides whether a candidate Lagrangian is structurally acceptable before numerical solving.

It checks:

- Scalaron classification: `ordinary`, `scalarizable`, or `hybrid`.
- Exact Legendre equivalence of the raw and transformed actions under `chi=R`.
- Raw EOM derivative order.
- Ghost-free coefficient relations.
- Whether final gauged EOMs respect the allowed derivative order.
- Whether a Lagrangian is trivial after constraints.

The scalaron transform is
`f(R,phi_i) -> F(chi,phi_i) R - U(chi,phi_i)`, with
`F = partial f/partial chi` and `U = chi F - f`.  `chi` is an independent
dimension-two field; it must not reuse `phi1` or `phi2` and receives no ad hoc
canonical kinetic term.  Ordinary theories pass through with an unchanged
action and no `E_chi`.  Hybrid residual operators remain subject to the
pre-existing coefficient-cancellation and derivative-order filter.

## Agent Responsibilities

The agent may:

- Read `eom_summary.txt` to understand which theory structures are ghost-free, ghostful, or trivial.
- Use reject patterns to avoid proposing similar high-risk structures in later rounds.
- Suggest controlled changes to work selection, such as `EOM_MAX_TERMS`, `EOM_N_SAMPLES`, or `EOM_N_WORKERS`.

The agent must:

- Treat ghost-free filtering as a hard constraint.
- Preserve the derivative-order constraint unless a human explicitly changes the physical rules.
- Reject a scalaron transform if the symbolic `chi=R` equivalence check fails.
- Keep the raw action, scalarized action, `F`, `U`, and `f_RR` in the serialized
  record so downstream stages can audit the representation.
- Record ghost-free relations and failure reasons for learning.
- Forward ghost-free, nontrivial theories to the real Builder and Solver code before calling them good candidates.
- Use isolated agent inputs/outputs for one-theory validation instead of forcing EOM to process the full 1120-theory batch.
- For harness checks, accept one sampled theory from the existing `lagrangians.pkl` only after it has been rewritten as isolated `agent_lagrangians.pkl` and processed by the real EOM code.

The agent must not:

- Relax ghost-free conditions to improve Solver performance.
- Delete or hide ghostful results.
- Modify EOM equations by hand after this stage.

## Failure Feedback

EOM failures are structural failures before numerical fitting begins. The agent should respond by changing the theory form, not by tuning Solver priors.

Common feedback rules:

- Ghostful or derivative-order violations: remove or replace the operators causing higher-order EOMs; preserve the derivative-order rule unless the user changes the physical assumptions.
- Trivial after constraints: the proposed structure carries no useful dynamics after ghost-free relations. Avoid repeating the same operator combination as a new theory.
- Symbolic intractability at EOM: reduce term count, simplify high-curvature contractions, or test a lower-complexity nearby structure.

Only theories with usable ghost-free EOM sections should move to Builder.

## Useful Environment Settings

- `EOM_LAGRANGIANS_PATH`
- `EOM_OUTPUT_DIR`
- `EOM_MAX_TERMS`
- `EOM_N_SAMPLES`
- `EOM_N_WORKERS`
- `EOM_MAX_ALLOWED_ORDER`
- `EOM_SEED_BASE`
- `EOM_RUN_SELF_TEST`

## Success Criteria

This stage succeeds when `eom_summary.txt` is written and contains usable ghost-free model sections for Builder.

Failures here mean the proposed theory is structurally invalid, ghostful, trivial, or symbolically intractable at the EOM stage.
