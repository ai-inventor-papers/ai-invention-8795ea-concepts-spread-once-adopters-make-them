#!/usr/bin/env bash
# Rebuild the paths marked `delete` in .aii/manifest.yaml.
set -euo pipefail
cd "$(dirname "$0")"
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python -r pyproject.toml
.venv/bin/python s5_typology.py --scope dev          # rebuilds dtw_cache/D_dev.npy (deterministic)
.venv/bin/python s5_typology.py --scope heldout      # rebuilds dtw_cache/D_{HELDOUT,COHORT}.npy (needs logs/unsealed.json)
