# AI Modified Gravity v5.4 AIC

This repository contains the production code for 1000-theory autonomous
searches of two-scalar, grammar-constrained modified-gravity models against
DES-SN and DESI DR2 BAO background data:

```text
Grammar Masker -> EOM ghost-cancellation filter -> Builder -> Solver
```

Run the deterministic stages in order:

```bash
python "GR_grammar_masker_v3.2.py"
python "EOM v5.2.py"
python "Builder v5.2.py"
python "Solver v5.2.py"
```

Install the Python dependencies into the project-local environment with:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Cold-start mini-batch discovery defaults to unrestricted open search. It does not reserve a dedicated non-EH proposal budget:

```bash
python -m ai_theory_lab.graph_agent_batch --group-mode open_only --help
```

Within a fixed Lagrangian, parameter samples and human-facing Solver reports remain ranked by total chi-square. Across different Lagrangian structures, the learned structure policy uses the AIC-equivalent score documented in `AGENTS.md` and `ai_theory_lab/proposal_schema.md`; raw chi-square, AIC, BIC, and the effective parameter count are all retained.

## Production 1000-theory runs

The matched six-provider benchmark uses 8 CPU cores per model and the common
1000/3000/5000 parameter-sampling schedule:

```bash
source .venv/bin/activate
source ~/.openai_env

python -m ai_theory_lab.check_api_connections \
  --preset frontier6 --live --timeout 60

python -m ai_theory_lab.submit_final_runs \
  --preset frontier6 \
  --attempts 1000 \
  --cpus 8 \
  --mem 32G \
  --time 72:00:00 \
  --group-mode open_only \
  --run-label frontier6_openonly_aic_v5_4 \
  --submit
```

Omit `--submit` for a dry run. Generated jobs fail immediately when a required
API key or compatible endpoint is missing.

The matched Claude 5 extension uses the same open-only numerical budget as the
1000-proposal frontier benchmark:

```bash
python -m ai_theory_lab.check_api_connections --preset claude5 --live --timeout 60
python -m ai_theory_lab.submit_final_runs \
  --preset claude5 --attempts 1000 --cpus 8 --mem 32G --time 72:00:00 \
  --group-mode open_only --run-label frontier6_openonly_aic_v5_4_claude5 \
  --submit
```

## Repository layout

- `gr_grammar_masker_v3_2/`: legal operator and invariant generation.
- `eom_v5_2/`: FLRW variation and derivative-order filtering.
- `builder_v5_2/`: reduced numerical model construction.
- `solver_v5_2/`: DES-SN and DESI DR2 BAO likelihood evaluation.
- `ai_theory_lab/`: proposal agents, AIC structure learning, scheduling,
  monitoring, and reports.
- `data/`: the observational inputs required by Solver.
- `tests/`: production regression tests.
- `cluster_tools/`: Oscar synchronization and preflight commands.
- `requirements.txt`: the maintained Python runtime dependencies.

Generated proposals, memory, reports, Solver output, serialized models, plots,
paper builds, and SLURM files are intentionally excluded from version control.

To avoid partial uploads or shell-glob mistakes, sync and verify the current production files with:

```bash
# Local Mac
bash cluster_tools/sync_code_to_oscar.sh

# Oscar login node
bash cluster_tools/preflight_1000_runs_on_oscar.sh
```
