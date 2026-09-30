# Pre-registration: Frame N (vocabulary-free newborn title phrases), confirmation of the home-neighbourhood churn signal

Written at S0. No Frame-N candidate list, onset, feature or outcome existed when this file was hashed into
`logs/seal.log` (record `S0_prereg`). Pass M (sample n-gram counting) had already been launched with the rules in
`lib/nrules.py`. Its sha256 is recorded in the same S0 record, and no Pass-M output had been inspected beyond the
per-file row counts in the log. This ordering is logged as deviation `D_passM_before_prereg`.

## 1. Mining rules (S2-S3)
* Sample: works files with `fi % 5 == 0` (408 of 2,040 files; snapshot 2026-09-23). Base filter as in EXP10 passC
  (type article|review, not paratext, not xpac). Publication years 2000..2017. Titles only.
* Tokens: `common5.surf(title).split()`. A token is VALID iff it matches `^(?=.*[a-z])[a-z0-9]{2,}$`, i.e. ASCII,
  >= 2 characters, not purely numeric. The ASCII rule is a declared tightening that restricts Frame N to English-script
  titles.
* n-grams: n in {2,3}. All tokens are valid. First and last token are not in STOP, where STOP = NLTK English stopwords
  (verbatim list) + spaCy es/pt/fr/de/it stop lists (the NLTK corpus download is blocked here) minus 13 English
  content words + FILLER (41 academic filler tokens, `lib/nrules.py`). Frozen in `inputs/stoplists.json`.
* KEY = tuple of Porter stems of the n-gram tokens. Stem-key grouping is applied AT COUNTING TIME: the counted unit is
  the key, so surface variants share one count. This is a declared deviation from 'hash the surface n-gram, then
  group', and it avoids splitting a phrase's count across plural/singular forms. Each key counts at most once per title.
* Candidate rule, per t in 2003..2017: `s_t(h) >= k_t` AND `max(s_{t-3}, s_{t-2}, s_{t-1}) <= floor(0.25 * s_t(h))`.
  `k_t = max(3, smallest integer such that |cand_t after lexical exclusions (i)-(iii)| <= 4,500)`.
  `t_det(h)` = first t with h in cand_t.
* Lexical exclusions:
  * (i) The key equals the key of any legacy form: lexicon_v1 forms (incl. aliases), the 65,026 art_O7Dq4L02QnDN
    display names, EXP5 frame_concepts names/aliases, and EXP10 cohort_candidates names.
  * (ii) Token-contiguous containment in either direction with any MULTI-token legacy key. Single-token legacy forms
    count for exact equality only.
  * (iii) The frozen generic phrase list (`lib/nrules.GENERIC`), plus any key containing a token of a country name or
    a city with population >= 1M (geonamescache).
* POS filter: spaCy en_core_web_sm tags up to 5 sample titles containing the phrase. Keep if, in >= 60% of contexts,
  the phrase tokens are `(ADJ|NOUN|PROPN)* (NOUN|PROPN)`. For a trigram with a stopword middle token, the middle token
  may be ADP/CCONJ/DET. This is declared: without it, 'theory of mind' patterns could never pass.
* Surface forms: the most frequent sample surface form is the name. Aliases are the other surface forms with >= 2
  sample occurrences (at most 6).
* Recall benchmark (report only): the mining rule WITHOUT exclusions, applied to the keys of EXP5 frame_concepts names
  with 2-3 tokens and t0 2003-2014. Report the share with t_det <= t0+2, by logvol tertile.

## 2. Pass N, onset, seals
* All 2,040 files. Titles 1995..2022 are matched with the Aho-Corasick automaton of all candidate aliases
  (`matcher.build_automaton`, stemmed verification `matcher.match`).
* Routing at write time:
  * year > t_det+2 -> `sealed/parts/sealedA_XXXX.parquet` (AGG ci, year, vfield, n), never opened before the unseal;
  * t_det-5 <= year <= t_det+2 -> `open/early_XXXX.parquet` (detail rows);
  * year < t_det-5 -> `open/pre_XXXX.parquet` (AGG).
