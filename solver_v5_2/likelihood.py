#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DES-SN and DESI-DR2 BAO data loading plus likelihood helpers for Solver v5.2."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.linalg import cho_factor, cho_solve

C_LIGHT = 299792.458  # km/s

# =============================================================================
# DES-SN + DESI-DR2 data loaders
# =============================================================================


def mu_model_from_h_grid(zHD, zHEL, z_grid, h_grid, H0_km_s_Mpc):
    zHD = np.asarray(zHD, dtype=float)
    zHEL = np.asarray(zHEL, dtype=float)
    z_grid = np.asarray(z_grid, dtype=float)
    h_grid = np.asarray(h_grid, dtype=float)
    if H0_km_s_Mpc <= 0 or not np.isfinite(H0_km_s_Mpc):
        raise ValueError("H0_km_s_Mpc must be positive and finite.")
    if not (np.all(np.isfinite(zHD)) and np.all(np.isfinite(zHEL))):
        raise ValueError("SN redshifts contain non-finite values.")
    if z_grid.shape != h_grid.shape:
        raise ValueError("z_grid and h_grid must have matching shapes.")
    if not (np.all(np.isfinite(z_grid)) and np.all(np.isfinite(h_grid))):
        raise ValueError("z_grid or h_grid contains non-finite values.")
    if np.any(h_grid <= 0):
        raise ValueError("h_grid must be positive for SN luminosity distances.")

    order = np.argsort(z_grid)
    z_sorted = z_grid[order]
    h_sorted = h_grid[order]
    unique_z, unique_idx = np.unique(z_sorted, return_index=True)
    z_sorted = unique_z
    h_sorted = h_sorted[unique_idx]
    if z_sorted[0] > 0.0:
        z_sorted = np.concatenate(([0.0], z_sorted))
        h_sorted = np.concatenate(([1.0], h_sorted))
    elif abs(z_sorted[0]) > 1e-12:
        raise ValueError("z_grid must not start above z=0 for SN integration.")
    else:
        z_sorted[0] = 0.0

    zmax = float(np.max(zHD))
    if zmax > float(z_sorted[-1]) + 1e-10:
        raise ValueError(
            f"SN zHD max {zmax:.12g} exceeds trajectory z max {float(z_sorted[-1]):.12g}."
        )
    integral_grid = cumulative_trapezoid(1.0 / h_sorted, z_sorted, initial=0.0)
    integral_at_sn = np.interp(zHD, z_sorted, integral_grid)
    d_l_mpc = (1.0 + zHEL) * (C_LIGHT / H0_km_s_Mpc) * integral_at_sn
    if np.any(d_l_mpc <= 0) or not np.all(np.isfinite(d_l_mpc)):
        raise ValueError("SN luminosity distance is non-positive or non-finite.")
    return 5.0 * np.log10(d_l_mpc) + 25.0


def _read_snana_like_table(path: Path) -> Dict[str, np.ndarray]:
    varnames = None
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.startswith("VARNAMES:"):
                varnames = s.split(":", 1)[1].split()
                continue
            if s.startswith("SN:"):
                if varnames is None:
                    raise ValueError(f"Found SN row before VARNAMES in {path}")
                vals = s.split(":", 1)[1].split()
                if len(vals) != len(varnames):
                    raise ValueError(
                        f"SN row has {len(vals)} values but {len(varnames)} columns in {path}: {s}"
                    )
                rows.append(vals)
    if varnames is None:
        raise ValueError(f"Missing VARNAMES line in {path}")
    if not rows:
        raise ValueError(f"No SN rows found in {path}")
    cols: Dict[str, List[str]] = {name: [] for name in varnames}
    for row in rows:
        for name, val in zip(varnames, row):
            cols[name].append(val)
    out: Dict[str, np.ndarray] = {}
    for name, vals in cols.items():
        try:
            out[name] = np.asarray(vals, dtype=float)
        except ValueError:
            out[name] = np.asarray(vals, dtype=str)
    return out


def _unpack_upper_triangle(vals: np.ndarray, n: int) -> np.ndarray:
    vals = np.asarray(vals, dtype=float).reshape(-1)
    expected = n * (n + 1) // 2
    if vals.size != expected:
        raise ValueError(f"Packed upper triangle has {vals.size} values; expected {expected} for n={n}.")
    mat = np.zeros((n, n), dtype=float)
    mat[np.triu_indices(n)] = vals
    lower = np.tril_indices(n, -1)
    mat[lower] = mat.T[lower]
    return mat


