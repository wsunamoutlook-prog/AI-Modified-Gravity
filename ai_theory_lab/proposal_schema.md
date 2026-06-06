# Agent Proposal Schema

Agent proposals should be written as JSON. A proposal contains both the theory structure and explicit numerical parameter samples.

For cold-start theory discovery, proposals must be generated from Grammar Masker rules and current-loop feedback, not from historical Solver winners.

For genuine cold-start discovery, the theory structure should be generated from token-level Grammar Masker rules. Matching against an existing `lagrangians.pkl` entry is allowed for replay, smoke tests, or compatibility checks, but it should not be the source of new cold-start theory choices.

Current harness command:

```bash
python -m ai_theory_lab.harness --proposal ai_theory_lab/proposal_example.json --pretty
```

The harness compiles:

```text
proposal.json
-> agent_lagrangians.pkl
-> agent_parameter_samples.json
-> EOM
-> Builder
-> Solver
-> Solver chi2 feedback
```

## Minimal Shape

```json
{
  "proposal_id": "example_phi1_eh_quadratic",
  "theory": {
    "scalar_config": "phi1_only",
    "potential_types": {
      "phi1": "quadratic",
      "phi2": null
    },
    "operators": [
      {
        "coefficient": "\\alpha",
        "candidate": "R"
      }
    ]
  },
  "parameter_samples": [
    {
      "H0_km_s_Mpc": 61.4,
      "Omega_m0": 0.367,
      "mu1_m1_over_H0": 0.468,
      "fbar1_f1_over_Mp": 0.0592,
      "varphi1_0_phi1_over_Mp": 3.99,
      "lambda_H_Lambda_over_H0": 4169.6
    }
  ],
  "rationale": "Short explanation of why this theory and parameter region were chosen."
}
```

## Theory Fields

- `scalar_config`: one of `none`, `phi1_only`, `phi2_only`, `both`.
- `potential_types.phi1`: `quadratic`, `axion`, or `null`.
- `potential_types.phi2`: `quadratic`, `axion`, or `null`.
- `operators`: non-fixed grammar candidate operators. Fixed scalar kinetic and potential terms are added automatically from `scalar_config` and `potential_types`.

Each operator should use a `candidate` label already present in the Grammar Masker catalog, for example:

- `R`
- `R · R`
- `R · R · R`
- `R^{ab} · R_{ab}`
- `φ1 · φ1 · R`
- `∇^{a}φ1 · ∇^{b}φ1 · R_{ab}`

The `coefficient` field is part of the physical theory, not just metadata. However, the tested Lagrangian is not merely a bare coefficient-weighted sum of operator labels. Grammar Masker balances dimensions by sector:

```text
gravity / non-minimal:  √(-g) M_p² coefficient Λ^(2-d) O_d
pure scalar generated:  √(-g) coefficient Λ^(4-d) O_d
fixed matter terms:     √(-g) O_d
```

Accepted-run reports must reconstruct the full dimension-balanced Lagrangian from the validated pkl object, preferably `agent_lagrangians.pkl` for agent runs. They should show the raw `general` string, the same form with Solver's best-fit coefficient values substituted, and per-term metadata such as `sector`, `mass_dim`, and `lambda_power`. Do not summarize accepted theories by candidate labels alone, and do not write only `coefficient * operator` without the required `M_p²` and `Λ` factors.

Reports must keep accepted theories sorted by Solver `chi2`, but each accepted entry should also include `effective_correction_status`. This is a diagnostic, not a ranking key. It estimates each non-EH, non-fixed-matter curvature correction relative to the Einstein-Hilbert reference. Count terms such as `R²`, `Riemann²`, `φR`, `φ²R`, `□φ R`, and derivative-curvature operators. Do not count standalone pure scalar/self terms as active modified-gravity corrections:

```text
relative_effect_i ~= |c_i / c_EH| * lambda_H^(lambda_power_i) * field_factor_i
```

