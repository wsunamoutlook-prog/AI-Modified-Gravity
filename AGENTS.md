# AI Modified Gravity Agent Guide

This file is the project-level guide for coding agents working in this repository. Read it first, then read the stage-specific `AGENT.md` files before changing or running a pipeline stage.

## Project Goal

This project searches for viable modified-gravity theories with two scalar fields. Candidate theories are generated inside a grammar-constrained theory space, filtered by symbolic EOM and ghost-free constraints, converted into numerical models, and compared against DES-SN + DESI-DR2 BAO data.

The long-term goal is an AI theory-discovery loop:

```text
propose theory -> validate grammar -> EOM ghost-free check -> Builder cache -> Solver scan -> score -> learn from results -> propose again
```

The agent proposes and analyzes candidate theories. The deterministic physics pipeline decides legality and data fit.

## Theory Validation Loop

A theory-generating agent must treat theory proposal as the start of a full validation process, not as the final product. Every proposed theory should be pushed through the complete pipeline whenever feasible:

```text
Grammar validity -> EOM ghost-free check -> Builder conversion -> Solver real-data comparison
```

The agent may use only part of the Grammar Masker logic to propose candidates, such as grammar tokens, candidate operators, scalar configurations, or structural fingerprints. That proposal-time shortcut is not validation. Validation requires actually running the project code for all downstream stages:

```text
python "EOM v5.2.py"
python "Builder v5.2.py"
python "Solver v5.2.py"
```

Only theories that pass the real EOM code, real Builder code, and real Solver code, and are compared against real DES-SN + DESI-DR2 BAO data, should be considered viable candidates. The main quality signal is the `chi2` value written by Solver:

```text
lower chi2_total means a better data fit
```

The agent should learn from both successful low-chi2 theories and rejected theories. A theory that looks elegant symbolically is not considered good unless it survives the pipeline and achieves competitive real-data chi-square.

## Cold-Start Discovery Rule

For a genuine theory-generating agent run, do not initialize from historical Solver winners.

At the start of a cold-start discovery loop, the agent may read:

- Grammar Masker rules and candidate/operator documentation.
- Stage `AGENT.md` files.
- The proposal schema.
- Its own proposals and validation feedback generated during the current loop.

At the start of a cold-start discovery loop, the agent must not read:

- `solver_result/` rankings, top-10 reports, or accepted-sample CSVs from previous human or batch runs.
- historical best-fit parameters from prior Solver runs.
- previous run plots as a source of proposal choices.

Historical Solver outputs may be used only for separate debugging, regression tests, or replay validation, and that mode must be labeled as replay rather than discovery.

The correct cold-start loop is:

```text
read grammar rules
-> generate a new theory from token-level Grammar Masker rules
-> write a grammar-constrained theory JSON
-> propose explicit parameter_samples
-> run harness --proposal
-> read only this loop's validation feedback
-> update this loop's memory
-> write a reflection from current-loop facts
-> propose the next theory/parameters
```

The agent may exploit its own current-loop memory after feedback is produced. The memory should record facts such as failed stages, rejection reasons, stage reachability, theory fingerprints, parameter sample counts, and chi-square values. The memory should not hard-code policy updates. The proposal agent should read those facts, write its own reflection, and then decide the next theory/parameter proposal.

## Pipeline Order

Run stages in this order:

```text
1. Grammar Masker
   python "GR_grammar_masker_v3.2.py"

2. EOM
   python "EOM v5.2.py"

3. Builder
   python "Builder v5.2.py"

4. Solver
   python "Solver v5.2.py"
```

Stage details live in:

- `gr_grammar_masker_v3_2/AGENT.md`
- `eom_v5_2/AGENT.md`
- `builder_v5_2/AGENT.md`
- `solver_v5_2/AGENT.md`

## Environment

Use the project-local virtual environment:

```bash
source .venv/bin/activate
python --version
```

Expected Python:

```text
Python 3.12.x
```

The `.venv` contains LangGraph, LangChain, LangSmith, OpenAI SDK, Gemini SDK, and the scientific packages needed by the current v5.2 pipeline.

If matplotlib cache warnings appear, set:

```bash
export MPLCONFIGDIR="$PWD/.matplotlib-cache"
```

## Repository Structure

Important root entry points:

- `GR_grammar_masker_v3.2.py`: editable settings and launcher for theory generation.
- `EOM v5.2.py`: editable settings and launcher for ghost-free EOM analysis.
- `Builder v5.2.py`: editable settings and launcher for build-cache generation.
- `Solver v5.2.py`: editable settings and launcher for numerical solving and ranking.

Implementation packages:

- `gr_grammar_masker_v3_2/`
- `eom_v5_2/`
- `builder_v5_2/`
- `solver_v5_2/`

