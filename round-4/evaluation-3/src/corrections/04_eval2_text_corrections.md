# 04 Eval2 text corrections, insert-ready

All 14 '## ' blocks of Eval2's text_corrections.md, rendered for insertion. Each insert starts with `[Correction, iteration 3, from art_7W9xiIO3FVBs]`; the number tokens are carried verbatim from the Eval2 block (checked token by token in the ledger).

## 10.3 H1 criteria (blocking)

[Correction, iteration 3, from art_7W9xiIO3FVBs] Verdict: **DISCONFIRMED** by the preregistered rule, which requires all six core criteria. Criterion by criterion (held-out, 8,515 episodes / 3,085 concepts): pooled dAUC >= 0.05 False; refit CI > 0 False; >= 3 of 4 groups positive False (2 of 4); cohort same sign True (both negative); within-field LPM beta > 0 at p < 0.05 **True** (beta = +0.068 per SD, concept-clustered SE 0.033, p = 0.041; two-way clustered p = 0.17; all splits +0.051, p_concept = 0.0065, p_twoway = 0.18); real dAUC above the rewired-backbone placebo p95 False. The frozen rule names p < 0.05 without an SE type and the sealed code uses the concept-clustered p, so the LPM criterion passes as preregistered but is fragile under two-way clustering. Clustered-SE logit: beta = -0.045 (p_concept = 0.29); boundary interaction +0.064 (p = 0.45; predicted negative, consistent = False); crossed concept x field bootstrap CI [-0.0023, 0.0010].

Source (from Eval2): `round-2/experiment-5/src/results/h1_heldout.json: verdict_H1.criteria.*`; `lpm_field_fe.*`; `lpm_field_fe_all_splits.*`; `logit_clustered_se.*`; `boundary.*`; `pigeonhole_crossed_bootstrap.ci95`; `round-2/experiment-5/src/models.py (p_concept in the criterion)`

## 11.3 / 16.3 Ordering -> MIXED (blocking)

[Correction, iteration 3, from art_7W9xiIO3FVBs] Ordering is **mixed / not established**. Of 175 broad (top-tercile O2r) concepts, 112 have a detected entropy take-off and 102 an evaluable gateway ordering: the first retained gateway field comes first in 57, ties 15, after 30 (57/87 = 65.5% of non-tied; 57/102 = 55.9% of evaluable; 57/175 = 32.6% of broad concepts; sign p = 0.0025). Peripheral fields: 49/20/37, 57.0%, p = 0.118; McNemar 27 vs 15, p = 0.088. The preregistered sign rule passes, but concept-FE lead-lag regressions show retention followed by SMALLER next-year entropy gains (gateway b = -0.0279, p = 0.0007; peripheral b = -0.0434, p = 5.9e-08), a significant pre-trend (event time -3: -0.072, p = 0.0002; DEV -0.088), and on DEV entropy predicting later gateway retention (b = 0.232 [0.066, 0.397], p = 0.0062; held-out b = 0.077, p = 0.22). On DEV, peripheral fields precede take-off as often as gateway fields (71.4% vs 70.3%, McNemar p = 0.34); the gateway permutation placebo is null (p = 0.63). The file flag decisions.H2_ordering.CONFIRMED = true checks only the sign rule and is overridden here.

Source (from Eval2): `round-2/experiment-6/src/results/heldout_result.json: ordering.*`; `round-2/experiment-6/src/results/dev_result.json: ordering.*`; `round-2/experiment-6/src/results/heldout_result.json: decisions.H2_ordering.CONFIRMED`

## 10.6 / 16.5 H3 (blocking)

[Correction, iteration 3, from art_7W9xiIO3FVBs] H3 is **small; it passes the preregistered within-group permutation rule, but the pooled concept-bootstrap CI includes 0**. Held-out (n = 2,838): G partial rho = 0.030 [-0.006, 0.065], G_A 0.026 [-0.011, 0.067], G_btw 0.046 [0.009, 0.086]; Holm p = 0.0045 from a one-sided within-group permutation test (2,000 draws; Holm over G, G_A, G_btw) whose null is centred below zero (about -0.012). Within-group DL pooled G = 0.068 [0.029, 0.107], I2 = 0.00; G_btw DL = 0.072 [-0.015, 0.159], I2 = 0.77 (negative in LifeEnv, -0.020). DEV values: G 0.138, G_btw 0.170; held-out/DEV shrinkage for G = 0.21. The calibration check found 0 of 40 shuffled outcomes declared significant (false-positive rate 0/40), which is not a p-value or an exceedance count.

Source (from Eval2): `round-2/experiment-5/src/results/h3_results.json: G.*, G_A.*, G_btw.*, holm_adjusted_p, notes`; `round-2/experiment-5/src/results/h1_dev.json: H3_dev`; `round-2/experiment-5/src/results/audit_placebo.json: H3_calibration_40_shuffles`

## 10.7 Power attribution and MDE wording (blocking)

