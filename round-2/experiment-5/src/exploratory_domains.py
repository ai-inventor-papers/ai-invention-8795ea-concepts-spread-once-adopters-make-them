#!/usr/bin/env python3
"""EXPLORATORY (post-unseal, never used for any verdict): where does the adopting field's gateway centrality carry
retention signal? Per home group (4 dev + 4 held-out) and the 2010-14 cohort: univariate AUC of gateway_j for R,
Spearman(gateway_j, R), Spearman(gateway_j, P_j(-c)), and the gateway increment over the iteration-1 base (L1) and
over the full X0, using leave-one-group-out fits across ALL 8 groups (each group predicted by a model fitted on the
other 7), with 300-draw concept bootstraps of the evaluation set. Writes results/exploratory_domain_specificity.json."""
import json

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

import models
from common import DEV_GROUPS, HELD_GROUPS, RES, ROOT, SEED, jdump

spec = json.loads((ROOT / "frozen_spec.json").read_text())
sc = spec["standardisation"]
F = pd.read_csv(ROOT / "episode_features.csv")
ep = pd.read_csv(ROOT / "episodes.csv")
F = F.drop(columns=[c for c in ("R",) if c in F]).merge(ep[["ci", "field", "R"]], on=["ci", "field"])
F = models.add_pj(F[F.R.notna()]).reset_index(drop=True)
main = F[F.split != "COHORT"].reset_index(drop=True)
y = main.R.to_numpy(int)
grp = main.group.to_numpy()
L1 = models.LADDER["L1_iter1_base"]
oof = {k: models.logo_oof(main, cols, sc, y, grp) for k, cols in
       {"L1": L1, "L1g": L1 + [models.GATE], "X0": models.X0, "X1": models.X1}.items()}
rng = np.random.default_rng(SEED)
out = {}
for g in DEV_GROUPS + HELD_GROUPS:
    m = grp == g
    d = main[m]
    yy = y[m]
    cid = d.ci.to_numpy()
    cs = np.unique(cid)
    idx_of = {c: np.nonzero(cid == c)[0] for c in cs}
    bl1, bx = [], []
    for _ in range(300):
        ii = np.concatenate([idx_of[c] for c in rng.choice(cs, len(cs))])
        bl1.append(models.auc(yy[ii], oof["L1g"][m][ii]) - models.auc(yy[ii], oof["L1"][m][ii]))
        bx.append(models.auc(yy[ii], oof["X1"][m][ii]) - models.auc(yy[ii], oof["X0"][m][ii]))
    out[g] = {"split": "DEV" if g in DEV_GROUPS else "HELDOUT", "n": int(m.sum()), "n_concepts": int(len(cs)),
              "R_rate": float(yy.mean()), "gateway_alone_auc": models.auc(yy, d.gateway_j.to_numpy()),
              "spearman_gateway_R": float(spearmanr(d.gateway_j, yy).statistic),
              "spearman_gateway_Pj": float(spearmanr(d.gateway_j, d.P_j).statistic),
              "dauc_over_L1": models.auc(yy, oof["L1g"][m]) - models.auc(yy, oof["L1"][m]), "dauc_over_L1_ci95": models.ci95(bl1),
              "dauc_over_X0": models.auc(yy, oof["X1"][m]) - models.auc(yy, oof["X0"][m]), "dauc_over_X0_ci95": models.ci95(bx),
              "top_adopting_fields": d.field.value_counts().head(5).to_dict()}
coh = F[F.split == "COHORT"]
out["COHORT"] = {"n": int(len(coh)), "gateway_alone_auc": models.auc(coh.R.to_numpy(int), coh.gateway_j.to_numpy()),
                 "spearman_gateway_R": float(spearmanr(coh.gateway_j, coh.R).statistic)}
out["note"] = ("EXPLORATORY, post-unseal, leave-one-group-out over all 8 home groups (this is NOT the frozen primary, "
               "which fits on dev only); reported to locate the domain-specificity of the gateway signal.")
jdump(out, RES / "exploratory_domain_specificity.json")
for g, v in out.items():
    if isinstance(v, dict):
        print(g, {k: (round(x, 4) if isinstance(x, float) else x) for k, x in v.items() if k not in ("top_adopting_fields", "dauc_over_L1_ci95", "dauc_over_X0_ci95")})
