"""Read the raw generations a run produced, addressed by cell and rep.

    python transcripts.py                        # what is stored, and how big
    python transcripts.py <cell_id>              # every record for that cell
    python transcripts.py <cell_id> --failed     # only the ones that parsed badly
    python transcripts.py --compact              # merge finished reps, offline

The store answers what a run scored. This answers what the model actually said,
which is the question every surprising result starts with and which nothing in
this project kept until 2026-09-22. `50-findings/14` was written with a judge
failing to emit JSON in 18% of calls under one format and 2% under another, and
1,513 reps on disk that could not say why.

ONE FILE PER REP, AND WHY THAT IS THE WHOLE DESIGN
--------------------------------------------------
Layout: `evalkit_store/transcripts/<cell_id>/<rep>.jsonl.gz`.

The first version appended every rep of a cell into one archive. That put a
worker's crash into a file holding OTHER reps' records, and this project kills
workers routinely -- the pool's lease exists for precisely that, and three
workers ran the last sweep. The reader grew a tolerance for truncated tails,
which is treating the symptom: a run that cannot be trusted to finish must not
be allowed to write where another run's results live.

With one file per rep:

  * a killed attempt damages only its own rep, which the pool releases and
    re-runs anyway, so the damage is to data that was about to be replaced;
  * the retry opens with "wt" and truncates, so it never appends to the corpse
    of the attempt before it;
  * no two processes ever hold the same file, so there is no interleaving to
    reason about and no lock to get wrong.

`run_suite` closes the file when the rep's row is committed, so a complete file
means a complete rep.

COMPACTION IS A SEPARATE, OFFLINE STEP
--------------------------------------
Per-rep files compress worse than one archive per cell, because a cell's reps
share a prompt template and gzip can only exploit that within a file. `--compact`
merges a cell's finished reps into `<cell_id>.jsonl.gz` and removes the parts,
which is where the 51x measured ratio lands.

It is deliberately NOT done by the workers. Two workers can hold different reps
of the same cell at once, so having them merge into a shared archive would
reintroduce exactly the shared-writer problem this layout exists to remove.
Run it when nothing is writing. It is idempotent and safe to interrupt: the
merged archive is written to a temporary file and moved into place, and the
parts are removed only afterwards.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "evalkit_store" / "transcripts"


def parts_for(cell_id: str) -> list[Path]:
    d = DIR / cell_id
    return sorted(d.glob("*.jsonl.gz"), key=lambda p: int(p.name.split(".")[0])) \
        if d.is_dir() else []


def archive_for(cell_id: str) -> Path:
    return DIR / f"{cell_id}.jsonl.gz"


def _read_gz(p: Path) -> tuple[list[dict], str | None]:
    out, note = [], None
    try:
        with gzip.open(p, "rt", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    note = "last line incomplete"
    except (EOFError, gzip.BadGzipFile, OSError) as e:
        note = f"{type(e).__name__} after {len(out)} record(s)"
    return out, note


def read(cell_id: str) -> tuple[list[dict], list[str]]:
    """Every record for a cell, from the archive and any un-compacted reps.

    Damage is reported per file and never loses another file's records, which
    is the property the per-rep layout exists to give.
    """
    out, notes = [], []
    arc = archive_for(cell_id)
    if arc.is_file():
        recs, note = _read_gz(arc)
        out += recs
        if note:
            notes.append(f"{arc.name}: {note}")
    for p in parts_for(cell_id):
        recs, note = _read_gz(p)
        out += recs
        if note:
            notes.append(f"{cell_id}/{p.name}: {note} -- that rep was "
                         f"interrupted; the pool re-runs it")
    if not out and not notes:
        notes.append(f"no transcript for {cell_id}")
    return out, notes


def cells() -> list[str]:
    if not DIR.is_dir():
        return []
    ids = {p.name[: -len(".jsonl.gz")] for p in DIR.glob("*.jsonl.gz")}
    ids |= {p.name for p in DIR.iterdir() if p.is_dir()}
    return sorted(ids)


def compact(cell_id: str) -> tuple[int, int]:
    """Merge a cell's finished reps into its archive. Returns (reps, records)."""
    parts = parts_for(cell_id)
    if not parts:
        return 0, 0
    existing, _ = _read_gz(archive_for(cell_id)) if archive_for(cell_id).is_file() \
        else ([], None)
    merged = list(existing)
    used = 0
    for p in parts:
        recs, note = _read_gz(p)
        if note:
            continue          # an interrupted rep: leave the part where it is
        merged += recs
        used += 1
    if not used:
        return 0, 0
    tmp = archive_for(cell_id).with_suffix(".gz.tmp")
    with gzip.open(tmp, "wt", encoding="utf-8", compresslevel=9) as fh:
        for r in merged:
            fh.write(json.dumps(r) + "\n")
    os.replace(tmp, archive_for(cell_id))     # only now are the parts redundant
    for p in parts:
        recs, note = _read_gz(p)
        if not note:
            p.unlink(missing_ok=True)
    d = DIR / cell_id
    if d.is_dir() and not any(d.iterdir()):
        d.rmdir()
    return used, len(merged)


