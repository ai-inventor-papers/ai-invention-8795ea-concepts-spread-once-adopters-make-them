# Reproducibility: how this research was actually conducted

- **Date:** 2026-09-28, roughly 17:07–17:40 UTC.
- **Tools:**
  - aii-web-tools skill: built-in `WebSearch` / `WebFetch`, plus the skill scripts `aii_fast_web_search.py` and `aii_fast_web_fetch.py grep`.
  - Plain `curl` / Python `urllib` against the free JSON APIs: OpenAlex, Crossref, Europe PMC, and the arXiv export API (which failed).
- **API keys:** none were used. The run's OpenAlex key was deliberately **not** used, per the plan. All OpenAlex calls were anonymous, about 40 in total.
- **Environment variables:** none needed. The aii-web-tools scripts use the skill's pre-provisioned interpreter (the `.ability_client_venv` next to the skill directory).
- **Cost:** no LLM or OpenRouter calls were made (cost $0).

## 1. Target collection (Step 1): order of attempts

1. `WebFetch https://link.springer.com/collections/fgcaicgjah` returned a 303 redirect to `idp.springer.com/authorize`.
2. The same fetch with `WebSearch` queries run in parallel:
   - `"Networks for everyday life" "Applied Network Science" collection`
   - `"Part of a collection" "Networks for everyday life" s41109`

   These returned only the landing page. Its snippets gave the call text.
3. `aii_fast_web_fetch.py fetch --url https://link.springer.com/collections/fgcaicgjah` returned a "JavaScript is disabled" page.
4. `curl` with a Chrome user-agent and a cookie jar returned HTTP 200, but the body was a 3 KB JS-challenge page. No DOIs were found in it.
5. More WebSearch queries:
   - `Applied Network Science "Networks for everyday life" guest editors call for papers deadline`
   - `"Networks for everyday life" Applied Network Science 2025 article`
   - `link.springer.com article 10.1007/s41109-025 "Networks for everyday life"`
   - `"Networks for everyday life" friendship paradox OR "partisan animosity" OR "temporal network generation" ...`
   - `"Networks for everyday life" special collection network science health mobility education politics editors`
6. `aii_fast_web_search.py` (ddgs) with 3 phrasings. Each returned only the landing page.
7. Wayback Machine:
   - The CDX API for `link.springer.com/collections/fgcaicgjah*` returned `[]`.
   - The 2025-09-28 snapshot of `/journal/41109/collections` was a JS shell.
8. **Conclusion:** the collection list is not recoverable by any route.

Along the way, `https://pmc.ncbi.nlm.nih.gov/articles/PMC12018473/` was blocked by reCAPTCHA. It was read through the Europe PMC REST API instead:
`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12018473/fullTextXML`. It turned out to be a Frontiers editorial ("Science of science: a complex network perspective"), not ANS.

## 2. ANS and neighbour sweep (Step 2)

**ANS queries.** Each call was

```
https://api.openalex.org/works?filter=primary_location.source.id:S3035517252,title_and_abstract.search:<Q>&select=id,doi,title,publication_year,cited_by_count&per_page=100&sort=cited_by_count:desc
```

The `<Q>` values, stored as `raw/openalex/q1..q15.json`:

| File | Query |
|---|---|
| q1 | `(emerging OR emergence) AND (topic OR concept OR technology OR field)` |
| q2 | `interdisciplinary OR interdisciplinarity OR disciplines` |
| q3 | `"knowledge flow" OR "knowledge diffusion" OR "knowledge transfer" OR "knowledge flows"` |
| q4 | `"citation network" OR "citation networks"` |
| q5 | `"science of science" OR scientometric OR bibliometric OR scientometrics` |
| q6 | `relatedness OR "product space" OR "economic complexity" OR diversification` |
| q7 | `"complex contagion" OR cascade OR virality OR "information diffusion"` |
| q8 | `"temporal network" AND ("community evolution" OR alluvial OR "evolving communities")` |
| q9 | `metapopulation OR "rescue effect" OR "source-sink"` |
| q10 | `("core-periphery" OR "eigenvector centrality") AND (diffusion OR persistence OR survival)` |
| q11 | `("co-occurrence" OR keyword OR concept) AND ("link prediction" OR forecasting OR prediction)` |
| q12 | `patent OR patents OR innovation` |
| q13 | `"research topics" OR "scientific fields" OR "research fields" OR "topic evolution"` |
| q14 | `"keyword" OR "co-word" OR "co-occurrence network"` |
| q15 | `"threshold model" OR "adoption" AND (spread OR diffusion)` |

