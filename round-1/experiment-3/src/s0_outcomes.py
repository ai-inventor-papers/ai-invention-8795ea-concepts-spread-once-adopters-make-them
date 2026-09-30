#!/usr/bin/env python3
"""S0 shared protocol: onset, newborn flag, dev restriction, venue-field windows, outcomes (O1, O2r, O3, R_j)
and the B5 / B_field reference baselines.

Grounding: yearly counts n[y] come from the S0-exact API call (quoted phrase, title_and_abstract.search,
type:article|review, is_paratext:false). Venue-field compositions (home field, O2r, R_j, early entropy/reach)
come from the title-matched base works of the full snapshot scan, because the shared key was exhausted
(deviation logged). Writes results/outcomes.csv and results/field_outcomes.csv."""
from __future__ import annotations

import math
import sys
from collections import Counter

import numpy as np
import pandas as pd
from loguru import logger

from common import load_api_yearly, load_matches, load_source_field, rarefy, shannon
from config import (DEV_FIELDS, DEV_T0, HOME_SHARE, LOGS, ORDER, PANEL, RAREFY_M, RAREFY_M_SENS, RES, T0_MIN_COUNT)


def onset(n: dict[int, int]) -> tuple[int | None, bool | None]:
    t0 = next((y for y in range(2000, 2015) if n.get(y, 0) >= T0_MIN_COUNT), None)
    if t0 is None:
        return None, None
    newborn = all(n.get(t0 - k, 0) < 0.25 * n.get(t0 + 2, 0) for k in (1, 2, 3))
    return t0, newborn


def field_counts(df: pd.DataFrame, years: list[int], sfield: dict) -> tuple[Counter, int, int]:
    sub = df[df.year.isin(years)]
    labs = [sfield.get(s) if s is not None and not (isinstance(s, float) and math.isnan(s)) else None
            for s in sub.source]
    c = Counter(l for l in labs if l is not None)
    return c, int(sum(c.values())), int(len(sub))


def home_fields(c: Counter) -> list[int]:
    tot = sum(c.values())
    if tot == 0:
        return []
    h = sorted([f for f, v in c.items() if v / tot >= HOME_SHARE], key=lambda f: -c[f])
    return h or [c.most_common(1)[0][0]]


