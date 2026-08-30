#!/bin/bash
#SBATCH --job-name=mg-fixed7-summary
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00
#SBATCH --output=slurm-fixed7-summary-%j.out

set -euo pipefail

cd "$HOME/Modify_GR"
source .venv/bin/activate

OUTPUT_ROOT="${FIXED7_OUTPUT_ROOT:-/oscar/scratch/$USER/fixed7_aic_resampling_20x5000_v1}"

python -m ai_theory_lab.fixed_lagrangian_resampling \
  --output-root "$OUTPUT_ROOT" \
  summarize \
  --expected-replicates 20

echo "Summary written to: $OUTPUT_ROOT/summary"
