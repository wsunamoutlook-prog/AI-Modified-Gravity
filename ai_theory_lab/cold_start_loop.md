# Cold-Start Theory-Generating Agent Loop

This document defines the correct loop for an agent that is genuinely generating theories, not replaying historical best models.

## Rule

At loop start, the agent must not inspect historical `solver_result/` outputs.

Do not use:

- historical `model_ranking.csv`
- historical `accepted_samples_summary.csv`
- top-10 reports
- top-10 plots
- best-fit parameters copied from old Solver runs

Those files are allowed only for replay tests, regression tests, or debugging.

## Allowed Starting Context

The agent may use:

- `AGENTS.md`
- stage-specific `AGENT.md` files
- `ai_theory_lab/proposal_schema.md`
- Grammar Masker token-level rules and candidate labels
- constraints encoded by the proposal compiler

## Loop

Baseline runner:

```bash
python -m ai_theory_lab.cold_start_runner --loops 20 --pretty
```

LangGraph runner:

```bash
python -m ai_theory_lab.graph_agent --loops 20 --pretty
```

Use `graph_agent.py` when testing LangGraph as the agent-loop controller. It keeps the same deterministic token-level generation helpers, harness validation, memory updates, and isolated agent files as `cold_start_runner.py`, but LangGraph owns the loop state and branching between initial validation, expanded sampling, skipping, and stopping.

Token-level independent-scalar discovery may be loaded from `ai_theory_lab/cache/`. This cache stores only Grammar Masker candidate-discovery state, not Solver winners, chi-square rankings, accepted samples, or best-fit parameters, so it is allowed in cold-start discovery. Use `--no-token-context-cache` to force a rebuild.

In the LangGraph runner, each validation is followed by deterministic reflection and an explicit decision record. The graph writes `loop_trace.jsonl` under the proposal run directory. Each trace row contains the loop's validation rows, reflection, decision, and summary facts. This makes the loop ready for a future LLM planner node without requiring API access yet.

```text
1. Read grammar/proposal rules.
2. Generate a new theory from token-level Grammar Masker rules, not by selecting a pre-existing full structure from `lagrangians.pkl`.
3. Generate a new proposal.json:
   - theory.scalar_config
   - theory.potential_types
   - theory.operators
   - parameter_samples
   - rationale
4. Run:
   python -m ai_theory_lab.harness --proposal <proposal.json> --memory-dir <current_loop_memory_dir> --loop-id <loop_id> --pretty
5. Read feedback from this run only:
   - validated
   - chi2
   - failed_stage
   - top reject reasons
   - accepted/rejected parameter sample indices
   - `all_samples_summary.csv`
6. Read the updated current-loop memory:
   - `attempt_history.jsonl`
   - `feedback_summary.json`
   - `reflection_prompt.md`
7. Write a reflection from current-loop facts only.
8. Generate the next proposal from the reflection.
9. At the end of a multi-loop run, generate a result report:

   ```bash
   python -m ai_theory_lab.report --run-name <run_name> --top-n 20
   ```

   The report must be written under `ai_theory_lab/reports/<run_name>/` and must include this fixed artifact set:

   - `summary.md`
   - `accepted_lagrangians_and_parameters.md`
   - `accepted_lagrangians_full.md`
   - `accepted_lagrangians_and_parameters.csv`
   - `accepted_summary.json`
   - `accepted_family_representatives.json`
   - `accepted_chi2_bar.png`
   - `top_h_overlay.png`
   - `top3_h_panels.png`

   The report must include h(z) plots, accepted chi-square plots, complete accepted Lagrangians, best-fit parameter values, and Solver output paths. The `summary.md` page itself must include the parameter choices for the top accepted models, not only links to detailed files.
```

## Accepted-Theory Reports

When the agent summarizes accepted models, it must write the full tested Lagrangian, not only a list of operators. Use the Solver top-model report style:

- raw `general` Lagrangian from the actual validated `agent_lagrangians.pkl` or `lagrangians.pkl` object;
- symbolic Lagrangian with `√(-g)`, `M_p²` prefactors, `Λ` powers used to balance mass dimension, and fixed scalar matter terms;
- numerical Lagrangian with best-fit coefficient values substituted from `model_ranking.csv`;
- per-term metadata including `sector`, `mass_dim`, `lambda_power`, fixed/non-fixed status, and whether the term is inside the `M_p²(...)` prefactor;
- fit metrics including `chi2`, `chi2_SN`, `chi2_BAO`, AIC/BIC, `k_params`, and max constraint error;
- initial conditions and sampled values such as `H0`, `Omega_m0`, `lambda_H`, scalar initial values, masses, decay constants, and solved scalar velocities;
- free coupling values with the proposal coefficient symbol they came from;
- proposal JSON path and Solver output files.

