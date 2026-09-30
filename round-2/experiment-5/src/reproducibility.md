# Reproducibility

This file describes what was **actually run** (2026-09-28, 17:08–19:20 UTC) and how to reproduce it on Ubuntu.

## 1. Get the artifact

This workspace is published as one folder of a public GitHub repository.

```bash
git clone <repository-url>
cd <repository>/<this-artifact-folder>        # the folder holding this file
```

**Inputs from other artifacts (read-only).** They are resolved in `common.py` by `_dep_dir()`, in this order:
1. the environment variable;
2. the pipeline run tree;
3. a sibling folder of the repository named by the artifact id.

| artifact id | env var | files used |
|---|---|---|
| `art_yrradSC27HtQ` | `AII_ART_YRRAD_DIR` | `results/source_field.parquet` (source → venue field), `config.py` + `scan/matches/*.jsonl` + `scan/ckpt.npz` + `results/outcomes.csv` (T1/T3 checks only) |
| `art_33_KKk_G8Gw5` | `AII_ART_33_DIR` | `field_backbone.json` (the frozen 1998–2002 gateway vector, φ, φ_min, n_field), `outcomes.csv` (P78 names) |

No user-uploaded file is used. The run's `user_uploads/` folder is private and is not published.

## 2. System, Python, environment

- **Hardware:** Ubuntu container, 4 vCPU (cgroup quota), 32 GB RAM, **no GPU**. MiniLM embeddings ran on CPU.
- **Software:** Python **3.12.14** and `uv` (any recent version); no other system packages.
- **Environment:** every library is pinned in `pyproject.toml` (75 packages, e.g. numpy 2.5.3, pandas 3.0.6,
  pyarrow 25.0.1, scikit-learn 1.9.1, statsmodels, networkx, pyahocorasick, snowballstemmer,
  sentence-transformers 6.1.0, torch 2.14.0+cpu).
- **Set-up:** `./restore.sh`. It runs:
  - `uv venv .venv --python=3.12`;
  - `uv pip install -r pyproject.toml` (with the PyTorch CPU index);
  - the download of `snapshot/` (the works and concepts manifests and the 12 legacy-concepts parquet files) from
    `https://openalex.s3.amazonaws.com/data/parquet/`.

  Use the **2026-09-23** release for identical numbers. The live manifest may be newer.

## 3. Data, models, keys (names only)

- **Data:** the OpenAlex S3 works snapshot, read over plain HTTPS range requests. No credentials and no API
  credits are needed. The legacy concepts entity also comes from the S3 snapshot.
- **Aliases:** Wikidata aliases from the public SPARQL endpoint (no key).
- **Model:** `sentence-transformers/all-MiniLM-L6-v2`, downloaded automatically from the Hugging Face hub (no key).
- **LLM labelling** (`grounding.py bench|precision`) needs the env vars `OPENROUTER_API_KEY` and
  `OPENROUTER_BASE_URL`. Models:
  - `google/gemini-2.5-flash-lite` (labeller 1 and the precision gate);
  - `openai/gpt-4.1-nano` (labeller 2);
  - `google/gemini-2.5-flash` (adjudicator).

  Temperature is 0. Spend was **$2.28** over 13,760 calls (`llm_cost_log.csv`). A rerun reads
  `scan/llm_cache/` (kept on the run volume) and costs nothing; without the cache, LLM labels may differ slightly.
- **OpenAlex API:** `OPENALEX_API_KEY` (optional) is read from the environment and never written to disk. It was
  NOT used for data: the pool was below the floor, and only 2 probe calls were made.

## 4. Commands, in the order they were run

Seed: **20260928** everywhere (plus fixed offsets). All commands run from this folder with
`.venv/bin/python` (written `py` below). `py method.py` runs the whole chain and skips steps whose outputs exist.

