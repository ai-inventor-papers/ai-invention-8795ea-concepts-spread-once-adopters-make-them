#!/usr/bin/env python3
"""STEP 8: assemble dated recognition events per concept, explicit absence, provisional fold, QC and reports.

Outputs (work/): concept_rows.parquet, entry_rows.parquet, verif_rows.parquet, wp_calibration.json
         (out/):  coverage_report.json, spotcheck_p78.csv, hand_check_sample.csv, qc_checks.json
RAW EVENTS ONLY: no O5 flags, no lags relative to t0.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from loguru import logger

from common import CACHE, OUT, ROOT, WORK, norm_label, setup_logging

ACCEPT = {"same", "narrower_entry", "broader_entry"}
REL = {"same": "same", "narrower_entry": "narrower", "broader_entry": "broader"}
DEV = {"CS": [17], "Eng": [22], "BGM": [13], "Med": [27]}
HELD = {"Physical": [15, 16, 19, 21, 25, 31], "LifeEnv": [11, 23, 24, 28, 30], "Social": [12, 14, 20, 32, 33],
        "MathDec": [26, 18]}
HEALTH_OTHER = [29, 34, 35, 36]
FIELD2GROUP = {f: g for d in (DEV, HELD) for g, fs in d.items() for f in fs} | {f: "unassigned_health" for f in HEALTH_OTHER}
L0_GROUP = {"Computer science": "CS", "Medicine": "Med", "Engineering": "Eng", "Mathematics": "MathDec",
            "Physics": "Physical", "Chemistry": "Physical", "Materials science": "Physical", "Geology": "Physical",
            "Economics": "Social", "Business": "Social", "Sociology": "Social", "Political science": "Social",
            "Psychology": "Social", "Philosophy": "Social", "History": "Social", "Art": "Social",
            "Environmental science": "LifeEnv", "Biology": None, "Geography": None}
SCOPE = {  # source -> level-0 disciplines in the source's domain scope ('all' = general)
    "mesh": {"Medicine", "Biology", "Chemistry", "Psychology"},
    "acm_ccs": {"Computer science"}, "msc": {"Mathematics"}, "pacs_physh": {"Physics", "Materials science"},
    "jel": {"Economics", "Business"},
    "nature_methods_moty": {"Biology", "Medicine", "Chemistry"}, "physics_world_boty": {"Physics", "Materials science"},
    "science_boty": "all", "mit_tr10": "all", "gartner_hype_cycle": "all", "research_fronts": "all", "wikipedia_en": "all", "wikidata": "all"}
LIST_EVENT = {"nature_methods_moty": "nature_methods_method_of_the_year", "science_boty": "science_breakthrough_of_the_year",
              "physics_world_boty": "physics_world_breakthrough_of_the_year", "mit_tr10": "mit_tr10_breakthrough_technology",
              "gartner_hype_cycle": "gartner_hype_cycle_emerging_tech_entry", "research_fronts": "research_front_listed"}
ORDER = {"acm_ccs": [1998, 2012], "msc": [2000, 2010, 2020], "pacs_physh": [2010, 2016]}


def wd_time(v: dict | None) -> tuple[int | None, str | None, int | None]:
    if not isinstance(v, dict) or not v.get("time"):
        return None, None, None
    t, p = v["time"], v.get("precision")
    m = re.match(r"([+-])(\d+)-(\d\d)-(\d\d)", t)
    if not m:
        return None, None, p
    y = int(m.group(2)) * (-1 if m.group(1) == "-" else 1)
    date = f"{y:04d}-{m.group(3)}-{m.group(4)}" if p == 11 else (f"{y:04d}-{m.group(3)}" if p == 10 else f"{y:04d}")
    return y, date, p


def ev(source, event_type, year, *, date=None, precision=None, usable=None, detail=None, method, conf, relation="same",
       entry_id=None) -> dict:
    return {"source": source, "event_type": event_type, "year": int(year) if year is not None and not pd.isna(year) else None,
            "date": date, "date_precision": precision,
            "year_usable": bool(usable) if usable is not None else (year is not None and not pd.isna(year)),
            "match_method": method, "match_confidence": round(float(conf), 3) if conf is not None else None,
            "relation": relation, "entry_id": entry_id, "detail": detail or {}}


def _fit_median(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    o = np.argsort(x)
    x, y = x[o], y[o]
    nb = max(10, min(300, len(x) // 12))
    edges = np.unique(np.quantile(x, np.linspace(0, 1, nb + 1)))
    bx, by = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (x >= a) & (x <= b)
        if m.sum() >= 3:
            bx.append(np.median(x[m]))
            by.append(np.median(y[m]))
    return np.array(bx), np.maximum.accumulate(np.array(by))


def wikipedia_table(k: pd.DataFrame) -> tuple[dict, dict]:
    """title -> creation record; exact first revisions where fetched, median-bin page-id estimate otherwise."""
    from sklearn.model_selection import KFold
    fr = {}
    p = CACHE / "wikipedia" / "first_rev.jsonl"
    if p.exists():
        for line in p.open():
            r = json.loads(line)
            fr[r["title_req"]] = r
    pid = {}
    p2 = CACHE / "wikipedia" / "pageids.jsonl"
    if p2.exists():
        for line in p2.open():
            r = json.loads(line)
            pid[r["title_req"]] = r
    # calibration set: exact first revision + page id of the same (non-redirected) page
    xs, ys = [], []
    for t, r in fr.items():
        q = pid.get(t)
        if r.get("first_rev_ts") and q and q.get("pageid") and r.get("pageid") == q.get("pageid"):
            xs.append(q["pageid"])
            ys.append(datetime.fromisoformat(r["first_rev_ts"].replace("Z", "+00:00")).timestamp())
    xs, ys = np.array(xs, float), np.array(ys, float)
    cal = {"n_calibration": int(len(xs)),
           "method": "page ids binned by quantile (~12 pages/bin); per-bin median page id and median first-revision time; "
                     "monotone upper envelope (cumulative max); linear interpolation. Robust to pages whose imported/merged "
                     "history makes the first revision much older than the page id (an L2 isotonic fit was dragged down by these)."}
    fit = None
    if len(xs) >= 200:
        yr = lambda v: datetime.fromtimestamp(float(v), timezone.utc).year
        same, ae, by = [], [], defaultdict(list)
        for tr, te in KFold(5, shuffle=True, random_state=0).split(xs):
            bx, byy = _fit_median(xs[tr], ys[tr])
            pr = np.interp(xs[te], bx, byy)
            for a_, b_ in zip(pr, ys[te]):
                same.append(yr(a_) == yr(b_))
                ae.append(abs(a_ - b_) / (365.25 * 86400))
                by[yr(a_)].append(yr(a_) == yr(b_))
        cal.update({"cv_share_same_calendar_year": float(np.mean(same)), "cv_median_abs_err_years": float(np.median(ae)),
                    "cv_mae_years": float(np.mean(ae)), "cv_p90_abs_err_years": float(np.quantile(ae, 0.9)),
                    "cv_share_within_1y": float(np.mean(np.array(ae) <= 1)),
                    "cv_same_year_by_estimated_year": {int(y): {"n": len(v), "share_same_year": float(np.mean(v))}
                                                       for y, v in sorted(by.items())},
                    "usable_estimated_years": sorted(int(y) for y, v in by.items() if len(v) >= 30 and np.mean(v) >= 0.9)})
        fit = _fit_median(xs, ys)
    out = {}
    for t in set(k.enwiki_title.dropna()) | set(fr) | set(pid):
        r = fr.get(t)
        if r and not r.get("error"):
            out[t] = {"method": "first_revision", **{kk: r.get(kk) for kk in ("norm_title", "pageid", "first_rev_ts",
                      "first_rev_size", "first_is_redirect", "first_article_ts", "followed_redirect", "missing")}}
        elif pid.get(t) and pid[t].get("pageid") and fit is not None:
            q = pid[t]
            ts = datetime.fromtimestamp(float(np.interp(q["pageid"], fit[0], fit[1])), timezone.utc)
            out[t] = {"method": "pageid_median_bin_estimate", "pageid": q["pageid"], "title_final": q["title_final"],
                      "followed_redirect": q["redirected"], "est_first_rev_ts": ts.strftime("%Y-%m-%dT%H:%M:%SZ")}
        elif pid.get(t) and pid[t].get("missing"):
            out[t] = {"method": "missing_page"}
    return out, cal


@logger.catch(reraise=True)
def main() -> None:
    setup_logging("s8_assemble")
    k = pd.read_parquet(WORK / "concept_keys.parquet")
    e = pd.read_parquet(WORK / "entries.parquet").set_index("entry_id", drop=False)
    c = pd.read_parquet(WORK / "candidates.parquet")
    v = pd.read_parquet(WORK / "verifications.parquet")
    mesh = pd.read_parquet(WORK / "mesh_desc.parquet").set_index("mesh_ui")
    supp = pd.read_parquet(WORK / "mesh_supp.parquet").set_index("mesh_ui")
    xw = pd.read_csv(OUT / "crosswalk_level1_to_field.csv").set_index("openalex_id")
    lst = pd.read_parquet(WORK / "list_entries.parquet").set_index("entry_id")
    tax = pd.read_parquet(WORK / "tax_entries.parquet")

    # ------------------------------------------------------------------ accepted links
    c["auto"] = c.methods.map(lambda m: any(x in ("wikidata_property", "exact_norm_label", "exact_norm_alias") for x in m))
    c["family"] = c.entry_id.map(e.family)
    vv = v[v.task.isin(["verify", "audit"])].drop_duplicates(["entry_id", "openalex_id", "task"])
    ver = vv[vv.task == "verify"].set_index(["entry_id", "openalex_id"])
    aud = vv[vv.task == "audit"].set_index(["entry_id", "openalex_id"])
    ver2 = v[v.task == "verify_lists_v2"].drop_duplicates(["entry_id", "openalex_id"]).set_index(["entry_id", "openalex_id"])
    val = v[v.task == "verify_alias"].drop_duplicates(["entry_id", "openalex_id"]).set_index(["entry_id", "openalex_id"])
    links = []
    n_drop_audit = 0
    for r in c.itertuples(index=False):
        key = (r.entry_id, r.openalex_id)
        m = list(r.methods)
        if r.family == "lists":
            src_v = ver2 if key in ver2.index else (ver if key in ver.index else None)   # v2 (stronger model) first
            if src_v is not None:
                x = src_v.loc[key]
                if x.relation in ACCEPT:
                    meth = "wikilink+llm" if "wikilink" in m else ("embed+llm" if set(m) <= {"embed", "embed065"} else
                            ("exact_norm_label+llm" if "exact_norm_label" in m else ("exact_norm_alias+llm" if "exact_norm_alias" in m else "fuzzy+llm")))
                    conf = float(x.confidence) if x.confidence is not None and not pd.isna(x.confidence) else 0.7
                    links.append((r.entry_id, r.openalex_id, meth, conf, REL[x.relation], "llm_verified"))
                elif x.status and str(x.status).startswith("not_verified"):
                    links.append((r.entry_id, r.openalex_id, "unverified", 0.5, "same", "unverified_budget"))
            continue
        if r.auto:
            meth = "wikidata_property" if "wikidata_property" in m else ("exact_norm_label" if "exact_norm_label" in m else "exact_norm_alias")
            conf = r.score if meth != "wikidata_property" else 1.0
            status = "accepted_without_llm"
            needs_llm = meth == "exact_norm_alias" or (r.family == "mesh" and meth == "exact_norm_label")
            if needs_llm:   # alias-only (audit precision 0.31) and MeSH label-only links require an LLM accept
                if key not in val.index:
                    continue
                x = val.loc[key]
                if x.relation not in ACCEPT:
                    if x.status and str(x.status).startswith("not_verified"):
                        links.append((r.entry_id, r.openalex_id, meth + "_unverified", 0.5, "same", "unverified_budget"))
                    continue
                llm_c = float(x.confidence) if x.confidence is not None and not pd.isna(x.confidence) else 0.7
                links.append((r.entry_id, r.openalex_id, meth + "+llm", round(min(conf, llm_c), 3), REL[x.relation],
                              "llm_verified"))
                continue
            relation = "same"
            if meth == "wikidata_property" and r.family == "msc" and re.search(r"(-XX|xx|-\d\d)$", str(e.at[r.entry_id, "code"])):
                relation = "broader"      # P3285 pointing at an MSC section / 2nd-level class: entry broader than concept
            if key in aud.index:
                a = aud.loc[key]
                if a.relation in ("different", "related") and meth != "wikidata_property":
                    n_drop_audit += 1
                    continue
                if a.relation in ("narrower_entry", "broader_entry"):
                    relation = REL[a.relation]
                status = f"audited:{a.relation}"
            links.append((r.entry_id, r.openalex_id, meth, conf, relation, status))
        else:
            if key in ver.index:
                x = ver.loc[key]
                if x.relation in ACCEPT:
                    conf = float(x.confidence) if x.confidence is not None and not pd.isna(x.confidence) else 0.7
                    links.append((r.entry_id, r.openalex_id, "fuzzy+llm", 0.9 * conf, REL[x.relation], "llm_verified"))
                elif x.status and str(x.status).startswith("not_verified"):
                    links.append((r.entry_id, r.openalex_id, "fuzzy_unverified", 0.5, "same", "unverified_budget"))
    L = pd.DataFrame(links, columns=["entry_id", "openalex_id", "match_method", "match_confidence", "relation", "link_status"])
    L["family"] = L.entry_id.map(e.family)
    L["source"] = L.entry_id.map(e.source)
    logger.info(f"accepted links {len(L)} by family {L.family.value_counts().to_dict()}; dropped by audit {n_drop_audit}")
    L.to_parquet(WORK / "links.parquet", index=False)

    # ------------------------------------------------------------------ taxonomy label sets per version
    vlabels = defaultdict(set)
    for s, ver_, ln, al in zip(tax.source, tax.version, tax.label_norm, tax.alt_labels):
        if pd.notna(ver_):
            vlabels[(s, int(ver_))].add(ln)
            for a in (al if al is not None else []):
                vlabels[(s, int(ver_))].add(norm_label(a))
    acm98_new = {f"acm_ccs:1998:{cd}": json.loads(fl).get("new_in_1998", False)
                 for cd, fl, s, ver_ in zip(tax.code, tax["flags"], tax.source, tax.version) if s == "acm_ccs" and ver_ == 1998}

    # ------------------------------------------------------------------ wikipedia
    wp, cal = wikipedia_table(k)
    (WORK / "wp_calibration.json").write_text(json.dumps(cal, indent=1))
    logger.info(f"wikipedia records {len(wp)}; methods {Counter(x['method'] for x in wp.values())}; calibration {cal}")
    usable_years = set(cal.get("usable_estimated_years", []))   # estimated years whose CV same-year share >= 0.9

    # ------------------------------------------------------------------ per-concept assembly
    Lg = {oid: g for oid, g in L.groupby("openalex_id")}
    l1 = xw.field_id.to_dict()
    rows = []
    for r in k.itertuples(index=False):
        events = []
        l0 = sorted({a["display_name"] for a in r.ancestors if a["level"] == 0})
        if r.level == 0:
            l0 = [r.label]
        # Wikidata inception / discovery
        for prop, et in (("p571", "wikidata_inception"), ("p575", "wikidata_discovery_or_invention")):
            for x in json.loads(getattr(r, prop)):
                y, date, p = wd_time(x.get("v"))
                if y is None:
                    continue
                events.append(ev("wikidata", et, y, date=date, precision=p, usable=(p or 0) >= 9,
                                 detail={"property": prop.upper(), "rank": x.get("rank"), "n_refs": x.get("n_refs"),
                                         "qualifiers": x.get("q"), "discoverer_or_inventor_qids": list(r.p61)[:10] if prop == "p575" else None,
                                         "calendar": (x.get("v") or {}).get("calendar")},
                                 method="wikidata_property", conf=1.0))
        # Wikipedia creation
        wstat = "not_found"
        t = r.enwiki_title
        wmeth = "wikidata_sitelink"
        if not t and isinstance(r.wikipedia_url, str) and "/wiki/" in r.wikipedia_url:
            from urllib.parse import unquote
            t = unquote(r.wikipedia_url.split("/wiki/", 1)[1]).replace("_", " ")
            wmeth = "openalex_wikipedia_url"
        w = wp.get(t) if t else None
        if t and w is None:
            wstat = "not_checked"
        elif w and w["method"] == "first_revision" and not w.get("missing") and w.get("first_rev_ts"):
            ts = w.get("first_article_ts") or w["first_rev_ts"]
            repair_failed = bool(w.get("first_is_redirect")) and not w.get("first_article_ts")
            events.append(ev("wikipedia_en", "wikipedia_article_created", int(ts[:4]), date=ts[:10], precision=11,
                             usable=not repair_failed, detail={"title": w.get("norm_title") or t, "pageid": w.get("pageid"),
                                                  "first_rev_ts": w["first_rev_ts"], "first_rev_size": w.get("first_rev_size"),
                                                  "first_is_redirect": w.get("first_is_redirect"),
                                                  "first_article_ts": w.get("first_article_ts"),
                                                  "title_followed_redirect": w.get("followed_redirect"),
                                                  "date_method": "first_revision" + ("+redirect_repair" if w.get("first_is_redirect") else "")
                                                  + ("_failed(no revision >=500 bytes in first 50)" if repair_failed else "")},
                             method=wmeth, conf=1.0))
            wstat = "found"
        elif w and w["method"] == "pageid_median_bin_estimate":
            ts = w["est_first_rev_ts"]
            events.append(ev("wikipedia_en", "wikipedia_page_created_estimated", int(ts[:4]), date=ts[:10],
                             precision="estimated", usable=int(ts[:4]) in usable_years,
                             detail={"title": w.get("title_final") or t, "pageid": w["pageid"],
                                     "date_method": "pageid_median_bin_estimate (page creation; no redirect repair)",
                                     "title_followed_redirect": w.get("followed_redirect")},
                             method=wmeth, conf=0.8))
            wstat = "found_estimated"
        elif w and (w.get("missing") or w["method"] == "missing_page"):
            wstat = "not_found"
        elif not t:
            wstat = "not_found"
        # links from external entries
        found = defaultdict(bool)
        g = Lg.get(r.openalex_id)
        present_jel = []
        if g is not None:
            tax_hits = defaultdict(dict)   # source -> version -> (entry, row)
            for x in g.itertuples(index=False):
                en = e.loc[x.entry_id]
                if x.family == "mesh":
                    if en.source == "mesh_scr":
                        s = supp.loc[en.code]
                        events.append(ev("mesh", "mesh_supplementary_record_introduced", s.date_introduced_year,
                                         precision=9, detail={"ui": en.code, "name": en.label, "scr_class": s.scr_class,
                                                              "heading_mapped_to": list(s.heading_mapped_to)[:5]},
                                         method=x.match_method, conf=x.match_confidence, relation=x.relation, entry_id=x.entry_id))
                    else:
                        m = mesh.loc[en.code]
                        events.append(ev("mesh", "mesh_descriptor_introduced", m.mesh_year_best,
                                         date=m.date_introduced, precision=9,
                                         detail={"ui": en.code, "name": en.label, "date_introduced": m.date_introduced,
                                                 "history_note": m.history_note, "history_year": m.history_year,
                                                 "history_year_earlier": m.history_year_earlier,
                                                 "year_rule": m.mesh_year_rule, "mesh_baseline": bool(m.mesh_baseline),
                                                 "tree_numbers": list(m.tree_numbers)[:12], "top_branches": list(m.top_branches),
                                                 "previous_indexing": list(m.previous_indexing)[:6], "link_status": x.link_status},
                                         method=x.match_method, conf=x.match_confidence, relation=x.relation, entry_id=x.entry_id))
                    found["mesh"] = True
                elif x.family in ORDER:
                    vv_ = int(en.version)
                    prev = tax_hits[x.family].get(vv_)
                    if prev is None or x.match_confidence > prev[1].match_confidence:
                        tax_hits[x.family][vv_] = (en, x)
                    found[x.family] = True
                elif x.family == "jel":
                    present_jel.append({"code": en.code, "label": en.label, "match_method": x.match_method,
                                        "relation": x.relation, "year_known": False})
                    found["jel"] = True
                elif x.family == "lists":
                    li = lst.loc[x.entry_id]
                    events.append(ev(en.source, LIST_EVENT[en.source], li.year, precision=9,
                                     detail={"item_text": li.item_text, "role": li.role,
                                             "rank": int(li["rank"]) if pd.notna(li["rank"]) else None,
                                             "phase": li.phase, "descriptor": (li.descriptor or "")[:200] if isinstance(li.descriptor, str) else None,
                                             "url": li.url, "primary_ref": li.primary_ref, "link_status": x.link_status},
                                     method=x.match_method, conf=x.match_confidence, relation=x.relation, entry_id=x.entry_id))
                    found[en.source] = True
            for fam_, byv in tax_hits.items():
                vers = ORDER[fam_]
                for vv_, (en, x) in sorted(byv.items()):
                    events.append(ev(fam_, "taxonomy_in_version", vv_, precision=9,
                                     detail={"version": vv_, "code": en.code, "node_label": en.label},
                                     method=x.match_method, conf=x.match_confidence, relation=x.relation, entry_id=en.entry_id))
                    i = vers.index(vv_) if vv_ in vers else -1
                    if i > 0:
                        older = vers[i - 1]
                        if older not in byv and en.label_norm not in vlabels[(fam_, older)]:
                            events.append(ev(fam_, "taxonomy_added_between", vv_, precision=9,
                                             detail={"older_version": older, "newer_version": vv_, "code": en.code,
                                                     "node_label": en.label, "rule": "matched node label absent from older version and concept unmatched in older version",
                                                     "scheme_redesign": fam_ in ("pacs_physh", "acm_ccs"),
                                                     "caution": ("PACS 2010 -> PhySH 2016 is a replacement scheme with a different labelling style; "
                                                                 "absence from PACS is weak evidence of novelty" if fam_ == "pacs_physh" else
                                                                 ("ACM CCS 2012 was a full redesign of CCS 1998; absence from 1998 is weaker evidence "
                                                                  "than an MSC revision" if fam_ == "acm_ccs" else None))},
                                             method=x.match_method, conf=x.match_confidence, relation=x.relation, entry_id=en.entry_id))
                    if fam_ == "acm_ccs" and vv_ == 1998 and acm98_new.get(en.entry_id):
                        events.append(ev(fam_, "taxonomy_added_between", 1998, precision=9,
                                         detail={"older_version": 1991, "newer_version": 1998, "code": en.code,
                                                 "node_label": en.label, "rule": "marked NEW! in the ACM CCS 1998 text (relative to CCS 1991)"},
                                         method=x.match_method, conf=x.match_confidence, relation=x.relation, entry_id=en.entry_id))
        events.sort(key=lambda d: (d["year"] if d["year"] is not None else 9999, d["source"], d["event_type"]))
        # explicit absence
        checked = {}
        for s in ("wikidata", "wikipedia_en", "mesh", "acm_ccs", "msc", "pacs_physh", "jel", "nature_methods_moty",
                  "science_boty", "physics_world_boty", "mit_tr10", "gartner_hype_cycle", "research_fronts"):
            if s == "wikipedia_en":
                checked[s] = wstat
                continue
            if s == "wikidata":
                checked[s] = ("found" if any(x["source"] == "wikidata" for x in events) else
                              ("not_found" if not r.wikidata_missing else "not_checked"))
                continue
            sc = SCOPE[s]
            if found.get(s):
                checked[s] = "found"
            elif sc == "all" or (set(l0) & sc):
                checked[s] = "not_found"
            else:
                checked[s] = "not_applicable"
        # provisional fold
        l1_anc = [a["id"] for a in r.ancestors if a["level"] == 1]
        if r.level == 1:
            l1_anc = [r.openalex_id]
        fields = [l1.get(a) for a in l1_anc if a in l1]
        fields = [int(f) if str(f).isdigit() else f for f in fields]
        groups = [FIELD2GROUP.get(f) for f in fields if f != "multi"]
        groups = [gg for gg in groups if gg]
        grp = None
        g_plural, g_share = None, None
        if groups:
            cnt = Counter(groups)
            top, n = cnt.most_common(1)[0]
            g_plural, g_share = top, round(n / len(groups), 3)
            grp = top if (len(cnt) == 1 or n / len(groups) >= 2 / 3) else "unassigned_multi"
        else:
            gl = {L0_GROUP.get(x) for x in l0}
            gl.discard(None)
            grp = gl.pop() if len(gl) == 1 and all(L0_GROUP.get(x) for x in l0) else "unassigned"
        fold = "dev" if grp in DEV else ("heldout" if grp in HELD else "unassigned")
        present = {"year_known": False, "n_wiki_sitelinks": r.n_wiki_sitelinks,
                   "openalex_works_count": r.present_day_works_count, "openalex_cited_by_count": r.present_day_cited_by_count,
                   "wikidata_n_claims": r.n_claims_total, "wikidata_instance_of": list(r.p31)[:10],
                   "wikidata_subclass_of": list(r.p279)[:10], "wikidata_part_of": list(r.p361)[:10],
                   "mesh_tree_codes_wikidata": list(r.p672)[:10], "jel": present_jel,
                   "wikidata_mag_id_matches_openalex": r.p6366_agrees}
        rows.append({
            "openalex_id": r.openalex_id, "level": int(r.level),
            "input": {"openalex_id": r.openalex_id, "qid": r.qid, "qid_resolved": r.qid_resolved, "label": r.label,
                      "label_norm": r.label_norm, "aliases": list(r.aliases), "aliases_norm": list(r.aliases_norm),
                      "acronyms": list(r.acronyms), "level": int(r.level), "ancestor_ids": list(r.ancestor_ids),
                      "level0_disciplines": l0, "enwiki_title": t,
                      "frame_role": "ancestor_only" if r.level < 2 else "target"},
            "output": {"events": events, "sources_checked": checked, "present_day": present},
            "fold": fold, "group": grp, "group_plurality": g_plural, "group_plurality_share": g_share, "l1_fields": fields, "l0": l0, "n_events": len(events),
            "n_events_year_usable": sum(1 for x in events if x["year_usable"]),
        })
    R = pd.DataFrame(rows)
    logger.info(f"concept rows {len(R)}; fold {R.fold.value_counts().to_dict()}; group {R.group.value_counts().to_dict()}")
    R.to_pickle(WORK / "concept_rows.pkl")

    # ------------------------------------------------------------------ QC known answers
    by_label = defaultdict(list)
    for rr in rows:
        by_label[rr["input"]["label_norm"]].append(rr)

    def has(lbl_norms, src, year):
        for ln in {norm_label(x) for x in lbl_norms} | set(lbl_norms):
            for rr in by_label.get(ln, []):
                if any(x["source"] == src and x["year"] == year for x in rr["output"]["events"]):
                    return True, rr["openalex_id"]
        return False, None
    qc = {
        "optogenetics_nature_methods_2010": has(["optogenetics"], "nature_methods_moty", 2010),
        "ipsc_nature_methods_2009": has(["induced pluripotent stem cell"], "nature_methods_moty", 2009),
        "crispr_science_boty_2015": has([x for x in by_label if "crispr" in x], "science_boty", 2015),
        "super_resolution_nature_methods_2008": has(["super-resolution microscopy", "superresolution microscopy",
                                                     "super resolution microscopy"], "nature_methods_moty", 2008),
    }
    wp_ts = [x["date"] for rr in rows for x in rr["output"]["events"] if x["event_type"] == "wikipedia_article_created"]
    mesh_y = [x["year"] for rr in rows for x in rr["output"]["events"] if x["event_type"] == "mesh_descriptor_introduced"]
    qc["wikipedia_min_date"] = min(wp_ts) if wp_ts else None
    qc["wikipedia_all_ge_2001_01_15"] = all(d >= "2001-01-15" for d in wp_ts)
    qc["mesh_years_in_1954_2026"] = all(1954 <= y <= 2026 for y in mesh_y if y is not None)
    (OUT / "qc_checks.json").write_text(json.dumps(qc, indent=1, default=str))
    logger.info(f"QC {qc}")
    for kk in ("optogenetics_nature_methods_2010", "ipsc_nature_methods_2009", "crispr_science_boty_2015",
               "super_resolution_nature_methods_2008"):
        assert qc[kk][0], f"known-answer check failed: {kk}"
    assert qc["wikipedia_all_ge_2001_01_15"] and qc["mesh_years_in_1954_2026"]


if __name__ == "__main__":
    main()
