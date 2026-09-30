# Reproducing "Checking the record before the paper"

This is the audit evaluation of iteration 3 (plan `gen_plan_evaluation_1_idx4`). It collects no new data. It reads result files that
earlier artifacts of the same run produced, re-computes and cross-checks them, and writes the outputs listed in step 5.

## 1. Get the artifact

```bash
git clone <this repository URL>
cd <repository>/<this artifact's folder>      # the folder that contains eval.py
```

## 2. Inputs (the other artifacts) and the one path setting

Every input is read relative to ONE root, `AII_RUN_ROOT`, which must contain the run's artifacts laid out as below. The default is
three levels above this folder, which is how the folders sit on the run server (`<root>/iter_3/gen_art/<this folder>`).

| Relative path under `AII_RUN_ROOT` | Artifact id | Used for |
|---|---|---|
| `round-2/experiment-5/src/` | art_wxWssKSUR45f | frame, episodes, outcomes, H1/H3 JSON, `models.py`, `frozen_spec.json` |
| `round-2/experiment-6/src/` | art_N-mpomDZZ1ln | frame, episodes, `entry_risk_sets_*.parquet`, `heldout_result.json`, `dev_result.json`, `full_method_out.json` |
| `round-2/dataset-2/src/` | art_O7Dq4L02QnDN | `full_data_out/full_data_out_{1,2,3}.json`, `out/coverage_report.json`, hand-check CSVs, README |
| `round-2/evaluation-1/src/` | art_lwI2DuRtQRZX | `eval_out.json` (F_record, E_power, A_replication, D_O1_artefact) |
| `iter_1/gen_art/gen_art_experiment_{1,3,4}/` | art_xp8BGBJZsxeI, art_yrradSC27HtQ, art_33_KKk_G8Gw5 | iteration-1 features and outcomes (T3 refits), screen results |
| `round-2/report-text/paper_draft.md` | iteration-2 draft | the audited text |
| `iter_3/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json` | iteration-3 strategy | hypothesis numbers (optional) |

The repository publishes those artifacts as sibling folders. Arrange (or symlink) them under a directory in this layout, then run
`export AII_RUN_ROOT=<that directory>`. No input was uploaded by the user, so none is private.

## 3. Environment

