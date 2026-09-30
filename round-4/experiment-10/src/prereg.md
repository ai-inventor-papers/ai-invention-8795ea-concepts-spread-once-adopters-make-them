# Pre-registration — fresh-cohort test of the OPEN (open-neighbourhood) claim (RQ1)

Written at S0 (2026-09-29, before any cohort outcome exists on disk). Its sha256, together with that of
`results/frozen_spec_v0.json`, is appended to `logs/seal.log`. Everything below is applied mechanically in code.

## Units and data
* Unit of analysis and resampling unit: the **concept** (OpenAlex legacy concept, EXP5 frozen lexicon `lexicon_v1`).
* Selection data: the 12,499-concept EXP5 frame (onsets 2003-2014), with EXP8 features/outcomes. Nothing in the
  cohort's outcome window is read before the seal.
* Confirmation data: the 2015-2016 onset cohort (EXP5 onset rule with the t0 range moved to 2015-2017; early volume
  (t0..t0+2) >= 30 grounded works; home rule on the first 30 venue-labelled grounded works capped at t0+2; diffuse-born
  dropped; LLM per-concept precision gate >= 0.8, EXP5 prompt/model/procedure). 2017 onsets are fallback rows.
* Grounding of features: TAG (legacy concept tag score >= 0.3 on a verified title match), identical to EXP5/EXP8.

## OPEN (frozen definition)
OPEN_b = mean over available k of s_k * (w_k(x_k) - mu_{k,b}) / sd_{k,b}, where
k in {new_edge_rate (+), n_comm_W3 (+), participation (+), NOV_res (+), ego_density_W3 (-), edge_persistence (-)};
w_k = winsorisation at the EXP5-frame 0.5 / 99.5 percentiles of build b; mu/sd = mean/sd of the winsorised component
on the EXP5 frame for build b (all 12,499 concepts, finite values). OPEN is NaN unless >= 4 of the 6 are finite.
Components are the EXP8 `lib/ego.concept_core` definitions (windows PRE = t0-3..t0-1, W1 = t0, W2 = t0+1,
W3 = t0+2; backbone slice for years > 2014 = slice 2010-14, which is pre-onset for the cohort), computed with
`n_null = 0` and `compute_btw = False` (neither is used by the six components).

Builds:
* **ALL**: every grounded early paper (EXP8 definition).
* **HOME** (primary): only grounded papers whose venue field is in the concept's home set, in BOTH the PRE window and
  W1-W3; venue-unlabelled papers are dropped. OPEN_home = NaN if fewer than 10 home papers in t0..t0+2
  (EXP5-frame sensitivity at 5 and 20).
* **SIZEMATCH**: 20 seeded random subsamples (seed = 1000 + ci) of the concept's grounded early papers, each window
  (PRE, W1, W2, W3) subsampled without replacement to that window's HOME paper count; each component averaged over
  the 20 draws, then winsorised/z-scored with SIZEMATCH constants. NaN under the same >= 10 rule.

## Outcomes
* Primary: **O2r_m50** = exact hypergeometric rarefied venue-field richness among 50 grounded, venue-labelled
  concept papers in t0+6..t0+8 (NaN if < 50 labelled papers). Co-outcome: **O2r_resid** = O2r_m50 - (a + b logvol)
  with EXP8's frozen DEV fit (a = 2.7410, b = 0.3966), or the MATCH-refit constants if S3 selects MATCH.
* Secondary: O1c, O1b, O3 (EXP8/EXP5 definitions, windows as frozen); O4 is NOT computed (no citation pass).
* Outcome grounding (S3, decided outcome-blind before the seal): TAG if
  min_{y in 2021..2024} tag_rate[y] / mean(tag_rate[2017..2019]) >= 0.90 AND the same holds for the 300-control
  TAG/title-match ratio; otherwise MATCH (verified title-match hits of all tagstates) for all outcome years, valid only
  if Spearman(O2r_m50_MATCH, O2r_m50_TAG) >= 0.90 on the EXP5 frame; otherwise the primary becomes the 2015-onset
  TAG window t0+5..t0+7 (<= 2022) and the full cohort is secondary. The <= 2022 TAG window for 2015 onsets is always
  reported as a sensitivity.

## Ladder (covariates; partial Spearman = Pearson of rank residuals; ranks of continuous covariates, dummies raw)
* R0 = B5 (logvol, growth_c, offhome_share, entropy, reach) + onset-year dummies (+ window flag if 2017 is added)
* R1 = R0 + CONTACT_REACH
* R2 = R1 + type dummies (method/object/property; topic = reference; 'unlabelled' its own dummy) + generic flag
  + legacy-level dummies
* R3 = R2 + fp_logN, fp_nfields, fp_reemerge, fp_wiki_pre, newborn
* R4 = R3 + venue-label coverage share (early) + home-paper coverage share (early)
* R5 = R4 + home-group dummies
95% CI: 2,000 concept bootstraps (percentile), refitting the residualisation in every draw; seed 20260929.

## Groups
CS+Eng, BGM+Med, PHYS, LIFEENV, SOC (MATHDEC reported only). Per group at R2 and R3: psp, bootstrap SE,
DerSimonian-Laird pooled estimate, tau2, I2, sign count.

## Verdict (applied in code, written to results/cohort_result.json)
CONFIRMED iff all of:
1. OPEN_home psp on O2r_m50 > 0 with 95% CI > 0 at R2 AND at R3;
2. O2r_resid has the same (positive) sign at R2;
3. positive point estimate in >= 4 of the 5 groups at R2;
4. psp > 0 within method AND within object concepts (R3 minus the type dummies);
5. RETENTION_RATIO_early psp < 0 given R0 (O2r_m50).
DISCONFIRMED iff the 95% CI of OPEN_home at R2 includes 0. Otherwise PARTIAL, with the failing clauses listed.
Named readings: (a) 'type absorbs OPEN' = R1 CI > 0 but R2 CI includes 0; (b) 'mechanical' = OPEN_home CI includes 0
while OPEN_all CI > 0, then SIZEMATCH decides between paper count and home restriction.
Anything not listed here is EXPLORATORY.

## Holm family (8 tests, one-sided bootstrap p in the frozen direction, at R2)
{OPEN_home, OPEN_all, OPEN_sizematch, RETENTION_RATIO_early} x {O2r_m50, O2r_resid}; frozen directions: OPEN +,
RETENTION_RATIO_early -.

## Power / extension trigger (decided before the seal)
Power = P(95% CI > 0 at R2) for pooled OPEN_home psp, from 1,000 subsamples of the EXP5 frame with the realised cohort
n and group mix, assuming the true effect is HALF the EXP5 selection estimate. If the cohort n (finite OPEN_home and
O2r-eligible expectation not used; n = gate-passing 2015-16 concepts) < 800 OR power < 0.80, the gate-passing 2017
candidates are added (outcome window t0+5..t0+7 = 2022-2024; window flag as covariate).

## Concept TYPE
LLM label (google/gemini-2.5-flash-lite, temperature 0, 20 concepts per call) in {method, object, property, topic} +
generic flag. Benchmark: 300 concepts double-labelled by openai/gpt-4.1-mini; 60 read by the executor agent blind to
model labels. Gate: M1 precision >= 0.85 for method AND object on the 60; one prompt revision allowed; then fall back to
M1 = M2 agreement for within-type tests.

## Drop order if late
Learned-model replications -> 2017 extension (unless required) -> SIZEMATCH for the cohort. Never dropped: HOME build,
TYPE rung, the S3 decision, the single unseal.
