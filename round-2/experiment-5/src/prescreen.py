#!/usr/bin/env python3
"""STEP 2: outcome-blind pre-screen on a ~1% random file sample (seed 20260928).

(a) `sample`: read ~20 random works files (base works 1995-2022 only), store titles+year to scan/sample_titles/part_*.parquet.
(b) `names`: AC + stemmed verification of lexicon_v0 forms; drop concepts with >= 10 sampled verified hits in
    1995-2002 (=> >= ~1,000 works in 8 years, so t0 >= 2003 is impossible). Low counts never drop a concept.
(c) `aliases`: Wikidata English aliases for survivors (drop <= 3 chars, all-caps <= 5 chars unless the name is
    that acronym, aliases equal to another concept's name/alias, aliases with >= 10 sampled pre-2003 hits).
    Writes lexicon_v1.parquet and appends its sha256 to frozen_lexicon.sha256.

Usage: python prescreen.py sample|names|aliases"""
from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import random
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from common import (ES_STOP, RES, ROOT, SAMPLE_TITLES_DIR, SCAN, SEED, Y0, Y1, phrase_spec, plural_variants,
                    read_parquet_parts, setup_logger, surf, surf_arrow, works_files, write_parquet_parts)

logger = setup_logger("prescreen")
N_SAMPLE_FILES = 20
PRE_MAX = 10
SAMPLE_PQ = SAMPLE_TITLES_DIR  # directory of part_*.parquet (each < 100 MB)


def read_sample_file(key: str, size: int) -> pa.Table:
    from rangefile import read_columns
    tb = read_columns(key, size, ["title", "publication_year", "type", "is_paratext", "is_xpac"], n_threads=8)
    base = pc.and_(pc.fill_null(pc.is_in(tb.column("type"), value_set=pa.array(["article", "review"])), False),
                   pc.invert(pc.fill_null(tb.column("is_paratext"), False)))
    base = pc.and_(base, pc.invert(pc.fill_null(tb.column("is_xpac"), False)))
    yr = tb.column("publication_year")
    base = pc.and_(base, pc.and_(pc.greater_equal(yr, Y0), pc.less_equal(yr, Y1)))
    base = pc.and_(base, pc.is_valid(tb.column("title")))
    t = tb.filter(base).select(["title", "publication_year"])
    return pa.table({"title": t.column("title"), "year": pc.cast(t.column("publication_year"), pa.int16()),
                     "stitle": surf_arrow(t.column("title"))})


def do_sample() -> None:
    files = works_files()
    pick = random.Random(SEED).sample(files, N_SAMPLE_FILES)
    t0 = time.time()
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as ex:
        tabs = list(ex.map(lambda f: read_sample_file(f[1], f[2]), pick))
    tb = pa.concat_tables(tabs)
    write_parquet_parts(tb.to_pandas(), SAMPLE_PQ)
    n_rows_sample = sum(f[3] for f in pick)
    n_rows_all = sum(f[3] for f in files)
    info = {"files": [f[0] for f in pick], "rows_sampled_all_types": n_rows_sample, "rows_total_all_types": n_rows_all,
            "sample_fraction": n_rows_sample / n_rows_all, "base_rows_1995_2022_in_sample": tb.num_rows,
            "seconds": time.time() - t0}
    (SCAN / "sample_info.json").write_text(json.dumps(info, indent=1))
    logger.info(f"sample: {info}")


# ----------------------------------------------------------------------------- parallel matching
_W: dict = {}


def _init(entries: list) -> None:
    from matcher import build_automaton
    A, specs = build_automaton(entries)
    _W.update(A=A, specs=specs)


def _match_chunk(args) -> list[tuple[int, int, int]]:
    from matcher import match
    stitles, titles, years = args
    out = []
    for st, t, y in zip(stitles, titles, years):
        for ci, mt in match(st, t, _W["A"], _W["specs"]).items():
            out.append((ci, y, mt))
    return out


