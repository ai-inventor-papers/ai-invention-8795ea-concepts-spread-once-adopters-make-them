# Do concepts spread from fields that keep them?

AI Inventor, invention loop iteration 3, artifact `gen_art_experiment_7` (plan `gen_plan_experiment_1_idx1`).
This is a "deepen" move on the lead `art_N-mpomDZZ1ln` (EXP6).

EXP6 found that a newborn concept next enters fields related to the off-home fields that currently **retain** it (the
*retained frontier*, `d0_ret_rel`). Two tests follow.

1. **Retained frontier vs the field-standard rival.** Does `d0` survive the relatedness-density rival as the
   relatedness literature builds it? That rival is RCA > 1 density, ω = Σ_j U_j φ_jk / Σ_j φ_jk (Hidalgo 2007;
   Guevara et al. 2016; Boschma, Balland & Kogler 2015). We use four RCA variants plus share-weighted (volume) density.
   The test runs on an independent frame and passes a battery of specificity nulls.
2. **Abandonment penalty.** Given ever-entered density, are fields related to presences the concept has **dropped**
   (`d_lost`) entered less?

Zero LLM and zero OpenAlex spend. Everything is computed from cached EXP5/EXP6 scan arrays of the full OpenAlex
snapshot (2026-09 release).

## Headline results

**Setup.** The estimator is a conditional logit with concept-year strata and Breslow ties. The unit is concept × target
field × year. Every coefficient is per DEV-SD. The resampling unit is **the concept**, except for the crossed
bootstrap, which resamples concept × target field.

**Frames.**
- **Step 1**, robustness: EXP6's frame, whose evidence was seen once before.
- **Step 2**, the independent confirmation: EXP5's 12,499-concept frame **minus every EXP6 concept**.
  - Matching is on OpenAlex ID, Wikidata QID and normalised label. 658 concepts are dropped (30 of them by QID only),
    leaving 11,841.
  - The 4,486 DEV concepts were used to build and check the code, standardise, run the power analysis and fix the
    sign rule.
  - The specification was then **hash-frozen**: `logs/seal.log`, git commit `24da538`. The held-out units were
    scored **once**: `logs/unseal.log`, 0 code changes since the freeze.

