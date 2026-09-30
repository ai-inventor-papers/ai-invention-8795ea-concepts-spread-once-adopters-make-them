# 05 Evaluation 3 corrections pack: application record

Mapping (file, block, target heading, action) is the explicit list `EVAL3_MAP` in `src/apply_corrections.py`, derived from Eval3 `corrections/00_index.md`. Status per block:

| source file | block | target | action | status | reason |
|---|---|---|---|---|---|
| `01_exp8_outcomes_relabel.md` | `New 19.4 O1c (sustained uptake)` | `^### 19\.4 ` | replace-section | ALREADY_PRESENT | `first sentence already in iter-5 report: 'Only n_authors_early is confirmed for O1c: pooled '` |
| `01_exp8_outcomes_relabel.md` | `New 19.5 O4 (field- and year-normalised citation growth): 2 of 10 confirmed` | `^### 19\.5 ` | replace-section | APPLIED | `section replaced` |
| `01_exp8_outcomes_relabel.md` | `New 19.5b O3 (transience): 1 of 10 confirmed` | `^### 19\.5b ` | replace-section | ALREADY_PRESENT | `first sentence already in iter-5 report: 'For transience (O3, binary; groups with an estimab'` |
| `01_exp8_outcomes_relabel.md` | `New 19.6 External recognition (O5, O5_WW): 0 and 0 of 10 confirmed` | `^### 19\.6 ` | replace-section | APPLIED | `section replaced` |
| `01_exp8_outcomes_relabel.md` | `New 19.7 Learned models vs B5 vs B5 + best single (held-out groups pooled)` | `^### 19\.7 ` | replace-section | ALREADY_PRESENT | `first sentence already in iter-5 report: 'All 8 outcomes; Spearman(pred, y) for continuous o'` |
| `01_exp8_outcomes_relabel.md` | `O3 as a positive held-out result` | `^### 19\.5b ` | append-to-section | APPLIED | `appended at end of section` |
| `01_exp8_outcomes_relabel.md` | `New dead end 22.6` | `^## 22\. ` | append-to-section | APPLIED | `appended at end of section` |
| `02_prereg_P1_P5.md` | `New 19.8` | `^### 19\.8 ` | replace-section | APPLIED | `section replaced` |
| `02_prereg_P1_P5.md` | `Correction to dead end 7.4 (Section 7, item 4)` | `^## 7\. ` | append-to-section | ALREADY_PRESENT | `first sentence already in iter-5 report: '4. **Raw cooccurrence growth indicators.** Degree '` |
| `02_prereg_P1_P5.md` | `Correction to Section 4.3` | `^### 4\.3 ` | append-to-section | APPLIED | `appended at end of section` |
| `02_prereg_P1_P5.md` | `New dead end 22.7` | `^## 22\. ` | append-to-section | APPLIED | `appended at end of section` |
| `02_prereg_P1_P5.md` | `Held-out table: iteration-1 candidates (O2r_m50)` | `^### 19\.8 ` | append-to-section | APPLIED | `appended at end of section` |
| `03_exp7_tables.md` | `18.5 Volume-matched contrast (retained R vs entered-not-retained N, same current x cumulative volume cell)` | `^### 18\.5 ` | append-to-section | APPLIED | `appended at end of section` |
| `03_exp7_tables.md` | `18.4 Dose by persistence age (held-out pooled 4)` | `^### 18\.4 ` | append-to-section | APPLIED | `appended at end of section` |
| `03_exp7_tables.md` | `18.9 Abandonment penalty d_lost: A1 vs R4 and variants (held-out pooled 4)` | `^### 18\.9 ` | append-to-section | APPLIED | `appended at end of section` |
| `03_exp7_tables.md` | `18.3 d0_ret_rel with three resampling units (held-out pooled 4, R3)` | `^### 18\.3 ` | append-to-section | APPLIED | `appended at end of section` |
| `03_exp7_tables.md` | `18.6 Held-out sensitivities of d0 (R3)` | `^### 18\.6 ` | append-to-section | APPLIED | `appended at end of section` |
| `03_exp7_tables.md` | `New subsection 18.6a Proximity dependence` | `^### 18\.6 ` | insert-new-section-after | APPLIED | `new section inserted after target section` |
| `03_exp7_tables.md` | `Step-3 comparison: Exp7 D_rca_pers vs Research 2 D_rca_persist_k` | `^### 18\.1 ` | append-to-section | APPLIED | `appended at end of section` |
| `03_exp7_tables.md` | `Nearest-neighbour paragraph (draft for Section 18.1 / Related work)` | `^### 18\.1 ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `10.3 H1 criteria (blocking)` | `^### 10\.3 ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `11.3 / 16.3 Ordering -> MIXED (blocking)` | `^### 11\.3 ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `10.6 / 16.5 H3 (blocking)` | `^### 10\.6 ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `10.7 Power attribution and MDE wording (blocking)` | `^### 10\.7 ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `5.4 The 'B5 + all_four' row (blocking)` | `^### 5\.4 ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `13.1 Dataset 2 coverage counts (blocking)` | `^### 13\.1 ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `8a Coverage table, iteration-2 column (blocking)` | `^## 8a\. ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `4.4 Remaining partial associations (blocking)` | `^### 4\.4 ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `11.2 / hypothesis LR, d and strata clashes` | `^### 11\.2 ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `16.1 'positive in all three evaluable groups'` | `^## 16\. ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `10.5 Relatedness pair is held-out only` | `^### 10\.5 ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `11.5 Trajectory robustness` | `^### 11\.5 ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `New: frame comparison (Exp5 vs Exp6) for Section 9/11` | `^## 9\. ` | append-to-section | APPLIED | `appended at end of section` |
| `04_eval2_text_corrections.md` | `New: O5 external recognition status (13 / 16 Open)` | `^### 13\.2 ` | append-to-section | APPLIED | `appended at end of section` |
| `05_record_tables_map.md` | `(whole file) 05_record_tables_map.md` | `^### 20\.1 ` | append-to-section | APPLIED | `appended at end of section` |
| `06_ledger_open_rows.md` | `(whole file) 06_ledger_open_rows.md` | `^### 20\.1 ` | append-to-section | APPLIED | `appended at end of section` |
| `07_failed_artifacts.md` | `New Section 22b (or addition to 5a): Experiment 9 did not run` | `^## 22a\. ` | insert-new-section-after | APPLIED | `new section inserted after target section` |
| `07_failed_artifacts.md` | `Iteration counts (from each artifact's .aii_worker_result.json)` | `^## 24\. ` | append-to-section | APPLIED | `appended at end of section` |
| `07_failed_artifacts.md` | `Artifact id placeholders -> real ids` | `^## 24\. ` | append-to-section | APPLIED | `appended at end of section` |
| `08_candidate_S_and_families.md` | `Candidate S (co-author reach; Cheng et al. 2023) on held-out groups` | `^### 19\.1 ` | append-to-section | APPLIED | `appended at end of section` |
| `08_candidate_S_and_families.md` | `New 19.1 family list` | `^### 19\.1 ` | append-to-section | APPLIED | `appended at end of section` |
| `08_candidate_S_and_families.md` | `D-family exclusion (why D_ratio, D_rare and the other D indicators were never frozen)` | `^### 19\.1 ` | append-to-section | APPLIED | `appended at end of section` |
| `09_o5_leakage.md` | `(whole file) 09_o5_leakage.md` | `^### 20\.2 ` | append-to-section | APPLIED | `appended at end of section` |
| `10_minor_slips.md` | `19.6 cross-reference` | `^### 19\.6 ` | append-to-section | APPLIED | `appended at end of section` |
| `10_minor_slips.md` | `18.11 home-field mismatch sentence` | `^### 18\.11 ` | append-to-section | ALREADY_PRESENT | `first sentence already in iter-5 report: 'The primary sample is the Experiment 5 frame minus'` |
| `10_minor_slips.md` | `M0_density_end +0.375 vs +0.377 (source note for 19.2)` | `^### 19\.2 ` | append-to-section | APPLIED | `appended at end of section` |
| `11_boundary_results.md` | `(whole file) 11_boundary_results.md` | `^### 19\.9 ` | insert-new-section-after | APPLIED | `new section inserted after target section` |
| `01_exp8_outcomes_relabel.md` | `Old text (19.5, verbatim)` | `-` | none | NOT_APPLIED_SUPERSEDED | `verbatim quote of the old draft text, kept in Eval3 file as evidence; the matching 'New' block is applied instead` |
| `01_exp8_outcomes_relabel.md` | `Old text (dead end 22.6, verbatim)` | `-` | none | NOT_APPLIED_SUPERSEDED | `verbatim quote of the old draft text, kept in Eval3 file as evidence; the matching 'New' block is applied instead` |
| `02_prereg_P1_P5.md` | `Old text (19.8, verbatim)` | `-` | none | NOT_APPLIED_SUPERSEDED | `verbatim quote of the old draft text, kept in Eval3 file as evidence; the matching 'New' block is applied instead` |
| `02_prereg_P1_P5.md` | `Old text (dead end 22.7, verbatim)` | `-` | none | NOT_APPLIED_SUPERSEDED | `verbatim quote of the old draft text, kept in Eval3 file as evidence; the matching 'New' block is applied instead` |
| `08_candidate_S_and_families.md` | `Old text (19.1 family list, verbatim)` | `-` | none | NOT_APPLIED_SUPERSEDED | `verbatim quote of the old draft text, kept in Eval3 file as evidence; the matching 'New' block is applied instead` |
| `01_case_studies_26_4.md` | `26.4_rebuilt` | `^### 26\.4 ` | replace-section | APPLIED | `section replaced` |
| `01_case_studies_26_4.md` | `26.5_atlas` | `^### 26\.4 ` | insert-new-section-after | APPLIED | `new section inserted after target section` |
| `02_exp11_25a.md` | `25a_exp11` | `^### 25\.7 ` | insert-new-section-after | APPLIED | `new section inserted after target section; new ## 25a placed after 25.7 (before Section 26)` |
| `02_exp11_25a.md` | `29_deadend_exp11` | `^## 29\. ` | append-to-section | APPLIED | `appended at end of section` |
| `02_exp11_25a.md` | `28.1_c4` | `^### 28\.1 ` | append-to-section | APPLIED | `appended at end of section` |
| `02_exp11_25a.md` | `24_counts` | `^## 24\. ` | append-to-section | APPLIED | `appended at end of section` |
| `02_exp11_25a.md` | `31_counts` | `Four iterations and sixteen artifacts (fifteen commissioned, twelve completed; t` | text-replace | APPLIED | `text-replace (1 occurrence(s))` |
| `03_exp10_rewrite.md` | `25.1` | `^### 25\.1 ` | replace-section | APPLIED | `section replaced` |
| `03_exp10_rewrite.md` | `25.2` | `^### 25\.2 ` | replace-section | APPLIED | `section replaced` |
| `03_exp10_rewrite.md` | `25.4` | `^### 25\.4 ` | replace-section | APPLIED | `section replaced` |
| `03_exp10_rewrite.md` | `25.7` | `^### 25\.7 ` | replace-section | APPLIED | `section replaced` |
| `03_exp10_rewrite.md` | `25.8` | `^### 25\.7 ` | insert-new-section-after | APPLIED | `new section inserted after target section` |
| `03_exp10_rewrite.md` | `31.1` | `1. **Early cooccurrence openness (OPEN) predicts later cross field breadth on a ` | text-prefix | APPLIED | `text-prefix (1 occurrence(s))` |
| `04_exp12_rewrite.md` | `26.1` | `^### 26\.1 ` | replace-section | APPLIED | `section replaced` |
| `04_exp12_rewrite.md` | `31.3_caveat` | `3. **Breadth is driven by exploration, not retention.**` | text-prefix | APPLIED | `text-prefix (1 occurrence(s))` |
| `04_exp12_rewrite.md` | `26.3` | `^### 26\.3 ` | replace-section | APPLIED | `section replaced` |
| `04_exp12_rewrite.md` | `26.2_pc` | `^### 26\.2 ` | append-to-section | APPLIED | `appended at end of section` |
| `06_section23_restore.md` | `23_restore` | `^## 23\. ` | replace-section | APPLIED | `section replaced` |
| `06_section23_restore.md` | `16.2_tag` | `2. **Two stable trajectory classes` | text-append-line | APPLIED | `text-append-line (1 occurrence(s))` |
| `07_section28_evidence.md` | `28.1_evidence` | `^### 28\.1 ` | append-to-section | APPLIED | `appended at end of section` |
| `07_section28_evidence.md` | `28.2_survives` | `^### 28\.2 ` | append-to-section | APPLIED | `appended at end of section` |
| `07_section28_evidence.md` | `31.2_retention` | `RETENTION_RATIO_early (−0.114), ` | text-replace | APPLIED | `text-replace (1 occurrence(s))` |
| `08_exp8_exp10_secondary.md` | `25.5_leads` | `^### 25\.5 ` | append-to-section | APPLIED | `appended at end of section` |
| `08_exp8_exp10_secondary.md` | `25.6` | `^### 25\.6 ` | replace-section | APPLIED | `section replaced` |
| `08_exp8_exp10_secondary.md` | `19.5b_tag` | `^### 19\.5b ` | append-to-section | APPLIED | `appended at end of section` |
| `08_exp8_exp10_secondary.md` | `19.7_tag` | `^### 19\.7 ` | append-to-section | APPLIED | `appended at end of section` |
| `08_exp8_exp10_secondary.md` | `19.2_pergroup` | `^### 19\.2 ` | append-to-section | APPLIED | `appended at end of section` |
| `09_coverage_table_30.md` | `30_table` | `^## 30\. ` | replace-section | APPLIED | `section replaced` |
| `10_minor_and_refs.md` | `fcr` | `footprint control rung` | text-replace-all | APPLIED | `text-replace-all (1 occurrence(s))` |
| `10_minor_and_refs.md` | `27.4_fcr_note` | `^### 27\.4 ` | append-to-section | APPLIED | `appended at end of section` |
| `10_minor_and_refs.md` | `27.3_I2` | `Higgins I² drops to 0.43 (vs 0.66 over the 6 units)` | text-replace | APPLIED | `text-replace (1 occurrence(s))` |
| `10_minor_and_refs.md` | `27.2_label` | `^### 27\.2 ` | append-to-section | APPLIED | `appended at end of section` |
| `11_evidence_synthesis.md` | `32_synthesis` | `^## 31\. ` | insert-new-section-after | APPLIED | `new section inserted after target section` |
| `05_eval3_application.md` | `27.6_list` | `^### 27\.6 ` | replace-section | APPLIED | `section replaced` |

The Section 27.6 replacement is the per-file summary of this table.

Evaluation 3 Step 3 is recorded: D_rca_persist_k rival untested; Exp7 D_rca_pers is a different construct (max rho 0.877, drca_persist_comparison.json).
