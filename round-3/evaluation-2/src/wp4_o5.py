#!/usr/bin/env python3
"""WP4: validate external recognition (O5, art_O7Dq4L02QnDN) on the Exp5 frame: pre-declared variants, coverage and
base rate per group x source, precedence/leakage flags, recognition lag (Kaplan-Meier), and association with the
publication outcomes (concept bootstrap B = 2000, per group, DL-pooled over the held-out groups, partial given B5)."""
from __future__ import annotations

import os

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json
import math
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats

import common as C

CURATED = ["gartner_hype_cycle", "mit_tr10", "nature_methods_moty", "science_boty", "physics_world_boty", "research_fronts"]
TAXO = ["acm_ccs", "msc", "pacs_physh"]
WINDOW = 8
DEFINITIONS = {
    "written_before_any_association": True,
    "common_conditions": "year_usable == true AND t0 < year <= t0 + 8 (t0 = Exp5 frame onset)",
    "qualifying_event_types": {
        "mesh": "event_type == mesh_descriptor_introduced AND detail.mesh_baseline is not true AND year > 1966 "
                "(supplementary records mesh_supplementary_record_introduced excluded: not descriptors)",
        "wikipedia_en": "event_type in {wikipedia_article_created (exact first revision), wikipedia_page_created_estimated}",
        "wikidata": "event_type in {wikidata_inception (P571), wikidata_discovery_or_invention (P575)}",
        "taxonomies": "acm_ccs / msc / pacs_physh event_type == taxonomy_added_between (taxonomy_in_version is a membership, not an addition date)",
        "curated_lists": "gartner_hype_cycle, mit_tr10, nature_methods_moty, science_boty, physics_world_boty, research_fronts (any listed event)",
        "excluded": "jel (present-day membership only, no dated events)"},
    "variants": {
        "O5_main": "1 if >= 1 qualifying event with relation == 'same' from MeSH / Wikipedia / Wikidata / taxonomy_added_between / curated lists",
        "O5_wiki": "O5_main restricted to wikipedia_en + wikidata (the only sources that run in every group)",
        "O5_tax": "O5_main restricted to dated taxonomies (mesh descriptor + acm_ccs/msc/pacs_physh taxonomy_added_between)",
        "O5_anyrel": "O5_main with relation in {same, narrower, broader}",
        "O5_main_noRF": "ADDITIONAL (declared here, before results): O5_main without research_fronts, which are citation-derived (leakage risk)",
        "O5_lag": "year of the first qualifying (relation same) event minus t0, for O5_main positives"},
    "outcomes": {"O1": "concept_outcomes.csv", "O2r_m50": "concept_outcomes.csv", "O3": "concept_outcomes.csv",
                 "O2r_resid": "O2r_m50 residualised on log N_outcome by OLS within Exp5 split (Exp5 has no O2r_resid column)",
                 "log_N_outcome": "log N_outcome", "log_early_volume": "log frame_concepts.early_volume"},
    "B5_for_partial": ["logvol", "growth_c", "offhome_share", "entropy", "reach"],
    "bootstrap": {"unit": "concept", "B": 2000, "seed": 20260928},
    "reading_rule": {"DUPLICATE": "|pooled rho| >= 0.8 for any publication outcome",
                     "RELATED_NOT_DUPLICATE": "pooled rho with O2r_m50 or O1 has 95% CI > 0 and |rho| < 0.8",
                     "UNRELATED": "pooled CI covers 0 for all of O1, O2r_m50 and O2r_resid",
                     "pooled": "DerSimonian-Laird across the 4 held-out groups (PHYS, LIFEENV, SOC, MATHDEC), bootstrap SEs"},
    "precedence_flag": "source flagged if > 30% of matched concepts have their first usable same-relation event at or before t0",
    "fit_for_use_rule": "positive precision >= 0.85 AND date error <= 1 year in >= 80% of checked positives (hand check)",
}
HELD = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]


