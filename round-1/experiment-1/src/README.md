# GEN_ART, iteration 1, experiment 1: naturalisation-gap screen (candidate L)

**Question.** When fields other than a concept's home field adopt it early, do they cite it as their own literature, and does that predict how widely it spreads later? The measure is the background-adjusted naturalisation gap A*_h. It is computed field by field and partially pooled across concepts.

The screen uses the frozen dev panel P78 under the pre-registered survival rule. Ground truth is O2r, the rarefied field breadth of papers in t0+6..t0+8, plus O1 (uptake), O3 (transience) and field-level retention R_j. Every result is compared with the common count baseline B5.

## Result: candidate L does NOT survive the pre-registered rule
The panel has 48 dev concepts:
- 13 in Biochemistry/Genetics/Molecular Biology, 21 in CS, 3 in Engineering and 11 in Medicine;
- 42 of them are newborn.

Of the 78 panel concepts, 22 were dropped for t0 outside 2003-2009 and 8 for a sealed home field.

| Clause (pre-registered) | Value | Pass |
|---|---|---|
| Delta-rho(O2r) >= 0.10 and 90% CI lower bound > 0 | **-0.006**, CI [-0.034, 0.017] (rho_B5 = 0.834, rho_B5+A*_h = 0.828); refit bootstrap CI [-0.092, 0.023] | no |
| Gain positive in >= 3 of 4 left-out groups | 0: Biochem 0.000, CS -0.003, Medicine 0.000; Engineering has n = 3, too few | no |
| Split-half reliability of A*_h >= 0.6 | **0.58** (50 splits, Spearman-Brown) | no, narrowly |
| Size: abs(Spearman) with log early volume and with early growth <= 0.6 | 0.14 / 0.18 | yes |

Other findings:
- **B5 alone predicts breadth very well** out of field (rho = 0.83). A*_h is unrelated to O2r overall (Spearman -0.01).
  - Its within-field sign flips: +0.45 in Medicine, -0.18 in CS, -0.08 in Biochem. This is domain-specific, not a general signal, and is reported as a negative generalisation result.
- **O1 uptake:** Delta-AUC is -0.026, CI [-0.084, 0.028].
- **O3 transience:** only 4 of 48 concepts are positive, so O3 cannot be evaluated.
- **Field-level test (rho*_cj -> R_j):**
  - 367 concept x field units from 46 concepts; AUC 0.853 -> 0.855, Delta +0.002, CI [-0.011, 0.016].
  - Units with stage-1 data only (n = 186): Delta -0.010.
  - The naturalisation contrast does not predict which adopting fields keep the concept.
- **Reliability vs n:** 0.34 (< 15 off-home children), 0.37 (15-29), 0.04 (30-59) and 0.72 (60+), so the eligibility threshold is 60. On the 11 eligible concepts, Delta-rho = +0.118 with CI [0.000, 0.355], underpowered with no evaluable group. This is suggestive at best.
- **M1:** raw lineage log-OR ~ background log-OR gives R^2 = 0.66, CI [0.39, 0.83].
  - The background log-OR is positive for 48 of 48 concepts and at least as large as the raw concept log-OR in 77% of them.
  - This confirms the probe: raw lineage "autonomy" is mostly citation homophily.
- **Pooling:**
  - REML gives tau_c = 0.29 and tau_cj = 0.65, so most variation is concept x field, not concept.
  - The PyMC NUTS check passes (R-hat 1.010, Spearman with REML 0.9996, 0 divergences).
  - The one-stage GLMM, with discretised labels and one link per child, agrees only weakly (Spearman 0.16).
- **Foils scored as candidates, all exploratory:** no foil reaches Delta-rho 0.10.
  - The closest are self_share at +0.028, CI [-0.005, 0.065], and A*_h_MH at +0.016.
  - relay_share correlates 0.70 with O2r, and 0.71-0.81 within every group, yet adds nothing over B5 (-0.012). It is redundant with early breadth.
- **Cross-source S0 check** on the 11 concepts with OpenAlex S0: Spearman(O2r from OpenAlex topics, O2r from S2 fields) = 0.87.
  - Home fields agree exactly for 9 of 11 concepts. For cancer stem cell S2 adds Biology to the OpenAlex home, Medicine; WiMAX is Engineering in OpenAlex and CS in S2.
