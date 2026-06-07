# Grammar Masker Stage

This stage defines the legal theory search space. It generates grammar-valid modified-gravity Lagrangians before any EOM, Builder, or Solver work is attempted.

For a theory-generating agent, this stage is only the first validation gate. A grammar-valid theory is not yet a good theory; it must continue through EOM, Builder, and Solver, and its final quality is judged by real-data `chi2_total`.

The agent may use selected Grammar Masker concepts during proposal, such as allowed tokens, candidate operators, sectors, scalar configurations, and duplicate fingerprints. This is only proposal guidance. It does not replace strict validation by actually running the downstream stage code:

```text
python "EOM v5.2.py"
python "Builder v5.2.py"
python "Solver v5.2.py"
```

For agent-style validation, do not reuse the full batch `lagrangians.pkl` directly as the discovery proposal interface. The preferred discovery path is `graph_agent.py`, where the agent builds or loads the token-level Grammar Masker candidate context, chooses legal `CandidateScalar` operators, scalar configuration, potential type, and parameters, then writes an isolated `agent_lagrangians.pkl` for EOM with `EOM_LAGRANGIANS_PATH`. Random smoke checks may sample one existing theory from `lagrangians.pkl`, but that is replay/debugging, not discovery.

Cold-start proposal compilation constructs the selected Lagrangian directly from legal Grammar Masker candidates. It must use the same sector rules, `M_p²` placement, `Λ` powers, fixed scalar matter terms, and coefficient metadata as `generate_lagrangians`, but it must not call the random `generate_lagrangians(... n_samples=...)` batch generator to choose a finished theory.

For cold-start discovery, the agent must not inspect historical `solver_result/` outputs before proposing. It should propose from Grammar Masker rules, allowed candidate labels, scalar configurations, and current-loop feedback only. Historical Solver winners may be used for replay tests, but replay is not discovery.

## Role In Pipeline

Input:

- Run settings from `GR_grammar_masker_v3.2.py`
- Tensor and FLRW contraction logic from `tensor.py`
- Grammar and candidate generation logic from `grammar.py`

Output:

- `lagrangians.pkl`
- `lagrangians/lagrangians_<n>terms.txt`

Downstream consumer:

- `eom_v5_2` reads `lagrangians.pkl`

## Main Files

- `runner.py`: orchestrates the stage, applies environment settings, writes text and pickle outputs.
- `grammar.py`: defines allowed grammar tokens, dimensions, candidate scalars, scalar configurations, and the batch Lagrangian generator used for ordinary non-agent runs.
- `tensor.py`: builds FLRW tensors and evaluates contractions.

## Theory Space

The grammar supports:

- Curvature targets: `R_SCALAR`, `RIC`, `RIE`
- Scalar fields: `PHI1`, `PHI2`
- Covariant derivatives: `NABLA`
- Scalar configurations: `none`, `phi1_only`, `phi2_only`, `both`
- Potential types: `quadratic`, `axion`
- Sectors: `gravity`, `non-minimal`, `scalar`, `matter`

The generated Lagrangians are structured dictionaries with:

- `n_terms`
- `general`
- `substituted`
- `terms`
- `scalar_config`
- `potential_types`

## Duplicate-Theory Policy

The agent should avoid flooding the pipeline with structurally identical theories. A structural theory fingerprint may be revisited for repeated sampling, different priors, or solver-strategy checks, but in cold-start discovery it must not appear more than 10 times in one experiment history unless the user explicitly asks for repeated sampling.

Two theories should be treated as the same structural theory when they share:

- `scalar_config`
- `potential_types`
- the unordered set of non-fixed candidate operators
- sector labels
- mass dimensions
- lambda powers
- fixed matter content

Do not treat these as new theories by themselves:

- coefficient renaming
- term reordering
- cosmetic rewriting of the same operator labels
- different agent motivation text

The agent may revisit an already-tested fingerprint when it changes something operationally meaningful, such as parameter priors, sample budget, random seed, or solver strategy. When doing so, record why the revisit is useful.

## Feedback From Downstream Stages

Downstream failures should influence future proposal probabilities:

- Repeated Builder timeouts should reduce the probability of very high term counts, many high-curvature contractions, and many derivative curvature operators in one theory.
- Repeated `q1_x` / `q2_x not determined` failures should reduce the probability of coupled scalar derivative structures and two-scalar mixing terms.
- Repeated no-scalar constraint failures should reduce the probability of pure high-curvature no-scalar theories without an Einstein-Hilbert `R` anchor.
- Repeated constraint drift or absurd `H(z)` failures should reduce the probability of highly nonlinear scalar self-interactions and aggressive derivative couplings.

These are proposal-bias rules, not hard grammar bans. The agent may still revisit a risky structure when it explicitly labels the reason, changes the experiment settings, and keeps the duplicate count within the experiment limit.

## Agent Responsibilities

The agent may:

- Propose which term counts, scalar configurations, dimensions, and candidate sectors to explore.
- Suggest search-budget changes such as `MASKER_N_SAMPLES`, `MASKER_N_TERMS_LIST`, or `MASKER_RANDOM_SEED`.
- Use generated candidate metadata to form a structured theory proposal.
- Prefer low-complexity and interpretable candidate combinations during early exploration.
- Use current-loop EOM/Builder/Solver feedback to bias later proposals.

The agent must:

- Treat this stage as the hard legality gate for theory structure.
- Output structured theory specifications, not arbitrary Python code.
- Preserve the grammar constraints unless a human explicitly asks to change the theory space.
- Send grammar-valid theories onward to the full validation chain instead of judging them only by symbolic appearance.
- Never mark a theory as validated merely because it follows part of the Grammar Masker logic; validation requires Solver output with real-data `chi2`.
- In cold-start discovery, avoid using previous `solver_result/` files as prior knowledge.

The agent must not:

- Bypass `GravityMasker`.
- Inject arbitrary symbolic expressions directly into downstream stages.
- Change tensor contractions or dimension-counting rules only to improve data fit.
- Choose theories by looking up previous top-10 Solver outputs before the loop begins.

## Useful Environment Settings

- `MASKER_MAX_DERIVATIVES`
- `MASKER_DIMENSIONS`
- `MASKER_N_TERMS_LIST`
- `MASKER_N_SAMPLES`
- `MASKER_RANDOM_SEED`
- `MASKER_OUTPUT_DIR`
- `MASKER_PICKLE_PATH`

## Success Criteria

This stage succeeds when it writes a valid `lagrangians.pkl` that can be loaded by the EOM stage.

Failures here are theory-space or serialization failures, not data-fit failures.
