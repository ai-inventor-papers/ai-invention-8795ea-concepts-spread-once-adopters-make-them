#!/usr/bin/env python3
"""iter-5 STEP 7 (Part A scoring, EXPLORATORY / selection data): which partner classes carry the HOME signal?

For every component c (totals, class parts, class-specific-null novelty, joint type x community parts, NOVCHURN_home,
OPEN_home, bridging share) and outcome o: psp(c, o | B5 + t0 dummies [+ group + body dummies when pooled]) with 2,000
concept bootstraps sharing their resample indices across components (lib_iter5/partA_stats.Scorer reproduces EXP8
rq1stats.psp_point exactly). Bodies: DEV, OLD_HELDOUT (+ PHYS/LIFEENV/SOC/MATHDEC -> DL on Fisher z with I2),
COHORT_2010_14, POOLED_EXP5, and the 2015-17 cohort at Exp10 rungs R0 and R3.
Shapley games (exact) on the psp of NOVCHURN_home (type / deg / carrier / direction) and of new_edge_rate and churn
(type x community, 4 players); Holm over the 5 pre-declared contrasts on POOLED_EXP5 / O2r_m50; class-label placebos
(200 draws); bridging papers. Refuses to join outcomes unless seal_iter5.check() passes.
Writes results/partner_classes.json, partner_shapley.json, bridging_papers_summary.json, figures/partner_forest.png,
figures/shapley_bars.png, data/partA_features_{exp5,cohort}.parquet.
Usage: python score_partA.py [--n-boot N] [--n-placebo N] [--workers 4] [--limit N]"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib_iter5"))

import numpy as np
import pandas as pd

from common_iter5 import B5, DATA, E8, E10, E11, FIGS, HELD, RES, SEED, add_deviation, jdump, read_parts, setup_logger

warnings.filterwarnings("ignore")
AXES = {"type": ["METHOD", "DOMAIN", "OTHER"], "comm": ["new", "old", "unk"], "deg": ["low", "high"],
        "carrier": ["mixed", "pure"]}
NOV_AXES = ["type", "deg", "carrier"]
PAIRS = {"type": ("METHOD", "DOMAIN"), "comm": ("new", "old"), "deg": ("low", "high"), "carrier": ("mixed", "pure")}
TC = [("METHOD", "new"), ("METHOD", "old"), ("DOMAIN", "new"), ("DOMAIN", "old")]
HOLM = {"C1_METHOD_minus_DOMAIN_novnull": ("novnull_type_METHOD", "novnull_type_DOMAIN"),
        "C2_commnew_minus_commold_ner": ("ner_comm_new", "ner_comm_old"),
        "C3_lowdeg_minus_highdeg_nov": ("nov_deg_low", "nov_deg_high"),
        "C4_mixed_minus_pure_ner": ("ner_carrier_mixed", "ner_carrier_pure"),
        "C5_dropped_minus_added_churn": ("chd_all", "cha_all")}


# ----------------------------------------------------------------------------- features
def novchurn(nov: np.ndarray, ep: np.ndarray, n_home: np.ndarray, k: dict) -> np.ndarray:
    a, b = k["NOV_res"], k["edge_persistence"]
    zn = a["sign"] * (np.clip(nov, a["lo"], a["hi"]) - a["mu"]) / a["sd"]
    ze = b["sign"] * (np.clip(ep, b["lo"], b["hi"]) - b["mu"]) / b["sd"]
    out = (zn + ze) / 2
    out[~(np.isfinite(zn) & np.isfinite(ze)) | (n_home < 10)] = np.nan
    return out


def joint_parts(rows: pd.DataFrame, cis: np.ndarray) -> pd.DataFrame:
    out = pd.DataFrame({"ci": cis})
    for (t, c) in TC:
        m = (rows.type == t) & (rows.comm == c)
        out[f"jner_{t}_{c}"] = out.ci.map(rows[m & (rows.role == "new")].groupby("ci").w_ner.sum()).fillna(0.0)
        out[f"jch_{t}_{c}"] = out.ci.map(rows[m & (rows.role != "new")].groupby("ci").w_ch.sum()).fillna(0.0)
    return out


def build_features(comp: pd.DataFrame, rows: pd.DataFrame, k: dict) -> tuple[pd.DataFrame, dict]:
    F = comp.copy()
    for ax, cl in AXES.items():
        for X in cl:
            F[f"ch_{ax}_{X}"] = F[f"chd_{ax}_{X}"] + F[f"cha_{ax}_{X}"]
    F = F.merge(joint_parts(rows, F.ci.to_numpy()), on="ci", how="left")
    undefined_churn = ~np.isfinite(F.churn)
    for c in [c for c in F.columns if c.startswith("jch_")]:
        F.loc[undefined_churn, c] = np.nan
    F["jch_rest"] = F.churn - F[[f"jch_{t}_{c}" for t, c in TC]].sum(1)
    F["jner_rest"] = F.new_edge_rate - F[[f"jner_{t}_{c}" for t, c in TC]].sum(1)
    F["NOVCHURN_home"] = novchurn(F.NOV_res.to_numpy(float), F.edge_persistence.to_numpy(float),
                                  F.n_home_early.to_numpy(float), k)
    # exact identities (T0 b) on every concept
    ident = {}
    for ax in NOV_AXES:
        ident[f"NOV_res=sum nov_{ax}"] = float(np.nanmax(np.abs(F[[f"nov_{ax}_{X}" for X in AXES[ax]]].sum(1, min_count=1) - F.NOV_res)))
    for ax in AXES:
        ident[f"ner=sum ner_{ax}"] = float(np.nanmax(np.abs(F[[f"ner_{ax}_{X}" for X in AXES[ax]]].sum(1) - F.new_edge_rate)))
        ident[f"churn=sum ch_{ax}"] = float(np.nanmax(np.abs(F[[f"ch_{ax}_{X}" for X in AXES[ax]]].sum(1, min_count=1) - F.churn)))
    ident["churn=chd_all+cha_all"] = float(np.nanmax(np.abs(F.chd_all + F.cha_all - F.churn)))
    ident["jner_rest_min"] = float(np.nanmin(F.jner_rest))
    ident["jch_rest_min"] = float(np.nanmin(F.jch_rest))
    return F, ident


def component_columns(F: pd.DataFrame) -> list[str]:
    cols = ["NOV_res", "new_edge_rate", "churn", "edge_persistence", "NOVCHURN_home", "OPEN_home",
            "bridging_share_home", "chd_all", "cha_all", "M", "n1"]
    for ax, cl in AXES.items():
        for X in cl:
            if F[f"m_{ax}_{X}"].sum() == 0:
                continue
            cols += [f"ner_{ax}_{X}", f"ch_{ax}_{X}", f"chd_{ax}_{X}", f"cha_{ax}_{X}"]
            if ax in NOV_AXES:
                cols += [f"nov_{ax}_{X}", f"novnull_{ax}_{X}"]
    cols += [f"jner_{t}_{c}" for t, c in TC] + [f"jch_{t}_{c}" for t, c in TC]
    if "new_edge_rate_ALL" in F:
        cols.append("new_edge_rate_ALL")
    return [c for c in cols if c in F.columns]


# ----------------------------------------------------------------------------- Shapley games
def games(F: pd.DataFrame, k: dict) -> dict:
    """{game: (players, target_fn(S) -> column values, fair share dict)} built on the body's rows."""
    from partA_stats import subsets
    G = {}
    nh = F.n_home_early.to_numpy(float)
    ok_nc = np.isfinite(F.NOVCHURN_home.to_numpy(float))
    for ax in NOV_AXES:
        pl = [X for X in AXES[ax] if F[f"m_{ax}_{X}"].sum() > 0]
        nov = {X: F[f"nov_{ax}_{X}"].to_numpy(float) for X in pl}
        ch = {X: F[f"ch_{ax}_{X}"].to_numpy(float) for X in pl}
        mn = {X: np.nanmean(nov[X][ok_nc]) for X in pl}
        mc = {X: np.nanmean(ch[X][ok_nc]) for X in pl}
        cols = {}
        for S in subsets(pl):
            nv = sum(nov[X] if X in S else mn[X] for X in pl)
            cv = sum(ch[X] if X in S else mc[X] for X in pl)
            t = novchurn(np.asarray(nv, float) + 0 * F.NOV_res.to_numpy(float), 1 - np.asarray(cv, float), nh, k)
            t[~ok_nc] = np.nan
            cols[S] = t
        M = F.M.to_numpy(float)
        share_new = {X: float(F.loc[ok_nc, f"m_{ax}_{X}"].sum() / max(M[ok_nc].sum(), 1)) for X in pl}
        share_ch = {X: float(np.nanmean(ch[X][ok_nc]) / np.nanmean(F.churn.to_numpy(float)[ok_nc])) for X in pl}
        G[f"NOVCHURN_{ax}"] = (pl, cols, {"new_partner_share": share_new, "churn_mass_share": share_ch})
    # direction game
    parts = {"NOV": F.NOV_res.to_numpy(float), "DROP": F.chd_all.to_numpy(float), "ADD": F.cha_all.to_numpy(float)}
    mp_ = {p: np.nanmean(v[ok_nc]) for p, v in parts.items()}
    cols = {}
    for S in subsets(list(parts)):
        nv = parts["NOV"] if "NOV" in S else mp_["NOV"] + 0 * parts["NOV"]
        cv = sum(parts[p] if p in S else mp_[p] for p in ("DROP", "ADD"))
        t = novchurn(np.asarray(nv, float), 1 - np.asarray(cv, float), nh, k)
        t[~ok_nc] = np.nan
        cols[S] = t
    tot = np.nanmean(F.churn.to_numpy(float)[ok_nc])
    G["NOVCHURN_direction"] = (list(parts), cols, {"churn_mass_share": {
        "DROP": float(np.nanmean(parts["DROP"][ok_nc]) / tot), "ADD": float(np.nanmean(parts["ADD"][ok_nc]) / tot)}})
    # type x community games on new_edge_rate and churn
    for nm, pre, rest in (("ner_type_x_comm", "jner", "jner_rest"), ("churn_type_x_comm", "jch", "jch_rest")):
        pl = [f"{t}_{c}" for t, c in TC]
        v = {p: F[f"{pre}_{p}"].to_numpy(float) for p in pl}
        rv = F[rest].to_numpy(float)
        ok = np.isfinite(rv)
        mv = {p: np.nanmean(v[p][ok]) for p in pl}
        cols = {}
        for S in subsets(pl):
            t = rv + sum(v[p] if p in S else mv[p] for p in pl)
            t = np.asarray(t, float)
            t[~ok] = np.nan
            cols[S] = t
        share = {p: float(np.nanmean(v[p][ok]) / np.nanmean((rv + sum(v.values()))[ok])) for p in pl}
        G[nm] = (pl, cols, {"mass_share": share})
    return G