def run_matching(entries: list[tuple[str, int, str]], n_workers: int = 4) -> list[tuple[int, int, int]]:
    tb = pa.Table.from_pandas(read_parquet_parts(SAMPLE_PQ), preserve_index=False)
    st, ti, yr = tb.column("stitle").to_pylist(), tb.column("title").to_pylist(), tb.column("year").to_pylist()
    n = len(st)
    step = 100_000
    chunks = [(st[i:i + step], ti[i:i + step], yr[i:i + step]) for i in range(0, n, step)]
    res = []
    with ProcessPoolExecutor(n_workers, mp_context=mp.get_context("spawn"), initializer=_init,
                             initargs=(entries,)) as ex:
        for r in ex.map(_match_chunk, chunks):
            res.extend(r)
    return res


def do_names() -> None:
    lex = pd.read_parquet(ROOT / "lexicon_v0.parquet")
    entries = [(f, ci, m) for ci, (fs, ms) in enumerate(zip(lex.forms, lex.mtypes)) for f, m in zip(fs, ms)]
    t0 = time.time()
    hits = run_matching(entries)
    logger.info(f"names matching: {len(hits)} verified hits in {time.time()-t0:.0f}s")
    h = pd.DataFrame(hits, columns=["ci", "year", "mt"])
    pre = h[h.year <= 2002].groupby("ci").size()
    post = h[h.year >= 2003].groupby("ci").size()
    lex["pre_hits"] = lex.index.map(pre).fillna(0).astype(int)
    lex["post_hits"] = lex.index.map(post).fillna(0).astype(int)
    drop = lex[lex.pre_hits >= PRE_MAX]
    drop[["concept_id", "name", "level", "pre_hits", "post_hits"]].sort_values("pre_hits", ascending=False).to_csv(
        RES / "prescreen_dropped.csv", index=False)
    surv = lex[lex.pre_hits < PRE_MAX].copy()
    surv.to_parquet(SCAN / "prescreen_survivors.parquet", index=False)
    info = json.loads((SCAN / "sample_info.json").read_text())
    info.update({"n_lexicon_v0": len(lex), "n_dropped_pre2003": len(drop), "n_survivors": len(surv),
                 "survivors_with_post2003_hits": int((surv.post_hits > 0).sum()), "threshold": PRE_MAX})
    (RES / "prescreen_summary.json").write_text(json.dumps(info, indent=1))
    logger.info(f"prescreen: dropped {len(drop)}, survivors {len(surv)}")


