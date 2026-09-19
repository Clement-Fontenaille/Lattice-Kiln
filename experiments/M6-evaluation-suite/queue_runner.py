"""Run a queue of suite jobs one at a time, resumably, unattended.

    python queue_runner.py            # work the queue
    python queue_runner.py --status   # what is done, running, left
    python queue_runner.py --plan     # print the queue and stop

The queue lives in `queue.json` and each job is `{"arm": ..., "reps": ...}`. A job is
**done** when the arm's results file holds one row per (task, rep) for the current
suite, so the queue is idempotent: re-running it skips finished work and resumes a job
interrupted half way, because `run_suite.py --resume` keeps what was already recorded.

That property is the point. A queue that loses an arm's work when the machine is
interrupted is a queue nobody can leave running overnight.

**Order is priority, not convenience.** If the queue does not finish, what ran first
should be what carries the most information, so the list is ordered by that and the
reasoning is in `queue.json` beside each job.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUEUE = HERE / "queue.json"
LOG = HERE / "queue.log"

# A job may carry `env`, applied to that job's subprocess only. That is what lets
# one queue hold jobs for different backends: the backend is bound at import time
# in ollama_client, so it cannot change inside a process -- but every job is
# already its own process, so per-job env is enough and nothing else has to move.
#
# `LATTICE_RESULTS_SUBDIR` is the one that must be read HERE as well as passed
# down. Until 2026-09-17 this file hardcoded `results/` while run_suite.py
# honoured the variable, so a queue pointed at another model's subdirectory
# checked the *default* directory for completion, found every arm full, and
# logged "already complete - skip" for all of it. A queue that reports a clean
# finish having run nothing is the failure this whole file exists to prevent.


def results_dir(job):
    return HERE / job.get("env", {}).get("LATTICE_RESULTS_SUBDIR", "results")


def suite_size():
    d = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))
    return len(d["tasks"]), d["suite_version"]


def rows_for(job):
    """Rows that actually executed. A row with `run_ok: false` is a run that
    raised before producing an attempt, so it is not work done and must not count
    toward completion -- otherwise a crashing arm looks finished and `--resume`
    never retries it."""
    p = results_dir(job) / f"{job['arm']}.json"
    if not p.is_file():
        return 0
    try:
        return sum(1 for r in json.loads(p.read_text(encoding="utf-8"))
                   if r.get("run_ok", True))
    except Exception:  # noqa: BLE001
        return 0


def state(job, ntasks):
    want = ntasks * job["reps"]
    have = rows_for(job)
    if have >= want:
        return "done", have, want
    return ("partial" if have else "todo"), have, want


_READY_CACHE = {}


def backend_ready(job, timeout_s=10.0, cache=False):
    """`cache` is for --status, which asks once per job over a whole queue and
    otherwise spends a timeout per row. The runner itself never caches: a
    backend that was up when the queue started is exactly what must be
    re-checked before each job."""
    env = job.get("env", {})
    key = (env.get("LATTICE_BACKEND"), env.get("LATTICE_BASE_URL"))
    if cache and key in _READY_CACHE:
        return _READY_CACHE[key]
    r = _backend_ready(job, timeout_s)
    if cache:
        _READY_CACHE[key] = r
    return r


def _backend_ready(job, timeout_s=10.0):
    """Is the backend this job needs actually up and serving?

    The check that was missing on 2026-09-15: llama-server died two tasks into a
    15-arm sweep and the harness walked the remaining 32 tasks against an
    untouched workspace, scoring every one. Five false-premise tasks were even
    credited with a correct decline, because "nothing changed" is what declining
    looks like from the outside. One HTTP call per job prevents all of it.

    Note the readiness check is on the BODY, not the status code alone:
    llama-server answers /health with 503 and `{"status":"loading model"}` while
    it maps 6.7GB off disk, which is a response but not a server ready to work.
    """
    env = job.get("env", {})
    backend = env.get("LATTICE_BACKEND", os.environ.get("LATTICE_BACKEND", "ollama"))
    if backend == "llamacpp":
        base = env.get("LATTICE_BASE_URL", "http://localhost:8090")
        url, want = f"{base}/health", '"status":"ok"'
    else:
        base = env.get("LATTICE_BASE_URL", "http://localhost:11434")
        url, want = f"{base}/api/tags", None
    try:
        with urllib.request.urlopen(url, timeout=timeout_s) as resp:
            if resp.status != 200:
                return False, f"{backend} at {base}: HTTP {resp.status}"
            if want and want not in resp.read().decode("utf-8", "replace"):
                return False, f"{backend} at {base}: reachable but not ready"
    except urllib.error.URLError as e:
        return False, f"{backend} at {base}: unreachable ({e.reason})"
    except Exception as e:  # noqa: BLE001
        return False, f"{backend} at {base}: {e!r}"

    # Reachable is not the same as having a card to work on. This host has 8GB and
    # llama-server alone holds ~7.6GB of it, so whichever backend loads second
    # lands on the 10-20x offload cliff M0 entry 1 measured -- slow, not failed,
    # so nothing reports it and a queue left overnight quietly takes days.
    #
    # The test is OCCUPANCY, not liveness, and the two backends differ in how to
    # ask. llama-server loads its model at startup, so a healthy /health means the
    # VRAM is already gone. Ollama's daemon answers /api/tags while holding
    # nothing, and only /api/ps says what is actually resident -- so an idle
    # Ollama daemon is not a reason to block a llama.cpp job.
    if backend == "llamacpp":
        try:
            with urllib.request.urlopen("http://localhost:11434/api/ps", timeout=3.0) as r:
                loaded = json.loads(r.read().decode("utf-8", "replace")).get("models") or []
            if loaded:
                names = ", ".join(m.get("name", "?") for m in loaded)
                return False, (f"llamacpp up, but Ollama is holding the card ({names}) "
                               f"-- unload it (keep_alive: 0) or stop the daemon")
        except Exception:  # noqa: BLE001
            pass                              # daemon absent or too old for /api/ps
    else:
        try:
            with urllib.request.urlopen("http://localhost:8090/health", timeout=3.0) as r:
                if r.status == 200:
                    return False, ("ollama up, but llama-server is resident on the card "
                                   "-- stop it before running an Ollama job")
        except Exception:  # noqa: BLE001
            pass                              # the good case: llama-server is down
    return True, f"{backend} at {base}: ready, sole occupant"


def log(msg):
    line = f"{time.strftime('%H:%M:%S')}  {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def main():
    # --queue lets another experiment drive this runner with its own job list
    # while run_suite, the suite and the arms stay where they are.
    qpath = QUEUE
    if "--queue" in sys.argv:
        qpath = Path(sys.argv[sys.argv.index("--queue") + 1]).resolve()
    jobs = json.loads(qpath.read_text(encoding="utf-8"))["jobs"]
    ntasks, sv = suite_size()

    if "--status" in sys.argv or "--plan" in sys.argv:
        print(f"suite {sv}, {ntasks} tasks\n")
        print("| # | job | arm | reps | backend | state | rows | ready |")
        print("|---|---|---|---|---|---|---|---|")
        for i, j in enumerate(jobs, 1):
            st, have, want = state(j, ntasks)
            be = j.get("env", {}).get("LATTICE_BACKEND", "ollama")
            ready, why = backend_ready(j, timeout_s=3.0, cache=True)
            print(f"| {i} | {j.get('label') or j['arm']} | `{j['arm']}` | {j['reps']} "
                  f"| {be} | {st} | {have}/{want} | {'yes' if ready else why} |")
        return

    t0 = time.monotonic()
    for i, j in enumerate(jobs, 1):
        st, have, want = state(j, ntasks)
        tag = j.get("label") or j["arm"]
        if st == "done":
            log(f"[{i}/{len(jobs)}] {tag} already complete ({have} rows) - skip")
            continue

        ready, why = backend_ready(j)
        if not ready:
            # Skip, do not run. A job that runs into a dead backend produces a
            # full set of scored rows measuring the untouched fixture, which is
            # worse than no data because it looks like data.
            log(f"[{i}/{len(jobs)}] {tag} SKIPPED - {why}")
            continue

        log(f"[{i}/{len(jobs)}] {tag} reps={j['reps']} - {st}, {have}/{want} ({why})")
        cmd = [sys.executable, str(HERE / "run_suite.py"), "--arm", j["arm"],
               "--reps", str(j["reps"]), "--resume"]
        env = {**os.environ, **{k: str(v) for k, v in j.get("env", {}).items()}}
        out = HERE / f"queue_{tag}.log"
        with out.open("a", encoding="utf-8") as fh:
            rc = subprocess.call(cmd, cwd=str(HERE), stdout=fh,
                                 stderr=subprocess.STDOUT, env=env)
        st, have, want = state(j, ntasks)
        log(f"      -> exit {rc}, {have}/{want} rows, {(time.monotonic()-t0)/60:.0f} min "
            f"elapsed overall")
        if rc != 0 and st != "done":
            # a failing arm must not take the queue down with it
            log(f"      !! {j['arm']} did not finish; continuing to the next job")

    log(f"QUEUE DONE in {(time.monotonic()-t0)/60:.0f} min")


if __name__ == "__main__":
    main()
