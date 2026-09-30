# When concepts were officially recognised

A lookup table of **external, dated recognition events** for all 65,026 OpenAlex legacy concepts. Recognition here
means a controlled vocabulary, taxonomy, encyclopaedia or curated list taking up the concept, and every event has a
year. The table is built from sources that do not depend on publication counts, so it can supply the outcome
**O5 (external recognition)** and the recognised/persistent split for the emergence study. It was built with
**zero OpenAlex API credits** (public S3 snapshot only) and **$1.49 of OpenRouter LLM calls** (cap $2).

The table holds **raw events only**. It has no O5 flags, no lags relative to an onset year t0 and no correlations;
the panel builder derives those. Facts known only today are kept in a separate `present_day` block
(`year_known=false`), so nothing here turns present-day existence into recognition.

<!-- NUMBERS -->
**At a glance (levels 2–5, 64,723 target concepts; `out/coverage_report.json` has the full breakdown):**

| Source | Concepts with ≥1 event | Event types | Year resolution |
|---|---|---|---|
| English Wikipedia | 64,363 (exact first revision for 6,540 titles; page-id estimate for the rest) | `wikipedia_article_created`, `wikipedia_page_created_estimated` | day / estimated |
| MeSH 2026 (NLM) | 20,872 | `mesh_descriptor_introduced`, `mesh_supplementary_record_introduced` | year |
| PACS 2010 / PhySH | 2,635 | `taxonomy_in_version`, `taxonomy_added_between` | version year |
| ACM CCS 1998 / 2012 | 1,298 | same | version year |
| MSC 2000 / 2010 / 2020 | 1,121 | same | version year |
| Wikidata P571 / P575 | 1,425 | `wikidata_inception`, `wikidata_discovery_or_invention` | Wikidata precision |
| Gartner Hype Cycle (1995–2025) | 466 | `gartner_hype_cycle_emerging_tech_entry` (+phase) | year |
| MIT TR10 (2001, 2003–2026) | 313 | `mit_tr10_breakthrough_technology` | year |
| Physics World BOTY (2009–2025) | 100 | `physics_world_breakthrough_of_the_year` | year |
| Clarivate/CAS Research Fronts (2017–2025) | 589 | `research_front_listed` (hot / emerging, rank, broad field) | report year |
| Science BOTY (1996–2025) | 53 | `science_breakthrough_of_the_year` | year |
| Nature Methods MoTY (2007–2025) | 38 | `nature_methods_method_of_the_year` | year |
| JEL (AEA) | 213 matched | present-day membership only (undated) | none |

25,884 target concepts have at least one year-usable event from a source other than Wikipedia.

---

## 1. Deliverables

| File | What it is |
|---|---|
| `full_data_out/full_data_out_{1,2,3}.json` | The full dataset in `exp_sel_data_out` format, split into parts of ≤90 MB. Each part is a valid document. Datasets can span parts, so concatenate `examples` that share a `dataset` name. |
| `data.py` | uv inline script (`uv run data.py`): standardises the processed sources into the 10 datasets, writes `full_data_out.json`, splits it into the parts above (95 MB rule), and writes mini/preview. |
| `full_data_out/{mini,preview}_full_data_out_{1,2,3}.json` | Per-part mini/preview variants from the aii-json format script (3 examples per dataset present in that part). |
| `mini_data_out.json` | Up to 200 examples per dataset. Concept rows are stratified by provisional group. |
| `preview_data_out.json` | 10 examples per dataset, strings truncated to 300 characters. |
| `out/coverage_report.json` | Coverage per source × level × level-0 discipline × provisional group: counts, 5-year event histograms, match-method mix, plus the LLM audit/agreement block. |
| `out/sources.json` | URL, version, retrieval date, sha256, licence, record count and notes for all 22 sources, plus 4 attempted-and-not-delivered items. |
| `out/crosswalk_level1_to_field.csv` | The 284 level-1 concepts mapped to the 26 OpenAlex fields (two LLMs, then manual resolution with a reason for each). |
| `out/spotcheck_p78.csv` | Join test against the 78 iteration-1 panel concepts (P78), with their events. |
| `out/hand_check.csv`, `out/hand_check_lists_v2.csv`, `out/hand_check_research_fronts.csv` | The executor's own verdicts on 60 + 30 + 30 LLM decisions. |
| `out/llm_agreement.json` | Audit precision per family and method, inter-model κ, and hand-check accuracy. |
| `out/llm_cost.json` | Running OpenRouter spend per task and model. |
| `out/qc_checks.json` | Results of the hard-asserted known-answer checks. |

