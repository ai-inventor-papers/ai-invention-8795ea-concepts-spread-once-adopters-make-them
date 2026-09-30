# Reproducing `gen_art_experiment_3` (co-occurrence screen: D and F vs B5)

This file describes what was **actually run** on 2026-09-28 to produce the published results. Every path below
is relative to this artifact's folder.

## 1. Get the artifact

This workspace is published as one folder of a public GitHub repository.

```bash
git clone <repository-url>
cd <repository>/<path-to>/gen_art_experiment_3     # this folder
```

The folder is self-contained. It reads no other artifact's outputs and no user-uploaded files.

## 2. System, Python and libraries

* **Hardware used:** Linux container (Debian 12, kernel 6.8), 4 CPU cores (AMD EPYC 9655), 29 GB RAM limit,
  **no GPU**. About 2 GB of RAM was in use at peak, plus about 5 GB during the snapshot scan.
* **System packages:** `curl`, `git` and `uv` (0.6.14 was used). Python **3.12.14**, installed through uv.
* **Environment** (the exact pinned versions are in `pyproject.toml`, from `uv pip freeze`):

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r pyproject.toml
```

  The key versions are numpy 2.5.3, pandas 3.0.6, scipy 1.18.1, scikit-learn 1.9.1, python-igraph 1.0.0,
  leidenalg 0.12.0, pyarrow 25.0.1, snowballstemmer 3.1.1 and matplotlib 3.11.2.
* The venv has no `pip` binary; use `uv pip ...`.

## 3. Data and credentials

| data | how it is obtained | credentials |
|---|---|---|
| OpenAlex snapshot metadata (`sources`, `topics`, `subfields`, `fields`; parquet, about 390 MB) | `./restore.sh`, which downloads from the public bucket `https://openalex.s3.amazonaws.com/data/parquet/...` into `snapshot/` | none |
| OpenAlex works snapshot (2,040 parquet files, 707 GB, **2026-09-23 release**) | never downloaded. `scan_snapshot.py` streams only 7 columns (about 25 GB) over HTTP range requests; `snapshot/works_manifest.json` lists the files | none |
| S0 yearly counts (78 concepts + global) | OpenAlex API, 156 credits. The raw responses are kept in `cache/` and replayed from there. | `OPENALEX_API_KEY` (env var), or `OPENALEX_ANON=1` for the public per-IP pool. Needed **only** if `cache/` is missing. |

* **API pool used.** The shared key named in the run had 0 daily credits left, so the counts were fetched with
  `OPENALEX_ANON=1` from the anonymous pool.
* **Drift.** OpenAlex counts drift over time. A fresh fetch or a later snapshot release will give slightly
  different numbers; the kept `cache/` and `scan/` reproduce the published ones exactly.
* **No LLM / OpenRouter calls** were made.

## 4. Commands, in the order they were run

All scripts derive their paths from `Path(__file__)`. The seeds are fixed in `config.py`: `SEED = 20260928`
(nulls, Leiden, bootstrap) and `random.Random(20260928)` for the processing order.

