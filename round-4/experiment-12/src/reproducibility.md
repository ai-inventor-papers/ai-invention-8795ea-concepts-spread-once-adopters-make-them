# Reproducing `gen_art_experiment_12` (RQ2: contact versus keeping)

These are the steps that were actually run, on 2026-09-29, on a shared Ubuntu server. Every path below is relative
to this artifact's folder.

## 1. Get the artifact

This folder is one folder of the run's public GitHub repository.

```bash
git clone <repository URL>
cd <repository>/<this artifact's folder>        # the folder holding method.py and this file
```

## 2. System, Python and libraries

- Ubuntu (Linux 6.8 kernel). The run used **CPU only**: 48 cores and about 250 GB RAM, of which about 24 worker
  processes were used. No GPU.
- Python **3.12** and [`uv`](https://docs.astral.sh/uv/) 0.6.14. No system packages beyond a C toolchain are needed;
  all wheels are binary.
- The exact installed versions are pinned in `pyproject.toml` (46 packages, `==` pins). The same list is in
  `requirements.lock.txt`. The main ones are numpy 2.5.3, pandas 3.0.6, pyarrow 25.0.1, scipy 1.18.1,
  scikit-learn 1.9.1, statsmodels 0.15.0, numba 0.67.0, tslearn 0.9.0, kmedoids 0.5.5, hmmlearn 0.3.3,
  networkx 3.7, igraph 1.0.0, lifelines 0.30.0, matplotlib 3.11.2, wordfreq 3.1.1, snowballstemmer 3.1.1 and
  loguru 0.7.3.

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python -r pyproject.toml      # or: bash restore.sh
```

## 3. Inputs, environment variables and keys

- **No API keys and no downloads.** The artifact is cache-only: it makes no OpenAlex, S3 or LLM calls, and a network
  guard in `lib/common.py` refuses HTTP and S3 client imports.
- The inputs are other artifacts of the same run, published as sibling folders of the repository. They are read
  through one constant each in `lib/common.py`, and each can be overridden by an environment variable:

  | env var | artifact id | used for |
  |---|---|---|
  | `AII_EXP5_DIR` | art_wxWssKSUR45f (EXP5) | `frame_concepts.csv`, `scan/year_field_totals.npz`, `scan/scan_info.json`, `concept_outcomes.csv`, `episodes.csv`, `lexicon_v1.parquet` |
  | `AII_EXP6_DIR` | art_N-mpomDZZ1ln (EXP6) | `inputs/field_backbone.json`, `results/frame_concepts.csv`, `results/cluster_assign_*.csv` |
  | `AII_EXP7_DIR` | art_22ppE1snfHKj (EXP7) | `results/state_panel_{dev,heldout}.parquet`, `results/overlap_report.json`, `results/risk_sets_*.parquet` (row counts only) |
  | `AII_EXP8_DIR` | art_dFQ6jbgNsR6Q (EXP8) | `data/analysis_table.parquet`, `data/outcomes.parquet`, `data/features_basic.parquet`, `data/ego_features.parquet`, `data/frame_matches_early/part_001.parquet`, `data/frame_arrays.npz`, `data/bg_topics.npz`, `data/o5_events.parquet`, `data/pass{A,B}_info.json`, `inputs/*`, `results/case_exemplars.json` |
  | `AII_DS2_DIR` | art_O7Dq4L02QnDN (dataset_2) | `full_data_out/full_data_out_{1,2,3}.json` (recognition-event cross-check for the case pairs) |

- If none are set, each defaults to `AII_RUN_ROOT/3_invention_loop/iter_{2,3}/gen_art/<folder>`, where
  `AII_RUN_ROOT` defaults to four levels above this folder (the run's own layout). In the published repository, set
  the five variables to the sibling folders of those artifact ids.
- Every input file listed above is under 100 MB (the largest, EXP8 `frame_matches_early/part_001.parquet`, is about
  27 MB), so all of them are in the published sibling folders.
- No user-uploaded files are used (the run's `user_uploads` folder was empty).
- Optional: `AII_JSON_SKILL` points to the aii-json schema validator used to check `method_out.json` after every
  stage. Without it, the validation step raises; the analysis itself does not need it.

## 4. Commands, in the order run

Seed `SEED = 20260929` everywhere (`lib/common.py`). The run used 2,000 concept-bootstrap resamples, 1,000
permutations for the sequence null and 200 placebo shuffles. Wall times on the shared machine are given in brackets.

```bash
.venv/bin/python s0_skeleton.py                                  # skeleton + validation + provenance      [<1 min]
.venv/bin/python s2_open.py --stage join
.venv/bin/python s2_open.py --stage test   --workers 24          # T2: ego_open == EXP8 on 300 concepts     [1 min]
.venv/bin/python s2_open.py --stage timing --workers 24
.venv/bin/python s2_open.py --stage home   --workers 24          # HOME-ONLY OPEN                         [<1 min]
.venv/bin/python s2_open.py --stage size   --workers 24          # SIZE-MATCHED OPEN (20 draws)           [3 min]
.venv/bin/python s2_open.py --stage assemble
.venv/bin/python s3_states.py                                    # D3 states + EXP7 verification          [2 min]
.venv/bin/python s4_decomp.py --scope dev                        # decomposition, PR verdicts on DEV      [1 min]
.venv/bin/python s5_typology.py --scope dev --workers 24         # DTW/HMM/PCA on DEV                      [37 min; HMM restarts dominate]
.venv/bin/python s6_sequence.py --scope dev                      # light sequence test                    [1 min]
.venv/bin/python s7_seal.py --freeze                             # freeze spec, T6 checklist, ONE-TIME unseal
.venv/bin/python s7_seal.py --run                                # held-out/cohort S4, S5, S6              [8 min]
.venv/bin/python s8_cases.py                                     # case pairs                             [1 min]
.venv/bin/python s9_atlas.py                                     # AI/CS atlas                            [1 min]
.venv/bin/python s10_outputs.py                                  # pipeline counts, method_out.json, figures
.venv/bin/python rederive.py                                     # T7 independent re-derivation
.venv/bin/python tests/test_units.py                             # T0 unit tests                          [8 min]
.venv/bin/python audit_headlines.py                              # headline re-derivation + placebos      [3 min]
```

`python method.py` runs the same sequence; `python method.py --from S8` resumes from a stage.

- The seal is one-shot. `s7_seal.py --freeze` refuses to run once `logs/unsealed.json` exists, and the held-out
  stages refuse to read held-out outcomes until it exists. A reader who clones the published folder gets the marker
  and can rerun the held-out stages; to redo the full sealed protocol, delete `logs/unsealed.json`,
  `logs/seal.log` and `results/frozen_spec.json` first.
- `s8_cases.py`, `s9_atlas.py` and `s10_outputs.py` were rerun after small post-seal fixes (listed in
  `results/deviations.json`); the commands above give the final outputs.

## 5. What you should get

| output | key numbers | where used |
|---|---|---|
| `results/states_verification.json` | 0 state mismatches over 5,557,942 EXP7 cells; 658 rebuilt EXP6-overlap concepts | methods (data integrity) |
| `results/t2_ego_open_reproduction.json` | max abs diff 0 for all 6 OPEN components | methods |
| `results/decomposition_dev.json` | PR1 (Medicine excluded, volume-stratified): s_explore - s_ret = 0.633 [0.537, 0.727]; s_E2 / s_M / s_rho = 0.79 / 0.03 / 0.18; PR2 REVERSED (raw), partial Spearman -0.169 | RQ2 decomposition results, `figures/fig_decomposition_waterfall` |
| `results/decomposition_heldout.json` | held-out pooled PR1 0.492 [0.403, 0.575]; cohort 0.445 [0.358, 0.527]; DL 0.504 [0.329, 0.679], I2 0.76 | robustness, `figures/fig_forest_explore_vs_retention` |
| `results/trajectories_dev.json`, `results/trajectories_heldout.json` | k = 4; ARI(DTW, HMM) 0.222 -> CONTINUUM; PC1 38.8%, PC2 10.7%; OPEN_all ~ PC1 partial 0.174 (DEV), held-out DL 0.120 | typology/continuum, `figures/fig_pca_loadings`, `fig_open_vs_pc1_hexbin`, `fig_dtw_hmm_agreement` |
| `results/sequence_light_*.json` | excess A < T over the null: -0.009 / +0.011 / -0.017; intersection-born HR 0.47 (DEV) | ordering (secondary), `figures/fig_km_takeoff` |
| `results/case_pairs.json`, `case_studies/` | 7 pairs; 7/7 high-OPEN members broader (illustration only) | case studies |
| `ai_atlas/` | 37 concepts in 5 types | AI/CS atlas |
| `results/T7_rederivation.json`, `results/audit_headlines.json` | pipeline vs independent code: max diff <= 1e-16; all placebos fail | verification |
| `method_out.json` (+ `full_`, `mini_`, `preview_`) | 12,499 concepts + 7 pairs; validates against exp_gen_sol_out | downstream artifacts |

Bootstrap CIs are deterministic given the seeds. A different seed moves the CI ends by <= 0.004 (T5 in
`results/decomposition_dev.json`). The numba DTW kernel equals tslearn `cdist_dtw` exactly (T0 d). The HMM restarts
use fixed seeds, but BLAS thread counts can change the last digits of the log-likelihoods.