[Correction, iteration 3, from art_7W9xiIO3FVBs] Exp5 (art_wxWssKSUR45f) power simulation (h1_dev.json power; planted effect b in SD log-odds of standardised gateway_j on the dev covariate structure; 40 sims x 150 boot): a planted effect b = 0.3 gives mean dAUC 0.0040 with power 0.90 (b = 0.2: 0.0019, power 0.65), so 0.004 is the **90%** point (the file key 'min_detectable_dauc_80pct' mislabels it), computed for 8,515 held-out episodes, not 27,393. At b = 0 the CI > 0 rule fires 0.125 of the time (nominal 0.025): the concept-only bootstrap is anti-conservative. Evaluation 1 (art_lwI2DuRtQRZX, E_power) adds a field random intercept: the SD of dAUC under the alternative stays near 0.016 (floor about 0.02) and about 34 held-out concepts per group give P(group delta > 0) >= 0.90 at delta = 0.05. The field-random-intercept figure governs the H1 verdict's field-level uncertainty; the Exp5 figure ignores between-field variance.

Source (from Eval2): `round-2/experiment-5/src/results/h1_dev.json: power.*`; `round-2/evaluation-1/src/eval_out.json: metadata.E_power.held_out_sizing_from_alternative_SD.*`

## 5.4 The 'B5 + all_four' row (blocking)

[Correction, iteration 3, from art_7W9xiIO3FVBs] | B3 + log field size + {gateway_j, phi_home_j, density_j} (size_controlled_all_three) | 0.697 | 0.782 | +0.085 | [0.004, 0.164] | refit [-0.043, 0.220] | and add | B3 + {gateway_j, phi_home_j, density_j} (all_four_available) | 0.705 | 0.787 | +0.082 | [0.008, 0.153] | refit [-0.042, 0.204] |. Neither row contains G, REL, RS or G_all; both refit CIs include 0.

Source (from Eval2): `round-1/experiment-4/src/screen_result.json: field_level.size_controlled_all_three.*, field_level.all_four_available.*`; `round-2/evaluation-1/src/eval_out.json: metadata.F_record.F5_exp4_field_level.rows.*`

## 13.1 Dataset 2 coverage counts (blocking)

[Correction, iteration 3, from art_7W9xiIO3FVBs] Concept counts (coverage_report.json by_source): mesh 20,872 concepts with an event (20,872 year-usable); wikipedia_en 64,363 concepts with an event (50,459 year-usable); wikidata 1,425 concepts with an event (1,316 year-usable); acm_ccs 1,298 concepts with an event (1,298 year-usable); msc 1,121 concepts with an event (1,121 year-usable); pacs_physh 2,635 concepts with an event (2,635 year-usable); gartner_hype_cycle 466 concepts with an event (466 year-usable); mit_tr10 313 concepts with an event (313 year-usable); research_fronts 589 concepts with an event (589 year-usable); nature_methods_moty 38 concepts with an event (38 year-usable); science_boty 53 concepts with an event (53 year-usable); physics_world_boty 100 concepts with an event (100 year-usable); jel 0 concepts with an event (0 year-usable). Wikipedia exact first revisions: 7,806. The draft's 3,583 / 17,872 / 8,462 / 1,015 are external-ENTRY counts (external_entries_acm_ccs / msc / pacs_physh / jel), not concepts; the '589' is Research Fronts only. JEL: 213 concepts found, 0 dated events (present-day membership).

Source (from Eval2): `round-2/dataset-2/src/out/coverage_report.json: by_source.*.n_with_event, n_with_year_usable_event, status`; `round-2/dataset-2/src/README.md: external_entries table`

## 8a Coverage table, iteration-2 column (blocking)

[Correction, iteration 3, from art_7W9xiIO3FVBs] Replace the 8a table with record_tables/coverage_iter2_steps.csv (status after iteration 2) and add the per-artifact row counts in record_tables/coverage_iter2.csv (concepts, episodes, groups, splits, median label coverage, grounding precision, LLM cost, credits).

Source (from Eval2): `record_tables/coverage_iter2.csv`; `record_tables/coverage_iter2_steps.csv`

## 4.4 Remaining partial associations (blocking)

[Correction, iteration 3, from art_7W9xiIO3FVBs] All 12 candidates are in the file: D_ratio +0.335 [-0.059, 0.688] (3/4 groups +); D_rare +0.311 [-0.101, 0.692] (3/4 groups +); D_z +0.313 [-0.161, 0.634] (4/4 groups +); D_sub +0.245 [-0.162, 0.634] (4/4 groups +); NOV_res +0.281 [-0.190, 0.639] (2/4 groups +); participation +0.322 [-0.115, 0.690] (3/4 groups +); n_comm_W3 +0.218 [-0.153, 0.627] (2/4 groups +); F_res -0.267 [-0.492, 0.324] (1/4 groups +); F_z -0.248 [-0.509, 0.353] (1/4 groups +); F_bg -0.301 [-0.560, 0.254] (2/4 groups +); deg_growth +0.050 [-0.466, 0.381] (1/4 groups +); btw_change -0.168 [-0.514, 0.400] (1/4 groups +). Paste record_tables/partial_association_all.csv.

