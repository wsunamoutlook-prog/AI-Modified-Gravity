# Solver Stage

This stage numerically samples model parameters, integrates the cosmological system, evaluates DES-SN + DESI-DR2 BAO likelihoods, and ranks models.

For a theory-generating agent, this is the stage that turns a legal symbolic theory into an empirical candidate. The best theories are the ones that survive the full pipeline and achieve the lowest `chi2` written by the real Solver code, subject to numerical and physical validity cuts.

## Role In Pipeline

Input:

- `built_models_cache.pkl` from `builder_v5_2`
- For agent/single-theory validation: isolated `agent_built_models_cache.pkl` through `BUILD_CACHE_PATH`
- DES-SN data
- DESI DR2 BAO data
- Run settings from `Solver v5.2.py`

Output:

- `solver_result/<run>/accepted_samples_summary.csv`
- `solver_result/<run>/all_samples_summary.csv`
- `solver_result/<run>/model_ranking.csv`
- `solver_result/<run>/best_solution.csv`
- `solver_result/<run>/best_fit_Hz.png`
- `solver_result/<run>/reject_reasons_by_model.csv`
- `solver_result/<run>/scan_report.txt`
- Partial CSV checkpoints during long scans
- For agent/single-theory validation: isolated `agent_solver_result/<run>/model_ranking.csv`

## Main Files

- `runner.py`: loads build cache, runs the scan, writes rankings and reports.
- `core.py`: parameter sampling, IVP solving, trajectory checks, chi2/AIC/BIC calculation, CSV output.
- `likelihood.py`: DES-SN and DESI BAO likelihood functions.
- `summary.py`: optional top-model summary generation.

## Scoring Contract

The primary ranking metric is now total chi-square:

```text
chi2_total = chi2_DES_SN + chi2_DESI_DR2_BAO
```

Ranking order:

```text
(chi2_total, AIC)
```

This means chi-square is the main criterion for parameter samples within one fixed Lagrangian and for human-facing Solver reports. The outer discovery agent uses AIC when it compares different Lagrangian structures, while preserving raw chi-square in every output. Expansion and refinement decisions remain chi-square based.

Important reported metrics:

- `chi2`
- `chi2_sn`
- `chi2_bao`
- `chi2_per_point`
- `AIC`
- `BIC`
- `k_params`
- `k_parameter_names`
- `max_abs_constraint`
- `reject_reason`

`k_params` is the nominal effective parameter count after EOM ghost-cancellation substitutions and Builder reduction. It includes free parameters that actually enter the current background likelihood. Cancelled or fixed coefficients and constraint-solved initial velocities are excluded. The analytically profiled DES-SN offset and DESI BAO scale are included. `H0` is included only if it survives in the dimensionless dynamics; when it is merely an absolute scale removed by the profiled likelihood it is not counted. The flat-LCDM reference has `k=3`: `Omega_m0`, `M_SN`, and `alpha_BAO`. This is an algebraic AIC/BIC count, not a numerical Fisher-rank calculation.

## Agent Responsibilities

The agent may:

- Read `model_ranking.csv` and `accepted_samples_summary.csv` to identify promising theories.
- Read `all_samples_summary.csv` to inspect every evaluated parameter sample, including rejected samples.
- Read `reject_reasons_by_model.csv` to learn why parameter samples fail.
- Propose explicit numerical parameter samples through `PARAMETER_SAMPLES_PATH`.
- Suggest parameter-prior changes, sample-budget changes, or optimizer upgrades when running random or hybrid scans.
- Compare parameter vectors within one theory by `chi2`; expose chi-square, AIC/BIC, and effective `k` so the outer agent can compare different structures by AIC.

For cold-start discovery, the agent may read Solver outputs only after the current proposal has been validated. It must not inspect historical `solver_result/` rankings or copied top-fit parameters before generating its initial proposals.

The agent must:

- Preserve numerical and physical cuts unless a human explicitly changes them.
- Record solver settings, random seeds, and output directories for reproducibility.
- When reporting accepted agent theories, include the complete dimension-balanced Lagrangian from the actual validated pkl object and the numerical best-fit coefficient values from Solver output. The report must preserve `√(-g)`, `M_p²`, `Λ` powers, and fixed scalar matter terms. An operator-only or bare `coefficient * operator` summary is not sufficient.
- Treat low chi2 with large constraint drift as invalid.
- Distinguish between structural failure and parameter-search failure.
- Use the real Solver output `chi2` for parameter optimization and sampling decisions; use AIC only in the outer cross-Lagrangian structure policy.
- Use isolated Solver output directories for agent validation so one-theory runs do not overwrite or confuse batch results.
- Treat agent-proposed parameter samples as part of the theory experiment. Learn which parameter regions produce accepted samples and lower chi-square.
- Label any use of historical Solver winners as replay/regression testing, not discovery.
- For scalaron models, sample `chi_bar_0_R_over_H0sq`, solve
  `qchi_0_dchi_bar_dln_a` from the initial lapse constraint, and reject the
  sample if `F<=0` or `f_RR<=0` at the initial point or anywhere on the trajectory.
