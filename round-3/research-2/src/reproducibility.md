# Reproducibility: how this research was actually conducted

- Date: 2026-09-28, all web access between about 21:30 and 23:30 UTC.
- Executor: Claude Code (Opus 5.5), following the aii-web-tools skill.
- Tools used:
  - (1) the built-in **WebSearch** and **WebFetch** tools, which the skill says to prefer;
  - (2) the skill's scripts `aii_fast_web_search.py` (scholarly mode) and `aii_fast_web_fetch.py grep` (regex grep over full HTML/PDF);
  - (3) plain anonymous `curl` GETs to open REST APIs (Europe PMC, Crossref, arXiv export API, Semantic Scholar Graph API, OpenAlex).
- Wrappers: `scripts/s.sh` (search), `scripts/f.sh` (fetch) and `scripts/g.sh` (grep). Each saves output to `raw/search/`, `raw/fetch/` or `raw/greps/` under the name given as its first argument.
- API keys / env vars: **none were used.** The OpenAlex key in the user's request was deliberately NOT used, as the plan instructed. No OpenRouter/LLM calls were made. The skill scripts call the pipeline's ability server; its credentials, if any, are handled inside the skill and were not read.

## 0. Local inputs (no web)
- `round-2/research-1/src/research_report.md` (art_dxvRpQufMR0e): prior 22 ANS papers, ~95 references, template, corrections.
- `round-2/experiment-6/src/results/heldout_result.json` (art_N-mpomDZZ1ln): the Exp6 held-out numbers used in the "ours" column.

## 1. Searches, in the order run

1. Scholarly mode (`s.sh q1..q9`, OpenAlex+Crossref), all nine run in parallel. They returned citation-ranked **off-topic** results and were abandoned for discovery:
   - "relatedness density persistence comparative advantage entry"
   - "lost comparative advantage neighbours entry probability"
   - "exit of related industries effect on entry region"
   - "duration-weighted relatedness density"
   - "RCA consecutive years entry definition relatedness"
   - "neighbour export failure deters entry"
   - "failed introduction predicts invasion failure similar habitat"
   - "topic abandonment field adoption diffusion scientometrics"
   - "concept adoption field retention persistence spread science"
2. WebSearch:
   - relatedness density "lost" comparative advantage neighbors predicts entry exit product space
   - "relatedness density" persistence weighted "consecutive years" RCA entry definition diversification
   - Fernandes Tang "Learning to export from neighbors" neighbors' failure exit negative signal
   - Bahar Hausmann Hidalgo "Neighbors and the evolution of the comparative advantage of nations" pdf
   - "Follow thy neighbor" role of first exporters Journal of Urban Economics 2025
   - Rigby 2015 "Technological relatedness and knowledge space" entry and exit US cities patent classes pdf
3. WebSearch:
   - Fernandes Tang learning from neighbors export pdf "number of neighbors" "exit" World Bank working paper Chinese exporters
   - Jun Alshamsi Gao Hidalgo "Bilateral relatedness" arXiv
   - Aleta Meloni Perra Moreno "Explore with caution" … EPJ Data Science
   - export entry "neighbors' exit" OR "exit of neighboring firms" OR "failed exporters" discourage entry …
   - "loss of comparative advantage" related products neighbors "relatedness" regions lose specializations …
4. WebSearch:
   - relatedness density "time-weighted" OR "duration" OR "tenure" of specializations …
   - "re-entry" OR "dormant" comparative advantage previously lost products …
   - arXiv Chinazzi … "Mapping the physics research space…"
   - Cheng Evans 2023 ASR "how new ideas diffuse in science" …
5. WebSearch:
   - Richardson … "Naturalization and invasion of alien plants" pdf
   - Blackburn 2011 unified framework pdf
   - Lockwood 2005 propagule pressure pdf
   - Pyšek Jarošík 2005 residence time pdf
   - plant closure "related industries" entry …
6. WebSearch:
   - "Evolution of research portfolios of universities" EPJ Data Science 2026 …
   - scientific concept diffusion across fields "retention" …
   - Rigby 2015 … "relatedness density" results exit …
7. RQ1 WebSearch: Xu 2021 TFSC 120366; Liang 2021 IP&M 102611; Behrouzi 2020 J Informetr 101079; Porter 2019 emergence scoring; "Applied Network Science co-occurrence network emerging topics prediction …".
8. RQ2 / venue WebSearch:
   - research topics life cycle trajectory types clustering …
   - "Networks for everyday life" Applied Network Science collection guest editors
   - "Networks for everyday life" … "innovation and collaboration networks" "information diffusion". This produced the deadline and scope snippets.
