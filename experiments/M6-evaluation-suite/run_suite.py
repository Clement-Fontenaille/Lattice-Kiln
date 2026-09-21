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
import traceback
import socket
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
RUNNER = f"{socket.gethostname()}-{os.getpid()}"

from _m6bridge import (Gate, RunRecorder, assemble, health,  # noqa: E402
                       meter_read, meter_reset, run_processor)

SUITE = HERE / "suite"
# LATTICE_RESULTS_SUBDIR lets a run against a different model land in its own
# results/ tree instead of overwriting the qwen2.5-coder baseline this suite
# was collected against -- run_task's output path keys only on arm name, not
# model, so switching model without switching this would silently corrupt or
# skip-as-already-done the existing rows (added 2026-09-15 alongside
# ollama_client.py's LATTICE_EVAL_MODEL, for the first Nemotron Nano 9B v2 pass).
RESULTS = HERE / os.environ.get("LATTICE_RESULTS_SUBDIR", "results")
SUITE_VERSION = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))["suite_version"]

# evalkit: every row records the setup that produced it, and lands in the
# setup-keyed store as `recorded`. Until 2026-09-20 a row's setup lived in the
# name of the directory it was written to, so reuse by another experiment meant
# reading directory names and diffing arm files against git history. Rows
# written from here need none of that.
#
# The legacy per-arm JSON is still written. Analysis scripts read it, and a
# transition that breaks every reader on day one is not a transition.
sys.path.insert(0, str(HERE.parent.parent / "evalkit"))
try:
    from setup_key import Cell            # noqa: E402
    from store import Store               # noqa: E402
    _STORE = Store()
except Exception as _e:                   # noqa: BLE001
    _STORE = None
    print(f"evalkit store unavailable, rows will not be keyed: {_e!r}", flush=True)
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
for _mod in ("m7_workflow", "m7b_workflow", "m7c_workflow", "m7e_workflow", "m7f_workflow", "judge_staged_workflow", "judge_anchored_workflow", "judge_caveat_workflow", "judge_bypass_workflow", "test_synth_workflow", "test_synth_retry_workflow", "judge_fullctx_workflow"):     # M7's arms live in their own dir
    try:
        ARMS.update(__import__(_mod).ARMS_EXTRA)
    except Exception as _e:  # noqa: BLE001
        print(f"({_mod} unavailable: {_e!r})", file=sys.stderr)


# --------------------------------------------------------------- driver

def _eval_params() -> dict:
    """Generation settings that were EXPLICITLY SET, and only those.

    num_ctx is deliberately absent. It is a ceiling, not a setting: it moved
    16384 -> 8192 on 2026-09-15 while observed usage stayed around 900-950
    tokens per call and nothing was ever seen to truncate. Keying on it refuses
    valid rows for a bound that never bound -- the same over-strictness as
    keying on a suite version when two fixtures of thirty-four changed. It is
    recorded in _eval_meta() instead, so an analysis that suspects truncation
    can still check it.
    """
    import ollama_client as _oc
    p = {}
    if _oc.THINK is not None:
        p["think"] = _oc.THINK
    if _oc.MIN_PREDICT:
        p["min_predict"] = _oc.MIN_PREDICT
    return p


def _eval_meta() -> dict:
    """Recorded, not keyed: the effective settings a run actually had."""
    import ollama_client as _oc
    return {"num_ctx": _oc.DEFAULT_NUM_CTX}


def _cell_for(task_id: str, arm_name: str):
    if _STORE is None:
        return None
    import ollama_client as _oc
    return Cell.make(task=task_id, arm=arm_name, backend=_oc.BACKEND,
                     model=_oc.DEFAULT_MODEL,
                     judge_format=os.environ.get("LATTICE_JUDGE_FORMAT",
                                                 "decision_first"),
                     params=_eval_params(), defaults=_eval_meta())


def _setup_of(task_id: str, arm_name: str):
    c = _cell_for(task_id, arm_name)
    return c.as_dict() if c else None


