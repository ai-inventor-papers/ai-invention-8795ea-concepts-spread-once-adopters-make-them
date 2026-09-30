#!/usr/bin/env bash
# Restores every path that .aii/manifest.yaml marks as `delete` (all public, no credentials, zero OpenAlex credits).
set -euo pipefail
cd "$(dirname "$0")"

# 1. Python environments
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python torch --index-url https://download.pytorch.org/whl/cpu
uv pip install --python .venv/bin/python -r pyproject.toml
uv venv .venv_io --python=3.12     # light env used for the network fetchers (optional; .venv also works)
uv pip install --python .venv_io/bin/python pandas pyarrow aiohttp loguru lemminflect lxml rapidfuzz

# 2. OpenAlex concepts: parquet snapshot + legacy JSON snapshot (public S3 bucket over HTTPS)
mkdir -p cache/raw/concepts cache/raw/concepts_legacy
curl -s https://openalex.s3.amazonaws.com/data/parquet/concepts/manifest.json -o cache/raw/concepts/manifest.json
python3 - <<'PY' > cache/raw/concepts/urls.txt
import json
for f in json.load(open("cache/raw/concepts/manifest.json"))["files"]:
    u = f["url"]; print(u.replace("s3://openalex/", "https://openalex.s3.amazonaws.com/"), "cache/raw/concepts/" + u.split("/concepts/")[1])
PY
curl -s "https://openalex.s3.amazonaws.com/?list-type=2&prefix=legacy-data/concepts/&max-keys=1000" \
  | grep -oE '<Key>[^<]+\.gz</Key>' | sed -E 's#<Key>legacy-data/concepts/(.*)</Key>#https://openalex.s3.amazonaws.com/legacy-data/concepts/\1 cache/raw/concepts_legacy/\1#' \
  > cache/raw/concepts_legacy/urls.txt
cat cache/raw/concepts/urls.txt cache/raw/concepts_legacy/urls.txt | xargs -P 12 -n 2 sh -c 'mkdir -p "$(dirname "$1")" && curl -s --retry 4 -o "$1" "$0"'
# note: the S3 snapshots are updated in place; a later restore may differ slightly from the 2026-09-28 copy

# 3. MeSH 2026 (NLM)
mkdir -p cache/raw/mesh
curl -s -o cache/raw/mesh/desc2026.gz https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2026.gz
curl -s -o cache/raw/mesh/supp2026.gz https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/supp2026.gz

# 4. Clarivate/CAS Research Fronts reports (English PDFs hosted by CAS-ISD)
mkdir -p cache/raw/research_fronts
cp scripts/research_fronts_urls.txt cache/raw/research_fronts/main.txt
while read -r y u; do curl -s -L -A 'Mozilla/5.0' --retry 3 -o "cache/raw/research_fronts/rf_$y.pdf" "$u"; done < scripts/research_fronts_urls.txt

# 5. Regenerable intermediates (embeddings, pickled rows): rerun the pipeline from cache
#    (cache/wikidata, cache/wikipedia and cache/llm are kept, so no network or LLM spend is needed)
echo "restored; now run ./run_all.sh (network and LLM steps are served from cache/)"
