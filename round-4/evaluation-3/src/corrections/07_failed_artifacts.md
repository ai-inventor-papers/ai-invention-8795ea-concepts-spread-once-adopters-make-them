# 07 Failed artifacts, iteration counts and artifact ids

## New Section 22b (or addition to 5a): Experiment 9 did not run

[Correction, iteration 4, from gen_art_experiment_9 .aii_worker_result.json] Iteration 3 commissioned a fifth artifact, gen_art_experiment_9, from the plan 'Plan: how new concepts spread — trajectories and reasons (iteration 3, experiment direction 3)' (`iter_3/gen_plan/gen_plan_experiment_3/`: state sequences, breadth decomposition, empirical trajectory typology, sequence tests, snapshot lineage check, case studies, recognition timing). The worker failed before producing any output: `failed = true`, error: 'output_format validation failed after 5 retries: The output file `./.terminal_claude_agent_struct_out.json` does not exist yet.'. The workspace holds no method.py (absent) and no results. What was lost: the RQ2 trajectory typology and sequence tests for iteration 3. Status: **not run, not refuted**.

## Iteration counts (from each artifact's .aii_worker_result.json)

| iteration | commissioned | completed | failed | failed artifacts |
|---|---|---|---|---|
| 1 | 5 | 3 | 2 | gen_art_dataset_1, gen_art_experiment_2 |
| 2 | 5 | 5 | 0 | - |
| 3 | 5 | 4 | 1 | gen_art_experiment_9 |

Source: `round-4/evaluation-3/src/results/partA_derived.json` -> `iterations.iter_<i>.*`
Cross-check with Section 5a: it lists gen_art_dataset_1 and gen_art_experiment_2 as the two iteration-1 failures, which agrees. Iteration 2 had no failures. Iteration 3's failure (Experiment 9) is not in the draft.

## Artifact id placeholders -> real ids

| placeholder in draft | real id | artifact |
|---|---|---|
| `[ARTIFACT:art_experiment_7]` (1 occurrences) | `art_22ppE1snfHKj` | Experiment 7 (retained frontier) |
| `[ARTIFACT:art_experiment_8]` (1 occurrences) | `art_dFQ6jbgNsR6Q` | Experiment 8 (held-out indicator screen) |
| `[ARTIFACT:art_evaluation_2]` (1 occurrences) | `art_7W9xiIO3FVBs` | Evaluation 2 (record audit, O5) |
| `[ARTIFACT:art_research_2]` (2 occurrences) | `art_EesdB8cuSfcU` | Research 2 (prior art, venue) |
