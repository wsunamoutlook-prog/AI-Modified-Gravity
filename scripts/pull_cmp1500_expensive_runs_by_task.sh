#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/cluster_report/cmp1500_expensive_v1/runs_by_task"
REMOTE_PREFIX="wsun47@ssh.ccv.brown.edu:/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/."

mkdir -p "$DEST"

pull_run() {
  local run="$1"
  echo "== pulling per-task run artifacts for $run =="
  rsync -av --relative --prune-empty-dirs \
    --include='*/' \
    --include='agent_lagrangians.pkl' \
    --include='agent_parameter_samples_by_lag_id.json' \
    --include='model_ranking.csv' \
    --include='accepted_samples_summary.csv' \
    --include='accepted_samples_summary_partial.csv' \
    --exclude='*' \
    "${REMOTE_PREFIX}/${run}*/" \
    "$DEST/"
}

pull_run "cmp1500_openai_gpt_5_5_expensive_v1"
pull_run "cmp1500_claude_opus_4_8_expensive_v1"
pull_run "cmp1500_gemini_3_1_pro_expensive_v1"

echo
echo "Per-task directories:"
find "$DEST" -mindepth 1 -maxdepth 1 -type d | wc -l

echo "Accepted sample summaries:"
find "$DEST" -name 'accepted_samples_summary*.csv' | wc -l
