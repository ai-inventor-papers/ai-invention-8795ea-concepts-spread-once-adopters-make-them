# Cheng's "ideational consistency": a large volume effect that is current size, and a reach reversal

AI Inventor, invention loop iteration 5, artifact `gen_art_experiment_14` (plan `gen_plan_experiment_2_idx2`).
This artifact rebuilds the ideational-consistency measure of Cheng et al. (2023, *ASR* 88:522-561) on this run's
grounded OpenAlex paper-topic-author rows. It uses 12,499 EXP5 frame concepts plus the 1,443-concept 2015-17 EXP10
cohort. It then asks two questions:

1. Does Cheng's volume result replicate, and how much of it survives a current-size control?
2. Does the same trait point the other way for later cross-field **reach** than it does for volume and **depth**?

The spec and predictions were sealed before any model was fitted (`logs/seal.log`; first git commit). Cost: cache
only, 0 OpenAlex credits, $0 LLM, CPU only.

> **Selection data, not confirmation.** All bodies (DEV, OLD_HELDOUT, COHORT_2010_14, COHORT_2015_17) had their
> outcomes read by EXP5/EXP8/EXP10 before this artifact. Consistency itself was never screened on them, so the
> tests are a priori but not confirmatory. Confirmation belongs to the Frame N experiment.

## Headline

**Frozen verdict** (`results/cheng_verdict.json:verdicts`): **REVERSAL CONFIRMED (on selection data), REVERSAL
REPLICATED, SIZE-DOMINATED, DEPTH-REACH SPLIT.** P4 (O3) and P6 (within-concept entries) did not hold.

| quantity | value | source (file:key path) |
|---|---|---|
| A1-NB (Cheng spec, NB2), b on z-consistency, HOME | **0.428** (+53.5%/SD) [0.399, 0.458]. Cheng: b = .43, +53% | `cheng_panel_models.json:builds.HOME.joint.A1_NB.coef.zCONS` |
| A1 PPML (Cheng spec), % per SD | +83.1% [+70.6, +96.5] | `cheng_panel_models.json:builds.HOME.joint.A1.coef.zCONS.pct_per_sd` / `.pct_ci` |
| A2 = A1 + log V(t), % per SD | **+1.3%** [+0.5, +2.1] | `cheng_panel_models.json:builds.HOME.joint.A2.coef.zCONS` |
| A3 = A2 + concept FE, % per SD | +1.4% [+0.7, +2.0] (CRV1) | `cheng_panel_models.json:builds.HOME.joint.A3.coef.zCONS` |
| RATIO b_A2 / b_A1 (500-draw concept-cluster bootstrap) | **0.021 [0.009, 0.035]** | `cheng_panel_models.json:builds.HOME.joint.ratio_boot.ratio` / `.ratio_ci` |
| RATIO, ALL-papers build | 0.024 [0.013, 0.038] | `cheng_panel_models.json:builds.ALL.joint.ratio_boot` |
| B-raw: Spearman(CONS_early_home, V(t0+3)), primary | **+0.256 [+0.239, +0.274]** | `cheng_static.json:volume.EXP5_pooled\|volume.B_raw_spearman_V_t0p3` |
| B-size: psp(CONS_early, V(t0+3) \| log V(t0+2)) | +0.047 [+0.029, +0.066] | `cheng_static.json:volume.EXP5_pooled\|volume.B_size_psp_V_t0p3_given_logV_t0p2` |
| **P3** psp(CONS_early_home, O2r_m50 \| B5), primary, n = 6,913 | **-0.069 [-0.093, -0.047]** | `cheng_static.json:trait.EXP5_pooled\|CONS_early_home.psp.O2r_m50` |
| P3 DL over 5 groups (I2, groups negative) | -0.079 [-0.102, -0.056] (I2 = 0.00, 5/5 negative) | `cheng_static.json:DL.EXP5_pooled.O2r_m50` |
| P3 replication, 2015-17 cohort, n = 615 | **-0.111 [-0.197, -0.030]** (MDE 0.119) | `cheng_static.json:trait.COHORT_2015_17\|CONS_early_home.psp.O2r_m50` |
| O2r_resid (size-residualised reach), primary | -0.077 [-0.101, -0.055] | `cheng_static.json:trait.EXP5_pooled\|CONS_early_home.psp.O2r_resid` |
| depth: O1c / O1b / O3, primary | -0.000 [-0.019, +0.017] / -0.004 [-0.022, +0.015] / -0.001 [-0.020, +0.017] | `cheng_static.json:trait.EXP5_pooled\|CONS_early_home.psp.{O1c,O1b,O3}` |
| **P5** paired diff psp(O1c) - psp(O2r_m50), common set | +0.035 [+0.004, +0.066] (DL over groups: +0.037 [-0.009, +0.083], I2 = 0.43) | `cheng_static.json:trait.EXP5_pooled\|CONS_early_home.paired_diff.O1c-O2r_m50`; `DL.EXP5_pooled.O1c-O2r_m50` |
| P6 / C1: within-concept, entries(t+1) on z CONS_home(t), concept + year FE | **+0.025** (boot CI [+0.004, +0.048]): opposite to P6 | `panel_C.json:C1.coef.zCONS`, `panel_C.json:C1.boot` |
| Holm (one-sided) P1-A1 / P2 / P3 / P4 / P5 | 8e-63 / 0.006 / 0.002 / 0.46 / 0.031 | `cheng_verdict.json:holm_family_one_sided` |

