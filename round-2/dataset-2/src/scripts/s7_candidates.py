#!/usr/bin/env python3
"""STEP 7b: candidate generation between external entries and concepts -> work/entries.parquet, work/candidates.parquet.

Entries = every MeSH descriptor, every taxonomy node, every list item. Candidate methods:
  wikidata_property : Wikidata P486 (MeSH UI), P2179 (ACM 2012 id), P3285 (MSC code)       conf 1.0
  exact_norm_label  : entry label/term == concept display-name (normalised)                   conf 0.9 (MeSH 0.85)
  exact_norm_alias  : entry label/term == concept alias (normalised)                          conf 0.85
  wikilink          : list item links to the concept's enwiki article (redirects resolved)    -> LLM
  fuzzy             : rapidfuzz token_set_ratio >= 88 & token_sort_ratio >= 70 over a rare-token block -> LLM
  embed             : all-MiniLM-L6-v2 cosine top-5 >= 0.75 (list items only)                 -> LLM
Generic taxonomy labels ('General', 'None of the above...', 'Proceedings...') are not label-matched.
"""
from __future__ import annotations

import json
import multiprocessing as mp
import re
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
import requests
from loguru import logger

from common import UA, WORK, norm_label, setup_logging

GENERIC = re.compile(r"^(general|generalities|miscellaneous|other|others|none of the above|proceedings|research exposition|"
                     r"instructional exposition|explicit machine computation|computational method|software|research data|"
                     r"biographies|bibliographies|dictionaries|historical|history|introductory exposition|"
                     r"problem books|applications|theory|methods|models|experimental|special topics|"
                     r"external book reviews|collections|computer science|mathematics|physics|chemistry|biology|"
                     r"medicine|engineering|economics|psychology)\b")
STOP = {"and", "the", "of", "in", "for", "on", "with", "to", "a", "an", "by", "or", "its", "from", "as", "at", "into",
        "etc", "e", "g", "via", "other", "general", "theory", "method", "system", "analysis", "application", "model"}
FUZZ_MIN_SET, FUZZ_MIN_SORT = 88, 70

# populated in workers
_G: dict = {}


def _toks(s: str) -> list[str]:
    return [t for t in s.split() if len(t) >= 3 and t not in STOP]


def _init(strings, owners, index):
    _G["s"], _G["o"], _G["idx"] = strings, owners, index


def _fuzzy_one(args):
    from rapidfuzz import fuzz
    eid, text = args
    cand = set()
    for t in set(_toks(text)):
        cand.update(_G["idx"].get(t, ()))
    out = {}
    for j in cand:
        s = _G["s"][j]
        a = fuzz.token_set_ratio(text, s)
        if a < FUZZ_MIN_SET:
            continue
        b = fuzz.token_sort_ratio(text, s)
        if b < FUZZ_MIN_SORT:
            continue
        o = _G["o"][j]
        sc = (a + b) / 2
        if sc > out.get(o, 0):
            out[o] = sc
    best = sorted(out.items(), key=lambda x: -x[1])[:5]
    return eid, best


def build_entries() -> pd.DataFrame:
    mesh = pd.read_parquet(WORK / "mesh_desc.parquet")
    tax = pd.read_parquet(WORK / "tax_entries.parquet")
    lst = pd.read_parquet(WORK / "list_entries.parquet")
    rows = []
    for r in mesh.itertuples(index=False):
        rows.append({"entry_id": f"mesh:{r.mesh_ui}", "family": "mesh", "source": "mesh", "version": 2026,
                     "year": r.mesh_year_best, "code": r.mesh_ui, "label": r.mesh_name,
                     "alt_labels": [t for t in r.entry_terms if t != r.mesh_name],
                     "descriptor": r.scope_first_sentence, "generic": False})
    supp_p = WORK / "mesh_supp.parquet"
    if supp_p.exists():
        for r in pd.read_parquet(supp_p).itertuples(index=False):
            rows.append({"entry_id": f"mesh:{r.mesh_ui}", "family": "mesh", "source": "mesh_scr", "version": 2026,
                         "year": r.date_introduced_year, "code": r.mesh_ui, "label": r.mesh_name,
                         "alt_labels": [t for t in r.entry_terms if t != r.mesh_name],
                         "descriptor": r.note, "generic": False})
    for r in tax.itertuples(index=False):
        ln = r.label_norm
        rows.append({"entry_id": f"{r.source}:{r.version if pd.notna(r.version) else 'na'}:{r.code}", "family": r.source,
                     "source": r.source, "version": int(r.version) if pd.notna(r.version) else None,
                     "year": int(r.version) if pd.notna(r.version) else None, "code": r.code, "label": r.label,
                     "alt_labels": list(r.alt_labels) if r.alt_labels is not None else [], "descriptor": None,
                     "generic": bool(GENERIC.match(ln)) or len(ln) < 3})
    for r in lst.itertuples(index=False):
        rows.append({"entry_id": r.entry_id, "family": "lists", "source": r.source, "version": None, "year": r.year,
                     "code": str(r.rank) if pd.notna(r.rank) else None, "label": r.item_text, "alt_labels": [],
                     "descriptor": r.descriptor, "generic": False})
    e = pd.DataFrame(rows)
    e["label_norm"] = e.label.map(norm_label)
    e["alt_norms"] = e.alt_labels.map(lambda xs: sorted({norm_label(x) for x in xs} - {""}))
    return e


