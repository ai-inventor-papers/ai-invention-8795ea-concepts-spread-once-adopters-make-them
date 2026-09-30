# 02 Pre-registered predictions P1-P5 (replaces 19.8 and 22.7; corrects dead end 7.4 and Section 4.3)

The draft's 19.8 paraphrases P1-P5 with statements that were never pre-registered (e.g. 'entropy is the single strongest indicator', 'CONTACT_REACH is the strongest single indicator'). The table below quotes the EXACT frozen text (Exp8 frozen_spec.json, key preregistered_predictions, file lines 2960-2964).

## Old text (19.8, verbatim)

> ### 19.8 Preregistered verdicts
>
> | Prediction | Description | Verdict |
> |---|---|---|
> | P1: entropy is the single strongest indicator | entropy raw rho is 0.63-0.85 per group, but several indicators outperform it in PSP | **FAILS** |
> | P2: edge persistence is negatively associated with breadth | pooled PSP = -0.080 [-0.126, -0.033], mean raw rho across 4 groups = -0.128 | **HOLDS** |
> | P3: cooccurrence growth indicators generalise beyond CS | deg_growth and str_growth pooled PSP include zero; new_edge_rate is positive in all 4 groups but CS-specific in dev | **FAILS** |
> | P4: early retention ratio predicts breadth conditional on volume | RETENTION_RATIO_early is confirmed for O2r_m50 but FRONTIER_POTENTIAL (retention × reach) does not add to the baseline minus reach | **FAILS** |
> | P5: CONTACT_REACH is the strongest single indicator for O2r_m50 | CONTACT_REACH pooled PSP +0.213 [0.159, 0.265]; M0_density_end is stronger (+0.375) | **FAILS** |

## New 19.8

[Correction, iteration 4, from art_dFQ6jbgNsR6Q]

| # | exact frozen text | verdict | deciding quantity |
|---|---|---|---|
| P1 | entropy, D_rare, D_ratio, participation, NOV_res: raw Spearman with O2r_m50 > 0 (CI > 0) in >= 3 of 4 held-out groups; AND D_rare, D_ratio, participation, NOV_res: pooled psp|B5 CI upper bound < 0.10 | **FAILS** | raw part: groups with raw CI > 0 = D_rare 2, D_ratio 3, participation 4, NOV_res 4, entropy 4 (of 4); adds-little part: pooled psp CI upper bounds D_rare 0.296, D_ratio 0.132, participation 0.271, NOV_res 0.241 (rule: all < 0.10) |
| P2 | edge_persistence: pooled raw rho and pooled psp with O2r_m50 both < 0 | **HOLDS** | edge_persistence pooled psp -0.080 [-0.126, -0.033]; mean raw rho over 4 groups -0.128 |
| P3 | deg_growth, str_growth, new_edge_rate FAIL held-out: pooled psp CI includes 0 OR sign flip in >= 2 of 4 groups | **FAILS** | new_edge_rate pooled psp +0.118 [+0.072, +0.163], sign flips 0 -> it TRANSFERS; deg_growth +0.002 [-0.046, +0.049] and str_growth +0.001 [-0.058, +0.060] do fail as predicted |
| P4 | RETENTION_RATIO_early and FRONTIER_POTENTIAL: pooled psp > 0 with CI > 0 for O2r_resid AND O1c | **FAILS** | RETENTION_RATIO_early on O2r_resid -0.120 [-0.166, -0.074] (predicted > 0: wrong sign); on O1c -0.006 [-0.041, +0.029]; FRONTIER_POTENTIAL on O2r_resid +0.055 [-0.057, +0.165] |
| P5 | CONTACT_REACH: pooled psp CI includes 0 (also reported given B5 minus reach) | **FAILS** | CONTACT_REACH pooled psp on O2r_m50 +0.213 [+0.159, +0.265] (predicted: CI includes 0); given B5 minus reach on O2r_resid +0.223 [+0.172, +0.273] |

