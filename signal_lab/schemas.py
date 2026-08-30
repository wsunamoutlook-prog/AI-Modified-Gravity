"""Helpers for concise JSON-compatible parameter schemas."""

from __future__ import annotations

from typing import Any


def object_schema(
    properties: dict[str, dict[str, Any]] | None = None,
    *,
    required: tuple[str, ...] = (),
) -> dict[str, Any]:
    schema: dict[str, Any] = {
        "type": "object",
        "properties": properties or {},
        "additionalProperties": False,
    }
    if required:
        schema["required"] = list(required)
    return schema


def number(
    default: float | None = None,
    *,
    minimum: float | None = None,
    exclusive_minimum: float | None = None,
    maximum: float | None = None,
    description: str = "",
) -> dict[str, Any]:
    rule: dict[str, Any] = {"type": "number"}
    if default is not None:
        rule["default"] = default
    if minimum is not None:
        rule["minimum"] = minimum
    if exclusive_minimum is not None:
        rule["exclusiveMinimum"] = exclusive_minimum
    if maximum is not None:
        rule["maximum"] = maximum
    if description:
        rule["description"] = description
    return rule


def integer(
    default: int | None = None,
    *,
    minimum: int | None = None,
    maximum: int | None = None,
    description: str = "",
) -> dict[str, Any]:
    rule: dict[str, Any] = {"type": "integer"}
    if default is not None:
        rule["default"] = default
    if minimum is not None:
        rule["minimum"] = minimum
    if maximum is not None:
        rule["maximum"] = maximum
    if description:
        rule["description"] = description
    return rule


def choice(default: str, choices: tuple[str, ...], description: str = "") -> dict[str, Any]:
    rule: dict[str, Any] = {"type": "string", "enum": list(choices), "default": default}
    if description:
        rule["description"] = description
    return rule


def boolean(default: bool = False, description: str = "") -> dict[str, Any]:
    rule: dict[str, Any] = {"type": "boolean", "default": default}
    if description:
        rule["description"] = description
    return rule
