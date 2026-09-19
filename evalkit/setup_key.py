"""What produced a row, recorded well enough to decide reuse from data.

A result is only reusable by another experiment if it came from the same setup.
Until 2026-09-19 that question was answered by hand every time -- reading
directory names, diffing arm files against their git history, and remembering
which sweep used which model. The seeder for E8 green-lit stale rows because
the directory name said nothing about the fixture version, which is the failure
this module removes.

A **Cell** is everything that can change an outcome except the draw itself.
Reps are draws from a cell, so `rep` is not part of cell identity.

    fixture_sha     this task's fixture files, hashed (NOT the suite version:
                    a suite bump that touched two tasks must not invalidate
                    the other thirty-two)
    task            which task
    arm             which pipeline
    arm_sha         sha256 of the arm's source file
    prompt_sha      sha256 of the effective prompts that arm will send
    backend         ollama | llamacpp
    model           the model tag
    params          think, min_predict, num_ctx, temperature
    judge_format    decision_first | reason_first

`model_digest` is recorded but is NOT part of identity, for a reason worth
stating: legacy rows have no digest, so requiring one would block every reuse of
everything recorded before today. The rule instead is **known-different blocks,
unknown abstains** -- two cells whose digests are both known and differ never
match; a cell whose digest is unknown carries no opinion, and `provenance` says
so, so an experiment that wants the stricter rule can demand it.

`arm_sha` IS part of identity, and deliberately strict. Today's format hook
changed all three judge arms without changing their `decision_first` behaviour,
and I established that by diffing. Under this module that reuse is refused by
default and requires an explicit waiver naming both hashes and the reason --
which makes the judgement a recorded artifact instead of a claim in a commit
message.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.request
from dataclasses import dataclass, asdict, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M6 = ROOT / "experiments" / "M6-evaluation-suite"
M7 = ROOT / "experiments" / "M7-static-workflow"

# Arms whose implementation lives in M7 as <arm>_workflow.py. The rest are
# defined inside M6 (baseline, monolith in run_suite; dloop, staged in m6_arms).
_M7_ARMS = {"m7", "m7b", "m7c", "m7e", "m7f", "judge_staged", "judge_anchored",
            "judge_caveat", "judge_bypass", "test_synth", "test_synth_retry",
            "judge_fullctx"}
_M6_ARM_FILES = {"baseline": "run_suite.py", "monolith": "run_suite.py",
                 "dloop": "m6_arms.py", "staged": "m6_arms.py"}


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def arm_source_path(arm: str) -> Path:
    if arm in _M7_ARMS:
        return M7 / f"{arm}_workflow.py"
    if arm in _M6_ARM_FILES:
        return M6 / _M6_ARM_FILES[arm]
    raise KeyError(f"unknown arm {arm!r}")


def arm_sha(arm: str) -> str:
    """Hash of the arm's source. Strict on purpose: a logic change that leaves
    the prompts alone -- the rotated-argument bug of 2026-09-17 was exactly
    that -- must not be mistaken for the same setup."""
    return _sha(arm_source_path(arm).read_text(encoding="utf-8"))


def prompt_sha(arm: str, judge_format: str) -> str:
    """Hash of the prompts this arm will actually send, after the judge-format
    transformation. Separate from arm_sha so a change that moves one and not the
    other is visible as such."""
    src = arm_source_path(arm).read_text(encoding="utf-8")
    parts = []
    for name in ("AUDIT", "JUDGE"):
        m = re.search(rf'^{name}\s*=\s*"""(.*?)"""', src, re.S | re.M)
        if m:
            parts.append(f"{name}:{m.group(1)}")
    if not parts:
        return "none"
    text = "\n".join(parts)
    if judge_format == "reason_first":
        import sys
        sys.path.insert(0, str(M7))
        os.environ["LATTICE_JUDGE_FORMAT"] = "reason_first"
        import judge_format as _jf
        import importlib
        importlib.reload(_jf)
        text = _jf.apply(text)
    return _sha(text)


def suite_version() -> str:
    return json.loads((M6 / "tasks.json").read_text(encoding="utf-8"))["suite_version"]


def task_dir(task: str) -> Path:
    d = json.loads((M6 / "tasks.json").read_text(encoding="utf-8"))
    for t in d["tasks"]:
        if t["id"] == task:
            return M6 / t["dir"]
    raise KeyError(f"unknown task {task!r}")


def fixture_sha(task: str) -> str:
    """Hash of one task's fixture: every file in its directory, including the
    check, since a change to either moves the outcome.

    Per task and not per suite, because the suite version is too coarse to key
    on. The 0.4.1 bump changed two fixtures out of thirty-four; keying on the
    suite version refused the other thirty-two for no reason, which the E8 plan
    made visible the first time it ran.
    """
    d = task_dir(task)
    # Sort on the relative POSIX string, NOT on the Path. Path comparison is
    # case-insensitive on Windows, so sorted() put orders.py before README.md
    # here while the git-side hasher sorted the raw names and put README.md
    # first -- identical content, different hash, on one platform only.
    files = [p for p in d.rglob("*")
             if p.is_file() and "__pycache__" not in p.parts]
    parts = []
    for rel, p in sorted((p.relative_to(d).as_posix(), p) for p in files):
        parts.append(rel)
        parts.append(p.read_text(encoding="utf-8", errors="replace"))
    return _sha("\n".join(parts))


def model_digest(model: str, base_url: str = "http://localhost:11434") -> str | None:
    """Exact weights, when the backend will tell us. None is a legitimate answer
    and must not be turned into a blocking mismatch."""
    try:
        req = urllib.request.Request(
            f"{base_url}/api/show",
            data=json.dumps({"model": model}).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read().decode("utf-8"))
        for k in ("digest", "model_info"):
            if isinstance(d.get(k), str):
                return d[k][:16]
        return _sha(json.dumps(d.get("details", {}), sort_keys=True))
    except Exception:  # noqa: BLE001
        return None


@dataclass(frozen=True)
class Cell:
    fixture_sha: str     # this task's fixture, not the suite version: see fixture_sha()
    task: str
    arm: str
    arm_sha: str
    prompt_sha: str
    backend: str
    model: str
    judge_format: str
    params: str          # canonical JSON of the param dict, so the cell hashes

    @staticmethod
    def make(*, task: str, arm: str, backend: str, model: str,
             judge_format: str = "decision_first", params: dict | None = None,
             fixture_hash: str | None = None, arm_hash: str | None = None,
             prompt_hash: str | None = None) -> "Cell":
        p = dict(params or {})
        return Cell(
            fixture_sha=fixture_hash or fixture_sha(task),
            task=task, arm=arm,
            arm_sha=arm_hash or arm_sha(arm),
            prompt_sha=prompt_hash or prompt_sha(arm, judge_format),
            backend=backend, model=model, judge_format=judge_format,
            params=json.dumps(p, sort_keys=True),
        )

    @property
    def id(self) -> str:
        return _sha(json.dumps(asdict(self), sort_keys=True))

    def as_dict(self) -> dict:
        return asdict(self)


def compatible(a: Cell, b: Cell, waivers: list[dict] | None = None) -> tuple[bool, str]:
    """Do these two cells describe the same setup?

    Exact on every field, with one escape: a waiver may declare two arm_sha or
    prompt_sha values equivalent. A waiver is a recorded artifact with a reason
    and a date, not a flag.
    """
    da, db = a.as_dict(), b.as_dict()
    for k in da:
        if da[k] == db[k]:
            continue
        if k in ("arm_sha", "prompt_sha") and _waived(k, da[k], db[k], waivers):
            continue
        return False, f"{k}: {da[k]!r} != {db[k]!r}"
    return True, "identical"


def _waived(field_name, x, y, waivers) -> bool:
    for w in (waivers or []):
        if w.get("field") != field_name:
            continue
        if {x, y} == set(w.get("equivalent", [])):
            return True
    return False
