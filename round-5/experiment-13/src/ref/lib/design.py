"""Frozen design matrices for the learned models: DEV-median imputation + missing flags (indicators with > 5%
missing on DEV) + standardisation with DEV constants. The same spec is applied unchanged to held-out units."""
from __future__ import annotations

import numpy as np
import pandas as pd


def fit_design(df: pd.DataFrame, cols: list[str], flag_min: float = 0.05) -> dict:
    spec = {"cols": list(cols), "median": {}, "flag": [], "mean": {}, "sd": {}}
    for c in cols:
        v = df[c].astype(float)
        spec["median"][c] = float(np.nanmedian(v)) if v.notna().any() else 0.0
        if v.isna().mean() > flag_min:
            spec["flag"].append(c)
    X = apply_design(df, spec, standardise=False)
    for j, c in enumerate(design_names(spec)):
        spec["mean"][c] = float(X[:, j].mean())
        sd = float(X[:, j].std())
        spec["sd"][c] = sd if sd > 1e-12 else 1.0
    return spec


def design_names(spec: dict) -> list[str]:
    return spec["cols"] + [f"{c}__missing" for c in spec["flag"]]


def apply_design(df: pd.DataFrame, spec: dict, standardise: bool = True) -> np.ndarray:
    parts = []
    for c in spec["cols"]:
        v = df[c].astype(float).to_numpy() if c in df.columns else np.full(len(df), np.nan)
        parts.append(np.where(np.isfinite(v), v, spec["median"][c]))
    for c in spec["flag"]:
        v = df[c].astype(float).to_numpy() if c in df.columns else np.full(len(df), np.nan)
        parts.append((~np.isfinite(v)).astype(float))
    X = np.column_stack(parts) if parts else np.zeros((len(df), 0))
    if standardise:
        names = design_names(spec)
        mu = np.array([spec["mean"][n] for n in names])
        sd = np.array([spec["sd"][n] for n in names])
        X = (X - mu) / sd
    return X
