"""D3 field-year state machine, RCA portfolios and concept x field entry risk sets, vectorised over concepts.

Semantics are EXACTLY those of EXP6 lib/h2.py (copied verbatim to lib/h2_exp6.py):
  entered(t)  = cumulative grounded count >= min_n
  retaining(t)= entered(t-2) & w3(t) >= min_n & off-home          (w3 = count over t-2..t)
  lost(t)     = entered(t) & w3(t) == 0                           (off-home filter applied at risk-set time)
  risk set    = concept-year strata t = t0+1..min(t0+horizon, 2022); candidates = ~entered(t-1) & off-home;
                event = entered(t) & candidate.
Everything that EXP6 computes per row is computed here as (per-stratum field mask) @ phi, gathered at the target
field k, which makes permutation / rewiring nulls a single matrix product.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

Y0, Y1 = 1995, 2022
NY = Y1 - Y0 + 1
NF = 26


# ----------------------------------------------------------------------------- states
def panel_states(G: np.ndarray, home_mask: np.ndarray, min_n: float = 2) -> dict[str, np.ndarray]:
    """G [C, NY, 27] grounded counts (slot 0 = unlabelled venue); home_mask [C, 26] bool.
    Returns [C, NY, 26] arrays (bool / int16 / float32)."""
    x = G[:, :, 1:].astype(np.float64)
    cum = np.cumsum(x, 1)
    entered = cum >= min_n
    w3 = x.copy()
    w3[:, 1:] += x[:, :-1]
    w3[:, 2:] += x[:, :-2]
    ent_lag2 = np.zeros_like(entered)
    ent_lag2[:, 2:] = entered[:, :-2]
    offhome = ~home_mask
    retaining = ent_lag2 & (w3 >= min_n) & offhome[:, None, :]
    lost = entered & (w3 == 0)
    yr = np.arange(NY, dtype=np.int16)
    first = np.where(entered.any(1), entered.argmax(1), NY).astype(np.int16)  # [C, 26]
    age = (yr[None, :, None] - first[:, None, :]).astype(np.int16)          # valid where entered
    lastpos = np.maximum.accumulate(np.where(x > 0, yr[None, :, None], -1), axis=1).astype(np.int16)
    tenure = (lastpos - first[:, None, :]).astype(np.int16)                  # tenure of a LOST presence
    return {"x": x.astype(np.float32), "cum": cum.astype(np.float32), "w3": w3.astype(np.float32),
            "entered": entered, "ent_lag2": ent_lag2, "retaining": retaining, "lost": lost,
            "offhome": offhome, "age": age, "tenure": tenure, "first": first}


def rca_entered_panel(G: np.ndarray, GF: np.ndarray, min_n: float = 2) -> np.ndarray:
    """Vectorised h2_exp6.rca_entered: cum >= 2 AND cumulative share > field's cumulative share of all works; absorbing."""
    x = np.cumsum(G[:, :, 1:].astype(np.float64), 1)
    tot = x.sum(2, keepdims=True)
    F = np.cumsum(GF.astype(np.float64), 0)
    share_all = F / np.maximum(F.sum(1, keepdims=True), 1)
    share_c = x / np.maximum(tot, 1)
    ok = (x >= min_n) & (share_c > share_all[None])
    return np.maximum.accumulate(ok.astype(np.int8), 1).astype(bool)


def _rca(nc: np.ndarray, NT: np.ndarray) -> np.ndarray:
    """nc [..., 26] concept counts, NT [..., 26] base totals broadcastable. RCA = (nc/sum nc) / (NT/sum NT); 0 if nc empty."""
    s = nc.sum(-1, keepdims=True)
    share_c = nc / np.where(s > 0, s, 1)
    share_all = NT / np.maximum(NT.sum(-1, keepdims=True), 1)
    return np.where(s > 0, share_c / np.where(share_all > 0, share_all, np.inf), 0.0)


