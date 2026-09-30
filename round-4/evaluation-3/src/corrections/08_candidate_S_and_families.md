# 08 Candidate S rows and the indicator families (corrects 19.1)

## Candidate S (co-author reach; Cheng et al. 2023) on held-out groups

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] The iteration-1 open rival 'candidate S' was scored in Exp8 as S_comp, S_comp_n and S_isolated_share. DL pooled over the 4 held-out groups from the per-unit rows:

| indicator | outcome | pooled psp | 95% CI | I2 | units positive (of 6) | units CI excl. 0 (of 6) |
|---|---|---|---|---|---|---|
| S_comp_n | O1c | -0.087 | [-0.200, +0.029] | 0.88 | 0 | 4 |
| S_comp_n | O2r_m50 | -0.029 | [-0.239, +0.184] | 0.94 | 3 | 3 |
| S_comp_n | O2r_resid | -0.028 | [-0.244, +0.190] | 0.94 | 3 | 3 |
| S_comp_n | O4 | -0.049 | [-0.192, +0.096] | 0.93 | 3 | 2 |

Source: `round-3/experiment-8/src/results/heldout_unit_results.csv` -> `indicator in S_* :: {z, se_z, rho, ci_lo, ci_hi}`; `round-4/evaluation-3/src/results/partA_derived.json` -> `candidate_S_DL4.*`
Reading: candidate S is now tested (not only 'not run'); none of its rows is in a frozen top-10 confirmed set for breadth; the social-reach rival is weak beyond B5.

## Indicator families (from indicator_dictionary.csv, column 'family')

## Old text (19.1 family list, verbatim)

> The 7 indicator families are:
>
> 1. **Volume/reach** (log_offhome_volume, burst, n_authors_early, author_growth)
> 2. **Cooccurrence topology** (D_ratio, D_rare, participation, n_comm_W3, ego_density_W3, new_edge_rate, NOV)
> 3. **Centrality** (G, G_A, G_btw, G_deg, G_phimin)
> 4. **Relatedness** (RS, REL_home, M0_density_end, D_vol_end, CONTACT_REACH, RETENTION_RATIO_early, FRONTIER_POTENTIAL)
> 5. **Lineage** (edge_persistence, relay_share)
> 6. **External recognition** (external recognition variants)
> 7. **Composite** (entropy, reach, nonhome_share from the five feature baseline)

## New 19.1 family list

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] Exp8 computes 53 indicators in 6 families (entropy, reach, offhome share, log volume and growth belong to the B5 baseline, not to an indicator family; there is no 'external recognition' family, O5 is an outcome):

- **A: co-occurrence ego network** (27): D_z, D_ratio, D_rare, D_sub, D_obs, NOV, NOV_res, F_res, F_z, deg_W1, deg_W3, deg_growth, str_growth, new_edge_rate, edge_persistence, turnover, participation, n_comm_W3, comm_entropy, comm_transitions, ego_density_W3, ego_density_change, btw_end, btw_change, kcore_end, constraint_end, constraint_change
- **E: popularity / volume** (6): share, growth_ind, accel, burst, author_growth, n_authors_early
- **F: disciplinary spread** (3): log_offhome_volume, rao_stirling, fields_gained_per_yr
- **FR: retained frontier / relatedness to entered fields** (7): CONTACT_REACH, RETAINED_REACH, RETENTION_RATIO_early, FRONTIER_POTENTIAL, D_rca_end, D_vol_end, M0_density_end
- **G: landing on gateway fields** (7): G, G_A, G_btw, G_deg, G_phimin, REL_home, RS
- **S: co-author (social) reach** (3): S_comp, S_comp_n, S_isolated_share

Source: `round-3/experiment-8/src/results/indicator_dictionary.csv` -> `family column (counts per value)`; `round-4/evaluation-3/src/results/partA_derived.json` -> `families.*`

## D-family exclusion (why D_ratio, D_rare and the other D indicators were never frozen)

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] DEV missing share: D_ratio 0.311, D_z 0.311, D_sub 0.311, D_obs 0.311, D_rare 0.883; the DEV eligibility rule excludes indicators with more than 30% missing. Deviation record, verbatim: 'T4 median M = 3.5 (> 3) so the n_ck >= 2 neighbour rule is kept; consequence: D-family indicators (need M >= 3; D_rare M >= 10) are missing for many concepts and may exceed the 30% missing eligibility bound.'

Source: `round-3/experiment-8/src/results/rq1_dev_selection.json` -> `missing.<indicator>`; `round-3/experiment-8/src/results/deviations.json` -> `T4_M_median`
