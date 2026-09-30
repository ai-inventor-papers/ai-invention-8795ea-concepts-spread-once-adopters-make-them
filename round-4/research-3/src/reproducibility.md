# Reproducibility: how this research was actually conducted

**Date.** 2026-09-29, about 02:14-02:45 UTC, in one session.

**Tools.**
- **aii-web-tools skill scripts**, called through two small wrappers:
  - `scripts/ws.sh` (search) calls `aii_fast_web_search.py` in `--mode general` (ddgs/marginalia, Serper fallback) or `--mode scholarly` (OpenAlex/Crossref).
  - `scripts/wf.sh` (fetch / grep) calls `aii_fast_web_fetch.py fetch|grep`.
  The wrappers append every call to `raw/query_log.tsv` (UTC timestamp, tool, tag, URL/query, pattern) and save output to `raw/search/<tag>.txt` or `raw/fetch/<tag>.txt`.
- **Built-in WebSearch/WebFetch** were not used.
- **Bibliographic APIs** were called directly from two scripts in the skill's Python venv (`requests`):
  - `scripts/verify_refs.py`: Crossref `/works/{doi}` for 60 DOIs and the arXiv export API for 7 IDs, written to `raw/verify.json`.
  - `scripts/s2_batch.py`: one Semantic Scholar `/paper/batch` POST for 20 abstracts, plus 4 Crossref bibliographic queries to correct wrong DOIs, written to `raw/s2_batch.json`.
- **Env vars / keys.** None were set by us. The skill scripts may use `SERPER_API_KEY` as a fallback; its value was not read or recorded. **The OpenAlex API key in the task text was NOT used.** The plan required $0 spend, and the two anonymous OpenAlex calls returned HTTP 429. The Semantic Scholar search endpoint also returned 429 (5 calls). The batch endpoint worked.

**Inputs read (internal, not web).**
- Prior reports:
  - `iter_3/gen_art/gen_art_research_2/research_report.md` (art_EesdB8cuSfcU)
  - `iter_2/gen_art/gen_art_research_1/research_report.md` and `research_out.json` (art_dxvRpQufMR0e)
- Exp8 results (`iter_3/gen_art/gen_art_experiment_8/results/`): `heldout_summary.json`, `prereg_verdicts.json`, `portability_table.csv`, `learned_vs_single_heldout.json`, `rq1_heldout.json`, `indicator_dictionary.csv`, `case_exemplars.json`, `provenance.json`.

## Order of work (as run)

1. **Intake.** Read both prior reports and Exp8 files; built the our-numbers card (report, Section 0).
2. **Batch 1 (02:16).** Cheng et al. 2023: Semantic Scholar record plus a grep of the Sage full-text HTML (`journals.sagepub.com/doi/full/10.1177/00031224231166955`). The page was openly readable, 231k characters. Also 12 strand searches (S1-S9, C3). Scholarly mode (Crossref backend) returned mostly irrelevant hits, so later searches used general mode.
3. **Cheng deep read (02:17-02:19).** Four greps for method terms (Jaccard / cosine / neighbour terms / dependent variable / bridging), then two offset fetches (char-offset 83,200 and 95,000) for Tables 4-5, the results text and the limitations.
4. **Batch 2 (02:19).** Anchor papers fetched or grepped:
   - Palla 2007 (arXiv PDF)
   - Ugander 2012 (PNAS HTML)
   - Wang et al. 2017 (NBER w22180 PDF)
   - Salatino 2017 (PeerJ PDF)
   - Cobo 2011 (sci2s PDF)
   - Aria 2026 (arXiv abs)
   - Maillart 2026 (arXiv PDF)
   - Chavalarias & Cointet 2013 (PLOS HTML)
   - Leydesdorff & Rafols (arXiv PDF)
   - Fang & Evans (arXiv abs)
   - Ravasz & Barabási (arXiv PDF)

   General searches g1-g6 ran alongside.
5. **Targeted greps (02:21).** Chavalarias density-survival passages, Maillart Table 2 numbers. One wrong arXiv ID (1110.3000) returned an unrelated paper, which was ignored. Chen 2012 was taken from the author's Drexel PDF instead.
6. **Batch 3 (02:22).**
   - Fetches: Chen 2012 PDF, Shi & Evans (Nature), Hofstra (PNAS), Foster (arXiv abs), Huang 2021 (ScienceDirect preview), Kong 2025 (S2 API).
   - Failures: a wrong Iacopini arXiv ID (1708.03144 is unrelated; resolved via Crossref instead); S2 search calls hit 429.
   - Searches: methods-vs-theories, GPT generality, C3, C4.
7. **Batch 4 (02:23).** Prabhakaran 2016 (ACL PDF), Singh 2022 (PLOS), Stewart 2017 (arXiv), Krauss 2026 (arXiv), Petralia (PEEG PDF), Hall & Trajtenberg (NBER w10901), Kong (arXiv PDF), Romero 2011 (Cornell PDF).
8. **Batch 5-6 (02:24-02:26).** Direct-precedent hunt (queries p1-p8).
   - Candidates checked: Cao et al. 2020 (ACL Anthology PDF, grepped twice); Osborne et al. 2017 (the ORO PDF gave 403, so the abstract came via S2 batch and the TTF page); McKeown 2016 (503, not read).
   - Vilhena 2014: the page gave 406, so the abstract came via S2 batch.
9. **Verification (02:27-02:38).** `verify_refs.py` resolved 66/67 identifiers. `s2_batch.py` fetched abstracts and fixed the Moser & Nicholas, Feldman & Yoon, Coulter and Chen 2009 DOIs. The Vincenot 2018 abstract came via the Crossref API. The Bettencourt 2009 pages were checked with curl on Crossref.
10. **Write-up (02:38-02:45).** `research_report.md` was written by hand from the raw extracts. `scripts/build_output.py` assembles the structured output. It **checks every supporting quote against the saved raw text** (whitespace-normalised) and fails otherwise; 3 file-mapping errors were caught and fixed. It also checks that every `[n]` in the answer resolves.

## How to retrace

- Re-run the queries in `raw/query_log.tsv`, in order, with the same skill scripts.
- Re-fetch the URLs listed there. Most are stable open-access pages; Sage served the Cheng full text openly on 2026-09-29, but this may change.
- `python scripts/verify_refs.py` reproduces the DOI checks.
- `python scripts/build_output.py` rebuilds the JSON from `scripts/answer.md` and `scripts/summary.md` and re-checks the quotes.
- Search-engine rankings drift, so the landscape conclusions rest on the fetched primary texts in `raw/fetch/`, not on snippets.

## Known limitations of this run

- **Not read in full:** McKeown et al. 2016 (503); Osborne 2017 full text (403); the Salatino p-values (PeerJ 403 on the second fetch); Vincenot and Vilhena full texts (403/406; abstracts only); the three method-entity arXiv papers named in the plan (not fetched); Van Noorden 2014 (not checked).
- **No new ANS sweep:** the OpenAlex sweep of ANS was rate-limited, so the ANS list is carried from art_dxvRpQufMR0e.
- **Not searched for C3:** marketing churn and epidemiology.
