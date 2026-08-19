#!/bin/bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
REMOTE=${MODIFY_GR_OSCAR_REMOTE:-wsun47@ssh.ccv.brown.edu:/oscar/home/wsun47/Modify_GR/}
MANIFEST=$(mktemp)
trap 'rm -f "$MANIFEST"' EXIT
TOKEN_CACHE=ai_theory_lab/cache/token_context_v1_deriv2_dims2_3_4_5_6.pkl

cd "$ROOT"
git ls-files -z > "$MANIFEST"
if [[ -s "$TOKEN_CACHE" ]]; then
  # This cache contains legal Grammar Masker candidates only, never historical
  # Solver winners. Shipping it avoids six simultaneous symbolic rebuilds.
  printf '%s\0' "$TOKEN_CACHE" >> "$MANIFEST"
  echo "Including verified token-context cache: $TOKEN_CACHE"
else
  echo "Token-context cache is absent; Oscar preflight will build it once."
fi

rsync -avc --itemize-changes --from0 --files-from="$MANIFEST" ./ "$REMOTE"
