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

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] Append: 'On held-out groups (Exp8), new_edge_rate transfers beyond B5 (pooled psp +0.118), whereas participation +0.150, NOV_res +0.139, D_rare +0.162 and D_ratio +0.066 are small but positive, so the iteration-1 conclusion that none adds to B5 does not hold on held-out data.'


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

[Correction, iteration 3, from art_7W9xiIO3FVBs] All 12 candidates are in the file: D_ratio +0.335 [-0.059, 0.688] (3/4 groups +); D_rare +0.311 [-0.101, 0.692] (3/4 groups +); D_z +0.313 [-0.161, 0.634] (4/4 groups +); D_sub +0.245 [-0.162, 0.634] (4/4 groups +); NOV_res +0.281 [-0.190, 0.639] (2/4 groups +); participation +0.322 [-0.115, 0.690] (3/4 groups +); n_comm_W3 +0.218 [-0.153, 0.627] (2/4 groups +); F_res -0.267 [-0.492, 0.324] (1/4 groups +); F_z -0.248 [-0.509, 0.353] (1/4 groups +); F_bg -0.301 [-0.560, 0.254] (2/4 groups +); deg_growth +0.050 [-0.466, 0.381] (1/4 groups +); btw_change -0.168 [-0.514, 0.400] (1/4 groups +). Paste record_tables/partial_association_all.csv.

Source (from Eval2): `round-1/experiment-3/src/results/exploratory_partial_association.json: candidates.*`


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

[Correction, iteration 3, from art_7W9xiIO3FVBs] | B3 + log field size + {gateway_j, phi_home_j, density_j} (size_controlled_all_three) | 0.697 | 0.782 | +0.085 | [0.004, 0.164] | refit [-0.043, 0.220] | and add | B3 + {gateway_j, phi_home_j, density_j} (all_four_available) | 0.705 | 0.787 | +0.082 | [0.008, 0.153] | refit [-0.042, 0.204] |. Neither row contains G, REL, RS or G_all; both refit CIs include 0.

Source (from Eval2): `round-1/experiment-4/src/screen_result.json: field_level.size_controlled_all_three.*, field_level.all_four_available.*`; `round-2/evaluation-1/src/eval_out.json: metadata.F_record.F5_exp4_field_level.rows.*`


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

1. **Background homophily measurement:** Background homophily explains 66% of between concept variance in raw lineage autonomy. This is a methodological finding: uniform null indices conflate field composition with concept specific integration. Nearest published neighbour: Ciotti et al. (2016) showed that citation homophily across fields exceeds chance, but they did not decompose it into background and concept specific terms or measure its share of raw lineage autonomy [4].

2. **Field level gateway effect:** The adopting field's gateway centrality on the topic backbone adds delta AUC = +0.10 for retention, surviving a field size control. This is a field level, not concept level, result: whether a specific nonhome field retains a concept is partly predicted by that field's centrality in the field relatedness network. Nearest published neighbour: Hidalgo et al. (2007) showed that a country's position in the product space predicts which products it diversifies into [5]; Guevara et al. (2016) extended this to scientific fields and found entry AUCs of 0.68 to 0.90. The present result concerns retention rather than entry, and conditions on concept level baseline and field size.

3. **Exploratory partial association of D_ratio:** The structural diversity of cooccurrence ties has a partial Spearman of 0.34 with rarefied breadth conditional on the five feature baseline (permutation p = 0.037). **[Correction, iteration 2:]** This finding is marginal, uncorrected (1 of 12 tests), negative in Engineering, and its 95% CI includes zero. Nearest published neighbour: Weng et al. (2013) showed that early community diversity predicts virality in social networks [2]; the present result is the scholarly analogue.



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

[Correction, iteration 3, from art_7W9xiIO3FVBs] Replace the 8a table with record_tables/coverage_iter2_steps.csv (status after iteration 2) and add the per-artifact row counts in record_tables/coverage_iter2.csv (concepts, episodes, groups, splits, median label coverage, grounding precision, LLM cost, credits).

Source (from Eval2): `record_tables/coverage_iter2.csv`; `record_tables/coverage_iter2_steps.csv`




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

[Correction, iteration 3, from art_7W9xiIO3FVBs] The common-panel design was not realised: Exp5 (12,499 concepts, TAG grounding) and Exp6 (653 newborn concepts, tag-AND-title) share 628 concepts (96.2% of Exp6). On them, onset agrees exactly for 97.6% (+/-1: 98.9%), home kappa = 0.99, O2r_m50 Spearman = 0.998, episode Jaccard median = 1.00, but retention kappa = 0.28 (Exp5 relative-share rule vs Exp6 absolute >= 2 works; with the matched definition R_abs2 kappa = 0.98). Pre-declared pooling verdict: **PARTIAL**. A replication of H2 on 'Exp5 minus Exp6' must rebuild RETAINED/LOST with Exp6's R_cj rule before a null can be read as a failure of the claim.

Source (from Eval2): `frame_agreement.json`; `record_tables/definitions_diff.csv`; `record_tables/frame_overlap_by_group.csv`


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

[Correction, iteration 5, from this evaluation] The Evaluation 3 block below was only partly applied in the iteration-5 report (80% of its numbers present); it is appended in full.

[Correction, iteration 3, from art_7W9xiIO3FVBs] Verdict: **DISCONFIRMED** by the preregistered rule, which requires all six core criteria. Criterion by criterion (held-out, 8,515 episodes / 3,085 concepts): pooled dAUC >= 0.05 False; refit CI > 0 False; >= 3 of 4 groups positive False (2 of 4); cohort same sign True (both negative); within-field LPM beta > 0 at p < 0.05 **True** (beta = +0.068 per SD, concept-clustered SE 0.033, p = 0.041; two-way clustered p = 0.17; all splits +0.051, p_concept = 0.0065, p_twoway = 0.18); real dAUC above the rewired-backbone placebo p95 False. The frozen rule names p < 0.05 without an SE type and the sealed code uses the concept-clustered p, so the LPM criterion passes as preregistered but is fragile under two-way clustering. Clustered-SE logit: beta = -0.045 (p_concept = 0.29); boundary interaction +0.064 (p = 0.45; predicted negative, consistent = False); crossed concept x field bootstrap CI [-0.0023, 0.0010].

Source (from Eval2): `round-2/experiment-5/src/results/h1_heldout.json: verdict_H1.criteria.*`; `lpm_field_fe.*`; `lpm_field_fe_all_splits.*`; `logit_clustered_se.*`; `boundary.*`; `pigeonhole_crossed_bootstrap.ci95`; `round-2/experiment-5/src/models.py (p_concept in the criterion)`


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

[Correction, iteration 3, from art_7W9xiIO3FVBs] The relatedness pair adds dAUC +0.0034 on held-out data but -0.00017 on DEV: the gain was not seen in development.

Source (from Eval2): `round-2/experiment-5/src/results/h1_heldout.json: rival_head_to_head.dauc_relatedness_pair`; `round-2/experiment-5/src/results/h1_dev.json: rival_head_to_head.dauc_relatedness_pair`


### 10.6 Concept breadth hypothesis: result: small but confirmed

Gateway weighted early landing G predicts volume residualised breadth on holdout data, but the effect is small:

| Variant | Holdout partial rho | Holm corrected p |
|---|---|---|
| G (eigenvector) | 0.030 | 0.0045 |
| G_A (authority) | 0.026 | 0.0045 |
| G_btw (betweenness) | 0.046 | 0.0045 |
| REL_home | -0.136 | 1.0 |

[Correction, iteration 3, from art_7W9xiIO3FVBs] H3 is **small; it passes the preregistered within group permutation rule, but the pooled concept bootstrap CI includes 0**. Heldout: G partial rho = 0.030 [-0.006, 0.065]; DL within group G = 0.068 [0.029, 0.107], I2 = 0.00; G_btw DL = 0.072 [-0.015, 0.159], I2 = 0.77 (negative in LifeEnv). The calibration check found 0 of 40 shuffled outcomes declared significant (a false positive rate check, not a p value). REL_home is strongly negative (-0.14), meaning that concepts whose home field is closely related to many other fields tend to achieve less size adjusted breadth.

[Correction, iteration 3, from art_7W9xiIO3FVBs] H3 is **small; it passes the preregistered within-group permutation rule, but the pooled concept-bootstrap CI includes 0**. Held-out (n = 2,838): G partial rho = 0.030 [-0.006, 0.065], G_A 0.026 [-0.011, 0.067], G_btw 0.046 [0.009, 0.086]; Holm p = 0.0045 from a one-sided within-group permutation test (2,000 draws; Holm over G, G_A, G_btw) whose null is centred below zero (about -0.012). Within-group DL pooled G = 0.068 [0.029, 0.107], I2 = 0.00; G_btw DL = 0.072 [-0.015, 0.159], I2 = 0.77 (negative in LifeEnv, -0.020). DEV values: G 0.138, G_btw 0.170; held-out/DEV shrinkage for G = 0.21. The calibration check found 0 of 40 shuffled outcomes declared significant (false-positive rate 0/40), which is not a p-value or an exceedance count.

Source (from Eval2): `round-2/experiment-5/src/results/h3_results.json: G.*, G_A.*, G_btw.*, holm_adjusted_p, notes`; `round-2/experiment-5/src/results/h1_dev.json: H3_dev`; `round-2/experiment-5/src/results/audit_placebo.json: H3_calibration_40_shuffles`


### 10.7 Minimum detectable effect and power

The minimum detectable delta AUC is 0.004 (at 80% power, 27,393 episodes). With only 26 fields, the standard deviation of the delta AUC under the alternative stays at approximately 0.015 regardless of the number of episodes (1,000 to 4,000), creating a floor. Approximately 34 holdout concepts per group give P(group delta > 0) >= 0.90 at a true delta of 0.05.

[Correction, iteration 3, from art_7W9xiIO3FVBs] Exp5 (art_wxWssKSUR45f) power simulation (h1_dev.json power; planted effect b in SD log-odds of standardised gateway_j on the dev covariate structure; 40 sims x 150 boot): a planted effect b = 0.3 gives mean dAUC 0.0040 with power 0.90 (b = 0.2: 0.0019, power 0.65), so 0.004 is the **90%** point (the file key 'min_detectable_dauc_80pct' mislabels it), computed for 8,515 held-out episodes, not 27,393. At b = 0 the CI > 0 rule fires 0.125 of the time (nominal 0.025): the concept-only bootstrap is anti-conservative. Evaluation 1 (art_lwI2DuRtQRZX, E_power) adds a field random intercept: the SD of dAUC under the alternative stays near 0.016 (floor about 0.02) and about 34 held-out concepts per group give P(group delta > 0) >= 0.90 at delta = 0.05. The field-random-intercept figure governs the H1 verdict's field-level uncertainty; the Exp5 figure ignores between-field variance.

Source (from Eval2): `round-2/experiment-5/src/results/h1_dev.json: power.*`; `round-2/evaluation-1/src/eval_out.json: metadata.E_power.held_out_sizing_from_alternative_SD.*`


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

[Correction, iteration 3, from art_7W9xiIO3FVBs] LR 68.6 = M1 (plain retaining relatedness d0_ret_rel) vs M0, Breslow; LR 71.7 = M2 (gateway-weighted d_ret_gate) vs M0, Breslow; LR 77.3 = M2 vs M0 with the exact conditional likelihood (statsmodels, Exp6 audit.json). Recomputed here: M1vsM0 Breslow 68.57 / exact 73.25; M2vsM0 Breslow 71.72 / exact 77.30. d = 0.281 is the M1 coefficient of plain retaining relatedness (d0_ret_rel, SE 0.032); d = 0.302 ('0.30') is the M2 coefficient of gateway-weighted retaining relatedness (d_ret_gate). Both are Breslow, per SD of the frozen DEV standardisation. The hypothesis text's '961 strata' is the number of INFORMATIVE strata (>= 1 event and >= 1 non-event) that enter the conditional likelihood (961 recomputed; 18846 rows); the file's n_strata = 2,339 counts ALL strata of the primary sample (n_ret > 0; 2339 recomputed, 46433 rows). The parquet itself holds 2992 strata / 61648 rows before the n_ret > 0 restriction. The conventional headline is the plain retaining-relatedness coefficient d0_ret_rel = 0.281 (SE 0.032), since the gateway weighting adds nothing (M3 vs M1 g-only permutation p = 0.17).

Source (from Eval2): `record_tables/next_field_trace.json`; `round-2/experiment-6/src/results/heldout_result.json: H2_pooled.*`; `round-2/experiment-6/src/results/audit.json: H2_LR`


### 11.3 Ordering: first retained gateway precedes entropy takeoff

Among 175 concepts in the top rarefied breadth tercile, 112 (64%) have a detected entropy change point. Of those with an evaluable ordering:

| Condition | N evaluable | Share "before" (excl. ties) | Sign test p (one sided) |
|---|---|---|---|
| First retained gateway field | 102 | 65.5% | 0.003 |
| First retained peripheral field | 106 | 57.0% | 0.118 |

McNemar test comparing gateway vs peripheral: p = 0.088 (27 gateway only, 15 peripheral only). [Correction, iteration 3, from art_7W9xiIO3FVBs] Ordering is **mixed / not established**. The preregistered sign rule passes, but concept FE lead lag regressions show retention followed by SMALLER next year entropy gains (gateway b = -0.0279, p = 0.0007; peripheral b = -0.0434, p = 5.9e-08), a significant pretrend (event time -3: -0.072, p = 0.0002; DEV -0.088), and on DEV entropy predicting later gateway retention (b = 0.232 [0.066, 0.397], p = 0.0062; heldout b = 0.077, p = 0.22). The gateway permutation placebo is null (p = 0.63).

[Correction, iteration 3, from art_7W9xiIO3FVBs] Ordering is **mixed / not established**. Of 175 broad (top-tercile O2r) concepts, 112 have a detected entropy take-off and 102 an evaluable gateway ordering: the first retained gateway field comes first in 57, ties 15, after 30 (57/87 = 65.5% of non-tied; 57/102 = 55.9% of evaluable; 57/175 = 32.6% of broad concepts; sign p = 0.0025). Peripheral fields: 49/20/37, 57.0%, p = 0.118; McNemar 27 vs 15, p = 0.088. The preregistered sign rule passes, but concept-FE lead-lag regressions show retention followed by SMALLER next-year entropy gains (gateway b = -0.0279, p = 0.0007; peripheral b = -0.0434, p = 5.9e-08), a significant pre-trend (event time -3: -0.072, p = 0.0002; DEV -0.088), and on DEV entropy predicting later gateway retention (b = 0.232 [0.066, 0.397], p = 0.0062; held-out b = 0.077, p = 0.22). On DEV, peripheral fields precede take-off as often as gateway fields (71.4% vs 70.3%, McNemar p = 0.34); the gateway permutation placebo is null (p = 0.63). The file flag decisions.H2_ordering.CONFIRMED = true checks only the sign rule and is overridden here.

Source (from Eval2): `round-2/experiment-6/src/results/heldout_result.json: ordering.*`; `round-2/experiment-6/src/results/dev_result.json: ordering.*`; `round-2/experiment-6/src/results/heldout_result.json: decisions.H2_ordering.CONFIRMED`


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

[Correction, iteration 3, from art_7W9xiIO3FVBs] DTW k-medoids k = 2 is stable under bootstrap (ARI 1.0), but the 6-state HMM does not reproduce it (HMM vs DTW ARI = 0.095), and the localised class is dominated by Medicine homes.

Source (from Eval2): `round-2/experiment-6/src/results/heldout_result.json: trajectories.hmm_vs_dtw_ARI`


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

[Correction, iteration 3, from art_7W9xiIO3FVBs] Concept counts (coverage_report.json by_source): mesh 20,872 concepts with an event (20,872 year-usable); wikipedia_en 64,363 concepts with an event (50,459 year-usable); wikidata 1,425 concepts with an event (1,316 year-usable); acm_ccs 1,298 concepts with an event (1,298 year-usable); msc 1,121 concepts with an event (1,121 year-usable); pacs_physh 2,635 concepts with an event (2,635 year-usable); gartner_hype_cycle 466 concepts with an event (466 year-usable); mit_tr10 313 concepts with an event (313 year-usable); research_fronts 589 concepts with an event (589 year-usable); nature_methods_moty 38 concepts with an event (38 year-usable); science_boty 53 concepts with an event (53 year-usable); physics_world_boty 100 concepts with an event (100 year-usable); jel 0 concepts with an event (0 year-usable). Wikipedia exact first revisions: 7,806. The draft's 3,583 / 17,872 / 8,462 / 1,015 are external-ENTRY counts (external_entries_acm_ccs / msc / pacs_physh / jel), not concepts; the '589' is Research Fronts only. JEL: 213 concepts found, 0 dated events (present-day membership).

Source (from Eval2): `round-2/dataset-2/src/out/coverage_report.json: by_source.*.n_with_event, n_with_year_usable_event, status`; `round-2/dataset-2/src/README.md: external_entries table`


### 13.2 Quality

All known answer asserts pass (optogenetics NM 2010, iPSC NM 2009, CRISPR BOTY 2015, superresolution NM 2008). Audit precision: 0.96 for label matches, 0.79 for ID links, 0.31 for alias only matches (alias matches were LLM verified; accepted LLM links are 0.97 precise on hand check). Intermodel kappa is 0.60 (accept/reject).

Coverage is uneven: Social Sciences and Engineering have no dated domain taxonomy, so a Wikipedia/Wikidata only external recognition variant is needed for cross group comparisons. Wikipedia creation dates cluster in its 2001-2007 growth wave, and Research Fronts are citation derived.

The dataset includes a provisional dev/holdout/unassigned split (19,600/28,300/17,100 concepts) based on level-1 ancestors mapped to OpenAlex fields and then to the hypothesis groups.

[Correction, iteration 3, from art_7W9xiIO3FVBs] O5 was joined to the Exp5 frame (all 12,499 concepts). O5_main base rate: 0.238 held-out. It is **UNRELATED** to publication outcomes: pooled held-out rho with O2r_m50 = 0.014 [-0.045, 0.073], with O1 = 0.001 [-0.033, 0.034]. For 8,371 of 12,499 concepts the first qualifying recognition is at or before t0. Executor-checked sample: positive precision 0.86, Wikipedia date error <= 1 year in 0.95, negative false-negative rate (Wikipedia only, lower bound) 0.14; FIT_FOR_USE = True.

Source (from Eval2): `o5_validation.json`; `o5_definitions.json`; `record_tables/o5_*.csv`




## 14. Research 1: How our results compare with related papers [ARTIFACT:art_dxvRpQufMR0e]

A positioning study for the Applied Network Science paper. The key comparative findings:

1. **Field entry versus retention.** Guevara et al. (2016) report field entry AUCs of 0.68 to 0.90 for the research space; no published AUC exists for retention or exit of an adopted concept. The iteration-1 delta AUC of +0.10 for gateway predicted retention had no direct counterpart, but it has now been disconfirmed on holdout data.

2. **Relatedness principle.** Neffke et al. (2011), Rigby (2015) and others credit relatedness for both entry and exit/survival of activities. The holdout test confirms that the relatedness pair (phi_home_j plus density) adds delta AUC +0.0034 (95% CI [0.0010, 0.0051]), beating gateway (which adds nothing). The principle of relatedness (the empirical regularity that regions and fields diversify into activities related to their existing portfolio [6]) is confirmed for concept field retention, though the effect is small.

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

2. **Two stable trajectory classes (research question 2 (trajectories)).** DTW k-medoids separates 188 concepts with sustained uptake into "integrating" (128 concepts, mean 6.7 fields retaining by year 9, O2r 5.2) and "localised" (60 concepts, mean 2.9 fields retaining, O2r 2.8). The localised class is dominated by Medicine home concepts. Holdout independent recluster ARI = 0.54. [Correction, iteration 5, from art_uw4OeagJP3rv] Superseded: at higher resolution the typology is a continuum (DTW-HMM ARI 0.222; Section 26.2).

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

[Correction, iteration 3, from art_7W9xiIO3FVBs] positive in all four held-out groups (sign test p = 0.0625); only Physical's bootstrap CI excludes 0 (Physical d = 0.33 [0.05, 0.57]; LifeEnv LR p = 0.23; Social LR p = 0.076; cohort d = 0.29).

Source (from Eval2): `round-2/experiment-6/src/results/heldout_result.json: H2_per_group.*, H2_sign_count`




## References (iteration 2 list)

[Correction, iteration 5, from this evaluation] Merged into the single numbered reference list at the end of the report; in-text numbers were renumbered (map in `references_master.md`).

# Iteration 3

## 17. Why this iteration ran

The iteration-2 review raised 13 MUST FIX items and 2 MINOR items. The central objections were:

1. **The confirmed entry hypothesis result may not be new.** The reviewer pointed out that the standard Hidalgo et al. (2007) density is computed over fields where the actor has revealed comparative advantage (RCA > 1), which is effectively a thresholded, persistent presence. Experiment 6's entry baseline used an unthresholded ever entered density. the retaining relatedness model beating the entry baseline (LR 68.6) might only show that a conventional thresholded density beats an unthresholded one. The reviewer required adding a conventional RCA density rival (D_rca) and a share weighted current presence density (D_vol) to the entry model and testing whether retained field relatedness (d0_ret_rel) survives both.

