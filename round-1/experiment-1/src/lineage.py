"""Concept lineage network, S2-based S0 field distributions, stage-1 field-stratified MH contrasts and foils.

Labels: each paper carries a FRACTIONAL field-membership vector over the Semantic Scholar fields of study
(s2-fos-model categories, a title/abstract text classifier, uniform over the predicted categories; the MAG
'external' categories are used only when the model has none). Text-based labels do not encode the paper's own
references, so they are not circular for citation-flow contrasts (the concern that ruled out OpenAlex topics).
"""
from __future__ import annotations

import gzip
import hashlib
import json
import math
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
S2_FIELDS = ["Computer Science", "Engineering", "Biology", "Medicine", "Chemistry", "Materials Science", "Physics",
             "Mathematics", "Environmental Science", "Agricultural and Food Sciences", "Geology", "Geography",
             "Psychology", "Sociology", "Economics", "Business", "Political Science", "Education", "Law",
             "Linguistics", "Philosophy", "History", "Art"]
FIDX = {f: i for i, f in enumerate(S2_FIELDS)}
F = len(S2_FIELDS)
S2_DEV = {"Computer Science": "Computer Science", "Engineering": "Engineering",
          "Biology": "Biochemistry, Genetics and Molecular Biology", "Medicine": "Medicine"}
SEED = 20260928


def membership(fos: list[dict] | None) -> np.ndarray | None:
    fos = fos or []
    cats = sorted({f["category"] for f in fos if f.get("source") == "s2-fos-model" and f["category"] in FIDX})
    if not cats:
        cats = sorted({f["category"] for f in fos if f["category"] in FIDX})
    if not cats:
        return None
    v = np.zeros(F)
    for c in cats:
        v[FIDX[c]] = 1.0 / len(cats)
    return v


def stable_seed(s: str) -> int:
    return int(hashlib.sha1(s.encode()).hexdigest()[:12], 16) ^ SEED


def home_set(mass: np.ndarray) -> list[int]:
    tot = mass.sum()
    if tot <= 0:
        return []
    h = [i for i in range(F) if mass[i] / tot >= 0.40]
    return h or [int(np.argmax(mass))]


@dataclass
class Concept:
    name: str
    t0: int
    ids: list[str]
    year: np.ndarray
    M: np.ndarray                       # (n, F) membership (rows of unlabelled papers are all zero)
    labelled: np.ndarray                # (n,) bool
    authors: list[set]
    mag: list[str | None]
    doi: list[str | None]
    gstatus: list[str]
    H: list[int]
    hmask: np.ndarray
    late_mass: np.ndarray
    thin_early: float
    thin_late: float
    exact_share: float
    # lineage
    child_idx: np.ndarray = field(default_factory=lambda: np.zeros(0, int))
    P: np.ndarray = field(default_factory=lambda: np.zeros((0, F)))       # mean CROSS-parent membership per child
    n_cross: np.ndarray = field(default_factory=lambda: np.zeros(0))
    n_self: np.ndarray = field(default_factory=lambda: np.zeros(0))
    has_any_parent: np.ndarray = field(default_factory=lambda: np.zeros(0, bool))
    links: list = field(default_factory=list)                              # (child, parent, self)
    indeg_before: dict = field(default_factory=dict)

    @property
    def C(self) -> np.ndarray:
        return self.M[self.child_idx]

    @property
    def cH(self) -> np.ndarray:
        return self.C @ self.hmask

    @property
    def child_year(self) -> np.ndarray:
        return self.year[self.child_idx]


def load_concept(raw: dict) -> Concept:
    t0 = raw["t0"]
    E = [p for p in raw["early"] if p.get("year") and p["gstatus"] != "rejected"]
    ids = [p["paperId"] for p in E]
    year = np.array([p["year"] for p in E])
    mem = [membership(p.get("s2FieldsOfStudy")) for p in E]
    labelled = np.array([m is not None for m in mem])
    M = np.array([m if m is not None else np.zeros(F) for m in mem]).reshape(len(E), F)
    authors = [{a["authorId"] for a in p.get("authors") or [] if a.get("authorId")} for p in E]
    ext = [p.get("externalIds") or {} for p in E]
    early_mask = (year >= t0) & (year <= t0 + 1)
    H = home_set(M[early_mask].sum(0))
    hmask = np.zeros(F)
    hmask[H] = 1.0
    late = np.zeros(F)
    for p in raw["late"]:
        m = membership(p.get("s2FieldsOfStudy"))
        if m is not None:
            late += m
    n_ver = sum(p["gstatus"] != "unverifiable" for p in raw["early"])
    n_conf = sum(p["gstatus"] == "confirmed" for p in raw["early"])
    c = Concept(name=raw["concept"], t0=t0, ids=ids, year=year, M=M, labelled=labelled, authors=authors,
                mag=[e.get("MAG") for e in ext], doi=[e.get("DOI") for e in ext],
                gstatus=[p["gstatus"] for p in E], H=H, hmask=hmask, late_mass=late,
                thin_early=(raw.get("total_early") or len(raw["early"])) / max(len(raw["early"]), 1),
                thin_late=(raw.get("total_late") or len(raw["late"])) / max(len(raw["late"]), 1),
                exact_share=n_conf / n_ver if n_ver else float("nan"))
    build_lineage(c, raw["citations"])
    return c


