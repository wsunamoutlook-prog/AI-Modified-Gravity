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
    model_env: str = ""


FRONTIER6_RUNS = [
    ModelRun(
        tag="openai",
        run_slug="openai_gpt_5_6_sol",
        provider="openai",
        model="gpt-5.6-sol",
        key_env="OPENAI_API_KEY",
    ),
    ModelRun(
        tag="claude",
        run_slug="claude_sonnet_5",
        provider="anthropic",
        model="claude-sonnet-5",
        key_env="ANTHROPIC_API_KEY",
    ),
    ModelRun(
        tag="gemini",
        run_slug="gemini_3_6_flash",
        provider="openai_compatible",
        model="gemini-3.6-flash",
        key_env="GEMINI_API_KEY",
        base_url_expr="$GEMINI_BASE_URL",
    ),
    ModelRun(
        tag="qwen",
        run_slug="qwen3_7_max",
        provider="openai_compatible",
        model="qwen3.7-max",
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
    ModelRun(
        tag="kimi",
        run_slug="kimi_k3",
        provider="openai_compatible",
        model="kimi-k3",
        model_env="KIMI_MODEL",
        key_env="MOONSHOT_API_KEY",
        base_url_expr="https://api.moonshot.ai/v1",
    ),
]


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
    "frontier6": FRONTIER6_RUNS,
    "cheap5": CHEAP5_RUNS,
    "expensive3": EXPENSIVE3_RUNS,
}

DEFAULT_RUN_LABEL = {
    "frontier6": "openonly_aic_v1",
    "cheap5": "cheap_v1",
    "expensive3": "expensive_v1",
}


def _simple_env_name(expr: str) -> str:
    if not expr.startswith("$"):
        return ""
    name = expr[1:]
    return name if name.isidentifier() else ""


def _required_env_lines(run: ModelRun) -> str:
    names = [run.key_env]
    base_url_env = _simple_env_name(run.base_url_expr)
    if base_url_env:
        names.append(base_url_env)
    return "\n".join(
        f': "${{{name}:?{name} is required for {run.tag}}}"'
        for name in names
    )


def _model_cli_value(run: ModelRun) -> str:
    if run.model_env:
        return f'"${{{run.model_env}:-{run.model}}}"'
    return run.model


def _slurm_text(
    run: ModelRun,
    *,
    run_name: str,
    attempts: int,
    cpus: int,
    mem: str,
    time_limit: str,
    run_label: str,
    group_mode: str,
    llm_fallback: str = "skip",
    resume: bool = False,
) -> str:
    waves = (attempts + 23) // 24
    base_url_line = ""
    if run.base_url_expr:
        base_url_line = f'  --llm-base-url "{run.base_url_expr}" \\\n'
    required_env_lines = _required_env_lines(run)
    model_cli_value = _model_cli_value(run)
    log_label = run_label.replace("_", "-")
    resume_line = "  --resume \\\n" if resume else ""
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

set -euo pipefail

cd ~/Modify_GR
source .venv/bin/activate
source ~/.openai_env

{required_env_lines}

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
  --n-workers "$SLURM_CPUS_PER_TASK" \\
  --run-name {run_name} \\
  --proposal-mode llm \\
  --llm-provider {run.provider} \\
  --llm-model {model_cli_value} \\
{base_url_line}  --llm-api-key-env {run.key_env} \\
  --llm-fallback {llm_fallback} \\
  --group-mode {group_mode} \\
  --scheduler async_slots \\
  --slot-count "$SLURM_CPUS_PER_TASK" \\
  --slot-workers 1 \\
  --diversity-strength 0.0 \\
{resume_line}\
  --timeout-setup 1200 \\
  --pretty
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Write and optionally submit multi-API comparison SLURM jobs.")
    parser.add_argument(
        "--preset",
        choices=sorted(RUN_PRESETS),
        default="frontier6",
        help=(
            "Model set to submit. frontier6 is the current production comparison; "
            "cheap5 and expensive3 are retained for historical reproduction."
        ),
    )
    parser.add_argument(
        "--run-label",
        default="",
        help="Suffix for run names and log files. Defaults to the selected preset's versioned label.",
    )
    parser.add_argument("--attempts", type=int, default=600)
    parser.add_argument("--cpus", type=int, default=8)
    parser.add_argument("--mem", default="32G")
    parser.add_argument("--time", default="72:00:00")
    parser.add_argument(
        "--group-mode",
        choices=("open_only", "sector_split", "track_split", "mixed"),
        default="open_only",
        help="Theory allocation for generated jobs. The default spends all initial attempts on unrestricted open search.",
    )
    parser.add_argument(
        "--llm-fallback",
        choices=("skip", "fail", "deterministic"),
        default="skip",
        help=(
            "Behavior after all LLM retries fail. Production comparisons default to skip "
            "so deterministic proposals cannot be attributed to an API model."
        ),
    )
    parser.add_argument(
        "--tags",
        nargs="+",
        default=[],
        help="Optional subset of preset tags to write/submit, for example: claude gemini deepseek kimi.",
    )
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--force", action="store_true", help="Overwrite existing SLURM files.")
    parser.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Resume existing async_slots run directories in place. The generated jobs "
            "recount completed initial attempts and continue to --attempts."
        ),
    )
    parser.add_argument(
        "--allow-existing-runs",
        action="store_true",
        help="Allow submission even if memory/proposals directories already exist.",
    )
    args = parser.parse_args()

    runs = RUN_PRESETS[args.preset]
    if args.tags:
        requested_tags = set(args.tags)
        known_tags = {run.tag for run in runs}
        unknown_tags = sorted(requested_tags - known_tags)
        if unknown_tags:
            raise SystemExit(f"Unknown tags for {args.preset}: {', '.join(unknown_tags)}")
        runs = [run for run in runs if run.tag in requested_tags]
    run_label = args.run_label or DEFAULT_RUN_LABEL[args.preset]

    out_paths: list[Path] = []
    for run in runs:
        run_name = f"cmp{args.attempts}_{run.run_slug}_{run_label}"
        if args.resume:
            missing = [
                path
                for path in (
                    Path("ai_theory_lab") / "memory" / run_name,
                    Path("ai_theory_lab") / "proposals" / run_name,
                )
                if not path.is_dir()
            ]
            if missing:
                joined = ", ".join(str(path) for path in missing)
                raise SystemExit(f"{run_name} cannot resume; missing artifacts: {joined}")
        elif not args.allow_existing_runs:
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
                group_mode=args.group_mode,
                llm_fallback=args.llm_fallback,
                resume=args.resume,
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
