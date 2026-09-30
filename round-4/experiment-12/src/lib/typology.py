"""Trajectory typology: DTW k-medoids (EXP6 lib/traj.py dtw_matrix / kmed / choose_k logic), Gaussian HMM
partition, Hennig (2007) cluster-wise bootstrap Jaccard, the frozen naming rule, and the PCA continuum fallback."""
from __future__ import annotations

import math
import warnings

import numpy as np
from sklearn.metrics import adjusted_rand_score, silhouette_score

VARS = ["new_entries", "n_ent_off", "n_ret", "n_lost", "ret_share", "frontier", "H", "home_share", "comm_span"]
ASINH_VARS = ["new_entries", "n_ent_off", "n_ret", "n_lost", "frontier", "comm_span"]
NAMING = {"ari_dtw_hmm": 0.5, "jaccard": 0.75, "ari_nomed": 0.5, "min_share_nomed": 0.05, "ari_heldout": 0.5,
          "ari_volume_max": 0.5}


# ----------------------------------------------------------------------------- inputs
def build_X(P, cis: np.ndarray, ages=range(0, 9)) -> np.ndarray:
    """P: panel.parquet frame. Returns raw [n, len(ages), len(VARS)] (asinh on counts; NaN-filled)."""
    import pandas as pd
    Q = P[P.age.isin(list(ages))].set_index(["ci", "age"]).sort_index()
    X = np.stack([Q[v].unstack("age").loc[cis].to_numpy(float) for v in VARS], axis=2)  # [n, T, V]
    for j, v in enumerate(VARS):
        if v in ASINH_VARS:
            X[:, :, j] = np.arcsinh(X[:, :, j])
    for j, v in enumerate(VARS):   # H / home_share are NaN when the 3-yr window has no labelled paper
        x = pd.DataFrame(X[:, :, j]).ffill(axis=1).bfill(axis=1).to_numpy()
        X[:, :, j] = np.nan_to_num(x, nan=1.0 if v == "home_share" else 0.0)
    return X


def zspec_fit(X: np.ndarray) -> dict:
    return {v: [float(X[:, :, j].mean()), float(X[:, :, j].std() or 1.0)] for j, v in enumerate(VARS)}


def zapply(X: np.ndarray, zs: dict) -> np.ndarray:
    return np.stack([(X[:, :, j] - zs[v][0]) / zs[v][1] for j, v in enumerate(VARS)], axis=2)


# ----------------------------------------------------------------------------- DTW k-medoids
def _dtw_kernel():
    import numba

    @numba.njit(cache=False, fastmath=False)
    def dtw_pair(a, b, r):
        T1, T2, d = a.shape[0], b.shape[0], a.shape[1]
        C = np.full((T1 + 1, T2 + 1), np.inf)
        C[0, 0] = 0.0
        for i in range(1, T1 + 1):
            lo = max(1, i - r)
            hi = min(T2, i + r)
            for j in range(lo, hi + 1):
                s = 0.0
                for k in range(d):
                    t = a[i - 1, k] - b[j - 1, k]
                    s += t * t
                m = C[i - 1, j - 1]
                if C[i - 1, j] < m:
                    m = C[i - 1, j]
                if C[i, j - 1] < m:
                    m = C[i, j - 1]
                C[i, j] = s + m
        return np.sqrt(C[T1, T2])

    @numba.njit(parallel=True)
    def cdist(A, B, r, sym):
        n, m = A.shape[0], B.shape[0]
        D = np.zeros((n, m))
        for i in numba.prange(n):
            j0 = i + 1 if sym else 0
            for j in range(j0, m):
                D[i, j] = dtw_pair(A[i], B[j], r)
        if sym:
            for i in range(n):
                for j in range(i + 1, m):
                    D[j, i] = D[i, j]
        return D
    return cdist


_CDIST = None


def dtw_matrix(Z: np.ndarray, radius: int = 2, n_jobs: int = 16, Z2: np.ndarray | None = None) -> np.ndarray:
    """multivariate DTW (squared-Euclidean local cost, sqrt of the accumulated cost) with a Sakoe-Chiba band of
    `radius` -- the tslearn cdist_dtw definition used by EXP6, re-implemented as a numba-parallel kernel
    (tslearn's per-pair joblib dispatch projected 61 min for 4,771 DEV concepts). Verified against tslearn in T0."""
    global _CDIST
    import numba
    numba.set_num_threads(max(1, min(n_jobs, numba.config.NUMBA_NUM_THREADS)))
    if _CDIST is None:
        _CDIST = _dtw_kernel()
    A = np.ascontiguousarray(Z, dtype=np.float64)
    if Z2 is None:
        return _CDIST(A, A, radius, True)
    return _CDIST(A, np.ascontiguousarray(Z2, dtype=np.float64), radius, False)


def dtw_matrix_tslearn(Z: np.ndarray, radius: int = 2, n_jobs: int = 4, Z2: np.ndarray | None = None) -> np.ndarray:
    from tslearn.metrics import cdist_dtw
    return cdist_dtw(Z, Z2, global_constraint="sakoe_chiba", sakoe_chiba_radius=radius, n_jobs=n_jobs)


