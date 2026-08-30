#!/bin/bash
#SBATCH --job-name=mg-fixed7-de
#SBATCH --array=1-140%20
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --output=slurm-fixed7-de-%A_%a.out

set -euo pipefail

cd "$HOME/Modify_GR"
source .venv/bin/activate

export MPLCONFIGDIR="${MPLCONFIGDIR:-$PWD/.matplotlib-cache}"
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
OUTPUT_ROOT="${FIXED7_DE_OUTPUT_ROOT:-/oscar/scratch/$USER/fixed7_de_20x5000_v1}"

python -m ai_theory_lab.fixed_lagrangian_de \
  --output-root "$OUTPUT_ROOT" \
  run \
  --task-index "$SLURM_ARRAY_TASK_ID" \
  --evaluations 5000 \
  --population-size 50 \
  --workers 8