| quantity | EXP6 held-out (robustness) | EXP5−EXP6 DEV | **EXP5−EXP6 held-out, pooled-4** (PHYS+LIFEENV+SOC+MATHDEC) | held-out 2010–14 cohort |
|---|---|---|---|---|
| concepts / events / informative strata | 369 / 1,373 / 961 | 4,302 / 8,305 / 7,241 | **3,162 / 6,978 / 6,076** | 3,949 / 7,432 / 6,434 |
| LR, +RCA>1 density (R1 vs R0) | 21.7 | 120.5 | 40.1 | 79.7 |
| LR, +share-weighted density (R2 vs R1) | 20.4 | 14.5 | 1.9 | 4.1 |
| **LR, +retained frontier (R3 vs R2)** | 57.6 | 365.6 | **325.8** (p = 8e-73) | 483.1 |
| **d0 in R3** [concept refit bootstrap, 1,000 draws] | 0.262 [0.196, 0.320] | 0.246 [0.222, 0.271] | **0.322 [0.291, 0.355]** | 0.321 [0.292, 0.347] |
| d0 in S_strict (all 4 RCA variants + both D_vol) | 0.252 [0.188, 0.315] | 0.228 [0.201, 0.254] | **0.304 [0.268, 0.336]**; LR 272.9 | 0.310 [0.282, 0.336] |
| d0 in S_pca (first PC of the 4 RCA densities) | 0.253 | 0.225 | 0.297 [0.264, 0.330] | – |
| crossed concept × target-field bootstrap CI of d0 | [0.096, 0.423] | [0.139, 0.333] | [0.201, 0.468] | – |
| two-way (concept, field) clustered SE of d0 | 0.067 | – | 0.056 (concept only: 0.016) | – |
| within-stratum AUC, R0 → R2 → R3 | 0.809 → 0.815 → 0.821 | 0.814 → 0.817 → 0.821 | 0.846 → 0.847 → 0.852 | – |
| retained-label permutation p (1,000; footprint kept) | 0.001 | 0.001 | **0.001** (null median LR 183 vs observed 326; non-trivial in 71% of strata) | – |
| degree-preserving rewire p (500) / node-label permutation p (1,000) | 0.002 / 0.001 | 0.002 / 0.001 | 0.004 / 0.003 | – |
| full-recompute rewire p (100) | 0.010 | 0.010 | 0.010 | – |
| **volume-matched retained − non-retained** (pre-declared coarse bins) | +0.130 [−0.002, 0.258] | −0.008 [−0.071, 0.050] | **−0.028 [−0.105, 0.046]** | – |
| volume-matched, fine bins (added before the freeze) | +0.071 [−0.067, 0.236] | −0.014 [−0.077, 0.048] | −0.026 [−0.107, 0.049] | – |
| dose: β by persistence age 2 / 3 / ≥4 | 0.10 / 0.14 / 0.21 | 0.06 / 0.10 / 0.25 | 0.10 / 0.08 / 0.30; β(≥4) − β(2) = 0.21 [0.16, 0.26] | – |
| **d_lost in A1** (given ever-entered density; all rows) | −0.053 [−0.125, 0.008] | −0.005 [−0.029, 0.016] | **−0.007 [−0.036, 0.022]**; LR 0.26 | −0.001 [−0.026, 0.020] |
| d_lost in R4 (with d0 and the rivals) | −0.026 [−0.116, 0.044] | +0.069 | +0.064 [0.030, 0.095] | – |

**Per held-out unit.** d0 in R3 [500-draw concept bootstrap]:

| unit | d0 [bootstrap CI] |
|---|---|
| PHYS | 0.148 [0.074, 0.219] |
| LIFEENV | 0.401 [0.347, 0.458] |
| SOC | 0.297 [0.245, 0.345] |
| MATHDEC (n = 161, underpowered) | 0.065 [−0.110, 0.234] |
| COHORT_DEVHOME | 0.304 [0.272, 0.335] |
| COHORT_NONDEVHOME | 0.338 [0.293, 0.385] |

- DerSimonian-Laird pooling over the 4 groups gives **0.243 [0.118, 0.368]**, with **I² = 0.92**. The effect is
  positive everywhere but heterogeneous in size.
- d_lost is not distinguishable from 0 in any unit, and the DL estimate is −0.017 [−0.045, 0.012], I² = 0.

### Frozen verdicts (`results/step2_heldout.json → verdicts`)

- **FRONTIER: PARTIAL: "persistence confounded with volume".**
  - Criteria met:
    - (1) pooled-4 d0 in R3 > 0, CI > 0, LR p < 0.01;
    - (2) the same in S_strict;
    - (3) 3 of 3 powered groups (PHYS, LIFEENV, SOC) plus the cohort positive. MATHDEC was excluded **before the
      freeze** because its simulated power at d = 0.15 was 0.42;
    - (4) retained-label permutation p = 0.001;
    - (6) EXP6 robustness CI > 0.
  - Failed criterion: **(5)**. Once a retained field is compared with an entered-but-not-retained field of the *same
    current and cumulative volume*, the retained label adds nothing: −0.028 [−0.105, 0.046]. DEV had already shown
    the same (−0.008). The finer bins agree.
  - Reading: relatedness to fields where the concept is *persistently present* predicts next entry far beyond every
    RCA > 1 density variant, continuous share-weighted density (D_vol, D_vol_w3, D_cum) and target-field FE.
  - But within matched volume cells, persistence per se is not separable from volume. The matched cells are
    dominated by low-volume presences (mean n(t−1) about 0.4), so this test has little leverage at high volume.
