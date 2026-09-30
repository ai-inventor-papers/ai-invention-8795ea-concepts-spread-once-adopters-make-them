"""Shared panel definitions (imported by preseal.py and every post-seal script so the frozen formulas are applied
identically): bodies, home lists, OPEN_home, closure jumps, the estimation panel with t+1 outcomes."""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

COMP = ["new_rate", "n_comm", "participation", "nov_res", "density", "persistence"]
SIGN = {"new_rate": 1, "n_comm": 1, "participation": 1, "nov_res": 1, "density": -1, "persistence": -1}
CONTROLS = ["log1p_home", "log1p_all", "log1p_deg", "log_at_risk"]
BODIES = ["DEV", "OLD_HELDOUT", "COHORT"]


def body_of(split: str) -> str:
    return {"DEV": "DEV", "COHORT": "COHORT"}.get(split, "OLD_HELDOUT")


def home_fields(h) -> list[int]:
    return [int(float(x)) for x in re.split(r"[|;]", str(h)) if x and x != "nan"]


def frame_plus(fr: pd.DataFrame) -> pd.DataFrame:
    fr = fr.copy()
    fr["body"] = fr.split.map(body_of)
    fr["home_list"] = fr.home.map(home_fields)
    fr["multi_home"] = (fr.intersect40 == 1).astype(int)
    fr["h_end"] = np.minimum(fr.t0 + 10, 2022)
    return fr


def open_home(df: pd.DataFrame, zc: dict) -> np.ndarray:
    Z = np.column_stack([SIGN[c] * (df[c].to_numpy(float) - zc[c]["mean"]) / zc[c]["sd"] for c in COMP])
    nn = np.isfinite(Z).sum(1)
    with np.errstate(invalid="ignore"):
        m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), axis=1)
    return np.where(nn >= 4, m, np.nan)


def closure_jumps(yf: pd.DataFrame, k_sd: float) -> pd.DataFrame:
    """Per concept: within-concept SD of density over t0..h_end (>= 5 defined years) and the FIRST closure jump
    t* = first t with age >= 2, deg(t) >= 3 and density(t) - density(t-1) >= k_sd x SD; also the list of years that
    would be eligible jump dates (used by the event-date permutation placebo)."""
    out = []
    for ci, d in yf.groupby("ci", sort=False):
        d = d.sort_values("year")
        dens = d.density.to_numpy(float)
        ok = np.isfinite(dens)
        if ok.sum() < 5:
            out.append((ci, np.nan, np.nan, 0, ""))
            continue
        sd = float(np.std(dens[ok], ddof=1))
        dd = np.r_[np.nan, np.diff(dens)]
        base = (d.age.to_numpy() >= 2) & np.isfinite(dd) & (d.deg.to_numpy() >= 3)
        cand = base & (dd >= k_sd * sd) & (sd > 0)
        ts = int(d.year.to_numpy()[np.argmax(cand)]) if cand.any() else np.nan
        elig = ",".join(str(int(y)) for y in d.year.to_numpy()[base])
        out.append((ci, sd, ts, 1, elig))
    return pd.DataFrame(out, columns=["ci", "dens_sd_w", "t_jump", "es_eligible", "eligible_years"])


def build_panel(yf_out: pd.DataFrame, fr: pd.DataFrame, zc: dict) -> pd.DataFrame:
    """yf_out = yearly features already joined (by the seal gate) with the D3 table at (ci, year).
    Adds t+1 outcomes, controls and flags. Rows: t0 <= t <= h_end - 1."""
    d = yf_out.merge(fr[["ci", "t0", "h_end", "body", "group", "split", "multi_home", "home_list"]], on="ci",
                     how="left")
    d = d.sort_values(["ci", "year"]).reset_index(drop=True)
    d["OPEN_home"] = open_home(d, zc)
    nxt = d[["ci", "year", "entries", "any_entry", "at_risk", "density", "deg", "n_home_works", "n_all_works",
             "cum_entries_prev", "dens_adj", "OPEN_home"]].copy()
    nxt["year"] = nxt["year"] - 1
    nxt = nxt.rename(columns={c: f"{c}_next" for c in nxt.columns if c not in ("ci", "year")})
    d = d.merge(nxt, on=["ci", "year"], how="left")
    d = d[d.year <= d.h_end - 1].copy()
    d["y_next"] = d.entries_next
    d["any_next"] = d.any_entry_next
    d["log1p_home"] = np.log1p(d.n_home_works)
    d["log1p_all"] = np.log1p(d.n_all_works)
    d["log1p_deg"] = np.log1p(d.deg)
    d["log_at_risk"] = np.log(d.at_risk_next.clip(lower=1))          # fields not yet entered by end of t
    d["log1p_home_next"] = np.log1p(d.n_home_works_next)
    d["log1p_all_next"] = np.log1p(d.n_all_works_next)
    d["log1p_deg_next"] = np.log1p(d.deg_next)
    d["log_at_risk_next"] = np.log(d.at_risk.clip(lower=1))           # for the reverse path: at risk entering t
    d["cum_entries_t"] = d.cum_entries_prev_next                      # entered by end of t (S2 lagged outcome)
    d["primary_home"] = d.home_list.map(lambda h: h[0] if len(h) else 0)
    d["home_year"] = d.primary_home * 10000 + d.year
    return d


def estimation_sample(d: pd.DataFrame) -> pd.DataFrame:
    return d[(d.at_risk_next > 0) & (d.deg >= 2) & d.y_next.notna()].copy()
