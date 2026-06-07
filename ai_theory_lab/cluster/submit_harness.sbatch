#!/usr/bin/env bash
# Submit one isolated harness validation on Oscar.
#
# Usage:
#   sbatch ai_theory_lab/cluster/submit_harness.sbatch <proposal.json> <run_name> [loop_id]

#SBATCH --job-name=mg-harness
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=00:30:00
#SBATCH --output=log/slurm/%x-%j.out
#SBATCH --error=log/slurm/%x-%j.err

set -euo pipefail

PROPOSAL_PATH="${1:?proposal JSON path is required}"
RUN_NAME="${2:?run name is required}"
LOOP_ID="${3:-loop_01}"

cd "${SLURM_SUBMIT_DIR}"
mkdir -p log/slurm ai_theory_lab/memory/"${RUN_NAME}"

source ai_theory_lab/cluster/oscar_env.sh

python -m ai_theory_lab.harness \
  --proposal "${PROPOSAL_PATH}" \
  --memory-dir "ai_theory_lab/memory/${RUN_NAME}" \
  --loop-id "${LOOP_ID}" \
  --timeout-eom 120 \
  --timeout-builder 120 \
  --timeout-solver 7200 \
  --env SOLVER_MAKE_PLOTS=0 \
  --env TOP_N=0 \
  --pretty
