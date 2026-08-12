#!/bin/bash
set -euo pipefail

cd ~/Modify_GR
source .venv/bin/activate
source ~/.openai_env

mkdir -p .matplotlib-cache log/slurm
export MPLCONFIGDIR="$PWD/.matplotlib-cache"

python -m py_compile \
  ai_theory_lab/agent_loop.py \
  ai_theory_lab/check_api_connections.py \
  ai_theory_lab/cold_start_runner.py \
  ai_theory_lab/dataset.py \
  ai_theory_lab/graph_agent.py \
  ai_theory_lab/graph_agent_batch.py \
  ai_theory_lab/harness.py \
  ai_theory_lab/joint_parameter_prior.py \
  ai_theory_lab/llm_agent.py \
  ai_theory_lab/memory.py \
  ai_theory_lab/report.py \
  ai_theory_lab/submit_final_runs.py \
  ai_theory_lab/validation_result.py \
  solver_v5_2/core.py \
  solver_v5_2/runner.py

python -m unittest discover -s tests -v
python -m ai_theory_lab.check_api_connections --preset frontier6 --live --timeout 30

python - <<'PY'
import inspect

from ai_theory_lab.graph_agent_batch import run_batch_agent
from ai_theory_lab.submit_final_runs import FRONTIER6_RUNS

signature = inspect.signature(run_batch_agent)
assert signature.parameters["group_mode"].default == "open_only"
print("group_mode default: open_only")
print("production models:", ", ".join(run.model for run in FRONTIER6_RUNS))
PY
