"""The pool's concurrency properties, as a test rather than as a claim.

Every assertion here failed at least once during the pool's construction, which
is why they are assertions and not prose:

  A  eight requesters racing produced FORTY reps for a target of five, because
     enqueue took a delta and each computed its own deficit before any wrote.
  B  twelve workers double-claimed: `os.rename` succeeded twice for the same
     source on Windows, twelve renames from seven sources.

    python test_pool_concurrency.py
"""
from __future__ import annotations

import collections
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from setup_key import Cell  # noqa: E402
from pool import Pool  # noqa: E402

TMP = HERE.parent / ".pool_selftest"


def cell():
    return Cell.make(task="wf1_crossfile", arm="baseline", backend="ollama",
                     model="selftest", params={}, defaults={"num_ctx": 8192})


def fresh() -> Pool:
    shutil.rmtree(TMP, ignore_errors=True)
    return Pool(TMP)


def test_enqueue_is_idempotent_under_concurrency():
    p, c = fresh(), cell()
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda i: p.enqueue(c, 5, env={}, requested_by=f"r{i}"), range(8)))
    assert p.counts()["pending"] == 5, p.counts()
    assert p.enqueue(c, 5, env={}, requested_by="again") == []
    print("ok  enqueue: 8 racing requesters, target 5 -> exactly 5")


def test_no_double_claim():
    p, c = fresh(), cell()
    p.enqueue(c, 5, env={}, requested_by="r")
    with ThreadPoolExecutor(8) as ex:
        got = [g for g in ex.map(lambda i: p.claim(who=f"w{i}"), range(12)) if g]
    stems = [g.stem for g in got]
    dup = [s for s, n in collections.Counter(stems).items() if n > 1]
    assert not dup, f"double-claimed: {dup}"
    assert len(got) == 5, len(got)
    print("ok  claim: 12 racing workers, 5 items -> 5 claims, none doubled")


def test_held_reps_are_not_requested():
    p, c = fresh(), cell()
    assert p.enqueue(c, 5, env={}, requested_by="r", held=3) == [4, 5]
    print("ok  enqueue: store holds 3 of 5 -> only reps 4 and 5 intended")


def test_lease_reaps_a_dead_worker():
    p, c = fresh(), cell()
    p.enqueue(c, 2, env={}, requested_by="r")
    p.claim(who="doomed")
    assert p.counts()["claimed"] == 1
    assert len(p.reap(lease_s=-1)) == 1
    assert p.counts() == {"pending": 2, "claimed": 0, "done": 0}, p.counts()
    print("ok  lease: a claimed item returns to pending when its worker dies")


def test_release_keeps_the_rep_reserved():
    p, c = fresh(), cell()
    p.enqueue(c, 2, env={}, requested_by="r")
    it = p.claim(who="w")
    p.release(it, note="backend down")
    assert p.counts() == {"pending": 2, "claimed": 0, "done": 0}, p.counts()
    assert p.enqueue(c, 2, env={}, requested_by="r") == []
    print("ok  release: unfinished work returns, its rep still reserved")


if __name__ == "__main__":
    for fn in (test_enqueue_is_idempotent_under_concurrency,
               test_no_double_claim,
               test_held_reps_are_not_requested,
               test_lease_reaps_a_dead_worker,
               test_release_keeps_the_rep_reserved):
        fn()
    shutil.rmtree(TMP, ignore_errors=True)
    print("\nall pool concurrency properties hold")
