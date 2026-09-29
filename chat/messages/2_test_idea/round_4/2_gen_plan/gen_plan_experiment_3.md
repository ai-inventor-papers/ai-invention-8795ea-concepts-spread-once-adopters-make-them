# gen_plan_experiment_3 — test_idea

> Phase: `invention_loop` · round 4 · `gen_plan`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_experiment_3` (terminal_claude_agent, claude-opus-5-5)

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
Your workspace: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_3`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_3/`:
GOOD: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_3/file.py`, `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_3/results/out.json`
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

id: experiment_iter4_dir3
type: experiment
objective: >-
  FIX: re-run the failed iteration-3 RQ2 artifact (gen_art_experiment_9, plan 3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3;
  never executed, its output-format loop failed). It runs on the existing EXP5/EXP7/EXP8 arrays with the pre-registration
  updated to the openness account. (a) A log-additive breadth decomposition: contact rate x retention probability x frontier
  advance, with Shapley shares. (b) An empirical trajectory typology, named only if two methods agree. (c) Matched-pair case
  studies from the quantitative extremes. (d) The request's stage-1 AI/CS atlas (about 40 concepts; retrospective, descriptive).
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
  total from usage.cost, stop on the first 'AI Inventor per-run OpenRouter budget' 403. Cache only: NO snapshot pass, $0 LLM.
  FIRST write a valid method_out.json skeleton, and validate it with aii-json against exp_gen_sol_out at the MINI stage, before
  any long computation. Exp9 died on output-format validation, so the format is checked first and after every stage. (1) STATE
  SEQUENCES, t0..t0+10, from EXP7 state_panel_*.parquet and EXP5 agg_counts (D3 states: untouched / entered / retained / lost
  per field). Yearly summaries: contact rate (new off-home fields entered), retention probability (share of entered off-home
  fields that become retained), frontier advance (entries per retained field), rarefied entropy, within-home share, field-level
  community span on the EXP6 backbone, and the Exp8 early OPEN components (t0..t0+2) as static covariates. (2) DECOMPOSITION.
  log(breadth at t0+8) = log contact + log retention + log frontier (+ residual). Shapley decomposition of the top-vs-bottom
  O2r_resid tercile gap; adjust for Medicine homes and also exclude them. PRE-REGISTERED (frozen_spec.json, hashed, before
  computing): localised and integrating concepts differ MORE in contact/exploration than in retention, and localised concepts
  have HIGHER early retention ratios. Report the concept-bootstrap CI of the contact share minus the retention share. (3)
  TYPOLOGY. DTW k-medoids (k = 2..8, silhouette + gap + bootstrap stability) and a Gaussian HMM (3-5 states, BIC) on the standardised
  yearly vectors. A class is NAMED only if DTW-HMM ARI >= 0.5, it replicates when held-out is re-clustered, and it survives
  excluding Medicine homes. Otherwise report a continuum: project the trajectories on the first 2-3 principal axes and show
  where early OPEN sits on them (Spearman of OPEN with axis 1). Record the old typology (Exp6: 2 classes, HMM ARI 0.094) as
  not established. (4) CASE STUDIES. Six to eight MATCHED PAIRS seeded from Exp8 results/case_exemplars.json: same home group,
  early volume and growth within 0.25 SD (B5-matched), opposite OPEN (top vs bottom quintile), mixed domains and not only
  AI, excluding GENERIC terms by a label rule logged in deviations. For each pair: an alluvial field-flow figure of D3 states
  over time; early ego-network snapshots W1..W3 from data/frame_matches_early (topics coloured by EXP3 community); the O2r
  outcome; and external recognition dates from art_O7Dq4L02QnDN (descriptive only). (5) AI/CS ATLAS (the request's stage 1,
  labelled RETROSPECTIVE and DESCRIPTIVE). About 40 CS-home frame concepts with AI/ML labels, chosen to span rapid emergence,
  gradual growth, local specialisation, cross-disciplinary diffusion and transient expansion (O3 = 1). Yearly panels of connectivity,
  new neighbours, community membership, field distribution and D3 states. Include a small-multiples figure and a table stating
  which structural changes looked meaningful. (6) pipeline_counts.json for the methodology figure: works, concepts, episodes,
  risk-set rows and split sizes at every stage, read from the actual artifacts. OUTPUTS: state_sequences.parquet, decomposition.json,
  trajectories.json (assignments, ARI, stability, medoids, or continuum axes), case_studies/ (figures + per-pair JSON), ai_atlas/
  (figures + table), pipeline_counts.json, frozen_spec.json + seal log, and a schema-valid method_out.json.
what_it_would_show: ''
depends_on:
- id: art_O7Dq4L02QnDN
  label: recognition dates
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

### [3] TOOL CALL — Glob · 2026-09-29 02:07:01 UTC

```
Pattern: "*"
```

### [4] TOOL RESULT — Glob · 2026-09-29 02:07:01 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3/.aii_claude_session.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3/.terminal_claude_agent_struct_out.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3/.aii/manifest.yaml", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3/README.md", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3/.aii/module_end.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3/.repl_agent.ptylog"], "durationMs": 25, "numFiles": 6, "truncated": false, "totalMatches": 6, "countIsComplete": true}
```

### [5] TOOL CALL — Glob · 2026-09-29 02:07:01 UTC

```
Pattern: "*"
```

### [6] TOOL RESULT — Glob · 2026-09-29 02:07:01 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/t1_passA_exact_65_1125_1407_1918.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/unit_tests.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/t0_8_ego_port.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/o5_join.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/t4_timing_nnull200_cut4.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/features_config.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/provenance.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/checks.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/o2r_resid_fit.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/o4_reference_expectations.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/outcome_base_rates.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/indicator_matrix.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/t4_ego_sanity.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/indicator_corr_dev.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/size_diagnostic_dev.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/indicator_clusters_dev.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/dev_ranking.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/indicator_dictionary.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/dev_ranking_sensitivity.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/rq1_dev_selection.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/learned_model.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/dev_oof_predictions.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/power_dev.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/frozen_spec.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/heldout_summary.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/heldout_unit_results.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/heldout_predictions.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/learned_vs_single_heldout.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/portability_table.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/prereg_verdicts.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/prereg_b5_minus_reach.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/sensitivities_pooled.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/sensitivities_heldout.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/audit.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/rederive.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/case_exemplars.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/rq1_heldout.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/deviations.json"], "durationMs": 34, "numFiles": 38, "truncated": false, "totalMatches": 38, "countIsComplete": true}
```