**Reading.**
- **Cheng's result replicates.** Their exact design (next-year volume, age and year controls, no current-size
  control, over-dispersed count model) gives b = 0.428 against their .43.
- **It is almost entirely current size.** Adding log V(t) keeps about 2% of the coefficient, and concept fixed
  effects leave the same +1.4%.
- **As an early trait, consistency points the other way for reach.** It correlates positively with volume three
  years on, but net of the B5 size/growth/breadth baseline it predicts less later rarefied cross-field richness.
  This holds in every body, in all five field groups (I2 = 0), and replicates on the fresh-ish 2015-17 cohort.
  - The frozen R2/R3 rung ladder of EXP10 keeps it: R3 gives -0.098 [-0.176, -0.024]
    (`cheng_static.json:cohort_rungs.R3|O2r_m50`).
- **Consistency adds nothing on depth.** The O1c/O1b/O3 partials are all about 0.
  - The "DEPTH-REACH SPLIT" label is therefore a null-versus-negative split, not a positive depth effect.
  - Its group-pooled DL CI includes 0.
- **The reach association is between concepts, not within them.** Within concepts, a more consistent year is
  followed by slightly *more* new off-home field entries (C1). The negative reach association is a between-concept
  property of the early trait.
- **Palla-type size × consistency interaction: none** (`palla.json:results.EXP5_pooled|O3.interaction` =
  -0.001 [-0.021, +0.020]).

The paper paragraph, with every number tagged by its key path, is in `reconciling_cheng.md`.

## What each test found

- **S2, construct identity** (`results/identity_check.json`).
  - CONS_early_home (the count-weighted cosine) has Spearman **0.77** with Exp11's unweighted Jaccard edge
    persistence, 0.62 with EXP10 edge_persistence_home, and 0.47 with -NOVCHURN_home.
  - It is only moderately size-laden: 0.34 with log early volume, below the 0.6 flag.
  - It is 0.91 with Cheng's verbatim support-restricted variant (CONS_r).
- **Test A, replication panel** (`results/cheng_panel_models.json`). 105,839 concept-years, 12,311 concepts (HOME).
  - The pattern is the same on ALL, per body (A2/A1 ratios 0.008-0.031) and per group. The DL over groups for A2 is
    +0.009 [+0.004, +0.014].
  - Social embeddedness (prior co-author density) is negative in A1 as in Cheng: NB -0.082, PPML -0.227.
  - The PMI embeddedness *analogue* is negative (-0.094). Cheng's word2vec measure was positive, and ours is not
    the same measure (flagged in every table).
