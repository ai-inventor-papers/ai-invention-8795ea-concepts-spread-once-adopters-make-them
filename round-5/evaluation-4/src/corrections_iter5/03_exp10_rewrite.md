# 03 Experiment 10 rewrite (25.1, 25.2, 25.4, 25.7, new 25.8, 31.1)

### 25.1 Design

[Correction, iteration 5, from art_NMe386dX9GLF] The OPEN index is the mean of six signed z-scored ego-network components from the early window (t0 to t0+2): new_edge_rate (+), n_comm_W3 (+), participation (+), NOV_res (+), ego_density_W3 (−), edge_persistence (−), with winsor bounds and z constants frozen on the 12,499 EXP5 concepts. Three builds: OPEN_home (home-field papers only), OPEN_all (all papers; **mechanically coupled** to spread, because its off-home papers are part of what later counts as breadth) and OPEN_sizematch (a size-matched subsample of all papers). The confirmatory cohort has onsets in **2015-2017**: 570 (2015), 500 (2016) and 373 (2017, the declared power extension), 1,443 concepts in total, of which 634 have a defined O2r_m50. None of them was used in any earlier screen.

Pre-seal power for OPEN_home at R2 was 0.16 (true effect = half the EXP5 estimate), and the minimum detectable effect (2.8 SE) was 0.105.

Source: `round-4/experiment-10/src/results/cohort_result.json` -> `n_by_t0`, `n_cohort`, `outcome_availability`; `results/frozen_spec.json` -> `power.with_2017`.

### 25.2 Control ladder

[Correction, iteration 5, from art_NMe386dX9GLF] Partial Spearman (psp) of each build with rarefied breadth (O2r_m50) and residualised breadth (O2r_resid), concept bootstrap B = 2,000. R0 = B5 + onset year; R1 = + CONTACT_REACH; R2 = + concept type, generic flag and legacy level; R3 = + footprint; R4 = + label and home-paper coverage; R5 = + home-group FE.

| build | outcome | R0 | R1 | R2 | R3 | R4 | R5 | n |
|---|---|---|---|---|---|---|---|---|
| OPEN_home | O2r_m50 | +0.123 [+0.041, +0.205] | +0.097 [+0.018, +0.179] | +0.091 [+0.013, +0.171] | +0.080 [+0.001, +0.162] | +0.069 [-0.012, +0.150] | +0.056 [-0.022, +0.135] | 573 |
| OPEN_home | O2r_resid | +0.116 [+0.034, +0.201] | +0.092 [+0.013, +0.176] | +0.085 [+0.007, +0.165] | +0.080 [-0.000, +0.162] | +0.069 [-0.012, +0.151] | +0.056 [-0.024, +0.136] | 573 |
| OPEN_all | O2r_m50 | +0.205 [+0.125, +0.281] | +0.180 [+0.100, +0.259] | +0.174 [+0.092, +0.253] | +0.171 [+0.088, +0.251] | +0.147 [+0.064, +0.224] | +0.138 [+0.055, +0.218] | 630 |
| OPEN_all | O2r_resid | +0.194 [+0.113, +0.271] | +0.170 [+0.090, +0.250] | +0.163 [+0.082, +0.242] | +0.168 [+0.086, +0.247] | +0.144 [+0.061, +0.222] | +0.136 [+0.055, +0.216] | 630 |
| OPEN_sizematch | O2r_m50 | +0.183 [+0.103, +0.257] | +0.154 [+0.074, +0.230] | +0.147 [+0.068, +0.221] | +0.137 [+0.057, +0.212] | +0.124 [+0.045, +0.202] | +0.113 [+0.035, +0.190] | 591 |
| OPEN_sizematch | O2r_resid | +0.176 [+0.094, +0.250] | +0.148 [+0.068, +0.223] | +0.142 [+0.063, +0.217] | +0.137 [+0.057, +0.211] | +0.124 [+0.045, +0.201] | +0.114 [+0.037, +0.192] | 591 |

