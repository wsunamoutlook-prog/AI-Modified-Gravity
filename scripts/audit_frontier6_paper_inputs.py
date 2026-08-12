#!/usr/bin/env python3
"""Audit the compact Frontier-6 paper-input package."""

from __future__ import annotations

import argparse
import csv
import json
import math
import pickle
from pathlib import Path
from typing import Any


REQUIRED_TASK_FILES = (
    "agent_lagrangians.pkl",
    "agent_eom_results/eom_results.pkl",
    "agent_eom_results/eom_summary.txt",
    "agent_builder_result/agent_build/build_cache_report.txt",
    "agent_builder_result/agent_build/build_models_summary.csv",
    "agent_solver_result/agent_solve/model_ranking.csv",
    "agent_solver_result/agent_solve/accepted_samples_summary.csv",
    "agent_solver_result/agent_solve/all_samples_summary.csv",
    "agent_solver_result/agent_solve/scan_report.txt",
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _close(left: float, right: float, tolerance: float = 1e-6) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)


def audit(root: Path) -> dict[str, Any]:
    manifest_path = root / "selection_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    selected = manifest["selected_tasks"]
    errors: list[str] = []
    warnings: list[str] = []
    task_audits: list[dict[str, Any]] = []

    run_names = set(manifest["runs"])
    selected_runs = {item["run"] for item in selected}
    if selected_runs != run_names:
        errors.append(
            f"Selected runs differ from manifest runs: {selected_runs ^ run_names}"
        )

    comparison_path = root / "reports/frontier6_openonly_aic_final/comparison_summary.json"
    comparison = json.loads(comparison_path.read_text(encoding="utf-8"))
    comparison_rows = comparison.get("runs", [])
    comparison_runs = (
        set(comparison_rows)
        if all(isinstance(row, str) for row in comparison_rows)
        else {row["run_name"] for row in comparison_rows}
    )
    if comparison_runs != run_names:
        errors.append(
            f"Comparison runs differ from manifest runs: {comparison_runs ^ run_names}"
        )

    for item in selected:
        run = item["run"]
        loop_id = item["loop_id"]
        task_name = Path(item["task_dir"]).name
        task_dir = root / "selected_tasks" / run / task_name
        task_errors: list[str] = []
        task_warnings: list[str] = []

        for relative in REQUIRED_TASK_FILES:
            path = task_dir / relative
            if not path.is_file() or path.stat().st_size == 0:
                task_errors.append(f"missing or empty: {relative}")

        solutions = sorted(
            (task_dir / "agent_solver_result/agent_solve").glob(
                "top_*_solution.csv"
            )
        )
        if not solutions:
            task_errors.append("missing H(z) solution CSV")

        proposal = root / "selected_proposals" / run / f"{loop_id}.json"
        if not proposal.is_file() or proposal.stat().st_size == 0:
            task_errors.append(f"missing exact proposal JSON: {proposal.name}")

        if not task_errors:
            with (task_dir / "agent_lagrangians.pkl").open("rb") as handle:
                lagrangians = pickle.load(handle)
            if not lagrangians:
                task_errors.append("agent_lagrangians.pkl is empty")

            eom_text = (
                task_dir / "agent_eom_results/eom_summary.txt"
            ).read_text(encoding="utf-8")
            if "Ghost-free: YES" not in eom_text:
                task_errors.append("EOM summary does not contain Ghost-free: YES")

            builder_rows = _read_csv(
                task_dir
                / "agent_builder_result/agent_build/build_models_summary.csv"
            )
            if not builder_rows or builder_rows[0].get("usable") != "True":
                task_errors.append("Builder summary is not usable")

            ranking_rows = _read_csv(
                task_dir / "agent_solver_result/agent_solve/model_ranking.csv"
            )
            successful = [
                row
                for row in ranking_rows
                if row.get("success") == "True" and row.get("chi2")
            ]
            if not successful:
                task_errors.append("model_ranking.csv has no successful row")
            else:
                best = min(successful, key=lambda row: float(row["AIC"]))
                checks = (
                    ("chi2", float(best["chi2"]), float(item["chi2"])),
                    ("AIC", float(best["AIC"]), float(item["aic"])),
                    ("BIC", float(best["BIC"]), float(item["bic"])),
                    ("k_params", float(best["k_params"]), float(item["k_params"])),
                )
                for label, actual, expected in checks:
                    if not _close(actual, expected):
                        task_errors.append(
                            f"{label} mismatch: solver={actual}, manifest={expected}"
                        )

            accepted_rows = _read_csv(
                task_dir
                / "agent_solver_result/agent_solve/accepted_samples_summary.csv"
            )
            all_rows = _read_csv(
                task_dir / "agent_solver_result/agent_solve/all_samples_summary.csv"
            )
            if not accepted_rows:
                task_errors.append("accepted_samples_summary.csv has no rows")
            if not all_rows:
                task_errors.append("all_samples_summary.csv has no rows")

            solution_rows = _read_csv(solutions[0])
            required_columns = {
                "z",
                "h_dimensionless",
                "H_km_s_Mpc",
                "constraint_residual",
            }
            if not solution_rows:
                task_errors.append("H(z) solution CSV has no rows")
            elif not required_columns.issubset(solution_rows[0]):
                task_errors.append("H(z) solution CSV lacks required columns")
            else:
                values = [
                    (
                        float(row["z"]),
                        float(row["h_dimensionless"]),
                        float(row["H_km_s_Mpc"]),
                        float(row["constraint_residual"]),
                    )
                    for row in solution_rows
                ]
                if not all(math.isfinite(value) for row in values for value in row):
                    task_errors.append("H(z) solution contains non-finite values")
                z_values = [row[0] for row in values]
                h_values = [row[1] for row in values]
                residuals = [abs(row[3]) for row in values]
                if min(z_values) > 1e-9 or max(z_values) < 2.0:
                    task_errors.append(
                        f"H(z) redshift coverage is incomplete: "
                        f"{min(z_values)}..{max(z_values)}"
                    )
                if min(h_values) <= 0:
                    task_errors.append("H(z) solution is not everywhere positive")
                max_residual = max(residuals)
                if max_residual > 1e-4:
                    task_warnings.append(
                        f"large plotted constraint residual: {max_residual:.3e}"
                    )
        else:
            accepted_rows = []
            all_rows = []
            solution_rows = []

        report_csv = root / "reports" / run / "accepted_lagrangians_and_parameters.csv"
        report_rows = _read_csv(report_csv)
        report_matches = [row for row in report_rows if row.get("loop_id") == loop_id]
        if len(report_matches) != 1:
            task_errors.append(
                f"expected one matching report row, found {len(report_matches)}"
            )

        task_audits.append(
            {
                "run": run,
                "loop_id": loop_id,
                "selection_reasons": item["selection_reasons"],
                "accepted_sample_rows": len(accepted_rows),
                "all_sample_rows": len(all_rows),
                "solution_rows": len(solution_rows),
                "errors": task_errors,
                "warnings": task_warnings,
            }
        )
        errors.extend(f"{run}/{loop_id}: {message}" for message in task_errors)
        warnings.extend(f"{run}/{loop_id}: {message}" for message in task_warnings)

    package_root = root.parent
    archive_root = package_root
    scheduler_root = (
        archive_root
        / "ai_theory_lab"
        / "proposals"
    )
    memory_root = archive_root / "ai_theory_lab" / "memory"
    run_completion: list[dict[str, Any]] = []
    for run in sorted(run_names):
        scheduler_path = scheduler_root / run / "scheduler_tasks.jsonl"
        history_path = memory_root / run / "attempt_history.jsonl"
        if not scheduler_path.is_file():
            errors.append(f"missing scheduler log for {run}")
            continue
        if not history_path.is_file():
            errors.append(f"missing attempt history for {run}")
            continue

        events = [
            json.loads(line)
            for line in scheduler_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        last = events[-1]
        initial_complete = (
            int(last.get("recorded_total", 0)) == 1000
            and int(last.get("target_attempts", 0)) == 1000
        )
        if not initial_complete:
            errors.append(
                f"{run} initial schedule incomplete: "
                f"{last.get('recorded_total')}/{last.get('target_attempts')}"
            )

        expanded_recorded = int(last.get("expanded_recorded_total", 0) or 0)
        expanded_submitted = int(last.get("expanded_submitted_total", 0) or 0)
        if expanded_recorded != expanded_submitted:
            warnings.append(
                f"{run} has an unmatched expanded bookkeeping record: "
                f"{expanded_recorded}/{expanded_submitted}"
            )

        run_completion.append(
            {
                "run": run,
                "last_event": last.get("event"),
                "initial_recorded": last.get("recorded_total"),
                "initial_target": last.get("target_attempts"),
                "expanded_recorded": expanded_recorded,
                "expanded_submitted": expanded_submitted,
                "refine_recorded": last.get("refine_recorded_total"),
                "refine_submitted": last.get("refine_submitted_total"),
                "initial_complete": initial_complete,
            }
        )

    return {
        "status": "ok" if not errors else "error",
        "selected_task_count": len(selected),
        "run_count": len(run_names),
        "errors": errors,
        "warnings": warnings,
        "run_completion": run_completion,
        "tasks": task_audits,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = audit(args.root)
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
