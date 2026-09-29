#!/usr/bin/env python3
"""WP2-T4: traceable next-field entry file. Refits Exp6's (art_N-mpomDZZ1ln) conditional logits M0/M1/M2/M3/M2lost from
results/entry_risk_sets_{heldout,dev}.parquet with (a) an independent Breslow partial-likelihood implementation
(Exp6's own form) and (b) statsmodels' exact ConditionalLogit, reproduces heldout_result.json H2_pooled, recomputes
within-stratum AUCs (refit and from full_method_out.json predict_M0/predict_M2), and writes the per-row parquet plus
next_field_trace.json mapping each headline number to its recomputation."""
from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd
from loguru import logger
from scipy import optimize, stats
from statsmodels.discrete.conditional_models import ConditionalLogit

import common as C

MODELS = {"M0": ["a_phi_home", "b_log_size", "c_density", "e_gate_own"],
          "M1": ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d0_ret_rel"],
          "M2": ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d_ret_gate"],
          "M3": ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d0_ret_rel", "d_ret_gate"],
          "M2lost": ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d_lost_gate"]}
REGS = sorted({c for v in MODELS.values() for c in v})


class Breslow:
    """Conditional logit, Breslow approximation for tied events: sum_s [sum_{i in E_s} x_i b - d_s log sum_{j in s} e^{x_j b}]."""

    def __init__(self, X, y, strata):
        o = np.argsort(strata, kind="stable")
        self.X, self.y, s = X[o], y[o].astype(float), strata[o]
        _, self.inv = np.unique(s, return_inverse=True)
        self.ns = self.inv.max() + 1
        self.d = np.bincount(self.inv, weights=self.y, minlength=self.ns)

    def nll(self, b):
        eta = self.X @ b
        m = np.zeros(self.ns)
        np.maximum.at(m, self.inv, eta)
        w = np.exp(eta - m[self.inv])
        S = np.bincount(self.inv, weights=w, minlength=self.ns)
        ll = (self.y * eta).sum() - (self.d * (np.log(S) + m)).sum()
        P = w / S[self.inv]
        Xbar = np.vstack([np.bincount(self.inv, weights=P * self.X[:, k], minlength=self.ns) for k in range(self.X.shape[1])]).T
        g = self.X.T @ self.y - (self.d[:, None] * Xbar).sum(0)
        return -ll, -g

    def hess(self, b):
        eta = self.X @ b
        m = np.zeros(self.ns)
        np.maximum.at(m, self.inv, eta)
        w = np.exp(eta - m[self.inv])
        S = np.bincount(self.inv, weights=w, minlength=self.ns)
        P = w / S[self.inv]
        k = self.X.shape[1]
        Xbar = np.vstack([np.bincount(self.inv, weights=P * self.X[:, j], minlength=self.ns) for j in range(k)]).T
        H = np.zeros((k, k))
        for a in range(k):
            for c in range(a, k):
                e = np.bincount(self.inv, weights=P * self.X[:, a] * self.X[:, c], minlength=self.ns)
                v = (self.d * (e - Xbar[:, a] * Xbar[:, c])).sum()
                H[a, c] = H[c, a] = v
        return H

    def fit(self):
        r = optimize.minimize(self.nll, np.zeros(self.X.shape[1]), jac=True, method="BFGS", options={"gtol": 1e-8, "maxiter": 500})
        H = self.hess(r.x)
        se = np.sqrt(np.diag(np.linalg.inv(H)))
        return {"coef": r.x, "se": se, "ll": -r.fun, "converged": bool(r.success)}


def within_auc(strat, y, score) -> pd.Series:
    d = pd.DataFrame({"s": strat, "y": y, "x": score})
    d["r"] = d.groupby("s").x.rank(method="average")
    g = d.groupby("s").agg(ntot=("y", "size"), nev=("y", "sum"))
    g = g.join(d[d.y == 1].groupby("s").r.sum().rename("rs")).fillna({"rs": 0})
    g = g[(g.nev > 0) & (g.nev < g.ntot)]
    return (g.rs - g.nev * (g.nev + 1) / 2) / (g.nev * (g.ntot - g.nev))


def boot_mean_by_concept(series: pd.Series, B: int, rng) -> list[float]:
    cid = series.index.to_numpy() // 100
    u, inv = np.unique(cid, return_inverse=True)
    sums = np.bincount(inv, weights=series.to_numpy())
    cnt = np.bincount(inv)
    bs = [sums[p].sum() / max(cnt[p].sum(), 1) for p in (rng.integers(0, len(u), len(u)) for _ in range(B))]
    return C.pct_ci(bs)


def prepare(df: pd.DataFrame, spec: dict) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    counts = {"n_rows_all": len(df), "n_strata_all": int(df.stratum.nunique()), "n_concepts_all": int(df.cidx.nunique()),
              "n_events_all": int(df.entered.sum())}
    prim = df[df.n_ret > 0].copy()  # frozen primary sample: strata with a non-empty retaining set
    counts.update({"n_rows_primary": len(prim), "n_strata_primary": int(prim.stratum.nunique()),
                   "n_concepts_primary": int(prim.cidx.nunique()), "n_events_primary": int(prim.entered.sum())})
    for c in REGS:
        s = spec["standardisation"][c]
        prim[c] = (prim[c] - s["mean"]) / (s["sd"] if s["sd"] > 0 else 1.0)
    g = prim.groupby("stratum").entered.agg(["sum", "size"])
    keep = g[(g["sum"] > 0) & (g["sum"] < g["size"])].index
    inf = prim[prim.stratum.isin(keep)].copy()
    counts.update({"n_rows_informative": len(inf), "n_strata_informative": int(inf.stratum.nunique()),
                   "n_concepts_informative": int(inf.cidx.nunique()), "n_events_informative": int(inf.entered.sum()),
                   "share_informative_strata_multi_event": float((g.loc[keep, "sum"] > 1).mean())})
    return prim, inf, counts


def fit_all(inf: pd.DataFrame) -> dict:
    out = {}
    y = inf.entered.to_numpy()
    s = inf.stratum.to_numpy()
    for m, cols in MODELS.items():
        X = inf[cols].to_numpy(float)
        br = Breslow(X, y, s).fit()
        ex = ConditionalLogit(y, X, groups=s).fit(disp=0, method="bfgs", maxiter=500)
        out[m] = {"breslow": {"coef": dict(zip(cols, br["coef"])), "se": dict(zip(cols, br["se"])), "ll": br["ll"],
                              "converged": br["converged"]},
                  "exact": {"coef": dict(zip(cols, ex.params)), "se": dict(zip(cols, ex.bse)), "ll": float(ex.llf)},
                  "_b_breslow": br["coef"]}
    return out


def lr(f, big, small, kind):
    v = 2 * (f[big][kind]["ll"] - f[small][kind]["ll"])
    return {"LR": v, "p": float(stats.chi2.sf(max(v, 0), 1))}


@logger.catch(reraise=True)
def main() -> None:
    C.setup_logging("wp2_t4")
    rng = np.random.default_rng(C.SEED)
    spec = C.read_json(C.E6 / "results/frozen_spec.json")
    held = C.read_json(C.E6 / "results/heldout_result.json")
    dev_res = C.read_json(C.E6 / "results/dev_result.json")
    audit = C.read_json(C.E6 / "results/audit.json")
    trace, tol = {}, 1e-3
    fits_by_split = {}
    for split in ("heldout", "dev"):
        df = pd.read_parquet(C.track(C.E6 / f"results/entry_risk_sets_{split}.parquet"))
        logger.info(f"{split}: {df.shape}; columns {list(df.columns)}")
        prim, inf, counts = prepare(df, spec)
        f = fit_all(inf)
        L = {k: {"breslow": lr(f, a, b, "breslow"), "exact": lr(f, a, b, "exact")}
             for k, (a, b) in {"M2_vs_M0": ("M2", "M0"), "M1_vs_M0": ("M1", "M0"), "M3_vs_M1": ("M3", "M1"),
                               "M2lost_vs_M0": ("M2lost", "M0")}.items()}
        aucs = {}
        for m, cols in MODELS.items():
            sc = inf[cols].to_numpy(float) @ f[m]["_b_breslow"]
            w = within_auc(inf.stratum.to_numpy(), inf.entered.to_numpy(), sc)
            aucs[m] = {"mean": float(w.mean()), "ci95": boot_mean_by_concept(w, 2000, rng), "n_strata": int(len(w))}
        for c in REGS:
            w = within_auc(inf.stratum.to_numpy(), inf.entered.to_numpy(), inf[c].to_numpy(float))
            aucs[c] = {"mean": float(w.mean()), "n_strata": int(len(w))}
        per_group = {}
        if split == "heldout":
            for gname, gd in inf.groupby("hgroup"):
                if gd.cidx.nunique() < 10:
                    per_group[gname] = {"n_concepts": int(gd.cidx.nunique()), "status": "too few concepts"}
                    continue
                y, s = gd.entered.to_numpy(), gd.stratum.to_numpy()
                b0 = Breslow(gd[MODELS["M0"]].to_numpy(float), y, s).fit()
                b2 = Breslow(gd[MODELS["M2"]].to_numpy(float), y, s).fit()
                b1 = Breslow(gd[MODELS["M1"]].to_numpy(float), y, s).fit()
                per_group[gname] = {"n_concepts": int(gd.cidx.nunique()), "n_events": int(y.sum()),
                                    "d_ret_gate": float(b2["coef"][-1]), "se": float(b2["se"][-1]),
                                    "LR_M2_vs_M0": float(2 * (b2["ll"] - b0["ll"])),
                                    "d0_ret_rel_M1": float(b1["coef"][-1]), "se_M1": float(b1["se"][-1])}
            ev = [g for g, v in per_group.items() if "d_ret_gate" in v]
            dl = C.dersimonian_laird([per_group[g]["d_ret_gate"] for g in ev], [per_group[g]["se"] for g in ev])
            dl1 = C.dersimonian_laird([per_group[g]["d0_ret_rel_M1"] for g in ev], [per_group[g]["se_M1"] for g in ev])
        fits_by_split[split] = {"counts": counts, "fits": {m: {k: v for k, v in x.items() if k != "_b_breslow"} for m, x in f.items()},
                                "LR": L, "auc_within_stratum": aucs, "per_group": per_group,
                                "DL_pooled_d_ret_gate": dl if split == "heldout" else None,
                                "DL_pooled_d0_ret_rel_M1": dl1 if split == "heldout" else None}
        if split == "heldout":
            # per-row file
            rows = prim.copy()
            for m, cols in MODELS.items():
                eta = rows[cols].to_numpy(float) @ f[m]["_b_breslow"]
                e = np.exp(eta - rows.assign(_e=eta).groupby("stratum")._e.transform("max").to_numpy())
                rows[f"p_{m}_within_stratum"] = e / pd.Series(e, index=rows.index).groupby(rows.stratum).transform("sum").to_numpy()
            rows["informative_stratum"] = rows.stratum.isin(inf.stratum.unique())
            rows = rows.rename(columns={"t": "year", "field": "target_field", "entered": "event"})
            rows["note_covariates"] = "standardised with frozen_spec.standardisation"
            rows.to_parquet(C.TAB / "next_field_heldout_rows.parquet", index=False)
    # AUC from the saved predictions of Exp6 (frozen DEV coefficients)
    fm = json.loads(C.track(C.E6 / "full_method_out.json").read_text())
    pred = {}
    for ds in fm["datasets"]:
        if ds["dataset"] != "entry_events_heldout":
            continue
        s = np.array([e["metadata_stratum"] for e in ds["examples"]])
        y = np.array([int(e["output"]) for e in ds["examples"]])
        p0 = np.array([float(e["predict_M0_size_density_home_owngateway"]) for e in ds["examples"]])
        p2 = np.array([float(e["predict_M2_plus_retaining_gateway_relatedness"]) for e in ds["examples"]])
        w0, w2 = within_auc(s, y, p0), within_auc(s, y, p2)
        pred = {"n_rows": int(len(y)), "n_strata_informative": int(len(w0)), "auc_M0_frozen_dev_coef": float(w0.mean()),
                "auc_M2_frozen_dev_coef": float(w2.mean()), "ci95_M0": boot_mean_by_concept(w0, 2000, rng),
                "ci95_M2": boot_mean_by_concept(w2, 2000, rng)}
    del fm
    H = held["H2_pooled"]
    hf = fits_by_split["heldout"]
    hc = hf["counts"]

    def tr(name, reported, src_key, recomputed, how, tol_=tol):
        ok = None if reported is None or recomputed is None else abs(float(reported) - float(recomputed)) <= tol_ * max(1.0, abs(float(reported)))
        trace[name] = {"reported": reported, "source_file": "round-2/experiment-6/src/results/heldout_result.json",
                       "key_path": src_key, "recomputed": recomputed, "how": how, "match": ok}

    tr("n_rows", H["n_rows"], "H2_pooled.n_rows", hc["n_rows_primary"], "rows of entry_risk_sets_heldout.parquet with n_ret > 0 (primary sample)")
    tr("n_strata", H["n_strata"], "H2_pooled.n_strata", hc["n_strata_primary"], "unique strata in the primary sample (all, incl. strata with 0 events)")
    tr("n_strata_model", H["models"]["M0"]["n_strata"], "H2_pooled.models.M0.n_strata", hc["n_strata_informative"],
       "strata with >= 1 event and >= 1 non-event (the only strata that enter a conditional likelihood)")
    tr("n_rows_model", H["models"]["M0"]["n_rows"], "H2_pooled.models.M0.n_rows", hc["n_rows_informative"], "rows in informative strata")
    tr("n_concepts", H["n_concepts"], "H2_pooled.n_concepts", hc["n_concepts_primary"], "unique cidx in primary sample")
    tr("n_events", H["n_events"], "H2_pooled.n_events", hc["n_events_primary"], "sum(entered) in primary sample")
    for k in ("M2_vs_M0", "M1_vs_M0", "M3_vs_M1", "M2lost_vs_M0"):
        tr(f"LR_{k}_breslow", H["LR"][k]["LR"], f"H2_pooled.LR.{k}.LR", hf["LR"][k]["breslow"]["LR"], "independent Breslow refit", 5e-3)
        trace[f"LR_{k}_exact"] = {"reported": audit["H2_LR"]["statsmodels_exact"] if k == "M2_vs_M0" else None,
                                  "source_file": "round-2/experiment-6/src/results/audit.json" if k == "M2_vs_M0" else None,
                                  "key_path": "H2_LR.statsmodels_exact" if k == "M2_vs_M0" else None,
                                  "recomputed": hf["LR"][k]["exact"]["LR"], "how": "statsmodels ConditionalLogit (exact conditional likelihood)"}
    for m, cname in (("M1", "d0_ret_rel"), ("M2", "d_ret_gate"), ("M2lost", "d_lost_gate")):
        tr(f"coef_{m}_{cname}", H["models"][m]["coef"][cname], f"H2_pooled.models.{m}.coef.{cname}",
           hf["fits"][m]["breslow"]["coef"][cname], "independent Breslow refit", 5e-3)
        tr(f"se_{m}_{cname}", H["models"][m]["se"][cname], f"H2_pooled.models.{m}.se.{cname}",
           hf["fits"][m]["breslow"]["se"][cname], "inverse observed information of the Breslow refit", 5e-3)
    tr("auc_within_M0", H["auc_within_stratum"]["M0"]["mean"], "H2_pooled.auc_within_stratum.M0.mean", hf["auc_within_stratum"]["M0"]["mean"], "refit linear predictor, mean-rank AUC per informative stratum")
    tr("auc_within_M2", H["auc_within_stratum"]["M2"]["mean"], "H2_pooled.auc_within_stratum.M2.mean", hf["auc_within_stratum"]["M2"]["mean"], "refit")
    tr("auc_within_M1", H["auc_within_stratum"]["M1"]["mean"], "H2_pooled.auc_within_stratum.M1.mean", hf["auc_within_stratum"]["M1"]["mean"], "refit")
    tr("auc_M0_frozen_dev_coef", held["frozen_dev_coef_auc"]["M0"]["mean"], "frozen_dev_coef_auc.M0.mean", pred.get("auc_M0_frozen_dev_coef"), "full_method_out.json entry_events_heldout predict_M0 (frozen DEV coefficients)")
    tr("auc_M2_frozen_dev_coef", held["frozen_dev_coef_auc"]["M2"]["mean"], "frozen_dev_coef_auc.M2.mean", pred.get("auc_M2_frozen_dev_coef"), "full_method_out.json predict_M2")
    for g in ("Physical", "LifeEnv", "Social", "Cohort"):
        if g in hf["per_group"] and "d_ret_gate" in hf["per_group"][g]:
            tr(f"d_{g}", held["H2_per_group"][g]["d"], f"H2_per_group.{g}.d", hf["per_group"][g]["d_ret_gate"], "Breslow refit within hgroup", 5e-3)
    tr("DL_pooled_d", held["H2_DL_pooled"]["b"], "H2_DL_pooled.b", hf["DL_pooled_d_ret_gate"]["pooled"], "DerSimonian-Laird over refit per-group d", 5e-3)
    trace["d0_ret_rel_DL_pooled_M1"] = {"reported": None, "recomputed": hf["DL_pooled_d0_ret_rel_M1"],
                                        "how": "new: DL pooling of the plain retaining-relatedness coefficient (M1), the review's suggested headline"}
    trace["dev_LR_M2_vs_M0"] = {"reported": dev_res.get("H2_pooled", {}).get("LR", {}).get("M2_vs_M0", {}).get("LR"),
                                "source_file": "round-2/experiment-6/src/results/dev_result.json", "key_path": "H2_pooled.LR.M2_vs_M0.LR",
                                "recomputed": fits_by_split["dev"]["LR"]["M2_vs_M0"]["breslow"]["LR"], "how": "Breslow refit on entry_risk_sets_dev.parquet"}
    strata_note = (f"The hypothesis text's '961 strata' is the number of INFORMATIVE strata (>= 1 event and >= 1 non-event) that enter the "
                   f"conditional likelihood ({hc['n_strata_informative']} recomputed; {hc['n_rows_informative']} rows); the file's n_strata = 2,339 counts ALL strata of the "
                   f"primary sample (n_ret > 0; {hc['n_strata_primary']} recomputed, {hc['n_rows_primary']} rows). The parquet itself holds "
                   f"{hc['n_strata_all']} strata / {hc['n_rows_all']} rows before the n_ret > 0 restriction.")
    lr_note = ("LR 68.6 = M1 (plain retaining relatedness d0_ret_rel) vs M0, Breslow; LR 71.7 = M2 (gateway-weighted d_ret_gate) vs M0, Breslow; "
               "LR 77.3 = M2 vs M0 with the exact conditional likelihood (statsmodels, Exp6 audit.json). "
               f"Recomputed here: M1vsM0 Breslow {hf['LR']['M1_vs_M0']['breslow']['LR']:.2f} / exact {hf['LR']['M1_vs_M0']['exact']['LR']:.2f}; "
               f"M2vsM0 Breslow {hf['LR']['M2_vs_M0']['breslow']['LR']:.2f} / exact {hf['LR']['M2_vs_M0']['exact']['LR']:.2f}.")
    d_note = ("d = 0.281 is the M1 coefficient of plain retaining relatedness (d0_ret_rel, SE 0.032); d = 0.302 ('0.30') is the M2 "
              "coefficient of gateway-weighted retaining relatedness (d_ret_gate). Both are Breslow, per SD of the frozen DEV standardisation.")
    out = {"trace": trace, "by_split": fits_by_split, "predictions_auc": pred, "strata_clash_resolution": strata_note,
           "LR_clash_resolution": lr_note, "d_clash_resolution": d_note,
           "per_row_file": "record_tables/next_field_heldout_rows.parquet",
           "n_trace_match": int(sum(1 for v in trace.values() if v.get("match") is True)),
           "n_trace_checked": int(sum(1 for v in trace.values() if v.get("match") is not None))}
    C.dump(out, C.TAB / "next_field_trace.json")
    C.save_manifest("wp2_t4")
    logger.info(strata_note)
    logger.info(lr_note)
    for k, v in trace.items():
        logger.info(f"{k}: rep={v.get('reported')} rec={v.get('recomputed') if not isinstance(v.get('recomputed'), dict) else '...'} match={v.get('match')}")


if __name__ == "__main__":
    main()
