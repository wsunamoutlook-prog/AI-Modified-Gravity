"""Public API for the Solver v5.2 package.

The package modules live under ``solver_v5_2``.  A few aliases are registered
for compatibility with short-lived pre-package module names used while this
solver was being reorganized.
"""
from __future__ import annotations

import sys

from . import core as _core
from . import likelihood as _likelihood
from . import runner as _runner
from . import summary as _summary
from .core import Model, SampleResult, load_current_likelihood_data
from .runner import run_solve_from_cache
from .summary import run_top10_summary

sys.modules.setdefault("solver_v5_2_core", _core)
sys.modules.setdefault("solver_v5_2_likelihood", _likelihood)
sys.modules.setdefault("solver_v5_2_runner", _runner)
sys.modules.setdefault("solver_v5_2_summary", _summary)

__all__ = [
    "Model",
    "SampleResult",
    "load_current_likelihood_data",
    "run_solve_from_cache",
    "run_top10_summary",
]
