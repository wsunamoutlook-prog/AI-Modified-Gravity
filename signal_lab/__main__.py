"""Command-line catalog browser for Signal Lab."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from .agent_api import execute, inspect, search, tool_manifest


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Browse and run atomic Signal Lab algorithms")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="search the algorithm catalog")
    list_parser.add_argument("--query", default="")
    list_parser.add_argument("--domain", choices=("general", "optics", "condensed_matter"))
    list_parser.add_argument("--category")
    list_parser.add_argument("--tag", action="append", default=[])
    list_parser.add_argument("--names-only", action="store_true")

    describe_parser = subparsers.add_parser("describe", help="show one algorithm contract")
    describe_parser.add_argument("name")

    run_parser = subparsers.add_parser("run", help="run one algorithm from an NPZ payload")
    run_parser.add_argument("name")
    run_parser.add_argument("--input", required=True, type=Path)
    run_parser.add_argument("--params", default="{}", help="JSON object")
    run_parser.add_argument("--output", required=True, type=Path)

    subparsers.add_parser("manifest", help="show the agent integration manifest")
    return parser


def _json_default(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    raise TypeError(f"not JSON serializable: {type(value).__name__}")


def main() -> int:
    args = _parser().parse_args()
    if args.command == "list":
        matches = search(args.query, domain=args.domain, category=args.category, tags=args.tag)
        if args.names_only:
            print("\n".join(item["name"] for item in matches))
        else:
            print(json.dumps(matches, indent=2))
        return 0
    if args.command == "describe":
        print(json.dumps(inspect(args.name), indent=2))
        return 0
    if args.command == "manifest":
        print(json.dumps(tool_manifest(), indent=2))
        return 0

    parameters = json.loads(args.params)
    if not isinstance(parameters, dict):
        raise ValueError("--params must decode to a JSON object")
    with np.load(args.input, allow_pickle=False) as loaded:
        payload = {key: loaded[key] for key in loaded.files}
    output = execute(args.name, payload, parameters)
    arrays: dict[str, np.ndarray] = {}
    sidecar: dict[str, Any] = {"metadata": output.metadata, "warnings": output.warnings, "scalars": {}}
    for name, value in output.values.items():
        array = np.asarray(value)
        if array.dtype == object:
            sidecar["scalars"][name] = value
        else:
            arrays[name] = array
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.output, **arrays)
    sidecar_path = args.output.with_suffix(args.output.suffix + ".json")
    sidecar_path.write_text(json.dumps(sidecar, indent=2, default=_json_default) + "\n")
    print(args.output)
    print(sidecar_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
