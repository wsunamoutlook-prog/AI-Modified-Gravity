#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
DEST=${FRONTIER6_LOCAL_DEST:-"$ROOT/cluster_report/frontier6_openonly_aic_final"}
ARCHIVE_NAME=frontier6_paper_inputs_20260730.tar.gz
REMOTE=${FRONTIER6_REMOTE_PAPER_PACKAGE:-"wsun47@ssh.ccv.brown.edu:/oscar/scratch/wsun47/$ARCHIVE_NAME"}

mkdir -p "$DEST"
rsync -av --progress "$REMOTE" "$DEST/$ARCHIVE_NAME"
tar -xzf "$DEST/$ARCHIVE_NAME" -C "$DEST"
tar -tzf "$DEST/$ARCHIVE_NAME" >/dev/null

PAPER_ROOT="$DEST/frontier6_paper_inputs_20260730"
MANIFEST="$PAPER_ROOT/selection_manifest.json"
[[ -f "$MANIFEST" ]] || {
  echo "Missing selection manifest after extraction: $MANIFEST" >&2
  exit 1
}

SELECTED=$(python -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["selected_tasks"]))' \
  "$MANIFEST")
SOLUTIONS=$(find "$PAPER_ROOT/selected_tasks" -name 'top_*_solution.csv' | wc -l | tr -d ' ')
PROPOSALS=$(find "$PAPER_ROOT/selected_proposals" -name 'task_*.json' | wc -l | tr -d ' ')

echo
echo "Frontier-6 paper inputs extracted to:"
echo "$PAPER_ROOT"
echo "Selected task directories: $SELECTED"
echo "H(z) solution CSV files: $SOLUTIONS"
echo "Proposal JSON files: $PROPOSALS"
