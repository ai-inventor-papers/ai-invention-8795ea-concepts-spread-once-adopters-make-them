"""Guarded access to frame tables. Held-out outcome / entry data can only be loaded once results/freeze_log.txt
exists (T5 sealing guard)."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from config import RES, SCAN


class SealedError(RuntimeError):
    pass


def frozen() -> bool:
    return (RES / "freeze_log.txt").exists()


def load_backbone() -> dict:
    b = json.loads((RES.parent / "inputs" / "field_backbone.json").read_text())
    b["phi"] = np.array(b["phi"]); b["g"] = np.array(b["gateway_eig"])
    b["g_deg"] = np.array(b["gateway_deg"]); b["g_btw"] = np.array(b["gateway_btw"])
    return b


def load_g(split: str) -> dict[int, np.ndarray]:
    """per-concept grounded counts [NY, 27] (slot 0 = no venue field, slot k = field 10+k)."""
    if split != "dev" and not frozen():
        raise SealedError(f"split {split!r} is sealed until frozen_spec.json is logged in freeze_log.txt")
    z = np.load(SCAN / f"frame_g_{'dev' if split == 'dev' else 'heldout'}.npz")
    return {int(c): z["g"][i] for i, c in enumerate(z["cidx"])}


def load_frame(split: str | None = None) -> pd.DataFrame:
    fc = pd.read_csv(RES / "frame_concepts.csv")
    if split is None:
        return fc
    if split != "dev" and not frozen():
        raise SealedError(f"split {split!r} is sealed")
    if split == "heldout":
        return fc[fc.split.isin(["heldout_field", "heldout_cohort"])]
    return fc[fc.split == split]
