"""Build an Overleaf-ready package for the unified five-agent cmp1500 result.

The package uses the user's supplied Overleaf zip as the template, keeps the
theory/numerical-method sections intact, and replaces the benchmark/results
block with the current five-agent result:

* GPT-5.5, Claude Opus 4.8, and Gemini 3.1 Pro from cmp1500 expensive runs.
* Qwen 3.7 Plus and DeepSeek V4 Pro from the previous cmp2000 run, truncated
  to task ids <= 1500.

No run-source comparison framing is used in the generated figures.
"""

from __future__ import annotations

import csv
import json
import math
import re
import shutil
import statistics
import zipfile
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ZIP = Path("/Users/sunwenrong/Desktop/Dark_Energy_Autonomous_Search_from_Cosmological_Background_Data__1_.zip")
WORK = ROOT / "tmp" / "cmp1500_source_zip_for_package"
OUT = ROOT / "overleaf_cmp1500_agent_results_v1"
FIG_DIR = OUT / "figures"
DATA_DIR = OUT / "data"
LCDM_CHI2 = 1645.28
H_LCDM_REPLAY_FIG_DIR = ROOT / "cluster_report" / "cmp600_final_v1" / "paper_figures_v3"


@dataclass(frozen=True)
class AgentSpec:
    key: str
    label: str
    model: str
    base: Path
    run: str
    task_limit: int | None = None
    initial_recorded_override: int | None = None
    status: str = "completed"


AGENTS = [
    AgentSpec(
        "openai",
        "GPT-5.5",
        "gpt-5.5",
        ROOT / "cluster_report" / "cmp1500_expensive_v1",
        "cmp1500_openai_gpt_5_5_expensive_v1",
        None,
        1396,
        "72 h censored",
    ),
    AgentSpec(
        "claude",
        "Opus 4.8",
        "claude-opus-4-8",
        ROOT / "cluster_report" / "cmp1500_expensive_v1",
        "cmp1500_claude_opus_4_8_expensive_v1",
        None,
        1500,
        "completed",
    ),
    AgentSpec(
        "gemini",
        "Gemini 3.1",
        "gemini-3.1-pro-preview",
        ROOT / "cluster_report" / "cmp1500_expensive_v1",
        "cmp1500_gemini_3_1_pro_expensive_v1",
        None,
        1500,
        "completed",
    ),
    AgentSpec(
        "qwen",
        "Qwen 3.7",
        "qwen3.7-plus",
        ROOT / "cluster_report" / "cmp2000_cheap_partial_v1_full",
        "cmp2000_qwen3_7_plus_cheap_v1",
        1500,
        1500,
        "truncated",
    ),
    AgentSpec(
        "deepseek",
        "DeepSeek V4",
        "deepseek-v4-pro",
        ROOT / "cluster_report" / "cmp2000_cheap_partial_v1_full",
        "cmp2000_deepseek_ali_v4_pro_cheap_v1",
        1500,
        1500,
        "truncated",
    ),
]

COLORS = {
    "openai": "#4C78A8",
    "claude": "#F58518",
    "gemini": "#54A24B",
    "qwen": "#B279A2",
    "deepseek": "#E45756",
}

TASK_RE = re.compile(r"task_(\d{6})")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
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


def finite_float(value: Any) -> float | None:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def task_number(loop_id: Any) -> int | None:
    m = TASK_RE.search(str(loop_id or ""))
    return int(m.group(1)) if m else None


def parse_time(value: Any) -> datetime | None:
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


def group_of(row: dict[str, Any]) -> str:
    th = row.get("theory") if isinstance(row.get("theory"), dict) else {}
    return str(row.get("proposal_group") or th.get("proposal_group") or "unknown")


def scalar_of(row: dict[str, Any]) -> str:
    th = row.get("theory") if isinstance(row.get("theory"), dict) else {}
    return str(th.get("scalar_config") or "unknown")


def operators_of(row: dict[str, Any]) -> list[str]:
    th = row.get("theory") if isinstance(row.get("theory"), dict) else {}
    return [str(op) for op in (th.get("operators") or [])]


def stage_of(row: dict[str, Any]) -> str:
    loop = str(row.get("loop_id") or "")
    if "_expanded_refine_" in loop or "_refine_" in loop:
        return "refine"
    if "_expanded_" in loop:
        return "expanded"
    return "initial"


def accepted(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in rows if r.get("validated") and finite_float(r.get("chi2")) is not None]


def load_rows(spec: AgentSpec) -> list[dict[str, Any]]:
    rows = read_jsonl(spec.base / "memory" / spec.run / "attempt_history.jsonl")
    if spec.task_limit is not None:
        rows = [r for r in rows if (task_number(r.get("loop_id")) or 10**9) <= spec.task_limit]
    return rows


def load_events(spec: AgentSpec) -> list[dict[str, Any]]:
    events = read_jsonl(spec.base / "proposals" / spec.run / "scheduler_tasks.jsonl")
    if spec.task_limit is not None:
        keep: list[dict[str, Any]] = []
        for event in events:
            tno = task_number(event.get("task_id") or event.get("validation_wave") or "")
            if tno is None or tno <= spec.task_limit:
                keep.append(event)
        events = keep
    return events


def wall_hours(events: list[dict[str, Any]], rows: list[dict[str, Any]]) -> float | None:
    times = [parse_time(e.get("timestamp")) for e in events]
    times = [t for t in times if t is not None]
    if len(times) >= 2:
        return max((max(times) - min(times)).total_seconds() / 3600.0, 0.0)
    times = [parse_time(r.get("timestamp")) for r in rows]
    times = [t for t in times if t is not None]
    if len(times) >= 2:
        return max((max(times) - min(times)).total_seconds() / 3600.0, 0.0)
    return None


