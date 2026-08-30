#!/usr/bin/env bash

set -euo pipefail

cd "${HOME}/Modify_GR"

OUTPUT_ROOT="${FIXED7_OUTPUT_ROOT:-/oscar/scratch/$USER/fixed7_aic_resampling_20x5000_v1}"
EXPORTS="ALL,FIXED7_OUTPUT_ROOT=$OUTPUT_ROOT"

prep_job=$(sbatch --parsable --export="$EXPORTS" run_fixed7_resampling_prepare.slurm)
array_job=$(sbatch --parsable --dependency="afterok:$prep_job" --export="$EXPORTS" run_fixed7_resampling_array.slurm)
summary_job=$(sbatch --parsable --dependency="afterok:$array_job" --export="$EXPORTS" run_fixed7_resampling_summary.slurm)

printf 'prepare_job=%s\narray_job=%s\nsummary_job=%s\noutput_root=%s\n' \
  "$prep_job" "$array_job" "$summary_job" "$OUTPUT_ROOT"
