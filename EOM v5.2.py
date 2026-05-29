#!/usr/bin/env python3
"""
EOM v5.2 entry point.

Adjust RUN_SETTINGS here, then run:
    python3 "EOM v5.2.py"

The implementation lives in eom_v5_2/ so this file stays short and easy to edit.
"""

from __future__ import annotations

import os
from pathlib import Path


# Runtime settings for the EOM stage. Values are applied as environment defaults,
# so shell variables can still override them for one-off smoke tests.
RUN_SETTINGS = {
    # Input/output paths
    "EOM_PROJECT_ROOT": str(Path(__file__).resolve().parent),
    "EOM_LAGRANGIANS_PATH": "",          # default: ./lagrangians.pkl
    "EOM_OUTPUT_DIR": "",                # default: ./eom_results

    # Work selection
    "EOM_MAX_TERMS": "12",               # use "all" or "none" for no cap
    "EOM_N_SAMPLES": "",                 # empty means process all selected lags
    "EOM_N_WORKERS": "1",

    # Symbolic/ghost-free settings
    "EOM_MAX_ALLOWED_ORDER": "2",
    "EOM_SEED_BASE": "42",
    "EOM_RUN_SELF_TEST": "1",
}


def _apply_run_settings() -> None:
    for key, value in RUN_SETTINGS.items():
        if value != "":
            os.environ.setdefault(key, value)


def main() -> None:
    _apply_run_settings()
    from eom_v5_2 import run_eom

    run_eom()


if __name__ == "__main__":
    main()
