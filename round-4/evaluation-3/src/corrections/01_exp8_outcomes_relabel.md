# 01 Exp8 outcome relabelling (replaces Sections 19.4-19.7 and dead end 22.6)

Tag for every insert below: `[Correction, iteration 4, from art_dFQ6jbgNsR6Q]`.

The draft's Section 19.5 is headed 'Transience' but reports the **O4** results (field- and year-normalised citation growth; REL_home and author_growth). The real O3 (transience) results are missing from the draft, and dead end 22.6 repeats the mislabel. The tables below are generated from Exp8's result files; the README tables at lines 57 (O4) and 87 (O3) were cross-read and agree to 3 decimals.

## Old text (19.5, verbatim)

> ### 19.5 Transience: 2 of 10 confirmed: 2 of 10 confirmed
>
> Two indicators predict transience (lower transience = better):
>
> | Indicator | Pooled beta | 95% CI | Holm p |
> |---|---|---|---|
> | REL_home | -0.114 | [-0.180, -0.047] | confirmed |
> | author_growth | +0.065 | [+0.024, +0.106] | confirmed |
>
> Concepts from fields with high relatedness to many other fields (REL_home) are less transient. Concepts with higher early author growth are more transient. The ElasticNet shrank all transience indicators to zero on this outcome, meaning no linear combination adds reliably.

## New 19.4 O1c (sustained uptake)

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] Only n_authors_early is confirmed for O1c: pooled psp +0.161 [+0.090, +0.230], Holm p 0.0001 (1 of 10 frozen indicators).

## New 19.5 O4 (field- and year-normalised citation growth): 2 of 10 confirmed

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] This section reports O4, not transience. Concepts whose home field is related to many fields (REL_home) show LOWER later citation growth, and early author growth predicts HIGHER citation growth.

| indicator | family | frozen sign | pooled psp | 95% CI | I2 | Holm p | sign agree | confirmed |
|---|---|---|---|---|---|---|---|---|
| G_deg | G | - | -0.021 | [-0.069, +0.028] | 0.41 | 1 | 5/6 | no |
| log_offhome_volume | F | - | -0.002 | [-0.069, +0.066] | 0.66 | 1 | 3/6 | no |
| REL_home | G | - | -0.114 | [-0.180, -0.047] | 0.69 | 0.00922 | 6/6 | **yes** |
| burst | E | - | +0.014 | [-0.043, +0.072] | 0.55 | 1 | 3/6 | no |
| G_A | G | - | -0.010 | [-0.055, +0.036] | 0.33 | 1 | 4/6 | no |
| author_growth | E | + | +0.065 | [+0.024, +0.106] | 0.21 | 0.0182 | 5/6 | **yes** |
| G_phimin | G | + | +0.064 | [-0.080, +0.206] | 0.93 | 1 | 5/6 | no |
| FRONTIER_POTENTIAL | FR | - | -0.017 | [-0.063, +0.030] | 0.39 | 1 | 5/6 | no |
| RETENTION_RATIO_early | FR | - | -0.026 | [-0.060, +0.009] | 0.00 | 1 | 5/6 | no |
| new_edge_rate | A | - | +0.003 | [-0.032, +0.037] | 0.00 | 1 | 3/6 | no |

Source: `3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/heldout_summary.json` -> `O4[i].{pooled,pooled_ci,I2,holm_p,sign_agree,n_units,confirmed}`

## New 19.5b O3 (transience): 1 of 10 confirmed

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] For transience (O3, binary; groups with an estimable O3), only n_authors_early is confirmed; MATHDEC has too few transient concepts for O3 (Exp8 deviation F6_MATHDEC_O3), so sign agreement is out of 5.

| indicator | family | frozen sign | pooled psp | 95% CI | I2 | Holm p | sign agree | confirmed |
|---|---|---|---|---|---|---|---|---|
| n_authors_early | E | + | +0.089 | [+0.031, +0.148] | 0.00 | 0.0286 | 4/5 | **yes** |
| S_comp_n | S | + | +0.068 | [+0.001, +0.134] | 0.10 | 0.406 | 4/5 | no |
| rao_stirling | F | + | +0.066 | [-0.002, +0.134] | 0.22 | 0.446 | 3/5 | no |
| G_deg | G | + | +0.036 | [-0.007, +0.079] | 0.00 | 0.586 | 4/5 | no |
| REL_home | G | + | +0.001 | [-0.056, +0.059] | 0.32 | 1 | 2/5 | no |
| G_btw | G | + | +0.040 | [-0.024, +0.104] | 0.48 | 0.891 | 3/5 | no |
| fields_gained_per_yr | F | + | +0.010 | [-0.042, +0.061] | 0.00 | 1 | 1/5 | no |
| M0_density_end | FR | + | +0.038 | [-0.011, +0.086] | 0.00 | 0.655 | 4/5 | no |
| G_A | G | + | +0.053 | [-0.058, +0.165] | 0.79 | 1 | 4/5 | no |
| CONTACT_REACH | FR | + | +0.049 | [-0.003, +0.101] | 0.00 | 0.452 | 5/5 | no |