def build(matches: pd.DataFrame | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    api, G = load_api_yearly()
    sfield = load_source_field()
    if matches is None:
        matches = load_matches()
    rows, frows = [], []
    for i in ORDER:
        name = PANEL[i][0]
        n = api.get(name)
        r = {"concept": name, "panel_group": PANEL[i][2], "order_pos": ORDER.index(i), "dropped_reason": ""}
        if n is None:
            r["dropped_reason"] = "no_api_counts"
            rows.append(r)
            continue
        t0, newborn = onset(n)
        r.update(t0=t0, newborn=newborn)
        if t0 is None:
            r["dropped_reason"] = "no_onset"
            rows.append(r)
            continue
        if not (DEV_T0[0] <= t0 <= DEV_T0[1]):
            r["dropped_reason"] = "t0_outside_dev_cohort"
            rows.append(r)
            continue
        d = matches[matches.ci == i]
        WH, WE2, WO = [t0, t0 + 1], [t0 + 2, t0 + 3, t0 + 4], [t0 + 6, t0 + 7, t0 + 8]
        cH, labH, totH = field_counts(d, WH, sfield)
        home_win = "t0..t0+1"
        if labH < 5:  # too few labelled title matches for a home decision: widen to t0..t0+2 (flagged)
            cH, labH, totH = field_counts(d, [t0, t0 + 1, t0 + 2], sfield)
            home_win = "t0..t0+2"
        home = home_fields(cH)
        r.update(n_title_WH=totH, lab_WH=labH, cov_WH=labH / totH if totH else np.nan, home_window=home_win,
                 home=";".join(str(h) for h in home))
        if not home:
            r["dropped_reason"] = "no_labelled_home_papers"
            rows.append(r)
            continue
        out_dev = [h for h in home if h not in DEV_FIELDS]
        if out_dev:
            r["dropped_reason"] = f"home_outside_dev:{out_dev[0]}"
            rows.append(r)
            continue
        grp = home[0]
        r["group"] = DEV_FIELDS[grp]
        r["group_id"] = grp
        cE2, labE2, totE2 = field_counts(d, WE2, sfield)
        cEarly = cH if home_win == "t0..t0+1" else field_counts(d, [t0, t0 + 1], sfield)[0]
        cEarly = cEarly + cE2
        labE = sum(cEarly.values())
        totE = int(d.year.isin(range(t0, t0 + 5)).sum())
        cO, labO, totO = field_counts(d, WO, sfield)
        r.update(n_title_early=totE, lab_early=labE, cov_early=labE / totE if totE else np.nan,
                 n_title_WO=totO, N_WO=labO, cov_WO=labO / totO if totO else np.nan)
        # ---- outcomes
        r["O2r"] = rarefy(list(cO.values()), RAREFY_M)
        r["O2r_m50"] = rarefy(list(cO.values()), RAREFY_M_SENS)
        r["reach30"] = int(labO >= RAREFY_M)
        share = lambda y: n.get(y, 0) / G[y] if G.get(y) else np.nan  # noqa: E731
        r["O1"] = int(np.mean([share(y) for y in WO]) >= share(t0 + 5))
        win = list(range(t0 + 3, t0 + 9))
        peak = max(win, key=lambda y: n.get(y, 0))
        tail = np.mean([n.get(t0 + 7, 0), n.get(t0 + 8, 0)])
        r["O3"] = int(n.get(peak, 0) >= max(n.get(y, 0) for y in win) and
                      (n.get(peak, 0) / tail >= 2 if tail > 0 else True))
        r["O2_raw_fields"] = len(cO)
        # ---- B5 baseline (t0..t0+4)
        r["logvol"] = math.log(sum(n.get(y, 0) for y in range(t0, t0 + 5)))
        r["growth"] = math.log((n.get(t0 + 4, 0) + 1) / (n.get(t0 + 1, 0) + 1))
        off = sum(v for f, v in cEarly.items() if f not in home)
        r["offhome_share"] = off / labE if labE else np.nan
        r["entropy"] = shannon(list(cEarly.values()))
        r["nfields2"] = sum(1 for v in cEarly.values() if v >= 2)
        r["n_api_early"] = sum(n.get(y, 0) for y in range(t0, t0 + 5))
        r["n_api_WO"] = sum(n.get(y, 0) for y in WO)
        # ---- field-level retention R_j and B_field
        cH2 = field_counts(d, [t0, t0 + 1], sfield)[0]
        for j, nj in cEarly.items():
            if j in home or nj < 5:
                continue
            sh_e = nj / labE
            sh_o = cO.get(j, 0) / labO if labO else 0.0
            frows.append({"concept": name, "field": j, "group": r["group"],
                          "R_j": int(sh_o >= 0.5 * sh_e and cO.get(j, 0) >= 9),
                          "n_j_early": nj, "logn_j_early": math.log1p(nj),
                          "growth_j": math.log((cE2.get(j, 0) / 3 + 1) / (cH2.get(j, 0) / 2 + 1)),
                          "share_j": sh_e, "n_j_WO": cO.get(j, 0), "share_j_WO": sh_o})
        rows.append(r)
    return pd.DataFrame(rows), pd.DataFrame(frows)


def main() -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / "s0_outcomes.log", rotation="30 MB", level="DEBUG")
    out, fout = build()
    out.to_csv(RES / "outcomes.csv", index=False)
    fout.to_csv(RES / "field_outcomes_base.csv", index=False)
    logger.info(f"dev concepts kept: {(out.dropped_reason == '').sum()}  dropped: "
                f"{out[out.dropped_reason != ''].dropped_reason.str.split(':').str[0].value_counts().to_dict()}")


if __name__ == "__main__":
    main()
