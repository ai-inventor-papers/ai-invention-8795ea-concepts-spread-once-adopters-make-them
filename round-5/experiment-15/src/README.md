# Why churning concepts spread: HOME partner classes, trait stability, and the completed Exp11 closure test

Cache-only, $0-LLM, 0-OpenAlex-credit experiment (AI Inventor iteration 5, `gen_plan_experiment_3_idx3`) on the run's
frozen OpenAlex-derived frames (EXP5 legacy-concept frame: 12,499 concepts; Exp10 fresh 2015-17 cohort: 1,443
concepts). It has three parts:

* **Part C (confirmatory reporting of a sealed test)**: finishes the sealed Exp11 within-concept test ("does home-only
  ego-network closure precede slower off-home spread?") from its cached panel with the sealed code. Exp11 finished DEV
  only; its event study crashed (an OpenBLAS thread explosion) and its held-out/cohort bodies never ran. The DEV verdict
  NOT SUPPORTED is copied, not re-decided.
* **Part A (EXPLORATORY; the outcomes are selection data)**: explains *why* the HOME novelty/churn signal
  (NOVCHURN_home = mean of z(NOV_res) and -z(edge_persistence)) predicts later off-home spread (O2r_m50). The HOME-only
  new, dropped and added partner sets are rebuilt with the exact EXP8 ego primitives (gate G2: reproduces Exp10 to 0.0
  on every concept). Every partner is classified on four axes (METHOD/DOMAIN type, new/same backbone community,
  low/high degree under the null, mixed/pure-home carrier papers). The three totals (NOV_res, new_edge_rate,
  churn = 1 - edge_persistence) are decomposed **exactly** into class parts, and each part is scored by partial Spearman
  given the B5 baseline, with Shapley attribution of the psp, a Holm family of 5 contrasts, and class-label placebos.
* **Part B (prediction hashed before computing)**: is HOME openness a stable concept trait? This covers the ICC
  (raw, size-adjusted, REML cross-check), yearly-window test-retest, reliability and a static 3-year retest.

The analysis spec, contrasts and predictions of Parts A/B were hash-sealed (`results/frozen_spec_iter5.json`,
`logs/seal_iter5.log`) together with the feature files **before** any outcome was joined. The outcomes had been
unsealed in earlier iterations, so that seal only controls this analysis's degrees of freedom. Part A is labelled
exploratory throughout.

## Main findings

**Part C: the sealed within-concept closure test stays NOT SUPPORTED, and no held-out body rescues it.**

* All gates pass. G0: 21/21 sealed hashes match. The panel rebuilt through the seal gate equals the cached one. G1: the
  DEV point estimates reproduce Exp11 to 0.0. All 8 Exp11 unit tests pass on the copied code.
* Body models (PPML, concept + year FE). OLD_HELDOUT: density +0.068 [-0.072, +0.209]; OPEN_home **-0.079
  [-0.146, -0.013]**, the *opposite* of the predicted sign. COHORT 2010-14: +0.003 and +0.029, both nulls. **H-M5 fails.**
  H-M3 (forward vs reverse) is null in all three bodies.
* Event study (Sun-Abraham, never-treated). DEV mean lag 0..2 = -0.018 [-0.042, +0.004], pre-trend p = 0.52. The
  pre-test is weak: Roth's 80%-power detectable slope is 0.022 per year, the size of the effect itself. The event-date
  placebo gives one-sided p = 0.19. OLD_HELDOUT (-0.005) and COHORT (-0.0005) are null, and the not-yet-treated controls
  agree. **H-M4 fails.** The mechanical check matters: home volume itself drops at the closure jump (-0.022, CI < 0,
  pre-trend p ~ 0). Closure jumps partly reflect year-to-year changes in how many home papers a concept has.
* Sequence (H-S1: intersection-born concepts take off without a prior home-prominence peak more often). This holds in
  DEV (+0.113 [+0.039, +0.172]), COHORT (+0.105 [+0.027, +0.161]) and pooled (+0.076 [+0.024, +0.126]). It fails in
  OLD_HELDOUT (+0.001 [-0.122, +0.113]). Only 40-52 multi-home take-off concepts per body, so this is weak and
  domain-dependent. Take-off *timing* does not differ (log-rank p > 0.7, Cox HR 0.84-0.92 with CIs spanning 1; Exp12's
  independent HR 0.47 is cited, not recomputed). Within-concept event studies (secondary, sealed): off-home entries
  *fall* after the home-prominence peak when all bodies are pooled (-0.030 [-0.047, -0.016], pre-trend p = 0.45; DEV
  alone -0.022 [-0.048, +0.004]), and home prominence falls after off-home take-off (ALL -0.93 percentile points
  [-1.54, -0.29]; DEV -1.08 [-2.13, -0.16]). A home-prominence peak marks the *end* of a concept's outward phase,
  not its launch pad.
* H-P1 as preregistered (ALL-papers partners): **fails.** The new-community half is strong (DL +0.216 [+0.081, +0.351]).
  The METHOD half is -0.055 [-0.122, +0.011].

**Part A (exploratory): the HOME signal is carried by partners from new communities that arrive through mixed-field
papers. It is not a METHOD effect, and it lives in each concept's partner *composition*.**

* NOVCHURN_home replicates in every body: POOLED_EXP5 +0.118 [+0.093, +0.143]; OLD_HELDOUT +0.103; DL over the four
  held-out groups +0.097 [+0.043, +0.151] (I2 = 0); 2015-17 cohort +0.171 (R0) and +0.144 (R3). It beats OPEN_home in
  every body except DEV.
* **Community (P-A2 holds).** New-community new partners carry the new_edge_rate signal (+0.085), same-community ones
  do not (-0.017): C2 = +0.102 [+0.069, +0.133], Holm p = 0.0025. The DL over held-out groups is +0.113, and the 2015-17
  cohort gives +0.18 / +0.14. In the type x community Shapley games, DOMAIN-new is the largest player for both
  new-edge rate and churn, and DOMAIN-old is negative in every body shown (POOLED, OLD_HELDOUT, 2015-17 R0/R3).
* **Carrier (P-A4 holds).** Partners carried by papers that also hold an off-home-field topic ("mixed") carry the
  signal (+0.091), pure-home ones do not (-0.012): C4 = +0.103, Holm p = 0.0025. The DL over held-out groups is +0.060
  [-0.003, +0.123], and the cohort gives +0.070 / +0.055. In the NOVCHURN Shapley game "mixed" contributes more than
  the whole psp in POOLED (phi 0.152 vs v 0.118) and OLD_HELDOUT (0.141 vs 0.103), and 0.80 of it in the 2015-17
  cohort at R0 (0.136 vs 0.171).
* **Composition, not partner identity.** C2 and C4 lie far outside the across-row label-permutation null (observed
  quantile 1.0). Count-based parts are invariant to within-concept shuffles by construction. The low-degree novelty
  contrast C3 (+0.081, Holm p = 0.0025, so P-A3 holds nominally) is *reproduced* by a within-concept shuffle (placebo
  mean +0.093, observed quantile 0.12). What predicts spread is how many of a concept's new partners are new-community,
  mixed-carried or peripheral, not which individual partners they are.
* **Degree.** Turnover among *high-degree* (hub) partners carries the churn signal (ch_deg_high +0.129), while churn
  among low-degree partners is negative (-0.081). The NOVCHURN degree game gives high phi +0.137 and low -0.020.
* **METHOD (P-A1 holds only on the pooled selection body).** On POOLED_EXP5 the METHOD Shapley share is 0.57 vs a 0.28
  share of new partners (excess CI [+0.12, +0.47]). This is DEV-driven (METHOD churn +0.084 in DEV, +0.025 in
  OLD_HELDOUT); in the 2015-17 cohort METHOD's share is 0.21 vs a fair 0.23. The class-null METHOD-DOMAIN novelty
  contrast C1 is -0.043 (Holm p = 0.105). This is a domain-specific (CS/Eng/Bio/Med) pattern, not a general mechanism.
* **Dropped vs added churn (P-A5 fails).** C5 = +0.010 [-0.033, +0.052], and both directions contribute similarly.
* **Bridging papers.** Early home papers that introduce a new-community partner (5% of early home papers) have more
  first-time authors on the concept (+5 pts), far more off-home topics (+25 pts) and slightly smaller teams; they are
  not reviews. bridging_share_home alone has psp +0.097, and controlling for it halves NOVCHURN's psp (0.118 -> 0.056).
* **Baseline vs method (prediction).** In 5-fold concept-CV ridge, adding NOVCHURN_home to B5 raises the out-of-fold
  Spearman by +0.0015 to +0.0040 in every body (CIs exclude 0 in DEV and OLD_HELDOUT; see the table). The signal is robust but small next to B5; the
  recognition outcome O5_WW is unrelated (NOVCHURN psp -0.018 [-0.047, +0.012]).

**Part B: HOME openness is a noisy yearly measurement of a moderately stable trait. The hashed prediction (ICC >= 0.40)
fails.**

* Yearly ICC of OPEN_home: 0.369 (DEV), 0.344 (OLD_HELDOUT), 0.390 (COHORT 2010-14). All are below the 0.40 floor, so
  **P-B1 is not supported as hashed.** NOVCHURN is less stable (0.26-0.29). The REML cross-check agrees (0.375 / 0.352
  / 0.388). Size adjustment barely moves OPEN_home (0.365 / 0.346), so the stability is not a size artefact. The
  positive control (log home volume) gives 0.64-0.73.
* The early-vs-later window retest *passes* the floor (OPEN_home rho 0.53 / 0.51 / 0.57; partial given size 0.54 /
  0.54 / 0.58). The deg >= 5 ICC is 0.50 / 0.50 / 0.55, the first-difference correlation is about -0.45 (close to the
  -0.5 pure-noise signature), and the disattenuated retest is 0.86-0.91. Openness looks like a fair trait measured
  through a noisy 1-year window. About 56% of the yearly variance is within-concept (within/total SD 0.75), which caps the
  power of the within-concept FE design (MDE of about 3.3% change in entries per within-SD on DEV).
* Static 3-year build, early (t0..t0+2) vs later (t0+3..t0+5): OPEN_home rho 0.33 (DEV) / 0.27 (OLD_HELDOUT).

## Results (every number is printed with the JSON key it comes from)

### Part C: completion of the sealed Exp11 within-concept closure test (reporting only)

- Seal verification (G0): `results/exp11_completion.json -> seal_verification` = 21/21 sealed hashes match, frozen spec ok = True
- Panel rebuilt through the seal gate equals the cached Exp11 panel: `panel_rebuild_equal_to_cache` = True; DEV reproduction gate G1 (1e-8): `G1_dev_reproduction` = True
- `dev_verdict`: **DEV verdict unchanged: NOT SUPPORTED**

| body | rows / concepts | H-M1 b(density) [CRV1 CI] | boot CI | H-M2 b(OPEN_home) [CRV1 CI] | boot CI | DL density (I2) | DL OPEN (I2) |
|---|---|---|---|---|---|---|---|
| DEV | 35328 / 4661 | -0.070 [-0.180, +0.040] | [-0.176, +0.039] | +0.015 [-0.038, +0.069] | [-0.037, +0.067] | -0.075 (0.25) | +0.012 (0.00) |
| OLD_HELDOUT | 20314 / 3225 | +0.068 [-0.072, +0.209] | [-0.070, +0.203] | -0.079 [-0.146, -0.013] | [-0.150, -0.022] | +0.060 (0.00) | -0.094 (0.37) |
| COHORT | 25925 / 4159 | +0.003 [-0.127, +0.133] | [-0.133, +0.139] | +0.029 [-0.063, +0.121] | [-0.059, +0.112] | +0.034 (0.42) | -0.008 (0.21) |

Keys: `results/exp11_completion.json -> body_models.<body>.*` (source `exp11_code/results/fe_results_completed.json -> <body>`).

- H-M5 (signs of H-M1 < 0 and H-M2 > 0 on OLD_HELDOUT and COHORT): `H_M5.holds_signs` = **False**
- H-M3 (|std fwd| - |std rev|, paired bootstrap): DEV +0.0027 [-0.0100, +0.0124]; OLD_HELDOUT -0.0043 [-0.0211, +0.0124]; COHORT -0.0042 [-0.0154, +0.0087] (`H_M3.<body>`)

| body | control | mean lag 0..2 | 95% CI | pre-trend Wald p | Roth 80% detectable slope | max abs lead | n treated | boots |
|---|---|---|---|---|---|---|---|---|
| DEV | primary_never | -0.0183 | [-0.0423, +0.0044] | 0.518 | 0.0221 | 0.0100 | 2754 | 1000 |
| DEV | not_yet_treated_last_cohort | -0.0039 | [-0.0312, +0.0215] | 0.321 | 0.0217 | 0.0138 | 2731 | 500 |
| DEV | outcome_entries_t | -0.0068 | [-0.0301, +0.0191] | 0.013 | 0.0226 | 0.0427 | 2754 | 300 |
| DEV | mechanical_home_volume | -0.0221 | [-0.0304, -0.0136] | 0.000 | 0.0088 | 0.0437 | 2754 | 300 |
| OLD_HELDOUT | primary_never | -0.0049 | [-0.0392, +0.0233] | 0.541 | 0.0291 | 0.0151 | 1425 | 300 |
| OLD_HELDOUT | not_yet_treated_last_cohort | -0.0216 | [-0.0711, +0.0250] | 0.720 | 0.0349 | 0.0133 | 1407 | 300 |
| COHORT | primary_never | -0.0005 | [-0.0301, +0.0296] | 0.183 | 0.0266 | 0.0316 | 1872 | 300 |
| COHORT | not_yet_treated_last_cohort | +0.0272 | [-0.0103, +0.0679] | 0.263 | 0.0314 | 0.0207 | 1788 | 300 |

Keys: `results/exp11_completion.json -> event_study.<body>.<control>.*`.
- DEV event-date permutation placebo: mean -0.0088, 2.5-97.5% [-0.0291, +0.0109], observed -0.0183, one-sided p = 0.186 (`event_study.DEV.placebo_event_date`, n = 1000)
- **H-M4** (`H_M4.holds`) = **False**: lag CI below 0 = False, pre-trend p = 0.518, leads small = False, placebo p = 0.186

| body | n multi / single (take-off) | share no prior peak multi | single | diff | 95% CI | holds |
|---|---|---|---|---|---|---|
| DEV | 52 / 1166 | 0.942 | 0.829 | +0.113 | [+0.039, +0.172] | True |
| OLD_HELDOUT | 40 / 934 | 0.825 | 0.824 | +0.001 | [-0.122, +0.113] | False |
| COHORT | 42 / 1075 | 0.952 | 0.847 | +0.105 | [+0.027, +0.161] | True |
| ALL | 134 / 3175 | 0.910 | 0.834 | +0.076 | [+0.024, +0.126] | True |

Keys: `results/exp11_completion.json -> H_S1.<body>` (Exp12 independent prior: HR 0.47, cited only).
- DEV: log-rank p = 0.816; Cox HR(multi-home) = 0.888 [+0.671, +1.175]
- OLD_HELDOUT: log-rank p = 0.823; Cox HR(multi-home) = 0.922 [+0.671, +1.266]
- COHORT: log-rank p = 0.761; Cox HR(multi-home) = 0.840 [+0.615, +1.146]
- ALL: log-rank p = 0.883; Cox HR(multi-home) = 0.886 [+0.745, +1.054]
- `sequence_event_studies.es_entries_around_peak_DEV`: mean lag 0..2 = -0.0219 [-0.0483, +0.0042], pre-trend p = 0.082, n treated = 2748
- `sequence_event_studies.es_prominence_around_takeoff_DEV`: mean lag 0..2 = -1.0761 [-2.1263, -0.1641], pre-trend p = 0.555, n treated = 1218
- `sequence_event_studies.es_entries_around_peak_ALL`: mean lag 0..2 = -0.0295 [-0.0468, -0.0164], pre-trend p = 0.453, n treated = 7672
- `sequence_event_studies.es_prominence_around_takeoff_ALL`: mean lag 0..2 = -0.9311 [-1.5356, -0.2881], pre-trend p = 0.665, n treated = 3307

- **H-P1 as preregistered** (ALL-papers static partner set, DL over the 4 held-out groups, O2r_m50): METHOD-DOMAIN -0.055 [-0.122, +0.011]; comm_new-comm_old +0.216 [+0.081, +0.351] (I2 0.70); holds = **False** (`results/exp11_completion.json -> H_P1`)
- Exp11 unit tests rerun on the copied code: 8/8 pass (`exp11_unit_tests_rerun`)

### Part A: which HOME partner classes carry the signal? (EXPLORATORY, selection data)

- Gates: G2 (home build == Exp10, all concepts, 1e-9) and identities: see `results/unit_tests_iter5.json`; Exp10 published cohort psp reproduced: NOV_res +0.1337 vs +0.1337, edge_persistence -0.1123 vs -0.1123 (`exp10_sanity_gate`)

psp with O2r_m50 given B5 (+ t0/group/body dummies; 2015-17 cohort: Exp10 rungs), 95% concept-bootstrap CI (2000 draws). Key: `results/partner_classes.json -> bodies.<body>|O2r_m50.components.<component>`.

| component | POOLED_EXP5 | DEV | OLD_HELDOUT | COHORT_2010_14 | COHORT_2015_17_R0 | COHORT_2015_17_R3 | DL 4 held-out groups (I2) |
|---|---|---|---|---|---|---|---|
| NOVCHURN_home | +0.118 [+0.093, +0.143] | +0.129 [+0.092, +0.166] | +0.103 [+0.047, +0.155] | +0.112 [+0.065, +0.159] | +0.171 [+0.080, +0.265] | +0.144 [+0.056, +0.238] | +0.097 [+0.043, +0.151] (0.00) |
| OPEN_home | +0.106 [+0.081, +0.129] | +0.139 [+0.103, +0.177] | +0.068 [+0.020, +0.116] | +0.091 [+0.045, +0.135] | +0.123 [+0.040, +0.207] | +0.080 [-0.002, +0.166] | +0.068 [+0.015, +0.122] (0.08) |
| NOV_res | +0.081 [+0.055, +0.106] | +0.091 [+0.053, +0.128] | +0.085 [+0.033, +0.135] | +0.061 [+0.015, +0.106] | +0.155 [+0.072, +0.238] | +0.123 [+0.040, +0.208] | +0.103 [+0.014, +0.190] (0.57) |
| churn | +0.080 [+0.055, +0.104] | +0.082 [+0.044, +0.116] | +0.075 [+0.028, +0.119] | +0.099 [+0.057, +0.141] | +0.103 [+0.016, +0.187] | +0.099 [+0.013, +0.191] | +0.073 [+0.025, +0.120] (0.00) |
| new_edge_rate | +0.051 [+0.028, +0.075] | +0.066 [+0.032, +0.101] | +0.048 [+0.003, +0.093] | +0.026 [-0.019, +0.068] | +0.029 [-0.048, +0.109] | +0.027 [-0.045, +0.107] | +0.054 [-0.043, +0.150] (0.73) |
| new_edge_rate_ALL | +0.106 [+0.082, +0.129] | +0.115 [+0.080, +0.149] | +0.113 [+0.065, +0.157] | +0.094 [+0.052, +0.137] | - | - | +0.118 [+0.071, +0.164] (0.00) |
| bridging_share_home | +0.097 [+0.074, +0.119] | +0.126 [+0.090, +0.161] | +0.080 [+0.035, +0.124] | +0.055 [+0.013, +0.096] | +0.115 [+0.041, +0.190] | +0.094 [+0.013, +0.172] | +0.115 [+0.003, +0.224] (0.79) |
| nov_type_METHOD | +0.012 [-0.014, +0.038] | +0.019 [-0.019, +0.057] | -0.006 [-0.060, +0.045] | +0.019 [-0.027, +0.066] | +0.022 [-0.065, +0.107] | +0.023 [-0.063, +0.106] | -0.021 [-0.074, +0.032] (0.00) |
| nov_type_DOMAIN | +0.082 [+0.056, +0.106] | +0.081 [+0.043, +0.118] | +0.093 [+0.040, +0.145] | +0.057 [+0.011, +0.104] | +0.155 [+0.065, +0.242] | +0.119 [+0.029, +0.210] | +0.130 [+0.012, +0.244] (0.76) |
| ch_type_METHOD | +0.052 [+0.028, +0.075] | +0.084 [+0.050, +0.120] | +0.025 [-0.023, +0.073] | +0.024 [-0.019, +0.065] | +0.026 [-0.051, +0.107] | +0.010 [-0.070, +0.088] | +0.010 [-0.038, +0.059] (0.00) |
| ch_type_DOMAIN | -0.001 [-0.024, +0.022] | -0.018 [-0.053, +0.015] | +0.008 [-0.042, +0.058] | +0.031 [-0.011, +0.072] | +0.016 [-0.064, +0.097] | +0.033 [-0.045, +0.118] | +0.011 [-0.050, +0.072] (0.29) |
| ner_comm_new | +0.085 [+0.061, +0.108] | +0.111 [+0.076, +0.146] | +0.068 [+0.025, +0.114] | +0.056 [+0.014, +0.097] | +0.107 [+0.030, +0.183] | +0.089 [+0.010, +0.167] | +0.099 [+0.004, +0.192] (0.71) |
| ner_comm_old | -0.017 [-0.041, +0.007] | -0.023 [-0.058, +0.011] | -0.019 [-0.067, +0.028] | -0.011 [-0.056, +0.029] | -0.070 [-0.151, +0.012] | -0.051 [-0.130, +0.034] | -0.029 [-0.075, +0.017] (0.00) |
| ner_carrier_mixed | +0.091 [+0.069, +0.114] | +0.126 [+0.093, +0.159] | +0.059 [+0.016, +0.106] | +0.071 [+0.028, +0.114] | +0.073 [-0.006, +0.147] | +0.064 [-0.010, +0.143] | +0.052 [-0.002, +0.105] (0.20) |
| ner_carrier_pure | -0.012 [-0.035, +0.012] | -0.007 [-0.042, +0.027] | -0.014 [-0.062, +0.032] | -0.024 [-0.068, +0.017] | +0.003 [-0.076, +0.084] | +0.009 [-0.069, +0.089] | -0.001 [-0.103, +0.102] (0.75) |
| nov_deg_low | +0.092 [+0.067, +0.116] | +0.094 [+0.057, +0.129] | +0.063 [+0.009, +0.113] | +0.118 [+0.070, +0.165] | +0.143 [+0.053, +0.232] | +0.130 [+0.042, +0.220] | +0.089 [+0.002, +0.175] (0.56) |
| nov_deg_high | +0.010 [-0.015, +0.036] | +0.011 [-0.028, +0.048] | +0.045 [-0.009, +0.096] | -0.026 [-0.073, +0.021] | +0.036 [-0.055, +0.127] | +0.008 [-0.081, +0.097] | +0.052 [-0.024, +0.127] (0.45) |
| ch_deg_low | -0.081 [-0.105, -0.057] | -0.087 [-0.120, -0.054] | -0.048 [-0.097, +0.002] | -0.111 [-0.155, -0.068] | -0.048 [-0.124, +0.029] | -0.040 [-0.117, +0.039] | -0.050 [-0.100, -0.000] (0.00) |
| ch_deg_high | +0.129 [+0.105, +0.153] | +0.136 [+0.101, +0.171] | +0.094 [+0.044, +0.145] | +0.164 [+0.123, +0.207] | +0.088 [+0.009, +0.163] | +0.068 [-0.009, +0.149] | +0.091 [+0.040, +0.140] (0.00) |
| chd_all | +0.038 [+0.014, +0.063] | +0.044 [+0.008, +0.075] | +0.036 [-0.015, +0.083] | +0.034 [-0.011, +0.078] | +0.037 [-0.044, +0.116] | +0.044 [-0.037, +0.120] | +0.036 [-0.018, +0.091] (0.15) |
| cha_all | +0.029 [+0.005, +0.053] | +0.029 [-0.006, +0.065] | +0.008 [-0.041, +0.058] | +0.049 [+0.005, +0.093] | +0.033 [-0.052, +0.116] | +0.021 [-0.062, +0.104] | +0.009 [-0.068, +0.086] (0.52) |

Holm family (POOLED_EXP5, O2r_m50; `holm_family_POOLED_EXP5_O2r_m50`), with the two placebo nulls (`placebo.<scheme>.<contrast>`):

| contrast | diff | 95% CI | p | Holm p | DL held-out groups | 2015-17 R0 / R3 diff | placebo across rows: mean (obs quantile) | placebo within concept: mean (obs quantile) |
|---|---|---|---|---|---|---|---|---|
| C1_METHOD_minus_DOMAIN_novnull | -0.043 | [-0.089, +0.000] | 0.0525 | 0.1050 | -0.109 [-0.234, +0.015] | -0.100 / -0.097 | -0.005 (0.02) | -0.019 (0.10) |
| C2_commnew_minus_commold_ner | +0.102 | [+0.069, +0.133] | 0.0005 | 0.0025 | +0.113 [+0.033, +0.193] | +0.177 / +0.141 | -0.006 (1.00) | degenerate: count part invariant (sd 0) |
| C3_lowdeg_minus_highdeg_nov | +0.081 | [+0.045, +0.119] | 0.0005 | 0.0025 | +0.037 [-0.084, +0.158] | +0.107 / +0.122 | +0.003 (1.00) | +0.093 (0.12) |
| C4_mixed_minus_pure_ner | +0.103 | [+0.071, +0.134] | 0.0005 | 0.0025 | +0.060 [-0.003, +0.123] | +0.070 / +0.055 | -0.002 (1.00) | degenerate: count part invariant (sd 0) |
| C5_dropped_minus_added_churn | +0.010 | [-0.033, +0.052] | 0.6565 | 0.6565 | +0.025 [-0.100, +0.150] | +0.004 / +0.023 | -0.003 (0.72) | +0.017 (0.10) |

Bootstrap p values have a floor of 1/2000 (Holm floor 0.0025). The within-concept placebo keeps each concept's class counts, so count-based parts (C2, C4) cannot move under it; the across-rows placebo is their null.

Shapley decomposition of the psp (O2r_m50). phi in psp units; share = phi / (v(full) - v(empty)); fair = the class's share of new partners (NOVCHURN games) or of the part's mass. Key: `results/partner_shapley.json -> games.<body>|O2r_m50.shapley.<game>`.

| body | game | v(full)-v(empty) | player: phi [CI] (share / fair) |
|---|---|---|---|
| POOLED_EXP5 | NOVCHURN_type | +0.118 | METHOD: +0.067 [+0.046, +0.086] (0.57 / 0.28); DOMAIN: +0.051 [+0.026, +0.078] (0.43 / 0.72) |
| POOLED_EXP5 | NOVCHURN_deg | +0.118 | low: -0.020 [-0.043, +0.003] (-0.17 / 0.54); high: +0.137 [+0.113, +0.161] (1.17 / 0.46) |
| POOLED_EXP5 | NOVCHURN_carrier | +0.118 | mixed: +0.152 [+0.128, +0.175] (1.29 / 0.46); pure: -0.034 [-0.059, -0.008] (-0.29 / 0.54) |
| POOLED_EXP5 | NOVCHURN_direction | +0.118 | NOV: +0.054 [+0.032, +0.075] (0.46); DROP: +0.028 [+0.009, +0.048] (0.24 / 0.51); ADD: +0.036 [+0.016, +0.056] (0.30 / 0.49) |
| POOLED_EXP5 | ner_type_x_comm | +0.052 | METHOD_new: +0.027 [+0.014, +0.039] (0.51 / 0.12); METHOD_old: +0.008 [-0.006, +0.022] (0.16 / 0.16); DOMAIN_new: +0.053 [+0.036, +0.070] (1.01 / 0.30); DOMAIN_old: -0.035 [-0.054, -0.016] (-0.68 / 0.41) |
| POOLED_EXP5 | churn_type_x_comm | +0.091 | METHOD_new: +0.050 [+0.033, +0.066] (0.54 / 0.11); METHOD_old: +0.017 [-0.002, +0.035] (0.18 / 0.17); DOMAIN_new: +0.095 [+0.072, +0.119] (1.04 / 0.26); DOMAIN_old: -0.070 [-0.096, -0.045] (-0.77 / 0.45) |
| OLD_HELDOUT | NOVCHURN_type | +0.103 | METHOD: +0.040 [-0.002, +0.080] (0.38 / 0.24); DOMAIN: +0.064 [+0.007, +0.120] (0.62 / 0.76) |
| OLD_HELDOUT | NOVCHURN_deg | +0.103 | low: -0.004 [-0.055, +0.044] (-0.04 / 0.58); high: +0.107 [+0.057, +0.156] (1.04 / 0.42) |
| OLD_HELDOUT | NOVCHURN_carrier | +0.103 | mixed: +0.141 [+0.090, +0.191] (1.36 / 0.53); pure: -0.037 [-0.089, +0.013] (-0.36 / 0.47) |
| OLD_HELDOUT | NOVCHURN_direction | +0.103 | NOV: +0.057 [+0.010, +0.104] (0.56); DROP: +0.025 [-0.018, +0.066] (0.24 / 0.52); ADD: +0.021 [-0.023, +0.065] (0.20 / 0.48) |
| OLD_HELDOUT | ner_type_x_comm | +0.026 (F5: small v) | METHOD_new: +0.014 [-0.010, +0.036]; METHOD_old: +0.016 [-0.008, +0.043]; DOMAIN_new: +0.045 [+0.011, +0.079]; DOMAIN_old: -0.049 [-0.093, -0.006] |
| OLD_HELDOUT | churn_type_x_comm | +0.048 | METHOD_new: +0.034 [-0.000, +0.066] (0.70 / 0.08); METHOD_old: -0.006 [-0.044, +0.029] (-0.12 / 0.15); DOMAIN_new: +0.073 [+0.025, +0.124] (1.52 / 0.26); DOMAIN_old: -0.053 [-0.110, +0.007] (-1.10 / 0.51) |
| COHORT_2015_17_R0 | NOVCHURN_type | +0.171 | METHOD: +0.036 [-0.034, +0.111] (0.21 / 0.23); DOMAIN: +0.135 [+0.039, +0.228] (0.79 / 0.77) |
| COHORT_2015_17_R0 | NOVCHURN_deg | +0.171 | low: +0.054 [-0.031, +0.141] (0.32 / 0.59); high: +0.116 [+0.033, +0.201] (0.68 / 0.41) |
| COHORT_2015_17_R0 | NOVCHURN_carrier | +0.171 | mixed: +0.136 [+0.054, +0.221] (0.80 / 0.46); pure: +0.035 [-0.052, +0.121] (0.20 / 0.54) |
| COHORT_2015_17_R0 | NOVCHURN_direction | +0.171 | NOV: +0.114 [+0.043, +0.183] (0.66); DROP: +0.051 [-0.019, +0.118] (0.30 / 0.54); ADD: +0.006 [-0.066, +0.081] (0.04 / 0.46) |
| COHORT_2015_17_R0 | ner_type_x_comm | -0.005 (F5: small v) | METHOD_new: +0.032 [-0.006, +0.072]; METHOD_old: +0.007 [-0.038, +0.050]; DOMAIN_new: +0.055 [-0.005, +0.114]; DOMAIN_old: -0.098 [-0.171, -0.023] |
| COHORT_2015_17_R0 | churn_type_x_comm | +0.071 | METHOD_new: +0.027 [-0.025, +0.081] (0.38 / 0.09); METHOD_old: +0.018 [-0.046, +0.084] (0.26 / 0.14); DOMAIN_new: +0.129 [+0.041, +0.215] (1.81 / 0.28); DOMAIN_old: -0.103 [-0.196, -0.012] (-1.45 / 0.48) |
| COHORT_2015_17_R3 | NOVCHURN_type | +0.144 | METHOD: +0.012 [-0.064, +0.087] (0.08 / 0.23); DOMAIN: +0.132 [+0.041, +0.230] (0.92 / 0.77) |
| COHORT_2015_17_R3 | NOVCHURN_deg | +0.144 | low: +0.049 [-0.035, +0.141] (0.34 / 0.59); high: +0.095 [+0.009, +0.175] (0.66 / 0.41) |
| COHORT_2015_17_R3 | NOVCHURN_carrier | +0.144 | mixed: +0.091 [+0.011, +0.181] (0.63 / 0.46); pure: +0.053 [-0.033, +0.144] (0.37 / 0.54) |
| COHORT_2015_17_R3 | NOVCHURN_direction | +0.144 | NOV: +0.088 [+0.015, +0.161] (0.61); DROP: +0.053 [-0.020, +0.119] (0.37 / 0.54); ADD: +0.004 [-0.067, +0.079] (0.03 / 0.46) |
| COHORT_2015_17_R3 | ner_type_x_comm | -0.014 (F5: small v) | METHOD_new: +0.026 [-0.014, +0.066]; METHOD_old: +0.002 [-0.040, +0.048]; DOMAIN_new: +0.037 [-0.024, +0.099]; DOMAIN_old: -0.080 [-0.157, -0.002] |
| COHORT_2015_17_R3 | churn_type_x_comm | +0.081 | METHOD_new: +0.020 [-0.030, +0.069] (0.25 / 0.09); METHOD_old: +0.014 [-0.047, +0.077] (0.17 / 0.14); DOMAIN_new: +0.111 [+0.023, +0.190] (1.37 / 0.28); DOMAIN_old: -0.064 [-0.157, +0.038] (-0.79 / 0.48) |

Predictions (`predictions`):

- P-A1: METHOD_shapley_share=+0.567, METHOD_share_ci=[+0.402, +0.752], METHOD_new_partner_share=+0.279, excess=+0.287, excess_ci=[+0.123, +0.473], holds_point=True, holds_ci=True
- P-A2: contrast=C2_commnew_minus_commold_ner, diff=+0.102, ci=[+0.069, +0.133], p_holm=+0.003, holds_point=True, holds_holm=True
- P-A3: contrast=C3_lowdeg_minus_highdeg_nov, diff=+0.081, ci=[+0.045, +0.119], p_holm=+0.003, holds_point=True, holds_holm=True
- P-A4: contrast=C4_mixed_minus_pure_ner, diff=+0.103, ci=[+0.071, +0.134], p_holm=+0.003, holds_point=True, holds_holm=True
- P-A5: contrast=C5_dropped_minus_added_churn, diff=+0.010, ci=[-0.033, +0.052], p_holm=+0.656, holds_point=True, holds_holm=False

Bridging papers (`results/bridging_papers_summary.json`):

- exp5: 24377 bridging of 462675 early home papers; team_size: bridging 3.652 vs other 3.797, diff CI [-0.331, -0.006]; share_new_authors: bridging 0.870 vs other 0.822, diff CI [+0.042, +0.054]; has_offhome_topic: bridging 0.597 vs other 0.348, diff CI [+0.237, +0.260]; n_topics: bridging 2.822 vs other 2.739, diff CI [+0.068, +0.098]; is_review: bridging 0.004 vs other 0.005, diff CI [-0.002, +0.000]
- cohort_2015_17: 3043 bridging of 56402 early home papers; team_size: bridging 4.171 vs other 4.951, diff CI [-1.694, -0.163]; share_new_authors: bridging 0.953 vs other 0.902, diff CI [+0.041, +0.061]; has_offhome_topic: bridging 0.562 vs other 0.360, diff CI [+0.173, +0.234]; n_topics: bridging 2.831 vs other 2.782, diff CI [+0.024, +0.074]
- POOLED_EXP5: psp(bridging_share_home|B5) = +0.097 [+0.075, +0.120]; psp(NOVCHURN_home|B5) = +0.118 [+0.092, +0.142]; psp(NOVCHURN_home|B5+bridging_share_home) = +0.056 [+0.029, +0.082]
- OLD_HELDOUT: psp(bridging_share_home|B5) = +0.080 [+0.034, +0.126]; psp(NOVCHURN_home|B5) = +0.103 [+0.048, +0.153]; psp(NOVCHURN_home|B5+bridging_share_home) = +0.051 [-0.003, +0.102]

### Part B: is HOME openness a stable concept trait? (prediction hashed before computing)

| body | variable | ICC raw [CI] | ICC size-adj | ICC deg>=5 | MixedLM REML ICC | retest rho [CI] | partial retest | disattenuated | lag-1 AC (FD corr) | within/total SD |
|---|---|---|---|---|---|---|---|---|---|---|
| DEV | OPEN_home | 0.369 [+0.354, +0.384] | 0.365 | 0.500 | 0.375 | 0.526 [+0.500, +0.552] | 0.535 | 0.859 | -0.020 (-0.448) | 0.75 |
| DEV | NOVCHURN | 0.255 [+0.238, +0.272] | 0.178 | 0.241 | 0.259 | 0.403 [+0.328, +0.470] | 0.273 | 0.891 | -0.152 (-0.469) | 0.73 |
| DEV | log1p_home_works | 0.707 [+0.694, +0.719] | 0.203 | 0.747 | NA | 0.740 [+0.720, +0.758] | 0.002 | 0.854 | +0.402 (-0.341) | 0.54 |
| OLD_HELDOUT | OPEN_home | 0.344 [+0.329, +0.361] | 0.346 | 0.495 | 0.352 | 0.510 [+0.464, +0.548] | 0.537 | 0.889 | -0.050 (-0.445) | 0.75 |
| OLD_HELDOUT | NOVCHURN | 0.272 [+0.246, +0.295] | 0.205 | 0.259 | 0.272 | 0.418 [+0.299, +0.533] | 0.370 | 0.904 | -0.205 (-0.436) | 0.68 |
| OLD_HELDOUT | log1p_home_works | 0.637 [+0.619, +0.657] | -0.016 | 0.705 | NA | 0.658 [+0.623, +0.688] | NA | 0.804 | +0.231 (-0.421) | 0.58 |
| COHORT_2010_14 | OPEN_home | 0.390 [+0.360, +0.414] | 0.363 | 0.549 | 0.388 | 0.575 [+0.544, +0.603] | 0.583 | 0.914 | -0.083 (-0.483) | 0.72 |
| COHORT_2010_14 | NOVCHURN | 0.285 [+0.264, +0.307] | 0.210 | 0.285 | 0.291 | 0.280 [+0.174, +0.371] | 0.230 | 0.570 | -0.193 (-0.476) | 0.69 |
| COHORT_2010_14 | log1p_home_works | 0.727 [+0.713, +0.738] | 0.258 | 0.773 | NA | 0.755 [+0.735, +0.776] | NA | 0.863 | +0.408 (-0.312) | 0.50 |

Key: `results/trait_stability.json -> bodies.<body>.<variable>.*`. Static 3-year build early vs later (`static_retest`): DEV OPEN 0.335 / NOVCHURN 0.333; OLD_HELDOUT OPEN 0.268 / NOVCHURN 0.293; COHORT_2010_14 OPEN 0.347 / NOVCHURN 0.357

- **P-B1 (OPEN_home) TRAIT_SUPPORTED = False**; P-B2 (NOVCHURN) = False; positive control ICC(log1p home works) = DEV 0.707, OLD_HELDOUT 0.637, COHORT_2010_14 0.727 (`verdict`)
- FE power link (DEV): within-concept SD of yearly OPEN_home = 0.422; the H-M2 PPML MDE is 3.3% change in off-home entries per within-SD (`bodies.DEV.fe_power_link`)

### Baseline vs method: 5-fold concept-CV ridge within body (`method_out.json -> metadata.cv_metrics`)

| body | n | B5 Spearman | +NOVCHURN | +partner classes | +OPEN_home | gain NOVCHURN [CI] |
|---|---|---|---|---|---|---|
| COHORT_2010_14 | 2182 | 0.7642 | 0.7657 | 0.7673 | 0.7656 | +0.0015 [-0.0007, +0.0038] |
| DEV | 3188 | 0.7608 | 0.7637 | 0.7660 | 0.7661 | +0.0028 [+0.0010, +0.0047] |
| OLD_HELDOUT | 1833 | 0.7057 | 0.7097 | 0.7090 | 0.7066 | +0.0040 [+0.0013, +0.0067] |
| COHORT_2015_17 | 634 | 0.7849 | 0.7877 | 0.7837 | 0.7857 | +0.0028 [-0.0022, +0.0080] |


## Layout

| path | what |
|---|---|
| `method.py` | pipeline entry point: runs every stage (skips finished ones) and assembles `results/exp11_completion.json` + `method_out.json` |
| `setup_exp11.py` | STEP 0: copies the sealed Exp11 code into `exp11_code/` with a path-only patch (`exp11_code/patch_diff.txt`, asserted path-only) and verifies the Exp11 seal (G0) -> `results/seal_verification.json` |
| `exp11_code/` | the sealed Exp11 code (verbatim except paths) + iter-5 runners: `run_completion.py` (body models, G1, robustness, OOF predictions), `run_event_study.py` (timing gate, per-cell checkpoint, placebo, figures), `run_partners.py` (H-P1 as preregistered), `sequence.py` (sealed, run as is); outputs in `exp11_code/results/`, `exp11_code/data/`, `exp11_code/figures/` |
| `partners_home.py` | STEP 6: HOME partner build + exact class decomposition + bridging papers + later-window (t0+3..t0+5) static retest build |
| `seal_iter5.py` | STEP 5: freezes the Part A/B spec and seals it with the feature hashes; `check()` gates every outcome join |
| `score_partA.py` | STEP 7: class psp per body, DL over held-out groups, Shapley games, Holm family, placebos, bridging, figures |
| `trait_stability.py` | STEP 8: ICC / test-retest / reliability / static retest (Part B) |
| `lib_iter5/` | `common_iter5.py` (paths), `ego.py` (Exp10 lib/ego.py verbatim), `ladder.py` (Exp10 verbatim), `partA_stats.py` (vectorised psp == EXP8 psp_point, Shapley, DL), `s7_ego_exp10_copy.py` (reference copy of the Exp10 HOME build) |
| `tests/test_iter5.py` | T0 tests: G2 reproduction, identities, Shapley, planted signal, ICC recovery, degree cut, psp equivalence -> `results/unit_tests_iter5.json` |
| `make_readme.py`, `README_narrative.md` | build this README (tables generated from the JSON files) |
| `results/` | `exp11_completion.json`, `partner_classes.json`, `partner_shapley.json`, `bridging_papers_summary.json`, `trait_stability.json`, `frozen_spec_iter5.json`, `seal_verification.json`, `unit_tests_iter5.json`, `deviations.json` |
| `data/` | `partner_home_components_{exp5,cohort,retest}.parquet` (sealed features), `partner_home_rows_{exp5,cohort}/` (one row per new/dropped/added partner with class labels and exact weights), `bridging_home_papers_*.parquet`, `partA_features_*.parquet` (features joined to outcomes) |
| `figures/` | `partner_forest.png`, `shapley_bars.png`, `trait_scatter.png` (+ pdf); event-study figures in `exp11_code/figures/` |
| `method_out.json` (+ `full_`/`mini_`/`preview_`) | exp_gen_sol_out: one example per concept (output O2r_m50; predictions of the B5 baseline vs B5 + NOVCHURN / partner classes / OPEN_home, 5-fold concept CV) and a sample of the Exp11 OOF panel predictions |
| `logs/` | every run's log, `seal_iter5.log`, attach log of the Exp11 seal gate (`exp11_code/logs/attach.log`) |

## How to run

```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r requirements.lock.txt
source env.sh                     # one BLAS thread per process (the Exp11 crash fix) + AII_RUN_ROOT
.venv/bin/python method.py --workers 4           # all stages (about 3 h on 4 CPUs: event study ~1 h, sequence ~1 h), skips finished ones
.venv/bin/python method.py --stages assemble     # only rebuild exp11_completion.json + method_out.json
.venv/bin/python tests/test_iter5.py             # T0 tests
.venv/bin/python make_readme.py                  # regenerate the README tables
```

Inputs are read, read-only, from earlier artifacts of the same run, addressed relative to the run root
(`$AII_RUN_ROOT`, default: four directories above this workspace):
`3_invention_loop/iter_4/gen_art/gen_art_experiment_11` (sealed code, cached panel, partner caches, topic types),
`.../round-4/experiment-10/src` (HOME build reproduction targets, 2015-17 cohort, frozen OPEN constants),
`.../round-3/experiment-8/src` (EXP5 early matches, outcomes, B5),
`.../round-2/experiment-5/src` (frame), and `.../round-2/dataset-2/src` (O5 recognition data,
used only through the O5_WW column of the EXP8 analysis table, as a secondary outcome).

## Deviations from the plan

**iter-5 Parts A/B (`results/deviations.json`)**

- `bridging_cohort_doc_type`: 2015-17 cohort bridging profile has no is_review: passC_early lacks doc_type
- `partA_exploratory`: Part A uses previously unsealed outcomes (EXP5 DEV/OLD_HELDOUT/COHORT_2010_14 and the 2015-17 cohort). The seal (results/frozen_spec_iter5.json, logs/seal_iter5.log) fixes only this analysis's degrees of freedom; every Part A number is EXPLORATORY.
- `placebo_schemes`: Plan: shuffle class labels WITHIN concept (200 draws). A within-concept shuffle leaves every count-based part (ner_X, churn_X) invariant, so its null for C2/C4 is degenerate (equals the observed value). Both schemes are reported: within_concept (meaningful for the novelty contrasts C1/C3 and the drop/add contrast C5) and across_rows (labels permuted across all partner rows of POOLED_EXP5, the informative null for count-based parts).
- `icc_estimator`: Plan: statsmodels MixedLM REML ICC with a 500-draw concept bootstrap. 500 MixedLM refits x 3 bodies x 3 variables x 2 versions is infeasible on 4 CPUs; the primary ICC is the one-way ANOVA ICC(1) (unbalanced k0) on year+age-residualised values with a 500-draw concept bootstrap (100 for per-group cells), and the MixedLM REML ICC is reported as a point cross-check (unit test T0(e) shows the ANOVA estimator recovers ICC 0.5 within 0.005 on the real unbalanced structure).
- `shapley_value_convention`: v(S) neutralises the parts of players not in S by their body mean (fixed on the observed sample, not re-estimated per bootstrap draw); v(empty) = 0 when the rebuilt score is constant. For the type x community games a non-player remainder (partners with unknown community / OTHER type) stays in every coalition, so v(empty) != 0 and efficiency is sum(phi) = v(full) - v(empty); both are reported.
- `novchurn_min_home`: NOVCHURN_home uses the Exp10 OPEN_home rule n_home_early >= 10 (as OPEN_home) and requires both NOV_res and edge_persistence finite.
- `code_changes_after_seal`: After the iter-5 seal, code-only fixes were made (no spec or feature change): score_partA.run_task guards the chd/cha difference for the reduced O5_WW column set, and the Shapley figure's axis label was corrected; partA_stats._psp_block returns NaN for constant columns (lstsq round-off on constant ranks produced |psp| ~1e-4 for v(empty)); trait_stability fits the MixedLM cross-check on FE-residualised values with bfgs (see mixedlm_on_residuals). All scoring runs used the fixed code. Final hashes vs the hashes at the seal: results/code_sha256_final.json.
- `exp11_unit_tests_t3`: Exp11 unit test t3 failed on the first rerun only because networkx (used by h2_exp6) and the root-level build_d3.py were missing from the iter-5 copy; after adding both (networkx==3.7 as pinned by Exp11; build_d3.py copied verbatim) t3 passes and all 8 Exp11 unit tests pass.
- `sequence_workers`: sequence.py (sealed) run with --boot 300 --workers 3 (Exp11 default 20 workers; 4-CPU container shared with the event study).
- `mixedlm_on_residuals`: The MixedLM REML cross-check is fitted as x_res ~ 1 with a random concept intercept on values already residualised on year and age dummies by OLS: the full dummy design gave a singular Hessian (LinAlgError) and lbfgs stopped at the tau2 = 0 boundary; bfgs/powell/nm/cg agree to 1e-4 (DEV OPEN_home 0.375 vs ANOVA 0.369).
- `event_study_workers`: run_event_study.py run with 3 workers (timing gate: 2.5 s per DEV fit, projected 60 min < 100 min budget, so no subsample and all planned draw counts were kept: DEV 1000 never-treated / 500 not-yet-treated / 300 entries_t / 300 home volume, 300 per cell elsewhere, 1000 permutations).

**iter-5 Part C runners (`exp11_code/results/deviations.json`)**

- `es_draws`: event-study draws per cell after the timing gate: {'DEV|primary_never': 1000, 'DEV|not_yet_treated_last_cohort': 500, 'DEV|outcome_entries_t': 300, 'DEV|mechanical_home_volume': 300, 'OLD_HELDOUT|primary_never': 300, 'OLD_HELDOUT|not_yet_treated_last_cohort': 300, 'COHORT|primary_never': 300, 'COHORT|not_yet_treated_last_cohort': 300}, perm 1000

Exp11's own sealed deviations (500 body-model boots and 300 event-study boots outside DEV, saturated Sun-Abraham design, etc.) are in the Exp11 artifact's `results/deviations.json` and apply unchanged.

## Kept artifacts

Everything in this directory is small (< 15 MB per file); nothing is marked `keep` beyond the default. All results,
data and figures stay at their relative paths on the run's volume and are also published with the repository.

## Restoring removed files

`.aii/manifest.yaml` marks only regenerable caches for deletion:

* `.venv/`: `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r requirements.lock.txt`
* `__pycache__/`, `lib_iter5/__pycache__/`, `exp11_code/__pycache__/`, `exp11_code/lib/__pycache__/`: Python bytecode, rebuilt automatically on the next import (`.venv/bin/python method.py --stages assemble`).
