# Concepts spread where they stick: network signals of cross-disciplinary diffusion in science

## Overview

This workspace contains a research paper investigating which early structural signals in scientific knowledge networks predict whether a concept will spread broadly across disciplines. The paper identifies seven confirmed network indicators, validates a retained-frontier entry model, and decomposes the breadth gap between integrating and localised concepts.

## Layout

| File / Directory | Description |
|---|---|
| `paper.tex` | LaTeX source for the paper |
| `paper.pdf` | Compiled PDF (15 pages) |
| `references.bib` | BibTeX bibliography (17 entries from Semantic Scholar/OpenAlex) |
| `references.json` | Fetch record for bibliography entries |
| `figures/` | Pre-generated figure PDFs (vector format) |
| `figures/fig2_v0.pdf` | Figure 1: Evidence synthesis forest plot (openness vs breadth) |
| `figures/fig3_v0.pdf` | Figure 2: Retained-frontier coefficient across domains |
| `figures/fig4_v0.pdf` | Figure 3: Nested conditional-logit model ladder |
| `figures/fig5_v0.pdf` | Figure 4: Breadth-gap decomposition into three channels |

## How to compile

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

Requires a TeX Live installation with `natbib` and `booktabs` packages.

## Restoring removed files

No files were marked for deletion. All workspace contents are text, code, or small PDF figures below the auto-keep floor.
