# Is 'fields that keep it' new? Prior art and venue check

## Summary

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

## Research Findings

EXECUTIVE SUMMARY. Web-only positioning study for the Applied Network Science (ANS) paper, iteration 3. Full tables are in research_report.md. The iteration-2 report (internal artifact art_dxvRpQufMR0e) is reused by citation.

OUR COMPARATOR NUMBERS
Source: this run's internal Exp6 held-out results (artifact art_N-mpomDZZ1ln; not a web source). They are to be replaced by iteration-3 values.
- Design: conditional logit, 369 concepts, 1,373 entry events, 961 informative strata.
- Retained-field relatedness d0_ret_rel: +0.281 per SD (SE 0.032).
- M1 vs M0: LR 68.6.
- DL pooled over 4 held-out groups: 0.28 [0.22, 0.35], I² = 0.
- Permutation p 0.001; rewired-backbone p 0.015.
- Within-stratum AUC: 0.809 → 0.817.
- Abandonment term d_lost: −0.063 (SE 0.035, p 0.055; stand-alone AUC 0.495).

(1) CLAIM A: RETAINED FRONTIER. Verdict: PARTIALLY ANTICIPATED (weak partial).
The relatedness literature uses persistence routinely, but only as a filter on the OUTCOME (what counts as an entry):
- Pinheiro et al. 2022 require RCA<1 for Δ years before and RCA≥1 for Δ years after an entry, with "a standard Δ = 4" [1]. The working paper used "four consecutive years" [2].
- Albora et al. 2023 count an activation only if "the RCA values were below a non-significance threshold t=0.25 in all the previous years" [3].
- Bahar et al. 2014 use tenfold "jumps" from RCA≤0.1 [4].

On the PREDICTOR side, every density found is a current snapshot:
- Hidalgo et al. 2007 use "xi = 1 if RCAi>1 and 0 otherwise" [5];
- Hausmann & Klinger 2007 vary only the presence threshold (RCA vs dollar value) [6];
- Pinheiro's basket is products "with an RCA greater one" in year y [1];
- Miao et al. apply RCA>1 to country × discipline [11];
- Li & Neffke compare binary and continuous prevalence across 32,480 specifications [9];
- Jun et al. relate current exports to future trade volume [10], and O'Clery et al. model presence and appearance [22];
- the neighbour-signal papers use neighbours' current RCA [4] or current export growth [12].
- Chinazzi et al. [19] and Aleta et al. [20] (physics research space) could not be read beyond the abstract: Springer login wall.

Nearest predictor-side designs:
- Galuppo Azevedo et al. compute densities "over a time window [t − ΔRCA, t]" [44]. This is a window aggregate, not a retained/lost split.
- In science, Cheng et al. find that ideas become core when they "achieve consistent intellectual usage" [23]. That outcome is global, not a per-field entry model, and their method section was paywalled.

No paper was found, in 6 strands searched, that builds density from retained or persistent presences only, or weights presences by duration, and tests it against RCA>1 density. The strands were:
- economic complexity;
- relatedness in science [11, 44];
- export learning [4, 12, 14];
- regional exit [7, 8];
- invasion biology [16-18, 21];
- idea diffusion [23].

Suggested framing: "to our knowledge, persistence has so far been used only to filter entry events; we move it to the predictor side." Confidence: moderate.

(2) CLAIM B: ABANDONMENT PENALTY. Verdict: PARTIALLY ANTICIPATED in mechanism; NEW as a test.
Mechanism precedents:
- Fernandes & Tang's learning model says more neighbours raise entry when the signal is positive, "whereas it will deter entry when the signal is negative" [12]. Empirically, entry rises with neighbours' export growth: mean growth "is associated with a 0.1 percentage-point increase in the probability of entry" [12]. That is a continuous performance signal for firms, not exits.
- Nomaler & Verspagen argue "absence or loss of comparative advantage should be considered as a useful source of information". They build anti-relatedness from co-absence, but in pooled data the new measures "do not add much" [13].
- Hausmann & Rodrik stress discovery externalities from successes [15].
- Hazir et al. relate French firms' adding and dropping of exported products to local product-space density, without neighbour exits as predictors [25].
- Ecology defines casual aliens as those that "rely on repeated introductions for their persistence" [16]. It explains establishment failure by propagule pressure [18] within a stage/barrier framework [17], not as a signal to similar sites.

Not found anywhere: neighbours' EXITS or lost presences entering an ENTRY model as a predictor. Exits are modelled only as a unit's own outcome [7, 8, 11, 26].

Our own (internal Exp6) evidence is fragile (p 0.055). Report it as a secondary, weak/null result consistent with negative-signal learning.

