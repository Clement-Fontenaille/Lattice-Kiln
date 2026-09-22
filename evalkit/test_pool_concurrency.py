"""The pool's concurrency properties, as a test rather than as a claim.

Every assertion here failed at least once during the pool's construction, which
is why they are assertions and not prose:

  A  eight requesters racing produced FORTY reps for a target of five, because
     enqueue took a delta and each computed its own deficit before any wrote.
  B  twelve workers double-claimed: `os.rename` succeeded twice for the same
     source on Windows, twelve renames from seven sources.
  C  a second worker on a one-GPU host claimed by cell id, which is effectively
     random across models, so it evicted the model the first was mid-item on and
     the two of them ran slower than one.

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
from worker import HOLD, pick  # noqa: E402

TMP = HERE.parent / ".pool_selftest"


def cell(model="selftest", task="wf1_crossfile", arm="baseline"):
    return Cell.make(task=task, arm=arm, backend="ollama",
                     model=model, params={}, defaults={"num_ctx": 8192})


def env(model):
    return {"LATTICE_BACKEND": "ollama", "LATTICE_EVAL_MODEL": model}


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


def test_second_worker_prefers_the_resident_model():
    """Both models have work pending; the card holds one of them."""
    p = fresh()
    p.enqueue(cell("mA", arm="baseline"), 2, env=env("mA"), requested_by="r")
    p.enqueue(cell("mB", arm="monolith"), 2, env=env("mB"), requested_by="r")
    got = pick(p, "w2", None, {"mB"})
    assert got.env["LATTICE_EVAL_MODEL"] == "mB", got.env
    print("ok  pick: work for two models, one resident -> takes the resident one")


def test_second_worker_holds_rather_than_evicting():
    """The resident model's work is exhausted and worker one is still on it.
    Claiming the other model here would evict it mid-item."""
    p = fresh()
    p.enqueue(cell("mA", arm="baseline"), 1, env=env("mA"), requested_by="r")
    p.enqueue(cell("mB", arm="monolith"), 2, env=env("mB"), requested_by="r")
    p.claim(who="w1", match=lambda d: d["cell"]["model"] == "mA")   # w1 busy on mA
    assert pick(p, "w2", None, {"mA"}) is HOLD
    assert p.counts()["pending"] == 2, p.counts()
    print("ok  pick: resident work exhausted, neighbour busy -> holds, evicts nothing")


def test_a_lone_worker_may_swap():
    """Same pool, nobody else mid-item: a swap costs one load and nothing else."""
    p = fresh()
    p.enqueue(cell("mB", arm="monolith"), 2, env=env("mB"), requested_by="r")
    got = pick(p, "w1", None, {"mA"})
    assert got is not None and got.env["LATTICE_EVAL_MODEL"] == "mB"
    print("ok  pick: alone on the host -> free to swap the model")


def test_sticky_beats_resident():
    """Both arms use the resident model, so rule 2 would take either. Rule 1
    keeps the worker inside the group it is already set up for, whichever way
    cell ids happen to sort."""
    p = fresh()
    p.enqueue(cell("mA", arm="baseline"), 2, env=env("mA"), requested_by="r")
    p.enqueue(cell("mA", arm="monolith"), 2, env=env("mA"), requested_by="r")
    import json as _json
    first = pick(p, "w1", None, {"mA"})
    key = (first.cell["arm"], _json.dumps(first.env, sort_keys=True))
    nxt = pick(p, "w1", key, {"mA"})
    assert nxt.cell["arm"] == first.cell["arm"], (first.cell["arm"], nxt.cell["arm"])
    print("ok  pick: sticky group is tried before anything else")


def test_peer_instance_blocks_an_unfittable_pairing():
    """Two servers on one GPU share its VRAM and each reports only its own
    models. A worker blind to its peer pairs two models that do not fit."""
    p = fresh()
    p.enqueue(cell("mB", arm="monolith"), 2, env=env("mB"), requested_by="r")
    # this worker's instance is empty; a PEER holds mA
    assert pick(p, "w1", None, set(), card={"mA"}) is HOLD
    assert p.counts()["pending"] == 2, p.counts()
    # same pool, no peer: swapping inside one instance evicts, so it is free
    assert pick(p, "w1", None, set(), card=set()) is not None
    print("ok  pick: a peer instance's model blocks the pairing, alone does not")


def test_swap_within_my_own_instance_is_allowed():
    """The card never holds both when one instance replaces its own model."""
    p = fresh()
    p.enqueue(cell("mB", arm="monolith"), 1, env=env("mB"), requested_by="r")
    got = pick(p, "w1", None, {"mA"}, card={"mA"})      # only I hold mA
    assert got is not None and got.env["LATTICE_EVAL_MODEL"] == "mB"
    print("ok  pick: a worker may replace the model in its own instance")


if __name__ == "__main__":
    for fn in (test_enqueue_is_idempotent_under_concurrency,
               test_no_double_claim,
               test_held_reps_are_not_requested,
               test_lease_reaps_a_dead_worker,
               test_release_keeps_the_rep_reserved,
               test_second_worker_prefers_the_resident_model,
               test_second_worker_holds_rather_than_evicting,
               test_a_lone_worker_may_swap,
               test_sticky_beats_resident,
               test_peer_instance_blocks_an_unfittable_pairing,
               test_swap_within_my_own_instance_is_allowed):
        fn()
    shutil.rmtree(TMP, ignore_errors=True)
    print("\nall pool concurrency properties hold")