Main generated artifacts:

- `lagrangians.pkl`
- `lagrangians/`
- `eom_results/`
- `solver_result/`
- `log/`

## Agent Rules

The agent may:

- Propose structured candidate theory specifications.
- Adjust run settings, sample budgets, scalar-configuration filters, and parameter priors when the user asks or when an experiment requires it.
- Read output CSVs and reports to summarize successful and failed theories.
- Add orchestration code for LangGraph/LangSmith around the existing pipeline.
- Add documentation that helps future agents understand the pipeline.

The agent must:

- Preserve the pipeline order unless explicitly asked otherwise.
- Keep theory generation grammar-constrained.
- Treat partial Grammar Masker compliance during proposal as insufficient for validation; verified theories must come from actually running EOM, Builder, and Solver and reading Solver's `chi2`.
- Avoid repeatedly proposing structurally identical theories. In cold-start discovery, the same structural theory fingerprint must not appear more than 10 times across one experiment history unless the user explicitly asks for repeated sampling.
- Treat ghost-free filtering as a hard physical constraint.
- Treat Builder rejection as a structural/numerical-preparation failure.
- Treat Solver rejection reasons as learning signals, not noise to hide.
- Record enough settings to reproduce an experiment.
- When summarizing accepted theories, write the complete dimension-balanced Lagrangian from the actual validated `agent_lagrangians.pkl` or `lagrangians.pkl` object, not only the operator list. Include `√(-g)`, `M_p²` prefactors for gravity/non-minimal sectors, `Λ` powers used for mass-dimension balancing, fixed scalar matter terms, and the numerical best-fit coefficient-substituted form from Solver output.
- Rank Solver results primarily by `chi2`, unless the user explicitly requests another metric.

The agent must not:

- Bypass the Grammar Masker by injecting arbitrary downstream symbolic expressions.
- Treat coefficient renaming or term reordering as a genuinely new theory.
- Estimate, hallucinate, or self-judge `chi2` without running the real Solver code.
- Relax ghost-free, derivative-order, constraint-drift, or EFT cuts only to improve fit.
- Manually edit cached model objects or result CSVs to change rankings.
- Delete generated results unless the user explicitly asks.
- Revert unrelated user changes in the working tree.

## Current Ranking Rule

Solver ranking is by total chi-square:

```text
chi2_total = chi2_DES_SN + chi2_DESI_DR2_BAO
```

Sort key:

```text
(chi2_total, AIC)
```

AIC and BIC are still computed and written for reference, but AIC is not the primary ranking metric.

## AI Orchestration Direction

Future AI orchestration should be built as an outer loop around the existing deterministic stages.

Recommended layout:

```text
ai_theory_lab/
  harness.py
  memory.py
  graph.py
  state.py
  validation_result.py
```

Validation should go through the harness:

```bash
python -m ai_theory_lab.harness --proposal ai_theory_lab/proposal_example.json
```

For a multi-loop discovery run, also attach a current-loop memory directory:

```bash
python -m ai_theory_lab.harness \
  --proposal path/to/proposal.json \
  --memory-dir ai_theory_lab/memory/<loop_name> \
  --loop-id loop_01 \
  --pretty
```

The harness is responsible for actually running EOM, Builder, and Solver, capturing stdout/stderr tails on failure, reading `model_ranking.csv`, and returning Solver's real `chi2`. A proposal agent should revise its theory and parameter choices when the harness returns `validated=false` and should inspect the returned failed stage, diagnostics, and logs.

When `--memory-dir` is used, the harness writes:

- `attempt_history.jsonl`: one fact record per proposal attempt.
- `feedback_summary.json`: aggregate facts from the current discovery loop.
- `reflection_prompt.md`: a prompt asking the proposal agent to infer its own next move from current-loop facts.
- `training_dataset.jsonl`: one learning record per attempt, with theory features, outcome, reward, failure tags, chi-square, and feedback paths.
- `policy_summary.json`: an interpretable learned policy summary, containing empirical rewards by feature, operator, and theory family.
- `agent_reflections.jsonl`: one reflection record after each validation attempt.
- `structure_prior.json`: the current-loop learned structure prior used by the next proposal.
- `parameter_prior.json`: the current-loop learned parameter prior inferred from accepted rows in Solver's `all_samples_summary.csv`.
- `joint_parameter_prior.json`: the current-loop structure-conditioned parameter memory inferred from all sample rows, grouped by exact theory family, coarse theory family, scalar family, and global fallback.

These files are current-loop memory. They are allowed for cold-start discovery. Historical `solver_result/` files are still not allowed as proposal memory.

