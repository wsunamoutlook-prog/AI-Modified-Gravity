from __future__ import annotations

import argparse
import csv
import json
import math
import pickle
import re
import statistics
from datetime import datetime
from pathlib import Path
from typing import Any

from .effective_corrections import diagnostics_for_attempt


REPORT_PLOT_DPI = 300
REPORT_BAR_MAX_ITEMS = 15
REPORT_COMPARISON_CHI2_THRESHOLD = 2000.0
REPORT_COLORS = {
    "accepted": "#0072B2",
    "eh_anchored": "#0072B2",
    "non_eh": "#D55E00",
    "open_search": "#009E73",
    "other": "#666666",
}
REPORT_HATCHES = {
    "eh_anchored": "",
    "non_eh": "///",
    "open_search": "",
    "other": "xx",
}
REPORT_RANK_COLORS = [
    "#0072B2",
    "#D55E00",
    "#009E73",
    "#CC79A7",
    "#E69F00",
    "#56B4E9",
    "#F0E442",
    "#000000",
]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_csv_first(path: Path | None) -> dict[str, str]:
    if not path or not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows[0] if rows else {}


def _read_csv_rows(path: Path | None) -> list[dict[str, str]]:
    if not path or not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _accepted_sample_row(attempt: dict[str, Any]) -> dict[str, str]:
    accepted_path = Path(attempt["accepted_samples_summary_path"]) if attempt.get("accepted_samples_summary_path") else None
    rows = _read_csv_rows(accepted_path)
    if not rows:
        return {}
    lag_id = str(attempt.get("best_lag_id") or "")
    if lag_id:
        rows = [row for row in rows if str(row.get("lag_id")) == lag_id] or rows
    attempt_chi2 = _float(attempt.get("chi2"))
    if not math.isnan(attempt_chi2):
        rows = sorted(rows, key=lambda row: abs(_float(row.get("chi2")) - attempt_chi2))
    return rows[0] if rows else {}


def _float(value: Any, default: float = math.nan) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _fmt(value: Any, digits: int = 6) -> str:
    x = _float(value)
    if math.isnan(x):
        return ""
    if abs(x) >= 1e4 or (abs(x) < 1e-3 and x != 0):
        return f"{x:.{digits}e}"
    return f"{x:.{digits}f}".rstrip("0").rstrip(".")


