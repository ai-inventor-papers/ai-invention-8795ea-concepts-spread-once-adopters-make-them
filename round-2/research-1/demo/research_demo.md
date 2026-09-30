# How our results compare with related papers

## Summary

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

## Research Findings

SCOPE AND CONFIDENCE. This is a web-only positioning study for an Applied Network Science (ANS) paper. The full tables are in research_report.md.

Our own comparator numbers are iteration-1 dev-panel placeholders from prior artifact art_33_KKk_G8Gw5; I re-read and confirmed them. They must be replaced by held-out values:
- gateway retention delta-AUC +0.103 (0.705 -> 0.808), 95% CI [0.034, 0.167], n = 80 episodes / 28 concepts, base rate 0.5625;
- +0.102 with field size controlled;
- relatedness-to-home adds -0.0003;
- next-field entry: relatedness-density AUC 0.614 [0.553, 0.666] vs log field size 0.742 [0.700, 0.784], n = 61 concept-steps.

Overall confidence:
- High for the verified bibliographic facts and the extracted numbers.
- Moderate for the novelty verdict. The searches were capped, and export-survival econometrics is a large literature.
- Low for anything about the target collection's contents.

(A) TARGET COLLECTION.
- The collection page could not be read by any route (WebFetch, skill fetch, browser-UA curl, Wayback). Search engines index only its landing page [1].
- Its scope text is: contributions of "theory, methods, and applications" for "health, mobility, education, politics, and related societal domains", published on a rolling basis [1].
- Guest editors, deadline and member articles could NOT be recovered, so no member list is given.
- No science-of-science paper was found to be confirmed in the collection.
- Fit argument: the societal relevance is research funding and foresight. The network representation is essential because the headline effect is a field's POSITION on a relatedness backbone. The methods overlap with ANS temporal-network, community-change and diffusion work [6, 11, 14].

(B) NEAREST RELATED WORK.
- ANS itself holds few science-of-science papers (OpenAlex sweep of source S3035517252 [2]). Still, 22 ANS papers are citable with a clear "how we relate" line. The core set:
  - Fontaine et al. 2024: AI entering neuroscience shows epistemic integration with social segregation. One concept in one off-home field; our panel generalises this [3].
  - De Domenico et al. 2016: disciplines as "sources" or "sinks" of research-interest flows [4].
  - Renoust et al. 2017, ANS 2:23 [5].
  - Holmgren et al. 2023, alluvial community change [6].
  - Gao et al. 2018, community evolution in patent networks [7].
  - Cunningham et al. 2022, disciplinary roles in field-of-study networks [8].
  - Du et al. 2025, concept networks in medicine [9].
  - Salnikov et al. 2018 [10].
  - Larson 2017, low-capacity weak ties impede diffusion [11].
  - Barnes et al. 2021, virality AUC 0.68 [12].
  - Temporal and community-aware centralities [13, 14].
  - Community-bounded knowledge flow [15], skill relatedness [16], position-dependent innovation adoption [17], and trait spreading across regions [18].
- Neighbour journals:
  - Relatedness canon [19-24, 27, 28, 60]. This includes Chinazzi et al. 2019 on the physics research space [29] and Li & Neffke's comparison of relatedness specifications [68].
  - Concept-pair forecasting [30-33, 57].
  - Topic-birth detection [39, 40, 70], including citation-network phase transitions in AI [58].
  - Flow-based maps of science [50].
  - Diffusion across disciplines [37, 38, 41, 42, 51-56, 69].

(C) COMPARISON NUMBERS PER RQ, each with a comparability note.

RQ2-H1 (retention).
- No published AUC for retention or exit of an adopted activity was found.
- Evidence for exit is regression-based and credits RELATEDNESS:
  - Neffke et al. 2011: technologically unrelated industries were more likely to exit 70 Swedish regions, 1969-2002 [22].
  - Rigby 2015 links exits of US cities from patent classes to relatedness [23].
  - Hidalgo et al. 2018 state the principle for both entry and exit [21].
  - Goya & Zahler 2019: new exports far from a firm's core competences survive less [24].
- Guevara et al. 2016 analyse entry only [19].
- So our +0.10 is an INCREMENT over a 0.71 baseline at a 0.56 base rate, with no direct published counterpart.
- The field's rival variable should be the relatedness DENSITY of the adopter's portfolio to the concept, not relatedness to the concept's home.