### 1.1 Datasets inside `data_out` (10)

| `dataset` | Rows | One row is |
|---|---|---|
| `concept_recognition` | 65,026 | a concept: `input` = join keys, `output` = events + absence flags + present-day block |
| `external_entries_mesh` | 31,830 | every MeSH descriptor (31,110) and the 720 supplementary records that Wikidata points to, with the concepts matched (possibly none) |
| `external_entries_acm_ccs` | 3,583 | every ACM CCS 1998 and 2012 node |
| `external_entries_msc` | 17,872 | every MSC 2000/2010/2020 node |
| `external_entries_pacs_physh` | 8,462 | every PACS 2010 and PhySH node |
| `external_entries_jel` | 1,015 | every JEL node (undated) |
| `external_entries_curated_lists` | 2,666 | every list item (Nature Methods, Science, Physics World, TR10, Gartner, Research Fronts) |
| `match_verifications` | 28,914 | one LLM judgement of one (entry, candidate concept) pair, with model, prompt hash and cost |
| `crosswalk_level1_to_field` | 284 | level-1 concept → OpenAlex field |
| `spotcheck_p78` | 78 | iteration-1 panel concept → joined concept and its events |

The `external_entries_*` datasets list every entry of every source, matched or not. A later phrase frame (N) can
therefore be matched against them without the Wikipedia selection built into the legacy-concept frame.

### 1.2 `concept_recognition` row format

`input` (JSON string):
`openalex_id, qid, qid_resolved` (Wikidata redirect resolved; the original is kept), `label, label_norm, aliases`
(≤20, from OpenAlex English variants and Wikidata label/aliases), `aliases_norm, acronyms` (aliases of ≤6 upper-case
characters, kept separately and **never** used for matching), `level, ancestor_ids, level0_disciplines, enwiki_title`,
and `frame_role` (`target` for levels 2–5, `ancestor_only` for levels 0–1).

`output` (JSON string):
* `events[]`, sorted by year. Each event has `source, event_type, year, date, date_precision` (Wikidata 7–11, `9` for
  year-level sources, or `"estimated"`), **`year_usable`**, `match_method, match_confidence, relation, entry_id`
  (the key into `external_entries_*`) and a `detail` object (for example MeSH UI, tree numbers, `year_rule`,
  `mesh_baseline`; taxonomy code and versions; list rank/role/phase and URL; Wikipedia title, raw first revision and
  redirect repair).
* `sources_checked{source: found | not_found | not_applicable | not_checked | found_estimated}`. `not_applicable`
  means the concept lies outside the source's domain scope. Scope is decided from the concept's level-0 disciplines:
  MeSH = Medicine/Biology/Chemistry/Psychology, ACM = Computer science, MSC = Mathematics, PACS/PhySH = Physics/
  Materials science, JEL = Economics/Business, Nature Methods = Biology/Medicine/Chemistry, Physics World =
  Physics/Materials science, other lists = all. A `found` outside the scope is still reported as `found`.
* `present_day{year_known:false, n_wiki_sitelinks, openalex_works_count, openalex_cited_by_count, wikidata_n_claims,
  wikidata_instance_of/subclass_of/part_of, mesh_tree_codes_wikidata, jel[], wikidata_mag_id_matches_openalex}`.

Metadata: `metadata_fold` (dev / heldout / unassigned), `metadata_group`, `metadata_group_plurality`,
`metadata_group_plurality_share`, `metadata_level`, `metadata_l1_fields`, `metadata_level0`, `metadata_n_events`,
`metadata_n_events_year_usable`, `metadata_frame_role`, `metadata_openalex_id`, `metadata_qid`.