def rolling(a: np.ndarray, w: int, axis: int) -> np.ndarray:
    """sum over the trailing window [y-w+1, y] (partial at the start)."""
    c = np.cumsum(a, axis)
    out = c.copy()
    sl = [slice(None)] * a.ndim
    sl2 = [slice(None)] * a.ndim
    sl[axis] = slice(w, None)
    sl2[axis] = slice(None, -w)
    out[tuple(sl)] = c[tuple(sl)] - c[tuple(sl2)]
    return out


def rca_panel(x: np.ndarray, GF: np.ndarray) -> dict[str, np.ndarray]:
    """x [C, NY, 26] counts; GF [NY, 26] venue-field base totals. Portfolio masks [C, NY, 26] evaluated AT year y
    (the risk-set code reads them at y = t-1). RCA > 1 (strict)."""
    x = x.astype(np.float64)
    GF = GF.astype(np.float64)
    r1 = _rca(x, GF[None])
    xw, Gw = rolling(x, 3, 1), rolling(GF, 3, 0)
    rw = _rca(xw, Gw[None])
    rc = _rca(np.cumsum(x, 1), np.cumsum(GF, 0)[None])
    Uw = rw > 1
    Uw_prev = np.zeros_like(Uw)
    Uw_prev[:, 3:] = Uw[:, :-3]                 # window y-5..y-3
    return {"U_1y": r1 > 1, "U_w3": Uw, "U_cum": rc > 1, "U_pers": Uw & Uw_prev, "rca_1y": r1.astype(np.float32),
            "ties_1y": int(np.isclose(r1, 1.0, rtol=0, atol=1e-12).sum())}


# ----------------------------------------------------------------------------- strata
STRATUM_MASKS = ["E", "ENTOFF", "RET", "LOST", "POOL", "HOME", "U_1y", "U_w3", "U_cum", "U_pers",
                 "RET_a2", "RET_a3", "RET_a4p", "LOST_s", "LOST_l"]


def build_strata(frame: pd.DataFrame, G: np.ndarray, GF: np.ndarray, *, horizon: int = 10, min_n: float = 2,
                 entry_def: str = "count") -> dict:
    """frame rows aligned with G (row i <-> G[i]); needs columns cidx, t0, home_list (list[int]).
    Returns per-stratum arrays (masks [S, 26] at t-1, counts, candidates, events) + stratum meta."""
    C = len(frame)
    home = np.zeros((C, NF), bool)
    for i, hl in enumerate(frame.home_list):
        for h in hl:
            home[i, h - 11] = True
    S = panel_states(G, home, min_n)
    R = rca_panel(S["x"], GF)
    ent = rca_entered_panel(G, GF, min_n) if entry_def == "rca" else S["entered"]
    t0 = frame.t0.to_numpy().astype(int)
    ci_l, t_l = [], []
    for i in range(C):
        for t in range(t0[i] + 1, min(t0[i] + horizon, Y1) + 1):
            ci_l.append(i); t_l.append(t)
    ci = np.array(ci_l, np.int64)
    t = np.array(t_l, np.int64)
    ti = t - Y0
    p = ti - 1                                                  # state row t-1
    E = ent[ci, p]
    offh = S["offhome"][ci]
    cand = ~E & offh
    keep = cand.any(1)
    ci, t, ti, p, E, offh, cand = ci[keep], t[keep], ti[keep], p[keep], E[keep], offh[keep], cand[keep]
    ev = ent[ci, ti] & cand
    RET = S["retaining"][ci, p]
    LOST = S["lost"][ci, p] & offh
    age = S["age"][ci, p]
    ten = S["tenure"][ci, p]
    POOL = S["ent_lag2"][ci, p] & offh                        # age-eligible entered off-home fields (RET subset)
    out = {"row_i": ci, "t": t, "cand": cand, "event": ev, "E": E, "ENTOFF": S["entered"][ci, p] & offh, "RET": RET,
           "LOST": LOST, "POOL": POOL, "HOME": home[ci],
           "U_1y": R["U_1y"][ci, p], "U_w3": R["U_w3"][ci, p], "U_cum": R["U_cum"][ci, p], "U_pers": R["U_pers"][ci, p],
           "RET_a2": RET & (age == 2), "RET_a3": RET & (age == 3), "RET_a4p": RET & (age >= 4),
           "LOST_s": LOST & (ten <= 1), "LOST_l": LOST & (ten >= 2),
           "xprev": S["x"][ci, p], "w3prev": S["w3"][ci, p], "cumprev": S["cum"][ci, p], "age": age,
           "logGF_prev": np.log(np.maximum(GF[p].astype(np.float64), 1)),
           "ties_rca_1y": R["ties_1y"], "min_n": min_n, "horizon": horizon, "entry_def": entry_def}
    # strict retained-footprint diagnostics for permutation (share of strata where the permutation is non-trivial)
    out["n_ret"] = RET.sum(1)
    out["n_pool"] = POOL.sum(1)
    return out


