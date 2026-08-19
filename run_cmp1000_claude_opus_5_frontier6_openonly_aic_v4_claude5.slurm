#!/bin/bash
#SBATCH --job-name=mg-claude-opus51000
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=72:00:00
#SBATCH --output=log/slurm/mg-claude-opus51000-frontier6-openonly-aic-v4-claude5-%j.out
#SBATCH --error=log/slurm/mg-claude-opus51000-frontier6-openonly-aic-v4-claude5-%j.err
#SBATCH --export=ALL

set -euo pipefail

cd ~/Modify_GR
source .venv/bin/activate
source ~/.openai_env

: "${ANTHROPIC_API_KEY:?ANTHROPIC_API_KEY is required for claude-opus5}"

mkdir -p log/slurm .matplotlib-cache

export PYTHONUNBUFFERED=1
export MPLCONFIGDIR="$PWD/.matplotlib-cache"
export AGENT_MIN_OPERATOR_TERMS=1
export AGENT_MAX_OPERATOR_TERMS=8
export AGENT_OPERATOR_COUNT_FIXED_PROB=0.05
export SOLVER_PARALLEL=1
export N_WORKERS=$SLURM_CPUS_PER_TASK

python -m ai_theory_lab.graph_agent_batch \
  --waves 42 \
  --batch-size 24 \
  --target-attempts 1000 \
  --initial-parameter-samples 1000 \
  --expanded-parameter-samples 3000 \
  --expanded-chi2-threshold 2000 \
  --refine-parameter-samples 5000 \
  --refine-chi2-threshold 1638 \
  --n-workers "$SLURM_CPUS_PER_TASK" \
  --run-name cmp1000_claude_opus_5_frontier6_openonly_aic_v4_claude5 \
  --proposal-mode llm \
  --llm-provider anthropic \
  --llm-model claude-opus-5 \
  --llm-api-key-env ANTHROPIC_API_KEY \
  --llm-fallback skip \
  --group-mode open_only \
  --scheduler async_slots \
  --slot-count "$SLURM_CPUS_PER_TASK" \
  --slot-workers 1 \
  --diversity-strength 0.0 \
  --timeout-setup 1200 \
  --pretty
