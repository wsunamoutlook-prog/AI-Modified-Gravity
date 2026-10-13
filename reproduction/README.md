# Supplementary calculations

Run these commands from the repository root with the virtual environment
activated. Use a new output directory for every experiment. The search launcher
copies source and data only: no old winners, learned memory, or numerical model
caches enter a new search. It retains the 1000/3000/5000 parameter schedule and
absolute chi-square gates described in the paper.

## CPL reference fit

```bash
python -m ai_theory_lab.fit_cpl --output-dir output/cpl
```

This fits flat `w(a) = w0 + wa*(1-a)` to the included DES-SN and DESI DR2 BAO
likelihood, with both nuisance scales profiled and no CMB or early-universe
sound-horizon constraint. It uses several DE starts and local refinement, checks
quadrature convergence, and records both the historical grid LambdaCDM reference
and a continuously optimized reference. It is a background parametrization;
the fit supplies no covariant action or perturbative stability result. It makes
no API calls and refuses to overwrite an existing output directory.

## Fixed-prior random search

```bash
python -m reproduction.search prepare --mode random --parents 1000 \
  --output-dir output/random1000
python -m reproduction.search run --output-dir output/random1000
```

This mode makes no API calls. It samples a scalar configuration, an operator
count from one to eight, an allowed potential, and a legal operator subset.
The parameter priors and correction-size mixture remain fixed. The mechanical
duplicate limit is retained, but results do not update later proposals or
parameter draws. Sampling is over grammar representations, not uniformly over
physical equivalence classes.

## Current-run memory comparison

Set `OPENAI_API_KEY` before the `run` commands. Each run makes paid model calls.

```bash
python -m reproduction.search prepare --mode memory-on --parents 250 \
  --model gpt-5.6-sol --output-dir output/memory_on250
python -m reproduction.search prepare --mode memory-off --parents 250 \
  --model gpt-5.6-sol --output-dir output/memory_off250
python -m reproduction.search run --output-dir output/memory_on250
python -m reproduction.search run --output-dir output/memory_off250
```

Memory-off retains LLM candidate selection and result logging, but removes prior
validation feedback from candidate selection and all three parameter-sampling
stages. No LLM weights are updated in either setting. Both runs use numerical
seed 20260607 and eight asynchronous slots by default. Different triggered
scans can give different realized evaluation counts. The comparison tests
structural and parameter feedback together.

## One LambdaCDM mock search

```bash
python -m reproduction.search prepare --mode mock --parents 250 \
  --mock-seed 20260908 --model gpt-5.6-sol --output-dir output/MOCK_lcdm250
python -m reproduction.search run --output-dir output/MOCK_lcdm250
```

Preparation generates **MOCK / SYNTHETIC** observations at the original
redshifts, using the full within-dataset covariance and independent Gaussian SN
and BAO noise streams. It also refits LambdaCDM to that realization. The SN input
stores packed precision; the generator uses the inverse-transpose Cholesky
operation, without adding diagonal noise a second time. It writes
`MOCK_DATA_001/manifest.json` and `MOCK_LCDM_reference.json`.

Use the refitted mock AIC as the baseline for every mock delta AIC. Never compare
a mock minimum with the observed-data reference, or mix mock records into
real-data search memory or paper tables. Keep the labelled directory when sharing
results; individual generic Solver files and plots need an explicit MOCK label
before export. One realization with 250 parents is a
search diagnostic, not a false-positive-rate estimate or a calibration of the
full eight-agent benchmark. The absolute refinement gates can allocate different
numerical work on real and synthetic data.

Mock preparation is local numerical work. Only the subsequent `run` command
starts the LLM search and incurs API charges. Data-only generation is also
available through `python -m ai_theory_lab.lcdm_mock --help`.

## Fixed-Lagrangian differential evolution

The seven files in `fixed7/` are archived covariant actions, retained as inputs
for this replay control. Their source paths and SHA-256 hashes are in
`ai_theory_lab/fixed7_resampling_manifest.json`. They are not cold-start search
seeds. Historical fit values in that manifest are comparison metadata and are
not used to initialize the DE population.

Prepare the numerical models, then run one proposal/replicate pair:

```bash
python -m ai_theory_lab.fixed_lagrangian_de --output-root output/fixed7_de prepare
python -m ai_theory_lab.fixed_lagrangian_de --output-root output/fixed7_de run \
  --proposal K301 --replicate 1 --evaluations 5000 --workers 8
```

For the complete control, repeat the second command for `G263`, `O769`, `F456`,
`Gm986`, `Q88`, `D820`, and `K301`, with replicate numbers 1 through 20. These
140 independent jobs can be submitted through a local cluster scheduler. Then:

```bash
python -m ai_theory_lab.fixed_lagrangian_de --output-root output/fixed7_de summarize \
  --expected-replicates 20
```

This measures finite-budget optimization variability for fixed actions. It is
not a theory-search baseline and its restart scatter is not an observational
parameter uncertainty.

## Provenance and execution

`reproduction.search prepare` writes `protocol.json`, input/source hashes, and a
private `workspace/`. `run` verifies those hashes and writes `console.log` and
`search_status.json`. A zero process exit code is not itself a count of completed
parents; use the recorded search history and final summaries for that count.
The launcher refuses to overwrite or silently restart a previous launch.

`--workers`, `--seed`, `--provider`, `--model`, `--api-key-env`, and `--base-url`
can be specified at preparation time. Changes to these settings define a new
run and are recorded in the protocol. Environment overrides of physics settings
and data paths are not inherited by this launcher.

The random and memory-off interventions are applied only to the private batch
source. Exact replacement guards fail if that source changes unexpectedly.
The EOM, Builder, Solver and likelihood implementations are shared across modes.
This is a portable v5.6 entry point for the recorded procedures, not an archived
copy of the historical experiment environment.
