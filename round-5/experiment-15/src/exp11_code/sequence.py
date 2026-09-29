#!/usr/bin/env python3
"""Step 7 (post-seal): RQ2 sequence question -- does a home-prominence peak precede off-home take-off, and do
intersection-born concepts take off without one?

prominence(ci, t): mean of within-(primary home field, year) percentile ranks of home-only deg(t) and kcore(t)
  (cells with >= 20 frame concepts, else NA), 0-100 scale; primary home = the home field with most grounded works
  over t0..t0+2.
peak = argmax prominence over t0..h_end (ties -> earliest); counts only if it exceeds the concept's median by >= 20.
take-off T = first t in t0..h_end with entries(t) >= 2 (D3 off-home entries); otherwise censored at h_end.
Tests: (a) share of take-off concepts WITHOUT a prior peak, intersection-born minus single-home, concept bootstrap
(H-S1); (b) Kaplan-Meier + log-rank by single vs multi home, Cox with group strata and log early volume;
(c) Sun-Abraham event studies: entries(t+1) around the peak year, prominence(t) around T (pre-trends).
Reported per body and excluding Medicine homes. Writes results/sequence_tests.json, data/sequence_concepts.parquet."""
from __future__ import annotations

import argparse
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from common import DATA, DATA_IN, RES, jdump, load_frame, setup_logger
from panel_m import frame_plus

warnings.filterwarnings("ignore")
SEED = 20260929


def primary_home(fr: pd.DataFrame) -> pd.Series:
    z = np.load(DATA_IN / "grounded_V.npz")
    G, cis = z["G"], z["ci"]
    pos = {c: i for i, c in enumerate(cis)}
    out = {}
    for r in fr.itertuples():
        hl = r.home_list
        if not hl:
            out[r.ci] = 0
            continue
        i = pos[r.ci]
        yi = [y - 1995 for y in (r.t0, r.t0 + 1, r.t0 + 2)]
        tot = [G[i, yi, h - 10].sum() for h in hl]
        out[r.ci] = hl[int(np.argmax(tot))]
    return pd.Series(out)


def prominence(yf: pd.DataFrame) -> pd.Series:
    def pr(s: pd.Series) -> pd.Series:
        return s.rank(pct=True, method="average") * 100 if len(s) >= 20 else pd.Series(np.nan, index=s.index)
    g = yf.groupby(["phome", "year"])
    return (g.deg.transform(pr) + g.kcore.transform(pr)) / 2


def concept_table(yf: pd.DataFrame, ent: pd.DataFrame, fr: pd.DataFrame) -> pd.DataFrame:
    rows = []
    E = ent.set_index(["ci", "year"]).entries
    for ci, d in yf.groupby("ci", sort=False):
        d = d.sort_values("year")
        pv = d.prom.to_numpy(float)
        yrs = d.year.to_numpy()
        ok = np.isfinite(pv)
        peak_y, peak_ok = np.nan, 0
        if ok.sum() >= 3:
            j = int(np.nanargmax(np.where(ok, pv, -np.inf)))
            peak_y = int(yrs[j])
            peak_ok = int(pv[j] - np.nanmedian(pv[ok]) >= 20)
        e = np.array([E.get((ci, int(y)), np.nan) for y in yrs], float)
        to = np.nonzero(e >= 2)[0]
        T = int(yrs[to[0]]) if len(to) else np.nan
        rows.append((ci, peak_y, peak_ok, T, int(yrs[0]), int(yrs[-1])))
    c = pd.DataFrame(rows, columns=["ci", "peak_year", "peak_valid", "takeoff_year", "first_year", "last_year"])
    c = c.merge(fr[["ci", "t0", "body", "group", "multi_home", "early_volume"]], on="ci")
    c["has_takeoff"] = c.takeoff_year.notna().astype(int)
    c["prior_peak"] = ((c.peak_valid == 1) & (c.peak_year < c.takeoff_year)).astype(int)
    c["no_prior_peak"] = 1 - c.prior_peak
    c["dur"] = np.where(c.has_takeoff == 1, c.takeoff_year - c.t0, c.last_year - c.t0) + 1
    return c


def share_test(c: pd.DataFrame, n_boot: int = 2000) -> dict:
    d = c[c.has_takeoff == 1]
    m, s = d[d.multi_home == 1], d[d.multi_home == 0]
    if len(m) < 10 or len(s) < 10:
        return {"n_multi": int(len(m)), "n_single": int(len(s)), "note": "too few"}
    diff = m.no_prior_peak.mean() - s.no_prior_peak.mean()
    rng = np.random.default_rng(SEED)
    mv, sv = m.no_prior_peak.to_numpy(), s.no_prior_peak.to_numpy()
    bs = np.array([rng.choice(mv, len(mv)).mean() - rng.choice(sv, len(sv)).mean() for _ in range(n_boot)])
    return {"n_multi": int(len(m)), "n_single": int(len(s)), "share_no_prior_peak_multi": float(m.no_prior_peak.mean()),
            "share_no_prior_peak_single": float(s.no_prior_peak.mean()), "diff": float(diff),
            "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
            "share_prior_peak_all": float(d.prior_peak.mean()),
            "share_takeoff_multi": float(c[c.multi_home == 1].has_takeoff.mean()),
            "share_takeoff_single": float(c[c.multi_home == 0].has_takeoff.mean()),
            "holds_H_S1": bool(np.percentile(bs, 2.5) > 0)}


