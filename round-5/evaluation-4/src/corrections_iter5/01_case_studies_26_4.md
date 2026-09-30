# 01 Section 26.4 rebuilt from case_pairs.json, plus the AI atlas

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

Source: `3_invention_loop/iter_4/gen_art/gen_art_experiment_12/results/case_pairs.json` -> `pairs[i].{OPEN_all,OPEN_home,logvol,O2r_resid,rho,Bn,E2}`; counts in `results/derived.json`.

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

Source: `3_invention_loop/iter_4/gen_art/gen_art_experiment_12/ai_atlas/atlas.json` -> `concepts[i]` (the 37-concept list; `ai_atlas/table.csv` is the per-measure median table by type, not the concept list).
