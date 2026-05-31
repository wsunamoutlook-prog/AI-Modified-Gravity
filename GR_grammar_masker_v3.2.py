#!/usr/bin/env python3
"""
GR grammar masker v3.2 entry point.

Adjust RUN_SETTINGS here, then run:
    python3 "GR_grammar_masker_v3.2.py"

The implementation lives in gr_grammar_masker_v3_2/ so this file stays short.
"""

from __future__ import annotations

import os
from pathlib import Path


RUN_SETTINGS = {
    # Paths
    "MASKER_PROJECT_ROOT": str(Path(__file__).resolve().parent),
    "MASKER_OUTPUT_DIR": "",             # default: ./lagrangians
    "MASKER_PICKLE_PATH": "",            # default: ./lagrangians.pkl

    # Grammar/tensor generation
    "MASKER_MAX_DERIVATIVES": "2",
    "MASKER_DIMENSIONS": "2,3,4,5,6",

    # Lagrangian sampling
    "MASKER_N_TERMS_LIST": "1,2,3,4,5,6,7,8,9,10,11,12",
    "MASKER_N_SAMPLES": "100",
    "MASKER_RANDOM_SEED": "42",#need to be changed

    # Output verbosity
    "MASKER_PRINT_GRAMMAR_SANITY": "1",
    "MASKER_VERBOSE_DIMENSIONS": "1",
    "MASKER_SAMPLE_PRINT_COUNT": "3",
}


def _apply_run_settings() -> None:
    for key, value in RUN_SETTINGS.items():
        if value != "":
            os.environ.setdefault(key, value)


def main() -> None:
    _apply_run_settings()
    from gr_grammar_masker_v3_2 import run_masker

    run_masker()


if __name__ == "__main__":
    main()
