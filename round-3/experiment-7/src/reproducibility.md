# Reproducibility

- **Environment:** Python 3.12. `bash install.sh` creates `.venv` from `requirements.lock.txt` (uv).
  - All numerics run on CPU; no GPU is needed.
  - BLAS threads are pinned to 1. Parallelism is a deterministic thread map over pre-drawn resamples.
- **Seeds:** SEED = 20261101. Each analysis draws from `np.random.default_rng([SEED, crc32(tag)])`.
  - A second-seed bootstrap moves the d0 CI endpoints by at most 0.004 (T6).
- **Inputs (read-only, by path under the run tree):**
  - EXP6 `iter_2/gen_art/gen_art_experiment_6`:
    - `scan/frame_g_*.npz`, `scan/frame_gpf_*.npz`, `scan/agg_counts.npz` (the GF key only);
    - `inputs/field_backbone.json`;
    - `results/frame_concepts.csv`, `lexicon.parquet`, `entry_risk_sets_*.parquet`, `frozen_spec.json`.
  - EXP5 `iter_2/gen_art/gen_art_experiment_5`:
    - `frame_concepts.csv`, `grounding_report.json`;
    - `scan/agg_counts.parquet`, `scan/year_field_totals.npz`, `scan/co_by_year.npz`.
  - Dataset `art_O7Dq4L02QnDN`: `full_data_out/full_data_out_{1,2,3}.json`, concept_recognition only.
- **Order:**

  ```bash
  python tests/test_units.py
  python method.py step1 && python method.py dev && python method.py freeze
  python method.py heldout
  python audit.py && python exploratory_lpm.py && python method.py   # default stage = outputs
  ```

  Wall times: step1 2 min, dev 21 min, heldout 15 min, audit 3 min, outputs 2 min on 10 vCPU.
- **Sealing:** `method.py heldout` refuses to run unless `logs/seal.log` matches the sha256 of
  `results/frozen_spec.json` and of every analysis `.py` file, and refuses a second unseal.
  - To re-run the held-out stage in a fresh clone, delete `logs/unseal.log`. The spec and code hashes must still
    match.
  - Frozen spec sha256: `345d391b73f2fb134cdc5551ba002a335ee0361668b4500e9690b2b44959d60d`.
  - Pre-freeze git commit: `24da538`.
- **Determinism:** risk sets and every point estimate are deterministic. Bootstrap, permutation and power results are
  deterministic given the seed and N (`AII_*` environment overrides are for smoke runs only).
- **Spend:** $0 of LLM calls and 0 OpenAlex API calls.