def median(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def best_row(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    acc = accepted(rows)
    return min(acc, key=lambda r: float(r["chi2"])) if acc else None


def family_key(row: dict[str, Any]) -> str:
    if row.get("family_key"):
        return str(row["family_key"])
    payload = {
        "scalar": scalar_of(row),
        "operators": operators_of(row),
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def unique_good_families(rows: list[dict[str, Any]], threshold: float) -> int:
    return len({family_key(r) for r in accepted(rows) if float(r["chi2"]) < threshold})


def build_metrics() -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    metrics: list[dict[str, Any]] = []
    rows_by_agent: dict[str, list[dict[str, Any]]] = {}
    for spec in AGENTS:
        rows = load_rows(spec)
        events = load_events(spec)
        rows_by_agent[spec.key] = rows
        acc = accepted(rows)
        hours = wall_hours(events, rows)
        item: dict[str, Any] = {
            "key": spec.key,
            "label": spec.label,
            "model": spec.model,
            "run": spec.run,
            "status": spec.status,
            "initial_recorded": spec.initial_recorded_override or len(rows),
            "validation_records": len(rows),
            "accepted": len(acc),
            "accepted_rate": len(acc) / len(rows) if rows else 0.0,
            "wall_hours": hours,
            "throughput": (spec.initial_recorded_override or len(rows)) / hours if hours and hours > 0 else None,
        }
        for sec in ("open_search", "non_eh"):
            sub = [r for r in rows if group_of(r) == sec]
            sub_acc = accepted(sub)
            chis = sorted(float(r["chi2"]) for r in sub_acc)
            item[f"{sec}_attempts"] = len(sub)
            item[f"{sec}_accepted"] = len(sub_acc)
            item[f"{sec}_accepted_rate"] = len(sub_acc) / len(sub) if sub else 0.0
            item[f"{sec}_best"] = chis[0] if chis else None
            item[f"{sec}_median"] = median(chis)
            item[f"{sec}_hits_lt2000"] = sum(c < 2000 for c in chis)
            item[f"{sec}_hits_lt1650"] = sum(c < 1650 for c in chis)
            item[f"{sec}_unique_lt2000"] = unique_good_families(sub, 2000)
            item[f"{sec}_unique_lt1650"] = unique_good_families(sub, 1650)
            item[f"{sec}_best_loop"] = best_row(sub).get("loop_id") if best_row(sub) else ""
        item["best"] = min(
            [x for x in (item["open_search_best"], item["non_eh_best"]) if x is not None],
            default=None,
        )
        metrics.append(item)
    return metrics, rows_by_agent


def set_plot_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "font.family": "serif",
            "mathtext.fontset": "dejavuserif",
            "axes.labelsize": 10,
            "axes.titlesize": 11,
            "xtick.labelsize": 8.5,
            "ytick.labelsize": 9,
            "legend.fontsize": 8.5,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "axes.axisbelow": True,
        }
    )


def savefig(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIG_DIR / f"{name}.pdf", bbox_inches="tight", facecolor="white")
    fig.savefig(FIG_DIR / f"{name}.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def copy_h_lcdm_replay_figure() -> None:
    """Include the replayed best-agent h(z) curves against the LCDM reference.

    The cmp1500/cmp2000 pull contains per-task ranking and accepted-sample
    summaries, but not the Solver solution-curve CSVs needed to redraw h(z).
    The dedicated replay artifact stores those solution curves and the figure.
    """
    for suffix in ("pdf", "png"):
        src = H_LCDM_REPLAY_FIG_DIR / f"agent_best_h_lcdm.{suffix}"
        if not src.exists():
            raise FileNotFoundError(f"missing h(z) replay figure: {src}")
        shutil.copy2(src, FIG_DIR / src.name)


def label_order(metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(metrics, key=lambda m: m["open_search_best"] if m["open_search_best"] is not None else 1e99)


def annotate_bars(ax: plt.Axes, bars: Any, fmt: str = "{:.2f}", dy: float = 2.0) -> None:
    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + dy,
            fmt.format(h),
            ha="center",
            va="bottom",
            fontsize=8,
        )


def plot_dashboard(metrics: list[dict[str, Any]]) -> None:
    ordered = label_order(metrics)
    labels = [m["label"] for m in ordered]
    colors = [COLORS[m["key"]] for m in ordered]
    x = np.arange(len(ordered))

    fig, axs = plt.subplots(2, 2, figsize=(7.2, 5.2))
    fig.suptitle("Five-agent autonomous background search", y=0.99, fontsize=12)

    vals = [LCDM_CHI2 - m["open_search_best"] for m in ordered]
    bars = axs[0, 0].bar(x, vals, color=colors, edgecolor="black", linewidth=0.4)
    axs[0, 0].axhline(0, color="black", linewidth=0.7)
    axs[0, 0].set_title("Best open-search improvement")
    axs[0, 0].set_ylabel(r"$\chi^2_{\Lambda{\rm CDM}}-\chi^2_{\rm open}$")
    axs[0, 0].set_ylim(0, max(vals) * 1.18)
    annotate_bars(axs[0, 0], bars, "{:.2f}", dy=0.06)

    vals = [m["open_search_hits_lt1650"] for m in ordered]
    bars = axs[0, 1].bar(x, vals, color=colors, edgecolor="black", linewidth=0.4)
    axs[0, 1].set_title(r"Open-search hits with $\chi^2<1650$")
    axs[0, 1].set_ylim(0, max(vals) * 1.18)
    annotate_bars(axs[0, 1], bars, "{:.0f}", dy=max(vals) * 0.015 if vals else 1)

    vals = [m["non_eh_best"] if m["non_eh_best"] and m["non_eh_best"] < 2000 else np.nan for m in ordered]
    bars = axs[1, 0].bar(x, np.nan_to_num(vals, nan=2000), color=colors, edgecolor="black", linewidth=0.4)
    axs[1, 0].axhline(LCDM_CHI2, color="0.35", linestyle="--", linewidth=0.8)
    axs[1, 0].set_ylim(1635, 2025)
    axs[1, 0].set_title(r"Best non-EH hit")
    axs[1, 0].set_ylabel(r"$\chi^2_{\mathrm{non\!-\!EH}}$")
    for bar, value in zip(bars, vals):
        if np.isfinite(value):
            axs[1, 0].text(
                bar.get_x() + bar.get_width() / 2,
                value + 10,
                f"{value:.1f}",
                ha="center",
                va="bottom",
                fontsize=8,
            )
        else:
            axs[1, 0].text(
                bar.get_x() + bar.get_width() / 2,
                1990,
                "none",
                ha="center",
                va="top",
                fontsize=8,
            )

    vals = [m["non_eh_hits_lt2000"] for m in ordered]
    bars = axs[1, 1].bar(x, vals, color=colors, edgecolor="black", linewidth=0.4)
    axs[1, 1].set_title(r"Non-EH hits with $\chi^2<2000$")
    axs[1, 1].set_ylim(0, max(vals) * 1.20)
    annotate_bars(axs[1, 1], bars, "{:.0f}", dy=max(vals) * 0.03 if vals else 1)

    for ax in axs.ravel():
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=22, ha="right")
    fig.tight_layout()
    savefig(fig, "main_benchmark_dashboard")


def plot_non_eh(metrics: list[dict[str, Any]]) -> None:
    ordered = sorted(metrics, key=lambda m: m["non_eh_best"] if m["non_eh_best"] else 1e99)
    labels = [m["label"] for m in ordered]
    colors = [COLORS[m["key"]] for m in ordered]
    x = np.arange(len(ordered))
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
    vals = [m["non_eh_best"] for m in ordered]
    bars = axs[0].bar(x, vals, color=colors, edgecolor="black", linewidth=0.4)
    axs[0].axhline(LCDM_CHI2, color="0.35", linestyle="--", linewidth=0.8)
    axs[0].set_ylim(1635, 2005)
    axs[0].set_ylabel(r"$\chi^2_{\mathrm{non\!-\!EH}}$")
    axs[0].set_title("Best non-EH background")
    for bar, value in zip(bars, vals):
        axs[0].text(bar.get_x() + bar.get_width() / 2, value + 8, f"{value:.1f}", ha="center", va="bottom", fontsize=8)

    vals2 = [m["non_eh_hits_lt2000"] for m in ordered]
    bars = axs[1].bar(x, vals2, color=colors, edgecolor="black", linewidth=0.4)
    axs[1].set_title(r"Hits below $\chi^2=2000$")
    for bar, value in zip(bars, vals2):
        axs[1].text(bar.get_x() + bar.get_width() / 2, value + 0.5, f"{value:.0f}", ha="center", va="bottom", fontsize=8)
    for ax in axs:
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=22, ha="right")
    fig.tight_layout()
    savefig(fig, "non_eh_summary")


