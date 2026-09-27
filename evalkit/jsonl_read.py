"""Read a JSONL file that something may still be writing.

Lifted out of `transcripts._read_gz` so every reader shares one tolerance
instead of each crashing in its own way. A sweep appends to the store index,
the row files, the stage logs and the transcripts while analysis reads them;
twice a reader died on the half-written final line of a file that was simply
not finished yet.

The rule is narrow on purpose:

  * the FINAL line failing to parse is a partial tail. Stop there, keep
    everything before it, and say so. The writer will finish it.
  * a gzip stream ending early (EOFError, BadGzipFile) is the same thing
    one layer down: keep what decoded, say so.
  * a line failing to parse ANYWHERE ELSE is not a partial tail -- no append
    produces it -- so by default it raises. `strict=False` downgrades it to a
    note, for the transcript reader, which has always tolerated it.

Plain `.jsonl` and `.jsonl.gz` are both handled; the suffix decides.
"""
from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path


def read_jsonl(path, *, strict: bool = True) -> tuple[list[dict], str | None]:
    """(records, note). `note` is None for a complete file."""
    p = Path(path)
    out: list = []
    bad: list[int] = []            # 1-based line numbers that did not parse
    last = 0                       # line number of the last non-blank line
    stream_note = None
    opener = gzip.open if p.suffix == ".gz" else open
    try:
        with opener(p, "rt", encoding="utf-8", errors="replace") as fh:
            for n, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                last = n
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    bad.append(n)
    except (EOFError, gzip.BadGzipFile) as e:
        stream_note = f"{type(e).__name__} after {len(out)} record(s)"
    except OSError as e:
        if p.suffix != ".gz":
            raise
        stream_note = f"{type(e).__name__} after {len(out)} record(s)"

    notes = []
    tail = bool(bad) and bad[-1] == last
    mid = bad[:-1] if tail else bad
    if tail:
        notes.append("last line incomplete")
    if mid:
        if strict:
            raise ValueError(f"{p}: line(s) {mid[:5]} are not JSON and are not the "
                             f"final line -- that is corruption, not a partial tail")
        notes.append(f"{len(mid)} unparseable line(s) before the end")
    if stream_note:
        notes.append(stream_note)
    return out, ("; ".join(notes) or None)


def load_jsonl(path, *, strict: bool = True) -> list[dict]:
    """Records only, with a partial tail reported on stderr rather than raised.
    A missing file is an empty list: an arm that never ran has no log."""
    p = Path(path)
    if not p.is_file():
        return []
    recs, note = read_jsonl(p, strict=strict)
    if note:
        print(f"[{p.name}: {note}; read {len(recs)} record(s)]", file=sys.stderr)
    return recs
