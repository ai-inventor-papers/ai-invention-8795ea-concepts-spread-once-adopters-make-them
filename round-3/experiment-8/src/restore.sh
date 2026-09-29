#!/usr/bin/env bash
# Recreate the deleted/regenerable parts of this workspace.
#   .venv/                 -> uv venv + pinned requirements
#   passA/parts/           -> uv run passA.py (zero-credit OpenAlex S3 range reads; ~25-55 min depending on bandwidth)
#   passB/parts/           -> uv run passB.py (~15-30 min)
#   data/ego_parts/, data/ego_timing/ -> python build_features.py --stage ego (~70 min on 5 workers)
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  uv venv .venv --python=3.12
  uv pip install --python .venv/bin/python -r requirements.lock.txt
fi
if [ "${1:-}" = "--scans" ]; then
  .venv/bin/python passA.py --workers 5 && .venv/bin/python passA.py --merge
  .venv/bin/python passB.py --workers 5 && .venv/bin/python passB.py --merge
fi
if [ "${1:-}" = "--ego" ]; then
  .venv/bin/python build_features.py --stage ego --workers 5
fi
