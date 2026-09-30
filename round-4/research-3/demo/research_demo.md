# Is 'keep exploring, spread widest' already known?

## Summary

Novelty and positioning report (iteration 4) for the Exp8 openness-vs-consolidation claim, for the Applied Network Science paper. It builds on art_EesdB8cuSfcU and art_dxvRpQufMR0e without redoing their work. Files: research_report.md (Sections A-I), reproducibility.md, raw/ (query log, fetched page extracts, verify.json).

VERDICTS
- C1, openness → later cross-field breadth: PARTIALLY ANTICIPATED. The same direction is shown for concept pairs (Maillart 2026: test R² 0.69 entropy / 0.78 exogenous, random 80/20 split), papers (Wang 2017: odds of top-1% citation in foreign fields +62.37%), memes (Weng 2013) and people (Ugander 2012). Concept-level evidence exists only for volume (Cheng 2023) or transfer to patents (Cao 2020). No study found combines the concept unit, a size-adjusted breadth outcome and held-out fields.
- C2, consolidation → less breadth: PARTIALLY ANTICIPATED in mechanism (Palla 2007 large-group turnover; Ugander; Weng; Burt) and CONTRADICTED-BY on other outcomes:
  - Cheng et al. 2023 ASR, full text read: "ideational consistency" = cosine of neighbour co-usage t−1→t, i.e. weighted edge persistence. +53% next-year articles per SD (b = .43); embeddedness +25%; author co-author density −15%. The DV is volume at t+1, with no current-volume control and in-sample. The authors state they do not study cross-domain translation.
  - Chavalarias & Cointet 2013: dense term-clusters survive; density rises during emergence and falls before decline.
  - Centola 2010 and Romero 2011: clustering helps adoption.
  - Salatino 2017: density among parent topics precedes birth.
  Recommended framing: an outcome-dependent reversal (consistency → depth/survival, churn → reach).
