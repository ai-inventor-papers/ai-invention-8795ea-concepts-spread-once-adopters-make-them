# Recomputation log (review, iteration 5)

Every value below was read directly from the artifact file named. The paths are relative to `3_invention_loop/`.

| Report claim | Artifact file / key | Recomputed | Verdict |
|---|---|---|---|
| Ladder OPEN_home R0..R5 .12/.10/.09/.08/.07/.06, n 573 | iter_4/gen_art_experiment_10/results/cohort_result.json primary | .123/.097/.091/.080/.069/.056; R4 CI [-0.012,0.150], R5 [-0.022,0.135] | match (CIs at R4/R5 incl. 0 not shown in table) |
| OPEN_all R0..R5 .21..14, n 630 | same | .205/.180/.174/.171/.147/.138 | match |
| Abstract +0.17 [0.09,0.25] | same, OPEN_all R2 | 0.174 [0.092,0.253] | match, but coupled build and not labelled |
| ALL-HOME +0.093 [0.016,0.169] | cohort_result.json contrasts | 0.0929 [0.016,0.169]; SIZEMATCH-HOME 0.053 [-0.015,0.117] | match; the null sizematch contrast is omitted |
| Planted control | cohort_result.json placebos.planted_0.10 | 0.047 [-0.045,0.132], recovered false | omitted from report |
| Cohort years 2015-2016 | cohort_result.json n_by_t0 | 2015:570, 2016:500, 2017:373 | MISMATCH |
| Screen table (10 rows) | iter_3/gen_art_experiment_8/results/heldout_summary.json O2r_m50 | all pooled/CI/I2/sign values match | match; family labels wrong (RS=G, log_offhome_volume=F) |
| Decomposition 0.732/0.779/0.268/0.464, n 3188 | iter_4/gen_art_experiment_12/results/decomposition_dev.json i_pooled | match | match, but variant i, not prereg variant iv |
| d0 0.322 [0.291,0.355], LR 325.8 | Exp7 summary / step2_heldout | match | match |
| LR 29.3 "on DEV" | iter_3/gen_art_experiment_7/results/step1_exp6_robustness.json dev.ladder.frontier_primary_sample.LR.R3_ret_vs_R2_vol | 29.319 | EXP6-frame DEV, not the independent frame |
| Dose 0.056/0.103/0.251 "monotone" | step2_dev.json battery.specificity.c_dose | DEV values; held-out pooled4 = 0.098/0.075/0.304 (not monotone) | MISLABELLED (DEV shown as headline) |
| Cheng Spearman +0.79 with persistence | iter_5/gen_art_experiment_14/results/identity_check.json | 0.767 (Exp11 Jaccard), 0.625 (Exp10 edge_persistence__home) | MISMATCH / untraceable |
| Frame N 636 vs "448 concepts" | iter_5/gen_art_experiment_13/results/frame_n_result.json | n_frame 636; OPEN_home available for 578; 448 = analysis-cell n | inconsistent labelling |
| Frame N verdict | frame_n_result.json verdicts | PARTIAL; R5 CI incl. 0; group clause false; CONFIRMED_HOLM false; REVERSAL_CONFIRMED false | report calls it "confirmation" |
| Pooled Frame N + Exp10 +0.096 [0.034,0.158] | frame_n_result.json exploratory_pooled_with_exp10 R3 | 0.0957 [0.034,0.158] | match; EXPLORATORY label omitted |
| Disattenuated NOVCHURN 0.178 [0.141,0.214] | iter_5/gen_art_experiment_16/results/clean_vs_raw_psp.json disattenuated | 0.178 [0.141,0.214], flagged approximate | match; flag omitted; rare20 CI incl. 0 |
| Domain Shapley +0.132 | iter_5/gen_art_experiment_15/results/partner_shapley.json | phi 0.1322 | match |
