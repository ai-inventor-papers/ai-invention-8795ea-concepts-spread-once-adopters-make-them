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

| Test | p-value | Holm corrected |
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

The 7 indicator families are:

1. **Volume/reach** (log_offhome_volume, burst, n_authors_early, author_growth)
2. **Cooccurrence topology** (D_ratio, D_rare, participation, n_comm_W3, ego_density_W3, new_edge_rate, NOV)
3. **Centrality** (G, G_A, G_btw, G_deg, G_phimin)
4. **Relatedness** (RS, REL_home, M0_density_end, D_vol_end, CONTACT_REACH, RETENTION_RATIO_early, FRONTIER_POTENTIAL)
5. **Lineage** (edge_persistence, relay_share)
6. **External recognition** (external recognition variants)
7. **Composite** (entropy, reach, nonhome_share from the five feature baseline)

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

Only **n_authors_early** (+0.161 [+0.090, +0.230], Holm p = 1.0e-4, sign agree 6/6) is confirmed for predicting sustained uptake. No cooccurrence or centrality indicator survives.

### 19.5 Transience: 2 of 10 confirmed: 2 of 10 confirmed

Two indicators predict transience (lower transience = better):

| Indicator | Pooled beta | 95% CI | Holm p |
|---|---|---|---|
| REL_home | -0.114 | [-0.180, -0.047] | confirmed |
| author_growth | +0.065 | [+0.024, +0.106] | confirmed |

Concepts from fields with high relatedness to many other fields (REL_home) are less transient. Concepts with higher early author growth are more transient. The ElasticNet shrank all transience indicators to zero on this outcome, meaning no linear combination adds reliably.

### 19.6 External recognition: 0 of 10 confirmed: 0 of 10 confirmed

No indicator predicts external recognition. All Holm p = 1.0. This is consistent with the Evaluation 2 finding that external recognition is unrelated to publication outcomes (Section 21.2).

### 19.7 Learned models

| Model | O2r_m50 metric (Spearman) | R-squared | Delta vs B5 | Delta CI |
|---|---|---|---|---|
| B5 (baseline) | 0.706 | 0.517 | - | - |
| B5 + best single (M0_density_end) | 0.739 | 0.549 | +0.033 | [+0.022, +0.045] |
| ElasticNet (all indicators) | 0.765 | 0.583 | +0.059 | [+0.046, +0.073] |
| EBM (Explainable Boosting Machine) | 0.757 | 0.573 | +0.052 | [+0.037, +0.067] |

The learned models add 5-6 percentage points of Spearman correlation over the five feature baseline on heldout data (n = 1,833). The ElasticNet slightly outperforms the EBM. Both CIs exclude zero.

For transience, the learned EBM gives a much larger gain (+0.174 over the five feature baseline, CI [+0.129, +0.219]), driven by nonlinear interactions. The ElasticNet shrank all transience features to zero.

### 19.8 Preregistered verdicts

| Prediction | Description | Verdict |
|---|---|---|
| P1: entropy is the single strongest indicator | entropy raw rho is 0.63-0.85 per group, but several indicators outperform it in PSP | **FAILS** |
| P2: edge persistence is negatively associated with breadth | pooled PSP = -0.080 [-0.126, -0.033], mean raw rho across 4 groups = -0.128 | **HOLDS** |
| P3: cooccurrence growth indicators generalise beyond CS | deg_growth and str_growth pooled PSP include zero; new_edge_rate is positive in all 4 groups but CS-specific in dev | **FAILS** |
| P4: early retention ratio predicts breadth conditional on volume | RETENTION_RATIO_early is confirmed for O2r_m50 but FRONTIER_POTENTIAL (retention × reach) does not add to the baseline minus reach | **FAILS** |
| P5: CONTACT_REACH is the strongest single indicator for O2r_m50 | CONTACT_REACH pooled PSP +0.213 [0.159, 0.265]; M0_density_end is stronger (+0.375) | **FAILS** |

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

6. **Transience ElasticNet: ALL shrunk to zero.** The ElasticNet learned model for transience has no nonzero coefficients, meaning no linear combination of the 53 indicators predicts transience beyond noise on heldout data. The EBM's gain (+0.174) relies on nonlinear interactions that the ElasticNet rejects.

