# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_full_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-09-29 23:07:03 UTC

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
  result, discussion, conclusion, captions, the website and the interactive page.
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
Your workspace: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_assemble_paper/paper/workspace`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_assemble_paper/paper/workspace/`:
GOOD: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_assemble_paper/paper/workspace/file.py`, `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_assemble_paper/paper/workspace/results/out.json`
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
The paper's sections, in this order:
Abstract, Introduction, Related Work, Method, Results, Discussion, Limitations, Conclusion, then the numbered references.
</paper_structure>

<paper_draft>
THE PAPER. Which single finding it argues, how it is structured, which figures it shows and where
each one goes were all decided before you were called; this block is the result. Typeset it. The
first typesetting pass does not restructure it, re-select what it covers, or add sections it does
not have. Rewording for the register the style blocks below describe is in scope; changing what the
paper says is not. The REVISION PASS todo is the one place the draft may move, and only within the
limits that todo sets.

title: >-
  Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
abstract: >-
  We ask which early structural signals in a concept's topic co-occurrence network anticipate later cross-field breadth. Using
  the OpenAlex bulk snapshot, we identify 12,499 concepts by title matching across 26 scientific fields, track 27,393 adoption
  episodes, and screen 53 early network indicators from six families against a five-feature popularity baseline on held-out
  field groups. Seven indicators survive held-out validation and compose into an openness index (OPEN) that measures a concept's
  early tendency to acquire novel, community-spanning co-occurrence partners; two of the seven carry negative signs. The Eval4
  descriptive pool of OPEN_home over 6 non-selection bodies gives partial Spearman +0.069 [95% CI +0.038, +0.100], I-squared
  = 0, 6/6 positive; evidence state is lead. The association behaves like a static topical-dispersion property of the home
  neighbourhood: temporal turnover is untested rather than refuted (V2 excess split-half reliability below 0.05). A within-concept
  closure test is null on development data and opposite-signed on held-out fields. Separately, on the Exp7 independent frame
  (EXP5 minus EXP6; 11,841 concepts, 6,978 entry events in 6,076 informative strata), a conditional logit on field-entry events
  shows that concepts spread next to fields related to the ones currently retaining them: d0 = 0.322 [0.291, 0.355]. The pre-registered
  verdict is FRONTIER = PARTIAL: the volume-matched contrast is null and the coefficient reverses under minimum-conditional-probability
  proximity. Early contact diversity accounts for most of the breadth gap; no discrete trajectory typology passes the naming
  rule.
paper_text: |
  \documentclass[sn-mathphys-num]{sn-jnl}

  \usepackage[utf8]{inputenc}
  \usepackage[T1]{fontenc}
  \usepackage{amsmath,amssymb}
  \usepackage{graphicx}
  \usepackage{booktabs}
  \usepackage{natbib}
  \usepackage[colorlinks=true,citecolor=blue,linkcolor=blue,urlcolor=blue]{hyperref}
  \usepackage{caption}
  \usepackage{multirow}
  \usepackage{array}
  \usepackage{xcolor}

  \title{Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts}

  \author{AI Inventor}

  \date{}

  \begin{document}

  \maketitle

  \begin{abstract}
  We ask which early structural signals in a concept's topic co-occurrence network anticipate later cross-field breadth. Using the OpenAlex bulk snapshot (476 million works), we identify 12,499 concepts by Aho--Corasick title matching across 26 scientific fields and track 27,393 adoption episodes. We screen 53 early network indicators from six families against a five-feature popularity baseline on held-out field groups \footnote{Code: \url{https://github.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/tree/fork/run_DVtwwCx0JbFq/round-3/experiment-8}}. Seven survive held-out validation and compose into an openness index (OPEN) that measures a concept's early tendency to acquire novel, community-spanning co-occurrence partners; two carry negative signs (early retention ratio and ego-network density). The Eval4 descriptive pool of OPEN$_{\text{home}}$ over 6 non-selection bodies  gives partial Spearman $+0.069$ $[+0.038, +0.100]$, $I^2 = 0$, 6/6 positive; the evidence state is lead. The association behaves like a static topical-dispersion property: a within-concept permutation null absorbs year-to-year churn, but the temporal-excess measure has split-half reliability below 0.05, so temporal turnover is untested rather than refuted. A within-concept closure test is null on development data and opposite-signed on held-out fields. Separately, on the Exp7 independent frame (EXP5 minus EXP6; 11,841 concepts, 6,978 entry events in 6,076 informative strata) \footnote{Code: \url{https://github.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/tree/fork/run_DVtwwCx0JbFq/round-3/experiment-7}}, a conditional logit on field-entry events shows that concepts spread next to fields related to the ones currently retaining them: $d_0 = 0.322$ $[0.291, 0.355]$. The pre-registered verdict is FRONTIER = PARTIAL: the volume-matched contrast is null and the coefficient reverses under minimum-conditional-probability proximity. Early contact diversity accounts for 73\% of the breadth gap; no discrete trajectory typology passes the naming rule.
  \end{abstract}

  \keywords{co-occurrence networks \and cross-disciplinary diffusion \and knowledge spread \and principle of relatedness \and scientific concepts \and temporal networks \and topic emergence}


  \section{Background}
  \label{sec:background}

  Some scientific concepts remain confined to their home discipline for decades, while others cross field boundaries within a few years. Optogenetics, born in neuroscience, entered genetics, psychiatry and bioengineering; deep learning, rooted in computer science, now appears in medicine, materials science and linguistics. Understanding what distinguishes broadly spreading concepts from locally absorbed ones matters for science policy, research evaluation and the design of interdisciplinary programmes \citep{Fortunato2018,Hofstra2019}. If early structural signals predict later cross-field integration, funders and institutions could identify concepts with high diffusion potential before that diffusion is observable in publication counts alone.

  The problem is hard because simple popularity metrics (publication volume, growth rate, share of papers outside the home field) already explain much of the variance in later breadth \citep{Rotolo2015}. Any network indicator must add information \emph{beyond} these baselines. Network science offers a rich toolkit for studying how information, behaviour and innovations spread through structured populations \citep{Leitch2019,Milli2018}. In citation and co-authorship networks, knowledge diffusion follows structured pathways that reflect both the topology of the network and the position of the spreading entity within it \citep{Domenico2016,Renoust2017}. Community structure shapes diffusion outcomes: bridge nodes and boundary-spanning ties accelerate spread across groups \citep{Cherifi2019,Burt2004}, while community cohesion can either facilitate or retard it depending on the contagion mechanism \citep{Centola2010,Ugander2012}.

  Prior work has proposed several candidate signals for concept diffusion. \citet{Cheng2023} tracked roughly 2{,}000 new ideas across Web of Science fields and found that early social reach, the number of disconnected researcher groups, was the strongest predictor of whether an idea became ``core.'' Their ideational consistency measure predicted next-year volume. \citet{Weng2013} showed that early community diversity predicts virality of online content (AUC 0.83). \citet{Salatino2017} showed that collaboration density rises before topic emergence, and \citet{Chavalarias2013} used phylomemetic methods to track the branching and merging of scientific fields. \citet{Gao2018} tracked community evolution in patent co-occurrence networks, revealing how technological change reshapes network structure. \citet{Sattar2023} developed approaches for detecting the temporal evolution of communities, and \citet{Callon1991} introduced co-word analysis as a tool for mapping research structure. These studies typically operate on curated concept sets without held-out validation, mix concept-level and field-level units of analysis, or do not control for simple volume-based predictors. No prior study has screened a broad set of temporal knowledge-network indicators against a shared baseline on held-out field groups for the specific outcome of size-adjusted cross-disciplinary breadth.

  A second open question concerns the routes by which concepts move between fields. The principle of relatedness, established for regional economic diversification \citep{Hidalgo2007,Boschma2011,Fitzgerald2021}, predicts that actors diversify into activities related to their existing portfolio. For scientific fields adopting new concepts, this principle has been tested for entry but not for the role of currently \emph{retaining} fields---those that have adopted a concept and kept publishing on it. Whether concepts spread next to fields related to the ones currently retaining them, beyond relatedness to the home field alone, is untested.

  This paper addresses both questions with a large-scale empirical study. We identify 12{,}499 concepts from the OpenAlex bulk snapshot, compute 53 early network indicators across six families, and test them on held-out field groups and a confirmatory onset cohort. We also build a conditional logit model of field entry that tests whether retained-field relatedness predicts the next field a concept enters. We report the following contributions:

  \begin{enumerate}
      \item We screen 53 early co-occurrence network indicators against a five-feature popularity baseline and confirm seven on held-out field groups for predicting rarefied cross-field breadth. Two of the seven carry negative signs: early retention ratio and ego-network density.
      \item We introduce the OPEN index, a six-component composite of early co-occurrence openness, and test it on a 2015--2017 cohort never used in selection. The Eval4 descriptive pool of OPEN$_{\text{home}}$ over 6 non-selection bodies gives partial Spearman +0.069 [+0.038, +0.100], $I^2 = 0$, 6/6 positive; the evidence state is lead.
      \item We test whether concepts spread next to fields related to the ones currently retaining them . On the Exp7 independent frame (EXP5 minus EXP6; 11,841 concepts, 6,978 entry events in 6,076 informative strata), the retained-frontier coefficient is $d_0 = +0.322$ $[+0.291, +0.355]$. The pre-registered verdict is FRONTIER = PARTIAL: the volume-matched contrast is null, the coefficient reverses under minimum-conditional-probability proximity, and the held-out dose response is not monotone. Persistence and volume remain confounded.
      \item We show that early neighbourhood consolidation, measured by Cheng et al.'s (2023) ideational consistency, predicts volume growth but \emph{narrower} cross-field reach, a reversal that holds in all five field groups.
      \item We decompose breadth into exploration and retention channels and show that early contact diversity accounts for 73\% of the breadth gap. No discrete trajectory typology passes the naming rule; diffusion paths form a continuum along a breadth axis.
  \end{enumerate}




  \section{Methods}
  \label{sec:methods}

  \subsection{Concept identification and panel construction}

  We use the OpenAlex bulk snapshot (2026-09-23; 476{,}196{,}327 works; 129.4 million base works 1995--2022). Concepts are identified by Aho--Corasick title matching of 56{,}643 legacy OpenAlex concepts (levels 2--5) plus Wikidata aliases, with stemmed verification. A per-concept LLM precision gate drops concepts with precision below 0.80.

  A concept's \emph{onset year} $t_0$ is the first year it reaches 20 grounded publications. \emph{Home field(s)} are the field(s) holding at least 40\% of the first 30 grounded papers. The specification was frozen on DEV data (hash-sealed before held-out scoring) and unsealed once. The panel comprises 12{,}499 concepts and 27{,}393 concept-by-field adoption episodes (Table~\ref{tab:panel}).

  \begin{table}[ht]
  \centering
  \caption{Panel composition. DEV concepts have home fields in Computer Science, Engineering, Biochemistry/Genetics/Medicine. Held-out groups cover the remaining field families.}
  \label{tab:panel}
  \small
  \begin{tabular}{lrr}
  \toprule
  Split & Concepts & Episodes \\
  \midrule
  DEV (CS/Eng/BGM/Med, onset 2003--2009) & 4{,}771 & 9{,}079 \\
  Cohort (onset 2010--2014, all fields) & 4{,}356 & 9{,}799 \\
  Held-out Physical Sciences & 742 & 1{,}662 \\
  Held-out Life \& Environment & 1{,}113 & 3{,}099 \\
  Held-out Social Sciences & 1{,}352 & 3{,}320 \\
  Held-out Math \& Decision Sci. & 165 & 434 \\
  \midrule
  \textbf{Total} & \textbf{12{,}499} & \textbf{27{,}393} \\
  \bottomrule
  \end{tabular}
  \end{table}

  \subsection{Outcome: rarefied field breadth}

  The primary outcome is \emph{rarefied field breadth} $O_{2r}$ ($m = 50$): the expected number of distinct venue fields among a fixed-size random draw of $m$ papers from a concept's publications in years $t_0 + 6$ to $t_0 + 8$, computed by exact hypergeometric rarefaction. Rarefaction separates size-adjusted breadth from sheer volume. Secondary outcomes include sustained uptake ($O_{1c}$), transience ($O_3$), and field- and year-normalised citation growth ($O_4$).

  \subsection{Baseline and indicator families}
  \label{sec:indicators}

  We define a \emph{five-feature baseline} (B5) consisting of log early volume, publication growth, non-home share, Shannon entropy and field reach, all computed over $t_0$ to $t_0 + 2$. The 53 candidate indicators span six families:

  \begin{enumerate}
      \item \textbf{Co-occurrence ego-network (A, 27 indicators):} degree, density, persistence, novelty, community counts, participation, brokerage from the concept's ego network on the co-occurrence backbone.
      \item \textbf{Popularity and volume (E, 6 indicators):} publication growth, author growth, author count.
      \item \textbf{Disciplinary spread (F, 3 indicators):} Shannon entropy of field distribution, home-field relatedness, Rao--Stirling diversity.
      \item \textbf{Retained frontier (FR, 7 indicators):} contact reach, retention ratio, RCA-based and volume-weighted field densities.
      \item \textbf{Gateway centrality (G, 7 indicators):} eigenvector centrality of home and early off-home fields on the field backbone.
      \item \textbf{Co-author reach (S, 3 indicators):} author overlap with other concepts, connected components among co-authors.
  \end{enumerate}

  \subsection{The OPEN index}

  The OPEN index is the mean of six signed $z$-scored ego-network components from the early window ($t_0$ to $t_0 + 2$):

  \begin{enumerate}
      \item New edge rate (positive sign): the fraction of a concept's co-occurrence neighbours that are new.
      \item Number of Leiden communities reached ($n_{\text{comm}}$, positive): how many distinct topic communities a concept's neighbours span.
      \item Participation coefficient (positive): the share of a concept's ties that cross community boundaries.
      \item Neighbourhood novelty residual (NOV$_{\text{res}}$, positive): the novelty of a concept's co-occurrence partners after residualising on degree.
      \item Ego density (negative sign): the density of the concept's local co-occurrence subgraph.
      \item Edge persistence (negative sign): the fraction of the concept's neighbours retained across windows.
  \end{enumerate}

  The $z$-score constants are frozen from the DEV data. We test three builds: OPEN$_{\text{home}}$ (home-field co-occurrence graph only), OPEN$_{\text{all}}$ (corpus-wide graph), and OPEN$_{\text{sizematch}}$ (corpus-wide papers subsampled to home counts).

  \subsection{Statistical framework}

  Indicator screening uses \emph{partial Spearman priority} (PSP): the Pearson correlation of rank-transformed indicator and outcome residuals, both residualised on the baseline covariates and control rungs. Inference uses 2{,}000 concept-level bootstrap resamples with refit. Pooling across field groups uses the DerSimonian--Laird random-effects estimator \citep{Dersimonian1986} with $I^2$ heterogeneity reporting \citep{Higgins2002}. Multiple comparisons use Holm correction across the pre-declared family.

  We also define NOVCHURN as the mean of $z$(NOV$_{\text{res}}$) and $-z$(edge persistence), a two-component novelty/churn measure used in mechanism analyses.

  \subsection{Field-entry model (RQ2)}

  For the field-entry analysis, we use a conditional logit (Breslow partial likelihood) on concept-year risk sets, stratified by concept-year, with standardised covariates: relatedness to home, log field size, density over entered fields, gateway centrality (baseline R0); RCA-based density (R1); volume-weighted density (R2); and retained-field relatedness $d_0$ (R3). A field is ``retaining'' a concept when it has published at least two grounded papers on the concept in each of the two most recent years. Relatedness is measured by positive pointwise mutual information (PMI) on the field-level backbone. The specification is frozen on DEV and scored once on the independent held-out frame.


  \section{Results}
  \label{sec:results}

  The headline finding is the openness--breadth association: the Eval4 descriptive pool of OPEN$_{\text{home}}$ over 6 non-selection bodies gives partial Spearman $+0.069$ $[+0.038, +0.100]$, $I^2 = 0$, 6/6 positive; the evidence state is lead. We present the indicator screen (RQ1) first because it defines the OPEN index.

  \subsection{RQ1: Which early network signals predict cross-field breadth?}

  \subsubsection{Experimental setup}

  The top 10 indicators selected on DEV by partial Spearman priority for rarefied breadth ($O_{2r}$, $m = 50$) were tested once on four held-out field groups and two cohort splits. Confirmation requires Holm-corrected $p < 0.05$ and a 95\% CI excluding zero on the DerSimonian--Laird pooled estimate. The held-out outcomes had been previously used by two earlier experiments, so the indicator-screen results are robustness checks within the same frame rather than fully independent confirmations. The fresh 2015--2017 cohort is the only body never used in any prior step.

  \subsubsection{Comparison to related work}

  Prior network-based diffusion studies in \emph{Applied Network Science} have examined knowledge flow through citation and co-authorship networks \citep{Domenico2016,Renoust2017}, community-driven diffusion mechanisms \citep{Cherifi2019,Milli2018}, and temporal community evolution \citep{Sattar2023,Gao2018}. These studies model diffusion at the network level but do not screen concept-level co-occurrence indicators against a held-out validation framework for the specific outcome of size-adjusted breadth. \citet{Weng2013} showed that early community diversity predicts online virality (AUC 0.83); our study extends this to scientific concepts, where the baseline is much stronger (B5 Spearman 0.65--0.86). \citet{Cheng2023} found that social reach predicts whether ideas become ``core,'' but did not control for a shared baseline or use held-out field groups. \citet{Fitzgerald2021} showed that academic knowledge is becoming more localised, motivating the question of which early signals distinguish concepts that overcome this localisation.

  \subsubsection{Results}

  Seven of the 53 screened indicators survive held-out validation with Holm correction (Table~\ref{tab:screen}) . These span two families: retained frontier (end-of-window field density, volume-weighted field density, contact reach, retention ratio) and co-occurrence topology (community count, neighbourhood novelty residual, ego density). No centrality or volume-only indicator survives. Two confirmed indicators carry negative signs: the early retention ratio ($-$0.114, concepts with higher early field retention spread \emph{less} broadly) and ego density ($-$0.102, concepts with denser co-occurrence neighbourhoods spread less).

  \begin{table}[ht]
  \centering
  \caption{Held-out indicator screen: the 10 indicators with highest DEV partial Spearman priority for rarefied breadth ($O_{2r}$, $m = 50$), tested on held-out groups. DerSimonian--Laird pooled estimates with 95\% CI. Confirmed indicators (Holm $p < 0.05$ and CI excluding zero) are marked.}
  \label{tab:screen}
  \small
  \begin{tabular}{llccccc}
  \toprule
  Indicator & Family & Pooled PSP & 95\% CI & $I^2$ & Sign & Conf. \\
  \midrule
  M0\_density\_end & FR & +0.375 & [+0.279, +0.462] & 0.74 & 6/6 & \textbf{Yes} \\
  D\_vol\_end & FR & +0.307 & [+0.256, +0.356] & 0.10 & 6/6 & \textbf{Yes} \\
  CONTACT\_REACH & FR & +0.211 & [+0.161, +0.261] & 0.00 & 6/6 & \textbf{Yes} \\
  $n_\text{comm}$ (W3) & A & +0.167 & [+0.063, +0.267] & 0.78 & 6/6 & \textbf{Yes} \\
  NOV$_{\text{res}}$ & A & +0.151 & [+0.044, +0.255] & 0.75 & 6/6 & \textbf{Yes} \\
  RETENTION\_RATIO & FR & $-$0.114 & [$-$0.160, $-$0.067] & 0.00 & 6/6 & \textbf{Yes} \\
  ego\_density (W3) & A & $-$0.102 & [$-$0.151, $-$0.053] & 0.00 & 6/6 & \textbf{Yes} \\
  Rao--Stirling & G & $-$0.072 & [$-$0.153, +0.010] & 0.44 & 5/6 & No \\
  $G_\text{btw}$ & G & +0.056 & [$-$0.006, +0.118] & 0.33 & 6/6 & No \\
  log offhome vol. & F & $-$0.089 & [$-$0.171, $-$0.007] & 0.63 & 5/6 & No \\
  \bottomrule
  \end{tabular}
  \end{table}

  About half of the M0\_density\_end and D\_vol\_end signal is a pre-onset footprint: on held-out data, the post-onset-only field density attenuates from +0.374 to +0.187 [+0.145, +0.246]. The remaining indicators measure genuinely early structural properties.

  An ElasticNet combining all indicators adds Spearman +0.059 [+0.046, +0.073] over B5 on held-out groups; an Explainable Boosting Machine adds +0.052 [+0.037, +0.067].

  \textbf{OPEN index confirmation.} The OPEN index was tested on a 2015--2017 onset cohort \footnote{Code: \url{https://github.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/tree/fork/run_DVtwwCx0JbFq/round-4/experiment-10}} (1{,}443 concepts) never used in any prior screen. We define a six-rung control ladder that tests OPEN's partial Spearman with rarefied breadth under increasingly demanding baselines (Table~\ref{tab:ladder}).

  \begin{table}[ht]
  \centering
  \caption{OPEN index control ladder on the 2015--2017 confirmatory cohort. PSP = partial Spearman priority with rarefied breadth ($O_{2r}$, $m = 50$), 95\% concept-bootstrap CI.}
  \label{tab:ladder}
  \small
  \begin{tabular}{lccccccc}
  \toprule
  Build & R0 & R1 & R2 & R3 & R4 & R5 & $n$ \\
  \midrule
  OPEN$_{\text{home}}$ & +.12 & +.10 & +.09 & +.08 & +.07 & +.06 & 573 \\
  OPEN$_{\text{all}}$ & +.21 & +.18 & +.17 & +.17 & +.15 & +.14 & 630 \\
  OPEN$_{\text{size}}$ & +.18 & +.15 & +.15 & +.14 & +.12 & +.11 & 591 \\
  \bottomrule
  \end{tabular}
  \end{table}

  OPEN$_{\text{home}}$ passes the primary concept-type rung (R2: PSP = +0.091, 95\% CI [+0.013, +0.171], Holm $p$ = 0.048) but its DerSimonian--Laird pooled interval includes zero (+0.083 [$-$0.007, +0.173]), making the home-only signal marginal. The paired difference OPEN$_{\text{all}}$ minus OPEN$_{\text{home}}$ at the footprint rung is +0.093 [+0.016, +0.169]; about half of this gap is paper count (OPEN$_{\text{sizematch}}$ minus OPEN$_{\text{home}}$ = +0.053 [$-$0.015, +0.117]). OPEN$_{\text{all}}$ is partly mechanically coupled to the outcome because early off-home papers that enter the ego network are also papers that determine later breadth.

  An evidence synthesis across six non-selection bodies (four held-out domain groups plus the 2010--2014 and 2015--2017 cohorts) gives a DerSimonian--Laird pooled OPEN$_{\text{home}}$ partial Spearman of +0.069 [+0.038, +0.100] with $I^2 = 0$, all six bodies positive. The DEV estimate (+0.109) shows shrinkage of 1.58$\times$ relative to the non-selection pool.

  [FIGURE:fig_evidence_synthesis]

  \textbf{Vocabulary-free replication (Frame~N).} To address survivorship bias in the legacy concept vocabulary, we mined 636 vocabulary-free phrase-born concepts \footnote{Code: \url{https://github.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/tree/fork/run_DVtwwCx0JbFq/round-5/experiment-13}} (2003--2015 onsets). These newborns have 14\% lower breadth and 89\% higher transience than legacy concepts. On Frame~N, OPEN$_{\text{home}}$ gives PSP +0.117 [+0.020, +0.218] at R3 for $O_{2r}$ ($m = 30$); the frozen verdict is PARTIAL: the R5 confidence interval includes zero (+0.086 [$-$0.009, +0.190]), three of four estimable groups are positive, and the Holm-corrected $p$-value is 0.052. Edge persistence is null on Frame~N ($-$0.013); the signal is carried by neighbourhood novelty (NOV$_{\text{res}}$ +0.208 [+0.113, +0.303]).

  \textbf{The consistency--breadth reversal.} We rebuilt Cheng et al.'s (2023) ideational consistency on OpenAlex topic co-usage for 12{,}311 concepts . In their design (next-year volume, no current-size control), the model reproduces their estimate: $b = 0.428$ (+53.5\%/SD). Adding current volume removes almost all of it: +1.3\% [+0.5\%, +2.1\%], a residual-to-raw ratio of 0.021. Net of B5, the partial Spearman of consistency with rarefied breadth is $-$0.069 [$-$0.093, $-$0.047] on the pooled bodies ($I^2 = 0$, 5/5 groups negative), replicating on the 2015--2017 cohort ($-$0.111 [$-$0.197, $-$0.030]). The consistency measure has Spearman +0.77 with edge persistence (Jaccard similarity); it is essentially weighted persistence, confirming that a stable neighbourhood predicts growth but not breadth.

  \subsubsection{Discussion of RQ1}

  The confirmed indicators divide into two groups. Contact reach, retention ratio and the field-density measures capture a concept's position in the inter-field backbone and partly reflect a pre-onset footprint. Community count, neighbourhood novelty and ego density capture the topology of the early home-field co-occurrence neighbourhood. The OPEN index combines these into a single measure of early openness. The practical forecasting gain is small: OPEN$_{\text{home}}$ adds only +0.002 Spearman on the fresh cohort. The indicators characterise structural preconditions for broad diffusion rather than providing individually actionable forecasts. Life \& Environment Sciences show the weakest OPEN signal (PSP +0.042 vs pooled +0.069), warranting domain-specific investigation.


  \subsection{RQ2: By what routes do concepts spread across fields?}

  \label{subsec:rq2_entry}
  \subsubsection{Experimental setup}

  We test whether relatedness to the fields currently retaining a concept predicts which field it enters next, using a conditional logit on concept-year risk sets with an independent frame of 11{,}841 concepts (6{,}978 entry events in 6{,}076 informative strata). The frame excludes all concepts used in the original frame construction (Experiment 6). The specification was hash-sealed on DEV before held-out scoring. Pre-registered criteria include: pooled R3 CI above zero, positive in the majority of evaluable groups, volume-matched contrast CI above zero, retained-label permutation null rejected, backbone-rewiring null rejected, and dose-response non-negative.

  \subsubsection{Comparison to related work}

  \citet{Hidalgo2007} showed that product-space relatedness predicts economic diversification; the minimum conditional probability defines the standard proximity. \citet{Boschma2011} extended the principle of relatedness to regional and technological diversification, and \citet{Fitzgerald2021} showed how regional knowledge networks shape academic localisation. Our contribution is to test whether relatedness to the set of fields currently \emph{retaining} a concept predicts entry, beyond relatedness to the home field and conventional density measures. The key methodological distinction is that retention, not mere presence, defines the reference set.

  \subsubsection{Results}

  On the independent held-out frame , the retained-frontier coefficient is $d_0 = 0.322$ [0.291, 0.355] with concept-clustered standard errors (R3 vs R2 likelihood-ratio 325.8, $p < 10^{-70}$). The result is positive in three of three evaluable held-out groups: Physical Sciences +0.148, Life \& Environment +0.401, Social Sciences +0.297. Mathematics \& Decision Sciences is null (+0.065 [$-$0.109, 0.239], 165 concepts). DerSimonian--Laird pooled $d_0$ = 0.243 [0.118, 0.368], $I^2 = 0.92$ (Table~\ref{tab:entry}).

  \begin{table}[ht]
  \centering
  \caption{Retained-frontier coefficient ($d_0$) from the conditional-logit model of field entry, by domain group and cohort. The pre-registered verdict is PARTIAL: criterion 5 (volume-matched CI $> 0$) fails.}
  \label{tab:entry}
  \small
  \begin{tabular}{lccc}
  \toprule
  Model & $d_0$ & 95\% CI (concept) & LR \\
  \midrule
  Development set & 0.228 & [0.164, 0.291] & 34.5 \\
  Held-out pooled & 0.322 & [0.291, 0.355] & 325.8 \\
  Physical Sciences & 0.148 & [0.078, 0.219] & -- \\
  Life \& Environment & 0.401 & [0.342, 0.460] & -- \\
  Social Sciences & 0.297 & [0.246, 0.348] & -- \\
  Math \& Decision Sci. & 0.065 & [$-$0.109, 0.239] & -- \\
  2010--2014 cohort & 0.321 & [0.292, 0.347] & -- \\
  \bottomrule
  \end{tabular}
  \end{table}

  The retained-frontier coefficient survives the conventional RCA density ($D_{\text{rca}}$) and a share-weighted current presence density: adding $d_0$ after both rivals gives LR = 34.5 on DEV, and $D_{\text{rca}}$ is absorbed once $d_0$ enters. All three specificity tests reject their nulls after Holm correction (retained-label permutation $p = 0.001$; backbone-rewiring $p = 0.004$; node-label $p = 0.003$).

  However, the pre-registered verdict is PARTIAL. The volume-matched contrast (comparing entry rates of retained versus entered-but-not-retained fields in the same volume cell) is null: $-$0.028 [$-$0.105, +0.046] on held-out data ($-$0.008 on DEV; Holm $p$ = 0.76). The dose response by retention age on held-out data is 0.098 / 0.075 / 0.304, which is not monotone. Under minimum-conditional-probability proximity \citep{Hidalgo2007} instead of PMI, $d_0 = -0.021$ ($p = 0.012$), while RCA density becomes strong (LR 246). Persistence is therefore confounded with volume, and the result is backbone-specific.

  \textbf{Gateway centrality.} Gateway centrality does not predict field retention: on 27{,}393 held-out episodes, the increment is effectively zero ($\Delta$AUC $-$0.00001, 95\% CI [$-$0.0006, +0.0003]).

  \textbf{Breadth decomposition.} On 3{,}188 DEV concepts \footnote{Code: \url{https://github.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/tree/fork/run_DVtwwCx0JbFq/round-4/experiment-12}}, the breadth gap between the top and bottom $O_{2r}$ terciles decomposes as: early contact diversity 77.9\%, frontier advance $-$4.6\% (broad concepts gain new fields at similar rates), and retention 26.8\%. The difference between exploration and retention is 0.464 [0.407, 0.528]. On the held-out pool excluding Medicine (variant iv), the contact share is 0.633 [0.537, 0.727] and the difference is 0.504 [0.329, 0.679] ($I^2 = 0.76$). These shares are an accounting identity for the breadth outcome, not causal effects, because breadth and contact diversity share papers.

  \textbf{Diffusion trajectories.} No discrete trajectory typology passes the naming rule . DTW $k$-medoids and HMM-based clustering on state sequences give an adjusted Rand index of 0.222. PCA reveals a continuum: PC1 (38.8\% of variance) is a breadth axis, PC2 (10.7\%) is a keep-versus-lose axis. Early openness (OPEN) correlates with PC1 beyond B5 (held-out partial 0.120, $I^2 = 0$) but not with PC2 (partial $-$0.07 to $-$0.11).

  \textbf{Sequence and closure tests.} A home-prominence half-peak vs off-home take-off test finds no signal beyond the mechanical lag (DEV excess $-$0.009 [$-$0.015, $-$0.003], held-out +0.011 [0.005, 0.016]). Intersection-born concepts take off later (HR 0.47 [0.42, 0.54]). A within-concept closure test (Experiment 15C) is null on DEV \footnote{Code: \url{https://github.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/tree/fork/run_DVtwwCx0JbFq/round-5/experiment-15}} (density PPML $b = -0.070$ [$-$0.180, 0.040]; OPEN$_{\text{home}}$ $b = +0.015$ [$-$0.038, 0.069]). On held-out fields, OPEN$_{\text{home}}$ is opposite-signed ($-$0.079 [$-$0.146, $-$0.013]). Early openness is a between-concept trait, not a within-concept mechanism.

  [FIGURE:fig_entry]

  \subsubsection{Discussion of RQ2}

  The retained-frontier result extends the principle of relatedness to concept adoption. The positive coefficient is large and consistent across three of three evaluable groups, but the PARTIAL verdict limits its interpretation: we cannot fully separate persistence from sustained volume as a predictor of field entry. The effect is also backbone-specific: it holds on the sparse PMI backbone but not under the standard Hidalgo proximity. The breadth decomposition shows that integrating and localised concepts differ primarily in how many fields they contact early, not in how many more fields they enter later. The null closure test and opposite-signed held-out result indicate that openness does not operate as a within-concept mechanism driving diffusion.


  \subsection{Confound analysis}
  \label{sec:confound}

  The openness signal could be an artefact of small yearly samples or of dynamic churn. We tested four null models \footnote{Code: \url{https://github.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/tree/fork/run_DVtwwCx0JbFq/round-5/experiment-16}}:

  \textbf{Fixed-size rarefaction.} Subsampling to 10 home papers per year retains 68\% of the pooled association. The bias-corrected Chao estimator retains 91\%.

  \textbf{Within-concept permutation null.} The excess churn over a 200-draw within-concept year-label permutation null is indistinguishable from zero: excess NOVCHURN pooled PSP = +0.008 [$-$0.02, +0.03], compared to raw NOVCHURN = +0.116 [+0.09, +0.14]. The $R^2$ of raw persistence on the permutation-null mean is 0.66. What predicts breadth is a static property of the concept's home-topic partner mix.

  \textbf{Degree-preserving configuration null.} Replacing raw ego density and persistence by curveball configuration $z$-scores raises OPEN$_{\text{home}}$ from +0.092 to +0.115.

  \textbf{Reliability.} Split-half reliability of NOVCHURN$_{\text{raw}}$ is 0.48. The temporal-excess variants (V2) have split-half Spearman--Brown reliability of approximately 0.01--0.05, and the planted-churn check fails. The disattenuated pooled NOVCHURN PSP is 0.178 [0.141, 0.214] (approximate, CI not independently re-derived).

  Because the V2 temporal-excess measure is unreliable, Experiment 16 cannot adjudicate temporal churn at typical sample sizes ($\sim$10 home papers/year). The association that survives behaves like a static dispersion property. Temporal turnover is untested rather than refuted.

  \textbf{Partner decomposition.} The home-only signal is carried by partners from new Leiden communities  arriving through mixed-field papers: contrast $C_2$ = +0.102 [+0.069, +0.133] (Holm $p$ = 0.0025), domain Shapley $\phi$ = +0.132 on the cohort (method = +0.012). Controlling for the share of early bridging papers halves NOVCHURN from 0.118 to 0.056.


  \subsection{Exploratory AI-domain stage}

  An exploratory retrospective atlas of 37 AI and computer science concepts was constructed from the large panel, examining how concepts such as deep learning, reinforcement learning and generative adversarial networks evolved through the co-occurrence network before their cross-field diffusion. This atlas is outcome-selected and retrospective; it provides qualitative context but no hypothesis-testing power.


  \subsection{Representative case studies}

  Seven matched case-study pairs were drawn from Experiment 12  (Table~\ref{tab:cases}). These pairs are illustration only; all are descriptive with no $p$-value.

  \begin{table}[ht]
  \centering
  \caption{Representative matched case-study pairs from Experiment 12, contrasting high-breadth and low-breadth concepts matched on early volume. All pairs are illustration; no inferential claim is made.}
  \label{tab:cases}
  \small
  \begin{tabular}{lll}
  \toprule
  High-breadth concept & Low-breadth concept & Group \\
  \midrule
  Graphics processing unit & Vertical-axis wind turbine & Eng \\
  Shotgun proteomics & Image-guided radiation therapy & BGM \\
  Nanocarriers & Nanosheet & CS \\
  Soft power & Autonomous learning & SOC \\
  Scopus & Oxygen reduction reaction & CS \\
  Sclerostin & IgG4-related disease & BGM \\
  User-generated content & Mindfulness-based cognitive therapy & SOC \\
  \bottomrule
  \end{tabular}
  \end{table}

  [FIGURE:fig_case_study]


  \subsection{Dead ends and negative results}
  \label{sec:dead_ends}

  Table~\ref{tab:deadends} lists the principal hypotheses and candidate signals that were tested and did not survive (across five iterations and 21 artifacts).

  \begin{table}[ht]
  \centering
  \caption{Principal dead ends and negative results across five research iterations.}
  \label{tab:deadends}
  \small
  \begin{tabular}{p{4.5cm}p{3cm}p{5cm}}
  \toprule
  Hypothesis / candidate & Decisive test & Result \\
  \midrule
  Naturalisation gap ($A^*_h$) & Exp.\ 1 & Fails every clause ($-$0.006) \\
  $D_{\text{ratio}}$, $F_{\text{res}}$ & Exp.\ 3 & No candidate survives \\
  Gateway landing on $O_{2r}$ & Exp.\ 4, 5 & $\Delta$AUC $-$0.00001 held-out \\
  H3 gateway-weighted landing & Exp.\ 5 & Pooled CI includes 0 [$-$0.006, 0.065] \\
  Ordering (central-first) & Exp.\ 6, Eval.\ 2 & MIXED: 32.6\% of broad concepts; negative lead-lag; pre-trend \\
  Two discrete trajectory classes & Exp.\ 6, 12 & HMM-vs-DTW ARI 0.094/0.222 \\
  Abandonment penalty ($d_{\text{lost}}$) & Exp.\ 7 & Specification-dependent: A1 $-$0.007, R4 +0.064, min-cp $-$0.030 \\
  Volume-matched retained-frontier contrast & Exp.\ 7 & Null: $-$0.028 [$-$0.105, +0.046] held-out \\
  $O_5$ external recognition & Exp.\ 8, Eval.\ 2 & No indicator beats B5 + onset year \\
  Rescue and relay models & Exp.\ 6 & Not supported \\
  Within-concept closure & Exp.\ 11, 15C & Null on DEV; opposite-signed held-out ($-$0.079) \\
  $n_{\text{authors\_early}}$ for $O_3$ & Exp.\ 8, 10 & Non-replication on fresh cohort (+0.014) \\
  RETENTION\_RATIO at R2/R3 & Exp.\ 10 & Null on cohort ($-$0.043 [$-$0.116, 0.031]) \\
  Trait prediction ($P$-B1) & Exp.\ 15B & Fails: yearly OPEN$_{\text{home}}$ ICC 0.34--0.39 \\
  Frame~N Cheng reversal & Exp.\ 13 & Not confirmed ($-$0.064 [$-$0.159, 0.031]) \\
  Co-author candidate S & Exp.\ 8 & Computed; not confirmed for any outcome \\
  \bottomrule
  \end{tabular}
  \end{table}


  \section{Discussion}
  \label{sec:discussion}

  \subsection{What the openness index captures}

  The OPEN index captures the degree to which a concept's early neighbourhood acquires partners from diverse communities rather than reinforcing existing ones. The signal is not demonstrably temporal turnover but a static topical-dispersion property. A within-concept permutation null absorbs the year-to-year component, yet the association persists: concepts whose home-field co-occurrence partners span many communities tend to reach more fields later. This is consistent with \citet{March1991}'s exploration--exploitation distinction at the concept level. However, the within-concept closure test (Experiment 15C) is null on DEV and opposite-signed on held-out fields, indicating that openness operates as a between-concept trait rather than as a within-concept causal mechanism.

  The home-only signal (OPEN$_{\text{home}}$) is marginal. The stronger OPEN$_{\text{all}}$ signal is partly mechanically coupled: early off-home papers that enter the ego network are a subset of the papers that determine the outcome. OPEN$_{\text{sizematch}}$ controls for this coupling and remains significant.

  \subsection{Reconciling consistency and breadth}

  \citet{Cheng2023} found that ideational consistency predicts a concept becoming ``core.'' We replicate their result for volume (+53\%/SD) but show that, net of volume, the same property predicts \emph{narrower} cross-field reach. The reversal holds in all five field groups ($I^2 = 0$) and replicates on a fresh cohort. The features predictive of local consolidation and growth are distinct from, and partly opposed to, the features predictive of broad disciplinary spread.

  \subsection{The retained-frontier claim}

  The confirmed field-entry result ($d_0 = 0.322$ on the independent frame) extends the principle of relatedness from economic geography \citep{Hidalgo2007,Boschma2011} to concept adoption. The result is PARTIAL: the volume-matched contrast is null, and the effect is backbone-specific (it reverses under minimum-conditional-probability proximity). What survives is a PMI-backbone relative-odds effect that cannot be separated from volume. The $I^2$ of 0.92 indicates substantial cross-domain heterogeneity, with Life \& Environment showing the strongest signal and Mathematics \& Decision Sciences null.

  \subsection{Limitations}

  \textbf{Effect size.} The OPEN--breadth association is modest. OPEN$_{\text{home}}$ adds no forecasting gain over B5 (+0.002 [$-$0.003, +0.008]).

  \textbf{Measurement noise.} Split-half reliability of OPEN$_{\text{home}}$ is 0.49. The temporal-excess variants have split-half reliability below 0.05, so temporal versus static dispersion cannot be resolved at available sample sizes.

  \textbf{Vocabulary bias.} The legacy OpenAlex concept vocabulary is survivor-selected. Frame~N is small (636 concepts) with pre-unseal power of 0.47.

  \textbf{Coupling.} About half of the OPEN$_{\text{all}}$ signal is mechanical coupling between the ego-network construction (which uses off-home papers) and the breadth outcome. OPEN$_{\text{home}}$ is free of this coupling but marginal.

  \textbf{Domain heterogeneity.} Life \& Environment shows the weakest OPEN signal (PSP +0.042). The retained-field relatedness $I^2$ is 0.92.

  \textbf{Not causal.} Early ego-network openness could reflect a concept's intrinsic generality, the diversity of the research community around it, or the breadth of the problems it addresses.

  \textbf{Prior unsealing.} Held-out outcomes were previously unsealed by two earlier experiments in the same project, so the indicator-screen held-out results are robustness checks.


  \section{Conclusions}
  \label{sec:conclusions}

  We screened 53 early temporal network indicators for predicting the cross-disciplinary breadth of new scientific concepts, using 12{,}499 concepts from the OpenAlex corpus with held-out validation and a fresh cohort confirmation. Seven indicators are confirmed, composing into an openness index that captures topical non-redundancy in a concept's early co-occurrence neighbourhood. The signal is a static between-concept trait; temporal turnover could not be tested at available sample sizes. Early openness predicts breadth; early consolidation predicts volume but not breadth. Concepts spread next to fields related to those currently retaining them, but the pre-registered verdict is PARTIAL: persistence and volume are confounded, and the effect is backbone-specific.


  \section*{Declarations}

  \subsection*{Funding}
  Not applicable.

  \subsection*{Conflict of interest}
  The authors declare no conflict of interest.

  \subsection*{Availability of data and materials}
  The study uses the publicly available OpenAlex bulk snapshot (2026-09-23). Concept frames, indicator matrices and analysis scripts are available from the corresponding author upon request.

  \subsection*{Code availability}
  Analysis code is available from the corresponding author upon request.

  \subsection*{Authors' contributions}
  All authors contributed to the study design, analysis and manuscript preparation.

  \bibliographystyle{sn-mathphys-num}
  \bibliography{references}

  \end{document}
summary: >-
  We screen 53 early co-occurrence network indicators against a popularity baseline for predicting cross-disciplinary breadth
  of 12,499 scientific concepts from OpenAlex. Seven indicators survive held-out validation, composing into an openness index
  (OPEN). The Eval4 descriptive pool of OPEN_home over 6 non-selection bodies gives partial Spearman +0.069 [+0.038, +0.100],
  I-squared = 0, 6/6 positive; evidence state is lead. The association behaves like a static topical-dispersion property;
  temporal turnover is untested rather than refuted (V2 excess split-half reliability below 0.05). A within-concept closure
  test is null on DEV and opposite-signed on held-out fields. On the Exp7 independent frame (EXP5 minus EXP6), a conditional
  logit shows concepts spread to fields related to those retaining them (d0 = 0.322 [0.291, 0.355]); the pre-registered verdict
  is FRONTIER = PARTIAL: the volume-matched contrast is null and the coefficient reverses under minimum-conditional-probability
  proximity. Early contact diversity accounts for 73% of the breadth gap; frontier advance contributes near zero. No discrete
  trajectory typology passes the naming rule.
</paper_draft>

<available_figures>
--- Item 1 ---
id: fig_evidence_synthesis
figure_type: data
title: Evidence synthesis across bodies
caption: >-
  Partial Spearman correlation of OPEN$_{\text{home}}$ (home-neighbourhood openness over $t_0..t_0{+}2$) with rarefied cross-field
  breadth ($O_{2r}$, $m=50$) at ladder rung R2. R2 controls for the five-feature popularity baseline B5 plus onset year, contact
  reach, concept type, a generic-concept flag and concept level. Blue squares with whiskers show the estimate and 95\% concept-bootstrap
  CI (2{,}000 draws) for each of six non-selection bodies: four held-out home groups (Physical Sciences, Life \& Environment,
  Social Sciences, Math \& Decision; onsets 2003--09), the 2010--14 onset cohort and the 2015--17 onset cohort. $n$ is the  number of concepts analysed. The black diamond spans the DerSimonian--Laird pooled estimate over these six bodies, $+0.069$
  $[+0.038, +0.100]$, $I^2 = 0$, 6/6 positive. The dotted vertical line marks this pooled estimate and the dashed line marks
  zero. The grey row below the separator is the DEV selection body, on which the index was chosen ($+0.109$ $[+0.073, +0.144]$).
  It is not pooled, and it is $1.58\times$ the non-selection pool. Values at right are estimate [95\% CI]. The association
  is small and has the same sign in every body, but only the two cohort rows and the pool have CIs above zero individually.
  All non-selection bodies except the 2015--17 cohort had outcomes read in earlier analyses, so the pool is descriptive rather
  than confirmatory.
image_gen_detailed_description: >-
  Forest plot (horizontal). Eight rows. Y-axis labels top to bottom: 'Physical Sciences' (n=413), 'Life & Environment' (n=630),
  'Social Sciences' (n=689), 'Math & Decision' (n=101), 'Cohort 2010-14 DEV-home' (n=1368), 'Cohort 2010-14 Other' (n=814),
  'DL Pooled (6 non-sel.)' (diamond marker), then a gap line, then 'DEV (selection)' (n=4771, shown in lighter grey colour).
  X-axis: 'Partial Spearman (OPEN_home | B5)', range -0.05 to 0.25. Values: PHYS 0.093, CI [0.028, 0.154]; LIFEENV 0.042,
  CI [-0.019, 0.103]; SOC 0.074, CI [0.024, 0.124]; MATHDEC 0.133, CI [-0.027, 0.303]; COH_DEVHOME 0.074, CI [0.024, 0.124];
  COH_OTHER 0.071, CI [0.015, 0.128]; DL Pooled 0.069, CI [0.038, 0.100]; DEV 0.109, CI [0.080, 0.138]. Vertical dashed line
  at x=0. DL Pooled row uses diamond shape. DEV row uses lighter shade to indicate selection body. Clean sans-serif font,
  white background.
aspect_ratio: '21:9'
summary: >-
  The openness-breadth association replicates across all six non-selection bodies with no heterogeneity.
figure_path: figures/fig_evidence_synthesis_v0.pdf

--- Item 2 ---
id: fig_entry
figure_type: data
title: Retained-frontier entry across domains
caption: >-
  Retained-frontier coefficient $d_0$ (log-odds of entering a field per SD of relatedness to the off-home fields that currently
  retain the concept) from the conditional-logit entry model (rung R3, controlling for home relatedness, field size, entered
  density, own gateway centrality, RCA density $D_{\mathrm{rca}}$ and volume density $D_{\mathrm{vol}}$), by unit. Circles
  with bars show point estimates with 95\% concept-bootstrap confidence intervals. The light-blue row is the development (DEV)
  set used for selection. Dark-blue rows are the held-out domain groups and the 2010--14 onset cohort. The black diamond is
  the DerSimonian--Laird random-effects estimate pooled over the four held-out groups, and its width spans its 95\% CI. The
  right column prints each estimate and interval; $n$ is the number of concepts in each unit. The dashed line marks $d_0 =
  0$. $d_0$ is positive with a CI excluding zero in all three evaluable held-out groups (Physical Sciences 0.148, Life \&
  Env.\ 0.401, Social Sciences 0.297) and in the cohort (0.321). Math \& Decision ($n = 165$, excluded as underpowered before
  the freeze) is null (0.065 [$-$0.110, 0.234]). The pooled estimate is 0.243 [0.118, 0.368] with high heterogeneity ($I^2
  = 0.92$). The frozen verdict is nonetheless PARTIAL: the pre-registered volume-matched contrast is null, and the effect
  is specific to the PMI backbone.
image_gen_detailed_description: >-
  Forest plot (horizontal). Seven rows. Y-axis labels (top to bottom): 'Development set' (n=274 concepts), 'Physical Sciences'
  (n=742), 'Life & Env.' (n=1113), 'Social Sciences' (n=1352), 'Math & Decision' (n=165), '2010-14 Cohort' (n=4356), 'DL Pooled
  (4 HO groups)'. X-axis: 'Retained-frontier coefficient (d0)', range -0.2 to 0.6. Values: Dev point=0.228, CI=[0.164, 0.291];
  Physical Sciences point=0.148, CI=[0.078, 0.219]; Life & Env. point=0.401, CI=[0.342, 0.460]; Social Sciences point=0.297,
  CI=[0.246, 0.348]; Math & Decision point=0.065, CI=[-0.109, 0.239]; Cohort point=0.321, CI=[0.292, 0.347]; DL Pooled point=0.243,
  CI=[0.118, 0.368]. Vertical dashed line at x=0. DL Pooled row uses a diamond marker. Dev row uses lighter shade to indicate
  selection data. All other rows use filled circles with horizontal CI bars. Clean sans-serif font, white background.
aspect_ratio: '21:9'
summary: >-
  Retained-frontier coefficient positive in 3 of 3 evaluable held-out groups, MATHDEC null. Verdict PARTIAL.
figure_path: figures/fig_entry_v0.pdf

--- Item 3 ---
id: fig_case_study
figure_type: data
title: Matched case-study pair
caption: >-
  Illustrative matched case-study pair from Experiment 12 (case pair 1 of 7): graphics processing unit (GPU; onset $t_0=2008$,
  high early-neighbourhood openness OPEN) versus vertical-axis wind turbine (VAWT; $t_0=2009$, low OPEN). Both have an Engineering
  home field and are matched on early volume and growth. (a) Number of off-home venue fields each concept has ever entered
  (solid line, filled markers) and currently retains (dashed line, open markers) in each year from $t_0$ to $t_0+8$; GPU is
  shown in black and VAWT in grey on a shared axis. By $t_0+2$ GPU had entered 7 off-home fields and VAWT 2; by $t_0+8$ they
  had entered 11 and 6 and retained 8 and 4. (b, c) Topic co-occurrence ego networks over the first three years ($t_0$ to
  $t_0+2$, all papers). The nodes are the concept's positive-PMI neighbour topics (the concept itself is not drawn), the edges
  are links between those topics in the 2010--14 topic backbone, node area scales with the number of the concept's papers
  carrying the topic, and colour gives the topic's Leiden community, named by the plurality OpenAlex field of its topics (plus
  the runner-up field when it has at least 0.6 times as many). GPU's neighbourhood has 34 topics in 8 communities (density
  0.30), led by Engineering \& Physics, Computer Science and Medicine communities. VAWT's has 12 topics in a single Engineering
  community (density 0.70). The pair illustrates the openness--breadth association and is not evidence for it (case\_pairs.json,
  pair 1).
image_gen_detailed_description: >-
  Two-panel figure (side by side, landscape). Left panel titled 'GPU (high breadth)': A timeline from t0 to t0+8 showing cumulative
  field count rising from 1 to approximately 12 fields, with coloured dots marking entry of each new field. Below the timeline,
  a small network diagram showing a central node 'GPU' connected to about 15 partner nodes in 4 distinct colour-coded clusters
  (blue=CS, green=Engineering, red=Medicine, orange=Materials). Right panel titled 'Vertical-axis wind turbine (low breadth)':
  Same timeline format but field count rises from 1 to approximately 3. Below, a smaller network diagram with central node
  connected to about 10 partner nodes mostly in 2 clusters (green=Engineering, yellow=Energy), with denser internal connections.
  Both panels share same y-axis scale. Caption at bottom: 'Illustration only (case_pairs.json pair 1)'. Clean sans-serif labels,
  white background, muted colours.
aspect_ratio: '21:9'
summary: >-
  Illustrative matched case pair showing contrasting ego-network structures between a high-breadth and a low-breadth concept.
figure_path: figures/fig_case_study_v0.pdf
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
really run. Its limits: the paper's single finding stays the one <paper_draft> argues, and a figure
fix re-orders or re-places the figures in <available_figures>, every one still included — a Figure 1
that shows a side result is fixed by moving the flagship figure there, never by drawing a new one. Recompile when it
is done.
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
````

### [2] SKILL-INPUT — aii-paper-to-latex · 2026-09-29 23:07:09 UTC

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

### [3] SKILL-INPUT — aii-paper-writing · 2026-09-29 23:07:09 UTC

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

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-09-29 23:07:09 UTC

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

### [5] SYSTEM-USER prompt · 2026-09-29 23:31:49 UTC

```
This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.

