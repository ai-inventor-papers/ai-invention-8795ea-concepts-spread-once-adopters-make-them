# Which early network signals travel across fields? A sealed held-out test of ~53 emergence indicators

AI Inventor, invention loop iteration 3, artifact `gen_art_experiment_8` (plan `gen_plan_experiment_2_idx2`, RQ1).

<!-- RESULTS -->
<!-- TABLES -->
### Frozen top 10, scored once on the held-out groups (DL-pooled PHYS/LIFEENV/SOC/MATHDEC)

psp = partial Spearman given B5 (+ onset-year dummies); binary outcomes: dAUC over B5 with frozen DEV coefficients. `sign` = frozen DEV sign; `agree` = units (4 groups + 2 cohort parts) with that sign; **bold** = confirmed (Holm p < 0.05 within the outcome family and pooled sign = frozen sign).


**O1c**

| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |
|---|---|---|---|---|---|---|---|---|
| **n_authors_early** | E | + | +0.161 | [+0.090, +0.230] | 0.70 | 0.000101 | 6/6 | +0.171 / +0.140 |
| burst | E | + | +0.019 | [-0.052, +0.089] | 0.69 | 1 | 4/6 | +0.106 / -0.014 |
| S_comp_n | S | - | -0.087 | [-0.200, +0.029] | 0.88 | 1 | 6/6 | -0.107 / -0.097 |
| CONTACT_REACH | FR | + | +0.048 | [+0.013, +0.084] | 0.00 | 0.0666 | 6/6 | +0.056 / +0.018 |
| author_growth | E | + | +0.035 | [-0.024, +0.094] | 0.61 | 1 | 5/6 | +0.003 / +0.026 |
| growth_ind | E | + | -0.008 | [-0.042, +0.026] | 0.00 | 1 | 3/6 | +0.050 / +0.003 |
| comm_transitions | A | - | +0.021 | [-0.038, +0.079] | 0.63 | 1 | 2/6 | +0.004 / +0.008 |
| share | E | + | +0.013 | [-0.024, +0.050] | 0.01 | 1 | 3/6 | -0.017 / +0.007 |
| fields_gained_per_yr | F | + | +0.002 | [-0.033, +0.036] | 0.00 | 1 | 4/6 | +0.004 / -0.020 |
| new_edge_rate | A | + | -0.002 | [-0.042, +0.038] | 0.19 | 1 | 5/6 | +0.024 / +0.003 |

**O2r_m50**

| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |
|---|---|---|---|---|---|---|---|---|
| **M0_density_end** | FR | + | +0.375 | [+0.279, +0.462] | 0.74 | 3.92e-12 | 6/6 | +0.276 / +0.354 |
| **D_vol_end** | FR | + | +0.307 | [+0.256, +0.356] | 0.10 | 3.69e-28 | 6/6 | +0.294 / +0.318 |
| **CONTACT_REACH** | FR | + | +0.211 | [+0.161, +0.261] | 0.00 | 9.3e-15 | 6/6 | +0.213 / +0.227 |
| **n_comm_W3** | A | + | +0.167 | [+0.063, +0.267] | 0.78 | 0.0088 | 6/6 | +0.222 / +0.096 |
| RS | G | - | -0.072 | [-0.153, +0.010] | 0.44 | 0.156 | 5/6 | -0.175 / -0.128 |
| G_btw (prev. scored) | G | + | +0.056 | [-0.006, +0.118] | 0.33 | 0.156 | 6/6 | +0.062 / +0.033 |
| log_offhome_volume | F | - | -0.089 | [-0.171, -0.007] | 0.63 | 0.102 | 5/6 | -0.155 / -0.125 |
| **RETENTION_RATIO_early** | FR | - | -0.114 | [-0.160, -0.067] | 0.00 | 1.32e-05 | 6/6 | -0.187 / -0.105 |
| **NOV** | A | + | +0.151 | [+0.044, +0.255] | 0.75 | 0.023 | 6/6 | +0.114 / +0.038 |
| **ego_density_W3** | A | - | -0.102 | [-0.151, -0.053] | 0.00 | 0.000288 | 6/6 | -0.095 / -0.041 |

