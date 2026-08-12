"""Strict validation harness for the modified-gravity pipeline.

The harness is the gatekeeper between an AI theory proposal and a validated
result. It does not estimate scores. It runs the real project scripts and reads
the chi2 written by Solver.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import pickle
import random
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .memory import record_attempt
from .proposal import _normalize_parameter_samples, _validate_parameter_samples, compile_proposal_to_run
from .validation_result import StageResult, ValidationResult


ROOT = Path(__file__).resolve().parents[1]
SOLVER_RESULT_DIR = ROOT / "solver_result"
AGENT_RUNS_DIR = ROOT / "ai_theory_lab" / "runs"
TAIL_CHARS = 12000


STAGE_COMMANDS: List[Tuple[str, List[str]]] = [
    ("EOM", ["EOM v5.2.py"]),
    ("Builder", ["Builder v5.2.py"]),
    ("Solver", ["Solver v5.2.py"]),
]


def _tail(text: str, limit: int = TAIL_CHARS) -> str:
    if len(text) <= limit:
        return text
    return text[-limit:]


def _base_env(extra_env: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")
    env.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib-cache"))
    if extra_env:
        env.update({str(k): str(v) for k, v in extra_env.items()})
    return env


def _run_stage(
    stage: str,
    script_args: List[str],
    *,
    python_executable: str,
    timeout_seconds: Optional[int],
    extra_env: Optional[Dict[str, str]] = None,
) -> StageResult:
    cmd = [python_executable] + script_args
    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            env=_base_env(extra_env),
        )
        return StageResult(
            stage=stage,
            cmd=cmd,
            returncode=proc.returncode,
            elapsed_seconds=time.time() - t0,
            stdout_tail=_tail(proc.stdout),
            stderr_tail=_tail(proc.stderr),
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        return StageResult(
            stage=stage,
            cmd=cmd,
            returncode=124,
            elapsed_seconds=time.time() - t0,
            stdout_tail=_tail(stdout),
            stderr_tail=_tail(stderr + f"\nTIMEOUT after {timeout_seconds} seconds."),
        )


def _ranking_files() -> List[Path]:
    if not SOLVER_RESULT_DIR.exists():
        return []
    return sorted(
        SOLVER_RESULT_DIR.glob("*/model_ranking.csv"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def latest_solver_output_dir() -> Optional[Path]:
    files = _ranking_files()
    return files[0].parent if files else None


def read_best_result(output_dir: Path) -> Dict[str, object]:
    ranking_path = output_dir / "model_ranking.csv"
    if not ranking_path.exists():
        raise FileNotFoundError(f"Missing model_ranking.csv: {ranking_path}")

    with ranking_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"model_ranking.csv is empty: {ranking_path}")

    rows = sorted(rows, key=lambda r: (float(r["chi2"]), float(r.get("AIC", "inf"))))
    best = rows[0]
    chi2 = float(best["chi2"])
    aic = float(best["AIC"])
    try:
        k_params = int(float(best.get("k_params")))
    except (TypeError, ValueError):
        # Older Solver outputs predate the explicit k_params column, but AIC
        # still contains the same information.
        k_params = max(0, int(round((aic - chi2) / 2.0)))
    return {
        "best_lag_id": best["lag_id"],
        "chi2": chi2,
        "aic": aic,
        "bic": float(best["BIC"]),
        "k_params": k_params,
        "k_parameter_names": [
            name for name in str(best.get("k_parameter_names") or "").split(";") if name
        ],
        "model_ranking_path": str(ranking_path),
        "scan_report_path": str(output_dir / "scan_report.txt"),
    }


def summarize_reject_reasons(output_dir: Path, limit: int = 12) -> List[Dict[str, str]]:
    path = output_dir / "reject_reasons_by_model.csv"
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: int(r.get("count", "0")), reverse=True)
    return rows[:limit]


def solver_feedback_paths(output_dir: Path) -> Dict[str, str]:
    paths = {
        "all_samples_summary_path": output_dir / "all_samples_summary.csv",
        "accepted_samples_summary_path": output_dir / "accepted_samples_summary.csv",
        "reject_reasons_by_model_path": output_dir / "reject_reasons_by_model.csv",
    }
    return {key: str(path) for key, path in paths.items() if path.exists()}


def _make_agent_run_dir(run_dir: Optional[Path] = None) -> Path:
    if run_dir is not None:
        path = run_dir.expanduser().resolve()
    else:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = AGENT_RUNS_DIR / f"agent_{stamp}_{uuid.uuid4().hex[:8]}"
    path.mkdir(parents=True, exist_ok=False)
    return path


def _load_lagrangian_pool(source_path: Path) -> Dict[int, List[Dict[str, Any]]]:
    with source_path.open("rb") as f:
        data = pickle.load(f)
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict n_terms -> list from {source_path}, got {type(data).__name__}")
    pool: Dict[int, List[Dict[str, Any]]] = {}
    for key, value in data.items():
        try:
            n_terms = int(key)
        except Exception as exc:
            raise TypeError(f"Invalid n_terms key in {source_path}: {key!r}") from exc
        if not isinstance(value, list):
            raise TypeError(f"Expected list for n_terms={n_terms}, got {type(value).__name__}")
        pool[n_terms] = value
    return pool


def _operator_specs(lagrangian: Dict[str, Any]) -> List[Dict[str, str]]:
    specs: List[Dict[str, str]] = []
    for term in lagrangian.get("terms", []):
        if term.get("fixed"):
            continue
        candidate = str(term.get("candidate"))
        coeff_symbol = str(term.get("coeff_symbol"))
        if not candidate or not coeff_symbol or coeff_symbol == "1":
            continue
        specs.append({"candidate": candidate, "coefficient": coeff_symbol})
    return specs


def _coefficient_symbols(lagrangian: Dict[str, Any]) -> List[str]:
    return [spec["coefficient"] for spec in _operator_specs(lagrangian)]


def _write_normalized_parameter_samples(
    source_path: Path,
    target_path: Path,
    coeffs: List[str],
    *,
    scalar_config: str = "none",
) -> None:
    with source_path.open(encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and isinstance(data.get("samples"), list):
        samples = data["samples"]
    else:
        samples = data
    _validate_parameter_samples(samples, coeffs, scalar_config=scalar_config)
    normalized = _normalize_parameter_samples(samples, coeffs)
    target_path.write_text(json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8")


def write_agent_lagrangians_from_sample(
    *,
    source_path: Path,
    target_path: Path,
    seed: int,
    max_terms: Optional[int] = None,
    source_n_terms: Optional[int] = None,
    source_local_number: Optional[int] = None,
) -> Dict[str, Any]:
    """Pick one existing Lagrangian and write an isolated agent_lagrangians.pkl."""

    pool = _load_lagrangian_pool(source_path)
    if source_n_terms is not None or source_local_number is not None:
        if source_n_terms is None or source_local_number is None:
            raise ValueError("source_n_terms and source_local_number must be provided together")
        if source_n_terms not in pool:
            raise ValueError(f"No n_terms={source_n_terms} group in {source_path}")
        local_index = source_local_number - 1
        if local_index < 0 or local_index >= len(pool[source_n_terms]):
            raise ValueError(
                f"source_local_number={source_local_number} out of range for "
                f"n_terms={source_n_terms}; available={len(pool[source_n_terms])}"
            )
        n_terms = source_n_terms
        lagrangian = pool[n_terms][local_index]
    else:
        candidates: List[Tuple[int, int, Dict[str, Any]]] = []
        for n_terms in sorted(pool):
            if max_terms is not None and n_terms > max_terms:
                continue
            for idx, lagrangian in enumerate(pool[n_terms]):
                candidates.append((n_terms, idx, lagrangian))
        if not candidates:
            raise ValueError(f"No Lagrangians available from {source_path} with max_terms={max_terms}")

        rng = random.Random(seed)
        n_terms, local_index, lagrangian = rng.choice(candidates)
    isolated = {n_terms: [lagrangian]}

    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("wb") as f:
        pickle.dump(isolated, f, protocol=pickle.HIGHEST_PROTOCOL)

    metadata = {
        "source_lagrangians_path": str(source_path),
        "agent_lagrangians_path": str(target_path),
        "seed": seed,
        "max_terms": max_terms,
        "source_n_terms": n_terms,
        "source_local_index": local_index,
        "source_local_number": local_index + 1,
        "scalar_config": lagrangian.get("scalar_config"),
        "potential_types": lagrangian.get("potential_types"),
        "operators": [spec["candidate"] for spec in _operator_specs(lagrangian)],
        "operator_specs": _operator_specs(lagrangian),
        "coefficient_symbols": _coefficient_symbols(lagrangian),
        "general": lagrangian.get("general"),
    }
    (target_path.parent / "agent_lagrangian_metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return metadata


def validate_current_pipeline(
    *,
    python_executable: Optional[str] = None,
    timeout_eom: int = 3600,
    timeout_builder: int = 3600,
    timeout_solver: int = 7200,
    extra_env: Optional[Dict[str, str]] = None,
) -> ValidationResult:
    """Run EOM -> Builder -> Solver and return Solver's best chi2."""

    py = python_executable or sys.executable
    timeouts = {
        "EOM": timeout_eom,
        "Builder": timeout_builder,
        "Solver": timeout_solver,
    }
    stages: List[StageResult] = []

    for stage, script_args in STAGE_COMMANDS:
        result = _run_stage(
            stage,
            script_args,
            python_executable=py,
            timeout_seconds=timeouts[stage],
            extra_env=extra_env,
        )
        stages.append(result)
        if not result.ok:
            return ValidationResult(
                validated=False,
                failed_stage=stage,
                stages=stages,
                diagnostics={
                    "message": f"{stage} failed. Return stdout/stderr tails to the proposing agent.",
                    "returncode": result.returncode,
                },
            )

    output_dir = latest_solver_output_dir()
    if output_dir is None:
        return ValidationResult(
            validated=False,
            failed_stage="Solver",
            stages=stages,
            diagnostics={"message": "Solver finished but no model_ranking.csv was found."},
        )

    try:
        best = read_best_result(output_dir)
    except Exception as exc:
        return ValidationResult(
            validated=False,
            failed_stage="Solver",
            solver_output_dir=str(output_dir),
            stages=stages,
            diagnostics={"message": f"Could not read Solver ranking: {type(exc).__name__}: {exc}"},
        )

    return ValidationResult(
        validated=True,
        best_lag_id=str(best["best_lag_id"]),
        chi2=float(best["chi2"]),
        aic=float(best["aic"]),
        bic=float(best["bic"]),
        k_params=int(best["k_params"]),
        k_parameter_names=list(best["k_parameter_names"]),
        solver_output_dir=str(output_dir),
        model_ranking_path=str(best["model_ranking_path"]),
        scan_report_path=str(best["scan_report_path"]),
        stages=stages,
        diagnostics={"top_reject_reasons": summarize_reject_reasons(output_dir)},
    )


