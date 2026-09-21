"""Read the raw generations a run produced, addressed by cell.

    python transcripts.py                        # what is stored, and how big
    python transcripts.py <cell_id>              # every record for that cell
    python transcripts.py <cell_id> --failed     # only the ones that parsed badly

The store answers what a run scored. This answers what the model actually said,
which is the question every surprising result starts with and which nothing in
this project kept until 2026-09-22. `50-findings/14` was written with a judge
failing to emit JSON in 18% of calls under one format and 2% under another, and
1,513 reps on disk that could not say why.

Files are `evalkit_store/transcripts/<cell_id>.jsonl.gz`, one per cell, written
in append mode by whichever worker ran the rep.

TWO THINGS THE READER HAS TO TOLERATE, both consequences of that:

  Multi-member gzip. Appending re-opens the file, and each open starts a new
  gzip member. Concatenated members are a valid gzip stream and `gzip.open`
  reads straight through them, so this needs no special handling -- it is noted
  because the file looks odd to tools that assume one member.

  A truncated tail. A worker killed mid-write leaves a partial final member,
  and this project kills workers routinely -- the lease exists for exactly that.
  Reading then raises EOFError or BadGzipFile *after* yielding good records, so
  the loop below keeps what it got instead of losing a whole cell to its last
  line. Corruption is reported, never silently skipped.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "evalkit_store" / "transcripts"


def path_for(cell_id: str) -> Path:
    return DIR / f"{cell_id}.jsonl.gz"


def read(cell_id: str) -> tuple[list[dict], str | None]:
    """Records for a cell, plus a note if the file ends badly."""
    p = path_for(cell_id)
    if not p.is_file():
        return [], f"no transcript for {cell_id}"
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
                    note = "last line was incomplete (worker killed mid-write)"
    except (EOFError, gzip.BadGzipFile, OSError) as e:
        note = f"stream ends badly after {len(out)} record(s): {type(e).__name__}"
    return out, note


def cells() -> list[Path]:
    return sorted(DIR.glob("*.jsonl.gz")) if DIR.is_dir() else []


def failed(records: list[dict]) -> list[dict]:
    """Generations whose text holds no closed JSON object.

    The same condition the judge applies, so this selects exactly the calls that
    produced no usable verdict -- the population that could not be inspected
    before transcripts existed.
    """
    return [r for r in records
            if "{" not in (r.get("text") or "") or "}" not in (r.get("text") or "")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cell", nargs="?")
    ap.add_argument("--failed", action="store_true",
                    help="only generations that produced no closed JSON object")
    ap.add_argument("--full", action="store_true", help="do not truncate text")
    args = ap.parse_args()

    if not args.cell:
        cs = cells()
        if not cs:
            print(f"no transcripts under {DIR}")
            print("they are written by default; LATTICE_TRANSCRIPT=0 disables them")
            return
        raw = sum(p.stat().st_size for p in cs)
        print(f"{len(cs)} cell(s), {raw/2**20:.1f} MiB compressed, under {DIR}")
        for p in cs[:20]:
            print(f"  {p.stem.replace('.jsonl','')}  {p.stat().st_size/1024:.0f} KiB")
        if len(cs) > 20:
            print(f"  ... and {len(cs)-20} more")
        return

    recs, note = read(args.cell)
    if note:
        print(f"[{note}]")
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