- **ABANDONMENT: INCONCLUSIVE.** The point estimate is negative (−0.007), the CI includes 0 and the Holm F3 p is
  0.46. The EXP6 frame hinted at −0.05 (CI includes 0), and this did not replicate on the larger frame. Given d0, the
  sign even turns positive (R4, +0.064). **No abandonment penalty is supported.**
- Holm-adjusted p values:
  - F1 (d0 pooled, S_strict, cohort): all < 1e-60.
  - F2:

    | test | Holm p |
    |---|---|
    | permutation | 0.005 |
    | dose trend | 0.005 |
    | rewire | 0.009 |
    | label permutation | 0.009 |
    | field FE | < 1e-56 |
    | volume-matched | 0.76 |

### Sensitivities (held-out pooled-4, d0 in R3 ± concept-cluster SE)

The effect is stable under:
- excluding intersection-born concepts: 0.332 ± 0.016;
- **target-field fixed effects**: 0.300 ± 0.017;
- horizon 8: 0.318;
- excluding weak-home concepts: 0.312;
- excluding Medicine-home concepts: 0.322;
- label coverage ≥ 0.5: 0.317;
- min_n = 3: 0.323; min_n = 5: 0.277;
- **RCA-defined entry event**: 0.243 ± 0.023;
- primary-topic instead of venue fields: 0.276;
- adding D_cum: 0.322.

Two results limit the claim:

1. **The effect is specific to the frozen PMI backbone.** With a Hidalgo min-conditional-probability proximity
   (`C_jk / max(C_jj, C_kk)`, 1998–2002 co-assignment) the retained frontier **vanishes and turns slightly negative**:
   −0.021 ± 0.009 (p = 0.012) held-out and −0.024 on DEV. Under that proximity, RCA > 1 density itself becomes
   strong (LR 246). The sparse positive-PMI backbone and the dense co-assignment proximity encode different
   relatedness.
2. **The econ-geo LPM comparability row does not reproduce the sign.** The LPM uses stratum FE and concept-clustered
   errors. On held-out pooled-4, d0 = −0.0010 [−0.0015, −0.0005], against a base rate of 1.2%. It is +0.0004
   (p = 0.06) on DEV and +0.0016 (n.s.) on EXP6.
   - An **EXPLORATORY** post-unseal diagnostic (`exploratory_lpm.py` → `results/exploratory_lpm.json`) shows why:
     d0 is negatively correlated with target-field size within strata (r = −0.25), and the linear size term misfits.
   - With size-decile dummies, the held-out LPM d0 is ≈ 0 (−0.0004 [−0.0009, 0.0001]).
   - So the frontier is a **relative-odds** effect. It is not an established effect on the additive probability
     scale.

**Guevara-comparable global AUCs** (different unit, event and proximity; not head-to-head):
- D_rca_cum alone 0.635, D_rca_1y alone 0.623, size alone 0.772.
- R3 linear predictor 0.837 (held-out pooled-4).
- Guevara et al. (2016) report 0.896 for individuals, 0.715 for organisations and 0.682 for countries.

## Checks