def build_lineage(c: Concept, citations: dict[str, list[str]]) -> None:
    pos = {pid: i for i, pid in enumerate(c.ids)}
    cross: dict[int, list[int]] = {}
    selfp: dict[int, list[int]] = {}
    indeg: dict[int, dict[int, int]] = {}
    for q_id, citing in citations.items():
        q = pos.get(q_id)
        if q is None or not c.labelled[q]:
            continue
        for p_id in citing:
            p = pos.get(p_id)
            if p is None or not c.labelled[p]:
                continue
            tp, tq = c.year[p], c.year[q]
            if tp > tq:
                for yy in range(tp + 1, c.t0 + 6):   # in-citations received strictly before year yy
                    indeg.setdefault(q, {}).setdefault(yy, 0)
                    indeg[q][yy] += 1
            if not (c.t0 <= tp <= c.t0 + 4 and 1 <= tp - tq <= 3):
                continue
            is_self = bool(c.authors[p] & c.authors[q])
            c.links.append((p, q, is_self))
            (selfp if is_self else cross).setdefault(p, []).append(q)
    anyp = sorted(set(cross) | set(selfp))
    kids = sorted(cross)
    c.child_idx = np.array(kids, int)
    c.P = np.array([c.M[cross[k]].mean(0) for k in kids]).reshape(len(kids), F)
    c.n_cross = np.array([len(cross[k]) for k in kids], float)
    c.n_self = np.array([len(selfp.get(k, [])) for k in kids], float)
    c.has_any_parent = np.zeros(len(c.ids), bool)
    c.has_any_parent[anyp] = True
    c._selfp, c._cross = selfp, cross
    c.indeg_before = indeg


# ---------------------------------------------------------------- stage-1 tables
T_STRATA = 5


def contribs(Cm: np.ndarray, Pm: np.ndarray, hmask: np.ndarray) -> np.ndarray:
    """Per-child contributions (4, n, F) to the cells a, b, c', d of every field-j table.
    Rows: child in j vs child in H; columns: parent in j vs parent in H; third-field parent mass is excluded and each
    child's retained parent mass renormalised to 1 (children with no retained mass contribute nothing)."""
    cH = Cm @ hmask
    pH = Pm @ hmask
    ret = Pm + pH[:, None]
    with np.errstate(invalid="ignore", divide="ignore"):
        pj = np.where(ret > 0, Pm / ret, 0.0)
        ph = np.where(ret > 0, pH[:, None] / ret, 0.0)
    return np.stack([Cm * pj, Cm * ph, cH[:, None] * pj, cH[:, None] * ph])


def onehot_years(years: np.ndarray, t0: int) -> np.ndarray:
    return np.eye(T_STRATA)[np.clip(years - t0, 0, T_STRATA - 1)]          # (n, T)


def tables_w(con: np.ndarray, oh: np.ndarray, W: np.ndarray) -> np.ndarray:
    """Weighted year-stratified tables for a batch of child weight vectors W (B, n) -> (4, B, T, F)."""
    return np.einsum("bn,nt,knf->kbtf", W, oh, con, optimize=True)


def tables(Cm: np.ndarray, Pm: np.ndarray, years: np.ndarray, hmask: np.ndarray, t0: int) -> np.ndarray:
    """Year-stratified 2x2 tables for every field j at once. Returns (4, T, F): a, b, c', d."""
    if len(Cm) == 0:
        return np.zeros((4, T_STRATA, F))
    return tables_w(contribs(Cm, Pm, hmask), onehot_years(years, t0), np.ones((1, len(Cm))))[:, 0]


