"""Registry and execution API for atomic Signal Lab algorithms."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from .model import AlgorithmResult, AlgorithmSpec, result
from .validation import SignalLabError, UnknownAlgorithmError, validate_parameters

AlgorithmFunction = Callable[[Mapping[str, Any], Mapping[str, Any]], AlgorithmResult]


class AlgorithmRegistry:
    def __init__(self) -> None:
        self._specs: dict[str, AlgorithmSpec] = {}
        self._functions: dict[str, AlgorithmFunction] = {}

    def register(
        self, spec: AlgorithmSpec
    ) -> Callable[[AlgorithmFunction], AlgorithmFunction]:
        if not spec.name or "." not in spec.name:
            raise SignalLabError(
                "algorithm names must be stable dotted identifiers, e.g. signal.welch_psd"
            )

        def decorator(function: AlgorithmFunction) -> AlgorithmFunction:
            if spec.name in self._specs:
                raise SignalLabError(f"algorithm already registered: {spec.name}")
            self._specs[spec.name] = spec
            self._functions[spec.name] = function
            return function

        return decorator

    def describe(self, name: str) -> dict[str, Any]:
        try:
            return self._specs[name].to_dict()
        except KeyError as exc:
            raise UnknownAlgorithmError(f"unknown algorithm: {name}") from exc

    def list(
        self,
        *,
        domain: str | None = None,
        category: str | None = None,
        tags: tuple[str, ...] = (),
        query: str | None = None,
    ) -> list[dict[str, Any]]:
        query_text = (query or "").lower().strip()
        requested_tags = {tag.lower() for tag in tags}
        matches: list[AlgorithmSpec] = []
        for spec in self._specs.values():
            if domain and spec.domain != domain:
                continue
            if category and spec.category != category:
                continue
            if requested_tags and not requested_tags.issubset(
                {tag.lower() for tag in spec.tags}
            ):
                continue
            searchable = " ".join(
                [spec.name, spec.domain, spec.category, spec.summary, *spec.tags]
            ).lower()
            if query_text and query_text not in searchable:
                continue
            matches.append(spec)
        return [spec.to_dict() for spec in sorted(matches, key=lambda item: item.name)]

    def run(
        self,
        name: str,
        payload: Mapping[str, Any],
        params: Mapping[str, Any] | None = None,
    ) -> AlgorithmResult:
        if name not in self._specs:
            raise UnknownAlgorithmError(f"unknown algorithm: {name}")
        spec = self._specs[name]
        missing = [key for key in spec.required_inputs if key not in payload]
        if missing:
            raise SignalLabError(f"missing required inputs: {', '.join(missing)}")
        parameters = dict(params or {})
        validate_parameters(spec.parameter_schema, parameters)
        output = self._functions[name](payload, parameters)
        if isinstance(output, Mapping):
            output = result(output)
        if not isinstance(output, AlgorithmResult):
            raise TypeError(f"{name} returned {type(output).__name__}, not AlgorithmResult")
        output.metadata.setdefault("algorithm", name)
        output.metadata.setdefault("algorithm_version", spec.version)
        missing_outputs = [key for key in spec.outputs if key not in output.values]
        if missing_outputs:
            raise RuntimeError(
                f"{name} did not return declared outputs: {', '.join(missing_outputs)}"
            )
        return output


REGISTRY = AlgorithmRegistry()


def algorithm(spec: AlgorithmSpec) -> Callable[[AlgorithmFunction], AlgorithmFunction]:
    return REGISTRY.register(spec)


def list_algorithms(**filters: Any) -> list[dict[str, Any]]:
    return REGISTRY.list(**filters)


def describe(name: str) -> dict[str, Any]:
    return REGISTRY.describe(name)


def run(
    name: str,
    payload: Mapping[str, Any],
    params: Mapping[str, Any] | None = None,
) -> AlgorithmResult:
    return REGISTRY.run(name, payload, params)
