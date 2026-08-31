"""M5 re-test on workflow-shaped tasks.

Answers the two clauses of the M5 evidence question on the right axis:
  (1) does a role sequence beat a plain monolith on multi-phase work, and
  (2) where does the extra cost stop being covered by the outcome gain.

Arms:
  - monolith     : one implementer, one pass.
  - fixed        : planner -> implementer -> (reviewer -> implementer)* up to
                   FIXED_ROUNDS review/fix rounds, stopping when the reviewer
                   approves. Iteration budget comparable to the orchestrator's.
  - orchestrated : the LLM orchestrator (added later; --arms orchestrated).

Scoring is subtests-passed (partial credit), not just pass/fail. test_task.py is
restored from the pristine fixture before scoring so an arm cannot "fix" the test.

    python experiments/M5-intelligent-orchestration/workflow_suite.py --arms monolith fixed
    python experiments/M5-intelligent-orchestration/workflow_suite.py --smoke
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from _bridge import Gate, RunRecorder, assemble, run_processor  # noqa: E402
from roles_v2 import build_prompt  # noqa: E402
from orchestrator import run_orchestrated  # noqa: E402

FIXTURE = HERE / "fixture_workflow"
RUNS = HERE / "runs"
RESULTS = HERE / "results_workflow"
ALL_ARMS = ("monolith", "fixed", "orchestrated")
_SUBTESTS = re.compile(r"SUBTESTS\s+(\d+)\s*/\s*(\d+)")
_DOCSCORE = re.compile(r"DOCSCORE\s+(\d+)\s*/\s*(\d+)")
_TODOSCORE = re.compile(r"TODOSCORE\s+(\d+)\s*/\s*(\d+)")
FIXED_ROUNDS = 3  # max review->fix rounds for the fixed arm (budget ~= orchestrator)
_PLACEHOLDER_PATHS = ("relative/name.py", "the/real/relative/path.py", "path/to/file",
                      "client/ratelimiter.py")
_DONE_WORDS = re.compile(r"\b(fixed|updated|implemented|added|resolved|corrected|"
                         r"has been|have been|now correctly|now passes|all tests pass)\b",
                         re.IGNORECASE)


def _wrote_real_files(pr) -> bool:
    fs = [f.strip().lower() for f in pr.files_written]
    return bool(fs) and not any(f in _PLACEHOLDER_PATHS for f in fs)


def _neutralize(text: str) -> str:
    """A 7B planner ignores 'no past tense' and writes 'Fixed X / all tests pass',
    which flips the downstream implementer into completion-report mode. Blunt the
    completion phrasing before it reaches the implementer."""
    return _DONE_WORDS.sub("TODO:", text or "")


def _run_role(role, bundle, obj, ws, rec, gate, root, task_id, extra=None, mode="oneshot"):
    return run_processor(role=role, objective=obj, context=bundle, workspace_root=ws,
                         recorder=rec, gate=gate, parent_invocation_id=root, intent_ref=task_id,
                         interaction_mode=mode, extra_input=extra,
                         prompt=build_prompt(role, bundle.render(), obj, extra),
                         config_ref="m5-roles-v2")


def load_tasks() -> tuple[list[dict], str, list[str]]:
    doc = json.loads((FIXTURE / "tasks.json").read_text(encoding="utf-8"))
    return doc["tasks"], doc["check_command"], doc.get("protected_files", [])


def fresh_workspace(task_dir: str) -> Path:
    dst = Path(tempfile.mkdtemp(prefix=f"m5wf_{task_dir}_")).resolve()
    shutil.copytree(FIXTURE / task_dir, dst, dirs_exist_ok=True)
    return dst


def restore_protected(ws: Path, task_dir: str, protected: list[str]) -> None:
    for name in protected:
        src = FIXTURE / task_dir / name
        if src.is_file():
            shutil.copy2(src, ws / name)


def objective_check(ws: Path, cmd: str) -> dict:
    """-> {pass: bool, sub: (p, t), doc: (p, t)|None, todo: (p, t)|None, tail: str}"""
    import subprocess
    try:
        cp = subprocess.run(cmd.split(), cwd=str(ws), capture_output=True, text=True, timeout=60)
        out = (cp.stdout + cp.stderr).strip()
    except (subprocess.TimeoutExpired, OSError) as e:
        return {"pass": False, "sub": (0, 0), "doc": None, "todo": None, "tail": f"<check error: {e}>"}

    def grab(rx):
        m = rx.search(out)
        return (int(m.group(1)), int(m.group(2))) if m else None

    return {"pass": cp.returncode == 0, "sub": grab(_SUBTESTS) or (0, 0),
            "doc": grab(_DOCSCORE), "todo": grab(_TODOSCORE), "tail": out[-500:]}


def _files_blob(ws: Path, rels: list[str]) -> str:
    out = []
    for rel in rels:
        p = ws / rel
        if p.is_file():
            out.append(f"--- {rel} ---\n{p.read_text(encoding='utf-8', errors='replace')}")
    return "\n\n".join(out) or "(no files written)"


def _source_blob(ws: Path) -> str:
    rels = sorted(p.name for p in ws.glob("*.py") if p.name != "test_task.py")
    return _files_blob(ws, rels)


def run_arm(task: dict, arm: str, rep: int, cmd: str, protected: list[str]) -> dict:
    ws = fresh_workspace(task["dir"])
    obj = task["objective"]
    rec = RunRecorder(RUNS, intent_text=obj,
                      meta={"task": task["id"], "kind": task["kind"], "arm": arm, "rep": rep,
                            "suite": "workflow"})
    gate = Gate()
    t0 = time.monotonic()
    root = rec.invocation(role=f"harness-{arm}", model_identity={"name": "harness"},
                          intent_ref=task["id"], config_ref="m5-workflow")
    bc = objective_check(ws, cmd)
    b_pass, b_tot = bc["sub"]
    rec.realized_effect(root, effect_type=2,
                        envelope={"command": cmd, "phase": "baseline", "representable": True,
                                  "attributable": root, "reversible": "n/a"},
                        outcome="realized", result_ref=f"baseline {b_pass}/{b_tot}")

    procs = []
    calls = 0
    if arm == "monolith":
        b = assemble(obj, ws, token_budget=8000)
        impl = _run_role("implementer", b, obj, ws, rec, gate, root, task["id"])
        procs = [impl]
        calls = 1
    elif arm == "fixed":
        # planner -> implementer -> (reviewer -> implementer)* up to FIXED_ROUNDS
        # review/fix rounds. Iteration budget comparable to the orchestrator's.
        # Deterministic guard: an implementer that wrote no real files is forced
        # to needs-change regardless of what the (unreliable 7B) reviewer says.
        b1 = assemble(obj, ws, token_budget=8000)
        plan = _run_role("planner", b1, obj, ws, rec, gate, root, task["id"])
        # NB: the planner's prose is deliberately NOT injected into the first
        # implementer. On a 7B, any ADDITIONAL INPUT text flips the implementer
        # from "act" to "discuss" and it stops emitting FILE blocks (the monolith,
        # which gets no extra input, writes reliably). The planner runs and is
        # recorded; its value to the chain is what this arm is measuring.
        b2 = assemble(obj, ws, token_budget=8000)
        last_impl = _run_role("implementer", b2, obj, ws, rec, gate, root, task["id"])
        procs = [plan, last_impl]
        calls = 2
        for _round in range(FIXED_ROUNDS):
            wrote = _wrote_real_files(last_impl)
            if wrote:
                b3 = assemble(obj, ws, token_budget=8000, path_hints=last_impl.files_written or None)
                rev = _run_role("reviewer", b3, obj, ws, rec, gate, root, task["id"], mode="review",
                                extra="IMPLEMENTER SAID:\n" + last_impl.summary
                                + "\n\nFILES THE IMPLEMENTER ACTUALLY WROTE:\n"
                                + _files_blob(ws, last_impl.files_written))
                procs.append(rev)
                calls += 1
                verdict = str(rev.control.get("verdict", "")).lower().replace(" ", "-")
                if verdict != "needs-change":
                    break
                fix_hint = _neutralize(rev.summary.strip().split(". ")[0])
            else:
                fix_hint = "the previous attempt wrote no file - nothing changed yet"
            # Retry: fold the revision hint into the OBJECTIVE, not ADDITIONAL
            # INPUT. Extra input flips a 7B implementer into "discuss" mode; the
            # objective section keeps it in "act" mode.
            retry_obj = (obj + f"\n\nThe first attempt did not pass: {fix_hint}. "
                         "Write the corrected file(s) now.")
            b4 = assemble(obj, ws, token_budget=8000)
            last_impl = _run_role("implementer", b4, retry_obj, ws, rec, gate, root, task["id"])
            procs.append(last_impl)
            calls += 1
        orch = None
    elif arm == "orchestrated":
        orch = run_orchestrated(objective=obj, workspace_root=ws, recorder=rec, gate=gate,
                                parent_invocation_id=root, intent_ref=task["id"])
        calls = orch.model_calls
    else:
        raise SystemExit(f"unknown arm {arm}")

    restore_protected(ws, task["dir"], protected)
    fc = objective_check(ws, cmd)
    obj_pass, (n_pass, n_tot), tail = fc["pass"], fc["sub"], fc["tail"]
    rec.realized_effect(root, effect_type=2,
                        envelope={"command": cmd, "phase": "final", "representable": True,
                                  "attributable": root, "reversible": "n/a"},
                        outcome="realized", result_ref=f"final {n_pass}/{n_tot} pass={obj_pass}")
    wall = round(time.monotonic() - t0, 1)
    rec.close("completed")
    if arm == "orchestrated":
        impl_files = list(orch.files_written)
        declined = orch.terminal_state == "abandoned"
        parse_ok = True
        extra_cols = {"orch_terminal": orch.terminal_state,
                      "spawn_sequence": [s.role for s in orch.steps if s.op == "spawn"]}
    else:
        impl_files = sorted({f for p in procs for f in p.files_written})
        declined = any(p.terminal_state == "declined" for p in procs)
        parse_ok = all(p.parse_ok for p in procs)
        extra_cols = {}
    shutil.rmtree(ws, ignore_errors=True)

    return {
        "task": task["id"], "kind": task["kind"], "arm": arm, "rep": rep, "run_id": rec.run_id,
        "objective_pass": obj_pass, "subtests": n_pass, "subtests_total": n_tot,
        "baseline_subtests": b_pass,
        "doc_score": fc["doc"], "todo_score": fc["todo"],
        "declined": declined,
        "decline_expected": bool(task["expect"].get("decline_correct")),
        "model_calls": calls, "wall_s": wall, "impl_files": impl_files,
        "parse_ok": parse_ok, "check_tail": tail, **extra_cols,
    }


def ledger(rows: list[dict]) -> str:
    by = {}
    for r in rows:
        by.setdefault(r["task"], {})[r["arm"]] = r
    L = ["", "## Cost/benefit ledger (fixed vs monolith, mean over reps)", "",
         "| task | mono subtests | fixed subtests | d subtests | mono calls | fixed calls | d calls | verdict |",
         "|---|---|---|---|---|---|---|---|"]
    for task, arms in sorted(by.items()):
        if "monolith" not in arms or "fixed" not in arms:
            continue
        m, f = arms["monolith"], arms["fixed"]
        mp = _mean(rows, task, "monolith", "subtests")
        fp = _mean(rows, task, "fixed", "subtests")
        tot = m["subtests_total"]
        dsub = fp - mp
        dcalls = _mean(rows, task, "fixed", "model_calls") - _mean(rows, task, "monolith", "model_calls")
        v = ("fixed helps" if dsub > 0.5 else "no gain" if abs(dsub) <= 0.5 else "fixed worse")
        L.append(f"| {task} | {mp:.1f}/{tot} | {fp:.1f}/{tot} | {dsub:+.1f} | "
                 f"{_mean(rows, task, 'monolith', 'model_calls'):.0f} | "
                 f"{_mean(rows, task, 'fixed', 'model_calls'):.0f} | {dcalls:+.1f} | {v} |")
    return "\n".join(L)


def _mean(rows, task, arm, key):
    xs = [r[key] for r in rows if r["task"] == task and r["arm"] == arm]
    return sum(xs) / len(xs) if xs else 0.0


def summarise(rows: list[dict]) -> str:
    L = ["# M5 workflow-suite results", "", f"_{time.strftime('%Y-%m-%d %H:%M')} - {len(rows)} runs_", ""]
    for arm in ALL_ARMS:
        ar = [r for r in rows if r["arm"] == arm]
        if not ar:
            continue
        opass = sum(r["objective_pass"] for r in ar)
        sub = sum(r["subtests"] for r in ar)
        subt = sum(r["subtests_total"] for r in ar)
        L.append(f"- **{arm}**: objective pass {opass}/{len(ar)}, subtests {sub}/{subt} "
                 f"({100*sub/subt:.0f}%), {sum(r['model_calls'] for r in ar)} calls, "
                 f"mean wall {sum(r['wall_s'] for r in ar)/len(ar):.1f}s")
    L += ["", "| task | kind | arm | rep | obj_pass | subtests | declined | calls | wall_s |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["task"], r["arm"], r["rep"])):
        L.append(f"| {r['task']} | {r['kind']} | {r['arm']} | {r['rep']} | {r['objective_pass']} | "
                 f"{r['subtests']}/{r['subtests_total']} | {r['declined']} | {r['model_calls']} | {r['wall_s']} |")
    # wf6_multi: doc/todo quality per arm (does an arm drop these while doing the algo?)
    wf6 = [r for r in rows if r["task"] == "wf6_multi" and r.get("doc_score")]
    if wf6:
        L += ["", "### wf6_multi secondary concerns (mean over reps)",
              "| arm | algo subtests | doc score | todo score |", "|---|---|---|---|"]
        for arm in ALL_ARMS:
            a = [r for r in wf6 if r["arm"] == arm]
            if not a:
                continue
            ms = sum(r["subtests"] for r in a) / len(a)
            md = sum(r["doc_score"][0] for r in a) / len(a)
            mt = sum(r["todo_score"][0] for r in a) / len(a)
            L.append(f"| {arm} | {ms:.1f}/6 | {md:.1f}/4 | {mt:.1f}/3 |")
    L.append(ledger(rows))
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--arms", nargs="+", default=["monolith", "fixed"])
    args = ap.parse_args()

    from _bridge import health
    if not health():
        print("Ollama not reachable - aborting.")
        raise SystemExit(2)

    RUNS.mkdir(exist_ok=True)
    RESULTS.mkdir(exist_ok=True)
    tasks, cmd, protected = load_tasks()
    if args.smoke:
        tasks, args.reps = tasks[:1], 1

    rows: list[dict] = []
    total = len(tasks) * len(args.arms) * args.reps
    i = 0
    for task in tasks:
        for arm in args.arms:
            for rep in range(1, args.reps + 1):
                i += 1
                print(f"[{i}/{total}] {task['id']} / {arm} / rep {rep} ...", flush=True)
                row = run_arm(task, arm, rep, cmd, protected)
                rows.append(row)
                print(f"      obj_pass={row['objective_pass']} subtests={row['subtests']}/{row['subtests_total']} "
                      f"declined={row['declined']} calls={row['model_calls']} wall={row['wall_s']}s", flush=True)
                RESULTS.mkdir(parents=True, exist_ok=True)
                (RESULTS / "results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
                (RESULTS / "summary.md").write_text(summarise(rows), encoding="utf-8")

    print("\n" + summarise(rows))


if __name__ == "__main__":
    main()
