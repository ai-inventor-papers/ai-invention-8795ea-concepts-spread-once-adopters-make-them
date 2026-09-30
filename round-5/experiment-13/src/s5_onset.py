#!/usr/bin/env python3
"""S5a: ONSET (masked), SEAL-B, CONTAINMENT DEDUP, HOME (outcome-blind).

MaskedCounts gives N(ci, y) from OPEN rows only (open/passN_pre_agg.parquet for y < t_det-5, open/parts/early_*.parquet
for t_det-5..t_det+4) and raises on any read of y > t_det+4. t0 = first y in 2003..2014 with N(y) >= 20 and
N(y-k) < 0.25*N(y+2) for k = 1..3 (y <= t_det+2 by the mask; the finder stops at t0, so it never reads past t0+2 for a
retained phrase; asserted). Selection clause: t0 >= t_det-2. Extension table: t0 = 2015.
SEAL-B moves every open row with year >= t0+3 into sealed/parts/sealedB.parquet (hashed before any feature code).
Writes data/frame_n_onset.csv (+ extension), open/early_frame.parquet (years <= t0+2 only), results/s5_onset.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, GROUP_OF_FIELD, RES, ROOT, jdump, setup_logger, sha256_file
from sealn import SEALED_PARTS, log_sealed_parts, record

logger = setup_logger("s5_onset")
Y0 = 1995
NY = 2024 - Y0 + 1
FIELD_IDS = list(range(11, 37))
HOME_N = 30
OPEN_HI = 4          # v2 open window t_det-5..t_det+4 (passN.OPEN_HI)
ANALYSIS_GROUP = {"CS": "CS+Eng", "Eng": "CS+Eng", "BGM": "BGM+Med", "Med": "BGM+Med", "PHYS": "PHYS",
                  "LIFEENV": "LIFEENV", "SOC": "SOC", "MATHDEC": "MATHDEC"}


class MaskError(RuntimeError):
    pass


class MaskedCounts:
    """Yearly N(ci, y) from open rows; refuses y > limit(ci) and records the max year read per concept."""

    def __init__(self, N: dict[int, np.ndarray], limit: dict[int, int]):
        self.N, self.limit, self.max_read = N, limit, {}

    def __call__(self, ci: int, y: int) -> float:
        if y > self.limit[ci]:
            raise MaskError(f"read of year {y} > limit {self.limit[ci]} for ci {ci}")
        self.max_read[ci] = max(self.max_read.get(ci, -1), y)
        return float(self.N[ci][y - Y0]) if 0 <= y - Y0 < NY else 0.0


def find_t0(ci: int, mc: MaskedCounts, lo: int = 2003, hi: int = 2014) -> int | None:
    for y in range(lo, hi + 1):
        if y + 2 > mc.limit[ci]:
            return None
        n2 = mc(ci, y + 2)
        if mc(ci, y) >= 20 and all(mc(ci, y - k) < 0.25 * n2 for k in (1, 2, 3)):
            return y
    return None


def home_rule(V: np.ndarray, t0: int, n_first: int = HOME_N) -> dict:
    """EXP10 s1_candidates.home_rule (= EXP5 frame.home_rule, verbatim logic); V capped at t0+2 by the caller."""
    acc = np.zeros(26)
    got = 0.0
    for y in range(t0, Y0 + NY):
        row = V[y - Y0, 1:27].astype(float)
        tot = row.sum()
        if tot <= 0:
            continue
        need = n_first - got
        if tot <= need:
            acc += row
            got += tot
        else:
            acc += row * need / tot
            got += need
        if got >= n_first - 1e-9:
            break
    if got <= 0:
        return {"home": [], "status": "no_labels", "n_home": 0.0}
    sh = acc / got
    order = np.argsort(sh)[::-1]
    home = [FIELD_IDS[k] for k in range(26) if sh[k] >= 0.4]
    res = {"n_home": float(got), "top_share": float(sh[order[0]]), "second_share": float(sh[order[1]]),
           "intersect40": int(len(home) >= 2), "intersect25": int(sh[order[1]] >= 0.25), "weak_home": 0}
    if home:
        home = sorted(home, key=lambda f: -sh[f - 11])
        res.update(home=home, status="ok")
    elif sh[order[0]] >= 0.25:
        res.update(home=[FIELD_IDS[order[0]]], status="weak_home", weak_home=1)
    else:
        res.update(home=[], status="diffuse_born")
    return res


def contiguous_in(a: tuple, b: tuple) -> bool:
    n = len(a)
    return n < len(b) and any(b[i:i + n] == a for i in range(len(b) - n + 1))


@logger.catch(reraise=True)
def main() -> None:
    cand = pd.read_csv(DATA / "frame_n_candidates.csv", low_memory=False)
    cand = cand[cand.ci >= 0].set_index("ci")
    import pyarrow.dataset as pads
    pre = pd.read_parquet(ROOT / "open/passN_pre_agg.parquet")
    eds = pads.dataset(sorted(str(p) for p in (ROOT / "open/parts").glob("early_*.parquet")), format="parquet")
    early = eds.to_table(columns=["ci", "year", "vfield", "work_id"]).to_pandas().drop_duplicates(["ci", "work_id"])
    tdet = cand.t_det.to_dict()
    assert (early.year.to_numpy() <= early.ci.map(tdet).to_numpy() + OPEN_HI).all(), "open early row beyond t_det+4"
    assert (pre.year.to_numpy() < pre.ci.map(tdet).to_numpy() - 5).all(), "pre row inside the early window"
    # yearly N and V from open rows
    cis = cand.index.to_numpy()
    pos = pd.Series(np.arange(len(cis)), index=cis)
    Nm = np.zeros((len(cis), NY))
    Vm = np.zeros((len(cis), NY, 27))
    for d, w in ((pre, pre.n.to_numpy(float)), (early, np.ones(len(early)))):
        f = pos.loc[d.ci.to_numpy()].to_numpy()
        y = d.year.to_numpy(np.int64) - Y0
        np.add.at(Nm, (f, y), w)
        np.add.at(Vm, (f, y, d.vfield.to_numpy(np.int64)), w)
    mc = MaskedCounts({ci: Nm[pos[ci]] for ci in cis}, {ci: int(tdet[ci]) + OPEN_HI for ci in cis})
    rows, ext = [], []
    n_no_t0 = n_clause = 0
    for ci in cis:
        t0 = find_t0(int(ci), mc)
        if t0 is None:
            if tdet[ci] >= 2013:
                t0e = find_t0(int(ci), mc, 2015, 2015)
                if t0e is not None and t0e >= tdet[ci] - 2:
                    ext.append((int(ci), t0e))
            n_no_t0 += 1
            continue
        if t0 < tdet[ci] - 2:
            n_clause += 1
            continue
        rows.append((int(ci), t0))
    for ci, t0 in rows:
        assert mc.max_read[ci] <= t0 + 2, f"onset finder read beyond t0+2 for ci {ci}"
    logger.info(f"onset: {len(rows)} with t0 in 2003..2014; {len(ext)} extension (t0 2015); no t0 {n_no_t0}; "
                f"selection clause dropped {n_clause}")
    on = pd.DataFrame(rows + ext, columns=["ci", "t0"])
    on["extension"] = [0] * len(rows) + [1] * len(ext)
    on = on.merge(cand[["name", "key", "aliases", "t_det", "n_tokens"]].reset_index(), on="ci")
    # ------------------------------------------------------------------ SEAL-B
    t0_of = on.set_index("ci").t0
    e = eds.to_table(filter=pads.field("ci").isin(t0_of.index.tolist())).to_pandas().drop_duplicates(["ci", "work_id"])
    e["t0"] = e.ci.map(t0_of)
    moveB = e.year >= e.t0 + 3
    sb = e[moveB].groupby(["ci", "year", "vfield", "mt"]).size().rename("n").reset_index()
    sb.to_parquet(SEALED_PARTS / "sealedB.parquet", index=False)
    keep = e[~moveB].drop(columns=["t0"])
    keep = keep[keep.year >= keep.ci.map(t0_of) - 5]
    keep.to_parquet(ROOT / "open/early_frame.parquet", index=False, compression="zstd")
    # the per-file early parts contain years up to t_det+4 >= t0+3: remove them so no post-t0+2 detail row stays
    # readable (their content for frame concepts now lives in sealedB / early_frame)
    del eds
    for p in (ROOT / "open/parts").glob("early_*.parquet"):
        p.unlink()
    n_sealed = log_sealed_parts()
    record("S5_sealB", sealedB_sha256=sha256_file(SEALED_PARTS / "sealedB.parquet"), rows=int(len(sb)),
           n_sealed_parts=n_sealed, sealed_files_log_sha256=sha256_file(ROOT / "logs/sealed_files.log"))
    logger.info(f"SEAL-B: moved {int(moveB.sum())} detail rows ({len(sb)} agg rows) into sealedB; parts {n_sealed}")
    # ------------------------------------------------------------------ containment dedup (early counts only)
    N = {ci: Nm[pos[ci]].copy() for ci in on.ci}
    for ci, t0 in zip(on.ci, on.t0):
        N[ci][t0 + 3 - Y0:] = 0
    keys = {ci: tuple(k.split(" ")) for ci, k in zip(on.ci, on.key)}
    t0d = dict(zip(on.ci, on.t0))
    by_len = sorted(on.ci, key=lambda c: len(keys[c]))
    drop = set()
    from collections import defaultdict
    idx = defaultdict(list)                      # token -> concepts containing it (speed)
    for c in on.ci:
        for t in set(keys[c]):
            idx[t].append(c)
    n_pairs = 0
    for a in by_len:
        ka = keys[a]
        cands = set(idx[ka[0]])
        for t in ka[1:]:
            cands &= set(idx[t])
        for b in cands:
            if b == a or not contiguous_in(ka, keys[b]):
                continue
            n_pairs += 1
            y_hi = min(t0d[a], t0d[b]) + 2
            ys = [y for y in range(t0d[a], t0d[a] + 3) if y <= y_hi]
            na = sum(N[a][y - Y0] for y in ys)
            nb = sum(N[b][y - Y0] for y in ys)
            if nb >= 0.6 * na:
                drop.add(a)
            else:
                drop.add(b)
    logger.info(f"containment pairs {n_pairs}; dropped {len(drop)}")
    on = on[~on.ci.isin(drop)].copy()
    # ------------------------------------------------------------------ home
    recs = []
    for r in on.itertuples():
        V = Vm[pos[r.ci]].copy()
        V[r.t0 + 3 - Y0:] = 0
        h = home_rule(V, r.t0)
        g = GROUP_OF_FIELD[h["home"][0]] if h["home"] else None
        recs.append({"ci": r.ci, "home": ";".join(map(str, h["home"])), "home_status": h["status"],
                     "n_home_fields": len(h["home"]), "intersection_born": int(len(h["home"]) >= 2),
                     "weak_home": h.get("weak_home", 0), "home_top_share": h.get("top_share", np.nan),
                     "group": g, "agroup": ANALYSIS_GROUP.get(g) if g else None,
                     "N_t0": N[r.ci][r.t0 - Y0], "N_t0p2": N[r.ci][r.t0 + 2 - Y0],
                     "early_volume": float(N[r.ci][r.t0 - Y0:r.t0 + 3 - Y0].sum())})
    on = on.merge(pd.DataFrame(recs), on="ci")
    n_diffuse = int((on.home == "").sum())
    on = on[on.home != ""].copy()
    on.to_csv(DATA / "frame_n_onset.csv", index=False)
    summ = {"candidates": int(len(cand)), "no_t0": n_no_t0, "selection_clause_dropped": n_clause,
            "onset_2003_2014": len(rows), "extension_2015": len(ext), "containment_pairs": n_pairs,
            "containment_dropped": len(drop), "diffuse_born_dropped": n_diffuse, "after_s5a": int(len(on)),
            "after_s5a_main": int((on.extension == 0).sum()), "by_t0": on.t0.value_counts().sort_index().to_dict(),
            "by_group": on.agroup.value_counts().to_dict(), "sealB_rows": int(len(sb)),
            "max_read_ok": True}
    jdump(summ, RES / "s5_onset.json")
    logger.info(f"S5a: {summ}")


if __name__ == "__main__":
    main()