Summary:
1. Primary Request and Intent:
   The user's task is to typeset a research paper draft as LaTeX with BibTeX, insert pre-generated figures, and compile to PDF. The paper is about "Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts." The task follows a detailed TODO list with 8 items: load skills and fetch bibliography, create paper.tex, verify figures, run revision pass, terminology sweep, visual review of PDF pages, final read, and output a JSON result file. The workspace is `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_assemble_paper/paper/workspace`. All output files must be inside this workspace.

2. Key Technical Concepts:
   - LaTeX typesetting with article document class (11pt, letterpaper, 1in margins)
   - BibTeX bibliography management via `plainnat` style
   - Semantic Scholar bibliography fetching via `aii_semscholar_bib__fetch` script
   - Three skills: aii-paper-to-latex, aii-paper-writing, aii-semscholar-bib
   - REVISION_CHECKLIST.md at `/ai-inventor/.claude/skills/aii-paper-writing/REVISION_CHECKLIST.md`
   - Figure placement rules: [!htbp], width=\linewidth,height=0.85\textheight,keepaspectratio
   - URL breaking for long GitHub URLs: `\usepackage[hyphens]{url}` + `\UrlBreaks`
   - bibtex binary location: `/usr/bin/bibtex.original` (not `bibtex`)
   - Output JSON schema requires: title, summary, findings_summary, out_expected_files (paper_tex_path, paper_pdf_path, references_bib_path, figure_paths)
   - Must create `.aii/manifest.yaml` and `README.md` per disposable_outputs instructions

