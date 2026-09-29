#!/usr/bin/env python3
"""T0-8: the ported ego module (lib/ego.py) run with the ORIGINAL EXP3 windows, EXP3's own title matches, EXP3's
background (scan/ckpt.npz), N_NULL = 1000, the same seeds and NO betweenness cutoff must reproduce EXP3
results/features_ego.csv on the P78 dev concepts (Spearman >= 0.95 per indicator; exact for deterministic ones).
This validates the port BEFORE the RQ1 window change (W1 = t0, W2 = t0+1, W3 = t0+2)."""
from __future__ import annotations

import importlib.util
import json
import multiprocessing as mp
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT.parents[3]
EXP3 = RUN / "round-1/experiment-3/src"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def exp3_modules():
    cfg = _load("config", EXP3 / "config.py")
    c3 = _load("exp3_common", EXP3 / "common.py")
    return cfg, c3


def build_ctx():
    cfg, c3 = exp3_modules()
    import numpy as np
    import pandas as pd
    sys.path.insert(0, str(ROOT / "lib"))
    tids, G, Gt, bg, _pairs, nt, years = c3.load_scan_aggregates()
    tm = pd.read_csv(EXP3 / "results/topic_meta.csv").set_index("topic").loc[tids]
    sl = [np.load(EXP3 / "backbone" / f"slice{s}.npz") for s in range(3)]
    names = tm.name.tolist()
    return dict(nt=nt, years=years, bg=bg, Gt=Gt, comm=[z["comm"] for z in sl], comm_q=[z["comm_q"] for z in sl],
                deg=[z["deg"] for z in sl], knn=[(z["ka"], z["kb"]) for z in sl],
                full_edges=[(z["a"], z["b"]) for z in sl], subfield=tm.subfield.to_numpy(), names=names,
                ldf=c3.topic_lemma_df(names), tlem=[c3.lemmas(n) for n in names], lemmas=c3.lemmas)


def _init():
    sys.path.insert(0, str(ROOT / "lib"))
    import ego
    ego.set_context(build_ctx())


def job(a):
    import ego
    ci, name, aliases, t0, works, seed = a
    r = ego.concept_core(name, aliases, t0, works, 1000, seed, windows=ego.exp3_windows, btw_cutoff=None)
    r.pop("_top_nb_W3", None)
    return name, r


def main():
    import numpy as np
    import pandas as pd
    from scipy.stats import spearmanr
    cfg, c3 = exp3_modules()
    out = pd.read_csv(EXP3 / "results/outcomes.csv")
    dev = out[out.dropped_reason.isna() | (out.dropped_reason == "")]
    matches = c3.load_matches()
    name2ci = {p[0]: i for i, p in enumerate(cfg.PANEL)}
    jobs = []
    for _, row in dev.iterrows():
        ci = name2ci[row.concept]
        d = matches[(matches.ci == ci) & (matches.year >= row.t0 - 3) & (matches.year <= row.t0 + 4)]
        jobs.append((ci, cfg.PANEL[ci][0], list(cfg.PANEL[ci][1]), int(row.t0),
                     list(zip(d.year.astype(int).tolist(), d.topics.tolist())), cfg.SEED + ci))
    with ProcessPoolExecutor(5, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        res = dict(ex.map(job, jobs))
    new = pd.DataFrame([{"concept": k, **v} for k, v in res.items()]).set_index("concept")
    old = pd.read_csv(EXP3 / "results/features_ego.csv").set_index("concept").loc[new.index]
    cmp = {}
    pairs = [("D_z", "D_z"), ("D_ratio", "D_ratio"), ("D_rare", "D_rare"), ("D_sub", "D_sub"), ("F_res", "F_res"),
             ("NOV_res", "NOV_res"), ("participation", "participation"), ("deg_growth", "deg_growth"),
             ("edge_persistence", "edge_persistence"), ("ego_density_change", "ego_density_change"),
             ("btw_end", "btw_t4"), ("kcore_end", "kcore_t4"), ("constraint_end", "constraint_t4")]
    for a, b in pairs:
        x, y = new[a].to_numpy(float), old[b].to_numpy(float)
        ok = np.isfinite(x) & np.isfinite(y)
        cmp[a] = {"n": int(ok.sum()), "spearman": float(spearmanr(x[ok], y[ok])[0]) if ok.sum() > 3 else None,
                  "max_abs_diff": float(np.max(np.abs(x[ok] - y[ok]))) if ok.any() else None,
                  "nan_pattern_equal": bool(np.array_equal(np.isfinite(x), np.isfinite(y)))}
    allok = all((v["spearman"] or 0) >= 0.95 for v in cmp.values())
    rep = {"n_concepts": len(new), "pass": allok, "indicators": cmp}
    (ROOT / "results/t0_8_ego_port.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
