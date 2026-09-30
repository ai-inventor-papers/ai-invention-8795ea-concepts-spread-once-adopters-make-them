#!/usr/bin/env python3
"""Step 3: grounding benchmark + sense filter + per-concept precision gate.
  sample  -> benchmark/bench_pairs.csv (400 stratified (concept, title) pairs from candidate hits in pass 2)
  fit     -> sense filter (logistic regression on MiniLM cosine + match/tag features), rule comparison,
             results/grounding_report.json, results/grounding_concepts.csv (precision_est, p_notag per candidate)
Usage: python grounding.py sample | fit"""
from __future__ import annotations

import hashlib
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from config import BENCH, P2, RES, SEED  # noqa: E402

logger.remove(); logger.add(sys.stdout, format="{time:HH:mm:ss}|{level:<7}|{message}")
DOMAIN = {11: "Life", 13: "Life", 24: "Life", 28: "Life", 30: "Life", 27: "Health", 29: "Health", 34: "Health",
          35: "Health", 36: "Health", 12: "Social", 14: "Social", 18: "Social", 20: "Social", 32: "Social", 33: "Social"}


def domain_of(vf: int) -> str:
    return "none" if vf < 11 else DOMAIN.get(int(vf), "Physical")


def load_hits(max_files: int | None = None) -> pd.DataFrame:
    hf = sorted(P2.glob("h*.parquet"))[:max_files]
    wf = [P2 / ("w" + p.name[1:]) for p in hf]
    H = pd.concat([pq.read_table(p).to_pandas() for p in hf], ignore_index=True)
    W = pd.concat([pq.read_table(p, columns=["work_id", "title"]).to_pandas() for p in wf], ignore_index=True)
    W = W.drop_duplicates("work_id")
    return H.merge(W, on="work_id", how="left")


