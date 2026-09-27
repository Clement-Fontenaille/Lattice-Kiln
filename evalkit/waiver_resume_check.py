"""What `run_suite --store-resume` would find, per arm, under each waiver mode.

    python evalkit/waiver_resume_check.py --model nemotron3-nano-4b:latest \\
        --waivers queue-a-2026-09-27                     # against the real store
    python evalkit/waiver_resume_check.py --model M --from-results \\
        experiments/M6-evaluation-suite/results_matrix_nemotron3-nano-4b

READ-ONLY on the store: it only calls Store.have(). With --from-results it
builds a throwaway store in a temp dir from the rows run_suite recorded in a
results directory (setups exactly as recorded) and never opens the real one.

Cells come from run_suite's own _cell_for(), so the arm_sha is today's and the
params are the real _eval_params() -- the same query run_suite's --store-resume
block makes. The environment must be the sweep's (the matrix ENV is applied
by default; --env-none to use the caller's). Three columns:

    no ids          what run_suite does with no --waivers (today's behaviour)
    --waivers IDS   with the named recorded families admitted
    --no-waivers    hashes alone
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
M6 = HERE.parent / "experiments" / "M6-evaluation-suite"
MATRIX_ENV = {"LATTICE_PROTOCOL": "tools", "LATTICE_PROTOCOL_VARIANT": "v2",
              "LATTICE_TEMPERATURE": "0.6", "LATTICE_TOP_P": "0.95",
              "LATTICE_MIN_PREDICT": "8192", "LATTICE_NUM_CTX": "16384"}
ARMS = ["baseline", "monolith", "monolith_recovery", "judge_anchored", "judge_caveat",
        "judge_bypass", "judge_fullctx", "m7", "test_synth", "dloop", "staged"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--waivers", nargs="+", required=True, metavar="ID")
    ap.add_argument("--store")
    ap.add_argument("--from-results", type=Path)
    ap.add_argument("--arms", nargs="+", default=ARMS)
    ap.add_argument("--env-none", action="store_true")
    a = ap.parse_args(argv)
    if not a.env_none:
        os.environ.update(MATRIX_ENV)
    os.environ["LATTICE_EVAL_MODEL"] = a.model
    os.environ.setdefault("LATTICE_TRANSCRIPT", "0")
    sys.path.insert(0, str(M6))
    sys.path.insert(0, str(HERE))
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        import run_suite as rs
    from setup_key import Cell, load_waivers
    from store import Store

    tmp = None
    if a.from_results:
        tmp = tempfile.TemporaryDirectory(prefix="waiver_check_")
        st = Store(Path(tmp.name))
        for f in sorted(a.from_results.glob("*.json")):
            for r in json.loads(f.read_text(encoding="utf-8")):
                if isinstance(r, dict) and r.get("setup"):
                    st.add(Cell(**r["setup"]), [r], provenance="recorded", source=str(f))
    else:
        st = Store(Path(a.store) if a.store else None)

    modes = {"no ids": load_waivers(), "--waivers " + ",".join(a.waivers): load_waivers(a.waivers),
             "--no-waivers": []}
    stored: dict[str, set] = {}
    for e in st._index_entries():
        if e.get("model") == a.model:
            stored.setdefault(e["arm"], set()).add(e["arm_sha"])
    tasks, *_ = rs.load_tasks()
    print(f"{a.model}  store: {'scratch from ' + str(a.from_results) if tmp else st.path}")
    print(f"{'arm':18} {'arm_sha now':17} {'stored arm_sha':34} " + " ".join(f"{m:>30}" for m in modes))
    for arm in a.arms:
        cells = [rs._cell_for(t["id"], arm) for t in tasks]
        cols = []
        for wv in modes.values():
            n = sum(min(1, st.have(c, waivers=wv, params_query=dict(json.loads(c.params))))
                    for c in cells)
            cols.append(f"{n}/{len(cells)}")
        print(f"{arm:18} {cells[0].arm_sha:17} {','.join(sorted(stored.get(arm, [])))[:34]:34} "
              + " ".join(f"{c:>30}" for c in cols))
    print("\n(cells holding at least one rep, per arm; min(1, have) per task)")
    if tmp:
        tmp.cleanup()
    return 0


if __name__ == "__main__":
    sys.exit(main())
