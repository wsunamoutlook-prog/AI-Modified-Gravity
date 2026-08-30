"""Signal Lab: atomic, agent-callable experimental data processing."""

from .model import AlgorithmResult, AlgorithmSpec
from .pipeline import PipelineResult, PipelineStep, run_pipeline
from .registry import REGISTRY, describe, list_algorithms, run
from .validation import SignalLabError, UnknownAlgorithmError

# Importing collections performs their declarative registry registration.
from . import generic as _generic  # noqa: F401,E402
from . import optics as _optics  # noqa: F401,E402
from . import condensed_matter as _condensed_matter  # noqa: F401,E402
from . import extensions as _extensions  # noqa: F401,E402

__all__ = [
    "AlgorithmResult",
    "AlgorithmSpec",
    "PipelineResult",
    "PipelineStep",
    "REGISTRY",
    "SignalLabError",
    "UnknownAlgorithmError",
    "describe",
    "list_algorithms",
    "run",
    "run_pipeline",
]

__version__ = "0.1.0"