* ONSET: t0 = first y in 2003..2014 with N(y) >= 20 verified title matches (all venues) AND N(x) < 0.25*N(y+2) for
  each x in y-3..y-1.
* The finder reads only years <= t_det+2 (MaskedCounts raises otherwise). Hence t0 <= t_det, and t0 >= t_det-2 is the
  OUTCOME-BLIND SELECTION CLAUSE (t_det <= t0+2).
* Extension set: t0 = 2015 (shift = 1 outcome window t0+5..t0+7), used only if fallback E triggers.
* SEAL-B: every open row with year >= t0+3 moves to `sealed/parts/sealedB.parquet`, hashed before any feature code runs.
* CONTAINMENT DEDUP: if A's tokens are a contiguous sub-sequence of B's and
  N_B(t0_A..t0_A+2) >= 0.6*N_A(t0_A..t0_A+2), keep B and drop A; otherwise drop B.

## 3. Precision gate + type
* Model google/gemini-2.5-flash-lite, temperature 0, 8 phrases per call. 20 titles per phrase (<= 200 chars), sampled
  with seed 7919+ci from the t0..t0+2 rows.
* JSON output {ci, specific, sense_share, type in method|object|property|topic, generic, gloss}.
* KEEP iff specific AND sense_share >= 0.8 AND NOT generic.
* Second model openai/gpt-4.1-mini on 100 random kept phrases (stratified by group): kappa on keep and on type. M2
  labels all M1 method/object phrases if the budget allows; within-type tests use M1 == M2 phrases.
* Blind check: the executor agent (an LLM, not a human annotator) labels 60 phrases (30 kept, 30 rejected; titles only).
* If keep-precision on the blind check is < 0.8, the rule tightens to sense_share >= 0.9 BEFORE the freeze.
* F7: if the M1-M2 kappa on type is < 0.4, R2 keeps only the generic flag.
* LLM cap: $1.35 hard stop for this artifact. Only gated phrases enter the frame.

## 4. Home, groups
* home = venue fields holding >= 40% of the first 30 venue-labelled grounded papers with year <= t0+2 (ordered by year
  then work id).
* >= 2 home fields = intersection-born.
* group = GROUP_OF_FIELD of the plurality home field, mapped to CS+Eng, BGM+Med, PHYS, LIFEENV, SOC (MATHDEC is
  report-only).

## 5. Indices (features over t0-3..t0+2 only)
* PRIMARY OPEN_home = mean of the six signed winsorised z-scores (EXP10 frozen constants `open_constants.home`),
  requiring >= 10 home papers in t0..t0+2 and >= 4 finite components.
* OPEN_all and OPEN_sizematch use their own frozen constants.
* SECONDARY NOVCHURN_home = mean(z(NOV_res_home), -z(edge_persistence_home)) with the same constants; both must be
  finite, plus >= 10 home papers.
* CHENG_consistency (Cheng et al. 2023, exact definition with OpenAlex topics as the terms):
  * for y in {t0+1, t0+2}: c_y[k] = the concept's home papers in year y carrying topic k (SELF topics removed);
    S = {k: c_{y-1}[k] >= 1};
  * cos_y = cosine(c_{y-1}[S], c_y[S]), and 0 if S is empty or c_y[S] is all zero;
  * CHENG_consistency_home = mean(cos_{t0+1}, cos_{t0+2}). `_all` uses all papers.
* CHENG_embeddedness_home = mean pairwise cosine, over the topics co-used in t0+2, in a 200-dim PPMI-SVD embedding of
  the backbone slice of t0+2 (>= 2 neighbours).
* CHENG_prominence_home = count-weighted mean log background frequency of the co-used topics in t0+2.
* Clean variants:
  * ego_density_W3_cz: z vs 200 degree-preserving rewirings of the slice backbone;
  * edge_persistence_sz: size-conditioned pool null, 200 draws;
  * NOVCHURN_home_rare: 10 home papers per early year, 50 draws;
  * edge_persistence_excess: observed minus the mean over 200 year-label permutations;
  * NOVCHURN_clean = mean(z NOV_res_home, -z edge_persistence_sz). z of edge_persistence_sz is standardised by its
    Frame-N mean/sd, a declared exception because no EXP5 constant exists; NOV_res uses its frozen EXP5 constants.

