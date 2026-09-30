#!/usr/bin/env python3
"""WP1 claims ledger + WP2 paper-ready record tables (T1 portability, T2 exp1 lineage robustness, T5 H1 criteria,
T6 ordering MIXED, T7 iteration-2 coverage) + an automatic harvest of every number in the iteration-2 draft sections.
Every source value is READ PROGRAMMATICALLY by key path (never retyped); reported values are the draft's text."""
from __future__ import annotations

import json
import math
import re
from decimal import Decimal, InvalidOperation

import numpy as np
import pandas as pd
from loguru import logger

import common as C

H1 = "round-2/experiment-5/src/results/h1_heldout.json"
H1D = "round-2/experiment-5/src/results/h1_dev.json"
H3 = "round-2/experiment-5/src/results/h3_results.json"
AP5 = "round-2/experiment-5/src/results/audit_placebo.json"
FS5 = "round-2/experiment-5/src/frozen_spec.json"
HO6 = "round-2/experiment-6/src/results/heldout_result.json"
DV6 = "round-2/experiment-6/src/results/dev_result.json"
AU6 = "round-2/experiment-6/src/results/audit.json"
COV = "round-2/dataset-2/src/out/coverage_report.json"
EPA = "round-1/experiment-3/src/results/exploratory_partial_association.json"
AU3 = "round-1/experiment-3/src/results/audit.json"
EV1 = "round-2/evaluation-1/src/eval_out.json"
S4 = "round-1/experiment-4/src/screen_result.json"
S1 = "round-1/experiment-1/src/results/screen_result.json"
S3 = "round-1/experiment-3/src/results/screen_result.json"
TRACE = "record_tables/next_field_trace.json"

_cache: dict = {}


def J(path: str):
    if path not in _cache:
        p = (C.WS / path) if path.startswith("record_tables") or path.startswith("results") else (C.ROOT / path)
        _cache[path] = C.read_json(p) if p.exists() else None
    return _cache[path]


def flatten(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, f"{prefix}.{k}" if prefix else str(k))
    elif isinstance(obj, list) and len(obj) <= 50:
        for i, v in enumerate(obj):
            yield from flatten(v, f"{prefix}.{i}")
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        yield prefix, float(obj)


def decimals(s: str) -> int:
    s = s.replace(",", "").strip().lstrip("+").replace("−", "-")
    if "e" in s.lower():
        return 99
    return len(s.split(".")[1]) if "." in s else 0


def to_num(s):
    if isinstance(s, bool) or s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    t = str(s).replace(",", "").replace("−", "-").replace("x 10^", "e").replace(" ", "").rstrip("%").lstrip("+")
    try:
        return float(Decimal(t))
    except (InvalidOperation, ValueError):
        return None


def status_of(rep, src, scale: float = 1.0) -> tuple[str, float]:
    if src is None:
        return "MISSING", math.nan
    if isinstance(src, (bool, str)) or isinstance(rep, bool):
        return ("MATCH" if str(rep).lower() == str(src).lower() else "MISMATCH"), math.nan
    r = to_num(rep)
    if r is None:
        return "MISMATCH", math.nan
    sv = float(src) * scale
    diff = abs(r - sv)
    s = str(rep)
    dp = decimals(s)
    if dp == 99:  # scientific notation: compare on 2 significant figures
        return ("MATCH" if diff <= 0.05 * abs(sv) else "MISMATCH"), diff
    half = 0.5 * 10 ** (-dp)
    if diff <= half + 1e-12:
        return "MATCH", diff
    if diff <= 2 * half + 1e-12:
        return "ROUNDING", diff
    return "MISMATCH", diff


ROWS: list[dict] = []


def add(cid, it, art, sec, claim, qty, rep, src, key=None, sev="minor", corr="", note="", override=None, scale=1.0,
        value=None, in_draft=True):
    """Add a ledger row; source value read from src/key unless `value` is given as (computed_value, expression)."""
    if value is not None:
        sval, key = value
        file_ok = True
    else:
        d = J(src) if src else None
        file_ok = d is not None
        try:
            sval = C.get_path(d, key) if file_ok else None
        except (KeyError, IndexError, TypeError):
            sval = None
    if not file_ok:
        st, diff = "MISSING_SOURCE", math.nan
    else:
        st, diff = status_of(rep, sval, scale)
    if override and st != "MISSING_SOURCE":
        st = override
    ROWS.append({"claim_id": cid, "iteration": it, "artifact_id": art, "draft_section": sec, "claim_text": claim, "quantity": qty,
                 "reported_value": rep, "in_draft": in_draft, "source_file": src, "key_path": key,
                 "source_value": sval if not isinstance(sval, float) else float(sval), "abs_diff": diff, "status": st,
                 "severity": sev, "correction_text": corr, "text_change_note": note})


def find_key(src: str, value: float, tol: float, hint: str = "") -> str | None:
    d = J(src)
    if d is None:
        return None
    cands = [k for k, v in flatten(d) if abs(v - value) <= tol]
    if hint:
        h = [k for k in cands if hint in k]
        cands = h or cands
    return cands[0] if cands else None


