#!/usr/bin/env bash
# Restore the deleted, re-downloadable parts of this workspace (no credentials needed).
set -euo pipefail
cd "$(dirname "$0")"
uv venv .venv --python=3.12
# exact pinned versions (torch is the +cpu build from the PyTorch CPU index)
uv pip install --python .venv/bin/python -r pyproject.toml --extra-index-url https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match
mkdir -p snapshot/concepts
curl -s -o snapshot/works_manifest.json https://openalex.s3.amazonaws.com/data/parquet/works/manifest.json
curl -s -o snapshot/concepts_manifest.json https://openalex.s3.amazonaws.com/data/parquet/concepts/manifest.json
.venv/bin/python - <<'PY'
import json, urllib.request
m = json.load(open("snapshot/concepts_manifest.json"))
for i, f in enumerate(m["files"]):
    urllib.request.urlretrieve(f["url"].replace("s3://openalex/", "https://openalex.s3.amazonaws.com/"),
                               f"snapshot/concepts/part_{i:02d}.parquet")
PY
echo "restored .venv and snapshot/ (note: the works manifest is the CURRENT release; this run used 2026-09-23)"
