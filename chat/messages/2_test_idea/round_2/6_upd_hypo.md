# upd_hypo — test_idea

> Phase: `invention_loop` · round 2 · `upd_hypo`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-28 21:00:49 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-28 21:00:55 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviser (Step 3.6: UPD_HYPO in the invention loop)

You received the current hypothesis, all artifacts, and the paper draft.
Revise the hypothesis based on what the evidence supports.

Honest revision → focused research. Inflated confidence → wasted iteration.
</your_role>
</ai_inventor_context>

You are deciding where a research run points next, using the evidence it
gathered this iteration. Your revised hypothesis IS the next iteration's
hypothesis — nothing else steers the run — so this is a steering decision
first and a piece of honest reflection second.

SCOPE: Your ONLY output is the revised hypothesis text. You do NOT run code,
produce artifacts, fix bugs, or otherwise act on the evidence yourself — the
next iteration of the invention loop will spawn fresh artifacts based on your
revised hypothesis. Reflect on the evidence and rewrite the hypothesis;
nothing else.

PRINCIPLES:
- Ground every revision in specific artifacts and results. A number that was
  projected, assumed or left as a placeholder is not a result.
- CLASSIFY EVERY ARTIFACT SEPARATELY, BEFORE CHOOSING A MOVE. One artifact
  is one bet. A round is normally MIXED, and judging the round as a whole is
  how one real positive gets thrown out with the nulls beside it. The round
  summary is then READ OFF the best of those verdicts, and the move follows
  from the summary and the remaining budget by a fixed rule — not by free
  judgement, because free judgement is where past runs went wrong.
- LATCH ONTO A GENUINE POSITIVE. One executed, non-obvious, baseline-proof
  result at a size the ask cares about is the run's whole output. Hold it,
  and spend the next round on its mechanism, its boundary, its confounds and
  its replication. Do not go looking for a different question while it lives.
- WEAK IS NOT NULL. A small real effect, a positive that lost to a baseline
  by a margin, a signal seen on one body of evidence — these are LEADS. The
  answer to a lead is to make it bigger and cleaner, not to abandon it. Widen
  off a lead only after deepening it has come back empty.
- A round where NOTHING is real is the signal to go WIDER, not smaller. The
  question the user asked is still open; the answer you tried is the only
  thing that was refuted, and every next bet should be a different answer to
  the ask.
- Never shrink the claim until the effect you happened to observe becomes
  the claim. A finding nobody needed is worse than an honest negative.
- A broken test is fixed ONCE, with the claim unchanged. A bet that breaks
  twice is dropped, and its budget goes to a new candidate.
- The run is looking for a POSITIVE, NON-OBVIOUS result. A clean negative is
  a LAST RESORT, right only when no iteration and no candidate remain.
- Increase specificity as evidence accumulates; do not inflate confidence
  without strong evidence.
- Revise hypothesis text only — never attempt to address feedback by running
  code, proposing fixes, or producing artifacts; the next loop iteration
  handles all artifact generation.

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo/`:
GOOD: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo/file.py`, `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo/results/out.json`
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

<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: Gateway fields keep new concepts and pass them on
hypothesis: >-
  MAIN CLAIM (RQ2 mechanism, answering RQ1's 'which signals generalise'). Cross-disciplinary integration of a new concept
  is decided one ADOPTION EPISODE at a time, where an episode is one concept adopted by one off-home field. It is not decided
  for the concept as a whole. Whether an off-home field that adopts a concept in t0..t0+2 still publishes on it in t0+6..t0+8
  (retention R_cj) is anticipated by the ADOPTING FIELD'S GATEWAY CENTRALITY: its eigenvector centrality on a frozen pre-period
  field-relatedness backbone (26-field topic co-assignment PMI, 1998-2002). The principle of relatedness (Hidalgo et al. 2018;
  Guevara et al. 2016) instead predicts that the field's relatedness to the concept's HOME field decides retention. We predict
  it does not. Mechanism, borrowed from metapopulation ecology (the rescue effect, Brown & Kodric-Brown 1977): a gateway field
  borders many fields, so a concept that has landed there keeps being re-imported from neighbouring fields and does not die
  out when the home field's interest fades. For the same reason the gateway field RELAYS the concept onward. Three consequences
  are tested. (H1, field level, primary) Gateway centrality predicts R_cj beyond the concept's early popularity and reach
  (B5: log early volume, growth, off-home share, entropy, reach), the field's size, its relatedness to home and its background
  citation insularity. Most importantly, it also beats the field's GENERIC RETENTION PROPENSITY: the leave-this-concept-out
  share of other same-cohort concepts that the field retained. That covariate is the confound that would reduce the effect
  to 'some fields keep everything'. (H2, RQ2 relay trajectory) After the first off-home retention, the next field a concept
  enters is better predicted by relatedness to the set of fields currently RETAINING it, weighted by their gateway centrality,
  than by relatedness to its home field. So trajectories that reach broad integration pass through an early retained gateway
  ('land in a gateway, stay, radiate'). Local concepts either never leave home or land only in peripheral fields and are lost
  there. Concepts born at an intersection (>= 2 home fields) form a separate stratum. (H3, concept level) The share of early
  off-home adoption that lands in gateway fields (G) predicts volume-residualised breadth (O2r_resid) and adds to B5. H3 is
  the concept-level aggregate of H1. EVIDENCE BEHIND THE CLAIM (iteration 1, dev panel only, a LEAD not a finding). art_33_KKk_G8Gw5:
  on 80 concept x off-home-field units from 28 concepts, adding gateway_j to B5 raises retention AUC by +0.103 (0.705 -> 0.808;
  95% CI [0.034, 0.167]; fixed-prediction bootstrap, refit CI not yet computed). The gain stays +0.102 with log field size
  in the model. Relatedness-to-home adds -0.000 and relatedness density +0.022. The gain is positive in Eng, BGM and Med and
  negative in CS. At concept level, G on O2r_resid gives delta-rho +0.15 (CI90 [0.0003, 0.32]), positive in 4 of 4 groups.
  On raw O2r G adds only +0.033 (CI90 [-0.095, 0.168]; refit CI90 [-0.196, 0.295]) on a weak baseline (rho_B5 = 0.327, n =
  34, 29 of 34 outcome windows truncated to the top-200 sources). art_xp8BGBJZsxeI independently shows that cross-field lineage
  varies mainly at the concept x field level (REML tau_cj = 0.65 vs tau_c = 0.29). CLOSED BETS, one sentence each in the paper:
  the naturalisation gap A*_h as a concept-level predictor (null: delta-rho -0.006, 0 of 4 groups, r_SB 0.58), and co-occurrence
  structural diversity D_ratio (delta-rho +0.006; out-of-group partial rho 0.335 is 1 of 12 tests and uncorrected). Both are
  only re-scored inside the frozen indicator matrix below, with no new budget. Two results are kept as reported measurement
  findings. M1: background homophily explains 66-72% of the between-concept variance in raw lineage log-odds, and 48 of 48
  background log-odds ratios are positive. Portability: raw co-occurrence growth indicators work only in CS. Candidate S (unconnected
  co-author components, Cheng et al. 2023) was NOT RUN because its artifact stalled; it is untested, not refuted. It gets
  its one fix as a pre-specified rival covariate in H3, but only if the snapshot's author IDs make it computable at zero credits.
  DESIGN THAT DECIDES IT (no new indicators are invented; power goes into more units). (1) ONE panel, ONE outcome table, ONE
  fold assignment. Everything is built from the free full OpenAlex S3 snapshot (476M works, the zero-credit column-pruned
  scan already used in art_yrradSC27HtQ): titles and abstracts, venue-source fields, referenced_works and author IDs. API
  credits are spent only on yearly count checks. Venue-field labels feed the features and author-career fields feed the outcomes,
  as before. (2) OUTCOME-BLIND FRAME N from the snapshot: title and abstract 2-3-gram noun phrases that are newly frequent
  in year t, with onset 2003-2014 under the relative newborn rule. Aim for >= 400 grounded concepts across all 26 home fields
  and >= 4,000 concept x off-home-field episodes. The existing P78 concepts are included, flagged. (3) GROUNDING first, as
  the user asked. Check existing resources (PubTator3 or MeSH for biomedical terms, legacy OpenAlex concepts with Wikidata
  IDs), then build a 500-pair labelled benchmark (cheap LLM labels, 150 double-labelled, 60 checked by hand; 300/200 train/test).
  Train a logistic sense filter on MiniLM embeddings plus match flags. Drop concepts with precision < 0.8 before any outcome
  is looked at. (4) STRICT SPLIT. SCREEN or DEV = home groups CS, Eng, BGM and Med with onset 2003-2009. It is used only to
  freeze the H1-H3 specifications, the covariate set and the top-10 indicator list; the gateway_j definition is already frozen
  from iteration 1. CONFIRMATION = held-out home groups (physical; life and environment; social; mathematics and decision
  sciences) with onset 2003-2009, plus the 2010-2014 cohort in all fields. These data are fetched after freezing and evaluated
  once. (5) CONFOUND ATTACKS for H1. (a) The leave-concept-out retention propensity of the field in the same cohort. (b) Within-field
  variation: gateway centrality recomputed on sliced backbones (1998-2002, 2003-07, 2008-12), used as a time-varying regressor
  with FIELD FIXED EFFECTS, so the effect cannot be a constant field trait. (c) A degree-preserving rewired-backbone placebo,
  which must give no gain. (d) A boundary test: the effect is predicted to weaken when the home field is itself a top-tercile
  gateway, which would explain the CS failure. (e) Label coverage and truncation as covariates, with no top-200-source truncation.
  (6) Resampling. Refit bootstraps clustered by concept (2,000 draws) are the only reported CIs. Groups are pooled by a random-effects
  meta-analysis (pooled estimate, I^2, sign test). (7) RQ1 DELIVERABLE, with no new metrics. Iteration 1's ~34 co-occurrence
  indicators, 14 lineage indicators and ~20 G/reference indicators are recomputed on the common panel. Per-group and pooled
  Spearman, AUC and out-of-group partial rho given B5 go into one matrix. The top 10 per outcome (O1 uptake, O2r, O2r_resid,
  O3 transience, O4 citation growth, O5 external recognition) are frozen on dev and scored once on held-out data, Holm-corrected.
  Indicators that work in one domain only are reported as negative results. Because the iteration-1 positive-control ladder
  showed that delta-rho over B5 is insensitive (a feature needs rho of about 0.95 to gain 0.10), the pre-registered concept-level
  quantity is partial association given B5 and O2r_resid, not delta-rho on raw O2r. (8) RQ2. Episode sequences (entry, retention
  and loss for each field-year) for concepts with O1 = 1 are clustered with DTW k-medoids and a Gaussian HMM, with k chosen
  by silhouette and bootstrap stability and no predefined classes. The per-year ego-network series from art_yrradSC27HtQ (entropy,
  participation, betweenness) are added. We test whether the first retained gateway precedes entropy take-off, using a change-point
  detector calibrated to a 5% false-alarm rate plus threshold-free lead-lag panels with concept fixed effects. The O1 gains
  of the G variants (+0.07 to +0.15 AUC) are checked once for a shared artefact by adding label coverage and the O1 base rate
  to B5. SUCCESS. H1 is CONFIRMED on held-out data if all of these hold: gateway_j delta-AUC >= 0.05 over the full covariate
  set (B5, size, relatedness-to-home, field retention propensity, insularity, coverage) with a concept-clustered refit 95%
  CI > 0; the same sign in >= 3 of 4 held-out groups and in the cohort; a positive within-field coefficient under field fixed
  effects; and a null placebo. H2 is CONFIRMED if gateway-weighted relatedness to retaining fields adds to relatedness-to-home
  and field size in held-out conditional logit (likelihood-ratio test p < 0.01), and among broad concepts (top O2r tercile)
  the first retained gateway precedes entropy take-off in >= 60% (sign test). H3 is CONFIRMED if the held-out partial rho
  of G with O2r_resid given B5 is > 0 after Holm correction. INFORMATIVE EITHER WAY. If gateway_j dies once field retention
  propensity or field fixed effects are added, the finding is that retention is a TRAIT OF THE ADOPTING FIELD, not of the
  concept-field fit or the field's position. That would contradict both the relatedness principle and concept-level emergence
  indicators, and it is reported as such. DISCONFIRMED: the pooled held-out delta-AUC CI includes 0, or the effect holds only
  in dev groups. The paper still reports the full held-out indicator x outcome x field matrix, M1 and the trajectory taxonomy.
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
  Concept-level naturalisation becomes one dyad property in a concept x field frame led by gateway retention
_confidence_delta: decreased
_key_changes:
- >-
  The headline moves from the concept-level naturalisation gap A*_h (null: delta-rho -0.006, 0/4 groups, r_SB 0.58) to the
  field-level gateway-retention LEAD from art_33_KKk_G8Gw5 (delta-AUC +0.10, 95% CI [0.03, 0.17], survives field size, not
  in CS).
- >-
  The unit of analysis becomes the concept x off-home-field adoption episode. This is backed by REML tau_cj = 0.65 > tau_c
  = 0.29 in art_xp8BGBJZsxeI.
- >-
  A named mechanism (the metapopulation rescue effect plus relay) gives a non-obvious prediction: the adopting field's centrality,
  not its relatedness to the concept's home, decides retention. This goes against the principle of relatedness (Hidalgo 2018;
  Guevara 2016), which is now cited as the nearest neighbour.
- >-
  The obvious confound is attacked head-on: the field's generic leave-concept-out retention propensity, time-varying centrality
  with field fixed effects, a degree-preserving rewired-backbone placebo, and a boundary test for gateway home fields (the
  CS failure).
- >-
  Power goes into more units, not more metrics, as the reviewer asked. One common panel, outcome table and fold assignment
  are built from the zero-credit OpenAlex S3 snapshot (>= 400 concepts, >= 4,000 episodes), replacing three experiments that
  each computed their own O2r and home labels.
- >-
  The failed held-out dataset (gen_art_dataset_1, stalled) is rebuilt first. Screen = CS/Eng/BGM/Med homes, onset 2003-2009;
  confirmation = physical, life/environment, social and mathematics/decision homes, onset 2003-2009, plus the 2010-2014 cohort,
  evaluated once after freezing.
- >-
  Given the positive-control ladder, the concept-level primary becomes partial association given B5 and O2r_resid, with a
  Holm-corrected frozen top 10. Only concept-clustered refit bootstrap CIs are reported.
- >-
  RQ2 is tested as a relay trajectory (land in a gateway -> retained -> radiate) with conditional-logit next-field entry,
  DTW/HMM episode clustering and power-matched ordering tests, reusing art_yrradSC27HtQ's yearly ego-network series.
- >-
  A*_h and D_ratio are closed as headline bets and are only re-scored inside the frozen RQ1 matrix. M1 (background homophily
  explains 66-72% of raw lineage variance) and CS-only co-occurrence growth are kept as measurement and negative findings.
  Candidate S is recorded as not run, not refuted, and gets its one fix only as a zero-credit rival covariate.
- >-
  The reviewer's evidence corrections are carried into the claim: rho_B5 differs by experiment (0.834, 0.770, 0.327), so the
  ceiling argument applies only to Exp1 and Exp3; A*_h medians are negative in all groups; the O1 gains of G variants are
  checked for a shared label-coverage artefact; and G_all and DOM_Physical are recorded as variants that hurt O2r.
_evidence_state: lead
_move: deepen
_move_rationale: >-
  Best strand is a lead (gateway retention dAUC +0.10, dev only, n=80). Deepen it: more units from the free snapshot, field-propensity/FE
  confounds, held-out confirmation.
_coverage: full
_coverage_statement: >-
  Next iteration answers RQ2 (how and through which fields concepts go from local to broadly integrated, as relay trajectories)
  and RQ1's held-out step (the frozen top-10 indicators, scored once on held-out fields and a later cohort with per-domain
  results).
_candidates_considered: 9
relation_type: embedding
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

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
in_dependencies:
- id: art_33_KKk_G8Gw5
  label: evaluates
- id: art_xp8BGBJZsxeI
  label: replication units
- id: art_yrradSC27HtQ
  label: replication units
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
</all_artifacts>

<previous_round_strands>
How you classified the PREVIOUS round's artifacts, one per bet. Use it for the
BROKEN-FIXED-ONCE rule: a bet that was "broken" then and is "broken" again now is
not a defect any more — drop it and give its slot to a new candidate. A "lead" that
you already deepened once and that came back "null" is the one case where widening
off a lead is allowed.

--- Strand 1 ---
artifact: art_xp8BGBJZsxeI
state: 'null'
why: >-
  A*_h delta-rho -0.006 (CI90 [-0.034,0.017]), 0/4 groups, r_SB 0.58, field-level dAUC +0.002; M1 (R2 0.66) is a measurement
  fact, not a predictive positive.

--- Strand 2 ---
artifact: art_yrradSC27HtQ
state: 'null'
why: >-
  D_ratio delta-rho +0.006 (CI90 [-0.09,0.14]); the partial rho 0.335 is 1 of 12 tests, its CI95 includes 0 and it is uncorrected;
  F_res -0.06. Portable indicators are redundant with B5.

--- Strand 3 ---
artifact: art_33_KKk_G8Gw5
state: lead
why: >-
  Field gateway_j adds retention dAUC +0.10 [0.03,0.17], survives field size, not CS; G on O2r_resid +0.15 CI90 [0.0003,0.32].
  n=80 rows/28 concepts, refit CI and field-propensity control pending.
