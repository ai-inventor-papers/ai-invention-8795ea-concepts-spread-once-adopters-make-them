# Reproducibility: "Is neighbourhood churn real or thin-sample noise?"

These are the exact steps that produced the results in this folder. Every path below is relative to this folder.

## 1. Get the artifact
This folder is published as one folder of a public GitHub repository:
```bash
git clone <repository-url>
cd <repository>/<this-artifact-folder>      # the folder that contains method.py and this file
```

## 2. System, Python and libraries
- Ubuntu or Debian (the run used Debian 12 in a Docker container), with no extra system packages.
- Hardware: 4 vCPU (AMD EPYC 9655P), a 29 GB RAM cgroup limit, no GPU. Peak RAM was about 3 GB.
- Python **3.12.14**. Environments are created with `uv`; the run never used pip.

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r <(python3 - <<'EOF'
import tomllib; print("\n".join(tomllib.load(open("pyproject.toml","rb"))["project"]["dependencies"]))
EOF
)
```

The exact versions installed are pinned in `pyproject.toml`: numpy 2.5.3, pandas 3.0.6, scipy 1.18.1, igraph 1.0.0, numba 0.67.0, pyarrow 25.0.1, matplotlib 3.11.2, statsmodels 0.15.0, loguru 0.7.3, snowballstemmer 3.1.1, psutil 7.2.2, plus their dependencies. These are the same numpy, pandas, scipy and igraph versions EXP10 used.

Always run with `OMP_NUM_THREADS=1`. Multi-threaded BLAS inside process pools made `psp_point` 10-30× slower in this run.

## 3. Inputs (no downloads, no API keys, $0 LLM spend)
All inputs are read, read-only, from earlier artifacts of the same run. The code resolves them through ONE root: the environment variable `AII_RUN_ROOT`. When it is unset, the root defaults to the folder three levels above this one (`lib/common.py`: `RUN_ROOT`). Under that root the code expects these sub-folders:

| artifact id | expected relative location under `AII_RUN_ROOT` | what is read |
|---|---|---|
| art_NMe386dX9GLF (EXP10) | `3_invention_loop/iter_4/gen_art/gen_art_experiment_10` | `inputs/` (topic backbone slices, topic meta, lexicon), `data/{ego_open_*, features_exp5_open, analysis_cohort, passC_early, passC_pre_agg, cohort_candidates.csv, bg_topics.npz, sealed/parts}`, `results/{frozen_spec, cohort_result}.json` |
| art_dFQ6jbgNsR6Q (EXP8) | `3_invention_loop/iter_3/gen_art/gen_art_experiment_8` | `data/frame_matches_early/part_*.parquet` |
| art_wxWssKSUR45f (EXP5) | `3_invention_loop/iter_2/gen_art/gen_art_experiment_5` | `frame_concepts.csv`, `scan/agg_counts.parquet` (outcome-window field counts) |
| art_uw4OeagJP3rv (EXP12) | `3_invention_loop/iter_4/gen_art/gen_art_experiment_12` | `open_features.parquet` (cross-check only) |
| art_O7Dq4L02QnDN (dataset) | `3_invention_loop/iter_2/gen_art/gen_art_dataset_2` | `full_data_out/*.json` (concept key cross-check only) |

If your clone lays these artifacts out differently, create that directory tree with symlinks and `export AII_RUN_ROOT=<that dir>`.

Some input files are 100 MB or larger (for example EXP5 `scan/agg_counts.parquet`), and the publisher does not push those. Rebuild them with the owning artifact's own `reproducibility.md`.

No user-uploaded material was used.

## 4. Commands, in the order they were run
Each stage writes its outputs and is skipped by `method.py --run-all` when the output exists. All seeds are fixed in `results/frozen_spec.json`.

```bash
export OMP_NUM_THREADS=1
.venv/bin/python s0_gate.py                  # ~40 s   gate T0 -> results/gate_t0.json (all diffs 0.0)
.venv/bin/python tests/u_fast6.py 1000       # ~1 min  U1/U2/U5/U6 -> results/unit_tests_fast6.json
.venv/bin/python s1_freeze.py                # seal 1 -> results/frozen_spec.json, logs/seal.log
.venv/bin/python s2_variants.py --tag full --workers 4   # ~3 min, 13,444 concepts
.venv/bin/python s3_nulls.py --tag full      # ~10 min (600 igraph rewires in 3 processes + numba curveball)
.venv/bin/python tests/u_nulls.py            # ~3 min  U3 toy curveball, U4 rewire calibration
.venv/bin/python tests/planted.py            # ~30 s   PC1, PC2
.venv/bin/python s4_composites.py            # ~2 min  seal 2 (constants) + split-half reliability
.venv/bin/python s4b_outcome_rel.py          # ~1 min  outcome reliability
.venv/bin/python s5_size.py                  # ~5 s
.venv/bin/python s6_assoc.py --workers 4     # ~25 min, 1,217 bootstrap cells, B = 2000, seed 20260930
.venv/bin/python s7_verdict.py               # ~1.5 min  P1-P3, verdict, DL, disattenuation, figures
.venv/bin/python s8_power.py                 # ~1 min   Frame-N power, 1000 draws
.venv/bin/python rederive.py                 # independent re-derivation
.venv/bin/python tests/placebo_calibration.py   # post-seal calibration (exploratory)
.venv/bin/python tests/headline_check.py     # headline audit, shuffled-outcome control
.venv/bin/python method.py                   # method_out.json (+ results/prediction_check.json)
SKILL=<aii-json skill>/scripts/aii_json_format_mini_preview.py; python $SKILL --input method_out.json   # full/mini/preview
```

`method.py --run-all` runs the same sequence, skipping finished stages; on 4 CPUs the whole pipeline takes about 50 min of wall time. `./restore.sh` rebuilds the bulk files that are not published (see the README).

Two tests were added or changed during the run, and both are declared in `results/deviations.json`:
- the U4 redesign (D9);
- `tests/placebo_calibration.py` (D11).

## 5. What you should get
Stochastic stages are seeded and should reproduce exactly on the same library versions. Key numbers, with the file and key path:

- **Verdict `PARTLY_THIN`**: `results/clean_vs_raw_psp.json → verdict.verdict`.
  - P1 false: same-sample ratio 0.40 in COH1517, 0.05 in OLDHO.
  - P2 true: z_pers_cfg pooled psp −0.116 [−0.145, −0.086].
  - P3 true: ρ = 0.034.
  - V1 retention 0.76 in COH1517 and 0.64 in OLDHO.
- **Pooled R2 psp with O2r_m50** (`headline_R2_O2r_m50`):
  - NOVCHURN_raw +0.116, NOVCHURN_exc +0.008, NOVCHURN_rare10 +0.078.
  - edge_persistence raw −0.088, its V2 null mean −0.120.
  - OPEN_home +0.085, OPEN_home_clean +0.115.
- **Thin-sample share** R² = 0.660 (`results/size_dependence.json → thin_sample_share.POOLED.R2`).
- **Split-half SB** (`results/reliability.json → variants.<v>.pooled.SB`): NOVCHURN_raw 0.476, NOVCHURN_exc 0.014, OPEN_home 0.485, OPEN_home_clean 0.577. The outcome O2r_m50 has SB 0.895.
- **Power**: joint Frame-N power at n = 800 / 2500 is 0.07 / 0.26 under S_A-T3 and 0.31 / 0.75 under S_A-T2 (`results/power_frame_n.json → results`).
- **Checks**:
  - `results/rederive.json → pass` is true (max diff 2.2e-16).
  - `results/headline_check.json` re-derives the numbers above; every shuffled-outcome control is null.
  - `results/unit_tests.json` summarises all unit and planted checks. PC2 fails by design of V2, as documented.
- **Figures**: `figures/forest_raw_vs_clean.png` (raw vs clean forest plot by body), `figures/persistence_vs_n.png` (the thin-sample picture), `figures/reliability_bars.png` and `figures/power_curves.png`. In the paper these support the RQ1 robustness section: churn is a static topical-dispersion property, not temporal turnover.