def do_aliases() -> None:
    surv = pd.read_parquet(SCAN / "prescreen_survivors.parquet")
    lex0 = pd.read_parquet(ROOT / "lexicon_v0.parquet")
    wd = json.loads((SCAN / "wikidata_aliases.json").read_text())
    from lexicon import PAREN, load_concepts
    lvl01 = {surf(PAREN.sub(" ", n)) for n in load_concepts().query("level <= 1").display_name}
    all_names = Counter()
    for f in lvl01:
        all_names[f] += 1
    for fs in lex0.forms:
        for f in fs:
            all_names[f] += 1
    cand: dict[int, list[str]] = {}
    alias_owner: dict[str, set[int]] = defaultdict(set)
    reasons = Counter()
    for i, r in surv.iterrows():
        e = wd.get(r.qid)
        if not e:
            continue
        own = set(r.forms)
        name_s = surf(r["name"]).strip()
        keep = []
        for a in e.get("aliases", []) + ([e["label"]] if e.get("label") else []):
            s = surf(a)
            core = s.strip()
            if not core or s in own:
                continue
            if len(core) <= 3:
                reasons["le3"] += 1
                continue
            if a.isupper() and len(a.replace(" ", "")) <= 5 and core != name_s:
                reasons["acronym"] += 1
                continue
            if all(t in ES_STOP for t in core.split()) or not phrase_spec(core) or core.isdigit():
                reasons["stop"] += 1
                continue
            if s in all_names:
                reasons["other_concept_name_or_level01"] += 1
                continue
            if len(core.split()) == 1 and not any(ch.isupper() for ch in a.strip()[1:]):
                # T2 fix: single-token lowercase aliases ('socials', 'ashes', 'morals') are generic words;
                # a single-token alias is kept only if it is mixed-case/acronym-like (miRNA, lncRNA, MOFs)
                reasons["single_token_lowercase"] += 1
                continue
            keep.append(s)
        for s in set(keep):
            alias_owner[s].add(int(r.concept_id))
        cand[int(r.concept_id)] = list(set(keep))
    amb = {s for s, o in alias_owner.items() if len(o) > 1}
    reasons["ambiguous_alias"] = len(amb)
    id2i = {cid: i for i, cid in enumerate(surv.concept_id)}
    entries = [(s, id2i[cid], "alias") for cid, ss in cand.items() for s in ss if s not in amb]
    logger.info(f"alias candidates: {len(entries)}; drops {dict(reasons)}")
    hits = run_matching(entries)
    # pre-2003 alias frequency per (concept, alias): recompute by alias string
    from matcher import build_automaton, match  # noqa: F401
    h = pd.DataFrame(hits, columns=["ci", "year", "mt"])
    # hits are per concept (best alias); to drop individual aliases we re-match per alias on pre-2003 titles
    tb = read_parquet_parts(SAMPLE_PQ)
    pre_titles = tb[tb.year <= 2002]
    import ahocorasick
    A = ahocorasick.Automaton()
    for s, ci, _ in entries:
        A.add_word(s, s)
    A.make_automaton()
    cnt = Counter()
    for st in pre_titles.stitle:
        for _, s in A.iter(st):
            cnt[s] += 1
    bad = {s for s, c in cnt.items() if c >= PRE_MAX}
    reasons["alias_pre2003_frequent"] = len(bad)
    rows = []
    for i, r in surv.reset_index(drop=True).iterrows():
        al = [s for s in cand.get(int(r.concept_id), []) if s not in amb and s not in bad]
        # plural variants of aliases
        extra = []
        for s in al:
            if len(s.split()) == 1:
                continue  # T2 fix: no plural variants of single-token aliases
            for v in plural_variants(s.strip()):
                vs = " " + v + " "
                if vs not in all_names and vs not in al and vs not in extra and vs not in amb:
                    extra.append(vs)
        forms = list(r.forms) + al + extra
        mtypes = list(r.mtypes) + ["alias"] * (len(al) + len(extra))
        rows.append({"concept_id": int(r.concept_id), "qid": r.qid, "name": r["name"], "level": int(r.level),
                     "description": r.description, "wd_description": (wd.get(r.qid) or {}).get("description") or "",
                     "works_count_legacy": int(r.works_count_legacy), "pre_hits_sample": int(r.pre_hits),
                     "post_hits_sample": int(r.post_hits), "forms": forms, "mtypes": mtypes,
                     "aliases_used": "|".join(s.strip() for s in al)})
    lex1 = pd.DataFrame(rows)
    out = ROOT / "lexicon_v1.parquet"
    lex1.to_parquet(out, index=False)
    hsh = hashlib.sha256(out.read_bytes()).hexdigest()
    with (ROOT / "frozen_lexicon.sha256").open("a") as f:
        f.write(f"lexicon_v1.parquet {hsh}\n")
    summ = json.loads((RES / "prescreen_summary.json").read_text())
    summ["alias"] = {"reasons": dict(reasons), "n_alias_forms": int(sum(m.count("alias") for m in lex1.mtypes)),
                     "concepts_with_alias": int((lex1.aliases_used != "").sum()), "lexicon_v1_sha256": hsh,
                     "n_concepts_v1": len(lex1)}
    (RES / "prescreen_summary.json").write_text(json.dumps(summ, indent=1))
    logger.info(f"lexicon_v1: {len(lex1)} concepts; {summ['alias']}")


if __name__ == "__main__":
    {"sample": do_sample, "names": do_names, "aliases": do_aliases}[sys.argv[1]]()
