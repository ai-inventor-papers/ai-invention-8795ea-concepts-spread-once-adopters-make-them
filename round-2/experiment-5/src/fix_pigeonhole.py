#!/usr/bin/env python3
"""Post-hoc recomputation of the held-out crossed concept x field bootstrap (a robustness diagnostic that is not
part of the verdict). The first held-out run's version indexed concept weights on dev concepts only, so every
held-out weight was 0 and the CI was NaN. Frozen spec unchanged; result written into results/h1_heldout.json."""
import json

import numpy as np
import pandas as pd

import models
import seal
from common import RES, ROOT, SEED, add_deviation, jdump

seal.assert_unsealed()
spec = json.loads((ROOT / "frozen_spec.json").read_text())
sc = spec["standardisation"]
F = pd.read_csv(ROOT / "episode_features.csv")
ep = pd.read_csv(ROOT / "episodes.csv")
F = F.drop(columns=[c for c in ("R",) if c in F]).merge(ep[["ci", "field", "R"]], on=["ci", "field"])
F = models.add_pj(F[F.R.notna()])
dev = F[F.split == "DEV"].reset_index(drop=True)
ho = F[F.split.str.startswith("HELDOUT")].reset_index(drop=True)
ph = models.pigeonhole_heldout(dev, ho, sc, models.B_SMALL, SEED + 17)
r = json.loads((RES / "h1_heldout.json").read_text())
r["pigeonhole_crossed_bootstrap"] = {"B": models.B_SMALL, "ci95": models.ci95(ph), "sd": float(np.nanstd(ph)),
                                     "n_valid": int(np.isfinite(ph).sum()), "recomputed_by": "fix_pigeonhole.py"}
jdump(r, RES / "h1_heldout.json")
add_deviation("pigeonhole_heldout_fix", "The held-out crossed concept x field bootstrap (robustness diagnostic, not a "
              "verdict criterion) was mis-indexed in the first run (all weights 0 -> NaN CI); recomputed post hoc by "
              "fix_pigeonhole.py with fields shared between dev refit and held-out evaluation.")
print(r["pigeonhole_crossed_bootstrap"])
