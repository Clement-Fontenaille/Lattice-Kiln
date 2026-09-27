"""A14 self-test: stage records join to store rows on cell id. No model needed.

    python stage_join_selftest.py

Copies the repo (minus .git and archive/) into a temp dir, empties the copy's
stage logs and store, and runs every M7 workflow through `run_suite.run_task`
against an unreachable model under two model tags and two sampling settings.
Each arm raises at its first call, which is exactly the path that must still be
attributable: the stage record is written in `finally`, and the row lands in
the copy's store with `run_ok: false`. Then `stage_join.py` runs on the copy.

Nothing in the real repo is written. The real evalkit_store is never opened.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARMS = ("judge_fullctx,judge_caveat,judge_bypass,judge_anchored,judge_staged,"
        "m7,m7b,m7c,m7e,m7f,test_synth,test_synth_retry")
TASKS = "wf2_retry,hf_extract_fn"

DRIVE = r'''
import sys, io, contextlib
root, arms, tasks, reps = sys.argv[1], sys.argv[2].split(","), sys.argv[3].split(","), int(sys.argv[4])
sys.path.insert(0, root + "/experiments/M6-evaluation-suite")
import run_suite as rs
T, cmd, prot, _ = rs.load_tasks()
T = {t["id"]: t for t in T}
for arm in arms:
    for tid in tasks:
        for rep in range(1, reps + 1):
            with contextlib.redirect_stdout(io.StringIO()):
                row = rs.run_task(T[tid], arm, rep, cmd, prot)
            rs._STORE.add(rs._cell_for(tid, arm), [row], provenance="recorded",
                          source="stage_join_selftest")
'''


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="a14_"))
    try:
        dst = tmp / "repo"
        shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "archive"))
        m7 = dst / "experiments" / "M7-static-workflow"
        for f in m7.glob("stage_influence*.jsonl"):
            f.write_text("", encoding="utf-8")
        shutil.rmtree(dst / "evalkit_store" / "rows", ignore_errors=True)
        (dst / "evalkit_store" / "index.jsonl").unlink(missing_ok=True)
        drive = tmp / "drive.py"
        drive.write_text(DRIVE, encoding="utf-8")
        base = {**os.environ, "LATTICE_TRANSCRIPT": "0",
                # unreachable on purpose: every arm must fail fast
                "LATTICE_BASE_URL": "http://127.0.0.1:9"}
        for env in ({"LATTICE_EVAL_MODEL": "selftest-a"},
                    {"LATTICE_EVAL_MODEL": "selftest-b"},
                    {"LATTICE_EVAL_MODEL": "selftest-a", "LATTICE_TEMPERATURE": "1.0"}):
            subprocess.run([sys.executable, str(drive), str(dst), ARMS, TASKS, "2"],
                           env={**base, **env}, check=True, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        return subprocess.run([sys.executable, str(m7 / "stage_join.py")]).returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
