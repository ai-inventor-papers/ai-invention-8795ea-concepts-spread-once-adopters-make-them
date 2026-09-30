#!/usr/bin/env python3
"""S6 SEQUENCE TEST, LIGHT (secondary). A = home-prominence half-peak age (first age 0..8 with HP >= 0.5 max HP);
T = off-home take-off age (first age 0..8 with new_entries >= 2 or n_ret >= 1). Order shares A < T / tie / A > T,
against a MECHANICAL-LAG NULL (1,000 within-concept permutations of the HP series); intersection-born vs single-home
take-off (Kaplan-Meier; discrete-time cloglog hazard with group and age FE, concept-clustered SE).
Verdict words only: HOME-FIRST / INTERSECTION-ROUTE / MIXED.

Usage: python s6_sequence.py --scope dev | heldout"""
from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from common import DATA, DISCLOSURE, RES, ROOT, SEED, jdump, load_outcomes, network_guard, setup_logger, update_status  # noqa: E402

network_guard()
logger = setup_logger("s6_sequence")
AG = np.arange(9)
N_PERM = 1000
N_BOOT = 2000
RULE = ("HOME-FIRST if the excess share of A < T over the mechanical-lag null is > 0 (95% CI > 0) and the "
        "intersection-born take-off hazard ratio CI does not lie above 1; INTERSECTION-ROUTE if the hazard ratio CI "
        "lies above 1 and the excess-share CI does not lie above 0; MIXED otherwise.")


def first_age(mask: np.ndarray) -> np.ndarray:
    return np.where(mask.any(1), mask.argmax(1), -1)


def half_peak(HP: np.ndarray) -> np.ndarray:
    mx = HP.max(-1, keepdims=True)
    a = first_age(HP >= 0.5 * mx) if HP.ndim == 2 else None
    return np.where(mx[..., 0] > 0, a, -1)


def table(cis: np.ndarray) -> tuple[pd.DataFrame, np.ndarray]:
    P = pd.read_parquet(ROOT / "panel.parquet", columns=["ci", "age", "HP", "new_entries", "n_ret"])
    P = P[P.age.isin(AG)].set_index(["ci", "age"]).sort_index()
    HP = P.HP.unstack("age").loc[cis].to_numpy(float)
    NE = P.new_entries.unstack("age").loc[cis].to_numpy(float)
    NR = P.n_ret.unstack("age").loc[cis].to_numpy(float)
    A = half_peak(HP)
    T = first_age((NE >= 2) | (NR >= 1))
    return pd.DataFrame({"ci": cis, "A": A, "T": T}), HP


