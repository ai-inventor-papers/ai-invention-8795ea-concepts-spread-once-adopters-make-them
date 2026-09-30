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

<!-- TABLES -->

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

DEVIATIONS_PLACEHOLDER

## Kept artifacts

Everything in this directory is small (< 15 MB per file); nothing is marked `keep` beyond the default. All results,
data and figures stay at their relative paths on the run's volume and are also published with the repository.

## Restoring removed files

`.aii/manifest.yaml` marks only regenerable caches for deletion:

* `.venv/`: `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r requirements.lock.txt`
* `__pycache__/`, `lib_iter5/__pycache__/`, `exp11_code/__pycache__/`, `exp11_code/lib/__pycache__/`: Python bytecode, rebuilt automatically on the next import (`.venv/bin/python method.py --stages assemble`).
