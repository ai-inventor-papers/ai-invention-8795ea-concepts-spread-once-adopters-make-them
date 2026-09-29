# review_report — test_idea

> Phase: `invention_loop` · round 2 · `review_report`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `review_report` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-28 20:55:37 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-28 20:55:43 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An adversarial paper reviewer (Step 3.5: REVIEW_REPORT in the invention loop)

You received a paper draft written by a DIFFERENT model. Review it with fresh eyes.
Provide constructive but rigorous critique that will improve the next iteration.

Specific critiques → better paper. Vague praise → no improvement.
</your_role>
</ai_inventor_context>

ROLE: You are a very experienced and critical researcher auditing a colleague's research
record. Your expertise spans the domain of the work under review, and you have reviewed for
top-tier venues in it — but that is not what you are doing here.

WHAT YOU ARE REVIEWING: the run's INTERNAL RESEARCH REPORT, not a paper. It is a lab
notebook written up: chronological, one section per iteration, complete. Its job is to
preserve everything the run did and concluded, including the parts that failed. A separate
step writes the publishable paper at the end, out of this report, and it can draw only on
what it finds here.

TASK: Audit the record. Is every result that exists written down, in full? Can each number
be traced to the artifact that produced it? Does the report say what was learned, what was
ruled out, and why the run moved where it did?

FIGURES: The report contains figure specifications with captions and descriptions but the
actual images have not been generated yet. Assume each figure shows exactly what its
caption describes — do not penalize for missing images.

ARTIFACTS: The report references code artifacts via [ARTIFACT:id] markers. The correct
URLs to the artifact folders will be added later — do not penalize for missing links.

GOAL: Your review feeds back to the report's author and steers the next iteration. Spend it
on what would most improve the RECORD: a missing experiment write-up, a table left out, a
number nobody can trace, reasoning that was never written down, a dead end that vanished.
Do not spend it on presentation, framing or novelty — those belong to a document that has
not been written yet.

STRENGTHS AND WEAKNESSES: Provide a thorough assessment touching on each of these:
(a) Completeness: Is every experiment the run executed written up, with its tables in
    full? A result that exists in an artifact workspace and not in the report is the
    defect this review exists to catch. Are dead ends recorded as dead ends rather than
    quietly dropped?
(b) Traceability: Can each number, table and claim be followed back to the artifact that
    produced it — an [ARTIFACT:id] marker, a named output file, a workspace path? Could a
    reader re-run what is described and get the same thing?
(c) What was learned: Does the report say what the evidence now supports, what it rules
    out, and why the run changed course when it did? Is the reasoning behind each
    iteration recorded, or only its outcome?
(d) Honesty: Are the limits of the evidence stated plainly, without selling? Does any claim
    outrun what actually ran?

SUPPLEMENTARY SCORES: Rate each on a 1-4 scale.
Soundness (1-4) — soundness of the technical claims and of the experimental methodology as the
report describes it, and whether every claim is supported by evidence that ran:
  4: excellent  3: good  2: fair  1: poor
Presentation (1-4) — quality of writing, clarity, and contextualization relative to prior work:
  4: excellent  3: good  2: fair  1: poor
Contribution (1-4) — how much of the run this report actually preserves: every experiment and table
recorded, every step's reasoning captured, every dead end kept with its evidence:
  4: excellent  3: good  2: fair  1: poor

OVERALL SCORE (1-10):
  10 — Award quality: Technically flawless with groundbreaking impact on one or more
       areas of the field, with exceptionally strong evaluation, reproducibility,
       and resources, and no unaddressed concerns.
   9 — Very Strong Accept: Technically flawless with groundbreaking impact on at least
       one area and excellent impact on multiple areas, with flawless evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   8 — Strong Accept: Technically strong with novel ideas, excellent impact on at least
       one area or high-to-excellent impact on multiple areas, with excellent evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   7 — Accept: Technically solid, with high impact on at least one sub-area or
       moderate-to-high impact on more than one area, with good-to-excellent evaluation,
       resources, reproducibility, and no unaddressed concerns.
   6 — Weak Accept: Technically solid, moderate-to-high impact, with no major concerns
       with respect to evaluation, resources, reproducibility.
   5 — Borderline Accept: Technically solid where reasons to accept outweigh reasons to
       reject, e.g., limited evaluation. Use sparingly.
   4 — Borderline Reject: Technically solid where reasons to reject, e.g., limited
       evaluation, outweigh reasons to accept. Use sparingly.
   3 — Reject: For instance, technical flaws, weak evaluation, inadequate reproducibility.
   2 — Strong Reject: For instance, major technical flaws, poor evaluation, limited
       impact, poor reproducibility.
   1 — Very Strong Reject: For instance, trivial results or unaddressed concerns.

CONFIDENCE (1-5):
  5: Absolutely certain. Very familiar with related work, checked details carefully.
  4: Confident but not absolutely certain. Unlikely you misunderstood something.
  3: Fairly confident. Possible you missed some related work or details.
  2: Willing to defend your assessment, but quite likely missed central aspects.
  1: Educated guess. Not in your area or difficult to evaluate.

For each dimension, provide a list of specific improvements:
- WHAT needs to change
- HOW to change it (concrete enough for the author to act on immediately)
- EXPECTED SCORE IMPACT: how much would fixing this raise the overall score?

REVIEW PRINCIPLES:
- Be specific and actionable — vague critique is useless
- Ground your review in evidence — search for existing work, accepted papers, known results
- Rank critiques by score impact — address the biggest score blockers first
- Distinguish major issues (the record is incomplete or untraceable) from minor issues (polish)
- Acknowledge genuine strengths — don't be negative for its own sake
- Compare against the bar set by accepted papers at top-tier venues
- Check COMPLETENESS artifact by artifact. Walk the supplementary materials and, for each executed artifact, find where the report reports it. An artifact whose results are absent, or summarised without its table, is a major issue: the paper step writes from this report alone and cannot publish what is not here
- Check every TABLE is present with its actual numbers. Open the output files and compare. Prose like "performance improved" standing in for a table that exists on disk is a major issue
- Check TRACEABILITY: each number, table and claim carries an [ARTIFACT:id] marker or names the output file it came from. An untraceable number is a major issue even when it is correct
- Check the REASONING is recorded, not just the outcomes: why each strategy, why these artifacts, what the previous review objected to, what the hypothesis update concluded and why it moved. A section that reports results with no account of why they were sought is incomplete
- Check DEAD ENDS are kept and labelled, with the evidence that killed them. A direction the run abandoned and the report does not mention is a major issue: it makes the run look luckier than it was, and the paper step will never know the alternative was tried
- Check the CHRONOLOGY holds: one section per iteration, in order, and the earlier sections unchanged except where a correction is marked in place. An earlier section silently rewritten destroys the record and is a major issue
- Check that every headline number came out of an artifact that ACTUALLY RAN, and RECOMPUTE it yourself from that artifact's own tables or result files — do not accept the report's figure on its word. A mismatch between what you recompute and what the report states is a finding in its own right. Where an artifact does not let you recompute a number, say so and score that claim unverified rather than accepted. A projected, expected, illustrative or placeholder number presented as a result is the most serious defect this report can have — set results_reported false and blocking true
- When the report claims a POSITIVE, non-obvious result, name the nearest published result that already answers something close to it and state what this iteration adds beyond that neighbour. This checks whether the FINDING has earned its claim, not how the paper will be framed against the literature: a positive result gets no credit for novelty in this record until that comparison is made, and its absence is a critique under 'novelty'
- Check for an iteration that added METRICS rather than SAMPLES to an already underpowered panel. When a power analysis or the effect sizes on record show the artifact panel cannot detect the effect being chased, more candidate metrics or readouts over the same panel do not fix that — flag it as a major issue and say the budget belonged on more graded samples or checkpoints instead
- Check COVERAGE against the user's ORIGINAL request, not against the report's own framing. Name the part of the request the run has not addressed yet
- Check that claims are PROPORTIONATE to the evidence. A small, expected-direction effect written up as the answer is the failure mode to name explicitly
- Do NOT review this as a paper. Section order, narrative arc, abstract framing, figure count and writing polish are the later paper step's concerns, and a critique about them spends the run's iteration budget on the wrong document. The nearest-neighbour check above is different: it asks whether the record has earned its positive claim, not how the paper will be sold against the literature. Bookkeeping — run ids, timestamps, spend, review scores, file hashes — BELONGS in this report; never ask for its removal

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report/`:
GOOD: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report/file.py`, `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report/results/out.json`
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

<role>
You are a very experienced and critical conference reviewer specialized in the domain of the work under review.
You have reviewed for top-tier venues in the relevant field. Your reviews are known for
being thorough, fair, and grounded in the actual state of the field.
</role>

<report>
# Do temporal network signals predict how scientific concepts spread across disciplines?

This report is the chronological record of a study that tests whether temporal changes in the structure of scientific knowledge networks can anticipate the emergence and cross disciplinary integration of new scientific concepts. The study compares three families of candidate network indicators against a baseline of simple popularity and reach measures, evaluated on a panel of 46 to 48 concepts across four home field groups (Biochemistry/Genetics, Computer Science, Engineering, Medicine) with onset years 2003 to 2009.

The primary outcome is rarefied field breadth (O2r), the expected number of distinct disciplines among a fixed size random draw of a concept's papers in years t0+6 to t0+8. This outcome separates size adjusted breadth from sheer volume. Secondary outcomes include sustained uptake and transience. Evaluation uses leave one group out (LOGO) ridge regression with 2,000 stratified concept level bootstraps, so that an indicator's incremental value (delta rho or delta AUC) is always measured on concepts from a home field the model has never seen.

Three candidate indicators are tested, each representing a different theory of how concepts spread:

- **Candidate L** (naturalisation gap, A\*_h): a background adjusted disciplinary self citation index on the concept's lineage network, drawn from the epidemiological negative control design [ARTIFACT:art_xp8BGBJZsxeI].
- **Candidate D** (structural diversity of cooccurrence ties): the number of distinct Leiden communities a concept's new neighbours reach on a corpus wide topic cooccurrence backbone [ARTIFACT:art_yrradSC27HtQ].
- **Candidate G** (gateway landing): the eigenvector centrality of the adopting fields on a topic coassignment backbone, weighted by early nonhome share [ARTIFACT:art_33_KKk_G8Gw5].



# Iteration 1

## 1. Strategy

The hypothesis predicts that a new concept spreads durably across disciplines when the fields that adopt it begin citing the concept's literature the way they cite their own literature, rather than reaching back to the concept's home field. The predicted signal is the "naturalisation gap" A\*_h: the log odds ratio of the concept's citing layer by cited layer mixing table (nonhome versus home), minus the same log odds ratio computed on the same citing papers' nonconcept references (the background term). A negative value means adopters still import the concept across field lines more than their general citing habits predict; a value near or above zero means the concept's lineage follows the adopters' own field boundaries.

Two alternative hypotheses compete. The first is that the structural diversity of cooccurrence ties matters: concepts that acquire neighbours in many different Leiden communities on a corpus wide backbone will spread more broadly, following complex contagion theory [1, 2]. The second is that what matters is where a concept lands: concepts adopted early by high centrality "gateway" fields on a topic relatedness backbone will spread, following the principle of relatedness from economic complexity [3].

All three candidates are tested against a shared five feature baseline: log early volume, publication growth, nonhome share, Shannon entropy and field reach, all computed over the first five years from onset. The shared evaluation protocol defines onset, outcomes and panel membership across all three experiments. The preregistered decision rule requires delta rho >= 0.10 with 90% bootstrap CI excluding zero, the same sign in at least three of four home field groups, split-half reliability >= 0.60 and absolute Spearman with log volume and growth <= 0.60.

## 2. Data infrastructure and deviations

The shared OpenAlex credit pool (10,000 daily credits, split across five artifacts) was exhausted partway through iteration 1. This forced a data deviation that affects all three experiments:

- **Yearly counts** (for onset, sustained uptake, transience, volume and growth) come from OpenAlex group by calls and follow the shared evaluation protocol exactly for all 78 panel concepts.
- **Field labels, concept papers and citation lineage** come from Semantic Scholar, a free source. Semantic Scholar's field assignments use a 23-field text classifier taxonomy (s2-fos), which is concept independent (it reads titles and abstracts, not references). The 23-field Semantic Scholar taxonomy was mapped to the 26-field OpenAlex scheme for the experiments that require venue labels.
- **Background references** come from free OpenAlex singleton GET calls (verified zero credit via response headers).
- **Agreement between sources** on the 11 concepts where both sources have full data: Spearman correlation of rarefied breadth between outcomes labelled by Semantic Scholar and outcomes labelled by OpenAlex is 0.87.

The panel comprises 78 concepts with onset years 2003 to 2014, of which 46 to 48 fall in the dev window (onset 2003 to 2009, home field in one of the four groups). The exact number varies by experiment because each has slightly different eligibility filters.

## 3. Experiment 1: Does the naturalisation gap predict cross field spread? [ARTIFACT:art_xp8BGBJZsxeI]

### 3.1 Construction

For each concept, the analysis downloads up to 25,000 phrase matched papers and their citation lists. A concept lineage link is a citation from a concept paper to an earlier concept paper within three years. Links between papers that share an author are removed from the main estimator (self lineage share ranged from 5% to 39% across concepts). The naturalisation gap A\*_h is the Mantel-Haenszel pooled log odds ratio (a stratum weighted average across yearly mixing tables) of the nonhome/home mixing table for concept citations, minus the same log odds ratio for the same citing papers' nonconcept references (the background term). The background term absorbs the adopters' general disciplinary homophily without modelling it.

Field labels for the lineage analysis come from Semantic Scholar's fractional field of study classifier. Home field is defined as the field(s) holding at least 40% of a concept's first 30 grounded papers. Concepts whose Semantic Scholar home field falls outside the four dev groups (Computer Science, Engineering, Biology, Medicine) are dropped ("sealed"), leaving 48 dev concepts (Biochemistry/Genetics 13, Computer Science 21, Engineering 3, Medicine 11).

### 3.2 Measurement result: background homophily dominates lineage

The first finding is the background homophily measurement result, which was predicted by the 8-concept probe. Among all 48 dev concepts, 100% have a positive background log odds ratio: every field's citing papers preferentially cite their own field's literature above chance. The coefficient of determination (R squared) of the raw concept lineage log odds ratio on the background log odds ratio is 0.66 (90% CI [0.39, 0.83]), with Spearman correlation 0.70.

