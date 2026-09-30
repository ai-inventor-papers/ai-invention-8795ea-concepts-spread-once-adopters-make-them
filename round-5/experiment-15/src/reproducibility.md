# Reproducibility

- **Environment**: Python 3.12, `uv`; exact pins in `requirements.lock.txt` (same versions as Exp11: numpy 2.5.3,
  pandas 2.3.3, scipy 1.18.1, statsmodels 0.15.0, pyfixest 0.60.0, lifelines 0.30.3, igraph 1.0.0, networkx 3.7).
  `source env.sh` before any run: one BLAS/OpenMP/MKL/numba thread per process (the fix for the Exp11 event-study
  crash) and `AII_RUN_ROOT` (the run root; default four levels above this directory).
- **Hardware used**: 4-CPU container (cgroup quota), no GPU; peak RSS < 2 GB per process.
- **Seeds**: 20260929 everywhere (bootstrap, placebo, CV folds); the sealed Exp11 code keeps its own seeds.
- **Spend**: $0 LLM, 0 OpenAlex credits, no network access; all inputs are read-only files of earlier artifacts of
  this run (Exp11, Exp10, EXP8, EXP5 frames; see README "How to run").
- **Seals**: Exp11 seal verified on the original files (`results/seal_verification.json`, 21/21). Part A/B spec +
  feature hashes sealed before any outcome join (`results/frozen_spec_iter5.json`, `logs/seal_iter5.log`); code
  changes after the seal are listed in `results/code_sha256_final.json` and `results/deviations.json`.
- **Gates**: G0 seal hashes; G1 DEV point estimates == Exp11 (diff 0.0); G2 HOME build == Exp10 on every concept
  (diff 0.0, NaN pattern equal); decomposition identities < 1e-12; Exp10 published cohort psp reproduced (1e-16);
  unit tests `results/unit_tests_iter5.json` and `exp11_code/results/unit_tests.json` all pass.
- **Commands** (about 3 h on 4 CPUs in total):
  ```bash
  uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r requirements.lock.txt
  source env.sh
  .venv/bin/python method.py --workers 4    # all stages; finished stages are skipped
  .venv/bin/python tests/test_iter5.py
  .venv/bin/python make_readme.py
  ```
- **Recorded runtimes**: body models 5 min; event study 90 min (3 workers, shared CPU); sequence 104 min; H-P1
  scoring 9 min; HOME builds 1.5 min + 0.3 min + 2 min; Part A scoring 17 min (2,000 boots); Part B 7 min.
