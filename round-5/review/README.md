# Review: iteration-5 report audit

This folder holds the adversarial review of the iteration-5 research report for run `run_Id7TLZ6r1C7M`. The report reviewed is `gen_report_text/paper.tex`.

## What was done
- I read the report and walked all 21 supplementary artifacts.
- I recomputed the headline numbers directly from each artifact's result JSON files: the Exp10 cohort ladder, the Exp8 held-out screen, the Exp12 decomposition, Exp7 d0/LR/dose, the Exp13 Frame N verdict, the Exp14 identity check, the Exp15 Shapley values and the Exp16 disattenuation.
- Nothing new was computed. There was no API or LLM spend.

## Layout
- `.terminal_claude_agent_struct_out.json`: the structured review (scores, critiques, blocking flag).
- `scratch/recompute_log.md`: each report claim, the artifact file/key it traces to, the recomputed value, and the verdict.
- `.aii/manifest.yaml`: empty. There are no heavy files; everything here is small text.

## How to reproduce
Every value in `scratch/recompute_log.md` names the JSON file and key it came from, under `3_invention_loop/iter_{3,4,5}/gen_art/...`. Reading those keys reproduces each check.

## Restoring removed files
Nothing is marked for deletion.
