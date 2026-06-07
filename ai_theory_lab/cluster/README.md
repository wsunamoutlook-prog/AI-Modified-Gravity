# Oscar Cluster Setup

These files provide the first Oscar integration layer for the modified-gravity
pipeline. LangGraph remains the orchestrator; Slurm only runs the deterministic
harness or graph-agent process on a compute node.

## Oscar Facts From Initial Check

- Login host: `ssh wsun47@ssh.ccv.brown.edu`
- Available Python module: `python/3.12.8-zr3c`
- Available CPU partitions for this user include `debug` and `batch`.
- The default account association is available for `wsun47`.

## Sync Project To Oscar

From the local machine, run this from the parent directory of the repository:

```bash
rsync -av --exclude .git --exclude .venv --exclude __pycache__ \
  --exclude 'ai_theory_lab/runs' \
  --exclude 'ai_theory_lab/reports' \
  --exclude 'ai_theory_lab/memory' \
  --exclude 'ai_theory_lab/proposals' \
  --exclude 'solver_result' \
  "Modify GR/" wsun47@ssh.ccv.brown.edu:~/Modify_GR/
```

If the repository is already on Oscar through Git, clone or pull it instead.

## First Login Setup

On Oscar:

```bash
cd ~/Modify_GR
source ai_theory_lab/cluster/oscar_env.sh
python --version
python -m ai_theory_lab.harness --read-latest-only --pretty
```

The environment script creates `.venv` on Oscar and installs the project
dependencies listed in `requirements-oscar.txt`.

## Smoke Test One Proposal

Use the `debug` partition for a short proposal validation:

```bash
cd ~/Modify_GR
sbatch ai_theory_lab/cluster/submit_harness.sbatch \
  ai_theory_lab/proposal_example.json \
  oscar_harness_smoke \
  loop_01
```

Watch status:

```bash
squeue -u wsun47
tail -f log/slurm/mg-harness-<jobid>.out
```

## Run LangGraph Agent

Use the `batch` partition for multi-loop discovery:

```bash
cd ~/Modify_GR
sbatch ai_theory_lab/cluster/submit_graph_agent.sbatch \
  graph_agent_oscar_20 \
  20
```

Use OpenAI API selection from grammar-generated candidates by passing `llm`:

```bash
cd ~/Modify_GR
sbatch ai_theory_lab/cluster/submit_graph_agent.sbatch \
  graph_agent_oscar_llm_smoke_1 \
  1 \
  llm
```

For a strict LLM run that stops instead of mixing in deterministic fallback
when the API fails:

```bash
cd ~/Modify_GR
sbatch ai_theory_lab/cluster/submit_graph_agent.sbatch \
  graph_agent_oscar_llm_strict_30 \
  30 \
  llm \
  fail
```

To keep writing memory/report artifacts but prevent the next proposal from
reading current-loop memory feedback, pass `off` after the fallback argument:

```bash
cd ~/Modify_GR
sbatch ai_theory_lab/cluster/submit_graph_agent.sbatch \
  graph_agent_oscar_llm_strict_50_nomem \
  50 \
  llm \
  fail \
  off
```

The Slurm script sources `~/.openai_env` when it exists. Keep that file outside
the repository and readable only by you:

```bash
chmod 600 ~/.openai_env
```

This runs:

```text
graph_agent -> harness -> EOM -> Builder -> Solver -> memory -> report
```

The report is written to:

```text
ai_theory_lab/reports/<run_name>/
```

## Sync Results Back

From the local machine:

```bash
rsync -av wsun47@ssh.ccv.brown.edu:~/Modify_GR/ai_theory_lab/reports/ ai_theory_lab/reports/
rsync -av wsun47@ssh.ccv.brown.edu:~/Modify_GR/ai_theory_lab/memory/ ai_theory_lab/memory/
rsync -av wsun47@ssh.ccv.brown.edu:~/Modify_GR/ai_theory_lab/proposals/ ai_theory_lab/proposals/
rsync -av wsun47@ssh.ccv.brown.edu:~/Modify_GR/ai_theory_lab/runs/ ai_theory_lab/runs/
```

## Notes

- Do not store API keys in this repository. Set `OPENAI_API_KEY` in the Oscar
  shell or a user-owned environment file when the Agent API layer is added.
- Keep new agent work pointed at `ai_theory_lab.graph_agent`; `graph.py` is a
  legacy minimal validation wrapper.
- LLM proposal work must obey `ai_theory_lab/lagrangian_legality.md`; the agent
  may choose or compose Grammar Masker candidates, but the compiled theory must
  include `sqrt(-g)`, sector-specific `M_p^2` placement, EFT `Lambda` powers,
  fixed scalar matter terms, and dimension-4 balancing.
- If the first Slurm job fails during pip install, rerun the same command after
  the environment finishes building or install dependencies interactively with
  `source ai_theory_lab/cluster/oscar_env.sh`.