- **Test B, static trait** (`results/cheng_static.json`).
  - Every CONS variant and body gives a negative reach partial (see `fig_reach_depth_forest`).
  - The ALL build is more negative still: -0.103, and ALL minus HOME = -0.032 [-0.052, -0.013]
    (`results/coupling.json`).
  - The second-order embedding analogue EMB_cos is the most negative: -0.173 [-0.195, -0.149]. This is exploratory.
- **Test C, within-panel** (`results/panel_C.json`). 79,159 concept-years.
  - C1: entries +2.5%/SD, CRV1 CI [+0.1%, +5.0%].
  - C2: home-share change +0.0010 [-0.0003, +0.0023]. So there is no within-concept "consolidation → less reach"
    dynamic, consistent with Exp11's closure null.
- **Test D, Palla** (`results/palla.json`). No size × consistency interaction on O3, O2r_m50 or O1c in either body.
  The reach penalty is present in all three size terciles (`fig_palla`).
- **Predictive check** (`results/predictive_comparison.json`). Adding CONS_early_home to a DEV-fitted rank-OLS on B5
  does not raise held-out Spearman with O2r_m50 (Δ = -0.0008 OLD_HELDOUT, -0.0004 COHORT_2010_14, +0.0018
  COHORT_2015_17; all CIs include 0). The partial association is real but small next to B5.
- **Audit** (`results/audit.json`; all re-derivations pass).
  - statsmodels GLM vs pyfixest on a 2,000-concept subset: |diff| < 1e-11.
  - statsmodels OLS-on-ranks psp vs the pipeline: 3e-17.
  - Hand DL: exact.
  - A shuffled-CONS within-group placebo gives a 95th percentile |psp| of 0.025, against the observed -0.069.

## Departures from Cheng and from the plan

Full list: `results/deviations.json`.
- **Neighbours.** Neighbours are OpenAlex topics (about 4.5k), so this is *topic co-usage* consistency on a coarser
  vocabulary than WoS terms.
- **Embeddedness.** EMB is a backbone-PMI analogue (no text embeddings).
- **Social embeddedness.** SOC ties come only from the concept's own papers (OpenAlex author ids, prior 10 years,
  <= 15 authors as Cheng).
- **Estimator.** PPML with FE instead of Cheng's multilevel over-dispersed Poisson, plus an NB2 twin.
- **Consistency support rule.** Consistency is NaN, not 0, below the minimum support (>= 3 papers and >= 2 topics
  in both years). 8.2% of early values are NaN; F5 was not triggered.
- **Cheng's text.** The publisher page returned 403. Cheng's definitions are quoted verbatim from the research
  artifact's saved full-text extract (`prereg.md`).
- **Post-seal edit.** One sealed lib file changed after the seal: `cheng.py` gained a null-author-id guard before
  S1 ran. No definition changed.

## Layout

