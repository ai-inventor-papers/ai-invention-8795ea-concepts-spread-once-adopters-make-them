#!/usr/bin/env python3
"""WP3: agreement between the Exp5 (art_wxWssKSUR45f, TAG grounding, 12,499 concepts) and Exp6 (art_N-mpomDZZ1ln,
tag-AND-title grounding, 653 newborn concepts) frames on their shared concepts, disagreement attribution, the
pre-declared pooling rule and the Exp5-minus-Exp6 counts the confirmation experiment needs."""
from __future__ import annotations

import math
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from loguru import logger

import common as C

# pre-declared (artifact plan, WP3) BEFORE any agreement was computed
POOL_RULE = {"onset_pm1_agree_min": 0.80, "home_kappa_min": 0.60, "o2r_m50_spearman_min": 0.70,
             "retention_kappa_min": 0.40, "n_both_min": 50}
G5 = {"CS": "CS", "Eng": "Eng", "BGM": "BGM", "Med": "Med", "PHYS": "PHYS", "LIFEENV": "LIFEENV", "SOC": "SOC",
      "MATHDEC": "MATHDEC"}
G6 = {"DEV_CS": "CS", "DEV_Eng": "Eng", "DEV_BGM": "BGM", "DEV_Med": "Med", "Physical": "PHYS", "LifeEnv": "LIFEENV",
      "Social": "SOC", "MathDec": "MATHDEC", "OtherHealth": "OTHERHEALTH"}
S5 = {"DEV": "dev", "COHORT": "heldout_cohort"}

DEFS = [
    ("grounding_rule", "TAG: title match AND legacy tag score >= 0.3 (+ Wikidata aliases, stemmed verification)",
     "round-2/experiment-5/src/README.md:121,127",
     "legacy tag (score >= 0.3) AND title match, plus untagged works scaled by p_notag",
     "iter_2/gen_art/gen_art_experiment_6/README.md:73; frame.py:55"),
    ("lexicon_aliases", "56,643 legacy concepts + 85,692 Wikidata alias forms (SPARQL)",
     "round-2/experiment-5/src/README.md:103-111", "display names and plural variants only; no Wikidata aliases",
     "round-2/experiment-6/src/README.md:105"),
    ("concept_universe", "all onset candidates passing the precision gate (newborn 5.4%)",
     "round-2/experiment-5/src/README.md:140", "newborn_prelim candidates only (653 newborn)",
     "iter_2/gen_art/gen_art_experiment_6/frame.py:47; README.md:67,106"),
    ("onset_rule", "t0 = first year 2000-2014 with >= 20 grounded works; keep 2003-2014",
     "iter_2/gen_art/gen_art_experiment_5/panel.py:68-76; frame.py:9", "iteration-1 rule: first year with >= 20 grounded works, t0 in 2003-2014",
     "iter_2/gen_art/gen_art_experiment_6/README.md:65-66; frame.py:62"),
    ("newborn_rule", "each of t0-3..t0-1 < 0.25 x count(t0+2)", "round-2/experiment-5/src/panel.py:75",
     "onset() newborn flag on the tag-AND-title counts (same iteration-1 rule)", "round-2/experiment-6/src/frame.py:62"),
    ("early_window_volume", "early_volume = grounded works t0..t0+2 (>= 30)", "round-2/experiment-5/src/frame.py:10",
     "n_early = grounded works t0..t0+2 (>= 30)", "round-2/experiment-6/src/frame.py:67-68"),
    ("home_rule", "fields with >= 40% of the first 30 venue-labelled grounded works from t0 (weak >= 25%)",
     "round-2/experiment-5/src/frame.py:10-11,96", "same 40% rule on first 30 labelled works (last year proportional); home_primary = top share",
     "round-2/experiment-6/src/frame.py:70-82"),
    ("episode_inclusion", "off-home field with n_early >= 2 grounded labelled works (t0..t0+2)",
     "iter_2/gen_art/gen_art_experiment_5/README.md:134; frozen_spec.json episode_rule", "off-home field with >= 2 works in t0..t0+2 (EPISODE_MIN = 2)",
     "iter_2/gen_art/gen_art_experiment_6/frame.py:104-107; config.py:25"),
    ("retention_outcome", "R = share_out >= 0.5 x share_early AND n_out >= 9 over t0+6..t0+8 (R_abs1-3 = n_out >= 1/2/3)",
     "round-2/experiment-5/src/frame.py:13,141-143", "R_cj = >= 2 works in field j over t0+6..t0+8 (absolute)",
     "round-2/experiment-6/src/frame.py:36-37"),
    ("O2r_labelling", "O2r_m30/m50 rarefied venue-field richness t0+6..t0+8 (iteration-1 definition)",
     "iter_2/gen_art/gen_art_experiment_5/frame.py (concept_outcomes)", "same iteration-1 definition; O2r_resid on log n_early fitted on dev",
     "iter_2/gen_art/gen_art_experiment_6/README.md:80; frame.py:120-123"),
    ("group_mapping", "common.GROUP_OF_FIELD -> PHYS/LIFEENV/SOC/MATHDEC (+ CS/Eng/BGM/Med)", "iter_2/gen_art/gen_art_experiment_5/frozen_spec.json group_map",
     "config.py field groups incl. OtherHealth [29,34,35,36]", "round-2/experiment-6/src/config.py:21"),
    ("split_rule", "DEV = CS/Eng/BGM/Med homes t0 2003-09; HELDOUT_* other homes 2003-09; COHORT 2010-14",
     "round-2/experiment-5/src/README.md:18-19", "dev = DEV_HOME primary with t0 <= 2009; heldout_field otherwise; heldout_cohort 2010-14",
     "round-2/experiment-6/src/frame.py:84-88"),
]


