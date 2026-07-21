#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="wsun47@ssh.ccv.brown.edu"
REMOTE_BASE="/oscar/home/wsun47/Modify_GR"
OUT_BASE="cluster_report/cmp2000_cheap_partial_v1_full"

RUNS=(
  "cmp2000_openai_gpt_5_4_mini_cheap_v1"
  "cmp2000_claude_sonnet_4_6_cheap_v1"
  "cmp2000_gemini_2_5_flash_cheap_v1"
  "cmp2000_qwen3_7_plus_cheap_v1"
  "cmp2000_deepseek_ali_v4_pro_cheap_v1"
)

mkdir -p "$OUT_BASE"/{memory,proposals,reports}

# Reuse the authenticated SSH connection after the first Duo approval when possible.
SSH_CONTROL="${TMPDIR:-/tmp}/mg-rsync-%r@%h:%p"
SSH_CMD="ssh -o ControlMaster=auto -o ControlPersist=10m -o ControlPath=${SSH_CONTROL}"
RSYNC=(rsync -av -e "$SSH_CMD")

for run in "${RUNS[@]}"; do
  echo
  echo "== Pulling memory: $run =="
  mkdir -p "$OUT_BASE/memory/$run"
  "${RSYNC[@]}" \
    "${REMOTE_HOST}:${REMOTE_BASE}/ai_theory_lab/memory/${run}/" \
    "$OUT_BASE/memory/$run/"

  echo
  echo "== Pulling report: $run =="
  mkdir -p "$OUT_BASE/reports/$run"
  "${RSYNC[@]}" \
    "${REMOTE_HOST}:${REMOTE_BASE}/ai_theory_lab/reports/${run}/" \
    "$OUT_BASE/reports/$run/" || true

  echo
  echo "== Pulling lightweight proposals: $run =="
  mkdir -p "$OUT_BASE/proposals/$run"
  "${RSYNC[@]}" \
    --include='*/' \
    --include='scheduler_tasks.jsonl' \
    --include='task_*.json' \
    --exclude='*' \
    "${REMOTE_HOST}:${REMOTE_BASE}/ai_theory_lab/proposals/${run}/" \
    "$OUT_BASE/proposals/$run/"
done

echo
echo "== Pulling comparison report if present =="
mkdir -p "$OUT_BASE/reports/cmp2000_cheap_partial_timeout_v1"
"${RSYNC[@]}" \
  "${REMOTE_HOST}:${REMOTE_BASE}/ai_theory_lab/reports/cmp2000_cheap_partial_timeout_v1/" \
  "$OUT_BASE/reports/cmp2000_cheap_partial_timeout_v1/" || true

echo
echo "Done. Local output:"
find "$OUT_BASE" -maxdepth 3 -type f | sort | sed -n '1,80p'