def sample() -> None:
    lex = pd.read_parquet(RES / "lexicon.parquet").set_index("concept_idx")
    cand = pd.read_csv(RES / "candidates.csv")
    H = load_hits()
    H = H[H.cidx.isin(cand.cidx) & H.title.notna()]
    H["domain"] = H.vf.map(domain_of)
    rng = np.random.default_rng(SEED)
    H["u"] = rng.random(len(H))
    # strata: tag (1 / 0 / -1) x variant (0/1); within stratum spread over domains; one pair per concept per stratum
    alloc = {(1, 0): 120, (1, 1): 80, (0, 0): 90, (0, 1): 70, (-1, 0): 25, (-1, 1): 15}
    pop = H.groupby(["tag", "variant"]).size().to_dict()
    picks = []
    for (tg, vr), n in alloc.items():
        s = H[(H.tag == tg) & (H.variant == vr)].sort_values("u").drop_duplicates("cidx")
        if s.empty:
            continue
        per_dom = max(1, n // max(s.domain.nunique(), 1))
        p = s.groupby("domain", group_keys=False).head(per_dom)
        if len(p) < n:
            p = pd.concat([p, s[~s.index.isin(p.index)].head(n - len(p))])
        picks.append(p.head(n))
    B = pd.concat(picks, ignore_index=True)
    B["pair_id"] = [f"p{i:04d}" for i in range(len(B))]
    B["name"] = B.cidx.map(lex["name"]); B["description"] = B.cidx.map(lex["description"]); B["level"] = B.cidx.map(lex["level"])
    B["form"] = B.cidx.map(lex["form"])
    B["split"] = np.where(rng.random(len(B)) < 0.6, "train", "test")
    B[["pair_id", "cidx", "name", "description", "form", "level", "title", "year", "vf", "domain", "tag", "score", "variant",
       "split"]].to_csv(BENCH / "bench_pairs.csv", index=False)
    (BENCH / "stratum_population.json").write_text(json.dumps({f"{k[0]}|{k[1]}": int(v) for k, v in pop.items()}, indent=1))
    logger.info(f"benchmark pairs {len(B)}; by stratum {B.groupby(['tag','variant']).size().to_dict()}; population {pop}")


def embed(texts: list[str]) -> np.ndarray:
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    return m.encode(texts, batch_size=256, normalize_embeddings=True, show_progress_bar=False)


def features(df: pd.DataFrame) -> np.ndarray:
    ctx = (df["name"].astype(str) + ": " + df["description"].fillna("").astype(str)).tolist()
    E1 = embed(df["title"].astype(str).tolist()); E2 = embed(ctx)
    cos = (E1 * E2).sum(1)
    ntok = df["form"].astype(str).str.split().str.len()
    return np.column_stack([cos, (df.variant == 0).astype(float), (df.variant == 1).astype(float), (df.tag == 1).astype(float),
                            df.score.fillna(0).astype(float), ntok.astype(float), df.level.astype(float), (df.tag == -1).astype(float)])


FEATS = ["cos_minilm", "exact", "variant", "tag", "tag_score", "n_tokens", "level", "notags"]


def fit() -> None:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import cohen_kappa_score, roc_auc_score
    B = pd.read_csv(BENCH / "bench_pairs.csv")
    L1 = pd.read_csv(BENCH / "labels_primary.csv")[["pair_id", "label"]].rename(columns={"label": "llm1"})
    B = B.merge(L1, on="pair_id", how="left")
    rep = {}
    p2 = BENCH / "labels_second.csv"
    if p2.exists():
        L2 = pd.read_csv(p2)[["pair_id", "label"]].rename(columns={"label": "llm2"})
        B = B.merge(L2, on="pair_id", how="left")
        m = B.llm1.isin(["yes", "no"]) & B.llm2.isin(["yes", "no"])
        rep["kappa_llm1_llm2"] = float(cohen_kappa_score(B.llm1[m], B.llm2[m])); rep["n_double"] = int(m.sum())
        rep["raw_agreement_llm1_llm2"] = float((B.llm1[m] == B.llm2[m]).mean())
    ph = BENCH / "hand_labels.csv"
    if ph.exists():
        Hh = pd.read_csv(ph)[["pair_id", "hand"]]
        B = B.merge(Hh, on="pair_id", how="left")
        m = B.hand.isin(["yes", "no"]) & B.llm1.isin(["yes", "no"])
        rep["agreement_llm1_hand"] = float((B.llm1[m] == B.hand[m]).mean()); rep["n_hand"] = int(m.sum())
    B["y"] = B.llm1.map({"yes": 1, "no": 0})
    B = B[B.y.notna()].copy()
    X = features(B)
    tr, te = (B.split == "train").to_numpy(), (B.split == "test").to_numpy()
    clf = LogisticRegression(C=1.0, max_iter=2000).fit(X[tr], B.y[tr])
    B["p"] = clf.predict_proba(X)[:, 1]
    pop = json.loads((BENCH / "stratum_population.json").read_text())
    B["w"] = [pop.get(f"{t}|{v}", 0) / max(((B.tag == t) & (B.variant == v)).sum(), 1) for t, v in zip(B.tag, B.variant)]

    def prec(mask: np.ndarray) -> dict:
        d = B[te & mask]
        if d.empty or d.w.sum() == 0:
            return {"n": 0}
        return {"n": int(len(d)), "precision_weighted": float((d.y * d.w).sum() / d.w.sum()), "precision_raw": float(d.y.mean())}
    rules = {"title_only": np.ones(len(B), bool), "exact_only": (B.variant == 0).to_numpy(),
             "lemma_variant_only": (B.variant == 1).to_numpy(), "tag_and_title": (B.tag == 1).to_numpy(),
             "tag_and_title_exact": ((B.tag == 1) & (B.variant == 0)).to_numpy(), "untagged_work_title": (B.tag == -1).to_numpy(),
             "title_without_tag_on_tagged_work": (B.tag == 0).to_numpy()}
    rep["rules_test"] = {k: prec(v) for k, v in rules.items()}
    # recall of tag&title relative to title-only among labelled-yes (population weighted)
    yes = B[B.y == 1]
    rep["recall_tag_and_title_vs_title_yes"] = float((yes.w * (yes.tag == 1)).sum() / yes.w.sum()) if len(yes) else None
    rep["filter_test_auc"] = float(roc_auc_score(B.y[te], B.p[te])) if B.y[te].nunique() == 2 else None
    thr = 0.5
    pt = B[te]
    rep["filter_test_precision_at_0.5"] = float(pt.y[pt.p >= thr].mean()) if (pt.p >= thr).any() else None
    rep["filter_test_recall_at_0.5"] = float(((pt.p >= thr) & (pt.y == 1)).sum() / max((pt.y == 1).sum(), 1))
    rep["filter_coefs"] = dict(zip(FEATS, map(float, clf.coef_[0])))
    rep["by_domain_tag_and_title_precision_test"] = {d: prec((B.domain == d).to_numpy() & rules["tag_and_title"])
                                                     for d in B.domain.unique()}
    rep["by_domain_tag_and_title_precision_all"] = B[B.tag == 1].groupby("domain").y.agg(["mean", "size"]).to_dict("index")
    rep["label_dist"] = B.llm1.value_counts().to_dict()
    pickle.dump(clf, open(RES / "sense_filter.pkl", "wb"))
    rep["sense_filter_sha256"] = hashlib.sha256((RES / "sense_filter.pkl").read_bytes()).hexdigest()
    # per-concept precision estimate on <= 20 reservoir titles accepted by the rule (tag & title), p_notag on untagged works
    lex = pd.read_parquet(RES / "lexicon.parquet").set_index("concept_idx")
    cand = pd.read_csv(RES / "candidates.csv")
    H = load_hits()
    H = H[H.cidx.isin(cand.cidx) & H.title.notna() & H.tag.isin([1, -1])]
    rng = np.random.default_rng(SEED + 1)
    H["u"] = rng.random(len(H))
    R = H.sort_values("u").groupby(["cidx", "tag"]).head(20).copy()
    R["name"] = R.cidx.map(lex["name"]); R["description"] = R.cidx.map(lex["description"])
    R["form"] = R.cidx.map(lex["form"]); R["level"] = R.cidx.map(lex["level"])
    logger.info(f"scoring {len(R)} reservoir titles for {R.cidx.nunique()} candidate concepts")
    R["p"] = clf.predict_proba(features(R))[:, 1]
    pc_ = R[R.tag == 1].groupby("cidx").p.agg(["mean", "size"]).rename(columns={"mean": "precision_est", "size": "n_reservoir"})
    pn = R[R.tag == -1].groupby("cidx").p.mean().rename("p_notag")
    gc_ = pc_.join(pn, how="outer").reset_index()
    gc_.to_csv(RES / "grounding_concepts.csv", index=False)
    rep["n_concepts_scored"] = int(len(gc_))
    rep["n_concepts_below_gate_0.8"] = int((gc_.precision_est < 0.8).sum())
    rep["precision_est_quantiles"] = gc_.precision_est.quantile([0.05, 0.25, 0.5, 0.75, 0.95]).to_dict()
    B.to_csv(BENCH / "bench_labelled.csv", index=False)
    (RES / "grounding_report.json").write_text(json.dumps(rep, indent=1, default=float))
    logger.info(json.dumps(rep, default=float)[:2500])


if __name__ == "__main__":
    {"sample": sample, "fit": fit}[sys.argv[1]]()
