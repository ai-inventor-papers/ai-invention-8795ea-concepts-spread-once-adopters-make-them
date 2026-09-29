#!/usr/bin/env bash
# Recreate the Python environment (pinned versions) for this artifact.
set -euo pipefail
cd "$(dirname "$0")"
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r requirements.lock.txt
.venv/bin/python -c "import numpy, pandas, sklearn, interpret, igraph, leidenalg, ahocorasick, aiohttp, statsmodels; print('environment ok')"