| path | content |
|---|---|
| `method.py` | orchestrator: `--only S0..S8,S3NB`, `--sample N` (S1 staging), `--quick` (10% smoke runs) |
| `lib/cheng.py` | the measures: CONS, CONS_r, EMB, EMB_cos, SOC per concept x year x build |
| `lib/build.py` | S1: loads Exp11 frame_matches_long / EXP10 passC_early, parallel build, V(t), static traits |
| `lib/identity.py` | S2 construct-identity check |
| `lib/panel_cheng.py` | S3 test A (PPML, NB, IRLS ratio bootstrap) and S5 test C |
| `lib/static_cheng.py` | S4 test B, S6 test D (Palla), S7 test E (coupling); multi-outcome concept bootstrap |
| `lib/outputs.py` | S8: Holm, mechanical verdict, figures, method_out.json, reconciling_cheng.md |
| `lib/s0_spec.py`, `prereg.md`, `results/frozen_spec.json`, `logs/seal.log` | sealed spec and predictions |
| `lib/{ego,ego_ctx,ego_yearly,fe_stats,panel_m}.py` | copied verbatim from Exp11 (SELF-topic rule, backbone context) |
| `lib/{rq1stats,stats_core}.py`, `lib/ladder.py` | copied from EXP8 / EXP10 (psp, DL, Holm, cohort rungs) |
| `lib/provenance.py` | sha256 of every upstream input -> `results/provenance.json` |
| `audit.py` | independent re-derivations + placebo -> `results/audit.json` |
| `rederive.py` | headline numbers recomputed from raw inputs via statsmodels / QR + placebos -> `results/rederive.json` (all pass; C1 not re-derived) |
| `tests/` | U1-U8 unit tests (`uv run pytest -c pytest.ini tests/`); summary in `results/unit_tests.json` |
| `data/cheng_features.parquet` | 279,242 rows: ci, year, build (HOME/ALL), CONS, CONS_r, EMB, EMB_cos, SOC, n_papers, n_topics, n_authors |
| `data/cheng_static.parquet` | per concept: early traits (t0+1..t0+2) for both builds + support counts |
| `data/static_analysis_table.parquet` | the joined test-B table (B5, outcomes, V(t0+2), V(t0+3), traits) |
| `data/V_exp5.parquet`, `data/V_cohort.parquet` | TAG-grounded yearly volume (EXP5 1995-2022; cohort t0..t0+3) |
| `data/identity_table.parquet`, `data/boot_ratio_*_joint.npy` | S2 table; bootstrap draws of (b_A1, b_A2) |
| `results/cheng_panel_models.json` | test A: A1/A1-NB/A2/A3 x build x spec x body x group, ratio bootstrap, DL |
| `results/cheng_static.json` | test B: psp per body / trait / outcome, paired diffs, volume tests, DL, cohort rungs, MDE |
| `results/panel_C.json`, `palla.json`, `coupling.json`, `identity_check.json` | tests C, D, E, S2 |
| `results/cheng_verdict.json` | predictions P1-P6, Holm family, verdict labels, source key paths |
| `results/predictive_comparison.json`, `headline_numbers.json`, `audit.json`, `deviations.json`, `s1_build.json`, `provenance.json` | supporting records |
| `figures/fig_cheng_ladder`, `fig_reach_depth_forest`, `fig_palla` (.png + .pdf) | figures |
| `method_out.json` (+ `full_`, `mini_`, `preview_`) | exp_gen_sol_out: one example per concept (13,942); output = O2r_m50; `predict_B5` vs `predict_B5_plus_CONS` |
| `reconciling_cheng.md` | one paper paragraph, every number tagged with its JSON key path |
| `reproducibility.md`, `requirements.lock.txt`, `pyproject.toml` | environment, commands, timings |

Every file here is small (the largest is `full_method_out.json`, about 15 MB), so the whole workspace, including
`data/` and `results/`, is published with the repository. Nothing is kept only on the run's volume.

## How to run

```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml
uv run method.py                     # S0..S8 in order (S0 refuses to overwrite an existing seal)
uv run method.py --only S3NB         # A1-NB re-fit (as done in this run)
uv run audit.py
uv run rederive.py
uv run pytest -c pytest.ini tests/
```

The inputs are read-only from earlier artifacts of the same run, located through `AII_RUN_ROOT` (default: four
levels above this directory). They are Exp11 `data/frame_matches_long`, `yearly_panel`, `counts_m` and `inputs/`;
EXP5 `frame_concepts.csv` and `scan/agg_counts.parquet`; EXP8 `data/analysis_table.parquet`; and EXP10
`data/passC_early`, `analysis_cohort`, `passC_pre_agg`, `sealed/parts`, `ego_open_*` and `results/frozen_spec.json`.

## Restoring removed files

`.aii/manifest.yaml` marks only regenerable caches for deletion:

| removed path | restore with |
|---|---|
| `.venv/` | `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml` (exact pins: `requirements.lock.txt`) |
| `lib/__pycache__/`, `tests/__pycache__/` | recreated automatically on the next `uv run method.py` / import |
| `.pytest_cache/` | `uv run pytest -c pytest.ini tests/` |

`restore.sh` runs the environment step.