### [7] TOOL CALL — Read · 2026-09-29 02:07:03 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3/.terminal_claude_agent_struct_out.json
```

### [8] TOOL RESULT — Read · 2026-09-29 02:07:03 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"How new concepts spread: paths and reasons\",\n  \"summary\": \"RQ2 artifact on the single EXP5 panel (12,499 concepts, TAG grounding, frozen split). From EXP5's cached concept x year x venue-field counts (scan/agg_counts.parquet, zero credits) it builds per-field state sequences (untouched / entered / retained / lost, EXP6 lib/h2.py states() verbatim) and yearly concept summaries: contact, retention, frontier advance, rarefied entropy, field-level brokerage on the frozen and time-varying 26-field backbones, and within-home prominence. It then runs five analyses. (a) An exact log-additive decomposition, log B = log early contact + log frontier multiplier + log retention, with Shapley (log-additive) shares for the top-vs-bottom O2r_resid tercile gap. It is volume-stratified, adjusted for Medicine homes and also run without them. Pre-registered prediction: retention carries the largest share. (b) Trajectory typology by DTW k-medoids and a 4-state Gaussian HMM, with optimal matching as a third view. A class is named only if DTW-HMM ARI >= 0.5, bootstrap-stable, replicated on held-out, and still present without Medicine homes; otherwise a PCA continuum is reported. (c) Sequence tests: does home prominence come before first off-home retention, or the reverse? Discrete-time hazards, Sun-Abraham event studies with pre-trend tests, random-year placebos and a mechanical-lag null. Intersection-born and single-home concepts are compared on the same measures. (d) 6-8 case concepts picked from quantitative extremes, each with a field-state raster and an alluvial figure. A zero-credit snapshot lineage check (case concepts plus 150 random held-out concepts) asks whether early adopter papers in fields that later RETAIN a concept already cite that field's literature and use its topics more than adopters in fields that later LOSE it, net of each field's own citing habits. (e) External recognition timing (art_O7Dq4L02QnDN, year_usable events only; plus a Wikipedia/Wikidata-only variant) per class or axis, and pipeline counts for the methodology figure. Everything is frozen on DEV (hash-sealed spec) and scored once on held-out groups and the 2010-14 cohort, with concept-clustered refit bootstrap CIs. Budget: 0 OpenAlex credits, <= $0.50 OpenRouter (optional), cpu_plus.\",\n  \"runpod_compute_profile\": \"cpu_plus\",\n  \"domain_practice\": \"WHAT I READ: the strategist's field reasoning (relatedness principle: Hidalgo 2007, Guevara 2016 entry AUC 0.68-0.90, Neffke 2011 exit/survival); this run's research artifact art_dxvRpQufMR0e (ANS template, 22 ANS papers incl. Holmgren 2023 alluvial change, De Domenico 2016 sources/sinks); the code and READMEs of EXP5 (art_wxWssKSUR45f) and EXP6 (art_N-mpomDZZ1ln: lib/h2.py, lib/traj.py); and two targeted lookups: the staggered event-study literature (Sun & Abraham 2021 interaction-weighted estimator, RESTUD 91(6); Roth 2022 'Pre-test with caution', AER:Insights; Borusyak/Gardner two-stage DiD) and sequence-analysis practice in the social sciences (optimal matching, typologies from dissimilarity + clustering; Biemann & Datta 2014, ORM). No domain handbook covers scientometrics, so these are held provisionally.\\n\\n(1) BASELINES AND COMPARISONS. (i) Volume/size: every diffusion or breadth claim in this field is compared with log volume, because breadth counts go up with paper counts (rarefaction, O2r_resid; Guevara/Neffke use size controls). A reviewer would first ask 'is your integrating class just the big concepts?'. (ii) Field composition and home-field effects: Medicine or CS homes are known to behave differently. This run already found Medicine dominating EXP6's localised class, 42/60. The standard move is stratification plus exclusion. (iii) Relatedness: retention and entry are compared with relatedness density on a field backbone. (iv) Trajectory typologies are compared with a continuum or a single-factor account (volume, age). In citation-trajectory clustering (sleeping-beauty and citation-history clustering work) the standard check is cluster validity plus stability. (v) Ordering claims ('A then B') are compared with the reverse path and with placebo timing.\\n\\n(2) CASES AND DATA. Standard: OpenAlex or WoS whole-corpus panels with concept or keyword vocabularies; venue- or journal-level discipline labels (Rinia 2002, Yan 2013); a relatedness backbone from co-classification. Known weak spots: paper-level topic classifiers used as discipline labels (they read the paper's own references, which is circular for lineage), conference-heavy CS under-covered by article|review filters (EXP5 deviation), and survivorship of named vocabularies (legacy concepts seeded from Wikipedia).\\n\\n(3) CONTROLS / WHAT IS HELD CONSTANT. Concept age (align on t0, not calendar year), calendar year (cohort FE), concept volume (strata), home-field group, and the same state definitions across splits. The confounds this design is most likely to be caught on: (a) retention defined as >= 2 papers in 3 years rises mechanically with volume; (b) the ordering test is biased by construction, because RETAINED needs entry at least 2 years earlier, so B >= t0+2 while home prominence can peak at t0; (c) TWFE event studies with staggered timing and heterogeneous effects produce spurious pre-trends and wrong-signed weights (Sun & Abraham; Roth).\\n\\n(4) HOW MUCH IS ENOUGH. Trajectory typologies: hundreds to thousands of units. Cluster stability is reported by bootstrap (Hennig-style Jaccard/ARI >= 0.6-0.75 counts as stable); ARI 0.5 counts as moderate agreement between methods. HMM state number is chosen by BIC with several EM restarts. Event studies report leads and lags with clustered CIs and a joint pre-trend test, plus the power of that pre-test (Roth). Resampling is by concept, with >= 1,000 refits. Heterogeneity across domains is reported per group with I2, not averaged. For lineage checks, a few hundred episodes with concept-clustered CIs is the minimum anyone reads. With ~500 episodes the MDE is roughly 0.25 SD, and that is the number to state.\\n\\n(5) MEASURES AND REPORTING. Shannon/rarefied entropy, disciplinary reach, Rao-Stirling (diversity); participation coefficient over backbone communities (Guimera-Amaral); state-transition matrices; Kitagawa / Das Gupta / Shapley decompositions of rate differences, which are standard in demography and inequality accounting (the contribution shares sum to the total gap); alluvial diagrams of state flows (Rosvall & Bergstrom 2010; Holmgren 2023 in ANS); Kaplan-Meier or cumulative incidence for time-to-event (first retention, recognition); forest plots per held-out group with DL pooling.\",\n  \"practice_alignment\": \"MEETS: (1) Volume confound: the decomposition runs within log-volume quintile strata and on O2r_resid terciles; trajectory classes are checked against volume terciles (ARI with volume terciles is reported, and a class is flagged 'volume class' if that ARI >= 0.5); retention is recomputed at min_n = 3 and 5. (2) Home-field composition: Medicine-home adjustment AND exclusion, applied to the decomposition, to class naming and to the sequence tests; per-group reporting with I2. (3) Cluster validity: silhouette and gap for k, bootstrap ARI stability, cross-method agreement (DTW vs HMM, plus optimal matching), held-out replication by independent re-clustering compared with nearest-DEV-medoid assignment. (4) Event studies: Sun-Abraham interaction-weighted estimator (not naive TWFE), a joint pre-trend test with its power, the reverse path, a random-year placebo, and a mechanical-lag null built from permuted series. (5) Resampling unit = concept, >= 1,000 refit bootstraps, named in every table; crossed concept x field bootstrap for episode-level lineage tests. (6) Frozen-on-DEV, hash-sealed, one held-out scoring. (7) Decomposition shares are exact (log-additive, so the Shapley value is unique) and come with bootstrap CIs.\\n\\nDEPARTS: (a) Discipline resolution is 26 venue fields, not 252 subfields. Justified: the D3 definitions, the frozen backbone and every prior artifact are at this level, and switching would break comparability with the H2 lead. Cost: 'retention' is coarse, and within-field migration between subfields is invisible. (b) 'Centrality within the home community' is measured by field-level home PROMINENCE (the concept's share of home-field output), and secondarily by home-topic reach from the snapshot pass. The full concept-topic ego network, where centrality proper lives, is not recomputed, because it belongs to the RQ1 artifact. Cost: a reviewer can say prominence is popularity. Mitigation: the secondary topic-reach measure, and prominence is reported as a proxy. (c) The lineage check covers ~150 held-out concepts plus the cases, not the full frame, because of the 6 h budget and the snapshot I/O cost of referenced_works. Cost: an MDE of ~0.25 SD, and the result is illustrative mechanism evidence, not a population estimate. (d) The ordering is observational: no instrument, so 'precedes' is not 'causes'. It is stated as temporal precedence with placebo and pre-trend checks. (e) Venue labels miss unlabelled works (label coverage 26-80%), and conference CS is under-covered by the article|review base. This is carried forward from EXP5 unchanged for comparability; label coverage is reported per class. (f) Held-out outcomes for the frame were already unsealed once by EXP5 (for H1/H3), so 'held-out' here means analysis choices frozen before this artifact reads held-out states. The executor enforces this in code (DEV-only filter plus an assert) and discloses it.\",\n  \"builds_on\": \"DEEPEN on the existing panel. Nothing starts from scratch. All paths are relative to the run root /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/ and are read-only; copy code into the workspace and do not import across trees.\\n(1) EXP5 art_wxWssKSUR45f = 3_invention_loop/iter_2/gen_art/gen_art_experiment_5/:\\n- frame_concepts.csv (12,499 concepts; columns ci, concept_id, qid, name, t0, newborn, home, intersect40, weak_home, group, split, precision_c, label_coverage_early, early_volume). NOTE: this and the next three files are in the workspace ROOT, not results/.\\n- concept_outcomes.csv (ci, concept_id, split, O1, O3, peak_year, N_outcome, O2r_m30, O2r_m50, O2_raw).\\n- concept_features_basic.csv (B5, G, REL_home; O2r_resid if present).\\n- episodes.csv (27,393 episodes with R).\\n- scan/agg_counts.parquet (19.7M rows keyed ci, year, vfield, ptfield, tagstate, mt, n). This is the source of every state matrix. Rebuild the dense arrays with panel.build_arrays('grounded'): TAG = tagstate==1, V[ci, y, 27], vfield code = OpenAlex field id - 10, code 0 = unlabelled. EXP5 deleted arrays_grounded.npz as regenerable.\\n- scan/year_field_totals.npz (base works per year x field, for RCA and home prominence).\\n- scan/co_by_year.npz (26x26 topic-field co-assignment per year, used for the time-varying backbone).\\n- scan/reservoir/part_*.parquet (12 hash-sampled hits per concept x era with file/row pointers, fallback lineage source).\\n- common.py (Y0, Y1, NY, source_field_lut, surf_arrow, works_files, read_parquet_parts).\\n- rangefile.py (HTTP-range column reader).\\n- matcher.py + lexicon_v1.parquet (Aho-Corasick matcher; the targeted pass must use these unchanged).\\n- scan_full.py (per-file pass template: COLS, TAG_MIN = 0.3, base filter).\\n- seal.py (freeze/unseal gate pattern).\\n- snapshot/works_manifest.json (2,040 file keys).\\n(2) EXP6 art_N-mpomDZZ1ln = 3_invention_loop/iter_2/gen_art/gen_art_experiment_6/:\\n- lib/h2.py: states(), used VERBATIM for ENTERED/RETAINED/LOST, and rca_entered.\\n- lib/traj.py: concept_series, dtw_matrix (tslearn Sakoe-Chiba), kmed (kmedoids.fasterpam), choose_k, hmm_fit (hmmlearn GaussianHMM, BIC), first_upward_change + calibrate_pen (ruptures PELT, 5% false-alarm calibration), lead_lag.\\n- lib/lib_outcomes.py (rarefied_richness, shannon) and lib/stats_core.py (CLogit, fe_ols).\\n- inputs/field_backbone.json (frozen 1998-2002 PMI phi and gateway g).\\n- results/frame_concepts.csv (its 653 concepts, used for the overlap flag and case mapping).\\n- results/entry_risk_sets_heldout.parquet and entry_risk_sets_dev.parquet (per-event d0_ret_rel, used to select frontier-extreme cases).\\n- results/cluster_assign_*.csv, trajectories_*.csv, ordering_*.csv (the iteration-2 k=2 typology and ordering result being re-tested).\\n- figures/fig_case_*.png (style reference for the field-flow plots).\\n(3) iteration-1 art_yrradSC27HtQ = 3_invention_loop/iter_1/gen_art/gen_art_experiment_3/: backbone/slice0-2.npz (topic PMI slices; used only for the home-topic reach normaliser if needed).\\n(4) Dependency art_O7Dq4L02QnDN = 3_invention_loop/iter_2/gen_art/gen_art_dataset_2/full_data_out/full_data_out_{1,2,3}.json (dataset 'concept_recognition'; join metadata_openalex_id == 'C' + concept_id; events carry source, event_type, year, year_usable, relation, match_confidence).\\nNEGATIVE FINDINGS BUILT PAST:\\n- Gateway centrality and gateway weighting are closed, so no gateway variable is used as a trajectory driver.\\n- EXP6's k=2 typology failed cross-method agreement (HMM-vs-DTW ARI 0.094) and its localised class was 42/60 Medicine, hence the naming rule and the Medicine exclusion.\\n- EXP6's ordering is MIXED: negative concept-FE lead-lag coefficients, a pre-trend at ev-3 of -0.072, and a significant reverse path on DEV. Hence the Sun-Abraham design, the mechanical-lag null and the both-direction test.\\n- M1 showed that raw lineage is mostly field homophily, so the lineage check is background-adjusted.\\nIf the run volume is not mounted, re-implement from the D3 definitions and the public S3 snapshot, and log every deviation in deviations.json.\",\n  \"implementation_pseudocode\": \"WORKSPACE = /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/<this artifact dir> (cwd). Read the aii-python, aii-parallel-computing, aii-long-running-tasks, aii-use-hardware and aii-json skills first. uv venv, python 3.12. Packages: numpy pandas pyarrow scipy scikit-learn statsmodels networkx tslearn kmedoids hmmlearn ruptures matplotlib loguru lifelines pyfixest (for Sun-Abraham via sunab; fallback: implement the IW estimator by hand).\\nRUN = /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M; E5 = RUN/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; E6 = RUN/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; DEP = RUN/3_invention_loop/iter_2/gen_art/gen_art_dataset_2.\\n\\nTIMEBOX (6 h total):\\n- S0-S2: 1 h.\\n- S3-S4: 1.25 h.\\n- S5: 0.75 h.\\n- S6 snapshot passes run IN THE BACKGROUND from ~0:45, taking about 1.5 h of wall time.\\n- S7-S9: 1.25 h.\\n- Writing up: 0.5 h.\\nIf behind schedule, drop in this order: optimal-matching view -> time-varying backbone brokerage -> home-topic reach A' -> lineage pass B (use the reservoir fallback).\\n\\nS0 SETUP & COPY\\n  copy E5/{common.py, rangefile.py, matcher.py, panel.py, seal.py, scan_full.py} and E6/lib/{h2.py, traj.py, lib_outcomes.py, stats_core.py} into lib/; set lib/config.py Y0 = common.Y0 (check it is 1995 and NY = 28; EXP6's config Y0 may differ, so re-index)\\n  sha256 of every copied file -> logs/provenance.json\\n  load frame = E5/frame_concepts.csv; outc = E5/concept_outcomes.csv; feats = E5/concept_features_basic.csv\\n  parse home: str split on '|' (check the separator in the data), values are field ids 11..36; MED = 27, CS = 17, ENG = 22, BGM = 13\\n  flags: med_home = 27 in home; intersection_born = intersect40 == 1; in_exp6 = concept_id in E6/results/frame_concepts.csv (join on concept_id; check that the column exists and record the overlap count)\\n  O2r_resid: if present in feats, use it; else fit OLS O2r_m50 ~ log(N_outcome) on DEV only, freeze the coefficients, residualise all splits\\n  ASSERT before the freeze: every analysis function receives frame[split == 'DEV'] only (guard: a global SEALED flag; functions raise if any non-DEV ci appears)\\n\\nS1 COUNTS -> STATES (all concepts; states are computed for all splits, but held-out rows are written to disk UNREAD until the unseal)\\n  arrays = panel.build_arrays('grounded', n_concepts = len(lexicon_v1)) -> V[ci, y, 27] (TAG counts)\\n  VF = year_field_totals.npz -> N_j(t)\\n  phi, g = E6/inputs/field_backbone.json\\n  for each concept c (vectorised per concept, multiprocessing over chunks):\\n    G = V[ci]                                         # [NY, 27]\\n    S = h2.states(G, home, min_n)  for min_n in {2 (primary), 3, 5}\\n    for age a in 0..8 (t = t0 + a <= 2022; also a = 9, 10 where t <= 2022, flagged 'extended'):\\n      for field j in 0..25: state = LOST if S.lost[t] & offhome[j]\\n                                    else RETAINED if S.retaining[t]\\n                                    else ENTERED if S.entered[t]\\n                                    else UNTOUCHED\\n                            (home fields get state HOME)\\n    write state_sequences.parquet: (ci, concept_id, split, group, t, age, field, state int8, n_t, w3, cum), about 3.6M rows\\n  concept-year summaries (panel.parquet):\\n    n_ent_off(t); new_entries(t) = n_ent_off(t) - n_ent_off(t-1)  [contact rate]\\n    n_ret(t); n_lost(t)\\n    ret_share(t) = n_ret(t) / max(1, n_ent_off(t-2))  [retention probability among fields old enough to qualify]\\n    frontier(t) = new_entries(t) / max(1, n_ret(t-1))  [entries per retained field]\\n    R20(t) = rarefied richness at m = 20 of the 3-yr window; H(t) = Shannon of the 3-yr window (lib_outcomes)\\n    brokerage on the frozen phi:\\n      comms = Louvain(phi, seed = 0); choose the resolution in {0.5, 0.75, 1, 1.25, 1.5} giving 3-8 communities (outcome-free, logged)\\n      n_comm_ret(t) = number of communities spanned by RETAINED(t) plus home\\n      part_ret(t) = 1 - sum_s (share of the concept's 3-yr off-home papers in retained fields of community s)^2\\n    brokerage on the time-varying backbone: from co_by_year.npz, rolling 5-yr PMI_ij = log(CO_ij * NT / (CO_ii * CO_jj)), positive part; Louvain per year with the same resolution; report the ARI of its communities vs the frozen ones; recompute n_comm_ret_tv and part_ret_tv\\n    home prominence HP(t) = n_c,home(t) / N_home(t) (summed over home fields); home_share(t) = n_c,home(t) / n_c(t) (within-home share)\\n    log_vol(t) = log1p(n_c(t)); label_cov(t) = 1 - V[ci, t, 0] / n_c(t)\\n  transition matrix: per group and split, counts of field-state transitions year to year (UNTOUCHED -> ENTERED -> RETAINED -> LOST -> re-ENTERED), with rates by phi(home, j) tercile  -> transitions.json\\n  VALIDATION: for concepts in both frames (in_exp6), Spearman of n_ret(t) and n_ent_off(t) between this panel and E6/results/trajectories_*.csv (expect > 0.8; the grounding differs slightly); log it\\n\\nS2 DECOMPOSITION (fit and freeze on DEV; then held-out once)\\n  H = 8. Per concept:\\n    E2 = off-home fields ENTERED by t0+2 (early contact)\\n    EH = entered by t0+H\\n    B = |RETAINED(t0+H)|\\n    M = EH / E2  (frontier multiplier)\\n    rho = B / EH  (retention)\\n    phi_adv = (EH - E2) / sum_{t=t0+2}^{t0+H-1} n_ret(t)  (entries per retained field-year; descriptive)\\n    identity log B = log E2 + log M + log rho (exact when E2, B >= 1)\\n  (a) GROUP-LEVEL exact (handles zeros): for tercile g in {top, bottom} of O2r_resid:\\n      Ebar_g = mean E2\\n      M_g = sum EH / sum E2\\n      rho_g = sum B / sum EH\\n      Bbar_g = Ebar_g * M_g * rho_g (identity)\\n    Delta log Bbar = Delta log Ebar + Delta log M + Delta log rho; the Shapley share of each factor = its Delta / total (unique, because log-additive)\\n    Das Gupta check: also the additive (non-log) Das Gupta 3-factor decomposition of Delta Bbar\\n  (b) VOLUME-STRATIFIED: repeat within quintiles of log early_volume (t0..t0+2 grounded volume), average the shares weighted by stratum n\\n  (c) MEDICINE: (i) adjusted = within the strata {med_home, non-med}, then averaged; (ii) excluded = drop med_home concepts\\n  (d) CONCEPT-LEVEL: hurdle model.\\n      (i) P(B >= 1) logistic on z(log1p E2), z(log M'), z(rho') [smoothed: M' = (EH + 0.5) / (E2 + 0.5), rho' = (B + 0.5) / (EH + 1)] + log volume + group; relative importance by LMG/Shapley of the McFadden R2.\\n      (ii) Among B >= 1: the exact variance decomposition var(log B) = sum cov(log B, log factor_k), which gives shares that sum to 1.\\n  (e) min_n = 3 and 5 sensitivity; outcome variant: terciles of O2r_m50 raw and of O2_raw\\n  CIs: 1,000 concept bootstrap resamples; within each split, the whole pipeline (terciles recomputed per resample)\\n  Pre-registered test (frozen): RETENTION-LEADS = share_rho > share_E2 AND share_rho > share_M in the volume-stratified, Medicine-excluded analysis, with bootstrap P(share_rho is max) >= 0.95. Evaluated on DEV (development) and then once on the pooled held-out groups, per group (DL-pool the shares with I2), and on the cohort (DEV-home and non-DEV-home parts).\\n  -> decomposition.json\\n\\nS3 TRAJECTORIES (DEV only until the freeze)\\n  VARS = [new_entries, n_ent_off, n_ret, n_lost, ret_share, frontier, H, n_comm_ret, part_ret, home_share]; ages 0..8 (9 steps); NOT log volume (shape classes; volume is checked afterwards)\\n  z-standardise each VAR with DEV means/SDs (frozen); array Z[n_concepts, 9, 10]\\n  DTW: traj.dtw_matrix (Sakoe-Chiba radius 2, n_jobs = 4) on DEV (about 4,771 concepts gives about 11M pairs: time it on 500 first and extrapolate; if > 25 min, use radius 1 or a random 3,000 DEV subsample for k selection, then assign the rest to the nearest medoid)\\n  k selection: traj.choose_k over k = 2..8 (silhouette, 100 x 80% subsample bootstrap ARI) + gap statistic on the MDS embedding of D; rule: the largest silhouette among k with median bootstrap ARI >= 0.6\\n  HMM: GaussianHMM(n_components = 4, covariance_type = 'diag', n_iter = 300), 10 random restarts, keep the best LL; also BIC over 2..6 states (reported). The concept-level HMM partition is k-medoids (same k as DTW, Euclidean) on the flattened posterior state-occupancy matrix [9 ages x S states] plus the final state one-hot.\\n  OPTIONAL third view: optimal matching on a concept-stage categorical sequence per age: {HOME_ONLY: n_ent_off = 0; CONTACT: n_ent_off > 0 & n_ret = 0; RETAIN_1: n_ret = 1; RETAIN_MANY: n_ret >= 2; CONTRACTING: n_lost > n_ret}. Substitution costs = 2 - p_ij - p_ji from the DEV transition rates, indel = 1; own DP implementation with numba or numpy; PAM with the same k.\\n  NAMING RULE (frozen): a class is NAMED only if all of:\\n    (1) ARI(DTW, HMM) >= 0.5 overall;\\n    (2) DTW bootstrap median ARI >= 0.6;\\n    (3) excluding med_home and re-clustering: ARI with the original labels restricted to non-Med concepts >= 0.5, AND the class keeps >= 5% of non-Med concepts;\\n    (4) held-out replication (after the unseal): re-cluster held-out independently with frozen VARS, z-spec and k, assign held-out to DEV medoids by DTW nearest medoid, ARI(independent, nearest-medoid) >= 0.5.\\n    Otherwise CONTINUUM: PCA on the flattened DEV Z (90 dims); keep 2-3 PCs (scree + > 10% variance each); report loadings per VAR x age; project held-out with frozen loadings.\\n  Class/axis profiling: medoid series; the class x group table; log-volume distribution; ARI(class, volume tercile) (flag 'volume class' if >= 0.5); O1 / O2r_resid / O3 / O4-absent / label coverage per class; the naming vocabulary is chosen from the data after profiling: localised, rapid interdisciplinary diffusion, gradual integration, transient expansion (O3), rising brokerage\\n  sensitivity: O1 == 1 subset only; min_n = 3\\n  -> trajectories.json (assignments, k grid, ARIs, stability, medoids with concept names, PCA loadings, the Exp6 k = 2 comparison = ARI of our labels vs E6 cluster_assign on overlapping concepts)\\n\\nS4 SEQUENCE TESTS (DEV development; held-out once)\\n  events per concept (ages 0..8):\\n    A (home prominence, primary) = first age where HP >= 0.5 * max_{0..8} HP (half-peak time)\\n    A_cp (secondary) = the first upward change point of log HP from traj.first_upward_change, with a penalty calibrated by traj.calibrate_pen to a 5% false-alarm rate on permuted DEV series\\n    A' (home-topic reach, if S6 pass A finishes) = half-peak time of the number of distinct home-field topics per year / the home field's active topic count\\n    B = first age with n_ret >= 1\\n    B_far = first retention in a field with phi(home, j) in the bottom tercile of the concept's off-home fields\\n  (i) ORDER SHARES among concepts with both A and B: before / tie / after.\\n      MECHANICAL-LAG NULL: B >= 2 by construction. So recompute the shares with A drawn from 1,000 within-concept permutations of the HP series (same detector); the reported statistic is observed minus null share, with concept bootstrap CIs.\\n  (ii) DISCRETE-TIME HAZARD of B: concept-age rows at risk (age >= 2, B not yet occurred); cloglog on post_A(t-1) indicator + age FE + log_vol(t-1) + label_cov + group FE; concept-clustered SE; HR = exp(beta). Reverse: the hazard of A given post_B(t-1), same controls (both directions).\\n  (iii) EVENT STUDIES with a staggered design: Sun & Abraham interaction-weighted estimator (pyfixest feols('Y ~ sunab(cohort_age, age) | ci + t', cluster = ci) or a hand-written IW: cohort-specific TWFE with the never-treated as control, aggregated by cohort shares).\\n        Forward: Y = n_ret(t) and H(t) around A; leads -3..-1 (ref -1), lags 0..4.\\n        Reverse: Y = log HP(t) around B.\\n        Report the joint Wald pre-trend test and its power against a linear pre-trend equal to 50% of the post effect (Roth 2022).\\n  (iv) RANDOM-YEAR PLACEBO: 200 draws assigning A to a random age from the DEV empirical A-age distribution within the group; recompute the hazard HR; the real HR must be outside the 95% placebo band.\\n  (v) INTERSECTION-BORN (intersect40 == 1, about 502) vs single-home: KM / cumulative incidence of B, and the discrete-time hazard with volume and group adjustment; class/axis distribution (chi-square or PC-score t-test); the share with B <= 2.\\n  Frozen verdict rule:\\n    HOME-FIRST supported if, on held-out, HR(B | post_A) > 1 with CI > 1, AND the pre-trend joint p > 0.10, AND the observed-minus-null 'A before B' share > 0 with CI > 0, AND the placebo is exceeded, AND the reverse HR does not exceed the forward one.\\n    INTERSECTION ROUTE supported if intersection-born concepts have a hazard ratio > 1 for B with CI > 1.\\n    Both, one or neither may hold. The iteration-2 ordering stays MIXED unless DEV and held-out agree.\\n  Report separately: DEV, each held-out group, DL pooled, cohort (DEV-home / non-DEV-home), Medicine excluded.\\n  -> sequence_tests.json\\n\\nS5 FREEZE -> UNSEAL ONCE\\n  frozen_spec.json = {VARS, z-spec, k, HMM restarts/seed, naming thresholds, Louvain resolution, decomposition definitions, event definitions, penalty, verdict rules, seeds, code sha256 of every lib and script file, list of held-out ci}\\n  seal.py freeze (writes logs/seal.log with the sha256) -> git commit -> seal.py unseal (refuses a second time) -> run S2 (b-e), S3 (4) and S4 on PHYS / LIFEENV / SOC / MATHDEC, pooled and DL, and on COHORT split into DEV-home and non-DEV-home. Also report every held-out result with the in_exp6 concepts excluded.\\n\\nS6 TARGETED SNAPSHOT PASSES (start at ~0:45 in the background with nohup and a PID; 0 credits)\\n  lineage sample L = case concepts (from S8; provisional: the top/bottom frontier-extreme concepts from E6 risk sets) + 150 random held-out concepts (seed 20260928; stratified 40 PHYS / 40 LIFEENV / 40 SOC / 30 MATHDEC) drawn from those with >= 1 off-home field ENTERED by t0+4 (so they have episodes; eligibility uses states only, not outcomes)\\n  PASS A (all 2,040 files; columns: id, title, publication_year, type, is_paratext, is_xpac, primary_location.source.id, concepts.id/score, topics.list.element.id, topics.list.element.field.id; reuse scan_full.process_file logic with the lexicon restricted to the 12,499 frame concepts, same matcher/forms, TAG_MIN = 0.3):\\n    (A1) for TAG hits of frame concepts: aggregate (ci, year, vfield, topic_id) counts over each hit's topics  -> topic_agg.parquet (feeds A' and co-topic fit)\\n    (A2) field-year topic totals over base works: (year, vfield, topic_id) counts  -> field_topic_totals.parquet (the 'field's own topics')\\n    (A3) id map for base works: (work_id int64, vfield int8, year int16) per file -> merged, sorted npy memmap (about 1.4 GB; keep only if < 2 GB, else delete after use, marked regenerable)\\n    (A4) for hits of concepts in L: (file, row, work_id, ci, year, vfield, topic ids)\\n    (A5) a random background sample: per (year 2003-2022, vfield) up to 300 base works by the smallest hash (file, row, work_id)\\n    Time 5 files first -> extrapolate; EXP5's 10-column scan took 33 min on 4 vCPU, budget <= 60 min\\n  PASS B (only files containing A4 or A5 rows; columns: referenced_works, authorships.author.id):\\n    probe 5 files; if the projection is > 75 min, keep a random subset of those files within budget (logged; files are not concept-ordered, so this thins works at random)\\n    extract refs and author ids for the A4 and A5 rows only  -> lineage_works.parquet\\n  cited-work field = searchsorted in the A3 id map (unknown if outside 1995-2022 article|review; report coverage)\\n\\nS7 LINEAGE CHECK (mechanism)\\n  episodes = (c in L, off-home field j) with >= 2 papers in j by t0+4; status = RETAINED-episode if j is in RETAINED at >= 3 distinct years within t0..t0+8, LOST-episode if j is ENTERED then LOST and never RETAINED; others are excluded\\n  EARLY adopter papers = the first <= 20 concept-papers in j that appear BEFORE the episode's status can resolve (years < entry year + 2), so the covariates are not mechanically tied to later persistence\\n  per paper:\\n    wf = share of resolved references in field j\\n    wh = share in the home field(s)\\n    bg_wf = mean within-field reference share of the A5 background works of field j in the same year (the field's own citing habit)\\n    adj_wf = logit(wf) - logit(bg_wf) (smoothed +0.5)\\n    cotopic_J = Jaccard(topics of the paper, the top-50 topics of field j that year from A2) minus the same for the A5 background works\\n    self-migrant = any author with an earlier concept-paper in the home field (from the A4 author ids)\\n  episode-level means -> test RETAINED vs LOST:\\n    LPM and logistic of status on z(adj_wf), z(adj_home), z(cotopic_J) + log early n_j + phi(home, j) + field FE (+ concept FE where a concept has both statuses); concept-clustered refit bootstrap (1,000) and a crossed concept x field bootstrap\\n    descriptive: the same measures in the LATE window (t0+5..t0+8) for retained episodes (adaptation over time: does adj_wf rise?)\\n  prediction: retained > lost on adj_wf and cotopic_J, and lost > retained on adj_home; report the MDE\\n  -> lineage_check.json\\n\\nS8 CASE STUDIES\\n  frontier contribution from E6 risk sets: for each E6 concept, the mean over its entry events of (d0_ret_rel of the entered field minus the stratum mean) / the SD of d0_ret_rel; map E6 cidx -> concept_id via E6/results/frame_concepts.csv; keep concepts in the EXP5 frame with >= 3 events\\n  pick 6-8, with at most 2 from CS/AI homes and >= 3 domains:\\n  - top 2 and bottom 1 frontier contribution;\\n  - the medoid of each named class, or the concepts at the PC1 extremes (max 3);\\n  - 1 transient spike (O3 = 1, highest peak ratio);\\n  - 1 high-volume local concept (top-decile early_volume, bottom-decile O2r_resid).\\n  Record the selection rule with the numbers.\\n  per case:\\n  - (a) a state raster: fields (rows, ordered by backbone community) x years, coloured by state;\\n  - (b) an alluvial plot of field counts flowing between UNTOUCHED / ENTERED / RETAINED / LOST per year (matplotlib fill_between ribbons; no browser dependency);\\n  - (c) a backbone map with retained fields highlighted at t0+2, t0+5 and t0+8;\\n  - (d) JSON with the series, events A/B, class, recognition events and lineage stats if in L.\\n  -> case_studies/<concept_id>.{png,pdf,json}\\n\\nS9 EXTERNAL TIMING + PIPELINE COUNTS\\n  load the DEP full_data_out parts (dataset == 'concept_recognition'); map 'C' + concept_id -> events\\n  primary: events with year_usable & relation == 'same' (any source); variant W: sources in {wikipedia_en, wikidata}; variant T: taxonomy/MeSH only\\n  per concept: recognised_by_t0+8 = any event with t0 < year <= t0+8; lag = min(year) - t0 among year > t0; pre_recognised = any event year <= t0 (reported separately, excluded from the lag)\\n  per class (or per PC tercile) x split: the share recognised (concept bootstrap CI), median lag (bootstrap CI), cumulative incidence curves; per group, because Social and Eng have no taxonomy (use variant W there)\\n  pipeline_counts.json: works 476,196,327 -> base 129,360,390 -> verified matches 60,011,338 -> agg rows 19,670,571 (E5/scan/scan_info.json); lexicon 56,643; frame 12,499 by split; episodes 27,393; E6 risk-set rows and events (from its parquet row counts); this artifact: state rows, concept-years, DTW n, lineage sample (concepts, episodes, papers, refs resolved); every number read from files, never typed\\n\\nOUTPUTS\\n- state_sequences.parquet; panel.parquet; transitions.json; decomposition.json; trajectories.json; sequence_tests.json; lineage_check.json; external_timing.json; pipeline_counts.json; case_studies/; frozen_spec.json; logs/seal.log; deviations.json\\n- figures/ (PNG + PDF, via the aii-data-fig-gen house style):\\n  - decomposition waterfall (per split);\\n  - class medoid panels or PCA loading heat map;\\n  - DTW-HMM agreement matrix;\\n  - Sun-Abraham event-study plots (both directions);\\n  - cumulative incidence of first retention (intersection-born vs single-home);\\n  - lineage forest plot;\\n  - recognition incidence by class;\\n  - transition diagram.\\n- method_out.json in exp_gen_sol_out format: one example per concept, with input = concept summary and output = class/axis scores, events A/B, decomposition factors. Validate with aii-json; make the mini/preview variants and split with aii-file-size-limit if > limit.\\n- README.md and .aii/manifest.yaml: keep the results/figures/parquets; delete (regenerable) the .venv, the id-map memmap and scan parts from passes A/B, with source commands.\",\n  \"fallback_plan\": \"Each fallback is logged in deviations.json with the reason.\\n(1) EXP5 files missing or the volume not mounted: re-download agg_counts-equivalent counts by re-running a copy of E5 scan_full.py on the public S3 snapshot (33 min, 0 credits) with lexicon_v1. If lexicon_v1 is gone too, rebuild it with E5 lexicon.py (outcome-blind), and state that the frame is re-derived, not identical.\\n(2) arrays too large for RAM: build V only for the 12,499 frame ci (remap indices) with pyarrow filters on ci.\\n(3) DTW too slow (> 25 min projected): Sakoe-Chiba radius 1, or Euclidean distance on age-aligned vectors (sequences are already aligned on t0, so DTW mainly absorbs 1-yr shifts); select k on a random 3,000 DEV subsample, then assign the rest to the nearest medoid.\\n(4) HMM fails to converge or collapses states: switch to a CategoricalHMM on the concept-stage sequence (5 symbols), and use the optimal-matching view as the second method. If no two methods agree (ARI < 0.5), report the CONTINUUM (PCA). That is a pre-registered, publishable outcome ('no discrete trajectory types; a retention axis and a contact axis').\\n(5) pyfixest sunab unavailable or failing: implement the interaction-weighted estimator by hand (cohort x relative-age dummies, never-treated control, weights = cohort shares among treated at each relative age); cross-check with a stacked-DiD version.\\n(6) Too few never-treated concepts for the event study: use not-yet-treated controls (Callaway-Sant'Anna style) and report the switch.\\n(7) Snapshot PASS A over budget (> 60 min projected): restrict the lexicon to L and the held-out groups only, drop A1 for DEV (A' is then reported on held-out only), and keep A3 only for years 2000-2022.\\n(8) PASS B over budget: use a random file subset. If S3 is unreachable, use the reservoir fallback: E5/scan/reservoir has 12 hits per concept x era with file/row pointers; read referenced_works for only those files/rows. This is thin (<= 12 papers per concept per era), so pool episodes across concepts by status, and label it illustrative.\\n(9) Free OpenAlex singleton GETs (0 credits) are a last resort for <= 3,000 sampled work IDs' referenced_works, polite rate 5 req/s. They are never used for batch or filter calls, which cost credits.\\n(10) Recognition join coverage low (< 30% of frame concepts have any event): report coverage per group and restrict the timing analysis to variant W.\\n(11) Time overrun: the priority order is S1 > S2 > S3 > S4 > S9 > S8 > S7. Always write partial JSONs with status fields rather than nothing.\",\n  \"testing_plan\": \"T0 UNIT TESTS (tests/test_units.py; no network):\\n(a) states() on a hand-built 12-year x 27 array reproduces the expected ENTERED/RETAINED/LOST masks, including the home-field exclusion from RETAINED and the 2-year entry lag.\\n(b) The decomposition identity: for 1,000 random concepts, |log B - (log E2 + log M + log rho)| < 1e-9 where defined; group-level Bbar equals the factor product exactly; the Shapley shares sum to 1.\\n(c) Planted trajectories: simulate 600 synthetic concepts from 3 known generating regimes (fast contact / low retention; slow contact / high retention; spike and loss). DTW k-medoids and the HMM partition must each recover them with ARI >= 0.8, and choose_k must pick 3. A pure-noise panel must NOT pass the naming rule.\\n(d) Event study: a synthetic staggered panel with a planted +0.5 post-effect and no pre-trend recovers the effect with CI coverage; with zero effect, the placebo band covers 0 and the pre-trend test rejects at about 5% over 100 simulations; the mechanical-lag null equals the observed share when HP is shuffled.\\n(e) The lineage reference-share function on a toy id map; the Jaccard function.\\n(f) The seal refuses a second unseal and refuses if the spec hash changes.\\nT1 SMOKE on 200 random DEV concepts end to end (S1-S4, S8 for 1 case, S9) in < 10 min; inspect 5 concepts' state rasters by eye against their yearly field counts.\\nT2 CROSS-FRAME VALIDATION: for the EXP5 concepts that are also in EXP6 (overlap count logged), Spearman >= 0.8 between our n_ret(t) and EXP6 trajectories_dev.csv n_retaining. If lower, check the Y0 indexing and field-code offsets (vfield = id - 10; h2 uses id - 11 on g[:, 1:]) before anything else.\\nT3 SNAPSHOT PROBES: pass A on 3 files. Our TAG hit counts for frame concepts must match E5 agg_counts for the same files (file-level rebuild from E5/scan/parts/agg_*.npz if present, else aggregate totals) within 1%. The id-map coverage of cited works in 2000-2022 should be >= 70%. Time 5 files each for passes A and B and extrapolate before launching the full run.\\nT4 SCALE: aii-long-running-tasks staging for DTW (500 -> 2,000 -> all DEV), timing each.\\nT5 ROBUSTNESS: a second bootstrap seed moves the CI ends by < 0.01; a second k-medoids seed and HMM restart set give the same k and ARI within 0.05.\\nT6 PRE-UNSEAL CHECKLIST: no held-out ci in any object used for choices (assert log), frozen_spec hash logged, git commit made.\\nT7 INDEPENDENT RE-DERIVATION after the unseal: recompute the held-out decomposition shares and the forward hazard ratio with separate minimal code (pandas groupby + statsmodels GLM) and match to 1e-6 / 1e-3.\\nT8 SANITY: the class x volume-tercile ARI and the class x Medicine table are printed before any class is named.\"\n}\n", "numLines": 12, "startLine": 1, "totalLines": 12}}
```

### [9] TOOL CALL — Read · 2026-09-29 02:07:03 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/case_exemplars.json
```

### [10] TOOL RESULT — Read · 2026-09-29 02:07:03 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/case_exemplars.json", "content": "{\n \"indicator\": \"M0_density_end\",\n \"frozen_sign\": 1,\n \"pooled_psp\": 0.37697368862603964,\n \"high\": [\n  {\n   \"ci\": 11217,\n   \"name\": \"Coefficient of variation\",\n   \"group\": \"MATHDEC\",\n   \"t0\": 2009,\n   \"M0_density_end\": 0.6276053632178341,\n   \"O2r_resid\": 7.330695450573898,\n   \"O2r_m50\": 11.773460564786076,\n   \"logvol\": 4.290459441148391,\n   \"top10_W3_neighbours\": [\n    [\n     \"Advanced Statistical Process Monitoring\",\n     6.31,\n     5\n    ],\n    [\n     \"Scientific Measurement and Uncertainty Evaluation\",\n     5.88,\n     4\n    ],\n    [\n     \"Fatigue and fracture mechanics\",\n     4.52,\n     2\n    ]\n   ]\n  },\n  {\n   \"ci\": 53797,\n   \"name\": \"Cross disciplinary\",\n   \"group\": \"PHYS\",\n   \"t0\": 2005,\n   \"M0_density_end\": 0.5597559622191193,\n   \"O2r_resid\": 6.5244304442149454,\n   \"O2r_m50\": 11.17733934372574,\n   \"logvol\": 4.820281565605037,\n   \"top10_W3_neighbours\": [\n    [\n     \"Interdisciplinary Research and Collaboration\",\n     5.72,\n     3\n    ],\n    [\n     \"Diverse Interdisciplinary Research Innovations\",\n     5.32,\n     2\n    ],\n    [\n     \"Design Education and Practice\",\n     5.06,\n     4\n    ],\n    [\n     \"Advanced Memory and Neural Computing\",\n     4.44,\n     2\n    ],\n    [\n     \"Innovative Teaching and Learning Methods\",\n     4.2,\n     3\n    ],\n    [\n     \"Complex Systems and Decision Making\",\n     4.18,\n     2\n    ],\n    [\n     \"Entrepreneurship Studies and Influences\",\n     4.09,\n     2\n    ],\n    [\n     \"Neural Networks and Applications\",\n     3.9,", "numLines": 80, "startLine": 1, "totalLines": 321}}
```

### [11] TOOL CALL — Glob · 2026-09-29 02:07:13 UTC

```
Pattern: "*"
```

