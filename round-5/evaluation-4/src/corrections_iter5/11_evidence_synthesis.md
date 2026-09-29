# 11 Evidence synthesis (new Section 32)

## 32. Evidence synthesis across bodies (iteration 5, descriptive)

[Correction, iteration 5, from this evaluation] How the home-only openness association behaves on every body scored so far. Same estimator, rungs and frozen EXP5 constants as Exp10; gate G1 reproduces Exp10's EXP5 selection psp (+0.099 at R0, +0.076 at R2) and gate G2 its cohort value (+0.091 [+0.013, +0.171]). Each body is labelled by design status: **selection** = the data on which the index or its constants were chosen; **already-unsealed** = held-out data whose outcomes earlier artifacts had already read; **confirmatory** = never used before the test. NOVCHURN_home = mean(z NOV_res, −z edge_persistence), the two home components that carried the cohort signal; it was chosen on the 2015-17 cohort, so that body is 'selection' for it.

**OPEN_home** (O2r_m50):

| body | onsets | status | R0 | R2 (primary) | R3 | n (R2) | placebo 95th pct abs psp |
|---|---|---|---|---|---|---|---|
| B1_DEV | 2003-09 | selection | +0.139 [+0.103, +0.174] | +0.109 [+0.073, +0.144] | +0.084 [+0.048, +0.121] | 3,003 | +0.035 |
| B2_PHYS | 2003-09 | already-unsealed | +0.083 [-0.014, +0.179] | +0.025 [-0.076, +0.128] | +0.041 [-0.065, +0.144] | 385 | +0.097 |
| B2_LIFEENV | 2003-09 | already-unsealed | +0.058 [-0.025, +0.140] | +0.067 [-0.018, +0.148] | +0.064 [-0.022, +0.147] | 552 | +0.084 |
| B2_SOC | 2003-09 | already-unsealed | +0.038 [-0.047, +0.121] | +0.044 [-0.041, +0.124] | +0.037 [-0.052, +0.121] | 546 | +0.087 |
| B2_MATHDEC | 2003-09 | already-unsealed | +0.259 [+0.008, +0.465] | +0.187 [-0.077, +0.409] | +0.168 [-0.099, +0.404] | 86 | +0.232 |
| B2_HELDOUT_pooled | 2003-09 | already-unsealed | +0.083 [+0.035, +0.133] | +0.070 [+0.021, +0.120] | +0.069 [+0.018, +0.119] | 1,569 | +0.056 |
| B3_EXP5_COHORT_2010_14 | 2010-14 | already-unsealed | +0.092 [+0.049, +0.136] | +0.074 [+0.029, +0.117] | +0.053 [+0.008, +0.097] | 1,993 | +0.037 |
| B4_COHORT_2015_17 | 2015-17 | confirmatory | +0.123 [+0.041, +0.205] | +0.091 [+0.013, +0.171] | +0.080 [+0.001, +0.162] | 573 | +0.077 |
| B5 Frame N | new frame (iteration-5 artifact) | pending iteration-5 artifact | - | - | - | - | - |

**NOVCHURN_home** (O2r_m50):

| body | onsets | status | R0 | R2 (primary) | R3 | n (R2) | placebo 95th pct abs psp |
|---|---|---|---|---|---|---|---|
| B1_DEV | 2003-09 | selection | +0.125 [+0.088, +0.162] | +0.116 [+0.079, +0.153] | +0.098 [+0.061, +0.137] | 2,741 | +0.035 |
| B2_PHYS | 2003-09 | already-unsealed | +0.099 [-0.006, +0.201] | +0.061 [-0.046, +0.179] | +0.078 [-0.030, +0.191] | 348 | +0.096 |
| B2_LIFEENV | 2003-09 | already-unsealed | +0.082 [-0.005, +0.168] | +0.084 [-0.008, +0.175] | +0.079 [-0.011, +0.172] | 500 | +0.092 |
| B2_SOC | 2003-09 | already-unsealed | +0.102 [+0.007, +0.188] | +0.124 [+0.029, +0.210] | +0.114 [+0.020, +0.199] | 489 | +0.096 |
| B2_MATHDEC | 2003-09 | already-unsealed | +0.204 [-0.095, +0.429] | +0.093 [-0.209, +0.408] | +0.078 [-0.236, +0.411] | 67 | +0.283 |
| B2_HELDOUT_pooled | 2003-09 | already-unsealed | +0.118 [+0.066, +0.169] | +0.113 [+0.061, +0.163] | +0.112 [+0.060, +0.163] | 1,404 | +0.051 |
| B3_EXP5_COHORT_2010_14 | 2010-14 | already-unsealed | +0.121 [+0.072, +0.167] | +0.113 [+0.065, +0.158] | +0.097 [+0.050, +0.144] | 1,799 | +0.048 |
| B4_COHORT_2015_17 | 2015-17 | selection (index chosen here) | +0.171 [+0.079, +0.256] | +0.161 [+0.071, +0.246] | +0.144 [+0.059, +0.226] | 506 | +0.087 |
| B5 Frame N | new frame (iteration-5 artifact) | pending iteration-5 artifact | - | - | - | - | - |

Random-effects pools at R2 (Fisher z, bootstrap SE; headline over non-selection bodies only, B2 groups entered separately):

| index | non-selection bodies | pooled psp | DL 95% CI | HKSJ 95% CI | I2 | tau2 (z) | sign agreement | all bodies (includes selection data) | selection body (DEV) | shrinkage DEV / pooled |
|---|---|---|---|---|---|---|---|---|---|---|
| OPEN_home | B2_PHYS, B2_LIFEENV, B2_SOC, B2_MATHDEC, B3_EXP5_COHORT_2010_14, B4_COHORT_2015_17 | +0.069 | [+0.038, +0.100] | [+0.042, +0.096] | 0.00 | 0.0000 | 6/6 | +0.085 | +0.109 | 1.58 |
| NOVCHURN_home | B2_PHYS, B2_LIFEENV, B2_SOC, B2_MATHDEC, B3_EXP5_COHORT_2010_14 | +0.105 | [+0.069, +0.140] | [+0.078, +0.131] | 0.00 | 0.0000 | 5/5 | +0.114 | +0.116 | 1.11 |

Leave one body out (pooled psp, R2): OPEN_home: without B2_PHYS +0.073; without B2_LIFEENV +0.069; without B2_SOC +0.073; without B2_MATHDEC +0.067; without B3_EXP5_COHORT_2010_14 +0.064; without B4_COHORT_2015_17 +0.065 | NOVCHURN_home: without B2_PHYS +0.110; without B2_LIFEENV +0.109; without B2_SOC +0.101; without B2_MATHDEC +0.105; without B3_EXP5_COHORT_2010_14 +0.094.

[FIGURE:fig_evidence_forest]

**Reading.** The home-only association is small and has the same sign in every body. It is consistently larger on the selection body (DEV) than on the non-selection pool (shrinkage ratio above), which is the winner's-curse pattern this run measured before. I2 is imprecise at this k. Because the non-selection bodies other than the 2015-17 cohort were already unsealed and reused, the pooled interval is **descriptive**: it is not a confirmation, and it is not a forecast gain (Section 25.7). NOVCHURN_home is shown for the Frame-N test; its cohort row is a selection estimate. The Frame-N row is empty and will be compared with this pool, not pooled into it.

Source: `results/evidence_synthesis.json` (this artifact; `src/synthesis.py`); figure `figures/evidence_forest.png|pdf`.