- For pure `f(R)` branches, also reject non-positive local scalaron mass squared.
  For mixed `f(R,phi_i)` branches, do not replace the coupled scalar mass matrix
  by this one-field diagnostic.
- Treat `F>0` as the positive effective-Planck-mass condition and `f_RR>0` as
  the selected invertible, Dolgov--Kawasaki-stable branch condition.  Do not
  claim that these background checks replace a future perturbation analysis.

The agent must not:

- Relax constraints only to improve chi2.
- Replace the raw Solver/report chi-square ranking with AIC. AIC belongs to the outer structure-learning policy and must not erase or overwrite chi-square output.
- Hide rejected samples or remove failure reasons.
- Interpret a failed random scan as a proof that the theory is impossible.
- Use historical Solver top results as initial memory in a cold-start theory-generation loop.

## Failure Feedback

Solver failures should be treated as learning signals. The agent must inspect `reject_reasons_by_model.csv`, `scan_report.txt`, and the harness diagnostics before proposing the next theory.

Common reject reasons to record:

- Empty `model_ranking.csv`: no accepted parameter sample was found. This can mean poor parameter sampling, bad priors, or a structurally unstable theory.
- `q1_x not determined by coupled scalar EOM` / `q2_x not determined by coupled scalar EOM`: the scalar system was not converted into an explicit numerical RHS.
- `constraint drift too large`: the trajectory violates the constraint during integration.
- `H(z) absurdly large`: the trajectory is numerically or physically unstable.
- `EFT cutoff violated`: the sampled trajectory leaves the EFT-valid regime.
- `no-scalar constraint not satisfied at x=0`: a no-scalar model did not satisfy the initial constraint.
- Repeated rejections with the same reason: the current-loop memory should make this repetition visible to the proposal agent.

These are feedback facts, not hard-coded policy updates. The proposal agent should read the current-loop memory, write its own reflection, and decide whether the next proposal should resample parameters, change the theory structure, or explore a new family.

A failed Solver scan is not automatically proof that a theory is impossible. If the structure is physically interesting and Builder succeeded, the agent may propose a resampling experiment with larger `N_SAMPLES_PER_MODEL`, different `RANDOM_SEED`, or adjusted parameter priors. That experiment must be recorded separately from a new theory proposal.

## Accepted-Theory Report Format

Accepted model summaries should mirror `top10_lagrangians_initial_conditions.txt` where possible. For each accepted theory, write:

- the raw `general` Lagrangian from the validated `agent_lagrangians.pkl` or `lagrangians.pkl` object;
- the symbolic dimension-balanced Lagrangian, including `√(-g)`, `M_p²` prefactors, `Λ` powers, and fixed scalar matter terms;
- the numerical Lagrangian after substituting the accepted Solver row's coefficient values while preserving those dimensional factors;
- per-term metadata such as `sector`, `mass_dim`, `lambda_power`, fixed/non-fixed status, and whether the term belongs inside `M_p²(...)`;
- fit metrics, initial conditions, sampled values, and free coupling values;
- the proposal JSON path, Solver output directory, `model_ranking.csv`, `all_samples_summary.csv`, and `best_solution.csv`.

Do not describe an accepted theory only as a list of candidate operators, and do not drop the `M_p²` or `Λ` factors when reconstructing the Lagrangian. The dimensional normalization and best-fit numerical values are required to identify what Solver actually tested.

For multi-loop agent runs, accepted-theory reporting is a required output artifact, not just a chat summary. Generate `ai_theory_lab/reports/<run_name>/` with the fixed file set:

- `summary.md`
- `accepted_lagrangians_and_parameters.md`
- `accepted_lagrangians_full.md`
- `accepted_lagrangians_and_parameters.csv`
- `accepted_summary.json`
- `accepted_family_representatives.json`
- `accepted_chi2_bar.png`
- `top_h_overlay.png`
- `top3_h_panels.png`

These files must contain h(z) plots from the accepted solution CSVs, accepted chi-square plots, complete accepted Lagrangians, best-fit parameter values, and Solver output paths. Keep all accepted attempts in `accepted_summary.json`, but show only the best chi-square representative from each theory family in the human-facing markdown/CSV/plot files. Use `coarse_family_key` when available, falling back to exact `family_key`. The `summary.md` front page must show parameter choices for the top accepted family representatives, including the accepted sample index, `H0`, `Omega_m0`, `lambda_H`, scalar initial values, scalar mass/decay parameters, scalar velocities, and compact free-coefficient values. Use:

```bash
python -m ai_theory_lab.report --run-name <run_name> --top-n 20
```

## Agent Parameter Samples

By default Solver randomly samples all free numerical parameters from configured priors. For agent training, prefer explicit samples:

```bash
PARAMETER_SAMPLES_PATH=ai_theory_lab/runs/<run_id>/agent_parameter_samples.json python "Solver v5.2.py"
```

When `PARAMETER_SAMPLES_PATH` is set:

- The JSON file must contain a list of parameter objects, or an object with a `samples` list.
- Solver evaluates exactly those samples; `N_SAMPLES_PER_MODEL` no longer determines the number of evaluated samples.
- Missing required random/free parameters produce an explicit rejection, not a fallback to random sampling.
- Result CSVs include `agent_parameter_sample_index`.
- `all_samples_summary.csv` includes one row per evaluated parameter sample. Accepted rows contain finite `chi2`; rejected rows contain `success=false`, `reason`, `agent_parameter_sample_index`, and the proposed parameter values.

## Agent Parameter Search Policy

For cold-start discovery, the default agent parameter policy is:

- Apply a 120s wall-time limit to Solver setup/lambdify before parameter sampling begins.
- Propose 1000 explicit parameter samples for each theory.
- Do not stop the solve early when a sample reaches low chi-square; complete the
  configured sample budget so parameter-memory statistics remain comparable.
- If the first 1000 samples fail to produce `chi2 < 2000`, test 3000 explicit samples for the same theory before moving on.
- Use `all_samples_summary.csv` to learn from every accepted and rejected sample, not only the best model ranking.

The 120s setup wall should not be applied to the numerical sampling loop itself. If setup/lambdify exceeds the wall, record it as a pre-sampling timeout and move to the next theory.

Common parameter keys:

- `H0_km_s_Mpc`
- `Omega_m0`
- `lambda_H_Lambda_over_H0` or `log10_lambda_H`
- `varphi1_0_phi1_over_Mp`, `mu1_m1_over_H0`, `fbar1_f1_over_Mp`
- `varphi2_0_phi2_over_Lambda`, `mu2_m2_over_Lambda`, `fbar2_f2_over_Lambda`
- `q2_0_dvarphi2_dln_a` for two-scalar models where Solver solves `q1_0`; for `phi2_only` agent proposals, this value may also be supplied as a root-search hint while Solver still solves `q2_0` from `E_N(x=0)=0`
- `chi_bar_0_R_over_H0sq` for scalaron models; `qchi_0_dchi_bar_dln_a` is
  constraint-solved and is not an independent AIC parameter
- `q1_0_dvarphi1_dln_a` and/or `q2_0_dvarphi2_dln_a` when an independent
  scalaron is present, because the lapse constraint is then used to solve `qchi_0`
- free coefficient names such as `\\beta`, `\\gamma`, or `coefficient:\\beta`

Constraint-solved values such as `q1_0` in phi1 models and `q2_0` in phi2-only models are solved from `E_N(x=0)=0`. For `phi2_only` agent samples, a proposed `q2_0_dvarphi2_dln_a` is only a root-search hint/preference, not a bypass of the initial constraint.

## Useful Environment Settings

- `BUILD_CACHE_PATH`
- `SOLVER_OUTPUT_DIR`
- `SOLVER_RUN_NAME`
- `SOLVER_MAKE_PLOTS`
- `TOP_N`
- `PARAMETER_SAMPLES_PATH`
- `N_SAMPLES_PER_MODEL`
- `RANDOM_SEED`
- `SOLVER_PARALLEL`
- `N_WORKERS`
- `N_GRID`
- `RTOL`
- `ATOL`
- `MAX_ABS_CONSTRAINT`
- `H0_MIN`, `H0_MAX`
- `OMEGA_M0_MIN`, `OMEGA_M0_MAX`
- `LOG10_ABS_C_MIN`, `LOG10_ABS_C_MAX`
- `LOG10_LAMBDA_H_MIN`, `LOG10_LAMBDA_H_MAX`
- `ENFORCE_EFT_CUTOFF`
- `EFT_MAX_H_OVER_LAMBDA`

## Success Criteria

This stage succeeds when accepted samples are found and `model_ranking.csv` is sorted by increasing chi-square.

Failures here mean either no parameter samples were accepted or the numerical/likelihood evaluation rejected all sampled trajectories.

For agent/single-theory validation, the harness should set `BUILD_CACHE_PATH` to the isolated `agent_built_models_cache.pkl`, set `SOLVER_OUTPUT_DIR` to the isolated `agent_solver_result/`, and read `agent_solver_result/agent_solve/model_ranking.csv`. The harness may set `SOLVER_MAKE_PLOTS=0` and `TOP_N=0` because the validation gate only needs numeric outputs and Solver's real `chi2`.