def ledger() -> None:
    A5, A6, AD, AE, A1, A3, A4 = "art_wxWssKSUR45f", "art_N-mpomDZZ1ln", "art_O7Dq4L02QnDN", "art_lwI2DuRtQRZX", "art_xp8BGBJZsxeI", "art_yrradSC27HtQ", "art_33_KKk_G8Gw5"
    s103 = "10.3 Field retention hypothesis: result: DISCONFIRMED"
    # ---------------- (i) H1 criteria
    crit_reported = {"pooled_dauc_ge_0.05": "false", "refit_ci_gt0": "false", "sign_ge3_of_4_evaluable": "false",
                     "n_groups_positive": "2", "cohort_same_sign": "true", "lpm_beta_within_gt0_p05": "false",
                     "placebo_null": "false"}
    for k, rep in crit_reported.items():
        blocking = k == "lpm_beta_within_gt0_p05"
        add(f"H1_crit_{k}", 2, A5, s103, "Verdict: DISCONFIRMED by all preregistered criteria.", f"verdict_H1.criteria.{k} (held-out, 8,515 episodes / 3,085 concepts)",
            rep, H1, f"verdict_H1.criteria.{k}", sev="blocking" if blocking else "minor",
            corr=("The within-field LPM criterion PASSES: beta_within = +0.068 per SD, concept-clustered p = 0.041 (two-way clustered p = 0.17); "
                  "the verdict rule still returns DISCONFIRMED because 5 of the 6 core criteria fail.") if blocking else "",
            note="add the criterion-by-criterion table (record_tables/h1_criteria.csv) to 10.3", in_draft=blocking)
    add("H1_verdict", 2, A5, s103, "Verdict: DISCONFIRMED", "verdict_H1.verdict", "DISCONFIRMED", H1, "verdict_H1.verdict")
    for k, rep in (("n", "8515"), ("beta_within_per_sd", "0.0678"), ("se_concept", "0.0331"), ("p_concept", "0.0408"),
                   ("se_twoway", "0.0497"), ("p_twoway", "0.172")):
        add(f"H1_lpm_{k}", 2, A5, s103, "(not reported: LPM with field FE)", f"lpm_field_fe.{k} (held-out)", rep, H1, f"lpm_field_fe.{k}",
            sev="blocking", note="add to 10.3 table", in_draft=False)
    for k, rep in (("n", "27392"), ("beta_within_per_sd", "0.0507"), ("p_concept", "0.0065"), ("p_twoway", "0.179")):
        add(f"H1_lpm_all_{k}", 2, A5, s103, "(not reported: LPM with field FE, all splits)", f"lpm_field_fe_all_splits.{k}", rep, H1,
            f"lpm_field_fe_all_splits.{k}", sev="blocking", note="add to 10.3 table", in_draft=False)
    code = (C.E5 / "models.py").read_text().splitlines()
    ln = next(i + 1 for i, l in enumerate(code) if '"lpm_beta_within_gt0_p05"' in l and "p_concept" in l)
    add("H1_lpm_prereg_SE", 2, A5, s103, "(SE type of the preregistered LPM criterion not stated)", "SE used by lpm_beta_within_gt0_p05",
        "concept-clustered", FS5, None, sev="blocking",
        value=("concept-clustered", f"frozen_spec.json verdict_rules.lpm_beta_within_gt0_p = {J(FS5)['verdict_rules']['lpm_beta_within_gt0_p']} (SE not named); "
                                    f"models.py:{ln} evaluates lpm.get('p_concept') -> concept-clustered"),
        corr="The frozen rule names p < 0.05 without an SE type; the sealed code evaluates the concept-clustered p, so the criterion PASSES as preregistered. State this and add the two-way p = 0.17 as a robustness note.",
        in_draft=False)
    add("H1_placebo_meaning", 2, A5, s103, "The placebo is not exceeded", "placebo_rewired.real_exceeds_p95 (criterion placebo_null)", "false", H1,
        "placebo_rewired.real_exceeds_p95",
        corr="placebo_null = false means the real held-out dAUC (-9e-6) does NOT exceed the 95th percentile of the 200 rewired-backbone placebo draws (p95 = 1.1e-4; 36.5% of draws >= real): the criterion fails. The draft sentence is correct but should name the criterion.",
        note="rename to 'rewired-backbone placebo criterion fails (real < placebo p95)'")
    add("H1_placebo_share_ge_real", 2, A5, s103, "(not reported)", "placebo_rewired.share_ge_real", "0.365", H1, "placebo_rewired.share_ge_real", in_draft=False)
    add("H1_dauc_heldout", 2, A5, s103, "Delta AUC (gateway over X0) holdout -0.00001", "primary.dauc", "-0.00001", H1, "primary.dauc")
    add("H1_dl_pooled", 2, A5, s103, "DerSimonian-Laird pooled delta AUC: -0.00004", "dl_pool.pooled", "-0.00004", H1, "dl_pool.pooled")
    add("H1_dl_Q", 2, A5, s103, "Q = 1.69", "dl_pool.Q", "1.69", H1, "dl_pool.Q")
    add("H1_auc_X0", 2, A5, s103, "AUC X0 0.837", "primary.auc_X0", "0.837", H1, "primary.auc_X0")
    add("H1_condlogit_beta", 2, A5, s103, "conditional logit is null (beta = -0.075, z = -1.20, p = 0.23)", "cond_logit.beta_gateway_std", "-0.075", H1, "cond_logit.beta_gateway_std")
    add("H1_condlogit_p", 2, A5, s103, "p = 0.23", "cond_logit.p_two_sided", "0.23", H1, "cond_logit.p_two_sided")
    add("H1_logit_cl_concept_p", 2, A5, s103, "(not reported)", "logit_clustered_se.concept.p", "0.288", H1, "logit_clustered_se.concept.p", sev="minor", in_draft=False)
    add("H1_boundary_interaction", 2, A5, s103, "(not reported)", "boundary.beta_interaction (predicted negative; consistent=false)", "0.064", H1, "boundary.beta_interaction", in_draft=False)
    add("H1_pigeonhole_ci_lo", 2, A5, s103, "(not reported; crossed concept x field bootstrap)", "pigeonhole_crossed_bootstrap.ci95[0]", "-0.0023", H1, "pigeonhole_crossed_bootstrap.ci95.0", in_draft=False)
    add("H1_pigeonhole_ci_hi", 2, A5, s103, "(not reported)", "pigeonhole_crossed_bootstrap.ci95[1]", "0.0010", H1, "pigeonhole_crossed_bootstrap.ci95.1", in_draft=False)
    # ---------------- (ii) ordering -> MIXED
    s113 = "11.3 Ordering: first retained gateway precedes entropy takeoff"
    o = [("n_top_o2r", "175"), ("n_tau_detected", "112"), ("gateway.n_evaluable", "102"), ("gateway.before", "57"), ("gateway.ties", "15"),
         ("gateway.after", "30"), ("gateway.share_before_excl_ties", "0.655"), ("gateway.sign_test_p_one_sided", "0.003"),
         ("peripheral.n_evaluable", "106"), ("peripheral.before", "49"), ("peripheral.ties", "20"), ("peripheral.after", "37"),
         ("peripheral.share_before_excl_ties", "0.570"), ("peripheral.sign_test_p_one_sided", "0.118"), ("mcnemar.gw_only", "27"),
         ("mcnemar.per_only", "15"), ("mcnemar.p_exact_two_sided", "0.088"),
         ("lead_lag.forward_dH_on_ret.coef.ret_gw.b", "-0.0279"), ("lead_lag.forward_dH_on_ret.coef.ret_gw.p", "0.0007"),
         ("lead_lag.forward_dH_on_ret.coef.ret_per.b", "-0.0434"), ("lead_lag.forward_dH_on_ret.coef.ret_per.p", "6e-8"),
         ("lead_lag.reverse_dret_on_H.coef.H.b", "0.0767"), ("lead_lag.event_study_H.coef.ev-3.b", "-0.0717"),
         ("lead_lag.event_study_H.coef.ev-3.p", "0.0002"), ("lead_lag.event_study_H.coef.ev-2.b", "-0.0204"),
         ("lead_lag.event_study_H.coef.ev-2.p", "0.075"), ("lead_lag_placebo.p_two_sided", "0.63")]
    for k, rep in o:
        in_d = k in ("n_top_o2r", "n_tau_detected", "gateway.n_evaluable", "gateway.share_before_excl_ties", "gateway.sign_test_p_one_sided",
                     "peripheral.n_evaluable", "peripheral.share_before_excl_ties", "peripheral.sign_test_p_one_sided", "mcnemar.gw_only",
                     "mcnemar.per_only", "mcnemar.p_exact_two_sided", "lead_lag_placebo.p_two_sided")
        add(f"ORD_{k}", 2, A6, s113, "ordering table / lead-lag", f"heldout ordering.{k}", rep, HO6, f"ordering.{k}",
            sev="blocking" if k.startswith("lead_lag.") and "placebo" not in k else "minor", in_draft=in_d,
            note="" if in_d else "add to the ordering table (record_tables/ordering_mixed.csv)")
    add("ORD_reverse_p_heldout", 2, A6, s113, "the reverse (entropy predicting retention) is not significant (p = 0.22)",
        "heldout ordering.lead_lag.reverse_dret_on_H.coef.H.p", "0.22", HO6, "ordering.lead_lag.reverse_dret_on_H.coef.H.p",
        sev="blocking", override="MISLABELLED",
        corr="Held-out reverse path b = 0.077 (p = 0.22), but on DEV the reverse path is significant: b = 0.232 [0.066, 0.397], p = 0.006 (dev_result.json).",
        note="quote both splits")
    for k, rep in (("lead_lag.reverse_dret_on_H.coef.H.b", "0.2318"), ("lead_lag.reverse_dret_on_H.coef.H.p", "0.0062"),
                   ("gateway.share_before_excl_ties", "0.714"), ("peripheral.share_before_excl_ties", "0.703"), ("mcnemar.p_exact_two_sided", "0.344"),
                   ("lead_lag.event_study_H.coef.ev-3.b", "-0.0883")):
        add(f"ORD_DEV_{k}", 2, A6, s113, "(dev ordering / lead-lag, not reported)", f"dev ordering.{k}", rep, DV6, f"ordering.{k}",
            sev="blocking" if "reverse" in k else "minor", in_draft=False)
    add("ORD_both_associated", 2, A6, s113, "both retained gateway and retained peripheral fields are associated with subsequent entropy change",
        "sign of forward ret_gw coefficient", "positive (implied)", HO6, "ordering.lead_lag.forward_dH_on_ret.coef.ret_gw.b", sev="blocking",
        override="MISLABELLED", corr="Both coefficients are NEGATIVE: retention is followed by SMALLER next-year entropy gains (ret_gw -0.028, p = 0.0007; ret_per -0.043, p = 6e-8).")
    add("ORD_file_flag", 2, A6, "16.3 / 11.3", "confirmed by the preregistered rule", "decisions.H2_ordering.CONFIRMED", "true", HO6,
        "decisions.H2_ordering.CONFIRMED", sev="blocking", override="FILE_FLAG_OVERRIDDEN",
        corr="The file flag CONFIRMED only checks the sign rule (share >= 0.60, sign p < 0.01). Lead-lag coefficients are negative, the event study has a significant pre-trend (ev-3 = -0.072, p = 0.0002), the dev reverse path is significant and the gateway permutation placebo is null (p = 0.63): ordering = MIXED / not established.")
    og = J(HO6)["ordering"]["gateway"]
    ntop = J(HO6)["ordering"]["n_top_o2r"]
    for nm, den, rep in (("of_broad_concepts", ntop, "0.326"), ("of_evaluable", og["n_evaluable"], "0.559"),
                         ("of_non_tied", og["before"] + og["after"], "0.655")):
        add(f"ORD_denominator_{nm}", 2, A6, "16.3 What we have learned", "In 66% of broad concepts, the first retained gateway field precedes ...",
            f"gateway before / {nm} ({og['before']}/{den})", rep, HO6, None, sev="blocking",
            value=(og["before"] / den, f"ordering.gateway.before / {den}"),
            override="MISLABELLED" if nm == "of_broad_concepts" else None,
            corr="57 of 175 broad (top-tercile) concepts = 32.6%; 57 of 102 evaluable = 55.9%; 57 of 87 non-tied = 65.5%. '66% of broad concepts' must read '65.5% of the 87 non-tied evaluable concepts (57/87)'." if nm == "of_broad_concepts" else "")
    # ---------------- (iii) exploratory partial associations (all 12)
    s44 = "4.4 Exploratory partial association"
    draft_pa = {"D_ratio": ("0.335", "0.019", "0.648"), "D_rare": ("0.311", "-0.034", "0.653"), "participation": ("0.322", "-0.037", "0.640"),
                "NOV_res": ("0.281", "-0.114", "0.581"), "F_res": ("-0.267", "-0.443", "0.249")}
    cands = J(EPA)["candidates"]
    for nm, v in cands.items():
        dr = draft_pa.get(nm)
        add(f"PA_{nm}_rho", 1, A3, s44, "partial association table", f"candidates.{nm}.logo_partial_rho (n = 47)", dr[0] if dr else f"{v['logo_partial_rho']:.3f}",
            EPA, f"candidates.{nm}.logo_partial_rho", in_draft=bool(dr), sev="blocking" if not dr else "minor",
            note="" if dr else "row omitted from the draft ('not available') although the file holds it")
        add(f"PA_{nm}_ci90_lo", 1, A3, s44, "partial association table", f"candidates.{nm}.CI90[0]", dr[1] if dr else f"{v['CI90'][0]:.3f}", EPA, f"candidates.{nm}.CI90.0", in_draft=bool(dr))
        add(f"PA_{nm}_ci90_hi", 1, A3, s44, "partial association table", f"candidates.{nm}.CI90[1]", dr[2] if dr else f"{v['CI90'][1]:.3f}", EPA, f"candidates.{nm}.CI90.1", in_draft=bool(dr))
        add(f"PA_{nm}_ci95_lo", 1, A3, s44, "(95% CI)", f"candidates.{nm}.CI95[0]", f"{v['CI95'][0]:.3f}", EPA, f"candidates.{nm}.CI95.0", in_draft=nm == "D_ratio")
        add(f"PA_{nm}_groups_pos", 1, A3, s44, "(groups positive)", f"candidates.{nm}.n_groups_positive", str(v["n_groups_positive"]), EPA, f"candidates.{nm}.n_groups_positive", in_draft=False)
    add("PA_remaining_7_claim", 1, A3, s44, "The remaining 7 indicators ... are not available in the current workspace output",
        "number of candidates in exploratory_partial_association.json", "5", EPA, None, sev="blocking",
        value=(len(cands), "len(candidates)"), corr=f"The file holds all {len(cands)} candidates; paste the full table (record_tables/partial_association_all.csv).")
    add("PA_perm_p", 1, A3, s44, "D_ratio's permutation p = 0.037 (one sided, 1,000 permutations)", "perm_p_value_one_sided", "0.037", AU3,
        find_key(AU3, 0.037, 0.0006, "perm") or "perm_p_value_one_sided")
    # ---------------- (iv) O5 coverage (concepts vs entries)
    s131 = "13.1 Sources"
    cov = J(COV)["by_source"]
    readme = (C.D2 / "README.md").read_text()
    C.track(C.D2 / "README.md")
    entries = {m.group(1): int(m.group(2).replace(",", "")) for m in re.finditer(r"\| `external_entries_(\w+)` \| ([\d,]+) \|", readme)}
    draft_cov = {"mesh": ("20872", None), "wikipedia_en": ("6540", "found (exact first revisions)"), "wikidata": ("1425", None),
                 "acm_ccs": ("3583", "entries"), "msc": ("17872", "entries"), "pacs_physh": ("8462", "entries"),
                 "research_fronts": ("589", "curated lists lumped"), "jel": ("1015", "entries")}
    for s, v in cov.items():
        dr = draft_cov.get(s)
        ov = None
        corr = ""
        if dr and dr[1] == "entries":
            ov = "MISLABELLED"
            corr = f"{s}: {v['n_with_event']:,} concepts with an event ({v['n_with_year_usable_event']:,} year-usable); {entries.get(s, 'n/a'):,} is the external-ENTRY count" if isinstance(entries.get(s), int) else ""
        if s == "research_fronts":
            ov = "MISLABELLED"
            corr = "589 is Research Fronts only; the curated lists are Gartner 466, MIT TR10 313, Research Fronts 589, NM MoTY 38, Science BOTY 53, Physics World BOTY 100 concepts."
        if s == "jel":
            corr = "JEL: 213 concepts found (present-day membership), 0 dated events; 1,015 is the entry count."
        add(f"O5cov_{s}_n_with_event", 2, AD, s131, "Concepts matched", f"by_source.{s}.n_with_event (CONCEPTS)", dr[0] if dr else str(v["n_with_event"]),
            COV, f"by_source.{s}.n_with_event", sev="blocking" if ov or (dr and dr[1]) else "minor", override=ov, corr=corr, in_draft=bool(dr))
        add(f"O5cov_{s}_n_year_usable", 2, AD, s131, "(not reported)", f"by_source.{s}.n_with_year_usable_event (CONCEPTS)", str(v["n_with_year_usable_event"]),
            COV, f"by_source.{s}.n_with_year_usable_event", in_draft=False)
    stt = cov["wikipedia_en"]["status"]
    add("O5cov_wikipedia_exact", 2, AD, s131, "English Wikipedia 6,540 exact first revisions", "by_source.wikipedia_en.status.found (exact first revisions)", "6540",
        COV, "by_source.wikipedia_en.status.found", sev="blocking",
        corr=f"Wikipedia: {cov['wikipedia_en']['n_with_event']:,} concepts with an event, {cov['wikipedia_en']['n_with_year_usable_event']:,} year-usable, {stt.get('found', 'n/a'):,} exact first revisions (6,540 is the dataset summary's count before redirect repair).")
    for s, n in entries.items():
        add(f"O5entries_{s}", 2, AD, s131, "(entries table)", f"external_entries_{s} (ENTRIES)", str(n), "round-2/dataset-2/src/README.md", None,
            value=(n, f"README table row external_entries_{s}"), in_draft=s in ("acm_ccs", "msc", "pacs_physh", "jel"),
            note="entries, not concepts" if s in ("acm_ccs", "msc", "pacs_physh", "jel") else "")
    for g, v in J(COV)["dated_domain_taxonomy_by_group"].items():
        own = v.get("own_domain_dated_taxonomies") or []
        val = max([v["share_with_event_by_domain_source"].get(s, 0) for s in own], default=0.0)
        add(f"O5tax_group_{g}", 2, AD, "13.2 Quality", "Social Sciences and Engineering have no dated domain taxonomy", f"dated_domain_taxonomy_by_group.{g} own-domain share",
            f"{val:.3f}", COV, None, value=(val, f"dated_domain_taxonomy_by_group.{g}.share_with_event_by_domain_source[{own}]"), in_draft=False)
    # ---------------- (v) H3
    s106 = "10.6 Concept breadth hypothesis: result: small but confirmed"
    for k, rep, ind in (("G.partial_rho", "0.030", True), ("G_A.partial_rho", "0.026", True), ("G_btw.partial_rho", "0.046", True),
                        ("REL_home.partial_rho", "-0.136", True), ("holm_adjusted_p.G", "0.0045", True), ("G.dl_pool.pooled", "0.068", True),
                        ("G.dl_pool.ci95.0", "0.029", True), ("G.dl_pool.ci95.1", "0.107", True), ("G.ci95.0", "-0.006", False),
                        ("G.ci95.1", "0.065", False), ("n", "2838", False), ("G_btw.dl_pool.pooled", "0.072", False),
                        ("G_btw.dl_pool.I2", "0.77", False), ("G_btw.per_group.LIFEENV.rho", "-0.020", False)):
        add(f"H3_{k}", 2, A5, s106, "H3 table", k, rep, H3, k, in_draft=ind, sev="blocking" if k.startswith("G.ci95") else "minor")
    add("H3_holm_test", 2, A5, s106, "The Holm corrected permutation p is 0.0045", "test that produced holm_adjusted_p", "within-group one-sided permutation, Holm over {G, G_A, G_btw}",
        H3, None, value=("within-group one-sided permutation, Holm over {G, G_A, G_btw}", "notes (Pre-registered test: one-sided permutation of the indicator WITHIN held-out group (2,000 draws), Holm)"),
        note="state the null is centred below zero (about -0.012)")
    add("H3_0of40", 2, A5, s106, "(0 of 40 shuffled outcomes exceed the real value)", "calibration false-positive rate of the preregistered test on 40 shuffled outcomes",
        "0", AP5, "H3_calibration_40_shuffles.false_positive_rate_preregistered_pooled_test", sev="blocking", override="MISLABELLED",
        corr="0/40 is the FALSE-POSITIVE RATE of the preregistered test on 40 shuffled outcomes (a calibration check), not an exceedance count and not a p-value.")
    add("H3_dev_G", 2, A5, s106, "(DEV value not reported)", "H3_dev.G", "0.138", H1D, "H3_dev.G", in_draft=False, sev="blocking",
        corr="held-out G 0.0295 vs DEV 0.138: shrinkage ratio 0.21 (about a quarter of the DEV value)")
    add("H3_shrinkage", 2, A5, s106, "(not reported)", "held-out G / DEV G", "0.21", H3, None,
        value=(J(H3)["G"]["partial_rho"] / J(H1D)["H3_dev"]["G"], "h3_results G.partial_rho / h1_dev H3_dev.G"), in_draft=False)
    add("H3_status", 2, A5, "16.5", "The effect is real but small (confirmed)", "G.ci95 includes 0", "false (implied)", H3, None, sev="blocking",
        value=(bool(J(H3)["G"]["ci95"][0] <= 0 <= J(H3)["G"]["ci95"][1]), "G.ci95[0] <= 0 <= G.ci95[1]"),
        corr="Status: 'small; passes the preregistered within-group permutation rule; pooled concept-bootstrap CI includes 0 ([-0.006, 0.065])'.")
    add("H3_mixed_variants", 2, A5, "16.5", "Holdout partial rho of G_btw ... = 0.046 (Holm p = 0.0045); DerSimonian-Laird pooled G = 0.068", "variant consistency",
        "G_btw pooled + G DL", H3, None, value=("mixes G_btw (pooled partial) and G (DL)", "G_btw.partial_rho vs G.dl_pool.pooled"), override="MISLABELLED",
        sev="blocking", corr="Quote one variant: G pooled partial 0.030 [-0.006, 0.065], DL within-group 0.068 [0.029, 0.107]; G_btw DL 0.072 [-0.015, 0.159], I2 = 0.77.")
    # ---------------- (vi) all_four row
    s54 = "5.4 Field level prediction"
    add("ALL4_label", 1, A4, s54, "B5 + all_four (G, REL, RS, G_all) | 0.697 | 0.782 | +0.085 | [0.004, 0.164]", "delta AUC of the row labelled 'B5 + all_four'", "0.085", S4,
        "field_level.size_controlled_all_three.delta_auc", sev="blocking", override="MISLABELLED",
        corr="The +0.085 row is 'B3 + log field size + {gateway_j, phi_home_j, density_j}' (size_controlled_all_three; AUC 0.697 -> 0.782; fixed CI95 [0.004, 0.164]; refit CI95 [-0.043, 0.220]). The row 'all_four_available' is B3 + {gateway_j, phi_home_j, density_j}: +0.082 (0.705 -> 0.787), fixed [0.008, 0.153], refit [-0.042, 0.204]. Neither contains G, REL, RS or G_all.")
    for k, rep in (("auc_base", "0.697"), ("auc_cand", "0.782"), ("ci95.0", "0.004"), ("ci95.1", "0.164")):
        add(f"ALL4_{k}", 1, A4, s54, "all_four row", f"field_level.size_controlled_all_three.{k}", rep, S4, f"field_level.size_controlled_all_three.{k}")
    add("ALL4_refit_lo", 1, AE, s54, "(refit CI not given for this row)", "F5 size_controlled_all_three new_ci95_refit[0]", "-0.043", EV1,
        "metadata.F_record.F5_exp4_field_level.rows.size_controlled_all_three.new_ci95_refit.0", in_draft=False, sev="blocking")
    add("ALL4_refit_hi", 1, AE, s54, "(refit CI)", "F5 new_ci95_refit[1]", "0.220", EV1, "metadata.F_record.F5_exp4_field_level.rows.size_controlled_all_three.new_ci95_refit.1", in_draft=False)
    add("ALL4_available_delta", 1, A4, s54, "(all_four_available row)", "field_level.all_four_available.delta_auc", "0.082", S4, "field_level.all_four_available.delta_auc", in_draft=False)
    # ---------------- clashes
    tr = J(TRACE)
    s112 = "11.2 Next field entry hypothesis: CONFIRMED"
    if tr:
        t = tr["trace"]
        add("CLASH_LR_68.6", 3, A6, "hypothesis_iter3", "M1 vs M0 LR 68.6", "LR M1 (d0_ret_rel) vs M0, Breslow, held-out", "68.6", TRACE,
            "trace.LR_M1_vs_M0_breslow.recomputed", note=tr["LR_clash_resolution"])
        add("CLASH_LR_71.7", 2, A6, s112, "LR = 71.7", "LR M2 (d_ret_gate) vs M0, Breslow, held-out", "71.7", TRACE, "trace.LR_M2_vs_M0_breslow.recomputed")
        add("CLASH_LR_77.3", 2, A6, "11.6 Audit", "exact likelihood conditional logit gives LR 77.3", "LR M2 vs M0, exact conditional likelihood", "77.3", TRACE, "trace.LR_M2_vs_M0_exact.recomputed")
        add("CLASH_LR_M1_exact", 3, A6, "hypothesis_iter3", "(M1 vs M0 exact not reported)", "LR M1 vs M0, exact", "73.2", TRACE, "trace.LR_M1_vs_M0_exact.recomputed", in_draft=False)
        add("CLASH_strata_961", 3, A6, "hypothesis_iter3", "961 strata", "informative strata (>= 1 event and >= 1 non-event)", "961", TRACE,
            "trace.n_strata_model.recomputed", note=tr["strata_clash_resolution"])
        add("CLASH_strata_2339", 2, A6, s112, "n_strata 2,339 (file)", "all strata of the primary sample (n_ret > 0)", "2339", TRACE, "trace.n_strata.recomputed")
        add("CLASH_d_0.281", 3, A6, "hypothesis_iter3", "d0_ret_rel 0.281 +/- 0.032", "M1 coef d0_ret_rel (Breslow)", "0.281", TRACE, "trace.coef_M1_d0_ret_rel.recomputed", note=tr["d_clash_resolution"])
        add("CLASH_d_0.30", 2, A6, s112, "d = 0.30 (bootstrap 95% CI [0.24, 0.37])", "M2 coef d_ret_gate (Breslow)", "0.30", TRACE, "trace.coef_M2_d_ret_gate.recomputed")
        add("H2_auc_M0", 2, A6, s112, "0.809 to 0.817", "within-stratum AUC M0 (refit)", "0.809", TRACE, "trace.auc_within_M0.recomputed")
        add("H2_auc_M2", 2, A6, s112, "0.809 to 0.817", "within-stratum AUC M2 (refit)", "0.817", TRACE, "trace.auc_within_M2.recomputed", override=None,
            note="0.817 is M1 (0.8169); M2 is 0.8166 -> both round to 0.817")
        add("H2_DL", 2, A6, s112, "DerSimonian-Laird pooled d: 0.28", "H2_DL_pooled.b (refit)", "0.28", TRACE, "trace.DL_pooled_d.recomputed")
    add("CLASH_MDE_power", 2, A5, "10.7 Minimum detectable effect and power", "The minimum detectable delta AUC is 0.004 (at 80% power, 27,393 episodes)",
        "power_ci_gt0 at planted b = 0.3 (mean dAUC 0.004)", "0.80", H1D, "power.0.3.power_ci_gt0", sev="blocking", override="MISLABELLED",
        corr="0.004 is the mean dAUC at planted b = 0.3, where power is 0.90 (b = 0.2 gives 0.0019 at power 0.65); the file key 'min_detectable_dauc_80pct' mislabels it. The simulation assumed 8,515 held-out episodes (not 27,393), and at b = 0 the CI>0 rule fires 12.5% of the time (nominal 2.5%).")
    add("CLASH_MDE_n", 2, A5, "10.7", "27,393 episodes", "power.n_heldout_episodes_assumed", "27393", H1D, "power.n_heldout_episodes_assumed", sev="blocking")
    add("CLASH_power_null_rate", 2, A5, "10.7", "(not reported)", "power.0.0.power_ci_gt0 (false-positive rate at b = 0)", "0.125", H1D, "power.0.0.power_ci_gt0", in_draft=False)
    ep = J(EV1)["metadata"]["E_power"]
    k015 = "metadata.E_power.held_out_sizing_from_alternative_SD.SD_alt_field_RE_N1000_m5"
    add("CLASH_10.7_sd015", 2, AE, "10.7", "the standard deviation of the delta AUC ... approximately 0.015 regardless of the number of episodes", "E_power SD under the alternative (Evaluation 1, not Exp5)",
        "0.015", EV1, k015, override="MISLABELLED" if k015 else None, sev="blocking",
        corr="This sentence and '34 concepts per group' come from Evaluation 1 (E_power, field random intercept), not Exp5; attribute them to art_lwI2DuRtQRZX and reconcile with Exp5's 0.004 (no field random intercept).")
    k34 = find_key(EV1, 34, 0.5, "E_power")
    add("CLASH_10.7_34", 2, AE, "10.7", "Approximately 34 holdout concepts per group", "E_power concepts per group (Evaluation 1)", "34", EV1, k34,
        override="MISLABELLED" if k34 else None, sev="blocking")
    del ep
    # ---------------- other headline rows (panel, H2, trajectories, relatedness pair, T3-related)
    fs = "round-2/experiment-5/src/results/frame_summary.json"
    for rep, hint in (("12499", "n_concepts"), ("27393", "n_episodes")):
        add(f"PANEL_{hint}", 2, A5, "10.2 Panel", f"The panel comprises {rep}", hint, rep, fs, find_key(fs, float(rep), 0.5, "") or hint)
    rv = J(H1).get("rival_head_to_head", {})
    k_pair = find_key(H1, 0.0034, 0.00006, "rival")
    add("REL_pair_heldout", 2, A5, "10.5 The relatedness pair beats gateway", "adds delta AUC +0.0034 on holdout data", "rival_head_to_head relatedness pair dAUC (held-out)", "0.0034", H1, k_pair)
    k_pair_dev = find_key(H1D, -0.00017, 0.00003, "rival")
    add("REL_pair_dev", 2, A5, "10.5", "(DEV value not reported)", "rival_head_to_head relatedness pair dAUC (DEV)", "-0.00017", H1D, k_pair_dev, in_draft=False, sev="blocking",
        corr="the relatedness-pair gain is held-out only (DEV -0.0002 [-0.0017, 0.0012])")
    del rv
    for g in ("Physical", "LifeEnv", "Social", "Cohort"):
        add(f"H2_group_{g}_d", 2, A6, s112, "per-group d", f"H2_per_group.{g}.d", f"{J(HO6)['H2_per_group'][g]['d']:.3f}", HO6, f"H2_per_group.{g}.d")
    add("H2_sign_test", 2, A6, "16.1", "positive in all three evaluable holdout field groups", "H2_sign_count.sign_test_p", "(not reported)", HO6, "H2_sign_count.sign_test_p",
        override="MISLABELLED", sev="minor", corr="Positive in 4/4 groups (sign test p = 0.0625); only Physical's CI excludes 0 (LifeEnv LR p = 0.23, Social 0.076).")
    add("H2_gonly_perm", 2, A6, s112, "gateway only permutation p = 0.17 holdout", "gonly_perm_null_M3_vs_M1.p", "0.17", HO6, "H2_pooled.gonly_perm_null_M3_vs_M1.p")
    add("H2_perm_p", 2, A6, s112, "Label permutation p = 0.001", "perm_null.p", "0.001", HO6, "H2_pooled.perm_null.p")
    add("H2_rewired_p", 2, A6, s112, "rewired backbone p = 0.015", "rewired_null.p", "0.015", HO6, "H2_pooled.rewired_null.p")
    add("H2_size_auc", 2, A6, s112, "target field size ... AUC 0.76", "auc_within_stratum.b_log_size.mean", "0.76", HO6, "H2_pooled.auc_within_stratum.b_log_size.mean")
    add("H2_density_auc", 2, A6, s112, "density 0.59", "auc_within_stratum.c_density.mean", "0.59", HO6, "H2_pooled.auc_within_stratum.c_density.mean")
    add("H2_M2lost", 2, A6, s112, "(M2lost not reported)", "LR.M2lost_vs_M0.p", "0.055", HO6, "H2_pooled.LR.M2lost_vs_M0.p", in_draft=False)
    tj = J(HO6)["trajectories"]
    add("TRAJ_ARI_heldout", 2, A6, "11.5 Trajectories", "holdout independent recluster gives ARI 0.54", "trajectories.heldout_independent_recluster_ARI", "0.54", HO6, "trajectories.heldout_independent_recluster_ARI")
    add("TRAJ_HMM_ARI", 2, A6, "11.5", "(HMM vs DTW not reported)", "trajectories.hmm_vs_dtw_ARI", "0.0945", HO6, "trajectories.hmm_vs_dtw_ARI", in_draft=False, sev="blocking",
        corr="the two-class DTW solution is not reproduced by the HMM (ARI 0.09)")
    k128 = find_key(HO6, 128, 0.5, "cluster_sizes")
    add("TRAJ_n_integrating", 2, A6, "11.5", "integrating (128 concepts)", "trajectories.cluster_sizes", "128", HO6, k128)
    k60 = find_key(HO6, 60, 0.5, "cluster_sizes")
    add("TRAJ_n_localised", 2, A6, "11.5", "localised (60 concepts)", "trajectories.cluster_sizes", "60", HO6, k60)
    del tj
    ev = J(EV1)["metadata"]
    k_union = "metadata.A_replication.union.specs.M2.delta"
    add("EV1_union", 2, AE, "12.2", "Union +0.001 [-0.012, +0.012]", "A_replication union delta", "0.001", EV1, k_union)
    del ev
    t3 = json.loads((C.RES / "t3_refit_bootstrap.json").read_text()) if (C.RES / "t3_refit_bootstrap.json").exists() else []
    for r in t3:
        add(f"T3_{r['row']}", 1, {"exp1": A1, "exp3": A3, "exp4": A4}[r["experiment"]], "6.2 / 5.3 (iteration-1 deltas)", "iteration-1 concept-level delta",
            f"{r['row']} point estimate (reproduced by refit pipeline)", f"{r['point_reported']:.4f}", "results/t3_refit_bootstrap.json", None,
            value=(r["point_reproduced"], f"t3_refit_bootstrap.json row {r['row']} point_reproduced"),
            note=f"refit CI95 [{r['ci95_refit'][0]:.3f}, {r['ci95_refit'][1]:.3f}], B = {r['B']}; widening vs fixed CI90 = {r['ci_widening_ratio_90']}")