def mh_lor(tab: np.ndarray) -> np.ndarray:
    """Mantel-Haenszel pooled log-OR over the strata axis (-2). tab (4, ..., T, F) -> (..., F). Strata with an empty
    row/column margin are skipped; strata with any zero cell get +0.5 in every cell (Haldane)."""
    a, b, c, d = tab[0], tab[1], tab[2], tab[3]
    valid = ((a + b) > 0) & ((c + d) > 0) & ((a + c) > 0) & ((b + d) > 0)
    corr = 0.5 * (valid & ((a == 0) | (b == 0) | (c == 0) | (d == 0)))
    a, b, c, d = a + corr, b + corr, c + corr, d + corr
    n = a + b + c + d
    with np.errstate(invalid="ignore", divide="ignore"):
        num = np.where(valid, a * d / n, 0).sum(-2)
        den = np.where(valid, b * c / n, 0).sum(-2)
        return np.where((num > 0) & (den > 0), np.log(num / den), np.nan)


def mh_lor_pooled(tab: np.ndarray, cols: np.ndarray) -> float:
    """MH over all (j, t) strata jointly for the given field columns -> one concept-level log-OR."""
    sub = tab[:, :, cols].reshape(4, -1, 1)
    return float(mh_lor(sub)[0])


@dataclass
class Stage1:
    rho_hat: np.ndarray          # (F,) concept minus background MH log-OR, NaN where undefined
    lor_c: np.ndarray
    lor_bg: np.ndarray
    v: np.ndarray                # bootstrap variance
    n_child_j: np.ndarray        # linked child mass in j
    A_h_MH: float
    A_h_MH_c: float
    A_h_MH_bg: float


def stage1(c: Concept, bgB: np.ndarray, bg_rows: np.ndarray, sub: np.ndarray | None = None,
           n_boot: int = 200, seed: int = SEED) -> Stage1:
    """bgB: (n_children, F) mean background-reference membership per child (zero rows where no background, which
    therefore contribute nothing to the background tables); sub: optional child subset (split-half).
    Bootstrap = multinomial child weights (resampling children with replacement; each child's concept links and
    background references move together, so the covariance between the two terms is kept)."""
    idx = np.arange(len(c.child_idx)) if sub is None else sub
    Cm, Pm, yrs = c.C[idx], c.P[idx], c.child_year[idx]
    Bm = np.where(bg_rows[idx][:, None], bgB[idx], 0.0)
    off = np.ones(F, bool)
    off[c.H] = False
    n = len(idx)
    conc, conb = contribs(Cm, Pm, c.hmask), contribs(Cm, Bm, c.hmask)
    oh = onehot_years(yrs, c.t0)
    tc = tables_w(conc, oh, np.ones((1, n)))[:, 0]
    tb = tables_w(conb, oh, np.ones((1, n)))[:, 0]
    lc, lb = mh_lor(tc), mh_lor(tb)
    rho = lc - lb
    rho[~off] = np.nan
    nj = Cm.sum(0)
    rho[nj <= 0] = np.nan
    rng = np.random.default_rng(seed)
    boots = np.full((n_boot, F), np.nan)
    for s0 in range(0, n_boot, 100):
        B = min(100, n_boot - s0)
        W = np.stack([np.bincount(rng.integers(0, n, n), minlength=n) for _ in range(B)]).astype(float)
        boots[s0:s0 + B] = mh_lor(tables_w(conc, oh, W)) - mh_lor(tables_w(conb, oh, W))
    ok = np.isfinite(boots).mean(0) >= 0.5
    with warnings.catch_warnings():  # all-NaN / single-value columns are expected for fields without data
        warnings.simplefilter("ignore", RuntimeWarning)
        v = np.nanvar(boots, axis=0, ddof=1) if n_boot > 1 else np.full(F, np.nan)
    rho[~ok] = np.nan
    v = np.where(np.isfinite(rho), np.maximum(v, 1e-3), np.nan)
    cols = np.where(off & (nj > 0))[0]
    amc = mh_lor_pooled(tc, cols) if len(cols) else float("nan")
    amb = mh_lor_pooled(tb, cols) if len(cols) else float("nan")
    return Stage1(rho_hat=rho, lor_c=lc, lor_bg=lb, v=v, n_child_j=nj, A_h_MH=amc - amb, A_h_MH_c=amc, A_h_MH_bg=amb)


# ---------------------------------------------------------------- foils
def crude_lor(child_off: np.ndarray, par_off: np.ndarray) -> float:
    """Unstratified 2x2 (child off-home vs home) x (parent off-home vs home) with Haldane 0.5 (probe definition)."""
    a = (child_off * par_off).sum() + .5
    b = (child_off * (1 - par_off)).sum() + .5
    cc = ((1 - child_off) * par_off).sum() + .5
    d = ((1 - child_off) * (1 - par_off)).sum() + .5
    return math.log(a * d / (b * cc))


