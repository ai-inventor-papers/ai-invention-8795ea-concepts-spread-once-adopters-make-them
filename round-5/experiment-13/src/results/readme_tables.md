### Ladder: partial Spearman with later breadth (95% concept-bootstrap CI, B = 2000)

| index | outcome | R0 | R1 | R2 | R3 | R4 | R5 | n (R3) |
|---|---|---|---|---|---|---|---|---|
| OPEN_home | O2r_m30 | +0.157 [+0.063, +0.253] | +0.127 [+0.026, +0.229] | +0.126 [+0.024, +0.227] | +0.117 [+0.020, +0.218] | +0.107 [+0.011, +0.211] | +0.086 [-0.009, +0.190] | 448 |
| OPEN_home | O2r_m50 | +0.193 [+0.092, +0.290] | +0.162 [+0.066, +0.262] | +0.164 [+0.068, +0.264] | +0.161 [+0.064, +0.263] | +0.145 [+0.043, +0.248] | +0.122 [+0.027, +0.230] | 397 |
| OPEN_home | O2r_resid | +0.197 [+0.096, +0.296] | +0.167 [+0.072, +0.266] | +0.169 [+0.072, +0.268] | +0.166 [+0.069, +0.269] | +0.151 [+0.050, +0.253] | +0.128 [+0.034, +0.238] | 397 |
| NOVCHURN_home | O2r_m30 | +0.106 [+0.004, +0.207] | +0.110 [+0.009, +0.212] | +0.109 [+0.005, +0.212] | +0.108 [+0.007, +0.211] | +0.069 [-0.037, +0.171] | +0.036 [-0.074, +0.141] | 435 |
| NOVCHURN_home | O2r_m50 | +0.137 [+0.031, +0.244] | +0.153 [+0.049, +0.264] | +0.154 [+0.050, +0.265] | +0.154 [+0.047, +0.266] | +0.102 [-0.003, +0.215] | +0.066 [-0.041, +0.183] | 385 |
| NOVCHURN_home | O2r_resid | +0.141 [+0.037, +0.245] | +0.157 [+0.054, +0.265] | +0.157 [+0.052, +0.265] | +0.157 [+0.051, +0.270] | +0.108 [+0.005, +0.220] | +0.073 [-0.035, +0.188] | 385 |
| OPEN_sizematch | O2r_m30 | +0.144 [+0.051, +0.239] | +0.100 [+0.009, +0.197] | +0.100 [+0.008, +0.196] | +0.085 [-0.006, +0.184] | +0.082 [-0.013, +0.181] | +0.066 [-0.028, +0.166] | 456 |
| OPEN_sizematch | O2r_m50 | +0.197 [+0.100, +0.294] | +0.152 [+0.055, +0.251] | +0.150 [+0.052, +0.251] | +0.137 [+0.038, +0.242] | +0.129 [+0.028, +0.232] | +0.109 [+0.008, +0.215] | 404 |
| OPEN_sizematch | O2r_resid | +0.198 [+0.101, +0.294] | +0.154 [+0.057, +0.254] | +0.153 [+0.056, +0.256] | +0.139 [+0.040, +0.243] | +0.132 [+0.031, +0.235] | +0.112 [+0.013, +0.217] | 404 |
| OPEN_all | O2r_m30 | +0.243 [+0.150, +0.333] | +0.197 [+0.100, +0.289] | +0.195 [+0.099, +0.287] | +0.185 [+0.087, +0.276] | +0.177 [+0.082, +0.267] | +0.149 [+0.055, +0.242] | 465 |
| OPEN_all | O2r_m50 | +0.268 [+0.166, +0.359] | +0.223 [+0.122, +0.317] | +0.223 [+0.122, +0.319] | +0.214 [+0.113, +0.311] | +0.201 [+0.100, +0.300] | +0.171 [+0.069, +0.275] | 409 |
| OPEN_all | O2r_resid | +0.269 [+0.165, +0.360] | +0.224 [+0.120, +0.320] | +0.224 [+0.119, +0.320] | +0.215 [+0.112, +0.314] | +0.202 [+0.094, +0.303] | +0.174 [+0.069, +0.279] | 409 |

### Holm family (one-sided bootstrap p in the frozen direction)