### [12] TOOL RESULT — Glob · 2026-09-29 02:07:13 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.aii_claude_session.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/config", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/HEAD", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/info/exclude", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/update.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/push-to-checkout.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/prepare-commit-msg.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-receive.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-rebase.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-push.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-merge-commit.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-commit.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/pre-applypatch.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/post-update.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/fsmonitor-watchman.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/commit-msg.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/hooks/applypatch-msg.sample", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/.git/description", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/field_backbone.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/topic_meta.csv", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/topic_ids.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/backbone/slice2.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/backbone/slice1.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/backbone/slice0.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/source_field.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/frozen_lexicon.sha256", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/lexicon_v1.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/snapshot/works_manifest.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/panel_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/frame_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/models_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/seal_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/stats_core.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/h2.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/common3.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego_exp3_orig.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/rangefile.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/matcher.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/common5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_0065.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_0065.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_0065.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_0065.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1407.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1407.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1407.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1407.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1125.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1125.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1125.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1125.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1918.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1918.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1918.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1918.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/tests/t1_check.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/t1_passA_exact_65_1125_1407_1918.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/logs/passA.pid", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1882.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1882.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1882.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1882.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1868.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1868.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1868.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1868.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1934.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1934.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1934.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1934.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1949.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1949.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1949.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1949.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1583.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1583.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1883.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1583.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1883.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1583.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1883.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1883.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1579.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1579.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1579.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1579.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1297.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1297.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1297.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1297.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1299.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1299.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1299.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1299.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1581.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/rs_1581.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/early_1581.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/agg_1581.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA/parts/done_1690.json"], "durationMs": 550, "numFiles": 100, "truncated": true, "totalMatches": 12871, "countIsComplete": true}
```

### [13] TOOL CALL — Grep · 2026-09-29 02:07:13 UTC

```
Pattern: "new_edge_rate|n_comm_W3|participation|NOV_res|ego_density_W3|edge_persistence|RETENTION_RATIO_early|CONTACT_REACH"
```

### [14] TOOL RESULT — Grep · 2026-09-29 02:07:13 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "18:CONTACT_REACH,FR,t0..t0+2,# off-home fields with >= 1 labelled work t0..t0+2,build_features.py,,,True,False\n20:RETENTION_RATIO_early,FR,t0..t0+2,\"RETAINED_REACH / max(CONTACT_REACH, 1)\",build_features.py,,,True,False\n31:NOV_res,A,t0..t0+2,NOV minus its degree-preserving expectation,Pass A + lib/ego.py,0.453345667591736,1.0,True,False\n38:new_edge_rate,A,t0..t0+2,(M/3) / (deg_W1 + 1),Pass A + lib/ego.py,0.147850473249739,1.0,True,False\n39:edge_persistence,A,t0..t0+2,\"mean Jaccard of neighbour sets W1-W2, W2-W3\",Pass A + lib/ego.py,-0.2510479605570467,-1.0,True,False\n41:participation,A,t0..t0+2,1 - sum of squared community shares of W3 neighbours,Pass A + lib/ego.py,0.5056228500855307,1.0,True,False\n42:n_comm_W3,A,t0..t0+2,# communities among W3 neighbours,Pass A + lib/ego.py,0.5009437583232178,1.0,False,False\n45:ego_density_W3,A,t0..t0+2,backbone edge density among W3 neighbours,Pass A + lib/ego.py,,,False,False", "numLines": 8, "totalLines": 8}
```

### [15] TOOL CALL — Glob · 2026-09-29 02:07:17 UTC

```
Pattern: "{lib/*,data/*,models/*,*.py,*.md}"
```

### [16] TOOL RESULT — Glob · 2026-09-29 02:07:17 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/panel_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/frame_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/models_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/seal_exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/stats_core.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/h2.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/common3.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego_exp3_orig.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/rangefile.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/matcher.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/common5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego_ctx.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/common.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/seal.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/rq1stats.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/design.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/o5_events.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/dev_select.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/method.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/bg_topics.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/counts_check.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ref_sample.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/passA_info.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/passB_targets.npy", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/frame_arrays.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/features_basic.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passB.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/build_features.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/indicators.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/cites_early.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/passB_info.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/heldout.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/outcomes.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/outcomes_sealed.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/outcomes_dev.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_features.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/rederive.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O1c.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O1c.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O2r_m50.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O2r_m50.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O2r_resid.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O2r_resid.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O4.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O4.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O1b.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O1b.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O3.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O3.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O5.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O5.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/linear_all_O5_WW.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models/ebm_O5_WW.joblib", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/analysis_table.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/outcomes.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/audit.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/make_outputs.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/readme_tables.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/reproducibility.md", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/README.md"], "durationMs": 198, "numFiles": 62, "truncated": false, "totalMatches": 62, "countIsComplete": true}
```

### [17] TOOL CALL — Glob · 2026-09-29 02:07:17 UTC

```
Pattern: "{results/*,lib/*,*.py}"
```

### [18] TOOL RESULT — Glob · 2026-09-29 02:07:17 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/stats_core.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/h2_exp6.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/cfg_exp6.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/exp5.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/seal.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/d3.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/models.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/analysis.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/audit.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/overlap_report.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/state_panel_dev.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/risk_sets_exp5_minus_exp6_dev.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/nulls_exp5_dev.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/step2_dev.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/risk_sets_exp6_extended_heldout.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/risk_sets_exp6_extended_dev.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/nulls_exp6_heldout.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/step1_exp6_robustness.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/frozen_spec.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/risk_sets_exp5_minus_exp6_heldout.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/state_panel_heldout.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/nulls_exp5_heldout_pooled4.npz", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/step2_heldout.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/audit.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/exploratory_lpm.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/exploratory_lpm.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/unit_tests_T0.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/outputs.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method.py", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/frontier_result.json", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/deviations.json"], "durationMs": 179, "numFiles": 31, "truncated": false, "totalMatches": 31, "countIsComplete": true}
```

### [19] TOOL CALL — Glob · 2026-09-29 02:07:21 UTC

```
Pattern: "data/*/*"
```

### [20] TOOL RESULT — Glob · 2026-09-29 02:07:21 UTC

```
{"filenames": ["/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/frame_matches_early/part_001.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00004.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00002.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00003.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00001.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00000.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00006.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00005.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00008.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00007.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00009.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00013.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00010.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00011.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00012.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_timing/chunk_00014.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00004.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00003.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00002.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00001.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00000.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00005.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00007.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00006.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00009.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00008.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00010.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00014.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00013.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00012.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts/chunk_00011.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00004.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00000.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00002.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00001.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00003.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00005.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00006.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00007.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00008.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00009.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00013.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00010.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00011.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00012.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00014.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00015.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00017.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00016.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00018.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00019.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00021.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00020.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00022.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00023.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00024.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00025.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00027.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00026.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00029.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00028.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00030.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00032.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00031.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00034.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00033.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00035.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00036.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00037.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00038.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00039.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00041.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00040.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00042.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00043.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00044.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00046.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00045.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00047.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00048.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00049.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00050.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00051.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00052.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00053.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00054.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00055.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00056.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00058.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00057.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00059.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00060.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00063.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00061.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00062.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00064.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00065.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00066.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00067.parquet", "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/ego_parts_c3/chunk_00068.parquet"], "durationMs": 189, "numFiles": 100, "truncated": true, "totalMatches": 344, "countIsComplete": true}
```

### [21] TOOL CALL — Read · 2026-09-29 02:07:21 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego.py
```

### [22] TOOL RESULT — Read · 2026-09-29 02:07:21 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib/ego.py", "content": "\"\"\"Co-occurrence ego-network indicators (family A), ported from art_yrradSC27HtQ features.concept_core.\n\nPort changes (all logged in results/deviations.json):\n  * windows are pluggable. RQ1 uses PRE = t0-3..t0-1, W1 = {t0}, W2 = {t0+1}, W3 = {t0+2}: the EXP3 W3 (t0+3..t0+4)\n    would leak past the t0..t0+2 feature window. new_edge_rate divides by the window length in years (3, not 5).\n  * the background comes from the context (Pass A BG/GT for RQ1; EXP3's ckpt for the port-validation test T0-8).\n  * betweenness uses a path-length cutoff (default 4) on the kNN backbone; N_NULL defaults to 200.\n  * dropped near-duplicate variants: D_lag, D_q, D_withself, F_bg; the per-field block is not needed.\n  * new: comm_entropy = Shannon entropy of the W3 neighbours' backbone-community weights.\nEverything else (PMI neighbour rule, SELF rule, the frequency-matched null of D_z, the multinomial null of F_res,\nNOV_res, participation, persistence, density, k-core, constraint) is the EXP3 code.\"\"\"\nfrom __future__ import annotations\n\nimport math\nimport warnings\nfrom collections import Counter\n\nimport igraph as ig\nimport numpy as np\n\nSELF_DF_MAX = 100\nSELF_SHARE = 0.20\nTOPN_F = 20\nR_RARE = 10\nSLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]\n\nC: dict = {}\n\n\ndef slice_of(y: int) -> int:\n    for i, (a, b) in enumerate(SLICES):\n        if a <= y <= b:\n            return i\n    return 0 if y < SLICES[0][0] else len(SLICES) - 1\n\n\ndef rq1_windows(t0: int) -> dict[str, list[int]]:\n    return {\"PRE\": [t0 - 3, t0 - 2, t0 - 1], \"W1\": [t0], \"W2\": [t0 + 1], \"W3\": [t0 + 2]}\n\n\ndef exp3_windows(t0: int) -> dict[str, list[int]]:\n    return {\"PRE\": [t0 - 3, t0 - 2, t0 - 1], \"W1\": [t0, t0 + 1], \"W2\": [t0 + 2], \"W3\": [t0 + 3, t0 + 4]}\n\n\ndef lgC(n: float, k: float) -> float:\n    from scipy.special import gammaln\n    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)\n\n\ndef set_context(ctx: dict) -> None:\n    \"\"\"ctx: nt, years (list), bg [len(years), nt], Gt {year: n}, comm/comm_q/deg/knn/full_edges per slice, subfield,\n    names, ldf (topic lemma df), tlem (topic lemma sets), lemmas (callable).\"\"\"\n    C.clear()\n    C.update(ctx)\n    C[\"graphs\"] = {}\n    C[\"yidx\"] = {y: i for i, y in enumerate(ctx[\"years\"])}\n\n\ndef knn_graph(s: int) -> ig.Graph:\n    if s not in C[\"graphs\"]:\n        ka, kb = C[\"knn\"][s]\n        C[\"graphs\"][s] = ig.Graph(n=C[\"nt\"], edges=list(zip(ka.tolist(), kb.tolist())), directed=False)\n    return C[\"graphs\"][s]\n\n\ndef bg_window(years: list[int]) -> tuple[np.ndarray, float]:\n    yi = [C[\"yidx\"][y] for y in years if y in C[\"yidx\"]]\n    return C[\"bg\"][yi].sum(axis=0).astype(float), float(sum(C[\"Gt\"].get(y, 0) for y in years))\n\n\ndef window_counts(works, years) -> tuple[np.ndarray, int]:\n    nck = np.zeros(C[\"nt\"], dtype=float)\n    ncw = 0\n    ys = set(years)\n    for y, tp in works:\n        if y in ys and len(tp):\n            ncw += 1\n            for k in tp:\n                nck[k] += 1\n    return nck, ncw\n\n\ndef pmi(nck, nc, nbg, N):\n    with np.errstate(divide=\"ignore\", invalid=\"ignore\"):\n        v = np.log(nck * N / (nc * nbg))\n    v[~np.isfinite(v)] = np.nan\n    return v\n\n\ndef neighbours(nck, nc, nbg, N, excl, min_n: int = 2):\n    p = pmi(nck, nc, nbg, N) if nc > 0 else np.full(C[\"nt\"], np.nan)\n    nb = (nck >= min_n) & (np.nan_to_num(p, nan=-1) > 0) & ~excl\n    return nb, p\n\n\ndef topS(nck, p, nb, top: int = TOPN_F):\n    idx = np.nonzero(nb)[0]\n    if len(idx) == 0:\n        return float(\"nan\"), 0\n    order = idx[np.lexsort((-p[idx], -nck[idx]))][:top]\n    return float(np.mean(p[order])), len(order)\n\n\ndef self_topics(name: str, aliases: list[str], n_early, nc_early) -> np.ndarray:\n    lem = C[\"lemmas\"]\n    sets = []\n    for ph in [name] + aliases:\n        cl = {l for l in lem(ph) if C[\"ldf\"].get(l, 0) <= SELF_DF_MAX}\n        if cl:\n            sets.append(cl)\n    lex = np.array([any(cl <= tl for cl in sets) for tl in C[\"tlem\"]])\n    share = n_early / nc_early if nc_early else np.zeros(C[\"nt\"])\n    return lex | (share >= SELF_SHARE)\n\n\ndef distinct_null(pool_idx, w, M, labels, rng, n):\n    if M <= 0 or len(pool_idx) == 0:\n        return np.zeros(n)\n    M = min(M, len(pool_idx))\n    lw = np.log(w[pool_idx])\n    out = np.empty(n)\n    lab = labels[pool_idx]\n    chunk = max(1, 2_000_000 // len(pool_idx))\n    for s in range(0, n, chunk):\n        m = min(chunk, n - s)\n        g = lw[None, :] + rng.gumbel(size=(m, len(pool_idx)))\n        top = np.argpartition(-g, M - 1, axis=1)[:, :M]\n        L = np.sort(lab[top], axis=1)\n        out[s:s + m] = 1 + (np.diff(L, axis=1) != 0).sum(axis=1)\n    return out\n\n\ndef f_null(p_mix, pool, T1, T3, nc1, nc3, nbg1, N1, nbg3, N3, rng, n):\n    if len(pool) == 0 or T1 == 0 or T3 == 0 or nc1 == 0 or nc3 == 0:\n        return np.full(n, np.nan)\n    pr = p_mix[pool] / p_mix[pool].sum()\n\n    def S(T, nc, nbg, N):\n        X = rng.multinomial(T, pr, size=n).astype(float)\n        with np.errstate(divide=\"ignore\", invalid=\"ignore\"):\n            P = np.log(X * N / (nc * nbg[pool][None, :]))\n        elig = (X >= 2) & np.isfinite(P) & (P > 0)\n        key = np.where(elig, X + 1e-6 * np.nan_to_num(P, nan=0, posinf=0, neginf=0), -np.inf)\n        order = np.argsort(-key, axis=1)[:, :TOPN_F]\n        Ps = np.take_along_axis(np.where(elig, P, np.nan), order, axis=1)\n        with np.errstate(invalid=\"ignore\"):\n            return np.nanmean(np.where(np.isfinite(Ps), Ps, np.nan), axis=1)\n    with warnings.catch_warnings():\n        warnings.simplefilter(\"ignore\", RuntimeWarning)\n        return S(T3, nc3, nbg3, N3) - S(T1, nc1, nbg1, N1)\n\n\ndef _centrality(idx: np.ndarray, s: int, cutoff: int | None) -> tuple[float, int, float]:\n    if len(idx) == 0:\n        return 0.0, 0, float(\"nan\")\n    g = knn_graph(s).copy()\n    g.add_vertices(1)\n    v = g.vcount() - 1\n    g.add_edges([(v, int(k)) for k in idx])\n    n = g.vcount()\n    b = g.betweenness(vertices=[v], directed=False, cutoff=cutoff)[0]\n    return b / ((n - 1) * (n - 2) / 2), int(g.coreness()[v]), float(g.constraint(vertices=[v])[0])\n\n\ndef concept_core(name: str, aliases: list[str], t0: int, works, n_null: int, seed: int, windows=rq1_windows,\n                 btw_cutoff: int | None = 4, nb_min_w: int = 2) -> dict:\n    \"\"\"All family-A indicators for one concept. works = [(year, tuple of topic indices)].\"\"\"\n    rng = np.random.default_rng(seed)\n    win = windows(t0)\n    early_years = sorted(set(win[\"W1\"] + win[\"W2\"] + win[\"W3\"]))\n    n_early, nc_early = window_counts(works, early_years)\n    SELF = self_topics(name, aliases, n_early, nc_early)\n    cnt, nc, bgw, NW, NB, P = {}, {}, {}, {}, {}, {}\n    for w, ys in win.items():\n        cnt[w], nc[w] = window_counts(works, ys)\n        bgw[w], NW[w] = bg_window(ys)\n    nbg_early, _ = bg_window(early_years)\n    for w in (\"W1\", \"W2\", \"W3\"):\n        NB[w], P[w] = neighbours(cnt[w], nc[w], bgw[w], NW[w], SELF, nb_min_w)\n    pre_set = cnt[\"PRE\"] >= 1\n    new = (NB[\"W1\"] | NB[\"W2\"] | NB[\"W3\"]) & ~pre_set\n    new_idx = np.nonzero(new)[0]\n    M = len(new_idx)\n    first_year = {}\n    for y in early_years:\n        cy, _ = window_counts(works, [y])\n        for k in new_idx:\n            if k not in first_year and cy[k] >= 1:\n                first_year[k] = y\n    pool = np.nonzero((nbg_early > 0) & ~pre_set & ~SELF)[0]\n    s_mid = slice_of(early_years[len(early_years) // 2])\n    r: dict = {\"M\": M, \"n_self_topics\": int(SELF.sum()), \"nc_PRE\": nc[\"PRE\"], \"nc_W1\": nc[\"W1\"], \"nc_W2\": nc[\"W2\"],\n               \"nc_W3\": nc[\"W3\"]}\n\n    def dz(labels_by_slice, pool_idx, new_list):\n        if M < 3:\n            return float(\"nan\"), float(\"nan\"), float(\"nan\"), None\n        labs = [labels_by_slice[slice_of(first_year.get(k, t0))][k] for k in new_list]\n        obs = len(set(labs))\n        nl = distinct_null(pool_idx, nbg_early, len(new_list), labels_by_slice[s_mid], rng, n_null)\n        mu, sd = nl.mean(), nl.std()\n        return (obs - mu) / sd if sd > 0 else 0.0, obs / mu if mu > 0 else float(\"nan\"), obs, labs\n\n    r[\"D_z\"], r[\"D_ratio\"], r[\"D_obs\"], labs = dz(C[\"comm\"], pool, new_idx)\n    S1, k1 = topS(cnt[\"W1\"], P[\"W1\"], NB[\"W1\"])\n    S3, k3 = topS(cnt[\"W3\"], P[\"W3\"], NB[\"W3\"])\n    obs_g = S3 - S1\n    pooled = cnt[\"W1\"] + cnt[\"W2\"] + cnt[\"W3\"]\n    mixpool = np.nonzero((pooled > 0) & ~SELF)[0]\n    T1 = int(cnt[\"W1\"][~SELF].sum())\n    T3 = int(cnt[\"W3\"][~SELF].sum())\n    ng = f_null(pooled, mixpool, T1, T3, nc[\"W1\"], nc[\"W3\"], bgw[\"W1\"], NW[\"W1\"], bgw[\"W3\"], NW[\"W3\"], rng,\n                n_null)\n    ok = np.isfinite(ng)\n    if np.isfinite(obs_g) and ok.sum() >= 20:\n        r[\"F_res\"] = obs_g - ng[ok].mean()\n        sdn = ng[ok].std()\n        r[\"F_z\"] = r[\"F_res\"] / sdn if sdn > 0 else 0.0\n    else:\n        r[\"F_res\"] = r[\"F_z\"] = float(\"nan\")\n    if M >= R_RARE and labs is not None:\n        cc = np.array(list(Counter(labs).values()), dtype=float)\n        r[\"D_rare\"] = float(sum(1 - math.exp(lgC(M - m, R_RARE) - lgC(M, R_RARE)) if M - m >= R_RARE else 1.0\n                                for m in cc))\n    else:\n        r[\"D_rare\"] = float(\"nan\")\n    sub3 = [C[\"subfield\"]] * len(SLICES)\n    r[\"D_sub\"], _, _, _ = dz(sub3, pool, new_idx)\n    # novelty vs degree-preserving expectation\n    s0 = slice_of(t0)\n    comm0 = C[\"comm\"][s0]\n    w1 = cnt[\"W1\"]\n    if w1.sum() > 0:\n        cs = Counter()\n        for k in np.nonzero(w1)[0]:\n            cs[comm0[k]] += w1[k]\n        C0 = cs.most_common(1)[0][0]\n        if M > 0:\n            r[\"NOV\"] = float(np.mean([C[\"comm\"][slice_of(first_year.get(k, t0))][k] != C0 for k in new_idx]))\n            dg = C[\"deg\"][s0][pool].astype(float)\n            E = dg[comm0[pool] != C0].sum() / dg.sum() if dg.sum() > 0 else float(\"nan\")\n            r[\"NOV_res\"] = r[\"NOV\"] - E\n        else:\n            r[\"NOV\"] = r[\"NOV_res\"] = float(\"nan\")\n    else:\n        r[\"NOV\"] = r[\"NOV_res\"] = float(\"nan\")\n    n1, n3 = NB[\"W1\"].sum(), NB[\"W3\"].sum()\n    r[\"deg_W1\"], r[\"deg_W3\"] = int(n1), int(n3)\n    r[\"deg_growth\"] = math.log(n3 + 1) - math.log(n1 + 1)\n    sp1 = np.nansum(P[\"W1\"][NB[\"W1\"]])\n    sp3 = np.nansum(P[\"W3\"][NB[\"W3\"]])\n    r[\"str_growth\"] = math.log(sp3 + 1) - math.log(sp1 + 1)\n    n_years = len(early_years)\n    r[\"new_edge_rate\"] = (M / float(n_years)) / (n1 + 1)\n\n    def jac(a, b):\n        u = (a | b).sum()\n        return (a & b).sum() / u if u else float(\"nan\")\n    with warnings.catch_warnings():\n        warnings.simplefilter(\"ignore\", RuntimeWarning)\n        r[\"edge_persistence\"] = float(np.nanmean([jac(NB[\"W1\"], NB[\"W2\"]), jac(NB[\"W2\"], NB[\"W3\"])]))\n    r[\"turnover\"] = float((NB[\"W1\"] & ~NB[\"W3\"]).sum() / n1) if n1 else float(\"nan\")\n    s4 = slice_of(win[\"W3\"][-1])\n    if n3 > 0:\n        ws = Counter()\n        for k in np.nonzero(NB[\"W3\"])[0]:\n            ws[C[\"comm\"][s4][k]] += cnt[\"W3\"][k]\n        tot = sum(ws.values())\n        pw = np.array([v / tot for v in ws.values()])\n        r[\"participation\"] = float(1 - (pw ** 2).sum())\n        r[\"n_comm_W3\"] = len(ws)\n        r[\"comm_entropy\"] = float(-(pw * np.log(pw)).sum())\n    else:\n        r[\"participation\"], r[\"n_comm_W3\"], r[\"comm_entropy\"] = float(\"nan\"), 0, float(\"nan\")\n    dom = []\n    for w in (\"W1\", \"W2\", \"W3\"):\n        s = slice_of(win[w][0])\n        if cnt[w].sum() > 0:\n            cs = Counter()\n            for k in np.nonzero(cnt[w])[0]:\n                cs[C[\"comm\"][s][k]] += cnt[w][k]\n            dom.append(cs.most_common(1)[0][0])\n    r[\"comm_transitions\"] = sum(1 for a, b in zip(dom, dom[1:]) if a != b)\n    for w, s in ((\"W1\", s0), (\"W3\", s4)):\n        idx = np.nonzero(NB[w])[0]\n        if len(idx) >= 2:\n            a, b = C[\"full_edges\"][s]\n            ins = np.zeros(C[\"nt\"], dtype=bool)\n            ins[idx] = True\n            e = int((ins[a] & ins[b]).sum())\n            r[f\"ego_density_{w}\"] = e / (len(idx) * (len(idx) - 1) / 2)\n        else:\n            r[f\"ego_density_{w}\"] = float(\"nan\")\n    r[\"ego_density_change\"] = r[\"ego_density_W3\"] - r[\"ego_density_W1\"]\n    b0, _, c0 = _centrality(np.nonzero(NB[\"W1\"])[0], s0, btw_cutoff)\n    b4, k4, c4 = _centrality(np.nonzero(NB[\"W3\"])[0], s4, btw_cutoff)\n    r[\"btw_start\"], r[\"btw_end\"], r[\"kcore_end\"] = b0, b4, k4\n    r[\"btw_change\"] = b4 - b0\n    r[\"constraint_end\"] = c4\n    r[\"constraint_change\"] = c4 - c0\n    idx = np.nonzero(NB[\"W3\"])[0]\n    top = idx[np.argsort(-P[\"W3\"][idx])][:10]\n    r[\"_top_nb_W3\"] = [(C[\"names\"][k], round(float(P[\"W3\"][k]), 2), int(cnt[\"W3\"][k])) for k in top]\n    return r\n\n\nEGO_OUT = [\"D_z\", \"D_ratio\", \"D_rare\", \"D_sub\", \"D_obs\", \"NOV\", \"NOV_res\", \"F_res\", \"F_z\", \"deg_W1\", \"deg_W3\",\n           \"deg_growth\", \"str_growth\", \"new_edge_rate\", \"edge_persistence\", \"turnover\", \"participation\", \"n_comm_W3\",\n           \"comm_entropy\", \"comm_transitions\", \"ego_density_W3\", \"ego_density_change\", \"btw_end\", \"btw_change\",\n           \"kcore_end\", \"constraint_end\", \"constraint_change\"]\n", "numLines": 311, "startLine": 1, "totalLines": 311}}
```

### [23] ASSISTANT · 2026-09-29 02:07:27 UTC

```
Reading the prior artifacts (EXP7 state panel, EXP8 ego code) so the plan can point at real files. Then I'll write the plan JSON.
```

