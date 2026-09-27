"""Which setup produced a stage record -- one helper, every workflow.

`stage_influence_*.jsonl` is append-only across every sweep ever run. Until
2026-09-27 only judge_caveat, judge_bypass and judge_anchored recorded `model`
and `results_subdir` on the record, and no workflow recorded the cell. The rest
wrote records that cannot be told apart by model, protocol or sampling, and any
join against a results file silently crossed models (50-findings/17, A14).

`run_suite.run_task` already computes the cell id and exports it as
LATTICE_CELL, with the rep as LATTICE_REP, around the arm call. The cell id
carries model, backend, protocol, sampling, fixture and arm version in one
value, so it is the join key: a stage record's `cell_id` is the store row's
`cell_id`. Nothing here derives anything; it copies what the runner exported.

Records written before this helper existed carry no `cell_id` and must stay
that way. They are not attributable, and a reader must treat them as such
rather than guessing.

Stage-record fields only. None of this reaches the model.
"""
from __future__ import annotations

import os
import time


def setup_tags() -> dict:
    """Fields to merge onto a stage record just before it is written."""
    rep = os.environ.get("LATTICE_REP")
    return {
        # The join key. None when the arm was called outside run_suite, which
        # is itself a fact about the record: it has no store row to join to.
        "cell_id": os.environ.get("LATTICE_CELL"),
        "cell_rep": int(rep) if rep and rep.isdigit() else None,
        # Kept alongside the cell for readers that predate it, and because
        # judge_caveat / judge_bypass / judge_anchored already wrote them.
        "model": os.environ.get("LATTICE_EVAL_MODEL"),
        "judge_format": os.environ.get("LATTICE_JUDGE_FORMAT", "decision_first"),
        "results_subdir": os.environ.get("LATTICE_RESULTS_SUBDIR"),
        "t_end": time.time(),
    }
