# Reproducibility

This describes what was actually run to produce the files in this folder.

## 1. Get the artifact

This folder is published as one folder of the run's public GitHub repository.

```bash
git clone <repository-url>
cd <repository>/<this-folder>        # the folder that holds eval.py, run_all.sh and this file
```

### Inputs from other artifacts

Every input is a file written by an earlier artifact of the same run. Each is under 100 MB, so all are in the repository's sibling folders:

| artifact id | role | files read |
|---|---|---|
| `art_dFQ6jbgNsR6Q` (Exp8) | estimator, analysis table, record | `data/analysis_table.parquet`, `data/frame_arrays.npz`, `inputs/field_backbone.json`, `lib/rq1stats.py` (copied verbatim to `vendor/`), `lib/indicators.py`, `results/*.json\|csv`, `README.md` |
| `art_22ppE1snfHKj` (Exp7) | record tables, D_rca check | `results/step2_dev.json`, `results/step2_heldout.json`, `results/frontier_result.json`, `results/frozen_spec.json`, `results/state_panel_dev.parquet`, `results/risk_sets_exp5_minus_exp6_dev.parquet` |
| `art_7W9xiIO3FVBs` (Eval2) | corrections to render | `text_corrections.md`, `claims_ledger.csv`, `o5_validation.json`, `record_tables/*` |
| `art_wxWssKSUR45f` (Exp5) | frame reference | listed in `results/inputs_manifest.json` |
| `art_EesdB8cuSfcU` (Research 2) | D_rca_persist_k definition | `research_report.md` |
| strategy step | correction targets (old text) | `iter_4/gen_strat/current_report.md` |

The code finds these inputs through ONE setting: the directory that contains the run layout `iter_2/gen_art/...`, `iter_3/gen_art/...` and `iter_4/gen_strat/...`.

- By default this is three levels above this folder (`Path(__file__).parents[2]` in `lib/common.py`).
- To override it, set `AII_RUN_LOOP=<dir>`.
- If your clone names the sibling folders by artifact id instead, arrange (or symlink) them into that layout:
  - `round-3/experiment-8/src` → `art_dFQ6jbgNsR6Q`
  - `round-3/experiment-7/src` → `art_22ppE1snfHKj`
  - `round-3/evaluation-2/src` → `art_7W9xiIO3FVBs`
  - `round-2/experiment-5/src` → `art_wxWssKSUR45f`
  - `round-3/research-2/src` → `art_EesdB8cuSfcU`
  - `iter_3/gen_art/gen_art_experiment_9` → the failed Exp9 folder (only its `.aii_worker_result.json` is read)

`results/inputs_manifest.json` lists every input with its size and sha256, so you can check your copies. No user-uploaded file is used.

## 2. System and Python environment

- Ubuntu 22.04+, CPU only.
- The run used 4 CPUs, about 1 TB RAM available (under 3 GB used) and no GPU.
- Python **3.12.14**, managed by `uv`.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh     # if uv is missing
uv venv --python 3.12 .venv
uv sync                                               # installs exactly the pins in pyproject.toml / uv.lock
```

Pinned versions (identical to `pyproject.toml`):

- Core: numpy 2.5.3, pandas 3.0.6, pyarrow 25.0.1, scipy 1.18.1, scikit-learn 1.9.1, statsmodels 0.15.0, matplotlib 3.11.2
- Utilities: wordfreq 3.1.1, loguru 0.7.3, jsonschema 4.26.0, pyyaml 6.0.3
- The rest are transitive pins listed in `pyproject.toml`.

Set single-threaded BLAS. Every script also sets this itself, because the first attempt of this artifact died of OpenBLAS thread exhaustion:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
```

- No API keys or environment secrets are needed.
- No LLM or OpenAlex calls are made, and nothing is downloaded.
- The only optional variable is `AII_RUN_LOOP` (see above).

## 3. Commands, in the order they were run

All seeds are 20260929. Gate T0 reuses Exp8's seeds (20260928 plus fixed offsets) so the record is reproduced exactly.

