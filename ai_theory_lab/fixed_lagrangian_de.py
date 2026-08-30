"""Differential-Evolution baseline for fixed validated Lagrangians.

The theory, Builder reduction, likelihood, physical cuts, and broad cold-start
parameter bounds are held fixed.  No LLM, agent memory, learned parameter
prior, historical best-fit vector, or local polishing step is used.

Each optimization uses a 50-member population for 99 generations, giving
exactly 5000 real Solver objective evaluations.  The Oscar array maps the
seven non-Sonnet headline representatives and 20 independent seeds onto 140
standalone tasks.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import multiprocessing as mp
import os
import statistics
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import numpy as np
from scipy.optimize import differential_evolution
from scipy.stats import qmc

from solver_v5_2.core import (
    MODE,
    PROFILED_LIKELIHOOD_PARAMETER_NAMES,
    SampleResult,
    effective_parameter_names,
    evaluate_sample,
    get_param_symbols,
    lambdify_model,
    load_current_likelihood_data,
    result_row,
    write_best_solution,
)
from solver_v5_2.runner import _load_built_models_cache

from .config_p import COEFFICIENT_PRIOR, PARAMETER_PRIORS
from .fixed_lagrangian_resampling import (
    DEFAULT_MANIFEST,
    _read_json,
    _representatives,
    _sample_sd,
    _write_csv,
    _write_json,
    prepare_experiment,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "ai_theory_lab" / "resampling" / "fixed7_de_20x5000_v1"
BASE_SEED = 2026082900
DEFAULT_REPLICATES = 20
DEFAULT_EVALUATION_BUDGET = 5000
DEFAULT_POPULATION_SIZE = 50
DEFAULT_MUTATION = (0.5, 1.0)
DEFAULT_RECOMBINATION = 0.7
INVALID_OBJECTIVE_PENALTY = 1.0e12


@dataclass(frozen=True)
class ParameterSpec:
    name: str
    transform: str
    low: float
    high: float

    def from_unit(self, value: float) -> float:
        u = float(np.clip(value, 0.0, 1.0))
        if self.transform == "linear":
            return self.low + u * (self.high - self.low)
        if self.transform == "log10":
            lo = math.log10(self.low)
            hi = math.log10(self.high)
            return 10.0 ** (lo + u * (hi - lo))
        if self.transform == "signed_log10":
            sign = -1.0 if u < 0.5 else 1.0
            local = (u * 2.0) if u < 0.5 else ((u - 0.5) * 2.0)
            lo = math.log10(self.low)
            hi = math.log10(self.high)
            return sign * 10.0 ** (lo + local * (hi - lo))
        raise ValueError(f"Unsupported transform: {self.transform}")


def _prior_spec(name: str) -> ParameterSpec:
    prior = PARAMETER_PRIORS[name]
    if prior.get("signed_log10"):
        transform = "signed_log10"
    elif prior.get("log10"):
        transform = "log10"
    else:
        transform = "linear"
    return ParameterSpec(name, transform, float(prior["low"]), float(prior["high"]))


_NAMED_SPECS = {
    name: _prior_spec(name)
    for name in PARAMETER_PRIORS
}


def _coefficient_spec(name: str) -> ParameterSpec:
    return ParameterSpec(
        name=name,
        transform="signed_log10",
        low=10.0 ** float(COEFFICIENT_PRIOR["log10_abs_low"]),
        high=10.0 ** float(COEFFICIENT_PRIOR["log10_abs_high"]),
    )


def _parameter_specs(model: Any) -> List[ParameterSpec]:
    param_syms = get_param_symbols(model)
    effective = effective_parameter_names(model, param_syms, MODE)
    profiled = set(PROFILED_LIKELIHOOD_PARAMETER_NAMES)
    names = [name for name in effective if name not in profiled]
    specs: List[ParameterSpec] = []
    symbol_names = {str(symbol) for symbol in param_syms}
    for name in names:
        if name in _NAMED_SPECS:
            specs.append(_NAMED_SPECS[name])
        elif name in symbol_names:
            specs.append(_coefficient_spec(name))
        else:
            raise KeyError(f"No DE parameter transform is defined for active parameter {name!r}")
    if not specs:
        raise ValueError(f"Lagrangian {model.lag_id} has no explicit parameters to optimize")
    return specs


def _geometric_midpoint(low: float, high: float) -> float:
    return math.sqrt(float(low) * float(high))


def _base_parameter_sample(model: Any) -> Dict[str, float]:
    """Complete neutral sample; inactive bookkeeping directions stay fixed."""

    sample: Dict[str, float] = {
        "H0_km_s_Mpc": 0.5 * (
            PARAMETER_PRIORS["H0_km_s_Mpc"]["low"]
            + PARAMETER_PRIORS["H0_km_s_Mpc"]["high"]
        ),
        "Omega_m0": 0.5 * (
            PARAMETER_PRIORS["Omega_m0"]["low"]
            + PARAMETER_PRIORS["Omega_m0"]["high"]
        ),
        "lambda_H_Lambda_over_H0": _geometric_midpoint(
            PARAMETER_PRIORS["lambda_H_Lambda_over_H0"]["low"],
            PARAMETER_PRIORS["lambda_H_Lambda_over_H0"]["high"],
        ),
    }
    if model.has_phi1:
        sample.update(
            {
                "varphi1_0_phi1_over_Mp": _geometric_midpoint(
                    PARAMETER_PRIORS["varphi1_0_phi1_over_Mp"]["low"],
                    PARAMETER_PRIORS["varphi1_0_phi1_over_Mp"]["high"],
                ),
                "mu1_m1_over_H0": _geometric_midpoint(
                    PARAMETER_PRIORS["mu1_m1_over_H0"]["low"],
                    PARAMETER_PRIORS["mu1_m1_over_H0"]["high"],
                ),
                "fbar1_f1_over_Mp": _geometric_midpoint(
                    PARAMETER_PRIORS["fbar1_f1_over_Mp"]["low"],
                    PARAMETER_PRIORS["fbar1_f1_over_Mp"]["high"],
                ),
            }
        )
    if model.has_phi2:
        sample.update(
            {
                "varphi2_0_phi2_over_Lambda": _geometric_midpoint(
                    PARAMETER_PRIORS["varphi2_0_phi2_over_Lambda"]["low"],
                    PARAMETER_PRIORS["varphi2_0_phi2_over_Lambda"]["high"],
                ),
                "mu2_m2_over_Lambda": _geometric_midpoint(
                    PARAMETER_PRIORS["mu2_m2_over_Lambda"]["low"],
                    PARAMETER_PRIORS["mu2_m2_over_Lambda"]["high"],
                ),
                "fbar2_f2_over_Lambda": _geometric_midpoint(
                    PARAMETER_PRIORS["fbar2_f2_over_Lambda"]["low"],
                    PARAMETER_PRIORS["fbar2_f2_over_Lambda"]["high"],
                ),
                "q2_0_dvarphi2_dln_a": _geometric_midpoint(
                    PARAMETER_PRIORS["q2_0_dvarphi2_dln_a"]["low"],
                    PARAMETER_PRIORS["q2_0_dvarphi2_dln_a"]["high"],
                ),
            }
        )
    coefficient_default = 1.0
    for symbol in get_param_symbols(model):
        sample[str(symbol)] = coefficient_default
    return sample


def _sample_from_unit(
    unit_vector: Sequence[float],
    specs: Sequence[ParameterSpec],
    base_sample: Mapping[str, float],
) -> Dict[str, float]:
    if len(unit_vector) != len(specs):
        raise ValueError(f"Expected {len(specs)} DE coordinates, received {len(unit_vector)}")
    sample = {str(key): float(value) for key, value in base_sample.items()}
    for coordinate, spec in zip(unit_vector, specs):
        sample[spec.name] = spec.from_unit(float(coordinate))
    return sample


def _model_by_lag_id(models: Iterable[Any], lag_id: str) -> Any:
    matches = [model for model in models if str(model.lag_id) == str(lag_id)]
    if len(matches) != 1:
        raise ValueError(f"Expected one cached model for lag_id={lag_id}; found {len(matches)}")
    return matches[0]


def _replicate_seed(proposal: str, replicate: int) -> int:
    if replicate < 1:
        raise ValueError("replicate must be >= 1")
    label_term = sum((index + 1) * ord(char) for index, char in enumerate(proposal))
    return int((BASE_SEED + replicate * 100_003 + label_term * 10_007) % (2**32 - 1))


def task_index_to_selection(
    task_index: int,
    proposals: Sequence[str],
    replicates: int = DEFAULT_REPLICATES,
) -> tuple[str, int]:
    task_count = len(proposals) * int(replicates)
    if task_index < 1 or task_index > task_count:
        raise ValueError(f"task_index must be in 1..{task_count}")
    zero = task_index - 1
    return str(proposals[zero % len(proposals)]), zero // len(proposals) + 1


_WORKER_MODEL: Any | None = None
_WORKER_COMPILED: Any | None = None
_WORKER_SN_DATA: dict | None = None
_WORKER_BAO_DATA: dict | None = None
_WORKER_SPECS: List[ParameterSpec] = []
_WORKER_BASE_SAMPLE: Dict[str, float] = {}
_WORKER_LOG_PATH: Path | None = None
_WORKER_LOCAL_INDEX = 0


def _initialize_objective_worker(cache_path: str, lag_id: str, raw_log_dir: str) -> None:
    global _WORKER_MODEL, _WORKER_COMPILED, _WORKER_SN_DATA, _WORKER_BAO_DATA
    global _WORKER_SPECS, _WORKER_BASE_SAMPLE, _WORKER_LOG_PATH, _WORKER_LOCAL_INDEX

    models, _ = _load_built_models_cache(Path(cache_path))
    model = _model_by_lag_id(models, lag_id)
    if model.reject_reason:
        raise RuntimeError(f"Cached model L#{lag_id} is structurally rejected: {model.reject_reason}")
    sn_data, bao_data = load_current_likelihood_data()
    _WORKER_MODEL = model
    _WORKER_COMPILED = lambdify_model(model, MODE)
    _WORKER_SN_DATA = sn_data
    _WORKER_BAO_DATA = bao_data
    _WORKER_SPECS = _parameter_specs(model)
    _WORKER_BASE_SAMPLE = _base_parameter_sample(model)
    raw_dir = Path(raw_log_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    _WORKER_LOG_PATH = raw_dir / f"worker_{os.getpid()}.jsonl"
    _WORKER_LOCAL_INDEX = 0


def _append_worker_record(record: Dict[str, Any]) -> None:
    if _WORKER_LOG_PATH is None:
        return
    with _WORKER_LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, ensure_ascii=True) + "\n")


def _de_objective(unit_vector: Sequence[float]) -> float:
    global _WORKER_LOCAL_INDEX
    _WORKER_LOCAL_INDEX += 1
    started_ns = time.time_ns()
    sample = _sample_from_unit(unit_vector, _WORKER_SPECS, _WORKER_BASE_SAMPLE)
    try:
        result = evaluate_sample(
            _WORKER_MODEL,
            np.random.default_rng(0),
            MODE,
            compiled=_WORKER_COMPILED,
            sn_data=_WORKER_SN_DATA,
            bao_data=_WORKER_BAO_DATA,
            agent_sample=sample,
            agent_sample_index=_WORKER_LOCAL_INDEX,
        )
        success = bool(result.success and math.isfinite(result.chi2))
        objective = float(result.chi2) if success else INVALID_OBJECTIVE_PENALTY
        reason = str(result.reason)
        aic = float(result.aic) if success else None
        chi2 = float(result.chi2) if success else None
    except Exception as exc:  # Defensive boundary around the baseline objective.
        success = False
        objective = INVALID_OBJECTIVE_PENALTY
        reason = f"objective exception: {type(exc).__name__}: {exc}"
        aic = None
        chi2 = None
    _append_worker_record(
        {
            "finished_ns": time.time_ns(),
            "started_ns": started_ns,
            "pid": os.getpid(),
            "worker_local_index": _WORKER_LOCAL_INDEX,
            "success": success,
            "reason": reason,
            "objective": objective,
            "chi2": chi2,
            "AIC": aic,
            "unit_vector": [float(value) for value in unit_vector],
            "parameters": sample,
        }
    )
    return objective


def _read_raw_evaluations(raw_log_dir: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for path in sorted(raw_log_dir.glob("worker_*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(json.loads(line))
    records.sort(
        key=lambda row: (
            int(row.get("finished_ns") or 0),
            int(row.get("pid") or 0),
            int(row.get("worker_local_index") or 0),
        )
    )
    return records


def _write_evaluation_reports(
    run_dir: Path,
    records: Sequence[Dict[str, Any]],
    population_size: int,
    k_params: int,
) -> Dict[str, Any]:
    flattened: List[Dict[str, Any]] = []
    convergence: List[Dict[str, Any]] = []
    best_chi2 = math.inf
    accepted = 0
    reasons: Counter[str] = Counter()
    for index, record in enumerate(records, 1):
        success = bool(record.get("success"))
        chi2 = record.get("chi2")
        if success and chi2 is not None and math.isfinite(float(chi2)):
            accepted += 1
            best_chi2 = min(best_chi2, float(chi2))
        else:
            reasons[str(record.get("reason") or "unknown failure")] += 1
        generation = 0 if index <= population_size else math.ceil(
            (index - population_size) / population_size
        )
        row = {
            "evaluation": index,
            "generation": generation,
            "success": success,
            "reason": record.get("reason"),
            "objective": record.get("objective"),
            "chi2": record.get("chi2"),
            "AIC": record.get("AIC"),
        }
        for name, value in (record.get("parameters") or {}).items():
            row[str(name)] = value
        flattened.append(row)
        convergence.append(
            {
                "evaluation": index,
                "generation": generation,
                "best_chi2": best_chi2 if math.isfinite(best_chi2) else None,
                "best_AIC": best_chi2 + 2.0 * k_params if math.isfinite(best_chi2) else None,
            }
        )
    _write_csv(run_dir / "evaluations.csv", flattened)
    _write_csv(run_dir / "convergence.csv", convergence)
    _write_csv(
        run_dir / "reject_reasons.csv",
        [
            {"reason": reason, "count": count}
            for reason, count in reasons.most_common()
        ],
    )
    return {
        "evaluations_logged": len(records),
        "accepted_evaluations": accepted,
        "acceptance_fraction": accepted / len(records) if records else 0.0,
        "reject_reasons": dict(reasons),
    }


def _verify_best(
    cache_path: Path,
    lag_id: str,
    unit_vector: Sequence[float],
) -> tuple[SampleResult, Dict[str, float], List[ParameterSpec]]:
    models, _ = _load_built_models_cache(cache_path)
    model = _model_by_lag_id(models, lag_id)
    specs = _parameter_specs(model)
    sample = _sample_from_unit(unit_vector, specs, _base_parameter_sample(model))
    sn_data, bao_data = load_current_likelihood_data()
    result = evaluate_sample(
        model,
        np.random.default_rng(0),
        MODE,
        compiled=lambdify_model(model, MODE),
        sn_data=sn_data,
        bao_data=bao_data,
        agent_sample=sample,
        agent_sample_index=None,
    )
    return result, sample, specs


def _rep_for_proposal(prepared: Dict[str, Any], proposal: str) -> Dict[str, Any]:
    matches = [rep for rep in prepared["representatives"] if rep["proposal"] == proposal]
    if len(matches) != 1:
        raise ValueError(f"Expected one prepared representative for {proposal}; found {len(matches)}")
    return matches[0]


def run_de_optimization(
    output_root: Path,
    proposal: str,
    replicate: int,
    *,
    evaluation_budget: int = DEFAULT_EVALUATION_BUDGET,
    population_size: int = DEFAULT_POPULATION_SIZE,
    workers: int = 8,
    force: bool = False,
) -> Dict[str, Any]:
    if population_size < 5:
        raise ValueError("population_size must be at least 5")
    if evaluation_budget < population_size or evaluation_budget % population_size != 0:
        raise ValueError("evaluation_budget must be a positive multiple of population_size")
    prepared = _read_json(output_root / "inputs" / "prepared_manifest.json")
    expected_replicates = int(
        ((prepared.get("sampling_contract") or {}).get("replicates") or DEFAULT_REPLICATES)
    )
    if replicate < 1 or replicate > expected_replicates:
        raise ValueError(f"replicate must be in 1..{expected_replicates}")
    rep = _rep_for_proposal(prepared, proposal)
    lag_id = str(rep["batch_lag_id"])
    cache_path = Path(str(prepared["build_cache_path"]))
    run_dir = output_root / "runs" / proposal / f"replicate_{replicate:02d}"
    status_path = run_dir / "result.json"
    if status_path.exists() and not force:
        previous = _read_json(status_path)
        if previous.get("complete") is True:
            print(status_path)
            return previous
    run_dir.mkdir(parents=True, exist_ok=True)
    raw_log_dir = run_dir / "raw_evaluations"
    raw_log_dir.mkdir(parents=True, exist_ok=True)
    for old_log in raw_log_dir.glob("worker_*.jsonl"):
        old_log.unlink()

    models, _ = _load_built_models_cache(cache_path)
    model = _model_by_lag_id(models, lag_id)
    specs = _parameter_specs(model)
    dimensions = len(specs)
    seed = _replicate_seed(proposal, replicate)
    generations = evaluation_budget // population_size - 1
    initial_population = qmc.LatinHypercube(d=dimensions, seed=seed).random(population_size)
    bounds = [(0.0, 1.0)] * dimensions
    started = time.time()

    context = mp.get_context("spawn")
    with context.Pool(
        processes=max(1, int(workers)),
        initializer=_initialize_objective_worker,
        initargs=(str(cache_path), lag_id, str(raw_log_dir)),
    ) as pool:
        optimizer = differential_evolution(
            _de_objective,
            bounds,
            strategy="best1bin",
            maxiter=generations,
            popsize=1,  # Ignored because an explicit population is supplied.
            mutation=DEFAULT_MUTATION,
            recombination=DEFAULT_RECOMBINATION,
            seed=seed,
            polish=False,
            init=initial_population,
            updating="deferred",
            workers=pool.map,
            tol=0.0,
            # A negative absolute tolerance disables convergence termination;
            # the experiment stops only when its fixed evaluation budget ends.
            atol=-1.0,
        )

    elapsed = time.time() - started
    records = _read_raw_evaluations(raw_log_dir)
    verified, best_sample, verified_specs = _verify_best(cache_path, lag_id, optimizer.x)
    k_params = int(verified.k_params) if verified.success else int(rep["headline_k"])
    evaluation_stats = _write_evaluation_reports(
        run_dir,
        records,
        population_size,
        k_params,
    )
    write_best_solution(verified if verified.success else None, run_dir / "best_solution.csv")
    _write_json(
        run_dir / "best_parameters.json",
        {
            "unit_vector": [float(value) for value in optimizer.x],
            "parameters": best_sample,
            "active_parameter_specs": [asdict(spec) for spec in verified_specs],
            "solver_result": result_row(verified),
        },
    )

    complete = (
        int(optimizer.nfev) == evaluation_budget
        and len(records) == evaluation_budget
        and verified.success
        and math.isfinite(verified.chi2)
    )
    payload = {
        "complete": complete,
        "agent": rep["agent"],
        "proposal": proposal,
        "replicate": replicate,
        "seed": seed,
        "batch_lag_id": lag_id,
        "headline_chi2": rep["headline_chi2"],
        "headline_AIC": rep["headline_aic"],
        "headline_k": rep["headline_k"],
        "algorithm": "scipy.optimize.differential_evolution",
        "strategy": "best1bin",
        "parameter_space": "normalized unit cube mapped to ai_theory_lab.config_p broad priors",
        "historical_parameter_seeding": False,
        "agent_memory": False,
        "local_polish": False,
        "population_size": population_size,
        "generations": generations,
        "evaluation_budget": evaluation_budget,
        "optimizer_nfev": int(optimizer.nfev),
        "optimizer_nit": int(optimizer.nit),
        "optimizer_message": str(optimizer.message),
        "optimizer_reported_success": bool(optimizer.success),
        "workers": workers,
        "active_parameters": [spec.name for spec in specs],
        "active_dimensions": dimensions,
        "best_chi2": float(verified.chi2) if verified.success else None,
        "best_AIC": float(verified.aic) if verified.success else None,
        "best_BIC": float(verified.bic) if verified.success else None,
        "k_params": int(verified.k_params) if verified.success else None,
        "delta_AIC_from_headline": (
            float(verified.aic) - float(rep["headline_aic"])
            if verified.success else None
        ),
        "elapsed_seconds": elapsed,
        **evaluation_stats,
    }
    _write_json(status_path, payload)
    print(status_path)
    if not complete:
        raise RuntimeError(f"DE task did not satisfy the fixed-budget contract: {payload}")
    return payload


def _quantile(values: Sequence[float], q: float) -> float | None:
    if not values:
        return None
    return float(np.quantile(np.asarray(values, dtype=float), q))


def summarize_de_results(
    output_root: Path,
    *,
    expected_replicates: int = DEFAULT_REPLICATES,
    allow_incomplete: bool = False,
) -> Dict[str, Any]:
    prepared = _read_json(output_root / "inputs" / "prepared_manifest.json")
    replicate_rows: List[Dict[str, Any]] = []
    missing: List[str] = []
    for rep in prepared["representatives"]:
        proposal = str(rep["proposal"])
        for replicate in range(1, expected_replicates + 1):
            path = output_root / "runs" / proposal / f"replicate_{replicate:02d}" / "result.json"
            if not path.exists():
                missing.append(f"{proposal}:{replicate}")
                continue
            row = _read_json(path)
            if not row.get("complete"):
                missing.append(f"{proposal}:{replicate}")
                continue
            replicate_rows.append(row)
    if missing and not allow_incomplete:
        raise RuntimeError(f"Missing or incomplete DE tasks: {', '.join(missing)}")

    summary_rows: List[Dict[str, Any]] = []
    for rep in prepared["representatives"]:
        proposal = str(rep["proposal"])
        rows = [row for row in replicate_rows if row["proposal"] == proposal]
        aic = [float(row["best_AIC"]) for row in rows]
        chi2 = [float(row["best_chi2"]) for row in rows]
        headline_aic = float(rep["headline_aic"])
        summary_rows.append(
            {
                "agent": rep["agent"],
                "proposal": proposal,
                "headline_AIC": headline_aic,
                "completed_replicates": len(rows),
                "expected_replicates": expected_replicates,
                "DE_AIC_mean": statistics.mean(aic) if aic else None,
                "DE_AIC_sd": _sample_sd(aic) if aic else None,
                "DE_AIC_median": statistics.median(aic) if aic else None,
                "DE_AIC_p16": _quantile(aic, 0.16),
                "DE_AIC_p84": _quantile(aic, 0.84),
                "DE_AIC_min": min(aic) if aic else None,
                "DE_AIC_max": max(aic) if aic else None,
                "DE_chi2_mean": statistics.mean(chi2) if chi2 else None,
                "DE_chi2_sd": _sample_sd(chi2) if chi2 else None,
                "fraction_beating_headline": (
                    sum(value <= headline_aic for value in aic) / len(aic) if aic else None
                ),
                "fraction_within_0p1_of_headline": (
                    sum(value <= headline_aic + 0.1 for value in aic) / len(aic) if aic else None
                ),
                "mean_acceptance_fraction": (
                    statistics.mean(float(row["acceptance_fraction"]) for row in rows)
                    if rows else None
                ),
                "mean_elapsed_seconds": (
                    statistics.mean(float(row["elapsed_seconds"]) for row in rows)
                    if rows else None
                ),
            }
        )

    summary_dir = output_root / "summary"
    _write_csv(summary_dir / "de_replicates.csv", replicate_rows)
    _write_csv(summary_dir / "fixed7_de_summary.csv", summary_rows)
    payload = {
        "experiment": "fixed7_de_20x5000_v1",
        "missing_or_incomplete": missing,
        "rows": summary_rows,
    }
    _write_json(summary_dir / "fixed7_de_summary.json", payload)

    markdown = [
        "# Fixed-Lagrangian Differential Evolution baseline",
        "",
        "Each row summarizes 20 independent DE/best/1/bin optimizations of a fixed",
        "serialized Lagrangian.  Every optimization uses 5000 real Solver evaluations,",
        "the broad cold-start bounds, and no agent memory or historical parameter seed.",
        "",
        "| Agent | Proposal | Agent AIC | DE AIC mean +/- SD | median [16%,84%] | DE best | <= agent | within 0.1 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        if row["DE_AIC_mean"] is None:
            markdown.append(
                f"| {row['agent']} | {row['proposal']} | {row['headline_AIC']:.6f} | -- | -- | -- | -- | -- |"
            )
            continue
        markdown.append(
            f"| {row['agent']} | {row['proposal']} | {row['headline_AIC']:.6f} "
            f"| {row['DE_AIC_mean']:.6f} +/- {row['DE_AIC_sd']:.6f} "
            f"| {row['DE_AIC_median']:.6f} [{row['DE_AIC_p16']:.6f},{row['DE_AIC_p84']:.6f}] "
            f"| {row['DE_AIC_min']:.6f} | {100*row['fraction_beating_headline']:.1f}% "
            f"| {100*row['fraction_within_0p1_of_headline']:.1f}% |"
        )
    (summary_dir / "summary.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")

    latex = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Fixed-Lagrangian Differential-Evolution ablation. Each DE run uses 5000 real likelihood evaluations from the same broad parameter bounds, without agent memory, historical best-fit initialization, or local polishing. The uncertainty is the sample standard deviation across 20 optimizer seeds, not an observational uncertainty.}",
        r"\label{tab:fixed-lagrangian-de}",
        r"\small",
        r"\setlength{\tabcolsep}{5pt}",
        r"\begin{ruledtabular}",
        r"\begin{tabular}{llrrrrr}",
        r"Agent & Proposal & Agent AIC & DE AIC $\langle\min\rangle\pm s$ & DE best & Beat agent (\%) & Within 0.1 (\%) \\",
        r"\hline",
    ]
    for row in summary_rows:
        if row["DE_AIC_mean"] is None:
            result = best = beat = near = "--"
        else:
            result = f"${row['DE_AIC_mean']:.4f} \\pm {row['DE_AIC_sd']:.4f}$"
            best = f"{row['DE_AIC_min']:.4f}"
            beat = f"{100*row['fraction_beating_headline']:.1f}"
            near = f"{100*row['fraction_within_0p1_of_headline']:.1f}"
        latex.append(
            f"{row['agent']} & {row['proposal']} & {row['headline_AIC']:.4f} & "
            f"{result} & {best} & {beat} & {near} \\\\"
        )
    latex.extend([r"\end{tabular}", r"\end{ruledtabular}", r"\end{table*}"])
    (summary_dir / "paper_table.tex").write_text("\n".join(latex) + "\n", encoding="utf-8")
    print(summary_dir)
    return payload


def prepare_de_experiment(
    manifest_path: Path,
    source_root: Path,
    output_root: Path,
    *,
    force: bool = False,
) -> Dict[str, Any]:
    prepared = prepare_experiment(
        manifest_path,
        source_root,
        output_root,
        force=force,
    )
    contract = dict(prepared.get("sampling_contract") or {})
    contract.update(
        {
            "replicates": DEFAULT_REPLICATES,
            "evaluations_per_lagrangian": DEFAULT_EVALUATION_BUDGET,
            "algorithm": "DE/best/1/bin",
            "population_size": DEFAULT_POPULATION_SIZE,
            "generations": DEFAULT_EVALUATION_BUDGET // DEFAULT_POPULATION_SIZE - 1,
            "mutation": list(DEFAULT_MUTATION),
            "recombination": DEFAULT_RECOMBINATION,
            "initialization": "Latin hypercube over normalized broad-prior coordinates",
            "historical_parameter_seeding": False,
            "agent_memory": False,
            "local_polish": False,
        }
    )
    prepared["experiment_id"] = "fixed7_de_20x5000_v1"
    prepared["sampling_contract"] = contract
    _write_json(output_root / "inputs" / "prepared_manifest.json", prepared)
    return prepared


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--source-root", type=Path, default=ROOT / "ai_theory_lab" / "runs")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Build the shared seven-model cache")
    prepare.add_argument("--force", action="store_true")

    run = subparsers.add_parser("run", help="Run one proposal/seed DE optimization")
    selection = run.add_mutually_exclusive_group(required=True)
    selection.add_argument("--task-index", type=int)
    selection.add_argument("--proposal")
    run.add_argument("--replicate", type=int)
    run.add_argument("--evaluations", type=int, default=DEFAULT_EVALUATION_BUDGET)
    run.add_argument("--population-size", type=int, default=DEFAULT_POPULATION_SIZE)
    run.add_argument("--workers", type=int, default=8)
    run.add_argument("--force", action="store_true")

    summarize = subparsers.add_parser("summarize", help="Summarize the 140 DE tasks")
    summarize.add_argument("--expected-replicates", type=int, default=DEFAULT_REPLICATES)
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

    if args.command == "prepare":
        prepared = prepare_de_experiment(
            manifest_path,
            source_root,
            output_root,
            force=args.force,
        )
        print(output_root / "inputs" / "prepared_manifest.json")
        print(f"prepared_representatives={len(prepared['representatives'])}")
        return 0
    if args.command == "run":
        manifest = _read_json(manifest_path)
        proposals = [str(rep["proposal"]) for rep in _representatives(manifest)]
        if args.task_index is not None:
            proposal, replicate = task_index_to_selection(args.task_index, proposals)
        else:
            proposal = str(args.proposal)
            if args.replicate is None:
                raise ValueError("--replicate is required when --proposal is used")
            replicate = int(args.replicate)
        run_de_optimization(
            output_root,
            proposal,
            replicate,
            evaluation_budget=args.evaluations,
            population_size=args.population_size,
            workers=args.workers,
            force=args.force,
        )
        return 0
    if args.command == "summarize":
        summarize_de_results(
            output_root,
            expected_replicates=args.expected_replicates,
            allow_incomplete=args.allow_incomplete,
        )
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
