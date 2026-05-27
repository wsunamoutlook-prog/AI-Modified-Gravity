#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DAT_PATH = REPO_ROOT / "data" / "PantheonPlus" / "Pantheon+SH0ES.dat"
DEFAULT_COV_PATH = REPO_ROOT / "data" / "PantheonPlus" / "Pantheon+SH0ES_STAT+SYS.cov"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "pantheonplus_no_shoes.npz"


def make_non_calibrator_mask(col):
    arr = np.asarray(col)
    if arr.dtype == np.bool_:
        return ~arr
    if np.issubdtype(arr.dtype, np.number):
        return arr.astype(float) == 0.0

    text = np.char.strip(arr.astype(str))
    lower = np.char.lower(text)
    is_calibrator = np.isin(lower, ["1", "1.0", "true", "t", "yes", "y"])
    is_non_calibrator = np.isin(lower, ["0", "0.0", "false", "f", "no", "n"])
    if not np.all(is_calibrator | is_non_calibrator):
        bad = np.unique(text[~(is_calibrator | is_non_calibrator)])
        raise ValueError(f"Unrecognized IS_CALIBRATOR values: {bad[:10]}")
    return is_non_calibrator


def read_pantheon_cov(path):
    vals = np.loadtxt(path)
    vals = np.asarray(vals, dtype=float).reshape(-1)

    n0 = int(round(vals[0]))
    if n0 > 0 and vals.size == n0 * n0 + 1:
        return vals[1:].reshape(n0, n0)

    n = int(round(np.sqrt(vals.size)))
    if n > 0 and n * n == vals.size:
        return vals.reshape(n, n)

    raise ValueError(
        f"Unexpected covariance size in {path}: got {vals.size} values. "
        "Expected either n*n+1 values with leading n, or exactly n*n values."
    )


def prepare_pantheonplus(dat_path=DEFAULT_DAT_PATH, cov_path=DEFAULT_COV_PATH, output_path=DEFAULT_OUTPUT_PATH):
    dat_path = Path(dat_path)
    cov_path = Path(cov_path)
    output_path = Path(output_path)

    tab = np.genfromtxt(dat_path, names=True, dtype=None, encoding=None)
    required = {"zHD", "zHEL", "m_b_corr", "IS_CALIBRATOR"}
    names = set(tab.dtype.names or ())
    missing = sorted(required - names)
    if missing:
        raise ValueError(f"Missing required Pantheon+ columns {missing}; available columns: {tab.dtype.names}")

    mask = make_non_calibrator_mask(tab["IS_CALIBRATOR"])
    zHD = np.asarray(tab["zHD"][mask], dtype=float)
    zHEL = np.asarray(tab["zHEL"][mask], dtype=float)
    mb = np.asarray(tab["m_b_corr"][mask], dtype=float)

    cov = read_pantheon_cov(cov_path)
    n_raw = len(tab)
    if cov.shape != (n_raw, n_raw):
        raise ValueError(f"Raw covariance shape {cov.shape} does not match raw table length {n_raw}.")
    cov = cov[np.ix_(mask, mask)]

    if not (len(zHD) == len(zHEL) == len(mb)):
        raise ValueError("Processed SN arrays have inconsistent lengths.")
    if cov.shape != (len(zHD), len(zHD)):
        raise ValueError(f"Processed covariance shape {cov.shape} does not match N_kept={len(zHD)}.")
    if not (np.all(np.isfinite(zHD)) and np.all(np.isfinite(zHEL)) and np.all(np.isfinite(mb))):
        raise ValueError("Processed zHD, zHEL, or m_b_corr contains non-finite values.")
    if not np.allclose(cov, cov.T, rtol=1e-10, atol=1e-12):
        raise ValueError("Processed covariance is not symmetric.")
    if np.any(np.diag(cov) <= 0):
        raise ValueError("Processed covariance diagonal contains non-positive entries.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        output_path,
        zHD=zHD.astype(float),
        zHEL=zHEL.astype(float),
        mb=mb.astype(float),
        cov=cov.astype(float),
        source="Pantheon+SH0ES.dat",
        include_shoes=False,
        observable="m_b_corr",
    )

    summary = {
        "N_raw": int(n_raw),
        "N_kept": int(len(zHD)),
        "N_calibrator_removed": int(n_raw - len(zHD)),
        "cov_shape": tuple(cov.shape),
        "zHD_min": float(np.min(zHD)),
        "zHD_max": float(np.max(zHD)),
        "output_path": str(output_path),
    }
    print(
        "Pantheon+ preprocessing complete: "
        f"N_raw={summary['N_raw']}, N_kept={summary['N_kept']}, "
        f"N_calibrator_removed={summary['N_calibrator_removed']}, "
        f"cov_shape={summary['cov_shape']}, "
        f"zHD=[{summary['zHD_min']:.8g}, {summary['zHD_max']:.8g}], "
        f"output={output_path}"
    )
    return summary


def main():
    prepare_pantheonplus()


if __name__ == "__main__":
    main()
