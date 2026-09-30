#!/usr/bin/env python3
"""Screen of candidate L, the background-adjusted naturalisation gap A*_h, on the frozen dev panel P78.

Pipeline (see README.md for the deviations forced by the shared OpenAlex credit pool running dry):
  S0      OpenAlex yearly counts (t0, newborn, O1, O3, log early volume, early growth) + S2 field distributions
          (home, dev restriction with sealed held-out fields, O2r rarefied breadth, field retention R_j, B5 reach).
  Lineage concept-paper citation links (S2 citation lists), self links split off, fractional S2 field labels.
  Stage 1 per concept x off-home field j: year-stratified MH log-OR (child j vs H) x (parent j vs H) minus the same
          log-OR on the same children's background references; child-bootstrap variance.
  Stage 2 REML crossed random-effects pooling -> rho*_cj, A*_h = sum_j pi_cj rho*_cj (PyMC NUTS headline check,
          statsmodels BinomialBayesMixedGLM robustness).
  Screen  LOGO (4 dev home-field groups) ridge Delta-rho over B5 for O2r (2,000 concept bootstrap), per-group signs,
          split-half reliability (50 splits, Spearman-Brown), size correlations, O1/O3 Delta-AUC, field-level
          rho*_cj -> R_j test (concept-clustered bootstrap), M1, foils, pre-registered survival rule.
Usage: python method.py [--max-concepts N] [--splits 50] [--no-pymc] [--no-glmm]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):  # small matrices: avoid BLAS oversubscription
    os.environ.setdefault(_v, "1")

import argparse
import gzip
import json
import math
import multiprocessing as mp
import pickle
import resource
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent
RES = ROOT / "results"
sys.path.insert(0, str(ROOT))

from lineage import (F, S2_DEV, S2_FIELDS, Concept, crude_lor, foils, load_concept, load_raw, membership,  # noqa: E402
                     stage1)
from panel import DEV_FIELDS, seeded_order, slug  # noqa: E402
from pool import fit_dl, fit_pymc, fit_reml, predict, var_of  # noqa: E402
from s0 import compute_s0, newborn, onset, rarefied_richness, shannon  # noqa: E402
from screen import compare, rho, spearman_brown  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(ROOT / "logs").mkdir(exist_ok=True)
logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")

SEED = 20260928
PROBE_CRUDE = {"optogenetics": -0.551, "crowdsourcing": 0.382, "extreme learning machine": -1.063,
               "induced pluripotent stem cell": -0.628, "compressed sensing": 0.243}
B5_COLS = ["B_logvol", "B_growth", "B_offhome", "B_entropy", "B_nfields"]
BINS = [(0, 15), (15, 30), (30, 60), (60, 10**9)]


def set_limits() -> None:
    ram = 16 * 1024 ** 3
    resource.setrlimit(resource.RLIMIT_AS, (ram * 2, ram * 2))


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


# ------------------------------------------------------------------ S0
def s0_openalex() -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    raw = json.loads((RES / "s0_raw.json").read_text())
    G = {int(k): v for k, v in raw["_G"].items()}
    counts = {}
    for c in seeded_order():
        v = raw[c["canonical"]]
        counts[c["canonical"]] = {int(k): x for k, x in v["yc"].items()} if isinstance(v["yc"], dict) else None
    rows, frows, dropped = compute_s0(raw, seeded_order())  # OpenAlex topic-field S0 (credit-bound subset)
    return {"G": G, "yc": counts, "oa_home_raw": raw}, pd.DataFrame(rows), pd.DataFrame(dropped)


def count_outcomes(yc: dict[int, int], G: dict[int, int], t0: int) -> dict:
    share = lambda y: yc.get(y, 0) / G[y]
    peak = max(yc.get(y, 0) for y in range(t0 + 3, t0 + 9))
    tail = np.mean([yc.get(t0 + 7, 0), yc.get(t0 + 8, 0)])
    return {"t0": t0, "newborn": bool(newborn(yc, t0)),
            "O1": int(np.mean([share(y) for y in range(t0 + 6, t0 + 9)]) >= share(t0 + 5)),
            "O3": int(tail == 0 or peak / tail >= 2),
            "B_logvol": math.log1p(sum(yc.get(y, 0) for y in range(t0, t0 + 5))),
            "B_growth": math.log((yc.get(t0 + 4, 0) + 1) / (yc.get(t0 + 1, 0) + 1))}


def s0_s2(c: Concept) -> tuple[dict, list[dict]]:
    """Field-based S0 parts from the S2 paper sample (fractional labels, scaled by the thinning factor)."""
    t0 = c.t0
    lab = c.labelled

    def mass(y0: int, y1: int) -> np.ndarray:
        m = lab & (c.year >= y0) & (c.year <= y1)
        return c.M[m].sum(0) * c.thin_early

    fe, f01, f34 = mass(t0, t0 + 4), mass(t0, t0 + 1), mass(t0 + 3, t0 + 4)
    fl = c.late_mass * c.thin_late
    H = c.H
    Ne, Nl = fe.sum(), fl.sum()
    offm = np.ones(F, bool)
    offm[H] = False
    row = {"home_s2": "|".join(S2_FIELDS[h] for h in H),
           "O2r": rarefied_richness(list(fl), 30), "O2r_m50": rarefied_richness(list(fl), 50),
           "O2r_m20": rarefied_richness(list(fl), 20), "N_late": float(Nl), "O2r_hurdle": int(Nl >= 30),
           "B_offhome": float(fe[offm].sum() / Ne) if Ne else np.nan,
           "B_entropy": shannon(list(fe)), "B_nfields": int((fe >= 2).sum()),
           "off_early_vol": math.log1p(fe[offm].sum()),
           "off_growth": math.log((f34[offm].sum() + 1) / (f01[offm].sum() + 1)),
           "label_coverage_early": float(lab.mean()) if len(lab) else np.nan,
           "late_sample_n": int(round(c.late_mass.sum())), "thin_early": c.thin_early, "thin_late": c.thin_late}
    frows = []
    for j in np.where(offm & (fe >= 5))[0]:
        se, sl = fe[j] / Ne, (fl[j] / Nl if Nl else 0.0)
        frows.append({"concept": c.name, "field": S2_FIELDS[j], "j": int(j), "R_j": int(sl >= 0.5 * se and fl[j] >= 9),
                      "n_j_early": float(fe[j]), "n_j_late": float(fl[j]), "log_n_j_early": math.log(fe[j]),
                      "growth_j": math.log((f34[j] + 1) / (f01[j] + 1)), "share_j": float(se)})
    return row, frows


def load_bg(c: Concept, sl: str) -> tuple[np.ndarray, np.ndarray]:
    p = RES / "concepts" / sl / "bg.json.gz"
    n = len(c.child_idx)
    B = np.zeros((n, F))
    has = np.zeros(n, bool)
    if not p.exists():
        return B, has
    d = json.loads(gzip.decompress(p.read_bytes()))
    pos = {c.ids[ci]: k for k, ci in enumerate(c.child_idx)}
    for pid, refs in d["refs"].items():
        k = pos.get(pid)
        if k is None:
            continue
        ms = [membership(d["fos"].get(r)) for r in refs]
        ms = [m for m in ms if m is not None]
        if ms:
            B[k] = np.mean(ms, axis=0)
            has[k] = True
    return B, has


# ------------------------------------------------------------------ stage 2 wrapper
def pool_all(units: list[dict], names: list[str], n_off: dict, engine: str = "reml"):
    """units: stage-1 data rows {ci, field, k-order}. Returns fit and per-concept feature dict."""
    y = np.array([u["rho_hat"] for u in units])
    v = np.array([u["v"] for u in units])
    cidx = np.array([u["ci"] for u in units])
    fields = [u["field"] for u in units]
    fit = (fit_reml if engine == "reml" else fit_dl)(y, v, cidx, len(names), fields)
    return fit


def concept_features(fit, units: list[dict], names: list[str], child_mass: dict) -> dict:
    by_c: dict[int, list[int]] = {}
    for k, u in enumerate(units):
        by_c.setdefault(u["ci"], []).append(k)
    p = len(fit.beta)
    nc = len(fit.u)
    grand = float(np.mean(fit.X @ fit.beta)) if len(units) else float("nan")
    out = {}
    for ci, name in enumerate(names):
        ks = by_c.get(ci, [])
        if not ks:
            out[name] = {"A_h": grand, "A_h_sd": float("nan"), "A_h_missing": 1, "A_h_u": float(fit.u[ci]),
                         "n_nat_fields": 0, "max_rho": float("nan"), "n_data_fields": 0}
            continue
        wts = np.array([child_mass[(ci, units[k]["field"])] for k in ks])
        wts = wts / wts.sum()
        L = np.zeros(len(fit.Cinv))
        vals, n_nat = [], 0
        for w_, k in zip(wts, ks):
            val, l = predict(fit, ci, units[k]["field"], k)
            sd = math.sqrt(max(var_of(fit, l), 1e-12))
            vals.append(val)
            n_nat += int(val > 0 and 0.5 * (1 + math.erf(val / sd / math.sqrt(2))) > 0.8)
            L += w_ * l
        lu = np.zeros(len(fit.Cinv))
        lu[p + ci] = 1
        out[name] = {"A_h": float(L[:p] @ fit.beta + (L[p:p + nc] @ fit.u) + (L[p + nc:] @ fit.w)),
                     "A_h_sd": math.sqrt(max(var_of(fit, L), 0)), "A_h_missing": 0, "A_h_u": float(fit.u[ci]),
                     "A_h_u_sd": math.sqrt(max(var_of(fit, lu), 0)),
                     "n_nat_fields": n_nat, "max_rho": float(max(vals)), "n_data_fields": len(ks)}
    return out


def stage1_units(concepts: list[Concept], bgs: list, subs: list | None = None, n_boot: int = 200,
                 seed: int = SEED) -> tuple[list[dict], dict, list]:
    units, child_mass, s1s = [], {}, []
    for ci, c in enumerate(concepts):
        B, has = bgs[ci]
        sub = None if subs is None else subs[ci]
        if len(c.child_idx) == 0 or (sub is not None and len(sub) == 0):
            s1s.append(None)
            continue
        s = stage1(c, B, has, sub=sub, n_boot=n_boot, seed=seed + ci)
        s1s.append(s)
        for j in np.where(np.isfinite(s.rho_hat) & (s.n_child_j >= 1.0))[0]:
            units.append({"ci": ci, "field": S2_FIELDS[j], "j": int(j), "rho_hat": float(s.rho_hat[j]),
                          "v": float(s.v[j]), "lor_c": float(s.lor_c[j]), "lor_bg": float(s.lor_bg[j]),
                          "n_child_j": float(s.n_child_j[j])})
            child_mass[(ci, S2_FIELDS[j])] = float(s.n_child_j[j])
    return units, child_mass, s1s


# ------------------------------------------------------------------ split-half reliability (worker)
_W: dict = {}


def _init_worker(pkl: str) -> None:
    import os
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    logger.remove()
    _W["data"] = pickle.loads(Path(pkl).read_bytes())


def _half_crude(c: Concept, B: np.ndarray, has: np.ndarray, sub: np.ndarray) -> tuple[float, float]:
    cH = c.cH[sub]
    Pm = c.P[sub]
    tot = Pm.sum(1)
    par_off = np.where(tot > 0, 1 - (Pm @ c.hmask) / np.where(tot > 0, tot, 1), 0)
    br = has[sub]
    if not br.any():
        return float("nan"), float("nan")
    Bm = B[sub][br]
    bt = Bm.sum(1)
    b_off = np.where(bt > 0, 1 - (Bm @ c.hmask) / np.where(bt > 0, bt, 1), 0)
    bgl = crude_lor(1 - cH[br], b_off)
    return bgl, crude_lor(1 - cH[br], par_off[br]) - bgl


def run_split(s: int) -> dict:
    concepts, bgs, names = _W["data"]
    rng = np.random.default_rng(SEED + 1000 + s)
    halves = [[], []]
    for c in concepts:
        n = len(c.child_idx)
        if n == 0:
            halves[0].append(np.zeros(0, int)); halves[1].append(np.zeros(0, int))
            continue
        cH = c.cH
        h0, h1 = [], []
        for grp in (np.where(cH >= 0.5)[0], np.where(cH < 0.5)[0]):
            g = rng.permutation(grp)
            h0 += list(g[: len(g) // 2]); h1 += list(g[len(g) // 2:])
        halves[0].append(np.array(sorted(h0), int)); halves[1].append(np.array(sorted(h1), int))
    res = {}
    for h in (0, 1):
        units, cm, s1s = stage1_units(concepts, bgs, subs=halves[h], n_boot=200, seed=SEED + 7 * s + h)
        feats = {}
        if len(units) >= 5:
            try:
                fit = pool_all(units, names, {})
                feats = concept_features(fit, units, names, cm)
            except (np.linalg.LinAlgError, ValueError) as e:
                logger.warning(f"split {s} half {h}: pooling failed {e!r}")
        rows = {}
        for ci, name in enumerate(names):
            c = concepts[ci]
            sub = halves[h][ci]
            n_off = int((c.cH[sub] < 0.5).sum()) if len(sub) else 0
            bgl, crude = _half_crude(c, *bgs[ci], sub) if len(sub) else (np.nan, np.nan)
            f = feats.get(name, {})
            rows[name] = {"A_h": f.get("A_h", np.nan) if not f.get("A_h_missing", 1) else np.nan,
                          "A_h_u": f.get("A_h_u", np.nan) if not f.get("A_h_missing", 1) else np.nan,
                          "max_rho": f.get("max_rho", np.nan), "n_nat_fields": f.get("n_nat_fields", np.nan),
                          "n_off": n_off, "bg_LOR": bgl, "A_h_crude": crude,
                          "A_h_MH": s1s[ci].A_h_MH if s1s[ci] is not None else np.nan}
        field_units = {}
        if feats:
            for k, u in enumerate(units):
                val, _ = predict(fit, u["ci"], u["field"], k)
                field_units[(names[u["ci"]], u["field"])] = (val, u["n_child_j"])
        res[h] = {"rows": rows, "field": field_units}
    return res


def reliability(results: list[dict], names: list[str]) -> dict:
    out = {}
    for feat in ("A_h", "A_h_u", "max_rho", "n_nat_fields", "bg_LOR", "A_h_crude", "A_h_MH"):
        rs = []
        for r in results:
            a = np.array([r[0]["rows"][n][feat] for n in names], float)
            b = np.array([r[1]["rows"][n][feat] for n in names], float)
            ok = np.array([min(r[0]["rows"][n]["n_off"], r[1]["rows"][n]["n_off"]) >= 10 for n in names])
            if feat == "bg_LOR":
                ok = np.ones(len(names), bool)
            rs.append(rho(a[ok], b[ok]))
        rs = np.array(rs, float)
        out[feat] = {"r_half_mean": float(np.nanmean(rs)) if np.isfinite(rs).any() else None,
                     "reliability_SB": float(np.nanmean([spearman_brown(x) for x in rs if np.isfinite(x)]))
                     if np.isfinite(rs).any() else None, "n_splits_valid": int(np.isfinite(rs).sum())}
    # field-level rho*
    rs = []
    for r in results:
        common = [k for k in r[0]["field"] if k in r[1]["field"] and min(r[0]["field"][k][1], r[1]["field"][k][1]) >= 5]
        if len(common) >= 5:
            rs.append(rho(np.array([r[0]["field"][k][0] for k in common]), np.array([r[1]["field"][k][0] for k in common])))
    rs = np.array(rs, float)
    out["rho_star_field"] = {"r_half_mean": float(np.nanmean(rs)) if np.isfinite(rs).any() else None,
                             "reliability_SB": float(np.nanmean([spearman_brown(x) for x in rs if np.isfinite(x)]))
                             if np.isfinite(rs).any() else None, "n_splits_valid": int(np.isfinite(rs).sum())}
    # reliability vs n (bins on the full-sample number of off-home linked children, per-half eligibility >= 3)
    return out


def reliability_vs_n(results: list[dict], names: list[str], n_off_full: dict) -> list[dict]:
    rows = []
    for lo, hi in BINS:
        members = [n for n in names if lo <= n_off_full[n] < hi]
        rs = []
        for r in results:
            a = np.array([r[0]["rows"][n]["A_h"] for n in members], float)
            b = np.array([r[1]["rows"][n]["A_h"] for n in members], float)
            rs.append(rho(a, b))
        rs = np.array(rs, float)
        rel = float(np.nanmean([spearman_brown(x) for x in rs if np.isfinite(x)])) if np.isfinite(rs).any() else None
        rows.append({"bin": f"{lo}-{hi if hi < 10**9 else 'inf'}", "floor": lo, "n_concepts": len(members),
                     "r_half_mean": float(np.nanmean(rs)) if np.isfinite(rs).any() else None, "reliability_SB": rel})
    return rows


# ------------------------------------------------------------------ GLMM robustness
def glmm_check(concepts: list[Concept], bgs: list, names: list[str], max_rows: int = 50000) -> dict:
    """One-stage BinomialBayesMixedGLM on link-level rows (discrete labels drawn from memberships; one parent / one
    background ref per child, seeded). y = parent in j (vs H); childj; refc (concept vs background)."""
    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
    rng = np.random.default_rng(SEED)
    rows = []
    for ci, c in enumerate(concepts):
        if len(c.child_idx) == 0:
            continue
        B, has = bgs[ci]
        Hs = set(c.H)
        for k, pi in enumerate(c.child_idx):
            cf = rng.choice(F, p=c.M[pi] / c.M[pi].sum())
            parents = c._cross.get(int(pi), [])
            if not parents:
                continue
            q = parents[rng.integers(len(parents))]
            pf = rng.choice(F, p=c.M[q] / c.M[q].sum())
            draws = [(1, pf)]
            if has[k]:
                draws.append((0, rng.choice(F, p=B[k] / B[k].sum())))
            for refc, g in draws:
                if cf in Hs:
                    js = [g] if g not in Hs else list({int(x) for x in np.nonzero(c.M[c.child_idx].sum(0))[0]} - Hs)
                else:
                    js = [cf]
                for j in js:
                    if g != j and g not in Hs:
                        continue
                    rows.append({"concept": names[ci], "j": int(j), "y": int(g == j), "childj": int(cf == j),
                                 "refc": refc})
    df = pd.DataFrame(rows)
    if len(df) > max_rows:
        df = df.sample(max_rows, random_state=SEED)
    df["stratum"] = df["concept"] + "|" + df["j"].astype(str) + "|" + df["refc"].astype(str)
    keep = df.groupby("stratum")["y"].transform(lambda s: s.nunique() > 1)
    df = df[keep].reset_index(drop=True)
    df["cj"] = df["concept"] + "|" + df["j"].astype(str)
    df["cx"] = df["childj"] * df["refc"]
    t = time.time()
    model = BinomialBayesMixedGLM.from_formula(
        "y ~ C(stratum) + childj + cx",
        {"c_int": "0 + C(concept):childj", "c_slope": "0 + C(concept):cx", "cj_slope": "0 + C(cj):cx"}, df)
    res = model.fit_vb()
    fe = dict(zip(model.exog_names, res.fe_mean))
    names_vc = model.vc_names
    vc_mean = np.asarray(res.vc_mean)
    slope = {}
    for nm, val in zip(names_vc, vc_mean):
        if nm.startswith("C(concept)[") and nm.endswith(":cx"):
            slope[nm.split("[", 1)[1].split("]")[0]] = fe.get("cx", 0.0) + float(val)
    logger.info(f"GLMM: {len(df)} rows, {df['stratum'].nunique()} strata, {time.time()-t:.0f}s, fixed cx={fe.get('cx'):.3f}")
    return {"n_rows": int(len(df)), "fixed_cx": float(fe.get("cx", np.nan)), "A_h_glmm": slope,
            "seconds": time.time() - t}


# ------------------------------------------------------------------ main
@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-concepts", type=int, default=10**6)
    ap.add_argument("--splits", type=int, default=50)
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--no-pymc", action="store_true")
    ap.add_argument("--no-glmm", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    set_limits()
    t_start = time.time()
    RES.mkdir(exist_ok=True)

    # ---------------- S0 (OpenAlex counts + OpenAlex topic-field S0 where the pool allowed)
    oa, oa_rows, oa_dropped = s0_openalex()
    G, YC = oa["G"], oa["yc"]
    order = seeded_order()
    dropped, orows, frows, concepts, bgs, names, sl_of = [], [], [], [], [], [], {}
    oa_home = {r["concept"]: r["home"] for _, r in oa_rows.iterrows()} if len(oa_rows) else {}
    oa_sealed = {r["concept"]: r["reason"] for _, r in oa_dropped.iterrows() if str(r["reason"]).startswith("home_sealed")}
    for c in order:
        name = c["canonical"]
        yc = YC[name]
        if yc is None:
            dropped.append({"concept": name, "reason": "no_counts"}); continue
        t0 = onset(yc)
        if t0 is None:
            dropped.append({"concept": name, "reason": "no_onset"}); continue
        if not 2003 <= t0 <= 2009:
            dropped.append({"concept": name, "reason": "t0_out_of_dev"}); continue
        if name in oa_sealed:
            dropped.append({"concept": name, "reason": oa_sealed[name] + " (OpenAlex S0)"}); continue
        sl = slug(name)
        p = RES / "concepts" / sl / "s2_raw.json.gz"
        if not p.exists():
            dropped.append({"concept": name, "reason": "not_fetched (time/rate budget)"}); continue
        if len(names) >= args.max_concepts:
            dropped.append({"concept": name, "reason": "beyond --max-concepts"}); continue
        cc = load_concept(load_raw(sl))
        sealed = [S2_FIELDS[h] for h in cc.H if S2_FIELDS[h] not in S2_DEV]
        if sealed:
            dropped.append({"concept": name, "reason": f"home_sealed_s2:{sealed[0]}"}); continue
        assert cc.year[cc.child_idx].max(initial=0) <= t0 + 4 if len(cc.child_idx) else True
        row = {"concept": name, "panel_group": c["panel_group"], **count_outcomes(yc, G, t0)}
        r2, fr = s0_s2(cc)
        row.update(r2)
        hmass = cc.M[cc.labelled & (cc.year >= t0) & (cc.year <= t0 + 1)].sum(0)
        row["dev_group"] = S2_DEV[S2_FIELDS[max(cc.H, key=lambda h: hmass[h])]]
        row["home_openalex_topic"] = oa_home.get(name)
        row["exact_share"] = cc.exact_share
        row["parent_thin"] = load_raw(sl).get("parent_thin", 1.0)
        orows.append(row)
        for f in fr:
            f["dev_group"] = row["dev_group"]
        frows += fr
        concepts.append(cc)
        bgs.append(load_bg(cc, sl))
        names.append(name)
        sl_of[name] = sl
    out = pd.DataFrame(orows)
    fo = pd.DataFrame(frows)
    dr = pd.DataFrame(dropped)
    logger.info(f"dev concepts: {len(names)}; dropped: {dr['reason'].str.split(':').str[0].value_counts().to_dict() if len(dr) else {}}")

    # ---------------- stage 1 + stage 2
    t = time.time()
    units, child_mass, s1s = stage1_units(concepts, bgs, n_boot=200)
    logger.info(f"stage 1: {len(units)} concept x field cells with data ({time.time()-t:.0f}s)")
    fit = pool_all(units, names, {})
    feats = concept_features(fit, units, names, child_mass)
    frows_feat = []
    unit_key = {(names[u["ci"]], u["field"]): k for k, u in enumerate(units)}
    all_fields = set(unit_key) | {(r["concept"], r["field"]) for r in frows}
    for (name, fld) in sorted(all_fields):
        ci = names.index(name)
        k = unit_key.get((name, fld))
        val, l = predict(fit, ci, fld, k)
        sd = math.sqrt(max(var_of(fit, l, 0.0 if k is not None else fit.tau_cj ** 2), 0))
        s = s1s[ci]
        j = S2_FIELDS.index(fld)
        frows_feat.append({"concept": name, "field": fld, "rho_star": val, "rho_sd": sd, "has_data": int(k is not None),
                           "rho_hat": units[k]["rho_hat"] if k is not None else np.nan,
                           "v": units[k]["v"] if k is not None else np.nan,
                           "lor_concept_j": float(s.lor_c[j]) if s is not None else np.nan,
                           "bg_LOR_j": float(s.lor_bg[j]) if s is not None else np.nan,
                           "n_child_j": float(s.n_child_j[j]) if s is not None else 0.0})
    ff = pd.DataFrame(frows_feat)

    # ---------------- features table
    frs = []
    n_off_full = {}
    for ci, (name, c) in enumerate(zip(names, concepts)):
        B, has = bgs[ci]
        fo_ = foils(c, B, has)
        n_off = int((c.cH < 0.5).sum()) if len(c.child_idx) else 0
        n_off_full[name] = n_off
        s = s1s[ci]
        frs.append({"concept": name, "dev_group": out.loc[out.concept == name, "dev_group"].iloc[0],
                    "n_papers": len(c.ids), "n_links": len(c.links), "n_children": len(c.child_idx),
                    "n_off_children": n_off, "n_bg_children": int(has.sum()), **feats[name],
                    "A_h_MH": s.A_h_MH if s is not None else np.nan, **fo_})
    feat = pd.DataFrame(frs)

    # ---------------- reliability (split halves) -> eligibility
    rel, rel_n = {}, []
    if args.splits > 0 and names:
        pkl = RES / "_concepts.pkl"
        pkl.write_bytes(pickle.dumps((concepts, bgs, names)))
        t = time.time()
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=mp.get_context("spawn"),
                                 initializer=_init_worker, initargs=(str(pkl),)) as ex:
            split_res = list(ex.map(run_split, range(args.splits)))
        pkl.unlink()
        rel = reliability(split_res, names)
        rel_n = reliability_vs_n(split_res, names, n_off_full)
        logger.info(f"reliability ({args.splits} splits, {time.time()-t:.0f}s): "
                    f"{ {k: v['reliability_SB'] for k, v in rel.items()} }")
    elig_floor = next((b["floor"] for b in rel_n if b["reliability_SB"] is not None and b["reliability_SB"] >= 0.6
                       and all((bb["reliability_SB"] or 0) >= 0.6 for bb in rel_n if bb["floor"] >= b["floor"]
                               and bb["n_concepts"] >= 4)), 30)
    feat["eligible"] = (feat["n_off_children"] >= elig_floor).astype(int)

    # ---------------- screen
    D = out.merge(feat, on=["concept", "dev_group"], how="left")
    D = D[np.isfinite(D["O2r"])].reset_index(drop=True)
    groups = D["dev_group"].values
    XB = np.column_stack([D[B5_COLS].values, D["A_h_missing"].values])
    y = D["O2r"].values
    main_cmp = compare(XB, D[["A_h"]].values, y, groups, "ridge", n_boot=args.n_boot, n_refit=200)
    logger.info(f"O2r Delta-rho = {main_cmp['delta']:.3f} CI90 {np.round(main_cmp['ci90'], 3)} "
                f"(rho_B={main_cmp['metric_B']:.3f}, rho_BC={main_cmp['metric_BC']:.3f}, n={len(y)})")
    res_auc = {}
    for o in ("O1", "O3"):
        res_auc[o] = compare(XB, D[["A_h"]].values, D[o].values.astype(float), groups, "logit", n_boot=args.n_boot)
    hurdle = None
    Dall = out.merge(feat, on=["concept", "dev_group"], how="left")
    if Dall["O2r_hurdle"].nunique() > 1:
        hurdle = compare(np.column_stack([Dall[B5_COLS].values, Dall["A_h_missing"].values]), Dall[["A_h"]].values,
                         Dall["O2r_hurdle"].values.astype(float), Dall["dev_group"].values, "logit", n_boot=args.n_boot)
    # size checks
    size = {"vol": rho(D["A_h"].values, D["B_logvol"].values), "growth": rho(D["A_h"].values, D["B_growth"].values),
            "offhome_vol": rho(D["A_h"].values, D["off_early_vol"].values),
            "offhome_growth": rho(D["A_h"].values, D["off_growth"].values)}
    XB_size = np.column_stack([XB, D[["off_early_vol", "off_growth"]].values])
    size_adj = compare(XB_size, D[["A_h"]].values, y, groups, "ridge", n_boot=args.n_boot)
    # eligible subset + newborn-only sensitivity
    sub_results = {}
    for tag, m in (("eligible", D["eligible"].values == 1), ("newborn_only", D["newborn"].values.astype(bool)),
                   ("full_parent_sample", D["parent_thin"].values <= 1.0001)):
        if m.sum() >= 8 and len(np.unique(groups[m])) >= 2:
            sub_results[tag] = {k: v for k, v in compare(XB[m], D[["A_h"]].values[m], y[m], groups[m], "ridge",
                                                         n_boot=args.n_boot).items() if not k.startswith("oof")}
            sub_results[tag]["n"] = int(m.sum())
        else:
            sub_results[tag] = {"n": int(m.sum()), "note": "too few concepts or groups"}
    # O2r m50 / m20 sensitivity
    sens_m = {}
    for col in ("O2r_m50", "O2r_m20"):
        mm = np.isfinite(D[col].values)
        sens_m[col] = {k: v for k, v in compare(XB[mm], D[["A_h"]].values[mm], D[col].values[mm], groups[mm], "ridge",
                                                n_boot=args.n_boot).items() if not k.startswith("oof")}
    # foils and secondaries as candidates (exploratory comparison table)
    cand_table = {}
    for col in ["A_h", "A_h_u", "n_nat_fields", "max_rho", "A_h_MH", "A_h_crude", "raw_LOR", "bg_LOR", "A_unif",
                "A_imp", "relay_share", "self_share", "coverage", "R_away"]:
        xc = D[[col]].values.astype(float)
        r = compare(XB, xc, y, groups, "ridge", n_boot=args.n_boot)
        cand_table[col] = {"delta_rho": r["delta"], "ci90": r["ci90"], "n_pos_groups": r["n_pos_groups"],
                           "per_group": {g: v["delta"] for g, v in r["per_group"].items()},
                           "spearman_with_O2r": rho(D[col].values, y),
                           "within_group_spearman_O2r": {g: rho(D[col].values[groups == g], y[groups == g])
                                                         for g in np.unique(groups)},
                           "abs_rho_vol": abs(rho(D[col].values, D["B_logvol"].values)),
                           "abs_rho_growth": abs(rho(D[col].values, D["B_growth"].values)),
                           "reliability_SB": (rel.get(col) or {}).get("reliability_SB"),
                           "delta_auc_O1": compare(XB, xc, D["O1"].values.astype(float), groups, "logit", n_boot=200)["delta"],
                           "delta_auc_O3": compare(XB, xc, D["O3"].values.astype(float), groups, "logit", n_boot=200)["delta"]}
    # field-level test
    FL = fo.merge(ff, on=["concept", "field"], how="left")
    field_level = None
    if len(FL) >= 20 and FL["R_j"].nunique() > 1:
        bg = FL["bg_LOR_j"].values.astype(float)
        bg_flag = (~np.isfinite(bg)).astype(float)
        XBf = np.column_stack([FL[["log_n_j_early", "growth_j", "share_j"]].values, bg, bg_flag])
        Xcf = FL[["rho_star", "has_data"]].values.astype(float)
        r = compare(XBf, Xcf, FL["R_j"].values.astype(float), FL["dev_group"].values, "logit", n_boot=args.n_boot,
                    clusters=FL["concept"].values)
        field_level = {"n_units": int(len(FL)), "n_concepts": int(FL["concept"].nunique()),
                       "n_units_with_data": int(FL["has_data"].fillna(0).sum()), "R_j_rate": float(FL["R_j"].mean()),
                       "auc_B": r["metric_B"], "auc_BC": r["metric_BC"], "delta": r["delta"], "ci90": r["ci90"],
                       "per_group": r["per_group"], "n_pos_groups": r["n_pos_groups"]}
        # restricted to units with a stage-1 datum
        m = FL["has_data"].fillna(0).values == 1
        if m.sum() >= 20 and FL.loc[m, "R_j"].nunique() > 1:
            r2 = compare(XBf[m], Xcf[m][:, :1], FL["R_j"].values[m].astype(float), FL["dev_group"].values[m], "logit",
                         n_boot=args.n_boot, clusters=FL["concept"].values[m])
            field_level["with_data_only"] = {"n_units": int(m.sum()), "auc_B": r2["metric_B"], "auc_BC": r2["metric_BC"],
                                             "delta": r2["delta"], "ci90": r2["ci90"], "n_pos_groups": r2["n_pos_groups"]}
    # M1: raw concept LOR vs background LOR
    mm = np.isfinite(feat["raw_LOR_sampled"].values) & np.isfinite(feat["bg_LOR"].values)
    M1 = None
    if mm.sum() >= 5:
        a, b = feat["raw_LOR_sampled"].values[mm], feat["bg_LOR"].values[mm]
        r2 = lambda a_, b_: float(np.corrcoef(a_, b_)[0, 1] ** 2)
        rng = np.random.default_rng(SEED)
        bs = [r2(a[i], b[i]) for i in (rng.integers(0, len(a), len(a)) for _ in range(2000)) if np.std(b[i]) > 0]
        M1 = {"R2": r2(a, b), "ci90": [float(np.percentile(bs, 5)), float(np.percentile(bs, 95))],
              "spearman": rho(a, b), "n": int(mm.sum()), "share_bg_positive": float((b > 0).mean()),
              "share_bg_ge_raw": float((b >= a).mean())}
    # agreement with the probe
    agree = {"spearman_A_h_vs_A_h_crude_all": rho(feat["A_h"].values, feat["A_h_crude"].values)}
    ov = [n for n in PROBE_CRUDE if n in names]
    agree["probe_overlap"] = {n: {"probe_crude": PROBE_CRUDE[n],
                                  "A_h_crude_new": float(feat.loc[feat.concept == n, "A_h_crude"].iloc[0]),
                                  "A_h_new": float(feat.loc[feat.concept == n, "A_h"].iloc[0])} for n in ov}
    if len(ov) >= 3:
        agree["spearman_vs_probe_A_h"] = rho(np.array([PROBE_CRUDE[n] for n in ov]),
                                             np.array([agree["probe_overlap"][n]["A_h_new"] for n in ov]))
        agree["spearman_vs_probe_crude"] = rho(np.array([PROBE_CRUDE[n] for n in ov]),
                                               np.array([agree["probe_overlap"][n]["A_h_crude_new"] for n in ov]))
    # cross-source validation of S0 (OpenAlex topic fields vs S2 fields) where both exist
    xval = None
    if len(oa_rows):
        m = oa_rows.merge(out[["concept", "O2r", "home_s2", "B_entropy"]], on="concept", suffixes=("_oa", "_s2"))
        if len(m) >= 3:
            xval = {"n": int(len(m)), "spearman_O2r": rho(m["O2r_oa"].values, m["O2r_s2"].values),
                    "home_agreement": [{"concept": r["concept"], "home_openalex": r["home"], "home_s2": r["home_s2"]}
                                       for _, r in m.iterrows()]}

    # ---------------- PyMC headline check + GLMM robustness
    pymc_check, glmm = None, None
    if not args.no_pymc and len(units) >= 10:
        try:
            import arviz as az
            y_ = np.array([u["rho_hat"] for u in units]); v_ = np.array([u["v"] for u in units])
            cidx = np.array([u["ci"] for u in units]); fl_ = [u["field"] for u in units]
            t = time.time()
            idata, X_, cols_ = fit_pymc(y_, v_, cidx, len(names), fl_)
            summ = az.summary(idata, var_names=["beta", "tau_c", "tau_cj"])
            post = idata.posterior
            beta_s = post["beta"].values.reshape(-1, X_.shape[1]); u_s = post["u"].values.reshape(-1, len(names))
            w_s = post["w"].values.reshape(-1, len(units))
            mu_s = beta_s @ X_.T + u_s[:, cidx] + w_s
            A_py = {}
            for ci, name in enumerate(names):
                ks = [k for k, u in enumerate(units) if u["ci"] == ci]
                if not ks:
                    continue
                wts = np.array([child_mass[(ci, units[k]["field"])] for k in ks]); wts /= wts.sum()
                A_py[name] = float((mu_s[:, ks] @ wts).mean())
            both = [n for n in A_py if not feat.loc[feat.concept == n, "A_h_missing"].iloc[0]]
            sp = rho(np.array([A_py[n] for n in both]), feat.set_index("concept").loc[both, "A_h"].values)
            rhat = float(np.nanmax(summ["r_hat"].values))
            pymc_check = {"max_rhat": rhat, "spearman_vs_reml": sp, "tau_c_mean": float(post["tau_c"].mean()),
                          "tau_cj_mean": float(post["tau_cj"].mean()), "seconds": time.time() - t,
                          "divergences": int(idata.sample_stats["diverging"].sum()),
                          "pass": bool(rhat < 1.01 and sp >= 0.95)}
            feat["A_h_pymc"] = feat["concept"].map(A_py)
            logger.info(f"PyMC check: {pymc_check}")
        except Exception as e:  # robustness check only; never blocks the screen
            logger.error(f"PyMC check failed: {e!r}")
            pymc_check = {"error": repr(e)[:300]}
    if not args.no_glmm:
        try:
            glmm = glmm_check(concepts, bgs, names)
            feat["A_h_glmm"] = feat["concept"].map(glmm["A_h_glmm"])
            glmm["spearman_vs_primary"] = rho(feat["A_h_glmm"].values.astype(float), feat["A_h"].values)
            glmm.pop("A_h_glmm")
        except Exception as e:
            logger.error(f"GLMM check failed: {e!r}")
            glmm = {"error": repr(e)[:300]}

    # ---------------- rule
    relA = (rel.get("A_h") or {}).get("reliability_SB")
    clauses = {
        "delta_rho_ge_0.10_and_ci_low_gt_0": {"value": [main_cmp["delta"], main_cmp["ci90"]],
                                              "pass": bool(main_cmp["delta"] >= 0.10 and main_cmp["ci90"][0] > 0)},
        "positive_groups_ge_3_of_4": {"value": main_cmp["n_pos_groups"], "pass": bool(main_cmp["n_pos_groups"] >= 3)},
        "reliability_ge_0.6": {"value": relA, "pass": bool(relA is not None and relA >= 0.6)},
        "size_abs_rho_le_0.6": {"value": [size["vol"], size["growth"]],
                                "pass": bool(max(abs(size["vol"]), abs(size["growth"])) <= 0.6)},
    }
    survives = all(v["pass"] for v in clauses.values())
    secondary_rules = {}
    for col in ("n_nat_fields", "max_rho", "A_h_u"):
        ct = cand_table[col]
        rr = (rel.get(col) or {}).get("reliability_SB")
        secondary_rules[col] = {"delta_rho": ct["delta_rho"], "ci90": ct["ci90"], "n_pos_groups": ct["n_pos_groups"],
                                "reliability_SB": rr, "abs_rho_vol": ct["abs_rho_vol"], "abs_rho_growth": ct["abs_rho_growth"],
                                "would_survive_exploratory": bool(ct["delta_rho"] >= 0.1 and ct["ci90"][0] > 0 and
                                                                  ct["n_pos_groups"] >= 3 and rr is not None and rr >= 0.6
                                                                  and max(ct["abs_rho_vol"], ct["abs_rho_growth"]) <= 0.6)}

    # ---------------- outputs
    D["oof_B5"] = main_cmp["oof_B"]; D["oof_B5_plus_A_h"] = main_cmp["oof_BC"]
    credits = pd.read_csv(ROOT / "logs" / "credits.csv")
    deviations = [
        "D1 (plan): availability-cancelling MH table with home children as the control row, not the literal off-home-only GLMM (T0 test ii demonstrates the drift).",
        "D2 (plan): two-stage crossed random-effects pooling (REML-EB via Henderson MME) with PyMC NUTS and a one-stage BinomialBayesMixedGLM as checks.",
        "D8 (new, credit-bound): the shared OpenAlex daily pool (10,000 credits, five artifacts) was at 2,098 at start and fell below the 1,000-credit sibling floor after 139 own credits; OpenAlex S0 is complete only for yearly counts (all 78 concepts) and for field distributions of 11 dev concepts (OpenAlex topic fields). The count-based parts of S0 (t0, newborn, O1, O3, log early volume, early growth) follow S0 exactly.",
        "D9 (new, zero-credit data): concept papers (title/abstract phrase search), their citation lists (lineage links) and field labels come from the Semantic Scholar Graph API. Field labels are fractional memberships over the 23 S2 fields of study (s2-fos-model, a title/abstract text classifier, hence not circular for citation flows) instead of 26-field OpenAlex venue labels; home, dev restriction (sealed = home outside CS/Engineering/Biology/Medicine), O2r, R_j and the field-based B5 terms are computed on these S2 labels for every dev concept, and cross-validated against the OpenAlex S0 where it exists.",
        "D10 (new): background references come from FREE OpenAlex singleton GETs (/works/W<MAG>, cost 0 verified from response headers; the client aborts if a singleton is ever charged) and their fields from S2 via MAG ids.",
        "D4' (plan D4 adapted): all phrase-matched early papers are downloaded (up to 25,000); citation lists are pulled for a seeded uniform sample of at most 1,500 parents per concept (parent_thin), which thins links linearly and cancels in the odds ratios.",
        "D3' (plan D3): local exact/lemma confirmation runs on title + abstract; S2 elides most abstracts, so papers whose abstract is elided and whose title lacks the phrase are kept as 'unverifiable' (S2 phrase index) and only papers with an available abstract lacking the phrase are rejected; exact_share = confirmed/(confirmed+rejected).",
        "D12: O3 = peak count in t0+3..t0+8 >= 2 x mean(t0+7, t0+8) (argmax taken over that range, as in the plan).",
    ]
    screen_result = {
        "candidate": "L_naturalisation_gap", "n_used": int(len(D)), "n_dev_concepts": len(names),
        "n_dropped_by_reason": dr["reason"].str.split(":").str[0].str.split(" ").str[0].value_counts().to_dict() if len(dr) else {},
        "delta_rho": main_cmp["delta"], "ci90": main_cmp["ci90"], "rho_B": main_cmp["metric_B"], "rho_BC": main_cmp["metric_BC"],
        "refit_bootstrap": main_cmp["refit_bootstrap"], "per_group": main_cmp["per_group"],
        "n_pos_groups": main_cmp["n_pos_groups"], "reliability": rel, "reliability_vs_n": rel_n,
        "eligibility_threshold": elig_floor, "eligible_subset_result": sub_results.get("eligible"),
        "sensitivity": {"newborn_only": sub_results.get("newborn_only"), "full_parent_sample": sub_results.get("full_parent_sample"),
                        "O2r_m50": sens_m.get("O2r_m50"), "O2r_m20": sens_m.get("O2r_m20"),
                        "B5_plus_offhome_vol_growth": {k: v for k, v in size_adj.items() if not k.startswith("oof")}},
        "size_corr": size,
        "delta_auc_O1": {k: v for k, v in res_auc["O1"].items() if not k.startswith("oof")},
        "delta_auc_O3": {k: v for k, v in res_auc["O3"].items() if not k.startswith("oof")},
        "outcome_prevalence": {"O1": float(D["O1"].mean()), "O3": float(D["O3"].mean()), "n": int(len(D))},
        "hurdle": {k: v for k, v in hurdle.items() if not k.startswith("oof")} if hurdle else "single class (all N_late >= 30)",
        "field_level": field_level, "M1": M1, "agreement": agree, "s0_cross_source": xval,
        "pooling": {"engine": fit.engine, "tau_c": fit.tau_c, "tau_cj": fit.tau_cj, "beta": dict(zip(fit.fields_x, fit.beta)),
                    "n_cells": len(units)},
        "pymc_check": pymc_check, "glmm_check": glmm,
        "survives": survives, "clause_results": clauses, "secondary_rules_exploratory": secondary_rules,
        "candidate_comparison_table": cand_table,
        "credits_used": int(credits["credits"].sum()), "openalex_calls": int(len(credits)),
        "runtime_s": time.time() - t_start, "deviations": deviations,
    }
    screen_result = jsonable(screen_result)
    out.drop(columns=[]).to_csv(RES / "outcomes.csv", index=False)
    if len(oa_rows):
        oa_rows.drop(columns=["yc"]).to_csv(RES / "outcomes_openalex_s0.csv", index=False)
    fo.to_csv(RES / "field_outcomes.csv", index=False)
    feat.to_csv(RES / "features.csv", index=False)
    ff.to_csv(RES / "field_features.csv", index=False)
    dr.to_csv(RES / "dropped.csv", index=False)
    D.to_csv(RES / "screen_table.csv", index=False)
    (RES / "screen_result.json").write_text(json.dumps(screen_result, indent=1))
    write_method_out(D, FL, screen_result)
    try:
        figures(D, feat, rel_n)
    except Exception as e:
        logger.error(f"figures failed: {e!r}")
    logger.info(f"SURVIVES={survives} clauses={ {k: v['pass'] for k, v in clauses.items()} } "
                f"runtime {time.time()-t_start:.0f}s")


def write_method_out(D: pd.DataFrame, FL: pd.DataFrame, sr: dict) -> None:
    ex = []
    for _, r in D.iterrows():
        inp = {"concept": r["concept"], "t0": int(r["t0"]), "dev_group": r["dev_group"], "home_s2": r["home_s2"],
               "B5": {k: r[k] for k in B5_COLS}, "A_h": r["A_h"], "A_h_sd": r["A_h_sd"],
               "n_off_children": int(r["n_off_children"]), "feature_window": [int(r["t0"]), int(r["t0"]) + 4]}
        e = {"input": json.dumps(jsonable(inp)), "output": f"{r['O2r']:.4f}",
             "predict_baseline_B5": f"{r['oof_B5']:.4f}", "predict_our_method_B5_plus_A_h": f"{r['oof_B5_plus_A_h']:.4f}",
             "metadata_task": "predict rarefied venue-field breadth O2r (m=30) in t0+6..t0+8 from t0..t0+4 features",
             "metadata_fold": r["dev_group"], "metadata_O1": int(r["O1"]), "metadata_O3": int(r["O3"]),
             "metadata_newborn": bool(r["newborn"]), "metadata_eligible": int(r["eligible"])}
        for k in ("A_h", "A_h_u", "A_h_MH", "A_h_crude", "raw_LOR", "bg_LOR", "relay_share", "self_share", "coverage",
                  "R_away", "A_unif", "A_imp", "n_nat_fields", "max_rho", "n_children", "n_links"):
            e[f"metadata_{k}"] = jsonable(r[k])
        ex.append(e)
    fex = []
    for _, r in FL.iterrows():
        fex.append({"input": json.dumps(jsonable({"concept": r["concept"], "field": r["field"], "dev_group": r["dev_group"],
                                                  "log_n_j_early": r["log_n_j_early"], "growth_j": r["growth_j"],
                                                  "share_j": r["share_j"], "bg_LOR_j": r.get("bg_LOR_j")})),
                    "output": str(int(r["R_j"])),
                    "predict_rho_star_cj": f"{r['rho_star']:.4f}" if np.isfinite(r.get("rho_star", np.nan)) else "nan",
                    "metadata_has_data": int(r["has_data"]) if np.isfinite(r.get("has_data", np.nan)) else 0,
                    "metadata_task": "field retention R_j of off-home field j in t0+6..t0+8"})
    mo = {"metadata": {"method_name": "naturalisation gap A*_h (candidate L) screen",
                       "description": "Background-adjusted, field-stratified, partially pooled lineage naturalisation gap vs the common B5 count baseline",
                       "screen_result_summary": {k: sr[k] for k in ("n_used", "delta_rho", "ci90", "rho_B", "rho_BC",
                                                                    "n_pos_groups", "survives", "clause_results",
                                                                    "size_corr", "eligibility_threshold", "credits_used")},
                       "deviations": sr["deviations"]},
          "datasets": [{"dataset": "P78_dev_concepts_O2r", "examples": ex}]}
    if fex:
        mo["datasets"].append({"dataset": "P78_dev_field_retention_units", "examples": fex})
    (ROOT / "method_out.json").write_text(json.dumps(jsonable(mo), indent=1))


def figures(D: pd.DataFrame, feat: pd.DataFrame, rel_n: list[dict]) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig_dir = RES / "figures"
    fig_dir.mkdir(exist_ok=True)
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
    for g, sub in D.groupby("dev_group"):
        ax[0].errorbar(sub["A_h"], sub["O2r"], xerr=sub["A_h_sd"], fmt="o", label=g[:22], alpha=.8)
    ax[0].set_xlabel("A*_h (pooled naturalisation gap)"); ax[0].set_ylabel("O2r (rarefied breadth, m=30)")
    ax[0].legend(fontsize=7)
    m = np.isfinite(feat["bg_LOR"]) & np.isfinite(feat["raw_LOR_sampled"])
    ax[1].scatter(feat.loc[m, "bg_LOR"], feat.loc[m, "raw_LOR_sampled"])
    lim = [min(feat.loc[m, "bg_LOR"].min(), feat.loc[m, "raw_LOR_sampled"].min()), max(feat.loc[m, "bg_LOR"].max(), feat.loc[m, "raw_LOR_sampled"].max())]
    ax[1].plot(lim, lim, "k--", lw=1); ax[1].set_xlabel("background log-OR"); ax[1].set_ylabel("raw concept log-OR (M1)")
    xs = [b["bin"] for b in rel_n]; ys = [b["reliability_SB"] if b["reliability_SB"] is not None else np.nan for b in rel_n]
    ax[2].bar(xs, ys); ax[2].axhline(0.6, color="r", ls="--"); ax[2].set_ylabel("split-half reliability (SB)")
    ax[2].set_xlabel("off-home linked children"); ax[2].set_ylim(-1, 1)
    fig.tight_layout(); fig.savefig(fig_dir / "screen_overview.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    main()
