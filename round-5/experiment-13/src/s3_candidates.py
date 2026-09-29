#!/usr/bin/env python3
"""S2 balance check + S3 CANDIDATES (outcome-blind; sample counts only).

1. balance: sample base works per (year, vfield) vs EXP10 passC_totals G (ratios ~0.2; TVD of field mix <= 0.05)
2. superset U = keys that pass the candidate rule at k = 3 in any t in 2003..2017
3. string recovery over the stored sample titles (surface forms + up to 5 context titles per key)
4. lexical exclusions (i) legacy exact key, (ii) multi-token legacy containment, (iii) generic list / place names
5. k_t per year (cap 4,500 after exclusions), t_det, POS filter (spaCy)
6. recall benchmark on EXP5 legacy newborns (report only)
Writes data/frame_n_candidates.csv, results/sample_balance.json, results/mining_recall.json, results/s3_summary.json
and appends S3_candidates to logs/seal.log.  Usage: python s3_candidates.py [--stage recover|select|all]"""
from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, EXP5, INPUTS, RES, ROOT, jdump, read_parquet_parts, setup_logger, sha256_file, write_parquet_parts

logger = setup_logger("s3_candidates")
Y0, Y1 = 2000, 2017
YEARS = list(range(Y0, Y1 + 1))
T_LO, T_HI = 2003, 2017
CAP = 4500
MIN_SRC = 0          # v2: the source-diversity burst filter was evaluated (MIN_SRC=3) and NOT used (D_v2_remine)
K_FIXED = 4          # v2: k_t fixed at 4 for every year (cap lifted; plan remedy for overall recall < 15%)
MERGED = ROOT / "passM" / "merged"
PARTS = ROOT / "passM" / "parts"
REC = DATA / "s3_recovery"


# ----------------------------------------------------------------------------- 1. balance
def balance() -> dict:
    bal = np.load(ROOT / "passM" / "sample_bal.npy").astype(float)          # [2000..2017, 27]
    G = np.load(INPUTS / "passC_totals.npz")["G"].astype(float)[Y0 - 1995:Y1 - 1995 + 1]
    out = {"years": {}, "fail": False}
    for k, y in enumerate(YEARS):
        r = bal[k].sum() / G[k].sum()
        p, q = bal[k, 1:] / max(bal[k, 1:].sum(), 1), G[k, 1:] / max(G[k, 1:].sum(), 1)
        tvd = 0.5 * np.abs(p - q).sum()
        out["years"][y] = {"ratio": float(r), "tvd_field_mix": float(tvd)}
        if not (0.12 <= r <= 0.30) or tvd > 0.05:
            out["fail"] = True
    out["overall_ratio"] = float(bal.sum() / G.sum())
    return out


# ----------------------------------------------------------------------------- 2. candidate rule
def load_counts() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ks, Ss, ns = [], [], []
    for p in sorted(MERGED.glob("bucket_*.npz")):
        z = np.load(p)
        ks.append(z["keys"]); Ss.append(z["S"]); ns.append(z["nlen"])
    return np.concatenate(ks), np.concatenate(Ss), np.concatenate(ns)


def cand_matrix(S: np.ndarray, kt: dict[int, int], NS: np.ndarray | None = None) -> np.ndarray:
    """C[key, t] for t in 2003..2017: s_t >= k_t and max(s_{t-3..t-1}) <= floor(0.25 s_t)
    [v2: and n_src_t >= MIN_SRC distinct primary sources among the year-t sample occurrences]."""
    C = np.zeros((len(S), T_HI - T_LO + 1), bool)
    for j, t in enumerate(range(T_LO, T_HI + 1)):
        i = t - Y0
        st = S[:, i]
        prior = S[:, i - 3:i].max(1)
        C[:, j] = (st >= kt[t]) & (prior <= np.floor(0.25 * st))
        if NS is not None:
            C[:, j] &= NS[:, i] >= MIN_SRC
    return C


def nsrc_matrix(keys: np.ndarray) -> np.ndarray:
    ns = pd.read_parquet(REC / "nsrc.parquet")
    pos = pd.Series(np.arange(len(keys)), index=keys.astype(np.uint64))
    ns = ns[ns.h.isin(pos.index)]
    NS = np.zeros((len(keys), len(YEARS)), np.int32)
    NS[pos.loc[ns.h.to_numpy(np.uint64)].to_numpy(), ns.year.to_numpy(np.int64) - Y0] = ns.n_src.to_numpy()
    return NS