| member | p (one-sided) | Holm p |
|---|---|---|
| OPEN_home|O2r_m30|R3 | 0.0105 | 0.0525 |
| OPEN_home|O2r_m30|R5 | 0.0375 | 0.1124 |
| NOVCHURN_home|O2r_m30|R3 | 0.0215 | 0.0860 |
| CHENG_consistency_home|O2r_m30|R0 (<0) | 0.0985 | 0.1889 |
| OPEN_all-OPEN_home|O2r_m30|R3 paired | 0.0945 | 0.1889 |

### Per group at R3 (O2r_m30) with DerSimonian-Laird pooling (groups estimable at n >= 30)

| index | CS+Eng | BGM+Med | PHYS | LIFEENV | SOC | MATHDEC | DL pooled [95% CI] | I2 | positive / estimable | leave-one-group-out DL |
|---|---|---|---|---|---|---|---|---|---|---|
| OPEN_home | +0.167 (n=134) | +0.097 (n=189) | +0.060 (n=51) | NA (n=15) | -0.025 (n=52) | NA (n=7) | +0.112 [-0.015, +0.239] | 0.00 | 3/4 | -CS+Eng: +0.083, -BGM+Med: +0.130, -PHYS: +0.115, -SOC: +0.121 |
| NOVCHURN_home | +0.130 (n=127) | +0.064 (n=188) | +0.169 (n=50) | NA (n=14) | +0.087 (n=50) | NA (n=6) | +0.090 [-0.032, +0.213] | 0.00 | 4/4 | -CS+Eng: +0.074, -BGM+Med: +0.131, -PHYS: +0.086, -SOC: +0.091 |
| OPEN_sizematch | +0.060 (n=133) | +0.117 (n=189) | +0.064 (n=53) | NA (n=16) | -0.050 (n=57) | NA (n=8) | +0.082 [-0.045, +0.208] | 0.00 | 3/4 | -CS+Eng: +0.095, -BGM+Med: +0.046, -PHYS: +0.083, -SOC: +0.091 |
| OPEN_all | +0.196 (n=137) | +0.177 (n=191) | +0.162 (n=53) | NA (n=16) | +0.052 (n=60) | NA (n=8) | +0.176 [+0.059, +0.292] | 0.00 | 4/4 | -CS+Eng: +0.165, -BGM+Med: +0.175, -PHYS: +0.177, -SOC: +0.183 |

### The six OPEN components alone (O2r_m30)

| component (OPEN sign) | HOME R2 | HOME R3 | ALL R2 | ALL R3 |
|---|---|---|---|---|
| new_edge_rate (+) | +0.048 [-0.046, +0.137] | +0.035 [-0.052, +0.122] | +0.163 [+0.076, +0.257] | +0.158 [+0.074, +0.251] |
| n_comm_W3 (+) | +0.073 [-0.025, +0.165] | +0.069 [-0.030, +0.166] | +0.149 [+0.059, +0.240] | +0.145 [+0.057, +0.239] |
| participation (+) | +0.124 [+0.015, +0.224] | +0.120 [+0.011, +0.223] | +0.146 [+0.055, +0.238] | +0.145 [+0.052, +0.236] |
| NOV_res (+) | +0.214 [+0.120, +0.307] | +0.208 [+0.113, +0.303] | +0.194 [+0.105, +0.283] | +0.181 [+0.095, +0.272] |
| ego_density_W3 (-) | -0.080 [-0.187, +0.022] | -0.078 [-0.182, +0.025] | -0.060 [-0.156, +0.041] | -0.053 [-0.151, +0.047] |
| edge_persistence (-) | -0.009 [-0.112, +0.089] | -0.013 [-0.113, +0.083] | -0.068 [-0.161, +0.020] | -0.061 [-0.156, +0.026] |

### Coupling contrasts (paired concept bootstrap, R3)

| contrast | estimate [95% CI] | n |
|---|---|---|
| all_minus_home | +0.056 [-0.024, +0.131] | 448 |
| sizematch_minus_home | -0.031 [-0.090, +0.029] | 447 |
| OPEN_all on the OPEN_home sample (psp) | +0.174 [+0.079, +0.261] | 448 |

### Cheng et al. (2023) measures (home papers, OpenAlex topics as terms)

