# Where our results sit among related papers (ANS positioning study)

A web-only literature and positioning study for an Applied Network Science (ANS) paper on emerging scientific concepts in evolving knowledge networks. The paper targets the collection "Networks for everyday life".

## What was done

- Tried to recover the collection's article list. It could not be recovered: Springer, PMC and Wayback are all JS- or IdP-blocked. The failed routes are documented.
- Swept ANS (22 citable papers) and four neighbour journals through the anonymous OpenAlex API.
- Extracted comparison numbers (AUC, R², precision, splits, base rates) from primary sources:
  - relatedness entry/exit work;
  - the research space;
  - concept-pair forecasting (Krenn; Maillart et al. preprints);
  - virality (Weng et al.);
  - idea diffusion (Cheng et al.).
- Ran a novelty check on the "gateway centrality → retention" claim against:
  - economic-complexity exit and survival work;
  - metapopulation analogies from cultural evolution;
  - betweenness and interdisciplinarity work.
- Inferred the ANS article template from 8 ANS articles from 2024–2026 (Europe PMC JATS XML).
- Verified about 95 references via Crossref, OpenAlex and arXiv, and fixed 12 misattributions or wrong DOIs.

## Layout

| Path | Content |
|---|---|
| `research_report.md` | Main deliverable, sections A–F: collection, related work, T2 comparison table, novelty verdict, ANS template, verified references and corrections |
| `research_out.json` | Structured answer with numbered citations (auto-saved from the final output) |
| `reproducibility.md` | Exact queries, URLs, order and tools used |
| `raw/openalex/` | OpenAlex query results (ANS q1–q15, neighbours n1–n6, ANS 2025–26 list, 30 ANS abstracts) |
| `raw/crossref/` | DOI lists and Crossref verification output (`xref1.json`) |
| `raw/greps/` | Regex-grep outputs from arXiv, PeerJ and Europe PMC full texts, plus arXiv abstract pages |
| `raw/ans_template/` | Europe PMC ANS listing and parsed structure of 8 ANS articles |
| `scripts/` | `xref.py` (DOI → Crossref), `xq.py` / `xq2.py` (bibliographic Crossref lookups), `abs.py` (OpenAlex abstracts by DOI) |

## How to run

The scripts need Python 3 (standard library only) and network access. Examples:

```bash
python3 scripts/xref.py raw/crossref/dois1.txt /tmp/xref_check.json
python3 scripts/xq2.py raw/crossref/q2.txt
cd raw/openalex && python3 ../../scripts/abs.py "10.1007/s41109-024-00618-2|10.1007/s41109-016-0017-9"
```

## Restoring removed files

Nothing is marked `delete` in `.aii/manifest.yaml`. The workspace holds only small text and JSON files (about 5 MB).
