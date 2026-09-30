"""Trimmed copy of ego.concept_core (EXP8 lib/ego.py) that computes ONLY the OPEN components and what they need:
M, first_year, new_edge_rate, NOV / NOV_res, participation, n_comm_W3, edge_persistence, ego_density_W3
(+ deg_W1/deg_W3 and the W3 neighbour list for the case-study snapshots).
Dropped: the D_z / D_sub / F nulls and betweenness / k-core / constraint (they dominate runtime and are not OPEN
components; none of the kept quantities touches the random generator). Every kept line is the EXP8 code."""
from __future__ import annotations

import warnings
from collections import Counter

import numpy as np

import ego
from ego import C, bg_window, neighbours, rq1_windows, self_topics, slice_of, window_counts

OPEN_KEYS = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]


def concept_open(name: str, aliases: list[str], t0: int, works, windows=rq1_windows, nb_min_w: int = 2,
                 keep_nb: bool = False) -> dict:
    win = windows(t0)
    early_years = sorted(set(win["W1"] + win["W2"] + win["W3"]))
    n_early, nc_early = window_counts(works, early_years)
    SELF = self_topics(name, aliases, n_early, nc_early)
    cnt, nc, bgw, NW, NB, P = {}, {}, {}, {}, {}, {}
    for w, ys in win.items():
        cnt[w], nc[w] = window_counts(works, ys)
        bgw[w], NW[w] = bg_window(ys)
    nbg_early, _ = bg_window(early_years)
    for w in ("W1", "W2", "W3"):
        NB[w], P[w] = neighbours(cnt[w], nc[w], bgw[w], NW[w], SELF, nb_min_w)
    pre_set = cnt["PRE"] >= 1
    new = (NB["W1"] | NB["W2"] | NB["W3"]) & ~pre_set
    new_idx = np.nonzero(new)[0]
    M = len(new_idx)
    first_year = {}
    for y in early_years:
        cy, _ = window_counts(works, [y])
        for k in new_idx:
            if k not in first_year and cy[k] >= 1:
                first_year[k] = y
    pool = np.nonzero((nbg_early > 0) & ~pre_set & ~SELF)[0]
    r: dict = {"M": M, "nc_W1": nc["W1"], "nc_W2": nc["W2"], "nc_W3": nc["W3"]}
    s0 = slice_of(t0)
    comm0 = C["comm"][s0]
    w1 = cnt["W1"]
    if w1.sum() > 0:
        cs = Counter()
        for k in np.nonzero(w1)[0]:
            cs[comm0[k]] += w1[k]
        C0 = cs.most_common(1)[0][0]
        if M > 0:
            r["NOV"] = float(np.mean([C["comm"][slice_of(first_year.get(k, t0))][k] != C0 for k in new_idx]))
            dg = C["deg"][s0][pool].astype(float)
            E = dg[comm0[pool] != C0].sum() / dg.sum() if dg.sum() > 0 else float("nan")
            r["NOV_res"] = r["NOV"] - E
        else:
            r["NOV"] = r["NOV_res"] = float("nan")
    else:
        r["NOV"] = r["NOV_res"] = float("nan")
    n1, n3 = NB["W1"].sum(), NB["W3"].sum()
    r["deg_W1"], r["deg_W3"] = int(n1), int(n3)
    n_years = len(early_years)
    r["new_edge_rate"] = (M / float(n_years)) / (n1 + 1)

    def jac(a, b):
        u = (a | b).sum()
        return (a & b).sum() / u if u else float("nan")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        r["edge_persistence"] = float(np.nanmean([jac(NB["W1"], NB["W2"]), jac(NB["W2"], NB["W3"])]))
    s4 = slice_of(win["W3"][-1])
    if n3 > 0:
        ws = Counter()
        for k in np.nonzero(NB["W3"])[0]:
            ws[C["comm"][s4][k]] += cnt["W3"][k]
        tot = sum(ws.values())
        pw = np.array([v / tot for v in ws.values()])
        r["participation"] = float(1 - (pw ** 2).sum())
        r["n_comm_W3"] = len(ws)
    else:
        r["participation"], r["n_comm_W3"] = float("nan"), 0
    idx = np.nonzero(NB["W3"])[0]
    if len(idx) >= 2:
        a, b = C["full_edges"][s4]
        ins = np.zeros(C["nt"], dtype=bool)
        ins[idx] = True
        e = int((ins[a] & ins[b]).sum())
        r["ego_density_W3"] = e / (len(idx) * (len(idx) - 1) / 2)
    else:
        r["ego_density_W3"] = float("nan")
    if keep_nb:
        r["_nb"] = {w: np.nonzero(NB[w])[0].tolist() for w in ("W1", "W2", "W3")}
        r["_cnt"] = {w: cnt[w] for w in ("W1", "W2", "W3")}
        r["_pmi"] = {w: P[w] for w in ("W1", "W2", "W3")}
        r["_pre"] = np.nonzero(pre_set)[0].tolist()
    return r


def set_context(ctx: dict) -> None:
    ego.set_context(ctx)
