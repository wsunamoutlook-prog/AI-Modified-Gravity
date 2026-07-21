"""Build a PRD-style Overleaf package for the cmp600/cmp2000 agent comparison.

This is an offline report builder.  It reads only local pulled JSONL/JSON/CSV
artifacts under cluster_report/ and writes a self-contained Overleaf folder.
"""

from __future__ import annotations

import csv
import json
import math
import re
import shutil
import statistics
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CMP600 = ROOT / "cluster_report" / "cmp600_final_v1"
CMP2000 = ROOT / "cluster_report" / "cmp2000_cheap_partial_v1_full"
OUT = ROOT / "overleaf_cmp2000_comparison_v1"
FIG_DIR = OUT / "figures"
DATA_DIR = OUT / "data"
MAIN8 = Path("/Users/sunwenrong/Desktop/main8.tex")
LCDM_CHI2 = 1645.28


RUNS_600 = {
    "openai": "cmp600_openai_gpt_5_5_final_v1",
    "claude": "cmp600_claude_opus_4_8_final_v1",
    "gemini": "cmp600_gemini_3_1_pro_final_v1",
    "qwen": "cmp600_qwen3_7_plus_final_v1",
    "deepseek": "cmp600_deepseek_ali_v4_pro_final_v1",
}

RUNS_2000 = {
    "openai": "cmp2000_openai_gpt_5_4_mini_cheap_v1",
    "claude": "cmp2000_claude_sonnet_4_6_cheap_v1",
    "gemini": "cmp2000_gemini_2_5_flash_cheap_v1",
    "qwen": "cmp2000_qwen3_7_plus_cheap_v1",
    "deepseek": "cmp2000_deepseek_ali_v4_pro_cheap_v1",
}

AGENT_LABEL = {
    "openai": "OpenAI",
    "claude": "Claude",
    "gemini": "Gemini",
    "qwen": "Qwen",
    "deepseek": "DeepSeek",
}

MODEL_600 = {
    "openai": "GPT-5.5",
    "claude": "Claude Opus 4.8",
    "gemini": "Gemini 3.1 Pro",
    "qwen": "Qwen 3.7 Plus",
    "deepseek": "DeepSeek V4 Pro",
}

MODEL_2000 = {
    "openai": "GPT-5.4 Mini",
    "claude": "Claude Sonnet 4.6",
    "gemini": "Gemini 2.5 Flash",
    "qwen": "Qwen 3.7 Plus",
    "deepseek": "DeepSeek V4 Pro",
}

