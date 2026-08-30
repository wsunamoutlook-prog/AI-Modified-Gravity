# Fixed-Lagrangian Resampling Control

This experiment measures finite-budget parameter-search variability for the
seven non-Sonnet headline representatives. It is a replay/control study, not a
cold-start agent run.

## Contract

- Keep each validated serialized Lagrangian fixed.
- Keep the broad cold-start parameter prior fixed.
- Disable current-loop and joint-parameter memory.
- Run 20 independent random seeds.
- Evaluate 5000 explicit parameter vectors per Lagrangian and seed.
- Record one minimum chi-square/AIC per scan, including scans with no accepted
  point.

The resulting standard deviation describes finite-budget parameter-search
variability. It is not a data error bar and does not measure variability of the
LLM proposal agent.

## Oscar

The submission helper creates a preparation job, a dependent 20-element Slurm
array, and a dependent summary job:

```bash
cd ~/Modify_GR
bash scripts/submit_fixed7_resampling_oscar.sh
```

By default, results are written to:

```text
/oscar/scratch/$USER/fixed7_aic_resampling_20x5000_v1
```

Override that location before submission when needed:

```bash
export FIXED7_OUTPUT_ROOT=/oscar/scratch/$USER/my_fixed7_control
bash scripts/submit_fixed7_resampling_oscar.sh
```

The summary directory contains the raw replicate minima, a machine-readable
summary, a short report, and a PRD-compatible LaTeX table.
