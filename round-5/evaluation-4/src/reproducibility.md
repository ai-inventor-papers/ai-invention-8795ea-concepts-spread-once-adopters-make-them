# Reproducibility

This describes what was actually run to produce the files in this folder: iteration 5, evaluation 4, "Fix the record
and pool the openness evidence". It made no LLM calls, no OpenAlex calls and no network requests. It downloaded no
data and needs no API keys.

## 1. Get the artifact

This folder is published as one folder of the run's public GitHub repository.

```bash
git clone <repository-url>
cd <repository>/<this-folder>          # the folder holding eval.py, audit.py and this file
```

### Inputs from other artifacts (read-only, never copied)

The code reads every input through ONE setting, the **run root**: the directory that contains the run layout
`3_invention_loop/iter_*/...`. Resolution order, in `src/paths.py`, `verify_ledger_v4.py` and `audit.py`:

- the environment variable `AII_RUN_ROOT`, if it is set;
- otherwise four levels above this folder (`Path(__file__).parents[...]`), which is where the folder sits in the run
  tree (`<run>/round-5/evaluation-4/src`).

If your clone names sibling folders by artifact id, arrange or symlink them into this layout under a directory `R`,
then run with `AII_RUN_ROOT=R`:

| layout path under `R/3_invention_loop/` | artifact id | files read |
|---|---|---|
| `round-4/experiment-10/src` | `art_NMe386dX9GLF` (Exp10) | `README.md`, `prereg.md`, `results/{cohort_result,cohort_report,learned_models_cohort,exp5_selection_result,frozen_spec}.json`, `data/{ego_open_exp5,covariates_exp5,analysis_cohort}.parquet`, `data/concept_types.csv`, `lib/{ladder,rq1stats}.py` (already copied verbatim to `vendor/`) |
| `round-4/experiment-12/src` | `art_uw4OeagJP3rv` (Exp12) | `results/{case_pairs,preregistration_R2,decomposition_dev,decomposition_heldout,sequence_light_dev,sequence_light_heldout,trajectories_dev,trajectories_heldout}.json`, `ai_atlas/atlas.json` |
| `round-3/experiment-8/src` | `art_dFQ6jbgNsR6Q` (Exp8) | `results/{heldout_unit_results.csv,rq1_heldout.json,heldout_summary.json}`, `data/outcomes.parquet` |
| `round-3/experiment-7/src` | `art_22ppE1snfHKj` (Exp7) | `results/step2_heldout.json`, `results/step2_dev.json` |
| `round-2/experiment-5/src` | `art_wxWssKSUR45f` (Exp5) | `frame_concepts.csv` |
| `round-4/evaluation-3/src` | `art_oKOd21ZMnu9S` (Eval3) | `corrections/00-11*.md`, `verify_ledger.py` (copied here as `verify_ledger_v4.py`), `results/{claims_ledger_v3.csv,boundary_spec.json,drca_persist_comparison.json,heterogeneity.json,spec_curve.json}` |
| `iter_4/gen_art/gen_art_experiment_11` | Experiment 11 (incomplete; its folder is named `gen_art_experiment_11`) | `prereg.md`, `results/{fe_results,deviations}.json`, `logs/{analysis_fe.log,event_study.log,event_study.out,partners.log}` |
| `round-2/research-1/src` | `art_dxvRpQufMR0e` (Research 1) | `research_out.json` |
| `round-3/research-2/src` | `art_EesdB8cuSfcU` (Research 2) | `references_new.json` |
| `round-4/research-3/src` | `art_hSyVUBa2okT2` (Research 3) | `research_out.json`, `raw/verify.json` |
| `iter_5/gen_strat/current_report.md`, `iter_4/gen_strat/current_report.md` | strategy-step report (not an artifact) | the base text that `report_corrected.md` corrects, and the Section 23 source |

Notes:

- The artifact counts in Sections 24 and 31 come from `iter_[1-4]/gen_art/gen_art_*/.aii_worker_result.json`. The
  result of that scan is saved in `results/artifact_counts.json`.
- The strategy reports may not be in the public repository. Without them the correction BLOCKS
  (`corrections_iter5/`), the ledgers and the synthesis are still fully reproducible. Only `report_corrected.md` and
  the text-presence check need the base report.
- `results/inputs_manifest.json` lists all 48 inputs with their size and sha256, so you can check your copies.
- The Dependency-1 dataset `art_O7Dq4L02QnDN` is not read. Its coverage rows are carried unchanged in the Section 30
  table.
- No user-uploaded file is used; the run's `user_uploads/` folder is empty.

## 2. System and Python environment

