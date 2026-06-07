#!/usr/bin/env bash
# Source this file on Oscar before running the project manually or from Slurm.

set -euo pipefail

module purge
module load python/3.12.8-zr3c

export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export MPLCONFIGDIR="${PWD}/.matplotlib-cache"

mkdir -p "${MPLCONFIGDIR}"

if [[ ! -d .venv ]]; then
  python -m venv .venv
fi

source .venv/bin/activate

REQ_FILE="ai_theory_lab/cluster/requirements-oscar.txt"
REQ_STAMP=".venv/.requirements-oscar.sha256"
REQ_HASH="$(python - <<'PY'
from pathlib import Path
import hashlib
path = Path("ai_theory_lab/cluster/requirements-oscar.txt")
print(hashlib.sha256(path.read_bytes()).hexdigest())
PY
)"

if [[ ! -f "${REQ_STAMP}" ]] || [[ "$(cat "${REQ_STAMP}")" != "${REQ_HASH}" ]]; then
  python -m pip install --upgrade pip wheel setuptools
  python -m pip install -r "${REQ_FILE}"
  printf "%s" "${REQ_HASH}" > "${REQ_STAMP}"
fi
