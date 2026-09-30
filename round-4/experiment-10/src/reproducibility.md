# Reproducing the fresh-cohort OPEN test (RQ1)

This file describes what was actually run for this artifact (AI Inventor run, iteration 4, `gen_art_experiment_10`,
plan `gen_plan_experiment_1_idx1`) on 2026-09-29. Every path below is relative to this folder.

## 1. Get the artifact and its sibling inputs

This workspace is published as one folder of a public GitHub repository. Clone the repository and `cd` into this
artifact's folder (`gen_art_experiment_10`). The code reads other run artifacts, which the repository publishes as
sibling folders. All of them resolve through ONE constant, `RUN_ROOT` in `lib/common.py`, which defaults to four levels
above this folder (the run-tree layout: `<RUN_ROOT>/3_invention_loop/iter_N/gen_art/<folder>`). Set the environment
variable `AII_RUN_ROOT` to the folder that contains `3_invention_loop/` if your checkout is laid out differently.

| input | artifact id / folder | what is read |
|---|---|---|
| EXP5 frame + scan | art_wxWssKSUR45f, `round-2/experiment-5/src` | `frame_concepts.csv`, `scan/agg_counts.parquet`, `scan/year_field_totals.npz`, `scan/reservoir/`, `scan/llm_cache/` (read-only cache lookup), `concept_features_basic.csv`, `grounding_precision.csv`, `results/backbones.json` |
| EXP8 indicators + frozen models | art_dFQ6jbgNsR6Q, `round-3/experiment-8/src` | `data/frame_matches_early/`, `data/ego_features.parquet`, `data/features_basic.parquet`, `data/outcomes.parquet`, `data/bg_topics.npz` (copied into `data/`), `data/analysis_table.parquet`, `results/indicator_matrix.parquet`, `results/frozen_spec.json`, `results/learned_model.json`, `models/*.joblib`, `inputs/` (copied into `inputs/`) |
| art_33 field backbone | `round-1/experiment-4/src` | `field_backbone.json` (`phi_min`, learned-model inputs only) |
| external recognition (declared dependency) | art_O7Dq4L02QnDN, `round-2/dataset-2/src` | `full_data_out/full_data_out_{1,2,3}.json` (Wikipedia creation years -> `fp_wiki_pre`) |

No user-uploaded file is used.

## 2. System, Python, libraries

