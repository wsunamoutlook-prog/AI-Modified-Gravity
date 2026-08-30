#!/usr/bin/env python3
"""Summarize provider-reported token usage for initial theory proposals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def token_count(usage: dict) -> tuple[int, int, int, int]:
    input_tokens = int(usage.get("input_tokens", usage.get("prompt_tokens", 0)) or 0)
    output_tokens = int(usage.get("output_tokens", usage.get("completion_tokens", 0)) or 0)
    cache_creation = int(usage.get("cache_creation_input_tokens", 0) or 0)
    cache_read = int(usage.get("cache_read_input_tokens", 0) or 0)
    total = usage.get("total_tokens")
    if total is None:
        total = input_tokens + output_tokens + cache_creation + cache_read
    return input_tokens, output_tokens, cache_creation + cache_read, int(total)


def summarize_run(proposal_root: Path, run: str) -> dict:
    run_dir = proposal_root / run
    if not run_dir.is_dir():
        raise FileNotFoundError(f"proposal directory not found: {run_dir}")

    files = sorted(
        path
        for path in run_dir.glob("task_*.json")
        if "_expanded" not in path.stem and "_refine" not in path.stem
    )
    totals = {"input": 0, "output": 0, "cache": 0, "all": 0}
    usage_records = 0
    missing_usage: list[str] = []

    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        usage = data.get("llm_usage")
        if not isinstance(usage, dict):
            missing_usage.append(path.name)
            continue
        input_tokens, output_tokens, cache_tokens, total_tokens = token_count(usage)
        totals["input"] += input_tokens
        totals["output"] += output_tokens
        totals["cache"] += cache_tokens
        totals["all"] += total_tokens
        usage_records += 1

    if usage_records == 0:
        raise RuntimeError(f"no llm_usage records found for {run}")

    return {
        "run": run,
        "initial_proposal_files": len(files),
        "usage_records": usage_records,
        "missing_usage_records": len(missing_usage),
        "input_tokens": totals["input"],
        "output_tokens": totals["output"],
        "cache_tokens": totals["cache"],
        "total_tokens": totals["all"],
        "mean_total_tokens_per_initial_theory": round(totals["all"] / usage_records),
        "mean_denominator": "initial proposals with provider-reported usage",
        "missing_usage_files": missing_usage,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal-root", type=Path, default=Path("ai_theory_lab/proposals"))
    parser.add_argument("--runs", nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = {
        "metric": "provider-reported input + output + cache tokens",
        "runs": {
            run: summarize_run(args.proposal_root, run)
            for run in args.runs
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    for run, row in result["runs"].items():
        print(
            f"{run}: mean={row['mean_total_tokens_per_initial_theory']} "
            f"usage={row['usage_records']}/{row['initial_proposal_files']}"
        )


if __name__ == "__main__":
    main()
