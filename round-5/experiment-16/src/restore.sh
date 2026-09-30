#!/usr/bin/env bash
# Rebuild every file marked `delete` in .aii/manifest.yaml (all deterministic: seeded).
set -euo pipefail
cd "$(dirname "$0")"
export AII_RUN_ROOT="${AII_RUN_ROOT:-$(cd ../../../.. && pwd)}"   # the run root holding EXP5/EXP8/EXP10 read-only inputs
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python numpy pandas pyarrow scipy igraph numba loguru snowballstemmer matplotlib statsmodels psutil
.venv/bin/python -c "import sys; sys.path.insert(0, 'lib'); from jobs import build_home_cache; build_home_cache()"
OMP_NUM_THREADS=1 .venv/bin/python s2_variants.py --tag full --workers 4      # ~3 min  -> data/s2_parts_full/
OMP_NUM_THREADS=1 .venv/bin/python s3_nulls.py --tag full                     # ~10 min -> data/v3_halves_full.pkl
