# gen_strat_1 — test_idea

> Phase: `invention_loop` · round 4 · `gen_strat`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_strat_1` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 02:00:31 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 02:00:37 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A strategy planner (Step 3.1: GEN_STRAT in the invention loop)

Each iteration of the invention loop runs: GEN_STRAT → GEN_PLAN → GEN_ART → GEN_REPORT_TEXT → REVIEW_REPORT → UPD_HYPO
Artifact types: RESEARCH (web search), EXPERIMENT (code), DATASET (data collection), EVALUATION (metrics), PROOF (Lean 4)
State persists across iterations: strategies, plans, artifacts, report_texts (read from the run tree)

You received the hypothesis, iteration status (current + remaining), previous iteration's strategies, available artifact types, existing artifacts, and reviewer feedback.
Your strategy governs THIS iteration only. You define what artifacts to create NOW.

Focused strategy → efficient progress. Scattered strategy → wasted iteration.
</your_role>
</ai_inventor_context>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.), with base_url=os.environ["OPENROUTER_BASE_URL"] and api_key=os.environ["OPENROUTER_API_KEY"] (the OpenAI SDK's defaults, OPENAI_BASE_URL and OPENAI_API_KEY, point at the same place, so a plain OpenAI() client also works with OpenRouter model ids). The key is this run's own OpenRouter key and works only at that base URL: never hard-code OpenRouter's own URL, or every call fails with 401
- **SPEND BUDGET**: OpenRouter budget for this phase of the run (Test idea): $20 USD for the ENTIRE Test idea phase, start to finish. This is ONE pot shared by every agent, subagent and step in this phase, not a per-agent, per-subagent or per-artifact allowance: other agents in this phase are drawing on this same $20 USD right now, including ones you never see. The run's other phases have pots of their own, and this phase cannot borrow from them. Every paid OpenRouter call counts against it: LLM calls from your code or the terminal, and image generation. Your own ceiling for THIS artifact is a smaller limit that sits inside that shared total: spend at most $10 USD here, and less when the work allows or you are unsure, preferring cheaper models. The phase's budget is enforced by AI Inventor, not by OpenRouter: once it is spent, every paid OpenRouter call is refused with HTTP 403 and an error whose message starts 'AI Inventor per-run OpenRouter budget' (retrying will not help; ':free' models keep working). The first such refusal ends a whole batch: stop every call still queued or in flight (check for it after a concurrent call gets its slot, not only before it waits for one) instead of letting each be refused in turn, and do not rerun the batch. GET <base_url>/key reports this phase's limit and what is left of it. Your per-artifact share is not enforced for you: read each response's usage.cost, keep a running total and stop when you approach it. Budget the work up front: estimate the per-call cost and the number of calls BEFORE starting a sweep, not after it overruns. Every call spends real money that the run cannot recover, and a sweep refused halfway costs the run its results.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Free-first web search (general + scholarly modes), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-concept-fig-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<time_budgets>

Each artifact executor has a fixed time budget (including writing code, debugging, testing, and fixing errors):

- research: 3h
- dataset: 6h
- experiment: 6h
- evaluation: 3h
- proof: 3h

</time_budgets>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<research_methodology>
Think like a researcher planning a study for a top venue.

- All strategies run in parallel and their artifacts combine into one pool. Together they must build toward a publishable paper — each strategy contributes a distinct, necessary piece. No strategy should be a standalone island.
- Ask yourself: what would a reviewer need to see? Proper baselines, controlled comparisons, ablations that isolate what matters. Plan artifacts that preempt reviewer objections.
- Depth over breadth. One well-designed experiment with proper controls beats five shallow ones.
- Match your evaluation to your claims. Measure what the hypothesis actually asserts.
- When results are weak or partial, vary the approach before writing it off. One failed method doesn't falsify the hypothesis.
- If iterations remain, think about what the NEXT iteration will need. Leave useful building blocks — datasets, baselines, preliminary results — that future strategies can build on, refine, or compare against.
</research_methodology>

<principles>
1. FOCUS ON NOVELTY - every strategy must lead to a genuinely novel contribution
2. MAXIMIZE PARALLELIZATION - all artifacts in your strategy run in parallel
3. BUILD ON EXISTING WORK - use completed artifacts from previous iterations, learn from failures
4. ITERATE ON THE METHOD - a negative result is first about the approach, not the hypothesis. Try different methods, parameters, data, or formulations. When the hypothesis itself has been widened, that same energy goes into testing SEVERAL candidate answers at once rather than one of them harder.
5. TWO SHAPES OF ITERATION - a DEEP TEST pushes one claim further; a WIDE SCREEN tests several candidate answers cheaply in parallel and confirms the survivor on held-out evidence. Read which one this iteration is from the hypothesis and the instructions in the user prompt, and build that shape. Never answer a widened hypothesis with one more deep test.
6. NEVER SHRINK TO FIT - do not plan an iteration whose best possible outcome is a smaller, safer version of a claim that already came back weak. If the claim is in trouble, the strategy's job is to put better candidates in play, not to find a corner where the old one survives.
7. DIAGNOSE BEFORE DECIDING - before each iteration, review what worked, what didn't, and why. Use that to choose what to try next. Gaps are action items, not conclusions.
8. SET DEPENDENCIES WISELY - depends_on is a list of {id, label} objects referencing existing artifacts; each label is a short free-text type (a word or two, e.g. "dataset", "validates", "extends") that tags how the dep is used
9. PLAN FOR DEPENDENCIES - if an artifact depends on another (e.g. experiments need datasets), ensure prerequisites exist first or plan them this iteration for the next
</principles>

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
Your workspace: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_strat/gen_strat_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_strat/gen_strat_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_strat/gen_strat_1/file.py`, `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_strat/gen_strat_1/results/out.json`
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

<hypothesis>
Your strategy should advance this hypothesis.

kind: hypothesis
title: Concepts that keep exploring spread widest
hypothesis: |-
  MAIN CLAIM (RQ1 and RQ2 through one mechanism): OPENNESS, NOT CONSOLIDATION. A new concept becomes broadly integrated when its first three years (t0..t0+2) keep its network neighbourhood OPEN. It keeps acquiring new co-occurrence partners (new_edge_rate) from many communities (n_comm_W3, participation, NOV_res). It keeps a loose, churning ego network (low ego_density_W3, low edge_persistence). It spreads its disciplinary contacts thinly (low RETENTION_RATIO_early: few of the fields it touches keep it). A concept that CONSOLIDATES early stays local, even when it grows as fast. Consolidation means a dense, persistent semantic neighbourhood and contacts concentrated in fields that keep it. The outcome is size-adjusted breadth (O2r rarefied at m = 50, and O2r_resid). This inverts the account this run pre-registered twice: naturalisation (A*_h, iteration 1) and the retained frontier (iterations 2-3). It also inverts P4 of art_dFQ6jbgNsR6Q, which predicted RETENTION_RATIO_early > 0 and found -0.120. MECHANISM. Exploration versus exploitation (March 1991), and interpretive flexibility, as in boundary objects (Star & Griesemer 1989). While a concept's partner set and meaning are still open, distant communities can recombine it at low adaptation cost; it behaves like a general-purpose tool. Early consolidation ties its meaning to a local problem set and raises the cost for other fields to adopt it. In network terms this is structural diversity of contact (Ugander et al. 2012; Weng et al. 2013) against closure and redundancy (Burt). The one-sentence finding we expect to state: 'concepts still being recombined with new partners across communities three years after birth become broadly integrated; concepts that settle early into a dense, stable neighbourhood stay local, even when they grow just as fast'. If it holds, emergence monitors should track neighbourhood openness, not growth or consolidation. It would also reverse the intuitive reading of Cheng et al. (2023) 'consistent usage' for cross-field breadth.

  EVIDENCE BEHIND IT: a LEAD, art_dFQ6jbgNsR6Q, EXP5 frame, frozen on DEV and scored once on held-out. Held-out partial Spearman given B5 for O2r_m50 (results/portability_table.csv and README tables):
  - new_edge_rate +0.118 [0.072, 0.163]: CI > 0 in PHYS, LIFEENV, SOC and both cohort parts, 0 sign flips. P3 predicted it would FAIL; it transferred.
  - n_comm_W3 +0.167 [0.063, 0.267], I2 0.78.
  - NOV +0.151 [0.044, 0.255], I2 0.75; NOV_res +0.139 [0.033, 0.241].
  - participation +0.150 [0.025, 0.271].
  - D_rare +0.162 [0.022, 0.296].
  - ego_density_W3 -0.102 [-0.151, -0.053].
  - edge_persistence -0.080 [-0.126, -0.033]. This was pre-registered (P2) and HOLDS.
  - RETENTION_RATIO_early -0.114 on O2r_m50, -0.120 on O2r_resid, with 6/6 sign agreement.
  - degree and strength growth are null, and so is turnover.
  - The weak spot is LIFEENV: NOV 0.03, n_comm_W3 0.06 and participation 0.02 all have CI including 0, while new_edge_rate holds at 0.09. MATHDEC has n = 101.
  There is entry-level corroboration from art_22ppE1snfHKj. In volume-matched cells, fields the concept entered but did NOT retain predict its next entry at least as strongly as retained fields: d_N_m 0.100 against d_R_m 0.073, contrast -0.028 [-0.105, 0.046] held-out and -0.0085 on DEV. Contact matters; keeping does not.

  WHY IT IS STILL ONLY A LEAD. (i) Apart from P2, the set was assembled after the held-out unseal. (ii) The obvious confound is untested: concept TYPE, i.e. method/tool concepts against object/phenomenon concepts, plus generic pre-existing terms. The top held-out concepts include 'Coefficient of variation' and 'Exponential growth'. (iii) There is mechanical coupling. Off-home spread brings new co-occurring topics, so an ego network built on all papers partly measures breadth itself. (iv) Heterogeneity is high (I2 0.75-0.78).

  CLOSED, one sentence each in the paper.
  (a) The RETAINED FRONTIER (art_22ppE1snfHKj). The PMI-backbone conditional logit gives d0 0.322 [0.291, 0.355], with a two-way (concept, field) SE of 0.056 against 0.016 concept-only, and crossed CI [0.201, 0.468]. But the pre-declared volume-matched contrast is null on DEV and held-out. The held-out dose betas are 0.098 / 0.075 / 0.304 (not monotone; Spearman 0.5). Hidalgo 2007's minimum-conditional-probability proximity fits better (within-stratum AUC 0.866 against 0.852). Under it, d0 reverses to -0.021 (p = 0.012), and RCA>1 density carries the signal (LR 246). The LPM with size deciles is about 0. What survives is the relatedness principle itself, which is not new. D_rca_pers, the persistence-filtered RCA density that Research 2 lists as missing, was already in S_strict.
  (b) The ABANDONMENT PENALTY is mixed and depends on the specification. A1 gives -0.007 [-0.036, 0.022]. In R4, with d0 and the rivals, it is +0.064 [0.030, 0.095]. It is -0.030 (p = 1e-4) under min-cp proximity and -0.044 with target-field FE.
  (c) Gateway retention (H1), gateway landing (H3; not established, CI [-0.006, 0.065]), gateway weighting, rescue and relay are closed. So are A*_h and D_ratio as headlines (D_ratio held-out 0.066 [0.001, 0.131]; the D family was never frozen because more than 30% of values were missing).
  (d) O5 external recognition is closed as a validation outcome. It is unrelated to O2r (rho 0.014) and O1 (0.001), and weakly negative with O3 (-0.049, p = 0.004, I2 0.55). Precedence leakage varies by source: MeSH 0.70, Gartner 0.68, ACM CCS 0.17. No indicator or model beats B5 plus onset year.
  (e) Candidate S (co-author components; S_comp, S_comp_n, S_isolated_share) was computed on 12,499 concepts and is not confirmed for any outcome (S_comp_n O3 +0.068, Holm 0.41).
  (f) M0_density_end and D_vol_end are NOT early network signals as built. They use cumulative 1995..t0+2 field history, which is a pre-onset footprint, and are re-scored post-onset only.
  (g) The two-class trajectory typology and the ordering result are NOT ESTABLISHED. HMM-vs-DTW ARI is 0.094; the DEV localised class is 55 Med + 7 Eng; the ordering is MIXED.

  DESIGN FOR THE NEXT ITERATION (zero OpenAlex credits; S3 snapshot; LLM spend < $2).
  (1) FRESH CONFIRMATION EVIDENCE that no screen has touched: the 2015-2016 onset cohort.
  - Grounding is identical: TAG rule, LLM precision gate, newborn rule on years <= t0, venue-label fields.
  - One new zero-credit snapshot pass adds 2015-2024 works.
  - The early window is t0..t0+2 and the outcomes are O2r_m50, O2r_resid, O1c, O1b, O3 and O4 at t0+6..t0+8, ending by 2024.
  - Fallback, declared now: if fewer than 800 concepts pass, add 2017 onsets with outcomes at t0+5..t0+7.
  - The whole EXP5 frame (12,499 concepts; DEV and old held-out) is now SELECTION data. Every definition, sign and control is frozen on it and hash-sealed BEFORE any cohort outcome is computed.
  - The cohort is evaluated once.
  - Groups: CS+Eng, BGM+Med, PHYS, LIFEENV, SOC, with MATHDEC reported.
  - Resampling unit: the concept. Report 2,000-draw bootstraps, DL pooling with I2, and Holm correction.
  (2) THE OPENNESS INDEX, with its signs fixed now: OPEN = mean of z(new_edge_rate), z(n_comm_W3), z(participation), z(NOV_res), -z(ego_density_W3) and -z(edge_persistence). RETENTION_RATIO_early is reported separately as the disciplinary analogue and is predicted negative. There are two builds. ALL-PAPERS, as in Exp8. HOME-ONLY: the ego network from the concept's home-field papers only, which off-home spread cannot mechanically inflate. All features use t0..t0+2 papers only.
  (3) ATTACK THE CONFOUNDS HEAD-ON. The control ladder is B5 -> +CONTACT_REACH -> +CONCEPT TYPE -> +PRE-ONSET FOOTPRINT -> +label coverage -> +home-group FE.
  - CONCEPT TYPE is LLM-labelled as method/technique/tool, object/material/organism/disease, property/measure/theory or topic/field. A 300-pair benchmark with 60 hand checks is required, with precision >= 0.85.
  - PRE-ONSET FOOTPRINT is the term's pre-t0 papers and fields, plus a re-emergence flag.
  - OPEN must add signal with CI > 0 at every rung.
  - The within-type estimates for method concepts and for object concepts must both be > 0.
  (4) WITHIN-CONCEPT DYNAMICS (RQ2 timing; replaces the MIXED ordering test). This runs on the yearly EXP5 panel.
  - Model: home-only openness in year t -> off-home field-entry hazard in t+1, with concept and year FE.
  - The reverse path is also estimated.
  - An event study runs around the first home-only closure jump (ego density rise), with pre-trend tests and a within-concept-year permutation placebo.
  - Prediction: closure precedes a slowdown of entry, and entry does not precede closure.
  (5) RQ2 TRAJECTORIES: RE-RUN THE FAILED ARTIFACT.
  - gen_art_experiment_9 (plan gen_plan_experiment_3) was never executed; its output-format loop failed.
  - It is re-run on the existing EXP5 arrays, with its pre-registration updated here.
  - The breadth decomposition is log-additive: contact rate x retention probability x frontier advance, with Shapley shares.
  - NEW PREDICTION, informative either way: localised and integrating concepts differ MORE in contact and exploration than in retention, and localised concepts have HIGHER early retention ratios. This is the opposite of the previous hypothesis.
  - Typology: DTW k-medoids plus HMM. A class is named only if ARI >= 0.5 and it survives excluding Medicine homes; otherwise the result is reported as a continuum along the OPEN axis.
  - The request's sequence question is tested directly. Does home-community prominence (home-only degree or k-core rank) peak before off-home entry take-off? Or do intersection-born concepts (>= 2 homes) diffuse without it? Both get pre-trend tests.
  (6) WHY IT WORKS, AND CASE STUDIES.
  - Decompose the n_comm_W3 and new_edge_rate signal: which communities the new partners come from (method communities against domain communities; home against off-home), and which bridging papers carry them.
  - Case studies are matched pairs from the quantitative extremes (equal early growth, opposite OPEN; seeded from case_exemplars.json), with alluvial field-flow and ego-network snapshots.
  - An AI/CS atlas of about 40 CS-home concepts serves as the request's stage-1 inspection, labelled as retrospective and descriptive.
  (7) SECONDARY REPLICATIONS on the fresh cohort, frozen from Exp8:
  - the O3 L1-logit (+0.093 AUC [0.028, 0.163] over a B5 at chance, 0.506) and n_authors_early for O3 (+0.089), O1b (+0.029) and O1c (+0.161);
  - the O4 EBM (Spearman 0.188 against 0.015; its linear model shrank to a constant);
  - the O2r ElasticNet (+0.059 [0.046, 0.073]);
  - CONTACT_REACH (+0.21, halved to +0.111 without intersection-born concepts).

  SUCCESS.
  - CONFIRMED if, on the fresh cohort: HOME-ONLY OPEN has partial rho > 0 with concept-bootstrap CI > 0 at the concept-type and footprint rungs; its sign is positive in >= 4 of 5 groups; it is > 0 within method concepts and within object concepts; and RETENTION_RATIO_early is < 0 given B5.
  - MECHANISM SUPPORTED if within-concept closure lowers the next-year entry hazard (CI < 0), pre-trends are flat, and the reverse path is weaker.
  - INFORMATIVE EITHER WAY. (a) If concept type absorbs OPEN, the portable RQ1 signal is concept type, and co-occurrence openness is its network marker; this is reported as that. (b) If HOME-ONLY OPEN fails while ALL-PAPERS OPEN holds, the Exp8 signal is mechanical (the ego network absorbs the spread), and this is reported as a measurement warning for co-occurrence emergence indicators.
  - DISCONFIRMED if the fresh-cohort CI of OPEN includes 0 at the concept-type rung. There is no subgroup hunting after the unseal.

  RECORD CORRECTIONS carried into the paper (reviewer MUST-FIX, not new tests):
  - The Exp8 O4/O3 labels are fixed. REL_home and author_growth predict O4 citation growth, not transience. O3 is a positive held-out result (n_authors_early and the L1-logit), with the caveat that B5 is at chance.
  - All 8 learned-model rows are shown.
  - The P1-P5 verdicts are given with their exact frozen text. P1 fails because D_rare, participation and NOV_res add MORE than predicted. P3 fails because new_edge_rate transfers, and this corrects dead end 7.4. P5 fails because CONTACT_REACH adds +0.223 given B5 minus reach.
  - The Exp7 tables are rebuilt from step2_dev.json and step2_heldout.json.
  - All 14 blocks of art_7W9xiIO3FVBs text_corrections.md are applied.
  - Real artifact ids replace the placeholders, and every table gets a Source line.
  - Exp9 is recorded as failed ('not run, not refuted').
  - Iteration counts: iteration 1 completed 3 of 5 artifacts, iteration 2 completed 5, iteration 3 completed 4 of 5.
motivation: >-
  Target venue: Applied Network Science, collection 'Networks for everyday life'. The contribution is framed as a network
  measurement: a layer-assortativity contrast in a concept-specific temporal multilayer citation network, adjusted by the
  same nodes' background assortativity. It is validated against about 45 network indicators on held-out fields. Gap. Emerging-topic
  work operationalises emergence as growth or structural prominence in co-word, co-occurrence or citation networks: Rotolo
  et al.'s attributes, Salatino et al.'s pre-emergence density, Chen's structural variation, link forecasting on OpenAlex
  concept graphs (arXiv 2606.03864; Shi & Ma 2026), and Maillart et al. 2026's endogenous-versus-exogenous diffusion of concept
  pairs. Diffusion is usually measured as reach or entropy across fields. The largest concept-diffusion study (Cheng et al.
  2023, ASR) shows that social reach, consistent usage and fit with traditions predict which ideas become core. But touching
  a discipline is not being practised by it. Many concepts appear in a neighbouring field as borrowed tools, cited back to
  their origin, and vanish when home interest fades. That is the task's 'temporary expansion' and 'short spike vs persistent
  integration' problem. Field-level knowledge-trade indices (Rinia et al. 2002; Yan et al. 2013 self-dependence and import/export;
  De Domenico et al. 2016 sources and sinks) measure how self-reliant a whole field is. They do not ask whether one concept
  has become part of an adopting field's own literature, and they do not net out the field's general insularity. The probe
  shows that this netting-out is the crux: raw concept lineage assortativity is mostly general homophily. Measured feasibility
  (2026-09-28, x-ratelimit headers). A group_by call costs 1 credit ($0.0001), EVEN with a title_and_abstract.search filter,
  so yearly phrase counts and field breakdowns are cheap. Paged phrase retrieval costs 10 credits per 200 works. ID-batch
  lookups cost 1 credit per 50 works, and singletons are free. The free allowance is 10,000 credits a day. The probe cost
  40-150 credits per concept. What the probe also showed. (i) Stemmed phrase search is unsafe for onset: 'altmetrics' returns
  about 3,700 works a year in 2000, and the exact-string share of stemmed matches was 0.35-0.97. It is only 0.35 for optogenetics
  because 'optogenetic' is a legitimate variant. So grounding needs lemma-aware local matching and a labelled benchmark. (ii)
  The strict newborn rule (<= 10 papers in each of the 3 prior years) rejected 6 of 8 well-known new concepts because of a
  few precursor papers, so the rule is made relative. Yearly counts near the threshold also changed between repeated calls
  on the same day (optogenetics 2007: 20 vs 18), so all counts are cached once and onset is fixed from that snapshot. (iii)
  Venue labels covered 26-80% of concept-papers, lowest for conference-heavy CS, so label coverage is a covariate and a sensitivity
  analysis is pre-registered. If the claim holds, practice changes. Emergence monitors (funders, foresight units, OpenAlex
  topic curators) should track whether adopting fields cite a concept like their own literature, not how many fields mention
  it. Diffusion studies should adjust field-level citation indicators for background homophily and stop using paper-level
  topic classifiers as discipline labels. RQ1 also gets an answer the field lacks: emergence and diffusion have different
  early network signals. If the claim fails, the study still delivers the full ~45-indicator x outcome x field matrix, the
  M1 homophily decomposition, the label-bias measurement and an empirical RQ2 trajectory taxonomy.
assumptions:
- >-
  Citations to earlier concept-papers are a usable, partial trace of how a concept is passed on. Missing links (obliteration
  by incorporation, software or textbook citations) are allowed if they do not hit off-home parents harder than home parents.
  Checks: lineage coverage per (concept, field, concept-age) is a covariate and a competitor indicator. A bibliographic-coupling
  version of A*_h (for papers without a direct concept-parent) must rank concepts consistently with the citation version on
  dev (Spearman >= 0.6).
- >-
  A child's other references are a valid proxy for its general disciplinary citing habits (the negative-control exposure).
  A 10-reference sample per citing paper is enough; this is checked by split-half reliability of the background log-odds ratio
  on dev concepts (target >= 0.7). Home and off-home adopters in the same year see the same concept stock, which is why availability
  and preferential attachment cancel in the odds ratio. An impact-aware availability version (A*_imp) and a placebo contrast
  with established concepts in the same field pair are reported alongside as checks.
- >-
  Venue field labels are concept-independent and stable enough to be used for features without leaking the future. The source
  is the first non-repository location of the work, with dominant field >= 40% of the source's topic profile. A drift audit
  on 300 sources compares pre-2008 and pre-2012 profiles with current ones and switches to period-specific profiles if agreement
  is < 90%. Venue-unlabelled papers are treated as missing at random within a concept. This is tested on dev concepts with
  a leakage-free team profile: one group_by call per paper over its authors' works published before that year. Author career
  profiles, where future information is harmless, label the OUTCOMES.
- >-
  Concept membership can be grounded with measured precision. Lemma-aware phrase matching of the name and aliases is done
  locally on downloaded titles and abstracts and validated on a labelled benchmark. Concepts with precision < 0.8 are dropped
  before any outcome is examined. Onsets in 2003-2014 leave an outcome window (t0+6..t0+8) that ends by 2022.
- >-
  The study fits the economy the user asked for. The estimate is about 45k OpenAlex credits (about $4.5): five daily free
  windows, or one day plus about $3.5 prepaid. It also needs < $1 of OpenRouter LLM labelling, CPU only. The work is ordered
  so that dev-set selection finishes first and held-out data are fetched only after freezing.
