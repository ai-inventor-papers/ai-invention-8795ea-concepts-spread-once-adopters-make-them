#!/usr/bin/env bash
# Download the public OpenAlex sources snapshot (parquet, ~160 MB, free, no API credits).
cd "$(dirname "$0")"
cat sources_urls.txt | xargs -P 8 -I{} sh -c 'u="{}"; p="sources/${u#https://openalex.s3.amazonaws.com/data/parquet/sources/}"; mkdir -p "$(dirname "$p")"; [ -s "$p" ] || curl -s --retry 3 -o "$p" "$u"'