RQ2-H2 (next field).
- Guevara et al. report mean field-entry AUCs for the research space vs a citation map [19]:
  - individuals: 0.8963 vs 0.8034;
  - organisations: 0.7148 vs 0.6873;
  - countries: 0.6816 vs 0.6819.
- Our density AUC of 0.61 lies below their organisation and country levels, and in our data log field size (0.74) beats density. Guevara et al. report no size baseline, so this is a new and unfavourable-to-relatedness finding, not a failure.
- The units differ (a concept moving across fields vs an entity entering fields), so the comparison is indicative only.
- Report density's increment over size, as the relatedness literature does [21, 27].

RQ2 trajectories.
- Weng et al. 2013 predict viral memes from community concentration in the first 50 tweets. They are "about seven times as precise as random guess" and over 3x more precise than community-blind prediction [34]. This is the closest precedent for H3 (early breadth across communities).
- Cheng et al. 2023 follow about 60,000 new ideas across 38M papers. Ideas become core when they reach networks of unrelated authors and fit research traditions [37].
- Sun & Latora 2020 find absorbing, mutual and back-nurture field-pair regimes [38].
- Maillart et al. (2606.03919, preprint) reach exogenous-diffusion R2 up to 0.78 on a stratified random split (n = 6,978 pair-years) and R2_test 0.60-0.87 in three other domains. The authors state these are "within-domain replications, not train-on-one-field / test-on-another" [31]. So they do not contradict our negative cross-domain portability result.

RQ1 (indicators).
- Concept-pair link forecasts:
  - Maillart et al. (2606.03864, preprint): ROC-AUC 0.954-0.967 over four domains; RMSLE 0.45 to 0.6 at 1-5 years; driven by Adamic-Adar and degree features [30].
  - Krenn et al. 2023: positives are only about 1-3% of pairs [32].
  - Gu & Krenn 2025: temporal evaluation, AUC > 0.9 in most experiments [33].
- Topic-birth detection reports precision/recall against 1,408 debutant topics [40].
- These are LEVEL AUCs on growing co-occurrence graphs where degree and common-neighbour features separate rare positives. Our metrics are INCREMENTS over a strong popularity/size baseline, at a ~0.56 base rate, on held-out fields. They are not comparable, and a +0.10 increment is the harder claim.
- The dominance of degree features [30] and our size result both mean every indicator must beat the B5 baseline.

(D) NOVELTY.
- Q1 (metapopulation / rescue ideas for persistence): YES in cultural evolution.
  - Premo & Kuhn 2010 model "frequent extinctions of local subpopulations within a persistent metapopulation" [43].
  - Premo 2012 shows that network topology between groups shapes those effects [44].
  - Hopkinson 2011 applies metapopulation ecology to Palaeolithic skills [45].
  - Rescue and metapopulation theory: Brown & Kodric-Brown 1977; Hanski 1998 [46, 47].
  - In ANS, De Domenico et al. use source/sink language for disciplines [4].
  - No scientometric use of a rescue effect for field-level concept retention was found.
- Q2 (centrality beats relatedness for survival?): PARTIAL.
  - Position is known to matter for diversification. Countries in connected parts of the product space upgrade faster [20]. Country centralities explain diversification and growth [25]. Technology-network robustness conditions regional resilience [26].
  - But survival and exit are credited to relatedness [22-24].
  - No paper was found showing adopter centrality beating relatedness for the survival of an adopted activity.
- Q3 (gateway fields relay ideas onward?): PARTIAL.
  - Betweenness has been used as a journal-interdisciplinarity indicator [48, 49].
  - Community breadth predicts virality [34], and reach to unrelated authors predicts core status [37].
  - Field-of-study bridging roles exist in ANS [8].
  - No relay test was found.
- Grades:
  - position-based retention: NEW for concept adoption by fields, partially anticipated in general [20, 25];
  - relay: partially anticipated [34, 37, 48];
  - rescue-and-relay mechanism: partially anticipated [43-45];
  - leave-concept-out propensity control: new (no precedent found);
  - concept × field episode unit: partially anticipated. Single-concept AI studies exist [3, 52-54], and Cheng et al. use a global outcome [37].
- Framing: H1 should be presented as the first test for concept adoption by scientific fields, not as a new general principle.

