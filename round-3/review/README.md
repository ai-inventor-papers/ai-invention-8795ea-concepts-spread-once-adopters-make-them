# Iteration-3 review of the research record (review_report)

This directory holds the adversarial audit of the run's internal research report after iteration 3.

## What was done
- Read the report (iterations 1-3). Walked every iteration-3 artifact workspace (`round-3/experiment-7/src`, `_8`, `_9`, `gen_art_evaluation_2`, `gen_art_research_2`), and the plans in `iter_3/gen_plan/`.
- Recomputed the headline numbers from the artifact result files. Examples: the LR ladder in Exp7 `results/step1_exp6_robustness.json` (log-likelihoods), `step2_heldout.json` (verdicts, dose, volume-matched, crossed bootstrap), Exp8 `README.md` tables, `prereg_verdicts.json` and `heldout_unit_results.csv`, and Eval2 `text_corrections.md`, `claims_ledger.csv` and `o5_validation.json`.
- Checked whether the report's iteration-1/2 sections carry the corrections requested by the previous review and produced by Evaluation 2. They do not: the earlier sections are byte-identical to `iter_3/gen_strat/current_report.md`.

## Layout
- `.terminal_claude_agent_struct_out.json`: the structured review (scores, critiques, blocking flag).
- `README.md`: this file.
- `.aii/manifest.yaml`: the disposal manifest. It is empty because nothing heavy was written.

## How to run
Nothing to run. The review is static JSON. To re-check a finding, open the source key named in each critique. Paths are relative to the run's `3_invention_loop/` directory.

## Restoring removed files
No files are marked for deletion, so there is nothing to restore.