**`relation`** is always stated **from the external entry's side**: `same`; `narrower` = the entry is more specific
than the concept (for example "Next-generation DNA sequencing" → *DNA sequencing*); `broader` = the entry is more
general (for example MSC section "94-XX" → *Cyclic redundancy check*). For the primary O5 analysis, use
`relation == "same"`; for Research Fronts, use `same` or `narrower` (a front is always a specific phrase).

**`match_method` / `match_confidence`:**
* `wikidata_property` (1.0): MeSH P486, ACM P2179, MSC P3285.
* `wikidata_sitelink` (1.0) for Wikipedia.
* `exact_norm_label` (0.9): taxonomy node label equals the concept name after normalisation.
* `exact_norm_label+llm` (MeSH term = concept name, LLM-confirmed) and `exact_norm_alias+llm` (the match came through
  an alias, LLM-confirmed): min(0.85, LLM confidence).
* `fuzzy+llm`: 0.9 × LLM confidence.
* `embed+llm` / `wikilink+llm`: LLM confidence (list items).

Normalisation: NFKC, casefold, possessives and punctuation removed except `-` and `+`, whitespace collapsed, and
the **last token lemmatised with lemminflect**. Stemming is never used, because the iteration-1 probe showed it is
unsafe.

### 1.3 Provisional fold (the panel builder overrides it)

Each level-1 concept is mapped to one of the 26 OpenAlex fields (`out/crosswalk_level1_to_field.csv`):
* 159 are agreed by `google/gemini-2.5-flash-lite` and `openai/gpt-4.1-nano`.
* 125 disagreements were resolved by hand: 111 kept model A, and 14 were overridden with the ASJC placement
  (reasons in the CSV).

Fields map to groups as follows:
* **Dev:** CS(17), Eng(22), BGM(13), Med(27).
* **Held-out:** Physical(15, 16, 19, 21, 25, 31), LifeEnv(11, 23, 24, 28, 30), Social(12, 14, 20, 32, 33),
  MathDec(26, 18).
* Fields 29/34/35/36 → `unassigned_health`.

A concept takes the group of its level-1 ancestors when they all agree or when ≥2/3 of them fall in one group;
otherwise it is `unassigned_multi`. Concepts without level-1 ancestors use the unambiguous level-0 parents.

Resulting fold (levels 2–5): dev 19,527 / held-out 28,123 / unassigned 17,073, of which 16.8k are
`unassigned_multi` (many legacy concepts have level-1 ancestors in several groups). The plurality group and its
share are included so the panel can apply its own rule. **This fold is provisional.** It does not include S1's
venue-based home or the onset-cohort hold-out, which this dataset cannot know.

## 2. Sources, their biases and lags (read before using O5)