A report that lists only `theory.operators`, or only `coefficient * operator` without the `M_p²`/`Λ` normalization, is incomplete. Operator lists are useful for quick structure comparison, but they do not specify the dimension-balanced theory that EOM, Builder, and Solver actually validated.

For every completed multi-loop cold-start or LangGraph agent run, this report is mandatory. Do not only give a chat summary. Generate the report folder and point the user to it. The h(z) plots must be made from the accepted Solver solution CSVs, not from guessed curves or historical `solver_result/` plots. The front-page `summary.md` must show the top accepted models' parameter choices, including `agent_parameter_sample_index`, `H0`, `Omega_m0`, `lambda_H`, scalar initial values, mass/decay parameters, scalar velocities where present, and compact free-coefficient values.

The files `accepted_lagrangians_and_parameters.md`, `accepted_lagrangians_full.md`, `accepted_lagrangians_and_parameters.csv`, `accepted_summary.json`, `accepted_family_representatives.json`, `summary.md`, and the h(z)/chi-square plots are part of the required run output. If the run has accepted models, these files must be populated from the actual validated Solver outputs. If the run has no accepted models, still create the markdown/CSV/JSON files with a clear no-accepted-model note.

The agent-facing memory should keep every accepted attempt. Human-facing report files should show one best chi-square representative per theory family so repeated similar accepted theories do not crowd out distinct families. Use `coarse_family_key` for this best-per-family display when available, falling back to exact `family_key`.

## Parameter Search Policy

For each proposed theory, the agent should choose all free numerical parameters explicitly.

Default policy:

- Apply a 120s wall-time limit to EOM, Builder, and Solver setup/lambdify.
- Do not apply this 120s wall to token-level Grammar Masker candidate discovery while building the independent-scalar space.
- Build the independent-scalar candidate space once at the start of a cold-start run, then reuse it for every proposal loop in that run.
- Apply the same 120s wall to each per-loop token-level proposal generation attempt after the candidate space has been built. If one proposal attempt times out, record it as a `GrammarGeneration`/`pre_sampling_timeout` failure and continue to the next loop.
- If a pre-sampling stage exceeds 120s, skip that theory and record the timeout as feedback.
- Generate 1000 parameter samples for the theory.
- Run the real Solver with those explicit samples.
- Do not stop the agent run early because a sample reaches low chi-square. Low chi-square is recorded as a quality label and learning signal, but the requested loop count should still run unless a hard failure stops initialization.
- If the first 1000 samples do not produce any sample with `chi2 < 2000`, generate and test 3000 parameter samples for the same theory before giving up on that theory family.
- If the first 1000 samples produce no accepted `chi2` and the reject feedback is structural or dominated by hard numerical failures, skip the 3000-sample expansion and change the theory structure instead. Skip-trigger feedback includes `q_initial_root_failure`, repeated `q_not_determined`, repeated `no_scalar_constraint`, high-count `constraint_drift`, high-count `integration_failure`, pre-sampling timeout, or symbolic timeout.
- Record every parameter sample, including rejected samples, in Solver's `all_samples_summary.csv`.

The 120s wall is not applied to the numerical sampling budget itself. Sampling is controlled by the 1000/3000 sample policy and structural skip rules.

The independent-scalar discovery step should not be repeated for every loop. Repeating it wastes time and prevents the agent from reaching EOM/Builder/Solver feedback.

The agent must read per-sample feedback from `all_samples_summary.csv`, not just the best `model_ranking.csv`. Future parameter proposals should be based on which individual samples were accepted, rejected, numerically unstable, or close to the chi-square target.

For two-scalar `both` models, every parameter sample must include `q2_0_dvarphi2_dln_a`. Solver uses that sampled value while solving `q1_0` from the constraint. Missing `q2_0_dvarphi2_dln_a` is a proposal-interface error, not a physical rejection.

## Current-Loop Memory

The harness memory layer records facts. It should not hard-code what the agent must do next.

The memory files are:

- `attempt_history.jsonl`: one structured record per proposal attempt.
- `feedback_summary.json`: aggregate facts such as failed-stage counts, failure-tag counts, solver-entry counts, best chi-square, best AIC-equivalent structure score, and theory-family summaries.
- `reflection_prompt.md`: the prompt the agent should read before producing the next proposal.
- `training_dataset.jsonl`: one record per validation stage, including theory features, result, raw chi-square, AIC/BIC, effective `k`, parameter reward, structure reward, failure tags, stage lineage, and feedback paths.
- `policy_summary.json`: empirical feature/operator/family rewards learned from the current loop.
- `agent_reflections.jsonl`: reflection records produced after validation attempts.
- `structure_prior.json`: structure preferences learned from current-loop accepted and failed attempts.
- `parameter_prior.json`: parameter ranges learned from accepted Solver sample rows.
- `joint_parameter_prior.json`: structure-conditioned parameter vectors learned from current-loop sample rows.

`structure_prior.json` records scalar-family learning with the same diagnostics for `none`, `phi1_only`, `phi2_only`, and `both`: Solver reachability, accepted-sample rate, q-root failure rate, `q_not_determined` rate, numerical-failure rates, best/median chi-square, best/median AIC-equivalent structure score, and operator-family counts. These diagnostics are used for soft, current-loop sampling adjustments. They are not a manual rule to privilege or punish `phi2` or any other scalar family, and every legal scalar family keeps a nonzero exploration floor.

`joint_parameter_prior.json` is the first memory layer that couples theory structure and numerical parameters. It groups sample-level reward records by exact theory family, coarse theory family, scalar family, and global fallback. These sample-level rewards use raw chi-square only: within a fixed Lagrangian, `k` is constant and AIC cannot change the parameter-vector ordering. When a later proposal matches one of those levels, the sampler can seed `H0`, `Omega_m0`, `lambda_H`, scalar initial values, scalar masses/decay constants, and sampled scalar velocities from high-reward vectors before recomputing free correction coefficients for the current operator set. Exact samples reuse stored vectors; random samples jitter around them in log space. The configured `joint_prior_usage_fraction`, currently `0.80`, keeps part of the sample budget on the ordinary learned/default priors as an exploration floor. If the matching groups have no positive current-loop evidence, the sampler falls back to the ordinary learned/default priors.

The agent should use these files to infer its own next proposal policy. For example, it may notice repeated Builder failures or repeated no-scalar constraint failures, but the decision about what to change belongs in the agent's reflection.

When current-loop memory contains accepted low-AIC theories, the next proposal policy should raise the probability of their shared features. If AIC-competitive attempts share `phi1_only`, an `R` anchor, and a simple scalar-curvature coupling, the agent should sample more from that neighborhood while preserving some exploration. This uses only current-loop feedback; historical `solver_result/` outputs remain out of scope for cold-start discovery.

Different Lagrangian structures are compared with

```text
structure_score = AIC - 2*k_LCDM = chi2 + 2*(k_model-k_LCDM),  k_LCDM=3.
```

Subtracting the constant reference penalty leaves exact AIC ordering unchanged. Accepted structures are quality-tiered by this score before they are used as positive feedback:

- `structure_score <= 1650`: excellent signal.
- `1650 < structure_score <= 1700`: competitive signal.
- `1700 < structure_score <= 2000`: acceptable positive signal.
- `structure_score > 2000`: poor accepted signal, with weaker or negative reinforcement depending on distance from 2000.

Excellent and competitive accepted attempts should have the strongest influence on structure priors. Acceptable attempts up to `structure_score <= 2000` should still provide useful positive feedback, but they should not dominate over lower-AIC models. Raw chi-square remains the parameter-learning metric, the expansion/refinement trigger, and the primary human-facing ranking. Initial, expanded, and refined stages stay in history, but the best validated AIC stage represents that lineage exactly once in structural learning.

`k_model` is the effective free-parameter count after ghost-cancellation substitutions and Builder reduction. Cancelled coefficients, fixed normalizations, and constraint-solved initial velocities are excluded. The profiled DES-SN offset and DESI BAO scale are included. `H0` is included only when it remains in the dimensionless dynamics; it is not counted when it appears solely as an absolute distance scale removed by the profiled likelihood. The current flat-LCDM reference therefore has `k_LCDM=3`: `Omega_m0`, `M_SN`, and `alpha_BAO`.

Accepted attempts also carry an effective-correction diagnostic. Reports and Solver rankings remain sorted by `chi2`, but the learned structure policy uses AIC-based `discovery_reward`, which downweights competitive structures whose non-EH curvature corrections are negligible relative to the Einstein-Hilbert term. Count modified-gravity corrections such as `R²`, `Riemann²`, `φR`, `φ²R`, `□φ R`, and derivative-curvature terms. Do not count pure scalar/self terms such as standalone `φ²` or standalone `□φ` as active modified-gravity corrections. For each counted correction, estimate

