#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

STAMP=20260730
SCRATCH_ROOT=${FRONTIER6_SCRATCH_ROOT:-"/oscar/scratch/$USER"}
STAGE="$SCRATCH_ROOT/frontier6_paper_inputs_$STAMP"
PACKAGE=${FRONTIER6_PAPER_PACKAGE:-"$SCRATCH_ROOT/frontier6_paper_inputs_$STAMP.tar.gz"}

if [[ -e "$STAGE" ]]; then
  echo "Refusing to reuse existing staging directory: $STAGE" >&2
  echo "Move it aside, then run this script again." >&2
  exit 2
fi

mkdir -p "$STAGE/selected_tasks" "$STAGE/selected_proposals" "$STAGE/reports"

python scripts/select_frontier6_paper_inputs.py \
  --report-root ai_theory_lab/reports \
  --output-json "$STAGE/selection_manifest.json" \
  --output-csv "$STAGE/selection_manifest.csv"

python - "$STAGE/selection_manifest.json" <<'PY' > "$STAGE/selections.tsv"
import json
import sys

manifest = json.load(open(sys.argv[1], encoding="utf-8"))
for item in manifest["selected_tasks"]:
    print(
        "\t".join(
            (
                item["run"],
                item["loop_id"],
                item["task_number"],
                item["task_dir"],
            )
        )
    )
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
        -name 'latest_built_models_cache_path.txt' -o \
        -name 'model_ranking*.csv' -o \
        -name 'accepted_samples_summary*.csv' -o \
        -name 'all_samples_summary*.csv' -o \
        -name 'reject_reasons_by_model*.csv' -o \
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

RUNS=(
  cmp1000_openai_gpt_5_6_sol_frontier6_openonly_aic_v2_8cpu
  cmp1000_claude_sonnet_5_frontier6_openonly_aic_v3_apifix
  cmp1000_gemini_3_6_flash_frontier6_openonly_aic_v3_apifix
  cmp1000_qwen3_7_max_frontier6_openonly_aic_v2_8cpu
  cmp1000_deepseek_ali_v4_pro_frontier6_openonly_aic_v3_apifix
  cmp1000_kimi_k3_frontier6_openonly_aic_v3_apifix
)

for run in "${RUNS[@]}"; do
  mkdir -p "$STAGE/reports/$run"
  cp -p \
    "ai_theory_lab/reports/$run/accepted_lagrangians_and_parameters.csv" \
    "ai_theory_lab/reports/$run/accepted_family_representatives.json" \
    "ai_theory_lab/reports/$run/benchmark_summary.json" \
    "ai_theory_lab/reports/$run/lcdm_reference.json" \
    "$STAGE/reports/$run/"
done

cp -a ai_theory_lab/reports/frontier6_openonly_aic_final \
  "$STAGE/reports/frontier6_openonly_aic_final"

tar -czf "$PACKAGE" -C "$SCRATCH_ROOT" "$(basename "$STAGE")"
tar -tzf "$PACKAGE" >/dev/null

SELECTED=$(python -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["selected_tasks"]))' \
  "$STAGE/selection_manifest.json")
SOLUTIONS=$(find "$STAGE/selected_tasks" -name 'top_*_solution.csv' | wc -l | tr -d ' ')
PROPOSALS=$(find "$STAGE/selected_proposals" -name 'task_*.json' | wc -l | tr -d ' ')

echo
echo "Paper-input package verified:"
ls -lh "$PACKAGE"
echo "Selected task directories: $SELECTED"
echo "H(z) solution CSV files: $SOLUTIONS"
echo "Proposal JSON files: $PROPOSALS"
