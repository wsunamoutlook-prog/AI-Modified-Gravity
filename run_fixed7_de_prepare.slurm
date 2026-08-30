#!/bin/bash
#SBATCH --job-name=mg-fixed7-de-prep
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=slurm-fixed7-de-prep-%j.out

set -euo pipefail

cd "$HOME/Modify_GR"
source .venv/bin/activate

export MPLCONFIGDIR="${MPLCONFIGDIR:-$PWD/.matplotlib-cache}"
OUTPUT_ROOT="${FIXED7_DE_OUTPUT_ROOT:-/oscar/scratch/$USER/fixed7_de_20x5000_v1}"
SOURCE_ROOT="${FIXED7_SOURCE_ROOT:-/oscar/scratch/$USER/Modify_GR_artifacts/runs}"

python -m ai_theory_lab.fixed_lagrangian_de \
  --source-root "$SOURCE_ROOT" \
  --output-root "$OUTPUT_ROOT" \
  prepare
