"""Work package 1: the work-record store.

Specification: docs/10-technical/13-work-record.md

Three record kinds, written under three different disciplines:
  Intent      write-once, out of band, never touched by any in-system actor.
  WorkItem    formulation and scope fixed at creation; state and conclusion mutate
              in place; current state readable in one fetch, no log replay.
  Transition  append-only, one log per item, kept alongside it.

Only a realized type-4 effect writes here (plus intent, arriving out of band).
This module does not gate anything -- the caller is expected to have already
passed capability and the gate. What it enforces is the SHAPE of the lineage:
containment against a ceiling it is handed, not derived; the immutability of
formulation/scope/intent; and the append-only discipline of the transition log.

Storage: the naive default the spec names -- plain JSON, one row per item/intent,
one JSONL per transition log. The service surface below is what's binding; nothing
outside this file may learn that a work item is a file (13-work-record.md,
General shape and the naive default).
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

# Work item states. 13-work-record.md, Work item states: `open` is this document's
# own addition -- 22-arch-cognition/01 names four things a state can change TO and
# never names what an item is before any of them happens. Live-vs-terminal is the
# predicate the whole retention mechanism runs on (12-knowledge-model.md,
# 14-context-manager.md), so it has to exist here for either of those to work.
OPEN = "open"
CHALLENGED = "challenged"
DEFERRED = "deferred"
ABANDONED = "abandoned"
EXECUTED = "executed"
LIVE_STATES = {OPEN, CHALLENGED, DEFERRED}
TERMINAL_STATES = {ABANDONED, EXECUTED}
ALL_STATES = LIVE_STATES | TERMINAL_STATES

# Scope states. 13-work-record.md, The declared scope.
STATED = "stated"
DERIVED = "derived"
PENDING = "pending"

# Conclusion verdicts. 13-work-record.md, Recorded conclusions.
ANSWERED = "answered"
BLOCKED = "blocked"
DECLINED = "declined"


class LineageError(Exception):
    """Raised when a creation or transition would break the shape of the lineage.

    This store rejects on shape (containment, immutability, log discipline). It
    never judges whether the work is right -- that is explicitly not its job
    (13-work-record.md, Responsibility).
    """


@dataclass
class Intent:
    intent_id: str
    content: str            # original human-authored text, verbatim
    entered_at: str


@dataclass
class Scope:
    boundary: str                    # natural-language mandate text
    derivation: Optional[str]        # what it was derived from; required unless stated
    scope_state: str                 # stated | derived | pending


@dataclass
class WorkItem:
    work_item_id: str
    intent_ref: str
    derived_from: list              # zero or more parent work_item_ids
    formulation: str
    scope: Scope
    state: str = OPEN
    conclusion: Optional[dict] = None   # {verdict, reasoning, effect_ref, invocation_ref, ts}

    def is_live(self) -> bool:
        return self.state in LIVE_STATES


@dataclass
class Transition:
    work_item_id: str
    transition: str          # challenged | deferred | abandoned | executed
    effect_ref: str
    invocation_ref: str
    ts: str
    app_state: str = "logged"     # logged -> applied, by a second append (never edited)
    seq: int = 0


class WorkRecordStore:
    """The naive filesystem default. See General shape and the naive default.

    work/
      intents/<intent_id>.json
      items/<work_item_id>.json
      transitions/<work_item_id>.jsonl
    """

    def __init__(self, root: Path | str):
        self.root = Path(root)
        (self.root / "intents").mkdir(parents=True, exist_ok=True)
        (self.root / "items").mkdir(parents=True, exist_ok=True)
        (self.root / "transitions").mkdir(parents=True, exist_ok=True)

    # ----------------------------------------------------------------- intent

    def write_intent(self, content: str) -> Intent:
        """Out of band, by a human. The only kind this store may not write itself.

        No transition log -- written once, read thereafter (13-work-record.md,
        Intent). Amendment is not implemented here: it is direct human action
        producing a NEW version, never an edit (open contract: intent versioning).
        """
        intent = Intent(intent_id=f"in_{uuid.uuid4().hex[:12]}",
                        content=content, entered_at=_now())
        self._write_json(self.root / "intents" / f"{intent.intent_id}.json",
                         asdict(intent))
        return intent

    def get_intent(self, intent_id: str) -> Intent:
        d = self._read_json(self.root / "intents" / f"{intent_id}.json")
        return Intent(**d)

    # -------------------------------------------------------------- work item

    def create_item(self, *, intent_ref: str, formulation: str, scope: Scope,
                    derived_from: Optional[list] = None,
                    ceiling: Optional[str] = None) -> WorkItem:
        """Effect 4a. Formulation and scope are fixed HERE and never rewritten.

        `ceiling` is the natural-language boundary derived from intent, handed in
        by the caller (03-capability-authority-model.md owns deciding containment;
        this store only refuses a creation whose scope wasn't checked against one).
        Passing ceiling=None skips the check -- a caller integrating the real scope
        checker must supply it; this is a seam, not a judgment this store makes.
        """
        if scope.scope_state != PENDING and ceiling is not None:
            if not _looks_contained(scope.boundary, ceiling):
                raise LineageError(
                    f"scope {scope.boundary!r} not contained in ceiling {ceiling!r}")
        if scope.scope_state == DERIVED and not scope.derivation:
            raise LineageError("a derived scope MUST carry its derivation "
                               "(13-work-record.md: an unrecorded derivation is "
                               "uncontestable)")
        item = WorkItem(work_item_id=f"wi_{uuid.uuid4().hex[:12]}",
                        intent_ref=intent_ref, derived_from=derived_from or [],
                        formulation=formulation, scope=scope, state=OPEN)
        self._write_json(self._item_path(item.work_item_id), _item_to_dict(item))
        return item

    def get_item(self, work_item_id: str) -> WorkItem:
        """One fetch, no log replay -- the orchestrator's most frequent read."""
        d = self._read_json(self._item_path(work_item_id))
        return _item_from_dict(d)

    def children(self, work_item_id: str) -> list[WorkItem]:
        out = []
        for p in (self.root / "items").glob("*.json"):
            d = self._read_json(p)
            if work_item_id in d.get("derived_from", []):
                out.append(_item_from_dict(d))
        return out

    def lineage(self, work_item_id: str) -> list:
        """[work_item, ..., intent]. 13-work-record.md, Service surface.

        Walks the FIRST parent only when an item has several (a merge). Multi-
        parent lineage reconstruction is left to the caller; this returns the
        primary chain, which is enough for the aggregate scope check's purpose.
        """
        chain = []
        item = self.get_item(work_item_id)
        chain.append(item)
        seen = {item.work_item_id}
        while item.derived_from:
            nxt = item.derived_from[0]
            if nxt in seen:
                break
            item = self.get_item(nxt)
            chain.append(item)
            seen.add(item.work_item_id)
        chain.append(self.get_intent(chain[0].intent_ref))
        return chain

    def scope_of(self, work_item_id: str):
        s = self.get_item(work_item_id).scope
        return (s.boundary, s.derivation, s.scope_state)

    def change_set(self, work_item_id: str) -> list:
        """13-work-record.md: composes with observability's realized-effect
        history rather than duplicating it. This store has no effect history of
        its own, so it returns transitions -- the closest thing it holds -- and
        documents the gap rather than faking a fuller answer.

        Open contract (13-work-record.md, What change_set actually returns):
        the real shape needs observability's effect log. Not built in M8.
        """
        return [asdict(t) for t in self.transitions(work_item_id)]

    # ----------------------------------------------------------------- write

    def transition_item(self, work_item_id: str, transition: str, *,
                        effect_ref: str, invocation_ref: str) -> Transition:
        """Effect 4b. State change only -- never formulation, never scope.

        One write path keeps the log and the item in step: log entry first
        (`logged`), then the item record, then a second append (`applied`). A
        transition left `logged` with no matching `applied` commit is the one a
        recovery procedure replays (13-work-record.md, Transition).
        """
        if transition not in (CHALLENGED, DEFERRED, ABANDONED, EXECUTED):
            raise LineageError(f"not a valid transition: {transition!r}")
        item = self.get_item(work_item_id)
        if not item.is_live():
            raise LineageError(f"{work_item_id} is terminal ({item.state}); "
                               "a terminal item does not transition further")

        seq = self._next_seq(work_item_id)
        t = Transition(work_item_id=work_item_id, transition=transition,
                       effect_ref=effect_ref, invocation_ref=invocation_ref,
                       ts=_now(), app_state="logged", seq=seq)
        self._append_transition(t)

        item.state = transition
        self._write_json(self._item_path(work_item_id), _item_to_dict(item))

        self._append_transition(Transition(
            work_item_id=work_item_id, transition=transition,
            effect_ref=effect_ref, invocation_ref=invocation_ref, ts=_now(),
            app_state="applied", seq=seq))
        return t

    def conclude(self, work_item_id: str, verdict: str, reasoning: str, *,
                effect_ref: str, invocation_ref: str,
                terminal: Optional[str] = None) -> WorkItem:
        """Effect 4d. Records a conclusion; the item's conclusion field mutates
        in place, which the spec explicitly allows (only state and conclusion do).

        Whether a conclusion ALSO ends the item is a build decision the spec
        does not pin down in one place. 13-work-record.md, Recorded conclusions
        says a false assumption or an already-satisfied request "end the item"
        (they are conclusions), while a different-problem or needs-investigation
        finding "end nothing" (they create a successor and are NOT this call at
        all). That maps cleanly onto declined-vs-not, but says nothing about
        `answered` or `blocked` terminating.

        This implementation's choice, stated so it can be overturned:
          answered  -> terminal=executed automatically, unless caller overrides
          declined  -> terminal=abandoned automatically, unless caller overrides
          blocked   -> NOT terminal by default; caller must pass `terminal`
                       explicitly if this occurrence of `blocked` should end the
                       item (M5's collapse of declined/blocked into one outcome
                       is exactly the failure keeping these separate exists to
                       prevent -- 13-work-record.md, Failure modes).
        """
        if verdict not in (ANSWERED, BLOCKED, DECLINED):
            raise LineageError(f"not a valid verdict: {verdict!r}")
        item = self.get_item(work_item_id)
        if not item.is_live():
            raise LineageError(f"{work_item_id} is terminal; conclusion already "
                               "reached or item otherwise closed")
        item.conclusion = {"verdict": verdict, "reasoning": reasoning,
                           "effect_ref": effect_ref, "invocation_ref": invocation_ref,
                           "ts": _now()}
        self._write_json(self._item_path(work_item_id), _item_to_dict(item))

        if terminal is None:
            terminal = {ANSWERED: EXECUTED, DECLINED: ABANDONED}.get(verdict)
        if terminal:
            self.transition_item(work_item_id, terminal,
                                 effect_ref=effect_ref, invocation_ref=invocation_ref)
        return self.get_item(work_item_id)

    def create_child(self, parent_id: str, *, formulation: str, scope: Scope,
                     ceiling: Optional[str] = None, effect_ref: str = "",
                     invocation_ref: str = "") -> WorkItem:
        """A split's child, or a successor with a redefined objective. Both are
        4a; what distinguishes them is not recorded as a different edge type but
        read off the PARENT's state afterward (13-work-record.md: an item left
        open while its children run was decomposed; one abandoned/executed as its
        successor was created was redefined).
        """
        parent = self.get_item(parent_id)
        return self.create_item(intent_ref=parent.intent_ref, formulation=formulation,
                                scope=scope, derived_from=[parent_id], ceiling=ceiling)

    # ----------------------------------------------------------------- reads

    def transitions(self, work_item_id: str) -> list[Transition]:
        p = self.root / "transitions" / f"{work_item_id}.jsonl"
        if not p.is_file():
            return []
        out = []
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(Transition(**json.loads(line)))
        return out

    def unapplied(self, work_item_id: str) -> list[Transition]:
        """Recovery reads rather than infers: any `logged` transition with no
        matching `applied` commit at the same seq is the one to replay.
        """
        rows = self.transitions(work_item_id)
        applied_seqs = {t.seq for t in rows if t.app_state == "applied"}
        return [t for t in rows if t.app_state == "logged" and t.seq not in applied_seqs]

    # ------------------------------------------------------------- internals

    def _item_path(self, work_item_id: str) -> Path:
        return self.root / "items" / f"{work_item_id}.json"

    def _next_seq(self, work_item_id: str) -> int:
        return len(self.transitions(work_item_id)) // 2 + 1

    def _append_transition(self, t: Transition):
        p = self.root / "transitions" / f"{t.work_item_id}.jsonl"
        with p.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(t)) + "\n")

    @staticmethod
    def _write_json(path: Path, data: dict):
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @staticmethod
    def _read_json(path: Path) -> dict:
        if not path.is_file():
            raise LineageError(f"no such record: {path.name}")
        return json.loads(path.read_text(encoding="utf-8"))


def _item_to_dict(item: WorkItem) -> dict:
    d = asdict(item)
    return d


def _item_from_dict(d: dict) -> WorkItem:
    d = dict(d)
    d["scope"] = Scope(**d["scope"])
    return WorkItem(**d)


def _looks_contained(boundary: str, ceiling: str) -> bool:
    """Placeholder containment check. 03-capability-authority-model.md: deciding
    containment is a natural-language judgment this store explicitly does not
    make -- it rejects a transition whose containment check did not pass; the
    check itself belongs to the invariant processor, not here.

    Until that processor exists, this is the seam: a caller can pass a
    pre-computed pass/fail as `ceiling=None` (skip) or wire a real checker in.
    Kept trivially permissive (always True unless ceiling is empty) so M8 does
    not silently pretend to enforce a check nothing has built yet.
    """
    return bool(ceiling)


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