`structure_prior.json` should include `scalar_family_learning.metrics`. These metrics are diagnostic, not a manual bias table. The same fields must be recorded for `none`, `phi1_only`, `phi2_only`, and `both`, including Solver reachability, accepted-sample rate, q-root failure rate, `q_not_determined` rate, numerical-failure rates, best/median chi-square, and operator-family counts. The proposal policy may use these metrics for soft sampling adjustments, but every legal scalar family must keep a nonzero exploration floor.

When current-loop feedback contains successful low-chi-square attempts, future proposals should increase the sampling probability of shared features from those successful attempts. For example, if accepted attempts are mostly `phi1_only` theories with an `R` anchor and a simple scalar-curvature coupling, the next proposals should favor that family while still keeping some exploration. This is a current-loop feedback update, not permission to inspect historical Solver winners.

The cold-start runner may use the current loop's `policy_summary.json` as a learned proposal prior. This is not an LLM fine-tune; it is an interpretable empirical policy trained from the current experiment's `training_dataset.jsonl`. The policy rewards features associated with accepted low-chi-square theories and penalizes features associated with repeated structural failures.

Accepted theories are not all equally good training signals. The proposal policy should treat Solver-accepted attempts by chi-square quality:

- `chi2 <= 1650`: excellent; strongly reinforce shared structural features.
- `1650 < chi2 <= 1700`: competitive; moderately reinforce shared structural features.
- `1700 < chi2 <= 2000`: acceptable; record as viable and use positive reinforcement, but less than competitive models.
- `chi2 > 2000`: poor accepted; apply weak or negative reinforcement depending on how far above 2000 it is.

Chi-square remains the primary Solver and report ranking metric. However, the agent's learning reward should distinguish a genuinely active modified-gravity correction from an EH-dominated fit. For accepted attempts, compute `fit_reward` from `chi2`, then compute `discovery_reward` from `fit_reward` plus `effective_correction_status`. The status is based on each non-EH, non-fixed-matter correction that contains curvature, such as `R²`, `Riemann²`, `φR`, `φ²R`, `□φ R`, or derivative-curvature terms. Pure scalar/self terms such as standalone `φ²` or standalone `□φ` are not counted as modified-gravity corrections for this diagnostic.

Do not penalize a clean EH+scalar baseline merely because it has no modified-gravity correction. `eh_only` means the validated theory is an EH/scalar baseline and should keep its normal chi-square-derived `fit_reward`. Penalize only models that add extra modified-gravity correction terms whose effective contribution is tiny after coefficient values and `Lambda` powers are applied. In other words, `EH + scalar` is a valid baseline; `EH + scalar + effectively-zero correction terms` is a poor discovery signal.

For each counted correction, estimate its effective size relative to the Einstein-Hilbert reference term:

```text
relative_effect_i ~= |c_i / c_EH| * lambda_H^(lambda_power_i) * field_factor_i
```

where `lambda_H = Lambda/H0` comes from the accepted Solver sample, `lambda_power_i` comes from the validated term metadata, and `c_EH` is the coefficient of the `M_p² R` term. EH `R`, fixed scalar kinetic/potential terms, and pure scalar/self terms are not counted as modified-gravity corrections.

Use these status thresholds:

```text
active:    max_relative_effect_to_EH >= 1e-2
moderate:  1e-4 <= max_relative_effect_to_EH < 1e-2
weak:      1e-6 <= max_relative_effect_to_EH < 1e-4
tiny / eh_dominated: max_relative_effect_to_EH < 1e-6, or no active non-EH correction
unclear: missing EH coefficient, lambda_H, coefficient values, or term metadata
```

The learned policy should use `discovery_reward`, not raw `fit_reward`, so a low-chi-square model whose extra operators are suppressed by tiny coefficients or large negative powers of `Lambda` is penalized as a weak discovery. Reports must still sort by `chi2`, but should display `effective_correction_status`, `max_relative_effect_to_EH`, and the dominant correction term next to each accepted family representative.

The structure prior should learn at a finer level than exact theory fingerprints. It must not hard-code a special penalty for `phi2` or any other legal scalar family. Instead, it should compare the same current-loop scalar-family metrics for `none`, `phi1_only`, `phi2_only`, and `both`. Families or operator buckets with repeated poor evidence may receive a soft downweight, but they must not be banned from exploration. Successful low-chi-square patterns such as a scalar family with an `R` anchor should raise the probability of that pattern without changing Solver's final chi-square ranking rule.

The cold-start runner should behave as an explicit agent loop:

```text
generate token-level legal theory
-> run harness through EOM, Builder, Solver
-> read feedback_summary.json and all_samples_summary.csv
-> write agent_reflections.jsonl
-> update structure_prior.json and parameter_prior.json
-> generate the next theory and parameters using those priors
```