The status thresholds are `active >= 1e-2`, `moderate >= 1e-4`, `weak >= 1e-6`, and `tiny`/`eh_dominated < 1e-6`. `eh_only` means the theory is a clean EH/scalar baseline with no extra modified-gravity correction terms, and should keep its normal chi-square-derived reward. This helps the agent avoid treating an `EH + scalar + effectively-zero correction terms` fit as a strong modified-gravity discovery signal.

Current compiler behavior:

- The proposal is matched against the existing grammar-generated `lagrangians.pkl` catalog.
- If the structure is not in that catalog, validation fails before EOM.
- This prevents arbitrary illegal symbolic expressions from entering downstream stages.
- This is acceptable for smoke tests and catalog-constrained discovery, but it is not yet a full token-level theory compiler.

## Cold-Start Discovery Restrictions

In a real discovery loop, the agent must not use `solver_result/` or historical top-10 outputs to choose its initial theories or parameters.

Allowed starting information:

- Grammar Masker allowed tokens, sectors, scalar configurations, and candidate operator labels.
- This proposal schema.
- Validation feedback produced by the current loop after each proposal.

Disallowed starting information:

- Historical `model_ranking.csv`.
- Historical `accepted_samples_summary.csv`.
- Historical top-10 reports or plots.
- Parameters copied from previous Solver winners.

Replay experiments may use historical Solver results, but replay is not cold-start discovery and must be labeled separately.

## Unclear / Needs Design Decision

- The current proposal compiler matches against `lagrangians.pkl`. It does not yet build a brand-new legal Lagrangian directly from token sequences or arbitrary operator combinations.
- If the agent must generate theories outside the existing `lagrangians.pkl` pool, we need an offline candidate catalog or a direct `theory JSON -> CandidateScalar -> Lagrangian dict` compiler.
- It is not yet specified whether cold-start parameter samples should begin from broad fixed priors, Latin-hypercube samples, small hand-coded physics priors, or an LLM-chosen distribution.
- It is not yet specified how many parameter samples the agent should propose per theory in early exploration.
- It is not yet specified whether the agent may query `lagrangians.pkl` as a legal operator catalog during cold start, or whether it must only use a separately exported grammar catalog.

## Parameter Samples

`parameter_samples` is a list. Each object is one agent-chosen numerical sample.

Always provide:

- `H0_km_s_Mpc`
- `Omega_m0`
- `lambda_H_Lambda_over_H0`

For phi1 theories, provide:

- `varphi1_0_phi1_over_Mp`
- `mu1_m1_over_H0`
- `fbar1_f1_over_Mp`

For phi2 theories, provide:

- `varphi2_0_phi2_over_Lambda`
- `mu2_m2_over_Lambda`
- `fbar2_f2_over_Lambda`

For two-scalar theories, also provide:

- `q2_0_dvarphi2_dln_a`

In two-scalar models, Solver treats `q2_0_dvarphi2_dln_a` as an agent-sampled free initial velocity while solving `q1_0` from the constraint. Missing this key is a proposal error and should be rejected before the Solver scan.

For free coefficients, provide keys matching the coefficient names:

```json
{
  "\\beta": 1.0e-5,
  "\\gamma": -3.0e-8
}
```

Solver solves constraint-determined initial velocities such as `q1_0` in phi1 models and `q2_0` in phi2-only models. These are written to result CSVs but are not normally proposal inputs. The exception is two-scalar `both` models, where the agent must propose `q2_0_dvarphi2_dln_a` and Solver solves `q1_0`.

## Feedback Contract

After validation, the agent should learn from:

- `validated`
- `chi2`
- `failed_stage`
- `model_ranking.csv`
- `reject_reasons_by_model.csv`
- `agent_parameter_sample_index`
- `attempt_history.jsonl`
- `feedback_summary.json`
- `reflection_prompt.md`

For multi-loop discovery, run the harness with `--memory-dir` so every proposal attempt is appended to current-loop memory:

```bash
python -m ai_theory_lab.harness \
  --proposal <proposal.json> \
  --memory-dir ai_theory_lab/memory/<loop_name> \
  --loop-id <loop_id> \
  --pretty
```