**O2r_resid**

| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |
|---|---|---|---|---|---|---|---|---|
| **M0_density_end** | FR | + | +0.377 | [+0.280, +0.466] | 0.75 | 7.67e-12 | 6/6 | +0.274 / +0.358 |
| **D_vol_end** | FR | + | +0.307 | [+0.257, +0.356] | 0.10 | 1.14e-28 | 6/6 | +0.295 / +0.321 |
| **CONTACT_REACH** | FR | + | +0.210 | [+0.159, +0.260] | 0.00 | 1.71e-14 | 6/6 | +0.203 / +0.222 |
| **n_comm_W3** | A | + | +0.164 | [+0.058, +0.266] | 0.79 | 0.0124 | 6/6 | +0.219 / +0.092 |
| RS | G | - | -0.073 | [-0.151, +0.005] | 0.41 | 0.136 | 5/6 | -0.179 / -0.130 |
| **log_offhome_volume** | F | - | -0.100 | [-0.171, -0.028] | 0.53 | 0.027 | 6/6 | -0.182 / -0.134 |
| G_btw (prev. scored) | G | + | +0.055 | [-0.008, +0.118] | 0.33 | 0.136 | 5/6 | +0.059 / +0.037 |
| **RETENTION_RATIO_early** | FR | - | -0.120 | [-0.166, -0.073] | 0.00 | 3.98e-06 | 6/6 | -0.191 / -0.107 |
| **NOV** | A | + | +0.152 | [+0.042, +0.258] | 0.76 | 0.027 | 6/6 | +0.110 / +0.042 |
| **ego_density_W3** | A | - | -0.097 | [-0.146, -0.048] | 0.00 | 0.000654 | 6/6 | -0.092 / -0.037 |

**O4**

| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |
|---|---|---|---|---|---|---|---|---|
| G_deg | G | - | -0.021 | [-0.069, +0.028] | 0.41 | 1 | 5/6 | -0.093 / -0.058 |
| log_offhome_volume | F | - | -0.002 | [-0.069, +0.066] | 0.66 | 1 | 3/6 | -0.080 / +0.014 |
| **REL_home** | G | - | -0.114 | [-0.180, -0.047] | 0.69 | 0.00922 | 6/6 | -0.013 / -0.072 |
| burst | E | - | +0.014 | [-0.043, +0.072] | 0.55 | 1 | 3/6 | -0.103 / +0.005 |
| G_A (prev. scored) | G | - | -0.010 | [-0.055, +0.036] | 0.33 | 1 | 4/6 | -0.059 / -0.049 |
| **author_growth** | E | + | +0.065 | [+0.024, +0.106] | 0.21 | 0.0182 | 5/6 | +0.049 / +0.080 |
| G_phimin | G | + | +0.064 | [-0.080, +0.206] | 0.93 | 1 | 5/6 | +0.057 / +0.048 |
| FRONTIER_POTENTIAL | FR | - | -0.017 | [-0.063, +0.030] | 0.39 | 1 | 5/6 | -0.074 / -0.047 |
| RETENTION_RATIO_early | FR | - | -0.026 | [-0.060, +0.009] | 0.00 | 1 | 5/6 | -0.075 / -0.024 |
| new_edge_rate | A | - | +0.003 | [-0.032, +0.037] | 0.00 | 1 | 3/6 | -0.058 / +0.000 |

**O1b**

| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |
|---|---|---|---|---|---|---|---|---|
| **n_authors_early** | E | + | +0.029 | [+0.015, +0.044] | 0.00 | 0.000789 | 4/6 | -0.002 / -0.006 |
| G_phimin | G | + | +0.001 | [-0.011, +0.013] | 0.00 | 1 | 3/6 | +0.011 / -0.007 |
| rao_stirling | F | + | -0.002 | [-0.022, +0.017] | 0.32 | 1 | 2/6 | +0.014 / -0.034 |
| G (prev. scored) | G | - | +0.000 | [-0.003, +0.003] | 0.00 | 1 | 1/6 | +0.000 / +0.001 |
| kcore_end | A | + | +0.010 | [-0.004, +0.023] | 0.00 | 1 | 5/6 | +0.011 / +0.019 |
| S_comp_n | S | + | +0.028 | [-0.003, +0.058] | 0.77 | 0.697 | 5/6 | +0.005 / -0.015 |
| M0_density_end | FR | + | +0.012 | [-0.004, +0.027] | 0.00 | 1 | 4/6 | +0.007 / -0.006 |
| REL_home | G | + | -0.002 | [-0.015, +0.010] | 0.18 | 1 | 2/6 | +0.009 / -0.022 |
| CONTACT_REACH | FR | + | +0.008 | [-0.006, +0.023] | 0.00 | 1 | 5/6 | +0.008 / +0.001 |
| G_btw (prev. scored) | G | - | +0.001 | [-0.005, +0.007] | 0.00 | 1 | 3/6 | +0.001 / -0.005 |

**O3**

| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |
|---|---|---|---|---|---|---|---|---|
| **n_authors_early** | E | + | +0.089 | [+0.031, +0.148] | 0.00 | 0.0286 | 4/5 | +0.019 / -0.021 |
| S_comp_n | S | + | +0.068 | [+0.001, +0.134] | 0.10 | 0.406 | 4/5 | +0.039 / -0.029 |
| rao_stirling | F | + | +0.066 | [-0.002, +0.134] | 0.22 | 0.446 | 3/5 | +0.040 / -0.036 |
| G_deg | G | + | +0.036 | [-0.007, +0.079] | 0.00 | 0.586 | 4/5 | +0.046 / -0.023 |
| REL_home | G | + | +0.001 | [-0.056, +0.059] | 0.32 | 1 | 2/5 | +0.034 / -0.008 |
| G_btw (prev. scored) | G | + | +0.040 | [-0.024, +0.104] | 0.48 | 0.891 | 3/5 | +0.064 / -0.009 |
| fields_gained_per_yr | F | + | +0.010 | [-0.042, +0.061] | 0.00 | 1 | 1/5 | -0.015 / -0.027 |
| M0_density_end | FR | + | +0.038 | [-0.011, +0.086] | 0.00 | 0.655 | 4/5 | +0.023 / +0.001 |
| G_A (prev. scored) | G | + | +0.053 | [-0.058, +0.165] | 0.79 | 1 | 4/5 | +0.036 / +0.013 |
| CONTACT_REACH | FR | + | +0.049 | [-0.003, +0.101] | 0.00 | 0.452 | 5/5 | +0.016 / +0.012 |

**O5**

| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |
|---|---|---|---|---|---|---|---|---|
| G_phimin | G | + | -0.004 | [-0.012, +0.004] | 0.00 | 1 | 1/6 | +0.014 / -0.004 |
| REL_home | G | + | -0.008 | [-0.024, +0.007] | 0.58 | 1 | 3/6 | +0.005 / +0.000 |
| S_comp_n | S | + | +0.003 | [-0.002, +0.009] | 0.00 | 1 | 6/6 | +0.008 / +0.027 |
| burst | E | - | +0.000 | [-0.003, +0.003] | 0.00 | 1 | 1/6 | +0.022 / +0.012 |
| n_authors_early | E | + | +0.003 | [-0.001, +0.008] | 0.00 | 1 | 5/6 | +0.005 / +0.020 |
| G (prev. scored) | G | - | -0.000 | [-0.002, +0.001] | 0.00 | 1 | 3/6 | +0.001 / -0.001 |
| FRONTIER_POTENTIAL | FR | + | +0.001 | [-0.003, +0.006] | 0.00 | 1 | 5/6 | +0.006 / +0.018 |
| share | E | - | -0.002 | [-0.004, +0.001] | 0.00 | 1 | 6/6 | -0.011 / -0.008 |
| G_btw (prev. scored) | G | - | +0.000 | [-0.002, +0.003] | 0.00 | 1 | 1/6 | +0.002 / +0.007 |
| deg_W1 | A | + | +0.002 | [-0.002, +0.007] | 0.00 | 1 | 5/6 | +0.002 / -0.007 |

