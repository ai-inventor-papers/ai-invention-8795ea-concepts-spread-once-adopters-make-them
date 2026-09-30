# Is neighbourhood churn real or thin-sample noise?

A $0-LLM, cache-only confound check of the home-only "churn / novelty" signal found by earlier experiments. On the 2015-17 cohort that signal was NOV_res +0.134 and edge_persistence −0.112 (partial Spearman with O2r_m50 at rung R2, EXP10). This artifact asks two things: is the signal real, or a by-product of few papers per year? And is it an artefact of degree dependence?

It recomputes the raw home-build indicators exactly, then builds noise-controlled versions:
- **V1**: fixed-n rarefaction.
- **V2**: a within-concept year-label permutation null, plus a Chao-corrected Jaccard (**V2b**).
- **V3**: degree-preserving configuration nulls: backbone rewiring, a k-matched random-set null, and curveball-randomised persistence.
- **V4**: split-half reliability of every variant.

All variants are compared side by side on the same concepts, with the EXP10 covariate ladder, per body and pooled.

**Label: selection data, outcomes previously unsealed.** Every body's outcomes were already unsealed by EXP5/EXP8/EXP10. The seal (`logs/seal.log`) is a pre-analysis commitment, not a blind. These results are robustness evidence, not confirmation.

## Headline

**Mechanical verdict: `PARTLY_THIN`** (`results/clean_vs_raw_psp.json` → `verdict`). The flag `DEGREE_ARTEFACT_PERSISTENCE` is false.

Partial Spearman with O2r_m50 given B5 + rung R2, 95% concept-bootstrap CI (B = 2000). Source: `results/clean_vs_raw_psp.json → headline_R2_O2r_m50`. "ret" is the retention ratio clean/raw on the same concepts, from the paired bootstrap.