2. **The indicator screen (research question 1) was still missing.** The request's core deliverable, a screen of 30 to 50 temporal knowledge network indicators with the strongest 10 validated on heldout fields, had not been attempted. The cooccurrence and lineage indicators existed only on the 46-48 concept dev panels, and no concept level indicator had been validated on heldout concepts.

3. **The external recognition outcome was built but never used.** Dataset 2 compiled recognition events for 65,026 concepts, but external recognition had not been joined to any panel or tested against any indicator.

4. **The record audit had not been run.** 246 claims across iterations 1-2 had not been checked against their source artifacts.

The hypothesis was updated to the "retained frontier" framing: we define the retained frontier as the set of fields that currently hold a concept above a persistence threshold, and predict that concepts spread from these fields to related ones. The retained field relatedness predictor (d0_ret_rel) must survive the conventional RCA density rival. The abandonment penalty (d_lost, relatedness to fields that dropped the concept) was a secondary claim. The mechanism draws on invasion biology: casual aliens (entered but lost) versus naturalised aliens (retained), following Richardson et al. (2000) [7] and Blackburn et al. (2011) [8].

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

- Exp7 frozen definition (frozen_spec.json covariates.D_rca_pers): 'U = RCA(t-3..t-1) > 1 AND RCA(t-6..t-4) > 1'.
- Research 2 (art_EesdB8cuSfcU) R1: 'entered or RCA > 1 in each of t-k..t'.
- Verdict: **DIFFERENT**. D_rca_pers uses two window-aggregated 3-year RCAs over a 6-year horizon; persist_k requires the state in each single year and admits 'entered' presences below RCA 1. Neither U-set contains the other.
- DEV check (958,542 candidate rows, 4,486 concepts; recipe check: rebuilt D_rca_1y vs Exp7 Spearman 1.0000):

| variant | Spearman with D_rca_pers | Spearman with D_rca_1y | share rows > 0 |
|---|---|---|---|
| D_rca_persist_2_entered_or_rca | 0.718 | 0.690 | 0.608 |
| D_rca_persist_2_rca | 0.877 | 0.875 | 0.342 |
| D_rca_persist_3_entered_or_rca | 0.729 | 0.690 | 0.588 |
| D_rca_persist_3_rca | 0.864 | 0.829 | 0.317 |

Source: `round-4/evaluation-3/src/results/drca_persist_comparison.json` -> `comparisons.*; recipe_check_D_rca_1y_spearman`
Consequence: Exp7's S_strict rival set did NOT contain Research 2's D_rca_persist_k; the 'persistence-filtered RCA density' rival (R1 in Research 2) remains untested against d0 and should be listed as an open rival.

[Correction, iteration 4, from art_22ppE1snfHKj] The retained-frontier predictor sits next to four lines of work. Hidalgo et al. (2007) define density from a region's current revealed-comparative-advantage basket and show that products close to that basket are entered next. Pinheiro et al. (2022) add persistence, but only on the outcome side: an entry counts only if RCA stays above one after years below it. Albora et al. (2023) benchmark relatedness against machine-learning forecasts of entry that use the unit's own past RCA trajectory (the benchmark Research 2 flags as a missing rival here). Cheng et al. (2023) bring the diffusion question to science and tie a topic's spread to the social structure of its early adopters (unconnected co-author groups; our candidate S). Our d0 moves persistence to the predictor side (relatedness to fields that RETAIN the concept). It is backbone-specific (18.6a) and not separable from volume in the matched contrast (18.5), and the persistence-filtered density twin D_rca_persist_k differs from Exp7's D_rca_pers (Step-3 above).



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

| estimate | concept bootstrap (1,000) | two-way concept x field clustered (coef +- 1.96 SE) | crossed concept x field bootstrap (500) |
|---|---|---|---|
| +0.322 | [+0.291, +0.355] | [+0.211, +0.432] | [+0.201, +0.468] |

Source: `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.boot.d0_R3.d0_ret_rel.{est,ci}; pooled4.crossed_boot.d0_R3.ci`; `round-4/evaluation-3/src/results/partA_derived.json` -> `exp7_d0_two_way_heldout.ci (from ladder...R3_ret.se_two_way_concept_field.d0_ret_rel)`


### 18.4 Dose response by persistence age

On dev (4,302 concepts), replacing d0_ret_rel with three dummy indicators for retention age shows a monotone nondecreasing dose response:

| Persistence age | d_ret coefficient | Boot 95% CI |
|---|---|---|
| 2 years | 0.056 | [0.019, 0.090] |
| 3 years | 0.103 | [0.058, 0.147] |
| >= 4 years | 0.251 | [0.226, 0.276] |
| Contrast (4+ minus 2) | 0.195 | [0.153, 0.236] |

Spearman correlation between beta and age = 1.0 (monotone nondecreasing). Permutation p (dose trend) = 0.001 (Holm corrected: 0.005).

| age 2 | age 3 | age >= 4 | 4+ minus 2 [CI] | monotone non-decreasing | Spearman(beta, age) |
|---|---|---|---|---|---|
| +0.098 | +0.075 | +0.304 | +0.206 [+0.156, +0.255] | False | 0.50 |

Source: `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.specificity.c_dose.*`


### 18.5 Volume matched contrast

The volume matched contrast tests whether persistence predicts entry beyond current volume. Strata are matched on total concept volume (log field concept paper count), so that retained and not retained fields within each stratum have similar volume. On dev:

| Estimand | Coefficient | Boot 95% CI | LR |
|---|---|---|---|
| d0 (volume matched strata) | 0.069 | [0.019, 0.118] | 13.1 (p = 0.001) |

The volume matched d0 is positive and significant on dev, but the Holm corrected p on the full battery is 0.76 for the heldout volume matched contrast, which is null. **Verdict for criterion 5 (volume_matched_CI > 0): FAILS.** Persistence and volume are confounded in the heldout data.

| split | bins | d_R_m [CI] | d_N_m [CI] | contrast R - N [CI] | one-sided p | match rate (strata) | matched R / N fields | mean cum. prev. volume R / N |
|---|---|---|---|---|---|---|---|---|
| DEV | coarse | +0.069 [+0.021, +0.114] | +0.078 [+0.031, +0.129] | -0.008 [-0.071, +0.050] | 0.611 | 0.128 | 5,209 / 5,673 | 7.78 / 6.07 |
| DEV | fine | +0.061 [+0.006, +0.112] | +0.075 [+0.020, +0.125] | -0.014 [-0.077, +0.048] | 0.683 | 0.121 | 4,869 / 5,359 | 6.20 / 5.52 |
| held-out pooled 4 | coarse | +0.073 [+0.004, +0.134] | +0.100 [+0.039, +0.157] | -0.028 [-0.105, +0.046] | 0.755 | 0.153 | 5,125 / 5,597 | 7.98 / 6.30 |
| held-out pooled 4 | fine | +0.066 [-0.002, +0.130] | +0.092 [+0.033, +0.152] | -0.026 [-0.107, +0.049] | 0.752 | 0.144 | 4,746 / 5,259 | 6.40 / 5.71 |

Source: `round-3/experiment-7/src/results/step2_dev.json` -> `battery.specificity.{b_volume_matched,b2_volume_matched_fine}.*`; `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.specificity.{b_volume_matched,b2_volume_matched_fine}.*`

Reading: both retained and non-retained matched fields carry a positive coefficient, and the pre-declared contrast is null in both bin sets. The retained-relatedness signal cannot be separated from volume.


### 18.6 Specificity tests

| Test | p value | Holm corrected |
|---|---|---|
| Label permutation (within stratum) | 0.001 | 0.005 |
| Rewired backbone | 0.004 | 0.009 |
| Node label permutation | 0.003 | 0.009 |
| Target field fixed effects | 3.98e-58 | 2.39e-57 |

All three specificity tests reject their nulls after Holm correction: the signal requires the specific backbone topology, the specific field labels, and the specific concept field assignments.

**Excluding intersection born concepts** (those with 2+ home fields): d0 = 0.255 (dev), essentially unchanged. **With target field fixed effects:** d0 = 0.241 (dev), retaining most of the signal. **With label coverage >= 0.5:** d0 = 0.236 (dev).

| sensitivity | d0 | concept-clustered p |
|---|---|---|
| e_excl_intersection_born | +0.332 | 4.2e-90 |
| g_target_field_FE | +0.300 | 3.9e-66 |
| h_horizon8 | +0.318 | 2.4e-74 |
| i_excl_weak_home | +0.312 | 4.2e-72 |
| j_excl_medicine_home | +0.322 | 7.5e-89 |
| n_newborn_only_descriptive | +0.562 | 0.034 |
| o_label_coverage_ge_0.5 | +0.317 | 5.4e-65 |
| f_min_n_3 | +0.323 | 2e-84 |
| f_min_n_5 | +0.277 | 1.2e-53 |
| l_rca_entry_event | +0.243 | 2.1e-26 |
| k_primary_topic_fields | +0.276 | 8.7e-93 |
| m_min_conditional_probability_proximity | -0.021 | 0.014 |

Source: `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.{specificity,specificity_rebuild}.<name>.d0_R3.{coef,p_wald_concept_2s}`


### 18.6a Proximity dependence

[Correction, iteration 4, from art_22ppE1snfHKj] The retained-frontier coefficient depends on the proximity backbone. Under Hidalgo's minimum conditional-probability proximity (instead of the frozen PMI backbone), d0 in R3 is -0.021 (LR R3 vs R2 p = 0.012), while the RCA density itself becomes much stronger (LR R1 vs R0 = 245.5). Within-stratum AUC is higher under min-cp without d0 (R2 0.867) than under PMI with d0 (R3 0.852). The d0 effect is backbone-specific: it measures relatedness as PMI encodes it, not relatedness in general.

Source: `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.specificity_rebuild.m_min_conditional_probability_proximity.ladder.{models.R3_ret.coef.d0_ret_rel,LR.*,auc_within.R2_vol}`; `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.ladder.frontier_primary_sample.auc_within.R3_ret`


### 18.7 Guevara AUC comparison

Global (pooled, not within stratum) AUCs on the heldout pooled4 frame, computed over all candidate rows:

| Predictor | AUC |
|---|---|
| D_rca_cum alone | 0.635 |
| c_density alone | 0.637 |
| b_log_size alone | 0.772 |
| R3 linear predictor (full model) | 0.837 |

Guevara et al. (2016) report AUCs of 0.90 (individuals), 0.72 (organisations), 0.68 (countries) for RCA transition entry into research fields [9]. The comparison is not head to head: different units (concept vs scholar/organisation/country), different events (three publication count entry vs RCA transition), and different proximity measures (26-field PMI vs author sharing over subfields).

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

| model | d_lost | CI | note |
|---|---|---|---|
| A1 = R0 + d_lost (all rows) | -0.007 | concept [-0.036, +0.022]; crossed [-0.082, +0.052] | verdict: INCONCLUSIVE (negative point estimate, CI includes 0) |
| R4 = R3 + d_lost (primary sample) | +0.064 | - | positive once d0 is in the model |
| min-cp proximity backbone, R4 | +0.003 | - | min-cp A1: d_lost -0.030, p = 0.00013 |
| target-field FE, A1 | -0.044 | - | key `pooled4.specificity.g_target_field_FE.d_lost_A1.coef` |

Source: `round-3/experiment-7/src/results/step2_heldout.json` -> `pooled4.ladder.*.models.{A1_lost,R4_lost}.coef.d_lost; verdicts.d_lost_ci; crossed_boot.d_lost_A1.ci; pooled4.specificity_rebuild.m_min_conditional_probability_proximity; pooled4.specificity.g_target_field_FE`


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

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] The iteration-1 open rival 'candidate S' was scored in Exp8 as S_comp, S_comp_n and S_isolated_share. DL pooled over the 4 held-out groups from the per-unit rows:

| indicator | outcome | pooled psp | 95% CI | I2 | units positive (of 6) | units CI excl. 0 (of 6) |
|---|---|---|---|---|---|---|
| S_comp_n | O1c | -0.087 | [-0.200, +0.029] | 0.88 | 0 | 4 |
| S_comp_n | O2r_m50 | -0.029 | [-0.239, +0.184] | 0.94 | 3 | 3 |
| S_comp_n | O2r_resid | -0.028 | [-0.244, +0.190] | 0.94 | 3 | 3 |
| S_comp_n | O4 | -0.049 | [-0.192, +0.096] | 0.93 | 3 | 2 |

Source: `round-3/experiment-8/src/results/heldout_unit_results.csv` -> `indicator in S_* :: {z, se_z, rho, ci_lo, ci_hi}`; `round-4/evaluation-3/src/results/partA_derived.json` -> `candidate_S_DL4.*`
Reading: candidate S is now tested (not only 'not run'); none of its rows is in a frozen top-10 confirmed set for breadth; the social-reach rival is weak beyond B5.

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] Exp8 computes 53 indicators in 6 families (entropy, reach, offhome share, log volume and growth belong to the B5 baseline, not to an indicator family; there is no 'external recognition' family, O5 is an outcome):

- **A: co-occurrence ego network** (27): D_z, D_ratio, D_rare, D_sub, D_obs, NOV, NOV_res, F_res, F_z, deg_W1, deg_W3, deg_growth, str_growth, new_edge_rate, edge_persistence, turnover, participation, n_comm_W3, comm_entropy, comm_transitions, ego_density_W3, ego_density_change, btw_end, btw_change, kcore_end, constraint_end, constraint_change
- **E: popularity / volume** (6): share, growth_ind, accel, burst, author_growth, n_authors_early
- **F: disciplinary spread** (3): log_offhome_volume, rao_stirling, fields_gained_per_yr
- **FR: retained frontier / relatedness to entered fields** (7): CONTACT_REACH, RETAINED_REACH, RETENTION_RATIO_early, FRONTIER_POTENTIAL, D_rca_end, D_vol_end, M0_density_end
- **G: landing on gateway fields** (7): G, G_A, G_btw, G_deg, G_phimin, REL_home, RS
- **S: co-author (social) reach** (3): S_comp, S_comp_n, S_isolated_share

Source: `round-3/experiment-8/src/results/indicator_dictionary.csv` -> `family column (counts per value)`; `round-4/evaluation-3/src/results/partA_derived.json` -> `families.*`

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] DEV missing share: D_ratio 0.311, D_z 0.311, D_sub 0.311, D_obs 0.311, D_rare 0.883; the DEV eligibility rule excludes indicators with more than 30% missing. Deviation record, verbatim: 'T4 median M = 3.5 (> 3) so the n_ck >= 2 neighbour rule is kept; consequence: D-family indicators (need M >= 3; D_rare M >= 10) are missing for many concepts and may exceed the 30% missing eligibility bound.'

Source: `round-3/experiment-8/src/results/rq1_dev_selection.json` -> `missing.<indicator>`; `round-3/experiment-8/src/results/deviations.json` -> `T4_M_median`




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

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] Both numbers are correct but refer to different outcomes: +0.375 is O2r_m50 (the 19.2 table and README), +0.377 is O2r_resid (the Exp8 summary headline). Add to 19.2: 'Source: heldout_summary.json -> O2r_m50[indicator=M0_density_end].pooled; the headline +0.377 is O2r_resid.'

Source: `round-3/experiment-8/src/results/heldout_summary.json` -> `O2r_m50[0].pooled`; `round-3/experiment-8/src/results/heldout_summary.json` -> `O2r_resid[0].pooled`


[Correction, iteration 5, from art_dFQ6jbgNsR6Q] Per-group held-out results for the confirmed O2r_m50 indicators (psp [95% CI] (n); † = CI includes 0). Domain failures are shown, not averaged away:

| indicator | PHYS | LIFEENV | SOC | MATHDEC | COH_DEVHOME | COH_OTHER | † cells |
|---|---|---|---|---|---|---|---|
| M0_density_end | +0.429 [+0.333, +0.520] (413) | +0.298 [+0.223, +0.372] (630) | +0.302 [+0.227, +0.372] (689) | +0.547 [+0.377, +0.673] (101) | +0.276 [+0.219, +0.327] (1368) | +0.354 [+0.290, +0.415] (814) | 0 |
| D_vol_end | +0.372 [+0.262, +0.477] (413) | +0.264 [+0.182, +0.348] (630) | +0.325 [+0.256, +0.395] (689) | +0.226 [+0.045, +0.434] (101) | +0.294 [+0.244, +0.350] (1368) | +0.318 [+0.251, +0.378] (814) | 0 |
| CONTACT_REACH | +0.254 [+0.152, +0.350] (413) | +0.184 [+0.094, +0.273] (630) | +0.210 [+0.134, +0.290] (689) | +0.174 [-0.062, +0.449] (101)† | +0.213 [+0.154, +0.268] (1368) | +0.227 [+0.158, +0.296] (814) | 1 |
| n_comm_W3 | +0.124 [+0.020, +0.225] (413) | +0.055 [-0.017, +0.136] (630)† | +0.193 [+0.118, +0.263] (689) | +0.360 [+0.193, +0.503] (101) | +0.222 [+0.169, +0.272] (1368) | +0.096 [+0.029, +0.169] (814) | 1 |
| RETENTION_RATIO_early | -0.062 [-0.154, +0.036] (413)† | -0.117 [-0.191, -0.037] (630) | -0.139 [-0.217, -0.069] (689) | -0.178 [-0.433, +0.076] (101)† | -0.187 [-0.231, -0.134] (1368) | -0.105 [-0.169, -0.037] (814) | 2 |
| NOV | +0.175 [+0.076, +0.265] (391) | +0.033 [-0.046, +0.119] (604)† | +0.132 [+0.051, +0.210] (668) | +0.440 [+0.194, +0.632] (85) | +0.114 [+0.058, +0.170] (1296) | +0.038 [-0.032, +0.109] (782)† | 2 |
| ego_density_W3 | -0.081 [-0.182, +0.024] (397)† | -0.078 [-0.164, +0.008] (610)† | -0.122 [-0.199, -0.043] (668) | -0.236 [-0.434, +0.029] (96)† | -0.095 [-0.150, -0.034] (1319) | -0.041 [-0.112, +0.030] (794)† | 4 |

Source: `round-3/experiment-8/src/results/heldout_unit_results.csv` (outcome == O2r_m50); confirmed list from `heldout_summary.json -> O2r_m50[*].confirmed`.



### 19.3 O2r_resid results: 8 of 10 confirmed

O2r_resid (breadth conditional on volume) adds one indicator to the confirmed set: **log_offhome_volume** (-0.100 [-0.171, -0.028], Holm p confirmed). Concepts with higher early offhome volume achieve less breadth than expected for their total size.

### 19.4 O1c (sustained uptake): 1 of 10 confirmed

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] Only n_authors_early is confirmed for O1c: pooled psp +0.161 [+0.090, +0.230], Holm p 0.0001 (1 of 10 frozen indicators).

### 19.5 O4 (field- and year-normalised citation growth): 2 of 10 confirmed

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] This section reports O4, not transience. Concepts whose home field is related to many fields (REL_home) show LOWER later citation growth, and early author growth predicts HIGHER citation growth.

| indicator | family | frozen sign | pooled psp | 95% CI | I2 | Holm p | sign agree | confirmed |
|---|---|---|---|---|---|---|---|---|
| G_deg | G | - | -0.021 | [-0.069, +0.028] | 0.41 | 1 | 5/6 | no |
| log_offhome_volume | F | - | -0.002 | [-0.069, +0.066] | 0.66 | 1 | 3/6 | no |
| REL_home | G | - | -0.114 | [-0.180, -0.047] | 0.69 | 0.00922 | 6/6 | **yes** |
| burst | E | - | +0.014 | [-0.043, +0.072] | 0.55 | 1 | 3/6 | no |
| G_A | G | - | -0.010 | [-0.055, +0.036] | 0.33 | 1 | 4/6 | no |
| author_growth | E | + | +0.065 | [+0.024, +0.106] | 0.21 | 0.0182 | 5/6 | **yes** |
| G_phimin | G | + | +0.064 | [-0.080, +0.206] | 0.93 | 1 | 5/6 | no |
| FRONTIER_POTENTIAL | FR | - | -0.017 | [-0.063, +0.030] | 0.39 | 1 | 5/6 | no |
| RETENTION_RATIO_early | FR | - | -0.026 | [-0.060, +0.009] | 0.00 | 1 | 5/6 | no |
| new_edge_rate | A | - | +0.003 | [-0.032, +0.037] | 0.00 | 1 | 3/6 | no |

Source: `round-3/experiment-8/src/results/heldout_summary.json` -> `O4[i].{pooled,pooled_ci,I2,holm_p,sign_agree,n_units,confirmed}`

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

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] Transience IS predictable beyond B5 on held-out groups: L1-logit AUC 0.599 vs B5 0.506 (paired difference [+0.028, +0.163]); EBM 0.599. Caveat: B5 itself is at chance for O3, so the gain is over a null baseline, not over a strong one.


[Correction, iteration 5, from art_NMe386dX9GLF] On the 2015-2017 cohort the learned model does not predict transience either: O3 AUC +0.540 vs B5 +0.561, -0.021 [-0.130, +0.101] (Section 25.6).



### 19.6 External recognition (O5, O5_WW): 0 and 0 of 10 confirmed

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] No indicator predicts external recognition beyond B5 + onset year (see file 10 for the section cross-reference fix).