The parameter prior must come from current-loop Solver feedback. Accepted rows in `all_samples_summary.csv` are used to estimate quantile ranges for common parameters such as `H0_km_s_Mpc`, `Omega_m0`, `lambda_H_Lambda_over_H0`, scalar initial values, scalar mass/decay parameters, and coefficient magnitudes/signs.

At proposal time, parameter sampling should be done as a whole physical configuration, not as unrelated independent draws. The cold-start sampler must choose `lambda_H`, scalar initial values, and free correction coefficients together. For non-EH curvature correction terms, choose coefficient magnitudes from a planned effective size relative to the EH term:

```text
|c_i| ~= target_relative_effect * |c_EH| / (lambda_H^(lambda_power_i) * field_factor_i)
```

Use a mixed sampling schedule with baseline, weak, moderate, and active-probe correction modes. Baseline samples should draw raw non-EH coefficients directly from the broad coefficient prior, currently `|c_I| = 1e-10` to `1e20` with both signs, rather than using the effective-size inversion. Weak, moderate, and active-probe samples should choose non-EH curvature correction coefficients from a planned effective size relative to the EH term. The default initial mode weights are `baseline=0.10`, `weak=0.30`, `moderate=0.30`, and `active_probe=0.30`; active-probe targets should cover `1e-2 <= relative_effect <= 1e2`. The parameter sample list should use a 50/50 split between agent-exact samples and learned-prior random samples. Both halves may consult `joint_parameter_prior.json` for up to the configured `joint_prior_usage_fraction` of samples, currently `0.80`: exact samples reuse high-reward parameter vectors from the nearest available current-loop family level, while random samples jitter around those vectors in log space. The remaining samples keep using learned/default priors as an exploration floor. If no positive current-loop evidence exists for exact/coarse/scalar/global matches, sampling falls back to the learned/default priors. The agent may softly adjust correction-mode weights from current-loop sample feedback while preserving exploration floors. This is only a proposal-time sampling policy; Solver ranking and human-facing reports still sort by real `chi2`. EH `R` remains fixed by the configured EH coefficient and should not be penalized or rescaled as a modified-gravity correction.

`joint_parameter_prior.json` is sample-level memory, not a table of hard-coded best parameters. Each sample row gets a reward from real Solver feedback: accepted low-chi-square rows are positive, poor accepted rows may be weak or negative, and rejected rows provide negative failure evidence. The sampler searches this memory in order: exact family, coarse operator/scalar bucket, scalar family, then global fallback. It seeds common cosmological/scalar parameters from the selected vector and then recomputes free coefficients for the current operator set, so coefficient values stay tied to the current theory's `lambda_power`, field factors, and correction mode.

The proposal-time coefficient cap in `config_p.py` is an exploration bound, not a physical acceptance rule. Large coefficients are allowed up to that cap so high-dimension `Lambda`-suppressed operators can be tested; unstable samples should be rejected by the real Solver feedback rather than hidden by an overly small proposal cap.

Parameter-prior updates are gated. `H0_km_s_Mpc` must keep the default range from `config_p.py`. All other parameters initially use the default range near `config_p.py`; after at least 10 current-loop attempts and at least 100 accepted Solver sample rows, the agent may use accepted-sample quantiles to update `parameter_prior.json`.

Default cold-start parameter ranges live in:

```text
ai_theory_lab/config_p.py
```

The runner should import these defaults instead of hard-coding ranges locally. Learned `parameter_prior.json` may narrow or override these defaults after enough accepted current-loop samples exist.

The default scalar prior is intentionally broad. Use log sampling for positive scale parameters: `varphi1_0_phi1_over_Mp` in `1e-3..1e1`, `mu1_m1_over_H0` in `1e-2..1e2`, `fbar1_f1_over_Mp` in `1e-2..1e2`, `mu2_m2_over_Lambda` in `1e-5..1e5`, and `fbar2_f2_over_Lambda` in `1e-5..1e5`. Use signed-log sampling for sign-sensitive phi2 quantities: `varphi2_0_phi2_over_Lambda` and `q2_0_dvarphi2_dln_a` should draw both signs with `|value|` in `1e-5..1e5`. These wider ranges are exploration priors; invalid samples are rejected by the Solver.

For genuine cold-start discovery, do not choose theory structures by looking up full entries from `lagrangians.pkl`. That file may be used for replay, regression, or compatibility tests. A discovery agent should generate fresh legal structures from the token-level Grammar Masker candidate pool, then validate the isolated generated theory through EOM, Builder, and Solver.

The cold-start agent should construct each Lagrangian directly from legal `CandidateScalar` operators in the cached token context. It should choose scalar configuration, potential type, and candidate-operator combination, compile the selected combination into a full dimension-balanced `agent_lagrangians.pkl`, and only then run validation. It must not use Grammar Masker's random `generate_lagrangians(... n_samples=...)` batch generator as the proposal source for discovery loops.

