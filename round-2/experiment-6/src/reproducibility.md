# Reproducibility: how concepts hop between fields (`gen_art_experiment_6`)

All paths below are relative to this artifact's folder.

## 1. Get the artifact

This folder is one directory of the run's public GitHub repository.

```bash
git clone <repository-url>
cd <repository>/<path-to>/gen_art_experiment_6
```

The published repository does **not** contain these files:
* the per-file scan outputs (`scan/pass1/`, `scan/pass2/m*.npz`), which are regenerable (section 4);
* any file of 100 MB or more.

The kept aggregates (`scan/agg_counts.npz`, `scan/pass2/{w,h}*.parquet`) are enough to rerun every analysis in steps
5-9 below without rescanning.

## 2. System and Python

* Ubuntu 22.04 or later, with `curl` and `git`.
* [uv](https://docs.astral.sh/uv/).
* Python 3.12. No GPU is needed; everything ran on 4 CPU cores with a 32 GB container limit.

```bash
bash install.sh
```

This creates `.venv` with Python 3.12, installs the CPU wheel of torch 2.14.0, then installs `requirements.lock.txt`.
The lock file holds all 85 packages, and the same pins are listed in `pyproject.toml`. The main ones: pyarrow 25.0.1,
numpy 2.5.3, pandas 3.0.6, scipy 1.18.1, scikit-learn 1.9.1, statsmodels 0.15.0, networkx 3.7, pyahocorasick 2.3.1,
tslearn 0.9.0, hmmlearn 0.3.3, ruptures 1.1.10, kmedoids 0.5.5, sentence-transformers 6.1.0, openai 3.20.0,
wordfreq 3.1.1 and matplotlib 3.11.2.

## 3. Data, models and keys

* **OpenAlex works snapshot.** `s3://openalex/data/parquet/works`, read anonymously over
  `https://openalex.s3.amazonaws.com/`. There are no downloads to disk: column chunks are fetched with HTTP range
  requests. The file list used is `inputs/works_manifest.json` (2026-09 release; 2,040 files; 476,196,327 works).
  Later releases drift, so exact counts may differ slightly.
* **OpenAlex concepts entity.** `inputs/concepts/`, from `data/parquet/concepts`.
* **Inputs from iteration-1 artifacts** of this run, copied into `inputs/`:
  * `field_backbone.json`, `outcomes.csv` and `field_outcomes.csv` from artifact `gen_art_experiment_4` (iteration 1);
  * `source_field.parquet` from artifact `gen_art_experiment_3` (iteration 1).
* **Model.** `sentence-transformers/all-MiniLM-L6-v2`, downloaded automatically from the HuggingFace Hub.
* **Environment variables (names only).**
  * `OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY`: needed only for the two labelling commands.
  * `OPENALEX_API_KEY`: optional, for `audit_api.py`; without it the anonymous pool is used, which is what this run
    did.
* **User uploads.** None of the run's uploads are used by this artifact.

## 4. Commands actually run, in order

Seed: `SEED=20261001` (`config.py`). Hardware: 4 CPU cores, no GPU. Runtimes are wall-clock on that machine.

| # | command | what it does | runtime |
|---|---|---|---|
| 1 | `.venv/bin/python build_lexicon.py` | legacy-concept lexicon (60,859 concepts) and its SHA-256 | 10 s |
| 2 | `.venv/bin/python pass1.py --workers 4` | title hits and tag flags for all 2,040 files -> `scan/pass1/` | 23 min |
| 3 | `.venv/bin/python aggregate.py` | -> `scan/agg_counts.npz` | 1 min |
| 4 | `.venv/bin/python cand.py` | P0 prefilter; 12,901 onsets, 653 newborn candidates | 10 s |
| 5 | `.venv/bin/python pass2.py --workers 4` | refs, authors, titles of candidate works + global id -> field map | 13 min |
| 6 | `.venv/bin/python grounding.py sample` | 400 stratified benchmark pairs | 1 min |
| 7 | `.venv/bin/python label_bench.py --model google/gemini-2.5-flash-lite --out benchmark/labels_primary.csv` | LLM labels | 1 min |
| 8 | `.venv/bin/python label_bench.py --model qwen/qwen3-30b-a3b-instruct-2507 --n 150 --out benchmark/labels_second.csv` | second labeller | 1 min |
| 9 | (manual) `benchmark/hand_labels.csv` | 60 pairs labelled by hand | - |
| 10 | `.venv/bin/python grounding.py fit` | rule comparison, sense filter, per-concept precision | 7 min |
| 11 | `.venv/bin/python frame.py` | frame (653 concepts), episodes; held-out outcomes sealed | 20 s |
| 12 | `.venv/bin/python agreement.py` | agreement with iteration 1 | 5 s |
| 13 | `.venv/bin/python audit_api.py` | 40 API calls on the anonymous pool | 1 min |
| 14 | `.venv/bin/python method.py dev` | dev analyses | 5 min |
| 15 | `.venv/bin/python method.py freeze` | writes `results/frozen_spec.json` and its hash in `results/freeze_log.txt` | 1 s |
| 16 | `.venv/bin/python method.py heldout` | held-out analyses, run ONCE | 10 min |
| 17 | `.venv/bin/python method.py outputs` | figures and `method_out.json` | 1 min |
| 18 | aii-json `aii_json_format_mini_preview.py --input method_out.json` | full, mini and preview variants | 1 min |
| 19 | `.venv/bin/python audit.py` | independent audit | 1 min |
| 20 | `.venv/bin/python audit_placebo.py` | independent audit with placebos | 3 min |
| 21 | `.venv/bin/python tests/test_units.py` | T0 unit tests | 1 min |

Resampling counts:
* 2,000 concept bootstraps;
* 1,000 joint label permutations and 1,000 g-only permutations;
* 200 rewired backbones;
* 100 DTW bootstrap resamples;
* 200 change-point calibration shuffles;
* 200 lead-lag placebos.

The environment variables `AII_NBOOT`, `AII_NPERM` and `AII_NREWIRE` were used only for debugging runs, never for the
reported results. Step 15 was executed twice, 0.2 s apart (identical spec apart from the timestamp; both hashes are
logged), before step 16.

To restore removed intermediates:
* `scan/pass1/`: `.venv/bin/python pass1.py --workers 4`;
* `scan/pass2/m*.npz`: `.venv/bin/python pass2.py --idmap-only`.

## 5. Expected outputs and numbers

**Main files.**
* `results/heldout_result.json`: held-out analyses (`H2_pooled`, `H2_per_group`, `H2_DL_pooled`, `decisions`).
* `results/dev_result.json`: dev analyses.
* `method_out.json` / `full_method_out.json`: 84,511 examples across 4 datasets.
* `figures/`: all figures.

**Headline numbers.** Each is in the results table of the paper's RQ2 / next-field-entry section.

| quantity | value | file / key |
|---|---|---|
| held-out LR, M2 vs M0 | 71.72 (p = 2.5e-17) | `heldout_result.json` H2_pooled.LR |
| held-out d | 0.302, bootstrap CI [0.240, 0.369] | `heldout_result.json` |
| g-only permutation (M3 vs M1) | p = 0.173 | `heldout_result.json` gonly_perm_null_M3_vs_M1 |
| label permutation | p = 0.001 | `heldout_result.json` |
| rewired backbone | p = 0.015 | `heldout_result.json` |
| DL pooled d | 0.284 [0.216, 0.352], I2 = 0 | `heldout_result.json` H2_DL_pooled |
| frozen-coefficient AUC, M0 -> M2 | 0.807 -> 0.815 | `heldout_result.json` frozen_dev_coef_auc |
| ordering p_gw | 0.655 (57 before, 30 after, 15 ties; sign p = 0.0025) | `heldout_result.json` ordering |
| ordering, peripheral share | 0.570 | `heldout_result.json` ordering |
| rescue R1 interaction | -0.217 [-1.12, 0.68] | `heldout_result.json` rescue_relay |
| relay fepois, retained x gateway | -1.30 [-4.93, 2.33] | `heldout_result.json` rescue_relay |
| dev trajectories | k = 2, bootstrap ARI 1.0 | `dev_result.json` trajectories |
| held-out independent recluster ARI | 0.54 | `heldout_result.json` trajectories |

**Independent checks.**
* `results/audit.json`: R1 and p_gw agree exactly.
* `results/audit_placebo.json`:
  * the exact-likelihood H2 LR is 77.3 (d 0.34); the pipeline's Breslow form gives 71.7, the conservative value;
  * the exact DL-pooled d is 0.32 [0.25, 0.39];
  * labels shuffled within strata reject in 0 of 20 runs at p < 0.01;
  * a random gateway year gives an ordering share of 0.43, never at or above 0.655;
  * the sklearn AUCs equal the pipeline's.
* `results/unit_tests_T0.json`: all tests pass.

**Spend.** OpenRouter $0.0074 over 550 calls (`results/openrouter_cost.json`). OpenAlex: 40 anonymous credits
(`results/credits_log.csv`).
