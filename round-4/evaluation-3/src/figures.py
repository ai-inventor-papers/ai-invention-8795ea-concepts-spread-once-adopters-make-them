#!/usr/bin/env python3
"""Part B figures (PNG + PDF): specification curve, OPEN forest (units + sub-units), B1 paired bars, LIFEENV panel.

Reads only results/*.json|csv written by partb_core.py, spec_curve.py and heterogeneity.py. Usage: python figures.py"""
from __future__ import annotations

import os as _os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    _os.environ[_v] = "1"

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from loguru import logger

from common import COMPONENTS, FIG, HELD4, LOGS, RES, UNITS6

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "figures.log", rotation="30 MB", level="DEBUG")
plt.rcParams.update({"font.size": 9, "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False,
                     "axes.spines.right": False})
BLUE, ORANGE, GREY, RED = "#2563a8", "#d97a1f", "#8a8a8a", "#b33a3a"


def save(fig, name: str) -> None:
    for ext in ("png", "pdf"):
        fig.savefig(FIG / f"{name}.{ext}", dpi=200, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"wrote figures/{name}.png|pdf")


def fig_spec_curve() -> None:
    S = pd.read_csv(RES / "spec_curve_specs.csv").sort_values("DL4_est").reset_index(drop=True)
    sc = json.loads((RES / "spec_curve.json").read_text())
    x = np.arange(len(S))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 7.2), sharex=True, gridspec_kw={"height_ratios": [2.2, 3]})
    sig = S.DL4_lo > 0
    a1.fill_between(x, S.DL4_lo, S.DL4_hi, color=BLUE, alpha=0.18, lw=0, label="95% CI (DL, analytic Fisher-z)")
    a1.scatter(x[sig], S.DL4_est[sig], s=2, color=BLUE, label="pooled psp, CI > 0")
    a1.scatter(x[~sig], S.DL4_est[~sig], s=4, color=RED, label="pooled psp, CI includes 0")
    hl = S[(S.composite == "EQ[" + "+".join(COMPONENTS) + "]") & (S.outcome == "O2r_m50") & (S.control == "C1")]
    if len(hl):
        a1.scatter(hl.index, hl.DL4_est, s=40, marker="D", color=ORANGE, zorder=5, label="headline (all 6, equal, O2r_m50, C1)")
    nq = sc["null"]["DL4"]
    a1.axhspan(nq["null_median_q05"], nq["null_median_q95"], color=GREY, alpha=0.35, label="Freedman-Lane null median, 5-95%")
    a1.axhline(0, color="k", lw=0.6)
    a1.set_ylabel("pooled psp (4 held-out groups)")
    s = sc["summary"]["DL4"]
    a1.set_title(f"OPEN specification curve: {len(S):,} specs; share CI>0 = {s['share_ci_gt0']:.3f}; median = "
                 f"{s['median']:.3f}; permutation p = {nq['p_share_ci_gt0']:.3f} ({nq['n_draws']} draws)", fontsize=9)
    a1.legend(fontsize=7, loc="upper left", frameon=False)
    rows = [(f"has_{c}", c) for c in COMPONENTS] + [("w_pc1", "PC1 weights")] + \
           [(f"o_{o}", o) for o in ["O2r_m30", "O2r_m50", "O2r_resid", "O2r_resid_N"]] + \
           [(f"c_{c}", c) for c in ["C0", "C1", "C2", "C3"]]
    S["w_pc1"] = (S.weights == "pc1").astype(int)
    for o in ["O2r_m30", "O2r_m50", "O2r_resid", "O2r_resid_N"]:
        S[f"o_{o}"] = (S.outcome == o).astype(int)
    for c in ["C0", "C1", "C2", "C3"]:
        S[f"c_{c}"] = (S.control == c).astype(int)
    for j, (col, lab) in enumerate(rows):
        m = S[col].to_numpy() == 1
        a2.scatter(x[m], np.full(m.sum(), j), s=0.6, color=BLUE if j < 7 else (ORANGE if j < 11 else "#4a7d4a"), marker="|")
    a2.set_yticks(range(len(rows)))
    a2.set_yticklabels([r[1] for r in rows], fontsize=7)
    a2.invert_yaxis()
    a2.set_xlabel("specification rank (by pooled psp)")
    fig.tight_layout()
    save(fig, "spec_curve")