- **Probe agreement** on the 5 overlap concepts: optogenetics -0.54 vs the probe's -0.55, and extreme learning machine -0.89 vs -1.06. Signs flip for crowdsourcing, iPSC and compressed sensing, whose probe CIs spanned 0 or were wide. Spearman is 0.40 for the crude values and 0.10 for pooled A*_h, reflecting the different label systems and data sources.

**Independent audit** (`audit/rederive.py`, which uses separate code paths throughout):
- Delta-rho, rho_B and rho_BC, the size correlations, O1 Delta-AUC and M1 R^2 are re-derived exactly.
- Field-level Delta-AUC is re-derived as 0.0020 against the reported 0.0019.
- O2r recomputed from the raw S2 records is within 0.024.
- **Placebo:** a shuffled A*_h has mean Delta-rho 0.000 and passes the Delta clause in 0 of 200 permutations.
- **Positive-control ladder and power caveat:** because B5 alone already reaches rho = 0.83, the Delta >= 0.10 clause is passed only by a feature that correlates about 0.95 or more with O2r (noise SD 0.25 gives Delta = +0.126, CI low 0.107). A feature correlating 0.83 with O2r gains just +0.068. The concept-level clause therefore has little headroom on this panel, so the null for A*_h should be read together with its near-zero raw correlation with O2r (-0.01) and the null field-level test, not from the Delta clause alone.

**Recommendation:** carry A*_h forward only as a null or negative reference. B5 plus early breadth already carries the breadth signal. On the dev panel, the naturalisation gap is neither incremental nor reliable enough at typical adopter counts, and its sign depends on the field.

## What had to change: the credit pool ran dry
The OpenAlex key is shared by five parallel artifacts, with 10,000 credits a day between them. At the start of this run it had **2,098** left, and within minutes it was below the 1,000-credit floor reserved for siblings; sibling artifacts later spent it to about 0. This artifact spent **139 credits** in total, and the plan capped it at 3,500. The plan's download-heavy design, about 3,500 credits of search-list pages, was therefore impossible. Following fallback F2 (S0 first, then candidate data) and the task's allowance for "a comparable large-scale publication dataset", the work moved to zero-credit sources:

| Plan component | Source used here | Deviation |
|---|---|---|
| Yearly counts giving t0, newborn, O1, O3, log early volume, early growth | OpenAlex group_by, all 78 concepts, exactly as S0 specifies | none |
| Field labels for home, the dev restriction, O2r, R_j and the B5 reach terms | Semantic Scholar fields of study, as fractional memberships over 23 fields (s2-fos-model, a title/abstract text classifier). OpenAlex S0 with 26 topic fields exists for 11 concepts and is used as a cross-check | D8/D9 |
| Concept papers and lineage links | S2 phrase bulk search, all early papers up to 25k; links come from S2 citation lists of a seeded uniform sample of at most 1,500 parents | D9, D4' |
| Background references (negative control) | Child reference lists from **free** OpenAlex singleton GETs (cost 0 verified per response, with an abort if one is ever charged); reference fields from S2 via MAG ids | D10 |
| Grounding | Local exact/lemma matcher on title + abstract. S2 elides about 88% of abstracts, so papers with an elided abstract are kept as "unverifiable", and only papers whose available abstract lacks the phrase are rejected | D3' |

These label changes matter in two ways:
- **Not circular.** Text-classifier labels do not encode a paper's references, so they avoid the circularity that ruled out OpenAlex topics for citation-flow work.
- **Coarser life sciences.** S2's "Biology" is broader than OpenAlex's Biochemistry/Genetics/Molecular Biology, so sealing of life-science subfields such as immunology and neuroscience is weaker. Three concepts sealed by the OpenAlex home check (biosimilar, microbial fuel cell, microblog) stay sealed, and are never fetched or analysed.

Every deviation is also listed in `results/screen_result.json` under `deviations`.

