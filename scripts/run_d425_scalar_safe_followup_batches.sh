#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate

export SAMPLE_INTEGRATION_TIMEOUT_SECONDS=2
export WORKER_SAMPLE_PROGRESS=100

for part in 01 02 03 04 05; do
  echo "[D425 follow-up] starting part ${part}/05"
  python -m ai_theory_lab.harness \
    --agent-sample \
    --source-lagrangians ai_theory_lab/proposals/replay_d425_tensor_safe_5000_source.pkl \
    --agent-source-n-terms 7 \
    --agent-source-local-number 1 \
    --agent-parameter-samples "ai_theory_lab/proposals/replay_d425_tensor_scalar_safe_followup_5000_part${part}.json" \
    --agent-run-dir "ai_theory_lab/runs/replay_d425_tensor_scalar_safe_followup_5000_part${part}_v2_timeout2s" \
    --timeout-eom 180 \
    --timeout-builder 180 \
    --timeout-solver 3600 \
    --pretty
done