**Other ANS calls:**

- All ANS works from 2025–2026: `filter=primary_location.source.id:S3035517252,publication_year:2025-2026` (143 works), stored as `raw/openalex/y2526.json`.
- Abstracts of 30 ANS papers in one call with `filter=doi:<30 DOIs joined by |>` and `select=...,abstract_inverted_index`, stored as `raw/openalex/ans_abstracts.json`.

**Neighbour journals.**

- Source ids came from `/sources?search=`: EPJ Data Science S2504380752, Scientometrics S148561398, QSS S4210195326, J. Informetrics S205292342.
- Queries are stored as `raw/openalex/n1..n6.json`.
- The first attempts at n2–n4 hit OpenAlex's anonymous rate limit for more than 5 boolean operators. They were re-run with fewer operators and a 2 s sleep.

**Misattributed item.** "Knowledge transfer, knowledge gaps, and knowledge silos …" (PMC12316298) was checked with Europe PMC `search?query=PMCID:PMC12316298`. Result: PLoS ONE 2025, Cunningham & Greene.

## 3. Comparison numbers (Step 3): documents grepped with `aii_fast_web_fetch.py grep`

Outputs are in `raw/greps/`.

| Document | Regex used | What it gave |
|---|---|---|
| `https://arxiv.org/pdf/1602.08409` (Guevara 2016) | `AUC\|area under\|ROC\|precision`, then `exit\|abandon\|leave\|persist` | Entry AUCs; confirmed there is no exit analysis |
| `https://oec.world/pdf/Hidalgo2018_Chapter_ThePrincipleOfRelatedness.pdf` | entry/exit, core | Entry/exit statements |
| `https://arxiv.org/pdf/0708.2090` (Hidalgo 2007) | core-periphery, jumps | Core-periphery claims |
| `https://arxiv.org/pdf/2205.02942` (Li & Neffke) | — | — |
| `https://arxiv.org/pdf/1801.05352` (Pinheiro et al. 2018 preprint) | — | — |
| `https://arxiv.org/pdf/2606.03864` and `https://arxiv.org/pdf/2606.03919` (Maillart et al.) | AUC / R² / split / Table | AUC, R², split design and the "within-domain replications" sentence |
| `https://arxiv.org/pdf/2210.00881` (Krenn 2023) | — | Data sizes and ~1–3% positives. Per-model AUCs appear only in a figure. |
| `https://arxiv.org/pdf/2402.08640` (Gu & Krenn) | — | "AUC values beyond 0.9 for most experiments" |
| `https://arxiv.org/pdf/1306.0158` (Weng 2013) | — | Precision and recall relative to baselines; n = 50 early tweets |
| `https://peerj.com/articles/cs-119.pdf` (Salatino 2017) | — | — |
| `https://arxiv.org/pdf/2310.01046` (Fontaine 2024) | — | — |
| `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7374558/fullTextXML` (Sun & Latora 2020) | — | — |
| `https://arxiv.org/pdf/2002.06419` (Tripodi 2020) | — | — |

**Wrong arXiv ids.** Two ids I guessed (1808.07496, 2101.07794) pointed to unrelated papers. Their outputs were discarded, and the correct sources were found by WebSearch.

**Paywalled or JS-blocked pages:**

- Blocked: Wiley (twec.12835: 403), IOPscience (bot manager), nature.com (IdP redirect), and the epjdatascience PDF (JS).
- Their abstracts were read through OpenAlex `abstract_inverted_index` instead, using `scripts/abs.py`.

