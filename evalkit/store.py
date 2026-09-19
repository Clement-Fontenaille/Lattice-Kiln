"""One results store, keyed by setup rather than by directory name.

Layout, chosen to survive being archived, carried to a disconnected machine and
merged back:

    evalkit_store/
      index.jsonl            one line per (cell, rep): the cell fields, the rep,
                             and where the row lives
      rows/<cell_id>.jsonl   the rows themselves, one JSON object per line

Append-only in normal use. Two stores merge by concatenating both files and
de-duplicating on (cell_id, rep, row_sha) -- which is what an air-gapped run
needs, and why the index carries the cell fields inline rather than pointing at
a separate table.

`provenance` is on every entry and takes two values:

    recorded   the harness wrote the setup at run time
    declared   the setup was supplied afterwards from a migration manifest,
               because the row predates the harness recording it

Nothing here treats those as equal. `query()` reports them separately and an
experiment may demand `recorded` only.
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path

from setup_key import Cell

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STORE = ROOT / "evalkit_store"


def _row_sha(row: dict) -> str:
    return hashlib.sha256(
        json.dumps(row, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]


class Store:
    def __init__(self, path: Path | None = None):
        self.path = Path(path or DEFAULT_STORE)
        self.index_path = self.path / "index.jsonl"
        self.rows_dir = self.path / "rows"

    # ---------------------------------------------------------------- writing

    def add(self, cell: Cell, rows: list[dict], provenance: str,
            source: str = "") -> int:
        """Add rows for one cell. Returns how many were new.

        De-duplicates on (cell_id, rep, row_sha), so re-ingesting a tree is a
        no-op rather than a silent doubling of a sample size.
        """
        if provenance not in ("recorded", "declared"):
            raise ValueError(f"provenance must be recorded|declared, got {provenance!r}")
        self.rows_dir.mkdir(parents=True, exist_ok=True)
        seen = {(e["rep"], e["row_sha"]) for e in self._index_entries()
                if e["cell_id"] == cell.id}
        added = 0
        with (self.rows_dir / f"{cell.id}.jsonl").open("a", encoding="utf-8") as rf, \
             self.index_path.open("a", encoding="utf-8") as xf:
            for r in rows:
                rep = int(r.get("rep", 1))
                sha = _row_sha(r)
                if (rep, sha) in seen:
                    continue
                seen.add((rep, sha))
                rf.write(json.dumps(r, default=str) + "\n")
                xf.write(json.dumps({
                    "cell_id": cell.id, "rep": rep, "row_sha": sha,
                    "provenance": provenance, "source": source,
                    **cell.as_dict(),
                }) + "\n")
                added += 1
        return added

    # ---------------------------------------------------------------- reading

    def _index_entries(self):
        if not self.index_path.is_file():
            return []
        out = []
        for line in self.index_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
        return out

    def summary(self):
        """(cell_id -> {cell fields, reps, provenance counts})."""
        agg = {}
        for e in self._index_entries():
            a = agg.setdefault(e["cell_id"], {
                "cell": {k: e[k] for k in Cell.__dataclass_fields__},
                "reps": set(), "provenance": defaultdict(int)})
            a["reps"].add(e["rep"])
            a["provenance"][e["provenance"]] += 1
        for a in agg.values():
            a["n_reps"] = len(a["reps"])
            a["reps"] = sorted(a["reps"])
            a["provenance"] = dict(a["provenance"])
        return agg

    def have(self, cell: Cell, require_recorded: bool = False,
             waivers: list[dict] | None = None) -> int:
        """How many reps this store holds for this cell.

        Exact on cell id when there are no waivers, which is the fast and strict
        path. With waivers it compares field by field through `compatible()`, so
        a recorded equivalence -- "this arm_sha is the same behaviour as that
        one, here is why" -- can admit rows the hash alone would refuse. The
        waiver is the artifact; this function does not decide anything.
        """
        if not waivers:
            reps = {e["rep"] for e in self._index_entries()
                    if e["cell_id"] == cell.id
                    and not (require_recorded and e["provenance"] != "recorded")}
            return len(reps)

        from setup_key import compatible
        reps = set()
        for e in self._index_entries():
            if require_recorded and e["provenance"] != "recorded":
                continue
            other = Cell(**{k: e[k] for k in Cell.__dataclass_fields__})
            ok, _ = compatible(cell, other, waivers)
            if ok:
                reps.add(e["rep"])
        return len(reps)

    def rows(self, cell: Cell) -> list[dict]:
        p = self.rows_dir / f"{cell.id}.jsonl"
        if not p.is_file():
            return []
        return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()
                if l.strip()]
