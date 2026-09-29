# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 4 · `gen_plan`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_experiment_1` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 02:06:49 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 02:06:55 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A plan generator (Step 3.2: GEN_PLAN in the invention loop)

You received the hypothesis, an artifact direction to elaborate, and dependency artifacts relevant to the plan.
Your job: elaborate this direction into a detailed, actionable plan for the executor agent.

Specific, actionable plan → valuable artifact. Vague plan → wasted execution.
</your_role>
</ai_inventor_context>

<artifact_type_info>
You are expanding an artifact direction of type: EXPERIMENT

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance
</artifact_type_info>

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

<time_budget>

The experiment executor has 6h total (including writing code, debugging, testing, and fixing errors).

</time_budget>

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

<plan_guidelines>
You are expanding an artifact direction from the strategy into a detailed plan.
The artifact direction specifies what to do at a high level (type, objective, approach, dependencies).
Your job is to make it concrete and actionable as a detailed plan.
Use web research to look up technical details, verify feasibility, and find reference materials
that will make your plan more concrete and actionable for the executor.

GOOD PLANS:
- Make each component SPECIFIC and actionable (not vague platitudes)
- Consider both success AND failure scenarios
- Build on the approach in the artifact direction
- Add concrete details the executor needs

BAD PLANS:
- Vague hand-waving ("do research on X")
- Ignoring the approach in the artifact direction
- Missing critical details the executor needs
</plan_guidelines>

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
Your workspace: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1/results/out.json`
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
- artifact: art_22ppE1snfHKj
  state: 'null'
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
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<strategy_domain_reasoning>
How the strategist established that researchers in this field reason, at the level of the field's principles and standards of evidence. Take it as the starting point for the concrete practice below — extend or correct it where your own reading disagrees, and say so when you do.

FIELD: scientometrics / science of science using network-science methods (target: Applied Network Science, collection 'Networks for everyday life'). No domain handbook fits (the four offered cover computational linguistics, mech-interp, multi-agent LLMs and neuro-symbolic AI), so the principles below are provisional. They rest on the literature this run has already read and verified (art_dxvRpQufMR0e: 22 ANS papers, Guevara 2016, Weng 2013, Maillart 2026; art_EesdB8cuSfcU: relatedness/exit prior art, ANS skeleton) and on this run's own measured failure modes. (1) PRINCIPLES. There is no single ground truth for emergence (Rotolo, Hicks & Martin 2015), so a signal is believed only when it predicts several later outcomes beyond count baselines. Fields differ in size and citing habits, so breadth must be volume-adjusted (rarefaction, residualisation), otherwise it relabels growth. Co-word analysis has argued since Callon et al. (1991) about density versus centrality of themes, and Salatino et al. (2018) tie topic birth to rising density. Our claim (loose, churning neighbourhoods predict breadth) takes a side in a live dispute, so it must be tested against the consolidation reading, not asserted. Relatedness (Hidalgo 2007) is the default model of diversification and is not a contribution. (2) WHAT CONVINCES. A temporal out-of-sample cohort that no selection step has touched, scored once from a sealed specification. Controls for the confounds a reviewer names first: concept TYPE (methods travel; Leydesdorff & Rafols 2011 'research technologies'), pre-existing generic terms, and volume. Replication within strata, with I2 reported. A within-unit design (concept fixed effects) with pre-trend checks, placebos and the reverse path, before any temporal 'mechanism' is claimed; staggered event studies need heterogeneity-robust estimators (Sun & Abraham 2021; Callaway & Sant'Anna 2021). Case studies are chosen from the quantitative extremes, not cherry-picked. (3) STANDARD MOVES, AND WHAT EACH RULES OUT. Rarefied O2r and O2r_resid rule out volume. Partial correlation given B5 rules out 'just popularity'. Held-out fields plus a later cohort rule out tuning to domain and period. Concept-level resampling rules out pseudo-replication across episodes. Leave-one-group-out and DL pooling stop one field from driving the average. Degree-preserving or label permutations rule out 'any structure works'. (4) FAILURE MODES, most of them already observed in this run. Mechanical coupling: an indicator built from the same papers whose spread is the outcome (an all-papers ego network gains off-home topics precisely when the concept spreads). Pre-onset footprint leaking into 'early' features (M0_density_end). Selection and scoring on the same concepts (H3 shrank from 0.14 to 0.03). Results that depend on the backbone or proximity (the retained frontier reversed under min-cp). Post-unseal subgroup hunting. A record whose text contradicts its own files (the review's BLOCKING items). Unexecuted artifacts that were never recorded (Exp9).
</strategy_domain_reasoning>

<domain_practice>
FIRST WORK OUT HOW THIS KIND OF STUDY IS ACTUALLY BUILT IN THIS FIELD. Then
write the plan.

The strategy already settled what the field believes and what it counts as
convincing. Your job is the level below that: how work of exactly this kind
is designed, run and reported by the people who do it, concretely enough that
the executor's output would be recognised as competent by one of them.

Establish, for this field and this artifact type:

- BASELINES AND COMPARISONS. Which comparisons appear in every paper of this
  kind, named specifically. Which one would a reviewer name first if it were
  missing, and what is the standard way of tuning it fairly?
- CASES AND DATA. Which datasets, corpora, cohorts, benchmarks, case sets or
  sources are standard here, and which are known to be saturated, leaked,
  deprecated or unrepresentative. Prefer the ones the field actually uses,
  and say why when you pick something else.
- CONTROLS AND WHAT IS HELD CONSTANT. What has to be held fixed for the
  comparison to mean anything, and which confound this design is most likely
  to be caught on.
- HOW MUCH IS ENOUGH. Sample sizes, item counts, seeds, repeats, splits —
  the number below which nobody in this field believes a result, and what the
  field reports alongside a point estimate (variance, intervals, a
  significance or uncertainty treatment). When a power analysis, or the
  effect sizes already on record, say the panel cannot detect the size of
  effect the plan is chasing, the fix is more graded samples or checkpoints
  — not more candidate metrics. An underpowered panel stays underpowered no
  matter how many readouts run over it.
- MEASURES AND REPORTING CONVENTIONS. Which measures are standard, how they
  are computed here, and the conventions a reader will expect to see — what
  is reported, against what, in what form.

Not every axis applies to every artifact type: a proof has proof standards
and an accepted level of rigour rather than sample sizes, a research artifact
has source quality and coverage, a dataset has provenance, licensing and
documentation norms. Answer the ones that apply and skip the ones that do not
rather than inventing content for them.

HOW MUCH EFFORT. Bounded, like the strategist's: the fitting domain handbook
plus a handful of targeted lookups — one or two recent papers doing this exact
kind of study, a benchmark or dataset card, a methods or reproducibility note.
Read what the field does; do not reason it out from first principles. You
cannot run code, so this is reading only.

THEN CHECK THE PLAN AGAINST IT.
- `domain_practice`: what you established above, concretely — named baselines,
  named data, the numbers, the measures, with what you read.
- `practice_alignment`: go through the plan you just wrote against that list
  and say, point by point, where it MEETS the field's practice and where it
  DEPARTS from it. For every departure: why it is justified here (budget,
  scope, the claim being narrower) and what it costs the result's
  credibility. A departure nobody named is the one a reviewer finds.
- Where the check exposes a gap you can close inside the budget, close it in
  the plan rather than reporting it. `practice_alignment` is for what remains
  after you have fixed what you can.
</domain_practice>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter4_dir1
type: experiment
objective: >-
  DECISIVE REPLICATION + CONFOUND TEST of the openness claim (RQ1) on a fresh 2015-2016 onset cohort that no screen has touched.
  Does HOME-ONLY OPEN keep a positive partial association with size-adjusted breadth (O2r_m50, O2r_resid at t0+6..t0+8) through
  the full control ladder (B5 -> +CONTACT_REACH -> +CONCEPT TYPE -> +PRE-ONSET FOOTPRINT -> +label coverage -> +home-group
  FE)? Does it hold within method concepts and within object concepts? Is RETENTION_RATIO_early negative? Secondary: replicate
  the frozen Exp8 learned models and the n_authors_early leads.
approach: >-
  INPUTS ARE READ BY PATH (run root = the run directory; experiments may formally depend only on datasets/research, so earlier
  experiments are reused by path). EXP5 = 3_invention_loop/iter_2/gen_art/gen_art_experiment_5/ (art_wxWssKSUR45f): frame_concepts.csv
  (12,499), concept_outcomes.csv, frozen_spec.json (split/folds), scan/agg_counts.parquet (concept ci x year 1995-2022 x venue
  field x tagstate counts for ALL 56,643 legacy concepts), scan/year_field_totals.npz, scan/co_by_year.npz, scan/llm_cache
  (precision-gate cache), results/source_field.parquet (source -> venue field), matcher.py, grounding.py, rangefile.py, scan_full.py.
  EXP8 = 3_invention_loop/iter_3/gen_art/gen_art_experiment_8/ (art_dFQ6jbgNsR6Q): passA.py, passB.py, lib/ego.py + lib/ego_ctx.py
  (EXP3 ego features ported, 1-year windows W1..W3, validated to 1e-15), lib/matcher.py, lib/rangefile.py, build_features.py,
  outcomes.py, data/frame_matches_early/part_*.parquet (grounded hits t0-3..t0+2 with work, topic, author ids), data/cites_early.parquet,
  data/ref_sample.parquet, data/bg_topics.npz, data/features_basic.parquet, data/ego_features.parquet, data/outcomes.parquet,
  data/analysis_table.parquet, results/indicator_matrix.parquet, results/indicator_dictionary.csv, results/frozen_spec.json,
  results/heldout_unit_results.csv, results/portability_table.csv, results/case_exemplars.json, results/o2r_resid_fit.json,
  models/*.joblib (frozen ElasticNet/L1-logit and EBM per outcome). EXP7 = 3_invention_loop/iter_3/gen_art/gen_art_experiment_7/
  (art_22ppE1snfHKj): results/state_panel_{dev,heldout}.parquet (authoritative D3 concept x field x year states), step2_{dev,heldout}.json.
  EXP6 = 3_invention_loop/iter_2/gen_art/gen_art_experiment_6/ (art_N-mpomDZZ1ln): lib/h2.py (ENTERED/RETAINED/LOST), lib/traj.py,
  inputs/field_backbone.json (26-field PMI backbone 1998-2002). EXP3 = 3_invention_loop/iter_1/gen_art/gen_art_experiment_3/
  (art_yrradSC27HtQ): backbone/slice0-2.npz (topic PMI slices 2000-04/05-09/10-14, Leiden gamma 3). If the run volume is not
  mounted, re-implement from these definitions against the public zero-credit OpenAlex S3 snapshot with the same HTTP-range
  code and log every deviation in deviations.json. SHARED DEFINITIONS (verbatim in every artifact). OPEN components over t0..t0+2
  papers only, Exp8 lib/ego.py code: new_edge_rate, n_comm_W3, participation, NOV_res, ego_density_W3, edge_persistence. OPEN
  = mean of z(new_edge_rate), z(n_comm_W3), z(participation), z(NOV_res), -z(ego_density_W3), -z(edge_persistence), with z
  constants frozen on the EXP5 frame (all 12,499 concepts = SELECTION data); a concept needs >= 4 of 6 components. Builds:
  ALL-PAPERS (as Exp8); HOME-ONLY (ego network from the concept's grounded papers whose venue field is in its home set; venue-unlabelled
  papers excluded; home-paper coverage logged); SIZE-MATCHED ALL-PAPERS (mean over 20 random subsamples of all early papers
  down to the home-only paper count; separates 'fewer papers' from 'home restriction'). RETENTION_RATIO_early and CONTACT_REACH
  as in Exp8 (reported separately, not in OPEN). B5 = log early volume, early growth, off-home share, entropy, reach (Exp8).
  Home = field(s) with >= 40% of the first 30 grounded works (>= 2 homes = intersection-born). D3 states from EXP6 lib/h2.py.
  STATISTICS: resampling unit = concept (named in every table); 2,000-draw concept bootstraps (refit); DerSimonian-Laird pooling
  with I2; Holm within each pre-declared family. SEALING: frozen_spec.json (formulas, signs, thresholds, covariates, code
  SHA-256) written and hashed into logs/seal.log BEFORE any outcome of the evaluation body is computed; that body is scored
  once. BUDGET: 0 OpenAlex API credits (zero-credit S3 snapshot only); OpenRouter spend capped per artifact as stated, running
  total from usage.cost, stop on the first 'AI Inventor per-run OpenRouter budget' 403. STEP 0, PRE-REGISTRATION FIRST. Write
  prereg.md + frozen_spec.json holding the OPEN definition and signs, the ladder, the groups, the success rules below and
  the fallback. Hash them. STEP 1, COHORT FRAME, from EXP5 scan/agg_counts.parquet (years <= t0 only for selection). Candidates
  are legacy concepts NOT in EXP5 frame_concepts.csv, with onset t0 in {2015, 2016} under the IDENTICAL EXP5 newborn rule
  and TAG grounding. The newborn check may use counts through t0+2 <= 2018, exactly as frozen. Apply the EXP5 per-concept
  LLM precision gate with the same prompt and model, reusing scan/llm_cache. Home and groups: CS+Eng, BGM+Med, PHYS, LIFEENV,
  SOC, MATHDEC (MATHDEC reported only). DECLARED FALLBACK: if fewer than 800 concepts pass, add 2017 onsets with outcomes
  at t0+5..t0+7. STEP 2, ONE ZERO-CREDIT SNAPSHOT PASS (adapt EXP8 passA.py; the matcher and grounding stay unchanged). For
  cohort concepts, take every grounded work 2012-2024: work id, year, primary source id (-> venue field via source_field.parquet),
  topic ids, author ids and referenced_works. Check that yearly counts <= 2022 reproduce agg_counts exactly (else stop and
  log). If time allows, run a second pass (EXP8 passB.py) for O4 citations to early works; O4 is the first thing dropped.
  STEP 3, FEATURES over t0..t0+2 only, for the cohort AND the EXP5 frame (EXP5 home-only builds come from data/frame_matches_early
  + source_field, with no new pass). OPEN in all three builds, via Exp8 lib/ego.py on EXP3 backbone slice2 (2010-14, pre-onset
  for the cohort, so leakage-free). Skip betweenness in the home-only and size-matched builds (it is not in OPEN, and it cost
  98% of ego time). Parallelise across 7 vCPUs. Also compute each OPEN component alone, RETENTION_RATIO_early, CONTACT_REACH,
  B5, n_authors_early and every Exp8 indicator needed by the frozen models/*.joblib. STEP 4, CONCEPT TYPE (LLM; cap $3). Label
  all EXP5 + cohort concepts (about 14.5k) with a cheap OpenRouter model. The input is the concept label, its Wikidata description
  where the art_O7Dq4L02QnDN key has it, and 3 early titles. There are 4 classes: method/technique/tool; object/material/organism/disease;
  property/measure/theory; topic/field. A separate flag marks GENERIC pre-existing terms (e.g. 'Coefficient of variation').
  BENCHMARK: 300 concepts stratified by group are double-labelled by a second model, and 60 are hand-checked by the executor.
  Required: precision >= 0.85 on method-vs-object. If this fails, revise the prompt once; if it fails again, restrict within-type
  tests to two-model-agreement concepts and log it. STEP 5, PRE-ONSET FOOTPRINT from agg_counts (years < t0): log grounded
  papers t0-10..t0-1, number of fields pre-t0, a re-emergence flag (any pre-t0 year >= 25% of the t0+2 count), and Wikipedia
  creation year < t0 from art_O7Dq4L02QnDN (year_usable only) as a generic-term marker. STEP 6, SELECTION ON EXP5 (all 12,499).
  Confirm the signs of OPEN (every build) and fit the ladder on O2r_m50 and O2r_resid. Freeze the z constants, the O2r_resid
  a/b (Exp8 o2r_resid_fit.json), the type classifier outputs, the Holm family (OPEN_home, OPEN_all, OPEN_sizematched, RETENTION_RATIO
  x 2 outcomes) and the rules. Write frozen_spec.json and hash it into logs/seal.log. Record here, as selection-data results,
  the EXP5 ladder with concept type and footprint (the first test of confound (ii) on the old data). STEP 7, ONLY THEN compute
  cohort outcomes: O2r_m50 (exact hypergeometric), O2r_resid, O1c, O1b, O3 and O4 at t0+6..t0+8. For 2015 onsets only, also
  a <= 2022 sensitivity at t0+5..t0+7. Hash the outcome file and score ONCE. REPORT the partial Spearman of each OPEN build
  at every ladder rung (concept bootstrap 2,000), per group with DL pooling and I2, within method and within object concepts,
  and for each OPEN component alone. Also RETENTION_RATIO_early given B5, and the ALL-vs-HOME-ONLY difference with a paired
  bootstrap. SECONDARY (frozen, no refit): Exp8 O3 L1-logit dAUC over B5, n_authors_early for O3/O1b/O1c, O4 EBM Spearman,
  O2r ElasticNet gain over B5, and CONTACT_REACH (with and without intersection-born concepts). Missing model inputs are imputed
  at the frozen DEV median. A replication is dropped if more than 20% of its model weight is imputed. VERDICT RULES (frozen).
  CONFIRMED if HOME-ONLY OPEN has psp > 0 with CI > 0 at the type and footprint rungs, a positive sign in >= 4 of 5 groups,
  psp > 0 within both method and object concepts, and RETENTION_RATIO_early < 0 given B5. DISCONFIRMED if the CI at the type
  rung includes 0. Outcomes (a) 'type absorbs OPEN' and (b) 'home-only fails, all-papers holds = mechanical' are reported
  as stated. No subgroup hunting after the unseal. DROP ORDER if time is short: O4/Pass B, then the learned-model replications,
  then the 2017 fallback extension. Never drop the home-only build, the type rung, or the single unseal. OUTPUTS: cohort_frame.csv,
  concept_types.csv (both frames; reusable), type_benchmark.json, footprint.csv, features_cohort.parquet, features_exp5_homeonly.parquet,
  frozen_spec.json + logs/seal.log, outcomes_cohort.parquet (hashed), cohort_result.json (every rung, group, type and CI),
  ladder and forest figures, and method_out.json with per-concept predictions.
what_it_would_show: ''
depends_on:
- id: art_O7Dq4L02QnDN
  label: concept key
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
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
</dependencies>

<prior_work>
Everything this run has already produced, earlier rounds included. This is what
the plan builds on.

--- Artifact 1 ---
id: art_xp8BGBJZsxeI
name: gen_art_experiment_1
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
iteration: 1
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

--- Artifact 2 ---
id: art_yrradSC27HtQ
name: gen_art_experiment_3
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
iteration: 1
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

--- Artifact 3 ---
id: art_33_KKk_G8Gw5
name: gen_art_experiment_4
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
iteration: 1
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

--- Artifact 4 ---
id: art_wxWssKSUR45f
name: gen_art_experiment_5
type: experiment
title: Do hub fields keep new concepts? Held-out test
summary: |-
  Sealed held-out test of H1 (does the adopting field's frozen 1998-2002 eigenvector gateway centrality predict retention of a newly adopted concept beyond B5, field size, phi(home,j), relatedness density, the field's leave-concept-out retention propensity P_j(-c), coverage and episode size?) and H3 (does gateway-weighted early landing G predict size-adjusted breadth O2r_resid given B5?).

  Data: one zero-credit scan of all 2,040 OpenAlex S3 works files (2026-09-23; 476,196,327 works; 129.4M base works 1995-2022), with Aho-Corasick title matching of 56,643 legacy concepts (levels 2-5) plus Wikidata aliases and stemmed verification: 60.0M verified matches. Grounding: legacy-tag rule TAG (test P 0.947, R 0.659), chosen on a 390-pair LLM benchmark with 60 hand-checked pairs (90% agreement), plus a per-concept LLM precision gate ($2.28 of OpenRouter).

  Authoritative S1 tables for iteration 3: frame_concepts.csv (12,499 concepts: DEV 4,771, held-out PHYS/LIFEENV/SOC/MATHDEC 742/1,113/1,352/165, cohort 4,356), episodes.csv (27,393 concept x off-home-field episodes with R and the R_abs1-3 sensitivity outcomes for all splits), concept_outcomes.csv (O1, O3, O2r_m30/m50) and concept_features_basic.csv (G, G_A, G_btw, REL_home, RS, DOM_*, count/label indicators, B5).

  The spec was frozen on DEV (sha256 in logs/seal.log) and unsealed once. H1: held-out dAUC -0.00001 [-0.0006, +0.0003] (DEV +0.00001), DL pooled -0.00004 (I2 = 0), cohort -0.0001. The placebo was not exceeded and the conditional logit is null. Verdict: DISCONFIRMED. Power: the minimum detectable dAUC is 0.004. The relatedness pair beats gateway on held-out (+0.0034 [0.0010, 0.0051] vs 0). The baseline ladder shows gateway's DEV signal (+0.0019 over the iteration-1 base) vanishes once P_j(-c) is added, and reverses on held-out (-0.0016). Gateway alone has AUC 0.605 on DEV vs 0.506 on held-out (0.41 in SOC): gateway is a domain-specific proxy for 'fields that keep things'. Iteration-1 replication: +0.023 (vs +0.10). H3: held-out partial rho G 0.030 / G_A 0.026 / G_btw 0.046 (Holm p = 0.0045); within-group DL pooled G 0.068 [0.029, 0.107]. The effect is small; the tests show 0/40 false positives on shuffled outcomes. REL_home is strongly negative (-0.14).

  An independent audit (sklearn, own AUC) matches to 1e-6. Deviations: no OpenAlex API audit or insularity (credits exhausted); LLM cap raised to $3.50; T3 t0 agreement 53%. See README.md, results/*.json and figures/.
iteration: 2
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

--- Artifact 5 ---
id: art_N-mpomDZZ1ln
name: gen_art_experiment_6
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
iteration: 2
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

--- Artifact 6 ---
id: art_lwI2DuRtQRZX
name: gen_art_evaluation_1
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
iteration: 2
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

--- Artifact 7 ---
id: art_dxvRpQufMR0e
name: gen_art_research_1
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
iteration: 2
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - research_out.json
  - research_verification.json

--- Artifact 8 ---
id: art_22ppE1snfHKj
name: gen_art_experiment_7
type: experiment
title: Do concepts spread from fields that keep them?
summary: |-
  Decisive zero-credit test of the retained-frontier claim (EXP6 lead: a concept next enters fields related to the off-home fields that currently RETAIN it, d0_ret_rel) against the field-standard relatedness-density rival built as the literature builds it (omega = sum U phi / sum phi with U = RCA>1: annual Hidalgo current portfolio [primary], 3-year, Guevara-2016 cumulative and persistence-filtered), plus share-weighted density (D_vol, D_vol_w3, D_cum), and of the abandonment penalty (d_lost: relatedness to dropped off-home presences). Conditional logit (Breslow) on concept x target-field x year entry risk sets, concept-year strata, frozen 1998-2002 26-field PMI backbone; nested ladder R0 (home relatedness, log size, entered density, own gateway) -> R1 +D_rca_1y -> R2 +D_vol -> R3 +d0 -> R4 +d_lost; S_strict = all 4 RCA + both D_vol; S_pca; A1 = R0 + d_lost.

  STEP 1 (EXP6 frame, robustness): risk sets rebuilt row-for-row (max diff 4e-16) and EXP6 held-out M1 vs M0 LR 68.57 / d0 0.2809 reproduced; d0 survives RCA>1 and volume: R3 0.262 [0.196,0.320], S_strict 0.252 [0.188,0.315], permutation p=0.001.

  STEP 2 (independent frame: EXP5 12,499 concepts minus every EXP6 concept by OpenAlex ID/QID/normalised label -> 11,841; DEV 4,486 used for code, standardisation, power and rules; hash-frozen, git 24da538; held-out scored ONCE). Held-out pooled PHYS+LIFEENV+SOC+MATHDEC (3,162 concepts, 6,978 entries): LR(R3 vs R2)=325.8, d0=0.322 [0.291,0.355] (concept refit bootstrap 1,000), S_strict 0.304 [0.268,0.336], crossed concept x field CI [0.201,0.468]; positive in PHYS 0.15, LIFEENV 0.40, SOC 0.30 (MATHDEC 0.07, underpowered, excluded pre-freeze), cohort 2010-14 0.321 [0.292,0.347]; DL 4 groups 0.243 [0.118,0.368], I2=0.92. Retained-label permutation p=0.001, rewire p=0.004, node-label p=0.003; dose by persistence age 2/3/>=4 = 0.10/0.08/0.30 (4+ minus 2: 0.21 [0.16,0.26]); stable under target-field FE (0.30), RCA-defined entry event (0.24), primary-topic fields, min_n 3/5, horizon 8, exclusions. BUT the pre-declared volume-matched contrast (retained vs entered-not-retained fields in the same current x cumulative volume cell) is null: -0.028 [-0.105,0.046] (fine bins -0.026), so frozen verdict FRONTIER = PARTIAL ('persistence confounded with volume'). Also: under a Hidalgo min-conditional-probability proximity d0 vanishes (-0.021, p=0.012) - backbone-specific; the econ-geo LPM row gives d0 slightly negative, and an EXPLORATORY diagnostic shows it is ~0 once size enters non-linearly (relative-odds, not additive-probability, effect). ABANDONMENT: d_lost in A1 = -0.007 [-0.036,0.022] (power 0.99 at -0.06) -> INCONCLUSIVE/no penalty; with d0 it turns positive (+0.064). Within-stratum AUC R2 0.847 -> R3 0.852; Guevara-comparable global AUC of D_rca_cum 0.635 (flagged, different unit/event).

  Checks: 10 unit tests pass; planted d0=0.2 detected 100%, null rejection 0/200; shuffled entries 0/20; independent audit (hand Breslow exact reproduction; statsmodels EXACT likelihood LR ratio 0.99-1.02; 20 rows re-derived from raw counts; inline DL) all pass. Outputs: results/frontier_result.json (all numbers), step1/step2 JSONs, frozen_spec + seal/unseal logs, risk-set and state-panel parquets, null draws, 6 figures (forest d0 / d_lost by unit, ladder, dose, null histograms, volume-matched), method_out.json = full_method_out.json (252,922 held-out candidate rows with predict_R2_rca_vol_baseline vs predict_R3_retained_frontier from frozen DEV coefficients). No LLM or OpenAlex spend.
iteration: 3
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

--- Artifact 9 ---
id: art_dFQ6jbgNsR6Q
name: gen_art_experiment_8
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
iteration: 3
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

--- Artifact 10 ---
id: art_7W9xiIO3FVBs
name: gen_art_evaluation_2
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
iteration: 3
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

--- Artifact 11 ---
id: art_EesdB8cuSfcU
name: gen_art_research_2
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
iteration: 3
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_research_2
out_expected_files:
- research_out.json
- reproducibility.md
out_dependency_files:
  file_list:
  - research_out.json
  - research_verification.json
</prior_work>

<build_on_prior_work>
BUILD ON WHAT THE EARLIER ROUNDS ALREADY PRODUCED. That is the default, not an option.

<prior_work> lists what this run has already built. Before planning anything
from scratch, go through it and find what this artifact can stand on:
- data that is already collected, cleaned, split or labelled
- models, fits, checkpoints or indexes that are already trained or built
- harnesses, scripts and evaluation code that already run
- the findings themselves, the NEGATIVE ones included — a condition already
  ruled out is a result to build past, not ground to cover again

Then say in `builds_on`, concretely, what this plan reuses: which artifact,
which file, from where. The executor gets a dependency's files only through
the direction's declared dependencies, so when the plan leans on an artifact
that is not among them, say in the plan where the executor picks it up
(workspace path, output file) and keep the plan runnable if it is missing.

STARTING A FRESH LINE is allowed on exactly two grounds:
1. The iteration's move is a WIDEN — the run deliberately went back to the
   original ask to screen different candidate answers, so a new line is the
   point of the round.
2. The line this would have continued is a SETTLED NEGATIVE — already tested
   well enough that pushing it further buys nothing.
On either ground, `builds_on` says which one it is and why, and still names
whatever infrastructure (data, harness, code) the new line can reuse.

"Cleaner to start over" is not one of the two grounds. Neither is a plan that
simply does not mention the earlier rounds.
</build_on_prior_work>

<own_your_inputs>
A STEP THIS PLAN COMMISSIONS MUST HAVE ITS INPUTS OWNED BY SOMETHING SCHEDULED.

If this plan pre-registers a later phase — a held-out confirmation, a blind
set, a second pass, a replication — that phase needs inputs of its own:
labels, ground truth, an annotation pass, a scored reference. Before writing
that phase into the plan, name what produces those inputs and where that
production is scheduled: inside this artifact's own steps, or as one of the
direction's declared dependencies. Say it concretely, not "labels will be
added" — which task, at which point in the plan.

A later step whose inputs nobody is scheduled to produce is not a plan for
that step, it is a plan to skip it while looking like it was included.
</own_your_inputs>



<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for experiment artifacts:
  - gpu_basic: 1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models (fallback: GPUs cheap→expensive: 2000 Ada → A4000 → 4000 Ada → L4 → PRO 4000 → PRO 4500 → 4090 → 5090)
  - cpu_plus: 4 vCPUs, 32GB RAM — large datasets, memory-intensive processing (fallback: CPUs cheap→expensive, then GPU hosts cheap→expensive (all ≥32GB RAM))

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
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
  "description": "Plan for an EXPERIMENT artifact.",
  "properties": {
    "domain_practice": {
      "default": "",
      "description": "How a study of exactly this kind is actually built and run in THIS field: the baselines every comparable paper reports, the datasets/corpora/cohorts/case sets that are standard (and the ones known to be saturated or unrepresentative), what is held constant, the sample sizes and repeats below which nobody believes a result, and the measures and reporting conventions a reader expects. Name what you read.",
      "title": "Domain Practice",
      "type": "string"
    },
    "practice_alignment": {
      "default": "",
      "description": "This plan checked point by point against that practice: where it meets the field's norms and where it departs from them, with why each departure is justified here and what it costs the result's credibility.",
      "title": "Practice Alignment",
      "type": "string"
    },
    "builds_on": {
      "default": "",
      "description": "What this plan REUSES from earlier rounds, named concretely: which artifacts, files, datasets, checkpoints, fitted models or negative findings, and where the executor picks each one up. If the plan starts a fresh line instead, say so here and give the reason it is allowed to \u2014 the iteration is a widen, or the prior line is a settled negative.",
      "title": "Builds On",
      "type": "string"
    },
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_basic",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu_basic', 'gpu_plus', 'cpu_plus', 'cpu_basic'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
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

### [3] TOOL CALL — Glob · 2026-09-29 02:07:07 UTC

```
Pattern: "*"
```

### [4] TOOL RESULT — Glob · 2026-09-29 02:07:07 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.aii_claude_session.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/config", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/HEAD", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/info/exclude", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/update.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/push-to-checkout.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/prepare-commit-msg.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-receive.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-rebase.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-push.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-merge-commit.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-commit.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-applypatch.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/post-update.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/fsmonitor-watchman.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/commit-msg.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/applypatch-msg.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/description", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/field_backbone.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/topic_meta.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/topic_ids.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/backbone/slice2.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/backbone/slice1.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/backbone/slice0.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/source_field.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/frozen_lexicon.sha256", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/lexicon_v1.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/snapshot/works_manifest.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/panel_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/frame_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/models_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/seal_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/stats_core.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/h2.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/common3.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego_exp3_orig.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/rangefile.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/matcher.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/common5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_0065.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_0065.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_0065.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_0065.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1407.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1407.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1407.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1407.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1125.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1125.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1125.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1125.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1918.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1918.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1918.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1918.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/tests/t1_check.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/t1_passA_exact_65_1125_1407_1918.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/logs/passA.pid", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1882.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1882.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1882.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1882.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1868.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1868.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1868.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1868.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1934.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1934.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1934.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1934.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1949.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1949.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1949.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1949.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1583.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1583.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1883.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1583.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1883.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1583.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1883.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1883.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1579.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1579.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1579.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1579.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1297.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1297.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1297.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1297.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1299.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1299.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1299.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1299.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1581.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1581.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1581.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1581.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1690.json"], "durationMs": 573, "numFiles": 100, "truncated": true, "totalMatches": 12871, "countIsComplete": true}
```

### [5] TOOL CALL — Glob · 2026-09-29 02:07:07 UTC

```
Pattern: "*"
```

### [6] TOOL CALL — Glob · 2026-09-29 02:07:07 UTC

```
Pattern: "**/*"
```

### [7] TOOL RESULT — Glob · 2026-09-29 02:07:07 UTC

```
{"filenames": [], "durationMs": 56, "numFiles": 0, "truncated": false, "totalMatches": 0, "countIsComplete": true}
```

### [8] TOOL RESULT — Glob · 2026-09-29 02:07:07 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/.aii_claude_session.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/rangefile.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/works_manifest.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/probe.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/logs/schema_leaf_paths.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts_manifest.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_01.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_00.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_03.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_02.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_05.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_04.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_06.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_08.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_07.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_10.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_09.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot/concepts/part_11.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/timing_probe.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/logs/timing_probe.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/lexicon.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/lexicon_v0.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/lexicon_v0_summary.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/matcher.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/sample_info.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/source_field.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/untsamp_0065.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/unt_0065.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/resv_0065.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/done_0065.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/agg_0065.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/untsamp_1407.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/unt_1407.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/resv_1407.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/done_1407.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/agg_1407.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/untsamp_1125.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/unt_1125.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/resv_1125.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/done_1125.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/agg_1125.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/untsamp_1934.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/unt_1934.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/resv_1934.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/done_1934.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/agg_1934.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/untsamp_1949.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/unt_1949.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/resv_1949.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/agg_1949.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/done_1949.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/untsamp_1918.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/unt_1918.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/resv_1918.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/done_1918.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/stage_test_parts/agg_1918.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/wikidata_aliases.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/logs/wikidata.pid", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/wikidata_aliases.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/logs/wikidata.log", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/logs/wikidata_stdout.log", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/untsamp_1949.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/unt_1949.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/done_1949.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/agg_1949.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/untsamp_1918.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/unt_1918.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/done_1918.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/agg_1918.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/untsamp_1934.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/unt_1934.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/done_1934.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/agg_1934.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/agg_1868.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/untsamp_1882.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/untsamp_1868.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/unt_1882.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/unt_1868.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/done_1882.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/done_1868.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/agg_1882.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/untsamp_1883.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/unt_1883.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/done_1883.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/agg_1883.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/untsamp_1583.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/unt_1583.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/done_1583.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/agg_1583.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/untsamp_1579.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/unt_1579.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/done_1579.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/agg_1579.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/untsamp_1581.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/untsamp_1301.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/unt_1581.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/unt_1301.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/done_1581.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/agg_1581.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/aborted_v1a_parts/agg_1301.npz"], "durationMs": 848, "numFiles": 100, "truncated": true, "totalMatches": 22627, "countIsComplete": true}
```

### [9] TOOL CALL — Glob · 2026-09-29 02:07:13 UTC

```
Pattern: "{*.py,*.md,lib/*.py,results/*.json,results/*.csv,data/*.parquet,models/*}"
```

### [10] TOOL RESULT — Glob · 2026-09-29 02:07:13 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/panel_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/frame_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/models_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/seal_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/stats_core.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/h2.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/common3.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego_exp3_orig.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/rangefile.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/matcher.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/common5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/t1_passA_exact_65_1125_1407_1918.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego_ctx.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/common.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/seal.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/rq1stats.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/unit_tests.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/t0_8_ego_port.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/design.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/o5_join.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/o5_events.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/dev_select.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/method.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/counts_check.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ref_sample.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/features_basic.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/t4_timing_nnull200_cut4.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passB.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/build_features.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/indicators.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/features_config.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/provenance.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/cites_early.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/checks.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/heldout.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/outcomes.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/o2r_resid_fit.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/o4_reference_expectations.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/outcome_base_rates.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/outcomes_sealed.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/outcomes_dev.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_features.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/t4_ego_sanity.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/indicator_corr_dev.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/size_diagnostic_dev.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/indicator_clusters_dev.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/rederive.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/dev_ranking.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/indicator_dictionary.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/dev_ranking_sensitivity.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/rq1_dev_selection.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O1c.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O1c.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O2r_m50.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O2r_m50.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O2r_resid.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O2r_resid.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O4.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O4.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O1b.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O1b.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O3.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O3.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O5.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O5.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O5_WW.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O5_WW.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/learned_model.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/power_dev.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/frozen_spec.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/analysis_table.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/outcomes.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/heldout_summary.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/heldout_unit_results.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/learned_vs_single_heldout.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/portability_table.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/prereg_verdicts.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/prereg_b5_minus_reach.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/sensitivities_pooled.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/sensitivities_heldout.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/audit.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/audit.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/rederive.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/make_outputs.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/case_exemplars.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/rq1_heldout.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/readme_tables.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/deviations.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/reproducibility.md", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/README.md"], "durationMs": 258, "numFiles": 92, "truncated": false, "totalMatches": 92, "countIsComplete": true}
```