- C3, a low retention ratio of contacted fields: NEW (analogues only: propagule/colonisation pressure; Palla; Cheng's social consistency b = .02).
- C4, within-concept closure → entry slowdown: NEW as a lead-lag test. The field-level prior is opposite (Chavalarias). Life-cycle analogues: Singh 2022, Prabhakaran 2016.

WHAT THE REPORT PROVIDES
- An our-numbers card (Exp8 held-out psp|B5 with CIs and I²).
- Strand-by-strand extraction rows for S1-S9.
- A Cheng operationalisation box with the reconciling sentence.
- T-RQ1: ours vs Maillart, Cheng, Cao, Wang, Weng, Ugander, Salatino, Chen, Kong. Level AUCs (Krenn 0.85; 0.954-0.967) are marked not comparable.
- T-RQ2: 12 trajectory/sequence comparators; our contact × retention decomposition and FE event study have no counterpart.
- 8 ANS papers with relation lines.
- An 8-lane Fig. 1 spec with {pipeline_counts.json:KEY} slots and a caption.
- A 14-row reviewer-threat table.
- 68 newly verified references, 66/67 identifiers resolved via Crossref/arXiv, plus 12 carried.

CORRECTIONS AND DESIGN GAPS
- Corrected DOIs: Chen 2012 = 10.1002/asi.21694 (not asi.22662); Moser & Nicholas = 10.1257/0002828041301407; Feldman & Yoon = 10.1093/icc/dtr040.
- UNVERIFIED (do not cite): Van Noorden 2014, Shinn & Joerges 2002, Fujimura 1992, arXiv 2209.03687 / 2408.06839 / 2606.25320.
- DESIGN GAPS for the experiments:
  1. ego_density_W3 is not degree-normalised (Ravasz & Barabási C(k) ~ 1/k); add a configuration-null z-score.
  2. Run Cheng's exact consistency/embeddedness measures on volume vs breadth; the predicted result is a sign flip.
  3. Report survival alongside breadth and test the size × turnover interaction (Palla).
  4. Concept-type tagging with within-type tests; no prior effect size exists.
  5. Heterogeneity-robust staggered event-study estimators for C4.

## Research Findings

VERDICTS (full tables and extraction rows in research_report.md, Sections A-D). Our comparator numbers are internal Exp8 held-out results, not web sources. They are pooled partial Spearman given the B5 count baseline, with rarefied off-home field breadth at t0+6..t0+8 as the outcome:
- new_edge_rate +0.118 [0.072, 0.163]
- n_comm_W3 +0.167 (I² 0.78)
- participation +0.150
- NOV_res +0.139
- ego_density_W3 −0.102 [−0.151, −0.053]
- edge_persistence −0.080 [−0.126, −0.033]
- RETENTION_RATIO_early −0.114 [−0.160, −0.067]
- CONTACT_REACH +0.211
- growth nulls ≈ 0
- ElasticNet over B5: ΔSpearman +0.059 [0.046, 0.073]

C1, openness (new partners, many communities, novelty) → later breadth: PARTIALLY ANTICIPATED. The direction is well established at other units:
- concept pairs, where upstream heterogeneity predicts downstream adoption diversity (test R² 0.69; exogenous 0.78; stratified 80/20 random split, not field hold-out) [2];
- papers, where highly novel papers have 62.37% higher odds of top-1% citation in foreign fields [24], and outsiders produce surprising, high-impact work [25]; citation structural diversity also correlates with topic breadth [37];
- memes, where early multi-community spread predicts virality [31];
- people, where connected components of the contact neighbourhood control adoption [30].
At the concept level it appears only for other outcomes: volume [1] and transfer to patents [16]. No study found combines the concept unit, a size-adjusted cross-field breadth outcome and held-out fields.

C2, early consolidation → less breadth: PARTIALLY ANTICIPATED in mechanism, and CONTRADICTED-BY on other outcomes.
- Cheng et al.'s "ideational consistency" is the cosine of a term's neighbour co-usage from t−1 to t, i.e. count-weighted edge persistence. It raises next-year article counts by 53% per SD. Semantic embeddedness raises them by 25% per SD [1].
- Dense term clusters survive longer. Density rises during emergence and falls before decline [8]. Callon's density was read as a cluster's capacity to maintain itself [3, 8].
- Clustering aids complex-contagion adoption [32, 33].
- Rising density among parent topics precedes topic birth [9].
- Supporting precedents come from social/group units: large groups persist only with membership turnover [36], edge density is uninformative once components are counted [30], and brokerage [34].
- Cheng's outcome is volume, in-sample, with no current-volume control, and the authors state they "do not explore how an idea translates across domains" [1]. So the defensible framing is an outcome-dependent reversal: consistency supports depth and persistence, churn supports reach.

C3, a low retention ratio of contacted fields → breadth: NEW. The analogues are propagule and colonisation pressure [58, 59], group turnover [36], and Cheng's near-null social consistency (b = .02) [1].

C4, within-concept closure precedes an entry slowdown: NEW as a within-unit lead-lag test. The field-level prior runs the other way (density falls before decline) [8]. Life-cycle descriptions show interdisciplinary, small-team early phases and specialised later phases [54], and method-framed topics in growth [46].

OTHER FINDINGS.
- Strategic diagrams are descriptive and theme-level, with an unresolved "emerging or disappearing" quadrant [4, 6].
- GPT generality is defined ex post [39, 40]. Our n_comm/participation are its co-occurrence analogue, so results must be conditioned on CONTACT_REACH.
- No effect size was found for method concepts reaching more fields than object concepts [45-47], so type must be tested within type.
- Level AUCs (0.85 [69]; 0.954-0.967) are not comparable to our increments.

CONTRIBUTION STATEMENT. "The first held-out, size-adjusted, concept-level test showing that early co-occurrence openness predicts later cross-field breadth, while early consolidation, which predicts volume and survival elsewhere [1, 8], does not."

DESIGN GAPS.
(1) Ego density is not degree-normalised, and local density scales about as 1/k [60].
(2) Run Cheng's exact measures on volume versus breadth in our frame.
(3) Report survival alongside breadth [8, 36].
(4) Use heterogeneity-robust event-study estimators for C4 [64, 65].

CONFIDENCE. High for the extracted definitions and numbers. Moderate for C3 and C4 novelty, because coverage outside science is partial. The verdicts would move to ANTICIPATED if a concept-level study with field hold-out and a breadth outcome surfaced; the three method-entity arXiv papers listed as unread are the first to check.

## Sources

[1] [How New Ideas Diffuse in Science (American Sociological Review 88:522-561)](https://journals.sagepub.com/doi/full/10.1177/00031224231166955) (Mengjie Cheng, Daniel Scott Smith, Xiang Ren, Hancheng Cao, Sanne Smith, Daniel A. McFarland; 2023) — Full text read. 56,540 new WoS terms; DV = articles using the term at t+1 (volume, no lagged-DV control); multilevel over-dispersed Poisson, in-sample. Ideational consistency (cosine of neighbour co-usage t-1 to t = weighted edge persistence) b=.43 (+53%/SD); ideational embeddedness b=.22; social embeddedness (author density) b=-.16. Main CONTRADICTED-BY source for C2 (volume outcome).

> rate of co-usage with the focal term in year

Locator: Table 2, Ideational consistency

> A one standard deviation increase in ideational consistency of a new idea is associated with a 53 percent

Locator: Results, The Effects of Ideational and Social Ecology

> a one standard deviation change in social embeddedness is associated with a 15 percent

Locator: Results

> We construct our dependent variable as the number of articles a new idea diffuses into the year ahead

Locator: Outcome of Interest

> we do not explore how an idea translates across domains or corpora

Locator: Limitations

[2] [Forecasting Conceptual Diffusion in Science: The Case of Quantum Computing (arXiv 2606.03919)](https://arxiv.org/pdf/2606.03919) (Thomas Maillart, Thibaut Chataing, David Dosu, Paul Bagourd, Julian Jang-Jaccard, Alain Mermoud; 2026) — Concept PAIRS in the OpenAlex quantum-computing subtree; upstream citation heterogeneity/entropy predicts downstream exogenous count (test R2 0.7804) and adoption entropy (0.6866); endogenous 0.0179 after growth normalisation; stratified 80/20 random split (not field hold-out). Closest C1 near-miss.

> stratified 80/20 train

Locator: Table 2 caption

> endogenous reinforcement proves largely unpredictable in the primary

Locator: Abstract

> exogenous count task achieves strong and consistent predictive power

Locator: Results

[3] [Co-word analysis as a tool for describing the network of interactions between basic and technological research (Scientometrics 22:155-205)](https://doi.org/10.1007/BF02019280) (M. Callon, J. P. Courtial, F. Laville; 1991) — Origin of density/centrality strategic diagrams; density read as a cluster's capacity to maintain itself (as quoted in Chavalarias & Cointet). Descriptive; DOI verified via Crossref.

[4] [An approach for detecting, quantifying, and visualizing the evolution of a research field (J Informetr 5:146-166)](https://sci2s.ugr.es/sites/default/files/ficherosPublicaciones/1321_mjcobo-joi-2010.pdf) (M.J. Cobo, A.G. López-Herrera, E. Herrera-Viedma, F. Herrera; 2011) — Defines Callon centrality/density and the four strategic-diagram quadrants; the low/low quadrant is ambiguous (emerging or disappearing); no predictive test.

> The themes of this quadrant have low density and low centrality, mainly representing either emerging or disappearing themes.

Locator: Section 3.2

[5] [SciMAT: A new science mapping analysis software tool (JASIST 63:1609-1630)](https://doi.org/10.1002/asi.22688) (M.J. Cobo, A.G. López-Herrera, E. Herrera-Viedma, F. Herrera; 2012) — Software operationalising strategic diagrams and thematic evolution; descriptive.

[6] [Rethinking Thematic Evolution in Science Mapping: An Integrated Framework for Longitudinal Analysis (J Informetr 20:101877)](https://arxiv.org/abs/2603.06436) (Massimo Aria, Luca D'Aniello, Michelangelo Misuraca, Maria Spano; 2026) — Recent critique/reframing of longitudinal strategic diagrams; framework, no predictive validation.

> Yet a structural inconsistency characterises dominant longitudinal implementations

Locator: Abstract

[7] [Software engineering as seen through its research literature: a study in co-word analysis (JASIS 49:1206-1223)](https://doi.org/10.1002/(sici)1097-4571(1998)49:13<1206::aid-asi7>3.0.co;2-f) (Neal Coulter, Ira Monarch, Suresh Konda; 1998) — Classic co-word strategic-diagram application; DOI found via Crossref bibliographic query.

[8] [Phylomemetic Patterns in Science Evolution - The Rise and Fall of Scientific Fields (PLoS ONE 8:e54847)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0054847) (David Chavalarias, Jean-Philippe Cointet; 2013) — Term-cluster fields: density higher for long-lived/steady fields, rises during emergence and falls before decline. CONTRADICTED-BY for C2 (survival outcome) and opposite timing prior for C4.

> steady fields have a density of up to twice the average value, whereas ephemeral fields always have a below-average density

Locator: Results, density

> the density grows when a new field is emerging, and decreases when the field starts to be neglected by the community

Locator: Figure 5 caption

[9] [How are topics born? Understanding the research dynamics preceding the emergence of new areas (PeerJ CS 3:e119)](https://peerj.com/articles/cs-119.pdf) (Angelo A. Salatino, Francesco Osborne, Enrico Motta; 2017) — Rising collaboration pace and density among PARENT topics precede topic birth (75 debutant vs 100 control topics, CS). Different unit/outcome; reads as opposite sign to C2.

> the pace of collaboration and the density measured in the sections of the network that will give rise to a new topic are significantly higher than those in the control group

Locator: Introduction

[10] [AUGUR: Forecasting the Emergence of New Research Topics (JCDL 2018:303-312)](https://doi.org/10.1145/3197026.3197052) (Angelo A. Salatino, Francesco Osborne, Enrico Motta; 2018) — Forecasts topic emergence from diachronic co-occurrence dynamics of research-area clusters (carried from prior report).

[11] [Identifying emerging topics in science and technology (Res Policy 43:1450-1467)](https://doi.org/10.1016/j.respol.2014.02.005) (Henry Small, Kevin W. Boyack, Richard Klavans; 2014) — Novelty+growth nomination of 71 emerging topics; no held-out metric (carried).

[12] [What is an emerging technology? (Res Policy 44:1827-1843)](https://doi.org/10.1016/j.respol.2015.06.006) (Daniele Rotolo, Diana Hicks, Ben R. Martin; 2015) — Five attributes of emergence; definitional baseline.

[13] [Predictive effects of structural variation on citation counts (JASIST 63:431-449)](http://cluster.ischool.drexel.edu/~cchen/papers/2012/jasist2012-predictive.pdf) (Chaomei Chen; 2012) — Paper-level boundary-spanning metrics (modularity change, cluster linkage, centrality divergence) predict citations (ZINB, 5 cases). Correct DOI 10.1002/asi.21694; the plan's 10.1002/asi.22662 is a different paper.

> Centrality Divergence metric is potentially

Locator: Abstract

[14] [Towards an explanatory and computational theory of scientific discovery (J Informetr 3:191-209)](https://doi.org/10.1016/j.joi.2009.03.004) (Chaomei Chen, Yue Chen, Mark Horowitz, Haiyan Hou, Zeyuan Liu, Donald Pellegrino; 2009) — Structural-variation / boundary-spanning theory of discovery; conceptual C1 precedent (Crossref query).

[15] [Tracking the dynamics of co-word networks for emerging topic identification (TFSC 170:120944)](https://doi.org/10.1016/j.techfore.2021.120944) (Lu Huang, Xiang Chen, Xingxing Ni, Jiarun Liu, Xiaoli Cao, Changtian Wang; 2021) — Dynamic co-word link prediction + BPNN for emerging topics; link-level, not comparable.

[16] [Will This Idea Spread Beyond Academia? Understanding Knowledge Transfer of Scientific Concepts across Text Corpora (Findings of EMNLP 2020:1746-1757)](https://aclanthology.org/2020.findings-emnlp.158.pdf) (Hancheng Cao, Mengjie Cheng, Zhepeng Cen, Daniel McFarland, Xiang Ren; 2020) — Concept-level (450k new concepts) prediction of transfer into patents/clinical trials with temporal cutoffs; interdisciplinary-venue usage is an early sign. C1 same direction, different outcome.

> usage in interdisciplinary venues

Locator: Introduction

[17] [Forecasting the Spreading of Technologies in Research Communities (K-CAP 2017:1-8)](https://doi.org/10.1145/3148011.3148030) (Francesco Osborne, Andrea Mannocci, Enrico Motta; 2017) — Technology-to-research-area propagation forecasting (technology-topic pairs); RQ2 local-origin-then-spread framing; abstract level.

[18] [Inheritance Patterns in Citation Networks Reveal Scientific Memes (PRX 4:041036)](https://doi.org/10.1103/PhysRevX.4.041036) (Tobias Kuhn, Matjaž Perc, Dirk Helbing; 2014) — Meme score from frequency and propagation along citations; no openness predictor.

[19] [Social Dynamics of Science (Sci Rep 3:1069)](https://doi.org/10.1038/srep01069) (Xiaoling Sun, Jasleen Kaur, Staša Milojević, Alessandro Flammini, Filippo Menczer; 2013) — Agent-based model: disciplines emerge from splitting and merging of collaboration communities (abstract).

[20] [Quantifying cross-disciplinary knowledge flow from the perspective of content: knowledge memes (J Informetr 14:101092)](https://doi.org/10.1016/j.joi.2020.101092) (Jin Mao, Zhentao Liang, Yujie Cao, Gang Li; 2020) — Knowledge-meme diffusion cascades between Medical Informatics and four disciplines; descriptive RQ2 comparator.

[21] [The Local Emergence and Global Diffusion of Research Technologies (JASIST 62:846-860)](https://arxiv.org/pdf/1011.3120) (Loet Leydesdorff, Ismael Rafols; 2011) — siRNA vs nanocrystalline solar cells; local emergence then global diffusion; mode-1 to mode-2 transition explains rate differences.

> The strength of preferential attachment decreases over time

Locator: Abstract

[22] [Atypical Combinations and Scientific Impact (Science 342:468-472)](https://doi.org/10.1126/science.1240474) (Brian Uzzi, Satyam Mukherjee, Michael Stringer, Ben Jones; 2013) — Paper-level: conventional core plus atypical combinations predicts high impact.

[23] [Tradition and Innovation in Scientists' Research Strategies (ASR 80:875-908)](https://doi.org/10.1177/0003122415601618) (Jacob G. Foster, Andrey Rzhetsky, James A. Evans; 2015) — Exploration vs tradition strategies in biomedical chemistry; risky innovation rarely chosen, rewarded.

[24] [Bias against novelty in science: A cautionary tale for users of bibliometric indicators (Res Policy 46:1416-1436; NBER w22180)](https://www.nber.org/system/files/working_papers/w22180/w22180.pdf) (Jian Wang, Reinhilde Veugelers, Paula Stephan; 2017) — Paper-level novelty (new distant journal pairs) raises foreign-field citation impact: odds of top-1% in foreign fields +29.39%/+62.37%; not in home field. Closest paper-level C1 analogue.

> 29.39% and 62.37% higher for moderately and highly novel papers respectively

Locator: Section 4 (home vs foreign field)

[25] [Surprising combinations of research contents and contexts are related to impact and emerge with scientific outsiders from distant disciplines (Nat Commun 14:1641)](https://www.nature.com/articles/s41467-023-36741-4) (Feng Shi, James Evans; 2023) — Surprise predicts outsized impact and emerges when outsiders publish to distant audiences; paper-level C1 analogue.

> most commonly when scientists from one field publish problem-solving results to an audience from a distant field

Locator: Abstract

[26] [The dynamics of correlated novelties (Sci Rep 4:5890)](https://doi.org/10.1038/srep05890) (F. Tria, V. Loreto, V. D. P. Servedio, S. H. Strogatz; 2014) — Adjacent-possible urn model; theory anchor for exploration.

[27] [Network Dynamics of Innovation Processes (PRL 120:048301)](https://doi.org/10.1103/PhysRevLett.120.048301) (Iacopo Iacopini, Staša Milojević, Vito Latora; 2018) — Random walks on concept networks reproduce novelty rates; no later-spread test.

[28] [The Diversity-Innovation Paradox in Science (PNAS 117:9284-9291)](https://www.pnas.org/doi/10.1073/pnas.1915378117) (Bas Hofstra, Vivek V. Kulkarni, Sebastian Munoz-Najar Galvez, Bryan He, Dan Jurafsky, Daniel A. McFarland; 2020) — Concept-link novelty and uptake-per-link measure in dissertations; uptake precedent.

> taken up by other scholars at lower rates

Locator: Significance

[29] [Generalization and the Rise of System-level Creativity in Science (arXiv 2510.03240)](https://arxiv.org/abs/2510.03240) (Hongbo Fang, James Evans; 2025) — Paper-level citation-role typology (foundations/extensions/generalizations) on OpenAlex and WoS; generality defined from downstream reuse (outcome-side).

> we decompose scientific contributions into three functional types, foundations, extensions, and generalizations

Locator: Abstract

[30] [Structural diversity in social contagion (PNAS 109:5962-5966)](https://www.pnas.org/doi/10.1073/pnas.1116502109) (Johan Ugander, Lars Backstrom, Cameron Marlow, Jon Kleinberg; 2012) — Number of connected components of the contact neighbourhood controls adoption; size becomes a negative predictor; edge density uninformative within one-component neighbourhoods.

> the size of the contact neighborhood is in fact generally a negative predictor of contagion

Locator: Abstract

> probability of contagion is tightly controlled by the number of connected components

Locator: Abstract

[31] [Virality Prediction and Community Structure in Social Networks (Sci Rep 3:2522)](https://arxiv.org/pdf/1306.0158) (Lilian Weng, Filippo Menczer, Yong-Yeol Ahn; 2013) — Early spread across many communities (first adopters) predicts meme virality at about 7x random precision (carried from art_dxvRpQufMR0e).

> about seven times as precise as random guess

Locator: Results, prediction (carried)

[32] [The Spread of Behavior in an Online Social Network Experiment (Science 329:1194-1197)](https://doi.org/10.1126/science.1185231) (Damon Centola; 2010) — Clustered-lattice networks spread behaviour farther and faster than random ones (complex contagion); CONTRADICTED-BY for C2 at the adoption-depth level.

[33] [Differences in the mechanics of information diffusion across topics: idioms, political hashtags, and complex contagion on Twitter (WWW 2011:695-704)](https://www.cs.cornell.edu/home/kleinber/www11-hashtags.pdf) (Daniel M. Romero, Brendan Meeder, Jon Kleinberg; 2011) — Persistent (complex-contagion) political hashtags have denser early-adopter subgraphs; idioms are non-persistent.

> hashtags on politically controversial topics are particularly persistent

Locator: Abstract

[34] [Structural Holes and Good Ideas (AJS 110:349-399)](https://doi.org/10.1086/421787) (Ronald S. Burt; 2004) — Brokerage across structural holes yields good ideas; constraint mechanism for C2.

[35] [The Diversity-Bandwidth Trade-off (AJS 117:90-171)](https://doi.org/10.1086/661238) (Sinan Aral, Marshall Van Alstyne; 2011) — Structural diversity vs channel bandwidth trade-off for novel information.

[36] [Quantifying social group evolution (Nature 446:664-667)](https://arxiv.org/pdf/0704.0744) (Gergely Palla, Albert-László Barabási, Tamás Vicsek; 2007) — Large communities persist longer when membership turns over; small ones need stable composition. Partial precedent for churn (C2/C3) with a size interaction.

> large groups persist longer if they are capable of dynamically altering their

Locator: Abstract

> The behaviour of small groups displays the opposite tendency

Locator: Abstract

[37] [Citation structural diversity: a novel metric combining structure and semantics for literature evaluation (Scientometrics 130:4027-4060)](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/s11192-025-05356-5?fields=title,year,authors,venue,abstract,externalIds) (Mingyue Kong, Yinglong Zhang, Likun Sheng, Kaifeng Hong; 2025) — Paper-level citation structural diversity correlates with citations and topic breadth; abstract level, no size control reported.

> structural diversity is shown to be positively correlated with topic breadth

Locator: Abstract

[38] [General purpose technologies 'Engines of growth'? (J Econometrics 65:83-108)](https://doi.org/10.1016/0304-4076(94)01598-T) (Timothy F. Bresnahan, M. Trajtenberg; 1995) — GPT concept anchor.

[39] [University Versus Corporate Patents: A Window On The Basicness Of Invention (EINT 5:19-50)](https://doi.org/10.1080/10438599700000006) (Manuel Trajtenberg, Rebecca Henderson, Adam Jaffe; 1997) — Origin of the generality index (ex-post, citing-class Herfindahl complement).

[40] [Uncovering GPTs with Patent Data (NBER w10901)](https://www.nber.org/system/files/working_papers/w10901/w10901.pdf) (Bronwyn Hall, Manuel Trajtenberg; 2004) — Generality defined from forward citations across classes (ex-post); used to flag GPT candidates, not tested as an early predictor of later generality.

> cited by subsequent patents that belong to a wide range of fields

Locator: Section 3.1 Generality

[41] [Was Electricity a General Purpose Technology? Evidence from Historical Patent Citations (AER 94:388-394)](https://doi.org/10.1257/0002828041301407) (Petra Moser, Tom Nicholas; 2004) — GPT test via patent citations; DOI corrected (plan's guess returned 404).

[42] [An empirical test for general purpose technology: an examination of the Cohen-Boyer rDNA technology (ICC 21:249-275)](https://doi.org/10.1093/icc/dtr040) (M. P. Feldman, J. W. Yoon; 2012) — GPT test on rDNA; DOI corrected (plan's guess pointed to a different paper).

[43] [Mapping general purpose technologies with patent data (Res Policy 49:104013)](https://doi.org/10.1016/j.respol.2020.104013) (Sergio Petralia; 2020) — Three-dimension GPT indicator (growth, range of uses via text mining, complementarity).

[44] [Measuring Patent Quality: Indicators of Technological and Economic Value (OECD STI WP 2013/03)](https://doi.org/10.1787/5k4522wkw1r8-en) (2013) — OECD operationalisation of generality/originality indicators.

[45] [Characterizing highly cited method and non-method papers using citation contexts: The role of uncertainty (J Informetr 12:461-480)](https://doi.org/10.1016/j.joi.2018.03.007) (Henry Small; 2018) — Method vs non-method classification of the top-1000 biomedical papers; no cross-field reach effect size.

[46] [Predicting the Rise and Fall of Scientific Topics from Trends in their Rhetorical Framing (ACL 2016:1170-1180)](https://aclanthology.org/P16-1111.pdf) (Vinodkumar Prabhakaran, William L. Hamilton, Dan McFarland, Dan Jurafsky; 2016) — Topics framed as methods are in early growth; result-framed topics decline. Concept-type (S7) and life-cycle (C4) evidence.

> rhetorical function is highly predictive of

Locator: Abstract

[47] [The Rising Dominance of Methods Across Science (arXiv 2606.07994)](https://arxiv.org/pdf/2606.07994) (Alexander Krauss, Ariel Rosenfeld, Lutz Bornmann; 2026) — Methods-paper share doubled (~20% to 40%) 1980-2019 across disciplines; argues methods transfer across fields but gives no cross-field reach effect size.

> share of methods papers doubled over the past four decades

Locator: Introduction

[48] [Exploration and Exploitation in Organizational Learning (Org Sci 2:71-87)](https://doi.org/10.1287/orsc.2.1.71) (James G. March; 1991) — Theory anchor for exploration vs exploitation framing.

[49] [Institutional Ecology, 'Translations' and Boundary Objects (Soc Stud Sci 19:387-420)](https://doi.org/10.1177/030631289019003001) (Susan Leigh Star, James R. Griesemer; 1989) — Boundary-object theory anchor.

[50] [Choosing experiments to accelerate collective discovery (PNAS 112:14569-14574)](https://doi.org/10.1073/pnas.1509757112) (Andrey Rzhetsky, Jacob G. Foster, Ian T. Foster, James A. Evans; 2015) — Model: more risk-taking would speed discovery.

[51] [Sociological Innovation through Subfield Integration (Social Currents 1:228-256)](https://doi.org/10.1177/2329496514540131) (Erin Leahey, James Moody; 2014) — Subfield-integration measures incl. novelty of combinations (verified; plan flagged VERIFY).

[52] [Finding Cultural Holes: How Structure and Culture Diverge in Networks of Scholarly Communication (Sociological Science 1:221-238)](https://doi.org/10.15195/v1.a15) (Daril Vilhena, Jacob Foster, Martin Rosvall, Jevin West, James Evans, Carl Bergstrom; 2014) — Information-theoretic measure of jargon barriers between fields; nearest quantitative 'interpretive distance' measure, not linked to term adoption.

[53] [Mapping Change in Large Networks (PLoS ONE 5:e8694)](https://doi.org/10.1371/journal.pone.0008694) (Martin Rosvall, Carl T. Bergstrom; 2010) — Alluvial diagrams with significance for community change; descriptive.

[54] [Quantifying the rise and fall of scientific fields (PLoS ONE 17:e0270131)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0270131) (Chakresh Kumar Singh, Emma Barme, Robert Ward, Liubov Tupikina, Marc Santolini; 2022) — 72 arXiv fields: early phases interdisciplinary (2.36 vs 2.05 fields per article) with small teams (2 vs 4.5), late phases specialised; stage-averaged life-cycle analogue for C4.

> the early phase of a field is characterized by disruptive works mixing of cognitively distant fields written by small teams of interdisciplinary authors

Locator: Abstract

[55] [How new concepts become universal scientific approaches: insights from citation network analysis of agent-based complex systems science (Proc R Soc B 285:20172360)](https://api.crossref.org/works/10.1098/rspb.2017.2360) (Christian E. Vincenot; 2018) — ABM and IBM communities: disjoint, then progressive merger; single-case RQ2 sequence.

> confirmed their past disjointedness, and detected their progressive merger

Locator: Abstract

[56] [Scientific discovery and topological transitions in collaboration networks (J Informetr 3:210-221)](https://doi.org/10.1016/j.joi.2009.03.001) (L. M. A. Bettencourt, D. I. Kaiser, J. Kaur; 2009) — Field emergence accompanied by a topological transition in collaboration networks (title-level; Crossref-verified).

[57] [Structure in scientific networks: towards predictions of research dynamism (arXiv 1708.03850)](https://arxiv.org/abs/1708.03850) (Benjamin W. Stewart, Andy Rivas, Luat T. Vuong; 2017) — Citation-network structure vs growth/decline of three optics areas; case-level.

[58] [The role of propagule pressure in explaining species invasions (TREE 20:223-228)](https://doi.org/10.1016/j.tree.2005.02.004) (Julie L. Lockwood, Phillip Cassey, Tim Blackburn; 2005) — Propagule pressure analogy for C3 (repeated introduction vs establishment).

[59] [The more you introduce the more you get: the role of colonization pressure and propagule pressure in invasion ecology (Divers Distrib 15:904-910)](https://doi.org/10.1111/j.1472-4642.2009.00594.x) (Julie L. Lockwood, Phillip Cassey, Tim M. Blackburn; 2009) — Colonisation-pressure analogy for C3.

[60] [Hierarchical organization in complex networks (PRE 67:026112)](https://arxiv.org/pdf/cond-mat/0206130) (Erzsébet Ravasz, Albert-László Barabási; 2003) — C(k) ~ 1/k: local density falls with degree; basis of the degree-dependence threat to ego_density_W3 (design gap).

> indicating that the higher a node

Locator: Section on hierarchical model

[61] [Quantifying biodiversity: procedures and pitfalls in the measurement and comparison of species richness (Ecol Lett 4:379-391)](https://doi.org/10.1046/j.1461-0248.2001.00230.x) (Nicholas J. Gotelli, Robert K. Colwell; 2001) — Rarefaction justification for size-adjusted breadth.

[62] [Meta-analysis in clinical trials (Control Clin Trials 7:177-188)](https://doi.org/10.1016/0197-2456(86)90046-2) (Rebecca DerSimonian, Nan Laird; 1986) — Random-effects pooling used across held-out groups.

[63] [Quantifying heterogeneity in a meta-analysis (Stat Med 21:1539-1558)](https://doi.org/10.1002/sim.1186) (Julian P. T. Higgins, Simon G. Thompson; 2002) — I-squared interpretation for I2 0.75-0.78.

[64] [Estimating dynamic treatment effects in event studies with heterogeneous treatment effects (J Econometrics 225:175-199)](https://doi.org/10.1016/j.jeconom.2020.09.006) (Liyang Sun, Sarah Abraham; 2021) — Staggered event-study estimator for C4.

[65] [Difference-in-Differences with multiple time periods (J Econometrics 225:200-230)](https://doi.org/10.1016/j.jeconom.2020.12.001) (Brantly Callaway, Pedro H. C. Sant'Anna; 2021) — Group-time ATT estimator for C4.

[66] [Difference-in-differences with variation in treatment timing (J Econometrics 225:254-277)](https://doi.org/10.1016/j.jeconom.2021.03.014) (Andrew Goodman-Bacon; 2021) — TWFE decomposition; staggered-timing bias for C4.

[67] [Learning on knowledge graph dynamics provides an early warning of impactful research (Nat Biotechnol 39:1300-1307)](https://doi.org/10.1038/s41587-021-00907-6) (James W. Weis, Joseph M. Jacobson; 2021) — Paper-level impact forecasting from knowledge-graph dynamics; not comparable (paper unit, impact outcome).

[68] [FOS: A Large-Scale Temporal Graph Benchmark for Scientific Interdisciplinary Link Prediction (arXiv 2511.18631)](https://arxiv.org/abs/2511.18631) (Kiyan Rezaee, Morteza Ziabakhsh, Niloofar Nikfarjam, Mohammad M. Ghassemi; 2025) — Field-pair link-prediction benchmark (65,027 sub-fields); level metrics, not comparable.

[69] [Predicting research trends with semantic and neural networks with an application in quantum physics (PNAS 117:1910)](https://arxiv.org/pdf/1906.06843) (Mario Krenn, Anton Zeilinger; 2020) — Concept-pair link forecast AUC 0.85: a level AUC, not comparable (carried).

[70] [The research space: using career paths to predict the evolution of the research output of individuals, institutions, and nations (Scientometrics 109:1695)](https://arxiv.org/pdf/1602.08409) (Miguel R. Guevara, Dominik Hartmann, Manuel Aristarán, Marcelo Mendoza, César A. Hidalgo; 2016) — Entity field-entry AUC 0.8963 (carried); different unit.

[71] [The evolution of knowledge within and across fields in modern physics (Sci Rep 10:12097)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7374558/fullTextXML) (Ye Sun, Vito Latora; 2020) — Four field-pair knowledge-flow modes (carried); RQ2 comparator.

[72] [Quantifying the diaspora of knowledge in the last century (Applied Network Science 1:15)](https://doi.org/10.1007/s41109-016-0017-9) (Manlio De Domenico, Elisa Omodei, Alex Arenas; 2016) — ANS: field-level source/sink knowledge flows (carried, verified in iteration 2).

[73] [Community evolution in patent networks: technological change and network dynamics (Applied Network Science 3:26)](https://doi.org/10.1007/s41109-018-0090-3) (Yuan Gao, Zhen Zhu, Raja Kali, Massimo Riccaboni; 2018) — ANS: temporal community tracking in technology networks (carried).

[74] [Co-occurrence simplicial complexes in mathematics: identifying the holes of knowledge (Applied Network Science 3:37)](https://doi.org/10.1007/s41109-018-0074-3) (Vsevolod Salnikov, Daniele Cassese, Renaud Lambiotte, Nick S. Jones; 2018) — ANS: higher-order concept co-occurrence (carried).

[75] [The weakness of weak ties for novel information diffusion (Applied Network Science 2:14)](https://doi.org/10.1007/s41109-017-0034-3) (Jennifer M. Larson; 2017) — ANS: cross-group ties may impede novel diffusion; counter-mechanism to C1 (carried).

[76] [Author multidisciplinarity and disciplinary roles in field of study networks (Applied Network Science 7:78)](https://doi.org/10.1007/s41109-022-00517-4) (Eoghan Cunningham, Barry Smyth, Derek Greene; 2022) — ANS: field-of-study networks and bridging roles; closest data design (carried).

[77] [Mapping change in higher-order networks with multilevel and overlapping communities (Applied Network Science 8:42)](https://doi.org/10.1007/s41109-023-00572-5) (Anton Holmgren, Daniel Edler, Martin Rosvall; 2023) — ANS: descriptive alluvial change (carried).

[78] [Epistemic integration and social segregation of AI in neuroscience (Applied Network Science 9:8)](https://arxiv.org/abs/2310.01046) (Sylvain Fontaine, Floriana Gargiulo, Michel Dubois, Paola Tubaro; 2024) — ANS: one concept (AI) entering one field (carried).

[79] [Journal publications in medicine: ranking vs. interdisciplinarity (Applied Network Science 11:11)](https://doi.org/10.1007/s41109-025-00769-w) (Anbang Du, Michael Head, Markus Brede; 2025) — ANS: concept correlation networks in PubMed (carried).

[80] [Crossref REST API (reference verification)](https://api.crossref.org/works) — Used to verify 60 DOIs (66/67 identifiers resolved with the arXiv API) and to correct 3 plan-recalled DOIs (Chen 2012, Moser & Nicholas 2004, Feldman & Yoon 2012).

## Verification

Numbered citations resolve to unique listed sources. Passage checks test text occurrence, not claim truth or entailment. Author/year metadata and locators are not independently verified. Details: `research_verification.json`.

- Source [1]: text found — rate of co-usage with the focal term in year
- Source [1]: text found — A one standard deviation increase in ideational consistency of a new idea is associated with a 53 pe
- Source [1]: text found — a one standard deviation change in social embeddedness is associated with a 15 percent
- Source [1]: text found — We construct our dependent variable as the number of articles a new idea diffuses into the year ahea
- Source [1]: text found — we do not explore how an idea translates across domains or corpora
- Source [2]: text found — stratified 80/20 train
- Source [2]: text found — endogenous reinforcement proves largely unpredictable in the primary
- Source [2]: text found — exogenous count task achieves strong and consistent predictive power
- Source [4]: text found — The themes of this quadrant have low density and low centrality, mainly representing either emerging
- Source [6]: text found — Yet a structural inconsistency characterises dominant longitudinal implementations
- Source [8]: text found — steady fields have a density of up to twice the average value, whereas ephemeral fields always have 
- Source [8]: text found — the density grows when a new field is emerging, and decreases when the field starts to be neglected 
- Source [9]: text found — the pace of collaboration and the density measured in the sections of the network that will give ris
- Source [13]: text found — Centrality Divergence metric is potentially
- Source [16]: text found — usage in interdisciplinary venues
- Source [21]: text found — The strength of preferential attachment decreases over time
- Source [24]: text found — 29.39% and 62.37% higher for moderately and highly novel papers respectively
- Source [25]: text found — most commonly when scientists from one field publish problem-solving results to an audience from a d
- Source [28]: text found — taken up by other scholars at lower rates
- Source [29]: text found — we decompose scientific contributions into three functional types, foundations, extensions, and gene
- Source [30]: text found — the size of the contact neighborhood is in fact generally a negative predictor of contagion
- Source [30]: text found — probability of contagion is tightly controlled by the number of connected components
- Source [31]: text found — about seven times as precise as random guess
- Source [33]: text found — hashtags on politically controversial topics are particularly persistent
- Source [36]: text found — large groups persist longer if they are capable of dynamically altering their
- Source [36]: text found — The behaviour of small groups displays the opposite tendency
- Source [37]: text found — structural diversity is shown to be positively correlated with topic breadth
- Source [40]: text found — cited by subsequent patents that belong to a wide range of fields
- Source [46]: text found — rhetorical function is highly predictive of
- Source [47]: text found — share of methods papers doubled over the past four decades
- Source [54]: text found — the early phase of a field is characterized by disruptive works mixing of cognitively distant fields
- Source [55]: text found — confirmed their past disjointedness, and detected their progressive merger
- Source [60]: text found — indicating that the higher a node

## Follow-up Questions

- DESIGN GAP: does the ego_density_W3 effect (-0.102) survive a degree-preserving null z-score or within-degree-decile estimation, given that neighbourhood density falls roughly as 1/k (Ravasz & Barabasi 2003)?
- Direct test of Cheng et al. 2023: in our frame, does their weighted ideational-consistency measure predict next-period VOLUME positively but size-adjusted cross-field BREADTH negatively (a sign flip by outcome), and does the same hold for their word2vec ideational embeddedness?
- Does early consolidation predict persistence/survival (as Chavalarias & Cointet 2013 and Palla et al. 2007 suggest) while openness predicts reach, and does the edge-persistence effect depend on concept size as Palla's size x turnover interaction implies; separately, does the openness effect hold within method and within object concepts?

---
*Generated by AI Inventor Pipeline*
