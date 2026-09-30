"""Shared screen protocol S0: onset, newborn flag, home field, dev restriction, outcomes O1/O2r/O3, R_j, B5.

Credit-bound deviation D8 (documented): field labels for S0 (home, early/late field distributions, B5, O2r, R_j)
come from ONE group_by=primary_topic.field.id call per window (1 credit) instead of source group_by + venue
labelling of every source (hundreds of credits per concept). The candidate lineage feature keeps VENUE labels,
so outcome labels and feature labels come from different label systems (no shared-measurement leakage).
"""
from __future__ import annotations

import math
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from loguru import logger
from scipy.special import gammaln

from oa import CapReached, Client, OAError, SharedPoolLow
from panel import BASE_FILTER, DEV_FIELDS, search_filter

FIELD_GB = "primary_topic.field.id"


def yearly(cl: Client, c: dict) -> dict[int, int]:
    d = cl.get("/works", {"filter": f"{search_filter(c)},{BASE_FILTER}", "group_by": "publication_year"},
               summary=f"yc {c['canonical']}")
    return {int(g["key"]): g["count"] for g in d["group_by"] if str(g["key"]).isdigit()}


def global_counts(cl: Client) -> dict[int, int]:
    d = cl.get("/works", {"filter": BASE_FILTER, "group_by": "publication_year"}, summary="global G")
    return {int(g["key"]): g["count"] for g in d["group_by"] if str(g["key"]).isdigit()}


def field_counts(cl: Client, c: dict, y0: int, y1: int) -> dict[str, int]:
    d = cl.get("/works", {"filter": f"{search_filter(c)},{BASE_FILTER},publication_year:{y0}-{y1}",
                          "group_by": FIELD_GB}, summary=f"fields {c['canonical']} {y0}-{y1}")
    return {g["key_display_name"]: g["count"] for g in d["group_by"]
            if g["key_display_name"] and g["key"] not in ("unknown", None)}


def onset(yc: dict[int, int]) -> int | None:
    ys = [y for y in range(2000, 2015) if yc.get(y, 0) >= 20]
    return min(ys) if ys else None


def newborn(yc: dict[int, int], t0: int) -> bool:
    return all(yc.get(t0 - k, 0) < 0.25 * yc.get(t0 + 2, 0) for k in (1, 2, 3))


def home_fields(fc: dict[str, int]) -> list[str]:
    tot = sum(fc.values())
    if not tot:
        return []
    h = [f for f, n in fc.items() if n / tot >= 0.40]
    return h or [max(fc, key=fc.get)]


def rarefied_richness(counts: list[int], m: int) -> float:
    """Exact hypergeometric rarefaction E[S_m] = sum_j 1 - C(N-n_j, m)/C(N, m) (Hurlbert 1971)."""
    N = int(sum(counts))
    if N < m:
        return float("nan")

    def lnC(n: int, k: int) -> float:
        return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1) if 0 <= k <= n else -np.inf

    s = 0.0
    for n_j in counts:
        if n_j <= 0:
            continue
        s += 1 - (math.exp(lnC(N - n_j, m) - lnC(N, m)) if N - n_j >= m else 0.0)
    return s


def shannon(counts: list[int]) -> float:
    a = np.asarray([x for x in counts if x > 0], float)
    if a.sum() == 0:
        return 0.0
    p = a / a.sum()
    return float(-(p * np.log(p)).sum())


def fetch_s0(cl: Client, order: list[dict]) -> dict:
    """All raw S0 pulls in seeded order; returns {canonical: raw dict}. Stops cleanly on credit guards."""
    raw: dict[str, dict] = {}
    stop = None
    try:
        G = global_counts(cl)
    except (CapReached, SharedPoolLow) as e:
        return {"_G": None, "_stop": repr(e)}

    def counts(c: dict) -> tuple[str, dict | str]:
        try:
            return c["canonical"], yearly(cl, c)
        except (CapReached, SharedPoolLow, OAError) as e:
            return c["canonical"], repr(e)

    with ThreadPoolExecutor(3) as ex:
        for name, yc in ex.map(counts, order):
            raw[name] = {"yc": yc}
    # windows only for concepts with an onset in the dev window
    def windows(c: dict) -> tuple[str, dict]:
        r = raw[c["canonical"]]
        out: dict = {}
        if not isinstance(r["yc"], dict):
            return c["canonical"], out
        t0 = onset(r["yc"])
        if t0 is None or not 2003 <= t0 <= 2009:
            return c["canonical"], out
        try:
            out["f_t0_t1"] = field_counts(cl, c, t0, t0 + 1)
            if any(h not in DEV_FIELDS for h in home_fields(out["f_t0_t1"])):
                return c["canonical"], out  # sealed: fetch nothing further
            out["f_early"] = field_counts(cl, c, t0, t0 + 4)
            out["f_t3_t4"] = field_counts(cl, c, t0 + 3, t0 + 4)
            out["f_late"] = field_counts(cl, c, t0 + 6, t0 + 8)
        except (CapReached, SharedPoolLow, OAError) as e:
            out["error"] = repr(e)
        return c["canonical"], out

    with ThreadPoolExecutor(3) as ex:
        for name, w in ex.map(windows, order):
            raw[name].update(w)
    raw["_G"] = G
    raw["_stop"] = stop
    return raw


