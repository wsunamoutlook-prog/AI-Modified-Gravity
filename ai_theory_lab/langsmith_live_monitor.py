"""Sidecar live monitor for discovery runs.

This script reads local attempt histories and emits periodic LangSmith trace
events with rolling chi-square minima. It does not touch running jobs.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

from .tracing import trace_event, tracing_enabled


DEFAULT_RUNS = [
    "cmp600_openai_gpt_5_5_final_v1",
    "cmp600_claude_opus_4_8_final_v1",
    "cmp600_gemini_3_1_pro_final_v1",
    "cmp600_qwen3_7_plus_final_v1",
    "cmp600_deepseek_ali_v4_pro_final_v1",
]


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


def _group(row: dict[str, Any]) -> str:
    theory = row.get("theory") if isinstance(row.get("theory"), dict) else {}
    return str(row.get("proposal_group") or theory.get("proposal_group") or "unknown")


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


def _summary(run: str) -> dict[str, Any]:
    hist = Path("ai_theory_lab") / "memory" / run / "attempt_history.jsonl"
    sched = Path("ai_theory_lab") / "proposals" / run / "scheduler_tasks.jsonl"
    rows = _read_jsonl(hist)
    events = _read_jsonl(sched)
    latest = events[-1] if events else {}
    accepted = [row for row in rows if row.get("validated") and _float(row.get("chi2")) is not None]
    open_rows = [row for row in rows if _group(row) == "open_search"]
    non_eh_rows = [row for row in rows if _group(row) == "non_eh"]
    return {
        "run_name": run,
        "event": "live_metrics",
        "recorded_total": latest.get("recorded_total", len(rows)),
        "submitted_total": latest.get("submitted_total"),
        "target_attempts": latest.get("target_attempts"),
        "accepted_total": len(accepted),
        "accept_rate": len(accepted) / len(rows) if rows else None,
        "global_best_chi2": _best(rows),
        "open_search_best_chi2": _best(rows, "open_search"),
        "non_eh_best_chi2": _best(rows, "non_eh"),
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
        "non_eh_chi2_lt_2000": _count_lt(rows, 2000.0, "non_eh"),
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
                f"{run}: recorded={payload['recorded_total']} "
                f"best={payload['global_best_chi2']} "
                f"open={payload['open_search_best_chi2']} "
                f"non_eh={payload['non_eh_best_chi2']}",
                flush=True,
            )
            trace_event("ai_theory_lab.live_metrics", payload, run_name=run)
        if args.once:
            break
        time.sleep(max(5.0, args.interval))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
