# Pre-registration: Cheng reach-vs-depth reversal on the selection bodies

Written in S0, 2026-09-29, before any model was fitted and before any consistency value was joined to an outcome.
Its SHA-256 and that of `results/frozen_spec.json` are appended to `logs/seal.log`. Every table produced from this
spec is **selection data, not confirmation**: the outcomes of all bodies were already read by EXP5/EXP8/EXP10. The
consistency measure itself was never screened on any of them.

## Source definitions (Cheng et al. 2023, ASR 88:522-561, Table 2)

The publisher page (journals.sagepub.com/doi/full/10.1177/00031224231166955) returned HTTP 403 to the fetch tool
(`logs/web/cheng_grep.txt`). The text below is copied verbatim from the full-text extract saved by research
artifact art_hSyVUBa2okT2 (`raw/fetch/cheng_all.txt`). Deviation `F6_partial` is logged.

> **Ideational consistency** | For each focal term at time _t_, we focus on its neighbor terms co-used with the focal
> term in the prior year (_t_ – 1), and then compare each neighbor terms' rate of co-usage with the focal term in
> year _t_ – 1 to that observed in year _t_ using cosine similarity. Should all the neighbor terms in _t_ – 1 stop
> being co-used with the term in _t_, the cosine similarity is rendered as 0. Should there be no neighbor terms in
> _t_ – 1 when there are some in _t_, then cosine similarity is again equal to 0.

> **Ideational embeddedness** | For each focal term's neighbor terms at time _t_, we estimate their variation in
> semantic network positioning. We first take the cumulative 10-year semantic network of terms (valued ties by
> number of cooccurrence) and estimate network embeddings using word2vec (200 dimensions). We then take the neighbor
> terms associated with a focal term, and for all pairs of neighbors, we calculate their cosine similarity on these
> dimensional arrays. The average of this measures the degree to which a focal term is used with a set of neighbor
> terms with similar semantic placement (or conversely, used in a neighborhood composed of many distinctive neighbor
> terms, in a cultural hole).

> **Social embeddedness** | For all authors associated with a focal term in year _t_, we estimate their density of
> collaboration with each other (number of observed ties divided by the total possible ties between them) in the
> prior 10 years of the WoS. We ignore papers with more than 15 authors.

> **N published articles** | The number of unique published articles in Web of Science in which an idea is used in
> the future (time _t_ + 1).

Reported effects: consistency b = .43 (+53% per SD), embeddedness b = .22, social embeddedness b = -.16 (-15% per SD).
The model is a multilevel over-dispersed Poisson, fitted in-sample, with no current-volume control.

## Our operationalisation (frozen)

- **Paper sets.** HOME = grounded papers whose venue field is in the concept's frozen home set. ALL = every grounded
  paper. EXP5 frame: Exp11 Pass M rows (TAG rule). 2015-17 cohort: EXP10 passC_early rows with tagstate == 1 (TAG).
- **Neighbours.** OpenAlex topics (4,516) on the concept's papers, excluding the concept's SELF topics (Exp11/EXP8
  `ego.self_topics`, ALL papers over t0..t0+2). So this is *topic co-usage consistency*.
- **v_t[k]** = the number of year-t papers of the concept in the paper set tagged with topic k.
- **CONS(t)** = cosine(v_{t-1}, v_t). It is defined iff both years have >= 3 papers (with >= 1 topic) and
  >= 2 non-self topics; otherwise it is NaN. This differs from Cheng, who sets 0 when t-1 has no neighbours. A
  minimum-support rule is needed because 0/1-heavy cosines on 2-3 topics are functions of degree.
- **CONS_r(t)** (sensitivity) is Cheng's verbatim version: the cosine over the t-1 neighbour support only.
- **EMB(t)** (ANALOGUE, flagged in every table): the co-usage-weighted (v_k v_l) mean positive backbone PMI over
  pairs of the top-20 year-t neighbours, on EXP3 slice s(t) (years >= 2015 use slice 2). Pairs without a backbone
  edge count as 0. **EMB_cos(t)** (exploratory): the unweighted mean pairwise cosine of the neighbours' backbone PMI
  rows. It is a second-order similarity, closer to Cheng's embedding cosine.