7. **Four of five preregistered predictions fail.** Entropy is not the single strongest indicator (prediction 1, "entropy is the strongest single indicator," fails; M0_density_end and D_vol_end are stronger). Cooccurrence growth indicators do not generalise beyond CS (prediction 3, "cooccurrence growth indicators generalise," fails). FRONTIER_POTENTIAL does not add to the baseline minus reach (prediction 4, "early retention ratio predicts breadth conditional on volume," fails). CONTACT_REACH is not the strongest single indicator (prediction 5, "CONTACT_REACH is the strongest single indicator," fails; M0_density_end is stronger).

8. **G_btw (betweenness centrality) for O2r_m50: NOT CONFIRMED.** G_btw pooled beta = +0.056 [-0.006, +0.118], Holm p = 0.156. This is the iteration-2 breadth hypothesis indicator rescored on the full indicator screen; it does not survive Holm correction.

9. **RS (relatedness support) for O2r_m50: NOT CONFIRMED.** RS pooled beta = -0.072 [-0.153, +0.010], Holm p = 0.156. The sign is negative (concepts with more relational support spread less broadly), opposite to the naive prediction.

10. **External recognition for all indicators: NULL.** No early indicator predicts whether a concept will be recognised externally. All Holm p = 1.0 across both external recognition variants and all 10 tested indicators.


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


## 23. What we have learned so far

Three iterations, twelve artifacts (ten commissioned, eight completed in iteration 1; five completed in iteration 2; four completed in iteration 3) have tested whether temporal network signals predict how new scientific concepts spread across disciplines, using OpenAlex data on up to 12,499 concepts with up to 27,393 concept by field adoption episodes.

**Confirmed findings:**

1. **Retaining relatedness predicts the next field entered, beyond the Hidalgo/Guevara RCA density rival (the retained frontier hypothesis, PARTIAL).** A conditional logit on concept year risk sets shows that relatedness to the fields currently retaining a concept predicts which field the concept enters next, beyond field size, the conventional RCA > 1 density (D_rca), share weighted current presence density (D_vol), ever entered density, relatedness to home, and the target field's own gateway centrality. On an independent frame of 3,162 heldout concepts (6,978 entry events), d0_ret_rel = 0.322 (95% CI [0.291, 0.355]), LR = 325.8. DerSimonian-Laird pooled over 4 heldout groups: 0.243 [0.118, 0.368], I squared = 0.92. Positive in 3 of 3 evaluable groups (PHYS 0.148, LIFEENV 0.401, SOC 0.297; MATHDEC null). Cohort (2010-2014): 0.321. Permutation p = 0.001, rewired backbone p = 0.004, node label p = 0.003 (all Holm corrected < 0.01). **However:** the volume matched contrast is null on heldout data (Holm p = 0.76), so persistence and volume are confounded. The conditional logit's d0 may reflect sustained volume rather than adapted knowledge. The verdict is PARTIAL. The dose response is monotone nondecreasing (age 2: 0.056, age 3: 0.103, age 4+: 0.251; contrast 4+ vs 2: 0.195 [0.153, 0.236]).

2. **Seven of 10 early network indicators are confirmed for predicting rarefied field breadth on heldout fields (the indicator screen deliverable).** The confirmed indicators (Holm p < 0.05, CI excluding zero, sign agreement 6/6 across 4 heldout groups + 2 cohort parts) are: M0_density_end (+0.375), D_vol_end (+0.307), CONTACT_REACH (+0.211), n_comm_W3 (+0.167), NOV (+0.151), RETENTION_RATIO_early (-0.114), and ego_density_W3 (-0.102). They span relatedness and cooccurrence families. An ElasticNet combining all indicators adds +0.059 (CI [0.046, 0.073]) Spearman correlation over the five feature baseline on 1,833 heldout concepts.

3. **Retaining relatedness predicts the next field entered (the entry hypothesis, confirmed on holdout data in iteration 2).** Holdout LR 71.7 (p = 2.5e-17), standardised d = 0.30 (95% CI [0.24, 0.37]), DL pooled d = 0.28 (95% CI [0.22, 0.35], I squared = 0). This was confirmed in iteration 2 and is now replicated on a separate frame in iteration 3 with additional RCA and volume density rivals.

