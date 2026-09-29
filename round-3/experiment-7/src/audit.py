#!/usr/bin/env python3
"""T7 independent audit (separate code path; never imports lib/d3.py or lib/models.py):
 (1) held-out pooled-4 LR(R3 vs R2) and d0 with statsmodels' EXACT conditional likelihood and a hand-written Breslow
     likelihood (scipy BFGS over a per-stratum Python loop) on the saved risk-set rows;
 (2) D_rca_1y and d0_ret_rel for 20 random held-out rows re-derived with naive loops from EXP5's raw agg_counts.parquet;
 (3) the DerSimonian-Laird pooling of per-unit d0 recomputed inline;
 (4) the same exact-likelihood check on the EXP6 held-out frame (Step 1).
Writes results/audit.json; every check records pass/fail and the numbers."""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from scipy import optimize, stats
from statsmodels.discrete.conditional_models import ConditionalLogit

ROOT = Path(__file__).resolve().parent
RES = ROOT / "results"
RUN = Path(__file__).resolve().parents[3] / "round-2"
EXP5, EXP6 = RUN / "experiment-5/src", RUN / "experiment-6/src"
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "audit.log", rotation="30 MB", level="DEBUG")
R2 = ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "D_rca_1y", "D_vol"]
R3 = R2 + ["d0_ret_rel"]
HELD4 = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]


def std(df: pd.DataFrame, spec: dict, cols: list[str]) -> np.ndarray:
    return np.column_stack([(df[c].to_numpy(float) - spec[c]["mean"]) / spec[c]["sd"] for c in cols])


