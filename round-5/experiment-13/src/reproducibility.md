# Reproducibility

* Data: public OpenAlex S3 snapshot (manifest of 2026-09-23, 2,040 works files, `snapshot/works_manifest.json`), read by HTTP range requests (`lib/rangefile.py`); 0 OpenAlex API credits.
* Environment: Python 3.12, `requirements.lock.txt` (uv), spaCy `en_core_web_sm`.
* Order: `python method.py --from S0 --to S9 --run` (stages S0-S9, see README). Pass M ~3 min, Pass N ~16 min on 9 workers.
* Seeds:
  * bootstrap 20260929 (B = 2000; resampling unit: concept);
  * SIZEMATCH 1000+ci;
  * size-conditioned null 3000+ci;
  * year permutation 4000+ci;
  * rarefaction 5000+ci;
  * rewiring 31+r;
  * gate titles 7919+ci;
  * CV folds 0.
* LLM: OpenRouter; models google/gemini-2.5-flash-lite (M1), openai/gpt-4.1-mini (M2, G2); temperature 0; every response is cached in `llm_cache/`, so a re-run is free. Spend: $0.92.
* Seal: `logs/seal.log` is a sha256 hash chain (S0_prereg → S3_candidates → S3v2_candidates → S5_sealB → S6_features → S7_freeze → S7_power → S8_unseal → S8_outcomes → S8_scored → S9_audit). `lib/sealn.py` refuses a second unseal; scoring resumes from the hashed `data/outcomes_frame_n.parquet`.
* Checks:
  * unit tests T1/T3/T4/T5/T6/T8 are in `results/unit_tests.json`;
  * the independent audit, `results/audit.json`, matches to within 1e-9;
  * Pass-N base totals equal EXP10 `passC_totals.npz` exactly.
