#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builder v5.2 entry point.

Edit RUN_SETTINGS here, then run:
    python3 "Builder v5.2.py"

The implementation lives in the builder_v5_2 package.  This file applies
run-specific defaults before importing the package, so configuration changes
here are visible to the build modules.
"""
from __future__ import annotations

import os

# =============================================================================
# Run settings edited from this file
# =============================================================================

# Shell environment variables override these defaults.  That keeps batch scripts
# useful while making ordinary interactive runs easy to tune from this file.
RUN_SETTINGS = {
    # Output and inputs
    "SOLVER_OUTPUT_DIR": "solver_result",
    "SOLVER_RUN_NAME": "",
    "BUILD_CACHE_PATH": "",
    "EOM_SUMMARY_PATH": "",
    "BUILDER_SOURCE_SCRIPT": "Builder v5.2.py",

    # Parser and model selection
    "SKIP_TRIVIAL_DUST_MODELS": "1",
    "SCALAR_CONFIG_FILTER": "all",
    "MAX_MODELS_TO_BUILD": "0",

    # Symbolic build controls
    "SOLVER_MODE": "eft",
    "BUILD_SIMPLIFY_MODE": "fast",
    "USE_LINEAR_RHS_SOLVER": "1",
    "ALLOW_GENERAL_SYMBOLIC_SOLVE": "1",
    "RHS_SIMPLIFY_MODE": "cancel",
    "SLOW_BUILD_SECONDS": "5",
    "BUILD_TIMEOUT_SECONDS": "60",

    # Normalization and EFT metadata carried into the cache
    "FIX_EH_COEFFICIENT": "0",
    "EH_COEFFICIENT_VALUE": "0.5",
    "ENFORCE_EFT_CUTOFF": "1",
    "EFT_MAX_H_OVER_LAMBDA": "0.1",

    # Kept for compatibility with historical Builder logs/cache metadata.
    "N_SAMPLES_PER_MODEL": "10",
    "RANDOM_SEED": "0",
    "SOLVER_PARALLEL": "auto",
    "PARALLEL_SAMPLE_THRESHOLD": "100",
    "N_WORKERS": str(max(1, (os.cpu_count() or 2) - 1)),
    "PROGRESS_EVERY_SECONDS": "10",
    "PROGRESS_SAVE_EVERY_MODELS": "25",
    "WORKER_SAMPLE_PROGRESS": "0",
    "LOG10_LAMBDA_H_MIN": "2.0",
    "LOG10_LAMBDA_H_MAX": "5.0",
}


def _apply_run_settings():
    """Apply file-level defaults before importing Builder modules."""
    for key, value in RUN_SETTINGS.items():
        os.environ.setdefault(key, str(value))


_apply_run_settings()

from builder_v5_2 import Model, run_build_cache

__all__ = ["Model", "main"]


def main():
    """Build and write the dimensionless model cache used by Solver v5.2."""
    run_build_cache()


if __name__ == "__main__":
    main()
