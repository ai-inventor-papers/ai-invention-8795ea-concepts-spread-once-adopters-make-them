# Fix the record and test how far openness holds

An evaluation with no new data, built from existing run files. It has two parts.

- **Part A** is a corrections pack for the report's blocking record defects. Every number in `corrections/*.md` is read from a named file and key and written into `results/claims_ledger_v3.csv` as it is inserted. A second, independent code path (`verify_ledger.py`) then re-reads every row.
- **Part B** bounds the Exp8 openness lead (OPEN composite) on the Exp8 held-out groups. Those groups were already unsealed, so **Part B is EXPLORATORY**: it can reveal fragility, but it cannot confirm OPEN. The Part B specification was hash-frozen before any Part B statistic was computed (`results/boundary_spec.json`, sha256 in `logs/seal.log`).

LLM spend: $0. OpenAlex calls: none. CPU only.

## Headline results

| item | result | file |
|---|---|---|
| Gate T0 (reproduce Exp8 pooled psp) | PASS: M0_density_end +0.3745 (O2r_m50) / +0.3770 (O2r_resid), D_vol_end +0.3071, n_comm_W3 +0.1666, ego_density_W3 −0.1024, new_edge_rate +0.1176; all diffs < 1e-3 | `results/gate_T0.json` |
| B1 post-onset re-score | M0_density_end 0.374 → 0.187 (attenuation 0.50 [0.38, 0.60]); D_vol_end 0.317 → 0.176 (0.45 [0.29, 0.64], MATHDEC excluded); verdict PARTIAL for both. D_vol_post is near rank-identical to the B5 `reach` column (ρ 0.965–0.998) | `results/post_onset_rescore.json` |
| B2 OPEN per unit | DL4 O2r_m50 +0.181 [0.082, 0.277], I2 0.73, prediction interval [−0.235, 0.541]; positive in 6/6 units | `results/per_group_table.csv`, `results/per_group_pooled.csv` |
| B3 specification curve (1,920 specs) | share with pooled CI > 0 = 0.997; share of estimates > 0 = 1.000; median 0.152; Freedman–Lane p = 0.005 (200 draws); with CONTACT_REACH as a control the median is 0.146 vs 0.158 | `results/spec_curve.json`, `results/spec_curve_specs.csv` |
| B4 heterogeneity | 21 sub-units: I2 0.43 vs 0.66 over 6 units; no trait moderates (all Holm p = 1); LIFEENV verdict UNEXPLAINED (psp 0.071 vs 0.186 in the other units; coverage reweighting gives 0.069) | `results/heterogeneity.json`, `results/subunit_table.csv` |
| Step 3: D_rca_pers vs D_rca_persist_k | DIFFERENT (max Spearman 0.877 on DEV; recipe check ρ = 1.0000) | `results/drca_persist_comparison.json` |
| Ledger | 1,290 rows: 753 MATCH, 537 ROUNDING_ONLY, 0 MISMATCH, 0 NOT_FOUND; the independent check agrees on every row; 9 orphan tokens (section numbers, a file number, a README line number, "8 outcomes") | `results/claims_ledger_v3.csv`, `results/ledger_verification.json` |

Paper-ready wording for Part B is in `corrections/11_boundary_results.md`.

## Layout