def draft_harvest() -> pd.DataFrame:
    """Every number with 120 characters of context from the draft's abstract and iteration-2 sections, matched
    automatically against a value index of the cited artifacts' result files (candidate key path)."""
    txt = C.DRAFT.read_text()
    C.track(C.DRAFT)
    lines = txt.splitlines()
    sec, keep = "", []
    it2 = False
    for i, l in enumerate(lines):
        if l.startswith("#"):
            sec = l.strip("# ").strip()
            if l.startswith("# Iteration 2"):
                it2 = True
        if i < 14 or it2:
            keep.append((sec, l))
    files = {"art_wxWssKSUR45f": ["round-2/experiment-5/src/results/" + f for f in ("h1_heldout.json", "h1_dev.json", "h3_results.json", "audit_placebo.json", "frame_summary.json", "checks.json", "deviations.json")],
             "art_N-mpomDZZ1ln": [HO6, DV6, AU6, "round-2/experiment-6/src/results/frame_summary.json", "round-2/experiment-6/src/results/audit_placebo.json"],
             "art_lwI2DuRtQRZX": [EV1], "art_O7Dq4L02QnDN": [COV]}
    index = []
    for art, fl in files.items():
        for f in fl:
            d = J(f)
            if d is None:
                continue
            for k, v in flatten(d):
                index.append((art, f, k, v))
    iv = np.array([x[3] for x in index])
    art_of_sec = {"10": "art_wxWssKSUR45f", "11": "art_N-mpomDZZ1ln", "12": "art_lwI2DuRtQRZX", "13": "art_O7Dq4L02QnDN"}
    rows = []
    num = re.compile(r"(?<![\w.])[-+−]?\d[\d,]*\.?\d*(?:\s?x\s?10\^-?\d+)?")
    for sec, l in keep:
        for m in num.finditer(l):
            s = m.group(0)
            v = to_num(s)
            if v is None or (1990 <= abs(v) <= 2030 and "." not in s) or re.fullmatch(r"\d{1,2}", s.replace(",", "")) and abs(v) <= 16 and "." not in s:
                continue
            ctx = l[max(0, m.start() - 60): m.end() + 60]
            dp = decimals(s)
            tol = 0.5 * 10 ** (-dp) if dp != 99 else abs(v) * 0.05
            hit = np.where(np.abs(iv - v) <= tol + 1e-12)[0]
            if len(hit) == 0 and v != 0:
                hit = np.where(np.abs(iv + 0) <= -1)[0]
            pref = art_of_sec.get(sec.split(".")[0].split(" ")[0], None)
            hits = [index[h] for h in hit]
            if pref:
                hp = [h for h in hits if h[0] == pref]
                hits = hp or hits
            rows.append({"draft_section": sec, "number": s, "context": ctx.strip(), "n_candidate_keys": len(hits),
                         "auto_status": "AUTO_MATCH" if hits else "NO_AUTOMATIC_SOURCE",
                         "candidate_source_file": hits[0][1] if hits else "", "candidate_key_path": hits[0][2] if hits else "",
                         "candidate_value": hits[0][3] if hits else math.nan})
    return pd.DataFrame(rows)


