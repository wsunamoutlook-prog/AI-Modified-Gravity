#!/usr/bin/env python3
"""Audit every parent theory in a completed scalaron discovery run.

The audit is read-only.  It merges initial/expanded/refine attempts by
``structure_trial_id``, checks serialized scalaron metadata and AIC bookkeeping,
and can replay the best accepted sample with the Solver identifiability audit.
It never reruns the theory proposal agent or a parameter scan.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import Counter, defaultdict
import json
import math
import os
from pathlib import Path
import re
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN = "cmp250_openai_gpt_5_6_sol_scalaron_openonly_aic_v1"
_WORKER_LIKELIHOOD: tuple[dict[str, Any], dict[str, Any]] | None = None


def _finite(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _as_float(value: Any) -> float | None:
    return float(value) if _finite(value) else None


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"Expected a JSON object: {path}")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise TypeError(f"Expected an object at {path}:{line_number}")
        records.append(value)
    return records


def _resolve_record_path(raw: Any, fallback_dir: Path) -> Path | None:
    if not raw:
        return None
    path = Path(str(raw)).expanduser()
    if path.is_file() or path.is_dir():
        return path
    fallback = fallback_dir / path.name
    return fallback if fallback.exists() else path


def _proposal_path(record: dict[str, Any], proposal_dir: Path) -> Path | None:
    attached = record.get("agent_lagrangian") or {}
    raw = attached.get("proposal_path") or record.get("proposal_path")
    resolved = _resolve_record_path(raw, proposal_dir)
    if resolved is not None and resolved.is_file():
        return resolved
    trial_id = str(record.get("structure_trial_id") or record.get("loop_id") or "")
    stage = str(record.get("validation_stage") or "initial")
    for name in (
        f"{trial_id}_{stage}.json",
        f"{trial_id}.json",
    ):
        candidate = proposal_dir / name
        if candidate.is_file():
            return candidate
    return resolved


def _solver_output_path(record: dict[str, Any], runs_root: Path) -> Path | None:
    raw = record.get("solver_output_dir")
    if not raw:
        return None
    path = Path(str(raw)).expanduser()
    if path.is_dir():
        return path
    # Downloaded archives may retain only the task directory basename.
    parts = path.parts
    task_name = next((part for part in parts if part.startswith("cmp") or part.startswith("agent_")), "")
    if task_name:
        candidate = runs_root / task_name / "agent_solver_result" / "agent_solve"
        if candidate.is_dir():
            return candidate
    return path


def _normalize_factor(value: str) -> str:
    normalized = value.strip().replace(" ", "")
    replacements = {
        r"\phi_1": "phi1",
        r"\phi_2": "phi2",
        "phi_1": "phi1",
        "phi_2": "phi2",
        "φ1": "phi1",
        "φ2": "phi2",
    }
    return replacements.get(normalized, normalized)


def classify_operator_labels(labels: Iterable[str]) -> dict[str, Any]:
    """Reproduce the exact algebraic-R classification from serialized labels."""

    label_list = list(labels)
    algebraic: list[int] = []
    nonlinear: list[int] = []
    for index, label in enumerate(label_list):
        factors = [_normalize_factor(part) for part in str(label).split("·")]
        if factors and all(part in {"phi1", "phi2", "R"} for part in factors):
            r_power = factors.count("R")
            if r_power:
                algebraic.append(index)
            if r_power >= 2:
                nonlinear.append(index)
    if not nonlinear:
        classification = "ordinary"
    else:
        residual = [index for index in range(len(label_list)) if index not in algebraic]
        classification = "hybrid" if residual else "scalarizable"
    return {
        "enabled": bool(nonlinear),
        "classification": classification,
        "algebraic_term_indices": algebraic,
        "nonlinear_term_indices": nonlinear,
    }


def _scalar_config_issues(scalar_config: str, labels: list[str]) -> list[str]:
    joined = "+".join(labels)
    has_phi1 = "φ1" in joined or "phi1" in joined or r"\phi_1" in joined
    has_phi2 = "φ2" in joined or "phi2" in joined or r"\phi_2" in joined
    issues: list[str] = []
    if scalar_config == "none" and (has_phi1 or has_phi2):
        issues.append("operator fields conflict with scalar_config=none")
    if scalar_config == "phi1_only" and has_phi2:
        issues.append("phi2 operator appears in phi1_only theory")
    if scalar_config == "phi2_only" and has_phi1:
        issues.append("phi1 operator appears in phi2_only theory")
    return issues


def _metadata_issues(proposal: dict[str, Any], record: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    theory = proposal.get("theory") or {}
    operators = theory.get("operators") or []
    labels = [str(item.get("candidate") or "") for item in operators if isinstance(item, dict)]
    declared = theory.get("scalaron") or {}
    computed = classify_operator_labels(labels)
    issues: list[str] = []
    for key in ("enabled", "classification", "algebraic_term_indices", "nonlinear_term_indices"):
        if declared.get(key) != computed[key]:
            issues.append(
                f"scalaron {key} mismatch: declared={declared.get(key)!r}, computed={computed[key]!r}"
            )
    scalar_config = str(theory.get("scalar_config") or (record.get("theory") or {}).get("scalar_config") or "")
    issues.extend(_scalar_config_issues(scalar_config, labels))
    track = str(theory.get("theory_track") or record.get("theory_track") or "")
    if track == "eh_anchored" and "R" not in labels:
        issues.append("eh_anchored theory has no Einstein-Hilbert R operator")
    return {
        "labels": labels,
        "scalar_config": scalar_config,
        "potential_types": theory.get("potential_types") or {},
        "theory_track": track,
        "declared_scalaron": declared,
        "computed_scalaron": computed,
    }, issues


def _bookkeeping_issues(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    chi2 = _as_float(record.get("chi2"))
    aic = _as_float(record.get("aic"))
    k_raw = record.get("k_params")
    names = [str(name) for name in record.get("k_parameter_names") or []]
    if chi2 is None and aic is not None:
        issues.append("finite AIC is present without finite chi2")
    if chi2 is not None and aic is None:
        issues.append("finite chi2 is present without finite AIC")
    if chi2 is not None and aic is not None:
        try:
            k = int(k_raw)
        except (TypeError, ValueError):
            issues.append("finite fit has no integer k_params")
        else:
            expected = chi2 + 2.0 * k
            if not math.isclose(aic, expected, rel_tol=0.0, abs_tol=5e-5):
                issues.append(f"AIC bookkeeping mismatch: AIC={aic:.8g}, chi2+2k={expected:.8g}")
            if names and len(names) != k:
                issues.append(f"k_params={k} but {len(names)} parameter names were recorded")
            for required in ("Omega_m0", "M_SN", "alpha_BAO"):
                if names and required not in names:
                    issues.append(f"required likelihood direction {required} is missing from k")
    if bool(record.get("validated")) != (chi2 is not None and aic is not None):
        issues.append("validated flag is inconsistent with finite fit statistics")
    return issues


def _best_record(records: list[dict[str, Any]]) -> dict[str, Any]:
    finite = [record for record in records if _finite(record.get("aic"))]
    if finite:
        return min(finite, key=lambda record: (float(record["aic"]), float(record.get("chi2") or math.inf)))
    stage_order = {"initial": 0, "expanded": 1, "refine": 2, "final": 2}
    return max(records, key=lambda record: stage_order.get(str(record.get("validation_stage")), -1))


def _read_best_sample(solver_output: Path) -> tuple[dict[str, float], dict[str, str]]:
    candidates = [
        solver_output / "accepted_samples_summary.csv",
        solver_output / "accepted_samples_summary_partial.csv",
    ]
    path = next((candidate for candidate in candidates if candidate.is_file()), None)
    if path is None:
        raise FileNotFoundError(f"accepted sample summary not found under {solver_output}")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    finite_rows = [row for row in rows if _finite(row.get("chi2"))]
    if not finite_rows:
        raise ValueError(f"no finite accepted samples in {path}")
    row = min(finite_rows, key=lambda item: (float(item["chi2"]), float(item.get("AIC") or math.inf)))
    sample: dict[str, float] = {}
    for key, value in row.items():
        if _finite(value):
            sample[str(key)] = float(value)
    return sample, row


def _audit_one_best(payload: dict[str, Any]) -> dict[str, Any]:
    """Worker-safe replay of one historical best sample."""

    os.environ["SOLVER_IDENTIFIABILITY_MODE"] = "report"
    os.environ.setdefault("SOLVER_MAKE_PLOTS", "0")
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/modify_gr_matplotlib")
    from solver_v5_2.core import _scan_single_model_worker, load_current_likelihood_data
    from solver_v5_2.runner import _load_built_models_cache

    solver_output = Path(payload["solver_output"])
    task_dir = solver_output.parents[1]
    cache_path = task_dir / "agent_built_models_cache.pkl"
    if not cache_path.is_file():
        raise FileNotFoundError(cache_path)
    models, _metadata = _load_built_models_cache(cache_path)
    sample, old_row = _read_best_sample(solver_output)
    old_lag_id = str(old_row.get("lag_id") or payload.get("best_lag_id") or "1")
    model = next((item for item in models if str(item.lag_id) == old_lag_id), None)
    if model is None:
        if len(models) != 1:
            raise LookupError(f"lag_id={old_lag_id} missing from {cache_path}")
        model = models[0]
    global _WORKER_LIKELIHOOD
    if _WORKER_LIKELIHOOD is None:
        _WORKER_LIKELIHOOD = load_current_likelihood_data()
    sn_data, bao_data = _WORKER_LIKELIHOOD
    output = _scan_single_model_worker(
        (model, "eft", 1, 17, 0, sn_data, bao_data, [sample])
    )
    best = output.get("best")
    if best is None:
        rejects = output.get("rejects") or {}
        raise RuntimeError(f"historical best sample no longer accepts: {rejects}")
    audit = dict(output.get("identifiability_audit") or {})
    old_chi2 = float(payload["chi2"])
    audit.update({
        "replayed_chi2": float(best.chi2),
        "historical_chi2": old_chi2,
        "replay_delta_chi2": float(best.chi2) - old_chi2,
        "current_k_nominal": int(best.k_params_nominal or best.k_params),
        "current_k_parameter_names": list(best.k_parameter_names or []),
        "aic_identifiable": float(best.aic_identifiable or best.aic),
    })
    return audit


@dataclass
class TrialAudit:
    trial_id: str
    best_record: dict[str, Any]
    stages: list[str]
    proposal_path: Path | None
    structural: dict[str, Any]
    issues: list[str]
    identifiability: dict[str, Any] | None = None


def _initial_trial_audits(
    records: list[dict[str, Any]], proposal_dir: Path
) -> list[TrialAudit]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        trial_id = str(record.get("structure_trial_id") or record.get("loop_id") or "")
        if not trial_id:
            raise ValueError("attempt record has no structure_trial_id or loop_id")
        grouped[trial_id].append(record)

    audits: list[TrialAudit] = []
    for trial_id, trial_records in grouped.items():
        best = _best_record(trial_records)
        path = _proposal_path(best, proposal_dir)
        issues = _bookkeeping_issues(best)
        structural: dict[str, Any] = {
            "labels": list((best.get("theory") or {}).get("operators") or []),
            "scalar_config": str((best.get("theory") or {}).get("scalar_config") or ""),
            "potential_types": (best.get("theory") or {}).get("potential_types") or {},
            "theory_track": str(best.get("theory_track") or ""),
            "declared_scalaron": {},
            "computed_scalaron": {},
        }
        if path is None or not path.is_file():
            issues.append(f"proposal JSON is missing: {path}")
        else:
            try:
                structural, metadata_issues = _metadata_issues(_read_json(path), best)
                issues.extend(metadata_issues)
            except Exception as exc:
                issues.append(f"proposal JSON could not be audited: {type(exc).__name__}: {exc}")
        stages = [str(record.get("validation_stage") or "unknown") for record in trial_records]
        audits.append(TrialAudit(trial_id, best, stages, path, structural, issues))
    return sorted(audits, key=lambda audit: _natural_key(audit.trial_id))


def _natural_key(value: str) -> tuple[Any, ...]:
    return tuple(int(part) if part.isdigit() else part for part in re.split(r"(\d+)", value))


def _verdict(audit: TrialAudit) -> tuple[str, str]:
    if audit.issues:
        return "inconsistent", "; ".join(audit.issues)
    record = audit.best_record
    if not _finite(record.get("aic")):
        reasons = [
            str(reason)
            for reason in record.get("failure_tags") or []
            if str(reason) != "no_accepted_samples"
        ]
        top_reasons = record.get("top_reject_reasons") or []
        failed_stage = str(record.get("failed_stage") or "unknown")
        if not reasons and not top_reasons:
            return (
                "rejection_diagnostic_incomplete",
                f"no finite sample at {failed_stage}, but no underlying rejection reason was retained",
            )
        return "reasonable_rejection", f"rejected at {failed_stage}: {','.join(reasons) or 'recorded deterministic failure'}"
    ident = audit.identifiability
    if ident is None:
        return "rank_not_run", "finite fit is internally consistent; identifiability replay was not run"
    if ident.get("error"):
        return "rank_replay_failed", str(ident["error"])
    delta = abs(float(ident.get("replay_delta_chi2") or 0.0))
    if delta > 1e-3:
        return "rank_replay_mismatch", f"best point replay changed chi2 by {delta:.3g}"
    nominal = int(ident.get("current_k_nominal", record.get("k_params") or 0))
    identifiable = int(ident.get("k_identifiable", nominal))
    if identifiable < nominal:
        return "reasonable_fit_k_reduced", f"fit reproduces; identifiable k={identifiable} instead of nominal k={nominal}"
    return "reasonable_fit", "fit reproduces and no rank loss is resolved at the configured threshold"


def _csv_row(audit: TrialAudit) -> dict[str, Any]:
    record = audit.best_record
    structural = audit.structural
    declared = structural.get("declared_scalaron") or {}
    computed = structural.get("computed_scalaron") or {}
    ident = audit.identifiability or {}
    verdict, explanation = _verdict(audit)
    return {
        "trial_id": audit.trial_id,
        "stages": ";".join(audit.stages),
        "best_stage": record.get("validation_stage"),
        "validated": bool(record.get("validated")),
        "failed_stage": record.get("failed_stage"),
        "scalar_config": structural.get("scalar_config"),
        "potential_types": json.dumps(structural.get("potential_types") or {}, ensure_ascii=False, sort_keys=True),
        "theory_track": structural.get("theory_track"),
        "operator_count": len(structural.get("labels") or []),
        "operators": " + ".join(structural.get("labels") or []),
        "scalaron_enabled": declared.get("enabled"),
        "scalaron_classification": declared.get("classification"),
        "computed_scalaron_enabled": computed.get("enabled"),
        "computed_scalaron_classification": computed.get("classification"),
        "chi2": record.get("chi2"),
        "AIC": record.get("aic"),
        "k_historical": record.get("k_params"),
        "k_names_historical": ";".join(map(str, record.get("k_parameter_names") or [])),
        "replayed_chi2": ident.get("replayed_chi2"),
        "replay_delta_chi2": ident.get("replay_delta_chi2"),
        "k_nominal_current": ident.get("current_k_nominal"),
        "k_identifiable": ident.get("k_identifiable"),
        "AIC_identifiable": ident.get("aic_identifiable"),
        "identifiability_status": ident.get("status"),
        "condition_number": ident.get("condition_number"),
        "null_combinations": json.dumps(ident.get("null_combinations") or [], sort_keys=True),
        "unresolved_parameters": ";".join(map(str, ident.get("unresolved_parameter_names") or [])),
        "failure_tags": ";".join(map(str, record.get("failure_tags") or [])),
        "top_reject_reasons_json": json.dumps(
            record.get("top_reject_reasons") or [], ensure_ascii=False, sort_keys=True
        ),
        "verdict": verdict,
        "explanation": explanation,
        "proposal_path": str(audit.proposal_path or ""),
        "solver_output_dir": str(record.get("solver_output_dir") or ""),
    }


def _write_outputs(output_dir: Path, run: str, audits: list[TrialAudit]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [_csv_row(audit) for audit in audits]
    csv_path = output_dir / "per_theory_audit.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["trial_id"])
        writer.writeheader()
        writer.writerows(rows)

    verdict_counts = Counter(row["verdict"] for row in rows)
    scalaron_counts = Counter(
        str(row["scalaron_classification"] or "missing") for row in rows
    )
    payload = {
        "run": run,
        "trial_count": len(rows),
        "verdict_counts": dict(verdict_counts),
        "scalaron_classification_counts": dict(scalaron_counts),
        "rows": rows,
    }
    (output_dir / "per_theory_audit.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        f"# Scalaron run audit: {run}",
        "",
        f"Parent theories audited: **{len(rows)}**",
        "",
        "## Verdict counts",
        "",
    ]
    for verdict, count in sorted(verdict_counts.items()):
        lines.append(f"- `{verdict}`: {count}")
    lines.extend(["", "## Scalaron classification", ""])
    for classification, count in sorted(scalaron_counts.items()):
        lines.append(f"- `{classification}`: {count}")
    lines.extend([
        "",
        "## Per-theory review",
        "",
        "| Trial | Stage | Scalaron | AIC | k old | k rank | Verdict | Explanation |",
        "|---|---|---|---:|---:|---:|---|---|",
    ])
    for row in rows:
        aic = "" if row["AIC"] is None else f"{float(row['AIC']):.4f}"
        lines.append(
            "| {trial_id} | {best_stage} | {scalaron_classification} | {aic} | "
            "{k_historical} | {k_identifiable} | `{verdict}` | {explanation} |".format(
                **row, aic=aic
            )
        )
    (output_dir / "audit_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def audit_run(args: argparse.Namespace) -> int:
    run = args.run
    proposal_dir = args.proposal_root / run
    memory_dir = args.memory_root / run
    history_path = memory_dir / "attempt_history.jsonl"
    if not history_path.is_file():
        raise FileNotFoundError(history_path)
    audits = _initial_trial_audits(_read_jsonl(history_path), proposal_dir)
    if args.expect_trials and len(audits) != args.expect_trials:
        raise RuntimeError(
            f"Expected {args.expect_trials} parent theories, found {len(audits)}. "
            "Refusing to label an incomplete run as fully audited."
        )

    replay_payloads: dict[str, dict[str, Any]] = {}
    if not args.skip_identifiability:
        for audit in audits:
            record = audit.best_record
            if not _finite(record.get("aic")):
                continue
            solver_output = _solver_output_path(record, args.runs_root)
            if solver_output is None or not solver_output.is_dir():
                audit.identifiability = {
                    "error": f"solver output directory is missing: {solver_output}"
                }
                continue
            replay_payloads[audit.trial_id] = {
                "solver_output": str(solver_output),
                "chi2": float(record["chi2"]),
                "best_lag_id": record.get("best_lag_id"),
            }

    if replay_payloads:
        if args.workers <= 1:
            for audit in audits:
                payload = replay_payloads.get(audit.trial_id)
                if payload is None:
                    continue
                try:
                    audit.identifiability = _audit_one_best(payload)
                except Exception as exc:
                    audit.identifiability = {"error": f"{type(exc).__name__}: {exc}"}
        else:
            by_trial = {audit.trial_id: audit for audit in audits}
            with ProcessPoolExecutor(max_workers=args.workers) as executor:
                futures = {
                    executor.submit(_audit_one_best, payload): trial_id
                    for trial_id, payload in replay_payloads.items()
                }
                for future in as_completed(futures):
                    trial_id = futures[future]
                    try:
                        by_trial[trial_id].identifiability = future.result()
                    except Exception as exc:
                        by_trial[trial_id].identifiability = {
                            "error": f"{type(exc).__name__}: {exc}"
                        }

    _write_outputs(args.output_dir, run, audits)
    counts = Counter(_verdict(audit)[0] for audit in audits)
    print(f"audited={len(audits)} output={args.output_dir}")
    print("verdicts=" + json.dumps(dict(sorted(counts.items())), sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", default=DEFAULT_RUN)
    parser.add_argument("--proposal-root", type=Path, default=ROOT / "ai_theory_lab" / "proposals")
    parser.add_argument("--memory-root", type=Path, default=ROOT / "ai_theory_lab" / "memory")
    parser.add_argument("--runs-root", type=Path, default=ROOT / "ai_theory_lab" / "runs")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--expect-trials", type=int, default=250)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--skip-identifiability", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be at least 1")
    if args.output_dir is None:
        args.output_dir = ROOT / "ai_theory_lab" / "reports" / args.run / "scalaron_run_audit"
    return audit_run(args)


if __name__ == "__main__":
    raise SystemExit(main())