| path | content |
|---|---|
| `seal.py` | STEP 0: `results/inputs_manifest.json` (path, size, sha256 of every input), `results/boundary_spec.json` (OPEN definition with DEV z-constants and PC1 loadings, spec grid, sub-unit rule, traits, GENERIC rule, verdict rules, seeds, iteration-4 listing at seal time), `logs/seal.log` |
| `partb_core.py` | Gate T0, B1 post-onset re-score (the exact Exp8 `states()` code on the window-restricted matrix), B2 per-group table |
| `spec_curve.py` | B3: 120 composites × 4 outcomes × 4 control sets, DL pooling with analytic Fisher-z SEs, 200-draw Freedman–Lane null, 2,000-draw headline bootstrap, bootstrap/analytic SE calibration |
| `heterogeneity.py` | B4: home-field × period sub-units, REML meta-regression with Knapp–Hartung, permutation p and Holm; leave-one-group-out; LIFEENV diagnosis |
| `step3_drca.py` | Exp7 D_rca_pers vs Research 2 D_rca_persist_k on DEV candidate rows |
| `figures.py` | `figures/spec_curve`, `open_forest`, `b1_post_onset`, `lifeenv_diagnosis` (.png and .pdf) |
| `build_corrections.py` | STEP 4: `corrections/00_index.md` … `11_boundary_results.md` and `results/claims_ledger_v3.csv`; derived numbers go first to `results/partA_derived.json` |
| `verify_ledger.py` | STEP 5: independent parser, re-computed statuses and orphan check → `results/ledger_verification.json`, `results/ledger_verification_rows.csv` |
| `eval.py` | STEP 6: `eval_out.json` (schema `exp_eval_sol_out`; 102 metrics; datasets `open_heldout_concepts` 7,728, `spec_curve` 1,920, `claims_ledger_v3` 1,290) plus `full_`/`mini_`/`preview_eval_out.json` |
| `audit_headlines.py` | independent re-derivation of headline numbers (different code path) plus a shuffled-OPEN placebo → `results/audit_headlines.json` |
| `lib/common.py` | paths, constants, DL pooling with prediction interval, Holm, `Ledger` (`num`, `carry`) |
| `lib/data.py` | frozen OPEN composites (equal and PC1 weights) |
| `vendor/rq1stats.py` | verbatim copy of Exp8 `lib/rq1stats.py` (psp_point, psp_boot); its sha256 is in `results/inputs_manifest.json` |
| `corrections/` | the corrections pack (file → section map in `00_index.md`) |
| `results/b_table.parquet` | the Exp8 analysis table plus the re-scored columns (D_vol_post, M0_density_post, footprint, OPEN, OPEN_PC1) |
| `logs/` | the seal log and per-script logs |

## How to run

```bash
uv sync
./run_all.sh          # about 10 min on 4 CPUs; seal.py is commented out so the frozen spec is not overwritten
```

Inputs are read-only files from earlier artifacts of this run: Exp8 `art_dFQ6jbgNsR6Q`, Exp7 `art_22ppE1snfHKj`, Eval2 `art_7W9xiIO3FVBs`, Exp5 `art_wxWssKSUR45f`, Research 2 `art_EesdB8cuSfcU`, and `iter_4/gen_strat/current_report.md`. `lib/common.py` finds them relative to this directory (override with `AII_RUN_LOOP`). The inputs are listed with their sha256 in `results/inputs_manifest.json`.

## Deviations and notes

- **Resource note.** The previous attempt of this artifact crashed the worker. OpenBLAS started 48 threads in each of about 36 worker processes on a 4-CPU box (`pthread_create failed`). Every script now pins BLAS/OMP to 1 thread and uses at most 3 workers. Results that had completed before the crash were checked and kept: seal, T0 and the spec curve. B1, B2 and B4 were re-run.
- **B1 fix after the seal.** Post-onset D_vol is near rank-identical to B5 `reach`, so in MATHDEC its psp is undefined in every bootstrap draw. Undefined draws are now dropped. A unit with fewer than 50% defined draws is excluded from both the full and the post pools (MATHDEC, D_vol only), and this is recorded in `units_excluded_undefined_post`. The frozen verdict rule is unchanged.
- **B4.** Only 21 sub-units reach n ≥ 60 (the plan expected about 30–50). Since 21 ≥ 20, the frozen n ≥ 60 rule is kept. Traits are sub-unit medians, so any trait reading is ecological.
- **GENERIC.** This is the frozen lexical rule (a 100-label audit is in `heterogeneity.json` → `generic.audit_100`). The optional LLM agreement check was not run ($0 by default).
- **Scope of OPEN.** OPEN is the all-papers build only. The HOME-ONLY build and the fresh 2015–16 cohort belong to another iteration-4 artifact. At seal time no cohort outcome was read (see `boundary_spec.json` → `cohort_2015_16_statement`).
- **Exp9.** Experiment 9 is recorded as *not run, not refuted* (`corrections/07_failed_artifacts.md`).

## Restoring removed files

`.aii/manifest.yaml` marks only regenerable caches for deletion:

| path | restore with |
|---|---|
| `.venv/` | `uv sync` (versions pinned in `uv.lock`) |
| `lib/__pycache__/`, `vendor/__pycache__/` | recreated automatically on the next `uv run python <script>.py` |

Everything else (results, figures, corrections, logs, code) is kept in place. No file here is 100 MB or larger, so everything except the deleted caches is also in the published repository.
