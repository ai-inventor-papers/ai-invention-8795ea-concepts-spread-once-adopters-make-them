# Reproducing this artifact (Ubuntu, Python 3.12, CPU only, 0 OpenAlex credits)

1. Install uv, then create the environment:
   `uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python requests numpy pandas scipy scikit-learn statsmodels networkx loguru matplotlib pyarrow`
2. Download the free OpenAlex S3 sources snapshot (~370 MB on disk, no credits): `bash snapshot/download_sources.sh`
3. Run the unit tests: `.venv/bin/python tests/test_units.py` (rarefaction vs Monte Carlo, Kleinberg spike).
4. Run the analysis offline from the frozen API cache `cache/raw/`: `.venv/bin/python method.py` (about 6 min on 4 CPUs). It writes
   outcomes.csv, field_outcomes.csv, features.csv, single_indicators.csv, screen_result.json, method_out.json,
   field_backbone.json, next_field_entry.csv and figures/. All seeds are fixed (20260928, 1, 7, 11, 12), so the results are bit-identical.
5. `.venv/bin/python make_variants.py` writes full_/mini_/preview_method_out.json.

Re-pulling raw data (only if `cache/raw/` is lost; OpenAlex counts drift day to day, so the numbers will differ slightly):
`export OPENALEX_API_KEY=<key>; .venv/bin/python s0_ground.py; .venv/bin/python pull_data.py A; .venv/bin/python pull_data.py backbone; .venv/bin/python pull_data.py BD`
(about 290 credits). `pull_data.py C|insularity|p5` are the stages this run could not afford: the shared key was below its 1,000-credit floor.