investigation_approach: >-
  ECONOMY FIRST. Every Tier-B concept is downloaded once, and that download feeds the lineage network, the co-occurrence ego
  network and the semantic features. Anything that group_by can answer uses group_by (1 credit, even with phrase filters).
  Existing resources come first: the legacy OpenAlex concept vocabulary with Wikidata IDs, PubTator3 entity annotations (a
  grounding check for biomedical concepts), NLM MeSH introduction years, Wikipedia creation dates, Clarivate Research Fronts,
  and Cheng et al.'s concept list if it is released. STEP 0, OUTCOME-BLIND FRAMES (answers the survivorship critique). Frame
  N (primary for base rates): for each year 2003-2014, draw a 10,000-work random sample (list calls with sample+seed, 600
  credits in total). Extract title noun-phrase 2-3-grams that are frequent in year t and absent from the t-3..t-1 samples.
  Phrase-count each candidate with ONE group_by-by-year call (about 3,000 credits). Frame W: legacy concepts with Wikidata
  IDs. They are needed for MeSH/Wikipedia outcomes and as nodes of the concept-level backbone. Being in W (MAG Fields of Study
  were seeded from Wikipedia around 2016-19) is treated as a known selection condition. No present-day works_count filter
  is applied; every size filter uses years <= t0 only. Newborn rule (relaxed after the probe): t0 is the first year with >=
  20 grounded papers, and each of t0-3..t0-1 must have fewer than 25% of the t0+2 count. Re-emerging terms (e.g. graphene)
  form a separate stratum. The O2r/O3 base rates of W and N are compared. If they differ by > 25% relative, W is reweighted
  by inverse inclusion probability, from a logistic model of W-membership among N candidates using pre-t0 features only. STEP
  1, GROUNDING BENCHMARK (the user's 'create labelled data, then train your own model'). Build 500 (concept, paper) pairs
  stratified by field and by match type: stemmed-only, lemma-variant, exact, tag-only. Label them with a cheap LLM via OpenRouter;
  a second model double-labels 150 pairs, and 60 pairs are checked by hand. Split 300/200 into train/test. Report the precision
  and recall of stemmed, exact, lemma-aware and tag-intersected rules. Train a logistic regression on MiniLM title/abstract
  embeddings plus match flags as a sense filter, and freeze it on dev. STEP 2, EXPLORATORY AI STAGE (about 40 hand-picked
  AI concepts with contrasting trajectories, plus 20 random dev newborns). Three graph views are inspected openly before the
  design is frozen. (a) The lineage multilayer network. (b) A PMI-normalised co-occurrence ego network. (c) A CONCEPT-LEVEL
  backbone (answers the centrality critique): nodes are about 1,500 Frame-W concepts, and edges come from one group_by concepts.id
  call per node per slice (2000-04, 2005-09, 2010-14; about 4.5k credits), restricted to vocabulary edges. Frame-N concepts
  are inserted as nodes through one phrase-filtered group_by call per slice. Leiden communities are aligned across slices.
  Participation, brokerage, betweenness and k-core are computed for the concept node itself. Legacy-tag imprecision is tolerable
  here, because co-occurrence aggregates many papers; this is checked by comparing tag-based and phrase-based ego rows on
  the 40 concepts. Frozen at the end of this step: lag G = 3, 5-year feature window, home rule, Mantel-Haenszel strata, references
  sampled per child, and detector calibration. STEP 3, ESTIMATOR. Children are concept-papers with >= 1 concept-parent in
  years t-3..t-1. Each child's parent weight is split equally among its parents. Shared-author links are removed from the
  main estimator and kept as a self-lineage channel. The concept term is the MH log odds ratio of the child-layer x parent-layer
  table. The background term is the same odds ratio over 10 sampled non-concept references per child, for up to 150 home and
  150 off-home children, fetched in 50-ID batches. A*_h and field-level rho*_j have child-resampling bootstrap CIs. Reported
  alongside, with no headline role: A*_unif (the previous design), A*_imp (availability weighted by 1 + in-citations), a placebo
  contrast (A*_h minus that of 3 established concepts in the same home/off-home field pair and period), naive R_away and renewal
  R. PRE-REGISTERED DIAGNOSTICS (dev only, before any held-out access): Spearman of each lineage indicator with log off-home
  growth and with log off-home volume, and the M1 decomposition (R^2 of the raw concept log-odds ratio on the background log-odds
  ratio across dev concepts). STEP 4, INDICATORS (about 45, in 10 families that measure different things), each on t0..t0+2
  and t0..t0+4. A popularity (count, share, growth, acceleration, Kleinberg burst, author growth). B co-occurrence connectivity
  (strength growth, new-edge rate, edge persistence, neighbour turnover, PMI selectivity growth). C backbone centrality of
  the concept node (eigenvector, PageRank, betweenness change, k-core). D community (participation, community transitions,
  Burt constraint, structural diversity of new neighbours). E closure (clustering change, triadic-closure rate). F disciplinary
  (reach, Shannon entropy, Rao-Stirling, fields gained per year, off-home volume and field-group composition). G lineage (A*_h,
  A*_h slope, max rho*_j, number of naturalised fields, A*_imp, A*_unif, self-lineage share, coverage, background log-odds
  ratio, naive R_away, renewal R). H semantic (drift and dispersion of the context embedding). I Cheng et al. resonance (reach
  over unconnected author components, links to prominent concepts, fit with established concepts). J count-based multivariate
  Hawkes off-home branching ratio. STEP 5, TWO TIERS, STRICT HOLD-OUT. Tier A (about 1,000 concepts from N and W, group_by
  only, about 4 credits each) covers families A and F with venue labels, O1, O2r (venue labels), O3 and O4 (a group_by by
  year on cites:<early IDs>). Tier B (about 300 concepts, 40-150 credits each as measured) covers all families, plus author-labelled
  outcomes from a 150-paper outcome-window sample. Dev: home field in Computer Science, Engineering, Biochemistry/Genetics
  or Medicine, onset 2003-2009. Held-out field groups, never used for selection: physical, life/environment, social, and mathematics/decision
  sciences, onset 2003-2009. Held-out cohort: onset 2010-2014 in all fields. A simulation-based power analysis on dev sets
  the Tier-B allocation (>= 45 concepts per held-out group). Budget in total: about 45k credits (Step 0 about 4k, backbone
  about 5k, Tier A about 4k, Tier B about 30k, audits about 2k). STEP 6, INDEPENDENT OUTCOMES at t0+6..t0+8, with no overlap
  with feature windows. O1 sustained uptake (field-normalised share in years 6-8 >= year-5 share). O2r PRIMARY breadth: rarefied
  field richness, the expected number of distinct fields among m = 50 random concept-papers (exact hypergeometric), author-labelled
  in Tier B and venue-labelled in Tier A. Also reported: breadth residualised on log volume, O2-raw (fields with >= 5 papers
  a year for 3 years) as a secondary outcome, and entries into 252-subfields with low pre-t0 relatedness to home ('previously
  unrelated subfields'). O3 transience: peak in t0+3..t0+8 and peak / mean(t0+7..t0+8) >= 2, so every window ends by 2022.
  O4 citation growth. O5 external recognition: MeSH descriptor introduced after t0, a Research Fronts listing, or a Wikipedia
  article created by t0+8 (creation date only, never existence). 'Local specialisation' is high O1 with low O2r. STEP 7, SELECTION
  AND VALIDATION. On dev only, rank indicators per outcome by Spearman, AUC (top vs bottom tercile within field group) and
  incremental AUC over the baseline. Freeze a top 10 per outcome and evaluate once on held-out data. The resampling unit is
  the concept: 2,000 field-clustered bootstrap resamples, leave-one-field-out, and a random-effects meta-analysis across held-out
  groups (pooled delta-AUC, I^2, sign test). The full outcome x indicator x field matrix is reported, and AI-only indicators
  are named as negative results. Label sensitivity: everything is rerun with venue-only, team-profile and primary_topic labels
  (P5). STEP 8, RQ2 TRAJECTORIES. For concepts with O1 = 1, build multivariate series (A*_h, naturalised-field count, entropy,
  participation, backbone betweenness, clustering, community transitions). Cluster them with DTW k-medoids and a Gaussian
  HMM, choosing k by silhouette and bootstrap stability, with no predefined classes. Ordering test with matched detection
  power: every series is standardised, and one Bayesian online change-point detector is applied to all of them. Its threshold
  is calibrated so that the false-alarm rate is 5% on dev concepts that never diffuse (bottom O2r tercile). This is complemented
  by threshold-free panel lead-lag regressions (Delta entropy(t+1) on A*_h(t) and the reverse, with concept fixed effects),
  a placebo that permutes field labels within concept-year, and minimum-link sensitivity at 10, 15 and 25 links. Intersection-born
  concepts (>= 2 fields with rho*_j >= 0 in the first window) are analysed separately. WHY IT WORKS. Decompose changes in
  A*_h into field-pair contributions and bridging papers. Contrast borrowed-phase and naturalised-phase papers of the same
  field: do naturalised papers cite field-specific co-concepts and field-specific methods? Case studies are drawn from the
  quantitative extremes. OPTIONAL: an Explainable Boosting Machine or L1-logistic model on all indicators, trained on dev,
  compared with the best single indicator on the same held-out set, with its interactions (e.g. entropy x A*_h) interpreted.
  The paper follows Applied Network Science structure, with a methodology figure: grounding -> frames -> three graph views
  -> ten indicator families with the background-adjusted lineage contrast -> two-tier hold-out -> outcomes -> trajectories.
success_criteria: >-
  Judged only on HELD-OUT fields and cohort, with settings frozen on dev. PRIMARY (both required for CONFIRMED). (C1, P1)
  A*_h level or slope ranks in the top 3 of ~45 indicators for O2r. Its pooled held-out AUC is >= 0.70, and it adds delta-AUC
  >= 0.04 (cluster-bootstrap 95% CI > 0) over a baseline logistic model with the best popularity indicator, early off-home
  volume, share and field-group composition, off-home growth, early reach/entropy, the Cheng-style resonance set, the Hawkes
  branching ratio and the background log-odds ratio. The random-effects pooled delta-AUC is > 0, with the same sign in >=
  3 of 4 held-out groups plus the cohort. The direction holds for author-labelled and venue-labelled O2r. (C2, not a relabel)
  On dev, |Spearman(A*_h, log off-home growth)| <= 0.5 and |Spearman(A*_h, log off-home n)| <= 0.5, and the held-out gain
  survives adding both to the baseline. Naive R_away is expected to fail this diagnostic (Spearman > 0.85), which is reported
  as a finding about reproduction-number indicators. MEASUREMENT RESULT (reported whatever C1 shows). (M1) Background homophily
  explains >= 50% of the between-concept variance of the raw concept lineage log-odds ratio on dev. The probe predicts this:
  background >= concept term in 6 of 8 concepts. SECONDARY (Holm-corrected across C3-C6). (C3, P2) Within the top tercile
  of early entropy, A*_h separates persistent from transient (O3) concepts with AUC >= 0.68. (C4, P3) A*_h's delta-AUC is
  larger for O2r than for O1 and O5, and the best popularity or co-occurrence indicator's delta-AUC is larger for O1/O5 than
  for O2r (paired bootstrap); this dissociation claim concerns the size-adjusted O2r. (C5, P4) With calibrated detectors,
  the gap closes before entropy take-off in >= 60% of broad concepts (sign test), the lead-lag coefficient A*_h(t) -> Delta
  entropy(t+1) is positive and larger than the reverse, and the permutation placebo is null. (C6, P5) The off-home share under
  primary_topic labels is >= 30% (relative) lower than under venue and author labels for method concepts, and significantly
  more so than for object concepts. PORTABILITY (reported with C1): a dev-frozen logistic model P(O2r top tercile | A*_h)
  has held-out calibration slope in [0.7, 1.3] in >= 3 of 4 groups. PARTIAL: C1 holds pooled but fails in some groups. If
  coverage- or label-coverage-stratified analysis explains the failure, it is reported as a measurement boundary; otherwise
  as a domain boundary. Also PARTIAL: C1 and C2 hold but C5 fails, i.e. naturalisation predicts but does not come first. DISCONFIRMED:
  the pooled delta-AUC CI includes 0; or A*_h works only in CS/AI; or A*_h adds nothing over the background term alone; or
  the bibliographic-coupling A*_h disagrees with the citation A*_h (Spearman < 0.4). Even then the paper reports the full
  indicator x outcome x field matrix, M1, the label-bias result and the empirical RQ2 trajectory taxonomy.
related_works:
- >-
  Cheng, Smith, Ren, Cao, Smith & McFarland (2023, American Sociological Review 88(3)), 'How New Ideas Diffuse in Science':
  about 60k new concepts in WoS. Ideas become core when they reach unrelated author networks, are used consistently, and fit
  prominent ideas and traditions. This is the closest large-scale competitor. Its predictors are social and semantic resonance.
  Ours is a background-adjusted, discipline-resolved lineage contrast. Their predictors enter as family I, and A*_h must add
  signal beyond them on held-out fields.
- >-
  Rinia, van Leeuwen, Bruins, van Vuren & van Raan (2002, Scientometrics 54:347-362), 'Measuring knowledge transfer between
  fields of science', and Yan, Ding, Cronin & Leydesdorff (2013, J. Informetrics 7:249-264), 'A bird's-eye view of scientific
  trading': field-level cross-disciplinary citation, import/export and 'discipline self-dependence' indices. A*_h is the same
  family of statistic (an E-I / layer-assortativity index), made conditional on one concept and adjusted by the same papers'
  background citing. It is used as an early predictor of that concept's integration, not as a description of a field.
- >-
  De Domenico, Omodei & Arenas (2016, Applied Network Science 1:15), 'Quantifying the diaspora of knowledge in the last century':
  whole disciplines are classed as knowledge sources or sinks from researcher mobility. Our analysis is concept-specific and
  time-varying: the same field can be naturalised for one concept and borrowing for another.
- >-
  Maillart, Chataing et al. (2026, arXiv 2606.03919), 'Forecasting Conceptual Diffusion in Science: The Case of Quantum Computing':
  OpenAlex concept-pair co-occurrence with upstream and downstream citation environments. Exogenous diffusion is predictable;
  endogenous reinforcement reduces to proportional growth. Their work covers one domain and concept pairs. Their growth finding
  is why our headline is an odds-ratio contrast pre-registered against growth and volume.
- >-
  Ciotti, Bonaventura, Nicosia, Panzarasa & Latora (2016, EPJ Data Science), 'Homophily and missing links in citation networks',
  together with general citation-homophily work: papers cite similar papers well above chance. This is the regularity that
  the background term nets out. The probe shows it dominates raw concept lineage assortativity (M1).
- >-
  Explainable forecasting of scientific breakthroughs from OpenAlex concept-network dynamics (arXiv 2606.03864; 59 topological
  and semantic features, LightGBM), and Shi & Ma (2026, SSRN 7276909), 'Tracing and Forecasting Frontier Trajectories in Evolving
  Knowledge Networks' (association-strength trajectories of concept pairs against null models): both are link-level co-occurrence
  forecasting. Their strongest features enter families B-E as rivals. Neither uses lineage structure across discipline layers.
- >-
  Kiss, Broom, Craze & Rafols (2010, J. Informetrics) and Bettencourt et al. (2006 Physica A; 2008 Scientometrics): epidemic
  models of idea spread with an aggregate R0. The naive citation next-generation matrix is kept only as a foil, because R-type
  indicators are functions of growth rate (Wallinga & Lipsitch 2007).
- >-
  Multivariate Hawkes processes (Hawkes 1971; Bacry, Mastromatteo & Muzy 2015): the branching matrix is the likelihood-based
  analogue of a next-generation matrix. Used as competitor family J on per-field counts, to test whether citation attribution
  adds anything to self-excitation in counts.
- >-
  Weng, Menczer & Ahn (2013, Scientific Reports), community structure and virality: early spread across many communities predicts
  virality. This is the reach/entropy rival that P2 targets by matching on early entropy.
- >-
  Salatino, Osborne & Motta (2017, PeerJ CS), 'How are topics born?', and AUGUR (2018): topic birth is anticipated by rising
  collaboration density between parent areas. Included in families B-E. It concerns birth, not cross-field naturalisation.
- >-
  Rotolo, Hicks & Martin (2015, Research Policy), 'What is an emerging technology?': five attributes. Used as the conceptual
  baseline. Our outcomes separate uptake, size-adjusted breadth and transience, and P3 predicts they have different early
  signals.
- >-
  Chen (2012, JASIST), structural variation and CiteSpace betweenness bursts; Leydesdorff & Rafols (2011, JASIST), 'Local
  emergence and global diffusion of research technologies': bridging and qualitative local-to-global patterns. Our RQ2 derives
  trajectories quantitatively and tests a pre-registered ordering with power-matched detectors.
- >-
  'Multiplex flows in citation networks' (Applied Network Science 2017) and 'Knowledge transfer, knowledge gaps, and knowledge
  silos in citation networks' (2024/25): multilayer and community framings of knowledge flow that are descriptive, not predictive.
  They motivate the multilayer framing, to which we add a concept-level, homophily-adjusted, held-out-validated predictor.
- >-
  SciTraj (arXiv 2606.22342), claim-grounded typed citations across NLP, ML and CV, finds disciplinary siloing in research
  relations. It is a possible future edge-typing for our lineage network (a 'uses' versus 'mentions' edge split), not a competitor
  for cross-domain prediction.
- >-
  'Beyond borrowed concepts: entropy's half-century cross-disciplinary journey between physics and economics' (Scientometrics
  2026) and 'How academic hot topics emerge: a bipartite mutualistic network analysis' (Scientometrics 2026): a single-concept
  semantic case study of a borrowed concept, and system-level nestedness transitions in AI. We make the borrowed-versus-practised
  distinction measurable across fields.
inspiration: >-
  Three imports, each used as a method rather than a metaphor. (1) Invasion biology: in the introduction-naturalisation-invasion
  continuum (Richardson et al. 2000; Blackburn et al. 2011), 'casual' aliens persist only through repeated introduction, while
  naturalised ones recruit from local stock. Recruitment provenance, not presence, is the diagnostic, and our lineage contrast
  is its network form. (2) Epidemiology's negative-control exposure and self-controlled designs (Lipsitch, Tchetgen Tchetgen
  & Cohen 2010; case-crossover designs): compare the same units' behaviour on a control exposure to remove unmeasured confounding.
  Here the control exposure is the same papers' non-concept references, which absorbs disciplinary homophily without modelling
  it. (3) Margin-free association in categorical data analysis: the odds ratio of a mixing table does not change when rows
  or columns are rescaled. That is why stock availability and preferential attachment to seminal home papers cancel when home
  and off-home adopters face the same stock. The review's critique, backed by our own probe, turned the question from 'do
  adopters cite each other more than chance?' (they do, mostly because every field cites itself) into 'does the concept's
  lineage follow the adopters' own field boundaries as their normal literature does?'. A measurement lesson carries over:
  paper-level topic classifiers read the paper's own references and text, so discipline must come from where a paper appears
  (features) or who writes it (outcomes).
terms:
- term: Concept-paper
  definition: >-
    A publication whose title or abstract contains the concept's name, an alias or a lemma variant (local matching on downloaded
    text), and which passes the sense filter trained on the labelled grounding benchmark.
- term: Onset (t0) and newborn concept
  definition: >-
    t0 is the first year with >= 20 grounded papers, where each of the three previous years has fewer than 25% of the t0+2
    count. Concepts that fail this rule are re-emerging terms and are analysed separately. All size filters use years <= t0
    only.
- term: Home field(s)
  definition: >-
    Field(s) (26-field level, venue labels) holding >= 40% of a concept's first 30 grounded papers. For multi-home concepts,
    all home fields count as home.
- term: Venue label / team profile / author label
  definition: >-
    Venue label: dominant field (>= 40%) of the topic profile of the first non-repository source hosting the work, used for
    features. Team profile: the field distribution of all the paper's authors' works published before that year, from one
    group_by call; a leakage-free sensitivity label. Author label: majority field of the authors' career profiles, used for
    outcomes. Paper primary_topic is used only for the P5 bias check.
- term: Concept lineage multilayer network
  definition: >-
    For one concept, nodes are its papers, layers are venue fields, and edges are citations to earlier papers on the same
    concept within 3 years. Edges between papers that share an author form a separate self-lineage channel.
- term: Naturalisation gap A*_h
  definition: >-
    The Mantel-Haenszel log odds ratio of the concept's citing-layer x cited-layer (off-home/home) mixing table, minus the
    same log odds ratio computed on the same citing papers' other references. Negative means borrowed (adopters cite the concept
    across field lines more than they cite anything else across field lines). Near or above zero means naturalised. It is
    a concept-conditional, background-adjusted disciplinary self-citation (layer-assortativity) index.
- term: rho*_j and naturalisation event
  definition: >-
    rho*_j is the same contrast for one field j (child in j or not x parent in j or not, minus background). A naturalisation
    event is the first upward change point in rho*_j, or in A*_h, found by the shared change-point detector calibrated to
    a 5% false-alarm rate on non-diffusing dev concepts.
- term: Background homophily term
  definition: >-
    The log odds ratio of the same citing papers' non-concept references (off-home/home by venue field). It is a negative-control
    exposure for general disciplinary citing habits.
- term: A*_unif, A*_imp, naive R_away
  definition: >-
    Earlier or foil indicators, all kept in family G. A*_unif is the off-home-to-off-home citation share against a uniform
    availability null. A*_imp weights availability by 1 + in-citations. R_away is the spectral radius of the off-home block
    of a citation next-generation matrix, which is approximately off-home growth.
- term: O2r rarefied breadth
  definition: >-
    The expected number of distinct fields among m = 50 randomly drawn concept-papers in t0+6..t0+8 (exact hypergeometric
    rarefaction). It is volume-adjusted, and it is the primary breadth outcome. O2-raw (fields with >= 5 papers a year for
    3 years) is secondary.
- term: O1 uptake, O3 transience, O5 recognition
  definition: >-
    O1: field-normalised share in years 6-8 is at least the year-5 share. O3: peak in t0+3..t0+8 with peak / mean(t0+7..t0+8)
    >= 2. O5: MeSH descriptor introduced after t0, a Research Fronts listing, or a Wikipedia article created by t0+8.
- term: Frames N and W
  definition: >-
    N: outcome-blind candidate phrases mined from random samples of each year's titles. W: legacy OpenAlex concepts with Wikidata
    IDs (a known selection condition). W is reweighted by inverse inclusion probability if its base rates differ from N's.
- term: M1 decomposition
  definition: >-
    The share of between-concept variance in the raw concept lineage log odds ratio that is explained by the background homophily
    term. It measures how much of 'lineage autonomy' is merely which fields adopt.
summary: >-
  We test whether a new concept spreads for good once the fields that adopt it cite its literature the way they cite their
  own, measured as a naturalisation gap. The gap is the concept's lineage odds ratio across discipline layers minus the same
  papers' background citation homophily, so availability, preferential attachment and field insularity cancel out. A probe
  on 8 concepts shows that most raw 'lineage autonomy' is general homophily and that early adoption is usually borrowed. On
  held-out fields and a later cohort, how early and how far the gap closes should predict size-adjusted, lasting breadth better
  than growth, centrality and reach, and it should close before entropy takes off.
