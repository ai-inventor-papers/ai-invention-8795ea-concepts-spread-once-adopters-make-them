#!/usr/bin/env python3
"""Step 1 (P0 prefilter, outcome-blind) + candidate frame for pass 2.
P0 uses the FULL pass-1 title-hit counts instead of a 5% file sample (deviation: the full scan was cheaper than planned).
Drop a concept if its title hits reach >= 200 in any year 1998-2002, or if its title hits cover > 0.5% of all base works.
Candidates = remaining concepts whose preliminary grounded yearly series (tag AND title + untagged-work title hits)
has onset t0 in 2003-2014 and >= 30 grounded works in t0..t0+2."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from config import RES, SCAN, Y0  # noqa: E402
from lib_outcomes import onset  # noqa: E402

logger.remove(); logger.add(sys.stdout, format="{time:HH:mm:ss}|{level:<7}|{message}")


@logger.catch(reraise=True)
def main() -> None:
    z = np.load(SCAN / "agg_counts.npz")
    lex = pd.read_parquet(RES / "lexicon.parquet")
    T_all = z["T_all"].sum(axis=2)  # [NC, NY]
    g = (z["T_tag"] + z["T_none"]).sum(axis=2)
    nbase = int(z["G"].sum())
    early = T_all[:, 1998 - Y0:2002 - Y0 + 1]
    drop_early = early.max(axis=1) >= 200
    drop_generic = T_all.sum(axis=1) > 0.005 * nbase
    rows = []
    for c in np.nonzero(~drop_early & ~drop_generic)[0]:
        yc = {Y0 + i: int(v) for i, v in enumerate(g[c]) if v}
        t0, nb = onset(yc)
        if not np.isfinite(t0) or not 2003 <= t0 <= 2014:
            continue
        t0 = int(t0)
        n_early = sum(yc.get(y, 0) for y in range(t0, t0 + 3))
        if n_early < 30:
            continue
        rows.append({"cidx": int(c), "t0_prelim": t0, "newborn_prelim": bool(nb), "n_early_prelim": n_early})
    cand = pd.DataFrame(rows).merge(lex[["concept_idx", "name", "level"]], left_on="cidx", right_on="concept_idx")
    cand.drop(columns="concept_idx").to_csv(RES / "candidates.csv", index=False)
    p0 = lex.loc[drop_early | drop_generic, ["concept_idx", "name"]].copy()
    p0["reason"] = np.where(drop_generic[p0.concept_idx], "generic_>0.5pct_titles", "early_>=200_hits_1998_2002")
    p0.to_csv(RES / "p0_dropped.csv", index=False)
    (SCAN / "cand_concepts.json").write_text(json.dumps({"cidx": cand.cidx.tolist()}))
    s = {"n_lexicon": len(lex), "p0_dropped_early": int(drop_early.sum()), "p0_dropped_generic": int(drop_generic.sum()),
         "n_after_p0": int((~drop_early & ~drop_generic).sum()), "n_candidates": len(cand),
         "n_candidates_newborn": int(cand.newborn_prelim.sum()),
         "t0_dist": cand.t0_prelim.value_counts().sort_index().to_dict()}
    (RES / "candidates_summary.json").write_text(json.dumps(s, indent=1, default=int))
    logger.info(s)


if __name__ == "__main__":
    main()
