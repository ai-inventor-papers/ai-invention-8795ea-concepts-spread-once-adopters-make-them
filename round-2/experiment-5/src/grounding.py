#!/usr/bin/env python3
"""STEP 4: semantic grounding -- all before any outcome column exists.

  bench     400-pair benchmark from the scan reservoir (stratified by domain x mtype x single_token x tagstate);
            labeller 1 (gemini-2.5-flash-lite) labels all 400, labeller 2 (gpt-4.1-nano, other family) 150;
            Cohen's kappa; disagreements adjudicated by gemini-2.5-flash if kappa < 0.6; writes
            grounding_benchmark.csv and results/handcheck_sheet.csv (60 pairs for the executor's own reading).
  filter    MiniLM + flags L2-logistic sense filter (C by 5-fold CV on the 300 train pairs, concept-disjoint
            100 test pairs); P/R of the candidate rules; frozen grounding rule; sense_filter.joblib; applies the
            filter to untagged rows -> scan/untagged_passrate.parquet.
  precision per-concept LLM precision gate for onset candidates (10 grounded titles, +10 if 7-8/10 positive);
            writes grounding_precision.csv.
Usage: python grounding.py bench|filter|precision"""
from __future__ import annotations

import asyncio
import json
import math
import random
import sys

import aiohttp
import numpy as np
import pandas as pd

from common import (DOMAIN_OF, MTYPES, RES, RESERVOIR_DIR, ROOT, SCAN, SEED, add_deviation, jdump,
                    read_parquet_parts, setup_logger)
from llm import LLM, BudgetStop, batch_prompt, parse_json

logger = setup_logger("grounding")
M1 = "google/gemini-2.5-flash-lite"
M2 = "openai/gpt-4.1-nano"
M3 = "google/gemini-2.5-flash"
BENCH = ROOT / "grounding_benchmark.csv"
PREC_CAP = 3.50  # USD, whole artifact (ledger total); raised from the plan's $2 -- see deviations.json
HAND = RES / "handcheck_sheet.csv"
HAND_LABELS = RES / "handcheck_labels.csv"


def domain_of_code(code: int) -> str:
    return DOMAIN_OF.get(int(code) + 10, "NA") if code > 0 else "NA"


def load_lex() -> pd.DataFrame:
    lex = pd.read_parquet(ROOT / "lexicon_v1.parquet")
    lex["single_token"] = lex["name"].map(lambda s: len(s.replace("-", " ").split()) == 1).astype(int)
    lex["desc"] = [(w if isinstance(w, str) and w else (d if isinstance(d, str) else "")) for w, d in zip(lex.wd_description, lex.description)]
    return lex


async def label_items(llm: LLM, model: str, items: list[dict], tag: str, bs: int = 10) -> dict:
    """{id: (refers bool, confidence)}; stops the whole batch on the first budget refusal."""
    out: dict = {}
    batches = [items[i:i + bs] for i in range(0, len(items), bs)]
    async with aiohttp.ClientSession() as sess:
        async def one(b):
            if llm.stopped:
                return
            try:
                txt = await llm.chat(sess, model, batch_prompt(b), tag, max_tokens=60 * len(b) + 100)
            except BudgetStop as e:
                logger.error(f"budget refusal: {e}")
                return
            d = parse_json(txt)
            labs = (d or {}).get("labels", []) if isinstance(d, dict) else []
            for x in labs:
                try:
                    out[int(x["id"])] = (bool(x["refers_to_concept"]), float(x.get("confidence", math.nan)))
                except (KeyError, TypeError, ValueError):
                    continue
        await asyncio.gather(*(one(b) for b in batches), return_exceptions=False)
    return out


def kappa(a: np.ndarray, b: np.ndarray) -> float:
    a, b = a.astype(int), b.astype(int)
    po = (a == b).mean()
    pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return float((po - pe) / (1 - pe)) if pe < 1 else math.nan


