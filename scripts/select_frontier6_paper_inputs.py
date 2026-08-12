#!/usr/bin/env python3
"""Select the compact set of Frontier-6 task artifacts needed for the paper."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Callable


RUNS = (
    "cmp1000_openai_gpt_5_6_sol_frontier6_openonly_aic_v2_8cpu",
    "cmp1000_claude_sonnet_5_frontier6_openonly_aic_v3_apifix",
    "cmp1000_gemini_3_6_flash_frontier6_openonly_aic_v3_apifix",
    "cmp1000_qwen3_7_max_frontier6_openonly_aic_v2_8cpu",
    "cmp1000_deepseek_ali_v4_pro_frontier6_openonly_aic_v3_apifix",
    "cmp1000_kimi_k3_frontier6_openonly_aic_v3_apifix",
)


def _minimum(
    rows: list[dict[str, str]],
    key: str,
    predicate: Callable[[dict[str, str]], bool] | None = None,
) -> dict[str, str] | None:
    candidates = [row for row in rows if row.get(key)]
    if predicate is not None:
        candidates = [row for row in candidates if predicate(row)]
    if not candidates:
        return None
    return min(candidates, key=lambda row: float(row[key]))


def _task_directory(row: dict[str, str]) -> Path:
    solver_dir = Path(row["solver_output_dir"])
    if solver_dir.name != "agent_solve":
        raise ValueError(f"Unexpected solver directory: {solver_dir}")
    return solver_dir.parents[1]


def select(report_root: Path) -> list[dict[str, Any]]:
    selected: dict[tuple[str, str], dict[str, Any]] = {}
    selectors = (
        ("best_aic", "aic", None),
        ("best_chi2", "chi2", None),
        (
            "best_active_correction",
            "aic",
            lambda row: row.get("effective_correction_status") in {"active", "moderate"},
        ),
        (
            "best_eh_baseline",
            "aic",
            lambda row: row.get("effective_correction_status") == "eh_only",
        ),
    )

    for run in RUNS:
        report_csv = report_root / run / "accepted_lagrangians_and_parameters.csv"
        if not report_csv.is_file():
            raise FileNotFoundError(report_csv)
        with report_csv.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        for reason, metric, predicate in selectors:
            row = _minimum(rows, metric, predicate)
            if row is None:
                continue
            key = (run, row["loop_id"])
            item = selected.setdefault(
                key,
                {
                    "run": run,
                    "loop_id": row["loop_id"],
                    "task_dir": str(_task_directory(row)),
                    "task_number": row["loop_id"].split("_lag_", 1)[0].split("_", 2)[:2],
                    "chi2": float(row["chi2"]),
                    "aic": float(row["aic"]),
                    "bic": float(row["bic"]),
                    "k_params": int(float(row["k_params"])),
                    "k_parameter_names": row.get("k_parameter_names", ""),
                    "delta_aic_vs_lcdm": float(row["delta_aic_vs_lcdm"]),
                    "effective_correction_status": row.get(
                        "effective_correction_status", ""
                    ),
                    "max_relative_effect_to_EH": row.get(
                        "max_relative_effect_to_EH", ""
                    ),
                    "solution_csv": row.get("solution_csv", ""),
                    "selection_reasons": [],
                },
            )
            item["selection_reasons"].append(reason)

    for item in selected.values():
        task_bits = item.pop("task_number")
        item["task_number"] = "_".join(task_bits)
        item["selection_reasons"].sort()
    return sorted(selected.values(), key=lambda item: (item["run"], item["aic"]))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    columns = (
        "run",
        "loop_id",
        "selection_reasons",
        "chi2",
        "aic",
        "bic",
        "k_params",
        "k_parameter_names",
        "delta_aic_vs_lcdm",
        "effective_correction_status",
        "max_relative_effect_to_EH",
        "task_dir",
        "solution_csv",
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            output = dict(row)
            output["selection_reasons"] = ";".join(row["selection_reasons"])
            writer.writerow({column: output.get(column, "") for column in columns})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report-root",
        type=Path,
        default=Path("ai_theory_lab/reports"),
    )
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    args = parser.parse_args()

    rows = select(args.report_root)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps({"runs": list(RUNS), "selected_tasks": rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    write_csv(args.output_csv, rows)
    print(f"Selected {len(rows)} unique task directories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
