# gen_report_text — iteration 3

Internal research report for "Do temporal network signals predict how scientific concepts spread across disciplines?"

## What this module does

Writes the cumulative internal research report (`paper_draft.md`) covering iterations 1 through 3 of the study. Iteration 3 adds four artifacts: a retained frontier robustness test (Experiment 7), a heldout indicator screen (Experiment 8), a record audit and external recognition validation (Evaluation 2), and a prior art positioning study (Research 2).

## Layout

| File | Description |
|---|---|
| `paper_draft.md` | Full report, iterations 1-3, ~1320 lines. Lines 1-792 carried forward verbatim from iteration 2; lines 793+ are new. |
| `references.bib` | BibTeX bibliography, 32 entries, fetched via aii-semscholar-bib. |
| `references.json` | Fetch record companion to `references.bib`. |
| `style_exemplars.md` | Style exemplar excerpts from target venue papers (reused from iteration 2). |
| `domain_terms.json` | Domain vocabulary, 51 terms (reused from iteration 2). |
| `.terminal_claude_agent_struct_out.json` | Structured output: `paper_text`, `figures` (7 specs), `title`, `abstract`, `summary`, `out_expected_files`. |
| `.aii/manifest.yaml` | Disposable output manifest. |

## How to run

This module is executed by the AI Inventor pipeline (`gen_report_text` step). It reads artifact output files from sibling `gen_art_*` directories and the previous iteration's report, then writes the updated report.

## Restoring removed files

No files were removed. All workspace outputs are text files below the auto-keep floor.