For each theory, the default parameter policy is:

- apply a 120s wall-time limit to EOM, Builder, and Solver setup/lambdify;
- do not apply the 120s wall to token-level Grammar Masker candidate discovery while building the independent-scalar space;
- build the independent-scalar candidate space once per cold-start run and reuse it for all proposal loops in that run;
- load the token-level independent-scalar candidate space from `ai_theory_lab/cache/` when available, or build it once and cache it for future runs;
- apply the same 120s wall-time limit to each per-loop token-level proposal generation attempt after the candidate space has been built; if a proposal attempt times out, record it as a `GrammarGeneration`/`pre_sampling_timeout` failure and move to the next loop;
- propose 1000 explicit parameter samples;
- do not stop the agent run early because a theory reaches a low chi-square; low chi-square is a quality label and learning signal, not a loop-termination condition;
- if no sample from the first 1000 reaches `chi2 < 2000`, test 3000 explicit samples for the same theory only when the first pass is not clearly structural or numerically unstable;
- do not expand to 3000 samples when the first 1000 produce no accepted `chi2` and the feedback shows a structural or dominant numerical failure such as `q_initial_root_failure`, `q_not_determined`, `no_scalar_constraint`, high-count `constraint_drift`, high-count `integration_failure`, pre-sampling timeout, or symbolic timeout;
- also skip the 3000-sample expansion for `scalar=none` empty-ranking failures and for no-accepted first passes tagged with `constraint_drift` or `integration_failure`, because these have been low-yield in current-loop tests;
- read Solver's `all_samples_summary.csv` so every accepted and rejected parameter sample contributes feedback.

Do not apply the 120s pre-sampling wall to the numerical sampling loop itself; sampling is governed by the explicit 1000/3000 sample budget and structural skip rules.

The token-context cache stores Grammar Masker candidate discovery results only. It is allowed in cold-start discovery because it does not contain historical Solver rankings, accepted chi-square values, best-fit parameters, or prior run proposal choices. To force a rebuild, use:

```bash
python -m ai_theory_lab.graph_agent --no-token-context-cache ...
python -m ai_theory_lab.cold_start_runner --no-token-context-cache ...
```

There are two validation interfaces:

- Agent proposal validation: use `--proposal proposal.json`. This is the preferred interface. The proposal contains both the theory JSON and the agent-selected parameter samples. The harness compiles it into isolated files such as `agent_lagrangians.pkl`, `agent_parameter_samples.json`, `agent_eom_results/`, `agent_built_models_cache.pkl`, and `agent_solver_result/` under `ai_theory_lab/runs/<run_id>/`.
- Agent/sample replay validation: use `--agent-sample` only for smoke tests, replaying existing `lagrangians.pkl` entries, or debugging the harness.
- Batch validation: use `--run-validation` only when intentionally validating the current full `lagrangians.pkl` batch. This can process 1120 Lagrangians and may take much longer.

The proposal schema is documented in:

```text
ai_theory_lab/proposal_schema.md
```

The preferred agent interface includes both a theory and explicit numerical parameter samples:

```bash
python -m ai_theory_lab.harness --proposal ai_theory_lab/proposal_example.json --pretty
```

When this file is provided, Solver evaluates exactly those samples. It does not randomly generate missing free parameters. Missing required keys cause an explicit rejection such as `agent parameter sample missing: H0_km_s_Mpc`.

For harness smoke checks, sample one existing Lagrangian instead of running the whole batch:

```bash
python -m ai_theory_lab.harness --agent-sample --agent-max-terms 1 --pretty
```

For a reproducible single-theory check from the existing generated pool, select the source group and 1-based local index explicitly:

```bash
python -m ai_theory_lab.harness --agent-sample --agent-source-n-terms 3 --agent-source-local-number 20 --pretty
```

The agent interface writes and reads isolated agent files:

- `ai_theory_lab/runs/<run_id>/agent_lagrangians.pkl`
- `ai_theory_lab/runs/<run_id>/agent_parameter_samples.json` when provided by the agent
- `ai_theory_lab/runs/<run_id>/agent_eom_results/eom_summary.txt`
- `ai_theory_lab/runs/<run_id>/agent_built_models_cache.pkl`
- `ai_theory_lab/runs/<run_id>/agent_solver_result/agent_solve/model_ranking.csv`

The agent harness defaults to numeric validation only by setting `SOLVER_MAKE_PLOTS=0` and `TOP_N=0` for Solver. This avoids plot/report extras during the validation gate. Ordinary manual Solver runs keep their default plotting behavior.

