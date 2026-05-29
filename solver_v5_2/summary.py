#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Top-10 reporting and plotting helpers for Solver v5.2."""
from __future__ import annotations

from .core import *

# =============================================================================
# Integrated Top-10 summary and plotting
# =============================================================================

def _find_lagrangian_pkl_for_summary() -> Optional[Path]:
    here = Path(__file__).resolve().parent
    candidates = [
        Path(os.environ["LAGRANGIANS_PKL_PATH"]).expanduser()
        if os.environ.get("LAGRANGIANS_PKL_PATH") else None,
        Path.cwd() / "lagrangians.pkl",
        Path.cwd() / "lagrangians(1).pkl",
        here / "lagrangians.pkl",
        here / "lagrangians(1).pkl",
    ]
    for p in candidates:
        if p is not None and p.exists() and p.is_file():
            return p.resolve()
    return None


def _load_lagrangian_map_from_pkl(pkl_path: Path) -> Dict[str, Dict[str, Any]]:
    import pickle
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


def _raw_lagrangian_string(lag_map: Dict[str, Dict[str, Any]], lag_id: str) -> str:
    item = lag_map.get(str(lag_id))
    if not item:
        return f"[not found in pkl for Lagrangian #{lag_id}]"
    return str(item.get("general", "[general form missing]"))


def _raw_terms_string(lag_map: Dict[str, Dict[str, Any]], lag_id: str) -> str:
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
        lp = term.get("lambda_power", "?")
        fixed = term.get("fixed", False)
        sector = term.get("sector", "gravity")
        pot = term.get("potential_type", "")
        fixed_s = ", fixed" if fixed else ""
        sector_s = f", {sector}" if sector != "gravity" else ""
        pot_s = f", pot={pot}" if pot else ""
        lines.append(f"    [{j}] coeff={coeff}, Λ^{lp}, dim={md}{fixed_s}{sector_s}{pot_s}: {cand}")
    return "\n".join(lines)


def _fmt(x, precision=8) -> str:
    try:
        if x is None or (isinstance(x, float) and not np.isfinite(x)):
            return "N/A"
        xf = float(x)
        if abs(xf) != 0 and (abs(xf) < 1e-4 or abs(xf) >= 1e5):
            return f"{xf:.{precision}e}"
        return f"{xf:.{precision}g}"
    except Exception:
        return str(x)