def _mrel(M: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """mean_{j in M} phi[j, k] for every k -> [S, 26]; zero when M is empty (EXP6 convention)."""
    n = M.sum(1, keepdims=True).astype(np.float64)
    return np.where(n > 0, (M.astype(np.float64) @ phi) / np.where(n > 0, n, 1), 0.0)


def _dens(M: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """Hidalgo density omega_k = sum_j M_j phi_jk / sum_j phi_jk -> [S, 26]."""
    cs = phi.sum(0)
    return (M.astype(np.float64) @ phi) / np.where(cs > 0, cs, 1)[None, :]


def _wdens(W: np.ndarray, phi: np.ndarray) -> np.ndarray:
    cs = phi.sum(0)
    return (W.astype(np.float64) @ phi) / np.where(cs > 0, cs, 1)[None, :]


def _share(v: np.ndarray) -> np.ndarray:
    s = v.sum(1, keepdims=True)
    return v / np.where(s > 0, s, 1)


def _gw(M: np.ndarray, phi: np.ndarray, gate: np.ndarray) -> np.ndarray:
    Wm = M * gate[None, :]
    den = Wm.sum(1, keepdims=True)
    return np.where(den > 0, (Wm @ phi) / np.where(den > 0, den, 1), 0.0)


NB_COARSE, CB_COARSE = [0.5, 1.5, 3.5], [2.5, 4.5, 9.5]                       # pre-declared (plan)
NB_FINE, CB_FINE = [0.5, 1.5, 3.5, 7.5, 15.5, 31.5], [2.5, 4.5, 9.5, 19.5, 49.5]  # added on EXP6/DEV before the freeze


def vol_matched_masks(st: dict, fine: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Volume-matched retained (R) vs entered-not-retained (N) off-home fields at t-1: coarsen n(t-1) {0,1,2-3,4+} x
    cum(t-1) {2,3-4,5-9,10+} (fine: n {0,1,2-3,4-7,8-15,16-31,32+} x cum {2,3-4,5-9,10-19,20-49,50+});
    keep only cells holding >= 1 R and >= 1 N."""
    n = st["xprev"]; cu = st["cumprev"]
    ne, ce = (NB_FINE, CB_FINE) if fine else (NB_COARSE, CB_COARSE)
    nb = np.digitize(n, ne)
    cb = np.digitize(cu, ce)
    ncell = (len(ne) + 1) * (len(ce) + 1)
    code = nb * (len(ce) + 1) + cb
    R = st["RET"]
    N = st["ENTOFF"] & ~st["RET"]
    oh = np.eye(ncell, dtype=bool)[code]                  # [S, 26, ncell]
    rc = (oh & R[:, :, None]).any(1)
    nc = (oh & N[:, :, None]).any(1)
    ok = rc & nc                                          # [S, 16]
    cell_ok = (oh & ok[:, None, :]).any(2)                # [S, 26]
    return R & cell_ok, N & cell_ok


def covariates(st: dict, phi: np.ndarray, gate: np.ndarray, which: set[str] | None = None) -> pd.DataFrame:
    """Row table: one row per (stratum, candidate field). Columns as in EXP6 + the EXP7 rivals and decompositions."""
    s_idx, k = np.nonzero(st["cand"])
    g = lambda A: A[s_idx, k]  # noqa: E731
    cols = {"s_idx": s_idx, "field": k + 11, "entered": st["event"][s_idx, k].astype(np.int8)}
    cols["a_phi_home"] = g(_mrel(st["HOME"], phi))
    cols["b_log_size"] = st["logGF_prev"][s_idx, k]
    cols["c_density"] = g(_dens(st["E"], phi))
    cols["e_gate_own"] = gate[k]
    cols["d0_ret_rel"] = g(_mrel(st["RET"], phi))
    cols["d_ret_gate"] = g(_gw(st["RET"], phi, gate))
    cols["d_lost_gate"] = g(_gw(st["LOST"], phi, gate))
    cols["d_lost"] = g(_mrel(st["LOST"], phi))
    for u in ("U_1y", "U_w3", "U_cum", "U_pers"):
        cols["D_rca_" + u[2:]] = g(_dens(st[u], phi))
    cols["D_vol"] = g(_wdens(_share(st["xprev"]), phi))
    cols["D_vol_w3"] = g(_wdens(_share(st["w3prev"]), phi))
    cols["D_cum"] = g(_wdens(_share(st["cumprev"]), phi))
    for m in ("RET_a2", "RET_a3", "RET_a4p"):
        cols["d_ret_" + m[4:]] = g(_mrel(st[m], phi))
    cols["d_lost_short"] = g(_mrel(st["LOST_s"], phi))
    cols["d_lost_long"] = g(_mrel(st["LOST_l"], phi))
    Rm, Nm = vol_matched_masks(st)
    cols["d_R_m"] = g(_mrel(Rm, phi))
    cols["d_N_m"] = g(_mrel(Nm, phi))
    cols["has_match"] = (Rm.any(1) & Nm.any(1))[s_idx].astype(np.int8)
    Rf, Nf = vol_matched_masks(st, fine=True)
    cols["d_R_mf"] = g(_mrel(Rf, phi))
    cols["d_N_mf"] = g(_mrel(Nf, phi))
    cols["has_match_f"] = (Rf.any(1) & Nf.any(1))[s_idx].astype(np.int8)
    cols["n_ret"] = st["RET"].sum(1)[s_idx]
    cols["n_lost"] = st["LOST"].sum(1)[s_idx]
    cols["n_entered_off"] = st["ENTOFF"].sum(1)[s_idx]
    cols["n_pool"] = st["POOL"].sum(1)[s_idx]
    return pd.DataFrame(cols)


PHI_COLS = ["a_phi_home", "c_density", "d0_ret_rel", "d_ret_gate", "d_lost_gate", "d_lost", "D_rca_1y", "D_rca_w3",
            "D_rca_cum", "D_rca_pers", "D_vol", "D_vol_w3", "D_cum", "d_ret_a2", "d_ret_a3", "d_ret_a4p",
            "d_lost_short", "d_lost_long", "d_R_m", "d_N_m", "d_R_mf", "d_N_mf"]


def attach_meta(df: pd.DataFrame, st: dict, frame: pd.DataFrame, meta_cols: list[str]) -> pd.DataFrame:
    """add cidx, t, age, stratum and concept-level meta columns."""
    ri = st["row_i"][df.s_idx.to_numpy()]
    df.insert(0, "cidx", frame.cidx.to_numpy()[ri])
    df.insert(1, "t", st["t"][df.s_idx.to_numpy()])
    df.insert(2, "age", df.t.to_numpy() - frame.t0.to_numpy()[ri])
    for c in meta_cols:
        df[c] = frame[c].to_numpy()[ri]
    df["stratum"] = df.cidx.astype(np.int64) * 100 + (df.t - 2000)
    return df