def load_des_sn(sn_dir: Path) -> dict:
    sn_dir = Path(sn_dir)
    data_path = sn_dir / "DES-Dovekie_HD.csv"
    cov_path = sn_dir / "STAT+SYS.npz"
    tab = _read_snana_like_table(data_path)
    required = {"zHD", "zHEL", "MU"}
    missing = sorted(required - set(tab.keys()))
    if missing:
        raise ValueError(f"Missing DES SN columns {missing}; available columns: {sorted(tab.keys())}")
    if "zHEL" not in tab:
        raise ValueError("DES SN zHEL column is required.")

    zHD = np.asarray(tab["zHD"], dtype=float)
    zHEL = np.asarray(tab["zHEL"], dtype=float)
    mu = np.asarray(tab["MU"], dtype=float)
    muerr = np.asarray(tab["MUERR"], dtype=float) if "MUERR" in tab else None
    if np.any(zHD <= 0.0):
        raise ValueError("DES SN contains non-positive zHD values; refusing to drop or reorder rows.")

    obj = np.load(cov_path, allow_pickle=False)
    print(f"[DES SN] npz files: {obj.files}", flush=True)
    for key in obj.files:
        print(f"[DES SN] npz key={key}, shape={np.shape(obj[key])}", flush=True)

    cov = None
    invcov = None
    cov_mode = None
    if "nsn" in obj.files and "cov" in obj.files:
        n_cov = int(np.asarray(obj["nsn"]).reshape(-1)[0])
        invcov = _unpack_upper_triangle(obj["cov"], n_cov)
        cov_mode = "invcov"
    elif "invcov" in obj.files:
        invcov = np.asarray(obj["invcov"], dtype=float)
        cov_mode = "invcov"
    elif "cov" in obj.files:
        cov = np.asarray(obj["cov"], dtype=float)
        cov_mode = "cov"
    else:
        raise ValueError(f"Could not identify DES SN covariance/invcov in {cov_path}; keys={obj.files}")

    n = len(mu)
    mat = invcov if invcov is not None else cov
    if mat.shape != (n, n):
        raise ValueError(f"DES SN {cov_mode} shape {mat.shape} does not match N_SN={n}")
    if not np.all(np.isfinite(mat)):
        raise ValueError(f"DES SN {cov_mode} contains non-finite values.")
    if not np.allclose(mat, mat.T, rtol=1e-8, atol=1e-10):
        raise ValueError(f"DES SN {cov_mode} is not symmetric.")

    one = np.ones(n, dtype=float)
    sn = {
        "zHD": zHD,
        "zHEL": zHEL,
        "mu": mu,
        "muerr": muerr,
        "cov": cov,
        "invcov": invcov,
        "cov_mode": cov_mode,
        "one": one,
    }
    if invcov is not None:
        Cinv_one = invcov @ one
        sn["Cinv_one"] = Cinv_one
        sn["one_Cinv_one"] = float(one @ Cinv_one)
    else:
        cho = cho_factor(cov, lower=True, check_finite=False)
        Cinv_one = cho_solve(cho, one, check_finite=False)
        sn["cho"] = cho
        sn["Cinv_one"] = Cinv_one
        sn["one_Cinv_one"] = float(one @ Cinv_one)

    print(
        f"[DES SN] N_SN={n}, zHD=[{float(np.min(zHD)):.6g}, {float(np.max(zHD)):.6g}], "
        f"zHEL=[{float(np.min(zHEL)):.6g}, {float(np.max(zHEL)):.6g}], "
        f"MU=[{float(np.min(mu)):.6g}, {float(np.max(mu)):.6g}]",
        flush=True,
    )
    if muerr is not None:
        print(
            f"[DES SN] MUERR sanity range=[{float(np.min(muerr)):.6g}, {float(np.max(muerr)):.6g}] "
            "(not used in chi2)",
            flush=True,
        )
    print(f"[DES SN] cov_mode={cov_mode}, matrix_shape={mat.shape}", flush=True)
    return sn


