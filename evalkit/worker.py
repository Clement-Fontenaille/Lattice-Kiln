"""A pair of hands. Claims work from the pool, runs it, records it, completes it.

Workers are interchangeable and know nothing about experiments. Start one, start
six, stop them whenever -- the pool is the authority on what should run and the
only thing any of them touch.

    python worker.py                 # drain the pool, then stop
    python worker.py --follow        # keep waiting for new work
    python worker.py --batch 8       # claim up to 8 compatible items at a time

Several workers are safe together. A worker takes work that uses a model already
resident on the card in preference to anything else, and when another worker is
mid-item it will take ONLY such work -- waiting rather than claiming something
that would evict the model its neighbour is using. On a single-GPU host that is
the difference between a second worker helping and a second worker halving
throughput for both.

Claims are batched by what `run_suite` takes -- one arm under one environment --
because a process start costs a few seconds and a rep costs thirty to ninety.
Claiming eight compatible items and running them in one invocation removes most
of that overhead without making the claim itself any less atomic: each item is
still claimed on its own, one exclusive create at a time.

On failure the batch is **released, not completed**, so its rep numbers stay
reserved and the work returns to pending for whoever comes next. A worker that
dies without releasing is covered by the lease: `pool.reap()` returns anything
held longer than it could plausibly still be running.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from pool import Pool, _who  # noqa: E402
from setup_key import ROOT  # noqa: E402

M6 = ROOT / "experiments" / "M6-evaluation-suite"


def backend_live(env: dict) -> tuple[bool, str]:
    backend = env.get("LATTICE_BACKEND", "ollama")
    if backend == "llamacpp":
        url = env.get("LATTICE_BASE_URL", "http://localhost:8090") + "/health"
        want = '"status":"ok"'
    else:
        url = env.get("LATTICE_BASE_URL", "http://localhost:11434") + "/api/tags"
        want = None
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            body = r.read().decode("utf-8", "replace")
        if want and want not in body:
            return False, f"{backend} reachable, not ready"
        return True, f"{backend} ready"
    except Exception as e:  # noqa: BLE001
        return False, f"{backend} unreachable ({e})"


def loaded_models(base_url: str = "http://localhost:11434") -> set[str]:
    """What the backend currently holds resident. Empty means an idle card, and
    an idle card is free to be filled with anything."""
    try:
        with urllib.request.urlopen(f"{base_url}/api/ps", timeout=5) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        return {m.get("name", "") for m in (d.get("models") or [])}
    except Exception:  # noqa: BLE001
        return set()


def others_working(pool, who: str) -> bool:
    """Is anyone else mid-item? Their model is the one on the card, and taking
    work that would evict it is how two workers turn into half of one."""
    for p in pool.claimed.glob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if d.get("claimed_by") and d["claimed_by"] != who:
            return True
    return False


def wants_loaded(d: dict, loaded: set[str]) -> bool:
    return d.get("env", {}).get("LATTICE_EVAL_MODEL") in loaded


def group_key(item) -> tuple:
    """What may share one run_suite invocation: same arm, same environment."""
    return (item.cell["arm"], json.dumps(item.env, sort_keys=True))


HOLD = object()
"""Returned by `pick` for: there is work, but taking any of it would evict the
model another worker is mid-item on. Distinct from None, which means the pool
has nothing this worker could take at all."""


def pick(pool, who: str, sticky, loaded: set[str]):
    """Choose the next item, in the order that costs the card least.

      1. more of the group just run       -- no model change at all
      2. anything using a resident model  -- no model change either
      3. anything, but only when a swap is safe

    A swap is safe only when nobody else is mid-item. This card holds one model;
    claiming work that evicts the model a neighbour is using turns two workers
    into rather less than one. So a second worker started while the first is
    busy takes ONLY work fitting the resident model, and otherwise HOLDs.
    """
    if sticky is not None:
        got = pool.claim(who, match=lambda d, k=sticky: (
            d["cell"]["arm"], json.dumps(d.get("env", {}), sort_keys=True)) == k)
        if got is not None:
            return got
    if loaded:
        got = pool.claim(who, match=lambda d: wants_loaded(d, loaded))
        if got is not None:
            return got
        if others_working(pool, who):
            return HOLD if pool.counts()["pending"] else None
    return pool.claim(who)


def run_batch(items, log_dir: Path, base_url: str | None = None) -> int:
    first = items[0]
    env = {**os.environ, **{k: str(v) for k, v in first.env.items()}}
    # The WORKER owns which backend instance it talks to, not the queue item.
    # Pinning an instance at enqueue time would split the pool into per-instance
    # halves and let one sit idle while the other has a backlog; this way any
    # worker can claim any item. It is deliberately not in the setup key either:
    # two servers running the same weights are the same setup.
    if base_url and "LATTICE_BASE_URL" not in first.env:
        env["LATTICE_BASE_URL"] = base_url
    work = [{"task": it.cell["task"], "rep": it.rep} for it in items]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8") as fh:
        json.dump(work, fh)
        wpath = fh.name
    cmd = [sys.executable, str(M6 / "run_suite.py"),
           "--arm", first.cell["arm"], "--work", wpath]
    log_dir.mkdir(parents=True, exist_ok=True)
    log = log_dir / f"worker_{first.cell['arm']}.log"
    try:
        with log.open("a", encoding="utf-8") as fh:
            return subprocess.call(cmd, cwd=str(M6), stdout=fh,
                                   stderr=subprocess.STDOUT, env=env)
    finally:
        os.unlink(wpath)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", default=None)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--follow", action="store_true")
    ap.add_argument("--idle-s", type=float, default=30.0)
    ap.add_argument("--base-url", default="http://localhost:11434",
                    help="the backend instance THIS worker uses -- for residency "
                         "checks, liveness, and the runs themselves. Several "
                         "instances on one host give several decode streams "
                         "where OLLAMA_NUM_PARALLEL cannot: it is a maximum, and "
                         "ollama refuses it outright for some architectures "
                         "(nemotron_h). Items stay instance-agnostic.")
    ap.add_argument("--reap", action="store_true",
                    help="return items whose worker died before starting")
    args = ap.parse_args()

    pool = Pool(Path(args.pool) if args.pool else None)
    who = _who()
    print(f"worker {who} | pool {pool.path} | backend {args.base_url} | "
          f"{pool.counts()}", flush=True)

    if args.reap:
        got = pool.reap()
        if got:
            print(f"reaped {len(got)} abandoned item(s)", flush=True)

    done = failed = 0
    sticky = None          # keep working one group while it lasts
    while True:
        loaded = loaded_models(args.base_url)
        first = pick(pool, who, sticky, loaded)
        if first is HOLD:
            if args.follow:
                print(f"[{who}] holding: {sorted(loaded)} resident and in use by "
                      f"another worker; nothing pending fits it", flush=True)
                time.sleep(args.idle_s)
                continue
            print(f"[{who}] stopping: nothing pending fits the resident model "
                  f"and another worker is using it", flush=True)
            break
        if first is None:
            if args.follow:
                time.sleep(args.idle_s)
                continue
            break

        # Fill the batch with items that can share one invocation. Each is still
        # claimed individually; batching is about process startup, not locking.
        batch = [first]
        key = sticky = group_key(first)
        while len(batch) < args.batch:
            nxt = pool.claim(who, match=lambda d, k=key: (
                d["cell"]["arm"], json.dumps(d.get("env", {}), sort_keys=True)) == k)
            if nxt is None:
                break
            batch.append(nxt)

        ok, why = backend_live({**first.env,
                                **({"LATTICE_BASE_URL": args.base_url}
                                   if args.base_url else {})})
        if not ok:
            for it in batch:
                pool.release(it, note=why)
            print(f"released {len(batch)} item(s): {why}", flush=True)
            if args.follow:
                time.sleep(args.idle_s)
                continue
            break

        label = f"{first.cell['arm']}/{first.cell['model']}/{first.cell['judge_format']}"
        print(f"[{who}] {len(batch)} item(s)  {label}", flush=True)
        rc = run_batch(batch, Path(args.pool or pool.path) / "logs",
                       base_url=args.base_url)
        for it in batch:
            if rc == 0:
                pool.complete(it, "ok")
                done += 1
            else:
                pool.release(it, note=f"run_suite exit {rc}")
                failed += 1
        print(f"      exit {rc} | done {done} released {failed} | {pool.counts()}",
              flush=True)

    print(f"worker {who} stopping: {done} completed, {failed} released", flush=True)


if __name__ == "__main__":
    main()
