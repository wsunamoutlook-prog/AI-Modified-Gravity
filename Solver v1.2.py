#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
top5_lagrangian_summary_and_plots.py

Purpose
-------
After running scan_all_lagrangians_bao_solver.py, this script collects the
top-5 fitted Lagrangians, reads their raw Lagrangian forms from lagrangians.pkl,
prints the numerical initial conditions / fitted parameters, and draws one
plot for each top model plus an overlay plot.

It is designed for your project folder:
    /Users/sunwenrong/Desktop/AI Modified Gravity/TheoryGPT-main/Modify GR

Outputs go to:
    /Users/sunwenrong/Desktop/AI Modified Gravity/TheoryGPT-main/Modify GR/solver_results_1

If solver_results_1/model_ranking.csv does not exist, the script will try to run:
    scan_all_lagrangians_bao_solver.py

Notes
-----
- The numerical solution is not an analytic expression.
- The solver integrates in x = ln(a) = -ln(1+z).
- It uses h = H/H0, varphi = phi/Mp, q = dvarphi/dln(a).
- Initial condition convention:
      x0 = 0, a0 = 1, h0 = 1
  and, if scalar exists:
      varphi0 = sampled/fitted, q0 = solved from E_N(x=0)=0.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import math
import os
import pickle
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

import numpy as np

try:
    import pandas as pd
except Exception as exc:
    raise RuntimeError("This script needs pandas. Please install pandas in your theory_gpt environment.") from exc

try:
    import matplotlib.pyplot as plt
except Exception as exc:
    raise RuntimeError("This script needs matplotlib. Please install matplotlib in your theory_gpt environment.") from exc


# ---------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------

DEFAULT_PROJECT_DIR = Path("/Users/sunwenrong/Desktop/AI Modified Gravity/TheoryGPT-main/Modify GR")
DEFAULT_OUTPUT_SUBDIR = "solver_results_1"
M_P_REDUCED_EV = 2.435e27
KM_S_MPC_TO_EV = 2.133119e-35

FALLBACK_BAO_DATA = np.array([
    [0.38,  81.5,   1.9],
    [0.51,  90.4,   1.9],
    [0.61,  97.3,   2.1],
    [1.48, 153.81,  6.39],
    [2.33, 224.0,   8.0],
    [2.40, 226.0,   8.0],
], dtype=float)

STANDARD_RESULT_COLUMNS = {
    "lag_id", "success", "reason",
    "chi2", "chi2_per_point", "AIC", "BIC", "k_params", "max_abs_constraint",
    "H0_km_s_Mpc", "Omega_m0", "rho_bar", "mu_m_over_H0",
    "varphi0_phi_over_Mp", "q0_dvarphi_dln_a", "eps_HM_H0_over_Mp",
}


# ---------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------

def resolve_project_dir(user_project_dir: Optional[str]) -> Path:
    if user_project_dir:
        return Path(user_project_dir).expanduser().resolve()
    if DEFAULT_PROJECT_DIR.exists():
        return DEFAULT_PROJECT_DIR
    return Path.cwd().resolve()


def find_scan_script(project_dir: Path) -> Optional[Path]:
    candidates = [
        project_dir / "scan_all_lagrangians_bao_solver.py",
        Path.cwd() / "scan_all_lagrangians_bao_solver.py",
        Path("/mnt/data/scan_all_lagrangians_bao_solver.py"),
    ]
    for p in candidates:
        if p.exists():
            return p.resolve()
    return None


def find_lagrangians_pkl(project_dir: Path, user_pkl: Optional[str] = None) -> Optional[Path]:
    candidates = []
    if user_pkl:
        candidates.append(Path(user_pkl).expanduser())
    candidates += [
        project_dir / "lagrangians.pkl",
        project_dir / "lagrangians(1).pkl",
        Path.cwd() / "lagrangians.pkl",
        Path.cwd() / "lagrangians(1).pkl",
        Path("/mnt/data/lagrangians.pkl"),
        Path("/mnt/data/lagrangians(1).pkl"),
    ]
    for p in candidates:
        if p.exists():
            return p.resolve()
    return None


# ---------------------------------------------------------------------
# Import scan module / data
# ---------------------------------------------------------------------

