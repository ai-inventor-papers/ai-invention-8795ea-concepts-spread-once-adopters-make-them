# How newborn scientific concepts hop between fields

AI Inventor, invention loop iteration 2, artifact `gen_art_experiment_6` (plan `gen_plan_experiment_2_idx2`).

**Question.** Once a newborn concept has spread beyond its home field, which field does it enter next? Four tests:
1. **H2 entry.** Does relatedness to the off-home fields that currently *retain* the concept, weighted by their
   gateway centrality, add to the standard next-entry baselines? The baselines are relatedness-to-home, target-field
   size, Hidalgo relatedness density and the target field's own centrality.
2. **Rescue.** Are retained gateway episodes fed by re-import from other non-home fields?
3. **Relay.** Do retained gateway episodes seed later field entries beyond what availability predicts?
4. **Trajectories without predefined classes, and an ordering test.** Does the first retained gateway field precede
   the concept's entropy take-off?

The data are the full OpenAlex works snapshot: 476,196,327 works in 2,040 parquet files from the 2026-09 release,
read at zero API credits. Fields are the 26 OpenAlex fields, and the backbone is the frozen iteration-1 1998-2002
field PMI network with its gateway centrality.

## Headline results

Development split: dev-home fields CS, Engineering, BGM and Medicine, with t0 in 2003-09. Held-out split: the other
fields with t0 in 2003-09, plus the whole 2010-14 cohort. The held-out stage was run **once**, after
`results/frozen_spec.json` was hashed into `results/freeze_log.txt`.

| test | dev (274 concepts) | held-out (369 concepts), frozen rule |
|---|---|---|
| H2: LR M2 vs M0 (clogit, concept-year strata) | 38.6, p=5e-10 | **71.7, p=2e-17** |
| d (standardised) [concept-bootstrap 95% CI] | 0.25 [0.18, 0.32] | 0.30 [0.24, 0.37] |
| label-permutation p (phi and g permuted jointly) | 0.009 | 0.001 |
| degree-preserving rewired-backbone p | 0.030 | 0.015 |
| per-group d (Physical / LifeEnv / Social / Cohort) | - | 0.33 / 0.18 / 0.24 / 0.29, all positive; DL pooled 0.28 [0.22, 0.35], I2=0 |
| **gateway weighting beyond plain retaining relatedness** (M3 vs M1; g-only permutation p) | LR 4.6, p=0.31 | LR 5.4, **p=0.17** |
| mean within-stratum AUC, M0 -> M2 | 0.801 -> 0.805 | 0.809 -> 0.817 (frozen dev coefficients: 0.807 -> 0.815) |
| single blocks: size / density / phi_home / own gateway / d | 0.71 / 0.61 / 0.58 / 0.48 / 0.56 | 0.76 / 0.59 / 0.57 / 0.45 / 0.55 |
| **H2 entry decision** | - | **CONFIRMED** (every frozen criterion met) |
| ordering: share of top-O2r concepts whose first retained gateway field precedes entropy take-off | 0.71 (peripheral 0.70) | **0.66, sign p=0.003** (peripheral 0.57, p=0.12; McNemar p=0.09) -> CONFIRMED by the frozen rule |
| lead-lag placebo (gateway scores permuted) | p=0.18 | p=0.63: the panel does **not** single out gateway fields |
| rescue: R1 retained x top-gateway on background-adjusted provenance | 1.47 [-0.16, 3.10] | -0.22 [-1.12, 0.68], **not supported** |
| rescue: Hanski connectivity on retention (R2) | +0.032 [0.007, 0.058] | +0.009 [-0.017, 0.035] |
| relay: fepois retained x gateway_j | 18.0 [4.2, 31.9] | -1.3 [-4.9, 2.3], **not supported** |
| H1 replication (gateway_j on retention, concept FE) | +0.017 (CI spans 0) | +0.005 [-0.022, 0.033]: **iteration-1 lead did not replicate** |
| trajectories: DTW k-medoids, k by silhouette + bootstrap ARI | k=2, median ARI 1.0, silhouette 0.29 | independent recluster ARI 0.54 |

**How to read this.**
- **Entry.** Fields related to where the concept is *currently retained* off-home are entered next. This holds in
  every held-out group, beyond size, density, home relatedness and own centrality, and survives both placebos.
- **What does not hold.** The *gateway weighting* of those retaining fields adds nothing detectable (g-only
  permutation p = 0.17 on held-out). The confirmed mechanism is relatedness to retaining fields, not gateway
  brokerage. Target-field size remains by far the strongest single predictor (AUC 0.76), and the incremental AUC is
  small (+0.008).
- **Trajectories.** Two stable classes with nearly equal volume: "integrating" (entry, retention, entropy and
  gateway share all rise) and "localized" (flat breadth). On held-out data the localized class is dominated by
  Medicine-home concepts (42 of 60).
- **Negative results.** Rescue and relay are not supported, and the iteration-1 gateway-retention lead did not
  replicate on this larger frame.