### [24] TOOL CALL — Read · 2026-09-29 02:07:27 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/d3.py
```

### [25] TOOL RESULT — Read · 2026-09-29 02:07:27 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/d3.py", "content": "\"\"\"D3 field-year state machine, RCA portfolios and concept x field entry risk sets, vectorised over concepts.\n\nSemantics are EXACTLY those of EXP6 lib/h2.py (copied verbatim to lib/h2_exp6.py):\n  entered(t)  = cumulative grounded count >= min_n\n  retaining(t)= entered(t-2) & w3(t) >= min_n & off-home          (w3 = count over t-2..t)\n  lost(t)     = entered(t) & w3(t) == 0                           (off-home filter applied at risk-set time)\n  risk set    = concept-year strata t = t0+1..min(t0+horizon, 2022); candidates = ~entered(t-1) & off-home;\n                event = entered(t) & candidate.\nEverything that EXP6 computes per row is computed here as (per-stratum field mask) @ phi, gathered at the target\nfield k, which makes permutation / rewiring nulls a single matrix product.\n\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\nimport pandas as pd\n\nY0, Y1 = 1995, 2022\nNY = Y1 - Y0 + 1\nNF = 26\n\n\n# ----------------------------------------------------------------------------- states\ndef panel_states(G: np.ndarray, home_mask: np.ndarray, min_n: float = 2) -> dict[str, np.ndarray]:\n    \"\"\"G [C, NY, 27] grounded counts (slot 0 = unlabelled venue); home_mask [C, 26] bool.\n    Returns [C, NY, 26] arrays (bool / int16 / float32).\"\"\"\n    x = G[:, :, 1:].astype(np.float64)\n    cum = np.cumsum(x, 1)\n    entered = cum >= min_n\n    w3 = x.copy()\n    w3[:, 1:] += x[:, :-1]\n    w3[:, 2:] += x[:, :-2]\n    ent_lag2 = np.zeros_like(entered)\n    ent_lag2[:, 2:] = entered[:, :-2]\n    offhome = ~home_mask\n    retaining = ent_lag2 & (w3 >= min_n) & offhome[:, None, :]\n    lost = entered & (w3 == 0)\n    yr = np.arange(NY, dtype=np.int16)\n    first = np.where(entered.any(1), entered.argmax(1), NY).astype(np.int16)  # [C, 26]\n    age = (yr[None, :, None] - first[:, None, :]).astype(np.int16)          # valid where entered\n    lastpos = np.maximum.accumulate(np.where(x > 0, yr[None, :, None], -1), axis=1).astype(np.int16)\n    tenure = (lastpos - first[:, None, :]).astype(np.int16)                  # tenure of a LOST presence\n    return {\"x\": x.astype(np.float32), \"cum\": cum.astype(np.float32), \"w3\": w3.astype(np.float32),\n            \"entered\": entered, \"ent_lag2\": ent_lag2, \"retaining\": retaining, \"lost\": lost,\n            \"offhome\": offhome, \"age\": age, \"tenure\": tenure, \"first\": first}\n\n\ndef rca_entered_panel(G: np.ndarray, GF: np.ndarray, min_n: float = 2) -> np.ndarray:\n    \"\"\"Vectorised h2_exp6.rca_entered: cum >= 2 AND cumulative share > field's cumulative share of all works; absorbing.\"\"\"\n    x = np.cumsum(G[:, :, 1:].astype(np.float64), 1)\n    tot = x.sum(2, keepdims=True)\n    F = np.cumsum(GF.astype(np.float64), 0)\n    share_all = F / np.maximum(F.sum(1, keepdims=True), 1)\n    share_c = x / np.maximum(tot, 1)\n    ok = (x >= min_n) & (share_c > share_all[None])\n    return np.maximum.accumulate(ok.astype(np.int8), 1).astype(bool)\n\n\ndef _rca(nc: np.ndarray, NT: np.ndarray) -> np.ndarray:\n    \"\"\"nc [..., 26] concept counts, NT [..., 26] base totals broadcastable. RCA = (nc/sum nc) / (NT/sum NT); 0 if nc empty.\"\"\"\n    s = nc.sum(-1, keepdims=True)\n    share_c = nc / np.where(s > 0, s, 1)\n    share_all = NT / np.maximum(NT.sum(-1, keepdims=True), 1)\n    return np.where(s > 0, share_c / np.where(share_all > 0, share_all, np.inf), 0.0)\n\n\ndef rolling(a: np.ndarray, w: int, axis: int) -> np.ndarray:\n    \"\"\"sum over the trailing window [y-w+1, y] (partial at the start).\"\"\"\n    c = np.cumsum(a, axis)\n    out = c.copy()\n    sl = [slice(None)] * a.ndim\n    sl2 = [slice(None)] * a.ndim\n    sl[axis] = slice(w, None)\n    sl2[axis] = slice(None, -w)\n    out[tuple(sl)] = c[tuple(sl)] - c[tuple(sl2)]\n    return out\n\n\ndef rca_panel(x: np.ndarray, GF: np.ndarray) -> dict[str, np.ndarray]:\n    \"\"\"x [C, NY, 26] counts; GF [NY, 26] venue-field base totals. Portfolio masks [C, NY, 26] evaluated AT year y\n    (the risk-set code reads them at y = t-1). RCA > 1 (strict).\"\"\"\n    x = x.astype(np.float64)\n    GF = GF.astype(np.float64)\n    r1 = _rca(x, GF[None])\n    xw, Gw = rolling(x, 3, 1), rolling(GF, 3, 0)\n    rw = _rca(xw, Gw[None])\n    rc = _rca(np.cumsum(x, 1), np.cumsum(GF, 0)[None])\n    Uw = rw > 1\n    Uw_prev = np.zeros_like(Uw)\n    Uw_prev[:, 3:] = Uw[:, :-3]                 # window y-5..y-3\n    return {\"U_1y\": r1 > 1, \"U_w3\": Uw, \"U_cum\": rc > 1, \"U_pers\": Uw & Uw_prev, \"rca_1y\": r1.astype(np.float32),\n            \"ties_1y\": int(np.isclose(r1, 1.0, rtol=0, atol=1e-12).sum())}\n\n\n# ----------------------------------------------------------------------------- strata\nSTRATUM_MASKS = [\"E\", \"ENTOFF\", \"RET\", \"LOST\", \"POOL\", \"HOME\", \"U_1y\", \"U_w3\", \"U_cum\", \"U_pers\",\n                 \"RET_a2\", \"RET_a3\", \"RET_a4p\", \"LOST_s\", \"LOST_l\"]\n\n\ndef build_strata(frame: pd.DataFrame, G: np.ndarray, GF: np.ndarray, *, horizon: int = 10, min_n: float = 2,\n                 entry_def: str = \"count\") -> dict:\n    \"\"\"frame rows aligned with G (row i <-> G[i]); needs columns cidx, t0, home_list (list[int]).\n    Returns per-stratum arrays (masks [S, 26] at t-1, counts, candidates, events) + stratum meta.\"\"\"\n    C = len(frame)\n    home = np.zeros((C, NF), bool)\n    for i, hl in enumerate(frame.home_list):\n        for h in hl:\n            home[i, h - 11] = True\n    S = panel_states(G, home, min_n)\n    R = rca_panel(S[\"x\"], GF)\n    ent = rca_entered_panel(G, GF, min_n) if entry_def == \"rca\" else S[\"entered\"]\n    t0 = frame.t0.to_numpy().astype(int)\n    ci_l, t_l = [], []\n    for i in range(C):\n        for t in range(t0[i] + 1, min(t0[i] + horizon, Y1) + 1):\n            ci_l.append(i); t_l.append(t)\n    ci = np.array(ci_l, np.int64)\n    t = np.array(t_l, np.int64)\n    ti = t - Y0\n    p = ti - 1                                                  # state row t-1\n    E = ent[ci, p]", "numLines": 120, "startLine": 1, "totalLines": 249}}
```

### [26] TOOL CALL — Grep · 2026-09-29 02:07:27 UTC

```
Pattern: "frame_matches_early|ego_features|O2r_resid|home_only|analysis_table"
```

### [27] TOOL RESULT — Grep · 2026-09-29 02:07:27 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "42:**O2r_resid**\n140:| O2r_resid | 1833 | 0.704 | 0.738 [+0.023, +0.047] | 0.763 [+0.047, +0.071] | 0.756 [+0.038, +0.066] |\n154:| P4 | RETENTION_RATIO_early and FRONTIER_POTENTIAL: pooled psp > 0 with CI > 0 for O2r_resid AND O1c | **FAILS** |\n166:1. **Breadth (O2r_m50 / O2r_resid, rarefied venue-field richness at t0+6..t0+8) is predictable beyond B5, and the\n167:   signal travels.** 7 (O2r_m50) and 8 (O2r_resid) of the frozen top 10 are confirmed (Holm p < 0.05; every\n193:   B5-minus-reach (+0.223 for O2r_resid); P4 fails because `RETENTION_RATIO_early` is **negative** (-0.120).\n195:   O2r_m30, or using EXP5's own O2r_resid definition (O2r_resid_N); excluding intersection-born concepts halves\n199:here touched held-out rows; G, G_A and G_btw were scored once before on O2r_resid and are flagged \"prev. scored\".\n220:| `outcomes.py` | one outcome table (O1c, O1b, O2r_m50/m30, O2r_resid, O3, O4, O5, O5_WW) and the outcome seal |\n236:| `data/frame_matches_early/part_*.parquet` | **kept**: grounded frame hits t0-3..t0+2 with work, topic and author ids |\n239:| `data/features_basic.parquet`, `data/ego_features.parquet` | families E/F/G/FR/S and A |\n240:| `data/outcomes_dev.parquet`, `data/outcomes_sealed.parquet`, `data/outcomes.parquet`, `data/analysis_table.parquet` | outcome tables (sealed file hashed in `logs/outcome_seal.log`) |\n251:| `results/portability_table.csv` | every indicator (+B5) x 10 units x {O2r_m50, O2r_resid, O1c}: psp, CI, raw Spearman; FROZEN/EXPLORATORY; previously_scored |\n271:- O2r_resid follows the plan (O2r_m50 on early logvol, DEV fit a = 2.741, b = 0.397). EXP5's constants belong to a\n272:  different formula (O2r_m30 on log outcome volume); that definition is reported as sensitivity `O2r_resid_N`.\n278:- Kept artifacts stay on the run's volume; `data/frame_matches_early/part_001.parquet` and `models/` are under\n316:`./restore.sh --ego`. Their merged outputs (`data/frame_matches_early/`, `data/cites_early.parquet`,\n317:`data/ego_features.parquet`) are kept and published.", "numLines": 18, "totalLines": 18}
```

### [28] TOOL CALL — Grep · 2026-09-29 02:07:31 UTC

```
Pattern: "early_|vfield|source|topics|author"
```

### [29] TOOL RESULT — Grep · 2026-09-29 02:07:31 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "10:  BG[year, topic]  base works per topic per year (1995-2022, 4,516 topics of EXP3 topic_ids.json); GT[year] = base\n12:  CNT              grounded (tagstate 1) frame hits keyed (ci, year, vfield) for years 2000-2016 -> check A1\n13:  EARLY rows       grounded frame hits with t0-3 <= year <= t0+2: (ci, year, work_id, vfield, topic idx list,\n14:                   author ids [only year >= t0], cited_by_count)\n15:  RSAMPLE          base works 2003-2016 with splitmix64(fi<<32 | row) % 400 == 0: (work_id, year, vfield,\n38:                    setup_logger, source_field_lut, works_files, write_parquet_parts)\n40:COLS = [\"title\", \"publication_year\", \"type\", \"is_paratext\", \"is_xpac\", \"primary_location.source.id\",\n41:        \"topics.list.element.field.id\", \"primary_topic.field.id\", \"concepts.list.element.id\",\n43:        \"id\", \"topics.list.element.id\", \"authorships.list.element.author.id\", \"cited_by_count\"]\n53:    sid, code = source_field_lut()\n102:    src = pl.field(\"source\").field(\"id\")\n106:    vfield = np.where(_W[\"sid\"][pos] == sidn, _W[\"code\"][pos], 0).astype(np.int64)\n109:    # topics -> topic index (EXP3 order)\n110:    tflat, toff = _list_offsets(tb.column(\"topics\"))\n126:    rsdf = pd.DataFrame({\"work_id\": wid[rs], \"year\": year[rs].astype(np.int16), \"vfield\": vfield[rs].astype(np.int8),\n163:    cnt_key = (g_ci * 32 + (gy - Y0)) * 32 + vfield[g_row]\n171:        aflat, aoff = _list_offsets(tb.column(\"authorships\"))\n172:        aid = _oa_int(aflat.field(\"author\").field(\"id\"), 22, \"https://openalex.org/A0\")\n182:                        \"vfield\": vfield[e_row].astype(np.int8), \"topics\": tops, \"authors\": auths,\n188:    edf.to_parquet(PASSA / f\"early_{fi:04d}.parquet\", index=False)\n209:        early.append(pd.read_parquet(PASSA / f\"early_{fi:04d}.parquet\"))\n215:    pd.DataFrame({\"ci\": ci.astype(np.int32), \"year\": (yy + Y0).astype(np.int16), \"vfield\": vf.astype(np.int8),\n217:    np.savez_compressed(DATA / \"bg_topics.npz\", BG=BG, GT=GT, years=np.arange(Y0, Y1 + 1))\n225:            \"early_rows\": int(len(edf))}", "numLines": 24, "totalLines": 24}
```

### [30] TOOL CALL — Read · 2026-09-29 02:08:33 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/topic_meta.csv
```

### [31] TOOL RESULT — Read · 2026-09-29 02:08:33 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/topic_meta.csv", "content": "topic,name,subfield,subfield_name,field,field_name,keywords\n10001,Geological and Geochemical Analysis,1908,Geophysics,19,Earth and Planetary Sciences,Zircon; Geochronology; Tectonics; Granitic Rocks; Isotopic Composition; Subduction Zones; Mantle Evolution; Plate Tectonics; Thermodynamic Modeling; Continental Growth\n10002,Advanced Chemical Physics Studies,3107,\"Atomic and Molecular Physics, and Optics\",31,Physics and Astronomy,Density Functional Theory; Dispersion Correction; Ab Initio Parametrization; Wavefunction Analyzer; Semiempirical Methods; Van der Waals Interactions; Continuum Solvation Models; Hybrid Density Functionals; Molecular Simulations; Electronic Structure Calculations", "numLines": 3, "startLine": 1, "totalLines": 4518}}
```

### [32] TOOL CALL — Read · 2026-09-29 02:08:33 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/preview_data_out.json
```

### [33] TOOL RESULT — Read · 2026-09-29 02:08:33 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/preview_data_out.json", "content": "{\n \"datasets\": [\n  {\n   \"dataset\": \"concept_recognition\",\n   \"examples\": [\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C144501496\\\", \\\"qid\\\": \\\"Q5533489\\\", \\\"qid_resolved\\\": \\\"Q5533489\\\", \\\"label\\\": \\\"Genome editing\\\", \\\"label_norm\\\": \\\"genome editing\\\", \\\"aliases\\\": [\\\"genome editing\\\", \\\"Genome engineering\\\"], \\\"aliases_norm\\\": [\\\"genome engineering\\\"], \\\"acronyms\\\": [], \\\"level\\\": 4, \\\"ancestor_ids\\\": [\\\"C98108389\\\", \\\"C141231307\\\",...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"nature_methods_moty\\\", \\\"event_type\\\": \\\"nature_methods_method_of_the_year\\\", \\\"year\\\": 2011, \\\"date\\\": null, \\\"date_precision\\\": 9, \\\"year_usable\\\": true, \\\"match_method\\\": \\\"embed+llm\\\", \\\"match_confidence\\\": 0.85, \\\"relation\\\": \\\"broader\\\", \\\"entry_id\\\": \\\"nature_methods_moty:2011:1.0:4\\\", \\\"detail\\\":...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 4,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\"\n     ],\n     \"metadata_n_events\": 11,\n     \"metadata_n_events_year_usable\": 10,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C144501496\",\n     \"metadata_qid\": \"Q5533489\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C46111723\\\", \\\"qid\\\": \\\"Q471857\\\", \\\"qid_resolved\\\": \\\"Q471857\\\", \\\"label\\\": \\\"Proteomics\\\", \\\"label_norm\\\": \\\"proteomic\\\", \\\"aliases\\\": [\\\"proteomics\\\"], \\\"aliases_norm\\\": [], \\\"acronyms\\\": [], \\\"level\\\": 3, \\\"ancestor_ids\\\": [\\\"C104317684\\\", \\\"C55493867\\\", \\\"C54355233\\\", \\\"C86803240\\\", \\\"C185592680\\\"], \\\"level0_discipli...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"wikipedia_en\\\", \\\"event_type\\\": \\\"wikipedia_page_created_estimated\\\", \\\"year\\\": 2002, \\\"date\\\": \\\"2002-06-05\\\", \\\"date_precision\\\": \\\"estimated\\\", \\\"year_usable\\\": true, \\\"match_method\\\": \\\"wikidata_sitelink\\\", \\\"match_confidence\\\": 0.8, \\\"relation\\\": \\\"same\\\", \\\"entry_id\\\": null, \\\"detail\\\": {\\\"title\\\": \\\"Pr...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 3,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\"\n     ],\n     \"metadata_n_events\": 9,\n     \"metadata_n_events_year_usable\": 9,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C46111723\",\n     \"metadata_qid\": \"Q471857\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C152662350\\\", \\\"qid\\\": \\\"Q815297\\\", \\\"qid_resolved\\\": \\\"Q815297\\\", \\\"label\\\": \\\"Systems biology\\\", \\\"label_norm\\\": \\\"systems biology\\\", \\\"aliases\\\": [\\\"systems biology\\\", \\\"systems approach to biology\\\", \\\"system biology\\\"], \\\"aliases_norm\\\": [\\\"system biology\\\", \\\"systems approach to biology\\\"], \\\"acronyms\\\": [], ...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"wikipedia_en\\\", \\\"event_type\\\": \\\"wikipedia_page_created_estimated\\\", \\\"year\\\": 2004, \\\"date\\\": \\\"2004-02-13\\\", \\\"date_precision\\\": \\\"estimated\\\", \\\"year_usable\\\": true, \\\"match_method\\\": \\\"wikidata_sitelink\\\", \\\"match_confidence\\\": 0.8, \\\"relation\\\": \\\"same\\\", \\\"entry_id\\\": null, \\\"detail\\\": {\\\"title\\\": \\\"Sy...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 2,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\",", "numLines": 60, "startLine": 1, "totalLines": 1106}}
```

### [34] TOOL CALL — Grep · 2026-09-29 02:08:33 UTC

```
Pattern: "def |set_context|ego_ctx"
```

### [35] TOOL RESULT — Grep · 2026-09-29 02:08:33 UTC

```
{"mode": "content", "numFiles": 0, "filenames": [], "content": "40:def yi(y: int) -> int:\n44:def home_list(h) -> list[int]:\n49:def states(g: np.ndarray, home: list[int], min_n: int = 2) -> dict:\n65:def rca_entered(g: np.ndarray, GF: np.ndarray) -> np.ndarray:\n76:def load_arrays(fr: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:\n92:def social(e: pd.DataFrame, home_codes: set[int]) -> dict:\n106:    def find(x):\n130:def stage_basic(logger) -> None:\n209:def _init_ego() -> None:\n211:    from ego_ctx import rq1_context\n212:    ego.set_context(rq1_context())\n216:def ego_chunk(chunk_id: int, jobs: list, n_null: int, btw_cutoff: int, nb_min_w: int) -> tuple[int, list, float]:\n232:def ego_jobs(fr: pd.DataFrame) -> list:\n242:def stage_ego(logger, workers: int, limit: int = 0, timing: int = 0, n_null: int = N_NULL,\n274:def stage_assemble(logger) -> None:\n287:def main() -> None:", "numLines": 16, "totalLines": 16}
```

### [36] TOOL CALL — Read · 2026-09-29 02:08:35 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/build_features.py
```

### [37] TOOL RESULT — Read · 2026-09-29 02:08:35 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/build_features.py", "content": "    df = pd.DataFrame(rows).merge(basic.drop(columns=[\"concept_id\"]), on=\"ci\", how=\"left\")\n    df.to_parquet(DATA / \"features_basic.parquet\", index=False)\n    logger.info(f\"basic families: {df.shape}\")\n\n\n# ----------------------------------------------------------------------------- family A (parallel)\n_CTX_LOADED = {\"ok\": False}\n\n\ndef _init_ego() -> None:\n    import ego\n    from ego_ctx import rq1_context\n    ego.set_context(rq1_context())\n    _CTX_LOADED[\"ok\"] = True\n\n\ndef ego_chunk(chunk_id: int, jobs: list, n_null: int, btw_cutoff: int, nb_min_w: int) -> tuple[int, list, float]:\n    import ego\n    t = time.time()\n    out = []\n    for ci, name, aliases, t0, works in jobs:\n        try:\n            r = ego.concept_core(name, aliases, t0, works, n_null, SEED + int(ci), btw_cutoff=btw_cutoff,\n                                 nb_min_w=nb_min_w)\n            r[\"_top_nb_W3\"] = json.dumps(r[\"_top_nb_W3\"])\n        except (ValueError, IndexError, ZeroDivisionError) as e:\n            r = {\"ego_error\": repr(e)[:200]}\n        r[\"ci\"] = int(ci)\n        out.append(r)\n    return chunk_id, out, time.time() - t\n\n\ndef ego_jobs(fr: pd.DataFrame) -> list:\n    em = read_parquet_parts(DATA / \"frame_matches_early\", columns=[\"ci\", \"year\", \"topics\"])\n    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics])) for ci, d in em.groupby(\"ci\")}\n    jobs = []\n    for r in fr.itertuples():\n        al = [a for a in str(r.aliases_used).split(\"|\") if a and a != \"nan\"]\n        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, [])))\n    return jobs\n\n\ndef stage_ego(logger, workers: int, limit: int = 0, timing: int = 0, n_null: int = N_NULL,\n              btw_cutoff: int = BTW_CUTOFF, nb_min_w: int = 2, chunk: int = 40, subset: list[int] | None = None) -> dict:\n    fr = load_frame()\n    if subset is not None:\n        fr = fr[fr.ci.isin(subset)]\n    if timing:\n        fr = fr[fr.split == \"DEV\"].sample(timing, random_state=SEED)\n    jobs = ego_jobs(fr)\n    if limit:\n        jobs = jobs[:limit]\n    outdir = EGO_DIR if not timing else DATA / \"ego_timing\"\n    outdir.mkdir(parents=True, exist_ok=True)\n    chunks = [jobs[i:i + chunk] for i in range(0, len(jobs), chunk)]\n    todo = [k for k in range(len(chunks)) if not (outdir / f\"chunk_{k:05d}.parquet\").exists()] if not timing \\\n        else list(range(len(chunks)))\n    logger.info(f\"ego: {len(jobs)} concepts, {len(chunks)} chunks, todo {len(todo)}, workers {workers}, \"\n                f\"N_NULL {n_null}, btw cutoff {btw_cutoff}, nb_min_w {nb_min_w}\")\n    t0 = time.time()\n    per = []\n    with ProcessPoolExecutor(workers, mp_context=mp.get_context(\"spawn\"), initializer=_init_ego) as ex:\n        futs = [ex.submit(ego_chunk, k, chunks[k], n_null, btw_cutoff, nb_min_w) for k in todo]\n        for i, fu in enumerate(as_completed(futs)):\n            k, out, dt = fu.result()\n            pd.DataFrame(out).to_parquet(outdir / f\"chunk_{k:05d}.parquet\", index=False)\n            per.append(dt / max(len(out), 1))\n            if i % 10 == 0 or i == len(futs) - 1:\n                el = time.time() - t0\n                logger.info(f\"ego chunk {i+1}/{len(futs)} {el/60:.1f} min; {np.mean(per):.2f} s/concept/worker; \"\n                            f\"eta {el / (i+1) * (len(futs) - i - 1) / 60:.1f} min\")\n    return {\"n\": len(jobs), \"wall_s\": time.time() - t0, \"s_per_concept_worker\": float(np.mean(per)) if per else None}\n\n\ndef stage_assemble(logger) -> None:", "numLines": 75, "startLine": 200, "totalLines": 313}}
```

### [38] TOOL CALL — ToolSearch · 2026-09-29 02:08:45 UTC

```
{'query': 'select:WebSearch', 'max_results': 1}
```

### [39] TOOL RESULT — ToolSearch · 2026-09-29 02:08:45 UTC

```
{"matches": ["WebSearch"], "query": "select:WebSearch", "total_deferred_tools": 27}
```

### [40] TOOL CALL — WebSearch · 2026-09-29 02:08:47 UTC

```
Hennig clusterwise stability bootstrap Jaccard 0.75 stable 0.6 cluster validation fpc clusterboot
```

### [41] TOOL CALL — WebSearch · 2026-09-29 02:08:47 UTC

```
Seawright Gerring 2008 case selection techniques extreme diverse most similar cases
```

### [42] TOOL RESULT — WebSearch · 2026-09-29 02:08:53 UTC