3. Files and Code Sections:
   - `paper.tex` (main LaTeX source, ~425 lines)
     - Document class: `\documentclass[11pt,letterpaper]{article}`
     - Key packages: graphicx, geometry, amsmath, booktabs, natbib, url (with hyphens), hyperref
     - URL break fix: `\makeatletter \g@addto@macro{\UrlBreaks}{\UrlOrds} \makeatother`
     - Sections: Introduction, Methods, Results (with RQ1, RQ2 subsections, Confound analysis, Case studies, Dead ends), Discussion (with Limitations subsection), Conclusions, Declarations
     - 3 figures: fig_evidence_synthesis_v0.pdf, fig_entry_v0.pdf, fig_case_study_v0.pdf
     - 6 tables: panel, screen, ladder, entry, cases, deadends
     - Bibliography: `\bibliographystyle{plainnat} \bibliography{references}`
   
   - `references.bib` (bibliography, 258 lines)
     - Contains 25 entries total (some unused: Liu2021, Fast2016, Clausen2012)
     - Active citation keys used in paper: Fortunato2018, Hofstra2019, Rotolo2015, OBrien2018, Domenico2016, Renoust2017, Cherifi2019, Burt2004, Centola2010, Ugander2012, Cheng2023, Weng2013, Salatino2017, Chavalarias2013, Gao2018, Sattar2023, Callon1991, Hidalgo2007, Neffke2011, Fitzgerald2021, Dersimonian1986, Higgins2002, March1991

   - `references.json` (fetch record, written by semscholar script)
   
   - `figures/fig_evidence_synthesis_v0.pdf` - Forest plot: OPEN_home partial Spearman across 6 non-selection bodies. Shows n=385 (Phys), n=552 (Life&Env), n=546 (Soc), n=86 (Math), n=1993 (Cohort 2010-14), n=573 (Cohort 2015-17), pooled +0.069 [+0.038, +0.100], DEV n=3003
   
   - `figures/fig_entry_v0.pdf` - Forest plot: retained-frontier coefficient d0 across domain groups. DEV 0.246, Phys 0.148, Life&Env 0.401, Soc 0.297, Math 0.065, Cohort 0.321, pooled 0.243 [0.118, 0.368]
   
   - `figures/fig_case_study_v0.pdf` - Three-panel: (a) GPU vs VAWT field entry timeline, (b) GPU ego network (34 topics, 8 communities, density 0.30), (c) VAWT ego network (12 topics, 1 community, density 0.70)

   - `paper.pdf` - Compiled PDF (17 pages, ~379KB)