</previous_round_strands>

<new_artifacts_this_iteration>
These 5 artifacts were created THIS iteration.

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

id: art_lwI2DuRtQRZX
type: evaluation
in_dependencies:
- id: art_33_KKk_G8Gw5
  label: evaluates
- id: art_xp8BGBJZsxeI
  label: replication units
- id: art_yrradSC27HtQ
  label: replication units
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
</new_artifacts_this_iteration>

<current_report>
This round's research report, every round in order, is at /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/current_report.md. The artifacts above are the evidence; open the report for how they
were written up, which the reviewer feedback below refers to.
</current_report>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

The previous review is BLOCKING: the paper must not ship as it stands. Every MUST-FIX item below is a requirement for this iteration, not a suggestion — an iteration that leaves one unaddressed does not publish.

- [MAJOR MUST-FIX] (evidence) Section 10.3 contradicts the artifact. It states H1 is 'DISCONFIRMED by all preregistered criteria'. Exp5 results/h1_heldout.json verdict_H1.criteria lists lpm_beta_within_gt0_p05 = true: the within-field linear probability model with field FE gives beta_within_per_sd = 0.068, p_concept = 0.041 (two-way clustered p = 0.17), and the all-splits version gives 0.051, p_concept = 0.0065. cohort_same_sign is also true, trivially, because both are negative. The report never mentions the LPM, the clustered-SE logits (held-out beta -0.045, p 0.29) or the boundary test (interaction +0.064, p 0.45, 'consistent: false'). A positive within-field gateway coefficient on held-out data is exactly the kind of residual signal the record must keep, especially since the report concludes that gateway is 'a domain specific proxy, not a position dependent causal factor'.
  Action: Replace 'by all preregistered criteria' with a criterion-by-criterion table built from verdict_H1.criteria. Add rows for lpm_field_fe, lpm_field_fe_all_splits, logit_clustered_se (concept / two-way / field) and boundary, for both DEV and held-out. State that the within-field LPM passes at concept-clustered p < 0.05 but not with two-way clustering, and that the verdict rule still returns DISCONFIRMED.
- [MAJOR MUST-FIX] (evidence) The ordering finding (11.3, 16.3: 'first retained gateway field precedes entropy takeoff', listed as CONFIRMED) is contradicted by the artifact's own lead-lag evidence, which the report paraphrases selectively. In heldout_result.json ordering.lead_lag, the concept+age FE regression of next-year entropy change on retention has NEGATIVE coefficients: ret_gw b = -0.028 (p = 0.0007), ret_per b = -0.043 (p = 6e-8). The report says only that both are 'associated with subsequent entropy change'. The event study shows a significant pre-trend: ev-3 = -0.072 (p = 0.0002; dev -0.088, p = 6e-6), so entropy was already rising before first gateway retention. In dev_result.json the reverse path (entropy -> next-year gateway retention) is significant (b = 0.232, p = 0.006), but the report states 'the reverse ... is not significant (p = 0.22)', quoting only held-out. On dev, peripheral fields precede take-off as often as gateway fields (70.3% vs 71.4%, McNemar p = 0.34). Finally, '66% of broad concepts' is 57 of 175 top-tercile concepts (33%). The 65.5% is among the 87 non-tied cases of the 102 evaluable, after 63 concepts had no detected change point.
  Action: Add the full ordering table for DEV and held-out (n_top, n_tau_detected, before/ties/after for gateway and peripheral, McNemar), the forward/reverse lead-lag coefficients and the event-study coefficients. Reword 16.3 as: 'the preregistered sign rule passes, but concept-FE lead-lag regressions show retention followed by smaller entropy gains, a significant pre-trend, and (on dev) entropy predicting later gateway retention; the ordering is not specific to gateway fields (placebo p = 0.63)'. Move it from 'Confirmed' to 'Mixed / not established'.
- [MAJOR MUST-FIX] (rigor) H3 (concept-level gateway landing -> volume-residualised breadth) is listed as 'confirmed' (10.6, 16.5), but its uncertainty is under-reported and variants are cherry-picked. From exp5 results/h3_results.json: the concept-bootstrap 95% CI of pooled G is [-0.006, 0.065], which includes zero. The artifact's note says the within-group permutation null is centred below zero (about -0.012), so the Holm p = 0.0045 is measured against a shifted null. G_btw's DL-pooled estimate is 0.072 with CI [-0.015, 0.159], I2 = 0.77, and it is negative in LifeEnv (-0.020). The DEV values were G 0.138 and G_btw 0.170 (h1_dev.json H3_dev), so held-out shrinkage is about 4x, which the report never states. Section 16.5 quotes the G_btw pooled partial (0.046) next to G's DL pooled (0.068), mixing variants to present the best numbers. The phrase '0 of 40 shuffled outcomes exceed the real value' is wrong: audit_placebo.json reports a 0/40 FALSE-POSITIVE RATE of the test on shuffled outcomes, a calibration check, not an exceedance count. Held-out n (2,838 concepts) is not given.
  Action: Add an H3 table with n, pooled partial rho, concept-bootstrap CI95, per-group rho (PHYS/LIFEENV/SOC/MATHDEC), DL pooled with CI and I2, and the DEV value for each of G, G_A, G_btw and REL_home. Quote the permutation-null centring note. Relabel as 'passes the preregistered permutation rule; pooled bootstrap CI includes zero; effect about 0.03 partial rho, a quarter of its DEV value'. Fix the 0/40 wording.
- [MAJOR MUST-FIX] (evidence) Previous MUST-FIX items remain unaddressed although the data is on disk. (a) The 34-row exp3 portability table is still missing: iteration 2 corrected the wording only, and the full table is now even pre-harmonised in art_lwI2DuRtQRZX eval_out.json metadata.F_record.F3_exp3_portability. The portable NEGATIVE signal edge_persistence and the size-confounded indicators are still absent. (b) Section 4.4 claims the remaining 7 of 12 partial associations are 'not available in the current workspace output'. That is false: iter_1 gen_art_experiment_3/results/exploratory_partial_association.json holds all 12 (D_z 0.313 [-0.161, 0.634] 4/4 groups; D_sub 0.245 4/4; n_comm_W3 0.218; F_z -0.248; F_bg -0.301; deg_growth 0.050; btw_change -0.168), and the permutation p = 0.037 is in results/audit.json perm_p_value_one_sided. (c) The exp1 robustness table is still missing (GLMM agreement 0.163, probe agreement 0.10, refit CI [-0.092, 0.023], newborn_only / full_parent_sample / O2r_m50 / O2r_m20 / B5+offhome sensitivities, field-level with-data-only dAUC -0.010), as is the note that r_SB 0.58 is unaudited. (d) There are no refit CIs for the concept-level headline deltas (A*_h, D_ratio, G) or for O2r_resid +0.15. (e) There is no iteration-1 'why this iteration' paragraph. (f) The next-field entry numbers in 5.5 are still untraceable. (g) The 5.4 'B5 + all_four' row still carries the size_controlled_all_three numbers (0.697 -> 0.782, +0.085); F5 shows its refit CI95 is [-0.043, 0.220].
  Action: Paste F3 in full (34 rows: pooled rho, four within-group rhos, rho_logvol, rho_growth, LOGO delta-rho). Replace 4.4's partial table with all 12 rows (rho, CI90, CI95, groups positive) and cite audit.json for p = 0.037. Add the exp1 robustness table. Add refit CI columns to the 6.2 decisive table, and either recompute the O2r_resid refit CI or label it 'fixed-prediction CI only'. Add the iteration-1 reasoning paragraph. Relabel the 5.4 rows and add the F5 refit CI for every row.
- [MAJOR MUST-FIX] (evidence) Many executed iteration-2 results are absent. Exp5 [art_wxWssKSUR45f]: sensitivities in h1_heldout.json (R_abs1 +0.0008, R_abs2, R_abs3, n_early>=5 -0.0004, newborn_only +0.0023 [-0.004, 0.013], excl_intersection_born); leave_one_field_out; the crossed concept x field (pigeonhole) bootstrap whose held-out CI [-0.0023, 0.0010] and DEV CI [-0.0056, 0.0013] are roughly 3-5x wider than the concept-only CIs the report presents as 'the only reported CIs'; T5 seed stability; the DEV rival head-to-head, where the relatedness pair is -0.00017 [-0.0017, 0.0012] on DEV, so its held-out +0.0034 was not seen in development; the per-group exploratory_domain_specificity table (gateway-P_j Spearman 0.83 in CS, -0.26 in PHYS), which is the actual evidence for the 'proxy for fields that keep things' claim; and the iteration-1 replication n and CI (85 episodes, 39 concepts, +0.023 [-0.004, 0.068], checks.json). Exp6 [art_N-mpomDZZ1ln]: the HMM trajectory model (6 states) and its HMM-vs-DTW ARI of 0.094, which is a direct robustness failure of the 'two stable classes' claim; the DTW k-selection grid (k=2 silhouette 0.29, lower bound of the stability ARI 0.81); the dev trajectory solution (66/62, with the localised class 55 Med + 7 Eng, 0 BGM, 0 CS); rescue models R1_s_other, R2_base, R2_full; the H1 replication in Exp6 (gateway b 0.005, p 0.70); relay_excess_ols (ret_x_top +0.288, p = 0.07, opposite in sign to the reported fepois); M2lost (relatedness to LOST fields, d = -0.063, LR p = 0.055); and the whole dev_result.json block (dev H2 robustness, planted control, power check).
  Action: Add an 'Exp5 robustness' table and an 'Exp6 robustness' table built from these keys. In 11.5, add the HMM result and the k-grid, and state that the two-class DTW solution is not reproduced by the HMM (ARI 0.09) and largely separates Medicine homes from the rest. In 10.5, state that the relatedness-pair gain is held-out only (DEV -0.0002). Add the pigeonhole CIs next to the concept-only CIs.
- [MAJOR MUST-FIX] (novelty) The one confirmed positive result, H2 (relatedness to the currently retaining fields predicts the next field entered), is claimed as new in Section 14.4 because it 'goes beyond the principle of relatedness ... by using the concept's retaining community as the reference set'. The nearest neighbour is the standard Hidalgo et al. (2007) density itself. It is computed over the portfolio where the actor has REVEALED presence (RCA > 1), i.e. a thresholded, persistent presence, which is essentially 'retained'. Exp6's M0 baseline instead uses a non-standard density over ALL fields ever entered (method.py: 'sum_{j in entered(t-1)} phi[j,k] / sum_j phi[j,k]'). M1 beating M0 (LR 68.6) may therefore only show that the conventional thresholded density beats an unthresholded one. The M2lost result (relatedness to lost fields is negative-leaning, LR p = 0.055) supports that reading. Other close neighbours are not compared: Guevara et al. (2016) research space entry AUCs of 0.68-0.90; Chinazzi et al. (2019, EPJ Data Science, 'Mapping the physics research space') predicting country entry into PACS subfields from relatedness; Boschma, Balland & Kogler (2015) for technologies in cities. Absolute within-stratum AUCs are 0.817 for M1/M2 vs 0.809 for M0, and log field size alone reaches 0.757. The gateway weighting adds nothing (M3 vs M1 perm p = 0.17).
  Action: Add to M0 a density computed on the conventionally thresholded portfolio (fields where the concept's share exceeds its expected share at t-1, or retained fields by the R definition) and re-test M1 against it on the frozen held-out risk sets. The risk sets exist in entry_risk_sets_heldout.parquet, so this needs no new data. Report the M1 coefficient (d0_ret_rel 0.281 ± 0.032) as the headline, not the gateway-weighted one. Write down the Hidalgo 2007 / Guevara 2016 / Chinazzi 2019 comparison and what, if anything, survives it.
- [MAJOR MUST-FIX] (evidence) The Dataset 2 source table (13.1) misstates coverage. Checked against out/coverage_report.json by_source: ACM CCS 1,298 concepts with events (report: 3,583, which is the external-entry count); MSC 1,121 (report 17,872 = entries); PACS/PhySH 2,635 (report 8,462 = entries); English Wikipedia 64,363 concepts with an event, 50,459 year-usable, 7,806 exact (report: 6,540); Wikidata 1,425 found, 1,316 year-usable; the curated lists are split as Gartner 466, MIT TR10 313, Research Fronts 589, NM MoTY 38, Science BOTY 53, PW BOTY 100 (the report lumps them as 589); JEL 213 found, 0 events. The dataset is also never used: O5 external recognition was built but not joined to any panel, so the request's 'externally documented recognition' ground truth still does not exist as an outcome.
  Action: Replace the table with n_with_event and n_with_year_usable_event per source from coverage_report.json, plus the per-group dated-taxonomy coverage (dated_domain_taxonomy_by_group). Record explicitly that O5 has not been evaluated against any indicator, and make joining O5 to the Exp5 frame (frame_concepts.csv, 12,499 concepts sharing legacy concept IDs) a zero-credit next step.
- [MAJOR MUST-FIX] (scope) Coverage of the original request is partial, and the run has drifted. The request's core RQ1 deliverable is a 30-50 indicator screen of temporal KNOWLEDGE-NETWORK indicators (new edges, neighbourhood novelty, centrality change, community transitions, brokerage, clustering), with the ~10 strongest validated on held-out fields and results reported globally and per field. Iteration 2 tested only field-relatedness quantities from economic complexity (gateway eigenvector, phi_home, density) on the large panel. The co-occurrence and lineage indicators exist only on the 46-48 concept dev panels, and no indicator was ever validated on held-out concepts. Section 16 admits the indicator matrix has not been rescored. Also missing: the exploratory AI-first stage (step 1), external-recognition outcomes (built but unused), the 'explain why the strongest indicator works' analysis with case studies (Exp6 generated case field-flow figures that the report never mentions), and the learned model. There is no updated iteration-2 coverage table.
  Action: Add an iteration-2 column to the 8a coverage table. Make the next iteration's first priority computing the frozen concept-level co-occurrence indicator set (Exp3's ~30 ego-network indicators) on the Exp5 frame. The snapshot scan and frame already exist at zero credits. Then select the top ~10 on DEV and score them once on the sealed held-out groups against O1/O2r/O3 and O5.
- [MAJOR MUST-FIX] (methodology) The iteration-2 design called for 'one common panel', but two incompatible panels were built, and the report does not say so. Exp5: 12,499 concepts, TAG rule (tag score >= 0.3 + title), Wikidata aliases, LLM precision gate, grounding benchmark with inter-LLM kappa 0.20 (deviations.json benchmark_kappa; the report quotes only the 90% LLM-hand agreement). Exp6: 653 newborn concepts, tag-AND-title, no Wikidata aliases, precision 0.996, a separate frame and episodes.csv. H1/H3 and H2/trajectories are therefore tested on different concept sets, grounding rules, home definitions and episode definitions: Exp6's 1,865 episodes against Exp5's 27,393. H2's held-out also includes the 2010-14 cohort of DEV-home fields. The Exp5 frame's onset agreement with P78 is 53% (|dt0| <= 1).
  Action: State in Section 9 or 11 that the common-panel design was not realised, and give a frame-comparison table (n concepts, grounding rule, precision, alias use, home rule, episode definition, overlap of concept IDs between the Exp5 and Exp6 frames). Either re-run H2 on the Exp5 frame (27k episodes) as a replication, or state that H2 is established only on the 653-newborn frame.
- [MINOR] (rigor) The power statements in 10.7 are misattributed and internally inconsistent. 'MDE 0.004 at 80% power' comes from h1_dev.json power, where b = 0.3 gives power 0.90 (b = 0.2 gives 0.65), so 0.004 is the 90% point. At b = 0 the CI>0 rule fires 12.5% of the time, versus a nominal 2.5%, indicating an anti-conservative concept-only bootstrap. The sentences about 'SD ~0.015 regardless of episodes' and '~34 concepts per group' come from Evaluation 1 (E_power), not Exp5, and imply an MDE floor of ~0.02, five times larger than 0.004. The report does not reconcile them.
  Action: Split 10.7 into Exp5 power (with the simulation grid and the null rejection rate 0.125) and Eval1 power (cite 12.6). Explain that the two differ because Eval1 includes a field random intercept and Exp5 does not, and say which one governs the H1 verdict.
- [MINOR] (clarity) Some summary statements overstate or mislabel results. 16.1 says H2 is 'positive in all three evaluable holdout field groups', but only Physical's CI excludes zero (LifeEnv LR p 0.23, Social 0.076; sign test over 4 is p = 0.0625). 14.2 says the principle of relatedness is 'confirmed for concept field retention' from a held-out-only dAUC of +0.0034 that is absent on DEV. 16 says 'two iterations and eight artifacts', but ten were commissioned and two failed. Exp6's first worker attempt crashed and was re-run, and this is not recorded.
  Action: Qualify each statement with the per-group CIs and the DEV value, and give artifact counts as 'ten commissioned, eight completed'.
</reviewer_feedback>



<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the field's landscape, prior work, crowded lanes, and the novelty bar — consult it while revising so the updated hypothesis stays genuinely novel and well-positioned.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<ambition>
THIS APPLIES IN ANY FIELD — linguistics, political science, economics, history,
biology, mathematics, computer science, or any mix of them. Where an example
below names a unit of study, read it as whatever your field's equivalent is:
languages, elections, markets, periods, corpora, species, model families, proof
techniques.