COLOR = {
    "openai": "#4C78A8",
    "claude": "#F58518",
    "gemini": "#54A24B",
    "qwen": "#B279A2",
    "deepseek": "#E45756",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            out.append(value)
    return out


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


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


def finite_float(value: Any) -> float | None:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def theory(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("theory") if isinstance(row.get("theory"), dict) else {}


def group(row: dict[str, Any]) -> str:
    th = theory(row)
    return str(row.get("proposal_group") or th.get("proposal_group") or "unknown")


def scalar(row: dict[str, Any]) -> str:
    return str(theory(row).get("scalar_config") or "unknown")


def operators(row: dict[str, Any]) -> list[str]:
    ops = theory(row).get("operators") or []
    return [str(op) for op in ops]


def potential_text(row: dict[str, Any]) -> str:
    pot = theory(row).get("potential_types") or {}
    if not isinstance(pot, dict):
        return "-"
    vals = []
    for key in ("phi1", "phi2"):
        if pot.get(key):
            vals.append(f"{key}={pot[key]}")
    return ", ".join(vals) if vals else "-"


def family_key(row: dict[str, Any]) -> str:
    if row.get("family_key"):
        return str(row["family_key"])
    payload = {
        "scalar": scalar(row),
        "potential": theory(row).get("potential_types"),
        "operators": operators(row),
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def stage(row: dict[str, Any]) -> str:
    explicit = row.get("validation_stage")
    if explicit:
        return str(explicit)
    loop_id = str(row.get("loop_id") or "")
    if "_expanded_refine_" in loop_id or "_refine_" in loop_id:
        return "refine"
    if "_expanded_" in loop_id:
        return "expanded"
    return "initial"


def accepted(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in rows if r.get("validated") and finite_float(r.get("chi2")) is not None]


def best_row(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    acc = accepted(rows)
    if not acc:
        return None
    return min(acc, key=lambda r: float(r["chi2"]))


def best_chi(rows: list[dict[str, Any]]) -> float | None:
    r = best_row(rows)
    return float(r["chi2"]) if r else None


def median_chi(rows: list[dict[str, Any]]) -> float | None:
    vals = sorted(float(r["chi2"]) for r in accepted(rows))
    return statistics.median(vals) if vals else None


def wall_hours(events: list[dict[str, Any]], rows: list[dict[str, Any]]) -> float | None:
    times = [parse_time(e.get("timestamp")) for e in events]
    times = [t for t in times if t is not None]
    if len(times) >= 2:
        return max(0.0, (max(times) - min(times)).total_seconds() / 3600.0)
    times = [parse_time(r.get("timestamp")) for r in rows]
    times = [t for t in times if t is not None]
    if len(times) >= 2:
        return max(0.0, (max(times) - min(times)).total_seconds() / 3600.0)
    return None


@dataclass
class RunBundle:
    cohort: str
    agent: str
    run_name: str
    model_label: str
    memory_dir: Path
    proposal_dir: Path
    report_dir: Path | None
    rows: list[dict[str, Any]]
    events: list[dict[str, Any]]


def load_bundles() -> list[RunBundle]:
    bundles: list[RunBundle] = []
    for agent, run in RUNS_600.items():
        bundles.append(
            RunBundle(
                cohort="flagship-600",
                agent=agent,
                run_name=run,
                model_label=MODEL_600[agent],
                memory_dir=CMP600 / "memory" / run,
                proposal_dir=CMP600 / "proposals" / run,
                report_dir=CMP600 / run,
                rows=read_jsonl(CMP600 / "memory" / run / "attempt_history.jsonl"),
                events=read_jsonl(CMP600 / "proposals" / run / "scheduler_tasks.jsonl"),
            )
        )
    for agent, run in RUNS_2000.items():
        bundles.append(
            RunBundle(
                cohort="cheap-2000 partial",
                agent=agent,
                run_name=run,
                model_label=MODEL_2000[agent],
                memory_dir=CMP2000 / "memory" / run,
                proposal_dir=CMP2000 / "proposals" / run,
                report_dir=CMP2000 / "reports" / run,
                rows=read_jsonl(CMP2000 / "memory" / run / "attempt_history.jsonl"),
                events=read_jsonl(CMP2000 / "proposals" / run / "scheduler_tasks.jsonl"),
            )
        )
    return bundles


def latest_progress(events: list[dict[str, Any]]) -> dict[str, Any]:
    if not events:
        return {}
    complete = any(e.get("event") == "scheduler_complete" for e in events)
    latest = events[-1]
    return {
        "target": latest.get("target_attempts"),
        "submitted": latest.get("submitted_total"),
        "recorded": latest.get("recorded_total"),
        "complete": complete,
        "latest_event": latest.get("event"),
    }


def sector_metrics(rows: list[dict[str, Any]], sector: str) -> dict[str, Any]:
    sub = [r for r in rows if group(r) == sector]
    sub_initial = [r for r in sub if stage(r) == "initial"]
    acc = accepted(sub)
    chis = sorted(float(r["chi2"]) for r in acc)
    return {
        "attempts": len(sub),
        "initial_attempts": len(sub_initial),
        "accepted": len(acc),
        "accept_rate": len(acc) / len(sub) if sub else 0.0,
        "best": min(chis) if chis else None,
        "median": statistics.median(chis) if chis else None,
        "hits_lt_2000": sum(c < 2000 for c in chis),
        "hits_lt_1650": sum(c < 1650 for c in chis),
        "unique_families": len({family_key(r) for r in sub}),
        "unique_good_families": len({family_key(r) for r in acc if float(r["chi2"]) < (2000 if sector == "non_eh" else 1650)}),
    }


def build_metrics(bundles: list[RunBundle]) -> list[dict[str, Any]]:
    metrics: list[dict[str, Any]] = []
    for b in bundles:
        acc = accepted(b.rows)
        progress = latest_progress(b.events)
        hours = wall_hours(b.events, b.rows)
        open_m = sector_metrics(b.rows, "open_search")
        non_m = sector_metrics(b.rows, "non_eh")
        metrics.append(
            {
                "cohort": b.cohort,
                "agent": b.agent,
                "agent_label": AGENT_LABEL[b.agent],
                "model": b.model_label,
                "run_name": b.run_name,
                "records": len(b.rows),
                "initial_records": sum(1 for r in b.rows if stage(r) == "initial"),
                "accepted": len(acc),
                "accepted_rate": len(acc) / len(b.rows) if b.rows else 0.0,
                "best_chi2": best_chi(b.rows),
                "target": progress.get("target") or (600 if b.cohort.startswith("flagship") else 2000),
                "recorded_initial": progress.get("recorded") or sum(1 for r in b.rows if stage(r) == "initial"),
                "submitted_initial": progress.get("submitted"),
                "scheduler_complete": progress.get("complete"),
                "wall_hours": hours,
                "initial_attempts_per_hour": (sum(1 for r in b.rows if stage(r) == "initial") / hours) if hours else None,
                "records_per_hour": (len(b.rows) / hours) if hours else None,
                **{f"open_{k}": v for k, v in open_m.items()},
                **{f"non_eh_{k}": v for k, v in non_m.items()},
            }
        )
    return metrics


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def setup_plot() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "mathtext.fontset": "cm",
            "axes.labelsize": 10,
            "axes.titlesize": 11,
            "xtick.labelsize": 8.5,
            "ytick.labelsize": 8.5,
            "legend.fontsize": 8.5,
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def savefig(fig: plt.Figure, name: str) -> None:
    for ext in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"{name}.{ext}", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def valfmt(value: float | None, nd: int = 3) -> str:
    if value is None or not math.isfinite(float(value)):
        return "n/a"
    return f"{float(value):.{nd}f}"


def agent_order() -> list[str]:
    return ["deepseek", "openai", "claude", "gemini", "qwen"]


def plot_figures(metrics: list[dict[str, Any]], bundles: list[RunBundle]) -> None:
    setup_plot()
    by = {(m["cohort"], m["agent"]): m for m in metrics}
    order = agent_order()

    # Fig. 1: improvement vs LCDM, positive is better.
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    x = np.arange(len(order))
    width = 0.36
    for j, cohort in enumerate(["flagship-600", "cheap-2000 partial"]):
        vals = [LCDM_CHI2 - (by[(cohort, a)]["open_best"] or float("nan")) for a in order]
        pos = x + (j - 0.5) * width
        bars = ax.bar(pos, vals, width=width, label=cohort, color=["#9ecae1", "#fdae6b"][j], edgecolor="black", linewidth=0.4)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, val + 0.05, f"{val:.2f}", ha="center", va="bottom", fontsize=7.5)
    ax.axhline(0, color="black", linewidth=0.7)
    ax.set_ylabel(r"$\Delta\chi^2_{\Lambda{\rm CDM}}=\chi^2_{\Lambda{\rm CDM}}-\chi^2_{\rm best}$")
    ax.set_title("Open-search improvement over LCDM")
    ax.set_xticks(x, [AGENT_LABEL[a] for a in order], rotation=20, ha="right")
    ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.18), fontsize=7.2)
    ax.grid(axis="y", alpha=0.25)
    savefig(fig, "fig1_open_search_lcdm_improvement")

    # Fig. 2: open-search best and low-chi2 hit count.
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.9), gridspec_kw={"width_ratios": [1.15, 1.0]})
    ax = axes[0]
    for cohort, marker, offset, yoff in [
        ("flagship-600", "o", -0.08, 0.12),
        ("cheap-2000 partial", "s", 0.08, -0.16),
    ]:
        y = [by[(cohort, a)]["open_best"] for a in order]
        ax.scatter(x + offset, y, marker=marker, s=42, label=cohort, edgecolor="black", linewidth=0.4)
        for xi, yi in zip(x + offset, y):
            va = "bottom" if yoff >= 0 else "top"
            ax.text(xi, yi + yoff, f"{yi:.3f}", ha="center", va=va, fontsize=6.3, rotation=0)
    ax.axhline(LCDM_CHI2, color="gray", linestyle="--", linewidth=0.8)
    ax.text(len(order) - 0.05, LCDM_CHI2 - 0.08, r"$\Lambda$CDM 1645.28", ha="right", va="top", fontsize=6.6, color="dimgray")
    ax.set_ylabel(r"best open-search $\chi^2_{\rm tot}$")
    ax.set_xticks(x, [AGENT_LABEL[a] for a in order], rotation=25, ha="right")
    ax.set_ylim(1637.75, 1645.75)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.52, 1.18), ncol=2)

    ax = axes[1]
    for j, cohort in enumerate(["flagship-600", "cheap-2000 partial"]):
        vals = [by[(cohort, a)]["open_hits_lt_1650"] for a in order]
        pos = x + (j - 0.5) * width
        bars = ax.bar(pos, vals, width=width, label=cohort, color=["#9ecae1", "#fdae6b"][j], edgecolor="black", linewidth=0.4)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, val + 3, f"{int(val)}", ha="center", va="bottom", fontsize=7)
    ax.set_ylabel(r"open-search hits with $\chi^2<1650$")
    ax.set_xticks(x, [AGENT_LABEL[a] for a in order], rotation=25, ha="right")
    ax.grid(axis="y", alpha=0.25)
    savefig(fig, "fig2_open_search_best_and_hits")

    # Fig. 3: non-EH search below 2000 only.
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.9), gridspec_kw={"width_ratios": [1.05, 1.0]})
    ax = axes[0]
    for cohort, marker, offset, yoff in [
        ("flagship-600", "o", -0.08, 9.0),
        ("cheap-2000 partial", "s", 0.08, -10.0),
    ]:
        y = []
        for a in order:
            v = by[(cohort, a)]["non_eh_best"]
            y.append(v if v is not None and v < 2000 else np.nan)
        ax.scatter(x + offset, y, marker=marker, s=42, label=cohort, edgecolor="black", linewidth=0.4)
        for xi, yi in zip(x + offset, y):
            if np.isfinite(yi):
                va = "bottom" if yoff >= 0 else "top"
                ax.text(xi, yi + yoff, f"{yi:.1f}", ha="center", va=va, fontsize=6.8)
    ax.set_ylabel(r"best non-EH $\chi^2_{\rm tot}$ below 2000")
    ax.set_xticks(x, [AGENT_LABEL[a] for a in order], rotation=25, ha="right")
    ax.set_ylim(1650, 2005)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, 1.18), ncol=2)
    ax = axes[1]
    for j, cohort in enumerate(["flagship-600", "cheap-2000 partial"]):
        vals = [by[(cohort, a)]["non_eh_hits_lt_2000"] for a in order]
        pos = x + (j - 0.5) * width
        bars = ax.bar(pos, vals, width=width, label=cohort, color=["#bcbddc", "#74c476"][j], edgecolor="black", linewidth=0.4)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, val + 0.6, f"{int(val)}", ha="center", va="bottom", fontsize=7)
    ax.set_ylabel(r"non-EH hits with $\chi^2<2000$")
    ax.set_xticks(x, [AGENT_LABEL[a] for a in order], rotation=25, ha="right")
    ax.grid(axis="y", alpha=0.25)
    savefig(fig, "fig3_non_eh_best_and_hits")

    # Fig. 4: acceptance rates.
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.7), sharey=True)
    for ax, cohort in zip(axes, ["flagship-600", "cheap-2000 partial"]):
        open_vals = [by[(cohort, a)]["open_accept_rate"] for a in order]
        non_vals = [by[(cohort, a)]["non_eh_accept_rate"] for a in order]
        ax.bar(x - width / 2, open_vals, width=width, label="open search", color="#4C78A8", edgecolor="black", linewidth=0.4)
        ax.bar(x + width / 2, non_vals, width=width, label="non-EH", color="#F58518", edgecolor="black", linewidth=0.4)
        ax.set_title(cohort)
        ax.set_xticks(x, [AGENT_LABEL[a] for a in order], rotation=25, ha="right")
        ax.grid(axis="y", alpha=0.25)
    axes[0].set_ylabel("accepted / attempted")
    axes[1].legend(frameon=False, fontsize=7, loc="upper right")
    savefig(fig, "fig4_sector_acceptance_rates")

    # Fig. 5: speed vs quality.
    fig, ax = plt.subplots(figsize=(5.7, 3.5))
    for cohort, marker in [("flagship-600", "o"), ("cheap-2000 partial", "s")]:
        for a in order:
            m = by[(cohort, a)]
            speed = m["initial_attempts_per_hour"]
            quality = m["open_best"]
            if speed is None or quality is None:
                continue
            size = 35 + 5 * m["non_eh_hits_lt_2000"]
            ax.scatter(speed, quality, marker=marker, s=size, color=COLOR[a], edgecolor="black", linewidth=0.5, alpha=0.85)
    ax.set_xlabel("initial theories per wall hour")
    ax.set_ylabel(r"best open-search $\chi^2_{\rm tot}$")
    ax.set_title("Speed-quality tradeoff; marker size tracks non-EH hits")
    ax.invert_yaxis()
    ax.grid(alpha=0.25)
    import matplotlib.lines as mlines
    agent_handles = [
        mlines.Line2D([], [], color=COLOR[a], marker="o", linestyle="None", markersize=5, label=AGENT_LABEL[a])
        for a in order
    ]
    cohort_handles = [
        mlines.Line2D([], [], color="black", marker="o", linestyle="None", markersize=5, label="flagship-600"),
        mlines.Line2D([], [], color="black", marker="s", linestyle="None", markersize=5, label="cheap-2000"),
    ]
    leg1 = ax.legend(handles=agent_handles, frameon=False, fontsize=6.4, loc="upper right", ncol=1)
    ax.add_artist(leg1)
    ax.legend(handles=cohort_handles, frameon=False, fontsize=6.4, loc="lower right")
    savefig(fig, "fig5_speed_quality_tradeoff")

    # Best-so-far curves.
    bundle_map = {(b.cohort, b.agent): b for b in bundles}
    for sector, threshold, name, ylabel in [
        ("open_search", 1650.0, "fig6_best_so_far_open_search", r"best-so-far open-search $\chi^2$"),
        ("non_eh", 2000.0, "fig7_best_so_far_non_eh", r"best-so-far non-EH $\chi^2$ below 2000"),
    ]:
        fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.9), sharey=False)
        for ax, cohort in zip(axes, ["flagship-600", "cheap-2000 partial"]):
            for a in order:
                b = bundle_map[(cohort, a)]
                rows = [r for r in b.rows if stage(r) == "initial" and group(r) == sector]
                rows = sorted(rows, key=lambda r: str(r.get("loop_id") or ""))
                xs, ys = [], []
                best = float("inf")
                count = 0
                for r in rows:
                    count += 1
                    if r.get("validated") and finite_float(r.get("chi2")) is not None:
                        c = float(r["chi2"])
                        if sector == "open_search" or c < threshold:
                            best = min(best, c)
                    if math.isfinite(best):
                        xs.append(count)
                        ys.append(best)
                if xs:
                    ax.plot(xs, ys, label=AGENT_LABEL[a], color=COLOR[a], linewidth=1.25)
            ax.set_title(cohort)
            ax.set_xlabel("initial attempts in sector")
            ax.grid(alpha=0.25)
            if sector == "open_search":
                ax.set_ylim(1637.75, 1650.5)
                ax.invert_yaxis()
            else:
                ax.set_ylim(1650, 2000)
                ax.invert_yaxis()
        axes[0].set_ylabel(ylabel)
        axes[1].legend(frameon=False, fontsize=6.8, loc="upper right")
        savefig(fig, name)

    # Fig. 8: completion/censoring.
    fig, ax = plt.subplots(figsize=(6.8, 2.8))
    cohorts = ["flagship-600", "cheap-2000 partial"]
    for j, cohort in enumerate(cohorts):
        vals = [100 * (by[(cohort, a)]["recorded_initial"] or 0) / (by[(cohort, a)]["target"] or 1) for a in order]
        pos = x + (j - 0.5) * width
        bars = ax.bar(pos, vals, width=width, label=cohort, color=["#9ecae1", "#fdae6b"][j], edgecolor="black", linewidth=0.4)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, min(val + 2, 105), f"{val:.0f}%", ha="center", va="bottom", fontsize=7)
    ax.axhline(100, color="black", linewidth=0.7)
    ax.set_ylim(0, 112)
    ax.set_ylabel("initial target recorded")
    ax.set_title("Run completion: cheap 2000-target jobs are 72-hour censored")
    ax.set_xticks(x, [AGENT_LABEL[a] for a in order], rotation=25, ha="right")
    ax.legend(frameon=False, fontsize=7, loc="lower right")
    ax.grid(axis="y", alpha=0.25)
    savefig(fig, "fig8_run_completion")