(3) RIVALS REVIEWERS WILL DEMAND
Checked against the M0..M4 ladder: D_rca, D_vol, ever-entered density, size, home relatedness, centrality.
- R1 (MISSING): persistence-filtered RCA density, D_rca_persist_k (entered or RCA>1 in each of t−k..t), the predictor-side twin of Pinheiro's Δ-rule [1]. This decides whether Claim A is new or just noise filtering.
- R2 (covered if D_vol is continuous prevalence): Li & Neffke [9].
- R3 (probably MISSING): own pre-entry sub-threshold intensity and trend, i.e. Albora's auto-correlation benchmark [3] and Galuppo Azevedo's "nascent" state [44]. Add an Albora-style activation-only risk set as a robustness check.
- R4 (MISSING): neighbour-momentum density, the relatedness-weighted recent usage growth in adopting fields [12]. This is the main confound for both claims.
- R5 (partly covered): Wald test of β_ret = β_lost inside D_ever, plus a co-absence control [13].
- R6 (planned): tenure dose-response (residence time) [21].

(4) RQ1 COMPARISON
No comparator evaluates on held-out fields.
- Small et al. nominate "71 emerging topics from 2007 to 2010" and report that "External evidence (e.g., awards) correlates well" [29].
- Porter et al.'s growth-based emergence score gives illustrative results. Use it as a baseline indicator, not a comparator number [30].
- Rotolo et al. is definitional [31]; Wang is demonstration-based [32]; Xu et al. report 8/10 contest hits [34].
- Liang et al.'s numbers are not accessible [35]. Behrouzi et al. report no numbers in the abstract [33].
- Link-forecast AUCs are LEVEL AUCs on rare positives. Krenn & Zeilinger report "AUC2017=0.85" with "roughly 5% of all edges" drawn [36]; Maillart et al. report "ROC–AUC in [0.954, 0.967]" on four domains [27].
- Palmucci et al.'s AUC and F1 values appear only in a figure [42].
- Kleinberg bursts [40] and CiteSpace [41] are baselines without held-out numbers.
- An OpenAlex sweep of ANS itself found no science-of-science emergence-forecasting comparator [28].
Our RQ1 result is an increment over the B5 count baseline (ρ_B5 0.77-0.83, iteration 1) on held-out field groups. It has no like-for-like counterpart and should be presented as such.

(5) RQ2 COMPARISON
Prior work:
- Sun & Latora classify field-pair regimes into four modes: "absorbing, absorbing to mutual, back-nurture and mutual mode" [37].
- De Domenico et al. define sink and source indices of areas [39].
- Sun et al. model discipline birth through community splitting and merging [46].
- Duede et al. track AI ubiquity across 20 fields [43].
- Mao et al. follow meme cascades across 5 disciplines [50].
- Leydesdorff & Rafols compare two technologies [48].
- Fontaine et al. study one concept (AI) in one host field [45].
- Topic life cycles have been fitted with logistic/Gompertz curves [49], and individual research-interest change follows an exponential distribution [55]; neither tracks per-field retention.
- Cheng et al. link core status to reaching unrelated authors plus consistent usage [23].

Nobody was found decomposing breadth into contact rate × retention probability, or tracking per-field entered/retained/lost states. Verdict: NEW (moderate confidence).

Entity-level field-entry AUCs are 0.879 for scientists, 0.856 for institutions and 0.631 for states [44]; Guevara et al. report an average AUC of 0.8963 for individuals [24]. These are only partly comparable to our internal within-stratum 0.809→0.817.

(6) VENUE
- The collection page, the collections list, Europe PMC, the Crossref ISSN filter and the Wayback CDX all failed [47, 53, 54, 57].
- Search-engine snippets (2026-09-28) give: submissions open 24 June 2026, deadline 30 November 2026, and scope items "Information diffusion and communication networks in digital societies" and "Innovation, collaboration, and knowledge exchange networks across sectors" [47].
- The editor list and member articles are unrecoverable. A snippet names Ronaldo Menezes, but his role is unverified.

(7) ANS STRUCTURE
Three science-of-science ANS articles were read. Cunningham 2022 is the published version [52]; Fontaine 2024 [45] and Holmgren 2023 [38] are arXiv versions.
- Section orders:
  - Cunningham: Introduction / Related work / Methods / Case studies / Conclusions.
  - Fontaine: Introduction / Literature review / Data and methods / Results / Discussion / Declarations.
  - Holmgren: Introduction / Methods / Results / Conclusions.
- Abstracts are unstructured, about 120-260 words.
- Figures: 7-13; tables: 0-4; references: 29-40.
- Explicit RQs appear in none of the three.
- A fourth sci-sci ANS article, Du et al. 2025, could not be read in full (Springer bot challenge) [56].
- Methodology figures are schematic multi-panel diagrams (a, b; a-e) without data counts.

