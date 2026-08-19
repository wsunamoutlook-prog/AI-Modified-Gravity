# Agent Proposal Schema

Agent proposals should be written as JSON. A proposal contains both the theory structure and explicit numerical parameter samples.

For the full legal Lagrangian contract, including `sqrt(-g)`, `M_p²` placement,
EFT `Λ` powers, sector rules, scalar fixed matter terms, and dimension-4
balancing, see:

```text
ai_theory_lab/lagrangian_legality.md
```

For cold-start theory discovery, proposals must be generated from Grammar Masker rules and current-loop feedback, not from historical Solver winners.

For genuine cold-start discovery, the theory structure should be generated from the token-level Grammar Masker candidate pool. Matching against an existing `lagrangians.pkl` entry is allowed for replay, smoke tests, or compatibility checks, but it should not be the source of new cold-start theory choices.

Mini-batch cold-start proposal runs now default to unrestricted open search:

```text
open_search: 1.00
dedicated non_eh: 0.00
```

Use `--group-mode open_only` for this policy. `open_search` has no theory-track constraint, so EH-anchored, non-EH, and non-gravity structures can still arise organically. `--group-mode sector_split` remains available only for explicit legacy or ablation experiments and reserves half of the initial-theory budget for forced non-EH proposals. There is no separate default `EH + phi2_only` sector.

The `open_search` sector uses a light scalar-family exploration floor before reward learning:

```text
phi1_only: 8% fixed baseline
phi2_only: 8% fixed baseline
both:      8% fixed baseline
none:      8% fixed baseline
reward-weighted choice among the four families: 68%
```

The reward-weighted portion uses only current-loop AIC-based structure-reward evidence from the `open_search` sector. If no scalar family has positive reward evidence yet, it is uniform over the four families.

When `sector_split` is requested explicitly, its dedicated `non_eh` sector retains the stronger scalar-family exploration rule:

```text
phi1_only: 15% fixed baseline
phi2_only: 15% fixed baseline
both:      15% fixed baseline
none:      15% fixed baseline
reward-weighted choice among the four families: 40%
```

The reward-weighted portion uses only current-loop AIC-based structure-reward evidence from the `non_eh` sector. If no scalar family has positive reward evidence yet, it is uniform over the four families. The fixed baselines keep every scalar family alive while preventing the non-EH search from collapsing into one family such as `none`.

The optional `--diversity-strength` setting is a proposal-time anti-collapse control, not a reward change. The default is `0.0`, so ordinary discovery runs disable diversity pressure and prioritize convergence. As it approaches `1.0`, exact and coarse families that have already appeared many times in the current loop are down-ranked before proposal selection, with extra pressure away from already-successful basins. This preserves scalar-family exploration floors and does not change Solver `chi2` ranking, accepted-sample parameter memory, or `discovery_reward`.

Production cluster runs use `--scheduler async_slots`. Each slot validates one theory at a time in an isolated run directory; as soon as that theory, including any triggered expanded/refined pass, finishes, its records are written to shared current-loop memory and the freed slot generates a replacement from the updated memory. A slow theory therefore occupies only its own slot. With eight CPUs, use eight slots and one Solver worker per slot. Complexity and predicted-runtime fields remain diagnostics and runtime-prior inputs; they do not partition the production queue. The older `wave` and `async_lanes` schedulers remain available for reproduction and scheduler ablations, including their `simple`, `medium`, `complex`, and `very_complex` runtime buckets. Scheduling never changes Solver `chi2` ranking or the AIC-based structure reward.

If an `async_slots` process exits before reaching its initial-theory target,
restart it with the identical run configuration and `--resume`. The resume
path reads completed initial records from current-loop memory, uses a new task
number above all existing artifacts, and replaces crash-boundary tasks that
were submitted but never recorded. It appends to the same memory and proposal
logs; it does not overwrite accepted results or restart learning. A
`scheduler_resume` event separates active wall-time segments for speed
reporting. Resume is intentionally unavailable for the legacy schedulers.

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