### [11] TOOL CALL — Glob · 2026-09-29 02:07:13 UTC

```
Pattern: "{*.py,*.md,results/*.csv,results/*.json,scan/*.parquet,scan/*.npz,scan/*.json}"
```

### [12] TOOL RESULT — Glob · 2026-09-29 02:07:13 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/rangefile.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/probe.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/timing_probe.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/lexicon.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/lexicon_v0_summary.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/matcher.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/sample_info.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/wikidata_aliases.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/wikidata_aliases.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/frame.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/backbones.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/features.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/seal.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/unit_tests_T0.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/checks.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/backbones.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/llm.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/oa_client.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/grounding_bench_summary.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/handcheck_sheet.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/handcheck_labels.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/untagged_passrate.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/audit.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/frame_build_em30_w1.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/frame_summary.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/p78_agreement.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/h1_dev_smoke.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/h1_heldout_smoke.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/h1_dev.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/fix_pigeonhole.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/models.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/report.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/make_variants.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/h1_heldout.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/checks.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/exploratory_domains.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/exploratory_domain_specificity.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/audit_placebo.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/audit_placebo.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/h3_results.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/method.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/grounding.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/panel.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/prescreen.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/common.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan_full.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/co_by_year.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/year_field_totals.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/agg_counts.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/untagged_rows.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/untagged_sample_titles.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/scan_info.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/prescreen_dropped.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/prescreen_summary.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan/prescreen_survivors.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/onset_candidates_match.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/onset_candidates_grounded.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/deviations.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/reproducibility.md", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/README.md"], "durationMs": 265, "numFiles": 60, "truncated": false, "totalMatches": 60, "countIsComplete": true}
```

### [13] TOOL CALL — Read · 2026-09-29 02:07:21 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/README.md
```

### [14] TOOL RESULT — Read · 2026-09-29 02:07:21 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/README.md", "content": "# Do hub fields keep new concepts? A sealed held-out test on the full OpenAlex snapshot\n\nAI Inventor, invention loop iteration 2, artifact `gen_art_experiment_5` (plan `gen_plan_experiment_1_idx1`).\nThis is a \"deepen\" move on the iteration-1 lead from `art_33_KKk_G8Gw5`: there, the adopting field's gateway centrality\nadded **+0.10 retention AUC** on 80 episodes from 28 concepts.\n\n**H1 (episode level).** When a new concept is adopted by an off-home field *j*, does the field's frozen\n1998–2002 eigenvector *gateway centrality* in the 26-field relatedness backbone predict that *j* keeps it\n(R_cj)? The test asks whether it does so beyond:\n- B5,\n- field size,\n- relatedness to the home field φ(home,j),\n- relatedness density,\n- the field's leave-concept-out retention propensity P_j(−c),\n- coverage,\n- the episode's own early size.\n\nThe specification was frozen on DEV homes (CS, Engineering, Biochem/Genetics, Medicine; onset 2003–09) and scored\n**once** on sealed held-out home groups and the 2010–14 cohort.\n\n**H3 (concept level).** Does gateway-weighted early landing (G) predict size-adjusted later breadth (O2r_resid) given\nB5?\n\n## Headline results\n\n| | DEV (LOGO, OOF) | HELD-OUT (frozen dev fit) |\n|---|---|---|\n| episodes / concepts | 9,079 / 3,987 | 8,515 / 3,085 (+ cohort 9,798) |\n| AUC of baseline X0 | 0.866 | 0.837 |\n| **ΔAUC of adding gateway_j** | **+0.00001** [−0.0007, +0.0005] | **−0.00001** [−0.0006, +0.0003] |\n| per group | CS, Eng, BGM, Med: all within ±0.0001 | PHYS +0.0005, LIFEENV −0.0003, SOC −0.0001, MATHDEC +0.0005 |\n| DerSimonian-Laird pooled (4 groups) | – | −0.00004 [−0.0004, +0.0003], I² = 0 |\n| cohort 2010–14 | – | −0.0001 [−0.0008, +0.0001] |\n| conditional logit, concept FE (β per SD) | +0.058 (p = 0.26) | −0.075 (p = 0.23) |\n| LPM with field FE + time-varying gateway_j,s | −0.003 (p = 0.92) | +0.068 (p = 0.041 concept-clustered; p = 0.17 two-way) |\n| boundary (gateway × top-tercile home; predicted < 0) | −0.051 (p = 0.39) | +0.064 (p = 0.45) |\n| 200 rewired-backbone placebos: real > 95th percentile? | no (placebo p95 = 0.00016) | no (p95 = 0.00011; 36.5% of placebos ≥ real) |\n| crossed concept × field bootstrap (Owen) | [−0.0056, +0.0013] | [−0.0023, +0.0010] |\n| leave-one-adopting-field-out range | [−0.0002, +0.0001] | [−0.0001, +0.0001] |\n| **Relatedness head-to-head** (each added to the same base) | relatedness −0.0002, gateway −0.0001 | **relatedness +0.0034 [0.0010, 0.0051]**; gateway −0.00005 [−0.0007, +0.0002] |\n\n**Verdict H1: DISCONFIRMED** (`results/h1_heldout.json → verdict_H1`). Pre-registered criteria:\n- pooled ΔAUC ≥ 0.05: no;\n- refit CI > 0: no;\n- same sign in ≥ 3 of 4 groups: no (2 of 4);\n- cohort same sign: yes (both ≈ 0);\n- LPM β_within > 0 with p < 0.05: yes, but fragile (two-way clustered p = 0.17);\n- placebo exceeded: no.\n\n**Power.** The null is informative. On the dev covariate structure with the realised held-out n, the minimum\nΔAUC detectable with 80% power is **0.004** (a planted effect of 0.3 SD log-odds). That is 12× smaller than the\npre-registered 0.05 bar.\n\n**Why the iteration-1 lead disappears: the \"trait of the adopting field\" reading.** The pre-registered baseline\nladder (`figures/ladder_dauc.png`) shows the gateway increment on DEV at each baseline:\n\n| baseline | DEV ΔAUC | HELD-OUT ΔAUC |\n|---|---|---|\n| size only | +0.0042 [0.0010, 0.0060] | −0.0017 |\n| iteration-1 base (B5 + size) | +0.0019 [0.0005, 0.0034] | −0.0016 [−0.0035, −0.0002] |\n| + relatedness (φ_home, density) | +0.0007 [−0.0008, 0.0022] | −0.0012 |\n| + P_j(−c) | 0.0000 | 0.0000 |\n\n- On DEV the increment is already small at the iteration-1 base, shrinks once relatedness is added, and **vanishes\n  once the adopting field's own retention propensity P_j(−c) enters**.\n- On HELD-OUT, gateway *hurts* even at the iteration-1 base.\n- Gateway alone has AUC **0.605 on DEV but 0.506 on HELD-OUT**.\n\nThe exploratory per-domain table (`results/exploratory_domain_specificity.json`, post-unseal, never used for the\nverdict) locates the effect:\n- In the four DEV domains, gateway alone predicts retention (AUC 0.59–0.64) and is largely a proxy for the field's\n  retention propensity (Spearman with P_j 0.49–0.83).\n- In Physical sciences, Life/Environment and Math/Decision it is weak (0.52–0.56).\n- In Social sciences/Humanities it is **reversed** (0.41).\n- Gateway is therefore a domain-specific proxy for \"fields that keep things\", not a portable structural mechanism.\n- The standard relatedness model *does* generalise: +0.0034 held-out.\n\n**Iteration-1 replication.** On the frame's P78 subset (85 episodes with n_early ≥ 5, 39 concepts), the\niteration-1 model gives ΔAUC **+0.023** [−0.004, +0.068]. The sign matches iteration 1, but the value is a quarter\nof +0.10, which is consistent with small-sample inflation of the original lead.\n\n**H3 (held-out, n = 2,838 concepts).**\n- Partial Spearman of O2r_resid given B5:\n  - G = +0.030 (one-sided within-group permutation p = 0.002);\n  - G_A = +0.026 (p = 0.004);\n  - G_btw = +0.046 (p = 0.0015).\n- All three are Holm-adjusted to p = 0.0045. The per-group values for G are positive in all 4 held-out groups\n  (0.03–0.09), with a DerSimonian-Laird pooled value of **0.068 [0.029, 0.107], I² = 0**.\n- **Verdict H3: CONFIRMED by the pre-registered test, but the effect is small.** The concept-bootstrap CI of the\n  pooled (not within-group) ρ for G includes 0 ([−0.006, 0.065]), because a negative between-group component\n  offsets it (see `results/h3_results.json → notes`).\n- The rival REL_home (landing in fields related to home) is strongly **negative**: −0.136, DL −0.157.\n  Concepts that land in fields related to their home spread less.\n\n## What was done\n\n1. **Lexicon (outcome-blind, hashed).**\n   - 64,209 legacy OpenAlex concepts (levels 2–5) from the free S3 snapshot. Their surface forms are the name, a\n     joined-hyphen variant and s/es/ies variants.\n   - A form shared by two concepts goes to nobody.\n   - **Pre-screen** on a 1.1% random file sample: 7,566 concepts with ≥ 10 sampled verified hits in 1995–2002 are\n     dropped, because t0 ≥ 2003 is impossible for them.\n   - **Wikidata aliases** for the 56,643 survivors come from the SPARQL endpoint, because `wbgetentities` was\n     rate-limited. Aliases are dropped if they:\n     - have ≤ 3 characters;\n     - are all-caps acronyms of ≤ 5 characters (the TAVI lesson);\n     - equal any concept name, including level-0/1 names;\n     - are ambiguous;\n     - are frequent before 2003;\n     - are lowercase single tokens (see the T2 fix below).\n   - Result: 85,692 alias forms (`lexicon_v1.parquet`; sha256 is the last line of `frozen_lexicon.sha256`).\n2. **One zero-credit scan** (`scan_full.py`) of all **2,040 parquet files (476,196,327 works)** of the\n   2026-09-23 snapshot, via HTTP range reads of 10 leaf columns, in 33 minutes on 4 vCPU.\n   - Base works: 129,360,390 (article|review, not paratext, not xpac, 1995–2022).\n   - Matching: Aho-Corasick over space-padded surface forms (word boundaries enforced), then OpenAlex-like stemmed\n     positional verification. This gives **60.0M verified matches**, aggregated per (concept, year, venue field,\n     primary-topic field, legacy-tag state, match type).\n   - The same pass also produces venue-field totals, 26×26 field co-assignment per year (the backbones) and a\n     hash reservoir of matched titles.\n3. **Grounding, existing resources first.**\n   - The legacy concept tags are present in the snapshot, so TAG = title match AND tag score ≥ 0.3.\n   - **Benchmark:** 390 LLM-labelled title/concept pairs. gemini-2.5-flash-lite labelled all of them and\n     gpt-4.1-nano labelled 146. Cohen's κ was only 0.20, so the 41 disagreements were adjudicated by\n     gemini-2.5-flash.\n   - **The executor read 60 pairs by hand:** 90% agreement with the gold label.\n   - **MiniLM + flags L2-logistic sense filter:** test AUC 0.871. Its precision (0.862) did not beat exact-name\n     precision (0.872), so under T4 the frozen rule is **TAG** (test precision 0.947, recall 0.659), chosen on\n     the benchmark test split only.\n   - **Per-concept LLM precision gate** on 13,413 onset candidates (13.7k calls): 93% have precision ≥ 0.8.\n     864 concepts whose labels did not parse were gated by the sense filter.\n4. **Frame S1** (`frame.py`, art_33 rules):\n   - t0 = first year 2000–2014 with ≥ 20 grounded works; keep 2003 ≤ t0 ≤ 2014, early volume ≥ 30, precision ≥ 0.8.\n   - Home = fields with ≥ 40% of the first 30 venue-labelled works (weak home ≥ 25%).\n   - Episodes = off-home fields with ≥ 2 early works.\n   - R = [share_out ≥ 0.5·share_early AND n_out ≥ 9] over t0+6..t0+8.\n   - Result: **12,499 concepts, 27,393 episodes** (targets: 400 and 4,000).\n     - DEV: 4,771 concepts;\n     - held-out: PHYS 742, LIFEENV 1,113, SOC 1,352, MATHDEC 165;\n     - COHORT: 4,356.\n     - Newborn: 5.4%; weak home: 1,150; intersection-born: 502.\n5. **Backbones.**\n   - Frozen art_33 gateway_eig. The recomputed S0 backbone from the scan correlates with it at Spearman ρ = 1.000.\n   - The time-varying gateway_j,s (slices S0/S1/S2) has a within-field SD of only 0.026, against a between-field\n     SD of 0.279, so the field-FE test has little power.\n   - Placebos: 200 degree-preserving double-edge-swap rewirings (weights re-attached within degree-product\n     quintiles) plus 200 field permutations.\n6. **Models** (`models.py`):\n   - Primary: exact Newton-IRLS L2 logistic (sklearn's objective; matches lbfgs to < 1e-8), leave-one-home-group-out\n     on DEV, with a 2,000-draw concept-clustered **refit** bootstrap.\n   - Secondary: conditional logit, LPM with field + cohort FE (concept and two-way clustered), boundary\n     interaction, relatedness head-to-head, placebos.\n   - Field-level robustness: leave-one-field-out, a crossed concept × field bootstrap, and two- and field-clustered\n     SEs.\n   - Power simulation and the explanatory ladder.\n7. **Freeze → unseal once.**\n   - `frozen_spec.json` (covariates, standardisation constants, thresholds, seeds, hashes, held-out ids) is hashed\n     into `logs/seal.log`.\n   - Pre-unseal checklist: held-out outcome columns absent from every table, and a git commit\n     `a3234b7` of the code and frame.\n   - `seal.py` refuses a second unseal. Held-out models are scored without re-tuning, and every sensitivity is\n     reported (see below).\n8. **Audit.** `audit.py` re-derives the held-out pooled ΔAUC, the per-group values and the H3 partial ρ with\n   separate code: sklearn lbfgs, a Mann-Whitney AUC, its own P_j(−c) and its own rank residualisation. **All match\n   to 1e-6** (`audit.json`).\n\n### Sensitivities (held-out ΔAUC, never used for the verdict)\n\nAll CIs include 0, and every |ΔAUC| is ≤ 0.0023:\n- R_abs1 +0.0008;\n- R_abs2 0.0000 (the direction's literal \"≥ 2 works\" outcome);\n- R_abs3 0.0000;\n- n_early ≥ 5 (iteration-1-exact) −0.0004;\n- newborn-only +0.0023 [−0.0039, 0.0128] (n = 387);\n- excluding intersection-born concepts 0.0000;\n- primary-topic fields instead of venue fields 0.0000;\n- ungrounded \"match\" counts 0.0000;\n- P_j_train −0.0004;\n- without P_j −0.0011 [−0.0026, 0.0000];\n- B5 over t0..t0+4 0.0000;\n- gateway variants (degree −0.0004, betweenness −0.0001, φ_min 0.0000, recomputed S0 0.0000);\n- slice field size −0.0001.\n\n### Tests\n\n| test | result |\n|---|---|\n| T0 unit tests (9) | all pass (`results/unit_tests_T0.json`): rarefaction vs Monte Carlo, Kleinberg, matcher (stem, IoT hyphen/stop words, microRNAs, word boundary), onset, home rule, episode R, seal gate, planted positive control, placebo degree/weight preservation |\n| T1 matcher regression vs iteration 1 (3 files, P78 phrases) | not exact equality: the new matcher is a strict subset, precision 1.00, recall 0.95 (it misses stem-only inflections of non-final tokens) |\n| T2 50-file inspection | found generic single-token aliases; fixed and re-hashed **before** the full scan (`deviations.json: t2_lexicon_fix`) |\n| T3 | recomputed backbone ρ = 1.000 ✓; P78 log yearly counts vs iteration-1 snapshot matches, median ρ = 0.999 ✓; base totals identical ✓; **t0 agreement with the iteration-1 API t0 is 53% (< 70% target)**, because API title+abstract counts are about 2× title counts and cross 20 earlier; API audit **not done** (pool below floor) |\n| T4 | κ = 0.20 (< 0.6, so adjudicated); hand-check agreement 90% ✓; filter did not beat exact-name, so the TAG rule was used |\n| T5 | second bootstrap seed moves CI ends by 0.00007 (< 0.01) ✓; iteration-1 replication same sign ✓ |\n| T6 | pre-unseal checklist passed (`logs/seal.log`) |\n| T7 | independent audit, all match ✓ |\n| shuffled-input controls (`audit_placebo.py`) | held-out ΔAUC with shuffled R: −0.0005 ± 0.0019 (20 shuffles); a planted 1-SD gateway effect is detected (+0.044); both H3 tests give 0/40 false positives on shuffled outcomes; H3 per-group ρ re-derived exactly, DL pooled 0.068 (re-derived 0.0676) |\n\n### Deviations (full list with reasons in `results/deviations.json`)\n\n- The OpenAlex API key had 0 credits and the anonymous pool 999, below the 1,500 floor. Therefore:\n  - **there is no API audit**;", "numLines": 200, "startLine": 1, "totalLines": 306}}
```

### [15] TOOL CALL — Read · 2026-09-29 02:07:21 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/README.md
```

### [16] TOOL RESULT — Read · 2026-09-29 02:07:21 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/README.md", "content": "# Which early network signals travel across fields? A sealed held-out test of ~53 emergence indicators\n\nAI Inventor, invention loop iteration 3, artifact `gen_art_experiment_8` (plan `gen_plan_experiment_2_idx2`, RQ1).\n\n<!-- RESULTS -->\n<!-- TABLES -->\n### Frozen top 10, scored once on the held-out groups (DL-pooled PHYS/LIFEENV/SOC/MATHDEC)\n\npsp = partial Spearman given B5 (+ onset-year dummies); binary outcomes: dAUC over B5 with frozen DEV coefficients. `sign` = frozen DEV sign; `agree` = units (4 groups + 2 cohort parts) with that sign; **bold** = confirmed (Holm p < 0.05 within the outcome family and pooled sign = frozen sign).\n\n\n**O1c**\n\n| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |\n|---|---|---|---|---|---|---|---|---|\n| **n_authors_early** | E | + | +0.161 | [+0.090, +0.230] | 0.70 | 0.000101 | 6/6 | +0.171 / +0.140 |\n| burst | E | + | +0.019 | [-0.052, +0.089] | 0.69 | 1 | 4/6 | +0.106 / -0.014 |\n| S_comp_n | S | - | -0.087 | [-0.200, +0.029] | 0.88 | 1 | 6/6 | -0.107 / -0.097 |\n| CONTACT_REACH | FR | + | +0.048 | [+0.013, +0.084] | 0.00 | 0.0666 | 6/6 | +0.056 / +0.018 |\n| author_growth | E | + | +0.035 | [-0.024, +0.094] | 0.61 | 1 | 5/6 | +0.003 / +0.026 |\n| growth_ind | E | + | -0.008 | [-0.042, +0.026] | 0.00 | 1 | 3/6 | +0.050 / +0.003 |\n| comm_transitions | A | - | +0.021 | [-0.038, +0.079] | 0.63 | 1 | 2/6 | +0.004 / +0.008 |\n| share | E | + | +0.013 | [-0.024, +0.050] | 0.01 | 1 | 3/6 | -0.017 / +0.007 |\n| fields_gained_per_yr | F | + | +0.002 | [-0.033, +0.036] | 0.00 | 1 | 4/6 | +0.004 / -0.020 |\n| new_edge_rate | A | + | -0.002 | [-0.042, +0.038] | 0.19 | 1 | 5/6 | +0.024 / +0.003 |\n\n**O2r_m50**\n\n| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |\n|---|---|---|---|---|---|---|---|---|\n| **M0_density_end** | FR | + | +0.375 | [+0.279, +0.462] | 0.74 | 3.92e-12 | 6/6 | +0.276 / +0.354 |\n| **D_vol_end** | FR | + | +0.307 | [+0.256, +0.356] | 0.10 | 3.69e-28 | 6/6 | +0.294 / +0.318 |\n| **CONTACT_REACH** | FR | + | +0.211 | [+0.161, +0.261] | 0.00 | 9.3e-15 | 6/6 | +0.213 / +0.227 |\n| **n_comm_W3** | A | + | +0.167 | [+0.063, +0.267] | 0.78 | 0.0088 | 6/6 | +0.222 / +0.096 |\n| RS | G | - | -0.072 | [-0.153, +0.010] | 0.44 | 0.156 | 5/6 | -0.175 / -0.128 |\n| G_btw (prev. scored) | G | + | +0.056 | [-0.006, +0.118] | 0.33 | 0.156 | 6/6 | +0.062 / +0.033 |\n| log_offhome_volume | F | - | -0.089 | [-0.171, -0.007] | 0.63 | 0.102 | 5/6 | -0.155 / -0.125 |\n| **RETENTION_RATIO_early** | FR | - | -0.114 | [-0.160, -0.067] | 0.00 | 1.32e-05 | 6/6 | -0.187 / -0.105 |\n| **NOV** | A | + | +0.151 | [+0.044, +0.255] | 0.75 | 0.023 | 6/6 | +0.114 / +0.038 |\n| **ego_density_W3** | A | - | -0.102 | [-0.151, -0.053] | 0.00 | 0.000288 | 6/6 | -0.095 / -0.041 |\n\n**O2r_resid**\n\n| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |\n|---|---|---|---|---|---|---|---|---|\n| **M0_density_end** | FR | + | +0.377 | [+0.280, +0.466] | 0.75 | 7.67e-12 | 6/6 | +0.274 / +0.358 |\n| **D_vol_end** | FR | + | +0.307 | [+0.257, +0.356] | 0.10 | 1.14e-28 | 6/6 | +0.295 / +0.321 |\n| **CONTACT_REACH** | FR | + | +0.210 | [+0.159, +0.260] | 0.00 | 1.71e-14 | 6/6 | +0.203 / +0.222 |\n| **n_comm_W3** | A | + | +0.164 | [+0.058, +0.266] | 0.79 | 0.0124 | 6/6 | +0.219 / +0.092 |\n| RS | G | - | -0.073 | [-0.151, +0.005] | 0.41 | 0.136 | 5/6 | -0.179 / -0.130 |\n| **log_offhome_volume** | F | - | -0.100 | [-0.171, -0.028] | 0.53 | 0.027 | 6/6 | -0.182 / -0.134 |\n| G_btw (prev. scored) | G | + | +0.055 | [-0.008, +0.118] | 0.33 | 0.136 | 5/6 | +0.059 / +0.037 |\n| **RETENTION_RATIO_early** | FR | - | -0.120 | [-0.166, -0.073] | 0.00 | 3.98e-06 | 6/6 | -0.191 / -0.107 |\n| **NOV** | A | + | +0.152 | [+0.042, +0.258] | 0.76 | 0.027 | 6/6 | +0.110 / +0.042 |\n| **ego_density_W3** | A | - | -0.097 | [-0.146, -0.048] | 0.00 | 0.000654 | 6/6 | -0.092 / -0.037 |\n\n**O4**\n\n| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |\n|---|---|---|---|---|---|---|---|---|\n| G_deg | G | - | -0.021 | [-0.069, +0.028] | 0.41 | 1 | 5/6 | -0.093 / -0.058 |\n| log_offhome_volume | F | - | -0.002 | [-0.069, +0.066] | 0.66 | 1 | 3/6 | -0.080 / +0.014 |\n| **REL_home** | G | - | -0.114 | [-0.180, -0.047] | 0.69 | 0.00922 | 6/6 | -0.013 / -0.072 |\n| burst | E | - | +0.014 | [-0.043, +0.072] | 0.55 | 1 | 3/6 | -0.103 / +0.005 |\n| G_A (prev. scored) | G | - | -0.010 | [-0.055, +0.036] | 0.33 | 1 | 4/6 | -0.059 / -0.049 |\n| **author_growth** | E | + | +0.065 | [+0.024, +0.106] | 0.21 | 0.0182 | 5/6 | +0.049 / +0.080 |\n| G_phimin | G | + | +0.064 | [-0.080, +0.206] | 0.93 | 1 | 5/6 | +0.057 / +0.048 |\n| FRONTIER_POTENTIAL | FR | - | -0.017 | [-0.063, +0.030] | 0.39 | 1 | 5/6 | -0.074 / -0.047 |\n| RETENTION_RATIO_early | FR | - | -0.026 | [-0.060, +0.009] | 0.00 | 1 | 5/6 | -0.075 / -0.024 |\n| new_edge_rate | A | - | +0.003 | [-0.032, +0.037] | 0.00 | 1 | 3/6 | -0.058 / +0.000 |\n\n**O1b**\n\n| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |\n|---|---|---|---|---|---|---|---|---|\n| **n_authors_early** | E | + | +0.029 | [+0.015, +0.044] | 0.00 | 0.000789 | 4/6 | -0.002 / -0.006 |\n| G_phimin | G | + | +0.001 | [-0.011, +0.013] | 0.00 | 1 | 3/6 | +0.011 / -0.007 |\n| rao_stirling | F | + | -0.002 | [-0.022, +0.017] | 0.32 | 1 | 2/6 | +0.014 / -0.034 |\n| G (prev. scored) | G | - | +0.000 | [-0.003, +0.003] | 0.00 | 1 | 1/6 | +0.000 / +0.001 |\n| kcore_end | A | + | +0.010 | [-0.004, +0.023] | 0.00 | 1 | 5/6 | +0.011 / +0.019 |\n| S_comp_n | S | + | +0.028 | [-0.003, +0.058] | 0.77 | 0.697 | 5/6 | +0.005 / -0.015 |\n| M0_density_end | FR | + | +0.012 | [-0.004, +0.027] | 0.00 | 1 | 4/6 | +0.007 / -0.006 |\n| REL_home | G | + | -0.002 | [-0.015, +0.010] | 0.18 | 1 | 2/6 | +0.009 / -0.022 |\n| CONTACT_REACH | FR | + | +0.008 | [-0.006, +0.023] | 0.00 | 1 | 5/6 | +0.008 / +0.001 |\n| G_btw (prev. scored) | G | - | +0.001 | [-0.005, +0.007] | 0.00 | 1 | 3/6 | +0.001 / -0.005 |\n\n**O3**\n\n| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |\n|---|---|---|---|---|---|---|---|---|\n| **n_authors_early** | E | + | +0.089 | [+0.031, +0.148] | 0.00 | 0.0286 | 4/5 | +0.019 / -0.021 |\n| S_comp_n | S | + | +0.068 | [+0.001, +0.134] | 0.10 | 0.406 | 4/5 | +0.039 / -0.029 |\n| rao_stirling | F | + | +0.066 | [-0.002, +0.134] | 0.22 | 0.446 | 3/5 | +0.040 / -0.036 |\n| G_deg | G | + | +0.036 | [-0.007, +0.079] | 0.00 | 0.586 | 4/5 | +0.046 / -0.023 |\n| REL_home | G | + | +0.001 | [-0.056, +0.059] | 0.32 | 1 | 2/5 | +0.034 / -0.008 |\n| G_btw (prev. scored) | G | + | +0.040 | [-0.024, +0.104] | 0.48 | 0.891 | 3/5 | +0.064 / -0.009 |\n| fields_gained_per_yr | F | + | +0.010 | [-0.042, +0.061] | 0.00 | 1 | 1/5 | -0.015 / -0.027 |\n| M0_density_end | FR | + | +0.038 | [-0.011, +0.086] | 0.00 | 0.655 | 4/5 | +0.023 / +0.001 |\n| G_A (prev. scored) | G | + | +0.053 | [-0.058, +0.165] | 0.79 | 1 | 4/5 | +0.036 / +0.013 |\n| CONTACT_REACH | FR | + | +0.049 | [-0.003, +0.101] | 0.00 | 0.452 | 5/5 | +0.016 / +0.012 |\n\n**O5**\n\n| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |\n|---|---|---|---|---|---|---|---|---|\n| G_phimin | G | + | -0.004 | [-0.012, +0.004] | 0.00 | 1 | 1/6 | +0.014 / -0.004 |\n| REL_home | G | + | -0.008 | [-0.024, +0.007] | 0.58 | 1 | 3/6 | +0.005 / +0.000 |\n| S_comp_n | S | + | +0.003 | [-0.002, +0.009] | 0.00 | 1 | 6/6 | +0.008 / +0.027 |\n| burst | E | - | +0.000 | [-0.003, +0.003] | 0.00 | 1 | 1/6 | +0.022 / +0.012 |\n| n_authors_early | E | + | +0.003 | [-0.001, +0.008] | 0.00 | 1 | 5/6 | +0.005 / +0.020 |\n| G (prev. scored) | G | - | -0.000 | [-0.002, +0.001] | 0.00 | 1 | 3/6 | +0.001 / -0.001 |\n| FRONTIER_POTENTIAL | FR | + | +0.001 | [-0.003, +0.006] | 0.00 | 1 | 5/6 | +0.006 / +0.018 |\n| share | E | - | -0.002 | [-0.004, +0.001] | 0.00 | 1 | 6/6 | -0.011 / -0.008 |\n| G_btw (prev. scored) | G | - | +0.000 | [-0.002, +0.003] | 0.00 | 1 | 1/6 | +0.002 / +0.007 |\n| deg_W1 | A | + | +0.002 | [-0.002, +0.007] | 0.00 | 1 | 5/6 | +0.002 / -0.007 |\n\n**O5_WW**\n\n| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |\n|---|---|---|---|---|---|---|---|---|\n| G_phimin | G | + | -0.001 | [-0.006, +0.005] | 0.05 | 1 | 2/6 | -0.007 / -0.004 |\n| G_deg | G | + | +0.001 | [-0.006, +0.008] | 0.18 | 1 | 4/6 | -0.008 / +0.003 |\n| REL_home | G | + | -0.005 | [-0.016, +0.006] | 0.54 | 1 | 1/6 | -0.010 / -0.007 |\n| S_comp | S | + | -0.005 | [-0.011, +0.002] | 0.00 | 1 | 1/6 | -0.009 / +0.016 |\n| G_A (prev. scored) | G | - | +0.001 | [-0.001, +0.004] | 0.00 | 1 | 4/6 | -0.007 / -0.003 |\n| FRONTIER_POTENTIAL | FR | + | +0.003 | [-0.002, +0.008] | 0.03 | 1 | 4/6 | -0.004 / +0.010 |\n| G_btw (prev. scored) | G | - | +0.001 | [-0.002, +0.004] | 0.00 | 1 | 3/6 | -0.002 / -0.004 |\n| btw_end | A | + | +0.001 | [-0.003, +0.004] | 0.00 | 1 | 4/6 | +0.011 / -0.002 |\n| ego_density_W3 | A | + | +0.000 | [-0.004, +0.005] | 0.00 | 1 | 3/6 | +0.005 / -0.008 |\n| rao_stirling | F | + | -0.003 | [-0.013, +0.008] | 0.63 | 1 | 1/6 | -0.006 / -0.013 |\n\n### Learned models vs B5 vs B5 + best single (held-out groups pooled)\n\nSpearman(pred, y) for continuous outcomes, AUC for binary; [95% CI of the paired difference vs B5].\n\n| outcome | n | B5 | B5 + best single | ElasticNet / L1-logit (all) | EBM |\n|---|---|---|---|---|---|\n| O1c | 3372 | 0.312 | 0.305 [-0.016, +0.004] | 0.303 [-0.019, -0.001] | 0.313 [-0.022, +0.026] |\n| O2r_m50 | 1833 | 0.706 | 0.739 [+0.022, +0.045] | 0.765 [+0.046, +0.073] | 0.757 [+0.037, +0.067] |\n| O2r_resid | 1833 | 0.704 | 0.738 [+0.023, +0.047] | 0.763 [+0.047, +0.071] | 0.756 [+0.038, +0.066] |\n| O4 | 3372 | 0.015 | 0.028 [-0.009, +0.036] | constant (all coef. 0) | 0.188 [+0.129, +0.219] |\n| O1b | 3372 | 0.507 | 0.518 [-0.003, +0.029] | 0.524 [-0.000, +0.039] | 0.526 [-0.001, +0.042] |\n| O3 | 3372 | 0.506 | 0.576 [+0.020, +0.128] | 0.599 [+0.028, +0.163] | 0.599 [+0.033, +0.161] |\n| O5 | 1417 | 0.746 | 0.742 [-0.013, +0.003] | 0.747 [-0.009, +0.009] | 0.726 [-0.038, -0.004] |\n| O5_WW | 1671 | 0.747 | 0.746 [-0.007, +0.005] | 0.751 [-0.003, +0.010] | 0.719 [-0.046, -0.011] |\n\n### Pre-registered predictions (frozen before the unseal)\n\n| id | prediction | verdict |\n|---|---|---|\n| P1 | entropy, D_rare, D_ratio, participation, NOV_res: raw Spearman with O2r_m50 > 0 (CI > 0) in >= 3 of 4 held-out groups; AND D_rare, D_ratio, participation, NOV_res: pooled psp|B5 CI upper bound < 0.10 | **FAILS** |\n| P2 | edge_persistence: pooled raw rho and pooled psp with O2r_m50 both < 0 | **HOLDS** |\n| P3 | deg_growth, str_growth, new_edge_rate FAIL held-out: pooled psp CI includes 0 OR sign flip in >= 2 of 4 groups | **FAILS** |\n| P4 | RETENTION_RATIO_early and FRONTIER_POTENTIAL: pooled psp > 0 with CI > 0 for O2r_resid AND O1c | **FAILS** |\n| P5 | CONTACT_REACH: pooled psp CI includes 0 (also reported given B5 minus reach) | **FAILS** |\n<!-- /TABLES -->\n**Question (RQ1).** Which temporal network indicators, measured only in a concept's first three years (t0..t0+2),\nanticipate its later emergence outcomes beyond simple volume/growth/breadth (B5), and do they generalise across\nscientific domains? About 53 indicators in 7 families were ranked on DEV home groups only (CS, Engineering,\nBiochem/Genetics, Medicine; 4,771 concepts), the top 10 per outcome were frozen and hash-sealed, and the frozen\nspec was scored **once** on four held-out home groups (PHYS 742, LIFEENV 1,113, SOC 1,352, MATHDEC 165) and on a\n2010-14 onset cohort split into DEV-home (2,484) and other-home (1,872) parts.\n\n## Headline results\n\n1. **Breadth (O2r_m50 / O2r_resid, rarefied venue-field richness at t0+6..t0+8) is predictable beyond B5, and the\n   signal travels.** 7 (O2r_m50) and 8 (O2r_resid) of the frozen top 10 are confirmed (Holm p < 0.05; every\n   confirmed indicator has the frozen sign in 6/6 units). The strongest are field-state indicators: `M0_density_end` (Hidalgo density of the fields not yet\n   entered by t0+2) psp **+0.377** [+0.280, +0.466], `D_vol_end` (# off-home fields entered by t0+2) **+0.307**\n   [+0.257, +0.356], `CONTACT_REACH` **+0.210** [+0.159, +0.260]. Ego-network rows also transfer: `n_comm_W3`\n   +0.164, `NOV` +0.152 (positive), `ego_density_W3` -0.097 and `RETENTION_RATIO_early` -0.120 (negative). Both\n   cohort parts agree in sign.\n   **Caveat:** `M0_density_end` and `D_vol_end` use cumulative field history 1995..t0+2 (EXP6 D3 definition), so\n   part of their signal is a **pre-onset field footprint** (the highest-scoring held-out concepts are generic terms\n   such as \"Coefficient of variation\" and \"Exponential growth\"). `CONTACT_REACH`, `n_comm_W3`, `NOV` and\n   `ego_density_W3` use only t0..t0+2.\n2. **Sustained uptake (O1c) is essentially a size/author signal.** Only `n_authors_early` is confirmed (psp +0.161\n   [+0.090, +0.230], 6/6 units); `CONTACT_REACH` +0.048 [+0.013, +0.084] misses Holm (p = 0.067). No ego-network\n   indicator transfers for O1c; learned models do not beat B5 (Spearman 0.303-0.313 vs 0.312). The same author-base\n   indicator is the only confirmed one for the binary retention/transience outcomes (O1b dAUC +0.029, O3 +0.089).\n3. **Citation growth (O4, field- and year-normalised)**: `REL_home` (-0.114) and `author_growth` (+0.065) are\n   confirmed. The linear model on all indicators shrinks to a constant, while the EBM reaches held-out Spearman\n   0.188 vs 0.015 for B5 (paired CI of the gain +0.13..+0.22): O4 signal is non-linear.\n4. **External recognition (O5 all sources, O5_WW Wikipedia/Wikidata) is NOT anticipated by any indicator.** No DEV\n   CI excluded 0, the frozen (filled) top 10s are all null held-out, and no model beats B5 + onset year\n   (AUC 0.746-0.751). O5 is dominated by Wikipedia page creation.\n5. **Learned vs single.** For breadth, ElasticNet on all indicators beats B5 held-out (Spearman 0.765 vs 0.706,\n   +0.059 [+0.046, +0.073]) and B5 + best single (0.739). The EBM is close (0.757). For O3 (transience) the L1-logit\n   gains +0.093 AUC [+0.028, +0.163] over a B5 model that is at chance (0.506).\n6. **Pre-registered predictions** (from iteration-1 P78 portability): P2 (edge_persistence negative for breadth)\n   **HOLDS**; P1, P3, P4, P5 **FAIL**. P3 fails because `new_edge_rate` transfers (+0.118) while\n   degree/strength growth are null as predicted; P5 fails because `CONTACT_REACH` adds signal even given\n   B5-minus-reach (+0.223 for O2r_resid); P4 fails because `RETENTION_RATIO_early` is **negative** (-0.120).\n7. **Robustness.** Breadth results hold when excluding EXP6-overlap concepts, adding label-coverage covariates, using\n   O2r_m30, or using EXP5's own O2r_resid definition (O2r_resid_N); excluding intersection-born concepts halves\n   `CONTACT_REACH` (+0.111) but leaves it positive.\n\n**Disclosure (second use).** EXP5 already unsealed O1/O3/O2r for these held-out concepts (its H1/H3). No selection\nhere touched held-out rows; G, G_A and G_btw were scored once before on O2r_resid and are flagged \"prev. scored\".\n\n**Audits.** T0 unit tests 7/7 pass; T0-8: the ported EXP3 ego code reproduces EXP3 P78 features exactly (max\n|diff| ~1e-15); T1: Pass A per-file counts equal EXP5's exactly; T2: A1 identical yearly grounded counts for all\n12,499 concepts, A2 background Spearman 1.000 vs EXP3; T3: 99.8% of citation links have citing year >= cited year;\nT5: DEV placebo 3.25/53 indicators with CI excluding 0 (<= 6), 29 indicator clusters at |rho| < 0.7, B5 LOGO\nSpearman with O2r_m50 0.755; T6 pre-unseal checklist passed (commit 64ed779); T7 (`audit.py`) independent psp\nequal to 4e-16, dAUC equal to sklearn to 3e-16, shuffled-outcome pooled |psp| 0.021, planted psp 0.10 recovered\n(0.089, CI > 0); `rederive.py` re-derives all 40 continuous pooled headline estimates with analytic SEs (100% same\nsignificance call, max |diff| 0.013) and all learned-model metrics (diff 1e-16); shuffled controls all null.\nPower: pooled MDE (2.8 SE) = 0.049; MATHDEC alone 0.23 (uninformative on its own).\n\n\n## Layout\n\n| path | content |\n|---|---|\n| `method.py` | end-to-end orchestrator (`--from STEP`, `--only STEP`); steps below |\n| `passA.py` | zero-credit OpenAlex S3 pass: EXP5 matcher + TAG grounding unchanged; early work/topic/author ids, topic background, reference sample |\n| `passB.py` | citations received by early works and by the reference sample (O4) |\n| `build_features.py` | the indicator matrix (families E, F, G, FR, A, S + B5) over t0..t0+2 |\n| `outcomes.py` | one outcome table (O1c, O1b, O2r_m50/m30, O2r_resid, O3, O4, O5, O5_WW) and the outcome seal |\n| `dev_select.py` | DEV-only ranking, frozen top 10s, learned models, power, freeze + seal |\n| `heldout.py` | the single unseal; frozen scoring, DL pooling, Holm, learned vs single, portability table, P1-P5, sensitivities |\n| `audit.py` | T7 independent re-derivation (own ranks/OLS, sklearn AUC, shuffled and planted controls) |\n| `make_outputs.py` | `results/rq1_heldout.json`, figures, case exemplars, `method_out.json` |\n| `lib/common.py` | paths, constants, frame loader (EXP5 `frame_concepts.csv`), helpers |\n| `lib/common5.py`, `lib/matcher.py`, `lib/rangefile.py` | EXP5 analyser / Aho-Corasick matcher / HTTP-range parquet reader (copied; mkdir side effect removed) |\n| `lib/ego.py`, `lib/ego_ctx.py` | EXP3 `features.concept_core` ported (1-year windows) + context (EXP3 Leiden backbones, Pass A background) |\n| `lib/ego_exp3_orig.py`, `lib/common3.py` | the unmodified EXP3 sources, for reference |\n| `lib/rq1stats.py` | partial Spearman + refit bootstrap, L2-logistic LOGO dAUC + bootstrap, DL pooling, Holm |\n| `lib/design.py` | frozen imputation / missing flags / standardisation for the learned models |\n| `lib/indicators.py` | indicator dictionary, families, outcomes, pre-registered predictions |\n| `lib/seal.py` | freeze / unseal gate (refuses without a matching spec hash, refuses a second unseal) |\n| `lib/h2.py`, `lib/stats_core.py` | EXP6 sources (D3 state machine, DL pooling), copied for provenance |\n| `tests/test_units.py`, `tests/t0_8_ego_port.py`, `tests/t1_check.py`, `tests/checks.py` | T0, T0-8, T1, T2/T3 |\n| `inputs/` | frozen lexicon (sha256 checked), source->field map, EXP3 backbones + topic metadata, EXP6 field backbone |\n| `data/frame_matches_early/part_*.parquet` | **kept**: grounded frame hits t0-3..t0+2 with work, topic and author ids |\n| `data/cites_early.parquet` | **kept**: citations to early works and the reference sample by citing year |\n| `data/ref_sample.parquet`, `data/bg_topics.npz`, `data/counts_check.parquet` | reference sample, topic background, reproduction counts |\n| `data/features_basic.parquet`, `data/ego_features.parquet` | families E/F/G/FR/S and A |\n| `data/outcomes_dev.parquet`, `data/outcomes_sealed.parquet`, `data/outcomes.parquet`, `data/analysis_table.parquet` | outcome tables (sealed file hashed in `logs/outcome_seal.log`) |\n| `results/` | every result table / JSON (see below) |\n| `figures/` | PNG + PDF figures |\n| `models/` | frozen learned models (joblib) |\n| `logs/seal.log`, `logs/unsealed.json` | seal evidence |\n\n\n| results file | content |\n|---|---|\n| `results/rq1_heldout.json` | **headline deliverable**: held-out summary per outcome, learned vs single, precision@top-decile, P1-P5 verdicts, sensitivities, audits, base rates, exemplars |\n| `results/heldout_summary.json`, `results/heldout_unit_results.csv` | pooled and per-unit held-out estimates (frozen top 10 + union) |", "numLines": 250, "startLine": 1, "totalLines": 318}}
```

### [17] TOOL CALL — Grep · 2026-09-29 02:07:29 UTC

```
Pattern: "2014|2003|>= ?20|early_vol|t0_max|T0_|MODEL|model *=|def "
```

### [18] TOOL RESULT — Grep · 2026-09-29 02:07:29 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "9:Rules (art_33 definitions): t0 = first year 2000..2014 with >= 20 grounded works (all venues); keep\n10:2003 <= t0 <= 2014 and early volume (t0..t0+2) >= 30; precision_c >= 0.8; home = fields with >= 40% of the\n33:def n_concepts() -> int:\n37:def year_totals() -> tuple[np.ndarray, np.ndarray]:\n43:def rarefied_richness(counts, m: int) -> float:\n59:def rarefied_richness_frac(counts, m: int) -> float:\n64:def shannon(v) -> float:\n73:def home_rule(V: np.ndarray, t0: int, n_first: int = HOME_N) -> dict:\n111:def split_of(group: str, t0: int) -> str:\n112:    if 2010 <= t0 <= 2014:\n118:def episode_rows(ci: int, V: np.ndarray, t0: int, home: list[int]) -> list[dict]:\n136:def episode_outcomes(V: np.ndarray, t0: int, field: int, share_early: float) -> dict:\n146:def concept_outcomes(N: np.ndarray, V: np.ndarray, G: np.ndarray, t0: int) -> dict:\n162:def cmd_match() -> None:\n166:    logger.info(f\"match onset candidates: {len(ot)} (t0 2003-2014, early >= 30)\")\n169:def cmd_grounded() -> None:\n176:def p78_names() -> set[str]:\n187:def build(early_min: float = EARLY_MIN, allow_weak: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:\n230:                      \"early_volume\": float(early_all), \"in_P78\": int(nm.lower() in p78)})\n240:def cmd_build() -> None:\n248:        add_deviation(\"frame_relaxation\", f\"targets not met at early>=30; relaxed to early volume >= 20: {ladder}\")", "numLines": 21, "totalLines": 21}
```

