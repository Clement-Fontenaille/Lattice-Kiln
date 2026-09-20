"""Bring the legacy results trees into the store, declaring what is not recorded.

The trees hold arm x task x rep rows and nothing about what produced them: no
model, no reasoning setting, no fixture version (until this afternoon), no arm
version. All of that lived in the directory name and in whoever remembered the
sweep.

So migration cannot read the setup off the rows. It **declares** it, from a
manifest, and marks every migrated entry `provenance: declared` so a later
reader can tell a stated setup from a recorded one.

Two fields are recovered rather than asserted:

  * `suite_version` comes from the row when the row has it, and from the
    manifest's `suite_before` otherwise. The 0.4.1 repair touched two fixtures,
    and rows re-run after it carry the field, so this splits a tree correctly
    down the middle instead of labelling it uniformly.

  * `arm_sha` and `prompt_sha` are computed from a **named git revision**, not
    from the working tree. The judge arms were edited today; hashing them as
    they are now would claim rows came from code that did not exist when they
    ran. The manifest names the revision that was current for that tree.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from setup_key import (Cell, ROOT, _sha, arm_source_path,  # noqa: E402
                       fixture_sha, suite_version, task_dir)
from store import Store  # noqa: E402

MANIFEST = HERE / "migration_manifest.json"


def _git_text(args: list[str]) -> str:
    """git output decoded as UTF-8, explicitly.

    NOT subprocess(text=True): that decodes with the locale encoding, cp1252 on
    this host, which mojibakes any fixture containing a multi-byte character and
    hashes it differently from the same bytes read off disk. One README with an
    em-dash was enough to make every fixture hash disagree.
    """
    out = subprocess.run(args, cwd=ROOT, capture_output=True)
    if out.returncode != 0:
        raise RuntimeError(f"{' '.join(args[:3])} failed: "
                           f"{out.stderr.decode('utf-8', 'replace').strip()[:200]}")
    return out.stdout.decode("utf-8", errors="replace")


def _file_at(rev: str, path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return _git_text(["git", "show", f"{rev}:{rel}"])


def arm_sha_at(rev: str, arm: str) -> str:
    return _sha(_file_at(rev, arm_source_path(arm)))


_FIX_CACHE: dict[tuple[str, str], str] = {}


def fixture_sha_at(rev: str, task: str) -> str:
    """One task's fixture as it stood at a revision.

    Must be read from git, not from the working tree: the 0.4.1 repair edited
    two fixtures, so hashing today's files would claim rows came from fixtures
    that did not exist when they ran -- the precise error this store exists to
    prevent.
    """
    key = (rev, task)
    if key in _FIX_CACHE:
        return _FIX_CACHE[key]
    d = task_dir(task).relative_to(ROOT).as_posix()
    ls_out = _git_text(["git", "ls-tree", "-r", "--name-only", rev, "--", d])
    parts = []
    # Sorted on the same key as the working-tree hasher: the relative POSIX
    # name. Sorting full paths here and Path objects there put README.md and
    # orders.py in opposite orders on Windows and hashed identical fixtures
    # differently.
    names = sorted(x[len(d) + 1:] for x in ls_out.splitlines()
                   if x.strip() and "__pycache__" not in x)
    for name in names:
        parts.append(name)
        parts.append(_git_text(["git", "show", f"{rev}:{d}/{name}"]))
    out = _sha("\n".join(parts))
    _FIX_CACHE[key] = out
    return out


def prompt_sha_at(rev: str, arm: str) -> str:
    src = _file_at(rev, arm_source_path(arm))
    parts = []
    for name in ("AUDIT", "JUDGE"):
        m = re.search(rf'^{name}\s*=\s*"""(.*?)"""', src, re.S | re.M)
        if m:
            parts.append(f"{name}:{m.group(1)}")
    return _sha("\n".join(parts)) if parts else "none"


def migrate(entry: dict, store: Store, dry: bool) -> tuple[int, int, list[str]]:
    tree = ROOT / entry["tree"]
    rev = entry["arm_rev"]
    notes = []
    cells = added = 0
    for p in sorted(tree.glob("*.json")):
        rows = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(rows, list) or not rows or "task" not in rows[0]:
            continue                       # probe output, not an arm file
        arm = p.stem
        if arm in entry.get("exclude", []):
            notes.append(f"{arm}: excluded by manifest (not independent draws)")
            continue
        try:
            a_sha, p_sha = arm_sha_at(rev, arm), prompt_sha_at(rev, arm)
        except (KeyError, RuntimeError) as e:
            # Not an accident to shrug at: an arm file we cannot hash is an arm
            # whose provenance cannot be stated, so its rows stay out.
            notes.append(f"{arm}: NOT MIGRATED - {e}")
            continue
        # Split by the row's own suite_version where it has one.
        by_suite: dict[str, list] = {}
        for r in rows:
            if not r.get("run_ok", True):
                continue               # a run that raised produced no attempt
            sv = r.get("suite_version") or entry["suite_before"]
            by_suite.setdefault(sv, []).append(r)
        for sv, group in sorted(by_suite.items()):
            # Rows carrying the current suite version came from today's
            # fixtures; the rest came from the manifest's fixture_rev. Split
            # per row rather than per tree, because a partially re-run tree
            # legitimately holds both.
            frev = None if sv == suite_version() else entry["fixture_rev"]
            for task in sorted({r["task"] for r in group}):
                f_sha = fixture_sha(task) if frev is None else fixture_sha_at(frev, task)
                cell = Cell.make(
                    task=task, arm=arm, backend=entry["backend"],
                    model=entry["model"], judge_format=entry["judge_format"],
                    params=entry.get("arm_params", {}).get(arm, entry["params"]),
                    fixture_hash=f_sha,
                    arm_hash=a_sha, prompt_hash=p_sha)
                trows = [r for r in group if r["task"] == task]
                cells += 1
                if not dry:
                    added += store.add(cell, trows, provenance="declared",
                                       source=entry["tree"])
                else:
                    added += len(trows)
    return cells, added, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--store", default=None)
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    store = Store(Path(args.store) if args.store else None)
    print(f"suite in working tree: {suite_version()}\n")
    tot_c = tot_a = 0
    for entry in manifest["trees"]:
        c, a, notes = migrate(entry, store, args.dry_run)
        tot_c += c
        tot_a += a
        print(f"{entry['tree']:56s} cells {c:5d}  rows {a:6d}")
        for n in notes:
            print(f"    {n}")
    print(f"\n{'TOTAL':56s} cells {tot_c:5d}  rows {tot_a:6d}")
    if args.dry_run:
        print("\n--dry-run: nothing written")


if __name__ == "__main__":
    main()
