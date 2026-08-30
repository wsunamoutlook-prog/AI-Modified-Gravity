#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

RUNS=(
  cmp1000_claude_opus_5_frontier6_openonly_aic_v4_claude5
  cmp1000_claude_fable_5_frontier6_openonly_aic_v4_claude5
)

STAMP=${CLAUDE5_PAPER_STAMP:-20260824}
SCRATCH_ROOT=${CLAUDE5_SCRATCH_ROOT:-"/oscar/scratch/$USER"}
STAGE="$SCRATCH_ROOT/claude5_paper_inputs_$STAMP"
PACKAGE=${CLAUDE5_PAPER_PACKAGE:-"$SCRATCH_ROOT/claude5_paper_inputs_$STAMP.tar.gz"}
COMPARISON=ai_theory_lab/reports/claude5_openonly_aic_final

for run in "${RUNS[@]}"; do
  python -m ai_theory_lab.report --run-name "$run" --top-n 100
done

python -m ai_theory_lab.compare_benchmarks \
  --runs "${RUNS[@]}" \
  --output-dir "$COMPARISON"

if [[ -e "$STAGE" ]]; then
  echo "Refusing to reuse existing staging directory: $STAGE" >&2
  echo "Move it aside or set CLAUDE5_PAPER_STAMP, then rerun." >&2
  exit 2
fi

mkdir -p \
  "$STAGE/selected_tasks" \
  "$STAGE/selected_proposals" \
  "$STAGE/reports" \
  "$STAGE/memory" \
  "$STAGE/scheduler"

python scripts/summarize_llm_token_usage.py \
  --runs "${RUNS[@]}" \
  --output "$STAGE/llm_token_usage_summary.json"

python scripts/select_paper_inputs.py \
  --runs "${RUNS[@]}" \
  --report-root ai_theory_lab/reports \
  --output-json "$STAGE/selection_manifest.json" \
  --output-csv "$STAGE/selection_manifest.csv"

python - "$STAGE/selection_manifest.json" <<'PY' > "$STAGE/selections.tsv"
import json
import sys

manifest = json.load(open(sys.argv[1], encoding="utf-8"))
for item in manifest["selected_tasks"]:
    print("\t".join((item["run"], item["loop_id"], item["task_number"], item["task_dir"])))
PY

while IFS=$'\t' read -r run loop_id task_number task_dir; do
  [[ -d "$task_dir" ]] || {
    echo "Missing selected task directory: $task_dir" >&2
    exit 1
  }
  task_name=$(basename "$task_dir")
  task_dest="$STAGE/selected_tasks/$run/$task_name"

  while IFS= read -r -d '' source_file; do
    relative=${source_file#"$task_dir"/}
    mkdir -p "$task_dest/$(dirname "$relative")"
    cp -p "$source_file" "$task_dest/$relative"
  done < <(
    find "$task_dir" -type f \
      \( \
        -name 'agent_lagrangians.pkl' -o \
        -name 'agent_lagrangian_metadata.json' -o \
        -name 'eom_results.pkl' -o \
        -name 'eom_summary.txt' -o \
        -name 'build_cache_report.txt' -o \
        -name 'build_models_summary.csv' -o \
        -name 'model_ranking*.csv' -o \
        -name 'accepted_samples_summary*.csv' -o \
        -name 'all_samples_summary*.csv' -o \
        -name 'scan_report.txt' -o \
        -name 'best_solution.csv' -o \
        -name 'top_*_solution.csv' \
      \) -print0
  )

  proposal_dest="$STAGE/selected_proposals/$run"
  mkdir -p "$proposal_dest"
  find "ai_theory_lab/proposals/$run" -maxdepth 1 -type f \
    -name "${task_number}*.json" -exec cp -p {} "$proposal_dest/" \;

  if ! find "$task_dest" -name 'top_*_solution.csv' -print -quit | grep -q .; then
    echo "Missing H(z) solution CSV for $loop_id in $task_dir" >&2
    exit 1
  fi
done < "$STAGE/selections.tsv"

for run in "${RUNS[@]}"; do
  mkdir -p "$STAGE/reports/$run" "$STAGE/memory/$run" "$STAGE/scheduler/$run"
  cp -p \
    "ai_theory_lab/reports/$run/accepted_lagrangians_and_parameters.csv" \
    "ai_theory_lab/reports/$run/accepted_family_representatives.json" \
    "ai_theory_lab/reports/$run/benchmark_summary.json" \
    "ai_theory_lab/reports/$run/lcdm_reference.json" \
    "$STAGE/reports/$run/"
  cp -p \
    "ai_theory_lab/memory/$run/attempt_history.jsonl" \
    "$STAGE/memory/$run/"
  cp -p \
    "ai_theory_lab/proposals/$run/scheduler_tasks.jsonl" \
    "$STAGE/scheduler/$run/"
done

cp -a "$COMPARISON" "$STAGE/reports/claude5_openonly_aic_final"

tar -czf "$PACKAGE" -C "$SCRATCH_ROOT" "$(basename "$STAGE")"
tar -tzf "$PACKAGE" >/dev/null

SOLUTIONS=$(find "$STAGE/selected_tasks" -name 'top_*_solution.csv' | wc -l | tr -d ' ')
PROPOSALS=$(find "$STAGE/selected_proposals" -name 'task_*.json' | wc -l | tr -d ' ')
MEMORIES=$(find "$STAGE/memory" -name attempt_history.jsonl | wc -l | tr -d ' ')

echo
echo "Claude-5 paper-input package verified:"
ls -lh "$PACKAGE"
echo "Attempt histories: $MEMORIES"
echo "H(z) solution CSV files: $SOLUTIONS"
echo "Selected proposal JSON files: $PROPOSALS"
echo "Token usage summary: $STAGE/llm_token_usage_summary.json"
