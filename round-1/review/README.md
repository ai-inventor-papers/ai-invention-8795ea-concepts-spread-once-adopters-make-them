# Review of the iteration-1 research report (REVIEW_REPORT)

This directory holds an audit of the iteration-1 internal research report. Every number was checked against the artifact workspaces for experiments 1, 3 and 4 and against the failed artifacts (dataset_1 and experiment_2). No experiments were run here.

## Layout
- `.terminal_claude_agent_struct_out.json`: the structured review (ReviewerFeedback schema). It holds the scores, 15 critiques, `results_reported`, `coverage` and `blocking`.
- `.aii/manifest.yaml`: the storage manifest. It is empty because nothing heavy is stored here.
- `README.md`: this file.

## Main findings
- Headline delta-rho values recompute exactly from each artifact's OOF files.
- Sections 6.1 and 8 contradict experiment 4: its B5 baseline has rho 0.327, not 0.77-0.83.
- Section 3.4 reports "median A*_h" values that are actually within-group Spearman correlations. The real medians are negative in every group.
- Two failed artifacts are missing from the report: the held-out dataset and candidate S.
- Each experiment computes its own O2r. The three versions agree only at rho 0.76-0.80, so the cross-experiment table does not compare like with like.

## How to run
Nothing runs here.

## Restoring removed files
No files are marked for deletion.
