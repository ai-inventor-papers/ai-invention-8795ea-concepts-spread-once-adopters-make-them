# Corrections pack, iteration 5: index

Each file is insert-ready; every insert carries `[Correction, iteration 5, from art_...]`. Every number is ledgered in `results/claims_ledger_v4.csv` and re-verified by `verify_ledger_v4.py`. `src/apply_corrections.py` applies the Eval3 pack and then these blocks to a copy of the report (`report_corrected.md`); the per-block record is `results/corrections_applied.csv`.

| file | blocks -> target (action) |
|---|---|
| `01_case_studies_26_4.md` | `26.4_rebuilt` -> `^### 26\.4 ` (replace-section); `26.5_atlas` -> `^### 26\.4 ` (insert-new-section-after) |
| `02_exp11_25a.md` | `25a_exp11` -> `^### 25\.7 ` (insert-new-section-after); `29_deadend_exp11` -> `^## 29\. ` (append-to-section); `28.1_c4` -> `^### 28\.1 ` (append-to-section); `24_counts` -> `^## 24\. ` (append-to-section); `31_counts` -> `Four iterations and sixteen artifacts (fifteen com` (text-replace) |
| `03_exp10_rewrite.md` | `25.1` -> `^### 25\.1 ` (replace-section); `25.2` -> `^### 25\.2 ` (replace-section); `25.4` -> `^### 25\.4 ` (replace-section); `25.7` -> `^### 25\.7 ` (replace-section); `25.8` -> `^### 25\.7 ` (insert-new-section-after); `31.1` -> `1. **Early cooccurrence openness (OPEN) predicts l` (text-prefix) |
| `04_exp12_rewrite.md` | `26.1` -> `^### 26\.1 ` (replace-section); `31.3_caveat` -> `3. **Breadth is driven by exploration, not retenti` (text-prefix); `26.3` -> `^### 26\.3 ` (replace-section); `26.2_pc` -> `^### 26\.2 ` (append-to-section) |
| `05_eval3_application.md` | Eval3 pack `00`-`11` applied; `27.6` replaced by the per-file list |
| `06_section23_restore.md` | `23_restore` -> `^## 23\. ` (replace-section); `16.2_tag` -> `2. **Two stable trajectory classes` (text-append-line) |
| `07_section28_evidence.md` | `28.1_evidence` -> `^### 28\.1 ` (append-to-section); `28.2_survives` -> `^### 28\.2 ` (append-to-section); `31.2_retention` -> `RETENTION_RATIO_early (−0.114), ` (text-replace) |
| `08_exp8_exp10_secondary.md` | `25.5_leads` -> `^### 25\.5 ` (append-to-section); `25.6` -> `^### 25\.6 ` (replace-section); `19.5b_tag` -> `^### 19\.5b ` (append-to-section); `19.7_tag` -> `^### 19\.7 ` (append-to-section); `19.2_pergroup` -> `^### 19\.2 ` (append-to-section) |
| `09_coverage_table_30.md` | `30_table` -> `^## 30\. ` (replace-section) |
| `10_minor_and_refs.md` | `fcr` -> `footprint control rung` (text-replace-all); `27.4_fcr_note` -> `^### 27\.4 ` (append-to-section); `27.3_I2` -> `Higgins I² drops to 0.43 (vs 0.66 over the 6 units` (text-replace); `27.2_label` -> `^### 27\.2 ` (append-to-section) |
| `11_evidence_synthesis.md` | `32_synthesis` -> `^## 31\. ` (insert-new-section-after) |