```text
relative_effect_i ~= |c_i / c_EH| * lambda_H^(lambda_power_i) * field_factor_i
```

with `lambda_H = Lambda/H0` from the accepted sample and `lambda_power_i` from the validated term metadata. Classify the accepted model by `max_relative_effect_to_EH`: `active >= 1e-2`, `moderate >= 1e-4`, `weak >= 1e-6`, and `tiny`/`eh_dominated < 1e-6`. `unclear` means required coefficient, EH reference, `lambda_H`, or term metadata is missing.

The report should show `effective_correction_status`, `max_relative_effect_to_EH`, and `dominant_correction_term` next to the chi-square-ranked accepted family representatives. A model can remain the best chi-square model while being labeled `eh_dominated`; that label changes the learning reward, not the Solver ranking.

The runner now has a lightweight learned policy layer. It converts current-loop attempts into `training_dataset.jsonl`, summarizes empirical rewards in `policy_summary.json`, and adds the learned score to candidate-theory selection. This is a small interpretable policy model, not an LLM fine-tune.

Mini-batch runs default to `--group-mode open_only`: every initial-theory slot is assigned to unrestricted `open_search`, and no budget is reserved for a dedicated `non_eh` proposal sector. This is not an EH-only restriction. The generated theory is classified after proposal and may still be `eh_anchored`, `non_eh`, or `non_gravity`. Use `--group-mode sector_split` only for an explicit legacy reproduction or ablation experiment; that mode retains the old 50/50 allocation between unrestricted `open_search` and forced `non_eh`. There is no separate default `EH + phi2_only` sector.

Scalar-family selection uses sector-specific exploration floors before applying reward learning. In `open_search`, each proposal first selects a scalar family from this schedule:

```text
phi1_only: 8% fixed baseline
phi2_only: 8% fixed baseline
both:      8% fixed baseline
none:      8% fixed baseline
reward-weighted choice among the four families: 68%
```

The reward-weighted 68% uses current-loop `policy_summary.json` evidence from the same `open_search` sector. If no scalar family has positive reward evidence yet, that portion falls back to a uniform draw.

When legacy `sector_split` is requested explicitly, each proposal in its dedicated `non_eh` sector uses a stronger scalar-family exploration floor:

```text
phi1_only: 15% fixed baseline
phi2_only: 15% fixed baseline
both:      15% fixed baseline
none:      15% fixed baseline
reward-weighted choice among the four families: 40%
```

The reward-weighted 40% uses current-loop `policy_summary.json` evidence from the same `non_eh` sector. If no scalar family has positive reward evidence yet, that 40% falls back to a uniform draw. This rule is dormant in the default `open_only` mode. EH-anchored track-split proposal modes continue to use the ordinary broad proposal policy unless they are run through `open_search`.

Production cluster discovery uses `--scheduler async_slots`. Each slot validates a batch of one theory in an isolated run directory. As soon as its initial validation and any triggered expanded/refined pass finish, the records are committed under `.memory.lock` to the shared current-loop memory, and the freed slot proposes a replacement using that updated memory. Other slots keep running throughout, so one slow theory cannot hold back a wave or a runtime class. The global `--target-attempts` counts initial theories; expanded and refined passes are recorded separately and do not consume that target. On an 8-CPU job, the production setting is `--slot-count 8 --slot-workers 1`.

For a crashed or externally interrupted production run, pass `--resume` with
the same run name and scientific settings. The runner recounts completed
initial attempts from `attempt_history.jsonl`, preserves the learned priors,
skips all existing task numbers, and generates replacements for work that was
in flight but never recorded. Monitoring treats each resume as a new active
segment and excludes the stopped interval from throughput.

The runner still records structural complexity and a learned expected-runtime estimate in proposal and scheduler logs. Under `async_slots` these are diagnostic fields and runtime-prior inputs, not hard queues. The legacy `wave` scheduler retains wave-level runtime quartiles, while `async_lanes` retains independently replenished `simple`, `medium`, `complex`, and `very_complex` queues with optional balanced lane floors. Keep those modes only for reproduction or scheduler ablations. All schedulers rely on `.memory.lock` around `record_attempt` so concurrent completions cannot corrupt `attempt_history.jsonl`, `policy_summary.json`, or `feedback_summary.json`.

## Agent Loop

