#!/usr/bin/env python3
"""STEP 9: coverage report, P78 spot check, hand-check sample, and the exp_sel_data_out JSON deliverables.

data_out: full_data_out/full_data_out_<n>.json (each part a valid exp_sel_data_out document, <= ~90 MB),
          mini_data_out.json (<= 200 rows per dataset, concept rows stratified by provisional group),
          preview_data_out.json (10 rows per dataset, long strings truncated).
"""
from __future__ import annotations

import ast
import json
import random
from collections import Counter, defaultdict

import pandas as pd
from loguru import logger

from common import OUT, ROOT, WORK, norm_label, setup_logging

P78 = ROOT.parents[2] / "round-1" / "." / "gen_art_experiment_4" / "outcomes.csv"
ACCEPT = {"same", "narrower_entry", "broader_entry"}
PART_BYTES = 90_000_000


def clean(x):
    """Recursively convert numpy scalars/arrays to Python and NaN/inf to None (strict JSON)."""
    import math
    if isinstance(x, dict):
        return {str(k_): clean(v_) for k_, v_ in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(y) for y in x]
    if hasattr(x, "tolist") and not isinstance(x, (str, bytes)):
        return clean(x.tolist())
    if isinstance(x, float):
        return None if (math.isnan(x) or math.isinf(x)) else x
    return x


def dumps(x) -> str:
    return json.dumps(clean(x), ensure_ascii=False, allow_nan=False, default=str)