def _read_model_ranking_csv() -> List[Dict[str, str]]:
    ranking_path = OUTPUT_DIR / "model_ranking.csv"
    if not ranking_path.exists():
        print(f"[INFO] No model ranking file found; skipping top-model summary: {ranking_path}", flush=True)
        return []
    with open(ranking_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        print(f"[INFO] Ranking file has no accepted models; skipping top-model summary: {ranking_path}", flush=True)
        return []
    return rows


def _float_from_row(row: Dict[str, str], key: str, default=np.nan) -> float:
    try:
        val = row.get(key, "")
        if val is None or val == "":
            return default
        return float(val)
    except Exception:
        return default


def _find_top_solution_csv(rank: int, lag_id: str) -> Optional[Path]:
    exact = OUTPUT_DIR / f"top_{rank:02d}_lagrangian_{lag_id}_solution.csv"
    if exact.exists():
        return exact
    matches = sorted(OUTPUT_DIR.glob(f"top_*_lagrangian_{lag_id}_solution.csv"))
    if matches:
        return matches[0]
    if rank == 1 and (OUTPUT_DIR / "best_solution.csv").exists():
        return OUTPUT_DIR / "best_solution.csv"
    return None


def _read_solution_csv(path: Path) -> Dict[str, np.ndarray]:
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    cols = reader.fieldnames or []
    arr = {}
    for c in cols:
        vals = []
        for r in rows:
            try:
                vals.append(float(r[c]))
            except Exception:
                vals.append(np.nan)
        arr[c] = np.asarray(vals, dtype=float)
    return arr


def _plot_top_model(rank: int, row: Dict[str, str], sol_path: Path, out_path: Path):
    if plt is None:
        return
    sol = _read_solution_csv(sol_path)
    if "z" not in sol or "h_dimensionless" not in sol:
        return
    order = np.argsort(sol["z"])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(sol["z"][order], sol["h_dimensionless"][order], lw=2.2, label=f"L#{row.get('lag_id')} numerical h(z)")
    ax.set_title(
        f"Top {rank}: Lagrangian #{row.get('lag_id')}\n"
        f"chi2={_float_from_row(row, 'chi2'):.4g}, AIC={_float_from_row(row, 'AIC'):.4g}")
    ax.set_xlabel("z")
    ax.set_ylabel("h(z)=H/H0")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def _plot_top_overlay(top_rows: List[Dict[str, str]], sol_paths: Dict[str, Path], out_path: Path):
    if plt is None:
        return
    fig, ax = plt.subplots(figsize=(9, 6))
    for i, row in enumerate(top_rows, 1):
        lag_id = str(row.get("lag_id"))
        sol_path = sol_paths.get(lag_id)
        if sol_path is None:
            continue
        sol = _read_solution_csv(sol_path)
        if "z" not in sol or "h_dimensionless" not in sol:
            continue
        order = np.argsort(sol["z"])
        ax.plot(sol["z"][order], sol["h_dimensionless"][order], lw=1.8,
                label=f"#{i} L{lag_id}, chi2={_float_from_row(row, 'chi2'):.3g}")
    ax.set_title("Top fitted Lagrangians: numerical h(z)")
    ax.set_xlabel("z")
    ax.set_ylabel("h(z)=H/H0")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def run_top10_summary(top_n: int = 10):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = _read_model_ranking_csv()
    if not rows:
        return
    top_rows = rows[:top_n]

    pkl_path = _find_lagrangian_pkl_for_summary()
    lag_map: Dict[str, Dict[str, Any]] = {}
    if pkl_path is not None:
        try:
            lag_map = _load_lagrangian_map_from_pkl(pkl_path)
        except Exception as exc:
            print(
                f"[WARN] Could not load Lagrangian pkl for top-model summary: "
                f"{type(exc).__name__}: {exc}",
                flush=True,
            )
            pkl_path = None
            lag_map = {}

    generated_plots: List[Path] = []
    sol_paths: Dict[str, Path] = {}
    for i, row in enumerate(top_rows, 1):
        lag_id = str(row.get("lag_id"))
        sol_path = _find_top_solution_csv(i, lag_id)
        if sol_path is None:
            continue
        sol_paths[lag_id] = sol_path
        plot_path = OUTPUT_DIR / f"top_{i:02d}_lagrangian_{lag_id}_Hz_fit.png"
        _plot_top_model(i, row, sol_path, plot_path)
        generated_plots.append(plot_path)

    overlay_path = OUTPUT_DIR / f"top{top_n}_overlay_Hz_fit.png"
    _plot_top_overlay(top_rows, sol_paths, overlay_path)
    if overlay_path.exists():
        generated_plots.append(overlay_path)

    lines: List[str] = []
    lines.append("Top fitted Lagrangians: forms, initial conditions, and numerical-fit parameters (v5.0)")
    lines.append("=" * 92)
    lines.append("")
    lines.append(f"Base output directory: {BASE_OUTPUT_DIR}")
    lines.append(f"Run output directory: {OUTPUT_DIR}")
    lines.append(f"Lagrangian pkl: {pkl_path if pkl_path is not None else '[not found]'}")
    lines.append(f"Ranking source: {OUTPUT_DIR / 'model_ranking.csv'}")
    lines.append("")
    lines.append("Numerical convention")
    lines.append("- Independent variable: x = ln(a) = -ln(1+z).")
    lines.append("- Dimensionless Hubble: h(x) = H(x) / H0.")
    lines.append("- Scalar 1: varphi1(x) = phi1(x) / Mp;  q1 = d varphi1 / dx.")
    lines.append("- Scalar 2: varphi2(x) = phi2(x) / Lambda;  q2 = d varphi2 / dx.")
    lines.append("- Masses: mu1 = m1/H0, mu2 = m2/Lambda.")
    lines.append("- Decay constants: fbar1 = f1/Mp, fbar2 = f2/Lambda.")
    lines.append("- EFT cutoff ratio: lambda_H = Lambda / H0.")
    lines.append("- a0 = 1, h0 = 1.  q1_0 solved from E_N(x=0)=0 (or q2_0 for phi2-only models).")
    lines.append("- Mp = 2.435e27 eV (physical reduced Planck mass).")
    lines.append("- Physical Lambda [eV] = lambda_H * H0 [eV].")
    lines.append("")

    standard_cols = {
        "lag_id", "success", "reason", "chi2", "chi2_per_point", "AIC", "BIC",
        "chi2_hz", "chi2_sn", "chi2_bao", "sn_offset_hat", "bao_alpha_hat", "N_SN", "N_BAO",
        "k_params", "max_abs_constraint", "H0_km_s_Mpc", "Omega_m0", "rho_bar",
        "mu1_m1_over_H0", "mu2_m2_over_Lambda",
        "fbar1_f1_over_Mp", "fbar2_f2_over_Lambda",
        "varphi1_0_phi1_over_Mp", "varphi2_0_phi2_over_Lambda",
        "q1_0_dvarphi1_dln_a", "q2_0_dvarphi2_dln_a",
        "eps_HM_H0_over_Mp", "lambda_H_Lambda_over_H0", "Lambda_eV",
    }

    for i, row in enumerate(top_rows, 1):
        lag_id = str(row.get("lag_id"))
        H0 = _float_from_row(row, "H0_km_s_Mpc")
        H0_eV = H0 * KM_S_MPC_TO_EV if np.isfinite(H0) else np.nan

        lines.append("")
        lines.append("=" * 92)
        lines.append(f"Rank {i}: Lagrangian #{lag_id}")
        lines.append("=" * 92)
        lines.append("")
        lines.append("Raw Lagrangian from pkl")
        lines.append(_raw_lagrangian_string(lag_map, lag_id) if lag_map else "[pkl not found]")
        terms = _raw_terms_string(lag_map, lag_id) if lag_map else ""
        if terms:
            lines.append("")
            lines.append("Raw terms")
            lines.append(terms)
        lines.append("")
        lines.append("Fit metrics")
        lines.append(f"  chi2            = {_fmt(_float_from_row(row, 'chi2'))}")
        lines.append(f"  chi2 per point  = {_fmt(_float_from_row(row, 'chi2_per_point'))}")
        lines.append(f"  AIC             = {_fmt(_float_from_row(row, 'AIC'))}")
        lines.append(f"  BIC             = {_fmt(_float_from_row(row, 'BIC'))}")
        lines.append(f"  k_params        = {_fmt(_float_from_row(row, 'k_params'), 0)}")
        lines.append(f"  max |E_N|       = {_fmt(_float_from_row(row, 'max_abs_constraint'))}")
        lines.append("")
        lines.append("Initial conditions and sampled values")
        lines.append(f"  H0 [km/s/Mpc]            = {_fmt(H0)}")
        lines.append(f"  H0 [eV]                  = {_fmt(H0_eV)}")
        lines.append(f"  eps_HM = H0/Mp            = {_fmt(_float_from_row(row, 'eps_HM_H0_over_Mp'))}")
        lines.append(f"  lambda_H = Lambda/H0      = {_fmt(_float_from_row(row, 'lambda_H_Lambda_over_H0'))}")
        lines.append(f"  Lambda [eV]               = {_fmt(_float_from_row(row, 'Lambda_eV'))}")
        lines.append(f"  Omega_m0                  = {_fmt(_float_from_row(row, 'Omega_m0'))}")
        lines.append(f"  rho_bar                   = {_fmt(_float_from_row(row, 'rho_bar'))}")

        v1_0 = _float_from_row(row, "varphi1_0_phi1_over_Mp")
        q1_0 = _float_from_row(row, "q1_0_dvarphi1_dln_a")
        mu1_v = _float_from_row(row, "mu1_m1_over_H0")
        fbar1_v = _float_from_row(row, "fbar1_f1_over_Mp")
        if np.isfinite(v1_0) and v1_0 != 0:
            lines.append(f"  varphi1_0 = phi1_0/Mp     = {_fmt(v1_0)}")
        if np.isfinite(q1_0) and q1_0 != 0:
            lines.append(f"  q1_0 = dvarphi1/dx|0      = {_fmt(q1_0)}")
        if np.isfinite(mu1_v) and mu1_v != 0:
            lines.append(f"  mu1 = m1/H0               = {_fmt(mu1_v)}")
        if np.isfinite(fbar1_v) and fbar1_v != 1.0:
            lines.append(f"  fbar1 = f1/Mp              = {_fmt(fbar1_v)}")

        v2_0 = _float_from_row(row, "varphi2_0_phi2_over_Lambda")
        q2_0 = _float_from_row(row, "q2_0_dvarphi2_dln_a")
        mu2_v = _float_from_row(row, "mu2_m2_over_Lambda")
        fbar2_v = _float_from_row(row, "fbar2_f2_over_Lambda")
        if np.isfinite(v2_0) and v2_0 != 0:
            lines.append(f"  varphi2_0 = phi2_0/Lambda = {_fmt(v2_0)}")
        if np.isfinite(q2_0) and q2_0 != 0:
            lines.append(f"  q2_0 = dvarphi2/dx|0      = {_fmt(q2_0)}")
        if np.isfinite(mu2_v) and mu2_v != 0:
            lines.append(f"  mu2 = m2/Lambda           = {_fmt(mu2_v)}")
        if np.isfinite(fbar2_v) and fbar2_v != 1.0:
            lines.append(f"  fbar2 = f2/Lambda          = {_fmt(fbar2_v)}")

        extra = []
        for k, v in row.items():
            if k in standard_cols or k.startswith("Unnamed"):
                continue
            try:
                vv = float(v)
                if np.isfinite(vv):
                    extra.append((k, vv))
            except Exception:
                pass
        if extra:
            lines.append("")
            lines.append("Free coupling values")
            for k, vv in sorted(extra):
                lines.append(f"  {k:<16} = {_fmt(vv)}")
        lines.append("")
        lines.append("Numerical solution file")
        lines.append(f"  {sol_paths.get(lag_id, '[not found]')}")

    lines.append("")
    lines.append("=" * 92)
    lines.append("Generated plots")
    lines.append("=" * 92)
    for p in generated_plots:
        lines.append(f"  {p}")
    lines.append("")

    report_path = OUTPUT_DIR / f"top{top_n}_lagrangians_initial_conditions.txt"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    selected_csv = OUTPUT_DIR / f"top{top_n}_selected_models.csv"
    with open(selected_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in top_rows:
            writer.writerow(row)

    print(f"\nTop-{top_n} summary written to: {report_path}")
    print(f"Top-{top_n} table written to:   {selected_csv}")
    for p in generated_plots:
        print(f"Top-{top_n} plot written to:    {p}")

