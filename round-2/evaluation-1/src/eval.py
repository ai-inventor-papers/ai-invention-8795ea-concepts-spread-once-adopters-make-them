#!/usr/bin/env python3
"""Stress test of the gateway-field retention lead (iteration-1 exp4: gateway_j adds ~+0.10 AUC to predicting
field retention R). Zero API calls: reads iteration-1 outputs read-only and writes everything into this workspace.

Blocks: 0 harmonisation + exact reproduction, A replication (refit concept bootstrap), B trait confound (propensity,
field-intercept decomposition, time-varying gateway), C placebos and rival centralities, D O1 artefact re-screen,
E power, F corrected record tables; verdict from the pre-registered ladder in prereg/verdict_ladder.json.

Usage: .venv/bin/python eval.py [--n-boot 2000] [--n-boot-secondary 2000] [--quick]
"""
from __future__ import annotations

import argparse
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
from scipy.stats import norm, spearmanr

HERE = Path(__file__).resolve().parent
(HERE / "logs").mkdir(exist_ok=True)
(HERE / "results" / "cache").mkdir(parents=True, exist_ok=True)
(HERE / "figures").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(HERE / "logs" / "eval.log", rotation="30 MB", level="DEBUG")

import harmonise as H  # noqa: E402
import lib  # noqa: E402
from lib import GROUPS, S4  # noqa: E402

N_WORKERS = 4
SEED = 20260928
RES = HERE / "results"
CACHE = RES / "cache"


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def cached(name: str, fn, use: bool):
    p = CACHE / f"{name}.pkl"
    if use and p.exists():
        logger.info(f"[cache] {name}")
        return pickle.loads(p.read_bytes())
    t = time.time()
    r = fn()
    p.write_bytes(pickle.dumps(r))
    logger.info(f"{name} done in {time.time() - t:.0f}s")
    return r


_EXEC: ProcessPoolExecutor | None = None


def pool_map(fn, jobs: list) -> list:
    """Map over one shared spawn-context process pool (created once to avoid repeated spawn/import cost)."""
    global _EXEC
    if _EXEC is None:
        _EXEC = ProcessPoolExecutor(max_workers=N_WORKERS, mp_context=mp.get_context("spawn"))
    return list(_EXEC.map(fn, jobs))


def chunks(seeds: list[int], k: int) -> list[list[int]]:
    return [list(x) for x in np.array_split(np.array(seeds), k) if len(x)]


def ci(x: np.ndarray) -> dict:
    x = np.asarray([v for v in x if np.isfinite(v)])
    if not len(x):
        return {"n": 0}
    return {"n": int(len(x)), "sd": float(x.std(ddof=1)), "ci90": [float(np.percentile(x, 5)), float(np.percentile(x, 95))],
            "ci95": [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))],
            "p_le0": float(np.mean(x <= 0)), "p_two_sided": float(min(1.0, 2 * min(np.mean(x <= 0), np.mean(x >= 0))))}


def holm(ps: dict[str, float]) -> dict[str, float]:
    items = sorted(ps.items(), key=lambda kv: kv[1])
    m = len(items)
    out, run = {}, 0.0
    for i, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - i) * p))
        out[k] = run
    return out


# ----------------------------------------------------------------------------- spec sets
def spec_set(ds: str, rivals: bool) -> tuple[list, dict]:
    M0 = H.M0 + (["src_exp1", "src_exp3"] if ds in ("union", "union_agree", "new_eps") else [])
    M1 = M0 + H.B5
    M2 = M1 + H.REL + (["bg_LOR_j"] if ds.startswith("exp1") else [])
    g = "gateway_j"
    sp = [("M0", M0, M0 + [g]), ("M1", M1, M1 + [g]), ("M2", M2, M2 + [g]),
          ("M2+P", M2 + ["P_within"], M2 + ["P_within", g]), ("P_alone", M2, M2 + ["P_within"]),
          ("M2+Ppool", M2 + ["P_pooled"], M2 + ["P_pooled", g]), ("Ppool_alone", M2, M2 + ["P_pooled"])]
    if rivals:
        sp += [(f"rival:{r}", M2, M2 + [r]) for r in H.RIVALS if r != "log_field_size"]
        # log_field_size is already inside M2 -> its rival test is M2 without it vs M2
        m2ns = [c for c in M2 if c != "log_field_size"]
        sp += [("rival:log_field_size", m2ns, M2), ("gateway_vs_M2_minus_size", m2ns, m2ns + [g])]
    return sp, {"M0": M0, "M1": M1, "M2": M2}


def run_boot(df: pd.DataFrame, specs: list, n: int, pool: pd.DataFrame, seed: int, stratified: bool = False) -> list:
    seeds = list(range(seed, seed + n))
    jobs = [(df, specs, c, 2.0, pool, stratified) for c in chunks(seeds, N_WORKERS * 4)]
    out = []
    for r in pool_map(lib.boot_worker, jobs):
        out.extend(r)
    return out


def summarise_boot(point: dict, boots: list, specs: list) -> dict:
    res = {}
    for nm, _, _ in specs:
        arr = np.array([b[nm]["delta"] for b in boots], float)
        nd = int(sum(b[nm]["nd"] > 0 for b in boots))
        pg = {lg: ci(np.array([b[nm]["pg"][lg] for b in boots], float)) for lg in GROUPS}
        p = point[nm]
        res[nm] = {"auc_base": p["auc_base"], "auc_cand": p["auc_cand"], "delta": p["delta"],
                   "brier_change": p["brier_cand"] - p["brier_base"],
                   "refit_boot": {**ci(arr), "n_draws": len(boots), "draws_with_single_class_test_group": nd,
                                  "share_single_class_draws": nd / max(1, len(boots))},
                   "per_group": {lg: {**p["per_group"][lg], "boot": pg[lg]} for lg in GROUPS},
                   "n_groups_positive": int(sum(1 for lg in GROUPS if np.isfinite(p["per_group"][lg]["delta"])
                                                and p["per_group"][lg]["delta"] > 0)),
                   "n_groups_evaluable": int(sum(1 for lg in GROUPS if np.isfinite(p["per_group"][lg]["delta"])))}
    return res


