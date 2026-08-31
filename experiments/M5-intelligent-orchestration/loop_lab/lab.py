"""Loop-lab (bundle D): loop control for the fixed sequence.

The judge-lab finding: the 7B reviewer verdict is unreliable, but the test result
is reliable (9/10). So drive the implementer<->review loop off the *measurable*
signal, not the reviewer's opinion.

Arms (same iteration budget, MAX_ROUNDS):
  oneshot     : implementer once. (= monolith baseline)
  naive_loop  : implementer, then (reviewer -> implementer)* while the reviewer
                says needs-change, up to MAX_ROUNDS. Returns the last written
                state. This is what the current `fixed` arm does.
  d_loop      : bundle D. (a) the pre-existing repo state is an entrant in the
                keeper pool - a change is accepted only if it BEATS it ("first do
                no harm"); (b) continue only while the score improved last round
                (progress gate = spec-08 repetition rule); (c) one stalled round
                -> stop and escalate; (d) return the best-scoring snapshot ever
                seen, not the last one. Fix hints are the real failing test
                lines, folded into the objective. No reviewer call.

    python lab.py                       # all arms, reps=2
    python lab.py --arms d_loop --reps 3
    python lab.py --smoke
"""
from __future__ import annotations

import argparse
import ast
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
M5 = HERE.parent
sys.path.insert(0, str(M5))

from _bridge import Gate, RunRecorder, assemble  # noqa: E402
from workflow_suite import (  # noqa: E402
    _files_blob, _run_role, fresh_workspace, load_tasks, objective_check,
    restore_protected,
)

RUNS = M5 / "runs"
RESULTS = HERE / "results"
ALL_ARMS = ("oneshot", "naive_loop", "d_loop")
MAX_ROUNDS = 3
STALL_TOL = 1          # stalled rounds tolerated before stopping
_KKEEP = "  keep-pool"


# ---------------------------------------------------------------- scoring

def _py_ok(ws: Path) -> bool:
    for p in ws.glob("*.py"):
        if p.name == "test_task.py":
            continue
        try:
            ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            return False
    return True


def score(ws: Path, cmd: str, task_dir: str, protected: list[str]) -> dict:
    restore_protected(ws, task_dir, protected)
    oc = objective_check(ws, cmd)
    p, t = oc["sub"]
    return {"sub": p, "tot": t, "py_ok": _py_ok(ws), "pass": oc["pass"],
            "tail": oc["tail"], "doc": oc["doc"], "todo": oc["todo"]}


def better(a: dict, b: dict) -> bool:
    """a strictly better than b: more subtests, or same subtests and newly parses."""
    if a["sub"] != b["sub"]:
        return a["sub"] > b["sub"]
    return a["py_ok"] and not b["py_ok"]


# ---------------------------------------------------------------- snapshots

def snap(ws: Path, tag: str) -> Path:
    d = Path(tempfile.mkdtemp(prefix=f"loop_{tag}_")).resolve()
    shutil.copytree(ws, d, dirs_exist_ok=True)
    return d


def _fail_lines(tail: str) -> str:
    keep = [ln for ln in (tail or "").splitlines()
            if ln.strip() and ("SUBTESTS" in ln or ln.startswith("  ") or "Error" in ln)]
    return "\n".join(keep[:12]) or (tail or "").strip()[-400:]


# ---------------------------------------------------------------- arms

def _implement(obj: str, ws: Path, rec, gate, root, tid: str):
    b = assemble(obj, ws, token_budget=8000)
    return _run_role("implementer", b, obj, ws, rec, gate, root, tid)


def _review(obj: str, ws: Path, impl, rec, gate, root, tid: str):
    b = assemble(obj, ws, token_budget=8000, path_hints=impl.files_written or None)
    return _run_role("reviewer", b, obj, ws, rec, gate, root, tid, mode="review",
                     extra="IMPLEMENTER SAID:\n" + impl.summary
                     + "\n\nFILES THE IMPLEMENTER ACTUALLY WROTE:\n"
                     + _files_blob(ws, impl.files_written))


def run_oneshot(obj, ws, cmd, tdir, prot, rec, gate, root, tid):
    _implement(obj, ws, rec, gate, root, tid)
    return {"calls": 1, "rounds": 1, "terminal": "done", "best_source": "round0",
            "kept_best": False}