def proposal_json_path(bundle: RunBundle, loop_id: str) -> Path | None:
    base = loop_id
    if base.endswith("_lag_1"):
        fname = f"{base}.json"
    else:
        fname = f"{base}_lag_1.json"
    path = bundle.proposal_dir / fname
    if path.exists():
        return path
    # Expanded/refine rows may point back to the expanded proposal file.
    candidates = list(bundle.proposal_dir.glob(f"{base}*.json"))
    if candidates:
        return candidates[0]
    return None


def build_vector_index(memory_dir: Path) -> dict[str, list[dict[str, Any]]]:
    path = memory_dir / "joint_parameter_prior.json"
    obj = read_json(path)
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    families = obj.get("families") if isinstance(obj.get("families"), dict) else {}
    for level_payload in families.values():
        if not isinstance(level_payload, dict):
            continue
        for family_payload in level_payload.values():
            if not isinstance(family_payload, dict):
                continue
            for vec in family_payload.get("top_vectors") or []:
                if not isinstance(vec, dict):
                    continue
                lid = str(vec.get("loop_id") or "")
                if lid:
                    out[lid].append(vec)
    return out


def vector_for_row(index: dict[str, list[dict[str, Any]]], row: dict[str, Any]) -> dict[str, Any] | None:
    lid = str(row.get("loop_id") or "")
    options = index.get(lid, [])
    if not options:
        return None
    target = finite_float(row.get("chi2"))
    if target is None:
        return options[0]
    return min(options, key=lambda v: abs((finite_float(v.get("chi2")) or 1e99) - target))