(E) ANS TEMPLATE.
- The official guideline pages are IdP-blocked [66]. The template was inferred from 8 ANS articles from 2024-2026 read as Europe PMC XML [61-65].
- Abstract: unstructured, 165-297 words.
- Keywords: 0 in half the articles, otherwise 3-7. Guideline snippets say 3-10 [66].
- Body order: Introduction -> Methods -> Results -> Discussion/Conclusions. A separate "Related works" section appears in 1 of 8 [64].
- Back-matter order: optional Abbreviations [65]; Acknowledgements; Author contributions; Funding; Data availability (older articles: "Availability of data and materials"); Declarations; References.
- Declarations always contain Competing interests, e.g. "The authors declare no competing interests." [62]. 2 of 8 add ethics and consent statements [61, 62].
- Citations are author-year [63]. Body length 5,000-10,700 words, 1-12 figures, 13-60 references.
- Data-availability model sentence: code on GitHub under GPL-3.0 [61].
- APC £1240 / $1790 / €1490 (snippet, unverified) [66].
- Suggested skeleton: Introduction; Related work; Data and methods, with a Fig. 1 methodology overview; RQ1 (setup, results, comparison); RQ2 (setup, H1-H3, trajectories, comparison); Discussion; Conclusions; back matter as above.

(F) CORRECTIONS. All DOIs were checked against Crossref [67].
1. Complex contagion is Centola & Macy 2007 and Centola 2010 [35, 36], with Weng et al. 2013 for community virality [34]. It is not Salatino.
2. Relatedness is Hidalgo et al. 2007/2018, Neffke et al. 2011 and Guevara et al. 2016 [19-22]. It is not Rotolo et al. 2015, which is the emerging-technology definition paper [59].
3. arXiv 2606.03864 is by Maillart, Chataing, Antoni et al., the same team as 2606.03919 [30, 31].
4. Renoust et al. 2017 is ANS 2:23 [5].
5. "Knowledge transfer, knowledge gaps, and knowledge silos" is Cunningham & Greene, PLoS ONE 2025, not ANS [51].
6. Pinheiro et al. 2022 has DOI 10.1016/j.respol.2021.104323 [60].
7. Kiss et al. 2010 has DOI 10.1016/j.joi.2009.08.002 [42]; Bettencourt et al. 2006 has 10.1016/j.physa.2005.08.083 [69]. Yan et al. 2013 (10.1016/j.joi.2012.11.008) and Bettencourt et al. 2008 (10.1007/s11192-007-1888-4) were also corrected; see the report's reference table.
8. Bayesian online change-point detection is Adams & MacKay 2007 (arXiv 0710.3742).
9. Shi & Ma 2026 (SSRN 7276909) exists [57].

WHAT WOULD CHANGE THESE CONCLUSIONS.
- A paper, most plausibly in export-survival or regional-exit econometrics, showing that the adopter's network centrality predicts survival over relatedness density would downgrade H1 to "replication in a new domain".
- Recovering the collection's member list may add topic-matched ANS citations.


## Sources

