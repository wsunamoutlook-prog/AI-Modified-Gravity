#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
DEST=${FRONTIER6_LOCAL_DEST:-"$ROOT/cluster_report/frontier6_openonly_aic_final"}
ARCHIVE_NAME=frontier6_openonly_aic_final_20260730.tar.gz
REMOTE=${FRONTIER6_REMOTE_PACKAGE:-"wsun47@ssh.ccv.brown.edu:/oscar/scratch/wsun47/$ARCHIVE_NAME"}

mkdir -p "$DEST"
rsync -av --progress "$REMOTE" "$DEST/$ARCHIVE_NAME"
tar -xzf "$DEST/$ARCHIVE_NAME" -C "$DEST"
tar -tzf "$DEST/$ARCHIVE_NAME" >/dev/null

REPORT_ROOT="$DEST/ai_theory_lab/reports"
SINGLE_REPORTS=$(find "$REPORT_ROOT" -name benchmark_summary.json -type f | wc -l | tr -d ' ')
COMPARISON="$REPORT_ROOT/frontier6_openonly_aic_final/comparison_summary.json"

echo
echo "Frontier-6 package extracted to:"
echo "$DEST"
echo "Single-run reports: $SINGLE_REPORTS"
if [[ -f "$COMPARISON" ]]; then
  echo "Comparison summary: present"
else
  echo "Comparison summary: missing" >&2
  exit 1
fi