| measure | V_next raw Spearman | V_next given log N(t0+2) | V_next given R0 | O2r_m30 given R0 | O2r_resid given R0 | O1b given R0 | O1c given R0 | O3 given R0 |
|---|---|---|---|---|---|---|---|---|
| CHENG_consistency_home | +0.418 [+0.345, +0.484] | +0.094 [+0.007, +0.186] | +0.121 [+0.039, +0.201] | -0.064 [-0.159, +0.031] | -0.090 [-0.186, +0.015] | -0.087 [-0.169, -0.004] | +0.051 [-0.028, +0.128] | -0.012 [-0.085, +0.059] |
| CHENG_consistency_all | +0.547 [+0.490, +0.608] | +0.162 [+0.071, +0.252] | +0.172 [+0.078, +0.253] | -0.083 [-0.174, +0.008] | -0.078 [-0.176, +0.019] | -0.104 [-0.183, -0.026] | +0.091 [+0.011, +0.172] | -0.003 [-0.070, +0.068] |
| CHENG_embeddedness_home | -0.113 [-0.196, -0.029] | +0.085 [+0.000, +0.160] | +0.068 [-0.022, +0.149] | -0.250 [-0.328, -0.164] | -0.330 [-0.413, -0.245] | -0.008 [-0.086, +0.078] | +0.064 [-0.019, +0.148] | -0.015 [-0.095, +0.065] |
| CHENG_prominence_home | +0.018 [-0.061, +0.098] | -0.018 [-0.096, +0.064] | -0.024 [-0.101, +0.060] | +0.034 [-0.053, +0.116] | +0.058 [-0.037, +0.147] | +0.079 [-0.008, +0.159] | +0.017 [-0.061, +0.096] | -0.100 [-0.168, -0.024] |

Spearman(CHENG_consistency_home, edge_persistence_home) = +0.791 [+0.753, +0.826] (n = 580); Spearman(CHENG_consistency_home, logvol) = +0.421 [+0.348, +0.486].

### Clean variants and secondary indicators (O2r_m30)

| indicator | rung | psp [95% CI] | n |
|---|---|---|---|
| ego_density_W3_cz | R3 | -0.072 [-0.175, +0.040] | 396 |
| edge_persistence_sz | R3 | -0.031 [-0.134, +0.065] | 404 |
| NOVCHURN_home_rare | R3 | +0.150 [+0.030, +0.285] | 294 |
| edge_persistence_excess | R3 | +0.043 [-0.050, +0.130] | 449 |
| NOVCHURN_clean | R3 | +0.121 [+0.019, +0.225] | 396 |
| CONTACT_REACH | R0 | +0.296 [+0.203, +0.381] | 465 |
| RETENTION_RATIO_early | R0 | -0.138 [-0.238, -0.038] | 465 |
| n_authors_early | R3 | -0.030 [-0.109, +0.062] | 465 |
| n_comm_W3__home | R3 | +0.069 [-0.027, +0.166] | 465 |
| NOVCHURN_home -> O3 | R3 | -0.011 [-0.100, +0.079] | 563 |
| OPEN_home -> O3 | R3 | +0.006 [-0.086, +0.093] | 578 |
| NOVCHURN_home -> O1b | R3 | -0.011 [-0.092, +0.079] | 563 |
| OPEN_home -> O1b | R3 | -0.010 [-0.092, +0.075] | 578 |
| NOVCHURN_home -> O1c | R3 | -0.089 [-0.165, -0.001] | 563 |
| OPEN_home -> O1c | R3 | -0.006 [-0.088, +0.074] | 578 |

### Palla et al. (2007) size x turnover interaction (R3 covariates)

| outcome | model | coefficient of z(logvol) x z(edge_persistence_home) [95% CI] | n |
|---|---|---|---|
| O2r_m30 | OLS on rank(y)/n | -0.006 [-0.030, +0.016] | 449 |
| O3 | logit | +0.033 [-0.458, +0.481] | 580 |
| O1b | logit | +0.098 [-0.131, +0.335] | 580 |
| O3 (psp of edge_persistence_home at R3) | partial Spearman | +0.049 [-0.047, +0.137] | 580 |

### Within concept type (R3 without type dummies; M1 = M2 labels only)

| index | method | object |
|---|---|---|
| OPEN_home | +0.225 [+0.011, +0.421] n=130 | +0.189 [-0.011, +0.393] n=138 |
| NOVCHURN_home | +0.033 [-0.185, +0.231] n=127 | +0.183 [-0.010, +0.400] n=134 |
| OPEN_sizematch | +0.207 [-0.020, +0.391] n=130 | +0.165 [-0.028, +0.353] n=141 |
| OPEN_all | +0.165 [-0.035, +0.350] n=130 | +0.245 [+0.063, +0.422] n=143 |

### Forecasting (5-fold CV, folds stratified by group; n = 435; outcome O2r_m30)