The cold-start runner should execute this loop explicitly:

```text
generate theory
-> run harness
-> read feedback_summary + all_samples_summary
-> write reflection
-> update structure prior + parameter prior
-> generate next theory
```

The structure prior is learned from accepted low-AIC attempts and repeated structural failures. It should learn both exact fingerprints and coarse families, but scalar-family feedback must be symmetric: the same accepted-rate, q-root, `q_not_determined`, numerical-failure, chi-square, AIC, and effective-parameter-count diagnostics are computed for `none`, `phi1_only`, `phi2_only`, and `both`. Repeated bad evidence may softly downweight a nearby family/operator bucket, while successful low-AIC evidence may softly raise it, but no legal scalar family should be eliminated. Repeated `q_not_determined` should also be summarized at the operator level; exact operators and coarse structures that often lead to unusable `q1_x` or `q2_x` RHS extraction may receive a soft downweight, especially scalar derivative and scalar-derivative-curvature couplings. The parameter prior is learned from accepted rows in Solver's `all_samples_summary.csv` using raw chi-square; it estimates quantile ranges for common cosmological, scalar, and coefficient parameters. The next proposal should sample from these priors when enough accepted current-loop data exists, and fall back to the broad cold-start prior otherwise.

Parameter-prior updates are intentionally delayed. `H0_km_s_Mpc` remains fixed to the default `config_p.py` range. Other parameters use the broad default range until the loop has at least 10 attempts and at least 100 accepted Solver sample rows; only then may `parameter_prior.json` become active. `joint_parameter_prior.json` is separate: it can record and reuse positive current-loop sample vectors earlier, but only through the exact/coarse/scalar/global fallback hierarchy and only as proposal-time seeding.

Default broad parameter priors are centralized in `ai_theory_lab/config_p.py`. Do not hard-code these ranges in the runner; import them from that config file so the agent and documentation agree about the sampling space.

The scalar exploration prior is broad by default. Positive scale parameters use log sampling: `varphi1_0_phi1_over_Mp` in `1e-3..1e1`, `mu1_m1_over_H0` in `1e-2..1e2`, `fbar1_f1_over_Mp` in `1e-2..1e2`, `mu2_m2_over_Lambda` in `1e-5..1e5`, and `fbar2_f2_over_Lambda` in `1e-5..1e5`. Sign-sensitive phi2 quantities use signed-log sampling: `varphi2_0_phi2_over_Lambda` and `q2_0_dvarphi2_dln_a` draw both signs with `|value|` in `1e-5..1e5`.

## Feedback Categories

The feedback summary may include categories such as:

- Builder failures.
- Solver failures.
- no-scalar constraint failures.
- `q1_x` / `q2_x` not determined.
- symbolic timeout.
- constraint drift.
- `H(z) absurdly large`.
- accepted low-chi-square samples.

These categories are observations, not policy rules. The proposal agent must write its own explanation and next-step plan from the facts before generating the next `proposal.json`.

Repeated `q_not_determined` failures should reduce repeated attempts in nearby structures, but should not fully ban legal grammar families. Keep some exploration while making the current-loop policy less likely to repeat exact operators or scalar-derivative couplings that repeatedly fail RHS extraction.

## Proposal Strictness

Each cold-start `proposal.json` must include at least one non-fixed Grammar Masker operator in `theory.operators`. A proposal containing only fixed scalar kinetic/potential matter terms is not a valid theory proposal for this loop, because it does not introduce a non-fixed modified-gravity structure for EOM/Builder/Solver to test.

For the current catalog-matching implementation, each operator entry must carry the exact coefficient symbol from the matched Grammar Masker catalog term:

```json
{
  "coefficient": "\\alpha",
  "candidate": "R"
}
```

The agent must not invent coefficient names such as `\\beta` or `\\gamma` unless those exact symbols are present in the catalog entry for the proposed theory. Every non-fixed coefficient symbol in `theory.operators` must appear in every `parameter_samples` object. Missing coefficient values are proposal-generation errors, not physical failures.

## Current Implementation Limitation

The current strict compiler can still match proposal JSON against structures already present in `lagrangians.pkl` for replay or compatibility tests. A genuine cold-start discovery agent should instead generate a fresh theory through token-level Grammar Masker rules and write an isolated run input for EOM/Builder/Solver.

Open design questions:

- Should we export a separate operator catalog so the agent can compose new legal theories without reading generated full Lagrangians?
- What initial parameter prior should be used when there is no current-loop feedback yet?
