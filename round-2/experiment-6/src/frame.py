#!/usr/bin/env python3
"""Step 4: frame concepts, home fields, splits, dev outcomes (held-out outcomes SEALED), episodes.
Grounded count g(c, y, f) = title&tag(>=0.3) hits + round(title hits on untagged works x p_sense(c)), where
p_sense(c) is the sense-filter mean probability on the concept's reservoir titles (grounding.py)."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from config import DEV_HOME, FIELD_GROUP, INP, NY, PREC_GATE, RES, SCAN, Y0  # noqa: E402
from frame_io import frozen, load_backbone  # noqa: E402
from lib_outcomes import home_of, onset, outcomes  # noqa: E402

logger.remove(); logger.add(sys.stdout, format="{time:HH:mm:ss}|{level:<7}|{message}")


def yr(y: int) -> int:
    return y - Y0


def concept_outcomes(g: np.ndarray, t0: int, G: np.ndarray) -> dict:
    tot = g.sum(1)
    yc = {Y0 + i: float(v) for i, v in enumerate(tot)}
    gtot = {Y0 + i: float(v) for i, v in enumerate(G)}
    fcD = g[yr(t0 + 6):yr(t0 + 8) + 1, 1:].sum(0)
    return outcomes(yc, gtot, t0, fcD)


def episode_outcome(g: np.ndarray, t0: int, j: int) -> int:
    return int(g[yr(t0 + 6):yr(t0 + 8) + 1, j - 10].sum() >= 2)


@logger.catch(reraise=True)
def main() -> None:
    z = np.load(SCAN / "agg_counts.npz")
    G, GF = z["G"], z["GF"]
    T_TAG, T_NONE, TPF = z["T_tag"], z["T_none"], z["TPF_tag"]
    cand = pd.read_csv(RES / "candidates.csv")
    cand = cand[cand.newborn_prelim]
    lex = pd.read_parquet(RES / "lexicon.parquet").set_index("concept_idx")
    gr_path = RES / "grounding_concepts.csv"
    gr = pd.read_csv(gr_path).set_index("cidx") if gr_path.exists() else pd.DataFrame()
    bb = load_backbone()
    gate = bb["g"]
    rows, eps, garr = [], [], {}
    drop = {"no_onset_after_grounding": 0, "precision_below_gate": 0, "n_early_lt30": 0, "no_labelled": 0}
    for c in cand.cidx:
        prec = float(gr.loc[c, "precision_est"]) if c in gr.index else np.nan
        pno = float(gr.loc[c, "p_notag"]) if c in gr.index and np.isfinite(gr.loc[c, "p_notag"]) else 1.0
        if np.isfinite(prec) and prec < PREC_GATE:
            drop["precision_below_gate"] += 1
            continue
        g = T_TAG[c].astype(float) + np.round(T_NONE[c] * pno)
        tot = g.sum(1)
        t0, nb = onset({Y0 + i: v for i, v in enumerate(tot)})
        if not np.isfinite(t0) or not 2003 <= t0 <= 2014:
            drop["no_onset_after_grounding"] += 1
            continue
        t0 = int(t0)
        n_early = float(tot[yr(t0):yr(t0) + 3].sum())
        if n_early < 30:
            drop["n_early_lt30"] += 1
            continue
        # home: venue fields of the first 30 labelled grounded works from t0 (last year taken proportionally)
        fc = np.zeros(26); need = 30.0
        for y in range(t0, min(t0 + 9, 2023)):
            v = g[yr(y), 1:]
            s = v.sum()
            if s <= 0:
                continue
            take = min(1.0, need / s)
            fc += v * take; need -= s * take
            if need <= 1e-9:
                break
        if fc.sum() == 0:
            drop["no_labelled"] += 1
            continue
        home, weak = home_of({11 + i: fc[i] for i in range(26) if fc[i] > 0})
        prim = home[0]
        grp = FIELD_GROUP[prim]
        if t0 <= 2009:
            split = "dev" if prim in DEV_HOME else "heldout_field"
        else:
            split = "heldout_cohort"
        early_tot = g[yr(t0):yr(t0) + 3].sum()
        lab_cov = float(g[yr(t0):yr(t0) + 3, 1:].sum() / early_tot) if early_tot else np.nan
        row = {"concept_id": lex.loc[c, "id"], "cidx": int(c), "name": lex.loc[c, "name"], "level": int(lex.loc[c, "level"]),
               "t0": t0, "newborn": bool(nb), "home": "|".join(map(str, home)), "home_primary": prim,
               "home_weak": bool(weak), "home_thin": bool(need > 1e-9), "intersection_born": int(len(home) >= 2),
               "group": grp, "split": split, "n_early": n_early, "label_coverage_early": lab_cov, "precision_est": prec,
               "p_notag": pno, "home_gateway": float(np.mean([gate[h - 11] for h in home]))}
        if split == "dev":
            row.update(concept_outcomes(g, t0, G))
        rows.append(row)
        garr[int(c)] = g
        for j in range(11, 37):
            if j in home:
                continue
            nj = g[yr(t0):yr(t0) + 3, j - 10].sum()
            if nj < 2:
                continue
            cum = np.cumsum(g[:, j - 10])
            ey = int(Y0 + np.argmax(cum >= 2))
            e = {"cidx": int(c), "field": j, "split": split, "group": grp, "t0": t0, "n_early_j": float(nj), "entry_year": ey,
                 "gateway_j": float(gate[j - 11]), "gateway_deg_j": float(bb["g_deg"][j - 11]),
                 "gateway_btw_j": float(bb["g_btw"][j - 11]),
                 "phi_home_j": float(np.mean([bb["phi"][h - 11, j - 11] for h in home])),
                 "log_size_j": float(math.log(max(GF[yr(t0 - 3):yr(t0 - 1) + 1, j - 11].sum(), 1))),
                 "label_coverage": lab_cov, "R_cj": episode_outcome(g, t0, j) if split == "dev" else np.nan}
            eps.append(e)
    fcdf = pd.DataFrame(rows)
    dev = fcdf.split == "dev"
    # O2r_resid: residual of O2r on log n_early, fitted on dev only (coefficients frozen later)
    d = fcdf[dev & fcdf.O2r_m30.notna()]
    coef = np.polyfit(np.log(d.n_early), d.O2r_m30, 1) if len(d) > 5 else [0.0, 0.0]
    fcdf.loc[dev, "O2r_resid"] = fcdf.loc[dev, "O2r_m30"] - np.polyval(coef, np.log(fcdf.loc[dev, "n_early"]))
    fcdf.to_csv(RES / "frame_concepts.csv", index=False)
    epdf = pd.DataFrame(eps)
    epdf.to_csv(RES / "episodes.csv", index=False)
    for sp, m in (("dev", fcdf.split == "dev"), ("heldout", fcdf.split != "dev")):
        ids = fcdf.loc[m, "cidx"].to_numpy()
        np.savez_compressed(SCAN / f"frame_g_{sp}.npz", cidx=ids, g=np.stack([garr[int(i)] for i in ids]) if len(ids) else np.zeros((0, NY, 27)))
        np.savez_compressed(SCAN / f"frame_gpf_{sp}.npz", cidx=ids,
                            g=np.stack([TPF[int(i)].astype(float) for i in ids]) if len(ids) else np.zeros((0, NY, 27)))
    summ = {"n_candidates": len(cand), "drops": drop, "n_frame": len(fcdf), "n_newborn": int(fcdf.newborn.sum()),
            "by_split": fcdf.split.value_counts().to_dict(),
            "by_split_newborn": fcdf[fcdf.newborn].split.value_counts().to_dict(),
            "by_group_newborn": {f"{a}|{b}": int(v) for (a, b), v in fcdf[fcdf.newborn].groupby(["split", "group"]).size().items()},
            "n_episodes": len(epdf), "episodes_by_split": epdf.split.value_counts().to_dict() if len(epdf) else {},
            "o2r_resid_coef_dev": list(map(float, coef)), "t0_dist": fcdf.t0.value_counts().sort_index().to_dict(),
            "home_primary_dist": fcdf.home_primary.value_counts().to_dict(),
            "label_coverage_by_home": fcdf.groupby("home_primary").label_coverage_early.median().round(3).to_dict()}
    (RES / "frame_summary.json").write_text(json.dumps({str(k): v for k, v in summ.items()}, indent=1, default=str))
    logger.info(json.dumps(summ, default=str)[:1500])


if __name__ == "__main__":
    main()
