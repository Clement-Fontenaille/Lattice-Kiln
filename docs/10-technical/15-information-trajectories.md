# Information Trajectories (v0)

**Traces to:** nothing of its own. This document composes
`10-technical/01`–`14` and adds no claim not already in one of them.

## TL;DR

Four walks through the system, following one piece of information each from the
moment it is produced to the moment it is forgotten, naming the document that owns
every step.

Its value is not the walks. It is **what the walks cannot complete**: a step no
document answers is a gap in that document, and four traces found seven.

> **Motto:** Follow one thing all the way down, and the seams show.

## Status of this document

**Derived and diagnostic.** It is normative nowhere. Every step cites the document
that owns it, and where no document owns a step, that is recorded as a gap rather
than filled here.

That discipline is the whole method. A trajectory document that invents the missing
step stops being a check on the set and becomes another thing to keep consistent
with it.

## Responsibility

Compose, and do not extend. Walk a piece of information across actor boundaries,
which is the one thing no single specification can do — each is written from its own
actor's point of view, and a gap that lives exactly between two of them is invisible
from either.

## Trajectory A — a file read, never remembered

The commonest path in the system, and the one most of what crosses actually takes.

| # | Step | Owner |
|---|---|---|
| 1 | An instance calls a read tool. It is one of the two things that cross from reasoning to runtime | `09` |
| 2 | **Capability**: passes under the permissive default, since no rule names this class of read | `03`, Reads |
| 3 | **Gate**: the read is in the input domain and passes, since no clause fires | `04`, `01` |
| 4 | The runtime performs it | `09`, `20-arch-runtime` |
| 5 | The result crosses back as an operation outcome | `09` |
| 6 | **Registered**: the content is written to the knowledge model as an Observation, on the bookkeeping path — unproposed, ungated | `12`, Write |
| 7 | The live set gains a **reference plus metadata**: crossing type `read`, registered_at. No content | `14`, Register |
| 8 | **Recorded** as a kind-2 realized-operation record, sharing the kind with typed effects so the gate reads one ordered history | `02` |
| 9 | **Recalled** into turn inputs while the policy selects it. Each appearance is a kind-5 record carrying its crossing type | `14`, `02` |
| 10 | Not recalled after a cache reset. It **leaves the live set** — which is not monotonic | `14` |
| 11 | Nothing proposed it as evidence and no claim cites it, so it is **not reachable** from any promoted claim | `12`, Elide |
| 12 | The sweep elides it from the knowledge model | `12` |
| 13 | It remains reconstructable in observability, and nowhere else | `02` |

**Where the walk stops.** Step 12 has no trigger. Nothing in the set says **when
the sweep runs** — per turn, at an instance's end, on a size threshold, never until
something asks. Step 10 has no terminator either: an instance ends, and whether its
live set ends with it is unstated.

## Trajectory B — a test failure that becomes a finding

The promotion path. Rare by design: most of what crosses takes trajectory A.

| # | Step | Owner |
|---|---|---|
| 1 | An instance proposes process execution, effect type 2 | `01` |
| 2 | **Capability**: the command is matched against the role's allowlist | `03` |
| 3 | **Gate**: H7's destructive-command denylist, among others | `04`, `05` |
| 4 | The runtime realizes it; kind-2 record | `02` |
| 5 | The output crosses back, registers as an Observation, and the live set gains a reference | `14`, `12` |
| 6 | A **thinking** processor forms an attempted argument over it, checks it, and proposes a Finding | `22-arch-cognition/04`, `12` |
| 7 | That proposal is a **type-5 memory mutation** — capability, then gate, like any effect | `01`, `03`, `04` |
| 8 | Written to the knowledge model with parent edges, each carrying **its own** mode of acquisition | `12` |
| 9 | Recorded as a kind-6 knowledge-state transition: claim, kind of change, grounds, as fields | `02` |
| 10 | Attached to a work item — a reference plus edge metadata, itself a type-4 mutation | `13` |
| 11 | Once its validity has been checked, its working is **compressed to a souvenir**; the Observation from step 5 is a root and stays raw | `12`, Compress |
| 12 | The Observation is now reachable, so the sweep MUST refuse to elide it | `12`, Elide |
| 13 | It persists — for how long, and until what, is not stated | — |

**Where the walk stops.** Step 11 has no scheduler: nothing says when validity is
checked or by what. `10-foundations/03` is explicit that a claim is checked when it
is **used** rather than by audit, which is an answer about the mechanism and not
about who runs it. And step 13 falls off the end: beyond reachability, the knowledge
model has no retention rule at all.

## Trajectory C — a declared scope

The mandate path. Nothing on it is built.