def analyse(J: pd.DataFrame, label: str, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    D, HP = table(J.ci.to_numpy())
    D = D.merge(J[["ci", "intersection_born", "group", "early_volume", "OPEN_home", "OPEN_all"]], on="ci")
    both = (D.A >= 0) & (D["T"] >= 0)
    d = D[both]
    obs = {"n": int(both.sum()), "A_lt_T": float((d.A < d["T"]).mean()), "tie": float((d.A == d["T"]).mean()),
           "A_gt_T": float((d.A > d["T"]).mean()), "n_no_takeoff": int((D["T"] < 0).sum())}
    # mechanical-lag null: permute each concept's HP series (ages 0..8) N_PERM times
    Hb = HP[both.to_numpy()]
    Tb = d["T"].to_numpy()
    p_lt = np.zeros(len(Hb))
    p_tie = np.zeros(len(Hb))
    for s in range(0, N_PERM, 100):
        idx = np.argsort(rng.random((100, len(Hb), 9)), axis=2)
        Hp = np.take_along_axis(np.broadcast_to(Hb, (100,) + Hb.shape), idx, axis=2)
        mx = Hp.max(2, keepdims=True)
        Ap = (Hp >= 0.5 * mx).argmax(2)
        p_lt += (Ap < Tb[None, :]).sum(0)
        p_tie += (Ap == Tb[None, :]).sum(0)
    p_lt /= N_PERM
    p_tie /= N_PERM
    ex = (d.A.to_numpy() < Tb).astype(float) - p_lt
    bs = np.array([ex[rng.integers(0, len(ex), len(ex))].mean() for _ in range(N_BOOT)])
    null = {"null_A_lt_T": float(p_lt.mean()), "null_tie": float(p_tie.mean()), "excess_A_lt_T": float(ex.mean()),
            "excess_ci": np.percentile(bs, [2.5, 97.5]).tolist()}
    # intersection-born vs single-home: KM and discrete-time cloglog hazard
    from lifelines import KaplanMeierFitter
    km = {}
    dur = np.where(D["T"] >= 0, D["T"], 8).astype(float)
    ev = (D["T"] >= 0).astype(int)
    for f in (0, 1):
        m = (D.intersection_born == f).to_numpy()
        k = KaplanMeierFitter().fit(dur[m], ev[m])
        km[str(f)] = {"n": int(m.sum()), "S": k.survival_function_at_times(AG).round(4).tolist(),
                      "share_T_le_2": float(((D["T"] >= 0) & (D["T"] <= 2))[m].mean())}
    rows = []
    for r in D.itertuples():
        last = r.T if r.T >= 0 else 8
        for a in range(0, int(last) + 1):
            rows.append((r.ci, a, int(r.T == a), r.intersection_born, np.log(r.early_volume), r.group))
    pp = pd.DataFrame(rows, columns=["ci", "age", "y", "ib", "lv", "group"])
    haz = {}
    try:
        import statsmodels.api as sm
        X = pd.get_dummies(pp[["ib", "lv"]].assign(age=pp.age.astype(str), group=pp.group), drop_first=True,
                           dtype=float)
        X = sm.add_constant(X)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fit = sm.GLM(pp.y, X, family=sm.families.Binomial(sm.families.links.CLogLog())).fit(
                cov_type="cluster", cov_kwds={"groups": pd.factorize(pp.ci)[0]})
        b, se = float(fit.params["ib"]), float(fit.bse["ib"])
        haz = {"n_person_periods": len(pp), "n_concepts": int(pp.ci.nunique()), "coef_ib": b, "se": se,
               "HR": float(np.exp(b)), "HR_ci": [float(np.exp(b - 1.96 * se)), float(np.exp(b + 1.96 * se))],
               "p": float(fit.pvalues["ib"]), "coef_logvol": float(fit.params["lv"])}
    except (ValueError, np.linalg.LinAlgError) as e:
        haz = {"error": repr(e)[:300]}
    ib_open = D.groupby("intersection_born")[["OPEN_home", "OPEN_all"]].mean().to_dict(orient="index")
    hp_up = bool(null["excess_ci"][0] > 0)
    hr_up = bool(haz.get("HR_ci", [0, 0])[0] > 1)
    verdict = ("HOME-FIRST" if hp_up and not hr_up else "INTERSECTION-ROUTE" if hr_up and not
               null["excess_ci"][0] > 0 else "MIXED")
    logger.info(f"{label}: n {obs['n']}; A<T {obs['A_lt_T']:.3f} vs null {null['null_A_lt_T']:.3f}; excess "
                f"{null['excess_A_lt_T']:.3f} {np.round(null['excess_ci'], 3).tolist()}; HR {haz.get('HR', np.nan):.3f} "
                f"{np.round(haz.get('HR_ci', [np.nan, np.nan]), 3).tolist()} -> {verdict}")
    return {"label": label, "order": obs, "mechanical_lag_null": null, "km": km, "cloglog_hazard": haz,
            "open_by_intersection_flag": ib_open, "verdict": verdict}


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", default="dev", choices=["dev", "heldout"])
    a = ap.parse_args()
    J = pd.read_parquet(DATA / "joined.parquet").merge(
        pd.read_parquet(ROOT / "open_features.parquet")[["ci", "OPEN_home", "OPEN_all"]], on="ci")
    res = {"definitions": {"A": "first age 0..8 with HP >= 0.5 * max_{0..8} HP (HP = home-field papers per 10k "
                                "home-field works)", "T": "first age 0..8 with new_entries >= 2 or n_ret >= 1",
                           "null": f"{N_PERM} within-concept permutations of the HP series",
                           "verdict_rule": RULE}}
    if a.scope == "dev":
        res["DEV"] = analyse(J[J.split == "DEV"], "DEV", SEED + 1000)
        res["Source"] = "s6_sequence.py --scope dev; panel.parquet (S3)"
        jdump(res, RES / "sequence_light_dev.json")
        update_status("S6_sequence_DEV", {"sequence_dev_verdict": res["DEV"]["verdict"]})
    else:
        load_outcomes().all()
        res["disclosure"] = DISCLOSURE
        res["HELDOUT"] = analyse(J[J.split == "HELDOUT"], "HELDOUT", SEED + 1100)
        res["COHORT"] = analyse(J[J.split == "COHORT"], "COHORT", SEED + 1200)
        res["Source"] = "s6_sequence.py --scope heldout; panel.parquet (S3)"
        jdump(res, RES / "sequence_light_heldout.json")
        update_status("S6_sequence_heldout", {"sequence_heldout_verdicts": {k: res[k]["verdict"]
                                                                            for k in ("HELDOUT", "COHORT")}})


if __name__ == "__main__":
    main()
