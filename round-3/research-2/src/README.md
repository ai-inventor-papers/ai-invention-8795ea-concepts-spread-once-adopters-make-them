# Prior-art and venue check: "fields that keep it" (iteration 3, research artifact)

This is a web-only positioning study for an Applied Network Science paper on emerging scientific concepts. It checks two claims against prior literature:
- **(A)** next-field entry follows relatedness to fields that *retain* a concept;
- **(B)** relatedness to fields that *dropped* it lowers entry.

The literatures checked are relatedness / economic complexity, export learning, exit, invasion biology and diffusion of ideas. The study also:
- collects comparison numbers for RQ1 (emergence detection) and RQ2 (diffusion trajectories);
- probes the target collection ("Networks for everyday life");
- extracts the ANS article structure;
- writes a Figure 1 specification.

No code experiments were run.

## Layout
- `research_report.md`: the full report.
  - A: verdicts and Table P, plus rivals for the experiment;
  - B: Table R1;
  - C: Table R2;
  - D: venue and ANS skeleton;
  - E: Fig. 1 spec;
  - F: references and corrections;
  - G: paper table templates;
  - H: what would change the conclusions.
- `research_out.json`: structured answer with numbered sources. It is saved automatically by the pipeline.
- `references_new.json`: 50 newly verified references (Crossref / arXiv API), plus UNVERIFIED items not to cite.
- `reproducibility.md`: the exact queries, pages and routes used.
- `scripts/`:
  - `s.sh`, `f.sh`, `g.sh`: wrappers around the aii-web-tools search, fetch and grep;
  - `xref.py`: Crossref DOI verification with backoff;
  - `pmc_struct.py`: Europe PMC XML → article structure.
- `raw/greps/`: regex-grep outputs with the exact quoted passages.
- `raw/epmc/`: Europe PMC XML and text.
- `raw/crossref/`, `raw/s2/`, `raw/openalex/`, `raw/venue/`, `raw/search/`: API responses.
- `raw/arxiv_pdf/`: arXiv PDFs of Fontaine 2024 and Holmgren 2023, plus extracted text.

## How to run / re-run
```bash
bash scripts/g.sh pinheiro2022 "https://run.unl.pt/bitstreams/e0c3b563-f946-4b3a-9a9b-5c2583cfd12a/download" "backward" 3 900
python3 scripts/xref.py 10.1016/j.respol.2021.104323 10.1038/s41598-023-28179-x
python3 scripts/pmc_struct.py PMC9673898
```
The shell wrappers expect the aii-web-tools skill at `../../../tools/aii-web-tools`.

## Restoring removed files
Nothing is marked for deletion: every file in this workspace is small text, code or a PDF under the auto-keep floor, so the manifest (`.aii/manifest.yaml`) has no entries. If the arXiv PDFs in `raw/arxiv_pdf/` are ever missing (they are excluded from the public upload), re-download them:
```bash
mkdir -p raw/arxiv_pdf
curl -L -o raw/arxiv_pdf/2310.01046.pdf https://arxiv.org/pdf/2310.01046
curl -L -o raw/arxiv_pdf/2303.00622.pdf https://arxiv.org/pdf/2303.00622
```