def fig_forest() -> None:
    T = pd.read_csv(RES / "per_group_table.csv")
    P = pd.read_csv(RES / "per_group_pooled.csv")
    SU = pd.read_csv(RES / "subunit_table.csv").sort_values(["unit", "psp_OPEN"])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 6.5), gridspec_kw={"width_ratios": [1, 1.4]})
    for k, o in enumerate(["O2r_m50", "O2r_resid"]):
        t = T[(T.indicator == "OPEN") & (T.outcome == o)].set_index("unit").reindex(UNITS6)
        y = np.arange(len(UNITS6)) + k * 0.3
        a1.errorbar(t.rho, y, xerr=[t.rho - t.ci_lo, t.ci_hi - t.rho], fmt="o", ms=4, color=[BLUE, ORANGE][k], label=o, capsize=2)
        for tag, yy in (("DL4", -1.2), ("DL6", -2.2)):
            p = P[(P.indicator == "OPEN") & (P.outcome == o) & (P.pool == tag)].iloc[0]
            a1.errorbar([p.pooled], [yy + k * 0.3], xerr=[[p.pooled - p.ci_lo], [p.ci_hi - p.pooled]], fmt="D", ms=5,
                        color=[BLUE, ORANGE][k], capsize=2)
    a1.set_yticks(list(range(len(UNITS6))) + [-1.2, -2.2])
    a1.set_yticklabels(UNITS6 + ["pooled DL4", "pooled DL6"])
    a1.axvline(0, color="k", lw=0.6)
    a1.set_xlabel("psp | B5 + t0 (bootstrap 95% CI, B=1,000)")
    a1.set_title("OPEN per held-out unit", fontsize=9)
    a1.legend(fontsize=7, frameon=False)
    z = np.arctanh(SU.psp_OPEN.to_numpy())
    se = np.sqrt(SU.v_OPEN.to_numpy())
    y = np.arange(len(SU))
    cols = {u: c for u, c in zip(UNITS6, plt.cm.tab10.colors)}
    for i, r in enumerate(SU.itertuples()):
        a2.errorbar([r.psp_OPEN], [i], xerr=[[r.psp_OPEN - np.tanh(z[i] - 1.96 * se[i])], [np.tanh(z[i] + 1.96 * se[i]) - r.psp_OPEN]],
                    fmt="o", ms=3, color=cols[r.unit], capsize=1.5)
    a2.set_yticks(y)
    a2.set_yticklabels([f"{s} (n={n})" for s, n in zip(SU.subunit, SU.n_usable)], fontsize=6)
    a2.axvline(0, color="k", lw=0.6)
    H = json.loads((RES / "heterogeneity.json").read_text())
    a2.set_title(f"OPEN per home-field x period sub-unit (k={H['k_subunits']}; I2 sub-unit {H['I2_subunit']:.2f} vs "
                 f"unit {H['I2_unit6']:.2f})", fontsize=9)
    a2.set_xlabel("psp | B5 + t0 (analytic Fisher-z 95% CI), O2r_m50")
    fig.tight_layout()
    save(fig, "open_forest")