def tex_escape_text(text: str) -> str:
    repl = {
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    return text


def op_to_tex(op: str) -> str:
    s = op
    s = s.replace("∇^{a}∇_{a}", r"\Box ")
    s = s.replace("φ1", r"\phi_1").replace("φ2", r"\phi_2")
    s = s.replace("∇", r"\nabla")
    s = s.replace("Λ", r"\Lambda")
    s = s.replace("·", r"\,")
    # Keep grammar indices as a compact audit notation.
    return s


def coeff_to_tex(symbol: str) -> str:
    return symbol.replace("\\", "\\")


def latex_number(value: Any, sig: int = 4) -> str:
    val = finite_float(value)
    if val is None:
        return r"{\rm n/a}"
    if val == 0:
        return "0"
    av = abs(val)
    if 1e-3 <= av < 1e4:
        return f"{val:.{sig}g}"
    exp = int(math.floor(math.log10(av)))
    mant = val / (10 ** exp)
    return rf"{mant:.{sig-1}g}\times10^{{{exp}}}"


def compact_ops(ops: list[str], max_ops: int = 4) -> str:
    if len(ops) <= max_ops:
        return "; ".join(ops)
    return "; ".join(ops[:max_ops]) + f"; +{len(ops)-max_ops} more"


def compact_ops_tex(ops: list[str], max_ops: int = 4) -> str:
    shown = [rf"${op_to_tex(op)}$" for op in ops[:max_ops]]
    if len(ops) > max_ops:
        shown.append(rf"$+{len(ops)-max_ops}$ more")
    return "; ".join(shown)


def selected_representatives(bundles: list[RunBundle]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    selected: list[dict[str, Any]] = []
    repeated: list[dict[str, Any]] = []

    # Per-agent best in both sectors for the cheap run; include non-EH only if
    # it reached the interesting new-physics threshold or is the sector leader.
    for b in bundles:
        if b.cohort != "cheap-2000 partial":
            continue
        for sec in ("open_search", "non_eh"):
            rows = [r for r in b.rows if group(r) == sec]
            r = best_row(rows)
            if not r:
                continue
            selected.append(
                {
                    "kind": "agent-sector-best",
                    "cohort": b.cohort,
                    "agent": b.agent,
                    "agent_label": AGENT_LABEL[b.agent],
                    "model": b.model_label,
                    "run_name": b.run_name,
                    "sector": sec,
                    "row": r,
                    "bundle": b,
                }
            )

    # Repeated good open-search families in the cheap run.
    fam_by_agent: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for b in bundles:
        if b.cohort != "cheap-2000 partial":
            continue
        for r in accepted(b.rows):
            if group(r) == "open_search" and float(r["chi2"]) < 1650:
                fam_by_agent[family_key(r)][b.agent].append(r)
    items: list[tuple[int, float, str, dict[str, list[dict[str, Any]]]]] = []
    for fam, byagent in fam_by_agent.items():
        if len(byagent) >= 5:
            best = min(float(r["chi2"]) for rows in byagent.values() for r in rows)
            items.append((len(byagent), best, fam, byagent))
    for _, _, fam, byagent in sorted(items, key=lambda x: (-x[0], x[1]))[:4]:
        best_agent = min(byagent, key=lambda a: min(float(r["chi2"]) for r in byagent[a]))
        best = min(byagent[best_agent], key=lambda r: float(r["chi2"]))
        repeated.append(
            {
                "family": fam,
                "agents": sorted(byagent),
                "best_agent": best_agent,
                "best_row": best,
                "best_chi2": float(best["chi2"]),
                "operator_content": operators(best),
                "scalar": scalar(best),
            }
        )

    # Repeated non-EH below 2000, if any exact family repeats.
    fam_by_agent = defaultdict(lambda: defaultdict(list))
    for b in bundles:
        if b.cohort != "cheap-2000 partial":
            continue
        for r in accepted(b.rows):
            if group(r) == "non_eh" and float(r["chi2"]) < 2000:
                fam_by_agent[family_key(r)][b.agent].append(r)
    for fam, byagent in fam_by_agent.items():
        if len(byagent) >= 2:
            best_agent = min(byagent, key=lambda a: min(float(r["chi2"]) for r in byagent[a]))
            best = min(byagent[best_agent], key=lambda r: float(r["chi2"]))
            repeated.append(
                {
                    "family": fam,
                    "agents": sorted(byagent),
                    "best_agent": best_agent,
                    "best_row": best,
                    "best_chi2": float(best["chi2"]),
                    "operator_content": operators(best),
                    "scalar": scalar(best),
                }
            )
    return selected, repeated


def lagrangian_terms_tex(row: dict[str, Any], sample: dict[str, Any] | None) -> tuple[str, str]:
    lag = (row.get("agent_lagrangian") or {}).get("lagrangian") or {}
    terms = lag.get("terms") or []
    pieces: list[str] = []
    coeffs: list[str] = []
    if not terms:
        # Fallback from theory operators.
        for i, op in enumerate(operators(row)):
            sym = [r"\alpha", r"\beta", r"\gamma", r"\delta", r"\epsilon", r"\zeta", r"\eta", r"\theta"][i % 8]
            pieces.append(rf"{sym}\,{op_to_tex(op)}")
        return " + ".join(pieces), ""

    for term in terms:
        if not isinstance(term, dict) or term.get("fixed"):
            continue
        sym = str(term.get("coeff_symbol") or "")
        op = str(term.get("candidate") or "")
        if not sym or sym == "1":
            continue
        value = None
        if sample:
            value = sample.get(sym)
        if finite_float(value) is not None and abs(float(value)) < 1e-14:
            continue
        power = term.get("lambda_power")
        lam = ""
        if isinstance(power, int) and power != 0:
            lam = rf"\Lambda^{{{power}}}\,"
        pieces.append(rf"{sym}\,{lam}{op_to_tex(op)}")
        if finite_float(value) is not None:
            coeffs.append(rf"{sym}={latex_number(value)}")
    fixed = []
    sc = scalar(row)
    if sc in ("phi1_only", "both"):
        fixed.append(r"\mathcal{L}_{\rm fixed}^{(1)}")
    if sc in ("phi2_only", "both"):
        fixed.append(r"\mathcal{L}_{\rm fixed}^{(2)}")
    body = r"\Mp^2\left[" + (" + ".join(pieces) if pieces else "0") + r"\right]"
    if fixed:
        body += " + " + " + ".join(fixed)
    return body, ",\\; ".join(coeffs)


def build_appendix_data(bundles: list[RunBundle]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, list[dict[str, Any]]]]]:
    selected, repeated = selected_representatives(bundles)
    index_cache: dict[str, dict[str, list[dict[str, Any]]]] = {}
    appendix_rows: list[dict[str, Any]] = []
    for item in selected:
        b: RunBundle = item["bundle"]
        row = item["row"]
        if b.run_name not in index_cache:
            index_cache[b.run_name] = build_vector_index(b.memory_dir)
        vec = vector_for_row(index_cache[b.run_name], row)
        sample = vec.get("sample") if isinstance(vec, dict) and isinstance(vec.get("sample"), dict) else None
        body, coeffs = lagrangian_terms_tex(row, sample)
        appendix_rows.append(
            {
                "agent": item["agent"],
                "agent_label": item["agent_label"],
                "model": item["model"],
                "sector": item["sector"],
                "loop_id": row.get("loop_id"),
                "chi2": float(row["chi2"]),
                "scalar": scalar(row),
                "potential": potential_text(row),
                "operators": operators(row),
                "lagrangian_body_tex": body,
                "coefficients_tex": coeffs,
                "sample": sample or {},
            }
        )
    return appendix_rows, repeated, index_cache


