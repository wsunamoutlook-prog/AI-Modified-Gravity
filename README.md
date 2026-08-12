# AI Modified Gravity

The current v5.2 pipeline searches two-scalar, grammar-constrained modified-gravity theories against DES-SN and DESI DR2 BAO background data:

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

Cold-start mini-batch discovery defaults to unrestricted open search. It does not reserve a dedicated non-EH proposal budget:

```bash
python -m ai_theory_lab.graph_agent_batch --group-mode open_only --help
```

Within a fixed Lagrangian, parameter samples and human-facing Solver reports remain ranked by total chi-square. Across different Lagrangian structures, the learned structure policy uses the AIC-equivalent score documented in `AGENTS.md` and `ai_theory_lab/proposal_schema.md`; raw chi-square, AIC, BIC, and the effective parameter count are all retained.

The current six-provider production preflight and SLURM generator are:

```bash
python -m ai_theory_lab.check_api_connections --preset frontier6 --live --timeout 30
python -m ai_theory_lab.submit_final_runs --preset frontier6 --attempts 600
```

The second command is a dry run unless `--submit` is added. Generated jobs default to `--group-mode open_only` and fail immediately when a required API key or compatible endpoint is missing. The older `cheap5` and `expensive3` presets are retained only for historical reproduction.

To avoid partial uploads or shell-glob mistakes, sync and verify the current production files with:

```bash
# Local Mac
bash scripts/sync_current_code_to_oscar.sh

# Oscar login node
bash scripts/preflight_frontier6_on_oscar.sh
```

Historical v3.x/v4.x CC+BAO entry points and random-EH-coefficient experiments remain in the repository for replay and regression only. They are not the current production pipeline.