**Our own numbers** were re-read, read-only, from `round-1/experiment-4/src/full_method_out.json` (keys `gateway_j`, `size_controlled_gateway_j`, `phi_home_j`, `all`).

## 4. Novelty check (Step 4): WebSearch queries, in order

1. `export survival product space centrality relatedness density survival of new exports` → Goya & Zahler 2019; Yenilmez 2026
2. `metapopulation model persistence of scientific fields OR ideas OR knowledge rescue effect` → ecology only
3. `cultural evolution population connectivity metapopulation loss of cultural traits persistence model` → Premo line, Rapa Nui
4. `"source-sink" OR "island biogeography" scientific disciplines knowledge ideas persistence citation` → ecology only
5. `colonization extinction dynamics research topics scientific fields ecological model "extinction" of topics citation network persistence` → ecology only
6. `regional network centrality predicts survival of new technological specialization beyond relatedness density` → Tóth 2022; Lee 2025
7. `"gateway" OR "broker" disciplines relay knowledge diffusion across fields citation network betweenness interdisciplinary hub` → Cunningham & Greene; Yu 2025
8. `Premo 2010 "local extinctions" cultural metapopulation PLOS One Paleolithic Levins model culture` → Premo & Kuhn 2010; Premo 2012; Hopkinson 2011
9. `diffusion of AI within and across scientific fields persistence adoption fields arXiv 2024 "Oil & water"` → Duede 2024
10. `cross-disciplinary concept adoption persistence "sustained" adoption field network position ...` → Macasaet & Powell 2026; Zhu 2026
11. `"research space" relatedness exit of research fields countries scientific diversification entry exit "principle of relatedness" science` → Tripodi 2020; Galán-Mena 2026

Abstracts for the hits were then fetched through OpenAlex (`scripts/abs.py "<doi1>|<doi2>|..."`).

## 5. ANS template (Step 5)

1. **Article list.** Europe PMC search:
   `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=JOURNAL:"Appl Netw Sci" AND (PUB_YEAR:2024 OR PUB_YEAR:2025 OR PUB_YEAR:2026)&format=json&resultType=lite&pageSize=200` returned 14 hits.
2. **Full text.** JATS XML for 8 of them, from `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`.
3. **Parsing.** From each XML I extracted: section titles, abstract and body word counts, keywords, figures, tables, references, the back-matter order, the data-availability text and the competing-interests text. Output: `raw/ans_template/ans_article_structure.json`.
4. **Official guidelines.**
   - WebFetch of the springeropen research-article guideline page returned a 301 redirect to link.springer.com (Springer IdP).
   - Two WebSearch queries gave snippets only: keywords "three to ten", the "Availability of data and materials" requirement, and the APC.

## 6. DOI verification (Step 6)

- **DOI list.** `scripts/xref.py raw/crossref/dois1.txt` queries `https://api.crossref.org/works/<DOI>` for 70 DOIs, 6 threads in parallel. Output: `raw/crossref/xref1.json`.
- **Unknown or failed DOIs.** Resolved with `query.bibliographic`:
  - `scripts/xq.py raw/crossref/q1.txt` (parallel; several calls hit HTTP 429).
  - `scripts/xq2.py raw/crossref/q2.txt` (sequential, 1.5 s sleep).
- **arXiv ids.** The `export.arxiv.org` API returned empty bodies, so ids were verified by fetching `https://arxiv.org/abs/<id>` with the skill fetch script.
- **SSRN 7276909.** Verified through a WebSearch result naming the page title.

## How to retrace

1. Re-run the OpenAlex URLs above (anonymous, fewer than 5 boolean operators per query or 1 request/s).
2. Re-run the Crossref checks with `python3 scripts/xref.py raw/crossref/dois1.txt out.json`.
3. Re-run the greps with the aii-web-tools `grep` subcommand on the listed PDFs.

Expect drift in these places:

- Search-engine results.
- OpenAlex citation counts.
- The Springer collection page. If it becomes fetchable (for example from a logged-in browser), the T1 gap can be closed directly.