def qualifies(e: dict, rels=("same",)) -> bool:
    if not e.get("year_usable") or e.get("year") is None or e.get("relation") not in rels:
        return False
    s, t = e["source"], e["event_type"]
    if s == "mesh":
        return t == "mesh_descriptor_introduced" and not e.get("mesh_baseline") and e["year"] > 1966
    if s == "wikipedia_en":
        return t in ("wikipedia_article_created", "wikipedia_page_created_estimated")
    if s == "wikidata":
        return t in ("wikidata_inception", "wikidata_discovery_or_invention")
    if s in TAXO:
        return t == "taxonomy_added_between"
    return s in CURATED


def src_class(s: str) -> str:
    return "wiki" if s in ("wikipedia_en", "wikidata") else ("tax" if s in TAXO + ["mesh"] else ("list" if s in CURATED else "other"))


def build(rows: list[dict], fr: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    t0 = fr.set_index("id").t0.to_dict()
    recs, evrows = [], []
    for r in rows:
        c = r["openalex_id"]
        T = t0[c]
        v = {"id": c, "n_events": len(r["events"])}
        firsts = {}
        for e in r["events"]:
            y = e.get("year")
            evrows.append({"id": c, "source": e["source"], "event_type": e["event_type"], "year": y, "relation": e["relation"],
                           "year_usable": e["year_usable"], "match_method": e["match_method"], "date_precision": str(e["date_precision"]),
                           "qual_any_window": qualifies(e, ("same",)), "qual_anyrel": qualifies(e, ("same", "narrower", "broader")),
                           "mesh_baseline": e.get("mesh_baseline"), "t0": T, "title": e.get("detail_title"), "entry_id": e.get("entry_id"),
                           "date": e.get("date")})
        ev = pd.DataFrame([x for x in evrows[-len(r["events"]):]]) if r["events"] else pd.DataFrame()
        inw = lambda y: y is not None and T < y <= T + WINDOW  # noqa: E731
        def any_(pred):
            return int(any(pred(e) and inw(e.get("year")) for e in r["events"]))
        v["O5_main"] = any_(lambda e: qualifies(e))
        v["O5_wiki"] = any_(lambda e: qualifies(e) and e["source"] in ("wikipedia_en", "wikidata"))
        v["O5_tax"] = any_(lambda e: qualifies(e) and (e["source"] in TAXO or e["source"] == "mesh"))
        v["O5_anyrel"] = any_(lambda e: qualifies(e, ("same", "narrower", "broader")))
        v["O5_main_noRF"] = any_(lambda e: qualifies(e) and e["source"] != "research_fronts")
        q = [e["year"] for e in r["events"] if qualifies(e) and inw(e["year"])]
        v["O5_lag"] = (min(q) - T) if q else math.nan
        qa = [e["year"] for e in r["events"] if qualifies(e)]
        v["first_qual_year_any"] = min(qa) if qa else math.nan
        qa_after = [y for y in qa if y > T]
        v["first_qual_year_after_t0"] = min(qa_after) if qa_after else math.nan
        v["any_usable_event"] = int(any(e.get("year_usable") for e in r["events"]))
        for s, st in r["sources_checked"].items():
            v[f"chk_{s}"] = st
        recs.append(v)
        del ev
    return pd.DataFrame(recs), pd.DataFrame(evrows)


# ------------------------------------------------------------------ association workers
OUTS = ["O1", "O2r_m50", "O2r_resid", "O3", "log_N_outcome", "log_early_volume"]


def _rank(x):
    return stats.rankdata(x)


def _sp_fast(x, y) -> float:
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 4:
        return math.nan
    a, b = stats.rankdata(x[ok]), stats.rankdata(y[ok])
    if a.std() == 0 or b.std() == 0:
        return math.nan
    return float(np.corrcoef(a, b)[0, 1])


def _psp_fast(x, y, Z) -> float:
    ok = np.isfinite(x) & np.isfinite(y) & np.isfinite(Z).all(1)
    if ok.sum() < 10:
        return math.nan
    R = np.column_stack([stats.rankdata(x[ok]), stats.rankdata(y[ok])] + [stats.rankdata(Z[ok, j]) for j in range(Z.shape[1])])
    M = np.column_stack([np.ones(ok.sum()), R[:, 2:]])
    coef = np.linalg.lstsq(M, R[:, :2], rcond=None)[0]
    E = R[:, :2] - M @ coef
    if E[:, 0].std() == 0 or E[:, 1].std() == 0:
        return math.nan
    return float(np.corrcoef(E[:, 0], E[:, 1])[0, 1])


def _stats(o5, Y: dict, Z) -> dict:
    out = {}
    for k, y in Y.items():
        out[f"rho_{k}"] = _sp_fast(o5, y)
    for k in ("O2r_m50", "O2r_resid"):
        out[f"auc_{k}"] = C.auc(o5, Y[k])
    for k in ("O1", "O2r_m50", "O2r_resid", "O3"):
        out[f"prho_{k}_B5"] = _psp_fast(o5, Y[k], Z)
    return out


def assoc_task(args):
    name, var, o5, Y, Z, B, seed = args
    pt = _stats(o5, Y, Z)
    rng = np.random.default_rng(seed)
    n = len(o5)
    boots = {k: [] for k in pt}
    for _ in range(B):
        i = rng.integers(0, n, n)
        s = _stats(o5[i], {k: v[i] for k, v in Y.items()}, Z[i])
        for k, v in s.items():
            boots[k].append(v)
    res = {"group": name, "variant": var, "n": int(n), "n_pos": int(o5.sum()), "base_rate": float(o5.mean()) if n else math.nan}
    for k, v in pt.items():
        b = np.asarray(boots[k], float)
        b = b[np.isfinite(b)]
        res[k] = v
        res[f"{k}_ci95"] = C.pct_ci(b)
        res[f"{k}_se"] = float(b.std(ddof=1)) if len(b) > 2 else math.nan
    ok = np.isfinite(Y["O1"])
    for k in ("O1", "O2r_m50", "O2r_resid", "O3"):
        okk = np.isfinite(Y[k])
        res[f"p_rho_{k}"] = float(stats.spearmanr(o5[okk], Y[k][okk]).pvalue) if okk.sum() > 3 and o5[okk].std() > 0 else math.nan
    del ok
    return res


def km(time_, event) -> list[dict]:
    t = np.asarray(time_, float)
    e = np.asarray(event, int)
    out, S = [], 1.0
    for u in np.unique(t[e == 1]):
        at_risk = (t >= u).sum()
        d = ((t == u) & (e == 1)).sum()
        S *= 1 - d / at_risk
        out.append({"years_since_t0": int(u), "cum_incidence": 1 - S, "at_risk": int(at_risk), "events": int(d)})
    return out


@logger.catch(reraise=True)
def main(B: int = C.B_MAIN, workers: int = 40) -> None:
    C.setup_logging("wp4")
    C.dump(DEFINITIONS | {"written_at": time.strftime("%Y-%m-%d %H:%M:%S")}, C.WS / "o5_definitions.json")
    logger.info("o5_definitions.json written before any association is computed")
    fr = C.read_csv(C.E5 / "frame_concepts.csv")
    fr["id"] = fr.concept_id.map(C.norm_id)
    fr["gkey"] = np.where(fr.split == "DEV", "DEV_" + fr.group.astype(str), np.where(fr.split == "COHORT", "COHORT", fr.group.astype(str)))
    oc = C.read_csv(C.E5 / "concept_outcomes.csv")
    fb = C.read_csv(C.E5 / "concept_features_basic.csv")
    rows = [json.loads(l) for l in open(C.RES / "o5_joined.jsonl")]
    rec, ev = build(rows, fr)
    df = fr.merge(rec, on="id", how="left").merge(oc[["ci", "O1", "O3", "N_outcome", "O2r_m50"]], on="ci").merge(
        fb[["ci"] + DEFINITIONS["B5_for_partial"]], on="ci")
    df["log_N_outcome"] = np.log(df.N_outcome.clip(lower=1))
    df["log_early_volume"] = np.log(df.early_volume)
    df["O2r_resid"] = np.nan
    for sp, g in df.groupby("split"):
        ok = g.O2r_m50.notna() & g.log_N_outcome.notna()
        X = np.column_stack([np.ones(ok.sum()), g.loc[ok, "log_N_outcome"]])
        b = np.linalg.lstsq(X, g.loc[ok, "O2r_m50"].to_numpy(float), rcond=None)[0]
        df.loc[g.index[ok], "O2r_resid"] = g.loc[ok, "O2r_m50"] - X @ b
    df.to_csv(C.TAB / "o5_concept_panel.csv", index=False)
    ev.to_csv(C.RES / "o5_events_frame.csv", index=False)
    out: dict = {"n_frame": len(fr), "n_joined": int(df.n_events.notna().sum())}
    variants = ["O5_main", "O5_wiki", "O5_tax", "O5_anyrel", "O5_main_noRF"]
    groups = ["DEV_CS", "DEV_Eng", "DEV_BGM", "DEV_Med"] + HELD + ["COHORT"]
    srcs = sorted(ev.source.unique())
    # ---------------- coverage and base rate
    cov_rows = []
    for gk in groups + ["ALL"]:
        g = df if gk == "ALL" else df[df.gkey == gk]
        n = len(g)
        row = {"group": gk, "n": n, "share_joined": float(g.n_events.notna().mean()), "share_any_usable_event": float(g.any_usable_event.mean())}
        for v in variants:
            k = int(g[v].sum())
            row[f"{v}_rate"] = k / n
            row[f"{v}_wilson95"] = C.wilson(k, n)
        cov_rows.append(row)
    cov = pd.DataFrame(cov_rows)
    cov.to_csv(C.TAB / "o5_coverage_by_group.csv", index=False)
    srows = []
    evq = ev.merge(df[["id", "gkey"]], on="id")
    for gk in groups + ["ALL"]:
        g = df if gk == "ALL" else df[df.gkey == gk]
        eg = evq if gk == "ALL" else evq[evq.gkey == gk]
        for s in srcs + ["jel"]:
            chk = g.get(f"chk_{s}")
            es = eg[eg.source == s]
            inwin = es[es.qual_any_window & (es.year > es.t0) & (es.year <= es.t0 + WINDOW)]
            srows.append({"group": gk, "source": s, "n": len(g),
                          "share_found": float((chk.astype(str).str.startswith("found")).mean()) if chk is not None else math.nan,
                          "share_not_applicable": float((chk == "not_applicable").mean()) if chk is not None else math.nan,
                          "share_with_usable_event": float(es[es.year_usable == True].id.nunique() / len(g)) if len(g) else math.nan,  # noqa: E712
                          "share_qualifying_in_window": float(inwin.id.nunique() / len(g)) if len(g) else math.nan,
                          "match_method_mix": es.match_method.value_counts(normalize=True).round(3).to_dict(),
                          "relation_mix": es.relation.value_counts(normalize=True).round(3).to_dict()})
    pd.DataFrame(srows).to_csv(C.TAB / "o5_coverage_by_group_source.csv", index=False)
    out["coverage_by_group"] = cov_rows
    # ---------------- precedence / leakage flags
    prec = {}
    tt = df.set_index("id").t0
    nb = df.set_index("id").newborn.astype(bool)
    for s in srcs:
        es = ev[(ev.source == s) & (ev.year_usable == True) & (ev.relation == "same") & ev.year.notna()]  # noqa: E712
        if s == "mesh":
            es = es[es.event_type == "mesh_descriptor_introduced"]
        if s in TAXO:
            es = es[es.event_type == "taxonomy_added_between"]
        if len(es) == 0:
            prec[s] = {"n_matched": 0}
            continue
        first = es.groupby("id").year.min()
        precedes = first <= tt.loc[first.index]
        ct = pd.crosstab(precedes.rename("precedes"), nb.loc[first.index].rename("newborn"))
        prec[s] = {"n_matched": int(len(first)), "share_first_event_le_t0": float(precedes.mean()),
                   "flag_gt_30pct": bool(precedes.mean() > 0.30),
                   "crosstab_precedes_x_newborn": {f"precedes={a}_newborn={b}": int(ct.loc[a, b]) if a in ct.index and b in ct.columns else 0
                                                   for a in (False, True) for b in (False, True)},
                   "share_after_window": float((first > tt.loc[first.index] + WINDOW).mean())}
    wd = ev[(ev.source == "wikidata") & ev.year.notna()]
    prec["wikidata_old_inception"] = {"share_year_lt_t0_minus_10": float((wd.year < wd.t0 - 10).mean()) if len(wd) else math.nan,
                                      "n_events": int(len(wd))}
    wp = ev[(ev.source == "wikipedia_en") & ev.year.notna()]
    prec["wikipedia_growth_wave"] = {"share_dates_2001_2007": float(wp.year.between(2001, 2007).mean()),
                                     "share_t0_2001_2007": float(df.t0.between(2001, 2007).mean()),
                                     "share_estimated": float((wp.event_type == "wikipedia_page_created_estimated").mean()),
                                     "share_exact": float((wp.event_type == "wikipedia_article_created").mean()),
                                     "share_year_usable": float(wp.year_usable.mean())}
    prec["excluded_sources"] = {"jel": {"n_concepts_found": int((df.get("chk_jel") == "found").sum()), "reason": "present-day membership only; no dated events"},
                                "mesh_supplementary_record": {"n_events": int((ev.event_type == "mesh_supplementary_record_introduced").sum())},
                                "taxonomy_in_version": {"n_events": int((ev.event_type == "taxonomy_in_version").sum()), "reason": "membership in a version, not an addition date"},
                                "mesh_baseline_or_le_1966": {"n_events": int(((ev.source == "mesh") & ((ev.mesh_baseline == True) | (ev.year <= 1966))).sum())}}  # noqa: E712
    cl = ev[ev.source.isin(CURATED)]
    prec["curated_embed_llm_broader"] = {"n_events": int(((cl.match_method == "embed+llm") & (cl.relation == "broader")).sum()),
                                         "n_curated_events": int(len(cl)), "by_source": cl[(cl.match_method == "embed+llm") & (cl.relation == "broader")].source.value_counts().to_dict()}
    out["precedence_leakage"] = prec
    # ---------------- lag and Kaplan-Meier
    lag = {}
    for s in srcs:
        es = ev[(ev.source == s) & ev.qual_any_window & ev.year.notna()]
        es = es[es.year > es.t0]
        if len(es) == 0:
            continue
        first = es.groupby("id").year.min() - tt.loc[es.id.unique()].groupby(level=0).first()
        lag[s] = {"n": int(len(first)), "median": float(first.median()), "iqr": [float(first.quantile(.25)), float(first.quantile(.75))],
                  "share_after_t0_plus_8": float((first > WINDOW).mean())}
    d_ = df[["id", "t0", "first_qual_year_any", "first_qual_year_after_t0"]].copy()
    pre = d_.first_qual_year_any <= d_.t0
    k_ = d_[~pre].copy()
    k_["event"] = k_.first_qual_year_after_t0.notna().astype(int)
    k_["time"] = np.where(k_.event == 1, k_.first_qual_year_after_t0 - k_.t0, 2025 - k_.t0)
    kmc = km(k_.time, k_.event)
    lag["_all_main_sources"] = {"n_at_risk": int(len(k_)), "n_excluded_recognised_at_or_before_t0": int(pre.sum()),
                                "n_eventual_recognitions": int(k_.event.sum()),
                                "share_eventual_after_t0_plus_8": float((k_[k_.event == 1].time > WINDOW).mean()),
                                "km_cumulative_incidence": kmc, "censoring": "2025 (Wikipedia/lists); MeSH 2026 cut treated as 2025 in the combined curve"}
    for s, cens in (("wikipedia_en", 2025), ("mesh", 2026)):
        es = ev[(ev.source == s) & ev.qual_any_window & ev.year.notna()]
        fq = es.groupby("id").year.min()
        dd = df[["id", "t0"]].set_index("id").join(fq.rename("fy"))
        dd = dd[~(dd.fy <= dd.t0)]
        e_ = dd.fy.notna().astype(int)
        tm = np.where(e_ == 1, dd.fy - dd.t0, cens - dd.t0)
        lag[f"_km_{s}"] = {"censor_year": cens, "curve": km(tm, e_)[:15], "n": int(len(dd))}
    out["lag"] = lag
    pd.DataFrame(kmc).to_csv(C.TAB / "o5_km_cumulative_incidence.csv", index=False)
    # ---------------- associations
    tasks = []
    Zc = DEFINITIONS["B5_for_partial"]
    seed = C.SEED
    for v in variants:
        for gk in groups + ["HELDOUT_POOLED_CONCEPTS", "DEV_ALL", "ALL"]:
            if gk == "HELDOUT_POOLED_CONCEPTS":
                g = df[df.gkey.isin(HELD)]
            elif gk == "DEV_ALL":
                g = df[df.split == "DEV"]
            elif gk == "ALL":
                g = df
            else:
                g = df[df.gkey == gk]
            o5 = g[v].to_numpy(float)
            if o5.std() == 0:
                continue
            Y = {k: g[k].to_numpy(float) for k in OUTS}
            seed += 1
            tasks.append((gk, v, o5, Y, g[Zc].to_numpy(float), B, seed))
    logger.info(f"{len(tasks)} association tasks, B={B}")
    t = time.time()
    with ProcessPoolExecutor(min(workers, len(tasks)), mp_context=mp.get_context("spawn")) as ex:
        ares = list(ex.map(assoc_task, tasks))
    logger.info(f"associations done in {time.time()-t:.0f}s")
    at = pd.DataFrame(ares)
    at.to_csv(C.TAB / "o5_associations.csv", index=False)
    pooled = {}
    for v in variants:
        pv = {}
        sub = at[(at.variant == v) & at.group.isin(HELD)]
        for k in ["rho_" + o for o in OUTS] + ["auc_O2r_m50", "auc_O2r_resid"] + [f"prho_{o}_B5" for o in ("O1", "O2r_m50", "O2r_resid", "O3")]:
            dl = C.dersimonian_laird(sub[k].to_numpy(float), sub[f"{k}_se"].to_numpy(float)) if len(sub) else {"k": 0}
            dl["per_group"] = dict(zip(sub.group, sub[k].round(4)))
            pv[k] = dl
        hp = {o: pv[f"rho_{o}"].get("p", math.nan) for o in ("O1", "O2r_m50", "O2r_resid", "O3")}
        pv["holm_pooled_rho_family"] = C.holm(hp)
        r = {o: pv[f"rho_{o}"] for o in ("O1", "O2r_m50", "O2r_resid", "O3", "log_N_outcome")}
        dup = any(abs(r[o].get("pooled", 0)) >= 0.8 for o in ("O1", "O2r_m50", "O2r_resid", "O3"))
        rel_ = any(r[o].get("ci95", [0, 0])[0] > 0 and abs(r[o]["pooled"]) < 0.8 for o in ("O2r_m50", "O1"))
        unrel = all(r[o].get("ci95", [-1, 1])[0] <= 0 <= r[o].get("ci95", [-1, 1])[1] for o in ("O1", "O2r_m50", "O2r_resid"))
        pv["reading"] = "DUPLICATE" if dup else ("RELATED_NOT_DUPLICATE" if rel_ else ("UNRELATED" if unrel else "MIXED (some CI excludes 0, but not with O1/O2r_m50 in the positive direction)"))
        pooled[v] = pv
    out["associations_pooled_heldout_DL"] = pooled
    out["associations_file"] = "record_tables/o5_associations.csv"
    out["base_rate_heldout"] = float(df[df.gkey.isin(HELD)].O5_main.mean())
    C.dump(out, C.RES / "o5_validation_core.json")
    C.save_manifest("wp4")
    logger.info(f"base rate held-out {out['base_rate_heldout']:.3f}; readings { {v: pooled[v]['reading'] for v in variants} }")
    for v in variants:
        logger.info(f"{v}: rho O2r_m50 {pooled[v]['rho_O2r_m50'].get('pooled')}, O1 {pooled[v]['rho_O1'].get('pooled')}, logN {pooled[v]['rho_log_N_outcome'].get('pooled')}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else C.B_MAIN)
