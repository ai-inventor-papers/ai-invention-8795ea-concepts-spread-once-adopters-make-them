# Does where a concept lands decide its spread? A G (gateway-landing) screen with S0 outcome tables

This repository screens candidate **G** (gateway landing) on the frozen P78 dev panel under shared protocol **S0**. The question is whether early off-home adoption by *gateway* fields, meaning fields that are eigenvector-central in a pre-period field-relatedness backbone, predicts later size-adjusted disciplinary breadth beyond a volume/growth/breadth baseline (B5).

It is also the **authoritative producer** of the shared outcome tables (`outcomes.csv`, `field_outcomes.csv`) and of the simple reference indicators (`features.csv`, `single_indicators.csv`).

Data: the OpenAlex API (disk-cached, 286 credits) plus the free public OpenAlex S3 *sources* snapshot. OpenRouter spend: $0.

## Headline results (dev panel; the screen is a ranking device, not a finding)

| Test | Result |
|---|---|
| **Primary: B5 vs B5+G, O2r (m=30), LOGO ridge** | Δρ = **+0.033**, 90% CI [−0.095, 0.168] (2,000 concept bootstraps); positive in 2 of 4 groups (CS −0.23, Eng +0.07, BGM +0.07, Med −0.05). n = 34 |
| Survival clauses | (i) Δρ≥0.10 & CI>0: **False**; (ii) ≥3/4 groups: **False**; (iii) split-half r_SB = 0.92: True; (iv) max \|ρ\| with size = 0.13: True → **does NOT survive** |
| O2r m=50 / newborn-only / LOCO | +0.023 / −0.061 / −0.003 |
| O2r residualised on log N (secondary) | Δρ = +0.150, 90% CI [0.000, 0.321], positive in 4 of 4 groups |
| O1 sustained uptake (logistic, AUC) | ΔAUC = +0.072, 90% CI [0.00, 0.16], positive in 3 of 4 groups (n = 46); G alone: pooled AUC 0.84, oriented AUC > 0.5 in 4 of 4 groups |
| O3 transience | **not evaluable** (2 of 46 positives, both Medicine) |
| **Field-level retention R_j** (80 concept×field rows, 28 concepts) | + gateway_j: ΔAUC = **+0.103**, 95% CI [0.034, 0.167] (concept-clustered); with log field size in the baseline: +0.102, 95% CI [0.029, 0.173]; positive in Eng, BGM and Med, negative in CS |
| Next-field entry (61 concept-steps) | relatedness density AUC 0.61 [0.55, 0.67] beats the permuted-φ null (0.50, p = 0.023) but **loses to log field size** (0.74 [0.70, 0.78]). Conditional logit: density still adds signal (standardised β = 0.42 [0.21, 0.67]) |

Reading: G does not add concept-level breadth signal beyond B5 under the pre-registered rule, which is a negative result. The gateway position of the *specific field* that adopts early does predict whether that field keeps the concept. This holds after controlling for field size, but not in Computer Science.

## What was cut, and why (see `method_out.json → metadata.deviations`)

- The shared OpenAlex key had ~2,180 credits left when this run started, for five parallel artifacts, and it reset ~11.7 h later. It crossed the plan's **1,000-credit floor** at 12:26 after this artifact had used 286 credits, and every pull stopped there as the plan requires.
- Labels were pulled as pooled windows: A = t0..t0+1 (home), B = t0+2 (A+B = W3, the G window) and D = t0+6..t0+8 (outcome). Each window is one group_by call returning the top-200 sources. Window C (t0+3..t0+4) was never pulled. As a result:
  - B5's label components (off-home share, entropy, reach) are measured on W3. log_count_W5 and growth log(n[t0+4]/n[t0+1]) come from the yearly counts, as specified.
  - Field-retention rows use W3 (≥5 labelled papers).
