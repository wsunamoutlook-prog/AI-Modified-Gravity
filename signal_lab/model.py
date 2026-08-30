"""Core data models for agent-callable Signal Lab algorithms."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

import numpy as np


def _json_value(value: Any) -> Any:
    """Convert common scientific Python values into JSON-safe objects."""
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


@dataclass(frozen=True)
class AlgorithmSpec:
    """Machine-readable contract for one atomic processing algorithm."""

    name: str
    domain: str
    category: str
    summary: str
    required_inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    parameter_schema: Mapping[str, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    caveats: tuple[str, ...] = ()
    references: tuple[str, ...] = ()
    version: str = "1.0"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "category": self.category,
            "summary": self.summary,
            "required_inputs": list(self.required_inputs),
            "outputs": list(self.outputs),
            "parameter_schema": dict(self.parameter_schema),
            "tags": list(self.tags),
            "assumptions": list(self.assumptions),
            "caveats": list(self.caveats),
            "references": list(self.references),
            "version": self.version,
        }


@dataclass
class AlgorithmResult:
    """Values and provenance returned by an atomic algorithm."""

    values: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self, *, json_safe: bool = False) -> dict[str, Any]:
        payload = {
            "values": self.values,
            "metadata": self.metadata,
            "warnings": self.warnings,
        }
        return _json_value(payload) if json_safe else payload


def result(
    values: Mapping[str, Any],
    *,
    metadata: Mapping[str, Any] | None = None,
    warnings: list[str] | None = None,
) -> AlgorithmResult:
    """Small convenience constructor used by algorithm implementations."""
    return AlgorithmResult(
        values=dict(values),
        metadata=dict(metadata or {}),
        warnings=list(warnings or []),
    )
