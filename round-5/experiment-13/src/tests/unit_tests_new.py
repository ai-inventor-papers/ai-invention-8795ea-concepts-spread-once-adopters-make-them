#!/usr/bin/env python3
"""S1 unit tests for the NEW Frame-N code: T5 (Cheng consistency), T6 (degree-preserving rewiring null),
T3 (seal: refuse unseal before the freeze, on a changed spec, on a second call; MaskedCounts raises beyond t_det+2)."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd


def t5() -> dict:
    from s6_features import cheng_cos
    a = np.array([3., 1., 0., 2.])
    r = {"identical": cheng_cos(a, a.copy()), "disjoint": cheng_cos(np.array([1., 0.]), np.array([0., 4.])),
         "empty_prev": cheng_cos(np.zeros(4), a), "scale_inv": abs(cheng_cos(a, 3 * a[::-1]) - cheng_cos(a, a[::-1])),
         "new_neighbours_ignored": cheng_cos(np.array([1., 1., 0.]), np.array([1., 1., 9.]))}
    r["pass"] = bool(abs(r["identical"] - 1) < 1e-12 and r["disjoint"] == 0 and r["empty_prev"] == 0
                     and r["scale_inv"] < 1e-12 and abs(r["new_neighbours_ignored"] - 1) < 1e-12)
    return r


def t6() -> dict:
    import random

    import igraph as ig
    from scipy.sparse import coo_matrix
    rng = np.random.default_rng(1)
    n = 400
    g = ig.Graph.Erdos_Renyi(n=n, p=0.03)
    S = np.arange(20)
    g.add_edges([(int(i), int(j)) for i in S for j in S if i < j and not g.are_adjacent(int(i), int(j))])
    deg0 = np.array(g.degree())
    el0 = np.asarray(g.get_edgelist())
    A0 = coo_matrix((np.ones(2 * len(el0)), (np.r_[el0[:, 0], el0[:, 1]], np.r_[el0[:, 1], el0[:, 0]])),
                    shape=(n, n)).tocsr()
    obs = A0[S][:, S].sum() / 2
    es, same_deg = [], True
    for r in range(200):
        h = g.copy()
        random.seed(31 + r)
        ig.set_random_number_generator(random)
        h.rewire(n=10 * h.ecount(), mode="simple")
        same_deg &= bool(np.array_equal(np.array(h.degree()), deg0))
        el = np.asarray(h.get_edgelist())
        A = coo_matrix((np.ones(2 * len(el)), (np.r_[el[:, 0], el[:, 1]], np.r_[el[:, 1], el[:, 0]])),
                       shape=(n, n)).tocsr()
        es.append(A[S][:, S].sum() / 2)
    es = np.asarray(es)
    z = (obs - es.mean()) / es.std()
    return {"degree_sequence_preserved": same_deg, "planted_clique_z": float(z), "pass": bool(same_deg and z > 3)}


def t3() -> dict:
    import sealn
    from s5_onset import MaskedCounts, MaskError
    tmp = ROOT / "tests" / "tmp_seal"
    shutil.rmtree(tmp, ignore_errors=True)
    (tmp / "parts").mkdir(parents=True)
    orig = {k: getattr(sealn, k) for k in ("SPEC", "SEAL", "MARK", "SEALED_PARTS", "SEALED_LOG")}
    try:
        sealn.SPEC, sealn.SEAL, sealn.MARK = tmp / "spec.json", tmp / "seal.log", tmp / "unsealed.json"
        sealn.SEALED_PARTS, sealn.SEALED_LOG = tmp / "parts", tmp / "sealed_files.log"
        pd.DataFrame({"ci": [1], "year": [2020], "vfield": [3], "n": [5]}).to_parquet(tmp / "parts/sealedA_0000.parquet")
        sealn.log_sealed_parts()
        out = {}
        try:
            sealn.unseal(sealn.SPEC, sealn.MARK)
            out["refuse_before_freeze"] = False
        except sealn.SealError:
            out["refuse_before_freeze"] = True
        sealn.freeze({"x": 1})
        sp = json.loads(sealn.SPEC.read_text())
        sealn.SPEC.write_text(json.dumps({"x": 2}))
        try:
            sealn.unseal(sealn.SPEC, sealn.MARK)
            out["refuse_changed_spec"] = False
        except sealn.SealError:
            out["refuse_changed_spec"] = True
        sealn.freeze(sp)
        df = sealn.unseal(sealn.SPEC, sealn.MARK)
        out["first_unseal_rows"] = int(len(df))
        try:
            sealn.unseal(sealn.SPEC, sealn.MARK)
            out["refuse_second_unseal"] = False
        except sealn.SealError:
            out["refuse_second_unseal"] = True
        out["chain_ok"] = sealn.verify_chain()
    finally:
        for k, v in orig.items():
            setattr(sealn, k, v)
        shutil.rmtree(tmp, ignore_errors=True)
    mc = MaskedCounts({7: np.arange(30.0)}, {7: 2012})
    mc(7, 2012)
    try:
        mc(7, 2013)
        out["mask_raises"] = False
    except MaskError:
        out["mask_raises"] = True
    out["pass"] = all(v for k, v in out.items() if k != "first_unseal_rows") and out["first_unseal_rows"] == 1
    return out


def main() -> None:
    p = ROOT / "results/unit_tests.json"
    res = json.loads(p.read_text()) if p.exists() else {}
    for k, f in (("T5", t5), ("T6", t6), ("T3", t3)):
        res[k] = f()
        print(k, res[k])
    p.write_text(json.dumps(res, indent=1, default=float))


if __name__ == "__main__":
    main()