def survival(c: pd.DataFrame) -> dict:
    from lifelines import CoxPHFitter, KaplanMeierFitter
    from lifelines.statistics import logrank_test
    out = {}
    km = {}
    for mh, d in c.groupby("multi_home"):
        k = KaplanMeierFitter().fit(d.dur, d.has_takeoff)
        km[str(mh)] = {"t": k.survival_function_.index.tolist(),
                       "S": k.survival_function_.iloc[:, 0].tolist(), "median": float(k.median_survival_time_),
                       "n": int(len(d))}
    out["km"] = km
    a, b = c[c.multi_home == 1], c[c.multi_home == 0]
    lr = logrank_test(a.dur, b.dur, a.has_takeoff, b.has_takeoff)
    out["logrank"] = {"stat": float(lr.test_statistic), "p": float(lr.p_value)}
    d = c[["dur", "has_takeoff", "multi_home", "early_volume", "group"]].dropna().copy()
    d["log_early_volume"] = np.log1p(d.early_volume)
    d = d.drop(columns=["early_volume"])
    try:
        cph = CoxPHFitter().fit(d, "dur", "has_takeoff", strata=["group"])
        s = cph.summary
        out["cox"] = {v: {"HR": float(s.loc[v, "exp(coef)"]), "ci": [float(s.loc[v, "exp(coef) lower 95%"]),
                                                                      float(s.loc[v, "exp(coef) upper 95%"])],
                          "p": float(s.loc[v, "p"])} for v in ("multi_home", "log_early_volume")}
    except Exception as e:  # noqa: BLE001
        out["cox"] = {"error": repr(e)[:300]}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=300)
    ap.add_argument("--workers", type=int, default=20)
    args = ap.parse_args()
    logger = setup_logger("sequence")
    from seal_m import check_seal
    check_seal()
    t = time.time()
    fr = frame_plus(load_frame())
    ph = primary_home(fr)
    yf = pd.read_parquet(DATA_IN / "yearly_features.parquet")
    yf["phome"] = yf.ci.map(ph)
    yf["prom"] = prominence(yf)
    p = pd.read_parquet(DATA_IN / "yearly_panel.parquet")
    ent = pd.concat([p[["ci", "year", "entries"]],
                     p.loc[p.year == p.h_end - 1, ["ci", "year", "entries_next"]].assign(year=lambda d: d.year + 1)
                     .rename(columns={"entries_next": "entries"})])
    c = concept_table(yf, ent, fr)
    c.to_parquet(DATA / "sequence_concepts.parquet", index=False)
    out: dict = {"definitions": __doc__, "n_concepts": int(len(c)),
                 "share_valid_peak": float(c.peak_valid.mean()), "share_takeoff": float(c.has_takeoff.mean())}
    for b in ("DEV", "OLD_HELDOUT", "COHORT", "ALL"):
        d = c if b == "ALL" else c[c.body == b]
        out[b] = {"share_test": share_test(d), "share_test_excl_Med": share_test(d[d.group != "Med"]),
                  "survival": survival(d)}
        logger.info(f"{b}: {out[b]['share_test']}")
    # (c) event studies (DEV, all bodies pooled as a secondary)
    from event_study import ES_CONTROLS, run_es
    pp = p.merge(yf[["ci", "year", "prom"]], on=["ci", "year"], how="left")
    pp = pp.merge(c[["ci", "peak_year", "peak_valid", "takeoff_year"]], on="ci")
    for b in ("DEV", "ALL"):
        d = pp if b == "ALL" else pp[pp.body == b]
        d = d[(d.at_risk_next > 0) & d.y_next.notna()].copy()
        d1 = d.assign(g=np.where(d.peak_valid == 1, d.peak_year, np.nan))
        out[f"es_entries_around_peak_{b}"] = run_es(d1, "y_next", ES_CONTROLS, "g", "never", args.boot, args.workers,
                                                    f"seq_peak_{b}")
        d2 = d[np.isfinite(d.prom)].assign(g=d.takeoff_year)
        out[f"es_prominence_around_takeoff_{b}"] = run_es(d2, "prom", ["log1p_home", "log1p_all"], "g", "never",
                                                          args.boot, args.workers, f"seq_takeoff_{b}")
        jdump(out, RES / "sequence_tests.json")
    out["seconds"] = time.time() - t
    jdump(out, RES / "sequence_tests.json")
    logger.info(f"sequence tests done in {(time.time()-t)/60:.1f} min")


if __name__ == "__main__":
    main()