Agent parameter sample JSON is a list of objects. Each object is one proposed numerical sample. Use actual values, not prose:

```json
[
  {
    "H0_km_s_Mpc": 70.0,
    "Omega_m0": 0.3,
    "lambda_H_Lambda_over_H0": 1000.0,
    "varphi1_0_phi1_over_Mp": 0.0,
    "mu1_m1_over_H0": 1.0,
    "fbar1_f1_over_Mp": 1.0
  }
]
```

Required keys depend on the theory:

- Always provide `H0_km_s_Mpc`, `Omega_m0`, and `lambda_H_Lambda_over_H0`.
- For phi1 theories, provide `varphi1_0_phi1_over_Mp`, `mu1_m1_over_H0`, and `fbar1_f1_over_Mp`.
- For phi2 theories, provide `varphi2_0_phi2_over_Lambda`, `mu2_m2_over_Lambda`, and `fbar2_f2_over_Lambda`.
- For two-scalar theories, also provide `q2_0_dvarphi2_dln_a`; Solver still solves `q1_0` from the constraint.
- For free symbolic coefficients, provide a key matching the coefficient name, such as `\\beta` or `\\gamma`. The Einstein-Hilbert coefficient may be fixed by Solver and then is not required.

In two-scalar `both` models, missing `q2_0_dvarphi2_dln_a` is a proposal-interface error, not a physical failure. The agent must generate this value explicitly for every parameter sample.

Solver writes `agent_parameter_sample_index` into result CSVs so the agent can learn which exact parameter sample produced a low chi-square or a rejection.

For quick inspection of existing Solver output without claiming a new validation run:

```bash
python -m ai_theory_lab.harness --read-latest-only --pretty
python -m ai_theory_lab.harness --output-dir solver_result/<run> --pretty
```

The minimal LangGraph wrapper is:

```bash
python -m ai_theory_lab.graph --read-latest-only --pretty
python -m ai_theory_lab.graph --output-dir solver_result/<run> --pretty
python -m ai_theory_lab.graph --agent-sample --pretty
python -m ai_theory_lab.graph --run-validation --pretty
```

The current LangGraph wrapper is minimal and still uses sample/replay validation. The preferred proposal interface is the harness command `python -m ai_theory_lab.harness --proposal <proposal.json>`. Use `--run-validation` only for the full current batch. Read-only graph modes are for debugging existing Solver outputs.

The LangGraph cold-start agent entrypoint is:

```bash
python -m ai_theory_lab.graph_agent --loops 20 --run-name graph_agent_run --pretty
```

This is the preferred LangGraph orchestration path. It keeps `cold_start_runner.py` as a baseline implementation but makes LangGraph own the stateful loop:

```text
initialize_run
-> start_loop
-> propose_theory
-> validate_initial
-> reflect_after_initial
-> decide_after_initial
-> validate_expanded when needed
-> reflect_after_expanded
-> decide_after_expanded
-> write_loop_trace
-> advance_loop
-> finalize_run
-> generate_result_report
```

For mini-batch proposal runs, the default proposal sectors are:

```text
open_search: 0.50
non_eh:      0.50
```

Do not reserve a separate `EH + phi2_only` sector by default. `phi2_only` EH-anchored theories may still appear through `open_search` and scalar-family exploration, but the dedicated sector budget should be used for explicit non-EH modified-gravity search instead.

The `open_search` mini-batch sector uses a light fixed scalar-family baseline. For open-search proposals, select scalar family with `phi1_only=0.08`, `phi2_only=0.08`, `both=0.08`, and `none=0.08` fixed probability, and use the remaining `0.68` probability for reward-weighted choice among the same four families from current-loop `open_search` policy evidence. If no scalar family has positive reward evidence, the reward-weighted part falls back to a uniform draw.

The `non_eh` mini-batch sector uses a stronger fixed scalar-family baseline. For non-EH proposals, select scalar family with `phi1_only=0.15`, `phi2_only=0.15`, `both=0.15`, and `none=0.15` fixed probability, and use the remaining `0.40` probability for reward-weighted choice among the same four families from current-loop `non_eh` policy evidence. If no scalar family has positive reward evidence, the reward-weighted part falls back to a uniform draw.

Mini-batch validation waves should be split by proposal complexity before running EOM, Builder, and Solver. The batch runner should classify generated Lagrangians into `simple`, `medium`, and `complex` buckets from operator count, term count, scalar family, derivative operators, high-curvature structures, mass dimension, and `Lambda` powers. Each bucket must be written to its own isolated agent run directory, for example:

```text
ai_theory_lab/runs/<run_name>_wave_0001_simple/
ai_theory_lab/runs/<run_name>_wave_0001_medium/
ai_theory_lab/runs/<run_name>_wave_0001_complex/
```

