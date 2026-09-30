#!/usr/bin/env bash
# Restores the files the manifest marks as `delete`: the Python environment and the OpenAlex snapshot
# metadata (sources, topics, subfields, fields; ~390 MB, free, no credentials). Run from the repository root.
set -euo pipefail

# 1. Python environment
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r pyproject.toml   # exact pinned versions

# 2. OpenAlex snapshot metadata (public bucket; HTTPS mirror of s3://openalex, no AWS account needed)
mkdir -p snapshot
for e in sources topics subfields fields; do
  curl -s "https://openalex.s3.amazonaws.com/data/parquet/$e/manifest.json" -o "snapshot/${e}_manifest.json"
  python3 - "$e" <<'EOF' > "snapshot/${e}_urls.txt"
import json, sys
e = sys.argv[1]
m = json.load(open(f"snapshot/{e}_manifest.json"))
for f in m["files"]:
    print(f["url"].replace("s3://openalex/", "https://openalex.s3.amazonaws.com/"), "snapshot/" + e + "/" + f["url"].split(f"/{e}/")[1])
EOF
  xargs -P 16 -n 2 sh -c 'mkdir -p "$(dirname "$1")" && curl -s --retry 4 -o "$1" "$0"' < "snapshot/${e}_urls.txt"
done
# works manifest (the scan streams column ranges of the works files over HTTPS; nothing is stored locally)
curl -s "https://openalex.s3.amazonaws.com/data/parquet/works/manifest.json" -o snapshot/works_manifest.json
# Equivalent with the AWS CLI:  aws s3 sync s3://openalex/data/parquet/<entity> snapshot/<entity> --no-sign-request
echo "restored .venv and snapshot/"
