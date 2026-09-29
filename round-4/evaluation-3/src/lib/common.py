"""Shared paths, constants, estimators and the ledger helper for the openness boundary evaluation.

Every estimator is the Exp8 one (vendor/rq1stats.py, copied verbatim from art_dFQ6jbgNsR6Q lib/rq1stats.py):
partial Spearman = Pearson of OLS residuals of within-unit ranks on [1, rank(B5 + extra controls), t0 dummies
(+ group dummies in the cohort units)]."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WS / "vendor"))
RUN = Path(os.environ.get("AII_RUN_LOOP", str(WS.parents[2])))          # .../3_invention_loop
E8 = RUN / "iter_3/gen_art/gen_art_experiment_8"
E7 = RUN / "iter_3/gen_art/gen_art_experiment_7"
E5 = RUN / "iter_2/gen_art/gen_art_experiment_5"
EV2 = RUN / "iter_3/gen_art/gen_art_evaluation_2"
DS2 = RUN / "iter_2/gen_art/gen_art_dataset_2"
E9 = RUN / "iter_3/gen_art/gen_art_experiment_9"
R2 = RUN / "iter_3/gen_art/gen_art_research_2"
REPORT = RUN / "iter_4/gen_strat/current_report.md"
RES = WS / "results"
FIG = WS / "figures"
LOGS = WS / "logs"
COR = WS / "corrections"
for _d in (RES, FIG, LOGS, COR):
    _d.mkdir(parents=True, exist_ok=True)

SEED = 20260929
Y0 = 1995
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
HELD4 = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]
UNITS6 = HELD4 + ["COH_DEVHOME", "COH_OTHER"]
DEV_UNITS = ["CS", "Eng", "BGM", "Med"]
COMPONENTS = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
COMP_SIGN = {"new_edge_rate": 1, "n_comm_W3": 1, "participation": 1, "NOV_res": 1, "ego_density_W3": -1,
             "edge_persistence": -1}


def rel(p: Path) -> str:
    """Run-relative path string (never an absolute server path in published files)."""
    p = Path(p).resolve()
    try:
        return str(p.relative_to(RUN.parent))
    except ValueError:
        try:
            return str(p.relative_to(WS))
        except ValueError:
            return p.name


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def jdump(obj, path: Path) -> None:
    def conv(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, np.ndarray):
            return [conv(x) for x in o.tolist()]
        if isinstance(o, float) and not math.isfinite(o):
            return None
        if isinstance(o, dict):
            return {str(k): conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [conv(x) for x in o]
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return o
    Path(path).write_text(json.dumps(conv(obj), indent=1))


def assert_sealed() -> None:
    """No Part B statistic may be computed before logs/seal.log exists (plan Step 0)."""
    s = LOGS / "seal.log"
    assert s.exists() and "sha256" in s.read_text(), "Part B blocked: logs/seal.log missing (run seal.py first)"
    spec = json.loads((RES / "boundary_spec.json").read_text())
    line = [l for l in s.read_text().splitlines() if l.startswith("sha256")][-1]
    assert line.split()[1] == sha256(RES / "boundary_spec.json"), "boundary_spec.json changed after the seal"
    return spec


# ----------------------------------------------------------------------------- estimators
def dummies(v: np.ndarray) -> np.ndarray:
    u = np.unique(v)
    if len(u) <= 1:
        return np.zeros((len(v), 0))
    return (v[:, None] == u[1:][None, :]).astype(float)


def rank(a: np.ndarray) -> np.ndarray:
    from scipy.stats import rankdata
    return rankdata(a, axis=0)


def design(Bc: np.ndarray | None, cat: np.ndarray | None, n: int) -> np.ndarray:
    Z = [np.ones((n, 1))]
    if Bc is not None and Bc.shape[1]:
        Z.append(rank(Bc))
    if cat is not None and cat.shape[1]:
        Z.append(cat)
    return np.hstack(Z)


def resid(Z: np.ndarray, Y: np.ndarray) -> np.ndarray:
    beta, *_ = np.linalg.lstsq(Z, Y, rcond=None)
    return Y - Z @ beta


def cat_for(t0: np.ndarray, group: np.ndarray, unit: str, t0_dummies: bool = True) -> np.ndarray:
    parts = [dummies(t0)] if t0_dummies else [np.zeros((len(t0), 0))]
    if unit.startswith("COH") or unit == "POOL6":
        parts.append(dummies(group))
    return np.hstack(parts)


def dl(z, v) -> dict:
    """DerSimonian-Laird on Fisher z with variances v; adds a 95% prediction interval (Higgins et al. 2009)."""
    from scipy import stats
    z, v = np.asarray(z, float), np.asarray(v, float)
    ok = np.isfinite(z) & np.isfinite(v) & (v > 0)
    z, v = z[ok], v[ok]
    k = len(z)
    if k == 0:
        return {"k": 0}
    w = 1 / v
    zf = (w * z).sum() / w.sum()
    Q = float((w * (z - zf) ** 2).sum())
    c = w.sum() - (w ** 2).sum() / w.sum()
    t2 = max(0.0, (Q - (k - 1)) / c) if k > 1 and c > 0 else 0.0
    ws = 1 / (v + t2)
    m = float((ws * z).sum() / ws.sum())
    s = float(math.sqrt(1 / ws.sum()))
    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 and k > 1 else 0.0
    if k >= 3:
        tq = stats.t.ppf(0.975, k - 2)
        h = tq * math.sqrt(t2 + s ** 2)
        pi = [math.tanh(m - h), math.tanh(m + h)]
    else:
        pi = [float("nan")] * 2
    return {"k": k, "est": math.tanh(m), "z": m, "se_z": s, "ci": [math.tanh(m - 1.96 * s), math.tanh(m + 1.96 * s)],
            "p": float(2 * stats.norm.sf(abs(m / s))), "tau2": t2, "I2": I2, "Q": Q,
            "Q_p": float(stats.chi2.sf(Q, k - 1)) if k > 1 else float("nan"), "pi": pi,
            "n_pos": int((z > 0).sum()), "n_neg": int((z < 0).sum())}


def holm(p) -> list[float]:
    p = np.asarray(p, float)
    out = np.full(len(p), np.nan)
    idx = np.nonzero(np.isfinite(p))[0]
    m = len(idx)
    run = 0.0
    for r, i in enumerate(idx[np.argsort(p[idx])]):
        run = max(run, min(1.0, (m - r) * p[i]))
        out[i] = run
    return out.tolist()


# ----------------------------------------------------------------------------- ledger
class Ledger:
    """num(src, key_path, fmt) reads the value from the named file, formats it and appends a ledger row.

    key_path syntax: JSON dotted/indexed path ('a.b[0].c'), CSV 'filter::column' where filter is
    'col==value&col2==value2', or MD '::block::token' (verbatim carry-over)."""

    def __init__(self) -> None:
        self.rows: list[dict] = []
        self._cache: dict = {}

    def _load(self, src: Path):
        if src not in self._cache:
            if not src.exists():
                self._cache[src] = None
            elif src.suffix == ".json":
                self._cache[src] = json.loads(src.read_text())
            elif src.suffix == ".csv":
                import pandas as pd
                self._cache[src] = pd.read_csv(src)
            else:
                self._cache[src] = src.read_text()
        return self._cache[src]

    @staticmethod
    def json_get(obj, path: str):
        import re
        for tok in re.findall(r"\['[^']+'\]|\[\d+\]|[^.\[\]]+", path):
            if tok.startswith("['"):
                obj = obj[tok[2:-2]]
            elif tok.startswith("["):
                obj = obj[int(tok[1:-1])]
            else:
                obj = obj[tok]
        return obj

    @staticmethod
    def csv_get(df, path: str):
        filt, col = path.rsplit("::", 1)
        m = np.ones(len(df), bool)
        if filt:
            for cond in filt.split("&"):
                c, v = cond.split("==", 1)
                s = df[c].astype(str)
                m &= (s == v).to_numpy()
        vals = df.loc[m, col]
        if len(vals) != 1:
            raise KeyError(f"{path}: {len(vals)} rows")
        return vals.iloc[0]

    def get(self, src: Path, key_path: str):
        obj = self._load(src)
        if obj is None:
            raise FileNotFoundError(src)
        if src.suffix == ".json":
            return self.json_get(obj, key_path)
        if src.suffix == ".csv":
            return self.csv_get(obj, key_path)
        raise KeyError(key_path)

    @staticmethod
    def tolerance(txt: str) -> float:
        """Half a unit in the last reported digit (handles 1.2e-05 style and thousands separators)."""
        t = txt.replace(",", "").replace("+", "").replace("%", "").lower()
        mant, _, ex = t.partition("e")
        dec = len(mant.split(".")[1]) if "." in mant else 0
        return 0.5 * 10 ** (-dec + (int(ex) if ex else 0)) * 1.0000001

    def num(self, src: Path, key_path: str, fmt: str = "{:.3f}", *, section: str = "", snippet: str = "",
            scale: float = 1.0, target_file: str = "") -> str:
        try:
            v = self.get(Path(src), key_path)
            if v is None:
                raise ValueError("null value")
            fv = float(v) * scale if not isinstance(v, bool) else float(v)
            txt = fmt.format(fv)
            rv = float(txt.replace(",", "").replace("+", "").replace("%", ""))
            tol = self.tolerance(txt)
            diff = abs(rv - fv) if np.isfinite(fv) else float("nan")
            status = "MATCH" if diff <= 1e-12 else ("ROUNDING_ONLY" if diff <= tol else "MISMATCH")
        except (FileNotFoundError, KeyError, IndexError, TypeError, ValueError) as e:
            txt, fv, rv, diff, tol, status = "NOT_FOUND", float("nan"), float("nan"), float("nan"), float("nan"), "NOT_FOUND"
        self.rows.append({"claim_id": f"C{len(self.rows)+1:04d}", "target_file": target_file, "target_section": section,
                          "text_snippet": snippet[:160], "reported_value": txt, "source_file": rel(Path(src)),
                          "key_path": key_path, "file_value": fv, "abs_diff": diff, "tolerance": tol,
                          "status": status, "scale": scale, "fmt": fmt, "kind": "value"})
        return txt

    NUM_RE = r"(?<![\w.])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:e[-+]?\d+)?(?![\w])"

    def carry(self, src: Path, key_path: str, source_text: str, text: str, *, section: str = "",
              target_file: str = "") -> str:
        """Verbatim carry-over: every numeric token of `text` must occur in `source_text` (the block/row/field named
        by key_path in src). One ledger row per token; returns text unchanged."""
        import re
        src_tokens = set(re.findall(self.NUM_RE, source_text))
        for tok in re.findall(self.NUM_RE, text):
            ok = tok in src_tokens
            self.rows.append({"claim_id": f"C{len(self.rows)+1:04d}", "target_file": target_file,
                              "target_section": section, "text_snippet": f"verbatim carry-over token {tok}",
                              "reported_value": tok, "source_file": rel(Path(src)), "key_path": key_path,
                              "file_value": tok if ok else "", "abs_diff": 0.0 if ok else float("nan"),
                              "tolerance": 0.0, "status": "MATCH" if ok else "MISMATCH", "scale": 1.0, "fmt": "verbatim",
                              "kind": "carry"})
        return text

    def write(self, path: Path) -> None:
        cols = list(self.rows[0].keys())
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(self.rows)
