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
from worker import HOLD, env_key, pick  # noqa: E402

TMP = HERE.parent / ".pool_selftest"


def cell(model="selftest", task="wf1_crossfile", arm="baseline", params=None,
         judge_format="decision_first"):
    return Cell.make(task=task, arm=arm, backend="ollama", model=model,
                     judge_format=judge_format, params=params or {},
                     defaults={"num_ctx": 8192})


def env(model, **extra):
    return {"LATTICE_BACKEND": "ollama", "LATTICE_EVAL_MODEL": model, **extra}


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


def test_a_model_that_does_not_fit_beside_a_peer_is_refused():
    """Peers keep what they hold; only this instance's share is freed by a swap.

    qwen 7B is 5,204 MiB resident and nemotron3-nano-4b is 2,865. Either beside
    the other overruns an 8 GiB card, and so does qwen beside a second copy of
    itself -- which a name-based guard would have allowed, since the names match.
    """
    p = fresh()
    p.enqueue(cell("big", arm="monolith"), 2, env=env("big"), requested_by="r")
    assert pick(p, "w1", None, set(), card={"small"},
                fits=lambda m: m != "big") is HOLD
    assert p.counts()["pending"] == 2, p.counts()
    print("ok  pick: a model that will not fit beside a peer is refused")


def test_the_guard_does_not_deadlock_when_something_fits():
    """The first guard admitted only work matching a peer's model, so when the
    resident model's work ran out and something else was pending, every worker
    held forever. Fitting is the condition, not matching."""
    p = fresh()
    p.enqueue(cell("small", arm="monolith"), 2, env=env("small"), requested_by="r")
    got = pick(p, "w1", None, set(), card={"other"}, fits=lambda m: m == "small")
    assert got is not None and got is not HOLD, "held while work that fits was pending"
    print("ok  pick: work that fits is taken, even when a peer holds something else")


def test_swap_within_my_own_instance_is_allowed():
    """The card never holds both when one instance replaces its own model."""
    p = fresh()
    p.enqueue(cell("mB", arm="monolith"), 1, env=env("mB"), requested_by="r")
    got = pick(p, "w1", None, {"mA"}, card={"mA"}, fits=lambda m: True)
    assert got is not None and got.env["LATTICE_EVAL_MODEL"] == "mB"
    print("ok  pick: a worker may replace the model in its own instance")


def test_same_setup_beats_same_model():
    """The model is one field of the setup key, not the setup.

    think=1 and think=0 run the same weights and produce different cells. A
    worker leaving one must not fall into the other just because no model load
    is needed -- that interleaves a 538-token setup with a 41-token one.
    """
    p = fresh()
    slow = env("mA", LATTICE_THINK="1", LATTICE_MIN_PREDICT="2048")
    fast = env("mA", LATTICE_THINK="0", LATTICE_MIN_PREDICT="400")
    S, F = {"think": True, "min_predict": 2048}, {"think": False}
    p.enqueue(cell("mA", arm="baseline", params=S), 1, env=slow, requested_by="r")
    p.enqueue(cell("mA", arm="monolith", params=S), 1, env=slow, requested_by="r")
    p.enqueue(cell("mA", arm="baseline", params=F), 1, env=fast, requested_by="r")

    first = pick(p, "w1", None, {"mA"})
    key = (first.cell["arm"], env_key(first.env))
    nxt = pick(p, "w1", key, {"mA"})
    assert env_key(nxt.env) == env_key(first.env), (
        f"crossed setups: {first.env} -> {nxt.env}")
    print("ok  pick: a worker finishes its SETUP before touching another")


def test_setup_affinity_partitions_workers():
    """Two setups, two workers: each settles on one without being told."""
    p = fresh()
    a = env("mA", LATTICE_JUDGE_FORMAT="decision_first")
    b = env("mA", LATTICE_JUDGE_FORMAT="reason_first")
    for arm in ("baseline", "monolith"):
        p.enqueue(cell("mA", arm=arm, judge_format="decision_first"), 2,
                  env=a, requested_by="r")
        p.enqueue(cell("mA", arm=arm, judge_format="reason_first"), 2,
                  env=b, requested_by="r")
    seen = {}
    for w in ("w1", "w2"):
        it = pick(p, w, None, {"mA"})
        k = (it.cell["arm"], env_key(it.env))
        for _ in range(3):
            nxt = pick(p, w, k, {"mA"})
            if nxt is None or nxt is HOLD:
                break
            seen.setdefault(w, set()).add(env_key(nxt.env))
            k = (nxt.cell["arm"], env_key(nxt.env))
    for w, envs in seen.items():
        assert len(envs) == 1, f"{w} mixed setups: {envs}"
    print("ok  pick: workers partition across setups on their own")


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
               test_a_model_that_does_not_fit_beside_a_peer_is_refused,
               test_the_guard_does_not_deadlock_when_something_fits,
               test_swap_within_my_own_instance_is_allowed,
               test_same_setup_beats_same_model,
               test_setup_affinity_partitions_workers):
        fn()
    shutil.rmtree(TMP, ignore_errors=True)
    print("\nall pool concurrency properties hold")
