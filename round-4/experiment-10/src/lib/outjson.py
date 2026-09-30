"""exp_gen_sol_out builder: one example per cohort concept (kept under unit test so the final write cannot fail)."""
from __future__ import annotations

import json
import math


def _s(v) -> str:
    if v is None:
        return "NA"
    if isinstance(v, float):
        return "NA" if not math.isfinite(v) else f"{v:.6g}"
    return str(v)


def _m(v):
    if isinstance(v, float) and not math.isfinite(v):
        return None
    if hasattr(v, "item"):
        v = v.item()
        if isinstance(v, float) and not math.isfinite(v):
            return None
    return v


def make_method_out(rows: list[dict], metadata: dict, dataset: str = "fresh_cohort_2015_2017_open") -> dict:
    """rows: dicts with keys label, openalex_id, t0, group, O2r_m50, pred_b5, pred_b5_open, and any meta_* keys."""
    ex = []
    for r in rows:
        e = {"input": json.dumps({"concept": r["label"], "openalex_id": f"C{int(r['openalex_id'])}", "t0": int(r["t0"]),
                                  "home_group": r["group"]}, ensure_ascii=False),
             "output": _s(r.get("O2r_m50")),
             "predict_B5": _s(r.get("pred_b5")),
             "predict_B5_plus_OPEN_home": _s(r.get("pred_b5_open"))}
        for k, v in r.items():
            if k.startswith("meta_"):
                e["metadata_" + k[5:]] = _m(v)
        ex.append(e)
    return {"metadata": metadata, "datasets": [{"dataset": dataset, "examples": ex}]}