def cmd_bench() -> None:
    lex = load_lex()
    rs = read_parquet_parts(RESERVOIR_DIR)
    cand = pd.read_csv(RES / "onset_candidates_match.csv")  # outcome-blind: onset on UNGROUNDED match counts
    rs = rs[rs.ci.isin(set(cand.ci)) & (rs.era >= 1) & rs.tagstate.isin([1, 2, 3])].copy()
    rs["dom"] = [domain_of_code(v if v > 0 else p) for v, p in zip(rs.vfield, rs.ptfield)]
    rs["single_token"] = lex.single_token.to_numpy()[rs.ci]
    rs["ts"] = rs.tagstate.clip(upper=2)
    rng = random.Random(SEED)
    cells = rs.groupby(["dom", "mt", "single_token", "ts"])
    keys = sorted(cells.groups)
    per = max(1, 400 // len(keys))
    pick = []
    for k in keys:
        g = cells.get_group(k)
        g = g.drop_duplicates("ci")
        pick.append(g.sample(min(per, len(g)), random_state=rng.randrange(10**6)))
    pick = pd.concat(pick)
    rest = rs[~rs.index.isin(pick.index)].drop_duplicates("ci")
    rest = rest[~rest.ci.isin(set(pick.ci))]
    if len(pick) < 400:
        pick = pd.concat([pick, rest.sample(400 - len(pick), random_state=SEED)])
    pick = pick.sample(frac=1, random_state=SEED).head(400).reset_index(drop=True)
    pick["id"] = np.arange(len(pick))
    pick["concept_id"] = lex.concept_id.to_numpy()[pick.ci]
    pick["name"] = lex["name"].to_numpy()[pick.ci]
    pick["description"] = lex.desc.to_numpy()[pick.ci]
    pick["mtype"] = [MTYPES[m] for m in pick.mt]
    concepts = sorted(set(pick.ci))
    rng2 = random.Random(SEED + 1)
    test_c = set(rng2.sample(concepts, k=round(len(concepts) * 0.25)))
    pick["split"] = np.where(pick.ci.isin(test_c), "test", "train")
    items = pick[["id", "name", "description", "title"]].to_dict("records")
    llm = LLM(concurrency=12)
    lab1 = asyncio.run(label_items(llm, M1, items, "bench:L1"))
    dbl = pick.sample(150, random_state=SEED).id.tolist()
    lab2 = asyncio.run(label_items(llm, M2, [it for it in items if it["id"] in set(dbl)], "bench:L2"))
    pick["l1"] = pick.id.map(lambda i: lab1.get(i, (None, None))[0])
    pick["l1_conf"] = pick.id.map(lambda i: lab1.get(i, (None, None))[1])
    pick["l2"] = pick.id.map(lambda i: lab2.get(i, (None, None))[0])
    both = pick.dropna(subset=["l1", "l2"])
    k = kappa(both.l1.to_numpy(bool), both.l2.to_numpy(bool)) if len(both) else math.nan
    pick["l3"] = None
    dis = both[both.l1 != both.l2]
    adjudicated = False
    if len(dis) and (not np.isfinite(k) or k < 0.6):
        adjudicated = True
        lab3 = asyncio.run(label_items(llm, M3, [it for it in items if it["id"] in set(dis.id)], "bench:L3"))
        pick["l3"] = pick.id.map(lambda i: lab3.get(i, (None, None))[0])

    def gold(r):
        if r.l2 is None or (isinstance(r.l2, float) and np.isnan(r.l2)):
            return r.l1
        if r.l1 == r.l2:
            return r.l1
        if r.l3 is not None and not (isinstance(r.l3, float) and np.isnan(r.l3)):
            return r.l3
        return r.l1
    pick["label"] = [gold(r) for r in pick.itertuples()]
    pick = pick.dropna(subset=["label"])
    pick["label"] = pick.label.astype(bool).astype(int)
    cols = ["id", "split", "ci", "concept_id", "name", "description", "title", "year", "vfield", "ptfield", "dom",
            "tagstate", "mtype", "single_token", "l1", "l1_conf", "l2", "l3", "label", "h"]
    pick[cols].to_csv(BENCH, index=False)
    hand = pick.sample(60, random_state=SEED + 7)[["id", "name", "description", "title"]]
    hand.to_csv(HAND, index=False)
    rep = {"n": len(pick), "n_double": int(len(both)), "kappa_l1_l2": k, "agree_l1_l2": float((both.l1 == both.l2).mean()),
           "adjudicated": adjudicated, "n_disagree": int(len(dis)), "positive_rate": float(pick.label.mean()),
           "models": {"L1": M1, "L2": M2, "L3": M3}, "llm_spent_usd": llm.spent,
           "split_counts": pick.split.value_counts().to_dict(),
           "positive_rate_by_tagstate": pick.groupby("tagstate").label.mean().to_dict(),
           "positive_rate_by_mtype": pick.groupby("mtype").label.mean().to_dict()}
    jdump(rep, RES / "grounding_bench_summary.json")
    logger.info(f"benchmark: {rep}")


# ----------------------------------------------------------------------------- sense filter
_EMB = None


def embed(texts: list[str]) -> np.ndarray:
    global _EMB
    if _EMB is None:
        from sentence_transformers import SentenceTransformer
        _EMB = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    return _EMB.encode(texts, batch_size=128, normalize_embeddings=True, show_progress_bar=False)


def cap_flag(name: str, title: str) -> int:
    t = title
    i = t.lower().find(name.lower().split(" (")[0][:12])
    return int(i > 0 and t[i:i + 1].isupper() and not t.istitle())


def features(df: pd.DataFrame) -> pd.DataFrame:
    et = embed(df.title.tolist())
    ec = embed([f"{n}: {d}" if d else n for n, d in zip(df.name, df.description.fillna(""))])
    X = pd.DataFrame({"cos": (et * ec).sum(1), "single_token": df.single_token.astype(int),
                      "is_alias": (df.mtype == "alias").astype(int), "is_variant": (df.mtype == "name_variant").astype(int),
                      "ts1": (df.tagstate == 1).astype(int), "ts2": (df.tagstate == 2).astype(int),
                      "ts3": (df.tagstate == 3).astype(int), "title_len": np.log1p(df.title.str.len()),
                      "cap": [cap_flag(n, t) for n, t in zip(df.name, df.title)]}, index=df.index)
    return X


def pr(y: np.ndarray, p: np.ndarray) -> dict:
    tp = int((y & p).sum()); fp = int((~y & p).sum()); fn = int((y & ~p).sum())
    prec = tp / (tp + fp) if tp + fp else math.nan
    rec = tp / (tp + fn) if tp + fn else math.nan
    f1 = 2 * prec * rec / (prec + rec) if prec and rec and np.isfinite(prec) and np.isfinite(rec) else math.nan
    return {"precision": prec, "recall": rec, "f1": f1, "n_pred_pos": int(p.sum())}


def cmd_filter() -> None:
    import joblib
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GridSearchCV, GroupKFold
    b = pd.read_csv(BENCH)
    X = features(b)
    y = b.label.to_numpy(bool)
    tr, te = (b.split == "train").to_numpy(), (b.split == "test").to_numpy()
    mu, sd = X[tr].mean(), X[tr].std().replace(0, 1)
    Xs = (X - mu) / sd
    gs = GridSearchCV(LogisticRegression(max_iter=2000), {"C": [0.01, 0.03, 0.1, 0.3, 1, 3, 10]}, scoring="roc_auc",
                      cv=GroupKFold(5))
    gs.fit(Xs[tr], y[tr], groups=b.ci[tr])
    clf = gs.best_estimator_
    p = clf.predict_proba(Xs)[:, 1]
    from sklearn.metrics import roc_auc_score
    rules = {"a_stemmed_any": np.ones(len(b), bool), "b_exact_name_only": (b.mtype == "name_exact").to_numpy(),
             "c_TAG": (b.tagstate == 1).to_numpy(), "d_filter_p05": p >= 0.5,
             "e_TAG_or_untagged_filter": (b.tagstate == 1).to_numpy() | ((b.tagstate == 3).to_numpy() & (p >= 0.5))}
    res = {k: pr(y[te], v[te]) for k, v in rules.items()}
    res_train = {k: pr(y[tr], v[tr]) for k, v in rules.items()}
    auc = float(roc_auc_score(y[te], p[te])) if len(set(y[te])) == 2 else math.nan
    # T4 decision (benchmark test split only, never outcomes)
    f, ex = res["d_filter_p05"], res["b_exact_name_only"]
    t4_filter_ok = bool(f["precision"] > ex["precision"] and f["recall"] >= ex["recall"])
    if t4_filter_ok:
        rule = "e_TAG_or_untagged_filter"
    else:
        rule = max(["c_TAG", "b_exact_name_only"], key=lambda k: -1 if not np.isfinite(res[k]["f1"]) else res[k]["f1"])
    joblib.dump({"clf": clf, "mu": mu, "sd": sd, "cols": list(X.columns), "C": gs.best_params_["C"]},
                ROOT / "sense_filter.joblib")
    # hand check agreement (executor's own labels)
    hand = {}
    if HAND_LABELS.exists():
        hl = pd.read_csv(HAND_LABELS).merge(b[["id", "label", "l1"]], on="id")
        hand = {"n": len(hl), "agree_with_gold": float((hl.executor_label.astype(int) == hl.label).mean()),
                "agree_with_L1": float((hl.executor_label.astype(int) == hl.l1.astype(bool).astype(int)).mean())}
    # apply filter to untagged rows (tagstate 3): pass rate per (concept, mtype) from the 20% hash sample
    us = pd.read_parquet(SCAN / "untagged_sample_titles.parquet")
    passrate = pd.DataFrame(columns=["ci", "mt", "passrate", "n_sample"])
    if len(us):
        lex = load_lex()
        us["name"] = lex["name"].to_numpy()[us.ci]
        us["description"] = lex.desc.to_numpy()[us.ci]
        us["single_token"] = lex.single_token.to_numpy()[us.ci]
        us["mtype"] = [MTYPES[m] for m in us.mt]
        Xu = (features(us) - mu) / sd
        us["p"] = clf.predict_proba(Xu[X.columns])[:, 1]
        passrate = us.assign(ok=us.p >= 0.5).groupby(["ci", "mt"]).agg(passrate=("ok", "mean"), n_sample=("ok", "size")).reset_index()
    passrate.to_parquet(SCAN / "untagged_passrate.parquet", index=False)
    rep = json.loads((RES / "grounding_bench_summary.json").read_text())
    rep.update({"filter": {"C": gs.best_params_["C"], "test_auc": auc,
                           "coef": dict(zip(X.columns, clf.coef_[0].round(3).tolist()))},
                "rules_test": res, "rules_train": res_train, "T4_filter_beats_exact": t4_filter_ok,
                "frozen_grounding_rule": rule, "handcheck": hand, "n_untagged_sample_rows": int(len(us)),
                "positive_rate_test": float(y[te].mean())})
    jdump(rep, ROOT / "grounding_report.json")
    logger.info(f"filter: rule={rule} test={res} auc={auc:.3f}")


# ----------------------------------------------------------------------------- per-concept precision gate
def grounded_mask(df: pd.DataFrame, rule: str) -> np.ndarray:
    if rule == "b_exact_name_only":
        return (df.mt == 0).to_numpy()
    return (df.tagstate == 1).to_numpy() | (df.tagstate == 3).to_numpy()  # ts3 rows are gated by the filter


def cmd_precision() -> None:
    rep = json.loads((ROOT / "grounding_report.json").read_text())
    rule = rep["frozen_grounding_rule"]
    lex = load_lex()
    cand = pd.read_csv(RES / "onset_candidates_grounded.csv")
    # outcome-blind pre-filter: concepts the home rule would drop anyway (diffuse_born / no labels) are not labelled
    from frame import home_rule, n_concepts
    from panel import build_arrays
    V = build_arrays("grounded", n_concepts())["V"]
    st = [home_rule(V[r.ci], r.t0)["status"] for r in cand.itertuples()]
    cand = cand[[x not in ("diffuse_born", "no_labels") for x in st]].reset_index(drop=True)
    # seeded random order: if the budget stops the batch, the labelled set is an unbiased prefix
    cand = cand.sample(frac=1, random_state=SEED).reset_index(drop=True)
    logger.info(f"precision gate: {len(cand)} candidates after the home-rule pre-filter")
    rs = read_parquet_parts(RESERVOIR_DIR)
    rs = rs[rs.ci.isin(set(cand.ci)) & (rs.era >= 1)]
    rs = rs[grounded_mask(rs, rule)].sort_values(["ci", "h"])
    first, second = [], []
    for ci, g in rs.groupby("ci"):
        first.append(g.head(10))
        second.append(g.iloc[10:20])
    first = pd.concat(first) if first else rs.head(0)
    second = pd.concat(second) if second else rs.head(0)
    llm = LLM(concurrency=48, cap=PREC_CAP)

    def items(df):
        return [{"id": int(i), "name": lex["name"].iat[ci], "description": lex.desc.iat[ci], "title": t}
                for i, ci, t in zip(df.index, df.ci, df.title)]

    async def run(df, tag):
        out = {}
        order = {c: i for i, c in enumerate(cand.ci)}
        groups = [items(g) for _, g in sorted(df.groupby("ci"), key=lambda kv: order.get(kv[0], 0))]
        async with aiohttp.ClientSession() as sess:
            async def one(its):
                if llm.stopped:
                    return
                try:
                    txt = await llm.chat(sess, M1, batch_prompt(its), tag, max_tokens=60 * len(its) + 100)
                except BudgetStop as e:
                    logger.error(f"budget refusal: {e}")
                    return
                d = parse_json(txt)
                for x in (d or {}).get("labels", []) if isinstance(d, dict) else []:
                    try:
                        out[int(x["id"])] = bool(x["refers_to_concept"])
                    except (KeyError, TypeError, ValueError):
                        continue
            await asyncio.gather(*(one(g) for g in groups))
        return out
    lab = asyncio.run(run(first, "prec:first"))
    first = first.assign(lab=first.index.map(lambda i: lab.get(int(i))))
    s1 = first.dropna(subset=["lab"]).groupby("ci").lab.agg(["sum", "size"])
    gray = s1[(s1["sum"] >= 0.7 * s1["size"]) & (s1["sum"] <= 0.8 * s1["size"]) & (s1["size"] >= 8)].index
    sec = second[second.ci.isin(gray)]
    lab2 = asyncio.run(run(sec, "prec:second")) if len(sec) else {}
    sec = sec.assign(lab=sec.index.map(lambda i: lab2.get(int(i))))
    allb = pd.concat([first, sec]).dropna(subset=["lab"])
    agg = allb.groupby("ci").lab.agg(["sum", "size"]).rename(columns={"sum": "n_pos", "size": "n_labelled_prec"})
    out = cand[["ci"]].merge(agg, left_on="ci", right_index=True, how="left")
    out["precision_c"] = out.n_pos / out.n_labelled_prec
    out["precision_source"] = np.where(out.n_labelled_prec.notna(), "llm", "none")
    # fallback: concepts without an LLM label (budget stop) are gated by the sense filter's mean prediction
    miss = out.precision_c.isna()
    if miss.any():
        import joblib
        sf = joblib.load(ROOT / "sense_filter.joblib")
        r2 = rs[rs.ci.isin(set(out.ci[miss]))].groupby("ci").head(10).copy()
        if len(r2):
            r2["name"] = lex["name"].to_numpy()[r2.ci]
            r2["description"] = lex.desc.to_numpy()[r2.ci]
            r2["single_token"] = lex.single_token.to_numpy()[r2.ci]
            r2["mtype"] = [MTYPES[m] for m in r2.mt]
            Xf = (features(r2) - sf["mu"]) / sf["sd"]
            r2["p"] = sf["clf"].predict_proba(Xf[sf["cols"]])[:, 1]
            fp = r2.groupby("ci").p.mean()
            out.loc[miss, "precision_c"] = out.loc[miss, "ci"].map(fp)
            out.loc[miss & out.precision_c.notna(), "precision_source"] = "filter"
        add_deviation("precision_gate_fallback", f"{int(miss.sum())} concepts had no LLM precision label; gated by "
                                                 "the sense filter's mean predicted precision (precision_source=filter)")
    out["concept_id"] = lex.concept_id.to_numpy()[out.ci]
    out["name"] = lex["name"].to_numpy()[out.ci]
    out["pass_gate"] = out.precision_c >= 0.8
    out.to_csv(ROOT / "grounding_precision.csv", index=False)
    logger.info(f"precision gate: {len(out)} candidates, pass={int(out.pass_gate.sum())}, "
                f"gray relabelled={len(gray)}, llm spent total={llm.spent:.3f}")


if __name__ == "__main__":
    {"bench": cmd_bench, "filter": cmd_filter, "precision": cmd_precision}[sys.argv[1]]()