| variant | COH1517 | OLDHO | POOLED (n) | pooled ret |
|---|---|---|---|---|
| NOVCHURN_raw (EXP10 z's) | +0.161 [0.07, 0.25] | +0.113 [0.06, 0.16] | +0.116 [0.09, 0.14] (6450) | – |
| NOVCHURN_exc (V2 excess) | +0.063 [−0.02, 0.15] | +0.006 [−0.05, 0.06] | +0.008 [−0.02, 0.03] | 0.06 |
| NOVCHURN_rare10 (V1, n = 10/yr) | +0.176 [0.05, 0.29] | +0.044 [−0.07, 0.15] | +0.078 [0.04, 0.11] (2874) | 0.68 |
| NOVCHURN_cfg (V3c curveball z) | +0.088 [−0.02, 0.20] | +0.071 [−0.01, 0.15] | +0.106 [0.07, 0.14] | 1.00 |
| NOVCHURN_chao (V2b) | +0.153 [0.07, 0.24] | +0.123 [0.07, 0.18] | +0.108 [0.08, 0.13] | 0.91 |
| edge_persistence raw | −0.112 [−0.20, −0.02] | −0.086 [−0.13, −0.04] | −0.088 [−0.11, −0.07] | – |
| edge_persistence V2 **null mean** | −0.123 | −0.116 | **−0.120** [−0.14, −0.10] | – |
| edge_persistence_exc (V2) | +0.001 | −0.006 | −0.003 [−0.03, 0.02] | 0.04 |
| edge_persistence_rare10 | −0.058 | −0.037 | −0.030 [−0.06, 0.00] | 0.45 |
| z_pers_cfg (V3c) | −0.066 | −0.122 | −0.116 [−0.15, −0.09] | 1.00 |
| NOV_res raw | +0.134 | +0.093 | +0.073 | – |
| NOV_res_exc (V2) | +0.071 | +0.002 | +0.003 | 0.04 |
| NOV_res_rare10 | +0.205 | +0.065 | +0.093 | 1.01 |
| ego_density_W3 raw | +0.018 | +0.006 | −0.013 [−0.04, 0.01] | – |
| z_dens_cfg (V3a) | −0.047 | −0.089 | **−0.091** [−0.12, −0.06] | same-sample diff −0.079 [−0.11, −0.04] |
| OPEN_home | +0.091 | +0.070 | +0.085 | – |
| OPEN_home_clean (V3 subs) | +0.129 | +0.094 | **+0.115** [0.09, 0.14] | 1.24 [1.11, 1.43] |

### Reading
1. **Raw persistence is mostly a sample-size artefact.**
   - Raw edge persistence has Spearman +0.72 with log n_home_early (`results/size_dependence.json → spearman.edge_persistence__raw.POOLED`).
   - Its bin means rise 0.00 → 0.09 → 0.27 → 0.38 over n bins 10-19 / 20-49 / 50-99 / ≥100. The V2 null mean (same papers, years shuffled) tracks it almost exactly: 0.00 / 0.10 / 0.28 / 0.39 (`binned_persistence`).
   - The "thin-sample share" (R² of raw persistence on its own V2 null mean) is **0.66** (`thin_sample_share.POOLED.R2`).
   - At fixed n = 10 papers per year, persistence is nearly flat (0.11 → 0.15). See `figures/persistence_vs_n.png`.
2. **The churn → outcome association is not temporal churn.**
   - The excess over the within-concept permutation null carries nothing: NOVCHURN_exc pooled +0.008, retention 0.06. P1 fails: retention is 0.40 in COH1517 and 0.05 in OLDHO.
   - The V2 null mean itself predicts the outcome as strongly as raw persistence (−0.120 vs −0.088).
   - So what predicts disciplinary breadth is a static property of the concept's pooled home topic mix at its sample size: how redundant or concentrated its partner topics are. It is not the year-to-year turnover of partners.
3. **The association is also not "just paper count".**
   - Fixed-n rarefaction keeps 68% pooled; 76% in COH1517 and 64% in OLDHO (`verdict.clauses.V1_retention`).
   - The Chao-corrected and degree-normalised composites keep 91-100%.
   - NOV_res survives rarefaction fully (retention 1.01) and is nearly size-free (ρ with log n +0.05).
   - DL over the 5 pooled groups at R2: NOVCHURN_raw +0.110 [0.085, 0.136], I² = 0, positive in 5/5 groups; NOVCHURN_rare10 +0.081 [0.042, 0.119], 5/5 (`groups`).
4. **The V2 excess cannot adjudicate on its own.**
   - Split-half reliability of every V2-excess variant is ≈ 0: NOVCHURN_exc SB = 0.014, edge_persistence_exc 0.046, NOV_res_exc 0.020 (`results/reliability.json → variants.*.pooled.SB`).
   - The planted-churn check PC2 fails: V2 absorbs about 80% of a planted 50% W3 topic replacement (`results/planted_checks.json`).
   - So a null V2 result means "temporal order is unmeasurable at ~10 papers per year", not "no churn".
5. **Degree normalisation helps OPEN.**
   - Replacing raw density and persistence by their configuration z's raises OPEN_home pooled from +0.092 to +0.115 on the same sample. The difference is +0.022 [0.011, 0.034] at R2 and +0.023 [0.011, 0.034] at R3.
   - Raw ego density was null because of its degree dependence (ρ with log degree −0.38). Its degree-normalised version z_dens_cfg is −0.091 pooled: neighbourhoods *less* interlinked than their partners' degrees imply go with broader later uptake.
   - P2 holds: z_pers_cfg is −0.116 [−0.145, −0.086].
   - The curveball z does **not** remove size dependence (ρ with log n +0.63), because its null expected Jaccard is ≈ 0 and z ≈ obs/sd.

**Recommended wording for the paper.** Rename "churn" to *topical non-redundancy / dispersion of the home neighbourhood*. It is robust to fixed-n rarefaction and to undersampling correction. It is not evidence of year-to-year partner turnover.

### Predictions (frozen in `results/frozen_spec.json`; evaluated in `clean_vs_raw_psp.json → predictions`)
- **P1 fails.** The same-sample ratio psp(NOVCHURN_exc)/psp(NOVCHURN_raw) at R2 is 0.40 [−0.27, 0.88] in COH1517 (n 490) and 0.05 [−0.56, 0.44] in OLDHO (n 1321).
- **P2 holds.** z_pers_cfg pooled is −0.116 [−0.145, −0.086] (n 4262).
- **P3 holds.** Spearman(NOVCHURN_exc, log n) = +0.034 [0.015, 0.054] (n 9945).
- **Holm (reported only):** p = 0.41 / 0.0005 / 0.002, Holm-adjusted 0.41 / 0.0015 / 0.004.
- **F6 contingency:** COH1517 has 235 concepts with finite NOVCHURN_rare10 and outcome (≥ 150), so n = 10 stays primary.

### Reliability and disattenuation (`results/reliability.json`)
Pooled Spearman-Brown split-half reliability:

| variant | SB | variant | SB |
|---|---|---|---|
| NOV_res | 0.48 | V2 null mean of persistence | 0.71 |
| edge_persistence | 0.57 | z_pers_cfg | 0.71 |
| ego_density_W3 | 0.41 | z_dens_cfg | 0.70 |
| NOVCHURN_raw | 0.48 | z_dens_k | 0.66 |
| OPEN_home | 0.49 | NOVCHURN_cfg | 0.62 |
| NOVCHURN_rare5 | 0.36 | OPEN_home_clean | 0.58 |

- Reliability rises with n: NOVCHURN_raw is 0.39 at 10-19 papers and 0.67 at ≥ 100.
- The outcome O2r_m50 has SB = **0.895** (conservative, from m = 25 halves). It was recomputed from the cached outcome-window field counts exactly (max diff 1.8e-15).
- **Disattenuated pooled NOVCHURN_raw** (approximate for a partial Spearman): 0.178 [0.141, 0.214] at R2 and 0.157 at R3. OPEN_home at R3 is 0.102 (`clean_vs_raw_psp.json → disattenuated`).

### Power for Frame N (`results/power_frame_n.json`)
Joint power is for the Frame-N CONFIRMED rule: OPEN_home R3 & R5 & NOVCHURN_raw R3 all significant.

| target | n = 800 | n = 1500 | n = 2500 |
|---|---|---|---|
| S_A, T1 (disattenuated) | 0.26 | 0.50 | 0.71 |
| S_A, T2 (COH1517 raw) | 0.31 | 0.57 | 0.75 |
| S_A, T3 (half of pooled raw) | 0.07 | 0.11 | 0.26 |
| S_B (pessimistic n-mix), T3 | 0.03 | – | 0.06 |

OPEN_home at R5 is the binding term: its analytic n for 0.8 marginal power under S_A/T1 is ≈ 2,700. Power for NOVCHURN_exc is not interpretable, because its SB is 0.014.

### Checks
Summary in `results/unit_tests.json`.
- **Gate T0 passes exactly** (`results/gate_t0.json`):
  - EXP10 home components and OPEN_home reproduce with diff 0.0.
  - The published cohort OPEN_home +0.0906, NOV_res +0.1337 and edge_persistence −0.1123 reproduce to about 1e-16.
- **Engine and tests:**
  - U1 fast engine == `ego.concept_core` on 1,000 concepts × {full, half, permuted, rarefied}: max diff 1.1e-16.
  - U2, U5 and U6 pass.
  - U3: the curveball toy has 12 states, χ² p = 0.96, and the margins are preserved in the full run.
  - U4: the redesign passes (mean z −0.067); the first design failed and is documented in the deviations.
  - U7 and fastpsp pass.
- **Planted checks:**
  - PC1 passes: under stationarity raw persistence still has ρ = 0.75 with log n, while V2 excess has mean −0.001 and ρ −0.04.
  - **PC2 fails** (see reading 4).
  - PC3: the planted association is recovered in every body (0.19-0.24). The placebo rule failed in 2 of 5 bodies at 20 draws, but a 500-permutation calibration shows nominal 3.6-5.8% false-positive rates (`results/placebo_calibration.json`).
- `rederive.py` re-derives the P1-P3 psp and the pooled SB of NOVCHURN_raw by a separate code path: max diff 2.2e-16.
- **Cross-checks:**
  - EXP12 `open_features` home values are identical (share equal = 1.0 for all six components).
  - Every analysed concept is found in the art_O7Dq4L02QnDN concept key, and the level agrees for 100%.

All deviations from the plan, with reasons, are in `results/deviations.json` (D0-D14).

## What was done (pipeline)
| stage | script | output |
|---|---|---|
| gate T0 | `s0_gate.py` | `results/gate_t0.json` |
| fast engine tests | `tests/u_fast6.py` | `results/unit_tests_fast6.json` |
| freeze + seal | `s1_freeze.py` (+ `lib/seal.py`) | `results/frozen_spec.json`, `logs/seal.log` |
| RAW, V1, V2, V2b, V4 halves | `s2_variants.py` (engine `lib/fast6.py`) | `data/s2_scalars_full.parquet`, `data/s2_parts_full/` |
| V3a / V3b / V3c nulls | `s3_nulls.py` (numba kernels `lib/nullkern.py`) | `data/v3_nulls_full.parquet`, `data/v3_halves_full.pkl`, `results/v3_nulls_full.json` |
| null tests / planted | `tests/u_nulls.py`, `tests/planted.py` | `results/unit_tests_nulls.json`, `results/planted_checks.json` |
| composites, 2nd seal, reliability | `s4_composites.py` | `data/clean_variants.parquet`, `results/frozen_constants_S1b.json`, `results/reliability_x.json` |
| outcome reliability | `s4b_outcome_rel.py` | `results/reliability.json` |
| size dependence | `s5_size.py` | `results/size_dependence.json`, `figures/persistence_vs_n.png` |
| associations | `s6_assoc.py` (tables `lib/tables.py`, bootstrap `lib/fastpsp.py`) | `results/clean_vs_raw_psp_cells.json`, `data/psp_boot.npz` |
| verdict, DL, disattenuation, figures | `s7_verdict.py` | `results/clean_vs_raw_psp.json`, `figures/forest_raw_vs_clean.png`, `figures/reliability_bars.png` |
| power | `s8_power.py` | `results/power_frame_n.json`, `figures/power_curves.png` |
| re-derivation | `rederive.py` | `results/rederive.json` |
| outputs | `method.py` | `method_out.json` (+ `full_/mini_/preview_`), `results/prediction_check.json` |

## Layout
- `method.py`: orchestrator (`--run-all`) and the exp_gen_sol_out builder. Each example has predictions from OLS fitted on DEV only: B5, B5+NOVCHURN_raw/exc/cfg and B5+OPEN_home/OPEN_home_clean.
- `lib/`: copied EXP10 modules (`ego.py`, `ego_ctx.py`, `ladder.py`, `rq1stats.py`, `common*.py`, `outc.py`; sha256 checked against EXP10). Only `common.py` and `ego_ctx.py` paths are patched (D0). The new modules are `fast6.py`, `nullkern.py`, `fastpsp.py`, `tables.py`, `jobs.py`, `seal.py` and `s2_cfg.py`.
- `data/clean_variants.parquet`: **the reusable deliverable for the Frame-N artifact**. It has one row per concept (13,444 with n_home_early ≥ 10: DEV 4670, OLDHO 3214, COH1014 4195, COH1517 1365) and holds all raw and clean variants, null means and sds. It has no outcome columns.
- `results/`: all JSON results. `figures/`: 4 PNGs. `logs/`: run logs and the hash-chained seal log.
- It stays on the run's volume and in the published repo; every file is under 100 MB.

## How to run
```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python numpy pandas pyarrow scipy igraph numba loguru snowballstemmer matplotlib statsmodels psutil
export AII_RUN_ROOT=<run root holding iter_2/EXP5, iter_3/EXP8, iter_4/EXP10>   # read-only inputs
OMP_NUM_THREADS=1 .venv/bin/python method.py --run-all   # stages skip when their output exists; ~1 h on 4 CPUs
```
Compute on 4 CPUs: S2 took 3 min, S3 10 min (rewiring), S6 25 min; everything else took under 2 min.

## Restoring removed files
The files marked `delete` in `.aii/manifest.yaml` are deterministic and seeded. `./restore.sh` rebuilds all of them:
- `.venv/`: `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python numpy pandas pyarrow scipy igraph numba loguru snowballstemmer matplotlib statsmodels psutil`
- `data/home_cache.pkl`: `.venv/bin/python -c "import sys; sys.path.insert(0, 'lib'); from jobs import build_home_cache; build_home_cache()"`
- (not a manifest entry, kept on the run volume but excluded from the published repo) `data/s2_parts_full/`: `.venv/bin/python s2_variants.py --tag full --workers 4`
- `data/v3_halves_full.pkl`: `.venv/bin/python s3_nulls.py --tag full`
- `__pycache__/`, `lib/__pycache__/`: recreated on import.