def std_coef_boot(df: pd.DataFrame, cols: list[str], target: str, n: int, seed: int) -> dict:
    """Standardised logistic coefficient of `target` in a full-sample fit, concept-clustered bootstrap CI."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    def fit(d):
        X = S4._prep(d[cols], np.ones(len(d), bool))
        X = StandardScaler().fit_transform(X)
        y = d["R"].to_numpy(int)
        if len(np.unique(y)) < 2:
            return math.nan
        return float(LogisticRegression(C=1.0, max_iter=1000).fit(X, y).coef_[0][cols.index(target)])
    b0 = fit(df)
    rng = np.random.default_rng(seed)
    bs = [fit(lib.resample(df, rng)) for _ in range(n)]
    return {"coef_std": b0, **ci(np.array(bs))}


# ----------------------------------------------------------------------------- Block B2 / B3 helpers
def field_effects(df: pd.DataFrame, M1: list[str]) -> pd.DataFrame:
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    X = StandardScaler().fit_transform(S4._prep(df[M1], np.ones(len(df), bool)))
    keys = sorted(df["key"].unique())
    D = (df["key"].to_numpy()[:, None] == np.array(keys)[None, :]).astype(float)
    m = LogisticRegression(C=1.0, max_iter=2000).fit(np.hstack([X, D]), df["R"].to_numpy(int))
    u = m.coef_[0][X.shape[1]:]
    cnt = df["key"].value_counts()
    return pd.DataFrame({"key": keys, "u": u, "n": [int(cnt[k]) for k in keys],
                         "gateway_j": [float(df.loc[df["key"] == k, "gateway_j"].iloc[0]) for k in keys],
                         "log_field_size": [float(df.loc[df["key"] == k, "log_field_size"].iloc[0]) for k in keys]})


def wls_perm(fe: pd.DataFrame, xcol: str, n_perm: int, seed: int) -> dict:
    import statsmodels.api as sm
    f = fe[fe["n"] >= 3].reset_index(drop=True)
    if len(f) < 4:
        return {"n_fields": int(len(f)), "note": "fewer than 4 fields with >= 3 rows"}
    X = sm.add_constant(f[xcol].to_numpy(float))
    r = sm.WLS(f["u"].to_numpy(float), X, weights=f["n"].to_numpy(float)).fit()
    slope = float(r.params[1])
    rng = np.random.default_rng(seed)
    null = []
    for _ in range(n_perm):
        xp = rng.permutation(f[xcol].to_numpy(float))
        null.append(sm.WLS(f["u"].to_numpy(float), sm.add_constant(xp), weights=f["n"].to_numpy(float)).fit().params[1])
    null = np.abs(np.array(null))
    return {"n_fields": int(len(f)), "slope": slope, "slope_se": float(r.bse[1]), "R2": float(r.rsquared),
            "perm_p_two_sided": float((1 + np.sum(null >= abs(slope))) / (1 + n_perm)), "n_perm": n_perm}


def mixed_icc(df: pd.DataFrame, fixed: list[str], vcs: list[str]) -> dict:
    """Latent-scale variance components from statsmodels BinomialBayesMixedGLM (variational Bayes)."""
    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
    from sklearn.preprocessing import StandardScaler
    d = df.copy()
    X = StandardScaler().fit_transform(S4._prep(d[fixed], np.ones(len(d), bool)))
    for i, c in enumerate(fixed):
        d[f"x{i}"] = X[:, i]
    d["concept_id"] = pd.factorize(d["concept"])[0]
    d["key_id"] = pd.factorize(d["key"])[0]
    fml = "R ~ " + " + ".join(f"x{i}" for i in range(len(fixed)))
    vc = {v: f"0 + C({v}_id)" for v in vcs}
    try:
        m = BinomialBayesMixedGLM.from_formula(fml, {k: vc[k] for k in vcs}, d.rename(columns={}), vcp_p=2.0)
        r = m.fit_vb()
    except (ValueError, np.linalg.LinAlgError) as e:
        logger.error(f"mixed GLM failed: {e}")
        return {"error": str(e)}
    sds = np.exp(r.vcp_mean)
    out = {f"tau2_{n}": float(s ** 2) for n, s in zip(m.vcp_names, sds)}
    tot = sum(out.values()) + math.pi ** 2 / 3
    for k in list(out):
        out[f"icc_latent_{k[5:]}"] = out[k] / tot
    return out


def slice_gateways(bb: H.Backbone) -> dict:
    """26-field backbones for exp3 slices 2000-04 and 2005-09 from topic-pair counts (scan/ckpt.npz)."""
    import networkx as nx
    e3 = lib.ITER1 / "gen_art_experiment_3"
    z = np.load(e3 / "scan" / "ckpt.npz")
    tids = json.loads((e3 / "scan" / "topic_ids.json").read_text())
    nt = len(tids)
    tm = pd.read_csv(e3 / "results" / "topic_meta.csv")
    names = pd.read_csv(e3 / "results" / "field_names.csv").set_index("field")["field_name"].to_dict()
    t2f = dict(zip(tm["topic"], tm["field"]))
    fidx = np.array([bb.idx.get(names.get(t2f.get(t, -1), ""), -1) for t in tids])
    Y0 = 1995
    out = {"n_topics": nt, "n_topics_without_field": int((fidx < 0).sum())}
    for s, (ya, yb) in enumerate([(2000, 2004), (2005, 2009)]):
        pk, pc = z[f"pk{s}"], z[f"pc{s}"].astype(np.int64)
        a, b = pk // nt, pk % nt
        fa, fb = fidx[a], fidx[b]
        ok = (fa >= 0) & (fb >= 0)
        C = np.bincount(fa[ok] * 26 + fb[ok], weights=pc[ok], minlength=676).reshape(26, 26)
        C = C + C.T
        np.fill_diagonal(C, np.diag(C) / 2)
        bgs = z["bg"][ya - Y0:yb - Y0 + 1].sum(0)
        nf = np.bincount(fidx[fidx >= 0], weights=bgs[fidx >= 0], minlength=26)
        W = float(z["Gt"][ya - Y0:yb - Y0 + 1].sum())
        with np.errstate(divide="ignore", invalid="ignore"):
            pmi = np.log(C * W / np.outer(nf, nf))
        phi = np.where(np.isfinite(pmi), np.maximum(pmi, 0), 0.0)
        np.fill_diagonal(phi, 0)
        G = nx.Graph()
        G.add_nodes_from(range(26))
        for i in range(26):
            for j in range(i + 1, 26):
                if phi[i, j] > 0:
                    G.add_edge(i, j, weight=phi[i, j])
        eig = nx.eigenvector_centrality_numpy(G, weight="weight")
        gv = np.array([eig[i] for i in range(26)])
        gv = np.abs(gv) / np.abs(gv).max()
        out[f"slice{s}"] = {"years": [ya, yb], "gateway": gv, "n_pos_edges": G.number_of_edges(), "W": W,
                            "spearman_vs_exp4": float(spearmanr(gv, bb.gate).statistic)}
    del z
    return out


# ----------------------------------------------------------------------------- C1 rewiring
def _connected(E: dict, n: int = 26) -> bool:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for a, b in E:
        adj[a].append(b)
        adj[b].append(a)
    seen, stack = {0}, [0]
    while stack:
        for v in adj[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def rewire(edges: dict, rng: np.random.Generator, nswap: int, shuffle_w: bool) -> dict:
    """Degree- and connectivity-preserving double-edge swaps with weights carried by their edges."""
    E = dict(edges)
    keys = list(E)
    done, tries = 0, 0
    while done < nswap and tries < nswap * 50:
        tries += 1
        i1, i2 = rng.choice(len(keys), 2, replace=False)
        (u, v), (x, y) = keys[i1], keys[i2]
        if rng.random() < 0.5:
            x, y = y, x
        if len({u, v, x, y}) < 4:
            continue
        e1, e2 = tuple(sorted((u, x))), tuple(sorted((v, y)))
        if e1 in E or e2 in E:
            continue
        w1, w2 = E.pop(keys[i1]), E.pop(keys[i2])
        E[e1], E[e2] = w1, w2
        if not _connected(E):
            del E[e1], E[e2]
            E[keys[i1]], E[keys[i2]] = w1, w2
            continue
        keys = list(E)
        done += 1
    if shuffle_w:
        ws = rng.permutation(list(E.values()))
        E = dict(zip(E.keys(), ws))
    return E


def eig_from_edges(E: dict) -> np.ndarray:
    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(range(26))
    for (a, b), w in E.items():
        G.add_edge(a, b, weight=w)
    e = nx.eigenvector_centrality_numpy(G, weight="weight")
    v = np.abs(np.array([e[i] for i in range(26)]))
    return v / v.max()


# ----------------------------------------------------------------------------- figures
def figures(A: dict, C: dict, B2: dict, E: dict) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "pdf.fonttype": 42})
    made = []
    # forest
    rows = []
    for ds in ("exp4", "exp1", "exp1_clean", "exp3", "union", "new_eps", "union_agree"):
        if ds not in A:
            continue
        r = A[ds]["specs"]["M2"]
        rows.append((f"{ds} (pooled)", r["delta"], r["refit_boot"].get("ci95", [np.nan, np.nan]), "k"))
        for lg in GROUPS:
            pg = r["per_group"][lg]
            if np.isfinite(pg.get("delta", np.nan) if pg.get("delta") is not None else np.nan):
                c95 = pg["boot"].get("ci95", [np.nan, np.nan])
                rows.append((f"   {ds}:{lg}", pg["delta"], c95, "0.55"))
    re = A.get("random_effects_M2", {})
    fig, ax = plt.subplots(figsize=(6.2, 0.22 * len(rows) + 1.2))
    for i, (lab, d, c, col) in enumerate(rows):
        yy = len(rows) - i
        ax.plot(c, [yy, yy], color=col, lw=1)
        ax.plot(d, yy, "o", color=col, ms=3.5)
    if re.get("pooled") is not None and np.isfinite(re.get("pooled", np.nan)):
        p, s = re["pooled"], re["se"]
        ax.fill([p - 1.96 * s, p, p + 1.96 * s, p], [0, 0.35, 0, -0.35], color="tab:blue")
        rows_l = [r[0] for r in rows] + ["RE pooled (descriptive)"]
        ax.set_yticks(list(range(len(rows), 0, -1)) + [0], rows_l)
    else:
        ax.set_yticks(list(range(len(rows), 0, -1)), [r[0] for r in rows])
    ax.axvline(0, color="r", lw=0.8, ls="--")
    ax.set_xlabel("delta-AUC of gateway_j over M2 (refit concept bootstrap 95% CI)")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(HERE / "figures" / f"forest_delta_auc.{ext}", dpi=200)
    plt.close(fig)
    made.append("figures/forest_delta_auc.png")
    # placebo histograms
    panels = [(k, v) for k, v in C.items() if k.startswith(("C1", "C2")) and isinstance(v, dict) and "null" in v]
    if panels:
        fig, axs = plt.subplots(1, len(panels), figsize=(3.1 * len(panels), 2.6))
        axs = np.atleast_1d(axs)
        for ax, (k, v) in zip(axs, panels):
            ax.hist(v["null"], bins=30, color="0.7")
            ax.axvline(v["real"], color="r")
            ax.set_title(k.replace("_", " "), fontsize=7)
            ax.set_xlabel("delta-AUC")
        fig.tight_layout()
        for ext in ("png", "pdf"):
            fig.savefig(HERE / "figures" / f"placebo_hist.{ext}", dpi=200)
        plt.close(fig)
        made.append("figures/placebo_hist.png")
    # stage-2 scatter
    fe = B2.get("_fe_union")
    if fe is not None:
        f = fe[fe["n"] >= 3]
        fig, ax = plt.subplots(figsize=(4.2, 3.2))
        ax.scatter(f["gateway_j"], f["u"], s=8 + 2 * f["n"], alpha=0.7)
        for _, r in f.iterrows():
            ax.annotate(str(r["key"])[:14], (r["gateway_j"], r["u"]), fontsize=5)
        ax.set_xlabel("gateway_j (eigenvector, 1998-2002 backbone)")
        ax.set_ylabel("field intercept u_j (stage 1, union)")
        fig.tight_layout()
        for ext in ("png", "pdf"):
            fig.savefig(HERE / "figures" / f"stage2_field_intercepts.{ext}", dpi=200)
        plt.close(fig)
        made.append("figures/stage2_field_intercepts.png")
    # MDE curve
    if "analytic" in E:
        fig, ax = plt.subplots(figsize=(4.2, 3.0))
        Ns = np.linspace(300, 6000, 60)
        for m in (5, 10):
            ax.plot(Ns, [E["_mde_fn"](n, m) for n in Ns], label=f"analytic, m={m}")
            sims = [(c["N"], c["mde_sim"]) for c in E.get("simulation", []) if c["m"] == m and c.get("mde_sim")]
            if sims:
                ax.plot(*zip(*sims), "o", ms=4, label=f"simulated, m={m}")
        fre = (E.get("simulation_meta", {}).get("field_RE_sensitivity") or {}).get("cells", [])
        if fre:
            ax.plot([c["N"] for c in fre], [c["mde_sim"] for c in fre], "s--", ms=4, color="k",
                    label="simulated + field RE, m=5")
        ax.axhline(0.05, color="r", ls="--", lw=0.8, label="H1 bar 0.05")
        ax.set_xlabel("episodes N")
        ax.set_ylabel("MDE delta-AUC (80% power, alpha .05)")
        ax.legend(fontsize=6)
        fig.tight_layout()
        for ext in ("png", "pdf"):
            fig.savefig(HERE / "figures" / f"mde_vs_n.{ext}", dpi=200)
        plt.close(fig)
        made.append("figures/mde_vs_n.png")
    return made


# ----------------------------------------------------------------------------- main
@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--n-boot-secondary", type=int, default=2000)
    ap.add_argument("--n-boot-exp4", type=int, default=2000)
    ap.add_argument("--n-boot-D", type=int, default=1000)
    ap.add_argument("--n-boot-F5", type=int, default=1000)
    ap.add_argument("--n-perm", type=int, default=1000)
    ap.add_argument("--n-rewire", type=int, default=200)
    ap.add_argument("--n-sim", type=int, default=500)
    ap.add_argument("--use-cache", action="store_true")
    ap.add_argument("--blocks", default="ABCDEF")
    args = ap.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (20 * 1024 ** 3, 20 * 1024 ** 3))
    t0 = time.time()
    uc = args.use_cache
    missing, deviations = [], []
    for p in [H.E4 / "field_outcomes.csv", H.E4 / "field_backbone.json", H.E4 / "screen_result.json",
              H.E4 / "features.csv", H.E4 / "outcomes.csv", H.E1 / "field_outcomes.csv", H.E1 / "features.csv",
              H.E1 / "outcomes.csv", H.E1 / "field_features.csv", H.E1 / "screen_result.json",
              H.E3 / "field_outcomes.csv", H.E3 / "outcomes.csv", H.E3 / "field_names.csv",
              H.E3 / "screen_result.json", H.E3 / "topic_meta.csv",
              lib.ITER1 / "gen_art_experiment_3" / "scan" / "ckpt.npz",
              lib.ITER1 / "gen_art_experiment_3" / "scan" / "topic_ids.json"]:
        if not p.exists():
            missing.append(str(p.relative_to(lib.ITER1)))
    logger.info(f"missing inputs: {missing}")

    # ------------------------------------------------------------------ Step 0
    data = H.build_all()
    bb = data["bb"]
    d4, W4 = data["exp4"]
    d1, W1 = data["exp1"]
    d3, W3 = data["exp3"]
    u, Wu = data["union"]
    pool = data["pool"]
    u.drop(columns=["cl"]).to_csv(RES / "union_episodes.csv", index=False)
    clean_mask = ~d1["field_s2"].isin(H.XW["crosswalk_clean_sensitivity_drops"]).to_numpy()
    ne_mask = (u["source"] != "exp4").to_numpy()
    ag_mask = (u["R_agrees_all_files"] == 1).to_numpy()
    DS = {"exp4": (d4, W4), "exp1": (d1, W1), "exp1_clean": (d1[clean_mask].reset_index(drop=True), W1[clean_mask]),
          "exp3": (d3, W3), "union": (u, Wu), "new_eps": (u[ne_mask].reset_index(drop=True), Wu[ne_mask]),
          "union_agree": (u[ag_mask].reset_index(drop=True), Wu[ag_mask])}
    for k, (d, _) in DS.items():
        logger.info(f"dataset {k}: rows={len(d)} concepts={d['concept'].nunique()} R-rate={d['R'].mean():.3f} "
                    f"groups={d['group'].value_counts().to_dict()}")

    # exact reproduction of exp4
    fr4 = pd.read_csv(H.E4 / "field_outcomes.csv")
    BF = ["log_n_W3", "growth_j", "share_W3"]
    rep = {"gateway_j": S4.field_level(fr4, BF, BF + ["gateway_j"], n_boot=10)["delta_auc"],
           "size_controlled_gateway_j": S4.field_level(fr4, BF + ["log_field_size"],
                                                       BF + ["log_field_size", "gateway_j"], n_boot=10)["delta_auc"]}
    rep_h = lib.eval_specs(d4, [("g", H.M0, H.M0 + ["gateway_j"]),
                                ("gs", H.M0 + ["log_field_size"], H.M0 + ["log_field_size", "gateway_j"])])
    reproduction = {"reported": {"gateway_j": 0.10254, "size_controlled_gateway_j": 0.10222},
                    "reproduced_from_exp4_file": rep,
                    "reproduced_from_harmonised_panel": {"gateway_j": rep_h["g"]["delta"],
                                                         "size_controlled_gateway_j": rep_h["gs"]["delta"]}}
    ok_rep = abs(rep["gateway_j"] - 0.10254) < 1e-4 and abs(rep["size_controlled_gateway_j"] - 0.10222) < 1e-4 and \
        abs(rep_h["g"]["delta"] - 0.10254) < 1e-4 and abs(rep_h["gs"]["delta"] - 0.10222) < 1e-4
    reproduction["exact_to_1e-4"] = bool(ok_rep)
    logger.info(f"reproduction: {reproduction}")
    if not ok_rep:
        raise RuntimeError(f"exp4 reproduction failed: {reproduction}")

    fast_eq = {}
    for ds, (d, _) in DS.items():
        cols = spec_set(ds, False)[1]["M2"]
        tr = (d["group"] != "CS").to_numpy()
        a1, a2 = lib._ORIG_PREP(d[cols], tr), lib.fast_prep(d[cols], tr)
        oof = S4.logo_predict(d, cols, "R", "logit")
        fast_eq[ds] = {"prep_maxabs": float(np.abs(a1 - a2).max()),
                       "auc_diff": float(abs(lib._ORIG_AUC(d["R"].to_numpy(float), oof) -
                                             lib.fast_auc(d["R"].to_numpy(float), oof)))}
        assert fast_eq[ds]["prep_maxabs"] < 1e-12 and fast_eq[ds]["auc_diff"] < 1e-12, fast_eq
    logger.info(f"fast-path equivalence: {fast_eq}")
    reproduction["fast_path_equivalence"] = fast_eq

    # ------------------------------------------------------------------ Block A (+B1 +C3 share the resamples)
    A: dict = {}
    pointres: dict = {}
    for i, ds in enumerate(DS):
        d, _ = DS[ds]
        rivals = ds in ("exp4", "union", "new_eps")
        specs, fams = spec_set(ds, rivals)
        nb = args.n_boot if ds in ("union", "new_eps") else (args.n_boot_exp4 if ds == "exp4" else args.n_boot_secondary)

        def job(d=d, specs=specs, nb=nb, i=i):
            pt = lib.eval_specs(d, specs, 2.0, pool, keep_oof=True)
            bs = run_boot(d, specs, nb, pool, SEED + 100000 * i)
            share1 = np.mean([b["M2"]["nd"] > 0 for b in bs])
            strat = None
            if share1 > 0.05:
                strat = run_boot(d, specs, nb, pool, SEED + 100000 * i + 50000, stratified=True)
            return pt, bs, strat
        pt, bs, strat = cached(f"A_{ds}_{nb}", job, uc)
        pointres[ds] = pt
        res = summarise_boot(pt, strat if strat is not None else bs, specs)
        A[ds] = {"n_rows": int(len(d)), "n_concepts": int(d["concept"].nunique()), "prevalence": float(d["R"].mean()),
                 "mean_episodes_per_concept": float(len(d) / d["concept"].nunique()),
                 "rows_per_group": d["group"].value_counts().to_dict(), "feature_sets": fams, "n_boot": nb,
                 "bootstrap_scheme": "stratified-by-group concept resampling (single-class draws > 5%)"
                 if strat is not None else "concept-clustered refit bootstrap", "specs": res}
        if strat is not None:
            A[ds]["unstratified_M2_ci95"] = summarise_boot(pt, bs, specs)["M2"]["refit_boot"].get("ci95")
        # P sensitivity to shrinkage a
        sens = {}
        for a_ in (0.0, 5.0):
            r = lib.eval_specs(d, [s for s in specs if s[0] in ("M2+P", "P_alone")], a_, pool)
            sens[f"a={a_:g}"] = {k: {"delta": v["delta"], "auc_base": v["auc_base"], "auc_cand": v["auc_cand"]}
                                 for k, v in r.items()}
        A[ds]["P_shrinkage_sensitivity"] = sens
        # descriptives
        A[ds]["spearman_gateway_with"] = {c: float(spearmanr(d["gateway_j"], d[c]).statistic)
                                          for c in ("log_field_size", "phi_home_j", "density_j")}
        m2 = specs[2][1]
        A[ds]["std_coef_gateway_in_M2"] = cached(f"coef_{ds}", lambda d=d, m2=m2: std_coef_boot(
            d, m2 + ["gateway_j"], "gateway_j", 1000 if ds in ("union", "new_eps", "exp4") else 300, SEED + i), uc)
        # correlation gateway vs P across fields (full-data leave-concept-out P, a=2)
        Pw = lib.propensity(d["key"].to_numpy(), d["concept"].to_numpy(), d["R"].to_numpy(float),
                            d["group"].to_numpy(), "__none__", 2.0)
        A[ds]["spearman_gateway_vs_P_rows"] = float(spearmanr(d["gateway_j"], Pw).statistic)
        byf = pd.DataFrame({"k": d["key"], "g": d["gateway_j"], "P": Pw}).groupby("k").mean()
        A[ds]["spearman_gateway_vs_P_fields"] = float(spearmanr(byf["g"], byf["P"]).statistic) if len(byf) > 3 else None
        r = res["M2"]
        logger.info(f"A {ds}: M2 delta={r['delta']:.4f} ci95={r['refit_boot'].get('ci95')} "
                    f"groups+={r['n_groups_positive']}/{r['n_groups_evaluable']}; +P delta={res['M2+P']['delta']:.4f} "
                    f"P alone={res['P_alone']['delta']:.4f}")
    # random-effects pooling over the three dataset estimates (descriptive)
    est = [A[k]["specs"]["M2"]["delta"] for k in ("exp4", "exp1", "exp3")]
    var = [A[k]["specs"]["M2"]["refit_boot"]["sd"] ** 2 for k in ("exp4", "exp1", "exp3")]
    A["random_effects_M2"] = {**S4.dersimonian_laird(est, var), "datasets": ["exp4", "exp1", "exp3"],
                              "label": "DESCRIPTIVE: concepts overlap across files; union-panel refit CI is inferential"}
    est0 = [A[k]["specs"]["M0"]["delta"] for k in ("exp4", "exp1", "exp3")]
    var0 = [A[k]["specs"]["M0"]["refit_boot"]["sd"] ** 2 for k in ("exp4", "exp1", "exp3")]
    A["random_effects_M0"] = {**S4.dersimonian_laird(est0, var0), "label": "DESCRIPTIVE"}

    # ------------------------------------------------------------------ Block B2 / B3
    B: dict = {"B1_propensity": {ds: {k: A[ds]["specs"][k] | {"per_group": None} for k in
                                      ("M2+P", "P_alone", "M2+Ppool", "Ppool_alone")} for ds in DS}}
    B["B1_note"] = ("P_within: leave-concept-out, training-fold-only shrunken field retention mean (a=2); P_pooled: same "
                    "from the rows of all three files, excluding the concept and the test group everywhere; exp1 "
                    "one-to-many rows enter with their own S2 key.")
    B2: dict = {"static_FE_note": "gateway_j is one number per field -> perfectly collinear with field dummies; a static "
                                  "field-FE test of gateway_j is unidentifiable by construction."}
    for ds in ("exp4", "exp1", "exp3", "union", "new_eps"):
        d, _ = DS[ds]
        M1 = spec_set(ds, False)[1]["M1"]
        fe = field_effects(d, M1)
        B2[ds] = {"stage2_gateway": wls_perm(fe, "gateway_j", 2000, SEED), "stage2_log_field_size":
                  wls_perm(fe, "log_field_size", 2000, SEED + 1),
                  "field_effects": fe.to_dict(orient="records")}
        if ds == "union":
            B2["_fe_union"] = fe
        if ds in ("exp4", "union"):
            def icc_job(d=d, M1=M1):
                return {"field_and_concept_M1": mixed_icc(d, M1, ["key", "concept"]),
                        "field_and_concept_M1_plus_gateway": mixed_icc(d, M1 + ["gateway_j"], ["key", "concept"]),
                        "field_only_M1": mixed_icc(d, M1, ["key"]),
                        "field_only_M1_plus_gateway": mixed_icc(d, M1 + ["gateway_j"], ["key"])}
            ic = cached(f"icc_{ds}", icc_job, uc)
            try:
                t_a = ic["field_and_concept_M1"]["tau2_key"]
                t_b = ic["field_and_concept_M1_plus_gateway"]["tau2_key"]
                ic["share_tau2_field_removed_by_gateway"] = 1 - t_b / t_a if t_a > 0 else None
            except KeyError:
                ic["share_tau2_field_removed_by_gateway"] = None
            B2[ds]["icc"] = ic
        logger.info(f"B2 {ds}: slope={B2[ds]['stage2_gateway'].get('slope')} R2={B2[ds]['stage2_gateway'].get('R2')} "
                    f"p={B2[ds]['stage2_gateway'].get('perm_p_two_sided')}")
    B["B2_field_intercepts"] = B2
    # B3
    B3: dict = {}
    if any("ckpt.npz" in m or "topic_ids" in m for m in missing):
        B3 = {"status": "SKIPPED", "reason": "exp3 scan files missing"}
    else:
        sg = cached("slice_gateways", lambda: slice_gateways(bb), uc)
        v0 = sg["slice0"]["spearman_vs_exp4"]
        B3["validation_gate"] = {"spearman_slice2000_04_vs_exp4": v0, "threshold": 0.7, "pass": bool(v0 >= 0.7),
                                 "slice_spearman_2000_04_vs_2005_09": float(spearmanr(sg["slice0"]["gateway"],
                                                                                      sg["slice1"]["gateway"]).statistic),
                                 "n_pos_edges": [sg["slice0"]["n_pos_edges"], sg["slice1"]["n_pos_edges"]],
                                 "note": "if the gate fails, both slices use the exp3-built series (always the case "
                                         "here: both slices are built from exp3's counts)"}
        B3["gateway_by_slice"] = {bb.fields[i]: [float(sg["slice0"]["gateway"][i]), float(sg["slice1"]["gateway"][i])]
                                  for i in range(26)}
        d = u.copy()
        sl = np.where(d["t0"] <= 2005, 0, 1)
        d["slice"] = sl
        gmat = np.vstack([sg["slice0"]["gateway"], sg["slice1"]["gateway"]])
        d["gateway_slice"] = [Wu[r] @ gmat[s] for r, s in enumerate(sl)]
        fm = d.groupby("key")["gateway_slice"].transform("mean")
        sd_w = float((d["gateway_slice"] - fm).std())
        sd_b = float(fm.std())
        both = d.groupby("key")["slice"].nunique()
        n_both = int((both == 2).sum())
        ratio = sd_w / sd_b if sd_b > 0 else math.nan
        B3["identifiability_gate"] = {"SD_within": sd_w, "SD_between": sd_b, "ratio": ratio, "ratio_threshold": 0.10,
                                      "n_fields_with_rows_in_both_slices": n_both, "fields_threshold": 8,
                                      "rows_per_slice": d["slice"].value_counts().to_dict()}
        if not (ratio >= 0.10 and n_both >= 8):
            B3["status"] = "NOT IDENTIFIABLE on iteration-1 data (passes to the iteration-2 common-panel experiment)"
        else:
            from sklearn.linear_model import LogisticRegression
            from sklearn.preprocessing import StandardScaler
            M1 = spec_set("union", False)[1]["M1"]

            def fe_coef(dd):
                X = StandardScaler().fit_transform(S4._prep(dd[M1 + ["gateway_slice"]], np.ones(len(dd), bool)))
                keys = sorted(dd["key"].unique())
                D = (dd["key"].to_numpy()[:, None] == np.array(keys)[None, :]).astype(float)
                y = dd["R"].to_numpy(int)
                if len(np.unique(y)) < 2:
                    return math.nan
                return float(LogisticRegression(C=1.0, max_iter=2000).fit(np.hstack([X, D]), y).coef_[0][len(M1)])
            b0 = fe_coef(d)
            rng = np.random.default_rng(SEED + 7)
            bs = [fe_coef(lib.resample(d, rng)) for _ in range(args.n_boot)]
            perm = []
            for _ in range(1000):
                dp = d.copy()
                # shuffle slice labels within field -> reassign gateway_slice from the permuted slice
                sp_ = dp.groupby("key")["slice"].transform(lambda s: rng.permutation(s.to_numpy()))
                dp["gateway_slice"] = [Wu[r] @ gmat[s] for r, s in enumerate(sp_.to_numpy())]
                perm.append(fe_coef(dp))
            perm = np.abs(np.array(perm))
            B3["status"] = "IDENTIFIABLE (gates passed)"
            B3["fe_model"] = {"coef_std_gateway_slice": b0, **ci(np.array(bs)),
                              "perm_p_two_sided_within_field_slice_shuffle":
                                  float((1 + np.sum(perm >= abs(b0))) / (1 + len(perm)))}
        logger.info(f"B3: {B3.get('status')} gates={B3['identifiability_gate']} val={v0:.3f}")
    B["B3_time_varying"] = B3

    # ------------------------------------------------------------------ Block C
    C: dict = {}
    G = bb.graph()
    edges = {tuple(sorted((a, b))): w["weight"] for a, b, w in G.edges(data=True)}
    for variant in ("carried", "weights_shuffled"):
        def c1_job(variant=variant):
            rng = np.random.default_rng(SEED + (1 if variant == "carried" else 2))
            vecs = []
            while len(vecs) < args.n_rewire:
                E = rewire(edges, rng, 10 * len(edges), variant == "weights_shuffled")
                try:
                    vecs.append(eig_from_edges(E))
                except Exception as e:  # noqa: BLE001  eigen solver failure -> redraw with a new seed
                    logger.warning(f"eig failed on rewired graph ({e}); redrawing")
            return vecs
        vecs = cached(f"C1_vecs_{variant}_{args.n_rewire}", c1_job, uc)
        rho = np.array([spearmanr(bb.gate, v).statistic for v in vecs])
        for ds in ("exp4", "union"):
            d, W = DS[ds]
            fams = spec_set(ds, False)[1]
            nulls = cached(f"C1_{variant}_{ds}_{args.n_rewire}", lambda d=d, W=W, fams=fams, vecs=vecs: [
                x for part in pool_map(lib.perm_worker, [(d, W, {"M0": fams["M0"], "M2": fams["M2"]}, list(c))
                                                          for c in np.array_split(np.array(vecs), N_WORKERS * 2)])
                for x in part], uc)
            for mdl in ("M0", "M2"):
                real = A[ds]["specs"][mdl]["delta"]
                nl = np.array([x[mdl] for x in nulls])
                C[f"C1_rewired_{variant}_{ds}_{mdl}"] = {
                    "real": real, "null": nl, "null_median": float(np.median(nl)),
                    "null_p95": float(np.percentile(nl, 95)), "real_percentile": float(np.mean(nl < real) * 100),
                    "p_empirical": float((1 + np.sum(nl >= real)) / (1 + len(nl))), "n_draws": int(len(nl))}
        C[f"C1_discrimination_{variant}"] = {
            "median_spearman_real_vs_rewired": float(np.median(rho)), "p05": float(np.percentile(rho, 5)),
            "p95": float(np.percentile(rho, 95)),
            "flag": ("degree-preserving rewiring cannot separate eigenvector position from degree on a 26-node graph"
                     if np.median(rho) > 0.8 else "placebo discriminates (median rho <= 0.8)")}
        logger.info(f"C1 {variant}: median rho={np.median(rho):.3f}")
    rng = np.random.default_rng(SEED + 3)
    perms = [rng.permutation(bb.gate) for _ in range(args.n_perm)]
    for ds in ("exp4", "union", "new_eps"):
        d, W = DS[ds]
        fams = spec_set(ds, False)[1]
        nulls = cached(f"C2_{ds}_{args.n_perm}", lambda d=d, W=W, fams=fams: [
            x for part in pool_map(lib.perm_worker, [(d, W, {"M2": fams["M2"]}, list(c))
                                                      for c in np.array_split(np.array(perms), N_WORKERS * 3)])
            for x in part], uc)
        nl = np.array([x["M2"] for x in nulls])
        real = A[ds]["specs"]["M2"]["delta"]
        C[f"C2_label_perm_{ds}_M2"] = {"real": real, "null": nl, "null_median": float(np.median(nl)),
                                       "null_p95": float(np.percentile(nl, 95)),
                                       "real_percentile": float(np.mean(nl < real) * 100),
                                       "p_empirical": float((1 + np.sum(nl >= real)) / (1 + len(nl))),
                                       "n_perm": int(len(nl))}
        logger.info(f"C2 {ds}: real={real:.4f} null p95={np.percentile(nl, 95):.4f}")
    # C3 rivals
    C3 = {}
    for ds in ("exp4", "union", "new_eps"):
        sp = A[ds]["specs"]
        tab = {"gateway_j": {k: sp["M2"][k] for k in ("delta", "auc_base", "auc_cand")} | {"ci95": sp["M2"]["refit_boot"].get("ci95"),
                                                                                           "p_two_sided": sp["M2"]["refit_boot"].get("p_two_sided")}}
        for r in H.RIVALS:
            s = sp[f"rival:{r}"]
            tab[r] = {"delta": s["delta"], "auc_base": s["auc_base"], "auc_cand": s["auc_cand"],
                      "ci95": s["refit_boot"].get("ci95"), "p_two_sided": s["refit_boot"].get("p_two_sided")}
        hp = holm({k: v["p_two_sided"] for k, v in tab.items() if v["p_two_sided"] is not None})
        for k in tab:
            tab[k]["p_holm"] = hp.get(k)
        tab["_note"] = ("log_field_size row = M2 without log_field_size vs M2 (size is part of M2); "
                        f"gateway without size control: {sp['gateway_vs_M2_minus_size']['delta']:.4f}")
        C3[ds] = {"n_boot": A[ds]["n_boot"], "table": tab}
    vecs = {k: v for k, v in bb.rivals.items()}
    names = list(vecs)
    C3["spearman_matrix_26_fields"] = {"names": names, "matrix": [[float(spearmanr(vecs[a], vecs[b]).statistic)
                                                                   for b in names] for a in names]}
    C["C3_rivals"] = C3

    # ------------------------------------------------------------------ Block D
    def block_d():
        ft = pd.read_csv(H.E4 / "features.csv")
        oc = pd.read_csv(H.E4 / "outcomes.csv")[["concept", "O1"]].rename(columns={"O1": "O1_oc"})
        df = ft.merge(oc, on="concept", how="left")
        assert np.allclose(df["O1"].fillna(-1), df["O1_oc"].fillna(-1)), "O1 mismatch features vs outcomes"
        df = df.dropna(subset=["O1"]).reset_index(drop=True)
        df["cl"] = np.arange(len(df))
        B5c = ["log_count_W5", "growth_W5_B5", "offhome_share_W3", "entropy_W3", "reach_W3"]
        variants = ["G", "G_all", "G_deg", "G_btw", "G_phimin", "G_A", "REL_home", "DOM_Social"]
        specs = []
        for v in variants:
            miss = f"_miss_{v}"
            df[miss] = df[v].isna().astype(int)
            extra = [v] + ([miss] if df[miss].any() else [])
            for bn, base in (("B5", B5c), ("B5+cov", B5c + ["label_coverage_early"]),
                             ("B5+cov+O1base", B5c + ["label_coverage_early", "O1_base"])):
                specs.append((f"{v}|{bn}", base, base + extra))
        pt = lib.concept_specs_eval(df, specs)
        seeds = list(range(SEED + 9000, SEED + 9000 + args.n_boot_D))
        bs = [x for part in pool_map(lib.concept_boot_worker, [(df, specs, c) for c in chunks(seeds, N_WORKERS * 2)])
              for x in part]
        return df, specs, pt, bs
    D: dict = {}
    if "D" in args.blocks:
        dfD, specsD, ptD, bsD = cached(f"D_{args.n_boot_D}", block_d, uc)
        s4 = json.loads((H.E4 / "screen_result.json").read_text())
        for nm, _, _ in specsD:
            v, bn = nm.split("|")
            arr = np.array([b[nm] for b in bsD])
            D.setdefault(v, {})[bn] = {**ptD[nm], **{k: x for k, x in ci(arr).items()},
                                       "n_groups_positive": int(sum(1 for x in ptD[nm]["per_group"].values()
                                                                    if np.isfinite(x) and x > 0))}
        for v in D:
            rep_v = (s4["secondary_screens"].get(v, {}).get("O1", {}) or {}).get("delta") if v != "G" else \
                s4["delta_auc_O1"]["delta"]
            D[v]["reported_iter1_delta"] = rep_v
            D[v]["reproduces_iter1"] = bool(rep_v is not None and abs(rep_v - D[v]["B5"]["delta"]) < 1e-6)
            d0, d2 = D[v]["B5"]["delta"], D[v]["B5+cov+O1base"]["delta"]
            d1_ = D[v]["B5+cov"]["delta"]
            art = lambda dd, c90: bool((d0 > 0) and (dd <= 0.5 * d0) and c90[0] <= 0 <= c90[1])  # noqa: E731
            D[v]["artefact_cov"] = art(d1_, D[v]["B5+cov"].get("ci90", [0, 0]))
            D[v]["artefact_cov_O1base"] = art(d2, D[v]["B5+cov+O1base"].get("ci90", [0, 0]))
            x = dfD[v].to_numpy(float)
            cov = dfD["label_coverage_early"].to_numpy(float)
            y = dfD["O1"].to_numpy(float)
            ok = np.isfinite(x) & np.isfinite(cov)
            D[v]["spearman_with_label_coverage"] = float(spearmanr(x[ok], cov[ok]).statistic)
            rx, rc, ry = [pd.Series(a[ok]).rank().to_numpy() for a in (x, cov, y)]
            ex_ = rx - np.polyval(np.polyfit(rc, rx, 1), rc)
            ey_ = ry - np.polyval(np.polyfit(rc, ry, 1), rc)
            D[v]["partial_spearman_with_O1_given_coverage"] = float(np.corrcoef(ex_, ey_)[0, 1])
            D[v]["spearman_with_O1"] = float(spearmanr(x[ok], y[ok]).statistic)
        D["_n_concepts"] = int(len(dfD))
        D["_n_boot"] = args.n_boot_D
        logger.info("D: " + "; ".join(f"{v}: {D[v]['B5']['delta']:.3f}->{D[v]['B5+cov+O1base']['delta']:.3f}"
                                      for v in D if not v.startswith("_")))

    # ------------------------------------------------------------------ Block E power
    E: dict = {}
    du = DS["union"][0]
    m2u = spec_set("union", False)[1]["M2"]
    se_boot = A["union"]["specs"]["M2"]["refit_boot"]["sd"]
    N0, nc0 = len(du), du["concept"].nunique()
    m0 = N0 / nc0
    # ICC of R within concept: latent-scale concept random intercept (M2 fixed) and ANOVA on Pearson residuals
    icc_c = cached("icc_concept_union", lambda: mixed_icc(du, m2u, ["concept"]), uc)
    rho_latent = icc_c.get("icc_latent_concept", math.nan)
    oofm = pointres["union"]["M2"]["oof_cand"]
    pr = (du["R"].to_numpy() - oofm) / np.sqrt(np.clip(oofm * (1 - oofm), 1e-6, None))
    grp = pd.Series(pr).groupby(du["concept"].to_numpy())
    k = grp.size()
    msb = (k * (grp.mean() - pr.mean()) ** 2).sum() / (len(k) - 1)
    msw = ((pr - grp.transform("mean").to_numpy()) ** 2).sum() / (len(pr) - len(k))
    n_bar = (len(pr) - (k ** 2).sum() / len(pr)) / (len(k) - 1)
    rho_anova = float(max(0.0, (msb - msw) / (msb + (n_bar - 1) * msw)))
    rho_c = rho_latent if np.isfinite(rho_latent) else rho_anova
    DE = lambda m: 1 + (m - 1) * rho_c  # noqa: E731
    se_fn = lambda N, m: se_boot * math.sqrt((N0 / DE(m0)) / (N / DE(m)))  # noqa: E731
    mde_fn = lambda N, m: (1.96 + 0.84) * se_fn(N, m)  # noqa: E731
    shrunk = A["union"]["specs"]["M2"]["refit_boot"]["ci90"][0]
    E["inputs"] = {"SE_boot_union_M2": se_boot, "N0_rows": N0, "n_concepts": nc0, "m0": m0,
                   "rho_c_latent": rho_latent, "rho_c_anova_pearson": rho_anova, "rho_c_used": rho_c,
                   "rho_c_source": "latent" if np.isfinite(rho_latent) else "anova",
                   "shrunken_effect_lower90_union": shrunk, "H1_bar": 0.05}
    E["analytic"] = [{"N": N, "m": m, "DE": DE(m), "SE": se_fn(N, m), "MDE_80": mde_fn(N, m),
                      "power_at_0.05": float(norm.cdf(0.05 / se_fn(N, m) - 1.96)),
                      "power_at_shrunken": float(norm.cdf(max(shrunk, 0) / se_fn(N, m) - 1.96))}
                     for N in (1000, 2000, 4000) for m in (5, 10)]
    E["_mde_fn"] = mde_fn

    def sim_job():
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        cols = m2u + ["gateway_j"]
        X = S4._prep(du[cols], np.ones(len(du), bool))
        sc = StandardScaler().fit(X)
        mdl = LogisticRegression(C=1.0, max_iter=2000).fit(sc.transform(X), du["R"].to_numpy(int))
        beta = mdl.coef_[0] / sc.scale_
        b0 = mdl.intercept_[0] - np.sum(mdl.coef_[0] * sc.mean_ / sc.scale_)
        sig = math.sqrt(rho_c * (math.pi ** 2 / 3) / (1 - rho_c)) if 0 < rho_c < 1 else 0.0
        gi = len(cols) - 1
        sg_, mg_ = float(X[:, gi].std()), float(X[:, gi].mean())

        def with_bstd(bstd):
            bb_ = beta.copy()
            bb_[gi] = bstd / sg_
            return b0 + (beta[gi] - bb_[gi]) * mg_, bb_

        keyc = pd.factorize(du["key"])[0]

        def run(bstd, N, m, n, base_seed, tau_f=0.0):
            b0_, be_ = with_bstd(bstd)
            seeds = list(range(base_seed, base_seed + n))
            return np.array([x for part in pool_map(lib.sim_worker, [(X, b0_, be_, gi, sig, N, m, list(c), keyc, tau_f)
                                                                     for c in chunks(seeds, N_WORKERS * 2)])
                             for x in part])
        # calibrate the standardised gateway coefficient that yields a true grouped-CV delta-AUC of 0.05
        grid = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
        pil = {b: float(run(b, 2000, 5, 48, SEED + 31 + int(b * 100) * 1000).mean()) for b in grid}
        xs, ys = np.array(grid), np.array([pil[b] for b in grid])
        order = np.argsort(ys)
        b_star = float(np.interp(0.05, ys[order], xs[order]))
        logger.info(f"E calibration: {pil} -> b_std*={b_star:.3f}")
        out = []
        for N in (1000, 2000, 4000):
            for m in (5, 10):
                nul = run(0.0, N, m, args.n_sim, SEED + N * 10 + m)
                alt = run(b_star, N, m, args.n_sim, SEED + N * 10 + m + 500000)
                crit = float(np.percentile(nul, 95))
                out.append({"N": N, "m": m, "n_sims_null": int(len(nul)), "n_sims_alt": int(len(alt)),
                            "SD_null": float(nul.std(ddof=1)), "crit95_null": crit,
                            "mean_delta_alt": float(alt.mean()), "SD_alt": float(alt.std(ddof=1)),
                            "power_at_0.05_sim": float(np.mean(alt > crit)),
                            "mde_sim": float(crit + 0.84 * alt.std(ddof=1)),
                            "power_at_0.05_normal_approx": float(norm.cdf((alt.mean() - crit) / alt.std(ddof=1)))})
                logger.info(f"E sim N={N} m={m}: crit={crit:.4f} alt mean={alt.mean():.4f} sd={alt.std(ddof=1):.4f} "
                            f"power={np.mean(alt > crit):.3f}")
        # sensitivity: add a field random intercept with the union field variance (field-only M1 model, B2)
        tau_f = math.sqrt(max(tau2_field_union, 0.0))
        pil_f = {b: float(run(b, 2000, 5, 48, SEED + 77 + int(b * 100) * 1000, tau_f).mean()) for b in grid}
        ysf = np.array([pil_f[b] for b in grid])
        of = np.argsort(ysf)
        b_star_f = float(np.interp(0.05, ysf[of], xs[of]))
        out_f = []
        for N in (1000, 2000, 4000):
            for m in (5,):
                nul = run(0.0, N, m, args.n_sim, SEED + N * 10 + m + 7, tau_f)
                alt = run(b_star_f, N, m, args.n_sim, SEED + N * 10 + m + 500007, tau_f)
                crit = float(np.percentile(nul, 95))
                out_f.append({"N": N, "m": m, "SD_null": float(nul.std(ddof=1)), "crit95_null": crit,
                              "mean_delta_alt": float(alt.mean()), "SD_alt": float(alt.std(ddof=1)),
                              "power_at_0.05_sim": float(np.mean(alt > crit)),
                              "mde_sim": float(crit + 0.84 * alt.std(ddof=1))})
                logger.info(f"E sim fieldRE N={N} m={m}: crit={crit:.4f} alt mean={alt.mean():.4f} "
                            f"sd={alt.std(ddof=1):.4f} power={np.mean(alt > crit):.3f}")
        return {"sigma_concept": sig, "fitted_std_coef_gateway_union": float(mdl.coef_[0][gi]),
                "field_RE_sensitivity": {"tau_field": tau_f, "tau2_source": "union field-only M1 random intercept (B2)",
                                         "calibration_pilot": pil_f, "b_std_for_delta_0.05": b_star_f,
                                         "cells": out_f},
                "calibration_pilot_mean_delta_by_bstd": pil, "b_std_for_delta_0.05": b_star, "cells": out}
    tau2_field_union = B2["union"]["icc"]["field_only_M1"].get("tau2_key", 0.0)
    if "E" in args.blocks:
        sim = cached(f"E_sim_fieldRE_{args.n_sim}", sim_job, uc)
        E["simulation"] = sim["cells"]
        E["simulation_meta"] = {k: v for k, v in sim.items() if k != "cells"} | {
            "note": "episodes simulated from the fitted union M2+gateway logit with a concept random intercept matched "
                    "to rho_c; covariates resampled from union rows; 4-fold GroupKFold by concept. The gateway "
                    "coefficient is set to 0 (null) or to the calibrated value giving a true delta-AUC of 0.05 (alt); "
                    "power = P(alt delta > 95th pct of null); MDE_sim = crit95_null + 0.84 x SD_alt (one-sided 5%). "
                    "The shrunken estimate (union lower 90% bound) is <= 0, so power at it equals the test size.",
            "power_at_shrunken": "not applicable: shrunken effect <= 0" if shrunk <= 0 else None}
    # held-out sizing per group
    hs = {}
    p_needed = None
    for p in np.linspace(0.5, 0.999, 2000):
        if 4 * p ** 3 * (1 - p) + p ** 4 >= 0.8:
            p_needed = float(p)
            break
    zz = {"p>=0.9": norm.ppf(0.9), f"p>={p_needed:.3f} (3 of 4 >= 0.8)": norm.ppf(p_needed)}
    for lg in GROUPS:
        pg = A["union"]["specs"]["M2"]["per_group"][lg]
        sd_g = pg["boot"].get("sd")
        n_g = int(du.loc[du["group"] == lg, "concept"].nunique())
        row = {"n_concepts_dev": n_g, "SE_group_refit": sd_g, "delta_group": pg["delta"]}
        if sd_g and np.isfinite(sd_g):
            for tgt_nm, tgt in (("0.05", 0.05), ("shrunken", max(shrunk, 1e-3))):
                for zk, z in zz.items():
                    row[f"concepts_needed_{zk}_at_{tgt_nm}"] = int(math.ceil(n_g * (z * sd_g / tgt) ** 2))
        hs[lg] = row
    # supplementary sizing from the simulated SD under the alternative (field-RE variant, N=1000, m=5 -> 200 concepts):
    # per-group SE(n_g) ~= SD_alt * sqrt(200 / n_g)  =>  n_g = 200 * (z * SD_alt / 0.05)^2
    sup = {}
    fre = (E.get("simulation_meta", {}).get("field_RE_sensitivity") or {}).get("cells", [])
    base_cell = next((c for c in fre if c["N"] == 1000 and c["m"] == 5), None)
    if base_cell:
        for zk, z in zz.items():
            sup[f"concepts_per_group_{zk}_at_0.05"] = int(math.ceil(200 * (z * base_cell["SD_alt"] / 0.05) ** 2))
        sup["SD_alt_field_RE_N1000_m5"] = base_cell["SD_alt"]
    E["held_out_sizing_from_alternative_SD"] = {**sup, "note": "the plan's per-group refit SEs are measured at a "
                                                "near-zero observed effect, where delta-AUC barely moves, so they "
                                                "understate the SE under the alternative; this supplementary sizing "
                                                "uses the simulated SD under a true delta of 0.05 with field and concept "
                                                "random intercepts"}
    E["held_out_sizing"] = {"per_group": hs, "p_per_group_needed_for_3of4_ge_0.8": p_needed,
                            "assumption": "independent groups; per-group SE scales as 1/sqrt(concepts) from the union "
                                          "per-group refit-bootstrap SD"}

    # ------------------------------------------------------------------ Block F
    s1 = json.loads((H.E1 / "screen_result.json").read_text())
    s3 = json.loads((H.E3 / "screen_result.json").read_text())
    s4 = json.loads((H.E4 / "screen_result.json").read_text())
    f1 = pd.read_csv(H.E1 / "features.csv")
    F = {"F1_rho_B5": {"ci_convention": "point estimates as reported (LOGO OOF Spearman); no CI",
                       "exp1": {"rho_B5": s1["rho_B"], "per_group": {k: {"n": v["n"], "rho_B5": v["metric_B"]}
                                                                     for k, v in s1["per_group"].items()}},
                       "exp3": {"rho_B5": s3["base_metrics"]["O2r"], "n_per_group": s3["n_per_group"]},
                       "exp4": {"rho_B5": s4["delta_rho_O2r_m30"]["base"],
                                "per_group": {k: {"n": v["n"], "rho_B5": v["base"]}
                                              for k, v in s4["delta_rho_O2r_m30"]["per_group"].items()}}},
         "F2_A_star_h": {"ci_convention": "median and IQR across concepts (no CI)",
                         "per_group": {g: {"n": int(x["A_h"].notna().sum()), "median": float(x["A_h"].median()),
                                           "q25": float(x["A_h"].quantile(0.25)), "q75": float(x["A_h"].quantile(0.75))}
                                       for g, x in f1.groupby("dev_group")}},
         "F3_exp3_portability": {"ci_convention": "as stored in exp3 screen_result.json['portability'] (point "
                                                  "Spearman within group; LOGO delta-rho without CI)",
                                 "table": s3["portability"]},
         "F4_exp4_secondary_screens": {"ci_convention": "iteration-1 row-bootstrap of FIXED OOF predictions (90%)",
                                       "table": s4["secondary_screens"],
                                       "flag_ci90_wholly_below_0": [k for k, v in s4["secondary_screens"].items()
                                                                    if isinstance(v, dict) and "O2r_m30" in v and
                                                                    v["O2r_m30"]["ci90"][1] < 0],
                                       "O3_note": "O3 not evaluable (2 positives)"}}
    F["F2_A_star_h"]["n_groups_negative_median"] = int(sum(v["median"] < 0 for v in F["F2_A_star_h"]["per_group"].values()))
    fl4 = s4["field_level"]
    newci = {"all_four_available": None, "size_controlled_all_three": None, "gateway_j": A["exp4"]["specs"]["M0"],
             "size_controlled_gateway_j": None}
    # refit CIs for the exact exp4 field-level feature lists (method.py lines 317-326)
    f5_specs = [("all_four_available", H.M0, H.M0 + ["gateway_j", "phi_home_j", "density_j"]),
                ("size_controlled_all_three", H.M0 + ["log_field_size"],
                 H.M0 + ["log_field_size", "gateway_j", "phi_home_j", "density_j"]),
                ("gateway_j", H.M0, H.M0 + ["gateway_j"]),
                ("size_controlled_gateway_j", H.M0 + ["log_field_size"], H.M0 + ["log_field_size", "gateway_j"]),
                ("phi_home_j", H.M0, H.M0 + ["phi_home_j"]), ("density_j", H.M0, H.M0 + ["density_j"]),
                ("log_field_size_alone_added", H.M0, H.M0 + ["log_field_size"])]
    f5 = cached(f"F5_{args.n_boot_F5}", lambda: (lib.eval_specs(d4, f5_specs, 2.0, pool),
                                                 run_boot(d4, f5_specs, args.n_boot_F5, pool, SEED + 777)), uc)
    f5s = summarise_boot(f5[0], f5[1], f5_specs)
    F["F5_exp4_field_level"] = {"ci_convention": "iter-1: fixed-prediction concept bootstrap 95%; new: concept-clustered "
                                                 "REFIT bootstrap 95%",
                                "feature_lists": {n: {"base": b, "cand": c} for n, b, c in f5_specs},
                                "rows": {n: {"iter1_delta": fl4[n]["delta_auc"], "iter1_ci95_fixed": fl4[n]["ci95"],
                                             "new_delta": f5s[n]["delta"], "new_ci95_refit": f5s[n]["refit_boot"].get("ci95"),
                                             "new_ci90_refit": f5s[n]["refit_boot"].get("ci90")} for n, _, _ in f5_specs}}
    del newci

    # ------------------------------------------------------------------ verdict
    un, ne = A["union"]["specs"], A["new_eps"]["specs"]
    c2u = C["C2_label_perm_union_M2"]
    cond = {"new_eps_delta_gt_0": ne["M2"]["delta"] > 0,
            "union_delta_gt_0_ci95_gt_0": un["M2"]["delta"] > 0 and un["M2"]["refit_boot"]["ci95"][0] > 0,
            "new_eps_delta_gt_0_ci95_gt_0": ne["M2"]["delta"] > 0 and ne["M2"]["refit_boot"]["ci95"][0] > 0,
            "union_ge3of4_groups_positive": un["M2"]["n_groups_positive"] >= 3,
            "survives_P_within_union_ci95_gt_0": un["M2+P"]["refit_boot"]["ci95"][0] > 0,
            "above_C2_p95_union": c2u["real"] > c2u["null_p95"],
            "P_alone_carries_gain_union": un["P_alone"]["delta"] > 0 and un["P_alone"]["refit_boot"]["ci95"][0] > 0,
            "gateway_adds_le_0.01_given_P_union": un["M2+P"]["delta"] <= 0.01,
            "inside_C2_null_union": c2u["real"] <= c2u["null_p95"]}
    cond = {k: bool(v) for k, v in cond.items()}
    if not cond["new_eps_delta_gt_0"]:
        verdict = "FAILS"
    elif (cond["P_alone_carries_gain_union"] and cond["gateway_adds_le_0.01_given_P_union"]) or cond["inside_C2_null_union"]:
        verdict = "FIELD-TRAIT"
    elif all(cond[k] for k in ("union_delta_gt_0_ci95_gt_0", "new_eps_delta_gt_0_ci95_gt_0",
                                "union_ge3of4_groups_positive", "survives_P_within_union_ci95_gt_0",
                                "above_C2_p95_union")):
        verdict = "REPLICATES"
    elif un["M2"]["delta"] > 0 and ne["M2"]["delta"] > 0:
        verdict = "ATTENUATES"
    else:
        verdict = "FAILS"
    logger.info(f"VERDICT: {verdict}  {cond}")

    # ------------------------------------------------------------------ deviations
    deviations += [
        "metrics_agg must be flat numbers under the exp_eval_sol_out schema: the plan's table keys (A_replication, "
        "B_trait, C_placebo, D_O1_artefact, E_power, F_record, overlap, verdict, missing_inputs, deviations) live in "
        "metadata; headline numbers are flattened into metrics_agg.",
        "density_j for exp1/exp3 rows uses early field presence approximated by home field(s) + fields with a retention "
        "row (>=5 early papers); exp4's own density_j (>=2 labelled papers) is kept for exp4 rows. Approximation vs "
        f"exp4's own: Spearman {data['checks']['exp4_recompute']['density_j_rows_approx_vs_exp4']['spearman']:.3f}.",
        "Union/new-episodes panels add source dummies (src_exp1, src_exp3) to M0 because R prevalence differs by label "
        "source (exp4 0.56, exp3 0.69, exp1 0.75).",
        "exp1 one-to-many S2 rows (Biology, Geography) are de-duplicated on their first mapped OpenAlex field and keep "
        "their own key 'S2:<field>' for field propensity and field effects; within-exp1 many-to-one duplicates keep "
        "the row with the largest early count.",
        f"{data['overlap']['union']['n_rows_regrouped_for_concept_consistency']} union rows were re-assigned to their "
        "concept's highest-priority-source home group so that no concept is split across LOGO folds.",
        "crosswalk-clean sensitivity also drops Philosophy, History and Art (many-to-one -> Arts and Humanities) under "
        "the stated rule.",
        "exp1 M2 includes bg_LOR_j (missing for 80 rows, training-fold median imputed as in screen._prep).",
        "B3 slice backbones use topic-PAIR counts over each work's first 3 topics (exp3 scan) aggregated to fields and "
        "per-topic tag totals as marginals, whereas exp4's backbone used work-level field co-assignment; the "
        "validation gate measures comparability.",
        "Holm correction uses two-sided refit-bootstrap p-values (2 x min(P(delta<=0), P(delta>=0))).",
        "Block C1/C2 recompute only point estimates (as planned); P-based and rival models share the Block A resamples.",
        "Block E uses the latent-scale concept ICC from BinomialBayesMixedGLM (variational Bayes) when available, else "
        "the ANOVA estimator on Pearson residuals; both are reported.",
    ]
    deviations.append(
        f"Scaling rule applied (host load average ~180 on a shared 4-CPU container made a draw cost 1-1.7 s): refit "
        f"bootstrap draws = {args.n_boot} for union and new-episodes panels, {args.n_boot_exp4} for exp4, "
        f"{args.n_boot_secondary} for exp1, exp1_clean, exp3 and union_agree (incl. their C3 rival CIs where run), "
        f"{args.n_boot_D} for Block D and {args.n_boot_F5} for the F5 refit CIs; {args.n_sim} simulations per cell and "
        "condition in Block E.")
    deviations.append("screen._prep is replaced at runtime by a numerically identical numpy version and pooled/group "
                      "AUCs use a rank (Mann-Whitney) AUC with screen._auc's conventions; equivalence is checked on "
                      "every dataset before Block A (metadata.fast_path_equivalence).")

    # ------------------------------------------------------------------ figures + outputs
    figs = figures(A, C, B2, E)
    E.pop("_mde_fn", None)
    B2.pop("_fe_union", None)
    Cout = {k: ({kk: vv for kk, vv in v.items() if kk != "null"} | ({"null_summary": ci(v["null"])} if "null" in v else {}))
            if isinstance(v, dict) else v for k, v in C.items()}

    def examples(ds: str) -> list[dict]:
        d = DS[ds][0]
        pt = pointres[ds]["M2"]
        ex = []
        for i, r in d.reset_index(drop=True).iterrows():
            inp = {"concept": r["concept"], "group": r["group"], "field_key": r["key"], "source": r["source"],
                   "t0": None if pd.isna(r["t0"]) else int(r["t0"]),
                   **{c: (None if pd.isna(r[c]) else float(r[c])) for c in H.M0 + H.B5 + H.REL + ["gateway_j"]}}
            pb, pc = float(pt["oof_base"][i]), float(pt["oof_cand"][i])
            y = float(r["R"])
            ex.append({"input": json.dumps(inp), "output": str(int(y)),
                       "predict_M2": f"{pb:.6f}", "predict_M2_plus_gateway": f"{pc:.6f}",
                       "metadata_concept": r["concept"], "metadata_group": r["group"],
                       "metadata_fold": f"leave-out-{r['group']}", "metadata_source": r["source"],
                       "metadata_field_key": r["key"],
                       "eval_brier_M2": (pb - y) ** 2, "eval_brier_M2_plus_gateway": (pc - y) ** 2,
                       "eval_logloss_M2": float(-(y * math.log(max(pb, 1e-9)) + (1 - y) * math.log(max(1 - pb, 1e-9)))),
                       "eval_logloss_M2_plus_gateway": float(-(y * math.log(max(pc, 1e-9)) +
                                                               (1 - y) * math.log(max(1 - pc, 1e-9))))})
        return ex

    ma = {"verdict_code": {"REPLICATES": 3, "ATTENUATES": 2, "FIELD-TRAIT": 1, "FAILS": 0}[verdict],
          "exp4_reproduced_delta_gateway": rep["gateway_j"], "exp4_reproduced_delta_size_controlled":
              rep["size_controlled_gateway_j"]}
    for ds in DS:
        for sp_ in ("M0", "M1", "M2", "M2+P", "P_alone", "M2+Ppool", "Ppool_alone"):
            s = A[ds]["specs"][sp_]
            tag = f"{ds}_{sp_.replace('+', '_plus_')}"
            ma[f"A_{tag}_delta_auc"] = s["delta"]
            if s["refit_boot"].get("ci95"):
                ma[f"A_{tag}_ci95_lo"], ma[f"A_{tag}_ci95_hi"] = s["refit_boot"]["ci95"]
        ma[f"A_{ds}_M2_auc_base"] = A[ds]["specs"]["M2"]["auc_base"]
        ma[f"A_{ds}_M2_n_groups_positive"] = A[ds]["specs"]["M2"]["n_groups_positive"]
        ma[f"A_{ds}_n_rows"] = A[ds]["n_rows"]
        ma[f"A_{ds}_std_coef_gateway_M2"] = A[ds]["std_coef_gateway_in_M2"]["coef_std"]
    for k in ("pooled", "I2", "tau2"):
        ma[f"A_RE_M2_{k}"] = A["random_effects_M2"].get(k)
    for ds in ("exp4", "exp1", "exp3", "union", "new_eps"):
        sg = B2[ds]["stage2_gateway"]
        for k in ("slope", "R2", "perm_p_two_sided"):
            if sg.get(k) is not None:
                ma[f"B2_{ds}_stage2_gateway_{k}"] = sg[k]
    if "identifiability_gate" in B3:
        ma["B3_sd_ratio_within_between"] = B3["identifiability_gate"]["ratio"]
        ma["B3_validation_spearman"] = B3["validation_gate"]["spearman_slice2000_04_vs_exp4"]
    for k, v in Cout.items():
        if isinstance(v, dict) and "p_empirical" in v:
            ma[f"{k}_p"] = v["p_empirical"]
            ma[f"{k}_real_percentile"] = v["real_percentile"]
        if isinstance(v, dict) and "median_spearman_real_vs_rewired" in v:
            ma[f"{k}_median_rho"] = v["median_spearman_real_vs_rewired"]
    for ds in ("exp4", "union", "new_eps"):
        for r, v in C3[ds]["table"].items():
            if isinstance(v, dict):
                ma[f"C3_{ds}_{r}_delta_auc"] = v["delta"]
                if v.get("p_holm") is not None:
                    ma[f"C3_{ds}_{r}_p_holm"] = v["p_holm"]
    for v, x in D.items():
        if not v.startswith("_"):
            for bn in ("B5", "B5+cov", "B5+cov+O1base"):
                ma[f"D_{v}_{bn.replace('+', '_plus_')}_delta_auc"] = x[bn]["delta"]
            ma[f"D_{v}_artefact"] = int(x["artefact_cov_O1base"])
    for c in E["analytic"]:
        ma[f"E_analytic_MDE_N{c['N']}_m{c['m']}"] = c["MDE_80"]
    for c in E.get("simulation", []):
        ma[f"E_sim_MDE_N{c['N']}_m{c['m']}"] = c["mde_sim"]
        ma[f"E_sim_power005_N{c['N']}_m{c['m']}"] = c["power_at_0.05_sim"]
    ma["E_rho_c"] = rho_c
    for c in (E.get("simulation_meta", {}).get("field_RE_sensitivity") or {}).get("cells", []):
        ma[f"E_simFieldRE_MDE_N{c['N']}_m{c['m']}"] = c["mde_sim"]
        ma[f"E_simFieldRE_power005_N{c['N']}_m{c['m']}"] = c["power_at_0.05_sim"]
        ma[f"E_simFieldRE_crit95null_N{c['N']}_m{c['m']}"] = c["crit95_null"]
    ma = {k.replace("-", "_").replace(":", "_").replace(".", "_"): float(v) for k, v in ma.items()
          if v is not None and np.isfinite(float(v))}

    meta = {"evaluation_name": "Stress-testing the gateway-field retention lead",
            "description": "Zero-credit re-evaluation of iteration-1 field-retention files: replication, trait confound, "
                           "placebos, O1 artefact, power and corrected record tables.",
            "unit": "adoption episode (concept c, off-home field j); resampling unit = concept",
            "ci_convention": "all NEW CIs: concept-clustered REFIT bootstrap (percentile); iteration-1 CIs are labelled",
            "prereg": {"verdict_ladder": json.loads((HERE / "prereg" / "verdict_ladder.json").read_text()),
                       "crosswalk": H.XW},
            "reproduction": reproduction, "harmonisation_checks": data["checks"],
            "overlap": data["overlap"], "A_replication": A, "B_trait": B, "C_placebo": Cout, "D_O1_artefact": D,
            "E_power": E, "F_record": F, "verdict": {"verdict": verdict, "conditions": cond},
            "missing_inputs": missing, "deviations": deviations, "figures": figs,
            "runtime_s": round(time.time() - t0, 1)}
    out = {"metadata": clean(meta), "metrics_agg": ma,
           "datasets": [{"dataset": f"field_retention_{ds}_LOGO_M2_vs_M2_plus_gateway", "examples": examples(ds)}
                        for ds in ("union", "exp4", "exp1", "exp3")]}
    (HERE / "eval_out.json").write_text(json.dumps(out, indent=1))
    (RES / "summary.json").write_text(json.dumps(clean({"verdict": verdict, "conditions": cond,
                                                         "headline": {ds: {k: A[ds]["specs"]["M2"][k] for k in
                                                                           ("delta", "auc_base", "auc_cand",
                                                                            "n_groups_positive")} |
                                                                      {"ci95": A[ds]["specs"]["M2"]["refit_boot"].get("ci95")}
                                                                      for ds in DS}}), indent=1))
    logger.info(f"wrote eval_out.json ({len(ma)} metrics) in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
