"""Shared paths, ID normaliser, statistics helpers and provenance tracking for the record audit."""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats

WS = Path(__file__).resolve().parent
# Root that holds the dependency artifacts (iter_1/..., iter_2/...). Default: the run layout this workspace sits in
# (<root>/iter_3/gen_art/<this folder>); override with AII_RUN_ROOT when the artifacts live elsewhere.
ROOT = Path(os.environ.get("AII_RUN_ROOT", str(WS.parents[2]))).resolve()
SEED = 20260928
B_MAIN = 2000

E5 = ROOT / "round-2/experiment-5/src"
E6 = ROOT / "round-2/experiment-6/src"
D2 = ROOT / "round-2/dataset-2/src"
EV1 = ROOT / "round-2/evaluation-1/src"
X1 = ROOT / "round-1/experiment-1/src"
X3 = ROOT / "round-1/experiment-3/src"
X4 = ROOT / "round-1/experiment-4/src"
DRAFT = ROOT / "round-2/report-text/paper_draft.md"
REVIEW = ROOT / "round-2/review/.terminal_claude_agent_struct_out.json"

RES = WS / "results"
TAB = WS / "record_tables"
LOGS = WS / "logs"
for _d in (RES, TAB, LOGS):
    _d.mkdir(exist_ok=True)

_READ: dict[str, str] = {}


def setup_logging(name: str) -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")


def rel(p: Path | str) -> str:
    """Path relative to ROOT (never absolute in outputs); workspace files relative to the workspace."""
    p = Path(p).resolve()
    try:
        return str(p.relative_to(WS))
    except ValueError:
        pass
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return p.name


def track(p: Path) -> Path:
    """Record the sha256 of every input file read (inputs_manifest.json)."""
    k = rel(p)
    if k not in _READ and p.exists() and p.is_file():
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 22), b""):
                h.update(chunk)
        _READ[k] = h.hexdigest()
    return p


def read_json(p: Path):
    return json.loads(track(p).read_text())


def read_csv(p: Path, **kw) -> pd.DataFrame:
    return pd.read_csv(track(p), **kw)


def save_manifest(name: str) -> None:
    path = RES / f"inputs_manifest_{name}.json"
    path.write_text(json.dumps(dict(sorted(_READ.items())), indent=1))


def get_path(obj, key_path: str):
    """Resolve a dotted key path; keys may themselves contain dots (longest match first); list indices as integers.
    Raises KeyError if absent."""
    parts = key_path.split(".")

    def rec(cur, i):
        if i == len(parts):
            return cur
        for j in range(len(parts), i, -1):
            k = ".".join(parts[i:j])
            if isinstance(cur, dict) and k in cur:
                try:
                    return rec(cur[k], j)
                except KeyError:
                    continue
            if isinstance(cur, list) and j == i + 1 and k.isdigit() and int(k) < len(cur):
                return rec(cur[int(k)], j)
        raise KeyError(key_path)

    return rec(obj, 0)


