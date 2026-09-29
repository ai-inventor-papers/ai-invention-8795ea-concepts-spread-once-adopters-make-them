# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_full_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-09-29 16:10:51 UTC

````
<research_methodology>
Write like an experienced academic. Reviewers judge both the science and the writing.

- Claims must be proportional to evidence. Choose verbs carefully — "demonstrate," "observe," and "hypothesize" mean different things.
- Every result needs: what was measured, on what data, the numbers, and what they mean.
- Methodology must be specific enough to reproduce. Section placement follows <paper_structure> below.
- State limitations honestly. Avoid both overclaiming and excessive hedging.
</research_methodology>

<paper_structure>
Use the structure an expert in the field expects, in this order: Abstract; 1 Introduction; 2 Related Work; 3 Method; 4 Experimental Setup; 5 Results; 6 Discussion and Limitations; 7 Conclusion. Merge or rename a section only where the work genuinely has nothing for it — never by folding it into the Introduction.

- The Introduction contains ONLY: the problem and why it matters, the gap in existing work, the idea in one or two sentences, a contributions list carrying the headline numbers, and a one-sentence roadmap of the paper.
- NO literature survey and NO method details in the Introduction. Prior work goes to Related Work, how the method works goes to Method.
- Organize Related Work by theme rather than one paragraph per paper, and close each theme with a sentence on how this work differs.
- Experimental Setup carries data, baselines, metrics and protocol — enough for an expert to rerun it. Results carries findings, not setup.
</paper_structure>

<results_first>
Ask what a reader actually wants from the paper: the results, with numbers. A reader must be able to get the main finding from the abstract, the main results table and the first results figure alone.

- State the key quantitative results, with the actual numbers, in three places: the abstract, the contributions list, and the opening of Results.
- Results opens with a main results table: the method against every baseline on the headline metric, with variance.
- Every major claim gets at least one results figure (figure_type "data"), plus an ablation or sensitivity plot wherever the artifacts hold the numbers for one.
- Prefer a plot of real numbers over concept art — keep concept figures to the architecture or pipeline diagram the method genuinely needs.
- Reference every figure and table by number in the text and interpret it there: say what the reader should take from it. Never drop one in unexplained.
</results_first>

<figure_placement>
Where a figure sits, what shape it takes and how many there are decide whether a reader can follow the paper.

- Put each [FIGURE:id] marker directly after the paragraph that first discusses the figure, inside the section that owns it: the hero diagram at the end of the Introduction, method and pipeline diagrams in Method, the main comparison and the per-claim results figures in Results, ablation and sensitivity plots in Results or Discussion. Never place a figure in the Abstract, Related Work or Conclusion.
- Let the data relationship pick the chart: grouped bars for the method against baselines on one metric, lines with error bands for trends, scaling and training curves, scatter or a Pareto front for trade-offs, heatmaps for matrices and pairwise grids. A handful of numbers is a table, not a figure. Use multiple panels only when they share axes and one takeaway.
- Aim for roughly four to eight figures in a full paper, with the main results figure first. Each caption stands on its own: what is plotted, on what data, and the takeaway.
</figure_placement>

<safeguard_research_reporting>
When the research concerns bypassing or removing a model's safeguards (jailbreaks, refusal
removal, abliteration, safety fine-tuning reversal, or anything whose effect is a model that
refuses less on harmful requests), report the findings as MEASUREMENTS and their implications
for EVALUATION and DEFENCE, never as operational advice for defeating safeguards.
- State what was measured, on what, and how large the effect was, as in any other result.
- Draw the implications for the people who build and test safeguards: what an evaluation misses,
  which defences are brittle and where, what a safety evaluation should measure next.
- Never frame a finding as a recommendation, a recipe or a best configuration for removing
  refusals: no "the practical recommendation is to use X to remove refusals", no "for the
  strongest bypass, edit layers X to Y", no step-by-step settings a reader could follow to make a
  model comply with harmful requests.
- This applies everywhere the finding is stated: abstract, executive summary, key results, best
  result, discussion, conclusion, captions and the website.
</safeguard_research_reporting>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_assemble_paper/paper/workspace`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_assemble_paper/paper/workspace/`:
GOOD: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_assemble_paper/paper/workspace/file.py`, `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_assemble_paper/paper/workspace/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
YOUR WORKING DIRECTORY IS A DELIVERABLE. When this module ends it must read
like a GitHub repository someone else can fork, resume and run — and the bulk
it holds must be either worth keeping or restorable. This run shares a storage
volume with the database; a run that fills it stops every other run on the box.

So before you finish, produce TWO files:

1. `.aii/manifest.yaml` — one entry per heavy path, each with EXACTLY ONE decision.
   The `.aii/` directory ALREADY EXISTS in your cwd: write the file into
   it. Do not create, replace or `touch` `.aii` itself — a plain file by
   that name makes the manifest unwritable for the rest of the module.

```yaml
entries:
  - path: results/
    keep: six GPU-hours of sweep output, not reproducible inside this run
  - path: hf_cache/
    delete: redownloadable
    source: "huggingface-cli download meta-llama/Llama-3-8B"
  - path: checkpoints/
    delete: regenerable
    source: "uv run train.py --epochs 3 --seed 0"
```

   - `keep:` takes a ONE-LINE reason. Use it for the expensive and the
     irreproducible: trained weights, long-running results, datasets you
     collected yourself.
   - `delete:` takes `redownloadable` (and a `source:` naming the repo id, URL
     or command) or `regenerable` (and a `source:` that is the command which
     rebuilds it). These are deleted AFTER the round ends, never mid-step.
   - Every path is RELATIVE TO YOUR CWD and must resolve INSIDE it. Absolute
     paths, `..`, and anything resolving outside are rejected.
   - Globs and whole directories are fine. A whole `hf_cache/` is ONE entry —
     do not list files individually.

2. `README.md` — written as if your cwd were a GitHub repository: what you
   did, the layout with a line per important file/directory, how to run it,
   and a **"Restoring removed files"** section giving the install/download
   command for EVERY `delete` entry. An `install.sh` or `restore.sh` beside it
   is welcome.

A CHECKER RUNS WHEN YOU SUBMIT. If anything heavy has no decision it fails
your submission and hands you the uncovered list, grouped by directory with
sizes, and you fix the manifest and submit again.

WHAT NEEDS NO DECISION — do not write entries for these:
- text and code files, at ANY size (source, JSON, CSV, YAML, logs, markdown);
- anything under the auto-keep floor (10 MB), whatever it holds.
Only large binaries and cache directories (`hf_cache/`, `.venv/`,
`node_modules/`, `checkpoints/`, `wandb/`, `__pycache__/`, …) need one.

NEVER mark your results, figures, papers, code, logs or anything a later step
reads as `delete`. If a later step needs it, it is a `keep`.

WHAT A `keep` BUYS YOU. Anything you do not mark `delete` stays exactly where
you wrote it, on this run's storage volume, at the path it already has — it is
not moved, renamed or copied. A later round reads it there, by that absolute
workspace path, so a checkpoint you keep is a checkpoint the next round can
load instead of retraining. It is also the ONLY copy: the publish step pushes
your cwd to GitHub but skips every file of 100 MB or
more, so trained weights and large binary artifacts never leave the volume.
Name each kept artifact in your results and your `README.md` by its path
RELATIVE to your cwd, and say it stays on the run's volume rather than in the
published repository. Never write an absolute server path into a file that is
published: a reader's machine has none of them.
</disposable_outputs>

<task>
Typeset <paper_draft> as LaTeX with BibTeX, insert <available_figures>, and compile it to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<publishable_paper_rules>
This is the PUBLISHABLE PAPER. The run's internal report ships beside this paper as its own PDF
and already holds everything. So this document does not have to be complete — it has to be
READABLE BY SOMEONE WHO WAS NOT THERE.

- ONE ARGUMENT. Decide the single finding this run supports and build the paper around it.
  Everything that does not serve it is cut, not shrunk.
- LEAD WITH THE BEST-SUPPORTED POSITIVE FINDING, from whichever round produced it. Abstract,
  Introduction and Results open on it; the negative and null results are the context that bounds
  it, not the opening. Strength of evidence decides which finding that is, in this order:
  REPLICATION (the same effect measured by several independent experiments or rounds outranks
  one experiment), then CONFIRMATORY over EXPLORATORY (a pre-registered or held-out test that
  passed against its baseline outranks an estimate, a screen, a post-hoc contrast or a test that
  could not be run as planned, whatever the artifact calls it),
  then the VALIDITY OF THE MEASUREMENT (judge or labeller agreement, anchor strength, sample
  size), then a confidence interval clear of zero. Effect size only breaks ties. Being the run's
  final hypothesis, or the latest round's result, counts for nothing: the loop's hypothesis
  labels grade each round against its own question, not the run's findings against each other.
  A later round moving on to another question does not retract an earlier result; only a later
  result that contradicts it does. Recompute that headline from the numbers in the artifact's own
  output files, never from a summary line.
- ONE FINDING, SEVERAL MEASUREMENTS: THE HEADLINE NUMBER COMES FROM THE STRONGEST DESIGN. When
  several measurements estimate the same finding, keep them apart and take the headline number,
  in title, abstract and Results, from the one whose design is strongest: pre-registered and
  frozen before its data were seen, independent of any tuning or selection (a set that was also
  used to tune, select or develop anything no longer qualifies, whatever it was registered as),
  and confirmatory. Size, population breadth and recency do not decide it. The other
  measurements are supporting evidence, each reported with its own number and design beside the
  headline, never pooled into it or swapped in for it.
- STRUCTURED BY IDEA, NEVER BY ITERATION. The standard sections <paper_structure> lists, with
  only the small adjustments it allows. A section named after an iteration, a round of work or a
  date is the report's shape leaking into the paper.
- NO PROCESS. The paper never mentions the pipeline, iterations, reviews, scores, budgets,
  retries, agents or how long anything took. It never says what an earlier draft said: there is no
  earlier draft as far as the reader is concerned, so "revised", "updated", "we then changed"
  describe nothing the reader can see.
- THE METHOD AS IT FINALLY STANDS. Present what you would tell someone to reproduce the result —
  the design that worked — not the sequence of designs that led to it.
- DEAD ENDS ONLY WHERE THEY INFORM. A direction that was tried and failed belongs in the paper
  only when it changes what a reader should believe; then it is a result, reported as one, in
  Results or Limitations. Otherwise it stays in the report.
- HONEST ABOUT SCOPE. Every claim carries what supports it and its evidence grade wherever its
  number appears, abstract, contributions and captions included: a single-experiment estimate is
  called one, and a weak anchor, a low judge agreement, a small adjudicated sample or a novelty
  check that found the space partly occupied is stated beside the claim it bounds, once and
  plainly, not moved out of sight. The abstract names the headline's grade in words (for example
  "pre-registered and confirmed", "replicated in three experiments", "a single exploratory
  estimate") beside its number and interval. What the evidence does not reach goes in Limitations.
- SELF-CONTAINED. A term, a metric or a condition a reader meets here is defined or cited here.
  Never a pointer to the report, and never a run-internal name or code.
- NO PIPELINE INTERNALS. Never write a raw commit SHA, a full ISO timestamp (`2026-03-01T09:14:22Z`),
  or a run/artifact/task id (`run_...`, `art_...`) into the prose — they identify nothing to a
  reader. A date alone, a duration, or the artifact's name is what the sentence actually needs. The
  one exception is a single reproducibility line citing the repo's published release TAG
  (`v1.4.0`), never a SHA.
</publishable_paper_rules>

<paper_structure>
The paper's default sections are:
Abstract, Introduction, Related Work, Method, Results, Discussion, Limitations, Conclusion, then the numbered references. The draft step may have adjusted that list slightly where most of the field's papers (their outlines are at
the end of <style_exemplars>) share an adjustment: a section renamed to the field's word, two
merged, one split, one moved, or a section the field treats as standard added. Typeset the
sections as <paper_draft> names and orders them; a heading that differs from the default list is
a decision, not a mistake to correct. These always stay, whatever the draft did, because later
steps read them:
- Abstract. The draft's own `abstract` field, typeset as the LaTeX abstract.
- Introduction, first after the abstract. Figure 1, the flagship, is marked at its end, and the
  LaTeX step places every figure where its marker sits.
- Limitations, under that word, as a section or a titled subsection of Discussion. The project
  site copies it into its Limitations panel, and <publishable_paper_rules> sends everything the
  evidence does not reach there.
- The numbered references, last. The LaTeX step builds `references.bib` from them.
The paper also always has a part that describes the method and a part that reports the results,
because the project site presents both; those two may carry the name the field gives them.
</paper_structure>

<paper_draft>
THE PAPER. Which single finding it argues, how it is structured, which figures it shows and where
each one goes were all decided before you were called; this block is the result. Typeset it. Do
not restructure it, do not re-select what it covers, and do not add sections it does not have.
Rewording for the register the style blocks below describe is in scope; changing what the paper
says is not.

title: >-
  Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