alternates:
- title: Unconnected author groups carry concepts far
  hypothesis: >-
    Size-adjusted broad integration is anticipated by the SOCIAL structure of early adoption, not by citation lineage. The
    measure is the number of mutually unconnected coauthorship components among off-home early adopters, normalised by adopter
    count (Cheng et al.'s 'unrelated authors', resolved by discipline). It beats A*_h, reach and centrality on held-out fields.
  why_it_could_win: >-
    Concepts may travel mainly through people and shared tools that are used without citing earlier concept-papers. Then coauthorship
    records transmission that lineage misses, especially in low-coverage fields such as the social sciences.
- title: Diverse entry points beat many neighbours
  hypothesis: >-
    On the concept-level co-occurrence backbone, the structural diversity of a concept's newly acquired neighbours best anticipates
    O2r across held-out fields. Structural diversity is the number of distinct Leiden communities its new ties reach, following
    complex-contagion theory. It beats degree growth, betweenness, entropy and A*_h, and fast-growing concepts whose new ties
    stay in one dense neighbourhood remain local.
  why_it_could_win: >-
    If integration depends on recombination with unrelated ideas rather than on adopters building their own literature, co-occurrence
    diversity will lead. It also needs no reference lists, so it would dominate where lineage and venue-label coverage are
    poor.
- title: Where a concept lands matters most
  hypothesis: >-
    Breadth is decided by WHICH fields adopt early, not by how they adopt. Early reach into high-relatedness 'gateway' fields
    on the subfield backbone (e.g. Computer Science, Mathematics, Biochemistry), together with the adopters' general insularity
    (the background homophily term), predicts O2r and the next field entered better than A*_h (principle of relatedness from
    economic complexity).
  why_it_could_win: >-
    The probe shows that background homophily is large and varies strongly by field. If concept-specific naturalisation is
    just noise around field composition, the composition and gateway terms will carry all the signal, and A*_h will add nothing
    once they are in the baseline.
- title: Frequency-free selectivity is the portable signal
  hypothesis: >-
    Most network indicators fail to generalise because they inherit field size and growth. Indicators expressed against frequency-matched
    nulls (PMI selectivity growth, new-neighbour novelty against a degree-preserving expectation) keep their rank on held-out
    fields and predict both uptake (O1) and breadth (O2r). Raw degree, strength and centrality rank well only where they were
    tuned.
  why_it_could_win: >-
    If the main cross-domain failure is baseline confounding rather than a missing mechanism, null-residualised co-occurrence
    indicators will generalise as well as A*_h. They are cheaper and have full coverage, and there would be no uptake-versus-breadth
    dissociation.
_relation_rationale: >-
  Consolidation account (naturalisation, retained frontier) failed decisive tests; Exp8 held-out shows openness wins
_confidence_delta: decreased
_key_changes:
- >-
  Headline moves from the RETAINED FRONTIER (closed) to OPENNESS VS CONSOLIDATION, built from the Exp8 held-out lead: new_edge_rate
  +0.118, n_comm_W3 +0.167, participation +0.150, NOV_res +0.139, ego_density -0.102, edge_persistence -0.080 (P2 holds),
  RETENTION_RATIO_early -0.12 (P4 reversed).
- >-
  Retained frontier closed. The volume-matched R-minus-N contrast is null on DEV (-0.0085) and held-out (-0.028). The held-out
  dose is not monotone (0.098/0.075/0.304). Under Hidalgo min-cp proximity, which fits better (AUC 0.866 vs 0.852), d0 reverses
  (-0.021, p 0.012). What survives is the relatedness principle, which is not new.
- >-
  Abandonment penalty closed as specification-dependent: A1 -0.007 (null), R4 +0.064, min-cp -0.030 (p 1e-4), target-field
  FE -0.044.
- >-
  Fresh confirmation body: a 2015-16 onset cohort from one new zero-credit snapshot pass, never screened. The whole EXP5 frame
  is now selection data, frozen and hash-sealed first. A fallback to 2017 onsets is declared in advance.
- >-
  Confounds attacked head-on: a HOME-ONLY ego-network build (no mechanical coupling to off-home spread), LLM-labelled concept
  type (method vs object), pre-onset footprint, CONTACT_REACH, label coverage and home FE. OPEN must also hold within each
  concept type.
- >-
  RQ2 timing test replaces the MIXED ordering result: within-concept home-only closure -> next-year entry hazard (concept
  and year FE), with the reverse path, an event study with pre-trends, and a placebo.
- >-
  The failed RQ2 artifact (gen_art_experiment_9, never executed) is re-run on the existing EXP5 arrays. Its pre-registration
  is inverted: localised vs integrating concepts differ more in contact/exploration than in retention. The DTW-HMM ARI >=
  0.5 naming rule stays. The home-prominence-before-diffusion vs intersection-born test is added.
- >-
  Why-it-works decomposition (where new partners come from: method vs domain communities, bridging papers), matched-pair case
  studies from the extremes, and an AI/CS atlas of about 40 concepts as the request's stage-1 inspection.
- >-
  Secondary leads replicated on the fresh cohort: the O3 L1-logit (+0.093 AUC over a B5 at chance), n_authors_early (O3/O1b/O1c),
  the O4 EBM (0.188 vs 0.015) and the O2r ElasticNet (+0.059).
- >-
  M0_density_end and D_vol_end reclassified as partly pre-onset footprint and re-scored post-onset only. Candidate S recorded
  as tested and not confirmed. O5 closed as a validation outcome, with per-source leakage.
- >-
  Record corrections mandated by the reviewer: O4/O3 relabelling, exact P1-P5 verdicts (new_edge_rate transfers, correcting
  dead end 7.4), Exp7 tables from step2 JSONs, the 14 Eval2 text corrections, real artifact ids, Exp9 recorded as failed,
  and trajectories/ordering/H3 moved to not established.
_strands:
- artifact: art_22ppE1snfHKj  state: 'null'
  why: >-
    Deepened lead fails its novel part: volume-matched R-N contrast -0.028 [-0.105,0.046] (DEV -0.0085); under better-fitting
    Hidalgo min-cp proximity d0 -0.021; dose non-monotone
- artifact: art_dFQ6jbgNsR6Q
  state: lead
  why: >-
    Held-out psp|B5: new_edge_rate +.118, n_comm +.167, ego_density -.102, RETENTION_RATIO -.12; concept-type/footprint confounds
    untested, I2 up to .78, LIFEENV weak
- artifact: art_7W9xiIO3FVBs
  state: 'null'
  why: >-
    Audit only: 224/246 claims match, ordering rewritten MIXED; O5 unrelated to O2r (rho 0.014) and O1 (0.001), 67% recognised
    <= t0. No new effect to build on.
- artifact: art_EesdB8cuSfcU
  state: 'null'
  why: >-
    Positioning only: retained-density claim partially anticipated; no test executed. Its 'missing' D_rca_persist rival was
    already in Exp7 S_strict.
_evidence_state: lead
_move: deepen
_move_rationale: >-
  Best strand is the Exp8 lead (open neighbourhoods predict breadth held-out). Deepen it: fresh 2015-16 cohort, home-only
  build, concept-type/footprint controls, within-concept timing.
_coverage: full
_coverage_statement: >-
  Next iteration answers RQ1 (which network signals transfer, confirmed on a fresh never-screened cohort, with why-it-works
  and learned models) and RQ2 (re-run trajectory typology, contact-vs-retention decomposition, home-prominence-vs-intersection
  sequence test, case studies).
_candidates_considered: 12
relation_type: replacement
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for study design, proper baselines, and the evaluation/validity norms this field demands.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<domain_reasoning>
FIRST WORK OUT HOW RESEARCHERS IN THIS FIELD REASON. Then choose the strategy.

The hypothesis names a field. Before proposing anything, establish how people
who publish in that field actually think — not research advice in general,
which holds everywhere and so settles nothing here.

Answer these four, for THIS field:

1. PRINCIPLES. What does the field take as given, and what does it still
   argue about? What has to be true of a study before anyone in it will read
   the result at all?
2. WHAT COUNTS AS CONVINCING. What kind of evidence makes a claim believed
   here — an effect on held-out cases, a controlled comparison, a replication
   across populations, a proof, a mechanism shown rather than correlated, a
   preregistered prediction that came true? Fields disagree about this, and
   the disagreement is what a strategy has to be built around.
3. STANDARD MOVES AND THEIR RATIONALE. Which methodological moves does a
   competent group reach for first, and what does each one EXIST to rule out?
   A move whose purpose you cannot state is a ritual, and copying it will not
   protect the result.
4. USUAL FAILURE MODES. How does work in this field normally go wrong —
   the confound everyone forgets, the measure that drifts from the construct,
   the baseline that was never tuned, the result that never replicates, the
   sample too small to carry the claim?

HOW MUCH EFFORT. This is a bounded step, not an artifact. Read the one domain
handbook that fits (if one does), and run a handful of targeted lookups on how
the field states its own norms — a review, a methods paper, a reproducibility
or replication study, a venue's reviewer guidance. Then stop and plan. If no
handbook and no clear norms exist for this field, say so plainly in
`domain_reasoning` and treat every principle you name as provisional.

WHAT TO WRITE.
- `domain_reasoning`: the four answers above, specific to this field, in a few
  sentences each. Name the field. Cite what you actually read. Anything you
  could have written without knowing which field this is does not belong here.
- `principle_alignment`: which of those principles THIS strategy follows and
  how, and which it deliberately BREAKS, with the reason each break is worth
  it and what you are doing instead to keep the result credible. Breaking a
  principle on purpose is a legitimate move and is sometimes the contribution
  itself — an unnamed break is the failure. "Follows all of them" is an
  answer only when it is true; say which ones and where.

The strategy that follows has to be the one this reasoning implies. If the
field's own standard of evidence rules out the cheap version of your idea,
plan the version it does not rule out.
</domain_reasoning>

<iteration_status>
Current iteration: 4 of 5
Remaining (including this one): 2
</iteration_status>

<candidate_alternates>
Runner-up answers to the same ask, carried from hypothesis generation. These are the
candidate population a wide screen draws on — treat them as real options, not as context.

--- Candidate 1 ---
title: Unconnected author groups carry concepts far
hypothesis: >-
  Size-adjusted broad integration is anticipated by the SOCIAL structure of early adoption, not by citation lineage. The measure
  is the number of mutually unconnected coauthorship components among off-home early adopters, normalised by adopter count
  (Cheng et al.'s 'unrelated authors', resolved by discipline). It beats A*_h, reach and centrality on held-out fields.
why_it_could_win: >-
  Concepts may travel mainly through people and shared tools that are used without citing earlier concept-papers. Then coauthorship
  records transmission that lineage misses, especially in low-coverage fields such as the social sciences.

--- Candidate 2 ---
title: Diverse entry points beat many neighbours
hypothesis: >-
  On the concept-level co-occurrence backbone, the structural diversity of a concept's newly acquired neighbours best anticipates
  O2r across held-out fields. Structural diversity is the number of distinct Leiden communities its new ties reach, following
  complex-contagion theory. It beats degree growth, betweenness, entropy and A*_h, and fast-growing concepts whose new ties
  stay in one dense neighbourhood remain local.
why_it_could_win: >-
  If integration depends on recombination with unrelated ideas rather than on adopters building their own literature, co-occurrence
  diversity will lead. It also needs no reference lists, so it would dominate where lineage and venue-label coverage are poor.

--- Candidate 3 ---
title: Where a concept lands matters most
hypothesis: >-
  Breadth is decided by WHICH fields adopt early, not by how they adopt. Early reach into high-relatedness 'gateway' fields
  on the subfield backbone (e.g. Computer Science, Mathematics, Biochemistry), together with the adopters' general insularity
  (the background homophily term), predicts O2r and the next field entered better than A*_h (principle of relatedness from
  economic complexity).
why_it_could_win: >-
  The probe shows that background homophily is large and varies strongly by field. If concept-specific naturalisation is just
  noise around field composition, the composition and gateway terms will carry all the signal, and A*_h will add nothing once
  they are in the baseline.

--- Candidate 4 ---
title: Frequency-free selectivity is the portable signal
hypothesis: >-
  Most network indicators fail to generalise because they inherit field size and growth. Indicators expressed against frequency-matched
  nulls (PMI selectivity growth, new-neighbour novelty against a degree-preserving expectation) keep their rank on held-out
  fields and predict both uptake (O1) and breadth (O2r). Raw degree, strength and centrality rank well only where they were
  tuned.
why_it_could_win: >-
  If the main cross-domain failure is baseline confounding rather than a missing mechanism, null-residualised co-occurrence
  indicators will generalise as well as A*_h. They are cheaper and have full coverage, and there would be no uptake-versus-breadth
  dissociation.
</candidate_alternates>



<latch_iteration>
THIS ITERATION LATCHES ONTO WHAT ALREADY WORKED.

The previous round produced something real — a genuine positive, or a lead
worth making bigger — and the revision's move is `deepen`, `extend` or `fix`
(`_move` on the hypothesis). So the OBJECT of this iteration is already
fixed: it is that result. Not a wider title, not a new question.

Spend EVERY artifact slot attacking that same object from a different side:

- MECHANISM — why it holds; what would have to be true for it to hold; the
  intermediate the effect travels through.
- BOUNDARY — the condition, size, regime or population where it stops.
- CONFOUND — the alternative account a reviewer names first, tested head-on
  so that it can actually lose.
- REPLICATION — the same claim on a SECOND family, population, period,
  corpus, site, cohort or case set the first result never touched.
- FIX — a strand that came back broken, run correctly, claim unchanged.
- If the object is a LEAD rather than a genuine positive: MORE POWER and a
  CLEANER MEASURE, so the next round can tell a real effect from a small one.
  When a power analysis or the effect sizes already on record say the panel
  cannot detect an effect this size, that budget buys more graded samples or
  checkpoints — not more candidate metrics. A wider panel of readouts over
  the same underpowered set does not change what the numbers can tell you.

Strands that came back null last round are CLOSED: one sentence in the paper,
no artifact here. Do not re-run them, do not widen away from a result that
worked, and do not spend a slot on an unrelated new candidate — that is what
a widen iteration is for, and this is not one.
</latch_iteration>

<previous_strategies>
Strategies from the PREVIOUS iteration. You can CONTINUE these directions,
ADAPT based on what worked and what didn't in the artifacts produced, or PIVOT if results suggest a better path.

--- Strategy 1 ---
kind: strategy
id: gen_strat_1_idx1
domain_reasoning: >-
  Field: scientometrics and science of science with network-science methods. Target venue: Applied Network Science (ANS; the
  Springer collection named in the request, which research art_dxvRpQufMR0e could only read as scope text). (1) PRINCIPLES
  TAKEN AS GIVEN. Emergence has no single ground truth (Rotolo, Hicks & Martin 2015), so an indicator is believed only if
  early data predict SEVERAL later outcomes (uptake, rarefied breadth, persistence, citations, external recognition) on held-out
  fields and a later cohort, beyond count baselines. Fields differ in size and citation habit, and papers cite their own field
  far above chance (this run: background homophily explains 66-72% of raw lineage variance). So raw breadth relabels volume
  unless it is rarefied or residualised. The default account of diversification is the principle of relatedness (Hidalgo et
  al. 2007, 2018; Guevara et al. 2016 'research space': entry AUC 0.68-0.90; Neffke et al. 2011 and later exit studies credit
  relatedness for survival too). Standard density is computed on the RCA > 1 portfolio, which already filters out tiny presences.
  So a claim that PERSISTENT adoption, not presence, drives the next entry must beat RCA density, a volume-weighted density
  and target size head-on, and must show that a lost presence differs from a kept one. (2) WHAT COUNTS AS CONVINCING in this
  field. Conditional-logit or hazard models on risk sets with concept-level strata. Label and backbone permutation nulls (degree-preserving
  rewiring rules out 'any hub works'). A placebo that keeps the footprint and scrambles persistence rules out 'retained just
  means big'. Dose-response across persistence age. Replication on a body of evidence the lead never touched. Heterogeneity
  reported with I2, not averaged away. (3) KNOWN FAILURE MODES, observed in this run. Indicators that relabel volume. Selection
  and scoring on the same concepts (iteration 2's H3 shrank from 0.14 on DEV to 0.03 on held-out). Fixed-prediction CIs that
  understate uncertainty. Frames that disagree across artifacts: EXP5 and EXP6 used different grounding and episode rules,
  so the common panel was never built. Truncated source lists. Lead-lag claims made without checking pre-trends (the ordering
  result has a significant pre-trend and a significant reverse path on DEV). A record whose sentences contradict its own result
  files (the review scored soundness 1 for this). (4) STANDARD MOVES and what each rules out: field fixed effects and leave-concept-out
  propensities (field traits); concept strata (concept traits and survivorship of named concepts); rarefaction and O2r_resid
  (volume); a temporal cohort with a feature-outcome gap (leakage); Holm and DL pooling (multiplicity and domain averaging).
  No domain handbook covers this field, so these rest on the cited sources and this run's own measurements, and are held provisionally.
principle_alignment: >-
  FOLLOWS. (a) The rival standard model is the baseline: every frontier test nests M0 -> +D_rca -> +D_vol -> +d0_ret_rel ->
  +d_lost, so the claim must beat conventional RCA relatedness density, not a straw man. (b) Confirmation is independent:
  the frontier claim is re-tested once on the EXP5 frame MINUS every EXP6 concept, a body of evidence the lead never touched,
  frozen on DEV and hash-sealed. The EXP6 re-analysis is labelled robustness only. (c) Specificity nulls: a within-concept-year
  retained-label permutation, a volume-matched persistence contrast, persistence-age dose, a rewired backbone and intersection-born
  exclusion. (d) RQ1 is finally delivered the way the user specified: 30-50 indicators from different families plus simple
  count references; a top 10 per outcome selected on DEV only and scored once on held-out groups and the cohort; per-group
  and pooled results; domain-specific failures (CS-only growth indicators) reported as negative results. (e) Several ground
  truths, including INDEPENDENT external recognition (O5: MeSH, Wikipedia/Wikidata, dated taxonomies), with a Wikipedia/Wikidata-only
  variant for groups without a dated taxonomy. (f) One frame (EXP5), one fold assignment and one outcome table across all
  three experiments, which closes the common-panel gap. (g) RQ2 classes are named only if two independent methods agree (DTW
  k-medoids vs HMM, ARI >= 0.5) and the class survives excluding Medicine homes; otherwise a continuum is reported. (h) The
  record is repaired before the paper: a claims ledger ties each sentence to a file and value. BREAKS ON PURPOSE. (1) No new
  frame and no API use. All state, frontier and family-F work reuses EXP5's cached concept x year x field counts (agg_counts.parquet),
  because the API key is exhausted and the cache already covers the frame. What is NOT cached (concept-topic ego networks,
  citations, author IDs) gets exactly one targeted pass over the free snapshot, re-using EXP5's matcher and grounding. The
  pass is checked against agg_counts before use. If it does not fit the time budget, the dependent rows (O4, candidate S)
  are dropped and logged, not approximated.(2) The concept vocabulary stays the legacy Wikidata-linked OpenAlex concepts (survivorship:
  a concept had to be named by about 2019). Within-concept strata neutralise this for entry tests; for concept-level RQ1 it
  is a stated limitation, partly offset by O5 and by the 2010-2014 cohort. (3) Three experiments run in parallel on the same
  frame without depending on each other, so the D3 definitions are copied verbatim into each, and the evaluation checks that
  they agree.
title: New ideas spread from fields that kept them
objective: >-
  Deliver the validated framework the task asks for, in three linked claims, each scored once on sealed held-out fields and
  a later cohort. (RQ1) Which of 30-50 temporal network indicators anticipate emergence, defined by several outcomes including
  independent external recognition, beyond simple count baselines, and which of them are portable across domains versus field-specific.
  (RQ2, main claim) Concepts spread across disciplines from their RETAINED FRONTIER: the next field a concept enters is predicted
  by its relatedness to fields that have KEPT it, beyond conventional RCA relatedness density, share-weighted density, target
  size and relatedness to home. Relatedness to fields that DROPPED it lowers entry (the abandonment penalty). (RQ2, trajectories)
  Locally concentrated and broadly integrated concepts differ mainly in RETENTION PROBABILITY per contacted field rather than
  in contact rate. Recurring trajectories are derived empirically and named only if two methods agree. The mechanism is shown
  in case studies and a lineage check of retained versus lost adopters.
rationale: >-
  Iteration 2 closed the gateway-centrality idea at scale (EXP5: held-out dAUC -0.00001 on 27,393 episodes, absorbed by the
  field's own retention propensity; EVAL1: the iteration-1 +0.10 does not beat a shuffled-R placebo). It also produced one
  strong lead: in EXP6's held-out conditional logit (369 concepts, 1,373 entry events), relatedness to RETAINED fields adds
  +0.281 per SD (SE 0.032, LR 68.6, permutation p 0.001, rewired p 0.015, I2 0). A dropped field shows a hint of a penalty
  (d_lost -0.063, p 0.055). The lead has not yet faced the obvious rival: standard relatedness density is computed on RCA-thresholded
  portfolios, which already favour sustained presences. It lives on one frame only, and its AUC gain is small (0.809 to 0.817).
  The review also blocked on record soundness (score 1) and on missing coverage. The RQ1 30-50 indicator screen with top-10
  held-out validation, O5 external recognition, the case studies and the learned model are all still absent, and the user
  requires them. The updated hypothesis moves to DEEPEN with lower confidence, so this iteration buys both a decisive test
  and completeness. (1) The decisive frontier test: the RCA/volume ladder, independent confirmation on EXP5-minus-EXP6, specificity
  nulls and the abandonment penalty. (2) The RQ1 held-out matrix with O5 and a learned model. It is independent of the frontier's
  fate and is the paper's main RQ1 table. (3) RQ2 trajectories and the mechanism, rebuilt on state sequences, with the ordering
  claim tested properly. (4) A record-repair and cross-frame agreement evaluation that clears the review's blocking items
  and validates O5 as a ground truth. (5) Research that turns the result into an ANS paper: prior art for the frontier and
  abandonment claims, per-RQ comparison numbers and the methodology figure. Everything reuses cached snapshot data at zero
  API credits. INFORMATIVE EITHER WAY: if D_rca absorbs the frontier effect, the paper reports that the relatedness principle
  holds unchanged for single concepts and that persistence adds nothing beyond RCA. The RQ1 matrix and trajectories stand
  alone.
artifact_directions:
- id: experiment_iter3_dir1
  type: experiment
  objective: >-
    Decisive test of the retained-frontier claim (RQ2 main claim) and the abandonment penalty. (a) ROBUSTNESS on EXP6's sealed
    risk sets: does d0_ret_rel survive conventional RCA > 1 relatedness density and share-weighted density? (b) INDEPENDENT
    CONFIRMATION, scored once, on the EXP5 frame minus every EXP6 concept: held-out groups PHYS / LIFEENV / SOC / MATHDEC
    (MATHDEC testable for the first time) and the 2010-2014 cohort. (c) SPECIFICITY: is it persistence, not volume or footprint,
    that carries the signal?
  approach: >-
    INPUTS ARE READ BY PATH from the run tree (relative to the run root). Experiments may formally depend only on dataset
    or research artifacts, so earlier experiments are reused by path, not as dependencies. 3_invention_loop/iter_2/gen_art/gen_art_experiment_5/
    (art_wxWssKSUR45f): frame_concepts.csv (12,499 concepts, TAG grounding + LLM precision gate), episodes.csv (27,393), concept_outcomes.csv,
    concept_features_basic.csv, frozen_spec.json (split and fold assignment), scan/agg_counts.parquet (concept x year x venue-field
    x tag-state counts, 19.7M rows: the source of every state matrix), scan/year_field_totals.npz, scan/co_by_year.npz (yearly
    26 x 26 FIELD co-occurrence, not concept-level), scan/reservoir/ (sampled matched rows with snapshot file/row pointers),
    results/source_field.parquet, rangefile.py, scan_full.py, matcher.py, grounding.py. 3_invention_loop/iter_2/gen_art/gen_art_experiment_6/
    (art_N-mpomDZZ1ln): lib/h2.py (states(), the frozen ENTERED/RETAINED/LOST definitions), lib/traj.py, lib/stats_core.py,
    results/entry_risk_sets_dev.parquet and entry_risk_sets_heldout.parquet, results/frame_concepts.csv, heldout_result.json,
    dev_result.json, trajectories_*.csv, ordering_*.csv, inputs/field_backbone.json (26-field positive-PMI backbone, 1998-2002).
    3_invention_loop/iter_1/gen_art/gen_art_experiment_3/ (art_yrradSC27HtQ): features.py (concept ego network = the OpenAlex
    TOPICS carried by a concept's matched works, placed on full-corpus topic co-occurrence backbones), backbone/slice0-2.npz
    (topic PMI slices 2000-04, 2005-09, 2010-14), scan_snapshot.py and results/exploratory_partial_association.json. NO concept-topic,
    work-ID, citation or author cache exists for the EXP5 frame. Anything that needs one requires ONE targeted pass over the
    free snapshot (EXP3 streamed 7 columns of 476M works in 17 min), re-using EXP5's matcher and grounding unchanged so that
    the frame is identical. If the run volume is not mounted on the executor, re-download the public zero-credit OpenAlex
    S3 works snapshot with the same range-request code and re-implement from the definitions below, logging every deviation
    in deviations.json. SHARED DEFINITIONS D3 (implement verbatim in every artifact; they are EXP6's frozen lib/h2.py definitions).
    26 venue-label OpenAlex fields; grounded yearly counts n_cj(t). ENTERED(t) = fields with >= 2 cumulative grounded papers.
    RETAINED(t) = off-home fields entered >= 2 years earlier with >= 2 papers in t-2..t. LOST(t) = entered fields with 0 papers
    in t-2..t. phi = the frozen 1998-2002 PMI backbone. d0_ret_rel(c,k,t) = mean phi[j,k] over j in RETAINED(t-1); d_lost
    = the same over LOST(t-1); M0 density = over ENTERED(t-1) (EXP6's M0). D_rca = Hidalgo 2007 / Guevara 2016 density over
    fields with RCA_cj(t-1) > 1, RCA_cj = (n_cj / n_c) / (N_j / N), no persistence requirement. D_vol = share-weighted density
    sum_j s_cj(t-1) phi[j,k] / sum_j phi[j,k]. Home field = field(s) holding >= 40% of the first 30 grounded works (>= 2 =
    intersection-born). SPLIT (unchanged from EXP5's frozen_spec.json): DEV = homes CS, Engineering, BGM, Medicine with onset
    2003-2009; HELD-OUT = homes PHYS, LIFEENV, SOC, MATHDEC with onset 2003-2009 PLUS the 2010-2014 cohort (split into DEV-home
    and non-DEV-home parts). STATISTICS: concept-clustered REFIT bootstrap CIs (>= 1,000 resamples; the model is refitted
    in every resample), crossed concept x field CIs for episode-level tests, DerSimonian-Laird pooling across held-out groups
    with I2, Holm correction inside each pre-declared family. The resampling unit is the concept, and it is named in every
    table. SEALING: every artifact writes frozen_spec.json (formula, covariates, thresholds, indicator list, code SHA-256)
    before any held-out outcome is read, logs its hash, and scores held-out exactly once. BUDGET: 0 OpenAlex API credits (the
    key is exhausted; the snapshot is free); OpenRouter <= $2 per artifact. STEP 1, ROBUSTNESS (EXP6 risk sets, no new scan).
    Rebuild the per-year states from EXP6's cached concept x field x year counts. Fit the nested conditional logit (strata
    = concept-year, alternatives = not-yet-entered fields k): M0 (EXP6's M0: ever-entered density, log target size, relatedness
    to home, target eigenvector centrality) -> M0+D_rca -> +D_vol -> +d0_ret_rel -> +d_lost. Report LR, standardised d, concept-clustered
    refit CIs and within-stratum AUC at every rung, on EXP6 DEV and held-out. This is labelled ROBUSTNESS: evidence already
    seen once. STEP 2, INDEPENDENT FRAME. Take EXP5's frame_concepts.csv, remove every concept ID, every Wikidata QID (via
    the art_O7Dq4L02QnDN QID/label key) and every normalised label that appears in EXP6's frame, and report the overlap count.
    Build year x field state matrices from EXP5's scan/agg_counts.parquet (onset t0 and home from EXP5). Build entry risk
    sets for t0+1..t0+10. On DEV only: check code, convergence, collinearity (VIF of D_rca, D_vol, d0_ret_rel) and power (simulate
    detectable d at 80% power). Then write frozen_spec.json, hash it and score held-out ONCE. STEP 3, SPECIFICITY AND DOSE,
    all pre-declared in the frozen spec. (a) A retained-label permutation within concept-year: shuffle which ENTERED fields
    count as RETAINED, keeping the footprint (1,000 draws). (b) A volume-matched contrast: relatedness to retained fields
    versus to one-off fields with the same t-1 paper count (coarsened exact matching on count bins). (c) Dose: separate terms
    for persistence age 2 / 3 / >= 4 years; prediction: monotone increasing. (d) A degree-preserving rewired backbone (500
    draws). (e) Exclude intersection-born concepts. (f) Sensitivity with min_n = 3 and 5. (g) A field fixed-effects version
    (target-field dummies) to rule out 'some targets are always entered'. STEP 4, ABANDONMENT PENALTY: d_lost given ever-entered
    density, on both frames, pooled across held-out groups; also split LOST by how long the field held the concept before
    dropping it. OUTPUTS: frontier_result.json (every rung, every group, every null, every CI, with the resampling unit named),
    risk_sets_exp5_minus_exp6_{dev,heldout}.parquet, state_panel.parquet (concept x field x year state; the authoritative
    D3 panel for the paper), frozen_spec.json with its hash in logs/seal.log, and figures: a forest plot per group, the ladder,
    and the dose-response. The Guevara 2016 entry AUCs (0.68-0.90) are reported next to ours, flagged where the settings differ.
  what_it_would_show: ''
  depends_on:
  - id: art_O7Dq4L02QnDN
    label: QID/label key for frame de-duplication
    relation_type:
    relation_rationale:
- id: experiment_iter3_dir2
  type: experiment
  objective: >-
    RQ1 held-out deliverable (user steps 2-5 and the optional learned model), on the single EXP5 frame with ONE outcome table
    and ONE fold assignment. Compute a 40-50 indicator matrix from different structural families plus simple count references.
    Select a top 10 per outcome on DEV only. Score it once on held-out home groups and the 2010-2014 cohort against five ground
    truths, including independent external recognition (O5). Report which signals are portable and which are domain-specific.
  approach: >-
    INPUTS ARE READ BY PATH from the run tree (relative to the run root). Experiments may formally depend only on dataset
    or research artifacts, so earlier experiments are reused by path, not as dependencies. 3_invention_loop/iter_2/gen_art/gen_art_experiment_5/
    (art_wxWssKSUR45f): frame_concepts.csv (12,499 concepts, TAG grounding + LLM precision gate), episodes.csv (27,393), concept_outcomes.csv,
    concept_features_basic.csv, frozen_spec.json (split and fold assignment), scan/agg_counts.parquet (concept x year x venue-field
    x tag-state counts, 19.7M rows: the source of every state matrix), scan/year_field_totals.npz, scan/co_by_year.npz (yearly
    26 x 26 FIELD co-occurrence, not concept-level), scan/reservoir/ (sampled matched rows with snapshot file/row pointers),
    results/source_field.parquet, rangefile.py, scan_full.py, matcher.py, grounding.py. 3_invention_loop/iter_2/gen_art/gen_art_experiment_6/
    (art_N-mpomDZZ1ln): lib/h2.py (states(), the frozen ENTERED/RETAINED/LOST definitions), lib/traj.py, lib/stats_core.py,
    results/entry_risk_sets_dev.parquet and entry_risk_sets_heldout.parquet, results/frame_concepts.csv, heldout_result.json,
    dev_result.json, trajectories_*.csv, ordering_*.csv, inputs/field_backbone.json (26-field positive-PMI backbone, 1998-2002).
    3_invention_loop/iter_1/gen_art/gen_art_experiment_3/ (art_yrradSC27HtQ): features.py (concept ego network = the OpenAlex
    TOPICS carried by a concept's matched works, placed on full-corpus topic co-occurrence backbones), backbone/slice0-2.npz
    (topic PMI slices 2000-04, 2005-09, 2010-14), scan_snapshot.py and results/exploratory_partial_association.json. NO concept-topic,
    work-ID, citation or author cache exists for the EXP5 frame. Anything that needs one requires ONE targeted pass over the
    free snapshot (EXP3 streamed 7 columns of 476M works in 17 min), re-using EXP5's matcher and grounding unchanged so that
    the frame is identical. If the run volume is not mounted on the executor, re-download the public zero-credit OpenAlex
    S3 works snapshot with the same range-request code and re-implement from the definitions below, logging every deviation
    in deviations.json. SHARED DEFINITIONS D3 (implement verbatim in every artifact; they are EXP6's frozen lib/h2.py definitions).
    26 venue-label OpenAlex fields; grounded yearly counts n_cj(t). ENTERED(t) = fields with >= 2 cumulative grounded papers.
    RETAINED(t) = off-home fields entered >= 2 years earlier with >= 2 papers in t-2..t. LOST(t) = entered fields with 0 papers
    in t-2..t. phi = the frozen 1998-2002 PMI backbone. d0_ret_rel(c,k,t) = mean phi[j,k] over j in RETAINED(t-1); d_lost
    = the same over LOST(t-1); M0 density = over ENTERED(t-1) (EXP6's M0). D_rca = Hidalgo 2007 / Guevara 2016 density over
    fields with RCA_cj(t-1) > 1, RCA_cj = (n_cj / n_c) / (N_j / N), no persistence requirement. D_vol = share-weighted density
    sum_j s_cj(t-1) phi[j,k] / sum_j phi[j,k]. Home field = field(s) holding >= 40% of the first 30 grounded works (>= 2 =
    intersection-born). SPLIT (unchanged from EXP5's frozen_spec.json): DEV = homes CS, Engineering, BGM, Medicine with onset
    2003-2009; HELD-OUT = homes PHYS, LIFEENV, SOC, MATHDEC with onset 2003-2009 PLUS the 2010-2014 cohort (split into DEV-home
    and non-DEV-home parts). STATISTICS: concept-clustered REFIT bootstrap CIs (>= 1,000 resamples; the model is refitted
    in every resample), crossed concept x field CIs for episode-level tests, DerSimonian-Laird pooling across held-out groups
    with I2, Holm correction inside each pre-declared family. The resampling unit is the concept, and it is named in every
    table. SEALING: every artifact writes frozen_spec.json (formula, covariates, thresholds, indicator list, code SHA-256)
    before any held-out outcome is read, logs its hash, and scores held-out exactly once. BUDGET: 0 OpenAlex API credits (the
    key is exhausted; the snapshot is free); OpenRouter <= $2 per artifact. INDICATORS, all over the feature window t0..t0+2
    only, grouped into families that are declared before scoring. (A) The ~34 concept-level co-occurrence ego-network indicators
    of art_yrradSC27HtQ, recomputed on the EXP5 frame. This needs the ONE targeted free snapshot pass: re-run EXP5's matcher
    and grounding over id, title, publication_year, type, primary_location.source.id, topics.id, referenced_works and authorships.author.id.
    Emit per grounded match (concept, year, work id, topic ids, reference ids, author ids) as a compact parquet (< 300MB,
    split if larger). Check that its per-concept yearly counts reproduce agg_counts.parquet (Spearman >= 0.99, else stop and
    log). Ego networks follow art_yrradSC27HtQ features.py on its backbone/ slices with Leiden gamma 3:degree/strength/new-edge
    growth, edge persistence and turnover, neighbourhood novelty NOV and NOV_res, participation coefficient, D_ratio / D_rare
    / D_z / D_sub, betweenness, Burt constraint (brokerage), k-core, clustering change, community transitions and community
    entropy. (B) Family F: field reach, field entropy, off-home share. (C) Family G variants: gateway landing G, G_A, G_btw.
    (D) Frontier rows: CONTACT_REACH, RETAINED_REACH (>= 2 papers in 2 of 3 years), RETENTION_RATIO_early, FRONTIER_POTENTIAL
    (sum over not-entered k of mean phi to early-retained fields). (E) Simple references: log early volume, early growth,
    B5 (log early volume, growth, off-home share, entropy, reach; identical to iteration 1). (F) Candidate S (unconnected
    co-author components among off-home early adopters) only if author IDs are cached; otherwise it is dropped and logged.
    Report the indicator-indicator Spearman matrix and hierarchical clusters, so near-duplicates are visible and families
    are really distinct. OUTCOMES, one table: O1 sustained uptake (log grounded works t0+6..t0+8 minus log early); O2r rarefied
    breadth (m = 30 and 50, no source truncation); O2r_resid (O2r residualised on log early volume); O3 transience (the art_33_KKk_G8Gw5
    features.py definition, verbatim); O4 citation growth (citations received by the concept's early works, counted from the
    referenced_works of all snapshot works in the same pass, t0+3..t0+8 vs t0..t0+2, field-normalised; dropped and logged
    if the pass does not fit the budget); O5 external recognition from art_O7Dq4L02QnDN, joined on legacy concept ID or QID,
    using only year_usable events: MeSH introduced after t0; a Wikipedia/Wikidata creation dated within t0..t0+8; a taxonomy
    entry added between dated versions. There is also an O5-WW variant (Wikipedia/Wikidata only) for every group, because
    SOC and ENG lack a dated taxonomy. Report O5 base rates per group, and drop a group from O5 scoring when it has < 20 positives.
    SELECTION on DEV only: rank indicators by partial Spearman given B5 (continuous outcomes) and by delta-AUC over B5 (binary
    O3/O5), with a concept-clustered refit bootstrap for each. Freeze the top 10 per outcome, a union top 10 (by mean rank
    across outcomes) and two learned models: an L1-logistic/elastic-net and an EBM (interpret, max 2-way interactions) on
    all indicators. Hash-freeze, then score ONCE on held-out. REPORTING: per held-out group and cohort part; DL-pooled with
    I2; Holm within each outcome family. A portability table gives, per indicator, its sign and CI in every group. Pre-registered
    predictions (from the iteration-2 portability table in 3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/eval_out.json
    F_record.F3): entropy, D_rare, D_ratio, participation and NOV_res stay associated with O2r but add little beyond B5. Edge
    persistence stays NEGATIVE. The CS-only degree, strength and new-edge growth fail held-out, which is a domain-specific
    negative result to report, not average away. RETENTION_RATIO_early and FRONTIER_POTENTIAL are positive for O2r_resid and
    O1 given B5; CONTACT_REACH is not. Compare the learned models with the best single indicator and with B5 on the same held-out
    set. Explain the model with EBM shape functions and L1 paths. OUTPUTS: indicator_matrix.parquet (concept x indicator),
    outcomes.parquet, rq1_dev_selection.json, frozen_spec.json + hash, rq1_heldout.json, portability_table.csv, learned_model.json,
    and figures: a portability heatmap (indicator x group, coloured by partial rho and marked where the CI excludes 0) and
    held-out delta-AUC bars with CIs.
  what_it_would_show: ''
  depends_on:
  - id: art_O7Dq4L02QnDN
    label: O5 external recognition ground truth
    relation_type:
    relation_rationale:
- id: experiment_iter3_dir3
  type: experiment
  objective: >-
    RQ2 trajectories and the 'why it works' analysis on the same EXP5 frame and D3 states. (a) Decompose each concept's breadth
    growth into contact rate x retention probability x frontier advance, and test whether localised and integrating concepts
    differ mainly in retention. (b) Derive recurring trajectories empirically, named only if two methods agree. (c) Re-test
    the temporal-sequence question properly: does a concept first become central within its home community and then diffuse,
    or does it emerge at an intersection? (d) Show the mechanism in case studies and a lineage check of retained versus lost
    adopters.
  approach: >-
    INPUTS ARE READ BY PATH from the run tree (relative to the run root). Experiments may formally depend only on dataset
    or research artifacts, so earlier experiments are reused by path, not as dependencies. 3_invention_loop/iter_2/gen_art/gen_art_experiment_5/
    (art_wxWssKSUR45f): frame_concepts.csv (12,499 concepts, TAG grounding + LLM precision gate), episodes.csv (27,393), concept_outcomes.csv,
    concept_features_basic.csv, frozen_spec.json (split and fold assignment), scan/agg_counts.parquet (concept x year x venue-field
    x tag-state counts, 19.7M rows: the source of every state matrix), scan/year_field_totals.npz, scan/co_by_year.npz (yearly
    26 x 26 FIELD co-occurrence, not concept-level), scan/reservoir/ (sampled matched rows with snapshot file/row pointers),
    results/source_field.parquet, rangefile.py, scan_full.py, matcher.py, grounding.py. 3_invention_loop/iter_2/gen_art/gen_art_experiment_6/
    (art_N-mpomDZZ1ln): lib/h2.py (states(), the frozen ENTERED/RETAINED/LOST definitions), lib/traj.py, lib/stats_core.py,
    results/entry_risk_sets_dev.parquet and entry_risk_sets_heldout.parquet, results/frame_concepts.csv, heldout_result.json,
    dev_result.json, trajectories_*.csv, ordering_*.csv, inputs/field_backbone.json (26-field positive-PMI backbone, 1998-2002).
    3_invention_loop/iter_1/gen_art/gen_art_experiment_3/ (art_yrradSC27HtQ): features.py (concept ego network = the OpenAlex
    TOPICS carried by a concept's matched works, placed on full-corpus topic co-occurrence backbones), backbone/slice0-2.npz
    (topic PMI slices 2000-04, 2005-09, 2010-14), scan_snapshot.py and results/exploratory_partial_association.json. NO concept-topic,
    work-ID, citation or author cache exists for the EXP5 frame. Anything that needs one requires ONE targeted pass over the
    free snapshot (EXP3 streamed 7 columns of 476M works in 17 min), re-using EXP5's matcher and grounding unchanged so that
    the frame is identical. If the run volume is not mounted on the executor, re-download the public zero-credit OpenAlex
    S3 works snapshot with the same range-request code and re-implement from the definitions below, logging every deviation
    in deviations.json. SHARED DEFINITIONS D3 (implement verbatim in every artifact; they are EXP6's frozen lib/h2.py definitions).
    26 venue-label OpenAlex fields; grounded yearly counts n_cj(t). ENTERED(t) = fields with >= 2 cumulative grounded papers.
    RETAINED(t) = off-home fields entered >= 2 years earlier with >= 2 papers in t-2..t. LOST(t) = entered fields with 0 papers
    in t-2..t. phi = the frozen 1998-2002 PMI backbone. d0_ret_rel(c,k,t) = mean phi[j,k] over j in RETAINED(t-1); d_lost
    = the same over LOST(t-1); M0 density = over ENTERED(t-1) (EXP6's M0). D_rca = Hidalgo 2007 / Guevara 2016 density over
    fields with RCA_cj(t-1) > 1, RCA_cj = (n_cj / n_c) / (N_j / N), no persistence requirement. D_vol = share-weighted density
    sum_j s_cj(t-1) phi[j,k] / sum_j phi[j,k]. Home field = field(s) holding >= 40% of the first 30 grounded works (>= 2 =
    intersection-born). SPLIT (unchanged from EXP5's frozen_spec.json): DEV = homes CS, Engineering, BGM, Medicine with onset
    2003-2009; HELD-OUT = homes PHYS, LIFEENV, SOC, MATHDEC with onset 2003-2009 PLUS the 2010-2014 cohort (split into DEV-home
    and non-DEV-home parts). STATISTICS: concept-clustered REFIT bootstrap CIs (>= 1,000 resamples; the model is refitted
    in every resample), crossed concept x field CIs for episode-level tests, DerSimonian-Laird pooling across held-out groups
    with I2, Holm correction inside each pre-declared family. The resampling unit is the concept, and it is named in every
    table. SEALING: every artifact writes frozen_spec.json (formula, covariates, thresholds, indicator list, code SHA-256)
    before any held-out outcome is read, logs its hash, and scores held-out exactly once. BUDGET: 0 OpenAlex API credits (the
    key is exhausted; the snapshot is free); OpenRouter <= $2 per artifact. (1) STATE SEQUENCES: for every concept, a field
    x year sequence over {untouched, entered, retained, lost}, t0..t0+10. Yearly concept summaries: contact rate (new fields
    entered per year), retention probability (share of entered off-home fields that become retained), frontier advance (entries
    per retained field), rarefied entropy, FIELD-level brokerage (how many backbone communities the retained set spans and
    its participation coefficient over them, on the frozen backbone and on a time-varying field backbone built from EXP5 scan/co_by_year.npz)
    and within-home share. Concept-topic ego-network measures belong to the RQ1 artifact and are not recomputed here. (2)
    DECOMPOSITION TEST: log(final breadth) = log contact + log retention + log frontier, with a Shapley decomposition of the
    variance between the top and bottom O2r_resid terciles. Adjust for Medicine homes and also exclude them (EXP6's 'localised'
    class was 42/60 Medicine). Prediction: retention explains the largest share. (3) TRAJECTORIES: DTW k-medoids on the standardised
    yearly summary vectors (k = 2..8, silhouette and gap) and a 4-state Gaussian or categorical HMM. A class is named only
    if DTW and HMM agree (ARI >= 0.5), it replicates on held-out when re-clustered, and it survives excluding Medicine homes.
    Otherwise report a continuum and show it along the 2-3 principal axes. Candidate names come from the data, e.g. localised,
    rapid interdisciplinary diffusion, gradual integration, transient expansion (O3), rising brokerage. (4) SEQUENCES, answering
    the reviewer: an event study with concept FE around (i) first within-home centrality peak and (ii) first off-home retention.
    Both directions (A -> B and B -> A) are tested and pre-trends reported; a random-year placebo is applied; DEV and held-out
    are reported separately. The iteration-2 ordering result is recorded as MIXED unless this test resolves it. Intersection-born
    concepts are compared with single-home concepts on time-to-first-retention and on the final trajectory class. (5) WHY
    IT WORKS: pick 6-8 case concepts from the quantitative extremes, with mixed domains and not only AI: the largest and smallest
    per-concept frontier contributions in art_N-mpomDZZ1ln heldout_result.json / entry risk sets; each trajectory medoid;
    one transient spike; one concept that stays local despite high volume. For each, draw a field-flow (alluvial) figure of
    states over time on the backbone. LINEAGE CHECK at zero credits, restricted to the case concepts plus 150 random held-out
    concepts: one targeted free snapshot pass re-using EXP5's matcher collects their works with referenced_works and topics.
    For retained versus lost adopters in the same field, compare the papers' reference lists and co-topics.Do retained adopters
    cite field-specific literature and pair the concept with the field's own methods (adaptation), while lost adopters cite
    mostly the home field (borrowing)? Report the share of within-field references and a Jaccard to the field's top co-concepts,
    with concept-clustered CIs. (6) A methodology-diagram data file for the paper's pipeline figure: stage names, inputs,
    counts at each stage (works, concepts, episodes, risk-set rows) and split sizes, taken from the actual runs. OUTPUTS:
    state_sequences.parquet, decomposition.json, trajectories.json (assignments, ARI, stability, medoids), sequence_tests.json,
    case_studies/ (figures and per-concept JSON), lineage_check.json, pipeline_counts.json, and figures for the paper. (7)
    EXTERNAL TIMING: join art_O7Dq4L02QnDN (year_usable events only) and report, per trajectory class or continuum axis, the
    share of concepts externally recognised and the median lag from onset to recognition, with concept-clustered CIs.
  what_it_would_show: ''
  depends_on:
  - id: art_O7Dq4L02QnDN
    label: recognition timing per trajectory
    relation_type:
    relation_rationale:
- id: evaluation_iter3_dir4
  type: evaluation
  objective: >-
    Clear the review's blocking soundness items and prepare the evidence record for the paper. (a) Rebuild every contested
    claim from its result file into a claims ledger (claim -> file -> key -> value -> status). (b) Produce the missing record
    tables. (c) Measure agreement between the EXP5 and EXP6 frames on the concepts they share. (d) Validate O5 as an independent
    ground truth before the RQ1 matrix uses it.
  approach: >-
    All inputs exist; no new data. 3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/ (art_lwI2DuRtQRZX) is read by path,
    not as a dependency (evaluations may depend only on experiments and datasets). (1) CLAIMS LEDGER (claims_ledger.csv):
    for every headline number in iterations 1-2, read the value from its source file and flag MATCH / MISMATCH / MISSING.
    Required corrections from the iteration-2 review: (i) list every preregistered H1 criterion from 3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/h1_heldout.json
    verdict_H1.criteria, including lpm_field_fe (beta 0.068/SD, p_concept 0.041, p_twoway 0.17) and lpm_field_fe_all_splits;
    (ii) the ordering result rewritten as MIXED, with the negative concept-FE lead-lag coefficients, the ev-3 pre-trend, the
    significant DEV reverse path (b 0.232, p 0.006), the placebo p and the correct denominators (57 of 175 broad concepts;
    57/87 non-tied); (iii) the 7 missing partial associations from 3_invention_loop/iter_1/gen_art/gen_art_experiment_3/results/exploratory_partial_association.json
    (D_z 0.313, D_sub 0.245, ...); (iv) the art_O7Dq4L02QnDN coverage counts corrected from out/coverage_report.json, with
    entries and concepts kept separate (ACM 3,583 entries vs 1,298 concepts; MSC 17,872 vs 1,121; PACS 8,462 vs 2,635; Wikipedia
    64,363 with any event, 50,459 year-usable); (v) H3 relabelled from 'confirmed' to its CI evidence (the pooled bootstrap
    CI includes 0; DEV-to-held-out shrinkage from 0.14 to 0.03); (vi) the mislabelled all_four row. (2) MISSING TABLES: the
    34-row portability table (from 3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/eval_out.json F_record.F3); the iteration-1
    lineage robustness table from 3_invention_loop/iter_1/gen_art/gen_art_experiment_1 (GLMM agreement 0.163, probe agreement
    0.10, sensitivities); concept-clustered REFIT bootstrap CIs for the iteration-1 concept-level headline deltas and for
    O2r_resid; a traceable next-field result file that joins EXP6's heldout_result.json to its risk-set rows. (3) CROSS-FRAME
    AGREEMENT on concepts in both the EXP5 and EXP6 frames: onset year (exact and +/-1), home field (kappa), grounded early
    volume (Spearman), O2r (Spearman), the episode set (Jaccard) and retention labels (kappa). Report which D3 definitions
    cause disagreements. This tells the paper whether the two frames can be pooled or must stay separate. (4) O5 VALIDATION:
    on the EXP5 frame joined to art_O7Dq4L02QnDN, report O5 coverage and base rate per home group and per source. Report the
    association of O5 with O1 and O2r (external recognition should relate to, but not duplicate, publication outcomes; report
    rho with CIs). Report the lag between onset and recognition. Hand-check 50 random positives and 50 negatives (year_usable,
    event after t0), using the dataset's own hand_check files where they exist. Flag sources that leak future information
    (e.g. Wikidata creation years before t0 for old concepts). OUTPUTS: eval_out.json (schema-valid), claims_ledger.csv, record_tables/
    (one CSV per table), frame_agreement.json, o5_validation.json and short notes on how each correction changes the text.
  what_it_would_show: ''
  depends_on:
  - id: art_wxWssKSUR45f
    label: S1 frame and H1 results to audit
    relation_type:
    relation_rationale:
  - id: art_N-mpomDZZ1ln
    label: frontier lead, ordering and trajectories to audit
    relation_type:
    relation_rationale:
  - id: art_O7Dq4L02QnDN
    label: O5 table to validate
    relation_type:
    relation_rationale:
- id: research_iter3_dir5
  type: research
  objective: >-
    Make the result publishable in Applied Network Science. (a) A prior-art check of the two new claims (the retained-frontier
    entry effect and the abandonment penalty) against the relatedness, exit and diffusion literatures. (b) Per-RQ comparison
    numbers for RQ1 (emerging-topic detection and forecasting) and RQ2 (interdisciplinary diffusion trajectories), mostly
    from ANS. (c) The ANS article structure and a concrete specification for the methodology figure.
  approach: >-
    Start from 3_invention_loop/iter_2/gen_art/gen_art_research_1/research_report.md and research_out.json (art_dxvRpQufMR0e:
    22 ANS papers, Guevara 2016 AUCs, exit literature, template notes); do not repeat that work. (1) PRIOR ART FOR THE NEW
    CLAIMS. Search for relatedness density that weights presences by persistence or duration, and for effects of exited or
    lost activities on neighbours' entry: Neffke, Henning & Boschma 2011; Bahar, Hausmann & Hidalgo 2014 (neighbours); Jun
    et al. 2020; Boschma and colleagues on exit; Pinheiro et al. 2022; Hausmann & Klinger (persistent RCA); Zaccaria et al.
    (economic fitness and entry forecasting, with AUC and precision numbers); knowledge-space entry work by Kogler, Rigby
    and Balland; and science-field entry by Chinazzi et al. 2019 (research space of countries). Also the invasion-biology
    casual/naturalised distinction (Richardson et al. 2000; Blackburn et al. 2011) and cultural-evolution metapopulation work
    (Premo). For each paper give: unit, whether presence is thresholded or persistence-weighted, whether exit is modelled,
    and the reported effect or AUC. Give a verdict: NEW / PARTIALLY ANTICIPATED / ANTICIPATED, with a quote. (2) RQ1 COMPARISON:
    emerging-topic detection and forecasting with numbers. Small, Boyack & Klavans 2014; Rotolo et al. 2015; Wang 2018; Xu
    et al. 2021; Krenn & Zeilinger 2020 and Gu & Krenn (link-forecast AUCs are level AUCs, flag them as not comparable); Salatino
    et al. (Augur); Behrouzi et al. 2020; Liang et al.; and ANS papers on temporal knowledge or co-occurrence networks. Extract
    metric, horizon, held-out design (whether they test across domains) and value. (3) RQ2 COMPARISON: interdisciplinary diffusion
    and trajectories. Fontaine 2024 (ANS, AI into neuroscience); Sun & Latora 2020; Sun et al. 2013 'social dynamics of science';
    De Domenico 2016 (ANS); Holmgren 2023 (ANS alluvial); Leydesdorff diffusion-of-topics work; Mao et al. 2020. Do any derive
    trajectory classes or decompose breadth into contact and retention? (4) VENUE. Retry the collection page link.springer.com/collections/fgcaicgjah
    through a different route (Crossref or OpenAlex filter on ANS with the collection's title or editors, the Springer Nature
    metadata API, a web search for 'site:appliednetsci.springeropen.com' plus the collection title). Record the collection's
    real title and member list if reachable, or state clearly that it is not. Give the ANS article structure (section order,
    abstract format, declarations, length) from 3 recent ANS research articles on science-of-science topics. Describe how
    those papers present their methodology figure (a pipeline diagram with stages, data counts and splits), as a concrete
    spec for ours. (5) Output a verified reference list (DOI or arXiv ID for every entry, ready for Semantic Scholar BibTeX
    fetching) and a per-RQ comparison table template: ours vs theirs, metric, comparable yes/no, why.
  what_it_would_show: ''
  depends_on: []
expected_outcome: >-
  After this iteration: (1) A decisive, independent held-out answer on the retained-frontier claim. It comes with the full
  relatedness ladder (M0 -> D_rca -> D_vol -> d0_ret_rel -> d_lost), per-group and pooled estimates with refit CIs and I2,
  specificity nulls (retained-label permutation, volume-matched contrast, dose, rewired backbone), the abandonment-penalty
  estimate, and the authoritative D3 state panel. (2) The RQ1 deliverable: a 40-50 indicator matrix from distinct families,
  top 10 per outcome frozen on DEV, and a single held-out scoring against O1-O5 including external recognition. It has a portability
  table, domain-specific negative results and a learned-model comparison. (3) RQ2: the breadth decomposition (contact x retention
  x frontier), empirically derived trajectories that are named only when two methods agree, a properly specified sequence
  test, 6-8 case studies and the lineage check of retained versus lost adopters, plus the pipeline counts for the methodology
  figure. (4) A clean record: a claims ledger, the missing tables, cross-frame agreement and a validated O5. (5) A prior-art
  verdict, per-RQ comparison numbers, the ANS structure and a methodology-figure spec. With these, iteration 4 can write the
  paper, or run one targeted follow-up if the frontier claim splits by domain.
summary: >-
  Iteration 3 tests the run's surviving lead and completes the study. The lead: a field picks up a new concept from related
  fields that KEPT it, not from fields that only touched it, and fields that dropped it may even deter adoption. Five parallel
  bets. (1) A decisive test against the standard relatedness-density model on a second, untouched held-out frame, with persistence-specific
  placebos. (2) The RQ1 held-out validation of 40-50 network indicators against five ground truths, including external recognition,
  plus a learned model. (3) RQ2 diffusion trajectories, a breadth decomposition, case studies and the mechanism. (4) A record
  repair that clears the review's soundness block and validates the external ground truth. (5) Prior art, comparison numbers
  and the journal template. All of it uses zero API credits.
</previous_strategies>

<dependency_rules>
- depends_on is a list of objects {id, label} — each entry references an existing artifact and tags how it is being used
- "id" can ONLY reference IDs from <existing_artifacts> — never IDs you are proposing (all new artifacts run in parallel)
- "label" is a SHORT free-text type label (a word or two, NOT a sentence) describing what role the dep plays — e.g. "dataset", "validates", "extends", "supersedes". Required on every dep.
- Setting depends_on provides the dependency's out_dependency_files to your artifact at execution time
- If no suitable existing artifacts exist, use empty depends_on
- New artifact IDs are assigned by the system after submission — do not invent IDs for your proposed artifacts
</dependency_rules>

<available_artifact_types>
Artifact types you can plan. Use this to choose the right types for your strategy objectives.

<artifact_types>
RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect

EVALUATION
Evaluate experiment results with metrics, statistical analysis, and validity checks.
Runtime: Python 3.12, UV (any evaluation library), isolated workspace, gradual scaling matching experiment.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Compute any quantitative metrics and statistical tests, analyze validity and robustness.
Deps: REQUIRED at least one EXPERIMENT | OPTIONAL DATASET if reference data needed

PROOF
Formally prove mathematical statements in Lean 4 with automated iteration.
Runtime: LLM agent with Lean 4 compiler feedback loop.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-lean (proof verification, Mathlib search, tactics: ring, linarith, nlinarith, omega, simp, etc.)
Capabilities: Formally verify properties and inequalities, iterative proof development, lemma decomposition.
Deps: REQUIRED none | OPTIONAL RESEARCH for mathematical background
</artifact_types>
</available_artifact_types>

<compute_hardware>
This planning session's own shell (if you inspect it, e.g. via aii-use-hardware or nproc) is a lightweight pod and is NOT what any artifact executes on. Each artifact you direct runs LATER on its own separately-provisioned pod, sized by artifact type:

  - research: cpu_basic (4 vCPUs, 16GB RAM — proofs, research, lightweight tasks)
  - experiment: gpu_basic (1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models), cpu_plus (4 vCPUs, 32GB RAM — large datasets, memory-intensive processing)
  - dataset: gpu_basic (1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models), cpu_plus (4 vCPUs, 32GB RAM — large datasets, memory-intensive processing)
  - evaluation: gpu_basic (1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models), cpu_plus (4 vCPUs, 32GB RAM — large datasets, memory-intensive processing)
  - proof: cpu_basic (4 vCPUs, 16GB RAM — proofs, research, lightweight tasks)

Size scale decisions (panel/sweep counts, model counts, etc.) against these tiers, not against this planning session's own hardware.
</compute_hardware>

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead

EVALUATION executor scope:
  Output: eval_out.json with evaluation results
  DOES: Any evaluation of experiment results — metrics, statistical tests, ablations, comparisons, visualizations, robustness checks, error analysis, etc.
  DOES NOT: Implement new methods (use EXPERIMENT), collect data (use DATASET)
  This is for analyzing experiment outputs from any angle

PROOF executor scope:
  Output: Lean 4 proof files (.lean) with verified theorems
  DOES: Write and verify Lean 4 formal proofs with Mathlib, iterative compilation
  DOES NOT: Run Python experiments, collect data, do empirical analysis
  Use only when formal mathematical guarantees are needed
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
EVALUATION: Must depend on at least one EXPERIMENT. Focus on statistical rigor and validity checks. When a power analysis or the effect sizes already on record show the panel underpowered for the effect being chased, spend the plan's budget on more graded samples or checkpoints, not on more candidate metrics — a wider panel of readouts over the same underpowered set proves nothing new.
PROOF: Use only when the hypothesis requires formal mathematical guarantees. Lean 4 + Mathlib.
</artifact_planning_rules>

<existing_artifacts>
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
out_dependency_files:
  file_list:
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
out_dependency_files:
  file_list:
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
out_dependency_files:
  file_list:
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
out_dependency_files:
  file_list:
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
out_dependency_files:
  file_list:
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
out_dependency_files:
  file_list:
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
out_dependency_files:
  file_list:
  - data.py
  - full_data_out/full_data_out_1.json
  - full_data_out/full_data_out_2.json
  - full_data_out/full_data_out_3.json
  - mini_data_out.json
  - preview_data_out.json
  - reproducibility.md
  data_file_paths:
  - full_data_out/full_data_out_1.json
  - full_data_out/full_data_out_2.json
  - full_data_out/full_data_out_3.json
  - mini_data_out.json
  - preview_data_out.json

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
out_dependency_files:
  file_list:
  - research_out.json
  - research_verification.json

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
out_dependency_files:
  file_list:
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
out_dependency_files:
  file_list:
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
out_dependency_files:
  file_list:
  - eval.py
  - full_eval_out.json
  - mini_eval_out.json
  - preview_eval_out.json
  - reproducibility.md

--- Item 12 ---
id: art_EesdB8cuSfcU
type: research
title: Is 'fields that keep it' new? Prior art and venue check
summary: |-
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
out_dependency_files:
  file_list:
  - research_out.json
  - research_verification.json
</existing_artifacts>

<current_report>
The run's research report so far, every round in order, is at /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_strat/current_report.md. The artifacts
above are the evidence; open the report for how the run has read them and what gaps remain.
Gaps and weak results signal what to try differently — not what to conclude.
</current_report>

<reviewer_feedback>
Paper reviewer feedback from the previous iteration. Your strategy MUST address these critiques.
Prioritize major issues — these are the most impactful improvements to make.

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
</reviewer_feedback>

<task>
Generate 1 research strategy for THIS iteration.

**ARTIFACT BUDGET: EXACTLY 5 artifact directions per strategy — fill EVERY slot.**
Not "up to" 5: 5. A short answer is a verification failure and comes back
for another turn, because an unspent slot is a bet the run never placed.

**EVERY ARTIFACT IS A BET.** For each direction, write `what_it_would_show`: the
sentence the paper gets out of it IF IT WORKS — the result, not the activity. A
direction whose success would produce no such sentence does not deserve the slot;
replace it with one that would.

Each strategy should:
1. Establish the FIELD'S REASONING first and write it into `domain_reasoning`, then say in `principle_alignment` which of those principles the strategy follows and which it breaks on purpose
2. Define a clear OBJECTIVE - what novel contribution we're building toward
3. Plan artifacts to execute NOW - specify type, objective, approach, and depends_on for each
4. Account for parallel execution - all strategies and all planned artifacts run simultaneously, their artifacts are combined into one shared pool

**AIM AT A POSITIVE RESULT.** The strategy's target is a finding the paper
can LEAD with: an effect that is there, a method that beats what came before,
a construction that works, a proof that goes through. Report a null honestly
when you get one — but do not plan toward one. If the evidence so far says
the literal question is a settled negative, do not widen into yet another
screen that will also come back empty. Move SIDEWAYS to the nearest object
that can come out positive: the adjacent phenomenon where the effect should
be strongest, a sharper instrument or detector that would find it if it is
there, the narrower condition under which it does hold, or a result that
holds by construction. State that shift in the strategy's rationale.

**BROADER IS NOT THE SAME AS DEEPER.** This applies when you are going DEEPER
on a claim that already has support — it is not an argument against a wide
screen, which tests DIFFERENT candidate answers rather than the same one in
more places. Adding models, datasets, or settings to an experiment that
already ran makes the table bigger; it does not make the contribution
stronger, and it is the default a strategy generator drifts into when it has
nothing sharper to propose. Spend an artifact on scale only when the SPREAD
itself is the finding (a scaling trend, a regime boundary, a generalisation
claim the paper actually makes). Otherwise spend it on something that could
change the conclusion: the mechanism behind an observed effect, the condition
under which it disappears, the confound that would explain it away, or the
baseline whose absence a reviewer would name first.


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
    "ArtifactDep": {
      "description": "A single dependency on an existing artifact, with a short type label.\n\n``id`` and ``label`` are LLM-generated at strategy time. ``label`` is free-text but\nshort \u2014 a word or two naming the type of dependency, not a sentence.\n\n``relation_type`` and ``relation_rationale`` are populated later, in upd_hypo,\nusing the MultiCite citation-function typology (Lauscher et al., NAACL 2022).\nThey are absent at strategy time and may stay absent for legacy runs.",
      "properties": {
        "id": {
          "description": "ID of an existing artifact this artifact depends on",
          "title": "Id",
          "type": "string"
        },
        "label": {
          "description": "Short free-text label naming the type of this dependency (a word or two, not a sentence)",
          "title": "Label",
          "type": "string"
        }
      },
      "required": [
        "id",
        "label"
      ],
      "title": "ArtifactDep",
      "type": "object"
    },
    "ArtifactDirection": {
      "description": "High-level direction for an artifact to execute this iteration.\n\nID is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).",
      "properties": {
        "type": {
          "description": "Type of artifact to create",
          "enum": [
            "experiment",
            "research",
            "proof",
            "evaluation",
            "dataset"
          ],
          "title": "Type",
          "type": "string"
        },
        "objective": {
          "description": "What we want to achieve with this artifact",
          "title": "Objective",
          "type": "string"
        },
        "approach": {
          "description": "High-level direction/method",
          "title": "Approach",
          "type": "string"
        },
        "what_it_would_show": {
          "default": "",
          "description": "EVERY ARTIFACT IS A BET: the sentence the paper gets out of this one IF IT WORKS. Name the result, not the activity \u2014 what would be true, at roughly what size, and why that answers part of the ask. A direction whose success would produce no such sentence is not worth a slot.",
          "title": "What It Would Show",
          "type": "string"
        },
        "depends_on": {
          "description": "Existing artifacts this depends on, each with a short type label",
          "items": {
            "$ref": "#/$defs/ArtifactDep"
          },
          "title": "Depends On",
          "type": "array"
        }
      },
      "required": [
        "type",
        "objective",
        "approach"
      ],
      "title": "ArtifactDirection",
      "type": "object"
    },
    "Strategy": {
      "description": "A research strategy.\n\nContent fields have LLMPrompt + LLMStructOut markers.\n``id`` is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).\n\nID format: gen_strat_idx{N}",
      "properties": {
        "domain_reasoning": {
          "default": "",
          "description": "How researchers in THIS field reason, established before choosing: the principles the field takes as given, what it counts as convincing evidence, the standard methodological moves and what each exists to rule out, and the field's usual failure modes. Name the field and cite what you read. Anything true of every field does not belong here.",
          "title": "Domain Reasoning",
          "type": "string"
        },
        "principle_alignment": {
          "default": "",
          "description": "Which of those field principles this strategy follows and how, and which it deliberately breaks \u2014 with the reason each break is worth it and what keeps the result credible without it.",
          "title": "Principle Alignment",
          "type": "string"
        },
        "title": {
          "description": "Strategy name in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "objective": {
          "description": "The novel contribution we're building toward",
          "title": "Objective",
          "type": "string"
        },
        "rationale": {
          "description": "Why this strategy is promising",
          "title": "Rationale",
          "type": "string"
        },
        "artifact_directions": {
          "description": "Artifacts to execute THIS iteration",
          "items": {
            "$ref": "#/$defs/ArtifactDirection"
          },
          "title": "Artifact Directions",
          "type": "array"
        },
        "expected_outcome": {
          "description": "What we'll have after this iteration's artifacts complete",
          "title": "Expected Outcome",
          "type": "string"
        },
        "summary": {
          "default": "",
          "description": "Brief summary of the strategy and its expected contribution",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "title",
        "objective",
        "rationale",
        "artifact_directions",
        "expected_outcome"
      ],
      "title": "Strategy",
      "type": "object"
    }
  },
  "description": "Top-level wrapper for LLM strategy generation output.",
  "properties": {
    "strategies": {
      "description": "List of generated strategies",
      "items": {
        "$ref": "#/$defs/Strategy"
      },
      "title": "Strategies",
      "type": "array"
    }
  },
  "required": [
    "strategies"
  ],
  "title": "Strategies",
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

### [3] TOOL CALL — Bash · 2026-09-29 02:01:27 UTC

```
Inspect Exp8 workspace and uploads:
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop; ls $R/iter_3/gen_art/; ls $R/iter_3/gen_art/gen_art_experiment_8 $R/iter_3/gen_art/gen_art_experiment_8/results | head -80; du -sh $R/iter_3/gen_art/gen_art_experiment_8/* 2>/dev/null | sort -h | tail -15; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/user_uploads; ls -la
```

### [4] TOOL RESULT — Bash · 2026-09-29 02:01:27 UTC

```
{"stdout": "gen_art_evaluation_2\ngen_art_experiment_7\ngen_art_experiment_8\ngen_art_experiment_9\ngen_art_research_2\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8:\nREADME.md\n__pycache__\naudit.py\nbuild_features.py\ndata\ndev_select.py\nfigures\nfull_method_out.json\nheldout.py\ninputs\nlib\nlogs\nmake_outputs.py\nmethod.py\nmethod_out.json\nmini_method_out.json\nmodels\noutcomes.py\npassA\npassA.py\npassB\npassB.py\npreview_method_out.json\npyproject.toml\nreadme_tables.py\nrederive.py\nreproducibility.md\nrequirements.lock.txt\nrestore.sh\nresults\nsnapshot\ntests\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results:\naudit.json\ncase_exemplars.json\nchecks.json\ndev_oof_predictions.parquet\ndev_ranking.csv\ndev_ranking_sensitivity.csv\ndeviations.json\nfeatures_config.json\nfrozen_spec.json\nheldout_predictions.parquet\nheldout_summary.json\nheldout_unit_results.csv\nindicator_clusters_dev.json\nindicator_corr_dev.csv\nindicator_dictionary.csv\nindicator_matrix.parquet\nlearned_model.json\nlearned_vs_single_heldout.json\no2r_resid_fit.json\no4_reference_expectations.csv\no5_join.json\noutcome_base_rates.json\nportability_table.csv\npower_dev.json\nprereg_b5_minus_reach.csv\nprereg_verdicts.json\nprovenance.json\nrederive.json\nrq1_dev_selection.json\nrq1_heldout.json\nsensitivities_heldout.csv\nsensitivities_pooled.json\nsize_diagnostic_dev.csv\nt0_8_ego_port.json\nt1_passA_exact_65_1125_1407_1918.json\nt4_ego_sanity.json\nt4_timing_nnull200_cut4.json\nunit_tests.json\n31K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/mini_method_out.json\n996K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/tests\n1.1M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/__pycache__\n1.2M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/logs\n1.4M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/snapshot\n2.3M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib\n3.6M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/figures\n13M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results\n24M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs\n35M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/method_out.json\n39M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/full_method_out.json\n55M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models\n63M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passB\n81M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data\n171M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA\ntotal 2030\ndrwxr-xr-x 3 root root 1005353 Sep 29 02:00 .\ndrwxr-xr-x 3 root root 1016342 Sep 29 02:00 ..\ndrwxr-xr-x 2 root root       1 Sep 29 02:00 .aii\n-rw------- 1 root root      54 Sep 29 02:00 .aii_claude_session.json\n-rw-r--r-- 1 root root   54762 Sep 29 02:01 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [5] TOOL CALL — Bash · 2026-09-29 02:01:33 UTC

```
Check Exp8 pass caches and EXP5 scan files:
E=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; ls -la $E/passA $E/passB $E/data | head -40; grep -n -i "passA\|pass A\|parquet\|restore\|snapshot" $E/README.md | head -50; ls $E/../gen_art_experiment_9 | head; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan 2>/dev/null | head
```

### [6] TOOL RESULT — Bash · 2026-09-29 02:01:33 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data:\ntotal 46479\ndrwxr-xr-x  6 231072 231072 2007277 Sep 29 00:35 .\ndrwxr-xr-x 17 root   root   3000144 Sep 29 01:03 ..\n-rw-r--r--  1 231072 231072 4314599 Sep 29 00:35 analysis_table.parquet\n-rw-r--r--  1 231072 231072  298030 Sep 28 23:17 bg_topics.npz\n-rw-r--r--  1 231072 231072 9459428 Sep 28 23:47 cites_early.parquet\n-rw-r--r--  1 231072 231072 1689738 Sep 28 23:17 counts_check.parquet\n-rw-r--r--  1 231072 231072 3381077 Sep 29 00:06 ego_features.parquet\ndrwxr-xr-x  2 231072 231072 1053996 Sep 28 23:27 ego_parts\ndrwxr-xr-x  2 231072 231072 2001087 Sep 29 00:05 ego_parts_c3\ndrwxr-xr-x  2 231072 231072 1035357 Sep 28 23:19 ego_timing\n-rw-r--r--  1 231072 231072 1806341 Sep 28 23:19 features_basic.parquet\n-rw-r--r--  1 231072 231072 2853717 Sep 28 23:19 frame_arrays.npz\ndrwxr-xr-x  2 231072 231072 2002622 Sep 28 23:17 frame_matches_early\n-rw-r--r--  1 231072 231072  156479 Sep 28 22:35 o5_events.parquet\n-rw-r--r--  1 231072 231072 1007932 Sep 29 00:35 outcomes.parquet\n-rw-r--r--  1 231072 231072  416193 Sep 28 23:50 outcomes_dev.parquet\n-rw-r--r--  1 231072 231072  622869 Sep 28 23:50 outcomes_sealed.parquet\n-rw-r--r--  1 231072 231072     229 Sep 28 23:17 passA_info.json\n-rw-r--r--  1 231072 231072     139 Sep 28 23:47 passB_info.json\n-rw-r--r--  1 231072 231072 8755448 Sep 28 23:18 passB_targets.npy\n-rw-r--r--  1 231072 231072 1725809 Sep 28 23:17 ref_sample.parquet\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA:\ntotal 6869\ndrwxr-xr-x  3 231072 231072 2016467 Sep 28 22:05 .\ndrwxr-xr-x 17 root   root   3000144 Sep 29 01:03 ..\ndrwxr-xr-x  2 231072 231072 2016467 Sep 28 23:15 parts\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passB:\ntotal 6848\ndrwxr-xr-x  3 231072 231072 2005733 Sep 28 22:05 .\ndrwxr-xr-x 17 root   root   3000144 Sep 29 01:03 ..\ndrwxr-xr-x  2 231072 231072 2005733 Sep 28 23:45 parts\n202:|diff| ~1e-15); T1: Pass A per-file counts equal EXP5's exactly; T2: A1 identical yearly grounded counts for all\n217:| `passA.py` | zero-credit OpenAlex S3 pass: EXP5 matcher + TAG grounding unchanged; early work/topic/author ids, topic background, reference sample |\n226:| `lib/common5.py`, `lib/matcher.py`, `lib/rangefile.py` | EXP5 analyser / Aho-Corasick matcher / HTTP-range parquet reader (copied; mkdir side effect removed) |\n227:| `lib/ego.py`, `lib/ego_ctx.py` | EXP3 `features.concept_core` ported (1-year windows) + context (EXP3 Leiden backbones, Pass A background) |\n236:| `data/frame_matches_early/part_*.parquet` | **kept**: grounded frame hits t0-3..t0+2 with work, topic and author ids |\n237:| `data/cites_early.parquet` | **kept**: citations to early works and the reference sample by citing year |\n238:| `data/ref_sample.parquet`, `data/bg_topics.npz`, `data/counts_check.parquet` | reference sample, topic background, reproduction counts |\n239:| `data/features_basic.parquet`, `data/ego_features.parquet` | families E/F/G/FR/S and A |\n240:| `data/outcomes_dev.parquet`, `data/outcomes_sealed.parquet`, `data/outcomes.parquet`, `data/analysis_table.parquet` | outcome tables (sealed file hashed in `logs/outcome_seal.log`) |\n252:| `results/learned_vs_single_heldout.json`, `results/learned_model.json`, `results/heldout_predictions.parquet`, `results/dev_oof_predictions.parquet` | learned models (coefficients, L1 path, EBM importances/shapes) and predictions |\n257:| `results/indicator_matrix.parquet`, `results/indicator_dictionary.csv`, `results/indicator_corr_dev.csv`, `results/indicator_clusters_dev.json`, `results/size_diagnostic_dev.csv` | indicators and DEV diagnostics |\n260:| `results/checks.json`, `results/unit_tests.json`, `results/t0_8_ego_port.json`, `results/t1_passA_exact_*.json`, `results/t4_ego_sanity.json`, `results/audit.json`, `results/rederive.json` | tests and audits |\n276:- Pass A took 62 min (a shared network cap of ~8 MB/s for part of the run); no fallback was needed. $0 OpenRouter,\n278:- Kept artifacts stay on the run's volume; `data/frame_matches_early/part_001.parquet` and `models/` are under\n285:./restore.sh                       # .venv from requirements.lock.txt\n293:| Pass A (2,040 files) | 62 min (33 min at full bandwidth in EXP5) |\n308:| deleted path | restore command |\n310:| `.venv/` | `./restore.sh` (`uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r requirements.lock.txt`) |\n313:Everything else stays in place. The per-file scan parts (`passA/parts/`, `passB/parts/`) and ego chunks\n315:They can be regenerated with `./restore.sh --scans` (Pass A + Pass B, zero-credit public S3 reads) and\n316:`./restore.sh --ego`. Their merged outputs (`data/frame_matches_early/`, `data/cites_early.parquet`,\n317:`data/ego_features.parquet`) are kept and published.\naborted_v1a_parts\nagg_counts.parquet\nco_by_year.npz\nllm_cache\nparts\nprescreen_survivors.parquet\nreservoir\nsample_info.json\nsample_titles\nscan_info.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [7] TOOL CALL — Bash · 2026-09-29 02:01:33 UTC

```
Peek at exemplars, deviations, windows:
E=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; cd $E; python3 -c "
import json;d=json.load(open('results/case_exemplars.json'));print(type(d), (list(d.keys())[:10] if isinstance(d,dict) else d[:2]))" ; head -c 1500 results/deviations.json; echo; grep -n -i "year\|window\|1995\|2022\|2024" README.md | head -30
```

### [8] TOOL RESULT — Bash · 2026-09-29 02:01:33 UTC

```
{"stdout": "<class 'dict'> ['indicator', 'frozen_sign', 'pooled_psp', 'high', 'low']\n{\n \"ego_windows\": \"Ego windows are 1 year (W1=t0, W2=t0+1, W3=t0+2) instead of EXP3 2+1+2 years; new_edge_rate divides by 3 years; D_lag, D_q, D_withself, F_bg dropped; comm_entropy added; slice_of clamps 2015-16 to slice 2; mid-window slice = slice_of(t0+1).\",\n \"T4_M_median\": \"T4 median M = 3.5 (> 3) so the n_ck >= 2 neighbour rule is kept; consequence: D-family indicators (need M >= 3; D_rare M >= 10) are missing for many concepts and may exceed the 30% missing eligibility bound.\",\n \"F4_ii_btw_cutoff_3\": \"T4 + profiling: igraph betweenness of the inserted node (cutoff 4) took 98% of ego time (3.5 s/concept under contention; >100 min projected). F4(ii) applied: betweenness path-length cutoff 4 -> 3 (1.2 s/concept). N_NULL kept at the planned 200 (nulls cost <1% of time). A first run started with N_NULL=100/cutoff 4 was aborted after ~50 concepts; its chunks (data/ego_parts/) are not used.\",\n \"O2r_resid_definition\": \"Plan O2r_resid = O2r_m50 - (a + b*logvol), DEV OLS a=2.741 b=0.397. EXP5 constants (4.790, -0.219) are for EXP5 own definition O2r_m30 - (a + b*log N_outcome), so they are not comparable; EXP5 definition refitted on DEV is reported as sensitivity outcome O2r_resid_N (held-out, top-10 of O2r_resid).\",\n \"F6_MATHDEC_O3\": \"MATHDEC has 3 O3 positives (< 20): dropped from O3 held-out scoring (F6); O3 pooled over PHYS/LIFEENV/SOC.\",\n \"bootstrap_B\": \"DEV ranking: B=1000 (continuous), B=500 (binary LOGO dAUC, refit), B=200 for coverage-sensitivity rankings and the T5 plac\n9:psp = partial Spearman given B5 (+ onset-year dummies); binary outcomes: dAUC over B5 with frozen DEV coefficients. `sign` = frozen DEV sign; `agree` = units (4 groups + 2 cohort parts) with that sign; **bold** = confirmed (Holm p < 0.05 within the outcome family and pooled sign = frozen sign).\n157:**Question (RQ1).** Which temporal network indicators, measured only in a concept's first three years (t0..t0+2),\n173:   **Caveat:** `M0_density_end` and `D_vol_end` use cumulative field history 1995..t0+2 (EXP6 D3 definition), so\n181:3. **Citation growth (O4, field- and year-normalised)**: `REL_home` (-0.114) and `author_growth` (+0.065) are\n185:   CI excluded 0, the frozen (filled) top 10s are all null held-out, and no model beats B5 + onset year\n202:|diff| ~1e-15); T1: Pass A per-file counts equal EXP5's exactly; T2: A1 identical yearly grounded counts for all\n203:12,499 concepts, A2 background Spearman 1.000 vs EXP3; T3: 99.8% of citation links have citing year >= cited year;\n227:| `lib/ego.py`, `lib/ego_ctx.py` | EXP3 `features.concept_core` ported (1-year windows) + context (EXP3 Leiden backbones, Pass A background) |\n237:| `data/cites_early.parquet` | **kept**: citations to early works and the reference sample by citing year |\n267:- Ego windows are 1 year each (planned); T4 median M = 3.5 (> 3), so the n >= 2 neighbour rule was kept. As a\n273:- O5 baselines add onset year as a linear term (dummies cannot transfer to the 2010-14 cohort).", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_strat/gen_strat_1", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-29 02:01:39 UTC

```
Check EXP5 agg_counts year coverage:
S=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan; cat $S/scan_info.json | head -c 1500; echo; python3 -c "
import pyarrow.parquet as pq
f=pq.ParquetFile('$S/agg_counts.parquet'); print(f.schema_arrow); m=f.metadata; print(m.num_rows, m.num_row_groups)
import collections
names=f.schema_arrow.names
yi=[i for i,n in enumerate(names) if 'year' in n]
for i in yi:
  mins=[m.row_group(r).column(i).statistics for r in range(min(m.num_row_groups,200))]
  print(names[i], min(s.min for s in mins if s), max(s.max for s in mins if s))
"
```

### [10] TOOL RESULT — Bash · 2026-09-29 02:01:39 UTC

```
{"stdout": "{\n \"files_done\": 2040,\n \"rows\": 476196327,\n \"base_rows\": 129360390,\n \"verified_hits\": 60011338,\n \"agg_rows\": 19670571\n}\nci: int32\nyear: int16\nvfield: int8\nptfield: int8\ntagstate: int8\nmt: int8\nn: int64\n-- schema metadata --\npandas: '{\"index_columns\": [], \"column_indexes\": [], \"columns\": [{\"name\":' + 824\n19670571 19\nyear 1995 2022", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-29 02:03:16 UTC

```
List Exp9, Eval2, Exp7 outputs:
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop; ls $R/iter_3/gen_art/gen_art_experiment_9; ls $R/iter_3/gen_art/gen_art_evaluation_2 | head -30; ls $R/iter_3/gen_art/gen_art_experiment_7/results | head -30; ls $R/iter_3/gen_art/gen_art_experiment_8/models
```

### [12] TOOL RESULT — Bash · 2026-09-29 02:03:16 UTC

```
{"stdout": "README.md\nclaims_ledger.csv\ncommon.py\neval.py\neval_out.json\nframe_agreement.json\nfull_eval_out.json\ninputs_manifest.json\nlogs\nmini_eval_out.json\no5_definitions.json\no5_validation.json\npreview_eval_out.json\npyproject.toml\nrecord_tables\nreproducibility.md\nresults\ntext_corrections.md\nuv.lock\nverify_headlines.py\nwp1_ledger.py\nwp2_t3_refit.py\nwp2_t4_nextfield.py\nwp3_frames.py\nwp4_extract.py\nwp4_handcheck.py\nwp4_o5.py\nwp5_text.py\naudit.json\ndeviations.json\nexploratory_lpm.json\nfrontier_result.json\nfrozen_spec.json\nnulls_exp5_dev.npz\nnulls_exp5_heldout_pooled4.npz\nnulls_exp6_heldout.npz\noverlap_report.json\nrisk_sets_exp5_minus_exp6_dev.parquet\nrisk_sets_exp5_minus_exp6_heldout.parquet\nrisk_sets_exp6_extended_dev.parquet\nrisk_sets_exp6_extended_heldout.parquet\nstate_panel_dev.parquet\nstate_panel_heldout.parquet\nstep1_exp6_robustness.json\nstep2_dev.json\nstep2_heldout.json\nunit_tests_T0.json\nebm_O1b.joblib\nebm_O1c.joblib\nebm_O2r_m50.joblib\nebm_O2r_resid.joblib\nebm_O3.joblib\nebm_O4.joblib\nebm_O5.joblib\nebm_O5_WW.joblib\nlinear_all_O1b.joblib\nlinear_all_O1c.joblib\nlinear_all_O2r_m50.joblib\nlinear_all_O2r_resid.joblib\nlinear_all_O3.joblib\nlinear_all_O4.joblib\nlinear_all_O5.joblib\nlinear_all_O5_WW.joblib", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] TOOL CALL — Bash · 2026-09-29 02:03:20 UTC

```
Locate failed Exp9 plan:
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3; ls $R; ls $R/gen_plan 2>/dev/null | head; find $R -maxdepth 3 -name "*experiment_3*" | head; head -30 $R/gen_art/gen_art_experiment_9/README.md
```

### [14] TOOL RESULT — Bash [ERROR] · 2026-09-29 02:03:20 UTC

```
Error: Exit code 1
gen_art
gen_plan
gen_report_text
gen_strat
review_report
upd_hypo
gen_plan_evaluation_1
gen_plan_experiment_1
gen_plan_experiment_2
gen_plan_experiment_3
gen_plan_research_1
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3
head: cannot open '/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_9/README.md' for reading: No such file or directory
```

### [15] THINKING · 2026-09-29 02:03:24 UTC

```
I've confirmed EXP5 counts span 1995-2022, Exp8's early-window matches are cached, and Exp9's directory is empty with its plan located in iter_3/gen_plan/gen_plan_experiment_3. Now I'll write the strategy JSON, README, and manifest.
```

### [16] TOOL CALL — Bash · 2026-09-29 02:03:24 UTC

```
List Exp9 plan files and EXP3 backbone:
ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/backbone 2>/dev/null
```

### [17] TOOL RESULT — Bash · 2026-09-29 02:03:24 UTC

```
{"stdout": "README.md\nslice0.npz\nslice1.npz\nslice2.npz", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-09-29 02:03:26 UTC

```
Ensure scratchpad exists:
mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-3-invention-loop-iter-4-gen-strat-gen-strat-1/093518dc-6f09-4794-8297-6ee773855bd6/scratchpad; echo ok
```

### [19] TOOL RESULT — Bash · 2026-09-29 02:03:26 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Write · 2026-09-29 02:06:18 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_strat/gen_strat_1/build_strategy.py

"""Builds .terminal_claude_agent_struct_out.json (the iteration-4 strategy) from plain Python strings."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

RUN = "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M"  # only used inside executor instructions (read-only inputs)

PATHS = (
    "INPUTS ARE READ BY PATH (run root = the run directory; experiments may formally depend only on datasets/research, so "
    "earlier experiments are reused by path). EXP5 = 3_invention_loop/iter_2/gen_art/gen_art_experiment_5/ (art_wxWssKSUR45f): "
    "frame_concepts.csv (12,499), concept_outcomes.csv, frozen_spec.json (split/folds), scan/agg_counts.parquet (concept ci x year "
    "1995-2022 x venue field x tagstate counts for ALL 56,643 legacy concepts), scan/year_field_totals.npz, scan/co_by_year.npz, "
    "scan/llm_cache (precision-gate cache), results/source_field.parquet (source -> venue field), matcher.py, grounding.py, "
    "rangefile.py, scan_full.py. EXP8 = 3_invention_loop/iter_3/gen_art/gen_art_experiment_8/ (art_dFQ6jbgNsR6Q): passA.py, passB.py, "
    "lib/ego.py + lib/ego_ctx.py (EXP3 ego features ported, 1-year windows W1..W3, validated to 1e-15), lib/matcher.py, lib/rangefile.py, "
    "build_features.py, outcomes.py, data/frame_matches_early/part_*.parquet (grounded hits t0-3..t0+2 with work, topic, author ids), "
    "data/cites_early.parquet, data/ref_sample.parquet, data/bg_topics.npz, data/features_basic.parquet, data/ego_features.parquet, "
    "data/outcomes.parquet, data/analysis_table.parquet, results/indicator_matrix.parquet, results/indicator_dictionary.csv, "
    "results/frozen_spec.json, results/heldout_unit_results.csv, results/portability_table.csv, results/case_exemplars.json, "
    "results/o2r_resid_fit.json, models/*.joblib (frozen ElasticNet/L1-logit and EBM per outcome). EXP7 = "
    "3_invention_loop/iter_3/gen_art/gen_art_experiment_7/ (art_22ppE1snfHKj): results/state_panel_{dev,heldout}.parquet (authoritative "
    "D3 concept x field x year states), step2_{dev,heldout}.json. EXP6 = 3_invention_loop/iter_2/gen_art/gen_art_experiment_6/ "
    "(art_N-mpomDZZ1ln): lib/h2.py (ENTERED/RETAINED/LOST), lib/traj.py, inputs/field_backbone.json (26-field PMI backbone 1998-2002). "
    "EXP3 = 3_invention_loop/iter_1/gen_art/gen_art_experiment_3/ (art_yrradSC27HtQ): backbone/slice0-2.npz (topic PMI slices "
    "2000-04/05-09/10-14, Leiden gamma 3). If the run volume is not mounted, re-implement from these definitions against the public "
    "zero-credit OpenAlex S3 snapshot with the same HTTP-range code and log every deviation in deviations.json. "
)

SHARED = (
    "SHARED DEFINITIONS (verbatim in every artifact). OPEN components over t0..t0+2 papers only, Exp8 lib/ego.py code: new_edge_rate, "
    "n_comm_W3, participation, NOV_res, ego_density_W3, edge_persistence. OPEN = mean of z(new_edge_rate), z(n_comm_W3), "
    "z(participation), z(NOV_res), -z(ego_density_W3), -z(edge_persistence), with z constants frozen on the EXP5 frame (all 12,499 "
    "concepts = SELECTION data); a concept needs >= 4 of 6 components. Builds: ALL-PAPERS (as Exp8); HOME-ONLY (ego network from the "
    "concept's grounded papers whose venue field is in its home set; venue-unlabelled papers excluded; home-paper coverage logged); "
    "SIZE-MATCHED ALL-PAPERS (mean over 20 random subsamples of all early papers down to the home-only paper count; separates 'fewer "
    "papers' from 'home restriction'). RETENTION_RATIO_early and CONTACT_REACH as in Exp8 (reported separately, not in OPEN). B5 = log "
    "early volume, early growth, off-home share, entropy, reach (Exp8). Home = field(s) with >= 40% of the first 30 grounded works "
    "(>= 2 homes = intersection-born). D3 states from EXP6 lib/h2.py. STATISTICS: resampling unit = concept (named in every table); "
    "2,000-draw concept bootstraps (refit); DerSimonian-Laird pooling with I2; Holm within each pre-declared family. SEALING: "
    "frozen_spec.json (formulas, signs, thresholds, covariates, code SHA-256) written and hashed into logs/seal.log BEFORE any outcome "
    "of the evaluation body is computed; that body is scored once. BUDGET: 0 OpenAlex API credits (zero-credit S3 snapshot only); "
    "OpenRouter spend capped per artifact as stated, running total from usage.cost, stop on the first 'AI Inventor per-run OpenRouter "
    "budget' 403. "
)

domain_reasoning = (
    "FIELD: scientometrics / science of science using network-science methods (target: Applied Network Science, collection "
    "'Networks for everyday life'). No domain handbook fits (the four offered cover computational linguistics, mech-interp, multi-agent "
    "LLMs and neuro-symbolic AI), so the principles below are provisional. They rest on the literature this run has already read and "
    "verified (art_dxvRpQufMR0e: 22 ANS papers, Guevara 2016, Weng 2013, Maillart 2026; art_EesdB8cuSfcU: relatedness/exit prior art, "
    "ANS skeleton) and on this run's own measured failure modes. "
    "(1) PRINCIPLES. There is no single ground truth for emergence (Rotolo, Hicks & Martin 2015), so a signal is believed only when it "
    "predicts several later outcomes beyond count baselines. Fields differ in size and citing habits, so breadth must be volume-adjusted "
    "(rarefaction, residualisation), otherwise it relabels growth. Co-word analysis has argued since Callon et al. (1991) about "
    "density versus centrality of themes, and Salatino et al. (2018) tie topic birth to rising density. Our claim (loose, churning "
    "neighbourhoods predict breadth) takes a side in a live dispute, so it must be tested against the consolidation reading, not "
    "asserted. Relatedness (Hidalgo 2007) is the default model of diversification and is not a contribution. "
    "(2) WHAT CONVINCES. A temporal out-of-sample cohort that no selection step has touched, scored once from a sealed specification. "
    "Controls for the confounds a reviewer names first: concept TYPE (methods travel; Leydesdorff & Rafols 2011 'research "
    "technologies'), pre-existing generic terms, and volume. Replication within strata, with I2 reported. A within-unit design (concept "
    "fixed effects) with pre-trend checks, placebos and the reverse path, before any temporal 'mechanism' is claimed; staggered event "
    "studies need heterogeneity-robust estimators (Sun & Abraham 2021; Callaway & Sant'Anna 2021). Case studies are chosen from the "
    "quantitative extremes, not cherry-picked. "
    "(3) STANDARD MOVES, AND WHAT EACH RULES OUT. Rarefied O2r and O2r_resid rule out volume. Partial correlation given B5 rules out "
    "'just popularity'. Held-out fields plus a later cohort rule out tuning to domain and period. Concept-level resampling rules out "
    "pseudo-replication across episodes. Leave-one-group-out and DL pooling stop one field from driving the average. Degree-preserving "
    "or label permutations rule out 'any structure works'. "
    "(4) FAILURE MODES, most of them already observed in this run. Mechanical coupling: an indicator built from the same papers whose "
    "spread is the outcome (an all-papers ego network gains off-home topics precisely when the concept spreads). Pre-onset footprint "
    "leaking into 'early' features (M0_density_end). Selection and scoring on the same concepts (H3 shrank from 0.14 to 0.03). Results "
    "that depend on the backbone or proximity (the retained frontier reversed under min-cp). Post-unseal subgroup hunting. A record "
    "whose text contradicts its own files (the review's BLOCKING items). Unexecuted artifacts that were never recorded (Exp9)."
)

principle_alignment = (
    "FOLLOWS. (a) Fresh confirmation body: the 2015-2016 onset cohort is new concepts, found with the identical grounding and newborn "
    "rule. The whole EXP5 frame becomes selection data, the specification is hash-sealed before any cohort outcome exists, and the "
    "cohort is scored once (Art 1). The fallback to 2017 onsets is declared now. (b) Confounds tested so that they can win: a "
    "HOME-ONLY ego build against mechanical coupling, a size-matched all-papers build, LLM concept type with a benchmark and hand "
    "checks, pre-onset footprint and generic-term flags, label coverage and home FE, and a within-type requirement (Art 1). (c) The "
    "mechanism is shown within concepts: concept and year FE, the reverse path, a heterogeneity-robust event study with pre-trends, "
    "and a placebo (Art 2). The where-do-new-partners-come-from decomposition makes 'why it works' a measured statement (Art 2). "
    "(d) The failed RQ2 artifact is re-run unchanged in substance, with the naming rule (DTW-HMM ARI >= 0.5 and survival without "
    "Medicine homes) kept (Art 3). (e) Case studies are matched pairs from the extremes (Art 3). (f) The record is repaired from files, "
    "with source keys (Art 4). (g) Novelty is checked against the nearest neighbours before the paper claims anything: Callon's "
    "strategic diagram, patent generality, Cheng 2023, Uzzi/Foster novelty and structural diversity (Art 5). "
    "BREAKS ON PURPOSE. (1) The cohort's outcome window (2021-2024) straddles the MAG-to-OpenAlex ingestion change, and 2024 is still "
    "filling. We accept this because it is the only never-screened body available. To keep it credible, outcomes are rarefied or "
    "year-normalised, label coverage is a ladder rung, 2015 onsets also get a <= 2022 outcome sensitivity (t0+5..t0+7), and the "
    "fallback is declared in advance. (2) The mechanism and trajectory work (Arts 2-3) reuses the EXP5 concepts, whose held-out "
    "outcomes are already unsealed. We accept this because the within-concept timing estimand was never tested, and concept FE absorb "
    "type and footprint by construction. These results are labelled mechanism evidence, not confirmation, and DEV and old held-out are "
    "reported separately. (3) The held-out for the cohort is TEMPORAL, not new fields: every field was seen during selection. This is "
    "the standard forecasting hold-out, and it is the only one left that no screen has touched. The field-transfer evidence stays the "
    "Exp8 held-out table, reported per group with its I2. (4) The legacy MAG/OpenAlex vocabulary keeps its survivorship condition (a "
    "concept had to be named by about 2021). This is stated as a limitation and partly handled by the generic-term flag. (5) The "
    "Boundary/specification-curve analysis in Art 4 runs on old held-out data after unsealing. It is explicitly exploratory, and it "
    "is frozen before the cohort is scored so that it cannot steer the confirmation."
)

objective = (
    "Turn the Exp8 lead into the paper's headline, or retire it cleanly: 'concepts whose early co-occurrence neighbourhood stays OPEN "
    "(new partners from many communities, loose and churning ego network, disciplinary contacts spread thinly) become broadly "
    "integrated; those that consolidate early stay local, even at equal growth'. We attack it on four sides at once. REPLICATION on a "
    "never-screened 2015-16 onset cohort. CONFOUND: concept type, generic terms, pre-onset footprint and mechanical coupling via a "
    "home-only build. MECHANISM: within-concept closure precedes an entry slowdown, and the new partners come from specific places. "
    "BOUNDARY: per group, construction and specification. In parallel we deliver the missing RQ2 pieces (typology, contact-vs-retention "
    "decomposition, home-prominence-vs-intersection sequence, case studies, AI stage-1 atlas) and a repaired, file-traceable record. "
    "The prior-art check tells the paper exactly what is new."
)

rationale = (
    "The latch object is fixed. Exp8 (art_dFQ6jbgNsR6Q) found that six openness components predict held-out size-adjusted breadth "
    "given B5 (new_edge_rate +0.118 with 0 sign flips; n_comm_W3 +0.167; participation +0.150; NOV_res +0.139; ego_density_W3 -0.102; "
    "edge_persistence -0.080, pre-registered), and that RETENTION_RATIO_early is negative (-0.120). Every consolidation account this run "
    "pre-registered failed: A*_h, gateway retention, and the retained frontier (a volume-matched null, reversal under min-cp). It is "
    "still a LEAD. Apart from P2 it was assembled after the unseal. Concept type and generic terms are untested. The all-papers ego "
    "network is mechanically coupled to spread. I2 reaches 0.78, and LIFEENV is weak. So this iteration does not widen. It spends one "
    "artifact on each thing that could still kill or bound the lead. Art 1 (the decisive one) does replication plus the confound "
    "ladder on fresh concepts. Art 2 tests the mechanism within concepts, where concept type and footprint are absorbed by fixed "
    "effects, and decomposes where new partners come from. Art 3 is the FIX: the failed Exp9 RQ2 artifact, re-run with its "
    "pre-registration inverted to the openness account, plus case studies and the AI atlas the request asks for. Art 4 is the "
    "reviewer's blocking record repair, plus a boundary/specification analysis of the lead on existing arrays. Art 5 is the "
    "nearest-neighbour novelty check, because Callon's density-centrality diagram and patent 'generality' are obvious precursors that "
    "have to be named. Everything is zero-credit. The OpenRouter plan is under $5 of the $20 phase pot. INFORMATIVE EITHER WAY: if "
    "concept type absorbs OPEN, the portable RQ1 signal is type, with openness as its network marker. If HOME-ONLY fails while "
    "ALL-PAPERS holds, the Exp8 signal is mechanical, and that is reported as a measurement warning for co-occurrence emergence "
    "indicators. Iteration 5 can then write the paper, or run one targeted follow-up."
)

art1 = {
    "type": "experiment",
    "objective": (
        "DECISIVE REPLICATION + CONFOUND TEST of the openness claim (RQ1) on a fresh 2015-2016 onset cohort that no screen has "
        "touched. Does HOME-ONLY OPEN keep a positive partial association with size-adjusted breadth (O2r_m50, O2r_resid at "
        "t0+6..t0+8) through the full control ladder (B5 -> +CONTACT_REACH -> +CONCEPT TYPE -> +PRE-ONSET FOOTPRINT -> +label "
        "coverage -> +home-group FE)? Does it hold within method concepts and within object concepts? Is RETENTION_RATIO_early "
        "negative? Secondary: replicate the frozen Exp8 learned models and the n_authors_early leads."
    ),
    "approach": (
        PATHS + SHARED +
        "STEP 0, PRE-REGISTRATION FIRST. Write prereg.md + frozen_spec.json holding the OPEN definition and signs, the ladder, the "
        "groups, the success rules below and the fallback. Hash them. "
        "STEP 1, COHORT FRAME, from EXP5 scan/agg_counts.parquet (years <= t0 only for selection). Candidates are legacy concepts "
        "NOT in EXP5 frame_concepts.csv, with onset t0 in {2015, 2016} under the IDENTICAL EXP5 newborn rule and TAG grounding. The "
        "newborn check may use counts through t0+2 <= 2018, exactly as frozen. Apply the EXP5 per-concept LLM precision gate with the "
        "same prompt and model, reusing scan/llm_cache. Home and groups: CS+Eng, BGM+Med, PHYS, LIFEENV, SOC, MATHDEC (MATHDEC "
        "reported only). DECLARED FALLBACK: if fewer than 800 concepts pass, add 2017 onsets with outcomes at t0+5..t0+7. "
        "STEP 2, ONE ZERO-CREDIT SNAPSHOT PASS (adapt EXP8 passA.py; the matcher and grounding stay unchanged). For cohort concepts, "
        "take every grounded work 2012-2024: work id, year, primary source id (-> venue field via source_field.parquet), topic ids, "
        "author ids and referenced_works. Check that yearly counts <= 2022 reproduce agg_counts exactly (else stop and log). If time "
        "allows, run a second pass (EXP8 passB.py) for O4 citations to early works; O4 is the first thing dropped. "
        "STEP 3, FEATURES over t0..t0+2 only, for the cohort AND the EXP5 frame (EXP5 home-only builds come from "
        "data/frame_matches_early + source_field, with no new pass). OPEN in all three builds, via Exp8 lib/ego.py on EXP3 backbone "
        "slice2 (2010-14, pre-onset for the cohort, so leakage-free). Skip betweenness in the home-only and size-matched builds (it is "
        "not in OPEN, and it cost 98% of ego time). Parallelise across 7 vCPUs. Also compute each OPEN component alone, "
        "RETENTION_RATIO_early, CONTACT_REACH, B5, n_authors_early and every Exp8 indicator needed by the frozen models/*.joblib. "
        "STEP 4, CONCEPT TYPE (LLM; cap $3). Label all EXP5 + cohort concepts (about 14.5k) with a cheap OpenRouter model. The input "
        "is the concept label, its Wikidata description where the art_O7Dq4L02QnDN key has it, and 3 early titles. There are 4 "
        "classes: method/technique/tool; object/material/organism/disease; property/measure/theory; topic/field. A separate flag marks "
        "GENERIC pre-existing terms (e.g. 'Coefficient of variation'). BENCHMARK: 300 concepts stratified by group are double-labelled "
        "by a second model, and 60 are hand-checked by the executor. Required: precision >= 0.85 on method-vs-object. If this fails, "
        "revise the prompt once; if it fails again, restrict within-type tests to two-model-agreement concepts and log it. "
        "STEP 5, PRE-ONSET FOOTPRINT from agg_counts (years < t0): log grounded papers t0-10..t0-1, number of fields pre-t0, a "
        "re-emergence flag (any pre-t0 year >= 25% of the t0+2 count), and Wikipedia creation year < t0 from art_O7Dq4L02QnDN "
        "(year_usable only) as a generic-term marker. "
        "STEP 6, SELECTION ON EXP5 (all 12,499). Confirm the signs of OPEN (every build) and fit the ladder on O2r_m50 and O2r_resid. "
        "Freeze the z constants, the O2r_resid a/b (Exp8 o2r_resid_fit.json), the type classifier outputs, the Holm family (OPEN_home, "
        "OPEN_all, OPEN_sizematched, RETENTION_RATIO x 2 outcomes) and the rules. Write frozen_spec.json and hash it into "
        "logs/seal.log. Record here, as selection-data results, the EXP5 ladder with concept type and footprint (the first test of "
        "confound (ii) on the old data). "
        "STEP 7, ONLY THEN compute cohort outcomes: O2r_m50 (exact hypergeometric), O2r_resid, O1c, O1b, O3 and O4 at t0+6..t0+8. "
        "For 2015 onsets only, also a <= 2022 sensitivity at t0+5..t0+7. Hash the outcome file and score ONCE. REPORT the partial "
        "Spearman of each OPEN build at every ladder rung (concept bootstrap 2,000), per group with DL pooling and I2, within method "
        "and within object concepts, and for each OPEN component alone. Also RETENTION_RATIO_early given B5, and the ALL-vs-HOME-ONLY "
        "difference with a paired bootstrap. SECONDARY (frozen, no refit): Exp8 O3 L1-logit dAUC over B5, n_authors_early for "
        "O3/O1b/O1c, O4 EBM Spearman, O2r ElasticNet gain over B5, and CONTACT_REACH (with and without intersection-born concepts). "
        "Missing model inputs are imputed at the frozen DEV median. A replication is dropped if more than 20% of its model weight is "
        "imputed. VERDICT RULES (frozen). CONFIRMED if HOME-ONLY OPEN has psp > 0 with CI > 0 at the type and footprint rungs, a "
        "positive sign in >= 4 of 5 groups, psp > 0 within both method and object concepts, and RETENTION_RATIO_early < 0 given B5. "
        "DISCONFIRMED if the CI at the type rung includes 0. Outcomes (a) 'type absorbs OPEN' and (b) 'home-only fails, all-papers "
        "holds = mechanical' are reported as stated. No subgroup hunting after the unseal. DROP ORDER if time is short: O4/Pass B, "
        "then the learned-model replications, then the 2017 fallback extension. Never drop the home-only build, the type rung, or the "
        "single unseal. OUTPUTS: cohort_frame.csv, concept_types.csv (both frames; reusable), type_benchmark.json, footprint.csv, "
        "features_cohort.parquet, features_exp5_homeonly.parquet, frozen_spec.json + logs/seal.log, outcomes_cohort.parquet (hashed), "
        "cohort_result.json (every rung, group, type and CI), ladder and forest figures, and method_out.json with per-concept "
        "predictions."
    ),
    "what_it_would_show": (
        "On about 1,500-2,500 never-screened 2015-16 concepts, an openness index built only from HOME-field papers in the first three "
        "years predicts size-adjusted breadth six to eight years later: partial rho about +0.10 to +0.15 given B5, CI > 0 after "
        "controlling for concept type and pre-onset footprint, positive in >= 4 of 5 field groups and within both method and object "
        "concepts, while the share of contacted fields that keep the concept is negatively related (about -0.1). This is RQ1's portable, "
        "non-mechanical early network signal, confirmed out of sample."
    ),
    "depends_on": [
        {"id": "art_O7Dq4L02QnDN", "label": "concept key"},
    ],
}

art2 = {
    "type": "experiment",
    "objective": (
        "MECHANISM of the openness effect (RQ2 timing and 'why it works'), within concepts on the EXP5 frame. (a) Does a concept's "
        "home-only neighbourhood CLOSING in year t lower its off-home field-entry hazard in t+1, with concept and year FE, when the "
        "reverse path (entry -> later closure) is weaker and pre-trends are flat? (b) Where do the new partners that carry the "
        "new_edge_rate / n_comm_W3 signal come from: method-topic vs domain-topic communities, home vs off-home fields, and which "
        "bridging papers bring them? (c) The request's sequence question: does home-community prominence peak BEFORE off-home entry "
        "take-off, or do intersection-born concepts (>= 2 homes) diffuse without it?"
    ),
    "approach": (
        PATHS + SHARED +
        "STEP 1, ONE ZERO-CREDIT SNAPSHOT PASS (EXP8 passA.py with the window extended; matcher and grounding unchanged). For the 12,499 "
        "EXP5 concepts, collect grounded works t0..min(t0+10, 2022): work id, year, source -> venue field, topic ids, author ids and "
        "document type. Check that counts reproduce agg_counts exactly. Also build the D3 yearly states from EXP7 "
        "state_panel_{dev,heldout}.parquet (authoritative). "
        "STEP 2, YEARLY PANEL (concept x year, t0..t0+10). Home-only openness(t) uses 1-year windows via Exp8 lib/ego.py on the "
        "time-appropriate EXP3 backbone slice (the slice before or containing t; no betweenness): new-partner rate, n_comm, "
        "participation, ego density, edge persistence, plus the OPEN_home composite with frozen EXP5 z constants. Controls: log "
        "home-paper volume(t), log total volume(t), concept age, and entries already made. Outcome: number of NEW off-home fields "
        "ENTERED in t+1 (D3), plus the binary any-entry hazard. Parallelise across 7 vCPUs. "
        "STEP 3, PRE-REGISTER BEFORE ESTIMATION (frozen_spec.json hashed). Primary: Poisson (or LPM) with concept FE and year FE, "
        "entries(t+1) on home-only ego density(t), and separately on OPEN_home(t). Prediction: density beta < 0 and OPEN beta > 0, "
        "concept-clustered CIs excluding 0. Reverse path: home-only density(t+1) on entries(t), same FE. Prediction: weaker in "
        "standardised terms (paired bootstrap of |beta| difference). Event study: the event is the first home-only CLOSURE JUMP (a "
        "within-concept rise in ego density >= 1 within-concept SD, first occurrence at age >= 2). Leads -3..-1 and lags 0..+4, "
        "estimated with the Sun & Abraham (2021) interaction-weighted estimator, with never-treated and not-yet-treated controls. "
        "Pre-trend joint test. Placebo: event year permuted within concept (1,000 draws), plus a within-concept-year permutation of "
        "the field labels of entries. Report DEV and old held-out separately (labelled mechanism evidence, not confirmation), and "
        "report excluding Medicine homes and excluding intersection-born concepts. "
        "STEP 4, WHY IT WORKS (partner-source decomposition, early window t0..t0+2). Label the OpenAlex topics that appear as "
        "partners as METHOD/TECHNIQUE vs DOMAIN/PHENOMENON with a cheap LLM (about 4.5k topics; 100 double-labelled; 40 hand-checked; "
        "cap $1). For every new partner, record: method vs domain; partner topic's field = home or off-home; Leiden community "
        "(EXP3) = the concept's first-year modal community or a new one; carrying paper's venue field home or off-home. Recompute "
        "new_edge_rate and n_comm_W3 restricted to each partner class, and report each class's partial Spearman with O2r_m50 given "
        "B5 (old held-out, from Exp8 outcomes; exploratory). This shows which partner class carries the signal and whether it survives "
        "when only HOME-venue papers deliver the new partners. BRIDGING PAPERS: papers that introduce >= 1 partner from a new "
        "community. Report their share, team size, share of authors new to the concept, document type (review vs article), and "
        "whether early bridging-paper share predicts O2r given B5. "
        "STEP 5, SEQUENCE TEST (RQ2). Home prominence(t) = within-home percentile rank of the concept's home-only degree and k-core "
        "among all frame concepts sharing that home in year t. Off-home take-off = the first year with >= 2 new off-home entries. "
        "Event-study both orders (prominence peak -> take-off; take-off -> prominence), with pre-trends. Compare single-home with "
        "intersection-born concepts on time to take-off, and on whether a prominence peak precedes take-off (share, concept "
        "bootstrap). Frozen prediction: intersection-born concepts take off without a prior home-prominence peak more often than "
        "single-home concepts. OUTPUTS: yearly_panel.parquet (reusable in iteration 5), fe_results.json, event_study.json with "
        "figures, partner_decomposition.json, topic_types.csv, bridging_papers.parquet, sequence_tests.json, frozen_spec.json + seal "
        "log, and method_out.json."
    ),
    "what_it_would_show": (
        "Within the same concept, a year in which its home neighbourhood closes is followed by fewer new-field entries (FE beta < 0, "
        "CI excludes 0, flat pre-trends, placebo null), while entries do not predict later closure as strongly. The breadth signal of "
        "new_edge_rate and n_comm_W3 is carried mainly by new partners from METHOD communities and from previously unlinked communities, "
        "even when they arrive through home-field papers. So openness is a leading cause-like marker, not a by-product of spread. "
        "Separately, intersection-born concepts take off without a prior home-prominence peak. This answers the request's "
        "'central-first vs intersection' question."
    ),
    "depends_on": [
        {"id": "art_O7Dq4L02QnDN", "label": "concept key"},
    ],
}

art3 = {
    "type": "experiment",
    "objective": (
        "FIX: re-run the failed iteration-3 RQ2 artifact (gen_art_experiment_9, plan 3_invention_loop/iter_3/gen_plan/"
        "gen_plan_experiment_3; never executed, its output-format loop failed). It runs on the existing EXP5/EXP7/EXP8 arrays with the "
        "pre-registration updated to the openness account. (a) A log-additive breadth decomposition: contact rate x retention "
        "probability x frontier advance, with Shapley shares. (b) An empirical trajectory typology, named only if two methods agree. "
        "(c) Matched-pair case studies from the quantitative extremes. (d) The request's stage-1 AI/CS atlas (about 40 concepts; "
        "retrospective, descriptive)."
    ),
    "approach": (
        PATHS + SHARED +
        "Cache only: NO snapshot pass, $0 LLM. FIRST write a valid method_out.json skeleton, and validate it with aii-json against "
        "exp_gen_sol_out at the MINI stage, before any long computation. Exp9 died on output-format validation, so the format is "
        "checked first and after every stage. "
        "(1) STATE SEQUENCES, t0..t0+10, from EXP7 state_panel_*.parquet and EXP5 agg_counts (D3 states: untouched / entered / "
        "retained / lost per field). Yearly summaries: contact rate (new off-home fields entered), retention probability (share of "
        "entered off-home fields that become retained), frontier advance (entries per retained field), rarefied entropy, within-home "
        "share, field-level community span on the EXP6 backbone, and the Exp8 early OPEN components (t0..t0+2) as static covariates. "
        "(2) DECOMPOSITION. log(breadth at t0+8) = log contact + log retention + log frontier (+ residual). Shapley decomposition of "
        "the top-vs-bottom O2r_resid tercile gap; adjust for Medicine homes and also exclude them. PRE-REGISTERED (frozen_spec.json, "
        "hashed, before computing): localised and integrating concepts differ MORE in contact/exploration than in retention, and "
        "localised concepts have HIGHER early retention ratios. Report the concept-bootstrap CI of the contact share minus the "
        "retention share. "
        "(3) TYPOLOGY. DTW k-medoids (k = 2..8, silhouette + gap + bootstrap stability) and a Gaussian HMM (3-5 states, BIC) on the "
        "standardised yearly vectors. A class is NAMED only if DTW-HMM ARI >= 0.5, it replicates when held-out is re-clustered, and it "
        "survives excluding Medicine homes. Otherwise report a continuum: project the trajectories on the first 2-3 principal axes and "
        "show where early OPEN sits on them (Spearman of OPEN with axis 1). Record the old typology (Exp6: 2 classes, HMM ARI 0.094) "
        "as not established. "
        "(4) CASE STUDIES. Six to eight MATCHED PAIRS seeded from Exp8 results/case_exemplars.json: same home group, early volume "
        "and growth within 0.25 SD (B5-matched), opposite OPEN (top vs bottom quintile), mixed domains and not only AI, excluding "
        "GENERIC terms by a label rule logged in deviations. For each pair: an alluvial field-flow figure of D3 states over time; "
        "early ego-network snapshots W1..W3 from data/frame_matches_early (topics coloured by EXP3 community); the O2r outcome; and "
        "external recognition dates from art_O7Dq4L02QnDN (descriptive only). "
        "(5) AI/CS ATLAS (the request's stage 1, labelled RETROSPECTIVE and DESCRIPTIVE). About 40 CS-home frame concepts with AI/ML "
        "labels, chosen to span rapid emergence, gradual growth, local specialisation, cross-disciplinary diffusion and transient "
        "expansion (O3 = 1). Yearly panels of connectivity, new neighbours, community membership, field distribution and D3 states. "
        "Include a small-multiples figure and a table stating which structural changes looked meaningful. "
        "(6) pipeline_counts.json for the methodology figure: works, concepts, episodes, risk-set rows and split sizes at every stage, "
        "read from the actual artifacts. OUTPUTS: state_sequences.parquet, decomposition.json, trajectories.json (assignments, ARI, "
        "stability, medoids, or continuum axes), case_studies/ (figures + per-pair JSON), ai_atlas/ (figures + table), "
        "pipeline_counts.json, frozen_spec.json + seal log, and a schema-valid method_out.json."
    ),
    "what_it_would_show": (
        "On about 12k concepts, what separates concepts that end broadly integrated from those that stay local is how many new fields "
        "they keep CONTACTING (Shapley share of contact > retention, CI excludes 0), not how well each field keeps them. Localised "
        "concepts in fact retain a larger share of the fields they touch. Trajectories form a continuum along the openness axis rather "
        "than robust discrete classes, unless the DTW-HMM agreement rule passes. Matched pairs with equal early growth but opposite "
        "openness show the mechanism visually. This completes RQ2 and the request's exploratory AI stage."
    ),
    "depends_on": [
        {"id": "art_O7Dq4L02QnDN", "label": "recognition dates"},
    ],
}

art4 = {
    "type": "evaluation",
    "objective": (
        "(A) Clear every BLOCKING reviewer MUST-FIX with file-traceable tables and ready-to-insert corrected text. (B) BOUNDARY of the "
        "openness lead on the existing Exp8 arrays: per-group behaviour, construction and specification robustness, and heterogeneity "
        "(why I2 is 0.75-0.78, why LIFEENV is weak). Also re-score the footprint-contaminated indicators post-onset only. The whole "
        "analysis is frozen BEFORE the Art 1 cohort unseal, so it cannot steer confirmation."
    ),
    "approach": (
        "No new data or methods; $0-0.5 LLM. Read by path: Exp8 (art_dFQ6jbgNsR6Q) results/*: heldout_unit_results.csv, "
        "portability_table.csv, prereg_verdicts.json, frozen_spec.json, learned_vs_single_heldout.json, sensitivities_pooled.json, "
        "indicator_dictionary.csv, deviations.json, README tables, data/analysis_table.parquet, indicator_matrix.parquet. Exp7 "
        "(art_22ppE1snfHKj) step2_dev.json and step2_heldout.json, deviations.json and frontier_result.json. Eval2 "
        "3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/ (art_7W9xiIO3FVBs): text_corrections.md (14 blocks), record_tables/*.csv, "
        "claims_ledger.csv, o5_validation.json and frame_agreement.json. Also 3_invention_loop/iter_3/gen_art/gen_art_experiment_9/ (and "
        ".aii_worker_result.json if present), the plan 3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3/, and the report "
        "3_invention_loop/iter_4/gen_strat/current_report.md. "
        "PART A, CORRECTIONS PACK (corrections/ with one markdown file per report section, each table followed by a 'Source: file -> "
        "key path' line). (1) Exp8 outcome relabelling: REL_home and author_growth are O4. The O3 top-10 table comes from the README. "
        "Include all 8 learned-model rows (O1c, O2r_m50, O2r_resid, O4, O1b, O3, O5, O5_WW, with n and paired CIs). Dead end 22.6 is "
        "rewritten. (2) A P1-P5 table with the EXACT frozen prediction text, the verdict and the deciding quantity. [Correction] "
        "sentences for dead end 7.4 (new_edge_rate transfers) and 4.3. A held-out table of the iteration-1 candidates (D_ratio, "
        "D_rare, participation, NOV_res, entropy, edge_persistence), with pooled psp, CI and per-group raw rho. (3) Exp7 tables from "
        "step2 JSONs: volume-matched d_R_m / d_N_m / contrast (coarse and fine; DEV and held-out; match rates and balance); dose "
        "betas with the monotone flag; d_lost A1 vs R4; d0 concept / two-way / crossed CIs; held-out sensitivities; a "
        "'Proximity dependence' subsection (min-cp d0 -0.021, p 0.012; RCA LR 246). A definitional comparison of D_rca_pers (Exp7 "
        "S_strict) with Research 2's D_rca_persist_k (equivalent or not, and why). A nearest-neighbour paragraph draft. (4) Eval2's 14 "
        "text_corrections blocks, rendered as insert-ready text marked '[Correction, iteration 3, from art_7W9xiIO3FVBs]', plus every "
        "record_tables CSV mapped to its target section. The 6 MISMATCH and 15 MISLABELLED ledger rows are listed individually. (5) "
        "A failed-artifact record for gen_art_experiment_9 (plan, failure mode, what was lost; 'not run, not refuted'). Correct "
        "iteration counts: iteration 1 completed 3 of 5, iteration 2 completed 5, iteration 3 completed 4 of 5. (6) Candidate S rows "
        "(S_comp, S_comp_n, S_isolated_share for every outcome). The six indicator families with counts from indicator_dictionary.csv "
        "and the D-family > 30%-missing exclusion rule. (7) O5 per-source leakage and lags, and the O5-O3 association per group (pooled "
        "-0.049, p 0.004, I2 0.55). (8) Minor slips (19.6 -> 20.2 cross-reference; the 18.11 count sentence). (9) claims_ledger_v3.csv: "
        "every number in the corrections pack re-read from its file, with MATCH status. "
        "PART B, BOUNDARY OF THE LEAD (exploratory, old held-out already unsealed; write boundary_spec.json and hash it first). (1) "
        "POST-ONSET RE-SCORE: M0_density_end and D_vol_end recomputed from EXP5 agg_counts using t0..t0+2 papers only, then scored "
        "held-out exactly as Exp8 scored them (psp given B5, pooled + per group). Report how much of the +0.377 / +0.307 was pre-onset "
        "footprint. (2) PER-GROUP TABLE for every confirmed O2r indicator plus the OPEN composite (all-papers, frozen EXP5-DEV z): "
        "PHYS, LIFEENV, SOC, MATHDEC, COH_DEVHOME and COH_OTHER, as rho [CI] and n, with a mark on each cell whose CI includes 0. Add "
        "the sensitivities_pooled robustness rows, including the halving of CONTACT_REACH without intersection-born concepts. (3) "
        "SPECIFICATION CURVE for OPEN: component subsets (all 63 non-empty subsets of the 6), equal vs first-PC weights, outcomes "
        "O2r_m30 / O2r_m50 / O2r_resid / O2r_resid_N, controls B5 vs B5 + coverage vs B5 + onset-year. Report the share of "
        "specifications with CI > 0 and the median psp, against a within-group outcome-permutation null (200 draws). (4) "
        "HETEROGENEITY: meta-regress the per-unit psp on unit traits (label coverage, median early volume, share multi-home, share "
        "GENERIC-looking labels by a frozen lexical rule, median O2r). Leave one group out. Test whether the weak LIFEENV cells are "
        "explained by low label coverage or by low OPEN variance (variance ratio test). OUTPUTS: eval_out.json (schema-valid), "
        "corrections/ , claims_ledger_v3.csv, post_onset_rescore.json, per_group_table.csv, spec_curve.json + figure, "
        "heterogeneity.json, boundary_spec.json + hash."
    ),
    "what_it_would_show": (
        "Every blocking review item is closed with insert-ready text and a source key. The openness lead is not a construction artifact: "
        "most of the 63-plus specifications keep CI > 0 against a permutation null. Its heterogeneity is bounded and explained, e.g. "
        "LIFEENV weakness tracks label coverage or restricted OPEN variance, not a domain reversal. M0_density_end's headline value is "
        "shown to be largely pre-onset footprint, so the paper's RQ1 headline moves to the purely post-onset openness indicators."
    ),
    "depends_on": [
        {"id": "art_dFQ6jbgNsR6Q", "label": "lead to bound"},
        {"id": "art_22ppE1snfHKj", "label": "record tables"},
        {"id": "art_wxWssKSUR45f", "label": "footprint counts"},
        {"id": "art_O7Dq4L02QnDN", "label": "O5 per source"},
    ],
}

art5 = {
    "type": "research",
    "objective": (
        "Nearest-neighbour NOVELTY CHECK for the openness-vs-consolidation claim, and paper positioning for Applied Network Science. "
        "Is 'early open, churning, multi-community co-occurrence neighbourhoods predict size-adjusted cross-field integration; early "
        "consolidation predicts staying local, at equal growth' new, partially anticipated or anticipated? What comparison numbers "
        "exist for RQ1 and RQ2 under this framing, and which works must the paper cite and distinguish?"
    ),
    "approach": (
        "Build on art_EesdB8cuSfcU and art_dxvRpQufMR0e (3_invention_loop/iter_3/gen_art/gen_art_research_2/research_report.md and "
        "iter_2/gen_art/gen_art_research_1/research_report.md). Do not repeat their relatedness, exit or venue work. For each work, "
        "record: unit, network, early-window measure, outcome, whether it is size-adjusted, whether it is held-out, and the effect "
        "size. Give a quote and a verdict (NEW / PARTIALLY ANTICIPATED / ANTICIPATED) for each of four sub-claims: C1 early "
        "new-partner rate and multi-community contact predict breadth beyond growth; C2 early ego DENSITY and edge PERSISTENCE predict "
        "LESS breadth; C3 the retention ratio of contacted fields is NEGATIVE; C4 within-concept closure precedes an entry slowdown. "
        "STRANDS. (1) Co-word strategic diagrams: density vs centrality of themes (Callon, Courtial & Laville 1991; Cobo et al. 2011 "
        "SciMAT; Coulter et al.). Do low-density themes become transversal? This is the most direct precursor. (2) Topic birth and "
        "emergence: Salatino et al. 2017/2018 (pre-emergence density, the opposite direction?), Small, Boyack & Klavans 2014, Rotolo "
        "2015, Chen 2009/2012 structural variation, Xu et al. 2021 and Liang et al. (3) Diffusion of ideas and concepts: Cheng et al. "
        "2023 ASR. Extract EXACTLY how 'consistent usage' and 'fit' are operationalised: does consistent usage mean a STABLE semantic "
        "context, and does our result contradict it for breadth? Also Kuhn, Perc & Helbing 2014 (memes), Sun et al. 2013 (social "
        "dynamics of science), Mao et al. 2020 and Maillart et al. 2026. (4) Recombination and novelty: Uzzi et al. 2013 atypical "
        "combinations; Foster, Rzhetsky & Evans 2015; Wang, Veugelers & Stephan 2017; Shi & Evans 2023; Tria et al. 2014 and "
        "Iacopini et al. 2018 (adjacent possible, network of novelties); Hofstra et al. 2020. (5) Structural diversity and virality: "
        "Ugander et al. 2012; Weng, Menczer & Ahn 2013; Centola 2010/2018; Burt constraint and closure vs brokerage. (6) General "
        "purpose technologies: the patent GENERALITY index (Trajtenberg, Henderson & Jaffe 1997; Hall & Trajtenberg 2004; Bresnahan & "
        "Trajtenberg 1995). Is early generality known to predict later diffusion? (7) Methods vs objects: Leydesdorff & Rafols 2011 "
        "research technologies; studies of method diffusion across fields (e.g. methods papers and their cross-field citation; "
        "entity/method extraction diffusion studies). This supports or undermines the concept-TYPE confound. (8) "
        "Exploration-exploitation and boundary objects applied to science: March 1991; Star & Griesemer 1989; Foster 2015; Fujimura. "
        "(9) Within-unit timing: any panel or event-study evidence that neighbourhood closure precedes diffusion slowdown (topic "
        "lifecycle, 'Social dynamics of science' splits and merges). ALSO: (a) an RQ1 comparison table with numbers (metric, horizon, "
        "held-out design, size-adjusted?, value; mark level AUCs as not comparable), and an RQ2 comparison table (trajectory classes, "
        "decompositions, sequence findings); (b) up to 8 ANS papers (2016-2026) on co-occurrence / knowledge-network evolution to cite "
        "in Related Work, each with a one-line relation; (c) an updated Fig. 1 methodology spec for the openness framing (lanes: "
        "grounding -> frames/cohorts -> three ego builds -> indicator families -> selection/seal -> fresh cohort -> within-concept "
        "mechanism -> trajectories), with the counts to be filled from pipeline_counts.json; (d) a 'threats a reviewer will raise' list "
        "with the literature answer to each; (e) a verified reference list with a DOI or arXiv ID for every entry (Semantic Scholar "
        "fetchable) and UNVERIFIED flags."
    ),
    "what_it_would_show": (
        "The paper can state precisely that open, multi-community early co-occurrence neighbourhoods predicting size-adjusted "
        "cross-field integration, and early consolidation predicting localisation, is NEW or only PARTIALLY ANTICIPATED (by Callon's "
        "density-centrality diagram, patent generality and Weng/Ugander structural diversity). It will cite quotes, and it will show "
        "how the result refines Cheng et al. 2023's 'consistent usage' and Salatino's pre-emergence density rather than duplicating "
        "them. It will also have per-RQ comparison numbers and a finished methodology-figure spec."
    ),
    "depends_on": [],
}

strategy = {
    "domain_reasoning": domain_reasoning,
    "principle_alignment": principle_alignment,
    "title": "Do open early neighbourhoods really predict spread?",
    "objective": objective,
    "rationale": rationale,
    "artifact_directions": [art1, art2, art3, art4, art5],
    "expected_outcome": (
        "(1) A single, sealed, out-of-sample verdict on the openness claim from a never-screened 2015-16 cohort. It will include "
        "home-only vs all-papers vs size-matched builds, the full confound ladder with LLM concept type (benchmarked) and pre-onset "
        "footprint, within-type estimates, per-group DL pooling with I2, and replications of the Exp8 learned models and "
        "n_authors_early. Reusable concept_types.csv for both frames. (2) Within-concept mechanism evidence: FE closure -> entry "
        "hazard with the reverse path, a Sun-Abraham event study with pre-trends and placebos, a decomposition of where new partners "
        "come from (method vs domain, home vs off-home, bridging papers), and a test of the request's 'central-first vs intersection' "
        "sequence question, all on a reusable yearly panel. (3) RQ2 finally on about 12k concepts: the contact x retention x frontier "
        "Shapley decomposition, a typology named only under DTW-HMM agreement or else a continuum along the openness axis, matched-pair "
        "case studies, the AI/CS stage-1 atlas and pipeline counts for Fig. 1. (4) A corrections pack that closes every blocking "
        "review item with source keys, a post-onset re-score of the footprint indicators, a per-group table and specification curve "
        "for the lead, and a heterogeneity diagnosis. (5) A novelty verdict per sub-claim with quotes, comparison tables and a "
        "methodology-figure spec. With these, iteration 5 writes the ANS paper, with openness either CONFIRMED, or re-scoped to "
        "'concept type with openness as its marker', or reported as a mechanical measurement warning."
    ),
    "summary": (
        "Iteration 4 latches onto the one lead that survived held-out testing: new concepts whose early co-occurrence neighbourhood "
        "stays open spread widest. Five bets attack it from every side. (1) A decisive confirmation on a fresh, never-screened "
        "2015-16 cohort, with a home-only build against mechanical coupling and LLM concept type and footprint controls. (2) "
        "Within-concept mechanism and partner-source decomposition. (3) A re-run of the failed RQ2 trajectory artifact, with case "
        "studies and the AI atlas. (4) A boundary analysis plus the reviewer's blocking record repair. (5) A nearest-neighbour novelty "
        "check. All use zero API credits and under $5 of LLM."
    ),
}

out = {"strategies": [strategy]}
(HERE / ".terminal_claude_agent_struct_out.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
print("directions:", len(strategy["artifact_directions"]))
```

### [21] TOOL RESULT — Write · 2026-09-29 02:06:18 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_strat/gen_strat_1/build_strategy.py", "content": "\"\"\"Builds .terminal_claude_agent_struct_out.json (the iteration-4 strategy) from plain Python strings.\"\"\"\nimport json\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n\nRUN = \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M\"  # only used inside executor instructions (read-only inputs)\n\nPATHS = (\n    \"INPUTS ARE READ BY PATH (run root = the run directory; experiments may formally depend only on datasets/research, so \"\n    \"earlier experiments are reused by path). EXP5 = 3_invention_loop/iter_2/gen_art/gen_art_experiment_5/ (art_wxWssKSUR45f): \"\n    \"frame_concepts.csv (12,499), concept_outcomes.csv, frozen_spec.json (split/folds), scan/agg_counts.parquet (concept ci x year \"\n    \"1995-2022 x venue field x tagstate counts for ALL 56,643 legacy concepts), scan/year_field_totals.npz, scan/co_by_year.npz, \"\n    \"scan/llm_cache (precision-gate cache), results/source_field.parquet (source -> venue field), matcher.py, grounding.py, \"\n    \"rangefile.py, scan_full.py. EXP8 = 3_invention_loop/iter_3/gen_art/gen_art_experiment_8/ (art_dFQ6jbgNsR6Q): passA.py, passB.py, \"\n    \"lib/ego.py + lib/ego_ctx.py (EXP3 ego features ported, 1-year windows W1..W3, validated to 1e-15), lib/matcher.py, lib/rangefile.py, \"\n    \"build_features.py, outcomes.py, data/frame_matches_early/part_*.parquet (grounded hits t0-3..t0+2 with work, topic, author ids), \"\n    \"data/cites_early.parquet, data/ref_sample.parquet, data/bg_topics.npz, data/features_basic.parquet, data/ego_features.parquet, \"\n    \"data/outcomes.parquet, data/analysis_table.parquet, results/indicator_matrix.parquet, results/indicator_dictionary.csv, \"\n    \"results/frozen_spec.json, results/heldout_unit_results.csv, results/portability_table.csv, results/case_exemplars.json, \"\n    \"results/o2r_resid_fit.json, models/*.joblib (frozen ElasticNet/L1-logit and EBM per outcome). EXP7 = \"\n    \"3_invention_loop/iter_3/gen_art/gen_art_experiment_7/ (art_22ppE1snfHKj): results/state_panel_{dev,heldout}.parquet (authoritative \"\n    \"D3 concept x field x year states), step2_{dev,heldout}.json. EXP6 = 3_invention_loop/iter_2/gen_art/gen_art_experiment_6/ \"\n    \"(art_N-mpomDZZ1ln): lib/h2.py (ENTERED/RETAINED/LOST), lib/traj.py, inputs/field_backbone.json (26-field PMI backbone 1998-2002). \"\n    \"EXP3 = 3_invention_loop/iter_1/gen_art/gen_art_experiment_3/ (art_yrradSC27HtQ): backbone/slice0-2.npz (topic PMI slices \"\n    \"2000-04/05-09/10-14, Leiden gamma 3). If the run volume is not mounted, re-implement from these definitions against the public \"\n    \"zero-credit OpenAlex S3 snapshot with the same HTTP-range code and log every deviation in deviations.json. \"\n)\n\nSHARED = (\n    \"SHARED DEFINITIONS (verbatim in every artifact). OPEN components over t0..t0+2 papers only, Exp8 lib/ego.py code: new_edge_rate, \"\n    \"n_comm_W3, participation, NOV_res, ego_density_W3, edge_persistence. OPEN = mean of z(new_edge_rate), z(n_comm_W3), \"\n    \"z(participation), z(NOV_res), -z(ego_density_W3), -z(edge_persistence), with z constants frozen on the EXP5 frame (all 12,499 \"\n    \"concepts = SELECTION data); a concept needs >= 4 of 6 components. Builds: ALL-PAPERS (as Exp8); HOME-ONLY (ego network from the \"\n    \"concept's grounded papers whose venue field is in its home set; venue-unlabelled papers excluded; home-paper coverage logged); \"\n    \"SIZE-MATCHED ALL-PAPERS (mean over 20 random subsamples of all early papers down to the home-only paper count; separates 'fewer \"\n    \"papers' from 'home restriction'). RETENTION_RATIO_early and CONTACT_REACH as in Exp8 (reported separately, not in OPEN). B5 = log \"\n    \"early volume, early growth, off-home share, entropy, reach (Exp8). Home = field(s) with >= 40% of the first 30 grounded works \"\n    \"(>= 2 homes = intersection-born). D3 states from EXP6 lib/h2.py. STATISTICS: resampling unit = concept (named in every table); \"\n    \"2,000-draw concept bootstraps (refit); DerSimonian-Laird pooling with I2; Holm within each pre-declared family. SEALING: \"\n    \"frozen_spec.json (formulas, signs, thresholds, covariates, code SHA-256) written and hashed into logs/seal.log BEFORE any outcome \"\n    \"of the evaluation body is computed; that body is scored once. BUDGET: 0 OpenAlex API credits (zero-credit S3 snapshot only); \"\n    \"OpenRouter spend capped per artifact as stated, running total from usage.cost, stop on the first 'AI Inventor per-run OpenRouter \"\n    \"budget' 403. \"\n)\n\ndomain_reasoning = (\n    \"FIELD: scientometrics / science of science using network-science methods (target: Applied Network Science, collection \"\n    \"'Networks for everyday life'). No domain handbook fits (the four offered cover computational linguistics, mech-interp, multi-agent \"\n    \"LLMs and neuro-symbolic AI), so the principles below are provisional. They rest on the literature this run has already read and \"\n    \"verified (art_dxvRpQufMR0e: 22 ANS papers, Guevara 2016, Weng 2013, Maillart 2026; art_EesdB8cuSfcU: relatedness/exit prior art, \"\n    \"ANS skeleton) and on this run's own measured failure modes. \"\n    \"(1) PRINCIPLES. There is no single ground truth for emergence (Rotolo, Hicks & Martin 2015), so a signal is believed only when it \"\n    \"predicts several later outcomes beyond count baselines. Fields differ in size and citing habits, so breadth must be volume-adjusted \"\n    \"(rarefaction, residualisation), otherwise it relabels growth. Co-word analysis has argued since Callon et al. (1991) about \"\n    \"density versus centrality of themes, and Salatino et al. (2018) tie topic birth to rising density. Our claim (loose, churning \"\n    \"neighbourhoods predict breadth) takes a side in a live dispute, so it must be tested against the consolidation reading, not \"\n    \"asserted. Relatedness (Hidalgo 2007) is the default model of diversification and is not a contribution. \"\n    \"(2) WHAT CONVINCES. A temporal out-of-sample cohort that no selection step has touched, scored once from a sealed specification. \"\n    \"Controls for the confounds a reviewer names first: concept TYPE (methods travel; Leydesdorff & Rafols 2011 'research \"\n    \"technologies'), pre-existing generic terms, and volume. Replication within strata, with I2 reported. A within-unit design (concept \"\n    \"fixed effects) with pre-trend checks, placebos and the reverse path, before any temporal 'mechanism' is claimed; staggered event \"\n    \"studies need heterogeneity-robust estimators (Sun & Abraham 2021; Callaway & Sant'Anna 2021). Case studies are chosen from the \"\n    \"quantitative extremes, not cherry-picked. \"\n    \"(3) STANDARD MOVES, AND WHAT EACH RULES OUT. Rarefied O2r and O2r_resid rule out volume. Partial correlation given B5 rules out \"\n    \"'just popularity'. Held-out fields plus a later cohort rule out tuning to domain and period. Concept-level resampling rules out \"\n    \"pseudo-replication across episodes. Leave-one-group-out and DL pooling stop one field from driving the average. Degree-preserving \"\n    \"or label permutations rule out 'any structure works'. \"\n    \"(4) FAILURE MODES, most of them already observed in this run. Mechanical coupling: an indicator built from the same papers whose \"\n    \"spread is the outcome (an all-papers ego network gains off-home topics precisely when the concept spreads). Pre-onset footprint \"\n    \"leaking into 'early' features (M0_density_end). Selection and scoring on the same concepts (H3 shrank from 0.14 to 0.03). Results \"\n    \"that depend on the backbone or proximity (the retained frontier reversed under min-cp). Post-unseal subgroup hunting. A record \"\n    \"whose text contradicts its own files (the review's BLOCKING items). Unexecuted artifacts that were never recorded (Exp9).\"\n)\n\nprinciple_alignment = (\n    \"FOLLOWS. (a) Fresh confirmation body: the 2015-2016 onset cohort is new concepts, found with the identical grounding and newborn \"\n    \"rule. The whole EXP5 frame becomes selection data, the specification is hash-sealed before any cohort outcome exists, and the \"\n    \"cohort is scored once (Art 1). The fallback to 2017 onsets is declared now. (b) Confounds tested so that they can win: a \"\n    \"HOME-ONLY ego build against mechanical coupling, a size-matched all-papers build, LLM concept type with a benchmark and hand \"\n    \"checks, pre-onset footprint and generic-term flags, label coverage and home FE, and a within-type requirement (Art 1). (c) The \"\n    \"mechanism is shown within concepts: concept and year FE, the reverse path, a heterogeneity-robust event study with pre-trends, \"\n    \"and a placebo (Art 2). The where-do-new-partners-come-from decomposition makes 'why it works' a measured statement (Art 2). \"\n    \"(d) The failed RQ2 artifact is re-run unchanged in substance, with the naming rule (DTW-HMM ARI >= 0.5 and survival without \"\n    \"Medicine homes) kept (Art 3). (e) Case studies are matched pairs from the extremes (Art 3). (f) The record is repaired from files, \"\n    \"with source keys (Art 4). (g) Novelty is checked against the nearest neighbours before the paper claims anything: Callon's \"\n    \"strategic diagram, patent generality, Cheng 2023, Uzzi/Foster novelty and structural diversity (Art 5). \"\n    \"BREAKS ON PURPOSE. (1) The cohort's outcome window (2021-2024) straddles the MAG-to-OpenAlex ingestion change, and 2024 is still \"\n    \"filling. We accept this because it is the only never-screened body available. To keep it credible, outcomes are rarefied or \"\n    \"year-normalised, label coverage is a ladder rung, 2015 onsets also get a <= 2022 outcome sensitivity (t0+5..t0+7), and the \"\n    \"fallback is declared in advance. (2) The mechanism and trajectory work (Arts 2-3) reuses the EXP5 concepts, whose held-out \"\n    \"outcomes are already unsealed. We accept this because the within-concept timing estimand was never tested, and concept FE absorb \"\n    \"type and footprint by construction. These results are labelled mechanism evidence, not confirmation, and DEV and old held-out are \"\n    \"reported separately. (3) The held-out for the cohort is TEMPORAL, not new fields: every field was seen during selection. This is \"\n    \"the standard forecasting hold-out, and it is the only one left that no screen has touched. The field-transfer evidence stays the \"\n    \"Exp8 held-out table, reported per group with its I2. (4) The legacy MAG/OpenAlex vocabulary keeps its survivorship condition (a \"\n    \"concept had to be named by about 2021). This is stated as a limitation and partly handled by the generic-term flag. (5) The \"\n    \"Boundary/specification-curve analysis in Art 4 runs on old held-out data after unsealing. It is explicitly exploratory, and it \"\n    \"is frozen before the cohort is scored so that it cannot steer the confirmation.\"\n)\n\nobjective = (\n    \"Turn the Exp8 lead into the paper's headline, or retire it cleanly: 'concepts whose early co-occurrence neighbourhood stays OPEN \"\n    \"(new partners from many communities, loose and churning ego network, disciplinary contacts spread thinly) become broadly \"\n    \"integrated; those that consolidate early stay local, even at equal growth'. We attack it on four sides at once. REPLICATION on a \"\n    \"never-screened 2015-16 onset cohort. CONFOUND: concept type, generic terms, pre-onset footprint and mechanical coupling via a \"\n    \"home-only build. MECHANISM: within-concept closure precedes an entry slowdown, and the new partners come from specific places. \"\n    \"BOUNDARY: per group, construction and specification. In parallel we deliver the missing RQ2 pieces (typology, contact-vs-retention \"\n    \"decomposition, home-prominence-vs-intersection sequence, case studies, AI stage-1 atlas) and a repaired, file-traceable record. \"\n    \"The prior-art check tells the paper exactly what is new.\"\n)\n\nrationale = (\n    \"The latch object is fixed. Exp8 (art_dFQ6jbgNsR6Q) found that six openness components predict held-out size-adjusted breadth \"\n    \"given B5 (new_edge_rate +0.118 with 0 sign flips; n_comm_W3 +0.167; participation +0.150; NOV_res +0.139; ego_density_W3 -0.102; \"\n    \"edge_persistence -0.080, pre-registered), and that RETENTION_RATIO_early is negative (-0.120). Every consolidation account this run \"\n    \"pre-registered failed: A*_h, gateway retention, and the retained frontier (a volume-matched null, reversal under min-cp). It is \"\n    \"still a LEAD. Apart from P2 it was assembled after the unseal. Concept type and generic terms are untested. The all-papers ego \"\n    \"network is mechanically coupled to spread. I2 reaches 0.78, and LIFEENV is weak. So this iteration does not widen. It spends one \"\n    \"artifact on each thing that could still kill or bound the lead. Art 1 (the decisive one) does replication plus the confound \"\n    \"ladder on fresh concepts. Art 2 tests the mechanism within concepts, where concept type and footprint are absorbed by fixed \"\n    \"effects, and decomposes where new partners come from. Art 3 is the FIX: the failed Exp9 RQ2 artifact, re-run with its \"\n    \"pre-registration inverted to the openness account, plus case studies and the AI atlas the request asks for. Art 4 is the \"\n    \"reviewer's blocking record repair, plus a boundary/specification analysis of the lead on existing arrays. Art 5 is the \"\n    \"nearest-neighbour novelty check, because Callon's density-centrality diagram and patent 'generality' are obvious precursors that \"\n    \"have to be named. Everything is zero-credit. The OpenRouter plan is under $5 of the $20 phase pot. INFORMATIVE EITHER WAY: if \"\n    \"concept type absorbs OPEN, the portable RQ1 signal is type, with openness as its network marker. If HOME-ONLY fails while \"\n    \"ALL-PAPERS holds, the Exp8 signal is mechanical, and that is reported as a measurement warning for co-occurrence emergence \"\n    \"indicators. Iteration 5 can then write the paper, or run one targeted follow-up.\"\n)\n\nart1 = {\n    \"type\": \"experiment\",\n    \"objective\": (\n        \"DECISIVE REPLICATION + CONFOUND TEST of the openness claim (RQ1) on a fresh 2015-2016 onset cohort that no screen has \"\n        \"touched. Does HOME-ONLY OPEN keep a positive partial association with size-adjusted breadth (O2r_m50, O2r_resid at \"\n        \"t0+6..t0+8) through the full control ladder (B5 -> +CONTACT_REACH -> +CONCEPT TYPE -> +PRE-ONSET FOOTPRINT -> +label \"\n        \"coverage -> +home-group FE)? Does it hold within method concepts and within object concepts? Is RETENTION_RATIO_early \"\n        \"negative? Secondary: replicate the frozen Exp8 learned models and the n_authors_early leads.\"\n    ),\n    \"approach\": (\n        PATHS + SHARED +\n        \"STEP 0, PRE-REGISTRATION FIRST. Write prereg.md + frozen_spec.json holding the OPEN definition and signs, the ladder, the \"\n        \"groups, the success rules below and the fallback. Hash them. \"\n        \"STEP 1, COHORT FRAME, from EXP5 scan/agg_counts.parquet (years <= t0 only for selection). Candidates are legacy concepts \"\n        \"NOT in EXP5 frame_concepts.csv, with onset t0 in {2015, 2016} under the IDENTICAL EXP5 newborn rule and TAG grounding. The \"\n        \"newborn check may use counts through t0+2 <= 2018, exactly as frozen. Apply the EXP5 per-concept LLM precision gate with the \"\n        \"same prompt and model, reusing scan/llm_cache. Home and groups: CS+Eng, BGM+Med, PHYS, LIFEENV, SOC, MATHDEC (MATHDEC \"\n        \"reported only). DECLARED FALLBACK: if fewer than 800 concepts pass, add 2017 onsets with outcomes at t0+5..t0+7. \"\n        \"STEP 2, ONE ZERO-CREDIT SNAPSHOT PASS (adapt EXP8 passA.py; the matcher and grounding stay unchanged). For cohort concepts, \"\n        \"take every grounded work 2012-2024: work id, year, primary source id (-> venue field via source_field.parquet), topic ids, \"\n        \"author ids and referenced_works. Check that yearly counts <= 2022 reproduce agg_counts exactly (else stop and log). If time \"\n        \"allows, run a second pass (EXP8 passB.py) for O4 citations to early works; O4 is the first thing dropped. \"\n        \"STEP 3, FEATURES over t0..t0+2 only, for the cohort AND the EXP5 frame (EXP5 home-only builds come from \"\n        \"data/frame_matches_early + source_field, with no new pass). OPEN in all three builds, via Exp8 lib/ego.py on EXP3 backbone \"\n        \"slice2 (2010-14, pre-onset for the cohort, so leakage-free). Skip betweenness in the home-only and size-matched builds (it is \"\n        \"not in OPEN, and it cost 98% of ego time). Parallelise across 7 vCPUs. Also compute each OPEN component alone, \"\n        \"RETENTION_RATIO_early, CONTACT_REACH, B5, n_authors_early and every Exp8 indicator needed by the frozen models/*.joblib. \"\n        \"STEP 4, CONCEPT TYPE (LLM; cap $3). Label all EXP5 + cohort concepts (about 14.5k) with a cheap OpenRouter model. The input \"\n        \"is the concept label, its Wikidata description where the art_O7Dq4L02QnDN key has it, and 3 early titles. There are 4 \"\n        \"classes: method/technique/tool; object/material/organism/disease; property/measure/theory; topic/field. A separate flag marks \"\n        \"GENERIC pre-existing terms (e.g. 'Coefficient of variation'). BENCHMARK: 300 concepts stratified by group are double-labelled \"\n        \"by a second model, and 60 are hand-checked by the executor. Required: precision >= 0.85 on method-vs-object. If this fails, \"\n        \"revise the prompt once; if it fails again, restrict within-type tests to two-model-agreement concepts and log it. \"\n        \"STEP 5, PRE-ONSET FOOTPRINT from agg_counts (years < t0): log grounded papers t0-10..t0-1, number of fields pre-t0, a \"\n        \"re-emergence flag (any pre-t0 year >= 25% of the t0+2 count), and Wikipedia creation year < t0 from art_O7Dq4L02QnDN \"\n        \"(year_usable only) as a generic-term marker. \"\n        \"STEP 6, SELECTION ON EXP5 (all 12,499). Confirm the signs of OPEN (every build) and fit the ladder on O2r_m50 and O2r_resid. \"\n        \"Freeze the z constants, the O2r_resid a/b (Exp8 o2r_resid_fit.json), the type classifier outputs, the Holm family (OPEN_home, \"\n        \"OPEN_all, OPEN_sizematched, RETENTION_RATIO x 2 outcomes) and the rules. Write frozen_spec.json and hash it into \"\n        \"logs/seal.log. Record here, as selection-data results, the EXP5 ladder with concept type and footprint (the first test of \"\n        \"confound (ii) on the old data). \"\n        \"STEP 7, ONLY THEN compute cohort outcomes: O2r_m50 (exact hypergeometric), O2r_resid, O1c, O1b, O3 and O4 at t0+6..t0+8. \"\n        \"For 2015 onsets only, also a <= 2022 sensitivity at t0+5..t0+7. Hash the outcome file and score ONCE. REPORT the partial \"\n        \"Spearman of each OPEN build at every ladder rung (concept bootstrap 2,000), per group with DL pooling and I2, within method \"\n        \"and within object concepts, and for each OPEN component alone. Also RETENTION_RATIO_early given B5, and the ALL-vs-HOME-ONLY \"\n        \"difference with a paired bootstrap. SECONDARY (frozen, no refit): Exp8 O3 L1-logit dAUC over B5, n_authors_early for \"\n        \"O3/O1b/O1c, O4 EBM Spearman, O2r ElasticNet gain over B5, and CONTACT_REACH (with and without intersection-born concepts). \"\n        \"Missing model inputs are imputed at the frozen DEV median. A replication is dropped if more than 20% of its model weight is \"\n        \"imputed. VERDICT RULES (frozen). CONFIRMED if HOME-ONLY OPEN has psp > 0 with CI > 0 at the type and footprint rungs, a \"\n        \"positive sign in >= 4 of 5 groups, psp > 0 within both method and object concepts, and RETENTION_RATIO_early < 0 given B5. \"\n        \"DISCONFIRMED if the CI at the type rung includes 0. Outcomes (a) 'type absorbs OPEN' and (b) 'home-only fails, all-papers \"\n        \"holds = mechanical' are reported as stated. No subgroup hunting after the unseal. DROP ORDER if time is short: O4/Pass B, \"\n        \"then the learned-model replications, then the 2017 fallback extension. Never drop the home-only build, the type rung, or the \"\n        \"single unseal. OUTPUTS: cohort_frame.csv, concept_types.csv (both frames; reusable), type_benchmark.json, footprint.csv, \"\n        \"features_cohort.parquet, features_exp5_homeonly.parquet, frozen_spec.json + logs/seal.log, outcomes_cohort.parquet (hashed), \"\n        \"cohort_result.json (every rung, group, type and CI), ladder and forest figures, and method_out.json with per-concept \"\n        \"predictions.\"\n    ),\n    \"what_it_would_show\": (\n        \"On about 1,500-2,500 never-screened 2015-16 concepts, an openness index built only from HOME-field papers in the first three \"\n        \"years predicts size-adjusted breadth six to eight years later: partial rho about +0.10 to +0.15 given B5, CI > 0 after \"\n        \"controlling for concept type and pre-onset footprint, positive in >= 4 of 5 field groups and within both method and object \"\n        \"concepts, while the share of contacted fields that keep the concept is negatively related (about -0.1). This is RQ1's portable, \"\n        \"non-mechanical early network signal, confirmed out of sample.\"\n    ),\n    \"depends_on\": [\n        {\"id\": \"art_O7Dq4L02QnDN\", \"label\": \"concept key\"},\n    ],\n}\n\nart2 = {\n    \"type\": \"experiment\",\n    \"objective\": (\n        \"MECHANISM of the openness effect (RQ2 timing and 'why it works'), within concepts on the EXP5 frame. (a) Does a concept's \"\n        \"home-only neighbourhood CLOSING in year t lower its off-home field-entry hazard in t+1, with concept and year FE, when the \"\n        \"reverse path (entry -> later closure) is weaker and pre-trends are flat? (b) Where do the new partners that carry the \"\n        \"new_edge_rate / n_comm_W3 signal come from: method-topic vs domain-topic communities, home vs off-home fields, and which \"\n        \"bridging papers bring them? (c) The request's sequence question: does home-community prominence peak BEFORE off-home entry \"\n        \"take-off, or do intersection-born concepts (>= 2 homes) diffuse without it?\"\n    ),\n    \"approach\": (\n        PATHS + SHARED +\n        \"STEP 1, ONE ZERO-CREDIT SNAPSHOT PASS (EXP8 passA.py with the window extended; matcher and grounding unchanged). For the 12,499 \"\n        \"EXP5 concepts, collect grounded works t0..min(t0+10, 2022): work id, year, source -> venue field, topic ids, author ids and \"\n        \"document type. Check that counts reproduce agg_counts exactly. Also build the D3 yearly states from EXP7 \"\n        \"state_panel_{dev,heldout}.parquet (authoritative). \"\n        \"STEP 2, YEARLY PANEL (concept x year, t0..t0+10). Home-only openness(t) uses 1-year windows via Exp8 lib/ego.py on the \"\n        \"time-appropriate EXP3 backbone slice (the slice before or containing t; no betweenness): new-partner rate, n_comm, \"\n        \"participation, ego density, edge persistence, plus the OPEN_home composite with frozen EXP5 z constants. Controls: log \"\n        \"home-paper volume(t), log total volume(t), concept age, and entries already made. Outcome: number of NEW off-home fields \"\n        \"ENTERED in t+1 (D3), plus the binary any-entry hazard. Parallelise across 7 vCPUs. \"\n        \"STEP 3, PRE-REGISTER BEFORE ESTIMATION (frozen_spec.json hashed). Primary: Poisson (or LPM) with concept FE and year FE, \"\n        \"entries(t+1) on home-only ego density(t), and separately on OPEN_home(t). Prediction: density beta < 0 and OPEN beta > 0, \"\n        \"concept-clustered CIs excluding 0. Reverse path: home-only density(t+1) on entries(t), same FE. Prediction: weaker in \"\n        \"standardised terms (paired bootstrap of |beta| difference). Event study: the event is the first home-only CLOSURE JUMP (a \"\n        \"within-concept rise in ego density >= 1 within-concept SD, first occurrence at age >= 2). Leads -3..-1 and lags 0..+4, \"\n        \"estimated with the Sun & Abraham (2021) interaction-weighted estimator, with never-treated and not-yet-treated controls. \"\n        \"Pre-trend joint test. Placebo: event year permuted within concept (1,000 draws), plus a within-concept-year permutation of \"\n        \"the field labels of entries. Report DEV and old held-out separately (labelled mechanism evidence, not confirmation), and \"\n        \"report excluding Medicine homes and excluding intersection-born concepts. \"\n        \"STEP 4, WHY IT WORKS (partner-source decomposition, early window t0..t0+2). Label the OpenAlex topics that appear as \"\n        \"partners as METHOD/TECHNIQUE vs DOMAIN/PHENOMENON with a cheap LLM (about 4.5k topics; 100 double-labelled; 40 hand-checked; \"\n        \"cap $1). For every new partner, record: method vs domain; partner topic's field = home or off-home; Leiden community \"\n        \"(EXP3) = the concept's first-year modal community or a new one; carrying paper's venue field home or off-home. Recompute \"\n        \"new_edge_rate and n_comm_W3 restricted to each partner class, and report each class's partial Spearman with O2r_m50 given \"\n        \"B5 (old held-out, from Exp8 outcomes; exploratory). This shows which partner class carries the signal and whether it survives \"\n        \"when only HOME-venue papers deliver the new partners. BRIDGING PAPERS: papers that introduce >= 1 partner from a new \"\n        \"community. Report their share, team size, share of authors new to the concept, document type (review vs article), and \"\n        \"whether early bridging-paper share predicts O2r given B5. \"\n        \"STEP 5, SEQUENCE TEST (RQ2). Home prominence(t) = within-home percentile rank of the concept's home-only degree and k-core \"\n        \"among all frame concepts sharing that home in year t. Off-home take-off = the first year with >= 2 new off-home entries. \"\n        \"Event-study both orders (prominence peak -> take-off; take-off -> prominence), with pre-trends. Compare single-home with \"\n        \"intersection-born concepts on time to take-off, and on whether a prominence peak precedes take-off (share, concept \"\n        \"bootstrap). Frozen prediction: intersection-born concepts take off without a prior home-prominence peak more often than \"\n        \"single-home concepts. OUTPUTS: yearly_panel.parquet (reusable in iteration 5), fe_results.json, event_study.json with \"\n        \"figures, partner_decomposition.json, topic_types.csv, bridging_papers.parquet, sequence_tests.json, frozen_spec.json + seal \"\n        \"log, and method_out.json.\"\n    ),\n    \"what_it_would_show\": (\n        \"Within the same concept, a year in which its home neighbourhood closes is followed by fewer new-field entries (FE beta < 0, \"\n        \"CI excludes 0, flat pre-trends, placebo null), while entries do not predict later closure as strongly. The breadth signal of \"\n        \"new_edge_rate and n_comm_W3 is carried mainly by new partners from METHOD communities and from previously unlinked communities, \"\n        \"even when they arrive through home-field papers. So openness is a leading cause-like marker, not a by-product of spread. \"\n        \"Separately, intersection-born concepts take off without a prior home-prominence peak. This answers the request's \"\n        \"'central-first vs intersection' question.\"\n    ),\n    \"depends_on\": [\n        {\"id\": \"art_O7Dq4L02QnDN\", \"label\": \"concept key\"},\n    ],\n}\n\nart3 = {\n    \"type\": \"experiment\",\n    \"objective\": (\n        \"FIX: re-run the failed iteration-3 RQ2 artifact (gen_art_experiment_9, plan 3_invention_loop/iter_3/gen_plan/\"\n        \"gen_plan_experiment_3; never executed, its output-format loop failed). It runs on the existing EXP5/EXP7/EXP8 arrays with the \"\n        \"pre-registration updated to the openness account. (a) A log-additive breadth decomposition: contact rate x retention \"\n        \"probability x frontier advance, with Shapley shares. (b) An empirical trajectory typology, named only if two methods agree. \"\n        \"(c) Matched-pair case studies from the quantitative extremes. (d) The request's stage-1 AI/CS atlas (about 40 concepts; \"\n        \"retrospective, descriptive).\"\n    ),\n    \"approach\": (\n        PATHS + SHARED +\n        \"Cache only: NO snapshot pass, $0 LLM. FIRST write a valid method_out.json skeleton, and validate it with aii-json against \"\n        \"exp_gen_sol_out at the MINI stage, before any long computation. Exp9 died on output-format validation, so the format is \"\n        \"checked first and after every stage. \"\n        \"(1) STATE SEQUENCES, t0..t0+10, from EXP7 state_panel_*.parquet and EXP5 agg_counts (D3 states: untouched / entered / \"\n        \"retained / lost per field). Yearly summaries: contact rate (new off-home fields entered), retention probability (share of \"\n        \"entered off-home fields that become retained), frontier advance (entries per retained field), rarefied entropy, within-home \"\n        \"share, field-level community span on the EXP6 backbone, and the Exp8 early OPEN components (t0..t0+2) as static covariates. \"\n        \"(2) DECOMPOSITION. log(breadth at t0+8) = log contact + log retention + log frontier (+ residual). Shapley decomposition of \"\n        \"the top-vs-bottom O2r_resid tercile gap; adjust for Medicine homes and also exclude them. PRE-REGISTERED (frozen_spec.json, \"\n        \"hashed, before computing): localised and integrating concepts differ MORE in contact/exploration than in retention, and \"\n        \"localised concepts have HIGHER early retention ratios. Report the concept-bootstrap CI of the contact share minus the \"\n        \"retention share. \"\n        \"(3) TYPOLOGY. DTW k-medoids (k = 2..8, silhouette + gap + bootstrap stability) and a Gaussian HMM (3-5 states, BIC) on the \"\n        \"standardised yearly vectors. A class is NAMED only if DTW-HMM ARI >= 0.5, it replicates when held-out is re-clustered, and it \"\n        \"survives excluding Medicine homes. Otherwise report a continuum: project the trajectories on the first 2-3 principal axes and \"\n        \"show where early OPEN sits on them (Spearman of OPEN with axis 1). Record the old typology (Exp6: 2 classes, HMM ARI 0.094) \"\n        \"as not established. \"\n        \"(4) CASE STUDIES. Six to eight MATCHED PAIRS seeded from Exp8 results/case_exemplars.json: same home group, early volume \"\n        \"and growth within 0.25 SD (B5-matched), opposite OPEN (top vs bottom quintile), mixed domains and not only AI, excluding \"\n        \"GENERIC terms by a label rule logged in deviations. For each pair: an alluvial field-flow figure of D3 states over time; \"\n        \"early ego-network snapshots W1..W3 from data/frame_matches_early (topics coloured by EXP3 community); the O2r outcome; and \"\n        \"external recognition dates from art_O7Dq4L02QnDN (descriptive only). \"\n        \"(5) AI/CS ATLAS (the request's stage 1, labelled RETROSPECTIVE and DESCRIPTIVE). About 40 CS-home frame concepts with AI/ML \"\n        \"labels, chosen to span rapid emergence, gradual growth, local specialisation, cross-disciplinary diffusion and transient \"\n        \"expansion (O3 = 1). Yearly panels of connectivity, new neighbours, community membership, field distribution and D3 states. \"\n        \"Include a small-multiples figure and a table stating which structural changes looked meaningful. \"\n        \"(6) pipeline_counts.json for the methodology figure: works, concepts, episodes, risk-set rows and split sizes at every stage, \"\n        \"read from the actual artifacts. OUTPUTS: state_sequences.parquet, decomposition.json, trajectories.json (assignments, ARI, \"\n        \"stability, medoids, or continuum axes), case_studies/ (figures + per-pair JSON), ai_atlas/ (figures + table), \"\n        \"pipeline_counts.json, frozen_spec.json + seal log, and a schema-valid method_out.json.\"\n    ),\n    \"what_it_would_show\": (\n        \"On about 12k concepts, what separates concepts that end broadly integrated from those that stay local is how many new fields \"\n        \"they keep CONTACTING (Shapley share of contact > retention, CI excludes 0), not how well each field keeps them. Localised \"\n        \"concepts in fact retain a larger share of the fields they touch. Trajectories form a continuum along the openness axis rather \"\n        \"than robust discrete classes, unless the DTW-HMM agreement rule passes. Matched pairs with equal early growth but opposite \"\n        \"openness show the mechanism visually. This completes RQ2 and the request's exploratory AI stage.\"\n    ),\n    \"depends_on\": [\n        {\"id\": \"art_O7Dq4L02QnDN\", \"label\": \"recognition dates\"},\n    ],\n}\n\nart4 = {\n    \"type\": \"evaluation\",\n    \"objective\": (\n        \"(A) Clear every BLOCKING reviewer MUST-FIX with file-traceable tables and ready-to-insert corrected text. (B) BOUNDARY of the \"\n        \"openness lead on the existing Exp8 arrays: per-group behaviour, construction and specification robustness, and heterogeneity \"\n        \"(why I2 is 0.75-0.78, why LIFEENV is weak). Also re-score the footprint-contaminated indicators post-onset only. The whole \"\n        \"analysis is frozen BEFORE the Art 1 cohort unseal, so it cannot steer confirmation.\"\n    ),\n    \"approach\": (\n        \"No new data or methods; $0-0.5 LLM. Read by path: Exp8 (art_dFQ6jbgNsR6Q) results/*: heldout_unit_results.csv, \"\n        \"portability_table.csv, prereg_verdicts.json, frozen_spec.json, learned_vs_single_heldout.json, sensitivities_pooled.json, \"\n        \"indicator_dictionary.csv, deviations.json, README tables, data/analysis_table.parquet, indicator_matrix.parquet. Exp7 \"\n        \"(art_22ppE1snfHKj) step2_dev.json and step2_heldout.json, deviations.json and frontier_result.json. Eval2 \"\n        \"3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/ (art_7W9xiIO3FVBs): text_corrections.md (14 blocks), record_tables/*.csv, \"\n        \"claims_ledger.csv, o5_validation.json and frame_agreement.json. Also 3_invention_loop/iter_3/gen_art/gen_art_experiment_9/ (and \"\n        \".aii_worker_result.json if present), the plan 3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3/, and the report \"\n        \"3_invention_loop/iter_4/gen_strat/current_report.md. \"\n        \"PART A, CORRECTIONS PACK (corrections/ with one markdown file per report section, each table followed by a 'Source: file -> \"\n        \"key path' line). (1) Exp8 outcome relabelling: REL_home and author_growth are O4. The O3 top-10 table comes from the README. \"\n        \"Include all 8 learned-model rows (O1c, O2r_m50, O2r_resid, O4, O1b, O3, O5, O5_WW, with n and paired CIs). Dead end 22.6 is \"\n        \"rewritten. (2) A P1-P5 table with the EXACT frozen prediction text, the verdict and the deciding quantity. [Correction] \"\n        \"sentences for dead end 7.4 (new_edge_rate transfers) and 4.3. A held-out table of the iteration-1 candidates (D_ratio, \"\n        \"D_rare, participation, NOV_res, entropy, edge_persistence), with pooled psp, CI and per-group raw rho. (3) Exp7 tables from \"\n        \"step2 JSONs: volume-matched d_R_m / d_N_m / contrast (coarse and fine; DEV and held-out; match rates and balance); dose \"\n        \"betas with the monotone flag; d_lost A1 vs R4; d0 concept / two-way / crossed CIs; held-out sensitivities; a \"\n        \"'Proximity dependence' subsection (min-cp d0 -0.021, p 0.012; RCA LR 246). A definitional comparison of D_rca_pers (Exp7 \"\n        \"S_strict) with Research 2's D_rca_persist_k (equivalent or not, and why). A nearest-neighbour paragraph draft. (4) Eval2's 14 \"\n        \"text_corrections blocks, rendered as insert-ready text marked '[Correction, iteration 3, from art_7W9xiIO3FVBs]', plus every \"\n        \"record_tables CSV mapped to its target section. The 6 MISMATCH and 15 MISLABELLED ledger rows are listed individually. (5) \"\n        \"A failed-artifact record for gen_art_experiment_9 (plan, failure mode, what was lost; 'not run, not refuted'). Correct \"\n        \"iteration counts: iteration 1 completed 3 of 5, iteration 2 completed 5, iteration 3 completed 4 of 5. (6) Candidate S rows \"\n        \"(S_comp, S_comp_n, S_isolated_share for every outcome). The six indicator families with counts from indicator_dictionary.csv \"\n        \"and the D-family > 30%-missing exclusion rule. (7) O5 per-source leakage and lags, and the O5-O3 association per group (pooled \"\n        \"-0.049, p 0.004, I2 0.55). (8) Minor slips (19.6 -> 20.2 cross-reference; the 18.11 count sentence). (9) claims_ledger_v3.csv: \"\n        \"every number in the corrections pack re-read from its file, with MATCH status. \"\n        \"PART B, BOUNDARY OF THE LEAD (exploratory, old held-out already unsealed; write boundary_spec.json and hash it first). (1) \"\n        \"POST-ONSET RE-SCORE: M0_density_end and D_vol_end recomputed from EXP5 agg_counts using t0..t0+2 papers only, then scored \"\n        \"held-out exactly as Exp8 scored them (psp given B5, pooled + per group). Report how much of the +0.377 / +0.307 was pre-onset \"\n        \"footprint. (2) PER-GROUP TABLE for every confirmed O2r indicator plus the OPEN composite (all-papers, frozen EXP5-DEV z): \"\n        \"PHYS, LIFEENV, SOC, MATHDEC, COH_DEVHOME and COH_OTHER, as rho [CI] and n, with a mark on each cell whose CI includes 0. Add \"\n        \"the sensitivities_pooled robustness rows, including the halving of CONTACT_REACH without intersection-born concepts. (3) \"\n        \"SPECIFICATION CURVE for OPEN: component subsets (all 63 non-empty subsets of the 6), equal vs first-PC weights, outcomes \"\n        \"O2r_m30 / O2r_m50 / O2r_resid / O2r_resid_N, controls B5 vs B5 + coverage vs B5 + onset-year. Report the share of \"\n        \"specifications with CI > 0 and the median psp, against a within-group outcome-permutation null (200 draws). (4) \"\n        \"HETEROGENEITY: meta-regress the per-unit psp on unit traits (label coverage, median early volume, share multi-home, share \"\n        \"GENERIC-looking labels by a frozen lexical rule, median O2r). Leave one group out. Test whether the weak LIFEENV cells are \"\n        \"explained by low label coverage or by low OPEN variance (variance ratio test). OUTPUTS: eval_out.json (schema-valid), \"\n        \"corrections/ , claims_ledger_v3.csv, post_onset_rescore.json, per_group_table.csv, spec_curve.json + figure, \"\n        \"heterogeneity.json, boundary_spec.json + hash.\"\n    ),\n    \"what_it_would_show\": (\n        \"Every blocking review item is closed with insert-ready text and a source key. The openness lead is not a construction artifact: \"\n        \"most of the 63-plus specifications keep CI > 0 against a permutation null. Its heterogeneity is bounded and explained, e.g. \"\n        \"LIFEENV weakness tracks label coverage or restricted OPEN variance, not a domain reversal. M0_density_end's headline value is \"\n        \"shown to be largely pre-onset footprint, so the paper's RQ1 headline moves to the purely post-onset openness indicators.\"\n    ),\n    \"depends_on\": [\n        {\"id\": \"art_dFQ6jbgNsR6Q\", \"label\": \"lead to bound\"},\n        {\"id\": \"art_22ppE1snfHKj\", \"label\": \"record tables\"},\n        {\"id\": \"art_wxWssKSUR45f\", \"label\": \"footprint counts\"},\n        {\"id\": \"art_O7Dq4L02QnDN\", \"label\": \"O5 per source\"},\n    ],\n}\n\nart5 = {\n    \"type\": \"research\",\n    \"objective\": (\n        \"Nearest-neighbour NOVELTY CHECK for the openness-vs-consolidation claim, and paper positioning for Applied Network Science. \"\n        \"Is 'early open, churning, multi-community co-occurrence neighbourhoods predict size-adjusted cross-field integration; early \"\n        \"consolidation predicts staying local, at equal growth' new, partially anticipated or anticipated? What comparison numbers \"\n        \"exist for RQ1 and RQ2 under this framing, and which works must the paper cite and distinguish?\"\n    ),\n    \"approach\": (\n        \"Build on art_EesdB8cuSfcU and art_dxvRpQufMR0e (3_invention_loop/iter_3/gen_art/gen_art_research_2/research_report.md and \"\n        \"iter_2/gen_art/gen_art_research_1/research_report.md). Do not repeat their relatedness, exit or venue work. For each work, \"\n        \"record: unit, network, early-window measure, outcome, whether it is size-adjusted, whether it is held-out, and the effect \"\n        \"size. Give a quote and a verdict (NEW / PARTIALLY ANTICIPATED / ANTICIPATED) for each of four sub-claims: C1 early \"\n        \"new-partner rate and multi-community contact predict breadth beyond growth; C2 early ego DENSITY and edge PERSISTENCE predict \"\n        \"LESS breadth; C3 the retention ratio of contacted fields is NEGATIVE; C4 within-concept closure precedes an entry slowdown. \"\n        \"STRANDS. (1) Co-word strategic diagrams: density vs centrality of themes (Callon, Courtial & Laville 1991; Cobo et al. 2011 \"\n        \"SciMAT; Coulter et al.). Do low-density themes become transversal? This is the most direct precursor. (2) Topic birth and \"\n        \"emergence: Salatino et al. 2017/2018 (pre-emergence density, the opposite direction?), Small, Boyack & Klavans 2014, Rotolo \"\n        \"2015, Chen 2009/2012 structural variation, Xu et al. 2021 and Liang et al. (3) Diffusion of ideas and concepts: Cheng et al. \"\n        \"2023 ASR. Extract EXACTLY how 'consistent usage' and 'fit' are operationalised: does consistent usage mean a STABLE semantic \"\n        \"context, and does our result contradict it for breadth? Also Kuhn, Perc & Helbing 2014 (memes), Sun et al. 2013 (social \"\n        \"dynamics of science), Mao et al. 2020 and Maillart et al. 2026. (4) Recombination and novelty: Uzzi et al. 2013 atypical \"\n        \"combinations; Foster, Rzhetsky & Evans 2015; Wang, Veugelers & Stephan 2017; Shi & Evans 2023; Tria et al. 2014 and \"\n        \"Iacopini et al. 2018 (adjacent possible, network of novelties); Hofstra et al. 2020. (5) Structural diversity and virality: \"\n        \"Ugander et al. 2012; Weng, Menczer & Ahn 2013; Centola 2010/2018; Burt constraint and closure vs brokerage. (6) General \"\n        \"purpose technologies: the patent GENERALITY index (Trajtenberg, Henderson & Jaffe 1997; Hall & Trajtenberg 2004; Bresnahan & \"\n        \"Trajtenberg 1995). Is early generality known to predict later diffusion? (7) Methods vs objects: Leydesdorff & Rafols 2011 \"\n        \"research technologies; studies of method diffusion across fields (e.g. methods papers and their cross-field citation; \"\n        \"entity/method extraction diffusion studies). This supports or undermines the concept-TYPE confound. (8) \"\n        \"Exploration-exploitation and boundary objects applied to science: March 1991; Star & Griesemer 1989; Foster 2015; Fujimura. \"\n        \"(9) Within-unit timing: any panel or event-study evidence that neighbourhood closure precedes diffusion slowdown (topic \"\n        \"lifecycle, 'Social dynamics of science' splits and merges). ALSO: (a) an RQ1 comparison table with numbers (metric, horizon, \"\n        \"held-out design, size-adjusted?, value; mark level AUCs as not comparable), and an RQ2 comparison table (trajectory classes, \"\n        \"decompositions, sequence findings); (b) up to 8 ANS papers (2016-2026) on co-occurrence / knowledge-network evolution to cite \"\n        \"in Related Work, each with a one-line relation; (c) an updated Fig. 1 methodology spec for the openness framing (lanes: \"\n        \"grounding -> frames/cohorts -> three ego builds -> indicator families -> selection/seal -> fresh cohort -> within-concept \"\n        \"mechanism -> trajectories), with the counts to be filled from pipeline_counts.json; (d) a 'threats a reviewer will raise' list \"\n        \"with the literature answer to each; (e) a verified reference list with a DOI or arXiv ID for every entry (Semantic Scholar \"\n        \"fetchable) and UNVERIFIED flags.\"\n    ),\n    \"what_it_would_show\": (\n        \"The paper can state precisely that open, multi-community early co-occurrence neighbourhoods predicting size-adjusted \"\n        \"cross-field integration, and early consolidation predicting localisation, is NEW or only PARTIALLY ANTICIPATED (by Callon's \"\n        \"density-centrality diagram, patent generality and Weng/Ugander structural diversity). It will cite quotes, and it will show \"\n        \"how the result refines Cheng et al. 2023's 'consistent usage' and Salatino's pre-emergence density rather than duplicating \"\n        \"them. It will also have per-RQ comparison numbers and a finished methodology-figure spec.\"\n    ),\n    \"depends_on\": [],\n}\n\nstrategy = {\n    \"domain_reasoning\": domain_reasoning,\n    \"principle_alignment\": principle_alignment,\n    \"title\": \"Do open early neighbourhoods really predict spread?\",\n    \"objective\": objective,\n    \"rationale\": rationale,\n    \"artifact_directions\": [art1, art2, art3, art4, art5],\n    \"expected_outcome\": (\n        \"(1) A single, sealed, out-of-sample verdict on the openness claim from a never-screened 2015-16 cohort. It will include \"\n        \"home-only vs all-papers vs size-matched builds, the full confound ladder with LLM concept type (benchmarked) and pre-onset \"\n        \"footprint, within-type estimates, per-group DL pooling with I2, and replications of the Exp8 learned models and \"\n        \"n_authors_early. Reusable concept_types.csv for both frames. (2) Within-concept mechanism evidence: FE closure -> entry \"\n        \"hazard with the reverse path, a Sun-Abraham event study with pre-trends and placebos, a decomposition of where new partners \"\n        \"come from (method vs domain, home vs off-home, bridging papers), and a test of the request's 'central-first vs intersection' \"\n        \"sequence question, all on a reusable yearly panel. (3) RQ2 finally on about 12k concepts: the contact x retention x frontier \"\n        \"Shapley decomposition, a typology named only under DTW-HMM agreement or else a continuum along the openness axis, matched-pair \"\n        \"case studies, the AI/CS stage-1 atlas and pipeline counts for Fig. 1. (4) A corrections pack that closes every blocking \"\n        \"review item with source keys, a post-onset re-score of the footprint indicators, a per-group table and specification curve \"\n        \"for the lead, and a heterogeneity diagnosis. (5) A novelty verdict per sub-claim with quotes, comparison tables and a \"\n        \"methodology-figure spec. With these, iteration 5 writes the ANS paper, with openness either CONFIRMED, or re-scoped to \"\n        \"'concept type with openness as its marker', or reported as a mechanical measurement warning.\"\n    ),\n    \"summary\": (\n        \"Iteration 4 latches onto the one lead that survived held-out testing: new concepts whose early co-occurrence neighbourhood \"\n        \"stays open spread widest. Five bets attack it from every side. (1) A decisive confirmation on a fresh, never-screened \"\n        \"2015-16 cohort, with a home-only build against mechanical coupling and LLM concept type and footprint controls. (2) \"\n        \"Within-concept mechanism and partner-source decomposition. (3) A re-run of the failed RQ2 trajectory artifact, with case \"\n        \"studies and the AI atlas. (4) A boundary analysis plus the reviewer's blocking record repair. (5) A nearest-neighbour novelty \"\n        \"check. All use zero API credits and under $5 of LLM.\"\n    ),\n}\n\nout = {\"strategies\": [strategy]}\n(HERE / \".terminal_claude_agent_struct_out.json\").write_text(json.dumps(out, indent=2, ensure_ascii=False))\nprint(\"directions:\", len(strategy[\"artifact_directions\"]))\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [22] TOOL CALL — Bash · 2026-09-29 02:06:22 UTC

```
Build and validate strategy JSON:
sed -i '/^RUN = /d' build_strategy.py && python3 build_strategy.py && python3 -c "
import json;d=json.load(open('.terminal_claude_agent_struct_out.json'))
s=d['strategies'][0]
for k in ['title','objective','rationale','artifact_directions','expected_outcome']: assert k in s
for a in s['artifact_directions']:
  assert a['type'] in ['experiment','research','proof','evaluation','dataset']
  for dep in a['depends_on']: assert set(dep)=={'id','label'}
  print(a['type'], len(a['approach']), [x['id'] for x in a['depends_on']])
"
```

### [23] TOOL RESULT — Bash · 2026-09-29 02:06:22 UTC

```
{"stdout": "directions: 5\nexperiment 9077 ['art_O7Dq4L02QnDN']\nexperiment 7754 ['art_O7Dq4L02QnDN']\nexperiment 7114 ['art_O7Dq4L02QnDN']\nevaluation 4649 ['art_dFQ6jbgNsR6Q', 'art_22ppE1snfHKj', 'art_wxWssKSUR45f', 'art_O7Dq4L02QnDN']\nresearch 3567 []", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] ASSISTANT · 2026-09-29 02:06:32 UTC

```
Now the README and the manifest. Nothing in this workspace is heavy.
```

### [25] TOOL CALL — Bash · 2026-09-29 02:06:32 UTC

````
Write manifest and README:
cat > .aii/manifest.yaml <<'EOF'
# No heavy binaries or caches in this workspace: only a small Python builder, the strategy JSON and this README.
entries: []
EOF
cat > README.md <<'EOF'
# Iteration 4 strategy (GEN_STRAT, gen_strat_1)

This is the strategy for iteration 4 of the AI Inventor run on emerging scientific concepts. It latches onto the
Exp8 lead: new concepts whose early co-occurrence neighbourhood stays OPEN spread widest. There are five artifact
directions, and each one attacks that lead from a different side:

1. **Experiment: fresh-cohort confirmation.** It uses a never-screened 2015-16 onset cohort. It adds a HOME-ONLY
   ego-network build (against mechanical coupling), a size-matched build, LLM concept type (benchmarked), pre-onset
   footprint, the control ladder and within-type tests. The specification is frozen on the EXP5 frame and the cohort
   is scored once.
2. **Experiment: within-concept mechanism.** Home-only closure in year t is set against off-home entry in year t+1,
   with concept and year FE, the reverse path, a Sun-Abraham event study and placebos. It also decomposes where new
   partners come from and tests whether concepts are central at home first or born at intersections.
3. **Experiment: RQ2 re-run of the failed Exp9.** It covers the contact x retention x frontier Shapley
   decomposition, the DTW/HMM typology with its naming rule, matched-pair case studies, the AI/CS stage-1 atlas and
   the pipeline counts.
4. **Evaluation: record repair plus boundary analysis.** It produces the corrections pack for every blocking review
   item, a post-onset re-score of the footprint indicators, per-group tables, a specification curve and a
   heterogeneity analysis.
5. **Research: nearest-neighbour novelty check.** Sources include Callon's strategic diagram, patent generality,
   Cheng 2023, the novelty/recombination literature and structural diversity. It also gathers comparison numbers
   and the Fig. 1 spec.

## Layout
- `build_strategy.py`: the single source of the strategy text; it writes the JSON below.
- `.terminal_claude_agent_struct_out.json`: the strategy output (schema: `Strategies`).
- `.aii/manifest.yaml`: the disposal manifest (empty; nothing heavy here).

## How to run
```bash
python3 build_strategy.py   # regenerates .terminal_claude_agent_struct_out.json
```
It needs only the Python standard library.

## Restoring removed files
Nothing is marked `delete`, so there is nothing to restore.
EOF
ls -la
````

### [26] TOOL RESULT — Bash · 2026-09-29 02:06:32 UTC

```
{"stdout": "total 2442\ndrwxr-xr-x  3 root root 1038734 Sep 29 02:06 .\ndrwxr-xr-x  3 root root 1049724 Sep 29 02:00 ..\ndrwxr-xr-x  2 root root   12500 Sep 29 02:06 .aii\n-rw-------  1 root root      54 Sep 29 02:00 .aii_claude_session.json\n-rw-r--r--  1 root root  299678 Sep 29 02:06 .repl_agent.ptylog\n-rw-r--r--  1 root root   50767 Sep 29 02:06 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 root root    2285 Sep 29 02:06 README.md\n-rw-r--r--+ 1 root root   46688 Sep 29 02:06 build_strategy.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] ASSISTANT · 2026-09-29 02:06:45 UTC

```
I've written the iteration-4 strategy to `./.terminal_claude_agent_struct_out.json`. It has exactly 5 artifact directions and matches the schema. Every direction attacks the Exp8 lead: new concepts whose early neighbourhood stays open, with new partners from many communities and a loose network, spread widest.

1. **Experiment: confirm the lead on concepts no screen has touched.** This is the decisive test. It uses the 2015-16 onset cohort, found with the same grounding and newborn rules. The whole EXP5 frame becomes selection data, and the specification is hash-sealed before any cohort outcome is computed. The openness index is built three ways:
   - from all papers, as in Exp8;
   - from home-field papers only, so spread into other fields can't inflate it mechanically;
   - from all papers subsampled to the home-only count, to separate "fewer papers" from "home restriction".
   
   Controls are added step by step: concept type (LLM-labelled, with a 300-concept benchmark and 60 hand checks), pre-onset footprint and generic-term flags, label coverage and home-group effects. The effect must also hold within method concepts and within object concepts. The fallback to 2017 onsets is declared in advance, and so is an order for dropping steps if time runs short.
2. **Experiment: the mechanism within each concept.** It asks whether a year in which a concept's home neighbourhood closes is followed by fewer new-field entries the next year. The model uses concept and year fixed effects, and the reverse direction is estimated too. An event study (Sun & Abraham estimator) checks pre-trends, alongside placebos. It also measures where new partners come from: method or domain topics, home or other fields, and which bridging papers bring them. Finally it tests whether concepts become prominent at home before spreading, or are born at an intersection of fields.
3. **Experiment: re-run the failed RQ2 artifact (Exp9).** It uses cached data only, and the output format is validated first, since that is what failed last time. It covers:
   - the contact × retention × frontier breakdown of breadth;
   - the trajectory typology, where a class is named only if the two clustering methods agree (ARI ≥ 0.5);
   - case studies of matched pairs with equal early growth but opposite openness;
   - the atlas of about 40 AI/CS concepts, the exploratory first stage the original request asks for.
4. **Evaluation: clear the blocking review items and test how robust the lead is.** It produces ready-to-insert corrected text with a source file and key for every blocking item. It re-scores `M0_density_end` and `D_vol_end` using post-onset papers only. It adds a per-group table and a specification curve over 63 subsets of the openness components. It also looks into why heterogeneity is high (I2 up to 0.78) and why LIFEENV is weak. All of this is frozen before the cohort is scored, so it cannot steer the confirmation.
5. **Research: check what is actually new.** It sets the claim against its nearest neighbours: Callon's density-versus-centrality diagram, the patent generality index, Cheng et al. 2023's "consistent usage", the novelty and recombination literature, and structural-diversity work. It gives a verdict per sub-claim and gathers comparison numbers and a spec for the methodology figure.

The plan uses no OpenAlex credits and stays under about $5 of LLM spend.

One thing the downstream steps should know: the cohort's outcome years (2021-2024) straddle the switch from MAG to OpenAlex's own data, and 2024 is still filling in. The strategy handles this with rarefied or year-normalised outcomes, label coverage as a control, and a sensitivity check for 2015 onsets using outcomes that end by 2022.

I also wrote `build_strategy.py` (it regenerates the JSON), a `README.md` and an empty `.aii/manifest.yaml`, because nothing in the workspace is large.
```
