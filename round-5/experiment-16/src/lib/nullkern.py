"""Numba kernels for the configuration nulls.

curveball_run   Strona et al. (2014) curveball chain on a bipartite incidence stored as fixed-size rows (row sums
                preserved by construction, column sums preserved by each trade); all calendar years advance in
                lockstep so sample d of year t0 and sample d of year t0+1 are combined for a concept's Jaccards.
ksets_null      V3b: random sets of size k drawn without replacement with probability proportional to weights
                (successive sampling == Gumbel top-k), SELF topics excluded; counts edges in a dense adjacency.
kpers_null      V3c-approx: k-matched Monte Carlo persistence null (row sizes k1, k2, k3; weights = column
                popularity in each window's year)."""
from __future__ import annotations

import numpy as np
from numba import njit


@njit(cache=True)
def _trade(data, off, i, j, mark, stamp, pool):
    a0, a1 = off[i], off[i + 1]
    b0, b1 = off[j], off[j + 1]
    if a1 == a0 or b1 == b0:
        return
    for p in range(a0, a1):
        mark[data[p]] = stamp
    # B-only and shared
    nb_only = 0
    ns = 0
    for p in range(b0, b1):
        if mark[data[p]] == stamp:
            ns += 1
        else:
            pool[nb_only] = data[p]
            nb_only += 1
    na = (a1 - a0) - ns
    if na == 0 or nb_only == 0:
        return
    # mark B elements with stamp + 1 to find A-only
    for p in range(b0, b1):
        mark[data[p]] = stamp + 1
    shared = np.empty(ns, np.int32)
    k = 0
    for p in range(a0, a1):
        x = data[p]
        if mark[x] == stamp + 1:
            shared[k] = x
            k += 1
        else:
            pool[nb_only] = x
            nb_only += 1
    tot = nb_only
    # shuffle the pooled non-shared elements
    for t in range(tot - 1, 0, -1):
        r = np.random.randint(0, t + 1)
        tmp = pool[t]
        pool[t] = pool[r]
        pool[r] = tmp
    # A gets shared + first na; B gets shared + rest
    q = a0
    for t in range(ns):
        data[q] = shared[t]
        q += 1
    for t in range(na):
        data[q] = pool[t]
        q += 1
    q = b0
    for t in range(ns):
        data[q] = shared[t]
        q += 1
    for t in range(na, tot):
        data[q] = pool[t]
        q += 1


@njit(cache=True)
def _jac(data, off, i, j, mark, stamp):
    a0, a1 = off[i], off[i + 1]
    b0, b1 = off[j], off[j + 1]
    for p in range(a0, a1):
        mark[data[p]] = stamp
    inter = 0
    for p in range(b0, b1):
        if mark[data[p]] == stamp:
            inter += 1
    u = (a1 - a0) + (b1 - b0) - inter
    if u == 0:
        return np.nan
    return inter / u


@njit(cache=True)
def curveball_run(data, off, year_lo, year_hi, conc_rows, n_samples, burn_mult, seed, nt):
    """data/off: all rows of all years (rows of year y are year_lo[y]..year_hi[y]-1).
    conc_rows: n_conc x 3 global row ids (W1, W2, W3; -1 = missing). Returns (sum, sumsq, n_finite) of the null
    persistence per concept over n_samples samples."""
    np.random.seed(seed)
    ny = len(year_lo)
    mark = np.zeros(nt + 1, np.int64)
    maxrow = 0
    for r in range(len(off) - 1):
        if off[r + 1] - off[r] > maxrow:
            maxrow = off[r + 1] - off[r]
    pool = np.empty(2 * maxrow + 2, np.int32)
    stamp = 1
    nc = conc_rows.shape[0]
    s1 = np.zeros(nc)
    s2 = np.zeros(nc)
    nf = np.zeros(nc, np.int64)
    for y in range(ny):
        n = year_hi[y] - year_lo[y]
        if n < 2:
            continue
        for t in range(burn_mult * n):
            i = year_lo[y] + np.random.randint(0, n)
            j = year_lo[y] + np.random.randint(0, n)
            if i != j:
                _trade(data, off, i, j, mark, stamp, pool)
                stamp += 2
    for d in range(n_samples):
        for y in range(ny):
            n = year_hi[y] - year_lo[y]
            if n < 2:
                continue
            for t in range(n):
                i = year_lo[y] + np.random.randint(0, n)
                j = year_lo[y] + np.random.randint(0, n)
                if i != j:
                    _trade(data, off, i, j, mark, stamp, pool)
                    stamp += 2
        for c in range(nc):
            r1, r2, r3 = conc_rows[c, 0], conc_rows[c, 1], conc_rows[c, 2]
            j12 = _jac(data, off, r1, r2, mark, stamp)
            stamp += 1
            j23 = _jac(data, off, r2, r3, mark, stamp)
            stamp += 1
            if np.isfinite(j12) and np.isfinite(j23):
                v = (j12 + j23) / 2
            elif np.isfinite(j12):
                v = j12
            elif np.isfinite(j23):
                v = j23
            else:
                continue
            s1[c] += v
            s2[c] += v * v
            nf[c] += 1
    return s1, s2, nf


