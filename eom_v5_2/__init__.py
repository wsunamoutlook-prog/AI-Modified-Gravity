"""Public API for the EOM v5.2 package."""
from __future__ import annotations

import sys

from . import core as _core
from . import runner as _runner
from .core import *
from .runner import run_eom

sys.modules.setdefault("eom_v5_2_core", _core)
sys.modules.setdefault("eom_v5_2_runner", _runner)

__all__ = ["run_eom"] + [name for name in dir(_core) if not name.startswith("__")]
