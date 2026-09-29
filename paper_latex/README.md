# Concepts spread where they stick

Network signals of interdisciplinary diffusion in science.

## What this is

A self-contained public web page (`index.html`) presenting the paper's findings, built from the LaTeX source. The page is published as the run's GitHub Pages site.

## Layout

```
paper.tex            Final paper (LaTeX source)
paper.pdf            Compiled paper
references.bib       Bibliography
references.json      Parsed references
index.html           Public web page (this deliverable)
interactive.html     Interactive companion page: explorable views over the run's own output data (self-contained, no network)
figures/
  fig2_v0.pdf        Evidence synthesis forest plot (vector)
  fig2_v0.png        Rendered at 200 DPI for the web page
  fig3_v0.pdf        Retained-frontier entry forest plot (vector)
  fig3_v0.png        Rendered at 200 DPI for the web page
  fig4_v0.pdf        Model ladder two-panel figure (vector)
  fig4_v0.png        Rendered at 200 DPI for the web page
  fig5_v0.pdf        Breadth decomposition bar chart (vector)
  fig5_v0.png        Rendered at 200 DPI for the web page
  fig*_spec.json     Figure specifications
workspace/           LaTeX build scratch (not part of the deliverable)
```

## How to view

Open `index.html` in any browser. No build step, no dependencies, no network required. All CSS and JavaScript are inline. Figures are referenced as `figures/*.png`.

## Restoring removed files

No files were marked for deletion. All content is text, code, or small images under the auto-keep floor.
