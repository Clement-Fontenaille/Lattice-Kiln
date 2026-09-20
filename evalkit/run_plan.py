"""Turn a declaration into intended work, or run the deficit directly.

    python run_plan.py <declaration.json> --enqueue   # into the pool (preferred)
    python run_plan.py <declaration.json>             # run it here and now

`--enqueue` is the one to use when anything else might be running. It adds the
deficit to the pool, where rep numbers are reserved by exclusive create, and
workers claim from there -- so two people enqueuing the same declaration produce
one set of work rather than two racing plans. Without it this runs the deficit
itself, which is fine alone and unsafe alongside a worker.

`plan.py` says what is missing; this acts on exactly that and nothing else,
asking the store rather than a directory what already exists.

Work is grouped by (arm, model, judge_format), because that is the unit
`run_suite` takes. Within a group the tasks still needing reps are passed
explicitly, so a group that is nine-tenths complete costs a tenth of a run
rather than a whole one.

The backend health gate still belongs to `queue_runner`; this drives
`run_suite` directly and checks liveness once per group, for the reason
recorded in queue_runner: a sweep that walks a dead backend produces a full set
of scored rows measuring an untouched fixture, which is worse than no data
because it looks like data.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from setup_key import ANY, ROOT  # noqa: E402
from store import Store  # noqa: E402
from plan import resolve  # noqa: E402

M6 = ROOT / "experiments" / "M6-evaluation-suite"


def backend_live(backend: str, base_url: str | None) -> tuple[bool, str]:
    url = base_url or ("http://localhost:8090/health" if backend == "llamacpp"
                       else "http://localhost:11434/api/tags")
    if backend == "llamacpp" and not url.endswith("/health"):
        url = url.rstrip("/") + "/health"
    if backend == "ollama" and not url.endswith("/api/tags"):
        url = url.rstrip("/") + "/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            body = r.read().decode("utf-8", "replace")
        if backend == "llamacpp" and '"status":"ok"' not in body:
            return False, f"{backend}: reachable, not ready"
        return True, f"{backend}: ready"
    except Exception as e:  # noqa: BLE001
        return False, f"{backend}: unreachable ({e})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("declaration")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--require-recorded", action="store_true")
    ap.add_argument("--enqueue", action="store_true",
                    help="put the deficit in the pool instead of running it")
    ap.add_argument("--pool", default=None)
    args = ap.parse_args()

    decl = json.loads(Path(args.declaration).read_text(encoding="utf-8"))
    store = Store()
    wpath = HERE / "waivers.json"
    waivers = (json.loads(wpath.read_text(encoding="utf-8"))["waivers"]
               if wpath.is_file() else [])

    if args.enqueue:
        from pool import Pool
        pool = Pool(Path(args.pool) if args.pool else None)
        made = 0
        for cell, query, reps in resolve(decl):
            mname = next(n for n, m in decl["models"].items()
                         if m["model"] == cell.model)
            m = decl["models"][mname]
            held = store.have(cell, args.require_recorded, waivers,
                              params_query=query)
            if held >= reps:
                continue
            env = {"LATTICE_BACKEND": m["backend"],
                   "LATTICE_EVAL_MODEL": m["model"],
                   "LATTICE_JUDGE_FORMAT": cell.judge_format,
                   "LATTICE_RESULTS_SUBDIR": decl.get(
                       "results_subdir_template",
                       "../{experiment}/results/{model}_{format}").format(
                           experiment=Path(args.declaration).parent.name,
                           model=mname, format=cell.judge_format)}
            for k, v in (m.get("params") or {}).items():
                if v == ANY:
                    continue
                if k == "think":
                    env["LATTICE_THINK"] = "1" if v else "0"
                elif k == "min_predict":
                    env["LATTICE_MIN_PREDICT"] = str(v)
            made += len(pool.enqueue(cell, reps, env=env, held=held,
                                     requested_by=decl.get("name", "unnamed")))
        print(f"{decl.get('name','experiment')}\n")
        print(f"enqueued {made} item(s) -> {pool.counts()}")
        print("\nrun `python worker.py` (as many as the host can feed) to work it")
        return

    # deficit per (arm, model-name, format): which tasks, and to what depth
    groups: dict[tuple, dict] = defaultdict(lambda: {"tasks": {}, "reps": 0})
    for cell, query, reps in resolve(decl):
        mname = next(n for n, m in decl["models"].items()
                     if m["model"] == cell.model)
        have = min(store.have(cell, args.require_recorded, waivers,
                              params_query=query), reps)
        if have < reps:
            g = groups[(cell.arm, mname, cell.judge_format)]
            g["tasks"][cell.task] = reps - have
            g["reps"] = max(g["reps"], reps)

    if not groups:
        print("nothing to run: the store already satisfies this declaration")
        return

    print(f"{decl.get('name', 'experiment')}\n")
    print(f"{'arm':18s} {'model':6s} {'format':15s} {'tasks':>6s} {'reps':>5s}")
    for (arm, mname, fmt), g in sorted(groups.items()):
        print(f"{arm:18s} {mname:6s} {fmt:15s} {len(g['tasks']):6d} {g['reps']:5d}")
    print(f"\n{len(groups)} run(s)\n")

    t0 = time.monotonic()
    for i, ((arm, mname, fmt), g) in enumerate(sorted(groups.items()), 1):
        m = decl["models"][mname]
        env = {**os.environ,
               "LATTICE_BACKEND": m["backend"],
               "LATTICE_EVAL_MODEL": m["model"],
               "LATTICE_JUDGE_FORMAT": fmt,
               "LATTICE_RESULTS_SUBDIR": decl.get(
                   "results_subdir_template",
                   "../{experiment}/results/{model}_{format}").format(
                       experiment=Path(args.declaration).parent.name,
                       model=mname, format=fmt)}
        for k, v in (m.get("params") or {}).items():
            if v == ANY:
                continue          # `any` resolves to the ambient default
            if k == "think":
                env["LATTICE_THINK"] = "1" if v else "0"
            elif k == "min_predict":
                env["LATTICE_MIN_PREDICT"] = str(v)

        any_params = [k for k, v in (m.get("params") or {}).items() if v == ANY]
        cmd = [sys.executable, str(M6 / "run_suite.py"), "--arm", arm,
               "--reps", str(g["reps"]), "--resume", "--store-resume",
               "--tasks", *sorted(g["tasks"])]
        if any_params:
            cmd += ["--params-any", *any_params]

        label = f"{mname}-{fmt}-{arm}"
        ok, why = backend_live(m["backend"], m.get("base_url"))
        if not ok:
            print(f"[{i}/{len(groups)}] {label} SKIPPED - {why}", flush=True)
            continue
        print(f"[{i}/{len(groups)}] {label}  {len(g['tasks'])} task(s) ({why})",
              flush=True)
        if args.dry_run:
            print("    " + " ".join(cmd[1:]))
            continue
        log = Path(args.declaration).parent / f"run_{label}.log"
        with log.open("a", encoding="utf-8") as fh:
            rc = subprocess.call(cmd, cwd=str(M6), stdout=fh,
                                 stderr=subprocess.STDOUT, env=env)
        print(f"      -> exit {rc}, {(time.monotonic()-t0)/60:.0f} min",
              flush=True)

    print(f"\nDONE in {(time.monotonic()-t0)/60:.0f} min")


if __name__ == "__main__":
    main()
