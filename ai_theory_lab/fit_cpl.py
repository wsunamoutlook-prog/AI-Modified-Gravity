#!/usr/bin/env python3
"""Flat CPL best-fit baseline on REAL observations; no theory search or mock data.

Run as python -m ai_theory_lab.fit_cpl --output-dir output/cpl. Inputs are read-only.
The Solver likelihood supplies data loading and the reference-grid fit.
Independent interval Gauss--Legendre quadrature checks numerical integration.
"""
from __future__ import annotations

import os
for _name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_name] = "1"

import csv
import hashlib
import argparse
import json
import math
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
from scipy.linalg import cho_solve
from scipy.optimize import differential_evolution, minimize, minimize_scalar

ROOT = Path(__file__).resolve().parents[1]
OUT = None
from solver_v5_2 import likelihood as lk

DATA_PATHS = [
    ROOT / "data/SN data/DES-Dovekie_HD.csv",
    ROOT / "data/SN data/STAT+SYS.npz",
    ROOT / "data/BAO data/desi_gaussian_bao_ALL_GCcomb_mean.txt",
    ROOT / "data/BAO data/desi_gaussian_bao_ALL_GCcomb_cov.txt",
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")


def write_csv(name, rows):
    with (OUT / name).open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def hubble(z, theta):
    om, w0, wa = theta
    z = np.asarray(z)
    log_rho_de = 3.0 * (1.0 + w0 + wa) * np.log1p(z) - 3.0 * wa * z / (1.0 + z)
    return np.sqrt(om * (1.0 + z) ** 3 + (1.0 - om) * np.exp(log_rho_de))


class Fit:
    def __init__(self):
        self.sn, self.bao = lk.sanity_check_data_loaders(ROOT / "data/SN data", ROOT / "data/BAO data")
        self.n = len(self.sn["mu"]) + len(self.bao["value"])
        assert self.n == 1833
        self.zmax = max(max(self.sn["zHD"]), max(self.bao["z"]))
        self.grids = {}
        self.knots = np.unique(np.r_[0.0, self.sn["zHD"], self.bao["z"]])
        self.sn_indices = np.searchsorted(self.knots, self.sn["zHD"])
        self.bao_indices = np.searchsorted(self.knots, self.bao["z"])
        self.quad_cache = {}
        self.calls = 0

    def grid(self, theta, size=12000, H0=70.0):
        self.calls += 1
        if size not in self.grids:
            self.grids[size] = np.linspace(0.0, self.zmax * 1.001, size)
        z = self.grids[size]
        h = hubble(z, theta)
        cs, offset = lk.chi2_des_sn_from_grid(self.sn, z, h, H0)
        cb, alpha = lk.chi2_desi_bao_from_grid(self.bao, z, h)
        return dict(chi2=cs + cb, chi2_sn=cs, chi2_bao=cb, sn_offset_hat=offset, bao_alpha_hat=alpha)

    def integrals(self, theta, order):
        if order not in self.quad_cache:
            x, w = leggauss(order)
            half = np.diff(self.knots) * 0.5
            mid = (self.knots[1:] + self.knots[:-1]) * 0.5
            self.quad_cache[order] = (mid[:, None] + half[:, None] * x, half[:, None] * w)
        z, weights = self.quad_cache[order]
        return np.r_[0.0, np.cumsum(np.sum(weights / hubble(z, theta), axis=1))]

    def exact(self, theta, order=8, H0=70.0):
        """Same Gaussian likelihood/profiles, independent accurate distance integral."""
        self.calls += 1
        integ = self.integrals(theta, order)
        dl = (1.0 + self.sn["zHEL"]) * lk.C_LIGHT / H0 * integ[self.sn_indices]
        mu = 5 * np.log10(dl) + 25
        residual = self.sn["mu"] - mu
        # Residual form avoids subtracting large chi-square terms after profiling.
        offset = float(self.sn["Cinv_one"] @ residual / self.sn["one_Cinv_one"])
        residual -= offset
        cs = float(residual @ lk._apply_precision(self.sn, residual))
        z = self.bao["z"]
        I = integ[self.bao_indices]
        h = hubble(z, theta)
        q = self.bao["quantity"]
        p = np.where(q == "DM_over_rs", I, np.where(q == "DH_over_rs", 1/h, (z*I**2/h)**(1/3)))
        pinv = cho_solve(self.bao["cho"], p, check_finite=False)
        alpha = float(pinv @ self.bao["value"] / (p @ pinv))
        r = self.bao["value"] - alpha * p
        cb = float(r @ cho_solve(self.bao["cho"], r, check_finite=False))
        return dict(chi2=cs + cb, chi2_sn=cs, chi2_bao=cb, sn_offset_hat=offset, bao_alpha_hat=alpha)

    def record(self, theta, method="exact", size=12000, k=5):
        out = (self.exact(theta) if method == "exact" else self.grid(theta, size))
        out.update(Omega_m0=float(theta[0]), w0=float(theta[1]), wa=float(theta[2]), H0_convention=70.0,
                   k=k, AIC=out["chi2"] + 2*k, BIC=out["chi2"] + k*np.log(self.n), N=self.n)
        return out


def main(argv=None):
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="New directory for fit results; existing directories are refused.")
    args = parser.parse_args(argv)
    OUT = args.output_dir.expanduser().resolve()
    OUT.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    input_hashes = {str(p.relative_to(ROOT)): digest(p) for p in DATA_PATHS}
    fit = Fit()
    print("REAL OBSERVATIONS: flat CPL baseline, no LLM calls, no mock data.", flush=True)
    print("Reproducing the original 551-point LCDM scan ...", flush=True)
    om_grid = np.linspace(0.05, 0.60, 551)
    hist = min((fit.record((om, -1, 0), "grid", 3000, 3) for om in om_grid), key=lambda r:r["chi2"])
    print("Historical LCDM grid:", json.dumps(hist), flush=True)
    assert abs(hist["Omega_m0"] - 0.306) < 1e-12
    assert abs(hist["chi2"] - 1645.28) < 0.01
    save_json("historical_lcdm_reproduction.json", hist)

    objective = lambda x: fit.grid(x)["chi2"]
    bounds = [(0.05, 0.60), (-3.0, 1.0), (-10.0, 10.0)]
    trials = []

    def run_de(seed, search_bounds, label):
        t = time.monotonic()
        result = differential_evolution(objective, search_bounds, seed=seed,
            popsize=15, maxiter=240, tol=1e-10, atol=1e-8, polish=False, workers=1)
        polished = minimize(objective, result.x, method="Nelder-Mead",
            bounds=search_bounds, options=dict(maxiter=2500, xatol=2e-9, fatol=1e-9))
        best = polished if polished.fun <= result.fun else result
        row = dict(label=label, seed=seed, bounds=search_bounds,
            x=best.x.tolist(), chi2=float(best.fun), de_success=bool(result.success),
            de_message=str(result.message), local_success=bool(polished.success),
            evaluations=int(result.nfev + polished.nfev), seconds=time.monotonic()-t)
        trials.append(row)
        save_json("optimizer_trials.json", trials)
        print("CPL search:", json.dumps(row), flush=True)
        return best

    best_runs = [run_de(seed, bounds, f"standard_bounds_seed_{seed}") for seed in (20261009, 817)]
    # Deliberate parameter-bound check, separate from all theory-search priors.
    wide_bounds = [(0.001, 0.999), (-5.0, 2.0), (-30.0, 20.0)]
    best_runs.append(run_de(931, wide_bounds, "wider_bounds_check"))
    grid_best = min(best_runs, key=lambda r:r.fun)
    exact_obj = lambda x: fit.exact(x)["chi2"]
    precise = minimize(exact_obj, grid_best.x, method="Nelder-Mead", bounds=wide_bounds,
        options=dict(maxiter=3000, xatol=5e-10, fatol=1e-10))
    assert precise.success, precise.message
    cpl = fit.record(precise.x)
    lcdm_opt = minimize_scalar(lambda om: fit.exact((om, -1, 0))["chi2"],
        bounds=(0.001, 0.999), method="bounded", options={"xatol":1e-12})
    assert lcdm_opt.success
    lcdm = fit.record((lcdm_opt.x, -1.0, 0.0), k=3)
    assert cpl["chi2"] <= lcdm["chi2"] + 1e-7
    print("Precise LCDM:", json.dumps(lcdm), flush=True)
    print("Precise CPL:", json.dumps(cpl), flush=True)

    # Check local optimization from contrasting starts with independent integrals.
    locals_out = []
    for initial in ((0.306,-1,0), (0.3,-0.5,-2), (0.1,-2,3), (0.5,-1,-5)):
        res = minimize(exact_obj, initial, method="Nelder-Mead", bounds=wide_bounds,
            options=dict(maxiter=4000, xatol=1e-8, fatol=1e-9))
        locals_out.append(dict(initial=list(initial), x=res.x.tolist(), chi2=float(res.fun),
                               success=bool(res.success), nfev=int(res.nfev)))
    save_json("independent_integral_multistart.json", locals_out)
    assert all(r["chi2"] >= cpl["chi2"] - 1e-6 for r in locals_out)

    convergence = []
    checks = {}
    for label, theta, record in (("CPL", precise.x, cpl), ("LCDM", (lcdm_opt.x,-1,0), lcdm)):
        for ngrid in (3000, 6000, 12000, 24000, 48000, 96000):
            r = fit.grid(theta, ngrid)
            convergence.append(dict(model=label, method="Solver_trapezoid_grid", size=ngrid,
                chi2=r["chi2"], difference_from_precise=r["chi2"]-record["chi2"]))
        for order in (4, 8, 16):
            r = fit.exact(theta, order)
            convergence.append(dict(model=label, method="interval_Gauss_Legendre", size=order,
                chi2=r["chi2"], difference_from_precise=r["chi2"]-record["chi2"]))
        I = fit.integrals(theta,16)
        check_indices = np.unique(np.linspace(1,len(fit.knots)-1,25,dtype=int))
        q_errors = [abs(quad(lambda z:1/float(hubble(z,theta)), 0, fit.knots[i],
                     epsabs=1e-12,epsrel=1e-12)[0]-I[i]) for i in check_indices]
        checks[label+"_quad_max_abs_distance_difference"] = max(q_errors)
        checks[label+"_H0_chi2_invariance_max_difference"] = max(
            abs(fit.exact(theta,H0=h0)["chi2"]-record["chi2"]) for h0 in (58.,70.,74.))
    write_csv("integration_convergence.csv", convergence)
    checks["LCDM_limit_h_max_absolute_error"] = float(np.max(np.abs(
        hubble(fit.knots,(0.306,-1,0))-np.sqrt(0.306*(1+fit.knots)**3+0.694))))
    checks["all_input_hashes_unchanged"] = all(digest(p)==input_hashes[str(p.relative_to(ROOT))] for p in DATA_PATHS)
    checks["broad_search_minima_chi2_spread"] = float(np.ptp([r.fun for r in best_runs]))
    checks["best_CPL_bound_distances"] = [min(float(x-lo),float(hi-x)) for x,(lo,hi) in zip(precise.x,wide_bounds)]
    checks["best_CPL_inside_original_bounds"] = all(lo<x<hi for x,(lo,hi) in zip(precise.x,bounds))
    checks["noiseless_distance_quadrature_order_max_chi2_difference"] = max(abs(r["difference_from_precise"])
        for r in convergence if r["method"]=="interval_Gauss_Legendre")
    checks["96000_grid_max_chi2_difference"] = max(abs(r["difference_from_precise"])
        for r in convergence if r["method"]=="Solver_trapezoid_grid" and r["size"]==96000)
    assert checks["all_input_hashes_unchanged"]
    assert checks["noiseless_distance_quadrature_order_max_chi2_difference"] < 1e-6
    assert checks["96000_grid_max_chi2_difference"] < 1e-4
    assert checks["broad_search_minima_chi2_spread"] < 1e-4
    for label in ("CPL", "LCDM"):
        assert checks[label+"_quad_max_abs_distance_difference"] < 1e-9
        assert checks[label+"_H0_chi2_invariance_max_difference"] < 1e-6
    save_json("checks.json",checks)

    rows = []
    for label, r in (("LCDM_continuous_refit",lcdm),("CPL_continuous_refit",cpl)):
        rows.append(dict(model=label,**r,delta_chi2=r["chi2"]-lcdm["chi2"],
                         delta_AIC=r["AIC"]-lcdm["AIC"],delta_BIC=r["BIC"]-lcdm["BIC"]))
    write_csv("best_fits.csv",rows)
    output = dict(dataset_kind="REAL_OBSERVATIONS", is_mock=False,
        created_utc=datetime.now(timezone.utc).isoformat(),
        description="Flat CPL phenomenological background fit, with fixed data covariance and profiled SN offset and BAO scale. No grammar, LLM, or theory search.",
        definitions=dict(w="w0 + wa*z/(1+z)", h2="Om*(1+z)^3 + (1-Om)*(1+z)^(3*(1+w0+wa))*exp(-3*wa*z/(1+z))",
            H0="70 km/s/Mpc fixed as a distance-scale convention, not inferred", radiation="omitted, matching the late-time LCDM reference", flat=True,
            covariance="Full within-dataset covariance, independent SN and BAO blocks", likelihood="Profile Gaussian chi-square, not marginalized evidence",
            CPL_parameters=["Omega_m0","w0","wa","profiled_SN_offset","profiled_BAO_scale"],
            uncertainty="Best-fit points only; no confidence or credible intervals computed"),
        standard_bounds=bounds, wider_bounds=wide_bounds,
        historical_grid_reference=hist, continuous_refits=rows,
        CPL_at_grid_optimized_point=fit.record(grid_best.x,"grid",12000),
        comparisons_to_paper=dict(reference_chi2=1645.28, reference_AIC=1651.28,
            CPL_delta_chi2=cpl["chi2"]-1645.28,CPL_delta_AIC=cpl["AIC"]-1651.28,
            quadratic_quintessence_recorded_chi2=1637.9518,quadratic_quintessence_recorded_AIC=1647.9518,
            CPL_minus_recorded_quintessence_AIC=cpl["AIC"]-1647.9518),
        checks=checks, input_sha256=input_hashes,
        source_sha256={str(p.relative_to(ROOT)):digest(p) for p in [Path(__file__),Path(lk.__file__)]},
        software=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()),
        likelihood_calls=fit.calls, elapsed_seconds=time.monotonic()-start)
    save_json("result.json",output)
    z = np.linspace(0,fit.zmax,500)
    write_csv("best_fit_backgrounds.csv",[dict(z=float(zi),w_CPL=float(precise.x[1]+precise.x[2]*zi/(1+zi)),
        h_CPL=float(hubble(zi,precise.x)),h_LCDM=float(hubble(zi,(lcdm_opt.x,-1,0)))) for zi in z])
    print("COMPLETE: all verification checks passed; saved",OUT,"elapsed",output["elapsed_seconds"],flush=True)


if __name__ == "__main__":
    main()
