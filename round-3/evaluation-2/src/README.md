# Checking the record before the paper (iteration-3 record audit)

This evaluation collects **no new data**. It audits and completes the iteration-2 record before iteration 3 builds on it. It has five
work packages (plan `gen_plan_evaluation_1_idx4`):

| WP | Question | Main output |
|---|---|---|
| WP1 | Does each number in the draft match its source file? | `claims_ledger.csv` (246 rows) |
| WP2 | Which record tables were missing, and what do the refit CIs look like? | `record_tables/*.csv`, `record_tables/next_field_trace.json` |
| WP3 | Do the Exp5 and Exp6 frames agree on the concepts they share? | `frame_agreement.json` |
| WP4 | Can external recognition (O5) serve as independent ground truth? | `o5_validation.json`, `o5_definitions.json` |
| WP5 | Outputs and the corrections to the text | `eval_out.json` (exp_eval_sol_out, validated), `text_corrections.md` |

All source paths in the outputs are **relative to the run's `3_invention_loop/` directory** (for example
`round-2/experiment-5/src/results/h1_heldout.json`). Workspace outputs are relative to this directory.

## Headline results

**WP1 ledger.** 246 rows: 224 MATCH, 15 MISLABELLED, 6 MISMATCH and 1 FILE_FLAG_OVERRIDDEN. 58 rows are blocking. A separate automatic
harvest found 555 numbers in the draft's abstract and iteration-2 sections; 494 of them match a key in the cited artifact's result files
(`record_tables/draft_number_harvest.csv`).

- **H1:** `lpm_beta_within_gt0_p05 = true`. The within-field LPM gives beta = +0.068/SD, with concept-clustered p = 0.041 and two-way p = 0.17.
  The frozen rule names no SE type, and the sealed `models.py` uses `p_concept`, so the criterion passes as preregistered. The verdict is
  still DISCONFIRMED, because 4 of the 6 core criteria fail. `placebo_null = false` means the real dAUC does not exceed the p95 of the
  rewired-backbone placebo.
- **Ordering → MIXED.** The draft's "66% of broad concepts" is 57/87 non-tied cases. The same count is 57/102 = 55.9% of evaluable concepts
  and 57/175 = 32.6% of broad concepts. The lead-lag coefficients are *negative*, the event study has a pre-trend (ev-3 = -0.072, p = 0.0002),
  and on DEV the reverse path is significant (b = 0.232, p = 0.006). The file flag `CONFIRMED` is overridden.
- **H3:** the pooled concept-bootstrap CI includes 0 ([-0.006, 0.065]). The DEV value was 0.138, so the held-out value has shrunk to 0.21 of
  it. "0/40 shuffles" is a false-positive rate, not a p-value.
- **Dataset 2:** ACM 3,583, MSC 17,872, PACS 8,462 and JEL 1,015 are **entry** counts. The concept counts are 1,298, 1,121, 2,635 and
  213 (JEL has 0 dated events). Wikipedia has 7,806 exact first revisions, not 6,540.
- **The "B5 + all_four" row** is actually `size_controlled_all_three` (B3 + log size + gateway/phi_home/density). Its refit CI95 is
  [-0.043, 0.220].
- **Power (10.7):** 0.004 is the **90%**-power point for 8,515 episodes, not 80% for 27,393. At b = 0 the CI rule fires 12.5% of the time.
  The SD-0.015 and 34-concepts sentences come from Evaluation 1.
- **Clashes resolved** (`record_tables/next_field_trace.json`):
  - The LRs: 68.6 is M1 vs M0 (Breslow), 71.7 is M2 vs M0 (Breslow), 77.3 is M2 vs M0 (exact likelihood). M1 vs M0 exact is 73.2.
  - The strata: 961 is the number of informative strata, 2,339 is all primary strata, and 2,992 is the count before the `n_ret > 0` restriction.
  - The coefficients: d = 0.281 is M1 `d0_ret_rel`, and d = 0.302 is M2 `d_ret_gate`.
  - All 26 checked Exp6 headline numbers reproduce from `entry_risk_sets_*.parquet` with an independent Breslow conditional logit and
    statsmodels' exact `ConditionalLogit`.

**WP2 refit bootstrap** (concepts resampled within home group, whole LOGO pipeline refit, B = 2000). Every point estimate reproduces
exactly (|diff| < 1e-6). The refit CIs are 1.2–2.2× wider than the fixed-prediction CIs, and **none excludes 0**:

| Row | Point | Refit CI95 |
|---|---|---|
| exp1 A\*_h Δρ | -0.006 | [-0.111, 0.032] |
| exp3 D_ratio Δρ | +0.006 | [-0.118, 0.164] |
| exp3 F_res Δρ | -0.060 | [-0.188, 0.027] |
| exp4 G Δρ (O2r_m30) | +0.033 | [-0.250, 0.339] |
| exp4 G Δρ (O2r_resid) | +0.150 | [-0.127, 0.428] |
| exp4 G ΔAUC (O1) | +0.072 | [-0.012, 0.231] |
| exp4 G ΔAUC (O1, +label coverage) | +0.016 | [-0.042, 0.159] |

The exp3 CIs in the source were already refit bootstraps; the ones here are recomputed. T1 (the 34-indicator portability table) matches
exp3's `screen_result.json` for every indicator.

**WP3 frame agreement** (628 shared concepts, 96% of Exp6):

| Measure | Value |
|---|---|
| Onset exact / ±1 | 0.976 / 0.989 |
| Home κ | 0.990 |
| O2r_m50 Spearman / Lin CCC | 0.998 / 0.997 |
| O1 κ / O3 κ | 0.97 / 0.93 |
| Episode Jaccard, median / pooled | 1.0 / 0.977 |
| **Retention κ, each frame's own rule** | **0.28** |
| Retention κ, matched definition (Exp5 `R_abs2` vs Exp6 `R_cj`) | 0.98 |

The pre-declared pooling verdict is **PARTIAL** (3 of 4 criteria met). In practice the frames measure the same concepts, onsets, homes and
episodes, but different retention outcomes (relative-share vs absolute ≥ 2). Nearly all retention disagreements (99.9%) are attributed to
RETENTION_WINDOW. An Exp5-minus-Exp6 H2 confirmation must rebuild RETAINED/LOST with `R_cj` (= `R_abs2`). The counts it will have after
removing the Exp6 concepts are in `record_tables/frame_overlap_by_group.csv`:

| Group | Concepts left | Episodes |
|---|---|---|
| PHYS | 708 | 1,580 |
| LIFEENV | 1,081 | 2,992 |
| SOC | 1,301 | 3,148 |
| MATHDEC | 165 | 434 |
| COHORT | 4,117 | 9,045 |

**WP4 O5 validation** (all 12,499 Exp5 concepts joined). The O5_main base rate is 0.238 on the held-out groups.

- **Reading: UNRELATED** to the publication outcomes (pre-declared rule). The pooled held-out ρ is 0.014 [-0.045, 0.073] with O2r_m50 and
  0.001 [-0.033, 0.034] with O1. With log N it is 0.072.
- Only O5_tax is RELATED-NOT-DUPLICATE (ρ with O2r_m50 = 0.069 [0.020, 0.118]).
- For **67% of concepts the first qualifying recognition is at or before t0.** MeSH, Gartner and MIT TR10 are flagged by the >30%
  precedence rule. MeSH also has 45% of its recognitions after t0+8.
- **Executor-checked hand check** (100 items: gpt-4.1-mini judge at $0.009, the executor reading all 100, and MediaWiki first revisions):

  | Measure | Value |
  |---|---|
  | Positive precision | 0.86 [0.74, 0.93] (0.96 if partial matches count) |
  | Date error ≤ 1 year | 95% |
  | False-negative rate of negatives (Wikipedia only, lower bound) | 0.14 |
  | Executor–LLM κ | 0.50 |

  → **FIT_FOR_USE = true** by the pre-declared rule. However, only 42% of the positive events plausibly mark the recognition of a *new*
  concept. The rest date long-known phenomena, and 84% of the negatives had a Wikipedia page before t0.

## Layout