- The outcome window was pulled for 34 of 46 dev concepts. These are the first ones in the seeded order, so they are an unbiased subset. The top-200-source cap truncates most windows (`trunc`=1 for 29 of 34), so the exclude-trunc sensitivity has n = 5 and was not run.
- Sources not looked up via the API were labelled from the S3 snapshot with the same ≥40% rule. API-vs-snapshot agreement on the overlap is 0.9997.
- **Not computed:** insularity I_j (so no INS features and no B5+G+INS joint model), φ_cit, SLICE_B, and the P5 primary-topic look. Weighted-degree, betweenness and φ_min-eigenvector gateways serve as gateway sensitivities instead.
- Label caveat: some non-English engineering venues (Korean, Japanese, Russian) carry Social-Sciences-dominated topic profiles in OpenAlex. This sent WiMAX, ZigBee, LTE-Advanced and cloud computing to a sealed home, and they were dropped, as S0 requires. The TAVI alias matches physics papers (Physical Review A), so TAVI also got a sealed home.

## Layout

| Path | What |
|---|---|
| `method.py` | Orchestrator. Runs the whole analysis offline from the cache (0 credits) and writes every output below |
| `oa_client.py` | OpenAlex client: sha1 disk cache (API key stripped), credit ledger, sub-budgets, BudgetStop, venue-field source labelling |
| `panel.py` | Frozen P78 panel, alias hygiene, query strings, seeded order (`panel_order.json`) |
| `s0_ground.py` | Yearly counts for the 78 concepts, t0, newborn flag and status → `yearly_counts.csv`, `global_totals.csv`, `grounding_log.json` |
| `s0_labels.py`, `pull_data.py` | Window label pulls, home field, dev gate (`cache/homes.json`), backbone and insularity pull code |
| `assemble.py` | Builds per-concept window field counts from the cache and the snapshot |
| `backbone.py` | 26-field positive-PMI backbone (1998–2002 whole-corpus topic co-assignment) and gateway centralities |
| `features.py` | G family, reference indicators, Kleinberg burst (own Viterbi), rarefaction, outcomes |
| `screen.py` | LOGO ridge/logistic, paired bootstrap, DerSimonian–Laird, field-level clustered bootstrap |
| `next_field.py` | Relatedness-density entry test, conditional logit, permutation null |
| `report.py` | Figures (`figures/*.png|pdf`) |
| `tests/test_units.py` | Rarefaction vs Monte Carlo, Kleinberg spike test |
| `outcomes.csv` | **Authoritative** S0 outcomes, all 78 rows. Non-dev rows are left blank on purpose |
| `field_outcomes.csv` | Concept × off-home field retention rows with baseline and candidate columns |
| `features.csv` | Dev concept features: G, secondaries, reference indicators, B5 columns, flags |
| `single_indicators.csv` | Indicator × outcome: pooled, per-group, random-effects pooled with I², sign consistency |
| `screen_result.json` | S0(j) screen keys: Δρ, CIs, per-group signs, reliability, size ρ, clauses, sensitivities |
| `method_out.json` / `full_method_out.json` | Everything, in exp_gen_sol_out format: per-concept OOF baseline and candidate predictions plus metadata (`mini_`/`preview_` variants via `make_variants.py`) |
| `reproducibility.md` | Step-by-step reproduction |
| `field_backbone.json`, `next_field_entry.csv`, `credits_log.csv` | Backbone matrices, entry rows, credit ledger |
| `cache/raw/` | **Frozen raw API responses** (282 JSON, ~39 MB). The only snapshot; keep it |
| `snapshot/` | S3 sources snapshot (parquet, ~370 MB). Re-downloadable, deleted after the round |

## How to run

```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python requests numpy pandas scipy scikit-learn statsmodels networkx loguru matplotlib pyarrow
bash snapshot/download_sources.sh          # free S3 sources snapshot (no credits)
.venv/bin/python tests/test_units.py
.venv/bin/python method.py                 # offline, ~6 min, 0 credits (reads cache/raw)
.venv/bin/python make_variants.py
```

Re-pulling from scratch (only if `cache/raw` is lost) runs `OPENALEX_API_KEY=... python s0_ground.py`, then `python pull_data.py A|backbone|BD|C|insularity|p5`. Responses drift day to day, so reuse the frozen cache whenever possible.

## Restoring removed files

- `snapshot/sources/`: `bash snapshot/download_sources.sh`. It reads `snapshot/sources_urls.txt` (from the OpenAlex manifest `s3://openalex/data/parquet/sources/manifest`, snapshot 2026-09-23) and downloads from `https://openalex.s3.amazonaws.com/data/parquet/sources/...`.
- `.venv/`: `uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python requests numpy pandas scipy scikit-learn statsmodels networkx loguru matplotlib pyarrow`.