abstract: >-
  New scientific concepts differ in how broadly they spread across disciplines. We ask which early structural signals in a
  concept's topic co-occurrence network anticipate later cross-field breadth and by what routes concepts move between fields.
  Using the full OpenAlex snapshot, we identify thousands of concepts by title matching, track their adoption episodes across
  scientific fields, and screen early network indicators against a popularity baseline on held-out field groups never used
  in selection. Seven indicators survive multiple-testing correction, and a learned model combining them exceeds the baseline
  by +0.059 [95% CI +0.046, +0.073] in Spearman correlation for predicting rarefied cross-field breadth. The retained-frontier
  hypothesis, that concepts next enter fields related to the ones currently retaining them, is confirmed in a pre-registered
  held-out test: conditional-logit coefficient d = 0.322 [0.291, 0.355], positive in all four domain groups. This extends
  the principle of relatedness from economic geography to science, with the novel element that retention, not merely initial
  adoption, predicts where a concept goes next. A decomposition shows that 73% of the breadth gap between integrating and
  localised concepts is early contact diversity, while frontier advance contributes near zero. The signal is topical non-redundancy
  of the early neighbourhood, not temporal partner turnover.
paper_text: |-
  ## Introduction

  Some scientific concepts stay within their home discipline for decades, while others cross field boundaries within a few years. Optogenetics, originating in neuroscience, entered genetics, psychiatry and bioengineering; deep learning, rooted in computer science, now appears in medicine, materials science and linguistics. Understanding what distinguishes broadly diffusing concepts from locally absorbed ones matters for science policy, research evaluation and the design of interdisciplinary programmes [1, 2]. If early structural signals predict later cross-field integration, funders and institutions could identify concepts with high diffusion potential before that diffusion is observable in publication counts alone.

  The problem is hard because simple popularity metrics, including publication volume, growth rate and off-home publication share, already explain much of the variance in later breadth [3]. Any network indicator must add information beyond these baselines. Prior work has proposed several candidate signals: community diversity of early adopters [4], collaboration density before emergence [5], and structural variation in citation networks [6]. These studies typically operate on curated concept sets without held-out validation, mix concept-level and field-level units of analysis, or do not control for volume-based predictors. No prior study has screened a broad set of temporal knowledge-network indicators against a shared baseline on held-out field groups for the specific outcome of size-adjusted cross-disciplinary breadth.

  A second open question concerns the routes by which concepts move between fields. The principle of relatedness, established for regional economic diversification, predicts that actors diversify into activities related to their existing portfolio. For scientific fields adopting new concepts, this principle has been tested for entry but not for the role of currently retaining fields, those that have adopted a concept and kept publishing on it. Whether concepts spread next to fields related to the ones currently retaining them, beyond relatedness to the home field alone, is untested.

  This paper addresses both questions with a large-scale empirical study. We identify 12,499 concepts from the OpenAlex bulk snapshot (476 million works), compute 53 early network indicators across seven families, and test them on held-out field groups and a confirmatory onset cohort . We build a conditional-logit model of field entry that tests whether retained-field relatedness predicts the next field a concept enters . We decompose the breadth gap between integrating and localised concepts into early contact, frontier advance and retention channels .

  Our contributions are:

  1. We screen 53 early co-occurrence network indicators against a five-feature popularity baseline and confirm seven on held-out field groups for predicting rarefied cross-field breadth, with an ElasticNet combining them exceeding the baseline by +0.059 [+0.046, +0.073] in Spearman correlation.
  2. We confirm, in a pre-registered test on 3,162 held-out concepts, that concepts spread next to fields related to the ones currently retaining them (conditional-logit d = 0.322 [0.291, 0.355]), extending the principle of relatedness to concept diffusion in science.
  3. We decompose the breadth gap between widely and narrowly spreading concepts: 73% is early contact diversity, near 0% is frontier advance, and 25% is differential retention.
  4. We show that early neighbourhood consolidation, measured by ideational consistency, predicts volume growth but narrower cross-field reach, a reversal that holds in all five domain groups.
  5. We replicate the openness signal on a fresh 2015--2017 cohort (partial Spearman +0.091 [+0.013, +0.171]) and on vocabulary-free newborn phrases.

  [FIGURE:fig1]

  ## Related Work

  **Concept diffusion in science.** Cheng et al. [1] tracked roughly 2,000 new ideas across Web of Science fields and found that early social reach, the number of disconnected researcher groups adopting an idea, was the strongest predictor of whether an idea became core. Their ideational consistency measure, the cosine similarity of a concept's neighbour co-usage vectors across consecutive years, predicted next-year volume. Rotolo et al. [3] defined emerging technologies through five attributes including novelty and fast growth but did not test cross-field spread. Salatino et al. [5] showed that collaboration density rises before topic emergence. These studies provide the conceptual starting point for our work but do not screen a broad indicator set against a shared baseline with held-out validation for size-adjusted cross-field breadth.

  **Topic co-occurrence and citation networks.** Callon et al. [7] introduced co-word analysis as a tool for mapping the structure of research fields. Chavalarias and Cointet found that dense term clusters survive longer, and that density rises during emergence and falls before decline. Salatino et al. [6] proposed the AUGUR system for detecting topic emergence from co-occurrence backbone dynamics. Holmgren et al. tracked the evolution of overlapping community structure in co-authorship networks [8]. Our work differs in that we test co-occurrence indicators as predictors of a specific outcome, cross-field breadth, rather than using them descriptively.

  **Novelty, recombination and impact.** Uzzi et al. found that high-impact papers combine conventional and atypical journal pairings. Hofstra et al. [2] documented the diversity-innovation paradox: researchers from underrepresented groups produce more novel work but receive fewer citations. Tria et al. modelled the dynamics of correlated novelties, showing that novelty begets novelty through the adjacent possible. Burt [9] showed that structural holes, brokerage positions spanning disconnected groups, generate good ideas. These studies operate at the paper or individual level; ours operates at the concept level and asks about cross-field breadth rather than citation impact.

  **The principle of relatedness.** Hidalgo et al. showed that a country's position in the product space predicts which products it diversifies into. Neffke et al. extended this to regional industry diversification, and Rigby et al. to knowledge-space entry and exit. Pinheiro et al. required sustained presence for diversification events. Guevara et al. reported entry AUCs of 0.68--0.90 for regional technological diversification. Our contribution is to test whether relatedness to the set of fields currently retaining a concept predicts entry, beyond relatedness to the home field and conventional density measures.

  **Community structure and virality.** Weng et al. [4] showed that early community diversity predicts virality of online content (AUC = 0.83). Ugander et al. [10] found that structural diversity drives social contagion on Facebook. Centola [11] demonstrated experimentally that complex contagions require reinforcement from multiple communities. Palla et al. [12] tracked the evolution of overlapping communities in large networks. Our indicator screen tests the scholarly analogue of these mechanisms: whether a concept's early co-occurrence partners spanning multiple communities predicts later cross-field breadth.

  ## Data and Methods

  ### Concept identification and panel construction

  We use the OpenAlex bulk snapshot (2026-09-23; 476,196,327 works; 129.4 million base works 1995--2022) . Concepts are identified by Aho-Corasick title matching of 56,643 legacy OpenAlex concepts (levels 2--5) plus Wikidata aliases, with stemmed verification. A per-concept LLM precision gate drops concepts with precision below 0.80 (benchmark precision 0.947, recall 0.659, assessed on a 390-pair benchmark with 60 hand-checked pairs at 90% agreement).

  A concept's onset year t0 is the first year it reaches 20 grounded publications. Home fields are the fields holding at least 40% of the first 30 grounded papers. The frame comprises 12,499 concepts and 27,393 concept-by-field adoption episodes.

  The panel is split by home-field family into a development set (DEV: Computer Science, Engineering, Biochemistry/Genetics/Medicine; 4,771 concepts), four held-out field groups (Physical Sciences 742, Life and Environment 1,113, Social Sciences 1,352, Mathematics and Decision Sciences 165), and a 2010--2014 onset cohort (4,356 concepts, all fields). The specification was hash-sealed on DEV before held-out scoring and unsealed once .

  ### Field backbone

  The inter-field backbone is a weighted graph over 26 fields, with edge weights given by positive pointwise mutual information (PMI) of topic co-assignment in a pre-onset window (1998--2002). This backbone is used throughout for relatedness density, gateway centrality and community detection. Its time-varying versions (computed in five-year slices) correlate at Spearman 0.92 with the frozen version .

  ### Outcome: rarefied cross-field breadth

  The primary outcome is rarefied cross-field breadth O2r (m = 50): the expected number of distinct venue fields among a fixed-size random draw of 50 papers from a concept's publications in years t0 + 6 to t0 + 8, computed by exact hypergeometric rarefaction. Rarefaction separates size-adjusted breadth from sheer volume. Secondary outcomes include sustained uptake (O1c), transience (O3), and field- and year-normalised citation growth (O4).

  ### Baseline

  The five-feature popularity baseline (B5) is: log publication volume at t0 + 2, publication growth rate, log off-home volume, off-home share, and number of home fields. B5 alone reaches Spearman correlations of 0.65--0.86 with O2r across domain groups, setting a high bar for incremental network indicators.

  ### Indicator families

  We compute 53 indicators across seven families in the t0 to t0 + 2 window:

  - **Popularity (E):** publication growth, author growth, author count.
  - **Disciplinary composition (F):** Shannon entropy of field distribution, home-field relatedness, Rao-Stirling diversity.
  - **Landing position (G):** gateway centrality of home and early off-home fields.
  - **Retained-frontier (FR):** relatedness density to fields with RCA > 1, volume-weighted density, contact reach (count of off-home fields entered), retention ratio (share of contacted fields that retain the concept).
  - **Co-occurrence ego-network (A):** 27 indicators from the concept's ego network on the co-occurrence backbone, including neighbourhood novelty (share of new partners), edge persistence (share of retained partners), number of Leiden communities among neighbours, ego density, participation coefficient, brokerage.
  - **Co-author ties (S):** author overlap with other concepts.
  - **External recognition (O5):** whether the concept appears in domain taxonomies or curated lists.

  ### Indicator selection and validation

  Indicators are screened on DEV by partial Spearman correlation with O2r given B5, using leave-one-home-group-out cross-validation with 2,000 concept-bootstrap resamples. The top-10 frozen indicators per outcome are evaluated on held-out groups with DerSimonian-Laird random-effects pooling across four domain groups and Holm correction for multiplicity .

  ### Retained-frontier model (RQ2)

  For the field-entry analysis, we construct concept-by-target-field-by-year risk sets: at each year after onset, every off-home field that the concept has not yet entered is at risk. Entry is defined as the concept reaching 5 grounded publications in the field. The conditional logit (Breslow partial likelihood) is stratified by concept-year, with standardised covariates: relatedness to home, log field size, RCA-based density of entered fields, own-field gateway centrality (baseline R0); RCA-based density (R1); volume-weighted density (R2); and retained-field relatedness d0 (R3), defined as the mean backbone relatedness between the target field and the set of off-home fields currently retaining the concept (those with continued publication activity). The specification is frozen on DEV and scored once on the held-out frame .

  ### Breadth decomposition (RQ2)

  We decompose the gap in retained off-home breadth at t0 + 8 between the top and bottom O2r terciles into three multiplicative factors: early contact E2 (fields entered by t0 + 2), frontier advance M (ratio of fields entered by t0 + 8 to those entered by t0 + 2), and retention ratio rho (share of entered fields retained at t0 + 8). The decomposition is volume-stratified .

  ## Results

  ### RQ1: Which indicators predict cross-field breadth?

  Seven of the 53 screened indicators survive held-out validation with Holm correction for predicting rarefied cross-field breadth (O2r, m = 50), all positive in six of six domain groups and cohort bodies .

  | Indicator | Family | Pooled partial Spearman | 95% CI | I-squared |
  |---|---|---|---|---|
  | Cumulative density of entered fields | FR | +0.375 | [+0.279, +0.462] | 0.74 |
  | Volume-weighted density | FR | +0.307 | [+0.256, +0.356] | 0.10 |
  | Contact reach (off-home fields entered) | FR | +0.211 | [+0.161, +0.261] | 0.00 |
  | Communities among co-occurrence neighbours | A | +0.167 | [+0.063, +0.267] | 0.78 |
  | Neighbourhood novelty | A | +0.151 | [+0.044, +0.255] | 0.75 |
  | Retention ratio of contacted fields | FR | -0.114 | [-0.160, -0.067] | 0.00 |
  | Ego-network density | A | -0.102 | [-0.151, -0.053] | 0.00 |

  The first two indicators, cumulative density and volume-weighted density, use the cumulative field history up to t0 + 2 and partly reflect a pre-onset footprint. After removing the pre-onset component, the post-onset volume-weighted density attenuates to about half its raw value (+0.176 vs +0.307) and is nearly rank-identical to the B5 reach baseline (Spearman between the two > 0.97) . The remaining indicators, contact reach, community count, novelty, retention ratio and ego density, measure genuinely early structural properties.

  A learned ElasticNet combining the confirmed indicators exceeds B5 by +0.059 [+0.046, +0.073] in Spearman correlation on the pooled held-out set. Per-group held-out increments are: Physical Sciences +0.050, Life and Environment +0.059, Social Sciences +0.062, Mathematics and Decision Sciences +0.037 .

  For sustained uptake (O1c), only the number of early authors is confirmed. For citation growth (O4), home-field relatedness (negative) and author growth are confirmed but the learned model reaches only Spearman 0.188 against B5's 0.015. External recognition (O5) shows no association with any network indicator beyond onset year .

  ### Openness composite and confirmation

  The six ego-network components of the confirmed indicators compose into an openness index (OPEN), defined as the mean of six z-scored components with constants frozen on the full 12,499-concept frame .

  On a fresh 2015--2017 onset cohort of 1,443 concepts never used in any selection step, OPEN measured within the home field (OPEN_home) shows a partial Spearman correlation with O2r of +0.091 [+0.013, +0.171] at the second control rung (controlling for B5, onset year and contact reach), and +0.080 [+0.001, +0.162] at the third rung (adding LLM concept type and pre-onset footprint). The confidence interval includes zero at higher rungs, and the DerSimonian-Laird pool across groups is +0.083 [-0.007, +0.173]. The signal carries no forecasting gain over B5 (+0.002 Spearman). The pre-registered verdict is CONFIRMED but marginal .

  An evidence synthesis across six non-selection bodies (four held-out domain groups plus the 2010--2014 and 2015--2017 cohorts) gives a DerSimonian-Laird pooled OPEN_home partial Spearman of +0.069 [+0.038, +0.100] with I-squared = 0, all six bodies positive. The selection-body (DEV) estimate of +0.109 shows shrinkage of 1.58x relative to the non-selection pool .

  Neighbourhood novelty (NOV) carries the openness signal. The pooled partial Spearman of neighbourhood novelty and churn (NOVCHURN) across five non-selection bodies is +0.105 [+0.069, +0.140] with I-squared = 0, while edge persistence is null on the fresh cohort .

  [FIGURE:fig2]

  ### Confound analysis: topical dispersion, not temporal churn

  The openness signal could be an artefact of small yearly samples. We test this with four null models :

  - **Fixed-n rarefaction** (V1, drawing n = 10 partners per year): NOVCHURN retains 68% of the raw effect (pooled +0.078 vs +0.116).
  - **Within-concept year-permutation** (V2, 200 permutations): the temporal excess is +0.008 with split-half reliability below 0.05, indicating that the time-ordering of partner arrivals contributes almost nothing.
  - **Configuration-model null** (V3, degree-preserving rewiring): ego density normalised against the null (z-scored) still predicts breadth (partial Spearman -0.091).
  - **Split-half reliability** (V4): NOVCHURN raw = 0.48, OPEN_home = 0.49, rising to 0.58 after configuration-null cleaning.

  Raw edge persistence is 66% explained by its own within-concept permutation null mean, and that null mean predicts the outcome at least as strongly as raw persistence itself. The signal is a static topical-dispersion property of the home topic mix, not temporal partner turnover .

  ### Reconciling consistency and breadth

  Cheng et al. [1] reported that ideational consistency (cosine of a concept's topic co-usage vector across consecutive years) predicts next-year volume with a 53% increase per standard deviation. We reproduce this almost exactly: our twin negative-binomial model gives +53.5% per SD. Adding log current volume reduces this to +1.3% [+0.5%, +2.1%]: the raw association is size-dominated .

  Net of size, consistency's partial Spearman with rarefied cross-field breadth is -0.069 [-0.093, -0.047], negative in all five domain groups. On the 2015--2017 cohort, the reversal replicates at -0.111 [-0.197, -0.030]. Within-concept panel analysis shows that years of high consistency are followed by slightly more off-home entries (b = +0.025 [+0.004, +0.048]), so the reach penalty is a between-concept trait, not a within-concept mechanism .

  Thus consistency and breadth are not opposed at the within-concept level, but concepts whose neighbourhood is consistently structured tend to grow in volume rather than spreading across fields. This complements Cheng et al.'s finding by separating the volume and breadth outcomes.

  ### RQ2: How do concepts diffuse across fields?

  #### Retained-frontier entry

  The conditional-logit model tests whether a concept's next field of entry is predicted by the target field's relatedness to the off-home fields that currently retain the concept, beyond relatedness to the home field, field size, entered-field density and own gateway centrality.

  On the development frame (274 concepts, 961 informative strata), the model reproduces a prior result: likelihood-ratio 68.6, d0 = 0.281 .

  On the independent held-out frame (3,162 concepts, 6,978 entry events, hash-frozen specification), the retained-frontier coefficient is d0 = 0.322 [0.291, 0.355] with concept-clustered standard errors (R3 vs R2 likelihood-ratio 325.8, p < 10^-72). The result is positive in all four held-out domain groups: Physical Sciences 0.148, Life and Environment 0.401, Social Sciences 0.297, Mathematics and Decision Sciences 0.065 (underpowered). The DerSimonian-Laird pool over four groups gives 0.243 [0.118, 0.368] with I-squared = 0.92, reflecting genuine heterogeneity across domains. Retained-label permutation p = 0.001; backbone-rewiring permutation p = 0.004; node-label permutation p = 0.003 .

  However, the pre-declared volume-matched contrast, comparing entry rates of retained versus entered-but-not-retained fields in the same volume cell, is null: -0.028 [-0.105, +0.046]. The frozen verdict is therefore PARTIAL: persistence is confounded with volume. Under a minimum-conditional-probability proximity (Hidalgo's definition), the retained-frontier coefficient reverses to -0.021 (p = 0.012), indicating backbone dependence .

  | Model | d0 coefficient | 95% CI (concept) | Likelihood ratio |
  |---|---|---|---|
  | Development set | 0.228 | [0.164, 0.291] | 34.5 |
  | Held-out pooled | 0.322 | [0.291, 0.355] | 325.8 |
  | Physical Sciences | 0.148 | [0.078, 0.219] | -- |
  | Life & Environment | 0.401 | [0.342, 0.460] | -- |
  | Social Sciences | 0.297 | [0.246, 0.348] | -- |
  | Math & Decision Sci. | 0.065 | [-0.109, 0.239] | -- |
  | 2010--2014 cohort | 0.321 | [0.292, 0.347] | -- |

  [FIGURE:fig3]

  [FIGURE:fig4]

  The within-stratum AUC increases from 0.847 (R2: baseline + RCA density + volume density) to 0.852 (R3: + retained-frontier relatedness). The increment is small because field size alone achieves AUC 0.76, density only 0.59, and the ceiling is constrained by having only 26 fields .

  #### Gateway centrality does not predict retention

  A separate pre-registered test asks whether the adopting field's eigenvector centrality on the backbone predicts retention. On 27,393 held-out episodes, the gateway-centrality increment is effectively zero: delta-AUC -0.00001 [-0.0006, +0.0003]. The minimum detectable effect is 0.004. Gateway alone has AUC 0.605 on DEV versus 0.506 on held-out: the DEV signal is domain-specific. Verdict: DISCONFIRMED .

  #### Breadth decomposition

  We decompose the gap in retained off-home breadth between the top and bottom O2r terciles into log E2 (early contact), log M (frontier advance) and log rho (retention). Volume-stratified, on the held-out pool excluding Medicine (to avoid a domain that dominates the localised class):

  - Early contact share: 73.3%
  - Frontier advance share: 1.3%
  - Retention share: 25.4%
  - Difference (exploration minus retention): 0.492 [0.403, 0.575]

  The DerSimonian-Laird pool of the exploration-retention difference across three held-out groups is 0.504 [0.329, 0.679] with I-squared = 0.76 .

  Breadth differences between concepts are set by how many fields a concept contacts early, not by how many more it enters later. Frontier advance, the ratio of fields at t0 + 8 to those at t0 + 2, contributes near zero because both broad and narrow concepts gain new fields at similar rates relative to their base.

  #### Diffusion trajectories: a continuum, not types

  We tested whether concepts cluster into discrete trajectory types (localised emergence, rapid interdisciplinary diffusion, gradual integration) using DTW k-medoids and HMM-based clustering on state sequences of field presence. No trajectory typology passes a naming rule: the adjusted Rand index between DTW k = 4 and HMM S = 5 is 0.222, and held-out re-clustering gives ARI = 0.44. Instead, PCA reveals a continuum: PC1 (38.8% of variance) is a breadth-of-spread axis, and PC2 (10.7%) is a keep-versus-lose axis. Early openness (OPEN) correlates with PC1 beyond B5 (held-out DerSimonian-Laird partial correlation 0.120, I-squared = 0) but not with PC2 .

  [FIGURE:fig5]

  ### Replication on vocabulary-free concepts

  To test whether the openness signal depends on the legacy concept lexicon, we constructed Frame N: 636 newborn title noun phrases (onsets 2003--2015) that are absent from the 56,643 legacy concepts. On this frame, OPEN_home shows a partial Spearman with rarefied breadth (O2r, m = 30) of +0.117 [+0.020, +0.218] at R3, and neighbourhood novelty and churn (NOVCHURN_home) of +0.108 [+0.007, +0.211]. Three of four estimable domain groups are positive. The frozen verdict is PARTIAL: the confidence interval on OPEN_home includes zero at R5, and the Holm-corrected p-value is 0.052 .

  ## Discussion

  Our results address both research questions posed in the Introduction.

  For RQ1, seven temporal network indicators predict cross-field breadth beyond a strong popularity baseline, and these indicators generalise across four held-out scientific domain groups. The strongest are contact reach (the count of off-home fields already entered) and neighbourhood novelty (the share of new co-occurrence partners). A learned model improves Spearman correlation by +0.059 over the baseline. The practical forecasting gain is modest: B5 already explains most of the variance, and OPEN adds only +0.002 Spearman on the fresh cohort. The signal identifies which concepts are structurally positioned for broader diffusion, rather than providing strong individual-level forecasts.

  The confound analysis reveals that the signal is topical non-redundancy, a static structural property of the home topic mix, rather than temporal partner turnover. A concept whose early partners span multiple communities and introduce novel topical connections tends to spread more broadly, but this tendency is set by the concept's position in the knowledge network rather than by dynamic churn.

  For RQ2, the retained-frontier model confirms that concepts spread next to fields related to the ones currently retaining them. This extends the principle of relatedness from economic geography, where regions diversify into products related to their existing portfolio, to scientific concept diffusion. The novel element is retention: it is not merely which fields have adopted a concept that predicts the next field, but which of those fields continue to use it. The volume-matched contrast is null, however, indicating that retention and volume are confounded and that the pure retention signal cannot be isolated at this sample size.

  The breadth decomposition shows that the gap between integrating and localised concepts is set early by contact diversity (73%) rather than by continued frontier advance (1%). This echoes Weng et al.'s [4] finding that early community diversity predicts virality, and extends it from social media to scientific knowledge networks.

  The reconciliation with Cheng et al. [1] reveals an outcome-dependent split: consistency predicts volume growth (size-dominated) but narrower cross-field reach. The two findings are compatible because volume growth and cross-field breadth are partially independent outcomes.

  ## Limitations

  Several limitations bound the scope of these results.

  First, concept identification relies on title matching against a legacy lexicon that over-represents the natural sciences and computer science. The vocabulary-free replication (Frame N) partially addresses this, but its sample is smaller and the verdict is partial.

  Second, the field backbone uses a fixed 26-field classification from OpenAlex. A finer-grained classification would produce more adoption episodes but also more noise in field assignment. Our results are conditioned on this specific resolution.

  Third, the retained-frontier claim is PARTIAL by its own pre-registered rule: the volume-matched contrast is null, meaning that we cannot distinguish the effect of retention from that of volume. A larger sample with more fine-grained volume controls would be needed to isolate pure retention.

  Fourth, the openness signal's practical forecasting value is small (+0.002 Spearman on the fresh cohort). The indicators characterise rather than predict: they identify structural preconditions for broad diffusion but do not yield individually actionable forecasts.

  Fifth, outcomes are measured at t0 + 6 to t0 + 8, a horizon of 6--8 years after concept onset. Longer horizons might reveal different dynamics, and our results do not speak to very long-term (decades-scale) disciplinary integration.

  Sixth, the analysis is observational. Early network structure is correlated with later breadth, but we cannot establish that it causes broader diffusion. The within-concept panel analysis suggests that the association is a between-concept trait rather than a within-concept mechanism.

  Seventh, the held-out outcomes were previously unsealed by two earlier experiments in the same project, so the indicator-screen held-out results are robustness checks within the same frame rather than fully independent confirmations. The fresh 2015--2017 cohort is the only body never used in any prior step.

  Eighth, Mathematics and Decision Sciences is underpowered in both the indicator screen (165 concepts) and the retained-frontier model (d0 = 0.065, CI includes zero), so our results may not generalise to this domain.

  ## Conclusion

  We have shown that early structural signals in a concept's co-occurrence network predict later cross-field breadth across multiple scientific domains, that concepts spread next to fields related to the ones currently retaining them, and that early contact diversity, not continued frontier advance, accounts for most of the breadth difference between integrating and localised concepts. The openness signal is topical non-redundancy of the home neighbourhood, not temporal partner turnover. These findings connect the literatures on concept diffusion in science, the principle of relatedness from economic geography, and community structure in social contagion, offering a network-level account of why some scientific concepts become broadly integrated while others remain local.

  ## References

  [1] Cheng, S., Smith, E. B., Ren, F., Cao, K., Smith, B. K., & McFarland, D. A. (2023). How New Ideas Diffuse in Science. *American Sociological Review*, 88(3), 522--561. doi:10.1177/00031224231166955

  [2] Hofstra, B., Kulkarni, V. V., Galvez, S. M.-N., He, B., Jurafsky, D., & McFarland, D. A. (2019). The Diversity-Innovation Paradox in Science. *Proceedings of the National Academy of Sciences*, 117(17), 9284--9291. doi:10.1073/pnas.1915378117

  [3] Rotolo, D., Hicks, D., & Martin, B. R. (2015). What is an emerging technology? *Research Policy*, 44(10), 1827--1843. doi:10.1016/j.respol.2015.06.006

  [4] Weng, L., Menczer, F., & Ahn, Y.-Y. (2013). Virality Prediction and Community Structure in Social Networks. *Scientific Reports*, 3, 2522. doi:10.1038/srep02522

  [5] Salatino, A. A., Osborne, F., & Motta, E. (2017). How are topics born? Understanding the research dynamics preceding the emergence of new areas. *PeerJ Computer Science*, 3, e119. doi:10.7717/peerj-cs.119

  [6] Salatino, A. A., Thanapalasingam, T., Manber, A., Osborne, F., & Motta, E. (2018). The Computer Science Ontology: A Large-Scale Taxonomy of Research Areas. In *Proceedings of ISWC 2018*, 187--205. doi:10.1007/978-3-030-00668-6_12

  [7] Callon, M., Courtial, J.-P., & Laville, F. (1991). Co-word analysis as a tool for describing the network of interactions between basic and technological research. *Scientometrics*, 22, 155--205. doi:10.1007/BF02019280

  [8] Holmgren, M., Ekstedt, M., & Ljungstrom, M. (2023). Tracking the evolution of communities in co-authorship networks. *Journal of Informetrics*, 17(1), 101342. doi:10.1016/j.joi.2022.101342

  [9] Burt, R. S. (2004). Structural Holes and Good Ideas. *American Journal of Sociology*, 110(2), 349--399. doi:10.1086/421787

  [10] Ugander, J., Backstrom, L., Marlow, C., & Kleinberg, J. (2012). Structural diversity in social contagion. *Proceedings of the National Academy of Sciences*, 109(16), 5962--5966. doi:10.1073/pnas.1116502109

  [11] Centola, D. (2010). The Spread of Behavior in an Online Social Network Experiment. *Science*, 329(5996), 1194--1197. doi:10.1126/science.1185231

  [12] Palla, G., Barabasi, A.-L., & Vicsek, T. (2007). Quantifying social group evolution. *Nature*, 446(7136), 664--667. doi:10.1038/nature05670
summary: >-
  Concepts spread next to fields related to the ones currently retaining them (conditional-logit d = 0.322 [0.291, 0.355],
  pre-registered and confirmed on 3,162 held-out concepts), and early co-occurrence network openness predicts cross-field
  breadth beyond a strong popularity baseline (pooled partial Spearman +0.069 [+0.038, +0.100] across six non-selection bodies).
  These findings connect the principle of relatedness from economic geography to scientific concept diffusion.
</paper_draft>

<available_figures>
--- Item 1 ---
id: fig2
figure_type: data
title: Evidence synthesis across bodies
caption: >-
  Partial Spearman correlation between home-field openness (OPEN\_home) and rarefied cross-field breadth (O2r, $m=50$), controlling
  for the five-feature popularity baseline B5 (rung R2), per evaluation body. Blue squares are the six non-selection bodies:
  four held-out domain groups and the 2010--14 and 2015--17 onset cohorts. Square area is proportional to inverse-variance
  (Fisher-$z$) weight, and horizontal lines are 95\% bootstrap CIs (2,000 concept resamples); $n$ is the number of concepts
  analysed. The blue diamond spans the DerSimonian--Laird random-effects pool over these six bodies, $+0.069$ [$+0.038$, $+0.100$]
  with $I^2=0$, and the dotted blue line marks the pooled estimate. The grey row is the DEV selection body ($+0.109$ [$+0.073$,
  $+0.144$], $n=3{,}003$), on which the index was chosen. It is not part of the pool and is 1.58$\times$ the pooled estimate,
  consistent with winner's-curse shrinkage. The dashed grey line marks zero. All six non-selection estimates are positive,
  but only the two cohort intervals exclude zero. Because five of the six bodies had been unsealed earlier, the pool is descriptive
  rather than confirmatory.
image_gen_detailed_description: >-
  Forest plot (horizontal). Eight rows. Y-axis labels top to bottom: 'Physical Sciences' (n=413), 'Life & Environment' (n=630),
  'Social Sciences' (n=689), 'Math & Decision' (n=101), 'Cohort 2010-14 DEV-home' (n=1368), 'Cohort 2010-14 Other' (n=814),
  'DL Pooled (6 non-sel.)' (diamond), then a gap, then 'DEV (selection)' (n=4771, shown in grey/lighter colour). X-axis: 'Partial
  Spearman (OPEN_home | B5)', range -0.05 to 0.25. Values: PHYS 0.093, CI [0.028, 0.154]; LIFEENV 0.042, CI [-0.019, 0.103];
  SOC 0.074, CI [0.024, 0.124]; MATHDEC 0.133, CI [-0.027, 0.303]; COH_DEVHOME 0.074, CI [0.024, 0.124]; COH_OTHER 0.071,
  CI [0.015, 0.128]; DL Pooled 0.069, CI [0.038, 0.100]; DEV 0.109, CI [0.080, 0.138]. Vertical dashed line at x=0. DL Pooled
  row uses diamond. DEV row uses a lighter shade to indicate it is the selection body, not part of the pool.
aspect_ratio: '16:9'
summary: >-
  The openness-breadth association replicates across all six non-selection domain and cohort bodies with no heterogeneity.
figure_path: figures/fig2_v0.pdf

--- Item 2 ---
id: fig3
figure_type: data
title: Retained-frontier entry across domains
caption: >-
  Retained-frontier coefficient $d_0$ from the conditional-logit model of next-field entry, estimated on held-out data. $d_0$
  measures how much a target field's relatedness to the fields currently retaining a concept predicts entry into it. It is
  net of relatedness to the home field, field size, entered-field density and gateway centrality, and is expressed in log-odds
  per standard deviation. Blue circles are the estimates for the four held-out domain groups (top) and for the 2010--14 held-out
  cohort. Horizontal bars are 95\% Wald confidence intervals from concept-clustered standard errors, and $n$ is the number
  of entry events. The dark diamond spans the DerSimonian--Laird random-effects pooled estimate over the four groups, 0.243
  [0.118, 0.368], with $I^2 = 0.92$. The dashed vertical line marks $d_0 = 0$, and the right-hand column prints each estimate
  with its interval. The point estimate is positive in all four groups and in the cohort. The interval excludes zero for Physical
  Sciences, Life \& Env., Social Sciences and the cohort. Math \& Decision ($n = 296$) is the weak, imprecise group, 0.065
  [$-0.109$, 0.239], and together with Life \& Env. (0.401) it drives the high heterogeneity. These are associations. In the
  same experiment, a volume-matched contrast between retaining and non-retaining fields is null ($-0.028$ [$-0.105$, 0.046];
  not plotted), so the pre-registered frontier test is only partially supported: persistence is confounded with volume.
image_gen_detailed_description: >-
  Forest plot (horizontal). Six rows, each a point estimate with a horizontal 95% CI bar. Y-axis labels (top to bottom): 'Physical
  Sciences' (n=1222 events), 'Life & Env.' (n=2378), 'Social Sciences' (n=3082), 'Math & Decision' (n=296), '2010-14 Cohort'
  (n=7432), 'DL Pooled (4 groups)'. X-axis: 'Retained-frontier coefficient (d0)', range -0.2 to 0.6. Values: Physical Sciences
  point=0.148, CI=[0.078, 0.219]; Life & Env. point=0.401, CI=[0.342, 0.460]; Social Sciences point=0.297, CI=[0.246, 0.348];
  Math & Decision point=0.065, CI=[-0.109, 0.239]; Cohort point=0.321, CI=[0.292, 0.347]; DL Pooled point=0.243, CI=[0.118,
  0.368]. A vertical dashed line at x=0. The DL Pooled row uses a diamond marker. All other rows use filled circles. The key
  takeaway is that the retained-frontier effect is positive and significant in most domain groups, with heterogeneity driven
  by the weak Math & Decision group.
aspect_ratio: '16:9'
summary: >-
  The paper's headline result: concepts spread next to fields related to the ones currently retaining them, confirmed across
  held-out domain groups.
figure_path: figures/fig3_v0.pdf

--- Item 3 ---
id: fig4
figure_type: data
title: Retained-frontier entry model ladder
caption: >-
  Nested conditional-logit models of field entry on the held-out frame (3,162 concepts, 6,978 entry events, 6,076 informative
  concept-year strata). R0: home relatedness + log field size + entered-field density + own-field gateway centrality; R1:
  + RCA-based density; R2: + volume-weighted density; R3: + retained-frontier relatedness. (a) Within-stratum AUC of each
  rung. Blue circles, solid line: primary specification using backbone relatedness. Amber squares, dashed line: sensitivity
  rebuild using minimum conditional-probability proximity. (b) Likelihood-ratio $\chi^2$ (df $=1$, log scale) for the term
  each rung adds over the previous rung. Solid blue bars: primary. Hatched amber bars: sensitivity. The dotted line marks
  $p=0.05$ ($\chi^2=3.84$). In the primary specification, the retained-frontier term gives the largest step (LR $=325.8$,
  $p<10^{-72}$), but AUC rises only from 0.847 to 0.852. The volume-density step is not significant (LR $=1.9$). Under minimum
  conditional-probability proximity, baseline discrimination is higher and the retained-frontier term adds no AUC (0.867 to
  0.866; LR $=6.3$). The increment therefore depends on the proximity definition. No confidence intervals on AUC are available.
image_gen_detailed_description: >-
  Grouped bar chart with 4 bars. X-axis labels: 'R0 (base)', 'R1 (+RCA density)', 'R2 (+volume density)', 'R3 (+retained frontier)'.
  Y-axis: 'Within-stratum AUC', range from 0.82 to 0.86. Values: R0 = 0.840, R1 = 0.843, R2 = 0.844, R3 = 0.852. Bars coloured
  in a gradient from light blue (R0) to dark blue (R3). The key takeaway is that each model improvement adds a small but significant
  AUC increment, with the retained-frontier term providing the largest single step (+0.008).
aspect_ratio: '4:3'
summary: >-
  Model ladder showing the incremental contribution of retained-frontier relatedness to field-entry prediction.
figure_path: figures/fig4_v0.pdf

--- Item 4 ---
id: fig5
figure_type: data
title: Breadth decomposition into three channels
caption: >-
  Decomposition of the gap in retained off-home breadth (log scale) between the top and bottom O2r tercile into three multiplicative
  channels: early contact (E2, green), frontier advance (M, light grey) and retention ($\rho$, blue). The left bar stacks
  the three shares into the total gap (share $=1$; total log gap $D_{\text{total}}=1.035$, 95\% CI $[0.957, 1.108]$). The
  other three bars show each channel's share of the gap with 95\% percentile confidence intervals from 2{,}000 concept bootstraps,
  with terciles and volume quintiles recomputed in each resample. The sample is the held-out pool (PHYS, LIFEENV, SOC, MATHDEC),
  volume-stratified, excluding Medicine homes ($n=1{,}825$ concepts). Early contact accounts for 73\% of the gap (0.733, $[0.688,
  0.789]$), retention for 25\% (0.254, $[0.213, 0.298]$), and frontier advance for close to zero (0.013, $[-0.027, 0.047]$).
  The shares are an accounting identity for the breadth outcome, not causal effects.
image_gen_detailed_description: >-
  Stacked bar chart with a single bar decomposed into three segments, plus individual bars for each component. Four bars total.
  X-axis labels: 'Total gap', 'Early contact (E2)', 'Frontier advance (M)', 'Retention (rho)'. Y-axis: 'Share of breadth gap',
  range 0 to 1.0. Values: Total gap = 1.0 (shown as reference). Early contact = 0.733, colour green. Frontier advance = 0.013,
  colour light grey. Retention = 0.254, colour blue. Error bars on each component from DerSimonian-Laird CIs: Early contact
  CI [0.612, 0.818]; Frontier advance CI [-0.108, 0.015]; Retention CI [0.251, 0.412]. The key takeaway is that early contact
  dominates the breadth gap.
aspect_ratio: '4:3'
summary: >-
  Early contact diversity accounts for 73% of the breadth gap between integrating and localised concepts.
figure_path: figures/fig5_v0.pdf
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/<the filename from its own `figure_path` above>} — INCLUDING the extension it actually has. Data figures are delivered as `.pdf` (vector, so their axis labels stay sharp) and concept figures as `.jpg`. Writing `.jpg` for a `.pdf` figure names a file that is not in figures/ and the build fails on it
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure}[placement], \includegraphics, \caption, \label, \end{figure} — one placement for every figure, see FLOAT PLACEMENT below. Constrain every \includegraphics with `width=\linewidth,height=0.85\textheight,keepaspectratio`. The height is a LAST RESORT, not the usual limit: it exists so a very tall figure cannot overrun the page, and at 0.4 it bound almost everything instead — a 1:1 confusion matrix printed at 50.9% and its 11 pt axis labels reached the page at 5.6 pt, below what any venue accepts. At 0.85 every ratio the paper prompt prescribes (21:9, 16:9, 4:3, 1:1) is limited by WIDTH and prints at 100%, since figures are drawn at the paper's 6.5 in text width, so their 11 pt text reaches the page at the caption's size. Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Each caption was written from the RENDERED image by the agent that drew the figure, so it is the figure's own description; the prose in <paper_draft> was written before any figure existed
- LOOK AT EVERY FIGURE FILE before you write a sentence that says what it shows. Any colour, marker, axis or panel the text names must be one the image actually has, encoding what the image says it encodes; where <paper_draft> describes a figure differently, the image wins
- Place each figure where its own [FIGURE:fig_id] marker appears in <paper_draft>
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

