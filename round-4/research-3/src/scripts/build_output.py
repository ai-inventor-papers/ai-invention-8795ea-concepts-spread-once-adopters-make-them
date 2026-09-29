"""Build .terminal_claude_agent_struct_out.json; checks every supporting quote against raw fetched text."""
import json, re
from pathlib import Path

W = Path(__file__).resolve().parent.parent
RAW = W / "raw" / "fetch"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("ﬁ", "fi").replace("ﬀ", "ff")).strip().lower()


RAWTXT = {p.stem: norm(p.read_text(errors="ignore")) for p in RAW.glob("*.txt")}
D = lambda d: f"https://doi.org/{d}"

# (index, url, title, authors, year, summary, [(quote, locator, rawfile or None)])
S = [
 (1, "https://journals.sagepub.com/doi/full/10.1177/00031224231166955", "How New Ideas Diffuse in Science (American Sociological Review 88:522-561)",
  ["Mengjie Cheng", "Daniel Scott Smith", "Xiang Ren", "Hancheng Cao", "Sanne Smith", "Daniel A. McFarland"], 2023,
  "Full text read. 56,540 new WoS terms; DV = articles using the term at t+1 (volume, no lagged-DV control); multilevel over-dispersed Poisson, in-sample. Ideational consistency (cosine of neighbour co-usage t-1 to t = weighted edge persistence) b=.43 (+53%/SD); ideational embeddedness b=.22; social embeddedness (author density) b=-.16. Main CONTRADICTED-BY source for C2 (volume outcome).",
  [("rate of co-usage with the focal term in year", "Table 2, Ideational consistency", "cheng_all"),
   ("A one standard deviation increase in ideational consistency of a new idea is associated with a 53 percent", "Results, The Effects of Ideational and Social Ecology", "cheng_results"),
   ("a one standard deviation change in social embeddedness is associated with a 15 percent", "Results", "cheng_results"),
   ("We construct our dependent variable as the number of articles a new idea diffuses into the year ahead", "Outcome of Interest", "cheng_all"),
   ("we do not explore how an idea translates across domains or corpora", "Limitations", "cheng_results2")]),
 (2, "https://arxiv.org/pdf/2606.03919", "Forecasting Conceptual Diffusion in Science: The Case of Quantum Computing (arXiv 2606.03919)",
  ["Thomas Maillart", "Thibaut Chataing", "David Dosu", "Paul Bagourd", "Julian Jang-Jaccard", "Alain Mermoud"], 2026,
  "Concept PAIRS in the OpenAlex quantum-computing subtree; upstream citation heterogeneity/entropy predicts downstream exogenous count (test R2 0.7804) and adoption entropy (0.6866); endogenous 0.0179 after growth normalisation; stratified 80/20 random split (not field hold-out). Closest C1 near-miss.",
  [("stratified 80/20 train", "Table 2 caption", "maill_n"),
   ("endogenous reinforcement proves largely unpredictable in the primary", "Abstract", "maill_n"),
   ("exogenous count task achieves strong and consistent predictive power", "Results", "maill_n")]),
 (3, D("10.1007/BF02019280"), "Co-word analysis as a tool for describing the network of interactions between basic and technological research (Scientometrics 22:155-205)",
  ["M. Callon", "J. P. Courtial", "F. Laville"], 1991, "Origin of density/centrality strategic diagrams; density read as a cluster's capacity to maintain itself (as quoted in Chavalarias & Cointet). Descriptive; DOI verified via Crossref.", []),
 (4, "https://sci2s.ugr.es/sites/default/files/ficherosPublicaciones/1321_mjcobo-joi-2010.pdf", "An approach for detecting, quantifying, and visualizing the evolution of a research field (J Informetr 5:146-166)",
  ["M.J. Cobo", "A.G. López-Herrera", "E. Herrera-Viedma", "F. Herrera"], 2011, "Defines Callon centrality/density and the four strategic-diagram quadrants; the low/low quadrant is ambiguous (emerging or disappearing); no predictive test.",
  [("The themes of this quadrant have low density and low centrality, mainly representing either emerging or disappearing themes.", "Section 3.2", "cobo2011")]),
 (5, D("10.1002/asi.22688"), "SciMAT: A new science mapping analysis software tool (JASIST 63:1609-1630)", ["M.J. Cobo", "A.G. López-Herrera", "E. Herrera-Viedma", "F. Herrera"], 2012, "Software operationalising strategic diagrams and thematic evolution; descriptive.", []),
 (6, "https://arxiv.org/abs/2603.06436", "Rethinking Thematic Evolution in Science Mapping: An Integrated Framework for Longitudinal Analysis (J Informetr 20:101877)",
  ["Massimo Aria", "Luca D'Aniello", "Michelangelo Misuraca", "Maria Spano"], 2026, "Recent critique/reframing of longitudinal strategic diagrams; framework, no predictive validation.",
  [("Yet a structural inconsistency characterises dominant longitudinal implementations", "Abstract", "rethink")]),
 (7, D("10.1002/(sici)1097-4571(1998)49:13<1206::aid-asi7>3.0.co;2-f"), "Software engineering as seen through its research literature: a study in co-word analysis (JASIS 49:1206-1223)", ["Neal Coulter", "Ira Monarch", "Suresh Konda"], 1998, "Classic co-word strategic-diagram application; DOI found via Crossref bibliographic query.", []),
 (8, "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0054847", "Phylomemetic Patterns in Science Evolution - The Rise and Fall of Scientific Fields (PLoS ONE 8:e54847)",
  ["David Chavalarias", "Jean-Philippe Cointet"], 2013, "Term-cluster fields: density higher for long-lived/steady fields, rises during emergence and falls before decline. CONTRADICTED-BY for C2 (survival outcome) and opposite timing prior for C4.",
  [("steady fields have a density of up to twice the average value, whereas ephemeral fields always have a below-average density", "Results, density", "chav_d"),
   ("the density grows when a new field is emerging, and decreases when the field starts to be neglected by the community", "Figure 5 caption", "chav_d")]),
 (9, "https://peerj.com/articles/cs-119.pdf", "How are topics born? Understanding the research dynamics preceding the emergence of new areas (PeerJ CS 3:e119)",
  ["Angelo A. Salatino", "Francesco Osborne", "Enrico Motta"], 2017, "Rising collaboration pace and density among PARENT topics precede topic birth (75 debutant vs 100 control topics, CS). Different unit/outcome; reads as opposite sign to C2.",
  [("the pace of collaboration and the density measured in the sections of the network that will give rise to a new topic are significantly higher than those in the control group", "Introduction", "salatino17")]),
 (10, D("10.1145/3197026.3197052"), "AUGUR: Forecasting the Emergence of New Research Topics (JCDL 2018:303-312)", ["Angelo A. Salatino", "Francesco Osborne", "Enrico Motta"], 2018, "Forecasts topic emergence from diachronic co-occurrence dynamics of research-area clusters (carried from prior report).", []),
 (11, D("10.1016/j.respol.2014.02.005"), "Identifying emerging topics in science and technology (Res Policy 43:1450-1467)", ["Henry Small", "Kevin W. Boyack", "Richard Klavans"], 2014, "Novelty+growth nomination of 71 emerging topics; no held-out metric (carried).", []),
 (12, D("10.1016/j.respol.2015.06.006"), "What is an emerging technology? (Res Policy 44:1827-1843)", ["Daniele Rotolo", "Diana Hicks", "Ben R. Martin"], 2015, "Five attributes of emergence; definitional baseline.", []),
 (13, "http://cluster.ischool.drexel.edu/~cchen/papers/2012/jasist2012-predictive.pdf", "Predictive effects of structural variation on citation counts (JASIST 63:431-449)",
  ["Chaomei Chen"], 2012, "Paper-level boundary-spanning metrics (modularity change, cluster linkage, centrality divergence) predict citations (ZINB, 5 cases). Correct DOI 10.1002/asi.21694; the plan's 10.1002/asi.22662 is a different paper.",
  [("Centrality Divergence metric is potentially", "Abstract", "chen12pdf")]),
 (14, D("10.1016/j.joi.2009.03.004"), "Towards an explanatory and computational theory of scientific discovery (J Informetr 3:191-209)", ["Chaomei Chen", "Yue Chen", "Mark Horowitz", "Haiyan Hou", "Zeyuan Liu", "Donald Pellegrino"], 2009, "Structural-variation / boundary-spanning theory of discovery; conceptual C1 precedent (Crossref query).", []),
 (15, D("10.1016/j.techfore.2021.120944"), "Tracking the dynamics of co-word networks for emerging topic identification (TFSC 170:120944)", ["Lu Huang", "Xiang Chen", "Xingxing Ni", "Jiarun Liu", "Xiaoli Cao", "Changtian Wang"], 2021, "Dynamic co-word link prediction + BPNN for emerging topics; link-level, not comparable.", []),
 (16, "https://aclanthology.org/2020.findings-emnlp.158.pdf", "Will This Idea Spread Beyond Academia? Understanding Knowledge Transfer of Scientific Concepts across Text Corpora (Findings of EMNLP 2020:1746-1757)",
  ["Hancheng Cao", "Mengjie Cheng", "Zhepeng Cen", "Daniel McFarland", "Xiang Ren"], 2020, "Concept-level (450k new concepts) prediction of transfer into patents/clinical trials with temporal cutoffs; interdisciplinary-venue usage is an early sign. C1 same direction, different outcome.",
  [("usage in interdisciplinary venues", "Introduction", "cao20b")]),
 (17, D("10.1145/3148011.3148030"), "Forecasting the Spreading of Technologies in Research Communities (K-CAP 2017:1-8)", ["Francesco Osborne", "Andrea Mannocci", "Enrico Motta"], 2017, "Technology-to-research-area propagation forecasting (technology-topic pairs); RQ2 local-origin-then-spread framing; abstract level.", []),
 (18, D("10.1103/PhysRevX.4.041036"), "Inheritance Patterns in Citation Networks Reveal Scientific Memes (PRX 4:041036)", ["Tobias Kuhn", "Matjaž Perc", "Dirk Helbing"], 2014, "Meme score from frequency and propagation along citations; no openness predictor.", []),
 (19, D("10.1038/srep01069"), "Social Dynamics of Science (Sci Rep 3:1069)", ["Xiaoling Sun", "Jasleen Kaur", "Staša Milojević", "Alessandro Flammini", "Filippo Menczer"], 2013, "Agent-based model: disciplines emerge from splitting and merging of collaboration communities (abstract).", []),
 (20, D("10.1016/j.joi.2020.101092"), "Quantifying cross-disciplinary knowledge flow from the perspective of content: knowledge memes (J Informetr 14:101092)", ["Jin Mao", "Zhentao Liang", "Yujie Cao", "Gang Li"], 2020, "Knowledge-meme diffusion cascades between Medical Informatics and four disciplines; descriptive RQ2 comparator.", []),
 (21, "https://arxiv.org/pdf/1011.3120", "The Local Emergence and Global Diffusion of Research Technologies (JASIST 62:846-860)", ["Loet Leydesdorff", "Ismael Rafols"], 2011, "siRNA vs nanocrystalline solar cells; local emergence then global diffusion; mode-1 to mode-2 transition explains rate differences.",
  [("The strength of preferential attachment decreases over time", "Abstract", "leyraf")]),
 (22, D("10.1126/science.1240474"), "Atypical Combinations and Scientific Impact (Science 342:468-472)", ["Brian Uzzi", "Satyam Mukherjee", "Michael Stringer", "Ben Jones"], 2013, "Paper-level: conventional core plus atypical combinations predicts high impact.", []),
 (23, D("10.1177/0003122415601618"), "Tradition and Innovation in Scientists' Research Strategies (ASR 80:875-908)", ["Jacob G. Foster", "Andrey Rzhetsky", "James A. Evans"], 2015, "Exploration vs tradition strategies in biomedical chemistry; risky innovation rarely chosen, rewarded.", []),
 (24, "https://www.nber.org/system/files/working_papers/w22180/w22180.pdf", "Bias against novelty in science: A cautionary tale for users of bibliometric indicators (Res Policy 46:1416-1436; NBER w22180)",
  ["Jian Wang", "Reinhilde Veugelers", "Paula Stephan"], 2017, "Paper-level novelty (new distant journal pairs) raises foreign-field citation impact: odds of top-1% in foreign fields +29.39%/+62.37%; not in home field. Closest paper-level C1 analogue.",
  [("29.39% and 62.37% higher for moderately and highly novel papers respectively", "Section 4 (home vs foreign field)", "wang2017")]),
 (25, "https://www.nature.com/articles/s41467-023-36741-4", "Surprising combinations of research contents and contexts are related to impact and emerge with scientific outsiders from distant disciplines (Nat Commun 14:1641)",
  ["Feng Shi", "James Evans"], 2023, "Surprise predicts outsized impact and emerges when outsiders publish to distant audiences; paper-level C1 analogue.",
  [("most commonly when scientists from one field publish problem-solving results to an audience from a distant field", "Abstract", "shievans")]),
 (26, D("10.1038/srep05890"), "The dynamics of correlated novelties (Sci Rep 4:5890)", ["F. Tria", "V. Loreto", "V. D. P. Servedio", "S. H. Strogatz"], 2014, "Adjacent-possible urn model; theory anchor for exploration.", []),
 (27, D("10.1103/PhysRevLett.120.048301"), "Network Dynamics of Innovation Processes (PRL 120:048301)", ["Iacopo Iacopini", "Staša Milojević", "Vito Latora"], 2018, "Random walks on concept networks reproduce novelty rates; no later-spread test.", []),
 (28, "https://www.pnas.org/doi/10.1073/pnas.1915378117", "The Diversity-Innovation Paradox in Science (PNAS 117:9284-9291)",
  ["Bas Hofstra", "Vivek V. Kulkarni", "Sebastian Munoz-Najar Galvez", "Bryan He", "Dan Jurafsky", "Daniel A. McFarland"], 2020, "Concept-link novelty and uptake-per-link measure in dissertations; uptake precedent.",
  [("taken up by other scholars at lower rates", "Significance", "hofstra")]),
 (29, "https://arxiv.org/abs/2510.03240", "Generalization and the Rise of System-level Creativity in Science (arXiv 2510.03240)", ["Hongbo Fang", "James Evans"], 2025,
  "Paper-level citation-role typology (foundations/extensions/generalizations) on OpenAlex and WoS; generality defined from downstream reuse (outcome-side).",
  [("we decompose scientific contributions into three functional types, foundations, extensions, and generalizations", "Abstract", "fang")]),
 (30, "https://www.pnas.org/doi/10.1073/pnas.1116502109", "Structural diversity in social contagion (PNAS 109:5962-5966)", ["Johan Ugander", "Lars Backstrom", "Cameron Marlow", "Jon Kleinberg"], 2012,
  "Number of connected components of the contact neighbourhood controls adoption; size becomes a negative predictor; edge density uninformative within one-component neighbourhoods.",
  [("the size of the contact neighborhood is in fact generally a negative predictor of contagion", "Abstract", "ugander2"),
   ("probability of contagion is tightly controlled by the number of connected components", "Abstract", "ugander")]),
 (31, "https://arxiv.org/pdf/1306.0158", "Virality Prediction and Community Structure in Social Networks (Sci Rep 3:2522)", ["Lilian Weng", "Filippo Menczer", "Yong-Yeol Ahn"], 2013,
  "Early spread across many communities (first adopters) predicts meme virality at about 7x random precision (carried from art_dxvRpQufMR0e).",
  [("about seven times as precise as random guess", "Results, prediction (carried)", None)]),
 (32, D("10.1126/science.1185231"), "The Spread of Behavior in an Online Social Network Experiment (Science 329:1194-1197)", ["Damon Centola"], 2010, "Clustered-lattice networks spread behaviour farther and faster than random ones (complex contagion); CONTRADICTED-BY for C2 at the adoption-depth level.", []),
 (33, "https://www.cs.cornell.edu/home/kleinber/www11-hashtags.pdf", "Differences in the mechanics of information diffusion across topics: idioms, political hashtags, and complex contagion on Twitter (WWW 2011:695-704)",
  ["Daniel M. Romero", "Brendan Meeder", "Jon Kleinberg"], 2011, "Persistent (complex-contagion) political hashtags have denser early-adopter subgraphs; idioms are non-persistent.",
  [("hashtags on politically controversial topics are particularly persistent", "Abstract", "romero")]),
 (34, D("10.1086/421787"), "Structural Holes and Good Ideas (AJS 110:349-399)", ["Ronald S. Burt"], 2004, "Brokerage across structural holes yields good ideas; constraint mechanism for C2.", []),
 (35, D("10.1086/661238"), "The Diversity-Bandwidth Trade-off (AJS 117:90-171)", ["Sinan Aral", "Marshall Van Alstyne"], 2011, "Structural diversity vs channel bandwidth trade-off for novel information.", []),
 (36, "https://arxiv.org/pdf/0704.0744", "Quantifying social group evolution (Nature 446:664-667)", ["Gergely Palla", "Albert-László Barabási", "Tamás Vicsek"], 2007,
  "Large communities persist longer when membership turns over; small ones need stable composition. Partial precedent for churn (C2/C3) with a size interaction.",
  [("large groups persist longer if they are capable of dynamically altering their", "Abstract", "palla"),
   ("The behaviour of small groups displays the opposite tendency", "Abstract", "palla")]),
 (37, "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/s11192-025-05356-5?fields=title,year,authors,venue,abstract,externalIds", "Citation structural diversity: a novel metric combining structure and semantics for literature evaluation (Scientometrics 130:4027-4060)",
  ["Mingyue Kong", "Yinglong Zhang", "Likun Sheng", "Kaifeng Hong"], 2025, "Paper-level citation structural diversity correlates with citations and topic breadth; abstract level, no size control reported.",
  [("structural diversity is shown to be positively correlated with topic breadth", "Abstract", "strdiv")]),
 (38, D("10.1016/0304-4076(94)01598-T"), "General purpose technologies 'Engines of growth'? (J Econometrics 65:83-108)", ["Timothy F. Bresnahan", "M. Trajtenberg"], 1995, "GPT concept anchor.", []),
 (39, D("10.1080/10438599700000006"), "University Versus Corporate Patents: A Window On The Basicness Of Invention (EINT 5:19-50)", ["Manuel Trajtenberg", "Rebecca Henderson", "Adam Jaffe"], 1997, "Origin of the generality index (ex-post, citing-class Herfindahl complement).", []),
 (40, "https://www.nber.org/system/files/working_papers/w10901/w10901.pdf", "Uncovering GPTs with Patent Data (NBER w10901)", ["Bronwyn Hall", "Manuel Trajtenberg"], 2004,
  "Generality defined from forward citations across classes (ex-post); used to flag GPT candidates, not tested as an early predictor of later generality.",
  [("cited by subsequent patents that belong to a wide range of fields", "Section 3.1 Generality", "hallt2")]),
 (41, D("10.1257/0002828041301407"), "Was Electricity a General Purpose Technology? Evidence from Historical Patent Citations (AER 94:388-394)", ["Petra Moser", "Tom Nicholas"], 2004, "GPT test via patent citations; DOI corrected (plan's guess returned 404).", []),
 (42, D("10.1093/icc/dtr040"), "An empirical test for general purpose technology: an examination of the Cohen-Boyer rDNA technology (ICC 21:249-275)", ["M. P. Feldman", "J. W. Yoon"], 2012, "GPT test on rDNA; DOI corrected (plan's guess pointed to a different paper).", []),
 (43, D("10.1016/j.respol.2020.104013"), "Mapping general purpose technologies with patent data (Res Policy 49:104013)", ["Sergio Petralia"], 2020, "Three-dimension GPT indicator (growth, range of uses via text mining, complementarity).", []),
 (44, D("10.1787/5k4522wkw1r8-en"), "Measuring Patent Quality: Indicators of Technological and Economic Value (OECD STI WP 2013/03)", None, 2013, "OECD operationalisation of generality/originality indicators.", []),
 (45, D("10.1016/j.joi.2018.03.007"), "Characterizing highly cited method and non-method papers using citation contexts: The role of uncertainty (J Informetr 12:461-480)", ["Henry Small"], 2018, "Method vs non-method classification of the top-1000 biomedical papers; no cross-field reach effect size.", []),
 (46, "https://aclanthology.org/P16-1111.pdf", "Predicting the Rise and Fall of Scientific Topics from Trends in their Rhetorical Framing (ACL 2016:1170-1180)",
  ["Vinodkumar Prabhakaran", "William L. Hamilton", "Dan McFarland", "Dan Jurafsky"], 2016, "Topics framed as methods are in early growth; result-framed topics decline. Concept-type (S7) and life-cycle (C4) evidence.",
  [("rhetorical function is highly predictive of", "Abstract", "prabh")]),
 (47, "https://arxiv.org/pdf/2606.07994", "The Rising Dominance of Methods Across Science (arXiv 2606.07994)", ["Alexander Krauss", "Ariel Rosenfeld", "Lutz Bornmann"], 2026,
  "Methods-paper share doubled (~20% to 40%) 1980-2019 across disciplines; argues methods transfer across fields but gives no cross-field reach effect size.",
  [("share of methods papers doubled over the past four decades", "Introduction", "krauss")]),
 (48, D("10.1287/orsc.2.1.71"), "Exploration and Exploitation in Organizational Learning (Org Sci 2:71-87)", ["James G. March"], 1991, "Theory anchor for exploration vs exploitation framing.", []),
 (49, D("10.1177/030631289019003001"), "Institutional Ecology, 'Translations' and Boundary Objects (Soc Stud Sci 19:387-420)", ["Susan Leigh Star", "James R. Griesemer"], 1989, "Boundary-object theory anchor.", []),
 (50, D("10.1073/pnas.1509757112"), "Choosing experiments to accelerate collective discovery (PNAS 112:14569-14574)", ["Andrey Rzhetsky", "Jacob G. Foster", "Ian T. Foster", "James A. Evans"], 2015, "Model: more risk-taking would speed discovery.", []),
 (51, D("10.1177/2329496514540131"), "Sociological Innovation through Subfield Integration (Social Currents 1:228-256)", ["Erin Leahey", "James Moody"], 2014, "Subfield-integration measures incl. novelty of combinations (verified; plan flagged VERIFY).", []),
 (52, D("10.15195/v1.a15"), "Finding Cultural Holes: How Structure and Culture Diverge in Networks of Scholarly Communication (Sociological Science 1:221-238)", ["Daril Vilhena", "Jacob Foster", "Martin Rosvall", "Jevin West", "James Evans", "Carl Bergstrom"], 2014, "Information-theoretic measure of jargon barriers between fields; nearest quantitative 'interpretive distance' measure, not linked to term adoption.", []),
 (53, D("10.1371/journal.pone.0008694"), "Mapping Change in Large Networks (PLoS ONE 5:e8694)", ["Martin Rosvall", "Carl T. Bergstrom"], 2010, "Alluvial diagrams with significance for community change; descriptive.", []),
 (54, "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0270131", "Quantifying the rise and fall of scientific fields (PLoS ONE 17:e0270131)",
  ["Chakresh Kumar Singh", "Emma Barme", "Robert Ward", "Liubov Tupikina", "Marc Santolini"], 2022, "72 arXiv fields: early phases interdisciplinary (2.36 vs 2.05 fields per article) with small teams (2 vs 4.5), late phases specialised; stage-averaged life-cycle analogue for C4.",
  [("the early phase of a field is characterized by disruptive works mixing of cognitively distant fields written by small teams of interdisciplinary authors", "Abstract", "singh22")]),
 (55, "https://api.crossref.org/works/10.1098/rspb.2017.2360", "How new concepts become universal scientific approaches: insights from citation network analysis of agent-based complex systems science (Proc R Soc B 285:20172360)",
  ["Christian E. Vincenot"], 2018, "ABM and IBM communities: disjoint, then progressive merger; single-case RQ2 sequence.",
  [("confirmed their past disjointedness, and detected their progressive merger", "Abstract", "vinc_cr")]),
 (56, D("10.1016/j.joi.2009.03.001"), "Scientific discovery and topological transitions in collaboration networks (J Informetr 3:210-221)", ["L. M. A. Bettencourt", "D. I. Kaiser", "J. Kaur"], 2009, "Field emergence accompanied by a topological transition in collaboration networks (title-level; Crossref-verified).", []),
 (57, "https://arxiv.org/abs/1708.03850", "Structure in scientific networks: towards predictions of research dynamism (arXiv 1708.03850)", ["Benjamin W. Stewart", "Andy Rivas", "Luat T. Vuong"], 2017, "Citation-network structure vs growth/decline of three optics areas; case-level.", []),
 (58, D("10.1016/j.tree.2005.02.004"), "The role of propagule pressure in explaining species invasions (TREE 20:223-228)", ["Julie L. Lockwood", "Phillip Cassey", "Tim Blackburn"], 2005, "Propagule pressure analogy for C3 (repeated introduction vs establishment).", []),
 (59, D("10.1111/j.1472-4642.2009.00594.x"), "The more you introduce the more you get: the role of colonization pressure and propagule pressure in invasion ecology (Divers Distrib 15:904-910)", ["Julie L. Lockwood", "Phillip Cassey", "Tim M. Blackburn"], 2009, "Colonisation-pressure analogy for C3.", []),
 (60, "https://arxiv.org/pdf/cond-mat/0206130", "Hierarchical organization in complex networks (PRE 67:026112)", ["Erzsébet Ravasz", "Albert-László Barabási"], 2003,
  "C(k) ~ 1/k: local density falls with degree; basis of the degree-dependence threat to ego_density_W3 (design gap).",
  [("indicating that the higher a node", "Section on hierarchical model", "ravasz")]),
 (61, D("10.1046/j.1461-0248.2001.00230.x"), "Quantifying biodiversity: procedures and pitfalls in the measurement and comparison of species richness (Ecol Lett 4:379-391)", ["Nicholas J. Gotelli", "Robert K. Colwell"], 2001, "Rarefaction justification for size-adjusted breadth.", []),
 (62, D("10.1016/0197-2456(86)90046-2"), "Meta-analysis in clinical trials (Control Clin Trials 7:177-188)", ["Rebecca DerSimonian", "Nan Laird"], 1986, "Random-effects pooling used across held-out groups.", []),
 (63, D("10.1002/sim.1186"), "Quantifying heterogeneity in a meta-analysis (Stat Med 21:1539-1558)", ["Julian P. T. Higgins", "Simon G. Thompson"], 2002, "I-squared interpretation for I2 0.75-0.78.", []),
 (64, D("10.1016/j.jeconom.2020.09.006"), "Estimating dynamic treatment effects in event studies with heterogeneous treatment effects (J Econometrics 225:175-199)", ["Liyang Sun", "Sarah Abraham"], 2021, "Staggered event-study estimator for C4.", []),
 (65, D("10.1016/j.jeconom.2020.12.001"), "Difference-in-Differences with multiple time periods (J Econometrics 225:200-230)", ["Brantly Callaway", "Pedro H. C. Sant'Anna"], 2021, "Group-time ATT estimator for C4.", []),
 (66, D("10.1016/j.jeconom.2021.03.014"), "Difference-in-differences with variation in treatment timing (J Econometrics 225:254-277)", ["Andrew Goodman-Bacon"], 2021, "TWFE decomposition; staggered-timing bias for C4.", []),
 (67, D("10.1038/s41587-021-00907-6"), "Learning on knowledge graph dynamics provides an early warning of impactful research (Nat Biotechnol 39:1300-1307)", ["James W. Weis", "Joseph M. Jacobson"], 2021, "Paper-level impact forecasting from knowledge-graph dynamics; not comparable (paper unit, impact outcome).", []),
 (68, "https://arxiv.org/abs/2511.18631", "FOS: A Large-Scale Temporal Graph Benchmark for Scientific Interdisciplinary Link Prediction (arXiv 2511.18631)", ["Kiyan Rezaee", "Morteza Ziabakhsh", "Niloofar Nikfarjam", "Mohammad M. Ghassemi"], 2025, "Field-pair link-prediction benchmark (65,027 sub-fields); level metrics, not comparable.", []),
 (69, "https://arxiv.org/pdf/1906.06843", "Predicting research trends with semantic and neural networks with an application in quantum physics (PNAS 117:1910)", ["Mario Krenn", "Anton Zeilinger"], 2020, "Concept-pair link forecast AUC 0.85: a level AUC, not comparable (carried).", []),
 (70, "https://arxiv.org/pdf/1602.08409", "The research space: using career paths to predict the evolution of the research output of individuals, institutions, and nations (Scientometrics 109:1695)", ["Miguel R. Guevara", "Dominik Hartmann", "Manuel Aristarán", "Marcelo Mendoza", "César A. Hidalgo"], 2016, "Entity field-entry AUC 0.8963 (carried); different unit.", []),
 (71, "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7374558/fullTextXML", "The evolution of knowledge within and across fields in modern physics (Sci Rep 10:12097)", ["Ye Sun", "Vito Latora"], 2020, "Four field-pair knowledge-flow modes (carried); RQ2 comparator.", []),
 (72, D("10.1007/s41109-016-0017-9"), "Quantifying the diaspora of knowledge in the last century (Applied Network Science 1:15)", ["Manlio De Domenico", "Elisa Omodei", "Alex Arenas"], 2016, "ANS: field-level source/sink knowledge flows (carried, verified in iteration 2).", []),
 (73, D("10.1007/s41109-018-0090-3"), "Community evolution in patent networks: technological change and network dynamics (Applied Network Science 3:26)", ["Yuan Gao", "Zhen Zhu", "Raja Kali", "Massimo Riccaboni"], 2018, "ANS: temporal community tracking in technology networks (carried).", []),
 (74, D("10.1007/s41109-018-0074-3"), "Co-occurrence simplicial complexes in mathematics: identifying the holes of knowledge (Applied Network Science 3:37)", ["Vsevolod Salnikov", "Daniele Cassese", "Renaud Lambiotte", "Nick S. Jones"], 2018, "ANS: higher-order concept co-occurrence (carried).", []),
 (75, D("10.1007/s41109-017-0034-3"), "The weakness of weak ties for novel information diffusion (Applied Network Science 2:14)", ["Jennifer M. Larson"], 2017, "ANS: cross-group ties may impede novel diffusion; counter-mechanism to C1 (carried).", []),
 (76, D("10.1007/s41109-022-00517-4"), "Author multidisciplinarity and disciplinary roles in field of study networks (Applied Network Science 7:78)", ["Eoghan Cunningham", "Barry Smyth", "Derek Greene"], 2022, "ANS: field-of-study networks and bridging roles; closest data design (carried).", []),
 (77, D("10.1007/s41109-023-00572-5"), "Mapping change in higher-order networks with multilevel and overlapping communities (Applied Network Science 8:42)", ["Anton Holmgren", "Daniel Edler", "Martin Rosvall"], 2023, "ANS: descriptive alluvial change (carried).", []),
 (78, "https://arxiv.org/abs/2310.01046", "Epistemic integration and social segregation of AI in neuroscience (Applied Network Science 9:8)", ["Sylvain Fontaine", "Floriana Gargiulo", "Michel Dubois", "Paola Tubaro"], 2024, "ANS: one concept (AI) entering one field (carried).", []),
 (79, D("10.1007/s41109-025-00769-w"), "Journal publications in medicine: ranking vs. interdisciplinarity (Applied Network Science 11:11)", ["Anbang Du", "Michael Head", "Markus Brede"], 2025, "ANS: concept correlation networks in PubMed (carried).", []),
 (80, "https://api.crossref.org/works", "Crossref REST API (reference verification)", None, None, "Used to verify 60 DOIs (66/67 identifiers resolved with the arXiv API) and to correct 3 plan-recalled DOIs (Chen 2012, Moser & Nicholas 2004, Feldman & Yoon 2012).", []),
]

