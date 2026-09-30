#!/usr/bin/env python3
"""T1 / T3 checks and the iteration-1 replication -> results/checks.json (merged into audit.json by audit.py).

  t1        matcher regression on 3 files: new AC + stemmed verification vs the iteration-1 stemmed matcher,
            both restricted to the P78 phrases (set agreement of (file, row, concept))
  t3        P78 concepts in the frame: Spearman of log yearly counts vs iteration-1 snapshot title matches and
            |dt0| <= 1 agreement with the iteration-1 S0 (API) t0; base-work yearly totals vs iteration-1 totals
  replicate iteration-1 model on the frame's P78 subset (n_early >= 5, R, B5 + log field size +/- gateway)
Usage: python checks.py t1|t3|replicate"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from common import ART3, NY, RES, ROOT, SCAN, Y0, Y1, jdump, phrase_spec, plural_variants, setup_logger, spec_in, \
    surf, title_pos, works_files

logger = setup_logger("checks")
OUT = RES / "checks.json"


def load_out() -> dict:
    return json.loads(OUT.read_text()) if OUT.exists() else {}


def p78() -> list[tuple[str, list[str]]]:
    sys.path.insert(0, str(ART3))
    import importlib
    cfg = importlib.import_module("config")
    return [(n, a) for n, a, _ in cfg.PANEL]


def cmd_t1() -> None:
    from matcher import build_automaton, match
    from prescreen import read_sample_file
    panel = p78()
    old_specs = [(ci, phrase_spec(ph)) for ci, (n, al) in enumerate(panel) for ph in [n] + al]
    entries = []
    for ci, (n, al) in enumerate(panel):
        for ph in [n] + al:
            f = surf(ph)
            entries.append((f, ci, "name_exact"))
            for v in plural_variants(f.strip()):
                entries.append((" " + v + " ", ci, "name_variant"))
    A, specs = build_automaton(entries)
    files = works_files()
    pick = [files[i] for i in (1407, 1125, 1918)]
    old, new = set(), set()
    for fi, key, size, _ in pick:
        tb = read_sample_file(key, size)
        for r, (t, st) in enumerate(zip(tb.column("title").to_pylist(), tb.column("stitle").to_pylist())):
            pos = title_pos(t)
            for ci, sp in old_specs:
                if spec_in(pos, sp):
                    old.add((fi, r, ci))
            for ci in match(st, t, A, specs):
                new.add((fi, r, ci))
    inter = old & new
    res = {"files": [p[0] for p in pick], "n_old": len(old), "n_new": len(new), "n_both": len(inter),
           "recall_vs_old": len(inter) / len(old) if old else math.nan,
           "precision_vs_old": len(inter) / len(new) if new else math.nan,
           "exact_set_equality": old == new,
           "only_old_examples": sorted(old - new)[:10], "only_new_examples": sorted(new - old)[:10],
           "note": "new = surface Aho-Corasick (last-token s/es/ies variants) + stemmed verification; old = stemmed "
                   "positional matcher on every title. Differences are stem-only inflections of non-final tokens."}
    o = load_out()
    o["T1_matcher_regression"] = res
    jdump(o, OUT)
    logger.info(f"T1: {res}")


def cmd_t3() -> None:
    from frame import n_concepts
    from panel import build_arrays, onset, yi
    fc = pd.read_csv(ROOT / "frame_concepts.csv")
    lex = pd.read_parquet(ROOT / "lexicon_v1.parquet", columns=["name"])
    panel = p78()
    name2ci = {n.lower(): i for i, n in enumerate(lex["name"])}
    # iteration-1 snapshot matches (base works), per P78 concept and year
    cnt = defaultdict(Counter)
    for fp in sorted((ART3 / "scan/matches").glob("matches_*.jsonl")):
        with fp.open() as f:
            for ln in f:
                m = json.loads(ln)
                if m["b"] and Y0 <= m["y"] <= Y1:
                    for c in m["c"]:
                        cnt[c][m["y"]] += 1
    s0 = pd.read_csv(ART3 / "results/outcomes.csv")
    s0t0 = {str(c).lower(): t for c, t in zip(s0.concept, s0.t0)}
    Am = build_arrays("match", n_concepts())
    Ag = build_arrays("grounded", n_concepts())
    rows = []
    for pi, (n, al) in enumerate(panel):
        ci = name2ci.get(n.lower())
        if ci is None:
            continue
        old = np.array([cnt[pi][y] for y in range(Y0, Y1 + 1)], float)
        newm, newg = Am["N"][ci], Ag["N"][ci]
        ok = (old + newm) > 0
        rho_m = spearmanr(np.log1p(old[ok]), np.log1p(newm[ok])).statistic if ok.sum() > 3 else math.nan
        rho_g = spearmanr(np.log1p(old[ok]), np.log1p(newg[ok])).statistic if ok.sum() > 3 else math.nan
        t0g, _ = onset(newg)
        t0_api = s0t0.get(n.lower(), math.nan)
        rows.append({"p78": n, "ci": int(ci), "in_frame": int(ci in set(fc.ci)), "rho_match": rho_m,
                     "rho_grounded": rho_g, "t0_grounded": t0g, "t0_iter1_api": t0_api,
                     "abs_dt0": abs(t0g - t0_api) if np.isfinite(t0g) and np.isfinite(t0_api) else math.nan,
                     "sum_old": float(old.sum()), "sum_match": float(newm.sum()), "sum_grounded": float(newg.sum())})
    d = pd.DataFrame(rows)
    d.to_csv(RES / "p78_agreement.csv", index=False)
    fr = d[d.in_frame == 1]
    z = np.load(SCAN / "year_field_totals.npz")
    old_ck = np.load(ART3 / "scan/ckpt.npz")
    oldG = dict(zip(range(1995, 1995 + len(old_ck["G"])), old_ck["G"].tolist()))
    ratio = {y: float(z["G"][y - Y0] / oldG[y]) for y in range(Y0, Y1 + 1) if oldG.get(y)}
    res = {"n_p78_in_lexicon": len(d), "n_p78_in_frame": int(len(fr)),
           "median_rho_match_all": float(d.rho_match.median()), "median_rho_grounded_all": float(d.rho_grounded.median()),
           "median_rho_match_frame": float(fr.rho_match.median()) if len(fr) else None,
           "share_abs_dt0_le1_all": float((d.abs_dt0 <= 1).mean()) if d.abs_dt0.notna().any() else None,
           "share_abs_dt0_le1_frame": float((fr.abs_dt0 <= 1).mean()) if len(fr) else None,
           "base_total_ratio_vs_iter1_min_max": [min(ratio.values()), max(ratio.values())],
           "note": "iteration-1 counts are ungrounded stemmed title matches of P78 phrases (+aliases); "
                   "t0_iter1_api is the S0 API onset (title_and_abstract search)"}
    o = load_out()
    o["T3_p78_agreement"] = res
    jdump(o, OUT)
    logger.info(f"T3: {res}")


def cmd_replicate() -> None:
    import models
    F = pd.read_csv(ROOT / "episode_features.csv")
    ep = pd.read_csv(ROOT / "episodes.csv")
    fc = pd.read_csv(ROOT / "frame_concepts.csv")
    F = F.drop(columns=[c for c in ("R",) if c in F]).merge(ep[["ci", "field", "R"]], on=["ci", "field"])
    sub = F[F.ci.isin(set(fc.ci[fc.in_P78 == 1])) & (F.n_early >= 5)].dropna(subset=["R"]).reset_index(drop=True)
    res = {"n_episodes": len(sub), "n_concepts": int(sub.ci.nunique())}
    if len(sub) >= 20 and sub.R.nunique() == 2:
        base = ["logvol", "growth_c", "offhome_share", "entropy", "reach", "log_field_size", "log_n_early", "growth_j"]
        sc = models.std_consts(sub, base + ["gateway_j"])
        y = sub.R.to_numpy(int)
        m0 = models.fit(models.Z(sub, base, sc), y)
        m1 = models.fit(models.Z(sub, base + ["gateway_j"], sc), y)
        a0 = models.auc(y, m0.predict_proba(models.Z(sub, base, sc))[:, 1])
        a1 = models.auc(y, m1.predict_proba(models.Z(sub, base + ["gateway_j"], sc))[:, 1])
        rng = np.random.default_rng(1)
        cs = sub.ci.unique()
        bs = []
        for _ in range(1000):
            pick = rng.choice(cs, len(cs))
            idx = np.concatenate([np.nonzero(sub.ci.to_numpy() == c)[0] for c in pick])
            d, yy = sub.iloc[idx], y[idx]
            if len(np.unique(yy)) < 2:
                continue
            p0 = models.fit(models.Z(d, base, sc), yy).predict_proba(models.Z(d, base, sc))[:, 1]
            p1 = models.fit(models.Z(d, base + ["gateway_j"], sc), yy).predict_proba(models.Z(d, base + ["gateway_j"], sc))[:, 1]
            bs.append(models.auc(yy, p1) - models.auc(yy, p0))
        res.update({"auc_base": a0, "auc_gateway": a1, "dauc_in_sample": a1 - a0, "ci95": models.ci95(bs),
                    "iteration1_value": 0.103, "same_sign_as_iteration1": bool(a1 - a0 > 0),
                    "note": "in-sample concept-clustered bootstrap, as in art_33 (80 rows, 28 concepts)"})
    o = load_out()
    o["iteration1_replication"] = res
    jdump(o, OUT)
    logger.info(f"replication: {res}")


if __name__ == "__main__":
    {"t1": cmd_t1, "t3": cmd_t3, "replicate": cmd_replicate}[sys.argv[1]]()
