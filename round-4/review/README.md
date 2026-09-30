# Review of the iteration-4 research report (run_Id7TLZ6r1C7M)

This folder holds an adversarial audit of the run's internal research report after iteration 4. It checks completeness, traceability and consistency against the iteration 1-4 artifact workspaces. No code was executed against the data; the audit read each artifact's result files and recomputed the report's headline numbers from them.

## Layout
- `.terminal_claude_agent_struct_out.json`: the structured review (scores, 10 critiques, `results_reported=false`, `blocking=true`).
- `.aii/manifest.yaml`: disposal manifest (empty, because nothing heavy was created).
- `README.md`: this file.

## Main findings
1. Five of the seven case-study pairs in report Section 26.4 do not exist in `gen_art_experiment_12/results/case_pairs.json`.
2. `iter_4/gen_art/gen_art_experiment_11` (within-concept closure test) ran its DEV models (null by the frozen rule) but is absent from the report.
3. The report reverses Exp10's coupling reading and Exp12's OPEN-versus-retention result, and it mislabels Exp12's PR2.
4. Most of Eval3's insert-ready corrections were not applied, although Section 27.6 says they were. Iteration 3's Section 23 was overwritten.

## How to run
Nothing to run. To re-check a finding, open the artifact file named in the corresponding critique.

## Restoring removed files
No files are marked `delete`, so nothing needs restoring.