### [19] TOOL CALL — Grep · 2026-09-29 02:07:29 UTC

```
Pattern: "model|MODEL|prompt|cache|def |cost"
```

### [20] TOOL RESULT — Grep · 2026-09-29 02:07:29 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "3:* every call's usage.cost is appended to llm_cost_log.csv and summed; hard stop at COST_CAP (USD);\n5:* responses are cached on disk (scan/llm_cache/<sha1>.json, keyed by model+messages, no secrets).\"\"\"\n21:LEDGER = ROOT / \"llm_cost_log.csv\"\n22:CACHE = SCAN / \"llm_cache\"\n31:    def __init__(self, concurrency: int = 16, cap: float = COST_CAP):\n43:    def sem(self) -> asyncio.Semaphore:\n51:    def _ledger_total() -> float:\n55:            return sum(float(r[\"cost\"] or 0) for r in csv.DictReader(f))\n57:    def _log(self, model: str, tag: str, usage: dict) -> None:\n62:                w.writerow([\"time\", \"model\", \"tag\", \"prompt_tokens\", \"completion_tokens\", \"cost\"])\n63:            w.writerow([time.strftime(\"%H:%M:%S\"), model, tag, usage.get(\"prompt_tokens\"),\n64:                        usage.get(\"completion_tokens\"), usage.get(\"cost\", 0)])\n66:    async def chat(self, session: aiohttp.ClientSession, model: str, messages: list[dict], tag: str,\n68:        ck = CACHE / (hashlib.sha1(json.dumps([model, messages, temperature]).encode()).hexdigest() + \".json\")\n77:            body = {\"model\": model, \"messages\": messages, \"max_tokens\": max_tokens, \"temperature\": temperature,\n93:                        self.spent += float(usage.get(\"cost\") or 0)\n95:                        self._log(model, tag, usage)\n106:def parse_json(txt: str | None):\n128:def batch_prompt(items: list[dict]) -> list[dict]:", "numLines": 19, "totalLines": 19}
```

### [21] TOOL CALL — Grep · 2026-09-29 02:07:35 UTC

```
Pattern: "gate|precision_c|flash|nano|sample|n_titles|def "
```

### [22] TOOL RESULT — Grep · 2026-09-29 02:07:35 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "5:            labeller 1 (gemini-2.5-flash-lite) labels all 400, labeller 2 (gpt-4.1-nano, other family) 150;\n6:            Cohen's kappa; disagreements adjudicated by gemini-2.5-flash if kappa < 0.6; writes\n11:  precision per-concept LLM precision gate for onset candidates (10 grounded titles, +10 if 7-8/10 positive);\n31:M1 = \"google/gemini-2.5-flash-lite\"\n32:M2 = \"openai/gpt-4.1-nano\"\n33:M3 = \"google/gemini-2.5-flash\"\n40:def domain_of_code(code: int) -> str:\n44:def load_lex() -> pd.DataFrame:\n51:async def label_items(llm: LLM, model: str, items: list[dict], tag: str, bs: int = 10) -> dict:\n56:        async def one(b):\n75:def kappa(a: np.ndarray, b: np.ndarray) -> float:\n82:def cmd_bench() -> None:\n98:        pick.append(g.sample(min(per, len(g)), random_state=rng.randrange(10**6)))\n103:        pick = pd.concat([pick, rest.sample(400 - len(pick), random_state=SEED)])\n104:    pick = pick.sample(frac=1, random_state=SEED).head(400).reset_index(drop=True)\n112:    test_c = set(rng2.sample(concepts, k=round(len(concepts) * 0.25)))\n117:    dbl = pick.sample(150, random_state=SEED).id.tolist()\n132:    def gold(r):\n146:    hand = pick.sample(60, random_state=SEED + 7)[[\"id\", \"name\", \"description\", \"title\"]]\n162:def embed(texts: list[str]) -> np.ndarray:\n170:def cap_flag(name: str, title: str) -> int:\n176:def features(df: pd.DataFrame) -> pd.DataFrame:\n187:def pr(y: np.ndarray, p: np.ndarray) -> dict:\n195:def cmd_filter() -> None:\n232:    # apply filter to untagged rows (tagstate 3): pass rate per (concept, mtype) from the 20% hash sample\n233:    us = pd.read_parquet(SCAN / \"untagged_sample_titles.parquet\")\n234:    passrate = pd.DataFrame(columns=[\"ci\", \"mt\", \"passrate\", \"n_sample\"])\n243:        passrate = us.assign(ok=us.p >= 0.5).groupby([\"ci\", \"mt\"]).agg(passrate=(\"ok\", \"mean\"), n_sample=(\"ok\", \"size\")).reset_index()\n249:                \"frozen_grounding_rule\": rule, \"handcheck\": hand, \"n_untagged_sample_rows\": int(len(us)),\n255:# ----------------------------------------------------------------------------- per-concept precision gate\n256:def grounded_mask(df: pd.DataFrame, rule: str) -> np.ndarray:\n259:    return (df.tagstate == 1).to_numpy() | (df.tagstate == 3).to_numpy()  # ts3 rows are gated by the filter\n262:def cmd_precision() -> None:\n274:    cand = cand.sample(frac=1, random_state=SEED).reset_index(drop=True)\n275:    logger.info(f\"precision gate: {len(cand)} candidates after the home-rule pre-filter\")\n287:    def items(df):\n291:    async def run(df, tag):\n296:            async def one(its):\n322:    out[\"precision_c\"] = out.n_pos / out.n_labelled_prec\n324:    # fallback: concepts without an LLM label (budget stop) are gated by the sense filter's mean prediction\n325:    miss = out.precision_c.isna()\n338:            out.loc[miss, \"precision_c\"] = out.loc[miss, \"ci\"].map(fp)\n339:            out.loc[miss & out.precision_c.notna(), \"precision_source\"] = \"filter\"\n340:        add_deviation(\"precision_gate_fallback\", f\"{int(miss.sum())} concepts had no LLM precision label; gated by \"\n344:    out[\"pass_gate\"] = out.precision_c >= 0.8\n346:    logger.info(f\"precision gate: {len(out)} candidates, pass={int(out.pass_gate.sum())}, \"", "numLines": 46, "totalLines": 46}
```

### [23] TOOL CALL — Grep · 2026-09-29 02:07:35 UTC

```
Pattern: "^def |^    def |window|W1|W3|slice|betweenness"
```

### [24] TOOL RESULT — Grep · 2026-09-29 02:07:35 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "4:  * windows are pluggable. RQ1 uses PRE = t0-3..t0-1, W1 = {t0}, W2 = {t0+1}, W3 = {t0+2}: the EXP3 W3 (t0+3..t0+4)\n5:    would leak past the t0..t0+2 feature window. new_edge_rate divides by the window length in years (3, not 5).\n7:  * betweenness uses a path-length cutoff (default 4) on the kNN backbone; N_NULL defaults to 200.\n9:  * new: comm_entropy = Shannon entropy of the W3 neighbours' backbone-community weights.\n30:def slice_of(y: int) -> int:\n37:def rq1_windows(t0: int) -> dict[str, list[int]]:\n38:    return {\"PRE\": [t0 - 3, t0 - 2, t0 - 1], \"W1\": [t0], \"W2\": [t0 + 1], \"W3\": [t0 + 2]}\n41:def exp3_windows(t0: int) -> dict[str, list[int]]:\n42:    return {\"PRE\": [t0 - 3, t0 - 2, t0 - 1], \"W1\": [t0, t0 + 1], \"W2\": [t0 + 2], \"W3\": [t0 + 3, t0 + 4]}\n45:def lgC(n: float, k: float) -> float:\n50:def set_context(ctx: dict) -> None:\n51:    \"\"\"ctx: nt, years (list), bg [len(years), nt], Gt {year: n}, comm/comm_q/deg/knn/full_edges per slice, subfield,\n59:def knn_graph(s: int) -> ig.Graph:\n66:def bg_window(years: list[int]) -> tuple[np.ndarray, float]:\n71:def window_counts(works, years) -> tuple[np.ndarray, int]:\n83:def pmi(nck, nc, nbg, N):\n90:def neighbours(nck, nc, nbg, N, excl, min_n: int = 2):\n96:def topS(nck, p, nb, top: int = TOPN_F):\n104:def self_topics(name: str, aliases: list[str], n_early, nc_early) -> np.ndarray:\n116:def distinct_null(pool_idx, w, M, labels, rng, n):\n133:def f_null(p_mix, pool, T1, T3, nc1, nc3, nbg1, N1, nbg3, N3, rng, n):\n138:    def S(T, nc, nbg, N):\n153:def _centrality(idx: np.ndarray, s: int, cutoff: int | None) -> tuple[float, int, float]:\n161:    b = g.betweenness(vertices=[v], directed=False, cutoff=cutoff)[0]\n165:def concept_core(name: str, aliases: list[str], t0: int, works, n_null: int, seed: int, windows=rq1_windows,\n169:    win = windows(t0)\n170:    early_years = sorted(set(win[\"W1\"] + win[\"W2\"] + win[\"W3\"]))\n171:    n_early, nc_early = window_counts(works, early_years)\n175:        cnt[w], nc[w] = window_counts(works, ys)\n176:        bgw[w], NW[w] = bg_window(ys)\n177:    nbg_early, _ = bg_window(early_years)\n178:    for w in (\"W1\", \"W2\", \"W3\"):\n181:    new = (NB[\"W1\"] | NB[\"W2\"] | NB[\"W3\"]) & ~pre_set\n186:        cy, _ = window_counts(works, [y])\n191:    s_mid = slice_of(early_years[len(early_years) // 2])\n192:    r: dict = {\"M\": M, \"n_self_topics\": int(SELF.sum()), \"nc_PRE\": nc[\"PRE\"], \"nc_W1\": nc[\"W1\"], \"nc_W2\": nc[\"W2\"],\n193:               \"nc_W3\": nc[\"W3\"]}\n195:    def dz(labels_by_slice, pool_idx, new_list):\n198:        labs = [labels_by_slice[slice_of(first_year.get(k, t0))][k] for k in new_list]\n200:        nl = distinct_null(pool_idx, nbg_early, len(new_list), labels_by_slice[s_mid], rng, n_null)\n205:    S1, k1 = topS(cnt[\"W1\"], P[\"W1\"], NB[\"W1\"])\n206:    S3, k3 = topS(cnt[\"W3\"], P[\"W3\"], NB[\"W3\"])\n208:    pooled = cnt[\"W1\"] + cnt[\"W2\"] + cnt[\"W3\"]\n210:    T1 = int(cnt[\"W1\"][~SELF].sum())\n211:    T3 = int(cnt[\"W3\"][~SELF].sum())\n212:    ng = f_null(pooled, mixpool, T1, T3, nc[\"W1\"], nc[\"W3\"], bgw[\"W1\"], NW[\"W1\"], bgw[\"W3\"], NW[\"W3\"], rng,\n230:    s0 = slice_of(t0)\n232:    w1 = cnt[\"W1\"]\n239:            r[\"NOV\"] = float(np.mean([C[\"comm\"][slice_of(first_year.get(k, t0))][k] != C0 for k in new_idx]))\n247:    n1, n3 = NB[\"W1\"].sum(), NB[\"W3\"].sum()\n248:    r[\"deg_W1\"], r[\"deg_W3\"] = int(n1), int(n3)\n250:    sp1 = np.nansum(P[\"W1\"][NB[\"W1\"]])\n251:    sp3 = np.nansum(P[\"W3\"][NB[\"W3\"]])\n256:    def jac(a, b):\n261:        r[\"edge_persistence\"] = float(np.nanmean([jac(NB[\"W1\"], NB[\"W2\"]), jac(NB[\"W2\"], NB[\"W3\"])]))\n262:    r[\"turnover\"] = float((NB[\"W1\"] & ~NB[\"W3\"]).sum() / n1) if n1 else float(\"nan\")\n263:    s4 = slice_of(win[\"W3\"][-1])\n266:        for k in np.nonzero(NB[\"W3\"])[0]:\n267:            ws[C[\"comm\"][s4][k]] += cnt[\"W3\"][k]\n271:        r[\"n_comm_W3\"] = len(ws)", "numLines": 60, "totalLines": 73, "appliedLimit": 60}
```

### [25] ASSISTANT · 2026-09-29 02:07:45 UTC

```
Still reading the prior experiments' code (the ego-network features and how the frame was built) so the plan points at real files. Next I'll write the plan JSON.
```

### [26] TOOL CALL — Read · 2026-09-29 02:07:45 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego.py
```

### [27] TOOL RESULT — Read · 2026-09-29 02:07:45 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego.py", "content": "\"\"\"Co-occurrence ego-network indicators (family A), ported from art_yrradSC27HtQ features.concept_core.\n\nPort changes (all logged in results/deviations.json):\n  * windows are pluggable. RQ1 uses PRE = t0-3..t0-1, W1 = {t0}, W2 = {t0+1}, W3 = {t0+2}: the EXP3 W3 (t0+3..t0+4)\n    would leak past the t0..t0+2 feature window. new_edge_rate divides by the window length in years (3, not 5).\n  * the background comes from the context (Pass A BG/GT for RQ1; EXP3's ckpt for the port-validation test T0-8).\n  * betweenness uses a path-length cutoff (default 4) on the kNN backbone; N_NULL defaults to 200.\n  * dropped near-duplicate variants: D_lag, D_q, D_withself, F_bg; the per-field block is not needed.\n  * new: comm_entropy = Shannon entropy of the W3 neighbours' backbone-community weights.\nEverything else (PMI neighbour rule, SELF rule, the frequency-matched null of D_z, the multinomial null of F_res,\nNOV_res, participation, persistence, density, k-core, constraint) is the EXP3 code.\"\"\"\nfrom __future__ import annotations\n\nimport math\nimport warnings\nfrom collections import Counter\n\nimport igraph as ig\nimport numpy as np\n\nSELF_DF_MAX = 100\nSELF_SHARE = 0.20\nTOPN_F = 20\nR_RARE = 10\nSLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]\n\nC: dict = {}\n\n\ndef slice_of(y: int) -> int:\n    for i, (a, b) in enumerate(SLICES):\n        if a <= y <= b:\n            return i\n    return 0 if y < SLICES[0][0] else len(SLICES) - 1\n\n\ndef rq1_windows(t0: int) -> dict[str, list[int]]:\n    return {\"PRE\": [t0 - 3, t0 - 2, t0 - 1], \"W1\": [t0], \"W2\": [t0 + 1], \"W3\": [t0 + 2]}\n\n\ndef exp3_windows(t0: int) -> dict[str, list[int]]:\n    return {\"PRE\": [t0 - 3, t0 - 2, t0 - 1], \"W1\": [t0, t0 + 1], \"W2\": [t0 + 2], \"W3\": [t0 + 3, t0 + 4]}\n\n\ndef lgC(n: float, k: float) -> float:\n    from scipy.special import gammaln\n    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)\n\n\ndef set_context(ctx: dict) -> None:\n    \"\"\"ctx: nt, years (list), bg [len(years), nt], Gt {year: n}, comm/comm_q/deg/knn/full_edges per slice, subfield,\n    names, ldf (topic lemma df), tlem (topic lemma sets), lemmas (callable).\"\"\"\n    C.clear()\n    C.update(ctx)\n    C[\"graphs\"] = {}\n    C[\"yidx\"] = {y: i for i, y in enumerate(ctx[\"years\"])}\n\n\ndef knn_graph(s: int) -> ig.Graph:\n    if s not in C[\"graphs\"]:", "numLines": 60, "startLine": 1, "totalLines": 311}}
```

### [28] TOOL CALL — Grep · 2026-09-29 02:07:45 UTC

```
Pattern: "year|bg_topics|YEARS|range\("
```

### [29] TOOL RESULT — Grep · 2026-09-29 02:07:45 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "41:    sl = [np.load(INPUTS / \"backbone\" / f\"slice{s}.npz\") for s in range(3)]\n51:    z = np.load(DATA / \"bg_topics.npz\")\n52:    years = z[\"years\"].tolist()\n53:    ctx.update(years=years, bg=z[\"BG\"], Gt=dict(zip(years, z[\"GT\"].tolist())))", "numLines": 4, "totalLines": 4}
```

### [30] TOOL CALL — Grep · 2026-09-29 02:07:45 UTC

```
Pattern: "YEAR|2022|2012|1995|bg|ref_sample|EARLY|early|def "
```

### [31] TOOL RESULT — Grep · 2026-09-29 02:07:45 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "10:  BG[year, topic]  base works per topic per year (1995-2022, 4,516 topics of EXP3 topic_ids.json); GT[year] = base\n13:  EARLY rows       grounded frame hits with t0-3 <= year <= t0+2: (ci, year, work_id, vfield, topic idx list,\n48:def _init() -> None:\n64:def _oa_int(arr, prefix_len: int = 22, null: str = \"https://openalex.org/X0\") -> np.ndarray:\n70:def _field_code(arr) -> np.ndarray:\n76:def _list_offsets(col) -> tuple[pa.Array, np.ndarray]:\n85:def process_file(fi: int, key: str, size: int) -> dict:\n165:    # early rows\n167:    early = (gy >= t0c - 3) & (gy <= t0c + 2)\n168:    e_row, e_ci = g_row[early], g_ci[early]\n185:           \"n_frame_hits\": int(len(h_row)), \"n_grounded\": int(len(g_row)), \"n_early\": int(len(e_row)),\n188:    edf.to_parquet(PASSA / f\"early_{fi:04d}.parquet\", index=False)\n197:def merge(logger) -> None:\n203:    keys, cnts, early, rs = [], [], [], []\n209:        early.append(pd.read_parquet(PASSA / f\"early_{fi:04d}.parquet\"))\n217:    np.savez_compressed(DATA / \"bg_topics.npz\", BG=BG, GT=GT, years=np.arange(Y0, Y1 + 1))\n218:    edf = pd.concat(early, ignore_index=True).sort_values([\"ci\", \"year\", \"work_id\"]).reset_index(drop=True)\n219:    write_parquet_parts(edf, DATA / \"frame_matches_early\")\n220:    pd.concat(rs, ignore_index=True).to_parquet(DATA / \"ref_sample.parquet\", index=False)\n223:                                       (\"n\", \"n_base\", \"n_win_titles\", \"n_frame_hits\", \"n_grounded\", \"n_early\",\n225:            \"early_rows\": int(len(edf))}\n230:def main() -> None:\n259:        def submit_next() -> None:\n287:                                f\"grounded={r['n_grounded']} early={r['n_early']}\")", "numLines": 24, "totalLines": 24}
```

### [32] TOOL CALL — ToolSearch · 2026-09-29 02:08:03 UTC

```
{'query': 'select:WebSearch,WebFetch', 'max_results': 2}
```

### [33] TOOL RESULT — ToolSearch · 2026-09-29 02:08:03 UTC

```
{"matches": ["WebSearch", "WebFetch"], "query": "select:WebSearch,WebFetch", "total_deferred_tools": 27}
```

### [34] TOOL CALL — WebSearch · 2026-09-29 02:08:07 UTC

```
OpenAlex legacy concepts deprecated still assigned to new works 2024 2025 Walden
```

### [35] TOOL CALL — WebSearch · 2026-09-29 02:08:07 UTC

```
Sun Abraham 2021 event study heterogeneous treatment effects staggered adoption interaction-weighted estimator
```

### [36] TOOL RESULT — WebSearch · 2026-09-29 02:08:13 UTC

```
{"query": "OpenAlex legacy concepts deprecated still assigned to new works 2024 2025 Walden", "results": [{"tool_use_id": "srvtoolu_01CzqdJ8mUXMnsUqQhY63qQX", "content": [{"title": "Concepts (deprecated)", "url": "https://help.openalex.org/data/concepts/"}, {"title": "Key Concepts - OpenAlex Developers", "url": "https://developers.openalex.org/guides/key-concepts"}, {"title": "OpenAlex Archives - OpenAlex blog", "url": "https://blog.openalex.org/category/openalex/"}, {"title": "Feature Archives - OpenAlex blog", "url": "https://blog.openalex.org/category/feature/"}, {"title": "OpenAlex", "url": "https://en.wikipedia.org/wiki/OpenAlex"}, {"title": "Attributes", "url": "https://help.openalex.org/data/works/attributes/"}, {"title": "Atlas of Science Collaboration, 1971-2020", "url": "https://arxiv.org/pdf/2308.16810"}, {"title": "Deprecations", "url": "https://help.openalex.org/api/deprecations/"}, {"title": "OpenAlex rewrite (\"Walden\") launch! - OpenAlex blog", "url": "https://blog.openalex.org/openalex-rewrite-walden-launch/"}, {"title": "Filling holes in science draws collective attention, but most higher-order holes remain unexplored", "url": "https://arxiv.org/pdf/2608.28822"}]}, "Based on the search results, here's what I found about OpenAlex legacy concepts in 2024-2025:\n\n## Concepts Status\n\nConcepts are superseded by Topics, OpenAlex's current subject-classification system. However, concepts are frozen — no longer recomputed or expanded — so new works are not tagged with them.\n\nThis is confirmed in the API documentation: Concepts are deprecated in favor of Topics, and while OpenAlex will continue to provide Concepts on Works, they are not actively maintaining, updating, or providing support for them.\n\n## Walden Expansion and New Works\n\nIn November 2025, OpenAlex added 190+ million new works as part of an expansion called XPAC (part of the Walden rewrite). These include datasets, software, and other research objects from DataCite and thousands of repositories.\n\n## Legacy Concept Assignment\n\nThe key finding is that legacy concept tags are retained for continuity while Topics are the current primary classification. Additionally, ancestors of assigned concepts are also included, so you may see low or zero scores. This means some works in the new Walden expansion may still have concept assignments, though these are no longer actively being updated or computed for new works."], "durationSeconds": 6.283341472, "searchCount": 1}
```

### [37] TOOL RESULT — WebSearch · 2026-09-29 02:08:13 UTC

```
{"query": "Sun Abraham 2021 event study heterogeneous treatment effects staggered adoption interaction-weighted estimator", "results": [{"tool_use_id": "srvtoolu_01QiqZnSP6KHsQwwiNbjUcdk", "content": [{"title": "Heterogeneous Effects Linear Panel Event Studies Liyang (Sophie) ...", "url": "https://conference.nber.org/confer/2023/SI2023/ML/heterogeneity.pdf"}, {"title": "Revisiting Event-Study Designs: Robust and Efficient Estimation ...", "url": "https://academic.oup.com/restud/article/91/6/3253/7601390"}, {"title": "Difference-in-Differences: Parallel Trends — CASRAI", "url": "https://casrai.org/guides/difference-in-differences-parallel-trends-staggered-adoption"}, {"title": "Comparative Evaluation of Difference in Differences Methods for Staggered Adoption Interventions", "url": "https://arxiv.org/pdf/2508.14365"}, {"title": "The problem", "url": "https://wiki.gccollab.ca/images/7/73/Handout_-_Treatment_effect_heterogeneity.pdf"}, {"title": "Making Event Study Plots Honest: A Functional Data Approach to Causal Inference", "url": "https://arxiv.org/pdf/2512.06804"}, {"title": "Visualization, Identification, and Estimation in the Linear ...", "url": "https://www.philadelphiafed.org/-/media/frbp/assets/working-papers/2021/wp21-44.pdf"}, {"title": "A Flexible, Heterogeneous Treatment Effects Difference-in- ...", "url": "https://www.york.ac.uk/media/economics/documents/hedg/workingpapers/2024/2417.pdf"}, {"title": "Difference-in-Differences Estimators of Intertemporal Treatment ...", "url": "https://www.nber.org/system/files/working_papers/w29873/revisions/w29873.rev0.pdf"}, {"title": "Interpreting Event-Studies from Recent Difference-in-Differences ...", "url": "https://arxiv.org/pdf/2401.12309"}]}, "Based on the search results, I found relevant information about the Sun and Abraham 2021 paper on event studies with heterogeneous treatment effects and staggered adoption.\n\nSun and Abraham published \"Estimating dynamic treatment effects in event studies with heterogeneous treatment effects\" in the Journal of Econometrics in 2021.\n\nThe paper shows that with variation in treatment timing, \"the coefficient on a given lead or lag can be contaminated by effects from other periods, and apparent pretrends can arise solely from treatment effects heterogeneity.\"\n\nThe paper proposes an interaction-weighted estimator for staggered adoption cases to obtain an uncontaminated dynamic event-study path.\n\nUsing an event-study design, Sun and Abraham (2021) estimate \"cohort-specific average treatment effects on the treated,\" k periods after the first treatment. Under staggered adoption, a two-way fixed effects estimator can be represented as a weighted average of policy effects for different event times and cohorts, but this estimator can put nonzero weight on effects at event times other than the one being studied, and can put negative weight on the effect at an event time for some cohorts."], "durationSeconds": 6.249977981999996, "searchCount": 1}
```

### [38] TOOL CALL — WebFetch · 2026-09-29 02:08:21 UTC

```
URL: https://help.openalex.org/data/concepts/
Prompt: When did OpenAlex stop tagging new works with legacy concepts? Quote exact sentences about new works, freeze date, and whether works published in 2023/2024/2025 have concepts.
```

### [39] TOOL RESULT — WebFetch · 2026-09-29 02:08:21 UTC

```
{"bytes": 38532, "code": 200, "codeText": "OK", "result": "# OpenAlex Concepts Deprecation Timeline\n\nBased on the documentation provided, here's what we know about when OpenAlex stopped tagging works with concepts:\n\n**Key Statement:**\n\"new works are not tagged with them and the concept tree is not maintained\"\n\nHowever, the page does **not specify an exact date** when this change occurred. It only indicates that:\n\n1. Concepts were replaced by Topics in 2024\n2. The system is now \"frozen\" with no new tagging\n3. Derived fields are \"no longer recomputed and are typically null on the live objects\"\n\n**Regarding 2023/2024/2025 Works:**\nThe document does not explicitly state whether works published in those years have concepts attached. It confirms that the deprecation happened sometime around or before 2024, but provides no granular information about which newly published works received concept tags versus which did not.\n\nFor precise dates about when tagging ceased, you would need to contact OpenAlex directly or consult their release notes, as this help page lacks that level of specificity.", "durationMs": 3639, "url": "https://help.openalex.org/data/concepts/"}
```

### [40] TOOL CALL — Grep · 2026-09-29 02:08:53 UTC

```
Pattern: "NOV_res|participation|ego_density|new_edge_rate|n_null|D_z|F_res"
```

### [41] TOOL RESULT — Grep · 2026-09-29 02:08:53 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "5:    would leak past the t0..t0+2 feature window. new_edge_rate divides by the window length in years (3, not 5).\n10:Everything else (PMI neighbour rule, SELF rule, the frequency-matched null of D_z, the multinomial null of F_res,\n11:NOV_res, participation, persistence, density, k-core, constraint) is the EXP3 code.\"\"\"\n165:def concept_core(name: str, aliases: list[str], t0: int, works, n_null: int, seed: int, windows=rq1_windows,\n200:        nl = distinct_null(pool_idx, nbg_early, len(new_list), labels_by_slice[s_mid], rng, n_null)\n204:    r[\"D_z\"], r[\"D_ratio\"], r[\"D_obs\"], labs = dz(C[\"comm\"], pool, new_idx)\n213:                n_null)\n216:        r[\"F_res\"] = obs_g - ng[ok].mean()\n218:        r[\"F_z\"] = r[\"F_res\"] / sdn if sdn > 0 else 0.0\n220:        r[\"F_res\"] = r[\"F_z\"] = float(\"nan\")\n242:            r[\"NOV_res\"] = r[\"NOV\"] - E\n244:            r[\"NOV\"] = r[\"NOV_res\"] = float(\"nan\")\n246:        r[\"NOV\"] = r[\"NOV_res\"] = float(\"nan\")\n254:    r[\"new_edge_rate\"] = (M / float(n_years)) / (n1 + 1)\n270:        r[\"participation\"] = float(1 - (pw ** 2).sum())\n274:        r[\"participation\"], r[\"n_comm_W3\"], r[\"comm_entropy\"] = float(\"nan\"), 0, float(\"nan\")\n291:            r[f\"ego_density_{w}\"] = e / (len(idx) * (len(idx) - 1) / 2)\n293:            r[f\"ego_density_{w}\"] = float(\"nan\")\n294:    r[\"ego_density_change\"] = r[\"ego_density_W3\"] - r[\"ego_density_W1\"]\n307:EGO_OUT = [\"D_z\", \"D_ratio\", \"D_rare\", \"D_sub\", \"D_obs\", \"NOV\", \"NOV_res\", \"F_res\", \"F_z\", \"deg_W1\", \"deg_W3\",\n308:           \"deg_growth\", \"str_growth\", \"new_edge_rate\", \"edge_persistence\", \"turnover\", \"participation\", \"n_comm_W3\",\n309:           \"comm_entropy\", \"comm_transitions\", \"ego_density_W3\", \"ego_density_change\", \"btw_end\", \"btw_change\",", "numLines": 22, "totalLines": 22}
```