def failed(records: list[dict]) -> list[dict]:
    """Generations whose text holds no closed JSON object.

    The same condition the judge applies, so this selects exactly the calls that
    produced no usable verdict -- the population that could not be inspected at
    all before transcripts existed.
    """
    return [r for r in records
            if "{" not in (r.get("text") or "") or "}" not in (r.get("text") or "")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cell", nargs="?")
    ap.add_argument("--failed", action="store_true",
                    help="only generations that produced no closed JSON object")
    ap.add_argument("--full", action="store_true", help="do not truncate text")
    ap.add_argument("--compact", action="store_true",
                    help="merge finished reps into per-cell archives (run with "
                         "no workers active)")
    args = ap.parse_args()

    if args.compact:
        before = sum(p.stat().st_size for p in DIR.rglob("*.jsonl.gz")) if DIR.is_dir() else 0
        reps = recs = done = 0
        for c in cells():
            r, n = compact(c)
            if r:
                done += 1
                reps += r
                recs += n
        after = sum(p.stat().st_size for p in DIR.rglob("*.jsonl.gz")) if DIR.is_dir() else 0
        print(f"compacted {reps} rep(s) across {done} cell(s), {recs} record(s)")
        print(f"{before/2**20:.2f} MiB -> {after/2**20:.2f} MiB")
        return

    if not args.cell:
        cs = cells()
        if not cs:
            print(f"no transcripts under {DIR}")
            print("written by default; LATTICE_TRANSCRIPT=0 disables them")
            return
        size = sum(p.stat().st_size for p in DIR.rglob("*.jsonl.gz"))
        loose = sum(1 for c in cs for _ in parts_for(c))
        print(f"{len(cs)} cell(s), {size/2**20:.2f} MiB on disk"
              + (f", {loose} rep(s) not yet compacted" if loose else ""))
        for c in cs[:20]:
            n = len(parts_for(c))
            arc = "archive" if archive_for(c).is_file() else ""
            print(f"  {c}  {arc}{' + ' if arc and n else ''}"
                  f"{f'{n} loose rep(s)' if n else ''}")
        if len(cs) > 20:
            print(f"  ... and {len(cs)-20} more")
        return

    recs, notes = read(args.cell)
    for n in notes:
        print(f"[{n}]")
    if args.failed:
        recs = failed(recs)
        print(f"{len(recs)} generation(s) with no closed JSON object")
    for r in recs:
        print(f"--- rep {r.get('rep')} task {r.get('task')} "
              f"{r.get('model')} {r.get('judge_format')} "
              f"| prompt {r.get('prompt_tok')} tok, out {r.get('eval_count')} tok, "
              f"done_reason {r.get('done_reason')}")
        t = r.get("text") or ""
        print(t if args.full else (t[:600] + ("..." if len(t) > 600 else "")))
        if r.get("thinking"):
            th = r["thinking"]
            print(f"  [thinking {len(th)} chars]"
                  + ("" if not args.full else "\n" + th))


if __name__ == "__main__":
    main()