# ---- quote self-check against raw fetched text ----
problems = []
sources = []
for idx, url, title, authors, year, summ, passages in S:
    sp = []
    for q, loc, rf in passages:
        if rf is not None and norm(q) not in RAWTXT.get(rf, ""):
            problems.append((idx, q, rf))
        sp.append({"quote": q, "locator": loc})
    sources.append({"index": idx, "url": url, "title": title, "summary": summ, "authors": authors, "year": year, "supporting_passages": sp})
if problems:
    for p in problems:
        print("QUOTE NOT FOUND:", p)
    raise SystemExit(1)

answer = (Path(W / "scripts" / "answer.md").read_text()).strip()
cited = {int(x) for grp in re.findall(r"\[([\d,\s\-]+)\]", answer) for x in re.split(r"[,\s]+", grp) if x and "-" not in x}
for grp in re.findall(r"\[(\d+)-(\d+)\]", answer):
    cited |= set(range(int(grp[0]), int(grp[1]) + 1))
missing = cited - {s["index"] for s in sources}
if missing:
    raise SystemExit(f"answer cites unknown sources: {missing}")

out = {
    "title": "Is 'keep exploring, spread widest' already known?",
    "layman_summary": "A literature check of whether prior studies already showed that scientific concepts which keep meeting new, varied partners early on later spread across more fields, and which studies say the opposite.",
    "summary": (Path(W / "scripts" / "summary.md").read_text()).strip(),
    "out_expected_files": {"output": "research_out.json", "reproducibility": "reproducibility.md"},
    "upload_ignore_regexes": [],
    "answer": answer,
    "sources": sources,
    "follow_up_questions": [
        "DESIGN GAP: does the ego_density_W3 effect (-0.102) survive a degree-preserving null z-score or within-degree-decile estimation, given that neighbourhood density falls roughly as 1/k (Ravasz & Barabasi 2003)?",
        "Direct test of Cheng et al. 2023: in our frame, does their weighted ideational-consistency measure predict next-period VOLUME positively but size-adjusted cross-field BREADTH negatively (a sign flip by outcome), and does the same hold for their word2vec ideational embeddedness?",
        "Does early consolidation predict persistence/survival (as Chavalarias & Cointet 2013 and Palla et al. 2007 suggest) while openness predicts reach, and does the edge-persistence effect depend on concept size as Palla's size x turnover interaction implies; separately, does the openness effect hold within method and within object concepts?"
    ],
}
(W / ".terminal_claude_agent_struct_out.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print("ok; sources", len(sources), "cited", len(cited), "answer words", len(answer.split()), "summary chars", len(out["summary"]))
