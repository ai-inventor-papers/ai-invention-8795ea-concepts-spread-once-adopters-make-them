#!/usr/bin/env python3
"""Step 4.7 agreement with iteration 1 (P78 concepts that re-enter this frame) and with any sibling iter_2 dataset."""
import json
import sys
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from config import INP, RES  # noqa: E402

fc = pd.read_csv(RES / "frame_concepts.csv")
it1 = pd.read_csv(INP / "outcomes.csv")
it1["key"] = it1.concept.str.lower().str.replace("-", " ")
fc["key"] = fc.name.str.lower().str.replace("-", " ")
m = fc.merge(it1, on="key", suffixes=("", "_it1"))
fields = json.loads((INP / "field_backbone.json").read_text())["fields"]
m["home_name"] = m.home_primary.map(lambda f: fields[int(f) - 11])
out = {"n_p78_in_frame": int(len(m)), "names": m.name.tolist()}
if len(m) >= 3:
    out["spearman_t0"] = float(spearmanr(m.t0, m.t0_it1).statistic)
    out["t0_exact_match_share"] = float((m.t0 == m.t0_it1).mean())
    h = m[m.home.notna()]
    out["home_agreement_share"] = float((h.home_name == h.home_it1).mean()) if len(h) else None
    d = m[m.O2r_m30.notna() & m.O2r_m30_it1.notna()] if "O2r_m30_it1" in m else m.iloc[0:0]
    out["spearman_O2r_dev_only"] = float(spearmanr(d.O2r_m30, d.O2r_m30_it1).statistic) if len(d) >= 3 else None
    out["n_O2r_pairs"] = int(len(d))
sib = sorted(Path(RES.parent.parent).glob("*dataset*/**/frame_concepts.csv"))
out["sibling_dataset_frame"] = [str(p.relative_to(RES.parent.parent)) for p in sib] or "none found at run time"
(RES / "agreement.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