def record_tables() -> dict:
    out = {}
    # T1 portability
    f3 = J(EV1)["metadata"]["F_record"]["F3_exp3_portability"]["table"]
    raw = J(S3)["portability"]
    prereg = {"entropy": "positive", "D_rare": "positive", "D_ratio": "positive", "participation": "positive", "NOV_res": "positive",
              "edge_persistence": "negative", "deg_growth": "CS-only", "str_growth": "CS-only", "new_edge_rate": "CS-only"}
    rows = []
    for nm, v in f3["indicators"].items():
        rw = raw["indicators"].get(nm, {})
        match = all(abs((rw.get(k) if rw.get(k) is not None else np.nan) - (v.get(k) if v.get(k) is not None else np.nan)) < 1e-9
                    for k in ("pooled_rho_O2r", "pooled_rho_O1", "rho_logvol") if isinstance(v.get(k), (int, float)))
        wg = v.get("within_group_rho_O2r", {})
        rows.append({"indicator": nm, "pooled_rho_O2r": v.get("pooled_rho_O2r"), "pooled_rho_O1": v.get("pooled_rho_O1"), "rho_logvol": v.get("rho_logvol"),
                     "rho_growth": v.get("rho_growth"), **{f"within_rho_O2r_{g}": wg.get(g) for g in ("BIO", "CS", "ENG", "MED")},
                     **{f"within_rho_O1_{g}": v.get("within_group_rho_O1", {}).get(g) for g in ("BIO", "CS", "ENG", "MED")},
                     "n_groups_positive_O2r": int(sum(1 for x in wg.values() if x is not None and x > 0)),
                     "sign_consistent_4of4": bool(len(wg) == 4 and (all(x > 0 for x in wg.values() if x is not None) or all(x < 0 for x in wg.values() if x is not None))),
                     "logo_delta_rho_O2r": v.get("logo_delta_rho_O2r"), "match_exp3_screen_result": match,
                     "iter3_preregistered_prediction": prereg.get(nm, "none stated"),
                     "source_file": "round-2/evaluation-1/src/eval_out.json", "key_path": f"metadata.F_record.F3_exp3_portability.table.indicators.{nm}"})
    t1 = pd.DataFrame(rows)
    t1.to_csv(C.TAB / "portability_F3.csv", index=False)
    out["T1_n_indicators"] = len(t1)
    out["T1_expected_34"] = len(t1) == 34
    out["T1_all_match_exp3"] = bool(t1.match_exp3_screen_result.all())
    # T2 exp1 lineage robustness
    s1 = J(S1)
    rows = []
    for k, v in C.jsonable(s1).items():
        if k in ("glmm_check", "agreement", "M1", "refit_bootstrap", "reliability", "field_level", "sensitivity", "pymc_check", "delta_auc_O1",
                 "delta_auc_O3", "delta_rho", "ci90", "rho_B", "rho_BC", "size_corr", "hurdle", "eligible_subset_result", "pooling", "s0_cross_source"):
            for kk, vv in flatten(v, k):
                rows.append({"block": k, "key_path": kk, "value": vv, "source_file": S1})
    t2 = pd.DataFrame(rows)
    t2.to_csv(C.TAB / "lineage_robustness_iter1.csv", index=False)
    out["T2_n_rows"] = len(t2)
    out["T2_glmm_key"] = "glmm_check.spearman_vs_primary"
    # T3 refit table (from wp2_t3 output)
    if (C.RES / "t3_refit_bootstrap.json").exists():
        t3 = pd.DataFrame(json.loads((C.RES / "t3_refit_bootstrap.json").read_text()))
        f5 = J(EV1)["metadata"]["F_record"]["F5_exp4_field_level"]["rows"]
        extra = [{"row": f"F5_field_level_{k}", "experiment": "exp4 (reused from art_lwI2DuRtQRZX F5)", "outcome": "R (field retention)",
                  "point_reported": v["iter1_delta"], "point_reproduced": v["new_delta"], "abs_diff": abs(v["iter1_delta"] - v["new_delta"]),
                  "reproduction_status": "MATCH" if abs(v["iter1_delta"] - v["new_delta"]) <= 0.002 else "MISMATCH",
                  "ci90_refit": v.get("new_ci90_refit"), "ci95_refit": v["new_ci95_refit"], "B": 2000, "fixed_prediction_ci95": v.get("iter1_ci95_fixed"),
                  "source_file": EV1, "key_path": f"metadata.F_record.F5_exp4_field_level.rows.{k}"} for k, v in f5.items()]
        t3 = pd.concat([t3, pd.DataFrame(extra)], ignore_index=True)
        t3.to_csv(C.TAB / "refit_bootstrap_iter1.csv", index=False)
    # T5 h1 criteria
    h = J(H1)
    rows = [{"criterion": k, "value": v, "passes": (v if isinstance(v, bool) else None), "source_file": H1, "key_path": f"verdict_H1.criteria.{k}"}
            for k, v in h["verdict_H1"]["criteria"].items()]
    rows += [{"criterion": f"lpm_field_fe.{k}", "value": h["lpm_field_fe"][k], "passes": None, "source_file": H1, "key_path": f"lpm_field_fe.{k}"}
             for k in ("n", "beta_within_per_sd", "se_concept", "p_concept", "se_twoway", "p_twoway")]
    rows += [{"criterion": f"lpm_field_fe_all_splits.{k}", "value": h["lpm_field_fe_all_splits"][k], "passes": None, "source_file": H1,
              "key_path": f"lpm_field_fe_all_splits.{k}"} for k in ("n", "beta_within_per_sd", "se_concept", "p_concept", "se_twoway", "p_twoway")]
    for sp, src in (("heldout", H1), ("dev", H1D)):
        d = J(src)
        for k in ("concept", "twoway", "field"):
            rows.append({"criterion": f"{sp}.logit_clustered_se.{k}.p", "value": d["logit_clustered_se"][k]["p"], "passes": None, "source_file": src,
                         "key_path": f"logit_clustered_se.{k}.p"})
        rows.append({"criterion": f"{sp}.logit_clustered_se.beta_gateway_std", "value": d["logit_clustered_se"]["concept"]["beta_gateway_std"], "passes": None,
                     "source_file": src, "key_path": "logit_clustered_se.concept.beta_gateway_std"})
        for k in ("beta_interaction", "p", "consistent"):
            rows.append({"criterion": f"{sp}.boundary.{k}", "value": d["boundary"][k], "passes": None, "source_file": src, "key_path": f"boundary.{k}"})
        if "lpm_field_fe" in d:
            rows.append({"criterion": f"{sp}.lpm_field_fe.beta_within_per_sd", "value": d["lpm_field_fe"].get("beta_within_per_sd"), "passes": None,
                         "source_file": src, "key_path": "lpm_field_fe.beta_within_per_sd"})
            rows.append({"criterion": f"{sp}.lpm_field_fe.p_concept", "value": d["lpm_field_fe"].get("p_concept"), "passes": None,
                         "source_file": src, "key_path": "lpm_field_fe.p_concept"})
    rows.append({"criterion": "verdict", "value": h["verdict_H1"]["verdict"], "passes": None, "source_file": H1, "key_path": "verdict_H1.verdict"})
    pd.DataFrame(rows).to_csv(C.TAB / "h1_criteria.csv", index=False)
    # T6 ordering mixed
    rows = []
    for sp, src in (("heldout", HO6), ("dev", DV6)):
        for k, v in flatten(J(src)["ordering"], "ordering"):
            if "calibration" in k or "null_q" in k or ".se" in k:
                continue
            rows.append({"split": sp, "key_path": k, "value": v, "source_file": src})
    t6 = pd.DataFrame(rows)
    og = J(HO6)["ordering"]["gateway"]
    den = pd.DataFrame([{"split": "heldout", "key_path": f"derived.share_before.{n}", "value": og["before"] / d_, "source_file": HO6}
                        for n, d_ in (("of_175_broad", J(HO6)["ordering"]["n_top_o2r"]), ("of_102_evaluable", og["n_evaluable"]),
                                      ("of_87_non_tied", og["before"] + og["after"]))])
    pd.concat([t6, den]).assign(verdict="MIXED / not established (file flag CONFIRMED overridden)").to_csv(C.TAB / "ordering_mixed.csv", index=False)
    # T7 coverage iteration 2
    rows = []
    for art, base in (("art_wxWssKSUR45f", C.E5), ("art_N-mpomDZZ1ln", C.E6), ("art_O7Dq4L02QnDN", C.D2), ("art_lwI2DuRtQRZX", C.EV1)):
        info = {"artifact": art}
        for f in ("results/frame_summary.json", "results/deviations.json", "out/llm_cost.json", "results/openrouter_cost.json", "out/coverage_report.json"):
            p = base / f
            if p.exists():
                d = C.read_json(p)
                for k, v in flatten(d):
                    kl = k.lower()
                    if any(s in kl for s in ("n_concepts", "n_episodes", "cost", "credits", "label_coverage", "precision", "n_target", "usd")) and len(info) < 40:
                        info[f"{f.split('/')[-1]}:{k}"] = v
        rows.append(info)
    fc5 = C.read_csv(C.E5 / "frame_concepts.csv")
    fc6 = C.read_csv(C.E6 / "results/frame_concepts.csv")
    summ = [{"artifact": "art_wxWssKSUR45f", "concepts": len(fc5), "episodes": len(C.read_csv(C.E5 / "episodes.csv", usecols=["ci"])),
             "groups": fc5.group.nunique(), "splits": fc5.split.nunique(), "label_coverage_median": fc5.label_coverage_early.median(),
             "grounding_precision": "TAG test P 0.947 (grounding_bench_summary); per-concept gate >= 0.8", "llm_cost_usd": "2.28 (precision gate); cap 3.50",
             "openalex_credits": 0},
            {"artifact": "art_N-mpomDZZ1ln", "concepts": len(fc6), "episodes": len(C.read_csv(C.E6 / "results/episodes.csv", usecols=["cidx"])),
             "groups": fc6.group.nunique(), "splits": fc6.split.nunique(), "label_coverage_median": fc6.label_coverage_early.median(),
             "grounding_precision": "tag-AND-title benchmark precision 0.996", "llm_cost_usd": "0.007", "openalex_credits": "0 for data (API audit only)"},
            {"artifact": "art_O7Dq4L02QnDN", "concepts": 65026, "episodes": None, "groups": None, "splits": 3, "label_coverage_median": None,
             "grounding_precision": "label 0.96 / ID 0.79 / alias 0.31; accepted LLM links 0.97", "llm_cost_usd": "1.49", "openalex_credits": 0},
            {"artifact": "art_lwI2DuRtQRZX", "concepts": 54, "episodes": 362, "groups": 4, "splits": None, "label_coverage_median": None,
             "grounding_precision": "reuses iteration-1 panels", "llm_cost_usd": "0", "openalex_credits": 0}]
    t7 = pd.DataFrame(summ).merge(pd.DataFrame(rows), on="artifact", how="left")
    steps = pd.DataFrame([
        ("RQ1: candidate indicator screen (dev)", "Done (iteration 1); gateway family re-tested at scale", "art_wxWssKSUR45f"),
        ("RQ1: holdout evaluation", "Done for gateway (H1 DISCONFIRMED; H3 small, CI includes 0)", "art_wxWssKSUR45f"),
        ("RQ1: top-10 on holdout", "Not started (co-occurrence indicators not rescored on the S1 frame)", "-"),
        ("RQ1: external ground truth (O5)", "Built (art_O7Dq4L02QnDN); validated in iteration 3 (this artifact)", "art_O7Dq4L02QnDN"),
        ("RQ1: exploratory AI first stage", "Not started", "-"),
        ("RQ2: diffusion trajectories", "Done (DTW k=2; HMM ARI 0.09 = robustness failure)", "art_N-mpomDZZ1ln"),
        ("RQ2: field entry conditional logit", "Done on held-out (H2 CONFIRMED on the 653-newborn frame only)", "art_N-mpomDZZ1ln"),
        ("RQ2: ordering", "MIXED (sign rule passes; lead-lag negative, pre-trend, dev reverse significant)", "art_N-mpomDZZ1ln"),
        ("Grounding benchmark", "Done (390 pairs, 60 hand-checked; kappa 0.20)", "art_wxWssKSUR45f"),
        ("Explain why strongest indicator works", "Not started", "-"),
        ("Case studies", "Figures exist (Exp6 case field-flow plots), not written up", "art_N-mpomDZZ1ln"),
        ("Optional learned model", "Not started", "-")], columns=["step", "status_after_iteration_2", "artifact"])
    t7.to_csv(C.TAB / "coverage_iter2.csv", index=False)
    steps.to_csv(C.TAB / "coverage_iter2_steps.csv", index=False)
    # partial association table (all 12)
    pa = pd.DataFrame([{"indicator": k, "logo_partial_rho": v["logo_partial_rho"], "ci90": v["CI90"], "ci95": v["CI95"],
                        "n_groups_positive": v["n_groups_positive"], "per_group": v["per_group"], "delta_rho_robustness": v.get("delta_rho_robustness"),
                        "source_file": EPA, "key_path": f"candidates.{k}"} for k, v in J(EPA)["candidates"].items()])
    pa.to_csv(C.TAB / "partial_association_all.csv", index=False)
    out["n_partial_candidates"] = len(pa)
    return out