def load_desi_dr2_bao(bao_dir: Path) -> dict:
    bao_dir = Path(bao_dir)
    mean_path = bao_dir / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
    cov_path = bao_dir / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
    raw = np.loadtxt(mean_path, comments="#", dtype=str)
    z = raw[:, 0].astype(float)
    value = raw[:, 1].astype(float)
    quantity = raw[:, 2].astype(str)
    allowed = {"DV_over_rs", "DM_over_rs", "DH_over_rs"}
    bad = sorted(set(quantity) - allowed)
    if bad:
        raise ValueError(f"Unsupported DESI BAO quantities {bad}")
    cov = np.loadtxt(cov_path, dtype=float)
    if cov.shape != (13, 13):
        raise ValueError(f"DESI BAO covariance must be 13x13; got {cov.shape}")
    if cov.shape != (len(z), len(z)):
        raise ValueError(f"DESI BAO covariance shape {cov.shape} does not match N_BAO={len(z)}")
    if not np.all(np.isfinite(cov)):
        raise ValueError("DESI BAO covariance contains non-finite values.")
    if not np.allclose(cov, cov.T, rtol=1e-10, atol=1e-12):
        raise ValueError("DESI BAO covariance is not symmetric.")
    cho = cho_factor(cov, lower=True, check_finite=False)
    counts = Counter(quantity.tolist())
    print(
        f"[DESI BAO] N_BAO={len(z)}, z=[{float(np.min(z)):.6g}, {float(np.max(z)):.6g}], "
        f"quantity_counts={dict(counts)}, cov_shape={cov.shape}",
        flush=True,
    )
    return {
        "z": z,
        "value": value,
        "quantity": quantity,
        "cov": cov,
        "cho": cho,
        "one": np.ones(len(z), dtype=float),
    }


def sanity_check_data_loaders(sn_dir: Path, bao_dir: Path) -> Tuple[dict, dict]:
    sn = load_des_sn(sn_dir)
    bao = load_desi_dr2_bao(bao_dir)
    sn_mat = sn["invcov"] if sn["invcov"] is not None else sn["cov"]
    print("[DATA CHECK] DES SN loaded successfully.", flush=True)
    print("[DATA CHECK] DESI DR2 BAO loaded successfully.", flush=True)
    print(f"[DATA CHECK] SN cov_mode={sn['cov_mode']}, matrix_shape={sn_mat.shape}", flush=True)
    print(f"[DATA CHECK] BAO covariance shape={bao['cov'].shape}", flush=True)
    print(f"[DATA CHECK] BAO quantity counts={dict(Counter(bao['quantity'].tolist()))}", flush=True)
    return sn, bao


def _apply_precision(obj: dict, vec: np.ndarray) -> np.ndarray:
    vec = np.asarray(vec, dtype=float)
    if obj.get("invcov") is not None:
        return obj["invcov"] @ vec
    return cho_solve(obj["cho"], vec, check_finite=False)


def chi2_des_sn_from_grid(sn, z_grid, h_grid, H0_km_s_Mpc):
    mu_th = mu_model_from_h_grid(
        sn["zHD"], sn["zHEL"], z_grid, h_grid, H0_km_s_Mpc
    )
    r = sn["mu"] - mu_th
    Cinv_r = _apply_precision(sn, r)
    chi0 = float(r @ Cinv_r)
    B = float(sn["one"] @ Cinv_r)
    A = float(sn["one_Cinv_one"])
    M_SN_hat = B / A
    chi2_sn = chi0 - (B * B) / A
    return float(chi2_sn), float(M_SN_hat)


