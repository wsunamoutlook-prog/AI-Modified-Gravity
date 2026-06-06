from __future__ import annotations

import argparse
import csv
import json
import math
import pickle
from pathlib import Path
from typing import Any

from .effective_corrections import diagnostics_for_attempt


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


def _solver_dir(attempt: dict[str, Any]) -> Path | None:
    value = attempt.get("solver_output_dir")
    return Path(value) if value else None


def _run_dir(attempt: dict[str, Any]) -> Path | None:
    solver_dir = _solver_dir(attempt)
    if not solver_dir:
        return None
    # .../agent_solver_result/agent_solve -> run root
    return solver_dir.parents[1]


def _load_lagrangian(attempt: dict[str, Any]) -> dict[str, Any]:
    run_dir = _run_dir(attempt)
    if not run_dir:
        return {}
    pkl_path = run_dir / "agent_lagrangians.pkl"
    if not pkl_path.exists():
        return {}
    with pkl_path.open("rb") as f:
        data = pickle.load(f)
    if isinstance(data, dict):
        for group in data.values():
            if group:
                return group[0]
    if isinstance(data, list) and data:
        return data[0]
    return {}


def _coefficient_value(row: dict[str, str], symbol: str) -> str | None:
    if symbol in {"1", "COEFF_FIXED_1"}:
        return "1"
    candidates = [
        symbol,
        symbol.replace("\\", ""),
        f"coef:{symbol.replace('\\', '')}",
        f"coefficient:{symbol.replace('\\', '')}",
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


def _family_key(attempt: dict[str, Any]) -> str:
    return str(attempt.get("coarse_family_key") or attempt.get("family_key") or attempt.get("loop_id"))


def _family_representatives(accepted: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best_by_family: dict[str, dict[str, Any]] = {}
    for attempt in sorted(accepted, key=lambda a: _float(a.get("chi2"))):
        key = _family_key(attempt)
        if key not in best_by_family:
            best_by_family[key] = attempt
    return sorted(best_by_family.values(), key=lambda a: _float(a.get("chi2")))


def _attach_effective_correction_diagnostics(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for attempt in attempts:
        row = dict(attempt)
        row["effective_correction"] = diagnostics_for_attempt(row)
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

    top = accepted[:top_n]
    labels = [str(a.get("loop_id")) for a in top]
    chi2 = [_float(a.get("chi2")) for a in top]

    fig, ax = plt.subplots(figsize=(max(8, 0.55 * len(top)), 4.5))
    ax.bar(range(len(top)), chi2, color="#2f6f9f")
    ax.set_xticks(range(len(top)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylabel("chi2")
    ax.set_title(f"Top {len(top)} accepted family representatives chi2")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_dir / "accepted_chi2_bar.png", dpi=180)
    plt.close(fig)

    overlay = top[: min(8, len(top))]
    fig, ax = plt.subplots(figsize=(8, 5))
    for rank, attempt in enumerate(overlay, start=1):
        z, h = _load_solution(attempt)
        if z and h:
            ax.plot(z, h, lw=2, label=f"#{rank} {attempt.get('loop_id')} chi2={_fmt(attempt.get('chi2'), 2)}")
    ax.set_xlabel("z")
    ax.set_ylabel("h(z)=H/H0")
    ax.set_title("Top accepted family representative h(z)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "top_h_overlay.png", dpi=180)
    plt.close(fig)

    panels = top[: min(3, len(top))]
    if panels:
        fig, axes = plt.subplots(len(panels), 1, figsize=(8, 3 * len(panels)), sharex=True)
        if len(panels) == 1:
            axes = [axes]
        for ax, attempt in zip(axes, panels):
            z, h = _load_solution(attempt)
            if z and h:
                ax.plot(z, h, lw=2, color="#2f6f9f")
            ax.set_ylabel("h(z)")
            ax.set_title(f"{attempt.get('loop_id')} chi2={_fmt(attempt.get('chi2'), 3)}")
            ax.grid(alpha=0.25)
        axes[-1].set_xlabel("z")
        fig.tight_layout()
        fig.savefig(out_dir / "top3_h_panels.png", dpi=180)
        plt.close(fig)


def _write_summary(
    out_dir: Path,
    run_name: str,
    feedback: dict[str, Any],
    accepted: list[dict[str, Any]],
    representatives: list[dict[str, Any]],
    top_n: int,
) -> None:
    failures = feedback.get("failure_tag_counts") or {}
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
        f"| Accepted attempts | {feedback.get('validated_count', len(accepted))} |",
        f"| Accepted theory families shown | {len(representatives)} |",
        f"| Best chi2 | {_fmt(feedback.get('best_chi2'), 6)} |",
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
        "",
        "## Plots",
        "",
        "![Accepted chi2 ranking](accepted_chi2_bar.png)",
        "",
        "![Top h(z) overlay](top_h_overlay.png)",
        "",
        "![Top 3 h(z) panels](top3_h_panels.png)",
        "",
        "## Top Accepted Family Representatives",
        "",
        "| Rank | Family | Loop | chi2 | Status | Max rel. effect | Dominant correction | Sample | H0 | Omega_m0 | lambda_H | Scalar | Potential | Operators |",
        "|---:|---|---|---:|---|---:|---|---:|---:|---:|---:|---|---|---|",
    ]
    for rank, attempt in enumerate(representatives[:top_n], start=1):
        theory = attempt.get("theory") or {}
        row = _read_csv_first(
            Path(attempt["accepted_samples_summary_path"]) if attempt.get("accepted_samples_summary_path") else None
        )
        ops = "; ".join(theory.get("operators") or [])
        potential = json.dumps(theory.get("potential_types") or {}, ensure_ascii=False)
        effective = _effective_summary(attempt)
        lines.append(
            f"| {rank} | {_family_key(attempt)} | {attempt.get('loop_id')} | {_fmt(attempt.get('chi2'), 6)} | "
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
        row = _read_csv_first(
            Path(attempt["accepted_samples_summary_path"]) if attempt.get("accepted_samples_summary_path") else None
        )
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


def _write_lagrangian_reports(out_dir: Path, accepted: list[dict[str, Any]], top_n: int) -> None:
    csv_rows: list[dict[str, Any]] = []
    csv_fieldnames = [
        "rank",
        "loop_id",
        "chi2",
        "chi2_sn",
        "chi2_bao",
        "aic",
        "bic",
        "scalar_config",
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
        accepted_path = Path(attempt["accepted_samples_summary_path"]) if attempt.get("accepted_samples_summary_path") else None
        row = _read_csv_first(accepted_path)
        terms = lag.get("terms") or []
        raw = lag.get("general") or ""
        bestfit = _bestfit_general(raw, terms, row)
        theory = attempt.get("theory") or {}
        solution_path = _solution_path(attempt)
        effective = _effective_summary(attempt)

        csv_rows.append(
            {
                "rank": rank,
                "loop_id": attempt.get("loop_id"),
                "chi2": attempt.get("chi2"),
                "chi2_sn": row.get("chi2_sn"),
                "chi2_bao": row.get("chi2_bao"),
                "aic": attempt.get("aic"),
                "bic": attempt.get("bic"),
                "scalar_config": theory.get("scalar_config"),
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
            f"- scalar_config: `{theory.get('scalar_config', '')}`",
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
            f"- accepted_samples_summary.csv: `{accepted_path or ''}`",
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
    out_dir = output_dir or Path("ai_theory_lab") / "reports" / run_name
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "accepted_summary.json").write_text(json.dumps(accepted, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "accepted_family_representatives.json").write_text(
        json.dumps(representatives, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    _write_plots(out_dir, representatives, top_n=top_n)
    _write_lagrangian_reports(out_dir, representatives, top_n=top_n)
    _write_summary(out_dir, run_name, feedback, accepted, representatives, top_n=top_n)
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