4. Errors and fixes:
   - **Semantic Scholar rate limiting (429)**: Many title-based lookups failed due to S2 rate limits. Fixed by switching to DOI-based batch lookups which are faster and more reliable.
   - **Wrong paper matches**: Initial title searches matched wrong papers (e.g., "Augur" matched Fast2016 instead of Salatino2017; "hot streaks" Liu2021 instead of Cheng2023). Fixed by using exact DOIs found via WebSearch.
   - **Boschma2011 wrong match**: DOI 10.1093/icc/dtr051 matched Clausen2012 (wrong paper). Fixed by finding correct DOI (10.1111/j.1944-8287.2011.01121.x → Neffke2011).
   - **Leitch2019 not found**: After multiple search attempts, paper could not be located. Per skill rules, citation removed from paper.
   - **bibtex command not found**: `bibtex` binary doesn't exist but `bibtex.original` does at `/usr/bin/bibtex.original`. Used that instead.
   - **Overfull hbox (41.8pt)**: Long GitHub URLs in footnotes caused overfull boxes exceeding 15pt limit. Fixed by adding `\usepackage[hyphens]{url}` before hyperref and `\g@addto@macro{\UrlBreaks}{\UrlOrds}`. All remaining overfull boxes now under 9pt.

5. Problem Solving:
   - Successfully fetched 23 of 24 bibliography entries through iterative DOI lookups and WebSearch fallback
   - Mapped all draft citation keys to actual BibTeX keys (e.g., Milli2018→OBrien2018, Boschma2011→Neffke2011)
   - Applied revision checklist: renamed section, simplified abstract, removed pipeline-internal references
   - Verified figure count (3), zero citation warnings, zero reference warnings

