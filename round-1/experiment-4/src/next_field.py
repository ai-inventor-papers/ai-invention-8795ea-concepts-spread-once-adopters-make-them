"""Relatedness-density next-field entry test (Hidalgo et al. 2007 principle of relatedness) vs a field-size baseline."""
from __future__ import annotations

import math
from collections import Counter

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from statsmodels.discrete.conditional_models import ConditionalLogit


def density(K: set[int], phi: np.ndarray) -> np.ndarray:
    den = phi.sum(axis=0)
    num = phi[list(K), :].sum(axis=0) if K else np.zeros(phi.shape[0])
    return np.where(den > 0, num / np.where(den > 0, den, 1), 0.0)


def build_rows(concepts: dict, bb) -> pd.DataFrame:
    """Steps: 'short' = A (t0..t0+1) -> t0+2 (cumulative >= 2 papers); 'long' = W3 -> outcome window (>= 3 papers)."""
    rows = []
    for nm, r in concepts.items():
        w = r.get("windows") or {}
        A, B, D = w.get("A"), w.get("B"), w.get("D")
        if not A or not B:
            continue
        cA = Counter(A["fields"])
        cW3 = cA + Counter(B["fields"])
        home_idx = [bb.idx[h] for h in r["home"] if h in bb.idx]
        steps = [("short", {bb.idx[f] for f, n in cA.items() if n >= 2},
                  lambda k: cW3.get(bb.fields[k], 0) >= 2)]
        if D:
            cD = Counter(D["fields"])
            steps.append(("long", {bb.idx[f] for f, n in cW3.items() if n >= 2},
                          lambda k, cD=cD: cD.get(bb.fields[k], 0) >= 3))
        for step, K, entered in steps:
            if not K:
                continue
            dens = density(K, bb.phi)
            for k in range(26):
                if k in K:
                    continue
                rows.append({"concept": nm, "group": r["group"], "step": step, "cs": f"{nm}|{step}",
                             "field": bb.fields[k], "k": k, "entered": int(entered(k)), "density": dens[k],
                             "log_size": bb.logsize[k],
                             "phi_home": float(np.mean([bb.phi[h, k] for h in home_idx])) if home_idx else 0.0})
    return pd.DataFrame(rows)


def per_cs_auc(df: pd.DataFrame, col: str) -> pd.Series:
    out = {}
    for cs, g in df.groupby("cs"):
        if g["entered"].nunique() == 2:
            out[cs] = roc_auc_score(g["entered"], g[col])
    return pd.Series(out)


def analyse(df: pd.DataFrame, bb, n_boot: int = 2000, n_perm: int = 1000, seed: int = 7) -> dict:
    rng = np.random.default_rng(seed)
    res = {"n_rows": len(df), "n_concept_steps": int(df["cs"].nunique()), "entry_rate": float(df["entered"].mean())}
    df = df.copy()
    df["dens_plus_size"] = np.nan
    for step in ("short", "long", "all"):
        d = df if step == "all" else df[df["step"] == step]
        if d.empty:
            continue
        a_den, a_size = per_cs_auc(d, "density"), per_cs_auc(d, "log_size")
        a_home = per_cs_auc(d, "phi_home")
        concepts = d["concept"].unique()

        def boot(series):
            idx = {c: [i for i in series.index if i.startswith(c + "|")] for c in concepts}
            bs = []
            for _ in range(n_boot):
                pick = rng.choice(concepts, len(concepts))
                vals = [series[i] for c in pick for i in idx[c]]
                if vals:
                    bs.append(np.mean(vals))
            return [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
        entry = {"n_evaluable_concept_steps": int(len(a_den)),
                 "auc_density_mean": float(a_den.mean()), "auc_density_ci95": boot(a_den),
                 "auc_size_mean": float(a_size.mean()), "auc_size_ci95": boot(a_size),
                 "auc_phi_home_mean": float(a_home.mean()),
                 "density_minus_size_mean": float((a_den - a_size.reindex(a_den.index)).mean()),
                 "density_minus_size_ci95": boot(a_den - a_size.reindex(a_den.index))}
        per_group = {}
        for g, gg in d.groupby("group"):
            ad, asz = per_cs_auc(gg, "density"), per_cs_auc(gg, "log_size")
            per_group[g] = {"n": int(len(ad)), "auc_density": float(ad.mean()) if len(ad) else math.nan,
                            "auc_size": float(asz.mean()) if len(asz) else math.nan}
        entry["per_group"] = per_group
        # conditional logit with groups = concept-step
        try:
            dd = d[d["cs"].isin(a_den.index)]
            X = dd[["density", "log_size", "phi_home"]].values
            X = (X - X.mean(0)) / X.std(0)
            m = ConditionalLogit(dd["entered"].values, X, groups=dd["cs"].values).fit(disp=0)
            coefs = m.params.tolist()
            # cluster bootstrap of coefficients (resample concepts)
            cb = []
            for _ in range(200):
                pick = rng.choice(dd["concept"].unique(), dd["concept"].nunique())
                parts = []
                for j, c in enumerate(pick):
                    p = dd[dd["concept"] == c].copy()
                    p["cs"] = p["cs"] + f"#{j}"
                    parts.append(p)
                bdf = pd.concat(parts)
                Xb = (bdf[["density", "log_size", "phi_home"]].values - dd[["density", "log_size", "phi_home"]].values.mean(0)) / dd[["density", "log_size", "phi_home"]].values.std(0)
                try:
                    cb.append(ConditionalLogit(bdf["entered"].values, Xb, groups=bdf["cs"].values).fit(disp=0).params)
                except (np.linalg.LinAlgError, ValueError):
                    continue
            cb = np.array(cb)
            entry["clogit"] = {"vars": ["density", "log_size", "phi_home"], "coef_std": coefs,
                               "ci95": [[float(np.percentile(cb[:, j], 2.5)), float(np.percentile(cb[:, j], 97.5))]
                                        for j in range(3)] if len(cb) else None,
                               "n_boot_ok": int(len(cb))}
            # AUC of combined score (density + size) from clogit linear predictor, within concept-step
            dd = dd.assign(lin=X @ np.array(coefs))
            entry["auc_combined_mean_in_sample"] = float(per_cs_auc(dd, "lin").mean())
        except (np.linalg.LinAlgError, ValueError) as e:
            entry["clogit"] = {"error": str(e)[:200]}
        # permutation null: shuffle field labels of phi
        null = []
        for _ in range(n_perm if step == "all" else 0):
            perm = rng.permutation(26)
            phip = bb.phi[np.ix_(perm, perm)]
            vals = []
            for cs, g in d.groupby("cs"):
                if g["entered"].nunique() < 2:
                    continue
                K = set(range(26)) - set(g["k"])
                dn = density(K, phip)
                vals.append(roc_auc_score(g["entered"], dn[g["k"].values]))
            null.append(np.mean(vals))
        if null:
            null = np.array(null)
            entry["perm_null"] = {"mean": float(null.mean()), "p95": float(np.percentile(null, 95)),
                                  "p_value": float((1 + (null >= a_den.mean()).sum()) / (1 + len(null))),
                                  "values": null.round(4).tolist()}
        res[step] = entry
    return res