def compute_s0(raw: dict, order: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """Returns (outcome rows for all concepts incl. dropped, field-retention rows, dropped rows)."""
    G = {int(k): v for k, v in raw["_G"].items()}
    rows, frows, dropped = [], [], []
    for c in order:
        name = c["canonical"]
        r = raw.get(name, {})
        yc = r.get("yc")
        if isinstance(yc, dict):
            yc = {int(k): v for k, v in yc.items()}
        row = {"concept": name, "panel_group": c["panel_group"]}
        if not isinstance(yc, dict):
            dropped.append({"concept": name, "reason": f"no_counts:{yc}"})
            continue
        t0 = onset(yc)
        row.update(t0=t0, yc={str(k): v for k, v in sorted(yc.items()) if 1995 <= k <= 2025})
        if t0 is None:
            dropped.append({"concept": name, "reason": "no_onset"})
            continue
        row["newborn"] = newborn(yc, t0)
        if not 2003 <= t0 <= 2009:
            dropped.append({"concept": name, "reason": "t0_out_of_dev"})
            continue
        f01 = r.get("f_t0_t1")
        if f01 is None:
            dropped.append({"concept": name, "reason": f"no_home_data:{r.get('error')}"})
            continue
        H = home_fields(f01)
        sealed = [h for h in H if h not in DEV_FIELDS]
        if sealed:
            dropped.append({"concept": name, "reason": f"home_sealed:{sealed[0]}"})
            continue
        if "f_late" not in r:
            dropped.append({"concept": name, "reason": f"no_window_data:{r.get('error')}"})
            continue
        dev_group = max(H, key=lambda h: f01.get(h, 0))
        fe, fl, f34 = r["f_early"], r["f_late"], r["f_t3_t4"]
        Ne, Nl = sum(fe.values()), sum(fl.values())
        tot_e = sum(yc.get(y, 0) for y in range(t0, t0 + 5))
        tot_l = sum(yc.get(y, 0) for y in range(t0 + 6, t0 + 9))
        share = lambda y: yc.get(y, 0) / G[y]
        o1 = int(np.mean([share(y) for y in range(t0 + 6, t0 + 9)]) >= share(t0 + 5))
        peak = max(yc.get(y, 0) for y in range(t0 + 3, t0 + 9))
        tail = np.mean([yc.get(t0 + 7, 0), yc.get(t0 + 8, 0)])
        o3 = int(tail == 0 or peak / tail >= 2)
        lc = list(fl.values())
        row.update(
            home="|".join(H), dev_group=dev_group,
            label_coverage_early=Ne / tot_e if tot_e else np.nan,
            label_coverage_late=Nl / tot_l if tot_l else np.nan,
            O1=o1, O2r=rarefied_richness(lc, 30), O2r_m50=rarefied_richness(lc, 50),
            O2r_m20=rarefied_richness(lc, 20), O3=o3, N_late=Nl, O2r_hurdle=int(Nl >= 30),
            # B5
            B_logvol=math.log1p(tot_e),
            B_growth=math.log((yc.get(t0 + 4, 0) + 1) / (yc.get(t0 + 1, 0) + 1)),
            B_offhome=(sum(n for f, n in fe.items() if f not in H) / Ne) if Ne else np.nan,
            B_entropy=shannon(list(fe.values())),
            B_nfields=sum(1 for n in fe.values() if n >= 2),
            off_early_vol=math.log1p(sum(n for f, n in fe.items() if f not in H)),
            off_growth=math.log((sum(n for f, n in f34.items() if f not in H) + 1)
                                / (sum(n for f, n in f01.items() if f not in H) + 1)),
        )
        rows.append(row)
        for j, nje in fe.items():
            if j in H or nje < 5:
                continue
            njl = fl.get(j, 0)
            se, sl = nje / Ne, (njl / Nl if Nl else 0.0)
            frows.append({"concept": name, "field": j, "dev_group": dev_group,
                          "R_j": int(sl >= 0.5 * se and njl >= 9), "n_j_early": nje, "n_j_late": njl,
                          "log_n_j_early": math.log(nje),
                          "growth_j": math.log((f34.get(j, 0) + 1) / (f01.get(j, 0) + 1)),
                          "share_j": se})
    logger.info(f"S0: {len(rows)} dev concepts, {len(frows)} field units, {len(dropped)} dropped")
    return rows, frows, dropped