def run_task(task, arm_name, rep, cmd, protected):
    ws = fresh_ws(task)
    base = score(ws, cmd)          # always the complete check
    # Name the cell this rep belongs to before the arm runs, so the client can
    # file its raw generations under it. Without this the transcript is a loose
    # pile that has to be joined back heuristically -- and this session spent
    # most of itself learning what a heuristic join costs.
    _c = _cell_for(task["id"], arm_name)
    if _c is not None:
        os.environ["LATTICE_CELL"] = _c.id
    os.environ["LATTICE_REP"] = str(rep)
    meter_reset()
    t_start = time.time()
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
    # A raising arm produced NO attempt, so the workspace below is untouched and
    # scoring it measures the fixture, not the model. Both facts are recorded:
    # `run_ok` gates every downstream read, and the traceback is kept because the
    # repr alone ("'list' object has no attribute 'get'") cost a day of confusion
    # on 2026-09-17 -- 90 of judge_bypass's 102 rows were this, scored as results.
    run_ok, trace = True, None
    try:
        terminal = ARMS[arm_name](task["objective"], ws)
    except Exception as e:  # noqa: BLE001
        terminal = f"error:{e!r}"[:120]
        run_ok = False
        trace = traceback.format_exc()
    finally:
        os.environ.pop("M6_WORKER_VIEW", None)
        os.environ.pop("M6_TASK", None)
        os.environ.pop("M6_REP", None)
        os.environ.pop("LATTICE_CELL", None)
        os.environ.pop("LATTICE_REP", None)
    wall = round(time.monotonic() - t0, 1)
    t_end = time.time()
    used = meter_read()
    restore_protected(ws, task, protected)
    fin = score(ws, cmd)

    def frac(s):
        return s["scores"].get("SUBTESTS", (0, 1))

    bsub, btot = frac(base)
    fsub, ftot = frac(fin)
    new_fails = fin["fails"] - base["fails"]
    # Two readings, kept side by side. `gate_pass` is what the check's exit code
    # says, and several checks deliberately keep their structural dimensions out
    # of it -- wf6_multi's docstring calls them "quality signal, does not gate".
    # `objective_pass` is what that name has always been read to mean and now
    # does: the gate AND every recorded dimension at full marks. Operator ruling
    # 2026-09-18, E0 defect 1. Both are kept so old figures stay reproducible and
    # any analysis can say which reading it used.
    struct = {k: v for k, v in fin["scores"].items() if k != "SUBTESTS"}
    gate = fin["exit"] == 0 and not fin["crashed"]
    met = gate and all(e == t for e, t in struct.values())
    row = {
        "task": task["id"], "shape": task["shape"], "trap": task["trap"],
        "worker_view": view,
        "stresses": task["stresses"], "rep": rep, "arm": arm_name, "terminal": terminal,
        "baseline_sub": [bsub, btot], "final_sub": [fsub, ftot],
        "struct": struct,
        # None, not False, when the arm raised: the run produced no attempt, so
        # neither "passed" nor "failed" is true of it. None makes a downstream
        # reader that forgot to filter raise instead of quietly counting it.
        "gate_pass": gate if run_ok else None,
        "objective_pass": met if run_ok else None,
        "run_ok": run_ok, "error_trace": trace,
        "regressed": bool(new_fails) if run_ok else None,
        "new_fails": sorted(new_fails),
        "check_crashed": fin["crashed"],
        "decline_expected": task["expect"]["decline_correct"],
        # `run_ok` first: an unreachable model leaves the workspace untouched,
        # which is indistinguishable from a correct decline on any task whose
        # source already passes. Five false-premise tasks were credited with a
        # correct decline during a total outage before this guard existed.
        "declined_correctly": run_ok and task["expect"]["decline_correct"]
                              and terminal == "declined"
                              and fsub == bsub and not fin["fails"] - base["fails"],
        # Which fixture version produced this row. Added 2026-09-19: the 0.4.1
        # repair changed two fixtures, and nothing on a row said whether it came
        # from before or after, so reuse of recorded rows had to be argued from
        # file dates instead of read off the data.
        "suite_version": SUITE_VERSION,
        "setup": _setup_of(task["id"], arm_name),
        "setup_meta": _eval_meta(),
        "wall_s": wall, "tail": fin["out"],
        # What was actually generated inside that wall time, and when. `gen_s`
        # is the backend's decode time; `wall_s` is decode plus prompt plus
        # scoring plus every gap. The pair is what lets throughput be compared
        # across one worker and several: tokens/gen_s falls when two workers
        # share a card, tokens/wall_s rises if one's gaps cover the other's
        # decoding. `runner` and the timestamps let concurrency be reconstructed
        # from the rows themselves rather than declared alongside them.
        "llm_calls": used["calls"],
        "gen_tok": used["gen_tok"],
        "prompt_tok": used["prompt_tok"],
        "gen_s": round(used["gen_s"], 2),
        "prompt_s": round(used.get("prompt_s", 0.0), 2),
        "runner": RUNNER,
        "t_start": round(t_start, 3),
        "t_end": round(t_end, 3),
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

    # aggregate. Rows whose arm raised produced no attempt, so they are counted
    # separately and excluded from every rate -- a denominator that includes them
    # reports the fixture, not the model.
    ok_rows = [r for r in rows if r.get("run_ok", True)]
    nfail = len(rows) - len(ok_rows)
    npass = sum(r["objective_pass"] for r in ok_rows)
    nreg = sum(r["regressed"] for r in ok_rows)
    ncrash = sum(r["check_crashed"] for r in ok_rows)
    dec_rows = [r for r in ok_rows if r["decline_expected"]]
    dec_ok = sum(r["declined_correctly"] for r in dec_rows)
    L += ["", f"**objective pass {npass}/{len(ok_rows)} - regressions {nreg} - "
              f"check crashes {ncrash} - decline accuracy {dec_ok}/{len(dec_rows)}**", ""]
    if nfail:
        L += [f"> **{nfail} of {len(rows)} runs did not execute** (the arm raised; "
              f"`run_ok: false`). They are excluded from every figure above. See "
              f"`error_trace` in the JSON.", ""]

    # stresses slices - mean final subtest fraction per capability tag.
    # ok_rows, not rows: a run that never executed scores the untouched fixture,
    # which would drag every tag it carries toward the baseline.
    by_tag = defaultdict(list)
    for r in ok_rows:
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
    ap.add_argument("--store-resume", action="store_true",
                    help="also count reps the evalkit store already holds for "
                         "this exact setup, wherever they were produced. --resume "
                         "alone only sees this results directory, so a rep another "
                         "experiment already paid for would be run again.")
    ap.add_argument("--work", default=None,
                    help="a JSON file of [{task, rep}, ...] to run exactly, with "
                         "each row labelled with the rep given. This is how a "
                         "pool worker hands over a claimed batch: the pool owns "
                         "the rep numbers, so the runner must not invent its own.")
    ap.add_argument("--params-any", nargs="*", default=[],
                    help="param names to treat as `any` when asking the store "
                         "what it has, e.g. --params-any num_ctx. Affects "
                         "matching only; the run still records concrete values.")
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
    # What the store already holds for this exact setup, counted as reps that do
    # not need running again. Rep numbers are per-series labels, not identities,
    # so N reps held anywhere satisfy the first N of the target.
    held = {}
    if args.store_resume and _STORE is not None:
        wpath = HERE.parent.parent / "evalkit" / "waivers.json"
        wv = (json.loads(wpath.read_text(encoding="utf-8"))["waivers"]
              if wpath.is_file() else [])
        for t in tasks:
            cell = _cell_for(t["id"], args.arm)
            q = dict(json.loads(cell.params))
            for name in args.params_any:
                q[name] = "any"
            n = _STORE.have(cell, waivers=wv, params_query=q)
            if n:
                held[t["id"]] = n
        if held:
            print(f"store already holds {sum(held.values())} rep(s) across "
                  f"{len(held)} task(s) for this setup", flush=True)

    # A work list replaces the (tasks x reps) cross product entirely: the pool
    # decided what runs and under which rep number, and nothing here may
    # second-guess it.
    if args.work:
        work = json.loads(Path(args.work).read_text(encoding="utf-8"))
        by_id = {t["id"]: t for t in tasks}
        plan_items = [(by_id[w["task"]], int(w["rep"])) for w in work
                      if w["task"] in by_id]
    else:
        plan_items = [(t, r) for t in tasks for r in range(1, args.reps + 1)]

    total = len(plan_items)
    i = 0
    for task, rep in plan_items:
            i += 1
            if not args.work and (task["id"], rep) in done:
                continue
            if not args.work and rep <= held.get(task["id"], 0):
                continue
            print(f"[{i}/{total}] {task['id']} rep{rep} ({args.arm}) ...", flush=True)
            row = run_task(task, args.arm, rep, cmd, protected)
            rows.append(row)
            # Into the setup-keyed store as well, as `recorded`: the harness
            # knows its own setup, so this row never needs a migration manifest
            # to say what produced it. A store failure must not lose a run that
            # already cost real time, so it is reported and stepped over.
            if _STORE is not None:
                try:
                    _STORE.add(_cell_for(task["id"], args.arm), [row],
                               provenance="recorded", source="run_suite",
                               meta=_eval_meta())
                    for was, now in getattr(_STORE, "renumbered", []):
                        # Another run of this exact cell already used that rep
                        # number. Both draws are kept; the operator is told,
                        # because it means two runs raced on one cell.
                        print(f"      !! rep {was} already held for this cell, "
                              f"stored as rep {now} -- concurrent run?",
                              flush=True)
                except Exception as e:  # noqa: BLE001
                    print(f"      !! evalkit store write failed: {e!r}", flush=True)
            print(f"      {row['terminal']} base={row['baseline_sub']} final={row['final_sub']} "
                  f"pass={row['objective_pass']} regr={row['regressed']} "
                  f"crash={row['check_crashed']}", flush=True)
            (RESULTS / f"{args.arm}.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
            (RESULTS / f"{args.arm}.md").write_text(summarise(rows, args.arm, sv), encoding="utf-8")
    print(f"\n{(time.monotonic()-t0)/60:.1f} min\n\n{summarise(rows, args.arm, sv)}")


if __name__ == "__main__":
    main()
