#!/usr/bin/env bash
# Rebuild the Python environment (.venv is deleted after the run; see README "Restoring removed files").
set -euo pipefail
cd "$(dirname "$0")"
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r requirements.lock.txt
.venv/bin/python -c "import numpy, pandas, scipy, statsmodels, networkx, sklearn, matplotlib, loguru; print('environment ok')"