### [42] TOOL CALL — Grep · 2026-09-29 02:08:53 UTC

```
Pattern: "ego|minutes|hours|elapsed|time"
```

### [43] TOOL RESULT — Grep · 2026-09-29 02:08:53 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "", "numLines": 0, "totalLines": 0}
```

### [44] TOOL CALL — Read · 2026-09-29 02:09:05 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/preview_data_out.json
```

### [45] TOOL RESULT — Read · 2026-09-29 02:09:05 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/preview_data_out.json", "content": "{\n \"datasets\": [\n  {\n   \"dataset\": \"concept_recognition\",\n   \"examples\": [\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C144501496\\\", \\\"qid\\\": \\\"Q5533489\\\", \\\"qid_resolved\\\": \\\"Q5533489\\\", \\\"label\\\": \\\"Genome editing\\\", \\\"label_norm\\\": \\\"genome editing\\\", \\\"aliases\\\": [\\\"genome editing\\\", \\\"Genome engineering\\\"], \\\"aliases_norm\\\": [\\\"genome engineering\\\"], \\\"acronyms\\\": [], \\\"level\\\": 4, \\\"ancestor_ids\\\": [\\\"C98108389\\\", \\\"C141231307\\\",...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"nature_methods_moty\\\", \\\"event_type\\\": \\\"nature_methods_method_of_the_year\\\", \\\"year\\\": 2011, \\\"date\\\": null, \\\"date_precision\\\": 9, \\\"year_usable\\\": true, \\\"match_method\\\": \\\"embed+llm\\\", \\\"match_confidence\\\": 0.85, \\\"relation\\\": \\\"broader\\\", \\\"entry_id\\\": \\\"nature_methods_moty:2011:1.0:4\\\", \\\"detail\\\":...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 4,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\"\n     ],\n     \"metadata_n_events\": 11,\n     \"metadata_n_events_year_usable\": 10,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C144501496\",\n     \"metadata_qid\": \"Q5533489\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C46111723\\\", \\\"qid\\\": \\\"Q471857\\\", \\\"qid_resolved\\\": \\\"Q471857\\\", \\\"label\\\": \\\"Proteomics\\\", \\\"label_norm\\\": \\\"proteomic\\\", \\\"aliases\\\": [\\\"proteomics\\\"], \\\"aliases_norm\\\": [], \\\"acronyms\\\": [], \\\"level\\\": 3, \\\"ancestor_ids\\\": [\\\"C104317684\\\", \\\"C55493867\\\", \\\"C54355233\\\", \\\"C86803240\\\", \\\"C185592680\\\"], \\\"level0_discipli...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"wikipedia_en\\\", \\\"event_type\\\": \\\"wikipedia_page_created_estimated\\\", \\\"year\\\": 2002, \\\"date\\\": \\\"2002-06-05\\\", \\\"date_precision\\\": \\\"estimated\\\", \\\"year_usable\\\": true, \\\"match_method\\\": \\\"wikidata_sitelink\\\", \\\"match_confidence\\\": 0.8, \\\"relation\\\": \\\"same\\\", \\\"entry_id\\\": null, \\\"detail\\\": {\\\"title\\\": \\\"Pr...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 3,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\"\n     ],\n     \"metadata_n_events\": 9,\n     \"metadata_n_events_year_usable\": 9,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C46111723\",\n     \"metadata_qid\": \"Q471857\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C152662350\\\", \\\"qid\\\": \\\"Q815297\\\", \\\"qid_resolved\\\": \\\"Q815297\\\", \\\"label\\\": \\\"Systems biology\\\", \\\"label_norm\\\": \\\"systems biology\\\", \\\"aliases\\\": [\\\"systems biology\\\", \\\"systems approach to biology\\\", \\\"system biology\\\"], \\\"aliases_norm\\\": [\\\"system biology\\\", \\\"systems approach to biology\\\"], \\\"acronyms\\\": [], ...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"wikipedia_en\\\", \\\"event_type\\\": \\\"wikipedia_page_created_estimated\\\", \\\"year\\\": 2004, \\\"date\\\": \\\"2004-02-13\\\", \\\"date_precision\\\": \\\"estimated\\\", \\\"year_usable\\\": true, \\\"match_method\\\": \\\"wikidata_sitelink\\\", \\\"match_confidence\\\": 0.8, \\\"relation\\\": \\\"same\\\", \\\"entry_id\\\": null, \\\"detail\\\": {\\\"title\\\": \\\"Sy...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 2,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\"\n     ],\n     \"metadata_n_events\": 8,\n     \"metadata_n_events_year_usable\": 8,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C152662350\",\n     \"metadata_qid\": \"Q815297\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C189206191\\\", \\\"qid\\\": \\\"Q222046\\\", \\\"qid_resolved\\\": \\\"Q222046\\\", \\\"label\\\": \\\"Genomics\\\", \\\"label_norm\\\": \\\"genomic\\\", \\\"aliases\\\": [\\\"genomics\\\", \\\"genomic science\\\", \\\"genome science\\\", \\\"genome sciences\\\"], \\\"aliases_norm\\\": [\\\"genome science\\\", \\\"genomic science\\\"], \\\"acronyms\\\": [], \\\"level\\\": 4, \\\"ancestor_ids\\\":...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"mesh\\\", \\\"event_type\\\": \\\"mesh_descriptor_introduced\\\", \\\"year\\\": 2001, \\\"date\\\": \\\"2001-01-01\\\", \\\"date_precision\\\": 9, \\\"year_usable\\\": true, \\\"match_method\\\": \\\"wikidata_property\\\", \\\"match_confidence\\\": 1.0, \\\"relation\\\": \\\"same\\\", \\\"entry_id\\\": \\\"mesh:D023281\\\", \\\"detail\\\": {\\\"ui\\\": \\\"D023281\\\", \\\"name\\\": \\\"...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 4,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\"\n     ],\n     \"metadata_n_events\": 8,\n     \"metadata_n_events_year_usable\": 8,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C189206191\",\n     \"metadata_qid\": \"Q222046\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C3019978661\\\", \\\"qid\\\": \\\"Q739734\\\", \\\"qid_resolved\\\": \\\"Q739734\\\", \\\"label\\\": \\\"Gut microbiome\\\", \\\"label_norm\\\": \\\"gut microbiome\\\", \\\"aliases\\\": [\\\"human gut flora\\\", \\\"gut microbiota\\\", \\\"gastrointestinal microbiota\\\", \\\"gut microbiome\\\", \\\"gastrointestinal microbiome\\\", \\\"Human gastrointestinal microbiota\\\",...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"wikipedia_en\\\", \\\"event_type\\\": \\\"wikipedia_page_created_estimated\\\", \\\"year\\\": 2005, \\\"date\\\": \\\"2005-11-11\\\", \\\"date_precision\\\": \\\"estimated\\\", \\\"year_usable\\\": true, \\\"match_method\\\": \\\"wikidata_sitelink\\\", \\\"match_confidence\\\": 0.8, \\\"relation\\\": \\\"same\\\", \\\"entry_id\\\": null, \\\"detail\\\": {\\\"title\\\": \\\"Gu...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 0.75,\n     \"metadata_level\": 3,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\",\n      \"13\",\n      \"24\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\",\n      \"Medicine\"\n     ],\n     \"metadata_n_events\": 7,\n     \"metadata_n_events_year_usable\": 7,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C3019978661\",\n     \"metadata_qid\": \"Q739734\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C2994067223\\\", \\\"qid\\\": \\\"Q380546\\\", \\\"qid_resolved\\\": \\\"Q380546\\\", \\\"label\\\": \\\"Genomic sequencing\\\", \\\"label_norm\\\": \\\"genomic sequencing\\\", \\\"aliases\\\": [\\\"DNA sequencing\\\", \\\"sequence analysis, DNA\\\", \\\"DNA sequence analysis\\\"], \\\"aliases_norm\\\": [\\\"dna sequence analysis\\\", \\\"dna sequencing\\\", \\\"sequence analy...\",", "numLines": 120, "startLine": 1, "totalLines": 1106}}
```

### [46] ASSISTANT · 2026-09-29 02:13:13 UTC

```
Checked the key risk (OpenAlex stopped tagging new works with legacy concepts, which threatens 2023-24 outcome counts). Now writing the plan JSON, README and manifest.
```

### [47] TOOL CALL — Write · 2026-09-29 02:13:13 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json

{
  "title": "Do open-neighbourhood concepts spread? Fresh-cohort test",
  "summary": "Single-unseal confirmation of the openness claim (RQ1) on a 2015-2016 onset cohort of OpenAlex legacy concepts that no screen has touched. The frame, grounding and outcomes are the EXP5/EXP8 ones, re-used by path. One zero-credit S3 snapshot pass adds 2015-2024 works for the cohort candidates plus 300 EXP5 control concepts. OPEN (the mean of six signed z-scored ego-network components) is built three ways: ALL-PAPERS, HOME-ONLY and SIZE-MATCHED ALL-PAPERS. It is tested through the ladder B5 -> +CONTACT_REACH -> +CONCEPT TYPE -> +PRE-ONSET FOOTPRINT -> +label coverage -> +home-group FE, within method and within object concepts, per group with DL pooling, and against RETENTION_RATIO_early. Every definition, z constant, covariate and verdict rule is frozen on the 12,499-concept EXP5 frame (selection data only) and hash-sealed before any cohort outcome is read. Two pre-declared, outcome-blind audits guard the measurement: one covers legacy-tag and venue-label coverage in 2021-2024 (OpenAlex froze its legacy concepts, so new works may be untagged), the other is a power check that can trigger the declared 2017 extension. Concept TYPE is LLM-labelled with a 300-concept, two-model benchmark and a 60-item check read by the executor. Secondary: the frozen Exp8 learned models (O3 L1-logit, O4 EBM, O2r ElasticNet) and the n_authors_early and CONTACT_REACH leads, with no refit. Expected LLM spend is about $1.5 (hard cap $3). OpenAlex API credits: 0.",
  "runpod_compute_profile": "gpu_basic",
  "domain_practice": "WHAT I READ AND CHECKED (bounded; no domain handbook fits: the four offered cover computational linguistics, mechanistic interpretability, multi-agent LLMs and neuro-symbolic AI, so this rests on this run's verified literature (art_dxvRpQufMR0e, art_EesdB8cuSfcU), the EXP5/EXP8 code and READMEs, and targeted lookups). (a) OpenAlex documentation on legacy Concepts (help.openalex.org/data/concepts; developers.openalex.org key-concepts; the Walden launch post). Concepts are deprecated and frozen: 'new works are not tagged with them', and no cut-off date is given. For a 2015-16 cohort whose outcome window is 2021-2024, this is the first measurement threat. EXP5's TAG grounding (title match AND legacy tag score >= 0.3) silently loses recall for works indexed after the freeze. Nobody in the field would accept a breadth or uptake outcome whose grounding recall changes inside the outcome window. (b) Sun & Abraham 2021 (J. Econometrics) and Callaway & Sant'Anna 2021 on staggered event studies. They are NOT used here: within-concept timing belongs to another artifact of this iteration. That boundary is stated so the executor does not drift into RQ2. (c) The EXP8 README (portability table, P1-P5, audits T0-T8, pooled MDE 0.049 at n about 1,800-3,400) and the EXP5 README (frame rules, TAG benchmark P 0.947 / R 0.659, LLM precision gate, seal/unseal machinery).\n\nHOW STUDIES OF THIS KIND ARE BUILT IN SCIENTOMETRICS AND SCIENCE OF SCIENCE. (1) BASELINES. Every emergence or diffusion predictor is judged against size and growth: early publication count, growth rate and early breadth (reach, Shannon or Rao-Stirling entropy). Rotolo, Hicks & Martin 2015 give the attribute framing. Cheng et al. 2023 (ASR) control volume and social reach before crediting semantic or structural resonance. Weng, Menczer & Ahn 2013 compare community count against early volume. Uzzi et al. 2013 and Wang, Veugelers & Stephan 2017 compare novelty (new combinations) against field and year baselines. The rival a reviewer names FIRST for our claim is the TYPE of concept: methods and 'research technologies' travel (Leydesdorff & Rafols 2011), and methods dominate citation tops (Van Noorden et al. 2014, 'The top 100 papers'). The second is the concept's pre-existing generic footprint. The fair way to tune such a baseline is to give it the same features, windows and sample as the candidate, fitted on the same selection data, which is what B5 plus the ladder does. (2) DATA. OpenAlex (or WoS or Scopus) works with venue-based field labels. Paper-level topic classifiers are known to be circular for diffusion because they read the paper's own text and references. The legacy MAG/OpenAlex concept vocabulary is a known selection condition: it was seeded from Wikipedia around 2016-19, so concepts born 2015-16 are under-represented relative to earlier cohorts. Temporal out-of-sample cohorts are the accepted confirmation design; examples are citation-forecasting work since Wang, Song & Barabasi 2013, and this run's own EXP5/EXP8 2010-14 cohort. (3) CONTROLS. Volume (hence rarefaction; Hurlbert 1971 and Heck et al. 1975 in diversity ecology), onset year (period effects, measured as onset-year dummies), field or home-group fixed effects, label coverage (venue coverage 26-80%, lowest in conference-heavy CS), and mechanical coupling between predictor and outcome. The last is the one this design is most likely to be caught on: an ego network built on all papers gains off-home topics exactly when the concept spreads off-home. (4) HOW MUCH IS ENOUGH. Concept-level studies in this literature use hundreds to tens of thousands of concepts (Cheng et al. about 60k; EXP8 12.5k). A within-stratum correlation on fewer than about 100 concepts is not believed. Reports give point estimates with bootstrap or analytic 95% CIs, the resampling unit named, heterogeneity across fields (I2 from DerSimonian-Laird 1986 / Higgins & Thompson 2002) and multiplicity control (Holm). This run's EXP8 pooled MDE (2.8 SE) was 0.049 at n about 1,800-3,400. At the expected cohort n of about 1,000-2,000 the pooled MDE is about 0.07-0.09, and within-type strata (about 25-40% of concepts each) have an MDE of about 0.12-0.15. Power has to be computed before the unseal and stated next to the verdict. (5) MEASURES AND REPORTING. Partial Spearman given baseline covariates (rank-residual correlation), incremental AUC or R2 over the baseline for learned models, forest plots per field with a pooled diamond, a ladder figure (estimate by control rung), per-component rows for composite indices, placebos (shuffled outcomes, planted effects), and a statement of the pre-registration and seal. For LLM-derived labels, practice since Gilardi et al. 2023 and Tornberg 2023 is agreement with a human-read gold subset (precision per class, Cohen's kappa between models), with the prompt and model version frozen and published.",
  "practice_alignment": "MEETS. (1) Temporal out-of-sample cohort scored once from a sealed spec (EXP5/EXP8 seal.py pattern with a hash chain). (2) The size/growth/breadth baseline B5 plus onset-year dummies. Breadth is volume-adjusted twice (O2r rarefied at m = 50, and O2r_resid with a frozen a/b). (3) The reviewer's first-named confounds are rungs of the ladder: concept type, generic pre-existing footprint, label coverage and home-group FE. (4) Mechanical coupling is attacked by construction: a HOME-ONLY build, plus a SIZE-MATCHED ALL-PAPERS build that separates 'fewer papers' from 'home restriction'. (5) The concept is the resampling unit (2,000 refit bootstraps), with DL pooling and I2 across 5 groups, Holm within the pre-declared 8-test family, and a per-component breakdown of the composite. (6) Placebos: 200 within-group outcome shuffles and a planted psp = 0.10 recovery on the cohort feature matrix. (7) LLM labels are validated against two models and a 60-item gold set, with per-class precision, Wilson CIs, kappa, and the prompt and model hashed.\n\nDEPARTURES, AND WHAT EACH COSTS. (a) The concept frame is the legacy OpenAlex concept vocabulary, not an outcome-blind phrase frame (the original Frame N). This is justified because it keeps the grounding identical to the selection data, and a new frame would be a new instrument. The cost: the 2015-16 cohort is conditioned on concepts that MAG/OpenAlex had already named by about 2016-19. Those are likely the more successful newborns, which restricts the range of outcomes and probably attenuates associations. This is stated as a scope limit. (b) The 'hand check' of 60 type labels is read by the executor agent, not a human annotator. This is disclosed. The two-model agreement and the frozen prompt are the checks a reader can re-run. (c) The outcome window runs into 2023-2024, and OpenAlex stopped tagging new works with legacy concepts. The plan does not ignore this. A pre-declared, outcome-blind coverage audit (base-work tag rates per year, and tag/title-match ratios on EXP5 control concepts) chooses the outcome grounding BEFORE the seal: TAG if coverage holds, otherwise title-match grounding (MATCH) for every outcome year, validated on EXP5 selection data (rho >= 0.9 with TAG-based O2r). The TAG-only window of 2015 onsets ending in 2022 is always reported as a sensitivity. What remains: if MATCH is chosen, grounding precision in the outcome window is lower (EXP5 exact-name precision 0.87 against TAG 0.95). The composition-based O2r is robust to uniform precision loss, and O1c is less robust. (d) Venue labels come from the frozen EXP5 source->field map. Sources created after the map miss labels in 2023-24, so O2r is computed on labelled papers only, and yearly label coverage is reported and entered as a covariate. (e) The cohort n (probably about 1,000-2,000) gives a pooled MDE of about 0.07-0.09 and within-type MDEs of about 0.12-0.15. That sits at the edge of the expected OPEN effect: the Exp8 single components were 0.08-0.17, and the composite is probably larger. The plan fixes this with more graded samples, not more metrics. The declared 2017 extension triggers when fewer than 800 concepts pass OR the simulated power of the primary clause is below 0.80. It needs no second pass, because the snapshot pass already collects 2017 candidates. (f) There is only one period-level replication, so period effects cannot be separated from cohort effects. The EXP5 selection-data ladder is reported as a second, non-confirmatory body. (g) O4 (citation growth) needs a citation pass and is the first thing dropped. The O4 EBM replication is then reported as 'not run', never as a null. (h) No human-coded concept-type taxonomy exists for OpenAlex legacy concepts. The 4-class scheme is the direction's own and is not a published standard; this is disclosed. The within-type test uses the method and object classes only.",
  "builds_on": "This is a DEEPEN of the EXP8 lead (art_dFQ6jbgNsR6Q), not a fresh line. Everything is re-used BY PATH under the run root /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/ (read-only; copy what is needed into the workspace). Only art_O7Dq4L02QnDN is a declared dependency. If a path is missing, re-implement from the definitions below against the public S3 snapshot and log it in results/deviations.json.\n\nEXP5 = iter_2/gen_art/gen_art_experiment_5 (art_wxWssKSUR45f).\n- results/frame_concepts.csv: 12,499 concepts, SELECTION data.\n- concept_outcomes.csv, results/frame_summary.json and results/deviations.json: the exact realised early-volume threshold (30, or relaxed 20) and the frame rules.\n- frame.py: home_rule (>= 40% of the first 30 venue-labelled works, weak >= 25%), split_of/group map, rarefied_richness (exact hypergeometric), concept_outcomes. Imported, not re-written.\n- scan/agg_counts.parquet: counts per concept x year 1995-2022 x venue field x tagstate x mtype for all 56,643 lexicon concepts. It gives the cohort candidate frame, the footprint, the tag-coverage audit and the MATCH-vs-TAG validation.\n- scan/year_field_totals.npz, results/source_field.parquet, matcher.py, rangefile.py, scan_full.py (base-work filter), snapshot/works_manifest.json (snapshot identity), snapshot/concepts/part_*.parquet (legacy concept descriptions, level), lexicon_v1.parquet + frozen_lexicon.sha256.\n- grounding.py: the TAG rule, and cmd_precision with the per-concept LLM gate prompt. M1 = google/gemini-2.5-flash-lite, 10 grounded titles, +10 if 7-8/10 positive, pass at >= 0.8.\n- llm.py: the OpenRouter client with a disk cache keyed by model+messages, and the usage.cost ledger.\n- scan/llm_cache/: re-used for any identical call.\n\nEXP8 = iter_3/gen_art/gen_art_experiment_8 (art_dFQ6jbgNsR6Q).\n- passA.py: the template for the new snapshot pass, with the EXP5 matcher and TAG unchanged. It writes BG[year, topic] and early rows (ci, year, work_id, vfield, topic idx list, author ids).\n- lib/ego.py concept_core: the six OPEN components are new_edge_rate, n_comm_W3, participation, NOV_res (analytic expectation, no null draws), ego_density_W3 and edge_persistence. Windows: PRE = t0-3..t0-1, W1..W3 = t0, t0+1, t0+2. Slice mapping: years > 2014 map to backbone slice2 (2010-14), which is pre-onset for the cohort.\n- lib/ego_ctx.py (context: inputs/backbone/slice0-2.npz, data/bg_topics.npz covering 1995-2022, inputs/topic_ids.json, topic_meta.csv).\n- build_features.py and lib/indicators.py: B5, CONTACT_REACH, RETENTION_RATIO_early, n_authors_early, and every input of the frozen models.\n- outcomes.py: O1c, O1b, O2r_m50, O2r_resid, O3, O4.\n- results/o2r_resid_fit.json: frozen a/b.\n- lib/rq1stats.py: partial Spearman with refit bootstrap, DL, Holm.\n- lib/design.py: frozen imputation and standardisation.\n- lib/seal.py: the freeze/unseal gate.\n- data/frame_matches_early/part_*.parquet: EXP5-frame early rows with vfield. The EXP5 HOME-ONLY and SIZE-MATCHED builds come from these, with no new pass.\n- data/ego_features.parquet: the ALL-PAPERS components for EXP5, used as the reproduction target.\n- data/features_basic.parquet, data/outcomes.parquet (EXP5 outcomes, selection data).\n- models/linear_all_O3.joblib, ebm_O4.joblib, linear_all_O2r_m50.joblib, linear_all_O2r_resid.joblib, plus results/learned_model.json, frozen_spec.json and case_exemplars.json.\n\nEXP6 = iter_2/gen_art/gen_art_experiment_6: lib/h2.py (D3 ENTERED/RETAINED/LOST states needed by RETENTION_RATIO_early; also copied in EXP8/lib/h2.py).\n\nDECLARED DEPENDENCY art_O7Dq4L02QnDN = iter_2/gen_art/gen_art_dataset_2/full_data_out/full_data_out_{1,2,3}.json (concept_recognition). It supplies the Wikipedia creation year (events with source 'wikipedia_en', year_usable true) for the generic-term footprint marker, and the QID and level for joining.\n\nNEGATIVE FINDINGS BUILT PAST, and not re-tested. The retained frontier, the abandonment penalty, gateway H1/H3, A*_h, O5 as a validation outcome, and candidate S are all closed. M0_density_end and D_vol_end are excluded from OPEN and from every rung, because they carry a pre-onset footprint. P3's 'new_edge_rate fails' is superseded, since it transferred.",
  "implementation_pseudocode": "PROJECT LAYOUT (workspace root W = this artifact's cwd). method.py (orchestrator with --only STEP), lib/ (copied EXP5/EXP8 modules plus new home.py, typing_llm.py, ladder.py), data/, data/sealed/, results/, figures/, logs/, tests/. Python 3.12 via uv. Pin the package versions from the EXP8 environment (read EXP8 reproducibility.md / pyproject / uv.lock), at least scikit-learn, interpret (EBM), joblib, numpy, pandas, pyarrow, python-igraph, leidenalg and pyahocorasick, so the frozen joblib models unpickle. Follow aii-python (loguru), aii-parallel-computing (ProcessPoolExecutor, spawn), aii-long-running-tasks (staged scale-up, background PIDs, never pkill by name) and aii-json (exp_gen_sol_out).\n\nS0 PRE-REGISTRATION AND OUTPUT-FORMAT DRY RUN (first 30 min).\n  - Write prereg.md holding, verbatim: the OPEN definition and signs; the three builds; the ladder rungs and their exact covariates; the groups; the verdict rules; the Holm family; the power/extension trigger; the tag-coverage decision rule; the drop order.\n  - Write results/frozen_spec_v0.json with the same content machine-readable, plus sha256 of the copied code files. Append sha256(prereg.md + spec_v0) to logs/seal.log with a timestamp. git commit.\n  - Output-format dry run (EXP9 died in its output loop): write a 3-example stub full_method_out.json in exp_gen_sol_out form and validate it with the aii-json skill NOW. Keep the builder function make_method_out() under unit test (tests/test_output.py) so the final write cannot fail.\n  FROZEN DEFINITIONS in prereg:\n    OPEN_b = mean over available k of s_k * (x_k - mu_k,b) / sd_k,b, where\n      k in {new_edge_rate(+), n_comm_W3(+), participation(+), NOV_res(+), ego_density_W3(-), edge_persistence(-)};\n      mu and sd are frozen PER BUILD b on all 12,499 EXP5 concepts;\n      OPEN is NaN unless >= 4 of the 6 are finite.\n    Winsorise each component at its EXP5 0.5/99.5 percentiles (frozen) before z-scoring.\n    Builds:\n      ALL: every grounded early paper, exactly as in EXP8.\n      HOME: only grounded papers whose venue field is in the concept's home set, applied to BOTH the PRE window and W1-W3. Venue-unlabelled papers are dropped. OPEN_home = NaN if fewer than 10 home papers in t0..t0+2 (declared now; EXP5 sensitivity at 5 and 20).\n      SIZEMATCH: for each concept, 20 seeded random subsamples (seed = 1000 + ci) of its early papers (PRE and W1-W3 subsampled separately, each to that window's home-only count). Each component is averaged over the 20 draws, then z-scored with SIZEMATCH constants.\n    Primary outcome: O2r_m50 (rarefied venue-field richness among 50 concept-papers in t0+6..t0+8, exact hypergeometric; NaN if fewer than 50 labelled papers, as in EXP8). Co-outcome: O2r_resid (EXP8 plan formula, frozen a/b from o2r_resid_fit.json).\n\nS1 COHORT CANDIDATE FRAME (outcome-blind; uses years <= t0+2 only).\n  - From EXP5 scan/agg_counts.parquet, compute grounded yearly counts under TAG exactly as frame.py/grounding.grounded_mask does (tagstate 1, plus tagstate 3 gated by the frozen sense-filter pass rate, as EXP5 did).\n  - t0 = first year in 2000..2017 with >= 20 grounded works. Keep t0 in {2015, 2016, 2017}, early volume (t0..t0+2) >= the EXP5 realised threshold, and ci not in EXP5 frame_concepts.csv. Concepts with t0 <= 2014 are excluded by the rule itself.\n  - Home and group via frame.home_rule on the first 30 venue-labelled works (years <= t0+2). Newborn flag with the EXP5 rule.\n  - 2017 rows are FALLBACK candidates only (flag role = 'fallback').\n  - Write data/cohort_candidates.csv. Log counts by t0 x group. The expected 2015-16 count is roughly 1,000-2,500 before the gate.\n\nS2 ONE ZERO-CREDIT SNAPSHOT PASS (passC.py, adapted from EXP8 passA.py). Launch in the background ASAP, with checkpoint files done_XXXX.json so it is resumable.\n  - Snapshot identity: compare the current S3 works manifest with EXP5 snapshot/works_manifest.json. Log any change to results/deviations.json.\n  - Base-work filter: identical to EXP5 scan_full.py (article|review, not paratext, not xpac), except the year cap moves 2022 -> 2024.\n  - Columns: title, publication_year, type, primary_location.source.id, the legacy concepts (id, score), topics (ids), authorships.author.id. referenced_works is read ONLY if O4 will be attempted; decide by the timing of the first 20 files.\n  - Match the full frozen lexicon (Aho-Corasick + stemmed verification, EXP5 matcher unchanged), but emit rows only for:\n    (i) cohort candidates incl. 2017, and\n    (ii) 300 CONTROL concepts sampled from EXP5 frame_concepts.csv (seed 7, stratified by group).\n  - Outputs per file:\n    (a) EARLY rows for candidates with t0-3 <= year <= t0+2: ci, year, work_id, vfield, topic idx list, author ids, title (titles only for candidates; needed for the precision gate and type labels), tagstate, mtype.\n    (b) AGG counts per (ci, year 1995-2024, vfield, tagstate, mtype) for candidates and controls. Rows with year >= t0+3 go to data/sealed/outcome_agg_*.parquet, which is NOT read before the seal; write the sha256 of each part to logs/sealed_files.log.\n    (c) Base totals per (year 2012-2024, vfield), plus the per-year counts of base works with >= 1 legacy concept tag and with >= 1 tag of score >= 0.3 (outcome-blind coverage audit).\n    (d) BG[year, topic] for 2012-2018.\n  - Use 4-5 worker processes (leave 2-3 vCPUs for S4/S5 running concurrently).\n  - Scale up per aii-long-running-tasks: 3 files -> 20 files -> all. Extrapolate time after 20 files. If the projected pass exceeds 150 min, drop titles and authorships for controls first, then referenced_works.\n  CHECKS right after the pass, all outcome-blind:\n    T1: for the 300 controls, yearly TAG counts 1995-2022 must equal agg_counts exactly. For candidates, counts for years <= t0+2 only. Rule: if >= 99% of (concept, year) cells match exactly and the median |rel diff| < 1%, proceed and log the residual; otherwise stop, log, and investigate (snapshot change) before anything else.\n    T2: BG 2012-2018 equals EXP8 bg_topics.npz on the overlapping years.\n    T3: base totals 2012-2022 equal EXP5 year_field_totals.\n\nS3 OUTCOME-GROUNDING DECISION (outcome-blind; frozen before the seal).\n  - tag_rate[y] = share of base works with >= 1 legacy tag of score >= 0.3, for y = 2015..2024.\n  - For the 300 EXP5 controls: ratio[y] = TAG-grounded / title-matched verified hits.\n  - RULE (declared in S0): if min over y in {2021..2024} of tag_rate[y] / mean(tag_rate[2017..2019]) >= 0.90 AND the same holds for the control ratio, then OUTCOME_GROUNDING = TAG. Otherwise OUTCOME_GROUNDING = MATCH (verified title-match hits, all tagstates, same lexicon, concepts still gated by the LLM precision gate) for ALL outcome years of the cohort.\n  - If MATCH is chosen, validate it on EXP5 selection data from agg_counts: Spearman(O2r_m50_MATCH, O2r_m50_TAG) at t0+6..t0+8 must be >= 0.90. Refit the O2r_resid a/b for MATCH on EXP5 (frozen). If validation fails, the primary becomes the TAG 2015-onset window t0+5..t0+7 (ending 2022) and the full cohort is secondary.\n  - Also report the venue-label coverage of base works by year (the share whose source is in source_field.parquet). This enters the coverage rung.\n\nS4 LLM PER-CONCEPT PRECISION GATE for the candidates (after S2, which provides the early titles).\n  - Re-use grounding.cmd_precision logic verbatim: same prompt builder, model google/gemini-2.5-flash-lite, temperature, batch size, 10 titles (+10 if 7-8/10), pass at precision >= 0.8. The llm.py cache and ledger are pointed at W/llm_cache plus a read-only lookup into EXP5 scan/llm_cache.
  - Expected: about 3,000 candidates at about $0.00017 each, so about $0.5.\n  - FINAL COHORT = 2015-16 candidates passing the gate. Write cohort_frame.csv (ci, openalex_id, label, t0, home, group, weak_home, intersection_born, newborn, precision_c, role).\n\nS5 CONCEPT TYPE (lib/typing_llm.py; runs concurrently with S2 for the EXP5 concepts, and after S4 for the cohort).\n  - Input per concept: label; the legacy description (EXP5 snapshot/concepts parquet); legacy level; 3 early titles (cohort from S2, EXP5 from the EXP5 reservoir/sample titles; if none, name+description only, flagged).\n  - Output JSON: {type: method|object|property|topic, generic: 0/1, confidence}. Class definitions in the prompt:\n    method = technique, tool, algorithm, instrument, assay, software, model class;\n    object = material, organism, disease, device-as-object, molecule, phenomenon-entity;\n    property = measure, statistic, theory, law, property;\n    topic = field or research area.\n    generic = a term in common scientific use before the concept's onset year (e.g. 'Coefficient of variation', 'Exponential growth').\n  - Batch 20 concepts per call; model M1 = google/gemini-2.5-flash-lite at temperature 0. About 14.5k-15k concepts, about 750 calls, about $0.6.\n  - BENCHMARK: 300 concepts stratified by group (50 per group, both frames) are labelled by M2 = openai/gpt-4.1-mini (another family; about $0.1). The executor reads 60 of them (stratified by M1 class) and assigns gold labels blind to the model outputs before comparing.\n    Metrics: per-class precision of M1 on the 60 gold (Wilson 95% CI), Cohen's kappa M1-vs-M2 on 300, and the method-vs-object confusion.\n    GATE: M1 precision >= 0.85 for BOTH 'method' and 'object' on the gold set. If it fails, revise the prompt once (definitions and 4 few-shot examples drawn from outside the benchmark), re-label everything, and re-check. If it fails again, the within-type tests use only concepts where M1 = M2 (M2 then labels all concepts in the method/object classes, about $0.5 more), and this is logged.\n  - Write concept_types.csv (both frames) and type_benchmark.json. Hard LLM cap for the artifact: $3.00, tracked from usage.cost. Stop the batch on the first 'AI Inventor per-run OpenRouter budget' 403 (checked after each semaphore acquire). GET <base_url>/key before starting.\n\nS6 PRE-ONSET FOOTPRINT (from agg_counts, years < t0 only; both frames). Write footprint.csv with:\n  - fp_logN = log1p(grounded papers t0-10..t0-1);\n  - fp_nfields = number of venue fields with >= 1 grounded paper before t0;\n  - fp_reemerge = 1 if any pre-t0 year has >= 25% of the t0+2 count (t0+2 <= 2018 for the cohort, hence allowed);\n  - fp_wiki_pre = 1 if art_O7Dq4L02QnDN has a wikipedia_en creation event with year_usable and year < t0;\n  - newborn flag;\n  - legacy level (2-5; kept in the TYPE rung as specificity dummies).\n\nS7 FEATURES over t0..t0+2 (and PRE) only. Write data/features_cohort.parquet, data/features_exp5_homeonly.parquet and data/features_exp5_sizematched.parquet.\n  - Add flags to ego.concept_core: compute_btw=False, n_null=0 (skip D_z/F_res nulls, which are not in OPEN).\n  - TEST FIRST (tests/t_ego_flags.py): on 100 EXP5 concepts the six components with flags off must equal EXP8 data/ego_features.parquet to 1e-12.\n  - EXP5 frame (12,499): the HOME build from EXP8 data/frame_matches_early + home sets from frame_concepts.csv; the SIZEMATCH build likewise. ALL = EXP8 ego_features.parquet (re-used, and recomputed for 200 concepts as a check).\n  - Cohort: ALL, HOME and SIZEMATCH from the S2 early rows. The context is identical to EXP8 (backbone slices; BG from EXP8 bg_topics.npz for years <= 2018, which covers the cohort).\n  - Cohort basic features via EXP8 build_features functions: B5 (log early volume, early growth, off-home share, entropy, reach), CONTACT_REACH, RETENTION_RATIO_early (EXP6 h2 D3 states from yearly field counts 1995..t0+2: agg_counts plus the S2 early rows), n_authors_early, every input column of the frozen models (from their feature_names_in_ / learned_model.json), home-paper coverage share, venue-label coverage share.\n  - Parallelise over concepts with ProcessPoolExecutor (spawn, chunks of 200). Log time per 1,000 concepts after the first 500.\n\nS8 SELECTION ON THE EXP5 FRAME (selection data; nothing from the cohort's outcome window is read).\n  (a) Freeze the winsor bounds and z constants per build. Compute OPEN_all, OPEN_home and OPEN_sizematch for the 12,499.\n  (b) Selection-data results: psp of each OPEN build and each component with O2r_m50 and O2r_resid at every ladder rung (EXP5 outcomes from EXP8 data/outcomes.parquet), per group with DL/I2, and within type. This is the FIRST test of confound (ii) and is reported as selection-data evidence, never as confirmation.\n  (c) Coupling diagnostic: Spearman of each OPEN build with early off-home share and with log early volume.\n  (d) Power: subsample the EXP5 frame to the realised cohort n and group mix (1,000 draws), and compute P(CI > 0 at the TYPE rung) for the pooled OPEN_home psp, assuming the true effect equals HALF the EXP5 selection estimate (a conservative shrinkage, cf. EXP5 H3 shrinkage 0.21). Also the MDE, and the within-method and within-object MDEs.\n      EXTENSION RULE (declared in S0): if the cohort n < 800 OR power < 0.80, add the 2017 candidates that passed the gate (outcome window t0+5..t0+7 = 2022-2024, window flag entered as a covariate with the onset-year dummies). This is decided HERE, before the seal.\n  (e) Freeze in results/frozen_spec.json: z constants, winsor bounds, OPEN_home min-paper rule, the outcome grounding (S3), O2r_resid a/b, the type labels (hash of concept_types.csv), footprint and covariate lists per rung, the group map, the Holm family, the extension decision, bootstrap seeds (B = 2,000, seed 20260929), the imputation medians for the learned models, and the sha256 of every script and input table (features_cohort.parquet, cohort_frame.csv, concept_types.csv, footprint.csv).\n  (f) Run the EXP8 lib/seal.py freeze: append the spec hash to logs/seal.log. Pre-unseal checklist: no outcome column in any cohort table, and data/sealed/ untouched (sha256 re-checked against logs/sealed_files.log). git commit.\n\nS9 SINGLE UNSEAL.\n  - seal.unseal() refuses without the matching spec hash and refuses a second call.\n  - Compute the cohort outcomes from data/sealed/ with EXP8 outcomes.py (year offsets as frozen; field normalisation from the S2 base totals 2012-2024):\n    O2r_m50, O2r_resid, O1c, O1b and O3 at t0+6..t0+8 (O3 peak window t0+3..t0+8; 2017 extension at t0+5..t0+7 with shifted windows);\n    the <= 2022 TAG sensitivity for 2015 onsets (t0+5..t0+7);\n    O4 only if Pass B ran.\n  - Write outcomes_cohort.parquet, hash it into logs/seal.log, and score ONCE (lib/ladder.py):\n    PRIMARY TABLE: for b in {HOME, ALL, SIZEMATCH} x outcome in {O2r_m50, O2r_resid} x rung R0..R5:\n      R0 = B5 + onset-year dummies\n      R1 = R0 + CONTACT_REACH\n      R2 = R1 + type dummies (method/object/property; topic is the reference) + generic flag + level dummies\n      R3 = R2 + fp_logN, fp_nfields, fp_reemerge, fp_wiki_pre, newborn\n      R4 = R3 + venue-label coverage share + home-paper coverage share\n      R5 = R4 + home-group dummies\n      psp = Pearson(resid(rank y | ranks of covariates, dummies), resid(rank OPEN | same)).\n      95% CI = 2,000 concept bootstraps, refitting the residualisation in each draw (percentile). Resampling unit 'concept' is named in every table.\n    PER GROUP (CS+Eng, BGM+Med, PHYS, LIFEENV, SOC; MATHDEC reported only) at R2 and R3 (R5 is undefined within a group): psp, bootstrap SE, DL pooled estimate, tau2, I2, and the sign count.\n    WITHIN TYPE: method-only and object-only subsets at R3 minus the type dummies (plus the property and topic subsets, descriptive).\n    Each of the six components alone at R2 and R3.\n    RETENTION_RATIO_early at R0 (the verdict clause) and at R3.\n    Paired bootstrap of psp(OPEN_all) - psp(OPEN_home) and of psp(OPEN_sizematch) - psp(OPEN_home), both at R3.\n    Holm over the 8-test family {OPEN_home, OPEN_all, OPEN_sizematch, RETENTION_RATIO_early} x {O2r_m50, O2r_resid} at R2 (one-sided bootstrap p in the frozen direction).\n  - VERDICT (frozen text, applied mechanically in code and written to cohort_result.json):\n    CONFIRMED iff all of:\n      - OPEN_home psp on O2r_m50 > 0 with CI > 0 at R2 AND at R3;\n      - O2r_resid has the same sign at R2;\n      - positive point estimate in >= 4 of the 5 groups at R2;\n      - psp > 0 within method AND within object concepts;\n      - RETENTION_RATIO_early psp < 0 given R0.\n    DISCONFIRMED iff the CI of OPEN_home at R2 includes 0.\n    Otherwise PARTIAL, with the failing clauses listed.\n    Named readings, reported as stated:\n      (a) 'type absorbs OPEN': the R1 CI > 0 but the R2 CI includes 0, and the type dummies carry the drop;\n      (b) 'mechanical': the OPEN_home CI includes 0 while the OPEN_all CI > 0; then check SIZEMATCH to say whether it is paper count or home restriction.\n    No subgroup hunting after the unseal; anything else is labelled EXPLORATORY.\n  - SECONDARY (frozen, no refit):\n    - O3 L1-logit (linear_all_O3): dAUC over the frozen B5 logit.\n    - O4 EBM Spearman vs B5 (only if O4 exists).\n    - O2r ElasticNet (linear_all_O2r_m50, linear_all_O2r_resid): Spearman gain over B5.\n    - n_authors_early psp for O3/O1b/O1c.\n    - CONTACT_REACH psp on O2r_m50 and O2r_resid, all concepts and excluding intersection-born.\n    - Missing inputs are imputed at the frozen DEV medians via lib/design.py. A replication is DROPPED and reported 'not evaluable' if more than 20% of |standardised coefficient| mass (linear) or of the mean |term importance| (EBM) sits on fully imputed features.\n    - Paired concept bootstrap CIs (2,000).\n  - PLACEBOS (post-unseal, reported): 200 within-group permutations of O2r_m50 give the null distribution of OPEN_home psp at R2 (expect |psp| < 0.05 for 95%). A planted signal y' = rank(O2r) + 0.10-SD-equivalent * OPEN_home must be recovered with CI > 0.\n\nS10 OUTPUTS.\n  - results/cohort_result.json: every rung x build x outcome x group x type estimate with CI, n and resampling unit; power and MDE; the verdict and the clause table; secondary; placebos; audits S2-T1..T3; the S3 decision; type benchmark metrics; LLM spend.\n  - results/exp5_selection_result.json.\n  - Figures (aii-data-fig-gen or matplotlib, PNG+PDF):\n    fig_ladder.png: psp by rung, the three builds, O2r_m50 and O2r_resid panels;\n    fig_forest_groups.png: per-group psp at R2 with the DL diamond, cohort and EXP5 side by side;\n    fig_components.png;\n    fig_within_type.png;\n    fig_coverage_audit.png: tag_rate and label coverage by year.\n  - full_method_out.json (exp_gen_sol_out): one example per cohort concept.\n    input = concept label + id + t0 + group;\n    output = O2r_m50;\n    predict_B5 = frozen-R0 fitted rank prediction;\n    predict_B5_plus_OPEN_home = R0 + OPEN_home fitted on EXP5 and applied frozen;\n    plus metadata for the OPEN builds, type, footprint and all outcomes.\n    Make the mini/preview variants with aii-json, and split by aii-file-size-limit if needed.\n  - README.md with a 'Restoring removed files' section; .aii/manifest.yaml (keep data/sealed/, the outcome and feature parquets, and concept_types.csv; delete .venv/, __pycache__/ and any raw S3 cache as regenerable with its command); reproducibility.md; results/deviations.json.\n\nTIME PLAN (6 h).\n  - 0:00-0:30 S0 + S1.\n  - 0:30 launch S2 (background).\n  - 0:30-2:30 in parallel: S5 on EXP5 concepts, S6, and S7 EXP5 HOME/SIZEMATCH builds (2-3 procs).\n  - About 2:30 S2 done -> T1-T3, S3, S4, S5 on the cohort, S7 on the cohort.\n  - 3:30-4:00 S8 freeze.\n  - 4:00-4:30 S9 unseal and primary.\n  - 4:30-5:15 secondary, placebos, audit.\n  - 5:15-6:00 S10.\n  DROP ORDER if late: O4/Pass B -> the learned-model replications -> the 2017 extension (only if the S8 rule did not require it; if it did, drop SIZEMATCH for the cohort before dropping 2017). NEVER drop: HOME build, the TYPE rung, the S3 decision, the single unseal.",
  "fallback_plan": "F1 SNAPSHOT CHANGED OR UNREACHABLE. If the S3 manifest differs from EXP5's (a new monthly release), run the pass on the current snapshot and apply the T1 tolerance rule: >= 99% of cells exact and median relative diff < 1% on the 300 controls. If T1 fails, recompute the cohort frame from the NEW pass's own counts (years <= t0+2) instead of agg_counts, and recompute the 300 controls' EXP5 frame membership under the new counts to quantify drift. Log it. Do NOT mix old-snapshot selection features with new-snapshot cohort features for the same concept: the EXP5 features stay old-snapshot, which is fine because they are only used to freeze constants. If S3 is unreachable for more than 30 min, stop and report the artifact as blocked. There is no API fallback (0 credits by design).\n\nF2 PASS TOO SLOW. Projected more than 150 min after 20 files, apply in order: (i) drop referenced_works (O4 goes); (ii) drop authorships for the controls; (iii) emit early rows only for 2015-16 candidates, collecting 2017 candidates' AGG counts but not early rows. The 2017 extension then becomes impossible, and this is logged before S8. (iv) Raise workers to 6 and postpone the EXP5 SIZEMATCH build until after the pass.\n\nF3 LEGACY-TAG COVERAGE COLLAPSES IN 2021-24. Handled by the frozen S3 rule (TAG -> MATCH, validated at rho >= 0.9 on EXP5). If the MATCH validation also fails, the primary outcome becomes the 2015-onset TAG window t0+5..t0+7 (<= 2022), which needs no post-freeze data. 2016 onsets are then scored at t0+4..t0+6 as secondary, and the reduced n goes into the S8 power statement BEFORE the seal.\n\nF4 COHORT TOO SMALL OR UNDERPOWERED. The declared rule adds 2017. If the total is still < 800, run anyway, report the MDE next to every estimate, and make the verdict wording conditional ('underpowered: CI width X'). Never lower the rungs or pool with EXP5 outcomes.\n\nF5 LLM ISSUES. On a 403 budget refusal, stop all queued calls immediately. Concepts without a type label get type = 'unlabelled' (their own dummy) and are excluded from the within-type tests. Concepts without a precision-gate label fall back to the EXP5 sense-filter mean prediction, exactly as EXP5's precision_gate_fallback did, and are flagged. If the benchmark gate fails twice, restrict within-type tests to M1 = M2 agreement concepts (declared).\n\nF6 FROZEN MODELS WILL NOT UNPICKLE (version skew). First recreate EXP8's environment from its lock/reproducibility file. Second, rebuild linear models from the coefficients and intercepts stored in results/learned_model.json / frozen_spec.json, if present. Third, report the replication as 'not evaluable (environment)', never as a null.\n\nF7 HOME-ONLY COVERAGE LOW. If fewer than 60% of cohort concepts have a finite OPEN_home (>= 10 home papers and >= 4 components), keep the primary as declared, but report the B5 profile of included vs excluded concepts and the EXP5 sensitivity at min-papers 5. Do not change the threshold after S8.\n\nF8 TIME. Follow the drop order. The minimum publishable core is S0-S4, the S5 type labels, S7 HOME+ALL, S8 and S9 primary: the ladder for OPEN_home and OPEN_all, groups, within type, RETENTION_RATIO_early.\n\nF9 EGO FLAG TEST FAILS (components with flags off differ from EXP8). Run the original concept_core with n_null = 200 and betweenness cutoff 3 for the HOME build only, on 7 procs, and drop SIZEMATCH to a 5-draw version (declared deviation).",
  "testing_plan": "UNIT AND REPRODUCTION TESTS (before any full run; tests/). U1: make_method_out() on 3 stub rows validates against exp_gen_sol_out with aii-json (the EXP9 failure mode). U2: ego flags. With compute_btw = False and n_null = 0, the six OPEN components on 100 EXP5 concepts equal EXP8 data/ego_features.parquet to 1e-12, and OPEN_all recomputed for 200 EXP5 concepts equals the value built from ego_features.parquet. U3: home filter. For 5 hand-picked concepts (single-home and intersection-born), HOME rows are exactly the rows with vfield in the home set, and the PRE window is filtered too. A synthetic concept whose off-home papers carry all its new topics must show new_edge_rate(HOME) < new_edge_rate(ALL). U4: SIZEMATCH with the subsample size equal to the full count reproduces ALL exactly, and draws are seed-deterministic. U5: rarefied_richness vs Monte Carlo (EXP5 T0 test re-run); O2r_resid with the frozen a/b reproduces EXP8 outcomes.parquet on 200 EXP5 concepts. U6: psp implementation equals EXP8 rq1stats on the EXP8 analysis_table for 3 indicators (1e-10), and the planted psp = 0.10 is recovered on synthetic data with n = 1,000. U7: the seal gate refuses to read data/sealed/ before the freeze, and refuses a second unseal. U8: the precision-gate prompt builder produces byte-identical messages to EXP5 for 20 EXP5 concepts (so the cache hits), which proves the prompt, model and parameters are unchanged.\n\nSTAGED SCALE-UP. Pass: 3 files (inspect rows, dtypes, year range 1995-2024, xpac excluded) -> 20 files (timing extrapolation, T1 on the files' partial counts against EXP5 per-file agg parts if available) -> all 2,040. Ego: 50 concepts -> 500 (time per concept per build) -> all. LLM typing: 40 concepts (inspect JSON parse rate >= 98% and spot-read the labels) -> the 300 benchmark -> all. Cost is checked after each stage against the $3 cap.\n\nCONFIRMATION SIGNALS BEFORE THE SEAL. (i) T1-T3 pass. (ii) The EXP5 selection ladder reproduces the EXP8 single-component signs on O2r_m50 at R0: new_edge_rate +, n_comm_W3 +, participation +, NOV_res +, ego_density_W3 -, edge_persistence -. A sign mismatch at R0 means a pipeline bug: stop and debug, do not re-sign. (iii) The coupling diagnostic shows OPEN_home less correlated with early off-home share than OPEN_all (expected; if not, the home filter is suspect). (iv) The cohort B5 and feature distributions are within the EXP5 range (report standardised mean differences; any |SMD| > 1 is investigated for a bug, not trimmed). (v) Type benchmark gate result recorded. (vi) The power statement is written.\n\nPOST-UNSEAL AUDIT (audit.py, independent code). Re-derive the primary OPEN_home psp at R2 and R3 with statsmodels OLS residuals and scipy rank (target |diff| < 1e-8). Re-derive the DL pooled estimate from per-group estimates by hand. Recompute O2r_m50 for 30 random cohort concepts directly from the sealed agg parts. Run the within-group shuffled-outcome control (200 draws; the 95th percentile of |psp| is reported) and the planted-signal recovery. Record everything in results/audit.json; any failed re-derivation is reported in the README headline, not hidden."
}
```

