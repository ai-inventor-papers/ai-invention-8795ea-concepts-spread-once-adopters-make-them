# 08 Secondary: Exp10 leads, 25.6 learned models, tags under 19.5b / 19.7, per-group table

## 25.5

[Correction, iteration 5, from art_NMe386dX9GLF] Secondary leads, verbatim from the Exp10 README (lines 48-53):

> * **Leads replicated (secondary):**
>   * CONTACT_REACH on O2r_m50 given R0: +0.211 [+0.122, +0.294] (EXP8 +0.210), halving to +0.101 without
>     intersection-born concepts (EXP8 +0.111);
>   * n_authors_early on O1c: +0.115 [+0.065, +0.165] (EXP8 +0.161);
>   * RETENTION_RATIO_early < 0 given R0 (EXP8 -0.114), but it vanishes once type and reach enter (R2 -0.043, CI includes 0).
>   * n_authors_early does NOT replicate for O3 (+0.014) or O1b (+0.036).

Keyed values: CONTACT_REACH on O2r_m50 given R0 +0.211 [+0.122, +0.294], without intersection-born concepts +0.101 (n = 613).

### 25.6 Learned models (cohort)

[Correction, iteration 5, from art_NMe386dX9GLF]

| outcome | metric | B5 | linear_all | diff [95% CI] | n | evaluable |
|---|---|---|---|---|---|---|
| O2r_m50 | Spearman | +0.789 | +0.818 | +0.030 [+0.012, +0.049] | 634 | yes |
| O2r_resid | Spearman | +0.789 | +0.816 | +0.027 [+0.009, +0.046] | 634 | yes |
| O3 | AUC | +0.561 | +0.540 | -0.021 [-0.130, +0.101] | 1443 | yes |
| O4 | - | - | - | - | - | no: not evaluable: O4 not computed (no citation pass; declared drop) |

The transience (O3) row is **evaluable and null**: AUC +0.540 vs +0.561, difference -0.021 [-0.130, +0.101]. The earlier row, which labelled this transience difference as not evaluable, was wrong. The frozen B5 + OPEN_home forecast adds +0.002 [-0.003, +0.008] (Section 25.7).

Source: `round-4/experiment-10/src/results/learned_models_cohort.json`; `cohort_result.json` -> `secondary.frozen_prediction_O2r_m50`.

## 19.5b

[Correction, iteration 5, from art_NMe386dX9GLF] On the 2015-2017 cohort the learned model does not predict transience either: O3 AUC +0.540 vs B5 +0.561, -0.021 [-0.130, +0.101] (Section 25.6).

## 19.7

[Correction, iteration 5, from art_NMe386dX9GLF] Cohort check: linear_all over B5 on O2r_m50 +0.030 [+0.012, +0.049]; the frozen B5 + OPEN_home forecast gains +0.002 (Section 25.6).

## 19.2 per-group table

[Correction, iteration 5, from art_dFQ6jbgNsR6Q] Per-group held-out results for the confirmed O2r_m50 indicators (psp [95% CI] (n); † = CI includes 0). Domain failures are shown, not averaged away:

| indicator | PHYS | LIFEENV | SOC | MATHDEC | COH_DEVHOME | COH_OTHER | † cells |
|---|---|---|---|---|---|---|---|
| M0_density_end | +0.429 [+0.333, +0.520] (413) | +0.298 [+0.223, +0.372] (630) | +0.302 [+0.227, +0.372] (689) | +0.547 [+0.377, +0.673] (101) | +0.276 [+0.219, +0.327] (1368) | +0.354 [+0.290, +0.415] (814) | 0 |
| D_vol_end | +0.372 [+0.262, +0.477] (413) | +0.264 [+0.182, +0.348] (630) | +0.325 [+0.256, +0.395] (689) | +0.226 [+0.045, +0.434] (101) | +0.294 [+0.244, +0.350] (1368) | +0.318 [+0.251, +0.378] (814) | 0 |
| CONTACT_REACH | +0.254 [+0.152, +0.350] (413) | +0.184 [+0.094, +0.273] (630) | +0.210 [+0.134, +0.290] (689) | +0.174 [-0.062, +0.449] (101)† | +0.213 [+0.154, +0.268] (1368) | +0.227 [+0.158, +0.296] (814) | 1 |
| n_comm_W3 | +0.124 [+0.020, +0.225] (413) | +0.055 [-0.017, +0.136] (630)† | +0.193 [+0.118, +0.263] (689) | +0.360 [+0.193, +0.503] (101) | +0.222 [+0.169, +0.272] (1368) | +0.096 [+0.029, +0.169] (814) | 1 |
| RETENTION_RATIO_early | -0.062 [-0.154, +0.036] (413)† | -0.117 [-0.191, -0.037] (630) | -0.139 [-0.217, -0.069] (689) | -0.178 [-0.433, +0.076] (101)† | -0.187 [-0.231, -0.134] (1368) | -0.105 [-0.169, -0.037] (814) | 2 |
| NOV | +0.175 [+0.076, +0.265] (391) | +0.033 [-0.046, +0.119] (604)† | +0.132 [+0.051, +0.210] (668) | +0.440 [+0.194, +0.632] (85) | +0.114 [+0.058, +0.170] (1296) | +0.038 [-0.032, +0.109] (782)† | 2 |
| ego_density_W3 | -0.081 [-0.182, +0.024] (397)† | -0.078 [-0.164, +0.008] (610)† | -0.122 [-0.199, -0.043] (668) | -0.236 [-0.434, +0.029] (96)† | -0.095 [-0.150, -0.034] (1319) | -0.041 [-0.112, +0.030] (794)† | 4 |

Source: `round-3/experiment-8/src/results/heldout_unit_results.csv` (outcome == O2r_m50); confirmed list from `heldout_summary.json -> O2r_m50[*].confirmed`.