Recommended skeleton:
1. Introduction with RQ1/RQ2.
2. Related work.
3. Data and methods, with a Fig. 1 5-lane pipeline carrying this run's counts.
4. RQ1: setup / results / comparison.
5. RQ2: setup / results / comparison.
6. Discussion.
7. Conclusions.
8. Back matter: Acknowledgements; Author contributions; Funding; Availability of data and materials; Declarations; References.

(8) REFERENCES
- 50 new references were verified through Crossref [51] and the arXiv API.
- Pinheiro 2022 and arXiv 1801.05352 are different versions of the work [1, 2].
- Two guessed DOIs (Albornoz 2012; Coniglio 2021) returned 404. They are UNVERIFIED and must not be cited.
- The Nomaler & Verspagen journal DOI guess was wrong, so cite the arXiv version [13].

CONFIDENCE AND WHAT WOULD CHANGE IT
- High for the extracted quotes and definitions.
- Moderate for the novelty verdicts.
- These would move to ANTICIPATED on finding any regional-exit or export-survival paper that uses duration- or stability-weighted density, or neighbours' exits, as ENTRY predictors. Boschma et al. 2015 ("rise and fall") and Coniglio et al. 2021 are the first to read.
- They would also move on learning that Cheng et al. measure consistent usage per field and use it to predict spread into new fields [23].


## Sources