### [48] TOOL RESULT — Write · 2026-09-29 02:13:13 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Do open-neighbourhood concepts spread? Fresh-cohort test\",\n  \"summary\": \"Single-unseal confirmation of the openness claim (RQ1) on a 2015-2016 onset cohort of OpenAlex legacy concepts that no screen has touched. The frame, grounding and outcomes are the EXP5/EXP8 ones, re-used by path. One zero-credit S3 snapshot pass adds 2015-2024 works for the cohort candidates plus 300 EXP5 control concepts. OPEN (the mean of six signed z-scored ego-network components) is built three ways: ALL-PAPERS, HOME-ONLY and SIZE-MATCHED ALL-PAPERS. It is tested through the ladder B5 -> +CONTACT_REACH -> +CONCEPT TYPE -> +PRE-ONSET FOOTPRINT -> +label coverage -> +home-group FE, within method and within object concepts, per group with DL pooling, and against RETENTION_RATIO_early. Every definition, z constant, covariate and verdict rule is frozen on the 12,499-concept EXP5 frame (selection data only) and hash-sealed before any cohort outcome is read. Two pre-declared, outcome-blind audits guard the measurement: one covers legacy-tag and venue-label coverage in 2021-2024 (OpenAlex froze its legacy concepts, so new works may be untagged), the other is a power check that can trigger the declared 2017 extension. Concept TYPE is LLM-labelled with a 300-concept, two-model benchmark and a 60-item check read by the executor. Secondary: the frozen Exp8 learned models (O3 L1-logit, O4 EBM, O2r ElasticNet) and the n_authors_early and CONTACT_REACH leads, with no refit. Expected LLM spend is about $1.5 (hard cap $3). OpenAlex API credits: 0.\",\n  \"runpod_compute_profile\": \"gpu_basic\",\n  \"domain_practice\": \"WHAT I READ AND CHECKED (bounded; no domain handbook fits: the four offered cover computational linguistics, mechanistic interpretability, multi-agent LLMs and neuro-symbolic AI, so this rests on this run's verified literature (art_dxvRpQufMR0e, art_EesdB8cuSfcU), the EXP5/EXP8 code and READMEs, and targeted lookups). (a) OpenAlex documentation on legacy Concepts (help.openalex.org/data/concepts; developers.openalex.org key-concepts; the Walden launch post). Concepts are deprecated and frozen: 'new works are not tagged with them', and no cut-off date is given. For a 2015-16 cohort whose outcome window is 2021-2024, this is the first measurement threat. EXP5's TAG grounding (title match AND legacy tag score >= 0.3) silently loses recall for works indexed after the freeze. Nobody in the field would accept a breadth or uptake outcome whose grounding recall changes inside the outcome window. (b) Sun & Abraham 2021 (J. Econometrics) and Callaway & Sant'Anna 2021 on staggered event studies. They are NOT used here: within-concept timing belongs to another artifact of this iteration. That boundary is stated so the executor does not drift into RQ2. (c) The EXP8 README (portability table, P1-P5, audits T0-T8, pooled MDE 0.049 at n about 1,800-3,400) and the EXP5 README (frame rules, TAG benchmark P 0.947 / R 0.659, LLM precision gate, seal/unseal machinery).\\n\\nHOW STUDIES OF THIS KIND ARE BUILT IN SCIENTOMETRICS AND SCIENCE OF SCIENCE. (1) BASELINES. Every emergence or diffusion predictor is judged against size and growth: early publication count, growth rate and early breadth (reach, Shannon or Rao-Stirling entropy). Rotolo, Hicks & Martin 2015 give the attribute framing. Cheng et al. 2023 (ASR) control volume and social reach before crediting semantic or structural resonance. Weng, Menczer & Ahn 2013 compare community count against early volume. Uzzi et al. 2013 and Wang, Veugelers & Stephan 2017 compare novelty (new combinations) against field and year baselines. The rival a reviewer names FIRST for our claim is the TYPE of concept: methods and 'research technologies' travel (Leydesdorff & Rafols 2011), and methods dominate citation tops (Van Noorden et al. 2014, 'The top 100 papers'). The second is the concept's pre-existing generic footprint. The fair way to tune such a baseline is to give it the same features, windows and sample as the candidate, fitted on the same selection data, which is what B5 plus the ladder does. (2) DATA. OpenAlex (or WoS or Scopus) works with venue-based field labels. Paper-level topic classifiers are known to be circular for diffusion because they read the paper's own text and references. The legacy MAG/OpenAlex concept vocabulary is a known selection condition: it was seeded from Wikipedia around 2016-19, so concepts born 2015-16 are under-represented relative to earlier cohorts. Temporal out-of-sample cohorts are the accepted confirmation design; examples are citation-forecasting work since Wang, Song & Barabasi 2013, and this run's own EXP5/EXP8 2010-14 cohort. (3) CONTROLS. Volume (hence rarefaction; Hurlbert 1971 and Heck et al. 1975 in diversity ecology), onset year (period effects, measured as onset-year dummies), field or home-group fixed effects, label coverage (venue coverage 26-80%, lowest in conference-heavy CS), and mechanical coupling between predictor and outcome. The last is the one this design is most likely to be caught on: an ego network built on all papers gains off-home topics exactly when the concept spreads off-home. (4) HOW MUCH IS ENOUGH. Concept-level studies in this literature use hundreds to tens of thousands of concepts (Cheng et al. about 60k; EXP8 12.5k). A within-stratum correlation on fewer than about 100 concepts is not believed. Reports give point estimates with bootstrap or analytic 95% CIs, the resampling unit named, heterogeneity across fields (I2 from DerSimonian-Laird 1986 / Higgins & Thompson 2002) and multiplicity control (Holm). This run's EXP8 pooled MDE (2.8 SE) was 0.049 at n about 1,800-3,400. At the expected cohort n of about 1,000-2,000 the pooled MDE is about 0.07-0.09, and within-type strata (about 25-40% of concepts each) have an MDE of about 0.12-0.15. Power has to be computed before the unseal and stated next to the verdict. (5) MEASURES AND REPORTING. Partial Spearman given baseline covariates (rank-residual correlation), incremental AUC or R2 over the baseline for learned models, forest plots per field with a pooled diamond, a ladder figure (estimate by control rung), per-component rows for composite indices, placebos (shuffled outcomes, planted effects), and a statement of the pre-registration and seal. For LLM-derived labels, practice since Gilardi et al. 2023 and Tornberg 2023 is agreement with a human-read gold subset (precision per class, Cohen's kappa between models), with the prompt and model version frozen and published.\",\n  \"practice_alignment\": \"MEETS. (1) Temporal out-of-sample cohort scored once from a sealed spec (EXP5/EXP8 seal.py pattern with a hash chain). (2) The size/growth/breadth baseline B5 plus onset-year dummies. Breadth is volume-adjusted twice (O2r rarefied at m = 50, and O2r_resid with a frozen a/b). (3) The reviewer's first-named confounds are rungs of the ladder: concept type, generic pre-existing footprint, label coverage and home-group FE. (4) Mechanical coupling is attacked by construction: a HOME-ONLY build, plus a SIZE-MATCHED ALL-PAPERS build that separates 'fewer papers' from 'home restriction'. (5) The concept is the resampling unit (2,000 refit bootstraps), with DL pooling and I2 across 5 groups, Holm within the pre-declared 8-test family, and a per-component breakdown of the composite. (6) Placebos: 200 within-group outcome shuffles and a planted psp = 0.10 recovery on the cohort feature matrix. (7) LLM labels are validated against two models and a 60-item gold set, with per-class precision, Wilson CIs, kappa, and the prompt and model hashed.\\n\\nDEPARTURES, AND WHAT EACH COSTS. (a) The concept frame is the legacy OpenAlex concept vocabulary, not an outcome-blind phrase frame (the original Frame N). This is justified because it keeps the grounding identical to the selection data, and a new frame would be a new instrument. The cost: the 2015-16 cohort is conditioned on concepts that MAG/OpenAlex had already named by about 2016-19. Those are likely the more successful newborns, which restricts the range of outcomes and probably attenuates associations. This is stated as a scope limit. (b) The 'hand check' of 60 type labels is read by the executor agent, not a human annotator. This is disclosed. The two-model agreement and the frozen prompt are the checks a reader can re-run. (c) The outcome window runs into 2023-2024, and OpenAlex stopped tagging new works with legacy concepts. The plan does not ignore this. A pre-declared, outcome-blind coverage audit (base-work tag rates per year, and tag/title-match ratios on EXP5 control concepts) chooses the outcome grounding BEFORE the seal: TAG if coverage holds, otherwise title-match grounding (MATCH) for every outcome year, validated on EXP5 selection data (rho >= 0.9 with TAG-based O2r). The TAG-only window of 2015 onsets ending in 2022 is always reported as a sensitivity. What remains: if MATCH is chosen, grounding precision in the outcome window is lower (EXP5 exact-name precision 0.87 against TAG 0.95). The composition-based O2r is robust to uniform precision loss, and O1c is less robust. (d) Venue labels come from the frozen EXP5 source->field map. Sources created after the map miss labels in 2023-24, so O2r is computed on labelled papers only, and yearly label coverage is reported and entered as a covariate. (e) The cohort n (probably about 1,000-2,000) gives a pooled MDE of about 0.07-0.09 and within-type MDEs of about 0.12-0.15. That sits at the edge of the expected OPEN effect: the Exp8 single components were 0.08-0.17, and the composite is probably larger. The plan fixes this with more graded samples, not more metrics. The declared 2017 extension triggers when fewer than 800 concepts pass OR the simulated power of the primary clause is below 0.80. It needs no second pass, because the snapshot pass already collects 2017 candidates. (f) There is only one period-level replication, so period effects cannot be separated from cohort effects. The EXP5 selection-data ladder is reported as a second, non-confirmatory body. (g) O4 (citation growth) needs a citation pass and is the first thing dropped. The O4 EBM replication is then reported as 'not run', never as a null. (h) No human-coded concept-type taxonomy exists for OpenAlex legacy concepts. The 4-class scheme is the direction's own and is not a published standard; this is disclosed. The within-type test uses the method and object classes only.\",\n  \"builds_on\": \"This is a DEEPEN of the EXP8 lead (art_dFQ6jbgNsR6Q), not a fresh line. Everything is re-used BY PATH under the run root /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/ (read-only; copy what is needed into the workspace). Only art_O7Dq4L02QnDN is a declared dependency. If a path is missing, re-implement from the definitions below against the public S3 snapshot and log it in results/deviations.json.\\n\\nEXP5 = iter_2/gen_art/gen_art_experiment_5 (art_wxWssKSUR45f).\\n- results/frame_concepts.csv: 12,499 concepts, SELECTION data.\\n- concept_outcomes.csv, results/frame_summary.json and results/deviations.json: the exact realised early-volume threshold (30, or relaxed 20) and the frame rules.\\n- frame.py: home_rule (>= 40% of the first 30 venue-labelled works, weak >= 25%), split_of/group map, rarefied_richness (exact hypergeometric), concept_outcomes. Imported, not re-written.\\n- scan/agg_counts.parquet: counts per concept x year 1995-2022 x venue field x tagstate x mtype for all 56,643 lexicon concepts. It gives the cohort candidate frame, the footprint, the tag-coverage audit and the MATCH-vs-TAG validation.\\n- scan/year_field_totals.npz, results/source_field.parquet, matcher.py, rangefile.py, scan_full.py (base-work filter), snapshot/works_manifest.json (snapshot identity), snapshot/concepts/part_*.parquet (legacy concept descriptions, level), lexicon_v1.parquet + frozen_lexicon.sha256.\\n- grounding.py: the TAG rule, and cmd_precision with the per-concept LLM gate prompt. M1 = google/gemini-2.5-flash-lite, 10 grounded titles, +10 if 7-8/10 positive, pass at >= 0.8.\\n- llm.py: the OpenRouter client with a disk cache keyed by model+messages, and the usage.cost ledger.\\n- scan/llm_cache/: re-used for any identical call.\\n\\nEXP8 = iter_3/gen_art/gen_art_experiment_8 (art_dFQ6jbgNsR6Q).\\n- passA.py: the template for the new snapshot pass, with the EXP5 matcher and TAG unchanged. It writes BG[year, topic] and early rows (ci, year, work_id, vfield, topic idx list, author ids).\\n- lib/ego.py concept_core: the six OPEN components are new_edge_rate, n_comm_W3, participation, NOV_res (analytic expectation, no null draws), ego_density_W3 and edge_persistence. Windows: PRE = t0-3..t0-1, W1..W3 = t0, t0+1, t0+2. Slice mapping: years > 2014 map to backbone slice2 (2010-14), which is pre-onset for the cohort.\\n- lib/ego_ctx.py (context: inputs/backbone/slice0-2.npz, data/bg_topics.npz covering 1995-2022, inputs/topic_ids.json, topic_meta.csv).\\n- build_features.py and lib/indicators.py: B5, CONTACT_REACH, RETENTION_RATIO_early, n_authors_early, and every input of the frozen models.\\n- outcomes.py: O1c, O1b, O2r_m50, O2r_resid, O3, O4.\\n- results/o2r_resid_fit.json: frozen a/b.\\n- lib/rq1stats.py: partial Spearman with refit bootstrap, DL, Holm.\\n- lib/design.py: frozen imputation and standardisation.\\n- lib/seal.py: the freeze/unseal gate.\\n- data/frame_matches_early/part_*.parquet: EXP5-frame early rows with vfield. The EXP5 HOME-ONLY and SIZE-MATCHED builds come from these, with no new pass.\\n- data/ego_features.parquet: the ALL-PAPERS components for EXP5, used as the reproduction target.\\n- data/features_basic.parquet, data/outcomes.parquet (EXP5 outcomes, selection data).\\n- models/linear_all_O3.joblib, ebm_O4.joblib, linear_all_O2r_m50.joblib, linear_all_O2r_resid.joblib, plus results/learned_model.json, frozen_spec.json and case_exemplars.json.\\n\\nEXP6 = iter_2/gen_art/gen_art_experiment_6: lib/h2.py (D3 ENTERED/RETAINED/LOST states needed by RETENTION_RATIO_early; also copied in EXP8/lib/h2.py).\\n\\nDECLARED DEPENDENCY art_O7Dq4L02QnDN = iter_2/gen_art/gen_art_dataset_2/full_data_out/full_data_out_{1,2,3}.json (concept_recognition). It supplies the Wikipedia creation year (events with source 'wikipedia_en', year_usable true) for the generic-term footprint marker, and the QID and level for joining.\\n\\nNEGATIVE FINDINGS BUILT PAST, and not re-tested. The retained frontier, the abandonment penalty, gateway H1/H3, A*_h, O5 as a validation outcome, and candidate S are all closed. M0_density_end and D_vol_end are excluded from OPEN and from every rung, because they carry a pre-onset footprint. P3's 'new_edge_rate fails' is superseded, since it transferred.\",\n  \"implementation_pseudocode\": \"PROJECT LAYOUT (workspace root W = this artifact's cwd). method.py (orchestrator with --only STEP), lib/ (copied EXP5/EXP8 modules plus new home.py, typing_llm.py, ladder.py), data/, data/sealed/, results/, figures/, logs/, tests/. Python 3.12 via uv. Pin the package versions from the EXP8 environment (read EXP8 reproducibility.md / pyproject / uv.lock), at least scikit-learn, interpret (EBM), joblib, numpy, pandas, pyarrow, python-igraph, leidenalg and pyahocorasick, so the frozen joblib models unpickle. Follow aii-python (loguru), aii-parallel-computing (ProcessPoolExecutor, spawn), aii-long-running-tasks (staged scale-up, background PIDs, never pkill by name) and aii-json (exp_gen_sol_out).\\n\\nS0 PRE-REGISTRATION AND OUTPUT-FORMAT DRY RUN (first 30 min).\\n  - Write prereg.md holding, verbatim: the OPEN definition and signs; the three builds; the ladder rungs and their exact covariates; the groups; the verdict rules; the Holm family; the power/extension trigger; the tag-coverage decision rule; the drop order.\\n  - Write results/frozen_spec_v0.json with the same content machine-readable, plus sha256 of the copied code files. Append sha256(prereg.md + spec_v0) to logs/seal.log with a timestamp. git commit.\\n  - Output-format dry run (EXP9 died in its output loop): write a 3-example stub full_method_out.json in exp_gen_sol_out form and validate it with the aii-json skill NOW. Keep the builder function make_method_out() under unit test (tests/test_output.py) so the final write cannot fail.\\n  FROZEN DEFINITIONS in prereg:\\n    OPEN_b = mean over available k of s_k * (x_k - mu_k,b) / sd_k,b, where\\n      k in {new_edge_rate(+), n_comm_W3(+), participation(+), NOV_res(+), ego_density_W3(-), edge_persistence(-)};\\n      mu and sd are frozen PER BUILD b on all 12,499 EXP5 concepts;\\n      OPEN is NaN unless >= 4 of the 6 are finite.\\n    Winsorise each component at its EXP5 0.5/99.5 percentiles (frozen) before z-scoring.\\n    Builds:\\n      ALL: every grounded early paper, exactly as in EXP8.\\n      HOME: only grounded papers whose venue field is in the concept's home set, applied to BOTH the PRE window and W1-W3. Venue-unlabelled papers are dropped. OPEN_home = NaN if fewer than 10 home papers in t0..t0+2 (declared now; EXP5 sensitivity at 5 and 20).\\n      SIZEMATCH: for each concept, 20 seeded random subsamples (seed = 1000 + ci) of its early papers (PRE and W1-W3 subsampled separately, each to that window's home-only count). Each component is averaged over the 20 draws, then z-scored with SIZEMATCH constants.\\n    Primary outcome: O2r_m50 (rarefied venue-field richness among 50 concept-papers in t0+6..t0+8, exact hypergeometric; NaN if fewer than 50 labelled papers, as in EXP8). Co-outcome: O2r_resid (EXP8 plan formula, frozen a/b from o2r_resid_fit.json).\\n\\nS1 COHORT CANDIDATE FRAME (outcome-blind; uses years <= t0+2 only).\\n  - From EXP5 scan/agg_counts.parquet, compute grounded yearly counts under TAG exactly as frame.py/grounding.grounded_mask does (tagstate 1, plus tagstate 3 gated by the frozen sense-filter pass rate, as EXP5 did).\\n  - t0 = first year in 2000..2017 with >= 20 grounded works. Keep t0 in {2015, 2016, 2017}, early volume (t0..t0+2) >= the EXP5 realised threshold, and ci not in EXP5 frame_concepts.csv. Concepts with t0 <= 2014 are excluded by the rule itself.\\n  - Home and group via frame.home_rule on the first 30 venue-labelled works (years <= t0+2). Newborn flag with the EXP5 rule.\\n  - 2017 rows are FALLBACK candidates only (flag role = 'fallback').\\n  - Write data/cohort_candidates.csv. Log counts by t0 x group. The expected 2015-16 count is roughly 1,000-2,500 before the gate.\\n\\nS2 ONE ZERO-CREDIT SNAPSHOT PASS (passC.py, adapted from EXP8 passA.py). Launch in the background ASAP, with checkpoint files done_XXXX.json so it is resumable.\\n  - Snapshot identity: compare the current S3 works manifest with EXP5 snapshot/works_manifest.json. Log any change to results/deviations.json.\\n  - Base-work filter: identical to EXP5 scan_full.py (article|review, not paratext, not xpac), except the year cap moves 2022 -> 2024.\\n  - Columns: title, publication_year, type, primary_location.source.id, the legacy concepts (id, score), topics (ids), authorships.author.id. referenced_works is read ONLY if O4 will be attempted; decide by the timing of the first 20 files.\\n  - Match the full frozen lexicon (Aho-Corasick + stemmed verification, EXP5 matcher unchanged), but emit rows only for:\\n    (i) cohort candidates incl. 2017, and\\n    (ii) 300 CONTROL concepts sampled from EXP5 frame_concepts.csv (seed 7, stratified by group).\\n  - Outputs per file:\\n    (a) EARLY rows for candidates with t0-3 <= year <= t0+2: ci, year, work_id, vfield, topic idx list, author ids, title (titles only for candidates; needed for the precision gate and type labels), tagstate, mtype.\\n    (b) AGG counts per (ci, year 1995-2024, vfield, tagstate, mtype) for candidates and controls. Rows with year >= t0+3 go to data/sealed/outcome_agg_*.parquet, which is NOT read before the seal; write the sha256 of each part to logs/sealed_files.log.\\n    (c) Base totals per (year 2012-2024, vfield), plus the per-year counts of base works with >= 1 legacy concept tag and with >= 1 tag of score >= 0.3 (outcome-blind coverage audit).\\n    (d) BG[year, topic] for 2012-2018.\\n  - Use 4-5 worker processes (leave 2-3 vCPUs for S4/S5 running concurrently).\\n  - Scale up per aii-long-running-tasks: 3 files -> 20 files -> all. Extrapolate time after 20 files. If the projected pass exceeds 150 min, drop titles and authorships for controls first, then referenced_works.\\n  CHECKS right after the pass, all outcome-blind:\\n    T1: for the 300 controls, yearly TAG counts 1995-2022 must equal agg_counts exactly. For candidates, counts for years <= t0+2 only. Rule: if >= 99% of (concept, year) cells match exactly and the median |rel diff| < 1%, proceed and log the residual; otherwise stop, log, and investigate (snapshot change) before anything else.\\n    T2: BG 2012-2018 equals EXP8 bg_topics.npz on the overlapping years.\\n    T3: base totals 2012-2022 equal EXP5 year_field_totals.\\n\\nS3 OUTCOME-GROUNDING DECISION (outcome-blind; frozen before the seal).\\n  - tag_rate[y] = share of base works with >= 1 legacy tag of score >= 0.3, for y = 2015..2024.\\n  - For the 300 EXP5 controls: ratio[y] = TAG-grounded / title-matched verified hits.\\n  - RULE (declared in S0): if min over y in {2021..2024} of tag_rate[y] / mean(tag_rate[2017..2019]) >= 0.90 AND the same holds for the control ratio, then OUTCOME_GROUNDING = TAG. Otherwise OUTCOME_GROUNDING = MATCH (verified title-match hits, all tagstates, same lexicon, concepts still gated by the LLM precision gate) for ALL outcome years of the cohort.\\n  - If MATCH is chosen, validate it on EXP5 selection data from agg_counts: Spearman(O2r_m50_MATCH, O2r_m50_TAG) at t0+6..t0+8 must be >= 0.90. Refit the O2r_resid a/b for MATCH on EXP5 (frozen). If validation fails, the primary becomes the TAG 2015-onset window t0+5..t0+7 (ending 2022) and the full cohort is secondary.\\n  - Also report the venue-label coverage of base works by year (the share whose source is in source_field.parquet). This enters the coverage rung.\\n\\nS4 LLM PER-CONCEPT PRECISION GATE for the candidates (after S2, which provides the early titles).\\n  - Re-use grounding.cmd_precision logic verbatim: same prompt builder, model google/gemini-2.5-flash-lite, temperature, batch size, 10 titles (+10 if 7-8/10), pass at precision >= 0.8. The llm.py cache and ledger are pointed at W/llm_cache plus a read-only lookup into EXP5 scan/llm_cache.\n  - Expected: about 3,000 candidates at about $0.00017 each, so about $0.5.\\n  - FINAL COHORT = 2015-16 candidates passing the gate. Write cohort_frame.csv (ci, openalex_id, label, t0, home, group, weak_home, intersection_born, newborn, precision_c, role).\\n\\nS5 CONCEPT TYPE (lib/typing_llm.py; runs concurrently with S2 for the EXP5 concepts, and after S4 for the cohort).\\n  - Input per concept: label; the legacy description (EXP5 snapshot/concepts parquet); legacy level; 3 early titles (cohort from S2, EXP5 from the EXP5 reservoir/sample titles; if none, name+description only, flagged).\\n  - Output JSON: {type: method|object|property|topic, generic: 0/1, confidence}. Class definitions in the prompt:\\n    method = technique, tool, algorithm, instrument, assay, software, model class;\\n    object = material, organism, disease, device-as-object, molecule, phenomenon-entity;\\n    property = measure, statistic, theory, law, property;\\n    topic = field or research area.\\n    generic = a term in common scientific use before the concept's onset year (e.g. 'Coefficient of variation', 'Exponential growth').\\n  - Batch 20 concepts per call; model M1 = google/gemini-2.5-flash-lite at temperature 0. About 14.5k-15k concepts, about 750 calls, about $0.6.\\n  - BENCHMARK: 300 concepts stratified by group (50 per group, both frames) are labelled by M2 = openai/gpt-4.1-mini (another family; about $0.1). The executor reads 60 of them (stratified by M1 class) and assigns gold labels blind to the model outputs before comparing.\\n    Metrics: per-class precision of M1 on the 60 gold (Wilson 95% CI), Cohen's kappa M1-vs-M2 on 300, and the method-vs-object confusion.\\n    GATE: M1 precision >= 0.85 for BOTH 'method' and 'object' on the gold set. If it fails, revise the prompt once (definitions and 4 few-shot examples drawn from outside the benchmark), re-label everything, and re-check. If it fails again, the within-type tests use only concepts where M1 = M2 (M2 then labels all concepts in the method/object classes, about $0.5 more), and this is logged.\\n  - Write concept_types.csv (both frames) and type_benchmark.json. Hard LLM cap for the artifact: $3.00, tracked from usage.cost. Stop the batch on the first 'AI Inventor per-run OpenRouter budget' 403 (checked after each semaphore acquire). GET <base_url>/key before starting.\\n\\nS6 PRE-ONSET FOOTPRINT (from agg_counts, years < t0 only; both frames). Write footprint.csv with:\\n  - fp_logN = log1p(grounded papers t0-10..t0-1);\\n  - fp_nfields = number of venue fields with >= 1 grounded paper before t0;\\n  - fp_reemerge = 1 if any pre-t0 year has >= 25% of the t0+2 count (t0+2 <= 2018 for the cohort, hence allowed);\\n  - fp_wiki_pre = 1 if art_O7Dq4L02QnDN has a wikipedia_en creation event with year_usable and year < t0;\\n  - newborn flag;\\n  - legacy level (2-5; kept in the TYPE rung as specificity dummies).\\n\\nS7 FEATURES over t0..t0+2 (and PRE) only. Write data/features_cohort.parquet, data/features_exp5_homeonly.parquet and data/features_exp5_sizematched.parquet.\\n  - Add flags to ego.concept_core: compute_btw=False, n_null=0 (skip D_z/F_res nulls, which are not in OPEN).\\n  - TEST FIRST (tests/t_ego_flags.py): on 100 EXP5 concepts the six components with flags off must equal EXP8 data/ego_features.parquet to 1e-12.\\n  - EXP5 frame (12,499): the HOME build from EXP8 data/frame_matches_early + home sets from frame_concepts.csv; the SIZEMATCH build likewise. ALL = EXP8 ego_features.parquet (re-used, and recomputed for 200 concepts as a check).\\n  - Cohort: ALL, HOME and SIZEMATCH from the S2 early rows. The context is identical to EXP8 (backbone slices; BG from EXP8 bg_topics.npz for years <= 2018, which covers the cohort).\\n  - Cohort basic features via EXP8 build_features functions: B5 (log early volume, early growth, off-home share, entropy, reach), CONTACT_REACH, RETENTION_RATIO_early (EXP6 h2 D3 states from yearly field counts 1995..t0+2: agg_counts plus the S2 early rows), n_authors_early, every input column of the frozen models (from their feature_names_in_ / learned_model.json), home-paper coverage share, venue-label coverage share.\\n  - Parallelise over concepts with ProcessPoolExecutor (spawn, chunks of 200). Log time per 1,000 concepts after the first 500.\\n\\nS8 SELECTION ON THE EXP5 FRAME (selection data; nothing from the cohort's outcome window is read).\\n  (a) Freeze the winsor bounds and z constants per build. Compute OPEN_all, OPEN_home and OPEN_sizematch for the 12,499.\\n  (b) Selection-data results: psp of each OPEN build and each component with O2r_m50 and O2r_resid at every ladder rung (EXP5 outcomes from EXP8 data/outcomes.parquet), per group with DL/I2, and within type. This is the FIRST test of confound (ii) and is reported as selection-data evidence, never as confirmation.\\n  (c) Coupling diagnostic: Spearman of each OPEN build with early off-home share and with log early volume.\\n  (d) Power: subsample the EXP5 frame to the realised cohort n and group mix (1,000 draws), and compute P(CI > 0 at the TYPE rung) for the pooled OPEN_home psp, assuming the true effect equals HALF the EXP5 selection estimate (a conservative shrinkage, cf. EXP5 H3 shrinkage 0.21). Also the MDE, and the within-method and within-object MDEs.\\n      EXTENSION RULE (declared in S0): if the cohort n < 800 OR power < 0.80, add the 2017 candidates that passed the gate (outcome window t0+5..t0+7 = 2022-2024, window flag entered as a covariate with the onset-year dummies). This is decided HERE, before the seal.\\n  (e) Freeze in results/frozen_spec.json: z constants, winsor bounds, OPEN_home min-paper rule, the outcome grounding (S3), O2r_resid a/b, the type labels (hash of concept_types.csv), footprint and covariate lists per rung, the group map, the Holm family, the extension decision, bootstrap seeds (B = 2,000, seed 20260929), the imputation medians for the learned models, and the sha256 of every script and input table (features_cohort.parquet, cohort_frame.csv, concept_types.csv, footprint.csv).\\n  (f) Run the EXP8 lib/seal.py freeze: append the spec hash to logs/seal.log. Pre-unseal checklist: no outcome column in any cohort table, and data/sealed/ untouched (sha256 re-checked against logs/sealed_files.log). git commit.\\n\\nS9 SINGLE UNSEAL.\\n  - seal.unseal() refuses without the matching spec hash and refuses a second call.\\n  - Compute the cohort outcomes from data/sealed/ with EXP8 outcomes.py (year offsets as frozen; field normalisation from the S2 base totals 2012-2024):\\n    O2r_m50, O2r_resid, O1c, O1b and O3 at t0+6..t0+8 (O3 peak window t0+3..t0+8; 2017 extension at t0+5..t0+7 with shifted windows);\\n    the <= 2022 TAG sensitivity for 2015 onsets (t0+5..t0+7);\\n    O4 only if Pass B ran.\\n  - Write outcomes_cohort.parquet, hash it into logs/seal.log, and score ONCE (lib/ladder.py):\\n    PRIMARY TABLE: for b in {HOME, ALL, SIZEMATCH} x outcome in {O2r_m50, O2r_resid} x rung R0..R5:\\n      R0 = B5 + onset-year dummies\\n      R1 = R0 + CONTACT_REACH\\n      R2 = R1 + type dummies (method/object/property; topic is the reference) + generic flag + level dummies\\n      R3 = R2 + fp_logN, fp_nfields, fp_reemerge, fp_wiki_pre, newborn\\n      R4 = R3 + venue-label coverage share + home-paper coverage share\\n      R5 = R4 + home-group dummies\\n      psp = Pearson(resid(rank y | ranks of covariates, dummies), resid(rank OPEN | same)).\\n      95% CI = 2,000 concept bootstraps, refitting the residualisation in each draw (percentile). Resampling unit 'concept' is named in every table.\\n    PER GROUP (CS+Eng, BGM+Med, PHYS, LIFEENV, SOC; MATHDEC reported only) at R2 and R3 (R5 is undefined within a group): psp, bootstrap SE, DL pooled estimate, tau2, I2, and the sign count.\\n    WITHIN TYPE: method-only and object-only subsets at R3 minus the type dummies (plus the property and topic subsets, descriptive).\\n    Each of the six components alone at R2 and R3.\\n    RETENTION_RATIO_early at R0 (the verdict clause) and at R3.\\n    Paired bootstrap of psp(OPEN_all) - psp(OPEN_home) and of psp(OPEN_sizematch) - psp(OPEN_home), both at R3.\\n    Holm over the 8-test family {OPEN_home, OPEN_all, OPEN_sizematch, RETENTION_RATIO_early} x {O2r_m50, O2r_resid} at R2 (one-sided bootstrap p in the frozen direction).\\n  - VERDICT (frozen text, applied mechanically in code and written to cohort_result.json):\\n    CONFIRMED iff all of:\\n      - OPEN_home psp on O2r_m50 > 0 with CI > 0 at R2 AND at R3;\\n      - O2r_resid has the same sign at R2;\\n      - positive point estimate in >= 4 of the 5 groups at R2;\\n      - psp > 0 within method AND within object concepts;\\n      - RETENTION_RATIO_early psp < 0 given R0.\\n    DISCONFIRMED iff the CI of OPEN_home at R2 includes 0.\\n    Otherwise PARTIAL, with the failing clauses listed.\\n    Named readings, reported as stated:\\n      (a) 'type absorbs OPEN': the R1 CI > 0 but the R2 CI includes 0, and the type dummies carry the drop;\\n      (b) 'mechanical': the OPEN_home CI includes 0 while the OPEN_all CI > 0; then check SIZEMATCH to say whether it is paper count or home restriction.\\n    No subgroup hunting after the unseal; anything else is labelled EXPLORATORY.\\n  - SECONDARY (frozen, no refit):\\n    - O3 L1-logit (linear_all_O3): dAUC over the frozen B5 logit.\\n    - O4 EBM Spearman vs B5 (only if O4 exists).\\n    - O2r ElasticNet (linear_all_O2r_m50, linear_all_O2r_resid): Spearman gain over B5.\\n    - n_authors_early psp for O3/O1b/O1c.\\n    - CONTACT_REACH psp on O2r_m50 and O2r_resid, all concepts and excluding intersection-born.\\n    - Missing inputs are imputed at the frozen DEV medians via lib/design.py. A replication is DROPPED and reported 'not evaluable' if more than 20% of |standardised coefficient| mass (linear) or of the mean |term importance| (EBM) sits on fully imputed features.\\n    - Paired concept bootstrap CIs (2,000).\\n  - PLACEBOS (post-unseal, reported): 200 within-group permutations of O2r_m50 give the null distribution of OPEN_home psp at R2 (expect |psp| < 0.05 for 95%). A planted signal y' = rank(O2r) + 0.10-SD-equivalent * OPEN_home must be recovered with CI > 0.\\n\\nS10 OUTPUTS.\\n  - results/cohort_result.json: every rung x build x outcome x group x type estimate with CI, n and resampling unit; power and MDE; the verdict and the clause table; secondary; placebos; audits S2-T1..T3; the S3 decision; type benchmark metrics; LLM spend.\\n  - results/exp5_selection_result.json.\\n  - Figures (aii-data-fig-gen or matplotlib, PNG+PDF):\\n    fig_ladder.png: psp by rung, the three builds, O2r_m50 and O2r_resid panels;\\n    fig_forest_groups.png: per-group psp at R2 with the DL diamond, cohort and EXP5 side by side;\\n    fig_components.png;\\n    fig_within_type.png;\\n    fig_coverage_audit.png: tag_rate and label coverage by year.\\n  - full_method_out.json (exp_gen_sol_out): one example per cohort concept.\\n    input = concept label + id + t0 + group;\\n    output = O2r_m50;\\n    predict_B5 = frozen-R0 fitted rank prediction;\\n    predict_B5_plus_OPEN_home = R0 + OPEN_home fitted on EXP5 and applied frozen;\\n    plus metadata for the OPEN builds, type, footprint and all outcomes.\\n    Make the mini/preview variants with aii-json, and split by aii-file-size-limit if needed.\\n  - README.md with a 'Restoring removed files' section; .aii/manifest.yaml (keep data/sealed/, the outcome and feature parquets, and concept_types.csv; delete .venv/, __pycache__/ and any raw S3 cache as regenerable with its command); reproducibility.md; results/deviations.json.\\n\\nTIME PLAN (6 h).\\n  - 0:00-0:30 S0 + S1.\\n  - 0:30 launch S2 (background).\\n  - 0:30-2:30 in parallel: S5 on EXP5 concepts, S6, and S7 EXP5 HOME/SIZEMATCH builds (2-3 procs).\\n  - About 2:30 S2 done -> T1-T3, S3, S4, S5 on the cohort, S7 on the cohort.\\n  - 3:30-4:00 S8 freeze.\\n  - 4:00-4:30 S9 unseal and primary.\\n  - 4:30-5:15 secondary, placebos, audit.\\n  - 5:15-6:00 S10.\\n  DROP ORDER if late: O4/Pass B -> the learned-model replications -> the 2017 extension (only if the S8 rule did not require it; if it did, drop SIZEMATCH for the cohort before dropping 2017). NEVER drop: HOME build, the TYPE rung, the S3 decision, the single unseal.\",\n  \"fallback_plan\": \"F1 SNAPSHOT CHANGED OR UNREACHABLE. If the S3 manifest differs from EXP5's (a new monthly release), run the pass on the current snapshot and apply the T1 tolerance rule: >= 99% of cells exact and median relative diff < 1% on the 300 controls. If T1 fails, recompute the cohort frame from the NEW pass's own counts (years <= t0+2) instead of agg_counts, and recompute the 300 controls' EXP5 frame membership under the new counts to quantify drift. Log it. Do NOT mix old-snapshot selection features with new-snapshot cohort features for the same concept: the EXP5 features stay old-snapshot, which is fine because they are only used to freeze constants. If S3 is unreachable for more than 30 min, stop and report the artifact as blocked. There is no API fallback (0 credits by design).\\n\\nF2 PASS TOO SLOW. Projected more than 150 min after 20 files, apply in order: (i) drop referenced_works (O4 goes); (ii) drop authorships for the controls; (iii) emit early rows only for 2015-16 candidates, collecting 2017 candidates' AGG counts but not early rows. The 2017 extension then becomes impossible, and this is logged before S8. (iv) Raise workers to 6 and postpone the EXP5 SIZEMATCH build until after the pass.\\n\\nF3 LEGACY-TAG COVERAGE COLLAPSES IN 2021-24. Handled by the frozen S3 rule (TAG -> MATCH, validated at rho >= 0.9 on EXP5). If the MATCH validation also fails, the primary outcome becomes the 2015-onset TAG window t0+5..t0+7 (<= 2022), which needs no post-freeze data. 2016 onsets are then scored at t0+4..t0+6 as secondary, and the reduced n goes into the S8 power statement BEFORE the seal.\\n\\nF4 COHORT TOO SMALL OR UNDERPOWERED. The declared rule adds 2017. If the total is still < 800, run anyway, report the MDE next to every estimate, and make the verdict wording conditional ('underpowered: CI width X'). Never lower the rungs or pool with EXP5 outcomes.\\n\\nF5 LLM ISSUES. On a 403 budget refusal, stop all queued calls immediately. Concepts without a type label get type = 'unlabelled' (their own dummy) and are excluded from the within-type tests. Concepts without a precision-gate label fall back to the EXP5 sense-filter mean prediction, exactly as EXP5's precision_gate_fallback did, and are flagged. If the benchmark gate fails twice, restrict within-type tests to M1 = M2 agreement concepts (declared).\\n\\nF6 FROZEN MODELS WILL NOT UNPICKLE (version skew). First recreate EXP8's environment from its lock/reproducibility file. Second, rebuild linear models from the coefficients and intercepts stored in results/learned_model.json / frozen_spec.json, if present. Third, report the replication as 'not evaluable (environment)', never as a null.\\n\\nF7 HOME-ONLY COVERAGE LOW. If fewer than 60% of cohort concepts have a finite OPEN_home (>= 10 home papers and >= 4 components), keep the primary as declared, but report the B5 profile of included vs excluded concepts and the EXP5 sensitivity at min-papers 5. Do not change the threshold after S8.\\n\\nF8 TIME. Follow the drop order. The minimum publishable core is S0-S4, the S5 type labels, S7 HOME+ALL, S8 and S9 primary: the ladder for OPEN_home and OPEN_all, groups, within type, RETENTION_RATIO_early.\\n\\nF9 EGO FLAG TEST FAILS (components with flags off differ from EXP8). Run the original concept_core with n_null = 200 and betweenness cutoff 3 for the HOME build only, on 7 procs, and drop SIZEMATCH to a 5-draw version (declared deviation).\",\n  \"testing_plan\": \"UNIT AND REPRODUCTION TESTS (before any full run; tests/). U1: make_method_out() on 3 stub rows validates against exp_gen_sol_out with aii-json (the EXP9 failure mode). U2: ego flags. With compute_btw = False and n_null = 0, the six OPEN components on 100 EXP5 concepts equal EXP8 data/ego_features.parquet to 1e-12, and OPEN_all recomputed for 200 EXP5 concepts equals the value built from ego_features.parquet. U3: home filter. For 5 hand-picked concepts (single-home and intersection-born), HOME rows are exactly the rows with vfield in the home set, and the PRE window is filtered too. A synthetic concept whose off-home papers carry all its new topics must show new_edge_rate(HOME) < new_edge_rate(ALL). U4: SIZEMATCH with the subsample size equal to the full count reproduces ALL exactly, and draws are seed-deterministic. U5: rarefied_richness vs Monte Carlo (EXP5 T0 test re-run); O2r_resid with the frozen a/b reproduces EXP8 outcomes.parquet on 200 EXP5 concepts. U6: psp implementation equals EXP8 rq1stats on the EXP8 analysis_table for 3 indicators (1e-10), and the planted psp = 0.10 is recovered on synthetic data with n = 1,000. U7: the seal gate refuses to read data/sealed/ before the freeze, and refuses a second unseal. U8: the precision-gate prompt builder produces byte-identical messages to EXP5 for 20 EXP5 concepts (so the cache hits), which proves the prompt, model and parameters are unchanged.\\n\\nSTAGED SCALE-UP. Pass: 3 files (inspect rows, dtypes, year range 1995-2024, xpac excluded) -> 20 files (timing extrapolation, T1 on the files' partial counts against EXP5 per-file agg parts if available) -> all 2,040. Ego: 50 concepts -> 500 (time per concept per build) -> all. LLM typing: 40 concepts (inspect JSON parse rate >= 98% and spot-read the labels) -> the 300 benchmark -> all. Cost is checked after each stage against the $3 cap.\\n\\nCONFIRMATION SIGNALS BEFORE THE SEAL. (i) T1-T3 pass. (ii) The EXP5 selection ladder reproduces the EXP8 single-component signs on O2r_m50 at R0: new_edge_rate +, n_comm_W3 +, participation +, NOV_res +, ego_density_W3 -, edge_persistence -. A sign mismatch at R0 means a pipeline bug: stop and debug, do not re-sign. (iii) The coupling diagnostic shows OPEN_home less correlated with early off-home share than OPEN_all (expected; if not, the home filter is suspect). (iv) The cohort B5 and feature distributions are within the EXP5 range (report standardised mean differences; any |SMD| > 1 is investigated for a bug, not trimmed). (v) Type benchmark gate result recorded. (vi) The power statement is written.\\n\\nPOST-UNSEAL AUDIT (audit.py, independent code). Re-derive the primary OPEN_home psp at R2 and R3 with statsmodels OLS residuals and scipy rank (target |diff| < 1e-8). Re-derive the DL pooled estimate from per-group estimates by hand. Recompute O2r_m50 for 30 random cohort concepts directly from the sealed agg parts. Run the within-group shuffled-outcome control (200 draws; the 95th percentile of |psp| is reported) and the planted-signal recovery. Record everything in results/audit.json; any failed re-derivation is reported in the README headline, not hidden.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [49] TOOL CALL — Edit · 2026-09-29 02:13:21 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json
OLD: EXP5 scan/llm_cache.
  - Expected:
NEW: EXP5 scan/llm_cache.\n  - Expected:
```

### [50] TOOL RESULT — Edit · 2026-09-29 02:13:21 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json", "oldString": "EXP5 scan/llm_cache.\n  - Expected:", "newString": "EXP5 scan/llm_cache.\\n  - Expected:", "originalFile": null, "structuredPatch": [{"oldStart": 5, "oldLines": 8, "newStart": 5, "newLines": 7, "lines": ["   \"domain_practice\": \"WHAT I READ AND CHECKED (bounded; no domain handbook fits: the four offered cover computational linguistics, mechanistic interpretability, multi-agent LLMs and neuro-symbolic AI, so this rests on this run's verified literature (art_dxvRpQufMR0e, art_EesdB8cuSfcU), the EXP5/EXP8 code and READMEs, and targeted lookups). (a) OpenAlex documentation on legacy Concepts (help.openalex.org/data/concepts; developers.openalex.org key-concepts; the Walden launch post). Concepts are deprecated and frozen: 'new works are not tagged with them', and no cut-off date is given. For a 2015-16 cohort whose outcome window is 2021-2024, this is the first measurement threat. EXP5's TAG grounding (title match AND legacy tag score >= 0.3) silently loses recall for works indexed after the freeze. Nobody in the field would accept a breadth or uptake outcome whose grounding recall changes inside the outcome window. (b) Sun & Abraham 2021 (J. Econometrics) and Callaway & Sant'Anna 2021 on staggered event studies. They are NOT used here: within-concept timing belongs to another artifact of this iteration. That boundary is stated so the executor does not drift into RQ2. (c) The EXP8 README (portability table, P1-P5, audits T0-T8, pooled MDE 0.049 at n about 1,800-3,400) and the EXP5 README (frame rules, TAG benchmark P 0.947 / R 0.659, LLM precision gate, seal/unseal machinery).\\n\\nHOW STUDIES OF THIS KIND ARE BUILT IN SCIENTOMETRICS AND SCIENCE OF SCIENCE. (1) BASELINES. Every emergence or diffusion predictor is judged against size and growth: early publication count, growth rate and early breadth (reach, Shannon or Rao-Stirling entropy). Rotolo, Hicks & Martin 2015 give the attribute framing. Cheng et al. 2023 (ASR) control volume and social reach before crediting semantic or structural resonance. Weng, Menczer & Ahn 2013 compare community count against early volume. Uzzi et al. 2013 and Wang, Veugelers & Stephan 2017 compare novelty (new combinations) against field and year baselines. The rival a reviewer names FIRST for our claim is the TYPE of concept: methods and 'research technologies' travel (Leydesdorff & Rafols 2011), and methods dominate citation tops (Van Noorden et al. 2014, 'The top 100 papers'). The second is the concept's pre-existing generic footprint. The fair way to tune such a baseline is to give it the same features, windows and sample as the candidate, fitted on the same selection data, which is what B5 plus the ladder does. (2) DATA. OpenAlex (or WoS or Scopus) works with venue-based field labels. Paper-level topic classifiers are known to be circular for diffusion because they read the paper's own text and references. The legacy MAG/OpenAlex concept vocabulary is a known selection condition: it was seeded from Wikipedia around 2016-19, so concepts born 2015-16 are under-represented relative to earlier cohorts. Temporal out-of-sample cohorts are the accepted confirmation design; examples are citation-forecasting work since Wang, Song & Barabasi 2013, and this run's own EXP5/EXP8 2010-14 cohort. (3) CONTROLS. Volume (hence rarefaction; Hurlbert 1971 and Heck et al. 1975 in diversity ecology), onset year (period effects, measured as onset-year dummies), field or home-group fixed effects, label coverage (venue coverage 26-80%, lowest in conference-heavy CS), and mechanical coupling between predictor and outcome. The last is the one this design is most likely to be caught on: an ego network built on all papers gains off-home topics exactly when the concept spreads off-home. (4) HOW MUCH IS ENOUGH. Concept-level studies in this literature use hundreds to tens of thousands of concepts (Cheng et al. about 60k; EXP8 12.5k). A within-stratum correlation on fewer than about 100 concepts is not believed. Reports give point estimates with bootstrap or analytic 95% CIs, the resampling unit named, heterogeneity across fields (I2 from DerSimonian-Laird 1986 / Higgins & Thompson 2002) and multiplicity control (Holm). This run's EXP8 pooled MDE (2.8 SE) was 0.049 at n about 1,800-3,400. At the expected cohort n of about 1,000-2,000 the pooled MDE is about 0.07-0.09, and within-type strata (about 25-40% of concepts each) have an MDE of about 0.12-0.15. Power has to be computed before the unseal and stated next to the verdict. (5) MEASURES AND REPORTING. Partial Spearman given baseline covariates (rank-residual correlation), incremental AUC or R2 over the baseline for learned models, forest plots per field with a pooled diamond, a ladder figure (estimate by control rung), per-component rows for composite indices, placebos (shuffled outcomes, planted effects), and a statement of the pre-registration and seal. For LLM-derived labels, practice since Gilardi et al. 2023 and Tornberg 2023 is agreement with a human-read gold subset (precision per class, Cohen's kappa between models), with the prompt and model version frozen and published.\",", "   \"practice_alignment\": \"MEETS. (1) Temporal out-of-sample cohort scored once from a sealed spec (EXP5/EXP8 seal.py pattern with a hash chain). (2) The size/growth/breadth baseline B5 plus onset-year dummies. Breadth is volume-adjusted twice (O2r rarefied at m = 50, and O2r_resid with a frozen a/b). (3) The reviewer's first-named confounds are rungs of the ladder: concept type, generic pre-existing footprint, label coverage and home-group FE. (4) Mechanical coupling is attacked by construction: a HOME-ONLY build, plus a SIZE-MATCHED ALL-PAPERS build that separates 'fewer papers' from 'home restriction'. (5) The concept is the resampling unit (2,000 refit bootstraps), with DL pooling and I2 across 5 groups, Holm within the pre-declared 8-test family, and a per-component breakdown of the composite. (6) Placebos: 200 within-group outcome shuffles and a planted psp = 0.10 recovery on the cohort feature matrix. (7) LLM labels are validated against two models and a 60-item gold set, with per-class precision, Wilson CIs, kappa, and the prompt and model hashed.\\n\\nDEPARTURES, AND WHAT EACH COSTS. (a) The concept frame is the legacy OpenAlex concept vocabulary, not an outcome-blind phrase frame (the original Frame N). This is justified because it keeps the grounding identical to the selection data, and a new frame would be a new instrument. The cost: the 2015-16 cohort is conditioned on concepts that MAG/OpenAlex had already named by about 2016-19. Those are likely the more successful newborns, which restricts the range of outcomes and probably attenuates associations. This is stated as a scope limit. (b) The 'hand check' of 60 type labels is read by the executor agent, not a human annotator. This is disclosed. The two-model agreement and the frozen prompt are the checks a reader can re-run. (c) The outcome window runs into 2023-2024, and OpenAlex stopped tagging new works with legacy concepts. The plan does not ignore this. A pre-declared, outcome-blind coverage audit (base-work tag rates per year, and tag/title-match ratios on EXP5 control concepts) chooses the outcome grounding BEFORE the seal: TAG if coverage holds, otherwise title-match grounding (MATCH) for every outcome year, validated on EXP5 selection data (rho >= 0.9 with TAG-based O2r). The TAG-only window of 2015 onsets ending in 2022 is always reported as a sensitivity. What remains: if MATCH is chosen, grounding precision in the outcome window is lower (EXP5 exact-name precision 0.87 against TAG 0.95). The composition-based O2r is robust to uniform precision loss, and O1c is less robust. (d) Venue labels come from the frozen EXP5 source->field map. Sources created after the map miss labels in 2023-24, so O2r is computed on labelled papers only, and yearly label coverage is reported and entered as a covariate. (e) The cohort n (probably about 1,000-2,000) gives a pooled MDE of about 0.07-0.09 and within-type MDEs of about 0.12-0.15. That sits at the edge of the expected OPEN effect: the Exp8 single components were 0.08-0.17, and the composite is probably larger. The plan fixes this with more graded samples, not more metrics. The declared 2017 extension triggers when fewer than 800 concepts pass OR the simulated power of the primary clause is below 0.80. It needs no second pass, because the snapshot pass already collects 2017 candidates. (f) There is only one period-level replication, so period effects cannot be separated from cohort effects. The EXP5 selection-data ladder is reported as a second, non-confirmatory body. (g) O4 (citation growth) needs a citation pass and is the first thing dropped. The O4 EBM replication is then reported as 'not run', never as a null. (h) No human-coded concept-type taxonomy exists for OpenAlex legacy concepts. The 4-class scheme is the direction's own and is not a published standard; this is disclosed. The within-type test uses the method and object classes only.\",", "   \"builds_on\": \"This is a DEEPEN of the EXP8 lead (art_dFQ6jbgNsR6Q), not a fresh line. Everything is re-used BY PATH under the run root /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/ (read-only; copy what is needed into the workspace). Only art_O7Dq4L02QnDN is a declared dependency. If a path is missing, re-implement from the definitions below against the public S3 snapshot and log it in results/deviations.json.\\n\\nEXP5 = iter_2/gen_art/gen_art_experiment_5 (art_wxWssKSUR45f).\\n- results/frame_concepts.csv: 12,499 concepts, SELECTION data.\\n- concept_outcomes.csv, results/frame_summary.json and results/deviations.json: the exact realised early-volume threshold (30, or relaxed 20) and the frame rules.\\n- frame.py: home_rule (>= 40% of the first 30 venue-labelled works, weak >= 25%), split_of/group map, rarefied_richness (exact hypergeometric), concept_outcomes. Imported, not re-written.\\n- scan/agg_counts.parquet: counts per concept x year 1995-2022 x venue field x tagstate x mtype for all 56,643 lexicon concepts. It gives the cohort candidate frame, the footprint, the tag-coverage audit and the MATCH-vs-TAG validation.\\n- scan/year_field_totals.npz, results/source_field.parquet, matcher.py, rangefile.py, scan_full.py (base-work filter), snapshot/works_manifest.json (snapshot identity), snapshot/concepts/part_*.parquet (legacy concept descriptions, level), lexicon_v1.parquet + frozen_lexicon.sha256.\\n- grounding.py: the TAG rule, and cmd_precision with the per-concept LLM gate prompt. M1 = google/gemini-2.5-flash-lite, 10 grounded titles, +10 if 7-8/10 positive, pass at >= 0.8.\\n- llm.py: the OpenRouter client with a disk cache keyed by model+messages, and the usage.cost ledger.\\n- scan/llm_cache/: re-used for any identical call.\\n\\nEXP8 = iter_3/gen_art/gen_art_experiment_8 (art_dFQ6jbgNsR6Q).\\n- passA.py: the template for the new snapshot pass, with the EXP5 matcher and TAG unchanged. It writes BG[year, topic] and early rows (ci, year, work_id, vfield, topic idx list, author ids).\\n- lib/ego.py concept_core: the six OPEN components are new_edge_rate, n_comm_W3, participation, NOV_res (analytic expectation, no null draws), ego_density_W3 and edge_persistence. Windows: PRE = t0-3..t0-1, W1..W3 = t0, t0+1, t0+2. Slice mapping: years > 2014 map to backbone slice2 (2010-14), which is pre-onset for the cohort.\\n- lib/ego_ctx.py (context: inputs/backbone/slice0-2.npz, data/bg_topics.npz covering 1995-2022, inputs/topic_ids.json, topic_meta.csv).\\n- build_features.py and lib/indicators.py: B5, CONTACT_REACH, RETENTION_RATIO_early, n_authors_early, and every input of the frozen models.\\n- outcomes.py: O1c, O1b, O2r_m50, O2r_resid, O3, O4.\\n- results/o2r_resid_fit.json: frozen a/b.\\n- lib/rq1stats.py: partial Spearman with refit bootstrap, DL, Holm.\\n- lib/design.py: frozen imputation and standardisation.\\n- lib/seal.py: the freeze/unseal gate.\\n- data/frame_matches_early/part_*.parquet: EXP5-frame early rows with vfield. The EXP5 HOME-ONLY and SIZE-MATCHED builds come from these, with no new pass.\\n- data/ego_features.parquet: the ALL-PAPERS components for EXP5, used as the reproduction target.\\n- data/features_basic.parquet, data/outcomes.parquet (EXP5 outcomes, selection data).\\n- models/linear_all_O3.joblib, ebm_O4.joblib, linear_all_O2r_m50.joblib, linear_all_O2r_resid.joblib, plus results/learned_model.json, frozen_spec.json and case_exemplars.json.\\n\\nEXP6 = iter_2/gen_art/gen_art_experiment_6: lib/h2.py (D3 ENTERED/RETAINED/LOST states needed by RETENTION_RATIO_early; also copied in EXP8/lib/h2.py).\\n\\nDECLARED DEPENDENCY art_O7Dq4L02QnDN = iter_2/gen_art/gen_art_dataset_2/full_data_out/full_data_out_{1,2,3}.json (concept_recognition). It supplies the Wikipedia creation year (events with source 'wikipedia_en', year_usable true) for the generic-term footprint marker, and the QID and level for joining.\\n\\nNEGATIVE FINDINGS BUILT PAST, and not re-tested. The retained frontier, the abandonment penalty, gateway H1/H3, A*_h, O5 as a validation outcome, and candidate S are all closed. M0_density_end and D_vol_end are excluded from OPEN and from every rung, because they carry a pre-onset footprint. P3's 'new_edge_rate fails' is superseded, since it transferred.\",", "-  \"implementation_pseudocode\": \"PROJECT LAYOUT (workspace root W = this artifact's cwd). method.py (orchestrator with --only STEP), lib/ (copied EXP5/EXP8 modules plus new home.py, typing_llm.py, ladder.py), data/, data/sealed/, results/, figures/, logs/, tests/. Python 3.12 via uv. Pin the package versions from the EXP8 environment (read EXP8 reproducibility.md / pyproject / uv.lock), at least scikit-learn, interpret (EBM), joblib, numpy, pandas, pyarrow, python-igraph, leidenalg and pyahocorasick, so the frozen joblib models unpickle. Follow aii-python (loguru), aii-parallel-computing (ProcessPoolExecutor, spawn), aii-long-running-tasks (staged scale-up, background PIDs, never pkill by name) and aii-json (exp_gen_sol_out).\\n\\nS0 PRE-REGISTRATION AND OUTPUT-FORMAT DRY RUN (first 30 min).\\n  - Write prereg.md holding, verbatim: the OPEN definition and signs; the three builds; the ladder rungs and their exact covariates; the groups; the verdict rules; the Holm family; the power/extension trigger; the tag-coverage decision rule; the drop order.\\n  - Write results/frozen_spec_v0.json with the same content machine-readable, plus sha256 of the copied code files. Append sha256(prereg.md + spec_v0) to logs/seal.log with a timestamp. git commit.\\n  - Output-format dry run (EXP9 died in its output loop): write a 3-example stub full_method_out.json in exp_gen_sol_out form and validate it with the aii-json skill NOW. Keep the builder function make_method_out() under unit test (tests/test_output.py) so the final write cannot fail.\\n  FROZEN DEFINITIONS in prereg:\\n    OPEN_b = mean over available k of s_k * (x_k - mu_k,b) / sd_k,b, where\\n      k in {new_edge_rate(+), n_comm_W3(+), participation(+), NOV_res(+), ego_density_W3(-), edge_persistence(-)};\\n      mu and sd are frozen PER BUILD b on all 12,499 EXP5 concepts;\\n      OPEN is NaN unless >= 4 of the 6 are finite.\\n    Winsorise each component at its EXP5 0.5/99.5 percentiles (frozen) before z-scoring.\\n    Builds:\\n      ALL: every grounded early paper, exactly as in EXP8.\\n      HOME: only grounded papers whose venue field is in the concept's home set, applied to BOTH the PRE window and W1-W3. Venue-unlabelled papers are dropped. OPEN_home = NaN if fewer than 10 home papers in t0..t0+2 (declared now; EXP5 sensitivity at 5 and 20).\\n      SIZEMATCH: for each concept, 20 seeded random subsamples (seed = 1000 + ci) of its early papers (PRE and W1-W3 subsampled separately, each to that window's home-only count). Each component is averaged over the 20 draws, then z-scored with SIZEMATCH constants.\\n    Primary outcome: O2r_m50 (rarefied venue-field richness among 50 concept-papers in t0+6..t0+8, exact hypergeometric; NaN if fewer than 50 labelled papers, as in EXP8). Co-outcome: O2r_resid (EXP8 plan formula, frozen a/b from o2r_resid_fit.json).\\n\\nS1 COHORT CANDIDATE FRAME (outcome-blind; uses years <= t0+2 only).\\n  - From EXP5 scan/agg_counts.parquet, compute grounded yearly counts under TAG exactly as frame.py/grounding.grounded_mask does (tagstate 1, plus tagstate 3 gated by the frozen sense-filter pass rate, as EXP5 did).\\n  - t0 = first year in 2000..2017 with >= 20 grounded works. Keep t0 in {2015, 2016, 2017}, early volume (t0..t0+2) >= the EXP5 realised threshold, and ci not in EXP5 frame_concepts.csv. Concepts with t0 <= 2014 are excluded by the rule itself.\\n  - Home and group via frame.home_rule on the first 30 venue-labelled works (years <= t0+2). Newborn flag with the EXP5 rule.\\n  - 2017 rows are FALLBACK candidates only (flag role = 'fallback').\\n  - Write data/cohort_candidates.csv. Log counts by t0 x group. The expected 2015-16 count is roughly 1,000-2,500 before the gate.\\n\\nS2 ONE ZERO-CREDIT SNAPSHOT PASS (passC.py, adapted from EXP8 passA.py). Launch in the background ASAP, with checkpoint files done_XXXX.json so it is resumable.\\n  - Snapshot identity: compare the current S3 works manifest with EXP5 snapshot/works_manifest.json. Log any change to results/deviations.json.\\n  - Base-work filter: identical to EXP5 scan_full.py (article|review, not paratext, not xpac), except the year cap moves 2022 -> 2024.\\n  - Columns: title, publication_year, type, primary_location.source.id, the legacy concepts (id, score), topics (ids), authorships.author.id. referenced_works is read ONLY if O4 will be attempted; decide by the timing of the first 20 files.\\n  - Match the full frozen lexicon (Aho-Corasick + stemmed verification, EXP5 matcher unchanged), but emit rows only for:\\n    (i) cohort candidates incl. 2017, and\\n    (ii) 300 CONTROL concepts sampled from EXP5 frame_concepts.csv (seed 7, stratified by group).\\n  - Outputs per file:\\n    (a) EARLY rows for candidates with t0-3 <= year <= t0+2: ci, year, work_id, vfield, topic idx list, author ids, title (titles only for candidates; needed for the precision gate and type labels), tagstate, mtype.\\n    (b) AGG counts per (ci, year 1995-2024, vfield, tagstate, mtype) for candidates and controls. Rows with year >= t0+3 go to data/sealed/outcome_agg_*.parquet, which is NOT read before the seal; write the sha256 of each part to logs/sealed_files.log.\\n    (c) Base totals per (year 2012-2024, vfield), plus the per-year counts of base works with >= 1 legacy concept tag and with >= 1 tag of score >= 0.3 (outcome-blind coverage audit).\\n    (d) BG[year, topic] for 2012-2018.\\n  - Use 4-5 worker processes (leave 2-3 vCPUs for S4/S5 running concurrently).\\n  - Scale up per aii-long-running-tasks: 3 files -> 20 files -> all. Extrapolate time after 20 files. If the projected pass exceeds 150 min, drop titles and authorships for controls first, then referenced_works.\\n  CHECKS right after the pass, all outcome-blind:\\n    T1: for the 300 controls, yearly TAG counts 1995-2022 must equal agg_counts exactly. For candidates, counts for years <= t0+2 only. Rule: if >= 99% of (concept, year) cells match exactly and the median |rel diff| < 1%, proceed and log the residual; otherwise stop, log, and investigate (snapshot change) before anything else.\\n    T2: BG 2012-2018 equals EXP8 bg_topics.npz on the overlapping years.\\n    T3: base totals 2012-2022 equal EXP5 year_field_totals.\\n\\nS3 OUTCOME-GROUNDING DECISION (outcome-blind; frozen before the seal).\\n  - tag_rate[y] = share of base works with >= 1 legacy tag of score >= 0.3, for y = 2015..2024.\\n  - For the 300 EXP5 controls: ratio[y] = TAG-grounded / title-matched verified hits.\\n  - RULE (declared in S0): if min over y in {2021..2024} of tag_rate[y] / mean(tag_rate[2017..2019]) >= 0.90 AND the same holds for the control ratio, then OUTCOME_GROUNDING = TAG. Otherwise OUTCOME_GROUNDING = MATCH (verified title-match hits, all tagstates, same lexicon, concepts still gated by the LLM precision gate) for ALL outcome years of the cohort.\\n  - If MATCH is chosen, validate it on EXP5 selection data from agg_counts: Spearman(O2r_m50_MATCH, O2r_m50_TAG) at t0+6..t0+8 must be >= 0.90. Refit the O2r_resid a/b for MATCH on EXP5 (frozen). If validation fails, the primary becomes the TAG 2015-onset window t0+5..t0+7 (ending 2022) and the full cohort is secondary.\\n  - Also report the venue-label coverage of base works by year (the share whose source is in source_field.parquet). This enters the coverage rung.\\n\\nS4 LLM PER-CONCEPT PRECISION GATE for the candidates (after S2, which provides the early titles).\\n  - Re-use grounding.cmd_precision logic verbatim: same prompt builder, model google/gemini-2.5-flash-lite, temperature, batch size, 10 titles (+10 if 7-8/10), pass at precision >= 0.8. The llm.py cache and ledger are pointed at W/llm_cache plus a read-only lookup into EXP5 scan/llm_cache.", "-  - Expected: about 3,000 candidates at about $0.00017 each, so about $0.5.\\n  - FINAL COHORT = 2015-16 candidates passing the gate. Write cohort_frame.csv (ci, openalex_id, label, t0, home, group, weak_home, intersection_born, newborn, precision_c, role).\\n\\nS5 CONCEPT TYPE (lib/typing_llm.py; runs concurrently with S2 for the EXP5 concepts, and after S4 for the cohort).\\n  - Input per concept: label; the legacy description (EXP5 snapshot/concepts parquet); legacy level; 3 early titles (cohort from S2, EXP5 from the EXP5 reservoir/sample titles; if none, name+description only, flagged).\\n  - Output JSON: {type: method|object|property|topic, generic: 0/1, confidence}. Class definitions in the prompt:\\n    method = technique, tool, algorithm, instrument, assay, software, model class;\\n    object = material, organism, disease, device-as-object, molecule, phenomenon-entity;\\n    property = measure, statistic, theory, law, property;\\n    topic = field or research area.\\n    generic = a term in common scientific use before the concept's onset year (e.g. 'Coefficient of variation', 'Exponential growth').\\n  - Batch 20 concepts per call; model M1 = google/gemini-2.5-flash-lite at temperature 0. About 14.5k-15k concepts, about 750 calls, about $0.6.\\n  - BENCHMARK: 300 concepts stratified by group (50 per group, both frames) are labelled by M2 = openai/gpt-4.1-mini (another family; about $0.1). The executor reads 60 of them (stratified by M1 class) and assigns gold labels blind to the model outputs before comparing.\\n    Metrics: per-class precision of M1 on the 60 gold (Wilson 95% CI), Cohen's kappa M1-vs-M2 on 300, and the method-vs-object confusion.\\n    GATE: M1 precision >= 0.85 for BOTH 'method' and 'object' on the gold set. If it fails, revise the prompt once (definitions and 4 few-shot examples drawn from outside the benchmark), re-label everything, and re-check. If it fails again, the within-type tests use only concepts where M1 = M2 (M2 then labels all concepts in the method/object classes, about $0.5 more), and this is logged.\\n  - Write concept_types.csv (both frames) and type_benchmark.json. Hard LLM cap for the artifact: $3.00, tracked from usage.cost. Stop the batch on the first 'AI Inventor per-run OpenRouter budget' 403 (checked after each semaphore acquire). GET <base_url>/key before starting.\\n\\nS6 PRE-ONSET FOOTPRINT (from agg_counts, years < t0 only; both frames). Write footprint.csv with:\\n  - fp_logN = log1p(grounded papers t0-10..t0-1);\\n  - fp_nfields = number of venue fields with >= 1 grounded paper before t0;\\n  - fp_reemerge = 1 if any pre-t0 year has >= 25% of the t0+2 count (t0+2 <= 2018 for the cohort, hence allowed);\\n  - fp_wiki_pre = 1 if art_O7Dq4L02QnDN has a wikipedia_en creation event with year_usable and year < t0;\\n  - newborn flag;\\n  - legacy level (2-5; kept in the TYPE rung as specificity dummies).\\n\\nS7 FEATURES over t0..t0+2 (and PRE) only. Write data/features_cohort.parquet, data/features_exp5_homeonly.parquet and data/features_exp5_sizematched.parquet.\\n  - Add flags to ego.concept_core: compute_btw=False, n_null=0 (skip D_z/F_res nulls, which are not in OPEN).\\n  - TEST FIRST (tests/t_ego_flags.py): on 100 EXP5 concepts the six components with flags off must equal EXP8 data/ego_features.parquet to 1e-12.\\n  - EXP5 frame (12,499): the HOME build from EXP8 data/frame_matches_early + home sets from frame_concepts.csv; the SIZEMATCH build likewise. ALL = EXP8 ego_features.parquet (re-used, and recomputed for 200 concepts as a check).\\n  - Cohort: ALL, HOME and SIZEMATCH from the S2 early rows. The context is identical to EXP8 (backbone slices; BG from EXP8 bg_topics.npz for years <= 2018, which covers the cohort).\\n  - Cohort basic features via EXP8 build_features functions: B5 (log early volume, early growth, off-home share, entropy, reach), CONTACT_REACH, RETENTION_RATIO_early (EXP6 h2 D3 states from yearly field counts 1995..t0+2: agg_counts plus the S2 early rows), n_authors_early, every input column of the frozen models (from their feature_names_in_ / learned_model.json), home-paper coverage share, venue-label coverage share.\\n  - Parallelise over concepts with ProcessPoolExecutor (spawn, chunks of 200). Log time per 1,000 concepts after the first 500.\\n\\nS8 SELECTION ON THE EXP5 FRAME (selection data; nothing from the cohort's outcome window is read).\\n  (a) Freeze the winsor bounds and z constants per build. Compute OPEN_all, OPEN_home and OPEN_sizematch for the 12,499.\\n  (b) Selection-data results: psp of each OPEN build and each component with O2r_m50 and O2r_resid at every ladder rung (EXP5 outcomes from EXP8 data/outcomes.parquet), per group with DL/I2, and within type. This is the FIRST test of confound (ii) and is reported as selection-data evidence, never as confirmation.\\n  (c) Coupling diagnostic: Spearman of each OPEN build with early off-home share and with log early volume.\\n  (d) Power: subsample the EXP5 frame to the realised cohort n and group mix (1,000 draws), and compute P(CI > 0 at the TYPE rung) for the pooled OPEN_home psp, assuming the true effect equals HALF the EXP5 selection estimate (a conservative shrinkage, cf. EXP5 H3 shrinkage 0.21). Also the MDE, and the within-method and within-object MDEs.\\n      EXTENSION RULE (declared in S0): if the cohort n < 800 OR power < 0.80, add the 2017 candidates that passed the gate (outcome window t0+5..t0+7 = 2022-2024, window flag entered as a covariate with the onset-year dummies). This is decided HERE, before the seal.\\n  (e) Freeze in results/frozen_spec.json: z constants, winsor bounds, OPEN_home min-paper rule, the outcome grounding (S3), O2r_resid a/b, the type labels (hash of concept_types.csv), footprint and covariate lists per rung, the group map, the Holm family, the extension decision, bootstrap seeds (B = 2,000, seed 20260929), the imputation medians for the learned models, and the sha256 of every script and input table (features_cohort.parquet, cohort_frame.csv, concept_types.csv, footprint.csv).\\n  (f) Run the EXP8 lib/seal.py freeze: append the spec hash to logs/seal.log. Pre-unseal checklist: no outcome column in any cohort table, and data/sealed/ untouched (sha256 re-checked against logs/sealed_files.log). git commit.\\n\\nS9 SINGLE UNSEAL.\\n  - seal.unseal() refuses without the matching spec hash and refuses a second call.\\n  - Compute the cohort outcomes from data/sealed/ with EXP8 outcomes.py (year offsets as frozen; field normalisation from the S2 base totals 2012-2024):\\n    O2r_m50, O2r_resid, O1c, O1b and O3 at t0+6..t0+8 (O3 peak window t0+3..t0+8; 2017 extension at t0+5..t0+7 with shifted windows);\\n    the <= 2022 TAG sensitivity for 2015 onsets (t0+5..t0+7);\\n    O4 only if Pass B ran.\\n  - Write outcomes_cohort.parquet, hash it into logs/seal.log, and score ONCE (lib/ladder.py):\\n    PRIMARY TABLE: for b in {HOME, ALL, SIZEMATCH} x outcome in {O2r_m50, O2r_resid} x rung R0..R5:\\n      R0 = B5 + onset-year dummies\\n      R1 = R0 + CONTACT_REACH\\n      R2 = R1 + type dummies (method/object/property; topic is the reference) + generic flag + level dummies\\n      R3 = R2 + fp_logN, fp_nfields, fp_reemerge, fp_wiki_pre, newborn\\n      R4 = R3 + venue-label coverage share + home-paper coverage share\\n      R5 = R4 + home-group dummies\\n      psp = Pearson(resid(rank y | ranks of covariates, dummies), resid(rank OPEN | same)).\\n      95% CI = 2,000 concept bootstraps, refitting the residualisation in each draw (percentile). Resampling unit 'concept' is named in every table.\\n    PER GROUP (CS+Eng, BGM+Med, PHYS, LIFEENV, SOC; MATHDEC reported only) at R2 and R3 (R5 is undefined within a group): psp, bootstrap SE, DL pooled estimate, tau2, I2, and the sign count.\\n    WITHIN TYPE: method-only and object-only subsets at R3 minus the type dummies (plus the property and topic subsets, descriptive).\\n    Each of the six components alone at R2 and R3.\\n    RETENTION_RATIO_early at R0 (the verdict clause) and at R3.\\n    Paired bootstrap of psp(OPEN_all) - psp(OPEN_home) and of psp(OPEN_sizematch) - psp(OPEN_home), both at R3.\\n    Holm over the 8-test family {OPEN_home, OPEN_all, OPEN_sizematch, RETENTION_RATIO_early} x {O2r_m50, O2r_resid} at R2 (one-sided bootstrap p in the frozen direction).\\n  - VERDICT (frozen text, applied mechanically in code and written to cohort_result.json):\\n    CONFIRMED iff all of:\\n      - OPEN_home psp on O2r_m50 > 0 with CI > 0 at R2 AND at R3;\\n      - O2r_resid has the same sign at R2;\\n      - positive point estimate in >= 4 of the 5 groups at R2;\\n      - psp > 0 within method AND within object concepts;\\n      - RETENTION_RATIO_early psp < 0 given R0.\\n    DISCONFIRMED iff the CI of OPEN_home at R2 includes 0.\\n    Otherwise PARTIAL, with the failing clauses listed.\\n    Named readings, reported as stated:\\n      (a) 'type absorbs OPEN': the R1 CI > 0 but the R2 CI includes 0, and the type dummies carry the drop;\\n      (b) 'mechanical': the OPEN_home CI includes 0 while the OPEN_all CI > 0; then check SIZEMATCH to say whether it is paper count or home restriction.\\n    No subgroup hunting after the unseal; anything else is labelled EXPLORATORY.\\n  - SECONDARY (frozen, no refit):\\n    - O3 L1-logit (linear_all_O3): dAUC over the frozen B5 logit.\\n    - O4 EBM Spearman vs B5 (only if O4 exists).\\n    - O2r ElasticNet (linear_all_O2r_m50, linear_all_O2r_resid): Spearman gain over B5.\\n    - n_authors_early psp for O3/O1b/O1c.\\n    - CONTACT_REACH psp on O2r_m50 and O2r_resid, all concepts and excluding intersection-born.\\n    - Missing inputs are imputed at the frozen DEV medians via lib/design.py. A replication is DROPPED and reported 'not evaluable' if more than 20% of |standardised coefficient| mass (linear) or of the mean |term importance| (EBM) sits on fully imputed features.\\n    - Paired concept bootstrap CIs (2,000).\\n  - PLACEBOS (post-unseal, reported): 200 within-group permutations of O2r_m50 give the null distribution of OPEN_home psp at R2 (expect |psp| < 0.05 for 95%). A planted signal y' = rank(O2r) + 0.10-SD-equivalent * OPEN_home must be recovered with CI > 0.\\n\\nS10 OUTPUTS.\\n  - results/cohort_result.json: every rung x build x outcome x group x type estimate with CI, n and resampling unit; power and MDE; the verdict and the clause table; secondary; placebos; audits S2-T1..T3; the S3 decision; type benchmark metrics; LLM spend.\\n  - results/exp5_selection_result.json.\\n  - Figures (aii-data-fig-gen or matplotlib, PNG+PDF):\\n    fig_ladder.png: psp by rung, the three builds, O2r_m50 and O2r_resid panels;\\n    fig_forest_groups.png: per-group psp at R2 with the DL diamond, cohort and EXP5 side by side;\\n    fig_components.png;\\n    fig_within_type.png;\\n    fig_coverage_audit.png: tag_rate and label coverage by year.\\n  - full_method_out.json (exp_gen_sol_out): one example per cohort concept.\\n    input = concept label + id + t0 + group;\\n    output = O2r_m50;\\n    predict_B5 = frozen-R0 fitted rank prediction;\\n    predict_B5_plus_OPEN_home = R0 + OPEN_home fitted on EXP5 and applied frozen;\\n    plus metadata for the OPEN builds, type, footprint and all outcomes.\\n    Make the mini/preview variants with aii-json, and split by aii-file-size-limit if needed.\\n  - README.md with a 'Restoring removed files' section; .aii/manifest.yaml (keep data/sealed/, the outcome and feature parquets, and concept_types.csv; delete .venv/, __pycache__/ and any raw S3 cache as regenerable with its command); reproducibility.md; results/deviations.json.\\n\\nTIME PLAN (6 h).\\n  - 0:00-0:30 S0 + S1.\\n  - 0:30 launch S2 (background).\\n  - 0:30-2:30 in parallel: S5 on EXP5 concepts, S6, and S7 EXP5 HOME/SIZEMATCH builds (2-3 procs).\\n  - About 2:30 S2 done -> T1-T3, S3, S4, S5 on the cohort, S7 on the cohort.\\n  - 3:30-4:00 S8 freeze.\\n  - 4:00-4:30 S9 unseal and primary.\\n  - 4:30-5:15 secondary, placebos, audit.\\n  - 5:15-6:00 S10.\\n  DROP ORDER if late: O4/Pass B -> the learned-model replications -> the 2017 extension (only if the S8 rule did not require it; if it did, drop SIZEMATCH for the cohort before dropping 2017). NEVER drop: HOME build, the TYPE rung, the S3 decision, the single unseal.\",", "+  \"implementation_pseudocode\": \"PROJECT LAYOUT (workspace root W = this artifact's cwd). method.py (orchestrator with --only STEP), lib/ (copied EXP5/EXP8 modules plus new home.py, typing_llm.py, ladder.py), data/, data/sealed/, results/, figures/, logs/, tests/. Python 3.12 via uv. Pin the package versions from the EXP8 environment (read EXP8 reproducibility.md / pyproject / uv.lock), at least scikit-learn, interpret (EBM), joblib, numpy, pandas, pyarrow, python-igraph, leidenalg and pyahocorasick, so the frozen joblib models unpickle. Follow aii-python (loguru), aii-parallel-computing (ProcessPoolExecutor, spawn), aii-long-running-tasks (staged scale-up, background PIDs, never pkill by name) and aii-json (exp_gen_sol_out).\\n\\nS0 PRE-REGISTRATION AND OUTPUT-FORMAT DRY RUN (first 30 min).\\n  - Write prereg.md holding, verbatim: the OPEN definition and signs; the three builds; the ladder rungs and their exact covariates; the groups; the verdict rules; the Holm family; the power/extension trigger; the tag-coverage decision rule; the drop order.\\n  - Write results/frozen_spec_v0.json with the same content machine-readable, plus sha256 of the copied code files. Append sha256(prereg.md + spec_v0) to logs/seal.log with a timestamp. git commit.\\n  - Output-format dry run (EXP9 died in its output loop): write a 3-example stub full_method_out.json in exp_gen_sol_out form and validate it with the aii-json skill NOW. Keep the builder function make_method_out() under unit test (tests/test_output.py) so the final write cannot fail.\\n  FROZEN DEFINITIONS in prereg:\\n    OPEN_b = mean over available k of s_k * (x_k - mu_k,b) / sd_k,b, where\\n      k in {new_edge_rate(+), n_comm_W3(+), participation(+), NOV_res(+), ego_density_W3(-), edge_persistence(-)};\\n      mu and sd are frozen PER BUILD b on all 12,499 EXP5 concepts;\\n      OPEN is NaN unless >= 4 of the 6 are finite.\\n    Winsorise each component at its EXP5 0.5/99.5 percentiles (frozen) before z-scoring.\\n    Builds:\\n      ALL: every grounded early paper, exactly as in EXP8.\\n      HOME: only grounded papers whose venue field is in the concept's home set, applied to BOTH the PRE window and W1-W3. Venue-unlabelled papers are dropped. OPEN_home = NaN if fewer than 10 home papers in t0..t0+2 (declared now; EXP5 sensitivity at 5 and 20).\\n      SIZEMATCH: for each concept, 20 seeded random subsamples (seed = 1000 + ci) of its early papers (PRE and W1-W3 subsampled separately, each to that window's home-only count). Each component is averaged over the 20 draws, then z-scored with SIZEMATCH constants.\\n    Primary outcome: O2r_m50 (rarefied venue-field richness among 50 concept-papers in t0+6..t0+8, exact hypergeometric; NaN if fewer than 50 labelled papers, as in EXP8). Co-outcome: O2r_resid (EXP8 plan formula, frozen a/b from o2r_resid_fit.json).\\n\\nS1 COHORT CANDIDATE FRAME (outcome-blind; uses years <= t0+2 only).\\n  - From EXP5 scan/agg_counts.parquet, compute grounded yearly counts under TAG exactly as frame.py/grounding.grounded_mask does (tagstate 1, plus tagstate 3 gated by the frozen sense-filter pass rate, as EXP5 did).\\n  - t0 = first year in 2000..2017 with >= 20 grounded works. Keep t0 in {2015, 2016, 2017}, early volume (t0..t0+2) >= the EXP5 realised threshold, and ci not in EXP5 frame_concepts.csv. Concepts with t0 <= 2014 are excluded by the rule itself.\\n  - Home and group via frame.home_rule on the first 30 venue-labelled works (years <= t0+2). Newborn flag with the EXP5 rule.\\n  - 2017 rows are FALLBACK candidates only (flag role = 'fallback').\\n  - Write data/cohort_candidates.csv. Log counts by t0 x group. The expected 2015-16 count is roughly 1,000-2,500 before the gate.\\n\\nS2 ONE ZERO-CREDIT SNAPSHOT PASS (passC.py, adapted from EXP8 passA.py). Launch in the background ASAP, with checkpoint files done_XXXX.json so it is resumable.\\n  - Snapshot identity: compare the current S3 works manifest with EXP5 snapshot/works_manifest.json. Log any change to results/deviations.json.\\n  - Base-work filter: identical to EXP5 scan_full.py (article|review, not paratext, not xpac), except the year cap moves 2022 -> 2024.\\n  - Columns: title, publication_year, type, primary_location.source.id, the legacy concepts (id, score), topics (ids), authorships.author.id. referenced_works is read ONLY if O4 will be attempted; decide by the timing of the first 20 files.\\n  - Match the full frozen lexicon (Aho-Corasick + stemmed verification, EXP5 matcher unchanged), but emit rows only for:\\n    (i) cohort candidates incl. 2017, and\\n    (ii) 300 CONTROL concepts sampled from EXP5 frame_concepts.csv (seed 7, stratified by group).\\n  - Outputs per file:\\n    (a) EARLY rows for candidates with t0-3 <= year <= t0+2: ci, year, work_id, vfield, topic idx list, author ids, title (titles only for candidates; needed for the precision gate and type labels), tagstate, mtype.\\n    (b) AGG counts per (ci, year 1995-2024, vfield, tagstate, mtype) for candidates and controls. Rows with year >= t0+3 go to data/sealed/outcome_agg_*.parquet, which is NOT read before the seal; write the sha256 of each part to logs/sealed_files.log.\\n    (c) Base totals per (year 2012-2024, vfield), plus the per-year counts of base works with >= 1 legacy concept tag and with >= 1 tag of score >= 0.3 (outcome-blind coverage audit).\\n    (d) BG[year, topic] for 2012-2018.\\n  - Use 4-5 worker processes (leave 2-3 vCPUs for S4/S5 running concurrently).\\n  - Scale up per aii-long-running-tasks: 3 files -> 20 files -> all. Extrapolate time after 20 files. If the projected pass exceeds 150 min, drop titles and authorships for controls first, then referenced_works.\\n  CHECKS right after the pass, all outcome-blind:\\n    T1: for the 300 controls, yearly TAG counts 1995-2022 must equal agg_counts exactly. For candidates, counts for years <= t0+2 only. Rule: if >= 99% of (concept, year) cells match exactly and the median |rel diff| < 1%, proceed and log the residual; otherwise stop, log, and investigate (snapshot change) before anything else.\\n    T2: BG 2012-2018 equals EXP8 bg_topics.npz on the overlapping years.\\n    T3: base totals 2012-2022 equal EXP5 year_field_totals.\\n\\nS3 OUTCOME-GROUNDING DECISION (outcome-blind; frozen before the seal).\\n  - tag_rate[y] = share of base works with >= 1 legacy tag of score >= 0.3, for y = 2015..2024.\\n  - For the 300 EXP5 controls: ratio[y] = TAG-grounded / title-matched verified hits.\\n  - RULE (declared in S0): if min over y in {2021..2024} of tag_rate[y] / mean(tag_rate[2017..2019]) >= 0.90 AND the same holds for the control ratio, then OUTCOME_GROUNDING = TAG. Otherwise OUTCOME_GROUNDING = MATCH (verified title-match hits, all tagstates, same lexicon, concepts still gated by the LLM precision gate) for ALL outcome years of the cohort.\\n  - If MATCH is chosen, validate it on EXP5 selection data from agg_counts: Spearman(O2r_m50_MATCH, O2r_m50_TAG) at t0+6..t0+8 must be >= 0.90. Refit the O2r_resid a/b for MATCH on EXP5 (frozen). If validation fails, the primary becomes the TAG 2015-onset window t0+5..t0+7 (ending 2022) and the full cohort is secondary.\\n  - Also report the venue-label coverage of base works by year (the share whose source is in source_field.parquet). This enters the coverage rung.\\n\\nS4 LLM PER-CONCEPT PRECISION GATE for the candidates (after S2, which provides the early titles).\\n  - Re-use grounding.cmd_precision logic verbatim: same prompt builder, model google/gemini-2.5-flash-lite, temperature, batch size, 10 titles (+10 if 7-8/10), pass at precision >= 0.8. The llm.py cache and ledger are pointed at W/llm_cache plus a read-only lookup into EXP5 scan/llm_cache.\\n  - Expected: about 3,000 candidates at about $0.00017 each, so about $0.5.\\n  - FINAL COHORT = 2015-16 candidates passing the gate. Write cohort_frame.csv (ci, openalex_id, label, t0, home, group, weak_home, intersection_born, newborn, precision_c, role).\\n\\nS5 CONCEPT TYPE (lib/typing_llm.py; runs concurrently with S2 for the EXP5 concepts, and after S4 for the cohort).\\n  - Input per concept: label; the legacy description (EXP5 snapshot/concepts parquet); legacy level; 3 early titles (cohort from S2, EXP5 from the EXP5 reservoir/sample titles; if none, name+description only, flagged).\\n  - Output JSON: {type: method|object|property|topic, generic: 0/1, confidence}. Class definitions in the prompt:\\n    method = technique, tool, algorithm, instrument, assay, software, model class;\\n    object = material, organism, disease, device-as-object, molecule, phenomenon-entity;\\n    property = measure, statistic, theory, law, property;\\n    topic = field or research area.\\n    generic = a term in common scientific use before the concept's onset year (e.g. 'Coefficient of variation', 'Exponential growth').\\n  - Batch 20 concepts per call; model M1 = google/gemini-2.5-flash-lite at temperature 0. About 14.5k-15k concepts, about 750 calls, about $0.6.\\n  - BENCHMARK: 300 concepts stratified by group (50 per group, both frames) are labelled by M2 = openai/gpt-4.1-mini (another family; about $0.1). The executor reads 60 of them (stratified by M1 class) and assigns gold labels blind to the model outputs before comparing.\\n    Metrics: per-class precision of M1 on the 60 gold (Wilson 95% CI), Cohen's kappa M1-vs-M2 on 300, and the method-vs-object confusion.\\n    GATE: M1 precision >= 0.85 for BOTH 'method' and 'object' on the gold set. If it fails, revise the prompt once (definitions and 4 few-shot examples drawn from outside the benchmark), re-label everything, and re-check. If it fails again, the within-type tests use only concepts where M1 = M2 (M2 then labels all concepts in the method/object classes, about $0.5 more), and this is logged.\\n  - Write concept_types.csv (both frames) and type_benchmark.json. Hard LLM cap for the artifact: $3.00, tracked from usage.cost. Stop the batch on the first 'AI Inventor per-run OpenRouter budget' 403 (checked after each semaphore acquire). GET <base_url>/key before starting.\\n\\nS6 PRE-ONSET FOOTPRINT (from agg_counts, years < t0 only; both frames). Write footprint.csv with:\\n  - fp_logN = log1p(grounded papers t0-10..t0-1);\\n  - fp_nfields = number of venue fields with >= 1 grounded paper before t0;\\n  - fp_reemerge = 1 if any pre-t0 year has >= 25% of the t0+2 count (t0+2 <= 2018 for the cohort, hence allowed);\\n  - fp_wiki_pre = 1 if art_O7Dq4L02QnDN has a wikipedia_en creation event with year_usable and year < t0;\\n  - newborn flag;\\n  - legacy level (2-5; kept in the TYPE rung as specificity dummies).\\n\\nS7 FEATURES over t0..t0+2 (and PRE) only. Write data/features_cohort.parquet, data/features_exp5_homeonly.parquet and data/features_exp5_sizematched.parquet.\\n  - Add flags to ego.concept_core: compute_btw=False, n_null=0 (skip D_z/F_res nulls, which are not in OPEN).\\n  - TEST FIRST (tests/t_ego_flags.py): on 100 EXP5 concepts the six components with flags off must equal EXP8 data/ego_features.parquet to 1e-12.\\n  - EXP5 frame (12,499): the HOME build from EXP8 data/frame_matches_early + home sets from frame_concepts.csv; the SIZEMATCH build likewise. ALL = EXP8 ego_features.parquet (re-used, and recomputed for 200 concepts as a check).\\n  - Cohort: ALL, HOME and SIZEMATCH from the S2 early rows. The context is identical to EXP8 (backbone slices; BG from EXP8 bg_topics.npz for years <= 2018, which covers the cohort).\\n  - Cohort basic features via EXP8 build_features functions: B5 (log early volume, early growth, off-home share, entropy, reach), CONTACT_REACH, RETENTION_RATIO_early (EXP6 h2 D3 states from yearly field counts 1995..t0+2: agg_counts plus the S2 early rows), n_authors_early, every input column of the frozen models (from their feature_names_in_ / learned_model.json), home-paper coverage share, venue-label coverage share.\\n  - Parallelise over concepts with ProcessPoolExecutor (spawn, chunks of 200). Log time per 1,000 concepts after the first 500.\\n\\nS8 SELECTION ON THE EXP5 FRAME (selection data; nothing from the cohort's outcome window is read).\\n  (a) Freeze the winsor bounds and z constants per build. Compute OPEN_all, OPEN_home and OPEN_sizematch for the 12,499.\\n  (b) Selection-data results: psp of each OPEN build and each component with O2r_m50 and O2r_resid at every ladder rung (EXP5 outcomes from EXP8 data/outcomes.parquet), per group with DL/I2, and within type. This is the FIRST test of confound (ii) and is reported as selection-data evidence, never as confirmation.\\n  (c) Coupling diagnostic: Spearman of each OPEN build with early off-home share and with log early volume.\\n  (d) Power: subsample the EXP5 frame to the realised cohort n and group mix (1,000 draws), and compute P(CI > 0 at the TYPE rung) for the pooled OPEN_home psp, assuming the true effect equals HALF the EXP5 selection estimate (a conservative shrinkage, cf. EXP5 H3 shrinkage 0.21). Also the MDE, and the within-method and within-object MDEs.\\n      EXTENSION RULE (declared in S0): if the cohort n < 800 OR power < 0.80, add the 2017 candidates that passed the gate (outcome window t0+5..t0+7 = 2022-2024, window flag entered as a covariate with the onset-year dummies). This is decided HERE, before the seal.\\n  (e) Freeze in results/frozen_spec.json: z constants, winsor bounds, OPEN_home min-paper rule, the outcome grounding (S3), O2r_resid a/b, the type labels (hash of concept_types.csv), footprint and covariate lists per rung, the group map, the Holm family, the extension decision, bootstrap seeds (B = 2,000, seed 20260929), the imputation medians for the learned models, and the sha256 of every script and input table (features_cohort.parquet, cohort_frame.csv, concept_types.csv, footprint.csv).\\n  (f) Run the EXP8 lib/seal.py freeze: append the spec hash to logs/seal.log. Pre-unseal checklist: no outcome column in any cohort table, and data/sealed/ untouched (sha256 re-checked against logs/sealed_files.log). git commit.\\n\\nS9 SINGLE UNSEAL.\\n  - seal.unseal() refuses without the matching spec hash and refuses a second call.\\n  - Compute the cohort outcomes from data/sealed/ with EXP8 outcomes.py (year offsets as frozen; field normalisation from the S2 base totals 2012-2024):\\n    O2r_m50, O2r_resid, O1c, O1b and O3 at t0+6..t0+8 (O3 peak window t0+3..t0+8; 2017 extension at t0+5..t0+7 with shifted windows);\\n    the <= 2022 TAG sensitivity for 2015 onsets (t0+5..t0+7);\\n    O4 only if Pass B ran.\\n  - Write outcomes_cohort.parquet, hash it into logs/seal.log, and score ONCE (lib/ladder.py):\\n    PRIMARY TABLE: for b in {HOME, ALL, SIZEMATCH} x outcome in {O2r_m50, O2r_resid} x rung R0..R5:\\n      R0 = B5 + onset-year dummies\\n      R1 = R0 + CONTACT_REACH\\n      R2 = R1 + type dummies (method/object/property; topic is the reference) + generic flag + level dummies\\n      R3 = R2 + fp_logN, fp_nfields, fp_reemerge, fp_wiki_pre, newborn\\n      R4 = R3 + venue-label coverage share + home-paper coverage share\\n      R5 = R4 + home-group dummies\\n      psp = Pearson(resid(rank y | ranks of covariates, dummies), resid(rank OPEN | same)).\\n      95% CI = 2,000 concept bootstraps, refitting the residualisation in each draw (percentile). Resampling unit 'concept' is named in every table.\\n    PER GROUP (CS+Eng, BGM+Med, PHYS, LIFEENV, SOC; MATHDEC reported only) at R2 and R3 (R5 is undefined within a group): psp, bootstrap SE, DL pooled estimate, tau2, I2, and the sign count.\\n    WITHIN TYPE: method-only and object-only subsets at R3 minus the type dummies (plus the property and topic subsets, descriptive).\\n    Each of the six components alone at R2 and R3.\\n    RETENTION_RATIO_early at R0 (the verdict clause) and at R3.\\n    Paired bootstrap of psp(OPEN_all) - psp(OPEN_home) and of psp(OPEN_sizematch) - psp(OPEN_home), both at R3.\\n    Holm over the 8-test family {OPEN_home, OPEN_all, OPEN_sizematch, RETENTION_RATIO_early} x {O2r_m50, O2r_resid} at R2 (one-sided bootstrap p in the frozen direction).\\n  - VERDICT (frozen text, applied mechanically in code and written to cohort_result.json):\\n    CONFIRMED iff all of:\\n      - OPEN_home psp on O2r_m50 > 0 with CI > 0 at R2 AND at R3;\\n      - O2r_resid has the same sign at R2;\\n      - positive point estimate in >= 4 of the 5 groups at R2;\\n      - psp > 0 within method AND within object concepts;\\n      - RETENTION_RATIO_early psp < 0 given R0.\\n    DISCONFIRMED iff the CI of OPEN_home at R2 includes 0.\\n    Otherwise PARTIAL, with the failing clauses listed.\\n    Named readings, reported as stated:\\n      (a) 'type absorbs OPEN': the R1 CI > 0 but the R2 CI includes 0, and the type dummies carry the drop;\\n      (b) 'mechanical': the OPEN_home CI includes 0 while the OPEN_all CI > 0; then check SIZEMATCH to say whether it is paper count or home restriction.\\n    No subgroup hunting after the unseal; anything else is labelled EXPLORATORY.\\n  - SECONDARY (frozen, no refit):\\n    - O3 L1-logit (linear_all_O3): dAUC over the frozen B5 logit.\\n    - O4 EBM Spearman vs B5 (only if O4 exists).\\n    - O2r ElasticNet (linear_all_O2r_m50, linear_all_O2r_resid): Spearman gain over B5.\\n    - n_authors_early psp for O3/O1b/O1c.\\n    - CONTACT_REACH psp on O2r_m50 and O2r_resid, all concepts and excluding intersection-born.\\n    - Missing inputs are imputed at the frozen DEV medians via lib/design.py. A replication is DROPPED and reported 'not evaluable' if more than 20% of |standardised coefficient| mass (linear) or of the mean |term importance| (EBM) sits on fully imputed features.\\n    - Paired concept bootstrap CIs (2,000).\\n  - PLACEBOS (post-unseal, reported): 200 within-group permutations of O2r_m50 give the null distribution of OPEN_home psp at R2 (expect |psp| < 0.05 for 95%). A planted signal y' = rank(O2r) + 0.10-SD-equivalent * OPEN_home must be recovered with CI > 0.\\n\\nS10 OUTPUTS.\\n  - results/cohort_result.json: every rung x build x outcome x group x type estimate with CI, n and resampling unit; power and MDE; the verdict and the clause table; secondary; placebos; audits S2-T1..T3; the S3 decision; type benchmark metrics; LLM spend.\\n  - results/exp5_selection_result.json.\\n  - Figures (aii-data-fig-gen or matplotlib, PNG+PDF):\\n    fig_ladder.png: psp by rung, the three builds, O2r_m50 and O2r_resid panels;\\n    fig_forest_groups.png: per-group psp at R2 with the DL diamond, cohort and EXP5 side by side;\\n    fig_components.png;\\n    fig_within_type.png;\\n    fig_coverage_audit.png: tag_rate and label coverage by year.\\n  - full_method_out.json (exp_gen_sol_out): one example per cohort concept.\\n    input = concept label + id + t0 + group;\\n    output = O2r_m50;\\n    predict_B5 = frozen-R0 fitted rank prediction;\\n    predict_B5_plus_OPEN_home = R0 + OPEN_home fitted on EXP5 and applied frozen;\\n    plus metadata for the OPEN builds, type, footprint and all outcomes.\\n    Make the mini/preview variants with aii-json, and split by aii-file-size-limit if needed.\\n  - README.md with a 'Restoring removed files' section; .aii/manifest.yaml (keep data/sealed/, the outcome and feature parquets, and concept_types.csv; delete .venv/, __pycache__/ and any raw S3 cache as regenerable with its command); reproducibility.md; results/deviations.json.\\n\\nTIME PLAN (6 h).\\n  - 0:00-0:30 S0 + S1.\\n  - 0:30 launch S2 (background).\\n  - 0:30-2:30 in parallel: S5 on EXP5 concepts, S6, and S7 EXP5 HOME/SIZEMATCH builds (2-3 procs).\\n  - About 2:30 S2 done -> T1-T3, S3, S4, S5 on the cohort, S7 on the cohort.\\n  - 3:30-4:00 S8 freeze.\\n  - 4:00-4:30 S9 unseal and primary.\\n  - 4:30-5:15 secondary, placebos, audit.\\n  - 5:15-6:00 S10.\\n  DROP ORDER if late: O4/Pass B -> the learned-model replications -> the 2017 extension (only if the S8 rule did not require it; if it did, drop SIZEMATCH for the cohort before dropping 2017). NEVER drop: HOME build, the TYPE rung, the S3 decision, the single unseal.\",", "   \"fallback_plan\": \"F1 SNAPSHOT CHANGED OR UNREACHABLE. If the S3 manifest differs from EXP5's (a new monthly release), run the pass on the current snapshot and apply the T1 tolerance rule: >= 99% of cells exact and median relative diff < 1% on the 300 controls. If T1 fails, recompute the cohort frame from the NEW pass's own counts (years <= t0+2) instead of agg_counts, and recompute the 300 controls' EXP5 frame membership under the new counts to quantify drift. Log it. Do NOT mix old-snapshot selection features with new-snapshot cohort features for the same concept: the EXP5 features stay old-snapshot, which is fine because they are only used to freeze constants. If S3 is unreachable for more than 30 min, stop and report the artifact as blocked. There is no API fallback (0 credits by design).\\n\\nF2 PASS TOO SLOW. Projected more than 150 min after 20 files, apply in order: (i) drop referenced_works (O4 goes); (ii) drop authorships for the controls; (iii) emit early rows only for 2015-16 candidates, collecting 2017 candidates' AGG counts but not early rows. The 2017 extension then becomes impossible, and this is logged before S8. (iv) Raise workers to 6 and postpone the EXP5 SIZEMATCH build until after the pass.\\n\\nF3 LEGACY-TAG COVERAGE COLLAPSES IN 2021-24. Handled by the frozen S3 rule (TAG -> MATCH, validated at rho >= 0.9 on EXP5). If the MATCH validation also fails, the primary outcome becomes the 2015-onset TAG window t0+5..t0+7 (<= 2022), which needs no post-freeze data. 2016 onsets are then scored at t0+4..t0+6 as secondary, and the reduced n goes into the S8 power statement BEFORE the seal.\\n\\nF4 COHORT TOO SMALL OR UNDERPOWERED. The declared rule adds 2017. If the total is still < 800, run anyway, report the MDE next to every estimate, and make the verdict wording conditional ('underpowered: CI width X'). Never lower the rungs or pool with EXP5 outcomes.\\n\\nF5 LLM ISSUES. On a 403 budget refusal, stop all queued calls immediately. Concepts without a type label get type = 'unlabelled' (their own dummy) and are excluded from the within-type tests. Concepts without a precision-gate label fall back to the EXP5 sense-filter mean prediction, exactly as EXP5's precision_gate_fallback did, and are flagged. If the benchmark gate fails twice, restrict within-type tests to M1 = M2 agreement concepts (declared).\\n\\nF6 FROZEN MODELS WILL NOT UNPICKLE (version skew). First recreate EXP8's environment from its lock/reproducibility file. Second, rebuild linear models from the coefficients and intercepts stored in results/learned_model.json / frozen_spec.json, if present. Third, report the replication as 'not evaluable (environment)', never as a null.\\n\\nF7 HOME-ONLY COVERAGE LOW. If fewer than 60% of cohort concepts have a finite OPEN_home (>= 10 home papers and >= 4 components), keep the primary as declared, but report the B5 profile of included vs excluded concepts and the EXP5 sensitivity at min-papers 5. Do not change the threshold after S8.\\n\\nF8 TIME. Follow the drop order. The minimum publishable core is S0-S4, the S5 type labels, S7 HOME+ALL, S8 and S9 primary: the ladder for OPEN_home and OPEN_all, groups, within type, RETENTION_RATIO_early.\\n\\nF9 EGO FLAG TEST FAILS (components with flags off differ from EXP8). Run the original concept_core with n_null = 200 and betweenness cutoff 3 for the HOME build only, on 7 procs, and drop SIZEMATCH to a 5-draw version (declared deviation).\",", "   \"testing_plan\": \"UNIT AND REPRODUCTION TESTS (before any full run; tests/). U1: make_method_out() on 3 stub rows validates against exp_gen_sol_out with aii-json (the EXP9 failure mode). U2: ego flags. With compute_btw = False and n_null = 0, the six OPEN components on 100 EXP5 concepts equal EXP8 data/ego_features.parquet to 1e-12, and OPEN_all recomputed for 200 EXP5 concepts equals the value built from ego_features.parquet. U3: home filter. For 5 hand-picked concepts (single-home and intersection-born), HOME rows are exactly the rows with vfield in the home set, and the PRE window is filtered too. A synthetic concept whose off-home papers carry all its new topics must show new_edge_rate(HOME) < new_edge_rate(ALL). U4: SIZEMATCH with the subsample size equal to the full count reproduces ALL exactly, and draws are seed-deterministic. U5: rarefied_richness vs Monte Carlo (EXP5 T0 test re-run); O2r_resid with the frozen a/b reproduces EXP8 outcomes.parquet on 200 EXP5 concepts. U6: psp implementation equals EXP8 rq1stats on the EXP8 analysis_table for 3 indicators (1e-10), and the planted psp = 0.10 is recovered on synthetic data with n = 1,000. U7: the seal gate refuses to read data/sealed/ before the freeze, and refuses a second unseal. U8: the precision-gate prompt builder produces byte-identical messages to EXP5 for 20 EXP5 concepts (so the cache hits), which proves the prompt, model and parameters are unchanged.\\n\\nSTAGED SCALE-UP. Pass: 3 files (inspect rows, dtypes, year range 1995-2024, xpac excluded) -> 20 files (timing extrapolation, T1 on the files' partial counts against EXP5 per-file agg parts if available) -> all 2,040. Ego: 50 concepts -> 500 (time per concept per build) -> all. LLM typing: 40 concepts (inspect JSON parse rate >= 98% and spot-read the labels) -> the 300 benchmark -> all. Cost is checked after each stage against the $3 cap.\\n\\nCONFIRMATION SIGNALS BEFORE THE SEAL. (i) T1-T3 pass. (ii) The EXP5 selection ladder reproduces the EXP8 single-component signs on O2r_m50 at R0: new_edge_rate +, n_comm_W3 +, participation +, NOV_res +, ego_density_W3 -, edge_persistence -. A sign mismatch at R0 means a pipeline bug: stop and debug, do not re-sign. (iii) The coupling diagnostic shows OPEN_home less correlated with early off-home share than OPEN_all (expected; if not, the home filter is suspect). (iv) The cohort B5 and feature distributions are within the EXP5 range (report standardised mean differences; any |SMD| > 1 is investigated for a bug, not trimmed). (v) Type benchmark gate result recorded. (vi) The power statement is written.\\n\\nPOST-UNSEAL AUDIT (audit.py, independent code). Re-derive the primary OPEN_home psp at R2 and R3 with statsmodels OLS residuals and scipy rank (target |diff| < 1e-8). Re-derive the DL pooled estimate from per-group estimates by hand. Recompute O2r_m50 for 30 random cohort concepts directly from the sealed agg parts. Run the within-group shuffled-outcome control (200 draws; the 95th percentile of |psp| is reported) and the planted-signal recovery. Record everything in results/audit.json; any failed re-derivation is reported in the README headline, not hidden.\"", " }"]}], "userModified": false, "replaceAll": false}
```