The status thresholds are `active >= 1e-2`, `moderate >= 1e-4`, `weak >= 1e-6`, and `tiny`/`eh_dominated < 1e-6`. `eh_only` means the theory is a clean EH/scalar baseline with no extra modified-gravity correction terms, and should keep its normal AIC-derived structure reward. This helps the agent avoid treating an `EH + scalar + effectively-zero correction terms` fit as a strong modified-gravity discovery signal.

For report figures, use publication-readable plotting defaults: LaTeX-style `$\chi^2$` labels and titles, compact representative labels such as `#L313`, high-resolution output at 300 dpi, colorblind-safe color legends for sector/track/group comparisons, hatch or line-style differences for grayscale readability, and horizontal mathtext chi-square values above bars when space allows. Dense bar charts should cap the plotted representatives at a readable count, currently 15, while markdown, CSV, and JSON retain the complete requested top list. For sector-comparison figures, readability takes priority over showing every poor accepted tail. `top_by_group_chi2_bar.png`, `top_by_track_chi2_bar.png`, `top_by_group_h_overlay.png`, `top_by_track_h_overlay.png`, and dense `top_h_overlay_topn.png` should include only accepted family representatives with `chi2 < 2000`. Hubble-overlay comparison legends should identify individual curves with compact representative labels and their concrete chi-square values. High-chi-square representatives remain available in markdown, CSV, and JSON report files.

Current cold-start compiler behavior:

- `graph_agent.py` and `cold_start_runner.py` build or load the token-level Grammar Masker candidate context once.
- The agent constructs a theory by choosing scalar configuration, potential type, and a combination of legal `CandidateScalar` operators from that candidate pool.
- For each proposal, the cold-start generator first samples the number of non-fixed Grammar Masker operators, defaulting to 1 through 8. Each operator count receives a fixed 5% exploration probability. The remaining probability mass is learned from current-loop feedback by combining operator-count accepted rate, AIC-based structure quality, and the policy `discovery_reward`, which already downweights tiny/`eh_dominated` corrections while preserving clean `eh_only` baselines. When the fixed exploration draw selects count 1, the generator forces an `R`-only baseline/control operator set. Fixed scalar kinetic/potential terms are added afterward according to `scalar_config`.
- The selected candidate combination is compiled directly into a full dimension-balanced `agent_lagrangians.pkl` entry with the same `M_p²`, `Λ`, sector, fixed scalar-matter, and coefficient-token conventions used by Grammar Masker.
- The cold-start agent must not call Grammar Masker's random `generate_lagrangians(... n_samples=...)` batch generator as its proposal source.
- Replay and compatibility checks may still match proposal JSON against `lagrangians.pkl`, but that is not cold-start discovery.

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

## Open Design Questions

- It is not yet specified whether cold-start parameter samples should eventually use broad fixed priors, Latin-hypercube samples, small physics priors, or an LLM-chosen distribution.
- It is not yet specified how large the direct candidate-combination search beam should be once this runs on a cluster.
- It is not yet specified whether the external API agent should output a complete operator combination directly or rank a proposed beam generated from the current candidate pool.

## LLM Provider Settings

For LLM-driven proposal selection, batch and graph entrypoints accept:

```bash
--proposal-mode llm
--llm-provider openai|anthropic|openai_compatible
--llm-model <model_name_or_gateway_slug>
--llm-base-url <optional_base_url>
--llm-api-key-env <optional_env_var_name>
```

`openai` uses the native OpenAI Responses API. `anthropic` uses the native Claude Messages API. `openai_compatible` uses the Chat Completions API shape for gateways or local servers such as Gemini, DashScope/Qwen, Requesty, OpenRouter, DeepSeek-compatible endpoints, and Ollama. Examples:

```bash
# Native OpenAI
--llm-provider openai \
--llm-model gpt-5.6-sol \
--llm-api-key-env OPENAI_API_KEY

# Native Anthropic Claude
--llm-provider anthropic \
--llm-model claude-sonnet-5 \
--llm-api-key-env ANTHROPIC_API_KEY

# Gemini OpenAI-compatible endpoint
--llm-provider openai_compatible \
--llm-base-url https://generativelanguage.googleapis.com/v1beta/openai/ \
--llm-model gemini-3.6-flash \
--llm-api-key-env GEMINI_API_KEY

# DashScope / Qwen OpenAI-compatible endpoint
--llm-provider openai_compatible \
--llm-base-url https://dashscope-us.aliyuncs.com/compatible-mode/v1 \
--llm-model qwen3.7-max \
--llm-api-key-env DASHSCOPE_API_KEY

# Moonshot / Kimi OpenAI-compatible endpoint
--llm-provider openai_compatible \
--llm-base-url https://api.moonshot.ai/v1 \
--llm-model "${KIMI_MODEL:-kimi-k3}" \
--llm-api-key-env MOONSHOT_API_KEY

# Requesty / OpenRouter / DeepSeek-style gateway
--llm-provider openai_compatible \
--llm-base-url https://<gateway-host>/v1 \
--llm-model <gateway-model-slug> \
--llm-api-key-env REQUESTY_API_KEY

# Local Ollama
--llm-provider openai_compatible \
--llm-base-url http://127.0.0.1:11434/v1 \
--llm-model qwen3:32b
```

LLM proposal records must include the selected provider/model/base URL metadata and latency/usage when available so later model-comparison tables can distinguish native APIs from gateways. Production comparisons use `--llm-fallback skip`: exhausted API failures are recorded and omitted while the scheduler refills the target, because silently replacing a failed API selection with the deterministic policy would contaminate model attribution. The response requests `candidate_index` plus a concise rationale, but the explicit index is authoritative and may be recovered if only the trailing rationale is truncated. Extended reasoning is disabled or minimized for this short selection call.

The production `frontier6` preset also includes `deepseek-v4-pro` through the configured DashScope-compatible endpoint. The matched `claude5` preset provides the Opus 5 and Fable 5 extension under the same 1000/3000/5000 numerical schedule. `cheap5` and `expensive3` remain available only for reproducing earlier experiments.

## Optional Tracing

LangSmith tracing is optional and disabled by default. To mirror scheduler events to a LangSmith project, set:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="<key>"
export LANGSMITH_PROJECT="modified-gravity-api-benchmark"
```

Tracing records monitoring metadata only. It does not change proposal scoring, parameter sampling, validation, Solver ranking, or local report generation. Local files such as `scheduler_tasks.jsonl` and `attempt_history.jsonl` remain authoritative.

## Model Comparison Tables

For cross-API/model comparisons, generate tables from local artifacts:

```bash
python -m ai_theory_lab.compare_benchmarks \
  --runs 'cmp600_*_v1' \
  --output-dir ai_theory_lab/reports/cmp600_model_benchmark_v1
