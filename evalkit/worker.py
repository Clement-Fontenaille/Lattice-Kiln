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
    """What one backend instance holds resident. Empty means it holds nothing."""
    try:
        with urllib.request.urlopen(f"{base_url}/api/ps", timeout=5) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        return {m.get("name", "") for m in (d.get("models") or [])}
    except Exception:  # noqa: BLE001
        return set()


def gpu_budget_mib(reserve_mib: int = 700) -> int | None:
    """Usable VRAM, or None when it cannot be read.

    `reserve_mib` is for the desktop and the driver, which held 464-650 MiB on
    the reference host with nothing else running.
    """
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            text=True, timeout=10, stderr=subprocess.DEVNULL)
        return int(out.strip().splitlines()[0]) - reserve_mib
    except Exception:  # noqa: BLE001
        return None


SIZES = ROOT / "evalkit_store" / "model_sizes.json"
DISK_TO_VRAM = 1.08
"""Fallback factor for a model never yet seen loaded.

There is no reliable constant. Measured on this host, the ratio of resident
VRAM to blob size on disk is 0.97 for nemotron-gpu (6,433 MiB on disk, 6,261
resident), 1.05 for nemotron3-nano-4b and 1.15 for qwen2.5-coder 7B -- it
depends on quant, on how much of the blob is actually mapped, and on the KV
layout, which for a hybrid Mamba model is nothing like a transformer's.

A factor high enough for qwen refuses nemotron-gpu outright, which would strand
its work. 1.08 is chosen to get every pairing on this card right, and is only
a bootstrap: the moment a model is observed resident its true size is recorded
and used instead, so the estimate matters once per model and then never again.
"""


