#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solver v5.2 entry point.

This file stays focused on editable run settings and starting the DES-SN +
DESI-DR2 BAO solve stage.  Implementation modules live in the solver_v5_2
package.  Model and SampleResult are imported here to keep older build-cache
pickles that reference __main__.Model compatible when this script is executed
directly.
"""
from __future__ import annotations

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# Run settings edited from this file
# =============================================================================

# Change values here, then run:
#     python3 "Solver v5.2.py"
#
# Shell environment variables still override these defaults, so batch scripts can
# keep controlling runs without editing the file.
RUN_SETTINGS = {
    # Data and output
    "SOLVER_OUTPUT_DIR": "solver_result",
    "SOLVER_RUN_NAME": "",
    "BUILD_CACHE_PATH": "",
    "SN_DIR": os.path.join(PROJECT_ROOT, "data", "SN data"),
    "BAO_DIR": os.path.join(PROJECT_ROOT, "data", "BAO data"),
    "CHECK_DATA_ONLY": "0",
    "TOP_N": "10",

    # Sampling and parallelism
    "N_SAMPLES_PER_MODEL": "3000", # samples per cached model #need to be optimized #Differential Evolution
    "RANDOM_SEED": "0",
    "SOLVER_PARALLEL": "auto",
    "PARALLEL_SAMPLE_THRESHOLD": "100",
    "N_WORKERS": str(max(1, (os.cpu_count() or 2) - 1)),
    "PROGRESS_EVERY_SECONDS": "10",
    "PROGRESS_SAVE_EVERY_MODELS": "25",
    "WORKER_SAMPLE_PROGRESS": "0",
    "MAX_MODELS_TO_BUILD": "0",

    # Numerical integration and likelihood grid
    "N_GRID": "150",
    "SN_INTEGRATION_GRID": "2000",
    "RTOL": "1e-6",
    "ATOL": "1e-8",
    "SAMPLE_INTEGRATION_TIMEOUT_SECONDS": "0",
    "MAX_ABS_CONSTRAINT": "1e-4",

    # Optional best-fit background identifiability audit.
    # off: historical behavior; report: write both counts without changing AIC;
    # use_rank: use the conservative Jacobian rank for primary AIC/BIC.
    "SOLVER_IDENTIFIABILITY_MODE": "off",
    "SOLVER_IDENTIFIABILITY_REL_STEP": "1e-3",
    "SOLVER_IDENTIFIABILITY_RANK_RTOL": "1e-4",
    "SOLVER_IDENTIFIABILITY_ZERO_RESPONSE_TOL": "1e-10",

    # Parameter priors
    "H0_MIN": "60.0",
    "H0_MAX": "75.0",
    "OMEGA_M0_MIN": "0.15",
    "OMEGA_M0_MAX": "0.45",
    "VARPHI1_0_MIN": "-5",
    "VARPHI1_0_MAX": "5",
    "VARPHI2_0_MIN": "-5",
    "VARPHI2_0_MAX": "5",
    "LOG10_MU1_MIN": "-3.0",
    "LOG10_MU1_MAX": "1.0",
    "LOG10_MU2_MIN": "-3.0",
    "LOG10_MU2_MAX": "1.0",
    "LOG10_FBAR1_MIN": "-2.0",
    "LOG10_FBAR1_MAX": "2.0",
    "LOG10_FBAR2_MIN": "-2.0",
    "LOG10_FBAR2_MAX": "2.0",
    "LOG10_LAMBDA_H_MIN": "2.0",
    "LOG10_LAMBDA_H_MAX": "5.0",
    "LOG10_ABS_C_MIN": "-10.0",
    "LOG10_ABS_C_MAX": "10.0",

    # Physical and trajectory cuts
    "FIX_EH_COEFFICIENT": "1",
    "EH_COEFFICIENT_VALUE": "0.5",
    "ENFORCE_EFT_CUTOFF": "1",
    "EFT_MAX_H_OVER_LAMBDA": "0.1",
    "MAX_ABS_Q0": "20.0",
    "PREFERRED_ABS_Q0": "2.0",
    "MAX_ABS_VARPHI_TRAJ": "200.0",
    "MAX_ABS_Q_TRAJ": "80.0",
    "MAX_H_KM_S_MPC": "1500.0",
    "MIN_H": "1e-8",

    # Cached Builder metadata checks
    "SOLVER_MODE": "eft",
    "BUILD_SIMPLIFY_MODE": "fast",
    "USE_LINEAR_RHS_SOLVER": "1",
    "ALLOW_GENERAL_SYMBOLIC_SOLVE": "1",
    "RHS_SIMPLIFY_MODE": "cancel",
}


def _apply_run_settings():
    """Apply file-level defaults before importing Solver modules."""
    for key, value in RUN_SETTINGS.items():
        os.environ.setdefault(key, str(value))


_apply_run_settings()

from solver_v5_2 import (
    Model,
    SampleResult,
    load_current_likelihood_data,
    run_solve_from_cache,
    run_top10_summary,
)

__all__ = ["Model", "SampleResult", "main"]


def main():
    """Run the Solver v5.2 solve stage using the current environment settings."""
    if os.environ.get("CHECK_DATA_ONLY", "0").strip().lower() in {"1", "true", "yes", "y", "on"}:
        load_current_likelihood_data()
        return
    run_solve_from_cache()
    top_n = int(os.environ.get("TOP_N", "10"))
    if top_n > 0:
        run_top10_summary(top_n=top_n)


if __name__ == "__main__":
    main()