**O5_WW**

| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |
|---|---|---|---|---|---|---|---|---|
| G_phimin | G | + | -0.001 | [-0.006, +0.005] | 0.05 | 1 | 2/6 | -0.007 / -0.004 |
| G_deg | G | + | +0.001 | [-0.006, +0.008] | 0.18 | 1 | 4/6 | -0.008 / +0.003 |
| REL_home | G | + | -0.005 | [-0.016, +0.006] | 0.54 | 1 | 1/6 | -0.010 / -0.007 |
| S_comp | S | + | -0.005 | [-0.011, +0.002] | 0.00 | 1 | 1/6 | -0.009 / +0.016 |
| G_A (prev. scored) | G | - | +0.001 | [-0.001, +0.004] | 0.00 | 1 | 4/6 | -0.007 / -0.003 |
| FRONTIER_POTENTIAL | FR | + | +0.003 | [-0.002, +0.008] | 0.03 | 1 | 4/6 | -0.004 / +0.010 |
| G_btw (prev. scored) | G | - | +0.001 | [-0.002, +0.004] | 0.00 | 1 | 3/6 | -0.002 / -0.004 |
| btw_end | A | + | +0.001 | [-0.003, +0.004] | 0.00 | 1 | 4/6 | +0.011 / -0.002 |
| ego_density_W3 | A | + | +0.000 | [-0.004, +0.005] | 0.00 | 1 | 3/6 | +0.005 / -0.008 |
| rao_stirling | F | + | -0.003 | [-0.013, +0.008] | 0.63 | 1 | 1/6 | -0.006 / -0.013 |

### Learned models vs B5 vs B5 + best single (held-out groups pooled)

Spearman(pred, y) for continuous outcomes, AUC for binary; [95% CI of the paired difference vs B5].

| outcome | n | B5 | B5 + best single | ElasticNet / L1-logit (all) | EBM |
|---|---|---|---|---|---|
| O1c | 3372 | 0.312 | 0.305 [-0.016, +0.004] | 0.303 [-0.019, -0.001] | 0.313 [-0.022, +0.026] |
| O2r_m50 | 1833 | 0.706 | 0.739 [+0.022, +0.045] | 0.765 [+0.046, +0.073] | 0.757 [+0.037, +0.067] |
| O2r_resid | 1833 | 0.704 | 0.738 [+0.023, +0.047] | 0.763 [+0.047, +0.071] | 0.756 [+0.038, +0.066] |
| O4 | 3372 | 0.015 | 0.028 [-0.009, +0.036] | constant (all coef. 0) | 0.188 [+0.129, +0.219] |
| O1b | 3372 | 0.507 | 0.518 [-0.003, +0.029] | 0.524 [-0.000, +0.039] | 0.526 [-0.001, +0.042] |
| O3 | 3372 | 0.506 | 0.576 [+0.020, +0.128] | 0.599 [+0.028, +0.163] | 0.599 [+0.033, +0.161] |
| O5 | 1417 | 0.746 | 0.742 [-0.013, +0.003] | 0.747 [-0.009, +0.009] | 0.726 [-0.038, -0.004] |
| O5_WW | 1671 | 0.747 | 0.746 [-0.007, +0.005] | 0.751 [-0.003, +0.010] | 0.719 [-0.046, -0.011] |

### Pre-registered predictions (frozen before the unseal)