## 6. Rungs
* R0: cont [logvol, growth_c, offhome_share, entropy, reach] + onset-year dummies 2003..2014 (reference 2008;
  window_flag when the extension set is present).
* R1: R0 + CONTACT_REACH.
* R2: R1 + type_method, type_object, type_property, generic. Legacy level dummies are dropped: Frame N has no level.
* R3: R2 + fp_logN, fp_nfields. fp_reemerge and newborn are constant by construction and fp_wiki_pre does not exist, so
  all three are dropped.
* R4: R3 + label_coverage_early, home_coverage_early.
* R5: R4 + home-group FE.
* Constant columns are dropped by the code and logged.

## 7. Outcomes (MATCH grounding = verified title-phrase matches)
* Primary: O2r_m50 over venue codes 1..26 at t0+6..t0+8.
* Also: O2r_m30; O2r_resid = O2r_m50 - (2.7410366547641205 + 0.3966308230599589*logvol); O1c, O1b, O3 (lib/outc);
  V_next = N(t0+3) (Cheng's DV); logN2 = log1p(N(t0+2)).

## 8. Statistics
* psp = partial Spearman: rank-transform, residualise both on the rung covariates, then Pearson.
* 2,000-draw concept bootstrap (percentile CI, seed 20260929, refit per draw).
* A group is estimable at n >= 30. DL pooling over estimable groups with I2. Leave-one-group-out.
* HOLM FAMILY (one-sided bootstrap p):
  * OPEN_home|O2r_m50|R3 (>0)
  * OPEN_home|O2r_m50|R5 (>0)
  * NOVCHURN_home|O2r_m50|R3 (>0)
  * CHENG_consistency_home|O2r_m50|R0 (<0)
  * (OPEN_all - OPEN_home)|O2r_m50|R3 paired (>0)

## 9. Verdict code (unadjusted 95% CIs decide; Holm p reported)
* CONFIRMED iff all of the following hold:
  * CI_low(OPEN_home,R3) > 0;
  * CI_low(OPEN_home,R5) > 0;
  * the group clause holds;
  * CI_low(NOVCHURN_home,R3) > 0.
* Group clause:
  * with 5 estimable groups, psp at R3 is positive in >= 4 of them;
  * with 4 estimable groups, it is positive in 4/4;
  * with <= 3 estimable groups the clause is NOT EVALUABLE and the verdict is capped at PARTIAL.
* PARTIAL iff OPEN_home or NOVCHURN has CI_low > 0 at R3 but some clause fails. NOT CONFIRMED otherwise.
* F4 cap: if the pre-unseal power (psp 0.08, R3 and R5 jointly) is < 0.5, the verdict is capped at PARTIAL.
* REVERSAL CONFIRMED iff Spearman(CHENG_consistency_home, V_next) has CI > 0 AND
  psp(CHENG_consistency_home, O2r_m50 | R0) has CI < 0.
* REVERSAL FAILS-AS-SIZE iff psp(CHENG, V_next | logN2) has a CI that includes 0.
* COUPLING WARNING CONFIRMED iff the paired ALL-HOME difference at R3 has CI > 0 AND psp(n_comm_W3_home, O2r_m50 | R3)
  has a CI that includes 0.
* CONFIRMED_HOLM flag: Holm p < 0.05 for the first three family members.

## 10. Declared fallbacks
* A: if fewer than 800 concepts have finite O2r_m50 AND finite OPEN_home, the primary outcome becomes O2r_m30. This
  is decided from counts only, before any psp.
* E: if the pre-unseal expected primary n is < 800, add the t0 = 2015 extension set.
* Fallbacks F1-F10 of the plan apply as written.
* No subgroup hunting: anything not listed here is labelled EXPLORATORY.