def import_scan_module(scan_script: Optional[Path]):
    if scan_script is None or not scan_script.exists():
        return None
    spec = importlib.util.spec_from_file_location("scan_all_lagrangians_bao_solver", str(scan_script))
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    # dataclasses need the module to be present in sys.modules during exec_module.
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def get_hz_data(scan_module=None) -> np.ndarray:
    """Use the same data as the scan script if possible; otherwise fallback BAO H(z)."""
    if scan_module is not None:
        try:
            choice = getattr(scan_module, "DATA_CHOICE", "bao")
            return np.asarray(scan_module.select_data(choice), dtype=float)
        except Exception:
            pass
    return FALLBACK_BAO_DATA.copy()


# ---------------------------------------------------------------------
# Load pkl and map Lagrangian IDs
# ---------------------------------------------------------------------

def load_lagrangian_map(pkl_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    The pkl appears to be a dict keyed by n_terms, where each value is a list
    of candidate dictionaries. The Lagrangian ID used by eom_summary/scan is
    the flattened sequential index, starting from 1, over sorted n_terms keys.
    """
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)

    lag_map: Dict[str, Dict[str, Any]] = {}

    if isinstance(data, dict):
        counter = 0
        for key in sorted(data.keys()):
            items = data[key]
            if not isinstance(items, list):
                continue
            for item in items:
                counter += 1
                lag_map[str(counter)] = item
    elif isinstance(data, list):
        for i, item in enumerate(data, 1):
            lag_map[str(i)] = item
    else:
        raise TypeError(f"Unsupported pkl structure: {type(data)}")

    return lag_map


def raw_lagrangian_string(lag_map: Dict[str, Dict[str, Any]], lag_id: str) -> str:
    item = lag_map.get(str(lag_id))
    if not item:
        return f"[not found in pkl for Lagrangian #{lag_id}]"
    return str(item.get("general", "[general form missing]"))


def raw_terms_string(lag_map: Dict[str, Dict[str, Any]], lag_id: str) -> str:
    item = lag_map.get(str(lag_id))
    if not item:
        return ""
    terms = item.get("terms", [])
    if not isinstance(terms, list):
        return ""
    lines = []
    for j, term in enumerate(terms, 1):
        coeff = term.get("coeff_symbol", "?")
        cand = term.get("candidate", "?")
        md = term.get("mass_dim", "?")
        mp = term.get("mp_power", "?")
        fixed = term.get("fixed", False)
        fixed_s = ", fixed" if fixed else ""
        lines.append(f"    [{j}] coeff={coeff}, mp_power={mp}, dim={md}{fixed_s}: {cand}")
    return "\n".join(lines)


# ---------------------------------------------------------------------
# Ranking and solution CSVs
# ---------------------------------------------------------------------

def ensure_scan_results(project_dir: Path, output_dir: Path, scan_script: Optional[Path], force_scan: bool = False):
    ranking_csv = output_dir / "model_ranking.csv"
    if ranking_csv.exists() and not force_scan:
        return

    if scan_script is None:
        raise FileNotFoundError(
            f"Cannot find {ranking_csv}, and scan_all_lagrangians_bao_solver.py was not found."
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["SOLVER_OUTPUT_DIR"] = str(output_dir)

    # Keep user's N_SAMPLES_PER_MODEL if set; otherwise use scan script default.
    print(f"[INFO] model_ranking.csv not found or force_scan=True. Running scan script:")
    print(f"       {scan_script}")
    print(f"[INFO] Output directory: {output_dir}")
    subprocess.run([sys.executable, str(scan_script)], cwd=str(project_dir), env=env, check=True)


def read_ranking(output_dir: Path, sort_by: str, top_n: int) -> pd.DataFrame:
    ranking_csv = output_dir / "model_ranking.csv"
    if not ranking_csv.exists():
        raise FileNotFoundError(f"Missing ranking csv: {ranking_csv}")

    df = pd.read_csv(ranking_csv)
    if df.empty:
        raise RuntimeError(f"{ranking_csv} exists but contains no accepted model.")

    # Coerce numeric columns.
    for col in ["chi2", "chi2_per_point", "AIC", "BIC", "k_params", "max_abs_constraint"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    sort_by_norm = sort_by.lower()
    if sort_by_norm == "rankfile":
        ranked = df.copy()
    elif sort_by_norm == "chi2":
        ranked = df.sort_values(["chi2", "AIC", "BIC"], ascending=True).copy()
    elif sort_by_norm == "aic":
        ranked = df.sort_values(["AIC", "chi2", "BIC"], ascending=True).copy()
    elif sort_by_norm == "bic":
        ranked = df.sort_values(["BIC", "chi2", "AIC"], ascending=True).copy()
    else:
        raise ValueError("--sort-by must be rankfile, chi2, AIC, or BIC.")

    return ranked.head(top_n).reset_index(drop=True)


def find_solution_csv(output_dir: Path, lag_id: str) -> Optional[Path]:
    # Best named top files from scan script.
    matches = sorted(output_dir.glob(f"top_*_lagrangian_{lag_id}_solution.csv"))
    if matches:
        return matches[0]

    # If global best happens to match, allow best_solution.csv.
    best = output_dir / "best_solution.csv"
    if best.exists():
        # We cannot always know the lag id from the csv itself, so only use this
        # if no other solution exists and the caller is rank #1.
        return None

    return None


def numeric_or_none(row: pd.Series, col: str) -> Optional[float]:
    if col not in row.index:
        return None
    val = row[col]
    try:
        if pd.isna(val):
            return None
        return float(val)
    except Exception:
        return None


def nonstandard_params(row: pd.Series) -> Dict[str, float]:
    out = {}
    for col in row.index:
        if col in STANDARD_RESULT_COLUMNS:
            continue
        if str(col).startswith("Unnamed"):
            continue
        val = numeric_or_none(row, col)
        if val is None:
            continue
        out[col] = val
    return out


# ---------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------

def plot_single_model(data: np.ndarray, sol_csv: Path, lag_id: str, rank: int, metrics: Dict[str, float], out_path: Path):
    df = pd.read_csv(sol_csv)
    if "z" not in df.columns or "H_km_s_Mpc" not in df.columns:
        raise ValueError(f"{sol_csv} does not contain z and H_km_s_Mpc columns.")

    df = df.sort_values("z")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(data[:, 0], data[:, 1], yerr=data[:, 2], fmt="o", capsize=3, label="BAO H(z) data")
    ax.plot(df["z"].values, df["H_km_s_Mpc"].values, lw=2.2, label=f"L#{lag_id} numerical H(z)")

    subtitle = f"rank {rank}, chi2={metrics.get('chi2', math.nan):.3g}, AIC={metrics.get('AIC', math.nan):.3g}, BIC={metrics.get('BIC', math.nan):.3g}"
    ax.set_title(f"Top {rank}: Lagrangian #{lag_id}\n{subtitle}")
    ax.set_xlabel("z")
    ax.set_ylabel("H(z) [km/s/Mpc]")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def plot_overlay(data: np.ndarray, ranked: pd.DataFrame, solution_paths: Dict[str, Path], out_path: Path):
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.errorbar(data[:, 0], data[:, 1], yerr=data[:, 2], fmt="o", capsize=3, label="BAO H(z) data", zorder=5)

    for i, row in ranked.iterrows():
        lag_id = str(row["lag_id"])
        sol_csv = solution_paths.get(lag_id)
        if sol_csv is None:
            continue
        df = pd.read_csv(sol_csv).sort_values("z")
        ax.plot(
            df["z"].values,
            df["H_km_s_Mpc"].values,
            lw=1.8,
            label=f"#{i+1} L{lag_id}, chi2={float(row['chi2']):.2g}"
        )

    ax.set_title("Top fitted Lagrangians: numerical H(z)")
    ax.set_xlabel("z")
    ax.set_ylabel("H(z) [km/s/Mpc]")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


# ---------------------------------------------------------------------
# Text report
# ---------------------------------------------------------------------

def format_float(x: Optional[float], precision: int = 8) -> str:
    if x is None:
        return "N/A"
    if not np.isfinite(x):
        return "N/A"
    if abs(x) != 0 and (abs(x) < 1e-4 or abs(x) >= 1e5):
        return f"{x:.{precision}e}"
    return f"{x:.{precision}g}"


def build_text_report(
    ranked: pd.DataFrame,
    lag_map: Dict[str, Dict[str, Any]],
    output_dir: Path,
    pkl_path: Path,
    sort_by: str,
    solution_paths: Dict[str, Path],
    generated_plot_paths: List[Path],
) -> str:
    lines: List[str] = []
    lines.append("Top fitted Lagrangians: forms, initial conditions, and numerical-fit parameters")
    lines.append("=" * 92)
    lines.append("")
    lines.append(f"Output directory: {output_dir}")
    lines.append(f"Lagrangian pkl: {pkl_path}")
    lines.append(f"Ranking source: {output_dir / 'model_ranking.csv'}")
    lines.append(f"Top selection rule: {sort_by}")
    lines.append("")
    lines.append("Numerical convention")
    lines.append("- Independent variable: x = ln(a) = -ln(1+z).")
    lines.append("- Dimensionless Hubble variable: h(x) = H(x) / H0.")
    lines.append("- Scalar variable: varphi(x) = phi(x) / Mpred.")
    lines.append("- Scalar slope: q(x) = d varphi / d ln(a).")
    lines.append("- Universal initial conditions: x0 = 0, a0 = 1, h0 = 1.")
    lines.append("- Physical adot0 is not independently sampled; h0=1 is equivalent to adot0 = H0_phys.")
    lines.append("- Matter density in the code: rho_bar = rho_m0/(Mpred^2 H0^2) = 3 Omega_m0.")
    lines.append("- If scalar is present, q0 is selected by the Hamiltonian/Friedmann constraint E_N(x=0)=0.")
    lines.append("- Mpred is the reduced Planck mass, Mpred = 2.435e27 eV.")
    lines.append("")

    for i, row in ranked.iterrows():
        rank = i + 1
        lag_id = str(row["lag_id"])

        H0 = numeric_or_none(row, "H0_km_s_Mpc")
        eps = numeric_or_none(row, "eps_HM_H0_over_Mp")
        mu = numeric_or_none(row, "mu_m_over_H0")
        H0_eV = None if H0 is None else H0 * KM_S_MPC_TO_EV
        m_eV = None if H0_eV is None or mu is None else mu * H0_eV

        lines.append("")
        lines.append("=" * 92)
        lines.append(f"Rank {rank}: Lagrangian #{lag_id}")
        lines.append("=" * 92)
        lines.append("")
        lines.append("Raw Lagrangian from pkl")
        lines.append(str(raw_lagrangian_string(lag_map, lag_id)))
        lines.append("")
        term_s = raw_terms_string(lag_map, lag_id)
        if term_s:
            lines.append("Raw terms")
            lines.append(term_s)
            lines.append("")

        lines.append("Fit metrics")
        lines.append(f"  chi2            = {format_float(numeric_or_none(row, 'chi2'))}")
        lines.append(f"  chi2 per point  = {format_float(numeric_or_none(row, 'chi2_per_point'))}")
        lines.append(f"  AIC             = {format_float(numeric_or_none(row, 'AIC'))}")
        lines.append(f"  BIC             = {format_float(numeric_or_none(row, 'BIC'))}")
        lines.append(f"  k_params        = {format_float(numeric_or_none(row, 'k_params'), 0)}")
        lines.append(f"  max |E_N|       = {format_float(numeric_or_none(row, 'max_abs_constraint'))}")
        lines.append("")

        lines.append("Initial conditions and sampled/fitted values")
        lines.append("  x0 = ln(a0)                       = 0")
        lines.append("  a0                                = 1")
        lines.append("  h0 = H0/H0                        = 1")
        lines.append("  adot0 / H0_phys                   = 1")
        lines.append(f"  H0_phys [km/s/Mpc]                = {format_float(H0)}")
        lines.append(f"  H0_phys [eV]                      = {format_float(H0_eV)}")
        lines.append(f"  eps_HM = H0/Mpred                 = {format_float(eps)}")
        lines.append(f"  Omega_m0                          = {format_float(numeric_or_none(row, 'Omega_m0'))}")
        lines.append(f"  rho_bar = rho_m0/(Mpred^2 H0^2)   = {format_float(numeric_or_none(row, 'rho_bar'))}")

        varphi0 = numeric_or_none(row, "varphi0_phi_over_Mp")
        q0 = numeric_or_none(row, "q0_dvarphi_dln_a")
        if varphi0 is not None:
            lines.append(f"  varphi0 = phi0/Mpred              = {format_float(varphi0)}")
            lines.append(f"  phi0 [eV]                         = {format_float(varphi0 * M_P_REDUCED_EV)}")
        if q0 is not None:
            lines.append(f"  q0 = dvarphi/dln(a)|0             = {format_float(q0)}")
            lines.append(f"  phidot0/(Mpred H0) = h0*q0        = {format_float(q0)}")
        if mu is not None:
            lines.append(f"  mu = m/H0                         = {format_float(mu)}")
            lines.append(f"  m [eV]                            = {format_float(m_eV)}")

        free_params = nonstandard_params(row)
        if free_params:
            lines.append("")
            lines.append("Free coupling values used in this best numerical sample")
            for k, v in sorted(free_params.items()):
                lines.append(f"  {k:<16} = {format_float(v)}")

        sol_csv = solution_paths.get(lag_id)
        lines.append("")
        lines.append("Numerical solution file")
        lines.append(f"  {sol_csv if sol_csv is not None else '[not found]'}")

    lines.append("")
    lines.append("=" * 92)
    lines.append("Generated plots")
    lines.append("=" * 92)
    for p in generated_plot_paths:
        lines.append(f"  {p}")

    lines.append("")
    lines.append("Interpretation reminder")
    lines.append("- These are numerical IVP solutions sampled over parameter priors, not analytic formulas.")
    lines.append("- The table gives the best sampled point for each top model under the current scan.")
    lines.append("- If N_SAMPLES_PER_MODEL is small, the ranking is a random-search result, not a guaranteed global optimum.")
    lines.append("- To make the result more stable, rerun the scan with e.g. N_SAMPLES_PER_MODEL=1000 or 5000.")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", default=None, help="Project folder. Default is your Modify GR folder if it exists, otherwise cwd.")
    parser.add_argument("--output-dir", default=None, help="Output folder. Default: project_dir/solver_results_1.")
    parser.add_argument("--pkl", default=None, help="Path to lagrangians.pkl or lagrangians(1).pkl.")
    parser.add_argument("--top-n", type=int, default=5, help="Number of top models to summarize.")
    parser.add_argument("--sort-by", default="rankfile", choices=["rankfile", "chi2", "AIC", "BIC"],
                        help="rankfile follows model_ranking.csv order; chi2/AIC/BIC resort the table.")
    parser.add_argument("--force-scan", action="store_true", help="Rerun scan_all_lagrangians_bao_solver.py before summarizing.")
    args = parser.parse_args()

    project_dir = resolve_project_dir(args.project_dir)
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else (project_dir / DEFAULT_OUTPUT_SUBDIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    scan_script = find_scan_script(project_dir)
    scan_module = import_scan_module(scan_script)
    data = get_hz_data(scan_module)

    pkl_path = find_lagrangians_pkl(project_dir, args.pkl)
    if pkl_path is None:
        raise FileNotFoundError(
            "Could not find lagrangians.pkl or lagrangians(1).pkl. "
            "Put it in the project folder or pass --pkl /path/to/lagrangians.pkl."
        )

    ensure_scan_results(project_dir, output_dir, scan_script, force_scan=args.force_scan)

    lag_map = load_lagrangian_map(pkl_path)
    ranked = read_ranking(output_dir, args.sort_by, args.top_n)

    # Locate solution CSVs and generate plots.
    solution_paths: Dict[str, Path] = {}
    generated_plots: List[Path] = []

    for i, row in ranked.iterrows():
        rank = i + 1
        lag_id = str(row["lag_id"])
        sol_csv = find_solution_csv(output_dir, lag_id)
        if sol_csv is not None and sol_csv.exists():
            solution_paths[lag_id] = sol_csv
            plot_path = output_dir / f"top_{rank:02d}_lagrangian_{lag_id}_Hz_fit.png"
            metrics = {
                "chi2": float(row["chi2"]) if "chi2" in row else math.nan,
                "AIC": float(row["AIC"]) if "AIC" in row else math.nan,
                "BIC": float(row["BIC"]) if "BIC" in row else math.nan,
            }
            plot_single_model(data, sol_csv, lag_id, rank, metrics, plot_path)
            generated_plots.append(plot_path)
        else:
            print(f"[WARNING] Could not find solution CSV for Lagrangian #{lag_id}. "
                  f"Run scan script again or use --sort-by rankfile.")

    overlay_path = output_dir / "top5_overlay_Hz_fit.png"
    if solution_paths:
        plot_overlay(data, ranked, solution_paths, overlay_path)
        generated_plots.append(overlay_path)

    # Report text.
    report = build_text_report(
        ranked=ranked,
        lag_map=lag_map,
        output_dir=output_dir,
        pkl_path=pkl_path,
        sort_by=args.sort_by,
        solution_paths=solution_paths,
        generated_plot_paths=generated_plots,
    )

    report_path = output_dir / "top5_lagrangians_initial_conditions.txt"
    report_path.write_text(report, encoding="utf-8")

    # Also save the exact top table as csv.
    top_csv = output_dir / "top5_selected_models.csv"
    ranked.to_csv(top_csv, index=False)

    print("")
    print("Done.")
    print(f"Top-5 text report: {report_path}")
    print(f"Top-5 table:       {top_csv}")
    for p in generated_plots:
        print(f"Plot:              {p}")
    print("")


if __name__ == "__main__":
    main()