def informative(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("stratum").entered.agg(["sum", "size"])
    ok = g.index[(g["sum"] > 0) & (g["sum"] < g["size"])]
    return df[df.stratum.isin(ok)].sort_values(["stratum"], kind="stable")


def breslow_fit(X: np.ndarray, y: np.ndarray, s: np.ndarray) -> tuple[np.ndarray, float]:
    """hand-written Breslow conditional likelihood, one Python loop per stratum (deliberately naive)."""
    groups = [np.nonzero(s == u)[0] for u in np.unique(s)] if len(np.unique(s)) < 3000 else None
    if groups is None:
        order = np.argsort(s, kind="stable")
        _, st, cn = np.unique(s[order], return_index=True, return_counts=True)
        groups = [order[a:a + c] for a, c in zip(st, cn)]

    def nll(b):
        eta = X @ b
        ll, g = 0.0, np.zeros_like(b)
        for ix in groups:
            e = eta[ix]; m = e.max(); w = np.exp(e - m); S = w.sum()
            ne = y[ix].sum()
            ll += (y[ix] * e).sum() - ne * (math.log(S) + m)
            g += (y[ix][:, None] * X[ix]).sum(0) - ne * (w[:, None] * X[ix]).sum(0) / S
        return -ll, -g
    r = optimize.minimize(nll, np.zeros(X.shape[1]), jac=True, method="BFGS", options={"gtol": 1e-6, "maxiter": 500})
    return r.x, -r.fun


def exact_fit(X: np.ndarray, y: np.ndarray, s: np.ndarray) -> tuple[np.ndarray, float]:
    m = ConditionalLogit(y, X, groups=s)
    r = m.fit(disp=0, method="bfgs", maxiter=300)
    return np.asarray(r.params), float(r.llf)


def ladder_check(df: pd.DataFrame, spec: dict, label: str, frac: float, seeds: list[int], reported: dict) -> dict:
    out = {"label": label, "subsample_fraction": frac, "runs": []}
    for sd in seeds:
        d = df
        if frac < 1:
            cids = df.cidx.unique()
            keep = np.random.default_rng(sd).choice(cids, int(frac * len(cids)), replace=False)
            d = df[df.cidx.isin(keep)]
        d = informative(d)
        y = d.entered.to_numpy(float); s = d.stratum.to_numpy()
        X2, X3 = std(d, spec, R2), std(d, spec, R3)
        t = time.time()
        b3b, l3b = breslow_fit(X3, y, s); _, l2b = breslow_fit(X2, y, s)
        tb = time.time() - t
        t = time.time()
        b3e, l3e = exact_fit(X3, y, s); _, l2e = exact_fit(X2, y, s)
        te = time.time() - t
        run = {"seed": sd, "n_strata": int(len(np.unique(s))), "share_multi_event_strata": float(d.groupby("stratum").entered.sum().gt(1).mean()),
               "breslow_hand": {"d0": float(b3b[-1]), "LR": float(2 * (l3b - l2b))},
               "exact_statsmodels": {"d0": float(b3e[-1]), "LR": float(2 * (l3e - l2e))}, "sec": [round(tb, 1), round(te, 1)]}
        run["LR_ratio_exact_over_breslow"] = run["exact_statsmodels"]["LR"] / run["breslow_hand"]["LR"] if run["breslow_hand"]["LR"] else None
        run["same_sign_d0"] = bool(np.sign(b3b[-1]) == np.sign(b3e[-1]))
        out["runs"].append(run)
        logger.info(f"[{label}] seed {sd}: {run}")
    if frac == 1:
        r = out["runs"][0]
        out["reported_pipeline"] = reported
        out["breslow_matches_pipeline"] = bool(abs(r["breslow_hand"]["LR"] - reported["LR"]) < 1e-3 * max(1, reported["LR"])
                                               and abs(r["breslow_hand"]["d0"] - reported["d0"]) < 1e-3)
    ratios = [r["LR_ratio_exact_over_breslow"] for r in out["runs"] if r["LR_ratio_exact_over_breslow"]]
    out["pass_same_sign_and_|ratio-1|<0.15"] = bool(all(r["same_sign_d0"] for r in out["runs"]) and all(abs(x - 1) < 0.15 for x in ratios))
    return out


def naive_rows(df: pd.DataFrame, fr: pd.DataFrame, n: int, seed: int) -> dict:
    """re-derive D_rca_1y and d0_ret_rel for n random rows from the raw scan with explicit loops."""
    bb = json.loads((EXP6 / "inputs" / "field_backbone.json").read_text())
    phi = bb["phi"]
    VF = np.load(EXP5 / "scan" / "year_field_totals.npz")["VF"]
    rows = df.sample(n, random_state=seed)
    ag = pd.read_parquet(EXP5 / "scan" / "agg_counts.parquet", filters=[("ci", "in", sorted(set(map(int, rows.cidx))))])
    ag = ag[ag.tagstate == 1]
    frm = fr.set_index("ci")
    out, ok = [], True
    for r in rows.itertuples():
        a = ag[ag.ci == r.cidx]
        cnt = {}
        for q in a.itertuples():
            if 1 <= q.vfield <= 26:
                cnt[(int(q.year), int(q.vfield))] = cnt.get((int(q.year), int(q.vfield)), 0) + int(q.n)
        yprev = int(r.t) - 1
        home = [int(h) for h in str(frm.loc[r.cidx, "home"]).split(";")]
        k = int(r.field)
        # D_rca_1y
        tot_c = sum(cnt.get((yprev, f - 10), 0) for f in range(11, 37))
        tot_all = sum(VF[yprev - 1995][f - 10] for f in range(11, 37))
        U = []
        for f in range(11, 37):
            if tot_c > 0:
                rca = (cnt.get((yprev, f - 10), 0) / tot_c) / (VF[yprev - 1995][f - 10] / tot_all)
                if rca > 1:
                    U.append(f)
        num = sum(phi[f - 11][k - 11] for f in U)
        den = sum(phi[f - 11][k - 11] for f in range(11, 37))
        drca = num / den if den > 0 else 0.0
        # retained set at t-1
        ret = []
        for f in range(11, 37):
            if f in home:
                continue
            cum_lag2 = sum(cnt.get((y, f - 10), 0) for y in range(1995, yprev - 2 + 1))
            w3 = sum(cnt.get((y, f - 10), 0) for y in range(yprev - 2, yprev + 1))
            if cum_lag2 >= 2 and w3 >= 2:
                ret.append(f)
        d0 = sum(phi[f - 11][k - 11] for f in ret) / len(ret) if ret else 0.0
        good = abs(drca - r.D_rca_1y) < 1e-5 and abs(d0 - r.d0_ret_rel) < 1e-5
        ok &= good
        out.append({"cidx": int(r.cidx), "t": int(r.t), "field": k, "D_rca_1y_naive": drca, "D_rca_1y_pipeline": float(r.D_rca_1y),
                    "d0_naive": d0, "d0_pipeline": float(r.d0_ret_rel), "match": bool(good)})
    return {"n": n, "all_match_1e-5": bool(ok), "rows": out}


def dl_inline(units: dict) -> dict:
    b = np.array([units[u]["d0_R3"]["coef"] for u in HELD4 if "d0_R3" in units.get(u, {})])
    se = np.array([units[u]["d0_R3"]["se_concept"] for u in HELD4 if "d0_R3" in units.get(u, {})])
    w = 1 / se**2
    fixed = (w * b).sum() / w.sum()
    Q = (w * (b - fixed) ** 2).sum()
    tau2 = max(0.0, (Q - (len(b) - 1)) / (w.sum() - (w**2).sum() / w.sum()))
    ws = 1 / (se**2 + tau2)
    return {"b": float((ws * b).sum() / ws.sum()), "se": float(math.sqrt(1 / ws.sum())), "tau2": float(tau2),
            "I2": float(max(0.0, (Q - (len(b) - 1)) / Q)) if Q > 0 else 0.0}


@logger.catch(reraise=True)
def main() -> None:
    res = {}
    # EXP6 held-out (Step 1): full sample, exact vs Breslow
    s1 = json.loads((RES / "step1_exp6_robustness.json").read_text())
    d6 = pd.read_parquet(RES / "risk_sets_exp6_extended_heldout.parquet")
    d6 = d6[d6.n_ret > 0]
    rep6 = {"LR": s1["heldout"]["ladder"]["frontier_primary_sample"]["LR"]["R3_ret_vs_R2_vol"]["LR"],
            "d0": s1["heldout"]["ladder"]["frontier_primary_sample"]["models"]["R3_ret"]["coef"]["d0_ret_rel"]}
    res["exp6_heldout_exact"] = ladder_check(d6, s1["standardisation"], "EXP6 held-out", 1.0, [0], rep6)
    ho = RES / "step2_heldout.json"
    if ho.exists():
        h = json.loads(ho.read_text())
        spec = json.loads((RES / "frozen_spec.json").read_text())["standardisation_DEV"]
        df = pd.read_parquet(RES / "risk_sets_exp5_minus_exp6_heldout.parquet")
        df4 = df[df.unit.isin(HELD4) & (df.n_ret > 0)]
        lad = h["pooled4"]["ladder"]["frontier_primary_sample"]
        rep = {"LR": lad["LR"]["R3_ret_vs_R2_vol"]["LR"], "d0": lad["models"]["R3_ret"]["coef"]["d0_ret_rel"]}
        res["exp5_heldout_pooled4_breslow_full"] = ladder_check_breslow_only(df4, spec, rep)
        res["exp5_heldout_pooled4_exact_subsample"] = ladder_check(df4, spec, "EXP5 held-out pooled-4 (30% concepts)", 0.3, [1, 2, 3], rep)
        fr = pd.read_csv(EXP5 / "frame_concepts.csv")
        res["naive_rows"] = naive_rows(df4, fr, 20, 11)
        dl = dl_inline(h["units"])
        rep_dl = h["DL_4groups"]["d0"]
        res["DL_inline"] = {**dl, "pipeline_b": rep_dl["b"], "pipeline_se": rep_dl["se"],
                            "match": bool(abs(dl["b"] - rep_dl["b"]) < 1e-9 and abs(dl["se"] - rep_dl["se"]) < 1e-9)}
    else:
        res["exp5"] = "held-out stage not run yet"
    checks = {k: v.get("pass_same_sign_and_|ratio-1|<0.15", v.get("all_match_1e-5", v.get("match", v.get("breslow_matches_pipeline"))))
              for k, v in res.items() if isinstance(v, dict)}
    res["summary"] = {"checks": checks, "all_pass": bool(all(x for x in checks.values() if x is not None))}
    (RES / "audit.json").write_text(json.dumps(res, indent=1, default=float))
    logger.info(f"audit summary: {res['summary']}")


def ladder_check_breslow_only(df: pd.DataFrame, spec: dict, reported: dict) -> dict:
    d = informative(df)
    y = d.entered.to_numpy(float); s = d.stratum.to_numpy()
    t = time.time()
    b3, l3 = breslow_fit(std(d, spec, R3), y, s); _, l2 = breslow_fit(std(d, spec, R2), y, s)
    LR = 2 * (l3 - l2)
    return {"breslow_hand": {"d0": float(b3[-1]), "LR": float(LR)}, "reported_pipeline": reported, "sec": round(time.time() - t, 1),
            "match": bool(abs(LR - reported["LR"]) < 1e-3 * max(1, reported["LR"]) and abs(b3[-1] - reported["d0"]) < 1e-3)}


if __name__ == "__main__":
    main()
