#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
REMOTE_HOST=${MODIFY_GR_OSCAR_HOST:-wsun47@ssh.ccv.brown.edu}
REMOTE_ROOT=${MODIFY_GR_OSCAR_ROOT:-/oscar/home/wsun47/Modify_GR}
ARCHIVE_NAME=frontier6_paper_inputs_20260730.tar.gz
REMOTE_PACKAGE=${FRONTIER6_REMOTE_PAPER_PATH:-"/oscar/scratch/wsun47/$ARCHIVE_NAME"}
DEST=${FRONTIER6_LOCAL_DEST:-"$ROOT/cluster_report/frontier6_openonly_aic_final"}

CONTROL_DIR=$(mktemp -d)
CONTROL_SOCKET="$CONTROL_DIR/ssh-control"

cleanup() {
  ssh -S "$CONTROL_SOCKET" -O exit "$REMOTE_HOST" >/dev/null 2>&1 || true
  rmdir "$CONTROL_DIR" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "Opening one reusable Oscar SSH connection..."
ssh -M -S "$CONTROL_SOCKET" -fNT -o ControlPersist=600 "$REMOTE_HOST"

ssh -S "$CONTROL_SOCKET" "$REMOTE_HOST" "mkdir -p '$REMOTE_ROOT/scripts'"
rsync -avc --relative \
  -e "ssh -S $CONTROL_SOCKET" \
  "$ROOT/./scripts/select_frontier6_paper_inputs.py" \
  "$ROOT/./scripts/package_frontier6_paper_inputs.sh" \
  "$REMOTE_HOST:$REMOTE_ROOT/"

ssh -S "$CONTROL_SOCKET" "$REMOTE_HOST" \
  "cd '$REMOTE_ROOT' && chmod +x scripts/select_frontier6_paper_inputs.py scripts/package_frontier6_paper_inputs.sh && bash scripts/package_frontier6_paper_inputs.sh"

mkdir -p "$DEST"
rsync -av --progress \
  -e "ssh -S $CONTROL_SOCKET" \
  "$REMOTE_HOST:$REMOTE_PACKAGE" \
  "$DEST/$ARCHIVE_NAME"

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
echo "Frontier-6 paper inputs are ready:"
echo "$PAPER_ROOT"
echo "Selected task directories: $SELECTED"
echo "H(z) solution CSV files: $SOLUTIONS"
echo "Proposal JSON files: $PROPOSALS"