| Source | What is dated | Known biases / lags |
|---|---|---|
| **MeSH 2026** (`desc2026.gz`) | `mesh_year_best` = year(DateIntroduced) for all 31,110 descriptors. The 2026 DTD replaced DateEstablished with DateIntroduced and removed DateCreated/DateRevised from descriptors. HistoryNote years are kept raw (`history_year`, `history_year_earlier`) and agree with DateIntroduced for 91% of descriptors. | Biomedicine only. Introduction lags first literature by several years (the curators add terms after uptake). **`mesh_baseline=true` for year ≤1966** marks the original vocabulary (5,523 descriptors), which is not recognition. 720 supplementary chemical records (SCRs) are added only where Wikidata P486 points to a C-number. |
| **English Wikipedia** | First revision (`rvdir=newer`). If the first revision is <200 bytes or its comment mentions a redirect, its content is read; if it starts with `#REDIRECT`, the first revision ≥500 bytes among the oldest 50 becomes `first_article_ts`. | **Creation dates are compressed into the 2001–2007 growth wave.** Early creation partly measures Wikipedia's own growth, so model creation relative to Wikipedia growth, or use "created after t0" only for onsets ≥2006. Page moves carry history, so the first revision is the original creation even under an old title. Titles are Wikidata enwiki sitelinks (current titles). **Rate limit:** Wikimedia throttled this shared IP to ~1–2 requests/s, so exact first revisions were fetched for 6,540 titles (level 2 first, random order within level). All other titles carry `wikipedia_page_created_estimated` from their page id; see §3. |
| **Wikidata** | P571 inception, P575 time of discovery/invention, with precision and qualifiers. Only precision ≥9 (year) is `year_usable`. | Sparse (≈1.4k concepts). Values are community-entered and sometimes give the year of a founding paper or an ancient date. |
| **ACM CCS 1998 → 2012** | `taxonomy_in_version` (year = version) and `taxonomy_added_between` (node label absent from 1998 and the concept unmatched in 1998). The 1998 page's own **NEW!** markers give `added_between 1991→1998`. | Computing only. Resolution is coarse (two versions). 2012 was a **full redesign** (`scheme_redesign=true`), so absence from 1998 is weak evidence of novelty. |
| **MSC 2000 → 2010 → 2020** | same | Mathematics only; incremental revisions every 10 years. Wikidata P3285 often points to a whole section (`-XX`/`xx`); those links carry `relation=broader`. |
| **PACS 2010 → PhySH 2016** | same | Physics only. PhySH *replaced* PACS with a different labelling style (`scheme_redesign=true`), so `added_between 2010→2016` is noisy. Treat it as membership in PhySH rather than as novelty. |
| **JEL** | nothing (undated) | Present-day membership only (`present_day.jel`, `year_known=false`). **Social sciences have no dated domain taxonomy here.** |
| **Nature Methods MoTY, Science BOTY, Physics World BOTY** | list year (winner, or Physics World top-10 rank) | Editorial, high-visibility and biomedicine-heavy (Physics World covers physics). The lists are small. Items often name a family or an event ("Dolly the sheep"), so most links are `narrower`/`broader`. Science runners-up were not delivered (§5). Physics World 2025 (winner + 9) was transcribed from physicsworld.com. |
| **Clarivate/CAS Research Fronts** (English reports on the CAS-ISD site, 2017–2025) | report year; role hot/emerging, rank within its broad field, core papers, citations, mean year of core papers | A citation-clustering product, so it is **not independent of publication data**. It is also the most "bibliometric" of the external sources. Front names are long phrases, so most links are `narrower`, and the LLM is sometimes over-eager with `same`. The parsed counts match the published totals for 2023 (128) and 2024 (125); 2021 and 2022 lose 4 and 9 fronts to table-layout breaks. The 2016 report lists fronts without ranks or counts and was not parsed; 2014–2015 English reports are not on the CAS-ISD page. |
| **MIT TR10, Gartner Hype Cycle** (Envisioning *Hindsight*, CC BY 4.0) | list year; Gartner phase where given | Technology-biased, inconsistent across years, and Gartner's method is contested. Hindsight is a **new, pre-release secondary compilation** (a red flag). Spot checks: the TR10 2010 list matches technologyreview.com 10/10, and Gartner 2023 has 25 entries as Gartner published. Labels were transcribed from charts; phase is missing for many entries. |

**Uneven domain coverage** (share of concepts in a group with ≥1 event from each domain source, from
`coverage_report.json`): MeSH covers BGM 60%, Med 70%, LifeEnv 41%, Physical 16%, Social 13%, CS 6%. ACM covers
CS 13%. MSC covers MathDec 18%. PACS/PhySH covers Physical 14%. `groups_without_dated_domain_taxonomy` = **Social,
Eng**. **Cross-group O5 comparisons should therefore also be reported with a Wikipedia/Wikidata-only variant.**

**Selection by construction:** the legacy concepts (MAG fields of study) were seeded from Wikipedia, so 99.4% have an
enwiki sitelink. Wikipedia *existence* is therefore uninformative. Use the creation date only.

## 3. Quality evidence

* **Known-answer checks (hard asserts, all pass):**
  * Optogenetics → Nature Methods 2010.
  * Induced pluripotent stem cell → Nature Methods 2009.
  * CRISPR → Science BOTY 2015.
  * Super-resolution microscopy → Nature Methods 2008.
  * All exact Wikipedia dates are ≥2001-01-15 (min 2001-01-16).
  * All MeSH years lie in 1954–2026.