def resolve_titles(titles: list[str]) -> dict[str, str]:
    """Map wiki link targets to their redirect-resolved article titles (50 per call)."""
    out = {}
    s = requests.Session()
    s.headers["User-Agent"] = UA
    for i in range(0, len(titles), 50):
        b = titles[i:i + 50]
        import time
        for _ in range(10):
            resp = s.get("https://en.wikipedia.org/w/api.php", params={"action": "query", "titles": "|".join(b),
                         "redirects": 1, "format": "json", "formatversion": 2}, timeout=60)
            if resp.status_code == 429:
                time.sleep(float(resp.headers.get("Retry-After", 10)))
                continue
            break
        r = resp.json()
        q = r.get("query", {})
        norm = {x["from"]: x["to"] for x in q.get("normalized", [])}
        red = {x["from"]: x["to"] for x in q.get("redirects", [])}
        for t in b:
            u = norm.get(t, t)
            out[t] = red.get(u, u)
    return out


@logger.catch(reraise=True)
def main() -> None:
    setup_logging("s7_candidates")
    k = pd.read_parquet(WORK / "concept_keys.parquet")
    e = build_entries()
    e.to_parquet(WORK / "entries.parquet", index=False)
    logger.info(f"entries {len(e)} by family {e.family.value_counts().to_dict()}; generic {int(e.generic.sum())}")

    cand = []   # (entry_id, openalex_id, method, score)
    # ---- ID links
    mesh_ui = set(e.loc[e.family == "mesh", "code"])
    acm12 = e[(e.source == "acm_ccs") & (e.version == 2012)]
    acm_leaf = defaultdict(list)
    for eid, code in zip(acm12.entry_id, acm12.code):
        acm_leaf[str(code).split(".")[-1]].append(eid)
    msc = e[e.source == "msc"]
    msc_code = defaultdict(list)
    for eid, code in zip(msc.entry_id, msc.code):
        msc_code[str(code)].append(eid)
    p486_missing = []
    for r in k.itertuples(index=False):
        for ui in r.p486:
            if ui in mesh_ui:
                cand.append((f"mesh:{ui}", r.openalex_id, "wikidata_property", 1.0))
            else:
                p486_missing.append((r.openalex_id, ui))
        for c in r.p2179:
            for eid in acm_leaf.get(str(c).split(".")[-1], []):
                cand.append((eid, r.openalex_id, "wikidata_property", 1.0))
        for c in r.p3285:
            for eid in msc_code.get(str(c), []):
                cand.append((eid, r.openalex_id, "wikidata_property", 1.0))
    logger.info(f"ID links {len(cand)}; P486 values not in desc2026: {len(p486_missing)} e.g. {p486_missing[:5]}")
    pd.DataFrame(p486_missing, columns=["openalex_id", "p486"]).to_csv(WORK / "p486_not_in_desc.csv", index=False)

    # ---- exact normalised
    lab = defaultdict(set)
    ali = defaultdict(set)
    for r in k.itertuples(index=False):
        if r.label_norm:
            lab[r.label_norm].add(r.openalex_id)
        for a in r.aliases_norm:
            ali[a].add(r.openalex_id)
    n_ex = 0
    for r in e.itertuples(index=False):
        if r.generic:
            continue
        terms = [r.label_norm] + list(r.alt_norms)
        for t in terms:
            for oid in lab.get(t, ()):
                cand.append((r.entry_id, oid, "exact_norm_label", 0.85 if r.family == "mesh" else 0.9))
                n_ex += 1
            for oid in ali.get(t, ()):
                cand.append((r.entry_id, oid, "exact_norm_alias", 0.85))
                n_ex += 1
    logger.info(f"exact candidate pairs {n_ex}")

    # ---- wiki links of list items
    lst = pd.read_parquet(WORK / "list_entries.parquet")
    title2c = defaultdict(set)
    for r in k.itertuples(index=False):
        if r.enwiki_title:
            title2c[r.enwiki_title].add(r.openalex_id)
    links = sorted({t for xs in lst.wiki_links for t in xs} | {t for xs in lst.descriptor_links for t in xs})
    res = resolve_titles(links)
    n_wl = 0
    for r in lst.itertuples(index=False):
        for t in list(r.wiki_links):
            for oid in title2c.get(res.get(t, t), set()) | title2c.get(t, set()):
                cand.append((r.entry_id, oid, "wikilink", 0.0))
                n_wl += 1
    logger.info(f"wikilink candidates {n_wl} from {len(links)} link titles")

    # ---- fuzzy (taxonomy nodes and list items without an exact/ID candidate)
    have = {c[0] for c in cand}
    strings, owners = [], []
    for r in k.itertuples(index=False):
        for s in [r.label_norm] + list(r.aliases_norm):
            if s:
                strings.append(s)
                owners.append(r.openalex_id)
    df_tok = defaultdict(int)
    for s in strings:
        for t in set(_toks(s)):
            df_tok[t] += 1
    index = defaultdict(list)
    for j, s in enumerate(strings):
        for t in set(_toks(s)):
            if df_tok[t] <= 300:
                index[t].append(j)
    todo = e[(e.family != "mesh") & (~e.generic) & (~e.entry_id.isin(have)) & (e.family != "jel")]
    uniq = todo.drop_duplicates("label_norm")
    logger.info(f"fuzzy: {len(todo)} entries without candidates, {len(uniq)} unique labels; {len(strings)} concept strings")
    with ProcessPoolExecutor(4, mp_context=mp.get_context("spawn"), initializer=_init,
                             initargs=(strings, owners, dict(index))) as ex:
        fz = dict(ex.map(_fuzzy_one, list(zip(uniq.label_norm, uniq.label_norm)), chunksize=200))
    n_fz = 0
    for r in todo.itertuples(index=False):
        for oid, sc in fz.get(r.label_norm, []):
            cand.append((r.entry_id, oid, "fuzzy", sc / 100))
            n_fz += 1
    logger.info(f"fuzzy candidates {n_fz}")

    # ---- MiniLM embeddings for list items
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    ck = k[k.label.notna()].reset_index(drop=True)
    ep = WORK / "concept_label_emb.npy"
    emb_c = np.load(ep).astype(np.float32) if ep.exists() else None
    if emb_c is None or len(emb_c) != len(ck):
        emb_c = model.encode(ck.label.tolist(), batch_size=512, normalize_embeddings=True, show_progress_bar=False)
        np.save(ep, emb_c.astype(np.float16))
    le = e[e.family == "lists"].reset_index(drop=True)
    t1 = le.label.fillna("").tolist()
    t2 = (le.label.fillna("") + ". " + le.descriptor.fillna("").str[:200]).tolist()
    s1 = model.encode(t1, batch_size=256, normalize_embeddings=True) @ emb_c.T
    s2 = model.encode(t2, batch_size=256, normalize_embeddings=True) @ emb_c.T
    S = np.maximum(s1, s2)
    n_em = 0
    for i, eid in enumerate(le.entry_id):
        top = np.argsort(-S[i])[:5]
        for j in top:
            if S[i, j] >= 0.75:
                cand.append((eid, ck.openalex_id[j], "embed", float(S[i, j])))
                n_em += 1
    logger.info(f"embedding candidates {n_em}")

    cd = pd.DataFrame(cand, columns=["entry_id", "openalex_id", "method", "score"])
    agg = cd.groupby(["entry_id", "openalex_id"]).agg(methods=("method", lambda x: sorted(set(x))),
                                                      score=("score", "max")).reset_index()
    agg.to_parquet(WORK / "candidates.parquet", index=False)
    assert not e.entry_id.duplicated().any(), "duplicate entry ids"
    fam = e.set_index("entry_id").family
    agg["family"] = agg.entry_id.map(fam)
    logger.info(f"candidate pairs {len(agg)}; entries with >=1 candidate by family "
                f"{agg.groupby('family').entry_id.nunique().to_dict()}")
    json.dump({"link_titles_resolved": res}, (WORK / "wikilink_resolution.json").open("w"))


if __name__ == "__main__":
    main()