# ----------------------------------------------------------------------------- one body x outcome
def design(d: pd.DataFrame, body: str, rung: str | None) -> tuple[np.ndarray, np.ndarray]:
    from rq1stats import dummies
    if rung is not None:
        from ladder import rung_design
        Bc, Cc = rung_design(d, rung)
        return Bc.to_numpy(float), Cc.to_numpy(float)
    parts = [dummies(d.t0.to_numpy())]
    if body in ("DEV", "OLD_HELDOUT", "COHORT_2010_14", "POOLED_EXP5"):
        parts.append(dummies(d.group.to_numpy()))
    if body == "POOLED_EXP5":
        parts.append(dummies(d.body.to_numpy()))
    return d[B5].to_numpy(float), np.hstack(parts)


def run_task(args) -> dict:
    from partA_stats import Scorer, shapley, summarize, summarize_diff
    body, rung, outcome, d, cols, k, n_boot, seed, with_games = args
    t = time.time()
    B, cat = design(d, body, rung)
    y = d[outcome].to_numpy(float)
    G = games(d, k) if with_games else {}
    gcols, gnames = [], []
    for g, (pl, cmap, _) in G.items():
        for S, v in cmap.items():
            gcols.append(v)
            gnames.append((g, S))
    X = np.column_stack([d[c].to_numpy(float) for c in cols] + gcols)
    names = cols + [f"G::{g}::{'|'.join(sorted(S))}" for g, S in gnames]
    sc = Scorer(X, names, y, B, cat)
    pt = sc.eval()
    bs = sc.boot(n_boot, seed)
    ix = {n: i for i, n in enumerate(names)}
    res = {"body": body, "rung": rung, "outcome": outcome, "n_base": int(len(sc.base_idx)), "n_boot": n_boot,
           "components": {}, "diffs": {}, "holm_contrasts": {}, "shapley": {}}
    for c in cols:
        res["components"][c] = {**summarize(pt[ix[c]], bs[:, ix[c]]), "n": sc.n[c]}
    for ax, (a, b) in PAIRS.items():
        for pre in ("ner", "ch", "chd", "cha") + (("nov", "novnull") if ax in NOV_AXES else ()):
            ca, cb = f"{pre}_{ax}_{a}", f"{pre}_{ax}_{b}"
            if ca in ix and cb in ix:
                res["diffs"][f"{ca}-{cb}"] = summarize_diff(pt[ix[ca]], pt[ix[cb]], bs[:, ix[ca]], bs[:, ix[cb]])
    if "chd_all" in ix and "cha_all" in ix:
        res["diffs"]["chd_all-cha_all"] = summarize_diff(pt[ix["chd_all"]], pt[ix["cha_all"]], bs[:, ix["chd_all"]], bs[:, ix["cha_all"]])
    for h, (a, b) in HOLM.items():
        if a in ix and b in ix:
            res["holm_contrasts"][h] = summarize_diff(pt[ix[a]], pt[ix[b]], bs[:, ix[a]], bs[:, ix[b]])
    for g, (pl, cmap, fair) in G.items():
        def vals(row: np.ndarray) -> dict:
            v = {}
            for S in cmap:
                x = row[ix[f"G::{g}::{'|'.join(sorted(S))}"]]
                v[S] = 0.0 if (len(S) == 0 and not np.isfinite(x)) else x
            return v
        v0 = vals(pt)
        phi0 = shapley(pl, v0)
        full = frozenset(pl)
        eff = abs(sum(phi0.values()) - (v0[full] - v0[frozenset()]))
        phib = []
        for r in range(bs.shape[0]):
            vb = vals(bs[r])
            if all(np.isfinite(list(vb.values()))):
                pb = shapley(pl, vb)
                phib.append([pb[p] for p in pl] + [vb[full] - vb[frozenset()]])
        phib = np.array(phib) if phib else np.zeros((0, len(pl) + 1))
        vfull = v0[full] - v0[frozenset()]
        out = {"players": pl, "v_full": v0[full], "v_empty": v0[frozenset()], "v_full_minus_empty": vfull,
               "efficiency_abs_err": eff, "fair_share": fair, "small_v_F5": bool(abs(vfull) < 0.03),
               "n_boot_ok": int(len(phib)), "phi": {}}
        for i, p in enumerate(pl):
            e = {"phi": phi0[p]}
            if len(phib) >= 10:
                e["phi_ci"] = [float(np.percentile(phib[:, i], 2.5)), float(np.percentile(phib[:, i], 97.5))]
                if abs(vfull) >= 0.03:
                    sh = phib[:, i] / phib[:, -1]
                    sh = sh[np.isfinite(sh) & (np.abs(phib[:, -1]) > 1e-9)]
                    e["share"] = phi0[p] / vfull
                    e["share_ci"] = [float(np.percentile(sh, 2.5)), float(np.percentile(sh, 97.5))] if len(sh) > 10 else None
            fs = fair.get("new_partner_share", fair.get("mass_share", fair.get("churn_mass_share", {}))).get(p)
            if fs is not None and "share" in e:
                e["fair_share"] = fs
                e["excess_share"] = e["share"] - fs
                if len(phib) >= 10:
                    ex = phib[:, i] / phib[:, -1] - fs
                    ex = ex[np.isfinite(ex)]
                    e["excess_ci"] = [float(np.percentile(ex, 2.5)), float(np.percentile(ex, 97.5))]
            out["phi"][p] = e
        # pairwise phi differences (paired bootstrap)
        if len(pl) >= 2 and len(phib) >= 10:
            out["phi_diff"] = {f"{pl[i]}-{pl[j]}": {"diff": phi0[pl[i]] - phi0[pl[j]], "ci": [
                float(np.percentile(phib[:, i] - phib[:, j], 2.5)), float(np.percentile(phib[:, i] - phib[:, j], 97.5))]}
                for i in range(len(pl)) for j in range(i + 1, len(pl))}
        res["shapley"][g] = out
    res["seconds"] = time.time() - t
    return res


