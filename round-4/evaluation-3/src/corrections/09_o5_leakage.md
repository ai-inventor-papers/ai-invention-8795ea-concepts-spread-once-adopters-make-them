# 09 O5 precedence leakage by source and the O5-O3 association

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

Source: `3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/o5_validation.json` -> `precedence_leakage.<source>.{n_matched,share_first_event_le_t0}; lag.<source>.{median,iqr}`
Coverage per group and source (share found, share qualifying in window) is in `iter_3/gen_art/gen_art_evaluation_2/record_tables/o5_coverage_by_group_source.csv`.

## O5-O3 association per held-out group (O5_main; Spearman)

| group | n | rho(O5, O3) | 95% CI |
|---|---|---|---|
| PHYS | 742 | -0.072 | [-0.122, -0.011] |
| LIFEENV | 1,113 | +0.025 | [-0.036, +0.091] |
| SOC | 1,352 | -0.061 | [-0.091, -0.024] |
| MATHDEC | 165 | -0.063 | [-0.099, -0.033] |

Pooled (DL, 4 held-out groups): -0.049 [-0.083, -0.016], p = 0.004, I2 = 0.55. Recognised concepts are slightly LESS transient, but the association is small and heterogeneous.

Source: `3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/record_tables/o5_associations.csv` -> `group==<g>&variant==O5_main::{n,rho_O3,rho_O3_ci95}`; `3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/o5_validation.json` -> `associations_pooled_heldout_DL.O5_main.rho_O3.{pooled,ci95,p,I2}`
