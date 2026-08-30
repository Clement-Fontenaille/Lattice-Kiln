"""M4 comparison harness - arm A (monolith) vs arm B (ephemeral split).

For each (task, arm, repetition): a fresh workspace copy, one RunRecorder run
spanning the whole orchestration, an objective pytest-style check before and
after, and a row of results. Every model effect goes through the M3 floor; every
event is recorded. A human reviews the runs afterwards (MVP invariant).

    python experiments/M4-ephemeral-processors/harness.py            # 4 tasks x N=2, both arms
    python experiments/M4-ephemeral-processors/harness.py --smoke    # 1 task x N=1
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from _bridge import Gate, Run, RunRecorder  # noqa: E402
from context_assembly import assemble  # noqa: E402
from ollama_client import health  # noqa: E402
from processor import run_processor  # noqa: E402

FIXTURE = HERE / "fixture"
RUNS = HERE / "runs"
RESULTS = HERE / "results"
ARMS = ("monolith", "ephemeral")


def load_tasks() -> tuple[list[dict], str]:
    doc = json.loads((FIXTURE / "tasks.json").read_text(encoding="utf-8"))
    return doc["tasks"], doc["check_command"]


def fresh_workspace(task_dir: str) -> Path:
    dst = Path(tempfile.mkdtemp(prefix=f"m4_{task_dir}_")).resolve()
    shutil.copytree(FIXTURE / task_dir, dst, dirs_exist_ok=True)
    return dst


def objective_check(ws: Path, check_command: str) -> tuple[bool, str]:
    try:
        cp = subprocess.run(check_command.split(), cwd=str(ws), capture_output=True,
                            text=True, timeout=60)
        return cp.returncode == 0, (cp.stdout + cp.stderr).strip()[-400:]
    except (subprocess.TimeoutExpired, OSError) as e:
        return False, f"<check error: {e}>"


def _files_blob(ws: Path, rels: list[str]) -> str:
    out = []
    for rel in rels:
        p = ws / rel
        if p.is_file():
            out.append(f"--- {rel} ---\n{p.read_text(encoding='utf-8', errors='replace')}")
    return "\n\n".join(out) or "(implementer wrote no files)"


def run_one(task: dict, arm: str, rep: int, check_command: str) -> dict:
    ws = fresh_workspace(task["dir"])
    obj = task["objective"]
    rec = RunRecorder(RUNS, intent_text=obj,
                      meta={"task": task["id"], "kind": task["kind"], "arm": arm, "rep": rep})
    gate = Gate()
    t0 = time.monotonic()
    root = rec.invocation(role=f"harness-{arm}", model_identity={"name": "harness"},
                          intent_ref=task["id"], config_ref="m4-harness")
    base_pass, _ = objective_check(ws, check_command)
    rec.realized_effect(root, effect_type=2,
                        envelope={"command": check_command, "phase": "baseline",
                                  "representable": True, "attributable": root, "reversible": "n/a"},
                        outcome="realized", result_ref=f"baseline_pass={base_pass}")

    procs = []
    ctx_reqs: list[str] = []
    reviewer_verdict = None

    if arm == "monolith":
        b = assemble(obj, ws, token_budget=8000)
        impl = run_processor(role="implementer", objective=obj, context=b, workspace_root=ws,
                             recorder=rec, gate=gate, parent_invocation_id=root, intent_ref=task["id"])
        procs = [impl]
        ctx_reqs = list(impl.context_requests)
    else:
        b1 = assemble(obj, ws, token_budget=8000)
        plan = run_processor(role="planner", objective=obj, context=b1, workspace_root=ws,
                             recorder=rec, gate=gate, parent_invocation_id=root, intent_ref=task["id"])
        b2 = assemble(obj, ws, token_budget=8000)
        impl = run_processor(role="implementer", objective=obj, context=b2, workspace_root=ws,
                             recorder=rec, gate=gate, parent_invocation_id=root, intent_ref=task["id"],
                             extra_input="PLAN FROM THE PLANNER:\n" + (plan.body_text or plan.summary))
        b3 = assemble(obj, ws, token_budget=8000, path_hints=impl.files_written or None)
        rev = run_processor(role="reviewer", objective=obj, context=b3, workspace_root=ws,
                            recorder=rec, gate=gate, parent_invocation_id=root, intent_ref=task["id"],
                            interaction_mode="review",
                            extra_input="IMPLEMENTER'S STATED CONCLUSION:\n" + impl.summary
                            + "\n\nFILES THE IMPLEMENTER WROTE:\n" + _files_blob(ws, impl.files_written))
        procs = [plan, impl, rev]
        ctx_reqs = list(plan.context_requests) + list(impl.context_requests)
        v = str(rev.control.get("verdict", "")).lower().replace(" ", "-")
        if v in ("approve", "needs-change"):
            reviewer_verdict = v
        else:
            u = rev.summary.upper()
            reviewer_verdict = ("needs-change" if ("NEEDS-CHANGE" in u or "NEEDS CHANGE" in u)
                                else "approve" if "APPROVE" in u else "unclear")

    obj_pass, check_tail = objective_check(ws, check_command)
    rec.realized_effect(root, effect_type=2,
                        envelope={"command": check_command, "phase": "final",
                                  "representable": True, "attributable": root, "reversible": "n/a"},
                        outcome="realized", result_ref=f"objective_pass={obj_pass}")
    wall = round(time.monotonic() - t0, 1)
    rec.close("completed")
    shutil.rmtree(ws, ignore_errors=True)

    declined = any(p.terminal_state == "declined" for p in procs)
    return {
        "task": task["id"], "kind": task["kind"], "arm": arm, "rep": rep,
        "run_id": rec.run_id,
        "baseline_pass": base_pass, "objective_pass": obj_pass,
        "declined": declined,
        "decline_expected": bool(task["expect"].get("decline_correct")),
        "reviewer_verdict": reviewer_verdict,
        "context_requests": ctx_reqs,
        "needs_extra_file": task["expect"].get("needs_extra_file"),
        "model_calls": len(procs),
        "impl_files": next((p.files_written for p in procs if p.role == "implementer"), []),
        "refused_by_gate": sum(p.refused_by_gate for p in procs),
        "refused_by_policy": sum(p.refused_by_policy for p in procs),
        "parse_ok": all(p.parse_ok for p in procs),
        "tok_s": [p.gen_tokens_per_s for p in procs],
        "wall_s": wall,
        "check_tail": check_tail,
    }


def summarise(rows: list[dict]) -> str:
    lines = ["# M4 comparison results", ""]
    lines.append(f"_{time.strftime('%Y-%m-%d %H:%M')} - {len(rows)} runs_\n")
    # per-arm objective pass rate
    for arm in ARMS:
        ar = [r for r in rows if r["arm"] == arm]
        if not ar:
            continue
        npass = sum(r["objective_pass"] for r in ar)
        lines.append(f"- **{arm}**: objective pass {npass}/{len(ar)}, "
                     f"mean wall {sum(r['wall_s'] for r in ar) / len(ar):.1f}s, "
                     f"{sum(r['model_calls'] for r in ar)} model calls total")
    lines.append("")
    lines.append("| task | kind | arm | rep | obj_pass | declined | reviewer | ctx_reqs | gate_ref | wall_s |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: (r["task"], r["arm"], r["rep"])):
        lines.append("| {task} | {kind} | {arm} | {rep} | {objective_pass} | {declined} | "
                     "{rv} | {cr} | {refused_by_gate} | {wall_s} |".format(
                         rv=r["reviewer_verdict"] or "-",
                         cr=len(r["context_requests"]), **r))
    lines.append("")
    lines.append("## Notes for the findings entries")
    lines.append("- M4: compare monolith vs ephemeral objective pass rates above.")
    lines.append("- M3: inspect `refused_by_gate` / effect stream for type-boundary blur.")
    lines.append("- M2: pick an unplanned question and answer it from the run records.")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--smoke", action="store_true", help="1 task x 1 rep")
    ap.add_argument("--arms", nargs="+", default=list(ARMS))
    args = ap.parse_args()

    if not health():
        print("Ollama not reachable on localhost:11434 - aborting.")
        raise SystemExit(2)

    RUNS.mkdir(exist_ok=True)
    RESULTS.mkdir(exist_ok=True)
    tasks, check_command = load_tasks()
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
                row = run_one(task, arm, rep, check_command)
                rows.append(row)
                print(f"      obj_pass={row['objective_pass']} declined={row['declined']} "
                      f"reviewer={row['reviewer_verdict']} ctx_reqs={len(row['context_requests'])} "
                      f"gate_ref={row['refused_by_gate']} wall={row['wall_s']}s", flush=True)

    (RESULTS / "results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    (RESULTS / "summary.md").write_text(summarise(rows), encoding="utf-8")
    print(f"\nwrote {RESULTS/'results.json'} and {RESULTS/'summary.md'}")
    print(summarise(rows))


if __name__ == "__main__":
    main()
