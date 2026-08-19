"""Build and verify the cold-start legal-operator cache."""

from __future__ import annotations

import argparse

from .cold_start_runner import (
    _build_token_level_context,
    _token_context_cache_path,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or verify the shared 141-candidate Grammar Masker cache."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=0,
        help="Optional wall-time limit in seconds for a cache miss; zero disables the limit.",
    )
    args = parser.parse_args()

    context = _build_token_level_context(args.timeout, use_cache=True)
    candidate_count = len(getattr(context["masker"], "all_candidates", []) or [])
    if candidate_count != 141:
        raise SystemExit(f"Expected 141 legal candidates, found {candidate_count}")

    path = _token_context_cache_path()
    if not path.is_file() or path.stat().st_size <= 0:
        raise SystemExit(f"Token-context cache was not written correctly: {path}")

    print(f"token_context_cache={path}")
    print(f"candidate_count={candidate_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