THE DEFAULT DELIVERABLE IS A NOVEL CONTRIBUTION. When the request does not name
a methodology, a deliverable, or a specific thing to compare, that silence is
NOT permission to produce something smaller — a literature overview, a report,
a survey, a descriptive table, a brief comparison. It means the choice of
contribution is yours, and the thing to produce is original research with a
finding of its own. Only an explicit request for a review or a replication
changes that.

CALIBRATE AMBITION TO WHAT THE REQUEST LEAVES OPEN. Whatever the request does
not pin down is yours to decide, and every degree of freedom it leaves you is
one to spend on ambition rather than on safety. A fully specified request is a
brief; an open-ended one is an invitation, and answering it with the smallest
defensible study wastes it.

THE TARGET is the most ambitious claim you can still expect to LAND — to finish
within the available resources with a non-trivial, genuinely insightful,
POSITIVE result. Both halves bind. Ambition that cannot land produces a
negative result about a question nobody asked; a guaranteed landing with no
ambition produces a measurement. Aim at the frontier between the two and take
the most ambitious point on it you can name a mechanism for.

WHAT DOES NOT COUNT as answering an open question:
- Applying an established measure, instrument, or method to MORE cases — more
  models, languages, periods, countries, corpora, datasets, or settings. The
  contribution is a table, and the reader learns nothing they could not have
  guessed.
- Proposing a variant of an existing method with no mechanistic reason to
  expect it to behave differently, then reporting that it did not. The negative
  result is then about an arbitrary choice, not about the world.
- Re-describing a known effect in new vocabulary, or naming it.
- A survey, a ranking, or a replication — unless that is what was asked for.

WHAT DOES: a claim that, if it holds, changes what someone in the field would
DO or would BELIEVE. Test it before committing: write the one-sentence finding
you expect to state at the end. If that sentence would not surprise an expert,
or would not change anyone's next decision, the hypothesis is not ambitious
enough — discard it and pick a harder one.

POSITIVE BY DESIGN, NOT BY LUCK. Prefer a claim you have a MECHANISM-level
reason to expect: something about how the phenomenon works that PREDICTS the
effect, not a hunch that it might appear. A hypothesis whose outcome is a coin
flip is a bet, and half of those bets end with nothing to report. Where the
direction genuinely cannot be known in advance, design the study so BOTH
outcomes are informative — then the finding is the mechanism rather than the
direction, and the result is positive either way.

SCALE THE CLAIM, NOT THE AMBITION, when resources bind. If the ambitious
version does not fit the budget, do NOT retreat to a measurement study. Narrow
what the claim COVERS — one language instead of twenty, one period, one
population, one model family — while keeping the mechanism it is about intact.
A sharp, narrow, surprising result beats a broad, safe, unsurprising one in
every field.
</ambition>

<evidence_state_and_move>
This is iteration 2 of 5. There are 3 iteration(s) AFTER this one.
Your revision is the ONLY thing that decides where the next iteration points,
so work the three steps below in order and do not skip to a conclusion.

The run is looking for a POSITIVE, NON-OBVIOUS result. A null is a last
resort, never a destination.

STEP 1 — CLASSIFY EVERY STRAND, SEPARATELY.

A STRAND is ONE artifact of this round: one bet, one test, one attempted
answer. Put EVERY artifact this round produced into `strands` — one entry
each, no merging, no omissions — with `artifact` (its name or id exactly as
listed above), `state`, and `why` (≤200 chars: the number, or the defect).
Rounds are MIXED. Judging a round as a whole is how one real positive gets
thrown away with the nulls around it.

- "genuine_positive" — ALL FOUR must hold:
  (a) the number was EXECUTED, not projected, assumed or placeholder;
  (b) it is at a size the ORIGINAL ask would care about — not the smallest
      size that clears a significance threshold;
  (c) it survived the obvious alternative explanation — the baseline, the
      confound, the simpler account that would produce the same number;
  (d) a reader in the field could NOT have predicted it before you ran it,
      and it is not already published.
- "lead" — real, but not yet genuine. A small effect in the right direction;
  a positive that lost to a baseline or missed a pre-registered bar by a
  margin; a signal seen on ONE body of evidence only. A lead is something to
  CHASE, not something to report.
- "null" — it ran and left nothing to build on: no effect, or one you cannot
  separate from the baseline or from noise.
- "broken" — it never tested the claim. A defect in the code, the data, the
  measure, the sample or the setup, a run that did not finish, or numbers
  that were never executed. The claim is UNTESTED here, not refuted.

STEP 2 — READ THE ROUND SUMMARY OFF THE BEST STRAND.

`evidence_state` is NOT a separate judgement. It is whichever of these fires
first:

- any strand "genuine_positive"  ->  "strong_survivor"
- else any strand "lead"         ->  "lead"
- else any strand "null"         ->  "weak_or_null"
- else (every strand "broken")   ->  "experiment_broken"

STEP 3 — READ THE MOVE OFF THE SUMMARY. A lookup, not a judgement — the
judgement was STEP 1:

- "strong_survivor" -> LATCH ON. `deepen` (why does it hold — the mechanism,
  the boundary where it stops, the confound that would explain it away) or
  `extend` (replication in a SECOND family, population, period, corpus or
  case set). HOLD the title and the object of the positive strand: do not
  rewrite the run around a different question while a real result is alive.
  Null strands of this round are CLOSED — one sentence in the paper, no
  further budget.
- "lead" -> `deepen` ON THAT LEAD. WEAK IS NOT NULL. Make it BIGGER and
  CLEANER before abandoning it: more power, a cleaner measure, the baseline
  it lost to attacked head-on, the second body of evidence it has not been
  seen on. `widen` here ONLY if this same lead was ALREADY deepened last
  round and came back null.
- "weak_or_null" AND at least one iteration remains -> `widen`. MANDATORY.
  Not "consider widening". Every artifact next round is a DIFFERENT bet on
  the ORIGINAL ask; none of them refines the idea that just failed.
- "experiment_broken" -> `fix`, ONCE. Keep the claim EXACTLY as it is, name
  the defect precisely in `move_rationale`, and say what a correct test looks
  like. Do not reframe, soften or re-scope a claim that was never tested.
  BROKEN IS FIXED ONCE: if the SAME bet already came back "broken" in the
  previous round's strands, it is not a defect any more — drop that bet and
  give its slot to a new candidate.
- `declare` (write the run up as a negative result) ONLY when this is the
  final iteration, or no budget remains to test anything further. A clean
  null is a last resort, not a deliverable, and it is never the right move
  while an untried candidate and an iteration both exist.

HOW TO WIDEN, when the rule says widen:

1. Go back to the USER'S ORIGINAL ASK — not to the hypothesis you just
   refuted. The refuted hypothesis was one answer to that ask; the ask is
   still open.
2. Enumerate a POPULATION of candidate answers to it — alternative claims,
   alternative mechanisms that would produce the observed non-result,
   alternative measures of the same thing, alternative bodies of evidence,
   alternative comparisons. Aim for many and cheap, not one and careful.
   Write down how many you weighed.
3. Propose a CHEAP SCREEN that tests all of them at once, coarsely, at a cost
   comparable to one deep test — and a HELD-OUT CONFIRMATION that the screen
   never saw, for whichever candidate survives it.
4. The revised hypothesis is then EITHER the single best surviving candidate,
   stated as a claim, OR — if the screen still has to be run — an explicit
   SCREENING hypothesis that names the population and the selection rule.
   Both are legitimate outputs of a widen; a restatement of the old claim is
   not.

<narrow_salvage_ban>
The failure this procedure exists to stop: a null result, and the revision
quietly shrinks the claim until whatever the data did show becomes the claim
— a smaller population, a milder verb, a subgroup, a weaker measure, an
effect in the direction everyone already expected. Each step is defensible.
The run ends with a finding nobody needed.

What is banned is SHRINKING THE CLAIM TO FIT A NULL. It is NOT a ban on
pursuing a small real effect: keeping a "lead" strand alive and going after
it harder next round is the opposite move, and it is required rather than
forbidden — the claim stays the size it was and the TEST gets stronger.

So: you may not REWRITE the claim down to the size of the effect you happened
to observe, UNLESS the paper can state why that smaller effect is ITSELF the
answer to the ask — a bound someone needed, a mechanism that only shows up at
that size, a belief it overturns. If you cannot write that sentence, the move
is `deepen` on the lead or `widen`, never a smaller claim.
</narrow_salvage_ban>

<screening_discipline>
Widening multiplies the number of claims in play, and a population of
candidates screened on one body of evidence will always contain one that
looks good by chance. So a widen is only honest with the discipline attached:

- Report `candidates_considered` — how many alternative claims you actually
  weighed this revision, not how many you could imagine. 1 means you weighed
  none, and after a weak or null result with budget left, 1 is a failure to
  do the move.
- A candidate is SCREENED on one body of evidence and CONFIRMED on another
  that the screen never touched — a held-out split, a later period, a
  different population, corpus, site, cohort or case set. Say in the revised
  hypothesis which evidence is which.
- The winner of a screen is a CANDIDATE, never yet a finding. Do not write a
  screening result as the answer, and do not report the best of several
  screened effects as though it had been the only one tested.
- Never re-screen on the confirmation evidence after seeing it. If the
  confirmation fails, that candidate is dead; go back to the population, do
  not go hunting for a subgroup where it survives.
</screening_discipline>

COVERAGE. Independently of the move, answer: does the hypothesis you are
about to write still answer the USER'S ORIGINAL ASK? Set `coverage` to
"full" (it answers the ask), "partial" (it answers a recognisable piece of
it) or "lost" (the run has drifted onto a different question), and write one
sentence in `coverage_statement` saying which part of the ask the next
iteration will answer. "lost" is not a failure to hide — it is the signal
that the next iteration must go back to the ask.
</evidence_state_and_move>

<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Work the procedure above in order, then write the revision:

1. Classify EVERY artifact of this round separately into `strands` — one entry per artifact,
   no merging, no omissions — judging from what it ACTUALLY produced: an executed number, not
   a projected, assumed or placeholder one. States: `genuine_positive`, `lead`, `null`,
   `broken`.
2. Read the round summary off the BEST strand and set `evidence_state`. It is derived, not
   judged: genuine_positive -> "strong_survivor", else lead -> "lead", else null ->
   "weak_or_null", else "experiment_broken". A summary that disagrees with your own strands
   is rejected.
3. Read the move off the summary. Set `move` and `move_rationale` (≤200 chars). The rule is
   not advisory:
   - "strong_survivor" -> LATCH: `deepen` or `extend` on THAT strand's object, title held.
     The null strands of this round are closed — one sentence in the paper, no more budget.
   - "lead" -> `deepen` on the lead. WEAK IS NOT NULL: make it bigger and cleaner (more
     power, a cleaner measure, the baseline it lost to attacked head-on) before abandoning
     it. Widen off a lead only if it was already deepened last round and came back null.
   - "weak_or_null" with an iteration remaining -> `widen`.
   - "experiment_broken" -> `fix`, once; a bet broken twice is dropped, not fixed again.
   - "declare" only on the final iteration or with no budget left.
4. If the move is `widen`, do the widen properly — go back to the user's ORIGINAL ask,
   enumerate a population of candidate answers, propose a cheap screen over all of them and a
   held-out confirmation for the survivor, and set `candidates_considered` to how many you
   actually weighed. The revised hypothesis is the best surviving candidate, or an explicit
   screening hypothesis naming the population and the selection rule. Every bet the next
   round makes must be a DIFFERENT answer to the ask — none of them refines the failed idea.
5. If the move is `fix`, keep the claim word-for-word and name the defect in `move_rationale`.
6. Set `coverage` and `coverage_statement` against the user's ORIGINAL ask, not against the
   hypothesis you are revising.
7. If reviewer feedback is provided, address the critiques directly. A reviewer asking you to
   shrink a claim is LEGITIMATE when your own strand classification agrees — the effect is a
   `lead` or a `null` — and is to be refused when a `genuine_positive` strand exists: you do
   not shrink a claim the evidence actually supports.

