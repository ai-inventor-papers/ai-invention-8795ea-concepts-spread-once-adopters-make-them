"""H2 next-field entry: field-year state machine, concept-year risk sets, conditional-logit blocks, AUCs, placebos."""
from __future__ import annotations

import math

import networkx as nx
import numpy as np
import pandas as pd
from scipy import stats

from cfg_exp6 import Y0
from stats_core import CLogit, fe_ols

REG = ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d0_ret_rel", "d_ret_gate"]
MODELS = {"M0": ["a_phi_home", "b_log_size", "c_density", "e_gate_own"],
          "M1": ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d0_ret_rel"],
          "M2": ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d_ret_gate"],
          "M3": ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d0_ret_rel", "d_ret_gate"],
          "M2lost": ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d_lost_gate"]}


def states(g: np.ndarray, home: list[int], min_n: int = 2) -> dict:
    """g: [NY, 27] grounded counts. Returns boolean [NY, 26] matrices (years Y0..)."""
    x = g[:, 1:]
    cum = np.cumsum(x, 0)
    entered = cum >= min_n
    w3 = x.copy()
    w3[1:] += x[:-1]; w3[2:] += x[:-2]
    ent_lag2 = np.zeros_like(entered); ent_lag2[2:] = entered[:-2]
    offhome = np.ones(26, bool)
    for h in home:
        offhome[h - 11] = False
    retaining = ent_lag2 & (w3 >= min_n) & offhome[None, :]
    lost = entered & (w3 == 0)
    return {"entered": entered, "retaining": retaining, "lost": lost, "w3": w3, "cum": cum, "offhome": offhome}


def rca_entered(g: np.ndarray, GF: np.ndarray) -> np.ndarray:
    """entry when cumulative count >= 2 and the field's cumulative share of the concept exceeds its share of all works."""
    x = np.cumsum(g[:, 1:], 0)
    tot = x.sum(1, keepdims=True)
    F = np.cumsum(GF, 0)
    share_all = F / np.maximum(F.sum(1, keepdims=True), 1)
    share_c = x / np.maximum(tot, 1)
    ok = (x >= 2) & (share_c > share_all)
    return np.maximum.accumulate(ok.astype(int), 0).astype(bool)


def build_risk_sets(frame: pd.DataFrame, G: dict[int, np.ndarray], bb: dict, GF: np.ndarray,
                    entry_def: str = "count", horizon: int = 8) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """Rows = (concept, year t, candidate field k not entered by t-1, not home). Returns df, Ret matrix, Lost matrix."""
    phi, gate = bb["phi"], bb["g"]
    colsum = phi.sum(0)
    logGF = np.log(np.maximum(GF, 1))
    rows, RET, LOST = [], [], []
    for r in frame.itertuples():
        c = int(r.cidx); t0 = int(r.t0)
        home = [int(h) for h in str(r.home).split("|")]
        S = states(G[c], home)
        ent = rca_entered(G[c], GF) if entry_def == "rca" else S["entered"]
        hidx = [h - 11 for h in home]
        a = phi[hidx].mean(0)
        for t in range(t0 + 1, min(t0 + horizon, 2022) + 1):
            ti = t - Y0
            E = ent[ti - 1]
            cand = ~E & S["offhome"]
            if not cand.any():
                continue
            ev = ent[ti] & cand
            Ret = S["retaining"][ti - 1]
            Lost = S["lost"][ti - 1] & S["offhome"]
            dens = (phi[E].sum(0)) / np.where(colsum > 0, colsum, 1)
            d0 = phi[Ret].mean(0) if Ret.any() else np.zeros(26)
            d = (gate[Ret] @ phi[Ret]) / gate[Ret].sum() if Ret.any() and gate[Ret].sum() > 0 else np.zeros(26)
            dl = (gate[Lost] @ phi[Lost]) / gate[Lost].sum() if Lost.any() and gate[Lost].sum() > 0 else np.zeros(26)
            for k in np.nonzero(cand)[0]:
                rows.append((c, t, t - t0, k + 11, int(ev[k]), a[k], logGF[ti - 1, k], dens[k], gate[k], d0[k], d[k], dl[k],
                             int(Ret.sum()), int(Lost.sum()), r.group, r.split, int(r.intersection_born), float(r.home_gateway)))
                RET.append(Ret); LOST.append(Lost)
    df = pd.DataFrame(rows, columns=["cidx", "t", "age", "field", "entered", "a_phi_home", "b_log_size", "c_density",
                                     "e_gate_own", "d0_ret_rel", "d_ret_gate", "d_lost_gate", "n_ret", "n_lost", "group",
                                     "split", "intersection_born", "home_gateway"])
    df["stratum"] = df.cidx.astype(np.int64) * 100 + (df.t - 2000)
    return df, np.array(RET, bool).reshape(-1, 26), np.array(LOST, bool).reshape(-1, 26)


def standardise(df: pd.DataFrame, spec: dict | None, cols: list[str]) -> tuple[pd.DataFrame, dict]:
    if spec is None:
        spec = {c: {"mean": float(df[c].mean()), "sd": float(df[c].std() or 1.0)} for c in cols}
    out = df.copy()
    for c in cols:
        out[c] = (df[c] - spec[c]["mean"]) / (spec[c]["sd"] if spec[c]["sd"] > 0 else 1.0)
    return out, spec


def fit_model(df: pd.DataFrame, cols: list[str], ridge: float = 0.0) -> dict:
    m = CLogit(df[cols].to_numpy(), df.entered.to_numpy(), df.stratum.to_numpy(), ridge=ridge).fit()
    return {"coef": dict(zip(cols, map(float, m["coef"]))), "se": dict(zip(cols, map(float, m["se"]))), "ll": m["ll"],
            "n_strata": m["n_strata"], "n_events": m.get("n_events", 0), "n_rows": m.get("n_rows", 0),
            "converged": m["converged"], "_b": m["coef"]}


def lr_test(big: dict, small: dict, df_: int) -> dict:
    lr = 2 * (big["ll"] - small["ll"])
    return {"LR": float(lr), "df": df_, "p": float(stats.chi2.sf(max(lr, 0), df_))}


def within_auc(df: pd.DataFrame, score: np.ndarray) -> pd.Series:
    """mean-rank AUC per informative stratum."""
    d = pd.DataFrame({"s": df.stratum.to_numpy(), "y": df.entered.to_numpy(), "x": score})
    d["r"] = d.groupby("s").x.rank(method="average")
    g = d.groupby("s").agg(ntot=("y", "size"), nev=("y", "sum"))
    re = d[d.y == 1].groupby("s").r.sum()
    g = g.join(re.rename("rs")).fillna({"rs": 0})
    g = g[(g.nev > 0) & (g.nev < g.ntot)]
    nn = g.ntot - g.nev
    return (g.rs - g.nev * (g.nev + 1) / 2) / (g.nev * nn)


def concept_boot_mean(series: pd.Series, n_boot: int, rng) -> list[float]:
    """series indexed by stratum id (cidx*100 + ...): concept-clustered bootstrap CI of the mean."""
    cid = (series.index.to_numpy() // 100)
    u, inv = np.unique(cid, return_inverse=True)
    sums = np.bincount(inv, weights=series.to_numpy()); cnts = np.bincount(inv)
    bs = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(u), len(u))
        bs.append(sums[pick].sum() / max(cnts[pick].sum(), 1))
    return [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]


def boot_coef(df: pd.DataFrame, cols: list[str], target: str, n_boot: int, rng, small_cols: list[str] | None = None) -> dict:
    """concept-clustered bootstrap of a clogit coefficient (and the LR vs small model if given)."""
    cids = df.cidx.unique()
    by = {c: ix for c, ix in df.groupby("cidx").indices.items()}
    X = df[cols].to_numpy(); y = df.entered.to_numpy(); st = df.stratum.to_numpy()
    Xs = df[small_cols].to_numpy() if small_cols else None
    bs, lrs = [], []
    for b in range(n_boot):
        pick = rng.choice(cids, len(cids))
        idx = np.concatenate([by[c] for c in pick])
        rep = np.repeat(np.arange(len(pick)), [len(by[c]) for c in pick])
        s2 = st[idx] * 10000 + rep  # relabel strata of repeated concepts
        m = CLogit(X[idx], y[idx], s2).fit()
        bs.append(m["coef"][cols.index(target)])
        if small_cols:
            ms = CLogit(Xs[idx], y[idx], s2).fit()
            lrs.append(2 * (m["ll"] - ms["ll"]))
    bs = np.array(bs)
    out = {"ci": [float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))], "se_boot": float(np.nanstd(bs)),
           "n_boot": n_boot}
    if small_cols:
        out["lr_boot"] = [float(x) for x in np.percentile(lrs, [5, 25, 50, 75, 95])]
        out["_lrs"] = np.array(lrs)
    return out


