# Reproducing this artifact (Ubuntu)

All sources are public and need no credentials. OpenAlex is read from its public S3 bucket, so no API credits are
used. Every LLM verdict is cached in `cache/llm/calls.jsonl`, so a rerun with unchanged prompts costs $0.

## 1. Prerequisites

* Ubuntu with `curl` and `python3`.
* [`uv`](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
* About 6 GB of free disk space (5 GB of it is the CPU-torch environment for MiniLM).
* Optional: `OPENROUTER_API_KEY` and `OPENROUTER_BASE_URL`. You need these only if you change a prompt or clear
  `cache/llm/`. The original spend was $1.49.

## 2. Restore removed files and environments

```bash
./restore.sh
```

This creates `.venv/` and `.venv_io/`, and downloads the files the manifest deletes after the round:
* the OpenAlex concept parquet and legacy JSON snapshots;
* MeSH `desc2026.gz` and `supp2026.gz`;
* the ten Research Fronts PDFs.

## 3. Rebuild everything

```bash
./run_all.sh
```

The pipeline runs these steps in order:

| Steps | What they build |
|---|---|
| s0 | concept frame |
| s2, s3b, s3 | Wikidata, Wikipedia page ids, Wikipedia first revisions |
| s4 | MeSH |
| s5 | taxonomies |
| s6b, s6 | curated lists and Research Fronts |
| s1 | field crosswalk (manual resolutions in `scripts/crosswalk_manual.json`) |
| s7 | keys, candidates, LLM verification, list re-verification |
| s8 | assembly and QC asserts |
| `hand_check.py` | merges the executor's verdicts |
| s9 | reports |
| s10 | `sources.json` |
| `uv run data.py` | the exp_sel_data_out files |
| `fill_readme.py` | README numbers |

The network steps (Wikidata, Wikipedia) resume from `cache/` and fetch only what is missing. To reproduce the exact
2026-09-28 numbers, keep `cache/wikidata/`, `cache/wikipedia/` and `cache/llm/` as shipped. The Wikipedia fetcher
`scripts/s3_wikipedia.py` can be left running longer to replace page-id estimates with exact first revisions.

## 4. Build only the deliverable files from existing intermediates

```bash
cd scripts && ../.venv/bin/python s8_assemble.py && cd .. && uv run data.py
```

`uv run data.py` writes the following:
* `full_data_out/full_data_out_{1,2,3}.json`: `full_data_out.json` is split because it is larger than 95 MB.
* `mini_data_out.json` and `preview_data_out.json`.

## 5. Validate

```bash
SKILL_DIR=../../../tools/aii-json   # or your copy of the aii-json validator
for f in full_data_out/full_data_out_*.json mini_data_out.json preview_data_out.json; do
  $SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_sel_data_out --file "$PWD/$f"
done
```

Expected results:
* 10 datasets, 159,730 examples in total, of which 65,026 are concept rows.
* All known-answer checks in `out/qc_checks.json` are true.

## 6. Sources of non-determinism

* The OpenAlex S3 snapshots and Wikidata claims change over time. The sha256 of every file used is in
  `out/sources.json`.
* The Wikipedia page-id calibration depends on how many exact first revisions were fetched (6,540 here).
* LLM verdicts are deterministic only through the cache (temperature 0, but providers are not bit-stable).
