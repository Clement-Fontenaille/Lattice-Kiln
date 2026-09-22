"""The pool: what is intended to be worked on, independent of who asked and who works.

A declaration is a *request*. A worker is a *pair of hands*. Neither is the
authority on what should run -- the pool is, and it is the only thing both of
them touch.

That inversion is what makes concurrency safe by construction rather than
detected afterwards. Before it, two `run_plan` invocations each computed a
deficit from the store, each ran it, and both wrote "rep 4"; the collision was
caught after the fact by renumbering. Under a pool the rep number is claimed at
*enqueue* time, so a second request finds it taken.

    pending/<cell>.<rep>.json      intended, unclaimed
    claimed/<cell>.<rep>.json      being worked on, worker named inside
    done/<cell>.<rep>.json         finished

**One** filesystem primitive carries the whole thing -- exclusive create:

    os.open(p, O_CREAT | O_EXCL)   two racers, exactly one wins, the other
                                   gets FileExistsError

Claim was built on `os.rename` first, on the usual reasoning that a rename is
atomic so the loser sees FileNotFoundError. Measured under eight threads on this
host, it is not: **twelve renames succeeded from seven distinct sources**, the
same file moving twice, leaving twenty claimed files from twelve intents. Both
operations now use exclusive create, and the same stress test shows no
double-claim. Do not reintroduce rename here.

No lock, no daemon, no database. A pool survives being archived and carried to a
disconnected machine because it is just directories.
"""
from __future__ import annotations

import json
import os
import socket
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POOL = ROOT / "evalkit_pool"
LEASE_S = 3 * 3600          # a task running longer than this is presumed dead


@dataclass
class Item:
    path: Path
    cell: dict
    rep: int
    env: dict
    requested_by: str
    meta: dict

    @property
    def stem(self) -> str:
        """`<cell_id>.<rep>` -- identity, unchanged as the item moves between
        pending, claimed and done. The worker is recorded inside the file and
        never in its name, so the name stays the identity."""
        n = self.path.name
        return n[:-5] if n.endswith(".json") else n


def _who() -> str:
    return f"{socket.gethostname()}-{os.getpid()}"


class Pool:
    def __init__(self, path: Path | None = None):
        self.path = Path(path or DEFAULT_POOL)
        self.pending = self.path / "pending"
        self.claimed = self.path / "claimed"
        self.done = self.path / "done"
        for d in (self.pending, self.claimed, self.done):
            d.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------- requesting

    def enqueue(self, cell, target: int, *, env: dict, requested_by: str,
                held: int = 0, meta: dict | None = None) -> list[int]:
        """Ensure `cell` reaches `target` reps in total. Returns reps created.

        TARGET, not delta, and that is what makes it idempotent. An earlier
        version took "how many more", so eight requesters each asking for five
        produced forty: every one computed its own deficit before any had
        written. Asking for a total instead means each requester tries rep
        numbers 1..target and exclusive-create settles who gets which, so the
        pool converges on `target` however many people ask for it.

        `held` is what the store already has; those rep numbers count as taken.
        """
        created = []
        for rep in range(1, target + 1):
            if rep <= held:
                continue
            name = f"{cell.id}.{rep}.json"
            if (self.claimed / name).exists() or (self.done / name).exists():
                continue
            try:
                fd = os.open(self.pending / name,
                             os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                continue          # already intended, by us or by someone else
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump({"cell": cell.as_dict(), "cell_id": cell.id,
                           "rep": rep, "env": env,
                           "requested_by": requested_by,
                           "requested_at": time.time(),
                           "meta": meta or {}}, fh, indent=2)
            created.append(rep)
        return created

    # ---------------------------------------------------------------- working

    def claim(self, who: str | None = None, match=None) -> Item | None:
        """Take one pending item, exclusively. None when there is nothing to do."""
        who = who or _who()
        for p in sorted(self.pending.glob("*.json")):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue                       # being written right now
            if match and not match(d):
                continue
            try:
                # THE claim. Exclusive create, so exactly one worker wins this
                # item however many are looking. Not a rename -- see the module
                # docstring for what that cost.
                fd = os.open(self.claimed / p.name,
                             os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                continue                       # already someone else's
            d["claimed_by"], d["claimed_at"] = who, time.time()
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(d, fh, indent=2)
            # The intent is now a claim. Removing the pending file is tidying,
            # NOT part of the claim -- the exclusive create above already
            # settled who owns this item. On Windows the unlink raises
            # PermissionError if a losing thread still has the file open for
            # reading, which under twelve racing claimers happens; letting that
            # propagate would abort a claim that had already succeeded. A stale
            # pending file is harmless: enqueue skips names present in claimed
            # or done, and the next claimer finds the item already taken.
            for _ in range(3):
                try:
                    p.unlink(missing_ok=True)
                    break
                except OSError:
                    time.sleep(0.01)
            return Item(self.claimed / p.name, d["cell"], d["rep"],
                        d.get("env", {}), d.get("requested_by", ""),
                        d.get("meta", {}))
        return None

    def complete(self, item: Item, outcome: str = "ok", note: str = "") -> None:
        d = json.loads(item.path.read_text(encoding="utf-8"))
        d["outcome"], d["note"], d["finished_at"] = outcome, note, time.time()
        (self.done / f"{item.stem}.json").write_text(
            json.dumps(d, indent=2), encoding="utf-8")
        item.path.unlink(missing_ok=True)

    def release(self, item: Item, note: str = "") -> None:
        """Hand an item back unfinished -- a dead backend, an interrupt. The rep
        number stays reserved, so nothing else claims it while it waits."""
        d = json.loads(item.path.read_text(encoding="utf-8"))
        d.pop("claimed_by", None)
        d.pop("claimed_at", None)
        d["released_note"] = note
        (self.pending / f"{item.stem}.json").write_text(
            json.dumps(d, indent=2), encoding="utf-8")
        item.path.unlink(missing_ok=True)

    def reap(self, lease_s: int = LEASE_S) -> list[str]:
        """Return items whose worker went away. A crashed worker must not hold a
        rep number forever, and a lease is the only thing that distinguishes
        slow from dead without asking the worker."""
        out, now = [], time.time()
        for p in sorted(self.claimed.glob("*.json")):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            if now - d.get("claimed_at", now) > lease_s:
                stem = p.name[:-5]
                d.pop("claimed_by", None)
                d["reaped_from"] = d.pop("claimed_at", None)
                (self.pending / f"{stem}.json").write_text(
                    json.dumps(d, indent=2), encoding="utf-8")
                p.unlink(missing_ok=True)
                out.append(stem)
        return out

    # ---------------------------------------------------------------- looking

    def counts(self) -> dict:
        return {d.name: len(list(d.glob("*.json")))
                for d in (self.pending, self.claimed, self.done)}