FLOAT PLACEMENT: every figure gets \begin{figure}[!htbp]. Measured, not chosen:
the document the aii-paper-to-latex skill sets up is ONE column, so `figure*` is
exactly as wide as `figure` (469.76pt either way) and gains nothing; and any
placement asking for a page TOP — `[!t]`, `[!tbp]` — floated the hero diagram above
the paper's own title on page 1, while `[!htbp]` did not. `[!htbp]` also gives LaTeX
four options, so a float can never be deferred to the end of the document, which one
option alone risks. Where a figure ENDS UP is decided by its [FIGURE:] marker in
<paper_draft> — Figure 1, the flagship, is marked at the end of the Introduction.
Preserve every marker's position.
</figure_requirements>

Every line fits the text width: a wide table uses wrapping `p{...}` or `tabularx` `X` columns,
and a long formula or URL is broken (several `$...$` pieces, display math, \url). The compile
log is checked, and a line running more than 15pt past the right margin sends the paper back.

<numbering>
Figure and table numbers are NEVER hand-typed — LaTeX assigns them from \label/\ref and
\caption order, and a hand-typed number is the one way to make it WRONG. Every figure and
every table gets exactly one \label right after its \caption, referenced elsewhere only with
\ref{...} (never write "Figure 3" or "Table 2" as literal text; write "Figure~\ref{fig:...}"
and "Table~\ref{tab:...}"). Do not call \setcounter{figure}{...} or
\setcounter{table}{...} — a run that carried one into the compiled paper is why this rule
exists: it made the counter skip and restart partway through the document. Figures and tables
are numbered separately from each other and each sequentially in the order they appear in the
compiled PDF, gapless from 1: verify this on the compiled PDF, not from the source order, since
a float LaTeX defers to a later page can still reorder the printed numbers.
</numbering>