- Ubuntu 22.04 or later, Python 3.12.14, and [uv](https://docs.astral.sh/uv/). No GPU is used.
- The original run used a 48-core CPU with 251 GB RAM. Peak use was well under 10 GB; the O5 join holds one ~90 MB JSON part per process.

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python ijson==3.5.1 loguru==0.7.3 numpy==2.5.3 openai==3.20.0 pandas==3.0.6 psutil==7.2.2 \
    pyarrow==25.0.1 pyyaml==6.0.3 requests==2.34.2 scikit-learn==1.9.1 scipy==1.18.1 statsmodels==0.15.0 tenacity==9.1.4
```

These are the same pins as `pyproject.toml`.

Environment variables, by name only:

- `OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY`, for the LLM judge in the hand check only. It used `openai/gpt-4.1-mini`, 50 calls,
  $0.009 in total, with a hard cap of $1.
- `AII_RUN_ROOT`, optional (see step 2).

The Wikipedia step calls the public MediaWiki API (no key) at most once per second.

## 4. Commands, in the order they were actually run

All bootstraps use seed 20260928 and B = 2000, resampling concepts.

| # | Command | What it does | Runtime |
|---|---|---|---|
| 1 | `.venv/bin/python wp2_t3_refit.py --B 2000 --workers 16` | T3 refit bootstrap → `results/t3_refit_bootstrap.json` | ~1.5 min |
| 2 | `.venv/bin/python wp4_extract.py` | joins O5 to the Exp5 frame → `results/o5_joined.jsonl` | ~1 min |
| 3 | `.venv/bin/python wp3_frames.py` | WP3 → `frame_agreement.json`, `record_tables/frame_*`, `definitions_diff.csv` | ~1 min |
| 4 | `.venv/bin/python wp2_t4_nextfield.py` | T4 refits → `record_tables/next_field_trace.json`, `next_field_heldout_rows.parquet` | ~1.5 min |
| 5 | `.venv/bin/python wp4_o5.py 2000` | writes `o5_definitions.json` first, then the O5 associations (40 processes) | ~8 min |
| 6 | `.venv/bin/python wp1_ledger.py` | `claims_ledger.csv` and the T1/T2/T5/T6/T7 tables | ~1 min |
| 7 | `.venv/bin/python wp4_handcheck.py` | hand-check sample, LLM judge and first MediaWiki pass | ~3 min |
| 8 | `.venv/bin/python wp4_handcheck.py --wiki-retry` | retries the lookups that got HTTP 429 (31 of 70 on the first pass), with backoff | ~2 min |
| 9 | *(manual step)* | the executor (the AI agent) read all 100 items and wrote `results/executor_verdicts.json`; this file is in the repository | — |
| 10 | `.venv/bin/python wp4_handcheck.py --finalize` | → `results/o5_handcheck_summary.json` | seconds |
| 11 | `.venv/bin/python wp1_ledger.py` | re-run so the ledger picks up the T3 rows | ~1 min |
| 12 | `.venv/bin/python eval.py` (also run as `uv run eval.py`) | assembles `eval_out.json`, `o5_validation.json`, `inputs_manifest.json` | seconds |
| 13 | `.venv/bin/python wp5_text.py` | `text_corrections.md` | seconds |
| 14 | aii-json `aii_json_format_mini_preview.py --input eval_out.json` | `full_`/`mini_`/`preview_eval_out.json`; schema `exp_eval_sol_out` validated | seconds |
| 15 | `.venv/bin/python verify_headlines.py` | independent re-derivation with placebo controls → `results/verify_headlines.json` | ~25 s |

`eval.py --stages all` re-runs steps 1–6, 10 and 11 in sequence, then assembles. It does not repeat the sampling, LLM and Wikipedia
steps (7–8), because `executor_verdicts.json` depends on the sampled items.

**Non-determinism.**

- **LLM verdicts:** `temperature = 0`, but the provider can still vary. The executor's verdicts override the LLM wherever they differ.
- **MediaWiki:** first-revision dates can change if a page is later deleted or moved.
- **Everything else** is deterministic given the inputs.

## 5. Expected outputs and numbers

| File | Key numbers |
|---|---|
| `claims_ledger.csv` | 246 rows: 224 MATCH, 15 MISLABELLED, 6 MISMATCH, 1 FILE_FLAG_OVERRIDDEN; 58 blocking |
| `record_tables/refit_bootstrap_iter1.csv` | e.g. exp4 G Δρ O2r_m30 = 0.033, refit CI95 [-0.250, 0.339]; no refit CI excludes 0 |
| `record_tables/next_field_trace.json` | 26/26 checks match. LR M1 vs M0: 68.57 (Breslow), 73.25 (exact). LR M2 vs M0: 71.72 (Breslow), 77.30 (exact). 961 informative strata of 2,339 |
| `frame_agreement.json` | n_both = 628; onset exact 0.976; home κ 0.990; O2r_m50 Spearman 0.998; retention κ 0.280 (0.980 with R_abs2); verdict PARTIAL |
| `o5_validation.json` | O5_main held-out base rate 0.238; reading UNRELATED; pooled ρ with O2r_m50 = 0.014 [-0.045, 0.073]; 67% of concepts are recognised at or before t0 |
| `results/o5_handcheck_summary.json` | precision 0.86, date error ≤ 1 year in 95%, false-negative rate 0.14, FIT_FOR_USE true; 42% of positives are "emergence-meaningful" |
| `eval_out.json` | 74 flat metrics; 6 datasets: ledger, T3, T4 trace, 628 shared concepts, 12,499 O5 concepts, 100 hand-check items |
| `text_corrections.md` | old sentence, new sentence and source keys for each blocking item in the draft (10.3, 11.3/16.3, 10.6/16.5, 10.7, 5.4, 13.1, 8a, 4.4, 11.2, 16.1, 10.5, 11.5 and the new frame and O5 paragraphs) |
| `results/verify_headlines.json` | see the table below |

`results/verify_headlines.json` recomputes the headline numbers through separate code paths, each with a placebo that fails as expected:

| Check | Re-derived value | Placebo |
|---|---|---|
| Retention κ (sklearn) | 0.280 | shuffled κ 0.013 |
| Home κ | 0.990 | shuffled 0.017 |
| Fresh Breslow LR, M1 vs M0 | 68.57 | within-stratum permuted LR 2.07 |
| Ordering counts from `ordering_heldout.csv` | 57/15/30 of 175 | — |
| Hand-written ridge, exp4 G Δρ | 0.033 | shuffled-G placebo reaches it in 22.5% of draws, i.e. no signal |
| O5 pooled ρ with O2r_m50 (Fisher-z pooling) | 0.009 [-0.037, 0.055] | — |

These numbers feed the iteration-3 paper's record corrections: the H1 criteria table, the ordering rewrite, H3, the frame comparison
and the O5 status paragraph.