# ----------------------------------------------------------------------------- placebo (label permutation)
def placebo(d: pd.DataFrame, rows: pd.DataFrame, n: int, seed: int, scheme: str) -> dict:
    """Class labels permuted (within concept, or across partner rows of the body); the 5 Holm contrasts recomputed."""
    from partA_stats import Scorer
    B, cat = design(d, "POOLED_EXP5", None)
    y = d.O2r_m50.to_numpy(float)
    R = rows[rows.ci.isin(set(d.ci))].copy()
    R["isnew"] = (R.comm == "new").astype(float)
    pos = {c: i for i, c in enumerate(d.ci.to_numpy())}
    R["pi"] = R.ci.map(pos)
    newr = R[R.role == "new"]
    chr_ = R[R.role != "new"]
    Et = {X: d[f"Enull_type_{X}"].to_numpy(float) for X in ("METHOD", "DOMAIN")}
    nC = len(d)
    rng = np.random.default_rng(seed)

    def perm(labels: np.ndarray, grp: np.ndarray) -> np.ndarray:
        if scheme == "across_rows":
            return labels[rng.permutation(len(labels))]
        o = np.lexsort((rng.random(len(labels)), grp))
        out = labels.copy()
        out[o] = labels[np.lexsort((np.arange(len(labels)), grp))]
        return out

    def agg(pi: np.ndarray, w: np.ndarray, mask: np.ndarray) -> np.ndarray:
        v = np.zeros(nC)
        np.add.at(v, pi[mask], w[mask])
        return v

    npi, cpi = newr.pi.to_numpy(), chr_.pi.to_numpy()
    base_nan_nov = ~np.isfinite(d.NOV_res.to_numpy(float))
    base_nan_ch = ~np.isfinite(d.churn.to_numpy(float))
    out = {h: [] for h in HOLM}
    for _ in range(n):
        cols = {}
        lt = perm(newr.type.to_numpy(), npi)
        isn = newr.isnew.to_numpy()
        for X in ("METHOD", "DOMAIN"):
            m = lt == X
            cnt = agg(npi, np.ones(len(npi)), m)
            nx = agg(npi, isn, m)
            with np.errstate(invalid="ignore", divide="ignore"):
                v = nx / cnt - Et[X]
            v[(cnt == 0) | base_nan_nov] = np.nan
            cols[f"novnull_type_{X}"] = v
        lc = perm(newr.comm.to_numpy(), npi)
        for X in ("new", "old"):
            cols[f"ner_comm_{X}"] = agg(npi, newr.w_ner.to_numpy(), lc == X)
        ld = perm(newr.deg.to_numpy(), npi)
        for X in ("low", "high"):
            v = agg(npi, newr.w_nov.to_numpy(), ld == X)
            v[base_nan_nov] = np.nan
            cols[f"nov_deg_{X}"] = v
        lr = perm(newr.carrier.to_numpy(), npi)
        for X in ("mixed", "pure"):
            cols[f"ner_carrier_{X}"] = agg(npi, newr.w_ner.to_numpy(), lr == X)
        lro = perm(chr_.role.to_numpy(), cpi)
        for X, nm in (("drop", "chd_all"), ("add", "cha_all")):
            v = agg(cpi, chr_.w_ch.to_numpy(), lro == X)
            v[base_nan_ch] = np.nan
            cols[nm] = v
        names = list(cols)
        sc = Scorer(np.column_stack([cols[c] for c in names]), names, y, B, cat)
        p = dict(zip(names, sc.eval()))
        for h, (a, b) in HOLM.items():
            out[h].append(p[a] - p[b])
    return {h: np.array(v) for h, v in out.items()}