def norm_id(x) -> str | None:
    """Exp5 integer 37253 -> 'C37253'; Exp6 'https://openalex.org/C739882' -> 'C739882'; 'C...' unchanged."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return None
    s = str(x).strip()
    if "/" in s:
        s = s.rstrip("/").split("/")[-1]
    if s.upper().startswith("C"):
        s = s[1:]
    if s.endswith(".0"):
        s = s[:-2]
    assert s.isdigit(), f"bad concept id {x!r}"
    return "C" + str(int(s))


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        v = float(o)
        return None if not math.isfinite(v) else v
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, Path):
        return rel(o)
    return o


def dump(obj, path: Path) -> None:
    path.write_text(json.dumps(jsonable(obj), indent=1))


# ------------------------------------------------------------------ statistics
def pct_ci(v, lo=2.5, hi=97.5) -> list[float]:
    v = np.asarray([x for x in v if x is not None and np.isfinite(x)], dtype=float)
    if len(v) == 0:
        return [math.nan, math.nan]
    return [float(np.percentile(v, lo)), float(np.percentile(v, hi))]


def wilson(k: int, n: int, z: float = 1.959964) -> list[float]:
    if n == 0:
        return [math.nan, math.nan]
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [c - h, c + h]


def cohen_kappa(a, b, labels=None) -> float:
    a = np.asarray(a)
    b = np.asarray(b)
    if len(a) == 0:
        return math.nan
    labs = np.unique(np.concatenate([a, b])) if labels is None else np.asarray(labels)
    idx = {v: i for i, v in enumerate(labs)}
    k = len(labs)
    m = np.zeros((k, k))
    for x, y in zip(a, b):
        m[idx[x], idx[y]] += 1
    n = m.sum()
    po = np.trace(m) / n
    pe = (m.sum(0) * m.sum(1)).sum() / n / n
    return float((po - pe) / (1 - pe)) if pe < 1 else (1.0 if po == 1 else math.nan)


def lin_ccc(x, y) -> float:
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return math.nan
    mx, my = x.mean(), y.mean()
    vx, vy = x.var(), y.var()
    cov = ((x - mx) * (y - my)).mean()
    return float(2 * cov / (vx + vy + (mx - my) ** 2))


def spearman(x, y) -> float:
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 4 or np.std(x[ok]) == 0 or np.std(y[ok]) == 0:
        return math.nan
    return float(stats.spearmanr(x[ok], y[ok]).statistic)


def partial_spearman(x, y, Z) -> float:
    """Spearman partial correlation: Pearson of rank-residuals after OLS on ranked covariates."""
    df = pd.DataFrame({"x": x, "y": y})
    Zd = pd.DataFrame(Z).reset_index(drop=True)
    df = pd.concat([df.reset_index(drop=True), Zd], axis=1).dropna()
    if len(df) < 10:
        return math.nan
    r = df.rank()
    Zm = np.column_stack([np.ones(len(r)), r.iloc[:, 2:].to_numpy(float)])
    bx = np.linalg.lstsq(Zm, r["x"].to_numpy(float), rcond=None)[0]
    by = np.linalg.lstsq(Zm, r["y"].to_numpy(float), rcond=None)[0]
    ex = r["x"].to_numpy(float) - Zm @ bx
    ey = r["y"].to_numpy(float) - Zm @ by
    if ex.std() == 0 or ey.std() == 0:
        return math.nan
    return float(np.corrcoef(ex, ey)[0, 1])


def auc(y, s) -> float:
    y = np.asarray(y, float)
    s = np.asarray(s, float)
    ok = np.isfinite(y) & np.isfinite(s)
    y, s = y[ok], s[ok]
    n1 = int((y == 1).sum())
    n0 = int((y == 0).sum())
    if n1 == 0 or n0 == 0:
        return math.nan
    r = stats.rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def dersimonian_laird(est, se) -> dict:
    est = np.asarray(est, float)
    se = np.asarray(se, float)
    ok = np.isfinite(est) & np.isfinite(se) & (se > 0)
    est, se = est[ok], se[ok]
    k = len(est)
    if k == 0:
        return {"k": 0}
    w = 1 / se ** 2
    fe = (w * est).sum() / w.sum()
    Q = float((w * (est - fe) ** 2).sum())
    tau2 = max(0.0, (Q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum())) if k > 1 else 0.0
    ws = 1 / (se ** 2 + tau2)
    re = float((ws * est).sum() / ws.sum())
    sre = float(math.sqrt(1 / ws.sum()))
    I2 = float(max(0.0, (Q - (k - 1)) / Q)) if Q > 0 and k > 1 else 0.0
    return {"k": k, "pooled": re, "se": sre, "ci95": [re - 1.959964 * sre, re + 1.959964 * sre], "tau2": tau2,
            "Q": Q, "I2": I2, "p": float(2 * stats.norm.sf(abs(re / sre)))}


def holm(pvals: dict) -> dict:
    items = [(k, v) for k, v in pvals.items() if v is not None and np.isfinite(v)]
    items.sort(key=lambda kv: kv[1])
    m = len(items)
    out, run = {}, 0.0
    for i, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - i) * p))
        out[k] = run
    return out
