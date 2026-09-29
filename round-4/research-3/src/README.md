# Is "keep exploring, spread widest" new? (iteration-4 novelty and positioning research)

This is a web-only literature check for the Applied Network Science paper on emerging scientific concepts. It asks whether the Exp8 result has already been shown or contradicted by prior work. The result: concepts whose first three years keep an *open* co-occurrence neighbourhood (new partners, many communities, low closure, low edge persistence, low retention of contacted fields) later spread to more fields, whereas early consolidation does not.

**Main answer.** C1 (openness → breadth) is partially anticipated at other units (pairs, papers, memes, people). C2 (consolidation → less breadth) is contradicted by concept- and field-level work on *volume* and *survival*: Cheng et al. 2023 and Chavalarias & Cointet 2013. We recommend framing it as an outcome-dependent reversal. C3 (low retention of contacted fields) and C4 (closure precedes an entry slowdown) are new.

## Layout

| Path | What it is |
|---|---|
| `research_report.md` | Full report, Sections 0 and A-I: our-numbers card, verdict table, strand extraction tables, Cheng operationalisation box, T-RQ1/T-RQ2 comparison tables, ANS papers, 8-lane Fig. 1 spec, reviewer-threat table, verified and UNVERIFIED references, design gaps |
| `research_out.json` | Structured result (answer, 80 sources with checked quotes, follow-up questions); saved by the pipeline |
| `reproducibility.md` | How the research was actually run (tools, order, failures) |
| `raw/query_log.tsv` | Every search/fetch/grep call with UTC timestamp |
| `raw/search/*.txt`, `raw/fetch/*.txt` | Saved search results and page/PDF extracts (the quote evidence) |
| `raw/verify.json`, `raw/s2_batch.json` | Crossref/arXiv/Semantic Scholar verification dumps |
| `scripts/ws.sh`, `scripts/wf.sh` | Wrappers around the aii-web-tools search and fetch/grep scripts |
| `scripts/verify_refs.py`, `scripts/s2_batch.py` | Reference verification |
| `scripts/build_output.py`, `scripts/answer.md`, `scripts/summary.md` | Assemble the structured output and check quotes |

## How to run

```bash
PY=/ai-inventor/.claude/skills/.ability_client_venv/bin/python   # any Python 3 with `requests`
$PY scripts/verify_refs.py          # re-verify DOIs/arXiv IDs -> raw/verify.json
python3 scripts/build_output.py     # rebuild structured output; fails if any quote is not in raw/fetch
```

The search/fetch wrappers require the aii-web-tools skill (the ability server).

## Restoring removed files

Nothing is marked for deletion. The workspace holds only text (about 8 MB, mostly the raw page extracts), and all of it is kept. `.aii/manifest.yaml` therefore lists no entries.
