#!/usr/bin/env bash
# Submit a cold-start LangGraph agent run on Oscar.
#
# Usage:
#   sbatch ai_theory_lab/cluster/submit_graph_agent.sbatch <run_name> [loops] [proposal_mode] [llm_model] [llm_fallback] [proposal_memory]

#SBATCH --job-name=mg-graph-agent
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --output=log/slurm/%x-%j.out
#SBATCH --error=log/slurm/%x-%j.err

set -euo pipefail

RUN_NAME="${1:?run name is required}"
LOOPS="${2:-20}"
PROPOSAL_MODE="${3:-deterministic}"
LLM_MODEL="${4:-}"
LLM_FALLBACK="${5:-deterministic}"
PROPOSAL_MEMORY="${6:-on}"
if [[ "${LLM_MODEL}" == "fail" || "${LLM_MODEL}" == "deterministic" ]]; then
  LLM_FALLBACK="${LLM_MODEL}"
  LLM_MODEL=""
  PROPOSAL_MEMORY="${5:-on}"
fi

cd "${SLURM_SUBMIT_DIR}"
mkdir -p log/slurm

source ai_theory_lab/cluster/oscar_env.sh
if [[ -f "${HOME}/.openai_env" ]]; then
  source "${HOME}/.openai_env"
fi

GRAPH_ARGS=(
  --loops "${LOOPS}"
  --run-name "${RUN_NAME}"
  --proposal-mode "${PROPOSAL_MODE}"
  --llm-fallback "${LLM_FALLBACK}"
  --llm-proposal-timeout 600
  --llm-api-timeout 120
  --pretty
)
if [[ -n "${LLM_MODEL}" ]]; then
  GRAPH_ARGS+=(--llm-model "${LLM_MODEL}")
fi
if [[ "${PROPOSAL_MEMORY}" == "off" || "${PROPOSAL_MEMORY}" == "no" || "${PROPOSAL_MEMORY}" == "false" ]]; then
  GRAPH_ARGS+=(--no-proposal-memory)
fi

python -m ai_theory_lab.graph_agent "${GRAPH_ARGS[@]}"

python -m ai_theory_lab.report \
  --run-name "${RUN_NAME}" \
  --top-n 20
