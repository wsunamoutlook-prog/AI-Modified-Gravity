"""Generate and submit final multi-API comparison SLURM jobs.

This helper avoids copy/pasting long cluster commands. It writes one SLURM file
per model and optionally submits them with sbatch.
"""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelRun:
    tag: str
    run_slug: str
    provider: str
    model: str
    key_env: str
    base_url_expr: str = ""


CHEAP5_RUNS = [
    ModelRun(
        tag="openai",
        run_slug="openai_gpt_5_4_mini",
        provider="openai",
        model="gpt-5.4-mini",
        key_env="OPENAI_API_KEY",
    ),
    ModelRun(
        tag="claude",
        run_slug="claude_sonnet_4_6",
        provider="anthropic",
        model="claude-sonnet-4-6",
        key_env="ANTHROPIC_API_KEY",
    ),
    ModelRun(
        tag="gemini",
        run_slug="gemini_3_5_flash",
        provider="openai_compatible",
        model="gemini-3.5-flash",
        key_env="GEMINI_API_KEY",
        base_url_expr="$GEMINI_BASE_URL",
    ),
    ModelRun(
        tag="qwen",
        run_slug="qwen3_7_plus",
        provider="openai_compatible",
        model="qwen3.7-plus",
        key_env="DASHSCOPE_API_KEY",
        base_url_expr="$QWEN_BASE_URL",
    ),
    ModelRun(
        tag="deepseek",
        run_slug="deepseek_ali_v4_pro",
        provider="openai_compatible",
        model="deepseek-v4-pro",
        key_env="DASHSCOPE_API_KEY",
        base_url_expr="$QWEN_BASE_URL",
    ),
]

EXPENSIVE3_RUNS = [
    ModelRun(
        tag="openai",
        run_slug="openai_gpt_5_5",
        provider="openai",
        model="gpt-5.5",
        key_env="OPENAI_API_KEY",
    ),
    ModelRun(
        tag="claude",
        run_slug="claude_opus_4_8",
        provider="anthropic",
        model="claude-opus-4-8",
        key_env="ANTHROPIC_API_KEY",
    ),
    ModelRun(
        tag="gemini",
        run_slug="gemini_3_1_pro",
        provider="openai_compatible",
        model="gemini-3.1-pro-preview",
        key_env="GEMINI_API_KEY",
        base_url_expr="$GEMINI_BASE_URL",
    ),
]

RUN_PRESETS = {
    "cheap5": CHEAP5_RUNS,
    "expensive3": EXPENSIVE3_RUNS,
}

DEFAULT_RUN_LABEL = {
    "cheap5": "cheap_v1",
    "expensive3": "expensive_v1",
}


def _slurm_text(
    run: ModelRun,
    *,
    run_name: str,
    attempts: int,
    cpus: int,
    mem: str,
    time_limit: str,
    run_label: str,
) -> str:
    waves = (attempts + 23) // 24
    base_url_line = ""
    if run.base_url_expr:
        base_url_line = f'  --llm-base-url "{run.base_url_expr}" \\\n'
    log_label = run_label.replace("_", "-")
    return f"""#!/bin/bash
#SBATCH --job-name=mg-{run.tag}{attempts}
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={cpus}
#SBATCH --mem={mem}
#SBATCH --time={time_limit}
#SBATCH --output=log/slurm/mg-{run.tag}{attempts}-{log_label}-%j.out
#SBATCH --error=log/slurm/mg-{run.tag}{attempts}-{log_label}-%j.err
#SBATCH --export=ALL

cd ~/Modify_GR
source .venv/bin/activate
source ~/.openai_env

mkdir -p log/slurm .matplotlib-cache

export PYTHONUNBUFFERED=1
export MPLCONFIGDIR="$PWD/.matplotlib-cache"
export AGENT_MIN_OPERATOR_TERMS=1
export AGENT_MAX_OPERATOR_TERMS=8
export AGENT_OPERATOR_COUNT_FIXED_PROB=0.05
export SOLVER_PARALLEL=1
export N_WORKERS=$SLURM_CPUS_PER_TASK

python -m ai_theory_lab.graph_agent_batch \\
  --waves {waves} \\
  --batch-size 24 \\
  --target-attempts {attempts} \\
  --initial-parameter-samples 1000 \\
  --expanded-parameter-samples 3000 \\
  --expanded-chi2-threshold 2000 \\
  --refine-parameter-samples 5000 \\
  --refine-chi2-threshold 1638 \\
  --non-eh-refine-parameter-samples 10000 \\
  --non-eh-refine-chi2-threshold 2000 \\
  --n-workers "$SLURM_CPUS_PER_TASK" \\
  --run-name {run_name} \\
  --proposal-mode llm \\
  --llm-provider {run.provider} \\
  --llm-model {run.model} \\
{base_url_line}  --llm-api-key-env {run.key_env} \\
  --llm-fallback deterministic \\
  --group-mode sector_split \\
  --scheduler async_slots \\
  --slot-count "$SLURM_CPUS_PER_TASK" \\
  --slot-workers 1 \\
  --diversity-strength 0.0 \\
  --timeout-setup 1200 \\
  --pretty
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Write and optionally submit multi-API comparison SLURM jobs.")
    parser.add_argument(
        "--preset",
        choices=sorted(RUN_PRESETS),
        default="cheap5",
        help="Model set to submit. expensive3 is GPT-5.5, Claude Opus 4.8, and Gemini 3.1 Pro.",
    )
    parser.add_argument(
        "--run-label",
        default="",
        help="Suffix for run names and log files. Defaults to cheap_v1 or expensive_v1 from the preset.",
    )
    parser.add_argument("--attempts", type=int, default=600)
    parser.add_argument("--cpus", type=int, default=8)
    parser.add_argument("--mem", default="32G")
    parser.add_argument("--time", default="72:00:00")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--force", action="store_true", help="Overwrite existing SLURM files.")
    parser.add_argument(
        "--allow-existing-runs",
        action="store_true",
        help="Allow submission even if memory/proposals directories already exist.",
    )
    args = parser.parse_args()

    runs = RUN_PRESETS[args.preset]
    run_label = args.run_label or DEFAULT_RUN_LABEL[args.preset]

    out_paths: list[Path] = []
    for run in runs:
        run_name = f"cmp{args.attempts}_{run.run_slug}_{run_label}"
        if not args.allow_existing_runs:
            conflicts = [
                path
                for path in (
                    Path("ai_theory_lab") / "memory" / run_name,
                    Path("ai_theory_lab") / "proposals" / run_name,
                )
                if path.exists()
            ]
            if conflicts:
                joined = ", ".join(str(path) for path in conflicts)
                raise SystemExit(f"{run_name} already has artifacts: {joined}")
        path = Path(f"run_{run_name}.slurm")
        if path.exists() and not args.force:
            raise SystemExit(f"{path} already exists; pass --force to overwrite.")
        path.write_text(
            _slurm_text(
                run,
                run_name=run_name,
                attempts=args.attempts,
                cpus=args.cpus,
                mem=args.mem,
                time_limit=args.time,
                run_label=run_label,
            ),
            encoding="utf-8",
        )
        out_paths.append(path)
        print(f"wrote {path}")

    if args.submit:
        for path in out_paths:
            result = subprocess.run(["sbatch", str(path)], check=True, text=True, capture_output=True)
            print(result.stdout.strip())
    else:
        print("dry run only; pass --submit to submit jobs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
