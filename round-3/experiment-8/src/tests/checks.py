#!/usr/bin/env python3
"""T2 (check A1, A2) and T3 (Pass B sanity) on the FULL passes. Writes results/checks.json (merged).

A1 STOP rule: per frame concept, Spearman over years 2000-2016 of Pass A grounded counts vs EXP5 agg_counts
   (tagstate 1): median >= 0.99, and recomputed early_volume (t0..t0+2) == frame.early_volume for >= 99%.
A2: Pass A background BG[year, topic] vs EXP3 scan/ckpt.npz bg for the years both cover: Spearman >= 0.999.
T3: share of cited early works; citing year >= cited year for > 99.5% of links."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from common import DATA, EXP3, EXP5, MATCH_Y0, MATCH_Y1, RES, jdump, load_frame, read_parquet_parts


def a1() -> dict:
    fr = load_frame()
    cc = pd.read_parquet(DATA / "counts_check.parquet").groupby(["ci", "year"]).n.sum()
    ag = pd.read_parquet(EXP5 / "scan/agg_counts.parquet", columns=["ci", "year", "tagstate", "n"])
    ag = ag[(ag.tagstate == 1) & ag.ci.isin(fr.ci) & (ag.year >= MATCH_Y0) & (ag.year <= MATCH_Y1)]
    e5 = ag.groupby(["ci", "year"]).n.sum()
    years = np.arange(MATCH_Y0, MATCH_Y1 + 1)
    idx = pd.MultiIndex.from_product([fr.ci.to_numpy(), years], names=["ci", "year"])
    A = cc.reindex(idx, fill_value=0).to_numpy().reshape(len(fr), len(years))
    B = e5.reindex(idx, fill_value=0).to_numpy().reshape(len(fr), len(years))
    rhos = []
    for i in range(len(fr)):
        if A[i].std() == 0 or B[i].std() == 0:
            rhos.append(1.0 if np.array_equal(A[i], B[i]) else 0.0)
        else:
            rhos.append(spearmanr(A[i], B[i])[0])
    rhos = np.array(rhos)
    t0 = fr.t0.to_numpy()
    ev = np.array([A[i, t0[i] - MATCH_Y0:t0[i] - MATCH_Y0 + 3].sum() for i in range(len(fr))])
    ev_ok = np.isclose(ev, fr.early_volume.to_numpy())
    return {"n_concepts": len(fr), "median_spearman": float(np.median(rhos)), "p05_spearman": float(np.percentile(rhos, 5)),
            "share_identical_yearly_vectors": float(np.mean(np.all(A == B, axis=1))),
            "share_early_volume_equal": float(ev_ok.mean()), "total_passA": int(A.sum()), "total_exp5": int(B.sum()),
            "pass": bool(np.median(rhos) >= 0.99 and ev_ok.mean() >= 0.99)}


def a2() -> dict:
    z = np.load(DATA / "bg_topics.npz")
    ck = np.load(EXP3 / "scan/ckpt.npz")
    bg3 = ck["bg"]
    ny = min(bg3.shape[0], z["BG"].shape[0])
    rows = bg3[:ny].sum(1) > 0
    a = z["BG"][:ny][rows].ravel()
    b = bg3[:ny][rows].ravel()
    per_year = [float(spearmanr(z["BG"][y], bg3[y])[0]) for y in range(ny) if bg3[y].sum() > 0]
    return {"years_compared": int(rows.sum()), "spearman_all_cells": float(spearmanr(a, b)[0]),
            "median_per_year_spearman": float(np.median(per_year)), "ratio_total_passA_over_exp3": float(a.sum() / b.sum()),
            "pass": bool(spearmanr(a, b)[0] >= 0.999)}


def t3() -> dict:
    fr = load_frame()[["ci", "t0"]]
    ce = pd.read_parquet(DATA / "cites_early.parquet")
    em = read_parquet_parts(DATA / "frame_matches_early", columns=["ci", "year", "work_id"]).merge(fr, on="ci")
    em = em[(em.year >= em.t0) & (em.year <= em.t0 + 2)]
    pubyear = em.drop_duplicates("work_id").set_index("work_id").year
    j = ce[ce.work_id.isin(pubyear.index)].copy()
    j["pub"] = j.work_id.map(pubyear)
    ok = (j.citing_year >= j.pub)
    return {"early_works": int(em.work_id.nunique()), "early_works_cited": int(j.work_id.nunique()),
            "share_cited": float(j.work_id.nunique() / max(em.work_id.nunique(), 1)),
            "links": int(j.n.sum()), "share_links_citing_ge_cited_year": float((j.n * ok).sum() / j.n.sum()),
            "pass": bool((j.n * ok).sum() / j.n.sum() > 0.995)}


def main() -> None:
    p = RES / "checks.json"
    out = json.loads(p.read_text()) if p.exists() else {}
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "A"):
        out["A1_reproduction"] = a1()
        out["A2_background"] = a2()
    if which in ("all", "B"):
        out["T3_passB"] = t3()
    jdump(out, p)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