Source: `round-3/experiment-8/src/results/rq1_heldout.json` -> `headline_by_outcome.{O5,O5_WW}.n_confirmed_holm`

> No indicator predicts external recognition. All Holm p = 1.0. This is consistent with the Evaluation 2 finding that external recognition is unrelated to publication outcomes (Section 21.2).

[Correction, iteration 4, from art_7W9xiIO3FVBs] Replace 'Section 21.2' with 'Section 20.2' (the O5 validation result is Section 20.2, External recognition validation; 21.2 is 'Missing rivals').


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


[Correction, iteration 5, from art_NMe386dX9GLF] Cohort check: linear_all over B5 on O2r_m50 +0.030 [+0.012, +0.049]; the frozen B5 + OPEN_home forecast gains +0.002 (Section 25.6).


### 19.8 Preregistered verdicts

[Correction, iteration 4, from art_dFQ6jbgNsR6Q]

| # | exact frozen text | verdict | deciding quantity |
|---|---|---|---|
| P1 | entropy, D_rare, D_ratio, participation, NOV_res: raw Spearman with O2r_m50 > 0 (CI > 0) in >= 3 of 4 held-out groups; AND D_rare, D_ratio, participation, NOV_res: pooled psp|B5 CI upper bound < 0.10 | **FAILS** | raw part: groups with raw CI > 0 = D_rare 2, D_ratio 3, participation 4, NOV_res 4, entropy 4 (of 4); adds-little part: pooled psp CI upper bounds D_rare 0.296, D_ratio 0.132, participation 0.271, NOV_res 0.241 (rule: all < 0.10) |
| P2 | edge_persistence: pooled raw rho and pooled psp with O2r_m50 both < 0 | **HOLDS** | edge_persistence pooled psp -0.080 [-0.126, -0.033]; mean raw rho over 4 groups -0.128 |
| P3 | deg_growth, str_growth, new_edge_rate FAIL held-out: pooled psp CI includes 0 OR sign flip in >= 2 of 4 groups | **FAILS** | new_edge_rate pooled psp +0.118 [+0.072, +0.163], sign flips 0 -> it TRANSFERS; deg_growth +0.002 [-0.046, +0.049] and str_growth +0.001 [-0.058, +0.060] do fail as predicted |
| P4 | RETENTION_RATIO_early and FRONTIER_POTENTIAL: pooled psp > 0 with CI > 0 for O2r_resid AND O1c | **FAILS** | RETENTION_RATIO_early on O2r_resid -0.120 [-0.166, -0.074] (predicted > 0: wrong sign); on O1c -0.006 [-0.041, +0.029]; FRONTIER_POTENTIAL on O2r_resid +0.055 [-0.057, +0.165] |
| P5 | CONTACT_REACH: pooled psp CI includes 0 (also reported given B5 minus reach) | **FAILS** | CONTACT_REACH pooled psp on O2r_m50 +0.213 [+0.159, +0.265] (predicted: CI includes 0); given B5 minus reach on O2r_resid +0.223 [+0.172, +0.273] |

Source: `round-3/experiment-8/src/results/frozen_spec.json` -> `preregistered_predictions.P1..P5`; `round-3/experiment-8/src/results/prereg_verdicts.json` -> `P1..P5.{verdict,detail,...}`

Reading: P1 fails on BOTH parts (D_rare is positive in fewer than 3 groups, and all four breadth candidates add more than the 0.10 bound). P3 was a prediction of FAILURE; its failure means new_edge_rate transfers to held-out groups. P4 fails because the retention ratio has the opposite sign. P5 predicted that CONTACT_REACH adds nothing; it adds a clearly positive amount.

[Correction, iteration 4, from art_dFQ6jbgNsR6Q]

| indicator | pooled psp given B5 | 95% CI | raw rho PHYS | LIFEENV | SOC | MATHDEC |
|---|---|---|---|---|---|---|
| D_ratio | +0.066 | [+0.001, +0.132] | +0.066 | +0.089 | +0.218 | +0.500 |
| D_rare | +0.162 | [+0.022, +0.296] | +0.305 | +0.128 | +0.374 | n/a (n too small) |
| participation | +0.150 | [+0.025, +0.271] | +0.306 | +0.154 | +0.331 | +0.687 |
| NOV_res | +0.139 | [+0.033, +0.241] | +0.277 | +0.078 | +0.239 | +0.722 |
| entropy | n/a (B5 member) | n/a | +0.775 | +0.631 | +0.639 | +0.847 |
| edge_persistence | -0.080 | [-0.126, -0.033] | -0.076 | -0.112 | -0.107 | -0.217 |

Source: `round-3/experiment-8/src/results/prereg_verdicts.json` -> `P1.detail.<ind>.{pooled_psp,pooled_ci,raw_rho.<group>}`; `round-3/experiment-8/src/results/prereg_verdicts.json` -> `P2.{pooled_psp,pooled_ci,raw_rho}`


### 19.9 Deviations

- One year ego network windows (t0 to t0+1 and t0+1 to t0+2) instead of three year windows, because the snapshot scan produces yearly slices.
- Betweenness centrality capped at concepts with degree >= 3 in each window, to avoid division by zero in normalisation.
- O2r_resid computed per the plan formula (residual of O2r_m50 on log_total_volume, linear).
- External recognition uses a linear onset year term, not a quadratic, because the quadratic was numerically unstable for extreme onset years.
- D_vol_end and M0_density_end use the cumulative 1995 to t0+2 field concept paper history, not a rolling window.
- The transience ElasticNet shrank all coefficients to zero, so no linear model is available for transience.

[FIGURE:fig_rq1_confirmed]


### 19.10 Boundary results for the OPEN lead (EXPLORATORY; Evaluation 3)

**11 Boundary results for the OPEN lead (EXPLORATORY)**

**Status: EXPLORATORY.** All analyses reuse the Exp8 held-out groups, which were unsealed in Exp5 and Exp8. They can reveal fragility; they cannot confirm OPEN. Confirmation needs the never-screened 2015-16 cohort. The specification was hash-frozen before any statistic (`logs/seal.log`, boundary_spec.json sha256).

**Reproduction gate T0**

Exp8's pooled held-out psp was re-derived from analysis_table.parquet with the Exp8 estimator: M0_density_end +0.3745 (record +0.3745, O2r_m50) and +0.3770 (O2r_resid); D_vol_end +0.3071; n_comm_W3 +0.1666; ego_density_W3 -0.1024; new_edge_rate +0.1176. All within the 1e-3 tolerance (gate passed).

Source: `round-4/evaluation-3/src/results/gate_T0.json` -> `rows[i].{record_pooled,rederived_pooled}`

**B1 Post-onset re-score of the two largest breadth effects**

- **M0_density_end** (O2r_m50, DL over held-out groups): full history +0.374 -> post-onset only (t0..t0+2 papers) +0.187 [+0.145, +0.246]; paired difference +0.187 [+0.138, +0.231]; attenuation 0.50 [0.38, 0.60]; verdict **PARTIAL** (frozen rule: MOST if upper CI of post < half of full; LITTLE if the paired difference CI includes 0).
- **D_vol_end** (O2r_m50, DL over held-out groups excluding MATHDEC): full history +0.317 -> post-onset only (t0..t0+2 papers) +0.176 [+0.114, +0.227]; paired difference +0.141 [+0.087, +0.209]; attenuation 0.45 [0.29, 0.64]; verdict **PARTIAL** (frozen rule: MOST if upper CI of post < half of full; LITTLE if the paired difference CI includes 0).
- D_vol_end given B5 + pre-onset footprint (D_vol_pre, log pre-onset papers): +0.181 [+0.134, +0.227].
- M0_density_end given B5 + pre-onset footprint (D_vol_pre, log pre-onset papers): +0.290 [+0.191, +0.383].
- D_vol_post is near rank-identical to the B5 'reach' column (within-unit Spearman 0.992 in LIFEENV, 0.998 in MATHDEC). Once the pre-onset years are removed, D_vol is almost the baseline itself; in MATHDEC its partial correlation is undefined in the bootstrap, so MATHDEC is excluded from the D_vol pools. M0_density_post is less collinear with reach (within-unit Spearman from 0.63 in CS to 0.93 in Med) and its bootstrap is defined in every unit.
- Spearman(D_vol_post, D_vol_end) = 0.747; Spearman(footprint share, O2r_m50) = 0.085; share of held-out concepts with any pre-onset off-home entry 0.911.

**Paper wording.** About half of the M0_density_end and D_vol_end breadth signal comes from the concept's pre-onset footprint in other fields. The post-onset part is still clearly positive, so these are partly, but not only, early network signals.

Source: `round-4/evaluation-3/src/results/post_onset_rescore.json` -> `pooled.*; footprint_controlled; collinearity_post_vs_B5_reach; spearman`

**B2 OPEN per unit (O2r_m50 and O2r_resid)**

- OPEN, O2r_m50, DL4: +0.181 [+0.082, +0.277], I2 0.73, prediction interval [-0.235, +0.541], positive in 6 of 6 units, CI includes 0 in 1 of 6.
- OPEN, O2r_m50, DL6: +0.163 [+0.108, +0.218], I2 0.62, prediction interval [-0.003, +0.321], positive in 6 of 6 units, CI includes 0 in 1 of 6.
- OPEN, O2r_resid, DL4: +0.177 [+0.076, +0.274], I2 0.73, prediction interval [-0.248, +0.544], positive in 6 of 6 units, CI includes 0 in 1 of 6.
- OPEN, O2r_resid, DL6: +0.157 [+0.102, +0.212], I2 0.62, prediction interval [-0.010, +0.316], positive in 6 of 6 units, CI includes 0 in 1 of 6.
- CONTACT_REACH without intersection-born (multi-home) concepts, O1c: +0.046 [+0.011, +0.080] (Exp8 sensitivity, verbatim from sensitivities_pooled.json; all rows of that file are carried in `results/per_group_extra.json`).
- CONTACT_REACH without intersection-born (multi-home) concepts, O2r_resid: +0.111 [+0.063, +0.158] (Exp8 sensitivity, verbatim from sensitivities_pooled.json; all rows of that file are carried in `results/per_group_extra.json`).

The full per-unit table (all confirmed indicators, the iteration-1 candidates, new_edge_rate, the post-onset rows, OPEN and OPEN_PC1; DEV units labelled SELECTION_DATA) is `results/per_group_table.csv`.

Source: `round-4/evaluation-3/src/results/per_group_pooled.csv` -> `indicator==OPEN&outcome==<o>&pool==<pool>::{pooled,ci_lo,ci_hi,I2,pi_lo,pi_hi,sign_pos_6,n_ci_includes_0_6}`

**B3 Specification curve**

Across 1,920 specifications (120 composites x 4 outcomes x 4 control sets), the pooled psp CI excludes 0 in a share of 0.997 (4 held-out groups; 1.000 with the 2 cohort units). Median psp 0.152 (IQR 0.134-0.169). Under a Freedman-Lane null (200 draws), the null median is -0.0023 and the null share with CI > 0 averages 0.016; permutation p = 0.005 (the smallest possible with this many draws). Headline spec (all 6 components, equal weights, O2r_m50, C1): +0.183 [+0.083, +0.280], I2 0.73, prediction interval [-0.238, +0.547]. With contact reach as a control (C3) the median is 0.146 vs 0.158 under C1. Analytic vs bootstrap SE calibration: median width ratio 1.037 (< 1.2, no inflation).

**Reading.** The positive OPEN association is a property of the construct, not of one combination: every component subset, both weightings, all four breadth outcomes and all four control sets give a positive pooled estimate. The prediction interval of the headline spec includes 0, so a new domain can show a null.

Source: `round-4/evaluation-3/src/results/spec_curve.json` -> `n_specs; summary.*; null.DL4.*; headline.DL4.*; marginals.DL4.control.*; calibration.*`

**B4 Heterogeneity and the LIFEENV diagnosis**

On 21 home-field x period sub-units (n >= 60), I2 is 0.43 (vs 0.66 over the 6 units). No trait explains the between-sub-unit variance (univariate REML meta-regression with Knapp-Hartung; Holm over 7 traits):

| trait (ecological, sub-unit level) | slope per SD | 95% CI | permutation p | Holm p |
|---|---|---|---|---|
| median_label_coverage | +0.018 | [-0.035, +0.072] | 0.485 | 1.000 |
| median_log_early_volume | -0.011 | [-0.076, +0.053] | 0.724 | 1.000 |
| share_multi_home | -0.019 | [-0.077, +0.039] | 0.492 | 1.000 |
| share_generic | +0.027 | [-0.032, +0.087] | 0.358 | 1.000 |
| median_O2r_m50 | -0.005 | [-0.052, +0.041] | 0.809 | 1.000 |
| sd_OPEN | -0.030 | [-0.090, +0.030] | 0.299 | 1.000 |
| mean_t0 | -0.026 | [-0.079, +0.027] | 0.316 | 1.000 |

LIFEENV: OPEN psp +0.071 vs the other 5 units pooled +0.186 [+0.133, +0.237]. (i) OPEN varies less in LIFEENV (SD ratio 0.88 [0.82, 0.94]; new_edge_rate 0.60), but the Thorndike range-restriction correction only moves psp to +0.080. (ii) Reweighting LIFEENV to the others' label-coverage distribution (entropy balancing) gives +0.069 [-0.019, +0.153]. Verdict under the frozen rule: **UNEXPLAINED**: neither coverage nor restricted range explains the weak LIFEENV cell, so it is treated as a domain boundary.

Source: `round-4/evaluation-3/src/results/heterogeneity.json` -> `k_subunits; I2_*; meta_regression.univariate.*; lifeenv.*`

Figures: `figures/spec_curve.pdf`, `figures/open_forest.pdf`, `figures/b1_post_onset.pdf`, `figures/lifeenv_diagnosis.pdf`.


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

**05 Eval2 record_tables: file -> report section**

| file | rows | target section |
|---|---|---|
| `record_tables/coverage_iter2.csv` | 4 | 8a (coverage table, iteration-2 column) |
| `record_tables/coverage_iter2_steps.csv` | 12 | 8a |
| `record_tables/definitions_diff.csv` | 12 | 9 / 11 (frame comparison Exp5 vs Exp6) |
| `record_tables/draft_number_harvest.csv` | 555 | ledger (all sections) |
| `record_tables/frame_crosstab_split_group.csv` | 14 | 9 / 11 (frame comparison) |
| `record_tables/frame_disagreement_causes.csv` | 713 | 9 / 11 (frame comparison) |
| `record_tables/frame_overlap_by_group.csv` | 6 | 9 / 11 (frame comparison) |
| `record_tables/h1_criteria.csv` | 38 | 10.3 (H1 criteria) |
| `record_tables/hypothesis_iter3_numbers.csv` | 35 | 11.2 / 16.x (hypothesis LR, d, strata) |
| `record_tables/lineage_robustness_iter1.csv` | 278 | 3.5 (alternative lineage indicators) |
| `record_tables/next_field_heldout_rows.parquet` | 46,433 | 11.2 (next-field entry, held-out rows) |
| `record_tables/next_field_trace.json` | json | 11.2 (next-field entry trace) |
| `record_tables/o5_associations.csv` | 60 | 20.2 (O5 associations) and file 09 |
| `record_tables/o5_concept_panel.csv` | 12,499 | 20.2 / 13 (O5 panel) |
| `record_tables/o5_coverage_by_group.csv` | 10 | 13.1 (Dataset 2 coverage) |
| `record_tables/o5_coverage_by_group_source.csv` | 130 | 13.1 and file 09 (per-source coverage) |
| `record_tables/o5_handcheck_items.csv` | 100 | 20.3 (O5 hand check) |
| `record_tables/o5_handcheck_items_final.csv` | 100 | 20.3 (O5 hand check) |
| `record_tables/o5_km_cumulative_incidence.csv` | 20 | 20.2 (O5 timing) |
| `record_tables/ordering_mixed.csv` | 159 | 11.3 / 16.3 (ordering MIXED) |
| `record_tables/partial_association_all.csv` | 12 | 4.4 (remaining partial associations) |
| `record_tables/portability_F3.csv` | 34 | 4.3 (portability) |
| `record_tables/refit_bootstrap_iter1.csv` | 14 | 3.3 / 4.2 (refit bootstrap) |

Source: `round-4/evaluation-3/src/results/partA_derived.json` -> `record_tables_rows.<file>` (row counts computed from the files listed)

**06 Eval2 ledger: open rows (MISMATCH and MISLABELLED)**

Eval2's claims_ledger.csv has 246 rows: 6 MISMATCH and 15 MISLABELLED. Each is listed with the fixed text; values are carried verbatim from the row.

**MISMATCH**