6. All user messages:
   - The initial user message was the full task prompt (pasted content) containing the paper draft, available figures, figure requirements, writing register rules, TODO list, and JSON output schema. Key constraints include:
     - "CRITICAL: Every file you create, write, or save MUST be inside this workspace directory"
     - "Do not ask follow up questions and do not ask the user anything. Execute all steps independently."
     - "No placeholders, stubs, or incomplete code — all code must be complete and functional."
     - "NEVER kill processes by name... ALWAYS use PID-based process management"
     - "references.bib and references.json are written ONLY by this script. Never write, paste or edit a BibTeX entry by hand"
     - Figure captions must be used exactly as provided in available_figures
     - All figures must be included, no exceptions
     - Output JSON must match the specified schema at `.terminal_claude_agent_struct_out.json`
     - Must create `.aii/manifest.yaml` and `README.md`

7. Pending Tasks:
   - Task 5 (Terminology sweep) - nearly complete, was in progress
   - Task 6 (Visual review) - Write Python script to convert PDF pages to PNG at 150 DPI, read ALL page images, check for layout issues
   - Task 7 (Final read and output JSON) - Check page count, read entire PDF, fix issues, recompile, then:
     - Write `.terminal_claude_agent_struct_out.json` with required schema
     - Create `README.md`
     - Create `.aii/manifest.yaml` (the `.aii/` directory already exists)

