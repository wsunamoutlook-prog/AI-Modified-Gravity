#!/bin/bash
set -euo pipefail

cd ~/Modify_GR
source .venv/bin/activate
source ~/.openai_env

mkdir -p .matplotlib-cache log/slurm
export MPLCONFIGDIR="$PWD/.matplotlib-cache"

python -m compileall -q \
  ai_theory_lab \
  gr_grammar_masker_v3_2 \
  eom_v5_2 \
  builder_v5_2 \
  solver_v5_2

python -m unittest discover -s tests -v
python -m ai_theory_lab.build_token_context_cache --timeout 0
python -m ai_theory_lab.check_api_connections --preset frontier6 --live --timeout 60
python -m ai_theory_lab.check_api_connections --preset claude5 --live --timeout 60

python - <<'PY'
import inspect

from ai_theory_lab.graph_agent_batch import run_batch_agent
from ai_theory_lab.submit_final_runs import CLAUDE5_RUNS, FRONTIER6_RUNS

signature = inspect.signature(run_batch_agent)
assert signature.parameters["group_mode"].default == "open_only"
assert len(FRONTIER6_RUNS) == 6
assert len(CLAUDE5_RUNS) == 2
print("group_mode default: open_only")
print("frontier6:", ", ".join(run.model for run in FRONTIER6_RUNS))
print("claude5:", ", ".join(run.model for run in CLAUDE5_RUNS))
PY
