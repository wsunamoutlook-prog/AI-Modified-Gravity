"""Input and parameter validation shared by Signal Lab algorithms."""

from __future__ import annotations

from numbers import Integral, Real
from typing import Any, Mapping

import numpy as np


class SignalLabError(ValueError):
    """Base exception for invalid Signal Lab calls."""


class UnknownAlgorithmError(SignalLabError):
    """Raised when an algorithm name is not registered."""


def as_1d(value: Any, name: str, *, finite: bool = True) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    if array.ndim != 1:
        raise SignalLabError(f"{name} must be one-dimensional; got shape {array.shape}")
    if array.size == 0:
        raise SignalLabError(f"{name} must not be empty")
    if finite and not np.all(np.isfinite(array)):
        raise SignalLabError(f"{name} contains NaN or infinite values")
    return array


def as_2d(value: Any, name: str, *, finite: bool = True) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    if array.ndim != 2:
        raise SignalLabError(f"{name} must be two-dimensional; got shape {array.shape}")
    if 0 in array.shape:
        raise SignalLabError(f"{name} must not be empty")
    if finite and not np.all(np.isfinite(array)):
        raise SignalLabError(f"{name} contains NaN or infinite values")
    return array


def paired_1d(
    payload: Mapping[str, Any],
    x_key: str = "x",
    y_key: str = "y",
    *,
    finite: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    x = as_1d(payload[x_key], x_key, finite=finite)
    y = as_1d(payload[y_key], y_key, finite=finite)
    if x.size != y.size:
        raise SignalLabError(f"{x_key} and {y_key} must have equal length")
    return x, y


def require_strictly_increasing(x: np.ndarray, name: str = "x") -> None:
    if np.any(np.diff(x) <= 0):
        raise SignalLabError(f"{name} must be strictly increasing")


def require_uniform_spacing(
    x: np.ndarray,
    name: str = "x",
    *,
    rtol: float = 1e-5,
    atol: float = 1e-12,
) -> float:
    require_strictly_increasing(x, name)
    dx = np.diff(x)
    step = float(np.median(dx))
    if not np.allclose(dx, step, rtol=rtol, atol=atol):
        raise SignalLabError(
            f"{name} must be uniformly sampled for this algorithm; resample first"
        )
    return step


def odd_window(window: int, n: int, name: str = "window") -> int:
    if not isinstance(window, Integral) or isinstance(window, bool):
        raise SignalLabError(f"{name} must be an integer")
    value = int(window)
    if value < 3 or value % 2 == 0:
        raise SignalLabError(f"{name} must be an odd integer >= 3")
    if value > n:
        raise SignalLabError(f"{name}={value} exceeds data length {n}")
    return value


def validate_parameters(schema: Mapping[str, Any], params: Mapping[str, Any]) -> None:
    """Validate the useful subset of JSON Schema used by the registry."""
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    missing = sorted(required.difference(params))
    if missing:
        raise SignalLabError(f"missing required parameters: {', '.join(missing)}")

    if schema.get("additionalProperties") is False:
        unknown = sorted(set(params).difference(properties))
        if unknown:
            raise SignalLabError(f"unknown parameters: {', '.join(unknown)}")

    for name, value in params.items():
        rule = properties.get(name)
        if not rule:
            continue
        expected = rule.get("type")
        if expected == "number" and (
            not isinstance(value, Real) or isinstance(value, bool)
        ):
            raise SignalLabError(f"parameter {name} must be a number")
        if expected == "integer" and (
            not isinstance(value, Integral) or isinstance(value, bool)
        ):
            raise SignalLabError(f"parameter {name} must be an integer")
        if expected == "boolean" and not isinstance(value, bool):
            raise SignalLabError(f"parameter {name} must be boolean")
        if expected == "string" and not isinstance(value, str):
            raise SignalLabError(f"parameter {name} must be a string")
        if expected == "array" and not isinstance(value, (list, tuple, np.ndarray)):
            raise SignalLabError(f"parameter {name} must be an array")
        if "enum" in rule and value not in rule["enum"]:
            raise SignalLabError(
                f"parameter {name} must be one of {rule['enum']}; got {value!r}"
            )
        if "minimum" in rule and value < rule["minimum"]:
            raise SignalLabError(f"parameter {name} must be >= {rule['minimum']}")
        if "exclusiveMinimum" in rule and value <= rule["exclusiveMinimum"]:
            raise SignalLabError(
                f"parameter {name} must be > {rule['exclusiveMinimum']}"
            )
        if "maximum" in rule and value > rule["maximum"]:
            raise SignalLabError(f"parameter {name} must be <= {rule['maximum']}")
