"""Public API for the Builder v5.2 package."""
from __future__ import annotations

import sys

from . import core as _core
from . import runner as _runner
from .core import Model
from .runner import run_build_cache

# Compatibility aliases for short-lived pre-package imports and old experiments.
sys.modules.setdefault("builder_v5_2_core", _core)
sys.modules.setdefault("builder_v5_2_runner", _runner)

__all__ = ["Model", "run_build_cache"]
