#!/usr/bin/env python3
"""Render the README result tables straight from results/*.json (no hand transcription) -> results/readme_tables.md,
then assemble README.md from README_template.md by replacing {{TABLES}}."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from common import RES, ROOT

R = json.loads((RES / "frame_n_result.json").read_text())
C = R["cells"]
P = R["primary_outcome"]
RUNGS = ["R0", "R1", "R2", "R3", "R4", "R5"]


def ci(c: dict, key: str = "rho") -> str:
    v = c.get(key)
    if v is None:
        return "NA"
    lo, hi = c["ci"]
    return f"{v:+.3f} [{lo:+.3f}, {hi:+.3f}]"


def main() -> None:
    out = []
    out.append(f"### Ladder: partial Spearman with later breadth (95% concept-bootstrap CI, B = {R['B']})\n")
    out.append("| index | outcome | " + " | ".join(RUNGS) + " | n (R3) |")
    out.append("|---|---|" + "---|" * len(RUNGS) + "---|")
    for x in ("OPEN_home", "NOVCHURN_home", "OPEN_sizematch", "OPEN_all"):
        for y in (P, "O2r_m50", "O2r_resid"):
            out.append(f"| {x} | {y} | " + " | ".join(ci(C[f"ladder|{x}|{y}|{r}"]) for r in RUNGS)
                       + f" | {C[f'ladder|{x}|{y}|R3']['n']} |")
    out.append("\n### Holm family (one-sided bootstrap p in the frozen direction)\n")
    out.append("| member | p (one-sided) | Holm p |")
    out.append("|---|---|---|")
    for k, v in R["holm"].items():
        out.append(f"| {k} | {v['p_one']:.4f} | {v['p_holm']:.4f} |")
    out.append(f"\n### Per group at R3 ({P}) with DerSimonian-Laird pooling (groups estimable at n >= 30)\n")
    out.append("| index | CS+Eng | BGM+Med | PHYS | LIFEENV | SOC | MATHDEC | DL pooled [95% CI] | I2 | positive / estimable | leave-one-group-out DL |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for x in ("OPEN_home", "NOVCHURN_home", "OPEN_sizematch", "OPEN_all"):
        g = C[f"groups|{x}|{P}|R3"]
        cells = []
        for k in ("CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC", "MATHDEC"):
            c = g["groups"][k]
            cells.append(f"{c['rho']:+.3f} (n={c['n']})" if c["rho"] is not None else f"NA (n={c['n']})")
        dl = g["DL"]
        logo = ", ".join(f"-{k}: {v['b']:+.3f}" for k, v in g["leave_one_group_out"].items())
        out.append(f"| {x} | " + " | ".join(cells) + f" | {dl['b']:+.3f} [{dl['ci'][0]:+.3f}, {dl['ci'][1]:+.3f}] | "
                   f"{dl['I2']:.2f} | {g['n_positive']}/{g['n_estimable']} | {logo} |")
    out.append(f"\n### The six OPEN components alone ({P})\n")
    out.append("| component (OPEN sign) | HOME R2 | HOME R3 | ALL R2 | ALL R3 |")
    out.append("|---|---|---|---|---|")
    sg = {"new_edge_rate": "+", "n_comm_W3": "+", "participation": "+", "NOV_res": "+", "ego_density_W3": "-",
          "edge_persistence": "-"}
    for k, s in sg.items():
        out.append(f"| {k} ({s}) | " + " | ".join(ci(C[f"comp|{k}__{b}|{P}|{r}"]) for b in ("home", "all")
                                                   for r in ("R2", "R3")) + " |")
    out.append("\n### Coupling contrasts (paired concept bootstrap, R3)\n")
    out.append("| contrast | estimate [95% CI] | n |")
    out.append("|---|---|---|")
    for k in ("all_minus_home", "sizematch_minus_home"):
        c = C[f"coupling|{k}|R3"]
        out.append(f"| {k} | {ci(c, 'diff')} | {c['n']} |")
    c = C["coupling|OPEN_all_on_home_sample|R3"]
    out.append(f"| OPEN_all on the OPEN_home sample (psp) | {ci(c)} | {c['n']} |")
    out.append("\n### Cheng et al. (2023) measures (home papers, OpenAlex topics as terms)\n")
    out.append(f"| measure | V_next raw Spearman | V_next given log N(t0+2) | V_next given R0 | {P} given R0 | O2r_resid given R0 | O1b given R0 | O1c given R0 | O3 given R0 |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for m in ("CHENG_consistency_home", "CHENG_consistency_all", "CHENG_embeddedness_home", "CHENG_prominence_home"):
        out.append(f"| {m} | {ci(C[f'cheng|{m}|V_next|raw'])} | {ci(C[f'cheng|{m}|V_next|logN2'])} | "
                   f"{ci(C[f'cheng|{m}|V_next|R0'])} | {ci(C[f'cheng|{m}|{P}|R0'])} | "
                   f"{ci(C[f'cheng|{m}|O2r_resid|R0'])} | {ci(C[f'cheng|{m}|O1b|R0'])} | "
                   f"{ci(C[f'cheng|{m}|O1c|R0'])} | {ci(C[f'cheng|{m}|O3|R0'])} |")
    c = C["cheng|consistency_vs_persistence"]
    out.append(f"\nSpearman(CHENG_consistency_home, edge_persistence_home) = {ci(c)} (n = {c['n']}); "
               f"Spearman(CHENG_consistency_home, logvol) = {ci(C['cheng|consistency_vs_logvol'])}.")
    out.append(f"\n### Clean variants and secondary indicators ({P})\n")
    out.append("| indicator | rung | psp [95% CI] | n |")
    out.append("|---|---|---|---|")
    for k in C:
        if k.startswith("clean|"):
            _, x, y, r = k.split("|")
            out.append(f"| {x} | {r} | {ci(C[k])} | {C[k]['n']} |")
    for k in C:
        if k.startswith("secondary|"):
            _, x, y, r = k.split("|")
            out.append(f"| {x} -> {y} | {r} | {ci(C[k])} | {C[k]['n']} |")
    out.append("\n### Palla et al. (2007) size x turnover interaction (R3 covariates)\n")
    out.append("| outcome | model | coefficient of z(logvol) x z(edge_persistence_home) [95% CI] | n |")
    out.append("|---|---|---|---|")
    for y in (P, "O3", "O1b"):
        c = C[f"palla|{y}"]
        out.append(f"| {y} | {c['model']} | {ci(c, 'coef')} | {c['n']} |")
    c = C["palla_psp|edge_persistence__home|O3|R3"]
    out.append(f"| O3 (psp of edge_persistence_home at R3) | partial Spearman | {ci(c)} | {c['n']} |")
    out.append("\n### Within concept type (R3 without type dummies; M1 = M2 labels only)\n")
    out.append("| index | method | object |")
    out.append("|---|---|---|")
    for x in ("OPEN_home", "NOVCHURN_home", "OPEN_sizematch", "OPEN_all"):
        a, b = C[f"type|{x}|method|R3"], C[f"type|{x}|object|R3"]
        out.append(f"| {x} | {ci(a)} n={a['n']} | {ci(b)} n={b['n']} |")
    f = R["forecast_cv"]
    out.append(f"\n### Forecasting (5-fold CV, folds stratified by group; n = {f['n']}; outcome {P})\n")
    out.append("| model | Spearman | AUC top tercile | delta Spearman vs B5 [95% CI] | delta AUC vs B5 [95% CI] |")
    out.append("|---|---|---|---|---|")
    for k, v in f["models"].items():
        ds = f"{v['d_spearman_vs_B5']:+.4f} [{v['d_spearman_ci'][0]:+.4f}, {v['d_spearman_ci'][1]:+.4f}]" if "d_spearman_vs_B5" in v else "-"
        da = f"{v['d_auc_vs_B5']:+.4f} [{v['d_auc_ci'][0]:+.4f}, {v['d_auc_ci'][1]:+.4f}]" if "d_auc_vs_B5" in v else "-"
        out.append(f"| {k} | {v['spearman']:.3f} | {v['auc_top_tercile']:.3f} | {ds} | {da} |")
    fz = R["forecast_frozen_exp5"]
    out.append(f"| frozen EXP5 OLS: B5 vs B5 + OPEN_home (no refit) | {fz['spearman_B5']:.3f} -> "
               f"{fz['spearman_B5_plus_OPEN_home']:.3f} | - | {fz['diff']:+.4f} [{fz['diff_ci'][0]:+.4f}, "
               f"{fz['diff_ci'][1]:+.4f}] | - |")
    pp = R["placebo_planted"]
    pl, pt = pp["placebo_within_group_shuffle_OPEN_home"], pp["planted_0.10"]
    out.append("\n### Placebo and planted effect (OPEN_home, R3)\n")
    out.append(f"* within-group shuffle of OPEN_home, {pl['n_perm']} draws: mean psp {pl['mean']:+.3f}, "
               f"95th percentile of |psp| = {pl['q95_abs']:.3f} (observed {C[f'ladder|OPEN_home|{P}|R3']['rho']:+.3f}).")
    out.append(f"* planted psp 0.10 on within-group-permuted outcomes, {pt['n_draws']} draws x {pt['n_boot_per_draw']} "
               f"bootstraps: mean estimate {pt['mean_estimate']:+.3f}, recovery rate (CI_low > 0) "
               f"{pt['recovery_rate_ci_low_gt0']:.2f}.")
    s = R["survivorship"]
    out.append("\n### Survivorship: Frame N vs legacy (curated-vocabulary) newborns, t0 2003-2014\n")
    out.append("| measure | Frame N | legacy raw | legacy reweighted to Frame N (t0 x logvol decile) | relative difference [95% CI] | flag > 25% |")
    out.append("|---|---|---|---|---|---|")
    for k, v in s["measures"].items():
        out.append(f"| {k} | {v['frame_n_mean']:.3f} | {v['legacy_raw_mean']:.3f} | {v['legacy_reweighted_mean']:.3f} | "
                   f"{v['rel_diff_vs_reweighted']:+.1%} [{v['rel_diff_ci'][0]:+.1%}, {v['rel_diff_ci'][1]:+.1%}] | "
                   f"{'FLAG' if v['FLAG_gt_25pct'] else ''} |")
    ex = json.loads((RES / "exploratory.json").read_text())
    out.append("\n### EXPLORATORY (post-unseal; not part of the verdict)\n")
    out.append("| subset | index | outcome | R3 | R5 | n |")
    out.append("|---|---|---|---|---|---|")
    for name in ("strict_gate_M2_also_keeps", "main_frame_only_t0_le_2014"):
        for x in ("OPEN_home", "NOVCHURN_home"):
            for y in (P, "O2r_m50"):
                a, b = ex[f"{name}|{x}|{y}|R3"], ex[f"{name}|{x}|{y}|R5"]
                out.append(f"| {name} | {x} | {y} | {ci(a)} | {ci(b)} | {a['n']} |")
    for x in ("OPEN_home", "NOVCHURN_home"):
        a, b = ex[f"min_home_20|{x}|{P}|R3"], ex[f"min_home_20|{x}|{P}|R5"]
        out.append(f"| min_home_20 | {x} | {P} | {ci(a)} | {ci(b)} | {a['n']} |")
    out.append("\nInverse-variance pooling with the independent EXP10 legacy cohort (OPEN_home; EXP10 used O2r_m50 and its "
               "legacy rungs):\n")
    out.append("| rung | Frame N | EXP10 cohort | pooled fixed-effect [95% CI] |")
    out.append("|---|---|---|---|")
    for r, v in R["exploratory_pooled_with_exp10"].items():
        out.append(f"| {r} | {v['frame_n']:+.3f} | {v['exp10_cohort']:+.3f} | {v['pooled_fixed']:+.3f} "
                   f"[{v['pooled_ci'][0]:+.3f}, {v['pooled_ci'][1]:+.3f}] |")
    md = "\n".join(out) + "\n"
    (RES / "readme_tables.md").write_text(md)
    tpl = (ROOT / "README_template.md").read_text()
    (ROOT / "README.md").write_text(tpl.replace("{{TABLES}}", md))
    print("README.md written")


if __name__ == "__main__":
    main()