def tex_table_metrics(metrics: list[dict[str, Any]], cohort: str) -> str:
    rows = [m for m in metrics if m["cohort"] == cohort]
    rows.sort(key=lambda m: agent_order().index(m["agent"]))
    lines = []
    for m in rows:
        comp = rf"{int(m['recorded_initial'])}/{int(m['target'])}"
        lines.append(
            rf"{tex_escape_text(m['model'])} & {comp} & "
            rf"{valfmt(m['open_best'])} & {int(m['open_hits_lt_1650'])} & "
            rf"{valfmt(m['non_eh_best'])} & {int(m['non_eh_hits_lt_2000'])} & "
            rf"{m['open_accept_rate']:.3f} & {m['non_eh_accept_rate']:.3f} \\"
        )
    return "\n".join(lines)


def tex_best_sector_rows(app_rows: list[dict[str, Any]], sector: str) -> str:
    rows = [r for r in app_rows if r["sector"] == sector]
    rows.sort(key=lambda r: agent_order().index(r["agent"]))
    lines = []
    for r in rows:
        ops = compact_ops_tex(r["operators"], 3)
        lines.append(
            rf"{tex_escape_text(r['model'])} & {valfmt(r['chi2'])} & "
            rf"{tex_escape_text(r['scalar'])} & {ops} \\"
        )
    return "\n".join(lines)


