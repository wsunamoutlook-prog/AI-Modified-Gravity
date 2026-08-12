"""Compare discovery runs across LLM providers.

This script reads the reproducible local artifacts written by graph_agent_batch:

* ai_theory_lab/memory/<run>/attempt_history.jsonl
* ai_theory_lab/proposals/<run>/scheduler_tasks.jsonl
* ai_theory_lab/proposals/<run>/task_*.json / wave_*.json for legacy runs

It is intentionally independent of LangSmith. LangSmith can monitor a live run,
but paper tables should be generated from these local artifacts.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


DEFAULT_CHI2_CAP = 10000.0
GLOBAL_THRESHOLD = 1650.0
NEW_PHYSICS_THRESHOLD = 2000.0


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return value if isinstance(value, dict) else None


def _float(value: Any) -> float | None:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def _parse_timestamp(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value)
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S%z"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _timestamp_sort_value(value: Any) -> float:
    timestamp = _parse_timestamp(value)
    if timestamp is None:
        return float("inf")
    return timestamp.timestamp()


def _stage_of(row: dict[str, Any]) -> str:
    stage = row.get("validation_stage")
    if stage:
        return str(stage)
    loop_id = str(row.get("loop_id") or "")
    if "_refine_" in loop_id or "_expanded_refine_" in loop_id:
        return "refine"
    if "_expanded_" in loop_id:
        return "expanded"
    return "initial"


def _theory(row: dict[str, Any]) -> dict[str, Any]:
    theory = row.get("theory")
    return theory if isinstance(theory, dict) else {}


def _group(row: dict[str, Any]) -> str:
    theory = _theory(row)
    return str(row.get("proposal_group") or theory.get("proposal_group") or "unknown")


def _track(row: dict[str, Any]) -> str:
    theory = _theory(row)
    return str(row.get("theory_track") or theory.get("theory_track") or "unknown")


def _scalar(row: dict[str, Any]) -> str:
    return str(_theory(row).get("scalar_config") or "unknown")


def _family_key(row: dict[str, Any]) -> str:
    if row.get("family_key"):
        return str(row["family_key"])
    theory = _theory(row)
    payload = {
        "scalar_config": theory.get("scalar_config"),
        "potential_types": theory.get("potential_types"),
        "operators": theory.get("operators") or [],
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _accepted(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if row.get("validated") and _float(row.get("chi2")) is not None]


def _chis(rows: Iterable[dict[str, Any]]) -> list[float]:
    values = [_float(row.get("chi2")) for row in rows]
    return [value for value in values if value is not None]


def _best(rows: Iterable[dict[str, Any]]) -> float | None:
    values = _chis(rows)
    return min(values) if values else None


def _median(rows: Iterable[dict[str, Any]]) -> float | None:
    values = sorted(_chis(rows))
    return statistics.median(values) if values else None


def _wall_seconds(events: list[dict[str, Any]], rows: list[dict[str, Any]]) -> float | None:
    elapsed = 0.0
    segment_start: datetime | None = None
    segment_last: datetime | None = None
    for event in events:
        timestamp = _parse_timestamp(event.get("timestamp"))
        if timestamp is None:
            continue
        if event.get("event") in {"scheduler_start", "scheduler_resume"}:
            if segment_start is not None and segment_last is not None:
                elapsed += max(0.0, (segment_last - segment_start).total_seconds())
            segment_start = timestamp
        segment_last = timestamp
    if segment_start is not None and segment_last is not None:
        elapsed += max(0.0, (segment_last - segment_start).total_seconds())
    if elapsed > 0.0:
        return elapsed
    timestamps = [_parse_timestamp(row.get("timestamp")) for row in rows]
    timestamps = [ts for ts in timestamps if ts is not None]
    if len(timestamps) >= 2:
        return max(0.0, (max(timestamps) - min(timestamps)).total_seconds())
    return None


def _latest_progress(events: list[dict[str, Any]]) -> dict[str, Any]:
    if not events:
        return {}
    complete = next((event for event in reversed(events) if event.get("event") == "scheduler_complete"), None)
    latest = events[-1]
    return {
        "target_attempts": latest.get("target_attempts"),
        "submitted_total": latest.get("submitted_total"),
        "recorded_total": latest.get("recorded_total"),
        "expanded_recorded_total": latest.get("expanded_recorded_total"),
        "refine_recorded_total": latest.get("refine_recorded_total"),
        "failed_total": latest.get("failed_total"),
        "latest_event": latest.get("event"),
        "latest_timestamp": latest.get("timestamp"),
        "scheduler_complete": bool(complete),
    }


def _proposal_stats_from_events(
    events: list[dict[str, Any]],
    *,
    proposal_json_count: int,
    debug_file_count: int,
) -> dict[str, Any] | None:
    submitted: dict[str, dict[str, Any]] = {}
    for index, event in enumerate(events):
        if event.get("event") != "submitted":
            continue
        if str(event.get("validation_stage") or "initial") != "initial":
            continue
        task_id = str(event.get("task_id") or f"event_{index}")
        submitted.setdefault(task_id, event)
    if not submitted:
        return None

    provider_counts: Counter[str] = Counter()
    model_counts: Counter[str] = Counter()
    proposal_mode_counts: Counter[str] = Counter()
    latencies: list[float] = []
    for event in submitted.values():
        provider = event.get("llm_provider")
        model = event.get("llm_model")
        proposal_mode = event.get("proposal_mode")
        if provider:
            provider_counts[str(provider)] += 1
        if model:
            model_counts[str(model)] += 1
        if proposal_mode:
            proposal_mode_counts[str(proposal_mode)] += 1
        latency = _float(event.get("llm_latency_sec"))
        if latency is not None:
            latencies.append(latency)

    # Scheduler events intentionally omit prompt bodies, token usage, and retry
    # details. Keep those fields unavailable instead of parsing multi-megabyte
    # proposal JSON files or reporting a misleading zero.
    return {
        "proposal_json_count": proposal_json_count,
        "llm_successful_proposal_count": len(submitted),
        "llm_api_call_count": None,
        "llm_provider": provider_counts.most_common(1)[0][0] if provider_counts else None,
        "llm_model": model_counts.most_common(1)[0][0] if model_counts else None,
        "llm_provider_counts": dict(provider_counts),
        "llm_model_counts": dict(model_counts),
        "proposal_mode_counts": dict(proposal_mode_counts),
        "llm_retry_error_count": None,
        "llm_retry_attempt_count": None,
        "llm_retry_stats_available": False,
        "mean_llm_latency_sec": statistics.mean(latencies) if latencies else None,
        "median_llm_latency_sec": statistics.median(latencies) if latencies else None,
        "llm_input_tokens": None,
        "llm_output_tokens": None,
        "llm_total_tokens": None,
        "llm_debug_failure_files": debug_file_count,
        "proposal_stats_source": "scheduler_tasks.jsonl",
    }


def _proposal_stats(run_name: str, events: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    proposal_dir = Path("ai_theory_lab") / "proposals" / run_name
    files = sorted(proposal_dir.glob("task_*.json")) + sorted(proposal_dir.glob("wave_*.json"))
    initial_files = [
        path
        for path in files
        if "_expanded" not in path.stem and "_refine" not in path.stem
    ]
    debug_files = list((proposal_dir / "llm_proposal_debug").glob("*.json")) if proposal_dir.exists() else []
    event_stats = _proposal_stats_from_events(
        events or [],
        proposal_json_count=len(files),
        debug_file_count=len(debug_files),
    )
    if event_stats is not None:
        return event_stats

    provider_counts: Counter[str] = Counter()
    model_counts: Counter[str] = Counter()
    proposal_mode_counts: Counter[str] = Counter()
    retry_errors = 0
    retry_attempts = 0
    latencies: list[float] = []
    usage_input = 0
    usage_output = 0
    usage_total = 0

    for path in initial_files:
        data = _read_json(path)
        if not data:
            continue
        provider = data.get("llm_provider")
        model = data.get("llm_model")
        if provider:
            provider_counts[str(provider)] += 1
        if model:
            model_counts[str(model)] += 1
        proposal_mode = data.get("proposal_mode")
        if proposal_mode:
            proposal_mode_counts[str(proposal_mode)] += 1
        latency = _float(data.get("llm_latency_sec"))
        if latency is not None:
            latencies.append(latency)
        choice = data.get("llm_choice") if isinstance(data.get("llm_choice"), dict) else {}
        errors = choice.get("retry_errors") if isinstance(choice.get("retry_errors"), list) else []
        retry_errors += len(errors)
        if errors:
            retry_attempts += 1
        usage = data.get("llm_usage")
        if isinstance(usage, dict):
            for key in ("input_tokens", "prompt_tokens"):
                value = usage.get(key)
                if isinstance(value, int):
                    usage_input += value
                    break
            for key in ("output_tokens", "completion_tokens"):
                value = usage.get(key)
                if isinstance(value, int):
                    usage_output += value
                    break
            value = usage.get("total_tokens")
            if isinstance(value, int):
                usage_total += value

    return {
        "proposal_json_count": len(files),
        "llm_successful_proposal_count": len(initial_files),
        "llm_api_call_count": None,
        "llm_provider": provider_counts.most_common(1)[0][0] if provider_counts else None,
        "llm_model": model_counts.most_common(1)[0][0] if model_counts else None,
        "llm_provider_counts": dict(provider_counts),
        "llm_model_counts": dict(model_counts),
        "proposal_mode_counts": dict(proposal_mode_counts),
        "llm_retry_error_count": retry_errors,
        "llm_retry_attempt_count": retry_attempts,
        "llm_retry_stats_available": True,
        "mean_llm_latency_sec": statistics.mean(latencies) if latencies else None,
        "median_llm_latency_sec": statistics.median(latencies) if latencies else None,
        "llm_input_tokens": usage_input or None,
        "llm_output_tokens": usage_output or None,
        "llm_total_tokens": usage_total or (usage_input + usage_output) or None,
        "llm_debug_failure_files": len(debug_files),
        "proposal_stats_source": "proposal_json",
    }


def _first_threshold(
    rows: list[dict[str, Any]],
    *,
    group: str | None,
    threshold: float,
    start_time: datetime | None = None,
) -> dict[str, Any]:
    first_ts: datetime | None = None
    start_ts: datetime | None = start_time
    initial_seen = 0
    initial_to_first: int | None = None
    all_seen = 0
    all_to_first: int | None = None

    sorted_rows = sorted(
        rows,
        key=lambda row: (_timestamp_sort_value(row.get("timestamp")), str(row.get("loop_id") or "")),
    )
    for row in sorted_rows:
        ts = _parse_timestamp(row.get("timestamp"))
        if ts and start_ts is None:
            start_ts = ts
        if group is not None and _group(row) != group:
            continue
        all_seen += 1
        if _stage_of(row) == "initial":
            initial_seen += 1
        chi2 = _float(row.get("chi2"))
        if row.get("validated") and chi2 is not None and chi2 < threshold:
            first_ts = ts
            all_to_first = all_seen
            if initial_to_first is None:
                initial_to_first = initial_seen if _stage_of(row) == "initial" else initial_seen
            break

    wall_hours = None
    if first_ts and start_ts:
        wall_hours = max(0.0, (first_ts - start_ts).total_seconds() / 3600.0)
    return {
        "attempt_to_first": all_to_first,
        "initial_attempt_to_first": initial_to_first,
        "wall_hours_to_first": wall_hours,
    }


def _auc_best_chi2(rows: list[dict[str, Any]], cap: float) -> float | None:
    ordered = [row for row in rows if _stage_of(row) == "initial"]
    if not ordered:
        return None
    ordered.sort(key=lambda row: (_timestamp_sort_value(row.get("timestamp")), str(row.get("loop_id") or "")))
    best_so_far = cap
    curve: list[float] = []
    for row in ordered:
        chi2 = _float(row.get("chi2"))
        if row.get("validated") and chi2 is not None:
            best_so_far = min(best_so_far, min(chi2, cap))
        curve.append(best_so_far)
    return statistics.mean(curve) if curve else None


def _sector_summary(rows: list[dict[str, Any]], sector: str) -> dict[str, Any]:
    sector_rows = [row for row in rows if _group(row) == sector]
    sector_acc = _accepted(sector_rows)
    return {
        f"{sector}_attempts": len(sector_rows),
        f"{sector}_initial_attempts": sum(1 for row in sector_rows if _stage_of(row) == "initial"),
        f"{sector}_accepted": len(sector_acc),
        f"{sector}_accept_rate": len(sector_acc) / len(sector_rows) if sector_rows else None,
        f"{sector}_best_chi2": _best(sector_acc),
        f"{sector}_median_accepted_chi2": _median(sector_acc),
        f"{sector}_chi2_lt_2000": sum(1 for row in sector_acc if (_float(row.get("chi2")) or math.inf) < 2000.0),
        f"{sector}_chi2_lt_1650": sum(1 for row in sector_acc if (_float(row.get("chi2")) or math.inf) < 1650.0),
        f"{sector}_unique_families": len({_family_key(row) for row in sector_rows}),
        f"{sector}_unique_accepted_families": len({_family_key(row) for row in sector_acc}),
        f"{sector}_scalar_counts_json": json.dumps(dict(Counter(_scalar(row) for row in sector_rows)), ensure_ascii=False, sort_keys=True),
        f"{sector}_accepted_scalar_counts_json": json.dumps(dict(Counter(_scalar(row) for row in sector_acc)), ensure_ascii=False, sort_keys=True),
    }


def _robustness_metrics(rows: list[dict[str, Any]], proposal_stats: dict[str, Any]) -> dict[str, Any]:
    accepted = _accepted(rows)
    entered = sum(1 for row in rows if row.get("entered_solver"))
    families = [_family_key(row) for row in rows]
    unique_families = len(set(families))
    failure_tags: Counter[str] = Counter()
    for row in rows:
        for tag in row.get("failure_tags") or []:
            failure_tags[str(tag)] += 1
    retry_attempts = proposal_stats.get("llm_retry_attempt_count")
    proposal_count = proposal_stats.get("proposal_json_count")
    retry_rate = None
    if isinstance(retry_attempts, int) and isinstance(proposal_count, int) and proposal_count:
        retry_rate = retry_attempts / proposal_count
    return {
        "accepted_rate": len(accepted) / len(rows) if rows else None,
        "entered_solver_rate": entered / len(rows) if rows else None,
        "duplicate_family_rate": 1.0 - (unique_families / len(rows)) if rows else None,
        "unique_family_count": unique_families,
        "llm_retry_rate": retry_rate,
        "llm_debug_failure_files": proposal_stats["llm_debug_failure_files"],
        "failure_tag_counts_json": json.dumps(dict(failure_tags.most_common(20)), ensure_ascii=False),
    }


def summarize_run(run_name: str, chi2_cap: float = DEFAULT_CHI2_CAP) -> dict[str, Any]:
    hist_path = Path("ai_theory_lab") / "memory" / run_name / "attempt_history.jsonl"
    sched_path = Path("ai_theory_lab") / "proposals" / run_name / "scheduler_tasks.jsonl"
    rows = _read_jsonl(hist_path)
    events = _read_jsonl(sched_path)
    proposal_stats = _proposal_stats(run_name, events)
    accepted = _accepted(rows)
    initial_rows = [row for row in rows if _stage_of(row) == "initial"]
    wall_seconds = _wall_seconds(events, rows)
    wall_hours = wall_seconds / 3600.0 if wall_seconds and wall_seconds > 0 else None
    progress = _latest_progress(events)
    event_start = _parse_timestamp(events[0].get("timestamp")) if events else None

    global_first = _first_threshold(rows, group=None, threshold=GLOBAL_THRESHOLD, start_time=event_start)
    new_physics_first = _first_threshold(
        rows,
        group="non_eh",
        threshold=NEW_PHYSICS_THRESHOLD,
        start_time=event_start,
    )
    non_eh_good = [
        row
        for row in accepted
        if _group(row) == "non_eh" and (_float(row.get("chi2")) or math.inf) < NEW_PHYSICS_THRESHOLD
    ]

    out: dict[str, Any] = {
        "run_name": run_name,
        "llm_provider": proposal_stats["llm_provider"],
        "llm_model": proposal_stats["llm_model"],
        "proposal_stats_source": proposal_stats["proposal_stats_source"],
        "llm_successful_proposal_count": proposal_stats["llm_successful_proposal_count"],
        "llm_api_call_count": proposal_stats["llm_api_call_count"],
        "records": len(rows),
        "initial_records": len(initial_rows),
        "accepted": len(accepted),
        "best_chi2": _best(accepted),
        "median_accepted_chi2": _median(accepted),
        "target_attempts": progress.get("target_attempts"),
        "submitted_total": progress.get("submitted_total"),
        "recorded_total": progress.get("recorded_total"),
        "scheduler_complete": progress.get("scheduler_complete"),
        "wall_time_hours": wall_hours,
        "initial_attempts_per_hour": len(initial_rows) / wall_hours if wall_hours else None,
        "records_per_hour": len(rows) / wall_hours if wall_hours else None,
        "accepted_per_hour": len(accepted) / wall_hours if wall_hours else None,
        "best_chi2_auc_capped": _auc_best_chi2(rows, chi2_cap),
        "count_chi2_lt_1650": sum(1 for row in accepted if (_float(row.get("chi2")) or math.inf) < GLOBAL_THRESHOLD),
        "attempt_to_first_chi2_lt_1650": global_first["attempt_to_first"],
        "initial_attempt_to_first_chi2_lt_1650": global_first["initial_attempt_to_first"],
        "wall_hours_to_first_chi2_lt_1650": global_first["wall_hours_to_first"],
        "non_eh_count_chi2_lt_2000": len(non_eh_good),
        "non_eh_unique_families_chi2_lt_2000": len({_family_key(row) for row in non_eh_good}),
        "attempt_to_first_non_eh_chi2_lt_2000": new_physics_first["attempt_to_first"],
        "initial_attempt_to_first_non_eh_chi2_lt_2000": new_physics_first["initial_attempt_to_first"],
        "wall_hours_to_first_non_eh_chi2_lt_2000": new_physics_first["wall_hours_to_first"],
        "active_or_moderate_families": _active_or_moderate_count(accepted),
        "mean_task_elapsed_sec": _mean_event_value(events, "recorded", "elapsed_sec"),
        "median_task_elapsed_sec": _median_event_value(events, "recorded", "elapsed_sec"),
        "mean_llm_latency_sec": proposal_stats["mean_llm_latency_sec"],
        "median_llm_latency_sec": proposal_stats["median_llm_latency_sec"],
        "llm_input_tokens": proposal_stats["llm_input_tokens"],
        "llm_output_tokens": proposal_stats["llm_output_tokens"],
        "llm_total_tokens": proposal_stats["llm_total_tokens"],
    }
    out.update(_sector_summary(rows, "open_search"))
    out.update(_sector_summary(rows, "non_eh"))
    out.update(_robustness_metrics(rows, proposal_stats))
    return out


def _effective_status(row: dict[str, Any]) -> str:
    for key in ("effective_correction", "effective_correction_summary"):
        value = row.get(key)
        if isinstance(value, dict):
            status = value.get("effective_correction_status")
            if status:
                return str(status)
    theory = _theory(row)
    value = theory.get("effective_correction")
    if isinstance(value, dict):
        status = value.get("effective_correction_status")
        if status:
            return str(status)
    return "unknown"


def _active_or_moderate_count(rows: list[dict[str, Any]]) -> int:
    families = set()
    for row in rows:
        if _track(row) != "eh_anchored":
            continue
        if _effective_status(row) not in {"active", "moderate"}:
            continue
        families.add(_family_key(row))
    return len(families)


def _event_values(events: list[dict[str, Any]], event_name: str, key: str) -> list[float]:
    values: list[float] = []
    for event in events:
        if event.get("event") != event_name:
            continue
        value = _float(event.get(key))
        if value is not None:
            values.append(value)
    return values


def _mean_event_value(events: list[dict[str, Any]], event_name: str, key: str) -> float | None:
    values = _event_values(events, event_name, key)
    return statistics.mean(values) if values else None


def _median_event_value(events: list[dict[str, Any]], event_name: str, key: str) -> float | None:
    values = _event_values(events, event_name, key)
    return statistics.median(values) if values else None


def _axis_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    run_name = summary["run_name"]
    model = summary.get("llm_model") or run_name
    return [
        {
            "run_name": run_name,
            "model": model,
            "axis": "global_optimum",
            "primary_metric": "best_chi2",
            "primary_value": summary.get("best_chi2"),
            "secondary_metric": "attempt_to_first_chi2_lt_1650",
            "secondary_value": summary.get("attempt_to_first_chi2_lt_1650"),
        },
        {
            "run_name": run_name,
            "model": model,
            "axis": "new_physics_search",
            "primary_metric": "non_eh_best_chi2",
            "primary_value": summary.get("non_eh_best_chi2"),
            "secondary_metric": "non_eh_count_chi2_lt_2000",
            "secondary_value": summary.get("non_eh_count_chi2_lt_2000"),
        },
        {
            "run_name": run_name,
            "model": model,
            "axis": "speed_efficiency",
            "primary_metric": "initial_attempts_per_hour",
            "primary_value": summary.get("initial_attempts_per_hour"),
            "secondary_metric": "mean_task_elapsed_sec",
            "secondary_value": summary.get("mean_task_elapsed_sec"),
        },
        {
            "run_name": run_name,
            "model": model,
            "axis": "robustness_stability",
            "primary_metric": "accepted_rate",
            "primary_value": summary.get("accepted_rate"),
            "secondary_metric": "non_eh_accept_rate",
            "secondary_value": summary.get("non_eh_accept_rate"),
        },
    ]


def _resolve_runs(patterns: list[str]) -> list[str]:
    runs: set[str] = set()
    memory_dir = Path("ai_theory_lab") / "memory"
    for pattern in patterns:
        if any(ch in pattern for ch in "*?[]"):
            runs.update(path.name for path in memory_dir.glob(pattern) if path.is_dir())
        else:
            if (memory_dir / pattern).is_dir():
                runs.add(pattern)
    return sorted(runs)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def compare_runs(run_names: list[str], output_dir: Path, chi2_cap: float = DEFAULT_CHI2_CAP) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summaries = [summarize_run(run_name, chi2_cap=chi2_cap) for run_name in run_names]
    summaries.sort(key=lambda row: (str(row.get("llm_model") or ""), row["run_name"]))
    axis_rows = [axis_row for summary in summaries for axis_row in _axis_rows(summary)]
    payload = {
        "generated_by": "ai_theory_lab.compare_benchmarks",
        "runs": run_names,
        "chi2_auc_cap": chi2_cap,
        "axes": {
            "global_optimum": "best chi2, threshold discovery speed, capped best-chi2 AUC",
            "new_physics_search": "non-EH best chi2, non-EH chi2<2000 yield, viable family diversity",
            "speed_efficiency": "initial attempts per wall-hour, task elapsed times, LLM latency/tokens when available",
            "robustness_stability": "acceptance, solver reachability, duplicate rate, LLM retry/debug failures",
        },
        "summaries": summaries,
    }
    (output_dir / "comparison_summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_csv(output_dir / "comparison_metrics.csv", summaries)
    _write_csv(output_dir / "comparison_by_axis.csv", axis_rows)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare AI modified-gravity discovery runs across LLM providers.")
    parser.add_argument("--runs", nargs="+", required=True, help="Run names or glob patterns under ai_theory_lab/memory.")
    parser.add_argument(
        "--output-dir",
        default="ai_theory_lab/reports/model_api_comparison",
        help="Directory for comparison_summary.json and CSV outputs.",
    )
    parser.add_argument("--chi2-cap", type=float, default=DEFAULT_CHI2_CAP, help="Cap used for best-chi2 AUC before first success.")
    args = parser.parse_args()

    run_names = _resolve_runs(args.runs)
    if not run_names:
        raise SystemExit("No runs matched --runs.")
    payload = compare_runs(run_names, Path(args.output_dir), chi2_cap=args.chi2_cap)
    print(args.output_dir)
    for summary in payload["summaries"]:
        print(
            f"{summary['run_name']}: best={summary.get('best_chi2')} "
            f"open={summary.get('open_search_best_chi2')} "
            f"non_eh={summary.get('non_eh_best_chi2')} "
            f"speed={summary.get('initial_attempts_per_hour')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