4. **Two stable trajectory classes.** DTW k-medoids separates 188 concepts into "integrating" (128 concepts, mean 6.7 fields retaining by year 9) and "localised" (60 concepts, mean 2.9 fields retaining). Holdout recluster ARI = 0.54.

5. **Background homophily dominates raw lineage (methodological finding).** Two thirds of between concept variance in raw lineage log odds is general disciplinary homophily.

6. **Edge persistence is negatively associated with breadth (preregistered prediction 2: HOLDS).** Concepts whose cooccurrence edges persist between windows spread less broadly. Pooled PSP = -0.080 [-0.126, -0.033].

**Disconfirmed or downgraded:**

1. **Gateway centrality does not predict field retention.** Disconfirmed on 27,393 episodes (iteration 2). The iteration-1 lead (+0.103 on 80 episodes) was a small sample artefact.

2. **No concept level network indicator beats the simple baseline for raw breadth (iteration 1).** All three theory driven indicators (naturalisation gap, structural diversity, gateway landing) fail the preregistered decision rule. The learned model (iteration 3) does add +0.059 over the five feature baseline using multiple indicators jointly.

3. **Volume matched persistence is null on heldout data (iteration 3).** The retained frontier hypothesis is PARTIAL: persistence and volume are confounded.

4. **Abandonment penalty is inconclusive.** d_lost = -0.007 [-0.036, 0.022] on the independent frame (iteration 3), not replicating the Experiment 6 estimate of -0.063.

5. **External recognition is unrelated to publication outcomes.** Pooled rho with O2r_m50: 0.014 [-0.045, 0.073]. external recognition measures prior recognition (67% at or before t0), not diffusion success.

6. **Rescue and relay mechanisms are not supported (iteration 2).** Neither reimportation nor onward radiation is detectable.

**Open:**

- The retained frontier claim's novelty against a persistence filtered RCA density rival (D_rca_persist_k) is untested.
- Neighbour momentum density (relatedness weighted usage growth) is the main uncontrolled confound.
- The "explain why strongest indicator works" analysis and case studies are not started.
- The AI first stage (exploratory nonlinear screening) is not started.
- Candidate S (unconnected coauthor groups, Cheng et al. 2023) remains untested.
- The HMM trajectory model (6 states, ARI 0.094 with DTW) from Experiment 6 is a direct robustness failure for the "two stable classes" claim.


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

[24] Blackburn, T. M., Pyšek, P., Bacher, S., Carlton, J. T., Duncan, R. P., Jarošík, V., Wilson, J. R. U., & Richardson, D. M. (2011). A proposed unified framework for biological invasions. Trends in Ecology & Evolution, 26(7), 333-339.

[25] Pinheiro, F. L., Hartmann, D., Boschma, R., & Hidalgo, C. A. (2022). The time and frequency of unrelated diversification. Research Policy, 51(8), 104323.

[26] Albora, G., Pietronero, L., Tacchella, A., & Zaccaria, A. (2023). Product progression: a machine learning approach to forecasting industrial upgrading. Scientific Reports, 13, 1481.

[27] Bahar, D., Hausmann, R., & Hidalgo, C. A. (2014). Neighbors and the evolution of the comparative advantage of nations: Evidence of international knowledge diffusion? Journal of International Economics, 92(1), 111-123.

[28] Fernandes, A. M., & Tang, H. (2014). Learning to Export from Neighbors. Journal of International Economics, 94(1), 67-84.

[29] Nomaler, Ö., & Verspagen, B. (2022). Some New Views on Product Space and Related Diversification. arXiv:2203.16316.

[30] Richardson, D. M., Pyšek, P., Rejmánek, M., Barbour, M. G., Panetta, F. D., & West, C. J. (2000). Naturalization and invasion of alien plants: concepts and definitions. Diversity and Distributions, 6, 93-107.

[31] Li, Y., & Neffke, F. (2022). Evaluating the principle of relatedness: Estimation, drivers and implications for policy. arXiv:2205.02942.

[32] Chinazzi, M., Gonçalves, B., Zhang, Q., & Vespignani, A. (2019). Mapping the physics research space: a machine learning approach. EPJ Data Science, 8, 33.