def plot_speed_quality(metrics: list[dict[str, Any]]) -> None:
    fig, ax = plt.subplots(figsize=(4.8, 3.4))
    for m in metrics:
        speed = m["throughput"]
        if not speed:
            continue
        size = 18 + 1.2 * m["open_search_hits_lt1650"]
        ax.scatter(
            speed,
            m["open_search_best"],
            s=size,
            color=COLORS[m["key"]],
            edgecolor="black",
            linewidth=0.5,
            alpha=0.85,
            label=m["label"],
        )
    ax.axhline(LCDM_CHI2, color="0.35", linestyle="--", linewidth=0.9, label=r"$\Lambda$CDM")
    ax.set_xlabel("initial theories per wall hour")
    ax.set_ylabel(r"best open-search $\chi^2$")
    ax.set_title("Speed and global optimum")
    ax.set_ylim(1637.86, 1645.7)
    ax.legend(frameon=False, loc="center right")
    savefig(fig, "speed_quality_tradeoff")


def plot_acceptance(metrics: list[dict[str, Any]]) -> None:
    ordered = label_order(metrics)
    labels = [m["label"] for m in ordered]
    x = np.arange(len(ordered))
    width = 0.36
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    open_vals = [m["open_search_accepted_rate"] for m in ordered]
    non_vals = [m["non_eh_accepted_rate"] for m in ordered]
    ax.bar(x - width / 2, open_vals, width, label="open search", color="#4C78A8", edgecolor="black", linewidth=0.3)
    ax.bar(x + width / 2, non_vals, width, label="non-EH", color="#E45756", edgecolor="black", linewidth=0.3)
    for xpos, value in zip(x - width / 2, open_vals):
        ax.text(xpos, value + 0.01, f"{value:.2f}", ha="center", va="bottom", fontsize=7)
    for xpos, value in zip(x + width / 2, non_vals):
        ax.text(xpos, value + 0.01, f"{value:.2f}", ha="center", va="bottom", fontsize=7)
    ax.set_ylabel("accepted / validation records")
    ax.set_title("Sector acceptance rate")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=22, ha="right")
    ax.legend(frameon=False)
    ax.set_ylim(0, max(open_vals + non_vals) * 1.22)
    fig.tight_layout()
    savefig(fig, "sector_acceptance")


def best_so_far_series(rows: list[dict[str, Any]], sector: str) -> tuple[list[int], list[float]]:
    sub = [r for r in rows if group_of(r) == sector]
    sub.sort(key=lambda r: (task_number(r.get("loop_id")) or 10**9, str(r.get("loop_id"))))
    xs: list[int] = []
    ys: list[float] = []
    best = math.inf
    count = 0
    for r in sub:
        if stage_of(r) == "initial":
            count += 1
        value = finite_float(r.get("chi2")) if r.get("validated") else None
        if value is not None and value < best:
            best = value
        if best < math.inf:
            xs.append(max(count, 1))
            ys.append(best)
    return xs, ys


def plot_best_so_far(rows_by_agent: dict[str, list[dict[str, Any]]], sector: str, filename: str, ylim: tuple[float, float]) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for spec in AGENTS:
        xs, ys = best_so_far_series(rows_by_agent[spec.key], sector)
        if not xs:
            continue
        if sector == "non_eh":
            filtered = [(x, y) for x, y in zip(xs, ys) if y < 2050]
            if not filtered:
                continue
            xs, ys = [p[0] for p in filtered], [p[1] for p in filtered]
        ax.plot(xs, ys, color=COLORS[spec.key], linewidth=1.8, label=spec.label)
    ax.axhline(LCDM_CHI2, color="0.35", linestyle="--", linewidth=0.9, label=r"$\Lambda$CDM")
    ax.set_xlabel(f"completed {sector.replace('_', '-')} initial records")
    ax.set_ylabel(r"best-so-far $\chi^2$")
    ax.set_ylim(*ylim)
    title = "Best-so-far open-search trajectory" if sector == "open_search" else "Best-so-far non-EH trajectory"
    ax.set_title(title)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.24))
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    savefig(fig, filename)