| id | prediction | verdict |
|---|---|---|
| P1 | entropy, D_rare, D_ratio, participation, NOV_res: raw Spearman with O2r_m50 > 0 (CI > 0) in >= 3 of 4 held-out groups; AND D_rare, D_ratio, participation, NOV_res: pooled psp|B5 CI upper bound < 0.10 | **FAILS** |
| P2 | edge_persistence: pooled raw rho and pooled psp with O2r_m50 both < 0 | **HOLDS** |
| P3 | deg_growth, str_growth, new_edge_rate FAIL held-out: pooled psp CI includes 0 OR sign flip in >= 2 of 4 groups | **FAILS** |
| P4 | RETENTION_RATIO_early and FRONTIER_POTENTIAL: pooled psp > 0 with CI > 0 for O2r_resid AND O1c | **FAILS** |
| P5 | CONTACT_REACH: pooled psp CI includes 0 (also reported given B5 minus reach) | **FAILS** |
<!-- /TABLES -->
**Question (RQ1).** Which temporal network indicators, measured only in a concept's first three years (t0..t0+2),
anticipate its later emergence outcomes beyond simple volume/growth/breadth (B5), and do they generalise across
scientific domains? About 53 indicators in 7 families were ranked on DEV home groups only (CS, Engineering,
Biochem/Genetics, Medicine; 4,771 concepts), the top 10 per outcome were frozen and hash-sealed, and the frozen
spec was scored **once** on four held-out home groups (PHYS 742, LIFEENV 1,113, SOC 1,352, MATHDEC 165) and on a
2010-14 onset cohort split into DEV-home (2,484) and other-home (1,872) parts.

## Headline results