Write the revision as a hypothesis the next iteration can act on: `title`, `hypothesis`,
`key_changes`, and `confidence_delta` ("increased", "decreased" or "unchanged").

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — bookkeeping only, and NOT the steering decision (`move` is).
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the steering fields and the H↔H relation
fields) AND the full list of A↔A `artifact_relations` for this iteration's new artifacts.
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
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    },
    "StrandEvidence": {
      "description": "One artifact of the round, classified on its own.\n\nA STRAND is one bet. Rounds are mixed \u2014 a genuine positive beside three\nnulls is the normal shape \u2014 and the round-level classification this\nreplaced read that round as \"mostly null\", threw the positive away and\nwidened. So every artifact gets its own entry, and the round's scalar\n``evidence_state`` is derived from the best of them rather than judged\nseparately (see ``components/evidence_moves.py``).",
      "properties": {
        "artifact": {
          "description": "The artifact this strand is, named or id'd exactly as it appears in the artifact list you were given.",
          "title": "Artifact",
          "type": "string"
        },
        "state": {
          "description": "'genuine_positive' \u2014 an EXECUTED number (not projected), at a size the ORIGINAL ask would care about, which survived the obvious alternative explanation (baseline, confound, simpler account), and which a reader in the field could not have predicted and is not already published; 'lead' \u2014 real but not yet genuine: a small right-direction effect, a positive that lost to a baseline or missed a pre-registered bar by a margin, or a signal seen on one body of evidence only; 'null' \u2014 it ran and left nothing to build on; 'broken' \u2014 it never tested the claim (defect in code, data, measure, sample or setup, a run that did not finish, or numbers that were never executed).",
          "enum": [
            "genuine_positive",
            "lead",
            "null",
            "broken"
          ],
          "title": "State",
          "type": "string"
        },
        "why": {
          "description": "Why this state, in one short line (max 200 characters) \u2014 the number for a positive or a lead, the defect for a broken strand.",
          "maxLength": 200,
          "title": "Why",
          "type": "string"
        }
      },
      "required": [
        "artifact",
        "state",
        "why"
      ],
      "title": "StrandEvidence",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.\n\n``strands`` / ``evidence_state`` / ``move`` / ``coverage`` /\n``candidates_considered`` carry the between-iteration steering decision \u2014\nthe only one a run makes. ``strands`` is the classification the model\nactually performs (one entry per artifact); ``evidence_state`` is the\nROUND SUMMARY read off the best strand, and a validator below rejects the\npair when they disagree.\nAn audit of 19 finished runs found the narrow-salvage move taken ~20\ntimes after a weak or null result and the widen move taken zero times,\nwith nothing in the output recording which move had been made, so the\nbias was invisible in the run record as well as unconstrained in the\nprompt. These fields make the decision explicit and checkable;\n``relation_type`` is kept only so runs already on disk still parse.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "strands": {
      "description": "EVERY artifact of this iteration, classified separately \u2014 one entry per artifact, no merging and no omissions. A round that mixes one genuine positive with several nulls is the normal shape; classifying the round as a whole is how the positive gets thrown away with the nulls.",
      "items": {
        "$ref": "#/$defs/StrandEvidence"
      },
      "title": "Strands",
      "type": "array"
    },
    "evidence_state": {
      "description": "The ROUND SUMMARY, read off the BEST strand rather than judged separately: any 'genuine_positive' strand -> 'strong_survivor'; else any 'lead' strand -> 'lead'; else any 'null' strand -> 'weak_or_null'; else (every strand 'broken') -> 'experiment_broken'. A value that disagrees with `strands` is rejected.",
      "enum": [
        "strong_survivor",
        "lead",
        "weak_or_null",
        "experiment_broken"
      ],
      "title": "Evidence State",
      "type": "string"
    },
    "move": {
      "description": "The steering move for the NEXT iteration, read off evidence_state and the remaining budget: 'deepen' \u2014 hold the claim and go after the mechanism, the boundary or the confound (also the move that makes a 'lead' bigger and cleaner); 'extend' \u2014 same claim, new population/period/setting; 'widen' \u2014 return to the user's original ask and put a population of alternative candidate answers in play, screened cheaply and confirmed on held-out evidence; 'fix' \u2014 the claim is unchanged and the defective test is repaired; 'declare' \u2014 write the run up as a negative result, permitted ONLY on the final iteration or with no budget left.",
      "enum": [
        "deepen",
        "extend",
        "widen",
        "fix",
        "declare"
      ],
      "title": "Move",
      "type": "string"
    },
    "move_rationale": {
      "description": "Why this move follows from this evidence_state and the remaining budget (one short line, max 200 characters). For 'fix', name the defect.",
      "maxLength": 200,
      "title": "Move Rationale",
      "type": "string"
    },
    "coverage": {
      "description": "Does the revised hypothesis still answer the USER'S ORIGINAL ask? 'full' \u2014 it answers the ask; 'partial' \u2014 it answers a recognisable piece of it; 'lost' \u2014 the run has drifted onto a different question and the next iteration must go back.",
      "enum": [
        "full",
        "partial",
        "lost"
      ],
      "title": "Coverage",
      "type": "string"
    },
    "coverage_statement": {
      "description": "One sentence naming which part of the user's original ask the next iteration will answer.",
      "title": "Coverage Statement",
      "type": "string"
    },
    "candidates_considered": {
      "description": "How many alternative claims, mechanisms, measures or bodies of evidence you actually weighed during THIS revision. 1 when none were weighed \u2014 which, after a weak_or_null result with budget remaining, means the widen was not done.",
      "title": "Candidates Considered",
      "type": "integer"
    },
    "relation_type": {
      "default": "evolution",
      "description": "LEGACY, kept for backward compatibility with runs already on disk \u2014 'move' is the field that steers the run. Moulines's structuralist typology of this revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely.",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "evidence_state",
    "move",
    "move_rationale",
    "coverage",
    "coverage_statement",
    "candidates_considered"
  ],
  "title": "RevisedHypothesis",
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

### [3] TOOL CALL — Bash · 2026-09-28 21:01:03 UTC

```
Inspect workspace, report size, uploads:
ls -la . .aii 2>/dev/null; ls ../; wc -c ../current_report.md; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/user_uploads 2>/dev/null | head
```

### [4] TOOL RESULT — Bash · 2026-09-28 21:01:03 UTC

```
{"stdout": ".:\ntotal 1994\ndrwxr-xr-x 3 root root 1002725 Sep 28 21:00 .\ndrwxr-xr-x 3 root root 1009502 Sep 28 21:00 ..\ndrwxr-xr-x 2 root root       1 Sep 28 21:00 .aii\n-rw------- 1 root root      54 Sep 28 21:00 .aii_claude_session.json\n-rw-r--r-- 1 root root   27857 Sep 28 21:01 .repl_agent.ptylog\n\n.aii:\ntotal 980\ndrwxr-xr-x 2 root root       1 Sep 28 21:00 .\ndrwxr-xr-x 3 root root 1002725 Sep 28 21:00 ..\ncurrent_report.md\nupd_hypo\n69392 ../current_report.md", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [5] TOOL CALL — Bash · 2026-09-28 21:01:07 UTC

```
List report section headings:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2; grep -n "^#" upd_hypo/current_report.md | head -120
```

### [6] TOOL RESULT — Bash · 2026-09-28 21:01:07 UTC

```
{"stdout": "1:# Do temporal network signals predict how scientific concepts spread across disciplines?\n15:# Iteration 1\n17:## 1. Strategy\n25:## 2. Data infrastructure and deviations\n36:## 3. Experiment 1: Does the naturalisation gap predict cross field spread? [ARTIFACT:art_xp8BGBJZsxeI]\n38:### 3.1 Construction\n44:### 3.2 Measurement result: background homophily dominates lineage\n59:### 3.3 Predictive screen: A\\*_h does not survive\n72:### 3.4 Within field heterogeneity and reliability gradient\n94:### 3.5 Alternative lineage indicators\n117:### 3.6 Secondary outcomes\n121:### 3.7 Field level prediction\n125:### 3.8 Variance decomposition (REML)\n129:### 3.9 Audit\n137:## 4. Experiment 3: Do diverse topic ties predict concept spread? [ARTIFACT:art_yrradSC27HtQ]\n139:### 4.1 Construction\n147:### 4.2 Screen results\n159:### 4.3 Portability: which indicators associate with rarefied breadth across all groups?\n167:### 4.4 Exploratory partial association\n181:### 4.5 Secondary outcomes\n185:### 4.6 Audit\n191:## 5. Experiment 4: Where a concept lands early vs. how broadly it spreads [ARTIFACT:art_33_KKk_G8Gw5]\n193:### 5.1 Construction\n205:### 5.2 Concept level screen\n215:### 5.3 Secondary results: volume residualised breadth and uptake\n221:### 5.4 Field level prediction: gateway centrality of the adopting field\n239:### 5.5 Predicting the next field entered\n243:### 5.6 Sensitivity analyses\n249:## 5a. Failed artifacts\n261:## 6. Comparison across experiments\n263:### 6.1 Shared baseline strength\n269:### 6.2 The decisive table: no candidate passes\n281:### 6.3 What worked where\n293:## 7. Dead ends and negative results\n317:## 8. What iteration 1 learned\n337:## 8a. Coverage of the original request\n357:# Iteration 2\n359:## 9. Why this iteration ran\n381:## 10. Experiment 5: Does the adopting field's gateway centrality predict retention on holdout data? [ARTIFACT:art_wxWssKSUR45f]\n383:### 10.1 Data\n389:### 10.2 Panel\n405:### 10.3 Field retention hypothesis: result: DISCONFIRMED\n427:### 10.4 Why gateway vanished: the baseline ladder\n443:### 10.5 The relatedness pair beats gateway\n447:### 10.6 Concept breadth hypothesis: result: small but confirmed\n460:### 10.7 Minimum detectable effect and power\n464:### 10.8 Iteration-1 replication\n468:### 10.9 Deviations\n480:## 11. Experiment 6: Where new scientific concepts spread next [ARTIFACT:art_N-mpomDZZ1ln]\n482:### 11.1 Panel and grounding\n495:### 11.2 Next field entry hypothesis: CONFIRMED\n547:### 11.3 Ordering: first retained gateway precedes entropy takeoff\n558:### 11.4 Rescue and relay mechanisms: NOT SUPPORTED\n564:### 11.5 Trajectories: two stable classes\n582:### 11.6 Audit\n586:### 11.7 Deviations\n595:## 12. Evaluation 1: Does the gateway field retention signal replicate? [ARTIFACT:art_lwI2DuRtQRZX]\n597:### 12.1 Design\n601:### 12.2 Reproduction and headline\n615:### 12.3 Trait confound\n623:### 12.4 Placebos\n629:### 12.5 Sustained uptake artefact\n642:### 12.6 Power\n646:### 12.7 Shuffled R placebo on Experiment 4\n652:## 13. Dataset 2: When research concepts were officially recognised [ARTIFACT:art_O7Dq4L02QnDN]\n656:### 13.1 Sources\n669:### 13.2 Quality\n679:## 14. Research 1: How our results compare with related papers [ARTIFACT:art_dxvRpQufMR0e]\n695:## 15. Dead ends and negative results from iteration 2\n713:## 16. What we have learned so far\n746:## References", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [7] TOOL CALL — Bash · 2026-09-28 21:01:09 UTC

```
Read coverage table, Exp6 and conclusions sections:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2; sed -n 337,360p upd_hypo/current_report.md; sed -n 480,600p upd_hypo/current_report.md; sed -n 695,745p upd_hypo/current_report.md
```

### [8] TOOL RESULT — Bash · 2026-09-28 21:01:09 UTC

```
{"stdout": "## 8a. Coverage of the original request\n\n**[Addition, iteration 2.]** The table below maps each research question and execution step to its status after iteration 1.\n\n| Step | Status | Artifact |\n|---|---|---|\n| RQ1: candidate indicator screen (dev) | Done | art_xp8BGBJZsxeI, art_yrradSC27HtQ, art_33_KKk_G8Gw5 |\n| RQ1: holdout evaluation | Not started (dataset failed) | - |\n| RQ1: top-10 on holdout | Not started | - |\n| RQ1: external ground truth (O5) | Not started | - |\n| RQ1: exploratory AI first stage | Not started | - |\n| RQ2: diffusion trajectories | Not started | - |\n| RQ2: field entry conditional logit | Partial (dev, Exp 4) | art_33_KKk_G8Gw5 |\n| Grounding benchmark | Not started (dataset failed) | - |\n| Explain why strongest indicator works | Not started | - |\n| Case studies | Not started | - |\n| Optional learned model | Not started | - |\n\n\n\n# Iteration 2\n\n## 9. Why this iteration ran\n\n## 11. Experiment 6: Where new scientific concepts spread next [ARTIFACT:art_N-mpomDZZ1ln]\n\n### 11.1 Panel and grounding\n\nA separate full corpus scan produces 653 newborn concepts (legacy concept lexicon, tag AND title grounding; benchmark precision 0.996 from LLM and hand labels at $0.007). The panel is split into dev (CS/Eng/BGM/Med homes, onset 2003-2009; 279 concepts) and holdout (other fields plus the 2010-2014 cohort; 374 concepts), run once after a hashed freeze.\n\n| Split | Concepts | Episodes |\n|---|---|---|\n| Dev (CS/Eng/BGM/Med, t0 2003-09) | 279 | 707 |\n| Holdout field groups | 126 | 390 |\n| Holdout cohort (2010-14) | 248 | 768 |\n| **Total** | **653** | **1,865** |\n\nThe episode count (1,865) falls short of the 4,000 target. MathDec is untestable (too few concepts). The sense filter proved uninformative (test AUC 0.24); grounding relies entirely on the tag AND title rule.\n\n### 11.2 Next field entry hypothesis: CONFIRMED\n\nA conditional logit on concept year risk sets tests whether relatedness to the nonhome fields that currently retain the concept predicts which field a concept enters next, beyond field size, Hidalgo relatedness density, relatedness to home and the target field's own gateway centrality.\n\n**Dev results (274 concepts, 887 entry events):**\n\n| Model | Log likelihood | Converged |\n|---|---|---|\n| M0 (size, density, phi_home, gate_own) | -2,170.9 | Yes |\n| M1 (M0 + ret_rel plain) | -2,153.6 | Yes |\n| M2 (M0 + ret_gate weighted) | -2,151.6 | Yes |\n| M3 (M0 + ret_rel + ret_gate) | -2,151.3 | Yes |\n\nthe gateway weighted model vs the baseline: LR = 38.6 (p = 5.1 x 10^-10). The standardised coefficient d for gateway weighted retaining relatedness is 0.250 (bootstrap 95% CI [0.182, 0.321]). Label permutation p = 0.009; rewired backbone p = 0.030.\n\nWithin stratum AUCs on dev:\n\n| Predictor | AUC |\n|---|---|\n| M0 (full baseline) | 0.801 |\n| M2 (+ ret_gate) | 0.805 |\n| Log field size alone | 0.708 |\n| Relatedness density alone | 0.606 |\n| Retaining field gateway relatedness alone | 0.561 |\n\n**Holdout results (369 concepts, 1,373 entry events):**\n\nthe gateway weighted model vs the baseline: LR = 71.7 (p = 2.5 x 10^-17). d = 0.30 (bootstrap 95% CI [0.24, 0.37]).\n\n| Decision criterion | Value | Passes? |\n|---|---|---|\n| LR p < 0.01 | 2.5 x 10^-17 | Yes |\n| d > 0 and CI > 0 | 0.30 [0.24, 0.37] | Yes |\n| Positive in >= 3 of 3 evaluable field groups | Physical +0.33, LifeEnv +0.18, Social +0.24 | Yes |\n| Cohort positive | +0.29 [0.22, 0.36] | Yes |\n| Label permutation p < 0.05 | 0.001 | Yes |\n| Rewired backbone gain above null 95th pct | Yes (p = 0.015) | Yes |\n\nDerSimonian-Laird pooled d: 0.28 (95% CI [0.22, 0.35], I squared = 0, Q = 0.75).\n\n**Verdict: CONFIRMED** by the frozen rule. But the gateway weighting adds nothing beyond plain retaining relatedness (the combined model vs the plain relatedness model, gateway only permutation p = 0.17 holdout, 0.31 dev), and target field size is the strongest single block (AUC 0.76 vs density 0.59). The incremental AUC from baseline to the gateway weighted model is only 0.809 to 0.817.\n\nHoldout per group details:\n\n| Group | N concepts | N events | d | Boot 95% CI | LR | LR p |\n|---|---|---|---|---|---|---|\n| Physical | 30 | 92 | 0.332 | [0.046, 0.565] | 3.91 | 0.048 |\n| Life & Environment | 34 | 118 | 0.178 | [-0.096, 0.506] | 1.47 | 0.226 |\n| Social | 53 | 161 | 0.245 | [-0.008, 0.459] | 3.15 | 0.076 |\n| MathDec | 0 | - | - | too few | - | - |\n| Cohort | 248 | 989 | 0.292 | [0.222, 0.361] | 54.0 | 2.0 x 10^-13 |\n\n### 11.3 Ordering: first retained gateway precedes entropy takeoff\n\nAmong 175 concepts in the top rarefied breadth tercile, 112 (64%) have a detected entropy change point. Of those with an evaluable ordering:\n\n| Condition | N evaluable | Share \"before\" (excl. ties) | Sign test p (one sided) |\n|---|---|---|---|\n| First retained gateway field | 102 | 65.5% | 0.003 |\n| First retained peripheral field | 106 | 57.0% | 0.118 |\n\nMcNemar test comparing gateway vs peripheral: p = 0.088 (27 gateway only, 15 peripheral only). The ordering result is confirmed by the preregistered rule (>= 60% and sign p < 0.01), but the lead lag gateway permutation placebo gives p = 0.63, meaning the panel does not single out gateway fields as the unique driver. The lead lag panel regressions with concept fixed effects show that both retained gateway and retained peripheral fields are associated with subsequent entropy change, but the reverse (entropy predicting retention) is not significant (p = 0.22).\n\n### 11.4 Rescue and relay mechanisms: NOT SUPPORTED\n\nThe metapopulation rescue hypothesis (retained gateway fields keep a concept alive through reimportation from neighbouring fields) is not supported on holdout data. The interaction between retention and gateway tercile on background adjusted citation provenance is -0.217 (95% CI [-1.12, 0.68]). The mediation indirect effect is 0.002 (95% CI [-0.007, 0.010]).\n\nThe relay hypothesis (retained gateway fields radiate the concept onward) is also not supported. The fixed effects Poisson coefficient for the retention by gateway interaction on excess onward entries is -1.30 (95% CI [-4.93, 2.33]). The mean excess entries from gateway retained fields is -0.011.\n\n### 11.5 Trajectories: two stable classes\n\nDTW k-medoids with k = 2 is stable (bootstrap ARI 1.0). The two classes are \"integrating\" (128 concepts) and \"localised\" (60 concepts), matched on initial volume. The holdout independent recluster gives ARI 0.54.\n\n| Feature (year 9) | Integrating (cluster 0) | Localised (cluster 1) |\n|---|---|---|\n| Fields entered (nonhome) | 9.1 | 5.0 |\n| Fields retaining | 6.7 | 2.9 |\n| Fields lost | 0.5 | 0.6 |\n| Rarefied breadth (O2r, m = 30) | 5.2 | 2.8 |\n| Shannon entropy | 1.31 | 0.42 |\n| Gateway share | 0.17 | 0.04 |\n| Log volume | 5.4 | 4.8 |\n\nThe localised class is dominated by Medicine home concepts (42 of 60 localised vs 14 of 128 integrating from Medicine). Intersection born concepts (at least 2 home fields): 9 in the integrating class, none in the localised class.\n\n[FIGURE:fig_trajectories]\n\n### 11.6 Audit\n\nThe independent audit reproduces the retaining relatedness coefficient, the gateway permutation p and holdout AUCs exactly. An exact likelihood conditional logit gives LR 77.3 and DerSimonian-Laird pooled d 0.32 [0.25, 0.39] (the Breslow partial likelihood pipeline is conservative). Within stratum shuffled labels reject 0 of 20 times. A random year ordering placebo gives 0.43 (vs the real 0.66), confirming that the ordering is not an artefact of temporal structure.\n\n### 11.7 Deviations\n\n- 1,865 episodes, below the 4,000 target.\n- MathDec untestable (0 holdout field group concepts in iteration 2's frame).\n- Sense filter uninformative (test AUC 0.24); grounding relies on tag AND title.\n- No Wikidata aliases (rate limited; lexicon uses display names and plural variants only).\n\n\n\n## 12. Evaluation 1: Does the gateway field retention signal replicate? [ARTIFACT:art_lwI2DuRtQRZX]\n\n### 12.1 Design\n\nThis zero API stress test reevaluates iteration 1's only live lead: gateway centrality adding +0.103 AUC for field retention on 80 episodes. The evaluation harmonises the three iteration-1 experiments onto a common covariate set (the five feature baseline + log field size + relatedness to home + relatedness density) and tests gateway on each experiment's panel, their deduplicated union (362 episodes, 54 concepts) and a new episodes only subset (282 episodes). All CIs are concept clustered refit bootstrap (2,000 draws, percentile).\n\n## 15. Dead ends and negative results from iteration 2\n\n1. **the field retention hypothesis (field level gateway retention): DISCONFIRMED.** On 27,393 episodes from 12,499 concepts, gateway centrality adds delta AUC -0.00001 (95% CI [-0.0006, +0.0003]) over the full covariate set. The signal is absorbed by the field's retention propensity and reverses sign on holdout data. Gateway alone has AUC 0.506 on holdout (0.41 in Social Sciences).\n\n2. **Rescue mechanism: NOT SUPPORTED.** The interaction between retention and gateway tercile on background adjusted citation provenance is null (coefficient -0.22, CI including zero).\n\n3. **Relay mechanism: NOT SUPPORTED.** Retained gateway fields do not radiate more onward entries than peripheral fields (coefficient -1.30, CI including zero).\n\n4. **Gateway weighting in the entry hypothesis.** The gateway weighting of retaining relatedness adds nothing beyond plain retaining relatedness (the combined model vs the plain relatedness model: gateway only permutation p = 0.17 holdout).\n\n5. **Iteration-1 gateway lead on 80 episodes.** Cannot be certified as above chance: the shuffled R placebo's 95th percentile (0.130) exceeds the observed +0.103.\n\n6. **Sustained uptake gains of all gateway variants.** All are label coverage artefacts.\n\n7. **Node label permutation test.** The union panel's real delta sits at the 54th percentile of the null, indistinguishable from random field labelling.\n\n\n\n## 16. What we have learned so far\n\nTwo iterations and eight artifacts have tested whether temporal network signals predict how new scientific concepts spread across disciplines, using OpenAlex data on 12,499 to 65,026 concepts with up to 27,393 concept by field adoption episodes.\n\n**Confirmed findings:**\n\n1. **Retaining relatedness predicts the next field entered (the entry hypothesis, confirmed on holdout data).** A conditional logit on concept year risk sets shows that relatedness to the fields currently retaining a concept predicts which field the concept enters next, beyond field size, Hidalgo relatedness density, relatedness to home and the target field's own gateway centrality. Holdout likelihood ratio 71.7 (p = 2.5 x 10^-17), standardised d = 0.30 (95% CI [0.24, 0.37]), positive in all three evaluable holdout field groups and the 2010-2014 cohort, DerSimonian-Laird pooled d = 0.28 (95% CI [0.22, 0.35], I squared = 0). The label permutation null and the rewired backbone placebo are both rejected.\n\n2. **Two stable trajectory classes (research question 2 (trajectories)).** DTW k-medoids separates 188 concepts with sustained uptake into \"integrating\" (128 concepts, mean 6.7 fields retaining by year 9, O2r 5.2) and \"localised\" (60 concepts, mean 2.9 fields retaining, O2r 2.8). The localised class is dominated by Medicine home concepts. Holdout independent recluster ARI = 0.54.\n\n3. **Ordering: first retained gateway field precedes entropy takeoff.** In 66% of broad concepts, the first retained gateway field precedes the calibrated entropy takeoff (sign p = 0.003). The lead lag gateway permutation placebo (p = 0.63) says the panel does not single out gateway fields specifically; retained peripheral fields also precede entropy takeoff in 57% of cases.\n\n4. **Background homophily dominates raw lineage (the background homophily measurement).** Two thirds of between concept variance in raw lineage log odds is general disciplinary homophily. This is confirmed across 48 dev concepts and is a methodological finding for any study using citation based cross field indices.\n\n5. **Concept level gateway landing predicts volume residualised breadth (the breadth hypothesis, small effect, confirmed).** Holdout partial rho of G_btw with volume residualised breadth = 0.046 (Holm p = 0.0045); DerSimonian-Laird pooled G = 0.068 (95% CI [0.029, 0.107]). The effect is real but small.\n\n**Disconfirmed:**\n\n1. **Gateway centrality does not predict field retention (the field retention hypothesis).** On holdout data, delta AUC is -0.00001. The iteration-1 lead (+0.103 on 80 episodes) was a small sample artefact absorbed by the field's retention propensity.\n\n2. **Rescue and relay mechanisms are not supported.** Neither the reimportation nor the onward radiation mechanism of the metapopulation analogy is detectable in the data.\n\n3. **No concept level network indicator beats the simple baseline.** All three theory driven indicators (naturalisation gap, structural diversity, gateway landing) fail the preregistered decision rule for predicting raw rarefied breadth. Power analysis shows that with baseline rho = 0.77 to 0.83, a feature needs Spearman approximately 0.95 with breadth to gain 0.10.\n\n**Open:**\n\n- The indicator screen's full indicator by outcome by field matrix has not been computed on the new common panel. The Experiment 3 cooccurrence indicators and the Experiment 1 lineage indicators have not been rescored on the iteration-2 frame.\n- External recognition has been compiled but not used as an outcome.\n- The learned model (optional extension) has not been attempted.\n- Candidate S (unconnected coauthor groups) remains untested.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-28 21:01:45 UTC

```
Inspect Exp6 held-out results structure:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art; ls gen_art_experiment_6/results | head -50; python3 - <<'E'
import json
d=json.load(open('gen_art_experiment_6/results/heldout_result.json'))
def show(x,depth=0,maxd=2):
    if isinstance(x,dict):
        for k,v in x.items():
            if isinstance(v,(dict,list)) and depth<maxd:
                print('  '*depth+str(k)); show(v,depth+1,maxd)
            else:
                s=json.dumps(v); print('  '*depth+f"{k}: {s[:160]}")
    elif isinstance(x,list):
        print('  '*depth+f"[list len {len(x)}] "+json.dumps(x[:2])[:200])
show(d)
E
```

### [10] TOOL RESULT — Bash · 2026-09-28 21:01:47 UTC

```
{"stdout": "agreement.json\napi_audit.csv\napi_audit.json\naudit.json\naudit_placebo.json\ncandidates.csv\ncandidates_summary.json\ncluster_assign_dev.csv\ncluster_assign_heldout.csv\ncredits_log.csv\ndev_result.json\ndev_spec_parts.json\ndeviations.json\nentry_risk_sets_dev.parquet\nentry_risk_sets_heldout.parquet\nepisodes.csv\nframe_concepts.csv\nframe_summary.json\nfreeze_log.txt\nfrozen_spec.json\ngrounding_concepts.csv\ngrounding_report.json\nheldout_result.json\nlexicon.parquet\nlexicon_dropped.csv\nlexicon_hash.txt\nlexicon_summary.json\nopenrouter_cost.json\nordering_dev.csv\nordering_heldout.csv\np0_dropped.csv\nrelay_dev.csv\nrelay_heldout.csv\nrescue_dev.csv\nrescue_heldout.csv\nsense_filter.pkl\ntrajectories_dev.csv\ntrajectories_heldout.csv\nunit_tests_T0.json\nworks_schema.json\nn_heldout_concepts: 374\nby_group\n  Cohort: 248\n  Social: 54\n  Physical: 34\n  LifeEnv: 34\n  OtherHealth: 4\nH2_pooled\n  n_rows: 46433\n  n_strata: 2339\n  n_concepts: 369\n  n_events: 1373\n  entry_rate: 0.02956948721814227\n  models\n    M0: {\"coef\": {\"a_phi_home\": 0.33064441529782246, \"b_log_size\": 1.584569503949015, \"c_density\": 0.36227353934450424, \"e_gate_own\": 0.09944954700323524}, \"se\": {\"a_ph\n    M1: {\"coef\": {\"a_phi_home\": 0.37188553304728283, \"b_log_size\": 1.6738276315064888, \"c_density\": 0.23852929616788293, \"e_gate_own\": 0.05164125007538622, \"d0_ret_rel\"\n    M2: {\"coef\": {\"a_phi_home\": 0.36478607003405844, \"b_log_size\": 1.6795135455218, \"c_density\": 0.24721762419454624, \"e_gate_own\": 0.019351762291929017, \"d_ret_gate\": \n    M3: {\"coef\": {\"a_phi_home\": 0.36936674458570773, \"b_log_size\": 1.6818176588931806, \"c_density\": 0.2380779743085792, \"e_gate_own\": 0.028999552223334616, \"d0_ret_rel\"\n    M2lost: {\"coef\": {\"a_phi_home\": 0.32791908447413465, \"b_log_size\": 1.5834072596401476, \"c_density\": 0.36914417297567764, \"e_gate_own\": 0.10317255712560171, \"d_lost_gate\n  LR\n    M2_vs_M0: {\"LR\": 71.71641463905598, \"df\": 1, \"p\": 2.4845706606291646e-17}\n    M1_vs_M0: {\"LR\": 68.56864172514634, \"df\": 1, \"p\": 1.2253722672182456e-16}\n    M3_vs_M1: {\"LR\": 5.359129220855721, \"df\": 1, \"p\": 0.02061406421285374}\n    M2lost_vs_M0: {\"LR\": 3.692783297256028, \"df\": 1, \"p\": 0.05464835230436948}\n  auc_within_stratum\n    M0: {\"mean\": 0.8091807114429179, \"ci\": [0.7984492331954763, 0.8199446379498353], \"n_strata\": 961}\n    M1: {\"mean\": 0.8168958319192421, \"ci\": [0.8057138021898398, 0.8279266011380061], \"n_strata\": 961}\n    M2: {\"mean\": 0.8165524635722822, \"ci\": [0.8053034495990403, 0.8271277315385243], \"n_strata\": 961}\n    M3: {\"mean\": 0.8171354241891543, \"ci\": [0.8065784780635473, 0.8281377372847883], \"n_strata\": 961}\n    M2lost: {\"mean\": 0.810261363396254, \"ci\": [0.7991874850291205, 0.8208290627453392], \"n_strata\": 961}\n    a_phi_home: {\"mean\": 0.5727290857204159, \"ci\": [0.5578387354462705, 0.5876780151717319]}\n    b_log_size: {\"mean\": 0.7571468245335505, \"ci\": [0.7432796973034494, 0.7704361272290426]}\n    c_density: {\"mean\": 0.5899142713082878, \"ci\": [0.5732591975021303, 0.6066060690864565]}\n    e_gate_own: {\"mean\": 0.45019316994915887, \"ci\": [0.4311663719925003, 0.46976280708685747]}\n    d0_ret_rel: {\"mean\": 0.549637962338796, \"ci\": [0.5340511145365596, 0.5652085594964081]}\n    d_ret_gate: {\"mean\": 0.5473633955058406, \"ci\": [0.5306560075632085, 0.5648480644241015]}\n    d_lost_gate: {\"mean\": 0.49472626329764474, \"ci\": [0.48894987381107574, 0.5007125379232532]}\n  boot_d\n    ci: [0.2396221224886921, 0.3687710454858924]\n    se_boot: 0.033015692804543896\n    n_boot: 2000\n    lr_boot: [48.022073443692626, 61.10967415431014, 72.08327110710115, 83.74084928574189, 100.49796369752603]\n  perm_null\n    n: 1000\n    lr_obs: 71.71641463905598\n    p: 0.000999000999000999\n    null_q: [2.298605642513394, 12.855549758748566, 18.16931363961462, 29.754805871363185]\n    null_mean: 4.780875612062727\n  gonly_perm_null_M3_vs_M1\n    n: 1000\n    lr_obs: 5.359129220855721\n    p: 0.17282717282717283\n    null_q: [1.2834225929473178, 7.377585618265675, 10.204503817493737, 16.23445376452073]\n  rewired_null\n    n: 200\n    lr_obs: 71.71641463905598\n    p: 0.014925373134328358\n    null_q95: 25.35432959295398\n    null_median: 2.9273494794483668\n    real_gain_le_null95: false\nfrozen_dev_coef_auc\n  M0\n    mean: 0.8070954731216242\n    ci: [0.7961158126587261, 0.8183723881714523]\n  M2\n    mean: 0.8151394525018186\n    ci: [0.8041990479187258, 0.826213950278546]\nH2_per_group\n  Physical\n    n_concepts: 30\n    n_events: 92\n    d: 0.33190390712722606\n    se: 0.16500811770727022\n    boot_ci: [0.04639854869882769, 0.5654476789600625]\n    LR: {\"LR\": 3.9093621019801503, \"df\": 1, \"p\": 0.04801782006983559}\n  LifeEnv\n    n_concepts: 34\n    n_events: 118\n    d: 0.1782552843878218\n    se: 0.14439994076117874\n    boot_ci: [-0.09589076212245926, 0.5057704115526264]\n    LR: {\"LR\": 1.4650246938848568, \"df\": 1, \"p\": 0.22613232849927772}\n  Social\n    n_concepts: 53\n    n_events: 161\n    d: 0.24451473387184078\n    se: 0.13045899284853288\n    boot_ci: [-0.008413244223572947, 0.45936866022886264]\n    LR: {\"LR\": 3.1544382682966443, \"df\": 1, \"p\": 0.07572074814889966}\n  MathDec\n    n_concepts: 0\n    status: \"too few concepts\"\n  Cohort\n    n_concepts: 248\n    n_events: 989\n    d: 0.2916284471668024\n    se: 0.03815489939611666\n    boot_ci: [0.2220069453650332, 0.36072498977180345]\n    LR: {\"LR\": 54.011853239082484, \"df\": 1, \"p\": 1.9928376965975005e-13}\n  OtherHealth\n    n_concepts: 4\n    status: \"too few concepts\"\nH2_DL_pooled\n  k: 4\n  b: 0.2835280026617289\n  se: 0.03470316750295396\n  ci\n    [list len 2] [0.21550979435593914, 0.35154621096751865]\n  p: 3.081594151322099e-16\n  tau2: 0.0\n  Q: 0.7519451573302255\n  I2: 0.0\nH2_sign_count\n  positive: 4\n  of: 4\n  sign_test_p: 0.0625\nrescue_relay\n  n_episodes_rescue: 1158\n  n_with_crefs: 842\n  self_lineage_share_of_crefs: 0.10519544642174146\n  R1_resc\n    n: 798\n    n_clusters: 299\n    coef: {\"R_cj\": {\"b\": 0.38852569364632084, \"se\": 0.39023897328474455, \"ci\": [-0.37944763291803074, 1.1564990202106724], \"p\": 0.3202475697554218}, \"top\": {\"b\": 0.019091\n  R1_s_other\n    n: 771\n    n_clusters: 293\n    coef: {\"R_cj\": {\"b\": 0.06712360174423884, \"se\": 0.0740060976389703, \"ci\": [-0.07852938326826248, 0.21277658675674016], \"p\": 0.3651541575300767}, \"top\": {\"b\": 0.165516\n  R2_base\n    n: 796\n    n_clusters: 299\n    coef: {\"gateway_j_z\": {\"b\": 0.0035048673272817183, \"se\": 0.012249919915773514, \"ci\": [-0.02060244227502974, 0.027612176929593175], \"p\": 0.774989994377331}, \"log_size_\n  R2_full\n    n: 796\n    n_clusters: 299\n    coef: {\"gateway_j_z\": {\"b\": 0.0010352073546354614, \"se\": 0.013104471352531928, \"ci\": [-0.024753822307780927, 0.026824237017051847], \"p\": 0.9370884273384971}, \"log_siz\n  R2_mediation\n    indirect: 0.002469659972646257\n    ci: [-0.006968969233683165, 0.009824928788321549]\n    share_mediated: 0.7046372207651179\n    n: 796\n    n_concepts: 299\n  H1_replication_all_episodes\n    n: 1153\n    n_clusters: 352\n    coef: {\"gateway_j_z\": {\"b\": 0.005335865553599093, \"se\": 0.01402195491154914, \"ci\": [-0.022241752024498306, 0.032913483131696494], \"p\": 0.7037774005826948}, \"log_size_\n  R3_incidence\n    top: [{\"S_bin\": 0, \"mean\": 0.8783783783783784, \"size\": 74}, {\"S_bin\": 1, \"mean\": 0.875, \"size\": 24}, {\"S_bin\": 2, \"mean\": 0.8875, \"size\": 80}, {\"S_bin\": 3, \"mean\": 0\n    mid: [{\"S_bin\": 0, \"mean\": 0.819672131147541, \"size\": 61}, {\"S_bin\": 1, \"mean\": 0.7368421052631579, \"size\": 57}, {\"S_bin\": 2, \"mean\": 0.8372093023255814, \"size\": 43}\n    bottom: [{\"S_bin\": 0, \"mean\": 0.7319587628865979, \"size\": 97}, {\"S_bin\": 1, \"mean\": 0.7933333333333333, \"size\": 150}, {\"S_bin\": 2, \"mean\": 0.8256880733944955, \"size\": 1\n  relay_n_episodes: 1047\n  relay_fepois\n    n: 603\n    n_clusters: 158\n    coef: {\"R_cj\": {\"b\": 1.3705620877502105, \"se\": 0.5873899744219215, \"ci\": [0.21927773788324423, 2.5218464376171768], \"p\": 0.019631953611490813}, \"gateway_j\": {\"b\": 2.3\n  relay_fepois_offset\n    n: 603\n    n_clusters: 158\n    coef: {\"R_cj\": {\"b\": 1.3815906986711366, \"se\": 0.6409897236774432, \"ci\": [0.12525084026334787, 2.637930557078925], \"p\": 0.031130369719795752}, \"gateway_j\": {\"b\": 2.75\n  relay_excess_ols\n    n: 1047\n    n_clusters: 331\n    coef: {\"R_cj\": {\"b\": 0.03911132970160812, \"se\": 0.10531233645264693, \"ci\": [-0.1680568527564908, 0.246279512159707], \"p\": 0.710589774034475}, \"top\": {\"b\": 0.128994332\n  relay_excess_gateway_retained\n    mean: -0.010675926846191609\n    n: 311\n    ci: [-0.11093317578891297, 0.09376289940586639]\n  relay_excess_by_cell\n    [list len 6] [{\"R_cj\": 0.0, \"gate_ter\": 0, \"mean\": -0.3467663164433726, \"size\": 82}, {\"R_cj\": 0.0, \"gate_ter\": 1, \"mean\": -0.1699127784089312, \"size\": 42}]\ntrajectories\n  n_concepts_clustered: 188\n  n_intersection_born_O1: 9\n  heldout_independent_recluster_ARI: 0.5361258296737231\n  cluster_sizes\n    [list len 2] [128, 60]\n  cluster_mean_series\n    0: {\"n_entered_offhome\": [2.625, 3.609, 4.594, 5.516, 6.336, 7.25, 7.938, 8.523, 9.062], \"n_retaining\": [1.016, 1.445, 2.367, 3.195, 4.125, 4.82, 5.555, 6.32, 6.65\n    1: {\"n_entered_offhome\": [0.817, 1.467, 2.05, 2.683, 3.317, 3.667, 4.083, 4.533, 4.967], \"n_retaining\": [0.117, 0.25, 0.633, 1.167, 1.667, 2.167, 2.533, 2.683, 2.8\n  cluster_by_group\n    0: {\"DEV_BGM\": 9, \"DEV_CS\": 9, \"DEV_Eng\": 20, \"DEV_Med\": 14, \"LifeEnv\": 26, \"OtherHealth\": 4, \"Physical\": 21, \"Social\": 25}\n    1: {\"DEV_BGM\": 0, \"DEV_CS\": 0, \"DEV_Eng\": 5, \"DEV_Med\": 42, \"LifeEnv\": 4, \"OtherHealth\": 0, \"Physical\": 4, \"Social\": 5}\n  cluster_outcomes\n    O2r_m30: {\"0\": 5.214, \"1\": 2.772}\n    O3: {\"0\": 0.0, \"1\": 0.0}\n  hmm\n    n_states: 6\n    note: \"refit with the frozen number of states\"\n  hmm_vs_dtw_ARI: 0.09450482650930404\n  hmm_top_paths\n    4-1: 28\n    0-5: 22\n    4-0: 20\n    0: 16\n    0-3-0: 14\n    4: 13\n    0-3: 12\n    4-2: 10\nordering\n  n_top_o2r: 175\n  n_tau_detected: 112\n  share_tau_detected: 0.64\n  gateway\n    n_evaluable: 102\n    before: 57\n    ties: 15\n    after: 30\n    share_before_excl_ties: 0.6551724137931034\n    sign_test_p_one_sided: 0.002506799450073193\n  peripheral\n    n_evaluable: 106\n    before: 49\n    ties: 20\n    after: 37\n    share_before_excl_ties: 0.5697674418604651\n    sign_test_p_one_sided: 0.1176899311055276\n  mcnemar\n    n: 96\n    gw_only: 27\n    per_only: 15\n    p_exact_two_sided: 0.08842954698775429\n  lead_lag\n    forward_dH_on_ret: {\"n\": 2992, \"n_clusters\": 374, \"coef\": {\"ret_gw\": {\"b\": -0.027939583860173887, \"se\": 0.008204208218249505, \"ci\": [-0.04407188190382086, -0.01180728581652692], \"\n    reverse_dret_on_H: {\"n\": 2992, \"n_clusters\": 374, \"coef\": {\"H\": {\"b\": 0.07673151369679986, \"se\": 0.06208029407404087, \"ci\": [-0.04533971852911299, 0.1988027459227127], \"p\": 0.2172\n    event_study_H: {\"n\": 3366, \"n_clusters\": 374, \"coef\": {\"ev-3\": {\"b\": -0.07165074712879511, \"se\": 0.019136067623735615, \"ci\": [-0.10927884457307889, -0.03402264968451134], \"p\":\n    n_treated: 296\n    n_concepts: 374\n  lead_lag_placebo\n    n: 200\n    obs: -0.027939583860173887\n    null_q: [-0.05375937043065577, -0.031892037361457834, -0.0084208680648549]\n    p_two_sided: 0.6268656716417911\ndecisions\n  H2_entry\n    LR_p<0.01: true\n    d>0_CI>0: true\n    field_groups_positive>=3_of_3: true\n    cohort_positive: true\n    perm_p<0.05: true\n    rewired_gain_above_null95: true\n    CONFIRMED: true\n  H2_ordering\n    p_gw: 0.6551724137931034\n    sign_p: 0.002506799450073193\n    peripheral_share: 0.5697674418604651\n    CONFIRMED: true\n  RESCUE\n    R1_interaction: -0.21735315531009167\n    R1_ci: [-1.1162120533726436, 0.6815057427524602]\n    indirect: 0.002469659972646257\n    indirect_ci: [-0.006968969233683165, 0.009824928788321549]\n    SUPPORTED: false\n  RELAY\n    fepois_ret_x_gate: -1.299228378652143\n    ci: [-4.927263091478967, 2.32880633417468]\n    mean_excess_gw_retained: -0.010675926846191609\n    SUPPORTED: false", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-28 21:01:51 UTC

```
Check H2 definitions and M1/M2lost coefficients:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art; python3 - <<'E'
import json
d=json.load(open('gen_art_experiment_6/results/heldout_result.json'))
for m in ['M1','M2lost']:
    print(m, json.dumps(d['H2_pooled']['models'][m])[:900])
f=json.load(open('gen_art_experiment_6/results/frozen_spec.json'))
print(json.dumps(f)[:3000])
E
grep -n -i "retain\|entered(t-1)\|ret_rel\|lost" gen_art_experiment_6/method.py | head -60
```

### [12] TOOL RESULT — Bash · 2026-09-28 21:01:51 UTC

```
{"stdout": "M1 {\"coef\": {\"a_phi_home\": 0.37188553304728283, \"b_log_size\": 1.6738276315064888, \"c_density\": 0.23852929616788293, \"e_gate_own\": 0.05164125007538622, \"d0_ret_rel\": 0.2809043442272664}, \"se\": {\"a_phi_home\": 0.027921572124598486, \"b_log_size\": 0.05288720649766899, \"c_density\": 0.034421918211009254, \"e_gate_own\": 0.0315219540144637, \"d0_ret_rel\": 0.032159975704963886}, \"ll\": -3235.809018933568, \"n_strata\": 961, \"n_events\": 1373, \"n_rows\": 18846, \"converged\": true}\nM2lost {\"coef\": {\"a_phi_home\": 0.32791908447413465, \"b_log_size\": 1.5834072596401476, \"c_density\": 0.36914417297567764, \"e_gate_own\": 0.10317255712560171, \"d_lost_gate\": -0.06322615097883642}, \"se\": {\"a_phi_home\": 0.027397318970110676, \"b_log_size\": 0.051120809259672675, \"c_density\": 0.030304621819881934, \"e_gate_own\": 0.030554888439417182, \"d_lost_gate\": 0.034737288878067214}, \"ll\": -3268.246948147513, \"n_strata\": 961, \"n_events\": 1373, \"n_rows\": 18846, \"converged\": true}\n{\"created\": \"2026-09-28T18:32:24.227628+00:00\", \"regressors\": {\"a_phi_home\": \"mean_h phi[h,k] over home fields\", \"b_log_size\": \"log venue-field works in k at t-1\", \"c_density\": \"Hidalgo density sum_{j in entered(t-1)} phi[j,k] / sum_j phi[j,k]\", \"e_gate_own\": \"gateway_eig of k\", \"d0_ret_rel\": \"mean_{j in Ret(t-1)} phi[j,k]\", \"d_ret_gate\": \"sum_{j in Ret(t-1)} g_j phi[j,k] / sum_{j in Ret} g_j\", \"d_lost_gate\": \"same over LOST fields (placebo)\"}, \"models\": {\"M0\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\"], \"M1\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\"], \"M2\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d_ret_gate\"], \"M3\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\"], \"M2lost\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d_lost_gate\"]}, \"primary_sample\": \"strata (concept, t) with non-empty retaining set; t = t0+1..t0+8\", \"standardisation\": {\"a_phi_home\": {\"mean\": 0.16202608575019556, \"sd\": 0.30285707738892603}, \"b_log_size\": {\"mean\": 9.731619276958401, \"sd\": 2.284239494682293}, \"c_density\": {\"mean\": 0.17244520298540197, \"sd\": 0.21075858352121596}, \"e_gate_own\": {\"mean\": 0.32849098315017977, \"sd\": 0.28592622199912354}, \"d0_ret_rel\": {\"mean\": 0.12733956053079426, \"sd\": 0.24445162515471244}, \"d_ret_gate\": {\"mean\": 0.15253833778314638, \"sd\": 0.30125319183313704}, \"d_lost_gate\": {\"mean\": 0.02216697846204525, \"sd\": 0.14547123546523702}}, \"gate_terciles\": [0.1520343866310761, 0.29798365664086207], \"o2r_resid_coef_dev\": [-0.03808207780883798, 3.891852441738708], \"o2r_top_tercile_cut_resid\": 0.4175760916556232, \"changepoint_pen\": 4.5, \"zspec\": {\"n_entered_offhome\": [4.013888888888889, 2.728327088811533], \"n_retaining\": [2.4739583333333335, 2.11469944339186], \"n_lost\": [0.1701388888888889, 0.43184768385214284], \"R20\": [3.0763716485002344, 1.2147270567565587], \"H\": [0.715027691192768, 0.435926568104874], \"G_share\": [0.07476598956623554, 0.08414117835153488], \"log_volume\": [4.4739204732977225, 0.9011972763296602]}, \"k\": 2, \"medoid_cidx\": [94, 41020], \"medoid_series\": [[[-0.7381405613526144, -0.6970060629368618, -0.3939789311157716, 0.8922569181864014, 0.8342324184555338, 0.11997874156459405, -1.0192800576910452], [-0.7381405613526144, -0.6970060629368618, -0.3939789311157716, 0.279683255470807, 0.5365876453930144, 0.04505957795465281, -0.5381024105049081], [-0.7381405613526144, -0.22412562447793088, -0.3939789311157716, 0.35078043043446056, 0.7031802150835025, 0.05006804153532872, -0.1884774672037731], [-0.7381405613526144, -0.22412562447793088, -0.3939789311157716, 0.08435046819318669, 0.6461946466452956, 0.1667237151886523, 0.21029648645433552], [-0.37161559295683355, -0.22412562447793088, -0.3939789311157716, 0.05125464661140303, 0.6033113289464309, 0.21516096712201177, 0.30072400592386056], [0.3614343438347282, -0.22412562447793088, -0.3939789311157716, 0.24652318549800872, 0.7295744687777501, 0.30750833893882357, 0.4786458153729669], [0.36143434383472\n2:\"\"\"How concepts hop between fields: H2 next-field entry (gateway-weighted relatedness to RETAINING fields vs\n37:REGS = [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\", \"d_lost_gate\"]\n76:    \"\"\"fit M0-M3 on the primary sample (strata with a non-empty retaining set).\"\"\"\n83:                 \"M3_vs_M1\": H2.lr_test(fits[\"M3\"], fits[\"M1\"], 1), \"M2lost_vs_M0\": H2.lr_test(fits[\"M2lost\"], fits[\"M0\"], 1)}\n148:    # secondary sample: all strata with an empty-retaining-set indicator\n273:    # R3 incidence-function curve: P(retained) by S_hanski quintile, gateway top vs bottom tercile\n296:        out[\"relay_excess_gateway_retained\"] = {\"mean\": float(gr.mean()), \"n\": int(len(gr)),\n388:        # recompute ret_gw from the per-year retaining sets\n405:            rets.append((c, t, S[\"retaining\"][t - Y0].copy()))\n482:                           \"c_density\": \"Hidalgo density sum_{j in entered(t-1)} phi[j,k] / sum_j phi[j,k]\",\n483:                           \"e_gate_own\": \"gateway_eig of k\", \"d0_ret_rel\": \"mean_{j in Ret(t-1)} phi[j,k]\",\n485:                           \"d_lost_gate\": \"same over LOST fields (placebo)\"},\n486:            \"models\": H2.MODELS, \"primary_sample\": \"strata (concept, t) with non-empty retaining set; t = t0+1..t0+8\",\n490:            \"rescue\": \"R1 resc ~ retained x gate tercile + log n_early_j + log size_j | concept; R2 LPM with S_hanski, resc mediators\",\n491:            \"relay\": \"fepois relay ~ retained + gateway_j + retained x gateway_j + log n_early_j + log size_j | concept (continuous interaction; tercile dummies separated on dev); OLS relay_excess ~ retained x gate tercile\",\n497:                \"RESCUE_SUPPORTED\": \"R1 retained x top-gateway interaction >0 with CI>0 AND R2 indirect effect >0\",\n498:                \"RELAY_SUPPORTED\": \"retained x gateway_j fepois coefficient >0 with CI>0 AND mean relay_excess of top-tercile-gateway retained episodes >0\"}}\n600:        rp = rrh[\"relay_fepois\"][\"coef\"][\"ret_x_gate\"]; ex = rrh[\"relay_excess_gateway_retained\"]\n601:        dec[\"RELAY\"] = {\"fepois_ret_x_gate\": rp[\"b\"], \"ci\": rp[\"ci\"], \"mean_excess_gw_retained\": ex[\"mean\"],", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] ASSISTANT · 2026-09-28 21:01:55 UTC

```
I've classified the artifacts and checked the key numbers. Now I'm confirming how "retaining" is defined in Exp6, and then I'll write the revision.
```

### [14] TOOL CALL — Bash · 2026-09-28 21:01:55 UTC

```
Locate retaining-set definition in Exp6 code:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; grep -rn -i "\"retaining\"\|retaining\]\|def .*retain\|lost\b" --include=*.py . | grep -v "^./.venv" | head -20
```

### [15] TOOL RESULT — Bash · 2026-09-28 21:01:55 UTC

```
{"stdout": "method.py:83:                 \"M3_vs_M1\": H2.lr_test(fits[\"M3\"], fits[\"M1\"], 1), \"M2lost_vs_M0\": H2.lr_test(fits[\"M2lost\"], fits[\"M0\"], 1)}\nmethod.py:405:            rets.append((c, t, S[\"retaining\"][t - Y0].copy()))\nmethod.py:485:                           \"d_lost_gate\": \"same over LOST fields (placebo)\"},\nmake_outputs.py:175:                col = (\"#2ca02c\" if (k + 11) in home else \"#d62728\" if S[\"retaining\"][ti, k] else\nmake_outputs.py:176:                       \"#7f7f7f\" if S[\"lost\"][ti, k] else \"#1f77b4\" if S[\"entered\"][ti, k] else \"#c7c7c7\")\nmake_outputs.py:179:        ax.set_title(f\"{r['name']} (t0={t0}; green=home, red=retaining, blue=entered, grey=lost)\", fontsize=8)\nlib/traj.py:17:VARS = [\"n_entered_offhome\", \"n_retaining\", \"n_lost\", \"R20\", \"H\", \"G_share\", \"log_volume\"]\nlib/traj.py:29:                     \"n_retaining\": int(S[\"retaining\"][ti].sum()), \"n_lost\": int((S[\"lost\"][ti] & off).sum()),\nlib/traj.py:33:                     \"ret_gw\": int((S[\"retaining\"][ti] & top).sum()), \"ret_per\": int((S[\"retaining\"][ti] & bot).sum())})\nlib/h2.py:19:          \"M2lost\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d_lost_gate\"]}\nlib/h2.py:34:    lost = entered & (w3 == 0)\nlib/h2.py:35:    return {\"entered\": entered, \"retaining\": retaining, \"lost\": lost, \"w3\": w3, \"cum\": cum, \"offhome\": offhome}\nlib/h2.py:51:    \"\"\"Rows = (concept, year t, candidate field k not entered by t-1, not home). Returns df, Ret matrix, Lost matrix.\"\"\"\nlib/h2.py:55:    rows, RET, LOST = [], [], []\nlib/h2.py:70:            Ret = S[\"retaining\"][ti - 1]\nlib/h2.py:71:            Lost = S[\"lost\"][ti - 1] & S[\"offhome\"]\nlib/h2.py:75:            dl = (gate[Lost] @ phi[Lost]) / gate[Lost].sum() if Lost.any() and gate[Lost].sum() > 0 else np.zeros(26)\nlib/h2.py:78:                             int(Ret.sum()), int(Lost.sum()), r.group, r.split, int(r.intersection_born), float(r.home_gateway)))\nlib/h2.py:79:                RET.append(Ret); LOST.append(Lost)\nlib/h2.py:81:                                     \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\", \"d_lost_gate\", \"n_ret\", \"n_lost\", \"group\",", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-28 21:01:59 UTC

```
Read retention definition and look for edge persistence row:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art; sed -n 20,36p gen_art_experiment_6/lib/h2.py; python3 -c "
import json;d=json.load(open('gen_art_evaluation_1/full_eval_out.json')) if __import__('os').path.exists('gen_art_evaluation_1/full_eval_out.json') else None
" ; ls gen_art_evaluation_1 | head; grep -o '\"edge_persist[^}]*}' -m3 gen_art_evaluation_1/*eval_out*.json 2>/dev/null | head -5
```

### [17] TOOL RESULT — Bash · 2026-09-28 21:01:59 UTC

```
{"stdout": "def states(g: np.ndarray, home: list[int], min_n: int = 2) -> dict:\n    \"\"\"g: [NY, 27] grounded counts. Returns boolean [NY, 26] matrices (years Y0..).\"\"\"\n    x = g[:, 1:]\n    cum = np.cumsum(x, 0)\n    entered = cum >= min_n\n    w3 = x.copy()\n    w3[1:] += x[:-1]; w3[2:] += x[:-2]\n    ent_lag2 = np.zeros_like(entered); ent_lag2[2:] = entered[:-2]\n    offhome = np.ones(26, bool)\n    for h in home:\n        offhome[h - 11] = False\n    retaining = ent_lag2 & (w3 >= min_n) & offhome[None, :]\n    lost = entered & (w3 == 0)\n    return {\"entered\": entered, \"retaining\": retaining, \"lost\": lost, \"w3\": w3, \"cum\": cum, \"offhome\": offhome}\n\nREADME.md\n__pycache__\naudit.py\neval.py\neval_out.json\nfigures\nfull_eval_out.json\nharmonise.py\nlib.py\nlogs", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-09-28 21:02:07 UTC

```
Extract exp3 portability table from evaluation:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1; python3 - <<'E'
import json
d=json.load(open('eval_out.json'))
def find(x,key,path=''):
    if isinstance(x,dict):
        for k,v in x.items():
            if key in k: print(path+'/'+k, json.dumps(v)[:1500]); 
            else: find(v,key,path+'/'+k)
    elif isinstance(x,list):
        for i,v in enumerate(x[:50]): find(v,key,path+f'[{i}]')
find(d,'F3')
E
```

### [19] TOOL RESULT — Bash · 2026-09-28 21:02:07 UTC

```
{"stdout": "/metadata/F_record/F3_exp3_portability {\"ci_convention\": \"as stored in exp3 screen_result.json['portability'] (point Spearman within group; LOGO delta-rho without CI)\", \"table\": {\"groups\": [\"BIO\", \"CS\", \"ENG\", \"MED\"], \"indicators\": {\"D_z\": {\"pooled_rho_O2r\": 0.19605303731113166, \"pooled_rho_O1\": 0.1864555692956741, \"rho_logvol\": -0.632809127351218, \"within_group_rho_O2r\": {\"BIO\": 0.21470588235294116, \"CS\": 0.25874125874125875, \"ENG\": 0.26666666666666666, \"MED\": -0.35}, \"within_group_rho_O1\": {\"BIO\": -0.1960392117639214, \"CS\": 0.13937366833451514, \"ENG\": 0.10350983390135314, \"MED\": 0.3651483716701107}, \"n_missing\": 1, \"logo_single_rho_O2r\": -0.04740980573543016, \"rho_entropy\": -0.05186555658341042, \"rho_offhome_share\": -0.10490286771507863, \"rho_growth\": -0.09096515572001233, \"logo_delta_rho_O2r\": 0.016998149861239598, \"logo_delta_rho_per_group\": {\"BIO\": 0.02352941176470591, \"CS\": 0.07692307692307698, \"ENG\": 0.03333333333333344, \"MED\": 0.024242424242424176}, \"negative_result_CS_only\": false, \"n_groups_same_sign_as_pooled\": 3}, \"D_ratio\": {\"pooled_rho_O2r\": 0.5292013567684243, \"pooled_rho_O1\": -0.029832891087307863, \"rho_logvol\": 0.10884983040394695, \"within_group_rho_O2r\": {\"BIO\": 0.5647058823529412, \"CS\": 0.6293706293706295, \"ENG\": 0.33333333333333337, \"MED\": 0.5333333333333333}, \"within_group_rho_O1\": {\"BIO\": 0.1960392117639214, \"CS\": -0.08362420100070908, \"ENG\": -0.5175491695067657, \"MED\": 0.18257418583505536}, \"n_missing\": 1, \"logo_single_rho_O2r\": 0.4850832562442184, \"rho_entropy\": 0.15954363243909958, \"rho_of", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Bash · 2026-09-28 21:02:11 UTC

```
Rank co-occurrence indicators by pooled rho:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1; python3 - <<'E'
import json
t=json.load(open('eval_out.json'))['metadata']['F_record']['F3_exp3_portability']['table']['indicators']
for k,v in sorted(t.items(), key=lambda kv: -abs(kv[1].get('pooled_rho_O2r') or 0)):
    w=v['within_group_rho_O2r']; print(f"{k:22s} pooled {v.get('pooled_rho_O2r'):+.2f} logvol {v.get('rho_logvol'):+.2f} groups {[round(w[g],2) if w[g] is not None else None for g in w]} dLOGO {v.get('logo_delta_rho_O2r'):+.3f}")
E
```

### [21] TOOL RESULT — Bash [ERROR] · 2026-09-28 21:02:11 UTC

```
Error: Exit code 1
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
TypeError: unsupported format string passed to NoneType.__format__
```

### [22] TOOL CALL — Bash · 2026-09-28 21:02:15 UTC

```
Rank co-occurrence indicators by pooled rho:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1; python3 - <<'E'
import json
t=json.load(open('eval_out.json'))['metadata']['F_record']['F3_exp3_portability']['table']['indicators']
f=lambda x: 'NA' if x is None else f"{x:+.2f}"
for k,v in sorted(t.items(), key=lambda kv: -abs(kv[1].get('pooled_rho_O2r') or 0)):
    w=v['within_group_rho_O2r']; print(f"{k:22s} pooled {f(v.get('pooled_rho_O2r'))} O1 {f(v.get('pooled_rho_O1'))} logvol {f(v.get('rho_logvol'))} groups {[f(w[g]) for g in w]} dLOGO {f(v.get('logo_delta_rho_O2r'))}")
E
```

### [23] TOOL RESULT — Bash · 2026-09-28 21:02:15 UTC

```
{"stdout": "entropy                pooled +0.70 O1 +0.32 logvol +0.13 groups ['+0.56', '+0.78', '+0.60', '+0.83'] dLOGO NA\nD_rare                 pooled +0.63 O1 -0.00 logvol +0.15 groups ['+0.67', '+0.59', '+0.47', '+0.68'] dLOGO +0.03\nD_ratio                pooled +0.53 O1 -0.03 logvol +0.11 groups ['+0.56', '+0.63', '+0.33', '+0.53'] dLOGO +0.01\nnfields2               pooled +0.53 O1 -0.04 logvol +0.65 groups ['+0.14', '+0.69', '+0.49', '+0.64'] dLOGO NA\nparticipation          pooled +0.51 O1 +0.07 logvol +0.10 groups ['+0.51', '+0.12', '+0.62', '+0.58'] dLOGO +0.02\nn_comm_W3              pooled +0.50 O1 -0.03 logvol +0.58 groups ['+0.32', '+0.52', '+0.14', '+0.73'] dLOGO +0.00\nNOV                    pooled +0.46 O1 +0.03 logvol +0.08 groups ['+0.62', '+0.27', '+0.39', '+0.67'] dLOGO +0.00\nNOV_res                pooled +0.45 O1 +0.03 logvol +0.05 groups ['+0.61', '+0.27', '+0.35', '+0.67'] dLOGO -0.01\noffhome_share          pooled +0.42 O1 +0.35 logvol +0.06 groups ['+0.37', '+0.28', '+0.20', '+0.85'] dLOGO NA\nbtw_t4                 pooled +0.33 O1 -0.06 logvol +0.79 groups ['+0.17', '+0.31', '+0.05', '+0.64'] dLOGO -0.05\nconstraint_t4          pooled -0.32 O1 +0.03 logvol -0.78 groups ['-0.11', '-0.27', '-0.13', '-0.66'] dLOGO +0.00\nD_sub                  pooled +0.29 O1 -0.01 logvol -0.55 groups ['+0.64', '+0.08', '+0.57', '-0.20'] dLOGO +0.04\nM                      pooled +0.28 O1 -0.13 logvol +0.80 groups ['+0.07', '+0.26', '-0.13', '+0.64'] dLOGO -0.02\nbtw_change             pooled +0.27 O1 +0.25 logvol +0.51 groups ['+0.19', '+0.33', '+0.05', '+0.25'] dLOGO -0.09\ncomm_transitions       pooled +0.27 O1 +0.21 logvol -0.05 groups ['+0.34', '-0.32', '+0.60', '+0.57'] dLOGO +0.00\nedge_persistence       pooled -0.25 O1 -0.35 logvol +0.18 groups ['-0.34', '-0.52', '-0.07', '-0.22'] dLOGO +0.01\nD_z                    pooled +0.20 O1 +0.19 logvol -0.63 groups ['+0.21', '+0.26', '+0.27', '-0.35'] dLOGO +0.02\nego_density_change     pooled -0.17 O1 -0.29 logvol -0.36 groups ['+0.04', '-0.39', '-0.08', '+0.08'] dLOGO -0.01\nbtw_t0                 pooled +0.16 O1 -0.30 logvol +0.49 groups ['+0.37', '+0.00', '-0.03', '+0.53'] dLOGO +0.02\ndeg_growth             pooled +0.16 O1 +0.42 logvol +0.24 groups ['-0.18', '+0.45', '-0.27', '+0.08'] dLOGO -0.01\ngrowth                 pooled +0.15 O1 +0.48 logvol +0.18 groups ['-0.33', '+0.08', '-0.15', '+0.03'] dLOGO NA\nnew_edge_rate          pooled +0.15 O1 +0.30 logvol +0.30 groups ['-0.27', '+0.48', '-0.32', '+0.35'] dLOGO -0.02\nD_withself             pooled +0.14 O1 +0.16 logvol -0.63 groups ['+0.12', '+0.29', '+0.28', '-0.35'] dLOGO +0.01\nD_lag                  pooled +0.14 O1 +0.19 logvol -0.67 groups ['+0.20', '+0.36', '+0.23', '-0.50'] dLOGO +0.03\nlogvol                 pooled +0.11 O1 -0.23 logvol +1.00 groups ['-0.26', '+0.40', '-0.08', '+0.50'] dLOGO NA\nF_bg                   pooled -0.11 O1 -0.19 logvol +0.40 groups ['+0.29', '+0.13', '-0.40', '-0.35'] dLOGO -0.04\nconstraint_change      pooled +0.07 O1 -0.35 logvol +0.29 groups ['+0.38', '-0.03', '+0.00', '+0.28'] dLOGO -0.05\nkcore_t4               pooled -0.06 O1 -0.21 logvol +0.12 groups ['-0.54', '-0.08', '+0.00', '+0.56'] dLOGO -0.06\nstr_growth             pooled +0.06 O1 +0.38 logvol +0.07 groups ['-0.21', '+0.47', '-0.23', '-0.13'] dLOGO -0.02\nF_obs_growth           pooled +0.05 O1 -0.41 logvol +0.32 groups ['+0.39', '-0.10', '-0.17', '+0.20'] dLOGO -0.08\nturnover               pooled -0.04 O1 -0.36 logvol -0.14 groups ['-0.01', '+0.05', '-0.05', '+0.17'] dLOGO -0.02\nF_res                  pooled -0.01 O1 -0.17 logvol +0.04 groups ['+0.41', '-0.17', '-0.18', '-0.07'] dLOGO -0.06\nF_z                    pooled +0.01 O1 -0.09 logvol -0.06 groups ['+0.43', '-0.19', '-0.15', '+0.00'] dLOGO -0.02\nD_q                    pooled +0.00 O1 -0.10 logvol -0.24 groups ['-0.06', '+0.04', '+0.00', '-0.03'] dLOGO +0.00", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] ASSISTANT · 2026-09-28 21:04:49 UTC

```
Next I'll write the revised hypothesis JSON, the manifest and the README.
```

### [25] TOOL CALL — Bash · 2026-09-28 21:04:49 UTC

```
Build and validate revised hypothesis JSON:
mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-3-invention-loop-iter-2-upd-hypo-upd-hypo/01f9c221-1f7b-44e6-8800-6f1ad928bcd3/scratchpad && cat > /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-3-invention-loop-iter-2-upd-hypo-upd-hypo/01f9c221-1f7b-44e6-8800-6f1ad928bcd3/scratchpad/build.py <<'PYEOF'
import json
H = """MAIN CLAIM (RQ2 mechanism, with RQ1's held-out deliverable attached). A new concept spreads across disciplines from its RETAINED FRONTIER, not from its contact footprint. Definitions are Exp6's frozen ones (lib/h2.py states(), 26 venue-label fields, grounded counts), kept verbatim. For concept c in year t: ENTERED(t) = fields with >= 2 cumulative grounded papers. RETAINED(t) = off-home fields entered >= 2 years earlier that still have >= 2 papers in t-2..t. LOST(t) = entered fields with 0 papers in t-2..t. CLAIM: the next field k a concept enters is predicted by its relatedness to RETAINED fields (d0_ret_rel = mean phi[j,k] over RETAINED(t-1), on the frozen 1998-2002 PMI backbone). It must add beyond four things: (i) the CONVENTIONAL Hidalgo 2007 / Guevara 2016 density on the thresholded current portfolio (fields with RCA_cj(t-1) > 1, no persistence requirement), D_rca; (ii) a share-weighted current-presence density, D_vol; (iii) the unthresholded ever-entered density (Exp6's M0); (iv) target-field size, relatedness to home and the target's own centrality. The lead has not yet faced (i). COROLLARY, the ABANDONMENT PENALTY: given ever-entered density, relatedness to LOST fields LOWERS the entry hazard of their neighbours. The principle of relatedness treats any revealed presence as capability, so it predicts that persistence adds nothing beyond current RCA and that a lost presence is neutral or positive. We predict both are wrong. MECHANISM (invasion biology: casual versus naturalised aliens, Richardson et al. 2000; Blackburn et al. 2011). Iteration 1 already showed that early off-home adoption is mostly borrowed (A*_h medians negative in every group; M1: background homophily explains 66-72% of raw lineage). A field that keeps using a concept for years has fitted it to its own methods and co-concepts, and that adapted form is what related neighbours import. A one-off contact that is dropped is a failed introduction, and it signals poor fit to the similar fields next to it. The one-sentence finding we expect to state: 'fields pick up a new concept from neighbours that kept it, not from neighbours that tried it — and a neighbour that dropped it makes adoption less likely'. That would change what emergence monitors track (retained adopters, not fields touched), and it refines the relatedness principle at the level of single concepts.

EVIDENCE BEHIND IT (a LEAD from art_N-mpomDZZ1ln, one frame only). Held-out conditional logit: 369 concepts, 1,373 entry events, 961 strata. M1 vs M0 LR = 68.6; d0_ret_rel = +0.281 per SD (SE 0.032). Group d for the gateway-weighted twin: Physical 0.33 (CI > 0), LifeEnv 0.18 (LR p 0.23), Social 0.24 (LR p 0.076), cohort 0.29 (CI > 0). Sign 4/4 (p 0.0625). DL pooled 0.28 [0.22, 0.35], I2 = 0. Label permutation p = 0.001; rewired backbone p = 0.015. Exact-likelihood audit: LR 77.3. Within-stratum AUC rises only from 0.809 to 0.817; log size alone gives 0.757 and density 0.590. M2lost: d_lost = -0.063 (SE 0.035, LR p = 0.055) on sparse lost sets (mean 0.02). The dev value is positive too (M2 vs M0 LR 38.6). CLOSED THIS ROUND, one sentence each in the paper. (a) Gateway centrality as the retention driver (H1). Exp5: 27,393 episodes, held-out dAUC -0.00001 [-0.0006, 0.0003]; crossed concept x field CI [-0.0023, 0.0010]. It is absorbed by the field retention propensity P_j(-c) and reverses on held-out. Eval1: union +0.001 [-0.012, 0.012]; iteration-1's +0.10 does not beat a shuffled-R placebo (95th percentile 0.130). One residual is recorded, not chased: the within-field LPM with field FE gives 0.068 per SD (p_concept 0.041, two-way p 0.17). (b) The gateway weighting of retaining relatedness (M3 vs M1 g-only perm p 0.17). (c) Rescue and relay: the relay fepois interaction is -1.30 [-4.9, 2.3]. (d) Gateway landing G at concept level (H3): held-out partial rho 0.030, pooled bootstrap CI95 [-0.006, 0.065], about a quarter of its DEV value 0.138, and the permutation null is centred near -0.012. (e) All G-variant O1 gains are label-coverage artefacts. (f) A*_h and D_ratio as headlines.

DESIGN (zero OpenAlex credits: the key is exhausted and the 476M-work S3 snapshot scans already exist; LLM spend < $1). (1) ATTACK THE BASELINE on the Exp6 risk sets already sealed (entry_risk_sets_dev/heldout.parquet plus Exp6's cached concept x field x year counts; no new scan). Nested LR ladder: M0 -> +D_rca -> +D_vol -> +d0_ret_rel -> +d_lost. RCA_cj(t-1) = concept share in j / all-works share in j. This re-analyses evidence already seen once, so it is labelled ROBUSTNESS, not confirmation. (2) INDEPENDENT CONFIRMATION on a body of evidence the lead never touched. Use the Exp5 S1 frame (frame_concepts.csv, 12,499 concepts, TAG grounding with LLM precision gate, episodes.csv 27,393) MINUS every concept ID in the Exp6 frame, with the overlap count reported. Build the same year x field state matrices from Exp5's cached snapshot matches, then fit M0..M4. Use its DEV split (CS/Eng/BGM/Med homes, onset 2003-09) only to check code, convergence and power, then hash-freeze. Evaluate ONCE on PHYS / LIFEENV / SOC / MATHDEC (MATHDEC has 165 concepts, testable for the first time) and on the 2010-14 cohort, with the cohort split into DEV-home and non-DEV-home fields. (3) SPECIFICITY AND DOSE. (a) A within-concept-year placebo: permute which ENTERED fields count as RETAINED, keeping the footprint and scrambling persistence. (b) A volume-matched contrast: retained fields against one-off fields of equal t-1 paper count, so persistence is separated from volume. (c) Dose: persistence age 2 / 3 / >= 4 years. (d) The rewired backbone. (e) Exclude intersection-born concepts. (f) Use min_n = 3 and 5 as a sensitivity check. (4) RQ1 TRANSLATION, pre-declared as 4 extra rows of the matrix in (5). Feature window t0..t0+2 only: CONTACT_REACH (fields with >= 1 paper); RETAINED_REACH (fields with >= 2 papers in 2 of the 3 years); RETENTION_RATIO_early = RETAINED_REACH / CONTACT_REACH; FRONTIER_POTENTIAL (sum over not-entered k of mean phi to early-retained fields). Prediction: RETENTION_RATIO_early and FRONTIER_POTENTIAL have held-out partial rho > 0 with O2r_resid and O1 given B5; CONTACT_REACH does not. (5) RQ1 HELD-OUT DELIVERABLE, no longer deferred, on the Exp5 frame with ONE outcome table and ONE fold assignment. Recompute from the snapshot the ~34 concept-level co-occurrence ego-network indicators of art_yrradSC27HtQ (full-corpus topic PMI per slice, Leiden gamma 3; degree/strength/new-edge growth, edge persistence, turnover, NOV/NOV_res, participation, D_ratio/D_rare/D_z, betweenness, constraint, k-core, clustering change, community transitions). Add family F (reach, entropy, off-home share), the G variants, simple count/growth baselines, the 4 frontier rows and candidate S (unconnected co-author components among off-home early adopters, from snapshot author IDs; its one fix, dropped if not computable). Outcomes: O1, O2r (m = 30/50), O2r_resid, O3, O4 (citation growth from snapshot referenced_works) and O5. O5 joins art_O7Dq4L02QnDN on legacy concept ID and is built from year_usable events only: MeSH introduced after t0; Wikipedia or Wikidata dated by t0+8; a taxonomy added between versions. A Wikipedia/Wikidata-only O5 variant runs across all groups, because Social and Eng have no dated taxonomy. On DEV only, rank by partial Spearman given B5 and by AUC, and freeze a top 10 per outcome plus an L1-logistic / EBM model. Score ONCE on held-out groups and the cohort. Report per group, DL-pooled with I2, Holm-corrected, with concept-clustered refit bootstrap CIs and crossed concept x field CIs for episode-level tests. Pre-registered from the P78 portability table (art_lwI2DuRtQRZX F3). Entropy (0.70), D_rare (0.63), D_ratio (0.53), participation (0.51) and NOV_res (0.45), which were positive in 4/4 dev groups, should stay associated with O2r on held-out but add little beyond B5. Edge persistence (-0.25, negative in 4/4) should stay NEGATIVE: a concept that keeps its semantic neighbours stays local. The CS-only indicators (degree, strength and new-edge growth) should fail held-out, and that is reported as a domain-specific negative result. (6) RQ2 TRAJECTORIES, rebuilt on per-field state sequences (untouched / entered / retained / lost). Decompose breadth into contact rate x retention probability x frontier advance per retained field. TEST: localised concepts differ from integrating ones mainly in RETENTION PROBABILITY, not in contact rate, with Medicine homes adjusted for and also excluded (Exp6's 'localised' class was 42/60 Medicine). Fit DTW k-medoids and an HMM. A trajectory class is named only if the two agree (ARI >= 0.5) and it survives excluding Medicine homes; otherwise it is reported as a continuum. Exp6's k = 2 fails that test (HMM-vs-DTW ARI 0.094). (7) WHY IT WORKS. Case studies are taken from the quantitative extremes of the frontier effect, with Exp6's field-flow plots. Compare the papers of retained and lost adopters in the same field: do retained adopters cite field-specific co-concepts and methods (a zero-credit lineage check from snapshot references)?

SUCCESS. The frontier claim is CONFIRMED if, on the independent Exp5-minus-Exp6 held-out, all of these hold: d0_ret_rel > 0 with concept-clustered CI > 0 and LR p < 0.01 over M0 + D_rca + D_vol; the same sign in >= 3 of 4 held-out groups and in the cohort; the retained-label permutation is rejected (p < 0.05); the volume-matched contrast is > 0; and in the Exp6 robustness ladder d0_ret_rel survives D_rca. The ABANDONMENT PENALTY is CONFIRMED if pooled held-out d_lost < 0 with CI < 0. INFORMATIVE EITHER WAY. If D_rca absorbs d0_ret_rel, the finding is that the relatedness principle holds unchanged for single concepts with the standard RCA portfolio and that persistence adds nothing. It is then reported as that, with entry AUCs set against Guevara 2016 (0.68-0.90) and Chinazzi et al. 2019. If d_lost >= 0, a dropped contact still primes its neighbours, and the failed-introduction account is rejected. DISCONFIRMED: the pooled held-out CI of d0_ret_rel over D_rca includes 0, or the effect holds only on the Exp6 frame. RECORD, carried into the paper. The ordering result ('first retained gateway precedes entropy take-off') is MIXED, not confirmed: the sign rule passed (57 before / 15 ties / 30 after, among 102 evaluable of 175 top-tercile concepts), but the concept-FE lead-lag coefficients are NEGATIVE (ret_gw -0.028, ret_per -0.043), there is a significant pre-trend (ev-3 -0.072), dev shows entropy -> later gateway retention (b 0.232, p 0.006), and the placebo p is 0.63. The common-panel design was NOT realised in iteration 2: Exp5 and Exp6 used different frames, grounding rules and episode definitions. This iteration makes the Exp5 frame the single panel. O5 has not yet been evaluated against any indicator."""

key_changes = [
 "Headline moves from gateway centrality (closed: Exp5 held-out dAUC -0.00001 on 27,393 episodes; Eval1 union +0.001) to the RETAINED-FRONTIER lead from art_N-mpomDZZ1ln (held-out d0_ret_rel +0.281, SE 0.032, LR 68.6).",
 "The reviewer's nearest-neighbour objection becomes the decisive test: d0_ret_rel must beat the conventional RCA>1 Hidalgo/Guevara density and a share-weighted current-presence density, not just Exp6's unthresholded ever-entered density.",
 "New non-obvious corollary (ABANDONMENT PENALTY): relatedness to LOST fields lowers neighbours' entry hazard (Exp6 hint: d_lost -0.063, LR p 0.055). The relatedness principle predicts no such effect. The mechanism is casual vs naturalised introductions from invasion biology.",
 "Independent confirmation on a second body of evidence: the Exp5 frame minus every Exp6 concept, dev only for code and power, hash-frozen, then held-out groups (including MathDec, testable for the first time) and the cohort, evaluated once. The Exp6 held-out re-analysis is labelled robustness only.",
 "Specificity checks added: a retained-label permutation within concept-year, a volume-matched persistence contrast, persistence-age dose, rewired backbone, min_n sensitivity and exclusion of intersection-born concepts.",
 "RQ1 held-out deliverable made mandatory on the Exp5 frame: ~34 co-occurrence ego-network indicators recomputed from the snapshot, plus families F and G, count baselines, 4 frontier rows and candidate S, against O1/O2r/O2r_resid/O3/O4/O5. Top 10 per outcome frozen on DEV and scored once, per group and DL-pooled, Holm-corrected, plus an L1/EBM learned model.",
 "O5 external recognition (art_O7Dq4L02QnDN) joined as an outcome for the first time, from year_usable events only, with a Wikipedia/Wikidata-only variant because Social and Eng lack a dated taxonomy.",
 "Pre-registered portability predictions from the F3 table: entropy, D_rare, D_ratio, participation and NOV_res stay associated with O2r but add little over B5; edge persistence stays negative; CS-only degree/strength/new-edge growth fail held-out.",
 "RQ2 trajectories rebuilt on per-field state sequences (entered/retained/lost), with a breadth decomposition into contact x retention x frontier advance. Classes are named only if DTW and HMM agree (Exp6's k=2 failed: ARI 0.094) and the class survives excluding Medicine homes.",
 "Record corrections carried into the claim. Ordering is moved to MIXED (negative FE lead-lag coefficients, pre-trend ev-3 -0.072, dev reverse path significant, placebo p 0.63). H3 is closed (bootstrap CI includes 0; a quarter of its DEV value). The residual within-field LPM gateway coefficient (p_concept 0.041, two-way p 0.17) is recorded but not chased. The common panel was not realised in iteration 2.",
 "Gateway weighting, rescue, relay, H3 gateway landing, the G-variant O1 gains (label-coverage artefacts), A*_h and D_ratio are closed as headline bets, with one sentence each in the paper.",
]

strands = [
 {"artifact":"art_wxWssKSUR45f","state":"null","why":"H1 gateway held-out dAUC -0.00001 [-0.0006,0.0003] on 27,393 episodes, absorbed by P_j(-c); H3 G partial rho 0.03, bootstrap CI95 [-0.006,0.065], 1/4 of DEV. Frame reusable."},
 {"artifact":"art_N-mpomDZZ1ln","state":"lead","why":"Held-out retaining-relatedness d +0.281 (SE .032), LR 68.6, perm p .001; AUC .809->.817 only; not yet tested vs RCA-thresholded density; one frame; lost-field d -0.063 p .055."},
 {"artifact":"art_lwI2DuRtQRZX","state":"null","why":"Gateway retention lead fails: union +0.001 [-0.012,0.012]; iteration-1's +0.103 is below the shuffled-R placebo 95th pct 0.130; all G O1 gains are label-coverage artefacts."},
 {"artifact":"art_O7Dq4L02QnDN","state":"broken","why":"O5 recognition table built (65,026 concepts) but never joined to any panel; no indicator tested against external recognition, so untested rather than refuted."},
 {"artifact":"art_dxvRpQufMR0e","state":"null","why":"Positioning only, no test. It flags the relatedness-density rival (Hidalgo 2007/Guevara 2016) that the H2 lead must now beat; the rescue/relay analogies are partly anticipated."},
]

rels = [
 {"from_id":"art_33_KKk_G8Gw5","to_id":"art_lwI2DuRtQRZX","relation_type":"differences","relation_rationale":"Stress test fails to replicate exp4's +0.103 gateway retention gain (union +0.001; below the shuffled-R placebo)"},
 {"from_id":"art_xp8BGBJZsxeI","to_id":"art_lwI2DuRtQRZX","relation_type":"uses","relation_rationale":"Reuses exp1's 367 field-retention units (s2-fos crosswalk) as replication episodes"},
 {"from_id":"art_yrradSC27HtQ","to_id":"art_lwI2DuRtQRZX","relation_type":"uses","relation_rationale":"Reuses exp3's 129 field-retention units and its portability table as replication inputs"},
]

out = {
 "title": "Concepts spread from fields that keep them",
 "hypothesis": H,
 "relation_rationale": "Same concept x field episode frame; the gateway-position claim gives way to the retained-frontier entry lead",
 "confidence_delta": "decreased",
 "key_changes": key_changes,
 "strands": strands,
 "evidence_state": "lead",
 "move": "deepen",
 "move_rationale": "Best strand is a lead (held-out retaining-relatedness d +0.28, one frame). Deepen it: beat RCA-thresholded density, confirm on the independent Exp5 frame, test the abandonment penalty.",
 "coverage": "full",
 "coverage_statement": "Next iteration answers RQ2 (the retained-frontier diffusion mechanism and state-sequence trajectories) and RQ1's held-out step (the frozen top-10 network indicators scored once on held-out fields and the cohort, including external recognition O5).",
 "candidates_considered": 12,
 "relation_type": "evolution",
 "artifact_relations": rels,
}
for s in strands: assert len(s["why"])<=200, (s["artifact"], len(s["why"]))
for r in rels: assert len(r["relation_rationale"])<=120
assert len(out["relation_rationale"])<=120 and len(out["move_rationale"])<=200, (len(out["relation_rationale"]), len(out["move_rationale"]))
json.dump(out, open("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json","w"), indent=2, ensure_ascii=False)
print("ok", len(H))
PYEOF
python3 /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-3-invention-loop-iter-2-upd-hypo-upd-hypo/01f9c221-1f7b-44e6-8800-6f1ad928bcd3/scratchpad/build.py
```

### [26] TOOL RESULT — Bash · 2026-09-28 21:04:49 UTC

```
{"stdout": "ok 10852", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": true}
```

### [27] TOOL CALL — Bash · 2026-09-28 21:04:59 UTC

```
Write manifest and README, verify output:
printf 'entries: []\n' > .aii/manifest.yaml && cat > README.md <<'EOF'
# upd_hypo — iteration 2 hypothesis revision

This step revises the run's hypothesis using the evidence from iteration 2. It produces only the revised hypothesis text: no code is run and no artifacts are generated here.

## What was decided
The five artifacts of iteration 2 were classified one by one:

| Artifact | State | Why |
|---|---|---|
| Exp5 (gateway held-out test) | null | Gateway retention gain is about 0 on 27,393 episodes; the concept-level H3 effect is tiny. |
| Exp6 (next field entered) | lead | Relatedness to the fields that currently retain a concept predicts the next field entered on held-out data. |
| Eval1 (gateway replication) | null | The gateway retention gain did not replicate. |
| Dataset 2 (O5 external recognition) | broken | The recognition table was built but never joined to a panel, so O5 is still untested. |
| Research 1 (positioning) | null | Positioning study with no test; it names the relatedness-density rival. |

The round summary is therefore **lead**, and the move is **deepen**. The new title is "Concepts spread from fields that keep them" (the retained-frontier claim plus the abandonment penalty). Four things are planned for the next iteration:
- test the lead against the RCA-thresholded Hidalgo density;
- confirm it on the Exp5 frame, with every Exp6 concept removed;
- deliver the frozen RQ1 indicator matrix on held-out data, including O5;
- rebuild the trajectories on field-state sequences.

## Layout
- `.terminal_claude_agent_struct_out.json`: the revised hypothesis, strand classification, move, coverage, and the artifact relations.
- `.aii/manifest.yaml`: the storage manifest. It has no heavy files, so it lists no entries.
- `README.md`: this file.

## How to run
Nothing needs to be run. A later pipeline step reads the JSON output.

## Restoring removed files
No files are marked `delete`, so nothing needs restoring.
EOF
python3 -c "import json;d=json.load(open('.terminal_claude_agent_struct_out.json'));print(d['evidence_state'],d['move'],len(d['strands']))"; ls -la
```

### [28] TOOL RESULT — Bash · 2026-09-28 21:04:59 UTC

```
{"stdout": "lead deepen 5\ntotal 2266\ndrwxr-xr-x 3 root root 1025399 Sep 28 21:04 .\ndrwxr-xr-x 3 root root 1032175 Sep 28 21:00 ..\ndrwxr-xr-x 2 root root    1200 Sep 28 21:04 .aii\n-rw------- 1 root root      54 Sep 28 21:00 .aii_claude_session.json\n-rw-r--r-- 1 root root  241301 Sep 28 21:04 .repl_agent.ptylog\n-rw-r--r-- 1 root root   16832 Sep 28 21:04 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    1890 Sep 28 21:04 README.md", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] ASSISTANT · 2026-09-28 21:05:14 UTC

```
I've revised the hypothesis and written it to `.terminal_claude_agent_struct_out.json`, with `README.md` and `.aii/manifest.yaml` beside it. The gateway-centrality claim is dead. The only live signal is Exp6's result, so the next iteration is set to deepen that one.

**How each artifact was classified:**

| Artifact | State | Main number |
|---|---|---|
| art_N-mpomDZZ1ln (Exp6) | **lead** | Relatedness to the fields that currently keep using a concept predicts the next field it enters: held-out effect +0.281 per SD (SE 0.032). AUC rises only from 0.809 to 0.817. |
| art_wxWssKSUR45f (Exp5) | null | Gateway gain for retention is −0.00001 on 27,393 episodes. The concept-level gateway effect (H3) is 0.03, and its bootstrap interval includes zero. |
| art_lwI2DuRtQRZX (Eval1) | null | The +0.10 gateway result doesn't replicate: +0.001 on the pooled panel, and it falls below a shuffled-label placebo. |
| art_O7Dq4L02QnDN (recognition data) | broken | The external-recognition table was built but never joined to any panel, so that outcome is untested, not refuted. |
| art_dxvRpQufMR0e (positioning) | null | Positioning only; it names the relatedness-density rival the lead now has to beat. |

That makes the round a **lead**, and the rule gives **deepen**. I weighed 12 candidate claims and set coverage to "full".

**The revised hypothesis, "Concepts spread from fields that keep them":**
- **Main claim:** a concept enters new fields next to the fields that kept using it, not next to every field it merely touched.
- **Decisive test:** the claim must beat the standard relatedness density from the economics literature (Hidalgo 2007 / Guevara 2016), computed only over fields where the concept is currently over-represented. This was the reviewer's main novelty objection, and Exp6's baseline never included it.
- **New prediction (abandonment penalty):** a field that tried the concept and dropped it makes its neighbouring fields *less* likely to take it up. Exp6 already leans this way (−0.063, p = 0.055), and standard relatedness theory doesn't predict it. The rationale comes from invasion biology: a failed introduction signals poor fit to similar nearby fields.
- **Independent confirmation:** the Exp5 concept set, minus every concept Exp6 used, evaluated once after freezing. Re-running Exp6's already-seen held-out data only counts as a robustness check.
- **RQ1 deliverable, now mandatory:**
  - Recompute the ~34 co-occurrence network indicators on the Exp5 panel.
  - Join the external-recognition outcome for the first time.
  - Freeze a top 10 per outcome on the development split and score them once on held-out fields and the 2010–14 cohort.
  - Predictions are written down in advance, including that edge persistence stays negative and that the CS-only indicators fail.
- **RQ2 trajectories:** rebuilt from each field's state over time (entered / kept / dropped). A trajectory class is only named if two clustering methods agree and it survives dropping Medicine-home concepts. Exp6's two-class solution fails that test (agreement 0.094).

**Reviewer corrections now written into the hypothesis:**
- The claim that the first retained gateway field comes before entropy take-off is moved to "mixed": the fixed-effect regressions go the wrong way, entropy was already rising beforehand, and the placebo gives p = 0.63.
- H3 is closed.
- The within-field gateway coefficient (p = 0.041 with concept-clustered errors, 0.17 with two-way clustering) is recorded but not pursued.
- The shared panel that iteration 2 planned was never actually built; Exp5 and Exp6 used different concept sets.

Everything planned uses the existing snapshot scans, because the OpenAlex credits are used up. There are no large files in the workspace, so the manifest has no entries.
```
