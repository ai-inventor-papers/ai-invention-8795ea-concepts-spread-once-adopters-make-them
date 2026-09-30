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
