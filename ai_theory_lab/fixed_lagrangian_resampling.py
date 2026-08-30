"""Controlled fixed-Lagrangian parameter-search resampling on Oscar.

This module intentionally does not run an LLM or update agent memory.  It
holds each serialized Lagrangian and the broad parameter prior fixed, changes
only the random seed, and records the best result from each finite scan.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import pickle
import random
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

from .cold_start_runner import _entry_from_lagrangian, _parameter_samples
from .graph_agent_batch import _write_batch_lagrangians


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "ai_theory_lab" / "fixed7_resampling_manifest.json"
DEFAULT_OUTPUT_ROOT = ROOT / "ai_theory_lab" / "resampling" / "fixed7_aic_resampling_20x5000_v1"
BASE_SEED = 2026082800


def _read_json(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"Expected a JSON object: {path}")
    return data


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_revision() -> Dict[str, Any]:
    def run(*args: str) -> str:
        proc = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return proc.stdout.strip()

    return {
        "commit": run("rev-parse", "HEAD") or None,
        "branch": run("branch", "--show-current") or None,
        "dirty": bool(run("status", "--porcelain")),
    }


def _representatives(manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
    reps = manifest.get("representatives")
    if not isinstance(reps, list) or not reps:
        raise ValueError("Manifest must contain a non-empty representatives list")
    proposals = [str(rep.get("proposal") or "") for rep in reps]
    if any(not proposal for proposal in proposals) or len(set(proposals)) != len(proposals):
        raise ValueError("Representative proposal labels must be non-empty and unique")
    return reps


def _resolve_source_task(rep: Dict[str, Any], source_root: Path) -> Path:
    candidates = [source_root / str(rep["source_task_dir"])]
    local = Path(str(rep.get("local_source_task_dir") or ""))
    if str(local):
        candidates.append(local if local.is_absolute() else ROOT / local)
    for candidate in candidates:
        if (candidate / "agent_lagrangians.pkl").exists():
            return candidate.resolve()
    rendered = "\n  ".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(
        f"Could not find agent_lagrangians.pkl for {rep['proposal']}; checked:\n  {rendered}"
    )


def _load_single_lagrangian(path: Path) -> tuple[int, Dict[str, Any]]:
    with path.open("rb") as handle:
        payload = pickle.load(handle)
    if not isinstance(payload, dict):
        raise TypeError(f"Expected grouped Lagrangian dictionary in {path}")
    items: List[tuple[int, Dict[str, Any]]] = []
    for n_terms, group in payload.items():
        if not isinstance(group, list):
            continue
        items.extend((int(n_terms), lagrangian) for lagrangian in group)
    if len(items) != 1:
        raise ValueError(f"Expected exactly one serialized Lagrangian in {path}; found {len(items)}")
    return items[0]


def _iter_batch_lagrangians(path: Path) -> Iterable[tuple[str, int, Dict[str, Any]]]:
    with path.open("rb") as handle:
        payload = pickle.load(handle)
    lag_id = 0
    for n_terms in sorted(payload, key=int):
        for lagrangian in payload[n_terms]:
            lag_id += 1
            yield str(lag_id), int(n_terms), lagrangian


def _run_stage(name: str, command: Sequence[str], env: Dict[str, str], log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    with log_path.open("w", encoding="utf-8") as log:
        log.write(f"stage={name}\ncommand={' '.join(command)}\n")
        log.flush()
        proc = subprocess.run(
            list(command),
            cwd=ROOT,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
            check=False,
        )
        log.write(f"\nreturncode={proc.returncode}\nelapsed_seconds={time.time() - started:.3f}\n")
    if proc.returncode != 0:
        raise RuntimeError(f"{name} failed with return code {proc.returncode}; see {log_path}")


def check_sources(manifest_path: Path, source_root: Path) -> List[Dict[str, Any]]:
    manifest = _read_json(manifest_path)
    checked: List[Dict[str, Any]] = []
    for rep in _representatives(manifest):
        source = _resolve_source_task(rep, source_root)
        source_pkl = source / "agent_lagrangians.pkl"
        n_terms, lagrangian = _load_single_lagrangian(source_pkl)
        checked.append(
            {
                "agent": rep["agent"],
                "proposal": rep["proposal"],
                "source": str(source),
                "sha256": _sha256(source_pkl),
                "n_terms": n_terms,
                "scalar_config": lagrangian.get("scalar_config"),
                "potential_types": lagrangian.get("potential_types"),
            }
        )
    return checked


def prepare_experiment(
    manifest_path: Path,
    source_root: Path,
    output_root: Path,
    *,
    force: bool = False,
) -> Dict[str, Any]:
    manifest = _read_json(manifest_path)
    reps = _representatives(manifest)
    inputs = output_root / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    batch_pkl = inputs / "fixed7_agent_lagrangians.pkl"
    build_cache = inputs / "fixed7_built_models_cache.pkl"
    prepared_manifest_path = inputs / "prepared_manifest.json"

    entries: List[Dict[str, Any]] = []
    source_records: List[Dict[str, Any]] = []
    for rep in reps:
        source = _resolve_source_task(rep, source_root)
        source_pkl = source / "agent_lagrangians.pkl"
        n_terms, lagrangian = _load_single_lagrangian(source_pkl)
        entries.append(_entry_from_lagrangian(lagrangian, n_terms))
        source_records.append(
            {
                **rep,
                "resolved_source_task_dir": str(source),
                "source_lagrangians_path": str(source_pkl),
                "source_lagrangians_sha256": _sha256(source_pkl),
                "n_terms": n_terms,
                "scalar_config": lagrangian.get("scalar_config"),
                "potential_types": lagrangian.get("potential_types"),
            }
        )

    previous_batch_hash = None
    if prepared_manifest_path.exists():
        previous_batch_hash = _read_json(prepared_manifest_path).get("batch_lagrangians_sha256")
    # Rewriting is cheap and preserves the source-entry to batch-lag-id mapping.
    # The grouped pickle order differs from manifest order when n_terms differs.
    lag_ids = _write_batch_lagrangians(entries, batch_pkl)
    current_batch_hash = _sha256(batch_pkl)
    batch_changed = previous_batch_hash not in {None, current_batch_hash}

    for index, record in enumerate(source_records):
        record["batch_lag_id"] = str(lag_ids[index])

    prepared = {
        "experiment_id": manifest["experiment_id"],
        "created_at_unix": time.time(),
        "git": _git_revision(),
        "python": sys.version,
        "sampling_contract": manifest.get("sampling_contract"),
        "manifest_path": str(manifest_path.resolve()),
        "batch_lagrangians_path": str(batch_pkl.resolve()),
        "batch_lagrangians_sha256": current_batch_hash,
        "build_cache_path": str(build_cache.resolve()),
        "representatives": source_records,
    }
    _write_json(prepared_manifest_path, prepared)

    if force or batch_changed or not build_cache.exists():
        eom_dir = inputs / "eom_results"
        builder_dir = inputs / "builder_results"
        env = os.environ.copy()
        env.update(
            {
                "MPLCONFIGDIR": str(output_root / ".matplotlib-cache"),
                "EOM_LAGRANGIANS_PATH": str(batch_pkl),
                "EOM_OUTPUT_DIR": str(eom_dir),
                "EOM_MAX_TERMS": "all",
                "EOM_N_SAMPLES": "all",
                "EOM_RUN_SELF_TEST": "0",
            }
        )
        _run_stage("EOM", [sys.executable, "EOM v5.2.py"], env, inputs / "eom.log")
        env.update(
            {
                "EOM_SUMMARY_PATH": str(eom_dir / "eom_summary.txt"),
                "SOLVER_OUTPUT_DIR": str(builder_dir),
                "SOLVER_RUN_NAME": "fixed7_build",
                "BUILD_CACHE_PATH": str(build_cache),
                "MAX_MODELS_TO_BUILD": "0",
            }
        )
        _run_stage("Builder", [sys.executable, "Builder v5.2.py"], env, inputs / "builder.log")

    if not build_cache.exists():
        raise FileNotFoundError(f"Builder did not create {build_cache}")
    prepared["build_cache_sha256"] = _sha256(build_cache)
    prepared["prepared_at_unix"] = time.time()
    _write_json(prepared_manifest_path, prepared)
    print(prepared_manifest_path)
    return prepared


def _seed_for_replicate(replicate: int, base_seed: int = BASE_SEED) -> int:
    if replicate < 1:
        raise ValueError("replicate must be >= 1")
    return int(base_seed + replicate * 100_003)


def _samples_for_replicate(
    prepared: Dict[str, Any],
    replicate: int,
    sample_count: int,
) -> Dict[str, List[Dict[str, Any]]]:
    batch_pkl = Path(str(prepared["batch_lagrangians_path"]))
    labels_by_lag = {
        str(rep["batch_lag_id"]): str(rep["proposal"])
        for rep in prepared["representatives"]
    }
    out: Dict[str, List[Dict[str, Any]]] = {}
    replicate_seed = _seed_for_replicate(replicate)
    for lag_id, n_terms, lagrangian in _iter_batch_lagrangians(batch_pkl):
        if lag_id not in labels_by_lag:
            raise ValueError(f"Prepared manifest has no proposal mapping for batch lag_id={lag_id}")
        entry = _entry_from_lagrangian(lagrangian, n_terms)
        rng = random.Random(replicate_seed + int(lag_id) * 1_000_003)
        # Empty summary freezes the broad cold-start prior and prevents use of
        # current-loop structure or joint-parameter memory.
        out[lag_id] = _parameter_samples(entry, rng, sample_count, {})
    return out


def _read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def run_replicate(
    output_root: Path,
    replicate: int,
    *,
    sample_count: int = 5000,
    workers: int = 7,
    force: bool = False,
) -> Dict[str, Any]:
    prepared_path = output_root / "inputs" / "prepared_manifest.json"
    prepared = _read_json(prepared_path)
    expected_reps = int((prepared.get("sampling_contract") or {}).get("replicates", 20))
    if replicate < 1 or replicate > expected_reps:
        raise ValueError(f"replicate must be in 1..{expected_reps}")

    run_dir = output_root / "replicates" / f"replicate_{replicate:02d}"
    status_path = run_dir / "status.json"
    if status_path.exists() and not force:
        existing = _read_json(status_path)
        if existing.get("complete") is True:
            print(status_path)
            return existing

    run_dir.mkdir(parents=True, exist_ok=True)
    sample_path = run_dir / "parameter_samples_by_lag_id.json"
    samples_by_lag_id = _samples_for_replicate(prepared, replicate, sample_count)
    _write_json(sample_path, {"samples_by_lag_id": samples_by_lag_id})

    solver_base = run_dir / "solver"
    solver_run_name = "scan"
    solver_output = solver_base / solver_run_name
    env = os.environ.copy()
    env.update(
        {
            "BUILD_CACHE_PATH": str(prepared["build_cache_path"]),
            "SOLVER_OUTPUT_DIR": str(solver_base),
            "SOLVER_RUN_NAME": solver_run_name,
            "PARAMETER_SAMPLES_PATH": str(sample_path),
            "N_SAMPLES_PER_MODEL": str(sample_count),
            "RANDOM_SEED": str(_seed_for_replicate(replicate)),
            "SOLVER_PARALLEL": "1",
            "N_WORKERS": str(max(1, workers)),
            "MAX_MODELS_TO_BUILD": "0",
            "SOLVER_MAKE_PLOTS": "0",
            "TOP_N": "0",
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "MPLCONFIGDIR": str(output_root / ".matplotlib-cache"),
        }
    )
    started = time.time()
    error: str | None = None
    returncode = 0
    try:
        _run_stage(
            "Solver",
            [sys.executable, "Solver v5.2.py"],
            env,
            run_dir / "solver.log",
        )
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        returncode = 1

    all_rows = _read_csv(solver_output / "all_samples_summary.csv")
    counts: Dict[str, int] = {}
    for row in all_rows:
        lag_id = str(row.get("lag_id") or "")
        counts[lag_id] = counts.get(lag_id, 0) + 1
    expected_lag_ids = [str(rep["batch_lag_id"]) for rep in prepared["representatives"]]
    complete = returncode == 0 and all(counts.get(lag_id) == sample_count for lag_id in expected_lag_ids)
    status = {
        "replicate": replicate,
        "seed": _seed_for_replicate(replicate),
        "sample_count_per_lagrangian": sample_count,
        "workers": workers,
        "returncode": returncode,
        "error": error,
        "complete": complete,
        "evaluated_rows_by_lag_id": counts,
        "elapsed_seconds": time.time() - started,
        "solver_output_dir": str(solver_output.resolve()),
        "parameter_samples_path": str(sample_path.resolve()),
    }
    _write_json(status_path, status)
    print(status_path)
    if not complete:
        raise RuntimeError(f"Replicate {replicate} did not complete all expected samples: {status}")
    return status


def _finite_float(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _sample_sd(values: Sequence[float]) -> float:
    return statistics.stdev(values) if len(values) >= 2 else 0.0


def _write_csv(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def summarize_results(
    output_root: Path,
    *,
    expected_replicates: int = 20,
    allow_incomplete: bool = False,
) -> Dict[str, Any]:
    prepared = _read_json(output_root / "inputs" / "prepared_manifest.json")
    reps_by_lag = {
        str(rep["batch_lag_id"]): rep for rep in prepared["representatives"]
    }
    minima_rows: List[Dict[str, Any]] = []
    incomplete: List[int] = []
    for replicate in range(1, expected_replicates + 1):
        run_dir = output_root / "replicates" / f"replicate_{replicate:02d}"
        status_path = run_dir / "status.json"
        if not status_path.exists() or not _read_json(status_path).get("complete"):
            incomplete.append(replicate)
            continue
        status = _read_json(status_path)
        solver_dir = Path(str(status["solver_output_dir"]))
        ranking = _read_csv(solver_dir / "model_ranking.csv")
        best_by_lag: Dict[str, Dict[str, str]] = {}
        for row in ranking:
            lag_id = str(row.get("lag_id") or "")
            chi2 = _finite_float(row.get("chi2"))
            if lag_id and chi2 is not None:
                current = best_by_lag.get(lag_id)
                if current is None or chi2 < float(current["chi2"]):
                    best_by_lag[lag_id] = row
        all_rows = _read_csv(solver_dir / "all_samples_summary.csv")
        accepted_counts = {lag_id: 0 for lag_id in reps_by_lag}
        total_counts = {lag_id: 0 for lag_id in reps_by_lag}
        for row in all_rows:
            lag_id = str(row.get("lag_id") or "")
            if lag_id not in reps_by_lag:
                continue
            total_counts[lag_id] += 1
            if str(row.get("success") or "").lower() == "true" and _finite_float(row.get("chi2")) is not None:
                accepted_counts[lag_id] += 1
        for lag_id, rep in reps_by_lag.items():
            best = best_by_lag.get(lag_id)
            total = total_counts[lag_id]
            accepted = accepted_counts[lag_id]
            minima_rows.append(
                {
                    "agent": rep["agent"],
                    "proposal": rep["proposal"],
                    "batch_lag_id": lag_id,
                    "replicate": replicate,
                    "seed": status["seed"],
                    "total_samples": total,
                    "accepted_samples": accepted,
                    "acceptance_fraction": accepted / total if total else 0.0,
                    "has_valid_minimum": best is not None,
                    "chi2_min": _finite_float(best.get("chi2")) if best else None,
                    "AIC_min": _finite_float(best.get("AIC")) if best else None,
                    "k_params": _finite_float(best.get("k_params")) if best else None,
                }
            )

    if incomplete and not allow_incomplete:
        raise RuntimeError(f"Incomplete replicates: {incomplete}")

    summary_rows: List[Dict[str, Any]] = []
    for rep in prepared["representatives"]:
        rows = [row for row in minima_rows if row["proposal"] == rep["proposal"]]
        valid = [row for row in rows if row["has_valid_minimum"]]
        chi2_values = [float(row["chi2_min"]) for row in valid]
        aic_values = [float(row["AIC_min"]) for row in valid]
        acceptance = [float(row["acceptance_fraction"]) for row in rows]
        summary_rows.append(
            {
                "agent": rep["agent"],
                "proposal": rep["proposal"],
                "headline_chi2": rep["headline_chi2"],
                "headline_AIC": rep["headline_aic"],
                "headline_k": rep["headline_k"],
                "completed_replicates": len(rows),
                "valid_minimum_replicates": len(valid),
                "failed_minimum_replicates": len(rows) - len(valid),
                "chi2_min_mean": statistics.mean(chi2_values) if chi2_values else None,
                "chi2_min_sd": _sample_sd(chi2_values) if chi2_values else None,
                "chi2_min_median": statistics.median(chi2_values) if chi2_values else None,
                "chi2_min_low": min(chi2_values) if chi2_values else None,
                "chi2_min_high": max(chi2_values) if chi2_values else None,
                "AIC_min_mean": statistics.mean(aic_values) if aic_values else None,
                "AIC_min_sd": _sample_sd(aic_values) if aic_values else None,
                "AIC_min_median": statistics.median(aic_values) if aic_values else None,
                "AIC_min_low": min(aic_values) if aic_values else None,
                "AIC_min_high": max(aic_values) if aic_values else None,
                "mean_acceptance_fraction": statistics.mean(acceptance) if acceptance else None,
            }
        )

    reports = output_root / "summary"
    _write_csv(reports / "replicate_minima.csv", minima_rows)
    _write_csv(reports / "fixed7_resampling_summary.csv", summary_rows)
    payload = {
        "experiment_id": prepared["experiment_id"],
        "sampling_contract": prepared.get("sampling_contract"),
        "expected_replicates": expected_replicates,
        "incomplete_replicates": incomplete,
        "rows": summary_rows,
    }
    _write_json(reports / "fixed7_resampling_summary.json", payload)

    markdown = [
        "# Fixed-Lagrangian 20 x 5000 resampling",
        "",
        "Each entry is the minimum from one 5000-sample scan of a fixed serialized Lagrangian.",
        "Only the random seed changes. The reported standard deviation is finite-budget parameter-search",
        "variability; it is not observational uncertainty and not variability of the theory-proposal agent.",
        "",
        "| Agent | Proposal | headline AIC | valid/total | mean minimum AIC | SD | range | mean accepted |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        mean = row["AIC_min_mean"]
        sd = row["AIC_min_sd"]
        low = row["AIC_min_low"]
        high = row["AIC_min_high"]
        markdown.append(
            f"| {row['agent']} | {row['proposal']} | {row['headline_AIC']:.6f} "
            f"| {row['valid_minimum_replicates']}/{row['completed_replicates']} "
            f"| {mean:.6f} | {sd:.6f} | {low:.6f}--{high:.6f} | {100*row['mean_acceptance_fraction']:.2f}% |"
            if mean is not None and sd is not None and low is not None and high is not None
            else (
                f"| {row['agent']} | {row['proposal']} | {row['headline_AIC']:.6f} "
                f"| 0/{row['completed_replicates']} | -- | -- | -- | -- |"
            )
        )
    (reports / "summary.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")

    latex = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Fixed-Lagrangian parameter-search stability control.  Each entry summarizes 20 independent 5000-sample scans with the serialized Lagrangian and broad parameter prior held fixed.  The quoted scatter is the sample standard deviation of the recovered minima; it measures finite-budget search variability, not observational uncertainty or agent-to-agent variability.}",
        r"\label{tab:fixed-lagrangian-resampling}",
        r"\small",
        r"\setlength{\tabcolsep}{5pt}",
        r"\begin{ruledtabular}",
        r"\begin{tabular}{llrrrrr}",
        r"Agent & Proposal & Headline AIC & Valid scans & $\langle\mathrm{AIC}_{\min}\rangle\pm s$ & AIC range & Accepted (\%) \\ ",
        r"\hline",
    ]
    for row in summary_rows:
        if row["AIC_min_mean"] is None:
            result = r"--"
            aic_range = r"--"
            acceptance_text = r"--"
        else:
            result = f"${row['AIC_min_mean']:.4f} \\pm {row['AIC_min_sd']:.4f}$"
            aic_range = f"{row['AIC_min_low']:.4f}--{row['AIC_min_high']:.4f}"
            acceptance_text = f"{100*row['mean_acceptance_fraction']:.1f}"
        latex.append(
            f"{row['agent']} & {row['proposal']} & "
            f"{row['headline_AIC']:.4f} & "
            f"{row['valid_minimum_replicates']}/{row['completed_replicates']} & "
            f"{result} & {aic_range} & {acceptance_text} \\\\"
        )
    latex.extend([r"\end{tabular}", r"\end{ruledtabular}", r"\end{table*}"])
    (reports / "paper_table.tex").write_text("\n".join(latex) + "\n", encoding="utf-8")
    print(reports)
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--source-root", type=Path, default=ROOT / "ai_theory_lab" / "runs")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("check", help="Validate all seven source task directories")
    prepare = subparsers.add_parser("prepare", help="Combine seven Lagrangians and run EOM/Builder once")
    prepare.add_argument("--force", action="store_true")
    run = subparsers.add_parser("run", help="Run one 7-model, 5000-sample replicate")
    run.add_argument("--replicate", type=int, required=True)
    run.add_argument("--samples", type=int, default=5000)
    run.add_argument("--workers", type=int, default=7)
    run.add_argument("--force", action="store_true")
    summarize = subparsers.add_parser("summarize", help="Summarize all replicate minima")
    summarize.add_argument("--expected-replicates", type=int, default=20)
    summarize.add_argument("--allow-incomplete", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest_path = args.manifest.expanduser().resolve()
    source_root = args.source_root.expanduser()
    if not source_root.is_absolute():
        source_root = (ROOT / source_root).resolve()
    output_root = args.output_root.expanduser()
    if not output_root.is_absolute():
        output_root = (ROOT / output_root).resolve()

    if args.command == "check":
        for row in check_sources(manifest_path, source_root):
            print(
                f"{row['proposal']}: source={row['source']} n_terms={row['n_terms']} "
                f"scalar={row['scalar_config']} sha256={row['sha256'][:12]}"
            )
        return 0
    if args.command == "prepare":
        prepare_experiment(manifest_path, source_root, output_root, force=args.force)
        return 0
    if args.command == "run":
        run_replicate(
            output_root,
            args.replicate,
            sample_count=args.samples,
            workers=args.workers,
            force=args.force,
        )
        return 0
    if args.command == "summarize":
        summarize_results(
            output_root,
            expected_replicates=args.expected_replicates,
            allow_incomplete=args.allow_incomplete,
        )
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
