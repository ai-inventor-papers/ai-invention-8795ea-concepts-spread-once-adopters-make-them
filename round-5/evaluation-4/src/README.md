# Evaluation 4 (iteration 5): fix the record and pool the openness evidence

This folder runs the plan in `iter_5/gen_plan/gen_plan_evaluation_1`. It uses no new data and spends $0 on LLMs and
no OpenAlex credit. It does three jobs:

1. It clears the ten BLOCKING reviewer items as insert-ready correction blocks (`corrections_iter5/`) and applies them,
   together with Evaluation 3's corrections pack, to a copy of the report (`report_corrected.md`).
2. It re-verifies every number against its source file. The v3 ledger is re-checked, and a new v4 ledger with 1,769
   rows covers every number in the new blocks.
3. It pools the home-only openness evidence across every body scored so far. This synthesis is descriptive and is
   labelled by design status.

## Headline results

| check | result |
|---|---|
| MUST-FIX items cleared | **10 / 10** |
| Gate G0 (inputs exist, sha256 in `results/inputs_manifest.json`) | pass |
| Gate G1 (EXP5 OPEN_home psp vs Exp10 README line 102) | pass: R0 +0.099, R2 +0.076; HOME NOV_res and edge_persistence match |
| Gate G2 (cohort OPEN_home vs Exp10) | pass: R2 +0.091 [+0.013, +0.171] reproduced exactly with Exp10's seed; seed 0 CI within ±0.005; R3 +0.080 |
| Gate G3 (Eval3 ledger re-verified) | pass: 1,290 rows, 0 MISMATCH, 0 NOT_FOUND, 9 orphans (identical to Eval3) |
| Ledger v4 | 1,769 rows: 0 MISMATCH, 0 NOT_FOUND, 0 orphans, 0 verifier disagreements |
| Text presence in `report_corrected.md` | v4: 1,769 / 1,769 in their target section. v3: 1,244 in the target section, 43 elsewhere in the report, 3 absent (`results/text_absent_rows.csv`) |
| Stale strings | 0. One correction note names the deleted 26.4 sentence, as the plan requires; it is counted separately |
| Verbatim checks | 7 / 7 byte-identical: Section 23, PR1, PR1b, PR2, PR3, Exp11 H-M1..H-P1, Exp10 "Leads replicated" |
| Correction blocks | 76 APPLIED, 5 ALREADY_PRESENT, 5 NOT_APPLIED_SUPERSEDED (old-text quotes), 0 target missing |
| References | 120 de-duplicated entries (18 cited in the text); 10 unverified items listed as excluded |
| Independent audit (`audit.py`, no shared code) | all 14 body × index psp cells reproduced (max diff 1.9e-16); pools +0.068 / +0.105; shuffled-feature placebo pool +0.021 [-0.010, +0.051], which includes 0 |

**Evidence synthesis** (`results/evidence_synthesis.json`, `figures/evidence_forest.png|pdf`, new report
Section 32). Outcome O2r_m50, rung R2. Pooling is DerSimonian-Laird on Fisher z, with HKSJ intervals.

| index | non-selection pool | DL CI | HKSJ CI | I2 | sign agreement | selection body (DEV) | shrinkage |
|---|---|---|---|---|---|---|---|
| OPEN_home (k=6: 4 held-out groups, 2010-14 cohort, 2015-17 cohort) | +0.069 | [+0.038, +0.100] | [+0.042, +0.096] | 0.00 | 6/6 | +0.109 | 1.58 |
| NOVCHURN_home (k=5; the 2015-17 cohort is a selection body for this index) | +0.105 | [+0.069, +0.140] | [+0.078, +0.131] | 0.00 | 5/5 | +0.116 | 1.11 |

Reading: the association is small, has the same sign in every body, and is about 1.6 times larger on the selection
body than in the non-selection pool. All non-selection bodies except the 2015-17 cohort had already been unsealed and
reused. The pool is therefore not a confirmation, and it is not a forecast gain (the frozen B5 + OPEN_home forecast
gains +0.002 [-0.003, +0.008]). The Frame-N row is empty: this iteration's confirmation artifact will be compared
with this pool, not pooled into it.

## What was corrected (report sections)

- **26.4** rebuilt from `case_pairs.json`: 7 pairs. The 5 invented rows and the "GPU computing and deep learning"
  sentence are deleted with an explicit note. New **26.5** holds the 37-concept AI atlas, labelled retrospective and
  outcome-selected.
- New **25a**: Experiment 11 (incomplete). It holds the verbatim pre-registration, the DEV FE table and the verdict
  NOT SUPPORTED, and says what did not run, as read from the logs (event study died on an OpenBLAS thread error; held-out bodies and
  H-S1/H-P1 were not run). The dead end is added to 29, the C4 note to 28.1, and the artifact counts, derived from
  disk, to 24 and 31: 20 commissioned, 16 completed, 4 failed.