| # | command | what it does | runtime |
|---|---|---|---|
| 0 | `./restore.sh` (in the original run: the same curl downloads, then `uv venv` + install) | venv and snapshot metadata | ~1 min |
| 1 | `OPENALEX_ANON=1 .venv/bin/python s0_fetch.py` | OR-syntax test (`compressed`/`compressive` share the same stem, so the pipe syntax is frozen), global and per-concept yearly counts written to `results/yearly_counts_api.json` | ~1 min |
| 2 | `.venv/bin/python snapshot_meta.py` | venue-field labels (>= 40% rule; repositories unlabelled) in `results/source_field.parquet`; topic metadata | ~1 min |
| 3 | `.venv/bin/python scan_snapshot.py --workers 6` | full scan of all 476,196,327 works: `scan/ckpt.npz` and title matches (resumable). It was run as pilots `--limit 6`, then `--limit 40`, then the full scan. The 239 MB `scan/matches.jsonl` was afterwards split with `split -d -a 1 -n l/3 --additional-suffix=.jsonl scan/matches.jsonl scan/matches/matches_` (a byte-identical concatenation) | ~17 min |
| 4 | `.venv/bin/python s0_outcomes.py` | onset, dev restriction, O1 / O2r / O3 / R_j, B5, in `results/outcomes.csv` and `results/field_outcomes_base.csv` | 10 s |
| 5 | `.venv/bin/python backbone.py` | PMI backbones, Leiden gamma grid (primary gamma 3.0; plan rule 1.0), alignment, in `backbone/` and `results/topic_communities.csv` | ~8.5 min |
| 6 | `.venv/bin/python features.py --workers 4` | ego features, D / F nulls (1,000 draws), rivals, 50 paper-level split halves | ~3 min |
| 7 | `.venv/bin/python screen.py --n_boot 2000 --workers 4` | the pre-registered screen, written to `results/screen_result.json` | ~3 min |
| 8 | `.venv/bin/python screen.py --n_boot 2000 --workers 4 --seed 20260929 --tag _seed2`, then `.venv/bin/python t6_check.py` | T6 bootstrap-seed stability (max CI endpoint difference 0.0125) | ~3 min |
| 9 | `.venv/bin/python extra_analyses.py` | EXPLORATORY out-of-group partial association | ~1 min |
| 10 | `.venv/bin/python make_outputs.py` | `figures/*` and `method_out.json` | 15 s |
| 11 | `.venv/bin/python method.py --from s0_outcomes` | reruns steps 4-10 end to end; the result was **bit-identical** to the step-by-step run | ~17 min |
| 12 | `.venv/bin/python tests/test_synthetic.py` | T0 synthetic unit tests, in `results/unit_tests_T0.json` (5/6 pass; see below) | 30 s |
| 13 | `.venv/bin/python audit.py` | independent re-derivation, placebo and positive control, in `results/audit.json` | ~1.5 min |
| 14 | AI Inventor's internal `aii_json_format_mini_preview.py --input method_out.json` | writes `full_` / `mini_` / `preview_method_out.json`. This is an internal tool: `full_method_out.json` has the same content as `method_out.json`, and mini/preview are truncations. | seconds |

Shortcut: `.venv/bin/python method.py` runs steps 1-10. Cached steps are skipped, so no credits are used when
`cache/` and `results/yearly_counts_api.json` exist.

## 5. What you should get

These are all in `results/screen_result.json`, `results/exploratory_partial_association.json`,
`results/audit.json` and `method_out.json` (metadata). They are the numbers for the paper's RQ1 screening of
co-occurrence candidates: the table of candidate incremental value over B5 and the per-field-group forest plot
`figures/delta_rho_forest.pdf`.

* **Panel.**
  * 78 concepts: 22 are outside the t0 cohort and 9 have a home outside the dev fields, which leaves **47 dev
    concepts** (BIO 16, CS 12, MED 10, ENG 9), all with O2r.
  * Base rates: O1 0.74, O3 0.085.
* **B5 baseline.** LOGO Spearman with O2r **0.770**; AUC 0.80 for O1 and 0.86 for the top tercile of O2r.
* **D (`D_ratio`)**
  * Delta-rho **+0.006**, 90% CI [-0.092, 0.135];
  * per group: BIO +0.185, CS +0.014, ENG -0.083, MED +0.012;
  * split-half SB 0.83; size rho 0.11 (log volume) and 0.02 (growth);
  * **does not survive**.
* **F (`F_res`)**
  * Delta-rho **-0.060**, 90% CI [-0.158, 0.014];
  * 1 of 4 groups positive; SB 0.44;
  * **does not survive**.
* **`D_z` (the plan's literal primary)**: Delta-rho +0.017, rho with log volume **-0.63**, so it fails as a size
  relabel.
* **Other tests.**
  * Dissociation tests: both inconclusive.
  * O3 and the reach30 hurdle: not estimable.
  * Field-level R_j: dAUC +0.000 for Dj and -0.008 for Fj.
* **Exploratory, not pre-registered.** Out-of-group partial rho of D_ratio given B5 is **+0.335**, 90% CI
  [0.02, 0.65]. Its permutation p-value is 0.037, so the evidence is marginal.
* **Audit** (`results/audit.json`):
  * every headline number above is re-derived exactly by independent code (sklearn pipelines, exact `math.comb`
    rarefaction from the raw title matches);
  * permuted candidates never reach Delta-rho >= 0.10 (0 of 200);
  * a planted feature does reach it (Delta-rho 0.114).
* **T0 tests.** One of six fails its tolerance: the F null has a small negative bias (-0.14, 0.3 SD) under pure
  growth.

The bootstrap CIs depend on the seed. With `--seed 20260929` they move by at most 0.0125.