def validate_agent_sample_pipeline(
    *,
    python_executable: Optional[str] = None,
    proposal_path: Optional[Path] = None,
    source_lagrangians_path: Optional[Path] = None,
    run_dir: Optional[Path] = None,
    seed: int = 42,
    max_terms: Optional[int] = None,
    source_n_terms: Optional[int] = None,
    source_local_number: Optional[int] = None,
    parameter_samples_path: Optional[Path] = None,
    timeout_eom: int = 3600,
    timeout_builder: int = 3600,
    timeout_solver: int = 7200,
    extra_env: Optional[Dict[str, str]] = None,
) -> ValidationResult:
    """Validate one sampled Lagrangian through isolated agent files.

    This is the intended harness shape for a future one-theory proposal agent.
    It does not run the full 1120-theory batch unless the sampled pkl is replaced
    by a larger proposal file on purpose.
    """

    py = python_executable or sys.executable
    source_path = (source_lagrangians_path or (ROOT / "lagrangians.pkl")).expanduser().resolve()
    agent_dir = _make_agent_run_dir(run_dir)
    agent_lagrangians_path = agent_dir / "agent_lagrangians.pkl"
    eom_dir = agent_dir / "agent_eom_results"
    builder_output_dir = agent_dir / "agent_builder_result"
    solver_output_base = agent_dir / "agent_solver_result"
    solver_run_name = "agent_solve"
    solver_output_dir = solver_output_base / solver_run_name
    build_cache_path = agent_dir / "agent_built_models_cache.pkl"
    agent_parameter_samples_path: Optional[Path] = None

    try:
        if proposal_path is not None:
            if parameter_samples_path is not None:
                raise ValueError("Use parameter_samples inside proposal.json, not --agent-parameter-samples")
            metadata = compile_proposal_to_run(proposal_path, agent_dir)
            if metadata.get("agent_parameter_samples_path"):
                agent_parameter_samples_path = Path(str(metadata["agent_parameter_samples_path"]))
        else:
            metadata = write_agent_lagrangians_from_sample(
                source_path=source_path,
                target_path=agent_lagrangians_path,
                seed=seed,
                max_terms=max_terms,
                source_n_terms=source_n_terms,
                source_local_number=source_local_number,
            )
            if parameter_samples_path is not None:
                source_parameter_path = parameter_samples_path.expanduser().resolve()
                if not source_parameter_path.exists():
                    raise FileNotFoundError(f"Agent parameter samples file does not exist: {source_parameter_path}")
                agent_parameter_samples_path = agent_dir / "agent_parameter_samples.json"
                _write_normalized_parameter_samples(
                    source_parameter_path,
                    agent_parameter_samples_path,
                    list(metadata.get("coefficient_symbols") or []),
                    scalar_config=str(metadata.get("scalar_config") or "none"),
                )
                metadata["agent_parameter_samples_path"] = str(agent_parameter_samples_path)
    except Exception as exc:
        return ValidationResult(
            validated=False,
            failed_stage="AgentSample",
            solver_output_dir=str(agent_dir),
            diagnostics={"message": f"Could not create agent_lagrangians.pkl: {type(exc).__name__}: {exc}"},
        )

    common_env = dict(extra_env or {})
    stages: List[StageResult] = []

    stage_specs = [
        (
            "EOM",
            ["EOM v5.2.py"],
            timeout_eom,
            {
                **common_env,
                "EOM_LAGRANGIANS_PATH": str(agent_lagrangians_path),
                "EOM_OUTPUT_DIR": str(eom_dir),
                "EOM_MAX_TERMS": "all",
                "EOM_N_SAMPLES": "all",
                "EOM_RUN_SELF_TEST": common_env.get("EOM_RUN_SELF_TEST", "0"),
            },
        ),
        (
            "Builder",
            ["Builder v5.2.py"],
            timeout_builder,
            {
                **common_env,
                "EOM_SUMMARY_PATH": str(eom_dir / "eom_summary.txt"),
                "SOLVER_OUTPUT_DIR": str(builder_output_dir),
                "SOLVER_RUN_NAME": "agent_build",
                "BUILD_CACHE_PATH": str(build_cache_path),
                "MAX_MODELS_TO_BUILD": "0",
            },
        ),
        (
            "Solver",
            ["Solver v5.2.py"],
            timeout_solver,
            {
                **common_env,
                "BUILD_CACHE_PATH": str(build_cache_path),
                "SOLVER_OUTPUT_DIR": str(solver_output_base),
                "SOLVER_RUN_NAME": solver_run_name,
                "MAX_MODELS_TO_BUILD": "0",
                "SOLVER_MAKE_PLOTS": common_env.get("SOLVER_MAKE_PLOTS", "0"),
                "TOP_N": common_env.get("TOP_N", "0"),
                **(
                    {"PARAMETER_SAMPLES_PATH": str(agent_parameter_samples_path)}
                    if agent_parameter_samples_path is not None
                    else {}
                ),
            },
        ),
    ]

    for stage, script_args, timeout, env in stage_specs:
        result = _run_stage(
            stage,
            script_args,
            python_executable=py,
            timeout_seconds=timeout,
            extra_env=env,
        )
        stages.append(result)
        if not result.ok:
            return ValidationResult(
                validated=False,
                failed_stage=stage,
                solver_output_dir=str(solver_output_dir),
                stages=stages,
                diagnostics={
                    "message": f"{stage} failed while validating isolated agent_lagrangians.pkl.",
                    "returncode": result.returncode,
                    "agent_run_dir": str(agent_dir),
                    "agent_lagrangian": metadata,
                },
            )

    try:
        best = read_best_result(solver_output_dir)
    except Exception as exc:
        return ValidationResult(
            validated=False,
            failed_stage="Solver",
            solver_output_dir=str(solver_output_dir),
            stages=stages,
            diagnostics={
                "message": f"Could not read isolated Solver ranking: {type(exc).__name__}: {exc}",
                "agent_run_dir": str(agent_dir),
                "agent_lagrangian": metadata,
                "top_reject_reasons": summarize_reject_reasons(solver_output_dir),
                **solver_feedback_paths(solver_output_dir),
            },
        )

    return ValidationResult(
        validated=True,
        best_lag_id=str(best["best_lag_id"]),
        chi2=float(best["chi2"]),
        aic=float(best["aic"]),
        bic=float(best["bic"]),
        k_params=int(best["k_params"]),
        k_parameter_names=list(best["k_parameter_names"]),
        solver_output_dir=str(solver_output_dir),
        model_ranking_path=str(best["model_ranking_path"]),
        scan_report_path=str(best["scan_report_path"]),
        stages=stages,
        diagnostics={
            "agent_run_dir": str(agent_dir),
            "agent_lagrangian": metadata,
            "top_reject_reasons": summarize_reject_reasons(solver_output_dir),
            **solver_feedback_paths(solver_output_dir),
        },
    )


