# 03 Exp7 tables (inserts for Section 18)

Tag: `[Correction, iteration 4, from art_22ppE1snfHKj]`. Every value is printed with its key path; a value not found at its key is printed NOT_FOUND (never retyped).

## 18.5 Volume-matched contrast (retained R vs entered-not-retained N, same current x cumulative volume cell)

| split | bins | d_R_m [CI] | d_N_m [CI] | contrast R - N [CI] | one-sided p | match rate (strata) | matched R / N fields | mean cum. prev. volume R / N |
|---|---|---|---|---|---|---|---|---|
| DEV | coarse | +0.069 [+0.021, +0.114] | +0.078 [+0.031, +0.129] | -0.008 [-0.071, +0.050] | 0.611 | 0.128 | 5,209 / 5,673 | 7.78 / 6.07 |
| DEV | fine | +0.061 [+0.006, +0.112] | +0.075 [+0.020, +0.125] | -0.014 [-0.077, +0.048] | 0.683 | 0.121 | 4,869 / 5,359 | 6.20 / 5.52 |
| held-out pooled 4 | coarse | +0.073 [+0.004, +0.134] | +0.100 [+0.039, +0.157] | -0.028 [-0.105, +0.046] | 0.755 | 0.153 | 5,125 / 5,597 | 7.98 / 6.30 |
| held-out pooled 4 | fine | +0.066 [-0.002, +0.130] | +0.092 [+0.033, +0.152] | -0.026 [-0.107, +0.049] | 0.752 | 0.144 | 4,746 / 5,259 | 6.40 / 5.71 |

Source: `round-3/experiment-7/src/results/step2_dev.json` -> `battery.specificity.{b_volume_matched,b2_volume_matched_fine}.*`; `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.specificity.{b_volume_matched,b2_volume_matched_fine}.*`

Reading: both retained and non-retained matched fields carry a positive coefficient, and the pre-declared contrast is null in both bin sets. The retained-relatedness signal cannot be separated from volume.

## 18.4 Dose by persistence age (held-out pooled 4)

| age 2 | age 3 | age >= 4 | 4+ minus 2 [CI] | monotone non-decreasing | Spearman(beta, age) |
|---|---|---|---|---|---|
| +0.098 | +0.075 | +0.304 | +0.206 [+0.156, +0.255] | False | 0.50 |

Source: `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.specificity.c_dose.*`

## 18.9 Abandonment penalty d_lost: A1 vs R4 and variants (held-out pooled 4)

| model | d_lost | CI | note |
|---|---|---|---|
| A1 = R0 + d_lost (all rows) | -0.007 | concept [-0.036, +0.022]; crossed [-0.082, +0.052] | verdict: INCONCLUSIVE (negative point estimate, CI includes 0) |
| R4 = R3 + d_lost (primary sample) | +0.064 | - | positive once d0 is in the model |
| min-cp proximity backbone, R4 | +0.003 | - | min-cp A1: d_lost -0.030, p = 0.00013 |
| target-field FE, A1 | -0.044 | - | key `pooled4.specificity.g_target_field_FE.d_lost_A1.coef` |

Source: `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.ladder.*.models.{A1_lost,R4_lost}.coef.d_lost; verdicts.d_lost_ci; crossed_boot.d_lost_A1.ci; pooled4.specificity_rebuild.m_min_conditional_probability_proximity; pooled4.specificity.g_target_field_FE`

## 18.3 d0_ret_rel with three resampling units (held-out pooled 4, R3)

| estimate | concept bootstrap (1,000) | two-way concept x field clustered (coef +- 1.96 SE) | crossed concept x field bootstrap (500) |
|---|---|---|---|
| +0.322 | [+0.291, +0.355] | [+0.211, +0.432] | [+0.201, +0.468] |

Source: `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.boot.d0_R3.d0_ret_rel.{est,ci}; pooled4.crossed_boot.d0_R3.ci`; `round-4/evaluation-3/src/results/partA_derived.json` -> `exp7_d0_two_way_heldout.ci (from ladder...R3_ret.se_two_way_concept_field.d0_ret_rel)`

## 18.6 Held-out sensitivities of d0 (R3)

