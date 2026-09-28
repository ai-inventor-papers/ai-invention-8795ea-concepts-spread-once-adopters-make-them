#!/usr/bin/env bash
# Rebuild everything from the cached downloads (run ./restore.sh first on a fresh clone).
# Network steps (s2, s3, s3b) resume from cache/ and only fetch what is missing.
# LLM steps (s1, s7_verify, s7d) reuse cache/llm/calls.jsonl, so a rerun costs nothing unless prompts change.
set -euo pipefail
cd "$(dirname "$0")/scripts"
PY=../.venv/bin/python
$PY s0_concepts.py            # concept frame (OpenAlex S3 parquet + legacy JSON ancestors)
$PY s2_wikidata.py            # Wikidata claims (resumable)
$PY s3b_pageids.py            # Wikipedia page ids, 50 titles per call (resumable)
$PY s3_wikipedia.py 4 0 4     # Wikipedia first revisions, paced (resumable; slow under IP throttling)
$PY s4_mesh.py                # MeSH descriptors
$PY s5_taxonomies.py          # ACM/MSC/PACS/PhySH/JEL nodes
$PY s6b_research_fronts.py    # Research Fronts 2017-2025 tables from the CAS-ISD PDFs
$PY s6_lists.py               # curated yearly lists (+ Research Fronts, Physics World 2025)
$PY s1_crosswalk.py && $PY s1_crosswalk.py --finalize   # level-1 -> field crosswalk (manual file: scripts/crosswalk_manual.json)
$PY s7_keys.py                # join keys
$PY s7_candidates.py          # writes work/p486_not_in_desc.csv, candidates
$PY s4b_mesh_supp.py          # SCRs for P486 C-numbers (needs p486_not_in_desc.csv)
$PY s7_candidates.py          # rerun so SCR entries are included
$PY s7_verify.py run          # LLM verification, audits, double labels
$PY s7_verify.py alias        # LLM verification of alias-only / MeSH label-only exact matches
$PY s7d_lists_v2.py           # stricter list re-verification (gpt-4.1-mini)
$PY s8_assemble.py            # events, absence flags, provisional fold, QC asserts
$PY hand_check.py             # merges the executor's hand verdicts, agreement stats
$PY s9_outputs.py             # coverage report, P78 spot check, data_out parts, mini, preview
$PY s10_provenance.py         # sources.json
cd .. && uv run data.py && cd scripts   # the exp_sel_data_out deliverables (parts + mini + preview)
$PY fill_readme.py            # README.md numbers from the final outputs