| model | Spearman | AUC top tercile | delta Spearman vs B5 [95% CI] | delta AUC vs B5 [95% CI] |
|---|---|---|---|---|
| B5 | 0.800 | 0.892 | - | - |
| B5_plus_OPEN_home | 0.804 | 0.896 | +0.0036 [-0.0029, +0.0104] | +0.0041 [-0.0005, +0.0092] |
| B5_plus_NOVCHURN_home | 0.803 | 0.897 | +0.0028 [-0.0046, +0.0103] | +0.0048 [-0.0002, +0.0099] |
| frozen EXP5 OLS: B5 vs B5 + OPEN_home (no refit) | 0.804 -> 0.809 | - | +0.0047 [-0.0012, +0.0112] | - |

### Placebo and planted effect (OPEN_home, R3)

* within-group shuffle of OPEN_home, 200 draws: mean psp +0.018, 95th percentile of |psp| = 0.095 (observed +0.117).
* planted psp 0.10 on within-group-permuted outcomes, 100 draws x 400 bootstraps: mean estimate +0.063, recovery rate (CI_low > 0) 0.24.

### Survivorship: Frame N vs legacy (curated-vocabulary) newborns, t0 2003-2014

| measure | Frame N | legacy raw | legacy reweighted to Frame N (t0 x logvol decile) | relative difference [95% CI] | flag > 25% |
|---|---|---|---|---|---|
| O2r_m50_vs_legacy_O2r_m50 | 4.282 | 4.919 | 4.977 | -14.0% [-17.8%, -10.3%] |  |
| O2r_m50_vs_legacy_O2r_m50_MATCH | 4.282 | 5.504 | 5.437 | -21.2% [-24.6%, -17.5%] |  |
| O3_vs_legacy_O3 | 0.083 | 0.038 | 0.044 | +88.9% [+29.3%, +177.0%] | FLAG |
| O1b_vs_legacy_O1b | 0.407 | 0.544 | 0.551 | -26.1% [-34.0%, -18.2%] | FLAG |

### EXPLORATORY (post-unseal; not part of the verdict)

| subset | index | outcome | R3 | R5 | n |
|---|---|---|---|---|---|
| strict_gate_M2_also_keeps | OPEN_home | O2r_m30 | +0.137 [+0.040, +0.245] | +0.106 [+0.004, +0.217] | 368 |
| strict_gate_M2_also_keeps | OPEN_home | O2r_m50 | +0.160 [+0.050, +0.272] | +0.125 [+0.012, +0.244] | 333 |
| strict_gate_M2_also_keeps | NOVCHURN_home | O2r_m30 | +0.104 [-0.008, +0.215] | +0.040 [-0.074, +0.162] | 360 |
| strict_gate_M2_also_keeps | NOVCHURN_home | O2r_m50 | +0.147 [+0.031, +0.268] | +0.074 [-0.048, +0.199] | 326 |
| main_frame_only_t0_le_2014 | OPEN_home | O2r_m30 | +0.101 [-0.000, +0.209] | +0.067 [-0.035, +0.175] | 400 |
| main_frame_only_t0_le_2014 | OPEN_home | O2r_m50 | +0.152 [+0.049, +0.265] | +0.112 [+0.011, +0.229] | 352 |
| main_frame_only_t0_le_2014 | NOVCHURN_home | O2r_m30 | +0.107 [-0.001, +0.212] | +0.040 [-0.069, +0.155] | 389 |
| main_frame_only_t0_le_2014 | NOVCHURN_home | O2r_m50 | +0.143 [+0.022, +0.263] | +0.073 [-0.047, +0.197] | 342 |
| min_home_20 | OPEN_home | O2r_m30 | +0.120 [+0.026, +0.222] | +0.089 [-0.008, +0.196] | 435 |
| min_home_20 | NOVCHURN_home | O2r_m30 | +0.091 [-0.011, +0.193] | +0.029 [-0.082, +0.141] | 423 |

Inverse-variance pooling with the independent EXP10 legacy cohort (OPEN_home; EXP10 used O2r_m50 and its legacy rungs):

| rung | Frame N | EXP10 cohort | pooled fixed-effect [95% CI] |
|---|---|---|---|
| R2 | +0.126 | +0.091 | +0.105 [+0.043, +0.166] |
| R3 | +0.117 | +0.080 | +0.096 [+0.034, +0.158] |
| R5 | +0.086 | +0.056 | +0.068 [+0.006, +0.129] |
