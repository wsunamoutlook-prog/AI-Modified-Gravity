# CosmoAgent — v5.6

Code for *CosmoAgent: AI Agent for Theoretical Cosmology*.
CosmoAgent searches a finite grammar of covariant gravity and scalar-field
Lagrangians, derives their homogeneous equations, and fits the resulting
expansion histories to DES supernova and DESI DR2 BAO data. The LLM selects
candidates; the symbolic and numerical calculations are performed by the code.

This branch contains the current pipeline and the supplementary experiment
entry points. Generated search histories, numerical caches, old manuscripts,
and cluster-specific job files are excluded. The likelihood inputs and the
seven fixed Lagrangians needed for the DE control are included.
Historical artifacts remain in the `v5.5scalaron` branch and Git history.

## Installation

Use Python 3.12 on Linux or macOS. Run the commands below from the repository
root. A shallow clone avoids downloading the large experimental archives in
older Git history.

```bash
git clone --branch v5.6 --single-branch --depth 1 \
  https://github.com/wsunamoutlook-prog/AI-Modified-Gravity.git
cd AI-Modified-Gravity
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -c requirements-tested.txt
export MPLCONFIGDIR="$PWD/.matplotlib-cache"
```

`requirements-tested.txt` records the top-level package versions used for
release checks; it is not a complete transitive dependency lock. The physics
pipeline, CPL fit, random control, and DE control do not require an API key.
LLM searches do and incur provider charges. No API call is made by installation,
`--help`, or the test suite.

## Calculation order

```text
Grammar -> scalaron transformation, where eligible -> EOM -> Builder -> Solver
```

| Stage | Entry point or module | What it does |
| --- | --- | --- |
| Grammar | `GR_grammar_masker_v3.2.py` | Constructs covariant operators and dimension-balanced candidate Lagrangians. |
| Scalaron | `eom_v5_2/scalaron.py` | Rewrites eligible nonlinear algebraic sectors in R using an auxiliary scalar before the derivative-order test. This stage is automatic. |
| EOM | `EOM v5.2.py` | Varies the FLRW minisuperspace action and imposes relations that remove the identified higher time derivatives. |
| Builder | `Builder v5.2.py` | Converts the retained equations into numerical background systems and build caches. |
| Solver | `Solver v5.2.py` | Samples parameters, solves the initial constraint, integrates the background, checks admissibility, and evaluates the likelihood. |
| Search | `ai_theory_lab/graph_agent_batch.py` | Coordinates candidate selection, staged parameter scans, and feedback from the current run. |

The version numbers in the four launcher filenames are retained for compatibility
with existing scripts. The release branch is **v5.6**.

For a manually configured batch, run the four launchers in order:

```bash
python "GR_grammar_masker_v3.2.py"
python "EOM v5.2.py"
python "Builder v5.2.py"
python "Solver v5.2.py"
```

Each launcher has a `RUN_SETTINGS` block; environment variables override those
settings. Review the batch size before starting: the default grammar command
creates a batch, not a single example. The stages write `lagrangians.pkl`,
`eom_results/`, and `solver_result/`. For one candidate, the harness performs
these steps in an isolated run directory:

```bash
python -m ai_theory_lab.harness \
  --proposal ai_theory_lab/proposal_example.json \
  --agent-run-dir output/example_replay --pretty
```

The supplied example contains a previously selected parameter vector and is
an installation/replay check, **not a cold-start discovery experiment**. The
command constructs the candidate dictionary if no grammar cache is available;
this symbolic preparation can be slow. Batch searches save a
reusable grammar-only cache.

Passing the background derivative-order and numerical checks does not establish
full perturbative stability. In particular, positive scalar and tensor kinetic
and gradient coefficients require additional checks.

## Likelihood and ranking

The included likelihood uses 1820 SN entries and 13 BAO entries, retaining the
full covariance within each dataset. The SN magnitude offset and BAO distance
scale are profiled. There is no CMB likelihood or model-specific early-universe
sound-horizon calculation. See [data/README.md](data/README.md) for the inputs.

Within a fixed Lagrangian, parameter samples are ranked by total chi-square.
Across structures, the search uses AIC, `chi2 + 2*k`, with the nominal parameter
count after symbolic reductions, including the two profiled nuisance parameters.
BIC is also recorded but does not guide the search. AIC improvements from a
finite search are not assigned a global significance.

The optional background-Jacobian audit is disabled by default. Setting
`SOLVER_IDENTIFIABILITY_MODE=report` writes diagnostic parameter counts while
leaving the nominal AIC/BIC ranking unchanged. A small numerical Jacobian
response alone does not prove an exact redundant parameter.

## LLM-guided search

Set the provider credential in your shell, then select the provider and model
explicitly. For example, after setting `OPENAI_API_KEY`:

```bash
python -m ai_theory_lab.graph_agent_batch \
  --run-name real_openai_1000 \
  --waves 42 --batch-size 24 --target-attempts 1000 \
  --initial-parameter-samples 1000 \
  --expanded-parameter-samples 3000 --expanded-chi2-threshold 2000 \
  --refine-parameter-samples 5000 --refine-chi2-threshold 1638 \
  --group-mode open_only --scheduler async_slots \
  --n-workers 8 --slot-count 8 --slot-workers 1 \
  --diversity-strength 0.0 --timeout-setup 1200 --seed 20260607 \
  --proposal-mode llm --llm-provider openai --llm-model gpt-5.6-sol \
  --llm-api-key-env OPENAI_API_KEY --llm-fallback skip --pretty
```

A parent proposal receives 1000 initial parameter samples. An accepted fit
below `chi2=2000` triggers a further 3000-sample scan; an expanded fit below
`chi2=1638` triggers a further 5000 samples. Earlier symbolic or numerical
failure may stop an evaluation before its allocation is exhausted. Expanded
and refined scans do not count as new parents.

Use a new run name for each experiment. Cold-start runs begin without earlier
search results or fitted parameter vectors. They may reuse the grammar-only
cache. Current-run feedback updates external proposal priors and parameter
memory; LLM weights are fixed. `--llm-fallback skip` prevents a failed API
selection from being silently replaced by a deterministic choice attributed
to that model.

Supported interfaces are `openai`, `anthropic`, and `openai_compatible`.
The latter also requires `--llm-base-url`; use `--llm-api-key-env` to name its
credential variable. API access to the historical model identifiers depends on
the provider. Changing the model produces a new experiment.

The batch runner's `--proposal-mode deterministic` uses an adaptive heuristic.
It is **not** the fixed-prior random control described below.

## Supplementary experiments

[reproduction/README.md](reproduction/README.md) gives complete commands for:

- the flat CPL fit to the same observed-data likelihood;
- 1000 fixed-prior random proposals;
- separate 250-parent LLM runs with and without current-run memory;
- one flat-LambdaCDM mock realization and a 250-parent search;
- 20 independent DE restarts for each of seven fixed Lagrangians.

The search controls use private source snapshots, data copies, and output
directories. Preparing a search does not launch it. Mock data and results carry
explicit labels and use a separately refitted mock reference.

The original eight-agent benchmark preceded the scalaron extension. **v5.6
includes that extension**, as do the supplementary searches. The commands here
rerun the documented protocols with the released implementation; they do not
claim bitwise reproduction of the historical benchmark. An immutable source
snapshot for the original LLM runs was not retained, and asynchronous scheduling
and remote model responses can also change the search trajectory. The one-mock
pilot does not calibrate the look-elsewhere effect of the full benchmark.

## Files written by a search

| Location | Contents |
| --- | --- |
| `ai_theory_lab/proposals/<run>/` | Candidate specifications and explicit parameter samples. |
| `ai_theory_lab/runs/<run>.../` | Per-evaluation EOM, Builder and Solver artifacts, plus validation feedback. |
| `ai_theory_lab/memory/<run>/attempt_history.jsonl` | Recorded outcomes, fit statistics, stages and failure diagnostics. |
| `ai_theory_lab/memory/<run>/` | Current-run structural, marginal and joint parameter priors; summaries and reflections. |
| `ai_theory_lab/reports/<run>/` | Human-readable summaries and accepted-theory reports. |

The supplementary runner places all of these under its own `workspace/`.
Large outputs are ignored by Git but remain available locally. Record the
source revision, environment, model identifier, seeds, and run configuration
with any new result. Keep raw logs and parameter-sample records when comparing
searches; equal parent counts need not imply equal numerical work.

To summarize completed runs in the same workspace:

```bash
python -m ai_theory_lab.compare_benchmarks \
  --runs 'real_*' --output-dir output/benchmark_summary
```

This writes CSV comparison tables and a JSON provenance summary. Do not combine
real-data and mock runs in the same comparison.

## Tests and source layout

```bash
python -m unittest discover -s tests
```

Tests cover symbolic scalaron eligibility, parameter counting, scheduling,
likelihood conventions, mock covariance handling, and the control interventions.
They do not launch a production search or call a model provider.

- `gr_grammar_masker_v3_2/`: tensor contractions and covariant grammar.
- `eom_v5_2/`: symbolic variations, scalaron transformation and order filtering.
- `builder_v5_2/`: conversion to numerical background equations.
- `solver_v5_2/`: integration, validation, likelihoods and fit reports.
- `ai_theory_lab/`: orchestration, proposals, current-run memory and analysis.
- `reproduction/`: portable supplementary-search launcher and fixed DE inputs.
- `tests/`: numerical, symbolic and bookkeeping regression checks.

Stage-specific `AGENT.md` files and `ai_theory_lab/proposal_schema.md` document
the lower-level interfaces. `AGENTS.md` contains development instructions.
