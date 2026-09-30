#!/usr/bin/env python3
"""iter-5 STEP 4 (Part C.4): H-P1 exactly as preregistered, by running the sealed partners.main scoring on the CACHED
Exp11 partner indicators (data/partner_indicators.parquet, ALL-papers static partner set) and bridging papers.
partners.build_indicators already ran in Exp11 (logs/partners.log shows only the build line); it is replaced here by
a loader of its cached outputs, after checking ner_all == EXP8 new_edge_rate (max abs < 1e-12). If the check fails the
indicators are rebuilt with the sealed build_indicators. Then H-P1 is evaluated:
  H-P1 holds iff DL diff(ner_METHOD - ner_DOMAIN) > 0 AND DL diff(ner_comm_new - ner_comm_old) > 0, both CI > 0,
  on O2r_m50 (O2r_resid twin reported). Writes results/partner_decomposition.json and results/H_P1.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from common import DATA_IN, RES, jdump, setup_logger


def main() -> None:
    logger = setup_logger("run_partners")
    import partners as PT
    cached = pd.read_parquet(DATA_IN / "partner_indicators.parquet")
    chk = float(np.nanmax(np.abs(cached.ner_all - cached.new_edge_rate)))
    logger.info(f"cached partner indicators {cached.shape}; ner_all vs EXP8 new_edge_rate max abs {chk:.2e}")
    if chk < 1e-12:
        icols = ["ci"] + [c for c in cached.columns if c.startswith(("ner_", "ncw3_")) or c == "bridging_share"]
        ind = cached[icols].copy()
        bp = pd.read_parquet(DATA_IN / "bridging_papers.parquet")
        PT.build_indicators = lambda lg: (ind, bp)
        source = "cached Exp11 partner_indicators.parquet + bridging_papers.parquet"
    else:
        source = "rebuilt with sealed partners.build_indicators"
    PT.main()
    r = json.loads((RES / "partner_decomposition.json").read_text())
    out = {"indicator_source": source, "check_ner_all_vs_EXP8_max_abs": chk}
    for o in ("O2r_m50", "O2r_resid"):
        P = r["pooled_heldout_DL"][o]
        a = P.get("diff_ner_METHOD_minus_ner_DOMAIN", {})
        b = P.get("diff_ner_comm_new_minus_ner_comm_old", {})
        out[o] = {"DL_METHOD_minus_DOMAIN": a, "DL_comm_new_minus_comm_old": b,
                  "DL_carrier_home_minus_offhome": P.get("diff_ner_carrier_home_minus_ner_carrier_offhome"),
                  "holds": bool(a.get("b", -1) > 0 and a.get("ci", [-1])[0] > 0 and b.get("b", -1) > 0
                                and b.get("ci", [-1])[0] > 0)}
        for u in ("DEV", "OLD_HELDOUT", "COHORT"):
            res = r["units"][u][o]["res"]
            out[o][f"{u}_diffs"] = {k: v for k, v in res.items() if k.startswith("diff_")}
    out["H_P1_holds_O2r_m50"] = out["O2r_m50"]["holds"]
    jdump(out, RES / "H_P1.json")
    logger.info(f"H-P1 holds (O2r_m50): {out['H_P1_holds_O2r_m50']}")


if __name__ == "__main__":
    main()
