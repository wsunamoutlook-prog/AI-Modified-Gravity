#!/usr/bin/env python3
"""Split an agent parameter-sample JSON array into deterministic chunks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--chunk-size", type=int, required=True)
    parser.add_argument("--output-prefix", type=Path, required=True)
    args = parser.parse_args()

    samples = json.loads(args.input.read_text())
    if not isinstance(samples, list):
        raise ValueError("input must be a JSON array of parameter samples")
    if args.chunk_size <= 0:
        raise ValueError("--chunk-size must be positive")

    args.output_prefix.parent.mkdir(parents=True, exist_ok=True)
    for start in range(0, len(samples), args.chunk_size):
        chunk = samples[start : start + args.chunk_size]
        number = start // args.chunk_size + 1
        output = args.output_prefix.with_name(
            f"{args.output_prefix.name}_part{number:02d}.json"
        )
        output.write_text(json.dumps(chunk, indent=2, ensure_ascii=False) + "\n")
        print(f"{output}: samples={len(chunk)} range={start + 1}-{start + len(chunk)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