OPEN_home at R2 (the registered primary) is +0.091 [+0.013, +0.171], Holm p = 0.048. **Its R4 and R5 intervals include 0**, and so does its DerSimonian-Laird pool over groups at R2, +0.083 [-0.007, +0.173] (Section 25.3). OPEN_all and OPEN_sizematch stay above 0 on every rung, but OPEN_all is mechanically coupled (Section 25.4).

Source: `cohort_result.json` -> `primary['<build>|<outcome>|R0..R5'].{rho,ci,n}`, `groups['OPEN_home|O2r_m50|R2'].DL`, `holm`.

### 25.4 Mechanical coupling: ALL minus HOME

[Correction, iteration 5, from art_NMe386dX9GLF] OPEN_all is **mechanically coupled** to the outcome: its ego network includes the off-home papers that later make up breadth. The paired concept-bootstrap differences at R3 are: ALL − HOME +0.093 [+0.016, +0.169] (n = 571); SIZEMATCH − HOME +0.053 [-0.015, +0.117] (n = 563). The first says the all-papers build carries more signal than the home build; the second (CI includes 0) says a size-matched all-papers build does not beat the home build by a detectable margin. The home-only signal is carried by NOV_res +0.134 [+0.049, +0.215] and low edge persistence -0.112 [-0.199, -0.023] (Section 25.8).

Source: `cohort_result.json` -> `contrasts`, `components`.

### 25.7 Verdict

[Correction, iteration 5, from art_NMe386dX9GLF] The pre-registered verdict rule returns **CONFIRMED** (all five clauses pass, `cohort_result.json -> verdict`). Read with its limits, the evidence is weaker than that word:
- OPEN_home is +0.091 [+0.013, +0.171] at R2 but its R4 +0.069 [-0.012, +0.150] and R5 +0.056 [-0.022, +0.135] intervals include 0, as does the group-level DL pool +0.083 [-0.007, +0.173].
- **No forecasting gain**: the frozen B5 model gives Spearman +0.768 and B5 + OPEN_home +0.770, a difference of +0.002 [-0.003, +0.008] (n = 573).
- The planted control (true psp 0.10) was **not recovered** by the pipeline draw: +0.047 [-0.045, +0.132]; the independent audit draw gave +0.150 [+0.065, +0.226]. With power 0.16 and MDE 0.105, a single cohort of this size cannot confirm or refute an effect near 0.09 reliably.
- OPEN_all and OPEN_sizematch are larger but are labelled **mechanically coupled** / partly coupled (Section 25.4). Evaluation 3's specification curve (Section 27.2) used the all-papers build and is relabelled **exploratory, all-papers build**.

**Reading:** a small home-only partial association, positive on the confirmatory cohort at the registered rung, fragile under coverage and group controls, and with no out-of-sample forecasting gain.

Source: `cohort_result.json` -> `verdict`, `primary`, `groups`, `secondary.frozen_prediction_O2r_m50`, `placebos`; `cohort_report.json` -> `audits.post_unseal_audit.A5_planted`; `frozen_spec.json` -> `power`.

### 25.8 Components, within type, sensitivities and placebos (cohort)

[Correction, iteration 5, from art_NMe386dX9GLF] Re-keyed to `cohort_result.json` (cohort) and `exp5_selection_result.json` (EXP5 selection data), replacing the copies in the Exp10 README.

| component (sign) | HOME cohort | HOME EXP5 | ALL cohort | ALL EXP5 |
|---|---|---|---|---|
| new_edge_rate | +0.014 [-0.062, +0.090] | +0.039 [+0.014, +0.062] | +0.075 [-0.003, +0.152] | +0.084 [+0.062, +0.109] |
| n_comm_W3 | +0.002 [-0.071, +0.081] | -0.001 [-0.025, +0.022] | +0.161 [+0.082, +0.238] | +0.133 [+0.110, +0.154] |
| participation | +0.050 [-0.041, +0.133] | +0.043 [+0.020, +0.071] | +0.145 [+0.068, +0.224] | +0.117 [+0.095, +0.142] |
| NOV_res | +0.134 [+0.049, +0.215] | +0.057 [+0.033, +0.081] | +0.145 [+0.064, +0.221] | +0.087 [+0.064, +0.113] |
| ego_density_W3 | +0.018 [-0.075, +0.113] | -0.009 [-0.042, +0.020] | -0.078 [-0.162, -0.002] | -0.070 [-0.091, -0.043] |
| edge_persistence | -0.112 [-0.199, -0.023] | -0.088 [-0.109, -0.066] | -0.029 [-0.110, +0.047] | -0.041 [-0.065, -0.018] |