This keeps simple models from waiting behind symbolic-heavy complex models on a cluster wave. Memory records should still be written per Lagrangian, and `wave_trace.jsonl` should record `validation_wave`, `complexity_bucket`, and `complexity_score` for reproducibility. Use `--no-complexity-split` only when deliberately reproducing the old single-batch behavior.

Mini-batch proposal generation must also have a per-attempt wall-time guard so one symbolic-heavy candidate cannot block the whole wave before validation begins. The default guard is `AGENT_PROPOSAL_TIMEOUT_SECONDS=300`. If a proposal attempt times out or cannot compile a candidate, skip that attempt and keep filling the batch, while preserving hard failure behavior when `--llm-fallback fail` is explicitly requested.

`graph_agent.py` must still use the same deterministic harness and isolated agent files. LangGraph controls branching, loop state, reflection, skip/expand decisions, loop tracing, and final summary writing; EOM, Builder, Solver, chi-square scoring, and memory updates remain deterministic project code. Each loop writes a structured record to `loop_trace.jsonl` with validation results, reflection, decision, and current-loop summary facts.

After every multi-loop agent run, generate a human-readable result report before reporting the run to the user:

```bash
python -m ai_theory_lab.report --run-name <run_name> --top-n 20
```

The report directory must be:

```text
ai_theory_lab/reports/<run_name>/
```

Every completed agent task must leave a fixed report artifact set. Do not only answer in chat, and do not provide only a plot or only a summary. The report directory must contain:

- `summary.md`: front-page run summary, top accepted theories, chi-square ranking, and visible parameter choices.
- `accepted_lagrangians_and_parameters.md`: complete accepted-theory Lagrangians plus best-fit parameter choices.
- `accepted_lagrangians_full.md`: full dimension-balanced Lagrangian detail for inspection.
- `accepted_lagrangians_and_parameters.csv`: machine-readable accepted Lagrangians and parameters.
- `accepted_summary.json`: structured accepted-attempt records.
- `accepted_family_representatives.json`: structured best-per-family records used for human-facing reports.
- `accepted_chi2_bar.png`: accepted-model chi-square plot.
- `top_h_overlay.png`: h(z) overlay for top accepted Solver solutions.
- `top3_h_panels.png`: separate h(z) panels for the best accepted Solver solutions.

The agent-facing memory and `accepted_summary.json` should keep all accepted attempts. The human-facing files (`summary.md`, `accepted_lagrangians_and_parameters.md`, `accepted_lagrangians_full.md`, `accepted_lagrangians_and_parameters.csv`, and plots) should show one best chi-square representative per theory family so repeated similar theories do not dominate the report. Use `coarse_family_key` when available, falling back to exact `family_key`.

The `summary.md` front page must show the best accepted family representatives together with the parameter choices that produced those scores: `agent_parameter_sample_index`, `H0_km_s_Mpc`, `Omega_m0`, `lambda_H_Lambda_over_H0`, relevant scalar initial values, scalar masses/decay constants, solved or sampled scalar velocities, and a compact list of free coefficient values. If no accepted models exist, still write `summary.md`, `accepted_lagrangians_and_parameters.md`, `accepted_lagrangians_full.md`, `accepted_lagrangians_and_parameters.csv`, `accepted_summary.json`, and `accepted_family_representatives.json` with failure counts and an explicit note that no accepted h(z) plot could be made.

Accepted reports should also include effective-correction diagnostics for each shown family representative. The human-facing order stays `chi2` from low to high; the diagnostics are interpretive labels used to tell whether a low-chi-square model is an actual modified-gravity correction or mostly EH/scalar baseline. Include `effective_correction_status`, `max_relative_effect_to_EH`, `dominant_correction_term`, and term-level relative effects in the machine-readable accepted CSV/JSON and markdown details.

Recommended LangGraph loop:

```text
load_memory
-> propose_theory
-> validate_theory
-> run_grammar_or_compile_spec
-> run_eom
-> run_builder
-> run_solver
-> score_result
-> reflect
-> update_memory
-> continue_or_stop
```

LangChain is optional. Use it if a unified LLM interface, prompt templates, structured output parsers, or retrievers are useful. LangGraph should own the stateful workflow. LangSmith should record proposals, settings, outputs, failures, and scores.

## Result Interpretation

Important Solver outputs:

- `model_ranking.csv`: best sample per model, sorted by chi-square.
- `accepted_samples_summary.csv`: all accepted samples, sorted by chi-square.
- `best_solution.csv`: best accepted sample by chi-square.
- `reject_reasons_by_model.csv`: rejection causes and counts.
- `scan_report.txt`: human-readable run summary.