@njit(cache=True)
def _draw_set(cum, tot, k, selfmark, stamp_self, chosen_mark, stamp, out, nt):
    """Successive sampling of k distinct items proportional to weights (cum = cumulative weights over nt items),
    skipping items marked SELF. Returns False if it cannot fill (pool too small)."""
    got = 0
    tries = 0
    while got < k:
        tries += 1
        if tries > 200 * k + 1000:
            return False
        u = np.random.random() * tot
        x = np.searchsorted(cum, u, side="right")
        if x >= nt:
            x = nt - 1
        if selfmark[x] == stamp_self or chosen_mark[x] == stamp:
            continue
        chosen_mark[x] = stamp
        out[got] = x
        got += 1
    return True


@njit(cache=True)
def ksets_null(set_k, set_conc, set_slice, set_year, self_flat, self_off, cum_w, pool_n, adj, n_draws, seed, nt):
    """For each set s: n_draws random sets of size set_k[s] ~ weights cum_w[set_year[s]] without replacement,
    excluding the SELF topics of concept set_conc[s]; edge counts in adj[set_slice[s]]. Returns mean, sd."""
    np.random.seed(seed)
    ns = len(set_k)
    mu = np.full(ns, np.nan)
    sd = np.full(ns, np.nan)
    selfmark = np.zeros(nt, np.int64)
    chosen = np.zeros(nt, np.int64)
    stamp = 1
    buf = np.empty(nt, np.int64)
    for s in range(ns):
        k = set_k[s]
        c = set_conc[s]
        y = set_year[s]
        if k < 2:
            continue
        for p in range(self_off[c], self_off[c + 1]):
            selfmark[self_flat[p]] = s + 1
        nself_pool = 0
        cum = cum_w[y]
        for p in range(self_off[c], self_off[c + 1]):
            x = self_flat[p]
            w = cum[x] - (cum[x - 1] if x > 0 else 0.0)
            if w > 0:
                nself_pool += 1
        if pool_n[y] - nself_pool < k:
            continue
        tot = cum[nt - 1]
        a = adj[set_slice[s]]
        s1 = 0.0
        s2 = 0.0
        nd = 0
        for d in range(n_draws):
            stamp += 1
            ok = _draw_set(cum, tot, k, selfmark, s + 1, chosen, stamp, buf, nt)
            if not ok:
                continue
            e = 0
            for i in range(k):
                for j in range(i + 1, k):
                    if a[buf[i], buf[j]]:
                        e += 1
            s1 += e
            s2 += e * e
            nd += 1
        if nd >= 2:
            m = s1 / nd
            mu[s] = m
            v = s2 / nd - m * m
            sd[s] = np.sqrt(v) if v > 0 else 0.0
    return mu, sd


@njit(cache=True)
def kpers_null(k3, conc, years3, self_flat, self_off, cum_w, pool_n, n_draws, seed, nt):
    """k-matched persistence null: for row r, windows w = 0..2 with sizes k3[r, w] drawn ~ cum_w[years3[r, w]]
    (SELF of concept conc[r] excluded); null persistence = nanmean(J(1, 2), J(2, 3)). Returns mean, sd."""
    np.random.seed(seed)
    nr = k3.shape[0]
    mu = np.full(nr, np.nan)
    sd = np.full(nr, np.nan)
    selfmark = np.zeros(nt, np.int64)
    chosen = np.zeros(nt, np.int64)
    m2 = np.zeros(nt, np.int64)
    stamp = 1
    b = np.empty((3, nt), np.int64)
    for r in range(nr):
        c = conc[r]
        for p in range(self_off[c], self_off[c + 1]):
            selfmark[self_flat[p]] = r + 1
        feasible = True
        for w in range(3):
            if pool_n[years3[r, w]] - (self_off[c + 1] - self_off[c]) < k3[r, w]:
                feasible = False
        if not feasible:
            continue
        s1 = 0.0
        s2 = 0.0
        nd = 0
        for d in range(n_draws):
            ok = True
            for w in range(3):
                stamp += 1
                cum = cum_w[years3[r, w]]
                if k3[r, w] > 0:
                    if not _draw_set(cum, cum[nt - 1], k3[r, w], selfmark, r + 1, chosen, stamp, b[w], nt):
                        ok = False
            if not ok:
                continue
            js = np.empty(2)
            for q in range(2):
                ka, kb = k3[r, q], k3[r, q + 1]
                stamp += 1
                for i in range(ka):
                    m2[b[q, i]] = stamp
                inter = 0
                for i in range(kb):
                    if m2[b[q + 1, i]] == stamp:
                        inter += 1
                u = ka + kb - inter
                js[q] = inter / u if u > 0 else np.nan
            if np.isfinite(js[0]) and np.isfinite(js[1]):
                v = (js[0] + js[1]) / 2
            elif np.isfinite(js[0]):
                v = js[0]
            elif np.isfinite(js[1]):
                v = js[1]
            else:
                continue
            s1 += v
            s2 += v * v
            nd += 1
        if nd >= 2:
            m = s1 / nd
            mu[r] = m
            vv = s2 / nd - m * m
            sd[r] = np.sqrt(vv) if vv > 0 else 0.0
    return mu, sd