Source: `round-3/experiment-8/src/results/frozen_spec.json` -> `preregistered_predictions.P1..P5`; `round-3/experiment-8/src/results/prereg_verdicts.json` -> `P1..P5.{verdict,detail,...}`

Reading: P1 fails on BOTH parts (D_rare is positive in fewer than 3 groups, and all four breadth candidates add more than the 0.10 bound). P3 was a prediction of FAILURE; its failure means new_edge_rate transfers to held-out groups. P4 fails because the retention ratio has the opposite sign. P5 predicted that CONTACT_REACH adds nothing; it adds a clearly positive amount.

## Correction to dead end 7.4 (Section 7, item 4)

> 4. **Raw cooccurrence growth indicators.** Degree growth, strength growth and new edge rate growth are specific to Computer Science: positively correlated with rarefied breadth in Computer Science (rho 0.45 to 0.47) and near zero or negative in the other three groups (with the exception of new_edge_rate in Medicine at 0.35). They are growth confounded (Spearman with publication growth > 0.70).

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] The held-out test contradicts 'specific to Computer Science' for new_edge_rate: pooled psp given B5 +0.118 [+0.072, +0.163] with 0 sign flips across the 4 held-out groups. Degree and strength growth do fail held-out (CIs include 0).

## Correction to Section 4.3

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] Append: 'On held-out groups (Exp8), new_edge_rate transfers beyond B5 (pooled psp +0.118), whereas participation +0.150, NOV_res +0.139, D_rare +0.162 and D_ratio +0.066 are small but positive, so the iteration-1 conclusion that none adds to B5 does not hold on held-out data.'

## Old text (dead end 22.7, verbatim)

> 7. **Four of five preregistered predictions fail.** Entropy is not the single strongest indicator (prediction 1, "entropy is the strongest single indicator," fails; M0_density_end and D_vol_end are stronger). Cooccurrence growth indicators do not generalise beyond CS (prediction 3, "cooccurrence growth indicators generalise," fails). FRONTIER_POTENTIAL does not add to the baseline minus reach (prediction 4, "early retention ratio predicts breadth conditional on volume," fails). CONTACT_REACH is not the strongest single indicator (prediction 5, "CONTACT_REACH is the strongest single indicator," fails; M0_density_end is stronger).

## New dead end 22.7

[Correction, iteration 4, from art_dFQ6jbgNsR6Q] 7. **Four of five pre-registered predictions fail, as frozen.** P2 (edge_persistence negative) holds. P1 fails (the iteration-1 breadth candidates do add beyond B5 on held-out data); P3 fails because new_edge_rate transfers; P4 fails because RETENTION_RATIO_early is negative, not positive; P5 fails because CONTACT_REACH is positive given B5. See the table in 19.8 for the deciding numbers.

## Held-out table: iteration-1 candidates (O2r_m50)

[Correction, iteration 4, from art_dFQ6jbgNsR6Q]

| indicator | pooled psp given B5 | 95% CI | raw rho PHYS | LIFEENV | SOC | MATHDEC |
|---|---|---|---|---|---|---|
| D_ratio | +0.066 | [+0.001, +0.132] | +0.066 | +0.089 | +0.218 | +0.500 |
| D_rare | +0.162 | [+0.022, +0.296] | +0.305 | +0.128 | +0.374 | n/a (n too small) |
| participation | +0.150 | [+0.025, +0.271] | +0.306 | +0.154 | +0.331 | +0.687 |
| NOV_res | +0.139 | [+0.033, +0.241] | +0.277 | +0.078 | +0.239 | +0.722 |
| entropy | n/a (B5 member) | n/a | +0.775 | +0.631 | +0.639 | +0.847 |
| edge_persistence | -0.080 | [-0.126, -0.033] | -0.076 | -0.112 | -0.107 | -0.217 |

Source: `round-3/experiment-8/src/results/prereg_verdicts.json` -> `P1.detail.<ind>.{pooled_psp,pooled_ci,raw_rho.<group>}`; `round-3/experiment-8/src/results/prereg_verdicts.json` -> `P2.{pooled_psp,pooled_ci,raw_rho}`