[1] [Networks for everyday life (Applied Network Science collection)](https://link.springer.com/collections/fgcaicgjah) — Target collection. The page is JS/IdP-blocked for all fetch routes; the scope text came only from search-engine snippets (health, mobility, education, politics; rolling publication). Article list, guest editors and deadline could not be recovered.

[2] [OpenAlex API: Applied Network Science (source S3035517252)](https://api.openalex.org/works?filter=primary_location.source.id:S3035517252) — 15 anonymous title/abstract queries plus a 2025-26 listing (143 works) and 30 abstracts. This is the basis of the ANS related-work sweep.

[3] [Epistemic integration and social segregation of AI in neuroscience (ANS 9:8, 2024)](https://arxiv.org/abs/2310.01046) (Sylvain Fontaine, Floriana Gargiulo, Michel Dubois, Paola Tubaro; 2024) — Closest ANS comparator: AI entering neuroscience (MAG 1970-2019) shows epistemic integration with social segregation. One concept × one field.

[4] [Quantifying the diaspora of knowledge in the last century (ANS 1:15)](https://doi.org/10.1007/s41109-016-0017-9) (Manlio De Domenico, Elisa Omodei, Alex Arenas; 2016) — Disciplines act as sources or sinks of researchers' interest flows over a century. Source-sink vocabulary in ANS.

[5] [Multiplex flows in citation networks (ANS 2:23)](https://doi.org/10.1007/s41109-017-0035-2) (Benjamin Renoust, Vivek Claver, Jean-François Baffier; 2017) — Flow-based knowledge transmission in citation DAGs. Corrected citation (vol 2, art 23).

[6] [Mapping change in higher-order networks with multilevel and overlapping communities (ANS 8:42)](https://doi.org/10.1007/s41109-023-00572-5) (Anton Holmgren, Daniel Edler, Martin Rosvall; 2023) — Alluvial diagrams for community change, with a science case study. Relevant to community-transition indicators.

[7] [Community evolution in patent networks: technological change and network dynamics (ANS 3:26)](https://doi.org/10.1007/s41109-018-0090-3) (Yuan Gao, Zhen Zhu, Raja Kali, Massimo Riccaboni; 2018) — Temporal community tracking to identify central technologies.

[8] [Author multidisciplinarity and disciplinary roles in field of study networks (ANS 7:78)](https://doi.org/10.1007/s41109-022-00517-4) (Eoghan Cunningham, Barry Smyth, Derek Greene; 2022) — Field-of-study networks and the bridging roles of topics.

[9] [Journal publications in medicine: ranking vs. interdisciplinarity (ANS 11:11)](https://doi.org/10.1007/s41109-025-00769-w) (Anbang Du, Michael Head, Markus Brede; 2025) — Concept correlation networks in PubMed; cancer research bridges distant clusters.

[10] [Co-occurrence simplicial complexes in mathematics: identifying the holes of knowledge (ANS 3:37)](https://doi.org/10.1007/s41109-018-0074-3) (Vsevolod Salnikov, Daniele Cassese, Renaud Lambiotte, Nick S. Jones; 2018) — Higher-order concept co-occurrence representation.

[11] [The weakness of weak ties for novel information diffusion (ANS 2:14)](https://doi.org/10.1007/s41109-017-0034-3) (Jennifer M. Larson; 2017) — Lower-capacity cross-group ties impede diffusion. A mechanism for failed off-home adoption.

[12] [Dank or not? Analyzing and predicting the popularity of memes on Reddit (ANS 6:21)](https://doi.org/10.1007/s41109-021-00358-7) (2021) — Virality prediction from content reaches AUC = 0.68 on 129,326 memes.

[13] [Temporal walk based centrality metric for graph streams (ANS 3:32)](https://doi.org/10.1007/s41109-018-0080-5) (2018) — Predicting emerging centrality in temporal networks.

[14] [Map equation centrality: community-aware centrality based on the map equation (ANS 7:56)](https://doi.org/10.1007/s41109-022-00477-9) (Christopher Blöcker, Juan Carlos Nieves, Martin Rosvall; 2022) — A community-aware centrality; robustness alternative to eigenvector gateway centrality.

[15] [Community structure in co-inventor networks affects time to first citation for patents (ANS 4:17)](https://doi.org/10.1007/s41109-019-0126-3) (2019) — Knowledge flows faster within communities.

[16] [Global connections and the structure of skills in local co-worker networks (ANS 5:78)](https://doi.org/10.1007/s41109-020-00325-8) (2020) — Skill relatedness operationalised in ANS.

[17] [Modelling innovation adoption spreading in complex networks (ANS 10:10)](https://doi.org/10.1007/s41109-025-00698-8) (Jing-Lin Duanmu, Wei Koong Chai; 2025) — Node position shapes adoption probability (Markov-chain model).

[18] [Understanding the romanization spreading on historical interregional networks in Northern Tunisia (ANS 7:53)](https://doi.org/10.1007/s41109-022-00492-w) (2022) — Spreading of a cultural trait over a mesoscale regional network. ANS analogue for trait persistence.

[19] [The research space: using career paths to predict the evolution of the research output of individuals, institutions, and nations (Scientometrics 109:1695, 2016)](https://arxiv.org/pdf/1602.08409) (Miguel R. Guevara, Dominik Hartmann, Manuel Aristarán, Marcelo Mendoza, César A. Hidalgo; 2016) — Field-entry AUC, research space vs UCSD map: individuals 0.8963 vs 0.8034; organisations 0.7148 vs 0.6873; countries 0.6816 vs 0.6819. No exit analysis.

> For countries, however, both methods are equally accurate

Locator: Results, Fig. 3

[20] [The product space conditions the development of nations (Science 317:482, 2007)](https://arxiv.org/pdf/0708.2090) (C. A. Hidalgo, B. Klinger, A.-L. Barabási, R. Hausmann; 2007) — Core-periphery product space; countries in more connected parts upgrade faster. Position governs diversification speed.

> allowing nations located in more connected parts of the

Locator: Abstract

[21] [The Principle of Relatedness (Springer Proc. Complexity, ICCS 2018, pp. 451-457)](https://oec.world/pdf/Hidalgo2018_Chapter_ThePrincipleOfRelatedness.pdf) (2018) — Synthesis: relatedness governs both entry and exit of activities.

> describing the probability that a region enters (or exits) an economic activity as a

Locator: p. 452, Introduction

[22] [How Do Regions Diversify over Time? Industry Relatedness and the Development of New Growth Paths in Regions (Econ Geogr 87:237)](https://doi.org/10.1111/j.1944-8287.2011.01121.x) (Frank Neffke, Martin Henning, Ron Boschma; 2011) — 70 Swedish regions, 1969-2002: related industries are more likely to enter; unrelated ones are more likely to exit.

[23] [Technological Relatedness and Knowledge Space: Entry and Exit of US Cities from Patent Classes (Reg Stud 49:1922)](https://doi.org/10.1080/00343404.2013.854878) (David L. Rigby; 2015) — Entry and exit of cities from patent classes linked to local and non-local relatedness, 1975-2005.

[24] [Distance from core competences and new export survival: Evidence from multi-product exporters (World Econ 42:3253)](https://doi.org/10.1111/twec.12835) (Daniel Goya, Andrés Zahler; 2019) — Distance of a new export from the firm's basket lowers its survival (relatedness, not centrality).

[25] [Bringing links back: economic complexity as network centrality in the Product Space (J Phys Complexity 7:035002)](https://doi.org/10.1088/2632-072X/ae8211) (Taylan Yenilmez; 2026) — Country centralities in the product space explain diversification, income and growth. Partial anticipation of position-based claims.

[26] [Technology Network Structure Conditions the Economic Resilience of Regions (Econ Geogr 98:355)](https://doi.org/10.1080/00130095.2022.2035715) (Gergő Tóth, Zoltán Elekes, Adam Whittle, Changjun Lee, Dieter F. Kogler; 2022) — Robustness of a region's technology network conditions its resilience (269 metros).

[27] [From Research Spaces to Strategic Portfolio Design: Forecasting Country-Level Scholarly Diversification (Mathematics 14:1953)](https://doi.org/10.3390/math14111953) (2026) — Research-space stepping-stone models for entry and exit of 164 countries in subfields.

> We estimate reduced-form stepping-stone models for entry and exit

Locator: Abstract

[28] [Knowledge and social relatedness shape research portfolio diversification (Sci Rep 10:14232)](https://doi.org/10.1038/s41598-020-71009-7) (Giorgio Tripodi, Francesca Chiaromonte, Fabrizio Lillo; 2020) — Physicists' diversification depends on knowledge and social relatedness.

[29] [Mapping the physics research space: a machine learning approach (EPJ Data Sci 8:33)](https://doi.org/10.1140/epjds/s13688-019-0210-z) (Matteo Chinazzi, Bruno Gonçalves, Qian Zhang, Alessandro Vespignani; 2019) — Research-space knowledge density predicts the evolution of research capacity of >400 urban areas. Numeric metrics not retrieved.

[30] [Explainable Forecasting of Scientific Breakthroughs from Concept Network Dynamics (arXiv preprint)](https://arxiv.org/pdf/2606.03864) (Thomas Maillart, Thibaut Chataing, Ntorina Antoni, David Dosu, Paul Bagourd, Julian Jang-Jaccard, Alain Mermoud; 2026) — OpenAlex concept-pair link forecasting: ROC-AUC 0.954-0.967 over four domains; RMSLE 0.45 to 0.6 at 1-5 years; driven by Adamic-Adar and degree-Hadamard features.

> ROC–AUC in [0.954, 0.967] at all horizons without re-tuning

Locator: Abstract

[31] [Forecasting Conceptual Diffusion in Science: The Case of Quantum Computing (arXiv preprint)](https://arxiv.org/pdf/2606.03919) (Thomas Maillart, Thibaut Chataing, David Dosu, Paul Bagourd, Julian Jang-Jaccard, Alain Mermoud; 2026) — Exogenous diffusion R2 up to 0.78 (stratified random 80/20 split, n = 6,978 pair-years). Comparative R2_test 0.60-0.87 are within-domain temporal hold-outs, not cross-field transfer.

> Metrics are within-domain replications, not

Locator: Section 4, Comparative validation protocol

[32] [Forecasting the future of artificial intelligence with machine learning-based link prediction in an exponentially growing knowledge network (Nat Mach Intell 5:1326, 2023)](https://arxiv.org/pdf/2210.00881) (2023) — Science4Cast: 143,000 arXiv AI papers, 64,719 concepts, ~17.9M edges. New links are rare (about 1-3%); per-model AUCs appear only in figures.

> with only about 1-3% of newly connected

Locator: Section II.C

[33] [Forecasting high-impact research topics via machine learning on evolving knowledge graphs (Mach Learn Sci Technol 6:025041, 2025)](https://arxiv.org/pdf/2402.08640) (Xuemei Gu, Mario Krenn; 2025) — Temporal train 2016-2019 / evaluate 2019-2022; AUC beyond 0.9 in most experiments.

> AUC values beyond 0.9 for most experiments

Locator: Abstract

[34] [Virality Prediction and Community Structure in Social Networks (Sci Rep 3:2522, 2013)](https://arxiv.org/pdf/1306.0158) (Lilian Weng, Filippo Menczer, Yong-Yeol Ahn; 2013) — Early community concentration (first 50 tweets) predicts virality. About 7x the precision of random guessing and over 3x that of community-blind prediction.

> about seven times as precise as random guess

Locator: Results, prediction

[35] [Complex Contagions and the Weakness of Long Ties (AJS 113:702-734)](https://doi.org/10.1086/521848) (Damon Centola, Michael Macy; 2007) — Correct citation for complex contagion (theory).

[36] [The Spread of Behavior in an Online Social Network Experiment (Science 329:1194)](https://doi.org/10.1126/science.1185231) (Damon Centola; 2010) — Experimental evidence for complex contagion in clustered networks.

[37] [How New Ideas Diffuse in Science (ASR 88:522-561)](https://doi.org/10.1177/00031224231166955) (Mengjie Cheng, Daniel Scott Smith, Xiang Ren, Hancheng Cao, Sanne Smith, Daniel A. McFarland; 2023) — ~60,000 new ideas (1993-2016) followed across 38M papers. Ideas become core when they reach networks of unrelated authors, achieve consistent use and fit traditions.

[38] [The evolution of knowledge within and across fields in modern physics (Sci Rep 10:12097)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7374558/fullTextXML) (Ye Sun, Vito Latora; 2020) — APS 1985-2015: absorbing, mutual and back-nurture field-pair regimes.

> cases of evolution from absorbing to mutual or even to back-nurture behaviors

Locator: Abstract

[39] [How are topics born? Understanding the research dynamics preceding the emergence of new areas (PeerJ CS 3:e119)](https://peerj.com/articles/cs-119.pdf) (Angelo A. Salatino, Francesco Osborne, Enrico Motta; 2017) — Topic co-occurrence dynamics in the five years before debut, compared with a control group.

[40] [AUGUR: forecasting the emergence of new research topics (JCDL 2018, 303-312)](https://doi.org/10.1145/3197026.3197052) (Angelo A. Salatino, Francesco Osborne, Enrico Motta; 2018) — Gold standard of 1,408 debutant topics (2000-2011); beats four baselines on precision and recall.

[41] [Local emergence and global diffusion of research technologies (JASIST 62:846)](https://doi.org/10.1002/asi.21509) (Loet Leydesdorff, Ismael Rafols; 2011) — siRNA vs nanocrystalline solar cells: geographical and cognitive diffusion patterns.

[42] [Can epidemic models describe the diffusion of topics across disciplines? (J Informetr 4:74)](https://doi.org/10.1016/j.joi.2009.08.002) (Istvan Z. Kiss, Mark Broom, Paul G. Craze, Ismael Rafols; 2010) — Epidemic models of topic diffusion across disciplines. Corrected DOI.

[43] [Modeling Effects of Local Extinctions on Culture Change and Diversity in the Paleolithic (PLoS ONE 5:e15582)](https://doi.org/10.1371/journal.pone.0015582) (L. S. Premo, Steven L. Kuhn; 2010) — Metapopulation model for cultural persistence and diversity. Partially anticipates the rescue/metapopulation analogy.

> frequent extinctions of local subpopulations within a persistent metapopulation

Locator: Abstract

[44] [Local extinctions, connectedness, and cultural evolution in structured populations (Adv Complex Syst 15:1150002)](https://doi.org/10.1142/S0219525911003268) (L. S. Premo) — Intergroup transmission rate and network topology shape the effects of local extinction on cultural diversity.

[45] [The Transmission of Technological Skills in the Palaeolithic: Insights from Metapopulation Ecology](https://doi.org/10.1007/978-1-4419-6970-5_12) (2011) — Metapopulation ecology applied to the persistence of technological skills.

[46] [Turnover Rates in Insular Biogeography: Effect of Immigration on Extinction (Ecology 58:445)](https://doi.org/10.2307/1935620) (James H. Brown, Astrid Kodric-Brown; 1977) — Original rescue-effect reference.

[47] [Metapopulation dynamics (Nature 396:41)](https://doi.org/10.1038/23876) (Ilkka Hanski; 1998) — Ecology reference for metapopulation persistence.

[48] [Betweenness centrality as an indicator of the interdisciplinarity of scientific journals (JASIST 58:1303)](https://doi.org/10.1002/asi.20614) (Loet Leydesdorff; 2007) — Betweenness as an interdisciplinarity indicator. Structural, not a relay test.

[49] [Betweenness and diversity in journal citation networks as measures of interdisciplinarity (Scientometrics 114:567)](https://doi.org/10.1007/s11192-017-2528-2) (Loet Leydesdorff, Caroline S. Wagner, Lutz Bornmann) — Betweenness centrality is treated as multidisciplinarity and diversity as interdisciplinarity.

[50] [Maps of random walks on complex networks reveal community structure (PNAS 105:1118)](https://doi.org/10.1073/pnas.0706851105) (Martin Rosvall, Carl T. Bergstrom; 2008) — Flow-based maps of science (Infomap).

[51] [Knowledge transfer, knowledge gaps, and knowledge silos in citation networks (PLoS ONE 20:e0329302)](https://doi.org/10.1371/journal.pone.0329302) (Eoghan Cunningham, Derek Greene; 2025) — Dynamic citation communities in XAI. Corrected venue: PLoS ONE, not ANS.

[52] [Oil & Water? Diffusion of AI Within and Across Scientific Fields (arXiv)](https://arxiv.org/abs/2405.15828) (Eamon Duede, William Dolan, André Bauer, Ian Foster, Karim Lakhani; 2024) — About 80M papers in 20 fields, 1985-2022; AI engagement up about 13x; uneven adoption across fields.

[53] [Rise of Generative Artificial Intelligence in Science (Scientometrics 130:5093)](https://doi.org/10.1007/s11192-025-05413-z) (Liangping Ding, Cornelia Lawson, Philip Shapira; 2025) — OpenAlex-based GenAI adoption across fields, 2017-2023.

[54] [The diffusion of artificial intelligence methods in scientific research: growth pattern, disciplinary variation, and task alignment (J Informetr 20:101858)](https://doi.org/10.1016/j.joi.2026.101858) (Wen Lou, Tan Fu, Mingzhu Gao, Qianqian Xu; 2026) — Recent AI-method diffusion study; single-concept-family comparator.

[55] [Beyond borrowed concepts: a semantic analysis of entropy's half-century cross-disciplinary journey between physics and economics (Scientometrics)](https://doi.org/10.1007/s11192-025-05489-7) (Bea Treena Macasaet, Justin J W Powell; 2026) — Borrowed-concept case study; notes that sustained cross-disciplinary dialogue is rare.

[56] [Selective permeability in interdisciplinary knowledge organization: evidence from communication studies (Scientometrics 131:2927)](https://doi.org/10.1007/s11192-026-05611-3) (2026) — Hub-and-spoke boundary spanning by a field.

[57] [Tracing and Forecasting Frontier Trajectories in Evolving Knowledge Networks (SSRN preprint)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7276909) (Yixuan Shi, Yifang Ma; 2026) — Forecasts association trajectories of concept pairs rather than link existence. Existence verified.

[58] [Complexity and phase transitions in citation networks: insights from artificial intelligence research (Front Res Metr Anal 9)](https://doi.org/10.3389/frma.2024.1456978) (Ariadne de Andrade Costa, Rafael B. Frigori; 2024) — Entropy and citation-network phase transitions in AI; descriptive.

[59] [What is an emerging technology? (Res Policy 44:1827)](https://doi.org/10.1016/j.respol.2015.06.006) (Daniele Rotolo, Diana Hicks, Ben R. Martin; 2015) — Definitional baseline for emergence. Not a relatedness reference (correction).

[60] [The time and frequency of unrelated diversification (Res Policy 51:104323)](https://doi.org/10.1016/j.respol.2021.104323) (Flávio L. Pinheiro, Dominik Hartmann, Ron Boschma, César A. Hidalgo) — Unrelated jumps. DOI corrected to the 2021 prefix.

[61] [Tunable network properties with Hamill and Gilbert's Social Circles generator (ANS 2025): full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12714787/fullTextXML) (2025) — ANS template exemplar: GitHub/OSF data-availability wording and the Declarations subsections.

> The source code, primary and secondary data used in the model, and documentation can be found on Github under a GNU General Public License 3.0.

Locator: Data availability

[62] [Temporal dynamics of the friendship paradox in a smartphone communication network (ANS 10:16, 2025): full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12102006/fullTextXML) (Cheng Wang, Omar Lizardo, David S. Hachen; 2025) — ANS template exemplar: no keywords; Introduction...Discussion, Conclusions; Declarations with ethics, consent and competing interests.

> The authors declare no competing interests.

Locator: Declarations

[63] [Navigation on temporal networks (ANS 2025): full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11926000/fullTextXML) (2025) — ANS template exemplar: Introduction, Methods, Results, Conclusions; no keywords; author-year citations.

[64] [Initialisation and network effects in decentralised federated learning (ANS 2025): full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12575549/fullTextXML) (2025) — ANS template exemplar with a separate 'Related works' section.

[65] [Changes in patient-sharing patterns after oncologist departures (ANS 2026): full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12775101/fullTextXML) (2026) — ANS template exemplar with an Abbreviations section and keywords.

[66] [Applied Network Science submission guidelines (snippets only)](https://link.springer.com/journal/41109/submission-guidelines) — The page is IdP-blocked. Snippets: 3-10 keywords; 'Availability of data and materials' required; APC £1240/$1790/€1490 (unverified).

[67] [Crossref REST API](https://api.crossref.org/works) — Used to verify about 95 DOIs (author, year, title, venue) and to find the correct DOIs for wrongly attributed references.

[68] [Evaluating the principle of relatedness: Estimation, drivers and implications for policy (arXiv)](https://arxiv.org/pdf/2205.02942) (Yang Li, Frank Neffke; 2023) — Compares relatedness specifications across establishments, firms, cities and countries.

[69] [The power of a good idea: quantitative modeling of the spread of ideas from epidemiological models (Physica A 364:513)](https://doi.org/10.1016/j.physa.2005.08.083) (2006) — Epidemic models of idea spread. Corrected DOI.

[70] [CiteSpace II: Detecting and visualizing emerging trends and transient patterns in scientific literature (JASIST 57:359)](https://doi.org/10.1002/asi.20317) (Chaomei Chen) — Emerging-trend detection baseline.

## Verification

Numbered citations resolve to unique listed sources. Passage checks test text occurrence, not claim truth or entailment. Author/year metadata and locators are not independently verified. Details: `research_verification.json`.

- Source [19]: text found — For countries, however, both methods are equally accurate
- Source [20]: text found — allowing nations located in more connected parts of the
- Source [21]: text found — describing the probability that a region enters (or exits) an economic activity as a
- Source [27]: UNVERIFIED — We estimate reduced-form stepping-stone models for entry and exit
- Source [30]: text found — ROC–AUC in [0.954, 0.967] at all horizons without re-tuning
- Source [31]: text found — Metrics are within-domain replications, not
- Source [32]: text found — with only about 1-3% of newly connected
- Source [33]: text found — AUC values beyond 0.9 for most experiments
- Source [34]: text found — about seven times as precise as random guess
- Source [38]: text found — cases of evolution from absorbing to mutual or even to back-nurture behaviors
- Source [43]: text found — frequent extinctions of local subpopulations within a persistent metapopulation
- Source [61]: text found — The source code, primary and secondary data used in the model, and documentation can be found on Git
- Source [62]: text found — The authors declare no competing interests.

## Follow-up Questions

- RISK / stronger baseline: an economic-complexity reviewer will ask whether the adopter's gateway centrality still adds retention signal once the relatedness DENSITY of the adopter's own concept portfolio to the adopted concept (not relatedness to the concept's home field) is in the baseline. The experiment step should add this rival and also check eigenvector centrality against density and size collinearity. Is there an export-survival or regional-exit paper that already shows centrality beating density? None was found; the search was capped.
- Next-field entry: our relatedness-density AUC (0.61) is below Guevara et al.'s organisation and country levels (0.68-0.72), and field size (0.74) beats it. Should the held-out analysis report density's increment over size in a conditional logit, stratified by field size, so the comparison with Guevara et al. is like-for-like?
- Collection fit: the 'Networks for everyday life' article list, guest editors and deadline remain unknown (Springer IdP/JS block). Can a logged-in browser or the editorial office confirm the members, and whether any science-of-science paper is in the collection to cite? Until then, fit rests on societal relevance and method overlap only.

---
*Generated by AI Inventor Pipeline*
