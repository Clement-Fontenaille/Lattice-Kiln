"""Work package 4: the wiring between the three stores.

"Each store is simple and the edges between them are where the specification
pass found its gaps." (08-persistent-work-and-knowledge.md, Work packages)

None of the three stores reaches into another on its own -- 12-knowledge-model.md
is explicit that nothing in the permission or invariant layers depends on it, and
13-work-record.md holds no artifact reference at all. This module is where the
edges actually get walked, and it is deliberately the only place that imports all
three.

Three things wired here:
  1. Task creation attaches intent/objective/scope -- ungated runtime call.
  2. 4c mid-work attachment -- a gated effect, registered like any other.
  3. Incremental removal when a task reaches a terminal state.
"""
from __future__ import annotations

from context_manager import (ContextManager, GENERATION_CONCLUSION, LABEL_NONE,
                             READ)
from knowledge_model import KnowledgeStore, ParentEdge, REASONED
from work_record import ABANDONED, EXECUTED, WorkItem, WorkRecordStore


class Substrate:
    """The three stores plus the two edges the spec found underspecified.

    Not a processor, not gated, not a cognitive component -- this is runtime
    plumbing that a real system's runtime would call at the points named below.
    Nothing here decides anything; it composes three already-specified writes.
    """

    def __init__(self, work: WorkRecordStore, knowledge: KnowledgeStore,
                context: ContextManager):
        self.work = work
        self.knowledge = knowledge
        self.context = context

    # ----------------------------------------------- 1. task creation

    def create_task(self, *, intent_content: str, formulation: str,
                    scope_boundary: str, scope_derivation: str,
                    invocation_id: str) -> WorkItem:
        """The ungated path: intent (out of band, here simulated as arriving
        with the task), the derived scope, and the objective all attach at
        creation with no capability check and no gate
        (14-context-manager.md: "attachment at creation is a runtime call, not
        a proposed effect").
        """
        from work_record import DERIVED, Scope

        intent = self.work.write_intent(intent_content)
        scope = Scope(boundary=scope_boundary, derivation=scope_derivation,
                      scope_state=DERIVED)
        item = self.work.create_item(intent_ref=intent.intent_id,
                                     formulation=formulation, scope=scope,
                                     ceiling=scope_derivation)

        intent_claim = self.knowledge.write_observation(
            {"kind": "intent", "text": intent_content}, source="operator")
        objective_claim = self.knowledge.write_observation(
            {"kind": "objective", "text": formulation}, source="system")
        scope_claim = self.knowledge.write_observation(
            {"kind": "derived_scope", "boundary": scope_boundary,
             "derivation": scope_derivation}, source="invariant_processor")

        self.context.register_task_start(
            item.work_item_id, intent_claim_ref=intent_claim.claim_id,
            objective_claim_ref=objective_claim.claim_id,
            scope_claim_ref=scope_claim.claim_id, invocation_id=invocation_id)
        return item

    # ----------------------------------------------- 2. mid-work attachment

    def attach(self, work_item_id: str, content: dict, *, source: str,
              crossing_type: str, invocation_id: str,
              parents: list[ParentEdge] | None = None) -> str:
        """4c: a processor deliberately attaching an artifact. A GATED effect
        in the real system (the caller is assumed to have already passed
        capability+gate); what this does is the two writes 4c actually causes:
        an Observation (or proposed claim, if the caller already gated a type-5
        write) and a live-set registration with no label.

        Returns the claim_id, since callers commonly want to reference what
        they just attached.
        """
        claim = self.knowledge.write_observation(content, source=source,
                                                  parents=parents)
        self.context.register(work_item_id, claim_ref=claim.claim_id,
                              crossing_type=crossing_type,
                              origin_invocation_id=invocation_id, label=LABEL_NONE)
        return claim.claim_id

    # ----------------------------------------------- 3. incremental removal

    def end_task(self, work_item_id: str, *, effect_ref: str,
                invocation_id: str, terminal: str = EXECUTED) -> list[str]:
        """Transitions the item to a terminal state, then triggers the
        incremental removal that terminal state causes
        (12-knowledge-model.md: "a task ending is the trigger").

        Computing `still_live` -- every claim still reachable from some OTHER
        live task -- is the one piece knowledge_model.py explicitly leaves to
        the caller, because it cannot see the work record or other live sets on
        its own. That's done here by walking every other work item's live set.
        """
        if terminal not in (ABANDONED, EXECUTED):
            raise ValueError("end_task terminal must be abandoned or executed")
        item = self.work.get_item(work_item_id)
        if item.is_live():
            # conclude() may already have terminated the item (answered/declined
            # auto-terminate). Only transition here if it has not.
            self.work.transition_item(work_item_id, terminal, effect_ref=effect_ref,
                                      invocation_ref=invocation_id)

        departing = self.context.end_task(work_item_id)
        still_live = self._live_claim_refs(exclude_work_item=work_item_id)
        return self.knowledge.sweep_from(departing, still_live=still_live)

    def _live_claim_refs(self, *, exclude_work_item: str) -> set:
        """Every claim_ref still held by some OTHER live work item's live set.
        Naive: scans every live-set log. Fine at this store's expected size
        (12-knowledge-model.md's own naive-default reasoning applies here too).
        """
        out = set()
        for p in (self.context.root / "live_sets").glob("*.jsonl"):
            wid = p.stem
            if wid == exclude_work_item:
                continue
            try:
                item = self.work.get_item(wid)
            except Exception:  # noqa: BLE001
                continue
            if not item.is_live():
                continue
            out.update(e.claim_ref for e in self.context.live_set(wid))
        return out
