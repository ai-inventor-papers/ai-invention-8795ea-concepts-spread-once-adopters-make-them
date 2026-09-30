# Reproducibility: Cheng reach-vs-depth reversal (`gen_art_experiment_14`)

These are the steps that were actually run to produce the numbers in `README.md`, `reconciling_cheng.md` and
`results/*.json`. All paths below are relative to this folder.

## 1. Get the artifact

This folder is published as one folder of the run's public GitHub repository:

```bash
git clone <repository-url>
cd <repository>/round-5/experiment-14/src   # this folder
```

## 2. System, Python and environment

- **OS and tools.** Ubuntu (Linux x86_64). No system packages beyond a C toolchain-free standard install. You need
  `uv` (we used uv 0.6.14) and `git`.
- **Python.** 3.12 (we used 3.12.14, installed by uv).
- **Environment.** Every installed package is pinned exactly in `pyproject.toml`, identical to
  `requirements.lock.txt` (76 packages). Key versions: pyfixest 0.60.0, statsmodels 0.15.0, numpy 2.5.3,
  pandas 2.3.3, scipy 1.18.1, pyarrow 25.0.1, loguru 0.7.3, matplotlib 3.11.2, jsonschema 4.26.0, pytest 9.1.1.
  Create it with:

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r requirements.lock.txt     # or: bash restore.sh
```

- **Hardware used.** 4 CPU cores (cgroup quota) and a 32 GB RAM container. **No GPU.** `method.py` pins one BLAS
  thread per process and parallelises across 4 spawn processes. `lib/common.py:set_limits` caps the address space
  at 26 GB.

## 3. Data, environment variables, keys

- **No downloads and no API keys.** 0 OpenAlex credits and $0 LLM were used; no key is read.
- **Inputs are earlier artifacts of the same run**, read-only, as sibling folders of this one. The single root
  constant is `lib/common.py:RUN_ROOT`, set from the environment variable **`AII_RUN_ROOT`**. By default it is four
  levels above this folder (`Path(__file__)`-anchored), i.e. the directory that contains `3_invention_loop/`. If
  your clone has a different layout, point `AII_RUN_ROOT` at the directory holding `3_invention_loop/`.
- **Files read.** Every file below is < 100 MB. The sha256 of each is in `results/provenance.json`; compare it after
  cloning.

| artifact folder (relative to `3_invention_loop/`) | files read |
|---|---|
| `iter_4/gen_art/gen_art_experiment_11` (Exp11) | `data/frame_matches_long/part_00{1..6}.parquet`, `data/yearly_panel.parquet`, `data/counts_m.parquet`, `inputs/topic_ids.json`, `inputs/topic_meta.csv`, `inputs/backbone/slice{0,1,2}.npz` |
| `round-2/experiment-5/src` (EXP5) | `frame_concepts.csv`, `scan/agg_counts.parquet` |
| `round-3/experiment-8/src` (EXP8) | `data/analysis_table.parquet` (+ `lib/rq1stats.py`, `lib/stats_core.py` copied into `lib/`) |
| `round-4/experiment-10/src` (EXP10) | `data/passC_early.parquet`, `data/analysis_cohort.parquet`, `data/passC_pre_agg.parquet`, `data/sealed/parts/sealed_*.parquet` (2,040 files, sha-checked against `logs/sealed_files.log`), `data/ego_open_{exp5,cohort}.parquet`, `results/frozen_spec.json`, `results/s3_decision.json` (+ `lib/ladder.py` copied) |
| `round-1/experiment-3/src` (EXP3) | `backbone/slice0.npz` (hash check only; the slices are read via Exp11 `inputs/`) |
| `round-4/research-3/src` (art_hSyVUBa2okT2) | `raw/fetch/cheng_all.txt` (Cheng et al. 2023 Table 2 text quoted in `prereg.md`) |

- **No user-uploaded (private) input is used.**
- **Optional variable `AII_JSON_SKILL_DIR`.** It is used only by `tests/test_output.py` to also run the pipeline's
  own validator. Without it, the test validates against the vendored schema `tests/exp_gen_sol_out.schema.json`.

## 4. Commands actually run, in order

Seed: **20260929** everywhere (`lib/common.py:SEED`). Per-task bootstrap seeds are `SEED + offset`, with the offsets
in the code. SOC author subsampling is seeded by `(ci, year)`. `rederive.py` uses 777 for its placebos. The wall
times below are from this run on 4 CPUs, with some steps sharing the CPU.

```bash
.venv/bin/python method.py --only S0                 # seal prereg.md + results/frozen_spec.json -> logs/seal.log; git commit (seconds)
.venv/bin/python -m pytest -c pytest.ini tests/test_measures.py   # U2-U4, U8 before the build
.venv/bin/python method.py --only S1 --sample 50     # staged scale-up (0.4 min)
.venv/bin/python method.py --only S1 --sample 500    # 17 CPU-s / 1,000 concepts (0.5 min)
.venv/bin/python method.py --only S1                 # full build: 13,942 concepts, 279,242 rows (2.4 min)
.venv/bin/python method.py --only S2                 # identity check (0.4 min)
.venv/bin/python method.py --only S3 --quick         # 10% smoke run (2 min; *_quick.json deleted afterwards)
.venv/bin/python method.py --only S3                 # test A, 500-draw ratio bootstrap x 2 builds x 2 specs (20 min)
.venv/bin/python method.py --only S4 --quick         # smoke run (9 min, shared CPU)
.venv/bin/python method.py --only S6,S7 --quick ; .venv/bin/python method.py --only S5 --quick   # smoke runs
.venv/bin/python method.py --only S3NB               # A1-NB re-fit (joint bfgs hit a singular Hessian; 0.4 min)
.venv/bin/python method.py --only S4,S6,S7,S5        # tests B (2,000 draws), D, E, C (500 pyfixest refits): 1.3 + 0.5 + 0.3 + 2.5 min
.venv/bin/python lib/provenance.py                   # input sha256 -> results/provenance.json
.venv/bin/python audit.py                            # independent re-derivations + within-group placebo (1 min)
.venv/bin/python method.py --only S8                 # verdict, figures, method_out.json, reconciling_cheng.md (0.2 min)
.venv/bin/python -m pytest -c pytest.ini tests/      # 10 unit tests -> results/unit_tests.json (1 min)
.venv/bin/python rederive.py                         # headline numbers from raw inputs via statsmodels / QR + placebos (2 min)
```

Then the aii-json format script produced `full_`, `mini_` and `preview_method_out.json` from `method_out.json`.
All four validate as `exp_gen_sol_out`. One command to redo everything after S0:
`.venv/bin/python method.py --only S1,S2,S3,S3NB,S4,S5,S6,S7,S8 && .venv/bin/python audit.py && .venv/bin/python rederive.py`.
S0 refuses to overwrite an existing seal.

## 5. What you should get

Key paths are `file:key`, all under `results/`. These are the numbers the paper's Cheng-reconciliation paragraph
uses (text in `reconciling_cheng.md`).

| number | value | key path |
|---|---|---|
| A1-NB b (Cheng spec), HOME | 0.428 (+53.5% / SD) | `cheng_panel_models.json:builds.HOME.joint.A1_NB.coef.zCONS` |
| A1 PPML, % per SD | +83.1% [+70.6, +96.5] | `cheng_panel_models.json:builds.HOME.joint.A1.coef.zCONS` |
| A2 (+ log V(t)), % per SD | +1.3% [+0.5, +2.1] | `cheng_panel_models.json:builds.HOME.joint.A2.coef.zCONS` |
| A2/A1 ratio | 0.021 [0.009, 0.035] | `cheng_panel_models.json:builds.HOME.joint.ratio_boot` |
| raw Spearman(CONS_early, V(t0+3)) | +0.256 [+0.239, +0.274] | `cheng_static.json:volume.EXP5_pooled\|volume.B_raw_spearman_V_t0p3` |
| psp(CONS_early, O2r_m50 \| B5), primary | -0.069 [-0.093, -0.047] | `cheng_static.json:trait.EXP5_pooled\|CONS_early_home.psp.O2r_m50` |
| same, 2015-17 cohort | -0.111 [-0.197, -0.030] | `cheng_static.json:trait.COHORT_2015_17\|CONS_early_home.psp.O2r_m50` |
| paired diff psp(O1c) - psp(O2r_m50) | +0.035 [+0.004, +0.066] | `cheng_static.json:trait.EXP5_pooled\|CONS_early_home.paired_diff.O1c-O2r_m50` |
| C1 within-concept entries | b = +0.025, boot CI [+0.004, +0.048] | `panel_C.json:C1` |
| verdict | REVERSAL CONFIRMED (on selection data), REVERSAL REPLICATED, SIZE-DOMINATED, DEPTH-REACH SPLIT | `cheng_verdict.json:verdicts` |

Figures: `figures/fig_cheng_ladder`, `fig_reach_depth_forest` and `fig_palla` (.png/.pdf). Bootstrap CIs depend on
the seeds above and reproduce exactly on the same library versions. Point estimates are deterministic.

## 6. Independent checks

- **`results/rederive.json` (all_pass = true).** Every headline number above except C1 is recomputed from raw
  inputs through a different code path: V(t) re-aggregated from EXP5 agg_counts, early CONS re-averaged from
  cheng_features, statsmodels GLM Poisson/NB on the full 105,839-row panel, and pandas ranks + numpy QR for psp.
  Agreement is 1e-9 to 1e-6; NB with fixed alpha agrees to 3e-8. Placebos fail as they should:
  - shuffled V: |rho| p95 = 0.018;
  - globally shuffled CONS: |psp| p95 = 0.023, 0/200 as extreme as -0.069;
  - permuted CONS in the panel: A1 b within ±0.016, versus 0.605 for the real b.

  The naive (non-clustered) Poisson z on that placebo reaches |34|. This shows why the pipeline reports
  CRV1/cluster-bootstrap CIs only.
- **C1 is NOT independently re-derived.** A concept + year FE PPML with 11,761 concepts was not re-fitted in a
  second library. It rests on pyfixest with CRV1 plus a 500-draw cluster bootstrap.
- **`results/audit.json`.** statsmodels vs pyfixest on a 2,000-concept subset, statsmodels OLS-on-ranks psp, hand
  DL, and a within-group shuffled-CONS placebo (p95 |psp| = 0.025).
- **Unit tests.** 10/10 pass (`results/unit_tests.json`), including U6, which reproduces EXP8's published psp to
  1e-10.
