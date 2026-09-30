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