## Method (as run)
1. **S0.** t0 is the first year in 2000-2014 with at least 20 phrase matches. The dev restriction keeps 2003 <= t0 <= 2009 and a home field in {CS, Engineering, Biology, Medicine}. Features use t0..t0+4, outcomes use t0+6..t0+8, and the two windows never overlap (asserted).
2. **Lineage.** A link runs from a concept paper p in year t (t0 <= t <= t0+4) to a concept paper q in t-3..t-1 that p cites. A link is SELF when p and q share an S2 author id and CROSS otherwise; self links are kept as a separate channel. Every paper carries a fractional field-membership vector.
3. **Stage 1.** For each concept c and off-home field j:
   - the concept log-OR is year-stratified Mantel-Haenszel over the table (child in j vs child in H) x (parent in j vs parent in H), with third-field parent mass excluded and each child renormalised;
   - the same MH log-OR is computed on the same children's background references;
   - rho_hat_cj is the concept log-OR minus the background log-OR, and its variance comes from 200 child-bootstrap resamples.

   Keeping home children as the control row cancels stock availability. The T0 test checks this under a stock that shifts from 90% to 40% home: mean rho_hat is below 0.1 when nothing naturalises, while the naive off-home rate drifts.
4. **Stage 2.** REML crossed random effects: field fixed effects, a concept random effect and a concept x field random effect, with Henderson MME BLUPs and the full prediction-error covariance. A*_h = sum_j pi_cj rho*_cj, where pi is the concept's off-home linked-child mass. Checks: PyMC NUTS (4 x 1,000 draws) and a one-stage BinomialBayesMixedGLM.
5. **Screen.**
   - LOGO over the four dev home-field groups: standardised ridge regression (alpha = 1) of B5 against B5 + A*_h. The missing flag goes into both models, and imputation uses the training-fold median.
   - Delta-rho for O2r, with a 2,000-resample concept bootstrap and a 200-resample refit bootstrap, and the sign of the gain in each group.
   - Split-half reliability: 50 splits with Spearman-Brown correction, plus a reliability-vs-n curve.
   - Size correlations and O1/O3 Delta-AUC.
   - Field-level test of rho*_cj against R_j: logistic LOGO with a concept-clustered bootstrap.
   - M1, and foils scored as candidates.

## Layout
- `method.py`: the driver (S0 assembly, stage 1, stage 2, screen, reliability, PyMC, GLMM, outputs).
- `oa.py`: OpenAlex client with cache, credit ledger, guards and a zero-credit singleton path.
- `s2.py`: Semantic Scholar client.
- `panel.py`: the P78 panel and its seeded order.
- `s0.py`: the S0 pieces.
- `ground.py`: the phrase matcher.
- `lineage.py`: the lineage network, MH tables and foils.
- `pool.py`: REML, DerSimonian-Laird and PyMC.
- `screen.py`: LOGO and bootstrap.
- `fetch_s2.py`, `fetch_bg.py`: the zero-credit data pulls.
- `tests/`: the T0 unit tests.
- `audit/rederive.py`: independent re-derivation of the headline numbers, with a placebo and a positive-control ladder; output in `audit/rederive_out.json`.
- `results/`:
  - `outcomes.csv`, `outcomes_openalex_s0.csv`, `field_outcomes.csv`;
  - `features.csv`, `field_features.csv`;
  - `screen_table.csv`, `screen_result.json`, `dropped.csv`;
  - `panel_order.json`, `s0_raw.json`;
  - `figures/`;
  - `concepts/<slug>/`, with the per-concept raw S2 data and background references.
- `method_out.json` (exp_gen_sol_out schema), with `full_`, `mini_` and `preview_` variants.
- `logs/credits.csv`: the ledger of every OpenAlex response and its credits (the key is never logged).
- `cache/`: raw response snapshot, not uploaded.

## How to run
See `reproducibility.md`. In short:
```bash
python -m pytest -c pytest.ini tests/
python fetch_s2.py
python fetch_bg.py
python method.py --splits 50 --n-boot 2000
python audit/rederive.py
```

## Restoring removed files
These entries in `.aii/manifest.yaml` are marked delete and regenerable:

```bash
# .venv/ : recreate the environment with the exact pinned versions from pyproject.toml
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r <(python3 -c "import tomllib;print('\n'.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))")

# __pycache__/ : bytecode, recreated by running the pipeline
.venv/bin/python method.py --splits 50 --n-boot 2000

# tests/__pycache__/ and .pytest_cache/ : recreated by running the tests
.venv/bin/python -m pytest -q -c pytest.ini tests/
```

Two directories are kept rather than deleted:
- `results/concepts/` holds the per-concept inputs and is published.
- `cache/` is the raw API snapshot. It is kept but not uploaded; re-pulling it through `fetch_s2.py` and `fetch_bg.py` (see `reproducibility.md`) drifts slightly because OpenAlex and S2 counts change daily.