### [51] TOOL CALL — Grep · 2026-09-29 02:13:27 UTC

```
Pattern: "^(?!  "|\{|\}).*"
```

### [52] TOOL RESULT — Grep [ERROR] · 2026-09-29 02:13:27 UTC

```
Error: Search failed — ripgrep rejected the pattern, glob, or file type without searching:
rg: regex parse error:
    (?:^(?!  "|\{|\}).*)
        ^^^
error: look-around, including look-ahead and look-behind, is not supported

Consider enabling PCRE2 with the --pcre2 flag, which can handle backreferences
and look-around.
```

### [53] TOOL CALL — Grep · 2026-09-29 02:13:27 UTC

```
Pattern: "[^\\]"[^,:}\n ]"
```

### [54] TOOL RESULT — Grep · 2026-09-29 02:13:27 UTC

```
{"mode": "count", "numFiles": 1, "filenames": [], "content": ".terminal_claude_agent_struct_out.json:9", "numMatches": 9}
```

### [55] TOOL CALL — Grep · 2026-09-29 02:13:33 UTC

```
Pattern: "^[^ {}]|^ [^ ]|^   "
```

### [56] TOOL RESULT — Grep · 2026-09-29 02:13:33 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "", "numLines": 0, "totalLines": 0}
```

### [57] TOOL CALL — Grep · 2026-09-29 02:13:33 UTC

```
Pattern: "[^\\]"[^,:}\n ]"
```

### [58] TOOL RESULT — Grep · 2026-09-29 02:13:33 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "2: \"t\n2: \"D\n3: \"s\n3: \"S\n4: \"r\n4: \"g\n5: \"d\n5: \"W\n6: \"p\n6: \"M\n7: \"b\n7: \"T\n8: \"i\n8: \"P\n9: \"f\n9: \"F\n10: \"t\n10: \"U", "numLines": 18, "totalLines": 18}
```