def coverage(R: pd.DataFrame, agr: dict) -> dict:
    tgt = R[R.level >= 2]
    ex = []
    for r in tgt.itertuples(index=False):
        for s, st in r.output["sources_checked"].items():
            evs = [x for x in r.output["events"] if x["source"] == s]
            ex.append({"source": s, "status": st, "level": r.level, "l0": r.l0[0] if len(r.l0) == 1 else ("multi" if r.l0 else "none"),
                       "group": r.group, "n_ev": len(evs), "usable": any(x["year_usable"] for x in evs),
                       "years": [x["year"] for x in evs if x["year_usable"] and x["year"] is not None],
                       "methods": [x["match_method"] for x in evs]})
    X = pd.DataFrame(ex)

    def summ(d: pd.DataFrame) -> dict:
        yrs = [y for ys in d.years for y in ys]
        hist = Counter((y // 5) * 5 for y in yrs)
        return {"n_concepts": int(len(d)), "n_with_event": int((d.n_ev > 0).sum()),
                "n_with_year_usable_event": int(d.usable.sum()),
                "status": {k: int(v) for k, v in d.status.value_counts().items()},
                "event_year_hist_5y": {int(k): int(v) for k, v in sorted(hist.items())},
                "match_method_mix": dict(Counter(m for ms in d.methods for m in ms))}
    rep = {"frame": "OpenAlex legacy concepts, levels 2-5 (levels 0-1 are ancestor-only rows)",
           "n_target_concepts": int(len(tgt)),
           "by_source": {s: summ(d) for s, d in X.groupby("source")},
           "by_source_level": {f"{s}|L{l}": summ(d) for (s, l), d in X.groupby(["source", "level"])},
           "by_source_group": {f"{s}|{g}": summ(d) for (s, g), d in X.groupby(["source", "group"])},
           "by_source_level0": {f"{s}|{l}": summ(d) for (s, l), d in X.groupby(["source", "l0"])},
           "by_source_level_l0_group": {f"{s}|L{l}|{l0}|{g}": {"n": int(len(d)), "n_with_event": int((d.n_ev > 0).sum()),
                                                                "n_year_usable": int(d.usable.sum())}
                                        for (s, l, l0, g), d in X.groupby(["source", "level", "l0", "group"])},
           "llm_audit_and_agreement": agr}
    # which groups have a dated taxonomy for their OWN domain (JEL is undated, so Social has none)
    own = {"CS": ["acm_ccs"], "MathDec": ["msc"], "Physical": ["pacs_physh"], "BGM": ["mesh"], "Med": ["mesh"],
           "LifeEnv": ["mesh"], "Social": [], "Eng": [], "unassigned_health": ["mesh"]}
    dom = ["acm_ccs", "msc", "pacs_physh", "mesh", "jel"]
    gaps = {}
    for g, d in X[X.source.isin(dom)].groupby("group"):
        sh = {s_: float((z.n_ev > 0).mean()) for s_, z in d.groupby("source")}
        gaps[g] = {"own_domain_dated_taxonomies": own.get(g), "share_with_event_by_domain_source": sh,
                   "note": ("no dated domain taxonomy (JEL membership is undated); MeSH covers only its psychology/"
                            "health-economics fringe" if g == "Social" else
                            ("engineering has no dedicated dated taxonomy here; covered partly by ACM/PACS/MeSH" if g == "Eng" else None))}
    rep["dated_domain_taxonomy_by_group"] = gaps
    rep["groups_without_dated_domain_taxonomy"] = sorted(g for g, v in own.items() if not v and g in gaps)
    rep["recommendation"] = ("For cross-group O5 comparisons use a Wikipedia/Wikidata-only variant (sources wikipedia_en, "
                             "wikidata), because domain taxonomies and curated lists cover groups unevenly.")
    return rep


def spot_p78(R: pd.DataFrame) -> pd.DataFrame:
    if not P78.exists():
        logger.warning(f"P78 file missing at {P78}; join test skipped")
        return pd.DataFrame()
    p = pd.read_csv(P78)
    idx_l, idx_a = defaultdict(list), defaultdict(list)
    for r in R.itertuples(index=False):
        idx_l[r.input["label_norm"]].append(r)
        for a in r.input["aliases_norm"]:
            idx_a[a].append(r)
    out = []
    for q in p.itertuples(index=False):
        names = [q.concept] + [x.strip() for x in str(q.aliases_used).split("|") if x.strip() and x != "nan"]
        hit, how = None, None
        for n in names:
            nn = norm_label(n)
            if idx_l.get(nn):
                hit, how = sorted(idx_l[nn], key=lambda r: -r.level)[0], "label_norm"
                break
        if hit is None:
            for n in names:
                nn = norm_label(n)
                if idx_a.get(nn):
                    hit, how = sorted(idx_a[nn], key=lambda r: -r.level)[0], "alias_norm"
                    break
        evs = hit.output["events"] if hit is not None else []
        out.append({"concept": q.concept, "aliases_used": q.aliases_used, "iter1_group": q.group, "iter1_home": q.home,
                    "t0": q.t0, "iter1_status": q.status, "joined": hit is not None, "join_on": how,
                    "openalex_id": hit.openalex_id if hit is not None else None,
                    "oa_label": hit.input["label"] if hit is not None else None,
                    "level": hit.level if hit is not None else None,
                    "provisional_group": hit.group if hit is not None else None,
                    "n_events": len(evs),
                    "events": "; ".join(f"{x['year']}:{x['source']}:{x['event_type']}" + (f"({x['relation']})" if x['relation'] != 'same' else "")
                                        for x in evs),
                    "sources_checked": json.dumps(hit.output["sources_checked"]) if hit is not None else None})
    return pd.DataFrame(out)


def build_datasets(R: pd.DataFrame) -> list[dict]:
    e = pd.read_parquet(WORK / "entries.parquet").set_index("entry_id", drop=False)
    L = pd.read_parquet(WORK / "links.parquet")
    k = pd.read_parquet(WORK / "concept_keys.parquet").set_index("openalex_id")
    mesh = pd.read_parquet(WORK / "mesh_desc.parquet").set_index("mesh_ui")
    v = pd.read_parquet(WORK / "verifications.parquet")
    ds = []
    # 1 concept_recognition
    ex = []
    for r in R.itertuples(index=False):
        ex.append({"input": dumps(r.input), "output": dumps(r.output), "metadata_fold": r.fold, "metadata_group": r.group,
                   "metadata_group_plurality": r.group_plurality, "metadata_group_plurality_share": r.group_plurality_share,
                   "metadata_level": int(r.level), "metadata_l1_fields": [str(x) for x in r.l1_fields],
                   "metadata_level0": list(r.l0), "metadata_n_events": int(r.n_events),
                   "metadata_n_events_year_usable": int(r.n_events_year_usable),
                   "metadata_frame_role": r.input["frame_role"], "metadata_openalex_id": r.openalex_id,
                   "metadata_qid": r.input["qid"]})
    ds.append({"dataset": "concept_recognition", "examples": ex})
    # 2-7 external_recognition_entries, one dataset per source family
    Lg = {eid: g for eid, g in L.groupby("entry_id")}
    fam_name = {"mesh": "external_entries_mesh", "acm_ccs": "external_entries_acm_ccs", "msc": "external_entries_msc",
                "pacs_physh": "external_entries_pacs_physh", "jel": "external_entries_jel", "lists": "external_entries_curated_lists"}
    lst = pd.read_parquet(WORK / "list_entries.parquet").set_index("entry_id")
    for fam, name in fam_name.items():
        ex = []
        for r in e[e.family == fam].itertuples(index=False):
            g = Lg.get(r.entry_id)
            matched = [] if g is None else [
                {"openalex_id": x.openalex_id, "qid": k.at[x.openalex_id, "qid"], "label": k.at[x.openalex_id, "label"],
                 "relation": x.relation, "match_method": x.match_method, "match_confidence": round(float(x.match_confidence), 3),
                 "link_status": x.link_status} for x in g.itertuples(index=False)]
            as_int = lambda x: None if x is None or (isinstance(x, float) and x != x) else int(x)
            inp = {"entry_id": r.entry_id, "source": r.source, "version": as_int(r.version), "year": as_int(r.year), "code": r.code,
                   "label": r.label, "label_norm": r.label_norm, "alt_labels": list(r.alt_labels)[:20],
                   "descriptor": r.descriptor if isinstance(r.descriptor, str) else None, "generic_label": bool(r.generic)}
            if fam == "mesh" and r.source == "mesh":
                m = mesh.loc[r.code]
                inp.update({"date_introduced": m.date_introduced, "history_note": m.history_note,
                            "mesh_year_best": m.mesh_year_best, "mesh_year_rule": m.mesh_year_rule,
                            "mesh_baseline": bool(m.mesh_baseline), "tree_numbers": list(m.tree_numbers)[:12],
                            "top_branches": list(m.top_branches)})
            if fam == "lists":
                li = lst.loc[r.entry_id]
                inp.update({"role": li.role, "rank": None if pd.isna(li["rank"]) else int(li["rank"]), "phase": li.phase,
                            "wiki_links": list(li.wiki_links), "url": li.url, "primary_ref": li.primary_ref})
            ex.append({"input": dumps(inp), "output": dumps({"matched_concepts": matched, "n_matched": len(matched)}),
                       "metadata_source": r.source, "metadata_family": fam,
                       "metadata_year": None if r.year is None or pd.isna(r.year) else int(r.year),
                       "metadata_year_known": fam != "jel", "metadata_n_matched": len(matched),
                       "metadata_entry_id": r.entry_id})
        ds.append({"dataset": name, "examples": ex})
    # 8 match_verifications
    ex = []
    for r in v.itertuples(index=False):
        en = e.loc[r.entry_id] if r.entry_id in e.index else None
        ex.append({"input": dumps({"entry_id": r.entry_id, "entry_text": None if en is None else en.label,
                                   "entry_source": None if en is None else en.source,
                                   "candidate_openalex_id": r.openalex_id,
                                   "candidate_label": k.at[r.openalex_id, "label"] if r.openalex_id in k.index else None,
                                   "candidate_methods": list(r.methods)}),
                   "output": dumps({"relation": r.relation, "confidence": r.confidence, "accepted": r.relation in ACCEPT}),
                   "metadata_task": r.task, "metadata_model": r.model, "metadata_prompt_hash": r.prompt_hash,
                   "metadata_cost_usd": float(r.cost or 0.0), "metadata_status": r.status,
                   "metadata_family": None if en is None else en.family})
    ds.append({"dataset": "match_verifications", "examples": ex})
    # 9 crosswalk
    xw = pd.read_csv(OUT / "crosswalk_level1_to_field.csv")
    ds.append({"dataset": "crosswalk_level1_to_field", "examples": [
        {"input": dumps({"openalex_id": r.openalex_id, "display_name": r.display_name,
                         "level0_parents": ast.literal_eval(r.level0_parents) if isinstance(r.level0_parents, str) else []}),
         "output": dumps({"field_id": r.field_id, "field_name": r.field_name, "decided_by": r.decided_by, "reason": r.reason}),
         "metadata_model_a": str(r.model_a), "metadata_model_b": str(r.model_b), "metadata_decided_by": r.decided_by}
        for r in xw.itertuples(index=False)]})
    # 10 spot check
    sp = pd.read_csv(OUT / "spotcheck_p78.csv") if (OUT / "spotcheck_p78.csv").exists() else pd.DataFrame()
    if len(sp):
        ds.append({"dataset": "spotcheck_p78", "examples": [
            {"input": dumps({"concept": r.concept, "aliases_used": [a for a in str(r.aliases_used).split("|") if a and a != "nan"],
                             "t0": None if pd.isna(r.t0) else int(r.t0), "iter1_group": None if pd.isna(r.iter1_group) else r.iter1_group,
                             "iter1_home": None if pd.isna(r.iter1_home) else r.iter1_home}),
             "output": dumps({"joined": bool(r.joined), "openalex_id": None if pd.isna(r.openalex_id) else r.openalex_id,
                              "oa_label": None if pd.isna(r.oa_label) else r.oa_label,
                              "provisional_group": None if pd.isna(r.provisional_group) else r.provisional_group,
                              "events": [e for e in str(r.events).split("; ") if e and e != "nan"],
                              "sources_checked": json.loads(r.sources_checked) if isinstance(r.sources_checked, str) else None}),
             "metadata_joined": bool(r.joined), "metadata_iter1_status": r.iter1_status}
            for r in sp.itertuples(index=False)]})
    return ds


def write_parts(ds: list[dict]) -> list[str]:
    d = ROOT / "full_data_out"
    d.mkdir(exist_ok=True)
    for f in d.glob("full_data_out_*.json"):
        f.unlink()
    parts, cur, cur_bytes = [], [], 0
    meta = {"description": "External, dated recognition events for OpenAlex legacy concepts (zero OpenAlex credits). "
                           "See README.md for field definitions, source biases and lags.",
            "parts_note": "Datasets are split across numbered parts; concatenate examples of equal 'dataset' names."}
    for d_ in ds:
        chunk = []
        for x in d_["examples"]:
            sz = len(dumps(x)) + 2
            if cur_bytes + sz > PART_BYTES and (chunk or cur):
                if chunk:
                    cur.append({"dataset": d_["dataset"], "examples": chunk})
                parts.append(cur)
                cur, chunk, cur_bytes = [], [], 0
            chunk.append(x)
            cur_bytes += sz
        if chunk:
            cur.append({"dataset": d_["dataset"], "examples": chunk})
    if cur:
        parts.append(cur)
    names = []
    for i, p in enumerate(parts, 1):
        f = d / f"full_data_out_{i}.json"
        f.write_text(json.dumps({"metadata": meta | {"part": i, "n_parts": len(parts)}, "datasets": p}, ensure_ascii=False))
        names.append(str(f.relative_to(ROOT)))
    return names


def trunc(x, n=300):
    if isinstance(x, str):
        return x if len(x) <= n else x[:n] + "..."
    if isinstance(x, list):
        return [trunc(y, n) for y in x]
    if isinstance(x, dict):
        return {k_: trunc(v_, n) for k_, v_ in x.items()}
    return x


@logger.catch(reraise=True)
def main() -> None:
    setup_logging("s9_outputs")
    R = pd.read_pickle(WORK / "concept_rows.pkl")
    agr = json.loads((OUT / "llm_agreement.json").read_text())
    rep = coverage(R, agr)
    (OUT / "coverage_report.json").write_text(json.dumps(rep, indent=1, default=str))
    logger.info(f"coverage by source: " + json.dumps({s: (d['n_with_event'], d['n_with_year_usable_event']) for s, d in rep['by_source'].items()}))
    logger.info(f"groups without dated domain taxonomy: {rep['groups_without_dated_domain_taxonomy']}")
    sp = spot_p78(R)
    if len(sp):
        sp.to_csv(OUT / "spotcheck_p78.csv", index=False)
        logger.info(f"P78 join rate {sp.joined.mean():.3f} ({sp.joined.sum()}/{len(sp)})")
    ds = build_datasets(R)
    names = write_parts(ds)
    logger.info(f"full parts: {names}")
    rnd = random.Random(0)
    mini, prev = [], []
    for d_ in ds:
        exs = d_["examples"]
        if d_["dataset"] == "concept_recognition":
            by = defaultdict(list)
            for x in exs:
                if x["metadata_level"] >= 2:
                    by[x["metadata_group"]].append(x)
            m = []
            per = max(1, 200 // len(by))
            for g in sorted(by):
                cand = sorted(by[g], key=lambda x: -x["metadata_n_events"])[:per // 2] + rnd.sample(by[g], min(len(by[g]), per - per // 2))
                m += cand
            m = m[:200]
        else:
            m = exs[:200] if len(exs) <= 200 else rnd.sample(exs, 200)
        mini.append({"dataset": d_["dataset"], "examples": m})
        prev.append({"dataset": d_["dataset"], "examples": trunc(m[:10])})
    (ROOT / "mini_data_out.json").write_text(json.dumps({"datasets": mini}, ensure_ascii=False, indent=1))
    (ROOT / "preview_data_out.json").write_text(json.dumps({"datasets": prev}, ensure_ascii=False, indent=1))
    logger.info("mini and preview written; dataset sizes " + json.dumps({d_["dataset"]: len(d_["examples"]) for d_ in ds}))


if __name__ == "__main__":
    main()
