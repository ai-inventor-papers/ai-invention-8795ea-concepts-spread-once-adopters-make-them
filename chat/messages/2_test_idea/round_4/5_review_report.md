# review_report — test_idea

> Phase: `invention_loop` · round 4 · `review_report`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `review_report` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 04:46:56 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 04:47:02 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report/`:
GOOD: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report/file.py`, `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report/results/out.json`
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

All three candidates are tested against a shared five feature baseline: log early volume, publication growth, nonhome share, Shannon entropy and field reach, all computed over the first five years from onset. The shared evaluation protocol defines onset, outcomes and panel membership across all three experiments. The preregistered decision rule requires delta rho >= 0.10 with 90% bootstrap CI excluding zero, the same sign in at least three of four home field groups, split half reliability >= 0.60 and absolute Spearman with log volume and growth <= 0.60.

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

The size independence clause passes: A\*_h is not a proxy for concept volume or growth. But the gap adds nothing to the baseline on holdout fields, and it is not measured reliably enough (split half r_SB = 0.58, just below the bar).

### 3.4 Within field heterogeneity and reliability gradient

**[Correction, iteration 2.]** The values +0.45 and -0.18 reported in the original version of this subsection were the within group Spearman correlations of A\*_h with rarefied breadth (Medicine 0.446, Computer Science -0.184), not the group medians of A\*_h itself. The per group medians of A\*_h are negative in every group: Biochemistry/Genetics -0.256, Computer Science -0.303, Engineering -0.041, Medicine -0.182 [ARTIFACT:art_lwI2DuRtQRZX]. No group is "naturalised" on average; all four medians are borrowed. The finding that survives is that the direction of A\*_h's association with rarefied breadth flips across groups (positive in Medicine, negative in Computer Science and Biochemistry/Genetics), not that the level of A\*_h differs.

| Home group | N | Median A\*_h | IQR | Within group rho(A\*_h, O2r) |
|---|---|---|---|---|
| Biochemistry/Genetics | 13 | -0.256 | [-0.458, -0.132] | - |
| Computer Science | 21 | -0.303 | [-0.471, -0.064] | -0.184 |
| Engineering | 3 | -0.041 | [-0.103, -0.014] | - |
| Medicine | 11 | -0.182 | [-0.315, -0.095] | +0.446 |

The original claim that "A\*_h is partly a field composition indicator itself, despite the background adjustment" does not follow from these corrected numbers, which show all groups are borrowed but their association with breadth varies.

Reliability depends on sample size. Concepts with fewer than 60 nonhome children have split half reliability below 0.40, while the 11 concepts with 60 or more nonhome children reach r_SB = 0.72. On those 11 concepts, the eligible subset delta rho is +0.118 (90% CI [0.00, 0.36]), but this is too underpowered to interpret.

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

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] On heldout groups (Exp8), new_edge_rate transfers beyond B5 (pooled psp +0.118), whereas participation +0.150, NOV_res +0.139, D_rare +0.162 and D_ratio +0.066 are small but positive, so the iteration-1 conclusion that none adds to B5 does not hold on heldout data.

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

4. **Raw cooccurrence growth indicators.** Degree growth, strength growth and new edge rate growth are specific to Computer Science: positively correlated with rarefied breadth in Computer Science (rho 0.45 to 0.47) and near zero or negative in the other three groups (with the exception of new_edge_rate in Medicine at 0.35). They are growth confounded (Spearman with publication growth > 0.70). [Correction, iteration 4, from art_dFQ6jbgNsR6Q] The heldout test contradicts "specific to Computer Science" for new_edge_rate: pooled psp given B5 +0.118 [+0.072, +0.163] with 0 sign flips across the 4 heldout groups. Degree and strength growth do fail heldout (CIs include 0).

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

One zero credit scan of all 2,040 OpenAlex bulk snapshot parquet files (2026-09-23 snapshot; 476,196,327 works; 129.4 million base works 1995 to 2022). Concepts are identified by Aho-Corasick (a multi pattern string matching algorithm) title matching of 56,643 legacy OpenAlex concepts (levels 2 to 5) plus Wikidata aliases, with stemmed verification. The matched set contains 60.0 million verified concept paper pairs.

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

DerSimonian-Laird pooled delta AUC: -0.00004 (I squared = 0, Q = 1.69). The placebo is not exceeded and the conditional logit is null (beta = -0.075, z = -1.20, p = 0.23). [Correction, iteration 3, from art_7W9xiIO3FVBs] Verdict: **DISCONFIRMED** by the preregistered rule, which requires all six core criteria. The within field LPM criterion PASSES: beta = +0.068 per SD, concept clustered SE 0.033, p = 0.041 (two way clustered p = 0.17). The verdict rule still returns DISCONFIRMED because 5 of the 6 core criteria fail.

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

[Correction, iteration 3, from art_7W9xiIO3FVBs] H3 is **small; it passes the preregistered within group permutation rule, but the pooled concept bootstrap CI includes 0**. Heldout: G partial rho = 0.030 [-0.006, 0.065]; DL within group G = 0.068 [0.029, 0.107], I2 = 0.00; G_btw DL = 0.072 [-0.015, 0.159], I2 = 0.77 (negative in LifeEnv). The calibration check found 0 of 40 shuffled outcomes declared significant (a false positive rate check, not a p value). REL_home is strongly negative (-0.14), meaning that concepts whose home field is closely related to many other fields tend to achieve less size adjusted breadth.

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
| [Correction, iteration 3] Positive in 4/4 groups (sign test p = 0.0625) | Physical +0.33, LifeEnv +0.18, Social +0.24; only Physical's CI excludes 0 | Yes |
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

McNemar test comparing gateway vs peripheral: p = 0.088 (27 gateway only, 15 peripheral only). [Correction, iteration 3, from art_7W9xiIO3FVBs] Ordering is **mixed / not established**. The preregistered sign rule passes, but concept FE lead lag regressions show retention followed by SMALLER next year entropy gains (gateway b = -0.0279, p = 0.0007; peripheral b = -0.0434, p = 5.9e-08), a significant pretrend (event time -3: -0.072, p = 0.0002; DEV -0.088), and on DEV entropy predicting later gateway retention (b = 0.232 [0.066, 0.397], p = 0.0062; heldout b = 0.077, p = 0.22). The gateway permutation placebo is null (p = 0.63).

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

3. **Ordering: MIXED / not established.** [Correction, iteration 3, from art_7W9xiIO3FVBs] 57 of 175 broad concepts (32.6%) have the first retained gateway field preceding entropy takeoff; 57 of 87 nontied evaluable = 65.5%. The preregistered sign rule passes, but concept FE lead lag regressions show retention followed by SMALLER next year entropy gains, and on DEV entropy predicts later gateway retention (b = 0.232, p = 0.006).

4. **Background homophily dominates raw lineage (the background homophily measurement).** Two thirds of between concept variance in raw lineage log odds is general disciplinary homophily. This is confirmed across 48 dev concepts and is a methodological finding for any study using citation based cross field indices.

5. **Concept level gateway landing predicts volume residualised breadth (the breadth hypothesis, small effect).** [Correction, iteration 3, from art_7W9xiIO3FVBs] Holdout partial rho of G = 0.030 [-0.006, 0.065]; DL within group G = 0.068 [0.029, 0.107], I2 = 0.00. The preregistered permutation rule passes but the pooled concept bootstrap CI includes 0.

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



# Iteration 3

## 17. Why this iteration ran

The iteration-2 review raised 13 MUST FIX items and 2 MINOR items. The central objections were:

1. **The confirmed entry hypothesis result may not be new.** The reviewer pointed out that the standard Hidalgo et al. (2007) density is computed over fields where the actor has revealed comparative advantage (RCA > 1), which is effectively a thresholded, persistent presence. Experiment 6's entry baseline used an unthresholded ever entered density. the retaining relatedness model beating the entry baseline (LR 68.6) might only show that a conventional thresholded density beats an unthresholded one. The reviewer required adding a conventional RCA density rival (D_rca) and a share weighted current presence density (D_vol) to the entry model and testing whether retained field relatedness (d0_ret_rel) survives both.

2. **The indicator screen (research question 1) was still missing.** The request's core deliverable, a screen of 30 to 50 temporal knowledge network indicators with the strongest 10 validated on heldout fields, had not been attempted. The cooccurrence and lineage indicators existed only on the 46-48 concept dev panels, and no concept level indicator had been validated on heldout concepts.

3. **The external recognition outcome was built but never used.** Dataset 2 compiled recognition events for 65,026 concepts, but external recognition had not been joined to any panel or tested against any indicator.

4. **The record audit had not been run.** 246 claims across iterations 1-2 had not been checked against their source artifacts.

The hypothesis was updated to the "retained frontier" framing: we define the retained frontier as the set of fields that currently hold a concept above a persistence threshold, and predict that concepts spread from these fields to related ones. The retained field relatedness predictor (d0_ret_rel) must survive the conventional RCA density rival. The abandonment penalty (d_lost, relatedness to fields that dropped the concept) was a secondary claim. The mechanism draws on invasion biology: casual aliens (entered but lost) versus naturalised aliens (retained), following Richardson et al. (2000) [30] and Blackburn et al. (2011) [24].

Four artifacts were executed: a retained frontier robustness and replication test on an independent frame (Experiment 7), a heldout indicator screen (Experiment 8), a record audit and External recognition validation (Evaluation 2), and a prior art positioning study (Research 2) [ARTIFACT:art_research_2].


## 18. Experiment 7: Do concepts spread from fields that keep them? [ARTIFACT:art_experiment_7]

### 18.1 Design

This experiment tests whether retained field relatedness (d0_ret_rel) survives the rival that the iteration-2 reviewer identified: the conventional Hidalgo/Guevara RCA density (D_rca, computed over fields with RCA > 1) and a share weighted current presence density (D_vol). Step 1 confirms that d0 reproduces on the Experiment 6 frame and survives the rivals. Step 2 tests d0 on an independent frame: the Experiment 5 concepts minus all Experiment 6 concepts, a set the entry model has never touched.

The conditional logit is the same as Experiment 6: concept by year risk sets, where each concept year stratum includes all nonhome fields not yet entered, and the event is entry (at least 2 cumulative grounded papers). The entry baseline includes relatedness to home (phi_home), log field size, density over all ever entered fields, and the target field's own gateway centrality. The rival models add rivals and the focal predictor in sequence:

| Model | Covariates |
|---|---|
| Entry baseline | phi_home + log_size + density + gate_own (Experiment 6's baseline) |
| + RCA density | Entry baseline + D_rca_1y (RCA > 1 density, 1 year window) |
| + volume density | + D_vol (share weighted current presence density) |
| + retained relatedness | + d0_ret_rel (retained field relatedness) |
| + abandonment | + d_lost (relatedness to lost fields) |

### 18.2 Step 1: Reproduction on the Experiment 6 frame

The Experiment 6 heldout results reproduce exactly: the retaining relatedness model versus the entry baseline gives LR = 68.57, d0_ret_rel = 0.281. On the dev frame (274 concepts, 887 entries, 648 strata), d0_ret_rel survives both rivals:

| Model | d0_ret_rel | LR (step) | AUC within |
|---|---|---|---|
| R0 (M0 baseline) | - | - | 0.801 |
| R1 (+ D_rca_1y) | - | 30.2 (p = 4.0e-8) | 0.805 |
| R2 (+ D_vol) | - | 17.0 (p = 3.7e-5) | 0.810 |
| R3 (+ d0_ret_rel) | 0.215 | 29.3 (p = 6.1e-8) | 0.813 |
| R4 (+ d_lost) | 0.215 | 0.03 (p = 0.86) | 0.813 |

On the Experiment 6 heldout frame (369 concepts, 1,373 entries), d0_ret_rel = 0.262 with concept clustered SE = 0.031 and LR = 57.6 (p = 3.2e-14) in the retaining relatedness model. D_rca_1y is absorbed once d0 enters (its coefficient drops from 0.171 standalone to nonsignificant).

### 18.3 Step 2: Independent frame (Experiment 5 minus Experiment 6)

The independent frame comprises 11,841 Experiment 5 concepts not in the Experiment 6 newborn set (dropped by concept ID, Wikidata QID or label match). The heldout split includes 3,162 concepts (PHYS 656, LIFEENV 1,071, SOC 1,274, MATHDEC 161) with 6,978 entry events in 6,076 informative strata. The dev split has 4,302 concepts.

**Pooled heldout result (4 field groups):**

| Model | d0_ret_rel | LR (R3 vs R2) | n_events | n_strata |
|---|---|---|---|---|
| R3 (pooled4) | 0.322 [0.291, 0.355] | 325.8 | 6,978 | 6,076 |
| S_strict | 0.304 [0.268, 0.336] | - | - | - |

The S_strict estimator drops concepts with any ambiguity in the overlap exclusion. The crossed concept by target field pigeonhole bootstrap CI is [0.139, 0.333] on dev (wider than the concept only CI [0.222, 0.271] by a factor of approximately 4). VIF of d0_ret_rel in the full model: 1.92.

**Per heldout group:**

| Group | d0 (R3) | Boot 95% CI | LR | n_concepts |
|---|---|---|---|---|
| PHYS | 0.148 | [0.074, 0.219] | 13.8 (p = 2.0e-4) | 656 |
| LIFEENV | 0.401 | [0.347, 0.458] | 157.7 (p = 3.7e-36) | 1,071 |
| SOC | 0.297 | [0.245, 0.345] | 116.8 (p = 3.2e-27) | 1,274 |
| MATHDEC | 0.065 | [-0.110, 0.234] | 0.33 (p = 0.57) | 161 |

MATHDEC is null (CI includes zero, LR nonsignificant). PHYS shows a smaller but significant effect. LIFEENV is the strongest.

**DerSimonian-Laird meta analysis (4 heldout groups):**

| Estimand | DL pooled | 95% CI | I squared | Q |
|---|---|---|---|---|
| d0_ret_rel | 0.243 | [0.118, 0.368] | 0.92 | 36.2 |
| d_lost | -0.017 | [-0.045, 0.012] | 0.00 | 2.4 |

I squared of 0.92 indicates substantial heterogeneity across groups. Including cohort splits (DEV home cohort and non-DEV home cohort, both 2010-2014), the 6-unit DL pooled d0 is 0.281 [0.216, 0.345], I squared = 0.87.

**Cohort (2010-2014, both DEV home and other):**

| Cohort | d0 | Boot 95% CI | LR | n_concepts |
|---|---|---|---|---|
| Cohort DEV home | 0.304 | [0.272, 0.335] | 283.5 | 2,199 |
| Cohort non-DEV home | 0.338 | [0.293, 0.385] | 181.6 | 1,750 |

### 18.4 Dose response by persistence age

On dev (4,302 concepts), replacing d0_ret_rel with three dummy indicators for retention age shows a monotone nondecreasing dose response:

| Persistence age | d_ret coefficient | Boot 95% CI |
|---|---|---|
| 2 years | 0.056 | [0.019, 0.090] |
| 3 years | 0.103 | [0.058, 0.147] |
| >= 4 years | 0.251 | [0.226, 0.276] |
| Contrast (4+ minus 2) | 0.195 | [0.153, 0.236] |

Spearman correlation between beta and age = 1.0 (monotone nondecreasing). Permutation p (dose trend) = 0.001 (Holm corrected: 0.005).

### 18.5 Volume matched contrast

The volume matched contrast tests whether persistence predicts entry beyond current volume. Strata are matched on total concept volume (log field concept paper count), so that retained and not retained fields within each stratum have similar volume. On dev:

| Estimand | Coefficient | Boot 95% CI | LR |
|---|---|---|---|
| d0 (volume matched strata) | 0.069 | [0.019, 0.118] | 13.1 (p = 0.001) |

The volume matched d0 is positive and significant on dev, but the Holm corrected p on the full battery is 0.76 for the heldout volume matched contrast, which is null. **Verdict for criterion 5 (volume_matched_CI > 0): FAILS.** Persistence and volume are confounded in the heldout data.

### 18.6 Specificity tests

| Test | p value | Holm corrected |
|---|---|---|
| Label permutation (within stratum) | 0.001 | 0.005 |
| Rewired backbone | 0.004 | 0.009 |
| Node label permutation | 0.003 | 0.009 |
| Target field fixed effects | 3.98e-58 | 2.39e-57 |

All three specificity tests reject their nulls after Holm correction: the signal requires the specific backbone topology, the specific field labels, and the specific concept field assignments.

**Excluding intersection born concepts** (those with 2+ home fields): d0 = 0.255 (dev), essentially unchanged. **With target field fixed effects:** d0 = 0.241 (dev), retaining most of the signal. **With label coverage >= 0.5:** d0 = 0.236 (dev).

### 18.7 Guevara AUC comparison

Global (pooled, not within stratum) AUCs on the heldout pooled4 frame, computed over all candidate rows:

| Predictor | AUC |
|---|---|
| D_rca_cum alone | 0.635 |
| c_density alone | 0.637 |
| b_log_size alone | 0.772 |
| R3 linear predictor (full model) | 0.837 |

Guevara et al. (2016) report AUCs of 0.90 (individuals), 0.72 (organisations), 0.68 (countries) for RCA transition entry into research fields [16]. The comparison is not head to head: different units (concept vs scholar/organisation/country), different events (three publication count entry vs RCA transition), and different proximity measures (26-field PMI vs author sharing over subfields).

### 18.8 Exploratory: linear probability model

A frozen linear probability model (LPM) was fitted on heldout pooled4 to check whether d0_ret_rel's conditional logit effect translates to a linear entry probability:

| LPM variant | b | 95% CI | p |
|---|---|---|---|
| Frozen LPM | -0.001 | [-0.002, -0.001] | 0.0001 |
| Size deciles | -0.0004 | [-0.001, 0.0001] | 0.12 |
| Informative strata | -0.003 | [-0.005, -0.001] | 0.013 |
| Size deciles + informative | 0.0003 | [-0.002, 0.003] | 0.78 |

The LPM coefficient is negative (-0.001), not positive, because size nonlinearity absorbs the additive d0 effect. The conditional logit's within stratum d0 of 0.322 does not translate to a positive additive probability. This is an expected consequence of the heterogeneity in strata sizes: the LPM averages over strata where few fields are at risk (and d0's marginal probability effect is large) and strata where many fields are at risk (and the effect is diluted). The correlation between d0_ret_rel and log_size within strata is -0.249.

### 18.9 Abandonment penalty

The abandonment coefficient (d_lost, relatedness to fields that dropped the concept) is null on the independent frame:

| Estimand | d_lost | 95% CI |
|---|---|---|
| Pooled 4 groups (R4) | -0.007 | [-0.036, 0.022] |
| DL pooled 4 groups | -0.017 | [-0.045, 0.012] |
| DL pooled 6 units (+ cohort) | -0.006 | [-0.025, 0.012] |

All CIs include zero. Verdict: **ABANDONMENT = INCONCLUSIVE** (negative point estimate, not significantly different from zero).

### 18.10 Verdict

| Criterion | Passes? |
|---|---|
| 1. Pooled4 R3 CI > 0 | Yes |
| 2. S_strict CI > 0 | Yes |
| 3. Sign rule (positive in >= 3 of {PHYS, LIFEENV, SOC}) | Yes (3/3; MATHDEC excluded by plan) |
| 4. Permutation p < 0.05 | Yes (label 0.001, rewire 0.004, node label 0.003) |
| 5. Volume matched CI > 0 | **No** (Holm p = 0.76) |
| 6. EXP6 R3 CI > 0 | Yes |

**FRONTIER = PARTIAL: persistence confounded with volume.** d0_ret_rel survives the RCA and volume density rivals in the conditional logit (criteria 1-4, 6), but the volume matched contrast is null on heldout data (criterion 5). The conditional logit shows that fields with higher retained relatedness are entered next, beyond RCA density and current volume density, but we cannot rule out that retention is a proxy for sustained volume rather than an independent signal of adapted knowledge.

### 18.11 Deviations

- The primary sample is the Experiment 5 frame minus Experiment 6 (by ID, QID and label), not a fully independent draw; 7 home field mismatches were found (17 of 11,841 concepts).
- The crossed bootstrap scope covers dev only (500 draws), not heldout.
- MATHDEC was excluded from the sign rule because its CI includes zero and its sample is small (161 concepts).
- RCA ties (D_rca_1y = 1 in fields where the concept is exactly at RCA parity) occur for 0 of 7,241 dev strata.
- Standardisation uses min(conditional probability) capping within stratum.

[FIGURE:fig_frontier_ladder]


## 19. Experiment 8: Heldout portability of early network indicators [ARTIFACT:art_experiment_8]

### 19.1 Design

This experiment addresses the reviewer's central scope objection: the request's core indicator screen deliverable, a screen of 30 to 50 temporal knowledge network indicators with the strongest validated on heldout fields, had never been attempted. Experiment 8 computes 53 indicators in 7 families over the early window t0 to t0+2 for all 12,499 concepts on the Experiment 5 frame, selects the top 10 on dev (by partial Spearman priority, PSP, conditional on the five feature baseline), and tests them once on heldout groups.

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] The 6 indicator families are (entropy, reach, offhome share, log volume and growth belong to the B5 baseline, not to an indicator family; O5 is an outcome, not an indicator family):

1. **A: cooccurrence ego network** (27 indicators): D_z, D_ratio, D_rare, D_sub, D_obs, NOV, NOV_res, F_res, F_z, deg_W1, deg_W3, deg_growth, str_growth, new_edge_rate, edge_persistence, turnover, participation, n_comm_W3, comm_entropy, comm_transitions, ego_density_W3, ego_density_change, btw_end, btw_change, kcore_end, constraint_end, constraint_change
2. **E: popularity / volume** (6): share, growth_ind, accel, burst, author_growth, n_authors_early
3. **F: disciplinary spread** (3): log_offhome_volume, rao_stirling, fields_gained_per_yr
4. **FR: retained frontier / relatedness to entered fields** (7): CONTACT_REACH, RETAINED_REACH, RETENTION_RATIO_early, FRONTIER_POTENTIAL, D_rca_end, D_vol_end, M0_density_end
5. **G: landing on gateway fields** (7): G, G_A, G_btw, G_deg, G_phimin, REL_home, RS
6. **S: coauthor (social) reach** (3): S_comp, S_comp_n, S_isolated_share

D family indicators (D_ratio, D_rare, D_z, D_sub, D_obs) have high DEV missing shares (0.31 to 0.88) because they require M >= 3 or M >= 10 cooccurrence neighbours; the DEV eligibility rule excludes indicators with more than 30% missing.

The outcomes are:

- **O2r_m50:** rarefied field breadth at m = 50 (primary)
- **O2r_resid:** O2r_m50 residualised on log volume (breadth conditional on size)
- **O1c:** sustained uptake (binary)
- **Transience:** transience (binary, years with zero offhome papers / years observed)
- **External recognition / Wikipedia-Wikidata only:** external recognition (binary; O5_WW = Wikipedia/Wikidata only)

The frame has 12,499 concepts: DEV 4,771 (CS 373, Eng 1,345, BGM 483, Med 2,570); heldout PHYS 742, LIFEENV 1,113, SOC 1,352, MATHDEC 165; cohort 4,356 (DEV home 2,484, other 1,872).

**Second use disclosure:** The Experiment 5 heldout concepts were previously unsealed for gateway retention and breadth testing, so their sustained uptake, transience and breadth outcomes are not fully naïve. The approximately 50 other indicators were never scored on heldout rows. The G family (G, G_A, G_btw) was scored once before on O2r_resid and its heldout rows are flagged as previously scored (not confirmatory).

### 19.2 O2r_m50 results: 7 of 10 confirmed

The top 10 indicators selected on dev (by partial Spearman priority conditional on the five feature baseline) were tested once on heldout groups. DerSimonian-Laird pooled betas and Holm corrected permutation p values:

| Indicator | Family | Pooled beta | 95% CI | I squared | Holm p | Sign agree | Confirmed? |
|---|---|---|---|---|---|---|---|
| M0_density_end | Relatedness | +0.375 | [+0.279, +0.462] | 0.74 | 3.9e-12 | 6/6 | **Yes** |
| D_vol_end | Relatedness | +0.307 | [+0.256, +0.356] | 0.10 | 3.7e-28 | 6/6 | **Yes** |
| CONTACT_REACH | Relatedness | +0.211 | [+0.161, +0.261] | 0.00 | 9.3e-15 | 6/6 | **Yes** |
| n_comm_W3 | Cooccurrence | +0.167 | [+0.063, +0.267] | 0.78 | 8.8e-3 | 6/6 | **Yes** |
| NOV | Cooccurrence | +0.151 | [+0.044, +0.255] | 0.75 | 2.3e-2 | 6/6 | **Yes** |
| RETENTION_RATIO_early | Relatedness | -0.114 | [-0.160, -0.067] | 0.00 | 1.3e-5 | 6/6 | **Yes** |
| ego_density_W3 | Cooccurrence | -0.102 | [-0.151, -0.053] | 0.00 | 2.9e-4 | 6/6 | **Yes** |
| RS | Relatedness | -0.072 | [-0.153, +0.010] | 0.44 | 0.156 | 5/6 | No |
| G_btw | Centrality | +0.056 | [-0.006, +0.118] | 0.33 | 0.156 | 6/6 | No |
| log_offhome_volume | Volume | -0.089 | [-0.171, -0.007] | 0.63 | 0.102 | 5/6 | No |

Seven of 10 indicators have Holm corrected p < 0.05 and 95% CI excluding zero. The three that fail (RS, G_btw, log_offhome_volume) have CIs touching or including zero after Holm correction.

The confirmed indicators span three families: relatedness (M0_density_end, D_vol_end, CONTACT_REACH, RETENTION_RATIO_early), cooccurrence topology (n_comm_W3, NOV, ego_density_W3), and none from centrality or volume alone. Two confirmed indicators have negative signs: RETENTION_RATIO_early (the share of early offhome fields that persist; concepts with higher early retention spread less broadly, suggesting that early lock in limits later diffusion) and ego_density_W3 (concepts with denser ego networks in the cooccurrence graph spread less, suggesting redundancy reduces diffusion).

### 19.3 O2r_resid results: 8 of 10 confirmed

O2r_resid (breadth conditional on volume) adds one indicator to the confirmed set: **log_offhome_volume** (-0.100 [-0.171, -0.028], Holm p confirmed). Concepts with higher early offhome volume achieve less breadth than expected for their total size.

### 19.4 O1c (sustained uptake): 1 of 10 confirmed

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] Only n_authors_early is confirmed for O1c: pooled psp +0.161 [+0.090, +0.230], Holm p 0.0001 (1 of 10 frozen indicators).

### 19.5 O4 (field- and year normalised citation growth): 2 of 10 confirmed

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] This section reports O4, not transience. The original Section 19.5 was headed "Transience" but reported O4 results. Concepts whose home field is related to many fields (REL_home) show LOWER later citation growth, and early author growth predicts HIGHER citation growth.

| indicator | family | frozen sign | pooled psp | 95% CI | I2 | Holm p | sign agree | confirmed |
|---|---|---|---|---|---|---|---|---|
| REL_home | G | - | -0.114 | [-0.180, -0.047] | 0.69 | 0.00922 | 6/6 | **yes** |
| author_growth | E | + | +0.065 | [+0.024, +0.106] | 0.21 | 0.0182 | 5/6 | **yes** |
| G_deg | G | - | -0.021 | [-0.069, +0.028] | 0.41 | 1 | 5/6 | no |
| log_offhome_volume | F | - | -0.002 | [-0.069, +0.066] | 0.66 | 1 | 3/6 | no |
| burst | E | - | +0.014 | [-0.043, +0.072] | 0.55 | 1 | 3/6 | no |
| G_A | G | - | -0.010 | [-0.055, +0.036] | 0.33 | 1 | 4/6 | no |
| G_phimin | G | + | +0.064 | [-0.080, +0.206] | 0.93 | 1 | 5/6 | no |
| FRONTIER_POTENTIAL | FR | - | -0.017 | [-0.063, +0.030] | 0.39 | 1 | 5/6 | no |
| RETENTION_RATIO_early | FR | - | -0.026 | [-0.060, +0.009] | 0.00 | 1 | 5/6 | no |
| new_edge_rate | A | - | +0.003 | [-0.032, +0.037] | 0.00 | 1 | 3/6 | no |

### 19.5b O3 (transience): 1 of 10 confirmed

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] For transience (O3, binary; groups with an estimable O3), only n_authors_early is confirmed; MATHDEC has too few transient concepts for O3, so sign agreement is out of 5.

| indicator | family | frozen sign | pooled psp | 95% CI | I2 | Holm p | sign agree | confirmed |
|---|---|---|---|---|---|---|---|---|
| n_authors_early | E | + | +0.089 | [+0.031, +0.148] | 0.00 | 0.0286 | 4/5 | **yes** |
| S_comp_n | S | + | +0.068 | [+0.001, +0.134] | 0.10 | 0.406 | 4/5 | no |
| rao_stirling | F | + | +0.066 | [-0.002, +0.134] | 0.22 | 0.446 | 3/5 | no |
| G_deg | G | + | +0.036 | [-0.007, +0.079] | 0.00 | 0.586 | 4/5 | no |
| CONTACT_REACH | FR | + | +0.049 | [-0.003, +0.101] | 0.00 | 0.452 | 5/5 | no |
| M0_density_end | FR | + | +0.038 | [-0.011, +0.086] | 0.00 | 0.655 | 4/5 | no |

### 19.6 External recognition (O5, O5_WW): 0 and 0 of 10 confirmed

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] No indicator predicts external recognition beyond B5 + onset year. All Holm p = 1.0. This is consistent with the Evaluation 2 finding that external recognition is unrelated to publication outcomes (Section 20.2).

### 19.7 Learned models vs B5 vs B5 + best single (heldout groups pooled)

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] All 8 outcomes; Spearman(pred, y) for continuous outcomes, AUC for binary (O1c, O1b, O3, O5, O5_WW).

| outcome | n | B5 | B5 + best single | ElasticNet / L1-logit (all) | EBM |
|---|---|---|---|---|---|
| O1c | 3,372 | 0.312 | 0.305 [-0.016, +0.004] | 0.303 [-0.019, -0.001] | 0.313 [-0.022, +0.026] |
| O2r_m50 | 1,833 | 0.706 | 0.739 [+0.022, +0.045] | 0.765 [+0.046, +0.073] | 0.757 [+0.037, +0.067] |
| O2r_resid | 1,833 | 0.704 | 0.738 [+0.023, +0.047] | 0.763 [+0.047, +0.071] | 0.756 [+0.038, +0.066] |
| O4 | 3,372 | 0.015 | 0.028 [-0.009, +0.036] | constant (all coefficients 0) | 0.188 [+0.129, +0.219] |
| O1b | 3,372 | 0.507 | 0.518 [-0.003, +0.029] | 0.524 [-0.000, +0.039] | 0.526 [-0.001, +0.042] |
| O3 | 3,372 | 0.506 | 0.576 [+0.020, +0.128] | 0.599 [+0.028, +0.163] | 0.599 [+0.033, +0.161] |
| O5 | 1,417 | 0.746 | 0.742 [-0.013, +0.003] | 0.747 [-0.009, +0.009] | 0.726 [-0.038, -0.004] |
| O5_WW | 1,671 | 0.747 | 0.746 [-0.007, +0.005] | 0.751 [-0.003, +0.010] | 0.719 [-0.046, -0.011] |

Transience (O3) IS predictable beyond B5 on heldout groups: L1-logit AUC 0.599 vs B5 0.506 (paired difference [+0.028, +0.163]); EBM 0.599. Caveat: B5 itself is at chance for O3, so the gain is over a null baseline, not over a strong one. The O4 signal is nonlinear: the ElasticNet set every coefficient to zero, while the EBM reaches Spearman 0.188 vs B5 0.015.

### 19.8 Preregistered verdicts

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] The table below quotes the exact frozen preregistered prediction text.

| # | exact frozen text | verdict | deciding quantity |
|---|---|---|---|
| P1 | entropy, D_rare, D_ratio, participation, NOV_res: raw Spearman with O2r_m50 > 0 (CI > 0) in >= 3 of 4 heldout groups; AND D_rare, D_ratio, participation, NOV_res: pooled psp\|B5 CI upper bound < 0.10 | **FAILS** | raw part: D_rare 2/4, D_ratio 3/4, participation 4/4, NOV_res 4/4, entropy 4/4; adds little part: upper bounds D_rare 0.296, D_ratio 0.132, participation 0.271, NOV_res 0.241 (rule: all < 0.10) |
| P2 | edge_persistence: pooled raw rho and pooled psp with O2r_m50 both < 0 | **HOLDS** | edge_persistence pooled psp -0.080 [-0.126, -0.033]; mean raw rho over 4 groups -0.128 |
| P3 | deg_growth, str_growth, new_edge_rate FAIL heldout: pooled psp CI includes 0 OR sign flip in >= 2 of 4 groups | **FAILS** | new_edge_rate pooled psp +0.118 [+0.072, +0.163], sign flips 0 -> it TRANSFERS; deg_growth +0.002 and str_growth +0.001 do fail as predicted |
| P4 | RETENTION_RATIO_early and FRONTIER_POTENTIAL: pooled psp > 0 with CI > 0 for O2r_resid AND O1c | **FAILS** | RETENTION_RATIO_early on O2r_resid -0.120 [-0.166, -0.074] (predicted > 0: wrong sign); FRONTIER_POTENTIAL on O2r_resid +0.055 [-0.057, +0.165] |
| P5 | CONTACT_REACH: pooled psp CI includes 0 (also reported given B5 minus reach) | **FAILS** | CONTACT_REACH pooled psp on O2r_m50 +0.213 [+0.159, +0.265] (predicted: CI includes 0) |

P1 fails on BOTH parts. P3 was a prediction of FAILURE; its failure means new_edge_rate transfers to heldout groups. P4 fails because the retention ratio has the opposite sign. P5 predicted that CONTACT_REACH adds nothing; it adds a clearly positive amount.

### 19.9 Deviations

- One year ego network windows (t0 to t0+1 and t0+1 to t0+2) instead of three year windows, because the snapshot scan produces yearly slices.
- Betweenness centrality capped at concepts with degree >= 3 in each window, to avoid division by zero in normalisation.
- O2r_resid computed per the plan formula (residual of O2r_m50 on log_total_volume, linear).
- External recognition uses a linear onset year term, not a quadratic, because the quadratic was numerically unstable for extreme onset years.
- D_vol_end and M0_density_end use the cumulative 1995 to t0+2 field concept paper history, not a rolling window.
- The transience ElasticNet shrank all coefficients to zero, so no linear model is available for transience.

[FIGURE:fig_rq1_confirmed]


## 20. Evaluation 2: Record audit and external recognition validation [ARTIFACT:art_evaluation_2]

### 20.1 Record audit

An independent audit of 246 claims across iterations 1-2. Each claim was matched to its source artifact output file and compared with the reported value.

| Status | Count |
|---|---|
| MATCH | 224 |
| MISLABELLED | 15 |
| MISMATCH | 6 |
| FILE_FLAG_OVERRIDDEN | 1 |
| **Total** | **246** |
| Blocking items | 58 |

The 15 MISLABELLED items are claims where the report's label for a value was wrong but the value itself was correct (e.g. reporting a within group correlation as a median). The 6 MISMATCH items are values that disagree with the source file. 58 items were flagged as blocking and fed into the iteration-3 corrections (many of these overlap with the reviewer's MUST FIX list).

### 20.2 External recognition validation

The external recognition outcome from Dataset 2 was joined to the Experiment 5 frame (12,499 concepts). Key findings:

**Base rate:** 23.8% of heldout concepts have at least one usable external recognition event (O5_main).

**Correlation with publication outcomes (DerSimonian-Laird pooled over 4 heldout groups):**

| Outcome | Pooled rho with O5_main | 95% CI |
|---|---|---|
| O1 (sustained uptake) | 0.001 | [-0.033, 0.034] |
| O2r_m50 (rarefied breadth) | 0.014 | [-0.045, 0.073] |
| O2r_resid | 0.014 | [-0.046, 0.075] |
| O3 (transience) | -0.049 | [-0.083, -0.016] |

External recognition is **unrelated** to publication based breadth and uptake outcomes. It has a weak negative association with transience (concepts recognised externally are slightly less transient), but the effect is small and not robust across groups.

**Precedence leakage:** 67% of concepts have their first recognition event at or before onset year t0. The median lag between onset and recognition is 6-8 years for taxonomies (ACM CCS, MeSH) and 1 year for curated lists (Gartner Hype Cycle). This means external recognition is measuring preexisting recognition, not outcome of diffusion recognition, for the majority of concepts.

### 20.3 External recognition handcheck (100 items)

| Metric | Value | 95% CI (Wilson) |
|---|---|---|
| Precision (strict) | 0.86 | [0.74, 0.93] |
| Precision (lenient, partial counts) | 0.96 | - |
| Date error <= 1 year | 95% | - |
| False negative rate | >= 0.14 | [0.07, 0.26] |
| Share of positives marking genuinely new concept | 42% | - |

Precision by source: Wikipedia 1.00 (n = 20), taxonomy 0.88 (n = 8), MeSH 0.80 (n = 10), Wikidata 0.80 (n = 5), curated lists 0.57 (n = 7). Wikipedia dates are the most reliable (95% within 1 year). The false negative rate is at least 14% (checked against Wikipedia only; taxonomies not checked for false negatives).

**FIT_FOR_USE:** True (precision >= 0.85 and date error <= 1 year in >= 80% of checked positives). However, only 42% of positives mark genuinely new concept emergence; the remainder are recognition events for long established phenomena that acquired a particular label.


## 21. Research 2: Prior art and venue positioning [ARTIFACT:art_research_2]

### 21.1 Retained frontier claim positioning

The prior art search covered 6 strands: economic complexity, relatedness in science, export learning, regional exit, invasion biology, and idea diffusion. The verdict:

**Claim A (entry follows retained relatedness): PARTIALLY ANTICIPATED (weak partial).** The relatedness literature uses persistence routinely, but only as a filter on the *outcome* (what counts as an entry). Pinheiro et al. (2022) require RCA < 1 for Δ = 4 years before and RCA >= 1 for Δ years after an entry [25]. Albora et al. (2023) count activation only if RCA < 0.25 in all previous years [26]. Bahar et al. (2014) use tenfold jumps from RCA <= 0.1 [27]. On the *predictor* side, every density found in all 6 strands uses current snapshot presence (RCA > 1, or continuous) [15, 16, 19, 31]. No paper was found that builds density from retained or persistent presences only, or weights presences by duration, and tests it against RCA > 1 density. The closest science analogue is Cheng et al. (2023), who find that what they call "consistent intellectual usage" predicts ideas becoming core [4], but their measure is global, not per field.

**Claim B (lost field penalty): mechanism partly anticipated; NEW as a test.** Fernandes & Tang (2014) model negative neighbour signals deterring entry [28]. Nomaler & Verspagen (2022) argue absence or loss of comparative advantage is informative but add little in practice [29]. No study uses neighbours' exits as entry predictors. Our Experiment 6 estimate is fragile: d_lost = -0.063, p = 0.055. The independent frame estimate (Experiment 7) is d_lost = -0.007, CI including zero. The abandonment penalty remains inconclusive.

### 21.2 Missing rivals

The positioning study identified several rivals the present analysis does not test:

1. **Persistence filtered RCA density** (D_rca_persist_k): entered or RCA > 1 in each of t-k to t. This is the predictor side twin of Pinheiro's Δ-rule and would directly test whether Claim A's novelty is in the persistence measure or just in the threshold.
2. **Own preentry subthreshold intensity** (Albora's autocorrelation benchmark): whether a concept's own past presence in a field predicts entry, beyond relatedness.
3. **Neighbour momentum density:** relatedness weighted recent usage growth in adopting fields, following Fernandes & Tang (2014) [28]. This is the main confound for both claims.

These are flagged as open and should be tested in a future iteration.

### 21.3 Indicator screen comparison

No comparator in the literature evaluates on heldout fields. Link forecast AUCs (Krenn & Zeilinger 2020: AUC 0.85 with approximately 5% of edges drawn; Maillart et al. 2026 [22]: AUC 0.95-0.97) are level metrics on rare positives and not comparable to our increments over the five feature baseline. The indicator screen heldout result (7 of 10 indicators confirmed, ElasticNet delta +0.059 over the five feature baseline) has no like for like counterpart and should be presented as such.

### 21.4 Venue

The Applied Network Science collection titled "Networks for everyday life" has submissions open 24 June 2026 and deadline 30 November 2026. Scope items include "Information diffusion and communication networks in digital societies" and "Innovation, collaboration, and knowledge exchange networks across sectors." The collection page was IdP blocked and the editor list is unrecovered.

ANS SciSci articles (Cunningham 2022, Fontaine 2024, Holmgren 2023) use unstructured abstracts of 120-260 words, 7-13 figures, 0-4 tables, and 29-40 references. Recommended skeleton: Introduction stating both research questions, Related work, Data and methods, indicator screen results, trajectory results, Discussion, Conclusions, Back matter.


## 22. Dead ends and negative results from iteration 3

1. **Volume matched contrast for the retained frontier hypothesis: NULL on heldout data.** d0_ret_rel's coefficient in the volume matched conditional logit is positive on dev (0.069, p = 0.006) but the heldout Holm corrected p is 0.76. We cannot separate persistence from volume as a predictor of field entry.

2. **Abandonment penalty (d_lost): INCONCLUSIVE.** d_lost is null on the independent frame (DL pooled -0.017 [-0.045, 0.012]). The Experiment 6 estimate (-0.063, p = 0.055) does not replicate. Relatedness to lost fields neither helps nor hurts entry prediction beyond the retained and RCA density terms.

3. **MATHDEC group: NULL.** d0_ret_rel = 0.065 [-0.110, 0.234] on the heldout MATHDEC group (161 concepts). The small sample precludes any conclusion for mathematics and decision sciences.

4. **LPM exploratory: NEGATIVE coefficient.** The linear probability model gives b = -0.001 for d0_ret_rel because size nonlinearity absorbs the additive effect. This limits the practical interpretability of d0 in a linear setting.

5. **External recognition as an outcome: UNRELATED to publication outcomes.** External recognition has pooled rho 0.014 with rarefied breadth and 0.001 with sustained uptake. It cannot serve as a validation outcome for the indicator screen. The 67% precedence leakage (recognition at or before t0) means external recognition measures prior recognition, not diffusion success.

6. [Correction, iteration 4, from art_dFQ6jbgNsR6Q] **O4 (citation growth) linear model: shrank to a constant.** The ElasticNet for O4 (field- and year normalised citation growth, NOT transience) set every coefficient to zero, so it ranks nothing on heldout data, while the EBM reaches Spearman 0.188 vs B5 0.015 (gain +0.174 [+0.129, +0.219]). The O4 signal is nonlinear. Transience (O3) is a separate outcome with a positive heldout learned model result (L1-logit AUC 0.599 vs B5 0.506).

7. [Correction, iteration 4, from art_dFQ6jbgNsR6Q] **Four of five preregistered predictions fail, as frozen.** P2 (edge_persistence negative) holds. P1 fails (the iteration-1 breadth candidates do add beyond B5 on heldout data); P3 fails because new_edge_rate transfers; P4 fails because RETENTION_RATIO_early is negative, not positive; P5 fails because CONTACT_REACH is positive given B5. See the table in 19.8 for the deciding numbers.

8. **G_btw (betweenness centrality) for O2r_m50: NOT CONFIRMED.** G_btw pooled beta = +0.056 [-0.006, +0.118], Holm p = 0.156. This is the iteration-2 breadth hypothesis indicator rescored on the full indicator screen; it does not survive Holm correction.

9. **RS (relatedness support) for O2r_m50: NOT CONFIRMED.** RS pooled beta = -0.072 [-0.153, +0.010], Holm p = 0.156. The sign is negative (concepts with more relational support spread less broadly), opposite to the naive prediction.

10. **External recognition for all indicators: NULL.** No early indicator predicts whether a concept will be recognised externally. All Holm p = 1.0 across both external recognition variants and all 10 tested indicators.

11. [Correction, iteration 4] **Experiment 9 (trajectory typology and sequence tests): did not run.** The worker failed before producing output (output format validation failed after 5 retries). The workspace holds no analysis code and no results. What was lost: the RQ2 trajectory typology and sequence tests for iteration 3. Status: **not run, not refuted**. The work was recovered in iteration 4 (Experiment 12).


## 22a. Coverage of the original request (updated)

| Step | Iteration 1 | Iteration 2 | Iteration 3 |
|---|---|---|---|
| RQ1: candidate indicator screen (dev) | Done (3 candidates) | Not extended | Done (53 indicators, 7 families) |
| RQ1: holdout evaluation | Not started | Frame built (12,499) | Done (7/10 confirmed for O2r_m50) |
| RQ1: top-10 on holdout | Not started | Not started | Done |
| RQ1: external ground truth (O5) | Not started | Built (64,723 concepts) | Validated: unrelated to breadth/uptake |
| RQ1: exploratory AI first stage | Not started | Not started | Not started |
| RQ1: learned model | Not started | Not started | Done (ElasticNet +0.059, EBM +0.052 over B5) |
| RQ2: diffusion trajectories | Not started | Done (2 classes, ARI 0.54) | Not extended |
| RQ2: field entry conditional logit | Partial (dev) | Done (confirmed, d = 0.30 holdout) | Robustness: d0 survives D_rca + D_vol rivals |
| RQ2: retained frontier test | Not started | Not started | Done: PARTIAL (persistence ~ volume confound) |
| Grounding benchmark | Not started | Done (precision 0.947, recall 0.659) | Audited (WP1) |
| Explain why strongest indicator works | Not started | Not started | Not started |
| Case studies | Not started | Not started | Not started |
| Record audit | Not started | Not started | Done (246 claims, 224 match, 6 mismatch) |

Still open: AI first stage (exploratory nonlinear indicator screening), case studies, "explain why strongest indicator works" analysis, persistence filtered RCA density rival (D_rca_persist_k), and neighbour momentum density confound.


## 23. What we have learned so far (end of iteration 3)

*See updated summary at end of iteration 4 (Section 31).*



# Iteration 4

## 24. Why this iteration ran

The iteration-3 review raised 10 MUST FIX items. The central objections were:

1. **The OPEN index had not been tested on a confirmatory cohort.** The 7 confirmed breadth indicators from Experiment 8 were selected and tested on the same unsealed heldout groups. A never screened 2015-2016 onset cohort was required to confirm the composite OPEN signal.

2. **Half of the M0_density_end and D_vol_end signal might be preonset footprint.** Many concepts have offhome papers before their onset year. The two strongest breadth predictors could partly reflect established presence rather than early network dynamics.

3. **The trajectory analysis (Experiment 9) had failed.** No breadth decomposition, no trajectory typology beyond the iteration-2 two class DTW, no sequence tests and no case studies existed.

4. **Prior art positioning was incomplete.** The openness versus consolidation framing needed strand by strand extraction and a contribution statement.

5. **The report contained 6 MISMATCH and 15 MISLABELLED claims** from the Evaluation 2 audit that had not been corrected in place.

Four artifacts were executed: a confirmatory cohort test of the OPEN index (Experiment 10, art_NMe386dX9GLF), a breadth decomposition and trajectory analysis (Experiment 12, art_uw4OeagJP3rv), a boundary study with specification curve and corrections pack (Evaluation 3, art_oKOd21ZMnu9S), and a novelty positioning study (Research 3, art_hSyVUBa2okT2).


## 25. Experiment 10: Confirmatory cohort test of the OPEN index [ARTIFACT:art_NMe386dX9GLF]

### 25.1 Design

The OPEN index is the mean of six signed z scored ego network components from the early window (t0 to t0+2): new_edge_rate (+), n_comm_W3 (+), participation (+), NOV_res (+), ego_density_W3 (−), edge_persistence (−). Three builds are tested: OPEN_home (home field cooccurrence graph only), OPEN_all (corpus wide graph), and OPEN_sizematch (size matched random reference graph). The confirmatory cohort comprises concepts with onset years 2015-2016, never used in any prior screen or selection.

### 25.2 Control ladder

A six rung control ladder tests OPEN's partial Spearman priority (PSP) with rarefied field breadth (O2r_m50) conditional on increasingly demanding baselines:

| build | outcome | R0 (B5+onset) | R1 (+contact_reach) | R2 (+concept_type) | R3 (+footprint) | R4 (+coverage) | R5 (+group_FE) | n |
|---|---|---|---|---|---|---|---|---|
| OPEN_home | O2r_m50 | +0.123 [+0.041, +0.205] | +0.097 [+0.018, +0.179] | +0.091 [+0.013, +0.171] | +0.080 [+0.001, +0.162] | +0.069 [-0.012, +0.150] | +0.056 [-0.022, +0.135] | 573 |
| OPEN_all | O2r_m50 | +0.205 [+0.125, +0.281] | +0.180 [+0.100, +0.259] | +0.174 [+0.092, +0.253] | +0.171 [+0.088, +0.251] | +0.147 [+0.064, +0.224] | +0.138 [+0.055, +0.218] | 630 |
| OPEN_sizematch | O2r_m50 | +0.183 [+0.103, +0.257] | +0.154 [+0.074, +0.230] | +0.147 [+0.068, +0.221] | +0.137 [+0.057, +0.212] | +0.124 [+0.045, +0.202] | +0.113 [+0.035, +0.190] | 591 |

OPEN_home at the concept type rung (the primary registered test): PSP = +0.091 [+0.013, +0.171], Holm p = 0.048. OPEN_all and OPEN_sizematch survive all six rungs with confidence intervals excluding zero.

### 25.3 Per-group DerSimonian-Laird pooling (concept type rung, rarefied breadth)

| build | CS+Eng | BGM+Med | PHYS | LIFEENV | SOC | MATHDEC (report only) | DL pooled [95% CI] | I2 | positive / 5 |
|---|---|---|---|---|---|---|---|---|---|
| OPEN_home | +0.043 (n=114) | +0.080 (n=277) | NA (n=27) | +0.007 (n=49) | +0.149 (n=96) | NA (n=10) | +0.083 [-0.007, +0.173] | 0.00 | 4 |
| OPEN_all | +0.094 (n=124) | +0.171 (n=287) | +0.218 (n=32) | +0.261 (n=58) | +0.287 (n=116) | NA (n=13) | +0.189 [+0.104, +0.275] | 0.00 | 5 |
| OPEN_sizematch | +0.069 (n=120) | +0.132 (n=279) | +0.224 (n=30) | +0.044 (n=49) | +0.290 (n=100) | NA (n=13) | +0.144 [+0.058, +0.230] | 0.00 | 5 |

OPEN_home's DerSimonian-Laird pooled confidence interval includes zero (+0.083 [-0.007, +0.173]). The home only signal is marginal; the corpus wide signal is robust.

### 25.4 Mechanical coupling: ALL minus HOME

The paired difference OPEN_all minus OPEN_home at the footprint rung is +0.093 [+0.016, +0.169] (n = 571), confirming that cross field cooccurrence carries information beyond home field structure. The home only signal is driven by NOV_res (+0.134 [+0.049, +0.215]) and edge_persistence (−0.112 [−0.199, −0.023]).

### 25.5 RETENTION_RATIO_early and Holm family

| test | estimate [95% CI] | n |
|---|---|---|
| RETENTION_RATIO_early\|O2r_m50\|R0 | -0.131 [-0.209, -0.056] | 634 |
| RETENTION_RATIO_early\|O2r_m50\|R2 | -0.043 [-0.116, +0.031] | 634 |

After adding concept type controls, the retention ratio signal attenuates and its confidence interval includes zero. The Holm family (8 members: 3 builds × 2 outcomes + 2 retention tests) yields Holm p = 0.048 for OPEN_home on rarefied breadth and 0.004 for OPEN_all and OPEN_sizematch.

### 25.6 Learned models (cohort)

| outcome | five feature baseline | linear_all (baseline + OPEN + all indicators) | diff [95% CI] |
|---|---|---|---|
| rarefied breadth (O2r_m50) | 0.789 | 0.818 | +0.030 [+0.012, +0.049] |
| residualised breadth (O2r_resid) | 0.789 | 0.816 | +0.027 [+0.009, +0.046] |
| transience | - | - | diff = -0.021 (not evaluable) |

The learned model adds 3 Spearman points over the five feature baseline on the cohort. Citation growth is not evaluable (no citation pass).

### 25.7 Verdict

**CONFIRMED but marginal for the home only build.** OPEN_home passes the primary concept type test (confidence interval excludes zero, Holm p = 0.048) but the DerSimonian-Laird pooled interval includes zero. OPEN_all and OPEN_sizematch are clearly confirmed across all rungs and groups. The OPEN construct captures a real signal; the home only variant captures a subset of it. The signal attenuates but does not vanish under full controls including group fixed effects (OPEN_all +0.138 at the group fixed effects rung, confidence interval excludes zero).

[FIGURE:fig_open_ladder]


## 26. Experiment 12: Breadth decomposition and trajectory analysis [ARTIFACT:art_uw4OeagJP3rv]

### 26.1 Log additive breadth decomposition

Rarefied breadth Bn can be decomposed as log Bn = log E2 (early contact diversity) + log M (frontier advance ratio) + log ρ (retention rate). On DEV (3,188 concepts with O2r_m50):

| component | share of log(top/bottom tercile ratio) | 95% CI |
|---|---|---|
| s_explore (= s_E2 + s_M) | 0.732 | [0.703, 0.764] |
| s_contact (= s_E2) | 0.779 | [0.738, 0.818] |
| s_ret (= s_rho) | 0.268 | [0.236, 0.297] |
| diff(s_explore − s_ret) | 0.464 | [0.407, 0.528] |

**Prediction 1 (exploration share exceeds retention share): SUPPORTED.** The exploration channel (early contact diversity) accounts for 73% of the top vs bottom breadth gap; retention accounts for 27%. The difference is 0.464 [0.407, 0.528], robust across all heldout units.

**Prediction 2 (frontier advance is positive): REVERSED.** The frontier advance ratio contributes negatively (s_M = −0.046 [−0.074, −0.017]). Broad concepts do not advance a wider frontier; they start with wider contact.

**Prediction 3 (OPEN correlates more with exploration share): positive retention correlation.** OPEN correlates with the retention term, not against it, complicating the predicted sign.

### 26.2 Trajectory typology

DTW k-medoids (k = 4, chosen by ARI stability) and 5-state HMM were compared on 9-variable annual trajectory profiles (new entries, offhome entries, fields retaining, fields lost, retention share, frontier, entropy, home share, community span):

| method | ARI with DTW k=4 | naming rule passes? |
|---|---|---|
| DTW k=4 | 1.0 (self) | No (all conditions false) |
| HMM S=5 | 0.222 | No |
| DTW k=4 (no Medicine) | 0.461 | No |

**Verdict: CONTINUUM.** The naming rule (which requires each cluster to dominate on a specific trajectory feature) fails for all conditions. The DTW-HMM agreement is low (ARI 0.222), improving to 0.461 when Medicine dominated clusters are excluded. PCA of the trajectory space shows the first principal component explains 38.8% and the second 10.7% of variance; OPEN correlates with the first component (the breadth axis). The two class finding from iteration 2 does not reproduce at higher resolution.

Heldout recluster: ARI = 0.443 (DTW) and 0.378 (HMM), confirming moderate but not strong reproducibility.

### 26.3 Sequence ordering

No ordering signal is found beyond mechanical lag. The lead lag regression of entry on prior retention (and vice versa) produces near zero coefficients once concept fixed effects are included. The iteration-2 ordering finding (Section 11.3) was already downgraded to MIXED and is now consistent with a simultaneous process rather than a gateway first sequence.

### 26.4 Case studies (7 matched pairs)

Seven pairs matched on the five feature baseline but differing in OPEN were examined:

| high OPEN concept | low OPEN concept | OPEN diff | O2r diff |
|---|---|---|---|
| GPU computing | Vertical axis wind turbine | high | high |
| Shotgun proteomics | Image-guided radiation therapy | high | high |
| Systems biology | Tissue engineering | moderate | moderate |
| Bayesian optimization | Reservoir computing | high | moderate |
| Social network analysis | Brain-computer interface | moderate | moderate |
| Deep learning | Metamaterial | high | high |
| Synthetic biology | Spintronics | moderate | moderate |

The high OPEN concepts consistently reached more fields. GPU computing and deep learning are canonical cases: dense new cooccurrence edges across many communities, high participation, low initial density, and rapid turnover of cooccurrence partners.


## 27. Evaluation 3: Boundary study and corrections [ARTIFACT:art_oKOd21ZMnu9S]

### 27.1 Postonset rescore

About half of the M0_density_end and D_vol_end breadth signal comes from the concept's preonset footprint in other fields:

| indicator | full history | postonset only | paired difference | attenuation | verdict |
|---|---|---|---|---|---|
| M0_density_end | +0.374 | +0.187 [+0.145, +0.246] | +0.187 [+0.138, +0.231] | 0.50 | PARTIAL |
| D_vol_end | +0.317 | +0.176 [+0.114, +0.227] | +0.141 [+0.087, +0.209] | 0.45 | PARTIAL |

The postonset part is still clearly positive, so these indicators are partly but not only early network signals. D_vol_post is near rank identical to the five feature baseline reach column (within unit Spearman 0.97-1.00).

### 27.2 OPEN specification curve

Across 1,920 specifications (120 composites × 4 outcomes × 4 control sets), the pooled PSP CI excludes zero in 99.7% of specs (DL over 4 heldout groups; 100% with cohort units). Median PSP = 0.152 (IQR 0.134-0.169). Under a Freedman-Lane null (200 draws), the null share with CI > 0 averages 1.6%; permutation p = 0.005.

Headline specification (all 6 components, equal weights, rarefied breadth, baseline plus onset controls): +0.183 [+0.083, +0.280], Higgins I² = 0.73, prediction interval [-0.238, +0.547]. The positive OPEN association is a property of the construct, not of one combination.

### 27.3 Heterogeneity and the Life & Environment Sciences diagnosis

On 21 home field × period subunits (n >= 60), Higgins I² drops to 0.43 (vs 0.66 over the 6 units). No ecological trait (label coverage, early volume, share multihome, share generic, median O2r, SD of OPEN, mean onset year) explains the between subunit variance (all Holm p = 1.0).

LIFEENV shows the weakest OPEN signal: PSP +0.071 vs +0.186 for the other 5 units pooled. Neither restricted range (Thorndike correction moves it only to +0.080) nor label coverage reweighting (entropy balancing: +0.069) explains the gap. Verdict: **UNEXPLAINED domain boundary**.

### 27.4 Retained frontier proximity dependence

[Correction, iteration 4, from art_22ppE1snfHKj] Under the minimum conditional probability proximity backbone (instead of the frozen PMI backbone), d0_ret_rel at the footprint control rung is -0.021 (vs +0.322 under PMI). The d0 effect is backbone specific: it measures relatedness as PMI encodes it, not relatedness in general.

### 27.5 Claims ledger

The iteration-4 claims ledger (v3) has 1,290 rows and 0 MISMATCH after all corrections from files 01-11 are applied.

### 27.6 Corrections applied

Evaluation 3 produced 12 correction files (00-11) covering sections throughout the report. All corrections have been applied in place with `[Correction, iteration N, from art_...]` tags. The major corrections are:

- Section 19.1: indicator families corrected from 7 to 6 (D family exclusion, external recognition is an outcome, the five feature baseline is a baseline)
- Sections 19.4-19.7: citation growth/transience relabelling, missing transience results, full 8 outcome learned models table
- Section 19.8: preregistered predictions quoted from exact frozen text
- Section 10.3: gateway retention LPM criterion passes (verdict still DISCONFIRMED, 5/6 fail)
- Section 11.3: ordering downgraded to MIXED (lead lag regressions negative)
- Section 10.6: gateway breadth effect small, pooled confidence interval includes 0
- Dead ends 22.6-22.7: citation growth/transience distinction, prediction failure reasons
- Dead end 22b: Experiment 9 failure added


## 28. Research 3: Novelty positioning [ARTIFACT:art_hSyVUBa2okT2]

### 28.1 Novelty verdicts

| claim | verdict | key comparator |
|---|---|---|
| openness → later cross field breadth | PARTIALLY ANTICIPATED | Cheng 2023 (volume, not breadth), Maillart 2026 (concept pairs, not field holdout), Wang 2017 (paper level novelty), Weng 2013 (memes), Ugander 2012 (adoption) |
| consolidation → less breadth | PARTIALLY ANTICIPATED, CONTRADICTED BY on volume | Cheng 2023 (consistency +53% volume/SD), Chavalarias 2013 (density → survival), Centola 2010, Salatino 2017 |
| low retention ratio → breadth | NEW | Analogues only: propagule pressure (Lockwood 2005), group turnover (Palla 2007) |
| within concept closure → entry slowdown | NEW as lead lag test | Field level prior is opposite (Chavalarias 2013); life cycle analogues (Singh 2022, Prabhakaran 2016) |

### 28.2 Contribution statement

"The first heldout, size adjusted, concept level test showing that early cooccurrence openness predicts later cross field breadth, while early consolidation, which predicts volume and survival elsewhere, does not."

### 28.3 Design gaps identified

1. ego_density_W3 is not degree normalised (Ravasz & Barabási C(k) ~ 1/k); add a configuration null z score.
2. Run Cheng's exact consistency/embeddedness measures on volume vs breadth; the predicted result is a sign flip.
3. Report survival alongside breadth and test the size × turnover interaction (Palla 2007).
4. Heterogeneity robust staggered event study estimators for the within concept closure claim (Sun & Abraham 2021; Callaway & Sant'Anna 2021).

### 28.4 Applied Network Science fit

The paper fits 8 ANS publications on cross field knowledge flows, topic dynamics and field of study networks (De Domenico 2016, Gao 2018, Salnikov 2018, Larson 2017, Cunningham 2022, Holmgren 2023, Fontaine 2024, Du 2025). The ANS collection "Networks for everyday life" (deadline 30 November 2026) includes scope items on information diffusion and knowledge exchange networks.


## 29. Dead ends and negative results from iteration 4

1. **OPEN_home DerSimonian-Laird pooled confidence interval includes zero.** The home only OPEN build has pooled PSP +0.083 [-0.007, +0.173] on the confirmatory cohort. The primary concept type per concept interval excludes zero (Holm p = 0.048), but the pooled cross group estimate does not. The home field signal is marginal.

2. **Frontier advance ratio is negative (Prediction 2 REVERSED).** Broad concepts do not advance a wider frontier; they start with wider contact. The frontier advance component of the breadth decomposition is -0.046, not positive as predicted.

3. **Trajectory naming rule fails (CONTINUUM).** No cluster dominates a trajectory feature. The DTW k=4 vs HMM S=5 adjusted Rand index is only 0.222. The two class finding from iteration 2 (we called those classes "broadly spreading" and "narrowly spreading") does not reproduce at higher resolution.

4. **No ordering signal beyond mechanical lag.** The sequence tests confirm that there is no gateway first ordering once concept fixed effects are included.

5. **D_vol_post is nearly collinear with the five feature baseline reach.** Once preonset years are removed, D_vol is almost the baseline itself (within unit Spearman 0.97-1.00).

6. **RETENTION_RATIO_early attenuates at the concept type rung.** After adding concept type controls, the retention ratio confidence interval includes zero (-0.043 [-0.116, +0.031]).

7. **LIFEENV domain boundary unexplained.** The weak OPEN signal in Life & Environment Sciences (PSP +0.071) is not accounted for by restricted range or label coverage.

8. **Candidate S (coauthor reach) is weak beyond the five feature baseline.** S_comp_n pooled PSP for rarefied breadth = -0.029 [-0.239, +0.184], Higgins I² = 0.94. The Cheng et al. social reach rival is not confirmed.

9. **d0_ret_rel is backbone specific.** Under minimum conditional probability proximity, d0 = -0.021. The retained frontier effect requires PMI backbone encoding.


## 30. Coverage of the original request (final)

| Step | Iteration 1 | Iteration 2 | Iteration 3 | Iteration 4 |
|---|---|---|---|---|
| RQ1: candidate indicator screen (dev) | Done (3) | Not extended | Done (53 indicators) | - |
| RQ1: holdout evaluation | Not started | Frame built (12,499) | Done (7/10 confirmed) | OPEN cohort confirmed |
| RQ1: top-10 on holdout | Not started | Not started | Done | Extended (OPEN composite) |
| RQ1: external ground truth (O5) | Not started | Built | Validated: unrelated | - |
| RQ1: learned model | Not started | Not started | Done (+0.059) | Cohort +0.030 |
| RQ2: diffusion trajectories | Not started | Done (2 classes) | Exp9 failed | Done: CONTINUUM (Exp12) |
| RQ2: field entry conditional logit | Partial (dev) | Confirmed (d=0.30) | Robustness: PARTIAL | Backbone-specific |
| RQ2: breadth decomposition | Not started | Not started | Not started | Done: explore 73%, retain 27% |
| Grounding benchmark | Not started | Done | Audited | - |
| Strongest indicator analysis | Not started | Not started | Not started | Decomposition + case studies |
| Case studies | Not started | Not started | Not started | Done (7 matched pairs) |
| Record audit | Not started | Not started | Done (246 claims) | Done (1,290 claims, 0 mismatch) |
| Spec curve / robustness | Not started | Not started | Not started | Done (1,920 specs, 99.7% CI>0) |
| Novelty positioning | Not started | Partial | Partial | Done (4 claims, 68 refs) |


## 31. What we have learned so far

Four iterations and sixteen artifacts (fifteen commissioned, twelve completed; three failed: gen_art_dataset_1, gen_art_experiment_2, gen_art_experiment_9) have tested whether temporal network signals predict how new scientific concepts spread across disciplines, using OpenAlex data on up to 12,499 concepts with up to 27,393 concept by field adoption episodes.

**Confirmed findings:**

1. **Early cooccurrence openness (OPEN) predicts later cross field breadth on a confirmatory cohort.** The OPEN index (mean of six z scored ego network components: new_edge_rate, n_comm_W3, participation, NOV_res, −ego_density_W3, −edge_persistence) is confirmed on 2015-2016 onset concepts never used in any prior screen. OPEN_home PSP = +0.091 [+0.013, +0.171] at the concept type rung (Holm p = 0.048); OPEN_all +0.174 [+0.092, +0.253]; OPEN_sizematch +0.147 [+0.068, +0.221]. The specification curve shows 99.7% of 1,920 specs have confidence intervals above zero (permutation p = 0.005). The OPEN signal survives controls for contact reach, concept type, preonset footprint, label coverage and group fixed effects.

2. **Seven of 10 early network indicators are confirmed for predicting rarefied field breadth on heldout fields.** M0_density_end (+0.375), D_vol_end (+0.307), CONTACT_REACH (+0.211), n_comm_W3 (+0.167), NOV (+0.151), RETENTION_RATIO_early (−0.114), ego_density_W3 (−0.102). An ElasticNet combining all indicators adds +0.059 [+0.046, +0.073] Spearman over the five feature baseline.

3. **Breadth is driven by exploration, not retention.** The log additive decomposition shows that early contact diversity accounts for 73% of the top vs bottom tercile breadth gap; retention accounts for 27% (difference 0.464 [0.407, 0.528]). Broad concepts start with wider contact, not by advancing a wider frontier.

4. **Retaining relatedness predicts the next field entered (the entry hypothesis, confirmed).** Holdout LR 71.7, d = 0.30 [0.24, 0.37], DerSimonian-Laird pooled d = 0.28 [0.22, 0.35], replicated on the Experiment 7 independent frame (d0 = 0.322 [0.291, 0.355]). The retained frontier hypothesis is PARTIAL: d0 survives RCA and volume density rivals in the conditional logit, but the volume matched contrast is null on heldout data (Holm p = 0.76), and d0 is backbone specific (under minimum conditional probability proximity, d0 = −0.021).

5. **Background homophily dominates raw lineage (methodological finding).** Two thirds of between concept variance in raw lineage log odds is general disciplinary homophily.

6. **Edge persistence is negatively associated with breadth (preregistered prediction 2: HOLDS).** Pooled PSP = −0.080 [−0.126, −0.033]. Consistent with the broader finding that early consolidation does not predict breadth.

**Disconfirmed or downgraded:**

1. **Gateway centrality does not predict field retention.** Disconfirmed on 27,393 episodes (iteration 2).

2. **No single concept level network indicator beats the simple baseline for raw breadth** (iteration 1). The composite OPEN and the learned model (iterations 3-4) do add beyond the five feature baseline.

3. **Volume-matched persistence is null on heldout data.** The retained frontier is PARTIAL.

4. **Abandonment penalty is inconclusive.** d_lost null on the independent frame.

5. **External recognition is unrelated to publication outcomes.** Measures prior recognition, not diffusion success.

6. **Rescue and relay mechanisms are not supported.**

7. **Ordering is MIXED.** Lead-lag regressions show retention followed by smaller entropy gains. No gateway first sequence is established.

8. **Trajectory classes are a CONTINUUM.** The naming rule fails; the agreement between DTW k-medoids and HMM clustering is low. The two class finding from iteration 2 does not reproduce at higher resolution.

9. **Candidate S (coauthor reach) is weak beyond the five feature baseline.** S_comp_n pooled PSP −0.029 [−0.239, +0.184].

10. **Frontier advance ratio is negative (Prediction 2 REVERSED).** Broad concepts start with wider contact, not by advancing further.

**Open:**

- ego_density_W3 is not degree normalised; the C(k) ~ 1/k dependence (Ravasz & Barabási 2003) may inflate or deflate the effect.
- Direct test of Cheng et al.'s consistency measure on volume vs breadth (predicted sign flip) is not run.
- Survival alongside breadth (Chavalarias & Cointet 2013; Palla et al. 2007 size × turnover interaction) is not reported.
- Heterogeneity robust staggered event study estimators for the within concept closure claim are not applied.
- The LIFEENV domain boundary remains unexplained.


## References

[1] Salatino, A., Osborne, F., & Motta, E. (2017). How are topics born? PeerJ Computer Science, 3, e119.
[2] Weng, L., Menczer, F., & Ahn, Y.-Y. (2013). Virality Prediction and Community Structure in Social Networks. Scientific Reports, 3, 2522.
[3] Rotolo, D., Hicks, D., & Martin, B. R. (2015). What is an emerging technology? Research Policy, 44(10), 1827-1843.
[4] Cheng, M., Smith, D. S., Ren, X., Cao, H., Smith, S., & McFarland, D. A. (2023). How New Ideas Diffuse in Science. American Sociological Review, 88(3), 522-561.
[5] Ciotti, V., Bonaventura, M., Nicosia, V., Panzarasa, P., & Latora, V. (2016). Homophily and missing links in citation networks. EPJ Data Science, 5, 7.
[6] Lipsitch, M., Tchetgen Tchetgen, E., & Cohen, T. (2010). Negative Controls. Epidemiology, 21(3), 383-388.
[7] Maillart, T. et al. (2026). Forecasting Conceptual Diffusion in Science. arXiv:2606.03919.
[8] Chavalarias, D. & Cointet, J.-P. (2013). Phylomemetic Patterns in Science Evolution. PLoS ONE, 8, e54847.
[9] Chen, C. (2012). Predictive effects of structural variation on citation counts. JASIST, 63, 431-449.
[10] Rafols, I. & Meyer, M. (2009). Diversity and network coherence. Scientometrics, 82, 263-287.
[11] Salatino, A., Osborne, F., & Motta, E. (2018). AUGUR. Proceedings of JCDL, 303-312.
[12] De Domenico, M., Omodei, E., & Arenas, A. (2016). Quantifying the diaspora of knowledge. Applied Network Science, 1, 15.
[13] Hidalgo, C. A. et al. (2007). The Product Space. Science, 317, 482-487.
[14] Guevara, M. R. et al. (2016). The research space. Scientometrics, 109, 1695-1709.
[15] Hidalgo, C. A. et al. (2018). The Principle of Relatedness. Unifying Themes in Complex Systems IX, 451-457.
[16] Neffke, F., Henning, M., & Boschma, R. (2011). How do regions diversify? Economic Geography, 87(3), 237-265.
[17] Rigby, D. L. (2015). Technological relatedness and knowledge space. Regional Studies, 49(11), 1922-1937.
[18] Blackburn, T. M. et al. (2011). A proposed unified framework for biological invasions. TREE, 26(7), 333-339.
[19] Pinheiro, F. L. et al. (2022). The time and frequency of unrelated diversification. Research Policy, 51(8), 104323.
[20] Albora, G. et al. (2023). Product progression. Scientific Reports, 13, 1481.
[21] Bahar, D., Hausmann, R., & Hidalgo, C. A. (2014). Neighbors and the evolution of comparative advantage. J. International Economics, 92(1), 111-123.
[22] Wang, J., Veugelers, R., & Stephan, P. (2017). Bias against novelty in science. Research Policy, 46, 1416-1436.
[23] Uzzi, B. et al. (2013). Atypical Combinations and Scientific Impact. Science, 342, 468-472.
[24] Foster, J. G., Rzhetsky, A., & Evans, J. A. (2015). Tradition and Innovation. ASR, 80, 875-908.
[25] Shi, F. & Evans, J. (2023). Surprising combinations. Nature Communications, 14, 1641.
[26] Ugander, J. et al. (2012). Structural diversity in social contagion. PNAS, 109, 5962-5966.
[27] Centola, D. (2010). The Spread of Behavior. Science, 329, 1194-1197.
[28] Palla, G., Barabási, A.-L., & Vicsek, T. (2007). Quantifying social group evolution. Nature, 446, 664-667.
[29] Burt, R. S. (2004). Structural Holes and Good Ideas. AJS, 110, 349-399.
[30] Lockwood, J. L., Cassey, P., & Blackburn, T. (2005). Propagule pressure. TREE, 20, 223-228.
[31] Singh, C. K. et al. (2022). Quantifying the rise and fall of scientific fields. PLoS ONE, 17, e0270131.
[32] Prabhakaran, V. et al. (2016). Predicting the Rise and Fall of Scientific Topics. ACL, 1170-1180.
[33] Ravasz, E. & Barabási, A.-L. (2003). Hierarchical organization in complex networks. PRE, 67, 026112.
[34] Gotelli, N. J. & Colwell, R. K. (2001). Quantifying biodiversity. Ecology Letters, 4, 379-391.
[35] DerSimonian, R. & Laird, N. (1986). Meta-analysis in clinical trials. Control. Clin. Trials, 7, 177-188.
[36] Higgins, J. P. T. & Thompson, S. G. (2002). Quantifying heterogeneity. Stat. Med., 21, 1539-1558.
[37] Cunningham, E., Smyth, B., & Greene, D. (2022). Author multidisciplinarity. Applied Network Science, 7, 78.
[38] Holmgren, A., Edler, D., & Rosvall, M. (2023). Mapping change in higher order networks. Applied Network Science, 8, 42.
[39] Fontaine, S. et al. (2024). Epistemic integration and social segregation of AI in neuroscience. Applied Network Science, 9, 8.
[40] Du, A., Head, M., & Brede, M. (2025). Journal publications in medicine. Applied Network Science, 11, 11.
[41] Gao, Y. et al. (2018). Community evolution in patent networks. Applied Network Science, 3, 26.
[42] Salnikov, V. et al. (2018). Cooccurrence simplicial complexes. Applied Network Science, 3, 37.
[43] Larson, J. M. (2017). The weakness of weak ties. Applied Network Science, 2, 14.
[44] Cao, H. et al. (2020). Will This Idea Spread Beyond Academia? Findings of EMNLP, 1746-1757.
[45] Tria, F. et al. (2014). The dynamics of correlated novelties. Scientific Reports, 4, 5890.
[46] Hofstra, B. et al. (2020). The Diversity-Innovation Paradox. PNAS, 117, 9284-9291.
[47] March, J. G. (1991). Exploration and Exploitation. Organization Science, 2, 71-87.
[48] Krenn, M. & Zeilinger, A. (2020). Predicting research trends. PNAS, 117, 1910.
[49] Richardson, D. M. et al. (2000). Naturalization and invasion. Diversity and Distributions, 6, 93-107.
[50] Li, Y. & Neffke, F. (2022). Evaluating the principle of relatedness. arXiv:2205.02942.
[51] Callon, M., Courtial, J. P., & Laville, F. (1991). Co-word analysis. Scientometrics, 22, 155-205.

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

--- Item 9 ---
id: art_22ppE1snfHKj
type: experiment
title: Do concepts spread from fields that keep them?
summary: |-
  Decisive zero-credit test of the retained-frontier claim (EXP6 lead: a concept next enters fields related to the off-home fields that currently RETAIN it, d0_ret_rel) against the field-standard relatedness-density rival built as the literature builds it (omega = sum U phi / sum phi with U = RCA>1: annual Hidalgo current portfolio [primary], 3-year, Guevara-2016 cumulative and persistence-filtered), plus share-weighted density (D_vol, D_vol_w3, D_cum), and of the abandonment penalty (d_lost: relatedness to dropped off-home presences). Conditional logit (Breslow) on concept x target-field x year entry risk sets, concept-year strata, frozen 1998-2002 26-field PMI backbone; nested ladder R0 (home relatedness, log size, entered density, own gateway) -> R1 +D_rca_1y -> R2 +D_vol -> R3 +d0 -> R4 +d_lost; S_strict = all 4 RCA + both D_vol; S_pca; A1 = R0 + d_lost.

  STEP 1 (EXP6 frame, robustness): risk sets rebuilt row-for-row (max diff 4e-16) and EXP6 held-out M1 vs M0 LR 68.57 / d0 0.2809 reproduced; d0 survives RCA>1 and volume: R3 0.262 [0.196,0.320], S_strict 0.252 [0.188,0.315], permutation p=0.001.

  STEP 2 (independent frame: EXP5 12,499 concepts minus every EXP6 concept by OpenAlex ID/QID/normalised label -> 11,841; DEV 4,486 used for code, standardisation, power and rules; hash-frozen, git 24da538; held-out scored ONCE). Held-out pooled PHYS+LIFEENV+SOC+MATHDEC (3,162 concepts, 6,978 entries): LR(R3 vs R2)=325.8, d0=0.322 [0.291,0.355] (concept refit bootstrap 1,000), S_strict 0.304 [0.268,0.336], crossed concept x field CI [0.201,0.468]; positive in PHYS 0.15, LIFEENV 0.40, SOC 0.30 (MATHDEC 0.07, underpowered, excluded pre-freeze), cohort 2010-14 0.321 [0.292,0.347]; DL 4 groups 0.243 [0.118,0.368], I2=0.92. Retained-label permutation p=0.001, rewire p=0.004, node-label p=0.003; dose by persistence age 2/3/>=4 = 0.10/0.08/0.30 (4+ minus 2: 0.21 [0.16,0.26]); stable under target-field FE (0.30), RCA-defined entry event (0.24), primary-topic fields, min_n 3/5, horizon 8, exclusions. BUT the pre-declared volume-matched contrast (retained vs entered-not-retained fields in the same current x cumulative volume cell) is null: -0.028 [-0.105,0.046] (fine bins -0.026), so frozen verdict FRONTIER = PARTIAL ('persistence confounded with volume'). Also: under a Hidalgo min-conditional-probability proximity d0 vanishes (-0.021, p=0.012) - backbone-specific; the econ-geo LPM row gives d0 slightly negative, and an EXPLORATORY diagnostic shows it is ~0 once size enters non-linearly (relative-odds, not additive-probability, effect). ABANDONMENT: d_lost in A1 = -0.007 [-0.036,0.022] (power 0.99 at -0.06) -> INCONCLUSIVE/no penalty; with d0 it turns positive (+0.064). Within-stratum AUC R2 0.847 -> R3 0.852; Guevara-comparable global AUC of D_rca_cum 0.635 (flagged, different unit/event).

  Checks: 10 unit tests pass; planted d0=0.2 detected 100%, null rejection 0/200; shuffled entries 0/20; independent audit (hand Breslow exact reproduction; statsmodels EXACT likelihood LR ratio 0.99-1.02; 20 rows re-derived from raw counts; inline DL) all pass. Outputs: results/frontier_result.json (all numbers), step1/step2 JSONs, frozen_spec + seal/unseal logs, risk-set and state-panel parquets, null draws, 6 figures (forest d0 / d_lost by unit, ladder, dose, null histograms, volume-matched), method_out.json = full_method_out.json (252,922 held-out candidate rows with predict_R2_rca_vol_baseline vs predict_R3_retained_frontier from frozen DEV coefficients). No LLM or OpenAlex spend.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md

--- Item 10 ---
id: art_dFQ6jbgNsR6Q
type: experiment
title: Which early network signals of new topics travel
summary: >-
  RQ1 held-out deliverable on the EXP5 frame (12,499 TAG-grounded OpenAlex concepts; DEV CS/Eng/BGM/Med 4,771; held-out PHYS
  742, LIFEENV 1,113, SOC 1,352, MATHDEC 165; 2010-14 cohort 2,484 DEV-home + 1,872 other). Two zero-credit OpenAlex S3 passes
  (Pass A reproduces EXP5 grounded counts exactly for all concepts; Pass B windowed citations). 53 indicators in 7 families
  over t0..t0+2 (popularity E, disciplinary F, landing G, retained-frontier FR, 27 co-occurrence ego-network A ported from
  EXP3 and validated to 1e-15, co-author S) plus B5 baseline. Outcomes: O1c/O1b uptake, O2r_m50/O2r_resid breadth, O3 transience,
  O4 field/year-normalised citation growth, O5/O5_WW external recognition (art_O7Dq4L02QnDN). DEV-only ranking (psp|B5, LOGO
  dAUC, refit bootstraps), frozen top-10s + ElasticNet/L1-logit + EBM, hash seal, single unseal, DL pooling, Holm. RESULTS:
  breadth is predictable beyond B5 and portable: 7/10 (O2r_m50) and 8/10 (O2r_resid) frozen indicators confirmed with 6/6
  unit sign agreement; M0_density_end psp +0.377 [0.280,0.466], D_vol_end +0.307, CONTACT_REACH +0.210, n_comm_W3 +0.164,
  NOV +0.152, ego_density_W3 -0.097, RETENTION_RATIO_early -0.120 (caveat: M0_density_end/D_vol_end use cumulative 1995..t0+2
  field history, i.e. partly a pre-onset footprint). O1c: only n_authors_early (+0.161). O4: REL_home -0.114, author_growth
  +0.065; EBM Spearman 0.188 vs B5 0.015. O5/O5_WW: no indicator or model beats B5+onset year. Learned: breadth ElasticNet
  0.765 vs B5 0.706 (+0.059 [0.046,0.073]). Pre-registered: P2 holds; P1,P3,P4,P5 fail. Robust to EXP6-overlap exclusion,
  coverage covariates, O2r_m30, EXP5 O2r_resid definition. Audits: T0-T8 pass; independent audit.py and rederive.py reproduce
  headline numbers, shuffled controls null. Key files: results/rq1_heldout.json, heldout_summary.json, portability_table.csv,
  learned_vs_single_heldout.json, prereg_verdicts.json, frozen_spec.json, deviations.json; figures/*; method_out.json (per-concept
  indicators, outcomes, predictions). Deviations: 1-yr ego windows (D family >30% missing so never frozen), betweenness cutoff
  3, O2r_resid per plan formula (EXP5 formula as sensitivity), linear onset-year term in O5 baselines. Second use of held-out
  outcomes (EXP5) disclosed; G family flagged previously scored.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md

--- Item 11 ---
id: art_7W9xiIO3FVBs
type: evaluation
title: Auditing the record before the paper
summary: >-
  Zero-new-data audit of the iteration-2 record (eval_out.json, exp_eval_sol_out, validated). WP1 claims_ledger.csv: 246 rows
  read by key path (224 MATCH, 15 MISLABELLED, 6 MISMATCH, 1 FILE_FLAG_OVERRIDDEN; 58 blocking). H1: lpm_beta_within_gt0_p05
  = true (beta +0.068/SD, concept-clustered p 0.041, two-way p 0.17; sealed code uses p_concept), verdict still DISCONFIRMED.
  Ordering -> MIXED: 57/87 non-tied = 65.5%, but 57/102 evaluable and 57/175 = 32.6% of broad concepts; lead-lag negative,
  pre-trend ev-3 -0.072 (p 0.0002), DEV reverse b 0.232 (p 0.006). H3: pooled CI [-0.006, 0.065] includes 0; DEV 0.138 ->
  shrinkage 0.21; 0/40 is a false-positive rate. Dataset-2 counts 3,583/17,872/8,462/1,015 are ENTRIES (concepts 1,298/1,121/2,635/213).
  The 'B5+all_four' row is size_controlled_all_three (+0.085, refit CI [-0.043, 0.220]). MDE 0.004 is the 90% point for 8,515
  episodes. WP2: record_tables/ has the 34-indicator portability table, exp1 lineage robustness, 12 partial associations,
  H1 criteria, ordering, coverage_iter2 and refit bootstrap CIs (B=2000; all 7 iteration-1 deltas reproduce exactly; none
  of the CIs excludes 0; 1.2-2.2x wider than fixed CIs). T4 next_field_trace.json reproduces all 26 Exp6 headline numbers:
  LR 68.6 = M1 vs M0 Breslow, 71.7 = M2 vs M0 Breslow, 77.3 = M2 exact (M1 exact 73.2); 961 = informative strata, 2,339 =
  all primary strata; d 0.281 = M1, 0.302 = M2. The per-row parquet is in record_tables/. WP3 frame_agreement.json (628 shared
  concepts): onset exact 0.976, home kappa 0.99, O2r_m50 rho 0.998, episode Jaccard median 1.0, but retention kappa 0.28 (0.98
  with the matched absolute R_abs2 rule) -> pooling PARTIAL. An Exp5-minus-Exp6 H2 confirmation must rebuild RETAINED/LOST
  with R_cj. Concepts left: PHYS 708, LIFEENV 1,081, SOC 1,301, MATHDEC 165, COHORT 4,117. WP4 o5_validation.json: O5_main
  held-out base rate 0.238, UNRELATED to publication outcomes (pooled rho O2r_m50 0.014 [-0.045, 0.073], O1 0.001). 67% of
  concepts are recognised at or before t0. Executor-checked 100-item hand check: precision 0.86, dates within 1 year 95%,
  false-negative rate >= 0.14, FIT_FOR_USE true, but only 42% of positives mark a genuinely new concept. LLM spend $0.009.
  text_corrections.md gives the old and new sentences with source keys. verify_headlines.py re-derives the headline numbers
  independently, with placebos.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
- reproducibility.md

--- Item 12 ---
id: art_EesdB8cuSfcU
type: research
title: Is 'fields that keep it' new? Prior art and venue checksummary: |-
  Prior-art, comparison and venue positioning for the iteration-3 ANS paper. It builds on art_dxvRpQufMR0e.

  (1) CLAIM A (next-field entry follows relatedness to fields that RETAIN a concept): PARTIALLY ANTICIPATED.
  - Persistence is used only as a filter on the entry OUTCOME: Pinheiro et al. 2022 (Δ=4 backward/forward RCA rule), Albora et al. 2023 (RCA<0.25 in all prior years), Bahar et al. 2014 (jumps).
  - All densities found are current-snapshot (RCA>1 or continuous).
  - No retained-only or duration-weighted density predictor was found in 6 strands.
  - Cheng et al. 2023 ("consistent intellectual usage" → core concept) is the closest science analogue; it is global, not per field.

  (2) CLAIM B (relatedness to fields that DROPPED it lowers entry): mechanism partly anticipated; NEW as a test.
  - Mechanism precedents: Fernandes & Tang 2014 (negative neighbour signals deter entry; empirically, neighbours' export growth); Nomaler & Verspagen 2022 (absence/loss informative, adds little).
  - No study uses neighbours' exits as entry predictors.
  - Our Exp6 estimate is fragile: d_lost −0.063, p 0.055.

  (3) RIVALS FOR THE EXPERIMENT
  - MISSING: persistence-filtered RCA density D_rca_persist_k; own pre-entry RCA level/trend (Albora benchmark); neighbour-momentum density.
  - PARTLY COVERED: a β_ret = β_lost test within D_ever.

  (4) RQ1 TABLE R1
  - No comparator uses held-out fields.
  - Link-forecast AUCs (Krenn 0.85 with ~5% positives; 0.95-0.97) are level metrics and not comparable to our increments over B5.

  (5) RQ2 TABLE R2
  - Prior work has field-pair modes (Sun & Latora, 4) and source/sink indices.
  - No contact × retention decomposition and no per-field entered/retained/lost tracking was found: NEW.
  - Entity-entry AUROC comparators: 0.879/0.856/0.631 (Galuppo Azevedo 2021).

  (6) VENUE
  - The collection page is IdP-blocked by every route.
  - Snippets give: submissions open 24 Jun 2026, deadline 30 Nov 2026, scope items on information diffusion and innovation/collaboration/knowledge-exchange networks.
  - Editors and member articles are unrecovered.

  (7) ANS SKELETON AND FIG. 1
  - Skeleton from 3 sci-sci ANS articles (Cunningham 2022 published; Fontaine 2024 and Holmgren 2023 on arXiv), plus a 5-lane Fig. 1 spec with this run's counts and a caption draft.

  (8) REFERENCES AND FILES
  - 50 new references verified (references_new.json); 4 UNVERIFIED items flagged.
  - Files: research_report.md (sections A-H) and reproducibility.md.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_research_2
out_expected_files:
- research_out.json
- reproducibility.md

--- Item 13 ---
id: art_NMe386dX9GLF
type: experiment
title: Do open-neighbourhood concepts spread? Fresh-cohort test
summary: >-
  Single-unseal confirmation of the RQ1 openness claim from EXP8, on a fresh 2015-2017 onset cohort of OpenAlex legacy concepts
  that no earlier screen had touched. One zero-credit S3 pass covered the snapshot of 2026-09-23 (identical to EXP5; checks
  T1-T3 exact). The outcome-blind S3 audit kept TAG grounding: legacy tags still cover 2021-24, with the control ratio at
  a minimum of 0.902. The LLM precision gate passed 94% of candidates, leaving 1,070 concepts with 2015-16 onsets. Pre-seal
  power was 0.16, so the declared 2017 extension applied (n = 1,443; 634 with O2r_m50; 573 with OPEN_home). OPEN is the mean
  of six signed, z-scored ego-network components, with constants frozen on the 12,499 EXP5 concepts; it was built ALL / HOME-ONLY
  / SIZE-MATCHED. The ladder runs R0 = B5 + onset year, then adds contact reach, LLM concept type, pre-onset footprint, coverage
  and group FE. The spec was hash-sealed before the unseal. RESULT: the frozen verdict is CONFIRMED but marginal. OPEN_home
  partial Spearman with O2r_m50 is +0.091 [+0.013, +0.171] at R2 and +0.080 [+0.001, +0.162] at R3. The CIs include 0 at R4/R5,
  the DL pool over groups is +0.083 [-0.007, +0.173], and Holm p = 0.048. It adds no practical prediction (B5 Spearman 0.768
  vs 0.770). Mechanical coupling is large: OPEN_all +0.174, ALL minus HOME +0.093 [+0.016, +0.169], with size-matched in between.
  Home-only signal comes from NOV_res (+0.134) and low edge persistence (-0.112), not from the community count. Type and footprint
  do not absorb OPEN. Replications: CONTACT_REACH (+0.211), n_authors_early on O1c (+0.115), RETENTION_RATIO_early < 0 at
  R0 only; the EXP8 ElasticNet beats B5 by +0.030. The type gate failed twice, so the declared M1 = M2 fallback was used.
  O4 was not run. Independent re-derivations (audit.py, rederive.py) reproduce psp exactly; the shuffled and random-OPEN placebos
  are null. LLM spend $2.04. Deliverables: results/cohort_report.json, cohort_result.json, exp5_selection_result.json, figures/,
  full_method_out.json (predict_B5 vs predict_B5_plus_OPEN_home per concept).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md

--- Item 14 ---
id: art_uw4OeagJP3rv
type: experiment
title: 'How concepts spread: early reach vs keeping fields'
summary: >-
  Cache-only re-run of the RQ2 trajectories analysis on all 12,499 EXP5 frame concepts (DEV 4,771 CS/Eng/BGM/Med; held-out
  PHYS/LIFEENV/SOC/MATHDEC 3,372; 2010-14 cohort 4,356). Held-out outcomes were previously unsealed by EXP5/EXP7/EXP8, so
  held-out results are within-frame robustness checks; this artifact's choices were hash-sealed on DEV (results/frozen_spec.json)
  before it read held-out data. (1) Exact decomposition of the top-vs-bottom O2r_resid tercile gap in retained off-home breadth
  at t0+8: log Bn = log E2 (early contact, fields entered by t0+2) + log M (frontier advance) + log rho (retention), volume-stratified.
  PR1 SUPPORTED everywhere: s_explore - s_ret (Medicine excluded) DEV 0.633 [0.537,0.727], held-out pooled 0.492 [0.403,0.575],
  cohort 0.445 [0.358,0.527], DL 0.504 [0.329,0.679] (I2 0.76). Shares DEV 0.79/0.03/0.18 (E2/M/rho). Frontier advance M ~0;
  D_rho positive (integrating concepts keep a larger share). Robust to min_n 3/5, O2r_m50, O1b-only, onset-restricted counts,
  Das Gupta and concept-level covariance decompositions. (2) PR2 (localised keep more early) FAILS raw (DEV reversed -0.110,
  held-out null +0.011, cohort reversed); only the partial clause holds (partial Spearman of early retention ratio with O2r_resid
  given B5: -0.169/-0.129/-0.173; replicates EXP8). (3) No trajectory typology passes the naming rule (DTW k=4 vs HMM S=5
  ARI 0.222; Hennig Jaccard 0.69-0.82; no-Med ARI 0.46; held-out re-cluster ARI 0.44/0.38) -> CONTINUUM: PC1 38.8% breadth-of-spread
  axis, PC2 10.7% keep-vs-lose axis. (4) Early ego-network openness (OPEN; 3 builds ALL/HOME-ONLY/SIZE-MATCHED) correlates
  with PC1 beyond B5+label coverage: DEV partial 0.174/0.117/0.135, held-out DL 0.120/0.060/0.094 (I2 0), not with the keeping
  axis. (5) Sequence test: no ordering signal beyond the mechanical lag (excess <=1.7pp, sign flips); intersection-born concepts
  take off off-home later (HR ~0.45). (6) 7 most-similar case pairs (7/7 high-OPEN broader, illustration) and a 37-concept
  retrospective AI/CS atlas. Verification: D3 states equal EXP7 on 5.56M cells; ego code reproduces EXP8 exactly; T0 unit
  tests pass; independent re-derivation of all headline numbers <=1e-16; placebos fail. Files: method_out.json (dataset rq2_concepts
  with predict_open_axis=PC1, predict_decomposition=log factors; dataset case_pairs), results/*.json, figures/, case_studies/,
  ai_atlas/, open_features.parquet, panel.parquet, state_sequences.parquet, results/pipeline_counts.json (for the methodology
  figure).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md

--- Item 15 ---
id: art_oKOd21ZMnu9S
type: evaluation
title: Record fixes and openness robustness tests
summary: >-
  Iteration-4 evaluation 3 (EXPLORATORY boundary study + record-correction pack), zero new data, $0 LLM spend. PART A: corrections/00-11
  *.md, insert-ready, each insert tagged [Correction, iteration 4, from art_...]: 01 relabels Exp8 19.5/22.6 as O4 citation
  growth (REL_home -0.114, author_growth +0.065; EBM 0.188 vs B5 0.015; linear model constant) and adds the real O3 transience
  table (only n_authors_early confirmed; L1-logit AUC 0.599 vs B5 0.506); 02 quotes the exact frozen P1-P5 text with verdicts
  and deciding numbers (P3 fails because new_edge_rate TRANSFERS: +0.118 [0.072,0.163], 0 sign flips; corrects dead end 7.4
  and 4.3); 03 Exp7 tables with key paths (volume-matched contrast null DEV and held-out, dose 0.098/0.075/0.304, d_lost A1
  vs R4, d0 concept/two-way/crossed CIs, proximity dependence: min-cp d0 -0.021); 04 the 14 Eval2 blocks; 05 record_tables
  map; 06 the 21 open Eval2 ledger rows; 07 Exp9 not run, iteration counts 3/5, 5/5, 4/5, real artifact ids; 08 candidate
  S and the true 6 families (53 indicators); 09 O5 precedence leakage per source; 10 minor slips (18.11: 22 home mismatches,
  5 DEV + 17 held-out); 11 paper-ready Part B text. Ledger results/claims_ledger_v3.csv: 1,290 rows, 0 MISMATCH, 0 NOT_FOUND;
  independent verify_ledger.py agrees on every row (9 orphan tokens, all section/line numbers). PART B (sealed spec, old held-out):
  Gate T0 reproduces Exp8 exactly. B1: about half of the two biggest breadth effects is pre-onset footprint: M0_density_end
  0.374 -> 0.187 post-onset (attenuation 0.50 [0.38,0.60]); D_vol_end 0.317 -> 0.176 (0.45); post-onset D_vol is nearly rank-identical
  to B5 reach (rho 0.97-1.00). B2: OPEN pooled psp +0.181 [0.082,0.277] (DL4, O2r_m50), 6/6 units positive, prediction interval
  includes 0. B3: 1,920-spec curve: 99.7% of pooled CIs > 0, all estimates > 0, median 0.152, Freedman-Lane p=0.005; contact-reach
  control barely moves it (0.146 vs 0.158). B4: 21 sub-units lower I2 to 0.43; no trait moderates; LIFEENV weakness UNEXPLAINED
  (not coverage, not range restriction) = domain boundary. Step 3: Exp7 D_rca_pers differs from Research 2 D_rca_persist_k
  (max rho 0.877), so that rival remains untested. audit_headlines.py re-derives all headline numbers by a separate code path
  (exact) and a shuffled-OPEN placebo is null. eval_out.json (exp_eval_sol_out, 102 metrics; datasets open_heldout_concepts
  7,728, spec_curve 1,920, claims_ledger_v3 1,290); figures/*.png|pdf.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
- reproducibility.md

--- Item 16 ---
id: art_hSyVUBa2okT2
type: research
title: Is 'keep exploring, spread widest' already known?
summary: |-
  Novelty and positioning report (iteration 4) for the Exp8 openness-vs-consolidation claim, for the Applied Network Science paper. It builds on art_EesdB8cuSfcU and art_dxvRpQufMR0e without redoing their work. Files: research_report.md (Sections A-I), reproducibility.md, raw/ (query log, fetched page extracts, verify.json).

  VERDICTS
  - C1, openness → later cross-field breadth: PARTIALLY ANTICIPATED. The same direction is shown for concept pairs (Maillart 2026: test R² 0.69 entropy / 0.78 exogenous, random 80/20 split), papers (Wang 2017: odds of top-1% citation in foreign fields +62.37%), memes (Weng 2013) and people (Ugander 2012). Concept-level evidence exists only for volume (Cheng 2023) or transfer to patents (Cao 2020). No study found combines the concept unit, a size-adjusted breadth outcome and held-out fields.
  - C2, consolidation → less breadth: PARTIALLY ANTICIPATED in mechanism (Palla 2007 large-group turnover; Ugander; Weng; Burt) and CONTRADICTED-BY on other outcomes:
    - Cheng et al. 2023 ASR, full text read: "ideational consistency" = cosine of neighbour co-usage t−1→t, i.e. weighted edge persistence. +53% next-year articles per SD (b = .43); embeddedness +25%; author co-author density −15%. The DV is volume at t+1, with no current-volume control and in-sample. The authors state they do not study cross-domain translation.
    - Chavalarias & Cointet 2013: dense term-clusters survive; density rises during emergence and falls before decline.
    - Centola 2010 and Romero 2011: clustering helps adoption.
    - Salatino 2017: density among parent topics precedes birth.
    Recommended framing: an outcome-dependent reversal (consistency → depth/survival, churn → reach).
  - C3, a low retention ratio of contacted fields: NEW (analogues only: propagule/colonisation pressure; Palla; Cheng's social consistency b = .02).
  - C4, within-concept closure → entry slowdown: NEW as a lead-lag test. The field-level prior is opposite (Chavalarias). Life-cycle analogues: Singh 2022, Prabhakaran 2016.

  WHAT THE REPORT PROVIDES
  - An our-numbers card (Exp8 held-out psp|B5 with CIs and I²).
  - Strand-by-strand extraction rows for S1-S9.
  - A Cheng operationalisation box with the reconciling sentence.
  - T-RQ1: ours vs Maillart, Cheng, Cao, Wang, Weng, Ugander, Salatino, Chen, Kong. Level AUCs (Krenn 0.85; 0.954-0.967) are marked not comparable.
  - T-RQ2: 12 trajectory/sequence comparators; our contact × retention decomposition and FE event study have no counterpart.
  - 8 ANS papers with relation lines.
  - An 8-lane Fig. 1 spec with {pipeline_counts.json:KEY} slots and a caption.
  - A 14-row reviewer-threat table.
  - 68 newly verified references, 66/67 identifiers resolved via Crossref/arXiv, plus 12 carried.

  CORRECTIONS AND DESIGN GAPS
  - Corrected DOIs: Chen 2012 = 10.1002/asi.21694 (not asi.22662); Moser & Nicholas = 10.1257/0002828041301407; Feldman & Yoon = 10.1093/icc/dtr040.
  - UNVERIFIED (do not cite): Van Noorden 2014, Shinn & Joerges 2002, Fujimura 1992, arXiv 2209.03687 / 2408.06839 / 2606.25320.
  - DESIGN GAPS for the experiments:
    1. ego_density_W3 is not degree-normalised (Ravasz & Barabási C(k) ~ 1/k); add a configuration-null z-score.
    2. Run Cheng's exact consistency/embeddedness measures on volume vs breadth; the predicted result is a sign flip.
    3. Report survival alongside breadth and test the size × turnover interaction (Palla).
    4. Concept-type tagging with within-type tests; no prior effect size exists.
    5. Heterogeneity-robust staggered event-study estimators for C4.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_research_3
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

- [MAJOR MUST-FIX] (evidence) Exp8 outcomes are mislabelled, and the result is a false dead end. The report calls REL_home (-0.114 [-0.180, -0.047]) and author_growth (+0.065 [0.024, 0.106]) 'transience' predictors (19.5), and says the transience EBM gains +0.174 [0.129, 0.219] while the 'transience ElasticNet shrank all coefficients to zero' (19.7, 19.9, 22.6). In art_dFQ6jbgNsR6Q README.md and results/learned_vs_single_heldout.json, all of these are O4 (field/year-normalised citation growth): EBM 0.188 vs B5 0.015, and the linear model is constant. The actual O3 (transience) results are different. n_authors_early is the only confirmed indicator (+0.089 [0.031, 0.148], Holm 0.029, 4/5 units). The O3 L1-logit gains +0.093 AUC [0.028, 0.163] over a B5 that sits at chance (0.506), and B5 + best single gains +0.070. So dead end 22.6 is false: a linear model does predict transience. O4 is one of the request's named outcomes ('future citation growth'), yet it never appears in the report's outcome list (19.1). O1b is missing (n_authors_early +0.029 [0.015, 0.044], confirmed). The learned-model table shows only the O2r_m50 row out of the 8 in the artifact.
  Action: Add O4 and O1b to the outcome list in 19.1. Relabel 19.5 as O4, and add an O3 subsection with the full O3 top-10 table from README.md. Replace the 19.7 table with all 8 rows of the artifact's 'Learned models vs B5' table (O1c, O2r_m50, O2r_resid, O4, O1b, O3, O5, O5_WW, with n and paired CIs). Rewrite dead end 22.6 as 'O4: the linear model shrinks to a constant; the EBM gain is non-linear'. Record O3 as a positive held-out result for n_authors_early and the L1-logit, with the caveat that B5 is at chance.
- [MAJOR MUST-FIX] (evidence) The preregistered predictions in 19.8 and 22.7 are misstated, and one hides a reversal of an iteration-1 dead end. From results/prereg_verdicts.json:
- P1 is not 'entropy is the strongest indicator'. It predicts that entropy, D_rare, D_ratio, participation and NOV_res are positive in >=3/4 groups AND that the pooled psp CI upper bound of the ego indicators is < 0.10. It fails because D_rare (0.162 [0.022, 0.296]), participation (0.150 [0.025, 0.271]) and NOV_res (0.139 [0.033, 0.241]) add MORE than predicted. The iteration-1 primary candidate D_ratio has held-out psp 0.066 [0.001, 0.131]. None of these held-out values for the iteration-1 candidates is in the report.
- P3 predicted that deg_growth, str_growth and new_edge_rate FAIL held-out. It fails because new_edge_rate transfers (+0.118 [0.072, 0.163], 0 sign flips), while degree and strength growth are null. The report inverts this ('cooccurrence growth indicators do not generalise beyond CS') and keeps iteration-1 dead end 7.4 ('raw cooccurrence growth indicators ... fail to generalise') uncorrected.
- P5 predicted that CONTACT_REACH adds NOTHING (CI includes 0). It fails because CONTACT_REACH adds +0.223 even given B5-minus-reach. It is not a 'strongest indicator' prediction.
- P4 fails because RETENTION_RATIO_early is significantly NEGATIVE (-0.120), the opposite sign.
  Action: Rebuild the 19.8 table from prereg_verdicts.json: the exact prediction text from frozen_spec, the verdict, and the quantity that decided it. Add a '[Correction, iteration 3]' to dead end 7.4 and to 4.3's growth-indicator wording, stating that new_edge_rate transfers on 4 held-out groups. Add a held-out table for the iteration-1 candidates (D_ratio, D_rare, participation, NOV_res, entropy, edge_persistence) with pooled psp, CI and per-group raw rho. The iteration-1 story of 'redundant under delta-rho' needs to be squared with a held-out partial CI that excludes 0.
- [MAJOR MUST-FIX] (evidence) Exp7 [art_22ppE1snfHKj]: the report misreads four results and omits two that bound the retained-frontier claim.
(a) Volume-matched (18.5, 22.1). 'd0 0.069 [0.019, 0.118], LR 13.1, positive and significant on dev' is d_R_m, the retained-field coefficient in matched strata. The preregistered criterion is the contrast d_R_m - d_N_m: -0.0085 [-0.071, 0.050] on DEV and -0.028 [-0.105, 0.046] held-out (step2_*.json -> specificity.b_volume_matched.contrast_R_minus_N). In matched cells, entered-but-NOT-retained fields predict entry at least as strongly (d_N_m 0.078 DEV, 0.100 held-out). Only 13-15% of strata match, and they are low-volume (mean n(t-1) about 0.4).
(b) Dose (18.4, 23.1). Held-out betas are 0.098 / 0.075 / 0.304, with monotone_nondecreasing = false and Spearman 0.5. The report quotes only DEV and calls the response monotone.
(c) Abandonment (18.9). The table labels the A1 value (-0.007) as 'R4'. In R4, with d0 and the rivals, d_lost is significantly POSITIVE: +0.064 [0.030, 0.095].
(d) Uncertainty. The two-way (concept, field) clustered SE of d0 is 0.056, against 0.016 concept-only. The held-out crossed CI is [0.201, 0.468]. Deviation 18.11 wrongly says the crossed bootstrap was run on dev only; deviations.json says R3 d0 and A1 d_lost in all units. The deviation 'Standardisation uses min(conditional probability) capping' misreads the min-cp proximity sensitivity.
(e) Sensitivities (18.6) quote DEV values although held-out values exist: target-field FE 0.300, RCA-defined entry event 0.243, primary-topic fields 0.276, min_n = 5 0.277, excluding intersection-born 0.332.
(f) Omitted: under Hidalgo's min-conditional-probability proximity, d0 = -0.021 +/- 0.009 (p = 0.012) held-out and -0.024 on DEV, while RCA>1 density becomes strong (LR 246).
  Action: Replace 18.4-18.6 and 18.9 with tables built from step2_dev.json and step2_heldout.json:
- Volume-matched: d_R_m, d_N_m and the R-N contrast for the coarse and fine bins, DEV and held-out, with match rates and the balance means.
- Dose: DEV and held-out betas, with the monotone flag.
- d_lost: A1 and R4 side by side.
- d0 uncertainty: concept, two-way and crossed CIs.
- Sensitivities: held-out values.
Add a subsection 'Proximity dependence' with the min-cp result, and state in 18.10 and 23.1 that the retained frontier holds on the sparse PMI backbone but not under the standard Hidalgo proximity. Correct 22.1 so it says the retained-minus-nonretained contrast is null on DEV as well.
- [MAJOR MUST-FIX] (novelty) Section 23.1 lists the retained frontier as a confirmed (PARTIAL) finding 'beyond the Hidalgo/Guevara RCA density rival'. The nearest published neighbour is Hidalgo et al. (2007) density built on the product-space proximity, the minimum conditional probability. Exp7 ran exactly that proximity, and the effect vanished and reversed (-0.021, p = 0.012). What survives is therefore narrower than the report says. On a positive-PMI 26-field backbone, relatedness to persistently present fields out-predicts RCA>1 density in relative odds. It does not do so on the additive-probability scale (LPM approximately 0 with size deciles). It does not do so under the standard proximity, and it is not separable from volume (retained is about equal to non-retained in matched cells). Research 2 [art_EesdB8cuSfcU] judged Claim A 'partially anticipated' without knowing the min-cp result. Its 'missing rival' D_rca_persist_k was already in Exp7's S_strict as D_rca_pers (d0 0.304 [0.268, 0.336]). Yet 21.2, 22a and 23 still call it untested. The Cheng et al. (2023) 'consistent usage' neighbour and Pinheiro et al. (2022) are named, but the report never states what this run adds beyond them in light of these limits.
  Action: Add a short 'nearest-neighbour check' paragraph to 18.10. Name Hidalgo 2007 (min-cp density), Guevara 2016 (entry AUC 0.68-0.90 vs our global R3 0.837, different unit) and Pinheiro 2022 / Cheng 2023. Say what survives: a PMI-backbone relative-odds effect, not separable from volume. State that D_rca_pers (persistence-filtered RCA density) was in S_strict, and either show it matches Research 2's D_rca_persist_k or say how the two differ. Remove 'D_rca_persist_k untested' from 22a and 23 Open if they are equivalent. Downgrade 23.1 from 'Confirmed' to 'Partial, backbone-specific'.
- [MAJOR MUST-FIX] (evidence) None of Evaluation 2's corrections were applied. Evaluation 2 [art_7W9xiIO3FVBs] audited 246 claims, flagged 58 as blocking and wrote text_corrections.md with 14 old/new blocks and source keys, plus record_tables/ holding the missing iteration-1/2 tables. The report summarises the counts (20.1) and applies nothing. The iteration-1/2 text is identical to iter_3/gen_strat/current_report.md:
- 10.3 still says 'DISCONFIRMED by all preregistered criteria', although the within-field LPM passes (+0.068, p_concept 0.041).
- 10.6 still says '0 of 40 shuffled outcomes exceed the real value'. It omits the held-out CI [-0.006, 0.065] and the DEV-to-held-out shrinkage to 0.21.
- 11.3 and 16.3 still call ordering 'CONFIRMED'. The audit rewrote it as MIXED: 57/175 = 32.6% of broad concepts, negative lead-lag coefficients, a pre-trend at ev-3 of -0.072, and a DEV reverse effect of b 0.232.
- 13.1 still gives external-entry counts (3,583 / 17,872 / 8,462; the concept counts are 1,298 / 1,121 / 2,635) and 6,540 for Wikipedia.
- 5.4 still shows 'B5 + all_four' (it is size_controlled_all_three; refit CI [-0.043, 0.220]).
- 4.4 still says 7 partials are 'not available in the current workspace'.
- 10.7's power figure is still misattributed (0.004 is the 90% point).
- 10.5 does not state that the gain is held-out only.
- The iteration-2 coverage column and the Exp5-vs-Exp6 frame comparison (retention kappa 0.28) are still missing.
Section 23 silently drops ordering and H3 from 'Confirmed' without listing them anywhere else. This leaves nearly every MUST-FIX item from the previous review open, although the fixes are sitting on disk.
  Action: For each of the 14 blocks in text_corrections.md, insert the 'New' text in place in the named section, marked '[Correction, iteration 3, from art_7W9xiIO3FVBs]', with its source keys. Paste record_tables/portability_F3.csv (34 rows) into 4.3, partial_association_all.csv (12 rows) into 4.4, lineage_robustness_iter1.csv into 3.x, refit_bootstrap_iter1.csv as a refit-CI column in 6.2, h1_criteria.csv into 10.3, ordering_mixed.csv into 11.3, frame_overlap_by_group.csv and definitions_diff.csv into 9/11, and o5_coverage_by_group_source.csv into 13.1. In 20.1, list the 6 MISMATCH and 15 MISLABELLED rows individually (claim_id, section, reported value, source value). Move ordering and H3 in 16 and 23 to 'Mixed / not established'.
- [MAJOR MUST-FIX] (evidence) A failed iteration-3 artifact is missing from the record. gen_art_experiment_9 (plan gen_plan_experiment_3, 'How new concepts spread: paths and reasons') was commissioned and failed. .aii_worker_result.json has failed = true, with 'output_format validation failed after 5 retries'. The log shows method.py was never run. This was iteration 3's entire RQ2 artifact:
- log-additive contact x frontier x retention decomposition with Shapley shares;
- DTW + 4-state HMM typology on the 12,499-concept panel, with a naming rule of ARI >= 0.5;
- home-prominence vs off-home-retention sequence tests with event studies and pre-trend tests;
- 6-8 case studies with alluvial figures and a lineage check;
- O5 timing per class.
The report says 'Four artifacts were executed', as if four were commissioned. The coverage table marks RQ2 trajectories 'Not extended' without saying why. Section 23 keeps 'two stable trajectory classes' under 'Confirmed' while listing the HMM ARI of 0.094 as 'Open'. Exp8's results/case_exemplars.json is also never mentioned.
  Action: Add a 'Failed artifacts, iteration 3' subsection like 5a: name gen_art_experiment_9, its plan, the failure mode (never executed; the output-format loop failed) and what was lost. List it in 22 as 'not run, not refuted'. In 23, move the two-class trajectory claim to 'Mixed / not established': HMM-vs-DTW ARI 0.094, the dev localised class is 55 Med + 7 Eng, and the held-out recluster ARI is 0.54. Make re-running Exp9 unchanged the first priority of the next iteration; it needs zero credits and runs on existing arrays.
- [MAJOR MUST-FIX] (evidence) Items tested in iteration 3 are still called untested, and Exp8's indicator families are misreported.
- Section 23 Open says 'Candidate S (unconnected coauthor groups, Cheng et al. 2023) remains untested'. Exp8 computed the co-author S family (S_comp, S_comp_n, S_isolated_share; indicator_dictionary.csv, family S) and scored it held-out. S_comp_n was in the frozen top 10 for O1c (-0.087 [-0.200, 0.029], Holm 1), O3 (+0.068 [0.001, 0.134], Holm 0.41), O1b (+0.028, Holm 0.70) and O5. None was confirmed. Candidate S has therefore been tested and not confirmed, which dead end 7.7 must record.
- Section 19.1 lists 7 families, including 'Lineage (edge_persistence, relay_share)' and 'External recognition' as INDICATOR families. The artifact has 6 families: E popularity 6, F disciplinary 3, G landing 7, FR retained-frontier 7, A co-occurrence ego-network 27, S co-author 3. There are 53 in total, O5 is an outcome, and edge_persistence belongs to A.
- The D family (D_ratio, D_rare, D_z, D_sub, D_obs) was never eligible for freezing because more than 30% of its values were missing. The report does not say so.
  Action: Replace the family list in 19.1 with the six families and their counts from indicator_dictionary.csv, and note the D-family exclusion rule (deviations.json). Update 7.7 and the 23 Open list: 'Candidate S: computed on 12,499 concepts in iteration 3 (S_comp, S_comp_n, S_isolated_share); not confirmed for any outcome (table)'. Add the S rows from the README tables.
- [MAJOR MUST-FIX] (rigor) Exp8's strongest 'early network' indicators are partly pre-onset footprint, and the per-field results the request requires are absent.
- The artifact itself warns that M0_density_end and D_vol_end use cumulative field history from 1995 to t0+2. Part of their signal is therefore a pre-onset field footprint, and the top-scoring held-out concepts are generic terms such as 'Coefficient of variation' and 'Exponential growth'. The report files this as a deviation (19.9) but still headlines M0_density_end as the strongest confirmed indicator (19.2, 23.2) without the caveat.
- The request asks for results 'globally and within individual scientific fields'. heldout_unit_results.csv has 726 per-unit rows, but the report gives only pooled values and '6/6 sign agreement'. That wording hides per-group nulls: NOV in LIFEENV is 0.033 [-0.046, 0.119] and in COH_OTHER 0.038 [-0.032, 0.109]; n_comm_W3 in LIFEENV is 0.055 [-0.017, 0.136], with I2 of 0.75-0.78 for both.
- Excluding intersection-born concepts halves CONTACT_REACH (+0.111). The report does not say so.
  Action: Add the footprint caveat next to M0_density_end and D_vol_end in 19.2 and 23.2. Re-score both with a post-onset-only window (t0..t0+2 papers only) on the existing Exp8 arrays, at zero credits. Add a per-group table (PHYS, LIFEENV, SOC, MATHDEC, two cohort parts: rho [CI], n) for the confirmed O2r indicators from heldout_unit_results.csv, and mark each cell whose CI includes 0. Add the robustness rows from sensitivities_pooled.json (EXP6-overlap exclusion, coverage covariates, O2r_m30, intersection-born exclusion).
- [MAJOR MUST-FIX] (clarity) The iteration-3 artifact markers are placeholders, so the new results cannot be traced. Sections 17-21 cite [ARTIFACT:art_experiment_7], [ARTIFACT:art_experiment_8], [ARTIFACT:art_evaluation_2] and [ARTIFACT:art_research_2]. None of these ids exists. The real ids are art_22ppE1snfHKj (Exp7), art_dFQ6jbgNsR6Q (Exp8), art_7W9xiIO3FVBs (Eval2) and art_EesdB8cuSfcU (Research 2). No iteration-3 table names its output file or key. The paper step and the link-injection step cannot resolve these markers.
  Action: Substitute the real ids in every marker. Under each iteration-3 table, add a 'Source:' line with the file and key path, for example 'results/step2_heldout.json -> units.*.R3' and 'results/prereg_verdicts.json', following Eval2's text_corrections.md convention.
- [MAJOR MUST-FIX] (scope) Coverage of the original request is partial.
- RQ1: the 53-indicator held-out screen now exists, with the learned model. However, the request's exploratory stage 1 (a focused AI domain, inspecting network evolution before fixing the method) was never done.
- The 'explain why the strongest indicators work' analysis and the case studies were not started. Exp8 even produced case_exemplars.json, which the report does not use.
- RQ2: 'which network trajectories distinguish locally concentrated from broadly integrated concepts' rests on 188 concepts from Exp6's 653-newborn frame, and the HMM does not reproduce that typology (ARI 0.094). The iteration-3 artifact that would have answered RQ2 on 12k concepts failed and is unrecorded.
- The request's question 'do concepts first become central within their original community and then diffuse, or emerge at intersections?' has no test on record. The ordering result that came closest was rewritten as MIXED by Eval2.
  Action: Name these gaps in 22a with the reason each is open (Exp9 failed; not attempted). Set the next iteration's priorities: (1) re-run Exp9 on the EXP5 frame (typology with the DTW-HMM agreement rule, the home-prominence-before-diffusion sequence test, case studies from quantitative extremes); (2) run the 'why it works' decomposition for CONTACT_REACH and n_comm_W3, the two confirmed indicators that are purely post-onset, using case_exemplars.json.
- [MINOR] (clarity) Small factual and bookkeeping slips:
- Section 23: 'twelve artifacts (ten commissioned, eight completed in iteration 1; ...)' is wrong. Iteration 1 completed 3 of 5, iteration 2 completed 5 (Exp6 was re-run after a crash), and iteration 3 completed 4 of 5.
- 19.6 cites 'Section 21.2' for the O5 result; it is 20.2.
- 18.11's '7 home field mismatches ... (17 of 11,841 concepts)' is self-contradictory.
- 20.2 gives '67% at or before t0' as if it held for every source. o5_validation.json precedence_leakage varies by source (MeSH 0.70, Gartner 0.68, ACM CCS 0.17).
- The O5-O3 association is significant (pooled -0.049, p = 0.004, I2 0.55, positive in LIFEENV), yet it is dismissed as 'not robust' without that detail.
  Action: Fix the count sentence and the cross-reference. Give per-source leakage shares and lags from o5_validation.json. Report the O3 association with its p-value and per-group values.
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

### [3] ASSISTANT · 2026-09-29 04:47:08 UTC

```
I'll start by checking the workspace and the artifact output files, then verify the headline numbers against them.
```

### [4] TOOL CALL — Bash · 2026-09-29 04:47:08 UTC

```
List workspace and iteration 4 artifact directories:
ls -la && ls -la .aii 2>/dev/null; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/user_uploads 2>/dev/null | head
```

### [5] TOOL RESULT — Bash · 2026-09-29 04:47:08 UTC

```
{"stdout": "total 1993\ndrwxr-xr-x 3 root root 1003158 Sep 29 04:46 .\ndrwxr-xr-x 3 root root 1003158 Sep 29 04:46 ..\ndrwxr-xr-x 2 root root       1 Sep 29 04:46 .aii\n-rw------- 1 root root      54 Sep 29 04:46 .aii_claude_session.json\n-rw-r--r-- 1 root root   32468 Sep 29 04:47 .repl_agent.ptylog\ntotal 981\ndrwxr-xr-x 2 root root       1 Sep 29 04:46 .\ndrwxr-xr-x 3 root root 1003158 Sep 29 04:46 ..\ngen_art_evaluation_3\ngen_art_experiment_10\ngen_art_experiment_11\ngen_art_experiment_12\ngen_art_research_3\ngen_art\ngen_plan\ngen_report_text\ngen_strat\nreview_report", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [6] ASSISTANT · 2026-09-29 04:47:12 UTC

```
The iteration 4 folder has a `gen_art_experiment_11` that the supplementary list doesn't mention. I'll check it first.
```

### [7] TOOL CALL — Bash · 2026-09-29 04:47:12 UTC

```
List contents and worker results of each iter-4 artifact:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art; for d in *; do echo "== $d"; ls $d | head -40; cat $d/.aii_worker_result.json 2>/dev/null | head -c 800; echo; done
```

### [8] TOOL RESULT — Bash · 2026-09-29 04:47:14 UTC

```
{"stdout": "== gen_art_evaluation_3\nREADME.md\naudit_headlines.py\nbuild_corrections.py\ncorrections\neval.py\neval_out.json\nfigures\nfigures.py\nfull_eval_out.json\nheterogeneity.py\nlib\nlogs\nmini_eval_out.json\npartb_core.py\npreview_eval_out.json\npyproject.toml\nreproducibility.md\nresults\nrun_all.sh\nseal.py\nspec_curve.py\nstep3_drca.py\nuv.lock\nvendor\nverify_ledger.py\n{\"pod_id\": \"oqj5wo6i4da82b\", \"result\": {\"final_response\": \"I'll treat the pasted spec as the task for this workspace. First I'm checking what the crashed attempt left behind and the process/thread limits, since `BlockingIOError` on spawn usually means the PID/thread limit was exhausted, not RAM.\\nConfirmed: OpenBLAS tried to start 48 threads per process and `pthread_create` failed. Every script will now pin BLAS to one thread. Reading the existing code in full:\\nMost of Part B survived the crash. Checking which outputs are complete: T0 gate, B2's `KeyError`, whether the spec-curve null ran all 200 draws, and whether heterogeneity was only the mini run.\\nStill mapping the Exp7 record keys so the corrections pack can cite them by path. Narrowing the search:\\nB2 is done, and the heterogeneity\n== gen_art_experiment_10\nREADME.md\n__pycache__\naudit.py\ndata\nfigures\nfull_method_out.json\ninputs\nlib\nllm_cache\nlogs\nmake_outputs.py\nmake_report.py\nmethod.py\nmethod_out.json\nmini_method_out.json\nmodels\npassC\npassC.py\nprereg.md\npreview_method_out.json\npyproject.toml\nreadme_tables.py\nrederive.py\nreproducibility.md\nrequirements.lock.txt\nrestore.sh\nresults\ns0_prereg.py\ns1_candidates.py\ns3_checks.py\ns4_gate.py\ns5_typing.py\ns6_covariates.py\ns7_ego.py\ns8_select.py\ns9_unseal.py\ns_learned.py\nsnapshot\ntests\n{\"pod_id\": \"xkyttc13i3t5ra\", \"result\": {\"final_response\": \"I'm running the 2015\\u201316 cohort confirmation experiment. I've surveyed the EXP5 and EXP8 code and am now adapting the snapshot pass so it can start in the background as early as possible.\\nThe venv is set up and the S3 manifest has been located. Next I'll check whether the snapshot has changed since EXP5, then write the snapshot pass.\\nNow S1, the cohort candidate frame script.\\nPass C (the snapshot scan) is running in the background. While it runs, I'm reading the EXP8 ego-network, outcome and statistics code so the HOME and SIZE-MATCHED builds reuse it exactly.\\nI restarted the snapshot pass with 9 workers, because at 7 its ETA was about 155\\u2013185 min. While it runs I'm writing the pre-registration and the HOME and SIZE-MA\n== gen_art_experiment_11\nREADME_template.md\n__pycache__\nanalysis_fe.py\naudit.py\nbuild_d3.py\nbuild_features.py\nchecks_m.py\ndata\nevent_study.py\nfigures\ninputs\nlib\nlogs\nmake_outputs.py\nmethod.py\nmodels\npartners.py\npassA\npassB\npassM\npassM.py\nprereg.md\npreseal.py\npyproject.toml\nreproducibility.md\nrequirements.lock.txt\nresults\nsequence.py\nsnapshot\ntests\ntopic_typing.py\nunit_tests.py\n\n== gen_art_experiment_12\nREADME.md\nai_atlas\naudit_headlines.py\ncase_studies\ndata\ndtw_cache\nfigures\nfull_method_out.json\nlib\nlogs\nmethod.py\nmethod_out.json\nmini_method_out.json\nopen_features.parquet\npanel.parquet\npreview_method_out.json\npyproject.toml\nrederive.py\nreproducibility.md\nrequirements.lock.txt\nrestore.sh\nresults\ns0_skeleton.py\ns10_outputs.py\ns2_open.py\ns3_states.py\ns4_decomp.py\ns5_typology.py\ns6_sequence.py\ns7_seal.py\ns8_cases.py\ns9_atlas.py\nstate_sequences.parquet\ntests\n{\"pod_id\": \"btwsi8sbywu2el\", \"result\": {\"final_response\": \"I'll check the workspace and the files the plan refers to before deciding anything.\\nThe workspace is empty apart from pipeline metadata. The full plan may be on disk, so I'll look for it.\\nThe full plan is on disk (about 42K characters). I'll read all of it.\\nThe inputs exist on disk, so the plan can be carried out. Next I'll check the inputs and the hardware limits.\\nThe inputs and hardware check out: 48 cores and about 250 GB of RAM. I'll load the required skills, starting with the output-format one, which the plan makes a hard gate.\\nI'll set up the environment in the background while I look at the data.\\nNow the shared library module:\\nS0 comes next: the skeleton, its validation and the provenance hashes.\\nS0 passes validation\n== gen_art_research_3\nREADME.md\nraw\nreproducibility.md\nresearch_out.json\nresearch_report.md\nresearch_verification.json\nscripts\n{\"pod_id\": \"cqkmk3cp9mnx69\", \"result\": {\"final_response\": \"I'll run this research task in the workspace. First I'll check the workspace, the prior reports and the web-tools skill.\\nNow our numbers from Exp8.\\nNext batch: Chen 2012, the novelty-to-impact papers, method-vs-object diffusion, GPT generality, and C3/C4 targeted queries.\\nThree candidate direct precedents came up: Cao et al. 2020 (EMNLP Findings), McKeown et al. 2016 (JASIST) and Osborne et al. 2017 (K-CAP). Checking each one's unit, features and outcome.\\nNow I'm verifying references (Crossref/arXiv) in the background and filling the remaining gaps: the Osborne 2017 abstract, new ANS candidates and a Weng quote carried from the prior report.\\nResearch phase is mostly done. Before writing, I'm pulling the exact Exp8 indicator de", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-29 04:47:16 UTC

```
Inspect Experiment 11 outputs and logs:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11; ls -la; ls results logs figures data | head -60; cat prereg.md | head -80; tail -50 logs/* 2>/dev/null | tail -80
```

### [10] TOOL RESULT — Bash · 2026-09-29 04:47:16 UTC

```
{"stdout": "total 24215\ndrwxr-xr-x 18 root   root   3000154 Sep 29 03:30 .\ndrwxr-xr-x  7 root   root   3000468 Sep 29 02:14 ..\ndrwxr-xr-x  2 root   root   1000119 Sep 29 03:21 .aii\n-rw-------  1 root   root        18 Sep 29 03:30 .aii_claude_session.json\ndrwxr-xr-x  8 231072 231072 1024625 Sep 29 03:15 .git\n-rw-r--r--  1 231072 231072      39 Sep 29 03:23 .gitignore\n-rw-r--r--  1 231072 231072 1386225 Sep 29 03:30 .repl_agent.ptylog\ndrwxr-xr-x  7 231072 231072 3000110 Sep 29 02:20 .venv\n-rw-r--r--  1 231072 231072   10208 Sep 29 03:18 README_template.md\ndrwxr-xr-x  2 231072 231072 1008528 Sep 29 03:01 __pycache__\n-rw-r--r--  1 231072 231072   14781 Sep 29 02:51 analysis_fe.py\n-rw-r--r--  1 231072 231072    5939 Sep 29 03:16 audit.py\n-rw-rw-rw-  1 231072 231072    5628 Sep 29 02:42 build_d3.py\n-rw-r--r--  1 231072 231072    7254 Sep 29 02:33 build_features.py\n-rw-r--r--  1 231072 231072    2801 Sep 29 02:54 checks_m.py\ndrwxr-xr-x  3 231072 231072 2014976 Sep 29 03:26 data\n-rw-r--r--  1 231072 231072   10428 Sep 29 02:52 event_study.py\ndrwxr-xr-x  2 231072 231072       1 Sep 29 02:19 figures\ndrwxr-xr-x  3 231072 231072 2002001 Sep 29 02:19 inputs\ndrwxr-xr-x  3 231072 231072 1032327 Sep 29 02:50 lib\ndrwxr-xr-x  2 231072 231072 1033784 Sep 29 03:24 logs\n-rw-r--r--  1 231072 231072   20313 Sep 29 03:18 make_outputs.py\n-rw-rw-rw-  1 231072 231072    6285 Sep 29 03:20 method.py\ndrwxr-xr-x  2 231072 231072       1 Sep 29 02:23 models\n-rw-r--r--  1 231072 231072   12588 Sep 29 03:14 partners.py\ndrwxr-xr-x  3 231072 231072       1 Sep 29 02:23 passA\ndrwxr-xr-x  3 231072 231072       1 Sep 29 02:23 passB\ndrwxr-xr-x  3 231072 231072 2027994 Sep 29 02:19 passM\n-rw-r--r--  1 231072 231072   12134 Sep 29 02:23 passM.py\n-rw-r--r--  1 231072 231072    4132 Sep 29 03:15 prereg.md\n-rw-r--r--  1 231072 231072   13010 Sep 29 02:50 preseal.py\n-rw-rw-rw-  1 231072 231072    2947 Sep 29 03:20 pyproject.toml\n-rw-r--r--  1 231072 231072    2859 Sep 29 03:21 reproducibility.md\n-rw-r--r--  1 231072 231072    2110 Sep 29 03:20 requirements.lock.txt\ndrwxr-xr-x  2 231072 231072 1047576 Sep 29 03:25 results\n-rw-r--r--  1 231072 231072    8684 Sep 29 03:15 sequence.py\ndrwxr-xr-x  2 231072 231072 1038834 Sep 29 02:19 snapshot\ndrwxr-xr-x  2 231072 231072 1000268 Sep 29 03:13 tests\n-rw-r--r--  1 231072 231072   10935 Sep 29 02:36 topic_typing.py\n-rw-rw-rw-  1 231072 231072   13577 Sep 29 02:49 unit_tests.py\ndata:\nbg_topics.npz\nboot_fe_DEV.parquet\nbridging_papers.parquet\nclosure_jumps.parquet\ncounts_m.parquet\nd3_concept_year.parquet\nframe_matches_long\ngrounded_V.npz\npartner_indicators.parquet\npassM_info.json\nport_static.parquet\nstatic_partners.parquet\nstatic_partners_typed.parquet\nw3_comms.json\nyearly_features.parquet\nyearly_panel.parquet\n\nfigures:\n\nlogs:\nanalysis_fe.log\nanalysis_fe.out\nanalysis_fe.pid\nattach.log\nbuild_d3.log\nbuild_features.log\nchecks_m.log\nevent_study.log\nevent_study.out\nevent_study.pid\nllm_calls.jsonl\nmethod.log\npartners.log\npartners.out\npartners.pid\npassM.log\npassM.pid\npassM_run.out\npreseal.log\nseal.log\nsmoke.log\nsmoke.pid\ntopic_typing.log\nunit_tests.log\nunit_tests.out\nunit_tests.pid\n\nresults:\nchecks.json\nd3_validation.json\ndeviations.json\nfe_results.json\nfrozen_spec.json\nllm_cost.json\nport_check.json\npreseal_diagnostics.json\nprovenance.json\ntopic_type_benchmark.json\ntopic_type_benchmark_sample.csv\n# Pre-registration: does home-only closure precede slower off-home spread? (within-concept)\n\nFrozen 2026-09-29 03:15:45 BEFORE any D3 outcome column was joined to the yearly feature panel.\nThe sha256 of `results/frozen_spec.json` is recorded in `logs/seal.log`; `lib/seal_m.attach_outcomes` refuses to\njoin outcomes unless that hash and the feature-file hash still match.\n\n**Honest note.** EXP7/EXP8 already looked at D3 states and static breadth for these concepts; this seal controls only the new within-concept yearly estimand. This is therefore MECHANISM evidence, not confirmation.\n\n## Panel\n- Rows: concept x calendar year t, t0 <= t <= min(t0+10, 2022) - 1 (outcome year t+1 <= 2022); sample: fields at risk at end of t > 0; home-only deg(t) >= 2.\n- Features (HOME-ONLY papers, 1-year windows, EXP3 backbone): new_rate, n_comm, participation, nov_res, density,\n  persistence; dens_adj (degree-matched null); deg; kcore. OPEN_home = mean of signed z-scores (>= 4 of 6).\n- Frozen DEV z constants: {\"new_rate\": [0.19747, 0.55965], \"n_comm\": [2.21405, 1.13443], \"participation\": [0.32751, 0.2415], \"nov_res\": [-0.47354, 0.44913], \"density\": [0.72141, 0.25062], \"persistence\": [0.26432, 0.20375]}\n- Controls: log1p_home_works(t), log1p_all_works(t), log1p_deg(t), log_at_risk (end of t); FE: concept + calendar year; clustering: concept.\n\n## Pre-seal feature-only decisions\n- F4: share of DEV eligible concept-years with deg >= 2 = 0.740 -> min_n = 2 kept (share >= 0.40).\n- F6: closure-jump threshold = 1.0 within-concept SD; treated DEV concepts =\n  2754 (never-treated 1203).\n- Share of eligible rows using the clamped 2010-14 backbone slice: 0.315.\n- Corr(density, log deg) on DEV = -0.281 (motivates the log-degree control and dens_adj).\n\n## Predictions and verdict rules\n- H-M1: DEV PPML beta_density < 0 with concept-clustered 95% CI < 0\n- H-M2: DEV PPML beta_OPEN > 0 with 95% CI > 0   (Holm over H-M1, H-M2)\n- H-M3: |std beta_fwd| - |std beta_rev| > 0 with paired bootstrap 95% CI > 0\n- H-M4: mean lag 0..+2 < 0 with CI < 0; pre-trend Wald p > 0.10 and max |lead| < 0.5 |mean lag|; event-date permutation p < 0.05\n- H-M5: signs of H-M1 and H-M2 hold on OLD_HELDOUT and COHORT\n- H-S1: intersection-born concepts take off WITHOUT a prior home-prominence peak more often than single-home concepts (share difference > 0, concept-bootstrap CI > 0)\n- H-P1: (exploratory) METHOD and new-community partners carry more of the new_edge_rate signal than DOMAIN and same-community partners\n- SUPPORTED = H-M1 & H-M2 (Holm) & H-M3 & H-M4 & H-M5 signs; PARTIAL = H-M1 or H-M2 holds but H-M3 or H-M4 fails;\n  NOT SUPPORTED = both H-M1 and H-M2 CIs include 0 on DEV.\n\n## Estimators\n- H-M1/H-M2: pyfixest fepois y(t+1) ~ X(t) + controls | ci + year; CRV1 by concept; 2,000 concept-cluster bootstrap refits (duplicates relabelled as new FE units), percentile 95% CI\n- binary: feols any_entry(t+1) ~ same | ci + year (LPM twin)\n- H-M3: feols both directions: entries(t+1) ~ density(t) + controls(t) and density(t+1) ~ entries(t) + controls(t+1), | ci + year; std beta = beta * SD_w(x) / SD_w(y) with FE-demeaned SDs; paired concept bootstrap of |std fwd| - |std rev|\n- H-M4: Sun-Abraham interaction-weighted event study around the first closure jump; leads -3..-2, lags 0..+4 (e=-1 omitted; e<=-4 and e>=5 binned per cohort, not reported); never-treated controls (primary) and last-treated cohort (not-yet-treated) variant; concept-cluster bootstrap 1,000; event-date permutation placebo 1,000 draws; home-volume outcome check\n- closure_jump: first t with age >= 2, deg(t) >= 3, density(t) - density(t-1) >= 1.0 x within-concept SD of density over t0..h_end (>= 5 defined years)\n- pooling: per group within body; DerSimonian-Laird with I2 over groups\n- multiplicity: Holm over {H-M1, H-M2}\n\n## Pre-declared robustness\n- dens_adj instead of density\n- exclude Medicine homes\n- exclude intersection-born\n- drop rows with year >= 2015\n- ALL-PAPERS density (coupling contrast)\n- exclude home coverage < 0.5\n- log at_risk as offset\n- S1 age FE instead of year FE\n- S2 add cum_entries(t-1)\n- home-field x year FE\n- joint model density + OPEN_home", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-29 04:47:20 UTC

```
Read Experiment 11 FE results and final logs:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11; ls -la .aii; cat .aii/* 2>/dev/null | head -c 1500; echo; python3 -c "
import json;d=json.load(open('results/fe_results.json'));print(json.dumps(d,indent=1)[:5000])"; tail -5 logs/method.log logs/event_study.log logs/partners.log logs/analysis_fe.log; tail -c 3000 .repl_agent.ptylog | strings | tail -30
```

### [12] TOOL RESULT — Bash · 2026-09-29 04:47:20 UTC

```
{"stdout": "total 3909\ndrwxr-xr-x  2 root   root   1000119 Sep 29 03:21 .\ndrwxr-xr-x 18 root   root   3000154 Sep 29 03:30 ..\n-rw-r--r--  1 231072 231072    1219 Sep 29 03:21 manifest.yaml\nentries:\n  - path: data/frame_matches_long/\n    keep: 5.3M grounded concept-paper rows from a 27-min snapshot pass; input of every yearly feature (costly to regenerate)\n  - path: data/yearly_panel.parquet\n    keep: sealed-then-joined concept-year panel reused by iteration 5 and Art 3\n  - path: data/yearly_features.parquet\n    keep: sealed feature file whose sha256 is in results/frozen_spec.json\n  - path: data/\n    keep: small derived tables, bootstrap and placebo draws behind the reported CIs\n  - path: results/\n    keep: all reported results\n  - path: figures/\n    keep: paper figures\n  - path: full_method_out/\n    keep: method output parts\n  - path: .venv/\n    delete: redownloadable\n    source: \"uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r requirements.lock.txt\"\n  - path: passM/parts/\n    delete: regenerable\n    source: \".venv/bin/python passM.py --workers 20\"\n  - path: __pycache__/\n    delete: regenerable\n    source: \"python (created automatically on import)\"\n  - path: lib/__pycache__/\n    delete: regenerable\n    source: \"python (created automatically on import)\"\n  - path: tests/__pycache__/\n    delete: regenerable\n    source: \"python (created automatically on import)\"\n\n{\n \"spec_sha\": \"7f2634add5f792fe9f3081c8d61287bc873d57327ceb0c61e3b137b2bce83236\",\n \"sample_counts\": {\n  \"DEV\": {\n   \"concept_years_t0_to_hend_minus1\": 47710,\n   \"concepts\": 4771,\n   \"rows_at_risk\": 47710,\n   \"rows_deg_ge2_at_risk\": 35328,\n   \"dropped_share_deg_lt2\": 0.2595263047579124\n  },\n  \"OLD_HELDOUT\": {\n   \"concept_years_t0_to_hend_minus1\": 33720,\n   \"concepts\": 3372,\n   \"rows_at_risk\": 33720,\n   \"rows_deg_ge2_at_risk\": 20314,\n   \"dropped_share_deg_lt2\": 0.39756820877817317\n  },\n  \"COHORT\": {\n   \"concept_years_t0_to_hend_minus1\": 41363,\n   \"concepts\": 4356,\n   \"rows_at_risk\": 41363,\n   \"rows_deg_ge2_at_risk\": 25925,\n   \"dropped_share_deg_lt2\": 0.3732321156589222\n  }\n },\n \"DEV\": {\n  \"n_rows\": 35328,\n  \"n_concepts\": 4661,\n  \"share_rows_all_zero_concepts\": 0.1785835597826087,\n  \"mean_y_next\": 0.25772758152173914,\n  \"share_any_next\": 0.21957087862318841,\n  \"H_M1_density\": {\n   \"b\": -0.07007581591010123,\n   \"se\": 0.0563105730669377,\n   \"ci\": [\n    -0.18044251107011033,\n    0.04029087924990786\n   ],\n   \"p\": 0.21333318542474888,\n   \"n\": 28989,\n   \"n_concepts\": 3463,\n   \"n_concepts_used\": 4661,\n   \"sd_within_x\": 0.20295510338391137,\n   \"pct_per_within_sd\": -1.4121586104921091\n  },\n  \"H_M2_open\": {\n   \"b\": 0.015404541259402072,\n   \"se\": 0.0273889157796701,\n   \"ci\": [\n    -0.03827674724435211,\n    0.06908582976315625\n   ],\n   \"p\": 0.5738182752468741,\n   \"n\": 28989,\n   \"n_concepts\": 3463,\n   \"n_concepts_used\": 4661,\n   \"sd_within_x\": 0.42173140334682396,\n   \"pct_per_within_sd\": 0.6517727344231394\n  },\n  \"joint\": {\n   \"density\": {\n    \"b\": -0.07317977774232762,\n    \"se\": 0.06954695075129218,\n    \"ci\": [\n     -0.20948929644944117,\n     0.06312974096478594\n    ],\n    \"p\": 0.2926914680966832,\n    \"n\": 28989,\n    \"n_concepts\": 3463\n   },\n   \"OPEN_home\": {\n    \"b\": -0.0026718459279541262,\n    \"se\": 0.033723866900153776,\n    \"ci\": [\n     -0.06876941047167798,\n     0.06342571861576973\n    ],\n    \"p\": 0.9368519483178539,\n    \"n\": 28989,\n    \"n_concepts\": 3463\n   }\n  },\n  \"lpm_density\": {\n   \"b\": -0.013811516238125118,\n   \"se\": 0.010105634205821445,\n   \"ci\": [\n    -0.03362353957551618,\n    0.006000507099265943\n   ],\n   \"p\": 0.17178330352596394,\n   \"n\": 35155\n  },\n  \"lpm_open\": {\n   \"b\": 0.003510883988820717,\n   \"se\": 0.005228633890967297,\n   \"ci\": [\n    -0.006739815231109886,\n    0.013761583208751321\n   ],\n   \"p\": 0.5019541248378494,\n   \"n\": 35155\n  },\n  \"H_M3_point\": {\n   \"b_fwd\": -0.011332175447951207,\n   \"b_rev\": 0.0008528556783903947,\n   \"std_fwd\": -0.004805354674945602,\n   \"std_rev\": 0.002108614040651668,\n   \"diff\": 0.002696740634293934,\n   \"n_fwd\": 35328,\n   \"n_rev\": 35297\n  },\n  \"by_group\": {\n   \"BGM\": {\n    \"density\": {\n     \"b\": 0.08558988038961719,\n     \"se\": 0.1700386150566163,\n     \"ci\": [\n      -0.247679681102421,\n      0.41885944188165536\n     ],\n     \"p\": 0.6147143181180363,\n     \"n\": 2719,\n     \"n_concepts\": 342,\n     \"n_concepts_used\": 468,\n     \"sd_within_x\": 0.20568434663219418,\n     \"pct_per_within_sd\": 1.776037115465634\n    },\n    \"OPEN_home\": {\n     \"b\": -0.0253819439388414,\n     \"se\": 0.07889853685095813,\n     \"ci\": [\n      -0.18002023459962563,\n      0.1292563467219428\n     ],\n     \"p\": 0.7476772445651352,\n     \"n\": 2719,\n     \"n_concepts\": 342,\n     \"n_concepts_used\": 468,\n     \"sd_within_x\": 0.41314013441815367,\n     \"pct_per_within_sd\": -1.0431510170155756\n    },\n    \"n_concepts\": 468\n   },\n   \"CS\": {\n    \"density\": {\n     \"b\": -0.3392254369879277,\n     \"se\": 0.1956466881493153,\n     \"ci\": [\n      -0.7226858994551251,\n      0.044235025479269774\n     ],\n     \"p\": 0.08294159292200809,\n     \"n\": 1681,\n     \"n_concepts\": 223,\n     \"n_concepts_used\": 356,\n     \"sd_within_x\": 0.19491023721485098,\n     \"pct_per_within_sd\": -6.398007037107489\n    },\n    \"OPEN_home\": {\n     \"b\": -0.004856733879900239,\n     \"se\": 0.09057067893770575,\n     \"ci\": [\n      -0.182372002653144,\n      0.1726585348933435\n     ],\n     \"p\": 0.9572349829215023,\n     \"n\": 1681,\n     \"n_concepts\": 223,\n     \"n_concepts_used\": 356,\n     \"sd_within_x\": 0.43294624660228354,\n     \"pct_per_within_sd\": -0.21004955691701355\n    },\n    \"n_concepts\": 356\n   },\n   \"Eng\": {\n    \"density\": {\n     \"b\": -0.14685204647836778,\n     \"se\": 0.10012048611471977,\n     \"ci\": [\n      -0.3430845933778611,\n      0.04938050042112557\n     ],\n     \"p\": 0.1424431965983013,\n     \"n\": 8729,\n     \"n_concepts\": 1030,\n     \"n_concepts_used\": 1314,\n     \"sd_within_x\": 0.19985056714634936,\n     \"pct_per_within_sd\": -2.8921980981828743\n    },\n    \"OPEN_home\": {\n     \"b\": 0.045635502806341564,\n     \"se\": 0.052019692661352916,\n     \"ci\": [\n      -0.05632122129675273,\n      0.14759222690943585\n     ],\n     \"p\": 0.3803380505604772,\n     \"n\": 8729,\n     \"n_concepts\": 1030,\n     \"n_concepts_used\": 1314,\n     \"sd_within_x\": 0.4218072795503652,\n     \"pct_per_within_sd\": 1.9435851262560755\n    },\n    \"n_concepts\": 1314\n   },\n   \"Med\": {\n    \"density\": {\n     \"b\": -0.004380677143834574,\n     \"se\": 0.07971632170435301,\n     \"ci\": [\n      -0.16062179666437515,\n      0.15186044237670\ntail: option used in invalid context -- 5\n/bin/bash: line 3: strings: command not found", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] ASSISTANT · 2026-09-29 04:47:28 UTC

```
Experiment 11 has partial results and no worker result file. I'll read the rest of its results and logs to see how far it got.
```

### [14] TOOL CALL — Bash · 2026-09-29 04:47:28 UTC

```
Read Experiment 11 remaining results and logs:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11; python3 -c "
import json;d=json.load(open('results/fe_results.json'));print(list(d.keys()));
for k in d:
  if isinstance(d[k],dict): print(k, list(d[k].keys())[:30])
for s in ['OLD_HELDOUT','COHORT']:
  if s in d:
    x=d[s]; print(s, {k:(x[k].get('b'),x[k].get('ci')) for k in ['H_M1_density','H_M2_open'] if k in x})
"; for f in logs/method.log logs/event_study.log logs/event_study.out logs/partners.log logs/partners.out logs/analysis_fe.log; do echo "== $f"; tail -n 8 $f; done; cat results/deviations.json | head -c 1500; ls ../../gen_plan/ ; grep -l "experiment_11\|experiment_4" -r ../../gen_strat 2>/dev/null | head
```

### [15] TOOL RESULT — Bash · 2026-09-29 04:47:28 UTC

```
{"stdout": "['spec_sha', 'sample_counts', 'DEV']\nsample_counts ['DEV', 'OLD_HELDOUT', 'COHORT']\nDEV ['n_rows', 'n_concepts', 'share_rows_all_zero_concepts', 'mean_y_next', 'share_any_next', 'H_M1_density', 'H_M2_open', 'joint', 'lpm_density', 'lpm_open', 'H_M3_point', 'by_group', 'DL_density', 'DL_OPEN_home', 'bootstrap']\n== logs/method.log\n2026-09-29 03:19:29.332 | INFO     | __main__:provenance:87 - provenance: 24/24 copies identical to source; lexicon sha ok=False\n2026-09-29 03:19:45.240 | INFO     | __main__:provenance:89 - provenance: 24/24 copies identical to source; lexicon sha ok=False\n2026-09-29 03:20:13.336 | INFO     | __main__:provenance:90 - provenance: 24/24 copies identical to source; lexicon sha ok=True\n== logs/event_study.log\n== logs/event_study.out\n    from scipy.linalg import norm\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/.venv/lib/python3.12/site-packages/scipy/linalg/__init__.py\", line 201, in <module>\n    from ._misc import *\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/.venv/lib/python3.12/site-packages/scipy/linalg/_misc.py\", line 3, in <module>\n    from .blas import get_blas_funcs\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/.venv/lib/python3.12/site-packages/scipy/linalg/blas.py\", line 247, in <module>\n    from scipy.linalg import _fblas\nKeyboardInterrupt\n== logs/partners.log\n2026-09-29 03:25:56.401 | INFO     | __main__:build_indicators:116 - partner indicators (12499, 15); bridging papers 59470/930744\n== logs/partners.out\n03:25:56|INFO   |partner indicators (12499, 15); bridging papers 59470/930744\n== logs/analysis_fe.log\n2026-09-29 03:16:03.412 | INFO     | __main__:main:259 - panel (122793, 62); estimation rows 81567\n2026-09-29 03:25:43.390 | INFO     | __main__:body_results:170 - DEV: 35328 rows / 4661 concepts; density b=-0.0701 OPEN b=0.0154 H-M3 diff=0.0027 (576s)\n{\n \"z_constants_own\": \"OPEN_home z constants are frozen on DEV concept-years (features only, pre-seal) instead of Art 1's static EXP5 constants: Art 1 runs in parallel and the yearly components are on a different scale.\",\n \"sa_saturated\": \"Sun-Abraham design is FULLY saturated in cohort x relative time (every e != -1 has its own cohort dummy; only -3..+4 reported) instead of binning e<=-4 and e>=5: in the T0(5) simulation binning biased late lags (err 0.07); saturation recovers ATT within 0.016.\",\n \"placebo_ii_not_run\": \"The within-concept-year field-identity permutation placebo (ii) was not run (time); the event-date permutation placebo (i) was run with 1,000 draws.\",\n \"hm3_ols_both_directions\": \"H-M3 standardised comparison uses FE-OLS in both directions (entries(t+1) on density(t); density(t+1) on entries(t)) so both betas are on the same fully standardised within scale; the PPML forward beta is reported separately (H-M1).\",\n \"at_risk_definition\": \"The exposure control is the number of off-home fields not yet entered by the END of t (predetermined at t, the risk set of the t+1 outcome); the plan's wording 'at_risk(t)' is implemented this way.\",\n \"es_controls\": \"Event-study controls are log1p home works, log1p all works and log at-risk; log degree is omitted because degree is itself shaped by the closure event.\",\n \"nov_res_slices\": \"Yearly nov_res compares community labels within one backbone slice (C0 recomputed per slice from the concept's t0 papers), because Leiden labelgen_plan_evaluation_1\ngen_plan_experiment_1\ngen_plan_experiment_2\ngen_plan_experiment_3\ngen_plan_research_1", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-29 04:47:34 UTC

```
Check iteration 4 plans and Experiment 11 DL results:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4; for d in gen_plan/*; do echo "== $d"; ls $d; find $d -maxdepth 2 -name "*.json" | head -3; done; python3 - <<'E'
import json,glob
for f in glob.glob('gen_plan/*/*.json')[:10]:
    try:
        d=json.load(open(f)); s=json.dumps(d)[:400]; print(f, s)
    except Exception as e: print(f,e)
E
python3 -c "
import json;d=json.load(open('gen_art/gen_art_experiment_11/results/fe_results.json'))['DEV'];print(json.dumps({k:d[k] for k in ['DL_density','DL_OPEN_home']},indent=0)[:1500]); print(json.dumps(d['bootstrap'])[:800])"
```

### [17] TOOL RESULT — Bash · 2026-09-29 04:47:34 UTC

```
{"stdout": "== gen_plan/gen_plan_evaluation_1\ngen_plan/gen_plan_evaluation_1/.terminal_claude_agent_struct_out.json\ngen_plan/gen_plan_evaluation_1/.aii_claude_session.json\ngen_plan/gen_plan_evaluation_1/.aii/module_end.json\n== gen_plan/gen_plan_experiment_1\nREADME.md\ngen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json\ngen_plan/gen_plan_experiment_1/.aii_claude_session.json\ngen_plan/gen_plan_experiment_1/.aii/module_end.json\n== gen_plan/gen_plan_experiment_2\ngen_plan/gen_plan_experiment_2/.terminal_claude_agent_struct_out.json\ngen_plan/gen_plan_experiment_2/.aii_claude_session.json\ngen_plan/gen_plan_experiment_2/.aii/module_end.json\n== gen_plan/gen_plan_experiment_3\nREADME.md\ngen_plan/gen_plan_experiment_3/.terminal_claude_agent_struct_out.json\ngen_plan/gen_plan_experiment_3/.aii_claude_session.json\ngen_plan/gen_plan_experiment_3/.aii/module_end.json\n== gen_plan/gen_plan_research_1\nREADME.md\ngen_plan/gen_plan_research_1/.terminal_claude_agent_struct_out.json\ngen_plan/gen_plan_research_1/.aii_claude_session.json\ngen_plan/gen_plan_research_1/.aii/module_end.json\n{\n\"DL_density\": {\n\"k\": 4,\n\"b\": -0.07457526250297025,\n\"se\": 0.06925316546328256,\n\"ci\": [\n-0.21031146681100407,\n0.06116094180506357\n],\n\"p\": 0.2815473399250814,\n\"tau2\": 0.004906156976220033,\n\"Q\": 3.9944737094319476,\n\"I2\": 0.24896238698072976\n},\n\"DL_OPEN_home\": {\n\"k\": 4,\n\"b\": 0.012377608236350413,\n\"se\": 0.026765285629040514,\n\"ci\": [\n-0.04008235159656899,\n0.06483756806926982\n],\n\"p\": 0.6437585995893068,\n\"tau2\": 0.0,\n\"Q\": 0.6968562593569024,\n\"I2\": 0.0\n}\n}\n{\"n_boot\": 2000, \"n_failed\": 0, \"b_density\": {\"mean\": -0.06762408406565129, \"sd\": 0.05566817638852141, \"ci\": [-0.17636810155135202, 0.03887615286992685], \"p_two_sided_sign\": 0.233, \"n\": 2000}, \"b_open\": {\"mean\": 0.014824469522076434, \"sd\": 0.02697224844607252, \"ci\": [-0.0368086918906705, 0.06706605181854923], \"p_two_sided_sign\": 0.581, \"n\": 2000}, \"std_fwd\": {\"mean\": -0.004651494021434662, \"sd\": 0.005092295150763845, \"ci\": [-0.015028424762096322, 0.0048046170565150875], \"p_two_sided_sign\": 0.382, \"n\": 2000}, \"std_rev\": {\"mean\": 0.0021456630545962775, \"sd\": 0.0055033191697370105, \"ci\": [-0.00824590160636021, 0.013486279811693636], \"p_two_sided_sign\": 0.719, \"n\": 2000}, \"diff\": {\"mean\": 0.0009293341208822413, \"sd\": 0.005526654370436406, \"ci\": [-0.00999901184973672, 0.012417882451345667], \"p_", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] ASSISTANT · 2026-09-29 04:47:42 UTC

```
Experiment 11 ran its DEV body model (both preregistered effects null), then the event study was interrupted and nothing was finalised. Now I'll check Experiment 10's numbers.
```

### [19] TOOL CALL — Bash · 2026-09-29 04:47:42 UTC

```
Read Experiment 10 README and results listing:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cat .aii_worker_result.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('failed'), str(d)[-600:])"; ls results; sed -n 1,200p README.md
```

### [20] TOOL RESULT — Bash · 2026-09-29 04:47:42 UTC

```
{"stdout": "None PEN placebos are null. LLM spend $2.04. Deliverables: results/cohort_report.json, cohort_result.json, exp5_selection_result.json, figures/, full_method_out.json (predict_B5 vs predict_B5_plus_OPEN_home per concept).', 'out_expected_files': {'script': 'method.py', 'full_output': 'full_method_out.json', 'mini_output': 'mini_method_out.json', 'preview_output': 'preview_method_out.json', 'reproducibility': 'reproducibility.md'}, 'upload_ignore_regexes': ['(^|/)\\\\.git/', '(^|/)llm_cache/', '(^|/)passC/', '(^|/)data/ego_open/']}, 'expected_files_valid': True, 'failed': False, 'error_message': None}}\naudit.json\ncohort_report.json\ncohort_result.json\ncoverage_by_year.csv\ndeviations.json\nexp5_selection_result.json\nfrozen_spec.json\nfrozen_spec_v0.json\nlearned_models_cohort.json\nlearned_port_validation.json\nllm_cost_log.csv\nreadme_tables.md\nrederive.json\ns1_candidates_summary.json\ns2_checks.json\ns3_decision.json\ns4_gate_summary.json\ns6_checks.json\ns6_checks_cohort.json\ntype_benchmark_final.json\ntype_benchmark_v1.csv\ntype_benchmark_v1.json\ntype_benchmark_v2.csv\ntype_benchmark_v2.json\ntype_gold_labels_v1.csv\ntype_gold_labels_v2.csv\ntype_gold_sheet_v1.csv\ntype_m2all.json\ntype_prompt_v2.txt\nu2_ego_flags.json\nu5_outcomes.json\nu8_prompt_identity.json\nunit_tests.json\n# Do open-neighbourhood concepts spread? A sealed fresh-cohort test (RQ1)\n\nAI Inventor, invention loop iteration 4, artifact `gen_art_experiment_10` (plan `gen_plan_experiment_1_idx1`).\nThis DEEPENS the EXP8 lead (`iter_3/gen_art/gen_art_experiment_8`): early ego-network \"openness\" of a concept\nanticipates later disciplinary breadth. Here we test it **once**, from a hash-sealed spec, on a **fresh onset cohort\n(2015-2017) that no earlier screen touched**, and we attack the three confounds a reviewer names first: mechanical\ncoupling (off-home papers inside the ego network), concept TYPE (methods travel), and a pre-existing generic footprint.\n\n## Headline\n\n**Verdict (frozen rule, applied in code): CONFIRMED, but marginally, and with no practical gain in prediction.**\n\n* **OPEN_home** is the primary build. It is the mean of six signed, z-scored ego-network components computed from\n  **home-venue papers only**, so off-home spread cannot feed it mechanically. Its partial Spearman with later venue-field\n  breadth (O2r_m50, t0+6..t0+8) is **+0.091 [+0.013, +0.171] at R2** (B5 + onset year + contact reach + type/level) and\n  **+0.080 [+0.001, +0.162] at R3** (+ pre-onset footprint). n = 573 concepts; the resampling unit is the concept;\n  2,000 refit bootstraps.\n* All five pre-registered clauses hold. (1) CI > 0 at R2 and R3. (2) O2r_resid has the same sign (+0.085 [+0.007, +0.165]).\n  (3) Positive in 4 of 5 groups; PHYS is **not estimable** (n = 27 < 30), so this means 4/4 of the estimable groups.\n  (4) Positive within method (+0.074, n = 81) AND within object (+0.093, n = 250) concepts; both CIs include 0, and the\n  clause asks only for the sign. (5) RETENTION_RATIO_early < 0 given R0 (-0.131 [-0.209, -0.056]).\n* **Why the confirmation is fragile:**\n  * the R3 lower bound is +0.001;\n  * the CI includes 0 once venue-label / home-paper coverage (R4: +0.069 [-0.012, +0.150]) and home-group FE\n    (R5: +0.056 [-0.022, +0.135]) are added;\n  * the DerSimonian-Laird pooled estimate across groups is +0.083 [-0.007, +0.173];\n  * Holm over the 8-test family gives p = 0.048 for O2r_m50 and 0.051 for O2r_resid;\n  * the pre-seal power for a true effect of half the EXP5 estimate was only 0.16 (MDE 0.105; within-method MDE 0.31).\n  The cohort point estimate (+0.091) is close to the EXP5 selection estimate (+0.076). The effect transfers in\n  direction and size; the sample is simply small.\n* **Predictive value is negligible.** A frozen OLS on B5 has Spearman 0.768 with O2r_m50; adding OPEN_home gives\n  0.770 (+0.002 [-0.003, +0.008]). OPEN_home is a real but small partial association, not a useful forecaster. The frozen\n  EXP8 ElasticNet on all 58 indicators still beats B5 on the cohort (+0.030 [+0.012, +0.049]), about half its EXP8\n  held-out gain.\n* **Mechanical coupling is real and large.** OPEN_all (all papers) gives +0.174 at R2. ALL minus HOME at R3 is\n  +0.093 [+0.016, +0.169]. The size-matched build, with ALL papers subsampled to the home counts, sits in between\n  (+0.147; SIZEMATCH minus HOME +0.053 [-0.015, +0.117]). Roughly half of the extra ALL-build signal comes from the larger\n  paper count and half from the off-home papers themselves. EXP8's openness signal was therefore inflated by coupling;\n  the uncoupled remainder is about half as large.\n* **Which components carry the home-only signal.** NOV_res (new neighbours outside the expected community,\n  +0.134 [+0.049, +0.215]) and low edge persistence (-0.112 [-0.199, -0.023]). The community count n_comm_W3 and\n  participation, which dominate the ALL build, are null in the HOME build (+0.002, +0.050). The \"many communities\" part\n  of EXP8's story is largely the off-home papers. Within the home venues, what anticipates breadth is\n  *novel, non-persistent* neighbours.\n* **Type and footprint do not absorb OPEN.** R1 to R2 (type) changes +0.097 to +0.091, and R2 to R3 (footprint) changes\n  +0.091 to +0.080. Named reading (a), \"type absorbs OPEN\", is FALSE. Reading (b), \"mechanical\", is also FALSE, since\n  OPEN_home's CI excludes 0 at R2.\n* **Leads replicated (secondary):**\n  * CONTACT_REACH on O2r_m50 given R0: +0.211 [+0.122, +0.294] (EXP8 +0.210), halving to +0.101 without\n    intersection-born concepts (EXP8 +0.111);\n  * n_authors_early on O1c: +0.115 [+0.065, +0.165] (EXP8 +0.161);\n  * RETENTION_RATIO_early < 0 given R0 (EXP8 -0.114), but it vanishes once type and reach enter (R2 -0.043, CI includes 0).\n  * n_authors_early does NOT replicate for O3 (+0.014) or O1b (+0.036).\n\n![ladder](figures/fig_ladder.png)\n\n## Design in one paragraph\n\n**Selection data.** These are the 12,499 EXP5 concepts (onsets 2003-2014). On them we froze:\n* per-build winsor bounds and z constants of the six components;\n* OPEN's definition and signs;\n* the rungs, the verdict rules and the Holm family;\n* the type labels;\n* the frozen B5 prediction models;\n* the power-driven extension decision.\n\nThe spec was hash-chained into `logs/seal.log` (`S0_prereg`, then `S8_freeze`, sha256 `c3389207...`) **before any\ncohort outcome was read**.\n\n**Confirmation data.** One zero-credit pass over the OpenAlex S3 snapshot (2026-09-23, 2,040 files, the same snapshot\nas EXP5/EXP8; `passC.py`) collected 2012-2024 title matches for the 1,535 onset-2015-17 candidates and 300 EXP5\ncontrols. Counts for years >= t0+3 went straight into `data/sealed/parts/`; each part's sha256 is in\n`logs/sealed_files.log`. After the outcome-blind audits (T1-T3 exact; S3 coverage rule keeps TAG grounding), the\nLLM precision gate (94% pass), typing, features and the power rule, the cohort was 1,070 concepts with onsets in 2015-16.\nPower was 0.139 < 0.80, so the declared 2017 extension was added, for n = 1,443 in total (634 with a defined O2r_m50,\n573 of them with a defined OPEN_home). `s9_unseal.py` unsealed the outcome counts **once**\n(`logs/unsealed.json`), computed the outcomes, and scored everything mechanically.\n\n## Results (cohort, 2015-2017 onsets; partial Spearman [95% concept-bootstrap CI], B = 2,000)\n\nRungs:\n* R0 = B5 + onset-year dummies\n* R1 = + CONTACT_REACH\n* R2 = + type dummies, generic flag and legacy-level dummies\n* R3 = + footprint (fp_logN, fp_nfields, fp_reemerge, fp_wiki_pre, newborn)\n* R4 = + venue-label and home-paper coverage\n* R5 = + home-group FE\n\n| build | outcome | R0 | R1 | R2 | R3 | R4 | R5 | n |\n|---|---|---|---|---|---|---|---|---|\n| OPEN_home | O2r_m50 | +0.123 [+0.041, +0.205] | +0.097 [+0.018, +0.179] | +0.091 [+0.013, +0.171] | +0.080 [+0.001, +0.162] | +0.069 [-0.012, +0.150] | +0.056 [-0.022, +0.135] | 573 |\n| OPEN_home | O2r_resid | +0.116 [+0.034, +0.201] | +0.092 [+0.013, +0.176] | +0.085 [+0.007, +0.165] | +0.080 [-0.000, +0.162] | +0.069 [-0.012, +0.151] | +0.056 [-0.024, +0.136] | 573 |\n| OPEN_all | O2r_m50 | +0.205 [+0.125, +0.281] | +0.180 [+0.100, +0.259] | +0.174 [+0.092, +0.253] | +0.171 [+0.088, +0.251] | +0.147 [+0.064, +0.224] | +0.138 [+0.055, +0.218] | 630 |\n| OPEN_all | O2r_resid | +0.194 [+0.113, +0.271] | +0.170 [+0.090, +0.250] | +0.163 [+0.082, +0.242] | +0.168 [+0.086, +0.247] | +0.144 [+0.061, +0.222] | +0.136 [+0.055, +0.216] | 630 |\n| OPEN_sizematch | O2r_m50 | +0.183 [+0.103, +0.257] | +0.154 [+0.074, +0.230] | +0.147 [+0.068, +0.221] | +0.137 [+0.057, +0.212] | +0.124 [+0.045, +0.202] | +0.113 [+0.035, +0.190] | 591 |\n| OPEN_sizematch | O2r_resid | +0.176 [+0.094, +0.250] | +0.148 [+0.068, +0.223] | +0.142 [+0.063, +0.217] | +0.137 [+0.057, +0.211] | +0.124 [+0.045, +0.201] | +0.114 [+0.037, +0.192] | 591 |\n\nEXP5 selection data (2003-14 onsets; not confirmatory), O2r_m50:\n\n| build | R0 | R1 | R2 | R3 | R4 | R5 | n |\n|---|---|---|---|---|---|---|---|\n| OPEN_home | +0.099 [+0.074, +0.123] | +0.081 [+0.056, +0.105] | +0.076 [+0.051, +0.099] | +0.058 [+0.033, +0.081] | +0.057 [+0.031, +0.082] | +0.058 [+0.033, +0.082] | 6565 |\n| OPEN_all | +0.179 [+0.157, +0.203] | +0.151 [+0.129, +0.177] | +0.136 [+0.114, +0.161] | +0.116 [+0.094, +0.141] | +0.103 [+0.080, +0.128] | +0.108 [+0.086, +0.132] | 7186 |\n| OPEN_sizematch | +0.145 [+0.118, +0.169] | +0.118 [+0.094, +0.145] | +0.110 [+0.086, +0.136] | +0.086 [+0.062, +0.111] | +0.084 [+0.059, +0.109] | +0.089 [+0.063, +0.115] | 6727 |\n\n### Per group (R2, O2r_m50) and DerSimonian-Laird pooling\n\n| build | CS+Eng | BGM+Med | PHYS | LIFEENV | SOC | MATHDEC (report only) | DL pooled [95% CI] | I2 | positive / 5 |\n|---|---|---|---|---|---|---|---|---|---|\n| OPEN_home | +0.043 (n=114) | +0.080 (n=277) | NA (n=27) | +0.007 (n=49) | +0.149 (n=96) | NA (n=10) | +0.083 [-0.007, +0.173] | 0.00 | 4 |\n| OPEN_all | +0.094 (n=124) | +0.171 (n=287) | +0.218 (n=32) | +0.261 (n=58) | +0.287 (n=116) | NA (n=13) | +0.189 [+0.104, +0.275] | 0.00 | 5 |\n| OPEN_sizematch | +0.069 (n=120) | +0.132 (n=279) | +0.224 (n=30) | +0.044 (n=49) | +0.290 (n=100) | NA (n=13) | +0.144 [+0.058, +0.230] | 0.00 | 5 |\n\n### Within concept type (R3 without type dummies; method/object = M1 = M2 concepts only)\n\n| build | method | object | property | topic |\n|---|---|---|---|---|\n| OPEN_home | +0.074 [-0.212, +0.314] n=81 | +0.093 [-0.025, +0.204] n=250 | +0.119 [-0.159, +0.370] n=78 | -0.073 [-0.279, +0.135] n=115 |\n| OPEN_all | +0.112 [-0.141, +0.352] n=90 | +0.200 [+0.069, +0.319] n=265 | +0.113 [-0.113, +0.343] n=89 | +0.111 [-0.083, +0.305] n=132 |\n| OPEN_sizematch | +0.200 [-0.056, +0.423] n=85 | +0.148 [+0.029, +0.268] n=253 | +0.150 [-0.127, +0.400] n=85 | +0.025 [-0.203, +0.236] n=118 |\n\n### The six components alone (O2r_m50, R2): cohort vs EXP5 selection\n\n| component (sign) | HOME cohort | HOME EXP5 | ALL cohort | ALL EXP5 |\n|---|---|---|---|---|\n| new_edge_rate (+) | +0.014 [-0.062, +0.090] | +0.039 [+0.014, +0.062] | +0.075 [-0.003, +0.152] | +0.084 [+0.062, +0.109] |\n| n_comm_W3 (+) | +0.002 [-0.071, +0.081] | -0.001 [-0.025, +0.022] | +0.161 [+0.082, +0.238] | +0.133 [+0.110, +0.154] |\n| participation (+) | +0.050 [-0.041, +0.133] | +0.043 [+0.020, +0.071] | +0.145 [+0.068, +0.224] | +0.117 [+0.095, +0.142] |\n| NOV_res (+) | +0.134 [+0.049, +0.215] | +0.057 [+0.033, +0.081] | +0.145 [+0.064, +0.221] | +0.087 [+0.064, +0.113] |\n| ego_density_W3 (-) | +0.018 [-0.075, +0.113] | -0.009 [-0.042, +0.020] | -0.078 [-0.162, -0.002] | -0.070 [-0.091, -0.043] |\n| edge_persistence (-) | -0.112 [-0.199, -0.023] | -0.088 [-0.109, -0.066] | -0.029 [-0.110, +0.047] | -0.041 [-0.065, -0.018] |\n\n### RETENTION_RATIO_early, Holm family, build contrasts\n\n| test | estimate [95% CI] | n |\n|---|---|---|\n| RETENTION_RATIO_early|O2r_m50|R0 | -0.131 [-0.209, -0.056] | 634 |\n| RETENTION_RATIO_early|O2r_m50|R2 | -0.043 [-0.116, +0.031] | 634 |\n| RETENTION_RATIO_early|O2r_m50|R3 | -0.025 [-0.100, +0.049] | 634 |\n| RETENTION_RATIO_early|O2r_resid|R0 | -0.143 [-0.223, -0.069] | 634 |\n| RETENTION_RATIO_early|O2r_resid|R2 | -0.060 [-0.131, +0.015] | 634 |\n| RETENTION_RATIO_early|O2r_resid|R3 | -0.039 [-0.113, +0.034] | 634 |\n| psp difference all_minus_home|R3 (paired) | +0.093 [+0.016, +0.169] | 571 |\n| psp difference sizematch_minus_home|R3 (paired) | +0.053 [-0.015, +0.117] | 563 |\n\n| Holm family member (R2, one-sided bootstrap p) | p | Holm p |\n|---|---|---|\n| OPEN_home|O2r_m50 | 0.0120 | 0.0480 |\n| OPEN_home|O2r_resid | 0.0170 | 0.0510 |\n| OPEN_all|O2r_m50 | 0.0005 | 0.0040 |\n| OPEN_all|O2r_resid | 0.0005 | 0.0040 |\n| OPEN_sizematch|O2r_m50 | 0.0005 | 0.0040 |\n| OPEN_sizematch|O2r_resid | 0.0005 | 0.0040 |\n| RETENTION_RATIO_early|O2r_m50 | 0.1194 | 0.1194 |\n| RETENTION_RATIO_early|O2r_resid | 0.0580 | 0.1159 |\n\n### Sensitivities (declared)\n\n| analysis | estimate [95% CI] | n |\n|---|---|---|\n| OPEN_all_on_home_sample|O2r_m50|R2 | +0.176 [+0.091, +0.263] | 571 |\n| OPEN_home|O2r_m50_le2022_TAG|2015onsets|R2 | +0.055 [-0.070, +0.193] | 221 |\n| OPEN_home|O2r_m50_TAG|R2 | +0.091 [+0.016, +0.171] | 573 |\n| OPEN_home|O2r_m50_MATCH|R2 | +0.122 [+0.058, +0.189] | 927 |\n| OPEN_all|O2r_m50_le2022_TAG|2015onsets|R2 | +0.180 [+0.045, +0.311] | 245 |\n| OPEN_all|O2r_m50_TAG|R2 | +0.174 [+0.092, +0.256] | 630 |\n| OPEN_all|O2r_m50_MATCH|R2 | +0.206 [+0.147, +0.266] | 1073 |\n| OPEN_sizematch|O2r_m50_le2022_TAG|2015onsets|R2 | +0.115 [-0.020, +0.248] | 232 |\n| OPEN_sizematch|O2r_m50_TAG|R2 | +0.147 [+0.070, +0.220] | 591 |\n| OPEN_sizematch|O2r_m50_MATCH|R2 | +0.181 [+0.123, +0.235] | 955 |\n| OPEN_home_min5|O2r_m50|R2 | +0.091 [+0.016, +0.171] | 573 |\n| OPEN_home_min20|O2r_m50|R2 | +0.083 [+0.002, +0.167] | 528 |\n| OPEN_home|O2r_m50|R2|2015_2016_only | +0.130 [+0.037, +0.220] | 414 |\n\n\n![groups](figures/fig_forest_groups.png)\n![components](figures/fig_components.png)\n![type](figures/fig_within_type.png)\n\n### Placebos and audits\n\n* Within-group outcome permutations (200): the 95th percentile of |psp| is 0.081 (pipeline) and 0.075 (independent\n  `audit.py`). The observed value is +0.091.\n* Planted psp = 0.10: the pipeline draw gave +0.047 [-0.045, +0.132], so it was **not** recovered. The independent audit\n  draw gave +0.150 [+0.065, +0.226], which was recovered. With n = 573 the SE is about 0.045, so a single planted draw\n  recovers CI > 0 only about half the time. This matches the pre-seal MDE of 0.105 and is reported as a limit of\n  sensitivity, not hidden.\n* `audit.py` (statsmodels / scipy, independent code):\n  * psp at R2 and R3 re-derived to 1e-16;\n  * the DL pooled estimates re-derived by hand, max |diff| 0;\n  * O2r_m50 re-computed for 30 cohort concepts directly from the sealed parts with `scipy.stats.hypergeom`,\n    max |diff| 2e-11.\n* Unit tests:\n  * U1: the exp_gen_sol_out builder validates;\n  * U2: the six components with n_null = 0 / no betweenness equal EXP8 exactly on 100 concepts, and on all 12,499;\n  * U3: HOME filter, including a synthetic concept whose off-home papers carry the new topics;\n  * U4: SIZEMATCH at full size equals ALL, and draws are seed-deterministic;\n  * U5: outcomes reproduce EXP8 to 1e-15;\n  * U6: psp equals EXP8 rq1stats exactly, and a synthetic planted 0.10 lies inside the CI;\n  * U7: the seal refuses before the freeze, refuses a second unseal, and refuses a changed spec;", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-29 04:47:42 UTC

```
Read rest of Experiment 10 README and cohort report JSON:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; sed -n 200,300p README.md; python3 -c "
import json;d=json.load(open('results/cohort_report.json'));print(json.dumps(d,indent=0)[:3500])"
```

### [22] TOOL RESULT — Bash · 2026-09-29 04:47:42 UTC

````
{"stdout": "  * U7: the seal refuses before the freeze, refuses a second unseal, and refuses a changed spec;\n  * U8: the precision-gate prompt is byte-identical to EXP5 (20/20 EXP5 cache hits).\n* Pre-seal confirmation signals:\n  * the EXP5 R0 signs of all six components match EXP8;\n  * OPEN_home is far less coupled to early off-home share than OPEN_all (Spearman 0.086 vs 0.267);\n  * cohort-vs-EXP5 standardised mean differences are all |SMD| < 0.33.\n\n### Measurement audit (why TAG grounding is still valid in 2021-24)\n\nOpenAlex froze its legacy concept vocabulary, so tagging of new works might have collapsed inside the outcome window.\nIt did not.\n* The share of base works with a legacy tag >= 0.3 in 2021-2024 is 1.01-1.03x its 2017-19 level.\n* The 300 control concepts' TAG / title-match ratio falls only to 0.90-0.96x (minimum 0.902 in 2023). This is just above\n  the declared 0.90 bar, so the outcome-blind rule chose TAG.\n* MATCH (all verified title matches) was validated anyway on the EXP5 frame: Spearman 0.937 with TAG-based O2r_m50.\n  It gives a larger and stronger cohort estimate (+0.122 [+0.058, +0.189], n = 927).\n* Venue-label coverage rises from 0.64 to 0.77 in 2021-24, which is why the coverage rung R4 exists.\n\n![coverage](figures/fig_coverage_audit.png)\n\n## Concept TYPE labels (LLM) and their quality\n\n* M1 = google/gemini-2.5-flash-lite labelled all 14,034 concepts, in 4 classes plus a generic flag.\n* M2 = openai/gpt-4.1-mini labelled a 300-concept benchmark (50 per group); kappa M1-M2 = 0.78 (v1) and 0.79 (v2).\n* 60 benchmark concepts were read blind by the **executor agent (an LLM, not a human annotator)**.\n* The gate (M1 precision >= 0.85 for method AND object) **failed twice**: method 0.73 then 0.80, object 1.00 then 0.87,\n  after the one allowed prompt revision (sharper definitions, 4 few-shot examples outside the benchmark).\n* Declared fallback: type dummies use the M1 v2 labels, and within-type tests use only concepts where M1 = M2. M2 was run\n  on all 9,751 M1 method/object concepts; agreement was 0.90.\n\nDetails are in `results/type_benchmark_final.json`.\n\n## Deviations from the plan (all in `results/deviations.json`)\n\n* **O4 / citations dropped up front.** `referenced_works` was not read, so there is no O4 and the O4-EBM replication\n  is not evaluated.\n* **2017 extension applied.** It was triggered by power 0.139 < 0.80.\n* **Type gate failed twice.** The M1 = M2 fallback was used.\n* **Home rule capped at t0+2.** It counts only years <= t0+2 for cohort concepts, to stay outcome-blind.\n* **13 gate labels retried.** Candidates without a parsable precision-gate label were retried once with smaller\n  batches, instead of EXP5's MiniLM sense-filter fallback.\n* **`s9_unseal.py` edited after the freeze.** The edit came before the unseal and only added a synthetic-data dry run and\n  a resume-from-hashed-outcomes path. Scoring logic is unchanged; see the git history.\n* **Collinear window flag.** `window_flag` (2017 onsets) is collinear with the 2017 onset dummy and is absorbed by it.\n* **Title-match window.** Pass C matched titles only for 2012-2024. The footprint and B5 therefore use EXP5\n  `scan/agg_counts.parquet` (identical counts; T1 exact) for the earlier years.\n\n## Scope limits\n\n* **Selected vocabulary.** The frame is the legacy OpenAlex concept vocabulary. Concepts born in 2015-17 that\n  OpenAlex/MAG had already named are probably the more successful newborns, so the outcome range is restricted.\n* **Range restriction on OPEN_home.** OPEN_home is missing for concepts with fewer than 10 home papers. Excluded concepts\n  are broader: mean off-home share 0.49 vs 0.26, and mean O2r_m50 6.7 vs 4.7.\n* **One period only.** There is a single period-level replication, so cohort and period effects are confounded.\n* **Unpublished taxonomy.** The 4-class type scheme is our own, not a published standard.\n\n## Layout\n\n| path | content |\n|---|---|\n| `prereg.md`, `results/frozen_spec_v0.json` | S0 pre-registration (hash in `logs/seal.log`) |\n| `s0_prereg.py` | writes spec v0 + the S0 seal record |\n| `s1_candidates.py` | S1 outcome-blind cohort candidate frame (`data/cohort_candidates.csv`) + 300 EXP5 controls (`data/controls.csv`) |\n| `passC.py` | S2 zero-credit S3 snapshot pass (`passC/parts/` per file; merged to `data/passC_*`; sealed counts to `data/sealed/parts/`) |\n| `s3_checks.py` | T1-T3 reproduction checks + the S3 outcome-grounding decision (`results/s2_checks.json`, `results/s3_decision.json`, `results/coverage_by_year.csv`) |\n| `s4_gate.py` | S4 EXP5 per-concept LLM precision gate (+ U8 prompt identity, + retry) |\n| `s5_typing.py` | S5 concept TYPE labels, benchmark, blind gold sheet, gate, M2 fallback (`data/concept_types.csv`) |\n| `s6_covariates.py` | S6/S7 footprint, B5, CONTACT_REACH, RETENTION_RATIO_early, n_authors_early, coverage (`data/covariates_*.parquet`) |\n| `s7_ego.py` | S7 six OPEN components under ALL / HOME / SIZEMATCH (+ 'full' EXP8 family-A settings) (`data/ego_open_*.parquet`) |\n| `s8_select.py` | S8 EXP5 selection ladder, coupling, power + extension, cohort feature table, FREEZE (`results/exp5_selection_result.json`, `results/frozen_spec.json`) |\n| `s9_unseal.py` | S9 single unseal, outcomes, frozen scoring, verdict, secondary, placebos (`results/cohort_result.json`) |\n| `s_learned.py` | frozen EXP8 learned models on the cohort (`results/learned_models_cohort.json`) |\n| `audit.py` | independent post-unseal audit (`results/audit.json`) |\n| `make_outputs.py`, `make_report.py`, `readme_tables.py` | figures, `full_method_out.json`, `results/cohort_report.json`, README tables |\n| `method.py` | orchestrator (`--only STEP` / `--from STEP`) |\n| `lib/` | `ladder.py` (OPEN + rungs + psp bootstrap), `outc.py` (outcomes), `seal2.py` (hash-chained seal), `llmc.py` (budgeted OpenRouter client), `featport.py` (EXP5/EXP8 feature ports), `outjson.py`, and copies of EXP8 `common.py`, `ego.py`, `ego_ctx.py`, `rq1stats.py`, `design.py`, `matcher.py`, `rangefile.py`, `common5.py` |\n| `tests/` | U1-U8 (`test_output.py`, `t_ego_flags.py`, `test_units.py`, `t_outcomes.py`) |\n| `inputs/` | frozen lexicon, source-field map, EXP3 topic backbones, field backbone (copied from EXP8) |\n| `data/` | cohort frame, Pass C merged outputs, covariates, ego builds, types, `features_cohort.parquet` (frozen), `outcomes_cohort.parquet` (post-unseal), `analysis_cohort.parquet` |\n| `data/sealed/parts/` | **kept**: the sealed outcome-window counts (hashes in `logs/sealed_files.log`) |\n| `results/cohort_report.json` | **headline deliverable**: verdict, clause table, all estimates with CI / n / unit, power, audits, type benchmark, LLM spend |\n| `full_method_out.json` (+ `mini_`, `preview_`) | exp_gen_sol_out: one example per cohort concept; output = O2r_m50; `predict_B5` vs `predict_B5_plus_OPEN_home` (frozen, EXP5-fitted) |\n| `figures/` | `fig_ladder`, `fig_forest_groups`, `fig_components`, `fig_within_type`, `fig_coverage_audit` (PNG + PDF) |\n| `logs/seal.log`, `logs/unsealed.json`, `logs/sealed_files.log` | seal evidence |\n| `rederive.py`, `results/rederive.json` | short independent re-derivation of the headline numbers + placebos |\n| `llm_cache/` | **kept**: every LLM response (lets a re-run reproduce the labels at $0) |\n\n## How to run\n\n```bash\n./restore.sh                                   # .venv with pinned versions (uv)\n.venv/bin/python method.py                     # full pipeline; or --only <step>; see method.py for the order\n```\n\nThe pipeline reads the sibling run artifacts (EXP5 `iter_2/gen_art/gen_art_experiment_5`, EXP8\n`iter_3/gen_art/gen_art_experiment_8`, art_33 `iter_1/gen_art/gen_art_experiment_4`, dataset\n`iter_2/gen_art/gen_art_dataset_2`) through `RUN_ROOT` in `lib/common.py` (env `AII_RUN_ROOT`). The OpenAlex snapshot\nis read from the public S3 bucket; no API key is needed and 0 OpenAlex credits were used. LLM calls go through OpenRouter\n(`OPENROUTER_BASE_URL`, `OPENROUTER_API_KEY`); the total spend was **$2.04**. A re-run with `llm_cache/` in place costs $0.\nThe single unseal cannot be repeated (`logs/unsealed.json`). `s9_unseal.py` resumes scoring from the hashed\n`data/outcomes_cohort.parquet`.\n{\n\"question\": \"Does an open early ego-neighbourhood (OPEN, t0..t0+2) anticipate later disciplinary breadth (O2r_m50, t0+6..t0+8) beyond size/growth/breadth, concept type, pre-onset footprint, coverage and field, on a fresh 2015-2017 onset cohort scored once from a sealed spec?\",\n\"verdict\": {\n\"verdict\": \"CONFIRMED\",\n\"clauses\": {\n\"1_open_home_R2_R3_ci_gt0\": true,\n\"2_o2r_resid_same_sign_R2\": true,\n\"3_positive_in_ge4_of_5_groups_R2\": true,\n\"4_within_method_and_object_gt0\": true,\n\"5_retention_ratio_lt0_R0\": true\n},\n\"failing_clauses\": [],\n\"named_readings\": {\n\"a_type_absorbs_OPEN\": false,\n\"b_mechanical\": false\n}\n},\n\"headline\": {\n\"OPEN_home|O2r_m50|R2\": {\n\"n\": 573,\n\"rho\": 0.0905904928497304,\n\"ci\": [\n0.013236035063533528,\n0.17104659543493156\n],\n\"se\": 0.04106142983555049,\n\"p_one\": 0.01199400299850075,\n\"p_two\": 0.028608810613794024,\n\"x\": \"OPEN_home\",\n\"y\": \"O2r_m50\",\n\"rung\": \"R2\",\n\"resampling_unit\": \"concept\",\n\"n_boot\": 2000\n},\n\"OPEN_home|O2r_m50|R3\": {\n\"n\": 573,\n\"rho\": 0.08044570966976407,\n\"ci\": [\n0.0005254040720849043,\n0.16173726767650506\n],\n\"se\": 0.04234173064177449,\n\"p_one\": 0.02498750624687656,\n\"p_two\": 0.05907505884124973,\n\"x\": \"OPEN_home\",\n\"y\": \"O2r_m50\",\n\"rung\": \"R3\",\n\"resampling_unit\": \"concept\",\n\"n_boot\": 2000\n},\n\"OPEN_home|O2r_resid|R2\": {\n\"n\": 573,\n\"rho\": 0.08481845531723738,\n\"ci\": [\n0.006979234290649221,\n0.16543587030004958\n],\n\"se\": 0.041433713080277684,\n\"p_one\": 0.01699150424787606,\n\"p_two\": 0.042125012015258735,\n\"x\": \"OPEN_home\",\n\"y\": \"O2r_resid\",\n\"rung\": \"R2\",\n\"resampling_unit\": \"concept\",\n\"n_boot\": 2000\n},\n\"OPEN_all|O2r_m50|R2\": {\n\"n\": 630,\n\"rho\": 0.17410165420736987,\n\"ci\": [\n0.0923126541384861,\n0.2534029984102734\n],\n\"se\": 0.040991291672706036,\n\"p_one\": 0.0004997501249375312,\n\"p_two\": 3.244314879802875e-05,\n\"x\": \"OPEN_all\",\n\"y\": \"O2r_m50\",\n\"rung\": \"R2\",\n\"resampling_unit\": \"concept\",\n\"n_boot\": 2000\n},\n\"OPEN_sizematch|O2r_m50|R2\": {\n\"n\": 591,\n\"rho\": 0.14732472326582408,\n\"ci\": [\n0.06830518865958383,\n0.22107327021148623\n],\n\"se\": 0.039532963543139676,\n\"p_one\": 0.0004997501249375312,\n\"p_two\": 0.000244891541507214,\n\"x\": \"OPEN_sizematch\",\n\"y\": \"O2r_m50\",\n\"rung\": \"R2\",\n\"resampling_unit\": \"concept\",\n\"n_boot\": 2000\n}\n},\n\"n_cohort\": 1443,\n\"n_by_t0\": {\n\"2015\": 570,\n\"2016\": 500,\n\"2017\": 373\n},\n\"outcome_availability\": {\n\"O2r_m50\": 634,\n\"O2r_resid\": 634,\n\"O1c\": 1443\n},\n\"resampling_unit\": \"concept\",\n\"bootstrap_B\": 2000,\n\"power_pre_seal\": {\n\"base_2015_2016\": {\n\"power_ci_gt0\": 0.139,\n\"n_expected\": 547,\n\"MDE_2.8SE_analytic\": 0.1227881227029841,\n\"within_type\": {\n\"method\": {\n\"n_expected\": 80,\n\"MDE_2.8SE\": 0.38460957905632925\n},\n\"object\": {\n\"n_expected\": 278,\n\"MDE_2.8SE\": 0.17673443286738488\n}\n}\n},\n\"with_2017\": {\n\"power_ci_gt0\": 0.159,\n\"n_expected\": 736,\n\"MDE_2.8SE_analytic\": 0.10515620726641516,\n\"within_type\": {\n\"method\": {\n\"n_expected\": 110,\n\"MDE_2.8SE\": 0.30733992797113296\n},\n\"object\": {\n\"n_expected\": 379,\n\"MDE_2.8SE\": 0.14924050144892728\n}\n}\n},\n\"extension_applied\": true\n},\n\"primary_ladder\": {\n\"OPEN_home|O2r_m50|R0\": {\n\"n\": 573,\n\"rho\": 0.12258114548096312,\n\"ci\": [\n0.04136619666988465,\n0.2050352453223211\n],\n\"se\": 0.042564293101143104,\n\"p_one\": 0.0024987506246876563,\n\"p_two\": 0.004463482229769635,\n\"x\": \"OPEN_home\",\n\"y\": \"O2r_m50\",\n\"rung\": \"R0\",\n\"resampling_unit\": \"concept\",\n\"n_boot\": 2000\n},\n\"OPEN_home|O2r_m50|R1\": {\n\"n\": 573,\n\"rho\": 0.09743550387304983,\n\"ci\": [\n0.017845655014202207,\n0.17851159055785454\n],\n\"se\": 0.0415694633424532,\n\"p_one\": 0.0074962518740629685,\n\"p_two\": 0.020174719505782417,\n\"x\": \"OPEN_home\",\n\"y\": \"O2r_m50\",\n\"rung\": \"R1\",\n\"resampling_", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [23] THINKING · 2026-09-29 04:47:56 UTC

```
I've noticed Experiment 10's README and the report interpret the ALL-minus-HOME gap in opposite ways. Next I'll check the cohort learned-model numbers and the Experiment 12 results.
```

### [24] TOOL CALL — Bash · 2026-09-29 04:47:56 UTC

```
Read Experiment 10 cohort learned-model results:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; python3 -c "
import json;d=json.load(open('results/learned_models_cohort.json'));print(json.dumps(d,indent=0)[:2500])"
```

### [25] TOOL RESULT — Bash · 2026-09-29 04:47:56 UTC

```
{"stdout": "{\n\"fully_imputed_features\": [],\n\"O2r_m50\": {\n\"n\": 634,\n\"metric\": \"Spearman\",\n\"B5\": 0.7886706783489855,\n\"linear_all\": 0.8184766169203301,\n\"diff\": 0.029805938571344615,\n\"diff_ci\": [\n0.011907416076822424,\n0.04884917468852921\n],\n\"imputed_coef_mass\": 0.0,\n\"evaluable\": true,\n\"note\": \"\"\n},\n\"O2r_resid\": {\n\"n\": 634,\n\"metric\": \"Spearman\",\n\"B5\": 0.7887242142370855,\n\"linear_all\": 0.815964257404026,\n\"diff\": 0.02724004316694051,\n\"diff_ci\": [\n0.008507660163781048,\n0.04600356683296491\n],\n\"imputed_coef_mass\": 0.0,\n\"evaluable\": true,\n\"note\": \"\"\n},\n\"O3\": {\n\"n\": 1443,\n\"metric\": \"AUC\",\n\"B5\": 0.5612224573633761,\n\"linear_all\": 0.5400099589194572,\n\"diff\": -0.021212498443918815,\n\"diff_ci\": [\n-0.12957036185118126,\n0.1005112372626442\n],\n\"imputed_coef_mass\": 0.0,\n\"evaluable\": true,\n\"note\": \"\"\n},\n\"O4_EBM\": \"not evaluable: O4 not computed (no citation pass; declared drop)\"\n}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] TOOL CALL — Bash · 2026-09-29 04:47:56 UTC

```
Read Experiment 12 README and results listing:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; ls results case_studies ai_atlas | head -60; sed -n 1,140p README.md
```

### [27] TOOL RESULT — Bash · 2026-09-29 04:47:56 UTC

```
{"stdout": "ai_atlas:\natlas.json\nego_W3_grid.pdf\nego_W3_grid.png\nsmall_multiples.pdf\nsmall_multiples.png\ntable.csv\n\ncase_studies:\npair01_CSEng\npair02_BGMMed\npair03_PHYS\npair04_SOC\npair05_CSEng\npair06_BGMMed\npair07_SOC\n\nresults:\nT7_rederivation.json\naudit_headlines.json\ncase_pairs.json\ndecomposition_dev.json\ndecomposition_heldout.json\ndeviations.json\nfield_communities.json\nfrozen_spec.json\nopen_diagnostics.json\npipeline_counts.json\npreregistration_R2.json\nsequence_light_dev.json\nsequence_light_heldout.json\nstates_verification.json\nt2_ego_open_reproduction.json\nt2_o2r_crosscheck.json\nt4_open_timing.json\ntrajectories_dev.json\ntrajectories_heldout.json\ntransitions_dev.json\ntransitions_heldout.json\ntypology_dev_assign.parquet\ntypology_heldout_assign.parquet\nunit_tests_T0.json\n# How concepts spread: contact versus keeping (RQ2 trajectories, cache-only re-run)\n\nAI Inventor, invention loop iteration 4, artifact `gen_art_experiment_12` (plan `gen_plan_experiment_3_idx3`, RQ2).\nIt re-runs the failed iteration-3 RQ2 artifact (gen_art_experiment_9, never executed). Every input is a cached\narray from EXP5, EXP6, EXP7 or EXP8 of this run. It makes **0 OpenAlex calls, no S3 reads and no LLM calls**; a network\nguard in `lib/common.py` makes any HTTP or S3 client import fail.\n\n> **Disclosure (second use of the frame).** EXP5, EXP7 and EXP8 already unsealed the held-out outcomes. This\n> artifact's seal (`results/frozen_spec.json`, sha256 in `logs/seal.log`) guarantees only one thing: every analysis\n> choice here (OPEN formula, z constants, typology variables, k, HMM states, PCA loadings, decomposition variants,\n> pre-registered text, case and atlas rules) was fixed on DEV before this artifact read held-out states or outcomes.\n> The held-out and cohort results are therefore **within-frame robustness checks, not confirmation**. Fresh\n> confirmation (the 2015-16 cohort) belongs to another artifact.\n\n## The question and the design\n\nDo concepts that end up spread across many fields get there because they **reach** more fields early (contact and\nexploration), or because they **keep** the fields they touch (retention)? And does the \"openness\" of a concept's\nearly topic neighbourhood line up with how it later spreads?\n\nThe frame is the 12,499 EXP5 concepts (onset t0 in 2003-2014). DEV has 4,771 concepts (CS, Eng, BGM, Med homes).\nThe held-out groups are PHYS 742, LIFEENV 1,113, SOC 1,352 and MATHDEC 165. The 2010-14 cohort has 4,356 concepts:\n2,484 with DEV homes and 1,872 with other homes. Fields are the 26 OpenAlex venue fields. Field states follow the\nEXP6/EXP7 D3 semantics:\n\n- *entered*: cumulative grounded papers >= 2;\n- *retained*: entered at least 2 years earlier and >= 2 papers in the last 3 years, off-home;\n- *lost*: entered, but 0 papers in 3 years.\n\n| stage | script | what it does |\n|---|---|---|\n| S0 | `s0_skeleton.py` | writes and validates the `method_out.json` skeleton FIRST (EXP9 died on output format); records sha256 provenance of the copied library code |\n| S1-S2 | `s2_open.py` | join; **OPEN** openness score in three builds: ALL-PAPERS (EXP8 ego features), HOME-ONLY (home-venue papers only), SIZE-MATCHED (20 year-stratified subsamples of all papers down to the home-only count) |\n| S3 | `s3_states.py` | D3 state sequences, ages 0..10, for all 12,499 concepts; verified cell by cell against the EXP7 state panel; per-age summaries |\n| S4 | `s4_decomp.py` | exact decomposition **log Bn = log E2 + log M + log rho** of the top-vs-bottom O2r_resid tercile gap, with pre-registered verdicts |\n| S5 | `s5_typology.py` | DTW k-medoids + Gaussian HMM typology under a strict naming rule, else a **PCA continuum**; OPEN on the axis |\n| S6 | `s6_sequence.py` | light ordering test: home-prominence half-peak vs off-home take-off, with a mechanical-lag permutation null; intersection-born vs single-home |\n| S7 | `s7_seal.py` | freeze -> T6 checklist -> unseal once -> held-out and cohort runs of S4-S6 |\n| S8 | `s8_cases.py` | 7 most-similar case pairs (matched on volume and growth, opposite OPEN; outcome shown after selection) |\n| S9 | `s9_atlas.py` | retrospective AI/CS atlas (37 concepts, 5 outcome types; outcome-selected by design) |\n| S10 | `s10_outputs.py` | `pipeline_counts.json`, `method_out.json`, summary figures |\n| T7 | `rederive.py` | independent pandas re-derivation of the held-out shares and the OPEN~PC1 Spearman |\n\nThe decomposition terms, per concept at horizon H = 8:\n\n- E2 = off-home fields entered by age 2 (early **contact**);\n- M = EH / E2 = frontier advance from age 2 to 8;\n- rho = Bn / EH = share of entered fields still retained at age 8 (**retention**);\n- Bn = retained off-home fields at t0+8.\n\nAt group level, mean Bn = mean E2 x (sum EH / sum E2) x (sum Bn / sum EH) holds exactly. The log ratio of each\nfactor (top vs bottom tercile) is its exact, unique Shapley share of the gap. The primary variant averages this\nwithin early-volume quintiles, weighted by n. **These shares are an accounting identity for the breadth outcome, not\ncausal effects**: Bn at t0+8 is built from the same papers as O2r, and only E2 is early.\n\n## Results\n\n### 1. Breadth gaps are mostly early contact; retention is the smaller part (PR1 and PR1b SUPPORTED everywhere)\n\nVolume-stratified decomposition of the top-vs-bottom O2r_resid tercile gap. D_k = log(top/bottom); shares sum to 1;\n95% CIs from 2,000 concept bootstraps (terciles and quintiles recomputed in each resample).\n\n| sample | n | D_E2 (contact) | D_M (frontier) | D_rho (retention) | s_E2 / s_M / s_rho | s_explore - s_ret [95% CI] |\n|---|---|---|---|---|---|---|\n| DEV, all homes (primary ii) | 3,188 | 1.050 | -0.062 | 0.393 | 0.76 / -0.05 / 0.29 | 0.431 [0.371, 0.493] |\n| DEV, Medicine excluded (**PR1 variant iv**) | 1,469 | 0.866 | 0.032 | 0.202 | 0.79 / 0.03 / 0.18 | **0.633 [0.537, 0.727]** |\n| Held-out pooled (PHYS/LIFEENV/SOC/MATHDEC), iv | 1,825 | 0.759 | 0.013 | 0.263 | 0.73 / 0.01 / 0.25 | **0.492 [0.403, 0.575]** |\n| Cohort 2010-14 pooled, iv | 1,403 | 0.724 | 0.033 | 0.291 | 0.69 / 0.03 / 0.28 | **0.445 [0.358, 0.527]** |\n| DL over held-out groups (PHYS, LIFEENV, SOC) | 3 groups | 0.772 | 0.005 | 0.246 | - | 0.504 [0.329, 0.679], I2 = 0.76 |\n\n- PR1 is **SUPPORTED** on DEV, in every held-out group and in both cohort parts: PHYS 0.33, LIFEENV 0.55, SOC 0.62,\n  MATHDEC 0.41, COH_DEVHOME 0.39, COH_OTHER 0.49, all with CI > 0 (`figures/fig_forest_explore_vs_retention.png`).\n  s_ret < 0.5 in all of them.\n- PR1b (contact alone beats retention) is **SUPPORTED**: DEV 0.604 [0.508, 0.698], held-out pooled 0.480\n  [0.394, 0.570], cohort 0.414 [0.324, 0.494]. Holm p < 0.001 in family R2-A.\n- **Frontier advance M carries almost nothing** (|D_M| <= 0.16 in every variant). Integrating concepts do not\n  enter proportionally more *new* fields after age 2; the gap is set by contact already made by t0+2, plus\n  somewhat better retention.\n- **PR3 (descriptive):** D_rho is **positive** everywhere (DEV 0.20 [0.14, 0.27]; held-out 0.26; cohort 0.29).\n  Integrating concepts keep a *larger* share of the fields they enter, so retention helps rather than hurts.\n  Retention is simply the smaller of the two contributions.\n- **Robust to**:\n  - min_n = 3 or 5. At min_n = 5, D_rho on the held-out pool shrinks to 0.07 [-0.001, 0.16], so the retention part\n    is the one that is sensitive to the threshold.\n  - O2r_m50 instead of O2r_resid;\n  - only sustained concepts (O1b = 1);\n  - onset-restricted counts (pre-t0 papers removed; s_E2 = 0.86 on DEV);\n  - excluding the 658 EXP6-overlap concepts;\n  - additive Das Gupta decomposition (DEV shares 0.77 / -0.05 / 0.28, summing exactly to the gap);\n  - concept-level covariance decomposition of var(log Bn) (DEV 0.59 / 0.03 / 0.38; held-out 0.56 / 0.01 / 0.44).\n    At the concept level retention matters more than at the group level.\n- **Medicine**: including Medicine homes raises the retention share (DEV Med group s_rho = 0.34 vs 0.07-0.21 for\n  CS/Eng/BGM), which is why PR1 is judged with Medicine excluded.\n- **Checks**:\n  - T5: a second bootstrap seed moves CI ends by <= 0.004.\n  - T9 placebo: with O2r_resid shuffled within group, D_k centres near 0 (Medicine-excluded D_total 0.04\n    [-0.02, 0.11] vs observed 1.10). With all homes, a within-group shuffle leaves D_total 0.15 [0.10, 0.20]\n    because group composition differs; the observed 1.38 is far outside that.\n  - Shares are unstable under the null by construction (D_total ~ 0), so the D_k are the quantities to read.\n\nSource: `results/decomposition_dev.json`, `results/decomposition_heldout.json`, `results/T7_rederivation.json`,\n`figures/fig_decomposition_waterfall.png`, `figures/fig_forest_explore_vs_retention.png`.\n\n### 2. PR2 (\"localised concepts keep more early\") is NOT supported as stated; only its partial clause holds\n\n- The raw clause fails. The mean early retention ratio (t0..t0+2) of the bottom O2r_resid tercile minus the top\n  tercile is:\n  - DEV: -0.110 [-0.132, -0.086] (**REVERSED**: bottom 0.166 vs top 0.275);\n  - held-out pooled: +0.011 [-0.019, 0.039] (NOT SUPPORTED);\n  - cohort: -0.058 [-0.083, -0.031] (REVERSED).\n- The partial clause holds everywhere. The partial Spearman of RETENTION_RATIO_early with O2r_resid given B5 is\n  negative: DEV -0.169 [-0.202, -0.134], held-out -0.129 [-0.175, -0.086], cohort -0.173 [-0.212, -0.133].\n  This replicates EXP8's -0.120 on the same frame and is not new evidence.\n- Read together: *at equal early size and breadth*, concepts that keep a higher share of their early contacts end up\n  narrower. Without that adjustment, integrating concepts keep more.\n- Verdict per the frozen rule: PR2 = REVERSED on DEV, NOT SUPPORTED on held-out, REVERSED on the cohort.\n\nSource: `results/decomposition_*.json` (keys `early_ratio_PR2`, `verdicts`).\n\n### 3. No trajectory typology survives the naming rule; the result is a continuum\n\n- DTW k-medoids on 9 yearly variables x ages 0..8 (4,771 DEV concepts) chose k = 4. It was the only k with median\n  80%-subsample ARI >= 0.6 (0.87), but its silhouette is only 0.13; the gap statistic points to k = 8.\n- The Gaussian HMM partition (BIC chose S = 5, the top of the tested range 3-5) agrees poorly: **ARI(DTW, HMM) =\n  0.22 < 0.5**.\n- Hennig bootstrap Jaccard: 0.69, 0.81, 0.82, 0.73.\n- Re-clustering without Medicine gives ARI 0.46 < 0.5.\n- Held-out re-clustering vs nearest-DEV-medoid assignment gives ARI 0.44 (held-out) and 0.38 (cohort), both < 0.5.\n- The classes are not volume classes (ARI with volume tercile 0.02). They are Medicine-skewed: 849 of the 1,080\n  concepts in class 1 are Medicine homes.\n- **No class is named. The pre-registered CONTINUUM is reported**, and the EXP6 two-class typology stays NOT\n  ESTABLISHED (ARI of our classes vs EXP6's on 122 overlapping concepts: 0.20).\n- PCA of the same DEV trajectories (`figures/fig_pca_loadings.png`):\n  - **PC1 (38.8%)** is a *breadth-of-spread* axis: fields entered, fields retained, field entropy and community\n    span load positively at every age; home share loads negatively.\n  - **PC2 (10.7%)** is a *keep-versus-lose* axis: retention share positive, fields lost and fields entered negative.\n  - PC1 correlates only weakly with early volume (Spearman 0.15).\n  - The bottom PC1 tercile is 76% Medicine-home concepts; the top tercile is 33%.\n\nSource: `results/trajectories_dev.json`, `results/trajectories_heldout.json`, `figures/fig_dtw_hmm_agreement.png`.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [28] TOOL CALL — Bash · 2026-09-29 04:48:06 UTC

```
Read rest of Experiment 12 README:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; sed -n 140,320p README.md
```

### [29] TOOL RESULT — Bash · 2026-09-29 04:48:06 UTC

````
{"stdout": "Source: `results/trajectories_dev.json`, `results/trajectories_heldout.json`, `figures/fig_dtw_hmm_agreement.png`.\n\n### 4. Early openness goes with breadth of spread, not with keeping\n\nSpearman of OPEN with PC1. \"Partial\" = given B5 and label coverage. 95% concept-bootstrap CIs; held-out pooled with\nDerSimonian-Laird over the 4 held-out groups.\n\n| OPEN build | DEV rho | DEV partial | held-out DL rho (I2) | held-out DL partial (I2) | cohort partial |\n|---|---|---|---|---|---|\n| ALL-PAPERS | 0.352 [0.325, 0.376] | 0.174 [0.146, 0.202] | 0.432 [0.312, 0.552] (0.94) | 0.120 [0.085, 0.155] (0.00) | 0.117 [0.087, 0.147] |\n| HOME-ONLY | 0.174 [0.145, 0.202] | 0.117 [0.085, 0.146] | 0.212 [0.089, 0.335] (0.90) | 0.060 [0.023, 0.097] (0.00) | 0.121 [0.088, 0.153] |\n| SIZE-MATCHED | 0.091 [0.063, 0.120] | 0.135 [0.107, 0.163] | 0.208 [0.005, 0.411] (0.97) | 0.094 [0.060, 0.129] (0.00) | 0.089 [0.058, 0.119] |\n\n- The raw association is partly mechanical. The all-papers ego network gains off-home topics exactly as the concept\n  spreads, which is why the HOME-ONLY and SIZE-MATCHED builds exist. Even so, a **positive partial association\n  survives in all three builds and in every split**, and is homogeneous across held-out groups (I2 = 0 for the\n  partials). It is small: 0.06-0.17.\n- A within-group shuffle of OPEN gives null bands that cover 0 (T9).\n- OPEN is **not** positively related to PC2, the keeping axis: DEV partial -0.07 to -0.11; held-out -0.04 to +0.01.\n- Coverage of OPEN_home is 84.7%. Between-build Spearman correlations are 0.57 (all vs home) and 0.73 (all vs\n  size). Source: `results/open_diagnostics.json`.\n\nSource: `results/trajectories_*.json` (keys `open_on_axis*`, `DL_heldout_groups_PC1`, `T9_*`),\n`figures/fig_open_vs_pc1_hexbin.png`.\n\n### 5. Ordering (light test): no signal beyond the mechanical lag\n\n- Home-prominence half-peak before off-home take-off (A < T) occurs in 25.6% of DEV concepts, against 26.4% under a\n  1,000-permutation mechanical-lag null. The excess is:\n  - DEV: -0.009 [-0.015, -0.003];\n  - held-out: +0.011 [0.005, 0.016];\n  - cohort: -0.017 [-0.023, -0.012].\n- The frozen rule's verdict words are MIXED (DEV), HOME-FIRST (held-out) and MIXED (cohort). But the effect is about\n  1 percentage point and flips sign, so **no ordering claim is made**.\n- Intersection-born concepts (two home fields) take off off-home *later*: cloglog hazard ratio 0.47 [0.42, 0.54] on\n  DEV, 0.45 held-out, 0.41 cohort (`figures/fig_km_takeoff.png`). This is largely mechanical, because a second\n  home absorbs fields that would otherwise count as off-home.\n\nSource: `results/sequence_light_*.json`.\n\n### 6. Case pairs and AI atlas (illustration, not inference)\n\n- **Seven most-similar pairs**, matched within reporting group on z(log volume) and z(growth) <= 0.25 and onset\n  +/- 2 years, with opposite OPEN_all quintiles (`case_studies/pair*/`, `figures/fig_case_pairs.png`):\n  - Graphics processing unit / Vertical axis wind turbine;\n  - Shotgun proteomics / Image-guided radiation therapy;\n  - Nanocarriers / Nanosheet;\n  - Soft power / Autonomous learning;\n  - Scopus / Oxygen reduction reaction;\n  - Sclerostin / IgG4-related disease;\n  - User-generated content / Mindfulness-based cognitive therapy.\n- The pairs cover CS+Eng, BGM+Med, PHYS and SOC. LIFEENV and MATHDEC had no valid match.\n- In **7 of 7** pairs the high-OPEN member has the higher O2r_resid. This is descriptive (n = 7, no p-value), and\n  O2r was not used in selection.\n- The OPEN_home order agrees with OPEN_all in all 7 pairs.\n- Each pair directory holds:\n  - `flow_raster.png`: state ribbons plus the field x age raster, ordered by backbone community;\n  - `ego_snapshots.png`: W1-W3 topic ego networks, plus W3 home-only;\n  - `pair.json`: B5, OPEN components in 3 builds, E2/M/rho, PC1, outcomes, and recognition events with lag to t0.\n- **AI/CS atlas** (`ai_atlas/`; RETROSPECTIVE and OUTCOME-SELECTED BY DESIGN): 37 CS-home concepts. RAPID,\n  GRADUAL, DIFFUSING and TRANSIENT have 8 each; LOCAL has only 5 eligible. AI-share tiers are relaxed per type and\n  recorded.\n- By the frozen written rule, these measures \"looked meaningful\" (DIFFUSING vs LOCAL >= 0.5 pooled SD at age 2, with\n  the same sign as the frame-wide DEV correlation): early volume, field entropy, fields entered and retained,\n  community span, frontier, ego-network communities, participation, ego density (negative), and OPEN_all and\n  OPEN_home.\n- Topic-level structure exists only for t0-3..t0+2 (a data limit of EXP8 Pass A), so the atlas cannot show\n  topic-neighbour change after t0+2.\n\n## Verification\n\n- **T0 unit tests** (`tests/test_units.py` -> `results/unit_tests_T0.json`): all pass.\n  - hand-built D3 states;\n  - decomposition identity (error < 1e-15);\n  - planted contact-only and retention-only gaps (shares ~1 / ~0);\n  - planted 3-regime typology (DTW and HMM ARI = 1.0, choose_k = 3); pure noise fails the naming rule;\n  - numba DTW equals tslearn;\n  - OPEN formula;\n  - seal refusals;\n  - generic filter.\n- **T2 reproduction**:\n  - `lib/ego_open.py` reproduces EXP8 ego features exactly on 300 concepts (max |diff| = 0;\n    `results/t2_ego_open_reproduction.json`);\n  - the rebuilt D3 states equal the EXP7 state panel on all 5,557,942 cells of its 11,841 concepts (0 mismatches;\n    the 658 missing concepts are exactly the EXP6 overlap);\n  - RETENTION_RATIO_early and CONTACT_REACH are re-derived exactly;\n  - O2r_m50 in EXP8 vs EXP5: rho = 1.0 (`results/states_verification.json`, `results/t2_o2r_crosscheck.json`).\n- **T6**: pre-unseal checklist passed (`logs/T6_preunseal_checklist.json`).\n- **T7**: independent re-derivation matches the pipeline to 6e-17 (shares) and 1e-16 (Spearman).\n- **Headline audit** (`audit_headlines.py` -> `results/audit_headlines.json`):\n  - separate code re-derives, from the raw per-concept files, PR1 on DEV, held-out and cohort, the PR2 partial\n    Spearman, the three OPEN~PC1 partials and ARI(DTW, HMM), all to <= 6e-17;\n  - every test fails on shuffled input: PR1 CIs span about -12..40 with the outcome shuffled; the PR2 partial is 0.02\n    [-0.02, 0.05] with the ratio shuffled; the OPEN partials under full permutation are about 0 [-0.03, 0.03]. The\n    observed 0.12-0.17 lie above the range of 100 within-group shuffles (max 0.046).\n- `method_out.json` was validated against `exp_gen_sol_out` after every stage (`logs/validate.log`).\n\n## Deviations\n\nAll are listed in `results/deviations.json`, each with its effect on the claims. The main ones:\n\n- The plan's \"O1c = 1\" is implemented as O1b = 1, because O1c is continuous in EXP8.\n- DTW uses a numba kernel identical to tslearn (tslearn projected 61 min).\n- fasterpam is single-threaded per job.\n- No git commit at the seal (the workspace is not a repository); the sha256 seal and one-time unseal marker are used\n  instead.\n- The atlas relaxes AI share per type.\n- `in_exp6` is taken from EXP7's overlap report.\n- The HMM uses min_covar = 1e-3.\n- T3 was not run as a separate smoke test.\n- Code was edited after the seal: a merge fix, figure layout, and the atlas AI-share relaxation changed from global\n  to per type after the per-type counts were visible. None of these edits touches a frozen analysis rule.\n\n## Layout\n\n| path | content |\n|---|---|\n| `s0_skeleton.py` ... `s10_outputs.py`, `rederive.py` | pipeline stages (see the table above) |\n| `lib/` | `common.py` (paths, seal-aware outcome loader, validation), `ego_open.py` (trimmed EXP8 ego code), `decomp.py`, `typology.py`, `cases_spec.py` (frozen case and atlas rules), `viz.py`; copied verbatim with sha256 in `logs/provenance.json`: `ego.py`, `ego_ctx.py` (path patch in `logs/ego_ctx_patch.diff`), `d3.py`, `rq1stats.py`, `traj_exp6.py`, `lib_outcomes.py`, `common_exp8.py`, `seal_exp8.py`, `build_features_exp8.py` |\n| `method.py` | driver running every stage in order (`python method.py [--from STAGE]`) |\n| `audit_headlines.py` | independent re-derivation of the headline numbers from raw files + placebo checks -> `results/audit_headlines.json` |\n| `reproducibility.md` | exact environment, inputs (env vars per artifact id), commands, runtimes and expected numbers |\n| `tests/test_units.py` | T0 unit tests |\n| `method_out.json` (+ `full_`, `mini_`, `preview_`) | exp_gen_sol_out: dataset `rq2_concepts` (12,499 concepts; predict_open_axis = PC1, predict_decomposition = log factors) and `case_pairs` (7); metadata = headline results |\n| `open_features.parquet` | OPEN components and scores in 3 builds, coverage, n_home |\n| `panel.parquet` | per concept x age (0..10) summaries: contact, retention, frontier, entropy, home share, home prominence, community span, ... |\n| `state_sequences.parquet` | per concept x age x field D3 state (0 untouched, 1 entered, 2 retained, 3 lost, 4 home, -1 after 2022) |\n| `data/` | joined frame, decomposition inputs (min_n 2/3/5, onset-restricted), state codes, OPEN parts, frozen typology objects |\n| `results/` | every JSON result, `frozen_spec.json`, `preregistration_R2.json`, `pipeline_counts.json` (every count read from files, for the methodology figure), `deviations.json` |\n| `figures/` | decomposition waterfall, forest plot, PCA loadings, DTW-HMM agreement, OPEN-vs-PC1 hexbin, KM take-off, case-pair overview (PNG + PDF) |\n| `case_studies/pairNN_*/` | per-pair figures and `pair.json` |\n| `ai_atlas/` | `small_multiples.png`, `ego_W3_grid.png`, `table.csv`, `atlas.json` |\n| `logs/` | stage logs, `seal.log`, `unsealed.json`, `validate.log`, provenance |\n\nAll of these are small and stay in the published repository. Nothing trained or irreproducible exceeds 100 MB.\n\n## How to run\n\n```bash\nuv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml\nexport AII_RUN_ROOT=<path to the run root holding 3_invention_loop/>   # defaults to four levels above this folder\n.venv/bin/python s0_skeleton.py\n.venv/bin/python s2_open.py --stage all --workers 24\n.venv/bin/python s3_states.py\n.venv/bin/python s4_decomp.py --scope dev\n.venv/bin/python s5_typology.py --scope dev --workers 24\n.venv/bin/python s6_sequence.py --scope dev\n.venv/bin/python s7_seal.py --freeze      # freeze + checklist + ONE-TIME unseal (refuses a second time)\n.venv/bin/python s7_seal.py --run         # held-out/cohort S4-S6\n.venv/bin/python s8_cases.py && .venv/bin/python s9_atlas.py\n.venv/bin/python s10_outputs.py && .venv/bin/python rederive.py\n.venv/bin/python tests/test_units.py\n```\n\nTotal wall time on 24 workers is about 45 min, most of it the HMM restarts. The inputs are the cached EXP5, EXP6,\nEXP7 and EXP8 artifacts of the same run, read-only.\n\n## Restoring removed files\n\nTwo paths are marked `delete` in `.aii/manifest.yaml`; both can be rebuilt:\n\n- `.venv/` (the Python environment):\n  `uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml` (or `bash restore.sh`).\n- `dtw_cache/` (DTW distance matrices, 408 MB, stored as row-chunk parts `D_<split>_part_NNN.npy` of <= 80 MB each, read back by `lib/typology.load_matrix_parts`):\n  `.venv/bin/python s5_typology.py --scope dev && .venv/bin/python s5_typology.py --scope heldout`.\n  The held-out call needs the existing unseal marker `logs/unsealed.json`; it recomputes and re-caches the matrices,\n  and the results are deterministic given the seeds.\n- `__pycache__/` directories (not shipped) are regenerated automatically by Python.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [30] TOOL CALL — Bash · 2026-09-29 04:48:06 UTC

```
Extract decomposition shares and preregistration text for Exp12:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; python3 - <<'E'
import json
d=json.load(open('results/decomposition_dev.json'))
def walk(x,p='',depth=0):
    if depth>3: return
    if isinstance(x,dict):
        for k,v in x.items():
            if isinstance(v,(int,float)) and any(s in k for s in ['s_','diff','share']): print(p+'.'+k, v)
            elif isinstance(v,list) and len(v)==2 and all(isinstance(t,(int,float)) for t in v) and any(s in k for s in ['s_','diff','ci']): print(p+'.'+k, v)
            else: walk(v,p+'.'+k,depth+1)
walk(d)
E
python3 -c "
import json;d=json.load(open('results/preregistration_R2.json'));print(json.dumps(d,indent=0)[:2500])"
```

### [31] TOOL RESULT — Bash · 2026-09-29 04:48:06 UTC

```
{"stdout": ".n_concepts_with_outcome 3188\n.variants.i_pooled.point.s_E2 0.7785985240775642\n.variants.i_pooled.point.s_M -0.04648969378092406\n.variants.i_pooled.point.s_rho 0.2678911697033599\n.variants.i_pooled.point.s_explore 0.7321088302966402\n.variants.i_pooled.point.s_contact 0.7785985240775642\n.variants.i_pooled.point.s_ret 0.2678911697033599\n.variants.i_pooled.point.diff_explore_ret 0.4642176605932803\n.variants.i_pooled.point.diff_contact_ret 0.5107073543742043\n.variants.i_pooled.ci.s_E2 [0.7377220010123606, 0.818427146694098]\n.variants.i_pooled.ci.s_M [-0.07442239269999372, -0.016695960246980848]\n.variants.i_pooled.ci.s_rho [0.23607427884025467, 0.29658072257640555]\n.variants.i_pooled.ci.s_explore [0.7034192774235946, 0.7639257211597452]\n.variants.i_pooled.ci.s_contact [0.7377220010123606, 0.818427146694098]\n.variants.i_pooled.ci.s_ret [0.23607427884025467, 0.29658072257640555]\n.variants.i_pooled.ci.diff_explore_ret [0.40683855484718895, 0.5278514423194905]\n.variants.i_pooled.ci.diff_contact_ret [0.4469340578901103, 0.5765540199886888]\n.variants.i_pooled.se.s_E2 0.020338861389451703\n.variants.i_pooled.se.s_M 0.014465510969440801\n.variants.i_pooled.se.s_rho 0.014987552948362537\n.variants.i_pooled.se.s_explore 0.014987552948362537\n.variants.i_pooled.se.s_contact 0.020338861389451703\n.variants.i_pooled.se.s_ret 0.014987552948362537\n.variants.i_pooled.se.diff_explore_ret 0.029975105896725075\n.variants.i_pooled.se.diff_contact_ret 0.03267018586405023\n.variants.i_pooled.p_two_sided.s_E2 0.0\n.variants.i_pooled.p_two_sided.s_M 0.002\n.variants.i_pooled.p_two_sided.s_rho 0.0\n.variants.i_pooled.p_two_sided.s_explore 0.0\n.variants.i_pooled.p_two_sided.s_contact 0.0\n.variants.i_pooled.p_two_sided.s_ret 0.0\n.variants.i_pooled.p_two_sided.diff_explore_ret 0.0\n.variants.i_pooled.p_two_sided.diff_contact_ret 0.0\n.variants.i_pooled.boot_nan_share 0.0\n.variants.ii_vol_PRIMARY.point.s_E2 0.7601342271482046\n.variants.ii_vol_PRIMARY.point.s_M -0.044767852858144275\n.variants.ii_vol_PRIMARY.point.s_rho 0.2846336257099397\n.variants.ii_vol_PRIMARY.point.s_explore 0.7153663742900602\n.variants.ii_vol_PRIMARY.point.s_contact 0.7601342271482046\n.variants.ii_vol_PRIMARY.point.s_ret 0.2846336257099397\n.variants.ii_vol_PRIMARY.point.diff_explore_ret 0.4307327485801205\n.variants.ii_vol_PRIMARY.point.diff_contact_ret 0.47550060143826484\n.variants.ii_vol_PRIMARY.ci.s_E2 [0.7242853268154643, 0.7986654579729577]\n.variants.ii_vol_PRIMARY.ci.s_M [-0.0713033148978912, -0.018301046784255887]\n.variants.ii_vol_PRIMARY.ci.s_rho [0.25327223086883677, 0.3144843950418541]\n.variants.ii_vol_PRIMARY.ci.s_explore [0.6855156049581458, 0.7467277691311631]\n.variants.ii_vol_PRIMARY.ci.s_contact [0.7242853268154643, 0.7986654579729577]\n.variants.ii_vol_PRIMARY.ci.s_ret [0.25327223086883677, 0.3144843950418541]\n.variants.ii_vol_PRIMARY.ci.diff_explore_ret [0.3710312099162917, 0.4934555382623264]\n.variants.ii_vol_PRIMARY.ci.diff_contact_ret [0.41585853501232495, 0.538955157822526]\n.variants.ii_vol_PRIMARY.se.s_E2 0.018953499125749715\n.variants.ii_vol_PRIMARY.se.s_M 0.013778428662125622\n.variants.ii_vol_PRIMARY.se.s_rho 0.015377994287512348\n.variants.ii_vol_PRIMARY.se.s_explore 0.015377994287512345\n.variants.ii_vol_PRIMARY.se.s_contact 0.018953499125749715\n.variants.ii_vol_PRIMARY.se.s_ret 0.015377994287512348\n.variants.ii_vol_PRIMARY.se.diff_explore_ret 0.030755988575024693\n.variants.ii_vol_PRIMARY.se.diff_contact_ret 0.03164791586243603\n.variants.ii_vol_PRIMARY.p_two_sided.s_E2 0.0\n.variants.ii_vol_PRIMARY.p_two_sided.s_M 0.003\n.variants.ii_vol_PRIMARY.p_two_sided.s_rho 0.0\n.variants.ii_vol_PRIMARY.p_two_sided.s_explore 0.0\n.variants.ii_vol_PRIMARY.p_two_sided.s_contact 0.0\n.variants.ii_vol_PRIMARY.p_two_sided.s_ret 0.0\n.variants.ii_vol_PRIMARY.p_two_sided.diff_explore_ret 0.0\n.variants.ii_vol_PRIMARY.p_two_sided.diff_contact_ret 0.0\n.variants.ii_vol_PRIMARY.boot_nan_share 0.0\n.variants.iii_vol_med_adjusted.point.s_E2 0.747208781880521\n.variants.iii_vol_med_adjusted.point.s_M -0.024420175915455845\n.variants.iii_vol_med_adjusted.point.s_rho 0.27721139403493483\n.variants.iii_vol_med_adjusted.point.s_explore 0.7227886059650651\n.variants.iii_vol_med_adjusted.point.s_contact 0.747208781880521\n.variants.iii_vol_med_adjusted.point.s_ret 0.27721139403493483\n.variants.iii_vol_med_adjusted.point.diff_explore_ret 0.4455772119301303\n.variants.iii_vol_med_adjusted.point.diff_contact_ret 0.46999738784558615\n.variants.iii_vol_med_adjusted.ci.s_E2 [0.7075824409320085, 0.7889095218943905]\n.variants.iii_vol_med_adjusted.ci.s_M [-0.0538518291587952, 0.004536193061780432]\n.variants.iii_vol_med_adjusted.ci.s_rho [0.2455217188338048, 0.3085348680586151]\n.variants.iii_vol_med_adjusted.ci.s_explore [0.6914651319413849, 0.7544782811661952]\n.variants.iii_vol_med_adjusted.ci.s_contact [0.7075824409320085, 0.7889095218943905]\n.variants.iii_vol_med_adjusted.ci.s_ret [0.2455217188338048, 0.3085348680586151]\n.variants.iii_vol_med_adjusted.ci.diff_explore_ret [0.38293026388276985, 0.5089565623323905]\n.variants.iii_vol_med_adjusted.ci.diff_contact_ret [0.40390096187844765, 0.5378878150667656]\n.variants.iii_vol_med_adjusted.se.s_E2 0.020738880563424825\n.variants.iii_vol_med_adjusted.se.s_M 0.0146515319304245\n.variants.iii_vol_med_adjusted.se.s_rho 0.016759477746097283\n.variants.iii_vol_med_adjusted.se.s_explore 0.016759477746097286\n.variants.iii_vol_med_adjusted.se.s_contact 0.020738880563424825\n.variants.iii_vol_med_adjusted.se.s_ret 0.016759477746097283\n.variants.iii_vol_med_adjusted.se.diff_explore_ret 0.033518955492194566\n.variants.iii_vol_med_adjusted.se.diff_contact_ret 0.03474615280550657\n.variants.iii_vol_med_adjusted.p_two_sided.s_E2 0.0\n.variants.iii_vol_med_adjusted.p_two_sided.s_M 0.092\n.variants.iii_vol_med_adjusted.p_two_sided.s_rho 0.0\n.variants.iii_vol_med_adjusted.p_two_sided.s_explore 0.0\n.variants.iii_vol_med_adjusted.p_two_sided.s_contact 0.0\n.variants.iii_vol_med_adjusted.p_two_sided.s_ret 0.0\n.variants.iii_vol_med_adjusted.p_two_sided.diff_explore_ret 0.0\n.variants.iii_vol_med_adjusted.p_two_sided.diff_contact_ret 0.0\n.variants.iii_vol_med_adjusted.boot_nan_share 0.0\n.variants.iv_vol_noMed_PR1.point.s_E2 0.787632631546018\n.variants.iv_vol_noMed_PR1.point.s_M 0.028694245127769424\n.variants.iv_vol_noMed_PR1.point.s_rho 0.18367312332621255\n.variants.iv_vol_noMed_PR1.point.s_explore 0.8163268766737874\n.variants.iv_vol_noMed_PR1.point.s_contact 0.787632631546018\n.variants.iv_vol_noMed_PR1.point.s_ret 0.18367312332621255\n.variants.iv_vol_noMed_PR1.point.diff_explore_ret 0.6326537533475749\n.variants.iv_vol_noMed_PR1.point.diff_contact_ret 0.6039595082198055\n.variants.iv_vol_noMed_PR1.ci.s_E2 [0.7306821891076823, 0.8410251691113064]\n.variants.iv_vol_noMed_PR1.ci.s_M [-0.012614294225798859, 0.07020319827558459]\n.variants.iv_vol_noMed_PR1.ci.s_rho [0.1362907910498397, 0.23153258391949647]\n.variants.iv_vol_noMed_PR1.ci.s_explore [0.7684674160805034, 0.8637092089501603]\n.variants.iv_vol_noMed_PR1.ci.s_contact [0.7306821891076823, 0.8410251691113064]\n.variants.iv_vol_noMed_PR1.ci.s_ret [0.1362907910498397, 0.23153258391949647]\n.variants.iv_vol_noMed_PR1.ci.diff_explore_ret [0.536934832161007, 0.7274184179003206]\n.variants.iv_vol_noMed_PR1.ci.diff_contact_ret [0.5076530678734679, 0.6983250662229235]\n.variants.iv_vol_noMed_PR1.se.s_E2 0.028272288473065916\n.variants.iv_vol_noMed_PR1.se.s_M 0.02133688941703711\n.variants.iv_vol_noMed_PR1.se.s_rho 0.024311030696847494\n.variants.iv_vol_noMed_PR1.se.s_explore 0.024311030696847497\n.variants.iv_vol_noMed_PR1.se.s_contact 0.028272288473065916\n.variants.iv_vol_noMed_PR1.se.s_ret 0.024311030696847494\n.variants.iv_vol_noMed_PR1.se.diff_explore_ret 0.04862206139369499\n.variants.iv_vol_noMed_PR1.se.diff_contact_ret 0.04822275570827288\n.variants.iv_vol_noMed_PR1.p_two_sided.s_E2 0.0\n.variants.iv_vol_noMed_PR1.p_two_sided.s_M 0.164\n.variants.iv_vol_noMed_PR1.p_two_sided.s_rho 0.0\n.variants.iv_vol_noMed_PR1.p_two_sided.s_explore 0.0\n.variants.iv_vol_noMed_PR1.p_two_sided.s_contact 0.0\n.variants.iv_vol_noMed_PR1.p_two_sided.s_ret 0.0\n.variants.iv_vol_noMed_PR1.p_two_sided.diff_explore_ret 0.0\n.variants.iv_vol_noMed_PR1.p_two_sided.diff_contact_ret 0.0\n.variants.iv_vol_noMed_PR1.boot_nan_share 0.0\n.variants.v_minn3.point.s_E2 0.8057658541704315\n.variants.v_minn3.point.s_M -0.08106853641996256\n.variants.v_minn3.point.s_rho 0.27530268224953114\n.variants.v_minn3.point.s_explore 0.7246973177504689\n.variants.v_minn3.point.s_contact 0.8057658541704315\n.variants.v_minn3.point.s_ret 0.27530268224953114\n.variants.v_minn3.point.diff_explore_ret 0.4493946355009377\n.variants.v_minn3.point.diff_contact_ret 0.5304631719209003\n.variants.v_minn3.ci.s_E2 [0.7629676270278876, 0.8501372970223371]\n.variants.v_minn3.ci.s_M [-0.11198433512323461, -0.05090051555532081]\n.variants.v_minn3.ci.s_rho [0.24037576661290777, 0.3101461361926345]\n.variants.v_minn3.ci.s_explore [0.6898538638073655, 0.7596242333870923]\n.variants.v_minn3.ci.s_contact [0.7629676270278876, 0.8501372970223371]\n.variants.v_minn3.ci.s_ret [0.24037576661290777, 0.3101461361926345]\n.variants.v_minn3.ci.diff_explore_ret [0.379707727614731, 0.5192484667741845]\n.variants.v_minn3.ci.diff_contact_ret [0.460352539005597, 0.6030597172255778]\n.variants.v_minn3.se.s_E2 0.02210463966154049\n.variants.v_minn3.se.s_M 0.015519017876063487\n.variants.v_minn3.se.s_rho 0.017472771849520487\n.variants.v_minn3.se.s_explore 0.017472771849520483\n.variants.v_minn3.se.s_contact 0.02210463966154049\n.variants.v_minn3.se.s_ret 0.017472771849520487\n.variants.v_minn3.se.diff_explore_ret 0.03494554369904097\n.variants.v_minn3.se.diff_contact_ret 0.03670130495644959\n.variants.v_minn3.p_two_sided.s_E2 0.0\n.variants.v_minn3.p_two_sided.s_M 0.0\n.variants.v_minn3.p_two_sided.s_rho 0.0\n.variants.v_minn3.p_two_sided.s_explore 0.0\n.variants.v_minn3.p_two_sided.s_contact 0.0\n.variants.v_minn3.p_two_sided.s_ret 0.0\n.variants.v_minn3.p_two_sided.diff_explore_ret 0.0\n.variants.v_minn3.p_two_sided.diff_contact_ret 0.0\n.variants.v_minn3.boot_nan_share 0.0\n.variants.v_minn5.point.s_E2 0.8206493926456864\n.variants.v_minn5.point.s_M -0.06931225302701047\n.variants.v_minn5.point.s_rho 0.24866286038132396\n.variants.v_minn5.point.s_explore 0.7513371396186759\n.variants.v_minn5.point.s_contact 0.8206493926456864\n.variants.v_minn5.point.s_ret 0.24866286038132396\n.variants.v_minn5.point.diff_explore_ret 0.502674279237352\n.variants.v_minn5.point.diff_contact_ret 0.5719865322643625\n.variants.v_minn5.ci.s_E2 [0.7692729805566314, 0.8733986170135577]\n.variants.v_minn5.ci.s_M [-0.10511604741923096, -0.02896312058992148]\n.variants.v_minn5.ci.s_rho [0.2030070113112655, 0.28999933117968374]\n.variants.v_minn5.ci.s_explore [0.7100006688203161, 0.7969929886887345]\n.variants.v_minn5.ci.s_contact [0.7692729805566314, 0.8733986170135577]\n.variants.v_minn5.ci.s_ret [0.2030070113112655, 0.28999933117968374]\n.variants.v_minn5.ci.diff_explore_ret [0.4200013376406324, 0.5939859773774688]\n.variants.v_minn5.ci.diff_contact_ret [0.4869742071115511, 0.6629484083955571]\n.variants.v_minn5.se.s_E2 0.026049769916206417\n.variants.v_minn5.se.s_M 0.018965860043630534\n.variants.v_minn5.se.s_rho 0.02219255932222488\n.variants.v_minn5.se.s_explore 0.02219255932222488\n.variants.v_minn5.se.s_contact 0.026049769916206417\n.variants.v_minn5.se.s_ret 0.02219255932222488\n.variants.v_minn5.se.diff_explore_ret 0.04438511864444976\n.variants.v_minn5.se.diff_contact_ret 0.044525235055201506\n.variants.v_minn5.p_two_sided.s_E2 0.0\n.variants.v_minn5.p_two_sided.s_M 0.0\n.variants.v_minn5.p_two_sided.s_rho 0.0\n.variants.v_minn5.p_two_sided.s_explore 0.0\n.variants.v_minn5.p_two_sided.s_contact 0.0\n.variants.v_minn5.p_two_sided.s_ret 0.0\n.variants.v_minn5.p_two_sided.diff_explore_ret 0.0\n.variants.v_minn5.p_two_sided.diff_contact_ret 0.0\n.variants.v_minn5.boot_nan_share 0.0\n.variants.v_minn3_noMed.point.s_E2 0.7856051860841123\n.variants.v_minn3_noMed.point.s_M 0.041984103090821595\n.variants.v_minn3_noMed.point.s_rho 0.17241071082506593\n.variants.v_minn3_noMed.point.s_explore 0.8275892891749339\n.variants.v_minn3_noMed.point.s_contact 0.7856051860841123\n.variants.v_minn3_noMed.point.s_ret 0.17241071082506593\n.variants.v_minn3_noMed.point.diff_explore_ret 0.655178578349868\n.variants.v_minn3_noMed.point.diff_contact_ret 0.6131944752590464\n.variants.v_minn3_noMed.ci.s_E2 [0.7193897045097026, 0.847522000176399]\n.variants.v_minn3_noMed.ci.s_M [-0.0013412414016709632, 0.0939958725454747]\n.variants.v_minn3_noMed.ci.s_rho [0.11247161661724242, 0.22958281825852966]\n.variants.v_minn3_noMed.ci.s_explore [0.7704171817414702, 0.8875283833827575]\n.variants.v_minn3_noMed.ci.s_contact [0.7193897045097026, 0.847522000176399]\n.variants.v_minn3_noMed.ci.s_ret [0.11247161661724242, 0.22958281825852966]\n.variants.v_minn3_noMed.ci.diff_explore_ret [0.5408343634829406, 0.775056766765515]\n.variants.v_minn3_noMed.ci.diff_contact_ret [0.5001715051847063, 0.7232220300762896]\n.variants.v_minn3_noMed.se.s_E2 0.03269622243186447\n.variants.v_minn3_noMed.se.s_M 0.024559378335881007\n.variants.v_minn3_noMed.se.s_rho 0.0292666274198789\n.variants.v_minn3_noMed.se.s_explore 0.029266627419878895\n.variants.v_minn3_noMed.se.s_contact 0.03269622243186447\n.variants.v_minn3_noMed.se.s_ret 0.0292666274198789\n.variants.v_minn3_noMed.se.diff_explore_ret 0.05853325483975779\n.variants.v_minn3_noMed.se.diff_contact_ret 0.05699117317138671\n.variants.v_minn3_noMed.p_two_sided.s_E2 0.0\n.variants.v_minn3_noMed.p_two_sided.s_M 0.06\n.variants.v_minn3_noMed.p_two_sided.s_rho 0.0\n.variants.v_minn3_noMed.p_two_sided.s_explore 0.0\n.variants.v_minn3_noMed.p_two_sided.s_contact 0.0\n.variants.v_minn3_noMed.p_two_sided.s_ret 0.0\n.variants.v_minn3_noMed.p_two_sided.diff_explore_ret 0.0\n.variants.v_minn3_noMed.p_two_sided.diff_contact_ret 0.0\n.variants.v_minn3_noMed.boot_nan_share 0.0\n.variants.v_minn5_noMed.point.s_E2 0.8227946203167877\n.variants.v_minn5_noMed.point.s_M 0.03734940485057297\n.variants.v_minn5_noMed.point.s_rho 0.13985597483263915\n.variants.v_minn5_noMed.point.s_explore 0.8601440251673607\n.variants.v_minn5_noMed.point.s_contact 0.8227946203167877\n.variants.v_minn5_noMed.point.s_ret 0.13985597483263915\n.variants.v_minn5_noMed.point.diff_explore_ret 0.7202880503347215\n.variants.v_minn5_noMed.point.diff_contact_ret 0.6829386454841486\n.variants.v_minn5_noMed.ci.s_E2 [0.7437702796699694, 0.8938241176286191]\n.variants.v_minn5_noMed.ci.s_M [-0.019776111618069924, 0.09980554612697823]\n.variants.v_minn5_noMed.ci.s_rho [0.07141910118643703, 0.21579124837266306]\n.variants.v_minn5_noMed.ci.s_explore [0.7842087516273369, 0.9285808988135629]\n.variants.v_minn5_noMed.ci.s_contact [0.7437702796699694, 0.8938241176286191]\n.variants.v_minn5_noMed.ci.s_ret [0.07141910118643703, 0.21579124837266306]\n.variants.v_minn5_noMed.ci.diff_explore_ret [0.5684175032546738, 0.8571617976271257]\n.variants.v_minn5_noMed.ci.diff_contact_ret [0.5412510782246159, 0.805525655314453]\n.variants.v_minn5_noMed.se.s_E2 0.03865219890616621\n.variants.v_minn5_noMed.se.s_M 0.02999736827295863\n.variants.v_minn5_noMed.se.s_rho 0.03655906999666085\n.variants.v_minn5_noMed.se.s_explore 0.03655906999666085\n.variants.v_minn5_noMed.se.s_contact 0.03865219890616621\n.variants.v_minn5_noMed.se.s_ret 0.03655906999666085\n.variants.v_minn5_noMed.se.diff_explore_ret 0.0731181399933217\n.variants.v_minn5_noMed.se.diff_contact_ret 0.06900198587940541\n.variants.v_minn5_noMed.p_two_sided.s_E2 0.0\n.variants.v_minn5_noMed.p_two_sided.s_M 0.186\n.variants.v_minn5_noMed.p_two_sided.s_rho 0.001\n.variants.v_minn5_noMed.p_two_sided.s_explore 0.0\n.variants.v_minn5_noMed.p_two_sided.s_contact 0.0\n.variants.v_minn5_noMed.p_two_sided.s_ret 0.001\n.variants.v_minn5_noMed.p_two_sided.diff_explore_ret 0.0\n.variants.v_minn5_noMed.p_two_sided.diff_contact_ret 0.0\n.variants.v_minn5_noMed.boot_nan_share 0.0\n.variants.vi_O2r_m50.point.s_E2 0.7572341697752052\n.variants.vi_O2r_m50.point.s_M -0.044085048744083505\n.variants.vi_O2r_m50.point.s_rho 0.28685087896887834\n.variants.vi_O2r_m50.point.s_explore 0.7131491210311217\n.variants.vi_O2r_m50.point.s_contact 0.7572341697752052\n.variants.vi_O2r_m50.point.s_ret 0.28685087896887834\n.variants.vi_O2r_m50.point.diff_explore_ret 0.42629824206224337\n.variants.vi_O2r_m50.point.diff_contact_ret 0.47038329080632685\n.variants.vi_O2r_m50.ci.s_E2 [0.7212413890292343, 0.7963451948087247]\n.variants.vi_O2r_m50.ci.s_M [-0.07067438624811152, -0.015793201128397612]\n.variants.vi_O2r_m50.ci.s_rho [0.2562052853506159, 0.31337498926906404]\n.variants.vi_O2r_m50.ci.s_explore [0.6866250107309358, 0.7437947146493841]\n.variants.vi_O2r_m50.ci.s_contact [0.7212413890292343, 0.7963451948087247]\n.variants.vi_O2r_m50.ci.s_ret [0.2562052853506159, 0.31337498926906404]\n.variants.vi_O2r_m50.ci.diff_explore_ret [0.37325002146187175, 0.4875894292987682]\n.variants.vi_O2r_m50.ci.diff_contact_ret [0.41212138709546836, 0.5347911579777643]\n.variants.vi_O2r_m50.se.s_E2 0.018703057187208088\n.variants.vi_O2r_m50.se.s_M 0.014092686377219896\n.variants.vi_O2r_m50.se.s_rho 0.014672676362202855\n.variants.vi_O2r_m50.se.s_explore 0.014672676362202857\n.variants.vi_O2r_m50.se.s_contact 0.018703057187208088\n.variants.vi_O2r_m50.se.s_ret 0.014672676362202855\n.variants.vi_O2r_m50.se.diff_explore_ret 0.02934535272440571\n.variants.vi_O2r_m50.se.diff_contact_ret 0.030521791399411108\n.variants.vi_O2r_m50.p_two_sided.s_E2 0.0\n.variants.vi_O2r_m50.p_two_sided.s_M 0.002\n.variants.vi_O2r_m50.p_two_sided.s_rho 0.0\n.variants.vi_O2r_m50.p_two_sided.s_explore 0.0\n.variants.vi_O2r_m50.p_two_sided.s_contact 0.0\n.variants.vi_O2r_m50.p_two_sided.s_ret 0.0\n.variants.vi_O2r_m50.p_two_sided.diff_explore_ret 0.0\n.variants.vi_O2r_m50.p_two_sided.diff_contact_ret 0.0\n.variants.vi_O2r_m50.boot_nan_share 0.0\n.variants.vi_O1b_sustained_only.point.s_E2 0.7851327063895319\n.variants.vi_O1b_sustained_only.point.s_M -0.06889798915125417\n.variants.vi_O1b_sustained_only.point.s_rho 0.28376528276172214\n.variants.vi_O1b_sustained_only.point.s_explore 0.7162347172382777\n.variants.vi_O1b_sustained_only.point.s_contact 0.7851327063895319\n.variants.vi_O1b_sustained_only.point.s_ret 0.28376528276172214\n.variants.vi_O1b_sustained_only.point.diff_explore_ret 0.43246943447655556\n.variants.vi_O1b_sustained_only.point.diff_contact_ret 0.5013674236278098\n.variants.vi_O1b_sustained_only.ci.s_E2 [0.7365053977475765, 0.8335972263605542]\n.variants.vi_O1b_sustained_only.ci.s_M [-0.10602519736240716, -0.035009048363221246]\n.variants.vi_O1b_sustained_only.ci.s_rho [0.24933816688330074, 0.3216405973904143]\n.variants.vi_O1b_sustained_only.ci.s_explore [0.6783594026095857, 0.7506618331166993]\n.variants.vi_O1b_sustained_only.ci.s_contact [0.7365053977475765, 0.8335972263605542]\n.variants.vi_O1b_sustained_only.ci.s_ret [0.24933816688330074, 0.3216405973904143]\n.variants.vi_O1b_sustained_only.ci.diff_explore_ret [0.3567188052191714, 0.5013236662333985]\n.variants.vi_O1b_sustained_only.ci.diff_contact_ret [0.4201747244740812, 0.5749783427029399]\n.variants.vi_O1b_sustained_only.se.s_E2 0.024999260281294816\n.variants.vi_O1b_sustained_only.se.s_M 0.01807562761028723\n.variants.vi_O1b_sustained_only.se.s_rho 0.018871548600107528\n.variants.vi_O1b_sustained_only.se.s_explore 0.018871548600107528\n.variants.vi_O1b_sustained_only.se.s_contact 0.024999260281294816\n.variants.vi_O1b_sustained_only.se.s_ret 0.018871548600107528\n.variants.vi_O1b_sustained_only.se.diff_explore_ret 0.037743097200215056\n.variants.vi_O1b_sustained_only.se.diff_contact_ret 0.0404409249257545\n.variants.vi_O1b_sustained_only.p_two_sided.s_E2 0.0\n.variants.vi_O1b_sustained_only.p_two_sided.s_M 0.0\n.variants.vi_O1b_sustained_only.p_two_sided.s_rho 0.0\n.variants.vi_O1b_sustained_only.p_two_sided.s_explore 0.0\n.variants.vi_O1b_sustained_only.p_two_sided.s_contact 0.0\n.variants.vi_O1b_sustained_only.p_two_sided.s_ret 0.0\n.variants.vi_O1b_sustained_only.p_two_sided.diff_explore_ret 0.0\n.variants.vi_O1b_sustained_only.p_two_sided.diff_contact_ret 0.0\n.variants.vi_O1b_sustained_only.boot_nan_share 0.0\n.variants.viii_onset_restricted.point.s_E2 0.8585678011462191\n.variants.viii_onset_restricted.point.s_M -0.11239133726759028\n.variants.viii_onset_restricted.point.s_rho 0.25382353612137104\n.variants.viii_onset_restricted.point.s_explore 0.7461764638786288\n.variants.viii_onset_restricted.point.s_contact 0.8585678011462191\n.variants.viii_onset_restricted.point.s_ret 0.25382353612137104\n.variants.viii_onset_restricted.point.diff_explore_ret 0.49235292775725775\n.variants.viii_onset_restricted.point.diff_contact_ret 0.604744265024848\n.variants.viii_onset_restricted.ci.s_E2 [0.818427854676209, 0.9085744683452258]\n.variants.viii_onset_restricted.ci.s_M [-0.15476645529294897, -0.07563199976628239]\n.variants.viii_onset_restricted.ci.s_rho [0.2237782219239448, 0.2807287493928801]\n.variants.viii_onset_restricted.ci.s_explore [0.7192712506071199, 0.7762217780760552]\n.variants.viii_onset_restricted.ci.s_contact [0.818427854676209, 0.9085744683452258]\n.variants.viii_onset_restricted.ci.s_ret [0.2237782219239448, 0.2807287493928801]\n.variants.viii_onset_restricted.ci.diff_explore_ret [0.43854250121423977, 0.5524435561521103]\n.variants.viii_onset_restricted.ci.diff_contact_ret [0.5471767920501125, 0.6728908667941018]\n.variants.viii_onset_restricted.se.s_E2 0.022144362792062486\n.variants.viii_onset_restricted.se.s_M 0.020316661634163045\n.variants.viii_onset_restricted.se.s_rho 0.014686711517235983\n.variants.viii_onset_restricted.se.s_explore 0.014686711517235983\n.variants.viii_onset_restricted.se.s_contact 0.022144362792062486\n.variants.viii_onset_restricted.se.s_ret 0.014686711517235983\n.variants.viii_onset_restricted.se.diff_explore_ret 0.029373423034471963\n.variants.viii_onset_restricted.se.diff_contact_ret 0.03161293813230454\n.variants.viii_onset_restricted.p_two_sided.s_E2 0.0\n.variants.viii_onset_restricted.p_two_sided.s_M 0.0\n.variants.viii_onset_restricted.p_two_sided.s_rho 0.0\n.variants.viii_onset_restricted.p_two_sided.s_explore 0.0\n.variants.viii_onset_restricted.p_two_sided.s_contact 0.0\n.variants.viii_onset_restricted.p_two_sided.s_ret 0.0\n.variants.viii_onset_restricted.p_two_sided.diff_explore_ret 0.0\n.variants.viii_onset_restricted.p_two_sided.diff_contact_ret 0.0\n.variants.viii_onset_restricted.boot_nan_share 0.0\n.variants.viii_onset_restricted_noMed.point.s_E2 0.8166833383739533\n.variants.viii_onset_restricted_noMed.point.s_M 0.025141546944322208\n.variants.viii_onset_restricted_noMed.point.s_rho 0.1581751146817245\n.variants.viii_onset_restricted_noMed.point.s_explore 0.8418248853182756\n.variants.viii_onset_restricted_noMed.point.s_contact 0.8166833383739533\n.variants.viii_onset_restricted_noMed.point.s_ret 0.1581751146817245\n.variants.viii_onset_restricted_noMed.point.diff_explore_ret 0.6836497706365511\n.variants.viii_onset_restricted_noMed.point.diff_contact_ret 0.6585082236922288\n.variants.viii_onset_restricted_noMed.ci.s_E2 [0.7580555089396425, 0.8772439088447826]\n.variants.viii_onset_restricted_noMed.ci.s_M [-0.0351342112111908, 0.08377625037120778]\n.variants.viii_onset_restricted_noMed.ci.s_rho [0.11066476556356196, 0.2054623386634095]\n.variants.viii_onset_restricted_noMed.ci.s_explore [0.7945376613365905, 0.8893352344364379]\n.variants.viii_onset_restricted_noMed.ci.s_contact [0.7580555089396425, 0.8772439088447826]\n.variants.viii_onset_restricted_noMed.ci.s_ret [0.11066476556356196, 0.2054623386634095]\n.variants.viii_onset_restricted_noMed.ci.diff_explore_ret [0.589075322673181, 0.7786704688728759]\n.variants.viii_onset_restricted_noMed.ci.diff_contact_ret [0.5668031671890846, 0.7482573350896375]\n.variants.viii_onset_restricted_noMed.se.s_E2 0.03107724574456982\n.variants.viii_onset_restricted_noMed.se.s_M 0.0304804351224009\n.variants.viii_onset_restricted_noMed.se.s_rho 0.024230955267049676\n.variants.viii_onset_restricted_noMed.se.s_explore 0.02423095526704968\n.variants.viii_onset_restricted_noMed.se.s_contact 0.03107724574456982\n.variants.viii_onset_restricted_noMed.se.s_ret 0.024230955267049676\n.variants.viii_onset_restricted_noMed.se.diff_explore_ret 0.04846191053409936\n.variants.viii_onset_restricted_noMed.se.diff_contact_ret 0.04665631647690804\n.variants.viii_onset_restricted_noMed.p_two_sided.s_E2 0.0\n.variants.viii_onset_restricted_noMed.p_two_sided.s_M 0.409\n.variants.viii_onset_restricted_noMed.p_two_sided.s_rho 0.0\n.variants.viii_onset_restricted_noMed.p_two_sided.s_explore 0.0\n.variants.viii_onset_restricted_noMed.p_two_sided.s_contact 0.0\n.variants.viii_onset_restricted_noMed.p_two_sided.s_ret 0.0\n.variants.viii_onset_restricted_noMed.p_two_sided.diff_explore_ret 0.0\n.variants.viii_onset_restricted_noMed.p_two_sided.diff_contact_ret 0.0\n.variants.viii_onset_restricted_noMed.boot_nan_share 0.0\n.variants.ix_noEXP6_noMed.point.s_E2 0.7834869969247006\n.variants.ix_noEXP6_noMed.point.s_M 0.02206143714355246\n.variants.ix_noEXP6_noMed.point.s_rho 0.19445156593174698\n.variants.ix_noEXP6_noMed.point.s_explore 0.805548434068253\n.variants.ix_noEXP6_noMed.point.s_contact 0.7834869969247006\n.variants.ix_noEXP6_noMed.point.s_ret 0.19445156593174698\n.variants.ix_noEXP6_noMed.point.diff_explore_ret 0.6110968681365061\n.variants.ix_noEXP6_noMed.point.diff_contact_ret 0.5890354309929536\n.variants.ix_noEXP6_noMed.ci.s_E2 [0.7285896894496919, 0.8464834952450123]\n.variants.ix_noEXP6_noMed.ci.s_M [-0.02094860676390847, 0.062238205309090404]\n.variants.ix_noEXP6_noMed.ci.s_rho [0.14375237500538474, 0.24348536466896695]\n.variants.ix_noEXP6_noMed.ci.s_explore [0.756514635331033, 0.8562476249946153]\n.variants.ix_noEXP6_noMed.ci.s_contact [0.7285896894496919, 0.8464834952450123]\n.variants.ix_noEXP6_noMed.ci.s_ret [0.14375237500538474, 0.24348536466896695]\n.variants.ix_noEXP6_noMed.ci.diff_explore_ret [0.513029270662066, 0.7124952499892305]\n.variants.ix_noEXP6_noMed.ci.diff_contact_ret [0.4939051582864316, 0.6948149440696897]\n.variants.ix_noEXP6_noMed.se.s_E2 0.029571190004501008\n.variants.ix_noEXP6_noMed.se.s_M 0.021587866680014528\n.variants.ix_noEXP6_noMed.se.s_rho 0.025541834533967123\n.variants.ix_noEXP6_noMed.se.s_explore 0.02554183453396713\n.variants.ix_noEXP6_noMed.se.s_contact 0.029571190004501008\n.variants.ix_noEXP6_noMed.se.s_ret 0.025541834533967123\n.variants.ix_noEXP6_noMed.se.diff_explore_ret 0.051083669067934254\n.variants.ix_noEXP6_noMed.se.diff_contact_ret 0.05086890200792258\n.variants.ix_noEXP6_noMed.p_two_sided.s_E2 0.0\n.variants.ix_noEXP6_noMed.p_two_sided.s_M 0.358\n.variants.ix_noEXP6_noMed.p_two_sided.s_rho 0.0\n.variants.ix_noEXP6_noMed.p_two_sided.s_explore 0.0\n.variants.ix_noEXP6_noMed.p_two_sided.s_contact 0.0\n.variants.ix_noEXP6_noMed.p_two_sided.s_ret 0.0\n.variants.ix_noEXP6_noMed.p_two_sided.diff_explore_ret 0.0\n.variants.ix_noEXP6_noMed.p_two_sided.diff_contact_ret 0.0\n.variants.ix_noEXP6_noMed.boot_nan_share 0.0\n.das_gupta_pooled.share_E2 0.767508790931281\n.das_gupta_pooled.share_M -0.05149802536399297\n.das_gupta_pooled.share_rho 0.2839892344327116\n.concept_level_cov.share_E2 0.5918624544739183\n.concept_level_cov.share_M 0.026232634646500663\n.concept_level_cov.share_rho 0.38190491087958095\n.concept_level_cov.identity_max_abs_err 4.440892098500626e-16\n.early_ratio_PR2.diff_bottom_minus_top -0.10985644166131972\n.early_ratio_PR2.ci [-0.13194436674436671, -0.08646458428602802]\n.early_ratio_PR2.psp_given_B5.ci [-0.20235651845780375, -0.1340540144497154]\n.early_ratio_PR2_noMed.diff_bottom_minus_top -0.030380713180299945\n.early_ratio_PR2_noMed.ci [-0.0619892455346123, 0.0026762652367938672]\n.early_ratio_PR2_noMed.psp_given_B5.ci [-0.18663893387393707, -0.09321641624655275]\n.verdicts.PR1.s_explore_minus_s_ret 0.6326537533475749\n.verdicts.PR1.ci [0.536934832161007, 0.7274184179003206]\n.verdicts.PR1.s_ret 0.18367312332621255\n.verdicts.PR1.s_ret_ci [0.1362907910498397, 0.23153258391949647]\n.verdicts.PR1.s_ret_below_0.5 True\n.verdicts.PR1b.s_contact_minus_s_ret 0.6039595082198055\n.verdicts.PR1b.ci [0.5076530678734679, 0.6983250662229235]\n.verdicts.PR2.diff -0.10985644166131972\n.verdicts.PR2.diff_ci [-0.13194436674436671, -0.08646458428602802]\n.verdicts.PR2.psp_ci [-0.20235651845780375, -0.1340540144497154]\n.verdicts.PR3_descriptive.ci [0.14394707520221456, 0.2667091999224775]\n.dev_groups.CS.n_concepts_with_outcome 216\n.dev_groups.CS.das_gupta_pooled.share_E2 0.7697377251850571\n.dev_groups.CS.das_gupta_pooled.share_M 0.16512492461519418\n.dev_groups.CS.das_gupta_pooled.share_rho 0.06513735019974859\n.dev_groups.CS.concept_level_cov.share_E2 0.52579371267494\n.dev_groups.CS.concept_level_cov.share_M 0.12068938269898696\n.dev_groups.CS.concept_level_cov.share_rho 0.3535169046260731\n.dev_groups.CS.concept_level_cov.identity_max_abs_err 4.440892098500626e-16\n.dev_groups.CS.early_ratio_PR2.diff_bottom_minus_top 0.1539821675238342\n.dev_groups.CS.early_ratio_PR2.ci [0.06449801490230803, 0.23470890881605166]\n.dev_groups.CS.early_ratio_PR2_noMed.diff_bottom_minus_top 0.1539821675238342\n.dev_groups.CS.early_ratio_PR2_noMed.ci [0.06551954989454997, 0.23252255395447888]\n.dev_groups.Eng.n_concepts_with_outcome 941\n.dev_groups.Eng.das_gupta_pooled.share_E2 0.8788889958317473\n.dev_groups.Eng.das_gupta_pooled.share_M -0.06562706717890002\n.dev_groups.Eng.das_gupta_pooled.share_rho 0.1867380713471527\n.dev_groups.Eng.concept_level_cov.share_E2 0.621308732922179\n.dev_groups.Eng.concept_level_cov.share_M -0.023367725617584344\n.dev_groups.Eng.concept_level_cov.share_rho 0.40205899269540574\n.dev_groups.Eng.concept_level_cov.identity_max_abs_err 4.440892098500626e-16\n.dev_groups.Eng.early_ratio_PR2.diff_bottom_minus_top -0.07023487140984941\n.dev_groups.Eng.early_ratio_PR2.ci [-0.11029734758081194, -0.03022673484116783]\n.dev_groups.Eng.early_ratio_PR2_noMed.diff_bottom_minus_top -0.07041437098255288\n.dev_groups.Eng.early_ratio_PR2_noMed.ci [-0.11190319854706438, -0.0311957868726843]\n.dev_groups.BGM.n_concepts_with_outcome 290\n.dev_groups.BGM.das_gupta_pooled.share_E2 0.672593323138095\n.dev_groups.BGM.das_gupta_pooled.share_M 0.10610982372306185\n.dev_groups.BGM.das_gupta_pooled.share_rho 0.22129685313884315\n.dev_groups.BGM.concept_level_cov.share_E2 0.45868000145790794\n.dev_groups.BGM.concept_level_cov.share_M 0.1595174960480624", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false, "persistedOutputPath": "/root/.claude/projects/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-3-invention-loop-iter-4-review-report-review-report/357c6d2d-3b97-4bd0-9c7a-7c771b541605/tool-results/bsynuapa8.txt", "persistedOutputSize": 32993}
```

### [32] ASSISTANT · 2026-09-29 04:48:18 UTC

```
The report's case-study table (26.4) lists pairs I don't see in the Experiment 12 README. I'll check `case_pairs.json` directly.
```

### [33] TOOL CALL — Bash · 2026-09-29 04:48:18 UTC

```
Verify case pair names in Experiment 12 outputs:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; python3 - <<'E'
import json
d=json.load(open('results/case_pairs.json'))
pairs = d if isinstance(d,list) else d.get('pairs', d)
print(type(pairs), (list(pairs.keys())[:10] if isinstance(pairs,dict) else len(pairs)))
items = pairs if isinstance(pairs,list) else pairs.get('pairs',[])
for p in items:
    s=json.dumps(p)
    import re
    names=re.findall(r'"(?:label|display_name|name|concept_name)": "([^"]+)"',s)
    print(names[:4], [k for k in p.keys()][:15])
E
grep -ril "deep learning\|systems biology\|spintronics\|reservoir computing\|metamaterial" results/case_pairs.json case_studies ai_atlas/table.csv 2>/dev/null | head; grep -i "deep learning\|spintronic\|metamaterial\|synthetic biology\|bayesian optim" ai_atlas/table.csv | cut -c1-200
```

### [34] TOOL RESULT — Bash · 2026-09-29 04:48:18 UTC

```
{"stdout": "<class 'list'> 7\n[] ['pair', 'rgroup', 'high', 'low', 'OPEN_all', 'OPEN_home', 'logvol', 'O2r_resid', 'Bn', 'E2', 'rho', 'high_open_higher_O2r_resid', 'open_home_order_disagrees']\n[] ['pair', 'rgroup', 'high', 'low', 'OPEN_all', 'OPEN_home', 'logvol', 'O2r_resid', 'Bn', 'E2', 'rho', 'high_open_higher_O2r_resid', 'open_home_order_disagrees']\n[] ['pair', 'rgroup', 'high', 'low', 'OPEN_all', 'OPEN_home', 'logvol', 'O2r_resid', 'Bn', 'E2', 'rho', 'high_open_higher_O2r_resid', 'open_home_order_disagrees']\n[] ['pair', 'rgroup', 'high', 'low', 'OPEN_all', 'OPEN_home', 'logvol', 'O2r_resid', 'Bn', 'E2', 'rho', 'high_open_higher_O2r_resid', 'open_home_order_disagrees']\n[] ['pair', 'rgroup', 'high', 'low', 'OPEN_all', 'OPEN_home', 'logvol', 'O2r_resid', 'Bn', 'E2', 'rho', 'high_open_higher_O2r_resid', 'open_home_order_disagrees']\n[] ['pair', 'rgroup', 'high', 'low', 'OPEN_all', 'OPEN_home', 'logvol', 'O2r_resid', 'Bn', 'E2', 'rho', 'high_open_higher_O2r_resid', 'open_home_order_disagrees']\n[] ['pair', 'rgroup', 'high', 'low', 'OPEN_all', 'OPEN_home', 'logvol', 'O2r_resid', 'Bn', 'E2', 'rho', 'high_open_higher_O2r_resid', 'open_home_order_disagrees']", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] TOOL CALL — Bash · 2026-09-29 04:48:18 UTC

```
Dump raw case_pairs.json head and search for report pair names:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; python3 - <<'E'
import json
d=json.load(open('results/case_pairs.json'))
print(json.dumps(d)[:1500])
E
grep -o '"high_label": "[^"]*"\|"low_label": "[^"]*"\|"label_hi[^,]*\|"label_lo[^,]*' results/case_pairs.json | head -20; grep -il "deep learning\|systems biology\|spintronics\|reservoir computing\|metamaterial\|Bayesian optimization" -r results/ ../../gen_report_text 2>/dev/null | head
```

### [36] TOOL RESULT — Bash · 2026-09-29 04:48:18 UTC

```
{"stdout": "{\"rule\": {\"pools\": \"per reporting group: top-quintile OPEN_all vs bottom-quintile OPEN_all among non-generic concepts with OPEN_home defined (quintiles within reporting group)\", \"match\": \"|z logvol diff| <= 0.25 and |z growth_c diff| <= 0.25 (z over all 12,499), same reporting group, |t0 diff| <= 2; widen to 0.35 for a group with no valid match (logged)\", \"seeding\": \"first try concepts named in EXP8 case_exemplars.json (high/low lists) as anchors; then the pair with the largest OPEN_all gap among remaining matches; ties by the smallest Mahalanobis distance on (logvol, growth_c, offhome_share)\", \"limits\": \"6-8 pairs; at most 2 from CS+Eng; at least 4 groups covered; one concept in at most one pair\", \"outcome_use\": \"O2r is NOT used in selection; displayed after selection only\", \"tol\": 0.25, \"tol_wide\": 0.35, \"max_pairs\": 8, \"min_pairs\": 6, \"max_cs_eng\": 2}, \"selection_log\": {\"generic_excluded\": 11157, \"generic_hits\": [{\"ci\": 3, \"name\": \"Complete intersection\", \"generic_why\": \"pre_onset_footprint\"}, {\"ci\": 4, \"name\": \"Torque converter\", \"generic_why\": \"pre_onset_footprint\"}, {\"ci\": 16, \"name\": \"Early adopter\", \"generic_why\": \"pre_onset_footprint\"}, {\"ci\": 37, \"name\": \"Prospect theory\", \"generic_why\": \"pre_onset_footprint\"}, {\"ci\": 48, \"name\": \"Dwarf spheroidal galaxy\", \"generic_why\": \"pre_onset_footprint\"}, {\"ci\": 52, \"name\": \"Magnetoelectric effect\", \"generic_why\": \"pre_onset_footprint\"}, {\"ci\": 53, \"name\": \"Neural development\", \"generic_why\": \"pre_onset_footprint\"}, {\"ci\": 54,\n../../gen_report_text/gen_report_text/paper_draft.md\n../../gen_report_text/gen_report_text/.terminal_claude_agent_struct_out.json\n../../gen_report_text/gen_report_text/.repl_agent.ptylog", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [37] TOOL CALL — Bash · 2026-09-29 04:48:24 UTC

```
Print actual case pairs from Experiment 12:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; python3 - <<'E'
import json
d=json.load(open('results/case_pairs.json'))
for k in d:
    if k not in ('rule','selection_log'): print(k, str(d[k])[:200])
ps = d.get('pairs') or d.get('case_pairs')
for p in ps:
    print(p['pair'], p['rgroup'], json.dumps(p['high'])[:120], json.dumps(p['low'])[:120], p['O2r_resid'], p['OPEN_all'])
E
```

### [38] TOOL RESULT — Bash · 2026-09-29 04:48:24 UTC

```
{"stdout": "pairs [{'pair': 'pair01_CSEng', 'rgroup': 'CS+Eng', 'high': 'Graphics processing unit', 'low': 'Vertical axis wind turbine', 'OPEN_all': [2.1224511003497835, -0.6691237194798072], 'OPEN_home': [0.4987059599\ndescriptive_summary in 7 of 7 pairs the high-OPEN member has the higher O2r_resid (no p-value; n <= 8; illustration only)\ndisclosure held-out outcomes were previously unsealed by EXP5/EXP7/EXP8; this seal fixes only this artifact's analysis choices (fixed on DEV before held-out states/outcomes were read by this artifact)\nSource s8_cases.py; rule frozen in results/frozen_spec.json (case_pairs)\npair01_CSEng CS+Eng \"Graphics processing unit\" \"Vertical axis wind turbine\" [3.2599171916920078, -0.9180104704375194] [2.1224511003497835, -0.6691237194798072]\npair02_BGMMed BGM+Med \"Shotgun proteomics\" \"Image-guided radiation therapy\" [1.3359666347862138, -3.5168864406072657] [1.5506709977859554, -1.2190170907446358]\npair03_PHYS PHYS \"Nanocarriers\" \"Nanosheet\" [2.787922462888554, 0.7304328490468972] [0.6659290147271483, -0.6149791238010124]\npair04_SOC SOC \"Soft power\" \"Autonomous learning\" [1.3480751627507148, 0.26018283759672567] [1.9551989199475421, -0.38976664105244546]\npair05_CSEng CS+Eng \"Scopus\" \"Oxygen reduction reaction\" [5.685703432708352, 0.7422291339682907] [1.843065009540754, -0.8267895779585691]\npair06_BGMMed BGM+Med \"Sclerostin\" \"IgG4-related disease\" [-0.9212264694059553, -1.578998499974558] [1.5477404399585464, -0.8642079724220579]\npair07_SOC SOC \"User-generated content\" \"Mindfulness-based cognitive therapy\" [0.739074703243495, -0.2206815977021952] [1.1430986105439127, -0.4039826307924678]", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] THINKING · 2026-09-29 04:48:52 UTC

```
Five of the seven case pairs cited in report 26.4 aren't in the artifact. Next I'll check the Experiment 12 preregistration wording and Evaluation 3's spec-curve build, then count artifacts per iteration.
```

### [40] TOOL CALL — Bash · 2026-09-29 04:48:52 UTC

```
Read Exp12 preregistration text and per-iteration artifact status:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop; python3 - <<'E'
import json
d=json.load(open('iter_4/gen_art/gen_art_experiment_12/results/preregistration_R2.json'))
s=json.dumps(d)
import re
for m in re.finditer(r'"(PR\d[a-z]?)[^"]*": "([^"]{0,400})', s): print(m.group(1), m.group(2)[:400]); 
print(s[:1200])
E
for i in 1 2 3 4; do echo "iter_$i:"; for d in iter_$i/gen_art/*/; do f=$d.aii_worker_result.json; if [ -f $f ]; then python3 -c "import json;d=json.load(open('$f'));print('  ',\"$d\".split('/')[-2], 'failed=',d.get('failed'))"; else echo "   $(basename $d) NO_RESULT"; fi; done; done
```

### [41] TOOL RESULT — Bash · 2026-09-29 04:48:54 UTC

```
{"stdout": "PR1 EXPLORATION > RETENTION: in variant (iv) [volume-stratified (early-volume quintiles), concepts with a Medicine (field 27) home excluded], s_explore - s_ret > 0 with the 95% concept-bootstrap CI > 0, where s_explore = s_E2 + s_M and s_ret = s_rho are the shares of the top-vs-bottom O2r_resid tercile gap in log mean breadth (Bn = retained off-home fields at t0+8). Equivalently s_ret < 0.5; both are \nPR1b (secondary, Holm family R2-A with PR1 and PR2): s_contact - s_ret > 0 with CI > 0 (s_contact = s_E2).\nPR2 LOCALISED KEEP MORE EARLY: mean RETENTION_RATIO_early(bottom O2r_resid tercile) - mean(top tercile) > 0 with CI > 0, AND the partial Spearman of RETENTION_RATIO_early with O2r_resid given B5 < 0 (CI < 0). The latter is flagged 'replication on the same frame as EXP8, not new evidence'.\nPR3 (descriptive, not tested): the sign of D_rho, i.e. whether late retention probability is lower for integrating (top-tercile) concepts.\n{\"PR1\": \"EXPLORATION > RETENTION: in variant (iv) [volume-stratified (early-volume quintiles), concepts with a Medicine (field 27) home excluded], s_explore - s_ret > 0 with the 95% concept-bootstrap CI > 0, where s_explore = s_E2 + s_M and s_ret = s_rho are the shares of the top-vs-bottom O2r_resid tercile gap in log mean breadth (Bn = retained off-home fields at t0+8). Equivalently s_ret < 0.5; both are printed (shares sum to 1).\", \"PR1b\": \"(secondary, Holm family R2-A with PR1 and PR2): s_contact - s_ret > 0 with CI > 0 (s_contact = s_E2).\", \"PR2\": \"LOCALISED KEEP MORE EARLY: mean RETENTION_RATIO_early(bottom O2r_resid tercile) - mean(top tercile) > 0 with CI > 0, AND the partial Spearman of RETENTION_RATIO_early with O2r_resid given B5 < 0 (CI < 0). The latter is flagged 'replication on the same frame as EXP8, not new evidence'.\", \"PR3\": \"(descriptive, not tested): the sign of D_rho, i.e. whether late retention probability is lower for integrating (top-tercile) concepts.\", \"verdict_rule\": \"per clause: SUPPORTED (CI on the predicted side) / NOT SUPPORTED (CI covers 0) / REVERSED (CI on the opposite side); evaluated separately on DEV and on held-out.\", \"holm_family_R2A\": [\"PR1\", \niter_1:\n   gen_art_dataset_1 failed= None\n   gen_art_experiment_1 failed= None\n   gen_art_experiment_2 failed= None\n   gen_art_experiment_3 failed= None\n   gen_art_experiment_4 failed= None\niter_2:\n   gen_art_dataset_2 failed= None\n   gen_art_evaluation_1 failed= None\n   gen_art_experiment_5 failed= None\n   gen_art_experiment_6 failed= None\n   gen_art_research_1 failed= None\niter_3:\n   gen_art_evaluation_2 failed= None\n   gen_art_experiment_7 failed= None\n   gen_art_experiment_8 failed= None\n   gen_art_experiment_9 failed= None\n   gen_art_research_2 failed= None\niter_4:\n   gen_art_evaluation_3 failed= None\n   gen_art_experiment_10 failed= None\n   gen_art_experiment_11 NO_RESULT\n   gen_art_experiment_12 failed= None\n   gen_art_research_3 failed= None", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [42] ASSISTANT · 2026-09-29 04:49:04 UTC

```
Experiment 12's PR2 and PR3 are misstated in the report. Now I'll check whether Evaluation 3's correction files were actually applied.
```

### [43] TOOL CALL — Bash · 2026-09-29 04:49:04 UTC

```
List Eval3 correction files and read 03 and 07:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3; ls corrections; head -c 2500 corrections/03*; echo; echo ----; head -c 1800 corrections/07*
```

### [44] TOOL RESULT — Bash · 2026-09-29 04:49:04 UTC

```
{"stdout": "00_index.md\n01_exp8_outcomes_relabel.md\n02_prereg_P1_P5.md\n03_exp7_tables.md\n04_eval2_text_corrections.md\n05_record_tables_map.md\n06_ledger_open_rows.md\n07_failed_artifacts.md\n08_candidate_S_and_families.md\n09_o5_leakage.md\n10_minor_slips.md\n11_boundary_results.md\n# 03 Exp7 tables (inserts for Section 18)\n\nTag: `[Correction, iteration 4, from art_22ppE1snfHKj]`. Every value is printed with its key path; a value not found at its key is printed NOT_FOUND (never retyped).\n\n## 18.5 Volume-matched contrast (retained R vs entered-not-retained N, same current x cumulative volume cell)\n\n| split | bins | d_R_m [CI] | d_N_m [CI] | contrast R - N [CI] | one-sided p | match rate (strata) | matched R / N fields | mean cum. prev. volume R / N |\n|---|---|---|---|---|---|---|---|---|\n| DEV | coarse | +0.069 [+0.021, +0.114] | +0.078 [+0.031, +0.129] | -0.008 [-0.071, +0.050] | 0.611 | 0.128 | 5,209 / 5,673 | 7.78 / 6.07 |\n| DEV | fine | +0.061 [+0.006, +0.112] | +0.075 [+0.020, +0.125] | -0.014 [-0.077, +0.048] | 0.683 | 0.121 | 4,869 / 5,359 | 6.20 / 5.52 |\n| held-out pooled 4 | coarse | +0.073 [+0.004, +0.134] | +0.100 [+0.039, +0.157] | -0.028 [-0.105, +0.046] | 0.755 | 0.153 | 5,125 / 5,597 | 7.98 / 6.30 |\n| held-out pooled 4 | fine | +0.066 [-0.002, +0.130] | +0.092 [+0.033, +0.152] | -0.026 [-0.107, +0.049] | 0.752 | 0.144 | 4,746 / 5,259 | 6.40 / 5.71 |\n\nSource: `3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/step2_dev.json` -> `battery.specificity.{b_volume_matched,b2_volume_matched_fine}.*`; `3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/step2_heldout.json` -> `pooled4.specificity.{b_volume_matched,b2_volume_matched_fine}.*`\n\nReading: both retained and non-retained matched fields carry a positive coefficient, and the pre-declared contrast is null in both bin sets. The retained-relatedness signal cannot be separated from volume.\n\n## 18.4 Dose by persistence age (held-out pooled 4)\n\n| age 2 | age 3 | age >= 4 | 4+ minus 2 [CI] | monotone non-decreasing | Spearman(beta, age) |\n|---|---|---|---|---|---|\n| +0.098 | +0.075 | +0.304 | +0.206 [+0.156, +0.255] | False | 0.50 |\n\nSource: `3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/step2_heldout.json` -> `pooled4.specificity.c_dose.*`\n\n## 18.9 Abandonment penalty d_lost: A1 vs R4 and variants (held-out pooled 4)\n\n| model | d_lost | CI | note |\n|---|---|---|---|\n| A1 = R0 + d_lost (all rows) | -0.007 | concept [-0.036, +0.022]; crossed [-0.082, +0.052] | verdict: INCONCLUSIVE (negative point estimate, CI includes 0) |\n| R4 = R3 + d_lost (primary sample) | +0.064 | - | positive once d0 is in the model |\n| min-cp proximity backbone, R4 | +0.003 | - | min-cp A1: d_lost -0.030, p = 0.00013 |\n| target-field FE, A1 | -0.044 | - | key `pooled4.sp\n----\n# 07 Failed artifacts, iteration counts and artifact ids\n\n## New Section 22b (or addition to 5a): Experiment 9 did not run\n\n[Correction, iteration 4, from gen_art_experiment_9 .aii_worker_result.json] Iteration 3 commissioned a fifth artifact, gen_art_experiment_9, from the plan 'Plan: how new concepts spread — trajectories and reasons (iteration 3, experiment direction 3)' (`iter_3/gen_plan/gen_plan_experiment_3/`: state sequences, breadth decomposition, empirical trajectory typology, sequence tests, snapshot lineage check, case studies, recognition timing). The worker failed before producing any output: `failed = true`, error: 'output_format validation failed after 5 retries: The output file `./.terminal_claude_agent_struct_out.json` does not exist yet.'. The workspace holds no method.py (absent) and no results. What was lost: the RQ2 trajectory typology and sequence tests for iteration 3. Status: **not run, not refuted**.\n\n## Iteration counts (from each artifact's .aii_worker_result.json)\n\n| iteration | commissioned | completed | failed | failed artifacts |\n|---|---|---|---|---|\n| 1 | 5 | 3 | 2 | gen_art_dataset_1, gen_art_experiment_2 |\n| 2 | 5 | 5 | 0 | - |\n| 3 | 5 | 4 | 1 | gen_art_experiment_9 |\n\nSource: `3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/results/partA_derived.json` -> `iterations.iter_<i>.*`\nCross-check with Section 5a: it lists gen_art_dataset_1 and gen_art_experiment_2 as the two iteration-1 failures, which agrees. Iteration 2 had no failures. Iteration 3's failure (Experiment 9) is not in the draft.\n\n## Artifact id placeholders -> real ids\n\n| placeholder in draft | real id | artifact |\n|---|---|---|\n| `[ARTIFACT:art_experiment_7]` (1 occurrences) | `art_22ppE1snfHKj` | Experiment 7 (retained frontier) |\n| `[ARTIFACT:art_experiment_8]` (1", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [45] TOOL CALL — Bash · 2026-09-29 04:49:10 UTC

```
Check Eval3 spec-curve build and headline in README:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3; grep -n -i "spec\|B2\|B3\|build\|ALL-PAPERS\|home" README.md | head -50
```

### [46] TOOL RESULT — Bash · 2026-09-29 04:49:10 UTC

```
{"stdout": "6:- **Part B** bounds the Exp8 openness lead (OPEN composite) on the Exp8 held-out groups. Those groups were already unsealed, so **Part B is EXPLORATORY**: it can reveal fragility, but it cannot confirm OPEN. The Part B specification was hash-frozen before any Part B statistic was computed (`results/boundary_spec.json`, sha256 in `logs/seal.log`).\n16:| B2 OPEN per unit | DL4 O2r_m50 +0.181 [0.082, 0.277], I2 0.73, prediction interval [−0.235, 0.541]; positive in 6/6 units | `results/per_group_table.csv`, `results/per_group_pooled.csv` |\n17:| B3 specification curve (1,920 specs) | share with pooled CI > 0 = 0.997; share of estimates > 0 = 1.000; median 0.152; Freedman–Lane p = 0.005 (200 draws); with CONTACT_REACH as a control the median is 0.146 vs 0.158 | `results/spec_curve.json`, `results/spec_curve_specs.csv` |\n28:| `seal.py` | STEP 0: `results/inputs_manifest.json` (path, size, sha256 of every input), `results/boundary_spec.json` (OPEN definition with DEV z-constants and PC1 loadings, spec grid, sub-unit rule, traits, GENERIC rule, verdict rules, seeds, iteration-4 listing at seal time), `logs/seal.log` |\n29:| `partb_core.py` | Gate T0, B1 post-onset re-score (the exact Exp8 `states()` code on the window-restricted matrix), B2 per-group table |\n30:| `spec_curve.py` | B3: 120 composites × 4 outcomes × 4 control sets, DL pooling with analytic Fisher-z SEs, 200-draw Freedman–Lane null, 2,000-draw headline bootstrap, bootstrap/analytic SE calibration |\n31:| `heterogeneity.py` | B4: home-field × period sub-units, REML meta-regression with Knapp–Hartung, permutation p and Holm; leave-one-group-out; LIFEENV diagnosis |\n33:| `figures.py` | `figures/spec_curve`, `open_forest`, `b1_post_onset`, `lifeenv_diagnosis` (.png and .pdf) |\n34:| `build_corrections.py` | STEP 4: `corrections/00_index.md` … `11_boundary_results.md` and `results/claims_ledger_v3.csv`; derived numbers go first to `results/partA_derived.json` |\n36:| `eval.py` | STEP 6: `eval_out.json` (schema `exp_eval_sol_out`; 102 metrics; datasets `open_heldout_concepts` 7,728, `spec_curve` 1,920, `claims_ledger_v3` 1,290) plus `full_`/`mini_`/`preview_eval_out.json` |\n49:./run_all.sh          # about 10 min on 4 CPUs; seal.py is commented out so the frozen spec is not overwritten\n56:- **Resource note.** The previous attempt of this artifact crashed the worker. OpenBLAS started 48 threads in each of about 36 worker processes on a 4-CPU box (`pthread_create failed`). Every script now pins BLAS/OMP to 1 thread and uses at most 3 workers. Results that had completed before the crash were checked and kept: seal, T0 and the spec curve. B1, B2 and B4 were re-run.\n60:- **Scope of OPEN.** OPEN is the all-papers build only. The HOME-ONLY build and the fresh 2015–16 cohort belong to another iteration-4 artifact. At seal time no cohort outcome was read (see `boundary_spec.json` → `cohort_2015_16_statement`).", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [47] TOOL CALL — Bash · 2026-09-29 04:49:16 UTC

```
Check spec-curve headline values and I2 figures in Eval3:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3; python3 - <<'E'
import json
d=json.load(open('results/spec_curve.json'))
s=json.dumps(d)
import re
for k in ['headline','I2','prediction_interval','median','share_ci_gt0','freedman']:
    for m in list(re.finditer('"[^"]*%s[^"]*": ([^,}]{0,80})'%k, s))[:4]: print(m.group(0)[:160])
E
grep -n "0.66\|0.43\|I2" README.md | head
```

### [48] TOOL RESULT — Bash · 2026-09-29 04:49:16 UTC

```
{"stdout": "\"headline\": {\"DL4\": {\"k\": 4\n\"I2\": 0.7274091009709045\n\"I2\": 0.8154633088551643\n\"I2\": 0.2357744304486206\n\"I2\": 0.7465171021521302\n\"median\": 0.15155908437166105\n\"median\": 0.13552027017334217\n\"p_median\": 0.004975124378109453\n\"null_median_mean\": -0.0023455512683427824\n\"share_ci_gt0\": 0.996875\n\"share_ci_gt0\": 1.0\n\"p_share_ci_gt0\": 0.004975124378109453\n\"null_share_ci_gt0_mean\": 0.01629166666666667\n16:| B2 OPEN per unit | DL4 O2r_m50 +0.181 [0.082, 0.277], I2 0.73, prediction interval [−0.235, 0.541]; positive in 6/6 units | `results/per_group_table.csv`, `results/per_group_pooled.csv` |\n18:| B4 heterogeneity | 21 sub-units: I2 0.43 vs 0.66 over 6 units; no trait moderates (all Holm p = 1); LIFEENV verdict UNEXPLAINED (psp 0.071 vs 0.186 in the other units; coverage reweighting gives 0.069) | `results/heterogeneity.json`, `results/subunit_table.csv` |", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [49] TOOL CALL — Bash · 2026-09-29 04:49:24 UTC

```
Check Exp8 headline indicator values in README:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; ls results | head -40; grep -n "M0_density_end\|ego_density_W3\|RETENTION_RATIO_early" README.md | head -12
```

### [50] TOOL RESULT — Bash · 2026-09-29 04:49:24 UTC

```
{"stdout": "audit.json\ncase_exemplars.json\nchecks.json\ndev_oof_predictions.parquet\ndev_ranking.csv\ndev_ranking_sensitivity.csv\ndeviations.json\nfeatures_config.json\nfrozen_spec.json\nheldout_predictions.parquet\nheldout_summary.json\nheldout_unit_results.csv\nindicator_clusters_dev.json\nindicator_corr_dev.csv\nindicator_dictionary.csv\nindicator_matrix.parquet\nlearned_model.json\nlearned_vs_single_heldout.json\no2r_resid_fit.json\no4_reference_expectations.csv\no5_join.json\noutcome_base_rates.json\nportability_table.csv\npower_dev.json\nprereg_b5_minus_reach.csv\nprereg_verdicts.json\nprovenance.json\nrederive.json\nrq1_dev_selection.json\nrq1_heldout.json\nsensitivities_heldout.csv\nsensitivities_pooled.json\nsize_diagnostic_dev.csv\nt0_8_ego_port.json\nt1_passA_exact_65_1125_1407_1918.json\nt4_ego_sanity.json\nt4_timing_nnull200_cut4.json\nunit_tests.json\n31:| **M0_density_end** | FR | + | +0.375 | [+0.279, +0.462] | 0.74 | 3.92e-12 | 6/6 | +0.276 / +0.354 |\n38:| **RETENTION_RATIO_early** | FR | - | -0.114 | [-0.160, -0.067] | 0.00 | 1.32e-05 | 6/6 | -0.187 / -0.105 |\n40:| **ego_density_W3** | A | - | -0.102 | [-0.151, -0.053] | 0.00 | 0.000288 | 6/6 | -0.095 / -0.041 |\n46:| **M0_density_end** | FR | + | +0.377 | [+0.280, +0.466] | 0.75 | 7.67e-12 | 6/6 | +0.274 / +0.358 |\n53:| **RETENTION_RATIO_early** | FR | - | -0.120 | [-0.166, -0.073] | 0.00 | 3.98e-06 | 6/6 | -0.191 / -0.107 |\n55:| **ego_density_W3** | A | - | -0.097 | [-0.146, -0.048] | 0.00 | 0.000654 | 6/6 | -0.092 / -0.037 |\n69:| RETENTION_RATIO_early | FR | - | -0.026 | [-0.060, +0.009] | 0.00 | 1 | 5/6 | -0.075 / -0.024 |\n82:| M0_density_end | FR | + | +0.012 | [-0.004, +0.027] | 0.00 | 1 | 4/6 | +0.007 / -0.006 |\n98:| M0_density_end | FR | + | +0.038 | [-0.011, +0.086] | 0.00 | 0.655 | 4/5 | +0.023 / +0.001 |\n129:| ego_density_W3 | A | + | +0.000 | [-0.004, +0.005] | 0.00 | 1 | 3/6 | +0.005 / -0.008 |\n154:| P4 | RETENTION_RATIO_early and FRONTIER_POTENTIAL: pooled psp > 0 with CI > 0 for O2r_resid AND O1c | **FAILS** |\n168:   confirmed indicator has the frozen sign in 6/6 units). The strongest are field-state indicators: `M0_density_end` (Hidalgo density of the fields not yet", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] TOOL CALL — Bash · 2026-09-29 04:49:48 UTC

```
List iteration 4 plan titles and strategy files:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4; ls gen_strat/* | head; python3 - <<'E'
import json,glob
for f in glob.glob('gen_plan/*/.terminal_claude_agent_struct_out.json'):
    d=json.load(open(f)); s=json.dumps(d)
    import re
    t=re.search(r'"title": "([^"]{0,200})',s)
    print(f.split('/')[1], t.group(1) if t else s[:200])
E
ls ../iter_4/gen_report_text/gen_report_text 2>/dev/null | head; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/ 
```

### [52] TOOL RESULT — Bash · 2026-09-29 04:49:48 UTC

```
{"stdout": "gen_strat/current_report.md\n\ngen_strat/gen_strat_1:\nREADME.md\nbuild_strategy.py\ngen_plan_research_1 Is 'keep exploring, spread widest' new?\ngen_plan_evaluation_1 Fix the record and test how far openness holds\ngen_plan_experiment_3 How concepts spread: contact versus keeping\ngen_plan_experiment_2 Does closing up at home slow a concept's spread?\ngen_plan_experiment_1 Do open-neighbourhood concepts spread? Fresh-cohort test\nREADME.md\ndomain_terms.json\npaper_draft.md\nreferences.bib\nreferences.json\nstyle_exemplars.md\niter_1\niter_2\niter_3\niter_4", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [53] TOOL CALL — Bash · 2026-09-29 04:49:52 UTC

```
Check iteration 3 version of Section 23 before overwrite:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4; grep -n "^## 23" -A 12 gen_strat/current_report.md | head -30; grep -c "" gen_strat/current_report.md
```

### [54] TOOL RESULT — Bash · 2026-09-29 04:49:52 UTC

```
{"stdout": "1216:## 23. What we have learned so far\n1217-\n1218-Three iterations, twelve artifacts (ten commissioned, eight completed in iteration 1; five completed in iteration 2; four completed in iteration 3) have tested whether temporal network signals predict how new scientific concepts spread across disciplines, using OpenAlex data on up to 12,499 concepts with up to 27,393 concept by field adoption episodes.\n1219-\n1220-**Confirmed findings:**\n1221-\n1222-1. **Retaining relatedness predicts the next field entered, beyond the Hidalgo/Guevara RCA density rival (the retained frontier hypothesis, PARTIAL).** A conditional logit on concept year risk sets shows that relatedness to the fields currently retaining a concept predicts which field the concept enters next, beyond field size, the conventional RCA > 1 density (D_rca), share weighted current presence density (D_vol), ever entered density, relatedness to home, and the target field's own gateway centrality. On an independent frame of 3,162 heldout concepts (6,978 entry events), d0_ret_rel = 0.322 (95% CI [0.291, 0.355]), LR = 325.8. DerSimonian-Laird pooled over 4 heldout groups: 0.243 [0.118, 0.368], I squared = 0.92. Positive in 3 of 3 evaluable groups (PHYS 0.148, LIFEENV 0.401, SOC 0.297; MATHDEC null). Cohort (2010-2014): 0.321. Permutation p = 0.001, rewired backbone p = 0.004, node label p = 0.003 (all Holm corrected < 0.01). **However:** the volume matched contrast is null on heldout data (Holm p = 0.76), so persistence and volume are confounded. The conditional logit's d0 may reflect sustained volume rather than adapted knowledge. The verdict is PARTIAL. The dose response is monotone nondecreasing (age 2: 0.056, age 3: 0.103, age 4+: 0.251; contrast 4+ vs 2: 0.195 [0.153, 0.236]).\n1223-\n1224-2. **Seven of 10 early network indicators are confirmed for predicting rarefied field breadth on heldout fields (the indicator screen deliverable).** The confirmed indicators (Holm p < 0.05, CI excluding zero, sign agreement 6/6 across 4 heldout groups + 2 cohort parts) are: M0_density_end (+0.375), D_vol_end (+0.307), CONTACT_REACH (+0.211), n_comm_W3 (+0.167), NOV (+0.151), RETENTION_RATIO_early (-0.114), and ego_density_W3 (-0.102). They span relatedness and cooccurrence families. An ElasticNet combining all indicators adds +0.059 (CI [0.046, 0.073]) Spearman correlation over the five feature baseline on 1,833 heldout concepts.\n1225-\n1226-3. **Retaining relatedness predicts the next field entered (the entry hypothesis, confirmed on holdout data in iteration 2).** Holdout LR 71.7 (p = 2.5e-17), standardised d = 0.30 (95% CI [0.24, 0.37]), DL pooled d = 0.28 (95% CI [0.22, 0.35], I squared = 0). This was confirmed in iteration 2 and is now replicated on a separate frame in iteration 3 with additional RCA and volume density rivals.\n1227-\n1228-4. **Two stable trajectory classes.** DTW k-medoids separates 188 concepts into \"integrating\" (128 concepts, mean 6.7 fields retaining by year 9) and \"localised\" (60 concepts, mean 2.9 fields retaining). Holdout recluster ARI = 0.54.\n1322", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/review_report/review_report", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [55] THINKING · 2026-09-29 04:51:24 UTC

```
Iteration 4 review found fabricated case-study rows, a missing Experiment 11 artifact, and sections left uncorrected. Now I'll write up the review JSON, manifest, and README.
```

### [56] TOOL CALL — Bash · 2026-09-29 04:51:24 UTC

```
Write the structured review JSON output:
cat > /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-3-invention-loop-iter-4-review-report-review-report/357c6d2d-3b97-4bd0-9c7a-7c771b541605/scratchpad/build.py <<'PY'
import json
out = {
"overall_assessment": (
"The iteration-4 record adds four real artifacts: Exp10 fresh-cohort OPEN test (art_NMe386dX9GLF), Exp12 RQ2 decomposition/typology (art_uw4OeagJP3rv), Eval3 boundary study + corrections pack (art_oKOd21ZMnu9S) and Research 3 (art_hSyVUBa2okT2). Many numbers recompute exactly from their files: the Exp10 ladder (OPEN_home R2 +0.091 [0.013, 0.171], Holm 0.048, DL +0.083 [-0.007, 0.173]), the Eval3 post-onset rescore (M0_density_end 0.374 -> 0.187), the spec curve (0.997, median 0.152, Freedman-Lane p = 0.005) and the Exp12 i_pooled decomposition shares (0.779 / -0.046 / 0.268; diff 0.464 [0.407, 0.528]). "
"But the record is not trustworthy as it stands, for four reasons. "
"(1) The case-study table in 26.4 is partly invented. Exp12 results/case_pairs.json holds 7 pairs: GPU/Vertical-axis wind turbine, Shotgun proteomics/Image-guided RT, Nanocarriers/Nanosheet, Soft power/Autonomous learning, Scopus/Oxygen reduction reaction, Sclerostin/IgG4-related disease, User-generated content/MBCT. The report prints five pairs that exist nowhere in the artifact: Systems biology/Tissue engineering, Bayesian optimization/Reservoir computing, SNA/BCI, Deep learning/Metamaterial, Synthetic biology/Spintronics. It uses qualitative 'high/moderate' cells instead of the numbers on disk, and it calls deep learning a 'canonical case'. That is illustrative content presented as a result, so results_reported = false. "
"(2) An executed artifact is missing. iter_4/gen_art_experiment_11 (plan 'Does closing up at home slow a concept's spread?') sealed a spec and ran its DEV body models. Both preregistered effects are null: density PPML b = -0.070 [-0.180, 0.040]; OPEN_home b = +0.015 [-0.038, 0.069]; DL density -0.075 [-0.210, 0.061]; H-M3 diff 0.0009 [-0.010, 0.012]. By the frozen rule that is NOT SUPPORTED. The event study was then interrupted, with no worker result. The report says 'Four artifacts were executed', counts 'fifteen commissioned', and in 28.1 lists 'within-concept closure -> entry slowdown: NEW', even though its own test of that claim was null. "
"(3) Several conclusions contradict the artifacts. Exp10 reads ALL-minus-HOME (+0.093) as mechanical coupling that inflated Exp8's openness signal about 2x; report 25.4 reads it as 'cross-field cooccurrence carries information'. Section 31.1 then headlines the coupled OPEN_all and the all-papers-only spec curve as confirmation. Exp10 says OPEN_home adds no practical prediction (+0.002 [-0.003, 0.008]); this is omitted. Exp12 says OPEN is NOT positively related to the keeping axis (PC2 partial -0.07 to -0.11); report 26.1 says OPEN 'correlates with the retention term'. Exp12's PR2 is 'localised keep more early'; the report renames it 'frontier advance positive'. The Exp10 cohort is 2015-2017 (373 are 2017 onsets), not 2015-2016. The O3 learned-model row is marked 'not evaluable' but is evaluable and null (-0.021 [-0.130, 0.101]). "
"(4) Section 27.6 claims 'All corrections have been applied in place'. They were not. Correction 03 (Exp7) is unapplied: 18.5 still presents d_R_m 0.069 as the volume-matched result, 18.4 is still DEV-only 'monotone', 18.9 still labels A1 as R4, and 18.11 is still wrong. Correction 07 is unapplied: the [ARTIFACT:art_experiment_7/8, art_evaluation_2, art_research_2] placeholders remain. Most of 04/05/06/09/10 is also unapplied: 13.1 entry counts, 5.4 'all_four', 4.4 '7 not available', 10.7 power, the 20.1 mismatch list, per-source O5 leakage. Iteration 3's Section 23 was silently replaced by a pointer, destroying that iteration's conclusions. "
"Soundness is therefore 1, and blocking is true. Coverage is partial. RQ1 is largely answered. RQ2's sequence question and the 'why it works' analysis are reported inaccurately. The exploratory AI stage exists only as Exp12's 37-concept atlas, which the report never mentions."),
"strengths": [
"Exp10 is a genuinely sealed, single-unseal confirmation on a fresh cohort, with a six-rung control ladder, HOME / ALL / SIZE-MATCHED builds that separate mechanical coupling, and an honest power statement in the artifact. The report's ladder and per-group DL tables (25.2-25.3) reproduce cohort_report.json exactly.",
"Eval3's post-onset rescore (27.1) directly answers the previous review's footprint objection. It records that about half of the M0_density_end and D_vol_end signal is pre-onset footprint, and that D_vol_post is nearly rank-identical to B5 reach.",
"Exp12 closes the Exp9 failure. The CONTINUUM verdict (DTW-HMM ARI 0.222, held-out 0.44 / 0.38) and the downgrade of the iteration-2 two-class typology are recorded as dead ends (29.3), which is correct.",
"Several previous MUST-FIX items were applied with in-place correction tags: the Exp8 O4/O3 relabel with the full 8-outcome learned-model table (19.5-19.7), the exact frozen P1-P5 text (19.8), the new_edge_rate reversal of dead end 7.4 and 4.3, the H1 LPM criterion, the H3 CI, ordering moved to MIXED, the Exp9 failure note (22.11), candidate S scored (29.8), and the proximity dependence of d0 (27.4).",
"Iteration chronology is otherwise kept: the iteration-4 sections are appended after the iteration-3 sections, and dead ends 29.1-29.9 are listed with numbers."
],
"dimension_scores": [
{"dimension":"soundness","score":1,
 "justification":"Case-study rows are fabricated. Three conclusions contradict their own artifacts: the coupling interpretation, OPEN versus the retention axis, and PR2. An executed null test (Exp11) is omitted while its claim is sold as NEW. Section 27.6 falsely states that all corrections were applied.",
 "improvements":[
  "Replace 26.4 with the seven pairs from Exp12 results/case_pairs.json, with numeric OPEN_all, OPEN_home, O2r_resid, E2 and rho per member.",
  "Rewrite 25.4, 26.1 and 31.1 to match the artifact readings (coupling inflates ALL; OPEN is not related to the keeping axis).",
  "Add Exp11 with its DEV null and the NOT SUPPORTED verdict."]},
{"dimension":"presentation","score":2,
 "justification":"Iteration-3 artifact markers are still placeholders. Earlier in-text reference numbers now point to different entries in the renumbered list: [24]-[30] cite Blackburn, Pinheiro, Albora, Bahar, Fernandes, Nomaler and Richardson, but the list has Foster, Shi, Ugander, Centola, Palla, Burt and Lockwood there. No iteration-4 table carries a 'Source: file -> key' line.",
 "improvements":[
  "Apply corrections/07 id substitutions.",
  "Keep a single stable reference list, or map old numbers to new ones.",
  "Add Source lines under every iteration-4 table (e.g. results/cohort_report.json -> headline.*)."]},
{"dimension":"contribution","score":2,
 "justification":"Much of iteration 4 is preserved, but the record drops an executed artifact (Exp11). It overwrote iteration 3's conclusions and left an insert-ready corrections pack mostly unapplied. It also omits Exp10 and Exp12 tables that bound the headline: OPEN_home predictive gain, within-type table, components, the n_authors_early O3 non-replication, planted-control non-recovery, PR1 variant iv, the sequence-test numbers, intersection-born HR, and the AI atlas.",
 "improvements":[
  "Add Section 25a on Exp11.",
  "Restore iteration-3 Section 23 verbatim with a correction note.",
  "Paste the omitted Exp10/Exp12 tables."]}
],
"critiques": [
{"category":"evidence","severity":"major",
 "description":"Fabricated case-study rows (Section 26.4, and 26.4's closing prose). Exp12 art_uw4OeagJP3rv results/case_pairs.json contains exactly 7 pairs: Graphics processing unit/Vertical axis wind turbine, Shotgun proteomics/Image-guided radiation therapy, Nanocarriers/Nanosheet, Soft power/Autonomous learning, Scopus/Oxygen reduction reaction, Sclerostin/IgG4-related disease, User-generated content/Mindfulness-based cognitive therapy. Only the first two appear in the report. The other five report rows do not exist in any Exp12 output: Systems biology/Tissue engineering, Bayesian optimization/Reservoir computing, Social network analysis/Brain-computer interface, Deep learning/Metamaterial, Synthetic biology/Spintronics. The 'OPEN diff'/'O2r diff' cells are qualitative words, not the numbers on disk. The sentence 'GPU computing and deep learning are canonical cases' describes a concept that is not in the pair set. The artifact also labels these pairs 'illustration, not inference' (7/7 descriptive, no p-value), which the report does not say.",
 "suggested_action":"Delete the invented rows and rebuild 26.4 from case_pairs.json. Give pair id, reporting group, high and low concept, OPEN_all (high/low), OPEN_home, logvol, O2r_resid, Bn, E2 and rho. Add the artifact's caveat that the pairs are an illustration only. Add a '[Correction, iteration 4]' note stating that the previous table contained rows not produced by any artifact. Also mention the 37-concept retrospective AI/CS atlas (ai_atlas/table.csv), the only execution of the request's exploratory AI stage."},
{"category":"evidence","severity":"major",
 "description":"An executed iteration-4 artifact is absent: iter_4/gen_art/gen_art_experiment_11, plan gen_plan_experiment_2 'Does closing up at home slow a concept's spread?'. It hash-sealed a within-concept pre-registration (prereg.md, logs/seal.log) and ran the DEV body models on 35,328 concept-years from 4,661 concepts (results/fe_results.json). H-M1 density PPML b = -0.070 [-0.180, 0.040], p = 0.21. H-M2 OPEN_home b = +0.015 [-0.038, 0.069]. The joint model is null, and so is the LPM twin. DL over groups: density -0.075 [-0.210, 0.061], I2 0.25; OPEN 0.012 [-0.040, 0.065]. H-M3 forward-minus-reverse diff 0.0009 [-0.010, 0.012]. By the frozen rule ('NOT SUPPORTED = both H-M1 and H-M2 CIs include 0 on DEV') this is a null. The Sun-Abraham event study was interrupted (logs/event_study.out KeyboardInterrupt), and there is no .aii_worker_result.json. Meanwhile Section 24 says 'Four artifacts were executed', Section 31 counts 'fifteen commissioned, twelve completed; three failed' (true: 20 commissioned, 16 completed, 4 failed/incomplete), and 28.1 records C4 'within concept closure -> entry slowdown' as NEW. The run's own test of that claim was null and is hidden.",
 "suggested_action":"Add 'Section 25a: Experiment 11 (incomplete)'. Give the plan, the preregistered H-M1 to H-M5, H-S1 and H-P1, the DEV table from fe_results.json (H_M1, H_M2, joint, lpm, H_M3 with bootstrap CIs, by_group, DL_*) and the verdict (NOT SUPPORTED on DEV). State that held-out, cohort and event study were not run because the worker stopped. List it in 29 as a dead end. In 28.1 add that the run's own lead-lag test of C4 was null on DEV. Fix the counts in 24 and 31."},
{"category":"evidence","severity":"major",
 "description":"The OPEN conclusions contradict Exp10's own reading. Exp10 README: 'Mechanical coupling is real and large ... EXP8's openness signal was therefore inflated by coupling; the uncoupled remainder is about half as large.' Also: 'Predictive value is negligible ... adding OPEN_home gives 0.770 (+0.002 [-0.003, +0.008]).' Report 25.4 reads ALL-minus-HOME +0.093 as 'confirming that cross field cooccurrence carries information beyond home field structure'. Report 25.7 and 31.1 present OPEN_all and OPEN_sizematch as 'clearly confirmed across all rungs and groups', and say 'the OPEN signal survives controls for ... label coverage and group fixed effects'. That is true only for the coupled builds; OPEN_home's CI includes 0 at R4 and R5. Section 31.1 also cites the Eval3 spec curve (99.7%) as confirmation, but Eval3 states that Part B is EXPLORATORY on already-unsealed groups and that 'OPEN is the all-papers build only'. Other omissions: the pipeline's planted psp = 0.10 was not recovered (+0.047 [-0.045, 0.132]), pre-seal power was 0.16 (MDE 0.105), and n_comm_W3 and participation are null in the HOME build (+0.002, +0.050) although they are headlined in 31.2. Section 25.1 says the cohort is 2015-2016, but it is 2015-2017 (n_by_t0 570/500/373) after the declared power extension.",
 "suggested_action":"Rewrite 25.4 using the artifact's wording: coupling inflates ALL; about half of the ALL-HOME gap is paper count (SIZEMATCH-HOME +0.053 [-0.015, 0.117]). In 25.6, add the OPEN_home predictive row (+0.002 [-0.003, 0.008]). Add the components table, the within-type table, the sensitivity table and the placebo/planted-control paragraph from the Exp10 README. Correct the cohort years. In 31.1, headline only OPEN_home (+0.091, R4/R5 include 0, DL includes 0), label OPEN_all 'mechanically coupled', and label the spec curve 'exploratory, all-papers build'."},
{"category":"evidence","severity":"major",
 "description":"Exp12 predictions and results are misstated (Section 26). (a) PR2 in results/preregistration_R2.json is 'LOCALISED KEEP MORE EARLY'. Its raw clause is REVERSED on DEV (-0.110 [-0.132, -0.086]), NOT SUPPORTED held-out (+0.011) and REVERSED in the cohort (-0.058). The report instead invents a 'Prediction 2 (frontier advance is positive): REVERSED'. (b) PR3 is the descriptive sign of D_rho (positive: integrating concepts keep more). The report's 'Prediction 3 (OPEN correlates more with exploration share) ... OPEN correlates with the retention term' contradicts the artifact: OPEN is related to PC1 (breadth) and NOT to PC2 (keeping), with DEV partial -0.07 to -0.11. (c) The report quotes variant i_pooled (0.732 / 0.268, diff 0.464) as the headline without naming it. The preregistered PR1 variant is iv, Medicine excluded: DEV 0.633 [0.537, 0.727], held-out 0.492 [0.403, 0.575], cohort 0.445 [0.358, 0.527], DL 0.504 [0.329, 0.679], I2 0.76. The primary ii volume-stratified variant gives 0.431. (d) The artifact states the shares are 'an accounting identity for the breadth outcome, not causal effects' because Bn and O2r share papers. Section 31.3's 'Breadth is driven by exploration' omits this. (e) Section 26.3 describes a 'lead lag regression of entry on prior retention' that Exp12 did not run. Exp12 ran a home-prominence half-peak vs off-home take-off test against a mechanical-lag null: excess DEV -0.009 [-0.015, -0.003], held-out +0.011 [0.005, 0.016] (rule word HOME-FIRST), cohort -0.017. Intersection-born HR is 0.47 [0.42, 0.54]. This is the request's 'central in home community first, or at intersections?' question, and its numbers are missing.",
 "suggested_action":"Rebuild 26.1 as a table of the four variants (i, ii, iii, iv) × DEV/held-out/cohort from decomposition_*.json, with PR1 on variant iv. Quote PR1, PR1b, PR2 and PR3 verbatim with their verdicts, and add the accounting-identity caveat to 26.1 and 31.3. Replace 26.3 with the sequence_light_*.json table (share A<T, null share, excess [CI], verdict word) and the intersection-born hazard ratios. Add the OPEN~PC1/PC2 table (three builds; DEV, held-out DL, cohort)."},
{"category":"clarity","severity":"major",
 "description":"Section 27.6 claims 'All corrections have been applied in place', and 27.5 reports '0 MISMATCH', but most of Eval3's insert-ready pack is not in the report. Correction 03 (Exp7) is unapplied: 18.5 still presents d_R_m 0.069 [0.019, 0.118] as the volume-matched result, although the preregistered contrast R-N is -0.008 [-0.071, 0.050] DEV and -0.028 [-0.105, 0.046] held-out. 18.4 is still DEV-only and 'monotone' (held-out 0.098 / 0.075 / 0.304, monotone = False). 18.9 still labels A1 as R4 (R4 d_lost is +0.064). 18.6 still quotes DEV sensitivities, and 18.11 still has the crossed-bootstrap and '7 of 17' slips. 22.1 and 31.4 repeat the DEV 0.069. Correction 07 is unapplied: [ARTIFACT:art_experiment_7], art_experiment_8, art_evaluation_2 and art_research_2 remain in 17-21. From corrections 04/05/06/09/10: 13.1 still gives entry counts as 'Concepts matched' (concepts 1,298/1,121/2,635/213); 5.4 still shows 'B5 + all_four' (size_controlled_all_three, refit CI [-0.043, 0.220]); 4.4 still says 7 partials are 'not available' (record_tables/partial_association_all.csv has 12); 10.7's 0.004 is still misattributed; 20.1 does not list the 6 MISMATCH / 15 MISLABELLED rows; 20.2 still says 67% for every source. Eval3 Step 3 is not recorded either: D_rca_pers differs from D_rca_persist_k (max rho 0.877), so that rival is untested.",
 "suggested_action":"Walk corrections/00_index.md file by file and insert every block at its named section with its tag and Source line. After insertion, rerun verify_ledger.py against the new report text and state the result in 27.5. Replace the 27.6 sentence with a per-file applied/not-applied list."},
{"category":"clarity","severity":"major",
 "description":"Chronology broken: iteration 3's 'What we have learned so far' (Section 23) was replaced by 'See updated summary at end of iteration 4 (Section 31)'. The iteration-3 conclusions are gone from the record, with no correction marker. They included the iteration-3 claim that the dose response is 'monotone' and the two-class typology listed as confirmed; iter_4/gen_strat/current_report.md lines 1216+ still hold that text. Section 16 (iteration 2) still lists 'Two stable trajectory classes' under Confirmed without an in-place correction, although Exp12 shows ARI 0.20 against its own classes.",
 "suggested_action":"Restore Section 23 verbatim from iter_4/gen_strat/current_report.md. Add '[Correction, iteration 4]' notes where Exp12 and Eval3 overturned it (dose not monotone on held-out; typology CONTINUUM; volume-matched contrast null on DEV too). Add a correction tag under 16.2."},
{"category":"novelty","severity":"major",
 "description":"Positive claims still lack an honest nearest-neighbour check against this run's own boundaries. Research 3 marks C3 ('low retention ratio -> breadth') NEW, and 31.2 lists RETENTION_RATIO_early as confirmed. But on the fresh cohort it is null once type and reach enter (R2 -0.043 [-0.116, 0.031]; R3 -0.025), and Exp12's raw PR2 clause is REVERSED (integrating concepts keep MORE early). C4 is marked NEW while Exp11 is null. For C1 (openness -> breadth), the nearest neighbours are Maillart et al. 2026 (concept-pair diffusion) and Cheng et al. 2023 (consistency -> volume, i.e. weighted edge persistence). The survivor beyond them is small: the home-only edge_persistence and NOV_res signal (-0.112, +0.134) on one cohort, with DL CI including 0 and no predictive gain. The report does not say this, and the Cheng sign-flip test Research 3 recommended was not run.",
 "suggested_action":"In 28, attach to each NEW or PARTIAL verdict the run's own evidence for and against: C3, the cohort attenuation and the PR2 reversal; C4, the Exp11 null. Write one paragraph stating what survives beyond Cheng 2023 and Maillart 2026: a home-only novelty / low-persistence partial association of about 0.08-0.13 on a 573-concept cohort, fragile at R4/R5, with no forecasting gain. Move RETENTION_RATIO_early in 31.2 to 'does not survive concept-type controls'."},
{"category":"evidence","severity":"major",
 "description":"Exp10 replication failures of earlier positive results are omitted. First, n_authors_early does NOT replicate for O3 (+0.014) or O1b (+0.036), although Exp8's only confirmed O3 indicator is recorded in 19.5b as positive. Second, the cohort O3 learned model is evaluable (evaluable = true in learned_models_cohort.json) and null: 0.540 vs B5 0.561, diff -0.021 [-0.130, 0.101]. Report 25.6 says 'not evaluable', and 19.7 still calls transience 'predictable beyond B5'. Third, CONTACT_REACH halves to +0.101 without intersection-born concepts, which the report does not mention anywhere. The per-group table for the Exp8 confirmed O2r indicators (heldout_unit_results.csv), required by the previous review and by the request ('within individual scientific fields'), is still absent.",
 "suggested_action":"Add Exp10's 'Leads replicated (secondary)' block verbatim. Correct 25.6's O3 row to -0.021 [-0.130, 0.101], evaluable, null, and add a '[Correction, iteration 4]' under 19.5b/19.7 noting the fresh-cohort non-replication. Add the per-group table (PHYS, LIFEENV, SOC, MATHDEC, COH_DEVHOME, COH_OTHER; psp [CI], n) for the 7 confirmed indicators, marking cells whose CI includes 0."},
{"category":"scope","severity":"major",
 "description":"Coverage of the original request is partial, and the coverage table overstates it. Section 30 marks 'Strongest indicator analysis: Decomposition + case studies' and 'Case studies: Done', but the case studies are misreported. The request's step 1 (exploratory AI area inspected before fixing the method) exists only as Exp12's retrospective 37-concept AI atlas (ai_atlas/), which the report never mentions. RQ2's ordering question ('central within the original community first, or emerging at intersections') has a real null answer in Exp12 that is not reported. The 'why it works' analysis relies on Exp10's component table, but the table itself is not in the report. The Cheng-measure test, the degree-normalised ego density and survival-alongside-breadth are listed as open with no reason.",
 "suggested_action":"Correct Section 30 per cell, with the artifact behind each. Add rows for 'Exploratory AI stage' (Exp12 atlas, retrospective, outcome-selected), 'Home-first vs intersection ordering' (Exp12 sequence test, no signal beyond mechanical lag; Exp11 closure test null on DEV, incomplete) and 'Why it works' (Exp10 components: NOV_res and low persistence carry the home-only signal). Set the next iteration's priorities: finish Exp11 held-out and event study from the cached panel at zero credits, then run the Cheng consistency test on volume vs breadth."},
{"category":"clarity","severity":"minor",
 "description":"Smaller slips. 27.4 calls the min-cp d0 = -0.021 'at the footprint control rung'; that rung does not exist in Exp7. 27.3 compares 21-subunit I2 0.43 with '0.66 over 6 units' while 27.2 gives 0.73 for the same headline; the artifact reports both, from different models, and this is not explained. The reference list was renumbered in iteration 4, so earlier citations point to wrong entries: [25] is now Shi & Evans instead of Pinheiro, and [28] Palla instead of Fernandes & Tang. Fernandes & Tang 2014 and Nomaler & Verspagen 2022 are cited but not listed.",
 "suggested_action":"Remove 'footprint control rung' and cite step2_heldout.json -> proximity sensitivity. Label the two I2 values by model. Keep one cumulative reference list with stable numbers and add the two missing entries."}
],
"results_reported": False,
"coverage": "partial",
"blocking": True,
"score": 2,
"confidence": 4
}
json.dump(out, open('.terminal_claude_agent_struct_out.json','w'), indent=1, ensure_ascii=False)
print("ok", len(out['critiques']))
PY
python3 /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-3-invention-loop-iter-4-review-report-review-report/357c6d2d-3b97-4bd0-9c7a-7c771b541605/scratchpad/build.py
```

### [57] TOOL RESULT — Bash · 2026-09-29 04:51:24 UTC

```
{"stdout": "ok 10", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [58] TOOL CALL — Bash · 2026-09-29 04:51:33 UTC

```
Write manifest and README, validate JSON output:
cat > .aii/manifest.yaml <<'EOF'
entries:
  - path: .terminal_claude_agent_struct_out.json
    keep: the review deliverable read by the next step (small text file)
EOF
cat > README.md <<'EOF'
# Review of the iteration-4 research report (run_Id7TLZ6r1C7M)

This folder holds an adversarial audit of the run's internal research report after iteration 4. It checks completeness, traceability and consistency against the iteration 1-4 artifact workspaces. No code was executed against the data; the audit read each artifact's result files and recomputed the report's headline numbers from them.

## Layout
- `.terminal_claude_agent_struct_out.json`: the structured review (scores, 10 critiques, `results_reported=false`, `blocking=true`).
- `.aii/manifest.yaml`: disposal manifest. Nothing heavy was created.
- `README.md`: this file.

## Main findings
1. Five of the seven case-study pairs in report Section 26.4 do not exist in `gen_art_experiment_12/results/case_pairs.json`.
2. `iter_4/gen_art/gen_art_experiment_11` (within-concept closure test) ran its DEV models (null by the frozen rule) but is absent from the report.
3. The report reverses Exp10's coupling reading and Exp12's OPEN-versus-retention result, and it mislabels Exp12's PR2.
4. Most of Eval3's insert-ready corrections were not applied, although Section 27.6 says they were. Iteration 3's Section 23 was overwritten.

## How to run
Nothing to run. To re-check a finding, open the artifact file named in the corresponding critique.

## Restoring removed files
No files are marked `delete`, so nothing needs restoring.
EOF
python3 -c "import json;d=json.load(open('.terminal_claude_agent_struct_out.json'));print(d['blocking'],d['results_reported'],d['score'])"
```

### [59] TOOL RESULT — Bash · 2026-09-29 04:51:33 UTC

```
{"stdout": "True False 2", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [60] ASSISTANT · 2026-09-29 04:51:43 UTC

```
I've written the review to `.terminal_claude_agent_struct_out.json`. Its verdict: the report must not ship as it stands. It scores 2/10 with confidence 4, soundness 1, presentation 2, contribution 2, and coverage "partial". I also wrote the disposal manifest in `.aii/` and a `README.md`.

**Why it blocks:**
- **Invented case studies.** Section 26.4 lists seven pairs of contrasting concepts, but only two exist in Experiment 12's `results/case_pairs.json`. The other five (Systems biology/Tissue engineering, Deep learning/Metamaterial, Synthetic biology/Spintronics, Bayesian optimization/Reservoir computing, Social network analysis/Brain-computer interface) appear in no output. Because made-up results are presented as real, I set `results_reported` to false and `blocking` to true.
- **An experiment that ran is missing.** `iter_4/gen_art_experiment_11` ("Does closing up at home slow a concept's spread?") sealed its plan and ran its dev-panel models. Both predicted effects came out null, which fails its own pre-registered rule. Its later event-study step was interrupted before finishing. The report omits the experiment entirely, while Section 28.1 labels that same claim "NEW". Its artifact counts are also wrong: 20 were commissioned and 16 completed, not "fifteen commissioned, twelve completed".
- **Conclusions that contradict the artifacts:**
  - Experiment 10 says counting other-field papers inflates the "openness" signal about twofold. The report reads the same gap as extra information and headlines the inflated version.
  - Experiment 10 found the home-only openness score adds no practical prediction (+0.002). The report omits this.
  - Experiment 12 found openness is not related to how well concepts keep fields. The report says it is.
  - The report restates Experiment 12's second prediction as a different one.
  - The fresh cohort covers 2015–2017, not 2015–2016.
  - The transience model on the cohort is reported as "not evaluable"; it was evaluated and is null.
- **Corrections claimed but not applied.** Section 27.6 says all of Evaluation 3's corrections were applied. Most were not: Experiment 7's tables are still wrong, the placeholder artifact IDs remain, and several earlier fixes are still missing. Iteration 3's "what we learned" section was also silently replaced with a pointer, which erases that iteration's conclusions.

The other critiques cover:
- Novelty claims that the run's own evidence weakens, such as the early-retention indicator losing significance on the fresh cohort.
- Earlier results that failed to replicate on the new cohort but aren't reported.
- Gaps against the original request: the exploratory AI stage, the "home community first or at intersections" question, and the per-field tables.
- Broken reference numbering.

**What checked out:** I recomputed the Experiment 10 control-ladder numbers, Evaluation 3's pre-onset rescore and specification curve, and the Experiment 12 decomposition shares from their files, and they match.
```

### [61] SYSTEM-USER prompt · 2026-09-29 04:51:45 UTC

```
<CRITICAL_ERROR>
The module-end file check FAILED (attempt 1/3).

PROBLEMS:
  - .aii/manifest.yaml: '.terminal_claude_agent_struct_out.json' matches nothing that needs a decision — remove it (text, code and files under the auto-keep floor are always kept)

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

### [62] TOOL CALL — Bash · 2026-09-29 04:51:49 UTC

```
Empty the manifest entries and update README line:
printf 'entries: []\n' > .aii/manifest.yaml && sed -i 's/- `.aii\/manifest.yaml`: disposal manifest. Nothing heavy was created./- `.aii\/manifest.yaml`: disposal manifest (empty, because nothing heavy was created)./' README.md && cat .aii/manifest.yaml && grep manifest README.md
```

### [63] TOOL RESULT — Bash · 2026-09-29 04:51:49 UTC

```
{"stdout": "entries: []\n- `.aii/manifest.yaml`: disposal manifest (empty, because nothing heavy was created).", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [64] ASSISTANT · 2026-09-29 04:51:50 UTC

```
I've fixed the manifest so the module-end check should now pass. The workspace holds only small text files, so nothing needs a keep or delete decision. `.aii/manifest.yaml` is now `entries: []`, and the manifest line in `README.md` says it is empty on purpose. The review itself in `.terminal_claude_agent_struct_out.json` is unchanged.
```
