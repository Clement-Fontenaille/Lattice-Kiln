"""M6 evaluation-suite runner. Arm-agnostic.

    python run_suite.py --arm baseline              # every task's pristine score
    python run_suite.py --arm monolith --reps 2
    python run_suite.py --arm dloop --tasks hf_extract_fn wf6_multi
    python run_suite.py --arm superpipe

An "arm" is a callable (objective, workspace_dir) -> terminal string
("resolved" | "needs-change" | "escalate" | "declined" | "done"). It mutates the
workspace in place. The runner restores protected files, scores, and records.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _m6bridge import Gate, RunRecorder, assemble, health, run_processor  # noqa: E402

SUITE = HERE / "suite"
RESULTS = HERE / "results"
RUNS = HERE / "runs"
_SCORE = re.compile(r"^([A-Z]+SCORE|SUBTESTS)\s+(\d+)\s*/\s*(\d+)", re.M)
_FAIL_LABEL = re.compile(r"^\s{2,}([^:]{2,70}):", re.M)


def load_tasks():
    d = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))
    return d["tasks"], d["check_command"], d["protected_files"], d["suite_version"]


def fresh_ws(task):
    dst = Path(tempfile.mkdtemp(prefix=f"m6_{task['id']}_")).resolve()
    shutil.copytree(SUITE / Path(task["dir"]).name, dst, dirs_exist_ok=True)
    for p in dst.rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)
    return dst


def restore_protected(ws, task, protected):
    src = SUITE / Path(task["dir"]).name
    for name in protected:
        if (src / name).is_file():
            shutil.copy2(src / name, ws / name)


def score(ws, cmd):
    try:
        cp = subprocess.run(cmd.split(), cwd=str(ws), capture_output=True, text=True, timeout=30)
        out = (cp.stdout + cp.stderr).strip()
    except subprocess.TimeoutExpired:
        return {"crashed": True, "scores": {}, "exit": -1, "fails": set(), "out": "TIMEOUT"}
    scores = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in _SCORE.finditer(out)}
    crashed = "SUBTESTS" not in scores or ("Traceback" in out and "SUBTESTS" not in out)
    return {"crashed": crashed, "scores": scores, "exit": cp.returncode,
            "fails": {m.group(1).strip() for m in _FAIL_LABEL.finditer(out)}, "out": out[-800:]}


# --------------------------------------------------------------- arms

def arm_baseline(objective, ws):
    return "done"


def arm_monolith(objective, ws):
    rec = RunRecorder(RUNS, intent_text=objective, meta={"arm": "monolith", "suite": "m6"})
    root = rec.invocation(role="m6-monolith", model_identity={"name": "harness"},
                          intent_ref="m6", config_ref="m6")
    b = assemble(objective, ws, token_budget=8000)
    run_processor(role="implementer", objective=objective, context=b, workspace_root=ws,
                  recorder=rec, gate=Gate(), parent_invocation_id=root, intent_ref="m6",
                  interaction_mode="oneshot")
    rec.close("completed")
    return "done"


ARMS = {"baseline": arm_baseline, "monolith": arm_monolith}
try:
    from m6_arms import ARMS_EXTRA
    ARMS.update(ARMS_EXTRA)          # dloop, staged
except Exception as _e:  # noqa: BLE001
    print(f"(m6_arms unavailable: {_e!r})", file=sys.stderr)
sys.path.insert(0, str(HERE.parent / "M7-static-workflow"))
for _mod in ("m7_workflow", "m7b_workflow", "m7c_workflow", "m7e_workflow", "m7f_workflow", "judge_staged_workflow", "judge_anchored_workflow", "judge_caveat_workflow", "judge_bypass_workflow", "test_synth_workflow", "judge_fullctx_workflow"):     # M7's arms live in their own dir
    try:
        ARMS.update(__import__(_mod).ARMS_EXTRA)
    except Exception as _e:  # noqa: BLE001
        print(f"({_mod} unavailable: {_e!r})", file=sys.stderr)


# --------------------------------------------------------------- driver

def run_task(task, arm_name, rep, cmd, protected):
    ws = fresh_ws(task)
    base = score(ws, cmd)          # always the complete check
    t0 = time.monotonic()
    # The worker may be shown less than the check measures. Set only around
    # the arm, never around scoring, so ground truth is identical for every
    # task whatever the arm was allowed to see.
    view = task.get("worker_view", "full")
    if view != "full":
        os.environ["M6_WORKER_VIEW"] = view
    # An arm logs its own stage record and cannot otherwise know WHICH rep it is
    # in, which makes per-rep matching impossible for anything at N>1 and
    # silently invites collapsing five draws on one side of a comparison and not
    # the other. Cheap to carry, so carry it.
    os.environ["M6_TASK"] = task["id"]
    os.environ["M6_REP"] = str(rep)
    try:
        terminal = ARMS[arm_name](task["objective"], ws)
    except Exception as e:  # noqa: BLE001
        terminal = f"error:{e!r}"[:120]
    finally:
        os.environ.pop("M6_WORKER_VIEW", None)
        os.environ.pop("M6_TASK", None)
        os.environ.pop("M6_REP", None)
    wall = round(time.monotonic() - t0, 1)
    restore_protected(ws, task, protected)
    fin = score(ws, cmd)

    def frac(s):
        return s["scores"].get("SUBTESTS", (0, 1))

    bsub, btot = frac(base)
    fsub, ftot = frac(fin)
    new_fails = fin["fails"] - base["fails"]
    row = {
        "task": task["id"], "shape": task["shape"], "trap": task["trap"],
        "worker_view": view,
        "stresses": task["stresses"], "rep": rep, "arm": arm_name, "terminal": terminal,
        "baseline_sub": [bsub, btot], "final_sub": [fsub, ftot],
        "struct": {k: v for k, v in fin["scores"].items() if k != "SUBTESTS"},
        "objective_pass": fin["exit"] == 0 and not fin["crashed"],
        "regressed": bool(new_fails), "new_fails": sorted(new_fails),
        "check_crashed": fin["crashed"],
        "decline_expected": task["expect"]["decline_correct"],
        "declined_correctly": task["expect"]["decline_correct"] and terminal == "declined"
                              and fsub == bsub and not fin["fails"] - base["fails"],
        "wall_s": wall, "tail": fin["out"],
    }
    shutil.rmtree(ws, ignore_errors=True)
    return row


def summarise(rows, arm, suite_version):
    L = [f"# M6 suite run - arm `{arm}` (suite {suite_version})", "",
         f"_{time.strftime('%Y-%m-%d %H:%M')} - {len(rows)} runs_", "",
         "| task | shape/trap | terminal | base | final | struct | pass | regr | decline | wall |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["task"], r["rep"])):
        st = " ".join(f"{k}={v[0]}/{v[1]}" for k, v in r["struct"].items()) or "-"
        dec = ("ok" if r["declined_correctly"] else "MISS") if r["decline_expected"] else "-"
        L.append(f"| {r['task']} | {r['shape']}/{r['trap']} | {r['terminal']} | "
                 f"{r['baseline_sub'][0]}/{r['baseline_sub'][1]} | "
                 f"{r['final_sub'][0]}/{r['final_sub'][1]} | {st} | {r['objective_pass']} | "
                 f"{'YES' if r['regressed'] else '-'} | {dec} | {r['wall_s']} |")

    # aggregate
    npass = sum(r["objective_pass"] for r in rows)
    nreg = sum(r["regressed"] for r in rows)
    ncrash = sum(r["check_crashed"] for r in rows)
    dec_rows = [r for r in rows if r["decline_expected"]]
    dec_ok = sum(r["declined_correctly"] for r in dec_rows)
    L += ["", f"**objective pass {npass}/{len(rows)} - regressions {nreg} - "
              f"check crashes {ncrash} - decline accuracy {dec_ok}/{len(dec_rows)}**", ""]

    # stresses slices - mean final subtest fraction per capability tag
    by_tag = defaultdict(list)
    for r in rows:
        f = r["final_sub"][0] / max(1, r["final_sub"][1])
        for tag in r["stresses"]:
            by_tag[tag].append(f)
    L += ["## `stresses` slices (mean final SUBTESTS fraction)", "",
          "| capability | n | mean |", "|---|---|---|"]
    for tag, xs in sorted(by_tag.items()):
        L.append(f"| {tag} | {len(xs)} | {sum(xs)/len(xs):.2f} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="baseline", choices=list(ARMS))
    ap.add_argument("--tasks", nargs="+")
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--resume", action="store_true",
                    help="keep rows already recorded for this arm and run only the "
                         "(task, rep) pairs that are missing. Makes a long queue "
                         "survive being interrupted, which it otherwise does not.")
    args = ap.parse_args()
    if args.arm not in ("baseline",) and not health():
        print("Ollama not reachable", file=sys.stderr)
        raise SystemExit(2)

    tasks, cmd, protected, sv = load_tasks()
    if args.tasks:
        tasks = [t for t in tasks if t["id"] in args.tasks]
    RESULTS.mkdir(parents=True, exist_ok=True)
    RUNS.mkdir(exist_ok=True)

    rows, t0 = [], time.monotonic()
    done = set()
    out_json = RESULTS / f"{args.arm}.json"
    if args.resume and out_json.is_file():
        rows = json.loads(out_json.read_text(encoding="utf-8"))
        done = {(r["task"], r["rep"]) for r in rows}
        print(f"resuming: {len(done)} rows already recorded", flush=True)
    total = len(tasks) * args.reps
    i = 0
    for task in tasks:
        for rep in range(1, args.reps + 1):
            i += 1
            if (task["id"], rep) in done:
                continue
            print(f"[{i}/{total}] {task['id']} rep{rep} ({args.arm}) ...", flush=True)
            row = run_task(task, args.arm, rep, cmd, protected)
            rows.append(row)
            print(f"      {row['terminal']} base={row['baseline_sub']} final={row['final_sub']} "
                  f"pass={row['objective_pass']} regr={row['regressed']} "
                  f"crash={row['check_crashed']}", flush=True)
            (RESULTS / f"{args.arm}.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
            (RESULTS / f"{args.arm}.md").write_text(summarise(rows, args.arm, sv), encoding="utf-8")
    print(f"\n{(time.monotonic()-t0)/60:.1f} min\n\n{summarise(rows, args.arm, sv)}")


if __name__ == "__main__":
    main()