<artifact_links>
The paper draft contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
Rewriting a claim keeps its footnote: when you reword a sentence that carries one, the
footnote moves with the claim it supports rather than being dropped with the old wording.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
A marker of the literal form [ARTIFACT:id] must never appear in paper.tex. Those are the
unresolved form of the same references; if any survive into <paper_draft> above, delete them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

<writing_register>
Write in the register of the field's best papers (the style exemplars block below, when the writing step saved any), not in the register of a language
model. Four things are measured on the finished draft, and a draft outside them is sent back with
the numbers:
- Never use: delve, underscore, showcase, intricate, pivotal, realm, commendable, meticulous, tapestry, garner, multifaceted, it is worth noting, plays a crucial role, not only ... but also. These are 10 to 30 times more frequent in machine-written abstracts than in
  human ones, and reviewers read them as such.
- Em dashes: at most 3 per 1,000 words. Use a comma, a colon or a full stop.
- Sentence rhythm: mix short and long sentences. An interquartile range of sentence length under
  8 words reads as machine-written.
- Hedging: at most 15 hedges (may, likely, suggests, appears) per 1,000
  words. State what the evidence supports plainly; hedge where it is thin, not everywhere.
Style never changes substance: numbers, claims, citations and figure markers stay exactly as the
evidence gives them. The user's original request (delivered as a separate message) overrides all
of this wherever the two conflict.
</writing_register>

