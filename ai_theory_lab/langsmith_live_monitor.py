"""Sidecar live monitor for discovery runs.

This script reads local attempt histories and emits periodic LangSmith trace
events with rolling chi-square minima. It does not touch running jobs.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from .dataset import AIC_REFERENCE_K
from .tracing import trace_event, tracing_enabled


DEFAULT_RUNS = [
    "cmp1000_openai_gpt_5_6_sol_frontier6_openonly_aic_v2_8cpu",
    "cmp1000_claude_sonnet_5_frontier6_openonly_aic_v2_8cpu",
    "cmp1000_gemini_3_6_flash_frontier6_openonly_aic_v2_8cpu",
    "cmp1000_qwen3_7_max_frontier6_openonly_aic_v2_8cpu",
    "cmp1000_deepseek_ali_v4_pro_frontier6_openonly_aic_v2_8cpu",
    "cmp1000_kimi_k3_frontier6_openonly_aic_v2_8cpu",
]

RUN_LABELS = {
    DEFAULT_RUNS[0]: "OpenAI",
    DEFAULT_RUNS[1]: "Claude",
    DEFAULT_RUNS[2]: "Gemini",
    DEFAULT_RUNS[3]: "Qwen",
    DEFAULT_RUNS[4]: "DeepSeek",
    DEFAULT_RUNS[5]: "Kimi",
}

LCDM_REFERENCE_AIC = 1651.28


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


def _float(value: Any) -> float | None:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def _fmt(value: Any) -> str:
    number = _float(value)
    return "n/a" if number is None else f"{number:.3f}"


def _timestamp(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


def _elapsed_hours(events: list[dict[str, Any]]) -> float | None:
    elapsed_seconds = 0.0
    segment_start: datetime | None = None
    segment_last: datetime | None = None
    for event in events:
        timestamp = _timestamp(event.get("timestamp"))
        if timestamp is None:
            continue
        if event.get("event") in {"scheduler_start", "scheduler_resume"}:
            if segment_start is not None and segment_last is not None:
                elapsed_seconds += max(0.0, (segment_last - segment_start).total_seconds())
            segment_start = timestamp
        segment_last = timestamp
    if segment_start is not None and segment_last is not None:
        elapsed_seconds += max(0.0, (segment_last - segment_start).total_seconds())
    elapsed = elapsed_seconds / 3600.0
    return elapsed if elapsed > 0 else None


def _group(row: dict[str, Any]) -> str:
    theory = row.get("theory") if isinstance(row.get("theory"), dict) else {}
    return str(row.get("proposal_group") or theory.get("proposal_group") or "unknown")


def _track(row: dict[str, Any]) -> str:
    theory = row.get("theory") if isinstance(row.get("theory"), dict) else {}
    return str(row.get("theory_track") or theory.get("theory_track") or "unknown")


def _best(rows: list[dict[str, Any]], group: str | None = None) -> float | None:
    values = []
    for row in rows:
        if group is not None and _group(row) != group:
            continue
        if not row.get("validated"):
            continue
        value = _float(row.get("chi2"))
        if value is not None:
            values.append(value)
    return min(values) if values else None


def _best_track(rows: list[dict[str, Any]], track: str) -> float | None:
    return _best([row for row in rows if _track(row) == track])


def _best_metric(rows: list[dict[str, Any]], key: str) -> float | None:
    values = [
        value
        for row in rows
        if row.get("validated")
        for value in [_float(row.get(key))]
        if value is not None
    ]
    return min(values) if values else None


def _structure_score(row: dict[str, Any]) -> float | None:
    score = _float(row.get("structure_score"))
    if score is not None:
        return score
    aic = _float(row.get("aic"))
    return None if aic is None else aic - 2.0 * AIC_REFERENCE_K


def _best_structure_score(rows: list[dict[str, Any]]) -> float | None:
    values = [score for row in rows if row.get("validated") for score in [_structure_score(row)] if score is not None]
    return min(values) if values else None


def _count_lt(rows: list[dict[str, Any]], threshold: float, group: str | None = None) -> int:
    total = 0
    for row in rows:
        if group is not None and _group(row) != group:
            continue
        if not row.get("validated"):
            continue
        value = _float(row.get("chi2"))
        if value is not None and value < threshold:
            total += 1
    return total


def _count_lt_track(rows: list[dict[str, Any]], threshold: float, track: str) -> int:
    return _count_lt([row for row in rows if _track(row) == track], threshold)


def _summary(run: str) -> dict[str, Any]:
    hist = Path("ai_theory_lab") / "memory" / run / "attempt_history.jsonl"
    sched = Path("ai_theory_lab") / "proposals" / run / "scheduler_tasks.jsonl"
    rows = _read_jsonl(hist)
    events = _read_jsonl(sched)
    latest = events[-1] if events else {}
    accepted = [row for row in rows if row.get("validated") and _float(row.get("chi2")) is not None]
    open_rows = [row for row in rows if _group(row) == "open_search"]
    non_eh_rows = [row for row in rows if _track(row) == "non_eh"]
    best_aic = _best_metric(rows, "aic")
    target_attempts = latest.get("target_attempts", 2000)
    recorded_total = latest.get("recorded_total", len(rows))
    elapsed_hours = _elapsed_hours(events)
    attempts_per_hour = recorded_total / elapsed_hours if elapsed_hours else None
    eta_hours = (
        max(0, target_attempts - recorded_total) / attempts_per_hour
        if attempts_per_hour and target_attempts is not None
        else None
    )
    return {
        "run_name": run,
        "event": "live_metrics",
        "recorded_total": recorded_total,
        "submitted_total": latest.get("submitted_total"),
        "target_attempts": target_attempts,
        "elapsed_hours": elapsed_hours,
        "initial_attempts_per_hour": attempts_per_hour,
        "eta_hours": eta_hours,
        "accepted_total": len(accepted),
        "accept_rate": len(accepted) / len(rows) if rows else None,
        "global_best_chi2": _best(rows),
        "global_best_aic": best_aic,
        "global_best_delta_aic_vs_lcdm": None if best_aic is None else best_aic - LCDM_REFERENCE_AIC,
        "global_best_structure_score": _best_structure_score(rows),
        "open_search_best_chi2": _best(rows, "open_search"),
        "non_eh_best_chi2": _best_track(rows, "non_eh"),
        "non_eh_best_structure_score": _best_structure_score(non_eh_rows),
        "open_search_attempts": len(open_rows),
        "non_eh_attempts": len(non_eh_rows),
        "open_search_accept_rate": (
            len([row for row in open_rows if row.get("validated") and _float(row.get("chi2")) is not None]) / len(open_rows)
            if open_rows
            else None
        ),
        "non_eh_accept_rate": (
            len([row for row in non_eh_rows if row.get("validated") and _float(row.get("chi2")) is not None]) / len(non_eh_rows)
            if non_eh_rows
            else None
        ),
        "global_chi2_lt_1650": _count_lt(rows, 1650.0),
        "open_search_chi2_lt_1650": _count_lt(rows, 1650.0, "open_search"),
        "non_eh_chi2_lt_2000": _count_lt_track(rows, 2000.0, "non_eh"),
        "scheduler_latest_event": latest.get("event"),
        "scheduler_complete": latest.get("event") == "scheduler_complete",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit rolling chi-square minima to LangSmith.")
    parser.add_argument("--runs", nargs="+", default=DEFAULT_RUNS)
    parser.add_argument("--interval", type=float, default=60.0)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    if not tracing_enabled():
        raise SystemExit("LangSmith tracing is not enabled. Set LANGSMITH_TRACING=true and LANGSMITH_API_KEY.")

    while True:
        for run in args.runs:
            payload = _summary(run)
            print(
                f"{RUN_LABELS.get(run, run)}: recorded={payload['recorded_total']}/{payload['target_attempts']} "
                f"accepted={payload['accepted_total']} "
                f"speed={_fmt(payload['initial_attempts_per_hour'])}/h "
                f"ETA={_fmt(payload['eta_hours'])}h "
                f"chi2*={_fmt(payload['global_best_chi2'])} "
                f"AIC*={_fmt(payload['global_best_aic'])} "
                f"dAIC={_fmt(payload['global_best_delta_aic_vs_lcdm'])} "
                f"score*={_fmt(payload['global_best_structure_score'])} "
                f"non_eh_chi2*={_fmt(payload['non_eh_best_chi2'])} "
                f"non_eh_score*={_fmt(payload['non_eh_best_structure_score'])}",
                flush=True,
            )
            trace_event("ai_theory_lab.live_metrics", payload, run_name=run)
        if args.once:
            break
        time.sleep(max(5.0, args.interval))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
