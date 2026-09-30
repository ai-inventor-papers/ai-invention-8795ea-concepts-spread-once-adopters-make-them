# Do hub fields keep new concepts? A sealed held-out test on the full OpenAlex snapshot

AI Inventor, invention loop iteration 2, artifact `gen_art_experiment_5` (plan `gen_plan_experiment_1_idx1`).
This is a "deepen" move on the iteration-1 lead from `art_33_KKk_G8Gw5`: there, the adopting field's gateway centrality
added **+0.10 retention AUC** on 80 episodes from 28 concepts.

**H1 (episode level).** When a new concept is adopted by an off-home field *j*, does the field's frozen
1998–2002 eigenvector *gateway centrality* in the 26-field relatedness backbone predict that *j* keeps it
(R_cj)? The test asks whether it does so beyond:
- B5,
- field size,
- relatedness to the home field φ(home,j),
- relatedness density,
- the field's leave-concept-out retention propensity P_j(−c),
- coverage,
- the episode's own early size.

The specification was frozen on DEV homes (CS, Engineering, Biochem/Genetics, Medicine; onset 2003–09) and scored
**once** on sealed held-out home groups and the 2010–14 cohort.

**H3 (concept level).** Does gateway-weighted early landing (G) predict size-adjusted later breadth (O2r_resid) given
B5?

## Headline results

| | DEV (LOGO, OOF) | HELD-OUT (frozen dev fit) |
|---|---|---|
| episodes / concepts | 9,079 / 3,987 | 8,515 / 3,085 (+ cohort 9,798) |
| AUC of baseline X0 | 0.866 | 0.837 |
| **ΔAUC of adding gateway_j** | **+0.00001** [−0.0007, +0.0005] | **−0.00001** [−0.0006, +0.0003] |
| per group | CS, Eng, BGM, Med: all within ±0.0001 | PHYS +0.0005, LIFEENV −0.0003, SOC −0.0001, MATHDEC +0.0005 |
| DerSimonian-Laird pooled (4 groups) | – | −0.00004 [−0.0004, +0.0003], I² = 0 |
| cohort 2010–14 | – | −0.0001 [−0.0008, +0.0001] |
| conditional logit, concept FE (β per SD) | +0.058 (p = 0.26) | −0.075 (p = 0.23) |
| LPM with field FE + time-varying gateway_j,s | −0.003 (p = 0.92) | +0.068 (p = 0.041 concept-clustered; p = 0.17 two-way) |
| boundary (gateway × top-tercile home; predicted < 0) | −0.051 (p = 0.39) | +0.064 (p = 0.45) |
| 200 rewired-backbone placebos: real > 95th percentile? | no (placebo p95 = 0.00016) | no (p95 = 0.00011; 36.5% of placebos ≥ real) |
| crossed concept × field bootstrap (Owen) | [−0.0056, +0.0013] | [−0.0023, +0.0010] |
| leave-one-adopting-field-out range | [−0.0002, +0.0001] | [−0.0001, +0.0001] |
| **Relatedness head-to-head** (each added to the same base) | relatedness −0.0002, gateway −0.0001 | **relatedness +0.0034 [0.0010, 0.0051]**; gateway −0.00005 [−0.0007, +0.0002] |

**Verdict H1: DISCONFIRMED** (`results/h1_heldout.json → verdict_H1`). Pre-registered criteria:
- pooled ΔAUC ≥ 0.05: no;
- refit CI > 0: no;
- same sign in ≥ 3 of 4 groups: no (2 of 4);
- cohort same sign: yes (both ≈ 0);
- LPM β_within > 0 with p < 0.05: yes, but fragile (two-way clustered p = 0.17);
- placebo exceeded: no.

**Power.** The null is informative. On the dev covariate structure with the realised held-out n, the minimum
ΔAUC detectable with 80% power is **0.004** (a planted effect of 0.3 SD log-odds). That is 12× smaller than the
pre-registered 0.05 bar.

