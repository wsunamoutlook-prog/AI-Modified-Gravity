# Builder Stage

This stage parses ghost-free EOM output and builds cached dimensionless model objects for numerical solving.

For a theory-generating agent, passing Builder means a theory is ready for numerical testing. It still must be evaluated by actually running Solver against DES-SN + DESI-DR2 BAO data, where lower Solver-written `chi2` indicates a better fit.

## Role In Pipeline

Input:

- `eom_results/eom_summary.txt` from `eom_v5_2`
- For agent/single-theory validation: isolated `agent_eom_results/eom_summary.txt` through `EOM_SUMMARY_PATH`
- Run settings from `Builder v5.2.py`

Output:

- `solver_result/<run>/built_models_cache.pkl`
- `solver_result/<run>/build_models_summary.csv`
- `solver_result/<run>/build_cache_report.txt`
- `solver_result/latest_built_models_cache_path.txt`
- For agent/single-theory validation: isolated `agent_built_models_cache.pkl`

Downstream consumer:

- `solver_v5_2` loads `built_models_cache.pkl`

## Main Files

- `runner.py`: orchestrates parsing, symbolic building, cache writing, and build reports.
- `core.py`: parses EOM summaries, constructs dimensionless equations, extracts RHS systems, and defines the `Model` dataclass.

## Build Contract

Builder converts accepted symbolic EOMs into numerical-ready model caches.

It records:

- `lag_id`
- `scalar_config`
- `general`
- `gf_relations`
- `free_symbols`
- `dimless_exprs`
- `rhs_exprs`
- `reject_reason`

Models with `reject_reason` are structurally skipped by Solver.

## Agent Responsibilities

The agent may:

- Use `build_models_summary.csv` to learn which ghost-free EOMs can be built numerically.
- Adjust build selection settings for experiments, such as scalar-configuration filters or model caps.
- Prefer theory structures that Builder can convert into linear or general RHS systems reliably.

The agent must:

- Treat Builder rejection as a hard structural/numerical-preparation failure.
- Keep build settings recorded with each experiment.
- Rebuild the cache when symbolic build settings change.
- Send Builder-accepted models to the real Solver code for real-data comparison before ranking them as good theories.
- Use `BUILD_CACHE_PATH` for isolated agent validation so Solver loads the agent-specific cache.
- In agent/single-theory validation, write `agent_built_models_cache.pkl` and pass that exact path to Solver. Do not let Solver fall back to `solver_result/latest_built_models_cache_path.txt` from a previous full-batch run.

The agent must not:

- Edit cached model objects manually.
- Ignore metadata mismatch warnings between Builder and Solver.
- Change normalization or EFT settings silently.

## Failure Feedback

Builder failures are not data-fit failures. They mean the symbolic EOMs could not be converted into a reliable numerical model under the current Builder settings.

Common feedback rules:

- `symbolic build timeout > 60s`: next proposals should reduce symbolic complexity. Prefer fewer terms, fewer high-curvature contractions, fewer derivative curvature operators, and fewer scalar-curvature derivative couplings.
- Missing or unusable RHS expressions: next proposals should simplify the scalar sector, avoid coupled derivative structures, and prefer forms that allow linear RHS extraction.
- Models with `reject_reason` should not be ranked by chi-square. They should be recorded as structural/numerical-preparation failures and sent back to proposal revision.

If many proposals fail at Builder, the agent should shift exploration toward lower term counts and previously buildable scalar configurations before spending more Solver samples.

## Useful Environment Settings

- `EOM_SUMMARY_PATH`
- `BUILD_CACHE_PATH`
- `SOLVER_OUTPUT_DIR`
- `SOLVER_RUN_NAME`
- `SCALAR_CONFIG_FILTER`
- `MAX_MODELS_TO_BUILD`
- `BUILD_SIMPLIFY_MODE`
- `USE_LINEAR_RHS_SOLVER`
- `ALLOW_GENERAL_SYMBOLIC_SOLVE`
- `RHS_SIMPLIFY_MODE`
- `BUILD_TIMEOUT_SECONDS`
- `FIX_EH_COEFFICIENT`
- `ENFORCE_EFT_CUTOFF`

## Success Criteria

This stage succeeds when a `built_models_cache.pkl` is written and contains active models without `reject_reason`.

Failures here mean the theory passed EOM analysis but could not be converted into a reliable Solver-ready system.
