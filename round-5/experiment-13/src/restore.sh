#!/usr/bin/env bash
# Restore the regenerable paths listed as `delete` in .aii/manifest.yaml.
set -euo pipefail
cd "$(dirname "$0")"
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r requirements.lock.txt
.venv/bin/python -m spacy download en_core_web_sm
PYTHONPATH=lib .venv/bin/python passM.py --workers 9
PYTHONPATH=lib .venv/bin/python passM.py --merge --workers 6
.venv/bin/python s3_candidates.py --stage recover
