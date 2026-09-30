#!/usr/bin/env python3
"""Builds the results tables of README.md from the JSON outputs (every number printed with its JSON key), and
splices them into README_narrative.md at the <!-- TABLES --> marker. Usage: python make_readme.py"""
from __future__ import annotations

import json
from pathlib import Path

WS = Path(__file__).resolve().parent
J = lambda p: json.loads((WS / p).read_text()) if (WS / p).exists() else None  # noqa: E731


def f(x, d=3):
    return "NA" if x is None else (f"{x:+.{d}f}" if isinstance(x, (int, float)) else str(x))


def u(x, d=3):
    return "NA" if x is None else f"{x:.{d}f}"


def ci(c, d=3):
    return "NA" if not c else f"[{c[0]:+.{d}f}, {c[1]:+.{d}f}]"


def part_c(out: list) -> None:
    c = J("results/exp11_completion.json")
    if not c:
        return
    out.append("### Part C: completion of the sealed Exp11 within-concept closure test (reporting only)\n")
    out.append(f"- Seal verification (G0): `results/exp11_completion.json -> seal_verification` = "
               f"{c['seal_verification']['n_ok']}/{c['seal_verification']['n_files']} sealed hashes match, "
               f"frozen spec ok = {c['seal_verification']['frozen_spec_ok']}")
    out.append(f"- Panel rebuilt through the seal gate equals the cached Exp11 panel: `panel_rebuild_equal_to_cache` = "
               f"{c.get('panel_rebuild_equal_to_cache')}; DEV reproduction gate G1 (1e-8): `G1_dev_reproduction` = "
               f"{c.get('G1_dev_reproduction')}")
    out.append(f"- `dev_verdict`: **{c['dev_verdict']}**\n")
    out.append("| body | rows / concepts | H-M1 b(density) [CRV1 CI] | boot CI | H-M2 b(OPEN_home) [CRV1 CI] | boot CI | "
               "DL density (I2) | DL OPEN (I2) |")
    out.append("|---|---|---|---|---|---|---|---|")
    for b, r in c.get("body_models", {}).items():
        dd, do = r.get("DL_density") or {}, r.get("DL_OPEN_home") or {}
        out.append(f"| {b} | {r['n_rows']} / {r['n_concepts']} | {f(r['H_M1_density']['b'])} {ci(r['H_M1_density']['ci_crv1'])} | "
                   f"{ci(r['H_M1_density']['ci_boot'])} | {f(r['H_M2_OPEN_home']['b'])} {ci(r['H_M2_OPEN_home']['ci_crv1'])} | "
                   f"{ci(r['H_M2_OPEN_home']['ci_boot'])} | {f(dd.get('b'))} ({u(dd.get('I2'), 2)}) | "
                   f"{f(do.get('b'))} ({u(do.get('I2'), 2)}) |")
    out.append("\nKeys: `results/exp11_completion.json -> body_models.<body>.*` (source "
               "`exp11_code/results/fe_results_completed.json -> <body>`).\n")
    h5 = c.get("H_M5") or {}
    out.append(f"- H-M5 (signs of H-M1 < 0 and H-M2 > 0 on OLD_HELDOUT and COHORT): `H_M5.holds_signs` = "
               f"**{h5.get('holds_signs')}**")
    h3 = c.get("H_M3") or {}
    out.append("- H-M3 (|std fwd| - |std rev|, paired bootstrap): " + "; ".join(
        f"{b} {f(v['point']['diff'], 4)} {ci((v.get('boot_diff') or {}).get('ci'), 4)}" for b, v in h3.items()) +
        " (`H_M3.<body>`)")
    es = c.get("event_study") or {}
    if es:
        out.append("\n| body | control | mean lag 0..2 | 95% CI | pre-trend Wald p | Roth 80% detectable slope | max abs lead | n treated | boots |")
        out.append("|---|---|---|---|---|---|---|---|---|")
        for b, E in es.items():
            for v, r in E.items():
                if isinstance(r, dict) and "att" in r:
                    out.append(f"| {b} | {v} | {f(r.get('mean_lag_0_2'), 4)} | {ci(r.get('lag02_ci'), 4)} | "
                               f"{u((r.get('pretrend_wald') or {}).get('p'), 3)} | {u(r.get('roth_detectable_slope_80pct'), 4)} | "
                               f"{u(r.get('max_abs_lead'), 4)} | {r.get('n_treated')} | {r.get('n_boot_ok')} |")
        out.append("\nKeys: `results/exp11_completion.json -> event_study.<body>.<control>.*`.")
        pl = (es.get("DEV") or {}).get("placebo_event_date")
        if pl:
            out.append(f"- DEV event-date permutation placebo: mean {f(pl['mean'], 4)}, 2.5-97.5% {ci(pl['q025_q975'], 4)}, "
                       f"observed {f(pl['observed'], 4)}, one-sided p = {pl['p_one_sided_le_obs']:.3f} "
                       f"(`event_study.DEV.placebo_event_date`, n = {pl['n']})")
        h4 = c.get("H_M4") or {}
        out.append(f"- **H-M4** (`H_M4.holds`) = **{h4.get('holds')}**: lag CI below 0 = {h4.get('lag_negative_ci_below_0')}, "
                   f"pre-trend p = {u(h4.get('pretrend_p'), 3)}, leads small = {h4.get('lead_small_vs_lag')}, "
                   f"placebo p = {u(h4.get('placebo_p_one_sided'), 3)}\n")
    hs = c.get("H_S1") or {}
    if hs:
        out.append("| body | n multi / single (take-off) | share no prior peak multi | single | diff | 95% CI | holds |")
        out.append("|---|---|---|---|---|---|---|")
        for b, r in hs.items():
            if "diff" in r:
                out.append(f"| {b} | {r['n_multi']} / {r['n_single']} | {r['share_no_prior_peak_multi']:.3f} | "
                           f"{r['share_no_prior_peak_single']:.3f} | {f(r['diff'])} | {ci(r['ci'])} | {r['holds_H_S1']} |")
        out.append("\nKeys: `results/exp11_completion.json -> H_S1.<body>` (Exp12 independent prior: HR 0.47, cited only).")
        sv = c.get("sequence_survival") or {}
        for b, r in sv.items():
            cx = (r.get("cox") or {}).get("multi_home") or {}
            out.append(f"- {b}: log-rank p = {r['logrank']['p']:.3g}; Cox HR(multi-home) = {u(cx.get('HR'))} {ci(cx.get('ci'))}")
        for k_, r in (c.get("sequence_event_studies") or {}).items():
            out.append(f"- `sequence_event_studies.{k_}`: mean lag 0..2 = {f(r.get('mean_lag_0_2'), 4)} {ci(r.get('lag02_ci'), 4)}, "
                       f"pre-trend p = {u((r.get('pretrend_wald') or {}).get('p'), 3)}, n treated = {r.get('n_treated')}")
    hp = c.get("H_P1")
    if hp:
        m = hp["O2r_m50"]
        out.append(f"\n- **H-P1 as preregistered** (ALL-papers static partner set, DL over the 4 held-out groups, O2r_m50): "
                   f"METHOD-DOMAIN {f(m['DL_METHOD_minus_DOMAIN'].get('b'))} {ci(m['DL_METHOD_minus_DOMAIN'].get('ci'))}; "
                   f"comm_new-comm_old {f(m['DL_comm_new_minus_comm_old'].get('b'))} {ci(m['DL_comm_new_minus_comm_old'].get('ci'))} "
                   f"(I2 {u(m['DL_comm_new_minus_comm_old'].get('I2'), 2)}); holds = **{hp['H_P1_holds_O2r_m50']}** "
                   f"(`results/exp11_completion.json -> H_P1`)")
    ut = c.get("exp11_unit_tests_rerun")
    if ut:
        out.append(f"- Exp11 unit tests rerun on the copied code: {sum(bool(v) for v in ut.values())}/{len(ut)} pass "
                   f"(`exp11_unit_tests_rerun`)")
    out.append("")