def run_naive_loop(obj, ws, cmd, tdir, prot, rec, gate, root, tid):
    impl = _implement(obj, ws, rec, gate, root, tid)
    calls, rounds = 1, 1
    terminal = "exhausted"
    for r in range(MAX_ROUNDS):
        rev = _review(obj, ws, impl, rec, gate, root, tid)
        calls += 1
        verdict = str(rev.control.get("verdict", "")).lower().replace(" ", "-")
        if verdict != "needs-change":
            terminal = "reviewer-approved"
            break
        hint = rev.summary.strip().split(". ")[0]
        retry = obj + f"\n\nThe previous attempt did not pass: {hint}. Write the corrected file(s) now."
        impl = _implement(retry, ws, rec, gate, root, tid)
        calls += 1
        rounds += 1
    return {"calls": calls, "rounds": rounds, "terminal": terminal,
            "best_source": "last", "kept_best": False}


def run_d_loop(obj, ws, cmd, tdir, prot, rec, gate, root, tid):
    incumbent = score(ws, cmd, tdir, prot)
    best = {"score": incumbent, "snap": snap(ws, "inc"), "source": "incumbent"}
    last = dict(best)
    calls, rounds, stall = 0, 0, 0
    terminal = "exhausted"

    for r in range(MAX_ROUNDS):
        if best["score"]["sub"] == best["score"]["tot"] and best["score"]["tot"] > 0:
            terminal = "resolved"
            break
        work = snap(best["snap"], f"w{r}")
        hint = _fail_lines(best["score"]["tail"])
        step_obj = obj if (r == 0 and best["source"] == "incumbent"
                           and best["score"]["sub"] == 0) else (
            obj + f"\n\nCurrent state still fails these checks:\n{hint}\n"
            "Edit the file(s) to make them pass. Output the whole corrected file(s).")
        _implement(step_obj, work, rec, gate, root, tid)
        calls += 1
        rounds += 1
        s = score(work, cmd, tdir, prot)
        last = {"score": s, "snap": work, "source": f"round{r}"}
        if better(s, best["score"]):
            shutil.rmtree(best["snap"], ignore_errors=True)
            best = {"score": s, "snap": snap(work, f"b{r}"), "source": f"round{r}"}
            stall = 0
        else:
            stall += 1
            if stall > STALL_TOL:
                terminal = "stalled"
                break
    else:
        terminal = "exhausted"

    if best["score"]["sub"] == best["score"]["tot"] and best["score"]["tot"] > 0:
        terminal = "resolved"
    elif best["source"] == "incumbent":
        terminal = "no-improvement" if best["score"]["sub"] < best["score"]["tot"] else "already-passing"

    # materialise the winner into ws
    for p in ws.glob("*"):
        if p.is_file() and p.name != "test_task.py":
            p.unlink()
    for p in Path(best["snap"]).glob("*"):
        if p.is_file():
            shutil.copy2(p, ws / p.name)

    kept_best = better(best["score"], last["score"])
    for d in {best["snap"], last["snap"]}:
        shutil.rmtree(d, ignore_errors=True)
    return {"calls": calls, "rounds": rounds, "terminal": terminal,
            "best_source": best["source"], "kept_best": kept_best,
            "incumbent_sub": incumbent["sub"]}


ARMS = {"oneshot": run_oneshot, "naive_loop": run_naive_loop, "d_loop": run_d_loop}


# ---------------------------------------------------------------- driver

def run_cell(task, arm, rep, cmd, protected):
    ws = fresh_workspace(task["dir"])
    obj = task["objective"]
    rec = RunRecorder(RUNS, intent_text=obj,
                      meta={"task": task["id"], "arm": arm, "rep": rep, "suite": "loop_lab"})
    gate = Gate()
    root = rec.invocation(role=f"loop-{arm}", model_identity={"name": "harness"},
                          intent_ref=task["id"], config_ref="loop-lab")
    base = score(ws, cmd, task["dir"], protected)
    t0 = time.monotonic()
    meta = ARMS[arm](obj, ws, cmd, task["dir"], protected, rec, gate, root, task["id"])
    fin = score(ws, cmd, task["dir"], protected)
    wall = round(time.monotonic() - t0, 1)
    rec.close("completed")
    shutil.rmtree(ws, ignore_errors=True)
    row = {
        "task": task["id"], "kind": task["kind"], "arm": arm, "rep": rep,
        "baseline_sub": base["sub"], "final_sub": fin["sub"], "sub_tot": fin["tot"],
        "objective_pass": fin["pass"], "regressed": fin["sub"] < base["sub"],
        "wall_s": wall, **meta,
    }
    if task["id"] == "wf6_multi":
        row["doc"] = fin["doc"]
        row["todo"] = fin["todo"]
    return row