def _parse_timestamp(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(str(value), "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return None


def _solver_dir(attempt: dict[str, Any]) -> Path | None:
    value = attempt.get("solver_output_dir")
    return Path(value) if value else None


def _existing_report_path(value: Any) -> Path | None:
    if not value:
        return None
    path = Path(str(value))
    if path.exists():
        return path
    text = str(value)
    marker = "ai_theory_lab/"
    if marker in text:
        rel = Path(text[text.index(marker):])
        if rel.exists():
            return rel
    return None


def _lcdm_scan_report_path(attempt: dict[str, Any]) -> Path | None:
    direct = _existing_report_path(attempt.get("scan_report_path"))
    if direct:
        return direct
    solver_dir = _solver_dir(attempt)
    if solver_dir:
        direct = _existing_report_path(solver_dir / "scan_report.txt")
        if direct:
            return direct
    return None


def _parse_lcdm_reference(path: Path) -> dict[str, float] | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if "Flat-LambdaCDM reference fit" not in text:
        return None
    values: dict[str, float] = {}
    patterns = {
        "chi2": r"chi2_total=([0-9.eE+-]+)",
        "chi2_sn": r"chi2_DES_SN=([0-9.eE+-]+)",
        "chi2_bao": r"chi2_DESI_BAO=([0-9.eE+-]+)",
        "chi2_per_point": r"chi2/N=([0-9.eE+-]+)",
        "AIC": r"AIC=([0-9.eE+-]+)",
        "BIC": r"BIC=([0-9.eE+-]+)",
        "sn_offset_hat": r"M_SN_hat=([0-9.eE+-]+)",
        "bao_alpha_hat": r"alpha_BAO_hat=([0-9.eE+-]+)",
        "H0": r"H0=([0-9.eE+-]+)",
        "Omega_m0": r"Omega_m0=([0-9.eE+-]+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            values[key] = float(match.group(1))
    return values if "chi2" in values else None


def _find_lcdm_reference(attempts: list[dict[str, Any]]) -> dict[str, Any] | None:
    for attempt in attempts:
        path = _lcdm_scan_report_path(attempt)
        if not path:
            continue
        lcdm = _parse_lcdm_reference(path)
        if lcdm:
            out: dict[str, Any] = dict(lcdm)
            out["scan_report_path"] = str(path)
            return out
    return None


def _lcdm_delta_fields(attempt: dict[str, Any], lcdm: dict[str, Any] | None) -> dict[str, Any]:
    if not lcdm:
        return {}
    lcdm_chi2 = _float(lcdm.get("chi2"))
    chi2 = _float(attempt.get("chi2"))
    lcdm_aic = _float(lcdm.get("AIC"))
    aic = _float(attempt.get("aic"))
    lcdm_bic = _float(lcdm.get("BIC"))
    bic = _float(attempt.get("bic"))
    fields: dict[str, Any] = {"lcdm_chi2": lcdm.get("chi2")}
    if not math.isnan(chi2) and not math.isnan(lcdm_chi2):
        fields["delta_chi2_vs_lcdm"] = chi2 - lcdm_chi2
        fields["lcdm_improvement_chi2"] = lcdm_chi2 - chi2
    if not math.isnan(aic) and not math.isnan(lcdm_aic):
        fields["delta_aic_vs_lcdm"] = aic - lcdm_aic
    if not math.isnan(bic) and not math.isnan(lcdm_bic):
        fields["delta_bic_vs_lcdm"] = bic - lcdm_bic
    return fields


def _track_from_operators(operators: Any) -> str:
    labels: list[str] = []
    if isinstance(operators, list):
        for item in operators:
            if isinstance(item, dict):
                labels.append(str(item.get("candidate") or item.get("label") or item))
            else:
                labels.append(str(item))
    if "R" in labels:
        return "eh_anchored"
    if any("R" in label for label in labels):
        return "non_eh"
    return "non_gravity"


def _theory_track(attempt: dict[str, Any]) -> str:
    theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
    return str(
        attempt.get("theory_track")
        or theory.get("theory_track")
        or _track_from_operators(theory.get("operators"))
    )


def _proposal_group(attempt: dict[str, Any]) -> str:
    theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
    return str(attempt.get("proposal_group") or theory.get("proposal_group") or _theory_track(attempt))


def _run_dir(attempt: dict[str, Any]) -> Path | None:
    solver_dir = _solver_dir(attempt)
    if not solver_dir:
        return None
    # .../agent_solver_result/agent_solve -> run root
    return solver_dir.parents[1]


def _load_lagrangian(attempt: dict[str, Any]) -> dict[str, Any]:
    metadata = attempt.get("agent_lagrangian")
    if isinstance(metadata, dict):
        lagrangian = metadata.get("lagrangian")
        if isinstance(lagrangian, dict):
            return lagrangian
    run_dir = _run_dir(attempt)
    if not run_dir:
        return {}
    pkl_path = run_dir / "agent_lagrangians.pkl"
    if not pkl_path.exists():
        return {}
    with pkl_path.open("rb") as f:
        data = pickle.load(f)
    best_lag_id = str(attempt.get("best_lag_id") or "")
    if isinstance(data, dict):
        global_idx = 1
        for key in sorted(data, key=lambda value: int(value)):
            group = data.get(key) or []
            for item in group:
                if best_lag_id and str(global_idx) == best_lag_id:
                    return item if isinstance(item, dict) else {}
                global_idx += 1
        for group in data.values():
            if group:
                return group[0]
    if isinstance(data, list) and data:
        return data[0]
    return {}


def _coefficient_value(row: dict[str, str], symbol: str) -> str | None:
    if symbol in {"1", "COEFF_FIXED_1"}:
        return "1"
    bare_symbol = symbol.replace("\\", "")
    candidates = [
        symbol,
        bare_symbol,
        f"coef:{bare_symbol}",
        f"coefficient:{bare_symbol}",
    ]
    for key in candidates:
        if key in row and row[key] not in ("", None):
            return row[key]
    return None


def _bestfit_general(raw: str, terms: list[dict[str, Any]], row: dict[str, str]) -> str:
    out = raw
    for term in terms:
        symbol = str(term.get("coeff_symbol", ""))
        value = _coefficient_value(row, symbol)
        if not value or symbol == "1":
            continue
        out = out.replace(symbol, f"({_fmt(value, 10)})")
    return out


def _term_lines(terms: list[dict[str, Any]], row: dict[str, str], numeric: bool) -> list[str]:
    lines: list[str] = []
    for term in terms:
        symbol = str(term.get("coeff_symbol", "1"))
        coeff = _coefficient_value(row, symbol) if numeric else symbol
        coeff = "1" if coeff in (None, "") else coeff
        coeff_text = _fmt(coeff, 10) if numeric and coeff != "1" else coeff
        candidate = term.get("candidate", "")
        power = int(term.get("lambda_power", 0) or 0)
        sector = term.get("sector", "")
        fixed = bool(term.get("fixed", False))
        prefix = ""
        if coeff_text != "1":
            prefix = f"{coeff_text} · "
        if power:
            prefix += f"Λ^{{{power}}} · "
        body = f"{prefix}{candidate}"
        if fixed:
            body = str(candidate)
        if sector in {"gravity", "non-minimal"} and not fixed:
            body = f"M_p² ( {body} )"
        lines.append(f"√(-g) [ {body} ]")
    return lines


def _coefficient_summary(terms: list[dict[str, Any]], row: dict[str, str]) -> str:
    parts: list[str] = []
    for term in terms:
        if term.get("fixed"):
            continue
        symbol = str(term.get("coeff_symbol", ""))
        value = _coefficient_value(row, symbol)
        if symbol and value not in (None, ""):
            parts.append(f"{symbol}={_fmt(value, 4)}")
    return ", ".join(parts)


def _solution_path(attempt: dict[str, Any]) -> Path | None:
    solver_dir = _solver_dir(attempt)
    if not solver_dir:
        return None
    best_lag_id = str(attempt.get("best_lag_id") or "1")
    direct = solver_dir / f"top_01_lagrangian_{best_lag_id}_solution.csv"
    if direct.exists():
        return direct
    lag_matches = sorted(solver_dir.glob(f"top_*_lagrangian_{best_lag_id}_solution.csv"))
    if lag_matches:
        return lag_matches[0]
    matches = sorted(solver_dir.glob("top_01_lagrangian_*_solution.csv"))
    return matches[0] if matches else None


def _load_solution(attempt: dict[str, Any]) -> tuple[list[float], list[float]]:
    path = _solution_path(attempt)
    if not path:
        return [], []
    rows = _read_csv_rows(path)
    z = [_float(r.get("z")) for r in rows]
    h = [_float(r.get("h_dimensionless")) for r in rows]
    pairs = [(zz, hh) for zz, hh in zip(z, h) if not math.isnan(zz) and not math.isnan(hh)]
    pairs.sort()
    return [p[0] for p in pairs], [p[1] for p in pairs]


def _accepted_attempts(feedback: dict[str, Any], memory_dir: Path) -> list[dict[str, Any]]:
    history_path = memory_dir / "attempt_history.jsonl"
    if history_path.exists():
        attempts = [json.loads(line) for line in history_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        attempts = feedback.get("top_chi2_attempts") or []
    return [a for a in attempts if a.get("validated") and a.get("chi2") is not None]


def _validation_stage(attempt: dict[str, Any]) -> str:
    stage = attempt.get("validation_stage")
    if stage:
        return str(stage)
    loop_id = str(attempt.get("loop_id") or "")
    if "_refine_" in loop_id or "_refine" in loop_id:
        return "refine"
    if "_expanded_" in loop_id or "_expanded" in loop_id:
        return "expanded"
    return "initial"


def _family_key(attempt: dict[str, Any]) -> str:
    exact = attempt.get("family_key")
    if exact:
        return str(exact)
    theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
    operators = "+".join(str(op) for op in (theory.get("operators") or [])) or "none"
    potentials = theory.get("potential_types") if isinstance(theory.get("potential_types"), dict) else {}
    scalar = theory.get("scalar_config")
    if scalar or operators != "none":
        return (
            f"scalar={scalar}|"
            f"potential={potentials}|"
            f"operators={operators}"
        )
    return str(attempt.get("loop_id"))


def _representative_key(attempt: dict[str, Any]) -> str:
    return f"group={_proposal_group(attempt)}|{_family_key(attempt)}"


def _family_representatives(accepted: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best_by_family: dict[str, dict[str, Any]] = {}
    members_by_family: dict[str, list[dict[str, Any]]] = {}
    for attempt in sorted(accepted, key=lambda a: _float(a.get("chi2"))):
        key = _representative_key(attempt)
        members_by_family.setdefault(key, []).append(attempt)
        if key not in best_by_family:
            best_by_family[key] = dict(attempt)
    representatives: list[dict[str, Any]] = []
    for key, representative in best_by_family.items():
        members = members_by_family.get(key) or [representative]
        stage_counts: dict[str, int] = {}
        loop_ids: list[str] = []
        for member in members:
            stage = _validation_stage(member)
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
            loop_id = member.get("loop_id")
            if loop_id is not None:
                loop_ids.append(str(loop_id))
        representative["best_validation_stage"] = _validation_stage(representative)
        representative["validation_stage_counts"] = stage_counts
        representative["family_accepted_records"] = len(members)
        representative["family_loop_ids"] = loop_ids
        representative["coarse_family_key"] = representative.get("coarse_family_key")
        representatives.append(representative)
    return sorted(representatives, key=lambda a: _float(a.get("chi2")))


def _attach_effective_correction_diagnostics(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for attempt in attempts:
        row = dict(attempt)
        if _theory_track(row) == "eh_anchored":
            row["effective_correction"] = diagnostics_for_attempt(row)
        else:
            row["effective_correction"] = {
                "effective_correction_status": "not_applicable_non_eh",
                "effective_correction_reason": "EH-relative correction diagnostic applies only to EH-anchored theories",
                "max_relative_effect_to_EH": None,
                "dominant_correction_term": "",
                "active_correction_terms": 0,
                "moderate_correction_terms": 0,
                "weak_correction_terms": 0,
                "tiny_correction_terms": 0,
                "correction_term_count": 0,
                "tiny_correction_fraction": None,
                "term_effects": [],
            }
        enriched.append(row)
    return enriched


def _effective_summary(attempt: dict[str, Any]) -> dict[str, Any]:
    value = attempt.get("effective_correction")
    if isinstance(value, dict):
        return value
    return diagnostics_for_attempt(attempt)


def _write_plots(out_dir: Path, accepted: list[dict[str, Any]], top_n: int) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Computer Modern Roman", "CMU Serif", "DejaVu Serif"],
            "mathtext.fontset": "cm",
            "axes.unicode_minus": False,
            "font.size": 10,
            "axes.labelsize": 11,
            "axes.titlesize": 12,
            "legend.fontsize": 8,
            "legend.framealpha": 0.95,
            "figure.dpi": REPORT_PLOT_DPI,
            "savefig.dpi": REPORT_PLOT_DPI,
        }
    )

    comparison_chi2_plot_threshold = REPORT_COMPARISON_CHI2_THRESHOLD

    def _savefig(fig: Any, filename: str) -> None:
        fig.savefig(out_dir / filename, dpi=REPORT_PLOT_DPI, bbox_inches="tight", facecolor="white")

    def _label_bar_values(ax: Any, bars: Any, values: list[float], *, fontsize: int = 8) -> None:
        for bar, value in zip(bars, values):
            if math.isnan(value):
                continue
            ax.annotate(
                f"${_fmt(value, 2)}$",
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                rotation=0,
                fontsize=fontsize,
                clip_on=False,
            )

    def _compact_loop_label(attempt: dict[str, Any]) -> str:
        loop_id = str(attempt.get("loop_id") or "")
        match = re.search(r"(?:task|wave)_(\d+)", loop_id)
        if match:
            return f"#L{int(match.group(1))}"
        return loop_id[:12] if loop_id else ""

    def _set_bar_ylim(ax: Any, values: list[float], *, pad: float = 1.28) -> None:
        finite = [value for value in values if not math.isnan(value)]
        if finite:
            ax.set_ylim(0, max(finite) * pad)

    def _apply_bar_hatches(bars: Any, keys: list[str]) -> None:
        for bar, key in zip(bars, keys):
            hatch = REPORT_HATCHES.get(key, REPORT_HATCHES["other"])
            if hatch:
                bar.set_hatch(hatch)
            bar.set_edgecolor("#222222")
            bar.set_linewidth(0.5)

    def _curve_label(prefix: str, attempt: dict[str, Any]) -> str:
        return rf"{prefix} {_compact_loop_label(attempt)} $\chi^2={_fmt(attempt.get('chi2'), 2)}$"

    top = accepted[:top_n]
    bar_top = top[: min(REPORT_BAR_MAX_ITEMS, len(top))]
    labels = [_compact_loop_label(a) for a in bar_top]
    chi2 = [_float(a.get("chi2")) for a in bar_top]

    fig, ax = plt.subplots(figsize=(max(10, 0.65 * len(bar_top)), 4.8))
    bars = ax.bar(range(len(bar_top)), chi2, color=REPORT_COLORS["accepted"], label="accepted family")
    _label_bar_values(ax, bars, chi2, fontsize=6 if len(bar_top) > 30 else 7)
    _set_bar_ylim(ax, chi2, pad=1.32)
    ax.set_xticks(range(len(bar_top)))
    ax.set_xticklabels(labels, rotation=0, ha="center")
    ax.set_ylabel(r"$\chi^2$")
    ax.set_title(rf"Top {len(bar_top)} accepted family representatives $\chi^2$")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper right")
    fig.tight_layout()
    _savefig(fig, "accepted_chi2_bar.png")
    plt.close(fig)

    overlay = top[: min(8, len(top))]
    fig, ax = plt.subplots(figsize=(8, 5))
    for rank, attempt in enumerate(overlay, start=1):
        z, h = _load_solution(attempt)
        if z and h:
            ax.plot(
                z,
                h,
                lw=2,
                color=REPORT_RANK_COLORS[(rank - 1) % len(REPORT_RANK_COLORS)],
                label=rf"#{rank} {_compact_loop_label(attempt)} $\chi^2={_fmt(attempt.get('chi2'), 2)}$",
            )
    ax.set_xlabel("z")
    ax.set_ylabel(r"$h(z)=H/H_0$")
    ax.set_title("Top accepted family representative h(z)")
    ax.grid(alpha=0.25)
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    fig.tight_layout()
    _savefig(fig, "top_h_overlay.png")
    plt.close(fig)

    dense_overlay = [attempt for attempt in top if _float(attempt.get("chi2")) < comparison_chi2_plot_threshold]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    plotted = 0
    for rank, attempt in enumerate(dense_overlay, start=1):
        z, h = _load_solution(attempt)
        if z and h:
            color = REPORT_RANK_COLORS[(rank - 1) % len(REPORT_RANK_COLORS)] if rank <= 8 else "#777777"
            alpha = 0.7 if rank <= 8 else 0.25
            lw = 1.4 if rank <= 8 else 0.8
            ax.plot(z, h, lw=lw, alpha=alpha, color=color)
            plotted += 1
    ax.set_xlabel("z")
    ax.set_ylabel(r"$h(z)=H/H_0$")
    ax.set_title(rf"Top {plotted} accepted family representative h(z) ($\chi^2 < {comparison_chi2_plot_threshold:g}$)")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    _savefig(fig, "top_h_overlay_topn.png")
    plt.close(fig)

    eh_top = [attempt for attempt in accepted if _theory_track(attempt) == "eh_anchored"][:10]
    non_eh_top = [attempt for attempt in accepted if _theory_track(attempt) == "non_eh"][:10]
    track_top = [
        (label, attempt)
        for label, attempt in [("EH", attempt) for attempt in eh_top] + [("non-EH", attempt) for attempt in non_eh_top]
        if _float(attempt.get("chi2")) < comparison_chi2_plot_threshold
    ]

    fig, ax = plt.subplots(figsize=(max(9, 0.65 * len(track_top)), 4.8))
    track_keys = ["eh_anchored" if label == "EH" else "non_eh" for label, _ in track_top]
    colors = [REPORT_COLORS[key] for key in track_keys]
    track_labels = [_compact_loop_label(attempt) for _, attempt in track_top]
    track_chi2 = [_float(attempt.get("chi2")) for _, attempt in track_top]
    bars = ax.bar(range(len(track_top)), track_chi2, color=colors)
    _apply_bar_hatches(bars, track_keys)
    _label_bar_values(ax, bars, track_chi2, fontsize=7)
    _set_bar_ylim(ax, track_chi2, pad=1.28)
    ax.set_xticks(range(len(track_top)))
    ax.set_xticklabels(track_labels, rotation=0, ha="center")
    ax.set_ylabel(r"$\chi^2$")
    ax.set_title(rf"Top EH-anchored vs non-EH representatives ($\chi^2 < {comparison_chi2_plot_threshold:g}$)")
    ax.grid(axis="y", alpha=0.25)
    track_legend = [
        Patch(facecolor=REPORT_COLORS["eh_anchored"], edgecolor="#222222", label="EH anchored"),
        Patch(facecolor=REPORT_COLORS["non_eh"], edgecolor="#222222", hatch=REPORT_HATCHES["non_eh"], label="non-EH"),
    ]
    if track_top:
        ax.legend(handles=track_legend, fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    fig.tight_layout()
    _savefig(fig, "top_by_track_chi2_bar.png")
    plt.close(fig)

    track_curve_top = track_top
    fig, ax = plt.subplots(figsize=(10, 5.5))
    plotted = 0
    for rank, (track_label, attempt) in enumerate(track_curve_top, start=1):
        z, h = _load_solution(attempt)
        if z and h:
            is_non_eh = track_label == "non-EH"
            ax.plot(
                z,
                h,
                lw=1.6,
                alpha=0.75,
                color=REPORT_COLORS["non_eh"] if is_non_eh else REPORT_COLORS["eh_anchored"],
                linestyle="--" if is_non_eh else "-",
                label=_curve_label(track_label, attempt),
            )
            plotted += 1
    ax.set_xlabel("z")
    ax.set_ylabel(r"$h(z)=H/H_0$")
    ax.set_title(rf"Track comparison h(z), {plotted} plotted representatives ($\chi^2 < {comparison_chi2_plot_threshold:g}$)")
    ax.grid(alpha=0.25)
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    elif track_curve_top:
        ax.text(0.5, 0.5, "No solution curves found for filtered track representatives", transform=ax.transAxes, ha="center", va="center")
    fig.tight_layout()
    _savefig(fig, "top_by_track_h_overlay.png")
    plt.close(fig)

    preferred_groups = ["open_search", "non_eh"]
    observed_groups = sorted({_proposal_group(attempt) for attempt in accepted})
    group_names = [group for group in preferred_groups if group in observed_groups] + [
        group for group in observed_groups if group not in preferred_groups
    ]
    group_tops = {group: [attempt for attempt in accepted if _proposal_group(attempt) == group][:10] for group in group_names}
    group_chi2_tops = {
        group: [attempt for attempt in group_tops[group] if _float(attempt.get("chi2")) < comparison_chi2_plot_threshold]
        for group in group_names
    }
    group_colors = {"open_search": REPORT_COLORS["open_search"], "non_eh": REPORT_COLORS["non_eh"]}
    group_top = [(group, attempt) for group in group_names for attempt in group_chi2_tops[group]]
    fig, ax = plt.subplots(figsize=(max(9, 0.62 * len(group_top)), 4.8))
    group_chi2 = [_float(attempt.get("chi2")) for _, attempt in group_top]
    if group_top:
        bar_keys = [group if group in group_colors else "other" for group, _ in group_top]
        bars = ax.bar(
            range(len(group_top)),
            group_chi2,
            color=[group_colors.get(group, "#666666") for group, _ in group_top],
        )
        _apply_bar_hatches(bars, bar_keys)
        _label_bar_values(ax, bars, group_chi2)
        _set_bar_ylim(ax, group_chi2, pad=1.28)
    else:
        ax.text(
            0.5,
            0.5,
            rf"No proposal-group representatives with $\chi^2 < {comparison_chi2_plot_threshold:g}$",
            transform=ax.transAxes,
            ha="center",
            va="center",
        )
    ax.set_xticks(range(len(group_top)))
    ax.set_xticklabels([_compact_loop_label(attempt) for _, attempt in group_top], rotation=0, ha="center")
    ax.set_ylabel(r"$\chi^2$")
    ax.set_title(rf"Top representatives by proposal group ($\chi^2 < {comparison_chi2_plot_threshold:g}$)")
    ax.grid(axis="y", alpha=0.25)
    legend_handles = [
        Patch(
            facecolor=group_colors.get(group, REPORT_COLORS["other"]),
            edgecolor="#222222",
            hatch=REPORT_HATCHES.get(group, REPORT_HATCHES["other"]),
            label=group,
        )
        for group in group_names
        if group_chi2_tops.get(group)
    ]
    if legend_handles:
        ax.legend(handles=legend_handles, fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    fig.tight_layout()
    _savefig(fig, "top_by_group_chi2_bar.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    plotted = 0
    for group, attempt in group_top:
        z, h = _load_solution(attempt)
        if z and h:
            ax.plot(
                z,
                h,
                lw=1.6,
                alpha=0.75,
                color=group_colors.get(group, "#666666"),
                linestyle="--" if group == "non_eh" else "-",
                label=_curve_label(group, attempt),
            )
            plotted += 1
    ax.set_xlabel("z")
    ax.set_ylabel(r"$h(z)=H/H_0$")
    ax.set_title(rf"Proposal group h(z) comparison, {plotted} plotted representatives ($\chi^2 < {comparison_chi2_plot_threshold:g}$)")
    ax.grid(alpha=0.25)
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    elif group_top:
        ax.text(0.5, 0.5, "No solution curves found for filtered proposal-group representatives", transform=ax.transAxes, ha="center", va="center")
    fig.tight_layout()
    _savefig(fig, "top_by_group_h_overlay.png")
    plt.close(fig)

    panels = top[: min(3, len(top))]
    if panels:
        fig, axes = plt.subplots(len(panels), 1, figsize=(8, 3 * len(panels)), sharex=True)
        if len(panels) == 1:
            axes = [axes]
        for rank, (ax, attempt) in enumerate(zip(axes, panels)):
            z, h = _load_solution(attempt)
            if z and h:
                ax.plot(z, h, lw=2, color=REPORT_RANK_COLORS[rank % len(REPORT_RANK_COLORS)])
            ax.set_ylabel(r"$h(z)$")
            ax.set_title(rf"{_compact_loop_label(attempt)} $\chi^2={_fmt(attempt.get('chi2'), 3)}$")
            ax.grid(alpha=0.25)
        axes[-1].set_xlabel("z")
        fig.tight_layout()
        _savefig(fig, "top3_h_panels.png")
        plt.close(fig)


def _write_summary(
    out_dir: Path,
    run_name: str,
    feedback: dict[str, Any],
    accepted: list[dict[str, Any]],
    representatives: list[dict[str, Any]],
    top_n: int,
    lcdm: dict[str, Any] | None,
    benchmark: dict[str, Any] | None,
) -> None:
    failures = feedback.get("failure_tag_counts") or {}
    accepted_chi2 = [_float(attempt.get("chi2")) for attempt in accepted]
    accepted_chi2 = [value for value in accepted_chi2 if not math.isnan(value)]
    best_chi2 = min(accepted_chi2) if accepted_chi2 else feedback.get("best_chi2")
    best_chi2_value = _float(best_chi2)
    lcdm_chi2_value = _float(lcdm.get("chi2") if lcdm else None)
    lines = [
        f"# LangGraph Agent Result Summary: {run_name}",
        "",
        "This report is generated from current-loop memory and the isolated Solver outputs for accepted attempts.",
        "Human-facing tables and plots use one best representative per theory family; full accepted attempts remain in `accepted_summary.json`.",
        "",
        "## Quick Result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Total attempts | {feedback.get('total_attempts', '')} |",
        f"| Accepted attempts | {len(accepted)} |",
        f"| Accepted theory families shown | {len(representatives)} |",
        f"| Best chi2 | {_fmt(best_chi2, 6)} |",
        f"| LCDM chi2 | {_fmt(lcdm.get('chi2') if lcdm else None, 6)} |",
        f"| Best delta chi2 vs LCDM | {_fmt(best_chi2_value - lcdm_chi2_value if not math.isnan(best_chi2_value) and not math.isnan(lcdm_chi2_value) else None, 6)} |",
        f"| Best chi2 improvement over LCDM | {_fmt(lcdm_chi2_value - best_chi2_value if not math.isnan(best_chi2_value) and not math.isnan(lcdm_chi2_value) else None, 6)} |",
        f"| q_not_determined | {failures.get('q_not_determined', 0)} |",
        f"| constraint_drift | {failures.get('constraint_drift', 0)} |",
        f"| q_initial_root_failure | {failures.get('q_initial_root_failure', 0)} |",
        "",
        "## Output Files",
        "",
        "- [accepted_lagrangians_and_parameters.md](accepted_lagrangians_and_parameters.md)",
        "- [accepted_lagrangians_full.md](accepted_lagrangians_full.md)",
        "- [accepted_lagrangians_and_parameters.csv](accepted_lagrangians_and_parameters.csv)",
        "- [accepted_summary.json](accepted_summary.json)",
        "- [lcdm_reference.json](lcdm_reference.json) when available",
        "- [benchmark_summary.json](benchmark_summary.json)",
        "- [benchmark_by_sector.csv](benchmark_by_sector.csv)",
        "",
        "## Plots",
        "",
        "![Accepted chi2 ranking](accepted_chi2_bar.png)",
        "",
        "![Top h(z) overlay](top_h_overlay.png)",
        "",
        "![Top-N h(z) overlay](top_h_overlay_topn.png)",
        "",
        "![Track chi2 comparison](top_by_track_chi2_bar.png)",
        "",
        "![Track h(z) comparison](top_by_track_h_overlay.png)",
        "",
        "![Proposal group chi2 comparison](top_by_group_chi2_bar.png)",
        "",
        "![Proposal group h(z) comparison](top_by_group_h_overlay.png)",
        "",
        "![Top 3 h(z) panels](top3_h_panels.png)",
        "",
        "## LCDM Reference",
        "",
        "| Quantity | Value |",
        "|---|---:|",
        f"| chi2_total | {_fmt(lcdm.get('chi2') if lcdm else None, 6)} |",
        f"| chi2_DES_SN | {_fmt(lcdm.get('chi2_sn') if lcdm else None, 6)} |",
        f"| chi2_DESI_BAO | {_fmt(lcdm.get('chi2_bao') if lcdm else None, 6)} |",
        f"| chi2/N | {_fmt(lcdm.get('chi2_per_point') if lcdm else None, 6)} |",
        f"| AIC | {_fmt(lcdm.get('AIC') if lcdm else None, 6)} |",
        f"| BIC | {_fmt(lcdm.get('BIC') if lcdm else None, 6)} |",
        f"| H0 | {_fmt(lcdm.get('H0') if lcdm else None, 6)} |",
        f"| Omega_m0 | {_fmt(lcdm.get('Omega_m0') if lcdm else None, 6)} |",
        "",
        "## Benchmark Metrics",
        "",
        "| Sector | Attempts | Accepted | Accept rate | Best chi2 | Delta chi2 vs LCDM | Unique families | chi2<1700 families | Active/moderate MG | Attempts/hour |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    sectors = (benchmark or {}).get("sectors") if isinstance(benchmark, dict) else {}
    if isinstance(sectors, dict) and sectors:
        preferred = ["all", "open_search", "non_eh"]
        sector_names = [name for name in preferred if name in sectors] + [name for name in sorted(sectors) if name not in preferred]
        for sector in sector_names:
            row = sectors[sector]
            lines.append(
                f"| {sector} | {row.get('attempts', '')} | {row.get('accepted', '')} | "
                f"{_fmt(row.get('accept_rate'), 3)} | {_fmt(row.get('best_chi2'), 6)} | "
                f"{_fmt(row.get('best_delta_chi2_vs_lcdm'), 6)} | "
                f"{row.get('unique_families', '')} | {row.get('unique_families_chi2_lt_1700', '')} | "
                f"{row.get('active_or_moderate_families', '')} | {_fmt(row.get('attempts_per_hour'), 3)} |"
            )
    else:
        lines.append("|  |  |  |  |  |  |  |  |  |  |")
    lines.extend(
        [
            "",
        "## Proposal Group Comparison",
        "",
        "- [Top open-search representatives](top_open_search.md)",
        "- [Top non-EH representatives](top_non_eh.md)",
        "",
        "## Track Comparison",
        "",
        "- [Top EH-anchored representatives](top_eh_anchored.md)",
        "- [Top non-EH representatives](top_non_eh.md)",
        "",
        "## Top Accepted Family Representatives",
        "",
        "| Rank | Group | Track | Family | Loop | Best stage | Family records | chi2 | Delta chi2 vs LCDM | Status | Max rel. effect | Dominant correction | Sample | H0 | Omega_m0 | lambda_H | Scalar | Potential | Operators |",
        "|---:|---|---|---|---|---|---:|---:|---:|---|---:|---|---:|---:|---:|---:|---|---|---|",
        ]
    )
    for rank, attempt in enumerate(representatives[:top_n], start=1):
        theory = attempt.get("theory") or {}
        row = _accepted_sample_row(attempt)
        ops = "; ".join(theory.get("operators") or [])
        potential = json.dumps(theory.get("potential_types") or {}, ensure_ascii=False)
        effective = _effective_summary(attempt)
        delta = _lcdm_delta_fields(attempt, lcdm)
        lines.append(
            f"| {rank} | {_proposal_group(attempt)} | {_theory_track(attempt)} | {_family_key(attempt)} | {attempt.get('loop_id')} | "
            f"{attempt.get('best_validation_stage', _validation_stage(attempt))} | "
            f"{attempt.get('family_accepted_records', 1)} | {_fmt(attempt.get('chi2'), 6)} | "
            f"{_fmt(delta.get('delta_chi2_vs_lcdm'), 6)} | "
            f"{effective.get('effective_correction_status', '')} | "
            f"{_fmt(effective.get('max_relative_effect_to_EH'), 3)} | "
            f"{effective.get('dominant_correction_term', '')} | "
            f"{row.get('agent_parameter_sample_index', '')} | {_fmt(row.get('H0_km_s_Mpc'), 3)} | "
            f"{_fmt(row.get('Omega_m0'), 4)} | {_fmt(row.get('lambda_H_Lambda_over_H0'), 3)} | "
            f"{theory.get('scalar_config', '')} | {potential} | {ops} |"
        )
    lines.extend(
        [
            "",
            "## Top Family Representative Parameter Choices",
            "",
            "| Rank | Loop | varphi1_0 | q1_0 | mu1 | fbar1 | varphi2_0 | q2_0 | mu2 | fbar2 | Free coefficients |",
            "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for rank, attempt in enumerate(representatives[:top_n], start=1):
        row = _accepted_sample_row(attempt)
        terms = (_load_lagrangian(attempt).get("terms") or [])
        lines.append(
            f"| {rank} | {attempt.get('loop_id')} | "
            f"{_fmt(row.get('varphi1_0_phi1_over_Mp'), 4)} | {_fmt(row.get('q1_0_dvarphi1_dln_a'), 4)} | "
            f"{_fmt(row.get('mu1_m1_over_H0'), 4)} | {_fmt(row.get('fbar1_f1_over_Mp'), 4)} | "
            f"{_fmt(row.get('varphi2_0_phi2_over_Lambda'), 4)} | {_fmt(row.get('q2_0_dvarphi2_dln_a'), 4)} | "
            f"{_fmt(row.get('mu2_m2_over_Lambda'), 4)} | {_fmt(row.get('fbar2_f2_over_Lambda'), 4)} | "
            f"{_coefficient_summary(terms, row)} |"
        )
    lines.extend(
        [
            "",
            "## Main Failure Tags",
            "",
            "| Tag | Count |",
            "|---|---:|",
        ]
    )
    for tag, count in sorted(failures.items(), key=lambda item: item[1], reverse=True):
        lines.append(f"| {tag} | {count} |")
    lines.append("")
    (out_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def _write_lagrangian_reports(
    out_dir: Path,
    accepted: list[dict[str, Any]],
    top_n: int,
    lcdm: dict[str, Any] | None,
) -> None:
    csv_rows: list[dict[str, Any]] = []
    csv_fieldnames = [
            "rank",
            "loop_id",
            "best_validation_stage",
            "validation_stage_counts",
            "family_accepted_records",
            "family_loop_ids",
            "chi2",
        "chi2_sn",
        "chi2_bao",
        "lcdm_chi2",
        "delta_chi2_vs_lcdm",
        "lcdm_improvement_chi2",
        "aic",
        "bic",
        "delta_aic_vs_lcdm",
        "delta_bic_vs_lcdm",
        "scalar_config",
        "proposal_group",
        "theory_track",
        "potential_types",
        "raw_general_lagrangian",
        "bestfit_general_lagrangian",
        "term_metadata",
        "agent_parameter_sample_index",
        "H0_km_s_Mpc",
        "Omega_m0",
        "lambda_H_Lambda_over_H0",
        "proposal_json",
        "agent_lagrangians_pkl",
        "solver_output_dir",
        "solution_csv",
        "effective_correction_status",
        "max_relative_effect_to_EH",
        "dominant_correction_term",
        "active_correction_terms",
        "moderate_correction_terms",
        "weak_correction_terms",
        "tiny_correction_terms",
        "tiny_correction_fraction",
        "effective_correction_json",
    ]
    md_lines = [
        "# Accepted Lagrangians And Parameters",
        "",
        "Each entry is the best chi-square representative of one accepted theory family.",
        "The full accepted-attempt list is preserved in `accepted_summary.json`.",
        "Each displayed entry uses the actual `agent_lagrangians.pkl` object that entered EOM -> Builder -> Solver.",
        "",
    ]
    full_lines = [
        "# Accepted Lagrangians Full",
        "",
        "Complete dimension-balanced Lagrangians, best-fit coefficient substitutions, metadata, and Solver paths.",
        "Only the best chi-square representative from each accepted theory family is shown for human inspection.",
        "The full accepted-attempt list is preserved in `accepted_summary.json`.",
        "",
    ]

    for rank, attempt in enumerate(accepted[:top_n], start=1):
        lag = _load_lagrangian(attempt)
        solver_dir = _solver_dir(attempt)
        row = _accepted_sample_row(attempt)
        terms = lag.get("terms") or []
        raw = lag.get("general") or ""
        bestfit = _bestfit_general(raw, terms, row)
        theory = attempt.get("theory") or {}
        solution_path = _solution_path(attempt)
        effective = _effective_summary(attempt)
        lcdm_delta = _lcdm_delta_fields(attempt, lcdm)

        csv_rows.append(
            {
                "rank": rank,
                "loop_id": attempt.get("loop_id"),
                "best_validation_stage": attempt.get("best_validation_stage", _validation_stage(attempt)),
                "validation_stage_counts": json.dumps(attempt.get("validation_stage_counts") or {}, ensure_ascii=False),
                "family_accepted_records": attempt.get("family_accepted_records", 1),
                "family_loop_ids": json.dumps(attempt.get("family_loop_ids") or [attempt.get("loop_id")], ensure_ascii=False),
                "chi2": attempt.get("chi2"),
                "chi2_sn": row.get("chi2_sn"),
                "chi2_bao": row.get("chi2_bao"),
                "lcdm_chi2": lcdm_delta.get("lcdm_chi2"),
                "delta_chi2_vs_lcdm": lcdm_delta.get("delta_chi2_vs_lcdm"),
                "lcdm_improvement_chi2": lcdm_delta.get("lcdm_improvement_chi2"),
                "aic": attempt.get("aic"),
                "bic": attempt.get("bic"),
                "delta_aic_vs_lcdm": lcdm_delta.get("delta_aic_vs_lcdm"),
                "delta_bic_vs_lcdm": lcdm_delta.get("delta_bic_vs_lcdm"),
                "scalar_config": theory.get("scalar_config"),
                "proposal_group": _proposal_group(attempt),
                "theory_track": _theory_track(attempt),
                "potential_types": json.dumps(theory.get("potential_types") or {}, ensure_ascii=False),
                "raw_general_lagrangian": raw,
                "bestfit_general_lagrangian": bestfit,
                "term_metadata": json.dumps(terms, ensure_ascii=False),
                "agent_parameter_sample_index": row.get("agent_parameter_sample_index"),
                "H0_km_s_Mpc": row.get("H0_km_s_Mpc"),
                "Omega_m0": row.get("Omega_m0"),
                "lambda_H_Lambda_over_H0": row.get("lambda_H_Lambda_over_H0"),
                "proposal_json": attempt.get("proposal_path"),
                "agent_lagrangians_pkl": str((_run_dir(attempt) or Path(".")) / "agent_lagrangians.pkl"),
                "solver_output_dir": str(solver_dir or ""),
                "solution_csv": str(solution_path or ""),
                "effective_correction_status": effective.get("effective_correction_status"),
                "max_relative_effect_to_EH": effective.get("max_relative_effect_to_EH"),
                "dominant_correction_term": effective.get("dominant_correction_term"),
                "active_correction_terms": effective.get("active_correction_terms"),
                "moderate_correction_terms": effective.get("moderate_correction_terms"),
                "weak_correction_terms": effective.get("weak_correction_terms"),
                "tiny_correction_terms": effective.get("tiny_correction_terms"),
                "tiny_correction_fraction": effective.get("tiny_correction_fraction"),
                "effective_correction_json": json.dumps(effective, ensure_ascii=False),
            }
        )

        block = [
            f"## {rank}. {attempt.get('loop_id')}  chi2={_fmt(attempt.get('chi2'), 6)}",
            "",
            f"- best_validation_stage: `{attempt.get('best_validation_stage', _validation_stage(attempt))}`",
            f"- validation_stage_counts: `{json.dumps(attempt.get('validation_stage_counts') or {}, ensure_ascii=False)}`",
            f"- family_accepted_records: `{attempt.get('family_accepted_records', 1)}`",
            f"- delta_chi2_vs_LCDM: `{_fmt(lcdm_delta.get('delta_chi2_vs_lcdm'), 8)}`",
            f"- delta_AIC_vs_LCDM: `{_fmt(lcdm_delta.get('delta_aic_vs_lcdm'), 8)}`",
            f"- delta_BIC_vs_LCDM: `{_fmt(lcdm_delta.get('delta_bic_vs_lcdm'), 8)}`",
            f"- scalar_config: `{theory.get('scalar_config', '')}`",
            f"- proposal_group: `{_proposal_group(attempt)}`",
            f"- theory_track: `{_theory_track(attempt)}`",
            f"- potential_types: `{json.dumps(theory.get('potential_types') or {}, ensure_ascii=False)}`",
            f"- agent_parameter_sample_index: `{row.get('agent_parameter_sample_index', '')}`",
            f"- H0_km_s_Mpc: `{_fmt(row.get('H0_km_s_Mpc'), 8)}`",
            f"- Omega_m0: `{_fmt(row.get('Omega_m0'), 8)}`",
            f"- lambda_H_Lambda_over_H0: `{_fmt(row.get('lambda_H_Lambda_over_H0'), 8)}`",
            f"- effective_correction_status: `{effective.get('effective_correction_status', '')}`",
            f"- max_relative_effect_to_EH: `{_fmt(effective.get('max_relative_effect_to_EH'), 8)}`",
            f"- dominant_correction_term: `{effective.get('dominant_correction_term', '')}`",
            "",
            "### Raw Dimension-Balanced Lagrangian",
            "",
            "```text",
            raw,
            "```",
            "",
            "### Best-Fit Lagrangian",
            "",
            "```text",
            bestfit,
            "```",
            "",
            "### Expanded Terms",
            "",
            "```text",
            " +\n".join(_term_lines(terms, row, numeric=False)),
            "```",
            "",
            "### Expanded Terms With Best-Fit Coefficients",
            "",
            "```text",
            " +\n".join(_term_lines(terms, row, numeric=True)),
            "```",
            "",
            "### Term Metadata",
            "",
            "```json",
            json.dumps(terms, ensure_ascii=False, indent=2),
            "```",
            "",
            "### Effective Correction Diagnostics",
            "",
            "```json",
            json.dumps(effective, ensure_ascii=False, indent=2),
            "```",
            "",
            "### Output Paths",
            "",
            f"- proposal: `{attempt.get('proposal_path', '')}`",
            f"- solver output: `{solver_dir or ''}`",
            f"- accepted_samples_summary.csv: `{attempt.get('accepted_samples_summary_path', '')}`",
            f"- solution csv: `{solution_path or ''}`",
            "",
        ]
        md_lines.extend(block)
        full_lines.extend(block)

    if not csv_rows:
        md_lines.extend(["No accepted models were found in this run.", ""])
        full_lines.extend(["No accepted models were found in this run.", ""])

    with (out_dir / "accepted_lagrangians_and_parameters.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    (out_dir / "accepted_lagrangians_and_parameters.md").write_text("\n".join(md_lines), encoding="utf-8")
    (out_dir / "accepted_lagrangians_full.md").write_text("\n".join(full_lines), encoding="utf-8")


def _write_track_reports(out_dir: Path, representatives: list[dict[str, Any]]) -> None:
    specs = [
        ("eh_anchored", "top_eh_anchored.md", "Top EH-Anchored Representatives"),
        ("non_eh", "top_non_eh.md", "Top Non-EH Representatives"),
    ]
    for track, filename, title in specs:
        rows = [attempt for attempt in representatives if _theory_track(attempt) == track][:10]
        lines = [
            f"# {title}",
            "",
            "| Rank | Loop | Best stage | Family records | chi2 | Status | Max rel. effect | Scalar | Operators |",
            "|---:|---|---|---:|---:|---|---:|---|---|",
        ]
        for rank, attempt in enumerate(rows, start=1):
            theory = attempt.get("theory") or {}
            effective = _effective_summary(attempt)
            lines.append(
                f"| {rank} | {attempt.get('loop_id')} | "
                f"{attempt.get('best_validation_stage', _validation_stage(attempt))} | "
                f"{attempt.get('family_accepted_records', 1)} | {_fmt(attempt.get('chi2'), 6)} | "
                f"{effective.get('effective_correction_status', '')} | "
                f"{_fmt(effective.get('max_relative_effect_to_EH'), 3)} | "
                f"{theory.get('scalar_config', '')} | {'; '.join(theory.get('operators') or [])} |"
            )
        if not rows:
            lines.extend(["", "No accepted family representatives were found for this track."])
        lines.append("")
        (out_dir / filename).write_text("\n".join(lines), encoding="utf-8")


def _write_group_reports(out_dir: Path, representatives: list[dict[str, Any]]) -> None:
    preferred_specs = [
        ("open_search", "top_open_search.md", "Top Open-Search Representatives"),
        ("non_eh", "top_non_eh.md", "Top Non-EH Representatives"),
    ]
    observed = sorted({_proposal_group(attempt) for attempt in representatives})
    spec_by_group = {group: (filename, title) for group, filename, title in preferred_specs}
    specs = []
    for group, filename, title in preferred_specs:
        specs.append((group, filename, title))
    for group in observed:
        if group not in spec_by_group:
            specs.append((group, f"top_{group}.md", f"Top {group} Representatives"))
    for group, filename, title in specs:
        rows = [attempt for attempt in representatives if _proposal_group(attempt) == group][:10]
        lines = [
            f"# {title}",
            "",
            "| Rank | Loop | Best stage | Family records | chi2 | Track | Status | Max rel. effect | Scalar | Operators |",
            "|---:|---|---|---:|---:|---|---|---:|---|---|",
        ]
        for rank, attempt in enumerate(rows, start=1):
            theory = attempt.get("theory") or {}
            effective = _effective_summary(attempt)
            lines.append(
                f"| {rank} | {attempt.get('loop_id')} | "
                f"{attempt.get('best_validation_stage', _validation_stage(attempt))} | "
                f"{attempt.get('family_accepted_records', 1)} | {_fmt(attempt.get('chi2'), 6)} | "
                f"{_theory_track(attempt)} | "
                f"{effective.get('effective_correction_status', '')} | "
                f"{_fmt(effective.get('max_relative_effect_to_EH'), 3)} | "
                f"{theory.get('scalar_config', '')} | {'; '.join(theory.get('operators') or [])} |"
            )
        if not rows:
            lines.extend(["", "No accepted family representatives were found for this proposal group."])
        lines.append("")
        (out_dir / filename).write_text("\n".join(lines), encoding="utf-8")


def _read_scheduler_events(run_name: str) -> list[dict[str, Any]]:
    path = Path("ai_theory_lab") / "proposals" / run_name / "scheduler_tasks.jsonl"
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def _wall_time_seconds(attempts: list[dict[str, Any]], events: list[dict[str, Any]]) -> float | None:
    timestamps: list[datetime] = []
    for event in events:
        ts = _parse_timestamp(event.get("timestamp"))
        if ts:
            timestamps.append(ts)
    if len(timestamps) >= 2:
        return max(0.0, (max(timestamps) - min(timestamps)).total_seconds())

    timestamps = []
    for attempt in attempts:
        ts = _parse_timestamp(attempt.get("timestamp"))
        if ts:
            timestamps.append(ts)
    if len(timestamps) >= 2:
        return max(0.0, (max(timestamps) - min(timestamps)).total_seconds())
    return None


def _scheduler_metadata(events: list[dict[str, Any]]) -> dict[str, Any]:
    if not events:
        return {}
    start = events[0]
    latest = events[-1]
    complete = next((event for event in reversed(events) if event.get("event") == "scheduler_complete"), None)
    return {
        "scheduler": start.get("scheduler") or latest.get("scheduler"),
        "target_attempts": latest.get("target_attempts") or start.get("target_attempts"),
        "submitted_total": latest.get("submitted_total"),
        "recorded_total": latest.get("recorded_total"),
        "expanded_submitted_total": latest.get("expanded_submitted_total"),
        "expanded_recorded_total": latest.get("expanded_recorded_total"),
        "refine_submitted_total": latest.get("refine_submitted_total"),
        "refine_recorded_total": latest.get("refine_recorded_total"),
        "failed_total": latest.get("failed_total"),
        "completed": bool(complete),
        "latest_event": latest.get("event"),
        "latest_timestamp": latest.get("timestamp"),
    }


def _proposal_metadata(run_name: str) -> dict[str, Any]:
    proposal_dir = Path("ai_theory_lab") / "proposals" / run_name
    files = sorted(proposal_dir.glob("*.json")) if proposal_dir.exists() else []
    llm_models: dict[str, int] = {}
    proposal_modes: dict[str, int] = {}
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        model = data.get("llm_model")
        if model:
            llm_models[str(model)] = llm_models.get(str(model), 0) + 1
        mode = data.get("proposal_mode")
        if mode:
            proposal_modes[str(mode)] = proposal_modes.get(str(mode), 0) + 1
    return {
        "proposal_json_count": len(files),
        "llm_models": llm_models,
        "proposal_modes": proposal_modes,
    }


def _safe_rate(numer: int, denom: int) -> float | None:
    return numer / denom if denom else None


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _median(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def _sector_metrics(
    name: str,
    attempts: list[dict[str, Any]],
    representatives: list[dict[str, Any]],
    lcdm: dict[str, Any] | None,
    wall_seconds: float | None,
) -> dict[str, Any]:
    accepted = [attempt for attempt in attempts if attempt.get("validated") and attempt.get("chi2") is not None]
    accepted_chi2 = sorted(_float(attempt.get("chi2")) for attempt in accepted)
    accepted_chi2 = [value for value in accepted_chi2 if not math.isnan(value)]
    best_chi2 = accepted_chi2[0] if accepted_chi2 else None
    top10 = accepted_chi2[:10]
    sector_reps = representatives if name == "all" else [
        attempt for attempt in representatives if _proposal_group(attempt) == name
    ]
    good_thresholds = {
        "unique_families_chi2_lt_1640": 1640.0,
        "unique_families_chi2_lt_1650": 1650.0,
        "unique_families_chi2_lt_1700": 1700.0,
        "unique_families_chi2_lt_2000": 2000.0,
    }
    good_counts = {
        key: sum(1 for attempt in sector_reps if _float(attempt.get("chi2")) < threshold)
        for key, threshold in good_thresholds.items()
    }
    effective_counts: dict[str, int] = {}
    for attempt in sector_reps:
        status = str(_effective_summary(attempt).get("effective_correction_status") or "unknown")
        effective_counts[status] = effective_counts.get(status, 0) + 1
    active_or_moderate = sum(
        1
        for attempt in sector_reps
        if _theory_track(attempt) == "eh_anchored"
        and str(_effective_summary(attempt).get("effective_correction_status") or "") in {"active", "moderate"}
    )
    scalar_counts: dict[str, int] = {}
    accepted_scalar_counts: dict[str, int] = {}
    track_counts: dict[str, int] = {}
    for attempt in attempts:
        theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
        scalar = str(theory.get("scalar_config") or "unknown")
        scalar_counts[scalar] = scalar_counts.get(scalar, 0) + 1
        track = _theory_track(attempt)
        track_counts[track] = track_counts.get(track, 0) + 1
    for attempt in accepted:
        theory = attempt.get("theory") if isinstance(attempt.get("theory"), dict) else {}
        scalar = str(theory.get("scalar_config") or "unknown")
        accepted_scalar_counts[scalar] = accepted_scalar_counts.get(scalar, 0) + 1
    entered_solver = sum(1 for attempt in attempts if attempt.get("entered_solver"))
    failure_counts: dict[str, int] = {}
    for attempt in attempts:
        for tag in attempt.get("failure_tags") or []:
            failure_counts[str(tag)] = failure_counts.get(str(tag), 0) + 1
    lcdm_delta = None
    lcdm_improvement = None
    if best_chi2 is not None and lcdm:
        lcdm_chi2 = _float(lcdm.get("chi2"))
        if not math.isnan(lcdm_chi2):
            lcdm_delta = best_chi2 - lcdm_chi2
            lcdm_improvement = lcdm_chi2 - best_chi2
    hours = wall_seconds / 3600.0 if wall_seconds and wall_seconds > 0 else None
    attempts_per_hour = len(attempts) / hours if hours else None
    accepted_per_hour = len(accepted) / hours if hours else None
    return {
        "sector": name,
        "attempts": len(attempts),
        "entered_solver": entered_solver,
        "entered_solver_rate": _safe_rate(entered_solver, len(attempts)),
        "accepted": len(accepted),
        "accept_rate": _safe_rate(len(accepted), len(attempts)),
        "best_chi2": best_chi2,
        "median_accepted_chi2": _median(accepted_chi2),
        "top10_mean_chi2": _mean(top10),
        "lcdm_chi2": lcdm.get("chi2") if lcdm else None,
        "best_delta_chi2_vs_lcdm": lcdm_delta,
        "best_chi2_improvement_over_lcdm": lcdm_improvement,
        "unique_families": len(sector_reps),
        **good_counts,
        "active_or_moderate_families": active_or_moderate,
        "effective_correction_counts": effective_counts,
        "scalar_counts": scalar_counts,
        "accepted_scalar_counts": accepted_scalar_counts,
        "track_counts": track_counts,
        "failure_tag_counts": failure_counts,
        "wall_time_hours": hours,
        "attempts_per_hour": attempts_per_hour,
        "accepted_per_hour": accepted_per_hour,
        "api_calls": None,
        "input_tokens": None,
        "output_tokens": None,
        "estimated_cost_usd": None,
    }


def _write_benchmark_outputs(
    out_dir: Path,
    run_name: str,
    feedback: dict[str, Any],
    attempts: list[dict[str, Any]],
    representatives: list[dict[str, Any]],
    lcdm: dict[str, Any] | None,
) -> dict[str, Any]:
    events = _read_scheduler_events(run_name)
    wall_seconds = _wall_time_seconds(attempts, events)
    group_names = sorted({_proposal_group(attempt) for attempt in attempts if _proposal_group(attempt)})
    sectors = ["all", *group_names]
    attempts_by_sector = {
        "all": attempts,
        **{group: [attempt for attempt in attempts if _proposal_group(attempt) == group] for group in group_names},
    }
    sector_metrics = [
        _sector_metrics(sector, attempts_by_sector[sector], representatives, lcdm, wall_seconds)
        for sector in sectors
    ]
    scheduler = _scheduler_metadata(events)
    proposal_meta = _proposal_metadata(run_name)
    benchmark = {
        "run_name": run_name,
        "generated_by": "ai_theory_lab.report",
        "ranking_rule": "chi2_total primary; AIC tie-breaker",
        "delta_chi2_vs_lcdm_definition": "model_chi2 - lcdm_chi2; negative means better than LCDM",
        "feedback_total_attempts": feedback.get("total_attempts"),
        "lcdm": lcdm or {},
        "scheduler": scheduler,
        "proposal_metadata": proposal_meta,
        "sectors": {row["sector"]: row for row in sector_metrics},
    }
    (out_dir / "benchmark_summary.json").write_text(json.dumps(benchmark, ensure_ascii=False, indent=2), encoding="utf-8")

    csv_fields = [
        "run_name",
        "sector",
        "attempts",
        "entered_solver",
        "entered_solver_rate",
        "accepted",
        "accept_rate",
        "best_chi2",
        "median_accepted_chi2",
        "top10_mean_chi2",
        "lcdm_chi2",
        "best_delta_chi2_vs_lcdm",
        "best_chi2_improvement_over_lcdm",
        "unique_families",
        "unique_families_chi2_lt_1640",
        "unique_families_chi2_lt_1650",
        "unique_families_chi2_lt_1700",
        "unique_families_chi2_lt_2000",
        "active_or_moderate_families",
        "wall_time_hours",
        "attempts_per_hour",
        "accepted_per_hour",
        "api_calls",
        "input_tokens",
        "output_tokens",
        "estimated_cost_usd",
        "scalar_counts_json",
        "accepted_scalar_counts_json",
        "track_counts_json",
        "effective_correction_counts_json",
        "failure_tag_counts_json",
    ]
    with (out_dir / "benchmark_by_sector.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for row in sector_metrics:
            flat = {"run_name": run_name, **row}
            for key in [
                "scalar_counts",
                "accepted_scalar_counts",
                "track_counts",
                "effective_correction_counts",
                "failure_tag_counts",
            ]:
                flat[f"{key}_json"] = json.dumps(flat.pop(key), ensure_ascii=False, sort_keys=True)
            writer.writerow({field: flat.get(field) for field in csv_fields})
    return benchmark


def generate_report(run_name: str, top_n: int = 20, output_dir: Path | None = None) -> Path:
    memory_dir = Path("ai_theory_lab") / "memory" / run_name
    feedback_path = memory_dir / "feedback_summary.json"
    if not feedback_path.exists():
        raise FileNotFoundError(f"Missing feedback summary: {feedback_path}")
    feedback = _read_json(feedback_path)
    accepted = _accepted_attempts(feedback, memory_dir)
    accepted.sort(key=lambda a: _float(a.get("chi2")))
    representatives = _family_representatives(accepted)
    accepted = _attach_effective_correction_diagnostics(accepted)
    representatives = _attach_effective_correction_diagnostics(representatives)
    lcdm = _find_lcdm_reference(accepted)
    out_dir = output_dir or Path("ai_theory_lab") / "reports" / run_name
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "accepted_summary.json").write_text(json.dumps(accepted, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "accepted_family_representatives.json").write_text(
        json.dumps(representatives, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if lcdm:
        (out_dir / "lcdm_reference.json").write_text(json.dumps(lcdm, ensure_ascii=False, indent=2), encoding="utf-8")
    benchmark = _write_benchmark_outputs(out_dir, run_name, feedback, accepted, representatives, lcdm)
    _write_plots(out_dir, representatives, top_n=top_n)
    _write_lagrangian_reports(out_dir, representatives, top_n=top_n, lcdm=lcdm)
    _write_track_reports(out_dir, representatives)
    _write_group_reports(out_dir, representatives)
    _write_summary(out_dir, run_name, feedback, accepted, representatives, top_n=top_n, lcdm=lcdm, benchmark=benchmark)
    return out_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate report files for a current-loop agent run.")
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--top-n", type=int, default=20)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    out_dir = generate_report(args.run_name, top_n=args.top_n, output_dir=args.output_dir)
    print(out_dir)


if __name__ == "__main__":
    main()
