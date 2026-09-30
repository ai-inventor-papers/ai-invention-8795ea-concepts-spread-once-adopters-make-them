#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers (TODO 5 audit). Deliberately does NOT import the pipeline's
modules: it reads raw files (API yearly counts, raw title-match jsonl, source labels, features.csv, reliability
splits) and recomputes through different code (sklearn pipelines, math.comb rarefaction, pandas Spearman).
Also runs placebo (permuted candidate) and positive-control (planted feature) checks.
Writes results/audit.json."""
from __future__ import annotations

import json
import math
import os
from collections import Counter, defaultdict
from pathlib import Path

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.impute import SimpleImputer  # noqa: E402
from sklearn.linear_model import Ridge  # noqa: E402
from sklearn.pipeline import make_pipeline  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

ROOT = Path(__file__).resolve().parent
RES = ROOT / "results"
B5 = ["logvol", "growth", "offhome_share", "entropy", "nfields2"]
rng = np.random.default_rng(777)
audit: dict = {}


def sp(a, b) -> float:
    return float(pd.Series(a).corr(pd.Series(b), method="spearman"))


# ---------------------------------------------------------------- 1. outcomes from raw data
out = pd.read_csv(RES / "outcomes.csv")
dev = out[out.dropped_reason.isna()].copy()
api = json.loads((RES / "yearly_counts_api.json").read_text())
G = {int(k): v for k, v in api["G"].items()}
chk = {"t0": 0, "logvol": 0.0, "growth": 0.0, "O1": 0}
for _, r in dev.iterrows():
    n = {int(k): v for k, v in api["concepts"][r.concept].items()}
    t0 = min(y for y in range(2000, 2015) if n.get(y, 0) >= 20)
    chk["t0"] += int(t0 != r.t0)
    chk["logvol"] = max(chk["logvol"], abs(math.log(sum(n.get(y, 0) for y in range(t0, t0 + 5))) - r.logvol))
    chk["growth"] = max(chk["growth"], abs(math.log((n.get(t0 + 4, 0) + 1) / (n.get(t0 + 1, 0) + 1)) - r.growth))
    o1 = int(sum(n.get(y, 0) / G[y] for y in (t0 + 6, t0 + 7, t0 + 8)) / 3 >= n.get(t0 + 5, 0) / G[t0 + 5])
    chk["O1"] += int(o1 != r.O1)
audit["api_outcomes_mismatches"] = chk

# O2r from the raw title-match jsonl + raw source labels, exact rational rarefaction with math.comb
sf = pd.read_parquet(RES / "source_field.parquet")
lab = dict(zip(sf.source.astype(int), sf.field))
panel_names = {}
import config  # only for the frozen panel names (data, not pipeline code)
for i, (nm, _, _) in enumerate(config.PANEL):
    panel_names[i] = nm
t0_of = dict(zip(dev.concept, dev.t0.astype(int)))
cnt: dict[str, Counter] = defaultdict(Counter)
for fp in sorted((ROOT / "scan" / "matches").glob("matches_*.jsonl")):
    with fp.open() as f:
        for ln in f:
            m = json.loads(ln)
            if not m["b"] or m["s"] is None:
                continue
            for c in m["c"]:
                nm = panel_names[c]
                if nm in t0_of and t0_of[nm] + 6 <= m["y"] <= t0_of[nm] + 8:
                    fl = lab.get(m["s"])
                    if fl is not None and not pd.isna(fl):
                        cnt[nm][int(fl)] += 1


def rarefy_exact(c: Counter, k: int) -> float:
    N = sum(c.values())
    tot = math.comb(N, k)
    return float(sum(1 - math.comb(N - v, k) / tot for v in c.values()))


diffs = [abs(rarefy_exact(cnt[r.concept], 30) - r.O2r) for _, r in dev.iterrows()]
audit["O2r_max_abs_diff_raw_recompute"] = float(max(diffs))
audit["N_WO_mismatches"] = int(sum(sum(cnt[r.concept].values()) != r.N_WO for _, r in dev.iterrows()))

# ---------------------------------------------------------------- 2. LOGO Delta-rho with sklearn
f = pd.read_csv(RES / "features.csv").merge(out[["concept", "O2r", "O1"]], on="concept")
f = f[f.O2r.notna()].reset_index(drop=True)
groups = f.group.to_numpy()


def logo_sk(df: pd.DataFrame, cols: list[str], y: np.ndarray) -> np.ndarray:
    pred = np.empty(len(df))
    g = df.group.to_numpy()
    for grp in np.unique(g):
        te = g == grp
        mdl = make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler(), Ridge(alpha=1.0))
        mdl.fit(df.loc[~te, cols], y[~te])
        pred[te] = mdl.predict(df.loc[te, cols])
    return pred


def delta(df: pd.DataFrame, cand: str, yname: str = "O2r") -> tuple[float, float, dict]:
    y = df[yname].to_numpy(float)
    pb, pc = logo_sk(df, B5, y), logo_sk(df, B5 + [cand], y)
    per = {g: sp(pc[df.group == g], y[df.group == g]) - sp(pb[df.group == g], y[df.group == g])
           for g in sorted(df.group.unique())}
    return sp(pb, y), sp(pc, y) - sp(pb, y), per


sr = json.loads((RES / "screen_result.json").read_text())
lg = {}
for key, cand in (("D", "D_ratio"), ("F", "F_res"), ("D_z_literal", "D_z")):
    base, d, per = delta(f, cand)
    lg[cand] = {"base_rho": base, "delta_rho": d, "per_group": per,
                "pipeline_delta_rho": sr["candidates"][key]["delta_rho"],
                "pipeline_per_group": sr["candidates"][key]["per_group_delta_rho"]}
audit["logo_sklearn"] = lg

# bootstrap CI (independent loop, 500 draws)
boot = {c: [] for c in ("D_ratio", "F_res")}
for b in range(500):
    idx = np.concatenate([rng.choice(np.nonzero(groups == g)[0], (groups == g).sum()) for g in np.unique(groups)])
    bd = f.iloc[idx].reset_index(drop=True)
    for c in boot:
        boot[c].append(delta(bd, c)[1])
audit["bootstrap_500_CI90"] = {c: [float(np.percentile(v, 5)), float(np.percentile(v, 95))] for c, v in boot.items()}

# ---------------------------------------------------------------- 3. split-half SB from the raw splits
rel = pd.read_csv(RES / "reliability_splits.csv")
rel = rel[rel.concept.isin(f.concept)]
sb = {}
for c in ("D_ratio", "F_res", "D_z"):
    rs = [sp(d[f"{c}_A"], d[f"{c}_B"]) for _, d in rel.groupby("split")]
    sb[c] = float(np.median([2 * r / (1 + r) for r in rs]))
audit["split_half_SB_median"] = sb
audit["size_rho"] = {c: {"logvol": sp(f[c], f.logvol), "growth": sp(f[c], f.growth)} for c in ("D_ratio", "F_res", "D_z")}

# ---------------------------------------------------------------- 4. placebo: permuted candidates must not pass
perm = {}
for c in ("D_ratio", "F_res"):
    ds = []
    for _ in range(200):
        g2 = f.copy()
        g2[c] = rng.permutation(g2[c].to_numpy())
        ds.append(delta(g2, c)[1])
    ds = np.array(ds)
    perm[c] = {"mean_delta_rho_permuted": float(ds.mean()), "sd": float(ds.std()),
               "share_permuted_ge_0.10": float((ds >= 0.10).mean()),
               "observed": lg[c]["delta_rho"], "perm_p_value_one_sided": float((ds >= lg[c]["delta_rho"]).mean())}
audit["placebo_permuted_candidate"] = perm

# exploratory partial association: permutation p-value (different code: numpy lstsq residuals on train folds)
def logo_partial(df: pd.DataFrame, c: str) -> float:
    rx, ry = [], []
    for grp in np.unique(df.group):
        te = (df.group == grp).to_numpy()
        tr = ~te & df[c].notna().to_numpy()
        tt = te & df[c].notna().to_numpy()
        Xtr = np.column_stack([np.ones(tr.sum()), StandardScaler().fit(df.loc[tr, B5]).transform(df.loc[tr, B5])])
        sc = StandardScaler().fit(df.loc[tr, B5])
        Xte = np.column_stack([np.ones(tt.sum()), sc.transform(df.loc[tt, B5])])
        for v, store in ((df.O2r.to_numpy(float), ry), (df[c].to_numpy(float), rx)):
            b = np.linalg.lstsq(Xtr, v[tr], rcond=None)[0]
            store.append(v[tt] - Xte @ b)
    return sp(np.concatenate(rx), np.concatenate(ry))


obs = logo_partial(f, "D_ratio")
pp = []
for _ in range(1000):
    g2 = f.copy()
    g2["D_ratio"] = rng.permutation(g2["D_ratio"].to_numpy())
    pp.append(logo_partial(g2, "D_ratio"))
pp = np.array(pp)
ex = json.loads((RES / "exploratory_partial_association.json").read_text())
audit["exploratory_partial_D_ratio"] = {"recomputed": obs,
                                        "pipeline": ex["candidates"]["D_ratio"]["logo_partial_rho"],
                                        "perm_p_value_one_sided": float((pp >= obs).mean()),
                                        "perm_95th_percentile": float(np.percentile(pp, 95))}

# ---------------------------------------------------------------- 5. positive control: planted feature passes
y = f.O2r.to_numpy(float)
resid = y - logo_sk(f, B5, y)
g3 = f.copy()
g3["planted"] = resid + rng.normal(scale=resid.std() * 0.5, size=len(y))
_, dpl, perpl = delta(g3, "planted")
audit["positive_control_planted"] = {"delta_rho": dpl, "per_group": perpl,
                                     "passes_delta_ge_0.10": bool(dpl >= 0.10)}
(RES / "audit.json").write_text(json.dumps(audit, indent=1))
print(json.dumps(audit, indent=1))
