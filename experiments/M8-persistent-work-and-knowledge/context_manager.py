"""Work package 3: the context manager.

Specification: docs/10-technical/14-context-manager.md

Three operations -- register, track, recall -- over a live set that holds
REFERENCES and metadata, never content. The turn input is composed afresh every
turn; there is no per-invocation bundle.

This module never initiates a crossing, never gates, never holds artifact
content. It registers what the caller says crossed, and recall runs the
configured (here: naive/degenerate) policy over what's registered.
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

# Crossing types. 14-context-manager.md, Track.
READ = "read"
GENERATION_REASONING = "generation:reasoning"   # Splitting a generation
GENERATION_CONCLUSION = "generation:conclusion"
RETRIEVAL = "retrieval"
EFFECT_RESPONSE = "effect_response"

# The two labels. 14-context-manager.md, The two labels.
LABEL_OBJECTIVE = "objective"
LABEL_DERIVED_SCOPE = "derived_scope"
LABEL_NONE = None


@dataclass
class LiveSetEntry:
    live_set_id: str
    work_item_id: str          # which task's live set this belongs to
    claim_ref: str              # into knowledge_model.py
    crossing_type: str
    label: Optional[str]
    origin_invocation_id: str
    registered_at: int          # per-run monotonic sequence, not wall clock


@dataclass
class TurnInputRecord:
    """What observability keeps per turn (14-context-manager.md, Observability):
    included entries in order, dropped entries, whether truncation happened.
    Kept here too for M8's small-test purposes; the real copy is 02's job.
    """
    included: list       # [live_set_id, ...] in presentation order
    dropped: list
    truncated: bool


class ContextManager:
    """Live set storage: one JSONL append log per work item, replayed to build
    the in-memory set. No content is ever held here -- only claim_refs.
    """

    def __init__(self, root: Path | str):
        self.root = Path(root)
        (self.root / "live_sets").mkdir(parents=True, exist_ok=True)
        self._seq = 0

    # ------------------------------------------------------------ register

    def register(self, work_item_id: str, *, claim_ref: str, crossing_type: str,
                origin_invocation_id: str, label: Optional[str] = None) -> LiveSetEntry:
        """Every artifact crossing in. MUST NOT be called to initiate a crossing
        -- the caller already obtained claim_ref from the knowledge model; this
        just records that it happened and attaches it to work_item_id's live set.
        """
        self._seq += 1
        entry = LiveSetEntry(live_set_id=f"ls_{uuid.uuid4().hex[:12]}",
                             work_item_id=work_item_id, claim_ref=claim_ref,
                             crossing_type=crossing_type, label=label,
                             origin_invocation_id=origin_invocation_id,
                             registered_at=self._seq)
        self._append(work_item_id, entry)
        return entry

    def register_task_start(self, work_item_id: str, *, intent_claim_ref: str,
                            objective_claim_ref: str, scope_claim_ref: str,
                            invocation_id: str) -> list[LiveSetEntry]:
        """A new task's live set is not empty: the intent crosses as a read, the
        scope evaluation's reads attach, its output attaches as `derived_scope`,
        and the task's objective attaches as `objective`
        (14-context-manager.md: "A new task's live set is not empty either").

        This is the ungated runtime call at task creation (13-work-record.md:
        "attachment at creation is a runtime call, not a proposed effect") --
        no capability evaluation, no gate. A processor attaching mid-work is a
        different act (4c) and goes through `register` with no special label.
        """
        out = [self.register(work_item_id, claim_ref=intent_claim_ref,
                            crossing_type=READ, origin_invocation_id=invocation_id)]
        out.append(self.register(work_item_id, claim_ref=scope_claim_ref,
                                 crossing_type=RETRIEVAL,
                                 origin_invocation_id=invocation_id,
                                 label=LABEL_DERIVED_SCOPE))
        out.append(self.register(work_item_id, claim_ref=objective_claim_ref,
                                 crossing_type=GENERATION_CONCLUSION,
                                 origin_invocation_id=invocation_id,
                                 label=LABEL_OBJECTIVE))
        return out

    # -------------------------------------------------------------- track

    def live_set(self, work_item_id: str) -> list[LiveSetEntry]:
        """It grows within a task's life and does not shrink -- reading it back
        is a pure replay of the append log.
        """
        p = self._log_path(work_item_id)
        if not p.is_file():
            return []
        return [LiveSetEntry(**json.loads(l)) for l in
               p.read_text(encoding="utf-8").splitlines() if l.strip()]

    def end_task(self, work_item_id: str) -> list[str]:
        """Returns the claim_refs that lose root status when this live set ends
        (12-knowledge-model.md: "a task ending is the trigger"). Does not itself
        touch the knowledge model -- wiring.py composes this with
        KnowledgeStore.sweep_from.
        """
        return [e.claim_ref for e in self.live_set(work_item_id)]

    # ------------------------------------------------------------- recall

    def recall(self, work_item_id: str, *, turn_budget: int = 8000,
              approx_tokens_per_entry: int = 200) -> TurnInputRecord:
        """The degenerate recall policy (07-naive-context-assembly.md): order by
        registered_at, include until budget runs out, EXCEPT never drop a
        labelled entry -- "never drop the objective or the ceiling, whatever the
        budget does" (14-context-manager.md, the field `label` earns its place
        on exactly this branch).

        This is deliberately the naive baseline, not a good policy -- the point
        of naming it that way is that a better one is a replacement on the same
        axis, not a different kind of thing.
        """
        entries = sorted(self.live_set(work_item_id), key=lambda e: e.registered_at)
        labelled = [e for e in entries if e.label]
        unlabelled = [e for e in entries if not e.label]

        included, dropped, budget = [], [], turn_budget
        for e in labelled:
            included.append(e.live_set_id)
            budget -= approx_tokens_per_entry
        truncated = False
        for e in unlabelled:
            if budget < approx_tokens_per_entry:
                dropped.append(e.live_set_id)
                truncated = truncated or budget > 0   # partial room counts as truncation
                continue
            included.append(e.live_set_id)
            budget -= approx_tokens_per_entry
        return TurnInputRecord(included=included, dropped=dropped, truncated=truncated)

    # ------------------------------------------------------------- internals

    def _log_path(self, work_item_id: str) -> Path:
        return self.root / "live_sets" / f"{work_item_id}.jsonl"

    def _append(self, work_item_id: str, entry: LiveSetEntry):
        with self._log_path(work_item_id).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(entry)) + "\n")
