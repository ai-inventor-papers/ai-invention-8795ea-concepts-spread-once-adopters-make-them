#!/usr/bin/env bash
# Recreate the deleted Python environment (the only non-cache entry marked delete in .aii/manifest.yaml).
set -euo pipefail
cd "$(dirname "$0")"
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r pyproject.toml
.venv/bin/python -c "import pyfixest, statsmodels, pandas, numpy; print('environment OK')"
