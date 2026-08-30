#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

STAMP=${CLAUDE5_PAPER_STAMP:-20260824}
REMOTE_HOST=${MODIFY_GR_OSCAR_HOST:-wsun47@ssh.ccv.brown.edu}
REMOTE_PACKAGE=${CLAUDE5_REMOTE_PACKAGE:-"/oscar/scratch/wsun47/claude5_paper_inputs_$STAMP.tar.gz"}
DEST=${CLAUDE5_PAPER_DEST:-"$ROOT/cluster_report/claude5_openonly_aic_final"}
LOCAL_PACKAGE="$DEST/$(basename "$REMOTE_PACKAGE")"

mkdir -p "$DEST"
rsync -av "$REMOTE_HOST:$REMOTE_PACKAGE" "$LOCAL_PACKAGE"
tar -xzf "$LOCAL_PACKAGE" -C "$DEST"

EXTRACTED="$DEST/claude5_paper_inputs_$STAMP"
[[ -d "$EXTRACTED" ]] || {
  echo "Missing extracted directory: $EXTRACTED" >&2
  exit 1
}

echo
echo "Claude-5 paper inputs are ready:"
echo "$EXTRACTED"
echo "Attempt histories: $(find "$EXTRACTED/memory" -name attempt_history.jsonl | wc -l | tr -d ' ')"
echo "H(z) solution CSV files: $(find "$EXTRACTED/selected_tasks" -name 'top_*_solution.csv' | wc -l | tr -d ' ')"
echo "Comparison summary: $(test -f "$EXTRACTED/reports/claude5_openonly_aic_final/comparison_metrics.csv" && echo present || echo missing)"
echo "Token usage summary: $(test -f "$EXTRACTED/llm_token_usage_summary.json" && echo present || echo missing)"