We define "lineage autonomy" as the degree to which a concept's citation chains stay within adopters' own disciplines rather than reaching back to the home field. Two thirds of the between concept variance in this raw lineage autonomy is explained by which fields adopt the concept and how insular those fields are in general. Uniform null lineage indicators (including the study's own earlier A\* and naive R_away) are therefore largely measures of field composition, not concept specific rooting. This is the background homophily measurement result.

| Statistic | Value | 90% CI |
|---|---|---|
| R squared of raw lineage LOR on background LOR | 0.66 | [0.39, 0.83] |
| Spearman of raw lineage LOR with background LOR | 0.70 | - |
| Share of concepts with positive background LOR | 100% (48/48) | - |
| Share where background >= raw lineage LOR | 77% (37/48) | - |

[FIGURE:fig_m1_scatter]

### 3.3 Predictive screen: A\*_h does not survive

The naturalisation gap A\*_h was tested as a predictor of rarefied breadth (O2r, m = 30) in LOGO ridge regression. The five feature baseline alone reaches rho = 0.834 with rarefied breadth. Adding A\*_h produces delta rho = -0.006 (90% CI [-0.034, 0.017]). A\*_h fails the preregistered rule on all three testable clauses:

| Clause | Required | Observed | Pass? |
|---|---|---|---|
| Delta rho >= 0.10 and CI low > 0 | >= 0.10 | -0.006, CI [-0.034, 0.017] | No |
| Positive in >= 3 of 4 groups | >= 3 | 0 of 4 (Bio 0.00, CS -0.003, Eng insufficient, Med 0.00) | No |
| Split-half reliability (Spearman-Brown) | >= 0.60 | 0.58 | No |
| Abs Spearman with log volume and growth | <= 0.60 | 0.14 (volume), 0.18 (growth) | Yes |

The size independence clause passes: A\*_h is not a proxy for concept volume or growth. But the gap adds nothing to the baseline on holdout fields, and it is not measured reliably enough (split-half r_SB = 0.58, just below the bar).

### 3.4 Within field heterogeneity and reliability gradient

**[Correction, iteration 2.]** The values +0.45 and -0.18 reported in the original version of this subsection were the within group Spearman correlations of A\*_h with rarefied breadth (Medicine 0.446, Computer Science -0.184), not the group medians of A\*_h itself. The per group medians of A\*_h are negative in every group: Biochemistry/Genetics -0.256, Computer Science -0.303, Engineering -0.041, Medicine -0.182 [ARTIFACT:art_lwI2DuRtQRZX]. No group is "naturalised" on average; all four medians are borrowed. The finding that survives is that the direction of A\*_h's association with rarefied breadth flips across groups (positive in Medicine, negative in Computer Science and Biochemistry/Genetics), not that the level of A\*_h differs.

| Home group | N | Median A\*_h | IQR | Within group rho(A\*_h, O2r) |
|---|---|---|---|---|
| Biochemistry/Genetics | 13 | -0.256 | [-0.458, -0.132] | - |
| Computer Science | 21 | -0.303 | [-0.471, -0.064] | -0.184 |
| Engineering | 3 | -0.041 | [-0.103, -0.014] | - |
| Medicine | 11 | -0.182 | [-0.315, -0.095] | +0.446 |

The original claim that "A\*_h is partly a field composition indicator itself, despite the background adjustment" does not follow from these corrected numbers, which show all groups are borrowed but their association with breadth varies.

Reliability depends on sample size. Concepts with fewer than 60 nonhome children have split-half reliability below 0.40, while the 11 concepts with 60 or more nonhome children reach r_SB = 0.72. On those 11 concepts, the eligible subset delta rho is +0.118 (90% CI [0.00, 0.36]), but this is too underpowered to interpret.

| Nonhome children bin | N concepts | Split-half r | Spearman-Brown |
|---|---|---|---|
| 0-15 | 21 | 0.24 | 0.34 |
| 15-30 | 9 | 0.32 | 0.37 |
| 30-60 | 7 | 0.14 | 0.04 |
| 60+ | 11 | 0.57 | 0.72 |

### 3.5 Alternative lineage indicators

None of the 14 candidate and foil features scored as exploratory candidates beat the five feature baseline. The full candidate comparison table:

| Indicator | Delta rho | 90% CI | Groups + | r_SB | rho(vol) | rho(growth) |
|---|---|---|---|---|---|---|
| A\*_h (primary) | -0.006 | [-0.034, 0.017] | 0/4 | 0.58 | 0.14 | 0.18 |
| A\*_h (Mantel-Haenszel) | +0.016 | [-0.005, 0.042] | 2/4 | 0.76 | 0.07 | 0.08 |
| A\*_h (unadjusted) | +0.015 | [-0.002, 0.037] | 2/4 | 0.74 | 0.17 | 0.42 |
| A\*_h (crude, no bg) | +0.012 | [-0.016, 0.040] | 1/4 | 0.72 | 0.05 | 0.10 |
| Naturalised field count | +0.002 | [-0.030, 0.036] | 1/4 | 0.71 | 0.33 | 0.37 |
| Max field level rho\* | -0.013 | [-0.038, 0.009] | 0/4 | 0.74 | 0.37 | 0.22 |
| Background LOR | -0.004 | [-0.060, 0.039] | 2/4 | 0.91 | 0.05 | 0.04 |
| Raw lineage LOR | +0.000 | [-0.008, 0.009] | 0/4 | - | 0.16 | 0.02 |
| A\*_unif | -0.011 | [-0.052, 0.022] | 1/4 | - | 0.02 | 0.17 |
| A\*_imp | -0.003 | [-0.043, 0.029] | 1/4 | - | 0.05 | 0.20 |
| Relay share | -0.012 | [-0.051, 0.021] | 0/4 | - | 0.02 | 0.00 |
| Self lineage share | +0.028 | [-0.005, 0.065] | 1/4 | - | 0.18 | 0.37 |
| Coverage | +0.008 | [-0.003, 0.023] | 1/4 | - | 0.31 | 0.36 |
| R_away | -0.025 | [-0.060, 0.007] | 1/4 | - | 0.01 | 0.16 |

The Mantel-Haenszel pooled variant (A\*_h MH) comes closest, with delta rho +0.016 and two groups positive, but still does not pass the decision rule. The background log odds ratio itself, which measures adopters' general disciplinary insularity, has the highest reliability (r_SB = 0.91) but no predictive gain.

### 3.6 Secondary outcomes

For sustained uptake, adding A\*_h to the five feature baseline gives delta AUC = -0.026 (90% CI [-0.084, 0.028]): no gain. Transience is not evaluable because only 4 of 48 concepts are transient, and all four are in Medicine.

### 3.7 Field level prediction

At the field level (367 concept by field units, predicting field retention R_j), adding the field level rho\*_cj to the baseline gives delta AUC = +0.002 (90% CI [-0.011, 0.016]): no gain.

### 3.8 Variance decomposition (REML)

A crossed random effects model (concept and concept by field) fitted by REML on 190 cells gives estimated standard deviations tau_c = 0.29 (between concept) and tau_cj = 0.65 (concept by field). The concept by field variance is more than twice the between concept variance, confirming that naturalisation is field specific rather than a concept level trait. A PyMC NUTS sampler check agrees with REML to Spearman 0.9996.

### 3.9 Audit

An independent rederivation confirms delta rho, baseline rho, the size correlations, sustained uptake delta AUC and the background homophily result exactly. Field level delta AUC is rederived at 0.0020.

**[Correction, iteration 2.]** The original text stated: "A shuffled A\*_h placebo passes 0 of 200 times, confirming that the null result is not an artefact of the evaluation protocol." The placebo's meaning is narrower: it bounds the false positive rate of the decision rule. The positive control ladder shows that the protocol has low sensitivity: a feature with Spearman 0.83 with rarefied breadth gains only +0.068 over the baseline, below the 0.10 threshold, so a feature needs Spearman of approximately 0.95 to pass. The leaky positive control also fails the delta clause. Reliability of 0.58 was not independently rederived (noted in the artifact summary).



## 4. Experiment 3: Do diverse topic ties predict concept spread? [ARTIFACT:art_yrradSC27HtQ]

### 4.1 Construction

This experiment builds a full corpus topic cooccurrence backbone from the 2026-09-23 OpenAlex bulk data snapshot (476 million works). For each of three time slices (2000 to 2004, 2005 to 2009, 2010 to 2014), topic coassignment PMI is computed over all works. Leiden community detection (gamma = 3) produces 25, 26 and 23 communities across the three slices (the plan's rule of approximately 8 communities was not achievable; this deviation is documented).

For each concept, the analysis tracks which topics cooccur with it through title matched works (median 48% of API volume; Spearman 0.88 with API counts). The primary candidate D_ratio is the ratio of distinct Leiden communities reached by the concept's new cooccurrence neighbours to the total number of new neighbours. D_z, the literal plan primary, was superseded because it failed the size independence diagnostic (Spearman with log volume = -0.63).

The panel comprises 47 dev concepts (Biochemistry/Genetics 16, Computer Science 12, Medicine 10, Engineering 9).

### 4.2 Screen results

The five feature baseline alone reaches rho = 0.770 with rarefied breadth. Neither candidate survives the preregistered rule:

| Candidate | Delta rho | 90% CI | Groups + | r_SB | rho(vol) | rho(growth) | Survives? |
|---|---|---|---|---|---|---|---|
| D_ratio (primary D) | +0.006 | [-0.092, 0.135] | 3/4 | 0.83 | 0.11 | 0.02 | No |
| F_res (disciplinary) | -0.060 | [-0.158, 0.014] | 1/4 | 0.44 | 0.04 | 0.09 | No |
| D_z (plan literal, superseded) | +0.017 | [-0.101, 0.087] | 4/4 | 0.90 | -0.63 | 0.09 | No (size) |

D_ratio passes the reliability and size independence clauses. It is positive in 3 of 4 groups, but its delta rho of +0.006 is far from the 0.10 threshold. F_res (frequency residualised by the baseline) has low reliability (r_SB = 0.44) and is negative in 3 of 4 groups.

### 4.3 Portability: which indicators associate with rarefied breadth across all groups?

**[Correction, iteration 2.]** The original text described D_ratio, D_rare, participation and neighbourhood novelty as having within group Spearman correlations "in the range 0.45 to 0.63 across all four groups." Those were pooled values. The within group minima are lower: D_ratio 0.33 (Engineering), D_rare 0.47 (Engineering), participation 0.12 (Computer Science), neighbourhood novelty 0.27 (Computer Science). Also, the claim that raw cooccurrence growth indicators were "near zero or negative" in groups other than Computer Science requires correction: new_edge_rate is 0.35 in Medicine, not near zero.

The corrected statement: several cooccurrence indicators have pooled Spearman correlations with rarefied breadth of 0.45 to 0.63 and are positive in all four groups, with within group values ranging from 0.12 to 0.68. All are redundant under delta rho: none adds to the five feature baseline.

[FIGURE:fig_portability]

### 4.4 Exploratory partial association

**[Correction, iteration 2.]** The original text reported 5 of 12 partial associations and labelled D_ratio's signal "real." The full 12-indicator table is required, and the 95% CI of D_ratio includes zero ([-0.059, 0.688]). With 12 tests, D_ratio's permutation p = 0.037 (one sided, 1,000 permutations) does not survive any multiplicity correction. The D_ratio partial association is marginal, uncorrected, 1 of 12, and negative in Engineering (-0.067). "Real" is removed from the closing summary.

| Indicator | Partial rho | 90% CI | 95% CI |
|---|---|---|---|
| D_ratio | 0.335 | [0.019, 0.648] | [-0.059, 0.688] |
| D_rare | 0.311 | [-0.034, 0.653] | - |
| Participation | 0.322 | [-0.037, 0.640] | - |
| NOV_res | 0.281 | [-0.114, 0.581] | - |
| F_res | -0.267 | [-0.443, 0.249] | - |

*(The remaining 7 indicators from the 12-indicator file were not extracted in iteration 1 and are not available in the current workspace output; they are all nonsignificant.)*

### 4.5 Secondary outcomes

For sustained uptake, D_ratio gives delta AUC = -0.005 (90% CI [-0.060, 0.036]): no gain. Transience is not estimable because all transient concepts in this panel are in Medicine. Dissociation tests between breadth and uptake are inconclusive.

### 4.6 Audit

All headline numbers (delta rho, CI, per group deltas, portability rho values) are rederived exactly by an independent rederivation. A shuffled placebo of the full screen fails; a planted control with a known predictive synthetic feature passes.



## 5. Experiment 4: Where a concept lands early vs. how broadly it spreads [ARTIFACT:art_33_KKk_G8Gw5]

### 5.1 Construction

This experiment asks whether early adoption by high centrality "gateway" fields on a topic relatedness backbone predicts breadth. The backbone is a 26-field positive PMI topic coassignment graph from 1998 to 2002. Gateway centrality G is the share weighted eigenvector centrality of the venue fields adopting a concept in t0 to t0+2.

This experiment also produces the shared outcome tables: all 78 concept outcomes, 80 concept by field retention episodes, baseline features and single indicator scores.

The panel comprises 46 dev concepts (34 with an outcome window rarefied breadth score). The credit floor was hit after 286 credits, so t0+3 to t0+4 labels are missing (the baseline's label based features use t0 to t0+2 only), and outcome windows keep only the top-200 sources (29 of 34 concepts are truncated).

**[Addition, iteration 2: per experiment baseline rho.]** The five feature baseline's correlation with rarefied breadth differs sharply across experiments: baseline rho = 0.834 (Experiment 1, n = 48), 0.770 (Experiment 3, n = 47), 0.327 (Experiment 4, n = 34) [ARTIFACT:art_lwI2DuRtQRZX]. Experiment 4's much weaker baseline reflects three data limitations: outcome windows truncated to the top-200 sources for 29 of 34 concepts, label based features using only t0 to t0+2 (not t0 to t0+4), and a different outcome table (Experiment 4's venue field outcomes, not Experiment 1's Semantic Scholar s2-fos or Experiment 3's title matched snapshot venue fields). Per group baselines in Experiment 4 are: Computer Science 0.10 (n = 10), Engineering 0.86 (n = 7), Biochemistry/Genetics 0.65 (n = 9), Medicine 0.57 (n = 8).

**[Addition, iteration 2: cross experiment outcome agreement.]** The three experiments each computed their own rarefied breadth and home field labels. Cross experiment Spearman correlations of rarefied breadth are: Experiment 1 vs 3, 0.764 (n = 41); Experiment 1 vs 4, 0.790 (n = 30); Experiment 3 vs 4, 0.803 (n = 33). Eight of the 41 concepts shared by Experiments 1 and 3 are assigned a different home group, so the LOGO folds differ. The comparison table in Section 6.2 is therefore not directly like for like; each candidate was screened on its own experiment's outcome table.

### 5.2 Concept level screen

Gateway centrality was tested against the five feature baseline on rarefied breadth (m = 30):

| Candidate | Delta rho | 90% CI | Groups + | r_SB | rho(vol) | rho(growth) | Survives? |
|---|---|---|---|---|---|---|---|
| G (eigenvector gateway) | +0.033 | [-0.095, 0.168] | 2/4 | 0.92 | 0.11 | 0.13 | No |

Gateway centrality does not survive the preregistered rule: delta rho is +0.033 (below 0.10), positive in only 2 of 4 groups (Engineering +0.071, Biochemistry +0.067; Computer Science -0.230, Medicine -0.048), and the CI includes zero. However, reliability is high (r_SB = 0.92) and the size check passes.

### 5.3 Secondary results: volume residualised breadth and uptake

When rarefied breadth is residualised on log volume, the story changes. G's delta rho rises to +0.15 (90% CI [0.000, 0.321]), positive in 4 of 4 groups. This is an exploratory finding: gateway centrality adds information about breadth conditional on size, but not on raw breadth.

**[Correction, iteration 2.]** The original text stated that G's sustained uptake delta AUC of +0.072 was "the strongest secondary signal in the iteration." This is false. The secondary variant screen reports stronger sustained uptake gains for several variants: G_deg +0.149 (95% CI [0.053, 0.266], 3/4 groups), G_phimin +0.154 ([0.058, 0.272]), REL_home +0.121 ([0.033, 0.229]), G_all +0.112. All exceed G's +0.072, whose 95% CI lower bound is exactly 0.000 (95% CI [-0.011, 0.187]). **All eight of these sustained uptake gains are label coverage artefacts:** adding label_coverage_early to the baseline reduces G's sustained uptake delta from +0.072 to +0.002 [ARTIFACT:art_lwI2DuRtQRZX]. The same screen reports variants that significantly harm rarefied breadth: G_all gives delta rho -0.240 (95% CI [-0.419, -0.087]) and DOM_Physical gives -0.110 ([-0.193, -0.037]). These are negative results, recorded below in Section 7.

### 5.4 Field level prediction: gateway centrality of the adopting field

At the field level (80 concept by field rows), the adopting field's own gateway centrality adds delta AUC = +0.10 (95% CI [0.03, 0.17]) for retention. This survives a field size control: with log field size in the baseline, the gateway centrality delta AUC is +0.10 (95% CI [0.04, 0.16]). In Computer Science, however, the gateway signal is absent (delta AUC negative), making this a three group result.

**[Addition, iteration 2: refit bootstrap CI.]** The iteration-1 CIs above are from the fixed prediction bootstrap (2,000 draws resampling fixed out of fold predictions). The wider concept clustered refit bootstrap gives: gateway over the simple three feature baseline, delta AUC +0.103, refit 95% CI [0.010, 0.212]; gateway over the full covariate set (the five feature baseline + log field size + relatedness to home + relatedness density), delta AUC +0.037, refit 95% CI [-0.018, 0.130] [ARTIFACT:art_lwI2DuRtQRZX]. The iteration-1 field level lead therefore holds against the simple baseline but does not reach significance over the full covariate set with the refit bootstrap.

| Field level model | AUC_base | AUC_cand | Delta AUC | 95% CI (fixed) | 95% CI (refit) |
|---|---|---|---|---|---|
| B3 (M0) + gateway_j | 0.705 | 0.808 | +0.103 | [0.034, 0.167] | [0.010, 0.212] |
| B5 + size + gateway_j (M2) | 0.770 | 0.807 | +0.037 | - | [-0.018, 0.130] |
| B5 + size + phi_home + density (M2, no gateway) | 0.770 | - | - | - | - |
| B5 + all_four (G, REL, RS, G_all) | 0.697 | 0.782 | +0.085 | [0.004, 0.164] | - |
| B5 + density_j | 0.705 | 0.727 | +0.022 | [-0.031, 0.082] | - |
| B5 + relatedness_to_home_j | 0.705 | 0.705 | -0.000 | [-0.045, 0.035] | - |
| B5 + log_field_size | 0.705 | 0.697 | -0.009 | [-0.042, 0.021] | - |

Gateway centrality is the strongest field level predictor of retention. Relatedness density (from economic complexity) adds only delta AUC = +0.022, and field size is uninformative.

### 5.5 Predicting the next field entered

For predicting which field a concept enters next (conditional logit), relatedness density (AUC = 0.61) beats a permutation null (p = 0.023) but is dominated by log field size (AUC = 0.74). In a conditional logit with both, density still adds signal.

### 5.6 Sensitivity analyses

The newborn only sensitivity (n = 28) reverses the sign of G's delta rho (-0.061), but the sample is too small for LOGO. Among gateway variants, G_btw (betweenness based gateway) gives the largest point estimate (+0.092) but with a wide CI and only 1 of 4 groups positive. G_A (authority based) is the most consistent (3 of 4 groups positive, delta = +0.033).



## 5a. Failed artifacts

**[Addition, iteration 2.]** The iteration-1 strategy (gen_strat_1) commissioned five artifacts. Two did not complete:

1. **gen_art_dataset_1** (outcome blind holdout Frame N concepts plus a 500-pair grounding benchmark): the worker stalled (REPL turn stalled, no new JSONL records for approximately 1,993 seconds). Consequence: no holdout evaluation set was produced in iteration 1. All results in Sections 3 through 5 are therefore dev panel only, and no holdout fields or concept groups were reserved.

2. **gen_art_experiment_2** (candidate S: the number of unconnected coauthor groups among early nonhome adopters, following Cheng et al. 2023): the worker stalled under the same condition. Consequence: candidate S is untested, not refuted. The Cheng et al. social reach hypothesis remains an open rival.

Both failures are carried forward as dead ends (Section 7: "not run, not refuted"). The holdout dataset was rebuilt in iteration 2 (Experiment 5, Section 9).



## 6. Comparison across experiments

### 6.1 Shared baseline strength

**[Correction, iteration 2.]** The original text stated that the five feature baseline "achieves Spearman correlations of 0.77 to 0.83 with rarefied breadth" across all three experiments. Experiment 4's baseline is much weaker: baseline rho = 0.327 (n = 34). The corrected statement: the baseline reaches rho = 0.834 (Experiment 1), 0.770 (Experiment 3) and 0.327 (Experiment 4). The ceiling argument (that incremental gain is narrow) applies only to Experiments 1 and 3. For Experiment 4, the baseline is weak, and G's null cannot be explained by a ceiling; it is explained by the small sample (n = 34), outcome window truncation, and missing t0+3 to t0+4 labels.

Among all indicators tested, entropy alone (Spearman 0.70 with rarefied breadth, positive in all four groups) approaches the full baseline's predictive power. Nonhome share (Spearman 0.42), participation (0.51) and number of reached fields (0.53) are the next strongest single predictors.

### 6.2 The decisive table: no candidate passes

| Candidate | Experiment | Theory | Delta rho | 90% CI | Groups + | r_SB | Survives? |
|---|---|---|---|---|---|---|---|
| A\*_h (naturalisation gap) | 1 | Lineage assortativity | -0.006 | [-0.034, 0.017] | 0/4 | 0.58 | No |
| D_ratio (structural diversity) | 3 | Cooccurrence community | +0.006 | [-0.092, 0.135] | 3/4 | 0.83 | No |
| G (gateway centrality) | 4 | Field relatedness | +0.033 | [-0.095, 0.168] | 2/4 | 0.92 | No |

None of the three theory driven network indicators adds incrementally to the simple baseline on holdout home fields for predicting cross disciplinary breadth. **Note (iteration 2):** this table is not directly comparable across experiments because each used its own rarefied breadth and home field labels. The per experiment baseline rho and the cross experiment outcome agreement matrix are reported in Section 5.1.

[FIGURE:fig_delta_rho]

### 6.3 What worked where

Despite the null at the concept level, three findings survive:

1. **Background homophily measurement:** Background homophily explains 66% of between concept variance in raw lineage autonomy. This is a methodological finding: uniform null indices conflate field composition with concept specific integration. Nearest published neighbour: Ciotti et al. (2016) showed that citation homophily across fields exceeds chance, but they did not decompose it into background and concept specific terms or measure its share of raw lineage autonomy [5].

2. **Field level gateway effect:** The adopting field's gateway centrality on the topic backbone adds delta AUC = +0.10 for retention, surviving a field size control. This is a field level, not concept level, result: whether a specific nonhome field retains a concept is partly predicted by that field's centrality in the field relatedness network. Nearest published neighbour: Hidalgo et al. (2007) showed that a country's position in the product space predicts which products it diversifies into [15]; Guevara et al. (2016) extended this to scientific fields and found entry AUCs of 0.68 to 0.90. The present result concerns retention rather than entry, and conditions on concept level baseline and field size.

3. **Exploratory partial association of D_ratio:** The structural diversity of cooccurrence ties has a partial Spearman of 0.34 with rarefied breadth conditional on the five feature baseline (permutation p = 0.037). **[Correction, iteration 2:]** This finding is marginal, uncorrected (1 of 12 tests), negative in Engineering, and its 95% CI includes zero. Nearest published neighbour: Weng et al. (2013) showed that early community diversity predicts virality in social networks [17]; the present result is the scholarly analogue.



## 7. Dead ends and negative results

1. **A\*_h as a concept level predictor.** The naturalisation gap does not add to simple reach and entropy for predicting breadth. The measurement is too noisy below 60 nonhome children, and the concept by field variance is twice the concept level variance, meaning naturalisation is a local, field specific process rather than a concept level trait.

2. **D_z (z scored structural diversity).** Failed the size diagnostic (Spearman with log volume = -0.63) and was replaced by D_ratio.

3. **F_res (frequency residualised field reach growth).** Negative in 3 of 4 groups, low reliability (r_SB = 0.44), delta rho = -0.060. Residualising reach on the baseline destroys the signal.

4. **Raw cooccurrence growth indicators.** Degree growth, strength growth and new edge rate growth are specific to Computer Science: positively correlated with rarefied breadth in Computer Science (rho 0.45 to 0.47) and near zero or negative in the other three groups (with the exception of new_edge_rate in Medicine at 0.35). They are growth confounded (Spearman with publication growth > 0.70).

5. **Transience** is not evaluable in this panel. Only 4 of 48 (experiment 1) or 4 of 47 (experiment 3) concepts are transient, and all are in Medicine. The predicted dissociation between breadth and transience cannot be tested.

6. **Insularity and paper level label bias.** The credit floor prevented computation of field level insularity and the paper level label bias check.

7. **Candidate S (unconnected coauthor groups).** Not run, not refuted. The artifact stalled, so the Cheng et al. (2023) social reach hypothesis is untested.

8. **O1 gains of gateway variants.** All eight gateway variant O1 (sustained uptake) gains reported in Experiment 4 (+0.05 to +0.15 delta AUC) are label coverage artefacts: G's delta falls from +0.072 to +0.002 after adding label_coverage_early to the baseline [ARTIFACT:art_lwI2DuRtQRZX].

9. **G_all and DOM_Physical on rarefied breadth.** G_all (the share weighted mean gateway centrality across all adopting fields) gives delta rho = -0.240 (95% CI [-0.419, -0.087]), and DOM_Physical (the share of early adoption in Physical Sciences) gives -0.110 ([-0.193, -0.037]). Both harm breadth prediction.

10. **Holdout Frame N dataset.** Not produced in iteration 1 (artifact stalled). Rebuilt in iteration 2.



## 8. What iteration 1 learned

**[Correction, iteration 2: this section formerly said "the ceiling for incremental gain is narrow" without qualification. The ceiling argument applies to Experiments 1 and 3 (baseline rho = 0.83, 0.77) but not to Experiment 4 (baseline rho = 0.33).]**

Three theory driven network indicators were tested on a dev panel of 46 to 48 new scientific concepts (onset 2003 to 2009, four home field groups) against a five feature baseline of popularity and reach. None passes the preregistered decision rule for predicting size adjusted cross disciplinary breadth at t0+6 to t0+8. The baseline (log volume, growth, nonhome share, entropy, reach) is strong in Experiments 1 and 3 (rho 0.77 to 0.83 with rarefied breadth) but weak in Experiment 4 (rho 0.33), where data truncation limits interpretation.

The main findings from iteration 1 are:

- **Background homophily measurement (confirmed):** Two thirds of the between concept variance in raw lineage assortativity is general disciplinary homophily, not concept specific. Cross field indices based on citation patterns must adjust for background homophily to measure anything specific to the concept.
- **Field level gateway effect (lead, not confirmed):** Whether an nonhome field retains a concept is predicted by that field's eigenvector centrality on the topic relatedness backbone, with delta AUC +0.10 (refit 95% CI [0.01, 0.21] over the simple baseline; [-0.02, 0.13] over the full M2 covariate set), surviving a field size control. This is a field level, not concept level, finding. It is a lead, carried forward to iteration 2 for holdout confirmation.
- **Partial association of structural diversity (marginal, uncorrected, 1 of 12 tests):** D_ratio has a partial Spearman of 0.34 with breadth after removing the baseline (permutation p = 0.037). The CI95 includes zero and it is negative in Engineering. Closed as a headline bet in iteration 2.
- **Domain specific indicators (negative result):** Raw cooccurrence growth indicators work only in Computer Science and fail to generalise.
- **Naturalisation is field specific:** The concept by field variance of A\*_h (tau_cj = 0.65) exceeds the concept level variance (tau_c = 0.29). A concept can be naturalised in one field and borrowed in another.
- **O1 gains are label coverage artefacts:** All gateway variant O1 signals collapse when label coverage enters the baseline.
- **Power analysis:** The positive control ladder shows that a feature needs Spearman of approximately 0.95 with rarefied breadth to gain 0.10 over the baseline in Experiments 1 and 3. The panel of 46 to 48 concepts is too small to detect moderate concept level effects.

The three candidates are carried forward in rank order: D_ratio (most portable, passes reliability and 3/4 groups), G (highest delta rho, but only 2/4 groups), A\*_h (fails). Iteration 2 should (a) rebuild the holdout set, (b) test the field level gateway effect on holdout fields with a full covariate set including field retention propensity, and (c) test the next field entry hypothesis (RQ2).



## 8a. Coverage of the original request

**[Addition, iteration 2.]** The table below maps each research question and execution step to its status after iteration 1.

| Step | Status | Artifact |
|---|---|---|
| RQ1: candidate indicator screen (dev) | Done | art_xp8BGBJZsxeI, art_yrradSC27HtQ, art_33_KKk_G8Gw5 |
| RQ1: holdout evaluation | Not started (dataset failed) | - |
| RQ1: top-10 on holdout | Not started | - |
| RQ1: external ground truth (O5) | Not started | - |
| RQ1: exploratory AI first stage | Not started | - |
| RQ2: diffusion trajectories | Not started | - |
| RQ2: field entry conditional logit | Partial (dev, Exp 4) | art_33_KKk_G8Gw5 |
| Grounding benchmark | Not started (dataset failed) | - |
| Explain why strongest indicator works | Not started | - |
| Case studies | Not started | - |
| Optional learned model | Not started | - |



# Iteration 2

## 9. Why this iteration ran

The iteration-1 review raised 13 MUST FIX items and 2 MINOR items. The central objections were:

1. **No holdout evaluation.** The holdout dataset (gen_art_dataset_1) stalled in iteration 1, so every result was dev only. The reviewer's first priority was to build the holdout set and run the gateway retention test (the field retention hypothesis) on it.

2. **The field level gateway lead was not stress tested.** The +0.10 delta AUC on 80 episodes from 28 concepts had no refit CIs, no field retention propensity confound, no rival centralities, and no check for the sustained uptake label coverage artefact.

3. **research question 2 (trajectories) was untouched.** No trajectory clustering, no next field entry conditional logit on holdout data, no ordering tests.

4. **Numerous evidence gaps.** Experiment 4's baseline rho was never stated; the A\*_h medians were misread as within group Spearman correlations; the Experiment 3 portability table was truncated; the Experiment 4 secondary screens were omitted; the sustained uptake gains were not checked for a shared label coverage artefact; refit CIs were not reported; and nearest published neighbours were not cited.

The hypothesis update shifted the headline from the concept level naturalisation gap (null: delta rho -0.006) to the field level gateway retention lead. The unit of analysis became the concept by field adoption episode, backed by the REML finding that concept by field variance exceeds concept variance (tau_cj = 0.65 vs tau_c = 0.29). Three testable consequences were preregistered:

- **the field retention hypothesis (field level, primary):** Gateway centrality predicts retention R_cj beyond the full covariate set (log volume, growth, nonhome share, entropy, reach, field size, relatedness to home, relatedness density) and, critically, beyond the field's leave concept out retention propensity. A degree preserving rewired backbone placebo must give no gain.
- **the entry hypothesis (next field entry, research question 2 (trajectories)):** Relatedness to the fields currently retaining the concept predicts which field a concept enters next, beyond size, Hidalgo density, relatedness to home and the target field's own centrality.
- **the breadth hypothesis (concept level):** The share of early nonhome adoption landing in gateway fields predicts volume residualised breadth, adding to the five feature baseline.

The design called for one common panel built from the zero credit OpenAlex bulk snapshot (476 million works), with outcome blind concept identification, a grounding benchmark, a strict dev/holdout split, and concept clustered refit bootstrap CIs as the only reported CIs. A\*_h and D_ratio were closed as headline bets and scored only inside the frozen indicator matrix.

Five artifacts were executed: a holdout gateway retention test (Experiment 5), a next field entry and trajectory experiment (Experiment 6), a stress test evaluation of the iteration-1 gateway lead (Evaluation 1), an external recognition dataset (Dataset 2), and a positioning study (Research 1).

## 10. Experiment 5: Does the adopting field's gateway centrality predict retention on holdout data? [ARTIFACT:art_wxWssKSUR45f]

### 10.1 Data

One zero credit scan of all 2,040 OpenAlex bulk snapshot parquet files (2026-09-23 snapshot; 476,196,327 works; 129.4 million base works 1995 to 2022). Concepts are identified by Aho-Corasick (a multi-pattern string matching algorithm) title matching of 56,643 legacy OpenAlex concepts (levels 2 to 5) plus Wikidata aliases, with stemmed verification. The matched set contains 60.0 million verified concept paper pairs.

Grounding uses the TAG rule: the legacy concept tag score must be at least 0.3, and the concept name must appear in the title. On a 390-pair LLM labelled benchmark with 60 hand checked pairs (90% agreement between LLM and hand labels), the TAG rule achieves test precision 0.947 and recall 0.659 (F1 0.777). A per concept LLM precision gate ($2.28 of OpenRouter) drops concepts with precision below 0.80.

### 10.2 Panel

The panel comprises 12,499 concepts and 27,393 concept by field episodes:

| Split | Concepts | Episodes |
|---|---|---|
| DEV (CS/Eng/BGM/Med, onset 2003-2009) | 4,771 | 9,079 |
| COHORT (onset 2010-2014, all fields) | 4,356 | 9,799 |
| HELDOUT_PHYS | 742 | 1,662 |
| HELDOUT_LIFEENV | 1,113 | 3,099 |
| HELDOUT_SOC | 1,352 | 3,320 |
| HELDOUT_MATHDEC | 165 | 434 |
| **Total** | **12,499** | **27,393** |

The dev retention rate is 29.4%. The spec was frozen on DEV data (hash sealed before holdout scoring) and unsealed once for holdout scoring.

### 10.3 Field retention hypothesis: result: DISCONFIRMED

The full covariate set includes: the five feature baseline (log volume, growth, nonhome share, entropy, reach), log field size, relatedness to home (phi_home_j), relatedness density, leave concept out field retention propensity (P_j(-c)), label coverage and episode size. Gateway centrality is the frozen 1998-2002 eigenvector centrality of the adopting field on the 26-field PMI backbone.

| Metric | DEV | Holdout | Cohort |
|---|---|---|---|
| Delta AUC (gateway over X0) | +0.00001 | -0.00001 | -0.0001 |
| 95% CI (refit) | [-0.0007, +0.0005] | [-0.0006, +0.0003] | [-0.0008, +0.0001] |
| AUC X0 | - | 0.837 | - |
| AUC X1 (X0 + gateway) | - | 0.837 | - |

Per holdout group:

| Group | Delta AUC |
|---|---|
| Physical | +0.0005 |
| Life & Environment | -0.0003 |
| Social Sciences | -0.0001 |
| Mathematics & Decision | +0.0005 |

DerSimonian-Laird pooled delta AUC: -0.00004 (I squared = 0, Q = 1.69). The placebo is not exceeded and the conditional logit is null (beta = -0.075, z = -1.20, p = 0.23). Verdict: **DISCONFIRMED** by all preregistered criteria.

### 10.4 Why gateway vanished: the baseline ladder

The baseline ladder shows where the iteration-1 signal goes:

| Baseline step | DEV delta AUC | Holdout delta AUC |
|---|---|---|
| L0: field size only | +0.0042 | -0.0017 |
| L1: iteration-1 base (B3) | +0.0019 | -0.0016 |
| L2: + relatedness pair | +0.0007 | -0.0012 |
| L3: + retention propensity P_j(-c) | +0.00003 | -0.00004 |
| L4: full X0 | +0.00001 | -0.00001 |

Gateway's dev panel signal (+0.0019 over the iteration-1 base) vanishes once the field's leave concept out retention propensity is added. On holdout data, the signal is negative at every step.

Gateway centrality alone has AUC 0.605 on DEV versus 0.506 on holdout (0.41 in Social Sciences). Gateway is a domain specific proxy for "fields that keep things," not a position dependent causal factor.

### 10.5 The relatedness pair beats gateway

The rival covariate pair (relatedness to home and relatedness density) adds delta AUC +0.0034 on holdout data (95% CI [0.0010, 0.0051]), compared to gateway's -0.00005 (95% CI [-0.0007, +0.0002]). The difference is -0.0034, favouring relatedness.

### 10.6 Concept breadth hypothesis: result: small but confirmed

Gateway weighted early landing G predicts volume residualised breadth on holdout data, but the effect is small:

| Variant | Holdout partial rho | Holm corrected p |
|---|---|---|
| G (eigenvector) | 0.030 | 0.0045 |
| G_A (authority) | 0.026 | 0.0045 |
| G_btw (betweenness) | 0.046 | 0.0045 |
| REL_home | -0.136 | 1.0 |

DerSimonian-Laird pooled partial rho for G: 0.068 (95% CI [0.029, 0.107], I squared = 0). The Holm corrected permutation p is 0.0045 for all three gateway variants (0 of 40 shuffled outcomes exceed the real value). REL_home is strongly negative (-0.14), meaning that concepts whose home field is closely related to many other fields tend to achieve less size adjusted breadth.

### 10.7 Minimum detectable effect and power

The minimum detectable delta AUC is 0.004 (at 80% power, 27,393 episodes). With only 26 fields, the standard deviation of the delta AUC under the alternative stays at approximately 0.015 regardless of the number of episodes (1,000 to 4,000), creating a floor. Approximately 34 holdout concepts per group give P(group delta > 0) >= 0.90 at a true delta of 0.05.

### 10.8 Iteration-1 replication

Reproducing the iteration-1 analysis on the new panel gives delta AUC +0.023 (vs the reported +0.103). The original +0.103 was on 80 episodes from 28 concepts; on the evaluation's harmonised union panel of 362 episodes from 54 concepts, the delta is +0.001 (95% CI [-0.012, +0.012]) [ARTIFACT:art_lwI2DuRtQRZX].

### 10.9 Deviations

- No OpenAlex API audit or insularity computation (credits exhausted).
- LLM budget cap raised from $2.00 to $3.50 (13,000 onset candidates vs planned 5,000).
- Onset year agreement between the new panel and the iteration-1 iteration-1 panel (78 concepts) is 53%.
- Conference papers excluded (type = article or review only); conference heavy Computer Science is undercovered.
- 896 concepts without an LLM precision label were gated by the sense filter.

[FIGURE:fig_h1_ladder]



## 11. Experiment 6: Where new scientific concepts spread next [ARTIFACT:art_N-mpomDZZ1ln]

### 11.1 Panel and grounding

A separate full corpus scan produces 653 newborn concepts (legacy concept lexicon, tag AND title grounding; benchmark precision 0.996 from LLM and hand labels at $0.007). The panel is split into dev (CS/Eng/BGM/Med homes, onset 2003-2009; 279 concepts) and holdout (other fields plus the 2010-2014 cohort; 374 concepts), run once after a hashed freeze.

| Split | Concepts | Episodes |
|---|---|---|
| Dev (CS/Eng/BGM/Med, t0 2003-09) | 279 | 707 |
| Holdout field groups | 126 | 390 |
| Holdout cohort (2010-14) | 248 | 768 |
| **Total** | **653** | **1,865** |

The episode count (1,865) falls short of the 4,000 target. MathDec is untestable (too few concepts). The sense filter proved uninformative (test AUC 0.24); grounding relies entirely on the tag AND title rule.

### 11.2 Next field entry hypothesis: CONFIRMED

A conditional logit on concept year risk sets tests whether relatedness to the nonhome fields that currently retain the concept predicts which field a concept enters next, beyond field size, Hidalgo relatedness density, relatedness to home and the target field's own gateway centrality.

**Dev results (274 concepts, 887 entry events):**

| Model | Log likelihood | Converged |
|---|---|---|
| M0 (size, density, phi_home, gate_own) | -2,170.9 | Yes |
| M1 (M0 + ret_rel plain) | -2,153.6 | Yes |
| M2 (M0 + ret_gate weighted) | -2,151.6 | Yes |
| M3 (M0 + ret_rel + ret_gate) | -2,151.3 | Yes |

the gateway weighted model vs the baseline: LR = 38.6 (p = 5.1 x 10^-10). The standardised coefficient d for gateway weighted retaining relatedness is 0.250 (bootstrap 95% CI [0.182, 0.321]). Label permutation p = 0.009; rewired backbone p = 0.030.

Within stratum AUCs on dev:

| Predictor | AUC |
|---|---|
| M0 (full baseline) | 0.801 |
| M2 (+ ret_gate) | 0.805 |
| Log field size alone | 0.708 |
| Relatedness density alone | 0.606 |
| Retaining field gateway relatedness alone | 0.561 |

**Holdout results (369 concepts, 1,373 entry events):**

the gateway weighted model vs the baseline: LR = 71.7 (p = 2.5 x 10^-17). d = 0.30 (bootstrap 95% CI [0.24, 0.37]).

| Decision criterion | Value | Passes? |
|---|---|---|
| LR p < 0.01 | 2.5 x 10^-17 | Yes |
| d > 0 and CI > 0 | 0.30 [0.24, 0.37] | Yes |
| Positive in >= 3 of 3 evaluable field groups | Physical +0.33, LifeEnv +0.18, Social +0.24 | Yes |
| Cohort positive | +0.29 [0.22, 0.36] | Yes |
| Label permutation p < 0.05 | 0.001 | Yes |
| Rewired backbone gain above null 95th pct | Yes (p = 0.015) | Yes |

DerSimonian-Laird pooled d: 0.28 (95% CI [0.22, 0.35], I squared = 0, Q = 0.75).

**Verdict: CONFIRMED** by the frozen rule. But the gateway weighting adds nothing beyond plain retaining relatedness (the combined model vs the plain relatedness model, gateway only permutation p = 0.17 holdout, 0.31 dev), and target field size is the strongest single block (AUC 0.76 vs density 0.59). The incremental AUC from baseline to the gateway weighted model is only 0.809 to 0.817.

Holdout per group details:

| Group | N concepts | N events | d | Boot 95% CI | LR | LR p |
|---|---|---|---|---|---|---|
| Physical | 30 | 92 | 0.332 | [0.046, 0.565] | 3.91 | 0.048 |
| Life & Environment | 34 | 118 | 0.178 | [-0.096, 0.506] | 1.47 | 0.226 |
| Social | 53 | 161 | 0.245 | [-0.008, 0.459] | 3.15 | 0.076 |
| MathDec | 0 | - | - | too few | - | - |
| Cohort | 248 | 989 | 0.292 | [0.222, 0.361] | 54.0 | 2.0 x 10^-13 |

### 11.3 Ordering: first retained gateway precedes entropy takeoff

Among 175 concepts in the top rarefied breadth tercile, 112 (64%) have a detected entropy change point. Of those with an evaluable ordering:

| Condition | N evaluable | Share "before" (excl. ties) | Sign test p (one sided) |
|---|---|---|---|
| First retained gateway field | 102 | 65.5% | 0.003 |
| First retained peripheral field | 106 | 57.0% | 0.118 |

McNemar test comparing gateway vs peripheral: p = 0.088 (27 gateway only, 15 peripheral only). The ordering result is confirmed by the preregistered rule (>= 60% and sign p < 0.01), but the lead lag gateway permutation placebo gives p = 0.63, meaning the panel does not single out gateway fields as the unique driver. The lead lag panel regressions with concept fixed effects show that both retained gateway and retained peripheral fields are associated with subsequent entropy change, but the reverse (entropy predicting retention) is not significant (p = 0.22).

### 11.4 Rescue and relay mechanisms: NOT SUPPORTED

The metapopulation rescue hypothesis (retained gateway fields keep a concept alive through reimportation from neighbouring fields) is not supported on holdout data. The interaction between retention and gateway tercile on background adjusted citation provenance is -0.217 (95% CI [-1.12, 0.68]). The mediation indirect effect is 0.002 (95% CI [-0.007, 0.010]).

The relay hypothesis (retained gateway fields radiate the concept onward) is also not supported. The fixed effects Poisson coefficient for the retention by gateway interaction on excess onward entries is -1.30 (95% CI [-4.93, 2.33]). The mean excess entries from gateway retained fields is -0.011.

### 11.5 Trajectories: two stable classes

DTW k-medoids with k = 2 is stable (bootstrap ARI 1.0). The two classes are "integrating" (128 concepts) and "localised" (60 concepts), matched on initial volume. The holdout independent recluster gives ARI 0.54.

| Feature (year 9) | Integrating (cluster 0) | Localised (cluster 1) |
|---|---|---|
| Fields entered (nonhome) | 9.1 | 5.0 |
| Fields retaining | 6.7 | 2.9 |
| Fields lost | 0.5 | 0.6 |
| Rarefied breadth (O2r, m = 30) | 5.2 | 2.8 |
| Shannon entropy | 1.31 | 0.42 |
| Gateway share | 0.17 | 0.04 |
| Log volume | 5.4 | 4.8 |

The localised class is dominated by Medicine home concepts (42 of 60 localised vs 14 of 128 integrating from Medicine). Intersection born concepts (at least 2 home fields): 9 in the integrating class, none in the localised class.

[FIGURE:fig_trajectories]

### 11.6 Audit

The independent audit reproduces the retaining relatedness coefficient, the gateway permutation p and holdout AUCs exactly. An exact likelihood conditional logit gives LR 77.3 and DerSimonian-Laird pooled d 0.32 [0.25, 0.39] (the Breslow partial likelihood pipeline is conservative). Within stratum shuffled labels reject 0 of 20 times. A random year ordering placebo gives 0.43 (vs the real 0.66), confirming that the ordering is not an artefact of temporal structure.

### 11.7 Deviations

- 1,865 episodes, below the 4,000 target.
- MathDec untestable (0 holdout field group concepts in iteration 2's frame).
- Sense filter uninformative (test AUC 0.24); grounding relies on tag AND title.
- No Wikidata aliases (rate limited; lexicon uses display names and plural variants only).



## 12. Evaluation 1: Does the gateway field retention signal replicate? [ARTIFACT:art_lwI2DuRtQRZX]

### 12.1 Design

This zero API stress test reevaluates iteration 1's only live lead: gateway centrality adding +0.103 AUC for field retention on 80 episodes. The evaluation harmonises the three iteration-1 experiments onto a common covariate set (the five feature baseline + log field size + relatedness to home + relatedness density) and tests gateway on each experiment's panel, their deduplicated union (362 episodes, 54 concepts) and a new episodes only subset (282 episodes). All CIs are concept clustered refit bootstrap (2,000 draws, percentile).

### 12.2 Reproduction and headline

The iteration-1 numbers reproduce exactly: +0.10254 (exp4, the simple baseline) and +0.10222 (size controlled).

| Panel | Delta AUC (gateway over M2) | 95% CI (refit) | Groups + |
|---|---|---|---|
| Exp 4 (80 rows, 28 concepts) | +0.037 | [-0.018, 0.130] | 4/4 |
| Exp 1 (367 rows, s2-fos crosswalk) | +0.001 | [-0.021, 0.009] | 2/4 |
| Exp 3 (129 rows) | -0.006 | [-0.052, 0.070] | 1/4 |
| Union (362 rows, 54 concepts) | +0.001 | [-0.012, 0.012] | 1/4 |
| New episodes only (282 rows) | -0.001 | [-0.021, 0.017] | 3/4 |

DerSimonian-Laird pooled delta AUC: +0.0015 (I squared = 0). The preregistered verdict: **FAILS**. The conditions not met: new episodes delta <= 0, union CI includes zero, union positive in only 1 of 4 groups.

### 12.3 Trait confound

**Retention propensity.** Adding the leave concept out field retention propensity P_j(-c) to the full covariate set on the union panel, gateway adds only +0.0015.

**Field intercepts.** Gateway explains 50% of Experiment 4's field intercepts (p = 0.14, 10 fields) and removes 74% of the field variance there, but R squared is 0.03 (p = 0.55) and only 2.5% on the union panel.

**Time varying backbone.** The time varying backbone validates (Spearman 0.92 between the 2000-04 slice and the 1998-2002 backbone), but the within field variation is not identifiable (within/between SD = 0.023).

### 12.4 Placebos

**Rewired backbone.** Degree preserving rewiring discriminates eigenvector from degree (median Spearman between real and rewired eigenvector = 0.32). On Experiment 4's simple baseline, the real value is at p = 0.01; on the union panel, it is not significant. No rival centrality (strength, degree, betweenness, PageRank, closeness, k-core, phi_min eigenvector, field size) survives Holm correction on the union panel.

**Node label permutation.** The union panel's real delta AUC sits at the 54th percentile of the node label permutation null. The gateway signal is indistinguishable from a random relabelling of the 26 fields.

### 12.5 Sustained uptake artefact

All eight gateway variant sustained uptake gains are label coverage artefacts. After adding label_coverage_early (and the sustained uptake base rate) to the five feature baseline:

| Variant | B5 delta | B5+cov delta | B5+cov+O1base delta | Artefact? |
|---|---|---|---|---|
| G | +0.072 | +0.016 | +0.002 | Yes |
| G_all | +0.112 | +0.021 | +0.021 | Yes |
| G_deg | +0.149 | - | - | Yes |
| G_phimin | +0.154 | - | - | Yes |
| G_A | +0.075 | - | - | Yes |
| REL_home | +0.121 | - | - | Yes |

### 12.6 Power

With a field random intercept (sigma_field = 0.71, from the union panel), the standard deviation of delta AUC under the alternative stays at approximately 0.015 regardless of sample size (1,000 to 4,000 episodes). The minimum detectable effect floor is approximately 0.02, set by the 26-field granularity. Approximately 34 holdout concepts per group give P(group delta > 0) >= 0.90 at a true delta of 0.05.

### 12.7 Shuffled R placebo on Experiment 4

A shuffled R placebo on Experiment 4's 80 rows gives a 95th percentile of 0.130, above the observed +0.103. The original iteration-1 lead cannot be certified as above chance on 80 episodes.



## 13. Dataset 2: When research concepts were officially recognised [ARTIFACT:art_O7Dq4L02QnDN]

An external recognition lookup table for all 65,026 OpenAlex legacy concepts (64,723 target concepts at levels 2 to 5), built with zero OpenAlex credits and $1.49 of OpenRouter calls. Every event is dated and sourced.

### 13.1 Sources

| Source | Concepts matched | Date type |
|---|---|---|
| MeSH 2026 | 20,872 | DateIntroduced year |
| English Wikipedia | 6,540 exact first revisions | Creation date (redirect first repair) |
| Wikidata P571/P575 | 1,425 | Inception/date of first description |
| ACM CCS 1998/2012 | 3,583 | taxonomy_in_version |
| MSC 2000/2010/2020 | 17,872 | taxonomy_in_version |
| PACS 2010/PhySH | 8,462 | taxonomy_in_version |
| Curated lists (NM MoTY, Science BOTY, MIT TR10, Gartner, Research Fronts) | 589 | Event year |
| JEL | 1,015 | Present day membership only |

### 13.2 Quality

All known answer asserts pass (optogenetics NM 2010, iPSC NM 2009, CRISPR BOTY 2015, superresolution NM 2008). Audit precision: 0.96 for label matches, 0.79 for ID links, 0.31 for alias only matches (alias matches were LLM verified; accepted LLM links are 0.97 precise on hand check). Intermodel kappa is 0.60 (accept/reject).

Coverage is uneven: Social Sciences and Engineering have no dated domain taxonomy, so a Wikipedia/Wikidata only external recognition variant is needed for cross group comparisons. Wikipedia creation dates cluster in its 2001-2007 growth wave, and Research Fronts are citation derived.

The dataset includes a provisional dev/holdout/unassigned split (19,600/28,300/17,100 concepts) based on level-1 ancestors mapped to OpenAlex fields and then to the hypothesis groups.



## 14. Research 1: How our results compare with related papers [ARTIFACT:art_dxvRpQufMR0e]

A positioning study for the Applied Network Science paper. The key comparative findings:

1. **Field entry versus retention.** Guevara et al. (2016) report field entry AUCs of 0.68 to 0.90 for the research space; no published AUC exists for retention or exit of an adopted concept. The iteration-1 delta AUC of +0.10 for gateway predicted retention had no direct counterpart, but it has now been disconfirmed on holdout data.

2. **Relatedness principle.** Neffke et al. (2011), Rigby (2015) and others credit relatedness for both entry and exit/survival of activities. The holdout test confirms that the relatedness pair (phi_home_j plus density) adds delta AUC +0.0034 (95% CI [0.0010, 0.0051]), beating gateway (which adds nothing). The principle of relatedness (the empirical regularity that regions and fields diversify into activities related to their existing portfolio [18]) is confirmed for concept field retention, though the effect is small.

3. **Gateway and centrality.** Adopter centrality retention is new for concept adoption by fields but partially anticipated by Hidalgo (2007, product space position predicts diversification speed) and Yenilmez (2026, centrality explains diversification). The present data show that gateway centrality is a domain specific proxy absorbed by field retention propensity, not a position dependent mechanism.

4. **Retaining relatedness for next field entry.** The confirmed entry hypothesis result (d = 0.30 on holdout, pooled 0.28) is new: no prior study has tested whether relatedness to the set of fields currently retaining a concept predicts the next field entered, beyond relatedness to the home field. This goes beyond the "principle of relatedness" (which uses relatedness to the actor's own portfolio) by using the concept's retaining community as the reference set.

5. **Background homophily.** The background homophily measurement (66% of between concept variance in raw lineage log odds is background homophily) is the concept level analogue of Ciotti et al. (2016). The present result is new in that it decomposes citation homophily into a background term and a concept specific term.



## 15. Dead ends and negative results from iteration 2

1. **the field retention hypothesis (field level gateway retention): DISCONFIRMED.** On 27,393 episodes from 12,499 concepts, gateway centrality adds delta AUC -0.00001 (95% CI [-0.0006, +0.0003]) over the full covariate set. The signal is absorbed by the field's retention propensity and reverses sign on holdout data. Gateway alone has AUC 0.506 on holdout (0.41 in Social Sciences).

2. **Rescue mechanism: NOT SUPPORTED.** The interaction between retention and gateway tercile on background adjusted citation provenance is null (coefficient -0.22, CI including zero).

3. **Relay mechanism: NOT SUPPORTED.** Retained gateway fields do not radiate more onward entries than peripheral fields (coefficient -1.30, CI including zero).

4. **Gateway weighting in the entry hypothesis.** The gateway weighting of retaining relatedness adds nothing beyond plain retaining relatedness (the combined model vs the plain relatedness model: gateway only permutation p = 0.17 holdout).

5. **Iteration-1 gateway lead on 80 episodes.** Cannot be certified as above chance: the shuffled R placebo's 95th percentile (0.130) exceeds the observed +0.103.

6. **Sustained uptake gains of all gateway variants.** All are label coverage artefacts.

7. **Node label permutation test.** The union panel's real delta sits at the 54th percentile of the null, indistinguishable from random field labelling.



## 16. What we have learned so far

Two iterations and eight artifacts have tested whether temporal network signals predict how new scientific concepts spread across disciplines, using OpenAlex data on 12,499 to 65,026 concepts with up to 27,393 concept by field adoption episodes.

**Confirmed findings:**

1. **Retaining relatedness predicts the next field entered (the entry hypothesis, confirmed on holdout data).** A conditional logit on concept year risk sets shows that relatedness to the fields currently retaining a concept predicts which field the concept enters next, beyond field size, Hidalgo relatedness density, relatedness to home and the target field's own gateway centrality. Holdout likelihood ratio 71.7 (p = 2.5 x 10^-17), standardised d = 0.30 (95% CI [0.24, 0.37]), positive in all three evaluable holdout field groups and the 2010-2014 cohort, DerSimonian-Laird pooled d = 0.28 (95% CI [0.22, 0.35], I squared = 0). The label permutation null and the rewired backbone placebo are both rejected.

2. **Two stable trajectory classes (research question 2 (trajectories)).** DTW k-medoids separates 188 concepts with sustained uptake into "integrating" (128 concepts, mean 6.7 fields retaining by year 9, O2r 5.2) and "localised" (60 concepts, mean 2.9 fields retaining, O2r 2.8). The localised class is dominated by Medicine home concepts. Holdout independent recluster ARI = 0.54.

3. **Ordering: first retained gateway field precedes entropy takeoff.** In 66% of broad concepts, the first retained gateway field precedes the calibrated entropy takeoff (sign p = 0.003). The lead lag gateway permutation placebo (p = 0.63) says the panel does not single out gateway fields specifically; retained peripheral fields also precede entropy takeoff in 57% of cases.

4. **Background homophily dominates raw lineage (the background homophily measurement).** Two thirds of between concept variance in raw lineage log odds is general disciplinary homophily. This is confirmed across 48 dev concepts and is a methodological finding for any study using citation based cross field indices.

5. **Concept level gateway landing predicts volume residualised breadth (the breadth hypothesis, small effect, confirmed).** Holdout partial rho of G_btw with volume residualised breadth = 0.046 (Holm p = 0.0045); DerSimonian-Laird pooled G = 0.068 (95% CI [0.029, 0.107]). The effect is real but small.

**Disconfirmed:**

1. **Gateway centrality does not predict field retention (the field retention hypothesis).** On holdout data, delta AUC is -0.00001. The iteration-1 lead (+0.103 on 80 episodes) was a small sample artefact absorbed by the field's retention propensity.

2. **Rescue and relay mechanisms are not supported.** Neither the reimportation nor the onward radiation mechanism of the metapopulation analogy is detectable in the data.

3. **No concept level network indicator beats the simple baseline.** All three theory driven indicators (naturalisation gap, structural diversity, gateway landing) fail the preregistered decision rule for predicting raw rarefied breadth. Power analysis shows that with baseline rho = 0.77 to 0.83, a feature needs Spearman approximately 0.95 with breadth to gain 0.10.

**Open:**

- The indicator screen's full indicator by outcome by field matrix has not been computed on the new common panel. The Experiment 3 cooccurrence indicators and the Experiment 1 lineage indicators have not been rescored on the iteration-2 frame.
- External recognition has been compiled but not used as an outcome.
- The learned model (optional extension) has not been attempted.
- Candidate S (unconnected coauthor groups) remains untested.



## References

[1] Salatino, A., Osborne, F., & Motta, E. (2017). How are topics born? Understanding the research dynamics preceding the emergence of new areas. PeerJ Computer Science, 3, e119.

[2] Weng, L., Menczer, F., & Ahn, Y.-Y. (2013). Virality Prediction and Community Structure in Social Networks. Scientific Reports, 3, 2522.

[3] Rotolo, D., Hicks, D., & Martin, B. R. (2015). What is an emerging technology? Research Policy, 44(10), 1827-1843.

[4] Cheng, M., Smith, D. S., Ren, X., Cao, H., Smith, S., & McFarland, D. A. (2023). How New Ideas Diffuse in Science. American Sociological Review, 88(3), 522-561.

[5] Ciotti, V., Bonaventura, M., Nicosia, V., Panzarasa, P., & Latora, V. (2016). Homophily and missing links in citation networks. EPJ Data Science, 5, 7.

[6] Lipsitch, M., Tchetgen Tchetgen, E., & Cohen, T. (2010). Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies. Epidemiology, 21(3), 383-388.

[7] Maillart, T., Chataing, A., et al. (2026). Forecasting Conceptual Diffusion in Science: The Case of Quantum Computing. arXiv:2606.03919.

[8] Renoust, B., Claver, V., & Basse, J.-F. (2017). Multiplex flows in citation networks. Applied Network Science, 2, 23.

[9] Chen, C. (2006). CiteSpace II: Detecting and Visualizing Emerging Trends and Transient Patterns in Scientific Literature. Journal of the American Society for Information Science and Technology, 57(3), 359-377.

[10] Rafols, I., & Meyer, M. (2009). Diversity and network coherence as indicators of interdisciplinarity: case studies in bionanoscience. Scientometrics, 82, 263-287.

[11] Salatino, A., Osborne, F., & Motta, E. (2018). AUGUR: Forecasting the Emergence of New Research Topics. Proceedings of the 18th ACM/IEEE JCDL, 303-312.

[12] Hawkes, A. G. (1971). Spectra of some self exciting and mutually exciting point processes. Biometrika, 58(1), 83-90.

[13] Pastor-Satorras, R., Castellano, C., Van Mieghem, P., & Vespignani, A. (2015). Epidemic processes in complex networks. Reviews of Modern Physics, 87, 925-979.

[14] De Domenico, M., Omodei, E., & Arenas, A. (2016). Quantifying the diaspora of knowledge in the last century. Applied Network Science, 1, 15.

[15] Hidalgo, C. A., Klinger, B., Barabasi, A.-L., & Hausmann, R. (2007). The Product Space Conditions the Development of Nations. Science, 317(5837), 482-487.

[16] Guevara, M. R., Hartmann, D., Aristarán, M., Mendoza, M., & Hidalgo, C. A. (2016). The research space: using career paths to explore the structure of scientific research. Scientometrics, 109, 1695-1709.

[17] Weng, L., Menczer, F., & Ahn, Y.-Y. (2013). Virality Prediction and Community Structure in Social Networks. Scientific Reports, 3, 2522.

[18] Hidalgo, C. A., Balland, P.-A., Boschma, R., Delgado, M., Feldman, M., Frenken, K., Glaeser, E., He, C., Kogler, D. F., Morrison, A., Neffke, F., Rigby, D., Stern, S., Zheng, S., & Zhu, S. (2018). The Principle of Relatedness. In Unifying Themes in Complex Systems IX (pp. 451-457). Springer.

[19] Neffke, F., Henning, M., & Boschma, R. (2011). How do regions diversify over time? Industry relatedness and the development of new growth paths in regions. Economic Geography, 87(3), 237-265.

[20] Rigby, D. L. (2015). Technological relatedness and knowledge space: entry and exit of US cities from patent classes. Regional Studies, 49(11), 1922-1937.

[21] Fontaine, M. C., Bhatt, U., Bhargava, R., & Aglietti, V. (2024). Epistemic integration and social segregation of AI in neuroscience. Applied Network Science, 9, 12.

[22] Maillart, T. et al. (2026). Explainable Forecasting of Scientific Breakthroughs from Concept Network Dynamics. arXiv:2606.03864.

[23] Muntakim, A. H., et al. (2026). SciTraj: How Does Research Evolve? Tracing Cross-Domain Trajectories in NLP, ML, and CV Through Claim-Grounded Typed Citations. arXiv:2606.22342.

</report>

<supplementary_materials>
The run's code, data, and experimental artifacts. This is your ground truth: the report is
complete only if everything here that ran is written up in it, tables and all. Read them —
check that the code matches the described methodology, that each reported number appears in
an output file, and that no executed artifact is missing from the report.

--- Item 1 ---
id: art_xp8BGBJZsxeI
type: experiment
title: Does citing a concept 'as your own' predict its spread?
summary: |-
  Screen of candidate L, the background-adjusted naturalisation gap A*_h, on the frozen P78 dev panel. Headline: it does NOT survive the pre-registered rule.
  PANEL: 48 dev concepts (Biochem 13, CS 21, Engineering 3, Medicine 11). Dropped: 22 with t0 outside 2003-2009 and 8 with a sealed home field.
  RULE CLAUSES:
  - LOGO Delta-rho for O2r over B5 = -0.006, 90% concept-bootstrap CI [-0.034, 0.017]; rho_B5 = 0.834. FAIL.
  - Positive left-out groups: 0 of 4. FAIL.
  - Split-half reliability (Spearman-Brown) = 0.58. FAIL (bar 0.6).
  - Abs Spearman with log early volume / early growth = 0.14 / 0.18. PASS.
  OTHER RESULTS:
  - A*_h's within-field sign flips: Medicine +0.45, CS -0.18.
  - Field-level rho*_cj -> R_j: Delta-AUC +0.002, CI [-0.011, 0.016], over 367 units.
  - O1 uptake: Delta-AUC -0.026. O3 transience is degenerate (4 positives of 48).
  - M1: R^2 of raw lineage log-OR on background log-OR = 0.66; the background log-OR is positive for 48/48 concepts. Raw lineage is mostly homophily.
  - Reliability vs n: 0.72 only above 60 off-home children. On those 11 concepts Delta-rho = +0.118, CI [0, 0.355], underpowered.
  - REML tau_c = 0.29, tau_cj = 0.65. PyMC NUTS check passes (Spearman 0.9996 with REML).
  - None of the 14 candidate and foil features, scored as exploratory candidates, beats B5.
  DATA DEVIATION: the shared OpenAlex credit pool ran dry (139 own credits spent). Yearly counts (t0, O1, O3, volume, growth) are OpenAlex S0 exactly. Field labels, concept papers, citation lineage and background-reference fields come from free Semantic Scholar data: fractional s2-fos text-classifier fields. Child reference lists come from free OpenAlex singleton GETs. The S2 and OpenAlex O2r agree with Spearman 0.87 on 11 concepts.
  AUDIT (audit/rederive.py, independent code paths): Delta-rho, rho_B, the size correlations, O1 Delta-AUC and M1 are re-derived exactly; field-level Delta-AUC is 0.0020. A shuffled-A*_h placebo passes 0 of 200 times. Power caveat: with rho_B5 = 0.83, a feature needs Spearman of about 0.95 or more with O2r to pass the Delta >= 0.10 clause. Reliability 0.58 was NOT independently re-derived.
  FILES: results/features.csv, field_features.csv, outcomes.csv, field_outcomes.csv, screen_result.json (all statistics and deviations), screen_table.csv (OOF predictions), dropped.csv, audit/rederive_out.json. method_out.json follows exp_gen_sol_out and holds per-concept B5 and B5+A*_h predictions plus field-retention units.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md

--- Item 2 ---
id: art_yrradSC27HtQ
type: experiment
title: Do diverse topic ties predict concept spread?
summary: >-
  Screen of two co-occurrence emergence indicators on the frozen P78 dev panel under shared protocol S0 (47 dev concepts:
  BIO 16, CS 12, MED 10, ENG 9). The shared OpenAlex key was exhausted, so S0 yearly counts (t0, newborn, O1, O3, logvol,
  growth) came from 156 anonymous API credits, and everything else came from a zero-credit column-pruned scan of all 476M
  works in the 2026-09-23 OpenAlex S3 snapshot. Venue-field compositions (home, O2r, R_j, entropy) and ego topics use title-matched
  works (median 48% of API volume; rho 0.88). Backbone: full-corpus topic PMI per slice (2000-04/05-09/10-14), Leiden gamma=3
  (25/26/23 communities; the plan rule gave about 8, reported as D_q). D_z failed the T3 size diagnostic (rho with log volume
  -0.63), so the pre-declared fallback D_ratio is the primary D. RESULTS (LOGO ridge, 2,000 stratified concept bootstraps):
  B5 alone reaches rho 0.770 with O2r. D_ratio delta-rho +0.006 [90% CI -0.092, 0.135], 3/4 groups positive, SB 0.83. F_res
  delta-rho -0.060 [-0.158, 0.014], 1/4 groups positive, SB 0.44. No candidate survives the pre-registered rule; D is carried
  forward as the best available result and the null is reported. Dissociation tests are inconclusive; O3 is not estimable
  (all transient concepts are Medicine); field-level R_j dAUC is about 0. Portability: D_ratio, D_rare, participation and
  NOV_res are associated with O2r in all 4 groups (rho 0.45-0.63) but are redundant under delta-rho. Degree, strength and
  new-edge growth are CS-only (a negative result). EXPLORATORY: the out-of-group partial rho of D_ratio given B5 is 0.335
  [0.02, 0.65], permutation p=0.037; delta-rho is near its ceiling because B5 is already strong. Audit: all headline numbers
  re-derived exactly by independent code; the placebo fails and the planted control passes. Files: results/outcomes.csv, field_outcomes.csv,
  features.csv (about 30 indicators), screen_result.json, exploratory_partial_association.json, audit.json, deviations.json;
  method_out.json (47+47+129 LOGO predictions).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md

--- Item 3 ---
id: art_33_KKk_G8Gw5
type: experiment
title: Where a concept lands early vs how broadly it spreads
summary: >-
  Screen of candidate G (gateway landing) on the frozen P78 dev panel under protocol S0. This artifact is also the AUTHORITATIVE
  producer of the shared outcome tables: outcomes.csv (all 78 rows; O1 uptake, O2r rarefied venue-field breadth m=30/50, O2r_resid,
  O2_raw, O3 transience, t0, newborn flag, home, group, label coverage, trunc flag), field_outcomes.csv (80 concept x off-home-field
  retention rows), features.csv (G family, ~20 simple reference indicators, B5 columns) and single_indicators.csv (pooled,
  per-group and DerSimonian-Laird Spearman/AUC with I2). RESULTS: 46 dev concepts (34 with an outcome window). Leave-one-home-group-out
  ridge, B5 vs B5+G on O2r: Delta-rho=+0.033, 90% CI [-0.095,0.168], positive in 2/4 groups, so G does NOT survive the pre-registered
  rule, although reliability (r_SB=0.92) and the size check (|rho|<=0.13) pass. Secondary: O2r residualised on log N gives
  Delta-rho=+0.15, CI90 [0.000,0.321], 4/4 groups. O1 Delta-AUC=+0.072, CI90 [0.00,0.16]. O3 is not evaluable (2 positives).
  Field level: the adopting field's gateway centrality adds +0.10 AUC for retention, 95% CI [0.03,0.17], and survives a field-size
  control (not in CS). Next-field entry: relatedness density AUC 0.61 beats the permutation null (p=0.023) but loses to log
  field size (0.74); in conditional logit, density still adds signal. CAVEATS: the shared OpenAlex key hit its 1,000-credit
  floor after 286 credits, so the t0+3..t0+4 labels are missing (label-based B5 parts use t0..t0+2), outcome windows keep
  only the top-200 sources (29/34 truncated), and insularity, SLICE_B and P5 were not computed. The backbone is 1998-2002
  topic co-assignment PMI over 26 fields (field_backbone.json). Cache is frozen in cache/raw.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_4
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md

--- Item 4 ---
id: art_wxWssKSUR45f
type: experiment
title: Do hub fields keep new concepts? Held-out test
summary: |-
  Sealed held-out test of H1 (does the adopting field's frozen 1998-2002 eigenvector gateway centrality predict retention of a newly adopted concept beyond B5, field size, phi(home,j), relatedness density, the field's leave-concept-out retention propensity P_j(-c), coverage and episode size?) and H3 (does gateway-weighted early landing G predict size-adjusted breadth O2r_resid given B5?).

  Data: one zero-credit scan of all 2,040 OpenAlex S3 works files (2026-09-23; 476,196,327 works; 129.4M base works 1995-2022), with Aho-Corasick title matching of 56,643 legacy concepts (levels 2-5) plus Wikidata aliases and stemmed verification: 60.0M verified matches. Grounding: legacy-tag rule TAG (test P 0.947, R 0.659), chosen on a 390-pair LLM benchmark with 60 hand-checked pairs (90% agreement), plus a per-concept LLM precision gate ($2.28 of OpenRouter).

  Authoritative S1 tables for iteration 3: frame_concepts.csv (12,499 concepts: DEV 4,771, held-out PHYS/LIFEENV/SOC/MATHDEC 742/1,113/1,352/165, cohort 4,356), episodes.csv (27,393 concept x off-home-field episodes with R and the R_abs1-3 sensitivity outcomes for all splits), concept_outcomes.csv (O1, O3, O2r_m30/m50) and concept_features_basic.csv (G, G_A, G_btw, REL_home, RS, DOM_*, count/label indicators, B5).

  The spec was frozen on DEV (sha256 in logs/seal.log) and unsealed once. H1: held-out dAUC -0.00001 [-0.0006, +0.0003] (DEV +0.00001), DL pooled -0.00004 (I2 = 0), cohort -0.0001. The placebo was not exceeded and the conditional logit is null. Verdict: DISCONFIRMED. Power: the minimum detectable dAUC is 0.004. The relatedness pair beats gateway on held-out (+0.0034 [0.0010, 0.0051] vs 0). The baseline ladder shows gateway's DEV signal (+0.0019 over the iteration-1 base) vanishes once P_j(-c) is added, and reverses on held-out (-0.0016). Gateway alone has AUC 0.605 on DEV vs 0.506 on held-out (0.41 in SOC): gateway is a domain-specific proxy for 'fields that keep things'. Iteration-1 replication: +0.023 (vs +0.10). H3: held-out partial rho G 0.030 / G_A 0.026 / G_btw 0.046 (Holm p = 0.0045); within-group DL pooled G 0.068 [0.029, 0.107]. The effect is small; the tests show 0/40 false positives on shuffled outcomes. REL_home is strongly negative (-0.14).

  An independent audit (sklearn, own AUC) matches to 1e-6. Deviations: no OpenAlex API audit or insularity (credits exhausted); LLM cap raised to $3.50; T3 t0 agreement 53%. See README.md, results/*.json and figures/.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md

--- Item 5 ---
id: art_N-mpomDZZ1ln
type: experiment
title: Where new scientific concepts spread next
summary: >-
  Full-corpus OpenAlex snapshot experiment (476M works, 0 API credits for data) on how 653 newborn concepts (legacy-concept
  lexicon, tag-AND-title grounding; benchmark precision 0.996, LLM+hand labelled, $0.007) enter new venue fields, using the
  frozen iteration-1 26-field PMI backbone. Dev = CS/Eng/BGM/Med homes, t0 2003-09 (274 concepts); held-out = other fields
  + 2010-14 cohort (369), run ONCE after a hashed freeze. H2 ENTRY (conditional logit on concept-year risk sets): relatedness
  to the off-home fields that currently RETAIN the concept predicts the next field entered beyond size, Hidalgo density, relatedness-to-home
  and own centrality: held-out LR 71.7 (p=2e-17), d=0.30 [0.24,0.37], positive in Physical/LifeEnv/Social/Cohort, DL pooled
  0.28 [0.22,0.35] I2=0, label-permutation p=0.001, rewired-backbone p=0.015 -> CONFIRMED by the frozen rule. BUT the gateway
  WEIGHTING adds nothing beyond plain retaining relatedness (M3 vs M1 g-only permutation p=0.17 held-out, 0.31 dev); target-field
  size is the strongest single block (AUC 0.76 vs density 0.59); incremental AUC only 0.809->0.817. ORDERING: first retained
  gateway field precedes the calibrated entropy take-off in 66% of broad concepts (sign p=0.003) vs 57% for peripheral fields
  (McNemar p=0.09) -> confirmed by rule, but the lead-lag gateway-permutation placebo (p=0.63) says the panel does not single
  out gateway fields. RESCUE (background-adjusted citation provenance, shared-author links removed; Hanski connectivity) and
  RELAY (availability-null) NOT supported on held-out; the iteration-1 gateway-retention lead did NOT replicate (coef ~0).
  TRAJECTORIES: DTW k-medoids k=2 stable (bootstrap ARI 1.0): volume-matched 'integrating' vs 'localized' classes (held-out
  independent recluster ARI 0.54; localized class dominated by Medicine homes). Independent audits: R1, p_gw and held-out
  AUCs reproduced exactly; exact-likelihood clogit gives LR 77.3, DL-pooled d 0.32 [0.25,0.39] (Breslow pipeline is conservative);
  within-stratum shuffled labels reject 0/20; random-year ordering placebo 0.43 << 0.66. Outputs: method_out.json (entry_events_dev/heldout
  with predict_M0 vs predict_M2 within-stratum probabilities; retention_episodes), results/*.json|csv (frame_concepts, episodes,
  dev/heldout results, frozen_spec, grounding report, deviations), figures/ (AUC forest, group forest, incidence curve, trajectory
  clusters, event studies, case field-flow plots). Caveats: 1,865 episodes (<4k target), MathDec untestable, sense filter
  uninformative, no Wikidata aliases.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md

--- Item 6 ---
id: art_lwI2DuRtQRZX
type: evaluation
title: Does the gateway-field retention signal replicate?
summary: >-
  Zero-API stress test of iteration-1's only live lead: the adopting field's gateway (eigenvector) centrality on the 1998-2002
  26-field PMI backbone (gateway_j) adding +0.103 AUC for field retention R (exp4, 80 episodes). Pre-registered verdict: FAILS.
  Reproduction: exp4's 0.10254 / 0.10222 reproduce exactly. Block A (LOGO logistic, concept-clustered REFIT bootstrap): delta-AUC
  over M2 (own field baseline + B5 + log field size + phi_home + density) is exp4 +0.037 [95% CI -0.018, 0.130], exp1 (s2-fos
  crosswalk, 367 rows) +0.001, exp3 (129) -0.006, union panel (362 de-duplicated episodes, 54 concepts) +0.001 [-0.012, 0.012],
  new-episodes-only panel (282) -0.001 [-0.021, 0.017]; the DL pooled value is +0.0015 (I2=0, descriptive). exp4's own M0
  lead keeps a refit CI of [0.010, 0.212], but the multi-feature iteration-1 rows lose significance. B1: gateway adds +0.0015
  over M2 + leave-concept-out field propensity P (union). B2: gateway explains 50% of exp4 field intercepts (p=0.14, 10 fields)
  and removes 74% of the field variance there, but R2=0.03 (p=0.55) and 2.5% on the union panel. B3: the time-varying backbone
  validates (rho 0.92) but is NOT IDENTIFIABLE (within/between SD 0.023). C2 node-label permutation: the union real value
  is at the 54th percentile; C1 rewiring discriminates (median rho 0.32): exp4 M0 at p=0.01, union not significant; no rival
  centrality (strength, degree, betweenness, PageRank, closeness, k-core, phi_min eigenvector, size) survives Holm correction.
  D: all 8 G-variant O1 gains (+0.05..+0.15) are label-coverage ARTEFACTS (G +0.072 -> +0.002). E: concept ICC 0.135; with
  a field random intercept the SD of delta-AUC under the alternative stays at ~0.015 whatever N is (1k-4k), an MDE floor of
  ~0.02 from having only 26 fields; ~34 held-out concepts per group give P(group delta>0)>=0.9 at a true delta of 0.05. F:
  corrected record tables (rho_B5, A*_h, exp3 portability, exp4 secondary screens, F5 refit CIs). Reusable output: results/union_episodes.csv
  (harmonised union panel). An independent audit (own solver) re-derives the headline deltas; a shuffled-R placebo on exp4's
  80 rows gives a 95th percentile of 0.130, above 0.103, so the original lead cannot be certified on 80 episodes. All tables
  are in eval_out.json metadata; the flat headline numbers are in metrics_agg.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
- reproducibility.md

--- Item 7 ---
id: art_O7Dq4L02QnDN
type: dataset
title: When research concepts were officially recognised
summary: |-
  External-recognition lookup table (outcome O5) for all 65,026 OpenAlex legacy concepts (64,723 target concepts at levels 2-5), built with zero OpenAlex credits and $1.49 of OpenRouter calls. Every event is dated and sourced, and carries year_usable, match_method, match_confidence and relation (same/narrower/broader, stated from the external entry's side). Present-day facts sit in a separate present_day block (year_known=false). sources_checked records found / not_found / not_applicable for each concept and source. There are no O5 flags and no t0 lags; the panel builder derives those.

  Sources: MeSH 2026 (20,872 concepts; DateIntroduced year; mesh_baseline flags years <=1966); English Wikipedia creation dates (6,540 exact first revisions with redirect-first repair; all other titles have a page-id estimate, 93% same calendar year in CV, and year_usable only for years that calibrate well); Wikidata P571/P575 (1,425 concepts); ACM CCS 1998/2012, MSC 2000/2010/2020 and PACS 2010/PhySH (taxonomy_in_version and taxonomy_added_between events); Nature Methods MoTY, Science BOTY, Physics World BOTY 2009-2025, MIT TR10, Gartner Hype Cycle 1995-2025 and Clarivate/CAS Research Fronts 2017-2025 (589 concepts); JEL as present-day membership only.

  Datasets (full_data_out/ parts): concept_recognition (65,026), external_entries_{mesh 31,830, acm_ccs 3,583, msc 17,872, pacs_physh 8,462, jel 1,015, curated_lists 2,666}, match_verifications (28,914 LLM judgements), crosswalk_level1_to_field (284) and spotcheck_p78 (78; 86% of the iteration-1 P78 concepts join). metadata_fold is a provisional dev/heldout/unassigned split from level-1 ancestors mapped to the OpenAlex fields and then to the hypothesis groups. It holds 19.6k/28.3k/17.1k concepts, and plurality group and share are included so the panel can apply S1's rule.

  Quality: all known-answer asserts pass (optogenetics NM 2010, iPSC NM 2009, CRISPR BOTY 2015, super-resolution NM 2008). Audit precision is 0.96 for label matches, 0.79 for ID links and 0.31 for alias-only matches, so alias matches were LLM-verified. Accepted LLM links are 0.97 precise on hand check. relation=same is reliable except for Research Fronts; narrower vs broader is only indicative. Inter-model kappa is 0.60 (accept/reject). Caveats: coverage is uneven (Social and Eng have no dated domain taxonomy, so use a Wikipedia/Wikidata-only O5 variant across groups), Wikipedia dates cluster in its 2001-2007 growth wave, and Research Fronts are citation-derived. See README.md, out/coverage_report.json and out/sources.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
- reproducibility.md

--- Item 8 ---
id: art_dxvRpQufMR0e
type: research
title: How our results compare with related papers
summary: |-
  Positioning study for the Applied Network Science (ANS) paper on emerging concepts. Deliverables: research_report.md (sections A-F) and raw evidence in raw/.
  (1) Collection: 'Networks for everyday life' cannot be read by any route (Springer IdP/JS, no Wayback snapshot). Only the scope text was recovered (societal domains: health, mobility, education, politics; rolling). The member list, editors and deadline are unknown, so do not claim topic overlap; argue fit through foresight/funding relevance and ANS method overlap.
  (2) 22 citable ANS papers with a 'how we relate' line each. The core set: Fontaine 2024 (AI into neuroscience), De Domenico 2016 (disciplines as sources/sinks), Holmgren 2023 (alluvial change), Gao 2018, Cunningham 2022, Larson 2017, Renoust 2017 (ANS 2:23). Plus about 40 neighbour-journal and preprint works.
  (3) Comparison numbers:
  - Guevara 2016 field-entry AUC: individuals 0.896, organisations 0.715, countries 0.682. Entry only, no exit. Our density AUC 0.61 < log-size 0.74: report density's increment over size.
  - Exit and survival evidence (Neffke 2011, Rigby 2015, Goya 2019) is regression-based and credits relatedness. No published retention AUC exists, so our +0.10 delta-AUC (0.705 -> 0.808, base rate 0.56) is an increment without a direct counterpart.
  - Link-forecast AUCs of 0.95-0.97 (Maillart 2606.03864; Gu & Krenn >0.9; Krenn positives about 1-3%) are level AUCs and not comparable.
  - Maillart 2606.03919 R2 0.60-0.87 are within-domain replications, not cross-field transfer.
  - Weng 2013: about 7x the precision of random guessing from the first 50 tweets (H3 precedent).
  (4) Novelty: adopter-centrality retention is NEW for concept adoption by fields but partially anticipated in general (Hidalgo 2007 position -> faster diversification; Yenilmez 2026 centrality explains diversification). The rescue/metapopulation analogy is partially anticipated in cultural evolution (Premo & Kuhn 2010; Premo 2012; Hopkinson 2011). Relay is partially anticipated (Weng 2013; Cheng 2023; Leydesdorff betweenness). Frame H1 as the first test in science, not a new principle. RISK: reviewers will want the adopter-portfolio relatedness-density rival.
  (5) ANS template, inferred from 8 articles from 2024-2026: unstructured abstract of 165-297 words; keywords optional; Introduction/Methods/Results/Discussion/Conclusions; back matter; author-year citations; 1-12 figures. Model wording for data availability and competing interests is included.
  (6) About 95 references verified; 12 corrections (Centola/Weng for complex contagion; Hidalgo/Neffke/Guevara for relatedness; Maillart authorship; Cunningham & Greene in PLoS ONE; wrong DOIs for Pinheiro, Yan, Kiss and Bettencourt fixed).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
- reproducibility.md
</supplementary_materials>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for judging whether the evidence recorded here actually supports what the run concluded, and whether a direction it abandoned was abandoned for a good reason.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<previous_review>
Your review from the previous iteration. Check which critiques the newest section
addressed. Do NOT re-raise critiques that have been adequately fixed. Only re-raise if the
fix is insufficient.

The previous review is BLOCKING: the paper must not ship as it stands. Every MUST-FIX item below is a requirement for this iteration, not a suggestion — an iteration that leaves one unaddressed does not publish.

- [MAJOR MUST-FIX] (evidence) A conclusion contradicts the artifact evidence. Sections 6.1 and 8 state that the B5 baseline 'achieves Spearman correlations of 0.77 to 0.83 with rarefied breadth' across all three experiments and that 'the ceiling for incremental gain is narrow'. Exp4 [art_33_KKk_G8Gw5] screen_result.json delta_rho_O2r_m30.base = 0.327 (n = 34; per group CS 0.10, Eng 0.86, BGM 0.65, Med 0.57). G's null therefore cannot be explained by a ceiling. The report also never gives Exp4's baseline rho at all.
  Action: Add a per-experiment line 'rho_B5 = 0.834 (Exp1, n = 48), 0.770 (Exp3, n = 47), 0.327 (Exp4, n = 34)'. Explain why Exp4's baseline is so much weaker: top-200-source truncation of 29/34 outcome windows, t0..t0+2 labels only, and a different O2r source. Rewrite the Section 8 ceiling argument so it applies only to Exp1 and Exp3.
- [MAJOR MUST-FIX] (evidence) Section 3.4 misreads numbers. 'The median A*_h in Medicine is +0.45 (naturalised), while in Computer Science it is -0.18 (borrowed).' These values are the within-group Spearman correlations of A*_h with O2r (Exp1 screen_result.json candidate_comparison_table.A_h.within_group_spearman_O2r: Med 0.446, CS -0.184). Median A*_h recomputed from results/features.csv is negative in every group: BGM -0.256, CS -0.303, Eng -0.041, Med -0.182. No group is 'naturalised' on average. The derived claim that 'A*_h is partly a field-composition indicator itself' does not follow from these numbers.
  Action: Correct in place with a marked correction. Report both the per-group medians of A*_h and the per-group Spearman with O2r. The finding that survives is that the direction of association flips (positive in Med, negative in CS and BGM), not that the level flips.
- [MAJOR MUST-FIX] (scope) Two executed but failed artifacts are missing from the record. The iteration-1 strategy (gen_strat_1) commissioned five artifacts: gen_art_dataset_1 (outcome-blind held-out Frame-N concepts plus a 500-pair grounding benchmark) and gen_art_experiment_2 (candidate S: unconnected co-author groups U, Cheng et al. 2023) did not complete. Both .aii_worker_result.json files read failed = true, 'REPL turn stalled (no new JSONL records for ~1993s)'. The report numbers its experiments 1, 3, 4 with no explanation, never mentions candidate S, and never says the held-out test set does not exist. Every result is therefore dev-panel only, which the user's request (step 3/5: reserve held-out fields or concepts) explicitly warns against.
  Action: Add a 'Failed artifacts' subsection. Name both artifacts, their purpose, the failure message and its consequences: no held-out evaluation, and candidate S (the Cheng et al. co-authorship hypothesis) untested. List both under Dead ends as 'not run, not refuted'. Carry the held-out dataset forward as the top priority for iteration 2.
- [MAJOR MUST-FIX] (methodology) The 'shared protocol' is not shared in practice, so the cross-experiment table in 6.2 is not like-for-like. Each experiment computes its own O2r and home field: Exp1 from Semantic Scholar s2-fos labels, Exp3 from title-matched snapshot venue fields, Exp4 from API top-200 sources. Across experiments, O2r agrees at Spearman 0.764 (Exp1 vs Exp3, n = 41), 0.790 (Exp1 vs Exp4, n = 30) and 0.803 (Exp3 vs Exp4, n = 33). 8 of the 41 concepts shared by Exp1 and Exp3 are assigned a different home group, so the LOGO folds differ. The report cites only the 0.87 agreement on 11 concepts, and says Exp4 produced the 'authoritative' outcomes, which Exp1 and Exp3 did not use.
  Action: State explicitly which outcomes.csv each screen used. Add the cross-experiment O2r agreement matrix and the home-group crosstab. Either re-run all three screens on one common outcome table and fold assignment (cheap: the features exist, and it is ridge on fewer than 50 rows), or caption 6.2 as not directly comparable.
- [MAJOR MUST-FIX] (evidence) Exp3's full indicator table is missing. [art_yrradSC27HtQ] screen_result.json.portability holds 34 indicators, each with pooled rho, within-group rho for all four groups, size correlations and LOGO delta-rho. That is the RQ1 deliverable the user asked for (30-50 indicators, portability across domains, domain-specific failures reported). The report shows about 9. It omits a portable NEGATIVE signal, edge_persistence (within-group -0.34, -0.52, -0.07, -0.22), and several size-confounded indicators (M rho_vol 0.80, btw_t4 0.79, constraint_t4 -0.78). The claim that D_ratio, D_rare, participation and NOV_res are 'in the range 0.45 to 0.63 across all four groups' is wrong: those are pooled values, and the within-group minima are 0.33 (D_ratio, Eng), 0.47 (D_rare, Eng), 0.12 (participation, CS) and 0.27 (NOV_res, CS). new_edge_rate is 0.35 in Med, not 'near zero or negative'.
  Action: Paste the 34-row portability table: pooled rho, four within-group rhos, rho_logvol, rho_growth, LOGO delta-rho, CS-only flag. Correct the 4.3 wording to 'pooled rho 0.45-0.63; within-group rho positive in all four groups, ranging 0.12-0.68'.
- [MAJOR MUST-FIX] (rigor) Section 8 overclaims the exploratory partial association. It says 'The signal is real but absorbed' for D_ratio. exploratory_partial_association.json tests 12 indicators, and only D_ratio's CI90 excludes zero ([0.019, 0.648]). Its CI95 is [-0.059, 0.688], and it is negative in Eng (-0.067). The permutation p = 0.037 (one-sided, 1,000 permutations) appears only in the artifact README and reproducibility.md, in no result file, and the artifact's own text calls it 'marginal'. With 12 tests, a lone p = 0.037 does not survive any multiplicity correction. The report also lists only 5 of the 12 partials.
  Action: Report all 12 partials with CI90 and CI95. Write the permutation null into a JSON output and cite it. Relabel the finding 'marginal, uncorrected, 1 of 12' and remove 'real' from Section 8.
- [MAJOR MUST-FIX] (evidence) The Exp4 secondary-variant screen is omitted, and a claim in 5.3 is contradicted by it. screen_result.json.secondary_screens reports O1 dAUC for G_deg +0.149 [0.053, 0.266] (3/4 groups), G_phimin +0.154 [0.058, 0.272], REL_home +0.121 [0.033, 0.229], G_all +0.112, G_A +0.075. All exceed G's +0.072, whose CI90 lower bound is exactly 0.000 and whose CI95 is [-0.011, 0.187], so 'strongest secondary signal in the iteration' is false. The same table has variants that significantly HURT O2r: G_all -0.240 [-0.419, -0.087] and DOM_Physical -0.110 [-0.193, -0.037]. A dead end with evidence has vanished. The consistent O1 gains across nearly every G variant also call for a check that they are not a shared artefact (for example label coverage or O1 base rate 33/46).
  Action: Add the full secondary_screens table (variant × {O2r, O1} with CI90 and groups positive). Delete the 'strongest' claim. Record G_all and DOM_Physical as negative results. Test whether the O1 gains persist when label_coverage_early is added to B5.
- [MAJOR MUST-FIX] (rigor) The reported CIs are the narrow fixed-prediction bootstrap, and the wider refit bootstrap is not reported. The report says '2,000 stratified concept-level bootstraps'. In Exp4 screen.py paired_delta, the 2,000 draws resample fixed OOF predictions without stratification. Only the 200-draw refit bootstrap is stratified, and it is much wider: Exp1 A*_h refit CI90 [-0.092, 0.023] vs reported [-0.034, 0.017]; Exp4 G refit CI90 [-0.196, 0.295] vs reported [-0.095, 0.168]. This matters most for the positive claims, such as Exp4 O2r_resid +0.150 with CI90 lower bound 0.0003.
  Action: Describe the bootstrap exactly per artifact. Report the refit CI alongside each headline delta. Recompute the refit CI for O2r_resid and for field-level gateway_j before carrying either forward as a 'finding'.
- [MAJOR MUST-FIX] (evidence) Exp1 robustness checks that went against the primary are omitted. screen_result.json.glmm_check shows the one-stage GLMM estimate of A*_h correlates only 0.163 with the primary estimator. Only the PyMC check (a re-fit of the same two-stage model, 0.9996) is reported. The agreement block shows the new A*_h correlates 0.10 with the probe's A*_h (crowdsourcing and iPSC flip sign), yet Section 3.2 says the result was 'predicted by the 8-concept probe'. The refit bootstrap and five sensitivities (newborn_only, full_parent_sample, O2r_m50, O2r_m20, B5+offhome) are absent. The field-level with_data_only result (186 units: dAUC -0.010) is absent, even though 181 of the 367 units have no lineage data. The reliability of 0.58 was not independently re-derived (artifact summary), and the report does not say so.
  Action: Add a 'robustness' table for Exp1 covering the GLMM agreement, probe agreement, refit CI, all five sensitivities and the field-level with-data-only result. Note that r_SB = 0.58 is unaudited.
- [MAJOR MUST-FIX] (scope) Coverage of the original request is partial. RQ1 is addressed only on a dev panel, with no held-out fields, time windows or concept groups. The 'about 10 strongest indicators on held-out data' step, external ground truth (reviews, curated emerging-topic lists), the exploratory AI-first stage, and the optional learned model are all missing. RQ2 (empirically derived diffusion trajectories, temporal sequences such as 'central in home community first, then diffuse') is not touched, although the per-year data needed for it already exists in Exp3's ego networks. The 'explain why the strongest indicator works' analysis and case studies are also absent.
  Action: Add a coverage table mapping each RQ and execution step of the request to done / partial / not started, with the artifact that addresses it. Use it to justify iteration-2 priorities: build the held-out set, then run RQ2 trajectory clustering on Exp3's yearly ego-network features for the 47 concepts. Both need no new OpenAlex credits.
- [MAJOR MUST-FIX] (methodology) The iteration spent its budget adding candidate METRICS to a panel the run's own power analysis shows cannot detect the effect. Exp1's positive-control ladder shows that a feature with rho 0.83 with O2r gains only +0.068 over B5, and one needs rho of about 0.95 to pass. Exp4 has n = 34 with 7-10 concepts per LOGO group. Iteration 2 proposes ensembles and interactions of the same indicators on the same 46-48 concepts, which the record already shows cannot pass the rule.
  Action: Record the power analysis as a finding that constrains the next step. Either change the primary question to one the panel can answer (for example partial association with a pre-specified multiplicity correction, or residualised O2r as the primary), or put the budget into more concepts: the failed held-out set, plus a larger panel from the free S3 snapshot that Exp3 already scans at zero credits. Do not add further metrics.
- [MAJOR MUST-FIX] (novelty) The positive claims are not compared with their nearest published neighbours. (a) The field-level gateway result (the adopting field's centrality predicts retention) sits next to the principle of relatedness and the 'research space' (Guevara et al. 2016, Scientometrics 109:1695), which already shows that a field-relatedness map predicts which fields actors enter. The report's own 5.5 finds relatedness density loses to field size. (b) The D_ratio partial association is the scholarly analogue of Weng et al. 2013 (community diversity predicts virality). (c) The background-homophily result neighbours Ciotti et al. 2016 on citation homophily and field-normalised mixing. (d) Maillart et al. 2026 (arXiv:2606.03919, cited as [7]) already report that 'exogenous diffusion and entropy are strongly predictable'. That is close to this run's finding that entropy alone (rho 0.70) does most of B5's work. None of these comparisons is written down.
  Action: For each of the three 'what worked' items in 6.3, add one line: nearest neighbour, what it showed, and what this run adds (for example retention rather than entry, and conditioning on B5 and field size). Add Guevara et al. 2016 and Hidalgo et al. 2018 to the references.
- [MAJOR MUST-FIX] (clarity) The reasoning for iteration 1 is only partly recorded. The report never says what the preceding hypothesis-stage review objected to: gen_strat_1 says that review computed a reliability of about 0.32 for A*_h from the probe, which motivated the field-stratified, partially pooled redesign and the reliability gate. It never says why five artifacts were commissioned, or why D_z was replaced (the fallback is described, but it is not stated that it was declared before outcomes were inspected). It also does not state that Exp3's gamma rule was redefined 'before any outcome was inspected' (deviations.json GAMMA_RULE).
  Action: Add to Section 1 a short 'Why this iteration' paragraph: the prior review's objections, the five-artifact wide-screen design, and which choices were pre-declared versus post hoc (D_ratio fallback, gamma ≥ 20 communities, SELF_TOPIC lexical rule), citing deviations.json.
- [MINOR] (rigor) Some numbers are untraceable or mislabelled. The next-field entry numbers (AUC 0.61 [0.55, 0.67], permutation p = 0.023, size AUC 0.74, conditional-logit β = 0.42) appear only in the Exp4 README table. No result file holds them; next_field_entry.csv has only the inputs. The Exp4 field-level row 'B5 + all_four (G, REL, RS, G_all)' carries the size_controlled_all_three numbers (0.697, 0.782, +0.085); all_four_available is 0.705 → 0.787, +0.082 [0.008, 0.153]. The M1 R² (0.66) is computed on raw_LOR_sampled; on the unthinned raw_LOR it is 0.72 (Spearman 0.76, 81% bg ≥ raw), which strengthens the claim but is not recorded.
  Action: Have next_field.py write next_field_result.json and cite it. Fix the table row label. Say which raw-LOR version M1 uses and report both values.
- [MINOR] (evidence) Section 3.9 misreads the placebo. 'A shuffled-A*_h placebo passes 0 of 200 times, confirming that the null result is not an artefact of the evaluation protocol.' A placebo that never passes shows the rule does not produce false positives. It says nothing about false negatives. The positive-control ladder (rho 0.83 feature → delta 0.068, fails) shows the protocol is very insensitive, and the leaky positive control also fails the delta clause.
  Action: Rephrase: the placebo bounds false positives, and the positive-control ladder shows low sensitivity. Include the ladder table from audit/rederive_out.json.
</previous_review>

<task>
Audit this research record. It is an internal report, not a paper: chronological, one
section per iteration, complete. Judge it on completeness, traceability and what it says
was learned — never on framing, section order or polish. When it claims a positive result,
novelty is evidence, not framing: check it against the nearest published neighbour (STEP 5),
not against how well the paper will read.

STEP 1 — READ THE REPORT: Read it carefully. Note what each iteration claims it did, found
and concluded.

STEP 2 — WALK THE ARTIFACTS: Go through the supplementary materials one artifact at a time
and find where the report reports it. Open the output files. Every executed artifact must
appear, and every table in those files must be in the report with its actual numbers. List
the misses; each one is a major issue.

STEP 3 — TRACE THE NUMBERS: For each number, table and claim in the report, find the
artifact it came from, and RECOMPUTE the headline number(s) yourself from that artifact's
own tables or result files rather than taking the report's figure on trust. Report any
mismatch as a finding, even when the underlying artifact is real. Where an artifact does
not let you recompute a number — the raw output is missing, or the computation cannot be
reproduced from what is there — say so and treat that claim as unverified rather than
accepted. An [ARTIFACT:id] marker or a named output file makes a number traceable; nothing
makes it untraceable, which is a major issue even when the number is right.

STEP 4 — CHECK COVERAGE AGAINST THE ORIGINAL REQUEST: The user's original request that
started this run is supplied as a separate message in this turn. Read it and ask what it
actually asked for. Is the run answering THAT, or a question next to it? Set `coverage`
to "full", "partial" or "lost", and when it is not "full", raise a critique naming the
part of the request that went unanswered. Judge against the request, not against the
report's own framing of it — a run that narrows one defensible step per iteration ends up
answering something nobody asked, and each step looked fine on its own.

STEP 5 — CHECK THE RECORD HOLDS TOGETHER:
- Is the REASONING written down at every step — why this strategy, why these artifacts,
  what the last review objected to, what the hypothesis revision concluded and why it moved?
  Outcomes with no account of why they were sought is a major issue.
- Are DEAD ENDS kept and labelled, with the evidence that killed them? A direction the
  artifacts show was tried and the report does not mention is a major issue.
- Is the CHRONOLOGY intact — one section per iteration, in order, earlier sections
  unchanged except where a correction is marked in place? A silently rewritten earlier
  section destroys the record.
- Are the numbers from artifacts that ACTUALLY RAN? Trace each one to an executed output. A
  projected, expected, illustrative or placeholder number presented as a result means
  `results_reported` is false.
- Is what the report concludes PROPORTIONATE to what it recorded? A tiny effect, or an
  effect in the direction everyone already expected, written up as the answer is either
  explained (a bound someone needed, a belief it overturns, a mechanism only visible at
  that size) or it overreaches, and you say so.
- When the report claims a POSITIVE, non-obvious result, name the nearest published result
  that already answers something close to it, and state what this iteration adds beyond
  that neighbour. A positive result earns no credit for novelty in this record until that
  comparison is made — its absence is a critique under `novelty`, not a paper-framing note.
- Does anything the report concludes CONTRADICT its own evidence — a table, a figure, a
  log, an artifact summary? Name the contradiction.
- A conclusion that contradicts the run's own evidence scores soundness 1.
- Set `blocking` by rule: true exactly when the soundness score is 1 or lower OR
  `results_reported` is false; otherwise false.

STEP 6 — WRITE YOUR REVIEW:
For each critique:
1. Categorize: methodology, evidence, novelty, clarity, scope, or rigor
2. Rate severity: major (the record is incomplete or untraceable) or minor (polish)
3. Describe the issue clearly, naming the artifact or section it is about
4. Suggest a concrete action to address it

Focus on the most impactful issues. Provide your review via structured output.
</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/user_uploads`. Check this folder for anything relevant to your task. It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you.
</user_data>

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
    "Critique": {
      "description": "A single actionable critique from the reviewer.",
      "properties": {
        "category": {
          "description": "Category: 'methodology', 'evidence', 'novelty', 'clarity', 'scope', or 'rigor'",
          "title": "Category",
          "type": "string"
        },
        "severity": {
          "description": "Severity: 'major' or 'minor'",
          "title": "Severity",
          "type": "string"
        },
        "description": {
          "description": "Clear description of the issue",
          "title": "Description",
          "type": "string"
        },
        "suggested_action": {
          "description": "Concrete suggestion for how to address this critique",
          "title": "Suggested Action",
          "type": "string"
        }
      },
      "required": [
        "category",
        "severity",
        "description",
        "suggested_action"
      ],
      "title": "Critique",
      "type": "object"
    },
    "DimensionScore": {
      "description": "Score for a single review dimension with improvement suggestions.",
      "properties": {
        "dimension": {
          "description": "Dimension name: 'soundness', 'presentation', or 'contribution'",
          "title": "Dimension",
          "type": "string"
        },
        "score": {
          "description": "Score from 1 (poor) to 4 (excellent)",
          "title": "Score",
          "type": "integer"
        },
        "justification": {
          "description": "Brief justification for this score",
          "title": "Justification",
          "type": "string"
        },
        "improvements": {
          "description": "Specific improvements to raise the score (what + how + why)",
          "items": {
            "type": "string"
          },
          "title": "Improvements",
          "type": "array"
        }
      },
      "required": [
        "dimension",
        "score",
        "justification"
      ],
      "title": "DimensionScore",
      "type": "object"
    }
  },
  "description": "Adversarial review of the paper draft.\n\nID format: review_it{iteration}__{model}",
  "properties": {
    "overall_assessment": {
      "description": "Overall assessment of the paper's quality and readiness",
      "title": "Overall Assessment",
      "type": "string"
    },
    "strengths": {
      "description": "Key strengths of the paper",
      "items": {
        "type": "string"
      },
      "title": "Strengths",
      "type": "array"
    },
    "dimension_scores": {
      "description": "Scores (1-4) for: soundness, presentation, contribution",
      "items": {
        "$ref": "#/$defs/DimensionScore"
      },
      "title": "Dimension Scores",
      "type": "array"
    },
    "critiques": {
      "description": "Actionable critiques \u2014 specific issues with concrete suggestions",
      "items": {
        "$ref": "#/$defs/Critique"
      },
      "title": "Critiques",
      "type": "array"
    },
    "results_reported": {
      "description": "True only when the paper's headline numbers come from an artifact that was EXECUTED \u2014 a run that finished and wrote its output \u2014 AND you RECOMPUTED the headline number(s) yourself from that artifact's own tables or result files rather than accepting the write-up's figure. A mismatch between what you recompute and what is reported is a critique in its own right, even when the artifact is real. False when any headline number is projected, expected, illustrative, a placeholder, produced by a run that errored, was truncated, never ran, or when you could not recompute it \u2014 say so in `overall_assessment` and treat that claim as unverified rather than accepted.",
      "title": "Results Reported",
      "type": "boolean"
    },
    "coverage": {
      "default": "partial",
      "description": "How much of the USER'S ORIGINAL request this paper answers: 'full' \u2014 it answers the request; 'partial' \u2014 it answers a recognisable piece of it; 'lost' \u2014 the paper answers a different question than the one asked.",
      "enum": [
        "full",
        "partial",
        "lost"
      ],
      "title": "Coverage",
      "type": "string"
    },
    "blocking": {
      "description": "True when this paper must not ship as it stands. It is DERIVED, not judged: true exactly when the soundness dimension score is 1 or lower OR results_reported is false; otherwise false. A headline claim that contradicts the run's own evidence scores soundness 1. A value that disagrees with this rule is sent back.",
      "title": "Blocking",
      "type": "boolean"
    },
    "score": {
      "description": "Overall quality score from 1 (very strong reject) to 10 (award quality)",
      "title": "Score",
      "type": "integer"
    },
    "confidence": {
      "default": 3,
      "description": "Confidence in assessment from 1 (educated guess) to 5 (absolutely certain)",
      "title": "Confidence",
      "type": "integer"
    }
  },
  "required": [
    "overall_assessment",
    "strengths",
    "critiques",
    "results_reported",
    "blocking",
    "score"
  ],
  "title": "ReviewerFeedback",
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

### [3] ASSISTANT · 2026-09-28 20:55:49 UTC

```
I'll audit the report against the artifacts. First I'll look at the workspace and the artifact outputs.
```

### [4] TOOL CALL — Bash · 2026-09-28 20:55:49 UTC

```
List workspace and iteration-2 artifact directories:
ls -la . .aii 2>/dev/null; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/; for d in /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/*/; do echo "== $d"; ls $d; ls $d/results 2>/dev/null | head -50; done
```

### [5] TOOL RESULT — Bash · 2026-09-28 20:55:49 UTC

```
{"stdout": ".:\ntotal 1997\ndrwxr-xr-x 3 root root 1003508 Sep 28 20:55 .\ndrwxr-xr-x 3 root root 1003508 Sep 28 20:55 ..\ndrwxr-xr-x 2 root root       1 Sep 28 20:55 .aii\n-rw------- 1 root root      54 Sep 28 20:55 .aii_claude_session.json\n-rw-r--r-- 1 root root   35870 Sep 28 20:55 .repl_agent.ptylog\n\n.aii:\ntotal 981\ndrwxr-xr-x 2 root root       1 Sep 28 20:55 .\ndrwxr-xr-x 3 root root 1003508 Sep 28 20:55 ..\ngen_art_dataset_2\ngen_art_evaluation_1\ngen_art_experiment_5\ngen_art_experiment_6\ngen_art_research_1\n== /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/\nREADME.md\ncache\ndata.py\nfull_data_out\nlogs\nmini_data_out.json\nout\npreview_data_out.json\npyproject.toml\nreproducibility.md\nrestore.sh\nrun_all.sh\nscripts\ntemp\nwork\n== /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/\nREADME.md\n__pycache__\naudit.py\neval.py\neval_out.json\nfigures\nfull_eval_out.json\nharmonise.py\nlib.py\nlogs\nmini_eval_out.json\nprereg\npreview_eval_out.json\npyproject.toml\nreproducibility.md\nresults\naudit_out.json\ncache\nsummary.json\nunion_episodes.csv\n== /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/\nREADME.md\n__pycache__\naudit.json\naudit.py\naudit_placebo.py\nbackbones.py\nchecks.py\ncohort_episodes_with_pred.csv\ncommon.py\nconcept_features_basic.csv\nconcept_outcomes.csv\ncredits_log.csv\ndev_episodes_with_oof.csv\nepisode_features.csv\nepisodes.csv\nexploratory_domains.py\nfeatures.py\nfigures\nfix_pigeonhole.py\nframe.py\nframe_concepts.csv\nfrozen_lexicon.sha256\nfrozen_spec.json\nfull_method_out.json\ngrounding.py\ngrounding_benchmark.csv\ngrounding_precision.csv\ngrounding_report.json\nheldout_episodes_with_pred.csv\nlexicon.py\nlexicon_v0.parquet\nlexicon_v1.parquet\nllm.py\nllm_cost_log.csv\nlogs\nmake_variants.py\nmatcher.py\nmethod.py\nmethod_out.json\nmini_method_out.json\nmodels.py\noa_client.py\npanel.py\nplacebo_gateways.npy\nplacebo_perm_gateways.npy\nprescreen.py\npreview_method_out.json\nprobe.py\npyproject.toml\nrangefile.py\nreport.py\nreproducibility.md\nrestore.sh\nresults\nscan\nscan_full.py\nseal.py\nsens_episodes_b5_t0p4.csv\nsens_episodes_match.csv\nsens_episodes_ptopic.csv\nsense_filter.joblib\nsnapshot\ntests\ntiming_probe.py\nwikidata_aliases.py\naudit_placebo.json\nbackbones.json\nchecks.json\ndeviations.json\nexploratory_domain_specificity.json\nframe_build_em30_w1.json\nframe_summary.json\ngrounding_bench_summary.json\nh1_dev.json\nh1_dev_smoke.json\nh1_heldout.json\nh1_heldout_smoke.json\nh3_results.json\nhandcheck_labels.csv\nhandcheck_sheet.csv\nlexicon_v0_summary.json\nonset_candidates_grounded.csv\nonset_candidates_match.csv\np78_agreement.csv\nprescreen_dropped.csv\nprescreen_summary.json\nsource_field.parquet\nunit_tests_T0.json\n== /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/\nREADME.md\naggregate.py\nagreement.py\naudit.py\naudit_api.py\naudit_placebo.py\nbenchmark\nbuild_lexicon.py\ncand.py\nconfig.py\nfigures\nframe.py\nfull_method_out.json\ngrounding.py\ninputs\ninstall.sh\nlabel_bench.py\nlib\nlogs\nmake_outputs.py\nmethod.py\nmethod_out.json\nmini_method_out.json\npass1.py\npass2.py\npreview_method_out.json\npyproject.toml\nreproducibility.md\nrequirements.lock.txt\nresults\nscan\ntests\nagreement.json\napi_audit.csv\napi_audit.json\naudit.json\naudit_placebo.json\ncandidates.csv\ncandidates_summary.json\ncluster_assign_dev.csv\ncluster_assign_heldout.csv\ncredits_log.csv\ndev_result.json\ndev_spec_parts.json\ndeviations.json\nentry_risk_sets_dev.parquet\nentry_risk_sets_heldout.parquet\nepisodes.csv\nframe_concepts.csv\nframe_summary.json\nfreeze_log.txt\nfrozen_spec.json\ngrounding_concepts.csv\ngrounding_report.json\nheldout_result.json\nlexicon.parquet\nlexicon_dropped.csv\nlexicon_hash.txt\nlexicon_summary.json\nopenrouter_cost.json\nordering_dev.csv\nordering_heldout.csv\np0_dropped.csv\nrelay_dev.csv\nrelay_heldout.csv\nrescue_dev.csv\nrescue_heldout.csv\nsense_filter.pkl\ntrajectories_dev.csv\ntrajectories_heldout.csv\nunit_tests_T0.json\nworks_schema.json\n== /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_research_1/\nREADME.md\nraw\nreproducibility.md\nresearch_out.json\nresearch_report.md\nresearch_verification.json\nscripts", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [6] TOOL CALL — Bash · 2026-09-28 20:55:53 UTC

```
Dump Experiment 5 result JSON heads:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results; python3 -c "
import json
for f in ['h1_heldout.json','h1_dev.json','h3_results.json','frame_summary.json','checks.json','deviations.json','audit_placebo.json','exploratory_domain_specificity.json']:
    d=json.load(open(f)); s=json.dumps(d)
    print('=====',f,len(s)); print(s[:3500])
"
```

### [7] TOOL RESULT — Bash · 2026-09-28 20:55:53 UTC

```
{"stdout": "===== h1_heldout.json 22538\n{\"spec_sha256\": \"147ce58a4052eaae6dfb77c465ae7a86ef3d742749a4babc1ffd06ab42d33293\", \"n_dev\": 9079, \"n_heldout\": 8515, \"n_cohort\": 9798, \"n_R_undefined_excluded\": {\"COHORT\": 1}, \"primary\": {\"n\": 8515, \"n_concepts\": 3085, \"R_rate\": 0.3058132706987669, \"auc_X0\": 0.8372646639437369, \"auc_X1\": 0.8372556983893966, \"dauc\": -8.9655543402678e-06, \"per_group\": {\"PHYS\": {\"n\": 1662, \"n_concepts\": 642, \"auc_X0\": 0.8622865099419227, \"auc_X1\": 0.8627842675521571, \"dauc\": 0.0004977576102344061, \"boot_se\": 0.0006127474871689199, \"boot_ci95\": [-0.0008215807441025069, 0.001701825176778286]}, \"LIFEENV\": {\"n\": 3099, \"n_concepts\": 1060, \"auc_X0\": 0.842959703566466, \"auc_X1\": 0.842703970514324, \"dauc\": -0.00025573305214199316, \"boot_se\": 0.00041771900184160336, \"boot_ci95\": [-0.001319236902137025, 0.0003100672477152758]}, \"SOC\": {\"n\": 3320, \"n_concepts\": 1233, \"auc_X0\": 0.8080540128036631, \"auc_X1\": 0.8079327595709502, \"dauc\": -0.00012125323271283683, \"boot_se\": 0.0002527552248880474, \"boot_ci95\": [-0.0007616475503815334, 0.00023531066208688203]}, \"MATHDEC\": {\"n\": 434, \"n_concepts\": 150, \"auc_X0\": 0.9175295857988166, \"auc_X1\": 0.9180535009861933, \"dauc\": 0.0005239151873767112, \"boot_se\": 0.0007612520840218499, \"boot_ci95\": [-0.00132796159832676, 0.0018212873714255628]}}, \"boot_ci95\": [-0.0006173982106458864, 0.00033315644834805376], \"boot_p_le0\": 0.568}, \"dl_pool\": {\"k\": 4, \"pooled\": -4.3991314466003225e-05, \"se\": 0.00019697749811468297, \"ci95\": [-0.0004300672107707818, 0.0003420845818387754], \"tau2\": 0.0, \"I2\": 0.0, \"Q\": 1.6886147538161116}, \"evaluable_groups\": [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"], \"sign_test_groups\": {\"n\": 4, \"n_positive\": 2, \"p_one_sided\": 0.6875}, \"cohort\": {\"n\": 9798, \"n_concepts\": 3843, \"R_rate\": 0.26546233925290874, \"auc_X0\": 0.8559328593757588, \"auc_X1\": 0.8557844571595976, \"dauc\": -0.00014840221616119198, \"per_group\": {\"BGM\": {\"n\": 622, \"n_concepts\": 221, \"auc_X0\": 0.8873167975461539, \"auc_X1\": 0.8870631104346121, \"dauc\": -0.00025368711154183377, \"boot_se\": 0.0008370045935318521, \"boot_ci95\": [-0.0023825991991262506, 0.0012169553988746998]}, \"CS\": {\"n\": 534, \"n_concepts\": 197, \"auc_X0\": 0.8341206536048943, \"auc_X1\": 0.8347401843103849, \"dauc\": 0.0006195307054905896, \"boot_se\": 0.0007087487833716178, \"boot_ci95\": [-0.0005658696138598485, 0.0021305816227387008]}, \"Eng\": {\"n\": 1680, \"n_concepts\": 659, \"auc_X0\": 0.8616677338324386, \"auc_X1\": 0.8619494655962172, \"dauc\": 0.0002817317637786587, \"boot_se\": 0.0006480038088431565, \"boot_ci95\": [-0.0013645913086587302, 0.00135350670672707]}, \"LIFEENV\": {\"n\": 1548, \"n_concepts\": 537, \"auc_X0\": 0.8404253126524333, \"auc_X1\": 0.8406497399620307, \"dauc\": 0.0002244273095974858, \"boot_se\": 0.0005086426380995615, \"boot_ci95\": [-0.0009896669146691461, 0.0011232558858107991]}, \"MATHDEC\": {\"n\": 216, \"n_concepts\": 92, \"auc_X0\": 0.7996512641673932, \"auc_X1\": 0.8003487358326068, \"dauc\": 0.0006974716652136115, \"boot_se\": 0.0021066048109364176, \"boot_ci95\": [-0.005691183413366199, 0.002938847207591231]}, \"Med\": {\"n\": 2267, \"n_concepts\": 1038, \"auc_X0\": 0.8651989706251569, \"auc_X1\": 0.8653213658046699, \"dauc\": 0.00012239517951295742, \"boot_se\": 0.00036589695423397666, \"boot_ci95\": [-0.0006325434806103203, 0.0009480077977083917]}, \"PHYS\": {\"n\": 863, \"n_concepts\": 310, \"auc_X0\": 0.8723349236517849, \"auc_X1\": 0.8714880467527766, \"dauc\": -0.0008468768990083086, \"boot_se\": 0.0009394206102585958, \"boot_ci95\": [-0.0031797173605917274, 0.0003919115965475352]}, \"SOC\": {\"n\": 2068, \"n_concepts\": 789, \"auc_X0\": 0.83723942\n===== h1_dev.json 16229\n{\"n_episodes\": 9079, \"n_concepts\": 3987, \"R_rate\": 0.29364467452362597, \"by_group\": {\"BGM\": {\"n\": 1270, \"R\": 0.36299212598425196, \"concepts\": 466}, \"CS\": {\"n\": 861, \"R\": 0.3600464576074332, \"concepts\": 357}, \"Eng\": {\"n\": 3051, \"R\": 0.28482464765650606, \"concepts\": 1200}, \"Med\": {\"n\": 3897, \"R\": 0.2632794457274827, \"concepts\": 1964}}, \"primary\": {\"auc_X0\": 0.8657544473440986, \"auc_X1\": 0.8657681339093544, \"dauc\": 1.3686565255799366e-05, \"per_group\": {\"CS\": {\"auc_X0\": 0.868309817926351, \"auc_X1\": 0.8683332357590305, \"dauc\": 2.341783267956199e-05, \"n\": 861, \"boot_se\": 0.0002964206747531905}, \"Eng\": {\"auc_X0\": 0.8632112935736368, \"auc_X1\": 0.863304640225129, \"dauc\": 9.334665149218768e-05, \"n\": 3051, \"boot_se\": 0.0005057632097695673}, \"BGM\": {\"auc_X0\": 0.8842495890859073, \"auc_X1\": 0.8843514796929338, \"dauc\": 0.00010189060702647801, \"n\": 1270, \"boot_se\": 0.00048452945059428447}, \"Med\": {\"auc_X0\": 0.8583152897530795, \"auc_X1\": 0.8582602933278474, \"dauc\": -5.499642523210113e-05, \"n\": 3897, \"boot_se\": 0.0004958048721347913}}, \"boot_ci95\": [-0.0007070657674354858, 0.0004759588102118098], \"boot_sd\": 0.0002801512968727787, \"boot_p_le0\": 0.631, \"dl_pool_groups\": {\"k\": 4, \"pooled\": 3.5639279200013704e-05, \"se\": 0.0002057686649512798, \"ci95\": [-0.0003676673041044947, 0.0004389458625045221], \"tau2\": 0.0, \"I2\": 0.0, \"Q\": 0.06683237721965415}}, \"T5_seed_stability\": {\"ci_seed1_500\": [-0.0006645566569091627, 0.0004211635345695987], \"ci_seed2_500\": [-0.0006704466054427899, 0.000489658161158668], \"max_abs_diff\": 6.849462658906931e-05}, \"rival_head_to_head\": {\"dauc_relatedness_pair\": -0.00017470842059497116, \"dauc_gateway\": -0.000142246695308601, \"diff_gateway_minus_relatedness\": 3.246172528637015e-05, \"diff_boot_ci95\": [-0.0015783023924223231, 0.0016099151945286989], \"relatedness_boot_ci95\": [-0.0017096415625327736, 0.0011992251564341885], \"gateway_boot_ci95\": [-0.000927531192910283, 0.00027783484949635273]}, \"ladder\": {\"L1_iter1_base\": {\"cols\": [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"log_n_early\", \"share_early\", \"growth_j\", \"log_field_size\"], \"auc_base\": 0.8554726199092265, \"dauc\": 0.0019460073189199179, \"ci95\": [0.00046512967459460267, 0.0033622151752069505]}, \"L2_plus_relatedness\": {\"cols\": [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"log_n_early\", \"share_early\", \"growth_j\", \"log_field_size\", \"phi_home\", \"density\"], \"auc_base\": 0.8528314637524187, \"dauc\": 0.0006932771708442198, \"ci95\": [-0.0007786918721284535, 0.0021721054125857977]}, \"L3_plus_Pj\": {\"cols\": [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"log_n_early\", \"share_early\", \"growth_j\", \"log_field_size\", \"phi_home\", \"density\", \"P_j\"], \"auc_base\": 0.8665087876522382, \"dauc\": 2.667125537048065e-05, \"ci95\": [-0.0006515142246219019, 0.00037671062932409776]}, \"L4_full_X0\": {\"cols\": [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"log_field_size\", \"phi_home\", \"density\", \"P_j\", \"label_coverage_early\", \"precision_c\", \"tag_coverage\", \"log_n_early\", \"share_early\", \"growth_j\"], \"auc_base\": 0.8657544473440986, \"dauc\": 1.3686565255799366e-05, \"ci95\": [-0.0006381478662662643, 0.0004211635345695987]}, \"L0_size_only\": {\"cols\": [\"log_n_early\", \"share_early\", \"log_field_size\"], \"auc_base\": 0.8336391266848366, \"dauc\": 0.004223358194140769, \"ci95\": [0.0010170984469827892, 0.005972329918350185]}}, \"gateway_alone_auc\": 0.6054439015180273, \"cond_logit\": {\"n_episodes_informative\": 4671, \"n_concepts_informative\": 1470, \"beta_gateway_std\": 0.05760821669635307, \n===== h3_results.json 3962\n{\"n\": 2838, \"G\": {\"partial_rho\": 0.02950282637789586, \"p_perm_one_sided\": 0.001999000499750125, \"ci95\": [-0.005645316827696381, 0.06495220976417931], \"per_group\": {\"PHYS\": {\"rho\": 0.08815908110625166, \"n\": 616, \"se\": 0.04222969304098089}, \"LIFEENV\": {\"rho\": 0.03157279387025358, \"n\": 968, \"se\": 0.03458586917742234}, \"SOC\": {\"rho\": 0.08620125351539243, \"n\": 1105, \"se\": 0.03140633304373836}, \"MATHDEC\": {\"rho\": 0.07916888808386258, \"n\": 149, \"se\": 0.08555881786939311}}, \"dl_pool\": {\"k\": 4, \"pooled\": 0.06832581887291983, \"se\": 0.019813935258362395, \"ci95\": [0.029490505766529534, 0.10716113197931013], \"tau2\": 0.0, \"I2\": 0.0, \"Q\": 1.6898313170596742}}, \"G_A\": {\"partial_rho\": 0.026181155490031614, \"p_perm_one_sided\": 0.00399800099950025, \"ci95\": [-0.01115668861449585, 0.06661133096553447], \"per_group\": {\"PHYS\": {\"rho\": 0.07245041089532982, \"n\": 616, \"se\": 0.04392553578737674}, \"LIFEENV\": {\"rho\": 0.019656998288203907, \"n\": 968, \"se\": 0.029793836941230036}, \"SOC\": {\"rho\": 0.07956023139864485, \"n\": 1105, \"se\": 0.02865793281795861}, \"MATHDEC\": {\"rho\": 0.1384434586257047, \"n\": 149, \"se\": 0.08053195621591049}}, \"dl_pool\": {\"k\": 4, \"pooled\": 0.059697280496741334, \"se\": 0.019618802734223017, \"ci95\": [0.021244427137664224, 0.09815013385581844], \"tau2\": 0.0001620737675430262, \"I2\": 0.09784437208019935, \"Q\": 3.3253686028844376}}, \"G_btw\": {\"partial_rho\": 0.04559887078144679, \"p_perm_one_sided\": 0.0014992503748125937, \"ci95\": [0.009104121849222446, 0.0862495145333611], \"per_group\": {\"PHYS\": {\"rho\": 0.10140288583252237, \"n\": 616, \"se\": 0.042034642331549785}, \"LIFEENV\": {\"rho\": -0.020376736896705216, \"n\": 968, \"se\": 0.03199201213135375}, \"SOC\": {\"rho\": 0.13947763368000918, \"n\": 1105, \"se\": 0.03185381299907427}, \"MATHDEC\": {\"rho\": 0.06637485152246067, \"n\": 149, \"se\": 0.08676012807764936}}, \"dl_pool\": {\"k\": 4, \"pooled\": 0.07164899353305614, \"se\": 0.04436059623373881, \"ci95\": [-0.015297775085071921, 0.1585957621511842], \"tau2\": 0.005685603332760305, \"I2\": 0.7743566244974596, \"Q\": 13.295316085919055}}, \"REL_home\": {\"partial_rho\": -0.13639675894418873, \"p_perm_one_sided\": 1.0, \"ci95\": [-0.17351749913750902, -0.10147997097025221], \"per_group\": {\"PHYS\": {\"rho\": -0.01915897677219635, \"n\": 616, \"se\": 0.04152924292816971}, \"LIFEENV\": {\"rho\": -0.19699259792929935, \"n\": 968, \"se\": 0.03218785667447833}, \"SOC\": {\"rho\": -0.18157636426593365, \"n\": 1105, \"se\": 0.03205239647668982}, \"MATHDEC\": {\"rho\": -0.25723955351270567, \"n\": 149, \"se\": 0.07540208149623213}}, \"dl_pool\": {\"k\": 4, \"pooled\": -0.15703491262206487, \"se\": 0.04589772331382849, \"ci95\": [-0.2469944503171687, -0.06707537492696103], \"tau2\": 0.006404205906291356, \"I2\": 0.7988680056049117, \"Q\": 14.915578245135025}}, \"holm_adjusted_p\": {\"G_btw\": 0.004497751124437781, \"G\": 0.004497751124437781, \"G_A\": 0.004497751124437781}, \"verdict_H3\": \"CONFIRMED\", \"notes\": \"Pre-registered test: one-sided permutation of the indicator WITHIN held-out group (2,000 draws), Holm over {G, G_A, G_btw}. Because the within-group permutation keeps group-level differences, its null is centred below zero (about -0.012 for G), reflecting a negative between-group component; the pooled partial rho (0.03-0.05) is therefore smaller than every within-group value (G: 0.03-0.09 in all 4 groups; DL pooled 0.068, 95% CI 0.029-0.107, I2 = 0). The concept-bootstrap CI of the pooled G rho includes 0 (-0.006, 0.065). Verdict per the pre-registered rule is CONFIRMED, but the effect is small; the rival REL_home (relatedness of early off-home landing fields to hom\n===== frame_summary.json 647\n{\"ladder\": [{\"early_min\": 30, \"weak_home\": true, \"n_concepts\": 12499, \"n_episodes\": 27393}], \"n_concepts\": 12499, \"n_episodes\": 27393, \"by_split\": {\"DEV\": 4771, \"COHORT\": 4356, \"HELDOUT_SOC\": 1352, \"HELDOUT_LIFEENV\": 1113, \"HELDOUT_PHYS\": 742, \"HELDOUT_MATHDEC\": 165}, \"episodes_by_split\": {\"COHORT\": 9799, \"DEV\": 9079, \"HELDOUT_SOC\": 3320, \"HELDOUT_LIFEENV\": 3099, \"HELDOUT_PHYS\": 1662, \"HELDOUT_MATHDEC\": 434}, \"by_group\": {\"Med\": 3868, \"SOC\": 2211, \"Eng\": 2087, \"LIFEENV\": 1668, \"PHYS\": 1097, \"BGM\": 719, \"CS\": 581, \"MATHDEC\": 268}, \"newborn_share\": 0.05392431394511561, \"weak_home\": 1150, \"intersect40\": 502, \"dev_R_rate\": 0.29364467452362597}\n===== checks.json 1468\n{\"T1_matcher_regression\": {\"files\": [1407, 1125, 1918], \"n_old\": 900, \"n_new\": 855, \"n_both\": 855, \"recall_vs_old\": 0.95, \"precision_vs_old\": 1.0, \"exact_set_equality\": false, \"only_old_examples\": [[1918, 2073, 44], [1918, 5247, 8], [1918, 13370, 8], [1918, 14955, 28], [1918, 23416, 57], [1918, 23600, 57], [1918, 25741, 23], [1918, 27629, 28], [1918, 32878, 28], [1918, 33642, 8]], \"only_new_examples\": [], \"note\": \"new = surface Aho-Corasick (last-token s/es/ies variants) + stemmed verification; old = stemmed positional matcher on every title. Differences are stem-only inflections of non-final tokens.\"}, \"T3_p78_agreement\": {\"n_p78_in_lexicon\": 55, \"n_p78_in_frame\": 48, \"median_rho_match_all\": 0.9990113692535837, \"median_rho_grounded_all\": 0.9920983318700615, \"median_rho_match_frame\": 0.9991379023041315, \"share_abs_dt0_le1_all\": 0.5272727272727272, \"share_abs_dt0_le1_frame\": 0.5416666666666666, \"base_total_ratio_vs_iter1_min_max\": [1.0, 1.0], \"note\": \"iteration-1 counts are ungrounded stemmed title matches of P78 phrases (+aliases); t0_iter1_api is the S0 API onset (title_and_abstract search)\"}, \"iteration1_replication\": {\"n_episodes\": 85, \"n_concepts\": 39, \"auc_base\": 0.85, \"auc_gateway\": 0.8726666666666666, \"dauc_in_sample\": 0.022666666666666613, \"ci95\": [-0.004082472495170955, 0.06833495670995672], \"iteration1_value\": 0.103, \"same_sign_as_iteration1\": true, \"note\": \"in-sample concept-clustered bootstrap, as in art_33 (80 rows, 28 concepts)\"}}\n===== deviations.json 3500\n{\"openalex_api_skipped\": \"At 17:39 the run key reported X-RateLimit-Remaining=0 (reset in ~6.4 h) and the anonymous per-IP pool 999 (< the plan floor of 1,500, shared with sibling runs). Per fallback 6: the 50-concept API audit is NOT done, insularity I_j = NA and is removed from X0 before freezing (its role is partly absorbed by P_j(-c) and field FE). 2 probe calls used (1 keyed, refused with 429; 1 anonymous).\", \"wikidata_endpoint\": \"wbgetentities (50 QIDs/call) was rate-limited (HTTP 429, maxlag 9 s); aliases were fetched from the Wikidata SPARQL endpoint instead (500 QIDs/query), only for the 43.5k pre-screen survivors with >= 1 post-2002 hit in the 1% sample.\", \"t2_lexicon_fix\": \"T2 inspection of the first 50 scanned files showed generic single-token Wikidata aliases (socials, ashes, morals, heavies, organics) and aliases equal to level-0/1 names (machine learning). Before the full scan (outcome-blind) aliases equal to level-0/1 names and lowercase single-token aliases were dropped (mixed-case ones like miRNA, lncRNA kept), and no plural variants are generated for single-token aliases. The lexicon was re-hashed (frozen_lexicon.sha256, last line) and the scan restarted from zero.\", \"base_type\": \"Base works = type in {article, review} (as iteration 1 and the plan); the 2026 snapshot also has type conference-paper, which is therefore excluded (conference-heavy CS is under-covered).\", \"llm_budget\": \"The per-concept precision gate covers ~13k outcome-blind onset candidates (plan expected <= 5k). At the measured $0.00022/call this exceeds the plan cap of $2.00, so the artifact LLM cap was raised to $3.50 (well inside the $10 per-artifact ceiling). Concepts are labelled in a seeded random order; any concept left unlabelled by a budget stop is gated by the sense filter (precision_source=filter).\", \"grounding_rule\": \"T4: the sense filter (test P=0.862, R=0.988) did not beat exact-name-only precision (0.872), so the frozen grounding rule is TAG (legacy concept tag score >= 0.3; test P=0.947, R=0.659, F1 0.777 > exact-name F1 0.562), chosen on the benchmark test split only. Untagged (tagstate 3) rows, 0.05% of hits, are therefore not counted.\", \"benchmark_kappa\": \"Cohen kappa between gemini-2.5-flash-lite and gpt-4.1-nano was 0.20 (< 0.6) on 146 double-labelled pairs; all 41 disagreements were adjudicated by gemini-2.5-flash as pre-specified. 10 of 400 pairs got no parsable label and were dropped (n=390).\", \"home_window\": \"Home = first 30 grounded venue-labelled works counted from t0 onward (iteration-1 home window started at t0); the boundary year contributes proportionally (expected composition of the hash-random tie break).\", \"precision_gate_fallback\": \"896 concepts had no LLM precision label; gated by the sense filter's mean predicted precision (precision_source=filter)\", \"post_unseal_code_fix\": \"First held-out scoring run crashed on cohort episodes whose outcome window has no venue-labelled grounded work (R = 0/0, undefined; none occur in DEV). Rows with undefined R are now excluded explicitly (count reported as n_R_undefined_excluded). No model, covariate, threshold or standardisation constant was changed; frozen_spec.json and its sha256 are unchanged.\", \"pigeonhole_heldout_fix\": \"The held-out crossed concept x field bootstrap (robustness diagnostic, not a verdict criterion) was mis-indexed in the first run (all weights 0 -> NaN CI); recomputed post hoc by fix_pigeonhole.py with fields shared between dev refit and held-out evaluation.\"}\n===== audit_placebo.json 1294\n{\"H3_G_per_group\": {\"audit\": {\"LIFEENV\": 0.031572793870253545, \"MATHDEC\": 0.07916888808386263, \"PHYS\": 0.08815908110625174, \"SOC\": 0.08620125351539244}, \"reported\": {\"PHYS\": 0.08815908110625166, \"LIFEENV\": 0.03157279387025358, \"SOC\": 0.08620125351539243, \"MATHDEC\": 0.07916888808386258}}, \"H3_G_DL_pooled\": {\"audit\": 0.0676251719388039, \"reported\": 0.06832581887291983, \"note\": \"SEs from an independent 300-draw bootstrap, so agreement is approximate\"}, \"H3_test_real_vs_shuffled_outcome\": {\"real_rho_p\": [0.02950282637789588, 0.001996007984031936], \"shuffled_rho_p\": [-1.1504953966775875e-05, 0.011976047904191617], \"shuffled_fails_at_0.05\": false}, \"heldout_dauc_real\": -7.0814885732017885e-06, \"heldout_dauc_shuffled_R\": {\"mean\": -0.0004923421172377512, \"sd\": 0.0019405164153251393}, \"heldout_dauc_planted_gateway_effect_1SD\": 0.04422868061475971, \"H3_calibrated_within_group_stat\": {\"real\": [0.06733617351122426, 0.0033222591362126247], \"shuffled_outcome\": [0.04814139685487308, 0.009966777408637873], \"note\": \"size-weighted mean of within-group partial rho; one-sided within-group permutation p\"}, \"H3_preregistered_test_valid\": true, \"H3_calibration_40_shuffles\": {\"false_positive_rate_preregistered_pooled_test\": 0.0, \"false_positive_rate_within_group_stat\": 0.0, \"nominal_alpha\": 0.05}}\n===== exploratory_domain_specificity.json 4423\n{\"CS\": {\"split\": \"DEV\", \"n\": 861, \"n_concepts\": 357, \"R_rate\": 0.3600464576074332, \"gateway_alone_auc\": 0.638873602248112, \"spearman_gateway_R\": 0.23976191260760119, \"spearman_gateway_Pj\": 0.8314206799749618, \"dauc_over_L1\": 0.0013348164627362546, \"dauc_over_L1_ci95\": [0.00040275968754140135, 0.0022435201729190607], \"dauc_over_X0\": 4.683566535901296e-05, \"dauc_over_X0_ci95\": [-0.0001623837132775585, 0.00026811682953241926], \"top_adopting_fields\": {\"22\": 303, \"33\": 262, \"26\": 57, \"14\": 44, \"27\": 36}}, \"Eng\": {\"split\": \"DEV\", \"n\": 3051, \"n_concepts\": 1200, \"R_rate\": 0.28482464765650606, \"gateway_alone_auc\": 0.5899967196826426, \"spearman_gateway_R\": 0.1419836641602803, \"spearman_gateway_Pj\": 0.5271755593204119, \"dauc_over_L1\": 0.0014381712916329281, \"dauc_over_L1_ci95\": [0.0003547780510088472, 0.002504297869664934], \"dauc_over_X0\": -1.0020262024679205e-05, \"dauc_over_X0_ci95\": [-0.00012627646757510657, 9.624186866584718e-05], \"top_adopting_fields\": {\"33\": 675, \"17\": 461, \"31\": 357, \"25\": 300, \"23\": 240}}, \"BGM\": {\"split\": \"DEV\", \"n\": 1270, \"n_concepts\": 466, \"R_rate\": 0.36299212598425196, \"gateway_alone_auc\": 0.6325717457346716, \"spearman_gateway_R\": 0.22403280240133258, \"spearman_gateway_Pj\": 0.4942088395831041, \"dauc_over_L1\": 0.0004156064233983292, \"dauc_over_L1_ci95\": [-0.0008517890290728053, 0.0019161076017773604], \"dauc_over_X0\": 6.971462586036203e-05, \"dauc_over_X0_ci95\": [-7.321926574666848e-05, 0.00020311538828751414], \"top_adopting_fields\": {\"27\": 349, \"11\": 200, \"16\": 140, \"28\": 125, \"33\": 117}}, \"Med\": {\"split\": \"DEV\", \"n\": 3897, \"n_concepts\": 1964, \"R_rate\": 0.2632794457274827, \"gateway_alone_auc\": 0.6300152835744689, \"spearman_gateway_R\": 0.20069006282086152, \"spearman_gateway_Pj\": 0.749326052367859, \"dauc_over_L1\": 0.0013426596407036806, \"dauc_over_L1_ci95\": [0.0007046755142917305, 0.0022240623438168905], \"dauc_over_X0\": -2.376388744451674e-06, \"dauc_over_X0_ci95\": [-0.00022338153852785592, 0.0003146361993586116], \"top_adopting_fields\": {\"33\": 917, \"13\": 798, \"28\": 297, \"11\": 252, \"36\": 230}}, \"PHYS\": {\"split\": \"HELDOUT\", \"n\": 1662, \"n_concepts\": 642, \"R_rate\": 0.3237063778580024, \"gateway_alone_auc\": 0.5356037254097819, \"spearman_gateway_R\": 0.05832122201867047, \"spearman_gateway_Pj\": -0.25921566573707644, \"dauc_over_L1\": 0.0007028139014934043, \"dauc_over_L1_ci95\": [-0.00125741597941412, 0.0025707597128757104], \"dauc_over_X0\": 0.00012071862307994063, \"dauc_over_X0_ci95\": [-0.0001813074067488041, 0.0003963957814581031], \"top_adopting_fields\": {\"22\": 414, \"33\": 199, \"25\": 194, \"13\": 155, \"23\": 129}}, \"LIFEENV\": {\"split\": \"HELDOUT\", \"n\": 3099, \"n_concepts\": 1060, \"R_rate\": 0.303323652791223, \"gateway_alone_auc\": 0.5230933351729031, \"spearman_gateway_R\": 0.03711839911718471, \"spearman_gateway_Pj\": 0.017695283725084936, \"dauc_over_L1\": -0.0017374079804480802, \"dauc_over_L1_ci95\": [-0.0029812820900238625, -0.00042731295443147196], \"dauc_over_X0\": -9.559193085850737e-05, \"dauc_over_X0_ci95\": [-0.000405695772904599, 0.00024196810077463374], \"top_adopting_fields\": {\"13\": 627, \"33\": 491, \"27\": 474, \"23\": 293, \"22\": 292}}, \"SOC\": {\"split\": \"HELDOUT\", \"n\": 3320, \"n_concepts\": 1233, \"R_rate\": 0.3102409638554217, \"gateway_alone_auc\": 0.4063083478187138, \"spearman_gateway_R\": -0.15090731086653641, \"spearman_gateway_Pj\": 0.234711337113779, \"dauc_over_L1\": -0.0005965150294654498, \"dauc_over_L1_ci95\": [-0.001542977141382254, 0.0004547993053009263], \"dauc_over_X0\": -0.00013609191503805018, \"dauc_over_X0_ci95\": [-0.0003801020099728075, 0.00014", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [8] TOOL CALL — Bash · 2026-09-28 20:56:03 UTC

```
Dump remaining H1 held-out and dev result keys:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results; python3 -c "
import json
d=json.load(open('h1_heldout.json'))
for k,v in d.items():
  if k in ('primary','cohort'): continue
  print('##',k, json.dumps(v)[:1500])
print('#### DEV')
d=json.load(open('h1_dev.json'))
for k,v in d.items():
  if k in ('primary','ladder','by_group'): continue
  print('##',k, json.dumps(v)[:1200])
"
```

### [9] TOOL RESULT — Bash · 2026-09-28 20:56:03 UTC

```
{"stdout": "## spec_sha256 \"147ce58a4052eaae6dfb77c465ae7a86ef3d742749a4babc1ffd06ab42d33293\"\n## n_dev 9079\n## n_heldout 8515\n## n_cohort 9798\n## n_R_undefined_excluded {\"COHORT\": 1}\n## dl_pool {\"k\": 4, \"pooled\": -4.3991314466003225e-05, \"se\": 0.00019697749811468297, \"ci95\": [-0.0004300672107707818, 0.0003420845818387754], \"tau2\": 0.0, \"I2\": 0.0, \"Q\": 1.6886147538161116}\n## evaluable_groups [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]\n## sign_test_groups {\"n\": 4, \"n_positive\": 2, \"p_one_sided\": 0.6875}\n## cond_logit {\"n_episodes_informative\": 5036, \"n_concepts_informative\": 1452, \"beta_gateway_std\": -0.0746527649197613, \"se\": 0.06240505008412258, \"z\": -1.1962615977253235, \"p_two_sided\": 0.23159448975679897, \"LR\": 1.4407798330089463, \"LR_p\": 0.23001318820583636, \"method\": \"ConditionalLogit\"}\n## lpm_field_fe {\"n\": 8515, \"within_field_sd_of_regressor\": 0.024114481018227937, \"beta_within_per_sd\": 0.06778995979996934, \"se_concept\": 0.0331393319594772, \"p_concept\": 0.04079531852765418, \"se_twoway\": 0.04966999749594251, \"p_twoway\": 0.17231372111171483}\n## lpm_field_fe_all_splits {\"n\": 27392, \"within_field_sd_of_regressor\": 0.027660339253232278, \"beta_within_per_sd\": 0.05067386565261721, \"se_concept\": 0.018604056811259772, \"p_concept\": 0.0064534148871445325, \"se_twoway\": 0.03769843239877019, \"p_twoway\": 0.1788868704273867}\n## boundary {\"beta_interaction\": 0.06417966727640417, \"se\": 0.08519974469773009, \"p\": 0.45127882861982116, \"beta_gateway_main\": -0.09900021818195034, \"n_top_tercile_home_episodes\": 1418, \"prediction\": \"negative interaction\", \"consistent\": false}\n## logit_clustered_se {\"concept\": {\"beta_gateway_std\": -0.044818092605625484, \"se\": 0.04216240540834801, \"p\": 0.2877878062578988}, \"twoway\": {\"beta_gateway_std\": -0.044818092605625484, \"se\": 0.03211135570372762, \"p\": 0.16280228890018333}, \"field\": {\"beta_gateway_std\": -0.044818092605625484, \"se\": 0.030306748920514468, \"p\": 0.13918960959753784}}\n## rival_head_to_head {\"dauc_relatedness_pair\": 0.0033563007447128257, \"relatedness_ci95\": [0.0010094242010481095, 0.005105673731210405], \"dauc_gateway\": -4.8790806590703895e-05, \"gateway_ci95\": [-0.0006670042214246024, 0.0001791307761191849], \"diff_gateway_minus_relatedness\": -0.0034050915513035296}\n## ladder {\"L1_iter1_base\": {\"auc_base\": 0.8287800661164155, \"dauc\": -0.001621790818804647, \"ci95\": [-0.0035174793414679663, -0.0001610124452294174], \"per_group\": {\"PHYS\": -0.00026458876291535205, \"LIFEENV\": -0.003279690163885962, \"SOC\": -0.0009674820875907875, \"MATHDEC\": 0.0005855522682446379}}, \"L2_plus_relatedness\": {\"auc_base\": 0.8296114588620087, \"dauc\": -0.0011816340749275511, \"ci95\": [-0.002800422402799094, 3.549670495509316e-07], \"per_group\": {\"PHYS\": -0.0020241040363015994, \"LIFEENV\": -0.001749726528239015, \"SOC\": 0.00024462627718668806, \"MATHDEC\": 0.0012635601577909439}}, \"L3_plus_Pj\": {\"auc_base\": 0.8360392415816693, \"dauc\": -3.5147571725069326e-05, \"ci95\": [-0.000673644201355314, 0.00026714658467579525], \"per_group\": {\"PHYS\": 0.0004927965709294879, \"LIFEENV\": -0.0002261685374436162, \"SOC\": -0.00011701360919147419, \"MATHDEC\": 9.245562130177909e-05}}, \"L4_full_X0\": {\"auc_base\": 0.8372646639437369, \"dauc\": -8.9655543402678e-06, \"ci95\": [-0.000621911239638534, 0.00032883696703854824], \"per_group\": {\"PHYS\": 0.0004977576102344061, \"LIFEENV\": -0.00025573305214199316, \"SOC\": -0.00012125323271283683, \"MATHDEC\": 0.0005239151873767112}}, \"L0_size_only\": {\"auc_base\": 0.8184903383808104, \"dauc\": -0.0017103419098605244, \"ci95\": [-0.005008237509068825, 0.0012084771771697052], \"per_group\": {\"PHYS\": -0.0012567966238474781, \"LIFEENV\": -0.0025607797148009537, \"SOC\": -0.00163395090515972, \"MATHDEC\": -0.0028353057199210774}}}\n## gateway_alone_auc 0.5056949785879173\n## placebo_rewired {\"p95\": 0.00011013988603601445, \"mean\": -9.676074521690503e-05, \"share_ge_real\": 0.365, \"real_exceeds_p95\": false, \"values\": [-6.691681862625032e-06, 1.299355701478433e-05, -0.00042560396002044865, -1.539736506261935e-05, -4.138447909218801e-05, -7.074991794575602e-05, 2.8001115366826923e-05, -7.679192195753082e-05, 9.498290177822888e-05, 1.7866140895383964e-05, -0.0003904563882952683, -5.873087770702501e-05, -7.796134209314687e-07, -0.0005079181437093183, 1.5657236202892832e-05, -5.119461463831687e-05, -3.3783248238883345e-06, 1.4747687211880134e-05, -0.00029794226234991505, -0.00022160511488777956, -0.00033932674144199204, -2.9235503283375763e-05, -0.00014403357950931728, -0.0002418100960458469, 7.055501459041214e-05, 7.796134208870598e-06, -1.4292912715596628e-06, -0.00018528812303131303, -0.00033367454414057196, -2.0529820083381445e-05, -0.0003286070569048505, -2.793614758189733e-05, -2.8910664358061666e-05, 5.002519450703069e-05, -0.00024941132689948464, -6.438307500844509e-05, -4.6386998542979896e-05, 2.0334916728148578e-05, -3.215905361175775e-05, 0.0003106759482243149, -0.00012519292183788, 0.00012993557014817636, -9.849116217230947e-05, -0.0001465023553420819, -2.0594787868533082e-05, 0.00018977090020144693, -0.00024674764771148716, -0.00015345390834509143, -6.152449246521474e-05, -4.222906029816009e-05, 7.854605215462662e-05, -0.00045503436665894625, -5.502771395782258e-05, -2.09196267939582e-05, -1.1304394602951184e-05, -1.2993557019225221e-07, -1.1109491247718317e\n## placebo_permutation {\"p95\": 0.00015462982525476452, \"share_ge_real\": 0.38, \"values\": [-3.6641830781780627e-05, -4.547744955063493e-07, -8.250908704410254e-05, -0.00039363980976392376, -1.3123492584976582e-05, -2.598711402956866e-05, -1.1304394602840162e-05, 0.0001357177030197887, -0.00011362865609465533, -0.0003301662837466024, -3.3393441528195567e-05, -0.0003493967481283944, -0.0002664328865887855, -7.094482130087787e-05, -1.9490335523286717e-07, -6.262894481146031e-05, -1.0070006686513366e-05, -0.00012116491916314143, -0.00019003077134194246, 4.339848042933525e-05, -6.431810722340447e-05, -0.0001702155968941188, -0.0003272427334182204, 3.6381959641618167e-06, -5.886081327732828e-05, 0.00025363423292923404, 1.253878251927798e-05, 0.00015293416606432242, -5.665190858461511e-05, -0.00016034049356294933, -0.00016917611233302488, 4.853093545031939e-05, -6.568243071003455e-05, -0.00010778155543789136, -0.00016826656334190115, -1.7866140895383964e-05, -0.0004851144511482941, 0.0001010249057901147, -5.717165086460696e-06, 1.7541301969847822e-06, -9.394341721724597e-05, -3.482273279975523e-05, -3.2353956966879593e-05, -2.3843177122118142e-05, 8.9655543402678e-06, -9.043515682316539e-05, -0.0007417372021909507, -0.00032081092269586886, 0.00021712233771742362, -5.847100656541926e-06, -0.0004059836889280799, -3.7551379772793325e-05, -3.2159053611646726e-05, -0.0003436146152568931, -0.00019691735655957832, -0.00018892631899547485, -0.00012876615001689018, 2.111453014919107e-05, 7.991037563992442e-06, 9.797\n## leave_one_field_out {\"by_field\": {\"11\": -5.418832267722884e-05, \"12\": -3.878199250906267e-05, \"13\": 8.823042700678574e-05, \"14\": -3.2276389175800446e-06, \"15\": -7.927410907826449e-06, \"16\": -1.528603223532876e-05, \"17\": 0.00013756992708136018, \"18\": -1.577093306248667e-05, \"19\": 2.3526158405284825e-05, \"20\": -1.3448696671525262e-05, \"21\": -1.8343470160497866e-05, \"22\": 0.00010844198903126046, \"23\": -3.5967480641496685e-05, \"24\": -2.7612407958677032e-05, \"25\": -8.384070705480529e-05, \"26\": 1.1376564277632006e-05, \"27\": -2.198644378692549e-05, \"28\": -3.132212134115964e-05, \"29\": -4.483535677057837e-06, \"30\": -6.054842813130179e-06, \"31\": -3.4308679425998356e-05, \"32\": -1.740982112918843e-06, \"33\": -0.00012334639832922711, \"34\": -1.2046074607474644e-05, \"35\": -6.487631509832781e-05, \"36\": -4.099732374807097e-06}, \"min\": -0.00012334639832922711, \"max\": 0.00013756992708136018, \"most_influential_field\": 17, \"dauc_without_it\": 0.00013756992708136018}\n## pigeonhole_crossed_bootstrap {\"B\": 500, \"ci95\": [-0.0022785500497700143, 0.0010009281747794191], \"sd\": 0.0007028881406013923, \"n_valid\": 500, \"recomputed_by\": \"fix_pigeonhole.py\"}\n## verdict_H1 {\"verdict\": \"DISCONFIRMED\", \"criteria\": {\"pooled_dauc_ge_0.05\": false, \"refit_ci_gt0\": false, \"sign_ge3_of_4_evaluable\": false, \"n_groups_positive\": 2, \"cohort_same_sign\": true, \"lpm_beta_within_gt0_p05\": true, \"placebo_null\": false}}\n## sensitivities {\"R_abs1\": {\"dauc\": 0.0008216880503503221, \"ci95\": [-0.0005837578096948791, 0.001965595694481029], \"n\": 8515, \"per_group\": {\"PHYS\": 0.002625810269238027, \"LIFEENV\": 0.00266916438371001, \"SOC\": -0.001977771943642459, \"MATHDEC\": 0.0008790049663780497}}, \"R_abs2\": {\"dauc\": -3.2977923351107385e-05, \"ci95\": [-0.0011965634092123978, 0.0007857622602803288], \"n\": 8515, \"per_group\": {\"PHYS\": 0.0020307564812208634, \"LIFEENV\": 0.0009867694825984596, \"SOC\": -0.0023663613864496336, \"MATHDEC\": -0.0012040939193256328}}, \"R_abs3\": {\"dauc\": 5.200956282425118e-06, \"ci95\": [-0.0012348622172581342, 0.0007847453433751601], \"n\": 8515, \"per_group\": {\"PHYS\": 0.0015156048759544793, \"LIFEENV\": 0.0009379590275376826, \"SOC\": -0.0022677133035761132, \"MATHDEC\": -0.0021470040530178203}}, \"n_early_ge5\": {\"dauc\": -0.00041009226922228414, \"ci95\": [-0.0024222030490049645, 0.0003131203312631448], \"n\": 3626, \"per_group\": {\"PHYS\": -0.0007688208875695768, \"LIFEENV\": -0.0007282465160548535, \"SOC\": -0.00026867614029935094, \"MATHDEC\": -0.0005052418845521434}}, \"newborn_only\": {\"dauc\": 0.002297622228159324, \"ci95\": [-0.003927294660467723, 0.01277247508837335], \"n\": 387, \"per_group\": {\"PHYS\": 0.01377410468319551, \"LIFEENV\": -0.00694444444444442, \"SOC\": -0.0018633540372671176, \"MATHDEC\": null}}, \"excl_intersection_born\": {\"dauc\": -1.1858400570718963e-05, \"ci95\": [-0.0006131799537924087, 0.00020801416397697178], \"n\": 8393, \"per_group\": {\"PHYS\": 0.0003455663833019651, \"LIFEENV\": -0.00022199654247923029, \"SOC\": -8.38346762\n#### DEV\n## n_episodes 9079\n## n_concepts 3987\n## R_rate 0.29364467452362597\n## T5_seed_stability {\"ci_seed1_500\": [-0.0006645566569091627, 0.0004211635345695987], \"ci_seed2_500\": [-0.0006704466054427899, 0.000489658161158668], \"max_abs_diff\": 6.849462658906931e-05}\n## rival_head_to_head {\"dauc_relatedness_pair\": -0.00017470842059497116, \"dauc_gateway\": -0.000142246695308601, \"diff_gateway_minus_relatedness\": 3.246172528637015e-05, \"diff_boot_ci95\": [-0.0015783023924223231, 0.0016099151945286989], \"relatedness_boot_ci95\": [-0.0017096415625327736, 0.0011992251564341885], \"gateway_boot_ci95\": [-0.000927531192910283, 0.00027783484949635273]}\n## gateway_alone_auc 0.6054439015180273\n## cond_logit {\"n_episodes_informative\": 4671, \"n_concepts_informative\": 1470, \"beta_gateway_std\": 0.05760821669635307, \"se\": 0.050620675092339903, \"z\": 1.138037305730649, \"p_two_sided\": 0.2551049050718702, \"LR\": 1.2934423734448046, \"LR_p\": 0.2554145329529829, \"method\": \"ConditionalLogit\"}\n## lpm_field_fe {\"n\": 9079, \"within_field_sd_of_regressor\": 0.025486300560656133, \"beta_within_per_sd\": -0.00345886836143571, \"se_concept\": 0.03468988448996966, \"p_concept\": 0.9205759349273591, \"se_twoway\": 0.07500050998634529, \"p_twoway\": 0.9632162541624284}\n## boundary {\"beta_interaction\": -0.051366877235913724, \"se\": 0.060181642960999884, \"p\": 0.3933650944321222, \"beta_gateway_main\": 0.0778233356256058, \"n_top_tercile_home_episodes\": 5024, \"prediction\": \"negative interaction\", \"consistent\": true}\n## logit_clustered_se {\"concept\": {\"beta_gateway_std\": 0.049364905393459176, \"se\": 0.03255847767989778, \"p\": 0.1294707948023824}, \"twoway\": {\"beta_gateway_std\": 0.049364905393459176, \"se\": 0.026546564945950497, \"p\": 0.06294793589312302}, \"field\": {\"beta_gateway_std\": 0.049364905393459176, \"se\": 0.02541215957655525, \"p\": 0.052068103338287756}}\n## placebo_rewired {\"n\": 200, \"p95\": 0.00016264201712380398, \"mean\": -0.0002718192802527214, \"real\": 1.3686565255799366e-05, \"share_ge_real\": 0.205, \"real_exceeds_p95\": false, \"values\": [-0.0002762463577066221, -0.0018747669920753385, -0.00021799072097650196, -0.00015634268773023763, -0.00031748152225941073, -0.0004525924869646092, -0.0013342061540645433, -0.0008623121007135248, -0.00015090315538490717, -0.0004913710885230405, 0.00012505075434621205, -0.0002832651091199123, -5.6266990495990044e-05, 0.00020278342624802104, 0.0001427731016645506, 3.953896629471654e-05, -0.00017921211941829274, -0.0005121348947871862, 0.00012768278612629302, 5.076896855582547e-05, -0.00018833649625560334, -0.00021313608458251032, -0.00031327027141159203, -0.0008902116375812952, -6.720454478192917e-05, -0.000394629298210214, -0.0009482333159306355, 2.17581293812108e-05, 0.00017599519168731703, -0.0010616446408497904, -0.00025694479132021275, -0.00032660589909672133, -0.0001351694543001436, -5.585756333048586e-05, 1.7839326508672926e-05, -0.0006942130043658956, -0.0007236332707065696, -8.989850768481578e-05, -0.0005460588599510707, -0.00010212283306287873, -7.305350429298585e-05, -0.00011265096018275855, -3.09994854084116\n## placebo_permutation {\"n\": 200, \"p95\": 0.00017410012880585395, \"share_ge_real\": 0.13, \"values\": [0.00010955101164189518, -0.00031490798007483, -3.597110099295975e-05, 2.2167556546826006e-05, -0.00033771892216782895, -0.0001294374739794213, -5.6559438471825985e-05, -5.498021940375519e-05, -0.00025717874970054844, 0.00019839670661470077, -0.0003352038695778603, -2.3395838033568594e-07, -8.416652736387142e-05, -0.0005579322477584636, -0.0003488904348338817, -0.00018851196504099388, -0.0002623843236655432, -0.00026150697973881254, -0.0005069878104173586, 0.00021372098053351607, -2.105625423964863e-05, 0.0002001513944681621, -0.001869327459730119, -0.00036035439547543735, -0.00015774643801280686, -0.00019137795520129952, -0.00032789267018928925, -0.0009041906508125974, -0.0014916601441019584, -0.00041667987556692765, -0.0007120523308747906, -0.00010668502148147851, -5.2991573170069195e-05, -0.0003468432990050285, -0.00022290384696588283, -0.000331460535490824, 0.00018523654771473996, -0.0003199380852542122, -5.2114229243227506e-05, -0.00012066403471278075, -0.00014031653866997118, -0.00022846035850143664, -0.00018535352690507434, -0.00012499226475093383, -0.0004415379534887798, -0.00018447618297823265, 0.00\n## leave_one_field_out {\"by_field\": {\"11\": -2.1903925243482725e-05, \"12\": 3.3073713556652784e-05, \"13\": -6.340348097777504e-05, \"14\": -1.8732190824044537e-06, \"16\": -0.0001594539603747558, \"17\": -0.00017623856059445497, \"18\": 2.0510411553598118e-05, \"19\": 2.0223746297842737e-05, \"20\": 5.2925460981456673e-05, \"21\": 3.432559736060714e-05, \"22\": 4.673672867394618e-05, \"23\": -8.121010473871593e-06, \"24\": 3.020378555596004e-06, \"25\": -0.00010636326896196202, \"26\": 9.191834061939019e-05, \"27\": -0.00010622333878484991, \"28\": 1.0962740097930634e-06, \"29\": 1.129377508179985e-05, \"30\": 2.362804878064395e-05, \"31\": 1.8050797522928264e-05, \"32\": 5.9287235409377637e-05, \"33\": 8.041535014913226e-05, \"34\": -1.2936295682441923e-06, \"35\": 4.554618219554385e-05, \"36\": 3.207421752748907e-05}, \"min\": -0.00017623856059445497, \"max\": 9.191834061939019e-05, \"most_influential_field\": 17, \"dauc_without_it\": -0.00017623856059445497, \"full\": 1.3686565255799366e-05}\n## pigeonhole_crossed_bootstrap {\"B\": 500, \"ci95\": [-0.005601464691729943, 0.0013088663307541258], \"sd\": 0.002317001584655802}\n## power {\"0.0\": {\"mean_dauc\": -0.00012345445272740895, \"power_ci_gt0\": 0.125}, \"0.1\": {\"mean_dauc\": 0.0003587990637813232, \"power_ci_gt0\": 0.325}, \"0.2\": {\"mean_dauc\": 0.0018673314094028697, \"power_ci_gt0\": 0.65}, \"0.3\": {\"mean_dauc\": 0.004004965929571655, \"power_ci_gt0\": 0.9}, \"min_detectable_dauc_80pct\": 0.004004965929571655, \"n_heldout_episodes_assumed\": 8515, \"note\": \"planted effect b in SD log-odds of standardised gateway_j on the dev covariate structure; 40 sims x 150 boot\"}\n## H3_dev {\"G\": 0.13819570627839578, \"G_A\": 0.13921297416616912, \"G_btw\": 0.16997089406664004, \"REL_home\": -0.04234826179807664, \"n\": 4205}\n## runtime_s 235.48593401908875", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-28 20:56:23 UTC

```
Walk Experiment 6 held-out result structure:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/results; python3 -c "
import json
d=json.load(open('heldout_result.json'))
def walk(d,p='',depth=0):
  if isinstance(d,dict):
    for k,v in d.items():
      s=json.dumps(v)
      if len(s)<400: print(p+k,':',s)
      else:
        print(p+k,': {...}' ); walk(v,p+'  ',depth+1) if depth<3 else print(p+'  ',s[:400])
  else: print(p, json.dumps(d)[:400])
walk(d)
" | head -300
```

### [11] TOOL RESULT — Bash · 2026-09-28 20:56:23 UTC

```
{"stdout": "n_heldout_concepts : 374\nby_group : {\"Cohort\": 248, \"Social\": 54, \"Physical\": 34, \"LifeEnv\": 34, \"OtherHealth\": 4}\nH2_pooled : {...}\n  n_rows : 46433\n  n_strata : 2339\n  n_concepts : 369\n  n_events : 1373\n  entry_rate : 0.02956948721814227\n  models : {...}\n    M0 : {\"coef\": {\"a_phi_home\": 0.33064441529782246, \"b_log_size\": 1.584569503949015, \"c_density\": 0.36227353934450424, \"e_gate_own\": 0.09944954700323524}, \"se\": {\"a_phi_home\": 0.02736968235608079, \"b_log_size\": 0.05112728370177903, \"c_density\": 0.03013663752993411, \"e_gate_own\": 0.030502854814615843}, \"ll\": -3270.093339796141, \"n_strata\": 961, \"n_events\": 1373, \"n_rows\": 18846, \"converged\": true}\n    M1 : {...}\n      coef : {\"a_phi_home\": 0.37188553304728283, \"b_log_size\": 1.6738276315064888, \"c_density\": 0.23852929616788293, \"e_gate_own\": 0.05164125007538622, \"d0_ret_rel\": 0.2809043442272664}\n      se : {\"a_phi_home\": 0.027921572124598486, \"b_log_size\": 0.05288720649766899, \"c_density\": 0.034421918211009254, \"e_gate_own\": 0.0315219540144637, \"d0_ret_rel\": 0.032159975704963886}\n      ll : -3235.809018933568\n      n_strata : 961\n      n_events : 1373\n      n_rows : 18846\n      converged : true\n    M2 : {...}\n      coef : {\"a_phi_home\": 0.36478607003405844, \"b_log_size\": 1.6795135455218, \"c_density\": 0.24721762419454624, \"e_gate_own\": 0.019351762291929017, \"d_ret_gate\": 0.3019648521082155}\n      se : {\"a_phi_home\": 0.02772926123612498, \"b_log_size\": 0.05279709656652038, \"c_density\": 0.03379253921762855, \"e_gate_own\": 0.032662090679520965, \"d_ret_gate\": 0.03418983053914712}\n      ll : -3234.235132476613\n      n_strata : 961\n      n_events : 1373\n      n_rows : 18846\n      converged : true\n    M3 : {...}\n      coef : {\"a_phi_home\": 0.36936674458570773, \"b_log_size\": 1.6818176588931806, \"c_density\": 0.2380779743085792, \"e_gate_own\": 0.028999552223334616, \"d0_ret_rel\": 0.11633740617530272, \"d_ret_gate\": 0.19139604594713114}\n      se : {\"a_phi_home\": 0.02791923110501382, \"b_log_size\": 0.05292618682191926, \"c_density\": 0.03440779835762934, \"e_gate_own\": 0.03320444240582659, \"d0_ret_rel\": 0.07809784050423697, \"d_ret_gate\": 0.0821312421090051}\n      ll : -3233.12945432314\n      n_strata : 961\n      n_events : 1373\n      n_rows : 18846\n      converged : true\n    M2lost : {...}\n      coef : {\"a_phi_home\": 0.32791908447413465, \"b_log_size\": 1.5834072596401476, \"c_density\": 0.36914417297567764, \"e_gate_own\": 0.10317255712560171, \"d_lost_gate\": -0.06322615097883642}\n      se : {\"a_phi_home\": 0.027397318970110676, \"b_log_size\": 0.051120809259672675, \"c_density\": 0.030304621819881934, \"e_gate_own\": 0.030554888439417182, \"d_lost_gate\": 0.034737288878067214}\n      ll : -3268.246948147513\n      n_strata : 961\n      n_events : 1373\n      n_rows : 18846\n      converged : true\n  LR : {\"M2_vs_M0\": {\"LR\": 71.71641463905598, \"df\": 1, \"p\": 2.4845706606291646e-17}, \"M1_vs_M0\": {\"LR\": 68.56864172514634, \"df\": 1, \"p\": 1.2253722672182456e-16}, \"M3_vs_M1\": {\"LR\": 5.359129220855721, \"df\": 1, \"p\": 0.02061406421285374}, \"M2lost_vs_M0\": {\"LR\": 3.692783297256028, \"df\": 1, \"p\": 0.05464835230436948}}\n  auc_within_stratum : {...}\n    M0 : {\"mean\": 0.8091807114429179, \"ci\": [0.7984492331954763, 0.8199446379498353], \"n_strata\": 961}\n    M1 : {\"mean\": 0.8168958319192421, \"ci\": [0.8057138021898398, 0.8279266011380061], \"n_strata\": 961}\n    M2 : {\"mean\": 0.8165524635722822, \"ci\": [0.8053034495990403, 0.8271277315385243], \"n_strata\": 961}\n    M3 : {\"mean\": 0.8171354241891543, \"ci\": [0.8065784780635473, 0.8281377372847883], \"n_strata\": 961}\n    M2lost : {\"mean\": 0.810261363396254, \"ci\": [0.7991874850291205, 0.8208290627453392], \"n_strata\": 961}\n    a_phi_home : {\"mean\": 0.5727290857204159, \"ci\": [0.5578387354462705, 0.5876780151717319]}\n    b_log_size : {\"mean\": 0.7571468245335505, \"ci\": [0.7432796973034494, 0.7704361272290426]}\n    c_density : {\"mean\": 0.5899142713082878, \"ci\": [0.5732591975021303, 0.6066060690864565]}\n    e_gate_own : {\"mean\": 0.45019316994915887, \"ci\": [0.4311663719925003, 0.46976280708685747]}\n    d0_ret_rel : {\"mean\": 0.549637962338796, \"ci\": [0.5340511145365596, 0.5652085594964081]}\n    d_ret_gate : {\"mean\": 0.5473633955058406, \"ci\": [0.5306560075632085, 0.5648480644241015]}\n    d_lost_gate : {\"mean\": 0.49472626329764474, \"ci\": [0.48894987381107574, 0.5007125379232532]}\n  boot_d : {\"ci\": [0.2396221224886921, 0.3687710454858924], \"se_boot\": 0.033015692804543896, \"n_boot\": 2000, \"lr_boot\": [48.022073443692626, 61.10967415431014, 72.08327110710115, 83.74084928574189, 100.49796369752603]}\n  perm_null : {\"n\": 1000, \"lr_obs\": 71.71641463905598, \"p\": 0.000999000999000999, \"null_q\": [2.298605642513394, 12.855549758748566, 18.16931363961462, 29.754805871363185], \"null_mean\": 4.780875612062727}\n  gonly_perm_null_M3_vs_M1 : {\"n\": 1000, \"lr_obs\": 5.359129220855721, \"p\": 0.17282717282717283, \"null_q\": [1.2834225929473178, 7.377585618265675, 10.204503817493737, 16.23445376452073]}\n  rewired_null : {\"n\": 200, \"lr_obs\": 71.71641463905598, \"p\": 0.014925373134328358, \"null_q95\": 25.35432959295398, \"null_median\": 2.9273494794483668, \"real_gain_le_null95\": false}\nfrozen_dev_coef_auc : {\"M0\": {\"mean\": 0.8070954731216242, \"ci\": [0.7961158126587261, 0.8183723881714523]}, \"M2\": {\"mean\": 0.8151394525018186, \"ci\": [0.8041990479187258, 0.826213950278546]}}\nH2_per_group : {...}\n  Physical : {\"n_concepts\": 30, \"n_events\": 92, \"d\": 0.33190390712722606, \"se\": 0.16500811770727022, \"boot_ci\": [0.04639854869882769, 0.5654476789600625], \"LR\": {\"LR\": 3.9093621019801503, \"df\": 1, \"p\": 0.04801782006983559}}\n  LifeEnv : {\"n_concepts\": 34, \"n_events\": 118, \"d\": 0.1782552843878218, \"se\": 0.14439994076117874, \"boot_ci\": [-0.09589076212245926, 0.5057704115526264], \"LR\": {\"LR\": 1.4650246938848568, \"df\": 1, \"p\": 0.22613232849927772}}\n  Social : {\"n_concepts\": 53, \"n_events\": 161, \"d\": 0.24451473387184078, \"se\": 0.13045899284853288, \"boot_ci\": [-0.008413244223572947, 0.45936866022886264], \"LR\": {\"LR\": 3.1544382682966443, \"df\": 1, \"p\": 0.07572074814889966}}\n  MathDec : {\"n_concepts\": 0, \"status\": \"too few concepts\"}\n  Cohort : {\"n_concepts\": 248, \"n_events\": 989, \"d\": 0.2916284471668024, \"se\": 0.03815489939611666, \"boot_ci\": [0.2220069453650332, 0.36072498977180345], \"LR\": {\"LR\": 54.011853239082484, \"df\": 1, \"p\": 1.9928376965975005e-13}}\n  OtherHealth : {\"n_concepts\": 4, \"status\": \"too few concepts\"}\nH2_DL_pooled : {\"k\": 4, \"b\": 0.2835280026617289, \"se\": 0.03470316750295396, \"ci\": [0.21550979435593914, 0.35154621096751865], \"p\": 3.081594151322099e-16, \"tau2\": 0.0, \"Q\": 0.7519451573302255, \"I2\": 0.0}\nH2_sign_count : {\"positive\": 4, \"of\": 4, \"sign_test_p\": 0.0625}\nrescue_relay : {...}\n  n_episodes_rescue : 1158\n  n_with_crefs : 842\n  self_lineage_share_of_crefs : 0.10519544642174146\n  R1_resc : {...}\n    n : 798\n    n_clusters : 299\n    coef : {...}\n      R_cj : {\"b\": 0.38852569364632084, \"se\": 0.39023897328474455, \"ci\": [-0.37944763291803074, 1.1564990202106724], \"p\": 0.3202475697554218}\n      top : {\"b\": 0.01909155907054358, \"se\": 0.4360024337147479, \"ci\": [-0.8389422672068428, 0.87712538534793], \"p\": 0.9651029293969586}\n      mid : {\"b\": 0.9633910498619155, \"se\": 0.6355699029870214, \"ci\": [-0.28738287605494583, 2.2141649757787767], \"p\": 0.13063223797510137}\n      ret_x_top : {\"b\": -0.21735315531009167, \"se\": 0.45674733922987976, \"ci\": [-1.1162120533726436, 0.6815057427524602], \"p\": 0.6345144159626195}\n      ret_x_mid : {\"b\": -1.0177293371100564, \"se\": 0.6434385150994409, \"ci\": [-2.283988349430653, 0.2485296752105406], \"p\": 0.1147778716224225}\n      log_n_early_j : {\"b\": -0.08624172251707338, \"se\": 0.049833070874791476, \"ci\": [-0.1843110385838364, 0.011827593549689666], \"p\": 0.08455612886823587}\n      log_size_j : {\"b\": 0.028106313862865866, \"se\": 0.043445653151247765, \"ci\": [-0.05739284193513622, 0.11360546966086796], \"p\": 0.5181749715247372}\n  R1_s_other : {...}\n    n : 771\n    n_clusters : 293\n    coef : {...}\n      R_cj : {\"b\": 0.06712360174423884, \"se\": 0.0740060976389703, \"ci\": [-0.07852938326826248, 0.21277658675674016], \"p\": 0.3651541575300767}\n      top : {\"b\": 0.16551661816778138, \"se\": 0.10347768344491243, \"ci\": [-0.03814002576791542, 0.3691732621034782], \"p\": 0.1107822287376373}\n      mid : {\"b\": 0.17248988693390926, \"se\": 0.12328553359169941, \"ci\": [-0.07015101090251757, 0.4151307847703361], \"p\": 0.16284165483183574}\n      ret_x_top : {\"b\": -0.17545142139489972, \"se\": 0.10702679156804946, \"ci\": [-0.3860931410035342, 0.03519029821373479], \"p\": 0.10222301892631246}\n      ret_x_mid : {\"b\": -0.15874566208099233, \"se\": 0.12350673010560757, \"ci\": [-0.4018219015115977, 0.08433057734961305], \"p\": 0.19969900112687095}\n      log_n_early_j : {\"b\": -0.0673084966361899, \"se\": 0.00970044179644942, \"ci\": [-0.08640014379323283, -0.04821684947914698], \"p\": 2.5569003972296234e-11}\n      log_size_j : {\"b\": 0.013174078004924027, \"se\": 0.007947811511443924, \"ci\": [-0.0024681799696262188, 0.02881633597947427], \"p\": 0.09847759411792752}\n  R2_base : {...}\n    n : 796\n    n_clusters : 299\n    coef : {...}\n      gateway_j_z : {\"b\": 0.0035048673272817183, \"se\": 0.012249919915773514, \"ci\": [-0.02060244227502974, 0.027612176929593175], \"p\": 0.774989994377331}\n      log_size_j_z : {\"b\": 0.025640831896764058, \"se\": 0.011977282057607855, \"ci\": [0.002070061741347065, 0.04921160205218105], \"p\": 0.03310234470585825}\n      phi_home_j_z : {\"b\": 0.010543829789288393, \"se\": 0.011731474251922214, \"ci\": [-0.01254320129558184, 0.033630860874158626], \"p\": 0.36950386257045165}\n      P_generic_z : {\"b\": 0.013614651180878998, \"se\": 0.011672228864862855, \"ci\": [-0.009355787559047844, 0.036585089920805836], \"p\": 0.24437970902516926}\n      log_n_early_j_z : {\"b\": 0.03495919135960664, \"se\": 0.011399230658437636, \"ci\": [0.012526001216276266, 0.057392381502937004], \"p\": 0.0023621351335091573}\n  R2_full : {...}\n    n : 796\n    n_clusters : 299\n    coef : {...}\n      gateway_j_z : {\"b\": 0.0010352073546354614, \"se\": 0.013104471352531928, \"ci\": [-0.024753822307780927, 0.026824237017051847], \"p\": 0.9370884273384971}\n      log_size_j_z : {\"b\": 0.027348657981188088, \"se\": 0.012016135984518053, \"ci\": [0.0037014249875052183, 0.05099589097487096], \"p\": 0.023555800798093388}\n      phi_home_j_z : {\"b\": 0.010771187319659089, \"se\": 0.011570116459136267, \"ci\": [-0.011998298647024074, 0.03354067328634225], \"p\": 0.3526335482462065}\n      P_generic_z : {\"b\": 0.015392255294581157, \"se\": 0.011850742767790993, \"ci\": [-0.007929491042113256, 0.03871400163127557], \"p\": 0.1950018867588117}\n      log_n_early_j_z : {\"b\": 0.034641731926118455, \"se\": 0.011382528642215586, \"ci\": [0.012241410624283883, 0.05704205322795303], \"p\": 0.002547615240638964}\n      S_hanski_z : {\"b\": 0.008820136867130735, \"se\": 0.013231377080149659, \"ci\": [-0.017218637747662677, 0.034858911481924146], \"p\": 0.5055385608645725}\n      resc_z : {\"b\": 0.001417530898756781, \"se\": 0.013740972915265862, \"ci\": [-0.025624106155437244, 0.028459167952950806], \"p\": 0.9179046725641214}\n  R2_mediation : {\"indirect\": 0.002469659972646257, \"ci\": [-0.006968969233683165, 0.009824928788321549], \"share_mediated\": 0.7046372207651179, \"n\": 796, \"n_concepts\": 299}\n  H1_replication_all_episodes : {...}\n    n : 1153\n    n_clusters : 352\n    coef : {...}\n      gateway_j_z : {\"b\": 0.005335865553599093, \"se\": 0.01402195491154914, \"ci\": [-0.022241752024498306, 0.032913483131696494], \"p\": 0.7037774005826948}\n      log_size_j_z : {\"b\": -0.01449833901542563, \"se\": 0.013829603447381896, \"ci\": [-0.04169765020523032, 0.01270097217437906], \"p\": 0.29519623170228015}\n      phi_home_j_z : {\"b\": -0.0015415016212103531, \"se\": 0.012913289305013622, \"ci\": [-0.026938656039078687, 0.023855652796657977], \"p\": 0.9050479268554787}\n      P_generic_z : {\"b\": 0.0336290863048401, \"se\": 0.014339407879455377, \"ci\": [0.005427119511303452, 0.06183105309837675], \"p\": 0.019572160818219896}\n      log_n_early_j_z : {\"b\": 0.10195214219703702, \"se\": 0.012746930111238989, \"ci\": [0.07688217398504778, 0.12702211040902625], \"p\": 1.85274643337237e-14}\n  R3_incidence : {...}\n    top : [{\"S_bin\": 0, \"mean\": 0.8783783783783784, \"size\": 74}, {\"S_bin\": 1, \"mean\": 0.875, \"size\": 24}, {\"S_bin\": 2, \"mean\": 0.8875, \"size\": 80}, {\"S_bin\": 3, \"mean\": 0.8953488372093024, \"size\": 86}, {\"S_bin\": 4, \"mean\": 0.9363636363636364, \"size\": 110}]\n    mid : [{\"S_bin\": 0, \"mean\": 0.819672131147541, \"size\": 61}, {\"S_bin\": 1, \"mean\": 0.7368421052631579, \"size\": 57}, {\"S_bin\": 2, \"mean\": 0.8372093023255814, \"size\": 43}, {\"S_bin\": 3, \"mean\": 0.8985507246376812, \"size\": 69}, {\"S_bin\": 4, \"mean\": 0.8852459016393442, \"size\": 61}]\n    bottom : [{\"S_bin\": 0, \"mean\": 0.7319587628865979, \"size\": 97}, {\"S_bin\": 1, \"mean\": 0.7933333333333333, \"size\": 150}, {\"S_bin\": 2, \"mean\": 0.8256880733944955, \"size\": 109}, {\"S_bin\": 3, \"mean\": 0.8421052631578947, \"size\": 76}, {\"S_bin\": 4, \"mean\": 0.8524590163934426, \"size\": 61}]\n  relay_n_episodes : 1047\n  relay_fepois : {...}\n    n : 603\n    n_clusters : 158\n    coef : {...}\n      R_cj : {\"b\": 1.3705620877502105, \"se\": 0.5873899744219215, \"ci\": [0.21927773788324423, 2.5218464376171768], \"p\": 0.019631953611490813}\n      gateway_j : {\"b\": 2.30287798519301, \"se\": 1.8329880772022555, \"ci\": [-1.2897786461234109, 5.895534616509431], \"p\": 0.20898842615553015}\n      ret_x_gate : {\"b\": -1.299228378652143, \"se\": 1.8510381187891956, \"ci\": [-4.927263091478967, 2.32880633417468], \"p\": 0.482746676251148}\n      log_n_early_j : {\"b\": 0.551762254169844, \"se\": 0.053217249911844754, \"ci\": [0.4474564443426283, 0.6560680639970597], \"p\": 3.463094106664496e-25}\n      log_size_j : {\"b\": 0.009190258572963602, \"se\": 0.04726846386105869, \"ci\": [-0.08345593059471143, 0.10183644774063863], \"p\": 0.8458416671150077}\n  relay_fepois_offset : {...}\n    n : 603\n    n_clusters : 158\n    coef : {...}\n      R_cj : {\"b\": 1.3815906986711366, \"se\": 0.6409897236774432, \"ci\": [0.12525084026334787, 2.637930557078925], \"p\": 0.031130369719795752}\n      gateway_j : {\"b\": 2.7503516740263754, \"se\": 1.8734555438535576, \"ci\": [-0.9216211919265973, 6.422324539979348], \"p\": 0.1420869791867755}\n      ret_x_gate : {\"b\": -1.8338376682412123, \"se\": 1.8921082414102122, \"ci\": [-5.542369821405228, 1.8746944849228033], \"p\": 0.3324437341432048}\n      log_n_early_j : {\"b\": 0.02687878624210584, \"se\": 0.05360317995901218, \"ci\": [-0.07818344647755804, 0.1319410189617697], \"p\": 0.6160613937378052}\n      log_size_j : {\"b\": 0.007540118987296676, \"se\": 0.05232098085096346, \"ci\": [-0.09500900348059171, 0.11008924145518506], \"p\": 0.8854114585981927}\n  relay_excess_ols : {...}\n    n : 1047\n    n_clusters : 331\n    coef : {...}\n      R_cj : {\"b\": 0.03911132970160812, \"se\": 0.10531233645264693, \"ci\": [-0.1680568527564908, 0.246279512159707], \"p\": 0.710589774034475}\n      top : {\"b\": 0.12899433233331814, \"se\": 0.13751660761306353, \"ci\": [-0.14152540558752724, 0.3995140702541635], \"p\": 0.34891639522446793}\n      mid : {\"b\": -0.06351284391645245, \"se\": 0.11013793095698726, \"ci\": [-0.28017383297649673, 0.15314814514359182], \"p\": 0.5645579707828992}\n      ret_x_top : {\"b\": 0.28844243632525507, \"se\": 0.15855899173436303, \"ci\": [-0.023471430904979607, 0.6003563035554897], \"p\": 0.0697948274583471}\n      ret_x_mid : {\"b\": 0.23172087175221745, \"se\": 0.13893684095366965, \"ci\": [-0.041592718909441995, 0.505034462413877], \"p\": 0.09630114989245404}\n      log_n_early_j : {\"b\": -0.12834882527973734, \"se\": 0.03970628775814054, \"ci\": [-0.20645818781117217, -0.050239462748302516], \"p\": 0.0013512075590312797}\n      log_size_j : {\"b\": -0.023609656257050707, \"se\": 0.023011493815124864, \"ci\": [-0.06887737616438339, 0.021658063650281972], \"p\": 0.3056458468962577}\n  relay_excess_gateway_retained : {\"mean\": -0.010675926846191609, \"n\": 311, \"ci\": [-0.11093317578891297, 0.09376289940586639]}\n  relay_excess_by_cell : {...}\n     [{\"R_cj\": 0.0, \"gate_ter\": 0, \"mean\": -0.3467663164433726, \"size\": 82}, {\"R_cj\": 0.0, \"gate_ter\": 1, \"mean\": -0.1699127784089312, \"size\": 42}, {\"R_cj\": 0.0, \"gate_ter\": 2, \"mean\": -0.04126316964340203, \"size\": 34}, {\"R_cj\": 1.0, \"gate_ter\": 0, \"mean\": -0.24759655631623126, \"size\": 347}, {\"R_cj\": 1.0, \"gate_ter\": 1, \"mean\": -0.17465437131174266, \"size\": 231}, {\"R_cj\": 1.0, \"gate_ter\": 2, \"mean\": -0\ntrajectories : {...}\n  n_concepts_clustered : 188\n  n_intersection_born_O1 : 9\n  heldout_independent_recluster_ARI : 0.5361258296737231\n  cluster_sizes : [128, 60]\n  cluster_mean_series : {...}\n    0 : {...}\n      n_entered_offhome : [2.625, 3.609, 4.594, 5.516, 6.336, 7.25, 7.938, 8.523, 9.062]\n      n_retaining : [1.016, 1.445, 2.367, 3.195, 4.125, 4.82, 5.555, 6.32, 6.656]\n      n_lost : [0.141, 0.148, 0.109, 0.141, 0.211, 0.25, 0.344, 0.391, 0.516]\n      R20 : [4.288, 4.277, 4.315, 4.326, 4.386, 4.458, 4.49, 4.563, 4.583]\n      H : [1.089, 1.151, 1.19, 1.212, 1.242, 1.268, 1.283, 1.303, 1.308]\n      G_share : [0.154, 0.153, 0.154, 0.16, 0.163, 0.168, 0.171, 0.173, 0.174]\n      log_volume : [3.431, 3.879, 4.366, 4.62, 4.879, 5.024, 5.218, 5.324, 5.379]\n    1 : {...}\n      n_entered_offhome : [0.817, 1.467, 2.05, 2.683, 3.317, 3.667, 4.083, 4.533, 4.967]\n      n_retaining : [0.117, 0.25, 0.633, 1.167, 1.667, 2.167, 2.533, 2.683, 2.883]\n      n_lost : [0.05, 0.067, 0.067, 0.2, 0.233, 0.233, 0.467, 0.5, 0.567]\n      R20 : [2.112, 2.18, 2.262, 2.336, 2.364, 2.376, 2.327, 2.351, 2.345]\n      H : [0.305, 0.336, 0.377, 0.403, 0.409, 0.415, 0.413, 0.421, 0.424]\n      G_share : [0.024, 0.023, 0.025, 0.029, 0.031, 0.033, 0.033, 0.036, 0.037]\n      log_volume : [3.436, 3.869, 4.216, 4.337, 4.493, 4.548, 4.693, 4.769, 4.821]\n  cluster_by_group : {\"0\": {\"DEV_BGM\": 9, \"DEV_CS\": 9, \"DEV_Eng\": 20, \"DEV_Med\": 14, \"LifeEnv\": 26, \"OtherHealth\": 4, \"Physical\": 21, \"Social\": 25}, \"1\": {\"DEV_BGM\": 0, \"DEV_CS\": 0, \"DEV_Eng\": 5, \"DEV_Med\": 42, \"LifeEnv\": 4, \"OtherHealth\": 0, \"Physical\": 4, \"Social\": 5}}\n  cluster_outcomes : {\"O2r_m30\": {\"0\": 5.214, \"1\": 2.772}, \"O3\": {\"0\": 0.0, \"1\": 0.0}}\n  hmm : {\"n_states\": 6, \"note\": \"refit with the frozen number of states\"}\n  hmm_vs_dtw_ARI : 0.09450482650930404\n  hmm_top_paths : {\"4-1\": 28, \"0-5\": 22, \"4-0\": 20, \"0\": 16, \"0-3-0\": 14, \"4\": 13, \"0-3\": 12, \"4-2\": 10}\nordering : {...}\n  n_top_o2r : 175\n  n_tau_detected : 112\n  share_tau_detected : 0.64\n  gateway : {\"n_evaluable\": 102, \"before\": 57, \"ties\": 15, \"after\": 30, \"share_before_excl_ties\": 0.6551724137931034, \"sign_test_p_one_sided\": 0.002506799450073193}\n  peripheral : {\"n_evaluable\": 106, \"before\": 49, \"ties\": 20, \"after\": 37, \"share_before_excl_ties\": 0.5697674418604651, \"sign_test_p_one_sided\": 0.1176899311055276}\n  mcnemar : {\"n\": 96, \"gw_only\": 27, \"per_only\": 15, \"p_exact_two_sided\": 0.08842954698775429}\n  lead_lag : {...}\n    forward_dH_on_ret : {...}\n      n : 2992\n      n_clusters : 374\n      coef : {...}\n         {\"ret_gw\": {\"b\": -0.027939583860173887, \"se\": 0.008204208218249505, \"ci\": [-0.04407188190382086, -0.01180728581652692], \"p\": 0.000732210852919447}, \"ret_per\": {\"b\": -0.04343494312087125, \"se\": 0.007849909752178485, \"ci\": [-0.058870568396224655, -0.02799931784551784], \"p\": 5.932942018418449e-08}, \"log_volume\": {\"b\": 0.005328277222836092, \"se\": 0.007952743025281716, \"ci\": [-0.01030955367265442, 0.02\n    reverse_dret_on_H : {\"n\": 2992, \"n_clusters\": 374, \"coef\": {\"H\": {\"b\": 0.07673151369679986, \"se\": 0.06208029407404087, \"ci\": [-0.04533971852911299, 0.1988027459227127], \"p\": 0.21723474575636884}, \"log_volume\": {\"b\": 0.03360839787610011, \"se\": 0.017894361869245357, \"ci\": [-0.0015780785389428453, 0.06879487429114306], \"p\": 0.061139753313223445}}}\n    event_study_H : {...}\n      n : 3366\n      n_clusters : 374\n      coef : {...}\n         {\"ev-3\": {\"b\": -0.07165074712879511, \"se\": 0.019136067623735615, \"ci\": [-0.10927884457307889, -0.03402264968451134], \"p\": 0.00020946833860825537}, \"ev-2\": {\"b\": -0.020413161362236098, \"se\": 0.011415313387750887, \"ci\": [-0.04285959774389622, 0.002033275019424026], \"p\": 0.0745510803558018}, \"ev+0\": {\"b\": 0.03088760394610438, \"se\": 0.009249548268737173, \"ci\": [0.012699807455463317, 0.0490754004367454\n    n_treated : 296\n    n_concepts : 374\n  lead_lag_placebo : {\"n\": 200, \"obs\": -0.027939583860173887, \"null_q\": [-0.05375937043065577, -0.031892037361457834, -0.0084208680648549], \"p_two_sided\": 0.6268656716417911}\ndecisions : {...}\n  H2_entry : {\"LR_p<0.01\": true, \"d>0_CI>0\": true, \"field_groups_positive>=3_of_3\": true, \"cohort_positive\": true, \"perm_p<0.05\": true, \"rewired_gain_above_null95\": true, \"CONFIRMED\": true}\n  H2_ordering : {\"p_gw\": 0.6551724137931034, \"sign_p\": 0.002506799450073193, \"peripheral_share\": 0.5697674418604651, \"CONFIRMED\": true}\n  RESCUE : {\"R1_interaction\": -0.21735315531009167, \"R1_ci\": [-1.1162120533726436, 0.6815057427524602], \"indirect\": 0.002469659972646257, \"indirect_ci\": [-0.006968969233683165, 0.009824928788321549], \"SUPPORTED\": false}\n  RELAY : {\"fepois_ret_x_gate\": -1.299228378652143, \"ci\": [-4.927263091478967, 2.32880633417468], \"mean_excess_gw_retained\": -0.010675926846191609, \"SUPPORTED\": false}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-28 20:56:49 UTC

```
Check density definition and dev trajectory results:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; grep -n "density" config.py method.py lib/*.py 2>/dev/null | head -30; python3 -c "
import json
d=json.load(open('results/dev_result.json'))
print(list(d.keys()))
t=d.get('trajectories',{}); print(json.dumps({k:v for k,v in t.items() if k!='cluster_mean_series'})[:2500])
"
```

### [13] TOOL RESULT — Bash · 2026-09-28 20:56:49 UTC

```
{"stdout": "lib/h2.py:14:REG = [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\"]\nlib/h2.py:15:MODELS = {\"M0\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\"],\nlib/h2.py:16:          \"M1\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\"],\nlib/h2.py:17:          \"M2\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d_ret_gate\"],\nlib/h2.py:18:          \"M3\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\"],\nlib/h2.py:19:          \"M2lost\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d_lost_gate\"]}\nlib/h2.py:80:    df = pd.DataFrame(rows, columns=[\"cidx\", \"t\", \"age\", \"field\", \"entered\", \"a_phi_home\", \"b_log_size\", \"c_density\",\nmethod.py:3:relatedness-to-home / size / Hidalgo density / own centrality), rescue, relay, trajectories and ordering.\nmethod.py:37:REGS = [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\", \"d_lost_gate\"]\nmethod.py:144:    X = dfs[[\"a_phi_home\", \"b_log_size\", \"c_density\", \"d_ret_gate\"]].to_numpy()\nmethod.py:146:               [\"a_phi_home\", \"b_log_size\", \"c_density\", \"d_ret_gate\"])\nmethod.py:431:    res[\"H2\"][\"size_vs_density_auc\"] = {\"size\": h[\"auc_within_stratum\"][\"b_log_size\"][\"mean\"],\nmethod.py:432:                                        \"density\": h[\"auc_within_stratum\"][\"c_density\"][\"mean\"]}\nmethod.py:482:                           \"c_density\": \"Hidalgo density sum_{j in entered(t-1)} phi[j,k] / sum_j phi[j,k]\",\n['n_dev_concepts_newborn', 'n_dev_episodes', 'dev_by_group', 'H2', 'H2_robustness', 'T0_planted_control', 'power_check', 'rescue_relay', 'trajectories', 'ordering']\n{\"n_concepts_clustered\": 128, \"n_intersection_born_O1\": 8, \"k_selection\": {\"grid\": {\"2\": {\"silhouette\": 0.2861415089076136, \"ari_median\": 1.0, \"ari_p10\": 0.8116927188209622, \"sizes\": [66, 62]}, \"3\": {\"silhouette\": 0.2258039518058049, \"ari_median\": 0.8036797714946194, \"ari_p10\": 0.5259573292021631, \"sizes\": [57, 49, 22]}, \"4\": {\"silhouette\": 0.202722742726286, \"ari_median\": 0.6662017097351829, \"ari_p10\": 0.39283032543398555, \"sizes\": [43, 45, 21, 19]}, \"5\": {\"silhouette\": 0.21161193116234628, \"ari_median\": 0.5421718177380617, \"ari_p10\": 0.39468133210546213, \"sizes\": [9, 47, 19, 20, 33]}, \"6\": {\"silhouette\": 0.10979835744005363, \"ari_median\": 0.4134477915536616, \"ari_p10\": 0.3389965601096043, \"sizes\": [10, 22, 19, 22, 24, 31]}, \"7\": {\"silhouette\": 0.1565681465018802, \"ari_median\": 0.47359610897176335, \"ari_p10\": 0.35694478920504635, \"sizes\": [10, 27, 15, 22, 23, 4, 27]}, \"8\": {\"silhouette\": 0.1616426930592681, \"ari_median\": 0.4684852707224122, \"ari_p10\": 0.33884783071562, \"sizes\": [24, 27, 15, 19, 22, 4, 7, 10]}}, \"k\": 2, \"flag\": \"stable\"}, \"cluster_sizes\": [66, 62], \"cluster_by_group\": {\"0\": {\"DEV_BGM\": 18, \"DEV_CS\": 6, \"DEV_Eng\": 20, \"DEV_Med\": 22}, \"1\": {\"DEV_BGM\": 0, \"DEV_CS\": 0, \"DEV_Eng\": 7, \"DEV_Med\": 55}}, \"cluster_outcomes\": {\"O2r_m30\": {\"0\": 4.758, \"1\": 2.782}, \"O3\": {\"0\": 0.0, \"1\": 0.0}}, \"hmm\": {\"n_states\": 6, \"bic_grid\": {\"2\": {\"ll\": -9007.948300462862, \"bic\": 18234.423501004654}, \"3\": {\"ll\": -4911.451516878343, \"bic\": 10175.365775819477}, \"4\": {\"ll\": -4400.168089211037, \"bic\": 9300.833272151238}, \"5\": {\"ll\": -3255.6733565078994, \"bic\": 7173.976668093847}, \"6\": {\"ll\": -2886.012354655563, \"bic\": 6610.88603542057}}, \"state_means\": [[-1.0458341238429134, -0.988219802265486, -0.3939789311157717, -0.9878313889563414, -1.0565134794164555, -0.718607204010742, -0.5749831685777468], [-0.07141884553041271, 0.019972330844150468, -0.39397893111577176, -0.8152832176808382, -0.8936046668904645, -0.7259843788845693, 0.6490794424579294], [0.7896301896445623, 0.6678040481964306, 0.8317910214988998, 1.3354064697600119, 1.3258777203117553, 1.8059045472944242, -0.08299498744633806], [2.6076580089256662, 2.462830098383911, 0.9494967669695865, 1.7964149489994652, 1.7407606583302189, 1.3590667891373152, 1.1965454791666739], [-0.14203308517385257, -0.3677119139578239, 2.106406393358538, -0.4101728121877721, -0.44124234900221615, -0.47961898319487817, -0.3738596617123762], [0.087933420323446, 0.12026223987499605, -0.39397893111577154, 0.2930175219381583, 0.3617004746785", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-28 20:57:03 UTC

```
Inspect lead-lag regression definitions and results:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; grep -n "forward_dH_on_ret\|reverse_dret_on_H\|event_study_H\|ret_gw\|dH" method.py lib/*.py | head -30; python3 -c "
import json
d=json.load(open('results/heldout_result.json'))
print(json.dumps(d['ordering']['lead_lag']['event_study_H'])[:1500])
d=json.load(open('results/dev_result.json'));print(json.dumps(d['ordering'])[:2500])"
```

### [15] TOOL RESULT — Bash · 2026-09-28 20:57:03 UTC

```
{"stdout": "method.py:388:        # recompute ret_gw from the per-year retaining sets\nmethod.py:389:        P2[\"ret_gw\"] = P2[\"_ret\"].map(lambda r: int((np.asarray(r) & topp).sum()))\nmethod.py:391:        coefs.append(ll[\"forward_dH_on_ret\"][\"coef\"][\"ret_gw\"][\"b\"])\nmethod.py:392:    obs = out[\"lead_lag\"][\"forward_dH_on_ret\"][\"coef\"][\"ret_gw\"][\"b\"]\nlib/traj.py:33:                     \"ret_gw\": int((S[\"retaining\"][ti] & top).sum()), \"ret_per\": int((S[\"retaining\"][ti] & bot).sum())})\nlib/traj.py:161:        gw = d[d.ret_gw > 0].t; pe = d[d.ret_per > 0].t\nlib/traj.py:188:    P[\"dH_next\"] = P.groupby(\"cidx\").H.shift(-1) - P.H\nlib/traj.py:189:    P[\"dret_gw_next\"] = P.groupby(\"cidx\").ret_gw.shift(-1) - P.ret_gw\nlib/traj.py:190:    P[\"ret_gw_i\"] = (P.ret_gw > 0).astype(float); P[\"ret_per_i\"] = (P.ret_per > 0).astype(float)\nlib/traj.py:191:    ok = P.dH_next.notna()\nlib/traj.py:193:    fwd = fe_ols(d.dH_next.to_numpy(), d[[\"ret_gw_i\", \"ret_per_i\", \"log_volume\"]].to_numpy(),\nlib/traj.py:194:                 [d.cidx.to_numpy(), d.age.to_numpy()], d.cidx.to_numpy(), [\"ret_gw\", \"ret_per\", \"log_volume\"])\nlib/traj.py:195:    rev = fe_ols(d.dret_gw_next.to_numpy(), d[[\"H\", \"log_volume\"]].to_numpy(), [d.cidx.to_numpy(), d.age.to_numpy()],\nlib/traj.py:198:    first = P[P.ret_gw > 0].groupby(\"cidx\").t.min()\nlib/traj.py:215:    return {\"forward_dH_on_ret\": fwd, \"reverse_dret_on_H\": rev, \"event_study_H\": es,\n{\"n\": 3366, \"n_clusters\": 374, \"coef\": {\"ev-3\": {\"b\": -0.07165074712879511, \"se\": 0.019136067623735615, \"ci\": [-0.10927884457307889, -0.03402264968451134], \"p\": 0.00020946833860825537}, \"ev-2\": {\"b\": -0.020413161362236098, \"se\": 0.011415313387750887, \"ci\": [-0.04285959774389622, 0.002033275019424026], \"p\": 0.0745510803558018}, \"ev+0\": {\"b\": 0.03088760394610438, \"se\": 0.009249548268737173, \"ci\": [0.012699807455463317, 0.04907540043674544], \"p\": 0.0009243786662947714}, \"ev+1\": {\"b\": 0.024203100335321595, \"se\": 0.013538632303749923, \"ci\": [-0.0024185120881185206, 0.050824712758761714], \"p\": 0.07463508094789233}, \"ev+2\": {\"b\": 0.022215925553030993, \"se\": 0.017960539555128174, \"ci\": [-0.013100678977254775, 0.05753253008331676], \"p\": 0.21689136348740207}, \"ev+3\": {\"b\": 0.02901143152813532, \"se\": 0.024111723298910783, \"ci\": [-0.018400518078254584, 0.07642338113452522], \"p\": 0.2296587478544001}, \"log_volume\": {\"b\": 0.0262226192119209, \"se\": 0.010619276597886787, \"ci\": [0.005341465232434579, 0.047103773191407225], \"p\": 0.013983293491331745}}}\n{\"calibration\": {\"pen\": 4.5, \"far_grid\": {\"0.5\": 0.86, \"0.75\": 0.815, \"1.0\": 0.745, \"1.25\": 0.64, \"1.5\": 0.59, \"1.75\": 0.5, \"2.0\": 0.39, \"2.25\": 0.35, \"2.5\": 0.295, \"2.75\": 0.265, \"3.0\": 0.23, \"3.25\": 0.185, \"3.5\": 0.125, \"3.75\": 0.085, \"4.0\": 0.06, \"4.25\": 0.055, \"4.5\": 0.045, \"4.75\": 0.045, \"5.0\": 0.035, \"5.25\": 0.025, \"5.5\": 0.02, \"5.75\": 0.015, \"6.0\": 0.01, \"6.5\": 0.005, \"8.0\": 0.0, \"9.5\": 0.0, \"11.0\": 0.0, \"12.5\": 0.0, \"14.0\": 0.0, \"15.5\": 0.0, \"17.0\": 0.0, \"18.5\": 0.0, \"20.0\": 0.0}, \"far_fresh\": 0.05}, \"n_top_o2r\": 91, \"n_tau_detected\": 50, \"share_tau_detected\": 0.5494505494505495, \"gateway\": {\"n_evaluable\": 45, \"before\": 30, \"ties\": 3, \"after\": 12, \"share_before_excl_ties\": 0.7142857142857143, \"sign_test_p_one_sided\": 0.003957948667448363}, \"peripheral\": {\"n_evaluable\": 44, \"before\": 26, \"ties\": 7, \"after\": 11, \"share_before_excl_ties\": 0.7027027027027027, \"sign_test_p_one_sided\": 0.010036925959866494}, \"mcnemar\": {\"n\": 39, \"gw_only\": 7, \"per_only\": 3, \"p_exact_two_sided\": 0.34375}, \"lead_lag\": {\"forward_dH_on_ret\": {\"n\": 2232, \"n_clusters\": 279, \"coef\": {\"ret_gw\": {\"b\": -0.040196727831825006, \"se\": 0.009720701026672796, \"ci\": [-0.059332258060155886, -0.021061197603494126], \"p\": 4.7018995494830635e-05}, \"ret_per\": {\"b\": -0.042968634253269335, \"se\": 0.007289833289186943, \"ci\": [-0.057318918752501155, -0.028618349754037514], \"p\": 1.086911527205257e-08}, \"log_volume\": {\"b\": 0.001790217777050994, \"se\": 0.0072104849297599674, \"ci\": [-0.012403866780816817, 0.015984302334918807], \"p\": 0.8041012255670422}}}, \"reverse_dret_on_H\": {\"n\": 2232, \"n_clusters\": 279, \"coef\": {\"H\": {\"b\": 0.2318238205025538, \"se\": 0.08409868345458633, \"ci\": [0.0662727048996404, 0.39737493610546715], \"p\": 0.006227599872461201}, \"log_volume\": {\"b\": 0.06875437291390774, \"se\": 0.022048318195237355, \"ci\": [0.025351509462892587, 0.11215723636492289], \"p\": 0.002009566739489137}}}, \"event_study_H\": {\"n\": 2511, \"n_clusters\": 279, \"coef\": {\"ev-3\": {\"b\": -0.08833206299233691, \"se\": 0.019085645104497038, \"ci\": [-0.12590280380847574, -0.050761322176198075], \"p\": 5.664977848158367e-06}, \"ev-2\": {\"b\": -0.0190013263830731, \"se\": 0.011009862279424224, \"ci\": [-0.040674614336235634, 0.002671961570089431], \"p\": 0.08548625499112437}, \"ev+0\": {\"b\": 0.025242715059806027, \"se\": 0.009603598322645412, \"ci\": [0.006337705482875357, 0.0441477246367367], \"p\": 0.009054048775242778}, \"ev+1\": {\"b\": -0.0002176693972625959, \"se\": 0.01243767640203529, \"ci\": [-0.02470165796025692, 0.024266319165731732], \"p\": 0.986049641", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] THINKING · 2026-09-28 20:57:11 UTC

```
I found several discrepancies in Experiments 5 and 6, including issues with the lead-lag regression signs and an omitted pre-trend. Now I'll check Evaluation 1 and the Iteration-1 corrections.
```

### [17] TOOL CALL — Bash · 2026-09-28 20:57:11 UTC

```
Check the 12-indicator partial association file in Exp3:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; ls results | head; python3 -c "
import json
d=json.load(open('results/exploratory_partial_association.json'))
print(json.dumps(d)[:3000])"; grep -rn "0.037\|permutation" results/*.json 2>/dev/null | head -5
```

### [18] TOOL RESULT — Bash · 2026-09-28 20:57:11 UTC

```
{"stdout": "audit.json\nbackbone_summary.json\ncredit_ledger.json\ndeviations.json\nexploratory_partial_association.json\nfeatures.csv\nfeatures_ego.csv\nfield_features.csv\nfield_names.csv\nfield_outcomes.csv\n{\"label\": \"EXPLORATORY, not pre-registered; not used for selection\", \"statistic\": \"LOGO out-of-group partial Spearman (candidate and O2r residualised on B5, train-fold OLS)\", \"n\": 47, \"n_boot\": 2000, \"candidates\": {\"D_ratio\": {\"logo_partial_rho\": 0.3354301572617946, \"CI90\": [0.018948440361753322, 0.6477704815957838], \"CI95\": [-0.058800896420754485, 0.687840097862216], \"per_group\": {\"BIO\": 0.5441176470588236, \"CS\": 0.25874125874125875, \"ENG\": -0.06666666666666667, \"MED\": 0.5833333333333334}, \"n_groups_positive\": 3, \"in_sample_partial_rho_given_B5\": 0.46493987049028673, \"delta_rho_robustness\": {\"in_sample_delta_rho\": 0.01628122109158192, \"logo_delta_rho_rank_features\": 0.01751464693185334, \"logo_delta_rho_alpha10\": 0.02429848905334575}}, \"D_rare\": {\"logo_partial_rho\": 0.3113460183227625, \"CI90\": [-0.034490950921292465, 0.6526579451244885], \"CI95\": [-0.1011025944673588, 0.6916179035984182], \"per_group\": {\"BIO\": 0.6263736263736264, \"CS\": -0.006993006993006993, \"ENG\": 0.3666666666666667, \"MED\": 0.6666666666666667}, \"n_groups_positive\": 3, \"in_sample_partial_rho_given_B5\": 0.5045806906272022, \"delta_rho_robustness\": {\"in_sample_delta_rho\": 0.05877378435517977, \"logo_delta_rho_rank_features\": 0.05694150810429888, \"logo_delta_rho_alpha10\": 0.03974630021141656}}, \"D_z\": {\"logo_partial_rho\": 0.3132284921369103, \"CI90\": [-0.08704635239022043, 0.5799076552231304], \"CI95\": [-0.16107242047106546, 0.6336646581654795], \"per_group\": {\"BIO\": 0.09117647058823529, \"CS\": 0.2517482517482518, \"ENG\": 0.5166666666666667, \"MED\": 0.7666666666666667}, \"n_groups_positive\": 4, \"in_sample_partial_rho_given_B5\": 0.21763798951588037, \"delta_rho_robustness\": {\"in_sample_delta_rho\": -0.0033302497687328625, \"logo_delta_rho_rank_features\": 0.0340425531914893, \"logo_delta_rho_alpha10\": 0.02614862781375271}}, \"D_sub\": {\"logo_partial_rho\": 0.24477335800185013, \"CI90\": [-0.09217554833352286, 0.5882462665149835], \"CI95\": [-0.1618255769734335, 0.6336417035994261], \"per_group\": {\"BIO\": 0.19117647058823528, \"CS\": 0.3216783216783217, \"ENG\": 0.45, \"MED\": 0.06666666666666667}, \"n_groups_positive\": 4, \"in_sample_partial_rho_given_B5\": 0.36947271045328395, \"delta_rho_robustness\": {\"in_sample_delta_rho\": 0.021954979956830045, \"logo_delta_rho_rank_features\": 0.05834104224483516, \"logo_delta_rho_alpha10\": 0.044650015417822986}}, \"NOV_res\": {\"logo_partial_rho\": 0.2810360777058279, \"CI90\": [-0.11369437953332881, 0.5813210317708407], \"CI95\": [-0.190450023398842, 0.6393068124929444], \"per_group\": {\"BIO\": 0.5676470588235295, \"CS\": -0.3356643356643357, \"ENG\": -0.11666666666666665, \"MED\": 0.65}, \"n_groups_positive\": 2, \"in_sample_partial_rho_given_B5\": 0.4233734196731422, \"delta_rho_robustness\": {\"in_sample_delta_rho\": 0.049337033610854175, \"logo_delta_rho_rank_features\": 0.004070305272895647, \"logo_delta_rho_alpha10\": -0.0392229417206289}}, \"participation\": {\"logo_partial_rho\": 0.3223866790009251, \"CI90\": [-0.03742811744620712, 0.6398722295284989], \"CI95\": [-0.11547575078900707, 0.6897617307678892], \"per\nresults/audit.json:84:   \"logvol\": 0.037022397891963106,\nresults/audit.json:111:  \"perm_p_value_one_sided\": 0.037,\nresults/exploratory_partial_association.json:130:    -0.03742811744620712,\nresults/screen_result_seed2.json:144:   \"rho_logvol\": 0.037022397891963106,\nresults/screen_result_seed2.json:199:     0.05037212283582515", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-09-28 20:57:19 UTC

```
List all 12 partials and Evaluation 1 summary:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; python3 -c "
import json
d=json.load(open('results/exploratory_partial_association.json'))
for k,v in d['candidates'].items(): print(k, round(v['logo_partial_rho'],3), [round(x,3) for x in v['CI90']], [round(x,3) for x in v['CI95']], v['n_groups_positive'])
print(len(d['candidates']))
"; cd ../../../iter_2/gen_art/gen_art_evaluation_1; ls results figures prereg; python3 -c "
import json
d=json.load(open('results/summary.json')); print(json.dumps(d)[:4000])"
```

### [20] TOOL RESULT — Bash · 2026-09-28 20:57:21 UTC

```
{"stdout": "D_ratio 0.335 [0.019, 0.648] [-0.059, 0.688] 3\nD_rare 0.311 [-0.034, 0.653] [-0.101, 0.692] 3\nD_z 0.313 [-0.087, 0.58] [-0.161, 0.634] 4\nD_sub 0.245 [-0.092, 0.588] [-0.162, 0.634] 4\nNOV_res 0.281 [-0.114, 0.581] [-0.19, 0.639] 2\nparticipation 0.322 [-0.037, 0.64] [-0.115, 0.69] 3\nn_comm_W3 0.218 [-0.073, 0.585] [-0.153, 0.627] 2\nF_res -0.267 [-0.443, 0.249] [-0.492, 0.324] 1\nF_z -0.248 [-0.451, 0.28] [-0.509, 0.353] 1\nF_bg -0.301 [-0.516, 0.187] [-0.56, 0.254] 2\ndeg_growth 0.05 [-0.413, 0.309] [-0.466, 0.381] 1\nbtw_change -0.168 [-0.449, 0.335] [-0.514, 0.4] 1\n12\nfigures:\nforest_delta_auc.pdf\nforest_delta_auc.png\nmde_vs_n.pdf\nmde_vs_n.png\nplacebo_hist.pdf\nplacebo_hist.png\nstage2_field_intercepts.pdf\nstage2_field_intercepts.png\n\nprereg:\ncrosswalk.json\nverdict_ladder.json\n\nresults:\naudit_out.json\ncache\nsummary.json\nunion_episodes.csv\n{\"verdict\": \"FAILS\", \"conditions\": {\"new_eps_delta_gt_0\": false, \"union_delta_gt_0_ci95_gt_0\": false, \"new_eps_delta_gt_0_ci95_gt_0\": false, \"union_ge3of4_groups_positive\": false, \"survives_P_within_union_ci95_gt_0\": false, \"above_C2_p95_union\": false, \"P_alone_carries_gain_union\": false, \"gateway_adds_le_0.01_given_P_union\": true, \"inside_C2_null_union\": true}, \"headline\": {\"exp4\": {\"delta\": 0.037460317460317416, \"auc_base\": 0.7695238095238095, \"auc_cand\": 0.8069841269841269, \"n_groups_positive\": 4, \"ci95\": [-0.018236774105807162, 0.13]}, \"exp1\": {\"delta\": 0.0006157635467980427, \"auc_base\": 0.8151888341543514, \"auc_cand\": 0.8158045977011494, \"n_groups_positive\": 2, \"ci95\": [-0.020989173263663095, 0.009461192810457559]}, \"exp1_clean\": {\"delta\": -0.005429292929292839, \"auc_base\": 0.7906565656565656, \"auc_cand\": 0.7852272727272728, \"n_groups_positive\": 1, \"ci95\": [-0.03189873153191621, 0.020575007158584874]}, \"exp3\": {\"delta\": -0.005747126436781658, \"auc_base\": 0.7558839627805145, \"auc_cand\": 0.7501368363437328, \"n_groups_positive\": 1, \"ci95\": [-0.051600205198358354, 0.07001736111111106]}, \"union\": {\"delta\": 0.00087029045944087, \"auc_base\": 0.7285419008594118, \"auc_cand\": 0.7294121913188527, \"n_groups_positive\": 1, \"ci95\": [-0.012079717600047765, 0.012000159257471185]}, \"new_eps\": {\"delta\": -0.0006496881496881324, \"auc_base\": 0.7383056133056133, \"auc_cand\": 0.7376559251559252, \"n_groups_positive\": 3, \"ci95\": [-0.02110277179705331, 0.017419970380496586]}, \"union_agree\": {\"delta\": 0.00020161290322584513, \"auc_base\": 0.7544354838709677, \"auc_cand\": 0.7546370967741935, \"n_groups_positive\": 1, \"ci95\": [-0.019194966924750815, 0.008286310396220223]}}}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-28 20:57:27 UTC

```
Search Evaluation 1 output for refit, power and residual results:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1; python3 -c "
import json
d=json.load(open('eval_out.json'))
m=d.get('metadata',d)
print(list(m.keys()))
def find(o,key,path=''):
  if isinstance(o,dict):
    for k,v in o.items():
      if key.lower() in k.lower(): print(path+'/'+k, json.dumps(v)[:700])
      find(v,key,path+'/'+k)
  elif isinstance(o,list):
    for i,v in enumerate(o[:50]): find(v,key,path+f'[{i}]')
for k in ['resid','F5','refit','power','icc','mde']: print('--',k); find(m,k)
" | head -80
```

### [22] TOOL RESULT — Bash · 2026-09-28 20:57:27 UTC

```
{"stdout": "['evaluation_name', 'description', 'unit', 'ci_convention', 'prereg', 'reproduction', 'harmonisation_checks', 'overlap', 'A_replication', 'B_trait', 'C_placebo', 'D_O1_artefact', 'E_power', 'F_record', 'verdict', 'missing_inputs', 'deviations', 'figures', 'runtime_s']\n-- resid\n-- F5\n/F_record/F5_exp4_field_level {\"ci_convention\": \"iter-1: fixed-prediction concept bootstrap 95%; new: concept-clustered REFIT bootstrap 95%\", \"feature_lists\": {\"all_four_available\": {\"base\": [\"b_logn\", \"b_growth\", \"b_share\"], \"cand\": [\"b_logn\", \"b_growth\", \"b_share\", \"gateway_j\", \"phi_home_j\", \"density_j\"]}, \"size_controlled_all_three\": {\"base\": [\"b_logn\", \"b_growth\", \"b_share\", \"log_field_size\"], \"cand\": [\"b_logn\", \"b_growth\", \"b_share\", \"log_field_size\", \"gateway_j\", \"phi_home_j\", \"density_j\"]}, \"gateway_j\": {\"base\": [\"b_logn\", \"b_growth\", \"b_share\"], \"cand\": [\"b_logn\", \"b_growth\", \"b_share\", \"gateway_j\"]}, \"size_controlled_gateway_j\": {\"base\": [\"b_logn\", \"b_growth\", \"b_share\", \"log_field_size\"], \"cand\": [\"b_logn\", \"b_\n-- refit\n/A_replication/exp4/specs/M0/refit_boot {\"n\": 2000, \"sd\": 0.044717864638280286, \"ci90\": [0.037157454277019504, 0.17882798573975045], \"ci95\": [0.024652053408572808, 0.19707972582972585], \"p_le0\": 0.005, \"p_two_sided\": 0.01, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/M1/refit_boot {\"n\": 2000, \"sd\": 0.050720216402520245, \"ci90\": [0.009150087097175725, 0.16756306018737985], \"ci95\": [-0.0038261805252323283, 0.18702096734289952], \"p_le0\": 0.0305, \"p_two_sided\": 0.061, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/M2/refit_boot {\"n\": 2000, \"sd\": 0.038515989996643664, \"ci90\": [-0.010651064773735718, 0.11112077294686004], \"ci95\": [-0.018236774105807162, 0.13], \"p_le0\": 0.1065, \"p_two_sided\": 0.213, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/M2+P/refit_boot {\"n\": 2000, \"sd\": 0.02580865819814689, \"ci90\": [-0.013164451827242457, 0.0697580312407898], \"ci95\": [-0.01886829565191584, 0.08543507146448315], \"p_le0\": 0.1685, \"p_two_sided\": 0.337, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/P_alone/refit_boot {\"n\": 2000, \"sd\": 0.06387414163580891, \"ci90\": [-0.13069995164410067, 0.08323118279569894], \"ci95\": [-0.15000364431486882, 0.10637035138240468], \"p_le0\": 0.63, \"p_two_sided\": 0.743, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/M2+Ppool/refit_boot {\"n\": 2000, \"sd\": 0.03474389265500624, \"ci90\": [-0.008241165343498223, 0.10051952172274993], \"ci95\": [-0.01686306063122931, 0.11830894510582016], \"p_le0\": 0.0955, \"p_two_sided\": 0.191, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/Ppool_alone/refit_boot {\"n\": 2000, \"sd\": 0.03691683638868385, \"ci90\": [-0.11744278331487645, 0.0027183206447391464], \"ci95\": [-0.1365505805683283, 0.015147965743099385], \"p_le0\": 0.941, \"p_two_sided\": 0.123, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/rival:r_strength/refit_boot {\"n\": 2000, \"sd\": 0.03332310590547106, \"ci90\": [-0.04862058864074997, 0.05750246305418719], \"ci95\": [-0.056531319290465745, 0.07612119013062396], \"p_le0\": 0.5845, \"p_two_sided\": 0.847, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/rival:r_degree/refit_boot {\"n\": 2000, \"sd\": 0.031945578452715916, \"ci90\": [-0.05947764820213803, 0.041672192749778916], \"ci95\": [-0.06884425896336162, 0.06134878193701717], \"p_le0\": 0.7635, \"p_two_sided\": 0.484, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/rival:r_betweenness/refit_boot {\"n\": 2000, \"sd\": 0.03463262784139228, \"ci90\": [-0.030651469098277696, 0.07659390159390157], \"ci95\": [-0.04481481062491519, 0.09192617976725916], \"p_le0\": 0.2465, \"p_two_sided\": 0.493, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/rival:r_pagerank/refit_boot {\"n\": 2000, \"sd\": 0.032400013499542676, \"ci90\": [-0.04383788254755994, 0.05742643587726205], \"ci95\": [-0.053365496085516516, 0.07839699074074072], \"p_le0\": 0.5515, \"p_two_sided\": 0.911, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/rival:r_closeness/refit_boot {\"n\": 2000, \"sd\": 0.03649711746821397, \"ci90\": [-0.033720105814797334, 0.08066397594175366], \"ci95\": [-0.045230808317698504, 0.1039651148693699], \"p_le0\": 0.3545, \"p_two_sided\": 0.709, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/rival:r_kcore/refit_boot {\"n\": 2000, \"sd\": 0.02982202678793591, \"ci90\": [-0.06763452963390393, 0.026016748455772832], \"ci95\": [-0.07745925273099191, 0.03491560470727127], \"p_le0\": 0.6945, \"p_two_sided\": 0.666, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/rival:r_eig_phimin/refit_boot {\"n\": 2000, \"sd\": 0.013449762184024026, \"ci90\": [-0.028451782023210644, 0.013820988476160827], \"ci95\": [-0.034076923076923255, 0.020574024822694863], \"p_le0\": 0.777, \"p_two_sided\": 0.46, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/rival:log_field_size/refit_boot {\"n\": 2000, \"sd\": 0.025019916559818747, \"ci90\": [-0.05646831891512738, 0.024199775533108956], \"ci95\": [-0.0651284258640178, 0.03402118100128378], \"p_le0\": 0.763, \"p_two_sided\": 0.479, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp4/specs/gateway_vs_M2_minus_size/refit_boot {\"n\": 2000, \"sd\": 0.038371995334301516, \"ci90\": [-0.011072357874683497, 0.10874982252889233], \"ci95\": [-0.019776500638569557, 0.129097227097227], \"p_le0\": 0.1055, \"p_two_sided\": 0.211, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 66, \"share_single_class_draws\": 0.033}\n/A_replication/exp1/specs/M0/refit_boot {\"n\": 500, \"sd\": 0.008378217618638788, \"ci90\": [-0.01444270158374966, 0.011380543984420602], \"ci95\": [-0.019146982852181436, 0.013947136869148271], \"p_le0\": 0.626, \"p_two_sided\": 0.76, \"n_draws\": 500, \"draws_with_single_class_test_group\": 8, \"share_single_class_draws\": 0.016}\n/A_replication/exp1/specs/M1/refit_boot {\"n\": 500, \"sd\": 0.008463216642900303, \"ci90\": [-0.01651941834023915, 0.0056575660593119305], \"ci95\": [-0.02125248036644931, 0.009271435656591399], \"p_le0\": 0.78, \"p_two_sided\": 0.44, \"n_draws\": 500, \"draws_with_single_class_test_group\": 8, \"share_single_class_draws\": 0.016}\n/A_replication/exp1/specs/M2/refit_boot {\"n\": 500, \"sd\": 0.00758077048131886, \"ci90\": [-0.014340113856853059, 0.006506470628608074], \"ci95\": [-0.020989173263663095, 0.009461192810457559], \"p_le0\": 0.724, \"p_two_sided\": 0.564, \"n_draws\": 500, \"draws_with_single_class_test_group\": 8, \"share_single_class_draws\": 0.016}\n/A_replication/exp1/specs/M2+P/refit_boot {\"n\": 500, \"sd\": 0.005403478301227007, \"ci90\": [-0.011289349777557921, 0.005249535888580864], \"ci95\": [-0.014607188569358883, 0.007090301685399693], \"p_le0\": 0.662, \"p_two_sided\": 0.688, \"n_draws\": 500, \"draws_with_single_class_test_group\": 8, \"share_single_class_draws\": 0.016}\n/A_replication/exp1/specs/P_alone/refit_boot {\"n\": 500, \"sd\": 0.020836506545380568, \"ci90\": [-0.010934734167788689, 0.05258756576851191], \"ci95\": [-0.018841472749540705, 0.06486385706063928], \"p_le0\": 0.138, \"p_two_sided\": 0.276, \"n_draws\": 500, \"draws_with_single_class_test_group\": 8, \"share_single_class_draws\": 0.016}\n/A_replication/exp1/specs/M2+Ppool/refit_boot {\"n\": 500, \"sd\": 0.006766100694023534, \"ci90\": [-0.013474104064999937, 0.006376309628162385], \"ci95\": [-0.020656152090043792, 0.009365386366314284], \"p_le0\": 0.678, \"p_two_sided\": 0.648, \"n_draws\": 500, \"draws_with_single_class_test_group\": 8, \"share_single_class_draws\": 0.016}\n/A_replication/exp1/specs/Ppool_alone/refit_boot {\"n\": 500, \"sd\": 0.011961460783319238, \"ci90\": [-0.0013392411169343699, 0.03339804184344297], \"ci95\": [-0.004182872391763901, 0.040900934559205196], \"p_le0\": 0.08, \"p_two_sided\": 0.16, \"n_draws\": 500, \"draws_with_single_class_test_group\": 8, \"share_single_class_draws\": 0.016}\n/A_replication/exp1_clean/specs/M0/refit_boot {\"n\": 500, \"sd\": 0.01544096678090408, \"ci90\": [-0.03070902663028176, 0.012222091142404532], \"ci95\": [-0.04295643870360239, 0.01749106377734879], \"p_le0\": 0.774, \"p_two_sided\": 0.46, \"n_draws\": 500, \"draws_with_single_class_test_group\": 62, \"share_single_class_draws\": 0.124}\n/A_replication/exp1_clean/specs/M1/refit_boot {\"n\": 500, \"sd\": 0.011955690249020693, \"ci90\": [-0.022446659707054683, 0.012279437264467244], \"ci95\": [-0.025637832791827138, 0.018051223420888097], \"p_le0\": 0.74, \"p_two_sided\": 0.548, \"n_draws\": 500, \"draws_with_single_class_test_group\": 62, \"share_single_class_draws\": 0.124}\n/A_replication/exp1_clean/specs/M2/refit_boot {\"n\": 500, \"sd\": 0.012987001453544395, \"ci90\": [-0.02452244871599709, 0.013293595825426958], \"ci95\": [-0.03189873153191621, 0.020575007158584874], \"p_le0\": 0.702, \"p_two_sided\": 0.608, \"n_draws\": 500, \"draws_with_single_class_test_group\": 62, \"share_single_class_draws\": 0.124}\n/A_replication/exp1_clean/specs/M2+P/refit_boot {\"n\": 500, \"sd\": 0.01175298573786199, \"ci90\": [-0.026720751539662174, 0.008622729627193942], \"ci95\": [-0.0331325857107107, 0.015579631611366192], \"p_le0\": 0.728, \"p_two_sided\": 0.564, \"n_draws\": 500, \"draws_with_single_class_test_group\": 62, \"share_single_class_draws\": 0.124}\n/A_replication/exp1_clean/specs/P_alone/refit_boot {\"n\": 500, \"sd\": 0.03780043797305338, \"ci90\": [-0.02618911073350319, 0.08682609224070498], \"ci95\": [-0.043125132064431186, 0.10595134684188794], \"p_le0\": 0.186, \"p_two_sided\": 0.372, \"n_draws\": 500, \"draws_with_single_class_test_group\": 62, \"share_single_class_draws\": 0.124}\n/A_replication/exp1_clean/specs/M2+Ppool/refit_boot {\"n\": 500, \"sd\": 0.013768422278259071, \"ci90\": [-0.02499013855062555, 0.01483917497231453], \"ci95\": [-0.03483401670901669, 0.020344211822660153], \"p_le0\": 0.696, \"p_two_sided\": 0.632, \"n_draws\": 500, \"draws_with_single_class_test_group\": 62, \"share_single_class_draws\": 0.124}\n/A_replication/exp1_clean/specs/Ppool_alone/refit_boot {\"n\": 500, \"sd\": 0.016220281396615382, \"ci90\": [-0.020541599927468394, 0.03413568632441334], \"ci95\": [-0.028971631628054714, 0.039049465029140584], \"p_le0\": 0.21, \"p_two_sided\": 0.42, \"n_draws\": 500, \"draws_with_single_class_test_group\": 62, \"share_single_class_draws\": 0.124}\n/A_replication/exp3/specs/M0/refit_boot {\"n\": 500, \"sd\": 0.032246886156648044, \"ci90\": [-0.08292675470775253, 0.006252809933446598], \"ci95\": [-0.12038119612068972, 0.013633997027568326], \"p_le0\": 0.914, \"p_two_sided\": 0.18, \"n_draws\": 500, \"draws_with_single_class_test_group\": 2, \"share_single_class_draws\": 0.004}\n/A_replication/exp3/specs/M1/refit_boot {\"n\": 500, \"sd\": 0.031017040138609994, \"ci90\": [-0.06693395979204225, 0.031558131031076714], \"ci95\": [-0.09076322322551555, 0.04449269503647141], \"p_le0\": 0.784, \"p_two_sided\": 0.436, \"n_draws\": 500, \"draws_with_single_class_test_group\": 2, \"share_single_class_draws\": 0.004}\n/A_replication/exp3/specs/M2/refit_boot {\"n\": 500, \"sd\": 0.02941244384248549, \"ci90\": [-0.0393294606999426, 0.05349040931427292], \"ci95\": [-0.051600205198358354, 0.07001736111111106], \"p_le0\": 0.532, \"p_two_sided\": 0.952, \"n_draws\": 500, \"draws_with_single_class_test_group\": 2, \"share_single_class_draws\": 0.004}\n/A_replication/exp3/specs/M2+P/refit_boot {\"n\": 500, \"sd\": 0.017582864500499968, \"ci90\": [-0.03400906696582458, 0.018454477017782682], \"ci95\": [-0.04508549622380597, 0.024257078777684328], \"p_le0\": 0.638, \"p_two_sided\": 0.724, \"n_draws\": 500, \"draws_with_single_class_test_group\": 2, \"share_single_class_draws\": 0.004}\n/A_replication/exp3/specs/P_alone/refit_boot {\"n\": 500, \"sd\": 0.0627915187044768, \"ci90\": [-0.05239789196310938, 0.13680079095898914], \"ci95\": [-0.08631982382718525, 0.16244534126309826], \"p_le0\": 0.26, \"p_two_sided\": 0.52, \"n_draws\": 500, \"draws_with_single_class_test_group\": 2, \"share_single_class_draws\": 0.004}\n/A_replication/exp3/specs/M2+Ppool/refit_boot {\"n\": 500, \"sd\": 0.030821209125323257, \"ci90\": [-0.028885455448033868, 0.0716383969905814], \"ci95\": [-0.038127034597622865, 0.07802258947057077], \"p_le0\": 0.346, \"p_two_sided\": 0.692, \"n_draws\": 500, \"draws_with_single_class_test_group\": 2, \"share_single_class_draws\": 0.004}\n/A_replication/exp3/specs/Ppool_alone/refit_boot {\"n\": 500, \"sd\": 0.046972612539038866, \"ci90\": [-0.05214963074262546, 0.08881987577639736], \"ci95\": [-0.07889395458717158, 0.10628251702361811], \"p_le0\": 0.378, \"p_two_sided\": 0.756, \"n_draws\": 500, \"draws_with_single_class_test_group\": 2, \"share_single_class_draws\": 0.004}\n/A_replication/union/specs/M0/refit_boot {\"n\": 2000, \"sd\": 0.009943671412557756, \"ci90\": [-0.014099988538190732, 0.017905561829474833], \"ci95\": [-0.018749521122400865, 0.023480870325544106], \"p_le0\": 0.5515, \"p_two_sided\": 0.897, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/M1/refit_boot {\"n\": 2000, \"sd\": 0.007922112206345906, \"ci90\": [-0.01208139934032062, 0.012669739592874162], \"ci95\": [-0.015878201547793187, 0.01638107999117978], \"p_le0\": 0.581, \"p_two_sided\": 0.841, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/M2/refit_boot {\"n\": 2000, \"sd\": 0.005953554809618843, \"ci90\": [-0.009665691146255623, 0.008014377520263646], \"ci95\": [-0.012079717600047765, 0.012000159257471185], \"p_le0\": 0.6335, \"p_two_sided\": 0.739, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/M2+P/refit_boot {\"n\": 2000, \"sd\": 0.00352052306879365, \"ci90\": [-0.005738548083604672, 0.005161929722476644], \"ci95\": [-0.007543141758378155, 0.00662135269913677], \"p_le0\": 0.4765, \"p_two_sided\": 0.953, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/P_alone/refit_boot {\"n\": 2000, \"sd\": 0.022037102775076266, \"ci90\": [-0.008609756558981857, 0.06322127550605762], \"ci95\": [-0.013334199493822228, 0.07558108251434237], \"p_le0\": 0.1075, \"p_two_sided\": 0.215, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/M2+Ppool/refit_boot {\"n\": 2000, \"sd\": 0.004980394232347449, \"ci90\": [-0.008712060927325705, 0.006582908032322854], \"ci95\": [-0.01216568045171185, 0.008302631897532128], \"p_le0\": 0.536, \"p_two_sided\": 0.938, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/Ppool_alone/refit_boot {\"n\": 2000, \"sd\": 0.014340974163215415, \"ci90\": [-0.0015434426121545771, 0.04280589886339879], \"ci95\": [-0.004574307776052122, 0.050952256760827874], \"p_le0\": 0.07, \"p_two_sided\": 0.14, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/rival:r_strength/refit_boot {\"n\": 2000, \"sd\": 0.011496125006386337, \"ci90\": [-0.0054221160739118535, 0.029330548396439293], \"ci95\": [-0.008196801925235576, 0.03624814745160267], \"p_le0\": 0.215, \"p_two_sided\": 0.43, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/rival:r_degree/refit_boot {\"n\": 2000, \"sd\": 0.014474258795281107, \"ci90\": [-0.009475491385150636, 0.03553905468677881], \"ci95\": [-0.013994488229317573, 0.04291466264733773], \"p_le0\": 0.2435, \"p_two_sided\": 0.487, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/rival:r_betweenness/refit_boot {\"n\": 2000, \"sd\": 0.00584318455636793, \"ci90\": [-0.0068996593453409805, 0.011309903407048655], \"ci95\": [-0.008163539450138079, 0.014268658539491889], \"p_le0\": 0.5355, \"p_two_sided\": 0.936, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/rival:r_pagerank/refit_boot {\"n\": 2000, \"sd\": 0.011709739795140308, \"ci90\": [-0.003999524540999189, 0.03155158946105351], \"ci95\": [-0.006559775359438807, 0.038300424075992864], \"p_le0\": 0.162, \"p_two_sided\": 0.324, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/rival:r_closeness/refit_boot {\"n\": 2000, \"sd\": 0.013632931466204316, \"ci90\": [-0.0005000652221672949, 0.04104056278251094], \"ci95\": [-0.0028695302565237917, 0.050085276497370955], \"p_le0\": 0.055, \"p_two_sided\": 0.11, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/rival:r_kcore/refit_boot {\"n\": 2000, \"sd\": 0.01712219835811962, \"ci90\": [-0.03410924788075324, 0.021464689258498107], \"ci95\": [-0.04242620459764613, 0.026803779024343232], \"p_le0\": 0.6415, \"p_two_sided\": 0.718, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/rival:r_eig_phimin/refit_boot {\"n\": 2000, \"sd\": 0.007733297854570544, \"ci90\": [-0.010260361947324959, 0.01485523122525495], \"ci95\": [-0.012676565539660109, 0.018531986370214342], \"p_le0\": 0.4425, \"p_two_sided\": 0.885, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/rival:log_field_size/refit_boot {\"n\": 2000, \"sd\": 0.005482300635299129, \"ci90\": [-0.012805781791055581, 0.0034499175164136907], \"ci95\": [-0.01671794599670682, 0.0054515633712070065], \"p_le0\": 0.7835, \"p_two_sided\": 0.435, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/union/specs/gateway_vs_M2_minus_size/refit_boot {\"n\": 2000, \"sd\": 0.006215348274891286, \"ci90\": [-0.010290902695655685, 0.008431169021338324], \"ci95\": [-0.013220161336135173, 0.012380509071941723], \"p_le0\": 0.615, \"p_two_sided\": 0.778, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 1, \"share_single_class_draws\": 0.0005}\n/A_replication/new_eps/specs/M0/refit_boot {\"n\": 2000, \"sd\": 0.009344361018837863, \"ci90\": [-0.018426599235917895, 0.010808943090690058], \"ci95\": [-0.023860852075218757, 0.01618317876898166], \"p_le0\": 0.7095, \"p_two_sided\": 0.587, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/M1/refit_boot {\"n\": 2000, \"sd\": 0.008983724683858729, \"ci90\": [-0.01721845273119541, 0.011458172266879526], \"ci95\": [-0.02136787280701747, 0.017159238225474452], \"p_le0\": 0.6705, \"p_two_sided\": 0.665, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/M2/refit_boot {\"n\": 2000, \"sd\": 0.009161844567754887, \"ci90\": [-0.017174653107523485, 0.013010523027579522], \"ci95\": [-0.02110277179705331, 0.017419970380496586], \"p_le0\": 0.664, \"p_two_sided\": 0.682, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/M2+P/refit_boot {\"n\": 2000, \"sd\": 0.006073151232694765, \"ci90\": [-0.010524874036301757, 0.00906035275658712], \"ci95\": [-0.013333561661902185, 0.011355640152274086], \"p_le0\": 0.5065, \"p_two_sided\": 1.0, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/P_alone/refit_boot {\"n\": 2000, \"sd\": 0.023969929008607307, \"ci90\": [-0.010254910677846635, 0.06591217200721135], \"ci95\": [-0.01890035929534232, 0.07689507437427963], \"p_le0\": 0.134, \"p_two_sided\": 0.268, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/M2+Ppool/refit_boot {\"n\": 2000, \"sd\": 0.011475141734860672, \"ci90\": [-0.014927243251557075, 0.02147991942405701], \"ci95\": [-0.019104778265690014, 0.027673217776133158], \"p_le0\": 0.4715, \"p_two_sided\": 0.943, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/Ppool_alone/refit_boot {\"n\": 2000, \"sd\": 0.014446084961915757, \"ci90\": [-0.0030576214648734613, 0.04426356866909459], \"ci95\": [-0.006388877386527974, 0.05031474899069678], \"p_le0\": 0.0825, \"p_two_sided\": 0.165, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/rival:r_strength/refit_boot {\"n\": 2000, \"sd\": 0.00865779731826134, \"ci90\": [-0.01291585638780401, 0.015137540218024208], \"ci95\": [-0.016728949217215412, 0.019844717011234914], \"p_le0\": 0.5365, \"p_two_sided\": 0.938, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/rival:r_degree/refit_boot {\"n\": 2000, \"sd\": 0.01643182761736031, \"ci90\": [-0.02979418196319596, 0.023469128796626253], \"ci95\": [-0.0355196577649368, 0.029982482482482423], \"p_le0\": 0.6305, \"p_two_sided\": 0.742, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/rival:r_betweenness/refit_boot {\"n\": 2000, \"sd\": 0.00600175895031832, \"ci90\": [-0.012810931778955042, 0.0064698987228845655], \"ci95\": [-0.01577393638692399, 0.009406877054780967], \"p_le0\": 0.73, \"p_two_sided\": 0.553, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/rival:r_pagerank/refit_boot {\"n\": 2000, \"sd\": 0.008712701350974758, \"ci90\": [-0.01225967338579192, 0.01662514883053562], \"ci95\": [-0.015332268778742894, 0.021353500853326483], \"p_le0\": 0.506, \"p_two_sided\": 0.995, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/rival:r_closeness/refit_boot {\"n\": 2000, \"sd\": 0.009849480296367457, \"ci90\": [-0.008411359525810952, 0.023681003594098252], \"ci95\": [-0.010729988379919527, 0.029533626945270154], \"p_le0\": 0.297, \"p_two_sided\": 0.594, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/rival:r_kcore/refit_boot {\"n\": 2000, \"sd\": 0.024513215507988302, \"ci90\": [-0.0601304572461896, 0.017334324942791846], \"ci95\": [-0.06957689317000267, 0.027727538440179642], \"p_le0\": 0.784, \"p_two_sided\": 0.435, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/rival:r_eig_phimin/refit_boot {\"n\": 2000, \"sd\": 0.011938357904938555, \"ci90\": [-0.026927298483362536, 0.011205234081902112], \"ci95\": [-0.033611814732596765, 0.0158921301649277], \"p_le0\": 0.732, \"p_two_sided\": 0.542, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/rival:log_field_size/refit_boot {\"n\": 2000, \"sd\": 0.011893717444863398, \"ci90\": [-0.027564724559105025, 0.011007839143615038], \"ci95\": [-0.033281655880950355, 0.01693065492570167], \"p_le0\": 0.8155, \"p_two_sided\": 0.374, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/new_eps/specs/gateway_vs_M2_minus_size/refit_boot {\"n\": 2000, \"sd\": 0.009145756705482965, \"ci90\": [-0.01580698397780166, 0.013907979125370494], \"ci95\": [-0.02033309790693764, 0.01938182517079299], \"p_le0\": 0.6295, \"p_two_sided\": 0.749, \"n_draws\": 2000, \"draws_with_single_class_test_group\": 3, \"share_single_class_draws\": 0.0015}\n/A_replication/union_agree/specs/M0/refit_boot {\"n\": 500, \"sd\": 0.00973198219472822, \"ci90\": [-0.01484443598971512, 0.014131194610912643], \"ci95\": [-0.019069722553195716, 0.02491426321177083], \"p_le0\": 0.602, \"p_two_sided\": 0.796, \"n_draws\": 500, \"draws_with_single_class_test_group\": 0, \"share_single_class_draws\": 0.0}\n/A_replication/union_agree/specs/M1/refit_boot {\"n\": 500, \"sd\": 0.007377332913202161, \"ci90\": [-0.01617980102924141, 0.005687201874741735], \"ci95\": [-0.021162706640318774, 0.007876073068656663], \"p_le0\": 0.736, \"p_two_sided\": 0.528, \"n_draws\": 500, \"draws_with_single_class_test_group\": 0, \"share_single_class_draws\": 0.0}\n/A_replication/union_agree/specs/M2/refit_boot {\"n\": 500, \"sd\": 0.006632383651430545, \"ci90\": [-0.01607606785151396, 0.006183888880728099], \"ci95\": [-0.019194966924750815, 0.008286310396220223], \"p_le0\": 0.686, \"p_two_sided\": 0.64, \"n_draws\": 500, \"draws_with_single_class_test_group\": 0, \"share_single_class_draws\": 0.0}\n/A_replication/union_agree/specs/M2+P/refit_boot {\"n\": 500, \"sd\": 0.004626288361781808, \"ci90\": [-0.00845977702089064, 0.0056010696725598014], \"ci95\": [-0.010817340313682141, 0.00741445550823068], \"p_le0\": 0.542, \"p_two_sided\": 0.924, \"n_draws\": 500, \"draws_with_single_class_test_group\": 0, \"share_single_class_draws\": 0.0}\n/A_replication/union_agree/specs/P_alone/refit_boot {\"n\": 500, \"sd\": 0.01770951223834848, \"ci90\": [-0.016345946101510505, 0.0417355036719502], \"ci95\": [-0.023866085837377374, 0.046417527027934474], \"p_le0\": 0.252, \"p_two_sided\": 0.504, \"n_draws\": 500, \"draws_with_single_class_test_group\": 0, \"share_single_class_draws\": 0.0}\n/A_replication/union_agree/specs/M2+Ppool/refit_boot {\"n\": 500, \"sd\": 0.006993779011263885, \"ci90\": [-0.014186669967903376, 0.0069910169298517], \"ci95\": [-0.019509166566337194, 0.00860090679172384], \"p_le0\": 0.66, \"p_two_sided\": 0.684, \"n_draws\": 500, \"draws_with_single_class_test_group\": 0, \"share_single_class_draws\": 0.0}\nTraceback (most recent call last):\n  File \"<string>\", line 13, in <module>\n  File \"<string>\", line 10, in find\n  File \"<string>\", line 10, in find\n  File \"<string>\", line 10, in find\n  [Previous line repeated 1 more time]\n  File \"<string>\", line 9, in find\nBrokenPipeError: [Errno 32] Broken pipe", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-28 20:57:33 UTC

```
Print Evaluation 1 record tables and power section:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1; python3 -c "
import json
m=json.load(open('eval_out.json'))['metadata']
F=m['F_record']; print(list(F.keys()))
f5=F['F5_exp4_field_level']; print(json.dumps({k:v for k,v in f5.items() if k!='feature_lists'})[:2500])
for k in F:
  if k!='F5_exp4_field_level': print('##',k,json.dumps(F[k])[:900])
print('## E', json.dumps(m['E_power'])[:1500])
print('## missing', json.dumps(m['missing_inputs'])[:800])
" 2>&1 | head -60
```

### [24] TOOL RESULT — Bash · 2026-09-28 20:57:33 UTC

```
{"stdout": "['F1_rho_B5', 'F2_A_star_h', 'F3_exp3_portability', 'F4_exp4_secondary_screens', 'F5_exp4_field_level']\n{\"ci_convention\": \"iter-1: fixed-prediction concept bootstrap 95%; new: concept-clustered REFIT bootstrap 95%\", \"rows\": {\"all_four_available\": {\"iter1_delta\": 0.08222222222222231, \"iter1_ci95_fixed\": [0.00805976430976427, 0.15293222402597403], \"new_delta\": 0.0822222222222222, \"new_ci95_refit\": [-0.04158854166666669, 0.2035205518018018], \"new_ci90_refit\": [-0.017641280089271516, 0.1823923172292432]}, \"size_controlled_all_three\": {\"iter1_delta\": 0.08507936507936509, \"iter1_ci95_fixed\": [0.0036578172723651047, 0.1637858035371011], \"new_delta\": 0.08507936507936509, \"new_ci95_refit\": [-0.042509192535107154, 0.21990591981473434], \"new_ci90_refit\": [-0.02260927899198884, 0.19657016526858978]}, \"gateway_j\": {\"iter1_delta\": 0.10253968253968249, \"iter1_ci95_fixed\": [0.03384553272235451, 0.1673901012017709], \"new_delta\": 0.10253968253968249, \"new_ci95_refit\": [0.009548203512734388, 0.21230629470412898], \"new_ci90_refit\": [0.026643047480620196, 0.1893955413939996]}, \"size_controlled_gateway_j\": {\"iter1_delta\": 0.10222222222222233, \"iter1_ci95_fixed\": [0.028981799797775657, 0.17321771114310708], \"new_delta\": 0.10222222222222221, \"new_ci95_refit\": [0.01697509578544065, 0.21727531102531097], \"new_ci90_refit\": [0.026207437152758674, 0.1978548047696983]}, \"phi_home_j\": {\"iter1_delta\": -0.0003174603174602719, \"iter1_ci95_fixed\": [-0.04487612612612619, 0.03481629080651441], \"new_delta\": -0.0003174603174602719, \"new_ci95_refit\": [-0.07942868764904608, 0.08070067780295054], \"new_ci90_refit\": [-0.05778133903133894, 0.06663998189465155]}, \"density_j\": {\"iter1_delta\": 0.02190476190476187, \"iter1_ci95_fixed\": [-0.030561594202898553, 0.08201236951236947], \"new_delta\": 0.02190476190476187, \"new_ci95_refit\": [-0.04878818458591322, 0.1061370477710573], \"new_ci90_refit\": [-0.03606711087982871, 0.0896771284271284]}, \"log_field_size_alone_added\": {\"iter1_delta\": -0.008571428571428674, \"iter1_ci95_fixed\": [-0.0420098141695703, 0.0210668563300141], \"new_delta\": -0.008571428571428563, \"new_ci95_refit\": [-0.08538796315112103, 0.048125748487505504], \"new_ci90_refit\": [-0.07118907563025209, 0.03280897000687248]}}}\n## F1_rho_B5 {\"ci_convention\": \"point estimates as reported (LOGO OOF Spearman); no CI\", \"exp1\": {\"rho_B5\": 0.8338037342596614, \"per_group\": {\"Biochemistry, Genetics and Molecular Biology\": {\"n\": 13, \"rho_B5\": 0.8681318681318682}, \"Computer Science\": {\"n\": 21, \"rho_B5\": 0.7688311688311688}, \"Engineering\": {\"n\": 3, \"rho_B5\": null}, \"Medicine\": {\"n\": 11, \"rho_B5\": 0.9363636363636365}}}, \"exp3\": {\"rho_B5\": 0.7698889916743756, \"n_per_group\": {\"BIO\": 16, \"CS\": 12, \"MED\": 10, \"ENG\": 9}}, \"exp4\": {\"rho_B5\": 0.32742551566080974, \"per_group\": {\"CS\": {\"n\": 10, \"rho_B5\": 0.10303030303030303}, \"Eng\": {\"n\": 7, \"rho_B5\": 0.8571428571428573}, \"BGM\": {\"n\": 9, \"rho_B5\": 0.65}, \"Med\": {\"n\": 8, \"rho_B5\": 0.5714285714285715}}}}\n## F2_A_star_h {\"ci_convention\": \"median and IQR across concepts (no CI)\", \"per_group\": {\"Biochemistry, Genetics and Molecular Biology\": {\"n\": 13, \"median\": -0.2556934214162558, \"q25\": -0.4582305327130662, \"q75\": -0.1322654778512496}, \"Computer Science\": {\"n\": 21, \"median\": -0.3027372476534742, \"q25\": -0.4707795277668117, \"q75\": -0.0637597650235339}, \"Engineering\": {\"n\": 3, \"median\": -0.0414635143567127, \"q25\": -0.10341682507269506, \"q75\": -0.013780361815635949}, \"Medicine\": {\"n\": 11, \"median\": -0.1820998849738501, \"q25\": -0.31536980698789197, \"q75\": -0.09513377044064154}}, \"n_groups_negative_median\": 4}\n## F3_exp3_portability {\"ci_convention\": \"as stored in exp3 screen_result.json['portability'] (point Spearman within group; LOGO delta-rho without CI)\", \"table\": {\"groups\": [\"BIO\", \"CS\", \"ENG\", \"MED\"], \"indicators\": {\"D_z\": {\"pooled_rho_O2r\": 0.19605303731113166, \"pooled_rho_O1\": 0.1864555692956741, \"rho_logvol\": -0.632809127351218, \"within_group_rho_O2r\": {\"BIO\": 0.21470588235294116, \"CS\": 0.25874125874125875, \"ENG\": 0.26666666666666666, \"MED\": -0.35}, \"within_group_rho_O1\": {\"BIO\": -0.1960392117639214, \"CS\": 0.13937366833451514, \"ENG\": 0.10350983390135314, \"MED\": 0.3651483716701107}, \"n_missing\": 1, \"logo_single_rho_O2r\": -0.04740980573543016, \"rho_entropy\": -0.05186555658341042, \"rho_offhome_share\": -0.10490286771507863, \"rho_growth\": -0.09096515572001233, \"logo_delta_rho_O2r\": 0.016998149861239598, \"logo_delta_rho_per_group\": {\"BIO\": 0.02352941176470591, \"CS\": 0.07692307692307698, \"ENG\": 0.0333333333333334\n## F4_exp4_secondary_screens {\"ci_convention\": \"iteration-1 row-bootstrap of FIXED OOF predictions (90%)\", \"table\": {\"G_all\": {\"label\": \"exploratory; not the pre-registered primary\", \"O2r_m30\": {\"delta\": -0.240488922841864, \"ci90\": [-0.4188532790332013, -0.08672601975160257], \"n_groups_positive\": 1}, \"O1\": {\"delta\": 0.11188811188811187, \"ci90\": [0.03376623376623388, 0.20982017982017978], \"n_groups_positive\": 1}, \"O3\": {\"delta\": 0.0, \"ci90\": [0.0, 0.0], \"n_groups_positive\": 0}}, \"G_deg\": {\"label\": \"exploratory; not the pre-registered primary\", \"O2r_m30\": {\"delta\": -0.04278074866310161, \"ci90\": [-0.17793128556794152, 0.08804562049691446], \"n_groups_positive\": 1}, \"O1\": {\"delta\": 0.14918414918414913, \"ci90\": [0.05277777777777781, 0.26644736842105265], \"n_groups_positive\": 3}, \"O3\": {\"delta\": 0.0, \"ci90\": [0.0, 0.0], \"n_groups_positive\": 0}}, \"G_btw\": {\"label\": \"exploratory; not the pre-registered primary\", \"O2r_m30\": {\n## E {\"inputs\": {\"SE_boot_union_M2\": 0.005953554809618843, \"N0_rows\": 362, \"n_concepts\": 54, \"m0\": 6.703703703703703, \"rho_c_latent\": 0.13501219531453199, \"rho_c_anova_pearson\": 0.14836479461253538, \"rho_c_used\": 0.13501219531453199, \"rho_c_source\": \"latent\", \"shrunken_effect_lower90_union\": -0.009665691146255623, \"H1_bar\": 0.05}, \"analytic\": [{\"N\": 1000, \"m\": 5, \"DE\": 1.540048781258128, \"SE\": 0.0033412018527540317, \"MDE_80\": 0.009355365187711288, \"power_at_0.05\": 1.0, \"power_at_shrunken\": 0.024997895148220435}, {\"N\": 1000, \"m\": 10, \"DE\": 2.215109757830788, \"SE\": 0.004007126935351831, \"MDE_80\": 0.011219955418985126, \"power_at_0.05\": 1.0, \"power_at_shrunken\": 0.024997895148220435}, {\"N\": 2000, \"m\": 5, \"DE\": 1.540048781258128, \"SE\": 0.0023625864873954325, \"MDE_80\": 0.006615242164707211, \"power_at_0.05\": 1.0, \"power_at_shrunken\": 0.024997895148220435}, {\"N\": 2000, \"m\": 10, \"DE\": 2.215109757830788, \"SE\": 0.0028334666290625475, \"MDE_80\": 0.007933706561375133, \"power_at_0.05\": 1.0, \"power_at_shrunken\": 0.024997895148220435}, {\"N\": 4000, \"m\": 5, \"DE\": 1.540048781258128, \"SE\": 0.0016706009263770158, \"MDE_80\": 0.004677682593855644, \"power_at_0.05\": 1.0, \"power_at_shrunken\": 0.024997895148220435}, {\"N\": 4000, \"m\": 10, \"DE\": 2.215109757830788, \"SE\": 0.0020035634676759157, \"MDE_80\": 0.005609977709492563, \"power_at_0.05\": 1.0, \"power_at_shrunken\": 0.024997895148220435}], \"simulation\": [{\"N\": 1000, \"m\": 5, \"n_sims_null\": 300, \"n_sims_alt\": 300, \"SD_null\": 0.0016863948602222495, \"crit95_null\": 0\n## missing []", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-28 20:57:42 UTC

```
Check Dataset 2 coverage report:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2; ls out full_data_out | head; python3 -c "
import json
d=json.load(open('out/coverage_report.json')); print(json.dumps(d)[:3000])"
```

### [26] TOOL RESULT — Bash · 2026-09-28 20:57:42 UTC

```
{"stdout": "full_data_out:\nfull_data_out_1.json\nfull_data_out_2.json\nfull_data_out_3.json\nmini_full_data_out_1.json\nmini_full_data_out_2.json\nmini_full_data_out_3.json\npreview_full_data_out_1.json\npreview_full_data_out_2.json\npreview_full_data_out_3.json\n{\"frame\": \"OpenAlex legacy concepts, levels 2-5 (levels 0-1 are ancestor-only rows)\", \"n_target_concepts\": 64723, \"by_source\": {\"acm_ccs\": {\"n_concepts\": 64723, \"n_with_event\": 1298, \"n_with_year_usable_event\": 1298, \"status\": {\"not_applicable\": 55103, \"not_found\": 8322, \"found\": 1298}, \"event_year_hist_5y\": {\"1995\": 755, \"2010\": 1673}, \"match_method_mix\": {\"fuzzy+llm\": 628, \"wikidata_property\": 422, \"exact_norm_alias+llm\": 431, \"exact_norm_label\": 947}}, \"gartner_hype_cycle\": {\"n_concepts\": 64723, \"n_with_event\": 466, \"n_with_year_usable_event\": 466, \"status\": {\"not_found\": 64257, \"found\": 466}, \"event_year_hist_5y\": {\"1995\": 200, \"2000\": 198, \"2005\": 242, \"2010\": 356, \"2015\": 217, \"2020\": 86, \"2025\": 28}, \"match_method_mix\": {\"fuzzy+llm\": 194, \"embed+llm\": 824, \"exact_norm_alias+llm\": 110, \"exact_norm_label+llm\": 199}}, \"jel\": {\"n_concepts\": 64723, \"n_with_event\": 0, \"n_with_year_usable_event\": 0, \"status\": {\"not_applicable\": 59852, \"not_found\": 4658, \"found\": 213}, \"event_year_hist_5y\": {}, \"match_method_mix\": {}}, \"mesh\": {\"n_concepts\": 64723, \"n_with_event\": 20872, \"n_with_year_usable_event\": 20872, \"status\": {\"not_applicable\": 24756, \"found\": 20872, \"not_found\": 19095}, \"event_year_hist_5y\": {\"1960\": 625, \"1965\": 6118, \"1970\": 1345, \"1975\": 1112, \"1980\": 846, \"1985\": 1023, \"1990\": 3293, \"1995\": 1360, \"2000\": 1930, \"2005\": 1520, \"2010\": 1267, \"2015\": 1317, \"2020\": 642, \"2025\": 151}, \"match_method_mix\": {\"wikidata_property\": 17228, \"exact_norm_label+llm\": 4014, \"exact_norm_alias+llm\": 1307}}, \"mit_tr10\": {\"n_concepts\": 64723, \"n_with_event\": 313, \"n_with_year_usable_event\": 313, \"status\": {\"not_found\": 64410, \"found\": 313}, \"event_year_hist_5y\": {\"2000\": 81, \"2005\": 66, \"2010\": 95, \"2015\": 44, \"2020\": 50, \"2025\": 20}, \"match_method_mix\": {\"embed+llm\": 250, \"fuzzy+llm\": 62, \"exact_norm_label+llm\": 36, \"exact_norm_alias+llm\": 8}}, \"msc\": {\"n_concepts\": 64723, \"n_with_event\": 1121, \"n_with_year_usable_event\": 1121, \"status\": {\"not_applicable\": 57566, \"not_found\": 6036, \"found\": 1121}, \"event_year_hist_5y\": {\"2000\": 914, \"2010\": 1142, \"2020\": 828}, \"match_method_mix\": {\"fuzzy+llm\": 864, \"exact_norm_alias+llm\": 242, \"exact_norm_label\": 1001, \"wikidata_property\": 777}}, \"nature_methods_moty\": {\"n_concepts\": 64723, \"n_with_event\": 38, \"n_with_year_usable_event\": 38, \"status\": {\"not_found\": 36511, \"not_applicable\": 28174, \"found\": 38}, \"event_year_hist_5y\": {\"2005\": 13, \"2010\": 17, \"2015\": 6, \"2020\": 11, \"2025\": 1}, \"match_method_mix\": {\"wikilink+llm\": 12, \"embed+llm\": 35, \"exact_norm_label+llm\": 1}}, \"pacs_physh\": {\"n_concepts\": 64723, \"n_with_event\": 2635, \"n_with_year_usable_event\": 2635, \"status\": {\"not_applicable\": 48266, \"not_found\": 13822, \"found\": 2635}, \"event_year_hist_5y\": {\"2010\": 1201, \"2015\": 3422}, \"match_method_mix\": {\"exact_norm_alias+llm\": 919, \"exact_norm_label\": 2663, \"fuzzy+llm\": 1041}}, \"physics_world_boty\": {\"n_concepts\": 64723, \"n_with_event\": 100, \"n_with_year_usable_event\": 100, \"status\": {\"not_applicable\": 49094, \"not_found", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] ASSISTANT · 2026-09-28 20:57:48 UTC

```
Status: I've traced Dataset 2. Its source table in the report gives external-entry counts where it claims matched-concept counts. I'll finish the Wikipedia/Wikidata check, then write the review.
```

### [28] TOOL CALL — Bash · 2026-09-28 20:57:48 UTC

```
Tabulate per-source concept coverage in Dataset 2:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2; python3 -c "
import json
d=json.load(open('out/coverage_report.json'))['by_source']
for k,v in d.items(): print(k, v.get('n_with_event'), v.get('n_with_year_usable_event'), v['status'])
d=json.load(open('out/coverage_report.json')); print([k for k in d.keys()])
"; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/user_uploads 2>/dev/null | head
```

### [29] TOOL RESULT — Bash · 2026-09-28 20:57:48 UTC

```
{"stdout": "acm_ccs 1298 1298 {'not_applicable': 55103, 'not_found': 8322, 'found': 1298}\ngartner_hype_cycle 466 466 {'not_found': 64257, 'found': 466}\njel 0 0 {'not_applicable': 59852, 'not_found': 4658, 'found': 213}\nmesh 20872 20872 {'not_applicable': 24756, 'found': 20872, 'not_found': 19095}\nmit_tr10 313 313 {'not_found': 64410, 'found': 313}\nmsc 1121 1121 {'not_applicable': 57566, 'not_found': 6036, 'found': 1121}\nnature_methods_moty 38 38 {'not_found': 36511, 'not_applicable': 28174, 'found': 38}\npacs_physh 2635 2635 {'not_applicable': 48266, 'not_found': 13822, 'found': 2635}\nphysics_world_boty 100 100 {'not_applicable': 49094, 'not_found': 15529, 'found': 100}\nresearch_fronts 589 589 {'not_found': 64134, 'found': 589}\nscience_boty 53 53 {'not_found': 64670, 'found': 53}\nwikidata 1425 1316 {'not_found': 63292, 'found': 1425, 'not_checked': 6}\nwikipedia_en 64363 50459 {'found_estimated': 56557, 'found': 7806, 'not_checked': 360}\n['frame', 'n_target_concepts', 'by_source', 'by_source_level', 'by_source_group', 'by_source_level0', 'by_source_level_l0_group', 'llm_audit_and_agreement', 'dated_domain_taxonomy_by_group', 'groups_without_dated_domain_taxonomy', 'recommendation']", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] TOOL CALL — ToolSearch · 2026-09-28 20:57:56 UTC

```
{'query': 'select:WebSearch', 'max_results': 1}
```

### [31] TOOL RESULT — ToolSearch · 2026-09-28 20:57:56 UTC

```
{"matches": ["WebSearch"], "query": "select:WebSearch", "total_deferred_tools": 27}
```

### [32] TOOL CALL — WebSearch · 2026-09-28 20:57:58 UTC

```
Sun Latora 2020 "evolution of knowledge within and across fields in modern physics" Scientific Reports
```

### [33] TOOL RESULT — WebSearch · 2026-09-28 20:58:02 UTC

```
{"query": "Sun Latora 2020 \"evolution of knowledge within and across fields in modern physics\" Scientific Reports", "results": [{"tool_use_id": "srvtoolu_018SQW1f2bTmd7KBBeqeHoVd", "content": [{"title": "Publications: Vito Latora", "url": "https://researchpublications.its.qmul.ac.uk/publications/staff/29612.html"}, {"title": "The evolution of knowledge within and across fields in modern physics ...", "url": "https://www.nature.com/articles/s41598-020-68774-w"}, {"title": "Quantifying the rise and fall of scientific fields", "url": "https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0270131"}, {"title": "The evolution of scientific literature as metastable knowledge ...", "url": "https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0287226"}, {"title": "Ye SUN", "url": "https://www.researchgate.net/profile/Ye-Sun-27"}, {"title": "[2001.07199] The evolution of knowledge within and across fields ...", "url": "https://arxiv.org/abs/2001.07199"}, {"title": "Google Scholar", "url": "https://scholar.google.com/scholar_lookup?title=The+evolution+of+knowledge+within+and+across+fields+in+modern+physics&amp=&publication_year=2020&amp=&author=Y.+Sun&amp=&author=V.+Latora"}, {"title": "The evolution of interdisciplinarity in physics research", "url": "https://www.nature.com/articles/srep00551"}, {"title": "The evolution of knowledge within and across fields in modern physics", "url": "https://arxiv.org/pdf/2001.07199"}, {"title": "The evolution of knowledge within and across fields in modern physics", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7374558/"}]}, "I found the paper you're looking for! Here are the key details:\n\n**Publication Information:**\nSun and Latora published \"The evolution of knowledge within and across fields in modern physics\" in 2020, specifically in Scientific Reports with DOI 10.1038/s41598-020-68774-w.\n\n**Research Overview:**\nThe article was published on July 21, 2020. The study analyzed bibliographic information from over 430,000 articles published by the American Physical Society (APS) between 1985 and 2015, using Physics and Astronomy Classification Scheme (PACS) codes to construct a temporal network where nodes represent physics fields and directed links show significant dependencies between fields.\n\n**Key Findings:**\nThe research found that knowledge flows have become increasingly homogeneous over recent years, indicating the important role of interdisciplinary research.\n\nThe paper is available open access through multiple sources, including Nature.com and the NIH/PMC database."], "durationSeconds": 5.409764056000014, "searchCount": 1}
```

### [34] TOOL CALL — Bash · 2026-09-28 20:58:38 UTC

```
Check iteration-2 strategy and worker results for failures:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2; ls; ls gen_strat* 2>/dev/null | head; find . -maxdepth 3 -name ".aii_worker_result.json" | while read f; do echo "$f: $(head -c 300 $f)"; done 2>/dev/null | head -20
```

### [35] TOOL RESULT — Bash · 2026-09-28 20:58:38 UTC

```
{"stdout": "gen_art\ngen_plan\ngen_report_text\ngen_strat\nreview_report\ncurrent_report.md\ngen_strat_1\n./gen_art/gen_art_evaluation_1/.aii_worker_result.json: {\"pod_id\": \"ntsfwx7q4u332j\", \"result\": {\"final_response\": \"I've read exp4's screen, backbone and method code and I'm now looking at the data files from all three experiments.\\nNext I'm setting up the Python environment, then writing `eval.py`, which covers harmonisation plus Blocks A\\u2013F.\\nNow I'\n./gen_art/gen_art_research_1/.aii_worker_result.json: {\"pod_id\": \"ogihi5rum9hfuv\", \"result\": {\"final_response\": \"I'll start by loading the web-tools skill and inspecting the workspace.\\nStep 1: the target collection. I'll try the collection page once, and run searches in parallel.\\nSpringer blocks all fetch routes (JS challenge), as the plan anticipate\n./gen_art/gen_art_dataset_2/.aii_worker_result.json: {\"pod_id\": \"ie80gohqe34n6o\", \"result\": {\"final_response\": \"I'll start by inspecting the workspace, the prior-iteration artifacts, and the skills.\\nDownloaded the 65,026-concept OpenAlex snapshot (zero credits); the Python env is still installing. Next: inspect the concept schema and start the Wikida\n./gen_art/gen_art_experiment_6/.aii_worker_result.json: {\"pod_id\": \"qbla4wkcphmne9\", \"result\": {\"final_response\": \"I'm treating the pasted pipeline prompt as the task. It matches this workspace, and the earlier attempt crashed because it asked for confirmation that never came. I'll keep spending minimal. First I'll look at the environment and the inputs \n./gen_art/gen_art_experiment_5/.aii_worker_result.json: {\"pod_id\": \"s1se1ncjdf8o54\", \"result\": {\"final_response\": \"Reading the iteration-1 scan code and data so I can reuse the reader and analyser; next I'll probe the snapshot schema.\\nEnvironment set up (4 CPU, 32 GB). Now probing the OpenAlex works parquet schema and timing.\\nLegacy concepts entity is", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] TOOL CALL — Bash · 2026-09-28 20:58:42 UTC

```
Check iteration-2 strategy for commissioned artifacts:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_strat/gen_strat_1; ls; grep -o '"failed": *[a-z]*' ../../gen_art/*/.aii_worker_result.json; python3 - <<'E'
import json,glob
for f in glob.glob('*.json'):
    s=open(f).read()
    print(f,len(s)); 
    import re
    print(re.findall(r'gen_art_[a-z]+_\d+',s)[:40])
E
```

### [37] TOOL RESULT — Bash · 2026-09-28 20:58:42 UTC

```
{"stdout": "README.md\nsrc\n../../gen_art/gen_art_evaluation_1/.aii_worker_result.json:\"failed\": false\n../../gen_art/gen_art_experiment_5/.aii_worker_result.json:\"failed\": false\n../../gen_art/gen_art_dataset_2/.aii_worker_result.json:\"failed\": false\n../../gen_art/gen_art_experiment_6/.aii_worker_result.json:\"failed\": false\n../../gen_art/gen_art_research_1/.aii_worker_result.json:\"failed\": false", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] ASSISTANT · 2026-09-28 20:58:52 UTC

```
All artifacts are traced. Now I'll write the review JSON, the README and the manifest.
```

### [39] TOOL CALL — Bash · 2026-09-28 20:58:52 UTC

```
Write manifest and README for the review workspace:
cat > .aii/manifest.yaml <<'EOF'
# This review workspace holds only small text files (review JSON, README), so no heavy paths need a decision.
entries: []
EOF
cat > README.md <<'EOF'
# Iteration-2 review of the research report (review_report)

This is an adversarial audit of the run's internal research report after iteration 2, on the question "Do temporal network signals predict how scientific concepts spread across disciplines?".
The review walked all eight artifacts from iterations 1 and 2, recomputed the headline numbers from each artifact's own result files, and checked whether the previous review's MUST-FIX items were done.

## Layout
- `.terminal_claude_agent_struct_out.json`: the structured review (ReviewerFeedback schema): scores, critiques, coverage and the blocking flag.
- `README.md`: this file.
- `.aii/manifest.yaml`: the disposable-outputs manifest. It is empty because there are no heavy files.

## How it was produced
The artifact result files named in the critiques were read directly (read-only), for example `gen_art_experiment_5/results/h1_heldout.json`, `h3_results.json`, `gen_art_experiment_6/results/heldout_result.json`, `dev_result.json`, `gen_art_evaluation_1/eval_out.json`, `gen_art_dataset_2/out/coverage_report.json` and `iter_1/.../gen_art_experiment_3/results/exploratory_partial_association.json`.
No code was run and no data was downloaded.

## Restoring removed files
Nothing is marked for deletion, so nothing needs restoring.
EOF
ls -la .aii
```

### [40] TOOL RESULT — Bash · 2026-09-28 20:58:52 UTC

```
{"stdout": "total 1014\ndrwxr-xr-x 2 root root   12200 Sep 28 20:58 .\ndrwxr-xr-x 3 root root 1024950 Sep 28 20:58 ..\n-rw-r--r-- 1 root root     122 Sep 28 20:58 manifest.yaml", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [41] TOOL CALL — Bash · 2026-09-28 21:00:32 UTC

```
Write the structured review JSON output:
python3 - <<'PYEOF'
import json
out = {
"overall_assessment": (
"Iteration 2 is a real improvement to the record. The run finally moved its budget from more metrics to more samples: a 12,499-concept / 27,393-episode zero-credit OpenAlex snapshot panel with a sealed held-out split. It honestly records the disconfirmation of its own iteration-1 lead (field-level gateway retention). Several iteration-1 errors are corrected in place with marked corrections (A*_h medians, per-experiment rho_B5, O1 label-coverage artefact, failed artifacts, portability wording). "
"I recomputed the headline numbers from the artifacts' own result files, and they match: "
"H1 held-out dAUC -8.97e-06, CI [-0.00062, 0.00033], DL pooled -4.4e-05 (exp5 results/h1_heldout.json); the ladder values; relatedness pair +0.0034 [0.0010, 0.0051]; "
"H3 G 0.0295 / G_A 0.026 / G_btw 0.046, Holm p 0.0045, DL-pooled G 0.068 [0.029, 0.107] (h3_results.json); "
"H2 held-out LR 71.7, d 0.302 [0.240, 0.369], DL 0.284 [0.216, 0.352], perm p 0.001, rewired p 0.015, per-group table (exp6 results/heldout_result.json); "
"ordering 57/87 = 65.5%, sign p 0.0025, McNemar 27/15 p 0.088; trajectory sizes 128/60 and ARI 0.54; "
"Eval1 union +0.00087 [-0.012, 0.012], exp4 M2 +0.037 [-0.018, 0.130], F5 gateway_j refit [0.0095, 0.212] (eval_out.json). "
"So results_reported is true. "
"However, the record still contradicts its own evidence in several places, and it drops results that go against its conclusions. "
"(1) Section 10.3 says H1 is 'DISCONFIRMED by all preregistered criteria'. h1_heldout.json verdict_H1.criteria has lpm_beta_within_gt0_p05 = TRUE: the within-field LPM gives beta 0.068 per SD, p_concept 0.041. The verdict stands, but the sentence is false and the positive within-field result has vanished from the record. "
"(2) The ordering finding is listed under 'Confirmed findings' (Section 16.3), but the artifact's own lead-lag evidence cuts against it. The concept-FE forward regression of next-year entropy change on retained-gateway status is NEGATIVE (held-out b = -0.028, p = 0.0007; dev -0.040, p = 5e-5). The event study has a significant pre-trend (ev-3 = -0.072, p = 0.0002 held-out; -0.088 dev), meaning entropy was already rising before the first gateway retention. On dev the reverse path (entropy -> later gateway retention) IS significant (b = 0.23, p = 0.006), although the report says the reverse is 'not significant (p = 0.22)', citing only held-out. On dev, peripheral fields precede take-off as often as gateways (70% vs 71%). The report's '66% of broad concepts' is really 57 of 175 broad concepts (33%); 65.5% is the share among the 87 non-tied evaluable cases. "
"(3) Section 4.4 says the remaining 7 of 12 partial associations 'are not available in the current workspace output'. They are in iter_1 exp3 results/exploratory_partial_association.json, including D_z 0.313 (4/4 groups) and D_sub 0.245 (4/4 groups). "
"(4) The Dataset 2 source table gives external-entry counts as 'concepts matched': ACM 3,583 vs 1,298 concepts, MSC 17,872 vs 1,121, PACS 8,462 vs 2,635. Wikipedia is given as 6,540 when 64,363 concepts have an event and 50,459 are year-usable (out/coverage_report.json). "
"Several previous MUST-FIX items remain unaddressed: the 34-row exp3 portability table (it now sits ready-made in eval_out.json F_record.F3), the exp1 robustness table (GLMM agreement 0.163, probe agreement 0.10, sensitivities), refit CIs for the concept-level headline deltas and for O2r_resid, the iteration-1 'why' paragraph, the traceable next-field result file, and the mislabelled all_four row. "
"Iteration 2's own positive claims are also under-qualified. H3 is labelled 'confirmed', but the concept-bootstrap CI of pooled G includes zero ([-0.006, 0.065]), the within-group permutation null is centred below zero, G_btw's DL-pooled CI includes zero (I2 = 0.77, negative in LifeEnv), and DEV-to-held-out shrinkage is from 0.14 to 0.03. The H2 novelty claim ignores that standard Hidalgo density is computed on RCA-thresholded (i.e. retained) portfolios, while M0's density uses all entered fields. "
"Coverage is partial: the 30-50 indicator screen and the ~10-indicator held-out validation (RQ1 core), the external-recognition outcome, case studies / 'why it works', and the learned model are all still missing. "
"Because conclusions stated in the record contradict the artifacts' own evidence (items 1-3), soundness is 1 and the review is blocking."),
"strengths": [
"Budget moved from metrics to samples, as the previous review demanded: Exp5 builds a 12,499-concept / 27,393-episode panel from the free snapshot (0 API credits) with a hash-sealed spec (logs/seal.log, frozen_spec.json) and a single unsealing for held-out scoring.",
"The iteration-1 lead is disconfirmed honestly, with a baseline ladder that shows where the signal goes (L1 +0.0019 -> L3 +0.00003 on DEV once P_j(-c) enters; negative at every held-out step). Evaluation 1 adds a node-label permutation (54th percentile) and a shuffled-R placebo (95th pct 0.130 > 0.103). This is exactly the kind of dead end the record must keep.",
"Marked in-place corrections to iteration-1 sections (3.4, 3.9, 4.3, 4.4, 5.3, 6.1, 8) keep the chronology intact. They fix the A*_h median misreading, the rho_B5 ceiling claim and the 'strongest secondary signal' claim, and they add the label-coverage O1 artefact test (G +0.072 -> +0.002).",
"The failed iteration-1 artifacts (gen_art_dataset_1, gen_art_experiment_2) are now recorded with consequences, and candidate S is labelled 'not run, not refuted'.",
"RQ2 is now actually addressed: conditional-logit next-field entry on a held-out split with permutation and rewired-backbone nulls; DTW trajectory classes with a held-out recluster; ordering tests with a random-year placebo. Exp6 audits report an exact-likelihood cross-check (LR 77.3).",
"Most headline numbers trace exactly to named result files; I recomputed every one listed in the overall assessment without a mismatch."
],
"dimension_scores": [
{"dimension": "soundness", "score": 1,
 "justification": "The headline numbers are real and recomputable, but several stated conclusions contradict the artifacts' own evidence. H1 'disconfirmed by all preregistered criteria' is contradicted by verdict_H1.criteria.lpm_beta_within_gt0_p05 = true. The ordering finding is 'confirmed' while the same artifact's lead-lag regression is negative, its event study shows a significant pre-trend and its dev reverse path is significant. The claim that 7 partials are unavailable is contradicted by the file. The Dataset-2 coverage counts are wrong. H3 is called confirmed although its concept-bootstrap CI includes zero.",
 "improvements": [
  "Rewrite 10.3 to list each preregistered H1 criterion with its value from verdict_H1.criteria, including lpm_field_fe (beta 0.068/SD, p_concept 0.041, p_twoway 0.17) and lpm_field_fe_all_splits (0.051, p_concept 0.006, p_twoway 0.18). The verdict is unchanged, but the record then holds all the evidence. Impact: +1 soundness.",
  "Downgrade the ordering result in 16.3 to 'mixed'. Add the lead-lag table (forward_dH_on_ret, reverse_dret_on_H, event_study_H) for dev and held-out, and the dev ordering (gateway 71%, peripheral 70%, McNemar p 0.34). Impact: removes a contradiction.",
  "Report H3 with its concept-bootstrap CI ([-0.006, 0.065] pooled G), the DEV values (G 0.138, G_btw 0.170), the notes on the below-zero permutation null, and G_btw's I2 = 0.77. Call it 'small, within-group, CI-dependent' rather than confirmed."
 ]},
{"dimension": "presentation", "score": 2,
 "justification": "Chronological and mostly traceable, with good use of marked corrections. But some numbers are mislabelled (the Dataset 2 counts, H3's '0 of 40 shuffles' given as if it were the p-value, 'MDE 0.004 at 80% power' that is really the 90% point). Section 10.7 mixes Exp5 and Eval1 power numbers without attribution, and the iteration-2 coverage table is missing.",
 "improvements": [
  "Attribute each number in 10.7 to its artifact. Reconcile Exp5's MDE 0.004 (h1_dev.json power: b = 0.3 gives power 0.90, not 0.80; null false-positive rate 0.125) with Eval1's ~0.02 floor under a field random intercept, and state which bootstrap each CI uses.",
  "Update the Section 8a coverage table for iteration 2."
 ]},
{"dimension": "contribution", "score": 2,
 "justification": "Many iteration-2 results that exist on disk are missing from the report: Exp5 sensitivities (R_abs1-3, newborn_only, n_early>=5, excl_intersection_born), leave-one-field-out, the crossed concept x field bootstrap (held-out CI [-0.0023, 0.0010], about 3x wider), boundary test, clustered-SE logits and per-group domain-specificity table. Also missing: Exp6 HMM trajectories and HMM-vs-DTW ARI 0.09, k-selection grid, R1_s_other / R2 / H1_replication rescue models, relay OLS (ret_x_top +0.29, p 0.07), M1-only coefficient, M2lost, and the dev result block. Previous MUST-FIX tables (the 34-row portability table, exp1 robustness, the remaining 7 partials) are still absent.",
 "improvements": [
  "Paste the missing tables listed in the critiques. Most exist as ready-made JSON (eval_out.json F_record.F3 has the full portability table).",
  "Record the HMM trajectory result as a robustness failure of the two-class solution (ARI 0.09 with DTW)."
 ]}
],
"critiques": [
{"category": "evidence", "severity": "major",
 "description": "Section 10.3 contradicts the artifact. It states H1 is 'DISCONFIRMED by all preregistered criteria'. Exp5 results/h1_heldout.json verdict_H1.criteria lists lpm_beta_within_gt0_p05 = true: the within-field linear probability model with field FE gives beta_within_per_sd = 0.068, p_concept = 0.041 (two-way clustered p = 0.17), and the all-splits version gives 0.051, p_concept = 0.0065. cohort_same_sign is also true, trivially, because both are negative. The report never mentions the LPM, the clustered-SE logits (held-out beta -0.045, p 0.29) or the boundary test (interaction +0.064, p 0.45, 'consistent: false'). A positive within-field gateway coefficient on held-out data is exactly the kind of residual signal the record must keep, especially since the report concludes that gateway is 'a domain specific proxy, not a position dependent causal factor'.",
 "suggested_action": "Replace 'by all preregistered criteria' with a criterion-by-criterion table built from verdict_H1.criteria. Add rows for lpm_field_fe, lpm_field_fe_all_splits, logit_clustered_se (concept / two-way / field) and boundary, for both DEV and held-out. State that the within-field LPM passes at concept-clustered p < 0.05 but not with two-way clustering, and that the verdict rule still returns DISCONFIRMED."},
{"category": "evidence", "severity": "major",
 "description": "The ordering finding (11.3, 16.3: 'first retained gateway field precedes entropy takeoff', listed as CONFIRMED) is contradicted by the artifact's own lead-lag evidence, which the report paraphrases selectively. In heldout_result.json ordering.lead_lag, the concept+age FE regression of next-year entropy change on retention has NEGATIVE coefficients: ret_gw b = -0.028 (p = 0.0007), ret_per b = -0.043 (p = 6e-8). The report says only that both are 'associated with subsequent entropy change'. The event study shows a significant pre-trend: ev-3 = -0.072 (p = 0.0002; dev -0.088, p = 6e-6), so entropy was already rising before first gateway retention. In dev_result.json the reverse path (entropy -> next-year gateway retention) is significant (b = 0.232, p = 0.006), but the report states 'the reverse ... is not significant (p = 0.22)', quoting only held-out. On dev, peripheral fields precede take-off as often as gateway fields (70.3% vs 71.4%, McNemar p = 0.34). Finally, '66% of broad concepts' is 57 of 175 top-tercile concepts (33%). The 65.5% is among the 87 non-tied cases of the 102 evaluable, after 63 concepts had no detected change point.",
 "suggested_action": "Add the full ordering table for DEV and held-out (n_top, n_tau_detected, before/ties/after for gateway and peripheral, McNemar), the forward/reverse lead-lag coefficients and the event-study coefficients. Reword 16.3 as: 'the preregistered sign rule passes, but concept-FE lead-lag regressions show retention followed by smaller entropy gains, a significant pre-trend, and (on dev) entropy predicting later gateway retention; the ordering is not specific to gateway fields (placebo p = 0.63)'. Move it from 'Confirmed' to 'Mixed / not established'."},
{"category": "rigor", "severity": "major",
 "description": "H3 (concept-level gateway landing -> volume-residualised breadth) is listed as 'confirmed' (10.6, 16.5), but its uncertainty is under-reported and variants are cherry-picked. From exp5 results/h3_results.json: the concept-bootstrap 95% CI of pooled G is [-0.006, 0.065], which includes zero. The artifact's note says the within-group permutation null is centred below zero (about -0.012), so the Holm p = 0.0045 is measured against a shifted null. G_btw's DL-pooled estimate is 0.072 with CI [-0.015, 0.159], I2 = 0.77, and it is negative in LifeEnv (-0.020). The DEV values were G 0.138 and G_btw 0.170 (h1_dev.json H3_dev), so held-out shrinkage is about 4x, which the report never states. Section 16.5 quotes the G_btw pooled partial (0.046) next to G's DL pooled (0.068), mixing variants to present the best numbers. The phrase '0 of 40 shuffled outcomes exceed the real value' is wrong: audit_placebo.json reports a 0/40 FALSE-POSITIVE RATE of the test on shuffled outcomes, a calibration check, not an exceedance count. Held-out n (2,838 concepts) is not given.",
 "suggested_action": "Add an H3 table with n, pooled partial rho, concept-bootstrap CI95, per-group rho (PHYS/LIFEENV/SOC/MATHDEC), DL pooled with CI and I2, and the DEV value for each of G, G_A, G_btw and REL_home. Quote the permutation-null centring note. Relabel as 'passes the preregistered permutation rule; pooled bootstrap CI includes zero; effect about 0.03 partial rho, a quarter of its DEV value'. Fix the 0/40 wording."},
{"category": "evidence", "severity": "major",
 "description": "Previous MUST-FIX items remain unaddressed although the data is on disk. (a) The 34-row exp3 portability table is still missing: iteration 2 corrected the wording only, and the full table is now even pre-harmonised in art_lwI2DuRtQRZX eval_out.json metadata.F_record.F3_exp3_portability. The portable NEGATIVE signal edge_persistence and the size-confounded indicators are still absent. (b) Section 4.4 claims the remaining 7 of 12 partial associations are 'not available in the current workspace output'. That is false: iter_1 gen_art_experiment_3/results/exploratory_partial_association.json holds all 12 (D_z 0.313 [-0.161, 0.634] 4/4 groups; D_sub 0.245 4/4; n_comm_W3 0.218; F_z -0.248; F_bg -0.301; deg_growth 0.050; btw_change -0.168), and the permutation p = 0.037 is in results/audit.json perm_p_value_one_sided. (c) The exp1 robustness table is still missing (GLMM agreement 0.163, probe agreement 0.10, refit CI [-0.092, 0.023], newborn_only / full_parent_sample / O2r_m50 / O2r_m20 / B5+offhome sensitivities, field-level with-data-only dAUC -0.010), as is the note that r_SB 0.58 is unaudited. (d) There are no refit CIs for the concept-level headline deltas (A*_h, D_ratio, G) or for O2r_resid +0.15. (e) There is no iteration-1 'why this iteration' paragraph. (f) The next-field entry numbers in 5.5 are still untraceable. (g) The 5.4 'B5 + all_four' row still carries the size_controlled_all_three numbers (0.697 -> 0.782, +0.085); F5 shows its refit CI95 is [-0.043, 0.220].",
 "suggested_action": "Paste F3 in full (34 rows: pooled rho, four within-group rhos, rho_logvol, rho_growth, LOGO delta-rho). Replace 4.4's partial table with all 12 rows (rho, CI90, CI95, groups positive) and cite audit.json for p = 0.037. Add the exp1 robustness table. Add refit CI columns to the 6.2 decisive table, and either recompute the O2r_resid refit CI or label it 'fixed-prediction CI only'. Add the iteration-1 reasoning paragraph. Relabel the 5.4 rows and add the F5 refit CI for every row."},
{"category": "evidence", "severity": "major",
 "description": "Many executed iteration-2 results are absent. Exp5 [art_wxWssKSUR45f]: sensitivities in h1_heldout.json (R_abs1 +0.0008, R_abs2, R_abs3, n_early>=5 -0.0004, newborn_only +0.0023 [-0.004, 0.013], excl_intersection_born); leave_one_field_out; the crossed concept x field (pigeonhole) bootstrap whose held-out CI [-0.0023, 0.0010] and DEV CI [-0.0056, 0.0013] are roughly 3-5x wider than the concept-only CIs the report presents as 'the only reported CIs'; T5 seed stability; the DEV rival head-to-head, where the relatedness pair is -0.00017 [-0.0017, 0.0012] on DEV, so its held-out +0.0034 was not seen in development; the per-group exploratory_domain_specificity table (gateway-P_j Spearman 0.83 in CS, -0.26 in PHYS), which is the actual evidence for the 'proxy for fields that keep things' claim; and the iteration-1 replication n and CI (85 episodes, 39 concepts, +0.023 [-0.004, 0.068], checks.json). Exp6 [art_N-mpomDZZ1ln]: the HMM trajectory model (6 states) and its HMM-vs-DTW ARI of 0.094, which is a direct robustness failure of the 'two stable classes' claim; the DTW k-selection grid (k=2 silhouette 0.29, lower bound of the stability ARI 0.81); the dev trajectory solution (66/62, with the localised class 55 Med + 7 Eng, 0 BGM, 0 CS); rescue models R1_s_other, R2_base, R2_full; the H1 replication in Exp6 (gateway b 0.005, p 0.70); relay_excess_ols (ret_x_top +0.288, p = 0.07, opposite in sign to the reported fepois); M2lost (relatedness to LOST fields, d = -0.063, LR p = 0.055); and the whole dev_result.json block (dev H2 robustness, planted control, power check).",
 "suggested_action": "Add an 'Exp5 robustness' table and an 'Exp6 robustness' table built from these keys. In 11.5, add the HMM result and the k-grid, and state that the two-class DTW solution is not reproduced by the HMM (ARI 0.09) and largely separates Medicine homes from the rest. In 10.5, state that the relatedness-pair gain is held-out only (DEV -0.0002). Add the pigeonhole CIs next to the concept-only CIs."},
{"category": "novelty", "severity": "major",
 "description": "The one confirmed positive result, H2 (relatedness to the currently retaining fields predicts the next field entered), is claimed as new in Section 14.4 because it 'goes beyond the principle of relatedness ... by using the concept's retaining community as the reference set'. The nearest neighbour is the standard Hidalgo et al. (2007) density itself. It is computed over the portfolio where the actor has REVEALED presence (RCA > 1), i.e. a thresholded, persistent presence, which is essentially 'retained'. Exp6's M0 baseline instead uses a non-standard density over ALL fields ever entered (method.py: 'sum_{j in entered(t-1)} phi[j,k] / sum_j phi[j,k]'). M1 beating M0 (LR 68.6) may therefore only show that the conventional thresholded density beats an unthresholded one. The M2lost result (relatedness to lost fields is negative-leaning, LR p = 0.055) supports that reading. Other close neighbours are not compared: Guevara et al. (2016) research space entry AUCs of 0.68-0.90; Chinazzi et al. (2019, EPJ Data Science, 'Mapping the physics research space') predicting country entry into PACS subfields from relatedness; Boschma, Balland & Kogler (2015) for technologies in cities. Absolute within-stratum AUCs are 0.817 for M1/M2 vs 0.809 for M0, and log field size alone reaches 0.757. The gateway weighting adds nothing (M3 vs M1 perm p = 0.17).",
 "suggested_action": "Add to M0 a density computed on the conventionally thresholded portfolio (fields where the concept's share exceeds its expected share at t-1, or retained fields by the R definition) and re-test M1 against it on the frozen held-out risk sets. The risk sets exist in entry_risk_sets_heldout.parquet, so this needs no new data. Report the M1 coefficient (d0_ret_rel 0.281 ± 0.032) as the headline, not the gateway-weighted one. Write down the Hidalgo 2007 / Guevara 2016 / Chinazzi 2019 comparison and what, if anything, survives it."},
{"category": "evidence", "severity": "major",
 "description": "The Dataset 2 source table (13.1) misstates coverage. Checked against out/coverage_report.json by_source: ACM CCS 1,298 concepts with events (report: 3,583, which is the external-entry count); MSC 1,121 (report 17,872 = entries); PACS/PhySH 2,635 (report 8,462 = entries); English Wikipedia 64,363 concepts with an event, 50,459 year-usable, 7,806 exact (report: 6,540); Wikidata 1,425 found, 1,316 year-usable; the curated lists are split as Gartner 466, MIT TR10 313, Research Fronts 589, NM MoTY 38, Science BOTY 53, PW BOTY 100 (the report lumps them as 589); JEL 213 found, 0 events. The dataset is also never used: O5 external recognition was built but not joined to any panel, so the request's 'externally documented recognition' ground truth still does not exist as an outcome.",
 "suggested_action": "Replace the table with n_with_event and n_with_year_usable_event per source from coverage_report.json, plus the per-group dated-taxonomy coverage (dated_domain_taxonomy_by_group). Record explicitly that O5 has not been evaluated against any indicator, and make joining O5 to the Exp5 frame (frame_concepts.csv, 12,499 concepts sharing legacy concept IDs) a zero-credit next step."},
{"category": "scope", "severity": "major",
 "description": "Coverage of the original request is partial, and the run has drifted. The request's core RQ1 deliverable is a 30-50 indicator screen of temporal KNOWLEDGE-NETWORK indicators (new edges, neighbourhood novelty, centrality change, community transitions, brokerage, clustering), with the ~10 strongest validated on held-out fields and results reported globally and per field. Iteration 2 tested only field-relatedness quantities from economic complexity (gateway eigenvector, phi_home, density) on the large panel. The co-occurrence and lineage indicators exist only on the 46-48 concept dev panels, and no indicator was ever validated on held-out concepts. Section 16 admits the indicator matrix has not been rescored. Also missing: the exploratory AI-first stage (step 1), external-recognition outcomes (built but unused), the 'explain why the strongest indicator works' analysis with case studies (Exp6 generated case field-flow figures that the report never mentions), and the learned model. There is no updated iteration-2 coverage table.",
 "suggested_action": "Add an iteration-2 column to the 8a coverage table. Make the next iteration's first priority computing the frozen concept-level co-occurrence indicator set (Exp3's ~30 ego-network indicators) on the Exp5 frame. The snapshot scan and frame already exist at zero credits. Then select the top ~10 on DEV and score them once on the sealed held-out groups against O1/O2r/O3 and O5."},
{"category": "methodology", "severity": "major",
 "description": "The iteration-2 design called for 'one common panel', but two incompatible panels were built, and the report does not say so. Exp5: 12,499 concepts, TAG rule (tag score >= 0.3 + title), Wikidata aliases, LLM precision gate, grounding benchmark with inter-LLM kappa 0.20 (deviations.json benchmark_kappa; the report quotes only the 90% LLM-hand agreement). Exp6: 653 newborn concepts, tag-AND-title, no Wikidata aliases, precision 0.996, a separate frame and episodes.csv. H1/H3 and H2/trajectories are therefore tested on different concept sets, grounding rules, home definitions and episode definitions: Exp6's 1,865 episodes against Exp5's 27,393. H2's held-out also includes the 2010-14 cohort of DEV-home fields. The Exp5 frame's onset agreement with P78 is 53% (|dt0| <= 1).",
 "suggested_action": "State in Section 9 or 11 that the common-panel design was not realised, and give a frame-comparison table (n concepts, grounding rule, precision, alias use, home rule, episode definition, overlap of concept IDs between the Exp5 and Exp6 frames). Either re-run H2 on the Exp5 frame (27k episodes) as a replication, or state that H2 is established only on the 653-newborn frame."},
{"category": "rigor", "severity": "minor",
 "description": "The power statements in 10.7 are misattributed and internally inconsistent. 'MDE 0.004 at 80% power' comes from h1_dev.json power, where b = 0.3 gives power 0.90 (b = 0.2 gives 0.65), so 0.004 is the 90% point. At b = 0 the CI>0 rule fires 12.5% of the time, versus a nominal 2.5%, indicating an anti-conservative concept-only bootstrap. The sentences about 'SD ~0.015 regardless of episodes' and '~34 concepts per group' come from Evaluation 1 (E_power), not Exp5, and imply an MDE floor of ~0.02, five times larger than 0.004. The report does not reconcile them.",
 "suggested_action": "Split 10.7 into Exp5 power (with the simulation grid and the null rejection rate 0.125) and Eval1 power (cite 12.6). Explain that the two differ because Eval1 includes a field random intercept and Exp5 does not, and say which one governs the H1 verdict."},
{"category": "clarity", "severity": "minor",
 "description": "Some summary statements overstate or mislabel results. 16.1 says H2 is 'positive in all three evaluable holdout field groups', but only Physical's CI excludes zero (LifeEnv LR p 0.23, Social 0.076; sign test over 4 is p = 0.0625). 14.2 says the principle of relatedness is 'confirmed for concept field retention' from a held-out-only dAUC of +0.0034 that is absent on DEV. 16 says 'two iterations and eight artifacts', but ten were commissioned and two failed. Exp6's first worker attempt crashed and was re-run, and this is not recorded.",
 "suggested_action": "Qualify each statement with the per-group CIs and the DEV value, and give artifact counts as 'ten commissioned, eight completed'."}
],
"results_reported": True,
"coverage": "partial",
"blocking": True,
"score": 3,
"confidence": 4
}
json.dump(out, open('.terminal_claude_agent_struct_out.json','w'), indent=2, ensure_ascii=False)
print("ok", len(out['critiques']))
PYEOF
python3 -c "import json;d=json.load(open('/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/review_report/review_report/.terminal_claude_agent_struct_out.json'));print(d['blocking'],d['score'])"
```

### [42] TOOL RESULT — Bash · 2026-09-28 21:00:32 UTC

```
{"stdout": "ok 11\nTrue 3", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] ASSISTANT · 2026-09-28 21:00:45 UTC

```
The review of the iteration-2 report is in `.terminal_claude_agent_struct_out.json`. I scored it 3/10 (confidence 4) and set it to blocking. Soundness is 1 because several stated conclusions contradict the artifacts' own result files.

**The numbers themselves check out.** I recomputed every headline number I traced from the result files, and all of them matched:
- **Experiment 5 (gateway retention on held-out data):** the gain is −0.00001 AUC, and the ladder and the relatedness-pair result (+0.0034) match.
- **Gateway landing and breadth (H3):** partial correlation 0.030 for G, pooled 0.068.
- **Experiment 6 (next field entered):** likelihood ratio 71.7, effect d = 0.30, plus the ordering and trajectory counts.
- **Evaluation 1 (replication):** the union-panel gain and the refit confidence intervals match.

So `results_reported` is true.

**Where the report contradicts its own evidence:**
- **Section 10.3** says the gateway-retention hypothesis failed "by all preregistered criteria". The result file shows one criterion passed: the within-field regression gives a positive coefficient, p = 0.041. The overall verdict still stands, but the sentence is false.
- **Ordering finding, listed as "confirmed":**
  - In Experiment 6's own regressions, retaining a gateway field is followed by *smaller* rises in disciplinary entropy.
  - Entropy was already rising three years before the first gateway retention.
  - On the development data, entropy predicts later gateway retention (p = 0.006), but the report calls the reverse direction "not significant" by quoting only the held-out value.
  - The "66% of broad concepts" is really 57 of 175 (33%); 65.5% is the share among the 87 untied cases.
- **Section 4.4** says 7 of the 12 partial associations are "not available". They are all in the iteration-1 file `exploratory_partial_association.json`.
- **The recognition dataset table** counts external entries as matched concepts: ACM 3,583 against 1,298 real matches, MSC 17,872 against 1,121, PACS 8,462 against 2,635. It also reports 6,540 Wikipedia concepts when 64,363 have a date.

**Other major issues:**
- **H3 is called "confirmed" without its caveats.** Its concept-bootstrap interval includes zero, and it shrank from about 0.14 on development data to 0.03 on held-out.
- **The novelty claim for the next-field result is weak.** The baseline density counts every field a concept ever entered. The standard Hidalgo density counts only fields with revealed, persistent presence, which is close to "retained". The "new" predictor may simply be the conventional measure beating a loose one. The report also doesn't compare it with Guevara 2016 or Chinazzi 2019.
- **Many executed results are missing,** including:
  - the Experiment 5 sensitivity checks, and the field-by-concept bootstrap intervals that are 3–5 times wider than the ones reported;
  - an HMM trajectory model that disagrees with the two-class solution (agreement 0.09);
  - the whole development-data result block for Experiment 6.
- **Most of last round's must-fix items are still open,** including the 34-indicator portability table (which Evaluation 1 already produced ready to paste) and the Experiment 1 robustness table.
- **The two iteration-2 experiments used different panels.** The planned common panel was never built, and the report doesn't say so.
- **Coverage is partial.** The 30–50 indicator screen was never run on the large panel, no indicator was validated on held-out data, and the external-recognition data was built but never used. Case studies and the learned model are also missing.

I also wrote a short `README.md` and an empty `.aii/manifest.yaml`; the workspace holds no heavy files.
```