Accepted-theory summaries should follow the Solver top-model report style. For each accepted model, include the raw `general` Lagrangian from the validated pkl object, the same Lagrangian with best-fit numerical coefficients substituted, per-term metadata (`sector`, `mass_dim`, `lambda_power`, fixed/non-fixed, and whether it is inside the `M_p²(...)` prefactor), fit metrics, scalar initial conditions, sampled values, free coupling values, the proposal JSON path, and Solver output files. A report that lists only candidate operators or `coefficient * operator` without `M_p²` and `Λ` powers is incomplete because it does not identify the tested dimension-balanced theory.

For agent runs, accepted-theory summaries must be written to `ai_theory_lab/reports/<run_name>/`, not only described in chat. The report should make the best models inspectable without opening each isolated Solver output directory manually.

Use reject reasons carefully:

- EOM failures imply structural theory problems.
- Builder failures imply symbolic/numerical-preparation problems.
- Solver failures may be caused by bad sampled parameters, not necessarily by an impossible theory.

## Failure Feedback Guide

When the harness returns `validated=false`, the agent must convert the failed stage and reject reasons into an explicit next action. Do not only summarize the error.

Common failure meanings:

- `symbolic build timeout > 60s`: the theory is too hard for the current Builder settings. In the next proposal, reduce term count, reduce high-curvature derivative operators, avoid mixing many non-minimal scalar-curvature terms, or propose a deliberate Builder-timeout experiment instead of treating the theory as validated.
- `q1_x not determined by coupled scalar EOM` or `q2_x not determined by coupled scalar EOM`: Builder/Solver could not form a usable first-order RHS for the scalar sector. In the next proposal, simplify scalar kinetic/mixing terms, reduce cross-field derivative couplings, prefer scalar sectors that previously produced active IVP models, or try one scalar at a time.
- `no acceptable real q1_0 root from E_N(x=0)=0` or `no acceptable real q2_0 root from E_N(x=0)=0`: the sampled initial constraint has no acceptable real scalar-velocity root. Treat this as `q_initial_root_failure`, not as a generic missing-ranking event. If it dominates the first 1000 samples and no sample is accepted, skip the 3000-sample expansion and change the theory structure or scalar/parameter prior.
- `no-scalar constraint not satisfied at x=0`: the no-scalar model could not satisfy the initial constraint under sampled parameters. In the next proposal, add an Einstein-Hilbert `R` anchor if missing, avoid pure high-curvature combinations without a stabilizing low-order term, or adjust priors only as a separate parameter-search experiment.
- `constraint drift too large`: the trajectory numerically violates the constraint. In the next proposal, reduce nonlinear scalar self-interactions, reduce derivative couplings, prefer equations with simpler RHS, or mark the current structure as unstable under current solver cuts.
- `H(z) absurdly large`: the sampled trajectory is physically/numerically unstable. In the next proposal, favor terms and priors that keep expansion histories close to plausible LCDM-like ranges before exploring more exotic corrections.
- `EFT cutoff violated`: the trajectory leaves the allowed EFT regime. In the next proposal, reduce operators that drive large `h/lambda_H`, revisit `LOG10_LAMBDA_H_*` only as an explicit prior experiment, and do not mark the theory as good simply because it fits outside the cutoff.
- Empty `model_ranking.csv`: no accepted sample was found. Check `reject_reasons_by_model.csv`; if there are no detailed reasons, treat it as an inconclusive parameter-search failure and either increase `N_SAMPLES_PER_MODEL` for the same theory or move to a simpler nearby structure.
- Structural or dominant numerical failure in the first 1000 samples: if there is no accepted chi-square and most rejected samples share `q_initial_root_failure`, `q_not_determined`, `no_scalar_constraint`, high-count `constraint_drift`, high-count `integration_failure`, pre-sampling timeout, or symbolic timeout, skip the 3000-sample expansion and propose a different legal theory structure or parameter prior.

After each validation, the agent should record:

- theory fingerprint and source/proposal ID
- failed stage or `validated=true`
- best `chi2` if available
- top reject reasons and counts
- one concrete change for the next proposal

Repeated failures of the same type should shift the search distribution. For example, several build timeouts should lower the probability of high-term, high-derivative, two-scalar proposals; repeated `q*_x not determined` failures should lower the probability of coupled scalar derivative structures.

## Before Editing

Before modifying code:

1. Read this file.
2. Read the relevant stage-specific `AGENT.md`.
3. Inspect the current code path and generated outputs.
4. Keep edits scoped to the requested behavior.
5. Run a small verification when possible.

For scoring or ranking changes, inspect both `solver_v5_2/core.py` and `solver_v5_2/runner.py`.

For theory-space changes, inspect both `gr_grammar_masker_v3_2/grammar.py` and `gr_grammar_masker_v3_2/tensor.py`.