| check | result |
|---|---|
| T0 unit tests (`tests/test_units.py`, 10) | all pass. Covers: toy D3 states; equality with `h2_exp6.states` / `rca_entered` on 50 real concepts; RCA toy with ties at exactly 1 (strict >); density algebra; FastCLogit vs statsmodels (rel. diff 1e-4); weighted bootstrap equal to duplicate-and-relabel; permutation keeps size and pool; rewire keeps degrees and weights; crossed offset with v = 1 is exact; seal guard |
| T1 reproduction gate | EXP6 risk sets rebuilt row-for-row (47,762 + 61,648 rows; max column diff 4e-16); held-out M1 vs M0 **LR 68.569, d0 0.2809, d_lost_gate −0.0632** |
| EXP5 array re-implementation | early volume 100%; home rule 99.9% (DEV) and 99.8% (held-out); GF identical to EXP6's |
| T3 planted / null | simulated d0 = 0.2 detected in 100% at pooled-4 size; null rejection 0/200 at α = 0.01; entry shuffled within strata rejects 0/20 |
| T4 sanity (DEV) | size > 0, density > 0, R0 within-AUC 0.814 ∈ [0.75, 0.85]; max VIF 37 (D_vol vs D_vol_w3), RCA variants 4.7–6.2 |
| T5 seal | held-out risk-set file created only after `logs/seal.log`; exactly one unseal |
| T6 seed stability | second bootstrap seed moves the d0 CI endpoints by 0.001 (DEV) and 0.004 (held-out) |
| T7 audit (`audit.py`, separate code path) | hand-looped Breslow reproduces the pipeline LR 325.84 / d0 0.3219 exactly. statsmodels **exact** conditional likelihood gives LR ratio exact/Breslow 1.00 on EXP6 (d0 0.286 vs 0.262) and 0.99–1.02 on 3 × 30% held-out subsamples. 20 random rows re-derived from the raw `agg_counts.parquet` with naive loops match (D_rca_1y and d0). DL recomputed inline matches. **All pass** (`results/audit.json`) |

**Power** (DEV simulation, `results/step2_dev.json → power`). 80% MDE for d0:
- 0.066 for pooled-4 and 0.071 for the cohort;
- 0.09–0.12 for PHYS, LIFEENV and SOC;
- 0.21 for MATHDEC.

For d_lost, the 80% MDE is 0.044 in pooled-4 (power 0.99 at −0.06). The abandonment null is therefore informative:
a penalty of −0.05 SD or larger would very likely have been detected.

## Layout

| path | content |
|---|---|
| `method.py` | orchestrator. Stages: `step1` (EXP6 robustness with the T1 gate), `dev`, `freeze`, `heldout` (sealed, once), `outputs` |
| `lib/d3.py` | vectorised D3 state machine, RCA>1 portfolios (annual / 3-year / cumulative / persistence-filtered), risk sets, every covariate as (field mask) @ φ, volume-matched masks |
| `lib/models.py` | Newton conditional logit (Breslow) with stratum weights, offsets, concept / two-way clustered SEs; rung definitions; refit, contrast and crossed bootstraps; LPM; Holm; DL |
| `lib/analysis.py` | shared battery: ladder, specificity (a)–(o), abandonment, per-unit fits, power simulation, shuffled control |
| `lib/exp5.py` | read-only inputs, de-duplication (ID / QID / normalised label), grounded arrays (EXP5 `c_TAG` rule), home rule, min-CP proximity |
| `lib/seal.py` | freeze / unseal guard |
| `lib/h2_exp6.py`, `lib/stats_core.py`, `lib/cfg_exp6.py` | verbatim EXP6 copies (import lines only changed; see `results/deviations.json`) |
| `audit.py` | T7 independent audit → `results/audit.json` |
| `exploratory_lpm.py` | EXPLORATORY post-unseal LPM diagnostic → `results/exploratory_lpm.json` |
| `outputs.py` | `results/frontier_result.json`, `figures/`, `method_out.json` / `full_method_out.json` (`python method.py` with no stage runs it) |
| `tests/test_units.py` | T0 unit tests → `results/unit_tests_T0.json` |
| `results/frontier_result.json` | **everything in one file**: step 1, DEV, power table, held-out, verdicts, overlap, deviations, tests, audit, Guevara comparison |
| `results/step1_exp6_robustness.json`, `results/step2_dev.json`, `results/step2_heldout.json` | per-stage results |
| `results/frozen_spec.json`, `logs/seal.log`, `logs/unseal.log` | freeze record (spec sha256 `345d391b…`, code hashes, git commit) |
| `results/overlap_report.json` | de-duplication counts by key and split × group, plus dropped IDs |
| `results/risk_sets_exp5_minus_exp6_{dev,heldout}.parquet`, `results/risk_sets_exp6_extended_{dev,heldout}.parquet` | every candidate row with all covariates |
| `results/state_panel_{dev,heldout}.parquet` | (concept, field, year) D3 state: 0 untouched, 1 entered, 2 retained, 3 lost, 4 home; plus counts, RCA and age |
| `results/nulls_*.npz` | permutation / rewire / label-permutation null LR draws |
| `results/deviations.json` | every departure from the plan |
| `figures/` | `forest_d0_by_unit`, `forest_dlost_by_unit`, `ladder`, `dose_response`, `null_hist`, `vol_matched` (PNG + PDF) |
| `method_out.json` = `full_method_out.json` (+ `mini_`, `preview_`) | exp_gen_sol_out: all 252,922 held-out candidate rows in informative primary strata (datasets `entry_events_heldout_pooled4`, `entry_events_heldout_cohort`). `input` = `concept_id|qid|year|target_field|` + 10 raw covariates (order in `metadata.input_format`). `predict_R2_rca_vol_baseline` vs `predict_R3_retained_frontier` are within-stratum probabilities from the **frozen DEV** coefficients |
| `logs/` | run logs (`method.log`, `*_full.out`, `audit.out`) |