# ----------------------------------------------------------------------------- bridging
def bridging(F: pd.DataFrame, bp: pd.DataFrame, meta: pd.DataFrame | None, logger, n_boot: int, frame: str) -> dict:
    out = {"frame": frame, "n_papers": int(len(bp)), "n_bridging": int(bp.bridging.sum())}
    if meta is None:
        out["note"] = "authors/doc_type not available for this frame"
        return out
    d = bp.merge(meta.drop(columns=["year"]).drop_duplicates(["ci", "work_id"]), on=["ci", "work_id"], how="left")
    d["team_size"] = d.authors.map(lambda a: len(a) if isinstance(a, (list, np.ndarray)) else np.nan)
    first = meta.explode("authors").dropna(subset=["authors"]).groupby(["ci", "authors"]).year.min().to_dict()
    d["share_new_authors"] = [np.mean([first.get((c, a), y) >= y for a in au]) if isinstance(au, (list, np.ndarray)) and len(au) else np.nan
                              for c, y, au in zip(d.ci, d.year, d.authors)]
    has_dt = "doc_type" in d.columns and d.doc_type.notna().any()
    if has_dt:
        d["is_review"] = (d.doc_type == 1).astype(float)
    else:
        out["is_review"] = "doc_type missing for this frame (logged)"
    d["has_offhome_topic"] = d.has_offhome_topic.astype(float)
    vars_ = ["team_size", "share_new_authors", "has_offhome_topic", "n_topics"] + (["is_review"] if has_dt else [])
    ids, inv = np.unique(d.ci.to_numpy(), return_inverse=True)
    rng = np.random.default_rng(SEED)
    prof = {}
    br_ = d.bridging.to_numpy(bool)
    for v in vars_:
        a, b = d.loc[d.bridging, v].mean(), d.loc[~d.bridging, v].mean()
        prof[v] = {"bridging": float(a), "other": float(b), "diff": float(a - b)}
        x = d[v].to_numpy(float)
        fin = np.isfinite(x)
        # per-concept sums / counts for bridging and other papers -> concept-cluster bootstrap by reweighting
        S = {}
        for nm, m in (("b", br_ & fin), ("o", ~br_ & fin)):
            S[nm] = (np.bincount(inv, weights=np.where(m, x, 0.0), minlength=len(ids)),
                     np.bincount(inv, weights=m.astype(float), minlength=len(ids)))
        bs = []
        for _ in range(n_boot):
            w = np.bincount(rng.integers(0, len(ids), len(ids)), minlength=len(ids)).astype(float)
            mb = (w * S["b"][0]).sum() / max((w * S["b"][1]).sum(), 1e-12)
            mo = (w * S["o"][0]).sum() / max((w * S["o"][1]).sum(), 1e-12)
            bs.append(mb - mo)
        bs = np.array(bs)
        prof[v]["diff_ci_concept_cluster"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
        prof[v]["n_papers_bridging"], prof[v]["n_papers_other"] = int((br_ & fin).sum()), int((~br_ & fin).sum())
    out["profile"] = prof
    return out


def psp_extra(d: pd.DataFrame, x: str, y: str, extra: list[str], body: str, n_boot: int, seed: int) -> dict:
    from partA_stats import Scorer, summarize
    B, cat = design(d, body, None)
    if extra:
        B = np.c_[B, d[extra].to_numpy(float)]
    sc = Scorer(d[[x]].to_numpy(float), [x], d[y].to_numpy(float), B, cat)
    return {**summarize(sc.eval()[0], sc.boot(n_boot, seed)[:, 0]), "n": sc.n[x], "extra_controls": extra}


# ----------------------------------------------------------------------------- figures
def figures(R: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    comps = ["NOVCHURN_home", "NOV_res", "churn", "new_edge_rate", "nov_type_METHOD", "nov_type_DOMAIN",
             "ner_comm_new", "ner_comm_old", "nov_deg_low", "nov_deg_high", "ner_carrier_mixed", "ner_carrier_pure",
             "chd_all", "cha_all"]
    bodies = [b for b in ("DEV", "OLD_HELDOUT", "COHORT_2010_14", "POOLED_EXP5", "COHORT_2015_17_R0",
                          "COHORT_2015_17_R3") if f"{b}|O2r_m50" in R]
    fig, ax = plt.subplots(figsize=(8, 9))
    cols = plt.cm.tab10(np.arange(len(bodies)))
    for bi, b in enumerate(bodies):
        cc = R[f"{b}|O2r_m50"]["components"]
        for ci_, c in enumerate(comps):
            e = cc.get(c, {})
            if e.get("rho") is None:
                continue
            yv = ci_ + (bi - len(bodies) / 2) * 0.12
            lo, hi = e["ci"] if e.get("ci") else (e["rho"], e["rho"])
            ax.errorbar(e["rho"], yv, xerr=[[e["rho"] - lo], [hi - e["rho"]]], fmt="o", ms=3, color=cols[bi],
                        label=b if ci_ == 0 else None, capsize=2)
    ax.axvline(0, color="grey", lw=0.8)
    ax.set_yticks(range(len(comps)))
    ax.set_yticklabels(comps, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("partial Spearman with O2r_m50 given B5 (95% concept-bootstrap CI)")
    ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIGS / f"partner_forest.{ext}", dpi=150)
    plt.close(fig)
    gs = ["NOVCHURN_type", "NOVCHURN_deg", "NOVCHURN_carrier", "NOVCHURN_direction", "ner_type_x_comm",
          "churn_type_x_comm"]
    bodies2 = [b for b in ("POOLED_EXP5", "OLD_HELDOUT", "COHORT_2015_17_R0") if f"{b}|O2r_m50" in R]
    fig, axs = plt.subplots(2, 3, figsize=(12, 6.5))
    for gi, g in enumerate(gs):
        a = axs.flat[gi]
        for bi, b in enumerate(bodies2):
            S = R[f"{b}|O2r_m50"]["shapley"].get(g)
            if not S:
                continue
            pl = S["players"]
            xs = np.arange(len(pl)) + (bi - 1) * 0.25
            ph = [S["phi"][p]["phi"] for p in pl]
            lo = [S["phi"][p].get("phi_ci", [np.nan, np.nan])[0] for p in pl]
            hi = [S["phi"][p].get("phi_ci", [np.nan, np.nan])[1] for p in pl]
            a.bar(xs, ph, width=0.25, color=cols[bi], label=b if gi == 0 else None,
                  yerr=[np.array(ph) - np.array(lo), np.array(hi) - np.array(ph)], capsize=2)
            a.set_xticks(np.arange(len(pl)))
            a.set_xticklabels(pl, fontsize=7, rotation=20)
        a.axhline(0, color="grey", lw=0.8)
        a.set_title(g, fontsize=9)
    axs.flat[0].legend(fontsize=7)
    fig.supylabel("Shapley value phi (psp units; sums to v(full) - v(empty)), O2r_m50")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIGS / f"shapley_bars.{ext}", dpi=150)
    plt.close(fig)


# ----------------------------------------------------------------------------- main
def load_all(logger, limit: int = 0) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict, dict]:
    spec = json.loads((RES / "frozen_spec_iter5.json").read_text())
    k = spec["novchurn_constants"]
    comp5 = pd.read_parquet(DATA / "partner_home_components_exp5.parquet")
    compc = pd.read_parquet(DATA / "partner_home_components_cohort.parquet")
    rows5 = read_parts(DATA / "partner_home_rows_exp5")
    rowsc = read_parts(DATA / "partner_home_rows_cohort")
    F5, id5 = build_features(comp5, rows5, k)
    Fc, idc = build_features(compc, rowsc, k)
    logger.info(f"identities exp5 {id5}")
    logger.info(f"identities cohort {idc}")
    return F5, Fc, rows5, rowsc, {"exp5": id5, "cohort": idc}, spec


