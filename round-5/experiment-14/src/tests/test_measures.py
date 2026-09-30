"""U2-U4 (+U8): Cheng measure unit tests on synthetic inputs. Run: uv run pytest tests/ -q"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

import cheng  # noqa: E402
import ego  # noqa: E402


def _ctx(nt: int = 6) -> None:
    ego.set_context({"nt": nt, "years": [], "bg": np.zeros((0, nt)), "Gt": {}, "lemmas": lambda s: set(),
                     "ldf": {}, "tlem": [set()] * nt})


def test_u2_cons_values() -> None:
    v = np.array([2.0, 0.0, 1.0])
    assert math.isclose(cheng.cons(v, v, 5, 5)[0], 1.0)
    a, b = np.array([1.0, 1.0, 0, 0]), np.array([0, 0, 1.0, 1.0])
    assert cheng.cons(a, b, 5, 5)[0] == 0.0
    c, cr = cheng.cons(np.array([2.0, 0.0, 1.0]), np.array([1.0, 1.0, 1.0]), 4, 4)
    assert math.isclose(c, 3 / math.sqrt(15))
    assert math.isclose(cr, 3 / (math.sqrt(5) * math.sqrt(2)))       # Cheng-verbatim support restriction
    assert math.isnan(cheng.cons(v, v, 2, 5)[0])                    # < 3 papers
    assert math.isnan(cheng.cons(np.array([3.0, 0, 0]), np.array([3.0, 1.0, 0]), 5, 5)[0])  # < 2 topics


def _paper_arrays(papers):
    years = np.array([p[0] for p in papers], np.int64)
    vfield = np.array([p[1] for p in papers], np.int64)
    t_off = np.r_[0, np.cumsum([len(p[2]) for p in papers])].astype(np.int64)
    tflat = np.concatenate([np.array(p[2], np.int64) for p in papers])
    a_off = np.r_[0, np.cumsum([len(p[3]) for p in papers])].astype(np.int64)
    aflat = np.concatenate([np.array(p[3], np.int64) for p in papers])
    return years, vfield, t_off, tflat, a_off, aflat


def test_u2_self_excluded_and_u8_home() -> None:
    _ctx(6)
    cheng.set_pmi_for_tests({s: sp.csr_matrix((6, 6)) for s in range(3)})
    # topic 5 is SELF; HOME = vfield 7
    papers = [(2009, 7, [0, 5], [1]), (2009, 7, [1, 5], [2]), (2009, 7, [0, 1], [3]), (2009, 3, [4], [9]),
              (2010, 7, [0, 5], [1]), (2010, 7, [1, 5], [2]), (2010, 7, [0, 1, 5], [3]), (2010, 3, [4, 2], [9])]
    y, vf, to, tf, ao, af = _paper_arrays(papers)
    self_ = np.zeros(6, bool)
    self_[5] = True
    rows = cheng.concept_measures(ci=1, name="x", aliases=[], t0=2010, y_lo=2010, y_hi=2010, years=y, vfield=vf,
                                  t_off=to, tflat=tf, a_off=ao, aflat=af, home={7}, want_self=self_)
    h = [r for r in rows if r["build"] == "HOME"][0]
    a = [r for r in rows if r["build"] == "ALL"][0]
    assert h["n_papers"] == 3 and a["n_papers"] == 4                 # U8: HOME = rows with vfield in home set
    assert math.isclose(h["CONS"], 1.0)                              # SELF topic 5 excluded -> identical (2,2)
    va, vb = np.array([2, 2, 0, 0, 1.0]), np.array([2, 2, 1, 0, 1.0])
    assert math.isclose(a["CONS"], va @ vb / (np.linalg.norm(va) * np.linalg.norm(vb)))


def test_u3_soc() -> None:
    adj = {1: {2}, 2: {1, 3}, 3: {2}}                                # ties 1-2, 2-3
    assert math.isclose(cheng.soc_density([1, 2, 3, 4], [adj]), 2 / 6)
    assert math.isnan(cheng.soc_density([1, 2], [adj]))
    _ctx(4)
    cheng.set_pmi_for_tests({s: sp.csr_matrix((4, 4)) for s in range(3)})
    # prior-year paper ties authors 1-2 and 2-3; year-t paper ties 1-4 only (must not count)
    papers = [(2009, 7, [0, 1], [1, 2]), (2009, 7, [0, 1], [2, 3]), (2009, 7, [0, 2], [5]),
              (2010, 7, [0, 1], [1, 4]), (2010, 7, [0, 2], [2]), (2010, 7, [1, 2], [3])]
    y, vf, to, tf, ao, af = _paper_arrays(papers)
    rows = cheng.concept_measures(ci=1, name="x", aliases=[], t0=2010, y_lo=2010, y_hi=2010, years=y, vfield=vf,
                                  t_off=to, tflat=tf, a_off=ao, aflat=af, home={7},
                                  want_self=np.zeros(4, bool))
    h = [r for r in rows if r["build"] == "HOME"][0]
    assert h["n_authors"] == 4 and math.isclose(h["SOC"], 2 / 6)
    # papers with > 15 authors are ignored
    big = list(range(100, 117))
    papers2 = [(2009, 7, [0, 1], big), (2010, 7, [0, 1], [100, 101]), (2010, 7, [0, 2], [102]),
               (2010, 7, [1, 2], [103]), (2009, 7, [0, 2], [5]), (2009, 7, [1, 2], [6])]
    y, vf, to, tf, ao, af = _paper_arrays(papers2)
    rows = cheng.concept_measures(ci=1, name="x", aliases=[], t0=2010, y_lo=2010, y_hi=2010, years=y, vfield=vf,
                                  t_off=to, tflat=tf, a_off=ao, aflat=af, home={7},
                                  want_self=np.zeros(4, bool))
    assert [r for r in rows if r["build"] == "HOME"][0]["SOC"] == 0.0


def test_u4_emb() -> None:
    W = np.zeros((3, 3))
    W[0, 1] = W[1, 0] = 1.0
    W[1, 2] = W[2, 1] = 2.0                                         # no 0-2 edge (PMI+ = 0)
    cheng.set_pmi_for_tests({s: sp.csr_matrix(W) for s in range(3)})
    v = np.array([1.0, 2.0, 3.0])
    e, ec = cheng.emb(v, 5, 0)
    # weights v_k v_l: (0,1)=2, (0,2)=3, (1,2)=6 ; PMI 1, 0, 2 -> (2*1 + 0 + 6*2)/11
    assert math.isclose(e, 14 / 11)
    Xn = W / np.linalg.norm(W, axis=1, keepdims=True)
    G = Xn @ Xn.T
    assert math.isclose(ec, (G[0, 1] + G[0, 2] + G[1, 2]) / 3)
    assert math.isnan(cheng.emb(np.array([1.0, 0, 0]), 5, 0)[0])