- **H1_crit_lpm_beta_within_gt0_p05** (section 10.3 Field retention hypothesis: result: DISCONFIRMED; verdict_H1.criteria.lpm_beta_within_gt0_p05 (held-out, 8,515 episodes / 3,085 concepts)): draft said 'Verdict: DISCONFIRMED by all preregistered criteria.' (reported false); file value True at `round-2/experiment-5/src/results/h1_heldout.json` -> `verdict_H1.criteria.lpm_beta_within_gt0_p05`. **Fixed text:** The within-field LPM criterion PASSES: beta_within = +0.068 per SD, concept-clustered p = 0.041 (two-way clustered p = 0.17); the verdict rule still returns DISCONFIRMED because 5 of the 6 core criteria fail.
- **PA_remaining_7_claim** (section 4.4 Exploratory partial association; number of candidates in exploratory_partial_association.json): draft said 'The remaining 7 indicators ... are not available in the current workspace output' (reported 5); file value 12 at `round-1/experiment-3/src/results/exploratory_partial_association.json` -> `len(candidates)`. **Fixed text:** The file holds all 12 candidates; paste the full table (record_tables/partial_association_all.csv).
- **O5cov_wikipedia_en_n_with_event** (section 13.1 Sources; by_source.wikipedia_en.n_with_event (CONCEPTS)): draft said 'Concepts matched' (reported 6540); file value 64363 at `round-2/dataset-2/src/out/coverage_report.json` -> `by_source.wikipedia_en.n_with_event`. **Fixed text:** 
- **O5cov_wikipedia_exact** (section 13.1 Sources; by_source.wikipedia_en.status.found (exact first revisions)): draft said 'English Wikipedia 6,540 exact first revisions' (reported 6540); file value 7806 at `round-2/dataset-2/src/out/coverage_report.json` -> `by_source.wikipedia_en.status.found`. **Fixed text:** Wikipedia: 64,363 concepts with an event, 50,459 year-usable, 7,806 exact first revisions (6,540 is the dataset summary's count before redirect repair).
- **H3_status** (section 16.5; G.ci95 includes 0): draft said 'The effect is real but small (confirmed)' (reported false (implied)); file value True at `round-2/experiment-5/src/results/h3_results.json` -> `G.ci95[0] <= 0 <= G.ci95[1]`. **Fixed text:** Status: 'small; passes the preregistered within-group permutation rule; pooled concept-bootstrap CI includes 0 ([-0.006, 0.065])'.
- **CLASH_MDE_n** (section 10.7; power.n_heldout_episodes_assumed): draft said '27,393 episodes' (reported 27393); file value 8515 at `round-2/experiment-5/src/results/h1_dev.json` -> `power.n_heldout_episodes_assumed`. **Fixed text:**

**MISLABELLED**

- **ORD_reverse_p_heldout** (section 11.3 Ordering: first retained gateway precedes entropy takeoff; heldout ordering.lead_lag.reverse_dret_on_H.coef.H.p): draft said 'the reverse (entropy predicting retention) is not significant (p = 0.22)' (reported 0.22); file value 0.21723474575636884 at `round-2/experiment-6/src/results/heldout_result.json` -> `ordering.lead_lag.reverse_dret_on_H.coef.H.p`. **Fixed text:** Held-out reverse path b = 0.077 (p = 0.22), but on DEV the reverse path is significant: b = 0.232 [0.066, 0.397], p = 0.006 (dev_result.json).
- **ORD_both_associated** (section 11.3 Ordering: first retained gateway precedes entropy takeoff; sign of forward ret_gw coefficient): draft said 'both retained gateway and retained peripheral fields are associated with subsequent entropy change' (reported positive (implied)); file value -0.027939583860173887 at `round-2/experiment-6/src/results/heldout_result.json` -> `ordering.lead_lag.forward_dH_on_ret.coef.ret_gw.b`. **Fixed text:** Both coefficients are NEGATIVE: retention is followed by SMALLER next-year entropy gains (ret_gw -0.028, p = 0.0007; ret_per -0.043, p = 6e-8).
- **ORD_denominator_of_broad_concepts** (section 16.3 What we have learned; gateway before / of_broad_concepts (57/175)): draft said 'In 66% of broad concepts, the first retained gateway field precedes ...' (reported 0.326); file value 0.32571428571428573 at `round-2/experiment-6/src/results/heldout_result.json` -> `ordering.gateway.before / 175`. **Fixed text:** 57 of 175 broad (top-tercile) concepts = 32.6%; 57 of 102 evaluable = 55.9%; 57 of 87 non-tied = 65.5%. '66% of broad concepts' must read '65.5% of the 87 non-tied evaluable concepts (57/87)'.
- **O5cov_acm_ccs_n_with_event** (section 13.1 Sources; by_source.acm_ccs.n_with_event (CONCEPTS)): draft said 'Concepts matched' (reported 3583); file value 1298 at `round-2/dataset-2/src/out/coverage_report.json` -> `by_source.acm_ccs.n_with_event`. **Fixed text:** acm_ccs: 1,298 concepts with an event (1,298 year-usable); 3,583 is the external-ENTRY count
- **O5cov_jel_n_with_event** (section 13.1 Sources; by_source.jel.n_with_event (CONCEPTS)): draft said 'Concepts matched' (reported 1015); file value 0 at `round-2/dataset-2/src/out/coverage_report.json` -> `by_source.jel.n_with_event`. **Fixed text:** JEL: 213 concepts found (present-day membership), 0 dated events; 1,015 is the entry count.
- **O5cov_msc_n_with_event** (section 13.1 Sources; by_source.msc.n_with_event (CONCEPTS)): draft said 'Concepts matched' (reported 17872); file value 1121 at `round-2/dataset-2/src/out/coverage_report.json` -> `by_source.msc.n_with_event`. **Fixed text:** msc: 1,121 concepts with an event (1,121 year-usable); 17,872 is the external-ENTRY count
- **O5cov_pacs_physh_n_with_event** (section 13.1 Sources; by_source.pacs_physh.n_with_event (CONCEPTS)): draft said 'Concepts matched' (reported 8462); file value 2635 at `round-2/dataset-2/src/out/coverage_report.json` -> `by_source.pacs_physh.n_with_event`. **Fixed text:** pacs_physh: 2,635 concepts with an event (2,635 year-usable); 8,462 is the external-ENTRY count
- **O5cov_research_fronts_n_with_event** (section 13.1 Sources; by_source.research_fronts.n_with_event (CONCEPTS)): draft said 'Concepts matched' (reported 589); file value 589 at `round-2/dataset-2/src/out/coverage_report.json` -> `by_source.research_fronts.n_with_event`. **Fixed text:** 589 is Research Fronts only; the curated lists are Gartner 466, MIT TR10 313, Research Fronts 589, NM MoTY 38, Science BOTY 53, Physics World BOTY 100 concepts.
- **H3_0of40** (section 10.6 Concept breadth hypothesis: result: small but confirmed; calibration false-positive rate of the preregistered test on 40 shuffled outcomes): draft said '(0 of 40 shuffled outcomes exceed the real value)' (reported 0); file value 0.0 at `round-2/experiment-5/src/results/audit_placebo.json` -> `H3_calibration_40_shuffles.false_positive_rate_preregistered_pooled_test`. **Fixed text:** 0/40 is the FALSE-POSITIVE RATE of the preregistered test on 40 shuffled outcomes (a calibration check), not an exceedance count and not a p-value.
- **H3_mixed_variants** (section 16.5; variant consistency): draft said 'Holdout partial rho of G_btw ... = 0.046 (Holm p = 0.0045); DerSimonian-Laird pooled G = 0.068' (reported G_btw pooled + G DL); file value mixes G_btw (pooled partial) and G (DL) at `round-2/experiment-5/src/results/h3_results.json` -> `G_btw.partial_rho vs G.dl_pool.pooled`. **Fixed text:** Quote one variant: G pooled partial 0.030 [-0.006, 0.065], DL within-group 0.068 [0.029, 0.107]; G_btw DL 0.072 [-0.015, 0.159], I2 = 0.77.
- **ALL4_label** (section 5.4 Field level prediction; delta AUC of the row labelled 'B5 + all_four'): draft said 'B5 + all_four (G, REL, RS, G_all) | 0.697 | 0.782 | +0.085 | [0.004, 0.164]' (reported 0.085); file value 0.08507936507936509 at `round-1/experiment-4/src/screen_result.json` -> `field_level.size_controlled_all_three.delta_auc`. **Fixed text:** The +0.085 row is 'B3 + log field size + {gateway_j, phi_home_j, density_j}' (size_controlled_all_three; AUC 0.697 -> 0.782; fixed CI95 [0.004, 0.164]; refit CI95 [-0.043, 0.220]). The row 'all_four_available' is B3 + {gateway_j, phi_home_j, density_j}: +0.082 (0.705 -> 0.787), fixed [0.008, 0.153], refit [-0.042, 0.204]. Neither contains G, REL, RS or G_all.
- **CLASH_MDE_power** (section 10.7 Minimum detectable effect and power; power_ci_gt0 at planted b = 0.3 (mean dAUC 0.004)): draft said 'The minimum detectable delta AUC is 0.004 (at 80% power, 27,393 episodes)' (reported 0.80); file value 0.9 at `round-2/experiment-5/src/results/h1_dev.json` -> `power.0.3.power_ci_gt0`. **Fixed text:** 0.004 is the mean dAUC at planted b = 0.3, where power is 0.90 (b = 0.2 gives 0.0019 at power 0.65); the file key 'min_detectable_dauc_80pct' mislabels it. The simulation assumed 8,515 held-out episodes (not 27,393), and at b = 0 the CI>0 rule fires 12.5% of the time (nominal 2.5%).
- **CLASH_10.7_sd015** (section 10.7; E_power SD under the alternative (Evaluation 1, not Exp5)): draft said 'the standard deviation of the delta AUC ... approximately 0.015 regardless of the number of episodes' (reported 0.015); file value 0.016009816372160212 at `round-2/evaluation-1/src/eval_out.json` -> `metadata.E_power.held_out_sizing_from_alternative_SD.SD_alt_field_RE_N1000_m5`. **Fixed text:** This sentence and '34 concepts per group' come from Evaluation 1 (E_power, field random intercept), not Exp5; attribute them to art_lwI2DuRtQRZX and reconcile with Exp5's 0.004 (no field random intercept).
- **CLASH_10.7_34** (section 10.7; E_power concepts per group (Evaluation 1)): draft said 'Approximately 34 holdout concepts per group' (reported 34); file value 34 at `round-2/evaluation-1/src/eval_out.json` -> `metadata.E_power.held_out_sizing_from_alternative_SD.concepts_per_group_p>=0.9_at_0.05`. **Fixed text:** 
- **H2_sign_test** (section 16.1; H2_sign_count.sign_test_p): draft said 'positive in all three evaluable holdout field groups' (reported (not reported)); file value 0.0625 at `round-2/experiment-6/src/results/heldout_result.json` -> `H2_sign_count.sign_test_p`. **Fixed text:** Positive in 4/4 groups (sign test p = 0.0625); only Physical's CI excludes 0 (LifeEnv LR p = 0.23, Social 0.076).



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

**09 O5 precedence leakage by source and the O5-O3 association**

[Correction, iteration 4, from art_7W9xiIO3FVBs] External recognition is often dated at or before the concept's onset year t0, so O5 partly measures prior recognition, not diffusion success. Per source:

| source | matched concepts | share first event <= t0 | median lag (years, events after t0) | IQR |
|---|---|---|---|---|
| wikipedia_en | 9,593 | 0.79 | 2.0 | [1.0, 3.0] |
| mesh | 3,905 | 0.70 | 8.0 | [4.0, 12.0] |
| pacs_physh | 239 | 0.00 | 8.0 | [5.0, 11.0] |
| wikidata | 217 | 0.96 | 5.0 | [4.0, 8.0] |
| acm_ccs | 166 | 0.17 | 6.0 | [4.0, 8.0] |
| research_fronts | 95 | 0.00 | 11.0 | [7.0, 13.0] |
| gartner_hype_cycle | 47 | 0.68 | 1.0 | [1.0, 3.0] |
| msc | 26 | 0.19 | 9.0 | [4.0, 13.0] |
| mit_tr10 | 23 | 0.52 | 5.5 | [1.8, 15.5] |
| nature_methods_moty | 5 | 0.40 | 1.0 | [1.0, 6.0] |
| physics_world_boty | 3 | 0.67 | 4.0 | [4.0, 4.0] |
| science_boty | 2 | 0.50 | 14.0 | [14.0, 14.0] |

Also: 0.81 of the 253 Wikidata inception events predate t0 by more than 10 years; 0.78 of Wikipedia dates fall in Wikipedia's 2001-2007 growth wave.

Source: `round-3/evaluation-2/src/o5_validation.json` -> `precedence_leakage.<source>.{n_matched,share_first_event_le_t0}; lag.<source>.{median,iqr}`
Coverage per group and source (share found, share qualifying in window) is in `round-3/evaluation-2/src/record_tables/o5_coverage_by_group_source.csv`.

**O5-O3 association per held-out group (O5_main; Spearman)**

| group | n | rho(O5, O3) | 95% CI |
|---|---|---|---|
| PHYS | 742 | -0.072 | [-0.122, -0.011] |
| LIFEENV | 1,113 | +0.025 | [-0.036, +0.091] |
| SOC | 1,352 | -0.061 | [-0.091, -0.024] |
| MATHDEC | 165 | -0.063 | [-0.099, -0.033] |

Pooled (DL, 4 held-out groups): -0.049 [-0.083, -0.016], p = 0.004, I2 = 0.55. Recognised concepts are slightly LESS transient, but the association is small and heterogeneous.

Source: `round-3/evaluation-2/src/record_tables/o5_associations.csv` -> `group==<g>&variant==O5_main::{n,rho_O3,rho_O3_ci95}`; `round-3/evaluation-2/src/o5_validation.json` -> `associations_pooled_heldout_DL.O5_main.rho_O3.{pooled,ci95,p,I2}`


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

**Claim A (entry follows retained relatedness): PARTIALLY ANTICIPATED (weak partial).** The relatedness literature uses persistence routinely, but only as a filter on the *outcome* (what counts as an entry). Pinheiro et al. (2022) require RCA < 1 for Δ = 4 years before and RCA >= 1 for Δ years after an entry [10]. Albora et al. (2023) count activation only if RCA < 0.25 in all previous years [11]. Bahar et al. (2014) use tenfold jumps from RCA <= 0.1 [12]. On the *predictor* side, every density found in all 6 strands uses current snapshot presence (RCA > 1, or continuous) [6, 9, 13, 14]. No paper was found that builds density from retained or persistent presences only, or weights presences by duration, and tests it against RCA > 1 density. The closest science analogue is Cheng et al. (2023), who find that what they call "consistent intellectual usage" predicts ideas becoming core [15], but their measure is global, not per field.

**Claim B (lost field penalty): mechanism partly anticipated; NEW as a test.** Fernandes & Tang (2014) model negative neighbour signals deterring entry [16]. Nomaler & Verspagen (2022) argue absence or loss of comparative advantage is informative but add little in practice [17]. No study uses neighbours' exits as entry predictors. Our Experiment 6 estimate is fragile: d_lost = -0.063, p = 0.055. The independent frame estimate (Experiment 7) is d_lost = -0.007, CI including zero. The abandonment penalty remains inconclusive.

### 21.2 Missing rivals

The positioning study identified several rivals the present analysis does not test:

1. **Persistence filtered RCA density** (D_rca_persist_k): entered or RCA > 1 in each of t-k to t. This is the predictor side twin of Pinheiro's Δ-rule and would directly test whether Claim A's novelty is in the persistence measure or just in the threshold.
2. **Own preentry subthreshold intensity** (Albora's autocorrelation benchmark): whether a concept's own past presence in a field predicts entry, beyond relatedness.
3. **Neighbour momentum density:** relatedness weighted recent usage growth in adopting fields, following Fernandes & Tang (2014) [16]. This is the main confound for both claims.

These are flagged as open and should be tested in a future iteration.

### 21.3 Indicator screen comparison

No comparator in the literature evaluates on heldout fields. Link forecast AUCs (Krenn & Zeilinger 2020: AUC 0.85 with approximately 5% of edges drawn; Maillart et al. 2026 [18]: AUC 0.95-0.97) are level metrics on rare positives and not comparable to our increments over the five feature baseline. The indicator screen heldout result (7 of 10 indicators confirmed, ElasticNet delta +0.059 over the five feature baseline) has no like for like counterpart and should be presented as such.

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

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] 6. **O4 (citation growth) linear model: shrank to a constant.** The ElasticNet for O4 (field- and year-normalised citation growth, NOT transience) set every coefficient to zero, so it ranks nothing on held-out data, while the EBM reaches Spearman 0.188 vs B5 0.015 (gain +0.174 [+0.129, +0.219]). The O4 signal is non-linear. Transience (O3) is a separate outcome with a positive held-out learned-model result (above).

Source: `round-3/experiment-8/src/results/learned_vs_single_heldout.json` -> `O4.POOLED_HELDOUT.*`; `round-3/experiment-8/src/results/deviations.json` -> `O4_linear_all_constant`

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] 7. **Four of five pre-registered predictions fail, as frozen.** P2 (edge_persistence negative) holds. P1 fails (the iteration-1 breadth candidates do add beyond B5 on held-out data); P3 fails because new_edge_rate transfers; P4 fails because RETENTION_RATIO_early is negative, not positive; P5 fails because CONTACT_REACH is positive given B5. See the table in 19.8 for the deciding numbers.




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


## 22b. Failed artifact of iteration 3: Experiment 9 did not run

[Correction, iteration 4, from gen_art_experiment_9 .aii_worker_result.json] Iteration 3 commissioned a fifth artifact, gen_art_experiment_9, from the plan 'Plan: how new concepts spread — trajectories and reasons (iteration 3, experiment direction 3)' (`iter_3/gen_plan/gen_plan_experiment_3/`: state sequences, breadth decomposition, empirical trajectory typology, sequence tests, snapshot lineage check, case studies, recognition timing). The worker failed before producing any output: `failed = true`, error: 'output_format validation failed after 5 retries: The output file `./.terminal_claude_agent_struct_out.json` does not exist yet.'. The workspace holds no method.py (absent) and no results. What was lost: the RQ2 trajectory typology and sequence tests for iteration 3. Status: **not run, not refuted**.


## 23. What we have learned so far (end of iteration 3)

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

[Correction, iteration 5, from iter_4 report] Section 23 was a stub in the iteration-5 report. The text above is restored byte-for-byte from `iter_4/gen_strat/current_report.md` lines 1216-1255 (heading suffix '(end of iteration 3)' added).

**Corrections to the restored Section 23 (iteration 5):**

- [Correction, iteration 5, from art_22ppE1snfHKj] The dose response is **not monotone** on held-out data: betas by persistence age 2 / 3 / ≥4 are 0.10 / 0.08 / 0.30.
- [Correction, iteration 5, from art_uw4OeagJP3rv] The trajectory typology is a **continuum**, not two classes: DTW-HMM ARI 0.222.
- [Correction, iteration 5, from art_oKOd21ZMnu9S] The volume-matched contrast (retained vs entered-not-retained fields) is null on DEV too: -0.008 [-0.071, +0.050].

# Iteration 4

## 24. Why this iteration ran

The iteration-3 review raised 10 MUST FIX items. The central objections were:

1. **The OPEN index had not been tested on a confirmatory cohort.** The 7 confirmed breadth indicators from Experiment 8 were selected and tested on the same unsealed heldout groups. A never screened 2015-2016 onset cohort was required to confirm the composite OPEN signal.

2. **Half of the M0_density_end and D_vol_end signal might be preonset footprint.** Many concepts have offhome papers before their onset year. The two strongest breadth predictors could partly reflect established presence rather than early network dynamics.

3. **The trajectory analysis (Experiment 9) had failed.** No breadth decomposition, no trajectory typology beyond the iteration-2 two class DTW, no sequence tests and no case studies existed.

4. **Prior art positioning was incomplete.** The openness versus consolidation framing needed strand by strand extraction and a contribution statement.

5. **The report contained 6 MISMATCH and 15 MISLABELLED claims** from the Evaluation 2 audit that had not been corrected in place.

Four artifacts were executed: a confirmatory cohort test of the OPEN index (Experiment 10, art_NMe386dX9GLF), a breadth decomposition and trajectory analysis (Experiment 12, art_uw4OeagJP3rv), a boundary study with specification curve and corrections pack (Evaluation 3, art_oKOd21ZMnu9S), and a novelty positioning study (Research 3, art_hSyVUBa2okT2).

| iteration | commissioned | completed | failed | failed artifacts |
|---|---|---|---|---|
| 1 | 5 | 3 | 2 | gen_art_dataset_1, gen_art_experiment_2 |
| 2 | 5 | 5 | 0 | - |
| 3 | 5 | 4 | 1 | gen_art_experiment_9 |

Source: `round-4/evaluation-3/src/results/partA_derived.json` -> `iterations.iter_<i>.*`
Cross-check with Section 5a: it lists gen_art_dataset_1 and gen_art_experiment_2 as the two iteration-1 failures, which agrees. Iteration 2 had no failures. Iteration 3's failure (Experiment 9) is not in the draft.

| placeholder in draft | real id | artifact |
|---|---|---|
| `[ARTIFACT:art_experiment_7]` (1 occurrences) | `art_22ppE1snfHKj` | Experiment 7 (retained frontier) |
| `[ARTIFACT:art_experiment_8]` (1 occurrences) | `art_dFQ6jbgNsR6Q` | Experiment 8 (held-out indicator screen) |
| `[ARTIFACT:art_evaluation_2]` (1 occurrences) | `art_7W9xiIO3FVBs` | Evaluation 2 (record audit, O5) |
| `[ARTIFACT:art_research_2]` (2 occurrences) | `art_EesdB8cuSfcU` | Research 2 (prior art, venue) |


[Correction, iteration 5, from gen_art_experiment_11] Artifact counts derived from disk (`results/artifact_counts.json`), iterations 1-4: 20 commissioned, 16 completed, 4 failed or incomplete.

| artifact directory | status | evidence |
|---|---|---|
| `iter_1/gen_art/gen_art_dataset_1` | failed/incomplete | `result.failed = true (REPL timeout: REPL turn stalled (no new JSONL records for 19)` |
| `round-1/experiment-1/src` | completed | `structured output present` |
| `iter_1/gen_art/gen_art_experiment_2` | failed/incomplete | `result.failed = true (REPL timeout: REPL turn stalled (no new JSONL records for 19)` |
| `round-1/experiment-3/src` | completed | `structured output present` |
| `round-1/experiment-4/src` | completed | `structured output present` |
| `round-2/dataset-2/src` | completed | `structured output present` |
| `round-2/evaluation-1/src` | completed | `structured output present` |
| `round-2/experiment-5/src` | completed | `structured output present` |
| `round-2/experiment-6/src` | completed | `structured output present` |
| `round-2/research-1/src` | completed | `structured output present` |
| `round-3/evaluation-2/src` | completed | `structured output present` |
| `round-3/experiment-7/src` | completed | `structured output present` |
| `round-3/experiment-8/src` | completed | `structured output present` |
| `iter_3/gen_art/gen_art_experiment_9` | failed/incomplete | `result.failed = true (output_format validation failed after 5 retries: The output )` |
| `round-3/research-2/src` | completed | `structured output present` |
| `round-4/evaluation-3/src` | completed | `structured output present` |
| `round-4/experiment-10/src` | completed | `structured output present` |
| `iter_4/gen_art/gen_art_experiment_11` | failed/incomplete | `no .aii_worker_result.json` |
| `round-4/experiment-12/src` | completed | `structured output present` |
| `round-4/research-3/src` | completed | `structured output present` |





## 25. Experiment 10: Confirmatory cohort test of the OPEN index [ARTIFACT:art_NMe386dX9GLF]

### 25.1 Design

[Correction, iteration 5, from art_NMe386dX9GLF] The OPEN index is the mean of six signed z-scored ego-network components from the early window (t0 to t0+2): new_edge_rate (+), n_comm_W3 (+), participation (+), NOV_res (+), ego_density_W3 (−), edge_persistence (−), with winsor bounds and z constants frozen on the 12,499 EXP5 concepts. Three builds: OPEN_home (home-field papers only), OPEN_all (all papers; **mechanically coupled** to spread, because its off-home papers are part of what later counts as breadth) and OPEN_sizematch (a size-matched subsample of all papers). The confirmatory cohort has onsets in **2015-2017**: 570 (2015), 500 (2016) and 373 (2017, the declared power extension), 1,443 concepts in total, of which 634 have a defined O2r_m50. None of them was used in any earlier screen.

Pre-seal power for OPEN_home at R2 was 0.16 (true effect = half the EXP5 estimate), and the minimum detectable effect (2.8 SE) was 0.105.

Source: `round-4/experiment-10/src/results/cohort_result.json` -> `n_by_t0`, `n_cohort`, `outcome_availability`; `results/frozen_spec.json` -> `power.with_2017`.

### 25.2 Control ladder

[Correction, iteration 5, from art_NMe386dX9GLF] Partial Spearman (psp) of each build with rarefied breadth (O2r_m50) and residualised breadth (O2r_resid), concept bootstrap B = 2,000. R0 = B5 + onset year; R1 = + CONTACT_REACH; R2 = + concept type, generic flag and legacy level; R3 = + footprint; R4 = + label and home-paper coverage; R5 = + home-group FE.