```
{"query": "Seawright Gerring 2008 case selection techniques extreme diverse most similar cases", "results": [{"tool_use_id": "srvtoolu_01Esijg9jn5seWJ9KAdF8Azi", "content": [{"title": "Seawright Gerring - Case Selection Techniques in Case Study Research ...", "url": "https://www.scribd.com/document/258843536/Seawright-Gerring-Case-Selection-Techniques-in-Case-Study-Research-a-Menu-of-Qualitative-and-Quantitative-Options-2008"}, {"title": "The Case for Selecting Cases That Are Deviant or Extreme on the ...", "url": "https://www.researchgate.net/publication/301580844_The_Case_for_Selecting_Cases_That_Are_Deviant_or_Extreme_on_the_Independent_Variable"}, {"title": "Case Selection Techniques in Case Study Research", "url": "https://www.researchgate.net/publication/224952181_Case_Selection_Techniques_in_Case_Study_Research"}, {"title": "http://prq.sagepub.com Political Research Quarterly", "url": "https://aceproject.org/electoral-advice/archive/questions/replies/614466876/555642411/Gerring-Case-selection-Techniques-in-Case-Study.pdf"}, {"title": "University of North Dakota University of North Dakota UND Scholarly ...", "url": "https://commons.und.edu/cgi/viewcontent.cgi?article=1005&context=pssa-fac"}, {"title": "The Case for Selecting Cases That Are Deviant or Extreme on the ...", "url": "https://journals.sagepub.com/doi/abs/10.1177/0049124116643556"}, {"title": "Case Selection for Case-Study Analysis: Qualitative and Quantitative ...", "url": "https://www.researchgate.net/publication/284222605_Case_Selection_for_Case-Study_Analysis_Qualitative_and_Quantitative_Techniques"}, {"title": "Case Selection Techniques in Case Study Research: Abstract, Citation ...", "url": "https://www.bohrium.com/en/paper-details/case-selection-techniques-in-case-study-research/811921289076801536-6470"}, {"title": "9 Small N", "url": "https://nulib-oer.github.io/empirical-methods-polisci/small-n.html"}, {"title": "Case selection techniques in case study research (PDF)", "url": "https://www.academia.edu/2753939/Case_selection_techniques_in_case_study_research"}]}, "Based on the search results, here's what the Seawright and Gerring 2008 paper covers:\n\nThe paper presents seven case selection procedures, each of which facilitates a different strategy for within-case analysis. The case selection procedures considered focus on typical, diverse, extreme, deviant, influential, most similar, and most different cases.\n\nThe article was published in Political Research Quarterly in 2008, titled \"Case Selection Techniques in Case Study Research: A Menu of Qualitative and Quantitative Options.\"\n\nThe paper addresses case selection methodology by providing a systematic framework for researchers to choose cases based on different strategic objectives. Case selection in case study research has the twin objectives of obtaining a representative sample and useful variation on dimensions of theoretical interest.\n\nSeveral of the specific techniques mentioned in your query:\n- The extreme case is characterized by cases that are very high or very low on a researcher's key independent or dependent variables and can provide the means to better understand and explore phenomena through maximizing variation on the dimensions of interest.\n- Diverse case selection is particularly suitable for research aiming at exploring correlations when cases are characterized by distinct characteristics.\n- The most similar cases method facilitates the identification of the causes of contrasting outcomes while simultaneously making it possible to eliminate other potential explanatory variables."], "durationSeconds": 6.396520743000001, "searchCount": 1}
```

### [43] TOOL RESULT — WebSearch · 2026-09-29 02:08:53 UTC

```
{"query": "Hennig clusterwise stability bootstrap Jaccard 0.75 stable 0.6 cluster validation fpc clusterboot", "results": [{"tool_use_id": "srvtoolu_01TmTwZrLMaTZM8ue45CZUNj", "content": [{"title": "Cluster-wise assessment of cluster stability", "url": "https://www.researchgate.net/publication/222432274_Cluster-wise_assessment_of_cluster_stability"}, {"title": "Cluster-wise assessment of cluster stability Christian Hennig", "url": "https://www.homepages.ucl.ac.uk/~ucakche/papers/clusta.pdf"}, {"title": "clusterboot: Clusterwise cluster stability assessment by resampling ...", "url": "https://rdrr.io/cran/fpc/man/clusterboot.html"}, {"title": "Package ‘fpc’ May 8, 2026 Title Flexible Procedures for Clustering", "url": "https://cran.r-project.org/web/packages/fpc/fpc.pdf"}, {"title": "Bootstrapping estimates of stability for clusters, ...", "url": "https://vaclab.unc.edu/publication/compstats_2019_yu/compstats_2019_yu.pdf"}, {"title": "R: Clusterwise cluster stability assessment by resampling", "url": "https://search.r-project.org/CRAN/refmans/fpc/html/clusterboot.html"}, {"title": "R: Cluster-wise stability assessment of Joint Dimension...", "url": "https://search.r-project.org/CRAN/refmans/clustrd/html/local_bootclus.html"}, {"title": "Cities cluster into growth regimes that propagate shocks", "url": "https://arxiv.org/pdf/2603.16007"}, {"title": "Bootstrap Evaluation of Clusters", "url": "https://www.r-bloggers.com/2015/09/bootstrap-evaluation-of-clusters/"}, {"title": "Computational linguistic analysis of learners' discourse in computer-mediated group learning environments", "url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11170177"}]}, "Based on the search results, I found comprehensive information about the topics in your query. Here are the key findings:\n\n## Hennig's Cluster-wise Stability Assessment\n\nThe Jaccard coefficient, a similarity measure between sets, is used as a cluster-wise measure of cluster stability, which is assessed by the bootstrap distribution of the Jaccard coefficient for every single cluster of a clustering. Hennig (2007) proposed a method to estimate cluster-wise stability through bootstrapping and other re-sampling approaches.\n\n## Interpretation of Stability Values\n\nThe specific numerical thresholds you mentioned are well-established:\n\n- Generally, a valid, stable cluster should yield a mean Jaccard similarity value of 0.75 or more.\n- Below average Jaccard values of 0.6, clusters should not be trusted.\n- \"Highly stable\" clusters should yield average Jaccard similarities of 0.85 and above.\n\n## Implementation in R\n\nThe clusterboot function in the fpc package in R is used to perform bootstrap validation for cluster stability assessment. The data is resampled using several schemes (bootstrap, subsetting, jittering, replacement of points by noise) and the Jaccard similarities of the original clusters to the most similar clusters in the resampled data are computed.\n\nThe mean over these similarities is used as an index of the stability of a cluster (other statistics can be computed as well)."], "durationSeconds": 7.078235885000002, "searchCount": 1}
```

### [44] THINKING · 2026-09-29 02:12:13 UTC

```
The home-only ego network can be rebuilt directly from EXP8's cached data, but EXP7's state panel only covers 11,841 of 12,499 concepts, so the remainder will need rebuilding. I'm now writing the plan JSON.
```

### [45] TOOL CALL — Write · 2026-09-29 02:12:13 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_3/.terminal_claude_agent_struct_out.json

