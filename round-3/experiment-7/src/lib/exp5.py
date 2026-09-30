"""EXP5 / EXP6 inputs (read-only, by path), outcome-blind de-duplication and the grounded count arrays
(own re-implementation of EXP5 panel.build_arrays('grounded'), because that function caches into EXP5's directory)."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

from d3 import NY, Y0

RUN = Path(__file__).resolve().parents[4]
EXP6 = RUN / "round-2/experiment-6/src"
EXP5 = RUN / "round-2/experiment-5/src"
DS2 = RUN / "round-2/dataset-2/src"
FIELD_IDS = list(range(11, 37))
GROUP_OF_FIELD = {17: "CS", 22: "Eng", 13: "BGM", 27: "Med", 29: "Med", 35: "Med", 36: "Med",
                  15: "PHYS", 16: "PHYS", 19: "PHYS", 21: "PHYS", 25: "PHYS", 31: "PHYS",
                  11: "LIFEENV", 23: "LIFEENV", 24: "LIFEENV", 28: "LIFEENV", 30: "LIFEENV", 34: "LIFEENV",
                  12: "SOC", 14: "SOC", 20: "SOC", 32: "SOC", 33: "SOC", 26: "MATHDEC", 18: "MATHDEC"}
DEV_GROUPS = ["CS", "Eng", "BGM", "Med"]
HELD_GROUPS = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]


def norm(s: str) -> str:
    """NFKD -> casefold -> non-alnum to space -> collapse -> strip a trailing 's' on the last token when len > 4."""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).casefold()
    s = re.sub(r"[^0-9a-z]+", " ", s).strip()
    toks = s.split()
    if toks and len(toks[-1]) > 4 and toks[-1].endswith("s"):
        toks[-1] = toks[-1][:-1]
    return " ".join(toks)


def load_backbone() -> dict:
    b = json.loads((EXP6 / "inputs" / "field_backbone.json").read_text())
    phi = np.array(b["phi"], float)
    assert np.allclose(phi, phi.T), "phi not symmetric"
    assert not np.isnan(phi).any()
    if np.abs(np.diag(phi)).max() > 0:
        logger.warning("phi diagonal non-zero -> zeroed")
        np.fill_diagonal(phi, 0)
    return {"phi": phi, "gate": np.array(b["gateway_eig"], float), "raw_keys": list(b.keys())}


def exp6_GF() -> np.ndarray:
    return np.load(EXP6 / "scan" / "agg_counts.npz")["GF"]


def exp5_GF() -> tuple[np.ndarray, dict]:
    z = np.load(EXP5 / "scan" / "year_field_totals.npz")
    assert list(z["years"]) == list(range(Y0, Y0 + NY))
    return z["VF"][:, 1:].astype(np.int64), {k: z[k].shape for k in z.files}


def exp6_frame() -> tuple[pd.DataFrame, dict[int, np.ndarray]]:
    fc = pd.read_csv(EXP6 / "results" / "frame_concepts.csv")
    fc = fc[fc.newborn].copy()
    fc["home_list"] = [[int(h) for h in str(x).split("|")] for x in fc.home]
    fc["hgroup"] = np.where(fc.split == "heldout_cohort", "Cohort", np.where(fc.split == "dev", fc.group, fc.group))
    fc["intersect"] = fc.intersection_born.astype(int)
    fc["weak_home"] = fc.home_weak.astype(int)
    fc["home_med"] = fc.home_list.map(lambda h: int(GROUP_OF_FIELD[h[0]] == "Med"))
    fc["label_cov"] = fc.label_coverage_early
    fc["newborn_i"] = 1
    G = {}
    for sp in ("dev", "heldout"):
        z = np.load(EXP6 / "scan" / f"frame_g_{sp}.npz")
        G.update({int(c): z["g"][i] for i, c in enumerate(z["cidx"])})
    return fc, G


def recognition_keys(openalex_ints: set[int]) -> tuple[set[str], set[str], int]:
    """(qids, label_norms, n_records) from the concept_recognition dataset for the given OpenAlex ids."""
    qids, labels, n = set(), set(), 0
    for f in sorted((DS2 / "full_data_out").glob("full_data_out_*.json")):
        d = json.loads(f.read_text())
        for ds in d["datasets"]:
            if ds["dataset"] != "concept_recognition":
                continue
            for ex in ds["examples"]:
                n += 1
                inp = json.loads(ex["input"])
                oid = int(str(inp["openalex_id"]).lstrip("C"))
                if oid in openalex_ints:
                    for k in ("qid", "qid_resolved"):
                        if inp.get(k):
                            qids.add(str(inp[k]))
                    if inp.get("label_norm"):
                        labels.add(inp["label_norm"])
                    if inp.get("label"):
                        labels.add(norm(inp["label"]))
        del d
    return qids, labels, n


def dedup(exp5: pd.DataFrame, exp6: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    ids6 = {int(u.split("/C")[-1]) for u in exp6.concept_id}
    lx = pd.read_parquet(EXP6 / "results" / "lexicon.parquet", columns=["oa_int", "wikidata", "name"])
    q6 = {str(w).rsplit("/", 1)[-1] for w in lx[lx.oa_int.isin(ids6)].wikidata.dropna()}
    rq, rl, nrec = recognition_keys(ids6)
    q6 |= rq
    lab6 = {norm(n) for n in exp6.name} | {norm(x) for x in rl}
    by_id = exp5.concept_id.astype(int).isin(ids6)
    by_q = exp5.qid.astype(str).isin(q6)
    by_l = exp5.name.map(norm).isin(lab6)
    drop = by_id | by_q | by_l
    rep = {"n_exp5": int(len(exp5)), "n_exp6_newborn_frame": int(len(exp6)), "n_exp6_ids": len(ids6), "n_exp6_qids": len(q6),
           "n_exp6_labels": len(lab6), "concept_recognition_records_scanned": nrec,
           "dropped_by_id": int(by_id.sum()), "dropped_by_qid": int(by_q.sum()), "dropped_by_label": int(by_l.sum()),
           "dropped_union": int(drop.sum()), "dropped_only_by_qid": int((by_q & ~by_id & ~by_l).sum()),
           "dropped_only_by_label": int((by_l & ~by_id & ~by_q).sum()),
           "kept": int((~drop).sum()),
           "dropped_by_split_group": exp5[drop].groupby(["split", "group"]).size().rename("n").reset_index().to_dict("records"),
           "dropped_concept_ids": sorted(map(int, exp5[drop].concept_id)),
           "exp6_ids_not_in_exp5": int(len(ids6 - set(exp5.concept_id.astype(int))))}
    return exp5[~drop].copy(), rep


def exp5_frame() -> pd.DataFrame:
    fc = pd.read_csv(EXP5 / "frame_concepts.csv")
    fc["home_list"] = [[int(h) for h in str(x).split(";")] for x in fc.home]
    fc["cidx"] = fc.ci.astype(int)
    fc["intersect"] = fc.intersect40.astype(int)
    fc["home_med"] = (fc.group == "Med").astype(int)
    fc["label_cov"] = fc.label_coverage_early
    fc["newborn_i"] = fc.newborn.astype(int)
    unit = np.where(fc.split.str.startswith("HELDOUT_"), fc.split.str.replace("HELDOUT_", "", regex=False), fc.split)
    unit = np.where(fc.split == "COHORT", np.where(fc.group.isin(DEV_GROUPS), "COHORT_DEVHOME", "COHORT_NONDEVHOME"), unit)
    fc["unit"] = unit
    return fc


def grounded_arrays(ci: np.ndarray) -> dict[str, np.ndarray]:
    """V [C, NY, 27] venue-field, P [C, NY, 27] primary-topic field, N [C, NY] all venues; weight = tagstate == 1
    (EXP5 frozen rule 'c_TAG'). Rows aligned with `ci`."""
    rule = json.loads((EXP5 / "grounding_report.json").read_text())["frozen_grounding_rule"]
    assert rule == "c_TAG", rule
    ag = pd.read_parquet(EXP5 / "scan" / "agg_counts.parquet", filters=[("tagstate", "==", 1)],
                         columns=["ci", "year", "vfield", "ptfield", "n"])
    pos = pd.Series(np.arange(len(ci)), index=ci)
    ag = ag[ag.ci.isin(pos.index)]
    r = pos.loc[ag.ci.to_numpy()].to_numpy()
    y = ag.year.to_numpy(np.int64) - Y0
    ok = (y >= 0) & (y < NY)
    r, y, n = r[ok], y[ok], ag.n.to_numpy(np.float64)[ok]
    vf, pt = ag.vfield.to_numpy(np.int64)[ok], ag.ptfield.to_numpy(np.int64)[ok]
    C = len(ci)
    N = np.bincount(r * NY + y, weights=n, minlength=C * NY).reshape(C, NY).astype(np.float32)
    V = np.bincount((r * NY + y) * 27 + vf, weights=n, minlength=C * NY * 27).reshape(C, NY, 27).astype(np.float32)
    P = np.bincount((r * NY + y) * 27 + pt, weights=n, minlength=C * NY * 27).reshape(C, NY, 27).astype(np.float32)
    return {"N": N, "V": V, "P": P}


def home_rule(V: np.ndarray, t0: int, n_first: int = 30) -> list[int]:
    """EXP5 frame.home_rule (re-implemented): fields with >= 40% of the first 30 venue-labelled works from t0 on
    (proportional boundary year), else the top field if >= 25% (weak home)."""
    acc = np.zeros(26)
    got = 0.0
    for y in range(t0, Y0 + NY):
        row = V[y - Y0, 1:27].astype(float)
        tot = row.sum()
        if tot <= 0:
            continue
        need = n_first - got
        if tot <= need:
            acc += row; got += tot
        else:
            acc += row * need / tot; got += need
        if got >= n_first - 1e-9:
            break
    if got <= 0:
        return []
    sh = acc / got
    home = [FIELD_IDS[k] for k in range(26) if sh[k] >= 0.4]
    if home:
        return sorted(home, key=lambda f: -sh[f - 11])
    o = int(np.argmax(sh))
    return [FIELD_IDS[o]] if sh[o] >= 0.25 else []


def phi_min_cp(years: tuple[int, int] = (1998, 2002)) -> np.ndarray:
    """Hidalgo min-conditional-probability proximity from EXP5 26x26 field co-assignment: C_jk / max(C_jj, C_kk)."""
    z = np.load(EXP5 / "scan" / "co_by_year.npz")
    yrs = list(z["years"])
    Cm = z["CO"][yrs.index(years[0]):yrs.index(years[1]) + 1].sum(0).astype(float)
    d = np.diag(Cm)
    P = Cm / np.maximum(np.maximum.outer(d, d), 1)
    np.fill_diagonal(P, 0)
    return (P + P.T) / 2