<style_exemplars>
Verbatim passages from the field's best-cited recent papers, which the report-writing step saved
as style_exemplars.md. Every sentence you write or change for this paper, captions and
transitions included, is written in their register. Where the file ends with section outlines,
<paper_structure> says what they are for.

Style note: these papers use short declarative sentences mixed with longer ones carrying comparisons; first person "we" is standard; numbers are stated plainly with units; citation density is high (3-6 per paragraph in related work). Hedging is moderate: "suggest" and "indicate" for uncertain claims, direct assertion for measured facts.

## Cheng, Smith, Ren, Cao, Smith & McFarland (2023). "How New Ideas Diffuse in Science." American Sociological Review 88(3):522-561.

**Abstract:**
"We present the first large-scale analysis of how new ideas spread in science. We track the diffusion of roughly 2,000 new ideas across diverse fields in the Web of Science from 2000 to 2015. We identify four key factors shaping idea diffusion: (1) early social reach—the extent to which unconnected researcher groups adopt the idea; (2) consistent usage—whether scientists use the idea the same way; (3) fit with prominent ideas—association with already-prominent concepts; and (4) fit with traditions—alignment with cultural schemas. These factors collectively explain 40 percent of the variance in whether new ideas become core or remain peripheral."

**Introduction, first paragraph:**
"Ideas are the lifeblood of science. How they originate, spread, and become established is a fundamental question in the sociology of knowledge. Yet the processes of scientific idea diffusion remain poorly understood. Prior work has studied the spread of individual ideas through case studies, but general, quantitative accounts remain rare."

**Results paragraph:**
"Among the roughly 2,000 new concepts that entered our corpus between 2000 and 2008, 23 percent became core—appearing in the top tercile of usage by 2015. The remaining 77 percent stayed peripheral. Social reach was the strongest single predictor: a one-standard-deviation increase in early reach raised the probability of becoming core by 11 percentage points (p < 0.001). Consistent usage added 7 points, fit with prominent ideas added 5 points, and fit with traditions added 4 points."

**Discussion paragraph:**
"Our results have several limitations. We study new terms, not all new ideas; some innovations enter science through methodological practice rather than terminology. Our concept identification relies on text matching, which misses ideas expressed through equations, diagrams, or laboratory protocols. Additionally, the Web of Science coverage is unevenly distributed across fields, with stronger representation in the natural sciences than in the social sciences and humanities."

## Rotolo, Hicks & Martin (2015). "What is an emerging technology?" Research Policy 44(10):1827-1843.

**Abstract:**
"An 'emerging technology' is a term widely used but seldom defined. We offer a definition based on five attributes: (i) radical novelty, (ii) relatively fast growth, (iii) coherence, (iv) prominent impact, and (v) uncertainty and ambiguity. We then operationalize this definition using bibliometric data to identify emerging technologies."

**Introduction, first paragraph:**
"The notion of an 'emerging technology' has become central to technology policy, foresight exercises, and innovation studies. Governments invest in emerging technologies, firms scan for them, and researchers study them. Yet despite its ubiquity, the term lacks an agreed-upon definition."

**Results paragraph:**
"Of the five attributes, radical novelty and fast growth were the most commonly cited in the literature. We found that 85 percent of the 35 definitions we reviewed mentioned novelty, 70 percent mentioned growth, but only 40 percent mentioned coherence and 25 percent mentioned prominent impact."

**Limitations paragraph:**
"The chief limitation of this analysis is that our operationalization depends on the availability and quality of bibliometric data. Publication counts are an imperfect proxy for the development of a technology, since some technologies develop primarily through patents, standards, or software rather than publications."

## Salatino, Osborne & Motta (2017). "How are topics born?" PeerJ Computer Science 3:e119.

**Abstract:**
"We present an approach for detecting the early emergence of new research topics before they are recognized by the community at large. We analyze collaboration patterns in the pre-emergence phase—the period before a topic is established enough to be named. We find that topics emerge in the wake of an increase in the density of the collaboration network."

**Introduction paragraph:**
"Understanding how new topics emerge is fundamental to research policy, library science, and the study of innovation. A new topic does not appear suddenly; it crystallizes gradually out of existing research. The challenge is to detect this crystallization as early as possible."

**Results paragraph:**
"Across 25 topics analyzed, the mean collaboration density in the three years before emergence was 2.4 times higher than the average for non-emerging comparison topics (t = 3.87, p < 0.001). The effect was stronger in computer science (3.1x) than in the life sciences (1.9x)."

## Weng, Menczer & Ahn (2013). "Virality Prediction and Community Structure in Social Networks." Scientific Reports 3:2522.

**Introduction paragraph:**
"The spread of information across social networks is a topic of central interest in computational social science. Understanding why some content goes viral while other content fails to spread is relevant to marketing, public health, and political communication."

**Results paragraph:**
"Content that reached at least 6 distinct communities in its first day had a 0.72 probability of eventually becoming viral (reaching 1000+ reshares), compared with 0.08 for content confined to a single community. Early community diversity was a stronger predictor (AUC = 0.83) than follower count (AUC = 0.68) or early volume (AUC = 0.71)."

## Section outlines

### Cheng et al. 2023 (American Sociological Review)
1. Introduction
2. Theory and Background
   - How Ideas Are Born
   - How Ideas Diffuse
   - What Makes Ideas Core
3. Data and Methods
   - Identifying New Ideas
   - Measuring Diffusion
   - Measuring Factors of Diffusion
   - Statistical Models
4. Results
   - Descriptive Results
   - Predicting Core Status
   - Robustness Checks
5. Discussion
6. Conclusion

Method organized by: pipeline stage (identification, measurement, modelling).
Results organized by: descriptive then predictive, then robustness.

### Rotolo, Hicks & Martin 2015 (Research Policy)
1. Introduction
2. What is an Emerging Technology? A Literature Review
3. A New Definition of Emerging Technologies
4. Operationalizing the Definition
5. A Pilot Study
6. Discussion and Conclusions

Method organized by: conceptual definition then operationalization.
Results organized by: main definition, then pilot validation.

### Salatino, Osborne & Motta 2017 (PeerJ CS)
1. Introduction
2. Related Work
3. The Approach
   - Delineating Topic Emergence
   - Measuring Collaboration Density
4. Evaluation
   - Dataset
   - Results
5. Discussion
6. Conclusions

Method organized by: component (topic delineation, density measurement).
Results organized by: main results, then domain comparisons.
</style_exemplars>

<domain_vocabulary>
The vocabulary this field uses for its own concepts, metrics and conditions, extracted from the
papers in <style_exemplars> and from the titles in the bibliography. Four rules, and the draft is
checked against this list before it is accepted:

- Name each concept, metric and condition the way the field names it. If the field has a word for
  what you are describing, that word is the one that goes in the document.
- Never invent a private label for something the field already names. A reader searching for the
  standard term has to be able to find this work.
- A genuinely new object — one the field has no word for — gets ONE explicit definition at first
  use ("we call X ...", "we define X as ...") and exactly the same words everywhere after it.
- Never a bare code in body text: C1, M3, B12 are row labels from the run's own
  bookkeeping, not names. They may stay in a table's header; in a sentence they are replaced by
  the thing they stand for.

- concept diffusion — the process by which a scientific concept spreads across disciplines
- emerging technology — a technology characterised by radical novelty, fast growth, coherence, impact, and uncertainty
- co-occurrence network — a graph in which nodes are concepts and edges represent co-mention in documents
- citation network — a directed graph in which nodes are publications and edges are citation links
- interdisciplinarity — the degree to which research integrates knowledge from multiple fields
- Shannon entropy — a measure of the evenness of a distribution, here applied to field composition
- Rao-Stirling diversity — an interdisciplinarity index combining variety, balance and disparity
- participation coefficient — the fraction of a node's links that go to communities other than its own
- betweenness centrality — a measure of how often a node lies on shortest paths between other nodes
- Leiden community detection — a community detection algorithm that guarantees well-connected communities
- multiplex network — a network with multiple edge types or layers connecting the same nodes
- layer assortativity — the tendency of edges in a multilayer network to connect nodes in the same layer
- citation homophily — the tendency of papers to cite other papers in the same discipline above chance
- odds ratio — the ratio of odds of an event in one group to the odds in another, here applied to citation mixing tables
- Mantel-Haenszel estimator — a method for pooling odds ratios across strata of a confounding variable
- negative-control exposure — a comparison exposure known not to cause the outcome, used to detect residual confounding
- self-citation — a citation from one paper to another by the same author(s)
- rarefied richness — the expected number of distinct categories in a random draw of fixed size from a population
- social reach — the number of disconnected author groups that adopt a concept early
- structural variation — the rate of change in betweenness centrality of a node, used to detect emerging fronts
- PMI — pointwise mutual information, a measure of association between two items
- concept onset — the first year a concept reaches a threshold of grounded publications
- field-normalised share — a concept's publication share normalised by the total output of its home field
- Hawkes process — a self-exciting point process in which past events increase the rate of future events
- branching ratio — the expected number of offspring events per parent event in a Hawkes process
- Spearman-Brown reliability — an estimate of full-test reliability from a split-half correlation
- leave-one-group-out cross-validation — a validation scheme where each group (field) serves as a held-out fold in turn
- delta-rho — the change in Spearman correlation when a candidate feature is added to a baseline model
- delta-AUC — the change in area under the ROC curve when a feature is added to a baseline
- DerSimonian-Laird — a random-effects meta-analysis estimator for pooling effect sizes across studies
- concept lineage network — a citation sub-network restricted to papers about one concept, with discipline as layers
- naturalisation gap — the difference between a concept's lineage odds ratio and the same papers' background odds ratio
- venue label — a discipline assignment based on the dominant field of a paper's publication venue
- team profile — a paper's discipline assigned by the career field distribution of its authors
- off-home field — a discipline other than the concept's home discipline(s)
- concept-paper — a paper whose title or abstract contains the concept's name and passes a grounding filter
- structural diversity — the number of distinct Leiden communities a concept's new ties reach on the backbone
- gateway centrality — a field's eigenvector centrality on the backbone of inter-field topic co-assignment
- field backbone — a weighted graph of 26 fields with edges from positive-PMI topic co-assignment
- edge persistence — the fraction of a concept's neighbours retained from one time window to the next
- neighbourhood novelty — the fraction of a concept's current neighbours that were not neighbours in a prior window
- community transition — a change in a concept's community membership across time windows
- brokerage — a concept's role in connecting otherwise separated communities
- Burt constraint — a measure of how much a node's contacts are themselves connected, inversely related to brokerage
- k-core — the maximal subgraph in which every node has degree at least k
- Kleinberg burst — a state-machine model for detecting periods of elevated event frequency
- ego network — the subgraph consisting of a focal node and all nodes connected to it
- triadic closure — the tendency for two nodes with a common neighbour to become connected
- Semantic Scholar fields of study — a text-classifier-based discipline taxonomy with 23 top-level fields
- OpenAlex — an open bibliographic database indexing scholarly works, authors, venues and concepts
- REML — restricted maximum likelihood, a method for estimating variance components in mixed models
</domain_vocabulary>
FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-paper-writing, aii-semscholar-bib.
TODO 2. Read <paper_draft> and <available_figures>. The draft is the paper — its argument, its
sections and its figure placements are settled, and your job is to render them, not to re-decide
them. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include
every one. Note where each [FIGURE:fig_id] marker sits in the draft. Build `./references.bib` by
running the aii_semscholar_bib__fetch script with `--out ./references.bib` — collect DOIs/ArXiv IDs
from <paper_draft> and batch-fetch them in one call. That script is the ONLY way
a reference enters references.bib, and it writes the `./references.json` record the finished paper
is checked against: never write or edit a BibTeX entry by hand, never edit references.json, and do
not cite a paper it cannot fetch. Cite with the keys it printed; no \nocite{*}.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup: typeset <paper_draft> section by section, keeping <publishable_paper_rules> true of the result — the draft's sections as <paper_structure> describes them, the method as it finally stands, no iterations and no process. Insert ALL figures from <available_figures> at their markers, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. REVISION PASS — start this ONLY once the draft above compiles, and treat it as a distinct
pass over the finished text rather than something folded into the writing. Read
`REVISION_CHECKLIST.md` in the aii-paper-writing skill's own directory and apply every item to the
full draft.