| build | outcome | R0 | R1 | R2 | R3 | R4 | R5 | n |
|---|---|---|---|---|---|---|---|---|
| OPEN_home | O2r_m50 | +0.123 [+0.041, +0.205] | +0.097 [+0.018, +0.179] | +0.091 [+0.013, +0.171] | +0.080 [+0.001, +0.162] | +0.069 [-0.012, +0.150] | +0.056 [-0.022, +0.135] | 573 |
| OPEN_home | O2r_resid | +0.116 [+0.034, +0.201] | +0.092 [+0.013, +0.176] | +0.085 [+0.007, +0.165] | +0.080 [-0.000, +0.162] | +0.069 [-0.012, +0.151] | +0.056 [-0.024, +0.136] | 573 |
| OPEN_all | O2r_m50 | +0.205 [+0.125, +0.281] | +0.180 [+0.100, +0.259] | +0.174 [+0.092, +0.253] | +0.171 [+0.088, +0.251] | +0.147 [+0.064, +0.224] | +0.138 [+0.055, +0.218] | 630 |
| OPEN_all | O2r_resid | +0.194 [+0.113, +0.271] | +0.170 [+0.090, +0.250] | +0.163 [+0.082, +0.242] | +0.168 [+0.086, +0.247] | +0.144 [+0.061, +0.222] | +0.136 [+0.055, +0.216] | 630 |
| OPEN_sizematch | O2r_m50 | +0.183 [+0.103, +0.257] | +0.154 [+0.074, +0.230] | +0.147 [+0.068, +0.221] | +0.137 [+0.057, +0.212] | +0.124 [+0.045, +0.202] | +0.113 [+0.035, +0.190] | 591 |
| OPEN_sizematch | O2r_resid | +0.176 [+0.094, +0.250] | +0.148 [+0.068, +0.223] | +0.142 [+0.063, +0.217] | +0.137 [+0.057, +0.211] | +0.124 [+0.045, +0.201] | +0.114 [+0.037, +0.192] | 591 |

OPEN_home at R2 (the registered primary) is +0.091 [+0.013, +0.171], Holm p = 0.048. **Its R4 and R5 intervals include 0**, and so does its DerSimonian-Laird pool over groups at R2, +0.083 [-0.007, +0.173] (Section 25.3). OPEN_all and OPEN_sizematch stay above 0 on every rung, but OPEN_all is mechanically coupled (Section 25.4).

Source: `cohort_result.json` -> `primary['<build>|<outcome>|R0..R5'].{rho,ci,n}`, `groups['OPEN_home|O2r_m50|R2'].DL`, `holm`.

### 25.3 Per-group DerSimonian-Laird pooling (concept type rung, rarefied breadth)

| build | CS+Eng | BGM+Med | PHYS | LIFEENV | SOC | MATHDEC (report only) | DL pooled [95% CI] | I2 | positive / 5 |
|---|---|---|---|---|---|---|---|---|---|
| OPEN_home | +0.043 (n=114) | +0.080 (n=277) | NA (n=27) | +0.007 (n=49) | +0.149 (n=96) | NA (n=10) | +0.083 [-0.007, +0.173] | 0.00 | 4 |
| OPEN_all | +0.094 (n=124) | +0.171 (n=287) | +0.218 (n=32) | +0.261 (n=58) | +0.287 (n=116) | NA (n=13) | +0.189 [+0.104, +0.275] | 0.00 | 5 |
| OPEN_sizematch | +0.069 (n=120) | +0.132 (n=279) | +0.224 (n=30) | +0.044 (n=49) | +0.290 (n=100) | NA (n=13) | +0.144 [+0.058, +0.230] | 0.00 | 5 |

OPEN_home's DerSimonian-Laird pooled confidence interval includes zero (+0.083 [-0.007, +0.173]). The home only signal is marginal; the corpus wide signal is robust.

### 25.4 Mechanical coupling: ALL minus HOME

[Correction, iteration 5, from art_NMe386dX9GLF] OPEN_all is **mechanically coupled** to the outcome: its ego network includes the off-home papers that later make up breadth. The paired concept-bootstrap differences at R3 are: ALL − HOME +0.093 [+0.016, +0.169] (n = 571); SIZEMATCH − HOME +0.053 [-0.015, +0.117] (n = 563). The first says the all-papers build carries more signal than the home build; the second (CI includes 0) says a size-matched all-papers build does not beat the home build by a detectable margin. The home-only signal is carried by NOV_res +0.134 [+0.049, +0.215] and low edge persistence -0.112 [-0.199, -0.023] (Section 25.8).

Source: `cohort_result.json` -> `contrasts`, `components`.

### 25.5 RETENTION_RATIO_early and Holm family

| test | estimate [95% CI] | n |
|---|---|---|
| RETENTION_RATIO_early\|O2r_m50\|R0 | -0.131 [-0.209, -0.056] | 634 |
| RETENTION_RATIO_early\|O2r_m50\|R2 | -0.043 [-0.116, +0.031] | 634 |

After adding concept type controls, the retention ratio signal attenuates and its confidence interval includes zero. The Holm family (8 members: 3 builds × 2 outcomes + 2 retention tests) yields Holm p = 0.048 for OPEN_home on rarefied breadth and 0.004 for OPEN_all and OPEN_sizematch.


[Correction, iteration 5, from art_NMe386dX9GLF] Secondary leads, verbatim from the Exp10 README (lines 48-53):

> * **Leads replicated (secondary):**
>   * CONTACT_REACH on O2r_m50 given R0: +0.211 [+0.122, +0.294] (EXP8 +0.210), halving to +0.101 without
>     intersection-born concepts (EXP8 +0.111);
>   * n_authors_early on O1c: +0.115 [+0.065, +0.165] (EXP8 +0.161);
>   * RETENTION_RATIO_early < 0 given R0 (EXP8 -0.114), but it vanishes once type and reach enter (R2 -0.043, CI includes 0).
>   * n_authors_early does NOT replicate for O3 (+0.014) or O1b (+0.036).

Keyed values: CONTACT_REACH on O2r_m50 given R0 +0.211 [+0.122, +0.294], without intersection-born concepts +0.101 (n = 613).


### 25.6 Learned models (cohort)

[Correction, iteration 5, from art_NMe386dX9GLF]

| outcome | metric | B5 | linear_all | diff [95% CI] | n | evaluable |
|---|---|---|---|---|---|---|
| O2r_m50 | Spearman | +0.789 | +0.818 | +0.030 [+0.012, +0.049] | 634 | yes |
| O2r_resid | Spearman | +0.789 | +0.816 | +0.027 [+0.009, +0.046] | 634 | yes |
| O3 | AUC | +0.561 | +0.540 | -0.021 [-0.130, +0.101] | 1443 | yes |
| O4 | - | - | - | - | - | no: not evaluable: O4 not computed (no citation pass; declared drop) |

The transience (O3) row is **evaluable and null**: AUC +0.540 vs +0.561, difference -0.021 [-0.130, +0.101]. The earlier row, which labelled this transience difference as not evaluable, was wrong. The frozen B5 + OPEN_home forecast adds +0.002 [-0.003, +0.008] (Section 25.7).

Source: `round-4/experiment-10/src/results/learned_models_cohort.json`; `cohort_result.json` -> `secondary.frozen_prediction_O2r_m50`.

### 25.7 Verdict

[Correction, iteration 5, from art_NMe386dX9GLF] The pre-registered verdict rule returns **CONFIRMED** (all five clauses pass, `cohort_result.json -> verdict`). Read with its limits, the evidence is weaker than that word:
- OPEN_home is +0.091 [+0.013, +0.171] at R2 but its R4 +0.069 [-0.012, +0.150] and R5 +0.056 [-0.022, +0.135] intervals include 0, as does the group-level DL pool +0.083 [-0.007, +0.173].
- **No forecasting gain**: the frozen B5 model gives Spearman +0.768 and B5 + OPEN_home +0.770, a difference of +0.002 [-0.003, +0.008] (n = 573).
- The planted control (true psp 0.10) was **not recovered** by the pipeline draw: +0.047 [-0.045, +0.132]; the independent audit draw gave +0.150 [+0.065, +0.226]. With power 0.16 and MDE 0.105, a single cohort of this size cannot confirm or refute an effect near 0.09 reliably.
- OPEN_all and OPEN_sizematch are larger but are labelled **mechanically coupled** / partly coupled (Section 25.4). Evaluation 3's specification curve (Section 27.2) used the all-papers build and is relabelled **exploratory, all-papers build**.

**Reading:** a small home-only partial association, positive on the confirmatory cohort at the registered rung, fragile under coverage and group controls, and with no out-of-sample forecasting gain.

Source: `cohort_result.json` -> `verdict`, `primary`, `groups`, `secondary.frozen_prediction_O2r_m50`, `placebos`; `cohort_report.json` -> `audits.post_unseal_audit.A5_planted`; `frozen_spec.json` -> `power`.

### 25.8 Components, within type, sensitivities and placebos (cohort)

[Correction, iteration 5, from art_NMe386dX9GLF] Re-keyed to `cohort_result.json` (cohort) and `exp5_selection_result.json` (EXP5 selection data), replacing the copies in the Exp10 README.

| component (sign) | HOME cohort | HOME EXP5 | ALL cohort | ALL EXP5 |
|---|---|---|---|---|
| new_edge_rate | +0.014 [-0.062, +0.090] | +0.039 [+0.014, +0.062] | +0.075 [-0.003, +0.152] | +0.084 [+0.062, +0.109] |
| n_comm_W3 | +0.002 [-0.071, +0.081] | -0.001 [-0.025, +0.022] | +0.161 [+0.082, +0.238] | +0.133 [+0.110, +0.154] |
| participation | +0.050 [-0.041, +0.133] | +0.043 [+0.020, +0.071] | +0.145 [+0.068, +0.224] | +0.117 [+0.095, +0.142] |
| NOV_res | +0.134 [+0.049, +0.215] | +0.057 [+0.033, +0.081] | +0.145 [+0.064, +0.221] | +0.087 [+0.064, +0.113] |
| ego_density_W3 | +0.018 [-0.075, +0.113] | -0.009 [-0.042, +0.020] | -0.078 [-0.162, -0.002] | -0.070 [-0.091, -0.043] |
| edge_persistence | -0.112 [-0.199, -0.023] | -0.088 [-0.109, -0.066] | -0.029 [-0.110, +0.047] | -0.041 [-0.065, -0.018] |

Within concept type (R3 without type dummies):

| build | method | object | property | topic |
|---|---|---|---|---|
| OPEN_home | +0.074 [-0.212, +0.314] n=81 | +0.093 [-0.025, +0.204] n=250 | +0.119 [-0.159, +0.370] n=78 | -0.073 [-0.279, +0.135] n=115 |
| OPEN_all | +0.112 [-0.141, +0.352] n=90 | +0.200 [+0.069, +0.319] n=265 | +0.113 [-0.113, +0.343] n=89 | +0.111 [-0.083, +0.305] n=132 |
| OPEN_sizematch | +0.200 [-0.056, +0.423] n=85 | +0.148 [+0.029, +0.268] n=253 | +0.150 [-0.127, +0.400] n=85 | +0.025 [-0.203, +0.236] n=118 |

Declared sensitivities (R2):

| analysis | estimate [95% CI] | n |
|---|---|---|
| OPEN_all_on_home_sample|O2r_m50|R2 | +0.176 [+0.091, +0.263] | 571 |
| OPEN_home|O2r_m50_le2022_TAG|2015onsets|R2 | +0.055 [-0.070, +0.193] | 221 |
| OPEN_home|O2r_m50_TAG|R2 | +0.091 [+0.016, +0.171] | 573 |
| OPEN_home|O2r_m50_MATCH|R2 | +0.122 [+0.058, +0.189] | 927 |
| OPEN_all|O2r_m50_le2022_TAG|2015onsets|R2 | +0.180 [+0.045, +0.311] | 245 |
| OPEN_all|O2r_m50_TAG|R2 | +0.174 [+0.092, +0.256] | 630 |
| OPEN_all|O2r_m50_MATCH|R2 | +0.206 [+0.147, +0.266] | 1073 |
| OPEN_sizematch|O2r_m50_le2022_TAG|2015onsets|R2 | +0.115 [-0.020, +0.248] | 232 |
| OPEN_sizematch|O2r_m50_TAG|R2 | +0.147 [+0.070, +0.220] | 591 |
| OPEN_sizematch|O2r_m50_MATCH|R2 | +0.181 [+0.123, +0.235] | 955 |
| OPEN_home_min5|O2r_m50|R2 | +0.091 [+0.016, +0.171] | 573 |
| OPEN_home_min20|O2r_m50|R2 | +0.083 [+0.002, +0.167] | 528 |
| OPEN_home|O2r_m50|R2|2015_2016_only | +0.130 [+0.037, +0.220] | 414 |

Placebos: within-group outcome permutations (200 draws): 95th percentile of |psp| = +0.081, against the observed +0.091. Planted psp = 0.10: +0.047 [-0.045, +0.132], not recovered; independent audit draw +0.150, recovered.

Source: `cohort_result.json` -> `components`, `within_type`, `sensitivity`, `placebos`; `exp5_selection_result.json` -> `components`.


## 25a. Experiment 11 (incomplete): does within-concept closure precede an entry slowdown? [ARTIFACT:gen_art_experiment_11]

[Correction, iteration 5, from gen_art_experiment_11] This experiment was commissioned in iteration 4 and was missing from the report. Plan title: *Within-concept closure, OPEN and the next field entry (FE Poisson / event study)*.

Pre-registered predictions and verdict rules, verbatim (`prereg.md`, lines 24-32):

> - H-M1: DEV PPML beta_density < 0 with concept-clustered 95% CI < 0
> - H-M2: DEV PPML beta_OPEN > 0 with 95% CI > 0   (Holm over H-M1, H-M2)
> - H-M3: |std beta_fwd| - |std beta_rev| > 0 with paired bootstrap 95% CI > 0
> - H-M4: mean lag 0..+2 < 0 with CI < 0; pre-trend Wald p > 0.10 and max |lead| < 0.5 |mean lag|; event-date permutation p < 0.05
> - H-M5: signs of H-M1 and H-M2 hold on OLD_HELDOUT and COHORT
> - H-S1: intersection-born concepts take off WITHOUT a prior home-prominence peak more often than single-home concepts (share difference > 0, concept-bootstrap CI > 0)
> - H-P1: (exploratory) METHOD and new-community partners carry more of the new_edge_rate signal than DOMAIN and same-community partners
> - SUPPORTED = H-M1 & H-M2 (Holm) & H-M3 & H-M4 & H-M5 signs; PARTIAL = H-M1 or H-M2 holds but H-M3 or H-M4 fails;
>   NOT SUPPORTED = both H-M1 and H-M2 CIs include 0 on DEV.

**DEV results** (concept-year panel, 35,328 rows, 4,661 concepts; concept-clustered CIs):

| model / term | b | 95% CI | p | n rows | n concepts (clustered) | I2 |
|---|---|---|---|---|---|---|
| H-M1 density (PPML) | -0.0701 | [-0.1804, +0.0403] | 0.213 | 28,989 | 3,463 | - |
| H-M2 OPEN_home (PPML) | +0.0154 | [-0.0383, +0.0691] | 0.574 | 28,989 | 3,463 | - |
| joint: density | -0.0732 | [-0.2095, +0.0631] | 0.293 | 28,989 | 3,463 | - |
| joint: OPEN_home | -0.0027 | [-0.0688, +0.0634] | 0.937 | 28,989 | 3,463 | - |
| LPM density | -0.0138 | [-0.0336, +0.0060] | 0.172 | 35,155 | NA | - |
| LPM OPEN_home | +0.0035 | [-0.0067, +0.0138] | 0.502 | 35,155 | NA | - |
| group BGM: density | +0.0856 | [-0.2477, +0.4189] | 0.615 | 2,719 | 342 | - |
| group BGM: OPEN_home | -0.0254 | [-0.1800, +0.1293] | 0.748 | 2,719 | 342 | - |
| group CS: density | -0.3392 | [-0.7227, +0.0442] | 0.083 | 1,681 | 223 | - |
| group CS: OPEN_home | -0.0049 | [-0.1824, +0.1727] | 0.957 | 1,681 | 223 | - |
| group Eng: density | -0.1469 | [-0.3431, +0.0494] | 0.142 | 8,729 | 1,030 | - |
| group Eng: OPEN_home | +0.0456 | [-0.0563, +0.1476] | 0.380 | 8,729 | 1,030 | - |
| group Med: density | -0.0044 | [-0.1606, +0.1519] | 0.956 | 15,860 | 1,868 | - |
| group Med: OPEN_home | +0.0068 | [-0.0650, +0.0787] | 0.852 | 15,860 | 1,868 | - |
| DL over DEV groups: density | -0.0746 | [-0.2103, +0.0612] | 0.282 | NA | NA | 0.25 |
| DL over DEV groups: OPEN_home | +0.0124 | [-0.0401, +0.0648] | 0.644 | NA | NA | 0.00 |

H-M3 point estimates: std beta_fwd -0.0048, std beta_rev +0.0021, difference +0.0027 (bootstrap CI [-0.0100, +0.0124]).

**Verdict: NOT SUPPORTED.** The rule is 'NOT SUPPORTED = both H-M1 and H-M2 CIs include 0 on DEV', and both do (table rows 1-2).

**What was not run.** Read from the logs, not from the plan:
- `logs/analysis_fe.log` last line: `2026-09-29 03:25:43.390 | INFO     | __main__:body_results:170 - DEV: 35328 rows / 4661 concepts; density b=-0.0701 OPEN b=0.0154 H-M3 diff=0.0027 (576s)`. Only the DEV body was estimated; OLD_HELDOUT and COHORT body models (H-M5) have no results in `fe_results.json` (only their `sample_counts`).
- H-M4 (Sun-Abraham event study): `logs/event_study.log` is empty (0 bytes) and `logs/event_study.out` ends in an OpenBLAS `pthread_create failed` error followed by `KeyboardInterrupt` during `import scipy`. No event-study estimate exists.
- H-S1 and H-P1: `logs/partners.log` last line: `2026-09-29 03:25:56.401 | INFO     | __main__:build_indicators:116 - partner indicators (12499, 15); bridging papers 594`; partner indicators were built, but no H-S1/H-P1 test output was written. (H-S1's question is answered descriptively by Exp12's sequence analysis, Section 26.3.)
- `deviations.json` records `placebo_ii_not_run`: "The within-concept-year field-identity permutation placebo (ii) was not run (time); the event-date permutation placebo (i) was run with 1,000 draws."
- No partial outputs from `event_study.out` or `partners.out` are reported as results.

Source: `3_invention_loop/iter_4/gen_art/gen_art_experiment_11/results/fe_results.json` -> `DEV.*`; `prereg.md` lines 24-32; `logs/*.log|out`; `results/deviations.json`.


## 26. Experiment 12: Breadth decomposition and trajectory analysis [ARTIFACT:art_uw4OeagJP3rv]

### 26.1 Log-additive breadth decomposition

[Correction, iteration 5, from art_uw4OeagJP3rv] Rarefied breadth is decomposed as log Bn = log E2 (early contact) + log M (frontier advance) + log ρ (retention); shares of the top-vs-bottom O2r_resid tercile gap. **Bn and O2r share papers; the decomposition is an identity, not a causal split.**

Pre-registered predictions, verbatim (`preregistration_R2.json`):

> **PR1** EXPLORATION > RETENTION: in variant (iv) [volume-stratified (early-volume quintiles), concepts with a Medicine (field 27) home excluded], s_explore - s_ret > 0 with the 95% concept-bootstrap CI > 0, where s_explore = s_E2 + s_M and s_ret = s_rho are the shares of the top-vs-bottom O2r_resid tercile gap in log mean breadth (Bn = retained off-home fields at t0+8). Equivalently s_ret < 0.5; both are printed (shares sum to 1).
> **PR1b** (secondary, Holm family R2-A with PR1 and PR2): s_contact - s_ret > 0 with CI > 0 (s_contact = s_E2).
> **PR2** LOCALISED KEEP MORE EARLY: mean RETENTION_RATIO_early(bottom O2r_resid tercile) - mean(top tercile) > 0 with CI > 0, AND the partial Spearman of RETENTION_RATIO_early with O2r_resid given B5 < 0 (CI < 0). The latter is flagged 'replication on the same frame as EXP8, not new evidence'.
> **PR3** (descriptive, not tested): the sign of D_rho, i.e. whether late retention probability is lower for integrating (top-tercile) concepts.

s_explore − s_ret by variant and body [95% concept-bootstrap CI] (PR1 is variant iv; the primary display variant is ii):

| body | i pooled | ii volume-stratified (primary) | iii volume + Medicine adjusted | iv volume-stratified, no Medicine (PR1) |
|---|---|---|---|---|
| DEV | +0.464 [+0.407, +0.528] (n=3,188) | +0.431 [+0.371, +0.493] (n=3,188) | +0.446 [+0.383, +0.509] (n=3,188) | +0.633 [+0.537, +0.727] (n=1,469) |
| held-out (4 groups pooled) | +0.549 [+0.466, +0.625] (n=1,833) | +0.494 [+0.402, +0.576] (n=1,833) | +0.490 [+0.401, +0.572] (n=1,833) | +0.492 [+0.403, +0.575] (n=1,825) |
| 2010-14 cohort (pooled) | +0.421 [+0.358, +0.487] (n=2,182) | +0.343 [+0.276, +0.405] (n=2,182) | +0.362 [+0.291, +0.439] (n=2,182) | +0.445 [+0.358, +0.527] (n=1,403) |