def first_home(h) -> int:
    s = str(h).replace("|", ";")
    return int(float(s.split(";")[0]))


def home_set(h) -> set:
    return {int(float(x)) for x in str(h).replace("|", ";").split(";") if x not in ("", "nan")}


def boot(fn, n: int, B: int, rng) -> list[float]:
    vals = []
    for _ in range(B):
        vals.append(fn(rng.integers(0, n, n)))
    return C.pct_ci(vals)


@logger.catch(reraise=True)
def main() -> None:
    C.setup_logging("wp3")
    rng = np.random.default_rng(C.SEED)
    B = C.B_MAIN
    f5 = C.read_csv(C.E5 / "frame_concepts.csv")
    f6 = C.read_csv(C.E6 / "results/frame_concepts.csv")
    o5 = C.read_csv(C.E5 / "concept_outcomes.csv")
    e5 = C.read_csv(C.E5 / "episodes.csv")
    e6 = C.read_csv(C.E6 / "results/episodes.csv")
    f5["id"] = f5.concept_id.map(C.norm_id)
    f6["id"] = f6.concept_id.map(C.norm_id)
    assert f5.id.is_unique and f6.id.is_unique
    assert all(C.norm_id(x) == x for x in f6.id)
    f5 = f5.merge(o5[["ci", "O1", "O3", "N_outcome", "O2r_m30", "O2r_m50"]], on="ci", how="left")
    fields5 = {first_home(h) for h in f5.home} | set(e5.field)
    fields6 = set(f6.home_primary.astype(int)) | set(e6.field)
    assert fields5 <= set(range(11, 37)) and fields6 <= set(range(11, 37)), "field codes outside the 26 OpenAlex fields"
    f5["g"] = f5.group.map(G5)
    f6["g"] = f6.group.map(G6)
    f5["split_c"] = f5.split.map(lambda s: S5.get(s, "heldout_field"))
    ids5, ids6 = set(f5.id), set(f6.id)
    both = sorted(ids5 & ids6)
    n_both = len(both)
    logger.info(f"n_exp5={len(ids5)} n_exp6={len(ids6)} n_both={n_both}")
    A = f5.set_index("id").loc[both]
    Bf = f6.set_index("id").loc[both]
    res: dict = {"n_exp5": len(ids5), "n_exp6": len(ids6), "n_both": n_both, "n_exp6_only": len(ids6 - ids5),
                 "share_exp6_in_exp5": n_both / len(ids6), "pooling_rule_predeclared": POOL_RULE,
                 "id_normaliser": "Exp5 int -> 'C'+int; Exp6 URL -> last path segment; idempotence asserted"}
    # cross-tab of split/group
    ct = pd.crosstab(A.split + "/" + A.group.astype(str), Bf.split + "/" + Bf.group.astype(str))
    ct.to_csv(C.TAB / "frame_crosstab_split_group.csv")
    res["crosstab_file"] = "record_tables/frame_crosstab_split_group.csv"
    # Exp5 minus Exp6 counts per Exp5 held-out group and cohort
    rows = []
    e5c = e5.merge(f5[["ci", "id"]], on="ci")
    for sp in ["HELDOUT_PHYS", "HELDOUT_LIFEENV", "HELDOUT_SOC", "HELDOUT_MATHDEC", "COHORT", "DEV"]:
        m = f5.split == sp
        rem = f5[m & f5.id.isin(ids6)]
        left = f5[m & ~f5.id.isin(ids6)]
        ep = e5c[e5c.ci.isin(left.ci)]
        rows.append({"exp5_split": sp, "n_concepts_exp5": int(m.sum()), "n_removed_in_exp6": len(rem),
                     "n_left_exp5_minus_exp6": len(left), "n_episodes_left": len(ep),
                     "n_newborn_left": int(left.newborn.sum()), "R_rate_left": float(ep.R.mean()) if len(ep) else math.nan,
                     "source_file": "iter_2/gen_art/gen_art_experiment_5/frame_concepts.csv + iter_2/gen_art/gen_art_experiment_6/results/frame_concepts.csv",
                     "key_path": "split==sp; concept_id normalised; set difference"})
    pd.DataFrame(rows).to_csv(C.TAB / "frame_overlap_by_group.csv", index=False)
    res["exp5_minus_exp6"] = rows
    # ---------------- concept-level agreement
    n = n_both
    t5, t6 = A.t0.to_numpy(float), Bf.t0.to_numpy(float)
    d = t6 - t5
    agr = {}
    agr["onset_exact"] = {"value": float((d == 0).mean()), "ci95": boot(lambda i: (d[i] == 0).mean(), n, B, rng), "n": n}
    agr["onset_pm1"] = {"value": float((abs(d) <= 1).mean()), "ci95": boot(lambda i: (abs(d[i]) <= 1).mean(), n, B, rng), "n": n}
    sdd = d.std(ddof=1)
    agr["onset_bland_altman"] = {"mean_diff_exp6_minus_exp5": float(d.mean()), "sd_diff": float(sdd),
                                 "loa95": [float(d.mean() - 1.96 * sdd), float(d.mean() + 1.96 * sdd)],
                                 "mean_diff_ci95": boot(lambda i: d[i].mean(), n, B, rng),
                                 "diff_table": {str(int(k)): int(v) for k, v in pd.Series(d).value_counts().sort_index().items()}}
    nb5, nb6 = A.newborn.astype(bool).to_numpy(), Bf.newborn.astype(bool).to_numpy()
    agr["newborn_kappa"] = {"value": C.cohen_kappa(nb5, nb6), "pct_agree": float((nb5 == nb6).mean()),
                            "exp5_share_newborn": float(nb5.mean()), "exp6_share_newborn": float(nb6.mean()),
                            "ci95": boot(lambda i: C.cohen_kappa(nb5[i], nb6[i]), n, B, rng), "n": n}
    h5 = np.array([first_home(h) for h in A.home])
    h6 = Bf.home_primary.astype(int).to_numpy()
    hs5 = [home_set(h) for h in A.home]
    hs6 = [home_set(h) for h in Bf.home]
    set_agree = np.array([bool(a & b) for a, b in zip(hs5, hs6)])
    labs = list(range(11, 37))
    agr["home_kappa_26"] = {"value": C.cohen_kappa(h5, h6, labs), "pct_agree": float((h5 == h6).mean()),
                            "ci95": boot(lambda i: C.cohen_kappa(h5[i], h6[i], labs), n, B, rng), "n": n,
                            "home_set_overlap_share": float(set_agree.mean()),
                            "note": "Exp5 primary = first listed home code; Exp6 home_primary; set overlap counts any shared home field"}
    g5, g6 = A.g.to_numpy(), Bf.g.to_numpy()
    agr["group_agreement"] = {"pct_agree": float((g5 == g6).mean()), "kappa": C.cohen_kappa(g5, g6), "n": n}
    lv5, lv6 = np.log(A.early_volume.to_numpy(float)), np.log(Bf.n_early.to_numpy(float))
    agr["early_volume_log"] = {"spearman": C.spearman(lv5, lv6), "lin_ccc": C.lin_ccc(lv5, lv6),
                               "spearman_ci95": boot(lambda i: C.spearman(lv5[i], lv6[i]), n, B, rng),
                               "ccc_ci95": boot(lambda i: C.lin_ccc(lv5[i], lv6[i]), n, B, rng),
                               "median_ratio_exp5_over_exp6": float(np.median(np.exp(lv5 - lv6))),
                               "window_note": "both frames: grounded works t0..t0+2 (same window, own t0 and own grounding); CCC valid as absolute agreement only where t0 agrees"}
    same_t0 = d == 0
    agr["early_volume_log_same_t0"] = {"n": int(same_t0.sum()), "spearman": C.spearman(lv5[same_t0], lv6[same_t0]),
                                       "lin_ccc": C.lin_ccc(lv5[same_t0], lv6[same_t0])}
    lc5, lc6 = A.label_coverage_early.to_numpy(float), Bf.label_coverage_early.to_numpy(float)
    agr["label_coverage_early"] = {"spearman": C.spearman(lc5, lc6), "ci95": boot(lambda i: C.spearman(lc5[i], lc6[i]), n, B, rng), "n": n}
    for o in ("O1", "O3"):
        a_, b_ = A[o].to_numpy(float), Bf[o].to_numpy(float)
        ok = np.isfinite(a_) & np.isfinite(b_)
        aa, bb = a_[ok].astype(int), b_[ok].astype(int)
        agr[f"{o}_kappa"] = {"value": C.cohen_kappa(aa, bb), "pct_agree": float((aa == bb).mean()), "n": int(ok.sum()),
                             "base_rate_exp5": float(aa.mean()), "base_rate_exp6": float(bb.mean()),
                             "ci95": boot(lambda i: C.cohen_kappa(aa[i], bb[i]), int(ok.sum()), B, rng)}
    for o in ("O2r_m30", "O2r_m50"):
        a_, b_ = A[o].to_numpy(float), Bf[o].to_numpy(float)
        ok = np.isfinite(a_) & np.isfinite(b_)
        aa, bb = a_[ok], b_[ok]
        m = int(ok.sum())
        agr[o] = {"spearman": C.spearman(aa, bb), "lin_ccc": C.lin_ccc(aa, bb), "n": m,
                  "spearman_ci95": boot(lambda i: C.spearman(aa[i], bb[i]), m, B, rng),
                  "ccc_ci95": boot(lambda i: C.lin_ccc(aa[i], bb[i]), m, B, rng),
                  "mean_diff_exp6_minus_exp5": float((bb - aa).mean())}
    sp5, sp6 = A.split_c.to_numpy(), Bf.split.to_numpy()
    agr["split_agreement"] = {"pct_agree": float((sp5 == sp6).mean()), "n": n}
    # ---------------- episodes
    e5b = e5c[e5c.id.isin(both)]
    e6b = e6.merge(f6[["cidx", "id"]], on="cidx")
    e6b = e6b[e6b.id.isin(both)]
    s5 = e5b.groupby("id").field.apply(set).to_dict()
    s6 = e6b.groupby("id").field.apply(set).to_dict()
    jac, inter_n, union_n = [], 0, 0
    for c in both:
        a_, b_ = s5.get(c, set()), s6.get(c, set())
        u = a_ | b_
        inter_n += len(a_ & b_)
        union_n += len(u)
        jac.append(len(a_ & b_) / len(u) if u else math.nan)
    jac = np.array(jac)
    jf = jac[np.isfinite(jac)]
    agr["episode_jaccard"] = {"median": float(np.median(jf)), "iqr": [float(np.percentile(jf, 25)), float(np.percentile(jf, 75))],
                              "mean": float(jf.mean()), "pooled": inter_n / union_n if union_n else math.nan,
                              "share_ge_0.5": float((jf >= 0.5).mean()), "n_concepts": int(len(jf)),
                              "n_concepts_no_episodes_either": int(np.isnan(jac).sum()),
                              "median_ci95": boot(lambda i: float(np.nanmedian(jac[i])), n, B, rng),
                              "n_episodes_exp5_shared_concepts": int(len(e5b)), "n_episodes_exp6_shared_concepts": int(len(e6b))}
    pairs = e5b.merge(e6b[["id", "field", "R_cj", "n_early_j"]], on=["id", "field"], how="inner")
    pairs = pairs[pairs.R.notna() & pairs.R_cj.notna()]
    cid = pairs.id.to_numpy()
    uc = np.unique(cid)
    rows_of = {c: np.where(cid == c)[0] for c in uc}
    r5 = pairs.R.to_numpy(int)
    r6 = pairs.R_cj.to_numpy(int)

    def kboot(x, y):
        vals = []
        for _ in range(B):
            pick = rng.choice(uc, len(uc))
            ii = np.concatenate([rows_of[c] for c in pick])
            vals.append(C.cohen_kappa(x[ii], y[ii], [0, 1]))
        return C.pct_ci(vals)

    ret = {"n_pairs": int(len(pairs)), "n_concepts": int(len(uc)), "R_rate_exp5": float(r5.mean()), "R_rate_exp6": float(r6.mean()),
           "kappa_R_vs_Rcj": C.cohen_kappa(r5, r6, [0, 1]), "pct_agree": float((r5 == r6).mean()), "ci95": kboot(r5, r6)}
    for k in ("R_abs1", "R_abs2", "R_abs3"):
        x = pairs[k].to_numpy(int)
        ret[f"kappa_{k}_vs_Rcj"] = C.cohen_kappa(x, r6, [0, 1])
        ret[f"pct_agree_{k}"] = float((x == r6).mean())
    ret["ci95_R_abs2"] = kboot(pairs.R_abs2.to_numpy(int), r6)
    ret["crosstab_R_vs_Rcj"] = {f"exp5R={a}_exp6R={b}": int(((r5 == a) & (r6 == b)).sum()) for a in (0, 1) for b in (0, 1)}
    ret["early_count_spearman_shared_pairs"] = C.spearman(pairs.n_early.to_numpy(float), pairs.n_early_j.to_numpy(float))
    agr["retention"] = ret
    res["agreement"] = agr
    # ---------------- disagreement attribution (deterministic, rules applied in order)
    ratio = np.exp(lv5 - lv6)
    grounding_off = (ratio < 0.5) | (ratio > 2)
    cause_rows = []
    for k, c in enumerate(both):
        onset_dis = d[k] != 0
        home_dis = h5[k] != h6[k]
        if onset_dis:
            cause = "GROUNDING" if grounding_off[k] else "ONSET_RULE"
            cause_rows.append({"id": c, "type": "onset", "cause": cause})
        if home_dis:
            if onset_dis:
                cause = "ONSET_RULE" if not grounding_off[k] else "GROUNDING"
            else:
                cause = "GROUNDING" if grounding_off[k] else "HOME_RULE"
            cause_rows.append({"id": c, "type": "home", "cause": cause})
        a_, b_ = s5.get(c, set()), s6.get(c, set())
        hs = hs5[k] | hs6[k]
        n5map = e5b[e5b.id == c].set_index("field").n_early.to_dict() if (a_ ^ b_) else {}
        n6map = e6b[e6b.id == c].set_index("field").n_early_j.to_dict() if (a_ ^ b_) else {}
        for fld in a_ ^ b_:
            cnt = n5map.get(fld, n6map.get(fld, math.nan))
            if onset_dis:
                cause = "ONSET_RULE"
            elif fld in hs:
                cause = "HOME_RULE"
            elif np.isfinite(cnt) and cnt <= 3:
                cause = "EPISODE_THRESHOLD"
            elif grounding_off[k]:
                cause = "GROUNDING"
            else:
                cause = "UNEXPLAINED"
            cause_rows.append({"id": c, "type": "episode_set", "cause": cause})
    pr = pairs.assign(dis=r5 != r6)
    t0d = dict(zip(both, d))
    for _, r in pr[pr.dis].iterrows():
        if r.R_abs2 == r.R_cj:
            cause = "RETENTION_WINDOW"  # definition (relative share + n_out>=9) vs absolute >=2; R_abs2 matches Exp6
        elif t0d[r.id] != 0:
            cause = "ONSET_RULE"
        elif grounding_off[both.index(r.id)]:
            cause = "GROUNDING"
        else:
            cause = "UNEXPLAINED"
        cause_rows.append({"id": r.id, "type": "retention", "cause": cause})
    cdf = pd.DataFrame(cause_rows)
    cdf.to_csv(C.TAB / "frame_disagreement_causes.csv", index=False)
    res["disagreement_attribution"] = {
        "rules_in_order": ["GROUNDING: early-volume ratio Exp5/Exp6 outside [0.5, 2] (count in year t0 is not stored; early t0..t0+2 volume used)",
                           "ONSET_RULE: counts agree but t0 differs", "HOME_RULE: t0 agrees, home differs (or episode field is a home field in one frame)",
                           "EPISODE_THRESHOLD: field present in one frame with <= 3 early works (next to the shared >= 2 threshold)",
                           "RETENTION_WINDOW: shared episode, R differs but Exp5 R_abs2 equals Exp6 R_cj (definition difference)",
                           "UNEXPLAINED otherwise"],
        "share_by_type": {t: g.cause.value_counts(normalize=True).round(4).to_dict() for t, g in cdf.groupby("type")} if len(cdf) else {},
        "count_by_type": {t: int(len(g)) for t, g in cdf.groupby("type")} if len(cdf) else {},
        "grounding_ratio_outside_share": float(grounding_off.mean())}
    # logistic model of any disagreement (onset, home, or Jaccard < 0.5)
    anyd = (d != 0) | (h5 != h6) | ~(np.nan_to_num(jac, nan=1.0) >= 0.5)
    X = pd.DataFrame({"level": A.level.to_numpy(float), "precision_c": A.precision_c.to_numpy(float),
                      "tag_coverage": A.tag_coverage.to_numpy(float), "label_coverage_early": lc5,
                      "log_early_volume": lv5})
    # collapse groups with < 5 disagreeing or < 5 agreeing concepts into the reference level (avoids separation)
    gs = pd.Series(g5, name="grp")
    tab = pd.crosstab(gs, anyd)
    keep_g = [g for g in tab.index if tab.loc[g].min() >= 5 and tab.shape[1] == 2]
    ref = max(keep_g, key=lambda g: tab.loc[g].sum()) if keep_g else None
    gs = gs.where(gs.isin(keep_g) & (gs != ref), "ref_or_small")
    Gd = pd.get_dummies(gs, prefix="grp", dtype=float).drop(columns=["grp_ref_or_small"], errors="ignore")
    X = pd.concat([X, Gd], axis=1)
    ok = X.notna().all(axis=1).to_numpy()
    try:
        cols = [c for c in X.columns if X.loc[ok, c].std() > 0]
        Xs = X.loc[ok, cols]
        num = ["level", "precision_c", "tag_coverage", "label_coverage_early", "log_early_volume"]
        Xs[num] = (Xs[num] - Xs[num].mean()) / Xs[num].std()
        fit = sm.Logit(anyd[ok].astype(float), sm.add_constant(Xs)).fit(disp=0, maxiter=200)
        ci = fit.conf_int()
        res["any_disagreement_logit"] = {"n": int(ok.sum()), "rate": float(anyd[ok].mean()), "scaling": "numeric covariates z-scored (OR per SD)",
                                         "odds_ratios": {k: {"OR": float(np.exp(fit.params[k])), "ci95": [float(np.exp(ci.loc[k, 0])), float(np.exp(ci.loc[k, 1]))],
                                                             "p": float(fit.pvalues[k])} for k in fit.params.index if k != "const"}}
    except (np.linalg.LinAlgError, ValueError) as e:  # perfect separation etc.
        logger.error(f"logit failed: {e}")
        res["any_disagreement_logit"] = {"error": repr(e)[:200]}
    # ---------------- pooling verdict
    crit = {"onset_pm1_ge_0.80": agr["onset_pm1"]["value"] >= POOL_RULE["onset_pm1_agree_min"],
            "home_kappa_ge_0.60": agr["home_kappa_26"]["value"] >= POOL_RULE["home_kappa_min"],
            "o2r_m50_spearman_ge_0.70": agr["O2r_m50"]["spearman"] >= POOL_RULE["o2r_m50_spearman_min"],
            "retention_kappa_ge_0.40": ret["kappa_R_vs_Rcj"] >= POOL_RULE["retention_kappa_min"]}
    k_ok = sum(crit.values())
    verdict = "UNDETERMINED" if n_both < 50 else ("POOLABLE" if k_ok == 4 else ("PARTIAL" if k_ok >= 2 else "SEPARATE"))
    res["pooling"] = {"criteria": crit, "n_met": k_ok, "verdict": verdict,
                      "retention_kappa_with_matched_definition_R_abs2": ret["kappa_R_abs2_vs_Rcj"],
                      "implication": ("A failed Exp5-minus-Exp6 confirmation can be read as a failure of the H2 claim only if the frames agree on "
                                      "the retention and episode definitions. Retention kappa between Exp5 R (relative share rule) and Exp6 R_cj (absolute >= 2) "
                                      "is the binding criterion; with the matched absolute definition (R_abs2) the frames agree much better, so the confirmation "
                                      "must rebuild RETAINED/LOST on the Exp5 frame with Exp6's R_cj rule (R_abs2) before reading a null as a failure."),
                      "scope_limit": "agreement is measured on the 628 shared (newborn-candidate) concepts only; Exp6's frame is not a random subset of Exp5, so it may overstate agreement for Exp5-only (mostly non-newborn) concepts"}
    C.dump(res, C.WS / "frame_agreement.json")
    pd.DataFrame(DEFS, columns=["definition", "exp5_art_wxWssKSUR45f", "exp5_source", "exp6_art_N-mpomDZZ1ln", "exp6_source"]) \
        .to_csv(C.TAB / "definitions_diff.csv", index=False)
    C.save_manifest("wp3")
    logger.info(f"verdict {verdict} criteria {crit}")
    logger.info({k: (v.get("value") if isinstance(v, dict) else v) for k, v in agr.items()})


if __name__ == "__main__":
    if len(sys.argv) > 1:
        C.B_MAIN = int(sys.argv[1])
    main()