## What was done

1. **Lexicon (`build_lexicon.py`).** OpenAlex legacy concepts, levels 2-5 with a Wikidata id, 60,859 concepts.
   Common English single words and very short forms are dropped. The lexicon is hashed in `results/lexicon_hash.txt`.
2. **Pass 1 (`pass1.py`, 23 min, 4 workers).**
   * Reads 9 leaf columns of every works file through HTTP range requests (from iteration-1 `rangefile.py`).
   * Matches titles with a word-boundary Aho-Corasick automaton (`lib/matcher.py`): 141M title hits on 129M base works.
   * Records each hit's legacy-tag flag and score, venue field (iteration-1 source -> field map) and primary-topic field.
   * `aggregate.py` builds dense concept x year x field counts in `scan/agg_counts.npz`.
3. **P0 and candidates (`cand.py`).** The outcome-blind P0 rule drops 3,102 concepts common before 2003. Onset uses
   the iteration-1 rule: t0 is the first year with >= 20 grounded works, t0 in 2003-2014, >= 30 works in t0..t0+2.
   This gives 12,901 onsets, of which **653 are newborn**.
4. **Pass 2 (`pass2.py`, 12.7 min).** For the newborn candidates it keeps work id, title, references and authors, and
   builds the global work-id -> venue-field map used for background references.
5. **Grounding (`grounding.py`, `label_bench.py`).**
   * 400 stratified (concept, title) pairs, labelled by `google/gemini-2.5-flash-lite`. `qwen/qwen3-30b-a3b-instruct-2507`
     double-labels 150 of them, and 60 were checked by hand (`benchmark/hand_labels.csv`). Total cost $0.0074.
   * The grounding rule is legacy tag (score >= 0.3) AND title match, plus untagged works. Its test precision is
     0.996 (population-weighted), >= 0.94 in every domain, with 78% recall relative to title-only.
   * The MiniLM + logistic sense filter is **uninformative**: test AUC 0.24 on only 12 negatives in 400. It dropped
     no concept. See `results/grounding_report.json`.
6. **Frame (`frame.py`).**
   * 653 concepts: dev 279, held-out field 126, held-out cohort 248. 1,865 off-home episodes.
   * Home is taken from the first 30 labelled works.
   * Outcomes use the iteration-1 definitions: O1, O3, O2r = rarefied venue-field richness at t0+6..8.
   * Held-out outcomes stayed **sealed**: `lib/frame_io.py` raises until the freeze log exists.
7. **Analyses (`method.py` + `lib/`).**
   * `lib/h2.py`: the state machine (entered, retaining, lost) and concept-year risk sets.
   * `lib/stats_core.py`: own vectorised conditional logit, validated against statsmodels to 0.05%; within-FE OLS and
     Poisson FE with CRV1 SEs; DerSimonian-Laird pooling.
   * `lib/rescue_relay.py`: background-adjusted citation provenance with shared-author links removed, Hanski
     connectivity, and the availability-null relay.
   * `lib/traj.py`: DTW k-medoids, Gaussian HMM (BIC), a Pelt change-point detector calibrated to a 5% false-alarm
     rate on year-shuffled series, and the lead-lag / event-study panels.
8. **Tests.**
   * `tests/test_units.py` (T0): matcher boundaries and plurals, rarefaction vs Monte Carlo, onset, clogit vs
     statsmodels, FE-OLS, DerSimonian-Laird. All pass: `results/unit_tests_T0.json`.
   * Planted control on the real risk-set structure: detection 100% at p < 0.001; null rejection 2% at 0.01.
   * `audit.py` (T7): an independent recomputation.
     * R1 and p_gw agree exactly.
     * The H2 LR differs by 7.8%. statsmodels' exact conditional likelihood gives LR 77.3 and d 0.34, against the
       own Breslow form's 71.7 and 0.30, because 30% of strata have more than one event. The conclusion is unchanged,
       and the Breslow form used here is the conservative one.
   * `audit_placebo.py`: labels shuffled within strata reject in 0 of 20 runs; a random gateway year gives an
     ordering share of 0.43 (never at or above 0.655); the exact-likelihood DL-pooled d is 0.32 [0.25, 0.39].
   * API audit on 40 frame concepts: snapshot title counts equal OpenAlex `title.search` counts (median ratio 1.00,
     Spearman 0.999), and grounded counts are 95% of them.

Every departure from the plan is in `results/deviations.json`. The larger ones:
* no Wikidata aliases;
* frame restricted to newborn concepts;
* episode target not met (1,865 < 4,000);
* MathDec has no concepts, so the sign rule was pinned before the freeze to 3 of 3 field groups plus the cohort;
* relay Poisson re-specified with a continuous gateway interaction before the freeze, because the tercile dummies
  separated;
* the supplied OpenAlex key was exhausted (HTTP 429), so the 40 audit calls used the anonymous pool.

## Layout