def appendix_lagrangian_blocks(app_rows: list[dict[str, Any]]) -> str:
    # Keep all open-search blocks and only non-EH blocks that are below 2000.
    blocks: list[str] = []
    label_counter = 0
    for r in sorted(app_rows, key=lambda x: (x["sector"], agent_order().index(x["agent"]))):
        if r["sector"] == "non_eh" and r["chi2"] >= 2000:
            continue
        label_counter += 1
        tag = f"A{label_counter}"
        sector = "open search" if r["sector"] == "open_search" else "non-EH"
        coeff_line = r["coefficients_tex"] or r"{\rm coefficient\ vector\ unavailable\ in\ local\ memory}"
        sample = r["sample"]
        param_bits = []
        for key, label in [
            ("H0_km_s_Mpc", r"H_0"),
            ("Omega_m0", r"\Omega_{m0}"),
            ("lambda_H_Lambda_over_H0", r"\lambda_H"),
        ]:
            if key in sample:
                param_bits.append(rf"{label}={latex_number(sample[key])}")
        params = ",\\; ".join(param_bits)
        blocks.append(
            rf"""
\paragraph*{{{tex_escape_text(r['model'])}, {sector}, $\chi^2={r['chi2']:.3f}$.}}
\begin{{equation}}
\begin{{split}}
\mathscr{{L}}_{{{tag}}}
=\sqrt{{-g}}\left\{{{r['lagrangian_body_tex']}\right\}}.
\end{{split}}
\end{{equation}}
Available nonzero generated-coefficient vector from local sample memory:
\begin{{equation}}
{coeff_line}.
\end{{equation}}
Representative background sample:
\begin{{equation}}
{params}.
\end{{equation}}
"""
        )
    return "\n".join(blocks)


def repeated_family_tex(repeated: list[dict[str, Any]]) -> str:
    if not repeated:
        return "No exact repeated family below the stated threshold was found."
    rows = []
    for item in repeated[:8]:
        agents = ", ".join(AGENT_LABEL[a] for a in item["agents"])
        ops = compact_ops_tex(item["operator_content"], 4)
        rows.append(
            rf"{tex_escape_text(item['scalar'])} & {valfmt(item['best_chi2'])} & "
            rf"{tex_escape_text(agents)} & {ops} \\"
        )
    return "\n".join(rows)


