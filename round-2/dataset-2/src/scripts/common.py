"""Shared helpers: paths, logging, label normalisation, polite async HTTP with a disk cache."""
from __future__ import annotations

import asyncio
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
RAW = CACHE / "raw"
WORK = ROOT / "work"          # intermediate tables (parquet/jsonl) produced by the pipeline scripts
OUT = ROOT / "out"            # final deliverables other than data_out*.json
for _d in (CACHE, RAW, WORK, OUT, ROOT / "logs"):
    _d.mkdir(parents=True, exist_ok=True)


def setup_logging(name: str) -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / f"{name}.log", rotation="30 MB", level="DEBUG")


# Wikimedia requires a User-Agent with a contact link (robot policy); no e-mail address is sent.
UA = "AII-research/1.0 (https://github.com/AMGrobelnik; scientometrics research bot, cached, low-rate) aiohttp"

# ----------------------------------------------------------------------------- normalisation
_lemma_cache: dict[str, str] = {}


def _lemma_noun(tok: str) -> str:
    """Singularise the last token with lemminflect (never stems)."""
    if tok in _lemma_cache:
        return _lemma_cache[tok]
    out = tok
    if len(tok) > 3 and tok.isalpha():
        from lemminflect import getLemma
        lem = getLemma(tok, upos="NOUN")
        if lem and lem[0]:
            out = lem[0]
    _lemma_cache[tok] = out
    return out


_PUNCT = re.compile(r"[^\w\s\-+]", flags=re.UNICODE)


def norm_label(s: str | None) -> str:
    """NFKC, casefold, strip possessives and punctuation except - and +, collapse whitespace, lemmatise last token."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s).casefold()
    s = re.sub(r"(\w)['’]s\b", r"\1", s)
    s = _PUNCT.sub(" ", s)
    s = s.replace("_", " ")
    toks = s.split()
    if not toks:
        return ""
    toks[-1] = _lemma_noun(toks[-1])
    return " ".join(toks)


def acronyms(aliases: list[str]) -> list[str]:
    return sorted({a for a in aliases if a and len(a) <= 6 and re.fullmatch(r"[A-Z0-9\-]+", a) and
                   any(c.isalpha() for c in a)})


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cgroup_ram_gb() -> float:
    try:
        v = Path("/sys/fs/cgroup/memory.max").read_text().strip()
        if v != "max":
            return int(v) / 1e9
    except (FileNotFoundError, ValueError):
        pass
    return 16.0


def set_ram_limit(gb: float) -> None:
    import resource
    b = int(gb * 1e9)
    resource.setrlimit(resource.RLIMIT_AS, (b, b))


MAXLAG_EVENTS = {"n": 0}


class Pace:
    """Global adaptive request pacer (AIMD): one slot every 1/rate s; a 429 pauses everyone for Retry-After and
    cuts the rate by 30%; every 300 successes raise it by 5% up to max_rate."""

    def __init__(self, rate: float, max_rate: float, min_rate: float = 0.5) -> None:
        import time
        self.rate, self.max_rate, self.min_rate = rate, max_rate, min_rate
        self.next_t = time.monotonic()
        self.lock = asyncio.Lock()
        self.ok = 0
        self.n429 = 0

    async def wait(self) -> None:
        import time
        async with self.lock:
            now = time.monotonic()
            t = max(now, self.next_t)
            self.next_t = t + 1.0 / self.rate
        await asyncio.sleep(max(0.0, t - time.monotonic()))

    def success(self) -> None:
        self.ok += 1
        if self.ok % 300 == 0:
            self.rate = min(self.max_rate, self.rate * 1.05)

    def throttled(self, retry_after: float) -> None:
        import time
        self.n429 += 1
        self.rate = max(self.min_rate, self.rate * 0.7)
        self.next_t = max(self.next_t, time.monotonic() + retry_after)


async def get_json(session, url: str, params: dict, sem: asyncio.Semaphore, *, tries: int = 8, maxlag_tries: int = 40,
                   pace: "Pace | None" = None):
    """GET with maxlag / 429 / 5xx backoff. maxlag errors (HTTP 200, error.code=maxlag) are retried patiently
    (Retry-After or 5 s, up to maxlag_tries) and counted; other failures back off exponentially."""
    import aiohttp
    delay = 2.0
    n_err = n_lag = 0
    params = {k: str(v) for k, v in params.items()}
    import time as _t
    if "maxlag" in params and _t.time() - MAXLAG_EVENTS.get("last_drop", 0) < 60:
        # lag was persistent within the last minute: skip maxlag (re-probed once the minute has passed)
        params = {k: v for k, v in params.items() if k != "maxlag"}
    while n_err < tries and n_lag < maxlag_tries:
        if pace is not None:
            await pace.wait()
        async with sem:
            try:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=60, sock_connect=15,
                                                                                          sock_read=45)) as r:
                    if r.status in (429, 500, 502, 503, 504):
                        ra = r.headers.get("Retry-After")
                        wait = float(ra) if ra and ra.replace(".", "").isdigit() else delay
                        if pace is not None and r.status == 429:
                            pace.throttled(min(wait, 60))
                            if pace.n429 % 20 == 1:
                                logger.warning(f"HTTP 429 (#{pace.n429}); rate now {pace.rate:.2f}/s, pause {wait}s")
                        else:
                            logger.warning(f"HTTP {r.status} retry in {wait}s")
                        n_err += 1
                        delay = min(delay * 2, 60)
                        sleep_for = min(wait, 60)
                    else:
                        r.raise_for_status()
                        d = await r.json(content_type=None)
                        if isinstance(d, dict) and d.get("error", {}).get("code") == "maxlag":
                            n_lag += 1
                            MAXLAG_EVENTS["n"] += 1
                            ra = r.headers.get("Retry-After")
                            sleep_for = float(ra) if ra and ra.isdigit() else 5.0
                            if n_lag >= 3 and "maxlag" in params:
                                # read-only request: after ~15 s of honouring maxlag, send it without maxlag
                                params = {k: v for k, v in params.items() if k != "maxlag"}
                                MAXLAG_EVENTS["dropped"] = MAXLAG_EVENTS.get("dropped", 0) + 1
                                MAXLAG_EVENTS["last_drop"] = __import__("time").time()
                                sleep_for = 0.5
                            if MAXLAG_EVENTS["n"] % 50 == 1:
                                logger.warning(f"maxlag ({MAXLAG_EVENTS['n']} total): {d['error'].get('info', '')[:80]}")
                        else:
                            if pace is not None:
                                pace.success()
                            return d
            except (aiohttp.ClientError, asyncio.TimeoutError, json.JSONDecodeError) as e:
                logger.warning(f"err {type(e).__name__} {str(e)[:150]} attempt {n_err}")
                n_err += 1
                sleep_for = delay
                delay = min(delay * 2, 60)
        await asyncio.sleep(sleep_for)       # sleep outside the semaphore so other workers proceed
    raise RuntimeError(f"failed (errors={n_err}, maxlag={n_lag}): {url} {str(params)[:200]}")