def learn_sizes(urls) -> dict:
    """Record what loaded models actually cost, and return everything known."""
    known = {}
    try:
        known = json.loads(SIZES.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        pass
    seen = {}
    for u in urls:
        try:
            with urllib.request.urlopen(f"{u}/api/ps", timeout=5) as r:
                d = json.loads(r.read().decode("utf-8", "replace"))
            for m in (d.get("models") or []):
                if m.get("size_vram"):
                    seen[m["name"]] = int(m["size_vram"] / 2**20)
        except Exception:  # noqa: BLE001
            continue
    if seen and seen != {k: known.get(k) for k in seen}:
        known.update(seen)
        try:
            SIZES.parent.mkdir(parents=True, exist_ok=True)
            SIZES.write_text(json.dumps(known, indent=2, sort_keys=True),
                             encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass
    return known


def catalogue_mib(base_url: str, known: dict | None = None) -> dict:
    """Model name -> resident size in MiB: measured where known, else estimated.

    The estimate is only ever used to REFUSE a load, and it is replaced by a
    measurement the first time the model is seen resident.
    """
    known = known or {}
    try:
        with urllib.request.urlopen(f"{base_url}/api/tags", timeout=5) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        out = {}
        for m in (d.get("models") or []):
            n = m["name"]
            out[n] = known.get(n, int(m.get("size", 0) / 2**20 * DISK_TO_VRAM))
        return out
    except Exception:  # noqa: BLE001
        return dict(known)


def resident_mib(url: str) -> int:
    """What one instance is holding, in MiB."""
    try:
        with urllib.request.urlopen(f"{url}/api/ps", timeout=5) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        return int(sum(m.get("size_vram", 0) for m in (d.get("models") or [])) / 2**20)
    except Exception:  # noqa: BLE001
        return 0


def card_models(urls) -> set[str]:
    """What the CARD holds, across every instance on it.

    Several server processes on one GPU share one pool of VRAM, and each one
    only reports its own models. A worker asking just its own instance is
    therefore blind to the thing most likely to hurt it: two instances holding
    two different models at once. With nemotron3-nano-4b at 2,865 MiB per
    instance and qwen 7B at 5,200 MiB, any pairing of the two overruns an 8 GiB
    card, and the first version of `pick` would have walked into it at the tail
    of a sweep -- the moment `others_working` goes false and the swap guard
    opens.

    Residency is a property of the card, so this is the set to reason about.
    """
    out = set()
    for u in urls:
        out |= loaded_models(u)
    return out


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
    """What may share one run_suite invocation: same arm, same setup."""
    return (item.cell["arm"], env_key(item.env))


HOLD = object()
"""Returned by `pick` for: there is work, but taking any of it would evict the
model another worker is mid-item on. Distinct from None, which means the pool
has nothing this worker could take at all."""


def env_key(env: dict) -> str:
    """The whole setup a run happens under, as one comparable string.

    Not just the model. `LATTICE_THINK`, `LATTICE_MIN_PREDICT`,
    `LATTICE_JUDGE_FORMAT` and the backend all land in the env, and every one of
    them is part of the cell the results key under -- two items differing in any
    of them are different setups producing different cells, however identical
    the weights on the card.
    """
    return json.dumps(env or {}, sort_keys=True)


def pick(pool, who: str, sticky, loaded: set[str], card: set[str] | None = None,
         fits=None):
    """Choose the next item, in the order that costs least and mixes least.

      1. more of the group just run        -- same arm, same setup
      2. the same SETUP, any arm           -- same model AND same parameters
      3. anything using a resident model   -- no model load, but a setup change
      4. anything, if no peer instance blocks it

    Rung 2 is not an optimisation, it is the one that keeps runs coherent. The
    model is only one field of the setup key: think, min_predict, judge_format
    and the backend are all in there too, and items differing in any of them
    produce different cells. Without rung 2 a worker leaving a think=1 group
    falls straight into think=0 work, because rung 3 matches on the model alone
    and the weights are identical. That interleaves a 538-token setup with a
    41-token one on the same card, which muddles throughput measurement and
    makes each setup finish later than if they had been run in sequence.

    With it, workers partition themselves across whatever setups are pending --
    each finishes the one it is on before touching another, without being told
    which to take.
    """
    if sticky is not None:
        got = pool.claim(who, match=lambda d, k=sticky: (
            d["cell"]["arm"], env_key(d.get("env"))) == k)
        if got is not None:
            return got
        # Same setup, different arm: no model load and no parameter change.
        got = pool.claim(who, match=lambda d, k=sticky[1]: env_key(d.get("env")) == k)
        if got is not None:
            return got
    if loaded:
        got = pool.claim(who, match=lambda d: wants_loaded(d, loaded))
        if got is not None:
            return got
        if others_working(pool, who):
            return HOLD if pool.counts()["pending"] else None

    # A swap replaces what THIS instance holds -- ollama evicts -- but leaves
    # every peer instance holding whatever it has. So the question is whether
    # the candidate fits beside the peers, and that is a question about bytes.
    #
    # Names are not enough, and an earlier version of this guard proved it in
    # two ways. It admitted only work matching a peer's model, which deadlocked
    # the moment the resident model's work ran out and something else was
    # pending: every worker held, forever. And it would still have allowed two
    # instances to load qwen 7B at 5,204 MiB each, which is 10.4 GiB on an 8 GiB
    # card -- same name, does not fit.
    if fits is not None:
        got = pool.claim(who, match=lambda d: fits(
            d.get("env", {}).get("LATTICE_EVAL_MODEL")))
        if got is not None:
            return got
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
    ap.add_argument("--peer", action="append", default=[],
                    help="another backend instance sharing this GPU, repeatable. "
                         "Residency is a property of the CARD, not of one server "
                         "process, and a worker blind to its peers will pair two "
                         "models that do not fit together.")
    ap.add_argument("--reserve-mib", type=int, default=700,
                    help="VRAM left to the desktop and driver when deciding "
                         "whether a model fits")
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
        card = card_models([args.base_url, *args.peer])

        # What can this worker load without overrunning the card?
        #
        # An earlier version assumed a swap frees this instance's share, which
        # is true only when this worker is alone on its instance. It is not:
        # two workers per instance is the whole point of gap-filling, and with
        # both free to choose, one took nemotron-gpu while the other took qwen
        # ON THE SAME INSTANCE -- 7,897 MiB of 8,192 before anything was even
        # decoding. Nothing frees anything when a co-worker is mid-item.
        #
        # So: already resident anywhere costs nothing to use. Anything else is
        # charged in full ON TOP of everything the card currently holds. That
        # refuses some swaps that would in fact have fit, and the refusal is
        # self-clearing -- the worker HOLDs, ollama's keep_alive unloads the
        # idle model, residency drops, and the next loop admits the work.
        budget = gpu_budget_mib(args.reserve_mib)
        urls = [args.base_url, *args.peer]
        sizes = catalogue_mib(args.base_url, learn_sizes(urls))
        card_mib = sum(resident_mib(u) for u in urls)

        def fits(model, _b=budget, _s=sizes, _c=card_mib, _card=card):
            if not model:
                return False
            if _b is None:
                return True          # cannot measure: do not pretend to know
            if any(m.split(":")[0] == model.split(":")[0] for m in _card):
                return True          # already on the card; using it adds nothing
            return _c + _s.get(model, 0) <= _b

        first = pick(pool, who, sticky, loaded, card, fits)
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
                d["cell"]["arm"], env_key(d.get("env"))) == k)
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