def chi2_desi_bao_from_grid(bao, z_grid, h_grid):
    z_grid = np.asarray(z_grid, dtype=float)
    h_grid = np.asarray(h_grid, dtype=float)
    if z_grid.shape != h_grid.shape:
        raise ValueError("BAO z_grid and h_grid must have matching shapes.")
    if not (np.all(np.isfinite(z_grid)) and np.all(np.isfinite(h_grid))):
        raise ValueError("BAO z_grid or h_grid contains non-finite values.")
    if np.any(h_grid <= 0):
        raise ValueError("BAO h_grid must be positive.")

    order = np.argsort(z_grid)
    z_sorted = z_grid[order]
    h_sorted = h_grid[order]
    unique_z, unique_idx = np.unique(z_sorted, return_index=True)
    z_sorted = unique_z
    h_sorted = h_sorted[unique_idx]
    if z_sorted[0] > 0.0:
        z_sorted = np.concatenate(([0.0], z_sorted))
        h_sorted = np.concatenate(([1.0], h_sorted))
    elif abs(z_sorted[0]) > 1e-12:
        raise ValueError("BAO z_grid must not start above z=0.")
    else:
        z_sorted[0] = 0.0

    z_bao = np.asarray(bao["z"], dtype=float)
    if float(np.max(z_bao)) > float(z_sorted[-1]) + 1e-10:
        raise ValueError(
            f"BAO z max {float(np.max(z_bao)):.12g} exceeds trajectory z max {float(z_sorted[-1]):.12g}."
        )
    integral_grid = cumulative_trapezoid(1.0 / h_sorted, z_sorted, initial=0.0)
    I = np.interp(z_bao, z_sorted, integral_grid)
    h_at_bao = np.interp(z_bao, z_sorted, h_sorted)

    p = np.empty_like(z_bao, dtype=float)
    q = np.asarray(bao["quantity"], dtype=str)
    p[q == "DM_over_rs"] = I[q == "DM_over_rs"]
    p[q == "DH_over_rs"] = 1.0 / h_at_bao[q == "DH_over_rs"]
    dv_mask = q == "DV_over_rs"
    p[dv_mask] = (z_bao[dv_mask] * I[dv_mask] ** 2 / h_at_bao[dv_mask]) ** (1.0 / 3.0)
    if not np.all(np.isfinite(p)) or np.any(p <= 0):
        raise ValueError("BAO shape prediction contains non-finite or non-positive values.")

    d = np.asarray(bao["value"], dtype=float)
    Cinv_p = cho_solve(bao["cho"], p, check_finite=False)
    Cinv_d = cho_solve(bao["cho"], d, check_finite=False)
    denom = float(p @ Cinv_p)
    if not np.isfinite(denom) or denom <= 0:
        raise ValueError("Invalid p^T C^{-1} p for DESI BAO.")
    alpha_hat = float((p @ Cinv_d) / denom)
    if not np.isfinite(alpha_hat) or alpha_hat <= 0:
        raise ValueError(f"Invalid DESI BAO alpha_hat={alpha_hat}.")
    r = d - alpha_hat * p
    Cinv_r = cho_solve(bao["cho"], r, check_finite=False)
    chi2_bao = float(r @ Cinv_r)
    return float(chi2_bao), float(alpha_hat)


def sanity_check_lcdm_new_data(sn_data, bao_data):
    H0 = 70.0
    Omega_m0 = 0.3
    zmax = max(float(np.max(sn_data["zHD"])), float(np.max(bao_data["z"])))
    z_grid = np.linspace(0.0, zmax * 1.001, 3000)
    h_grid = np.sqrt(Omega_m0 * (1.0 + z_grid) ** 3 + 1.0 - Omega_m0)
    chi2_sn, M_SN_hat = chi2_des_sn_from_grid(sn_data, z_grid, h_grid, H0)
    chi2_bao, alpha_BAO_hat = chi2_desi_bao_from_grid(bao_data, z_grid, h_grid)
    print(
        f"[LCDM sanity] chi2_DES_SN={chi2_sn:.6g}, "
        f"chi2_DES_SN/N_SN={chi2_sn/len(sn_data['mu']):.6g}, M_SN_hat={M_SN_hat:.6g}",
        flush=True,
    )
    print(
        f"[LCDM sanity] chi2_DESI_BAO={chi2_bao:.6g}, "
        f"chi2_DESI_BAO/N_BAO={chi2_bao/len(bao_data['value']):.6g}, "
        f"alpha_BAO_hat={alpha_BAO_hat:.6g}",
        flush=True,
    )
    if not (5.0 < alpha_BAO_hat < 100.0):
        raise ValueError(
            f"DESI BAO alpha_BAO_hat={alpha_BAO_hat:.6g} is outside expected order-of-magnitude."
        )
    if abs(M_SN_hat) > 5.0:
        raise ValueError(
            f"DES SN M_SN_hat={M_SN_hat:.6g} is unexpectedly large for distance-modulus data."
        )
    return {
        "chi2_sn": chi2_sn,
        "M_SN_hat": M_SN_hat,
        "chi2_bao": chi2_bao,
        "alpha_BAO_hat": alpha_BAO_hat,
    }


def load_current_likelihood_data(sn_dir: Path, bao_dir: Path) -> Tuple[dict, dict]:
    sn_data, bao_data = sanity_check_data_loaders(sn_dir, bao_dir)
    sanity_check_lcdm_new_data(sn_data, bao_data)
    return sn_data, bao_data