def fig_b1() -> None:
    R = json.loads((RES / "post_onset_rescore.json").read_text())
    C = pd.DataFrame(R["cells"])
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for ax, full in zip(axes, ["M0_density_end", "D_vol_end"]):
        c = C[(C.full == full) & (C.outcome == "O2r_m50")].set_index("unit").reindex(UNITS6)
        c = c.map(lambda v: [np.nan, np.nan] if isinstance(v, list) and None in v else v)
        x = np.arange(len(UNITS6))
        for off, col, lab, key in ((-0.18, BLUE, "full history (Exp8)", "full"), (0.18, ORANGE, "post-onset only (t0..t0+2)", "post")):
            est = c[f"est_{key}"].to_numpy()
            lo = np.array([v[0] for v in c[f"ci_{key}"]]); hi = np.array([v[1] for v in c[f"ci_{key}"]])
            ax.bar(x + off, est, width=0.36, color=col, alpha=0.85, label=lab)
            ax.errorbar(x + off, est, yerr=[est - lo, hi - est], fmt="none", color="k", lw=0.8, capsize=2)
        p = R["pooled"][f"DL4|{full}|O2r_m50"]
        exc = p.get("units_excluded_undefined_post") or []
        ax.set_title(f"{full}: pooled DL4{' excl. ' + ','.join(exc) if exc else ''} {p['psp_full']:.3f} -> {p['psp_post']:.3f} (atten. "
                     f"{p['attenuation']:.2f} [{p['attenuation_ci'][0]:.2f}, {p['attenuation_ci'][1]:.2f}]; {p['verdict']})", fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels(UNITS6, fontsize=7, rotation=20)
        ax.axhline(0, color="k", lw=0.6)
    axes[0].set_ylabel("psp with O2r_m50 | B5 + t0 (paired bootstrap 95% CI)")
    axes[0].legend(fontsize=7, frameon=False)
    fig.tight_layout()
    save(fig, "b1_post_onset")


def fig_lifeenv() -> None:
    H = json.loads((RES / "heterogeneity.json").read_text())
    L = H["lifeenv"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    names = ["OPEN"] + COMPONENTS
    r = [L["sd_ratio"][k]["ratio"] for k in names]
    lo = [L["sd_ratio"][k]["ci"][0] for k in names]
    hi = [L["sd_ratio"][k]["ci"][1] for k in names]
    y = np.arange(len(names))
    a1.errorbar(r, y, xerr=[np.subtract(r, lo), np.subtract(hi, r)], fmt="o", color=BLUE, capsize=2)
    a1.axvline(1, color="k", lw=0.6)
    a1.set_yticks(y)
    a1.set_yticklabels(names, fontsize=7)
    a1.set_xlabel("SD ratio LIFEENV / other held-out units (bootstrap 95% CI)")
    a1.set_title("(i) variance restriction", fontsize=9)
    T = L["tercile_psp"]
    ks = list(T.keys())
    est = [T[k]["rho"] for k in ks]
    a2.errorbar(range(len(ks)), est, yerr=[np.subtract(est, [T[k]["ci"][0] for k in ks]), np.subtract([T[k]["ci"][1] for k in ks], est)],
                fmt="o", color=ORANGE, capsize=2, label="LIFEENV by DEV coverage tercile")
    o = L["others_pooled_6minusL"]
    a2.axhspan(o["ci"][0], o["ci"][1], color=GREY, alpha=0.3, label=f"other 5 units pooled {o['est']:.3f}")
    eb = L["entropy_balanced"]
    a2.errorbar([len(ks)], [eb["psp_reweighted"]], yerr=[[eb["psp_reweighted"] - eb["ci"][0]], [eb["ci"][1] - eb["psp_reweighted"]]],
                fmt="D", color=RED, capsize=2, label="LIFEENV entropy-balanced to others' coverage")
    a2.set_xticks(range(len(ks) + 1))
    a2.set_xticklabels([f"{k} (n={T[k]['n']})" for k in ks] + ["reweighted"], fontsize=7)
    a2.axhline(0, color="k", lw=0.6)
    a2.set_ylabel("psp OPEN x O2r_m50")
    a2.set_title(f"(ii) label coverage; verdict: {L['verdict']}", fontsize=9)
    a2.legend(fontsize=6.5, frameon=False, loc="upper left")
    fig.tight_layout()
    save(fig, "lifeenv_diagnosis")


def main() -> None:
    fig_spec_curve()
    fig_forest()
    fig_b1()
    fig_lifeenv()


if __name__ == "__main__":
    logger.catch(reraise=True)(main)()
