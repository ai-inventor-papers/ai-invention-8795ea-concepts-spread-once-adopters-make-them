"""Loading the Exp8 analysis table and building the frozen OPEN composites (constants from boundary_spec.json)."""
from __future__ import annotations

import itertools
import json
import math

import numpy as np
import pandas as pd

from common import COMP_SIGN, COMPONENTS, E8, RES

EXTRA = ["label_coverage_early", "CONTACT_REACH", "early_volume", "intersect40", "home", "name", "group", "split"]


def load_table(cols: list[str] | None = None) -> pd.DataFrame:
    return pd.read_parquet(E8 / "data/analysis_table.parquet", columns=cols)


def zmat(A: pd.DataFrame, spec: dict) -> np.ndarray:
    c = spec["open_definition"]["dev_constants"]
    return np.column_stack([COMP_SIGN[k] * (A[k].to_numpy(float) - c["mu"][k]) / c["sd"][k] for k in COMPONENTS])


def composite(Z: np.ndarray, sub: tuple[int, ...], weights: str, spec: dict) -> np.ndarray:
    X = Z[:, list(sub)]
    s = len(sub)
    need = math.ceil(2 * s / 3)
    avail = np.isfinite(X).sum(1)
    if weights == "equal":
        out = np.nanmean(np.where(np.isfinite(X), X, np.nan), axis=1) if s > 1 else X[:, 0].copy()
        out[avail < need] = np.nan
        return out
    key = "|".join(COMPONENTS[i] for i in sub)
    w = np.asarray(spec["open_definition"]["dev_constants"]["pc1"][key]["loadings"])
    out = X @ w                       # complete cases only for PC1 scores
    return out


def all_composites(spec: dict) -> list[dict]:
    out = []
    for s in range(1, 7):
        for sub in itertools.combinations(range(6), s):
            out.append({"sub": sub, "weights": "equal", "size": s,
                        "name": "EQ[" + "+".join(COMPONENTS[i] for i in sub) + "]"})
            if s >= 2:
                out.append({"sub": sub, "weights": "pc1", "size": s,
                            "name": "PC1[" + "+".join(COMPONENTS[i] for i in sub) + "]"})
    assert len(out) == 120
    return out


def add_open(A: pd.DataFrame, spec: dict) -> pd.DataFrame:
    Z = zmat(A, spec)
    A = A.copy()
    A["OPEN"] = composite(Z, tuple(range(6)), "equal", spec)
    # the plan's frozen rule for the full composite: >= 4 of 6 present (ceil(2*6/3) = 4, identical)
    A["OPEN_PC1"] = composite(Z, tuple(range(6)), "pc1", spec)
    A["OPEN_n_components"] = np.isfinite(Z).sum(1)
    return A
