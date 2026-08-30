"""M5 comparison harness - monolith vs M4 fixed chain vs LLM orchestrator.

Reuses the M4 fixture task set and its monolith / ephemeral arms unchanged, and
adds the `orchestrated` arm driven by orchestrator.run_orchestrated.

    python experiments/M5-intelligent-orchestration/compare.py                 # 3 arms x 4 tasks x N=2
    python experiments/M5-intelligent-orchestration/compare.py --arms orchestrated
    python experiments/M5-intelligent-orchestration/compare.py --smoke
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from _bridge import Gate, RunRecorder, health  # noqa: E402  (puts M2/M3/M4 dirs on path)
import harness as _m4  # noqa: E402  (M4's harness.py)
from harness import (fresh_workspace, load_tasks, objective_check,  # noqa: E402
                     run_one as run_fixed_arm)
from orchestrator import run_orchestrated  # noqa: E402

RUNS = HERE / "runs"
RESULTS = HERE / "results"
ALL_ARMS = ("monolith", "ephemeral", "orchestrated")

# fixed-arm runs go into M5's runs/ tree, not M4's
_m4.RUNS = RUNS


def run_orchestrated_task(task: dict, rep: int, check_command: str) -> dict:
    ws = fresh_workspace(task["dir"])
    obj = task["objective"]
    rec = RunRecorder(RUNS, intent_text=obj,
                      meta={"task": task["id"], "kind": task["kind"], "arm": "orchestrated", "rep": rep})
    gate = Gate()
    t0 = time.monotonic()
    root = rec.invocation(role="harness-orchestrated", model_identity={"name": "harness"},
                          intent_ref=task["id"], config_ref="m5-harness")
    base_pass, _ = objective_check(ws, check_command)
    rec.realized_effect(root, effect_type=2,
                        envelope={"command": check_command, "phase": "baseline",
                                  "representable": True, "attributable": root, "reversible": "n/a"},
                        outcome="realized", result_ref=f"baseline_pass={base_pass}")

    orch = run_orchestrated(objective=obj, workspace_root=ws, recorder=rec, gate=gate,
                            parent_invocation_id=root, intent_ref=task["id"])

    obj_pass, check_tail = objective_check(ws, check_command)
    rec.realized_effect(root, effect_type=2,
                        envelope={"command": check_command, "phase": "final",
                                  "representable": True, "attributable": root, "reversible": "n/a"},
                        outcome="realized", result_ref=f"objective_pass={obj_pass}")
    wall = round(time.monotonic() - t0, 1)
    rec.close("completed")
    shutil.rmtree(ws, ignore_errors=True)

    spawn_seq = [f"{s.role}" for s in orch.steps if s.op == "spawn"]
    return {
        "task": task["id"], "kind": task["kind"], "arm": "orchestrated", "rep": rep,
        "run_id": rec.run_id,
        "baseline_pass": base_pass, "objective_pass": obj_pass,
        "declined": orch.terminal_state == "abandoned",
        "decline_expected": bool(task["expect"].get("decline_correct")),
        "orch_terminal": orch.terminal_state,
        "steps": len(orch.steps), "spawn_sequence": spawn_seq,
        "model_calls": orch.model_calls,
        "impl_files": orch.files_written,
        "reviewer_verdict": next((s.processor_verdict for s in reversed(orch.steps)
                                  if s.processor_verdict), None),
        "wall_s": wall,
        "check_tail": check_tail,
    }


def summarise(rows: list[dict]) -> str:
    L = ["# M5 comparison results", "", f"_{time.strftime('%Y-%m-%d %H:%M')} - {len(rows)} runs_", ""]
    for arm in ALL_ARMS:
        ar = [r for r in rows if r["arm"] == arm]
        if not ar:
            continue
        npass = sum(r["objective_pass"] for r in ar)
        calls = sum(r.get("model_calls", 1) for r in ar)
        L.append(f"- **{arm}**: objective pass {npass}/{len(ar)}, "
                 f"mean wall {sum(r['wall_s'] for r in ar) / len(ar):.1f}s, {calls} model calls total")
    L += ["", "| task | kind | arm | rep | obj_pass | declined | steps/seq | calls | wall_s |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["task"], r["arm"], r["rep"])):
        seq = "/".join(r.get("spawn_sequence", [])) or (str(r.get("steps", "")) if "steps" in r else "-")
        L.append(f"| {r['task']} | {r['kind']} | {r['arm']} | {r['rep']} | {r['objective_pass']} | "
                 f"{r['declined']} | {seq} | {r.get('model_calls', 1)} | {r['wall_s']} |")
    L += ["", "## For the findings entry",
          "- M5: orchestrated vs monolith vs M4 fixed chain - pass rate, cost, and whether",
          "  the orchestrator's per-step choices (spawn_sequence + rationales in the decision",
          "  records) reconstruct into a legible strategy.",
          "- End-of-MVP: this closes M0-M5; trigger the findings 1-6 sequence rework."]
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--arms", nargs="+", default=list(ALL_ARMS))
    args = ap.parse_args()

    if not health():
        print("Ollama not reachable - aborting.")
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
                if arm == "orchestrated":
                    row = run_orchestrated_task(task, rep, check_command)
                    print(f"      obj_pass={row['objective_pass']} term={row['orch_terminal']} "
                          f"seq={'/'.join(row['spawn_sequence'])} calls={row['model_calls']} "
                          f"wall={row['wall_s']}s", flush=True)
                else:
                    row = run_fixed_arm(task, arm, rep, check_command)
                    print(f"      obj_pass={row['objective_pass']} declined={row['declined']} "
                          f"wall={row['wall_s']}s", flush=True)
                rows.append(row)

    (RESULTS / "results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    (RESULTS / "summary.md").write_text(summarise(rows), encoding="utf-8")
    print("\n" + summarise(rows))


if __name__ == "__main__":
    main()
