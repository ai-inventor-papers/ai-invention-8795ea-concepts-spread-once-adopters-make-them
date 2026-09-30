# Do temporal network signals predict how scientific concepts spread across disciplines?

This report is the chronological record of a study that tests whether temporal changes in the structure of scientific knowledge networks can anticipate the emergence and cross-disciplinary integration of new scientific concepts. The study compares three families of candidate network indicators against a baseline of simple popularity and reach measures, evaluated on a panel of 46 to 48 concepts across four home-field groups (Biochemistry/Genetics, Computer Science, Engineering, Medicine) with onset years 2003 to 2009.

The primary outcome is rarefied field breadth (O2r), the expected number of distinct disciplines among a fixed-size random draw of a concept's papers in years t0+6 to t0+8. This outcome separates size-adjusted breadth from sheer volume. Secondary outcomes include sustained uptake and transience. Evaluation uses leave-one-group-out (LOGO) ridge regression with 2,000 stratified concept-level bootstraps, so that an indicator's incremental value (delta-rho or delta-AUC) is always measured on concepts from a home field the model has never seen.

Three candidate indicators are tested, each representing a different theory of how concepts spread:

- **Candidate L** (naturalisation gap, A\*_h): a background-adjusted disciplinary self-citation index on the concept's lineage network, drawn from the epidemiological negative-control design [ARTIFACT:art_xp8BGBJZsxeI].
- **Candidate D** (structural diversity of co-occurrence ties): the number of distinct Leiden communities a concept's new neighbours reach on a corpus-wide topic co-occurrence backbone [ARTIFACT:art_yrradSC27HtQ].
- **Candidate G** (gateway landing): the eigenvector centrality of the adopting fields on a topic co-assignment backbone, weighted by early off-home share [ARTIFACT:art_33_KKk_G8Gw5].

---

# Iteration 1

## 1. Strategy

The hypothesis predicts that a new concept spreads durably across disciplines when the fields that adopt it begin citing the concept's literature the way they cite their own literature, rather than reaching back to the concept's home field. The predicted signal is the "naturalisation gap" A\*_h: the log odds ratio of the concept's citing-layer-by-cited-layer mixing table (off-home versus home), minus the same log odds ratio computed on the same citing papers' non-concept references. A negative value means adopters still import the concept across field lines more than their general citing habits predict; a value near or above zero means the concept's lineage follows the adopters' own field boundaries.

Two alternative hypotheses compete. The first is that the structural diversity of co-occurrence ties matters: concepts that acquire neighbours in many different Leiden communities on a corpus-wide backbone will spread more broadly, following complex-contagion theory [1, 2]. The second is that what matters is where a concept lands: concepts adopted early by high-centrality "gateway" fields on a topic-relatedness backbone will spread, following the principle of relatedness from economic complexity [3].

All three candidates are tested against a shared five-feature baseline: log early volume, publication growth, off-home share, Shannon entropy and field reach, all computed over the first five years from onset. The shared evaluation protocol defines onset, outcomes and panel membership across all three experiments. The pre-registered decision rule requires delta-rho >= 0.10 with 90% bootstrap CI excluding zero, the same sign in at least three of four home-field groups, split-half reliability >= 0.60 and absolute Spearman with log volume and growth <= 0.60.

## 2. Data infrastructure and deviations

The shared OpenAlex credit pool (10,000 daily credits, split across five artifacts) was exhausted partway through iteration 1. This forced a data deviation that affects all three experiments:

- **Yearly counts** (for onset, sustained uptake, transience, volume and growth) come from OpenAlex group-by calls and follow the shared evaluation protocol exactly for all 78 panel concepts.
- **Field labels, concept papers and citation lineage** come from Semantic Scholar, a free source. Semantic Scholar's field assignments use a 23-field text-classifier taxonomy (s2-fos), which is concept-independent (it reads titles and abstracts, not references). The 23-field Semantic Scholar taxonomy was mapped to the 26-field OpenAlex scheme for the experiments that require venue labels.
- **Background references** come from free OpenAlex singleton GET calls (verified zero-credit via response headers).
- **Agreement between sources** on the 11 concepts where both sources have full data: Spearman correlation of rarefied breadth between outcomes labelled by Semantic Scholar and outcomes labelled by OpenAlex is 0.87.