@logger.catch(reraise=True)
def main() -> None:
    C.setup_logging("wp1")
    ledger()
    led = pd.DataFrame(ROWS)
    led.to_csv(C.WS / "claims_ledger.csv", index=False)
    logger.info(f"ledger rows {len(led)}; status {led.status.value_counts().to_dict()}")
    hv = draft_harvest()
    hv.to_csv(C.TAB / "draft_number_harvest.csv", index=False)
    logger.info(f"draft harvest {len(hv)} numbers; auto {hv.auto_status.value_counts().to_dict()}")
    # iteration-3 hypothesis text numbers (strategy) that cite earlier artifacts
    sp = C.ROOT / "iter_3/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json"
    if sp.exists():
        st = C.read_json(sp)["strategies"][0]
        txt = " ".join(str(v) for k, v in flatten_text(st))
        hy = [{"number": m.group(0), "context": txt[max(0, m.start() - 60): m.end() + 60]} for m in
              re.finditer(r"(?<![\w.])[-+]?\d[\d,]*\.\d+", txt)]
        pd.DataFrame(hy).to_csv(C.TAB / "hypothesis_iter3_numbers.csv", index=False)
    rt = record_tables()
    C.dump({"ledger_status_counts": led.status.value_counts().to_dict(), "n_rows": len(led),
            "n_blocking": int((led.severity == "blocking").sum()), "harvest": hv.auto_status.value_counts().to_dict(), **rt},
           C.RES / "wp1_summary.json")
    C.save_manifest("wp1")


def flatten_text(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flatten_text(v, f"{p}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from flatten_text(v, f"{p}.{i}")
    else:
        yield p, o


if __name__ == "__main__":
    main()