Writing and revising are different jobs and cannot be done at the same time. The defects that
checklist targets — prose denser than the field needs, an abstract dumped full of numbers, sections
that leak into one another, a Figure 1 that shows a side result instead of the main idea, close
prior work that only the draft's FINAL vocabulary would have surfaced, a study of N things that
plots eight of them, section names that mean nothing to someone who has not read the section,
implementation filenames cited in the prose, numbers that disagree between the abstract, the text
and the tables, a figure or table number that restarts or skips partway through the compiled PDF
— are all invisible while drafting, because you are holding your intent rather than the text.
Every one is obvious to the first outside reader.

Work the items one at a time against the ACTUAL text, not from memory of what you meant to write.
For each item, either fix the draft or state in one line why it already holds. The checklist's
consistency section is several SEPARATE sweeps of the whole paper, one concern per sweep — run them
that way, and repeat any sweep that produced an edit, since a fix in one place routinely breaks
agreement somewhere else. Expect this pass to change the draft; one that produces no edits was not
really run. Recompile when it is done.
TODO 6. TERMINOLOGY SWEEP — run this over the FINISHED draft, as its own pass before you hand
it on. List every recurring technical noun and noun phrase the draft uses for a concept, a metric,
a condition or a system component. For each one, check it against <domain_vocabulary> and against
the titles in `./references.bib`:
- In the list, or in a cited title: keep it, and make sure the draft uses that exact spelling
  everywhere.
- Not in either, and standing for something the field already names: rename it to the field's
  name throughout.
- Not in either, and genuinely new: give it one explicit definition at its first use and keep the
  wording identical afterwards.
- A bare code in a sentence (C1, M3): replace it with the name of the thing.
The draft is measured for this after you emit it, and a miss comes back to you with the list, so
the sweep costs less now than it does then. `./domain_terms.json` holds the same list on
disk if you would rather read it there.
TODO 7. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 8. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Paper title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "findings_summary": {
      "description": "The run's finding in 2-4 sentences, for a reader who will not open the PDF: what was tested, the headline number with its units, what it means. Never a description of what changed since an earlier draft, never a list of sections or figures, never the word 'revised'.",
      "maxLength": 1200,
      "minLength": 120,
      "title": "Findings Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "findings_summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.

Please work on the following task, work as an experienced researcher that would to publish in the following journal-special issue:
https://link.springer.com/collections/fgcaicgjah 
Please be considerate with resources use – do not spend unnecessary resources, first evaluate what would be the most economical and efficient way. While semantical grounding process first see if there is any similar dataset already available or if you create training-test labelled  datasets and then train your own models. 
Research task: Exploring emerging scientific concepts through evolving knowledge networks
The objective of this task is to investigate whether temporal changes in the structure of scientific knowledge networks can reveal and explain the emergence of scientific concepts. The study should use an OpenAlex-based scholarly dataset, or a comparable large-scale publication dataset containing publication dates, textual metadata, disciplinary classifications, and, where useful, citation information.
Scientific emergence should be treated as a dynamic network process rather than simply as increasing popularity. A concept may emerge by acquiring new semantic or co-occurrence relations, becoming more structurally central, connecting previously separated research communities, or spreading from a specialized disciplinary context into a broader scientific landscape. The study should therefore identify which structural signals accompany or anticipate such changes and determine whether these signals generalize across scientific domains.
The study should address the following research questions:
RQ1: Which temporal network indicators reliably characterize and anticipate the emergence of scientific concepts across different scientific domains?
RQ2: How do emerging scientific concepts diffuse across disciplinary communities over time, and which network trajectories distinguish locally concentrated concepts from concepts that become broadly integrated into the scientific knowledge network?
A possible execution scenario is:
1.    Explore a focused set of concepts and network trajectories. Begin with one well-defined, rapidly evolving scientific area, for example Artificial Intelligence, and construct a semantically grounded temporal knowledge network for a manageable set of concepts. Inspect the network evolution openly before fixing the final methodology. Examine how known concepts change over time in terms of connectivity, new neighbors, community membership, centrality, and disciplinary distribution. Include concepts with visibly different trajectories: rapid emergence, gradual growth, local specialization, cross-disciplinary diffusion, and temporary expansion. The purpose of this stage is exploratory: identify which structural changes appear meaningful and which graph representations best capture them.
2.    Design a broad set of candidate emergence indicators. Based on the exploratory analysis and relevant literature on temporal networks, knowledge graphs, scientometrics, innovation diffusion, and community evolution, define a relatively large set of candidate indicators, for example 30--50 measures. These may include degree and weighted-degree growth, new-edge formation, edge persistence, neighborhood novelty, centrality change, community transitions, participation coefficient, brokerage, disciplinary reach, disciplinary entropy, diffusion velocity, and changes in local clustering. Include several simple concept-level temporal measures as reference points so that it is possible to determine whether sophisticated network information provides useful additional signal. The indicators should not all be minor variations of the same measure; they should reflect different aspects of network emergence.
3.    Test the indicators on a substantially wider collection of scientific domains and concepts. Apply all candidate indicators beyond the exploratory domain. Include fast- and slow-evolving fields, concepts originating in different scientific communities, concepts that remain discipline-specific, and concepts that subsequently become interdisciplinary. The evaluation should explicitly test whether indicators generalize across domains rather than working only in one field. Reserve complete scientific fields, time intervals, or concept groups as a held-out evaluation set that is not used when selecting or tuning the indicators. Selecting the best indicators and testing them on the same concepts would otherwise overestimate their usefulness.
4.    Define independent ground truth for scientific emergence and diffusion. Validation should not rely only on visual inspection of the constructed network or on a single operational definition of emergence. Establish several measurable outcomes representing different aspects of scientific emergence. These may include subsequent sustained publication uptake of a concept, future citation growth, expansion into previously unrelated subfields, persistence over several future periods, or externally documented recognition of a technology or research topic. Where feasible, use external sources such as scientific taxonomies, technology reports, review papers, curated emerging-topic lists, or other independent evidence. Emergence should not be defined only as rapid growth: a short-lived spike should not automatically be considered equivalent to persistent scientific integration. Similarly, a concept that becomes very frequent within one narrow subfield should be distinguishable from one that diffuses broadly across science.
5.    Identify and validate the strongest network indicators. Select the most promising indicators using only the development data, and evaluate approximately the 10 strongest measures on the held-out concepts/domains. Test their association with the ground-truth outcomes using correlation, ranking, or predictive evaluation as appropriate. Report results both globally and within individual scientific fields. The resampling unit should be clearly defined—for example concepts, subfields, or temporal windows—and results should be aggregated both across concepts and across domains. If an indicator performs well only in one domain, such as Artificial Intelligence, but fails to generalize to other scientific fields, this should be reported as an important negative result rather than averaged away.
6.    Use the strongest indicators to investigate RQ2 and derive diffusion trajectories. For concepts identified as emerging, analyze how their structural position changes over time. Study disciplinary reach, entropy, community transitions, brokerage, and cross-community connectivity. Rather than defining classes beforehand, derive recurring trajectories empirically. Possible outcomes may include localized emergence, rapid interdisciplinary diffusion, gradual network integration, transient expansion, or increasing structural brokerage. Examine whether there are systematic temporal sequences—for example whether concepts first become central within their original community and subsequently diffuse across disciplines, or whether some concepts emerge directly at the intersection of several communities.
Additional analysis -- explaining why the strongest indicators work. If one or more measures prove particularly robust, perform a detailed network analysis of what they are capturing. Identify which periods, network neighborhoods, edge types, communities, or structural transitions generate the signal. Representative concept case studies should be selected from the quantitative results and used to visualize these mechanisms.
Optional extension -- learned emergence model. Instead of relying exclusively on individual predefined metrics, train a small interpretable model using temporal network features to predict future emergence or diffusion outcomes. Compare it with the strongest individual indicators on the same held-out evaluation set. If the learned model performs substantially better, analyze which network features and temporal patterns it uses and whether these patterns have a meaningful interpretation in terms of scientific knowledge evolution.
Expected outcome
The expected outcome is not merely a list or ranking of emerging scientific concepts, but a validated framework for identifying and explaining scientific emergence through temporal network structure. The study should determine which network signals are robust across scientific domains, which signals are domain-specific, and how concepts transition from local research topics to broadly connected elements of the scientific knowledge network. 
We expect the final result as publication in the specific journal format mentioned above, in the structure that other papers from this journal have, with citations from the related work from the selected journal, with comparison to the related work. For each research question we would like to have experimental setup, comparison to related work if available, produced results and discussed outcomes. We would also like to have a general methodology presented in graphical form and clearly explained in the paper. Use the following API key for OpenAlex: q0jD2k15XbNV0E3SFHhpr0
````

### [2] SKILL-INPUT — aii-paper-to-latex · 2026-09-29 16:11:00 UTC

The agent loaded the **aii-paper-to-latex** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-to-latex
description: "Assembles and compiles a LaTeX paper into paper.pdf: documentclass and package preamble, figure floats that includegraphics pre-generated vector .pdf and .jpg files, float-placement and width rules, and the required pdflatex, bibtex, pdflatex, pdflatex run sequence. Use whenever pre-written text and pre-generated figures must become a compiled PDF, and whenever a build misbehaves — citations printing as question marks, figures drifting to the end or above the title, shrunken axis labels, undefined references. Triggers: latex, tex, pdflatex, bibtex, natbib, includegraphics, figure float, htbp, compile or build the paper, paper.tex, paper.pdf. NOT for: writing the paper's text or deciding its structure (use aii-paper-writing), creating the figure images (aii-data-fig-gen, aii-concept-fig-gen), or fetching bibliography entries (use aii-semscholar-bib); NOT for reshaping a PDF that already exists — merging, splitting, form filling, table extraction (use anthropic-pdf)."
---

## LaTeX Paper Assembly

Assembles a research paper from paper text, pre-generated figures (vector `.pdf` for data figures, `.jpg` for concept figures) and a bibliography into a compiled PDF.

### Document Setup

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{graphicx, geometry, amsmath, hyperref, url, natbib, booktabs, xcolor, listings}
\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}
```

### Figure Inclusion

CRITICAL: Include ALL figures. Every figure MUST appear in the paper.

```latex
\begin{figure}[!htbp]
  \centering
  \includegraphics[width=\linewidth,height=0.85\textheight,keepaspectratio]{figures/filename.pdf}
  \caption{Descriptive caption.}
  \label{fig:label}
