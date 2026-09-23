"""Nudge sweep through the WHOLE pipeline, not one isolated judge call.

WHAT THE EARLIER PROBE COULD NOT SAY. probe_think_nudge fired a single
/api/chat with the judge prompt and counted thinking characters. Every rep in
every arm returned the same verdict, so nothing in it tested whether a shorter
reasoning trace costs judgement quality -- and its one apparent effect did not
replicate at n=5 anyway.

This runs `judge_anchored` end to end instead: the implementer writes files
through the tool loop, the check runs against the real fixture, and the judge
reads the actual diff. So the outcome is `objective_pass` and subtest counts,
which is the thing that actually matters, with thinking cost alongside rather
than instead.

THE NUDGE REACHES EVERY STAGE. It is applied at the transport
(ollama_client.NUDGE), because the M7 audit and judge stages call generate()
directly rather than going through the role library -- appending it in
prompt_for would have nudged the implementer only and quietly left the name
"whole pipeline" wrong.

IT IS KEYED. The nudge text feeds adapter_fingerprint(), so nudged rows carry a
different `params.adapter` and can never pool with unnudged ones. Without that
this sweep would be unreadable against every other row in the store, which is
the defect 50-findings/15 exists to prevent.

THREE ARMS, n=10, ONE TASK, run concurrently against the three Ollama slots.
Each arm is a separate process with its own LATTICE_NUDGE, so a crash in one
does not take the others with it.

    python sweep_nudge_pipeline.py [--reps 10] [--task wf2_retry] [--model M]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Two treatments and a control. Kept small deliberately: at n=10 through a full
# pipeline each additional arm is another ~30 minutes, and six arms at n=5 is
# what produced an unreplicable result last time.
ARMS = {
    "control": "",
    "first_pass": "Form a judgement on the first pass and write it.",
    "answer_first": ("Write your answer FIRST, then stop. Any reasoning you do "
                     "must fit in a few sentences before it."),
}


def run_arm(name: str, nudge: str, *, reps: int, task: str, model: str,
            arm: str) -> subprocess.Popen:
    env = dict(os.environ)
    env.update({
        "LATTICE_EVAL_MODEL": model,
        "LATTICE_PROTOCOL": "tools",
        "LATTICE_MIN_PREDICT": "8192",
        "LATTICE_NUM_CTX": "16384",
        "LATTICE_NUDGE": nudge,
    })
    log = HERE / f"sweep_nudge_{name}.log"
    fh = open(log, "w", encoding="utf-8")
    p = subprocess.Popen(
        [sys.executable, "-u", str(HERE / "run_suite.py"),
         "--arm", arm, "--tasks", task, "--reps", str(reps)],
        cwd=str(HERE), env=env, stdout=fh, stderr=subprocess.STDOUT)
    p._log = log          # type: ignore[attr-defined]
    p._name = name        # type: ignore[attr-defined]
    return p


def main(argv: list[str]) -> None:
    reps, task = 10, "wf2_retry"
    model = "nemotron3-nano-4b:latest"
    arm = "judge_anchored"
    for flag, setter in (("--reps", "reps"), ("--task", "task"),
                         ("--model", "model"), ("--suite-arm", "arm")):
        if flag in argv:
            i = argv.index(flag)
            val = argv[i + 1]
            if setter == "reps":
                reps = int(val)
            elif setter == "task":
                task = val
            elif setter == "model":
                model = val
            else:
                arm = val

    print(f"arm={arm} task={task} model={model} reps={reps} per nudge")
    print(f"{len(ARMS)} nudge arms x {reps} reps = {len(ARMS) * reps} full "
          f"pipeline runs, 3 concurrent")
    for n, t in ARMS.items():
        print(f"  {n:13} {t!r}")

    t0 = time.monotonic()
    procs = [run_arm(n, t, reps=reps, task=task, model=model, arm=arm)
             for n, t in ARMS.items()]
    for p in procs:
        rc = p.wait()
        print(f"  {p._name:13} exit {rc}  ({p._log.name})")
    print(f"total wall {(time.monotonic() - t0) / 60:.1f} min")
    print("\nrows land in evalkit_store/index.jsonl, keyed by params.adapter; "
          "read them with report_nudge_sweep.py")


if __name__ == "__main__":
    main(sys.argv[1:])
