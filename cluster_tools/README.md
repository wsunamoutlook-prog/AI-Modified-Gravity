# Oscar cluster tools

This directory contains the two maintained cluster helpers for the v5.4 AIC
1000-theory benchmark.

From the local repository, synchronize files tracked by the clean branch plus
the legal-operator token cache when it is available:

```bash
bash cluster_tools/sync_code_to_oscar.sh
```

On Oscar, compile the production modules, run the regression suite, and test
both supported API presets. The preflight also verifies (or builds once) the
141-candidate cache before concurrent jobs are submitted:

```bash
cd ~/Modify_GR
bash cluster_tools/preflight_1000_runs_on_oscar.sh
```

Generate or submit jobs through `ai_theory_lab.submit_final_runs`. Generated
`.slurm` files and all runtime artifacts are intentionally untracked.
