"""Persist a probe's per-call measurements before it summarises them.

A summary is a lossy encoding chosen before the question is known. A `-22%`
median once cost a 74-minute rerun because the values under it were gone.
Every probe therefore writes what each call returned, and prints a summary of
that file rather than instead of it.

    evalkit_store/probe_runs/<probe>_<YYYYmmddTHHMMSS>.json
        {"probe", "written_at", "argv", "meta": {...}, "calls": [...]}

Timestamped, never overwritten: two runs of one probe are two files. `meta`
holds what was held fixed (model, sampling, caps, prompt files); `calls` holds
one entry per request, or per model / per arm where the probe's unit is larger,
with the raw response fields the summary is computed from.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "evalkit_store" / "probe_runs"


def persist(probe: str, meta: dict, calls: list) -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%S")
    RUNS.mkdir(parents=True, exist_ok=True)
    out = RUNS / f"{probe}_{stamp}.json"
    n = 1
    while out.exists():                    # same second, same probe: keep both
        n += 1
        out = RUNS / f"{probe}_{stamp}_{n}.json"
    out.write_text(json.dumps({"probe": probe, "written_at": stamp,
                               "argv": sys.argv[1:], "meta": meta,
                               "calls": calls}, indent=1, default=str),
                   encoding="utf-8")
    print(f"raw values -> {out.relative_to(ROOT)}", flush=True)
    return out