8. Current Work:
   I was in the middle of Task 5 (Terminology sweep). I had:
   - Checked that no domain_terms.json or domain_vocabulary files exist
   - Scanned the paper for recurring technical terms
   - Verified terminology is mostly consistent (OPEN 47 uses, breadth 44, co-occurrence 20)
   - Fixed "V2" bare code → removed label
   - Confirmed R0-R5 codes are defined notation, "retained frontier" vs "retained-frontier" usage is correct
   - The sweep is essentially complete - no more fixes needed
   
   The paper is compiled at 17 pages with 0 warnings. Next steps are Task 6 (visual review) and Task 7 (final read + output JSON + manifest + README).

9. Optional Next Step:
   Complete Task 5 (mark as done), then proceed to Task 6: "VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page."
   
   After visual review, proceed to Task 7 which includes writing the output JSON file at `.terminal_claude_agent_struct_out.json`, creating `README.md`, and creating `.aii/manifest.yaml`. The task says: "IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above."

If you need specific details from before compaction (like exact code snippets, error messages, or content you generated), read the full transcript at: /var/lib/aii-agent/claude/projects/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-assemble-paper-paper-workspace/daf76a4a-7038-41c3-b571-5cfed86791c6.jsonl
Continue the conversation from where it left off without asking the user any further questions. Resume directly — do not acknowledge the summary, do not recap what was happening, do not preface with "I'll continue" or similar. Pick up the last task as if the break never happened.
```

### [6] SYSTEM-USER prompt · 2026-09-29 23:35:10 UTC

```
<CRITICAL_ERROR>
The module-end file check FAILED (attempt 1/3).

