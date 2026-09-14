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
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUEUE = HERE / "queue.json"
RESULTS = HERE / "results"
LOG = HERE / "queue.log"


def suite_size():
    d = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))
    return len(d["tasks"]), d["suite_version"]


def rows_for(arm):
    p = RESULTS / f"{arm}.json"
    if not p.is_file():
        return 0
    try:
        return len(json.loads(p.read_text(encoding="utf-8")))
    except Exception:  # noqa: BLE001
        return 0


def state(job, ntasks):
    want = ntasks * job["reps"]
    have = rows_for(job["arm"])
    if have >= want:
        return "done", have, want
    return ("partial" if have else "todo"), have, want


def log(msg):
    line = f"{time.strftime('%H:%M:%S')}  {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def main():
    jobs = json.loads(QUEUE.read_text(encoding="utf-8"))["jobs"]
    ntasks, sv = suite_size()

    if "--status" in sys.argv or "--plan" in sys.argv:
        print(f"suite {sv}, {ntasks} tasks\n")
        print("| # | arm | reps | state | rows | why it is here |")
        print("|---|---|---|---|---|---|")
        for i, j in enumerate(jobs, 1):
            st, have, want = state(j, ntasks)
            print(f"| {i} | `{j['arm']}` | {j['reps']} | {st} | {have}/{want} | "
                  f"{j.get('why', '')} |")
        return

    t0 = time.monotonic()
    for i, j in enumerate(jobs, 1):
        st, have, want = state(j, ntasks)
        if st == "done":
            log(f"[{i}/{len(jobs)}] {j['arm']} already complete ({have} rows) - skip")
            continue
        log(f"[{i}/{len(jobs)}] {j['arm']} reps={j['reps']} - {st}, {have}/{want}")
        cmd = [sys.executable, str(HERE / "run_suite.py"), "--arm", j["arm"],
               "--reps", str(j["reps"]), "--resume"]
        out = HERE / f"queue_{j['arm']}.log"
        with out.open("a", encoding="utf-8") as fh:
            rc = subprocess.call(cmd, cwd=str(HERE), stdout=fh, stderr=subprocess.STDOUT)
        st, have, want = state(j, ntasks)
        log(f"      -> exit {rc}, {have}/{want} rows, {(time.monotonic()-t0)/60:.0f} min "
            f"elapsed overall")
        if rc != 0 and st != "done":
            # a failing arm must not take the queue down with it
            log(f"      !! {j['arm']} did not finish; continuing to the next job")

    log(f"QUEUE DONE in {(time.monotonic()-t0)/60:.0f} min")


if __name__ == "__main__":
    main()