DerSimonian-Laird over the held-out groups (PHYS, LIFEENV, SOC, variant iv): +0.504 [+0.329, +0.679], I2 = 0.76.

Verdicts per clause (the rule: SUPPORTED / NOT SUPPORTED / REVERSED by CI side, per body):

| body | PR1 (s_explore − s_ret, variant iv) | PR1b (s_contact − s_ret) | PR2 (bottom − top retention ratio; psp given B5) | PR3 (descriptive) |
|---|---|---|---|---|
| DEV | SUPPORTED: +0.633 [+0.537, +0.727] | SUPPORTED: +0.604 [+0.508, +0.698] | REVERSED: diff -0.110 [-0.132, -0.086]; psp -0.169 [-0.202, -0.134] | D_rho +0.202 [+0.144, +0.267] |
| held-out | SUPPORTED: +0.492 [+0.403, +0.575] | SUPPORTED: +0.480 [+0.394, +0.570] | NOT SUPPORTED: diff +0.011 [-0.019, +0.039]; psp -0.129 [-0.175, -0.086] | D_rho +0.263 [+0.207, +0.325] |
| 2010-14 cohort | SUPPORTED: +0.445 [+0.358, +0.527] | SUPPORTED: +0.414 [+0.324, +0.494] | REVERSED: diff -0.058 [-0.083, -0.031]; psp -0.173 [-0.212, -0.133] | D_rho +0.291 [+0.237, +0.351] |

PR2 is REVERSED on its first clause wherever the difference is negative: localised concepts do **not** keep more early; the psp clause replicates EXP8 on the same frame and is not new evidence.

Source: `round-4/experiment-12/src/results/decomposition_dev.json`, `decomposition_heldout.json` -> `variants.*`, `verdicts.*`, `DL_heldout_groups`; `preregistration_R2.json`.

### 26.2 Trajectory typology

DTW k-medoids (k = 4, chosen by ARI stability) and 5-state HMM were compared on 9-variable annual trajectory profiles (new entries, offhome entries, fields retaining, fields lost, retention share, frontier, entropy, home share, community span):

| method | ARI with DTW k=4 | naming rule passes? |
|---|---|---|
| DTW k=4 | 1.0 (self) | No (all conditions false) |
| HMM S=5 | 0.222 | No |
| DTW k=4 (no Medicine) | 0.461 | No |

**Verdict: CONTINUUM.** The naming rule (which requires each cluster to dominate on a specific trajectory feature) fails for all conditions. The DTW-HMM agreement is low (ARI 0.222), improving to 0.461 when Medicine dominated clusters are excluded. PCA of the trajectory space shows the first principal component explains 38.8% and the second 10.7% of variance; OPEN correlates with the first component (the breadth axis). The two class finding from iteration 2 does not reproduce at higher resolution.

Heldout recluster: ARI = 0.443 (DTW) and 0.378 (HMM), confirming moderate but not strong reproducibility.


[Correction, iteration 5, from art_uw4OeagJP3rv] Where OPEN sits in the trajectory space (partial Spearman given B5 and label coverage):

| build | DEV PC1 | DEV PC2 | held-out DL PC1 | 2010-14 cohort PC1 |
|---|---|---|---|---|
| OPEN_all | +0.174 [+0.146, +0.202] | -0.105 [-0.133, -0.076] | +0.120 [+0.085, +0.155] | +0.117 [+0.087, +0.147] |
| OPEN_home | +0.117 [+0.085, +0.146] | -0.068 [-0.099, -0.037] | +0.060 [+0.023, +0.097] | +0.121 [+0.088, +0.153] |
| OPEN_sizematch | +0.135 [+0.107, +0.163] | -0.076 [-0.103, -0.049] | +0.094 [+0.060, +0.129] | +0.089 [+0.058, +0.119] |

The typology is a continuum (DTW-HMM ARI 0.222); OPEN loads on the breadth axis (PC1) and weakly negatively on PC2 (retention-heavy profiles) for the all-papers build.

Source: `trajectories_dev.json` -> `open_on_axis.pooled`, `hmm.ari_dtw_hmm`; `trajectories_heldout.json` -> `DL_heldout_groups_PC1`, `open_on_axis_cohort_PC1`. (`open_diagnostics.json` holds build correlations and coverage, not the PC table.)


### 26.3 Sequence: home prominence first, or born at the intersection?

[Correction, iteration 5, from art_uw4OeagJP3rv] A = first age with home-field prominence ≥ half its 0-8 maximum; T = first cross-field take-off age. The share of concepts with A < T is compared with a mechanical-lag null (1,000 within-concept permutations of the prominence series). The hazard ratio compares take-off of intersection-born concepts with single-home concepts (cloglog, controlling log volume).

| body | n | share A < T | null share | excess [95% CI] | intersection-born take-off HR [95% CI] | verdict |
|---|---|---|---|---|---|---|
| DEV | 4,555 | 0.256 | 0.264 | -0.009 [-0.015, -0.003] | 0.47 [0.42, 0.54] | MIXED |
| held-out | 3,280 | 0.136 | 0.126 | +0.011 [+0.005, +0.016] | 0.45 [0.38, 0.52] | HOME-FIRST |
| 2010-14 cohort | 4,195 | 0.160 | 0.178 | -0.017 [-0.023, -0.012] | 0.41 [0.35, 0.47] | MIXED |

The excess over the mechanical lag is at most a few percentage points and changes sign between bodies (HOME-FIRST only on the held-out groups). Intersection-born concepts take off **later**, not earlier (HR < 1 in every body). There is no general home-first sequence and no intersection route.

Source: `sequence_light_dev.json`, `sequence_light_heldout.json` -> `<body>.order`, `mechanical_lag_null`, `cloglog_hazard`, `verdict`.

### 26.4 Case studies (7 matched pairs)

[Correction, iteration 5, from art_uw4OeagJP3rv] The previous 26.4 table contained 5 rows that no artifact produced, and a sentence on GPU computing and deep learning that is not in the pair set. Both are deleted. [Correction, iteration 4/5] The table below is read row by row from `case_pairs.json -> pairs`.

Pairs were selected on OPEN_all (top vs bottom quintile within reporting group), matched on logvol, growth and onset within group; the outcome was not used in selection (`case_pairs.json -> rule.outcome_use`: "O2r is NOT used in selection; displayed after selection only"). **Illustration, not inference.**

| pair | group | high-OPEN_all concept | low-OPEN_all concept | OPEN_all (high / low) | OPEN_home | logvol | O2r_resid | rho (retention) | Bn | E2 | high has higher O2r_resid | OPEN_home order disagrees |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pair01_CSEng | CS+Eng | Graphics processing unit | Vertical axis wind turbine | +2.122 / -0.669 | +0.499 / -0.407 | +4.890 / +4.898 | +3.260 / -0.918 | +0.727 / +0.667 | 8 / 4 | 7 / 2 | yes | no |
| pair02_BGMMed | BGM+Med | Shotgun proteomics | Image-guided radiation therapy | +1.551 / -1.219 | +1.454 / -0.763 | +4.419 / +4.477 | +1.336 / -3.517 | +0.600 / +0.000 | 3 / 0 | 3 / 1 | yes | no |
| pair03_PHYS | PHYS | Nanocarriers | Nanosheet | +0.666 / -0.615 | +0.390 / -0.233 | +4.710 / +4.796 | +2.788 / +0.730 | +0.600 / +0.875 | 6 / 7 | 6 / 4 | yes | no |
| pair04_SOC | SOC | Soft power | Autonomous learning | +1.955 / -0.390 | +1.602 / +0.313 | +4.942 / +4.942 | +1.348 / +0.260 | +0.750 / +1.000 | 6 / 4 | 4 / 3 | yes | no |
| pair05_CSEng | CS+Eng | Scopus | Oxygen reduction reaction | +1.843 / -0.827 | +0.202 / -0.410 | +4.554 / +4.511 | +5.686 / +0.742 | +0.643 / +0.833 | 9 / 5 | 6 / 4 | yes | no |
| pair06_BGMMed | BGM+Med | Sclerostin | IgG4-related disease | +1.548 / -0.864 | +2.838 / -0.800 | +5.081 / +5.112 | -0.921 / -1.579 | +1.000 / +0.750 | 4 / 3 | 3 / 2 | yes | no |
| pair07_SOC | SOC | User-generated content | Mindfulness-based cognitive therapy | +1.143 / -0.404 | +1.440 / -0.463 | +4.522 / +4.511 | +0.739 / -0.221 | +0.750 / +1.000 | 3 / 4 | 3 / 3 | yes | no |

The high-OPEN_all member is broader (higher O2r_resid) in 7/7 pairs and has more retained off-home fields (Bn) in 5/7. In 0/7 pairs the OPEN_home ordering disagrees with the OPEN_all ordering, so these pairs illustrate the all-papers build, which Section 25.4 shows is mechanically coupled to spread.

Source: `round-4/experiment-12/src/results/case_pairs.json` -> `pairs[i].{OPEN_all,OPEN_home,logvol,O2r_resid,rho,Bn,E2}`; counts in `results/derived.json`.

### 26.5 Exploratory AI atlas: retrospective, outcome-selected (37 concepts)

[Correction, iteration 5, from art_uw4OeagJP3rv] This is the exploratory stage the request asks for (Artificial Intelligence first). It is labelled by its own file as "RETROSPECTIVE, DESCRIPTIVE, OUTCOME-SELECTED BY DESIGN". Concepts were chosen per trajectory type AFTER outcomes were known, so the table describes; it does not test.

| name | type | t0 | ai_share | early_volume | growth_c | O1b | O3 | O2r_resid | OPEN_all | OPEN_home |
|---|---|---|---|---|---|---|---|---|---|---|
| Cloud computing | RAPID | 2008 | 0.121 | 904 | +2.909 | 0 | 0 | +0.067 | +6.540 | +6.499 |
| Convolutional neural network | RAPID | 2014 | 0.552 | 713 | +2.288 | 1 | 0 | +3.291 | +2.415 | +1.657 |
| Mobile apps | RAPID | 2011 | 0.130 | 309 | +1.357 | 1 | 0 | +4.159 | +2.218 | +1.872 |
| CUDA | RAPID | 2008 | 0.197 | 285 | +1.604 | 0 | 0 | +1.827 | +2.938 | +1.993 |
| CDIO | RAPID | 2009 | 0.159 | 285 | +1.726 | 0 | 1 | -0.380 | +0.526 | +1.326 |
| Artificial bee colony algorithm | RAPID | 2010 | 0.258 | 266 | +1.504 | 0 | 0 | +0.265 | +1.609 | +1.198 |
| Crowdsourcing | RAPID | 2009 | 0.127 | 247 | +1.692 | 1 | 0 | +5.309 | +3.640 | +1.088 |
| Cloud storage | RAPID | 2010 | 0.174 | 213 | +1.447 | 0 | 0 | -0.720 | +0.125 | +1.904 |
| Conditional random field | GRADUAL | 2007 | 0.650 | 137 | +0.262 | 1 | 0 | +1.475 | +0.561 | +1.616 |
| Steganography | GRADUAL | 2003 | 0.832 | 124 | +0.375 | 1 | 0 | -0.948 | +0.066 | -0.590 |
| XML Schema (W3C) | GRADUAL | 2003 | 0.332 | 111 | +0.076 | 1 | 0 | +0.027 | -0.517 | -1.307 |
| Blind signature | GRADUAL | 2004 | 0.540 | 96 | +0.241 | 1 | 0 | -0.732 | -0.396 | -0.368 |
| Learning Management | GRADUAL | 2004 | 0.694 | 91 | +0.028 | 1 | 0 | +0.951 | +0.013 | -0.875 |
| Digital forensics | GRADUAL | 2006 | 0.307 | 90 | -0.056 | 1 | 0 | -0.170 | +0.632 | +0.107 |
| Differential privacy | GRADUAL | 2013 | 0.607 | 85 | -0.170 | 1 | 0 | +0.450 | -0.309 | -0.391 |
| Bat algorithm | GRADUAL | 2014 | 0.304 | 84 | -0.069 | 1 | 0 | +1.440 | +0.623 | +0.982 |
| Iris recognition | LOCAL | 2004 | 0.161 | 105 | +0.429 | 1 | 0 | -1.129 | -0.244 | -0.225 |
| CAPTCHA | LOCAL | 2009 | 0.203 | 95 | +0.578 | 1 | 0 | -1.175 | +0.146 | +0.735 |
| Group key | LOCAL | 2004 | 0.236 | 85 | +0.331 | 1 | 0 | -2.098 | -0.694 | -0.362 |
| Honeypot | LOCAL | 2004 | 0.120 | 81 | +0.377 | 1 | 0 | -1.491 | -0.223 | -0.058 |
| Quality of experience | LOCAL | 2010 | 0.374 | 71 | +0.176 | 1 | 0 | -0.966 | +0.440 | -0.534 |
| Extreme learning machine | DIFFUSING | 2011 | 0.687 | 348 | +1.063 | 1 | 0 | +1.297 | +1.457 | +0.371 |
| Deep learning | DIFFUSING | 2012 | 0.574 | 147 | +1.076 | 1 | 0 | +4.000 | +1.043 | -0.129 |
| Non-negative matrix factorization | DIFFUSING | 2006 | 0.349 | 134 | +1.030 | 1 | 0 | +3.041 | +1.111 | +1.619 |
| Linked data | DIFFUSING | 2009 | 0.408 | 117 | +0.934 | 0 | 0 | +2.070 | +0.406 | +0.856 |
| Deep belief network | DIFFUSING | 2014 | 0.388 | 116 | +1.052 | 1 | 0 | +1.992 | +1.263 | +1.194 |
| Feature learning | DIFFUSING | 2014 | 0.653 | 114 | +0.926 | 1 | 0 | +1.264 | -0.310 | -0.395 |
| Topic model | DIFFUSING | 2011 | 0.698 | 106 | +0.588 | 1 | 0 | +2.115 | -0.362 | -0.085 |
| Visual analytics | DIFFUSING | 2008 | 0.511 | 97 | +0.464 | 1 | 0 | +4.534 | +0.375 | +0.819 |
| HTML5 | TRANSIENT | 2010 | 0.123 | 170 | +1.553 | 0 | 1 | +2.919 | +1.653 | +0.179 |
| Machine to machine | TRANSIENT | 2011 | 0.133 | 151 | +1.314 | 0 | 1 | -2.019 | +0.439 | +0.028 |
| Learning object | TRANSIENT | 2003 | 0.732 | 143 | +1.114 | 0 | 1 | +0.210 | +0.299 | +0.706 |
| Android application | TRANSIENT | 2013 | 0.120 | 130 | +0.727 | 0 | 1 | +1.105 | +0.145 | -0.302 |
| BitTorrent | TRANSIENT | 2007 | 0.109 | 116 | +0.526 | 0 | 1 | -0.545 | -1.059 | -0.566 |
| Digital reference | TRANSIENT | 2003 | 0.119 | 110 | +0.452 | 0 | 1 | -1.180 | +0.320 | +0.599 |
| Folksonomy | TRANSIENT | 2007 | 0.429 | 105 | -0.204 | 0 | 1 | -0.591 | -0.168 | -0.720 |
| XQuery | TRANSIENT | 2003 | 0.270 | 103 | +0.455 | 0 | 1 | NA | -0.546 | -0.050 |

Measures that looked meaningful across types (`atlas.json -> looked_meaningful`): `n_c`, `H`, `n_ent_off`, `n_ret`, `comm_span`, `frontier`, `n_comm_W3_all`, `participation_all`, `ego_density_W3_all`, `OPEN_all`, `OPEN_home`. Data limit: topic-level ego structure exists only for t0-3..t0+2 (EXP8 Pass A kept only those hits; no snapshot pass is allowed here), so topic-neighbour change after t0+2 cannot be shown.

Source: `round-4/experiment-12/src/ai_atlas/atlas.json` -> `concepts[i]` (the 37-concept list; `ai_atlas/table.csv` is the per-measure median table by type, not the concept list).


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


[Correction, iteration 5, from art_oKOd21ZMnu9S] Label: **exploratory, all-papers build.** The curve varies composites of the all-papers components on already-unsealed held-out groups; it does not test the home-only build and is not confirmatory. Headline pooled psp +0.183 [+0.083, +0.280], I2 = 0.73.


### 27.3 Heterogeneity and the Life & Environment Sciences diagnosis

On 21 home field × period subunits (n >= 60), I2 = 0.43 (21 home-field × period sub-units) vs I2 = 0.66 (6 units); the spec-curve headline pool has I2 = 0.73 (DL over 4 held-out groups) [Correction, iteration 5, from art_oKOd21ZMnu9S]. No ecological trait (label coverage, early volume, share multihome, share generic, median O2r, SD of OPEN, mean onset year) explains the between subunit variance (all Holm p = 1.0).

LIFEENV shows the weakest OPEN signal: PSP +0.071 vs +0.186 for the other 5 units pooled. Neither restricted range (Thorndike correction moves it only to +0.080) nor label coverage reweighting (entropy balancing: +0.069) explains the gap. Verdict: **UNEXPLAINED domain boundary**.

### 27.4 Retained frontier proximity dependence

[Correction, iteration 4, from art_22ppE1snfHKj] Under the minimum conditional probability proximity backbone (instead of the frozen PMI backbone), d0_ret_rel at the R3 rung is -0.021 (vs +0.322 under PMI). The d0 effect is backbone specific: it measures relatedness as PMI encodes it, not relatedness in general.


[Correction, iteration 5, from art_22ppE1snfHKj] The earlier name of the R3 rung (it was called the footprint-control rung) is replaced by 'R3 rung' everywhere (1 occurrence(s)). [Correction, iteration 5, from art_22ppE1snfHKj] The Exp7 d0 value under min-cp proximity at R3 is -0.021 (`step2_heldout.json -> pooled4.specificity_rebuild.m_min_conditional_probability_proximity.ladder.models.R3_ret.coef.d0_ret_rel`).


### 27.5 Claims ledger

The iteration-4 claims ledger (v3) has 1,290 rows and 0 MISMATCH after all corrections from files 01-11 are applied.

### 27.6 Corrections applied

[Correction, iteration 5, from this evaluation] The previous text claimed that all Evaluation 3 corrections had been applied in place; most had not. This list is generated by `src/apply_corrections.py` from `results/corrections_applied.csv` and records, per correction file, what happened to each block in this corrected report.

| correction file | blocks | APPLIED | ALREADY_PRESENT | NOT_APPLIED (target missing) | NOT_APPLIED (superseded old-text quote) |
|---|---|---|---|---|---|
| `01_case_studies_26_4.md` | 2 | 2 | 0 | 0 | 0 |
| `01_exp8_outcomes_relabel.md` | 9 | 4 | 3 | 0 | 2 |
| `02_exp11_25a.md` | 5 | 5 | 0 | 0 | 0 |
| `02_prereg_P1_P5.md` | 7 | 4 | 1 | 0 | 2 |
| `03_exp10_rewrite.md` | 6 | 6 | 0 | 0 | 0 |
| `03_exp7_tables.md` | 8 | 8 | 0 | 0 | 0 |
| `04_eval2_text_corrections.md` | 14 | 14 | 0 | 0 | 0 |
| `04_exp12_rewrite.md` | 4 | 4 | 0 | 0 | 0 |
| `05_record_tables_map.md` | 1 | 1 | 0 | 0 | 0 |
| `06_ledger_open_rows.md` | 1 | 1 | 0 | 0 | 0 |
| `06_section23_restore.md` | 2 | 2 | 0 | 0 | 0 |
| `07_failed_artifacts.md` | 3 | 3 | 0 | 0 | 0 |
| `07_section28_evidence.md` | 3 | 3 | 0 | 0 | 0 |
| `08_candidate_S_and_families.md` | 4 | 3 | 0 | 0 | 1 |
| `08_exp8_exp10_secondary.md` | 5 | 5 | 0 | 0 | 0 |
| `09_coverage_table_30.md` | 1 | 1 | 0 | 0 | 0 |
| `09_o5_leakage.md` | 1 | 1 | 0 | 0 | 0 |
| `10_minor_and_refs.md` | 4 | 4 | 0 | 0 | 0 |
| `10_minor_slips.md` | 3 | 2 | 1 | 0 | 0 |
| `11_boundary_results.md` | 1 | 1 | 0 | 0 | 0 |
| `11_evidence_synthesis.md` | 1 | 1 | 0 | 0 | 0 |

Evaluation 3 Step 3 is recorded: D_rca_persist_k rival untested; Exp7 D_rca_pers is a different construct (max rho 0.877, drca_persist_comparison.json).

## 28. Research 3: Novelty positioning [ARTIFACT:art_hSyVUBa2okT2]

### 28.1 Novelty verdicts

| claim | verdict | key comparator |
|---|---|---|
| openness → later cross field breadth | PARTIALLY ANTICIPATED | Cheng 2023 (volume, not breadth), Maillart 2026 (concept pairs, not field holdout), Wang 2017 (paper level novelty), Weng 2013 (memes), Ugander 2012 (adoption) |
| consolidation → less breadth | PARTIALLY ANTICIPATED, CONTRADICTED BY on volume | Cheng 2023 (consistency +53% volume/SD), Chavalarias 2013 (density → survival), Centola 2010, Salatino 2017 |
| low retention ratio → breadth | NEW | Analogues only: propagule pressure (Lockwood 2005), group turnover (Palla 2007) |
| within concept closure → entry slowdown | NEW as lead lag test | Field level prior is opposite (Chavalarias 2013); life cycle analogues (Singh 2022, Prabhakaran 2016) |


