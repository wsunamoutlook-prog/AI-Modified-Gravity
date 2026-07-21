#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/cluster_report/cmp1500_expensive_v1/runs_by_task"
REMOTE_PREFIX="wsun47@ssh.ccv.brown.edu:/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs/."

mkdir -p "$DEST"

if [ "$#" -eq 0 ]; then
  set -- \
    cmp1500_openai_gpt_5_5_expensive_v1 \
    cmp1500_claude_opus_4_8_expensive_v1 \
    cmp1500_gemini_3_1_pro_expensive_v1
fi

pull_run() {
  local run="$1"
  echo "== pulling light per-task run artifacts for $run =="
  rsync -av --relative --prune-empty-dirs \
    --include='*/' \
    --include='agent_lagrangians.pkl' \
    --include='model_ranking.csv' \
    --include='accepted_samples_summary.csv' \
    --include='accepted_samples_summary_partial.csv' \
    --exclude='*' \
    "${REMOTE_PREFIX}/${run}*/" \
    "$DEST/"
}

for run in "$@"; do
  pull_run "$run"
done

echo
echo "Per-task directories:"
find "$DEST" -mindepth 1 -maxdepth 1 -type d | wc -l

echo "Accepted sample summaries:"
find "$DEST" -name 'accepted_samples_summary*.csv' | wc -l
