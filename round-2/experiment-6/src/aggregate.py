#!/usr/bin/env python3
"""Aggregate pass-1 per-file hit records into dense count arrays [concept, year, field-slot] (slot 0 = no venue field,
slot 1..26 = fields 11..36) and base totals. Output: scan/agg_counts.npz.
Arrays: T_all (all title hits), T_tag (title & tag>=0.3), T_tag_exact (same, exact form only), T_untag (title, work tagged
but not with c), T_none (title, work has no tags at all), TO (tag-only: tagged >=0.3, no title hit), TPF_tag (T_tag by
primary-topic field instead of venue field); G[y], GF[y, f]."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from config import NY, P1, RES, SCAN, Y0  # noqa: E402

logger.remove(); logger.add(sys.stdout, format="{time:HH:mm:ss}|{level:<7}|{message}")


NAMES = ["T_all", "T_tag", "T_tag_exact", "T_untag", "T_none", "TO", "TPF_tag"]
S = 27


def _add(acc: np.ndarray, keys: np.ndarray, w: np.ndarray | None = None) -> None:
    if not len(keys):
        return
    u, inv = np.unique(keys, return_inverse=True)
    c = np.bincount(inv, weights=w).astype(np.int64) if w is not None else np.bincount(inv)
    acc[u] += c.astype(acc.dtype)


def chunk(args: tuple[list[str], int]) -> dict:
    files, NC = args
    size = NC * NY * S
    acc = {k: np.zeros(size, np.int32) for k in NAMES}
    G = np.zeros(NY, np.int64); GF = np.zeros((NY, 26), np.int64); nrows = 0; nbase = 0
    for f in files:
        z = np.load(f)
        yr = z["year"].astype(np.int64) - Y0
        ok = (yr >= 0) & (yr < NY)
        c = z["cidx"].astype(np.int64)
        slot = z["vf"].astype(np.int64); slot = np.where(slot >= 11, slot - 10, 0)
        pslot = z["pf"].astype(np.int64); pslot = np.where(pslot >= 11, pslot - 10, 0)
        key = (c * NY + yr) * S + slot
        tag = z["tag"]; var = z["variant"]
        for nm, m in (("T_all", ok), ("T_tag", ok & (tag == 1)), ("T_tag_exact", ok & (tag == 1) & (var == 0)),
                      ("T_untag", ok & (tag == 0)), ("T_none", ok & (tag == -1))):
            _add(acc[nm], key[m])
        m = ok & (tag == 1)
        _add(acc["TPF_tag"], ((c * NY + yr) * S + pslot)[m])
        tk = z["to_key"]; tc = z["to_cnt"]
        tcon = tk // 10000; tyr = (tk // 100) % 100; tvf = tk % 100 - 1
        okt = (tyr >= 0) & (tyr < NY)
        tsl = np.where(tvf >= 11, tvf - 10, 0)
        _add(acc["TO"], ((tcon * NY + tyr) * S + tsl)[okt], tc[okt].astype(float))
        G += z["G"]; GF += z["GF"]; nrows += int(z["n"]); nbase += int(z["base_all"].sum())
    np.savez(SCAN / f"agg_part_{abs(hash(files[0])) % 10**8}.npz", G=G, GF=GF, nrows=nrows, nbase=nbase, **acc)
    return {"n": len(files)}


@logger.catch(reraise=True)
def main() -> None:
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor
    NC = len(pd.read_parquet(RES / "lexicon.parquet", columns=["concept_idx"]))
    files = sorted(str(f) for f in P1.glob("f*.npz") if ".tmp" not in f.name)
    for old in SCAN.glob("agg_part_*.npz"):
        old.unlink()
    parts = [files[i::4] for i in range(4)]
    t0 = time.time()
    with ProcessPoolExecutor(4, mp_context=mp.get_context("spawn")) as ex:
        list(ex.map(chunk, [(p, NC) for p in parts]))
    logger.info(f"chunks done in {time.time()-t0:.0f}s")
    out = None
    for pp in sorted(SCAN.glob("agg_part_*.npz")):
        z = np.load(pp)
        if out is None:
            out = {k: z[k].astype(np.int32) for k in NAMES}; G = z["G"].copy(); GF = z["GF"].copy()
            nrows = int(z["nrows"]); nbase = int(z["nbase"])
        else:
            for k in NAMES:
                out[k] += z[k]
            G += z["G"]; GF += z["GF"]; nrows += int(z["nrows"]); nbase += int(z["nbase"])
        pp.unlink()
    out = {k: v.reshape(NC, NY, S) for k, v in out.items()}
    np.savez_compressed(SCAN / "agg_counts.npz", G=G, GF=GF, n_rows=np.array(nrows), n_base=np.array(nbase),
                        n_files=np.array(len(files)), **out)
    logger.info(f"aggregated {len(files)} files, rows={nrows:,} base={nbase:,}; T_all={out['T_all'].sum():,} "
                f"T_tag={out['T_tag'].sum():,} T_none={out['T_none'].sum():,} TO={out['TO'].sum():,} ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
