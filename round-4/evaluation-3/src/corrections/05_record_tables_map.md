# 05 Eval2 record_tables: file -> report section

| file | rows | target section |
|---|---|---|
| `record_tables/coverage_iter2.csv` | 4 | 8a (coverage table, iteration-2 column) |
| `record_tables/coverage_iter2_steps.csv` | 12 | 8a |
| `record_tables/definitions_diff.csv` | 12 | 9 / 11 (frame comparison Exp5 vs Exp6) |
| `record_tables/draft_number_harvest.csv` | 555 | ledger (all sections) |
| `record_tables/frame_crosstab_split_group.csv` | 14 | 9 / 11 (frame comparison) |
| `record_tables/frame_disagreement_causes.csv` | 713 | 9 / 11 (frame comparison) |
| `record_tables/frame_overlap_by_group.csv` | 6 | 9 / 11 (frame comparison) |
| `record_tables/h1_criteria.csv` | 38 | 10.3 (H1 criteria) |
| `record_tables/hypothesis_iter3_numbers.csv` | 35 | 11.2 / 16.x (hypothesis LR, d, strata) |
| `record_tables/lineage_robustness_iter1.csv` | 278 | 3.5 (alternative lineage indicators) |
| `record_tables/next_field_heldout_rows.parquet` | 46,433 | 11.2 (next-field entry, held-out rows) |
| `record_tables/next_field_trace.json` | json | 11.2 (next-field entry trace) |
| `record_tables/o5_associations.csv` | 60 | 20.2 (O5 associations) and file 09 |
| `record_tables/o5_concept_panel.csv` | 12,499 | 20.2 / 13 (O5 panel) |
| `record_tables/o5_coverage_by_group.csv` | 10 | 13.1 (Dataset 2 coverage) |
| `record_tables/o5_coverage_by_group_source.csv` | 130 | 13.1 and file 09 (per-source coverage) |
| `record_tables/o5_handcheck_items.csv` | 100 | 20.3 (O5 hand check) |
| `record_tables/o5_handcheck_items_final.csv` | 100 | 20.3 (O5 hand check) |
| `record_tables/o5_km_cumulative_incidence.csv` | 20 | 20.2 (O5 timing) |
| `record_tables/ordering_mixed.csv` | 159 | 11.3 / 16.3 (ordering MIXED) |
| `record_tables/partial_association_all.csv` | 12 | 4.4 (remaining partial associations) |
| `record_tables/portability_F3.csv` | 34 | 4.3 (portability) |
| `record_tables/refit_bootstrap_iter1.csv` | 14 | 3.3 / 4.2 (refit bootstrap) |

Source: `round-4/evaluation-3/src/results/partA_derived.json` -> `record_tables_rows.<file>` (row counts computed from the files listed)