The panel comprises 78 concepts with onset years 2003 to 2014, of which 46 to 48 fall in the dev window (onset 2003 to 2009, home field in one of the four groups). The exact number varies by experiment because each has slightly different eligibility filters.

## 3. Experiment 1: Does the naturalisation gap predict cross-field spread? [ARTIFACT:art_xp8BGBJZsxeI]

### 3.1 Construction

For each concept, the analysis downloads up to 25,000 phrase-matched papers and their citation lists. A concept lineage link is a citation from a concept-paper to an earlier concept-paper within three years. Links between papers that share an author are removed from the main estimator (self-lineage share ranged from 5% to 39% across concepts). The naturalisation gap A\*_h is the Mantel-Haenszel pooled log odds ratio (a stratum-weighted average across yearly mixing tables) of the off-home/home mixing table for concept citations, minus the same log odds ratio for the same citing papers' non-concept references (the background term). The background term absorbs the adopters' general disciplinary homophily without modelling it.

Field labels for the lineage analysis come from Semantic Scholar's fractional field-of-study classifier. Home field is defined as the field(s) holding at least 40% of a concept's first 30 grounded papers. Concepts whose Semantic Scholar home field falls outside the four dev groups (Computer Science, Engineering, Biology, Medicine) are dropped ("sealed"), leaving 48 dev concepts (Biochemistry/Genetics 13, Computer Science 21, Engineering 3, Medicine 11).

### 3.2 Measurement result: background homophily dominates lineage

The first finding is the background-homophily measurement result, which was predicted by the 8-concept probe. Among all 48 dev concepts, 100% have a positive background log odds ratio: every field's citing papers preferentially cite their own field's literature above chance. The coefficient of determination (R-squared) of the raw concept lineage log odds ratio on the background log odds ratio is 0.66 (90% CI [0.39, 0.83]), with Spearman correlation 0.70.

