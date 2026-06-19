#!/bin/bash
#SBATCH --job-name=mg-async312
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=36:00:00
#SBATCH --output=log/slurm/mg-sector312-async-v6-%j.out
#SBATCH --error=log/slurm/mg-sector312-async-v6-%j.err
#SBATCH --export=ALL

cd ~/Modify_GR
source .venv/bin/activate
source ~/.openai_env

mkdir -p log/slurm .matplotlib-cache

export PYTHONUNBUFFERED=1
export MPLCONFIGDIR="$PWD/.matplotlib-cache"
export AGENT_MIN_OPERATOR_TERMS=1
export AGENT_MAX_OPERATOR_TERMS=8
export AGENT_OPERATOR_COUNT_FIXED_PROB=0.05
export AGENT_PROPOSAL_TIMEOUT_SECONDS=300
export SOLVER_PARALLEL=1
export N_WORKERS=$SLURM_CPUS_PER_TASK

python -m ai_theory_lab.graph_agent_batch \
  --waves 13 \
  --batch-size 24 \
  --target-attempts 312 \
  --initial-parameter-samples 1000 \
  --expanded-parameter-samples 3000 \
  --expanded-chi2-threshold 2000 \
  --n-workers "$SLURM_CPUS_PER_TASK" \
  --run-name graph_agent_batch_312_sector_async_v6 \
  --proposal-mode llm \
  --llm-model gpt-5-mini \
  --llm-fallback deterministic \
  --group-mode sector_split \
  --scheduler async_slots \
  --slot-count "$SLURM_CPUS_PER_TASK" \
  --slot-workers 1 \
  --timeout-setup 1200 \
  --pretty