[1] [The time and frequency of unrelated diversification (Research Policy 51:104323; open-access copy)](https://run.unl.pt/bitstreams/e0c3b563-f946-4b3a-9a9b-5c2583cfd12a/download) (Flávio L. Pinheiro, Dominik Hartmann, Ron Boschma, César A. Hidalgo; 2022) — Entry events are defined with a persistence filter on the OUTCOME (Δ=4 years backward RCA<1 and forward RCA≥1); density uses the current RCA≥1 basket. Closest anticipation of Claim A's 'retained' idea.

> In the main manuscript we will consider a standard Δ = 4

Locator: Methods, Identifying new products

> These conditions help reduce the number of false-positive observations. We only consider entry events as those events that satisfy these conditions.

Locator: Methods, Identifying new products

> We call the set of products present in a country with an RCA greater one

Locator: Methods

[2] [Shooting High or Low: Do Countries Benefit from Entering Unrelated Activities? (working-paper precursor)](https://arxiv.org/pdf/1801.05352) (Flávio L. Pinheiro, Aamena Alshamsi, Dominik Hartmann, Ron Boschma, César A. Hidalgo; 2018) — Earlier version with the 'four consecutive years' backward/forward entry conditions; different title and author list from the Research Policy paper.

> we consider a backward condition that requires that a country c had an RCA lower than 1.0 over product p for four consecutive years before y

Locator: p. 11-12, Identifying New Products

[3] [Product progression: a machine learning approach to forecasting industrial upgrading (Sci Rep 13:1481)](https://www.nature.com/articles/s41598-023-28179-x) (Giambattista Albora, Luciano Pietronero, Andrea Tacchella, Andrea Zaccaria; 2023) — Activation = new RCA>1 element with RCA<0.25 in all previous years; RCA auto-correlation benchmark; tree models beat it. Persistence used on the outcome/eligibility, not as a relatedness predictor.

> requiring that the RCA values were below a non-significance threshold t=0.25 in all the previous years

Locator: Results, data description

> which simply uses the RCA values in 2013 to predict the export matrix in 2018

Locator: Results, Fig. 3 discussion

> tree-based algorithms clearly outperform both the quite strong auto-correlation benchmark and the other supervised algorithms

Locator: Abstract

[4] [Neighbors and the evolution of the comparative advantage of nations (J Int Econ 92:111-123)](https://scholar.harvard.edu/files/dbaharc/files/bhh-jie.pdf) (Dany Bahar, Ricardo Hausmann, César A. Hidalgo; 2014) — Neighbour's CURRENT comparative advantage raises the probability of adding a product by 65%; neighbours' loss of RCA is not modelled.

> countries are 65% more likely to start exporting a product which was being exported with comparative advantage by one of its geographic neighbors at the beginning of the period

Locator: Introduction

> from RCAcp ≤0.1 to RCAcp ≥0.1 within a ten year period

Locator: Section 3 (jump definition)

[5] [The Product Space Conditions the Development of Nations (Science 317:482)](https://arxiv.org/pdf/0708.2090) (C. A. Hidalgo, B. Klinger, A.-L. Barabási, R. Hausmann; 2007) — Density built from current RCA>1 presences; no persistence rule found.

> xi = 1 if RCAi>1 and 0 otherwise

Locator: density definition, p. 5

[6] [The Structure of the Product Space and the Evolution of Comparative Advantage (CID WP 146)](https://www.hks.harvard.edu/sites/default/files/centers/cid/files/publications/faculty-working-papers/146.pdf) (Ricardo Hausmann, Bailey Klinger; 2007) — Future presence regressed on density conditional on current state; robustness with dollar-value presence thresholds; no persistence-based predictor.

> We also check whether changing the criteria for the dummy variable x from RCA>1 to a threshold dollar value of exports.

Locator: Section 4 robustness, p. 28

[7] [How Do Regions Diversify over Time? (Econ Geogr 87:237; PEEG 09.16)](http://econ.geo.uu.nl/peeg/peeg0916.pdf) (Frank Neffke, Martin Henning, Ron Boschma; 2011) — Entry and exit of industries in 70 Swedish regions both modelled as outcomes of relatedness; neighbours' exits not a predictor.

> And unrelated industries had a higher probability to exit the region.

Locator: Abstract

[8] [Technological Relatedness and Knowledge Space: Entry and Exit of US Cities from Patent Classes (Reg Stud 49:1922)](https://econpapers.repec.org/article/tafregstd/v_3a49_3ay_3a2015_3ai_3a11_3ap_3a1922-1937.htm) (David L. Rigby; 2015) — Entry and exit of cities from patent classes linked to relatedness (abstract only; full text 403).

> Entries and exits of cities from patent classes are linked to local and non-local measures of

Locator: Abstract

[9] [Evaluating the principle of relatedness: Estimation, drivers and implications for policy](https://arxiv.org/pdf/2205.02942) (Yang Li, Frank Neffke; 2022) — Compares 32,480 relatedness/density specifications including binary vs continuous prevalence; the rival family for D_rca vs D_vol.

> we distinguish between approaches that use continuous prevalence information and those that binarize prevalence information

Locator: Section 3.1

[10] [Bilateral relatedness: knowledge diffusion and the evolution of bilateral trade (J Evol Econ 30:247)](https://oec.world/pdf/bilateral-relatedness-knowledge-diffusion-and-the-evolution-of-bilateral-trade.pdf) (Bogang Jun, Aamena Alshamsi, Jian Gao, César A. Hidalgo; 2020) — Continuous trade-volume outcome; relatedness from current exports; no exit modelling.

> represents the volume of trade (in US dollar) of product p from exporter o to destination d in year t + 2

Locator: Eq. 4

[11] [The latent structure of global scientific development](https://arxiv.org/pdf/2104.10812) (Lili Miao, Dakota Murray, Woo-Sung Jung, Vincent Larivière, Cassidy R. Sugimoto, Yong-Yeol Ahn; 2021) — Country × discipline RCA; entry and exit of advantages both follow relatedness; exits not used as predictors.

> By examining the entry (exit) of advantages across each subsequent time step

Locator: Results, The principle of relatedness

[12] [Learning to Export from Neighbors (Dallas Fed WP 185; J Int Econ 94:67)](https://www.dallasfed.org/-/media/documents/institute/wpapers/2014/0185.pdf) (Ana Fernandes, Heiwai Tang; 2014) — Social-learning model: neighbours' negative signals deter entry; empirically entry rises with neighbours' export growth. Closest mechanism anticipation of Claim B (continuous signal, firms, not exits).

> whereas it will deter entry when the signal is negative

Locator: Introduction

> is associated with a 0.1 percentage-point increase in the probability of entry into the market

Locator: Section 5.1

[13] [Some New Views on Product Space and Related Diversification](https://arxiv.org/pdf/2203.16316) (Önder Nomaler, Bart Verspagen; 2022) — Argues absence/loss of comparative advantage carries information; anti-relatedness indicators from co-absence predict gains and losses but add little in pooled samples.

> The first is that absence or loss of comparative advantage should be considered as a useful source of information.

Locator: Section 3.6

> all measures that we analyzed performed extremely well, and hence the theoretical proposals do not add much to an already high predictive power

Locator: Section 3.6

[14] [Follow thy neighbor: The role of first exporters (J Urban Econ 150:103813)](https://ideas.repec.org/a/eee/juecon/v150y2025ics0094119025000786.html) (Hao Fe, Yang Liang, Mary E. Lovely; 2025) — First-exporter spillovers on neighbours' entry (abstract/snippet only; 38% higher entry probability).

[15] [Economic Development as Self-Discovery (NBER w8952; J Dev Econ 72:603)](https://www.nber.org/system/files/working_papers/w8952/w8952.pdf) (Ricardo Hausmann, Dani Rodrik; 2003) — Discovery externalities: learning what can be produced orients other entrepreneurs; about imitating successes.

> because this knowledge can orient the investments of other entrepreneurs

Locator: Introduction

[16] [Naturalization and invasion of alien plants: concepts and definitions (Divers Distrib 6:93)](https://www.ibot.cas.cz/personal/pysek/pdf/naturalization_and_invasion_%20of_alien_plants.pdf) (D. M. Richardson, P. Pyšek, M. Rejmánek, M. G. Barbour, F. D. Panetta, C. J. West; 2000) — Casual vs naturalized stages: the ecological analogue of entered-but-lost vs retained.

> rely on repeated introductions for their persistence

Locator: Table 1, 'Casual alien plants'

[17] [A proposed unified framework for biological invasions (TREE 26:333)](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1016/j.tree.2011.03.023%22&format=json&resultType=core) (2011) — Stage/barrier framework for invasions (abstract).

> provides a terminology and categorisation for populations at different points in the invasion process

Locator: Abstract

[18] [The role of propagule pressure in explaining species invasions (TREE 20:223)](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%2210.1016/j.tree.2005.02.004%22&format=json&resultType=core) (2005) — Establishment failure explained by propagule pressure, not framed as a signal for similar sites (abstract level).

> we propose propagule pressure as a key element to understanding why some introduced populations fail to establish whereas others succeed

Locator: Abstract

[19] [Mapping the physics research space: a machine learning approach (EPJ Data Sci 8:33)](https://doi.org/10.1140/epjds/s13688-019-0210-z) (Matteo Chinazzi, Bruno Gonçalves, Qian Zhang, Alessandro Vespignani; 2019) — Knowledge density for >400 urban areas; full text not reachable (Springer IdP); DOI verified.

[20] [Explore with caution: mapping the evolution of scientific interest in physics (EPJ Data Sci 8:27)](https://doi.org/10.1140/epjds/s13688-019-0205-9) (Alberto Aleta, Sandro Meloni, Nicola Perra, Yamir Moreno; 2019) — Author × PACS exploration; full text not reachable; DOI verified.

[21] [Residence time determines the distribution of alien plants](https://link.springer.com/chapter/10.1007/3-7643-7380-6_5) (P. Pyšek, V. Jarošík; 2005) — Residence-time analogue for the tenure dose test; title-level only.

[22] [Productive Ecosystems and the arrow of development (Nat Commun 12:1479)](https://www.nature.com/articles/s41467-021-21689-0) (Neave O'Clery, Muhammed Ali Yildirim, Ricardo Hausmann; 2021) — Presence/appearance-based capability model; no exit predictor.

> We use the presence and appearance of industries in countries (phenotypes) to infer capability

Locator: Introduction

[23] [How New Ideas Diffuse in Science (ASR 88:522)](https://journals.sagepub.com/doi/10.1177/00031224231166955) (Mengjie Cheng, Daniel Scott Smith, Xiang Ren, Hancheng Cao, Sanne Smith, Daniel A. McFarland; 2023) — ≈60,000 new ideas; reaching unrelated authors and consistent usage predict becoming core. Closest science analogue of retention; method paywalled.

> achieve consistent intellectual usage

Locator: Abstract

> New ideas become core concepts of science when they reach expansive networks of unrelated authors

Locator: Abstract

[24] [The research space: using career paths to predict the evolution of the research output of individuals, institutions, and nations (Scientometrics 109:1695)](https://arxiv.org/pdf/1602.08409) (Miguel R. Guevara, Dominik Hartmann, Manuel Aristarán, Marcelo Mendoza, César A. Hidalgo; 2016) — Field-entry AUC for individuals, organisations and countries; entry only, no exit or persistence rule.

> The average area under the ROC curve for individuals (Figure 3 a) is 0.8963 for the research space and 0.8034 for the UCSD science map.

Locator: Results, Figure 3

[25] [Local Product Space and Firm Level Churning in Exported Products (AFSE 2017)](https://afse2017.sciencesconf.org/142849/HAZIR_BELLONE_GAGLIO.pdf) (Hazir, Bellone, Gaglio) — Firm product adding/dropping vs local product-space density.

[26] [The Principle of Relatedness (ICCS 2018)](https://oec.world/pdf/Hidalgo2018_Chapter_ThePrincipleOfRelatedness.pdf) (2018) — Principle stated for both entry and exit.

> describing the probability that a region enters (or exits) an economic activity as a function of the number of related activities present in that location

Locator: Section 1

[27] [Concept-pair link forecasting across technology and biomedical domains (Maillart et al., arXiv 2606.03864)](https://arxiv.org/pdf/2606.03864) (2026) — Link-existence ROC-AUC 0.954-0.967 across four domains: level AUCs, not comparable with increments.

> ROC–AUC in [0.954, 0.967] at all horizons without re-tuning

Locator: Abstract/Introduction

[28] [OpenAlex sweep of Applied Network Science for emergence/link-prediction papers](https://api.openalex.org/works?filter=primary_location.source.id:S3035517252,title_and_abstract.search:emerging%20OR%20emergence%20OR%20%22link%20prediction%22) — 89 hits; none is a science-of-science emergence-forecasting comparator.

[29] [Identifying emerging topics in science and technology (Res Policy 43:1450)](https://www.sciencedirect.com/science/article/abs/pii/S0048733314000298) (Henry Small, Kevin W. Boyack, Richard Klavans; 2014) — 71 emerging topics; validated by external evidence, no held-out metric.

> 71 emerging topics from 2007 to 2010 are identified and characterized

Locator: Highlights

> External evidence (e.g., awards) correlates well with emerging topics

Locator: Highlights

[30] [Emergence scoring to identify frontier R&D topics and key players (TFSC 146:628)](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.techfore.2018.04.016?fields=title,year,authors,venue,abstract,externalIds) (A. Porter, Jon Garner, S. Carley, Nils C. Newman; 2019) — Growth-based emergence score; illustrative results only; use as baseline indicator.

[31] [What is an emerging technology? (Res Policy 44:1827)](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.respol.2015.06.006?fields=title,year,authors,venue,abstract,externalIds) (D. Rotolo, D. Hicks, Ben Martin; 2015) — Five attributes of emergence; definitional, no numbers.

[32] [A bibliometric model for identifying emerging research topics (JASIST 69:290)](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1002/asi.23930?fields=title,year,authors,venue,abstract,externalIds) (Qi Wang; 2018) — Criteria-based identification; evaluation by demonstration.

[33] [Predicting scientific research trends based on link prediction in keyword networks (J Informetr 14:101079)](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.joi.2020.101079?fields=title,year,authors,venue,abstract,externalIds) (Saman Behrouzi, Zahra Shafaeipour Sarmoor, K. Hajsadeghi, K. Kavousi; 2020) — Keyword link prediction; numbers not in abstract.

[34] [A topic models based framework for detecting and forecasting emerging technologies (TFSC 162:120366)](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.techfore.2020.120366?fields=title,year,authors,venue,abstract,externalIds) (Shuo Xu, Liyuan Hao, Guancan Yang, Kun Lu, Xin An; 2021) — Contest-based validation: 8 of 10 submitted technologies met organiser criteria.

[35] [Combining deep neural network and bibliometric indicator for emerging research topic prediction (IP&M 58:102611)](https://api.crossref.org/works/10.1016/j.ipm.2021.102611) (2021) — DOI verified; numbers not accessible.

[36] [Predicting research trends with semantic and neural networks with an application in quantum physics (PNAS 117:1910)](https://arxiv.org/pdf/1906.06843) (Mario Krenn, Anton Zeilinger; 2020) — Concept-pair 5-year link forecast, AUC 0.85 with ~5% of edges drawn: a LEVEL AUC.

> AUC2017=0.85

Locator: Fig. 5 label

> roughly 5% of all edges have been drawn by the end of 2017

Locator: Results

[37] [The evolution of knowledge within and across fields in modern physics (Sci Rep 10:12097)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7374558/fullTextXML) (Ye Sun, Vito Latora; 2020) — Four field-pair knowledge-flow modes (empirical classification).

> absorbing, absorbing to mutual, back-nurture and mutual mode

Locator: Results, knowledge-flow modes

[38] [Mapping change in higher-order networks with multilevel and overlapping communities (ANS 8:42)](https://arxiv.org/pdf/2303.00622) (Anton Holmgren, Daniel Edler, Martin Rosvall; 2023) — ANS template: Introduction/Methods/Results/Conclusions; Fig. 1 multi-panel schematic.

[39] [Quantifying the diaspora of knowledge in the last century (ANS 1:15)](https://arxiv.org/pdf/1604.00696) (Manlio De Domenico, Elisa Omodei, Alex Arenas; 2016) — Source and sink indices of research areas.

[40] [Bursty and Hierarchical Structure in Streams (DMKD 7:373)](https://api.crossref.org/works/10.1023/A:1024940629314) (Jon Kleinberg; 2003) — Burst detection baseline.

[41] [CiteSpace II: Detecting and visualizing emerging trends and transient patterns in scientific literature (JASIST 57:359)](https://api.crossref.org/works/10.1002/asi.20317) (Chaomei Chen; 2006) — Emerging-trend baseline tool.

[42] [Where is your field going? A machine learning approach to study the relative motion of the domains of physics (PLoS ONE 15:e0233997)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7302634/fullTextXML) (Andrea Palmucci, Hao Liao, Andrea Napoletano, Andrea Zaccaria; 2020) — PACS-pair forecasting with ROC-AUC and best F1; values in figure only.

> We evaluate the effectiveness of context similarity to forecast unseen PACS couples using standard performance metrics such as the ROC-AUC and the best F1-score.

Locator: Results

[43] [Oil & Water? Diffusion of AI Within and Across Scientific Fields](https://arxiv.org/pdf/2405.15828) (Eamon Duede, William Dolan, André Bauer, Ian Foster, Karim Lakhani; 2024) — AI 'ubiquity' across 20 fields; no per-field exit.

> every field in our corpus experiencing a rapid increase in the diffusion of AI-engaged research across their publication venues

Locator: Ubiquity section

[44] [Evaluating the state-of-the-art in mapping research spaces: A Brazilian case study (PLoS ONE 16:e0248724)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7971485/fullTextXML) (2021) — Field-entry AUROC for scientists/institutions/states (0.879/0.856/0.631, Table 2); densities over a time window; graded RCA states.

> both models achieved good results when predicting the inactive to active (0 → A) transition for scientists and institutions (average AUROC >0.8)

Locator: Conclusions

> over a time window [t − ΔRCA, t]

Locator: Methods

[45] [Epistemic integration and social segregation of AI in neuroscience (ANS 9:8)](https://arxiv.org/pdf/2310.01046) (Sylvain Fontaine, Floriana Gargiulo, Michel Dubois, Paola Tubaro; 2024) — ANS sci-sci template (Introduction, Literature review, Data and methods, Results, Discussion, Declarations); RQ2 single-concept comparator.

[46] [Social Dynamics of Science (Sci Rep 3:1069)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3545262/fullTextXML) (Xiaoling Sun, Jasleen Kaur, Staša Milojević, Alessandro Flammini, Filippo Menczer; 2013) — Discipline birth/decline via community split/merge model.

> The key idea behind our model is that new scientific fields emerge from splitting and merging of these social communities.

Locator: Introduction

[47] [Networks for everyday life (Applied Network Science collection)](https://link.springer.com/collections/fgcaicgjah) (2026) — Page IdP-blocked; search-engine snippets (2026-09-28) give: submissions open 24 June 2026, deadline 30 November 2026, scope items on information diffusion and innovation/collaboration/knowledge-exchange networks; editor list unrecovered.

[48] [The Local Emergence and Global Diffusion of Research Technologies (JASIST 62:846)](https://arxiv.org/pdf/1011.3120) (Loet Leydesdorff, Ismael Rafols; 2011) — Two-case comparison of geographic vs cognitive diffusion.

[49] [Modelling trend life cycles in scientific research using the Logistic and Gompertz equations (Scientometrics 126:9113)](https://api.crossref.org/works/10.1007/s11192-021-04137-0) (2021) — Topic life-cycle curve fits (title-level).

[50] [Quantifying cross-disciplinary knowledge flow from the perspective of content: knowledge memes (J Informetr 14:101092)](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.joi.2020.101092?fields=title,year,authors,venue,abstract,externalIds) (Jin Mao, Zhentao Liang, Yujie Cao, Gang Li; 2020) — Meme diffusion cascades across 5 disciplines.

> preferential attachment takes effect in cross-disciplinary knowledge meme diffusion

Locator: Abstract

[51] [Crossref REST API (DOI verification)](https://api.crossref.org/works) — Used to verify 50+ new DOIs (first author, year, title, venue).

[52] [Author multidisciplinarity and disciplinary roles in field of study networks (ANS 7:78)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9673898/fullTextXML) (Eoghan Cunningham, Barry Smyth, Derek Greene; 2022) — Published ANS sci-sci article: Introduction/Related work/Methods/Case studies/Conclusions; 214-word abstract; 7 figs, 4 tables, 29 refs; Fig. 1 two-step schematic.

[53] [Europe PMC search for the collection name](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22Networks%20for%20everyday%20life%22&format=json&resultType=core) — 24 hits, none in Applied Network Science: route failed.

[54] [Crossref ISSN-filtered search for the collection](https://api.crossref.org/works?query=%22Networks+for+everyday+life%22&filter=issn:2364-8228&rows=50) — No collection metadata: route failed.

[55] [Quantifying patterns of research-interest evolution (Nat Hum Behav 1:0078)](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/s41562-017-0078?fields=title,year,authors,venue,abstract,externalIds) (Tao Jia, Dashun Wang, B. Szymanski; 2017) — Individual research-interest change follows an exponential distribution (abstract).

[56] [Journal publications in medicine: ranking vs. interdisciplinarity (ANS 11:11)](https://api.crossref.org/works/10.1007/s41109-025-00769-w) (2025) — ANS sci-sci precedent; not read in full (Springer bot challenge).

[57] [Wayback CDX query for the collection page](https://web.archive.org/cdx/search/cdx?url=link.springer.com/collections/fgcaicgjah*&output=txt&limit=20) — Empty: no archived snapshot.

## Verification

Numbered citations resolve to unique listed sources. Passage checks test text occurrence, not claim truth or entailment. Author/year metadata and locators are not independently verified. Details: `research_verification.json`.

- Source [1]: text found — In the main manuscript we will consider a standard Δ = 4
- Source [1]: text found — These conditions help reduce the number of false-positive observations. We only consider entry event
- Source [1]: text found — We call the set of products present in a country with an RCA greater one
- Source [2]: text found — we consider a backward condition that requires that a country c had an RCA lower than 1.0 over produ
- Source [3]: text found — requiring that the RCA values were below a non-significance threshold t=0.25 in all the previous yea
- Source [3]: text found — which simply uses the RCA values in 2013 to predict the export matrix in 2018
- Source [3]: text found — tree-based algorithms clearly outperform both the quite strong auto-correlation benchmark and the ot
- Source [4]: text found — countries are 65% more likely to start exporting a product which was being exported with comparative
- Source [4]: text found — from RCAcp ≤0.1 to RCAcp ≥0.1 within a ten year period
- Source [5]: text found — xi = 1 if RCAi>1 and 0 otherwise
- Source [6]: text found — We also check whether changing the criteria for the dummy variable x from RCA>1 to a threshold dolla
- Source [7]: text found — And unrelated industries had a higher probability to exit the region.
- Source [8]: text found — Entries and exits of cities from patent classes are linked to local and non-local measures of
- Source [9]: text found — we distinguish between approaches that use continuous prevalence information and those that binarize
- Source [10]: text found — represents the volume of trade (in US dollar) of product p from exporter o to destination d in year 
- Source [11]: text found — By examining the entry (exit) of advantages across each subsequent time step
- Source [12]: text found — whereas it will deter entry when the signal is negative
- Source [12]: text found — is associated with a 0.1 percentage-point increase in the probability of entry into the market
- Source [13]: text found — The first is that absence or loss of comparative advantage should be considered as a useful source o
- Source [13]: text found — all measures that we analyzed performed extremely well, and hence the theoretical proposals do not a
- Source [15]: text found — because this knowledge can orient the investments of other entrepreneurs
- Source [16]: text found — rely on repeated introductions for their persistence
- Source [17]: text found — provides a terminology and categorisation for populations at different points in the invasion proces
- Source [18]: text found — we propose propagule pressure as a key element to understanding why some introduced populations fail
- Source [22]: text found — We use the presence and appearance of industries in countries (phenotypes) to infer capability
- Source [23]: text found — achieve consistent intellectual usage
- Source [23]: text found — New ideas become core concepts of science when they reach expansive networks of unrelated authors
- Source [24]: text found — The average area under the ROC curve for individuals (Figure 3 a) is 0.8963 for the research space a
- Source [26]: text found — describing the probability that a region enters (or exits) an economic activity as a function of the
- Source [27]: text found — ROC–AUC in [0.954, 0.967] at all horizons without re-tuning
- Source [29]: text found — 71 emerging topics from 2007 to 2010 are identified and characterized
- Source [29]: text found — External evidence (e.g., awards) correlates well with emerging topics
- Source [36]: text found — AUC2017=0.85
- Source [36]: text found — roughly 5% of all edges have been drawn by the end of 2017
- Source [37]: text found — absorbing, absorbing to mutual, back-nurture and mutual mode
- Source [42]: text found — We evaluate the effectiveness of context similarity to forecast unseen PACS couples using standard p
- Source [43]: text found — every field in our corpus experiencing a rapid increase in the diffusion of AI-engaged research acro
- Source [44]: text found — both models achieved good results when predicting the inactive to active (0 → A) transition for scie
- Source [44]: text found — over a time window [t − ΔRCA, t]
- Source [46]: text found — The key idea behind our model is that new scientific fields emerge from splitting and merging of the
- Source [50]: text found — preferential attachment takes effect in cross-disciplinary knowledge meme diffusion

## Follow-up Questions

- Does retained-field relatedness (d0_ret_rel) survive a persistence-filtered RCA density rival (RCA>1 / entered in each of t-2..t, Pinheiro-style Δ-rule moved to the predictor side) and a neighbour-momentum density (relatedness-weighted usage growth in adopting fields, Fernandes & Tang's signal) on the iteration-3 held-out groups?
- Is the abandonment coefficient distinguishable from absence: in D_ever = D_ret + D_lost, can β_ret = β_lost be rejected, and does D_lost remain negative after controlling for never-entered co-absence (Nomaler & Verspagen anti-relatedness)?
- How do Cheng et al. (2023) measure 'consistent intellectual usage' — per field or globally — and does it predict spread into NEW fields (which would anticipate Claim A in science)?
- Do Boschma, Balland & Kogler (2015, 'rise and fall') or Coniglio et al. (2021, path-defying changes) use duration- or stability-weighted density as a predictor of technology/product entry?
- Who are the guest editors and member articles of the 'Networks for everyday life' collection (recoverable only from an authenticated browser session), and do any members study knowledge or innovation diffusion?

---
*Generated by AI Inventor Pipeline*