def make_tex(metrics: list[dict[str, Any]], appendix_rows: list[dict[str, Any]], repeated: list[dict[str, Any]]) -> str:
    source = MAIN8.read_text(encoding="utf-8")
    marker = r"\section{Representative Results}"
    prefix = source.split(marker)[0]
    prefix = prefix.replace(r"\preprint{AI-MG-v5.2.2-agent}", r"\preprint{AI-MG-agent-benchmark-v1}")

    result = rf"""
\section{{LLM-Agent Benchmark Results}}
\label{{sec:results}}

This section replaces the earlier single-run summary with a controlled comparison of two autonomous-search campaigns.  The first campaign used five flagship models and a target of 600 initial theory proposals per agent.  The second campaign used cheaper models and a target of 2000 initial proposals per agent, but all five jobs were stopped by a 72-hour wall-time limit.  We therefore refer to the latter as a censored 2000-target run.  The local JSONL records, rather than LangSmith screenshots, are the source of truth for all numbers quoted below.

The comparison separates two proposal sectors.  The open-search sector is allowed to include the Einstein--Hilbert anchor and therefore tests whether the agent can rediscover the global background-fit basin.  The non-EH sector forbids a bare Einstein--Hilbert $R$ anchor and is used as a more stringent new-physics search.  All reported rankings are still by the real Solver value of $\chiT$.

\begin{{figure*}}[t]
\centering
\includegraphics[width=0.82\textwidth]{{figures/fig1_open_search_lcdm_improvement.pdf}}
\caption{{Improvement of the best open-search representative over the fixed $\Lambda$CDM reference, $\chi^2_{{\Lambda{{\rm CDM}}}}=1645.28$.  Positive values indicate lower $\chi^2$ than the reference.  The 2000-target run is censored at 72 hours, while the 600-run completed.}}
\label{{fig:open-lcdm-improvement}}
\end{{figure*}}

\begin{{table*}}[t]
\centering
\footnotesize
\begin{{ruledtabular}}
\begin{{tabular}}{{lrrrrrrr}}
Model & Recorded & Open best & Open hits $<1650$ & non-EH best & non-EH hits $<2000$ & Open acc. & non-EH acc.\\
\hline
\multicolumn{{8}}{{c}}{{Flagship 600-run}}\\
{tex_table_metrics(metrics, "flagship-600")}
\hline
\multicolumn{{8}}{{c}}{{Cheap 2000-target run, censored at 72 hours}}\\
{tex_table_metrics(metrics, "cheap-2000 partial")}
\end{{tabular}}
\end{{ruledtabular}}
\caption{{Per-agent comparison by sector.  ``Recorded'' denotes recorded initial proposals over the target.  Expanded and refinement evaluations are kept in the internal memory and appendix, but they do not count toward the initial proposal target.}}
\label{{tab:agent-comparison}}
\end{{table*}}

\begin{{figure*}}[t]
\centering
\includegraphics[width=0.95\textwidth]{{figures/fig2_open_search_best_and_hits.pdf}}
\caption{{Open-search performance.  The left panel shows the best $\chiT$ found by each agent, with numerical values annotated.  The right panel counts accepted open-search representatives with $\chiT<1650$.  The open-search sector is already saturated: both campaigns repeatedly find the same $\chi^2\simeq1638$ basin.}}
\label{{fig:open-search-summary}}
\end{{figure*}}

\begin{{figure*}}[t]
\centering
\includegraphics[width=0.95\textwidth]{{figures/fig3_non_eh_best_and_hits.pdf}}
\caption{{New-physics sector performance.  Only non-EH representatives with $\chiT<2000$ are plotted in the left panel; agents with no such hit are left blank rather than compressing the plot with $\chi^2\simeq9434$ failures.  In the censored 2000-target run, DeepSeek finds the strongest non-EH branch, while Qwen finds a distinct $\chi^2\simeq1896$ branch.}}
\label{{fig:noneh-summary}}
\end{{figure*}}

\begin{{figure*}}[t]
\centering
\includegraphics[width=0.88\textwidth]{{figures/fig4_sector_acceptance_rates.pdf}}
\caption{{Acceptance rates split by proposal sector.  The non-EH sector has a consistently lower acceptance rate than open search, indicating that the difficulty is structural and not merely a lack of parameter samples.}}
\label{{fig:sector-acceptance}}
\end{{figure*}}

\begin{{figure}}[t]
\centering
\includegraphics[width=\columnwidth]{{figures/fig5_speed_quality_tradeoff.pdf}}
\caption{{Wall-clock efficiency versus open-search quality.  Marker size is proportional to the number of non-EH hits below $\chiT=2000$.  The fast models are not always the best new-physics explorers; DeepSeek is slower but produces the strongest non-EH signal in the censored run.}}
\label{{fig:speed-quality}}
\end{{figure}}

\subsection{{Open-search basin}}
\label{{subsec:open-results}}

The open-search sector shows strong convergence across both campaigns.  Every agent reaches a representative within approximately $\Delta\chi^2\simeq7$ of the $\Lambda$CDM reference, and the best representatives cluster tightly around $\chiT\simeq1638$.  The repeated low-$\chi^2$ families are not random long operator strings: they are dominated by an Einstein--Hilbert anchor plus either a $\phi_1$ scalar sector, a two-scalar fixed sector, or weak high-curvature decorations.  Several exact operator families recur across all five cheap-run agents, including $R$ alone, $R+\phi_1^2R^2$, $R+\phi_1R_{{\mu\nu\rho\sigma}}R^{{\mu\nu\rho\sigma}}$, and two-scalar $R$ baselines.  This recurrence is evidence that the search has found a robust background expansion basin rather than a single accidental sample.

\begin{{figure*}}[t]
\centering
\includegraphics[width=0.95\textwidth]{{figures/fig6_best_so_far_open_search.pdf}}
\caption{{Best-so-far open-search trajectories as a function of initial sector attempts.  The fast approach to $\chi^2\simeq1638$ explains why increasing the open-search budget from 600 to a 2000-target run gives only small gains in the global optimum.}}
\label{{fig:open-best-so-far}}
\end{{figure*}}

\subsection{{Non-EH new-physics search}}
\label{{subsec:noneh-results}}

The non-EH sector behaves differently.  Its acceptance rate is lower, its median accepted $\chi^2$ is often near the poor $\chi^2\simeq9434$ plateau, and only a small fraction of accepted theories fall below $\chiT=2000$.  Nevertheless, the censored 2000-target run finds two notable non-EH branches.  DeepSeek finds a two-scalar branch with $\chiT=1693.860$, based on $\phi_2^2R$ and mixed scalar-derivative interactions.  Qwen finds a $\phi_2$-only branch with $\chiT=1896.001$ containing $\Box R$, a cubic Riemann contraction, $\phi_2^2R$, $\phi_2R_{{\mu\nu}}R^{{\mu\nu}}$, $\phi_2R_{{\mu\nu\rho\sigma}}R^{{\mu\nu\rho\sigma}}$, and derivative $\phi_2$ operators.  These are the most interesting outputs of the censored run because they are not merely EH-anchored dark-energy baselines.

\begin{{figure*}}[t]
\centering
\includegraphics[width=0.95\textwidth]{{figures/fig7_best_so_far_non_eh.pdf}}
\caption{{Best-so-far non-EH trajectories, showing only accepted representatives below $\chiT=2000$.  The blank early intervals are meaningful: many non-EH accepted branches survive the deterministic pipeline but remain far above the new-physics threshold.}}
\label{{fig:noneh-best-so-far}}
\end{{figure*}}

\begin{{figure}}[t]
\centering
\includegraphics[width=\columnwidth]{{figures/fig8_run_completion.pdf}}
\caption{{Completion fractions.  The 600-run finished for all agents, while the 2000-target cheap-model jobs were stopped by the 72-hour wall-time limit and should be interpreted as censored searches.}}
\label{{fig:completion}}
\end{{figure}}

\section{{Physical Interpretation and Limitations}}
\label{{sec:validation-boundaries}}

The comparison clarifies the role of the autonomous agent.  For global background fitting, the agent reliably rediscovers the EH-anchored scalar basin, but this is not by itself a discovery of modified gravity.  The best open-search models often improve over the $\Lambda$CDM background reference by only $\Delta\chi^2\simeq7$, and many such models differ only in weak or effectively redundant high-curvature decorations.  Their value is mainly as a calibration of search competence.

The non-EH sector is the more relevant new-physics stress test.  The DeepSeek and Qwen branches below $\chiT=2000$ show that the search can find non-EH backgrounds substantially better than the common $\chi^2\simeq9434$ plateau.  However, they should not yet be interpreted as complete viable modified-gravity theories.  The present validation is an FLRW background validation: perturbation stability, tensor propagation, structure growth, local screening, and a full covariant degeneracy analysis remain outside the likelihood used here.

The censored 2000-target run also reveals an algorithmic lesson.  Increasing the number of proposals helps the non-EH sector more than the open-search sector, but brute force alone is inefficient.  The repeated failure of many non-EH proposals indicates that future searches should improve the non-EH proposal distribution, remove empty scalar-family pools from the scheduler, and add a more explicit diversity or motif-level prior while preserving the cold-start rule that final rankings are determined only by deterministic validation and real $\chiT$.

\section{{Conclusion}}
\label{{sec:conclusion}}

We have compared autonomous modified-gravity searches driven by five LLM proposal agents across two campaigns.  The flagship 600-run and the censored cheap 2000-target run agree on the global result: the best background fits are EH-anchored scalar sectors with $\chiT\simeq1638$.  This agreement is useful because it shows that the agent framework is robust against the choice of proposal model for the easy global optimum.

The new-physics sector remains harder and more informative.  In the censored 2000-target run, DeepSeek finds the strongest non-EH candidate, with $\chiT=1693.860$, and Qwen finds a distinct $\phi_2$-only branch at $\chiT=1896.001$.  These branches motivate follow-up studies with targeted non-EH proposal policies, perturbation-level stability checks, and additional cosmological data.  The present results should therefore be read as an autonomous background-discovery audit: the machine can efficiently locate robust expansion-history basins, but the physics pipeline must still decide which branches survive as genuine gravitational theories.

\appendix

\section{{Representative Theory Archive}}
\label{{app:theory-archive}}

This appendix records compact versions of the representative Lagrangian densities used in the discussion.  The fixed scalar pieces $\mathcal{{L}}_{{\rm fixed}}^{{(i)}}$ are the canonical kinetic terms plus the selected quadratic or axion potential defined in Eq.~\eqref{{eq:fixed-sector}}.  Only generated operators with nonzero coefficient entries in the local sample memory are displayed.  The remote run-specific Solver CSVs contain the final accepted-sample rows; when those CSVs are not present in the local archive, the numerical coefficient vector below should be read as the locally recoverable representative vector associated with the proposal memory rather than as an independent re-fit.

\begin{{table*}}[t]
\centering
\scriptsize
\begin{{ruledtabular}}
\begin{{tabular}}{{llll}}
Model & $\chiT$ & Scalar & Representative open-search content\\
\hline
{tex_best_sector_rows(appendix_rows, "open_search")}
\end{{tabular}}
\end{{ruledtabular}}
\caption{{Best open-search representative for each cheap-run agent.  Full coefficient-substituted densities for the most useful representatives are written below.}}
\label{{tab:appendix-open-best}}
\end{{table*}}

\begin{{table*}}[t]
\centering
\scriptsize
\begin{{ruledtabular}}
\begin{{tabular}}{{llll}}
Model & $\chiT$ & Scalar & Representative non-EH content\\
\hline
{tex_best_sector_rows(appendix_rows, "non_eh")}
\end{{tabular}}
\end{{ruledtabular}}
\caption{{Best non-EH representative for each cheap-run agent.  Rows with $\chiT\simeq9434$ are retained as diagnostics but are not expanded into long equations unless they pass the $\chiT<2000$ new-physics threshold.}}
\label{{tab:appendix-noneh-best}}
\end{{table*}}

\begin{{table*}}[t]
\centering
\scriptsize
\begin{{ruledtabular}}
\begin{{tabular}}{{llll}}
Scalar sector & Best $\chiT$ & Agents finding family & Repeated operator content\\
\hline
{repeated_family_tex(repeated)}
\end{{tabular}}
\end{{ruledtabular}}
\caption{{Repeated low-$\chi^2$ families in the censored cheap 2000-target run.  Exact-family repetition across agents is a stronger signal than a single isolated low-$\chi^2$ proposal.}}
\label{{tab:appendix-repeated}}
\end{{table*}}

\begin{{widetext}}
{appendix_lagrangian_blocks(appendix_rows)}
\end{{widetext}}

\bibliographystyle{{apsrev4-2}}
\bibliography{{main2}}

\end{{document}}
"""
    return prefix + result


