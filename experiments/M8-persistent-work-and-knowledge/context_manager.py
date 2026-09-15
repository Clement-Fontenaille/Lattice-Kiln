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
    """Kind 5, 02-observability-event-model.md: "the recorded unit is the turn,
    not the invocation." MUST carry, per that spec: what was presented (in
    order, WITH crossing type -- "flattening crossing type here defeats the
    authored-versus-generated requirement at the one point where the erasure
    cannot be recovered"), what was held back, `policy_ref`, which prefix this
    turn continued from, and isolation requested vs actually granted ("a judge
    whose isolation was silently degraded is indistinguishable afterwards from
    one that had it, which is the case the record exists for").

    M9's own accounting: packages 1 and 2 ("the recall trace" / "turn-input
    records") are explicitly sayable to land with M8 rather than waiting on M9
    proper, so this is that landing, not a preview of unbuilt M9 work.
    """
    invocation_id: str
    turn_index: int                    # per-work-item, monotonic from 1
    included: list       # [(live_set_id, crossing_type), ...] in presentation order
    dropped: list                       # [live_set_id, ...]
    truncated: bool
    policy_ref: str                     # which recall policy produced this selection
    continued_from: Optional[str]       # prefix_id, or None (a fresh sequence)
    isolation_requested: str            # share_nothing | share_base | continue(id)
    isolation_granted: str              # what was ACTUALLY granted -- may differ
    stub_isolation: bool = True         # True until a real arbitration policy can degrade a request


class ContextManager:
    """Live set storage: one JSONL append log per work item, replayed to build
    the in-memory set. No content is ever held here -- only claim_refs.
    """

    def __init__(self, root: Path | str):
        self.root = Path(root)
        (self.root / "live_sets").mkdir(parents=True, exist_ok=True)
        (self.root / "turn_inputs").mkdir(parents=True, exist_ok=True)
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

    def recall(self, work_item_id: str, *, invocation_id: str,
              turn_budget: int = 8000, approx_tokens_per_entry: int = 200,
              isolation_requested: str = "share_nothing",
              continued_from: Optional[str] = None) -> TurnInputRecord:
        """The degenerate recall policy (07-naive-context-assembly.md): order by
        registered_at, include until budget runs out, EXCEPT never drop a
        labelled entry -- "never drop the objective or the ceiling, whatever the
        budget does" (14-context-manager.md, the field `label` earns its place
        on exactly this branch).

        This is deliberately the naive baseline, not a good policy -- the point
        of naming it that way is that a better one is a replacement on the same
        axis, not a different kind of thing. The record it produces (kind 5) is
        real regardless of how naive the policy is; recording is M9 packages 1-2,
        not the policy itself.

        `isolation_requested` and `continued_from` are the caller's declared
        preference (06-processor-contract.md is what would actually set these;
        M8 has no processor-instantiation record to read them from, so they are
        a seam the caller fills in, like `ceiling` in work_record.py). This
        naive policy NEVER arbitrates or degrades what was requested -- it has
        no prefix-sharing mechanism to degrade INTO -- so `isolation_granted`
        always equals what was requested here. That equality is itself the
        build decision to flag: a real arrangement with finite slots WILL
        sometimes degrade a preference (14-context-manager.md, Arbitration),
        and this naive policy cannot yet exhibit that, which is exactly the
        kind of gap 14-context-manager.md warns is invisible unless recorded --
        recorded here as `stub_isolation=True` so a reader does not mistake
        "never degrades" for "was never under pressure."
        """
        entries = sorted(self.live_set(work_item_id), key=lambda e: e.registered_at)
        labelled = [e for e in entries if e.label]
        unlabelled = [e for e in entries if not e.label]

        included, dropped, budget = [], [], turn_budget
        for e in labelled:
            included.append((e.live_set_id, e.crossing_type))
            budget -= approx_tokens_per_entry
        for e in unlabelled:
            if budget < approx_tokens_per_entry:
                dropped.append(e.live_set_id)
                continue
            included.append((e.live_set_id, e.crossing_type))
            budget -= approx_tokens_per_entry
        # truncated means exactly "something was dropped for budget reasons" --
        # NOT "budget still had partial room left over." A prior version tied
        # this to `budget > 0` at the point of the first drop, which is False
        # whenever the labelled entries alone already exhausted (or exceeded)
        # the turn budget, silently reporting truncated=False while `dropped`
        # was non-empty -- caught by M9's test_failure_modes.py exercising
        # check_overload() on a turn where anchors alone ate the whole budget.
        truncated = bool(dropped)

        turn_index = self._next_turn(work_item_id)
        record = TurnInputRecord(
            invocation_id=invocation_id, turn_index=turn_index, included=included,
            dropped=dropped, truncated=truncated, policy_ref="naive-degenerate-v1",
            continued_from=continued_from, isolation_requested=isolation_requested,
            isolation_granted=isolation_requested)
        self._append_turn_input(work_item_id, record)
        return record

    def turn_inputs(self, work_item_id: str) -> list[TurnInputRecord]:
        """Read back every turn-input record for this item, in turn order."""
        p = self._turn_input_path(work_item_id)
        if not p.is_file():
            return []
        out = []
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                d = json.loads(line)
                d["included"] = [tuple(x) for x in d["included"]]
                out.append(TurnInputRecord(**d))
        return out

    # ------------------------------------------------------------- internals

    def _log_path(self, work_item_id: str) -> Path:
        return self.root / "live_sets" / f"{work_item_id}.jsonl"

    def _turn_input_path(self, work_item_id: str) -> Path:
        return self.root / "turn_inputs" / f"{work_item_id}.jsonl"

    def _next_turn(self, work_item_id: str) -> int:
        p = self._turn_input_path(work_item_id)
        if not p.is_file():
            return 1
        return sum(1 for l in p.read_text(encoding="utf-8").splitlines() if l.strip()) + 1

    def _append_turn_input(self, work_item_id: str, record: TurnInputRecord):
        with self._turn_input_path(work_item_id).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(record)) + "\n")

    def _append(self, work_item_id: str, entry: LiveSetEntry):
        with self._log_path(work_item_id).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(entry)) + "\n")