- **SOC(t)**: nodes are the distinct authors on the concept's year-t papers in the paper set (papers with
  <= 15 authors). If there are more than 200, a seeded random subset of 200 is used. An edge means the two authors
  co-authored any concept paper (any field, <= 15 authors) in t-10..t-1. NaN if < 3 authors. Author ids are
  OpenAlex-disambiguated, and ties come only from the concept's own papers (a narrower tie set than Cheng's WoS
  co-author network).
- **V(t)** = the TAG-grounded (tagstate == 1) yearly count, all fields, from EXP5 scan/agg_counts. It is checked
  against Exp11 counts_m summed over vfield. If fewer than 99% of the checked cells match exactly, counts_m is used
  for EXP5 (F3). Cohort V(t0+3) = the sum of the EXP10 sealed parts at year t0+3 with tagstate == 1 (EXP10 s3
  decision = TAG). It is read directly; seal2.unseal() is not called.
- **Static early trait:** CONS_early = mean(CONS(t0+1), CONS(t0+2)) (the mean of the defined values). The same
  rule is used for EMB_early, SOC_early, CONS_early_all and CONS_r_early.

## Tests

- **A (Cheng replication panel, EXP5, t0+1 <= t <= min(t0+10, 2021)).**
  - A1: PPML V(t+1) ~ z CONS(t) + z EMB(t) + z SOC(t) | age + year, CRV1 by concept.
  - A1-NB: negative binomial with age and year dummies.
  - A2: A1 + log1p V(t).
  - A3: A2 | ci + year.
  - Each is fitted on HOME and ALL, on SOC-complete rows and CONS-only.
  - RATIO = b_A2 / b_A1 (CONS), from a 500-draw concept-cluster bootstrap that uses the same draws for A1 and A2.
  - Per body and per group, DL-pooled.
- **B (static early trait, per body; PRIMARY = EXP5 pooled with body dummies; REPLICATION = COHORT_2015_17).**
  - B-raw: Spearman(CONS_early_home, V(t0+3)).
  - B-size: psp | log V(t0+2).
  - B-depth: psp with O1c, O1b, O3 | B5 + onset-year dummies (+ group and body dummies where pooled).
  - B-reach: psp with O2r_m50 and O2r_resid | same.
  - 2,000 concept-bootstrap refits, seed 20260929.
  - DL over the 5 groups.
  - Paired diff psp(O1c) - psp(O2r_m50) on the same draws, using the common complete-case set.
  - Cohort rungs R2/R3 (EXP10).
- **C (within-panel, EXP5).**
  - C1: fepois entries(t+1) ~ z CONS_home(t) + log1p n_home + log1p n_all + log1p deg + log at_risk | ci + year.
  - C2: feols dHomeShare(t+1) ~ same.
  - 500-draw concept-cluster bootstrap.
- **D (Palla).** OLS on ranks, O3 / O2r_m50 ~ rank CONS_early + rank log early vol + product + B5 + onset-year dummies.
  Also psp by early-size tercile.
- **E (coupling).** Paired bootstrap of psp(CONS_early_all) - psp(CONS_early_home) on O2r_m50 and O1c.

## Predictions

- **P1:** raw Spearman(CONS_early_home, V(t0+3)) > 0, and A1 b > 0 on HOME.
- **P2:** RATIO A2/A1 < 0.5.
- **P3:** psp(CONS_early_home, O2r_m50 | B5) < 0.
- **P4:** psp(CONS_early_home, O3 | B5) <= 0.
- **P5:** psp(O1c) - psp(O2r_m50) > 0.
- **P6:** C1 b < 0.

Holm family: {P1-A1, P2, P3, P4, P5}, on the PRIMARY body, one-sided in the predicted direction.

## Verdict rules (written mechanically to results/cheng_verdict.json)

- **REVERSAL CONFIRMED (on selection data)** iff P1 raw rho > 0 with CI > 0 AND P3 psp < 0 with CI < 0 on the
  PRIMARY body.
- **REVERSAL REPLICATED** iff the same holds on COHORT_2015_17. CI < 0 is not required if n < 600; the MDE is
  reported.
- **SIZE-DOMINATED** iff the upper bound of the A2/A1 ratio CI is < 0.5.
- **DEPTH-REACH SPLIT** iff the P5 CI is > 0.
- **NULL-REVERSAL** iff the P3 CI includes 0. Everything else is EXPLORATORY. No post-hoc subgroup claims.
