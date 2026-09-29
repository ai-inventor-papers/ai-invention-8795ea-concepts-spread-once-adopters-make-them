#!/usr/bin/env python3
"""Step 6 (EXPLORATORY; the static outcomes were already unsealed by EXP8): why does the early new_edge_rate /
n_comm_W3 signal work?  Partner-source decomposition of the EXP8 static new-partner set (t0..t0+2, ALL papers,
recomputed through lib/ego_yearly and verified equal to EXP8 to 0 difference), plus a bridging-paper profile.

Partner classes: type METHOD | DOMAIN (LLM-typed topics), partner field home | off-home (topic field vs home list),
community new | old (comm of the partner in the slice of its first year vs the concept's first-year modal community),
carrier home | off-home venue (venue fields of the concept papers of the partner's first year).
Class-restricted indicators: new_edge_rate_X = (|NEW & X| / 3) / (n1 + 1); n_comm_W3_X = # communities among W3
neighbours in class X (type and partner-field classes).
Score: partial Spearman (EXP8 rq1stats.psp_boot, identical code) with O2r_m50 and O2r_resid given B5 + t0 dummies
(+ group dummies in COHORT), 2,000 concept bootstraps; per body and per held-out group, DL pooled over the 4 held-out
groups with I2; paired bootstrap differences METHOD-DOMAIN, comm_new-comm_old, carrier home-off-home.
Writes results/partner_decomposition.json, data/partner_indicators.parquet, data/bridging_papers.parquet."""
from __future__ import annotations

import json
import multiprocessing as mp
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, DATA_IN, INPUTS, RES, RES_IN, RUN_ROOT, jdump, load_frame, read_parquet_parts, setup_logger

EXP8 = RUN_ROOT / "3_invention_loop/iter_3/gen_art/gen_art_experiment_8"
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
OUTS = ["O2r_m50", "O2r_resid"]
HELD = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]
SEED = 20260929
N_BOOT = 2000


def home_codes(h) -> set[int]:
    return {int(float(x)) for x in re.split(r"[|;]", str(h)) if x and x != "nan"}


