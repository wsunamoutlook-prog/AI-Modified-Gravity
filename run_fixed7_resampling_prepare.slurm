#!/bin/bash
#SBATCH --job-name=mg-fixed7-prep
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=slurm-fixed7-prep-%j.out

set -euo pipefail

cd "$HOME/Modify_GR"
source .venv/bin/activate

export MPLCONFIGDIR="${MPLCONFIGDIR:-$PWD/.matplotlib-cache}"
OUTPUT_ROOT="${FIXED7_OUTPUT_ROOT:-/oscar/scratch/$USER/fixed7_aic_resampling_20x5000_v1}"

python -m ai_theory_lab.fixed_lagrangian_resampling \
  --source-root ai_theory_lab/runs \
  --output-root "$OUTPUT_ROOT" \
  prepare