* **Audit of exact matches** (100 random entries per family, LLM-judged; `llm_agreement.json`):
  * Precision by method: label matches **0.96**, Wikidata-ID links 0.79 (MeSH 0.84, MSC 0.67, where most
    "failures" are section-level links now marked `broader`), alias-only matches **0.31**.
  * Because of that alias result, *no alias-only match is accepted without an LLM verdict*. A second pass verified
    all 12,581 alias-only and MeSH label-only pairs; 36–52% were accepted, depending on family. The main culprit is
    noisy aliases on Wikidata and OpenAlex ("Glasses" is an alias of methamphetamine, "MEN" of multiple endocrine
    neoplasia).
* **Inter-model agreement** (`gemini-2.5-flash-lite` vs `gpt-4.1-mini` on 373 double-labelled pairs):
  * accept/reject: raw 0.80, κ = 0.60.
  * 3-class (same / hierarchical / reject): κ = 0.44.
  * 5-class: κ = 0.41. It is deflated because gpt-4.1-mini flips the narrower/broader direction under
    `*_entry` label names; the list re-verification therefore uses the direction-explicit labels
    `item_is_more_specific` / `item_is_more_general`.
* **Hand checks by the executor:**
  * 30 random accepted LLM links: precision **0.97**, but exact relation only 0.67.
  * 30 inter-model disagreements: primary right on accept/reject 70%, second model 77%.
  * 30 random curated-list links after the v2 pass: precision **0.87**; the 10 `same` links are **10/10 correct**;
    exact relation 0.63.
  * 30 random Research Fronts links: precision **0.97**, exact relation 0.80, but only 5 of the 9 `same` links are
    truly the same topic. A Research Front is a long, specific phrase, so read its `same`/`narrower` links as "a front
    about this concept".
  * **Conclusion:** accepted links are reliable, and `relation=same` is reliable for taxonomies and the editorial
    lists (not for Research Fronts). Narrower-vs-broader is only indicative.
* **Known residual errors:**
  * Gartner "Micro Fuel Cells" was first matched to *Microbial fuel cell*; v2 corrected this to *Fuel cells*
    (narrower) but also accepted a few sibling fuel-cell types as `narrower`.
  * List items naming a family ("Gene-editing nucleases") link to members with an uncertain direction.
* **Wikipedia page-id estimate:**
  * Page ids are assigned when a page is created, so they are a monotone clock. A calibration on the 6,540
    titles with both an exact first revision and a page id (pageid quantile bins → median page id / median first
    revision → monotone envelope → interpolation) gives, in 5-fold CV: **93.2% same calendar year**, median
    absolute error 0.001 years, p90 0.19 years.
  * An estimated event is `year_usable=true` only if its estimated year is one where the CV same-year share is
    ≥0.9 with ≥30 calibration pages (currently 2002, 2003, 2004, 2005, 2006, 2007, 2013).
  * An L2 isotonic fit was tried first and rejected: 77% same-year, because imported or merged histories give some
    pages a very old first revision at a high page id.
  * Estimates date page creation (which may be creation as a redirect), with no redirect repair.
* **Join test with iteration 1:** 67 of the 78 P78 concepts (86%) join on normalised label or alias. The 11 misses
  (H5N1, pandemic H1N1, microblog, ZigBee, network coding, ribotype 027, TAVI, LTE-Advanced, single-incision
  laparoscopic surgery, plug-in hybrid electric vehicle, piezoelectric nanogenerator) have no legacy concept with
  that name. Hand-checked joined examples are plausible:
  * sentiment analysis: ACM 2012 (new vs 1998) and MeSH 2022;
  * biosimilar: MeSH 2012;
  * drug-eluting stent: MeSH 2008;
  * synthetic biology: TR10 2004, MeSH 2011;
  * cognitive radio: TR10 2006;
  * differential privacy: Gartner 2020, TR10 2020;
  * GWAS: MeSH 2009;
  * WiMAX: Gartner 2004.

  One informative oddity: *cancer stem cell* links to MeSH "Neoplastic Stem Cells" (1986), a descriptor that
  predates the concept's onset.