{
  "title": "How concepts spread: contact versus keeping",
  "summary": "Re-run of the failed iteration-3 RQ2 artifact (gen_art_experiment_9, never executed), cache only: 0 OpenAlex credits, no snapshot pass, $0 LLM. It uses the EXP5/EXP7/EXP8 arrays for all 12,499 frame concepts. The pre-registration is inverted to the openness account and hash-sealed before any held-out or cohort result is computed. Seven parts. (0) The method_out.json skeleton is written and validated against exp_gen_sol_out FIRST, and re-validated after every stage; Exp9 died on output format. (1) OPEN covariates in three builds. ALL-PAPERS comes from EXP8 ego_features. HOME-ONLY is recomputed from EXP8 frame_matches_early restricted to home-venue papers. SIZE-MATCHED ALL-PAPERS averages 20 random subsamples down to the home-only paper count. z constants are frozen on all 12,499 concepts. (2) D3 state sequences, t0..t0+10: EXP7 state_panel where it exists (11,841 concepts), and a verified rebuild with EXP7 lib/d3.py for the 658 EXP6-overlap concepts. From these come yearly contact, retention, frontier, entropy, within-home share and backbone-community span. (3) An exact log-additive decomposition, log B = log E2 (early contact) + log M (frontier advance) + log rho (retention), with Shapley shares of the top-vs-bottom O2r_resid tercile gap. It is volume-stratified, Medicine-adjusted and also run without Medicine. Pre-registered prediction: exploration (E2, M) carries more of the gap than retention, and localised concepts have HIGHER early retention ratios. (4) A typology by DTW k-medoids plus a Gaussian HMM. A class is named only if DTW-HMM ARI >= 0.5, Hennig bootstrap Jaccard >= 0.75, it replicates on held-out re-clustering, and it survives excluding Medicine homes. Otherwise a PCA continuum is reported, with Spearman and partial Spearman of OPEN against axis 1. (5) A light sequence test: home prominence half-peak against off-home take-off, and intersection-born against single-home concepts, with a mechanical-lag null. (6) Six to eight B5-matched case pairs with opposite OPEN, each with an alluvial D3 flow, W1..W3 ego snapshots, O2r and recognition dates. (7) A retrospective AI/CS atlas of 40 concepts. Also produced: pipeline_counts.json for the methodology figure.",
  "runpod_compute_profile": "cpu_plus",
  "domain_practice": "WHAT I READ. No domain handbook fits: the four offered are computational linguistics, mech-interp, multi-agent LLMs and neuro-symbolic AI. So I took the strategist's field reasoning as the base and checked it against sources I opened:\n- this run's iteration-3 RQ2 plan (3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3), which read Sun & Abraham 2021, Roth 2022 and sequence-analysis practice;\n- the code of the artifacts reused here: EXP8 lib/ego.py and build_features.py, EXP7 lib/d3.py, and the EXP8 README;\n- two targeted lookups. Hennig 2007, 'Cluster-wise assessment of cluster stability' (CSDA; fpc::clusterboot): mean bootstrap Jaccard >= 0.75 means a valid, stable cluster, < 0.6 means not to be trusted, >= 0.85 means highly stable. Seawright & Gerring 2008, 'Case selection techniques in case study research' (Political Research Quarterly 61(2)): typical, diverse, extreme, deviant, influential, most-similar and most-different designs, where most-similar pairs are matched on controls and differ on the variable of interest.\n\n(1) BASELINES AND COMPARISONS.\n- Breadth is always compared with volume. Breadth counts rise with paper counts, so rarefied richness (O2r_m50), residualised breadth (O2r_resid) and volume strata are standard. The first question a reviewer asks is whether 'integrating' just means 'big'.\n- Home-field composition. Medicine and CS homes behave differently; in this run Medicine dominated EXP6's localised class, 55 Med of 62. The standard fix is stratification plus exclusion.\n- Relatedness is the default model of diversification (Hidalgo 2007; Neffke 2011). It is a context variable, not a contribution.\n- A trajectory typology is compared with a continuum or single-factor account (volume, age, field), and with a second clustering method.\n- Ordering claims are compared with the reverse path, placebo timing and the mechanical lag built into state definitions.\n\n(2) CASES AND DATA.\n- The field works on whole-corpus OpenAlex, WoS or Scopus panels with concept or keyword vocabularies, venue or journal discipline labels (Rinia 2002; Yan 2013; Leydesdorff & Rafols) and a co-classification relatedness backbone.\n- Known weak spots: paper-level topic classifiers used as discipline labels; conference-heavy CS under-covered by venue labels; survivorship of named vocabularies (legacy concepts seeded from Wikipedia); generic pre-existing terms that look 'new' ('Coefficient of variation').\n- Case studies are credible only when chosen by a stated quantitative rule (Seawright & Gerring). Here that means most-similar pairs: matched on B5 volume and growth, opposite on OPEN, outcome shown afterwards.\n\n(3) CONTROLS AND WHAT IS HELD CONSTANT.\n- Align on concept age, not calendar year.\n- Onset-year cohort, volume stratum, home group and identical state definitions across splits.\n- The confounds most likely to catch this design:\n  (a) Retention (>= 2 papers in 3 years) rises mechanically with volume.\n  (b) The all-papers ego network gains off-home topics exactly when the concept spreads (mechanical coupling). The home-only build answers this.\n  (c) Generic, re-emerging terms.\n  (d) Medicine homes.\n  (e) The mechanical lag: RETAINED needs entry at least 2 years earlier.\n\n(4) HOW MUCH IS ENOUGH.\n- Typologies need hundreds to thousands of units. Cross-method ARI >= 0.5 means moderate agreement. Cluster-wise bootstrap Jaccard should be >= 0.75.\n- HMM state number is chosen by BIC with several EM restarts.\n- Decomposition shares need bootstrap CIs, with resampling by concept (>= 1,000; the direction asks for 2,000).\n- Heterogeneity across domains is reported per group with I2 (DL pooling), not averaged.\n- Case studies: 6-8 pairs are illustration, never inference. This is stated.\n\n(5) MEASURES AND REPORTING.\n- Diversity: rarefied richness and Shannon entropy.\n- Participation coefficient over backbone communities (Guimera-Amaral).\n- State-transition matrices.\n- Kitagawa, Das Gupta and Shapley decompositions. Shares sum to the total gap; for a log-additive identity the Shapley value is unique.\n- Alluvial diagrams of state flows (Rosvall & Bergstrom 2010; Holmgren 2023 in ANS).\n- Kaplan-Meier / cumulative incidence for time-to-event.\n- Forest plots per held-out group with DL pooling.\n- Every table names its resampling unit and carries a Source line.",
  "practice_alignment": "MEETS.\n(1) Volume. The decomposition runs within early-volume quintiles and on O2r_resid terciles. Every class or axis is checked against volume terciles (ARI; a 'volume class' flag at >= 0.5), and retention is recomputed at min_n = 3 and 5.\n(2) Medicine. The decomposition, class naming and continuum Spearman are all run with Medicine adjusted AND excluded, with per-group results and I2.\n(3) Cluster validity. k is chosen by silhouette and gap. Hennig cluster-wise bootstrap Jaccard is required to be >= 0.75 (added after the lookup; the old plan had only a global ARI >= 0.6). Classes must agree across methods (DTW vs HMM ARI >= 0.5), replicate under independent held-out re-clustering, and be compared with EXP6's failed k = 2 typology on the overlap.\n(4) Mechanical coupling. OPEN is used in three builds (ALL-PAPERS, HOME-ONLY, SIZE-MATCHED), and every OPEN statement is reported for all three.\n(5) Case selection follows a written most-similar-pair rule (B5-matched, opposite OPEN), fixed before any outcome is looked at, with a generic-term filter. O2r is displayed after selection and never used to choose.\n(6) Resampling is by concept with 2,000 refit bootstraps; DL pooling; Holm within each pre-declared family; a hash seal before evaluation.\n\nDEPARTS.\n(a) The 'held-out' groups are not fresh. EXP5, EXP7 and EXP8 already unsealed their outcomes, and the hypothesis now treats the whole EXP5 frame as SELECTION data. Here the seal guarantees only that this artifact's analysis choices were fixed on DEV before it read held-out states and outcomes. Cost: the held-out replication is a within-frame robustness check, not a confirmation. The paper must say so; the fresh confirmation is the 2015-16 cohort, which belongs to another artifact.\n(b) Discipline resolution is 26 venue fields, not 252 subfields. This keeps comparability with EXP5-EXP8, whose D3 states, backbone and outcomes are all at this level. Cost: within-field migration is invisible, so 'retention' is coarse.\n(c) The topic-level ego network exists only for t0-3..t0+2. EXP8 Pass A kept only those hits, and this artifact is forbidden a snapshot pass. The atlas and case studies therefore show topic-level structure for W1..W3 and field-level D3 structure for t0..t0+10. Cost: the atlas cannot show topic-neighbour change after t0+2, which the request asks for. This is stated as a data limit.\n(d) The decomposition is an accounting identity for the breadth outcome, not a predictor. B at t0+8 is built from the same t0+6..t0+8 papers as O2r. Only the E2 factor is early. The shares are descriptive, and the paper must not read them as causal.\n(e) Case pairs (6-8) and the 40-concept atlas are illustrative and retrospective. The atlas is selected on outcomes by design (it is the request's stage-1 inspection) and is labelled so.\n(f) The sequence test is light. Proper within-concept closure-to-entry hazards with event studies belong to the RQ2-timing direction. Here only home-prominence half-peak vs off-home take-off, a mechanical-lag null and the intersection-born contrast are run. Cost: no Sun-Abraham event study in this artifact.\n(g) Venue-label coverage (26-80%) is inherited. Label coverage is reported per class/axis tercile and entered as a covariate in the continuum partial correlation.",
  "builds_on": "DEEPEN: no new line. Every input is an existing cached artifact. RUN = /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M; all paths below are read-only. COPY code into the workspace lib/ and record sha256 values; never import across trees.\n\n(1) EXP8 art_dFQ6jbgNsR6Q = RUN/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/ (the main source).\n- data/analysis_table.parquet: authoritative per-concept B5 (logvol, growth, off-home share, entropy, reach), O2r_m50, O2r_resid (DEV fit a = 2.741, b = 0.397 on early logvol), O1c, O1b, O3, O4 and split/group. Check the columns; if something is absent, join data/outcomes.parquet and data/features_basic.parquet.\n- data/features_basic.parquet: RETENTION_RATIO_early, CONTACT_REACH, n_authors_early.\n- data/ego_features.parquet: new_edge_rate, n_comm_W3, participation, NOV_res, ego_density_W3, edge_persistence and _top_nb_W3, i.e. the ALL-PAPERS OPEN components.\n- data/frame_matches_early/part_001.parquet: grounded hits for t0-3..t0+2 with ci, year, work_id, vfield, topics (EXP3 topic index list) and authors. This is the input for the HOME-ONLY and SIZE-MATCHED builds and the ego snapshots.\n- data/bg_topics.npz (BG[year, topic], GT); inputs/backbone/slice0-2.npz (topic PMI slices, Leiden communities); inputs/topic_meta.csv (topic -> subfield/field names, used for the AI filter); inputs/topic_ids.json; inputs/field_backbone.json; inputs/source_field.parquet.\n- lib/ego.py and lib/ego_ctx.py (rq1_context() builds the context), build_features.py (ego_jobs/ego_chunk pattern, SEED, N_NULL, BTW_CUTOFF), lib/common.py, lib/rq1stats.py, lib/seal.py.\n- data/frame_arrays.npz: check its keys. It is expected to hold the per-frame grounded [C, NY, 27] counts used to rebuild D3 states; if not, rebuild from EXP5 agg_counts.\n- data/o5_events.parquet: recognition events already joined to the frame.\n- results/case_exemplars.json (the seeds for case pairs); results/frozen_spec.json and indicator_dictionary.csv (definitions quoted verbatim); data/passA_info.json and passB_info.json (pipeline counts).\n\n(2) EXP7 art_22ppE1snfHKj = RUN/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/.\n- results/state_panel_dev.parquet and state_panel_heldout.parquet: the authoritative D3 concept x field x year states for the 11,841 concepts in EXP5 minus EXP6.\n- lib/d3.py: panel_states(G, home_mask, min_n) is the vectorised EXP6 h2 semantics (entered = cum >= min_n; retaining = entered(t-2) & w3 >= min_n & off-home; lost = entered & w3 == 0), used to rebuild the 658 missing concepts and to verify the panel.\n- lib/h2_exp6.py, lib/exp5.py (frame loaders), results/overlap_report.json.\n- Risk-set parquet row counts, used for pipeline_counts.\n\n(3) EXP5 art_wxWssKSUR45f = RUN/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/.\n- frame_concepts.csv (12,499; ci, concept_id, name, t0, home ('|'-separated OpenAlex field ids 11..36), intersect40, group, split, label_coverage_early, early_volume).\n- concept_outcomes.csv (a cross-check of O2r_m50); scan/agg_counts.parquet (fallback count source; TAG = tagstate == 1; vfield = field id - 10, code 0 = unlabelled); scan/year_field_totals.npz (home prominence denominators); scan/scan_info.json (pipeline counts); episodes.csv.\n\n(4) EXP6 art_N-mpomDZZ1ln = RUN/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/.\n- lib/traj.py (dtw_matrix with tslearn Sakoe-Chiba, kmed with kmedoids.fasterpam, choose_k, hmm_fit), lib/lib_outcomes.py (rarefied_richness, shannon), inputs/field_backbone.json (26-field PMI phi, 1998-2002).\n- results/cluster_assign_*.csv (the old k = 2 typology, re-compared here).\n- results/frame_concepts.csv (overlap flag).\n\n(5) EXP3 art_yrradSC27HtQ backbone slices (already copied into EXP8 inputs/backbone).\n\n(6) Declared dependency art_O7Dq4L02QnDN = RUN/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/full_data_out/full_data_out_{1,2,3}.json (dataset 'concept_recognition'; join metadata_openalex_id == 'C' + concept_id; output JSON has events with source, year, year_usable, relation, match_confidence). EXP8 data/o5_events.parquet is used first, and the dependency cross-checks it.\n\nNEGATIVE FINDINGS BUILT PAST.\n- EXP6's k = 2 typology (HMM-vs-DTW ARI 0.094; localised class 55 Med + 7 Eng) is NOT ESTABLISHED. Hence the stricter naming rule and the Medicine exclusion.\n- The iteration-3 prediction that retention carries the largest share is replaced by its inverse. Grounds: EXP8 RETENTION_RATIO_early -0.120 held-out and the volume-matched R-vs-N contrast null in EXP7.\n- Gateway, rescue and relay are closed, so no gateway variable enters.\n- The ordering result is MIXED (evaluation_2), so no strong ordering claim is pre-registered, only a light test with a mechanical-lag null.\n- O5 is unrelated to O2r and is used descriptively only.\n\nIf the run volume is not mounted, rebuild from the public S3 snapshot is NOT allowed here (cache-only direction). Stop, write a partial method_out.json with status 'inputs_missing', and log it in deviations.json.",
  "implementation_pseudocode": "CWD = this artifact's gen_art workspace. First read the skills aii-python, aii-json, aii-parallel-computing, aii-long-running-tasks, aii-use-hardware, aii-file-size-limit and aii-data-fig-gen.\nSetup: uv venv, Python 3.12. Packages: numpy pandas pyarrow polars scipy scikit-learn statsmodels igraph networkx tslearn kmedoids hmmlearn matplotlib loguru wordfreq joblib.\nCONSTANTS: RUN, E5, E6, E7, E8 paths as in builds_on; SEED = 20260929; B = 2000 bootstraps; min_n = 2 (primary), with 3 and 5 as sensitivities.\nNo OpenAlex calls, no S3 reads, no OpenRouter calls. Assert this in code: a network guard raises if requests or boto is imported.\n\nTIMEBOX, 6 h:\n- S0: 0.25 h\n- S1-S2: 1.25 h\n- S3: 0.5 h\n- S4: 0.5 h\n- S5: 1.0 h\n- S6: 0.25 h\n- S7 (seal + held-out): 0.5 h\n- S8: 0.5 h\n- S9: 0.5 h\n- S10 and write-up: 0.75 h\nDROP ORDER if behind: SIZE-MATCHED build -> S6 sequence test -> HMM restarts 10 -> 4 -> atlas figure reduced to 20 panels -> case pairs 8 -> 6. Never drop S0, S3, S4, S5 or the seal.\n\nS0 FORMAT FIRST (Exp9 died here)\n  write method_out.json skeleton = {'metadata': {'artifact': 'rq2_trajectories_rerun', 'status': 'skeleton', 'stages_done': []}, 'datasets': [{'dataset': 'rq2_concepts', 'examples': [{'input': '{json concept summary}', 'output': '{json observed trajectory summary}', 'predict_open_axis': '...', 'predict_decomposition': '...', 'metadata_ci': 0, 'metadata_split': 'DEV', 'metadata_group': 'CS+Eng'}]}]}\n  validate with the aii-json skill against exp_gen_sol_out. Fix it until it passes, then make the mini and preview variants.\n  write a helper validate_out(stage) that re-validates after EVERY stage; the pipeline aborts the stage write if validation fails.\n  copy code: E8/lib/{ego.py, ego_ctx.py, common.py, rq1stats.py, seal.py}, E8/build_features.py (for ego_jobs), E7/lib/d3.py, E6/lib/{traj.py, lib_outcomes.py}\n    -> lib/, with sha256 values written to logs/provenance.json\n\nS1 LOAD AND JOIN (no held-out outcome is READ yet: open analysis_table with a column filter; outcome columns of non-DEV rows are masked by a SealedFrame wrapper that raises on access until the unseal)\n  frame = E5/frame_concepts.csv\n  home_list = [int(x) for x in home.split('|')]\n  home group map:\n    CS + Eng = {17, 22}\n    BGM + Med = {13, 27}\n    PHYS, LIFEENV, SOC, MATHDEC per EXP5 'group' (use the frame's group column directly and a coarse map to the 5 reporting groups)\n  flags:\n    med_home = 27 in home_list\n    intersection_born = intersect40 == 1\n    in_exp6 = concept_id in E6/results/frame_concepts.csv\n  A = E8 analysis_table.parquet (B5, outcomes); F = features_basic; EGO = ego_features (6 OPEN components + _top_nb_W3)\n  log the counts per split and group -> logs/join.json\n\nS2 OPEN COVARIATES, 3 builds (outcome-free, so all 12,499 concepts are computed before the seal)\n  (a) ALL-PAPERS: components from EGO (NaN kept).\n  (b) HOME-ONLY:\n      em = read frame_matches_early (ci, year, vfield, topics)\n      works_home[ci] = [(year, topics) for rows with vfield in {h - 10 for h in home_list}]  (vfield 0 = unlabelled -> excluded)\n      log home_cov = n_home_rows / n_rows in t0..t0+2, and n_home per concept\n      lib/ego_open.py = a trimmed copy of ego.concept_core that computes ONLY M, first_year, new_edge_rate, NOV/NOV_res, participation, n_comm_W3, edge_persistence and ego_density_W3 (drop the D_z / F nulls and betweenness; they dominate the runtime and are not OPEN components)\n        TEST: on the ALL-PAPERS input for 300 random concepts, ego_open must reproduce E8 ego_features for all 6 components to <= 1e-12 (NaN pattern identical). It must pass before use.\n      run with a ProcessPoolExecutor (spawn, initializer = ego.set_context(ego_ctx.rq1_context()); check that rq1_context resolves its paths against E8 and patch the paths to E8 inputs, logging the patch), in chunks of 40 concepts\n      TIME 200 concepts first -> extrapolate to 12,499 (aii-long-running-tasks). The trimmed code should run at about 0.1-0.3 s per concept per worker.\n  (c) SIZE-MATCHED ALL-PAPERS:\n      for each concept with n_home >= 5: 20 draws, each subsampling (without replacement, seed = SEED + ci*100 + r) the concept's t0..t0+2 works down to n_home (stratified by year so the W1/W2/W3 proportions are kept)\n      run ego_open on each draw and average each component over the draws\n      if the projection is > 45 min, run only on the DEV + held-out 5,000-concept stratified subsample and on all case/atlas concepts (logged deviation)\n  OPEN = mean over the available of [z(new_edge_rate), z(n_comm_W3), z(participation), z(NOV_res), -z(ego_density_W3), -z(edge_persistence)], computed only when >= 4 of 6 are present\n  z constants = mean and population SD (ddof = 0) over ALL 12,499 frame concepts, separately per build, frozen in frozen_spec.json\n  also carried, NOT in OPEN: RETENTION_RATIO_early, CONTACT_REACH\n  write open_features.parquet (ci, 6 x 3 components, OPEN_all, OPEN_home, OPEN_size, n_components, home_cov, n_home)\n  diagnostics: Spearman between the builds; the share of concepts with OPEN_home defined, by group\n\nS3 STATE SEQUENCES, ages 0..10 (a <= 2022 - t0; ages 9-10 flagged 'extended'; the analysis uses ages 0..8, which every concept has because t0 <= 2014)\n  SP = concat(E7 state_panel_dev, state_panel_heldout); inspect the schema (expected columns include ci/cidx, year, field and the state flags or code)\n  missing = the frame ci not in SP (expected 658 = EXP6 overlap)\n  G = E8 frame_arrays.npz, or else build [C, NY, 27] from E5 agg_counts (TAG only)\n  S = d3.panel_states(G, home_mask, min_n) for ALL concepts\n  VERIFY: on the 11,841 concepts in SP, the rebuilt entered/retaining/lost flags equal SP exactly (report the mismatch count; it must be 0, or explain it by a documented difference such as Y0 indexing)\n  per (ci, age, field): state in {HOME, UNTOUCHED, ENTERED, RETAINED, LOST}, with precedence LOST > RETAINED > ENTERED for off-home fields  -> state_sequences.parquet (int8; about 12,499 x 11 x 26 = 3.6M rows)\n  per (ci, age) summaries -> panel.parquet:\n    n_c\n    n_off (off-home papers in the year)\n    n_ent_off = number of off-home fields entered (cumulative)\n    new_entries = the diff of n_ent_off  [CONTACT RATE]\n    n_ret = retaining fields; n_lost\n    ret_share = n_ret / max(1, n_ent_off at age - 2)  [RETENTION PROBABILITY]\n    frontier = new_entries / max(1, n_ret at age - 1)  [FRONTIER ADVANCE]\n    R20 = rarefied richness m = 20 over the 3-yr window (lib_outcomes; NaN if < 20 papers)\n    H = Shannon of the 3-yr field distribution\n    home_share = home papers / labelled papers\n    HP = home prominence = sum over home fields of n_c,home / N_home(t) from year_field_totals\n    comm_span = number of field-backbone communities touched by RETAINED plus home\n      communities: Louvain on E6 phi (positive part), seed 0, resolution chosen from {0.5, 0.75, 1, 1.25, 1.5} as the first giving 4-8 communities (outcome-free); frozen\n    part_ret = participation over those communities of the concept's 3-yr off-home papers\n    label_cov = 1 - unlabelled / n_c\n  transitions.json: year-to-year field-state transition counts and rates per group and split (the DEV table first; held-out rows are written only after S7)\n\nS4 DECOMPOSITION (DEV first; held-out/cohort after S7)\n  per concept (H = 8):\n    E2 = off-home fields entered by age 2\n    EH = entered by age 8\n    Bn = |RETAINED at age 8|\n    M = EH / E2\n    rho = Bn / EH\n    identity: log Bn = log E2 + log M + log rho when E2, Bn >= 1\n  GROUP-LEVEL (exact with zeros): for g in {top, bottom} tercile of O2r_resid (terciles computed within split):\n    Ebar = mean E2\n    Mg = sum EH / sum E2\n    rhog = sum Bn / sum EH\n    Bbar = Ebar * Mg * rhog\n    D_k = log factor_k(top) - log factor_k(bottom)\n    share_k = D_k / sum D\n    s_explore = s_E2 + s_M; s_contact = s_E2; s_ret = s_rho\n  ADDITIVE Das Gupta 3-factor decomposition of Bbar(top) - Bbar(bottom) as a check\n  VARIANTS:\n    (i) pooled\n    (ii) within early-volume quintiles (log early_volume), with shares = the n-weighted mean of stratum D_k over the n-weighted total  [PRIMARY]\n    (iii) primary + Medicine-adjusted (within {med, non-med} strata)\n    (iv) primary with med_home excluded\n    (v) min_n 3 / 5\n    (vi) outcome terciles of O2r_m50 and of O1c = 1 only\n    (vii) EARLY-RATIO: RETENTION_RATIO_early (t0..t0+2) by tercile\n  CONCEPT-LEVEL complement among Bn >= 1: the exact covariance decomposition var(log Bn) = sum_k cov(log Bn, log f_k); report shares\n  CIs: 2,000 concept bootstrap resamples within split, recomputing terciles and strata in each\n  PRE-REGISTERED (text copied verbatim into frozen_spec before any computation; verdicts are evaluated separately on DEV and on held-out):\n    PR1 EXPLORATION > RETENTION: in variant (iv) [volume-stratified, Medicine excluded], s_explore - s_ret > 0 with the 95% concept-bootstrap CI > 0. Equivalently s_ret < 0.5; both are printed, noting that shares sum to 1.\n    PR1b (secondary, Holm family R2-A with PR1 and PR2): s_contact - s_ret > 0 with CI > 0.\n    PR2 LOCALISED KEEP MORE EARLY: mean RETENTION_RATIO_early(bottom O2r_resid tercile) - mean(top tercile) > 0 with CI > 0, AND the partial Spearman of RETENTION_RATIO_early with O2r_resid given B5 < 0. The latter is flagged 'replication on the same frame as EXP8, not new evidence'.\n    PR3 (descriptive, not tested): the sign of D_rho, i.e. whether late retention probability is lower for integrating concepts.\n  verdict per clause: SUPPORTED / NOT SUPPORTED / REVERSED (CI on the opposite side)\n  per-group shares with DL pooling and I2 over the held-out groups; cohort 2010-14 split into DEV-home and other-home parts\n  -> decomposition.json (every number, the CI, n per tercile, the resampling unit 'concept', Source lines)\n\nS5 TYPOLOGY (DEV fit; frozen; held-out after S7)\n  VARS = [new_entries, n_ent_off, n_ret, n_lost, ret_share, frontier, H, home_share, comm_span] at ages 0..8 -> X[n, 9, 9]\n    asinh on the count VARS; then z per VAR with DEV means and SDs (frozen)\n    volume is NOT a VAR; it is checked afterwards\n  DTW:\n    E6 traj.dtw_matrix (Sakoe-Chiba radius 2, n_jobs = 4)\n    TIME 500 DEV concepts, then extrapolate to 4,771 (about 11.4M pairs). If > 25 min, select k on a random 3,000 DEV subsample and assign the rest to the nearest medoid.\n    k-medoids (fasterpam) for k = 2..8\n    k chosen as the max silhouette among the k whose median bootstrap ARI (100 x 80% subsamples) is >= 0.6; the gap statistic is reported\n  HMM:\n    hmmlearn GaussianHMM(diag) on the stacked sequences with lengths; 3, 4 and 5 states; 10 restarts each; BIC picks S\n    concept partition = k-medoids (the same k as DTW) on the Euclidean distance of [posterior state occupancy per age (9 x S) + final-state one-hot]\n  CLUSTER-WISE STABILITY: Hennig Jaccard; for 100 bootstrap resamples, the Jaccard of each original cluster with its best-matching resampled cluster (mean per cluster)\n  NAMING RULE (frozen): a class is NAMED only if ALL of:\n    (1) ARI(DTW, HMM) >= 0.5\n    (2) the class's mean bootstrap Jaccard >= 0.75\n    (3) re-clustering with med_home excluded gives ARI >= 0.5 against the original labels restricted to non-Med, and the class keeps >= 5% of non-Med concepts\n    (4) after S7: an independent held-out re-cluster (frozen VARS, z and k) vs held-out nearest-DEV-medoid assignment gives ARI >= 0.5\n    (5) ARI(class, early-volume tercile) < 0.5; otherwise the class is flagged 'volume class' and is not named\n  Otherwise CONTINUUM:\n    PCA on the flattened DEV X (81 dims); keep the PCs with >= 10% variance (max 3)\n    loadings heat map (VAR x age)\n    project held-out with the frozen loadings\n  OPEN ON THE AXIS (always reported, for classes as well):\n    Spearman(OPEN_b, PC1) for b in {all, home, size}\n    partial Spearman given B5 + label_cov\n    per group, with DL and I2\n    concept bootstrap CIs\n    class means of OPEN_b if classes are named\n  PROFILES: medoid series with concept names; class/PC-tercile x group table; Med share; O1c, O2r_resid, O3 and O4 per class/tercile; label coverage\n  OLD TYPOLOGY: ARI of our labels (or the PC1 median split) vs E6 cluster_assign on the overlapping concepts; recorded as 'Exp6 two-class typology: NOT ESTABLISHED (HMM-DTW ARI 0.094)'\n  -> trajectories.json\n\nS6 SEQUENCE TEST, LIGHT (secondary; DEV then held-out)\n  A = the first age with HP >= 0.5 * max_{0..8} HP (home prominence half-peak)\n  T = off-home take-off = the first age with new_entries >= 2 or n_ret >= 1 (frozen)\n  order shares among concepts with both: A < T, tie, A > T\n  MECHANICAL-LAG NULL: 1,000 within-concept permutations of the HP series -> the null share; report observed minus null with a concept-bootstrap CI\n  intersection-born vs single-home:\n    Kaplan-Meier of T\n    discrete-time cloglog hazard of T on the intersection flag + early log-volume + group FE (concept-clustered SE)\n    share with T <= 2\n    OPEN_home by flag\n  -> sequence_light.json (verdict words: HOME-FIRST / INTERSECTION-ROUTE / MIXED; no stronger claim)\n\nS7 SEAL -> UNSEAL ONCE\n  frozen_spec.json holds:\n    OPEN formula and z constants per build; VARS; z spec; k and S; Louvain resolution; decomposition definitions\n    PR1/PR1b/PR2 text; naming thresholds; case-pair rule; generic rule; seeds\n    the sha256 of every file in lib/ and every script; the list of held-out ci\n  seal.py freeze -> logs/seal.log (sha256 of frozen_spec) -> git commit -> unseal (refuses a second time)\n  run S4, S5 (projection, re-cluster, rule (4)) and S6 on PHYS / LIFEENV / SOC / MATHDEC (MATHDEC reported, excluded from DL if n < 150 with an outcome)\n  also: pooled; DL pooling; cohort (DEV-home, other-home); Medicine excluded; in_exp6 excluded\n  disclose in every JSON: 'held-out outcomes were previously unsealed by EXP5/EXP7/EXP8; this seal fixes only this artifact's choices'\n\nS8 MATCHED CASE PAIRS (rule frozen in S7; figures made after)\n  GENERIC filter (logged in deviations.json with the list of hits). A concept is excluded if any of:\n    (a) pre-onset footprint: grounded papers in 1995..t0-1 >= 0.5 x early volume\n    (b) single-token name with wordfreq zipf_frequency(name, 'en') >= 4.0\n    (c) the name matches the regex (?i)^(coefficient|exponential|linear|rate|ratio|index|analysis|method|model|approach|system|process|cross[- ]?disciplinary|interdisciplinary)\\b\n  pools per reporting group (5 groups; at most 2 pairs from CS+Eng, at least 4 groups covered): top-quintile OPEN_all vs bottom-quintile OPEN_all among non-generic concepts with OPEN_home defined\n  MATCH: |z logvol diff| <= 0.25 and |z growth diff| <= 0.25 (B5 SDs over all 12,499), same reporting group, onset year within 2\n    SEEDING: first try the concepts named in E8 case_exemplars.json (high and low lists of every indicator) as the anchor; then, among the remaining matches, take the pair with the largest OPEN_all gap; ties broken by the smallest Mahalanobis distance on (logvol, growth, off-home share)\n    O2r is NOT used in selection\n  6-8 pairs; each pair reports OPEN_home for both members (flag the pair if the OPEN_home order disagrees with OPEN_all)\n  per pair -> case_studies/<pairid>/:\n    (a) alluvial plot of off-home field counts flowing UNTOUCHED -> ENTERED -> RETAINED -> LOST over ages 0..10 (matplotlib fill_between ribbons), side by side\n    (b) a field x year state raster ordered by backbone community\n    (c) ego snapshots W1, W2, W3 from frame_matches_early:\n        neighbours = the ego.neighbours rule (PMI > 0, count >= 2, SELF excluded); edges between neighbours from the slice's full_edges\n        networkx spring layout (seed 0); nodes coloured by EXP3 Leiden community and sized by count; the top-10 neighbour labels\n        both builds (all and home-only) for W3\n    (d) pair.json: names, group, t0, B5, the 6 OPEN components in each build, O2r_m50, O2r_resid, O1c, O3\n        recognition events (year_usable, relation 'same') from E8 o5_events / the dependency, with the lag to t0, marked pre-t0 where applicable; descriptive only\n        the decomposition factors E2, M, rho; class/axis score\n  a descriptive summary: in how many pairs the high-OPEN member has the higher O2r_resid (no p-value, n <= 8)\n\nS9 AI/CS ATLAS (RETROSPECTIVE, DESCRIPTIVE; outcome-selected by design)\n  eligible = home contains 17 (CS) AND AI share >= 0.3, where AI share = the share of the concept's t0..t0+2 topic assignments whose topic_meta subfield is in {1702 Artificial Intelligence, 1707 Computer Vision and Pattern Recognition} or whose topic name matches (?i)neural|learning|language processing|reinforcement|recommender|speech recognition; generic filter applied\n  5 types x 8 concepts (the largest early volume first within a type, one concept per type at most once; ties broken by seed):\n    RAPID = top-decile early growth\n    GRADUAL = bottom-half early growth & O1c = 1\n    LOCAL = O1c = 1 & bottom O2r_resid tercile\n    DIFFUSING = top O2r_resid tercile\n    TRANSIENT = O3 = 1\n    if a type has < 8 eligible concepts, relax AI share to 0.2 and log it\n  per concept, yearly panels:\n    topic level for ages -3..2: nc per year; degree; new neighbours (not in PRE); n communities; ego density; OPEN components\n    field level for ages 0..10: n_c, H, n_ent_off, n_ret, n_lost, home_share, comm_span, and the state raster\n  figures:\n    ai_atlas/small_multiples.png (5 rows = types x 8; lines for n_ent_off, n_ret, H on twin axes)\n    ai_atlas/ego_W3_grid.png\n  ai_atlas/table.csv + atlas.json: per type, the medians of each yearly measure at ages 2, 5 and 8; which measures separate the types (Kruskal-Wallis H with n = 40, labelled descriptive); and a 'looked meaningful' column filled by a written rule: the measure separates DIFFUSING from LOCAL by >= 0.5 pooled SD at age 2 AND has the same sign as the frame-wide DEV Spearman with O2r_resid\n\nS10 PIPELINE COUNTS AND OUTPUTS\n  pipeline_counts.json holds EVERY number read from files, never typed:\n    E5 scan_info (works, base works, verified matches, agg rows); lexicon size; frame by split and group\n    E8 passA_info early_rows and passB_info\n    E7 risk-set row counts (via pyarrow metadata); E5 episodes rows\n    this artifact: state rows, concept-ages, DTW n, OPEN coverage per build, pairs, atlas n\n  method_out.json (exp_gen_sol_out):\n    dataset 'rq2_concepts', one example per concept (12,499):\n      input = a JSON string {name, group, split, t0, B5, OPEN_all, OPEN_home, OPEN_size, RETENTION_RATIO_early}\n      output = a JSON string {O2r_resid tercile, E2, EH, Bn, class or PC scores}\n      predict_open_axis = the PC1 score, or the class label\n      predict_decomposition = a JSON string {log E2, log M, log rho}\n      metadata_* fields\n    dataset 'case_pairs' (one example per pair)\n    metadata = the headline results (the PR verdicts, shares with CIs, naming outcome, OPEN-axis Spearman)\n    validate; if > the size limit, split with aii-file-size-limit; mini/preview via aii-json\n  figures (PNG + PDF, aii-data-fig-gen style):\n    decomposition waterfall per split\n    a forest plot of s_explore - s_ret by group\n    PCA loadings heat map or class medoids\n    the DTW-HMM agreement matrix\n    OPEN vs PC1 hexbin\n    KM of take-off by intersection flag\n    the case pairs\n    the atlas\n  README.md (layout, how to run, results with Source lines, 'held-out previously unsealed' disclosure)\n  .aii/manifest.yaml:\n    keep: results/, figures/, case_studies/, ai_atlas/, open_features.parquet, panel.parquet, state_sequences.parquet if < 100 MB\n    delete, regenerable: .venv/ (source 'uv sync'), dtw_cache/ (source 'uv run method.py --stage S5')",
  "fallback_plan": "Every fallback is logged in deviations.json with its reason and its effect on the claims.\n(1) Output format. If the aii-json validation of the skeleton fails, fix the structure before ANY computation. This is a hard gate. If the full file exceeds the limit, split it (aii-file-size-limit); never drop the validation.\n(2) EXP7 state_panel schema is unclear or incomplete. Rebuild ALL states with d3.panel_states from E8 frame_arrays.npz, or from E5 agg_counts (TAG rows, pyarrow filter on the frame ci). Keep the SP cross-check on whatever overlap parses. If the rebuild mismatches SP beyond 0.1% of cells, trust the rebuild (it follows the documented h2 semantics) and report the mismatch.\n(3) ego_open fails the 1e-12 reproduction test. Fall back to the untrimmed ego.concept_core with n_null = 20 and btw_cutoff = 2 for HOME-ONLY. The OPEN components do not depend on the nulls or betweenness; verify this on 100 concepts. If it is too slow (> 60 min projected), compute HOME-ONLY on a stratified 5,000-concept subsample (all case/atlas concepts included); the z constants then come from that subsample (a deviation).\n(4) The rq1_context paths break outside E8. Patch the path constants to the E8 inputs (backbone slices, bg_topics.npz, topic_ids.json); record the diff.\n(5) Few concepts have HOME-ONLY OPEN (< 50% have >= 4 components, likely in CS with low label coverage). Report coverage by group. Run the OPEN-on-axis analysis on the defined subset, with a selection check comparing B5 of the covered and uncovered concepts, and add a relaxed variant with nb_min_w = 1 as a sensitivity.\n(6) DTW is too slow. Use Sakoe-Chiba radius 1, or Euclidean distance on the age-aligned vectors (the series are already aligned at t0), with k selected on a 3,000-concept subsample and nearest-medoid assignment.\n(7) The HMM does not converge or collapses states. Use a CategoricalHMM on a 5-symbol stage sequence (HOME_ONLY, CONTACT, RETAIN_1, RETAIN_MANY, CONTRACTING). If no two methods reach ARI 0.5, report the CONTINUUM; that is a pre-registered, publishable outcome.\n(8) Decomposition degeneracy: a factor mean of 0 in a stratum, e.g. no retained fields in the bottom tercile of a small group. Merge adjacent volume quintiles (logged). If a group still has < 30 concepts per tercile, report it without a CI and exclude it from DL.\n(9) No valid match for a group within 0.25 SD. Widen to 0.35 SD for that group (logged). If there is still none, skip the group; at least 6 pairs must remain, otherwise report fewer and say why.\n(10) The atlas finds < 30 eligible AI concepts. Include CS-home concepts with AI share >= 0.1, and mark the tier.\n(11) Recognition join coverage is low. Use the Wikipedia/Wikidata-only variant, and report coverage per group.\n(12) Time overrun. The priority order is S0 > S3 > S4 > S5 > S7 > S8 > S2(b) > S9 > S10 figures > S6 > S2(c). Always write partial JSONs with status fields, and never leave method_out.json invalid.",
  "testing_plan": "T0 UNIT TESTS (tests/test_units.py; no network):\n(a) d3.panel_states on a hand-built 12-year x 27 array reproduces the expected ENTERED/RETAINED/LOST masks, including the home exclusion and the 2-year lag.\n(b) Decomposition identity: for 1,000 random concepts, |log Bn - (log E2 + log M + log rho)| < 1e-9 where defined; group-level Bbar equals the factor product; the shares sum to 1; the additive Das Gupta terms sum to the gap.\n(c) Planted decomposition: a synthetic panel where top and bottom terciles differ only in contact gives s_contact of about 1 and s_ret of about 0; one differing only in retention gives the reverse.\n(d) Planted typology: 600 synthetic concepts from 3 regimes (fast contact / low retention; slow contact / high retention; spike then loss). DTW-kmedoids and the HMM partition each recover them with ARI >= 0.8, and choose_k gives 3. A pure-noise panel must FAIL the naming rule.\n(e) OPEN formula: the hand-computed z-mean on 5 rows; the >= 4-of-6 rule; the signs.\n(f) The seal refuses a second unseal and a changed spec hash; SealedFrame raises on held-out outcome access before the unseal.\n(g) The generic regex and the wordfreq rule on a fixed list: 'Coefficient of variation' and 'Exponential growth' are excluded, 'Optogenetics' is kept.\nT1 FORMAT: the method_out.json skeleton validates against exp_gen_sol_out BEFORE S1, and again after every stage (the log shows 'validate OK' per stage).\nT2 REPRODUCTION:\n- ego_open reproduces E8 ego_features for the 6 components on 300 concepts to <= 1e-12.\n- The rebuilt D3 states equal EXP7 state_panel on its 11,841 concepts (0 mismatches expected).\n- RETENTION_RATIO_early recomputed from the states at age 2 matches E8 features_basic (Spearman >= 0.99; exact where the definitions coincide).\n- O2r_m50 from E8 vs E5 concept_outcomes: rho >= 0.99.\nT3 SMOKE: 200 random DEV concepts run end to end (S2-S6, one case pair, 5 atlas concepts) in < 10 min. Eye-check 5 state rasters against their yearly field counts.\nT4 SCALE: aii-long-running-tasks staging for the HOME-ONLY ego (200 -> 2,000 -> all) and DTW (500 -> 2,000 -> all DEV), timing each and extrapolating before committing.\nT5 ROBUSTNESS: a second bootstrap seed moves the CI ends by < 0.01. A second k-medoids seed and HMM restart set give the same k and an ARI within 0.05.\nT6 PRE-UNSEAL CHECKLIST: an assert log shows that no held-out ci entered any fitted object used for choices; frozen_spec hash logged; git commit made; the PR text is in frozen_spec verbatim.\nT7 INDEPENDENT RE-DERIVATION after the unseal: separate minimal pandas code recomputes the held-out group-level shares (to 1e-9) and the OPEN-PC1 Spearman (to 1e-6).\nT8 SANITY printed BEFORE any class is named: class x volume-tercile ARI, the class x Medicine table, and the class x group table.\nT9 PLACEBO: shuffle O2r_resid within group, rerun the decomposition 200 times; the share difference s_explore - s_ret must centre on its null (report the null distribution). Also shuffle OPEN within group and recompute Spearman with PC1 200 times (the null band must cover 0)."
}
```

### [46] TOOL RESULT — Write · 2026-09-29 02:12:13 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_3/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"How concepts spread: contact versus keeping\",\n  \"summary\": \"Re-run of the failed iteration-3 RQ2 artifact (gen_art_experiment_9, never executed), cache only: 0 OpenAlex credits, no snapshot pass, $0 LLM. It uses the EXP5/EXP7/EXP8 arrays for all 12,499 frame concepts. The pre-registration is inverted to the openness account and hash-sealed before any held-out or cohort result is computed. Seven parts. (0) The method_out.json skeleton is written and validated against exp_gen_sol_out FIRST, and re-validated after every stage; Exp9 died on output format. (1) OPEN covariates in three builds. ALL-PAPERS comes from EXP8 ego_features. HOME-ONLY is recomputed from EXP8 frame_matches_early restricted to home-venue papers. SIZE-MATCHED ALL-PAPERS averages 20 random subsamples down to the home-only paper count. z constants are frozen on all 12,499 concepts. (2) D3 state sequences, t0..t0+10: EXP7 state_panel where it exists (11,841 concepts), and a verified rebuild with EXP7 lib/d3.py for the 658 EXP6-overlap concepts. From these come yearly contact, retention, frontier, entropy, within-home share and backbone-community span. (3) An exact log-additive decomposition, log B = log E2 (early contact) + log M (frontier advance) + log rho (retention), with Shapley shares of the top-vs-bottom O2r_resid tercile gap. It is volume-stratified, Medicine-adjusted and also run without Medicine. Pre-registered prediction: exploration (E2, M) carries more of the gap than retention, and localised concepts have HIGHER early retention ratios. (4) A typology by DTW k-medoids plus a Gaussian HMM. A class is named only if DTW-HMM ARI >= 0.5, Hennig bootstrap Jaccard >= 0.75, it replicates on held-out re-clustering, and it survives excluding Medicine homes. Otherwise a PCA continuum is reported, with Spearman and partial Spearman of OPEN against axis 1. (5) A light sequence test: home prominence half-peak against off-home take-off, and intersection-born against single-home concepts, with a mechanical-lag null. (6) Six to eight B5-matched case pairs with opposite OPEN, each with an alluvial D3 flow, W1..W3 ego snapshots, O2r and recognition dates. (7) A retrospective AI/CS atlas of 40 concepts. Also produced: pipeline_counts.json for the methodology figure.\",\n  \"runpod_compute_profile\": \"cpu_plus\",\n  \"domain_practice\": \"WHAT I READ. No domain handbook fits: the four offered are computational linguistics, mech-interp, multi-agent LLMs and neuro-symbolic AI. So I took the strategist's field reasoning as the base and checked it against sources I opened:\\n- this run's iteration-3 RQ2 plan (3_invention_loop/iter_3/gen_plan/gen_plan_experiment_3), which read Sun & Abraham 2021, Roth 2022 and sequence-analysis practice;\\n- the code of the artifacts reused here: EXP8 lib/ego.py and build_features.py, EXP7 lib/d3.py, and the EXP8 README;\\n- two targeted lookups. Hennig 2007, 'Cluster-wise assessment of cluster stability' (CSDA; fpc::clusterboot): mean bootstrap Jaccard >= 0.75 means a valid, stable cluster, < 0.6 means not to be trusted, >= 0.85 means highly stable. Seawright & Gerring 2008, 'Case selection techniques in case study research' (Political Research Quarterly 61(2)): typical, diverse, extreme, deviant, influential, most-similar and most-different designs, where most-similar pairs are matched on controls and differ on the variable of interest.\\n\\n(1) BASELINES AND COMPARISONS.\\n- Breadth is always compared with volume. Breadth counts rise with paper counts, so rarefied richness (O2r_m50), residualised breadth (O2r_resid) and volume strata are standard. The first question a reviewer asks is whether 'integrating' just means 'big'.\\n- Home-field composition. Medicine and CS homes behave differently; in this run Medicine dominated EXP6's localised class, 55 Med of 62. The standard fix is stratification plus exclusion.\\n- Relatedness is the default model of diversification (Hidalgo 2007; Neffke 2011). It is a context variable, not a contribution.\\n- A trajectory typology is compared with a continuum or single-factor account (volume, age, field), and with a second clustering method.\\n- Ordering claims are compared with the reverse path, placebo timing and the mechanical lag built into state definitions.\\n\\n(2) CASES AND DATA.\\n- The field works on whole-corpus OpenAlex, WoS or Scopus panels with concept or keyword vocabularies, venue or journal discipline labels (Rinia 2002; Yan 2013; Leydesdorff & Rafols) and a co-classification relatedness backbone.\\n- Known weak spots: paper-level topic classifiers used as discipline labels; conference-heavy CS under-covered by venue labels; survivorship of named vocabularies (legacy concepts seeded from Wikipedia); generic pre-existing terms that look 'new' ('Coefficient of variation').\\n- Case studies are credible only when chosen by a stated quantitative rule (Seawright & Gerring). Here that means most-similar pairs: matched on B5 volume and growth, opposite on OPEN, outcome shown afterwards.\\n\\n(3) CONTROLS AND WHAT IS HELD CONSTANT.\\n- Align on concept age, not calendar year.\\n- Onset-year cohort, volume stratum, home group and identical state definitions across splits.\\n- The confounds most likely to catch this design:\\n  (a) Retention (>= 2 papers in 3 years) rises mechanically with volume.\\n  (b) The all-papers ego network gains off-home topics exactly when the concept spreads (mechanical coupling). The home-only build answers this.\\n  (c) Generic, re-emerging terms.\\n  (d) Medicine homes.\\n  (e) The mechanical lag: RETAINED needs entry at least 2 years earlier.\\n\\n(4) HOW MUCH IS ENOUGH.\\n- Typologies need hundreds to thousands of units. Cross-method ARI >= 0.5 means moderate agreement. Cluster-wise bootstrap Jaccard should be >= 0.75.\\n- HMM state number is chosen by BIC with several EM restarts.\\n- Decomposition shares need bootstrap CIs, with resampling by concept (>= 1,000; the direction asks for 2,000).\\n- Heterogeneity across domains is reported per group with I2 (DL pooling), not averaged.\\n- Case studies: 6-8 pairs are illustration, never inference. This is stated.\\n\\n(5) MEASURES AND REPORTING.\\n- Diversity: rarefied richness and Shannon entropy.\\n- Participation coefficient over backbone communities (Guimera-Amaral).\\n- State-transition matrices.\\n- Kitagawa, Das Gupta and Shapley decompositions. Shares sum to the total gap; for a log-additive identity the Shapley value is unique.\\n- Alluvial diagrams of state flows (Rosvall & Bergstrom 2010; Holmgren 2023 in ANS).\\n- Kaplan-Meier / cumulative incidence for time-to-event.\\n- Forest plots per held-out group with DL pooling.\\n- Every table names its resampling unit and carries a Source line.\",\n  \"practice_alignment\": \"MEETS.\\n(1) Volume. The decomposition runs within early-volume quintiles and on O2r_resid terciles. Every class or axis is checked against volume terciles (ARI; a 'volume class' flag at >= 0.5), and retention is recomputed at min_n = 3 and 5.\\n(2) Medicine. The decomposition, class naming and continuum Spearman are all run with Medicine adjusted AND excluded, with per-group results and I2.\\n(3) Cluster validity. k is chosen by silhouette and gap. Hennig cluster-wise bootstrap Jaccard is required to be >= 0.75 (added after the lookup; the old plan had only a global ARI >= 0.6). Classes must agree across methods (DTW vs HMM ARI >= 0.5), replicate under independent held-out re-clustering, and be compared with EXP6's failed k = 2 typology on the overlap.\\n(4) Mechanical coupling. OPEN is used in three builds (ALL-PAPERS, HOME-ONLY, SIZE-MATCHED), and every OPEN statement is reported for all three.\\n(5) Case selection follows a written most-similar-pair rule (B5-matched, opposite OPEN), fixed before any outcome is looked at, with a generic-term filter. O2r is displayed after selection and never used to choose.\\n(6) Resampling is by concept with 2,000 refit bootstraps; DL pooling; Holm within each pre-declared family; a hash seal before evaluation.\\n\\nDEPARTS.\\n(a) The 'held-out' groups are not fresh. EXP5, EXP7 and EXP8 already unsealed their outcomes, and the hypothesis now treats the whole EXP5 frame as SELECTION data. Here the seal guarantees only that this artifact's analysis choices were fixed on DEV before it read held-out states and outcomes. Cost: the held-out replication is a within-frame robustness check, not a confirmation. The paper must say so; the fresh confirmation is the 2015-16 cohort, which belongs to another artifact.\\n(b) Discipline resolution is 26 venue fields, not 252 subfields. This keeps comparability with EXP5-EXP8, whose D3 states, backbone and outcomes are all at this level. Cost: within-field migration is invisible, so 'retention' is coarse.\\n(c) The topic-level ego network exists only for t0-3..t0+2. EXP8 Pass A kept only those hits, and this artifact is forbidden a snapshot pass. The atlas and case studies therefore show topic-level structure for W1..W3 and field-level D3 structure for t0..t0+10. Cost: the atlas cannot show topic-neighbour change after t0+2, which the request asks for. This is stated as a data limit.\\n(d) The decomposition is an accounting identity for the breadth outcome, not a predictor. B at t0+8 is built from the same t0+6..t0+8 papers as O2r. Only the E2 factor is early. The shares are descriptive, and the paper must not read them as causal.\\n(e) Case pairs (6-8) and the 40-concept atlas are illustrative and retrospective. The atlas is selected on outcomes by design (it is the request's stage-1 inspection) and is labelled so.\\n(f) The sequence test is light. Proper within-concept closure-to-entry hazards with event studies belong to the RQ2-timing direction. Here only home-prominence half-peak vs off-home take-off, a mechanical-lag null and the intersection-born contrast are run. Cost: no Sun-Abraham event study in this artifact.\\n(g) Venue-label coverage (26-80%) is inherited. Label coverage is reported per class/axis tercile and entered as a covariate in the continuum partial correlation.\",\n  \"builds_on\": \"DEEPEN: no new line. Every input is an existing cached artifact. RUN = /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M; all paths below are read-only. COPY code into the workspace lib/ and record sha256 values; never import across trees.\\n\\n(1) EXP8 art_dFQ6jbgNsR6Q = RUN/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/ (the main source).\\n- data/analysis_table.parquet: authoritative per-concept B5 (logvol, growth, off-home share, entropy, reach), O2r_m50, O2r_resid (DEV fit a = 2.741, b = 0.397 on early logvol), O1c, O1b, O3, O4 and split/group. Check the columns; if something is absent, join data/outcomes.parquet and data/features_basic.parquet.\\n- data/features_basic.parquet: RETENTION_RATIO_early, CONTACT_REACH, n_authors_early.\\n- data/ego_features.parquet: new_edge_rate, n_comm_W3, participation, NOV_res, ego_density_W3, edge_persistence and _top_nb_W3, i.e. the ALL-PAPERS OPEN components.\\n- data/frame_matches_early/part_001.parquet: grounded hits for t0-3..t0+2 with ci, year, work_id, vfield, topics (EXP3 topic index list) and authors. This is the input for the HOME-ONLY and SIZE-MATCHED builds and the ego snapshots.\\n- data/bg_topics.npz (BG[year, topic], GT); inputs/backbone/slice0-2.npz (topic PMI slices, Leiden communities); inputs/topic_meta.csv (topic -> subfield/field names, used for the AI filter); inputs/topic_ids.json; inputs/field_backbone.json; inputs/source_field.parquet.\\n- lib/ego.py and lib/ego_ctx.py (rq1_context() builds the context), build_features.py (ego_jobs/ego_chunk pattern, SEED, N_NULL, BTW_CUTOFF), lib/common.py, lib/rq1stats.py, lib/seal.py.\\n- data/frame_arrays.npz: check its keys. It is expected to hold the per-frame grounded [C, NY, 27] counts used to rebuild D3 states; if not, rebuild from EXP5 agg_counts.\\n- data/o5_events.parquet: recognition events already joined to the frame.\\n- results/case_exemplars.json (the seeds for case pairs); results/frozen_spec.json and indicator_dictionary.csv (definitions quoted verbatim); data/passA_info.json and passB_info.json (pipeline counts).\\n\\n(2) EXP7 art_22ppE1snfHKj = RUN/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/.\\n- results/state_panel_dev.parquet and state_panel_heldout.parquet: the authoritative D3 concept x field x year states for the 11,841 concepts in EXP5 minus EXP6.\\n- lib/d3.py: panel_states(G, home_mask, min_n) is the vectorised EXP6 h2 semantics (entered = cum >= min_n; retaining = entered(t-2) & w3 >= min_n & off-home; lost = entered & w3 == 0), used to rebuild the 658 missing concepts and to verify the panel.\\n- lib/h2_exp6.py, lib/exp5.py (frame loaders), results/overlap_report.json.\\n- Risk-set parquet row counts, used for pipeline_counts.\\n\\n(3) EXP5 art_wxWssKSUR45f = RUN/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/.\\n- frame_concepts.csv (12,499; ci, concept_id, name, t0, home ('|'-separated OpenAlex field ids 11..36), intersect40, group, split, label_coverage_early, early_volume).\\n- concept_outcomes.csv (a cross-check of O2r_m50); scan/agg_counts.parquet (fallback count source; TAG = tagstate == 1; vfield = field id - 10, code 0 = unlabelled); scan/year_field_totals.npz (home prominence denominators); scan/scan_info.json (pipeline counts); episodes.csv.\\n\\n(4) EXP6 art_N-mpomDZZ1ln = RUN/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/.\\n- lib/traj.py (dtw_matrix with tslearn Sakoe-Chiba, kmed with kmedoids.fasterpam, choose_k, hmm_fit), lib/lib_outcomes.py (rarefied_richness, shannon), inputs/field_backbone.json (26-field PMI phi, 1998-2002).\\n- results/cluster_assign_*.csv (the old k = 2 typology, re-compared here).\\n- results/frame_concepts.csv (overlap flag).\\n\\n(5) EXP3 art_yrradSC27HtQ backbone slices (already copied into EXP8 inputs/backbone).\\n\\n(6) Declared dependency art_O7Dq4L02QnDN = RUN/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/full_data_out/full_data_out_{1,2,3}.json (dataset 'concept_recognition'; join metadata_openalex_id == 'C' + concept_id; output JSON has events with source, year, year_usable, relation, match_confidence). EXP8 data/o5_events.parquet is used first, and the dependency cross-checks it.\\n\\nNEGATIVE FINDINGS BUILT PAST.\\n- EXP6's k = 2 typology (HMM-vs-DTW ARI 0.094; localised class 55 Med + 7 Eng) is NOT ESTABLISHED. Hence the stricter naming rule and the Medicine exclusion.\\n- The iteration-3 prediction that retention carries the largest share is replaced by its inverse. Grounds: EXP8 RETENTION_RATIO_early -0.120 held-out and the volume-matched R-vs-N contrast null in EXP7.\\n- Gateway, rescue and relay are closed, so no gateway variable enters.\\n- The ordering result is MIXED (evaluation_2), so no strong ordering claim is pre-registered, only a light test with a mechanical-lag null.\\n- O5 is unrelated to O2r and is used descriptively only.\\n\\nIf the run volume is not mounted, rebuild from the public S3 snapshot is NOT allowed here (cache-only direction). Stop, write a partial method_out.json with status 'inputs_missing', and log it in deviations.json.\",\n  \"implementation_pseudocode\": \"CWD = this artifact's gen_art workspace. First read the skills aii-python, aii-json, aii-parallel-computing, aii-long-running-tasks, aii-use-hardware, aii-file-size-limit and aii-data-fig-gen.\\nSetup: uv venv, Python 3.12. Packages: numpy pandas pyarrow polars scipy scikit-learn statsmodels igraph networkx tslearn kmedoids hmmlearn matplotlib loguru wordfreq joblib.\\nCONSTANTS: RUN, E5, E6, E7, E8 paths as in builds_on; SEED = 20260929; B = 2000 bootstraps; min_n = 2 (primary), with 3 and 5 as sensitivities.\\nNo OpenAlex calls, no S3 reads, no OpenRouter calls. Assert this in code: a network guard raises if requests or boto is imported.\\n\\nTIMEBOX, 6 h:\\n- S0: 0.25 h\\n- S1-S2: 1.25 h\\n- S3: 0.5 h\\n- S4: 0.5 h\\n- S5: 1.0 h\\n- S6: 0.25 h\\n- S7 (seal + held-out): 0.5 h\\n- S8: 0.5 h\\n- S9: 0.5 h\\n- S10 and write-up: 0.75 h\\nDROP ORDER if behind: SIZE-MATCHED build -> S6 sequence test -> HMM restarts 10 -> 4 -> atlas figure reduced to 20 panels -> case pairs 8 -> 6. Never drop S0, S3, S4, S5 or the seal.\\n\\nS0 FORMAT FIRST (Exp9 died here)\\n  write method_out.json skeleton = {'metadata': {'artifact': 'rq2_trajectories_rerun', 'status': 'skeleton', 'stages_done': []}, 'datasets': [{'dataset': 'rq2_concepts', 'examples': [{'input': '{json concept summary}', 'output': '{json observed trajectory summary}', 'predict_open_axis': '...', 'predict_decomposition': '...', 'metadata_ci': 0, 'metadata_split': 'DEV', 'metadata_group': 'CS+Eng'}]}]}\\n  validate with the aii-json skill against exp_gen_sol_out. Fix it until it passes, then make the mini and preview variants.\\n  write a helper validate_out(stage) that re-validates after EVERY stage; the pipeline aborts the stage write if validation fails.\\n  copy code: E8/lib/{ego.py, ego_ctx.py, common.py, rq1stats.py, seal.py}, E8/build_features.py (for ego_jobs), E7/lib/d3.py, E6/lib/{traj.py, lib_outcomes.py}\\n    -> lib/, with sha256 values written to logs/provenance.json\\n\\nS1 LOAD AND JOIN (no held-out outcome is READ yet: open analysis_table with a column filter; outcome columns of non-DEV rows are masked by a SealedFrame wrapper that raises on access until the unseal)\\n  frame = E5/frame_concepts.csv\\n  home_list = [int(x) for x in home.split('|')]\\n  home group map:\\n    CS + Eng = {17, 22}\\n    BGM + Med = {13, 27}\\n    PHYS, LIFEENV, SOC, MATHDEC per EXP5 'group' (use the frame's group column directly and a coarse map to the 5 reporting groups)\\n  flags:\\n    med_home = 27 in home_list\\n    intersection_born = intersect40 == 1\\n    in_exp6 = concept_id in E6/results/frame_concepts.csv\\n  A = E8 analysis_table.parquet (B5, outcomes); F = features_basic; EGO = ego_features (6 OPEN components + _top_nb_W3)\\n  log the counts per split and group -> logs/join.json\\n\\nS2 OPEN COVARIATES, 3 builds (outcome-free, so all 12,499 concepts are computed before the seal)\\n  (a) ALL-PAPERS: components from EGO (NaN kept).\\n  (b) HOME-ONLY:\\n      em = read frame_matches_early (ci, year, vfield, topics)\\n      works_home[ci] = [(year, topics) for rows with vfield in {h - 10 for h in home_list}]  (vfield 0 = unlabelled -> excluded)\\n      log home_cov = n_home_rows / n_rows in t0..t0+2, and n_home per concept\\n      lib/ego_open.py = a trimmed copy of ego.concept_core that computes ONLY M, first_year, new_edge_rate, NOV/NOV_res, participation, n_comm_W3, edge_persistence and ego_density_W3 (drop the D_z / F nulls and betweenness; they dominate the runtime and are not OPEN components)\\n        TEST: on the ALL-PAPERS input for 300 random concepts, ego_open must reproduce E8 ego_features for all 6 components to <= 1e-12 (NaN pattern identical). It must pass before use.\\n      run with a ProcessPoolExecutor (spawn, initializer = ego.set_context(ego_ctx.rq1_context()); check that rq1_context resolves its paths against E8 and patch the paths to E8 inputs, logging the patch), in chunks of 40 concepts\\n      TIME 200 concepts first -> extrapolate to 12,499 (aii-long-running-tasks). The trimmed code should run at about 0.1-0.3 s per concept per worker.\\n  (c) SIZE-MATCHED ALL-PAPERS:\\n      for each concept with n_home >= 5: 20 draws, each subsampling (without replacement, seed = SEED + ci*100 + r) the concept's t0..t0+2 works down to n_home (stratified by year so the W1/W2/W3 proportions are kept)\\n      run ego_open on each draw and average each component over the draws\\n      if the projection is > 45 min, run only on the DEV + held-out 5,000-concept stratified subsample and on all case/atlas concepts (logged deviation)\\n  OPEN = mean over the available of [z(new_edge_rate), z(n_comm_W3), z(participation), z(NOV_res), -z(ego_density_W3), -z(edge_persistence)], computed only when >= 4 of 6 are present\\n  z constants = mean and population SD (ddof = 0) over ALL 12,499 frame concepts, separately per build, frozen in frozen_spec.json\\n  also carried, NOT in OPEN: RETENTION_RATIO_early, CONTACT_REACH\\n  write open_features.parquet (ci, 6 x 3 components, OPEN_all, OPEN_home, OPEN_size, n_components, home_cov, n_home)\\n  diagnostics: Spearman between the builds; the share of concepts with OPEN_home defined, by group\\n\\nS3 STATE SEQUENCES, ages 0..10 (a <= 2022 - t0; ages 9-10 flagged 'extended'; the analysis uses ages 0..8, which every concept has because t0 <= 2014)\\n  SP = concat(E7 state_panel_dev, state_panel_heldout); inspect the schema (expected columns include ci/cidx, year, field and the state flags or code)\\n  missing = the frame ci not in SP (expected 658 = EXP6 overlap)\\n  G = E8 frame_arrays.npz, or else build [C, NY, 27] from E5 agg_counts (TAG only)\\n  S = d3.panel_states(G, home_mask, min_n) for ALL concepts\\n  VERIFY: on the 11,841 concepts in SP, the rebuilt entered/retaining/lost flags equal SP exactly (report the mismatch count; it must be 0, or explain it by a documented difference such as Y0 indexing)\\n  per (ci, age, field): state in {HOME, UNTOUCHED, ENTERED, RETAINED, LOST}, with precedence LOST > RETAINED > ENTERED for off-home fields  -> state_sequences.parquet (int8; about 12,499 x 11 x 26 = 3.6M rows)\\n  per (ci, age) summaries -> panel.parquet:\\n    n_c\\n    n_off (off-home papers in the year)\\n    n_ent_off = number of off-home fields entered (cumulative)\\n    new_entries = the diff of n_ent_off  [CONTACT RATE]\\n    n_ret = retaining fields; n_lost\\n    ret_share = n_ret / max(1, n_ent_off at age - 2)  [RETENTION PROBABILITY]\\n    frontier = new_entries / max(1, n_ret at age - 1)  [FRONTIER ADVANCE]\\n    R20 = rarefied richness m = 20 over the 3-yr window (lib_outcomes; NaN if < 20 papers)\\n    H = Shannon of the 3-yr field distribution\\n    home_share = home papers / labelled papers\\n    HP = home prominence = sum over home fields of n_c,home / N_home(t) from year_field_totals\\n    comm_span = number of field-backbone communities touched by RETAINED plus home\\n      communities: Louvain on E6 phi (positive part), seed 0, resolution chosen from {0.5, 0.75, 1, 1.25, 1.5} as the first giving 4-8 communities (outcome-free); frozen\\n    part_ret = participation over those communities of the concept's 3-yr off-home papers\\n    label_cov = 1 - unlabelled / n_c\\n  transitions.json: year-to-year field-state transition counts and rates per group and split (the DEV table first; held-out rows are written only after S7)\\n\\nS4 DECOMPOSITION (DEV first; held-out/cohort after S7)\\n  per concept (H = 8):\\n    E2 = off-home fields entered by age 2\\n    EH = entered by age 8\\n    Bn = |RETAINED at age 8|\\n    M = EH / E2\\n    rho = Bn / EH\\n    identity: log Bn = log E2 + log M + log rho when E2, Bn >= 1\\n  GROUP-LEVEL (exact with zeros): for g in {top, bottom} tercile of O2r_resid (terciles computed within split):\\n    Ebar = mean E2\\n    Mg = sum EH / sum E2\\n    rhog = sum Bn / sum EH\\n    Bbar = Ebar * Mg * rhog\\n    D_k = log factor_k(top) - log factor_k(bottom)\\n    share_k = D_k / sum D\\n    s_explore = s_E2 + s_M; s_contact = s_E2; s_ret = s_rho\\n  ADDITIVE Das Gupta 3-factor decomposition of Bbar(top) - Bbar(bottom) as a check\\n  VARIANTS:\\n    (i) pooled\\n    (ii) within early-volume quintiles (log early_volume), with shares = the n-weighted mean of stratum D_k over the n-weighted total  [PRIMARY]\\n    (iii) primary + Medicine-adjusted (within {med, non-med} strata)\\n    (iv) primary with med_home excluded\\n    (v) min_n 3 / 5\\n    (vi) outcome terciles of O2r_m50 and of O1c = 1 only\\n    (vii) EARLY-RATIO: RETENTION_RATIO_early (t0..t0+2) by tercile\\n  CONCEPT-LEVEL complement among Bn >= 1: the exact covariance decomposition var(log Bn) = sum_k cov(log Bn, log f_k); report shares\\n  CIs: 2,000 concept bootstrap resamples within split, recomputing terciles and strata in each\\n  PRE-REGISTERED (text copied verbatim into frozen_spec before any computation; verdicts are evaluated separately on DEV and on held-out):\\n    PR1 EXPLORATION > RETENTION: in variant (iv) [volume-stratified, Medicine excluded], s_explore - s_ret > 0 with the 95% concept-bootstrap CI > 0. Equivalently s_ret < 0.5; both are printed, noting that shares sum to 1.\\n    PR1b (secondary, Holm family R2-A with PR1 and PR2): s_contact - s_ret > 0 with CI > 0.\\n    PR2 LOCALISED KEEP MORE EARLY: mean RETENTION_RATIO_early(bottom O2r_resid tercile) - mean(top tercile) > 0 with CI > 0, AND the partial Spearman of RETENTION_RATIO_early with O2r_resid given B5 < 0. The latter is flagged 'replication on the same frame as EXP8, not new evidence'.\\n    PR3 (descriptive, not tested): the sign of D_rho, i.e. whether late retention probability is lower for integrating concepts.\\n  verdict per clause: SUPPORTED / NOT SUPPORTED / REVERSED (CI on the opposite side)\\n  per-group shares with DL pooling and I2 over the held-out groups; cohort 2010-14 split into DEV-home and other-home parts\\n  -> decomposition.json (every number, the CI, n per tercile, the resampling unit 'concept', Source lines)\\n\\nS5 TYPOLOGY (DEV fit; frozen; held-out after S7)\\n  VARS = [new_entries, n_ent_off, n_ret, n_lost, ret_share, frontier, H, home_share, comm_span] at ages 0..8 -> X[n, 9, 9]\\n    asinh on the count VARS; then z per VAR with DEV means and SDs (frozen)\\n    volume is NOT a VAR; it is checked afterwards\\n  DTW:\\n    E6 traj.dtw_matrix (Sakoe-Chiba radius 2, n_jobs = 4)\\n    TIME 500 DEV concepts, then extrapolate to 4,771 (about 11.4M pairs). If > 25 min, select k on a random 3,000 DEV subsample and assign the rest to the nearest medoid.\\n    k-medoids (fasterpam) for k = 2..8\\n    k chosen as the max silhouette among the k whose median bootstrap ARI (100 x 80% subsamples) is >= 0.6; the gap statistic is reported\\n  HMM:\\n    hmmlearn GaussianHMM(diag) on the stacked sequences with lengths; 3, 4 and 5 states; 10 restarts each; BIC picks S\\n    concept partition = k-medoids (the same k as DTW) on the Euclidean distance of [posterior state occupancy per age (9 x S) + final-state one-hot]\\n  CLUSTER-WISE STABILITY: Hennig Jaccard; for 100 bootstrap resamples, the Jaccard of each original cluster with its best-matching resampled cluster (mean per cluster)\\n  NAMING RULE (frozen): a class is NAMED only if ALL of:\\n    (1) ARI(DTW, HMM) >= 0.5\\n    (2) the class's mean bootstrap Jaccard >= 0.75\\n    (3) re-clustering with med_home excluded gives ARI >= 0.5 against the original labels restricted to non-Med, and the class keeps >= 5% of non-Med concepts\\n    (4) after S7: an independent held-out re-cluster (frozen VARS, z and k) vs held-out nearest-DEV-medoid assignment gives ARI >= 0.5\\n    (5) ARI(class, early-volume tercile) < 0.5; otherwise the class is flagged 'volume class' and is not named\\n  Otherwise CONTINUUM:\\n    PCA on the flattened DEV X (81 dims); keep the PCs with >= 10% variance (max 3)\\n    loadings heat map (VAR x age)\\n    project held-out with the frozen loadings\\n  OPEN ON THE AXIS (always reported, for classes as well):\\n    Spearman(OPEN_b, PC1) for b in {all, home, size}\\n    partial Spearman given B5 + label_cov\\n    per group, with DL and I2\\n    concept bootstrap CIs\\n    class means of OPEN_b if classes are named\\n  PROFILES: medoid series with concept names; class/PC-tercile x group table; Med share; O1c, O2r_resid, O3 and O4 per class/tercile; label coverage\\n  OLD TYPOLOGY: ARI of our labels (or the PC1 median split) vs E6 cluster_assign on the overlapping concepts; recorded as 'Exp6 two-class typology: NOT ESTABLISHED (HMM-DTW ARI 0.094)'\\n  -> trajectories.json\\n\\nS6 SEQUENCE TEST, LIGHT (secondary; DEV then held-out)\\n  A = the first age with HP >= 0.5 * max_{0..8} HP (home prominence half-peak)\\n  T = off-home take-off = the first age with new_entries >= 2 or n_ret >= 1 (frozen)\\n  order shares among concepts with both: A < T, tie, A > T\\n  MECHANICAL-LAG NULL: 1,000 within-concept permutations of the HP series -> the null share; report observed minus null with a concept-bootstrap CI\\n  intersection-born vs single-home:\\n    Kaplan-Meier of T\\n    discrete-time cloglog hazard of T on the intersection flag + early log-volume + group FE (concept-clustered SE)\\n    share with T <= 2\\n    OPEN_home by flag\\n  -> sequence_light.json (verdict words: HOME-FIRST / INTERSECTION-ROUTE / MIXED; no stronger claim)\\n\\nS7 SEAL -> UNSEAL ONCE\\n  frozen_spec.json holds:\\n    OPEN formula and z constants per build; VARS; z spec; k and S; Louvain resolution; decomposition definitions\\n    PR1/PR1b/PR2 text; naming thresholds; case-pair rule; generic rule; seeds\\n    the sha256 of every file in lib/ and every script; the list of held-out ci\\n  seal.py freeze -> logs/seal.log (sha256 of frozen_spec) -> git commit -> unseal (refuses a second time)\\n  run S4, S5 (projection, re-cluster, rule (4)) and S6 on PHYS / LIFEENV / SOC / MATHDEC (MATHDEC reported, excluded from DL if n < 150 with an outcome)\\n  also: pooled; DL pooling; cohort (DEV-home, other-home); Medicine excluded; in_exp6 excluded\\n  disclose in every JSON: 'held-out outcomes were previously unsealed by EXP5/EXP7/EXP8; this seal fixes only this artifact's choices'\\n\\nS8 MATCHED CASE PAIRS (rule frozen in S7; figures made after)\\n  GENERIC filter (logged in deviations.json with the list of hits). A concept is excluded if any of:\\n    (a) pre-onset footprint: grounded papers in 1995..t0-1 >= 0.5 x early volume\\n    (b) single-token name with wordfreq zipf_frequency(name, 'en') >= 4.0\\n    (c) the name matches the regex (?i)^(coefficient|exponential|linear|rate|ratio|index|analysis|method|model|approach|system|process|cross[- ]?disciplinary|interdisciplinary)\\\\b\\n  pools per reporting group (5 groups; at most 2 pairs from CS+Eng, at least 4 groups covered): top-quintile OPEN_all vs bottom-quintile OPEN_all among non-generic concepts with OPEN_home defined\\n  MATCH: |z logvol diff| <= 0.25 and |z growth diff| <= 0.25 (B5 SDs over all 12,499), same reporting group, onset year within 2\\n    SEEDING: first try the concepts named in E8 case_exemplars.json (high and low lists of every indicator) as the anchor; then, among the remaining matches, take the pair with the largest OPEN_all gap; ties broken by the smallest Mahalanobis distance on (logvol, growth, off-home share)\\n    O2r is NOT used in selection\\n  6-8 pairs; each pair reports OPEN_home for both members (flag the pair if the OPEN_home order disagrees with OPEN_all)\\n  per pair -> case_studies/<pairid>/:\\n    (a) alluvial plot of off-home field counts flowing UNTOUCHED -> ENTERED -> RETAINED -> LOST over ages 0..10 (matplotlib fill_between ribbons), side by side\\n    (b) a field x year state raster ordered by backbone community\\n    (c) ego snapshots W1, W2, W3 from frame_matches_early:\\n        neighbours = the ego.neighbours rule (PMI > 0, count >= 2, SELF excluded); edges between neighbours from the slice's full_edges\\n        networkx spring layout (seed 0); nodes coloured by EXP3 Leiden community and sized by count; the top-10 neighbour labels\\n        both builds (all and home-only) for W3\\n    (d) pair.json: names, group, t0, B5, the 6 OPEN components in each build, O2r_m50, O2r_resid, O1c, O3\\n        recognition events (year_usable, relation 'same') from E8 o5_events / the dependency, with the lag to t0, marked pre-t0 where applicable; descriptive only\\n        the decomposition factors E2, M, rho; class/axis score\\n  a descriptive summary: in how many pairs the high-OPEN member has the higher O2r_resid (no p-value, n <= 8)\\n\\nS9 AI/CS ATLAS (RETROSPECTIVE, DESCRIPTIVE; outcome-selected by design)\\n  eligible = home contains 17 (CS) AND AI share >= 0.3, where AI share = the share of the concept's t0..t0+2 topic assignments whose topic_meta subfield is in {1702 Artificial Intelligence, 1707 Computer Vision and Pattern Recognition} or whose topic name matches (?i)neural|learning|language processing|reinforcement|recommender|speech recognition; generic filter applied\\n  5 types x 8 concepts (the largest early volume first within a type, one concept per type at most once; ties broken by seed):\\n    RAPID = top-decile early growth\\n    GRADUAL = bottom-half early growth & O1c = 1\\n    LOCAL = O1c = 1 & bottom O2r_resid tercile\\n    DIFFUSING = top O2r_resid tercile\\n    TRANSIENT = O3 = 1\\n    if a type has < 8 eligible concepts, relax AI share to 0.2 and log it\\n  per concept, yearly panels:\\n    topic level for ages -3..2: nc per year; degree; new neighbours (not in PRE); n communities; ego density; OPEN components\\n    field level for ages 0..10: n_c, H, n_ent_off, n_ret, n_lost, home_share, comm_span, and the state raster\\n  figures:\\n    ai_atlas/small_multiples.png (5 rows = types x 8; lines for n_ent_off, n_ret, H on twin axes)\\n    ai_atlas/ego_W3_grid.png\\n  ai_atlas/table.csv + atlas.json: per type, the medians of each yearly measure at ages 2, 5 and 8; which measures separate the types (Kruskal-Wallis H with n = 40, labelled descriptive); and a 'looked meaningful' column filled by a written rule: the measure separates DIFFUSING from LOCAL by >= 0.5 pooled SD at age 2 AND has the same sign as the frame-wide DEV Spearman with O2r_resid\\n\\nS10 PIPELINE COUNTS AND OUTPUTS\\n  pipeline_counts.json holds EVERY number read from files, never typed:\\n    E5 scan_info (works, base works, verified matches, agg rows); lexicon size; frame by split and group\\n    E8 passA_info early_rows and passB_info\\n    E7 risk-set row counts (via pyarrow metadata); E5 episodes rows\\n    this artifact: state rows, concept-ages, DTW n, OPEN coverage per build, pairs, atlas n\\n  method_out.json (exp_gen_sol_out):\\n    dataset 'rq2_concepts', one example per concept (12,499):\\n      input = a JSON string {name, group, split, t0, B5, OPEN_all, OPEN_home, OPEN_size, RETENTION_RATIO_early}\\n      output = a JSON string {O2r_resid tercile, E2, EH, Bn, class or PC scores}\\n      predict_open_axis = the PC1 score, or the class label\\n      predict_decomposition = a JSON string {log E2, log M, log rho}\\n      metadata_* fields\\n    dataset 'case_pairs' (one example per pair)\\n    metadata = the headline results (the PR verdicts, shares with CIs, naming outcome, OPEN-axis Spearman)\\n    validate; if > the size limit, split with aii-file-size-limit; mini/preview via aii-json\\n  figures (PNG + PDF, aii-data-fig-gen style):\\n    decomposition waterfall per split\\n    a forest plot of s_explore - s_ret by group\\n    PCA loadings heat map or class medoids\\n    the DTW-HMM agreement matrix\\n    OPEN vs PC1 hexbin\\n    KM of take-off by intersection flag\\n    the case pairs\\n    the atlas\\n  README.md (layout, how to run, results with Source lines, 'held-out previously unsealed' disclosure)\\n  .aii/manifest.yaml:\\n    keep: results/, figures/, case_studies/, ai_atlas/, open_features.parquet, panel.parquet, state_sequences.parquet if < 100 MB\\n    delete, regenerable: .venv/ (source 'uv sync'), dtw_cache/ (source 'uv run method.py --stage S5')\",\n  \"fallback_plan\": \"Every fallback is logged in deviations.json with its reason and its effect on the claims.\\n(1) Output format. If the aii-json validation of the skeleton fails, fix the structure before ANY computation. This is a hard gate. If the full file exceeds the limit, split it (aii-file-size-limit); never drop the validation.\\n(2) EXP7 state_panel schema is unclear or incomplete. Rebuild ALL states with d3.panel_states from E8 frame_arrays.npz, or from E5 agg_counts (TAG rows, pyarrow filter on the frame ci). Keep the SP cross-check on whatever overlap parses. If the rebuild mismatches SP beyond 0.1% of cells, trust the rebuild (it follows the documented h2 semantics) and report the mismatch.\\n(3) ego_open fails the 1e-12 reproduction test. Fall back to the untrimmed ego.concept_core with n_null = 20 and btw_cutoff = 2 for HOME-ONLY. The OPEN components do not depend on the nulls or betweenness; verify this on 100 concepts. If it is too slow (> 60 min projected), compute HOME-ONLY on a stratified 5,000-concept subsample (all case/atlas concepts included); the z constants then come from that subsample (a deviation).\\n(4) The rq1_context paths break outside E8. Patch the path constants to the E8 inputs (backbone slices, bg_topics.npz, topic_ids.json); record the diff.\\n(5) Few concepts have HOME-ONLY OPEN (< 50% have >= 4 components, likely in CS with low label coverage). Report coverage by group. Run the OPEN-on-axis analysis on the defined subset, with a selection check comparing B5 of the covered and uncovered concepts, and add a relaxed variant with nb_min_w = 1 as a sensitivity.\\n(6) DTW is too slow. Use Sakoe-Chiba radius 1, or Euclidean distance on the age-aligned vectors (the series are already aligned at t0), with k selected on a 3,000-concept subsample and nearest-medoid assignment.\\n(7) The HMM does not converge or collapses states. Use a CategoricalHMM on a 5-symbol stage sequence (HOME_ONLY, CONTACT, RETAIN_1, RETAIN_MANY, CONTRACTING). If no two methods reach ARI 0.5, report the CONTINUUM; that is a pre-registered, publishable outcome.\\n(8) Decomposition degeneracy: a factor mean of 0 in a stratum, e.g. no retained fields in the bottom tercile of a small group. Merge adjacent volume quintiles (logged). If a group still has < 30 concepts per tercile, report it without a CI and exclude it from DL.\\n(9) No valid match for a group within 0.25 SD. Widen to 0.35 SD for that group (logged). If there is still none, skip the group; at least 6 pairs must remain, otherwise report fewer and say why.\\n(10) The atlas finds < 30 eligible AI concepts. Include CS-home concepts with AI share >= 0.1, and mark the tier.\\n(11) Recognition join coverage is low. Use the Wikipedia/Wikidata-only variant, and report coverage per group.\\n(12) Time overrun. The priority order is S0 > S3 > S4 > S5 > S7 > S8 > S2(b) > S9 > S10 figures > S6 > S2(c). Always write partial JSONs with status fields, and never leave method_out.json invalid.\",\n  \"testing_plan\": \"T0 UNIT TESTS (tests/test_units.py; no network):\\n(a) d3.panel_states on a hand-built 12-year x 27 array reproduces the expected ENTERED/RETAINED/LOST masks, including the home exclusion and the 2-year lag.\\n(b) Decomposition identity: for 1,000 random concepts, |log Bn - (log E2 + log M + log rho)| < 1e-9 where defined; group-level Bbar equals the factor product; the shares sum to 1; the additive Das Gupta terms sum to the gap.\\n(c) Planted decomposition: a synthetic panel where top and bottom terciles differ only in contact gives s_contact of about 1 and s_ret of about 0; one differing only in retention gives the reverse.\\n(d) Planted typology: 600 synthetic concepts from 3 regimes (fast contact / low retention; slow contact / high retention; spike then loss). DTW-kmedoids and the HMM partition each recover them with ARI >= 0.8, and choose_k gives 3. A pure-noise panel must FAIL the naming rule.\\n(e) OPEN formula: the hand-computed z-mean on 5 rows; the >= 4-of-6 rule; the signs.\\n(f) The seal refuses a second unseal and a changed spec hash; SealedFrame raises on held-out outcome access before the unseal.\\n(g) The generic regex and the wordfreq rule on a fixed list: 'Coefficient of variation' and 'Exponential growth' are excluded, 'Optogenetics' is kept.\\nT1 FORMAT: the method_out.json skeleton validates against exp_gen_sol_out BEFORE S1, and again after every stage (the log shows 'validate OK' per stage).\\nT2 REPRODUCTION:\\n- ego_open reproduces E8 ego_features for the 6 components on 300 concepts to <= 1e-12.\\n- The rebuilt D3 states equal EXP7 state_panel on its 11,841 concepts (0 mismatches expected).\\n- RETENTION_RATIO_early recomputed from the states at age 2 matches E8 features_basic (Spearman >= 0.99; exact where the definitions coincide).\\n- O2r_m50 from E8 vs E5 concept_outcomes: rho >= 0.99.\\nT3 SMOKE: 200 random DEV concepts run end to end (S2-S6, one case pair, 5 atlas concepts) in < 10 min. Eye-check 5 state rasters against their yearly field counts.\\nT4 SCALE: aii-long-running-tasks staging for the HOME-ONLY ego (200 -> 2,000 -> all) and DTW (500 -> 2,000 -> all DEV), timing each and extrapolating before committing.\\nT5 ROBUSTNESS: a second bootstrap seed moves the CI ends by < 0.01. A second k-medoids seed and HMM restart set give the same k and an ARI within 0.05.\\nT6 PRE-UNSEAL CHECKLIST: an assert log shows that no held-out ci entered any fitted object used for choices; frozen_spec hash logged; git commit made; the PR text is in frozen_spec verbatim.\\nT7 INDEPENDENT RE-DERIVATION after the unseal: separate minimal pandas code recomputes the held-out group-level shares (to 1e-9) and the OPEN-PC1 Spearman (to 1e-6).\\nT8 SANITY printed BEFORE any class is named: class x volume-tercile ARI, the class x Medicine table, and the class x group table.\\nT9 PLACEBO: shuffle O2r_resid within group, rerun the decomposition 200 times; the share difference s_explore - s_ret must centre on its null (report the null distribution). Also shuffle OPEN within group and recompute Spearman with PC1 200 times (the null band must cover 0).\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [47] ASSISTANT · 2026-09-29 02:12:21 UTC

```
The plan JSON is written. Next come the workspace deliverables: the manifest and the README.
```

### [48] TOOL CALL — Write · 2026-09-29 02:12:21 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_3/.aii/manifest.yaml

entries: []
```