Within concept type (R3 without type dummies):

| build | method | object | property | topic |
|---|---|---|---|---|
| OPEN_home | +0.074 [-0.212, +0.314] n=81 | +0.093 [-0.025, +0.204] n=250 | +0.119 [-0.159, +0.370] n=78 | -0.073 [-0.279, +0.135] n=115 |
| OPEN_all | +0.112 [-0.141, +0.352] n=90 | +0.200 [+0.069, +0.319] n=265 | +0.113 [-0.113, +0.343] n=89 | +0.111 [-0.083, +0.305] n=132 |
| OPEN_sizematch | +0.200 [-0.056, +0.423] n=85 | +0.148 [+0.029, +0.268] n=253 | +0.150 [-0.127, +0.400] n=85 | +0.025 [-0.203, +0.236] n=118 |

Declared sensitivities (R2):

| analysis | estimate [95% CI] | n |
|---|---|---|
| OPEN_all_on_home_sample|O2r_m50|R2 | +0.176 [+0.091, +0.263] | 571 |
| OPEN_home|O2r_m50_le2022_TAG|2015onsets|R2 | +0.055 [-0.070, +0.193] | 221 |
| OPEN_home|O2r_m50_TAG|R2 | +0.091 [+0.016, +0.171] | 573 |
| OPEN_home|O2r_m50_MATCH|R2 | +0.122 [+0.058, +0.189] | 927 |
| OPEN_all|O2r_m50_le2022_TAG|2015onsets|R2 | +0.180 [+0.045, +0.311] | 245 |
| OPEN_all|O2r_m50_TAG|R2 | +0.174 [+0.092, +0.256] | 630 |
| OPEN_all|O2r_m50_MATCH|R2 | +0.206 [+0.147, +0.266] | 1073 |
| OPEN_sizematch|O2r_m50_le2022_TAG|2015onsets|R2 | +0.115 [-0.020, +0.248] | 232 |
| OPEN_sizematch|O2r_m50_TAG|R2 | +0.147 [+0.070, +0.220] | 591 |
| OPEN_sizematch|O2r_m50_MATCH|R2 | +0.181 [+0.123, +0.235] | 955 |
| OPEN_home_min5|O2r_m50|R2 | +0.091 [+0.016, +0.171] | 573 |
| OPEN_home_min20|O2r_m50|R2 | +0.083 [+0.002, +0.167] | 528 |
| OPEN_home|O2r_m50|R2|2015_2016_only | +0.130 [+0.037, +0.220] | 414 |

Placebos: within-group outcome permutations (200 draws): 95th percentile of |psp| = +0.081, against the observed +0.091. Planted psp = 0.10: +0.047 [-0.045, +0.132], not recovered; independent audit draw +0.150, recovered.

Source: `cohort_result.json` -> `components`, `within_type`, `sensitivity`, `placebos`; `exp5_selection_result.json` -> `components`.

## 31.1 prefix

1. **A small home-only openness association on a confirmatory cohort (fragile).** [Correction, iteration 5, from art_NMe386dX9GLF] On 2015-2017 onset concepts never screened before, OPEN_home has psp +0.091 [+0.013, +0.171] at R2 (Holm p = 0.048), but R4, R5 and the group DL pool +0.083 [-0.007, +0.173] include 0, and adding it to B5 changes forecast Spearman by +0.002 [-0.003, +0.008]. OPEN_all is larger but mechanically coupled to the outcome. The previous wording of this finding follows, superseded: 