def logit_s(p: float, n: float) -> float:
    return math.log((p * n + 0.5) / ((1 - p) * n + 0.5))


def foils(c: Concept, bgB: np.ndarray, bg_rows: np.ndarray) -> dict:
    out: dict = {}
    if len(c.child_idx) == 0:
        return {k: float("nan") for k in ("raw_LOR", "bg_LOR", "A_h_crude", "A_unif", "A_imp", "relay_share",
                                          "R_away", "raw_LOR_sampled")} | {
            "self_share": _self_share(c), "coverage": _coverage(c)}
    Cm, Pm, cH = c.C, c.P, c.cH
    tot = Pm.sum(1)
    pH = Pm @ c.hmask
    par_off = np.where(tot > 0, 1 - pH / np.where(tot > 0, tot, 1), 0)
    out["raw_LOR"] = crude_lor(1 - cH, par_off)
    br = bg_rows
    if br.any():
        bt = bgB[br].sum(1)
        b_off = np.where(bt > 0, 1 - (bgB[br] @ c.hmask) / np.where(bt > 0, bt, 1), 0)
        out["bg_LOR"] = crude_lor(1 - cH[br], b_off)
        out["raw_LOR_sampled"] = crude_lor(1 - cH[br], par_off[br])
        out["A_h_crude"] = out["raw_LOR_sampled"] - out["bg_LOR"]
    else:
        out["bg_LOR"] = out["raw_LOR_sampled"] = out["A_h_crude"] = float("nan")
    # relay share: off-home child mass whose parents sit in third fields
    offc = Cm * (1 - c.hmask)
    third = 1 - Pm - pH[:, None]
    third = np.clip(third, 0, 1)
    den = offc.sum()
    out["relay_share"] = float((offc * third).sum() / den) if den > 0 else float("nan")
    out["self_share"] = _self_share(c)
    out["coverage"] = _coverage(c)
    # A_unif / A_imp (probe definitions, fractional): off-home children's share of off-home parents vs stock
    w_off = 1 - cH
    A = (w_off * par_off).sum() / w_off.sum() if w_off.sum() > 0 else float("nan")
    e_u = e_i = 0.0
    wsum = 0.0
    lab = np.where(c.labelled)[0]
    for k, ci in enumerate(c.child_idx):
        if w_off[k] <= 0:
            continue
        y = c.year[ci]
        stock = lab[(c.year[lab] >= y - 3) & (c.year[lab] < y)]
        if len(stock) == 0:
            continue
        so = 1 - c.M[stock] @ c.hmask
        wi = np.array([1 + c.indeg_before.get(int(q), {}).get(int(y), 0) for q in stock], float)
        e_u += w_off[k] * so.mean()
        e_i += w_off[k] * (so * wi).sum() / wi.sum()
        wsum += w_off[k]
    if wsum > 0 and np.isfinite(A):
        out["A_unif"] = logit_s(A, wsum) - logit_s(e_u / wsum, wsum)
        out["A_imp"] = logit_s(A, wsum) - logit_s(e_i / wsum, wsum)
    else:
        out["A_unif"] = out["A_imp"] = float("nan")
    out["R_away"] = r_away(c)
    return out


def _self_share(c: Concept) -> float:
    tot = {}
    for p, q, s in c.links:
        tot.setdefault(p, [0, 0])
        tot[p][0] += s
        tot[p][1] += 1
    if not tot:
        return float("nan")
    return float(np.mean([a / b for a, b in tot.values()]))


def _coverage(c: Concept) -> float:
    m = c.labelled & (c.year >= c.t0) & (c.year <= c.t0 + 4)
    return float(c.has_any_parent[m].mean()) if m.any() else float("nan")


def r_away(c: Concept) -> float:
    """Spectral radius of K[a,b] = cross-link mass child-field a -> parent-field b / stock mass of b in parent
    years, restricted to off-home fields with >= 5 papers of stock."""
    K = c.C.T @ c.P                                     # (F, F) child field x parent field link mass
    stock = c.M[(c.year >= c.t0 - 3) & (c.year <= c.t0 + 3)].sum(0)
    keep = [i for i in range(F) if i not in c.H and stock[i] >= 5]
    if not keep:
        return float("nan")
    Ks = K[np.ix_(keep, keep)] / stock[keep][None, :]
    return float(np.max(np.abs(np.linalg.eigvals(Ks))))


def load_raw(slug_: str) -> dict:
    return json.loads(gzip.decompress((ROOT / "results" / "concepts" / slug_ / "s2_raw.json.gz").read_bytes()))