**Why the iteration-1 lead disappears: the "trait of the adopting field" reading.** The pre-registered baseline
ladder (`figures/ladder_dauc.png`) shows the gateway increment on DEV at each baseline:

| baseline | DEV ΔAUC | HELD-OUT ΔAUC |
|---|---|---|
| size only | +0.0042 [0.0010, 0.0060] | −0.0017 |
| iteration-1 base (B5 + size) | +0.0019 [0.0005, 0.0034] | −0.0016 [−0.0035, −0.0002] |
| + relatedness (φ_home, density) | +0.0007 [−0.0008, 0.0022] | −0.0012 |
| + P_j(−c) | 0.0000 | 0.0000 |

- On DEV the increment is already small at the iteration-1 base, shrinks once relatedness is added, and **vanishes
  once the adopting field's own retention propensity P_j(−c) enters**.
- On HELD-OUT, gateway *hurts* even at the iteration-1 base.
- Gateway alone has AUC **0.605 on DEV but 0.506 on HELD-OUT**.

The exploratory per-domain table (`results/exploratory_domain_specificity.json`, post-unseal, never used for the
verdict) locates the effect:
- In the four DEV domains, gateway alone predicts retention (AUC 0.59–0.64) and is largely a proxy for the field's
  retention propensity (Spearman with P_j 0.49–0.83).
- In Physical sciences, Life/Environment and Math/Decision it is weak (0.52–0.56).
- In Social sciences/Humanities it is **reversed** (0.41).
- Gateway is therefore a domain-specific proxy for "fields that keep things", not a portable structural mechanism.
- The standard relatedness model *does* generalise: +0.0034 held-out.

**Iteration-1 replication.** On the frame's P78 subset (85 episodes with n_early ≥ 5, 39 concepts), the
iteration-1 model gives ΔAUC **+0.023** [−0.004, +0.068]. The sign matches iteration 1, but the value is a quarter
of +0.10, which is consistent with small-sample inflation of the original lead.

**H3 (held-out, n = 2,838 concepts).**
- Partial Spearman of O2r_resid given B5:
  - G = +0.030 (one-sided within-group permutation p = 0.002);
  - G_A = +0.026 (p = 0.004);
  - G_btw = +0.046 (p = 0.0015).
- All three are Holm-adjusted to p = 0.0045. The per-group values for G are positive in all 4 held-out groups
  (0.03–0.09), with a DerSimonian-Laird pooled value of **0.068 [0.029, 0.107], I² = 0**.
- **Verdict H3: CONFIRMED by the pre-registered test, but the effect is small.** The concept-bootstrap CI of the
  pooled (not within-group) ρ for G includes 0 ([−0.006, 0.065]), because a negative between-group component
  offsets it (see `results/h3_results.json → notes`).
- The rival REL_home (landing in fields related to home) is strongly **negative**: −0.136, DL −0.157.
  Concepts that land in fields related to their home spread less.

## What was done

1. **Lexicon (outcome-blind, hashed).**
   - 64,209 legacy OpenAlex concepts (levels 2–5) from the free S3 snapshot. Their surface forms are the name, a
     joined-hyphen variant and s/es/ies variants.
   - A form shared by two concepts goes to nobody.
   - **Pre-screen** on a 1.1% random file sample: 7,566 concepts with ≥ 10 sampled verified hits in 1995–2002 are
     dropped, because t0 ≥ 2003 is impossible for them.
   - **Wikidata aliases** for the 56,643 survivors come from the SPARQL endpoint, because `wbgetentities` was
     rate-limited. Aliases are dropped if they:
     - have ≤ 3 characters;
     - are all-caps acronyms of ≤ 5 characters (the TAVI lesson);
     - equal any concept name, including level-0/1 names;
     - are ambiguous;
     - are frequent before 2003;
     - are lowercase single tokens (see the T2 fix below).
   - Result: 85,692 alias forms (`lexicon_v1.parquet`; sha256 is the last line of `frozen_lexicon.sha256`).
