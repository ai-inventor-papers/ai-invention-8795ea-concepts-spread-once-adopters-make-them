# gen_report_text — iteration 4

Internal research report for "Do temporal network signals predict how scientific concepts spread across disciplines?"

## What this module does

Writes the cumulative internal research report (`paper_draft.md`) covering iterations 1 through 4 of the study. Iteration 4 adds four artifacts: a confirmatory cohort test of the OPEN index (Experiment 10), a breadth decomposition and trajectory analysis (Experiment 12), a boundary study with specification curve (Evaluation 3), and a novelty positioning study (Research 3).

## Layout

| File | Description |
|---|---|
| `paper_draft.md` | Full report, iterations 1-4, ~1600 lines. Lines 1-1247 carried forward from iteration 3 with in-place corrections; lines 1248+ are new. |
| `references.bib` | BibTeX bibliography, ~74 entries, fetched via aii-semscholar-bib. |
| `references.json` | Fetch record companion to `references.bib`. |
| `style_exemplars.md` | Style exemplar excerpts from target venue papers (reused from iteration 2). |
| `domain_terms.json` | Domain vocabulary, 51 terms (reused from iteration 2). |
| `.terminal_claude_agent_struct_out.json` | Structured output: `paper_text`, `figures` (8 specs), `title`, `abstract`, `summary`, `out_expected_files`. |
| `.aii/manifest.yaml` | Disposable output manifest. |

## How to run

This module is executed by the AI Inventor pipeline (`gen_report_text` step). It reads artifact output files from sibling `gen_art_*` directories and the previous iteration's report, then writes the updated report.

## Key changes in iteration 4

1. **OPEN index confirmed on cohort.** OPEN_all PSP = +0.174 [+0.092, +0.253] at R2, surviving all six control rungs. Specification curve: 99.7% of 1,920 specs have CI > 0.
2. **Breadth decomposition.** Exploration (early contact diversity) accounts for 73% of the top-vs-bottom breadth gap; retention 27%. Frontier advance ratio is negative (PR2 REVERSED).
3. **Trajectory typology is a CONTINUUM.** The naming rule fails; DTW-HMM agreement is low. The two-class finding from iteration 2 does not reproduce at higher resolution.
4. **Boundary study.** Half of M0_density_end and D_vol_end signal is pre-onset footprint (PARTIAL). LIFEENV domain boundary unexplained.
5. **Novelty positioning.** C1/C2 partially anticipated, C3/C4 new. Contribution: first held-out, size-adjusted, concept-level test of early openness predicting cross-field breadth.
6. **12 corrections applied** from Evaluation 3 (MUST-FIX items): indicator family count, O4/O3 relabelling, preregistered text, H1/H3 criteria, ordering downgrade, Experiment 9 failure, field count.

## Restoring removed files

No files were removed. All workspace outputs are text files below the auto-keep floor.
