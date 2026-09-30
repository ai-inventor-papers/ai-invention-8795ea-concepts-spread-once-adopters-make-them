"""Frozen constants and paths shared by every module (paths derived from this file's location)."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INP, RES, LOGS, FIGS, SCAN, BENCH = (ROOT / d for d in ("inputs", "results", "logs", "figures", "scan", "benchmark"))
# (EXP7 copy) directory creation removed: this module is imported for constants only
P1 = SCAN / "pass1"
P2 = SCAN / "pass2"

SEED = 20261001
FIELDS = list(range(11, 37))
NF = 26
Y0, Y1 = 1995, 2022
NY = Y1 - Y0 + 1
DEV_HOME = {17: "CS", 22: "Eng", 13: "BGM", 27: "Med"}
HELDOUT_GROUP = {"Physical": [15, 16, 21, 25, 31], "LifeEnv": [11, 19, 23, 24, 28, 30],
                 "Social": [12, 14, 20, 32, 33], "MathDec": [18, 26], "OtherHealth": [29, 34, 35, 36]}
FIELD_GROUP = {f: g for g, fs in HELDOUT_GROUP.items() for f in fs}
FIELD_GROUP.update({f: "DEV_" + s for f, s in DEV_HOME.items()})
M_RAREFY, M_RAREFY_SENS = 30, 50
EPISODE_MIN = 2
RET_MIN = 2
T0_MIN = 20
TAG_SCORE = 0.3
PREC_GATE = 0.8
N_BOOT = int(os.environ.get("AII_NBOOT", 2000))  # env overrides only for debugging runs
N_PERM = int(os.environ.get("AII_NPERM", 1000))
N_REWIRE = int(os.environ.get("AII_NREWIRE", 200))
OPENROUTER_CAP_USD = 0.50
