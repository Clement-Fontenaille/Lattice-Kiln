"""A pair of hands. Claims work from the pool, runs it, records it, completes it.

Workers are interchangeable and know nothing about experiments. Start one, start
six, stop them whenever -- the pool is the authority on what should run and the
only thing any of them touch.

    python worker.py                 # drain the pool, then stop
    python worker.py --follow        # keep waiting for new work
    python worker.py --batch 8       # claim up to 8 compatible items at a time

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


def group_key(item) -> tuple:
    """What may share one run_suite invocation: same arm, same environment."""
    return (item.cell["arm"], json.dumps(item.env, sort_keys=True))


def run_batch(items, log_dir: Path) -> int:
    first = items[0]
    env = {**os.environ, **{k: str(v) for k, v in first.env.items()}}
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
    ap.add_argument("--reap", action="store_true",
                    help="return items whose worker died before starting")
    args = ap.parse_args()

    pool = Pool(Path(args.pool) if args.pool else None)
    who = _who()
    print(f"worker {who} | pool {pool.path} | {pool.counts()}", flush=True)

    if args.reap:
        got = pool.reap()
        if got:
            print(f"reaped {len(got)} abandoned item(s)", flush=True)

    done = failed = 0
    sticky = None          # keep working one group while it lasts
    while True:
        # Prefer more of what we just ran. Claim order is by cell id, which is
        # effectively random across models, and every switch between them costs
        # a full model load and evicts the other -- on an 8GB card that is the
        # difference between a sweep and a thrash.
        first = None
        if sticky is not None:
            first = pool.claim(who, match=lambda d, k=sticky: (
                d["cell"]["arm"],
                json.dumps(d.get("env", {}), sort_keys=True)) == k)
        if first is None:
            first = pool.claim(who)
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

        ok, why = backend_live(first.env)
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
        rc = run_batch(batch, Path(args.pool or pool.path) / "logs")
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
