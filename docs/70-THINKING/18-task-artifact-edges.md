# Task ↔ artifact edges — a worked trace

*Nothing here is load-bearing. This is a concrete run followed end to end, kept
because tracing one is the only way found so far to see what the edge model is
missing. It contradicts the specification set in at least one place, deliberately:
where it does, the contradiction is the finding.*

> **Motto:** Follow one task all the way through and see what has no name.

## Why this exists

`10-technical/13` and `14` both describe relations between a task and the artifacts
around it, and neither says what such a relation *is*. Attempts to name the relation
categories abstractly produced two dead ends — semantic labels the system cannot
assign, and mechanical facts that are real but did not obviously add up to a model.

So: take one ordinary task, follow it from the operator's request to the last
artifact being deleted, and write down every point where something has no name.

## The setup

**Intent**, arriving out of band: *"Add a `--json` output format to the `report`
command."*

**Ceiling**, derived at task creation by the invariant processor: *the `report`
command's output path and its formatters, the tests covering that output, and the
CLI help text. Not the web API, not the storage layer.*

**Task T-88**, scope = the ceiling. No narrowing at the root.

## The walk

### Turn 0 — instantiation

Instance I-1, an implementer, binds its seven things (`10-technical/06`).

**The live set is not empty. The intent is already in it.**

This is the first correction the trace produced, and it undoes something the
specification set currently says — both `14` and `06` state that a new task's live
set starts empty. It does not. The operator's request has crossed into the work, and
a crossing is what registration records.

It also fits `10-foundations/03` without strain: a human's contribution enters as an
**observation** — the operator stated something, at a time, in a context — while what
that statement *carries* is a separate question. So the work record holds the
authoritative intent, write-once, and the knowledge model holds an Observation of it
having crossed. Content appearing in two stores is not duplication here, for the same
reason an Observation of a file is not a copy of the file: one is the source, the
other is the record of it entering the work.

**What this opens and does not settle.**

- **By what crossing type?** The four named are `read`, `generation`, `retrieval`,
  `effect_response`. Intent arrived by none of them — it arrived by *binding*. Either
  binding is a fifth type, or instantiation is modelled as the runtime reading the
  work record.
- **Does the objective follow, and the scope?** Both are bound at instantiation and
  both appear in the turn input, so by the same argument both crossed. Nothing here
  decides it. If they do, the turn-zero live set holds three artifacts and "the live
  set is empty at turn zero" was wrong in three ways rather than one.
- **Who registers a binding?** `14` says the context manager never initiates a
  crossing and only records what came back once something else did. Binding is not a
  call, so the runtime is the candidate.

### Turns 1–2 — orienting reads

`read("cli/report.py")`, then `read("cli/formats.py")`.

Each: scope check before the call, capability under the permissive read default,
gate, execution. The content crosses back. Registration writes an **Observation** to
the knowledge model and creates an **edge** from T-88 to it, carrying crossing type
`read` and originating invocation I-1.

Live set: intent + 2.

### Turn 3 — a retrieval

`search_kb("output format stability")` returns `c-4471`, a Decision recorded in some
earlier task: *output formats must stay stable across versions; adding a field is
fine, reordering is not.*

Registration writes **no content** — the claim already exists — and creates an edge
T-88 → c-4471 with crossing type `retrieval`.

This is the clean case separating the two things: **an edge is created, an artifact
is not.** Everything in the live set is an edge; only some edges brought an artifact
into existence.

### Turn 4 — the dead end, and the first real problem

`read("docs/api/web.md")`, reached while searching for the word "format".

**The scope check fires on every tool call, and scopes are written about what may be
changed.** The ceiling says "not the web API". Read naturally, that forbids modifying
it, not looking at it.

Two readings and the set picks neither:

- If the check applies the boundary to reads, it refuses an orientation read that no
  reasonable operator meant to forbid. Under the current disposition that is a
  rejection with a motivating message and the task loops — recoverable, but the
  system just spent a model call to block something harmless.
- If the check does not apply to reads, then **reads are unscoped**, and the
  read-then-carry composition is exactly what `10-technical/04`'s sequence evaluation
  exists to worry about.

The likely shape of an answer, not adopted here: a scope has two faces, what the work
may **reach** and what it may **change**, and only the second is what a derived
boundary naturally states. Nothing in the specification set distinguishes them.

### Turn 5 — a change

Write to `cli/formats.py`, adding a `JsonFormatter`. Effect type 1: scope check,
capability with `path_within`, gate, realized.

Something leaves for the first time. The **change set** gains an entry — an
**outbound** edge, held by the work record (`13`, `change_set`), composed from
observability's realized-effect history plus attribution.

So the task now has two edge sets with different owners: what came in (the live set,
context manager) and what went out (the change set, work record). Nothing in the set
says they are the same shape, and an artifact can be on both sides — `formats.py` was
read at turn 2 and written at turn 5.