2. **One zero-credit scan** (`scan_full.py`) of all **2,040 parquet files (476,196,327 works)** of the
   2026-09-23 snapshot, via HTTP range reads of 10 leaf columns, in 33 minutes on 4 vCPU.
   - Base works: 129,360,390 (article|review, not paratext, not xpac, 1995–2022).
   - Matching: Aho-Corasick over space-padded surface forms (word boundaries enforced), then OpenAlex-like stemmed
     positional verification. This gives **60.0M verified matches**, aggregated per (concept, year, venue field,
     primary-topic field, legacy-tag state, match type).
   - The same pass also produces venue-field totals, 26×26 field co-assignment per year (the backbones) and a
     hash reservoir of matched titles.
3. **Grounding, existing resources first.**
   - The legacy concept tags are present in the snapshot, so TAG = title match AND tag score ≥ 0.3.
   - **Benchmark:** 390 LLM-labelled title/concept pairs. gemini-2.5-flash-lite labelled all of them and
     gpt-4.1-nano labelled 146. Cohen's κ was only 0.20, so the 41 disagreements were adjudicated by
     gemini-2.5-flash.
   - **The executor read 60 pairs by hand:** 90% agreement with the gold label.
   - **MiniLM + flags L2-logistic sense filter:** test AUC 0.871. Its precision (0.862) did not beat exact-name
     precision (0.872), so under T4 the frozen rule is **TAG** (test precision 0.947, recall 0.659), chosen on
     the benchmark test split only.
   - **Per-concept LLM precision gate** on 13,413 onset candidates (13.7k calls): 93% have precision ≥ 0.8.
     864 concepts whose labels did not parse were gated by the sense filter.
4. **Frame S1** (`frame.py`, art_33 rules):
   - t0 = first year 2000–2014 with ≥ 20 grounded works; keep 2003 ≤ t0 ≤ 2014, early volume ≥ 30, precision ≥ 0.8.
   - Home = fields with ≥ 40% of the first 30 venue-labelled works (weak home ≥ 25%).
   - Episodes = off-home fields with ≥ 2 early works.
   - R = [share_out ≥ 0.5·share_early AND n_out ≥ 9] over t0+6..t0+8.
   - Result: **12,499 concepts, 27,393 episodes** (targets: 400 and 4,000).
     - DEV: 4,771 concepts;
     - held-out: PHYS 742, LIFEENV 1,113, SOC 1,352, MATHDEC 165;
     - COHORT: 4,356.
     - Newborn: 5.4%; weak home: 1,150; intersection-born: 502.
5. **Backbones.**
   - Frozen art_33 gateway_eig. The recomputed S0 backbone from the scan correlates with it at Spearman ρ = 1.000.
   - The time-varying gateway_j,s (slices S0/S1/S2) has a within-field SD of only 0.026, against a between-field
     SD of 0.279, so the field-FE test has little power.
   - Placebos: 200 degree-preserving double-edge-swap rewirings (weights re-attached within degree-product
     quintiles) plus 200 field permutations.