```

The output files are `comparison_metrics.csv`, `comparison_by_axis.csv`, and `comparison_summary.json`. The comparison uses four fixed axes: global optimum, new-physics search, speed/efficiency, and robustness/stability.

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

For `phi2_only` agent proposals, `q2_0_dvarphi2_dln_a` may also be provided. Solver still solves `q2_0` from `E_N(x=0)=0`; the proposed value is used only as a root-search hint/preference so the initial constraint remains a hard gate.

For free coefficients, provide keys matching the coefficient names:

```json
{
  "\\beta": 1.0e-5,
  "\\gamma": -3.0e-8
}
```

Solver solves constraint-determined initial velocities such as `q1_0` in phi1 models and `q2_0` in phi2-only models. These are written to result CSVs. In `phi2_only`, a provided `q2_0_dvarphi2_dln_a` is a Solver root-search hint, not a direct override. In two-scalar `both` models, the agent must propose `q2_0_dvarphi2_dln_a` and Solver solves `q1_0`.

## Feedback Contract

After validation, the agent should learn from:

- `validated`
- `chi2`
- `aic`, `bic`, `k_params`, and `k_parameter_names`
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

The memory layer records facts only. It summarizes failures, successful Solver entry, chi-square/AIC/BIC values, effective parameter counts, parameter sample counts, validation-stage lineage, and theory-family fingerprints. It does not decide that any class of theory should be preferred or avoided.

Before generating the next proposal, the agent should read `reflection_prompt.md` and write a reflection using current-loop facts only. The next `proposal.json` should be based on that reflection, not on historical `solver_result/` outputs or copied old best-fit parameters.

The agent should also read Solver's `all_samples_summary.csv` when present. This file gives one row per parameter sample, including rejected samples, so the agent can learn parameter regions from both finite chi-square values and failure reasons.

Cold-start runs should use a 120s wall-time limit for EOM, Builder, and Solver setup/lambdify. Do not apply this wall to token-level Grammar Masker candidate discovery while building the independent-scalar space. Build the independent-scalar space once per cold-start run and reuse it for all proposal loops in that run. The wall is not the sampling budget; the 1000/3000/5000 parameter sampling policy and structural skip rules control numerical sampling. A low chi-square such as `chi2 <= 1650` is a quality label and learning signal, not an early-stop condition for the agent run. The 3000-sample expansion should be skipped when the first 1000 samples have no accepted chi-square and are dominated by `q_initial_root_failure`, `q_not_determined`, `no_scalar_constraint`, high-count `constraint_drift`, or high-count `integration_failure`. It should also be skipped for `scalar=none` empty-ranking failures and for no-accepted first passes tagged with `constraint_drift` or `integration_failure`. In async-slot mini-batch runs, any 3000-sample expanded theory whose best chi-square remains below `1638` should receive one final 5000-sample refinement. This rule is uniform across actual theory tracks; an organically discovered `non_eh` theory receives no separate threshold or sampling budget. Expanded and refined attempts are extra validation records and do not count toward the global initial-theory target.

Repeated `q_not_determined` feedback should be treated as structural feedback, not a parameter-only failure. The current-loop policy may softly downweight exact operators and operator families that repeatedly cause this tag, especially scalar derivative and scalar-derivative-curvature couplings, while preserving some exploration.

The project separates parameter learning from structure learning. Parameter vectors within one fixed Lagrangian are rewarded by raw `chi2`; AIC would add the same constant to every vector and cannot change their ordering. Expansion/refinement decisions also remain the raw-chi-square thresholds described above. Different Lagrangian structures are compared by

```text
structure_score = AIC - 2*k_LCDM = chi2 + 2*(k_model-k_LCDM),  k_LCDM=3.
```

The constant subtraction preserves exact AIC ordering while retaining the existing quality-scale interpretation. `structure_score <= 1650` is excellent, `1650 < score <= 1700` is competitive, `1700 < score <= 2000` is acceptable positive feedback, and `score > 2000` should not strongly reinforce the structure. The final structure signal is `discovery_reward`: it starts from this AIC-based score, keeps clean `eh_only` EH/scalar baselines as valid baselines, downweights `weak` corrections, and penalizes `tiny` or `eh_dominated` extra correction terms. In the dedicated `non_eh` proposal sector only, accepted structures are quality-gated rather than rewarded just for surviving: `score <= 2000` stays positive, `2000 < score <= 3000` is weak positive, `3000 < score <= 6000` is marginal/near-zero negative, and `score > 6000` is negative. A non-EH trial with no accepted sample receives a stronger penalty than a very poor accepted non-EH structure.

Initial, expanded, and refined evaluations of the same proposal are kept as separate raw validation records, but only the best validated AIC stage is the representative for one structure-policy update. This prevents a promising theory from receiving two or three rewards merely because it was allocated more parameter samples. Solver and reports still rank by raw `chi2`, and all chi-square values remain in JSONL, CSV, JSON, and markdown outputs.

The nominal effective `k_model` is counted after EOM ghost-cancellation relations and Builder reduction. Cancelled, fixed, and constraint-solved quantities are excluded; parameters that remain free and actually enter the background likelihood are included. The profiled DES-SN offset and DESI BAO scale count as fitted nuisance parameters. `H0` counts only if it survives in the dimensionless dynamics, rather than when it is merely an absolute scale removed by those profiled likelihoods. This is the algebraic parameter count used by AIC/BIC, not a numerical Fisher-rank estimate.

Parameter sampling should treat each sample as one coherent physical setup. After choosing `lambda_H` and scalar initial values, non-EH curvature correction coefficients should be sampled from a planned effective size relative to the EH term:

```text
|c_i| ~= target_relative_effect * |c_EH| / (lambda_H^(lambda_power_i) * field_factor_i)
```

The default cold-start sampler mixes baseline, weak, moderate, and active-probe modes. Baseline samples do not use the effective-size inversion; they draw raw non-EH coefficients log-uniformly from the broad `config_p.py` coefficient prior, currently `|c_I| = 1e-10` to `1e20` with both signs. Weak, moderate, and active-probe samples choose non-EH curvature correction coefficients from a planned effective size relative to the EH term. The initial mode weights are:

```text
baseline:     0.10
weak:         0.30
moderate:     0.30
active_probe: 0.30
```

The initial target effective-size ranges are:

```text
weak:         1e-6 <= relative_effect < 1e-4
moderate:     1e-4 <= relative_effect < 1e-2
active_probe: 1e-2 <= relative_effect <= 1e2
```

The sampler uses a 50/50 split between agent-exact samples and learned-prior random samples. Both halves can check `joint_parameter_prior.json`, which stores parameter vectors rewarded strictly by raw chi-square from the current loop and groups them by exact theory family, coarse theory family, scalar family, and global fallback. The default `joint_prior_usage_fraction` is `0.80`: agent-exact samples in that fraction reuse the nearest matching high-reward vectors, and learned-prior random samples in that fraction jitter around those vectors in log space. The remaining sample budget keeps using the learned/default priors as an exploration floor. If no matching positive current-loop evidence exists, agent-exact samples fall back to current learned/default prior centers, low/high quantile anchors, and boundary probes, while learned-prior random samples draw stochastically from the current prior. The agent may softly adjust correction-mode weights from current-loop `all_samples_summary.csv` feedback while preserving exploration floors. Generated samples include numeric agent metadata such as `agent_sample_source_code`, `agent_correction_mode_code`, `agent_joint_prior_level_code`, and `agent_joint_prior_reward` so the memory layer can learn which source, correction mode, and family-level memory produced accepted or rejected samples; this metadata is not a physical coupling used by the EOM.

The coefficient cap from `config_p.py` is only a proposal-time exploration bound. Large coefficients are allowed up to that cap so `Lambda`-suppressed higher-dimension operators can actually be tested; numerical instability, constraint drift, or EFT rejection should come from the real Solver feedback.

The default scalar sampling prior is intentionally broad. Positive scale parameters use log sampling: `varphi1_0_phi1_over_Mp` in `1e-3..1e1`, `mu1_m1_over_H0` in `1e-2..1e2`, `fbar1_f1_over_Mp` in `1e-2..1e2`, `mu2_m2_over_Lambda` in `1e-5..1e5`, and `fbar2_f2_over_Lambda` in `1e-5..1e5`. Sign-sensitive phi2 quantities use signed-log sampling: `varphi2_0_phi2_over_Lambda` and `q2_0_dvarphi2_dln_a` draw both signs with `|value|` in `1e-5..1e5`. These are exploration ranges, not acceptance criteria.

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