### [49] TOOL RESULT — Write · 2026-09-29 02:12:21 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_3/.aii/manifest.yaml", "content": "entries: []\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [50] TOOL CALL — Write · 2026-09-29 02:12:21 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_3/README.md

# gen_plan_experiment_3 (iteration 4): plan for the RQ2 trajectories re-run

This directory holds a PLAN only. Nothing was executed here: no data was downloaded and no API was called.

## What it plans

This re-runs the failed iteration-3 RQ2 artifact (gen_art_experiment_9, which was never executed) on cached EXP5, EXP7 and EXP8 arrays. It uses 0 OpenAlex credits and $0 of LLM calls. The steps are:

1. Write the method_out.json skeleton and validate it first (the old run died on output format).
2. Build OPEN covariates in three versions: all-papers, home-only, and size-matched.
3. Build D3 state sequences.
4. Decompose breadth as log contact x frontier x retention, with Shapley shares and an inverted pre-registration.
5. Fit a DTW + HMM typology under a strict naming rule; if no class passes, report a PCA continuum.
6. Run a light sequence test.
7. Build 6-8 matched case pairs, B5-matched with opposite OPEN.
8. Build a retrospective AI/CS atlas of 40 concepts.
9. Write pipeline counts.

## Layout

- `.terminal_claude_agent_struct_out.json`: the plan (ExperimentPlan schema).
- `.aii/manifest.yaml`: no heavy files, so it has no entries.
- `README.md`: this file.