def build_indicators(logger) -> tuple[pd.DataFrame, pd.DataFrame]:
    fr = load_frame()
    tt = pd.read_csv(RES_IN / "topic_types.csv").set_index("topic_idx")
    tids = json.loads((INPUTS / "topic_ids.json").read_text())
    tm = pd.read_csv(INPUTS / "topic_meta.csv").set_index("topic").loc[tids]
    tfield = tm.field.to_numpy(int)
    ttype = tt.loc[np.arange(len(tids)), "class"].to_numpy()
    prt = pd.read_parquet(DATA_IN / "static_partners.parquet")
    port = pd.read_parquet(DATA_IN / "port_static.parquet")
    w3 = json.loads((DATA_IN / "w3_comms.json").read_text())
    L = read_parquet_parts(DATA_IN / "frame_matches_long", columns=["ci", "year", "work_id", "vfield", "doc_type",
                                                                 "topics", "authors"])
    L = L.merge(fr[["ci", "t0"]], on="ci")
    hom = {r.ci: home_codes(r.home) for r in fr.itertuples()}
    early = L[(L.year >= L.t0) & (L.year <= L.t0 + 2)]
    # carrier: venue fields of the concept papers of the partner's first year that contain the partner
    ex = early[["ci", "year", "work_id", "vfield", "topics"]].explode("topics").dropna(subset=["topics"])
    ex["topics"] = ex.topics.astype(int)
    car = prt.merge(ex.rename(columns={"topics": "topic", "year": "first_year"}), on=["ci", "topic", "first_year"],
                    how="left")
    car["vhome"] = [(v - 0 + 10) in hom[c] if v > 0 else np.nan for c, v in zip(car.ci, car.vfield.fillna(0).astype(int))]

    def carrier(s: pd.Series) -> str:
        v = s.dropna()
        if len(v) == 0:
            return "unlabelled"
        return "home" if v.all() else ("offhome" if (~v.astype(bool)).all() else "mixed")
    cm = car.groupby(["ci", "topic"]).vhome.agg(carrier).rename("carrier").reset_index()
    prt = prt.merge(cm, on=["ci", "topic"], how="left")
    prt["type"] = ttype[prt.topic.to_numpy()]
    prt["pfield_home"] = [tfield[k] in hom[c] for c, k in zip(prt.ci, prt.topic)]
    n1 = port.set_index("ci").n1_static
    classes = {"METHOD": prt.type == "METHOD", "DOMAIN": prt.type == "DOMAIN", "pfield_home": prt.pfield_home,
               "pfield_offhome": ~prt.pfield_home, "comm_new": prt.comm_new == 1, "comm_old": prt.comm_new == 0,
               "carrier_home": prt.carrier == "home", "carrier_offhome": prt.carrier == "offhome"}
    ind = pd.DataFrame({"ci": fr.ci})
    for nm, m in classes.items():
        cnt = prt[m].groupby("ci").size()
        ind[f"ner_{nm}"] = (ind.ci.map(cnt).fillna(0) / 3.0) / (ind.ci.map(n1) + 1)
    ind["ner_all"] = (ind.ci.map(prt.groupby("ci").size()).fillna(0) / 3.0) / (ind.ci.map(n1) + 1)
    # n_comm_W3 by class for type / partner field
    for nm, fn in {"METHOD": lambda k, c: ttype[k] == "METHOD", "DOMAIN": lambda k, c: ttype[k] == "DOMAIN",
                   "pfield_home": lambda k, c: tfield[k] in hom[c], "pfield_offhome": lambda k, c: tfield[k] not in hom[c]}.items():
        vals = {}
        for c in fr.ci:
            dct = w3.get(str(c))
            if dct is None:
                vals[c] = np.nan
                continue
            vals[c] = len({cm_ for k, cm_ in dct.items() if fn(int(k), c)})
        ind[f"ncw3_{nm}"] = ind.ci.map(vals)
    ind.loc[ind.ci.map(n1).isna(), [c for c in ind.columns if c != "ci"]] = np.nan
    # ---------------- bridging papers: early papers that introduce >= 1 new partner from a new community
    newc = prt[prt.comm_new == 1][["ci", "topic", "first_year"]]
    ep = early.copy()
    first_auth = {}
    L_sorted = L.sort_values(["ci", "year"])
    seen_auth = L_sorted.explode("authors").dropna(subset=["authors"]).groupby(["ci", "authors"]).year.min()
    ep = ep.reset_index(drop=True)
    ex2 = ep[["ci", "year", "work_id", "topics"]].explode("topics").dropna(subset=["topics"])
    ex2["topics"] = ex2.topics.astype(int)
    br = ex2.merge(newc.rename(columns={"topic": "topics", "first_year": "year"}), on=["ci", "year", "topics"])
    bw = set(zip(br.ci, br.work_id))
    ep["bridging"] = [(c, w) in bw for c, w in zip(ep.ci, ep.work_id)]
    ep["team_size"] = ep.authors.map(len)
    fa = seen_auth.to_dict()
    ep["share_new_authors"] = [np.mean([fa.get((c, a), y) >= y for a in au]) if len(au) else np.nan
                               for c, y, au in zip(ep.ci, ep.year, ep.authors)]
    ep["home_venue"] = [(v + 10) in hom[c] if v > 0 else np.nan for c, v in zip(ep.ci, ep.vfield)]
    bp = ep[["ci", "year", "work_id", "vfield", "doc_type", "bridging", "team_size", "share_new_authors", "home_venue"]]
    bp.to_parquet(DATA / "bridging_papers.parquet", index=False)
    ind["bridging_share"] = ind.ci.map(bp.groupby("ci").bridging.mean())
    logger.info(f"partner indicators {ind.shape}; bridging papers {int(bp.bridging.sum())}/{len(bp)}")
    prt.to_parquet(DATA / "static_partners_typed.parquet", index=False)
    return ind, bp


def _cat(d: pd.DataFrame, pooled_groups: bool) -> np.ndarray:
    from rq1stats import dummies
    parts = [dummies(d.t0.to_numpy())]
    if pooled_groups:
        parts.append(dummies(d.group.to_numpy()))
    return np.hstack(parts)