| # | Step | Owner |
|---|---|---|
| 1 | Intent arrives from outside, written once, never rewritten by the system | `13`, Intent |
| 2 | An **invariant processor** derives the ceiling from intent | `03`, Who may write a scope |
| 3 | Recorded on the work item as three fields: boundary, derivation, state `derived` | `13` |
| 4 | Made visible to the operator, so a wrong derivation is contested rather than ratified | `03` |
| 5 | The orchestrator formulates a child item and **narrows**; containment is checked; the transition is logged | `03`, `13` |
| 6 | Bound at instantiation into an instance, and **static for its life** | `06` |
| 7 | Recorded verbatim in the kind-1 invocation record, **as bound** — because the item's scope may move underneath it | `02` |
| 8 | The instance ends. The bound scope ends with it; only the kind-1 record survives | `06`, `02` |
| 9 | The item is refined; the scope is re-derived; the change appears in the transition log | `13` |
| 10 | At task end, the **aggregate check** compares the accumulated change set against the declaration | `03` |
| 11 | The item reaches a terminal transition. Its scope's lifetime is its item's | `13` |
| 12 | Whether a terminal item is retained or removed is open | `13`, open contract |

**Where the walk stops.** Step 2 has no trigger — the runtime holds hardcoded
invariant-layer call sites, and none of them is named as "derive a root item's
ceiling". Step 4 has no channel: `08`'s two-mode handoff belongs to the
orchestrator, and the orchestrator is not who derived this.

## Trajectory D — an effect that is refused

The negative path, and the one whose records matter most, since nothing else
survives a refusal.

| # | Step | Owner |
|---|---|---|
| 1 | An instance proposes a type-1 workspace mutation | `01` |
| 2 | **Representability**: if the target is outside the assigned workspace, the runtime rejects it *before the gate is consulted* | `04`, `09` |
| 3 | Otherwise **capability**: no matching grant, or a constraint violated → `reject_by_capability` with a machine-readable reason | `03` |
| 4 | Recorded as a kind-4 disposition. **Never** as a safety intervention — a capability rejection is ordinary policy | `02`, `03` |
| 5 | Had the gate refused instead, the disposition would link to a kind-3 safety-intervention record carrying `retry_eligible: false` | `02`, `04` |
| 6 | The typed refusal crosses back to the instance | `09` |
| 7 | That crossing **registers like any other**: the instance was told something, so an Observation is written and the live set gains a reference | `14` |
| 8 | So a refusal leaves two records with different purposes — the decision, in observability; what the instance saw, in the knowledge model | `02`, `12` |
| 9 | Repeated rephrased proposals after a refusal are **boundary probing**, visible in the kind-4 history and read by `check_sequence` | `02`, `04` |
| 10 | The Observation of the refusal is swept like any other, unless something built on it | `12` |

**Where the walk stops.** Step 2 produces no record. Kind 4 exists for every
operation proposed by a cognitive component, and its dispositions are
`realized` / `rejected-by-capability` / `rejected-by-gate` /
`rejected-by-containment`. **There is no disposition for a non-representable
operation**, so the one rejection that happens earliest is the one the record cannot
express.

## What the tracing found

Seven gaps, none of which is visible from inside the document that owns the step.
They are listed here and belong in those documents; this one does not fix them.

1. **The sweep has no trigger** (`12`). Per turn, at an instance's end, on a size
   threshold, on demand — nothing chooses. Trajectory A cannot be completed without
   one, and A is the path most information takes.
2. **Nothing says what ends a live set** (`14`). It is described as an index over a
   run while `live_set_id` binds per instance. Whether an instance's live set dies
   with it, and what happens to its entries if it does, is unstated.
3. **The sweep's root set names only promoted claims** (`12`), while **three stores
   hold references into the claim store**: the work record's attachment edges, the
   live set, and observability. None of the three is named as a reachability root.
   Taken literally, a finding attached to a work item and cited by nothing else is
   swept, leaving the work record holding a dangling reference — and `13`'s failure
   modes do not list that one. This is the sharpest of the seven.
4. **"Promoted" is undefined** (`12`). It carries the root set and therefore the
   whole retention rule, and no document says what promotes a claim.
5. **No disposition for a non-representable operation** (`02`). The earliest
   rejection in the pipeline is the one kind 4 cannot express.
6. **Nothing triggers deriving a root item's ceiling** (`03`). The runtime holds
   hardcoded invariant-layer call sites; this is not one of them.
7. **No channel shows a derived scope to the operator** (`03`). Recording it with
   its derivation is normative, and being *visible* is what makes it contestable —
   but `08`'s two-mode handoff belongs to the orchestrator, which is not who derived
   it.

## Relationships

Every specification in this set, as a consumer of none of them. If a document
changes, this one is re-walked rather than edited around: a trace that is patched to
stay plausible has stopped being a check.

## Open contracts

- **Which trajectories are worth keeping.** Four were walked because they take
  different paths — the default, the promotion, the mandate, the negative. A turn
  input, an operator statement, and a decommission are candidates and are not
  walked.
- **Whether this should be executable.** Every step names an owning document and a
  record kind, which is most of what a conformance test needs. A harness that
  replays a real run and asserts each step produced its record would turn this from
  a reading into a check.