We define "lineage autonomy" as the degree to which a concept's citation chains stay within adopters' own disciplines rather than reaching back to the home field. Two-thirds of the between-concept variance in this raw lineage autonomy is explained by which fields adopt the concept and how insular those fields are in general. Uniform-null lineage indicators (including the study's own earlier A\* and naive R_away) are therefore largely measures of field composition, not concept-specific rooting. This is the background-homophily measurement result.

| Statistic | Value | 90% CI |
|---|---|---|
| R-squared of raw lineage LOR on background LOR | 0.66 | [0.39, 0.83] |
| Spearman of raw lineage LOR with background LOR | 0.70 | - |
| Share of concepts with positive background LOR | 100% (48/48) | - |
| Share where background >= raw lineage LOR | 77% (37/48) | - |

[FIGURE:fig_m1_scatter]

### 3.3 Predictive screen: A\*_h does not survive

The naturalisation gap A\*_h was tested as a predictor of rarefied breadth (O2r, m = 30) in LOGO ridge regression. The five-feature baseline alone reaches rho = 0.834 with rarefied breadth. Adding A\*_h produces delta-rho = -0.006 (90% CI [-0.034, 0.017]). A\*_h fails the pre-registered rule on all three testable clauses:

| Clause | Required | Observed | Pass? |
|---|---|---|---|
| Delta-rho >= 0.10 and CI low > 0 | >= 0.10 | -0.006, CI [-0.034, 0.017] | No |
| Positive in >= 3 of 4 groups | >= 3 | 0 of 4 (Bio 0.00, CS -0.003, Eng insufficient, Med 0.00) | No |
| Split-half reliability (Spearman-Brown) | >= 0.60 | 0.58 | No |
| Abs Spearman with log volume and growth | <= 0.60 | 0.14 (volume), 0.18 (growth) | Yes |

The size-independence clause passes: A\*_h is not a proxy for concept volume or growth. But the gap adds nothing to the baseline on held-out fields, and it is not measured reliably enough (split-half r_SB = 0.58, just below the bar).

### 3.4 Within-field heterogeneity and reliability gradient

A\*_h's sign flips across fields. The median A\*_h in Medicine is +0.45 (naturalised), while in Computer Science it is -0.18 (borrowed). This within-field heterogeneity means A\*_h is partly a field-composition indicator itself, despite the background adjustment.

Reliability depends on sample size. Concepts with fewer than 60 off-home children have split-half reliability below 0.40, while the 11 concepts with 60 or more off-home children reach r_SB = 0.72. On those 11 concepts, the eligible-subset delta-rho is +0.118 (90% CI [0.00, 0.36]), but this is too underpowered to interpret.

| Off-home children bin | N concepts | Split-half r | Spearman-Brown |
|---|---|---|---|
| 0-15 | 21 | 0.24 | 0.34 |
| 15-30 | 9 | 0.32 | 0.37 |
| 30-60 | 7 | 0.14 | 0.04 |
| 60+ | 11 | 0.57 | 0.72 |

### 3.5 Alternative lineage indicators

None of the 14 candidate and foil features scored as exploratory candidates beat the five-feature baseline. The full candidate comparison table:

| Indicator | Delta-rho | 90% CI | Groups + | r_SB | rho(vol) | rho(growth) |
|---|---|---|---|---|---|---|
| A\*_h (primary) | -0.006 | [-0.034, 0.017] | 0/4 | 0.58 | 0.14 | 0.18 |
| A\*_h (Mantel-Haenszel) | +0.016 | [-0.005, 0.042] | 2/4 | 0.76 | 0.07 | 0.08 |
| A\*_h (unadjusted) | +0.015 | [-0.002, 0.037] | 2/4 | 0.74 | 0.17 | 0.42 |
| A\*_h (crude, no bg) | +0.012 | [-0.016, 0.040] | 1/4 | 0.72 | 0.05 | 0.10 |
| Naturalised field count | +0.002 | [-0.030, 0.036] | 1/4 | 0.71 | 0.33 | 0.37 |
| Max field-level rho\* | -0.013 | [-0.038, 0.009] | 0/4 | 0.74 | 0.37 | 0.22 |
| Background LOR | -0.004 | [-0.060, 0.039] | 2/4 | 0.91 | 0.05 | 0.04 |
| Raw lineage LOR | +0.000 | [-0.008, 0.009] | 0/4 | - | 0.16 | 0.02 |
| A\*_unif | -0.011 | [-0.052, 0.022] | 1/4 | - | 0.02 | 0.17 |
| A\*_imp | -0.003 | [-0.043, 0.029] | 1/4 | - | 0.05 | 0.20 |
| Relay share | -0.012 | [-0.051, 0.021] | 0/4 | - | 0.02 | 0.00 |
| Self-lineage share | +0.028 | [-0.005, 0.065] | 1/4 | - | 0.18 | 0.37 |
| Coverage | +0.008 | [-0.003, 0.023] | 1/4 | - | 0.31 | 0.36 |
| R_away | -0.025 | [-0.060, 0.007] | 1/4 | - | 0.01 | 0.16 |

The Mantel-Haenszel pooled variant (A\*_h MH) comes closest, with delta-rho +0.016 and two groups positive, but still does not pass the decision rule. The background log odds ratio itself, which measures adopters' general disciplinary insularity, has the highest reliability (r_SB = 0.91) but no predictive gain.

### 3.6 Secondary outcomes

For sustained uptake, adding A\*_h to the five-feature baseline gives delta-AUC = -0.026 (90% CI [-0.084, 0.028]): no gain. Transience is not evaluable because only 4 of 48 concepts are transient, and all four are in Medicine.

### 3.7 Field-level prediction

At the field level (367 concept-by-off-home-field units, predicting field retention R_j), adding the field-level rho\*_cj to the baseline gives delta-AUC = +0.002 (90% CI [-0.011, 0.016]): no gain.

### 3.8 Variance decomposition (REML)

A crossed random-effects model (concept and concept-by-field) fitted by REML on 190 cells gives estimated standard deviations tau_c = 0.29 (between-concept) and tau_cj = 0.65 (concept-by-field). The concept-by-field variance is more than twice the between-concept variance, confirming that naturalisation is field-specific rather than a concept-level trait. A PyMC NUTS sampler check agrees with REML to Spearman 0.9996.

### 3.9 Audit

An independent re-derivation confirms delta-rho, baseline rho, the size correlations, sustained-uptake delta-AUC and the background-homophily result exactly. Field-level delta-AUC is re-derived at 0.0020. A shuffled-A\*_h placebo passes 0 of 200 times, confirming that the null result is not an artefact of the evaluation protocol.

**Power caveat.** With the baseline at rho = 0.83, a feature needs Spearman of approximately 0.95 or more with rarefied breadth to achieve the delta >= 0.10 clause. The ceiling for any single indicator is therefore very close when the baseline is this strong.

---

## 4. Experiment 3: Do diverse topic ties predict concept spread? [ARTIFACT:art_yrradSC27HtQ]

### 4.1 Construction

This experiment builds a full-corpus topic co-occurrence backbone from the 2026-09-23 OpenAlex bulk data snapshot (476 million works). For each of three time slices (2000 to 2004, 2005 to 2009, 2010 to 2014), topic co-assignment PMI is computed over all works. Leiden community detection (gamma = 3) produces 25, 26 and 23 communities across the three slices (the plan's rule of approximately 8 communities was not achievable; this deviation is documented).

For each concept, the analysis tracks which topics co-occur with it through title-matched works (median 48% of API volume; Spearman 0.88 with API counts). The primary candidate D_ratio is the ratio of distinct Leiden communities reached by the concept's new co-occurrence neighbours to the total number of new neighbours. D_z, the literal plan primary, was superseded because it failed the size-independence diagnostic (Spearman with log volume = -0.63).

The panel comprises 47 dev concepts (Biochemistry/Genetics 16, Computer Science 12, Medicine 10, Engineering 9).

### 4.2 Screen results

The five-feature baseline alone reaches rho = 0.770 with rarefied breadth. Neither candidate survives the pre-registered rule:

| Candidate | Delta-rho | 90% CI | Groups + | r_SB | rho(vol) | rho(growth) | Survives? |
|---|---|---|---|---|---|---|---|
| D_ratio (primary D) | +0.006 | [-0.092, 0.135] | 3/4 | 0.83 | 0.11 | 0.02 | No |
| F_res (disciplinary) | -0.060 | [-0.158, 0.014] | 1/4 | 0.44 | 0.04 | 0.09 | No |
| D_z (plan literal, superseded) | +0.017 | [-0.101, 0.087] | 4/4 | 0.90 | -0.63 | 0.09 | No (size) |

D_ratio passes the reliability and size-independence clauses. It is positive in 3 of 4 groups, but its delta-rho of +0.006 is far from the 0.10 threshold. F_res (frequency residualised by the baseline) has low reliability (r_SB = 0.44) and is negative in 3 of 4 groups.

### 4.3 Portability: which indicators associate with rarefied breadth across all groups?

Several co-occurrence indicators have within-group Spearman correlations with rarefied breadth in the range 0.45 to 0.63 across all four home-field groups: D_ratio, D_rare (rarefied community diversity), participation coefficient and neighbourhood novelty (NOV_res). All are redundant under delta-rho: none adds to the five-feature baseline.

In contrast, degree growth, strength growth and new-edge growth are associated with rarefied breadth only in Computer Science (within-group rho 0.45 to 0.47) and negatively or near zero in the other three groups. This is reported as a negative result: raw co-occurrence growth indicators are domain-specific.

[FIGURE:fig_portability]

### 4.4 Exploratory partial association

An exploratory (not pre-registered) analysis computes the out-of-group partial Spearman of each candidate with rarefied breadth, after residualising both on the five-feature baseline:

| Indicator | Partial rho | 90% CI | Permutation p |
|---|---|---|---|
| D_ratio | 0.335 | [0.019, 0.648] | 0.037 |
| D_rare | 0.311 | [-0.034, 0.653] | - |
| Participation | 0.322 | [-0.037, 0.640] | - |
| NOV_res | 0.281 | [-0.114, 0.581] | - |
| F_res | -0.267 | [-0.443, 0.249] | - |

D_ratio's partial correlation of 0.34 with rarefied breadth, conditional on the five-feature baseline, is positive and significant by permutation (p = 0.037). The formal delta-rho test is near its ceiling because the baseline is already very strong (rho = 0.77), so a genuine partial association can exist even though the incremental prediction is small.

### 4.5 Secondary outcomes

For sustained uptake, D_ratio gives delta-AUC = -0.005 (90% CI [-0.060, 0.036]): no gain. Transience is not estimable because all transient concepts in this panel are in Medicine. Dissociation tests between breadth and uptake are inconclusive.

### 4.6 Audit

All headline numbers (delta-rho, CI, per-group deltas, portability rho values) are re-derived exactly by an independent re-derivation. A shuffled placebo of the full screen fails; a planted control with a known-predictive synthetic feature passes.

---

## 5. Experiment 4: Where a concept lands early vs. how broadly it spreads [ARTIFACT:art_33_KKk_G8Gw5]

### 5.1 Construction

This experiment asks whether early adoption by high-centrality "gateway" fields on a topic-relatedness backbone predicts breadth. The backbone is a 26-field positive-PMI topic co-assignment graph from 1998 to 2002. Gateway centrality G is the share-weighted eigenvector centrality of the venue fields adopting a concept in t0 to t0+2.

This artifact also produces the authoritative shared outcome tables: outcomes.csv (all 78 rows), field_outcomes.csv (80 concept-by-off-home-field retention rows), features.csv and single_indicators.csv.

The panel comprises 46 dev concepts (34 with an outcome-window rarefied breadth score). The credit floor was hit after 286 credits, so t0+3 to t0+4 labels are missing (the baseline's label-based features use t0 to t0+2 only), and outcome windows keep only the top-200 sources (29 of 34 concepts are truncated).

### 5.2 Concept-level screen

Gateway centrality was tested against the five-feature baseline on rarefied breadth (m = 30):

| Candidate | Delta-rho | 90% CI | Groups + | r_SB | rho(vol) | rho(growth) | Survives? |
|---|---|---|---|---|---|---|---|
| G (eigenvector gateway) | +0.033 | [-0.095, 0.168] | 2/4 | 0.92 | 0.11 | 0.13 | No |

Gateway centrality does not survive the pre-registered rule: delta-rho is +0.033 (below 0.10), positive in only 2 of 4 groups (Engineering +0.071, Biochemistry +0.067; Computer Science -0.230, Medicine -0.048), and the CI includes zero. However, reliability is high (r_SB = 0.92) and the size check passes.

### 5.3 Secondary results: volume-residualised breadth and uptake

When rarefied breadth is residualised on log volume, the story changes. G's delta-rho rises to +0.15 (90% CI [0.000, 0.321]), positive in 4 of 4 groups. This is an exploratory finding: gateway centrality adds information about breadth conditional on size, but not on raw breadth.

For sustained uptake, gateway centrality gives delta-AUC = +0.072 (90% CI [0.00, 0.16]), positive in 3 of 4 groups. This is the strongest secondary signal in the iteration, though it was not the pre-registered primary.

### 5.4 Field-level prediction: gateway centrality of the adopting field

At the field level (80 concept-by-off-home-field rows), the adopting field's own gateway centrality adds delta-AUC = +0.10 (95% CI [0.03, 0.17]) for retention. This survives a field-size control: with log field size in the baseline, the gateway centrality delta-AUC is +0.10 (95% CI [0.04, 0.16]). In Computer Science, however, the gateway signal is absent (delta-AUC negative), making this a three-group result.

| Field-level model | AUC_base | AUC_cand | Delta-AUC | 95% CI |
|---|---|---|---|---|
| B5 + gateway_j | 0.705 | 0.808 | +0.103 | [0.034, 0.167] |
| B5 + size + gateway_j | 0.697 | 0.799 | +0.102 | [0.029, 0.173] |
| B5 + all_four (G, REL, RS, G_all) | 0.697 | 0.782 | +0.085 | [0.004, 0.164] |
| B5 + density_j | 0.705 | 0.727 | +0.022 | [-0.031, 0.082] |
| B5 + relatedness_to_home_j | 0.705 | 0.705 | -0.000 | [-0.045, 0.035] |
| B5 + log_field_size | 0.705 | 0.697 | -0.009 | [-0.042, 0.021] |

Gateway centrality is the strongest field-level predictor of retention. Relatedness density (from economic complexity) adds only delta-AUC = +0.022, and field size is uninformative.

### 5.5 Predicting the next field entered

For predicting which field a concept enters next (conditional logit), relatedness density (AUC = 0.61) beats a permutation null (p = 0.023) but is dominated by log field size (AUC = 0.74). In a conditional logit with both, density still adds signal.

### 5.6 Sensitivity analyses

The newborn-only sensitivity (n = 28) reverses the sign of G's delta-rho (-0.061), but the sample is too small for LOGO. Among gateway variants, G_btw (betweenness-based gateway) gives the largest point estimate (+0.092) but with a wide CI and only 1 of 4 groups positive. G_A (authority-based) is the most consistent (3 of 4 groups positive, delta = +0.033).

---

## 6. Comparison across experiments

### 6.1 Shared baseline strength

Across all three experiments, the five-feature baseline (log volume, growth, off-home share, entropy, reach) achieves Spearman correlations of 0.77 to 0.83 with rarefied breadth. This is a high ceiling. Among all indicators tested, entropy alone (Spearman 0.70 with rarefied breadth, positive in all four groups) approaches the baseline's full predictive power. Off-home share (Spearman 0.42), participation (0.51) and number of reached fields (0.53) are the next strongest single predictors.

### 6.2 The decisive table: no candidate passes

| Candidate | Experiment | Theory | Delta-rho | 90% CI | Groups + | r_SB | Survives? |
|---|---|---|---|---|---|---|---|
| A\*_h (naturalisation gap) | 1 | Lineage assortativity | -0.006 | [-0.034, 0.017] | 0/4 | 0.58 | No |
| D_ratio (structural diversity) | 3 | Co-occurrence community | +0.006 | [-0.092, 0.135] | 3/4 | 0.83 | No |
| G (gateway centrality) | 4 | Field relatedness | +0.033 | [-0.095, 0.168] | 2/4 | 0.92 | No |

None of the three theory-driven network indicators adds incrementally to the simple baseline on held-out home fields for predicting cross-disciplinary breadth.

[FIGURE:fig_delta_rho]

### 6.3 What worked where

Despite the null at the concept level, three findings survive:

1. **Background-homophily measurement:** Background homophily explains 66% of between-concept variance in raw lineage autonomy. This is a methodological finding: uniform-null indices conflate field composition with concept-specific integration.

2. **Field-level gateway effect:** The adopting field's gateway centrality on the topic backbone adds delta-AUC = +0.10 for retention, surviving a size control. This is a field-level, not concept-level, result: whether a specific off-home field retains a concept is partly predicted by that field's centrality in the field-relatedness network.

3. **Exploratory partial association of D_ratio:** The structural diversity of co-occurrence ties has a partial Spearman of 0.34 with rarefied breadth conditional on the five-feature baseline (permutation p = 0.037). The signal exists but is absorbed by the baseline in the incremental test.

---

## 7. Dead ends and negative results

1. **A\*_h as a concept-level predictor.** The naturalisation gap does not add to simple reach and entropy for predicting breadth. The measurement is too noisy below 60 off-home children, and the concept-by-field variance is twice the concept-level variance, meaning naturalisation is a local, field-specific process rather than a concept-level trait.

2. **D_z (z-scored structural diversity).** Failed the size diagnostic (Spearman with log volume = -0.63) and was replaced by D_ratio.

3. **F_res (frequency-residualised field-reach growth).** Negative in 3 of 4 groups, low reliability (r_SB = 0.44), delta-rho = -0.060. Residualising reach on the baseline destroys the signal.

4. **Raw co-occurrence growth indicators.** Degree growth, strength growth and new-edge-rate growth are specific to Computer Science: positively correlated with rarefied breadth in Computer Science (rho 0.45 to 0.47) and near zero or negative in the other three groups. They are growth-confounded (Spearman with publication growth > 0.70).

5. **Transience** is not evaluable in this panel. Only 4 of 48 (experiment 1) or 4 of 47 (experiment 3) concepts are transient, and all are in Medicine. The predicted dissociation between breadth and transience cannot be tested.

6. **Insularity and paper-level label bias.** The credit floor prevented computation of field-level insularity and the paper-level label-bias check.

---

## 8. What we have learned so far

Three theory-driven network indicators were tested on a dev panel of 46 to 48 new scientific concepts (onset 2003 to 2009, four home-field groups) against a five-feature baseline of popularity and reach. None passes the pre-registered decision rule for predicting size-adjusted cross-disciplinary breadth at t0+6 to t0+8. The baseline (log volume, growth, off-home share, entropy, reach) is strong (rho 0.77 to 0.83 with rarefied breadth), and the ceiling for incremental gain is narrow.

The main findings from iteration 1 are:

- **Background-homophily measurement (confirmed):** Two-thirds of the between-concept variance in raw lineage assortativity is general disciplinary homophily, not concept-specific. Cross-field indices based on citation patterns must adjust for background homophily to measure anything specific to the concept.
- **Field-level gateway effect (new):** Whether an off-home field retains a concept is predicted by that field's eigenvector centrality on the topic-relatedness backbone, with delta-AUC +0.10 (95% CI [0.03, 0.17]), surviving a field-size control. This is a field-level, not concept-level, finding.
- **Partial association of structural diversity (exploratory):** D_ratio has a partial Spearman of 0.34 with breadth after removing the baseline (permutation p = 0.037). The signal is real but absorbed in the incremental test.
- **Domain-specific indicators (negative result):** Raw co-occurrence growth indicators work only in Computer Science and fail to generalise.
- **Naturalisation is field-specific:** The concept-by-field variance of A\*_h (tau_cj = 0.65) exceeds the concept-level variance (tau_c = 0.29). A concept can be naturalised in one field and borrowed in another.

The three candidates are carried forward in rank order: D_ratio (most portable, passes reliability and 3/4 groups), G (highest delta-rho, but only 2/4 groups), A\*_h (fails). Iteration 2 should consider (a) whether an ensemble or interaction of the three improves on the five-feature baseline, (b) expanding the panel to held-out fields and cohorts, and (c) the trajectory analysis once the indicators are frozen.

---

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

[12] Hawkes, A. G. (1971). Spectra of some self-exciting and mutually exciting point processes. Biometrika, 58(1), 83-90.

[13] Pastor-Satorras, R., Castellano, C., Van Mieghem, P., & Vespignani, A. (2015). Epidemic processes in complex networks. Reviews of Modern Physics, 87, 925-979.

[14] De Domenico, M., Omodei, E., & Arenas, A. (2016). Quantifying the diaspora of knowledge in the last century. Applied Network Science, 1, 15.