- **25.1/25.2/25.4/25.7** rewritten and **25.8** added (Exp10). The rewrite shows the full R0-R5 ladder, states that
  R4/R5 and the DL pool include 0, reports no forecasting gain, notes that the planted control was not recovered, and
  labels OPEN_all as mechanically coupled.
- **26.1/26.3** rewritten, with a PC table added to 26.2 (Exp12). PR1-PR3 are quoted verbatim with their verdicts.
  The decomposition is labelled an identity, not a causal split. The sequence tables show MIXED / HOME-FIRST only on
  held-out data, and intersection-born concepts take off later (HR < 1).
- **23** restored byte-for-byte from the iteration-4 report, with three correction tags. **16.2** is tagged.
- **28.1/28.2**: evidence for and against C1-C4, and what survives beyond Cheng 2023 / Maillart 2026.
  RETENTION_RATIO_early is moved to "does not survive type controls".
- **25.5/25.6/19.2/19.5b/19.7**: the Leads block is quoted verbatim; the O3 learned-model row now reads evaluable and
  null (−0.021 [−0.130, +0.101]); the per-group EXP8 table carries † marks.
- **30**: the coverage table is corrected cell by cell, with a change log. **27.2/27.3/27.4** get the spec curve
  relabelled "exploratory, all-papers build", I2 labelled by model, and "R3 rung" used throughout.
- **27.6** is replaced by the audit list generated from `results/corrections_applied.csv`.
- **References**: one cumulative list with an old->new number map (`references_master.md`). In-text `[n]` citations
  are renumbered.

## Layout

```
eval.py                     driver: runs src/* in order, then assembles eval_out.json (+ full/mini/preview)
src/synthesis.py            gates G1/G2 + item 11 (vendor/ladder.py, vendor/rq1stats.py = Exp10 code, verbatim)
src/build_corrections.py    items 1-4, 6-11 -> corrections_iter5/*.md, results/claims_ledger_v4.csv
src/apply_corrections.py    item 5 (explicit EVAL3_MAP) + iteration-5 blocks -> report_corrected.md
src/refs.py                 cumulative reference list, in-text renumbering
src/figures.py              forest plot (aii-data-fig-gen house style, hand-written: asymmetric CIs)
src/checks.py               ledger v3/v4 verification, text presence, stale strings, verbatim diffs
src/ledger.py, src/paths.py helpers
verify_ledger_v4.py         COPY of Eval3 verify_ledger.py, repointed by CLI args (+ a 'lines:a-b' carry form)
corrections_iter5/          00_index.md + 01..11 insert-ready blocks
report_corrected.md         corrected copy of iter_5/gen_strat/current_report.md
references_master.json|md   cumulative references
results/                    gates, ledgers, verification, evidence synthesis, corrections_applied.csv, per_group_table.csv
figures/evidence_forest.*   forest plot
```

## How to run

```bash
uv sync
uv run eval.py            # ~2 min on 4 CPUs; add --assemble-only to rebuild eval_out.json only
uv run audit.py           # independent re-derivation + placebos -> results/audit.json
```

The inputs are read, read-only, from the run's earlier artifacts. They are found from this folder's position in the
run tree, or from `AII_RUN_ROOT`; `reproducibility.md` maps each input to its artifact id.

## Deviations from the plan

- The bootstrap seed is Exp10's frozen 20260929, not 0, so that every CI can be compared with the record. G2 was also
  run with seed 0 and passes.
- DL pools on Fisher z, as the plan says. Exp10 pooled raw psp.
- The AI atlas comes from `atlas.json -> concepts`, because `ai_atlas/table.csv` is a per-measure table. The
  OPEN~PC1/PC2 table comes from the trajectories files, because `open_diagnostics.json` holds no PC table.
- Reference de-duplication matches on the title head (before ':' or '?', first 5 words) and adds a prefix pass,
  because the end-of-report list abbreviates titles. One possible remaining duplicate is Lockwood 2005, which appears
  with two different titles.
- An Eval3 block is marked ALREADY_PRESENT only when at least 90% of its numbers are already in the report. Partly
  applied blocks are appended in full with a note.
- The review's "Exp8 raw sign flip +0.143 / −0.126" is in no file (NOT_FOUND). It is not used, and 28.1 cites the
  file-backed consolidation numbers instead.

## What is NOT claimed

- No new confirmation. The pooled estimate is descriptive and mostly uses already-unsealed bodies.
- NOVCHURN_home on the 2015-17 cohort is a selection estimate.
- The ledger checks numbers against files, not the reasoning around them. A correct number attached to a wrong claim
  would pass. The verbatim and text-presence checks reduce this risk but do not remove it.
- The 3 v3 values absent from the report (`results/text_absent_rows.csv`) belong to Eval3 blocks that the strategist
  had already applied with at least 90% of their numbers. They were not re-inserted.

## Restoring removed files

No files were removed. `.venv/` is regenerable with `uv sync`.