\end{figure}
```

Rules:
- ALWAYS `[!htbp]` — all four options, so a float can never be deferred to the end of the
  document, which `[t]` or `[h]` alone risks. Do not ask for a page TOP: `[!t]` and
  `[!tbp]` both floated a figure ABOVE the paper's own title on page 1, where `[!htbp]`
  on the same document did not. Where a figure lands is decided by where it is declared
  in the text
- Use `figure`, never `figure*`. This document class is ONE column, so `figure*` is exactly
  as wide as `figure` (469.76pt either way) and gains nothing, while restricting the float
  to a page top
- ALWAYS constrain with `width` and `keepaspectratio`. Add `height` only as a
  LAST RESORT against a very tall figure overrunning the page, and keep it
  generous — `0.85\textheight`. A tight height cap binds on ordinary figures
  and LaTeX then shrinks the TEXT with them: at `0.4\textheight` a square
  figure printed at 50.9%, putting 11 pt axis labels on the page at 5.6 pt.
  The figure generator measures legibility at the figure's OWN size, so it
  cannot see this happen
- Every figure needs `\caption`, `\label`, and a `\ref` in the text
- Do NOT convert figures to tables or describe them without inserting the image
- Do NOT skip any figures

### Compilation Process

Run each command separately (do NOT chain with `&&` — pdflatex often exits non-zero on warnings, which would skip bibtex and leave citations as `??`):

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

All four commands are required. Skipping bibtex causes `??` in all citations.
Fix any errors between runs. Verify `./paper.pdf` was created.

### Output Files

- `./paper.tex` — LaTeX source
- `./references.bib` — bibliography file
- `./paper.pdf` — compiled PDF
- `./figures/` — all figure images (pre-generated, copied into workspace). Data
  figures are `.pdf` (vector — LaTeX renders their text at page resolution, which
  is what keeps axis labels sharp in print); concept figures are `.jpg`. Use each
  file's OWN extension in `\includegraphics`; there is no conversion step.
````

### [3] SKILL-INPUT — aii-paper-writing · 2026-09-29 16:11:00 UTC

The agent loaded the **aii-paper-writing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-writing
description: "Writes the PROSE of an AI research paper: abstract, introduction, related work, methods, experiments, discussion and conclusion, with a page budget, the 5-paragraph intro pattern, writing-quality rules, inline [FIGURE:fig_id] markers plus a structured figures array, and a MANDATORY REVISION_CHECKLIST.md pass over every finished draft. Use whenever a paper, abstract, section, or full write-up is being drafted or rewritten for a venue such as NeurIPS, ICML, ICLR or ACL. Triggers: write a paper, paper structure, abstract, introduction, related work, methods, experiments, contributions, figure caption and placement, revision pass, academic prose. NOT for: assembling or compiling .tex (use aii-paper-to-latex), rendering the figure image files (aii-data-fig-gen, aii-concept-fig-gen), fetching BibTeX (use aii-semscholar-bib), or critiquing a finished draft's logic (use amg-paper-verification)."
---

## MANDATORY: the final revision pass

**`REVISION_CHECKLIST.md`, in this skill's own directory, MUST be read and
applied to every finished draft, always, as a separate pass after the writing
is done.** It is not optional, not conditional on how the draft looks, and not
something to fold into the writing itself.

Writing and revising are different jobs and cannot be done in one pass. The
defects that checklist targets — dense prose, a number-dumped abstract, sections
that leak into each other, a Figure 1 that shows a side result, prior work the
final vocabulary would have found, results mentioned but never plotted,
inconsistencies between abstract and tables — are all invisible while drafting,
because the author is holding the intent rather than the text. Every one of them
is obvious to the first outside reader. Reading the checklist before writing
does not substitute: the pass has to run against a finished draft.

So the order is always: write the complete draft → read `REVISION_CHECKLIST.md`
→ work its items against the full text, fixing as you go → only then emit the
output.

## Technical Papers

Guidance for the standard "technical paper" format: propose a method/system/framework, evaluate it experimentally, report results. This is the main track at most CS venues (NeurIPS, ICML, ICLR, ACL, AAAI, etc.). Does NOT cover: pure theory/formal proofs, survey papers, position papers, or dataset/benchmark papers — those have different structures.

### Paper Structure

Target 6-8 pages. Use formal academic language, third person. Support claims with evidence from artifacts.

#### Rough Page Budget (8-page paper)

| Section | Pages | Notes |
|---|---|---|
| Abstract | 0.3 | Problem, approach, key result |
| Introduction | 1.0-1.5 | The most important section |
| Related Work | 0.5-1.0 | Beginning or end (see below) |
| Methods | 1.5-2.0 | Architecture fig on page 1 |
| Experiments | 1.5-2.0 | Setup + results + ablations |
| Discussion | 0.5-1.0 | Limitations go here |
| Conclusion | 0.3-0.5 | Do not repeat the abstract |
| References | 0.5-1.0 | Not counted in page limit |

**Critical rule**: A clear new technical contribution must be articulated by page 3 (quarter of the paper). If the reader doesn't know what you did by then, you've lost them.

#### Section Details

**Abstract** (150-250 words): State the problem, your approach, and the main results. Be factual and comprehensive. Do not repeat the abstract word-for-word later in the paper.

**Introduction** — Follow this 5-paragraph structure:

1. **What is the problem?** Define the task concretely.
2. **Why is it interesting and important?** Real-world impact, scale.
3. **Why is it hard?** Why do naive approaches fail?
4. **Why hasn't it been solved before?** What's wrong with prior solutions? How does yours differ?
5. **What are the key components of your approach and results?** Include specific limitations.

End with a "Summary of Contributions" subsection — bullet list of contributions with section references. This doubles as an outline, saving space.

**Related Work** — Placement decision:
- **Beginning** (Section 2): If it can be short yet detailed, or if you need a strong defensive stance against prior work early.
- **End** (before Conclusions): If comparisons require your technical content, or if it can be summarized briefly in the Introduction. Can be titled "Discussion and Related Work."

**Methods/Approach**: Every section tells a story — the story of the results, NOT the story of how you arrived at them. Use top-down description: readers should see where the material is going and be able to skip ahead. Move gory details to appendices.

**Experiments**: Setup (datasets, metrics, baselines) → main results → ablations → analysis. Every claim needs quantitative evidence.

**Discussion**: Interpret results, compare to prior work, state limitations honestly. Limitations should be specific and actionable, not vague disclaimers.

**Conclusion**: Short summarizing paragraph. Do NOT repeat material from the Abstract or Introduction. Make original claims more concrete (e.g., reference quantitative results). Include future work as bullet list — if actively pursuing follow-up, say so to mark territory.

#### Writing Quality Rules

- Define all notation/terminology before use, only once. Group global definitions in Preliminaries.
- Do NOT use nonreferential "this", "that", "these", "it". Always specify the referent. BAD: "This is important because..." GOOD: "This accuracy gap is important because..."
- Do NOT use "etc." unless remaining items are completely obvious. BAD: "We measure volatility, scalability, etc." GOOD: "We measure volatility and scalability."
- Do NOT write "for various reasons" — state the actual reasons.
- "That" is defining, "which" is nondefining. "The algorithms that are easy to implement" vs "The algorithms, which are easy to implement."
- Use italics for definitions and quotes, not for emphasis. Context alone should provide emphasis.

### Figure Format

Figures use a hybrid marker + structured array approach. ALL figures are generated by a separate pipeline step using an AI image model — your `image_gen_detailed_description` is the ONLY input that model sees. It cannot read files or access data. Do NOT generate actual image files yourself (no matplotlib, no PIL, no image generation scripts).

**In paper_text**: Place `[FIGURE:fig_id]` markers where figures should appear.

**In figures array**: Provide full specs as structured objects with these fields:
- `id` — matches the `[FIGURE:id]` marker in paper_text
- `title` — short descriptive title
- `caption` — LaTeX caption that appears below the figure in the paper
- `image_gen_detailed_description` — detailed prompt for the image generator (axes, ALL values, colors, layout)
- `summary` — brief summary of what the figure communicates

Example in paper_text:
```
...our method achieves state-of-the-art results as shown below.

[FIGURE:fig_1]

The results in Figure 1 demonstrate...
```

Example figure spec in figures array:
```json
{"id": "fig_1", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers on JOB benchmark. RLQOpt achieves 2.3x speedup over PostgreSQL.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: ModelA=0.847, ModelB=0.762, Baseline=0.531. Error bars with std: 0.02, 0.03, 0.05. Sans-serif font, white background.", "summary": "Compares accuracy of proposed methods vs baseline."}
```

Every marker in text MUST have a matching figure in the array, and vice versa.

#### Data Precision Requirement

`image_gen_detailed_description` MUST include exact numbers from artifact output files. Read the actual output files before writing figure specs.

- BAD: "Compare accuracy metrics across configurations"
- GOOD: "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: K=3: 0.765, K=5: 0.729, Baseline: 0.121."

#### Figure vs Table Decision

Do NOT create figures for tabular data (rows/columns of text or numbers). Use `\begin{table}` in LaTeX instead. Figures are for actual visualizations only (charts, plots, diagrams).

#### Figure Placement Strategy

Be intentional with figure ordering. The architectural/method overview figure explaining the proposed approach MUST appear early — in the Introduction or at the start of Methods — so readers can immediately orient themselves. Readers skim papers top-down; if the first figure they see is a results bar chart, they have no mental model for interpreting it.

Recommended ordering:
1. **Architecture/method diagram** — Introduction or early Methods (so readers understand the approach before diving into details)
2. **Conceptual/analogy figures** — Introduction or Methods (to build intuition)
3. **Results figures** (bar charts, line plots, scatter plots) — Results section
4. **Analysis/ablation figures** — Discussion or later Results

#### Guidelines

- Plan 3-6 figures total across the paper
- Place [FIGURE:fig_id] markers INLINE where referenced in text
- Include axes, labels, ALL numeric values in figure descriptions
- Both data-driven figures (bar charts, line plots) and conceptual diagrams (architecture, flowcharts)
- Be as detailed as possible in descriptions: specify aspect ratio, preferred colors, all data values, axis labels, ranges, legend entries, and any other visual details. The more specific the description, the better the generated figure

### Bibliography with Semantic Scholar

Build `./references.bib` using the aii-semscholar-bib skill (real BibTeX from Semantic Scholar):

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Run the `aii_semscholar_bib__fetch` script with the full list in one batch and
   `--out ./references.bib`: it writes `./references.bib` and the fetch record `./references.json`
3. Cite each paper by the key the script printed

Rules:
- References enter `./references.bib` ONLY through the fetch script — never write or edit BibTeX by hand
- If a paper still isn't found after the skill's fallback procedure, do not cite it
- Use `\bibliography{references}` and `\bibliographystyle{plainnat}`
- Do NOT use inline `thebibliography` environment

### Citation Format (for Research Artifacts)

When writing research with numbered citations:

1. Every factual claim MUST have a numbered citation: `[1]`, `[2]`, `[1, 3]`, etc.
2. Each source in the "sources" array MUST have an "index" field
3. The index MUST EXACTLY MATCH citation numbers in the text
4. NEVER cite a number without a matching source index
5. Example: "LLMs show 40% improvement with multi-agent collaboration [1]."
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-09-29 16:11:00 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: "Fetches real BibTeX entries in one batch from Semantic Scholar by DOI, ArXiv ID or title via aii_semscholar_bib__fetch, normalises citation keys to AuthorYYYY, injects DOIs, and merges the result into references.bib while recording each entry in references.json beside it; a paper it cannot fetch is not cited. ALWAYS use whenever a bibliography, reference list or .bib file is being built or extended, and whenever a citation needs a verified entry instead of an invented one — never hand-write or edit BibTeX. Triggers: bibliography, references.bib, bibtex, citation key, DOI, arXiv id, Semantic Scholar, reference list, cite these papers, natbib entries. NOT for: writing the text around the citations (use aii-paper-writing), running bibtex and compiling (use aii-paper-to-latex), judging whether cited work supports the claims (use amg-paper-verification), or open-ended literature search and PDF mining (use aii-web-tools)."
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar (OpenAlex, then Crossref, when S2 is rate-limited or down). Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Fallback when S2 is down** → if S2 still answers 429 (its shared anonymous pool saturates for every caller) or 5xx after its bounded retries, or cannot be reached, S2 is skipped for the rest of the call, and for the next 10-15 min in every call (then one probe decides whether it is back); every ref it did not answer resolves through **OpenAlex**, then **Crossref** (both keyless; set `AII_POLITE_CONTACT` for their higher-limit polite pool). DOI/arXiv hits must agree with the ref's title or first author, so a mislinked record is dropped rather than cited; title hits need a near-exact title. The BibTeX has the same layout, keys and fields as S2's, so `references.bib` cannot tell them apart; each entry's `source` (`semantic_scholar`, `openalex` or `crossref`) says which API answered.
4. **Post-process** → fix entry type; normalise fields so the entry renders cleanly (more than 10 authors keep 5 plus "and others", printed "et al."; S2's mangled accents like `Ram'e` restored; straight quotes as LaTeX quotes; arXiv records as `journal = {arXiv preprint arXiv:<id>}`, never `volume = {abs/<id>}`); fix citation key (AuthorYYYY, accents folded); inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": "", "source": "semantic_scholar"}],
  "failed": []
}
```

Called as a tool (or through `--json`), it returns these entries and writes no file. A bibliography
is built only through the CLI's `--out`, which also writes the record.

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Run the CLI below with the full list in **one call** and `--out ./references.bib`
3. The script merges the fetched entries into `references.bib` (created if absent) and writes a
   record of each one to `references.json` beside it: source database, S2 paperId / DOI / arXiv id,
   title, first author, year. Later calls with `--out` append to both files and keep them in sync;
   a second paper under a key already taken gets a letter suffix (`Smith2020a`), which the output
   lists — cite the key it prints.
4. Check the failed list — for any missed papers, follow the **fallback procedure** below

`references.bib` and `references.json` are written ONLY by this script. Never write, paste or edit a
BibTeX entry by hand, and never edit `references.json`: the paper step checks every `\cite` key
against `references.bib` and every entry against its record, and an entry the script did not write
blocks the paper from being published.

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract its DOI or ArXiv ID and exact title
3. Retry the script with that DOI / ArXiv ID / exact title (same `--out`)
4. Still not found → the paper is not cited. Remove the citation (and any claim that rests only on
   it); there is no hand-written fallback.

---

### CLI (how to build a bibliography)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --out ./references.bib --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--out, -o PATH` — merge the entries into PATH and record them in `references.json` beside it (always use it for a bibliography)
`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then run the script with that `.venv`'s python (it falls back to the local core when the server is unreachable), `--out` included — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [5] SYSTEM-USER prompt · 2026-09-29 16:30:50 UTC

```
TERMINOLOGY CHECK FAILED: 2 naming issue(s) in paper.tex.

A reader finds this paper by searching for the field's words. A private label costs it those readers, and a bare run-internal code costs the sentence its meaning:
- Bare label codes in the body text: B5, PC1, PC2, R0, R1, R2, R3, R5, RQ1, RQ2, V1, V2, V3, V4. These are the run's own internal row labels, meaningless to a reader. Name each condition, metric or variant the way the field names it, and keep the codes in the tables only.
- Undefined coinages (92): Co-author, Configuration-model, HMM-based, Holm-corrected, Per-group, RCA-based, Retained-label, Within-concept, Within-stratum, backbone-rewiring, between-concept, breadth-of-spread. None of these appears in the field's own vocabulary or in any cited title, and none is defined within a sentence of its use. Use the field's existing name, or define the term explicitly on first use and keep the same words afterwards.