def score_unit(args) -> dict:
    """psp for all indicators and outcomes in one unit, with paired bootstrap differences."""
    from rq1stats import psp_point
    unit, d, cols, pooled_groups, n_boot = args
    out = {}
    cat = _cat(d, pooled_groups)
    Bm = d[B5].to_numpy(float)
    rng = np.random.default_rng(SEED + hash(unit) % 1000)
    for o in OUTS:
        y = d[o].to_numpy(float)
        ok = np.isfinite(y) & np.isfinite(Bm).all(1)
        X = {c: d[c].to_numpy(float) for c in cols}
        n = int(ok.sum())
        pts = {c: psp_point(X[c][ok & np.isfinite(X[c])], y[ok & np.isfinite(X[c])], Bm[ok & np.isfinite(X[c])],
                            cat[ok & np.isfinite(X[c])]) for c in cols}
        idx = np.nonzero(ok)[0]
        bs = {c: [] for c in cols}
        for _ in range(n_boot):
            i = idx[rng.integers(0, len(idx), len(idx))]
            for c in cols:
                j = i[np.isfinite(X[c][i])]
                bs[c].append(psp_point(X[c][j], y[j], Bm[j], cat[j]) if len(j) > 30 else np.nan)
        res = {}
        for c in cols:
            v = np.array(bs[c], float); v = v[np.isfinite(v)]
            z = np.arctanh(np.clip(v, -0.999999, 0.999999))
            res[c] = {"rho": pts[c], "ci": [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if len(v) else None,
                      "z": float(np.arctanh(np.clip(pts[c], -0.999999, 0.999999))) if np.isfinite(pts[c]) else np.nan,
                      "se_z": float(np.std(z, ddof=1)) if len(z) > 2 else np.nan}
        for a, b in (("ner_METHOD", "ner_DOMAIN"), ("ner_comm_new", "ner_comm_old"),
                     ("ner_carrier_home", "ner_carrier_offhome"), ("ncw3_METHOD", "ncw3_DOMAIN"),
                     ("ner_pfield_offhome", "ner_pfield_home")):
            if a in cols and b in cols:
                dv = np.array(bs[a], float) - np.array(bs[b], float)
                dv = dv[np.isfinite(dv)]
                res[f"diff_{a}_minus_{b}"] = {"diff": pts[a] - pts[b], "ci": [float(np.percentile(dv, 2.5)),
                                                                           float(np.percentile(dv, 97.5))] if len(dv) else None,
                                              "se": float(np.std(dv, ddof=1)) if len(dv) > 2 else np.nan}
        out[o] = {"n": n, "res": res}
    return {"unit": unit, **out}


def main() -> None:
    logger = setup_logger("partners")
    t = time.time()
    ind, bp = build_indicators(logger)
    A = pd.read_parquet(EXP8 / "data" / "analysis_table.parquet", columns=["ci", "t0", "group", "split", "unit",
                                                                           "new_edge_rate", "n_comm_W3"] + B5 + OUTS)
    D = A.merge(ind, on="ci", how="left")
    D.to_parquet(DATA / "partner_indicators.parquet", index=False)
    chk = float(np.nanmax(np.abs(D.ner_all - D.new_edge_rate)))
    cols = [c for c in ind.columns if c != "ci"] + ["new_edge_rate"]
    D["body"] = np.where(D.split == "DEV", "DEV", np.where(D.split == "COHORT", "COHORT", "OLD_HELDOUT"))
    jobs = [("DEV", D[D.body == "DEV"], cols, True, N_BOOT),
            ("OLD_HELDOUT", D[D.body == "OLD_HELDOUT"], cols, True, N_BOOT),
            ("COHORT", D[D.body == "COHORT"], cols, True, N_BOOT)]
    jobs += [(g, D[D.unit == g], cols, False, N_BOOT) for g in HELD]
    with ProcessPoolExecutor(max_workers=len(jobs), mp_context=mp.get_context("spawn")) as ex:
        R = {r["unit"]: r for r in ex.map(score_unit, jobs)}
    from rq1stats import dersimonian_laird
    pooled = {}
    for o in OUTS:
        pooled[o] = {}
        for c in cols:
            zs = [R[g][o]["res"][c]["z"] for g in HELD]
            ses = [R[g][o]["res"][c]["se_z"] for g in HELD]
            pl = dersimonian_laird(np.array(zs, float), np.array(ses, float))
            pooled[o][c] = {"psp": float(np.tanh(pl["b"])) if np.isfinite(pl["b"]) else None,
                            "ci": [float(np.tanh(pl["ci"][0])), float(np.tanh(pl["ci"][1]))] if np.isfinite(pl["b"]) else None,
                            "I2": pl["I2"], "k": pl["k"]}
        for key in [k for k in R["PHYS"][o]["res"] if k.startswith("diff_")]:
            bs = [R[g][o]["res"][key]["diff"] for g in HELD]
            ses = [R[g][o]["res"][key]["se"] for g in HELD]
            pooled[o][key] = dersimonian_laird(np.array(bs, float), np.array(ses, float))
    bprof = {}
    for b, d in bp.merge(D[["ci", "body"]], on="ci").groupby("body"):
        bprof[b] = {k: {"bridging": float(d.loc[d.bridging, v].median() if k == "median_team_size" else d.loc[d.bridging, v].mean()),
                        "other": float(d.loc[~d.bridging, v].median() if k == "median_team_size" else d.loc[~d.bridging, v].mean())}
                    for k, v in (("median_team_size", "team_size"), ("share_new_authors", "share_new_authors"),
                                 ("review_share", "doc_type"), ("home_venue_share", "home_venue"))}
        bprof[b]["n_bridging"] = int(d.bridging.sum()); bprof[b]["n_papers"] = int(len(d))
    out = {"check_ner_all_equals_EXP8_new_edge_rate_max_abs": chk, "units": R, "pooled_heldout_DL": pooled,
           "bridging_profile": bprof, "n_boot": N_BOOT,
           "topic_types": json.loads((RES_IN / "topic_type_benchmark.json").read_text()),
           "seconds": time.time() - t}
    jdump(out, RES / "partner_decomposition.json")
    logger.info(f"partner decomposition done in {(time.time()-t)/60:.1f} min; ner_all check {chk}")


if __name__ == "__main__":
    main()