The memory layer records facts only. It summarizes failures, successful Solver entry, chi-square values, parameter sample counts, and theory-family fingerprints. It does not decide that any class of theory should be preferred or avoided.

Before generating the next proposal, the agent should read `reflection_prompt.md` and write a reflection using current-loop facts only. The next `proposal.json` should be based on that reflection, not on historical `solver_result/` outputs or copied old best-fit parameters.

The agent should also read Solver's `all_samples_summary.csv` when present. This file gives one row per parameter sample, including rejected samples, so the agent can learn parameter regions from both finite chi-square values and failure reasons.

Cold-start runs should use a 120s wall-time limit for EOM, Builder, and Solver setup/lambdify. Do not apply this wall to token-level Grammar Masker candidate discovery while building the independent-scalar space. Build the independent-scalar space once per cold-start run and reuse it for all proposal loops in that run. The wall is not the sampling budget; the 1000/3000 parameter sampling policy and early stop threshold control numerical sampling. The 3000-sample expansion should be skipped when the first 1000 samples have no accepted chi-square and are dominated by `q_initial_root_failure`, `q_not_determined`, `no_scalar_constraint`, high-count `constraint_drift`, or high-count `integration_failure`. It should also be skipped for `scalar=none` empty-ranking failures and for no-accepted first passes tagged with `constraint_drift` or `integration_failure`.

Repeated `q_not_determined` feedback should be treated as structural feedback, not a parameter-only failure. The current-loop policy may softly downweight exact operators and operator families that repeatedly cause this tag, especially scalar derivative and scalar-derivative-curvature couplings, while preserving some exploration.

When learning from accepted proposals, treat chi-square quality as part of the label. `chi2 <= 1650` is an excellent accepted signal, `1650 < chi2 <= 1700` is competitive, `1700 < chi2 <= 2000` is acceptable positive feedback, and `chi2 > 2000` should not strongly reinforce the structure. The final learning signal is `discovery_reward`: it starts from the chi-square-based `fit_reward`, keeps clean `eh_only` EH/scalar baselines as valid baselines, downweights `weak` corrections, and penalizes `tiny` or `eh_dominated` extra correction terms. Solver and reports still rank by `chi2`.

## Cold-Start Proposal Requirements

In cold-start discovery, `theory.operators` must contain at least one non-fixed Grammar Masker operator. Pure fixed-matter proposals with no non-fixed operator should be rejected before running the full pipeline.

When the proposal is generated from the current catalog, operator coefficients must be copied exactly from the matched Grammar Masker term metadata. For example, if the catalog term uses `\\alpha`, the proposal should write:

```json
{
  "coefficient": "\\alpha",
  "candidate": "R"
}
```

Do not rename free coefficients or guess generic names. Every non-fixed coefficient in `theory.operators` must be present in every object in `parameter_samples`.

The proposal compiler writes solver-compatible aliases for LaTeX coefficient names. For example, if the proposal provides `\\beta`, the compiled `agent_parameter_samples.json` will also include `beta`. This is an interface compatibility step only; it does not change the theory.

## Accepted Report Contract

After an accepted validation, any human-readable summary should include enough information to reproduce the accepted model:

- raw `general` Lagrangian from the actual validated `agent_lagrangians.pkl` or `lagrangians.pkl` object;
- full symbolic Lagrangian with `√(-g)`, `M_p²`, `Λ` powers, and fixed scalar matter terms;
- full numerical Lagrangian with best-fit coefficient values substituted while preserving `M_p²` and `Λ` factors;
- per-term metadata including `sector`, `mass_dim`, `lambda_power`, fixed/non-fixed status, and whether the term is inside the `M_p²(...)` prefactor;
- fit metrics from Solver;
- initial conditions and sampled values from the accepted row;
- free coupling values and their proposal symbols;
- proposal JSON path and Solver output directory.

This mirrors `solver_result/.../top10_lagrangians_initial_conditions.txt` and improves it for agent runs by pointing to the isolated `agent_lagrangians.pkl`. A report containing only `operators`, or only bare `coefficient * operator` terms, is a structure sketch, not a complete accepted-theory record.
