# 11 Boundary results for the OPEN lead (EXPLORATORY)

**Status: EXPLORATORY.** All analyses reuse the Exp8 held-out groups, which were unsealed in Exp5 and Exp8. They can reveal fragility; they cannot confirm OPEN. Confirmation needs the never-screened 2015-16 cohort. The specification was hash-frozen before any statistic (`logs/seal.log`, boundary_spec.json sha256).

## Reproduction gate T0

Exp8's pooled held-out psp was re-derived from analysis_table.parquet with the Exp8 estimator: M0_density_end +0.3745 (record +0.3745, O2r_m50) and +0.3770 (O2r_resid); D_vol_end +0.3071; n_comm_W3 +0.1666; ego_density_W3 -0.1024; new_edge_rate +0.1176. All within the 1e-3 tolerance (gate passed).

Source: `round-4/evaluation-3/src/results/gate_T0.json` -> `rows[i].{record_pooled,rederived_pooled}`

## B1 Post-onset re-score of the two largest breadth effects

- **M0_density_end** (O2r_m50, DL over held-out groups): full history +0.374 -> post-onset only (t0..t0+2 papers) +0.187 [+0.145, +0.246]; paired difference +0.187 [+0.138, +0.231]; attenuation 0.50 [0.38, 0.60]; verdict **PARTIAL** (frozen rule: MOST if upper CI of post < half of full; LITTLE if the paired difference CI includes 0).
- **D_vol_end** (O2r_m50, DL over held-out groups excluding MATHDEC): full history +0.317 -> post-onset only (t0..t0+2 papers) +0.176 [+0.114, +0.227]; paired difference +0.141 [+0.087, +0.209]; attenuation 0.45 [0.29, 0.64]; verdict **PARTIAL** (frozen rule: MOST if upper CI of post < half of full; LITTLE if the paired difference CI includes 0).
- D_vol_end given B5 + pre-onset footprint (D_vol_pre, log pre-onset papers): +0.181 [+0.134, +0.227].
- M0_density_end given B5 + pre-onset footprint (D_vol_pre, log pre-onset papers): +0.290 [+0.191, +0.383].
- D_vol_post is near rank-identical to the B5 'reach' column (within-unit Spearman 0.992 in LIFEENV, 0.998 in MATHDEC). Once the pre-onset years are removed, D_vol is almost the baseline itself; in MATHDEC its partial correlation is undefined in the bootstrap, so MATHDEC is excluded from the D_vol pools. M0_density_post is less collinear with reach (within-unit Spearman from 0.63 in CS to 0.93 in Med) and its bootstrap is defined in every unit.
- Spearman(D_vol_post, D_vol_end) = 0.747; Spearman(footprint share, O2r_m50) = 0.085; share of held-out concepts with any pre-onset off-home entry 0.911.

**Paper wording.** About half of the M0_density_end and D_vol_end breadth signal comes from the concept's pre-onset footprint in other fields. The post-onset part is still clearly positive, so these are partly, but not only, early network signals.

Source: `round-4/evaluation-3/src/results/post_onset_rescore.json` -> `pooled.*; footprint_controlled; collinearity_post_vs_B5_reach; spearman`

## B2 OPEN per unit (O2r_m50 and O2r_resid)

- OPEN, O2r_m50, DL4: +0.181 [+0.082, +0.277], I2 0.73, prediction interval [-0.235, +0.541], positive in 6 of 6 units, CI includes 0 in 1 of 6.
- OPEN, O2r_m50, DL6: +0.163 [+0.108, +0.218], I2 0.62, prediction interval [-0.003, +0.321], positive in 6 of 6 units, CI includes 0 in 1 of 6.
- OPEN, O2r_resid, DL4: +0.177 [+0.076, +0.274], I2 0.73, prediction interval [-0.248, +0.544], positive in 6 of 6 units, CI includes 0 in 1 of 6.
- OPEN, O2r_resid, DL6: +0.157 [+0.102, +0.212], I2 0.62, prediction interval [-0.010, +0.316], positive in 6 of 6 units, CI includes 0 in 1 of 6.
- CONTACT_REACH without intersection-born (multi-home) concepts, O1c: +0.046 [+0.011, +0.080] (Exp8 sensitivity, verbatim from sensitivities_pooled.json; all rows of that file are carried in `results/per_group_extra.json`).
- CONTACT_REACH without intersection-born (multi-home) concepts, O2r_resid: +0.111 [+0.063, +0.158] (Exp8 sensitivity, verbatim from sensitivities_pooled.json; all rows of that file are carried in `results/per_group_extra.json`).

