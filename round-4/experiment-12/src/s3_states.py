#!/usr/bin/env python3
"""S3 STATE SEQUENCES (ages 0..10; analysis ages 0..8) with the EXP6/EXP7 D3 semantics (lib/d3.panel_states):
  entered(t) = cumulative grounded count >= min_n; retaining(t) = entered(t-2) & w3(t) >= min_n & off-home;
  lost(t) = entered(t) & w3(t) == 0. Code: 0 UNTOUCHED, 1 ENTERED, 2 RETAINED, 3 LOST, 4 HOME (EXP7 precedence).
Rebuilt for ALL 12,499 concepts from EXP8 frame_arrays.npz (V [C, 28, 27]) and VERIFIED cell by cell against the
EXP7 state_panel on its 11,841 concepts. Writes state_sequences.parquet, panel.parquet, data/decomp_inputs.parquet,
results/states_verification.json and results/transitions_dev.json."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.special import gammaln  # noqa: E402

import d3  # noqa: E402
from common import (AGES, DATA, E5, E6, E7, E8_DATA, H, LOGS, NF, NY, RES, ROOT, Y0, Y1, jdump, jload,  # noqa: E402
                    network_guard, setup_logger, spearman, update_status)

network_guard()
logger = setup_logger("s3_states")
STATE_NAMES = {0: "UNTOUCHED", 1: "ENTERED", 2: "RETAINED", 3: "LOST", 4: "HOME", -1: "NA_after_2022"}


def load_J() -> pd.DataFrame:
    J = pd.read_parquet(DATA / "joined.parquet")
    J["home_list"] = [[int(x) for x in s.split(";")] for s in J.home_list]
    return J


def load_V(J: pd.DataFrame) -> np.ndarray:
    z = np.load(E8_DATA / "frame_arrays.npz")
    pos = pd.Series(np.arange(len(z["ci"])), index=z["ci"])
    return z["V"][pos.loc[J.ci.to_numpy()].to_numpy()].astype(np.float64)


def hmask(J) -> np.ndarray:
    m = np.zeros((len(J), NF), bool)
    for i, hl in enumerate(J.home_list):
        for h in hl:
            m[i, h - 11] = True
    return m


def state_code(S: dict, home: np.ndarray) -> np.ndarray:
    code = np.zeros(S["x"].shape, np.int8)
    code[S["entered"]] = 1
    code[S["retaining"]] = 2
    code[S["lost"] & S["offhome"][:, None, :]] = 3
    code[np.broadcast_to(home[:, None, :], code.shape)] = 4
    return code


def field_communities() -> dict:
    """Louvain on the EXP6 26-field PMI backbone (positive phi), seed 0; first resolution giving 4-8 communities."""
    import json

    import networkx as nx
    bb = json.loads((E6 / "inputs/field_backbone.json").read_text())
    phi = np.clip(np.asarray(bb["phi"], float), 0, None)
    G = nx.Graph()
    G.add_nodes_from(range(NF))
    for i in range(NF):
        for j in range(i + 1, NF):
            if phi[i, j] > 0:
                G.add_edge(i, j, weight=phi[i, j])
    tried = {}
    for res in (0.5, 0.75, 1.0, 1.25, 1.5):
        cs = nx.community.louvain_communities(G, weight="weight", resolution=res, seed=0)
        tried[res] = len(cs)
        if 4 <= len(cs) <= 8:
            lab = np.zeros(NF, int)
            for c, members in enumerate(sorted(cs, key=lambda s: min(s))):
                for m in members:
                    lab[m] = c
            return {"resolution": res, "labels": lab.tolist(), "n_comm": len(cs), "tried": tried,
                    "members": [[bb["fields"][m] for m in sorted(s)] for s in sorted(cs, key=lambda s: min(s))]}
    raise RuntimeError(f"no resolution gives 4-8 communities: {tried}")


def rarefied(win: np.ndarray, m: int) -> np.ndarray:
    """vectorised exact hypergeometric rarefaction E[S_m] over the last axis (NaN if N < m); EXP6 logic."""
    N = win.sum(-1, keepdims=True)
    lc = lambda a, b: gammaln(a + 1) - gammaln(b + 1) - gammaln(a - b + 1)  # noqa: E731
    with np.errstate(invalid="ignore", over="ignore"):
        term = np.where(N - win < m, 1.0, 1.0 - np.exp(lc(np.maximum(N - win, m), m) - lc(np.maximum(N, m), m)))
    term = np.where(win > 0, term, 0.0)
    out = term.sum(-1)
    return np.where(N[..., 0] >= m, out, np.nan)


def shannon(win: np.ndarray) -> np.ndarray:
    N = win.sum(-1, keepdims=True)
    p = win / np.where(N > 0, N, 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        h = -(np.where(p > 0, p * np.log(p), 0.0)).sum(-1)
    return np.where(N[..., 0] > 0, h, np.nan)


def gather_age(A: np.ndarray, t0: np.ndarray, ages: list[int], fill=np.nan) -> np.ndarray:
    """A [C, NY, ...] -> [C, len(ages), ...] at year t0+age (fill where the year is outside 1995..2022)."""
    yi = (t0[:, None] - Y0) + np.asarray(ages)[None, :]
    ok = (yi >= 0) & (yi < NY)
    out = A[np.arange(len(t0))[:, None], np.clip(yi, 0, NY - 1)]
    if out.dtype.kind in "fc":
        out = np.where(ok.reshape(ok.shape + (1,) * (out.ndim - 2)), out, fill)
    return out, ok


def summaries(V: np.ndarray, home: np.ndarray, t0: np.ndarray, GF: np.ndarray, comm: np.ndarray,
              min_n: float = 2, ages=AGES) -> tuple[dict, dict]:
    S = d3.panel_states(V, home, min_n)
    x = S["x"].astype(np.float64)                         # labelled counts [C, NY, 26]
    off = S["offhome"]                                    # [C, 26]
    ent_off = (S["entered"] & off[:, None, :]).sum(2)     # [C, NY]
    n_ret = S["retaining"].sum(2)
    n_lost = (S["lost"] & off[:, None, :]).sum(2)
    lag = lambda a, k: np.concatenate([np.zeros_like(a[:, :k]), a[:, :-k]], 1)  # noqa: E731
    new_ent = ent_off - lag(ent_off, 1)
    ret_share = n_ret / np.maximum(1, lag(ent_off, 2))
    frontier = new_ent / np.maximum(1, lag(n_ret, 1))
    w3 = S["w3"].astype(np.float64)                       # 3-yr window counts per field
    R20 = rarefied(w3, 20)
    Hh = shannon(w3)
    lab3 = w3.sum(2)
    home_share = np.where(lab3 > 0, (w3 * home[:, None, :]).sum(2) / np.where(lab3 > 0, lab3, 1), np.nan)
    hp_den = (GF[None, :, :] * home[:, None, :]).sum(2)
    HP = np.where(hp_den > 0, (x * home[:, None, :]).sum(2) / np.where(hp_den > 0, hp_den, 1) * 1e4, 0.0)
    ncomm = comm.max() + 1
    Cm = np.eye(ncomm)[comm]                              # [26, ncomm]
    touched = ((S["retaining"] | home[:, None, :]).astype(np.float64) @ Cm) > 0
    comm_span = touched.sum(2)
    offw = w3 * off[:, None, :]
    cw = offw @ Cm
    ct = cw.sum(2, keepdims=True)
    part_ret = np.where(ct[..., 0] > 0, 1 - ((cw / np.where(ct > 0, ct, 1)) ** 2).sum(2), np.nan)
    n_c = V.sum(2)
    n_lab = V[:, :, 1:].sum(2)
    label_cov = np.where(n_c > 0, n_lab / np.where(n_c > 0, n_c, 1), np.nan)
    n_off = (x * off[:, None, :]).sum(2)
    yearly = {"n_c": n_c, "n_off": n_off, "n_ent_off": ent_off, "new_entries": new_ent, "n_ret": n_ret,
              "n_lost": n_lost, "ret_share": ret_share, "frontier": frontier, "R20": R20, "H": Hh,
              "home_share": home_share, "HP": HP, "comm_span": comm_span, "part_ret": part_ret, "label_cov": label_cov}
    out = {}
    for k, A in yearly.items():
        g, ok = gather_age(A.astype(np.float64), t0, ages)
        out[k] = g
    out["_ok"] = ok
    return out, S


def decomp_inputs(V, home, t0, min_n: float, tag: str) -> pd.DataFrame:
    S = d3.panel_states(V, home, min_n)
    off = S["offhome"]
    ent_off = (S["entered"] & off[:, None, :]).sum(2).astype(float)
    n_ret = S["retaining"].sum(2).astype(float)
    e, _ = gather_age(ent_off, t0, [2, H])
    b, _ = gather_age(n_ret, t0, [H])
    return pd.DataFrame({f"E2{tag}": e[:, 0], f"EH{tag}": e[:, 1], f"Bn{tag}": b[:, 0]})


def transitions(codes: np.ndarray, groups: np.ndarray, ages=range(0, H)) -> dict:
    """year-to-year transition counts between off-home states 0..3 (ages a -> a+1), per group."""
    out = {}
    for g in list(np.unique(groups)) + ["ALL"]:
        m = np.ones(len(groups), bool) if g == "ALL" else groups == g
        T = np.zeros((4, 4), np.int64)
        for a in ages:
            s0 = codes[m, a].ravel()
            s1 = codes[m, a + 1].ravel()
            ok = (s0 >= 0) & (s0 <= 3) & (s1 >= 0) & (s1 <= 3)
            np.add.at(T, (s0[ok], s1[ok]), 1)
        rate = T / np.maximum(T.sum(1, keepdims=True), 1)
        out[str(g)] = {"counts": T.tolist(), "rates": rate.round(5).tolist(), "n_concepts": int(m.sum())}
    out["_states"] = ["UNTOUCHED", "ENTERED", "RETAINED", "LOST"]
    return out


@logger.catch(reraise=True)
def main() -> None:
    J = load_J()
    V = load_V(J)
    home = hmask(J)
    t0 = J.t0.to_numpy().astype(int)
    GF = np.load(E5 / "scan/year_field_totals.npz")["VF"][:, 1:].astype(np.float64)
    logger.info(f"V {V.shape}; t0 range {t0.min()}..{t0.max()}")
    # ---------------- verification against EXP7 state_panel
    S = d3.panel_states(V, home, 2)
    code = state_code(S, home)
    sp = pd.concat([pd.read_parquet(E7 / f"results/state_panel_{s}.parquet",
                                    columns=["concept_id", "field", "year", "state", "n"]) for s in ("dev", "heldout")])
    pos = pd.Series(np.arange(len(J)), index=J.concept_id.to_numpy())
    in_sp = J.concept_id.isin(set(sp.concept_id.unique())).to_numpy()
    i = pos.loc[sp.concept_id.to_numpy()].to_numpy()
    yv = sp.year.to_numpy() - Y0
    fv = sp.field.to_numpy() - 11
    mine = code[i, yv, fv]
    mism = int((mine != sp.state.to_numpy()).sum())
    nmis = int((np.abs(S["x"][i, yv, fv] - sp.n.to_numpy()) > 1e-6).sum())
    missing = J[~in_sp]
    ver = {"sp_rows": len(sp), "sp_concepts": int(in_sp.sum()), "missing_concepts": int((~in_sp).sum()),
           "missing_are_exp6_overlap": bool(missing.in_exp6.all()), "state_cell_mismatches": mism,
           "count_cell_mismatches": nmis, "mismatch_share": mism / len(sp),
           "state_distribution_sp": sp.state.value_counts().sort_index().to_dict()}
    del sp, i, yv, fv, mine
    logger.info(f"VERIFY vs EXP7 state_panel: {ver['sp_concepts']} concepts, {ver['sp_rows']:,} cells, "
                f"state mismatches {mism}, count mismatches {nmis}; missing {ver['missing_concepts']} "
                f"(all EXP6 overlap: {ver['missing_are_exp6_overlap']})")
    # ---------------- RETENTION_RATIO_early re-derivation (EXP8 definition, t0..t0+2 window)
    rr, cr = [], []
    for r in range(len(J)):
        yi0 = t0[r] - Y0
        x3 = V[r, yi0:yi0 + 3, 1:]
        off = ~home[r]
        contact = int(((x3.sum(0) >= 1) & off).sum())
        ret = int((((x3 >= 2).sum(0) >= 2) & off).sum())
        rr.append(ret / max(contact, 1))
        cr.append(contact)
    rr, cr = np.array(rr), np.array(cr)
    ver["RETENTION_RATIO_early_rederived"] = {
        "max_abs_diff_vs_E8": float(np.nanmax(np.abs(rr - J.RETENTION_RATIO_early.to_numpy()))),
        "CONTACT_REACH_max_abs_diff": float(np.nanmax(np.abs(cr - J.CONTACT_REACH.to_numpy())))}
    # ---------------- communities, summaries
    comm = field_communities()
    jdump(comm, RES / "field_communities.json")
    logger.info(f"field communities: resolution {comm['resolution']}, {comm['n_comm']} communities")
    sm, _ = summaries(V, home, t0, GF, np.asarray(comm["labels"]), 2)
    ok = sm.pop("_ok")
    d3ratio = sm["n_ret"][:, 2] / np.maximum(1, sm["n_ent_off"][:, 2])
    ver["RETENTION_RATIO_early_vs_D3_age2_ratio_spearman"] = spearman(rr, d3ratio)
    ver["note"] = ("RETENTION_RATIO_early (EXP8: fields with >= 2 papers in >= 2 of the 3 window years / fields "
                   "touched in the window) is re-derived EXACTLY from the same arrays; the D3 age-2 ratio "
                   "(retaining at t0+2 / entered by t0+2, cumulative history since 1995) is a different "
                   "definition and is reported only as a rank correlation.")
    jdump(ver, RES / "states_verification.json")
    C = len(J)
    na = len(AGES)
    P = pd.DataFrame({"ci": np.repeat(J.ci.to_numpy(), na), "age": np.tile(AGES, C),
                      "year": np.repeat(t0, na) + np.tile(AGES, C), "extended": np.tile(np.array(AGES) > 8, C),
                      "in_window": ok.ravel()})
    for k, A in sm.items():
        P[k] = A.ravel().astype(np.float32)
    P.to_parquet(ROOT / "panel.parquet", index=False)
    # ---------------- state sequences (ci, age, field, state)
    cg, okc = gather_age(code, t0, AGES)
    cg = np.where(okc[:, :, None], cg, -1).astype(np.int8)
    np.save(DATA / "state_codes.npy", cg)
    SS = pd.DataFrame({"ci": np.repeat(J.ci.to_numpy(), na * NF).astype(np.int32),
                       "age": np.tile(np.repeat(np.array(AGES, np.int8), NF), C),
                       "field": np.tile(np.arange(11, 37, dtype=np.int8), C * na), "state": cg.ravel()})
    SS.to_parquet(ROOT / "state_sequences.parquet", index=False)
    logger.info(f"panel {P.shape}; state_sequences {len(SS):,} rows")
    # ---------------- decomposition inputs (min_n 2/3/5; onset-restricted sensitivity)
    D = [J[["ci"]].reset_index(drop=True)]
    for mn in (2, 3, 5):
        D.append(decomp_inputs(V, home, t0, mn, "" if mn == 2 else f"_mn{mn}"))
    Vw = V.copy()
    for r in range(C):
        Vw[r, :t0[r] - Y0] = 0.0
    D.append(decomp_inputs(Vw, home, t0, 2, "_onset"))
    D = pd.concat(D, axis=1)
    D["RETENTION_RATIO_early_rederived"] = rr
    D.to_parquet(DATA / "decomp_inputs.parquet", index=False)
    pre = (V[np.arange(C)[:, None], np.clip((t0[:, None] - Y0) + np.arange(-30, 0)[None, :], 0, NY - 1)].sum(2)
           * ((t0[:, None] - Y0) + np.arange(-30, 0)[None, :] >= 0)).sum(1)
    D2 = pd.DataFrame({"ci": J.ci, "pre_onset_papers": pre})
    D2.to_parquet(DATA / "pre_onset.parquet", index=False)
    # ---------------- transitions (DEV only before the seal)
    dev = (J.split == "DEV").to_numpy()
    jdump(transitions(cg[dev][:, :, :], J.group.to_numpy()[dev]) | {"split": "DEV"}, RES / "transitions_dev.json")
    logger.info(f"decomp inputs: E2>=1 {float((D.E2 >= 1).mean()):.3f}, Bn>=1 {float((D.Bn >= 1).mean()):.3f}")
    update_status("S3_states", {"states_verification": {k: ver[k] for k in ("state_cell_mismatches",
                                                                          "sp_concepts", "missing_concepts")}})


if __name__ == "__main__":
    main()