def kmed(D: np.ndarray, k: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    import kmedoids
    r = kmedoids.fasterpam(D, k, random_state=seed, max_iter=300, init="build", n_cpu=1)
    return np.asarray(r.labels), np.asarray(r.medoids)


def _boot_fit(D, idx, k, seed):
    lb, _ = kmed(np.ascontiguousarray(D[np.ix_(idx, idx)]), k, seed)
    return lb


def choose_k(D: np.ndarray, seed: int, ks=range(2, 9), n_boot: int = 100, n_jobs: int = 24) -> dict:
    """EXP6 choose_k logic (median ARI of 100 x 80% subsample refits >= 0.6, then max silhouette), with the refits
    run in parallel (single-threaded fasterpam per job)."""
    from joblib import Parallel, delayed
    rng = np.random.default_rng(seed)
    n = len(D)
    ks = list(ks)
    subs = [np.sort(rng.choice(n, int(0.8 * n), replace=False)) for _ in range(n_boot)]
    full = Parallel(n_jobs=min(n_jobs, len(ks)))(delayed(kmed)(D, k, seed) for k in ks)
    jobs = [(k, b) for k in ks for b in range(n_boot)]
    fits = Parallel(n_jobs=n_jobs, batch_size=4)(delayed(_boot_fit)(D, subs[b], k, seed + b + 1) for k, b in jobs)
    res = {}
    for i, k in enumerate(ks):
        lab = full[i][0]
        sil = float(silhouette_score(D, lab, metric="precomputed")) if len(set(lab)) > 1 else float("nan")
        aris = [adjusted_rand_score(lab[subs[b]], fits[j]) for j, (kk, b) in enumerate(jobs) if kk == k]
        res[k] = {"silhouette": sil, "ari_median": float(np.median(aris)), "ari_p10": float(np.percentile(aris, 10)),
                  "sizes": np.bincount(lab).tolist()}
    ok = [k for k, v in res.items() if v["ari_median"] >= 0.6]
    if ok:
        kbest, flag = max(ok, key=lambda k: res[k]["silhouette"]), "stable"
    else:
        kbest, flag = max(res, key=lambda k: res[k]["silhouette"]), "unstable (no k with median bootstrap ARI >= 0.6)"
    return {"grid": res, "k": kbest, "flag": flag}


def gap_statistic(F: np.ndarray, ks=range(1, 9), n_ref: int = 10, seed: int = 0) -> dict:
    """Tibshirani gap on the flattened (Euclidean) vectors with KMeans, uniform reference in the PCA box."""
    from sklearn.cluster import KMeans
    rng = np.random.default_rng(seed)
    Fc = F - F.mean(0)
    _, _, Vt = np.linalg.svd(Fc, full_matrices=False)
    Xp = Fc @ Vt.T
    lo, hi = Xp.min(0), Xp.max(0)

    def logW(A, k):
        km = KMeans(k, n_init=3, random_state=seed).fit(A)
        return math.log(km.inertia_)
    out = {}
    for k in ks:
        lw = logW(F, k)
        ref = [logW(rng.uniform(lo, hi, size=Xp.shape) @ Vt, k) for _ in range(n_ref)]
        out[k] = {"gap": float(np.mean(ref) - lw), "sk": float(np.std(ref) * math.sqrt(1 + 1 / n_ref))}
    kk = sorted(out)
    k_gap = next((k for k, k2 in zip(kk, kk[1:]) if out[k]["gap"] >= out[k2]["gap"] - out[k2]["sk"]), kk[-1])
    return {"grid": out, "k_gap": k_gap}


def hennig_jaccard(D: np.ndarray, labels: np.ndarray, k: int, seed: int, n_boot: int = 100, n_jobs: int = 24) -> dict:
    """clusterboot: bootstrap resample (distinct points), recluster, Jaccard of each original cluster (restricted
    to the resampled points) with its best-matching resampled cluster; mean over resamples per cluster."""
    from joblib import Parallel, delayed
    rng = np.random.default_rng(seed)
    n = len(D)
    idxs = [np.unique(rng.integers(0, n, n)) for _ in range(n_boot)]
    fits = Parallel(n_jobs=n_jobs, batch_size=2)(delayed(_boot_fit)(D, idx, k, seed + 1000 + b)
                                                 for b, idx in enumerate(idxs))
    J = np.full((n_boot, k), np.nan)
    for b, (idx, lb) in enumerate(zip(idxs, fits)):
        lo = labels[idx]
        for c in range(k):
            A = lo == c
            if not A.any():
                continue
            J[b, c] = max(((A & (lb == d)).sum() / (A | (lb == d)).sum()) for d in range(k))
    return {"mean_jaccard": np.nanmean(J, 0).tolist(), "n_boot": n_boot}


# ----------------------------------------------------------------------------- HMM partition
def hmm_fit(Z: np.ndarray, seed: int, states=(3, 4, 5), restarts: int = 10, n_iter: int = 200) -> dict:
    from hmmlearn.hmm import GaussianHMM
    X = Z.reshape(-1, Z.shape[2])
    L = [Z.shape[1]] * Z.shape[0]
    grid, best = {}, None
    for s in states:
        cand = []
        for r in range(restarts):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                m = GaussianHMM(n_components=s, covariance_type="diag", n_iter=n_iter, random_state=seed + 97 * r,
                                min_covar=1e-3).fit(X, L)
            ll = m.score(X, L)
            cand.append((ll, r, m))
        ll, r, m = max(cand, key=lambda t: t[0])
        p = s * (s - 1) + (s - 1) + 2 * s * Z.shape[2]
        bic = -2 * ll + p * math.log(len(X))
        grid[s] = {"ll": float(ll), "bic": float(bic), "best_restart": r, "converged": bool(m.monitor_.converged),
                   "ll_restarts": [float(c[0]) for c in cand], "state_occupancy": None}
        if best is None or bic < best[1]:
            best = (s, bic, m)
    s, _, m = best
    return {"grid": grid, "n_states": s, "model": m}


def hmm_features(m, Z: np.ndarray) -> np.ndarray:
    """[posterior state occupancy per age (T x S) + final-state one-hot] per concept."""
    S = m.n_components
    post = np.stack([m.predict_proba(z) for z in Z])            # [n, T, S]
    fin = np.eye(S)[post[:, -1, :].argmax(1)]
    return np.concatenate([post.reshape(len(Z), -1), fin], axis=1)


def euclid(F: np.ndarray) -> np.ndarray:
    sq = (F ** 2).sum(1)
    D = np.sqrt(np.maximum(sq[:, None] + sq[None, :] - 2 * F @ F.T, 0))
    np.fill_diagonal(D, 0)
    return D


# ----------------------------------------------------------------------------- PCA continuum
def pca_fit(Z: np.ndarray, max_pc: int = 3, min_var: float = 0.10) -> dict:
    F = Z.reshape(len(Z), -1)
    mu = F.mean(0)
    U, s, Vt = np.linalg.svd(F - mu, full_matrices=False)
    ev = s ** 2 / (s ** 2).sum()
    keep = max(1, min(max_pc, int((ev >= min_var).sum())))
    return {"mean": mu, "components": Vt[:keep], "explained": ev[:10].tolist(), "keep": keep}


def pca_project(Z: np.ndarray, pc: dict) -> np.ndarray:
    return (Z.reshape(len(Z), -1) - pc["mean"]) @ pc["components"].T


def naming_rule(ari_dtw_hmm: float, jacc: list[float], ari_nomed: float, share_nomed: list[float],
                ari_vol: float, ari_heldout: float | None) -> dict:
    """per class: NAMED only if all five conditions hold ((4) evaluated after the unseal; None = pending)."""
    k = len(jacc)
    out = {"conditions": {"1_ari_dtw_hmm": ari_dtw_hmm >= NAMING["ari_dtw_hmm"],
                          "3_ari_nomed": ari_nomed >= NAMING["ari_nomed"],
                          "4_ari_heldout": None if ari_heldout is None else ari_heldout >= NAMING["ari_heldout"],
                          "5_not_volume_class": ari_vol < NAMING["ari_volume_max"]},
           "per_class": []}
    glob = [v for v in out["conditions"].values() if v is not None]
    for c in range(k):
        ok_c = jacc[c] >= NAMING["jaccard"] and share_nomed[c] >= NAMING["min_share_nomed"]
        out["per_class"].append({"class": c, "jaccard": jacc[c], "share_nonMed": share_nomed[c],
                                 "named": bool(all(glob) and ok_c and out["conditions"]["4_ari_heldout"] is not False)})
    out["any_named"] = any(p["named"] for p in out["per_class"])
    out["pending_heldout"] = ari_heldout is None
    return out


# ----------------------------------------------------------------------------- split DTW cache (GitHub 100 MB limit)
MAX_PART_BYTES = 80 * 1024 * 1024


def save_matrix_parts(D: np.ndarray, cache_dir, name: str) -> list:
    """save a matrix as row-chunk parts <name>_part_001.npy, ... each <= MAX_PART_BYTES."""
    from pathlib import Path
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    for old in cache_dir.glob(f"{name}_part_*.npy"):
        old.unlink()
    rows = max(1, MAX_PART_BYTES // max(1, D.shape[1] * D.itemsize))
    paths = []
    for k, i in enumerate(range(0, D.shape[0], rows), start=1):
        p = cache_dir / f"{name}_part_{k:03d}.npy"
        np.save(p, D[i:i + rows])
        paths.append(p)
    return paths


def load_matrix_parts(cache_dir, name: str) -> np.ndarray | None:
    """concatenate the sorted row-chunk parts; None if the cache is absent."""
    from pathlib import Path
    parts = sorted(Path(cache_dir).glob(f"{name}_part_*.npy"))
    if not parts:
        return None
    return np.concatenate([np.load(p) for p in parts], axis=0)