## Restoring removed files

Nothing is marked for deletion, so there is nothing to restore.
```

### [51] TOOL RESULT — Write · 2026-09-29 02:12:21 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_plan/gen_plan_experiment_3/README.md", "content": "# gen_plan_experiment_3 (iteration 4): plan for the RQ2 trajectories re-run\n\nThis directory holds a PLAN only. Nothing was executed here: no data was downloaded and no API was called.\n\n## What it plans\n\nThis re-runs the failed iteration-3 RQ2 artifact (gen_art_experiment_9, which was never executed) on cached EXP5, EXP7 and EXP8 arrays. It uses 0 OpenAlex credits and $0 of LLM calls. The steps are:\n\n1. Write the method_out.json skeleton and validate it first (the old run died on output format).\n2. Build OPEN covariates in three versions: all-papers, home-only, and size-matched.\n3. Build D3 state sequences.\n4. Decompose breadth as log contact x frontier x retention, with Shapley shares and an inverted pre-registration.\n5. Fit a DTW + HMM typology under a strict naming rule; if no class passes, report a PCA continuum.\n6. Run a light sequence test.\n7. Build 6-8 matched case pairs, B5-matched with opposite OPEN.\n8. Build a retrospective AI/CS atlas of 40 concepts.\n9. Write pipeline counts.\n\n## Layout\n\n- `.terminal_claude_agent_struct_out.json`: the plan (ExperimentPlan schema).\n- `.aii/manifest.yaml`: no heavy files, so it has no entries.\n- `README.md`: this file.\n\n## Restoring removed files\n\nNothing is marked for deletion, so there is nothing to restore.\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [52] TOOL CALL — Grep · 2026-09-29 02:12:25 UTC

```
Pattern: "^  "[a-z_]+": ".*".*""
```

### [53] TOOL RESULT — Grep · 2026-09-29 02:12:25 UTC

```
{"mode": "count", "numFiles": 0, "filenames": [], "content": "", "numMatches": 0}
```

### [54] ASSISTANT · 2026-09-29 02:12:39 UTC

```
The plan for the RQ2 re-run is in `.terminal_claude_agent_struct_out.json`. I did not parse-check the JSON because I had no way to run code; a search for stray quote characters found none.

It re-runs the iteration-3 RQ2 artifact (gen_art_experiment_9), which never executed. It uses only cached EXP5, EXP7 and EXP8 files: no OpenAlex credits, no snapshot pass, no LLM spend. It asks for the `cpu_plus` compute profile.

**Things I found in the prior artifacts that shaped the plan:**
- **Home-only openness can be built from cache.** EXP8's early-hits file (`frame_matches_early/part_001.parquet`) records a venue field for each paper. So the home-only ego network can be recomputed from home-venue papers without a new snapshot pass.
- **EXP7's state panel is incomplete.** It covers 11,841 of the 12,499 concepts, because EXP7 dropped the EXP6 overlap. The executor rebuilds the missing 658 with EXP7's `lib/d3.py` and must show zero mismatches with the panel on the concepts it does cover.
- **Most of the ego-network runtime can be cut.** The six openness components need neither the null simulations nor betweenness. The plan uses a trimmed copy of EXP8's `lib/ego.py`, which must reproduce EXP8's `ego_features.parquet` to 1e-12 on 300 concepts before it is used.

**What the plan does:**
- **Output format first.** A `method_out.json` skeleton is written and validated against `exp_gen_sol_out` before any computation, and again after every stage. Exp9 failed at exactly this step.
- **Openness in three versions:** from all papers, from home-field papers only, and from all papers subsampled to the home-only count. Scaling constants are frozen on all 12,499 concepts.
- **Breadth decomposition.** Retained breadth at t0+8 splits into early contact × frontier advance × retention, with Shapley shares of the gap between the top and bottom residual-breadth terciles.
  - The pre-registration is inverted from iteration 3. Contact and exploration should carry more of the gap than retention, and localised concepts should have higher early retention ratios.
  - Results are reported within early-volume strata, with Medicine homes adjusted for and also excluded.
- **Trajectory types.** DTW k-medoids plus an HMM. A class is named only if all of these hold:
  - the two methods agree (ARI ≥ 0.5);
  - it is stable under bootstrap (Hennig Jaccard ≥ 0.75);
  - it replicates when the held-out concepts are re-clustered;
  - it survives dropping Medicine homes;
  - it is not just a volume class.

  Otherwise the result is reported as a continuum along the first principal axis, with the openness correlation for all three versions.
- **Light sequence test.** Does home prominence peak before off-home take-off, and do concepts born in two or more fields spread without it? It runs against a mechanical-lag null.
- **Case pairs.** Six to eight pairs matched on early volume and growth, with opposite openness, chosen by a written rule that excludes generic terms. Breadth outcomes are shown only after selection.
- **AI/CS atlas.** Forty concepts, labelled retrospective and descriptive, plus `pipeline_counts.json` read from the actual files.
- **Seal.** All choices are hash-sealed on the development split before held-out results are scored once.

**Limits the plan states openly:**
- **Held-out data is not fresh.** EXP5, EXP7 and EXP8 already opened the held-out outcomes. The seal here only fixes this artifact's own choices, so held-out agreement is a robustness check, not a confirmation.
- **The decomposition is an accounting identity, not a predictor.** Only the early-contact factor comes from the early window.
- **Topic-level detail is limited.** Topic-level networks exist only up to t0+2, so the atlas and case studies show field-level structure after that.

I also wrote `README.md` and an empty `.aii/manifest.yaml`, since the workspace holds no large files.

Sources:
- [Hennig, Cluster-wise assessment of cluster stability](https://www.homepages.ucl.ac.uk/~ucakche/papers/clusta.pdf)
- [fpc clusterboot documentation](https://rdrr.io/cran/fpc/man/clusterboot.html)
- [Seawright & Gerring 2008, Case Selection Techniques in Case Study Research](https://www.researchgate.net/publication/224952181_Case_Selection_Techniques_in_Case_Study_Research)
```
