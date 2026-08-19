#!/bin/bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
REMOTE=${MODIFY_GR_OSCAR_REMOTE:-wsun47@ssh.ccv.brown.edu:/oscar/home/wsun47/Modify_GR/}

cd "$ROOT"

rsync -avc --itemize-changes --relative \
  ./README.md \
  ./AGENTS.md \
  ./ai_theory_lab/agent_loop.py \
  ./ai_theory_lab/check_api_connections.py \
  ./ai_theory_lab/cold_start_loop.md \
  ./ai_theory_lab/cold_start_runner.py \
  ./ai_theory_lab/dataset.py \
  ./ai_theory_lab/graph_agent.py \
  ./ai_theory_lab/graph_agent_batch.py \
  ./ai_theory_lab/harness.py \
  ./ai_theory_lab/joint_parameter_prior.py \
  ./ai_theory_lab/langsmith_live_monitor.py \
  ./ai_theory_lab/llm_agent.py \
  ./ai_theory_lab/memory.py \
  ./ai_theory_lab/proposal_schema.md \
  ./ai_theory_lab/report.py \
  ./ai_theory_lab/compare_benchmarks.py \
  ./ai_theory_lab/submit_final_runs.py \
  ./ai_theory_lab/tracing.py \
  ./ai_theory_lab/validation_result.py \
  ./solver_v5_2/AGENT.md \
  ./solver_v5_2/core.py \
  ./solver_v5_2/runner.py \
  ./tests/test_compare_benchmarks.py \
  ./tests/test_hybrid_model_selection.py \
  ./tests/test_open_only_scheduler.py \
  ./run_cmp1000_claude_opus_5_frontier6_openonly_aic_v4_claude5.slurm \
  ./run_cmp1000_claude_fable_5_frontier6_openonly_aic_v4_claude5.slurm \
  ./scripts/sync_current_code_to_oscar.sh \
  ./scripts/preflight_frontier6_on_oscar.sh \
  ./scripts/package_frontier6_openonly_results.sh \
  ./scripts/pull_frontier6_openonly_results.sh \
  ./scripts/select_frontier6_paper_inputs.py \
  ./scripts/audit_frontier6_paper_inputs.py \
  ./scripts/package_frontier6_paper_inputs.sh \
  ./scripts/pull_frontier6_paper_inputs.sh \
  ./scripts/fetch_frontier6_paper_inputs.sh \
  "$REMOTE"