* Ubuntu / Debian 12 container, Python **3.12.14**, [uv](https://github.com/astral-sh/uv), curl.
* Environment: `./restore.sh`. It runs `uv venv .venv --python=3.12` followed by
  `uv pip install --python .venv/bin/python -r requirements.lock.txt`. The same pins are in `pyproject.toml`.
* Key versions: numpy 2.5.3, pandas 3.0.6, pyarrow 25.0.1, scipy 1.18.1, scikit-learn 1.9.1, interpret 0.7.8,
  python-igraph 1.0.0, leidenalg 0.12.0, statsmodels 0.15.0, pyahocorasick 2.3.1, snowballstemmer 3.1.1,
  matplotlib 3.11.2, loguru 0.7.3, aiohttp 3.12.15. These are the EXP8 pins, so the frozen EXP8 joblib models unpickle.
* Hardware used: 11 vCPU (cgroup quota 10.2 CPUs), 57 GB RAM. The GPU (RTX A4500) was **not** used.

## 3. Data, credentials

* **OpenAlex works snapshot 2026-09-23.** It is read over HTTP range requests from the public S3 bucket
  `https://openalex.s3.amazonaws.com/data/parquet/works/`. The manifest in `snapshot/works_manifest.json` has 2,040
  files and is identical to EXP5's (checked against the live `manifest.json`, kept in `snapshot/current_manifest.json`).
  No API key is needed; **0 OpenAlex credits** were used.
* **LLM calls (OpenRouter).** Env vars `OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY` (names only). Models:
  google/gemini-2.5-flash-lite (precision gate + types) and openai/gpt-4.1-mini (type benchmark/fallback), temperature 0,
  JSON mode. The total was **$2.04** (`results/llm_cost_log.csv`). Every response is cached in `llm_cache/`, keyed by
  sha1 of (model, messages, temperature), so a re-run with the cache present makes no paid call.
* Optional: `AII_RUN_ROOT` (see 1) and `AII_JSON_SKILL_DIR` (AI Inventor JSON validator; `tests/test_output.py` falls
  back to a structural check).

## 4. Commands, in the order they were run (`method.py --list` gives the same order)

Seeds: bootstrap 20260929; SIZEMATCH draws 1000 + ci; control sample 7; EXP8 family-A nulls 20260928 + ci; benchmark
and gold-sheet samples 20260929 / 7 / 11.

```bash
./restore.sh
.venv/bin/python tests/test_output.py                       # U1
.venv/bin/python s0_prereg.py                               # S0 pre-registration -> logs/seal.log
.venv/bin/python s1_candidates.py                           # S1 1,535 candidates (t0 2015-17), 300 controls (<1 min)
.venv/bin/python passC.py --files 65,1125,1407 --workers 3  # 3-file test
.venv/bin/python passC.py --workers 9                       # S2 pass; run with 7, then 9, then 16 workers (resumable); ~30 min total
.venv/bin/python passC.py --merge                           # ~2.5 min
.venv/bin/python s7_ego.py --frame exp5 --builds all,home,sizematch --workers 2 --chunk 200   # 15 min
.venv/bin/python tests/t_ego_flags.py                       # U2 (run on the 100-concept --tag _u2 subset first)
.venv/bin/python s5_typing.py exp5                          # types v1, $0.31
.venv/bin/python s4_gate.py u8                              # U8
.venv/bin/python s6_covariates.py exp5
.venv/bin/python s3_checks.py                               # T1-T3 + S3 decision (TAG)
.venv/bin/python s4_gate.py run && .venv/bin/python s4_gate.py retry     # precision gate, $0.29
.venv/bin/python s7_ego.py --frame cohort --builds all,home,sizematch --workers 3 --chunk 50
.venv/bin/python s7_ego.py --frame cohort --builds full --workers 5 --chunk 20 --tag _full
.venv/bin/python s6_covariates.py cohort
.venv/bin/python s5_typing.py cohort && .venv/bin/python s5_typing.py bench && .venv/bin/python s5_typing.py sheet
#   the executor agent read results/type_gold_sheet_v1.csv blind -> results/type_gold_labels_v1.csv (copied to _v2)
.venv/bin/python s5_typing.py gate                          # gate v1 fails (method 0.73)
for c in exp5 cohort bench gate; do .venv/bin/python s5_typing.py $c --prompt v2; done   # gate v2 fails (method 0.80)
.venv/bin/python s5_typing.py m2all --prompt v2             # declared fallback -> data/concept_types.csv
.venv/bin/python tests/test_units.py && .venv/bin/python tests/t_outcomes.py   # U3, U4, U6, U7, U5
.venv/bin/python s8_select.py --nboot 500                   # S8 selection + power + FREEZE (~8 min)
.venv/bin/python s9_unseal.py --dryrun                      # synthetic counts, nothing unsealed
.venv/bin/python s9_unseal.py                               # the SINGLE unseal + scoring (~5 min)
.venv/bin/python s_learned.py validate && .venv/bin/python s_learned.py features && .venv/bin/python s_learned.py score
.venv/bin/python audit.py                                   # independent audit (~2 min)
.venv/bin/python make_outputs.py && .venv/bin/python make_report.py && .venv/bin/python readme_tables.py > results/readme_tables.md
.venv/bin/python rederive.py                                # short independent re-derivation of the headline numbers
```

`s9_unseal.py` refuses a second unseal (`logs/unsealed.json`). Re-running it only resumes scoring from the hashed
`data/outcomes_cohort.parquet`. To reproduce from scratch, delete `logs/unsealed.json`, `data/outcomes_cohort.parquet`
and `logs/seal.log`, then re-run from S0.

## 5. What you should get

| number | value | file |
|---|---|---|
| Verdict (frozen rule) | CONFIRMED (5/5 clauses) | `results/cohort_result.json` -> `verdict` |
| OPEN_home psp with O2r_m50 at R2 / R3 | +0.091 [+0.013, +0.171] / +0.080 [+0.001, +0.162], n = 573 | `results/cohort_result.json` -> `primary` |
| OPEN_all at R2; ALL minus HOME at R3 | +0.174 [+0.092, +0.253]; +0.093 [+0.016, +0.169] | `primary`, `contrasts` |
| DL pooled OPEN_home across 5 groups at R2 | +0.083 [-0.007, +0.173] | `groups` |
| Frozen B5 vs B5 + OPEN_home prediction (Spearman) | 0.768 vs 0.770 (+0.002 [-0.003, +0.008]) | `secondary.frozen_prediction_O2r_m50` |
| EXP8 ElasticNet gain over B5 on the cohort | +0.030 [+0.012, +0.049] | `results/learned_models_cohort.json` |
| Pre-seal power / MDE | 0.159 / 0.105 (with 2017) | `results/frozen_spec.json` -> `power` |
| Checks T1-T3 | exact (100% of cells) | `results/s2_checks.json` |
| Independent re-derivation | psp R2 0.0906 identical; shuffled-outcome q95 0.072 | `results/audit.json`, `results/rederive.json` |

Bootstrap CIs are percentile intervals from 2,000 concept resamples; `rederive.py` (400 draws) reproduces them within
Monte Carlo error. In the paper, these numbers belong to the RQ1 confirmation section: the ladder figure
`figures/fig_ladder.png`, the group forest `figures/fig_forest_groups.png`, the component figure
`figures/fig_components.png`, the within-type figure `figures/fig_within_type.png` and the measurement audit
`figures/fig_coverage_audit.png`.