def read_existing_output(output_dir: Path) -> ValidationResult:
    """Read one existing Solver output directory without claiming validation."""

    try:
        best = read_best_result(output_dir)
    except Exception as exc:
        return ValidationResult(
            validated=False,
            failed_stage="Solver",
            solver_output_dir=str(output_dir),
            diagnostics={"message": f"Could not read ranking: {type(exc).__name__}: {exc}"},
        )
    return ValidationResult(
        validated=False,
        best_lag_id=str(best["best_lag_id"]),
        chi2=float(best["chi2"]),
        aic=float(best["aic"]),
        bic=float(best["bic"]),
        k_params=int(best["k_params"]),
        k_parameter_names=list(best["k_parameter_names"]),
        solver_output_dir=str(output_dir),
        model_ranking_path=str(best["model_ranking_path"]),
        scan_report_path=str(best["scan_report_path"]),
        diagnostics={
            "message": "Read-only check of existing Solver output; this did not run EOM/Builder/Solver.",
            "top_reject_reasons": summarize_reject_reasons(output_dir),
        },
    )


def read_latest_only() -> ValidationResult:
    """Read the latest Solver output without claiming a new validation run."""

    output_dir = latest_solver_output_dir()
    if output_dir is None:
        return ValidationResult(
            validated=False,
            failed_stage="Solver",
            diagnostics={"message": "No existing model_ranking.csv found."},
        )
    return read_existing_output(output_dir)