def write_metrics(metrics: list[dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    keys = [
        "label",
        "model",
        "run",
        "status",
        "initial_recorded",
        "validation_records",
        "accepted",
        "accepted_rate",
        "wall_hours",
        "throughput",
        "open_search_attempts",
        "open_search_accepted",
        "open_search_accepted_rate",
        "open_search_best",
        "open_search_median",
        "open_search_hits_lt2000",
        "open_search_hits_lt1650",
        "non_eh_attempts",
        "non_eh_accepted",
        "non_eh_accepted_rate",
        "non_eh_best",
        "non_eh_median",
        "non_eh_hits_lt2000",
        "non_eh_hits_lt1650",
    ]
    with (DATA_DIR / "unified_agent_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        for row in metrics:
            writer.writerow({k: row.get(k) for k in keys})
    (DATA_DIR / "unified_agent_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")


def latex_num(value: Any, digits: int = 4) -> str:
    f = finite_float(value)
    if f is None:
        return "--"
    if f == 0:
        return "0"
    af = abs(f)
    if af >= 1e4 or af < 1e-3:
        exp = int(math.floor(math.log10(af)))
        mant = f / (10**exp)
        return rf"{mant:.{digits-1}g}\times 10^{{{exp}}}"
    return f"{f:.{digits}g}"


def latex_operator(candidate: str) -> str:
    known = {
        "R": "R",
        "R · R": "R^2",
        "R^{ab} · R_{ab}": r"R_{\mu\nu}R^{\mu\nu}",
        "R^{bcd}_{a} · R^{a}_{bcd}": r"R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}",
        "R^{cd}_{ab} · R^{afh}_{c} · R^{b}_{fdh}": r"{\cal R}_{3a}",
        "R^{bd}_{ac} · R^{agh}_{b} · R^{c}_{dgh}": r"{\cal R}_{3b}",
        "R^{b}_{a} · R^{cd} · R^{a}_{cbd}": r"{\cal R}_{3c}",
        "R_{ab} · R^{adef} · R^{b}_{def}": r"{\cal R}_{3d}",
        "∇^{a}∇_{a}R": r"\Box R",
        "∇^{a}∇_{a}R · R^{c}_{c}": r"R\Box R",
        "∇^{a}R · ∇_{a}R": r"(\nabla R)^2",
        "∇^{c}R^{ab} · ∇_{c}R_{ab}": r"\nabla_\lambda R_{\mu\nu}\nabla^\lambda R^{\mu\nu}",
        "∇^{e}R^{bcd}_{a} · ∇_{e}R^{a}_{bcd}": r"\nabla_\lambda R_{\mu\nu\rho\sigma}\nabla^\lambda R^{\mu\nu\rho\sigma}",
        "∇^{a}∇_{a}φ1": r"\Box\phi_1",
        "∇^{a}∇_{a}φ2": r"\Box\phi_2",
        "∇^{a}φ1 · ∇_{a}φ1": r"(\nabla\phi_1)^2",
        "∇^{a}φ2 · ∇_{a}φ2": r"(\nabla\phi_2)^2",
        "-½ g^{μν} ∇_μφ1 ∇_νφ1": r"-\frac12(\nabla\phi_1)^2",
        "-½ g^{μν} ∇_μφ2 ∇_νφ2": r"-\frac12(\nabla\phi_2)^2",
        "-½ m_1² φ1²": r"-\frac12m_1^2\phi_1^2",
        "-½ m_2² φ2²": r"-\frac12m_2^2\phi_2^2",
        "-m_1² f_1² (1 - cos(φ1/f_1))": r"-m_1^2f_1^2\left[1-\cos(\phi_1/f_1)\right]",
        "-m_2² f_2² (1 - cos(φ2/f_2))": r"-m_2^2f_2^2\left[1-\cos(\phi_2/f_2)\right]",
    }
    if candidate in known:
        return known[candidate]
    parts = [p.strip() for p in candidate.split(" · ")]
    if len(parts) > 1:
        return " ".join(latex_operator(p) for p in parts)
    out = candidate
    out = out.replace("φ1", r"\phi_1").replace("φ2", r"\phi_2")
    out = out.replace("∇^{a}∇_{a}", r"\Box ")
    out = out.replace("∇", r"\nabla")
    out = out.replace("²", "^2").replace("³", "^3")
    return out


def symbol_to_latex(symbol: str) -> str:
    return symbol.replace("\\", "\\")


def latex_power(power: Any) -> str:
    try:
        p = int(power)
    except Exception:
        return ""
    if p == 0:
        return ""
    return rf"\Lambda^{{{p}}}"


def local_csv_for_row(row: dict[str, Any], spec: AgentSpec) -> Path | None:
    remote = row.get("accepted_samples_summary_path")
    if not remote:
        return None
    marker = "/ai_theory_lab/runs/"
    if marker not in remote:
        return None
    rel = remote.split(marker, 1)[1]
    if spec.base.name == "cmp1500_expensive_v1":
        return spec.base / "runs_by_task" / rel
    return None


def sample_from_csv(row: dict[str, Any], spec: AgentSpec) -> dict[str, Any] | None:
    path = local_csv_for_row(row, spec)
    if not path or not path.exists():
        return None
    try:
        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    except Exception:
        return None
    valid = [r for r in rows if finite_float(r.get("chi2")) is not None]
    if not valid:
        return None
    return min(valid, key=lambda r: float(r["chi2"]))


QWEN_EXACT_1896 = {
    "H0_km_s_Mpc": 61.2619903618848,
    "Omega_m0": 0.3253939201479154,
    "lambda_H_Lambda_over_H0": 1481.7333000734354,
    "\\alpha": 410963.8284091356,
    "\\beta": -3.511447512019949e-06,
    "\\gamma": -8844.981979518423,
    "\\delta": -0.0308874490803324,
    "\\epsilon": 41228604.064942464,
    "\\zeta": -6384.2024185072405,
    "\\eta": 5282550093619810.0,
    "\\theta": 1.418381641907789e-10,
}


def sample_from_joint(row: dict[str, Any], spec: AgentSpec) -> tuple[dict[str, Any] | None, float | None, str]:
    if spec.key == "qwen" and row.get("loop_id") == "task_000809_expanded_refine_slot_03_lag_1":
        return QWEN_EXACT_1896, float(row["chi2"]), "exact from pulled terminal summary"
    path = spec.base / "memory" / spec.run / "joint_parameter_prior.json"
    if not path.exists():
        return None, None, ""
    data = json.loads(path.read_text(encoding="utf-8"))
    loop = row.get("loop_id")
    found: list[dict[str, Any]] = []
    for fams in data.get("families", {}).values():
        for info in fams.values():
            for vector in info.get("top_vectors", []):
                if vector.get("loop_id") == loop:
                    found.append(vector)
    if not found:
        return None, None, ""
    best = min(found, key=lambda v: float(v.get("chi2", 1e99)))
    return best.get("sample") or {}, finite_float(best.get("chi2")), "nearest recovered joint-prior vector"


def best_sample_for_row(row: dict[str, Any], spec: AgentSpec) -> tuple[dict[str, Any] | None, float | None, str]:
    sample = sample_from_csv(row, spec)
    if sample is not None:
        return sample, finite_float(sample.get("chi2")), "exact Solver CSV"
    return sample_from_joint(row, spec)


def lagrangian_terms(row: dict[str, Any]) -> list[dict[str, Any]]:
    al = row.get("agent_lagrangian")
    if isinstance(al, dict):
        lag = al.get("lagrangian")
        if isinstance(lag, dict) and isinstance(lag.get("terms"), list):
            return lag["terms"]
    return []


def coefficient_value(sample: dict[str, Any], symbol: str) -> float | None:
    if symbol == "1":
        return 1.0
    if symbol in sample:
        return finite_float(sample.get(symbol))
    bare = symbol.lstrip("\\")
    return finite_float(sample.get(bare))


def term_latex(term: dict[str, Any], sample: dict[str, Any]) -> tuple[str | None, str | None]:
    symbol = str(term.get("coeff_symbol") or "")
    candidate = str(term.get("candidate") or "")
    fixed = bool(term.get("fixed"))
    if fixed:
        return latex_operator(candidate), None
    value = coefficient_value(sample, symbol)
    if value is not None and abs(value) == 0:
        return None, None
    coeff = symbol_to_latex(symbol)
    power = latex_power(term.get("lambda_power"))
    op = latex_operator(candidate)
    bits = [coeff]
    if power:
        bits.append(power)
    bits.append(op)
    return " ".join(bits), coeff


def join_latex_terms(terms: list[str]) -> str:
    rendered: list[str] = []
    for term in terms:
        clean = term.strip()
        if not clean:
            continue
        if not rendered:
            rendered.append(clean)
        elif clean.startswith("-"):
            rendered.append("- " + clean[1:].strip())
        else:
            rendered.append("+ " + clean)
    return " ".join(rendered) if rendered else r"\text{terms unavailable}"


def representative_lagrangian(row: dict[str, Any], sample: dict[str, Any]) -> tuple[str, str]:
    terms = lagrangian_terms(row)
    grav: list[str] = []
    other: list[str] = []
    coeffs: list[str] = []
    seen: set[str] = set()
    for term in terms:
        rendered, coeff = term_latex(term, sample)
        if not rendered:
            continue
        if term.get("sector") in ("gravity", "non-minimal"):
            grav.append(rendered)
        else:
            other.append(rendered)
        if coeff and coeff not in seen:
            val = coefficient_value(sample, coeff)
            if val is not None and abs(val) != 0:
                coeffs.append(rf"{coeff}={latex_num(val, 4)}")
                seen.add(coeff)
    inside: list[str] = []
    if grav:
        inside.append(r"\Mp^2\left[" + join_latex_terms(grav) + r"\right]")
    inside.extend(other)
    if not inside:
        inside = [r"\text{terms unavailable}"]
    lag = r"\sqrt{-g}\left\{" + join_latex_terms(inside) + r"\right\}"
    coeff_text = ",\\; ".join(coeffs) if coeffs else r"\text{no free nonzero coefficients recovered}"
    return lag, coeff_text


def select_representatives(rows_by_agent: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    reps: list[dict[str, Any]] = []
    spec_map = {s.key: s for s in AGENTS}
    for key, rows in rows_by_agent.items():
        for sec in ("open_search", "non_eh"):
            sub = [r for r in rows if group_of(r) == sec]
            row = best_row(sub)
            if not row:
                continue
            spec = spec_map[key]
            sample, sample_chi2, sample_source = best_sample_for_row(row, spec)
            if sample is None:
                sample = {}
            lag, coeffs = representative_lagrangian(row, sample)
            reps.append(
                {
                    "key": key,
                    "label": spec.label,
                    "sector": sec,
                    "loop_id": row.get("loop_id"),
                    "chi2": float(row["chi2"]),
                    "sample_chi2": sample_chi2,
                    "sample_source": sample_source,
                    "scalar": scalar_of(row),
                    "operators": operators_of(row),
                    "lagrangian": lag,
                    "coefficients": coeffs,
                    "H0": sample.get("H0_km_s_Mpc"),
                    "Omega_m0": sample.get("Omega_m0"),
                    "lambda_H": sample.get("lambda_H_Lambda_over_H0"),
                }
            )
    return reps


def write_representatives(reps: list[dict[str, Any]]) -> None:
    (DATA_DIR / "representative_theories.json").write_text(json.dumps(reps, ensure_ascii=False, indent=2), encoding="utf-8")


def table_rows(metrics: list[dict[str, Any]]) -> str:
    ordered = label_order(metrics)
    lines = []
    for m in ordered:
        lines.append(
            f"{m['label']} & {m['initial_recorded']}/1500 & "
            f"{m['open_search_best']:.3f} & {m['open_search_median']:.3f} & {m['open_search_hits_lt1650']} & "
            f"{m['non_eh_best']:.3f} & {m['non_eh_hits_lt2000']} & "
            f"{m['open_search_accepted_rate']:.3f} / {m['non_eh_accepted_rate']:.3f} \\\\"
        )
    return "\n".join(lines)


def appendix_representative_tex(reps: list[dict[str, Any]]) -> str:
    sections: list[str] = []
    for sector, title in [("open_search", "Open-search representatives"), ("non_eh", "Non-EH representatives")]:
        sector_tex = "open" if sector == "open_search" else "nonEH"
        sections.append(rf"\subsection{{{title}}}" + "\n")
        items = [r for r in reps if r["sector"] == sector]
        items.sort(key=lambda r: r["chi2"])
        for idx, r in enumerate(items, 1):
            ops = "; ".join(latex_operator(op) for op in r["operators"])
            source_note = ""
            if r["sample_source"] and r["sample_source"] != "exact Solver CSV":
                source_note = (
                    rf" The coefficient vector is the {r['sample_source']}; "
                    rf"its stored sample has $\chi^2={r['sample_chi2']:.3f}$."
                    if r["sample_chi2"] is not None
                    else rf" The coefficient vector is the {r['sample_source']}."
                )
            sections.extend(
                [
                    rf"\paragraph*{{{r['label']} {idx}.}} "
                    rf"Scheduler id {tex_escape(str(r['loop_id']))}, scalar family {tex_escape(r['scalar'])}, "
                    rf"$\chiT={r['chi2']:.3f}$.{source_note}",
                    r"\begin{widetext}",
                    r"\begin{equation}",
                    rf"\mathscr{{L}}_{{{r['key']},{sector_tex},{idx}}}={r['lagrangian']}.",
                    r"\end{equation}",
                    r"\end{widetext}",
                    rf"\noindent Nonzero recovered coefficients: ${r['coefficients']}$. "
                    rf"Representative operator content: ${ops}$.",
                    "",
                ]
            )
    return "\n".join(sections)


def tex_escape(text: str) -> str:
    return (
        text.replace("\\", r"\textbackslash{}")
        .replace("_", r"\_")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("#", r"\#")
    )


def new_abstract(metrics: list[dict[str, Any]]) -> str:
    best_open = min(metrics, key=lambda m: m["open_search_best"])
    best_non = min(metrics, key=lambda m: m["non_eh_best"])
    return rf"""We present a physics-first autonomous search for two-scalar modified-gravity backgrounds and use it to benchmark large-language-model proposal policies under an identical deterministic validation pipeline. Candidate theories are generated as covariant, dimension-balanced Lagrangian densities built from curvature tensors, covariant derivatives, and two scalar fields. They are then subjected to symbolic FLRW equation-of-motion filtering, algebraic cancellation of independent third- and higher-time derivatives, Builder conversion into numerical models, and direct comparison with DES type-Ia supernovae and DESI Data Release 2 baryon-acoustic-oscillation distances. The AI component affects only the proposal distribution over legal operator combinations and explicit parameter samples; ghost filtering, numerical regularity, constraint preservation, and the final ranking by $\chi^2_{{\rm tot}}$ are determined by the physics code. The unified benchmark uses five agents: GPT-5.5, Claude Opus 4.8, Gemini 3.1 Pro, Qwen 3.7 Plus, and DeepSeek V4 Pro. Qwen obtains the best open-search value, $\chi^2_{{\rm tot}}={best_open['open_search_best']:.3f}$, while DeepSeek obtains the strongest non-EH branch, $\chi^2_{{\rm tot}}={best_non['non_eh_best']:.3f}$. The fixed $\Lambda$CDM reference gives $\chi^2_{{\rm tot}}=1645.28$, so all agents locate competitive Einstein--Hilbert-anchored backgrounds, whereas genuinely non-EH backgrounds remain substantially less favored. These results benchmark proposal policies for background discovery; they do not by themselves establish full covariant ghost freedom, perturbation stability, structure-growth viability, gravitational-wave consistency, or local-gravity screening."""


def benchmark_design_tex() -> str:
    return r"""\subsection{Benchmark design and monitoring}
\label{subsec:benchmark-design}

We analyze a unified five-agent benchmark.  GPT-5.5, Claude Opus 4.8, and Gemini 3.1 Pro are taken from the new 1500-target production runs.  The GPT-5.5 job reached the 72-hour wall-time limit after 1396 recorded initial theories, and we keep the censored result as produced rather than completing it with an additional run.  Qwen 3.7 Plus and DeepSeek V4 Pro are taken from the earlier 2000-target production runs, truncated to task ids not exceeding 1500; expanded and refined validations attached to those first 1500 initial tasks are retained.  We treat these five data sets as one benchmark without drawing a run-source distinction in the figures.

All runs use the same grammar cache, proposal schema, sector split, parameter ranges, initial sample budget, expansion/refinement rules, and ranking by $\chi^2_{\rm tot}$.  The $\Lambda$CDM reference for the same DES-SN plus DESI-DR2 BAO likelihood is
\begin{equation}
\chi^2_{\Lambda{\rm CDM}}=1645.28,
\qquad
H_0=70.0~{\rm km\,s^{-1}\,Mpc^{-1}},
\qquad
\Omega_{m0}=0.306 .
\label{eq:lcdm-reference}
\end{equation}
The benchmark axes are global optimum quality, new-physics search performance, speed/efficiency, robustness/stability, and acceptance rate.  LangSmith tracing was enabled only as a monitoring layer; the paper tables and figures are generated from local JSONL and CSV artifacts, which are the reproducible source of truth.
"""


def results_tex(metrics: list[dict[str, Any]], reps: list[dict[str, Any]]) -> str:
    best_open = min(metrics, key=lambda m: m["open_search_best"])
    best_non = min(metrics, key=lambda m: m["non_eh_best"])
    return rf"""\section{{Benchmark Results}}
\label{{sec:results}}

\begin{{figure*}}[t]
\centering
\includegraphics[width=0.88\textwidth]{{figures/main_benchmark_dashboard.pdf}}
\caption{{Unified five-agent benchmark.  The panels show the positive open-search improvement relative to the fixed $\Lambda$CDM reference, the number of high-quality open-search hits, the best non-EH background in the $\chi^2<2000$ display range, and the number of non-EH hits below that threshold.  The dashed reference line in the non-EH best panel is $\Lambda$CDM, while $\chi^2=2000$ is used only as a display and hit-count threshold.}}
\label{{fig:benchmark-dashboard}}
\end{{figure*}}

\begin{{table*}}[t]
\centering
\caption{{Unified benchmark metrics.  GPT-5.5 is wall-time censored at 1396 recorded initial theories; Qwen 3.7 and DeepSeek V4 use the first 1500 task ids from the earlier 2000-target run.  ``Open'' denotes the full grammar sector, while ``non-EH'' denotes the sector without a bare Einstein--Hilbert $R$ anchor.}}
\label{{tab:agent-benchmark}}
\resizebox{{\textwidth}}{{!}}{{%
\begin{{tabular}}{{lccccccc}}
\toprule
Agent & Initial & Open best & Open median & Open $<1650$ & non-EH best & non-EH $<2000$ & Acc. rate open/non-EH \\
\midrule
{table_rows(metrics)}
\bottomrule
\end{{tabular}}}}
\end{{table*}}

The open-search sector is highly stable across agents.  Every proposal policy finds an Einstein--Hilbert-anchored basin below the fixed $\Lambda$CDM reference value $\chi^2_{{\Lambda{{\rm CDM}}}}=1645.28$.  The best open-search value is obtained by {best_open['label']}, with $\chiT={best_open['open_search_best']:.3f}$.  The spread among the best open-search values is small, about {max(m['open_search_best'] for m in metrics)-min(m['open_search_best'] for m in metrics):.3f} in $\chi^2$, even though the agents differ substantially in accepted medians and hit counts.  This indicates that the background likelihood contains a broad EH-anchored attractor: many operator lists and scalar choices reproduce nearly the same late-time expansion history once the Solver is allowed to scan the explicit parameter samples.

\begin{{figure*}}[t]
\centering
\includegraphics[width=0.88\textwidth]{{figures/agent_best_h_lcdm.pdf}}
\caption{{Replayed best-agent background histories compared with the same fixed $\Lambda$CDM reference used in Eq.~\eqref{{eq:lcdm-reference}}.  The upper panel shows $h(z)=H(z)/H_0$ for the best representative background from each agent, and the lower panel shows the percent residual relative to $\Lambda$CDM.  This diagnostic uses the dedicated Solver replay curves because the production JSONL pull stores rankings and accepted samples but not every solution-curve CSV.}}
\label{{fig:agent-best-h-lcdm}}
\end{{figure*}}

\begin{{figure*}}[t]
\centering
\includegraphics[width=0.88\textwidth]{{figures/best_so_far_open_search.pdf}}
\caption{{Best-so-far open-search value as a function of completed open-search initial records.  The dashed line is the fixed $\Lambda$CDM reference.}}
\label{{fig:best-so-far-open}}
\end{{figure*}}

\begin{{figure*}}[t]
\centering
\includegraphics[width=0.88\textwidth]{{figures/non_eh_summary.pdf}}
\caption{{Non-EH search summary.  The left panel shows the best non-EH background found by each agent, restricted to the display range below $\chi^2=2000$; the dashed reference line is the fixed $\Lambda$CDM value from Eq.~\eqref{{eq:lcdm-reference}}.  The right panel counts non-EH hits below $\chi^2=2000$.}}
\label{{fig:noneh-summary}}
\end{{figure*}}

\subsection{{Open-search sector}}
\label{{subsec:open-search-results}}

Figure~\ref{{fig:best-so-far-open}} shows that the open-search optimum is usually found well before the full target budget is exhausted.  GPT-5.5, Gemini 3.1, Qwen 3.7, and DeepSeek V4 all reach $\chiT<1638.1$, while Claude Opus 4.8 reaches $\chiT=1638.004$.  The most stable open-search medians are obtained by GPT-5.5, Gemini, and Qwen; Claude has a competitive best value but a much worse open-search median because many of its accepted backgrounds sit on the high-$\chi^2$ plateau.  This distinction is important: the best value measures global optimization, whereas the accepted median and hit count measure how reliably the agent returns to the good basin.

The representative open-search theories in Appendix~\ref{{app:representatives}} show that the optimum is not tied to a single visible operator.  Some best models are nearly EH plus scalar, while others contain curvature corrections such as $R^2$, $\phi_1R^2$, or scalar-coupled Riemann/Ricci-squared terms.  At the background level these alternatives are largely degenerate.  We therefore treat the open-search result as evidence for a robust EH-anchored dark-energy basin, not as evidence that the data uniquely prefer one higher-curvature completion.

\subsection{{Non-EH sector}}
\label{{subsec:noneh-results}}

The non-EH sector remains the harder new-physics test because the bare Einstein--Hilbert anchor is absent.  In this sector, the best result is obtained by {best_non['label']} with $\chiT={best_non['non_eh_best']:.3f}$.  The corresponding structure is a two-scalar branch containing $\phi_2^2R$ and derivative scalar interactions.  Qwen finds a distinct $\phi_2$-only curvature branch at $\chiT=1896.001$, while Claude and Gemini find non-EH branches near $\chiT=1930.880$ and $\chiT=1939.014$.  GPT-5.5 reaches the familiar $\chiT\simeq1946.871$ plateau but finds only three hits below 2000 in the censored run.

\begin{{figure*}}[t]
\centering
\includegraphics[width=0.88\textwidth]{{figures/best_so_far_non_eh.pdf}}
\caption{{Best-so-far non-EH value as a function of completed non-EH initial records, plotted only after the best-so-far value enters the $\chi^2<2000$ display range.  The dashed reference line is the fixed $\Lambda$CDM value, not the non-EH refinement threshold.}}
\label{{fig:best-so-far-noneh}}
\end{{figure*}}

The contrast between open search and non-EH search is the main physics message of the benchmark.  All agents can locate a good EH-anchored expansion history, but only a subset repeatedly finds non-EH backgrounds below $\chi^2=2000$.  Even the best such background remains worse than $\Lambda$CDM by roughly {best_non['non_eh_best']-LCDM_CHI2:.1f} in $\chi^2$ and worse than the best open-search branch by roughly {best_non['non_eh_best']-best_open['open_search_best']:.1f}.  Thus the non-EH candidates are interesting as discovered runnable structures, not as competitive replacements for the EH-anchored basin on DES-SN plus DESI-DR2 BAO background data.

\subsection{{Agent-level behavior}}
\label{{subsec:agent-comparison}}

\begin{{figure}}[t]
\centering
\includegraphics[width=0.48\textwidth]{{figures/sector_acceptance.pdf}}
\caption{{Accepted fraction by sector.  Acceptance is a robustness diagnostic: it measures how often an agent reaches a Solver-evaluable background, not whether the resulting background has a low $\chi^2$.}}
\label{{fig:sector-acceptance}}
\end{{figure}}

\begin{{figure}}[t]
\centering
\includegraphics[width=0.48\textwidth]{{figures/speed_quality_tradeoff.pdf}}
\caption{{Speed and global optimum.  The horizontal axis gives initial theories per wall hour; the vertical axis gives the best open-search $\chi^2$.  GPT-5.5 is shown as a censored run because it reached the wall-time limit before recording all 1500 initial theories.}}
\label{{fig:speed-quality}}
\end{{figure}}

The five agents separate along different axes.  Qwen gives the best open-search minimum in the unified data set.  DeepSeek gives the strongest non-EH discovery and the largest number of non-EH hits below 2000.  GPT-5.5 gives a very stable open-search basin, with a low median and many hits below 1650, but its non-EH performance is weak and the job was wall-time censored.  Claude has the highest non-EH acceptance rate among the three new 1500-target agents, but its open-search accepted median is poor.  Gemini is balanced: it reaches a competitive open-search optimum and finds a non-EH branch below 2000, though it does not match DeepSeek's non-EH discovery.

\section{{Validation Boundaries and Physical Interpretation}}
\label{{sec:validation-boundaries}}

The validation performed here is a background-level filter, not a complete proof of covariant viability.  The symbolic stage removes independent higher-time derivatives in the homogeneous FLRW equations and the Solver enforces regular integration, the modified Friedmann constraint, and the data likelihood.  A fully viable theory must still pass perturbation-level tests: after solving nondynamical constraints, the scalar and tensor quadratic actions must have positive kinetic eigenvalues, acceptable sound speeds, no rapid gradient instabilities, and a regular constraint structure.  The present DES-SN plus DESI-DR2 BAO likelihood also does not include structure growth, weak lensing, redshift-space distortions, gravitational-wave propagation, or local-gravity screening.

The EFT interpretation is likewise diagnostic rather than automatic.  The trajectory-level cut controls $|H|/\Lambda$, but broad coefficient and scalar priors can still produce branches whose fitted corrections are large compared with the EH term.  Accepted operator lists also need not be inequivalent covariant theories: integration by parts, field redefinitions, curvature identities, and FLRW degeneracies can map different raw operator lists to the same background equations.  The results should therefore be read as best-per-family background representatives, pending a full operator-basis and perturbation audit.

\section{{Discussion and Conclusions}}
\label{{sec:conclusion}}

The unified benchmark shows that autonomous proposal agents can reliably recover high-quality EH-anchored dark-energy backgrounds under a deterministic modified-gravity validation pipeline.  The best open-search backgrounds improve the fixed $\Lambda$CDM reference by $\Delta\chi^2\simeq7.2$--$7.35$, and the differences among the best agents are small compared with the gap between open search and the non-EH sector.

The non-EH results are more discriminating.  DeepSeek's $\chiT=1693.860$ branch is the most interesting new-physics candidate found in these data: it is substantially better than the recurring $\chiT\simeq1946.87$ plateau and is structurally simple.  Nevertheless, it is still worse than the $\Lambda$CDM reference and much worse than the EH-anchored basin.  The current background data and priors therefore favor EH-anchored scalar histories, while non-EH backgrounds remain useful diagnostic targets for further search.

At the agent level, no single metric captures performance.  The relevant axes are global optimum, new-physics discovery, speed/efficiency, robustness/stability, and acceptance rate.  For future production searches, a practical strategy is to use a strong global optimizer for EH-anchored basins and a separate explorer tuned for the non-EH sector.  Follow-up work should add perturbation-level stability, growth and lensing likelihoods, gravitational-wave propagation constraints, local-gravity screening checks, and an operator-basis audit that removes FLRW-equivalent representatives.

\appendix
\section{{Representative Accepted Theories}}
\label{{app:representatives}}

This appendix lists compact coefficient-substituted representatives for the best open-search and non-EH families used in the unified benchmark.  Coefficients whose recovered value is exactly zero are omitted.  For GPT-5.5, Claude Opus 4.8, and Gemini 3.1 Pro the coefficients are read from the pulled Solver CSV files.  For Qwen and DeepSeek, which are taken from the earlier truncated 2000-run artifacts, the exact per-task Solver CSV files were not pulled; when necessary we use the recovered current-loop parameter memory and mark this explicitly.

We use the abbreviations
\begin{{align}}
{{\cal R}}_{{3a}}&=R^{{cd}}{{}}_{{ab}}R^{{afh}}{{}}_cR^b{{}}_{{fdh}},&
{{\cal R}}_{{3b}}&=R^{{bd}}{{}}_{{ac}}R^{{agh}}{{}}_bR^c{{}}_{{dgh}},\\
{{\cal R}}_{{3c}}&=R^b{{}}_aR^{{cd}}R^a{{}}_{{cbd}},&
{{\cal R}}_{{3d}}&=R_{{ab}}R^{{adef}}R^b{{}}_{{def}} .
\end{{align}}

{appendix_representative_tex(reps)}
"""


def replace_block(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + replacement + "\n\n" + text[end:]


def build_tex(metrics: list[dict[str, Any]], reps: list[dict[str, Any]]) -> None:
    src = (WORK / "main8_cmp600_final.tex").read_text(encoding="utf-8")
    src = re.sub(
        r"\\begin\{abstract\}.*?\\end\{abstract\}",
        lambda _m: "\\begin{abstract}\n" + new_abstract(metrics) + "\n\\end{abstract}",
        src,
        flags=re.S,
    )
    src = replace_block(src, r"\subsection{Benchmark design and monitoring}", r"\section{Benchmark Results}", benchmark_design_tex())
    src = replace_block(src, r"\section{Benchmark Results}", r"\bibliographystyle", results_tex(metrics, reps))
    (OUT / "main8_cmp1500_unified_results.tex").write_text(src, encoding="utf-8")


def copy_template() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    FIG_DIR.mkdir(parents=True)
    DATA_DIR.mkdir(parents=True)
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    with zipfile.ZipFile(SOURCE_ZIP) as zf:
        zf.extractall(WORK)
    shutil.copy2(WORK / "main2.bib", OUT / "main2.bib")


def write_readme(metrics: list[dict[str, Any]]) -> None:
    lines = [
        "# Unified cmp1500 agent result package",
        "",
        "This package was generated from local pulled JSONL/CSV artifacts.",
        "GPT-5.5, Claude Opus 4.8, and Gemini 3.1 Pro use the cmp1500 production runs.",
        "Qwen 3.7 Plus and DeepSeek V4 Pro use the first 1500 task ids from the earlier cmp2000 run.",
        "No run-source distinction is used in the figures.",
        "",
        "## Metrics",
    ]
    for m in label_order(metrics):
        lines.append(
            f"- {m['label']}: initial={m['initial_recorded']}/1500, "
            f"open_best={m['open_search_best']:.3f}, non_eh_best={m['non_eh_best']:.3f}, "
            f"status={m['status']}"
        )
    (OUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def zip_output() -> Path:
    zip_path = ROOT / "overleaf_cmp1500_agent_results_v1.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in OUT.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(OUT.parent))
    return zip_path


def sanity_check() -> None:
    tex = (OUT / "main8_cmp1500_unified_results.tex").read_text(encoding="utf-8")
    for required in [
        r"\section{Benchmark Results}",
        r"\appendix",
        r"\section{Representative Accepted Theories}",
        r"figures/agent_best_h_lcdm.pdf",
    ]:
        if required not in tex:
            raise RuntimeError(f"missing TeX marker: {required}")
    if "cheap_v1" in tex or "expensive_v1" in tex:
        raise RuntimeError("run-label suffix leaked into TeX")
    if tex.count(r"\begin{equation}") != tex.count(r"\end{equation}"):
        raise RuntimeError("equation environment mismatch")
    for figure in [
        FIG_DIR / "agent_best_h_lcdm.pdf",
        FIG_DIR / "agent_best_h_lcdm.png",
    ]:
        if not figure.exists():
            raise RuntimeError(f"missing generated figure: {figure}")


def main() -> None:
    copy_template()
    set_plot_style()
    metrics, rows_by_agent = build_metrics()
    reps = select_representatives(rows_by_agent)
    write_metrics(metrics)
    write_representatives(reps)
    plot_dashboard(metrics)
    plot_non_eh(metrics)
    plot_acceptance(metrics)
    plot_speed_quality(metrics)
    copy_h_lcdm_replay_figure()
    plot_best_so_far(rows_by_agent, "open_search", "best_so_far_open_search", (1637.85, 1645.8))
    plot_best_so_far(rows_by_agent, "non_eh", "best_so_far_non_eh", (1635.0, 2050.0))
    build_tex(metrics, reps)
    write_readme(metrics)
    sanity_check()
    zip_path = zip_output()
    print(OUT)
    print(zip_path)
    for m in label_order(metrics):
        print(
            f"{m['label']}: open={m['open_search_best']:.3f} "
            f"non_eh={m['non_eh_best']:.3f} initial={m['initial_recorded']}/1500 status={m['status']}"
        )


if __name__ == "__main__":
    main()
