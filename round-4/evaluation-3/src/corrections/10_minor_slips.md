# 10 Minor slips

## 19.6 cross-reference

> No indicator predicts external recognition. All Holm p = 1.0. This is consistent with the Evaluation 2 finding that external recognition is unrelated to publication outcomes (Section 21.2).

[Correction, iteration 4, from art_7W9xiIO3FVBs] Replace 'Section 21.2' with 'Section 20.2' (the O5 validation result is Section 20.2, External recognition validation; 21.2 is 'Missing rivals').

## 18.11 home-field mismatch sentence

> - The primary sample is the Experiment 5 frame minus Experiment 6 (by ID, QID and label), not a fully independent draw; 7 home field mismatches were found (17 of 11,841 concepts).

[Correction, iteration 4, from art_22ppE1snfHKj] Replace with: 'The primary sample is the Experiment 5 frame minus Experiment 6 (by ID, QID and label), not a fully independent draw. Home fields disagree with Exp5's for 22 concepts (5 DEV, 17 held-out; held-out home agreement 0.9977).'

Source: `3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/step2_dev.json` -> `input_checks.home_mismatch_cidx (length)`; `3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/step2_heldout.json` -> `input_checks.home_mismatch_cidx (length); input_checks.home_agreement`

## M0_density_end +0.375 vs +0.377 (source note for 19.2)

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] Both numbers are correct but refer to different outcomes: +0.375 is O2r_m50 (the 19.2 table and README), +0.377 is O2r_resid (the Exp8 summary headline). Add to 19.2: 'Source: heldout_summary.json -> O2r_m50[indicator=M0_density_end].pooled; the headline +0.377 is O2r_resid.'

Source: `3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/heldout_summary.json` -> `O2r_m50[0].pooled`; `3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/heldout_summary.json` -> `O2r_resid[0].pooled`