Source: `3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/heldout_summary.json` -> `O3[i].*`

## New 19.6 External recognition (O5, O5_WW): 0 and 0 of 10 confirmed

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] No indicator predicts external recognition beyond B5 + onset year (see file 10 for the section cross-reference fix).

Source: `3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/rq1_heldout.json` -> `headline_by_outcome.{O5,O5_WW}.n_confirmed_holm`

## New 19.7 Learned models vs B5 vs B5 + best single (held-out groups pooled)

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] All 8 outcomes; Spearman(pred, y) for continuous outcomes, AUC for binary (O1c, O1b, O3, O5, O5_WW); [95% CI of the paired difference vs B5].

| outcome | n | B5 | B5 + best single | ElasticNet / L1-logit (all) | EBM |
|---|---|---|---|---|---|
| O1c | 3,372 | 0.312 | 0.305 [-0.016, +0.004] | 0.303 [-0.019, -0.001] | 0.313 [-0.022, +0.026] |
| O2r_m50 | 1,833 | 0.706 | 0.739 [+0.022, +0.045] | 0.765 [+0.046, +0.073] | 0.757 [+0.037, +0.067] |
| O2r_resid | 1,833 | 0.704 | 0.738 [+0.023, +0.047] | 0.763 [+0.047, +0.071] | 0.756 [+0.038, +0.066] |
| O4 | 3,372 | 0.015 | 0.028 [-0.009, +0.036] | constant (all coefficients 0; no ranking) | 0.188 [+0.129, +0.219] |
| O1b | 3,372 | 0.507 | 0.518 [-0.003, +0.029] | 0.524 [-0.000, +0.039] | 0.526 [-0.001, +0.042] |
| O3 | 3,372 | 0.506 | 0.576 [+0.020, +0.128] | 0.599 [+0.028, +0.163] | 0.599 [+0.033, +0.161] |
| O5 | 1,417 | 0.746 | 0.742 [-0.013, +0.003] | 0.747 [-0.009, +0.009] | 0.726 [-0.038, -0.004] |
| O5_WW | 1,671 | 0.747 | 0.746 [-0.007, +0.005] | 0.751 [-0.003, +0.010] | 0.719 [-0.046, -0.011] |

Source: `3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/learned_vs_single_heldout.json` -> `<outcome>.POOLED_HELDOUT.{n,B5.metric,<model>.metric,<model>.delta_ci}`

Cross-read: README.md line 132 table (Exp8) shows the same values to 3 decimals.

## O3 as a positive held-out result

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] Transience IS predictable beyond B5 on held-out groups: L1-logit AUC 0.599 vs B5 0.506 (paired difference [+0.028, +0.163]); EBM 0.599. Caveat: B5 itself is at chance for O3, so the gain is over a null baseline, not over a strong one.

## Old text (dead end 22.6, verbatim)

> 6. **Transience ElasticNet: ALL shrunk to zero.** The ElasticNet learned model for transience has no nonzero coefficients, meaning no linear combination of the 53 indicators predicts transience beyond noise on heldout data. The EBM's gain (+0.174) relies on nonlinear interactions that the ElasticNet rejects.

## New dead end 22.6

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] 6. **O4 (citation growth) linear model: shrank to a constant.** The ElasticNet for O4 (field- and year-normalised citation growth, NOT transience) set every coefficient to zero, so it ranks nothing on held-out data, while the EBM reaches Spearman 0.188 vs B5 0.015 (gain +0.174 [+0.129, +0.219]). The O4 signal is non-linear. Transience (O3) is a separate outcome with a positive held-out learned-model result (above).

Source: `3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/learned_vs_single_heldout.json` -> `O4.POOLED_HELDOUT.*`; `3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/deviations.json` -> `O4_linear_all_constant`
