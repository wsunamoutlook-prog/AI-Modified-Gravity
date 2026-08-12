#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

RUNS=(
  cmp1000_openai_gpt_5_6_sol_frontier6_openonly_aic_v2_8cpu
  cmp1000_claude_sonnet_5_frontier6_openonly_aic_v3_apifix
  cmp1000_gemini_3_6_flash_frontier6_openonly_aic_v3_apifix
  cmp1000_qwen3_7_max_frontier6_openonly_aic_v2_8cpu
  cmp1000_deepseek_ali_v4_pro_frontier6_openonly_aic_v3_apifix
  cmp1000_kimi_k3_frontier6_openonly_aic_v3_apifix
)

COMPARISON_DIR=ai_theory_lab/reports/frontier6_openonly_aic_final
if [[ -d "/oscar/scratch/${USER:-}" ]]; then
  PACKAGE_DIR="/oscar/scratch/$USER"
else
  PACKAGE_DIR="$ROOT/cluster_report"
fi
PACKAGE=${FRONTIER6_PACKAGE:-"$PACKAGE_DIR/frontier6_openonly_aic_final_20260730.tar.gz"}
MANIFEST=$(mktemp)
trap 'rm -f "$MANIFEST"' EXIT

for run in "${RUNS[@]}"; do
  report_dir="ai_theory_lab/reports/$run"
  memory_dir="ai_theory_lab/memory/$run"
  scheduler="ai_theory_lab/proposals/$run/scheduler_tasks.jsonl"
  [[ -d "$report_dir" ]] || { echo "Missing report directory: $report_dir" >&2; exit 1; }
  [[ -f "$memory_dir/attempt_history.jsonl" ]] || {
    echo "Missing attempt history: $memory_dir/attempt_history.jsonl" >&2
    exit 1
  }
  [[ -f "$scheduler" ]] || { echo "Missing scheduler log: $scheduler" >&2; exit 1; }
done

python -m ai_theory_lab.compare_benchmarks \
  --runs "${RUNS[@]}" \
  --output-dir "$COMPARISON_DIR"

printf '%s\n' "$COMPARISON_DIR" >> "$MANIFEST"
for run in "${RUNS[@]}"; do
  printf '%s\n' "ai_theory_lab/reports/$run" >> "$MANIFEST"
  for name in \
    attempt_history.jsonl \
    feedback_summary.json \
    policy_summary.json \
    structure_prior.json \
    parameter_prior.json
  do
    path="ai_theory_lab/memory/$run/$name"
    [[ -f "$path" ]] && printf '%s\n' "$path" >> "$MANIFEST"
  done
  printf '%s\n' "ai_theory_lab/proposals/$run/scheduler_tasks.jsonl" >> "$MANIFEST"
done

mkdir -p "$(dirname "$PACKAGE")"
tar -czf "$PACKAGE" -T "$MANIFEST"
tar -tzf "$PACKAGE" >/dev/null

if tar -tzf "$PACKAGE" | grep -Eq '/task_[^/]*\.json$'; then
  echo "Refusing package: task proposal JSON files were included." >&2
  exit 1
fi

echo
echo "Package verified:"
ls -lh "$PACKAGE"
echo "Single-run reports: $(tar -tzf "$PACKAGE" | grep -c '/benchmark_summary.json$' || true)"
echo "Comparison summary: $(tar -tzf "$PACKAGE" | grep -c 'frontier6_openonly_aic_final/comparison_summary.json$' || true)"
echo "Task proposal JSON files: 0"