def part_a(out: list) -> None:
    r = J("results/partner_classes.json")
    if not r:
        return
    B = r["bodies"]
    out.append("### Part A: which HOME partner classes carry the signal? (EXPLORATORY, selection data)\n")
    san = r["exp10_sanity_gate"]
    out.append(f"- Gates: G2 (home build == Exp10, all concepts, 1e-9) and identities: see `results/unit_tests_iter5.json`; "
               f"Exp10 published cohort psp reproduced: NOV_res {f(san['NOV_res']['recomputed_R2'], 4)} vs "
               f"{f(san['NOV_res']['exp10_published'], 4)}, edge_persistence {f(san['edge_persistence']['recomputed_R2'], 4)} vs "
               f"{f(san['edge_persistence']['exp10_published'], 4)} (`exp10_sanity_gate`)\n")
    comps = ["NOVCHURN_home", "OPEN_home", "NOV_res", "churn", "new_edge_rate", "new_edge_rate_ALL", "bridging_share_home",
             "nov_type_METHOD", "nov_type_DOMAIN", "ch_type_METHOD", "ch_type_DOMAIN", "ner_comm_new", "ner_comm_old",
             "ner_carrier_mixed", "ner_carrier_pure", "nov_deg_low", "nov_deg_high", "ch_deg_low", "ch_deg_high",
             "chd_all", "cha_all"]
    bodies = ["POOLED_EXP5", "DEV", "OLD_HELDOUT", "COHORT_2010_14", "COHORT_2015_17_R0", "COHORT_2015_17_R3"]
    out.append("psp with O2r_m50 given B5 (+ t0/group/body dummies; 2015-17 cohort: Exp10 rungs), 95% concept-bootstrap CI "
               f"({r['n_boot']} draws). Key: `results/partner_classes.json -> bodies.<body>|O2r_m50.components.<component>`.\n")
    out.append("| component | " + " | ".join(bodies) + " | DL 4 held-out groups (I2) |")
    out.append("|---|" + "---|" * (len(bodies) + 1))
    dl = r["DL_heldout_groups"]["O2r_m50"]["components"]
    for cmp_ in comps:
        cells = []
        for b in bodies:
            e = B.get(f"{b}|O2r_m50", {}).get("components", {}).get(cmp_)
            cells.append("-" if not e or e.get("rho") is None else f"{e['rho']:+.3f} {ci(e.get('ci'))}")
        d = dl.get(cmp_) or {}
        cells.append("-" if d.get("psp") is None else f"{d['psp']:+.3f} {ci(d['ci'])} ({d['I2']:.2f})")
        out.append(f"| {cmp_} | " + " | ".join(cells) + " |")
    out.append("\nHolm family (POOLED_EXP5, O2r_m50; `holm_family_POOLED_EXP5_O2r_m50`), with the two placebo nulls "
               "(`placebo.<scheme>.<contrast>`):\n")
    out.append("| contrast | diff | 95% CI | p | Holm p | DL held-out groups | 2015-17 R0 / R3 diff | placebo across rows: mean (obs quantile) | placebo within concept: mean (obs quantile) |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for h, e in r["holm_family_POOLED_EXP5_O2r_m50"].items():
        pa, pw = r["placebo"]["across_rows"][h], r["placebo"]["within_concept"][h]
        d = e["DL_heldout_groups"]
        out.append(f"| {h} | {f(e['diff'])} | {ci(e['ci'])} | {e['p_two']:.4f} | {e['p_holm']:.4f} | {f(d['b'])} {ci(d['ci'])} | "
                   f"{f(e['cohort_2015_17_R0_direction'])} / {f(e['cohort_2015_17_R3_direction'])} | "
                   f"{f(pa['mean'])} ({pa['observed_quantile']:.2f}) | " +
                   ("degenerate: count part invariant (sd 0)" if pw["sd"] < 1e-9 else f"{f(pw['mean'])} ({pw['observed_quantile']:.2f})") + " |")
    out.append("\nBootstrap p values have a floor of 1/2000 (Holm floor 0.0025). The within-concept placebo keeps each concept's "
               "class counts, so count-based parts (C2, C4) cannot move under it; the across-rows placebo is their null.")
    out.append("\nShapley decomposition of the psp (O2r_m50). phi in psp units; share = phi / (v(full) - v(empty)); fair = the "
               "class's share of new partners (NOVCHURN games) or of the part's mass. Key: "
               "`results/partner_shapley.json -> games.<body>|O2r_m50.shapley.<game>`.\n")
    out.append("| body | game | v(full)-v(empty) | player: phi [CI] (share / fair) |")
    out.append("|---|---|---|---|")
    for b in ("POOLED_EXP5", "OLD_HELDOUT", "COHORT_2015_17_R0", "COHORT_2015_17_R3"):
        for g, s in B.get(f"{b}|O2r_m50", {}).get("shapley", {}).items():
            cells = []
            for p, e in s["phi"].items():
                sh = f" ({e['share']:.2f} / {e['fair_share']:.2f})" if "share" in e and "fair_share" in e else \
                    (f" ({e['share']:.2f})" if "share" in e else "")
                cells.append(f"{p}: {e['phi']:+.3f} {ci(e.get('phi_ci'))}{sh}")
            out.append(f"| {b} | {g} | {s['v_full_minus_empty']:+.3f}{' (F5: small v)' if s['small_v_F5'] else ''} | "
                       + "; ".join(cells) + " |")
    out.append("\nPredictions (`predictions`):\n")
    for k_, v in r["predictions"].items():
        out.append(f"- {k_}: " + ", ".join(f"{a}={f(b) if isinstance(b, float) else (ci(b) if isinstance(b, list) else b)}"
                                           for a, b in v.items()))
    br = J("results/bridging_papers_summary.json")
    if br:
        out.append("\nBridging papers (`results/bridging_papers_summary.json`):\n")
        for fr in ("exp5", "cohort_2015_17"):
            x = br.get(fr, {})
            out.append(f"- {fr}: {x.get('n_bridging')} bridging of {x.get('n_papers')} early home papers; " + "; ".join(
                f"{v}: bridging {e['bridging']:.3f} vs other {e['other']:.3f}, diff CI {ci(e['diff_ci_concept_cluster'])}"
                for v, e in (x.get("profile") or {}).items()))
        for b, x in br.get("psp", {}).items():
            out.append(f"- {b}: " + "; ".join(f"psp({k_}) = {f(e['rho'])} {ci(e['ci'])}" for k_, e in x.items()))
    out.append("")


def part_b(out: list) -> None:
    t = J("results/trait_stability.json")
    if not t:
        return
    out.append("### Part B: is HOME openness a stable concept trait? (prediction hashed before computing)\n")
    out.append("| body | variable | ICC raw [CI] | ICC size-adj | ICC deg>=5 | MixedLM REML ICC | retest rho [CI] | partial retest | "
               "disattenuated | lag-1 AC (FD corr) | within/total SD |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for b in ("DEV", "OLD_HELDOUT", "COHORT_2010_14"):
        for v in ("OPEN_home", "NOVCHURN", "log1p_home_works"):
            e = t["bodies"][b][v]
            tr = e["test_retest"]
            ml = (e.get("mixedlm_reml") or {}).get("icc_reml")
            out.append(f"| {b} | {v} | {e['icc_raw']['icc']:.3f} {ci(e['icc_raw']['ci'])} | {e['icc_size_adj']['icc']:.3f} | "
                       f"{e['icc_raw_deg_ge5']['icc']:.3f} | {u(ml)} | {u(tr.get('rho'))} {ci(tr.get('ci'))} | "
                       f"{u(tr.get('partial_rho_given_size'))} | {u(e.get('disattenuated_retest'))} | "
                       f"{f(e['autocorr']['lag1_within_demeaned'])} ({f(e['autocorr']['first_difference_corr'])}) | "
                       f"{e['within_over_total_sd']:.2f} |")
    out.append("\nKey: `results/trait_stability.json -> bodies.<body>.<variable>.*`. Static 3-year build early vs later "
               "(`static_retest`): " + "; ".join(
                   f"{b} OPEN {u(t['static_retest'][b]['OPEN_home'].get('rho'))} / NOVCHURN {u(t['static_retest'][b]['NOVCHURN'].get('rho'))}"
                   for b in ("DEV", "OLD_HELDOUT", "COHORT_2010_14")))
    v = t["verdict"]
    out.append(f"\n- **P-B1 (OPEN_home) TRAIT_SUPPORTED = {v['P-B1_OPEN_home']['TRAIT_SUPPORTED']}**; "
               f"P-B2 (NOVCHURN) = {v['P-B2_NOVCHURN']['TRAIT_SUPPORTED']}; positive control ICC(log1p home works) = "
               + ", ".join(f"{b} {x:.3f}" for b, x in v["positive_control_icc_log1p_home_works"].items()) + " (`verdict`)")
    fp = t["bodies"]["DEV"].get("fe_power_link")
    if fp:
        out.append(f"- FE power link (DEV): within-concept SD of yearly OPEN_home = {fp['sd_within_x_panel']:.3f}; the H-M2 "
                   f"PPML MDE is {fp['MDE_pct_change_entries_per_within_sd']:.1f}% change in off-home entries per within-SD "
                   f"(`bodies.DEV.fe_power_link`)")
    out.append("")


def cv_block(out: list) -> None:
    m = J("method_out.json")
    if not m:
        return
    cv = m["metadata"]["cv_metrics"]
    out.append("### Baseline vs method: 5-fold concept-CV ridge within body (`method_out.json -> metadata.cv_metrics`)\n")
    out.append("| body | n | B5 Spearman | +NOVCHURN | +partner classes | +OPEN_home | gain NOVCHURN [CI] |")
    out.append("|---|---|---|---|---|---|---|")
    for b, r in cv.items():
        g = r["gain_NOVCHURN_spearman"]
        out.append(f"| {b} | {r['n']} | {r['B5']['spearman_oof']:.4f} | {r['B5_plus_NOVCHURN']['spearman_oof']:.4f} | "
                   f"{r['B5_plus_partner_classes']['spearman_oof']:.4f} | {r['B5_plus_OPEN_home']['spearman_oof']:.4f} | "
                   f"{g['est']:+.4f} {ci(g['ci'], 4)} |")
    out.append("")


def main() -> None:
    out: list = []
    part_c(out)
    part_a(out)
    part_b(out)
    cv_block(out)
    nar = (WS / "README_narrative.md").read_text()
    dev = []
    for src, p in (("iter-5 Parts A/B (`results/deviations.json`)", "results/deviations.json"),
                   ("iter-5 Part C runners (`exp11_code/results/deviations.json`)", "exp11_code/results/deviations.json")):
        d = J(p) or {}
        if d:
            dev.append(f"**{src}**\n")
            dev += [f"- `{k}`: {v}" for k, v in d.items()]
            dev.append("")
    dev.append("Exp11's own sealed deviations (500 body-model boots and 300 event-study boots outside DEV, saturated "
               "Sun-Abraham design, etc.) are in the Exp11 artifact's `results/deviations.json` and apply unchanged.")
    (WS / "README.md").write_text(nar.replace("<!-- TABLES -->", "\n".join(out))
                                  .replace("DEVIATIONS_PLACEHOLDER", "\n".join(dev)))
    print("README.md written", len(out), "table lines")


if __name__ == "__main__":
    main()