## 4. Layout

```
README.md                 this file
data.py                   builds full_data_out (parts), mini_data_out.json, preview_data_out.json
reproducibility.md        step-by-step reproduction on Ubuntu
pyproject.toml            dependencies (Python 3.12, uv)
run_all.sh                rebuilds everything from cache/ (network and LLM steps resume from cache)
restore.sh                re-downloads every path the manifest marks `delete`
.aii/manifest.yaml        keep/delete decision for every heavy path
scripts/
  common.py               paths, logging, normalisation, polite async HTTP (maxlag, 429 backoff, AIMD pacer)
  llm.py                  OpenRouter JSON calls: disk cache, cost ledger, $2 cap, 403-budget stop
  s0_concepts.py          concept frame (OpenAlex parquet + legacy JSON ancestors)
  s1_crosswalk.py         level-1 -> field crosswalk (2 LLMs + crosswalk_manual.json)
  s2_wikidata.py          Wikidata wbgetentities, compacted
  s3_wikipedia.py         Wikipedia first revisions + redirect repair (paced, resumable)
  s3b_pageids.py          Wikipedia page ids, 50 titles per call
  s4_mesh.py, s4b_mesh_supp.py   MeSH descriptors / SCRs
  s5_taxonomies.py        ACM 1998/2012, MSC 2000/2010/2020, PACS 2010, PhySH, JEL
  s6_lists.py             Nature Methods, Science, Physics World (Wikipedia; 2025 from physicsworld.com), TR10 + Gartner (Hindsight), Research Fronts
  s6b_research_fronts.py  Research Fronts 2017-2025 tables parsed from the CAS-ISD English PDFs
  s7_keys.py              join keys
  s7_candidates.py        ID / exact / wikilink / fuzzy / MiniLM candidates
  s7_verify.py            LLM verification, audits, double labels, alias pass
  s7d_lists_v2.py         stricter list re-verification (gpt-4.1-mini, direction-explicit labels)
  s8_assemble.py          events, absence flags, fold, Wikipedia calibration, QC asserts
  hand_check.py (+ *_verdicts.json)   the executor's hand verdicts and agreement statistics
  s9_outputs.py           coverage report, P78 spot check, data_out parts, mini, preview
  s10_provenance.py       out/sources.json
full_data_out/            deliverable parts (kept)
mini_data_out.json, preview_data_out.json
out/                      reports listed in section 1
work/                     intermediate tables (entries, candidates, links, verifications, keys)
cache/wikidata/           compacted Wikidata entities (kept)
cache/wikipedia/          first revisions + page ids (kept)
cache/llm/                every LLM call and verdict (kept; reruns are free)
cache/raw/tax, cache/raw/lists   small source files (kept)
cache/raw/concepts/       OpenAlex concept parquet parts (small, kept)
cache/raw/{concepts_legacy,mesh,research_fronts}   large downloads (deleted after the round; see restore)
temp/                     dataset search log (50 HF queries) and candidate evaluation (25+ candidates, kept vs discarded)
logs/                     run logs
```

`cache/wikidata/`, `cache/wikipedia/`, `cache/llm/` and `full_data_out/` consist of text files (each <100 MB), so they are
always kept and published. The kept artefacts stay on the run's storage volume at these relative paths. Everything except files ≥100 MB is
also published; none of the kept files reaches 100 MB.

## 5. Deviations from the plan

1. **The 2026 parquet concepts snapshot has empty `ancestors`.** Ancestors, MAG ids and English variants come from
   OpenAlex's legacy JSON concept snapshot (same ids, still zero credits).
2. **Wikipedia throughput:** Wikimedia rate-limited the shared IP (HTTP 429 at >1–2 req/s), so only 6,540 titles
   have exact first revisions. All others carry the calibrated page-id estimate, flagged by
   `event_type=wikipedia_page_created_estimated` and `date_precision="estimated"`. The fetcher (`s3_wikipedia.py`)
   resumes and can complete the rest later.
3. **Wikidata `maxlag=5`:** the query-service lag stayed above 5 s, so maxlag was honoured for 3 retries per request
   and then dropped for 60 s. The requests are read-only at 4 concurrent.
