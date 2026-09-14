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
| 10 | Passed over by the recall policy on later turns. It **stays in the live set**: not shown is not the same as not held | `14` |
| 11 | **The task ends.** Its live set ends with it, and this artifact stops being a root | `14`, `12` |
| 12 | Nothing promoted it and no other live task holds it, so it is deleted, along with any ancestor no remaining root still reaches | `12` |
| 13 | It remains reconstructable in observability, and nowhere else | `02` |

**The walk now completes.** A live set belongs to a task, so what ends it is the
task ending, and that is the deletion trigger. The one thing left unspecified on this
path is whether an artifact can be **detached early** — recognised as noise, or
superseded — which would be a second trigger nothing describes.

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
| 12 | The Observation is reachable from a promoted claim, so deletion MUST refuse it when the task ends | `12`, Elide |
| 13 | It persists — for how long, and until what, is not stated | — |

**Where the walk stops.** Step 11 has no scheduler and no mechanism: nothing says
when validity is checked or by what, and compression itself likely needs a step that
analyses the argument and labels its stages rather than dropping a reasoning artifact
(`12-knowledge-model.md`). `10-foundations/03` is explicit that a claim is checked when it
is **used** rather than by audit, which is an answer about the mechanism and not
about who runs it. And step 13 falls off the end: beyond reachability, the knowledge
model has no retention rule at all.

## Trajectory C — a declared scope

The mandate path. Nothing on it is built.

| # | Step | Owner |
|---|---|---|
| 1 | Intent arrives from outside, written once, never rewritten by the system | `13`, Intent |
| 2 | The task is created, which **calls the invariant processor** to derive its ceiling from intent. Creation is the trigger, so every task has a ceiling | `03`, `13` |
| 3 | Recorded on the work item as three fields: boundary, derivation, state `derived` | `13` |
| 4 | **Carried into the instructions**, which is how the operator sees it. No separate channel, and the kind-1 record holds it verbatim | `03`, `02` |
| 5 | The processor issuing an invocation writes that invocation's scope, **narrowing** within the task's ceiling; containment is checked | `03`, `13` |
| 6 | Bound at instantiation into an instance, and **static for its life** | `06` |
| 7 | Recorded verbatim in the kind-1 invocation record, **as bound** — because the item's scope may move underneath it | `02` |
| 8 | The instance ends. The bound scope ends with it; only the kind-1 record survives | `06`, `02` |
| 9 | Work is redefined: a **successor task** is created with a new objective and its own derived scope. T-88 is untouched | `13`, `01` |
| 10 | At task end, the **aggregate check** compares the accumulated change set against the declaration | `03` |
| 11 | The item reaches a terminal transition. Its scope's lifetime is its item's | `13` |
| 12 | Whether a terminal item is retained or removed is open | `13`, open contract |

**Where the walk stops.** It no longer stops on the way down — steps 2 and 4 both
had holes and both are filled. It stops at the end: step 12, whether a terminal work
item is retained or removed, which decides how long a scope outlives the work it
bounded.

One step is worth reading twice. Step 8 and step 9 are what make the chain honest: an
instance's scope dies with the instance while the item's scope can move afterwards,
so an instance that wants more mandate has to stop and be replaced rather than grow.

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

Seven gaps, none visible from inside the document that owns the step. **Five are now
answered and one was fixed outright**, which is what the exercise was for. What
follows is the current state rather than the original list.

**Answered.**

1. **The root set** is promoted artifacts plus the live set, and **promotion is
   inscription in that set** — an act, not a property a claim type confers. That
   settles what had been two separate gaps.
2. **There is no sweep to trigger.** Reachability only changes at moments the system
   already knows about, so removal runs incrementally when an item leaves the live
   set: walk up its provenance and delete each ancestor no remaining root reaches.
   The question of when a periodic pass runs disappeared with the pass.
3. **A task's ceiling is derived at task creation**, by a call to the invariant
   processor. Every task has one by construction, because a task that exists was
   created.
4. **A derived scope reaches the operator inside the instructions.** No separate
   channel, and it cannot be forgotten, since the instructions are recorded verbatim
   in the kind-1 record.

**Fixed rather than filed.** Kind 4 gained `rejected-as-non-representable`. The
earliest rejection in the pipeline — before capability, before the gate — produced
no record at all, so a component repeatedly proposing writes outside its workspace
was invisible.

**Still open.**

5. **Whether an artifact can be detached from a live task** (`14`). The live set
   only grows within a task's life as specified, and a task ending is the single
   deletion trigger. Early detachment would be a second one, and nothing describes
   it.

**New, surfaced by the answers.**

6. **The live set and the work record's attachments may be one relation** (`12`,
   `13`, `14`). Both run from a task to a claim, with different fields, held by two
   actors. Attaching does not confer survival — an unpromoted artifact goes when its
   task ends whether or not something attached it deliberately, and what must outlive a
   task is promoted — so the two differ in what they record rather than in what they
   mean.

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