PROBLEMS:
  - .aii/manifest.yaml: 'paper.pdf' matches nothing that needs a decision — remove it (text, code and files under the auto-keep floor are always kept)
  - .aii/manifest.yaml: 'figures/' matches nothing that needs a decision — remove it (text, code and files under the auto-keep floor are always kept)

FIX IT:
1. Add one entry per uncovered path to `.aii/manifest.yaml` (create it if missing).
   Every path is RELATIVE TO YOUR CWD and must resolve inside it. Globs and
   whole directories are fine — a whole `hf_cache/` is ONE entry.

   entries:
     - path: results/
       keep: six GPU-hours of sweep output, not reproducible in this run
     - path: hf_cache/
       delete: redownloadable
       source: "huggingface-cli download meta-llama/Llama-3-8B"
     - path: checkpoints/
       delete: regenerable
       source: "uv run train.py --epochs 3"

   `keep:` takes a one-line reason. `delete:` takes `redownloadable` or
   `regenerable` and a `source:` that brings the files back.
2. Make sure `README.md` reads like a GitHub repository README: what you did,
   the layout (a line per important file/dir), how to run it, and a
   "Restoring removed files" section with the command for EVERY delete entry.
3. Text and code files never need a decision, and neither does anything under
   the auto-keep floor. Only large binaries and cache directories do.
</CRITICAL_ERROR>
```