def recompute_d(RET: np.ndarray, fields: np.ndarray, phi: np.ndarray, gate: np.ndarray) -> np.ndarray:
    k = fields - 11
    w = RET * gate[None, :]
    den = w.sum(1)
    num = (w * phi[:, k].T).sum(1)
    return np.where(den > 0, num / np.where(den > 0, den, 1), 0.0)


def eig_gateway(phi: np.ndarray) -> np.ndarray:
    Gx = nx.from_numpy_array(phi)
    try:
        ev = nx.eigenvector_centrality_numpy(Gx, weight="weight")
    except Exception:  # noqa: BLE001 -- disconnected graph after rewiring: fall back to power iteration
        ev = nx.eigenvector_centrality(Gx, weight="weight", max_iter=2000)
    v = np.array([ev[i] for i in range(len(phi))])
    v = np.abs(v)
    return v / v.max()


def rewire(phi: np.ndarray, rng) -> np.ndarray:
    """degree-preserving double-edge swaps on the phi>0 graph; original weights reassigned at random to the new edges."""
    Gx = nx.Graph()
    Gx.add_nodes_from(range(len(phi)))
    iu = np.transpose(np.nonzero(np.triu(phi, 1) > 0))
    Gx.add_edges_from(map(tuple, iu))
    ne = Gx.number_of_edges()
    try:
        nx.double_edge_swap(Gx, nswap=10 * ne, max_tries=1000 * ne, seed=int(rng.integers(1 << 31)))
    except nx.NetworkXAlgorithmError:
        pass
    w = phi[iu[:, 0], iu[:, 1]].copy()
    rng.shuffle(w)
    P = np.zeros_like(phi)
    for (i, j), wt in zip(Gx.edges(), w):
        P[i, j] = P[j, i] = wt
    return P