| Path | Content |
|---|---|
| `eval.py` | orchestrator and assembler: `eval_out.json`, `inputs_manifest.json`, `o5_validation.json` |
| `common.py` | paths, `norm_id`, dotted-key reader, kappa / Lin CCC / partial Spearman / DL pooling / Holm / Wilson, sha256 tracking |
| `wp1_ledger.py` | claims ledger, draft number harvest, T1, T2, T5, T6, T7 tables, 12-candidate partial-association table |
| `wp2_t3_refit.py` | T3 refit bootstrap (re-implements the exp1, exp3 and exp4 LOGO pipelines; 16 worker processes) |
| `wp2_t4_nextfield.py` | T4 Breslow and exact conditional-logit refits, AUCs, per-row parquet, trace JSON |
| `wp3_frames.py` | WP3 agreement, disagreement attribution, logit of any disagreement, pooling rule, Exp5-minus-Exp6 counts |
| `wp4_extract.py` | joins Dataset 2's concept_recognition to the Exp5 frame (`results/o5_joined.jsonl`) |
| `wp4_o5.py` | O5 variants (writes `o5_definitions.json` first), coverage, precedence flags, lag and KM, associations (B = 2000) |
| `wp4_handcheck.py` | 100-item sample, verdict reuse, LLM judge, MediaWiki check (`--wiki-retry` with backoff), `--finalize` metrics |
| `verify_headlines.py` | independent re-derivation of the headline numbers with shuffled/placebo controls (`results/verify_headlines.json`) |
| `reproducibility.md` | exact commands, pins, runtimes and expected numbers |
| `wp5_text.py` | `text_corrections.md` (old sentence, new sentence and source keys for each blocking item) |
| `claims_ledger.csv` | WP1 ledger (`source_value` read programmatically; `status`, `severity`, `correction_text`) |
| `frame_agreement.json`, `o5_validation.json`, `o5_definitions.json` | WP3 and WP4 results; the O5 definitions were pre-declared |
| `record_tables/` | `portability_F3`, `lineage_robustness_iter1`, `refit_bootstrap_iter1`, `h1_criteria`, `ordering_mixed`, `coverage_iter2(_steps)`, `partial_association_all`, `definitions_diff`, `frame_*`, `o5_*`, `next_field_trace.json`, `next_field_heldout_rows.parquet`, `draft_number_harvest`, `hypothesis_iter3_numbers` |
| `results/` | intermediate JSON: T3, O5 core, hand-check summary, LLM metadata, per-stage input manifests; `executor_verdicts.json` |
| `eval_out.json` (+ `full_`/`mini_`/`preview_`) | exp_eval_sol_out output: 74 flat metrics and 6 datasets |
| `logs/` | per-stage logs, including every LLM prompt and response |

`record_tables/next_field_heldout_rows.parquet` (2.5 MB) is below the auto-keep floor, so it is kept and published.

## How to run

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python pandas pyarrow numpy scipy statsmodels scikit-learn ijson loguru requests openai tenacity psutil pyyaml
.venv/bin/python wp4_extract.py && .venv/bin/python wp4_o5.py          # O5 panel and associations
.venv/bin/python wp4_handcheck.py && .venv/bin/python wp4_handcheck.py --wiki-retry   # sample, LLM judge, Wikipedia dates
# the executor reads the items and writes results/executor_verdicts.json, then:
.venv/bin/python eval.py --stages all                                   # T3, T4, WP3, WP4, finalize, WP1, then assemble
.venv/bin/python wp5_text.py
```

The inputs are read from the dependency artifacts under one root (`AII_RUN_ROOT`, default: three levels up) and are never copied; see `reproducibility.md`. The LLM calls need `OPENROUTER_BASE_URL` and
`OPENROUTER_API_KEY`.

## Deviations and limits

- **Hand check.** It is "executor-checked", not human-checked. Step 1 reused no verdicts because no (concept, entry) pair overlapped
  Dataset 2's hand-check files.
- **LLM judge.** It was used on positives only. Wikidata events carry no entry title (the event sits on the concept's own item), so the
  LLM's "no" on those was overridden by the executor's reading.
- **Wikipedia API.** It returned HTTP 429 for 31 of the 70 lookups on the first pass (the IP is shared). All 31 were resolved by
  `--wiki-retry` with backoff.
- **GROUNDING attribution (WP3).** The rule uses the t0..t0+2 early-volume ratio, because counts for year t0 alone are not stored in
  either frame.
- **Newborn κ.** It is 0 by construction, because every Exp6 concept is newborn. Percent agreement is 0.968.
- **O5_main_noRF.** This variant, which drops the citation-derived Research Fronts, was declared in `o5_definitions.json` before any
  association was computed. The false-negative rate is a lower bound, because only Wikipedia was checked.
- **Scope of the frame agreement.** It describes the 628 shared, mostly newborn concepts. It may overstate agreement for Exp5-only concepts,
  95% of which are not newborn.

## Restoring removed files

`.aii/manifest.yaml` marks only `.venv/` for deletion (regenerable). To rebuild it:

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python ijson==3.5.1 loguru==0.7.3 numpy==2.5.3 openai==3.20.0 pandas==3.0.6 psutil==7.2.2 \
    pyarrow==25.0.1 pyyaml==6.0.3 requests==2.34.2 scikit-learn==1.9.1 scipy==1.18.1 statsmodels==0.15.0 tenacity==9.1.4
```
