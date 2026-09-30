"""Stage-0 offline unit tests (no credits)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from features import rarefied_richness, kleinberg_batched


def mc_rarefy(counts, m, draws=100_000, seed=0):
    rng = np.random.default_rng(seed)
    labels = np.repeat(np.arange(len(counts)), counts)
    tot = 0
    for _ in range(draws // 1000):
        idx = np.argsort(rng.random((1000, len(labels))), axis=1)[:, :m]
        s = labels[idx]
        tot += sum(len(np.unique(r)) for r in s)
    return tot / (draws // 1000 * 1000)


def test_rarefaction():
    assert abs(rarefied_richness([10, 10, 10], 1) - 1.0) < 1e-12
    assert abs(rarefied_richness([50], 30) - 1.0) < 1e-12
    assert np.isnan(rarefied_richness([5, 5], 30))
    for c in ([40, 20, 10, 5, 3, 1, 1], [100, 3, 2, 2, 1], [30, 30, 30, 1]):
        ex, mc = rarefied_richness(c, 30), mc_rarefy(c, 30)
        assert abs(ex - mc) < 0.02, (c, ex, mc)


def test_kleinberg_spike():
    r = [10] * 5 + [60] * 3 + [10] * 5
    d = [100000] * len(r)
    st, w = kleinberg_batched(r, d)
    assert st == [0] * 5 + [1] * 3 + [0] * 5, st
    assert w > 0


if __name__ == "__main__":
    test_rarefaction(); test_kleinberg_spike(); print("unit tests passed")
