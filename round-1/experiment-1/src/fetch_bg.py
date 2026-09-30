#!/usr/bin/env python3
"""Stage B (zero credits): negative-control background references for sampled lineage children.
Children are sampled per concept (seeded, min(100, n) home + min(100, n) off-home). Each child's reference list
comes from a FREE OpenAlex singleton GET (/works/W<MAG> or /works/doi:..; cost 0 verified from headers), 10
non-concept references per child are sampled with a child-seeded RNG, and their fields come from S2 (/paper/batch
with MAG ids). Saves results/concepts/<slug>/bg.json.gz."""
from __future__ import annotations

import gzip
import json
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from loguru import logger

import s2
from lineage import SEED, load_concept, load_raw, stable_seed
from oa import Client, FreeCallCharged, OAError
from panel import slug

ROOT = Path(__file__).resolve().parent
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "fetch_bg.log", rotation="30 MB", level="DEBUG")
N_CHILD, N_REF = 100, 10


def sample_children(c) -> list[int]:
    cH = c.cH
    home = [k for k in range(len(c.child_idx)) if cH[k] >= 0.5]
    off = [k for k in range(len(c.child_idx)) if cH[k] < 0.5]
    rng = random.Random(SEED)
    return sorted(rng.sample(home, min(N_CHILD, len(home))) + rng.sample(off, min(N_CHILD, len(off))))


def oa_refs(cl: Client, mag: str | None, doi: str | None) -> list[str] | None:
    key = f"W{mag}" if mag else (f"doi:{doi}" if doi else None)
    if key is None:
        return None
    try:
        d = cl.get(f"/works/{key}", {"select": "id,referenced_works"}, projected=0, free=True, summary="singleton")
    except OAError as e:  # F8: skip this child after repeated failures, never abort the concept
        logger.warning(f"singleton {key} skipped: {str(e)[:120]}")
        return None
    return d.get("referenced_works") or []


@logger.catch(reraise=True)
def fetch_one(cl: Client, sl: str) -> dict:
    out_p = ROOT / "results" / "concepts" / sl / "bg.json.gz"
    if out_p.exists():
        return json.loads(gzip.decompress(out_p.read_bytes()))
    c = load_concept(load_raw(sl))
    ks = sample_children(c)
    concept_w = {f"https://openalex.org/W{m}" for m in c.mag if m}
    pids = [c.ids[c.child_idx[k]] for k in ks]

    def one(k: int) -> tuple[int, list[str] | None]:
        i = c.child_idx[k]
        return k, oa_refs(cl, c.mag[i], c.doi[i])

    refs: dict[str, list[str]] = {}
    with ThreadPoolExecutor(8) as ex:
        for k, rw in ex.map(one, ks):
            if rw is None:
                continue
            other = sorted(r for r in rw if r not in concept_w)
            pid = c.ids[c.child_idx[k]]
            refs[pid] = random.Random(stable_seed(pid)).sample(other, min(N_REF, len(other)))
    uniq = sorted({r for v in refs.values() for r in v})
    res = s2.batch([f"MAG:{r.rsplit('/W', 1)[-1]}" for r in uniq], "s2FieldsOfStudy", size=500)
    fos = {r: (x or {}).get("s2FieldsOfStudy") for r, x in zip(uniq, res) if x}
    d = {"children": pids, "refs": refs, "fos": fos}
    out_p.write_bytes(gzip.compress(json.dumps(d).encode()))
    return d


def main() -> None:
    cl = Client(concurrency=8)
    done: set[str] = set()
    idle = 0
    while True:
        todo = sorted(p.parent.name for p in (ROOT / "results" / "concepts").glob("*/s2_raw.json.gz")
                      if not (p.parent / "bg.json.gz").exists())
        if not todo:
            if (ROOT / "logs" / "fetch_s2.done").exists() or idle > 90:
                break
            idle += 1
            time.sleep(20)
            continue
        idle = 0
        for sl in todo:
            t = time.time()
            try:
                d = fetch_one(cl, sl)
            except FreeCallCharged as e:
                logger.error(f"STOP: {e}")
                return
            nref = sum(len(v) for v in d["refs"].values())
            logger.info(f"bg {sl}: children={len(d['children'])} with_refs={len(d['refs'])} refs={nref} "
                        f"labelled={sum(1 for v in d['fos'].values() if v)} {time.time()-t:.0f}s "
                        f"oa_calls={cl.calls} oa_credits={cl.own_total}")
            done.add(sl)


if __name__ == "__main__":
    main()