### Turn 6 — the test run

Effect type 2. Output crosses back, registers as an Observation with crossing type
`effect_response`. One test fails.

### Turn 7 — the budget binds, and the policy does real work

Six entries and the turn budget starts to cut. This is the first turn where recall is
not trivially "everything".

Registration order — `07`'s degenerate policy — drops the oldest, which is
`report.py`: the most needed thing in the set. A policy with the available facts
could do better. Keep the retrieval, because it was deliberately fetched. Keep the
most recent `effect_response`, because it is the failure being worked on. Keep the
file being modified.

**Except that "the file being modified" is not a fact the live set holds.** It is in
the change set, at the work record. So a good inbound decision needs the outbound
edges, and the two sets are not independent from the policy's point of view. This is
the second real problem the trace found.

### Turn 8 — resolution

Fix, tests pass, result `answered`. I-1 ends.

**The live set survives**, because it belongs to T-88 and not to the instance. A
second instance under T-88 would find it populated.

### Attachment — and who does it

Two things were worth singling out: `c-4471`, which governed the work and will govern
future work on formatters, and the finding produced here — *the formatter interface
assumes line-oriented output; JSON needs a whole-document hook.*

Attachment is a tool call proposing a type-4 effect, gated like any other, carrying
the claim, the task, and a **reason** in natural language. The reason is what makes
the attachment contestable: without it, a curated edge and an arbitrary one are
indistinguishable afterwards.

**The trace argues against the implementer doing it.** Attaching *before* the work is
predicting relevance; attaching *after* is reporting it. At turn 3 the implementer
could not have known `c-4471` would matter, and at turn 8 its attention belongs to
the result. Both attachments were only obvious in retrospect. A planner predicts, a
reviewer reports, and the doer is badly placed for either — which is the shape of the
M5 follow-up result that a 7B does the doing and not the judging.

Unresolved: whether attachment is a distinct act or falls out of something an
orchestrator does anyway when it formulates the next task.

### T-88 ends

The live set ends with the task, which is the deletion trigger. For each artifact:
promoted, or held by another live task?

| Artifact | Outcome |
|---|---|
| Observations of `report.py`, `formats.py`, `web.md`, the test output | Not promoted, no other task. Deleted |
| `c-4471` | A promoted claim from another task. **Survives — what dies is the edge T-88 → c-4471, not the claim** |
| The finding | Survives if the attachment promoted it. Otherwise deleted, and the edge dangles |
| The intent Observation | Roots of any surviving finding stay raw, so reachability protects it. The authoritative intent is in the work record regardless |

**The inverse index is required here, and not in theory.** Deciding whether another
live task holds the `report.py` Observation means going from an artifact to its
tasks. The live set answers task → artifacts and nothing answers the other direction.
This question is asked once per artifact at every task end.

## What the trace found

1. **The live set is not empty at turn zero** — the intent is in it. Contradicts
   `14` and `06` as written. Open: the crossing type, whether objective and scope
   follow, and who registers a binding.
2. **Reads are scope-checked against a boundary written about changes.** Reach and
   change are not distinguished anywhere, and both readings of the current rule are
   bad.
3. **The recall policy needs the outbound edges.** Inbound and outbound edge sets
   have different owners and the policy needs both.
4. **The inverse index is a precondition of the deletion rule**, demonstrated rather
   than supposed.
5. **An edge is not an artifact**, shown cleanly by the retrieval: an edge created,
   no artifact created, and at task end the edge dies while the claim lives.
6. **Attachment wants to happen after the work**, not during it, and probably not by
   the doer.

## What the trace does not settle

The original question. **What are the possible relations between a task and the
artifacts around it?** The walk produced mechanical facts — crossing type,
originating invocation, inbound versus outbound — and one declared relation, the
curated attachment with its reason. It did not produce a vocabulary, and it is not
yet clear whether one is needed or whether the mechanical facts plus a free-text
reason are the whole of it.

Two dead ends worth not repeating. **Semantic categories the system assigns
itself** — subject, instrument, governing — fail because they presume what the work
will do, which is decided live from the scope and the file contents. **Mechanical
facts already carried elsewhere** — the originating task, the claim type, the
promoted flag — should not be copied onto the edge, because a second place to hold
them is a second place to go stale.

## Next passes

- Run a task whose interesting structure is *not* a boundary, to test whether the
  findings above are general. *"Tests pass locally and fail in CI"* is the candidate:
  instrument-heavy, exploration-heavy, and the subject is not known at the start —
  finding it is the work.
- Run a task that **splits**, to exercise inheritance. Both mechanisms are to be
  supported — explicit inheritance duplicating **edges** and not artifacts, or no
  inheritance — and nothing has traced either.
- Run a task that is **refused** on scope, to see what a rejection leaves behind.
