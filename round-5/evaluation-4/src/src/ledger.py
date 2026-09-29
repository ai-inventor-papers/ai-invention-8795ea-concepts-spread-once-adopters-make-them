"""Claims ledger (same schema as Eval3 claims_ledger_v3.csv). Adapted from Eval3 lib/common.Ledger.

num(src, key_path, fmt) reads the value from the named file, formats it and appends a 'value' row.
carry(src, key_path, text) appends one 'carry' row per numeric token of a verbatim text; key_path forms the verifier
understands: a JSON path to a string, or 'lines:a-b' (1-based inclusive line slice of a text file)."""
from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path

import numpy as np

from paths import rel

NUM_RE = r"(?<![\w.])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:e[-+]?\d+)?(?![\w])"


class Ledger:
    def __init__(self) -> None:
        self.rows: list[dict] = []
        self._cache: dict = {}
        self.target_file = ""
        self.section = ""

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
        idx = None
        mm = re.match(r"(.+)\[(\d+)\]$", col)
        if mm:
            col, idx = mm.group(1), int(mm.group(2))
        m = np.ones(len(df), bool)
        for cond in [c for c in filt.split("&") if c]:
            c, v = cond.split("==", 1)
            m &= (df[c].astype(str) == v).to_numpy()
        vals = df.loc[m, col]
        if len(vals) != 1:
            raise KeyError(f"{path}: {len(vals)} rows")
        v = vals.iloc[0]
        return json.loads(v)[idx] if idx is not None else v

    def get(self, src: Path, key_path: str):
        obj = self._load(Path(src))
        if obj is None:
            raise FileNotFoundError(src)
        if Path(src).suffix == ".json":
            return self.json_get(obj, key_path)
        if Path(src).suffix == ".csv":
            return self.csv_get(obj, key_path)
        raise KeyError(key_path)

    @staticmethod
    def tolerance(txt: str) -> float:
        t = txt.replace(",", "").replace("+", "").replace("%", "").lower()
        mant, _, ex = t.partition("e")
        dec = len(mant.split(".")[1]) if "." in mant else 0
        return 0.5 * 10 ** (-dec + (int(ex) if ex else 0)) * 1.0000001

    def num(self, src: Path, key_path: str, fmt: str = "{:+.3f}", *, scale: float = 1.0, snippet: str = "") -> str:
        try:
            v = self.get(Path(src), key_path)
            if v is None:
                raise ValueError("null value")
            fv = float(v) * scale
            if not math.isfinite(fv):
                raise ValueError("non-finite")
            txt = fmt.format(fv)
            rv = float(txt.replace(",", "").replace("+", "").replace("%", ""))
            tol = self.tolerance(txt)
            diff = abs(rv - fv)
            status = "MATCH" if diff <= 1e-12 else ("ROUNDING_ONLY" if diff <= tol else "MISMATCH")
        except (FileNotFoundError, KeyError, IndexError, TypeError, ValueError):
            txt, fv, diff, tol, status = "NOT_FOUND", float("nan"), float("nan"), float("nan"), "NOT_FOUND"
        self.rows.append({"claim_id": f"V{len(self.rows)+1:04d}", "target_file": self.target_file,
                          "target_section": self.section, "text_snippet": snippet[:160], "reported_value": txt,
                          "source_file": rel(Path(src)), "key_path": key_path, "file_value": fv, "abs_diff": diff,
                          "tolerance": tol, "status": status, "scale": scale, "fmt": fmt, "kind": "value"})
        return txt

    def ci(self, src: Path, key_path: str, fmt: str = "{:+.3f}") -> str:
        """'[lo, hi]' from a 2-element list at key_path."""
        return f"[{self.num(src, key_path + '[0]', fmt)}, {self.num(src, key_path + '[1]', fmt)}]"

    def est_ci(self, src: Path, key: str, est="rho", ci="ci", fmt="{:+.3f}") -> str:
        return f"{self.num(src, f'{key}.{est}', fmt)} {self.ci(src, f'{key}.{ci}', fmt)}"

    @staticmethod
    def source_text(src: Path, key_path: str) -> str:
        if key_path.startswith("lines:"):
            a, b = key_path[6:].split("-")
            return "\n".join(Path(src).read_text().splitlines()[int(a) - 1:int(b)])
        obj = json.loads(Path(src).read_text())
        return str(Ledger.json_get(obj, key_path))

    def carry(self, src: Path, key_path: str, text: str | None = None) -> str:
        """Verbatim carry-over; returns the source text itself when text is None."""
        st = self.source_text(Path(src), key_path)
        text = st if text is None else text
        src_tokens = set(re.findall(NUM_RE, st))
        for tok in re.findall(NUM_RE, text):
            ok = tok in src_tokens
            self.rows.append({"claim_id": f"V{len(self.rows)+1:04d}", "target_file": self.target_file,
                              "target_section": self.section, "text_snippet": f"verbatim carry-over token {tok}",
                              "reported_value": tok, "source_file": rel(Path(src)), "key_path": key_path,
                              "file_value": tok if ok else "", "abs_diff": 0.0 if ok else float("nan"),
                              "tolerance": 0.0, "status": "MATCH" if ok else "MISMATCH", "scale": 1.0,
                              "fmt": "verbatim", "kind": "carry"})
        return text

    def write(self, path: Path) -> None:
        cols = ["claim_id", "target_file", "target_section", "text_snippet", "reported_value", "source_file",
                "key_path", "file_value", "abs_diff", "tolerance", "status", "scale", "fmt", "kind"]
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(self.rows)
