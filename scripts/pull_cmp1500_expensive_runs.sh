#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/cluster_report/cmp1500_expensive_v1/runs"
REMOTE="wsun47@ssh.ccv.brown.edu:/oscar/home/wsun47/Modify_GR/ai_theory_lab/runs"

mkdir -p "$DEST"

pull_run() {
  local run="$1"
  echo "== pulling run artifacts for $run =="
  rsync -av --prune-empty-dirs \
    --include='*/' \
    --include='agent_lagrangians.pkl' \
    --include='agent_parameter_samples_by_lag_id.json' \
    --include='model_ranking.csv' \
    --include='accepted_samples_summary.csv' \
    --include='accepted_samples_summary_partial.csv' \
    --exclude='*' \
    "$REMOTE/${run}*/" \
    "$DEST/"
}

pull_run "cmp1500_openai_gpt_5_5_expensive_v1"
pull_run "cmp1500_claude_opus_4_8_expensive_v1"
pull_run "cmp1500_gemini_3_1_pro_expensive_v1"

echo
echo "Pulled accepted sample summaries:"
find "$DEST" -name 'accepted_samples_summary*.csv' | wc -l
