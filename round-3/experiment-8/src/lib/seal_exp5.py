#!/usr/bin/env python3
"""STEP 9 gate: unseal held-out and cohort outcomes EXACTLY ONCE, after the dev specification is frozen.

`python seal.py unseal` raises unless frozen_spec.json exists and its sha256 equals the last FREEZE line in
logs/seal.log, and raises on a second call (an UNSEAL line already exists). It then computes the held-out and
cohort outcome columns (episodes.csv, concept_outcomes.csv) and the sensitivity episode tables
(sens_episodes_{ptopic,match,b5_t0p4}.csv), and appends an UNSEAL line to logs/seal.log."""
from __future__ import annotations

import hashlib
import sys
import time

import numpy as np
import pandas as pd

from common import LOGS, ROOT, setup_logger

SEAL_LOG = LOGS / "seal.log"
SPEC = ROOT / "frozen_spec.json"


class SealError(RuntimeError):
    pass


def spec_sha(path=SPEC) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _lines(log=SEAL_LOG) -> list[str]:
    return log.read_text().splitlines() if log.exists() else []


def assert_frozen(spec=SPEC, log=SEAL_LOG) -> str:
    if not spec.exists():
        raise SealError("frozen_spec.json missing: freeze the dev specification first")
    fr = [ln for ln in _lines(log) if " FREEZE " in ln]
    if not fr:
        raise SealError("no FREEZE entry in seal.log")
    logged = fr[-1].split("sha256(frozen_spec.json)=")[-1].strip()
    h = spec_sha(spec)
    if logged != h:
        raise SealError(f"frozen_spec.json hash mismatch: logged {logged[:12]} != current {h[:12]}")
    return h


def assert_unsealed(spec=SPEC, log=SEAL_LOG) -> None:
    h = assert_frozen(spec, log)
    un = [ln for ln in _lines(log) if " UNSEAL " in ln]
    if not un or h not in un[-1]:
        raise SealError("held-out outcomes have not been unsealed under the current frozen spec")


def begin_unseal(spec=SPEC, log=SEAL_LOG) -> str:
    h = assert_frozen(spec, log)
    if any(" UNSEAL " in ln for ln in _lines(log)):
        raise SealError("unseal already performed once; a second unseal is not allowed")
    return h


def mark_unsealed(h: str, log=SEAL_LOG) -> None:
    with log.open("a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} UNSEAL spec={h}\n")


def alt_table(fc: pd.DataFrame, A: dict, arr: str, b5_end: int = 2) -> pd.DataFrame:
    """Sensitivity episode table (all splits) with outcomes, features and coverage covariates."""
    from features import build_features
    from frame import episode_outcomes, episode_rows, home_rule
    X = A[arr]
    rows = []
    fc2 = fc.copy()
    for i, r in enumerate(fc.itertuples()):
        if arr == "V" and b5_end == 2 and A.get("_same_home"):
            home = [int(h) for h in str(r.home).split(";") if h]
        else:
            h = home_rule(X[r.ci], r.t0)
            home = h["home"] or [int(x) for x in str(r.home).split(";") if x]
        fc2.iat[i, fc2.columns.get_loc("home")] = ";".join(map(str, home))
        for e in episode_rows(r.ci, X[r.ci], r.t0, home):
            e.update(episode_outcomes(X[r.ci], r.t0, e["field"], e["share_early"]))
            rows.append(e)
    ep = pd.DataFrame(rows).merge(fc2[["ci", "concept_id", "name", "t0", "group", "split", "home"]], on="ci")
    B = dict(A)
    B["V"] = X
    F = build_features(fc2, ep, B, "V", b5_end=b5_end)
    return F.merge(fc[["ci", "label_coverage_early", "precision_c", "tag_coverage", "newborn", "intersect40",
                       "weak_home"]], on="ci", how="left")


def unseal() -> None:
    logger = setup_logger("seal")
    h = begin_unseal()
    from frame import concept_outcomes, episode_outcomes, n_concepts, year_totals
    from panel import build_arrays
    fc = pd.read_csv(ROOT / "frame_concepts.csv")
    ep = pd.read_csv(ROOT / "episodes.csv")
    co = pd.read_csv(ROOT / "concept_outcomes.csv")
    A = build_arrays("grounded", n_concepts())
    N, V = A["N"], A["V"]
    G, _ = year_totals()
    t0m = fc.set_index("ci").t0
    m = ep.split != "DEV"
    outs = [episode_outcomes(V[r.ci], int(t0m[r.ci]), r.field, r.share_early) for r in ep[m].itertuples()]
    O = pd.DataFrame(outs, index=ep.index[m])
    for c in O.columns:
        ep.loc[m, c] = O[c]
    mc = co.split != "DEV"
    oc = [concept_outcomes(N[r.ci], V[r.ci], G, int(t0m[r.ci])) for r in co[mc].itertuples()]
    OC = pd.DataFrame(oc, index=co.index[mc])
    for c in OC.columns:
        if c not in co:
            co[c] = np.nan
        co.loc[mc, c] = OC[c]
    ep.to_csv(ROOT / "episodes.csv", index=False)
    co.to_csv(ROOT / "concept_outcomes.csv", index=False)
    mark_unsealed(h)
    logger.info(f"UNSEALED under spec {h[:16]}: {int(m.sum())} episodes, {int(mc.sum())} concepts")
    # sensitivity tables (reported only; never used for the verdict)
    alt_table(fc, A, "P").to_csv(ROOT / "sens_episodes_ptopic.csv", index=False)
    Am = build_arrays("match", n_concepts())
    alt_table(fc, Am, "V").to_csv(ROOT / "sens_episodes_match.csv", index=False)
    A2 = dict(A)
    A2["_same_home"] = True
    alt_table(fc, A2, "V", b5_end=4).to_csv(ROOT / "sens_episodes_b5_t0p4.csv", index=False)
    logger.info("sensitivity episode tables written")


if __name__ == "__main__":
    {"unseal": unseal}[sys.argv[1]]()