1. **Breadth (O2r_m50 / O2r_resid, rarefied venue-field richness at t0+6..t0+8) is predictable beyond B5, and the
   signal travels.** 7 (O2r_m50) and 8 (O2r_resid) of the frozen top 10 are confirmed (Holm p < 0.05; every
   confirmed indicator has the frozen sign in 6/6 units). The strongest are field-state indicators: `M0_density_end` (Hidalgo density of the fields not yet
   entered by t0+2) psp **+0.377** [+0.280, +0.466], `D_vol_end` (# off-home fields entered by t0+2) **+0.307**
   [+0.257, +0.356], `CONTACT_REACH` **+0.210** [+0.159, +0.260]. Ego-network rows also transfer: `n_comm_W3`
   +0.164, `NOV` +0.152 (positive), `ego_density_W3` -0.097 and `RETENTION_RATIO_early` -0.120 (negative). Both
   cohort parts agree in sign.
   **Caveat:** `M0_density_end` and `D_vol_end` use cumulative field history 1995..t0+2 (EXP6 D3 definition), so
   part of their signal is a **pre-onset field footprint** (the highest-scoring held-out concepts are generic terms
   such as "Coefficient of variation" and "Exponential growth"). `CONTACT_REACH`, `n_comm_W3`, `NOV` and
   `ego_density_W3` use only t0..t0+2.
2. **Sustained uptake (O1c) is essentially a size/author signal.** Only `n_authors_early` is confirmed (psp +0.161
   [+0.090, +0.230], 6/6 units); `CONTACT_REACH` +0.048 [+0.013, +0.084] misses Holm (p = 0.067). No ego-network
   indicator transfers for O1c; learned models do not beat B5 (Spearman 0.303-0.313 vs 0.312). The same author-base
   indicator is the only confirmed one for the binary retention/transience outcomes (O1b dAUC +0.029, O3 +0.089).
3. **Citation growth (O4, field- and year-normalised)**: `REL_home` (-0.114) and `author_growth` (+0.065) are
   confirmed. The linear model on all indicators shrinks to a constant, while the EBM reaches held-out Spearman
   0.188 vs 0.015 for B5 (paired CI of the gain +0.13..+0.22): O4 signal is non-linear.
4. **External recognition (O5 all sources, O5_WW Wikipedia/Wikidata) is NOT anticipated by any indicator.** No DEV
   CI excluded 0, the frozen (filled) top 10s are all null held-out, and no model beats B5 + onset year
   (AUC 0.746-0.751). O5 is dominated by Wikipedia page creation.
5. **Learned vs single.** For breadth, ElasticNet on all indicators beats B5 held-out (Spearman 0.765 vs 0.706,
   +0.059 [+0.046, +0.073]) and B5 + best single (0.739). The EBM is close (0.757). For O3 (transience) the L1-logit
   gains +0.093 AUC [+0.028, +0.163] over a B5 model that is at chance (0.506).
6. **Pre-registered predictions** (from iteration-1 P78 portability): P2 (edge_persistence negative for breadth)
   **HOLDS**; P1, P3, P4, P5 **FAIL**. P3 fails because `new_edge_rate` transfers (+0.118) while
   degree/strength growth are null as predicted; P5 fails because `CONTACT_REACH` adds signal even given
   B5-minus-reach (+0.223 for O2r_resid); P4 fails because `RETENTION_RATIO_early` is **negative** (-0.120).
7. **Robustness.** Breadth results hold when excluding EXP6-overlap concepts, adding label-coverage covariates, using
   O2r_m30, or using EXP5's own O2r_resid definition (O2r_resid_N); excluding intersection-born concepts halves
   `CONTACT_REACH` (+0.111) but leaves it positive.

**Disclosure (second use).** EXP5 already unsealed O1/O3/O2r for these held-out concepts (its H1/H3). No selection
here touched held-out rows; G, G_A and G_btw were scored once before on O2r_resid and are flagged "prev. scored".

**Audits.** T0 unit tests 7/7 pass; T0-8: the ported EXP3 ego code reproduces EXP3 P78 features exactly (max
|diff| ~1e-15); T1: Pass A per-file counts equal EXP5's exactly; T2: A1 identical yearly grounded counts for all
12,499 concepts, A2 background Spearman 1.000 vs EXP3; T3: 99.8% of citation links have citing year >= cited year;
T5: DEV placebo 3.25/53 indicators with CI excluding 0 (<= 6), 29 indicator clusters at |rho| < 0.7, B5 LOGO
Spearman with O2r_m50 0.755; T6 pre-unseal checklist passed (commit 64ed779); T7 (`audit.py`) independent psp
equal to 4e-16, dAUC equal to sklearn to 3e-16, shuffled-outcome pooled |psp| 0.021, planted psp 0.10 recovered
(0.089, CI > 0); `rederive.py` re-derives all 40 continuous pooled headline estimates with analytic SEs (100% same
significance call, max |diff| 0.013) and all learned-model metrics (diff 1e-16); shuffled controls all null.
Power: pooled MDE (2.8 SE) = 0.049; MATHDEC alone 0.23 (uninformative on its own).


## Layout

| path | content |
|---|---|
| `method.py` | end-to-end orchestrator (`--from STEP`, `--only STEP`); steps below |
| `passA.py` | zero-credit OpenAlex S3 pass: EXP5 matcher + TAG grounding unchanged; early work/topic/author ids, topic background, reference sample |
| `passB.py` | citations received by early works and by the reference sample (O4) |
| `build_features.py` | the indicator matrix (families E, F, G, FR, A, S + B5) over t0..t0+2 |
| `outcomes.py` | one outcome table (O1c, O1b, O2r_m50/m30, O2r_resid, O3, O4, O5, O5_WW) and the outcome seal |
| `dev_select.py` | DEV-only ranking, frozen top 10s, learned models, power, freeze + seal |
| `heldout.py` | the single unseal; frozen scoring, DL pooling, Holm, learned vs single, portability table, P1-P5, sensitivities |
| `audit.py` | T7 independent re-derivation (own ranks/OLS, sklearn AUC, shuffled and planted controls) |
| `make_outputs.py` | `results/rq1_heldout.json`, figures, case exemplars, `method_out.json` |
| `lib/common.py` | paths, constants, frame loader (EXP5 `frame_concepts.csv`), helpers |
| `lib/common5.py`, `lib/matcher.py`, `lib/rangefile.py` | EXP5 analyser / Aho-Corasick matcher / HTTP-range parquet reader (copied; mkdir side effect removed) |
| `lib/ego.py`, `lib/ego_ctx.py` | EXP3 `features.concept_core` ported (1-year windows) + context (EXP3 Leiden backbones, Pass A background) |
| `lib/ego_exp3_orig.py`, `lib/common3.py` | the unmodified EXP3 sources, for reference |
| `lib/rq1stats.py` | partial Spearman + refit bootstrap, L2-logistic LOGO dAUC + bootstrap, DL pooling, Holm |
| `lib/design.py` | frozen imputation / missing flags / standardisation for the learned models |
| `lib/indicators.py` | indicator dictionary, families, outcomes, pre-registered predictions |
| `lib/seal.py` | freeze / unseal gate (refuses without a matching spec hash, refuses a second unseal) |
| `lib/h2.py`, `lib/stats_core.py` | EXP6 sources (D3 state machine, DL pooling), copied for provenance |
| `tests/test_units.py`, `tests/t0_8_ego_port.py`, `tests/t1_check.py`, `tests/checks.py` | T0, T0-8, T1, T2/T3 |
| `inputs/` | frozen lexicon (sha256 checked), source->field map, EXP3 backbones + topic metadata, EXP6 field backbone |
| `data/frame_matches_early/part_*.parquet` | **kept**: grounded frame hits t0-3..t0+2 with work, topic and author ids |
| `data/cites_early.parquet` | **kept**: citations to early works and the reference sample by citing year |
| `data/ref_sample.parquet`, `data/bg_topics.npz`, `data/counts_check.parquet` | reference sample, topic background, reproduction counts |
| `data/features_basic.parquet`, `data/ego_features.parquet` | families E/F/G/FR/S and A |
| `data/outcomes_dev.parquet`, `data/outcomes_sealed.parquet`, `data/outcomes.parquet`, `data/analysis_table.parquet` | outcome tables (sealed file hashed in `logs/outcome_seal.log`) |
| `results/` | every result table / JSON (see below) |
| `figures/` | PNG + PDF figures |
| `models/` | frozen learned models (joblib) |
| `logs/seal.log`, `logs/unsealed.json` | seal evidence |


| results file | content |
|---|---|
| `results/rq1_heldout.json` | **headline deliverable**: held-out summary per outcome, learned vs single, precision@top-decile, P1-P5 verdicts, sensitivities, audits, base rates, exemplars |
| `results/heldout_summary.json`, `results/heldout_unit_results.csv` | pooled and per-unit held-out estimates (frozen top 10 + union) |
| `results/portability_table.csv` | every indicator (+B5) x 10 units x {O2r_m50, O2r_resid, O1c}: psp, CI, raw Spearman; FROZEN/EXPLORATORY; previously_scored |
| `results/learned_vs_single_heldout.json`, `results/learned_model.json`, `results/heldout_predictions.parquet`, `results/dev_oof_predictions.parquet` | learned models (coefficients, L1 path, EBM importances/shapes) and predictions |
| `results/prereg_verdicts.json`, `results/prereg_b5_minus_reach.csv` | P1-P5 |
| `results/sensitivities_heldout.csv`, `results/sensitivities_pooled.json` | post-seal sensitivities |
| `results/rq1_dev_selection.json`, `results/dev_ranking.csv`, `results/dev_ranking_sensitivity.csv` | DEV ranking, frozen top 10s, union, placebo |
| `results/frozen_spec.json` (+ `logs/seal.log`, `logs/unsealed.json`, `logs/outcome_seal.log`) | the frozen specification and seal evidence |
| `results/indicator_matrix.parquet`, `results/indicator_dictionary.csv`, `results/indicator_corr_dev.csv`, `results/indicator_clusters_dev.json`, `results/size_diagnostic_dev.csv` | indicators and DEV diagnostics |
| `results/o2r_resid_fit.json`, `results/o5_join.json`, `results/outcome_base_rates.json`, `results/o4_reference_expectations.csv` | outcome construction |
| `results/power_dev.json`, `results/case_exemplars.json` | power / MDE; case exemplars with top W3 ego neighbours |
| `results/checks.json`, `results/unit_tests.json`, `results/t0_8_ego_port.json`, `results/t1_passA_exact_*.json`, `results/t4_ego_sanity.json`, `results/audit.json`, `results/rederive.json` | tests and audits |
| `results/deviations.json`, `results/provenance.json`, `results/features_config.json` | deviations, sha256 of copied inputs, ego settings |
| `figures/portability_heatmap`, `heldout_forest_<outcome>`, `learned_vs_single`, `ebm_shapes`, `indicator_clusters`, `o5_base_rates` | PNG + PDF |
| `method_out.json`, `full_/mini_/preview_method_out.json` | exp_gen_sol_out: one example per concept (12,499); `predict_{B5,best_single,linear_all,EBM}_<outcome>`; DEV rows out-of-fold |

### Deviations from the plan (all in `results/deviations.json`)

- Ego windows are 1 year each (planned); T4 median M = 3.5 (> 3), so the n >= 2 neighbour rule was kept. As a
  result D_z/D_ratio/D_sub are missing for 31% of DEV concepts (> 30% eligibility bound) and D_rare for 88%: the D
  family could not enter any frozen top 10 (it is in the portability table and P1).
- F4(ii): betweenness path cutoff 4 -> 3 (betweenness was 98% of ego time); N_NULL = 200 as planned.
- O2r_resid follows the plan (O2r_m50 on early logvol, DEV fit a = 2.741, b = 0.397). EXP5's constants belong to a
  different formula (O2r_m30 on log outcome volume); that definition is reported as sensitivity `O2r_resid_N`.
- O5 baselines add onset year as a linear term (dummies cannot transfer to the 2010-14 cohort).
- MATHDEC dropped for O3 (3 positives); bootstrap B as listed in deviations; the first `audit.py` version used a
  loose sklearn tolerance and a too-weak planted control (fixed; pipeline unchanged).
- Pass A took 62 min (a shared network cap of ~8 MB/s for part of the run); no fallback was needed. $0 OpenRouter,
  0 OpenAlex credits.
- Kept artifacts stay on the run's volume; `data/frame_matches_early/part_001.parquet` and `models/` are under
  100 MB and are published.


## How to run

```bash
./restore.sh                       # .venv from requirements.lock.txt
.venv/bin/python method.py         # resumes; skips steps whose outputs exist
```

The steps and their runtimes on this run (cpu_plus, 5 workers):

| step | runtime |
|---|---|
| Pass A (2,040 files) | 62 min (33 min at full bandwidth in EXP5) |
| Pass B | 24 min |
| family A ego features (12,499 concepts) | 36 min |
| DEV ranking + placebo + learned models + freeze | 29 min |
| held-out scoring, portability, P1-P5, sensitivities | 16 min |
| audit, outputs, re-derivation | 3 min |


The seal allows exactly one unseal per frozen spec. Re-running the confirmatory part from scratch needs a new
freeze, and that would no longer be a sealed test.

## Restoring removed files

These paths are marked `delete` in `.aii/manifest.yaml` and are removed after the round:

| deleted path | restore command |
|---|---|
| `.venv/` | `./restore.sh` (`uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r requirements.lock.txt`) |
| `__pycache__/`, `lib/__pycache__/` | created automatically by Python |

Everything else stays in place. The per-file scan parts (`passA/parts/`, `passB/parts/`) and ego chunks
(`data/ego_parts_c3/`) are small and kept on the run volume, but they are excluded from the published repository.
They can be regenerated with `./restore.sh --scans` (Pass A + Pass B, zero-credit public S3 reads) and
`./restore.sh --ego`. Their merged outputs (`data/frame_matches_early/`, `data/cites_early.parquet`,
`data/ego_features.parquet`) are kept and published.
