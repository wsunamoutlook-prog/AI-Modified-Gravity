"""Stable discovery and execution surface intended for automated agents."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .model import AlgorithmResult
from .pipeline import PipelineResult, PipelineStep, run_pipeline
from .registry import describe, list_algorithms, run


def search(
    query: str = "",
    *,
    domain: str | None = None,
    category: str | None = None,
    tags: Sequence[str] = (),
) -> list[dict[str, Any]]:
    """Search atomic algorithms by stable names and metadata."""
    return list_algorithms(
        query=query,
        domain=domain,
        category=category,
        tags=tuple(tags),
    )


def inspect(name: str) -> dict[str, Any]:
    """Return the complete machine-readable contract before execution."""
    return describe(name)


def execute(
    name: str,
    data: Mapping[str, Any],
    params: Mapping[str, Any] | None = None,
) -> AlgorithmResult:
    """Execute exactly one atomic algorithm."""
    return run(name, data, params)


def execute_pipeline(
    state: Mapping[str, Any],
    steps: Sequence[PipelineStep | Mapping[str, Any]],
    *,
    allow_overwrite: bool = True,
) -> PipelineResult:
    """Execute a declarative sequence of atomic algorithms."""
    return run_pipeline(state, steps, allow_overwrite=allow_overwrite)


def tool_manifest() -> dict[str, Any]:
    """Return a compact tool manifest suitable for an agent system prompt."""
    return {
        "tool": "signal_lab.execute",
        "workflow": [
            "search(query/domain/category/tags)",
            "inspect(name)",
            "execute(name, data, params)",
        ],
        "rules": [
            "Inspect assumptions and caveats before execution.",
            "Preserve raw data and record every algorithm name and parameter.",
            "Do not infer causality or physical mechanism from a processing result alone.",
            "Propagate units explicitly; arrays are not assigned hidden units.",
        ],
        "algorithm_count": len(list_algorithms()),
        "domains": ["general", "optics", "condensed_matter"],
    }