4. **No Wikidata property** exists for PhySH or JEL codes (`wbsearchentities(type=property)` found none), so those
   sources are matched on labels only.
5. **Not delivered:**
   * Science BOTY runners-up: science.org returns 403.
   * Science "Molecule of the Year" 1989–1995.
   * PACS editions before 2010.
   * Research Fronts 2014–2016 (2016 layout not parseable; 2014–2015 not hosted).

   Each is listed in `sources.json`. Clarivate's own Research Fronts download page is lead-gen gated, so the
   identical English reports were taken from CAS-ISD (`english.casisd.cas.cn/research/rp/`).
6. **Extra quality steps not in the plan:**
   * LLM verification of alias-only matches (after the audit showed 0.31 precision).
   * A second, stricter verification of all list items with a stronger model.
   * 30-item hand checks of the list links and of the Research Fronts links.
   * Relation `broader` for section-level MSC ID links.
7. The verification budget was spent on all fuzzy candidates (3,860 calls) rather than 200, as the plan intended.
   Total spend was $1.49.

## 6. How to run

```bash
./restore.sh     # environments + large raw downloads (public, no credentials)
./run_all.sh     # full pipeline; network/LLM steps are served from cache/, so a rerun costs $0
```

Requirements: `uv`, Python 3.12, ~5 GB for `.venv` (CPU torch for MiniLM), and `OPENROUTER_API_KEY` /
`OPENROUTER_BASE_URL` only if prompts change.

Reading the data:

```python
import glob, json
rows = [x for f in sorted(glob.glob("full_data_out/full_data_out_*.json"))
        for d in json.load(open(f))["datasets"] if d["dataset"] == "concept_recognition" for x in d["examples"]]
ev = {r["metadata_openalex_id"]: json.loads(r["output"])["events"] for r in rows}

def first_recognition_year(events, source):
    """Strict variant: earliest year-usable event of one source whose relation is 'same' (MeSH baseline excluded)."""
    ys = [e["year"] for e in events if e["source"] == source and e["year_usable"] and e["relation"] == "same"
          and not e["detail"].get("mesh_baseline")]
    return min(ys) if ys else None

print(first_recognition_year(ev["C50738837"], "mesh"))   # Optogenetics -> 2013
```

## 7. Restoring removed files

Every path marked `delete` in `.aii/manifest.yaml` is restored by `./restore.sh`:

| Path | Restore |
|---|---|
| `.venv/` | `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python torch --index-url https://download.pytorch.org/whl/cpu && uv pip install --python .venv/bin/python -r pyproject.toml` |
| `.venv_io/` | `uv venv .venv_io --python=3.12 && uv pip install --python .venv_io/bin/python pandas pyarrow aiohttp loguru lemminflect lxml rapidfuzz` |
| `scripts/__pycache__/` | recreated automatically on import |
| `cache/raw/concepts_legacy/` | `https://openalex.s3.amazonaws.com/legacy-data/concepts/` (bucket listing; `restore.sh` fetches every `part_*.gz`) |
| `cache/raw/mesh/` | `https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2026.gz` and `supp2026.gz` |
| `cache/raw/research_fronts/` | the 10 PDFs listed in `scripts/research_fronts_urls.txt` (CAS-ISD) |
| `work/concept_label_emb.npy` | `cd scripts && ../.venv/bin/python s7_candidates.py` |
| `work/concept_rows.pkl` | `cd scripts && ../.venv/bin/python s8_assemble.py` |

The OpenAlex S3 snapshots are updated in place, so a later restore can differ slightly from the 2026-09-28 copy
(sha256 values in `out/sources.json`).

## 8. Licences

OpenAlex and Wikidata: CC0. Wikipedia metadata: CC BY-SA. MeSH: NLM terms. ACM CCS: free for research use. MSC:
CC BY-NC-SA. PhySH: CC0. PACS: AIP content, codes and labels only. Hindsight (TR10/Gartner): CC BY 4.0, attributed to
"Envisioning, Hindsight". Only names, codes, years and short labels are stored; no charts or full texts.