Source (from Eval2): `round-1/experiment-3/src/results/exploratory_partial_association.json: candidates.*`

## 11.2 / hypothesis LR, d and strata clashes

[Correction, iteration 3, from art_7W9xiIO3FVBs] LR 68.6 = M1 (plain retaining relatedness d0_ret_rel) vs M0, Breslow; LR 71.7 = M2 (gateway-weighted d_ret_gate) vs M0, Breslow; LR 77.3 = M2 vs M0 with the exact conditional likelihood (statsmodels, Exp6 audit.json). Recomputed here: M1vsM0 Breslow 68.57 / exact 73.25; M2vsM0 Breslow 71.72 / exact 77.30. d = 0.281 is the M1 coefficient of plain retaining relatedness (d0_ret_rel, SE 0.032); d = 0.302 ('0.30') is the M2 coefficient of gateway-weighted retaining relatedness (d_ret_gate). Both are Breslow, per SD of the frozen DEV standardisation. The hypothesis text's '961 strata' is the number of INFORMATIVE strata (>= 1 event and >= 1 non-event) that enter the conditional likelihood (961 recomputed; 18846 rows); the file's n_strata = 2,339 counts ALL strata of the primary sample (n_ret > 0; 2339 recomputed, 46433 rows). The parquet itself holds 2992 strata / 61648 rows before the n_ret > 0 restriction. The conventional headline is the plain retaining-relatedness coefficient d0_ret_rel = 0.281 (SE 0.032), since the gateway weighting adds nothing (M3 vs M1 g-only permutation p = 0.17).

Source (from Eval2): `record_tables/next_field_trace.json`; `round-2/experiment-6/src/results/heldout_result.json: H2_pooled.*`; `round-2/experiment-6/src/results/audit.json: H2_LR`

## 16.1 'positive in all three evaluable groups'

[Correction, iteration 3, from art_7W9xiIO3FVBs] positive in all four held-out groups (sign test p = 0.0625); only Physical's bootstrap CI excludes 0 (Physical d = 0.33 [0.05, 0.57]; LifeEnv LR p = 0.23; Social LR p = 0.076; cohort d = 0.29).

Source (from Eval2): `round-2/experiment-6/src/results/heldout_result.json: H2_per_group.*, H2_sign_count`

## 10.5 Relatedness pair is held-out only

[Correction, iteration 3, from art_7W9xiIO3FVBs] The relatedness pair adds dAUC +0.0034 on held-out data but -0.00017 on DEV: the gain was not seen in development.

Source (from Eval2): `round-2/experiment-5/src/results/h1_heldout.json: rival_head_to_head.dauc_relatedness_pair`; `round-2/experiment-5/src/results/h1_dev.json: rival_head_to_head.dauc_relatedness_pair`

## 11.5 Trajectory robustness

[Correction, iteration 3, from art_7W9xiIO3FVBs] DTW k-medoids k = 2 is stable under bootstrap (ARI 1.0), but the 6-state HMM does not reproduce it (HMM vs DTW ARI = 0.095), and the localised class is dominated by Medicine homes.

Source (from Eval2): `round-2/experiment-6/src/results/heldout_result.json: trajectories.hmm_vs_dtw_ARI`

## New: frame comparison (Exp5 vs Exp6) for Section 9/11

[Correction, iteration 3, from art_7W9xiIO3FVBs] The common-panel design was not realised: Exp5 (12,499 concepts, TAG grounding) and Exp6 (653 newborn concepts, tag-AND-title) share 628 concepts (96.2% of Exp6). On them, onset agrees exactly for 97.6% (+/-1: 98.9%), home kappa = 0.99, O2r_m50 Spearman = 0.998, episode Jaccard median = 1.00, but retention kappa = 0.28 (Exp5 relative-share rule vs Exp6 absolute >= 2 works; with the matched definition R_abs2 kappa = 0.98). Pre-declared pooling verdict: **PARTIAL**. A replication of H2 on 'Exp5 minus Exp6' must rebuild RETAINED/LOST with Exp6's R_cj rule before a null can be read as a failure of the claim.

Source (from Eval2): `frame_agreement.json`; `record_tables/definitions_diff.csv`; `record_tables/frame_overlap_by_group.csv`

## New: O5 external recognition status (13 / 16 Open)

[Correction, iteration 3, from art_7W9xiIO3FVBs] O5 was joined to the Exp5 frame (all 12,499 concepts). O5_main base rate: 0.238 held-out. It is **UNRELATED** to publication outcomes: pooled held-out rho with O2r_m50 = 0.014 [-0.045, 0.073], with O1 = 0.001 [-0.033, 0.034]. For 8,371 of 12,499 concepts the first qualifying recognition is at or before t0. Executor-checked sample: positive precision 0.86, Wikipedia date error <= 1 year in 0.95, negative false-negative rate (Wikipedia only, lower bound) 0.14; FIT_FOR_USE = True.

Source (from Eval2): `o5_validation.json`; `o5_definitions.json`; `record_tables/o5_*.csv`
