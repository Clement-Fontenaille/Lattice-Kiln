"""Work package 2: the knowledge model store.

Specification: docs/10-technical/12-knowledge-model.md

Six operations over a DAG of claims: Write, Read, Query, Traverse dependents,
Compress, Elide. Records what it is given; judges neither the claim nor the
question (pertinence is judged live by whoever is asking, never precomputed here).

Two write paths, gated differently:
  Observation  bookkeeping. Every crossing lands here immediately, ungated.
  Above it     a proposal. Evidence/Finding/Decision arrive as type-5 effects.

This module does not itself gate -- the caller has already passed capability and
the gate. What it enforces: the Observation path may never write a claim ABOVE
Observation; content is immutable once written (a correction is a new entry plus
an edge, never an edit); Elide refuses a reachable root; Compress refuses an
unchecked step or a root.
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

# Claim types. 12-knowledge-model.md, The claim record.
OBSERVATION = "observation"
EVIDENCE = "evidence"
FINDING = "finding"
DECISION = "decision"
CLAIM_TYPES = {OBSERVATION, EVIDENCE, FINDING, DECISION}

# Mode of acquisition, carried on the EDGE (parent link), not the claim. F6:
# assessed per link of a provenance chain, not once per claim.
READ = "read"
REASONED = "reasoned"
TESTED = "tested"
OPERATED = "operated"
MODES = {READ, REASONED, TESTED, OPERATED}


class KnowledgeError(Exception):
    """Refusals this store makes on its own authority: eliding a reachable root,
    compressing a root or an unchecked step, or the bookkeeping path attempting
    to write above Observation.
    """


@dataclass
class ParentEdge:
    claim_id: str
    mode: str                 # read | reasoned | tested | operated
    second_hand: bool = False  # only meaningful for `read`


@dataclass
class Claim:
    claim_id: str
    type: str
    content: dict              # structured, never a single unparsed paragraph
    source: str                 # who produced it -- an axis, not a fifth type
    parents: list               # list[ParentEdge]
    scope: Optional[str] = None
    tags: list = field(default_factory=list)
    checked: bool = False       # whether validity has checked this step (for Compress)
    created_at: str = ""        # 03-evidence-belief-and-provenance.md, Scope: "has to
                                 # be assessed near its own creation" -- unenforceable
                                 # and unauditable without a timestamp to measure
                                 # "near" against. Added when this gap surfaced while
                                 # building M9's scope-assessment seam; every existing
                                 # write path sets it (none relied on the old default).


class KnowledgeStore:
    """The naive filesystem default.

    knowledge/
      claims/<claim_id>.json
      children/<claim_id>.jsonl     # child links, appended on every write

    `children/` is redundant with `parents[]` and kept anyway -- Traverse
    dependents is first-class, and deriving it by scanning every claim would
    make the walk quadratic from day one.
    """

    def __init__(self, root: Path | str):
        self.root = Path(root)
        (self.root / "claims").mkdir(parents=True, exist_ok=True)
        (self.root / "children").mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------- write

    def write_observation(self, content: dict, *, source: str,
                          parents: Optional[list[ParentEdge]] = None,
                          scope: Optional[str] = None,
                          tags: Optional[list] = None) -> Claim:
        """Bookkeeping. Ungated, unproposed -- every crossing the context manager
        registers lands here immediately (12-knowledge-model.md, Write).
        """
        return self._write(OBSERVATION, content, source=source,
                           parents=parents, scope=scope, tags=tags, checked=False)

    def propose_claim(self, type_: str, content: dict, *, source: str,
                      parents: list[ParentEdge], scope: Optional[str] = None,
                      tags: Optional[list] = None, checked: bool = False) -> Claim:
        """A type-5 memory mutation. Evidence, Finding, Decision, a qualification,
        a requalification. The caller is assumed to already be a gated, realized
        effect -- this store enforces only that the type is above Observation and
        that it never arrives via the bookkeeping path (that's write_observation).
        """
        if type_ not in (EVIDENCE, FINDING, DECISION):
            raise KnowledgeError(
                f"propose_claim is for Evidence/Finding/Decision, not {type_!r} "
                "-- Observations use write_observation (the bookkeeping path)")
        return self._write(type_, content, source=source, parents=parents,
                           scope=scope, tags=tags, checked=checked)

    def qualify(self, claim_id: str, qualification: dict, *, source: str) -> Claim:
        """A correction. NEVER an edit -- a new entry plus an edge to the one it
        qualifies (12-knowledge-model.md, Write: "No write revises an existing
        entry"). The original stands alongside it.
        """
        old = self.read(claim_id)
        return self.propose_claim(
            DECISION, {"qualifies": claim_id, **qualification}, source=source,
            parents=[ParentEdge(claim_id=claim_id, mode=REASONED)],
            scope=old.scope, checked=True)

    def compress(self, claim_id: str, souvenir_content: dict, *,
                source: str) -> Claim:
        """Produce a souvenir for a CHECKED claim; the working it replaces is
        deleted, not overwritten -- this creates rather than rewrites
        (12-knowledge-model.md, Compress).

        Refuses a root (nothing regenerates an observation never kept) and an
        unchecked step (would preserve a conclusion whose support was never
        verified). Splitting a generation into reasoning+conclusion does NOT
        make either half compressible on its own -- that distinction belongs to
        the caller deciding what `souvenir_content` names; this store only
        enforces the checked/root precondition.
        """
        claim = self.read(claim_id)
        if not claim.checked:
            raise KnowledgeError(f"{claim_id} is not checked; compressing an "
                                 "unchecked step preserves an unverified conclusion")
        if not claim.parents:
            raise KnowledgeError(f"{claim_id} is a root; roots MUST NOT be "
                                 "compressed (nothing regenerates a kept observation)")
        souvenir = self.propose_claim(
            claim.type, souvenir_content, source=source,
            parents=[ParentEdge(claim_id=p.claim_id, mode=p.mode) for p in claim.parents],
            scope=claim.scope, checked=True)
        self._delete_working(claim_id)
        return souvenir

    def promote(self, claim_id: str, *, source: str) -> None:
        """5b Relate. Inscription in the root set -- an act, not a property
        (12-knowledge-model.md, The root set, and what promotion is).
        """
        self.read(claim_id)  # raises if it doesn't exist
        promoted = self._promoted_ids()
        promoted.add(claim_id)
        self._write_promoted(promoted)

    # -------------------------------------------------------------- reads

    def read(self, claim_id: str) -> Claim:
        d = self._read_json(self._claim_path(claim_id))
        return _claim_from_dict(d)

    def query(self, *, term: str = "", tags: Optional[list] = None,
             breadth: int = 20, depth: int = 0,
             matching_mode: str = "literal") -> list[Claim]:
        """Deterministic matching over content+tags (12-knowledge-model.md,
        Narrowing: term matching, edit-distance/token-overlap for fuzzy).

        breadth/depth/matching_mode are exposed on every call whether or not
        this naive implementation uses all of them, per the spec's own
        requirement that the parameter surface not foreclose measurements a
        richer policy would need. `depth` beyond 0 (walk N hops) is NOT
        implemented in this naive pass -- open contract carried forward.
        """
        out = []
        for p in sorted((self.root / "claims").glob("*.json")):
            d = self._read_json(p)
            blob = json.dumps(d.get("content", {})) + " " + " ".join(d.get("tags", []))
            hit = False
            if term:
                hit = (term.lower() in blob.lower() if matching_mode == "literal"
                      else _fuzzy_hit(term, blob))
            elif tags:
                hit = bool(set(tags) & set(d.get("tags", [])))
            else:
                hit = True
            if hit:
                out.append(_claim_from_dict(d))
            if len(out) >= breadth:
                break
        return out

    def traverse_dependents(self, claim_id: str) -> list[Claim]:
        """What cites this claim -- the direction opposite a provenance lookup.
        Satisfied by the children/ index, which every write appends to.
        """
        p = self.root / "children" / f"{claim_id}.jsonl"
        if not p.is_file():
            return []
        ids = [json.loads(line)["child"] for line in
              p.read_text(encoding="utf-8").splitlines() if line.strip()]
        return [self.read(i) for i in ids]

    # -------------------------------------------------------------- elide

    def elide(self, claim_id: str) -> None:
        """Not proposed by anyone -- runtime bookkeeping, not a type-5 effect
        (12-knowledge-model.md, Elide). Refuses a reachable root.
        """
        if self._is_reachable_root(claim_id):
            raise KnowledgeError(
                f"refusing to elide {claim_id}: it is reachable from a root "
                "(a promoted claim, or a live task's attachment)")
        self._delete_working(claim_id)

    def sweep_from(self, departing_claim_ids: list[str], *,
                   still_live: set[str], promoted: Optional[set[str]] = None) -> list[str]:
        """Incremental removal triggered by a task ending
        (12-knowledge-model.md, Removal is incremental). NOT a periodic pass --
        this walks up from the departing items only.

        `still_live` is every claim_id still reachable from some OTHER live
        task or promotion; the caller (wiring.py) computes that from the work
        record and context manager, since this store cannot see either on its
        own (12-knowledge-model.md, Authority: "nothing in the permission or
        invariant layers depends on this store" -- and by the same logic it
        does not reach into the other two stores to decide liveness itself).
        """
        promoted = promoted or self._promoted_ids()
        deleted = []
        frontier = list(departing_claim_ids)
        seen = set()
        while frontier:
            cid = frontier.pop()
            if cid in seen or cid in still_live or cid in promoted:
                continue
            seen.add(cid)
            if not self._claim_path(cid).is_file():
                continue
            claim = self.read(cid)
            deleted.append(cid)
            self._delete_working(cid)
            frontier.extend(p.claim_id for p in claim.parents)
        return deleted

    def _is_reachable_root(self, claim_id: str) -> bool:
        return claim_id in self._promoted_ids()

    # ------------------------------------------------------------- internals

    def _write(self, type_: str, content: dict, *, source: str,
              parents: Optional[list[ParentEdge]], scope: Optional[str],
              tags: Optional[list], checked: bool) -> Claim:
        if not isinstance(content, dict):
            raise KnowledgeError("content MUST be structured, not a bare string "
                                 "(12-knowledge-model.md: excludes a single "
                                 "unparsed paragraph)")
        claim = Claim(claim_id=f"cl_{uuid.uuid4().hex[:12]}", type=type_,
                     content=content, source=source, parents=parents or [],
                     scope=scope, tags=tags or [], checked=checked,
                     created_at=_now())
        self._write_json(self._claim_path(claim.claim_id), _claim_to_dict(claim))
        for edge in claim.parents:
            self._append_child(edge.claim_id, claim.claim_id)
        return claim

    def _delete_working(self, claim_id: str):
        p = self._claim_path(claim_id)
        if p.is_file():
            p.unlink()

    def _claim_path(self, claim_id: str) -> Path:
        return self.root / "claims" / f"{claim_id}.json"

    def _append_child(self, parent_id: str, child_id: str):
        p = self.root / "children" / f"{parent_id}.jsonl"
        with p.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"child": child_id}) + "\n")

    def _promoted_path(self) -> Path:
        return self.root / "promoted.json"

    def _promoted_ids(self) -> set:
        p = self._promoted_path()
        if not p.is_file():
            return set()
        return set(json.loads(p.read_text(encoding="utf-8")))

    def _write_promoted(self, ids: set):
        self._promoted_path().write_text(json.dumps(sorted(ids)), encoding="utf-8")

    @staticmethod
    def _write_json(path: Path, data: dict):
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @staticmethod
    def _read_json(path: Path) -> dict:
        if not path.is_file():
            raise KnowledgeError(f"no such claim: {path.name}")
        return json.loads(path.read_text(encoding="utf-8"))


def _claim_to_dict(c: Claim) -> dict:
    d = asdict(c)
    return d


def _claim_from_dict(d: dict) -> Claim:
    d = dict(d)
    d["parents"] = [ParentEdge(**p) for p in d.get("parents", [])]
    return Claim(**d)


def _fuzzy_hit(term: str, blob: str) -> bool:
    """Token-overlap fuzzy match. Deliberately crude (12-knowledge-model.md,
    Narrowing: deterministic matching, not embeddings)."""
    t = set(term.lower().split())
    b = set(blob.lower().split())
    return bool(t) and len(t & b) / len(t) >= 0.5


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
