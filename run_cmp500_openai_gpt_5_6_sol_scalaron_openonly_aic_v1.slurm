#!/bin/bash
#SBATCH --job-name=mg-openai500
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=72:00:00
#SBATCH --output=log/slurm/mg-openai500-scalaron-openonly-aic-v1-%j.out
#SBATCH --error=log/slurm/mg-openai500-scalaron-openonly-aic-v1-%j.err
#SBATCH --export=ALL

set -euo pipefail

cd ~/Modify_GR
source .venv/bin/activate
source ~/.openai_env

: "${OPENAI_API_KEY:?OPENAI_API_KEY is required for openai}"

mkdir -p log/slurm .matplotlib-cache

export PYTHONUNBUFFERED=1
export MPLCONFIGDIR="$PWD/.matplotlib-cache"
export AGENT_MIN_OPERATOR_TERMS=1
export AGENT_MAX_OPERATOR_TERMS=8
export AGENT_OPERATOR_COUNT_FIXED_PROB=0.05
export SOLVER_PARALLEL=1
export N_WORKERS=$SLURM_CPUS_PER_TASK

python -m ai_theory_lab.graph_agent_batch \
  --waves 21 \
  --batch-size 24 \
  --target-attempts 500 \
  --initial-parameter-samples 1000 \
  --expanded-parameter-samples 3000 \
  --expanded-chi2-threshold 2000 \
  --refine-parameter-samples 5000 \
  --refine-chi2-threshold 1638 \
  --n-workers "$SLURM_CPUS_PER_TASK" \
  --run-name cmp500_openai_gpt_5_6_sol_scalaron_openonly_aic_v1 \
  --proposal-mode llm \
  --llm-provider openai \
  --llm-model gpt-5.6-sol \
  --llm-api-key-env OPENAI_API_KEY \
  --llm-fallback skip \
  --group-mode open_only \
  --scheduler async_slots \
  --slot-count "$SLURM_CPUS_PER_TASK" \
  --slot-workers 1 \
  --diversity-strength 0.0 \
  --timeout-setup 1200 \
  --pretty