### [59] TOOL CALL — Glob · 2026-09-29 02:13:39 UTC

```
Pattern: "{.aii/*,*}"
```

### [60] TOOL RESULT — Glob · 2026-09-29 02:13:39 UTC

```
{"filenames": [".aii_claude_session.json", ".terminal_claude_agent_struct_out.json", ".repl_agent.ptylog"], "durationMs": 32, "numFiles": 3, "truncated": false, "totalMatches": 3, "countIsComplete": true}
```

### [61] TOOL CALL — Write · 2026-09-29 02:13:49 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1/.aii/manifest.yaml

entries: []
```

### [62] TOOL RESULT — Write · 2026-09-29 02:13:49 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1/.aii/manifest.yaml", "content": "entries: []\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [63] TOOL CALL — Write · 2026-09-29 02:13:49 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1/README.md

# Plan: Do open-neighbourhood concepts spread? Fresh-cohort test

AI Inventor, invention loop iteration 4, step GEN_PLAN, direction `experiment_iter4_dir1`.

This directory holds a **plan**, not an executed experiment. A separate executor agent runs it.

## What the plan does

It is a sealed, single-unseal confirmation of the openness claim (RQ1) on a 2015-2016 onset cohort of OpenAlex
legacy concepts that no earlier screen has touched.

- **The index.** OPEN is the mean of six signed z-scored ego-network components:
  - `new_edge_rate`
  - `n_comm_W3`
  - `participation`
  - `NOV_res`
  - `-ego_density_W3`
  - `-edge_persistence`
- **Three builds of OPEN.**
  - ALL-PAPERS.
  - HOME-ONLY.
  - SIZE-MATCHED ALL-PAPERS.
- **The control ladder**, which OPEN must survive:
  1. B5
  2. + CONTACT_REACH
  3. + concept type (LLM-labelled, with a benchmark)
  4. + pre-onset footprint
  5. + label coverage
  6. + home-group fixed effects
- **Selection data.** All constants are frozen on the EXP5 frame of 12,499 concepts, which serves as selection data only.
- **Measurement guard.** A pre-declared, outcome-blind audit of legacy-tag coverage. OpenAlex no longer tags new works
  with legacy concepts, and the audit decides the outcome grounding before the seal.

## Layout

| path | content |
|---|---|
| `.terminal_claude_agent_struct_out.json` | the plan (ExperimentPlan schema): domain practice, practice alignment, what it builds on, pseudocode, fallbacks, tests |
| `.aii/manifest.yaml` | disposal manifest (nothing heavy was produced) |
| `README.md` | this file |

## How to run

There is nothing to run here. The executor follows the `implementation_pseudocode` field of the plan JSON.

## Restoring removed files

No files are marked `delete`. This planning step produced no large binaries or caches.
```

### [64] TOOL RESULT — Write · 2026-09-29 02:13:49 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_1/README.md", "content": "# Plan: Do open-neighbourhood concepts spread? Fresh-cohort test\n\nAI Inventor, invention loop iteration 4, step GEN_PLAN, direction `experiment_iter4_dir1`.\n\nThis directory holds a **plan**, not an executed experiment. A separate executor agent runs it.\n\n## What the plan does\n\nIt is a sealed, single-unseal confirmation of the openness claim (RQ1) on a 2015-2016 onset cohort of OpenAlex\nlegacy concepts that no earlier screen has touched.\n\n- **The index.** OPEN is the mean of six signed z-scored ego-network components:\n  - `new_edge_rate`\n  - `n_comm_W3`\n  - `participation`\n  - `NOV_res`\n  - `-ego_density_W3`\n  - `-edge_persistence`\n- **Three builds of OPEN.**\n  - ALL-PAPERS.\n  - HOME-ONLY.\n  - SIZE-MATCHED ALL-PAPERS.\n- **The control ladder**, which OPEN must survive:\n  1. B5\n  2. + CONTACT_REACH\n  3. + concept type (LLM-labelled, with a benchmark)\n  4. + pre-onset footprint\n  5. + label coverage\n  6. + home-group fixed effects\n- **Selection data.** All constants are frozen on the EXP5 frame of 12,499 concepts, which serves as selection data only.\n- **Measurement guard.** A pre-declared, outcome-blind audit of legacy-tag coverage. OpenAlex no longer tags new works\n  with legacy concepts, and the audit decides the outcome grounding before the seal.\n\n## Layout\n\n| path | content |\n|---|---|\n| `.terminal_claude_agent_struct_out.json` | the plan (ExperimentPlan schema): domain practice, practice alignment, what it builds on, pseudocode, fallbacks, tests |\n| `.aii/manifest.yaml` | disposal manifest (nothing heavy was produced) |\n| `README.md` | this file |\n\n## How to run\n\nThere is nothing to run here. The executor follows the `implementation_pseudocode` field of the plan JSON.\n\n## Restoring removed files\n\nNo files are marked `delete`. This planning step produced no large binaries or caches.\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [65] ASSISTANT · 2026-09-29 02:14:05 UTC

```
The plan for the fresh-cohort test of the openness claim is written to `./.terminal_claude_agent_struct_out.json`. I also added a `README.md` and an empty `.aii/manifest.yaml`, since this step produced no large files. I couldn't run code in this step, so the JSON's syntax was checked by pattern searches, not a parser, and none of the plan has been executed.

**The main risk I found.** OpenAlex's own documentation says its legacy concepts are frozen and "new works are not tagged with them", and it gives no cut-off date. The cohort's outcome window is 2021–2024. Earlier rounds counted a paper only if its title matched the concept *and* it carried the legacy tag. If recent works lack the tag, 2023–24 counts would be too low without any error showing. The plan handles this with a rule fixed before any outcome is read:
- It measures what share of all works carry legacy tags each year, plus the ratio of tagged to title-matched papers on 300 concepts from the earlier frame.
- If coverage holds, it keeps the old tag-based rule.
- If coverage drops, it counts title matches alone for every outcome year. That switch is only allowed if, on the earlier frame, the breadth measure (O2r) agrees with the tag-based version at Spearman ≥ 0.9.
- The 2015-onset window ending in 2022, which needs no recent works, is always reported as a sensitivity check.

**How the plan is built:**
- **Reuse:** it takes the frame, matcher, precision gate prompt and cache, ego-network code, outcome code, seal gate and frozen models from experiments 5 and 8 by path.
- **Data pass:** one snapshot pass reads all 2,040 files, costs 0 OpenAlex credits, and collects the 2017 fallback candidates at the same time. So the declared extension never needs a second pass.
- **Order:** the earlier 12,499-concept frame is used only to freeze constants. All definitions and z-constants are hash-sealed before the cohort outcomes are unsealed once.
- **Power:** at the likely cohort size of about 1,000–2,000 concepts, the smallest detectable pooled effect is about 0.07–0.09. Within method or object concepts alone it is about 0.12–0.15. So the plan adds the 2017 onsets if fewer than 800 concepts pass the gate *or* simulated power is below 0.80. Both are decided before the seal.
- **Verdict:** confirmed, disconfirmed and the two named readings ("concept type absorbs openness"; "home-only fails, so the signal is mechanical") are written as fixed rules the code applies mechanically.
- **Concept-type labels:** a 300-concept benchmark labelled by two models from different families, plus a 60-item gold set. The plan says openly that the executor agent reads those 60, not a human. The labels must reach precision ≥ 0.85 for both method and object concepts. If they fail twice, the within-type tests use only concepts the two models agree on.
- **Cost and hardware:** expected LLM spend is about $1.5, with a hard cap of $3. I chose `gpu_basic` for its 7 CPU cores; the GPU itself is not used.

**Guards against losing a run or overrunning time:**
- A test in the first 30 minutes checks that the output file is in the right format, because experiment 9 failed in that loop.
- A test checks that dropping betweenness and the null draws leaves the six openness components identical to experiment 8's.
- If time runs short, the plan drops citation growth (O4) first, then the learned-model replications, then the 2017 extension. The home-only build, the concept-type step and the single unseal are never dropped.

Sources:
- [OpenAlex Concepts (deprecated)](https://help.openalex.org/data/concepts/)
- [OpenAlex Key Concepts](https://developers.openalex.org/guides/key-concepts)
- [OpenAlex Walden launch](https://blog.openalex.org/openalex-rewrite-walden-launch/)
- [Sun & Abraham heterogeneous event studies](https://conference.nber.org/confer/2023/SI2023/ML/heterogeneity.pdf)
```