| # | command | runtime (4 vCPU) | output |
|---|---|---|---|
| 0 | `py probe.py`; `py timing_probe.py` | 1 min | `logs/schema_leaf_paths.json`, `logs/timing_probe.json` (legacy tags present, so HAVE_TAGS) |
| 1 | `py lexicon.py` | 10 s | `lexicon_v0.parquet` (64,209 concepts); sha256 in `frozen_lexicon.sha256` |
| 2 | `py prescreen.py sample`; `py prescreen.py names` | 1 min | 20 random files (1.1% of works); 7,566 concepts dropped, 56,643 survive |
| 3 | `py wikidata_aliases.py`; `py prescreen.py aliases` | 8 min | `lexicon_v1.parquet` (85,692 alias forms); sha256 = **last** line of `frozen_lexicon.sha256` (b9f410fa…) |
| 4 | `py scan_full.py --files 1407,1125,65 --workers 3`, then `--limit 3` | 1 min | stage-1 timing (outputs moved to `scan/stage_test_parts/`) |
| 5 | `py scan_full.py --workers 5` (T2 inspection at 50 files, then a restart after the lexicon fix, see `results/deviations.json: t2_lexicon_fix`) | 33 min | per-file parts, 2,040/2,040 files, 0 failures |
| 6 | `py scan_full.py --merge` | 2 min | `scan/agg_counts.parquet`, `scan/reservoir/part_*.parquet` (split < 100 MB), `scan/*.npz`: 476,196,327 works; 129,360,390 base; 60,011,338 verified matches |
| 7 | `py frame.py match`; `py backbones.py` | 30 s | 14,935 match onset candidates; recomputed S0 vs frozen ρ = 1.000 |
| 8 | `py grounding.py bench` | 20 s | 390 labelled pairs, κ = 0.20, so adjudicated |
| 9 | the executor read 60 pairs by hand | manual | `results/handcheck_labels.csv` (90% agreement with gold) |
| 10 | `py grounding.py filter` | 5 min | frozen rule **TAG** (test P 0.947, R 0.659) |
| 11 | `py frame.py grounded`; `py grounding.py precision` | 15 min | 13,413 candidates, 93% pass precision ≥ 0.8 |
| 12 | `py frame.py build`; `py features.py` | 30 s | **12,499 concepts, 27,393 episodes**; held-out outcome columns blank |
| 13 | `py tests/test_units.py`; `py checks.py t1`; `py checks.py t3` | 2 min | T0 9/9 pass; T1 recall 0.95 / precision 1.0; T3 ρ 0.999, t0 agreement 53% |
| 14 | `SMOKE=1 py models.py dev`; `SMOKE=1 py models.py smoke_heldout` | 3 min | smoke only (dev data), no freeze |
| 15 | `py models.py dev` | 4 min | `results/h1_dev.json`, **`frozen_spec.json`** (sha256 147ce58a…), FREEZE + T6 in `logs/seal.log`, git commit a3234b7 |
| 16 | `py seal.py unseal` (exactly once) | 25 s | held-out/cohort outcomes, `sens_episodes_*.csv`, UNSEAL line |
| 17 | `py models.py heldout` (first run crashed on one undefined cohort outcome; fixed and rerun, spec unchanged) | 9 min | `results/h1_heldout.json`, `results/h3_results.json` |
| 18 | `py fix_pigeonhole.py`; `py checks.py replicate`; `py exploratory_domains.py` | 2 min | crossed-bootstrap fix, iteration-1 replication, exploratory per-domain table |
| 19 | `py report.py`; aii-json format script (full/mini/preview); `py audit.py`; `py audit_placebo.py` | 5 min | figures, `method_out.json` + variants, `audit.json`, `results/audit_placebo.json` |

The seal refuses a second unseal. Reproducing the confirmatory part from scratch therefore needs a fresh workspace:
steps 15 → 16 → 17 in order, with a new freeze.

## 5. Expected outputs and numbers

| number | value | file |
|---|---|---|
| frame | 12,499 concepts / 27,393 episodes (DEV 9,079; held-out 8,515; cohort 9,798 defined) | `results/frame_summary.json` |
| DEV ΔAUC (gateway over X0, LOGO) | +0.00001 [−0.0007, +0.0005]; AUC(X0) 0.866 | `results/h1_dev.json → primary` |
| **HELD-OUT ΔAUC** | **−0.00001 [−0.0006, +0.0003]**; AUC(X0) 0.837 | `results/h1_heldout.json → primary` |
| DL pooled over 4 held-out groups | −0.00004 [−0.0004, +0.0003], I² = 0 | `→ dl_pool` |
| cohort ΔAUC | −0.0001 [−0.0008, +0.0001] | `→ cohort` |
| relatedness pair vs gateway (held-out) | +0.0034 [0.0010, 0.0051] vs −0.00005 | `→ rival_head_to_head` |
| ladder: gateway over the iteration-1 base | DEV +0.0019 [0.0005, 0.0034]; HELD-OUT −0.0016 [−0.0035, −0.0002] | `→ ladder`, `figures/ladder_dauc.png` |
| power (80%) | minimum detectable ΔAUC 0.004 | `results/h1_dev.json → power` |
| **H1 verdict** | **DISCONFIRMED** | `→ verdict_H1` |
| H3 partial ρ (held-out, G / G_A / G_btw) | 0.030 / 0.026 / 0.046, Holm p = 0.0045; per-group DL pooled G 0.068 [0.029, 0.107] | `results/h3_results.json` |
| iteration-1 replication (P78 subset) | +0.023 [−0.004, +0.068] (iteration 1: +0.10) | `results/checks.json` |
| independent audit | all match to 1e-6 | `audit.json` |
| shuffled-input controls | shuffled-R held-out ΔAUC −0.0005 ± 0.0019; planted 1-SD gateway effect detected (+0.044); H3 tests 0/40 false positives on shuffled outcomes | `results/audit_placebo.json` |

In the paper, these numbers belong to the H1 (gateway retention) held-out results table, the forest plot
(`figures/forest_dauc.pdf`), the baseline-ladder figure (`figures/ladder_dauc.pdf`) and the H3 paragraph.
