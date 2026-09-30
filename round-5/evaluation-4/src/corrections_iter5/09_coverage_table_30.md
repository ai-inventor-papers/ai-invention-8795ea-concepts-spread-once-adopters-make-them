# 09 Section 30 coverage table, corrected cell by cell

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
