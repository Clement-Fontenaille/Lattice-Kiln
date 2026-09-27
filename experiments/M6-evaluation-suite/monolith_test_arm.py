"""`monolith_test`: monolith, plus a `run_tests` tool the worker calls when it chooses.

THE VARIABLE IS WHO DECIDES WHEN TO PROBE THE GATE (Queue A11). `dloop` and
every arm above it score the workspace every round and feed the failing subtest
names back unasked (m6_arms.py, "Current state still fails"). This arm is
`monolith` -- same context, same role, same one-shot shape -- with one addition:
a tool the model may call, at its own discretion and its own cost in turns, to
learn whether the gate passes. Paired against `dloop` that is one variable:
model-driven probing against harness-driven probing. Paired against `monolith`
it is the first deliberate, counted, capped probe next to none.

WHAT THE TOOL RETURNS, AND WHAT IT WITHHOLDS. The gate only: whether the check
exits clean, and the SUBTESTS fraction. Not the check's output, not the failing
subtest names, and not the structural dimensions, which run_suite keeps out of
the gate on purpose and which `objective_pass` alone measures. A worker allowed
to iterate against the full grader would make `gate_pass` measure the grader
back to itself; `objective_pass` is the reading that survives, and both are on
the row.

WHAT IT RUNS AGAINST. write_file is not applied during the tool loop -- effects
are realized through the gate only after conclude. So `run_tests` scores a
scratch copy of the workspace with the files written SO FAR in this exchange
overlaid, and the protected check files restored from the fixture, exactly as
run_suite restores them before its own scoring. A worker that edits the test
file cannot change what run_tests reports.

CAPPED at RUN_TESTS_CAP calls per task, across recovery attempts. Calls beyond
the cap are refused, counted, and cost a turn like any other. The count goes on
the row as `arm_extra.run_tests`, beside the score.

A NEW FILE ON PURPOSE. setup_key.arm_source_path() hashes the whole arm file,
so defining this arm in run_suite.py would move arm_sha for baseline, monolith
and monolith_recovery and detach them from every collected row.

Tools protocol only: under markers there is no tool channel to offer it on.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import row_extra
from _m6bridge import Gate, RunRecorder, assemble, run_processor
import processor as _proc

HERE = Path(__file__).resolve().parent
SUITE = HERE / "suite"
ARM = "monolith_test"
RUN_TESTS_CAP = 3
_SUBTESTS = re.compile(r"^SUBTESTS\s+(\d+)\s*/\s*(\d+)", re.M)

RUN_TESTS = {"type": "function", "function": {
    "name": "run_tests",
    "description": (
        "Run the task's test suite against the files as they stand now, "
        "including every file you have written with write_file so far. "
        "Returns only whether the suite passes and how many subtests pass. "
        f"You may call it at most {RUN_TESTS_CAP} times; later calls are "
        "refused. It takes no arguments."),
    "parameters": {"type": "object", "properties": {}, "required": []}}}


def _fmt(passes: bool, exit_status: int, sub: tuple[int, int] | None,
         left: int) -> str:
    return json.dumps({"status": "ran", "suite_passes": passes,
                       "exit_status": exit_status,
                       "subtests_passed": sub[0] if sub else None,
                       "subtests_total": sub[1] if sub else None,
                       "calls_left": left})


def _fmt_refused() -> str:
    return json.dumps({"status": "refused",
                       "detail": f"run_tests limit of {RUN_TESTS_CAP} reached",
                       "calls_left": 0})


# Model-facing, so it is in this arm's adapter fingerprint -- and only this
# arm's. Every other arm's fingerprint is computed without it.
_proc.ARM_TOOLS[ARM] = {
    "tools": [RUN_TESTS],
    "result_samples": [_fmt(True, 0, (5, 5), 2), _fmt(False, 1, (3, 5), 0),
                       _fmt(False, 1, None, 1), _fmt_refused()],
}


def _task(task_id: str) -> tuple[dict, str, list[str]]:
    d = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))
    for t in d["tasks"]:
        if t["id"] == task_id:
            return t, d["check_command"], d["protected_files"]
    raise KeyError(f"unknown task {task_id!r}")


def gate_on(ws: Path, files: dict[str, str], task: dict, cmd: str,
            protected: list[str]) -> dict:
    """Score a scratch copy: workspace + pending writes, protected restored."""
    tmp = Path(tempfile.mkdtemp(prefix="m6_runtests_"))
    try:
        shutil.copytree(ws, tmp, dirs_exist_ok=True)
        for rel, body in files.items():
            dst = (tmp / rel).resolve()
            if tmp.resolve() not in dst.parents:
                continue                         # outside the workspace: ignored
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(body, encoding="utf-8")
        src = SUITE / Path(task["dir"]).name
        for name in protected:
            if (src / name).is_file():
                shutil.copy2(src / name, tmp / name)
        try:
            cp = subprocess.run(cmd.split(), cwd=str(tmp), capture_output=True,
                                text=True, timeout=30)
            out, code = cp.stdout + cp.stderr, cp.returncode
        except subprocess.TimeoutExpired:
            out, code = "", -1
        m = _SUBTESTS.search(out)
        sub = (int(m.group(1)), int(m.group(2))) if m else None
        # Same gate run_suite applies: clean exit AND the check did not crash.
        return {"passes": code == 0 and sub is not None,
                "exit_status": code, "sub": sub}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def arm_monolith_test(objective, ws):
    if _proc.PROTOCOL != "tools":
        raise RuntimeError("monolith_test needs LATTICE_PROTOCOL=tools: "
                           "run_tests is offered as a tool")
    ws = Path(ws)
    task, cmd, protected = _task(os.environ["M6_TASK"])
    state = {"invocations": 0, "refused": 0, "results": []}

    def run_tests(call, files):
        if state["invocations"] >= RUN_TESTS_CAP:
            state["refused"] += 1
            return _fmt_refused()
        state["invocations"] += 1
        g = gate_on(ws, files, task, cmd, protected)
        state["results"].append({"passes": g["passes"],
                                 "exit_status": g["exit_status"],
                                 "sub": list(g["sub"]) if g["sub"] else None,
                                 "files_pending": len(files)})
        return _fmt(g["passes"], g["exit_status"], g["sub"],
                    RUN_TESTS_CAP - state["invocations"])

    # From here to rec.close() this is arm_monolith, with the tool added.
    rec = RunRecorder(HERE / "runs", intent_text=objective,
                      meta={"arm": ARM, "suite": "m6"})
    root = rec.invocation(role="m6-monolith-test", model_identity={"name": "harness"},
                          intent_ref="m6", config_ref="m6")
    b = assemble(objective, ws, token_budget=8000)
    try:
        run_processor(role="implementer", objective=objective, context=b,
                      workspace_root=ws, recorder=rec, gate=Gate(),
                      parent_invocation_id=root, intent_ref="m6",
                      interaction_mode="oneshot",
                      extra_tools=[RUN_TESTS],
                      tool_handlers={"run_tests": run_tests},
                      # Each probe costs a turn. Without the extra turns a
                      # worker that probes would lose the turns it needs to
                      # write and conclude, and the arm would measure that.
                      max_tool_turns=_proc.MAX_TOOL_TURNS + RUN_TESTS_CAP)
    finally:
        # On the row even when the arm raised: a probe count that vanishes
        # with the run is the lossy summary A4 exists to stop.
        row_extra.EXTRA["run_tests"] = {"invocations": state["invocations"],
                                        "refused": state["refused"],
                                        "cap": RUN_TESTS_CAP,
                                        "results": state["results"]}
    rec.close("completed")
    return "done"


ARMS_EXTRA = {ARM: arm_monolith_test}