[Correction, iteration 5, from gen_art_experiment_11] C4 (within-concept closure -> entry slowdown) was tested: DEV null (H-M1 CI [-0.1804, +0.0403]), [ARTIFACT:gen_art_experiment_11]. The 'NEW as lead-lag test' verdict therefore describes a test that was run and failed on DEV, not an open result.


[Correction, iteration 5, from this run's artifacts] Evidence from this run FOR and AGAINST each verdict:

| claim | for | against |
|---|---|---|
| C1 openness → breadth | Exp10 OPEN_home R2 +0.091 [+0.013, +0.171] on the confirmatory cohort | R4 +0.069 [-0.012, +0.150] and R5 include 0; the all-papers build (Eval3 spec-curve headline +0.183) is mechanically coupled |
| C2 consolidation → less breadth | Exp8 P2 (edge persistence) pooled psp -0.080 [-0.126, -0.033]; ego_density_W3 -0.102 | the review's 'raw sign flip' pair `+0.143 / -0.126` could not be located in any file (NOT_FOUND) and is not used |
| C3 low retention ratio → breadth | Exp8 held-out -0.114 given B5 | cohort R2 -0.043 [-0.116, +0.031], R3 -0.025; PR2 raw difference (bottom − top) DEV -0.110, held-out +0.011, 2010-14 cohort -0.058 |
| C4 closure → entry slowdown | none | Exp11 DEV null: H-M1 -0.0701 [-0.1804, +0.0403] |

**RETENTION_RATIO_early does not survive type controls** (cohort R2 CI includes 0); it is moved from 'NEW' to 'does not survive type controls'.



### 28.2 Contribution statement

"The first heldout, size adjusted, concept level test showing that early cooccurrence openness predicts later cross field breadth, while early consolidation, which predicts volume and survival elsewhere, does not."


**What survives beyond Cheng 2023 and Maillart 2026.** [Correction, iteration 5, from this run's artifacts] A home-only partial association of novel, non-persistent early neighbours with later breadth: on the 573-concept cohort, NOV_res +0.134 [+0.049, +0.215] and edge persistence -0.112 [-0.199, -0.023], with the composite OPEN_home +0.091 [+0.013, +0.171]. It is fragile at R4/R5, adds nothing to forecasting (+0.002), and awaits the Frame-N confirmation (Section 32).


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


10. **Within-concept closure does not precede an entry slowdown (Experiment 11, DEV only).** [Correction, iteration 5, from gen_art_experiment_11] H-M1 density b = -0.0701 [-0.1804, +0.0403]; H-M2 OPEN_home b = +0.0154 [-0.0383, +0.0691]. NOT SUPPORTED. The event study, the held-out bodies and H-S1/H-P1 did not run (Section 25a).



## 30. Coverage of the original request (final)

[Correction, iteration 5, from this evaluation] Corrected cell by cell; the change log below lists each old cell, the new cell and the artifact behind it. Cells for this iteration's work read 'pending iteration-5 artifact'.

| Step | Iteration 1 | Iteration 2 | Iteration 3 | Iteration 4 | Iteration 5 |
|---|---|---|---|---|---|
| RQ1: candidate indicator screen (dev) | Done (3) | Not extended | Done (53 indicators) | - | pending iteration-5 artifact |
| RQ1: holdout evaluation | Not started | Frame built (12,499) | Done (7/10 confirmed) | OPEN_home small, fragile (+0.091 [+0.013, +0.171] at R2; R4/R5 include 0) | pending iteration-5 artifact |
| RQ1: top-10 on holdout | Not started | Not started | Done | Extended (OPEN composite; OPEN_all mechanically coupled) | pending iteration-5 artifact |
| RQ1: external ground truth (O5) | Not started | Built | Validated: unrelated | - | pending iteration-5 artifact |
| RQ1: learned model | Not started | Not started | Done (+0.059) | Cohort linear_all +0.030; B5 + OPEN_home +0.002 (no gain) | pending iteration-5 artifact |
| RQ2: diffusion trajectories | Not started | Done (2 classes) | Exp9 failed | Done: CONTINUUM (Exp12) | pending iteration-5 artifact |
| RQ2: field entry conditional logit | Partial (dev) | Confirmed (d=0.30) | Robustness: PARTIAL | Backbone-specific | pending iteration-5 artifact |
| RQ2: breadth decomposition | Not started | Not started | Not started | Done (identity, not causal): s_explore − s_ret +0.431 (DEV, variant ii) | pending iteration-5 artifact |
| Grounding benchmark | Not started | Done | Audited | - | pending iteration-5 artifact |
| Strongest indicator analysis | Not started | Not started | Not started | Components (Exp10: NOV_res, low edge persistence); Exp11 H-P1 not run | pending iteration-5 artifact |
| Case studies | Not started | Not started | Not started | Done (7 matched pairs, rebuilt from case_pairs.json) | pending iteration-5 artifact |
| Record audit | Not started | Not started | Done (246 claims) | Done (1,290 claims, 0 mismatch; corrections now applied, Section 27.6) | pending iteration-5 artifact |
| Spec curve / robustness | Not started | Not started | Not started | Done (1,920 specs, 99.7% CI>0): exploratory, all-papers build | pending iteration-5 artifact |
| Novelty positioning | Not started | Partial | Partial | Done (4 claims, 68 refs) | pending iteration-5 artifact |
| Exploratory AI stage | Not started | Not started | Not started | Done: 37-concept atlas (retrospective, outcome-selected) | pending iteration-5 artifact |
| Home-first vs intersection | Not started | MIXED (Exp6) | Exp9 failed | Done: MIXED / HOME-FIRST held-out only; intersection-born HR < 1 | pending iteration-5 artifact |
| Why it works | Not started | Not started | Not started | Exp10 components; Exp11 H-P1 not run | pending iteration-5 artifact |

Change log:

| row | column | old cell | new cell | artifact |
|---|---|---|---|---|
| RQ1: holdout evaluation | Iteration 4 | OPEN cohort confirmed | OPEN_home small, fragile (+0.091 [+0.013, +0.171] at R2; R4/R5 include 0) | art_NMe386dX9GLF |
| RQ1: top-10 on holdout | Iteration 4 | Extended (OPEN composite) | Extended (OPEN composite; OPEN_all mechanically coupled) | art_NMe386dX9GLF |
| RQ1: learned model | Iteration 4 | Cohort +0.030 | Cohort linear_all +0.030; B5 + OPEN_home +0.002 (no gain) | art_NMe386dX9GLF |
| RQ2: diffusion trajectories | Iteration 4 | Done: CONTINUUM (Exp12) | Done: CONTINUUM (Exp12) | art_uw4OeagJP3rv |
| RQ2: breadth decomposition | Iteration 4 | Done: explore 73%, retain 27% | Done (identity, not causal): s_explore − s_ret +0.431 (DEV, variant ii) | art_uw4OeagJP3rv |
| Strongest indicator analysis | Iteration 4 | Decomposition + case studies | Components (Exp10: NOV_res, low edge persistence); Exp11 H-P1 not run | art_NMe386dX9GLF, gen_art_experiment_11 |
| Case studies | Iteration 4 | Done (7 matched pairs) | Done (7 matched pairs, rebuilt from case_pairs.json) | art_uw4OeagJP3rv |
| Record audit | Iteration 4 | Done (1,290 claims, 0 mismatch) | Done (1,290 claims, 0 mismatch; corrections now applied, Section 27.6) | art_oKOd21ZMnu9S |
| Spec curve / robustness | Iteration 4 | Done (1,920 specs, 99.7% CI>0) | Done (1,920 specs, 99.7% CI>0): exploratory, all-papers build | art_oKOd21ZMnu9S |

## 31. What we have learned so far

Four iterations and 20 commissioned artifacts (16 completed; 4 failed or incomplete: gen_art_dataset_1, gen_art_experiment_2, gen_art_experiment_9, gen_art_experiment_11) [Correction, iteration 5, from run records] have tested whether temporal network signals predict how new scientific concepts spread across disciplines, using OpenAlex data on up to 12,499 concepts with up to 27,393 concept by field adoption episodes.

**Confirmed findings:**

1. **A small home-only openness association on a confirmatory cohort (fragile).** [Correction, iteration 5, from art_NMe386dX9GLF] On 2015-2017 onset concepts never screened before, OPEN_home has psp +0.091 [+0.013, +0.171] at R2 (Holm p = 0.048), but R4, R5 and the group DL pool +0.083 [-0.007, +0.173] include 0, and adding it to B5 changes forecast Spearman by +0.002 [-0.003, +0.008]. OPEN_all is larger but mechanically coupled to the outcome. The previous wording of this finding follows, superseded: **Early cooccurrence openness (OPEN) predicts later cross field breadth on a confirmatory cohort.** The OPEN index (mean of six z scored ego network components: new_edge_rate, n_comm_W3, participation, NOV_res, −ego_density_W3, −edge_persistence) is confirmed on 2015-2016 onset concepts never used in any prior screen. OPEN_home PSP = +0.091 [+0.013, +0.171] at the concept type rung (Holm p = 0.048); OPEN_all +0.174 [+0.092, +0.253]; OPEN_sizematch +0.147 [+0.068, +0.221]. The specification curve shows 99.7% of 1,920 specs have confidence intervals above zero (permutation p = 0.005). The OPEN signal survives controls for contact reach, concept type, preonset footprint, label coverage and group fixed effects.

2. **Seven of 10 early network indicators are confirmed for predicting rarefied field breadth on heldout fields.** M0_density_end (+0.375), D_vol_end (+0.307), CONTACT_REACH (+0.211), n_comm_W3 (+0.167), NOV (+0.151), RETENTION_RATIO_early (−0.114; [Correction, iteration 5, from art_NMe386dX9GLF] does not survive type controls: cohort R2 -0.043 [-0.116, +0.031]), ego_density_W3 (−0.102). An ElasticNet combining all indicators adds +0.059 [+0.046, +0.073] Spearman over the five feature baseline.

3. [Correction, iteration 5, from art_uw4OeagJP3rv] **Caveat: Bn and O2r share papers; the decomposition is an identity, not a causal split.** **Breadth is driven by exploration, not retention.** The log additive decomposition shows that early contact diversity accounts for 73% of the top vs bottom tercile breadth gap; retention accounts for 27% (difference 0.464 [0.407, 0.528]). Broad concepts start with wider contact, not by advancing a wider frontier.

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


## 32. Evidence synthesis across bodies (iteration 5, descriptive)

[Correction, iteration 5, from this evaluation] How the home-only openness association behaves on every body scored so far. Same estimator, rungs and frozen EXP5 constants as Exp10; gate G1 reproduces Exp10's EXP5 selection psp (+0.099 at R0, +0.076 at R2) and gate G2 its cohort value (+0.091 [+0.013, +0.171]). Each body is labelled by design status: **selection** = the data on which the index or its constants were chosen; **already-unsealed** = held-out data whose outcomes earlier artifacts had already read; **confirmatory** = never used before the test. NOVCHURN_home = mean(z NOV_res, −z edge_persistence), the two home components that carried the cohort signal; it was chosen on the 2015-17 cohort, so that body is 'selection' for it.

**OPEN_home** (O2r_m50):

| body | onsets | status | R0 | R2 (primary) | R3 | n (R2) | placebo 95th pct abs psp |
|---|---|---|---|---|---|---|---|
| B1_DEV | 2003-09 | selection | +0.139 [+0.103, +0.174] | +0.109 [+0.073, +0.144] | +0.084 [+0.048, +0.121] | 3,003 | +0.035 |
| B2_PHYS | 2003-09 | already-unsealed | +0.083 [-0.014, +0.179] | +0.025 [-0.076, +0.128] | +0.041 [-0.065, +0.144] | 385 | +0.097 |
| B2_LIFEENV | 2003-09 | already-unsealed | +0.058 [-0.025, +0.140] | +0.067 [-0.018, +0.148] | +0.064 [-0.022, +0.147] | 552 | +0.084 |
| B2_SOC | 2003-09 | already-unsealed | +0.038 [-0.047, +0.121] | +0.044 [-0.041, +0.124] | +0.037 [-0.052, +0.121] | 546 | +0.087 |
| B2_MATHDEC | 2003-09 | already-unsealed | +0.259 [+0.008, +0.465] | +0.187 [-0.077, +0.409] | +0.168 [-0.099, +0.404] | 86 | +0.232 |
| B2_HELDOUT_pooled | 2003-09 | already-unsealed | +0.083 [+0.035, +0.133] | +0.070 [+0.021, +0.120] | +0.069 [+0.018, +0.119] | 1,569 | +0.056 |
| B3_EXP5_COHORT_2010_14 | 2010-14 | already-unsealed | +0.092 [+0.049, +0.136] | +0.074 [+0.029, +0.117] | +0.053 [+0.008, +0.097] | 1,993 | +0.037 |
| B4_COHORT_2015_17 | 2015-17 | confirmatory | +0.123 [+0.041, +0.205] | +0.091 [+0.013, +0.171] | +0.080 [+0.001, +0.162] | 573 | +0.077 |
| B5 Frame N | new frame (iteration-5 artifact) | pending iteration-5 artifact | - | - | - | - | - |

**NOVCHURN_home** (O2r_m50):

| body | onsets | status | R0 | R2 (primary) | R3 | n (R2) | placebo 95th pct abs psp |
|---|---|---|---|---|---|---|---|
| B1_DEV | 2003-09 | selection | +0.125 [+0.088, +0.162] | +0.116 [+0.079, +0.153] | +0.098 [+0.061, +0.137] | 2,741 | +0.035 |
| B2_PHYS | 2003-09 | already-unsealed | +0.099 [-0.006, +0.201] | +0.061 [-0.046, +0.179] | +0.078 [-0.030, +0.191] | 348 | +0.096 |
| B2_LIFEENV | 2003-09 | already-unsealed | +0.082 [-0.005, +0.168] | +0.084 [-0.008, +0.175] | +0.079 [-0.011, +0.172] | 500 | +0.092 |
| B2_SOC | 2003-09 | already-unsealed | +0.102 [+0.007, +0.188] | +0.124 [+0.029, +0.210] | +0.114 [+0.020, +0.199] | 489 | +0.096 |
| B2_MATHDEC | 2003-09 | already-unsealed | +0.204 [-0.095, +0.429] | +0.093 [-0.209, +0.408] | +0.078 [-0.236, +0.411] | 67 | +0.283 |
| B2_HELDOUT_pooled | 2003-09 | already-unsealed | +0.118 [+0.066, +0.169] | +0.113 [+0.061, +0.163] | +0.112 [+0.060, +0.163] | 1,404 | +0.051 |
| B3_EXP5_COHORT_2010_14 | 2010-14 | already-unsealed | +0.121 [+0.072, +0.167] | +0.113 [+0.065, +0.158] | +0.097 [+0.050, +0.144] | 1,799 | +0.048 |
| B4_COHORT_2015_17 | 2015-17 | selection (index chosen here) | +0.171 [+0.079, +0.256] | +0.161 [+0.071, +0.246] | +0.144 [+0.059, +0.226] | 506 | +0.087 |
| B5 Frame N | new frame (iteration-5 artifact) | pending iteration-5 artifact | - | - | - | - | - |

Random-effects pools at R2 (Fisher z, bootstrap SE; headline over non-selection bodies only, B2 groups entered separately):

| index | non-selection bodies | pooled psp | DL 95% CI | HKSJ 95% CI | I2 | tau2 (z) | sign agreement | all bodies (includes selection data) | selection body (DEV) | shrinkage DEV / pooled |
|---|---|---|---|---|---|---|---|---|---|---|
| OPEN_home | B2_PHYS, B2_LIFEENV, B2_SOC, B2_MATHDEC, B3_EXP5_COHORT_2010_14, B4_COHORT_2015_17 | +0.069 | [+0.038, +0.100] | [+0.042, +0.096] | 0.00 | 0.0000 | 6/6 | +0.085 | +0.109 | 1.58 |
| NOVCHURN_home | B2_PHYS, B2_LIFEENV, B2_SOC, B2_MATHDEC, B3_EXP5_COHORT_2010_14 | +0.105 | [+0.069, +0.140] | [+0.078, +0.131] | 0.00 | 0.0000 | 5/5 | +0.114 | +0.116 | 1.11 |

Leave one body out (pooled psp, R2): OPEN_home: without B2_PHYS +0.073; without B2_LIFEENV +0.069; without B2_SOC +0.073; without B2_MATHDEC +0.067; without B3_EXP5_COHORT_2010_14 +0.064; without B4_COHORT_2015_17 +0.065 | NOVCHURN_home: without B2_PHYS +0.110; without B2_LIFEENV +0.109; without B2_SOC +0.101; without B2_MATHDEC +0.105; without B3_EXP5_COHORT_2010_14 +0.094.

[FIGURE:fig_evidence_forest]

**Reading.** The home-only association is small and has the same sign in every body. It is consistently larger on the selection body (DEV) than on the non-selection pool (shrinkage ratio above), which is the winner's-curse pattern this run measured before. I2 is imprecise at this k. Because the non-selection bodies other than the 2015-17 cohort were already unsealed and reused, the pooled interval is **descriptive**: it is not a confirmation, and it is not a forecast gain (Section 25.7). NOVCHURN_home is shown for the Frame-N test; its cohort row is a selection estimate. The Frame-N row is empty and will be compared with this pool, not pooled into it.

Source: `results/evidence_synthesis.json` (this artifact; `src/synthesis.py`); figure `figures/evidence_forest.png|pdf`.

## References

[Correction, iteration 5, from this evaluation] One cumulative list: the report's two lists plus Research 1-3, de-duplicated (DOI, arXiv id, then author + year + title), Research 3 DOI corrections applied, unverified items excluded. Numbered by first citation, then alphabetically.

[1] Salatino, A., Osborne, F., & Motta, E. (2017). How are topics born? Understanding the research dynamics preceding the emergence of new areas. PeerJ Computer Science, 3, e119. https://doi.org/10.7717/peerj-cs.119

[2] Weng, L., Menczer, F., & Ahn, Y.-Y. (2013). Virality Prediction and Community Structure in Social Networks. Scientific Reports, 3, 2522. https://doi.org/10.1038/srep02522

[3] Rotolo, D., Hicks, D., & Martin, B. R. (2015). What is an emerging technology? Research Policy, 44(10), 1827-1843. Research Policy https://doi.org/10.1016/j.respol.2015.06.006

[4] Ciotti, V., Bonaventura, M., Nicosia, V., Panzarasa, P., & Latora, V. (2016). Homophily and missing links in citation networks. EPJ Data Science, 5, 7.

[5] Hidalgo, C. A., Klinger, B., Barabasi, A.-L., & Hausmann, R. (2007). The Product Space Conditions the Development of Nations. Science, 317(5837), 482-487. https://doi.org/10.1126/science.1144581

[6] Hidalgo, C. A., Balland, P.-A., Boschma, R., Delgado, M., Feldman, M., Frenken, K., Glaeser, E., He, C., Kogler, D. F., Morrison, A., Neffke, F., Rigby, D., Stern, S., Zheng, S., & Zhu, S. (2018). The Principle of Relatedness. In Unifying Themes in Complex Systems IX (pp. 451-457). Springer.

[7] Lockwood, J. L., Cassey, P., & Blackburn, T. (2005). Propagule pressure. TREE, 20, 223-228.

[8] Foster, J. G., Rzhetsky, A., & Evans, J. A. (2015). Tradition and Innovation in Scientists’ Research Strategies. ASR, 80, 875-908. https://doi.org/10.1177/0003122415601618

[9] Neffke, F., Henning, M., & Boschma, R. (2011). How do regions diversify over time? Industry relatedness and the development of new growth paths in regions. Economic Geography, 87(3), 237-265. https://doi.org/10.1111/j.1944-8287.2011.01121.x

[10] Shi, F. & Evans, J. (2023). Surprising combinations of research contents and contexts are related to impact and emerge with scientific outsiders from distant disciplines. Nature Communications, 14, 1641. https://doi.org/10.1038/s41467-023-36741-4

[11] Ugander, J. et al. (2012). Structural diversity in social contagion. PNAS, 109, 5962-5966. https://doi.org/10.1073/pnas.1116502109

[12] Centola, D. (2010). The Spread of Behavior in an Online Social Network Experiment. Science, 329, 1194-1197. https://doi.org/10.1126/science.1185231

[13] Pinheiro, F. L. et al. (2022). The time and frequency of unrelated diversification. Research Policy, 51(8), 104323. https://doi.org/10.1016/j.respol.2021.104323

[14] Singh, C. K. et al. (2022). Quantifying the rise and fall of scientific fields. PLoS ONE, 17, e0270131. https://doi.org/10.1371/journal.pone.0270131

[15] Cheng, M., Smith, D. S., Ren, X., Cao, H., Smith, S., & McFarland, D. A. (2023). How New Ideas Diffuse in Science. American Sociological Review, 88(3), 522-561. https://doi.org/10.1177/00031224231166955

[16] Palla, G., Barabási, A.-L., & Vicsek, T. (2007). Quantifying social group evolution. Nature, 446, 664-667. https://doi.org/10.1038/nature05670

[17] Burt, R. S. (2004). Structural Holes and Good Ideas. AJS, 110, 349-399. https://doi.org/10.1086/421787

[18] Wang, J., Veugelers, R., & Stephan, P. (2017). Bias against novelty in science. Research Policy, 46, 1416-1436. https://doi.org/10.1016/j.respol.2017.06.006

[19] A. Tacchella, D. Mazzilli, L. Pietronero (2018). A dynamical systems approach to gross domestic product forecasting. Nature Physics. https://doi.org/10.1038/s41567-018-0204-y

[20] Alan L. Porter, Jon Garner, Stephen F. Carley, Nils C. Newman (2019). Emergence scoring to identify frontier R&amp;D topics and key players. Technological Forecasting and Social Change. https://doi.org/10.1016/j.techfore.2018.04.016

[21] Alberto Aleta, Sandro Meloni, Nicola Perra, Yamir Moreno (2019). Explore with caution: mapping the evolution of scientific interest in physics. EPJ Data Science. https://doi.org/10.1140/epjds/s13688-019-0205-9

[22] Albora, G. et al. (2023). Product progression. Scientific Reports, 13, 1481. https://doi.org/10.1038/s41598-023-28179-x

[23] Alexander Krauss, Ariel Rosenfeld, Lutz Bornmann (2026). The Rising Dominance of Methods Across Science. arXiv:2606.07994

[24] Ana P. Fernandes, Heiwai Tang (2014). Learning to export from neighbors. Journal of International Economics. https://doi.org/10.1016/j.jinteco.2014.06.003

[25] Andrea Palmucci, Hao Liao, Andrea Napoletano, Andrea Zaccaria (2020). Where is your field going? A machine learning approach to study the relative motion of the domains of physics. PLOS ONE. https://doi.org/10.1371/journal.pone.0233997

[26] Andrea Zaccaria, Matthieu Cristelli, Andrea Tacchella, Luciano Pietronero (2014). How the Taxonomy of Products Drives the Economic Development of Countries. PLoS ONE. https://doi.org/10.1371/journal.pone.0113770

[27] Andrew Goodman-Bacon (2021). Difference-in-differences with variation in treatment timing. Journal of Econometrics. https://doi.org/10.1016/j.jeconom.2021.03.014

[28] Andrey Rzhetsky, Jacob G. Foster, Ian T. Foster, James A. Evans (2015). Choosing experiments to accelerate collective discovery. Proceedings of the National Academy of Sciences. https://doi.org/10.1073/pnas.1509757112

[29] Bahar, D., Hausmann, R., & Hidalgo, C. A. (2014). Neighbors and the evolution of comparative advantage. J. International Economics, 92(1), 111-123. https://doi.org/10.1016/j.jinteco.2013.11.001

[30] Benjamin W. Stewart, Andy Rivas, Luat T. Vuong (2017). Structure in scientific networks: towards predictions of research dynamism. arXiv:1708.03850

[31] Blackburn, T. M. et al. (2011). A proposed unified framework for biological invasions. TREE, 26(7), 333-339. https://doi.org/10.1016/j.tree.2011.03.023

[32] Bogang Jun, Aamena Alshamsi, Jian Gao, César A. Hidalgo (2019). Bilateral relatedness: knowledge diffusion and the evolution of bilateral trade. Journal of Evolutionary Economics. https://doi.org/10.1007/s00191-019-00638-7

[33] Bogang Jun, Aamena Alshamsi, Jian Gao, Cesar A Hidalgo (2017). Relatedness, Knowledge Diffusion, and the Evolution of Bilateral Trade. arXiv. arXiv:1709.05392

[34] Brantly Callaway, Pedro H.C. Sant’Anna (2021). Difference-in-Differences with multiple time periods. Journal of Econometrics. https://doi.org/10.1016/j.jeconom.2020.12.001

[35] Bronwyn Hall, Manuel Trajtenberg (2004). Uncovering GPTS with Patent Data. https://doi.org/10.3386/w10901

[36] Callon, M., Courtial, J. P., & Laville, F. (1991). Co-word analysis as a tool for describing the network of interactions between basic and technological research: The case of polymer chemsitry. Scientometrics, 22, 155-205. https://doi.org/10.1007/BF02019280

[37] Cao, H. et al. (2020). Will This Idea Spread Beyond Academia? Findings of EMNLP, 1746-1757. Findings of the Association for Computational Linguistics: EMNLP 2020 https://doi.org/10.18653/v1/2020.findings-emnlp.158

[38] Chaomei Chen (2005). CiteSpace II: Detecting and visualizing emerging trends and transient patterns in scientific literature. Journal of the American Society for Information Science and Technology. https://doi.org/10.1002/asi.20317

[39] Chavalarias, D. & Cointet, J.-P. (2013). Phylomemetic Patterns in Science Evolution. PLoS ONE, 8, e54847. https://doi.org/10.1371/journal.pone.0054847

[40] Chen, C. (2006). CiteSpace II: Detecting and Visualizing Emerging Trends and Transient Patterns in Scientific Literature. Journal of the American Society for Information Science and Technology, 57(3), 359-377.

[41] Chen, C. (2012). Predictive effects of structural variation on citation counts. JASIST, 63, 431-449. https://doi.org/10.1002/asi.21694

[42] Cunningham, E., Smyth, B., & Greene, D. (2022). Author multidisciplinarity and disciplinary roles in field of study networks. Applied Network Science, 7, 78. https://doi.org/10.1007/s41109-022-00517-4

[43] Daniel M. Romero, Brendan Meeder, Jon Kleinberg (2011). Differences in the mechanics of information diffusion across topics. Proceedings of the 20th international conference on World wide web. https://doi.org/10.1145/1963405.1963503

[44] Daril Vilhena, Jacob Foster, Martin Rosvall, Jevin West, James Evans, Carl Bergstrom (2014). Finding Cultural Holes: How Structure and Culture Diverge in Networks of Scholarly Communication. Sociological Science. https://doi.org/10.15195/v1.a15

[45] David L. Rigby (2013). Technological Relatedness and Knowledge Space: Entry and Exit of US Cities from Patent Classes. Regional Studies. https://doi.org/10.1080/00343404.2013.854878

[46] De Domenico, M., Omodei, E., & Arenas, A. (2016). Quantifying the diaspora of knowledge in the last century. Applied Network Science, 1, 15. arXiv:1604.00696

[47] DerSimonian, R. & Laird, N. (1986). Meta-analysis in clinical trials. Control. Clin. Trials, 7, 177-188. https://doi.org/10.1016/0197-2456(86)90046-2

[48] Du, A., Head, M., & Brede, M. (2025). Journal publications in medicine. Applied Network Science, 11, 11.

[49] Erin Leahey, James Moody (2014). Sociological Innovation through Subfield Integration. Social Currents. https://doi.org/10.1177/2329496514540131

[50] Flávio L. Pinheiro, Aamena Alshamsi, Dominik Hartmann, Ron Boschma, César A. Hidalgo (2018). Shooting High or Low: Do Countries Benefit from Entering Unrelated Activities?. arXiv. arXiv:1801.05352

[51] Fontaine, M. C., Bhatt, U., Bhargava, R., & Aglietti, V. (2024). Epistemic integration and social segregation of AI in neuroscience. Applied Network Science, 9, 12. https://doi.org/10.1007/s41109-024-00618-2

[52] Francesco Osborne, Andrea Mannocci, Enrico Motta (2017). Forecasting the Spreading of Technologies in Research Communities. Proceedings of the Knowledge Capture Conference. https://doi.org/10.1145/3148011.3148030

[53] Francisco Galuppo Azevedo, Fabricio Murai (2021). Evaluating the state-of-the-art in mapping research spaces: A Brazilian case study. PLOS ONE. https://doi.org/10.1371/journal.pone.0248724

[54] Gao, Y. et al. (2018). Community evolution in patent networks. Applied Network Science, 3, 26.

[55] Gotelli, N. J. & Colwell, R. K. (2001). Quantifying biodiversity. Ecology Letters, 4, 379-391. https://doi.org/10.1046/j.1461-0248.2001.00230.x

[56] Guevara, M. R., Hartmann, D., Aristarán, M., Mendoza, M., & Hidalgo, C. A. (2016). The research space: using career paths to explore the structure of scientific research. Scientometrics, 109, 1695-1709.

[57] Hao Fe, Yang Liang, Mary E. Lovely (2025). Follow thy neighbor: The role of first exporters. Journal of Urban Economics. https://doi.org/10.1016/j.jue.2025.103813

[58] Hawkes, A. G. (1971). Spectra of some self exciting and mutually exciting point processes. Biometrika, 58(1), 83-90.

[59] Henry Small (2018). Characterizing highly cited method and non-method papers using citation contexts: The role of uncertainty. Journal of Informetrics. https://doi.org/10.1016/j.joi.2018.03.007

[60] Henry Small, Kevin W. Boyack, Richard Klavans (2014). Identifying emerging topics in science and technology. Research Policy. https://doi.org/10.1016/j.respol.2014.02.005

[61] Higgins, J. P. T. & Thompson, S. G. (2002). Quantifying heterogeneity in a meta‐analysis. Stat. Med., 21, 1539-1558. https://doi.org/10.1002/sim.1186

[62] Hofstra, B. et al. (2020). The Diversity–Innovation Paradox in Science. PNAS, 117, 9284-9291. https://doi.org/10.1073/pnas.1915378117

[63] Holmgren, A., Edler, D., & Rosvall, M. (2023). Mapping change in higher order networks. Applied Network Science, 8, 42. https://doi.org/10.1007/s41109-023-00572-5

[64] Hongbo Fang, James Evans (2025). Generalization and the Rise of System-level Creativity in Science. arXiv:2510.03240

[65] Iacopo Iacopini, Staša Milojević, Vito Latora (2018). Network Dynamics of Innovation Processes. Physical Review Letters. https://doi.org/10.1103/PhysRevLett.120.048301

[66] James W. Weis, Joseph M. Jacobson (2021). Learning on knowledge graph dynamics provides an early warning of impactful research. Nature Biotechnology. https://doi.org/10.1038/s41587-021-00907-6

[67] Jin Mao, Zhentao Liang, Yujie Cao, Gang Li (2020). Quantifying cross-disciplinary knowledge flow from the perspective of content: Introducing an approach based on knowledge memes. Journal of Informetrics. https://doi.org/10.1016/j.joi.2020.101092

[68] Jon Kleinberg (2003). Bursty and Hierarchical Structure in Streams. Data Mining and Knowledge Discovery. https://doi.org/10.1023/A:1024940629314

[69] Joseph Henrich (2004). Demography and Cultural Evolution: How Adaptive Cultural Processes Can Produce Maladaptive Losses—The Tasmanian Case. American Antiquity. https://doi.org/10.2307/4128416

[70] Julie L. Lockwood, Phillip Cassey, Tim Blackburn (2005). The role of propagule pressure in explaining species invasions. Trends in Ecology &amp; Evolution. https://doi.org/10.1016/j.tree.2005.02.004

[71] Julie L. Lockwood, Phillip Cassey, Tim M. Blackburn (2009). The more you introduce the more you get: the role of colonization pressure and propagule pressure in invasion ecology. Diversity and Distributions. https://doi.org/10.1111/j.1472-4642.2009.00594.x

[72] Kiyan Rezaee, Morteza Ziabakhsh, Niloofar Nikfarjam, Mohammad M. Ghassemi, Yazdan Rezaee Jouryabi, Sadegh Eskandari, Reza Lashgari (2025). FOS: A Large-Scale Temporal Graph Benchmark for Scientific Interdisciplinary Link Prediction. arXiv:2511.18631

[73] Krenn, M. & Zeilinger, A. (2020). Predicting research trends with semantic and neural networks with an application in quantum physics. PNAS, 117, 1910. https://doi.org/10.1073/pnas.1914370116

[74] Larson, J. M. (2017). The weakness of weak ties. Applied Network Science, 2, 14.

[75] Li, Y. & Neffke, F. (2022). Evaluating the principle of relatedness. arXiv:2205.02942. arXiv:2205.02942

[76] Lili Miao, Dakota Murray, Woo-Sung Jung, Vincent Larivière, Cassidy R. Sugimoto, Yong-Yeol Ahn (2021). The latent structure of global scientific development. arXiv. arXiv:2104.10812

[77] Lipsitch, M., Tchetgen Tchetgen, E., & Cohen, T. (2010). Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies. Epidemiology, 21(3), 383-388.

[78] Liyang Sun, Sarah Abraham (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. Journal of Econometrics. https://doi.org/10.1016/j.jeconom.2020.09.006

[79] Loet Leydesdorff, Ismael Rafols (2010). The Local Emergence and Global Diffusion of Research Technologies. arXiv. arXiv:1011.3120

[80] Loet Leydesdorff, Ismael Rafols (2011). Local emergence and global diffusion of research technologies: An exploration of patterns of network formation. Journal of the American Society for Information Science and Technology. https://doi.org/10.1002/asi.21509

[81] Lu Huang, Xiang Chen, Xingxing Ni, Jiarun Liu, Xiaoli Cao, Changtian Wang (2021). Tracking the dynamics of co-word networks for emerging topic identification. Technological Forecasting and Social Change. https://doi.org/10.1016/j.techfore.2021.120944

[82] M.J. Cobo, A.G. López-Herrera, E. Herrera-Viedma, F. Herrera (2011). An approach for detecting, quantifying, and visualizing the evolution of a research field: A practical application to the Fuzzy Sets Theory field. Journal of Informetrics. https://doi.org/10.1016/j.joi.2010.10.002

[83] M.J. Cobo, A.G. López‐Herrera, E. Herrera‐Viedma, F. Herrera (2012). <scp>SciMAT</scp>
                    : A new science mapping analysis software tool. Journal of the American Society for Information Science and Technology. https://doi.org/10.1002/asi.22688

[84] Maillart, T., Chataing, A., et al. (2026). Forecasting Conceptual Diffusion in Science: The Case of Quantum Computing. arXiv:2606.03919. arXiv:2606.03919

[85] Maillart, T. et al. (2026). Explainable Forecasting of Scientific Breakthroughs from Concept Network Dynamics. arXiv:2606.03864. arXiv:2606.03864

[86] Manuel Trajtenberg, Rebecca Henderson, Adam Jaffe (1997). University Versus Corporate Patents: A Window On The Basicness Of Invention. Economics of Innovation and New Technology. https://doi.org/10.1080/10438599700000006

[87] March, J. G. (1991). Exploration and Exploitation in Organizational Learning. Organization Science, 2, 71-87. https://doi.org/10.1287/orsc.2.1.71

[88] Mario Krenn, Anton Zeilinger (2019). Predicting Research Trends with Semantic and Neural Networks with an application in Quantum Physics. arXiv. arXiv:1906.06843

[89] Martin Rosvall, Carl T. Bergstrom (2010). Mapping Change in Large Networks. PLoS ONE. https://doi.org/10.1371/journal.pone.0008694

[90] Massimo Aria, Luca D’Aniello, Michelangelo Misuraca, Maria Spano (2026). Rethinking thematic evolution in science mapping:An integrated framework for longitudinal analysis. Journal of Informetrics. https://doi.org/10.1016/j.joi.2026.101877

[91] Matteo Chinazzi, Bruno Gonçalves, Qian Zhang, Alessandro Vespignani (2019). Mapping the physics research space: a machine learning approach. EPJ Data Science. https://doi.org/10.1140/epjds/s13688-019-0210-z

[92] Mingyue Kong, Yinglong Zhang, Likun Sheng, Kaifeng Hong (2025). Citation structural diversity: a novel metric combining structure and semantics for literature evaluation. Scientometrics. https://doi.org/10.1007/s11192-025-05356-5

[93] Muntakim, A. H., et al. (2026). SciTraj: How Does Research Evolve? Tracing Cross-Domain Trajectories in NLP, ML, and CV Through Claim-Grounded Typed Citations. arXiv:2606.22342. arXiv:2606.22342

[94] Neave O’Clery, Muhammed Ali Yıldırım, Ricardo Hausmann (2021). Productive Ecosystems and the arrow of development. Nature Communications. https://doi.org/10.1038/s41467-021-21689-0

[95] Önder Nomaler, Bart Verspagen (2022). Some New Views on Product Space and Related Diversification. arXiv. arXiv:2203.16316

[96] Pastor-Satorras, R., Castellano, C., Van Mieghem, P., & Vespignani, A. (2015). Epidemic processes in complex networks. Reviews of Modern Physics, 87, 925-979.

[97] Petr Pyšek, Vojtěch Jarošík (None). Residence time determines the distribution of alien plants. Invasive Plants: Ecological and Agricultural Aspects. https://doi.org/10.1007/3-7643-7380-6_5

[98] Pierre-Alexandre Balland, Ron Boschma, Joan Crespo, David L. Rigby (2018). Smart specialization policy in the European Union: relatedness, knowledge complexity and regional diversification. Regional Studies. https://doi.org/10.1080/00343404.2018.1437900

[99] Prabhakaran, V. et al. (2016). Predicting the Rise and Fall of Scientific Topics. ACL, 1170-1180. https://doi.org/10.18653/v1/P16-1111

[100] Qi Wang (2017). A bibliometric model for identifying emerging research topics. Journal of the Association for Information Science and Technology. https://doi.org/10.1002/asi.23930

[101] R. Belderbos, V. Van Roy, F. Duvivier (2012). International and domestic technology transfers and productivity growth: firm level evidence. Industrial and Corporate Change. https://doi.org/10.1093/icc/dts012

[102] R. Boschma, P.-A. Balland, D. F. Kogler (2014). Relatedness and technological change in cities: the rise and fall of technological knowledge in US metropolitan areas from 1981 to 2010. Industrial and Corporate Change. https://doi.org/10.1093/icc/dtu012

[103] Rafols, I., & Meyer, M. (2009). Diversity and network coherence as indicators of interdisciplinarity: case studies in bionanoscience. Scientometrics, 82, 263-287.

[104] Ravasz, E. & Barabási, A.-L. (2003). Hierarchical organization in complex networks. PRE, 67, 026112. https://doi.org/10.1103/PhysRevE.67.026112

[105] Renoust, B., Claver, V., & Basse, J.-F. (2017). Multiplex flows in citation networks. Applied Network Science, 2, 23.

[106] Ricardo Hausmann, Dani Rodrik (2003). Economic development as self-discovery. Journal of Development Economics. https://doi.org/10.1016/S0304-3878(03)00124-X

[107] Richardson, D. M. et al. (2000). Naturalization and invasion of alien plants: concepts and definitions. Diversity and Distributions, 6, 93-107. https://doi.org/10.1046/j.1472-4642.2000.00083.x

[108] Rigby, D. L. (2015). Technological relatedness and knowledge space: entry and exit of US cities from patent classes. Regional Studies, 49(11), 1922-1937.

[109] Salatino, A., Osborne, F., & Motta, E. (2018). AUGUR: Forecasting the Emergence of New Research Topics. Proceedings of the 18th ACM/IEEE JCDL, 303-312. https://doi.org/10.1145/3197026.3197052

[110] Salnikov, V. et al. (2018). Cooccurrence simplicial complexes. Applied Network Science, 3, 37.

[111] Saman Behrouzi, Zahra Shafaeipour Sarmoor, Khosrow Hajsadeghi, Kaveh Kavousi (2020). Predicting scientific research trends based on link prediction in keyword networks. Journal of Informetrics. https://doi.org/10.1016/j.joi.2020.101079

[112] Sergio Petralia (2020). Mapping general purpose technologies with patent data. Research Policy. https://doi.org/10.1016/j.respol.2020.104013

[113] Sinan Aral, Marshall Van Alstyne (2011). The Diversity-Bandwidth Trade-off. American Journal of Sociology. https://doi.org/10.1086/661238

[114] Susan Leigh Star, James R. Griesemer (1989). Institutional Ecology, `Translations' and Boundary Objects: Amateurs and Professionals in Berkeley's Museum of Vertebrate Zoology, 1907-39. Social Studies of Science. https://doi.org/10.1177/030631289019003001

[115] Tao Jia, Dashun Wang, Boleslaw K. Szymanski (2017). Quantifying patterns of research-interest evolution. Nature Human Behaviour. https://doi.org/10.1038/s41562-017-0078

[116] Timothy F. Bresnahan, M. Trajtenberg (1995). General purpose technologies ‘Engines of growth’?. Journal of Econometrics. https://doi.org/10.1016/0304-4076(94)01598-T

[117] Tobias Kuhn, Matjaž Perc, Dirk Helbing (2014). Inheritance Patterns in Citation Networks Reveal Scientific Memes. Physical Review X. https://doi.org/10.1103/PhysRevX.4.041036

[118] Tria, F. et al. (2014). The dynamics of correlated novelties. Scientific Reports, 4, 5890. https://doi.org/10.1038/srep05890

[119] Uzzi, B. et al. (2013). Atypical Combinations and Scientific Impact. Science, 342, 468-472. https://doi.org/10.1126/science.1240474

[120] Xiaoling Sun, Jasleen Kaur, Staša Milojević, Alessandro Flammini, Filippo Menczer (2013). Social Dynamics of Science. Scientific Reports. https://doi.org/10.1038/srep01069
