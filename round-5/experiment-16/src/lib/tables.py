"""Analysis tables: clean_variants joined with the EXP10 covariate frames and the (previously unsealed) outcomes.
Selection data, outcomes previously unsealed by EXP5/EXP8/EXP10."""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import DATA, DATA_IN
from ladder import rung_design

COV = ["logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH", "type", "generic", "level",
       "fp_logN", "fp_nfields", "fp_reemerge", "fp_wiki_pre", "newborn", "t0", "agroup", "label_coverage_early",
       "home_coverage_early", "n_all_early", "O2r_m50", "O2r_resid"]
BODIES = ["DEV", "OLDHO", "COH1014", "COH1517"]


def load_tables() -> dict[str, pd.DataFrame]:
    cv = pd.read_parquet(DATA / "clean_variants.parquet")
    cv = cv.drop(columns=[c for c in ("t0",) if c in cv.columns])
    fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet", columns=["ci"] + COV)
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=["ci"] + COV + ["window_flag"])
    cv = cv.drop(columns=[c for c in ("agroup",) if c in cv.columns])
    e = cv[cv.frame == "exp5"].merge(fe, on="ci", how="inner", validate="1:1")
    e["window_flag"] = 0
    c = cv[cv.frame == "cohort"].merge(ac, on="ci", how="inner", validate="1:1")
    pooled = pd.concat([e, c], ignore_index=True)
    pooled["window_flag"] = pooled.window_flag.fillna(0).astype(int)
    out = {b: pooled[pooled.body == b].reset_index(drop=True) for b in BODIES}
    out["POOLED"] = pooled
    return out


def design(df: pd.DataFrame, rung: str, pooled: bool, drop_group: bool = False) -> tuple[np.ndarray, np.ndarray]:
    Bc, Cc = rung_design(df, rung, drop_group=drop_group)
    if pooled and df.body.nunique() > 1:
        bs = sorted(df.body.unique())[1:]
        Cc = pd.concat([Cc, pd.DataFrame({f"body_{b}": (df.body == b).astype(float) for b in bs}, index=df.index)],
                       axis=1)
        Cc = Cc.loc[:, Cc.std() > 0]
    return Bc.to_numpy(float), Cc.to_numpy(float)