The parquet results stay on the run's volume and are small enough (≤ 28 MB) to be published. No absolute server paths
are needed to read them. Inputs are read by path from EXP5/EXP6 (`lib/exp5.py`: `RUN`), and the concept-recognition
dataset `art_O7Dq4L02QnDN` is used for QID and label de-duplication.

## How to run

```bash
bash install.sh                          # uv venv + pinned requirements
.venv/bin/python tests/test_units.py     # T0
.venv/bin/python method.py step1         # ~2 min
.venv/bin/python method.py dev           # ~21 min (1,000 bootstraps, nulls, power)
.venv/bin/python method.py freeze
.venv/bin/python method.py heldout       # ~15 min, runs once (seal guard)
.venv/bin/python audit.py
.venv/bin/python exploratory_lpm.py      # EXPLORATORY
.venv/bin/python method.py outputs    # also the default: `uv run method.py`
```

Smoke-run overrides: `AII_SMOKE_CONCEPTS`, `AII_NBOOT`, `AII_NPERM`, `AII_NREWIRE`, `AII_NREWIRE_FULL`,
`AII_NCROSS`, `AII_NUNITBOOT`, `AII_NPOWER`, `AII_THREADS`. Seed 20261101.

## Caveats and deviations

- **Held-out provenance.** The EXP5 held-out concepts' counts and retention outcomes were unsealed in iteration 2 for
  H1/H3. No entry or frontier analysis had touched them. The replication is independent of EXP6's concepts and of
  every d0 analysis, but the frame is not never-seen data.
- **Scope of the frame.** The EXP5 frame is mostly non-newborn onset concepts. The newborn-only subgroup has 13
  held-out concepts, so it is descriptive only.
- **Entry event.** Entry is EXP6's D3 count rule, not the RCA transition. The RCA-event sensitivity keeps d0 at 0.243.
- **Primary sample.** Frontier rungs use EXP6's primary sample (strata with a non-empty retained set). A1 uses all
  candidate rows.
- **Choices made before the freeze** (see `results/deviations.json`):
  - S_pca and fine-bin matching were added before the EXP5 freeze;
  - MATHDEC was excluded from the sign rule on the basis of the power table;
  - the power grids are one-dimensional.

## Restoring removed files

| removed path (`.aii/manifest.yaml`) | restore with |
|---|---|
| `.venv/` | `bash install.sh` (`uv venv .venv --python=3.12 && uv pip install -r requirements.lock.txt`) |
| `lib/__pycache__/`, `__pycache__/` | regenerated automatically by any `python` run |
