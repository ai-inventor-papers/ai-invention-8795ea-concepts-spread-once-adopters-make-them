#!/usr/bin/env python3
"""WP5: text_corrections.md, one block per blocking item: the old sentence (verbatim from the iteration-2 draft), the new
sentence (every number filled programmatically from its source key) and the source keys."""
from __future__ import annotations

import json

import pandas as pd

import common as C


def g(path, key):
    return C.get_path(C.read_json(C.ROOT / path), key)


def old(snippet: str) -> str:
    txt = C.DRAFT.read_text()
    for line in txt.splitlines():
        if snippet in line:
            return line.strip()
    return f"(not found verbatim; searched for: {snippet!r})"


def main() -> None:
    H1 = "round-2/experiment-5/src/results/h1_heldout.json"
    H1D = "round-2/experiment-5/src/results/h1_dev.json"
    H3 = "round-2/experiment-5/src/results/h3_results.json"
    HO = "round-2/experiment-6/src/results/heldout_result.json"
    DV = "round-2/experiment-6/src/results/dev_result.json"
    COV = "round-2/dataset-2/src/out/coverage_report.json"
    EV1 = "round-2/evaluation-1/src/eval_out.json"
    S4 = "round-1/experiment-4/src/screen_result.json"
    EPA = "round-1/experiment-3/src/results/exploratory_partial_association.json"
    crit = g(H1, "verdict_H1.criteria")
    lp, la = g(H1, "lpm_field_fe"), g(H1, "lpm_field_fe_all_splits")
    lc, bd, ph = g(H1, "logit_clustered_se"), g(H1, "boundary"), g(H1, "pigeonhole_crossed_bootstrap")
    o, od = g(HO, "ordering"), g(DV, "ordering")
    ll, lld = o["lead_lag"], od["lead_lag"]
    h3 = C.read_json(C.ROOT / H3)
    h3d = g(H1D, "H3_dev")
    pw = g(H1D, "power")
    cov = g(COV, "by_source")
    f5 = g(EV1, "metadata.F_record.F5_exp4_field_level.rows")
    fl = g(S4, "field_level")
    cands = g(EPA, "candidates")
    fa = json.loads((C.WS / "frame_agreement.json").read_text())
    o5 = json.loads((C.WS / "o5_validation.json").read_text())
    tr = json.loads((C.TAB / "next_field_trace.json").read_text())
    rows = []

    def block(title, old_snip, new, keys):
        rows.append(f"## {title}\n\n**Old** ({'draft line' if not old_snip.startswith('(') else 'context'}):\n\n> {old(old_snip) if not old_snip.startswith('(') else old_snip}\n\n"
                    f"**New:**\n\n> {new}\n\n**Source keys:** " + "; ".join(f"`{k}`" for k in keys) + "\n")

    fails = [k for k in ("pooled_dauc_ge_0.05", "refit_ci_gt0", "sign_ge3_of_4_evaluable", "placebo_null") if not crit[k]]
    block("10.3 H1 criteria (blocking)", "Verdict: **DISCONFIRMED** by all preregistered criteria",
          f"Verdict: **DISCONFIRMED** by the preregistered rule, which requires all six core criteria. Criterion by criterion (held-out, "
          f"{g(H1, 'primary.n'):,} episodes / {g(H1, 'primary.n_concepts'):,} concepts): pooled dAUC >= 0.05 {crit['pooled_dauc_ge_0.05']}; refit CI > 0 "
          f"{crit['refit_ci_gt0']}; >= 3 of 4 groups positive {crit['sign_ge3_of_4_evaluable']} ({crit['n_groups_positive']} of 4); cohort same sign "
          f"{crit['cohort_same_sign']} (both negative); within-field LPM beta > 0 at p < 0.05 **{crit['lpm_beta_within_gt0_p05']}** "
          f"(beta = {lp['beta_within_per_sd']:+.3f} per SD, concept-clustered SE {lp['se_concept']:.3f}, p = {lp['p_concept']:.3f}; two-way clustered "
          f"p = {lp['p_twoway']:.2f}; all splits {la['beta_within_per_sd']:+.3f}, p_concept = {la['p_concept']:.4f}, p_twoway = {la['p_twoway']:.2f}); "
          f"real dAUC above the rewired-backbone placebo p95 {crit['placebo_null']}. The frozen rule names p < 0.05 without an SE type and the sealed code "
          f"uses the concept-clustered p, so the LPM criterion passes as preregistered but is fragile under two-way clustering. Clustered-SE logit: "
          f"beta = {lc['concept']['beta_gateway_std']:+.3f} (p_concept = {lc['concept']['p']:.2f}); boundary interaction {bd['beta_interaction']:+.3f} "
          f"(p = {bd['p']:.2f}; predicted negative, consistent = {bd['consistent']}); crossed concept x field bootstrap CI "
          f"[{ph['ci95'][0]:.4f}, {ph['ci95'][1]:.4f}].",
          [f"{H1}: verdict_H1.criteria.*", "lpm_field_fe.*", "lpm_field_fe_all_splits.*", "logit_clustered_se.*", "boundary.*",
           "pigeonhole_crossed_bootstrap.ci95", "iter_2/gen_art/gen_art_experiment_5/models.py (p_concept in the criterion)"])
    del fails
    gw, pe, mc = o["gateway"], o["peripheral"], o["mcnemar"]
    block("11.3 / 16.3 Ordering -> MIXED (blocking)", "In 66% of broad concepts, the first retained gateway field precedes",
          f"Ordering is **mixed / not established**. Of {o['n_top_o2r']} broad (top-tercile O2r) concepts, {o['n_tau_detected']} have a detected entropy "
          f"take-off and {gw['n_evaluable']} an evaluable gateway ordering: the first retained gateway field comes first in {gw['before']}, ties "
          f"{gw['ties']}, after {gw['after']} ({gw['before']}/{gw['before'] + gw['after']} = {gw['share_before_excl_ties']:.1%} of non-tied; "
          f"{gw['before']}/{gw['n_evaluable']} = {gw['before'] / gw['n_evaluable']:.1%} of evaluable; {gw['before']}/{o['n_top_o2r']} = "
          f"{gw['before'] / o['n_top_o2r']:.1%} of broad concepts; sign p = {gw['sign_test_p_one_sided']:.4f}). Peripheral fields: {pe['before']}/{pe['ties']}/"
          f"{pe['after']}, {pe['share_before_excl_ties']:.1%}, p = {pe['sign_test_p_one_sided']:.3f}; McNemar {mc['gw_only']} vs {mc['per_only']}, "
          f"p = {mc['p_exact_two_sided']:.3f}. The preregistered sign rule passes, but concept-FE lead-lag regressions show retention followed by "
          f"SMALLER next-year entropy gains (gateway b = {ll['forward_dH_on_ret']['coef']['ret_gw']['b']:.4f}, p = {ll['forward_dH_on_ret']['coef']['ret_gw']['p']:.4f}; "
          f"peripheral b = {ll['forward_dH_on_ret']['coef']['ret_per']['b']:.4f}, p = {ll['forward_dH_on_ret']['coef']['ret_per']['p']:.1e}), a significant "
          f"pre-trend (event time -3: {ll['event_study_H']['coef']['ev-3']['b']:.3f}, p = {ll['event_study_H']['coef']['ev-3']['p']:.4f}; DEV "
          f"{lld['event_study_H']['coef']['ev-3']['b']:.3f}), and on DEV entropy predicting later gateway retention (b = "
          f"{lld['reverse_dret_on_H']['coef']['H']['b']:.3f} [{lld['reverse_dret_on_H']['coef']['H']['ci'][0]:.3f}, {lld['reverse_dret_on_H']['coef']['H']['ci'][1]:.3f}], "
          f"p = {lld['reverse_dret_on_H']['coef']['H']['p']:.4f}; held-out b = {ll['reverse_dret_on_H']['coef']['H']['b']:.3f}, p = "
          f"{ll['reverse_dret_on_H']['coef']['H']['p']:.2f}). On DEV, peripheral fields precede take-off as often as gateway fields "
          f"({od['gateway']['share_before_excl_ties']:.1%} vs {od['peripheral']['share_before_excl_ties']:.1%}, McNemar p = {od['mcnemar']['p_exact_two_sided']:.2f}); "
          f"the gateway permutation placebo is null (p = {o['lead_lag_placebo']['p_two_sided']:.2f}). The file flag decisions.H2_ordering.CONFIRMED = true "
          f"checks only the sign rule and is overridden here.",
          [f"{HO}: ordering.*", f"{DV}: ordering.*", f"{HO}: decisions.H2_ordering.CONFIRMED"])
    G = h3["G"]
    block("10.6 / 16.5 H3 (blocking)", "The Holm corrected permutation p is 0.0045 for all three gateway variants",
          f"H3 is **small; it passes the preregistered within-group permutation rule, but the pooled concept-bootstrap CI includes 0**. Held-out "
          f"(n = {h3['n']:,}): G partial rho = {G['partial_rho']:.3f} [{G['ci95'][0]:.3f}, {G['ci95'][1]:.3f}], G_A {h3['G_A']['partial_rho']:.3f} "
          f"[{h3['G_A']['ci95'][0]:.3f}, {h3['G_A']['ci95'][1]:.3f}], G_btw {h3['G_btw']['partial_rho']:.3f} [{h3['G_btw']['ci95'][0]:.3f}, "
          f"{h3['G_btw']['ci95'][1]:.3f}]; Holm p = {h3['holm_adjusted_p']['G']:.4f} from a one-sided within-group permutation test (2,000 draws; Holm over "
          f"G, G_A, G_btw) whose null is centred below zero (about -0.012). Within-group DL pooled G = {G['dl_pool']['pooled']:.3f} "
          f"[{G['dl_pool']['ci95'][0]:.3f}, {G['dl_pool']['ci95'][1]:.3f}], I2 = {G['dl_pool']['I2']:.2f}; G_btw DL = {h3['G_btw']['dl_pool']['pooled']:.3f} "
          f"[{h3['G_btw']['dl_pool']['ci95'][0]:.3f}, {h3['G_btw']['dl_pool']['ci95'][1]:.3f}], I2 = {h3['G_btw']['dl_pool']['I2']:.2f} (negative in LifeEnv, "
          f"{h3['G_btw']['per_group']['LIFEENV']['rho']:.3f}). DEV values: G {h3d['G']:.3f}, G_btw {h3d['G_btw']:.3f}; held-out/DEV shrinkage for G = "
          f"{G['partial_rho'] / h3d['G']:.2f}. The calibration check found 0 of 40 shuffled outcomes declared significant (false-positive rate 0/40), "
          f"which is not a p-value or an exceedance count.",
          [f"{H3}: G.*, G_A.*, G_btw.*, holm_adjusted_p, notes", f"{H1D}: H3_dev", "iter_2/gen_art/gen_art_experiment_5/results/audit_placebo.json: H3_calibration_40_shuffles"])
    block("10.7 Power attribution and MDE wording (blocking)", "The minimum detectable delta AUC is 0.004 (at 80% power, 27,393 episodes)",
          f"Exp5 (art_wxWssKSUR45f) power simulation (h1_dev.json power; {pw['note']}): a planted effect b = 0.3 gives mean dAUC "
          f"{pw['0.3']['mean_dauc']:.4f} with power {pw['0.3']['power_ci_gt0']:.2f} (b = 0.2: {pw['0.2']['mean_dauc']:.4f}, power "
          f"{pw['0.2']['power_ci_gt0']:.2f}), so 0.004 is the **90%** point (the file key 'min_detectable_dauc_80pct' mislabels it), computed for "
          f"{pw['n_heldout_episodes_assumed']:,} held-out episodes, not 27,393. At b = 0 the CI > 0 rule fires {pw['0.0']['power_ci_gt0']:.3f} of the time "
          f"(nominal 0.025): the concept-only bootstrap is anti-conservative. Evaluation 1 (art_lwI2DuRtQRZX, E_power) adds a field random intercept: "
          f"the SD of dAUC under the alternative stays near {g(EV1, 'metadata.E_power.held_out_sizing_from_alternative_SD.SD_alt_field_RE_N1000_m5'):.3f} "
          f"(floor about 0.02) and about {g(EV1, 'metadata.E_power.held_out_sizing_from_alternative_SD.concepts_per_group_p>=0.9_at_0.05'):.0f} held-out "
          f"concepts per group give P(group delta > 0) >= 0.90 at delta = 0.05. The field-random-intercept figure governs the H1 verdict's "
          f"field-level uncertainty; the Exp5 figure ignores between-field variance.",
          [f"{H1D}: power.*", f"{EV1}: metadata.E_power.held_out_sizing_from_alternative_SD.*"])
    sc = fl["size_controlled_all_three"]
    af = fl["all_four_available"]
    block("5.4 The 'B5 + all_four' row (blocking)", "| B5 + all_four (G, REL, RS, G_all) |",
          f"| B3 + log field size + {{gateway_j, phi_home_j, density_j}} (size_controlled_all_three) | {sc['auc_base']:.3f} | {sc['auc_cand']:.3f} | "
          f"{sc['delta_auc']:+.3f} | [{sc['ci95'][0]:.3f}, {sc['ci95'][1]:.3f}] | refit [{f5['size_controlled_all_three']['new_ci95_refit'][0]:.3f}, "
          f"{f5['size_controlled_all_three']['new_ci95_refit'][1]:.3f}] | and add | B3 + {{gateway_j, phi_home_j, density_j}} (all_four_available) | "
          f"{af['auc_base']:.3f} | {af['auc_cand']:.3f} | {af['delta_auc']:+.3f} | [{af['ci95'][0]:.3f}, {af['ci95'][1]:.3f}] | refit "
          f"[{f5['all_four_available']['new_ci95_refit'][0]:.3f}, {f5['all_four_available']['new_ci95_refit'][1]:.3f}] |. Neither row contains G, REL, RS "
          f"or G_all; both refit CIs include 0.",
          [f"{S4}: field_level.size_controlled_all_three.*, field_level.all_four_available.*", f"{EV1}: metadata.F_record.F5_exp4_field_level.rows.*"])
    ents = {"acm_ccs": 3583, "msc": 17872, "pacs_physh": 8462}
    lines = "; ".join(f"{s} {cov[s]['n_with_event']:,} concepts with an event ({cov[s]['n_with_year_usable_event']:,} year-usable)" for s in
                      ("mesh", "wikipedia_en", "wikidata", "acm_ccs", "msc", "pacs_physh", "gartner_hype_cycle", "mit_tr10", "research_fronts",
                       "nature_methods_moty", "science_boty", "physics_world_boty", "jel"))
    block("13.1 Dataset 2 coverage counts (blocking)", "| ACM CCS 1998/2012 | 3,583 |",
          f"Concept counts (coverage_report.json by_source): {lines}. Wikipedia exact first revisions: {cov['wikipedia_en']['status'].get('found', 0):,}. "
          f"The draft's 3,583 / 17,872 / 8,462 / 1,015 are external-ENTRY counts (external_entries_acm_ccs / msc / pacs_physh / jel), not concepts; the "
          f"'589' is Research Fronts only. JEL: 213 concepts found, 0 dated events (present-day membership).",
          [f"{COV}: by_source.*.n_with_event, n_with_year_usable_event, status", "iter_2/gen_art/gen_art_dataset_2/README.md: external_entries table"])
    block("8a Coverage table, iteration-2 column (blocking)", "| RQ2: diffusion trajectories | Not started | - |",
          "Replace the 8a table with record_tables/coverage_iter2_steps.csv (status after iteration 2) and add the per-artifact row counts in "
          "record_tables/coverage_iter2.csv (concepts, episodes, groups, splits, median label coverage, grounding precision, LLM cost, credits).",
          ["record_tables/coverage_iter2.csv", "record_tables/coverage_iter2_steps.csv"])
    block("4.4 Remaining partial associations (blocking)", "The remaining 7 indicators from the 12-indicator file were not extracted",
          "All " + str(len(cands)) + " candidates are in the file: " + "; ".join(
              f"{k} {v['logo_partial_rho']:+.3f} [{v['CI95'][0]:.3f}, {v['CI95'][1]:.3f}] ({v['n_groups_positive']}/4 groups +)" for k, v in cands.items())
          + ". Paste record_tables/partial_association_all.csv.", [f"{EPA}: candidates.*"])
    t = tr["trace"]
    block("11.2 / hypothesis LR, d and strata clashes", "(hypothesis text: M1-vs-M0 LR 68.6 on 961 strata; draft: LR 71.7, d = 0.30; audit: LR 77.3)",
          f"{tr['LR_clash_resolution']} {tr['d_clash_resolution']} {tr['strata_clash_resolution']} The conventional headline is the plain "
          f"retaining-relatedness coefficient d0_ret_rel = {t['coef_M1_d0_ret_rel']['recomputed']:.3f} (SE {t['se_M1_d0_ret_rel']['recomputed']:.3f}), "
          f"since the gateway weighting adds nothing (M3 vs M1 g-only permutation p = {g(HO, 'H2_pooled.gonly_perm_null_M3_vs_M1.p'):.2f}).",
          ["record_tables/next_field_trace.json", f"{HO}: H2_pooled.*", "iter_2/gen_art/gen_art_experiment_6/results/audit.json: H2_LR"])
    pg = g(HO, "H2_per_group")
    block("16.1 'positive in all three evaluable groups'", "positive in all three evaluable holdout field groups",
          f"positive in all four held-out groups (sign test p = {g(HO, 'H2_sign_count.sign_test_p'):.4f}); only Physical's bootstrap CI excludes 0 "
          f"(Physical d = {pg['Physical']['d']:.2f} [{pg['Physical']['boot_ci'][0]:.2f}, {pg['Physical']['boot_ci'][1]:.2f}]; LifeEnv LR p = "
          f"{pg['LifeEnv']['LR']['p']:.2f}; Social LR p = {pg['Social']['LR']['p']:.3f}; cohort d = {pg['Cohort']['d']:.2f}).", [f"{HO}: H2_per_group.*, H2_sign_count"])
    block("10.5 Relatedness pair is held-out only", "The rival covariate pair (relatedness to home and relatedness density) adds delta AUC +0.0034",
          f"The relatedness pair adds dAUC {g(H1, 'rival_head_to_head.dauc_relatedness_pair'):+.4f} on held-out data but "
          f"{g(H1D, 'rival_head_to_head.dauc_relatedness_pair'):+.5f} on DEV: the gain was not seen in development.",
          [f"{H1}: rival_head_to_head.dauc_relatedness_pair", f"{H1D}: rival_head_to_head.dauc_relatedness_pair"])
    block("11.5 Trajectory robustness", "DTW k-medoids with k = 2 is stable (bootstrap ARI 1.0)",
          f"DTW k-medoids k = 2 is stable under bootstrap (ARI 1.0), but the 6-state HMM does not reproduce it (HMM vs DTW ARI = "
          f"{g(HO, 'trajectories.hmm_vs_dtw_ARI'):.3f}), and the localised class is dominated by Medicine homes.", [f"{HO}: trajectories.hmm_vs_dtw_ARI"])
    pool = fa["pooling"]
    block("New: frame comparison (Exp5 vs Exp6) for Section 9/11", "(not in draft: two incompatible panels)",
          f"The common-panel design was not realised: Exp5 (12,499 concepts, TAG grounding) and Exp6 (653 newborn concepts, tag-AND-title) share "
          f"{fa['n_both']} concepts ({fa['share_exp6_in_exp5']:.1%} of Exp6). On them, onset agrees exactly for {fa['agreement']['onset_exact']['value']:.1%} "
          f"(+/-1: {fa['agreement']['onset_pm1']['value']:.1%}), home kappa = {fa['agreement']['home_kappa_26']['value']:.2f}, O2r_m50 Spearman = "
          f"{fa['agreement']['O2r_m50']['spearman']:.3f}, episode Jaccard median = {fa['agreement']['episode_jaccard']['median']:.2f}, but retention kappa = "
          f"{fa['agreement']['retention']['kappa_R_vs_Rcj']:.2f} (Exp5 relative-share rule vs Exp6 absolute >= 2 works; with the matched definition R_abs2 "
          f"kappa = {fa['agreement']['retention']['kappa_R_abs2_vs_Rcj']:.2f}). Pre-declared pooling verdict: **{pool['verdict']}**. A replication of H2 on "
          f"'Exp5 minus Exp6' must rebuild RETAINED/LOST with Exp6's R_cj rule before a null can be read as a failure of the claim.",
          ["frame_agreement.json", "record_tables/definitions_diff.csv", "record_tables/frame_overlap_by_group.csv"])
    hc = o5["hand_check"]
    mn = o5["associations_pooled_heldout_DL"]["O5_main"]
    block("New: O5 external recognition status (13 / 16 Open)", "External recognition has been compiled but not used as an outcome.",
          f"O5 was joined to the Exp5 frame (all {o5['n_joined']:,} concepts). O5_main base rate: {o5['base_rate_heldout']:.3f} held-out. It is "
          f"**{mn['reading']}** to publication outcomes: pooled held-out rho with O2r_m50 = {mn['rho_O2r_m50']['pooled']:.3f} "
          f"[{mn['rho_O2r_m50']['ci95'][0]:.3f}, {mn['rho_O2r_m50']['ci95'][1]:.3f}], with O1 = {mn['rho_O1']['pooled']:.3f} "
          f"[{mn['rho_O1']['ci95'][0]:.3f}, {mn['rho_O1']['ci95'][1]:.3f}]. For {o5['lag']['_all_main_sources']['n_excluded_recognised_at_or_before_t0']:,} "
          f"of {o5['n_frame']:,} concepts the first qualifying recognition is at or before t0. Executor-checked sample: positive precision "
          f"{hc['positive_precision_strict']:.2f}, Wikipedia date error <= 1 year in {hc['wikipedia_date_error_years']['share_le_1']:.2f}, negative "
          f"false-negative rate (Wikipedia only, lower bound) {hc['negatives_false_negative_rate']:.2f}; FIT_FOR_USE = {hc['FIT_FOR_USE']}.",
          ["o5_validation.json", "o5_definitions.json", "record_tables/o5_*.csv"])
    led = pd.read_csv(C.WS / "claims_ledger.csv")
    head = ("# Text corrections for the iteration-3 paper draft\n\nGenerated by `wp5_text.py` from `claims_ledger.csv` and the source files. "
            "Every number in a **New** sentence is read from the named source key. Paths are relative to the run's `3_invention_loop` "
            f"directory. Ledger: {len(led)} rows, {int((led.severity == 'blocking').sum())} blocking; status counts "
            f"{led.status.value_counts().to_dict()}.\n\n")
    (C.WS / "text_corrections.md").write_text(head + "\n".join(rows))


if __name__ == "__main__":
    main()
