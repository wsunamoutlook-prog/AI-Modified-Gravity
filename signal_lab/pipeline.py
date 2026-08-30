"""Composable, JSON-friendly pipelines built from atomic algorithms."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from .model import AlgorithmResult
from .registry import REGISTRY
from .validation import SignalLabError


@dataclass(frozen=True)
class PipelineStep:
    """One algorithm call with explicit state-key mappings."""

    algorithm: str
    params: Mapping[str, Any] = field(default_factory=dict)
    inputs: Mapping[str, str] = field(default_factory=dict)
    outputs: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "PipelineStep":
        if "algorithm" not in value:
            raise SignalLabError("pipeline step is missing algorithm")
        return cls(
            algorithm=str(value["algorithm"]),
            params=dict(value.get("params", {})),
            inputs=dict(value.get("inputs", {})),
            outputs=dict(value.get("outputs", {})),
        )


@dataclass
class PipelineResult:
    state: dict[str, Any]
    history: list[dict[str, Any]]


def run_pipeline(
    initial_state: Mapping[str, Any],
    steps: Sequence[PipelineStep | Mapping[str, Any]],
    *,
    allow_overwrite: bool = True,
) -> PipelineResult:
    """Run atomic steps, mapping each step's input/output names to shared state keys."""
    state = dict(initial_state)
    history: list[dict[str, Any]] = []
    for index, raw_step in enumerate(steps):
        step = raw_step if isinstance(raw_step, PipelineStep) else PipelineStep.from_mapping(raw_step)
        spec = REGISTRY.describe(step.algorithm)
        payload: dict[str, Any] = {}
        for required_name in spec["required_inputs"]:
            state_key = step.inputs.get(required_name, required_name)
            if state_key not in state:
                raise SignalLabError(
                    f"pipeline step {index} ({step.algorithm}) needs state key {state_key!r} "
                    f"for input {required_name!r}"
                )
            payload[required_name] = state[state_key]
        output = REGISTRY.run(step.algorithm, payload, step.params)
        destinations: dict[str, str] = {}
        for output_name, value in output.values.items():
            state_key = step.outputs.get(output_name, output_name)
            if not allow_overwrite and state_key in state:
                raise SignalLabError(
                    f"pipeline step {index} would overwrite state key {state_key!r}"
                )
            state[state_key] = value
            destinations[output_name] = state_key
        history.append(
            {
                "step": index,
                "algorithm": step.algorithm,
                "params": dict(step.params),
                "input_state_keys": {
                    name: step.inputs.get(name, name) for name in spec["required_inputs"]
                },
                "output_state_keys": destinations,
                "metadata": dict(output.metadata),
                "warnings": list(output.warnings),
            }
        )
    return PipelineResult(state=state, history=history)