# ----------------------------------------------------------------------------- 3. recovery
def recover_file(fi: int, keys_sorted: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    import pyarrow as pa
    import pyarrow.compute as pc

    from common5 import surf_arrow
    from nrules import ngram_table
    t = pd.read_parquet(PARTS / f"titles_{fi:04d}.parquet", columns=["title", "year", "source"])
    if not len(t):
        return (pd.DataFrame(columns=["h", "form", "c"]), pd.DataFrame(columns=["h", "fi", "row"]),
                pd.DataFrame(columns=["h", "year", "source"]))
    st = pc.utf8_trim_whitespace(surf_arrow(pa.array(t.title.tolist())))
    ng = ngram_table(st, want_forms=True)
    pos = np.clip(np.searchsorted(keys_sorted, ng["h"]), 0, len(keys_sorted) - 1)
    m = keys_sorted[pos] == ng["h"]
    d = pd.DataFrame({"h": ng["h"][m], "form": ng["form"][m], "row": ng["row"][m]}).drop_duplicates(["h", "row"])
    forms = d.groupby(["h", "form"]).size().rename("c").reset_index()
    ctx = d.groupby("h").head(2)[["h", "row"]].assign(fi=fi)
    rows = d.row.to_numpy()
    src = pd.DataFrame({"h": d.h.to_numpy(), "year": t.year.to_numpy()[rows].astype(np.int16),
                        "source": t.source.to_numpy()[rows]})
    src = src[src.source > 0].drop_duplicates()
    return forms, ctx, src


def recover(U: np.ndarray, workers: int) -> None:
    REC.mkdir(parents=True, exist_ok=True)
    fis = sorted(int(p.stem.split("_")[1]) for p in PARTS.glob("done_*.json"))
    keys_sorted = np.sort(U)
    fs, cs, ss = [], [], []
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn")) as ex:
        for k, (f, c, sr) in enumerate(ex.map(recover_file, fis, [keys_sorted] * len(fis), chunksize=4)):
            fs.append(f); cs.append(c); ss.append(sr)
            if k % 100 == 0:
                logger.info(f"recovery {k}/{len(fis)}")
    forms = pd.concat([f for f in fs if len(f)], ignore_index=True).groupby(["h", "form"], as_index=False)["c"].sum()
    ctx = pd.concat([c for c in cs if len(c)], ignore_index=True).astype({"row": np.int64, "fi": np.int64}).sort_values(["h", "fi", "row"]).groupby("h").head(5)
    # attach context titles
    tl = []
    for fi, g in ctx.groupby("fi"):
        t = pd.read_parquet(PARTS / f"titles_{fi:04d}.parquet", columns=["title"])
        rr = g.row.to_numpy().astype(np.int64)
        tl.append(pd.DataFrame({"h": g.h.to_numpy().astype(np.uint64), "fi": fi, "row": rr,
                                "title": t.title.to_numpy()[rr]}))
    ctx = pd.concat(tl, ignore_index=True).sort_values(["h", "fi", "row"])
    nsrc = pd.concat([x for x in ss if len(x)], ignore_index=True).drop_duplicates().groupby(
        ["h", "year"]).size().rename("n_src").reset_index()
    nsrc.to_parquet(REC / "nsrc.parquet", index=False)
    forms.to_parquet(REC / "forms.parquet", index=False)
    write_parquet_parts(ctx, REC / "contexts", rows_per_part=500_000)   # split parts, each < 100 MB
    logger.info(f"recovered forms for {forms.h.nunique()} keys; contexts {len(ctx)}")


# ----------------------------------------------------------------------------- 4. exclusions
def legacy_keys() -> tuple[set, set, set]:
    from common5 import surf
    from nrules import key_of_tokens
    forms: set[str] = set()
    lex = pd.read_parquet(INPUTS / "lexicon_v1.parquet", columns=["name", "forms"])
    for fs in lex.forms:
        forms.update(str(f) for f in fs)
    forms.update(lex.name.astype(str))
    o7 = pd.read_parquet(INPUTS / "o7_concept_labels.parquet")
    forms.update(o7.label.dropna().astype(str))
    for al in o7.aliases:
        forms.update(str(a) for a in al)
    fr = pd.read_csv(EXP5 / "frame_concepts.csv", usecols=["name", "aliases_used"])
    forms.update(fr.name.astype(str))
    for a in fr.aliases_used.dropna():
        forms.update(x for x in str(a).split("|") if x)
    cc = pd.read_csv(INPUTS / "cohort_candidates.csv", usecols=["name"])
    forms.update(cc.name.astype(str))
    keys = {key_of_tokens(surf(f).split()) for f in forms}
    keys.discard(())
    multi = {k for k in keys if len(k) >= 2}
    subs = set()
    for k in multi:
        for n in (2, 3):
            for i in range(len(k) - n + 1):
                subs.add(k[i:i + n])
    logger.info(f"legacy forms {len(forms)} -> keys {len(keys)} (multi-token {len(multi)}, sub-tuples {len(subs)})")
    return keys, multi, subs


def place_keys() -> set:
    import geonamescache

    from common5 import surf
    from nrules import key_of_tokens
    gc = geonamescache.GeonamesCache()
    names = [c["name"] for c in gc.get_countries().values()]
    names += [c["name"] for c in gc.get_cities().values() if c.get("population", 0) >= 1_000_000]
    names += [s["name"] for s in gc.get_us_states().values()]
    keys = {key_of_tokens(surf(n).split()) for n in names}
    keys.discard(())
    return keys


def generic_keys() -> set:
    from common5 import surf
    from nrules import GENERIC, key_of_tokens
    return {key_of_tokens(surf(g).split()) for g in GENERIC}


def _gen_tok_stems() -> set:
    from nrules import GENERIC_TOKENS, stem
    return {stem(t) for t in GENERIC_TOKENS}


GEN_TOK_STEMS = _gen_tok_stems()


def exclusion_of(key: tuple, leg: set, multi: set, subs: set, gen: set, places: set) -> str:
    if key in leg:
        return "legacy_exact"
    if key in subs:
        return "contained_in_legacy"
    n = len(key)
    for m in (2, 3):
        for i in range(n - m + 1):
            if m < n and key[i:i + m] in multi:
                return "contains_legacy"
    if key in gen:
        return "generic_list"
    if any(t in GEN_TOK_STEMS for t in key):
        return "generic_token"
    for m in (1, 2, 3):
        for i in range(n - m + 1):
            if key[i:i + m] in places:
                return "place_name"
    return ""


# ----------------------------------------------------------------------------- 5. POS
def pos_ok_batch(items: list[tuple[int, list[str], list[str]]]) -> dict[int, float]:
    """items: (idx, surface tokens of the phrase form, context titles). Returns idx -> share of contexts that pass."""
    import spacy

    from common5 import surf
    from nrules import stem
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser", "lemmatizer"])
    flat = [(i, toks, t) for i, toks, ts in items for t in ts]
    docs = nlp.pipe([t for _, _, t in flat], batch_size=256)
    ok: dict[int, list[int]] = {}
    for (i, toks, _), doc in zip(flat, docs):
        seq = []
        for tk in doc:
            for s in surf(tk.text).split():
                seq.append((stem(s), tk.pos_))
        key = [stem(x) for x in toks]
        n = len(key)
        res = None
        for j in range(len(seq) - n + 1):
            if [s for s, _ in seq[j:j + n]] == key:
                tags = [p for _, p in seq[j:j + n]]
                good = tags[-1] in ("NOUN", "PROPN") and tags[0] in ("ADJ", "NOUN", "PROPN")
                if n == 3:
                    good &= tags[1] in ("ADJ", "NOUN", "PROPN", "ADP", "CCONJ", "DET")
                res = int(good)
                break
        if res is not None:
            ok.setdefault(i, []).append(res)
    return {i: float(np.mean(v)) for i, v in ok.items()}


# ----------------------------------------------------------------------------- main
def select(workers: int) -> None:
    keys, S, nlen = load_counts()
    kt3 = {t: 3 for t in range(T_LO, T_HI + 1)}
    C3 = cand_matrix(S, kt3)
    inU = C3.any(1)
    forms = pd.read_parquet(REC / "forms.parquet")
    ctx = read_parquet_parts(REC / "contexts")
    Uk, US, Un, UC = keys[inU], S[inU], nlen[inU], C3[inU]
    UNS = nsrc_matrix(Uk)
    top = forms.sort_values(["h", "c", "form"], ascending=[True, False, True]).groupby("h")
    name_of = top.head(1).set_index("h").form
    from nrules import key_of_tokens
    leg, multi, subs = legacy_keys()
    gen, places = generic_keys(), place_keys()
    names = name_of.reindex(Uk).to_numpy()
    excl = np.empty(len(Uk), object)
    keytup = []
    for j, nm in enumerate(names):
        if not isinstance(nm, str):
            excl[j] = "unrecovered"
            keytup.append(())
            continue
        k = key_of_tokens(nm.split())
        keytup.append(k)
        excl[j] = exclusion_of(k, leg, multi, subs, gen, places)
    ok_lex = excl == ""
    logger.info(f"superset U={len(Uk)}; exclusions: {pd.Series(excl).value_counts().to_dict()}")
    # k_t per year
    kt = {}
    for j, t in enumerate(range(T_LO, T_HI + 1)):
        i = t - Y0
        st, prior = US[:, i], US[:, i - 3:i].max(1)
        base = ok_lex & (prior <= np.floor(0.25 * st)) & (UNS[:, i] >= MIN_SRC)
        k = 3
        while (base & (st >= k)).sum() > CAP:
            k += 1
        kt[t] = K_FIXED if K_FIXED else k
    Ck = cand_matrix(US, kt, UNS)
    has = Ck.any(1)
    t_det = np.where(has, T_LO + np.argmax(Ck, 1), -1)
    logger.info(f"k_t = {kt}; candidates after k_t (before exclusions) {has.sum()}, after {int((has & ok_lex).sum())}")
    sel = np.nonzero(has & ok_lex)[0]
    # POS filter
    ctx_by = {h: g.title.tolist() for h, g in ctx[ctx.h.isin(set(Uk[sel].tolist()))].groupby("h")}
    items = [(int(j), names[j].split(), ctx_by.get(Uk[j], [])[:5]) for j in sel]
    chunks = [items[i::workers] for i in range(workers)]
    pos_share: dict[int, float] = {}
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn")) as ex:
        for d in ex.map(pos_ok_batch, chunks):
            pos_share.update(d)
    pos = np.array([pos_share.get(int(j), 0.0) for j in sel])
    excl_sel = excl[sel].copy()
    excl_sel[pos < 0.6] = "pos"
    # aliases: other surface forms with >= 2 sample occurrences (<= 6)
    alias_of = {}
    for h, g in top:
        f = g[(g.c >= 2)].form.tolist()
        alias_of[h] = f[1:7]
    rows = []
    for jj, j in enumerate(sel):
        h = Uk[j]
        rows.append({"h": np.uint64(h).astype(np.int64), "key": " ".join(keytup[j]), "name": names[j],
                     "aliases": "|".join(alias_of.get(h, [])), "n_tokens": int(Un[j]), "t_det": int(t_det[j]),
                     "k_t_det": kt[int(t_det[j])], "n_src_t_det": int(UNS[j, int(t_det[j]) - Y0]),
                     "pos_share": float(pos[jj]), "excluded_by": excl_sel[jj],
                     **{f"s_{y}": int(US[j, y - Y0]) for y in YEARS}})
    cand = pd.DataFrame(rows)
    keep = cand.excluded_by == ""
    cand["ci"] = -1
    cand.loc[keep, "ci"] = np.arange(int(keep.sum()))
    cand = cand.sort_values(["ci"]).reset_index(drop=True)
    cand.to_csv(DATA / "frame_n_candidates.csv", index=False)
    summ = {"U_superset": int(len(Uk)), "exclusions_superset": pd.Series(excl).value_counts().to_dict(), "k_t": kt,
            "after_k_t": int(has.sum()), "after_lexical": int(len(sel)), "pos_dropped": int((excl_sel == "pos").sum()),
            "retained": int(keep.sum()), "retained_by_t_det": cand[keep].t_det.value_counts().sort_index().to_dict(),
            "retained_by_ntok": cand[keep].n_tokens.value_counts().to_dict()}
    jdump(summ, RES / "s3_summary.json")
    logger.info(f"S3: {summ}")
    # recall benchmark (report only): same rule and k_t, no exclusions, on EXP5 legacy newborns
    recall_benchmark(Uk, US, kt, UNS)


def recall_benchmark(keys: np.ndarray, S: np.ndarray, kt: dict, NS: np.ndarray) -> None:
    from common5 import surf
    from nrules import STOP, TOK_OK, key_hash, key_of_tokens
    fr = pd.read_csv(EXP5 / "frame_concepts.csv", usecols=["ci", "name", "t0", "newborn"])
    f5 = pd.read_parquet(INPUTS / "features_exp5_open.parquet", columns=["ci", "logvol"])
    fr = fr.merge(f5, on="ci")
    stop = STOP()
    order = np.argsort(keys)
    ks = keys[order]
    rows = []
    for r in fr.itertuples():
        toks = surf(r.name).split()
        if not (2 <= len(toks) <= 3) or not (2003 <= r.t0 <= 2014):
            continue
        minable = all(TOK_OK.match(t) for t in toks) and toks[0] not in stop and toks[-1] not in stop
        h = np.uint64(key_hash(key_of_tokens(toks)))
        p = np.searchsorted(ks, h)
        det = -1
        if p < len(ks) and ks[p] == h:
            s = S[order[p]]
            for t in range(T_LO, T_HI + 1):
                i = t - Y0
                if s[i] >= kt[t] and s[i - 3:i].max() <= math.floor(0.25 * s[i]) and NS[order[p], i] >= MIN_SRC:
                    det = t
                    break
        rows.append({"ci": r.ci, "t0": r.t0, "logvol": r.logvol, "minable": minable, "t_det": det,
                     "newborn": bool(r.newborn),
                     "detected_by_t0p2": bool(det != -1 and det <= r.t0 + 2)})
    d = pd.DataFrame(rows)
    d["tertile"] = pd.qcut(d.logvol, 3, labels=["low", "mid", "high"])
    out = {"n_2_3_token_legacy_newborns": int(len(d)), "share_minable": float(d.minable.mean()),
           "recall_t_det_le_t0p2_all": float(d.detected_by_t0p2.mean()),
           "recall_among_minable": float(d[d.minable].detected_by_t0p2.mean()),
           "recall_by_logvol_tertile": d.groupby("tertile", observed=True).detected_by_t0p2.mean().to_dict(),
           "recall_by_logvol_tertile_minable": d[d.minable].groupby("tertile", observed=True).detected_by_t0p2.mean().to_dict(),
           "detected_ever_share": float((d.t_det != -1).mean()),
           "recall_newborn_true_subset": {"n": int(d.newborn.sum()),
                                          "recall": float(d[d.newborn].detected_by_t0p2.mean())},
           "t_det_minus_t0": (d[d.t_det != -1].t_det - d[d.t_det != -1].t0).value_counts().sort_index().to_dict(),
           "k_t": kt, "note": "report only; the rule is not changed by this benchmark unless recall < 15% (plan)"}
    jdump(out, RES / "mining_recall.json")
    logger.info(f"recall benchmark: {out}")


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all")
    ap.add_argument("--workers", type=int, default=9)
    a = ap.parse_args()
    if a.stage in ("recover", "all"):
        b = balance()
        jdump(b, RES / "sample_balance.json")
        logger.info(f"balance fail={b['fail']} overall ratio {b['overall_ratio']:.3f}; "
                    f"ratios {[round(v['ratio'], 3) for v in b['years'].values()]}; "
                    f"tvd {[round(v['tvd_field_mix'], 3) for v in b['years'].values()]}")
        keys, S, _ = load_counts()
        C3 = cand_matrix(S, {t: 3 for t in range(T_LO, T_HI + 1)})
        U = keys[C3.any(1)]
        logger.info(f"superset U (k=3) = {len(U)} keys")
        recover(U, a.workers)
    if a.stage in ("select", "all"):
        select(a.workers)


if __name__ == "__main__":
    main()