| path | content |
|---|---|
| `config.py` | constants, splits, seeds (SEED=20261001) |
| `build_lexicon.py`, `pass1.py`, `aggregate.py`, `cand.py`, `pass2.py` | snapshot pipeline (steps 0-2, 5) |
| `grounding.py`, `label_bench.py` | benchmark sampling, LLM labels, sense filter, rule comparison (step 3) |
| `frame.py`, `agreement.py`, `audit_api.py` | frame, episodes, iteration-1 agreement, API audit (step 4) |
| `method.py` | stages `dev` -> `freeze` -> `heldout` -> `outputs` (steps 6-9) |
| `make_outputs.py` | figures and `method_out.json` |
| `audit.py`, `audit_placebo.py` | independent re-derivations (statsmodels exact clogit, sklearn AUC, inline DL) and placebos that must fail -> `results/audit.json`, `results/audit_placebo.json` |
| `requirements.lock.txt`, `install.sh` | all 85 installed packages pinned; environment rebuild |
| `lib/` | `matcher.py`, `rangefile.py` (iteration 1), `lib_outcomes.py` (iteration-1 outcome code), `h2.py`, `stats_core.py`, `rescue_relay.py`, `traj.py`, `frame_io.py` (sealing guard) |
| `tests/test_units.py` | T0 unit tests |
| `inputs/` | frozen backbone (`field_backbone.json`), source -> field map, works manifest, concepts entity, iteration-1 outcomes |
| `results/frame_concepts.csv`, `results/episodes.csv` | frame and episodes (S1-compatible columns) |
| `results/dev_result.json`, `results/heldout_result.json`, `results/frozen_spec.json`, `results/freeze_log.txt` | results and the freeze record |
| `results/entry_risk_sets_{dev,heldout}.parquet` | every candidate-field row with regressors and outcomes |
| `results/rescue_*.csv`, `results/relay_*.csv`, `results/trajectories_*.csv`, `results/cluster_assign_*.csv`, `results/ordering_*.csv` | analysis tables |
| `results/grounding_report.json`, `results/grounding_concepts.csv`, `benchmark/` | grounding benchmark, labels (LLM x2, hand) |
| `results/agreement.json`, `results/api_audit.json`, `results/audit.json`, `results/unit_tests_T0.json` | checks |
| `results/deviations.json`, `results/openrouter_cost.json`, `results/credits_log.csv` | deviations and spend |
| `figures/` | AUC forest, held-out group forest, incidence-function curve, trajectory clusters, event studies, 4 case field-flow plots (cluster medoids and extreme relay episodes) |
| `method_out.json`, `full_method_out.json`, `mini_method_out.json`, `preview_method_out.json` | exp_gen_sol_out outputs. Datasets: `entry_events_dev` (36,222), `entry_events_heldout` (46,433), `retention_episodes_{dev,heldout}`. Predictions `predict_M0...` vs `predict_M2...` are within-stratum probabilities from the frozen dev coefficients. |
| `scan/agg_counts.npz`, `scan/pass2/{w,h}*.parquet` | kept aggregates and frame work rows. These stay on the run's volume; files >= 100 MB are not in the published repo. |

## How to run

```bash
bash install.sh
.venv/bin/python build_lexicon.py
.venv/bin/python pass1.py --workers 4 && .venv/bin/python aggregate.py && .venv/bin/python cand.py
.venv/bin/python pass2.py --workers 4
.venv/bin/python grounding.py sample
.venv/bin/python label_bench.py --model google/gemini-2.5-flash-lite --out benchmark/labels_primary.csv
.venv/bin/python label_bench.py --model qwen/qwen3-30b-a3b-instruct-2507 --n 150 --out benchmark/labels_second.csv
.venv/bin/python grounding.py fit && .venv/bin/python frame.py && .venv/bin/python agreement.py
.venv/bin/python method.py dev && .venv/bin/python method.py freeze && .venv/bin/python method.py heldout
.venv/bin/python method.py outputs && .venv/bin/python audit.py && .venv/bin/python tests/test_units.py
```

`OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY` must be set for labelling. `audit_api.py` optionally reads
`OPENALEX_API_KEY` and otherwise uses the anonymous pool. No key is ever written to a file.

## Restoring removed files

Only one path is deleted after the run (see `.aii/manifest.yaml`):

| removed path | restore with |
|---|---|
| `.venv/` | `bash install.sh` |

Kept on the run's volume, but not published to the repository (`upload_ignore_regexes`):

| path | how to regenerate in a fresh clone |
|---|---|
| `scan/pass1/` (per-file hit records) | `.venv/bin/python pass1.py --workers 4` (about 23 min; the OpenAlex snapshot drifts between releases, and `scan/agg_counts.npz` holds the aggregates used by every analysis) |
| `scan/pass2/m*.npz` (global id -> field map) | `.venv/bin/python pass2.py --idmap-only` (requires `scan/pass1/`) |

The MiniLM model (`sentence-transformers/all-MiniLM-L6-v2`) lives in the run's shared HF cache and is re-downloaded
automatically.
