#!/bin/bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
REMOTE=${MODIFY_GR_OSCAR_REMOTE:-wsun47@ssh.ccv.brown.edu:/oscar/home/wsun47/Modify_GR/}
MANIFEST=$(mktemp)
trap 'rm -f "$MANIFEST"' EXIT

cd "$ROOT"
git ls-files -z > "$MANIFEST"

rsync -avc --itemize-changes --from0 --files-from="$MANIFEST" ./ "$REMOTE"