| sensitivity | d0 | concept-clustered p |
|---|---|---|
| e_excl_intersection_born | +0.332 | 4.2e-90 |
| g_target_field_FE | +0.300 | 3.9e-66 |
| h_horizon8 | +0.318 | 2.4e-74 |
| i_excl_weak_home | +0.312 | 4.2e-72 |
| j_excl_medicine_home | +0.322 | 7.5e-89 |
| n_newborn_only_descriptive | +0.562 | 0.034 |
| o_label_coverage_ge_0.5 | +0.317 | 5.4e-65 |
| f_min_n_3 | +0.323 | 2e-84 |
| f_min_n_5 | +0.277 | 1.2e-53 |
| l_rca_entry_event | +0.243 | 2.1e-26 |
| k_primary_topic_fields | +0.276 | 8.7e-93 |
| m_min_conditional_probability_proximity | -0.021 | 0.014 |

Source: `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.{specificity,specificity_rebuild}.<name>.d0_R3.{coef,p_wald_concept_2s}`

## New subsection 18.6a Proximity dependence

[Correction, iteration 4, from art_22ppE1snfHKj] The retained-frontier coefficient depends on the proximity backbone. Under Hidalgo's minimum conditional-probability proximity (instead of the frozen PMI backbone), d0 in R3 is -0.021 (LR R3 vs R2 p = 0.012), while the RCA density itself becomes much stronger (LR R1 vs R0 = 245.5). Within-stratum AUC is higher under min-cp without d0 (R2 0.867) than under PMI with d0 (R3 0.852). The d0 effect is backbone-specific: it measures relatedness as PMI encodes it, not relatedness in general.

Source: `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.specificity_rebuild.m_min_conditional_probability_proximity.ladder.{models.R3_ret.coef.d0_ret_rel,LR.*,auc_within.R2_vol}`; `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.ladder.frontier_primary_sample.auc_within.R3_ret`

## Step-3 comparison: Exp7 D_rca_pers vs Research 2 D_rca_persist_k

- Exp7 frozen definition (frozen_spec.json covariates.D_rca_pers): 'U = RCA(t-3..t-1) > 1 AND RCA(t-6..t-4) > 1'.
- Research 2 (art_EesdB8cuSfcU) R1: 'entered or RCA > 1 in each of t-k..t'.
- Verdict: **DIFFERENT**. D_rca_pers uses two window-aggregated 3-year RCAs over a 6-year horizon; persist_k requires the state in each single year and admits 'entered' presences below RCA 1. Neither U-set contains the other.
- DEV check (958,542 candidate rows, 4,486 concepts; recipe check: rebuilt D_rca_1y vs Exp7 Spearman 1.0000):

| variant | Spearman with D_rca_pers | Spearman with D_rca_1y | share rows > 0 |
|---|---|---|---|
| D_rca_persist_2_entered_or_rca | 0.718 | 0.690 | 0.608 |
| D_rca_persist_2_rca | 0.877 | 0.875 | 0.342 |
| D_rca_persist_3_entered_or_rca | 0.729 | 0.690 | 0.588 |
| D_rca_persist_3_rca | 0.864 | 0.829 | 0.317 |

Source: `round-4/evaluation-3/src/results/drca_persist_comparison.json` -> `comparisons.*; recipe_check_D_rca_1y_spearman`
Consequence: Exp7's S_strict rival set did NOT contain Research 2's D_rca_persist_k; the 'persistence-filtered RCA density' rival (R1 in Research 2) remains untested against d0 and should be listed as an open rival.

## Nearest-neighbour paragraph (draft for Section 18.1 / Related work)

[Correction, iteration 4, from art_22ppE1snfHKj] The retained-frontier predictor sits next to four lines of work. Hidalgo et al. (2007) define density from a region's current revealed-comparative-advantage basket and show that products close to that basket are entered next. Pinheiro et al. (2022) add persistence, but only on the outcome side: an entry counts only if RCA stays above one after years below it. Albora et al. (2023) benchmark relatedness against machine-learning forecasts of entry that use the unit's own past RCA trajectory (the benchmark Research 2 flags as a missing rival here). Cheng et al. (2023) bring the diffusion question to science and tie a topic's spread to the social structure of its early adopters (unconnected co-author groups; our candidate S). Our d0 moves persistence to the predictor side (relatedness to fields that RETAIN the concept). It is backbone-specific (18.6a) and not separable from volume in the matched contrast (18.5), and the persistence-filtered density twin D_rca_persist_k differs from Exp7's D_rca_pers (Step-3 above).
