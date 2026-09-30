"""Rescue (citation provenance into off-home episodes, background-adjusted; Hanski connectivity) and relay
(episode j seeding later field entries beyond an availability null). Work-level data from pass 2."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from config import P2, SEED


def load_works(cidx: set[int], p_notag: dict[int, float]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """grounded (work, concept) rows for the given concepts + the works table (refs, authors)."""
    H, W = [], []
    for hp in sorted(P2.glob("h*.parquet")):
        h = pq.read_table(hp, columns=["work_id", "cidx", "tag", "year", "vf"]).to_pandas()
        h = h[h.cidx.isin(cidx)]
        keep = (h.tag == 1) | ((h.tag == -1) & (h.cidx.map(p_notag).fillna(1.0) >= 0.5))
        h = h[keep]
        if h.empty:
            continue
        w = pq.read_table(P2 / ("w" + hp.name[1:]), columns=["work_id", "year", "vf", "refs", "authors"]).to_pandas()
        w = w[w.work_id.isin(h.work_id)]
        H.append(h); W.append(w)
    H = pd.concat(H, ignore_index=True).drop_duplicates(["work_id", "cidx"])
    W = pd.concat(W, ignore_index=True).drop_duplicates("work_id").set_index("work_id")
    return H, W


def lookup_fields(ids: np.ndarray) -> dict[int, int]:
    """venue field of arbitrary work ids via the global id map (scan/pass2/m*.npz, each sorted by id)."""
    ids = np.unique(ids.astype(np.int64))
    out = {}
    for mp in sorted(P2.glob("m*.npz")):
        z = np.load(mp)
        mid = z["id"]
        if not len(mid):
            continue
        p = np.clip(np.searchsorted(mid, ids), 0, len(mid) - 1)
        hit = mid[p] == ids
        for i, v in zip(ids[hit], z["vf"][p[hit]]):
            out[int(i)] = int(v)
    return out


def classify(vf: int, home: set[int], j: int) -> str | None:
    if vf is None or vf < 11:
        return None
    if vf in home:
        return "HOME"
    return "SELF" if vf == j else "OTHER"


def rescue_table(frame: pd.DataFrame, eps: pd.DataFrame, H: pd.DataFrame, W: pd.DataFrame, G: dict, phi: np.ndarray,
                 n_bg: int = 10) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    REFS, AUTH, YEAR = W["refs"].to_dict(), W["authors"].to_dict(), W["year"].to_dict()
    fr = frame.set_index("cidx")
    Hc = {c: d for c, d in H.groupby("cidx")}
    # pass A: collect citing papers and background samples
    recs, bg_need = [], []
    for e in eps.itertuples():
        c, j = int(e.cidx), int(e.field)
        f = fr.loc[c]; t0 = int(f.t0)
        if e.entry_year > t0 + 2 or c not in Hc:
            continue
        home = {int(h) for h in str(f.home).split("|")}
        hc = Hc[c]
        cyear = dict(zip(hc.work_id, hc.year)); cvf = dict(zip(hc.work_id, hc.vf))
        cset = set(cyear)
        P = hc[(hc.vf == j) & hc.year.between(t0 + 3, t0 + 5)].work_id.tolist()
        cnt = {"HOME": 0, "SELF": 0, "OTHER": 0, "self_lineage": 0, "n_citing": 0, "n_cref": 0}
        bg_ids = []
        for p in P:
            if p not in REFS:
                continue
            refs = REFS[p]; au = set(AUTH[p]) - {0}
            yp = int(YEAR[p])
            refs = np.asarray(refs if refs is not None else [], np.int64)
            cnt["n_citing"] += 1
            cref = [r for r in refs if r in cset and yp - 5 <= cyear[r] <= yp]
            for r in cref:
                cnt["n_cref"] += 1
                ra = set(AUTH[r]) - {0} if r in AUTH else set()
                if au & ra:
                    cnt["self_lineage"] += 1
                    continue
                k = classify(int(cvf[r]), home, j)
                if k:
                    cnt[k] += 1
            other = [r for r in refs if r not in cset]
            if other:
                bg_ids.extend(rng.choice(other, min(n_bg, len(other)), replace=False).tolist())
        occ = [k for k in range(11, 37) if k not in home and k != j
               and G[c][t0 - 1995:t0 - 1995 + 3, k - 10].sum() >= 2]
        S = sum(phi[j - 11, k - 11] * math.log1p(G[c][t0 - 1995:t0 - 1995 + 3, k - 10].sum()) for k in occ)
        recs.append({"cidx": c, "field": j, "home": home, "S_hanski": S, **cnt, "_bg": bg_ids})
        bg_need.extend(bg_ids)
    fmap = lookup_fields(np.asarray(bg_need, np.int64)) if bg_need else {}
    rows = []
    for r in recs:
        b = {"HOME": 0, "SELF": 0, "OTHER": 0}
        for i in r.pop("_bg"):
            k = classify(fmap.get(int(i), -1), r["home"], r["field"])
            if k:
                b[k] += 1
        r.pop("home")
        r.update({"bg_HOME": b["HOME"], "bg_SELF": b["SELF"], "bg_OTHER": b["OTHER"]})
        ho = r["HOME"] + r["OTHER"]
        r["s_other"] = r["OTHER"] / ho if ho else np.nan
        tot = r["HOME"] + r["OTHER"] + r["SELF"]
        r["s_self"] = r["SELF"] / tot if tot else np.nan
        r["resc"] = (math.log((r["OTHER"] + .5) / (r["HOME"] + .5)) - math.log((b["OTHER"] + .5) / (b["HOME"] + .5))
                     if tot > 0 and sum(b.values()) > 0 else np.nan)
        rows.append(r)
    return pd.DataFrame(rows)


def relay_table(frame: pd.DataFrame, eps: pd.DataFrame, H: pd.DataFrame, W: pd.DataFrame) -> pd.DataFrame:
    REFS, AUTH = W["refs"].to_dict(), W["authors"].to_dict()
    fr = frame.set_index("cidx")
    Hc = {c: d for c, d in H.groupby("cidx")}
    out = []
    for c, ec in eps.groupby("cidx"):
        if c not in Hc:
            continue
        f = fr.loc[c]; t0 = int(f.t0)
        home = {int(h) for h in str(f.home).split("|")}
        hc = Hc[c].sort_values(["year", "work_id"])
        cyear = dict(zip(hc.work_id, hc.year)); cvf = dict(zip(hc.work_id, hc.vf))
        # entry year of every off-home field (cumulative grounded >= 2 is approximated by the 2nd grounded work)
        ent = {}
        for k, d in hc[hc.vf >= 11].groupby("vf"):
            if len(d) >= 2 and int(k) not in home:
                ent[int(k)] = int(d.year.iloc[1])
        first5 = {k: hc[hc.vf == k].work_id.head(5).tolist() for k in ent}
        for e in ec.itertuples():
            j, ej = int(e.field), int(e.entry_year)
            hit_sum, E, nk = 0, 0.0, 0
            for k, ek in ent.items():
                if k == j or not (ej + 1 <= ek <= min(ej + 5, t0 + 8)):
                    continue
                nk += 1
                before = hc[hc.year < ek]
                a = float((before.vf == j).mean()) if len(before) else 0.0
                m, hit = 0, 0
                for p in first5[k]:
                    if p not in REFS:
                        continue
                    au = set(AUTH[p]) - {0}
                    refs = REFS[p]
                    for r in (refs if refs is not None else []):
                        if r in cyear and cyear[r] < ek:
                            ra = set(AUTH[r]) - {0} if r in AUTH else set()
                            if au & ra:
                                continue
                            m += 1
                            if int(cvf[r]) == j:
                                hit = 1
                hit_sum += hit
                E += 1 - (1 - a) ** m
            out.append({"cidx": int(c), "field": j, "n_later_fields": nk, "relay": hit_sum, "E_avail": E,
                        "relay_excess": hit_sum - E})
    return pd.DataFrame(out)