6. **Models** (`models.py`):
   - Primary: exact Newton-IRLS L2 logistic (sklearn's objective; matches lbfgs to < 1e-8), leave-one-home-group-out
     on DEV, with a 2,000-draw concept-clustered **refit** bootstrap.
   - Secondary: conditional logit, LPM with field + cohort FE (concept and two-way clustered), boundary
     interaction, relatedness head-to-head, placebos.
   - Field-level robustness: leave-one-field-out, a crossed concept × field bootstrap, and two- and field-clustered
     SEs.
   - Power simulation and the explanatory ladder.
7. **Freeze → unseal once.**
   - `frozen_spec.json` (covariates, standardisation constants, thresholds, seeds, hashes, held-out ids) is hashed
     into `logs/seal.log`.
   - Pre-unseal checklist: held-out outcome columns absent from every table, and a git commit
     `a3234b7` of the code and frame.
   - `seal.py` refuses a second unseal. Held-out models are scored without re-tuning, and every sensitivity is
     reported (see below).
8. **Audit.** `audit.py` re-derives the held-out pooled ΔAUC, the per-group values and the H3 partial ρ with
   separate code: sklearn lbfgs, a Mann-Whitney AUC, its own P_j(−c) and its own rank residualisation. **All match
   to 1e-6** (`audit.json`).

### Sensitivities (held-out ΔAUC, never used for the verdict)

All CIs include 0, and every |ΔAUC| is ≤ 0.0023:
- R_abs1 +0.0008;
- R_abs2 0.0000 (the direction's literal "≥ 2 works" outcome);
- R_abs3 0.0000;
- n_early ≥ 5 (iteration-1-exact) −0.0004;
- newborn-only +0.0023 [−0.0039, 0.0128] (n = 387);
- excluding intersection-born concepts 0.0000;
- primary-topic fields instead of venue fields 0.0000;
- ungrounded "match" counts 0.0000;
- P_j_train −0.0004;
- without P_j −0.0011 [−0.0026, 0.0000];
- B5 over t0..t0+4 0.0000;
- gateway variants (degree −0.0004, betweenness −0.0001, φ_min 0.0000, recomputed S0 0.0000);
- slice field size −0.0001.

### Tests

| test | result |
|---|---|
| T0 unit tests (9) | all pass (`results/unit_tests_T0.json`): rarefaction vs Monte Carlo, Kleinberg, matcher (stem, IoT hyphen/stop words, microRNAs, word boundary), onset, home rule, episode R, seal gate, planted positive control, placebo degree/weight preservation |
| T1 matcher regression vs iteration 1 (3 files, P78 phrases) | not exact equality: the new matcher is a strict subset, precision 1.00, recall 0.95 (it misses stem-only inflections of non-final tokens) |
| T2 50-file inspection | found generic single-token aliases; fixed and re-hashed **before** the full scan (`deviations.json: t2_lexicon_fix`) |
| T3 | recomputed backbone ρ = 1.000 ✓; P78 log yearly counts vs iteration-1 snapshot matches, median ρ = 0.999 ✓; base totals identical ✓; **t0 agreement with the iteration-1 API t0 is 53% (< 70% target)**, because API title+abstract counts are about 2× title counts and cross 20 earlier; API audit **not done** (pool below floor) |
| T4 | κ = 0.20 (< 0.6, so adjudicated); hand-check agreement 90% ✓; filter did not beat exact-name, so the TAG rule was used |
| T5 | second bootstrap seed moves CI ends by 0.00007 (< 0.01) ✓; iteration-1 replication same sign ✓ |
| T6 | pre-unseal checklist passed (`logs/seal.log`) |
| T7 | independent audit, all match ✓ |
| shuffled-input controls (`audit_placebo.py`) | held-out ΔAUC with shuffled R: −0.0005 ± 0.0019 (20 shuffles); a planted 1-SD gateway effect is detected (+0.044); both H3 tests give 0/40 false positives on shuffled outcomes; H3 per-group ρ re-derived exactly, DL pooled 0.068 (re-derived 0.0676) |

### Deviations (full list with reasons in `results/deviations.json`)

- The OpenAlex API key had 0 credits and the anonymous pool 999, below the 1,500 floor. Therefore:
  - **there is no API audit**;
  - **insularity I_j = NA**, dropped from X0 before freezing.

  2 probe calls were made (`credits_log.csv`).
- Wikidata aliases came from SPARQL instead of wbgetentities (429 rate limiting).
- LLM budget raised from $2 to $3.50 because there were 13k candidates rather than the planned ≤ 5k. Spent:
  **$2.28**.
- Home window counted from t0 on.
- Base type article|review excludes the snapshot's `conference-paper` type, so conference-heavy CS is
  under-covered.
- Grounding rule = TAG (T4).
- Post-unseal fixes, with the frozen spec unchanged:
  - one cohort episode with an undefined outcome (0/0) is excluded;
  - the held-out crossed bootstrap was mis-indexed and was recomputed by `fix_pigeonhole.py`.

## Layout

| path | content |
|---|---|
| `method.py` | end-to-end orchestrator (idempotent; `--from STEP`, `--only STEP`) |
| `common.py` | constants, field → group map, OpenAlex-like analyser (copied from art_yrradSC27HtQ), helpers |
| `rangefile.py` | column-pruned HTTP-range parquet reader (verbatim from art_yrradSC27HtQ) |
| `probe.py`, `timing_probe.py` | step 0: schema probe, read timing (`logs/schema_leaf_paths.json`, `logs/timing_probe.json`) |
| `lexicon.py`, `prescreen.py`, `wikidata_aliases.py` | steps 1–2: lexicon v0/v1, 1% pre-screen, aliases |
| `matcher.py` | Aho-Corasick + stemmed positional verification |
| `scan_full.py` | step 3: the single full-snapshot scan (per-file parts, resumable) and merge |
| `panel.py` | dense per-concept count arrays, onset rule |
| `llm.py`, `grounding.py` | step 4: budgeted OpenRouter client, benchmark, sense filter, precision gate |
| `oa_client.py` | credit-capped OpenAlex client (unused beyond the probes: pool below floor) |
| `frame.py` | step 5: frame, home rule, episodes, outcomes (DEV only before the seal) |
| `backbones.py` | step 6: frozen / recomputed backbones, gateway_j,s, placebo backbones |
| `features.py` | step 7: episode covariates, concept-level G family and art_33 reference indicators |
| `models.py` | steps 8–9: DEV analysis + FREEZE, held-out scoring, H3 |
| `seal.py` | the freeze/unseal gate (raises without a matching spec hash or on a second unseal) |
| `checks.py`, `audit.py`, `audit_placebo.py`, `fix_pigeonhole.py`, `exploratory_domains.py` | T1/T3, replication, T7 audit, post-hoc diagnostic fix, exploratory per-domain table |
| `report.py`, `make_variants.py` | figures, `method_out.json`, full/mini/preview variants |
| `tests/test_units.py` | T0 unit tests |
| `frame_concepts.csv` | **authoritative S1 concepts** (12,499; split column; precision, coverage, home, flags) |
| `episodes.csv` | **authoritative S1 episodes** (27,393; outcomes for all splits after the unseal) |
| `concept_outcomes.csv` | O1, O3, O2r_m30/m50, O2_raw, N_outcome for every frame concept |
| `concept_features_basic.csv` | G, G_A, G_btw, REL_home, RS, DOM_*, count/label indicators, B5 (for iteration 3) |
| `episode_features.csv` | episode covariates used by the models |
| `dev_episodes_with_oof.csv`, `heldout_episodes_with_pred.csv`, `cohort_episodes_with_pred.csv` | predictions |
| `sens_episodes_{ptopic,match,b5_t0p4}.csv` | sensitivity episode tables |
| `grounding_benchmark.csv`, `grounding_precision.csv`, `grounding_report.json`, `sense_filter.joblib` | grounding |
| `results/handcheck_sheet.csv`, `results/handcheck_labels.csv` | the executor's 60 hand-read pairs |
| `frozen_spec.json`, `logs/seal.log` | the frozen specification and seal evidence |
| `results/h1_dev.json`, `results/h1_heldout.json`, `results/h3_results.json` | all model results |
| `results/backbones.json`, `placebo_gateways.npy`, `placebo_perm_gateways.npy` | backbones and placebos |
| `results/exploratory_domain_specificity.json` | exploratory per-domain gateway table (post-unseal) |
| `results/checks.json`, `results/p78_agreement.csv`, `audit.json`, `results/audit_placebo.json` | T1/T3, replication, T7, shuffled-input controls |
| `results/deviations.json`, `credits_log.csv`, `llm_cost_log.csv` | deviations and cost ledgers |
| `results/prescreen_summary.json`, `results/prescreen_dropped.csv`, `results/frame_summary.json` | lexicon / frame summaries |
| `method_out.json` (+ `full_`, `mini_`, `preview_`) | exp_gen_sol_out output: one example per episode (DEV: OOF LOGO; held-out/cohort: frozen model) |
| `figures/` | `forest_dauc`, `ladder_dauc`, `placebo_hist`, `coef_secondary`, `leave_one_field_out`, `gateway_map` (PNG + PDF) |
| `lexicon_v0.parquet`, `lexicon_v1.parquet`, `frozen_lexicon.sha256` | frozen lexicons |
| `scan/agg_counts.parquet` | **kept**: merged scan counts (45 MB) |
| `scan/reservoir/part_*.parquet` | **kept**: hash-sampled matched titles (1.84M rows, 3 parts of 18–48 MB) behind every LLM label; read with `common.read_parquet_parts` |
| `scan/llm_cache/` | **kept on the run volume** (thousands of hash-named files; excluded from the published repo): raw paid LLM responses |
| `scan/year_field_totals.npz`, `scan/co_by_year.npz`, `scan/wikidata_aliases.json`, `scan/untagged_*.parquet`, `scan/scan_info.json` | small scan outputs |
| `reproducibility.md` | exact commands, runtimes, seeds |

Every file in the workspace is below 100 MB. The reservoir and the 1% title sample are stored as `part_*.parquet`
splits. The dense count caches `scan/arrays_*.npz` are compressed (23 MB and 29 MB). The running reservoir copy
used during the scan is deleted after the merge. Suggested upload exclusions: `(^|/)scan/llm_cache/`, `(^|/)scan/parts/`,
`(^|/)scan/stage_test_parts/`, `(^|/)scan/aborted_v1a_parts/`, `(^|/)scan/oa_cache/`.

## How to run

```bash
./restore.sh                              # .venv + snapshot metadata (free)
.venv/bin/python tests/test_units.py      # T0 (no network)
.venv/bin/python method.py                # resumes; skips steps whose outputs exist
```

The full run from scratch takes about 1.5 h:
- scan: 33 min;
- precision gate: 15 min and about $2.3 of OpenRouter (it needs `OPENROUTER_API_KEY` / `OPENROUTER_BASE_URL`);
- models: about 25 min.

LLM responses are cached in `scan/llm_cache/`, so a rerun costs nothing.

The seal permits exactly one unseal per frozen spec. To rerun the confirmatory part from scratch, a new freeze
(new `logs/seal.log`) is required, and that would no longer be a sealed test.

## Restoring removed files

These paths are marked `delete` in `.aii/manifest.yaml` and are removed after the round. Each command below brings
its path back.

| deleted path | restore command |
|---|---|
| `.venv/` | `./restore.sh` (runs `uv venv .venv --python=3.12` and `uv pip install --python .venv/bin/python -r pyproject.toml --extra-index-url https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match`, with the exact pinned versions) |
| `scan/arrays_grounded.npz` | `.venv/bin/python frame.py grounded` (rebuilt from `scan/agg_counts.parquet`) |
| `scan/arrays_match.npz` | `.venv/bin/python frame.py match` (rebuilt from `scan/agg_counts.parquet`) |
| `scan/sample_titles/` | `.venv/bin/python prescreen.py sample` (the same 20 files, chosen with seed 20260928) |
| `__pycache__/` | created automatically by Python |

Kept items:
- `snapshot/` (14 MB of manifests and legacy concepts): `./restore.sh` re-downloads it if it is missing.
- `scan/parts/`, `scan/stage_test_parts/`, `scan/aborted_v1a_parts/` (per-file scan parts; the last two are obsolete
  test and aborted runs): these can be regenerated with `.venv/bin/python scan_full.py --workers 5`.
- `scan/llm_cache/` (raw LLM responses).

The MiniLM model (`sentence-transformers/all-MiniLM-L6-v2`) sits in the run's shared HF cache, not in this
workspace. It is re-downloaded automatically on first use.