@__import__("loguru").logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=0, help="0 = spec N_BOOT")
    ap.add_argument("--n-placebo", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out-tag", default="")
    args = ap.parse_args()
    logger = setup_logger(f"score_partA{args.out_tag}")
    t0 = time.time()
    from seal_iter5 import check
    seal = check()
    F5, Fc, rows5, rowsc, ident, spec = load_all(logger)
    for nm, idd in ident.items():
        bad = {k_: v for k_, v in idd.items() if not k_.endswith("_min") and v > 1e-12}
        if bad:
            raise RuntimeError(f"decomposition identity failed ({nm}): {bad}")
        if idd["jner_rest_min"] < -1e-12 or idd["jch_rest_min"] < -1e-12:
            raise RuntimeError(f"joint-part remainder negative ({nm})")
    n_boot = args.n_boot or spec["N_BOOT"]
    n_pl = args.n_placebo or spec["N_PLACEBO"]
    k = spec["novchurn_constants"]
    # ---------------- outcomes (after the seal check)
    A = pd.read_parquet(E8 / "data/analysis_table.parquet", columns=["ci", "t0", "group", "split", "unit", "new_edge_rate",
                                                                     "O2r_m50", "O2r_resid", "O5_WW"] + B5)
    A = A.rename(columns={"new_edge_rate": "new_edge_rate_ALL"})
    op = pd.read_parquet(E10 / "data/features_exp5_open.parquet", columns=["ci", "OPEN_home"])
    D5 = A.merge(F5, on="ci", how="left").merge(op, on="ci", how="left")
    D5["body"] = np.where(D5.split == "DEV", "DEV", np.where(D5.split == "COHORT", "COHORT_2010_14", "OLD_HELDOUT"))
    AC = pd.read_parquet(E10 / "data/analysis_cohort.parquet")
    keep = [c for c in AC.columns if not c.endswith(("__home", "__all", "__sizematch")) and c not in ("n_home_early",)]
    Dc = AC[keep].merge(Fc, on="ci", how="left")
    Dc["body"] = "COHORT_2015_17"
    D5.to_parquet(DATA / "partA_features_exp5.parquet", index=False)
    Dc.to_parquet(DATA / "partA_features_cohort.parquet", index=False)
    cols5 = component_columns(D5)
    colsc = [c for c in component_columns(Dc) if c != "new_edge_rate_ALL"]
    # ---------------- sanity gate: Exp10 published cohort component psp at R2 (must match to 3 decimals)
    from ladder import rung_design
    from rq1stats import psp_point
    san = {}
    Bc, Cc = rung_design(Dc, "R2")
    Bm, Cm, yv = Bc.to_numpy(float), Cc.to_numpy(float), Dc.O2r_m50.to_numpy(float)
    for c, pub in (("NOV_res", 0.1336899997969982), ("edge_persistence", -0.1123107545240305)):
        xv = Dc[c].to_numpy(float)
        ok = np.isfinite(xv) & np.isfinite(yv) & np.all(np.isfinite(Bm), 1)
        rho = psp_point(xv[ok], yv[ok], Bm[ok], Cm[ok])
        san[c] = {"recomputed_R2": rho, "exp10_published": pub, "abs_diff": abs(rho - pub), "n": int(ok.sum())}
    san["pass"] = bool(all(v["abs_diff"] < 5e-4 for v in san.values() if isinstance(v, dict)))
    logger.info(f"Exp10 sanity gate: {san}")
    if not san["pass"]:
        raise RuntimeError(f"Exp10 published component psp not reproduced: {san}")
    # ---------------- tasks
    tasks = []
    bodies5 = {"POOLED_EXP5": D5, "DEV": D5[D5.body == "DEV"], "OLD_HELDOUT": D5[D5.body == "OLD_HELDOUT"],
               "COHORT_2010_14": D5[D5.body == "COHORT_2010_14"]}
    bodies5.update({g: D5[(D5.body == "OLD_HELDOUT") & (D5.unit == g)] for g in HELD})
    for bi, (b, d) in enumerate(bodies5.items()):
        for oi, o in enumerate(("O2r_m50", "O2r_resid")):
            tasks.append((b, None, o, d.reset_index(drop=True), cols5, k, n_boot, SEED + 1000 * bi, True))
    tasks.append(("POOLED_EXP5", None, "O5_WW", D5.reset_index(drop=True),
                  ["NOVCHURN_home", "NOV_res", "churn", "new_edge_rate", "OPEN_home"], k, n_boot, SEED + 77, False))
    for ri, rung in enumerate(("R0", "R3")):
        for o in ("O2r_m50", "O2r_resid"):
            tasks.append(("COHORT_2015_17", rung, o, Dc.reset_index(drop=True), colsc, k, n_boot, SEED + 5000 + ri, True))
    order = np.argsort([-len(t[3]) for t in tasks])
    logger.info(f"{len(tasks)} scoring tasks, n_boot {n_boot}, workers {args.workers}")
    R = {}
    with ProcessPoolExecutor(args.workers, mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(run_task, tasks[i]): i for i in order}
        from concurrent.futures import as_completed
        for fu in as_completed(futs):
            r = fu.result()
            key = f"{r['body']}{'_' + r['rung'] if r['rung'] else ''}|{r['outcome']}"
            R[key] = r
            logger.info(f"{key}: n={r['n_base']} NOVCHURN={r['components'].get('NOVCHURN_home', {}).get('rho')} "
                        f"({r['seconds']:.0f}s)")
    # ---------------- DL over held-out groups + Holm
    from partA_stats import dl_fisher
    from rq1stats import dersimonian_laird, holm
    dl = {}
    for o in ("O2r_m50", "O2r_resid"):
        dl[o] = {"components": {}, "diffs": {}}
        for c in cols5:
            e = [R[f"{g}|{o}"]["components"][c] for g in HELD]
            dl[o]["components"][c] = dl_fisher([x["rho"] for x in e], [x["se_z"] for x in e])
        for dk in R[f"POOLED_EXP5|{o}"]["diffs"]:
            e = [R[f"{g}|{o}"]["diffs"].get(dk, {}) for g in HELD]
            pl = dersimonian_laird(np.array([x.get("diff") if x.get("diff") is not None else np.nan for x in e], float),
                                   np.array([x.get("se") if x.get("se") is not None else np.nan for x in e], float))
            dl[o]["diffs"][dk] = pl
        for h in HOLM:
            e = [R[f"{g}|{o}"]["holm_contrasts"].get(h, {}) for g in HELD]
            dl[o].setdefault("holm_contrasts", {})[h] = dersimonian_laird(
                np.array([x.get("diff") if x.get("diff") is not None else np.nan for x in e], float),
                np.array([x.get("se") if x.get("se") is not None else np.nan for x in e], float))
    H = R["POOLED_EXP5|O2r_m50"]["holm_contrasts"]
    hp = holm([H[h]["p_two"] for h in HOLM])
    holm_res = {h: {**H[h], "p_holm": hp[i],
                    "DL_heldout_groups": dl["O2r_m50"]["holm_contrasts"][h],
                    "cohort_2015_17_R0_direction": R["COHORT_2015_17_R0|O2r_m50"]["holm_contrasts"].get(h, {}).get("diff"),
                    "cohort_2015_17_R3_direction": R["COHORT_2015_17_R3|O2r_m50"]["holm_contrasts"].get(h, {}).get("diff")}
                for i, h in enumerate(HOLM)}
    # ---------------- placebos
    pl_res = {}
    obs = {h: H[h]["diff"] for h in HOLM}
    for scheme in ("across_rows", "within_concept"):
        P = placebo(D5.reset_index(drop=True), rows5, n_pl, SEED + 9, scheme)
        pl_res[scheme] = {}
        for h, v in P.items():
            v = v[np.isfinite(v)]
            pl_res[scheme][h] = {"n": int(len(v)), "mean": float(v.mean()), "sd": float(v.std(ddof=1)),
                                 "q025_q975": [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))],
                                 "observed": obs[h], "observed_quantile": float((v < obs[h]).mean()),
                                 "p_two_placebo": float((1 + (np.abs(v - v.mean()) >= abs(obs[h] - v.mean())).sum()) / (1 + len(v)))}
        logger.info(f"placebo {scheme}: { {h: round(x['mean'], 4) for h, x in pl_res[scheme].items()} }")
    # ---------------- bridging
    L = read_parts(E11 / "data/frame_matches_long", columns=["ci", "year", "work_id", "doc_type", "authors"])
    L = L.merge(D5[["ci", "t0"]], on="ci")
    L = L[L.year <= L.t0 + 2].drop(columns=["t0"])
    bp5 = pd.read_parquet(DATA / "bridging_home_papers_exp5.parquet")
    br = {"exp5": bridging(D5, bp5, L, logger, 500, "EXP5")}
    del L
    pc = pd.read_parquet(E10 / "data/passC_early.parquet", columns=["ci", "year", "work_id", "authors", "tagstate"])
    pc = pc[pc.tagstate == 1].drop(columns=["tagstate"])
    bpc = pd.read_parquet(DATA / "bridging_home_papers_cohort.parquet")
    br["cohort_2015_17"] = bridging(Dc, bpc, pc, logger, 500, "COHORT_2015_17")
    br["cohort_2015_17"]["note_doc_type"] = "passC_early has authors but no doc_type: is_review not computed (logged)"
    add_deviation("bridging_cohort_doc_type", "2015-17 cohort bridging profile has no is_review: passC_early lacks doc_type")
    br["psp"] = {}
    for b, d in (("POOLED_EXP5", D5), ("OLD_HELDOUT", D5[D5.body == "OLD_HELDOUT"])):
        br["psp"][b] = {"bridging_share_home|B5": psp_extra(d, "bridging_share_home", "O2r_m50", [], b, n_boot, SEED + 3),
                        "NOVCHURN_home|B5": psp_extra(d, "NOVCHURN_home", "O2r_m50", [], b, n_boot, SEED + 3),
                        "NOVCHURN_home|B5+bridging_share_home": psp_extra(d, "NOVCHURN_home", "O2r_m50",
                                                                          ["bridging_share_home"], b, n_boot, SEED + 3)}
    # ---------------- predictions P-A1..P-A5
    PS = R["POOLED_EXP5|O2r_m50"]["shapley"]
    ty = PS["NOVCHURN_type"]["phi"]["METHOD"]
    pred = {
        "P-A1": {"METHOD_shapley_share": ty.get("share"), "METHOD_share_ci": ty.get("share_ci"),
                 "METHOD_new_partner_share": PS["NOVCHURN_type"]["fair_share"]["new_partner_share"]["METHOD"],
                 "excess": ty.get("excess_share"), "excess_ci": ty.get("excess_ci"),
                 "holds_point": bool(ty.get("excess_share") is not None and ty["excess_share"] > 0),
                 "holds_ci": bool(ty.get("excess_ci") is not None and ty["excess_ci"][0] > 0)},
    }
    for key, h in (("P-A2", "C2_commnew_minus_commold_ner"), ("P-A3", "C3_lowdeg_minus_highdeg_nov"),
                   ("P-A4", "C4_mixed_minus_pure_ner"), ("P-A5", "C5_dropped_minus_added_churn")):
        e = holm_res[h]
        pred[key] = {"contrast": h, "diff": e["diff"], "ci": e["ci"], "p_holm": e["p_holm"],
                     "holds_point": bool(e["diff"] is not None and e["diff"] > 0),
                     "holds_holm": bool(e["diff"] is not None and e["diff"] > 0 and e["p_holm"] < 0.05)}
    out = {"status": spec["status"], "seal": seal, "identities": ident, "exp10_sanity_gate": san, "n_boot": n_boot,
           "bodies": R, "DL_heldout_groups": dl, "holm_family_POOLED_EXP5_O2r_m50": holm_res, "placebo": pl_res,
           "predictions": pred, "seconds": time.time() - t0}
    shap = {k_: {"shapley": v["shapley"], "n_base": v["n_base"]} for k_, v in R.items() if v["shapley"]}
    jdump({k_: v for k_, v in out.items()}, RES / f"partner_classes{args.out_tag}.json")
    jdump({"games": shap, "predictions": pred, "status": spec["status"]}, RES / f"partner_shapley{args.out_tag}.json")
    jdump(br, RES / f"bridging_papers_summary{args.out_tag}.json")
    figures(R)
    logger.info(f"Part A scoring done in {(time.time()-t0)/60:.1f} min; predictions {pred}")


if __name__ == "__main__":
    main()