- Ubuntu (Linux 6.8), CPU only. The run used 4 CPUs and under 3 GB of RAM; there was no GPU.
- Python **3.12.14**, managed by **uv 0.6.14**. No system packages beyond Python and uv are needed.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh      # if uv is missing
uv venv --python 3.12 .venv
uv sync                                                # installs exactly the pins in pyproject.toml / uv.lock
```

Pinned versions (identical to `pyproject.toml`):

- numpy 2.5.3, pandas 3.0.6, pyarrow 25.0.1, scipy 1.18.1, matplotlib 3.11.2, loguru 0.7.3, jsonschema 4.26.0,
  pyyaml 6.0.3;
- plus their transitive pins: attrs, contourpy, cycler, fonttools, jsonschema-specifications, kiwisolver, packaging,
  pillow, pyparsing, python-dateutil, referencing, rpds-py, six, typing-extensions.

Environment variables, all optional and by name only:

- `AII_RUN_ROOT`: the run root, as above.
- `AII_FIG_SKILL_SCRIPTS`: the `scripts/` directory of the aii-data-fig-gen skill, for the house style of the
  forest plot. The published figure used it. Without it the same data is drawn with plain matplotlib.
- `OPENBLAS_NUM_THREADS=1`: the driver sets this itself.

## 3. Commands, in the order they were run

```bash
uv run eval.py         # ~2 min on 4 CPUs
uv run audit.py        # ~2 min; independent re-derivation + placebos -> results/audit.json
```

`eval.py` runs the following steps and aborts if any of them fails:

1. `src/synthesis.py --nboot 2000 --nperm 200 --workers 3`: gates G1/G2 and the evidence synthesis.
   - Bootstrap seed `numpy.default_rng(20260929)`, Exp10's frozen seed; placebo seed = 20260929 + 7.
   - G2 is also computed with seed 0.
2. `src/build_corrections.py`: `corrections_iter5/00-11*.md` and `results/claims_ledger_v4.csv`.
3. `src/apply_corrections.py`: `report_corrected.md` and `results/corrections_applied.csv`.
4. `src/refs.py`: `references_master.json|md`, and the in-text renumbering in `report_corrected.md`.
5. `src/figures.py`: `figures/evidence_forest.png|pdf`.
6. `src/checks.py`: G3, the v3/v4 ledger verification, text presence, stale strings and verbatim checks, written to
   `results/ledger_rerun.json`. It calls `verify_ledger_v4.py` as a subprocess.
7. The driver then assembles `eval_out.json`, `full_eval_out.json`, `mini_eval_out.json` and
   `preview_eval_out.json`.

The final mini/preview files were regenerated with the aii-json `aii_json_format_mini_preview.py --input eval_out.json`
tool. All four validate against the `exp_eval_sol_out` schema.

Everything is deterministic: a rerun gives identical numbers.

## 4. What you should get

`results/gates.json`: all gates pass.

| gate | expected result |
|---|---|
| G1 | EXP5 OPEN_home psp R0 +0.099, R2 +0.076 (n = 6,565) |
| G2 | cohort OPEN_home R2 +0.091 [+0.013, +0.171] (n = 573), R3 +0.080 |
| G3 | Eval3 ledger: 1,290 rows, 0 MISMATCH, 0 NOT_FOUND, 9 orphans |

`eval_out.json -> metrics_agg`:

- `n_mustfix_cleared` = 10.
- `ledger_v4_rows` = 1,769, with `ledger_v4_mismatch` = `ledger_v4_not_found` = `ledger_v4_orphans` = 0.
- `text_absent_v4` = 0 and `text_absent_v3` = 3.
- `stale_hits` = 0.
- Correction blocks: `corrections_applied` = 76, `corrections_already_present` = 5,
  `corrections_not_applied_target_missing` = 0.
- `references_master_n` = 120.

Evidence synthesis (report Section 32, `results/evidence_synthesis.json`, `figures/evidence_forest.*`), at R2:

| index | non-selection pool | DL 95% CI | HKSJ 95% CI | I2 | sign agreement | shrinkage |
|---|---|---|---|---|---|---|
| OPEN_home | +0.069 | [+0.038, +0.100] | [+0.042, +0.096] | 0 | 6/6 | 1.58 |
| NOVCHURN_home | +0.105 | [+0.069, +0.140] | [+0.078, +0.131] | 0 | 5/5 | 1.11 |

For OPEN_home the selection body (DEV) gives +0.109.

`results/audit.json`:

- All 14 body × index psp cells are reproduced by independent code, with max |diff| 1.9e-16 and identical n.
- The independent pools (own bootstrap SEs, B = 500) are OPEN_home +0.068 and NOVCHURN_home +0.105.
- The placebos fail as they should. A feature shuffled within each body gives a pooled psp of +0.021 with DL CI
  [-0.010, +0.051], which includes 0. Every per-cell placebo mean is within 3 SE of 0.

Where the numbers appear in the paper: the corrected report sections 23-32 (`report_corrected.md`) and the
insert-ready blocks in `corrections_iter5/`.