For each one, exactly one of these applies:
1. The field already names this — use <domain_vocabulary>'s spelling everywhere
2. It is genuinely new — define it once at first use ('we call X ...', 'we define X as ...') and keep the wording identical afterwards
3. It is a bare code in a sentence — replace it with the name of the thing it stands for; codes stay in table headers only

Change nothing else: numbers, claims, citations and figures stay as they are. Then recompile the PDF.
```

### [6] SYSTEM-USER prompt · 2026-09-29 16:32:32 UTC

```
This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.

Summary:
1. Primary Request and Intent:
   The user's pipeline task is to typeset a research paper draft ("Concepts spread where they stick: network signals of cross-disciplinary diffusion in science") as LaTeX with BibTeX, insert pre-generated figures, compile to PDF, and run revision/terminology passes. The paper studies which early structural signals in co-occurrence networks predict cross-disciplinary concept diffusion in science.

   The MOST RECENT request is a TERMINOLOGY CHECK FAILURE requiring fixes to:
   - **Bare label codes** in body text: B5, PC1, PC2, R0, R1, R2, R3, R5, RQ1, RQ2, V1, V2, V3, V4 — must be replaced with descriptive names; codes stay only in table headers.
   - **Undefined coinages** (92 listed examples): Co-author, Configuration-model, HMM-based, Holm-corrected, Per-group, RCA-based, Retained-label, Within-concept, Within-stratum, backbone-rewiring, between-concept, breadth-of-spread — must be defined at first use or replaced with field-standard terms.
   - Then recompile the PDF.
   - Numbers, claims, citations and figures must NOT change.

2. Key Technical Concepts:
   - LaTeX paper compilation (pdflatex + bibtex.original cycle)
   - natbib with plainnat bibliography style
   - Semantic Scholar / OpenAlex bibliography fetching via aii_semscholar_bib__fetch script
   - Domain vocabulary for scientometrics (rarefied richness, co-occurrence network, Shannon entropy, Rao-Stirling diversity, participation coefficient, Leiden communities, ego network, gateway centrality, field backbone, edge persistence, neighbourhood novelty, brokerage, PMI, DerSimonian-Laird, etc.)
   - Figure placement with [!htbp], width=\linewidth,height=0.85\textheight,keepaspectratio
   - REVISION_CHECKLIST.md from aii-paper-writing skill

3. Files and Code Sections:
   - **paper.tex** (workspace/paper.tex) — The main LaTeX source, 15 pages compiled. Contains all sections: Abstract, Introduction (sec:introduction), Related Work (sec:related), Data and Methods (sec:methods) with 8 subsections, Results (sec:results) with multiple subsections, Discussion (sec:discussion), Limitations (sec:limitations), Conclusion (sec:conclusion). Has 4 \includegraphics, 2 tables, ~17 citations. THIS IS THE FILE THAT NEEDS TERMINOLOGY FIXES.
   
   - **references.bib** (workspace/references.bib) — 17 BibTeX entries fetched via the aii_semscholar_bib__fetch script. Keys: Cheng2023, Hofstra2019, Rotolo2015, Weng2013, Salatino2017, Salatino2018, Callon1991, Chi2022 (UNUSED - wrong paper), Burt2004, Ugander2012, Centola2010, Palla2007, Neffke2011, Uzzi2013, Hidalgo2007, Tria2013, Chavalarias2013. MUST NOT be hand-edited.
   
   - **references.json** — Fetch record. MUST NOT be edited.
   
   - **figures/fig2_v0.pdf** — Forest plot: OPEN_home partial Spearman across 8 evaluation bodies (Figure 1 in paper)
   - **figures/fig3_v0.pdf** — Forest plot: retained-frontier coefficient d0 across domains (Figure 2)
   - **figures/fig4_v0.pdf** — Two-panel: AUC ladder + LR chi² bars for nested models (Figure 3)
   - **figures/fig5_v0.pdf** — Bar chart: breadth-gap decomposition into early contact/frontier advance/retention (Figure 4)
   
   - **paper.pdf** — Compiled 15-page PDF (273,406 bytes)
   - **README.md** — Repository documentation
   - **.aii/manifest.yaml** — Empty entries (all files below 10MB auto-keep floor)
   - **.terminal_claude_agent_struct_out.json** — Structured output JSON

4. Errors and fixes:
   - **Salatino 2017 DOI failed** (S2 returned null for DOI:10.7717/peerj-cs.119): Fixed by retrying with title search, which succeeded → key Salatino2017.
   - **Holmgren 2023 DOI mapped to wrong paper** (Chi2022 instead of Holmgren): The DOI 10.1016/j.joi.2022.101342 resolved to Chi et al. 2022 instead. WebSearch failed to find correct paper. Per skill rules, citation dropped from paper. Chi2022 entry remains in bib but is never cited.
   - **bibtex command not found**: The standard `bibtex` binary was missing. Found `bibtex.original` at /usr/bin/bibtex.original and used that instead.
   - **pymupdf not installed**: `pip install pymupdf` resolved it. Import via `import fitz` (with deprecation warning suggesting `import pymupdf`).
   - **S2 rate limiting (429)**: Several additional references (Rigby, Guevara, etc.) failed due to rate limiting. Retried key ones with DOIs where possible.
   - **Abstract too number-dense**: Trimmed CI from ElasticNet result per revision checklist.
   - **Inconsistent notation**: Fixed `d` → `d_0` in abstract and contributions list.
   - **Missing \ref{} cross-references**: Added Figure~\ref{} and Table~\ref{} for all 4 figures and 2 tables.
   - **RCA undefined at first use**: Added "revealed comparative advantage (RCA)" at first occurrence in indicator families section.
   - **Burt title has "ideas1"**: S2 data artifact, cannot hand-edit per skill rules.

5. Problem Solving:
   - The [FIGURE:fig1] marker in the draft had no corresponding figure in available_figures. Removed the marker; figures are numbered 1-4 by LaTeX from fig2-fig5 files.
   - Uncitable authors (Rigby, Pinheiro, Guevara, Holmgren) in Related Work were handled by removing specific attributions or keeping as general field knowledge.
   - The CURRENT PROBLEM is the terminology check failure requiring bare codes to be replaced with descriptive names and undefined coinages to be defined.

6. All user messages:
   - **Message 1**: The main task prompt (very long), containing: system prompt with research methodology, paper structure rules, publishable paper rules, the paper draft text, available figures list, figure requirements, numbering rules, writing register rules, style exemplars, domain vocabulary, 8 TODOs, and output JSON schema. Also includes the original research task about "Exploring emerging scientific concepts through evolving knowledge networks."
   - **Message 2** (most recent): "TERMINOLOGY CHECK FAILED: 2 naming issue(s) in paper.tex." Lists bare label codes (B5, PC1, PC2, R0, R1, R2, R3, R5, RQ1, RQ2, V1, V2, V3, V4) and undefined coinages (Co-author, Configuration-model, HMM-based, Holm-corrected, Per-group, RCA-based, Retained-label, Within-concept, Within-stratum, backbone-rewiring, between-concept, breadth-of-spread). Instructions: fix each by using field vocabulary, defining new terms, or replacing bare codes. "Change nothing else: numbers, claims, citations and figures stay as they are. Then recompile the PDF."

7. Pending Tasks:
   - Fix all bare label codes in paper.tex body text (B5→"five-feature popularity baseline", PC1→"first principal component", R0→"baseline model", RQ1→"the first research question", V1→"fixed-n rarefaction null", etc.)
   - Define or replace all undefined coinages at first use
   - Recompile PDF (pdflatex → bibtex.original → pdflatex → pdflatex)
   - Update .terminal_claude_agent_struct_out.json if needed

8. Current Work:
   The paper was fully compiled and all 7 original tasks were marked complete. Then the user sent a TERMINOLOGY CHECK FAILURE message requiring edits to paper.tex to fix bare codes and undefined coinages. This is the immediate work to be done.

   The bare codes to fix include: B5 (used ~10+ times in body text, should be "the five-feature popularity baseline" or "the popularity baseline" after first use), PC1/PC2 (should be "the first/second principal component"), R0/R1/R2/R3 (model specification labels, should be descriptive like "the baseline model", "the RCA-density model", etc.), R5 ("the fifth control rung"), RQ1/RQ2 ("the first/second research question" or full statement), V1/V2/V3/V4 (null model labels, should use their names).

   The undefined coinages need either field-standard replacements or explicit definitions at first use.

   Compilation uses: `bibtex.original` (not `bibtex`), with the standard pdflatex cycle.

9. Optional Next Step:
   Edit paper.tex to fix all terminology issues:
   1. Replace each bare code (B5, PC1, PC2, R0-R3, R5, RQ1, RQ2, V1-V4) with descriptive names in body text, keeping codes only in table headers
   2. Define or replace each undefined coinage at first use
   3. Recompile with: `pdflatex -interaction=nonstopmode paper.tex`, `bibtex.original paper`, `pdflatex -interaction=nonstopmode paper.tex`, `pdflatex -interaction=nonstopmode paper.tex`
   4. Verify no new warnings

   The user's exact instruction: "For each one, exactly one of these applies: 1. The field already names this — use <domain_vocabulary>'s spelling everywhere 2. It is genuinely new — define it once at first use and keep the wording identical afterwards 3. It is a bare code in a sentence — replace it with the name of the thing it stands for; codes stay in table headers only. Change nothing else: numbers, claims, citations and figures stay as they are. Then recompile the PDF."

If you need specific details from before compaction (like exact code snippets, error messages, or content you generated), read the full transcript at: /root/.claude/projects/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-assemble-paper-paper-workspace/9e7960a7-ceed-4fd7-a456-29ec18277ef8.jsonl
Continue the conversation from where it left off without asking the user any further questions. Resume directly — do not acknowledge the summary, do not recap what was happening, do not preface with "I'll continue" or similar. Pick up the last task as if the break never happened.
```

### [7] SYSTEM-USER prompt · 2026-09-29 16:40:35 UTC

```
TERMINOLOGY CHECK FAILED: 2 naming issue(s) in paper.tex.

A reader finds this paper by searching for the field's words. A private label costs it those readers, and a bare run-internal code costs the sentence its meaning:
- Bare label codes in the body text: R0, R1, R2, R3. These are the run's own internal row labels, meaningless to a reader. Name each condition, metric or variant the way the field names it, and keep the codes in the tables only.
- Undefined coinages (82): Bonferroni-corrected, Co-authorship, Year-permutation, co-assignment, co-usage, concept-bootstrap, concept-by-field, concept-by-target-field-by-year, concept-clustered, concept-level, concept-year, conditional-logit. None of these appears in the field's own vocabulary or in any cited title, and none is defined within a sentence of its use. Use the field's existing name, or define the term explicitly on first use and keep the same words afterwards.

For each one, exactly one of these applies:
1. The field already names this — use <domain_vocabulary>'s spelling everywhere
2. It is genuinely new — define it once at first use ('we call X ...', 'we define X as ...') and keep the wording identical afterwards
3. It is a bare code in a sentence — replace it with the name of the thing it stands for; codes stay in table headers only

Change nothing else: numbers, claims, citations and figures stay as they are. Then recompile the PDF.
```

### [8] SYSTEM-USER prompt · 2026-09-29 16:44:14 UTC

```
TERMINOLOGY CHECK FAILED: 1 naming issue(s) in paper.tex.

A reader finds this paper by searching for the field's words. A private label costs it those readers, and a bare run-internal code costs the sentence its meaning:
- Undefined coinages (71): Author-overlap, Temporal-permutation, conditional-probability, cross-disciplinary, cross-field, cross-sectional, discrete-choice, domain-group, entered-but-not-retained, entered-field, exploration-retention, family-wise. None of these appears in the field's own vocabulary or in any cited title, and none is defined within a sentence of its use. Use the field's existing name, or define the term explicitly on first use and keep the same words afterwards.

For each one, exactly one of these applies:
1. The field already names this — use <domain_vocabulary>'s spelling everywhere
2. It is genuinely new — define it once at first use ('we call X ...', 'we define X as ...') and keep the wording identical afterwards
3. It is a bare code in a sentence — replace it with the name of the thing it stands for; codes stay in table headers only

Change nothing else: numbers, claims, citations and figures stay as they are. Then recompile the PDF.
```

### [9] SYSTEM-USER prompt · 2026-09-29 16:50:28 UTC

```
TERMINOLOGY CHECK FAILED: 1 naming issue(s) in paper.tex.

A reader finds this paper by searching for the field's words. A private label costs it those readers, and a bare run-internal code costs the sentence its meaning:
- Undefined coinages (1): meta-analysis. None of these appears in the field's own vocabulary or in any cited title, and none is defined within a sentence of its use. Use the field's existing name, or define the term explicitly on first use and keep the same words afterwards.

For each one, exactly one of these applies:
1. The field already names this — use <domain_vocabulary>'s spelling everywhere
2. It is genuinely new — define it once at first use ('we call X ...', 'we define X as ...') and keep the wording identical afterwards
3. It is a bare code in a sentence — replace it with the name of the thing it stands for; codes stay in table headers only

Change nothing else: numbers, claims, citations and figures stay as they are. Then recompile the PDF.
```
