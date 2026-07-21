#!/bin/bash
#SBATCH --job-name=mg-gemini2000
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=72:00:00
#SBATCH --output=log/slurm/mg-gemini2000-cheap-v1-%j.out
#SBATCH --error=log/slurm/mg-gemini2000-cheap-v1-%j.err
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
export SOLVER_PARALLEL=1
export N_WORKERS=$SLURM_CPUS_PER_TASK

python -m ai_theory_lab.graph_agent_batch \
  --waves 84 \
  --batch-size 24 \
  --target-attempts 2000 \
  --initial-parameter-samples 1000 \
  --expanded-parameter-samples 3000 \
  --expanded-chi2-threshold 2000 \
  --refine-parameter-samples 5000 \
  --refine-chi2-threshold 1638 \
  --non-eh-refine-parameter-samples 10000 \
  --non-eh-refine-chi2-threshold 2000 \
  --n-workers "$SLURM_CPUS_PER_TASK" \
  --run-name cmp2000_gemini_3_5_flash_cheap_v1 \
  --proposal-mode llm \
  --llm-provider openai_compatible \
  --llm-model gemini-3.5-flash \
  --llm-base-url "$GEMINI_BASE_URL" \
  --llm-api-key-env GEMINI_API_KEY \
  --llm-fallback deterministic \
  --group-mode sector_split \
  --scheduler async_slots \
  --slot-count "$SLURM_CPUS_PER_TASK" \
  --slot-workers 1 \
  --diversity-strength 0.0 \
  --timeout-setup 1200 \
  --pretty
