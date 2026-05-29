"""Public API for the GR grammar masker v3.2 package."""
from __future__ import annotations

__all__ = ["CandidateScalar", "GravityMasker", "GravityState", "run_masker"]


def run_masker(*args, **kwargs):
    """Run the masker without importing heavy tensor modules before logging starts."""
    from .runner import run_masker as _run_masker

    return _run_masker(*args, **kwargs)


def __getattr__(name):
    if name in {"CandidateScalar", "GravityMasker", "GravityState"}:
        from . import grammar

        return getattr(grammar, name)
    raise AttributeError(name)
