#!/usr/bin/env python3
"""Step 4.8 API audit (<= 40 credits): for 40 random frame concepts, one group_by=publication_year call with a quoted
title.search + base filter; compare with the snapshot title-hit and grounded yearly counts.
The key is read from env OPENALEX_API_KEY only and is never written to disk (the credit log strips it)."""
from __future__ import annotations

import csv
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from loguru import logger
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from config import RES, SCAN, SEED, Y0  # noqa: E402

logger.remove(); logger.add(sys.stdout, format="{time:HH:mm:ss}|{level:<7}|{message}")
CAP = 40


@logger.catch(reraise=True)
def main() -> None:
    key = os.environ.get("OPENALEX_API_KEY")  # optional; the shared key was exhausted (HTTP 429) -> anonymous pool
    fc = pd.read_csv(RES / "frame_concepts.csv")
    pick = fc.sample(min(CAP, len(fc)), random_state=SEED)
    zz = np.load(SCAN / "agg_counts.npz")
    z = {"T_all": zz["T_all"], "T_tag": zz["T_tag"], "T_none": zz["T_none"]}
    log = RES / "credits_log.csv"
    new = not log.exists()
    rows = []
    with log.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time", "purpose", "status", "x_ratelimit_remaining", "credits_used_est"])
        for r in pick.itertuples():
            q = r.name.replace('"', "")
            params = {"filter": f'title.search:"{q}",type:article|review,is_paratext:false', "group_by": "publication_year",
                      **({"api_key": key} if key else {})}
            try:
                resp = requests.get("https://api.openalex.org/works", params=params, timeout=60)
            except requests.RequestException as e:
                logger.warning(f"{q}: {e!r}"); continue
            w.writerow([time.strftime("%H:%M:%S"), f"audit:{q}", resp.status_code, resp.headers.get("x-ratelimit-remaining", ""), 1])
            if resp.status_code != 200:
                logger.warning(f"{q}: HTTP {resp.status_code}"); continue
            api = {int(g["key"]): int(g["count"]) for g in resp.json().get("group_by", []) if str(g["key"]).isdigit()}
            ys = list(range(1998, 2023))
            snap_title = [int(z["T_all"][r.cidx, y - Y0].sum()) for y in ys]
            snap_g = [int((z["T_tag"][r.cidx, y - Y0] + z["T_none"][r.cidx, y - Y0]).sum()) for y in ys]
            a = [api.get(y, 0) for y in ys]
            t0 = int(r.t0)
            e_api = sum(api.get(y, 0) for y in range(t0, t0 + 3))
            e_g = sum(snap_g[ys.index(y)] for y in range(t0, t0 + 3))
            e_t = sum(snap_title[ys.index(y)] for y in range(t0, t0 + 3))
            rows.append({"name": q, "t0": t0, "rho_title_vs_api": spearmanr(snap_title, a).statistic,
                         "rho_grounded_vs_api": spearmanr(snap_g, a).statistic, "early_api": e_api, "early_grounded": e_g,
                         "early_title": e_t, "ratio_grounded_api": e_g / e_api if e_api else np.nan,
                         "ratio_title_api": e_t / e_api if e_api else np.nan})
            time.sleep(0.2)
    d = pd.DataFrame(rows)
    d.to_csv(RES / "api_audit.csv", index=False)
    out = {"n": len(d), "median_rho_title_vs_api": float(d.rho_title_vs_api.median()),
           "median_rho_grounded_vs_api": float(d.rho_grounded_vs_api.median()),
           "median_ratio_grounded_to_api_early": float(d.ratio_grounded_api.median()),
           "median_ratio_title_to_api_early": float(d.ratio_title_api.median()), "credits_used": len(d)}
    (RES / "api_audit.json").write_text(json.dumps(out, indent=1))
    logger.info(out)


if __name__ == "__main__":
    main()
