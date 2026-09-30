# Reproducing the RQ1 held-out indicator test

This describes exactly what was run for this artifact (AI Inventor run, iteration 3, `gen_art_experiment_8`).

## 1. Get the artifact

The workspace is published as one folder of a public GitHub repository. Clone the repository and `cd` into this
artifact's folder (`gen_art_experiment_8`). The other run artifacts it reads are published as sibling folders:

| input | artifact id | how the code finds it |
|---|---|---|
| EXP5 frame, outcomes, basic features, `scan/agg_counts.parquet` | `art_wxWssKSUR45f` (`round-2/experiment-5/src`) | `lib/common.py: EXP5` |
| EXP3 ego-network code / backbones (copied into `lib/`, `inputs/`) | `art_yrradSC27HtQ` (`round-1/experiment-3/src`) | `lib/common.py: EXP3` (only `tests/t0_8_ego_port.py` reads it) |
| EXP6 D3 code / phi backbone (copied) and `results/frame_concepts.csv` | `art_N-mpomDZZ1ln` (`round-2/experiment-6/src`) | `lib/common.py: EXP6` |
| Eval1 F3 portability prior | `round-2/evaluation-1/src` | `lib/common.py: EVAL1` |
| O5 external recognition (declared dependency) | `art_O7Dq4L02QnDN` (`round-2/dataset-2/src`) | `lib/common.py: O5DIR` |

All of them resolve from ONE constant, `RUN_ROOT` in `lib/common.py` (default: four levels above this folder, i.e.
the run tree layout). Set the environment variable `AII_RUN_ROOT` to the folder that contains `3_invention_loop/`
if your layout differs. No user-uploaded file is used.

## 2. System and Python

- Ubuntu (Debian 12 container used here), Python **3.12.14**, [uv](https://github.com/astral-sh/uv) 0.x.
- `./restore.sh` creates `.venv` and installs the exact pinned versions from `requirements.lock.txt` (identical
  pins to `pyproject.toml`, e.g. numpy 2.5.3, pandas 3.0.6, pyarrow 25.0.1, scikit-learn 1.9.1, python-igraph 1.0.0,
  interpret 0.7.8, pyahocorasick, snowballstemmer, scipy, loguru, matplotlib, joblib).

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r requirements.lock.txt
```

## 3. Data, credentials

- OpenAlex works snapshot: read directly from the **public** S3 bucket over HTTP range requests
  (`https://openalex.s3.amazonaws.com/`, keys listed in `snapshot/works_manifest.json`, snapshot of 2026-09-23;
  2,040 parquet files, 476,196,327 works). No API key and **0 OpenAlex credits** are needed.
- No LLM calls: **$0 OpenRouter**. No environment variables are required other than the optional `AII_RUN_ROOT`.
- Hardware used: 6 vCPU container (cgroup quota 5.1 CPUs), 57 GB RAM; no GPU was used. 5 worker processes.

## 4. Commands, in the order they were run

Seed everywhere: **20260928**.

```bash
.venv/bin/python tests/test_units.py                  # T0 1-7 (<1 min)       -> results/unit_tests.json
.venv/bin/python tests/t0_8_ego_port.py               # T0-8 (~2 min)         -> results/t0_8_ego_port.json
.venv/bin/python passA.py --files 65,1125,1407,1918 --workers 4 && .venv/bin/python tests/t1_check.py 65,1125,1407,1918   # T1
.venv/bin/python passA.py --workers 5                 # Pass A: 62 min (network-capped; 33 min at full bandwidth)
.venv/bin/python passA.py --merge
.venv/bin/python tests/checks.py A                    # T2: A1 / A2           -> results/checks.json
.venv/bin/python passB.py --workers 5                 # Pass B: 24 min
.venv/bin/python passB.py --merge
.venv/bin/python tests/checks.py B                    # T3
.venv/bin/python build_features.py --stage basic
.venv/bin/python build_features.py --timing 60 --workers 5   # T4 timing (the run then applied F4(ii): cutoff 3)
.venv/bin/python build_features.py --stage ego --workers 5   # family A: 36 min (N_NULL 200, betweenness cutoff 3)
.venv/bin/python build_features.py --stage assemble
.venv/bin/python outcomes.py                          # outcome table + outcome seal (logs/outcome_seal.log)
.venv/bin/python dev_select.py --stage all --workers 5   # DEV ranking, learned models, power, FREEZE (logs/seal.log)
.venv/bin/python heldout.py --stage all --workers 5      # the single unseal + all held-out scoring
.venv/bin/python audit.py                             # T7                    -> results/audit.json
.venv/bin/python make_outputs.py                      # rq1_heldout.json, figures, method_out.json
.venv/bin/python rederive.py                          # independent re-derivation of the headline numbers
```

`python method.py` runs the same sequence and skips steps whose outputs exist. The seal permits one unseal per frozen
spec: re-running `heldout.py --stage unseal` against the existing seal raises `SealError` by design; to redo the
whole confirmatory test, delete `logs/unsealed.json` and `logs/seal.log` and re-freeze (it is then no longer a
sealed test).

## 5. What you should get

Numbers below are in `results/rq1_heldout.json` (tables rendered into `README.md` by `readme_tables.py`, which
`readme_tables.py --check` verifies). Bootstrap CIs can move in the third decimal if the worker scheduling changes the
job-to-seed order; the seeds are fixed per job, so a rerun on the same code reproduces them.

- Checks: `results/checks.json` A1 `share_identical_yearly_vectors` = 1.0, A2 `spearman_all_cells` = 1.000;
  `results/unit_tests.json` 7/7 pass; `results/t0_8_ego_port.json` pass; `results/audit.json` `all_pass` = true.
- Frozen spec sha256 `c3906b4f3dd6...` (`logs/seal.log`), code commit `64ed779`.
- Breadth (O2r_resid, DL-pooled 4 held-out groups): M0_density_end psp +0.377 [+0.280, +0.466]; D_vol_end +0.307;
  CONTACT_REACH +0.210; n_comm_W3 +0.164; NOV +0.152; ego_density_W3 -0.097; RETENTION_RATIO_early -0.120;
  8/10 confirmed after Holm (7/10 for O2r_m50).
- O1c: only n_authors_early confirmed (+0.161). O4: REL_home -0.114, author_growth +0.065 confirmed. O5 / O5_WW: none.
- Learned vs B5 (held-out pooled): O2r_m50 Spearman 0.706 (B5) -> 0.765 (ElasticNet) / 0.757 (EBM); O4 EBM 0.188 vs
  B5 0.015; O3 AUC 0.506 -> 0.599 (L1-logit); O1c, O1b, O5, O5_WW: no reliable gain.
- Pre-registered predictions: P2 HOLDS; P1, P3, P4, P5 FAIL (`results/prereg_verdicts.json`).
- Figures: `figures/portability_heatmap.png`, `figures/heldout_forest_O2r_resid.png`, `figures/learned_vs_single.png`
  are the RQ1 figures intended for the paper's RQ1 results section (indicator portability, held-out validation,
  learned-model comparison); `figures/indicator_clusters.png` supports the indicator-design section.

