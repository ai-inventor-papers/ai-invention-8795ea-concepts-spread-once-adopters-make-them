# gen_report_text — Iteration 1

First internal research report for the study "Do temporal network signals predict how scientific concepts spread across disciplines?"

## What this step does

Writes the chronological lab-notebook report for iteration 1 of the invention loop. The report covers three experiments testing whether network indicators (naturalisation gap, structural diversity, gateway centrality) predict cross-disciplinary concept spread beyond a five-feature baseline of popularity and reach. All three candidates fail the pre-registered decision rule. Two positive findings survive: background homophily explains 66% of lineage variance, and field-level gateway centrality predicts retention (delta-AUC +0.10).

## Layout

- `paper_draft.md` — full report text with `[FIGURE:]` markers and `[ARTIFACT:]` references
- `references.bib` — BibTeX bibliography (machine-generated via Semantic Scholar)
- `references.json` — fetch provenance record for each bibliography entry
- `style_exemplars.md` — verbatim passages from target-venue papers for register calibration
- `domain_terms.json` — 51-entry domain vocabulary with glosses
- `.terminal_claude_agent_struct_out.json` — structured JSON output (title, abstract, figures, summary) for downstream pipeline
- `.aii/manifest.yaml` — disposable-output manifest

## How to run

This step is executed by the AI Inventor pipeline (step 3.4, GEN_REPORT_TEXT). It reads artifact outputs from earlier experiment steps and writes the report. No separate entry point; the pipeline orchestrator invokes the agent with the task prompt.

## Restoring removed files

All files in this workspace are text and below the auto-keep floor. No files were removed.
