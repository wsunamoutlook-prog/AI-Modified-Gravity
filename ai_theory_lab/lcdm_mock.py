"""Generate one explicitly labelled flat-LCDM synthetic likelihood data set.

This module does not propose theories or modify observed data. The existing
Solver loaders, nuisance profiling and LCDM reference fit remain authoritative.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import inspect
import json
import os
from pathlib import Path
import shutil
from typing import Any

import numpy as np
import scipy
from scipy.integrate import cumulative_trapezoid
from scipy.linalg import solve_triangular

from solver_v5_2.likelihood import (
    chi2_des_sn_from_grid,
    chi2_desi_bao_from_grid,
    load_des_sn,
    load_desi_dr2_bao,
    mu_model_from_h_grid,
)

DATASET_KIND = "MOCK_SYNTHETIC"
DEFAULT_SEED = 20260908
SN_TABLE = "DES-Dovekie_HD.csv"
SN_COV = "STAT+SYS.npz"
BAO_TABLE = "desi_gaussian_bao_ALL_GCcomb_mean.txt"
BAO_COV = "desi_gaussian_bao_ALL_GCcomb_cov.txt"
MOCK_HEADER = "# MOCK / SYNTHETIC — generated flat-LCDM data; NOT real observations.\n"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def gaussian_noise(matrix: np.ndarray, whitened: np.ndarray, *, precision: bool) -> np.ndarray:
    """Transform standard normals using a full covariance or full precision.

    If P = L L.T is precision, L^{-T} z has covariance P^{-1}.
    L^{-1} z would be incorrect for a correlated, non-diagonal matrix.
    Matrix right-hand sides are supported for exact transform tests.
    """
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Gaussian covariance/precision must be square.")
    if not np.all(np.isfinite(matrix)) or not np.allclose(matrix, matrix.T, rtol=1e-10, atol=1e-12):
        raise ValueError("Gaussian covariance/precision must be finite and symmetric.")
    factor = np.linalg.cholesky(matrix)
    z = np.asarray(whitened, dtype=float)
    if z.shape[0] != matrix.shape[0] or not np.all(np.isfinite(z)):
        raise ValueError("Whitened Gaussian dimensions or values are invalid.")
    if precision:
        return solve_triangular(factor.T, z, lower=False, check_finite=False)
    return factor @ z


def bao_shape_from_grid(bao: dict, z_grid: np.ndarray, h_grid: np.ndarray) -> np.ndarray:
    """Unscaled BAO shape, matching chi2_desi_bao_from_grid exactly.

    The existing likelihood does not export this vector. Its integration,
    interpolation and DV convention are repeated here and parity-tested.
    """
    z_grid = np.asarray(z_grid, dtype=float)
    h_grid = np.asarray(h_grid, dtype=float)
    if z_grid.shape != h_grid.shape or z_grid.ndim != 1 or not len(z_grid):
        raise ValueError("BAO z_grid and h_grid must be matching nonempty vectors.")
    if not (np.all(np.isfinite(z_grid)) and np.all(np.isfinite(h_grid))) or np.any(h_grid <= 0):
        raise ValueError("BAO grid must be finite with positive h.")
    order = np.argsort(z_grid)
    z_sorted, h_sorted = z_grid[order], h_grid[order]
    z_sorted, unique_idx = np.unique(z_sorted, return_index=True)
    h_sorted = h_sorted[unique_idx]
    if z_sorted[0] > 0.0:
        z_sorted = np.concatenate(([0.0], z_sorted))
        h_sorted = np.concatenate(([1.0], h_sorted))
    elif abs(z_sorted[0]) > 1e-12:
        raise ValueError("BAO grid must start at z=0.")
    else:
        z_sorted[0] = 0.0
    z_bao = np.asarray(bao["z"], dtype=float)
    if float(np.max(z_bao)) > float(z_sorted[-1]) + 1e-10:
        raise ValueError("BAO redshift exceeds the prediction grid.")
    integral_grid = cumulative_trapezoid(1.0 / h_sorted, z_sorted, initial=0.0)
    integral = np.interp(z_bao, z_sorted, integral_grid)
    h_at_bao = np.interp(z_bao, z_sorted, h_sorted)
    q = np.asarray(bao["quantity"], dtype=str)
    if not set(q) <= {"DM_over_rs", "DH_over_rs", "DV_over_rs"}:
        raise ValueError("Unsupported BAO quantity.")
    prediction = np.empty_like(z_bao, dtype=float)
    prediction[q == "DM_over_rs"] = integral[q == "DM_over_rs"]
    prediction[q == "DH_over_rs"] = 1.0 / h_at_bao[q == "DH_over_rs"]
    dv = q == "DV_over_rs"
    prediction[dv] = (z_bao[dv] * integral[dv] ** 2 / h_at_bao[dv]) ** (1.0 / 3.0)
    if not np.all(np.isfinite(prediction)) or np.any(prediction <= 0):
        raise ValueError("Invalid BAO shape prediction.")
    return prediction


def write_sn_mock_table(source: Path, target: Path, values: np.ndarray) -> None:
    """Keep source row order and metadata, replacing only the MU column."""
    lines = [MOCK_HEADER]
    mu_index = None
    row_index = 0
    for line in source.read_text(encoding="utf-8").splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("VARNAMES:"):
            mu_index = stripped.split(":", 1)[1].split().index("MU")
        if stripped.startswith("SN:"):
            if mu_index is None or row_index >= len(values):
                raise ValueError("SN row count or column header does not match loaded observations.")
            fields = stripped.split(":", 1)[1].split()
            fields[mu_index] = format(float(values[row_index]), ".17g")
            lines.append("SN: " + " ".join(fields) + "\n")
            row_index += 1
        else:
            lines.append(line)
    if row_index != len(values):
        raise ValueError("SN row count does not match generated data.")
    with target.open("x", encoding="utf-8") as stream:
        stream.write("".join(lines))


def write_bao_mock_table(source: Path, target: Path, values: np.ndarray) -> None:
    """Keep BAO redshift, quantity and row order, replacing only values."""
    lines = [MOCK_HEADER]
    row_index = 0
    for line in source.read_text(encoding="utf-8").splitlines(keepends=True):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            lines.append(line)
            continue
        fields = stripped.split()
        if len(fields) != 3 or row_index >= len(values):
            raise ValueError("BAO table format or row count does not match loaded observations.")
        fields[1] = format(float(values[row_index]), ".17g")
        lines.append(" ".join(fields) + "\n")
        row_index += 1
    if row_index != len(values):
        raise ValueError("BAO row count does not match generated data.")
    with target.open("x", encoding="utf-8") as stream:
        stream.write("".join(lines))


def _validate_destination(sn_dir: Path, bao_dir: Path, output_dir: Path) -> tuple[Path, Path, Path]:
    sn_dir, bao_dir = sn_dir.resolve(strict=True), bao_dir.resolve(strict=True)
    output_dir = output_dir.resolve()
    if not output_dir.name.startswith("MOCK_"):
        raise ValueError("Output directory basename must start with MOCK_.")
    if output_dir.exists():
        raise FileExistsError(f"Refusing to overwrite existing directory: {output_dir}")
    for source in (sn_dir, bao_dir):
        if output_dir == source or output_dir in source.parents or source in output_dir.parents:
            raise ValueError("Mock destination must be disjoint from both real input directories.")
        manifest = source / "manifest.json"
        if manifest.exists() and json.loads(manifest.read_text()).get("is_real_observation") is False:
            raise ValueError("Mock generation requires original observed input data, not another mock.")
    return sn_dir, bao_dir, output_dir


def _write_json(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


@contextmanager
def _private_lcdm_cache(directory: Path):
    """Isolate the unchanged reference fitter's only filesystem side effect."""
    keys = ("SOLVER_LCDM_CACHE", "SOLVER_LCDM_CACHE_DIR")
    saved = {key: os.environ.get(key) for key in keys}
    os.environ.update(SOLVER_LCDM_CACHE="1", SOLVER_LCDM_CACHE_DIR=str(directory))
    try:
        yield
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def generate_mock(sn_dir: Path, bao_dir: Path, output_dir: Path, *, seed: int = DEFAULT_SEED) -> dict[str, Any]:
    """Generate and verify one mock; fail rather than overwrite any data set."""
    from solver_v5_2.core import lcdm_fit_reference

    sn_dir, bao_dir, output_dir = _validate_destination(Path(sn_dir), Path(bao_dir), Path(output_dir))
    if not isinstance(seed, int) or seed < 0:
        raise ValueError("Seed must be an explicit nonnegative integer.")
    sources = {"sn_table": sn_dir / SN_TABLE, "sn_covariance": sn_dir / SN_COV,
               "bao_table": bao_dir / BAO_TABLE, "bao_covariance": bao_dir / BAO_COV}
    source_hashes = {key: {"path": str(path), "sha256": sha256_file(path)} for key, path in sources.items()}
    sn, bao = load_des_sn(sn_dir), load_desi_dr2_bao(bao_dir)
    output_dir.mkdir(parents=True, exist_ok=False)
    for child in ("SN", "BAO", "MOCK_LCDM_cache", "REAL_DATA_GENERATING_FIT_ONLY_cache"):
        (output_dir / child).mkdir()
    marker = {
        "dataset_kind": DATASET_KIND, "is_real_observation": False,
        "label": "MOCK / SYNTHETIC: one Gaussian flat-LCDM realization",
        "created_utc": datetime.now(timezone.utc).isoformat(), "seed": seed,
        "generation_status": "INCOMPLETE", "source_files": source_hashes,
        "scope": "Synthetic diagnostic only. Never merge with real-observation benchmarks or discovery memory.",
    }
    readme = (
        "# MOCK / SYNTHETIC — NOT REAL OBSERVATIONS\n\n"
        "This directory belongs to one simulated flat-LCDM data set. Its values and any\n"
        "fits/search results obtained from them are mock results, separate from every\n"
        "real-data search. Never ingest them into real discovery memory, rankings or tables.\n\n"
        "Original filenames are retained solely for unchanged Solver loader compatibility.\n"
        "SN MUERR and other retained metadata come from the real survey; MUERR is not added\n"
        "again. The copied full likelihood covariance/precision is the complete noise model.\n"
        "Assumptions: fixed Gaussian likelihood, original redshifts and ordering, independent\n"
        "SN and BAO blocks, no additional covariance-uncertainty or selection-function draws.\n"
        "The generating LCDM parameters are fitted to real data once. The separate mock\n"
        "LCDM fit re-estimates Omega_m0 and both profiled nuisance parameters on this mock.\n"
        "Exception: REAL_DATA_GENERATING_FIT_ONLY.json and its similarly named cache\n"
        "contain a fit of REAL observations solely to define the synthetic generating mean;\n"
        "they are provenance records, not mock fits or a new real-data theory search.\n"
        "One data realization does not provide a look-elsewhere probability.\n"
    )
    folders = [output_dir, *(output_dir / name for name in ("SN", "BAO", "MOCK_LCDM_cache"))]
    for folder in folders:
        _write_json(folder / "manifest.json", marker)
        (folder / "README_MOCK.md").write_text(readme, encoding="utf-8")
    generating_cache = output_dir / "REAL_DATA_GENERATING_FIT_ONLY_cache"
    generating_cache_marker = {
        "artifact_kind": "LCDM_GENERATING_FIT_CACHE", "record_kind": "REAL_DATA_GENERATING_FIT_ONLY",
        "input_dataset_kind": "REAL_OBSERVATION", "parent_experiment_dataset_kind": DATASET_KIND,
        "is_mock_search_result": False, "generation_status": "INCOMPLETE", "source_files": source_hashes,
        "purpose": "Cache of the real-observation LCDM fit used ONLY to set the synthetic generating mean; not a mock fit or new theory search.",
    }
    _write_json(generating_cache / "manifest.json", generating_cache_marker)
    (generating_cache / "README_MOCK.md").write_text(
        "# REAL-DATA GENERATING FIT ONLY — provenance for a MOCK experiment\n\n"
        "The numeric LCDM cache in this folder was fitted to REAL OBSERVATIONS solely\n"
        "to set the generating mean for the parent synthetic data set. It is not a mock\n"
        "fit, not a theory-search result, and must not be pooled into either benchmark.\n"
        "The separately fitted MOCK reference is in ../MOCK_LCDM_reference.json.\n",
        encoding="utf-8")

    print("[MOCK] Fitting original observations ONLY to set generating parameters.", flush=True)
    with _private_lcdm_cache(output_dir / "REAL_DATA_GENERATING_FIT_ONLY_cache"):
        generating_fit = lcdm_fit_reference(sn, bao)
    _write_json(output_dir / "REAL_DATA_GENERATING_FIT_ONLY.json", {
        "record_kind": "REAL_DATA_GENERATING_FIT_ONLY", "input_dataset_kind": "REAL_OBSERVATION",
        "is_mock_search_result": False, "purpose": "Set synthetic generating mean; not a new real-data theory search.",
        "fit": generating_fit, "source_files": source_hashes,
    })
    zmax = max(float(np.max(sn["zHD"])), float(np.max(bao["z"])))
    z_grid = np.linspace(0.0, zmax * 1.001, 3000)
    omega = generating_fit["Omega_m0"]
    h_grid = np.sqrt(omega * (1.0 + z_grid) ** 3 + (1.0 - omega))
    sn_shape = mu_model_from_h_grid(sn["zHD"], sn["zHEL"], z_grid, h_grid, 70.0)
    bao_shape = bao_shape_from_grid(bao, z_grid, h_grid)
    sn_mean = sn_shape + generating_fit["sn_offset_hat"]
    bao_mean = generating_fit["bao_alpha_hat"] * bao_shape
    sn_stream, bao_stream = np.random.SeedSequence(seed).spawn(2)
    sn_z = np.random.Generator(np.random.PCG64(sn_stream)).standard_normal(len(sn_mean))
    bao_z = np.random.Generator(np.random.PCG64(bao_stream)).standard_normal(len(bao_mean))
    sn_precision = sn["invcov"] is not None
    sn_matrix = sn["invcov"] if sn_precision else sn["cov"]
    sn_noise = gaussian_noise(sn_matrix, sn_z, precision=sn_precision)
    bao_noise = gaussian_noise(bao["cov"], bao_z, precision=False)
    sn_values, bao_values = sn_mean + sn_noise, bao_mean + bao_noise
    write_sn_mock_table(sources["sn_table"], output_dir / "SN" / SN_TABLE, sn_values)
    write_bao_mock_table(sources["bao_table"], output_dir / "BAO" / BAO_TABLE, bao_values)
    shutil.copyfile(sources["sn_covariance"], output_dir / "SN" / SN_COV)
    shutil.copyfile(sources["bao_covariance"], output_dir / "BAO" / BAO_COV)
    np.savez_compressed(output_dir / "MOCK_generation_arrays.npz",
        dataset_kind=np.array(DATASET_KIND), is_real_observation=np.array(False), seed=np.array(seed),
        sn_zHD=sn["zHD"], sn_zHEL=sn["zHEL"], bao_z=bao["z"], bao_quantity=bao["quantity"],
        z_grid=z_grid, h_grid=h_grid, sn_shape=sn_shape, bao_shape=bao_shape,
        sn_mean=sn_mean, bao_mean=bao_mean, sn_whitened_gaussian=sn_z, bao_whitened_gaussian=bao_z,
        sn_noise=sn_noise, bao_noise=bao_noise, sn_mock=sn_values, bao_mock=bao_values)

    mock_sn, mock_bao = load_des_sn(output_dir / "SN"), load_desi_dr2_bao(output_dir / "BAO")
    for actual, expected in ((mock_sn["mu"], sn_values), (mock_bao["value"], bao_values),
        (mock_sn["zHD"], sn["zHD"]), (mock_sn["zHEL"], sn["zHEL"]),
        (mock_bao["z"], bao["z"]), (mock_bao["quantity"], bao["quantity"]),
        (mock_sn["invcov"] if sn_precision else mock_sn["cov"], sn_matrix), (mock_bao["cov"], bao["cov"])):
        if not np.array_equal(actual, expected):
            raise RuntimeError("MOCK readback verification failed; data must not be used.")
    for key, copied in (("sn_covariance", output_dir / "SN" / SN_COV), ("bao_covariance", output_dir / "BAO" / BAO_COV)):
        if sha256_file(copied) != source_hashes[key]["sha256"]:
            raise RuntimeError("Copied covariance is not byte-identical to its source.")

    print("[MOCK] Re-fitting LCDM to SYNTHETIC data in its isolated cache.", flush=True)
    with _private_lcdm_cache(output_dir / "MOCK_LCDM_cache"):
        mock_fit = lcdm_fit_reference(mock_sn, mock_bao)
    _write_json(output_dir / "MOCK_LCDM_reference.json", {
        "dataset_kind": DATASET_KIND, "is_real_observation": False,
        "record_kind": "MOCK_LCDM_REFIT", "label": "LCDM reference fitted on MOCK data only",
        "fit": mock_fit, "seed": seed,
    })
    for key, source in sources.items():
        if sha256_file(source) != source_hashes[key]["sha256"]:
            raise RuntimeError("Original data changed during generation; mock provenance is invalid.")
    functions = (load_des_sn, load_desi_dr2_bao, lcdm_fit_reference,
                 chi2_des_sn_from_grid, chi2_desi_bao_from_grid, mu_model_from_h_grid,
                 bao_shape_from_grid, gaussian_noise)
    code = {f"{func.__module__}.{func.__name__}": {
        "source_sha256": hashlib.sha256(inspect.getsource(func).encode()).hexdigest(),
        "module_path": str(Path(inspect.getfile(func)).resolve()),
        "module_sha256": sha256_file(Path(inspect.getfile(func))),
    } for func in functions}
    generated_files = (
        f"SN/{SN_TABLE}", f"SN/{SN_COV}", f"BAO/{BAO_TABLE}", f"BAO/{BAO_COV}",
        "MOCK_generation_arrays.npz", "MOCK_LCDM_reference.json",
    )
    marker.update({
        "generation_status": "VERIFIED", "source_bytes_unchanged": True,
        "copied_covariance_bytes_identical": True, "loader_readback_exact": True,
        "N_SN": len(sn_mean), "N_BAO": len(bao_mean), "generating_fit": generating_fit,
        "generating_fit_record_kind": "REAL_DATA_GENERATING_FIT_ONLY", "mock_lcdm_refit": mock_fit,
        "generating_model": "flat LCDM", "H0_fixed_km_s_Mpc": 70.0,
        "reference_fit_grid": {"Omega_m0_min": 0.05, "Omega_m0_max": 0.6, "Omega_m0_count": 551,
                               "redshift_grid_count": 3000, "redshift_grid_max": zmax * 1.001},
        "random": {"bit_generator": "PCG64", "seed_sequence_entropy": seed,
                   "sn_spawn_key": list(sn_stream.spawn_key), "bao_spawn_key": list(bao_stream.spawn_key)},
        "sn_noise_transform": "solve(cholesky(P).T, z)" if sn_precision else "cholesky(C) @ z",
        "bao_noise_transform": "cholesky(C) @ z", "sn_input_matrix_kind": sn["cov_mode"],
        "assumptions": ["Fixed full Gaussian likelihood covariance/precision", "SN and BAO blocks independent",
                        "Original redshifts, row order and nuisance profiling", "No second addition of MUERR",
                        "No covariance-estimation uncertainty or survey-selection resimulation"],
        "versions": {"numpy": np.__version__, "scipy": scipy.__version__}, "code_provenance": code,
        "generated_files_sha256": {name: sha256_file(output_dir / name) for name in generated_files},
        "files": {"SN": "SN", "BAO": "BAO", "arrays": "MOCK_generation_arrays.npz",
                  "mock_reference": "MOCK_LCDM_reference.json", "generating_reference": "REAL_DATA_GENERATING_FIT_ONLY.json"},
    })
    for folder in folders:
        _write_json(folder / "manifest.json", marker)
    generating_cache_marker["generation_status"] = "VERIFIED"
    _write_json(generating_cache / "manifest.json", generating_cache_marker)
    print(f"[MOCK VERIFIED] {output_dir} — SYNTHETIC DATA ONLY", flush=True)
    return marker


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sn-dir", type=Path, required=True, help="Original observed SN directory (read-only).")
    parser.add_argument("--bao-dir", type=Path, required=True, help="Original observed BAO directory (read-only).")
    parser.add_argument("--output-dir", type=Path, required=True, help="New disjoint directory, basename MOCK_*.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()
    generate_mock(args.sn_dir, args.bao_dir, args.output_dir, seed=args.seed)


if __name__ == "__main__":
    main()