| step | command | what it writes | runtime (4 CPUs) |
|---|---|---|---|
| 0 seal (run once, 02:23 UTC; do NOT re-run unless re-freezing) | `uv run python seal.py` | `results/inputs_manifest.json`, `results/boundary_spec.json`, `logs/seal.log` (sha256 `61a354ec…c9c`) | ~1 min |
| 1 gate T0 | `uv run python partb_core.py --stage t0 --workers 3` | `results/gate_T0.json` | ~1 min |
| 2a B1 | `uv run python partb_core.py --stage b1 --workers 3 --nboot 1000` | `results/b_table.parquet`, `results/post_onset_rescore.json` | ~1.5 min |
| 2b B2 | `uv run python partb_core.py --stage b2 --workers 3 --nboot 1000` | `results/per_group_table.csv`, `per_group_pooled.csv`, `per_group_extra.json`, `b2_new_rows.csv` | ~0.5 min |
| 2c B3 | `uv run python spec_curve.py --null 200 --workers 3` | `results/spec_curve.json`, `spec_curve_specs.csv`, `spec_curve_null_DL4/DL6.csv` | ~5 min |
| 2d B4 | `uv run python heterogeneity.py --nperm 1000 --nboot 1000` | `results/heterogeneity.json`, `subunit_table.csv` | ~10 s |
| 3 | `uv run python step3_drca.py` | `results/drca_persist_comparison.json` | ~20 s |
| figures | `uv run python figures.py` | `figures/{spec_curve,open_forest,b1_post_onset,lifeenv_diagnosis}.{png,pdf}` | ~5 s |
| 4 Part A | `uv run python build_corrections.py` | `corrections/00..11_*.md`, `results/claims_ledger_v3.csv`, `results/partA_derived.json` | ~5 s |
| 5 | `uv run python verify_ledger.py` | `results/ledger_verification.json`, `ledger_verification_rows.csv` | ~5 s |
| 6 | `uv run python eval.py` | `eval_out.json` | ~5 s |
| 6b | `python <aii-json skill>/aii_json_format_mini_preview.py --input eval_out.json` | `full_/mini_/preview_eval_out.json` | seconds |
| audit | `uv run python audit_headlines.py` | `results/audit_headlines.json` | ~1 min |

`./run_all.sh` runs steps 1–6 in this order. The seal step is commented out so that the frozen spec is kept.

**What differed from the plan's run.** The spec curve (B3) came from the first attempt of this artifact. It finished before the container crash and was not re-run: it read only sealed inputs, and its null had its full 200 draws. B1, B2 and B4 were re-run after the crash with single-threaded BLAS. B1 was also re-run after a post-seal fix: bootstrap draws in which psp is undefined are dropped, and MATHDEC is excluded from the D_vol pools because post-onset D_vol is rank-collinear with B5 `reach`. README.md lists all deviations.

## 4. What you should get

Values are all in `eval_out.json` → `metrics_agg`. The text of each result is in `corrections/11_boundary_results.md`, and the paper uses it as new Section 19.10 and the corrected Sections 18–22.

| result | expected value | file / key |
|---|---|---|
| Gate T0 | pass; M0_density_end +0.3745 (O2r_m50), D_vol_end +0.3071, n_comm_W3 +0.1666, ego_density_W3 −0.1024, new_edge_rate +0.1176; diffs ≤ 3e-17 | `results/gate_T0.json` |
| B1 M0_density_end, O2r_m50, 4 held-out groups | full 0.374 → post-onset 0.187 [0.145, 0.246]; attenuation 0.50 [0.38, 0.60]; PARTIAL | `post_onset_rescore.json` → `pooled["DL4\|M0_density_end\|O2r_m50"]` |
| B1 D_vol_end (MATHDEC excluded) | 0.317 → 0.176; attenuation 0.45 [0.29, 0.64]; PARTIAL | same file, `D_vol_end` key |
| OPEN pooled psp, O2r_m50, DL4 (bootstrap-SE pooling) | +0.181 [0.082, 0.277], I2 0.73, prediction interval [−0.235, 0.541] | `per_group_pooled.csv` |
| Spec curve | 1,920 specs; share CI > 0 = 0.997; median 0.152; Freedman–Lane p = 0.005 (200 draws) | `spec_curve.json` |
| Heterogeneity | 21 sub-units, I2 0.43 (vs 0.66 over 6 units); no trait moderates; LIFEENV UNEXPLAINED | `heterogeneity.json` |
| D_rca_pers vs persist_k | DIFFERENT (max Spearman 0.877) | `drca_persist_comparison.json` |
| Ledger | 1,290 rows: 753 MATCH, 537 ROUNDING_ONLY, 0 MISMATCH, 0 NOT_FOUND; independent verification agrees on every row | `claims_ledger_v3.csv`, `ledger_verification.json` |

Bootstrap and permutation numbers are deterministic given the seeds. Point estimates are exact.

## 5. Independent audit (`audit_headlines.py`)

The audit uses a separate code path: pandas ranks with statsmodels OLS residuals, OPEN rebuilt from the raw table, D_vol_post rebuilt from the raw arrays, and an inline DL pool with analytic SEs. It gets:

- The OPEN rebuild is identical: max abs diff 0.0, NaN pattern equal.
- The D_vol_post rebuild is identical for 100% of concepts.
- Per-unit psp matches the record to ≤ 5e-16 for M0_density_end, D_vol_end and OPEN.
- Analytic-SE pooled values:

  | quantity | analytic-SE pool | reported (bootstrap-SE pool) |
  |---|---|---|
  | M0_density_end | 0.374 | 0.3745 |
  | D_vol_end | 0.310 | 0.307 |
  | OPEN DL4 | 0.189 | 0.181 |
  | OPEN DL6 | 0.168 | 0.163 |

  The small gaps come only from the variance model.
- Spec share, median and permutation p recomputed from the raw spec and null rows match exactly (0.996875, 0.1516, 0.004975).
- **Placebo.** OPEN shuffled within unit (20 draws) gives a mean pooled psp of −0.004 (max |est| 0.071). 2 of 20 draws have a CI excluding 0, as expected from the nominal 5% rate. The test does not pass vacuously.
