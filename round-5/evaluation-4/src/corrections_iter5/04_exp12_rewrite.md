# 04 Experiment 12 rewrite (26.1, 26.2 addition, 26.3, 31.3 caveat)

### 26.1 Log-additive breadth decomposition

[Correction, iteration 5, from art_uw4OeagJP3rv] Rarefied breadth is decomposed as log Bn = log E2 (early contact) + log M (frontier advance) + log ρ (retention); shares of the top-vs-bottom O2r_resid tercile gap. **Bn and O2r share papers; the decomposition is an identity, not a causal split.**

Pre-registered predictions, verbatim (`preregistration_R2.json`):

> **PR1** EXPLORATION > RETENTION: in variant (iv) [volume-stratified (early-volume quintiles), concepts with a Medicine (field 27) home excluded], s_explore - s_ret > 0 with the 95% concept-bootstrap CI > 0, where s_explore = s_E2 + s_M and s_ret = s_rho are the shares of the top-vs-bottom O2r_resid tercile gap in log mean breadth (Bn = retained off-home fields at t0+8). Equivalently s_ret < 0.5; both are printed (shares sum to 1).
> **PR1b** (secondary, Holm family R2-A with PR1 and PR2): s_contact - s_ret > 0 with CI > 0 (s_contact = s_E2).
> **PR2** LOCALISED KEEP MORE EARLY: mean RETENTION_RATIO_early(bottom O2r_resid tercile) - mean(top tercile) > 0 with CI > 0, AND the partial Spearman of RETENTION_RATIO_early with O2r_resid given B5 < 0 (CI < 0). The latter is flagged 'replication on the same frame as EXP8, not new evidence'.
> **PR3** (descriptive, not tested): the sign of D_rho, i.e. whether late retention probability is lower for integrating (top-tercile) concepts.

s_explore − s_ret by variant and body [95% concept-bootstrap CI] (PR1 is variant iv; the primary display variant is ii):

| body | i pooled | ii volume-stratified (primary) | iii volume + Medicine adjusted | iv volume-stratified, no Medicine (PR1) |
|---|---|---|---|---|
| DEV | +0.464 [+0.407, +0.528] (n=3,188) | +0.431 [+0.371, +0.493] (n=3,188) | +0.446 [+0.383, +0.509] (n=3,188) | +0.633 [+0.537, +0.727] (n=1,469) |
| held-out (4 groups pooled) | +0.549 [+0.466, +0.625] (n=1,833) | +0.494 [+0.402, +0.576] (n=1,833) | +0.490 [+0.401, +0.572] (n=1,833) | +0.492 [+0.403, +0.575] (n=1,825) |
| 2010-14 cohort (pooled) | +0.421 [+0.358, +0.487] (n=2,182) | +0.343 [+0.276, +0.405] (n=2,182) | +0.362 [+0.291, +0.439] (n=2,182) | +0.445 [+0.358, +0.527] (n=1,403) |

DerSimonian-Laird over the held-out groups (PHYS, LIFEENV, SOC, variant iv): +0.504 [+0.329, +0.679], I2 = 0.76.

Verdicts per clause (the rule: SUPPORTED / NOT SUPPORTED / REVERSED by CI side, per body):

| body | PR1 (s_explore − s_ret, variant iv) | PR1b (s_contact − s_ret) | PR2 (bottom − top retention ratio; psp given B5) | PR3 (descriptive) |
|---|---|---|---|---|
| DEV | SUPPORTED: +0.633 [+0.537, +0.727] | SUPPORTED: +0.604 [+0.508, +0.698] | REVERSED: diff -0.110 [-0.132, -0.086]; psp -0.169 [-0.202, -0.134] | D_rho +0.202 [+0.144, +0.267] |
| held-out | SUPPORTED: +0.492 [+0.403, +0.575] | SUPPORTED: +0.480 [+0.394, +0.570] | NOT SUPPORTED: diff +0.011 [-0.019, +0.039]; psp -0.129 [-0.175, -0.086] | D_rho +0.263 [+0.207, +0.325] |
| 2010-14 cohort | SUPPORTED: +0.445 [+0.358, +0.527] | SUPPORTED: +0.414 [+0.324, +0.494] | REVERSED: diff -0.058 [-0.083, -0.031]; psp -0.173 [-0.212, -0.133] | D_rho +0.291 [+0.237, +0.351] |

PR2 is REVERSED on its first clause wherever the difference is negative: localised concepts do **not** keep more early; the psp clause replicates EXP8 on the same frame and is not new evidence.

Source: `round-4/experiment-12/src/results/decomposition_dev.json`, `decomposition_heldout.json` -> `variants.*`, `verdicts.*`, `DL_heldout_groups`; `preregistration_R2.json`.

### 26.3 Sequence: home prominence first, or born at the intersection?

[Correction, iteration 5, from art_uw4OeagJP3rv] A = first age with home-field prominence ≥ half its 0-8 maximum; T = first cross-field take-off age. The share of concepts with A < T is compared with a mechanical-lag null (1,000 within-concept permutations of the prominence series). The hazard ratio compares take-off of intersection-born concepts with single-home concepts (cloglog, controlling log volume).

| body | n | share A < T | null share | excess [95% CI] | intersection-born take-off HR [95% CI] | verdict |
|---|---|---|---|---|---|---|
| DEV | 4,555 | 0.256 | 0.264 | -0.009 [-0.015, -0.003] | 0.47 [0.42, 0.54] | MIXED |
| held-out | 3,280 | 0.136 | 0.126 | +0.011 [+0.005, +0.016] | 0.45 [0.38, 0.52] | HOME-FIRST |
| 2010-14 cohort | 4,195 | 0.160 | 0.178 | -0.017 [-0.023, -0.012] | 0.41 [0.35, 0.47] | MIXED |

The excess over the mechanical lag is at most a few percentage points and changes sign between bodies (HOME-FIRST only on the held-out groups). Intersection-born concepts take off **later**, not earlier (HR < 1 in every body). There is no general home-first sequence and no intersection route.

Source: `sequence_light_dev.json`, `sequence_light_heldout.json` -> `<body>.order`, `mechanical_lag_null`, `cloglog_hazard`, `verdict`.

## Addition to 26.2

[Correction, iteration 5, from art_uw4OeagJP3rv] Where OPEN sits in the trajectory space (partial Spearman given B5 and label coverage):

| build | DEV PC1 | DEV PC2 | held-out DL PC1 | 2010-14 cohort PC1 |
|---|---|---|---|---|
| OPEN_all | +0.174 [+0.146, +0.202] | -0.105 [-0.133, -0.076] | +0.120 [+0.085, +0.155] | +0.117 [+0.087, +0.147] |
| OPEN_home | +0.117 [+0.085, +0.146] | -0.068 [-0.099, -0.037] | +0.060 [+0.023, +0.097] | +0.121 [+0.088, +0.153] |
| OPEN_sizematch | +0.135 [+0.107, +0.163] | -0.076 [-0.103, -0.049] | +0.094 [+0.060, +0.129] | +0.089 [+0.058, +0.119] |

The typology is a continuum (DTW-HMM ARI 0.222); OPEN loads on the breadth axis (PC1) and weakly negatively on PC2 (retention-heavy profiles) for the all-papers build.

Source: `trajectories_dev.json` -> `open_on_axis.pooled`, `hmm.ari_dtw_hmm`; `trajectories_heldout.json` -> `DL_heldout_groups_PC1`, `open_on_axis_cohort_PC1`. (`open_diagnostics.json` holds build correlations and coverage, not the PC table.)