def _parse_env_overrides(values: Iterable[str]) -> Dict[str, str]:
    env: Dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise ValueError(f"Expected KEY=VALUE for --env, got: {item}")
        key, value = item.split("=", 1)
        env[key] = value
    return env


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run or inspect strict pipeline validation.")
    parser.add_argument(
        "--read-latest-only",
        action="store_true",
        help="Only read the latest Solver ranking. Does not validate a new theory.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Read this existing Solver output directory. Implies read-only mode.",
    )
    parser.add_argument(
        "--agent-sample",
        action="store_true",
        help="Sample one Lagrangian into agent_lagrangians.pkl and validate only that isolated theory.",
    )
    parser.add_argument(
        "--proposal",
        type=Path,
        help="Compile proposal JSON into agent_lagrangians.pkl and validate it.",
    )
    parser.add_argument("--source-lagrangians", type=Path, default=ROOT / "lagrangians.pkl")
    parser.add_argument("--agent-run-dir", type=Path)
    parser.add_argument("--agent-seed", type=int, default=42)
    parser.add_argument(
        "--agent-max-terms",
        type=int,
        help="Only sample from source Lagrangians with n_terms <= this value.",
    )
    parser.add_argument("--agent-source-n-terms", type=int)
    parser.add_argument(
        "--agent-source-local-number",
        type=int,
        help="1-based index within the selected n_terms group.",
    )
    parser.add_argument(
        "--agent-parameter-samples",
        type=Path,
        help="JSON file with agent-proposed numerical parameter samples for Solver.",
    )
    parser.add_argument("--python", default=sys.executable, help="Python executable for stage scripts.")
    parser.add_argument("--timeout-eom", type=int, default=3600)
    parser.add_argument("--timeout-builder", type=int, default=3600)
    parser.add_argument("--timeout-solver", type=int, default=7200)
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Environment override for all stage scripts. Can be repeated.",
    )
    parser.add_argument(
        "--memory-dir",
        type=Path,
        help="Append this validation result to a current-loop memory directory.",
    )
    parser.add_argument(
        "--loop-id",
        help="Optional label stored with --memory-dir attempt records, such as loop_01.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)

    try:
        env = _parse_env_overrides(args.env)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.output_dir is not None:
        result = read_existing_output(args.output_dir.expanduser().resolve())
    elif args.read_latest_only:
        result = read_latest_only()
    elif args.agent_sample or args.proposal is not None:
        result = validate_agent_sample_pipeline(
            python_executable=args.python,
            proposal_path=args.proposal,
            source_lagrangians_path=args.source_lagrangians,
            run_dir=args.agent_run_dir,
            seed=args.agent_seed,
            max_terms=args.agent_max_terms,
            source_n_terms=args.agent_source_n_terms,
            source_local_number=args.agent_source_local_number,
            parameter_samples_path=args.agent_parameter_samples,
            timeout_eom=args.timeout_eom,
            timeout_builder=args.timeout_builder,
            timeout_solver=args.timeout_solver,
            extra_env=env,
        )
    else:
        result = validate_current_pipeline(
            python_executable=args.python,
            timeout_eom=args.timeout_eom,
            timeout_builder=args.timeout_builder,
            timeout_solver=args.timeout_solver,
            extra_env=env,
        )

    if args.memory_dir is not None:
        memory_info = record_attempt(result, args.memory_dir, loop_id=args.loop_id)
        result.diagnostics = {
            **(result.diagnostics or {}),
            "agent_memory": {
                "memory_dir": memory_info["memory_dir"],
                "attempt_history_path": memory_info["attempt_history_path"],
                "feedback_summary_path": memory_info["feedback_summary_path"],
                "reflection_prompt_path": memory_info["reflection_prompt_path"],
            },
        }

    print(json.dumps(result.to_dict(), indent=2 if args.pretty else None, ensure_ascii=False))
    if args.read_latest_only or args.output_dir is not None:
        return 0 if result.chi2 is not None else 1
    return 0 if result.validated else 1


if __name__ == "__main__":
    raise SystemExit(main())