def summarise(rows):
    L = ["# Loop-lab results (bundle D)", "",
         f"_{time.strftime('%Y-%m-%d %H:%M')} - {len(rows)} runs, MAX_ROUNDS={MAX_ROUNDS}, "
         f"STALL_TOL={STALL_TOL}_", ""]
    for arm in ALL_ARMS:
        ar = [r for r in rows if r["arm"] == arm]
        if not ar:
            continue
        sub = sum(r["final_sub"] for r in ar)
        tot = sum(r["sub_tot"] for r in ar)
        reg = sum(r["regressed"] for r in ar)
        opass = sum(r["objective_pass"] for r in ar)
        calls = sum(r["calls"] for r in ar)
        L.append(f"- **{arm}**: obj pass {opass}/{len(ar)}, subtests {sub}/{tot} "
                 f"({100*sub/tot:.0f}%), **{reg} regressions vs baseline**, "
                 f"{calls} calls, mean wall {sum(r['wall_s'] for r in ar)/len(ar):.1f}s")
    L += ["", "| task | arm | rep | base | final | pass | regressed | rounds | calls | terminal | best_src | kept_best | wall |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["task"], r["arm"], r["rep"])):
        L.append(f"| {r['task']} | {r['arm']} | {r['rep']} | {r['baseline_sub']} | "
                 f"{r['final_sub']}/{r['sub_tot']} | {r['objective_pass']} | {r['regressed']} | "
                 f"{r.get('rounds','-')} | {r['calls']} | {r['terminal']} | "
                 f"{r.get('best_source','-')} | {r.get('kept_best','-')} | {r['wall_s']} |")
    # per-task mean, arms side by side
    L += ["", "## per task (mean final subtests)", "",
          "| task | oneshot | naive_loop | d_loop | d regressions |", "|---|---|---|---|---|"]
    for task in sorted({r["task"] for r in rows}):
        cells = []
        for arm in ALL_ARMS:
            xs = [r["final_sub"] for r in rows if r["task"] == task and r["arm"] == arm]
            cells.append(f"{sum(xs)/len(xs):.1f}" if xs else "-")
        dreg = sum(r["regressed"] for r in rows if r["task"] == task and r["arm"] == "d_loop")
        tot = next(r["sub_tot"] for r in rows if r["task"] == task)
        L.append(f"| {task} (/{tot}) | {cells[0]} | {cells[1]} | {cells[2]} | {dreg} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+", default=list(ALL_ARMS))
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    from _bridge import health
    if not health():
        print("Ollama not reachable", file=sys.stderr)
        raise SystemExit(2)

    RESULTS.mkdir(parents=True, exist_ok=True)
    tasks, cmd, protected = load_tasks()
    if args.smoke:
        tasks, args.reps, args.arms = tasks[:1], 1, ["d_loop"]

    rows, t0 = [], time.monotonic()
    total = len(tasks) * len(args.arms) * args.reps
    i = 0
    for task in tasks:
        for arm in args.arms:
            for rep in range(1, args.reps + 1):
                i += 1
                print(f"[{i}/{total}] {task['id']} / {arm} / rep {rep}", flush=True)
                row = run_cell(task, arm, rep, cmd, protected)
                rows.append(row)
                print(f"      base={row['baseline_sub']} final={row['final_sub']}/{row['sub_tot']} "
                      f"pass={row['objective_pass']} regressed={row['regressed']} "
                      f"term={row['terminal']} calls={row['calls']}", flush=True)
                (RESULTS / "results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
                (RESULTS / "summary.md").write_text(summarise(rows), encoding="utf-8")
    print(f"\n{(time.monotonic()-t0)/60:.1f} min\n")
    print(summarise(rows))


if __name__ == "__main__":
    main()
