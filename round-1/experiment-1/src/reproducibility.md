# Reproducing the naturalisation-gap screen (candidate L)

This is what was actually run, in order. All paths are relative to this artifact's folder.

## 1. Get the artifact
This workspace is published as one folder, `gen_art_experiment_1`, of the run's public GitHub repository:
```bash
git clone <repository-url>
cd <repository>/<path-to>/gen_art_experiment_1
```
The raw API response cache (`cache/`, 73 MB of hash-named files) is **not** published. The per-concept data the analysis actually reads (`results/concepts/<slug>/s2_raw.json.gz` and `bg.json.gz`) and `results/s0_raw.json` **are** published, so step 4 reproduces every reported number exactly without any API call.

No input from another artifact or from user uploads is used. The artifact pulls its own data.

## 2. System, Python and libraries
- The run used Ubuntu/Debian Linux in a 4-CPU container with a 29 GB RAM limit and **no GPU**.
- Python 3.12.14.
- `uv` 0.x; pip is not used.

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r <(python3 -c "import tomllib;print('\n'.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))")
```
`pyproject.toml` pins all 63 installed packages to the exact versions used. The main ones:
- numpy==2.5.3, pandas==3.0.6, scipy==1.18.1, scikit-learn==1.9.1;
- statsmodels==0.15.0, pymc==6.3.2, nutpie==0.16.11, arviz==1.3.0;
- loguru==0.7.3, requests==2.34.2, matplotlib==3.11.2, pyarrow==25.0.1, psutil==7.2.2, pytest==9.1.1.

## 3. Environment variables and keys (names only)
- `OPENALEX_API_KEY` is needed only to re-pull data (steps 5.2 and 5.4). It is never written to logs, cache keys or outputs.
- Semantic Scholar is used anonymously; no key is needed.
- No OpenRouter or LLM calls are made ($0).
- Optional: `OA_OWN_CAP` (default 3500) and `OA_SHARED_FLOOR` (default 1000) are the credit guards in `oa.py`.

## 4. Reproduce the reported numbers from the published data (no network)
```bash
.venv/bin/python -m pytest -q -c pytest.ini tests/          # T0 unit tests, 6 pass, ~1 min
.venv/bin/python method.py --splits 50 --n-boot 2000         # full screen, ~4-5 min on 4 CPUs
.venv/bin/python audit/rederive.py                           # independent re-derivation, ~1 min
```
To regenerate the method output variants, use the aii-json skill's formatter, or copy `method_out.json` to `full_method_out.json` and take the first 3 examples per dataset for the mini version:
```bash
python <aii-json-skill>/scripts/aii_json_format_mini_preview.py --input method_out.json
```

Seeds:
- The panel order uses `random.Random(20260928)`.
- Bootstraps, split halves, child sampling and parent thinning use 20260928 or seeds derived from it (e.g. SHA-1 of the child id XOR 20260928).
- The PyMC seed is 20260928 (4 chains x 1,000 draws, nutpie).

The re-runs were deterministic: two full runs gave identical statistics. The PyMC R-hat varies in the third decimal.

## 5. How the data were pulled (only needed to rebuild `results/concepts/` from scratch; counts drift daily)
1. **Unit tests** (as above).
2. **OpenAlex S0 pulls**, 139 credits in total. `panel.seeded_order()` gives the 78-concept order, and `s0.fetch_s0(Client(), order)` writes `results/s0_raw.json`:
   ```python
   import json; from oa import Client; from panel import seeded_order; from s0 import fetch_s0
   order = seeded_order(); open('results/panel_order.json','w').write(json.dumps(order, indent=1))
   open('results/s0_raw.json','w').write(json.dumps(fetch_s0(Client(), order)))
   ```
   On 2026-09-28 the shared daily pool dropped below the 1,000-credit sibling floor during this step. Yearly counts exist for all 78 concepts; OpenAlex topic-field windows exist for 11 dev concepts.
3. **Semantic Scholar pull**: `python fetch_s2.py`, about 70 min with anonymous rate limits. For each of the 53 dev-eligible concepts it writes `results/concepts/<slug>/s2_raw.json.gz`, containing:
   - all phrase-matched papers of t0-3..t0+4, up to 25,000;
   - a late-window t0+6..t0+8 field sample, capped at 3,000 in paperId-hash order;
   - citation lists for a seeded sample of at most 1,500 parents.
4. **Background references**: `OPENALEX_API_KEY=... python fetch_bg.py`, about 60 min, 0 credits. It uses free OpenAlex singleton GETs for children's reference lists and S2 MAG-id lookups for their fields, and writes `results/concepts/<slug>/bg.json.gz`.
5. **Analysis**: `python method.py --splits 50 --n-boot 2000`.

The per-call ledger of every OpenAlex response and its credits is in `logs/credits.csv`: 139 credits over 12,023 responses, most of them free singletons.

## 6. Expected outputs and numbers
`results/screen_result.json` (key: value):
- `n_used`: 48 dev concepts.
- `delta_rho`: **-0.0056**; `ci90`: [-0.034, 0.017]; `rho_B`: 0.834; `rho_BC`: 0.828.
- `n_pos_groups`: 0.
- `reliability.A_h.reliability_SB`: **0.58**.
- `size_corr`: vol 0.145, growth -0.177.
- `delta_auc_O1.delta`: -0.026.
- `field_level.delta`: +0.002, ci90 [-0.011, 0.016], 367 units.
- `M1.R2`: 0.659.
- `pymc_check.pass`: true (Spearman with REML 0.9996).
- `survives`: **false**. The clause results are in `clause_results`.

Other outputs:
- `results/features.csv`, `field_features.csv`, `outcomes.csv`, `field_outcomes.csv`, `dropped.csv`, and `screen_table.csv` (with OOF predictions).
- `results/figures/screen_overview.png`, with three panels: A*_h vs O2r, the M1 scatter, and reliability vs n.
- `method_out.json` and its `full_`, `mini_` and `preview_` variants, in the exp_gen_sol_out schema.
- `audit/rederive_out.json`: independently recomputed values, a shuffled-A*_h placebo (0% passing) and a positive-control power ladder.

In the paper these numbers belong to the RQ1 screening section, as the "naturalisation gap" candidate: the concept-level Delta-rho table, the field-level retention test and the reliability-vs-n curve.