9. Contrarian WebSearch:
   - "short-lived" OR "temporary" OR "failed" specializations relatedness density …
   - country research field entry "principle of relatedness" science "exit" …
   - "The time and frequency of unrelated diversification" … pdf

## 2. Pages / PDFs actually read (grep or fetch; outputs in raw/)

Economic complexity and relatedness:
- arxiv.org/pdf/0708.2090 (Hidalgo 2007)
- hks.harvard.edu … faculty-working-papers/146.pdf (Hausmann & Klinger 2007)
- econ.geo.uu.nl/peeg/peeg0916.pdf (Neffke 2011)
- scholar.harvard.edu/files/dbaharc/files/bhh-jie.pdf (Bahar 2014)
- oec.world/pdf/bilateral-relatedness-…pdf (Jun 2020)
- arxiv.org/pdf/1801.05352 and run.unl.pt/bitstreams/e0c3b563-…/download (Pinheiro 2018 WP / 2022 OA)
- nature.com/articles/s41598-023-28179-x (Albora 2023)
- arxiv.org/pdf/2205.02942 (Li & Neffke)
- arxiv.org/pdf/2203.16316 (Nomaler & Verspagen)
- nature.com/articles/s41467-021-21689-0 (O'Clery 2021)
- arxiv.org/pdf/2104.10812 (Miao et al.)
- arxiv.org/pdf/2407.13880 (software complexity, not used)
- econpapers.repec.org Rigby abstract

Export learning:
- dallasfed.org/…/2014/0185.pdf (Fernandes & Tang)
- nber.org/…/w8952.pdf (Hausmann & Rodrik)
- afse2017.sciencesconf.org/142849/HAZIR_BELLONE_GAGLIO.pdf

Ecology:
- ibot.cas.cz/personal/pysek/pdf/naturalization_and_invasion_%20of_alien_plants.pdf (Richardson 2000)
- Europe PMC abstracts for Blackburn 2011 and Lockwood 2005. The ResearchGate PDF of Blackburn returned 403.

Science:
- Europe PMC full-text XML: PMC7302634 (Palmucci), PMC7971485 (Galuppo Azevedo), PMC3545262 (Sun 2013), PMC7374558 (Sun & Latora), PMC9673898 (Cunningham; structure parsed by `scripts/pmc_struct.py`)
- journals.sagepub.com Cheng 2023 abstract
- arxiv.org/pdf/1906.06843 (Krenn & Zeilinger)
- sciencedirect Small 2014 abstract page
- arXiv PDFs 2310.01046 (Fontaine) and 2303.00622 (Holmgren), downloaded to `raw/arxiv_pdf/` and parsed with PyMuPDF
- arxiv.org/pdf/1604.00696, 1011.3120 and 2405.15828

Failed:
- par.nsf.gov (Porter): connection error.
- sciencedirect Liang 2021: 403.
- tandfonline Rigby/Balland: 403.
- EPJDS/Springer article pages: IdP 303.
- Springer content/pdf: anti-bot challenge, not circumvented.
- econ.geo.uu.nl PEEG 1316: SSL error.

## 3. Venue routes
All attempted on 2026-09-28. Results are in `raw/greps/v_*.txt` and `raw/venue/`.
- link.springer.com/collections/fgcaicgjah
- link.springer.com/journal/41109/collections
- appliednetsci.springeropen.com/articles/collections
- Europe PMC `search?query="Networks for everyday life"`
- Crossref `works?query="Networks+for+everyday+life"&filter=issn:2364-8228`
- Wayback CDX

Only search-engine snippets gave content.

## 4. Verification
- `python3 scripts/xref.py <DOIs>` → `raw/crossref/verified.jsonl`, `batch1.log`, `batch2.log`. It uses anonymous Crossref with retry/backoff, because a first unthrottled run hit HTTP 429.
- arXiv: `export.arxiv.org/api/query?id_list=…` → `raw/arxiv_api.xml`.
- Semantic Scholar Graph API for abstracts → `raw/s2/`.
- OpenAlex anonymous query of ANS (source S3035517252) for emergence and sci-sci papers → `raw/openalex/`.

## 5. How to retrace
1. Run the WebSearch queries in section 1. Results drift over time; the snippet facts about the collection are dated 2026-09-28.
2. Re-run the greps with `scripts/g.sh <name> <url> <regex>`. The patterns used are recorded in the first lines of each `raw/greps/*.txt`.
3. Re-verify DOIs with `scripts/xref.py`.

The verdicts depend mainly on these files:
- `pinheiro2022_oa2.txt`
- `albora2.txt`
- `bahar2.txt` / `bahar3.txt`
- `fertang.txt` / `fertang2.txt`
- `nv_E.txt`
- `hid2007_rca.txt`
- `hk146b.txt`
- `latent_exit.txt`
- `raw/epmc/PMC7971485.txt`
