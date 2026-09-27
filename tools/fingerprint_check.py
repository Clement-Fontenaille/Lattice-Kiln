"""Attest, by computation, that a change moved no model-facing key.

    python tools/fingerprint_check.py --baseline <ref>
    python tools/fingerprint_check.py --baseline origin/main --head WORKTREE
    python tools/fingerprint_check.py --baseline <ref> --env LATTICE_NUDGE=x

Prints, at a baseline ref and at HEAD (or the uncommitted working tree), under
both output protocols:

    processor.adapter_fingerprint()     the text the model sees
    processor.recovery_fingerprint()    the recovery policy
    run_suite._eval_params(arm)         per registered arm: sampling, protocol,
                                        adapter, recovery -- what the key holds

and exits 1 if any value present on both sides differs. An arm present on one
side only is listed and does not fail the check: adding an arm moves no other
arm's key, and that is what this is for.

WHY THIS AND NOT A WAIVER. adapter_fingerprint hashes the TEXT THE MODEL SEES,
not the file producing it, so a refactor that leaves model-facing text alone
does not move it -- no declaration needed. A waiver lets an author assert
"non-breaking" where the hash is the arbiter. This prints the hash instead. If a
value moves when the author believes it should not, that is a finding about the
fingerprint or the change, never a case for an exemption.

Each side runs in its own process from its own checkout (a temporary git
worktree), with every LATTICE_* variable removed from the environment unless
given with --env, so the values are the defaults both sides would record.
`arm_sha` is deliberately not compared: it hashes source files and moves on any
edit, which is its job and not this script's.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOLS = ("tools", "markers")

DUMP = r'''
import contextlib, io, json, os, sys
root = sys.argv[1]
sys.path.insert(0, os.path.join(root, "experiments", "M6-evaluation-suite"))
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    import run_suite as rs
    import processor as proc
out = {"adapter": proc.adapter_fingerprint(),
       "recovery": (proc.recovery_fingerprint()
                    if hasattr(proc, "recovery_fingerprint") else "n/a"),
       "eval_params": {}}
for arm in sorted(rs.ARMS):
    try:
        out["eval_params"][arm] = (rs._eval_params(arm)
                                   if hasattr(rs, "_eval_params") else "n/a")
    except TypeError:                     # older signature, no arm argument
        out["eval_params"][arm] = rs._eval_params()
print(json.dumps(out, sort_keys=True))
'''


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()


def _dump(tree: Path, extra_env: dict) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("LATTICE_")}
    env.update({"LATTICE_TRANSCRIPT": "0", **extra_env})
    res = {}
    for proto in PROTOCOLS:
        cp = subprocess.run([sys.executable, "-c", DUMP, str(tree)],
                            env={**env, "LATTICE_PROTOCOL": proto},
                            capture_output=True, text=True, cwd=tree)
        if cp.returncode:
            raise SystemExit(f"could not compute fingerprints in {tree} "
                             f"({proto}):\n{cp.stderr[-2000:]}")
        res[proto] = json.loads(cp.stdout.strip().splitlines()[-1])
    return res


def _checkout(ref: str, tmp: Path) -> Path:
    if ref == "WORKTREE":
        return ROOT
    dst = tmp / ref.replace("/", "_")
    _git("worktree", "add", "--detach", "-q", str(dst), ref)
    return dst


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--baseline", required=True, help="git ref to compare against")
    ap.add_argument("--head", default="HEAD",
                    help="git ref, or WORKTREE for the uncommitted checkout")
    ap.add_argument("--env", action="append", default=[], metavar="K=V",
                    help="LATTICE_* setting applied to both sides")
    a = ap.parse_args(argv)
    extra = dict(kv.split("=", 1) for kv in a.env)

    tmp = Path(tempfile.mkdtemp(prefix="fpcheck_"))
    trees = []
    try:
        base_tree = _checkout(a.baseline, tmp)
        head_tree = _checkout(a.head, tmp)
        trees = [t for t in (base_tree, head_tree) if t != ROOT]
        base, head = _dump(base_tree, extra), _dump(head_tree, extra)
    finally:
        for t in trees:
            subprocess.run(["git", "worktree", "remove", "--force", str(t)],
                           cwd=ROOT, capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)

    base_id = _git("rev-parse", "--short", a.baseline)
    head_id = "worktree" if a.head == "WORKTREE" else _git("rev-parse", "--short", a.head)
    print(f"baseline {a.baseline} ({base_id})  vs  head {a.head} ({head_id})"
          + (f"  env {extra}" if extra else ""))
    moved = 0
    for proto in PROTOCOLS:
        b, h = base[proto], head[proto]
        print(f"\n[{proto}]")
        for k in ("adapter", "recovery"):
            same = b[k] == h[k]
            moved += not same
            print(f"  {k:10} {b[k]:>14}  {h[k]:>14}  {'same' if same else 'MOVED'}")
        arms = sorted(set(b["eval_params"]) | set(h["eval_params"]))
        for arm in arms:
            x, y = b["eval_params"].get(arm), h["eval_params"].get(arm)
            if x is None or y is None:
                print(f"  {arm:24} {'only at head' if x is None else 'only at baseline'}"
                      f"  {json.dumps(y if x is None else x, sort_keys=True)}")
                continue
            same = x == y
            moved += not same
            print(f"  {arm:24} {'same' if same else 'MOVED'}  "
                  f"{json.dumps(y, sort_keys=True)}"
                  + ("" if same else f"  (was {json.dumps(x, sort_keys=True)})"))
    print(f"\n{'PASS' if not moved else 'FAIL'}: {moved} value(s) moved "
          "among those present on both sides.")
    return 1 if moved else 0


if __name__ == "__main__":
    sys.exit(main())