The full per-unit table (all confirmed indicators, the iteration-1 candidates, new_edge_rate, the post-onset rows, OPEN and OPEN_PC1; DEV units labelled SELECTION_DATA) is `results/per_group_table.csv`.

Source: `round-4/evaluation-3/src/results/per_group_pooled.csv` -> `indicator==OPEN&outcome==<o>&pool==<pool>::{pooled,ci_lo,ci_hi,I2,pi_lo,pi_hi,sign_pos_6,n_ci_includes_0_6}`

## B3 Specification curve

Across 1,920 specifications (120 composites x 4 outcomes x 4 control sets), the pooled psp CI excludes 0 in a share of 0.997 (4 held-out groups; 1.000 with the 2 cohort units). Median psp 0.152 (IQR 0.134-0.169). Under a Freedman-Lane null (200 draws), the null median is -0.0023 and the null share with CI > 0 averages 0.016; permutation p = 0.005 (the smallest possible with this many draws). Headline spec (all 6 components, equal weights, O2r_m50, C1): +0.183 [+0.083, +0.280], I2 0.73, prediction interval [-0.238, +0.547]. With contact reach as a control (C3) the median is 0.146 vs 0.158 under C1. Analytic vs bootstrap SE calibration: median width ratio 1.037 (< 1.2, no inflation).

**Reading.** The positive OPEN association is a property of the construct, not of one combination: every component subset, both weightings, all four breadth outcomes and all four control sets give a positive pooled estimate. The prediction interval of the headline spec includes 0, so a new domain can show a null.

Source: `round-4/evaluation-3/src/results/spec_curve.json` -> `n_specs; summary.*; null.DL4.*; headline.DL4.*; marginals.DL4.control.*; calibration.*`

## B4 Heterogeneity and the LIFEENV diagnosis

On 21 home-field x period sub-units (n >= 60), I2 is 0.43 (vs 0.66 over the 6 units). No trait explains the between-sub-unit variance (univariate REML meta-regression with Knapp-Hartung; Holm over 7 traits):

| trait (ecological, sub-unit level) | slope per SD | 95% CI | permutation p | Holm p |
|---|---|---|---|---|
| median_label_coverage | +0.018 | [-0.035, +0.072] | 0.485 | 1.000 |
| median_log_early_volume | -0.011 | [-0.076, +0.053] | 0.724 | 1.000 |
| share_multi_home | -0.019 | [-0.077, +0.039] | 0.492 | 1.000 |
| share_generic | +0.027 | [-0.032, +0.087] | 0.358 | 1.000 |
| median_O2r_m50 | -0.005 | [-0.052, +0.041] | 0.809 | 1.000 |
| sd_OPEN | -0.030 | [-0.090, +0.030] | 0.299 | 1.000 |
| mean_t0 | -0.026 | [-0.079, +0.027] | 0.316 | 1.000 |

LIFEENV: OPEN psp +0.071 vs the other 5 units pooled +0.186 [+0.133, +0.237]. (i) OPEN varies less in LIFEENV (SD ratio 0.88 [0.82, 0.94]; new_edge_rate 0.60), but the Thorndike range-restriction correction only moves psp to +0.080. (ii) Reweighting LIFEENV to the others' label-coverage distribution (entropy balancing) gives +0.069 [-0.019, +0.153]. Verdict under the frozen rule: **UNEXPLAINED**: neither coverage nor restricted range explains the weak LIFEENV cell, so it is treated as a domain boundary.

Source: `round-4/evaluation-3/src/results/heterogeneity.json` -> `k_subunits; I2_*; meta_regression.univariate.*; lifeenv.*`

Figures: `figures/spec_curve.pdf`, `figures/open_forest.pdf`, `figures/b1_post_onset.pdf`, `figures/lifeenv_diagnosis.pdf`.