def write_summary(metrics: list[dict[str, Any]], appendix_rows: list[dict[str, Any]], repeated: list[dict[str, Any]]) -> None:
    lines = [
        "# cmp600 vs cmp2000 cheap partial summary",
        "",
        "The cheap 2000-target runs are censored at the 72-hour Slurm limit.",
        "",
        "The local archive used here contains full memory/proposal JSONL artifacts, but not the remote per-task Solver run directories for the cheap 2000-target campaign.  Therefore the appendix writes the recoverable representative coefficient vectors from local proposal/sample memory; replace these with the corresponding `accepted_samples_summary.csv` rows if the remote run directories are later pulled back.",
        "",
        "## Metrics",
        "",
    ]
    for cohort in ["flagship-600", "cheap-2000 partial"]:
        lines.append(f"### {cohort}")
        for m in sorted([x for x in metrics if x["cohort"] == cohort], key=lambda x: agent_order().index(x["agent"])):
            lines.append(
                f"- {m['model']}: recorded {m['recorded_initial']}/{m['target']}, "
                f"open best {valfmt(m['open_best'])}, open <1650 {m['open_hits_lt_1650']}, "
                f"non-EH best {valfmt(m['non_eh_best'])}, non-EH <2000 {m['non_eh_hits_lt_2000']}."
            )
        lines.append("")
    lines.append("## Interesting representatives")
    for r in appendix_rows:
        if r["sector"] == "open_search" or r["chi2"] < 2000:
            lines.append(
                f"- {r['model']} {r['sector']}: chi2={r['chi2']:.3f}, scalar={r['scalar']}, ops={'; '.join(r['operators'])}"
            )
    lines.append("")
    lines.append("## Repeated families")
    for r in repeated[:10]:
        lines.append(
            f"- agents={','.join(r['agents'])}, best={r['best_chi2']:.3f}, scalar={r['scalar']}, ops={'; '.join(r['operator_content'])}"
        )
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    bundles = load_bundles()
    metrics = build_metrics(bundles)
    write_csv(DATA_DIR / "comparison_metrics_local.csv", metrics)
    with (DATA_DIR / "comparison_metrics_local.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    plot_figures(metrics, bundles)
    appendix_rows, repeated, _ = build_appendix_data(bundles)
    with (DATA_DIR / "appendix_representatives.json").open("w", encoding="utf-8") as f:
        json.dump(
            [
                {k: v for k, v in row.items() if k not in {"sample"}}
                | {"sample": row.get("sample", {})}
                for row in appendix_rows
            ],
            f,
            indent=2,
            ensure_ascii=False,
        )
    with (DATA_DIR / "repeated_families.json").open("w", encoding="utf-8") as f:
        json.dump(repeated, f, indent=2, ensure_ascii=False, default=str)

    tex = make_tex(metrics, appendix_rows, repeated)
    (OUT / "main.tex").write_text(tex, encoding="utf-8")
    shutil.copy2(ROOT / "main2.bib", OUT / "main2.bib")
    write_summary(metrics, appendix_rows, repeated)

    zip_path = ROOT / "overleaf_cmp2000_comparison_v1.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in OUT.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(OUT.parent))

    print(f"Wrote {OUT}")
    print(f"Wrote {zip_path}")


if __name__ == "__main__":
    main()
