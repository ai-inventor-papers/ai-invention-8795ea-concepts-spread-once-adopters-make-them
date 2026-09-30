#!/usr/bin/env python3
"""S2: raw + resampling variants per concept (HOME build, concepts with n_home_early >= 10), checkpointed per chunk.

Per concept (fast6 engine, SELF fixed at the full-build set):
  RAW     the six components on the full home build (must equal EXP10 values), NB sets W1..W3, window counts
  V1      rarefaction: for n in N_RARE, if every W-year has >= n papers: n papers per W-year + min(|PRE|, 3n) PRE,
          D_RARE draws, nanmean (>= half finite)
  V2      within-concept year-label permutation null (D_PERM permutations; PRE fixed): null mean / sd, excess, zperm
  V2b     Chao 2005 abundance Jaccard persistence (non-SELF topic count vectors, W1-W2 and W2-W3)
  V4raw   S_RAW split-halves (within window): the six components on each half
  V4clean first S_CLEAN of those splits: V2 (D_PERM_HALF perms per half) and V1 n=5 (D_RARE_HALF draws per half,
          concepts with >= 10 papers per W-year); the half NB sets are kept for the V3 half-nulls
Usage: python s2_variants.py [--limit N] [--sample-per-body N] [--tag TAG] [--workers 3] [--draws-scale 1.0]"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import pickle
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, RES, setup_logger

from s2_cfg import CFG_FULL
CFG_DEFAULT = {k: v for k, v in CFG_FULL.items() if not k.startswith("V3")}
V2_METRICS = ["edge_persistence", "NOV_res", "ego_density_W3", "new_edge_rate", "n_comm_W3", "participation"]
_G: dict = {}


def seed_key(frame: str, ci: int) -> int:
    return int(ci) + (0 if frame == "exp5" else 100000)


def _init(cfg: dict) -> None:
    import ego
    from ego_ctx import rq1_context
    from jobs import build_home_cache
    warnings.simplefilter("ignore", RuntimeWarning)
    ego.set_context(rq1_context())
    _G["cache"] = build_home_cache()
    _G["cfg"] = cfg


def _nanagg(v: np.ndarray, min_fin: int) -> tuple[float, float, int]:
    f = np.isfinite(v)
    if f.sum() < min_fin:
        return float("nan"), float("nan"), int(f.sum())
    return float(v[f].mean()), float(v[f].std()), int(f.sum())


def v2_block(P: dict, lab: np.ndarray, obs: dict, D: int, rng) -> dict:
    from fast6 import fast6, permute_labels
    r = fast6(P, permute_labels(lab, D, rng))
    out = {}
    for m in V2_METRICS:
        mu, sd, nf = _nanagg(r[m], D // 2)
        o = float(obs[m])
        out[f"{m}_nullmean"] = mu
        out[f"{m}_nullsd"] = sd
        out[f"{m}_exc"] = o - mu if np.isfinite(o) and np.isfinite(mu) else float("nan")
        out[f"{m}_zperm"] = out[f"{m}_exc"] / sd if np.isfinite(out[f"{m}_exc"]) and sd > 0 else float("nan")
    return out


def v1_block(P: dict, lab: np.ndarray, n: int, D: int, rng) -> dict | None:
    from fast6 import OUT6, fast6, rarefy_labels
    if any((lab == w).sum() < n for w in (1, 2, 3)):
        return None
    r = fast6(P, rarefy_labels(lab, n, D, rng))
    return {m: _nanagg(r[m], (D + 1) // 2)[0] for m in OUT6}


def one_concept(key: tuple) -> tuple[dict, dict]:
    from fast6 import OUT6, chao_jaccard, fast6, half_split, prep
    cfg = _G["cfg"]
    c = _G["cache"][key]
    frame, ci = key
    sk = seed_key(frame, ci)
    P = prep(c["name"], c["aliases"], c["t0"], c["works"])
    lab = P["lab"]
    row: dict = {"frame": frame, "ci": int(ci), "body": c["body"], "t0": c["t0"], "n_home_early": c["n_home_early"],
                 "n_home_pre": int((lab == 0).sum()), "n_W1": int((lab == 1).sum()), "n_W2": int((lab == 2).sum()),
                 "n_W3": int((lab == 3).sum()), "n_self": int(P["SELF"].sum()), "n_cand": int(len(P["cand"]))}
    raw = fast6(P, lab[None, :], return_sets=True, return_counts=True)
    obs = {m: float(raw[m][0]) for m in list(OUT6) + ["M", "deg_W1", "deg_W3", "e_W3"]}
    row.update({f"{m}__raw": v for m, v in obs.items()})
    row["min_year_n"] = int(min(row["n_W1"], row["n_W2"], row["n_W3"]))
    extra: dict = {"NB": {w: P["cg"][raw["NB"][w][0]].astype(np.int32) for w in (1, 2, 3)},
                   "SELF": np.nonzero(P["SELF"])[0].astype(np.int32)}
    # V2b Chao
    ns = ~P["selfU"]
    cw = {w: raw["cnt"][w][0][ns] for w in (1, 2, 3)}
    j12, j23 = chao_jaccard(cw[1], cw[2]), chao_jaccard(cw[2], cw[3])
    fin = [j for j in (j12, j23) if np.isfinite(j)]
    row["EP_chao"] = float(np.mean(fin)) if fin else float("nan")
    # V1 rarefaction
    for n in cfg["N_RARE"]:
        rng = np.random.default_rng([7000000, sk, n])
        r = v1_block(P, lab, n, cfg["D_RARE"], rng)
        for m in OUT6:
            row[f"{m}_rare{n}"] = r[m] if r is not None else float("nan")
    # V2 permutation null
    rng = np.random.default_rng([8000000, sk])
    row.update(v2_block(P, lab, obs, cfg["D_PERM"], rng))
    # V4 split halves
    rng = np.random.default_rng([9000000, sk])
    LA, LB = half_split(lab, cfg["S_RAW"], rng)
    ra = fast6(P, LA, return_sets=True)
    rb = fast6(P, LB, return_sets=True)
    extra["half_raw"] = {h: np.stack([r[m] for m in OUT6], 1).astype(np.float32) for h, r in (("A", ra), ("B", rb))}
    S = cfg["S_CLEAN"]
    extra["half_NB"] = {h: [[P["cg"][r["NB"][w][s]].astype(np.int32) for w in (1, 2, 3)] for s in range(S)]
                        for h, r in (("A", ra), ("B", rb))}
    rng_p = np.random.default_rng([9100000, sk])
    rng_r = np.random.default_rng([9200000, sk])
    hc: dict = {}
    for h, L, r in (("A", LA, ra), ("B", LB, rb)):
        rows_h = []
        for s in range(S):
            obs_h = {m: float(r[m][s]) for m in OUT6}
            d = v2_block(P, L[s], obs_h, cfg["D_PERM_HALF"], rng_p)
            rr = v1_block(P, L[s], cfg["RARE_HALF_N"], cfg["D_RARE_HALF"], rng_r)
            d.update({f"{m}_rare{cfg['RARE_HALF_N']}": (rr[m] if rr is not None else float("nan")) for m in OUT6})
            rows_h.append(d)
        hc[h] = pd.DataFrame(rows_h).astype(np.float32)
    extra["half_clean"] = hc
    return row, extra


def run_chunk(k: int, keys: list) -> tuple[int, list, list, float]:
    t = time.time()
    rows, extras = [], []
    for key in keys:
        try:
            r, e = one_concept(key)
        except (ValueError, IndexError, ZeroDivisionError, FloatingPointError) as ex:
            r, e = {"frame": key[0], "ci": int(key[1]), "s2_error": repr(ex)[:200]}, {}
        rows.append(r)
        extras.append(e)
    return k, rows, extras, time.time() - t


def select_keys(cache: dict, min_home: int, sample_per_body: int, seed: int = 5) -> list:
    keys = sorted(k for k, v in cache.items() if v["n_home_early"] >= min_home)
    if sample_per_body:
        rng = np.random.default_rng(seed)
        out = []
        for b in ("DEV", "OLDHO", "COH1014", "COH1517"):
            kb = [k for k in keys if cache[k]["body"] == b]
            out += [kb[i] for i in sorted(rng.choice(len(kb), min(sample_per_body, len(kb)), replace=False))]
        keys = out
    return keys


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--sample-per-body", type=int, default=0)
    ap.add_argument("--tag", default="full")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--chunk", type=int, default=100)
    ap.add_argument("--cfg", default="")
    a = ap.parse_args()
    logger = setup_logger(f"s2_variants_{a.tag}")
    cfg = dict(CFG_DEFAULT)
    if a.cfg:
        cfg.update(json.loads(a.cfg))
    from jobs import build_home_cache
    cache = build_home_cache()
    keys = select_keys(cache, cfg["MIN_HOME"], a.sample_per_body)
    if a.limit:
        keys = keys[:a.limit]
    # big concepts first so the tail is short
    keys.sort(key=lambda k: -len(cache[k]["works"]))
    del cache
    outdir = DATA / f"s2_parts_{a.tag}"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "cfg.json").write_text(json.dumps(cfg))
    chunks = [keys[i:i + a.chunk] for i in range(0, len(keys), a.chunk)]
    todo = [k for k in range(len(chunks)) if not (outdir / f"chunk_{k:05d}.pkl").exists()]
    logger.info(f"S2 {a.tag}: {len(keys)} concepts, {len(chunks)} chunks, todo {len(todo)}, cfg {cfg}")
    t0 = time.time()
    done = 0
    with ProcessPoolExecutor(a.workers, mp_context=mp.get_context("spawn"), initializer=_init,
                             initargs=(cfg,)) as ex:
        futs = [ex.submit(run_chunk, k, chunks[k]) for k in todo]
        for i, fu in enumerate(as_completed(futs)):
            k, rows, extras, dt = fu.result()
            (outdir / f"chunk_{k:05d}.pkl").write_bytes(pickle.dumps({"rows": rows, "extras": extras}, protocol=5))
            done += len(rows)
            el = time.time() - t0
            logger.info(f"chunk {i+1}/{len(futs)} ({done} concepts) {el/60:.1f} min; {dt/len(rows):.3f} s/concept; "
                        f"eta {el/(i+1)*(len(futs)-i-1)/60:.1f} min")
    rows = []
    for p in sorted(outdir.glob("chunk_*.pkl")):
        rows += pickle.loads(p.read_bytes())["rows"]
    df = pd.DataFrame(rows)
    df.to_parquet(DATA / f"s2_scalars_{a.tag}.parquet", index=False)
    logger.info(f"wrote {len(df)} rows -> data/s2_scalars_{a.tag}.parquet; errors {df.get('s2_error', pd.Series()).notna().sum()}")


if __name__ == "__main__":
    main()
