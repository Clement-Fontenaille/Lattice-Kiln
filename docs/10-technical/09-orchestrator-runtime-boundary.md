# Orchestrator / Runtime Boundary (v0)

**Traces to:** `00-design/10-foundations/02-reasoning-vs-runtime.md`,
`00-design/20-arch-runtime.md`,
`00-design/22-arch-cognition/03-orchestrator.md`,
`00-design/90-notes/01-next-conceptual-pass.md`,
`00-design/40-roadmap/01-MILESTONES/completed/05-intelligent-orchestration.md` (M5);
binds to `10-technical/06-processor-contract.md`,
`10-technical/08-orchestrator-contract.md`,
`10-technical/01-effect-vocabulary.md`,
`10-technical/04-enforcement-gate.md`.

## TL;DR

Two kinds of thing cross from the reasoning side (orchestrator + processors) to
the runtime: a **proposed effect** and a **read request**. Three cross back: the
**outcome** of either, a **turn input**, and an **objective signal** where one
exists. Nothing else. The runtime validates the four properties plus the deny-list
gate and makes **no semantic judgment** about the work.

> **Motto:** The model proposes; the runtime makes it real — and checks only what it can check without understanding.

## Status of this document

v0 for Milestone 5. It narrows the "how much does the runtime validate?" open
question (`02-reasoning-vs-runtime.md`, `20-arch-runtime.md`) to a concrete MVP
answer, and fixes the crossings and the assumptions each side may not make. The
placement of the gate relative to the runtime stays open
(`01-invariant-enforcement.md`); the call *order* is pinned here.

## Narrowing

`90-notes/01-next-conceptual-pass.md` flags "the exact orchestrator/runtime
boundary" as the highest-value seam to narrow before specifying machinery. This
document does that narrowing. Discarded alternatives are named under each
crossing and under Validation depth.

## The crossings

### Reasoning → runtime

| Crossing | Payload | Not allowed |
|---|---|---|
| **Proposed effect** | typed `1..9`, with its four-property envelope (`01-effect-vocabulary.md`). A processor-invocation request is one of these — type 6 — carrying role, objective, scope, live-set identity, capability set and interaction mode (`06`) | calling a runtime internal; reading raw runtime state; instructing the runtime to skip or reorder a check; requesting a capability or a scope the caller does not hold; binding a processor outside the role library without recording the definition |
| **Read request** | a runtime-mediated read — a file, a process output, a knowledge-model query. Not typed, no effect envelope | assuming it passes because reads usually do; issuing one outside the caller's assigned workspace or allowlist |

**Two rather than three, and not the two previously listed.** A processor
invocation is not a separate kind of crossing: it is effect type 6, and listing it
beside "proposed effect" double-counts. What was genuinely missing is the read. A
read is a runtime-mediated operation, it sits in the gate's input domain
(`04-enforcement-gate.md`), and it is by far the most frequent thing the reasoning
side sends across — a boundary specification that does not mention it describes a
system that cannot look at anything.

### Runtime → reasoning

| Crossing | Payload | Not allowed |
|---|---|---|
| **Operation outcome** | what a proposed effect or a read returned, or the typed refusal (`rejected_by_capability` / `rejected_by_gate` → kind-3) | leaking another run's data; exposing the gate's internal rule set; returning a read result without registering the crossing (`14-context-manager.md`) |
| **Turn input** | what the model is actually shown this turn, composed by `14-context-manager.md` out of the live set | presenting it as complete when recall dropped or truncated entries (the recall trace MUST say so); flattening crossing type, so a generation reads as authored material |
| **Objective signal** | build / test / lint outcome where the runtime can produce one | fabricating a signal where none exists; treating absence of a signal as success |

**The turn input is not requested.** It is the one crossing with no counterpart on
the other side of the table: nothing on the reasoning side asks for it, because
composition happens as a turn happens. The removed `context_bundle` was a
request/response object, which is why it appeared here as a symmetric crossing and
why its replacement does not.

## Validation depth (the narrowed open question)

For the MVP the runtime checks, and only checks:

1. **Representable** — the effect is expressible in the runtime's model of the
   world (e.g. the path is inside the assigned workspace). Non-representable
   effects are **rejected before the gate**, not gated.
2. **Permitted** — the proposing actor holds the capability
   (`03-capability-authority-model.md`).
3. **Attributable** — the effect is tied to a specific invocation.
4. **Reversible where required** — an undo path exists (VCS for a file write,
   etc.).
5. **The deny-list gate** — `04-enforcement-gate.md`.

A **read** takes the same path with two of the five doing nothing: it has no
reversibility requirement and no effect type, but it is representable or it is
not, it is attributable, it is capability-checked — under a permissive default —
and it reaches the gate. It passes unless a rule names it; the point is that there
is a place for such a rule to fire.

The runtime makes **no semantic judgment**: it does not read a diff to decide
whether the change is *good*, does not run a type-checker or linter before
realizing a write, does not assess whether a test is meaningful. "Is this the
right change?" is a cognitive question answered by a reviewer processor, never by
the runtime.

Discarded: a runtime that semantically validates before realizing (lint,
type-check, spec-conformance). It recreates the rigid workflow engine
`02-reasoning-vs-runtime.md` exists to prevent, and it puts a persuadable-by
-construction judgment in the one place that must stay mechanical.

## Call order (pinned; placement still open)

Every effect that reaches the runtime is processed in this order, and the runtime
**cannot be instructed to reorder or skip a step**:

```
representability pre-check  ->  capability  ->  invariant gate  ->  realize
        (runtime)              (policy)          (floor)          (runtime)
```

Whether the gate is a component *of* the runtime or a layer the runtime is
subordinate *to* is left open (`01-invariant-enforcement.md`). What is fixed:
there is no runtime code path to an effect realization that bypasses the gate.

## What each side may not assume

**Reasoning MUST NOT assume:**

- a proposed effect will be realized — it may be refused;
- a read will be permitted — the default is permissive, not guaranteed;
- its turn input is complete — recall may have dropped or truncated entries, and
  the live set itself holds only what has actually crossed;
- what it saw last turn is still in front of it — the live set is not monotonic;
- a spawned processor will run or succeed.

**Runtime MUST NOT assume:**

- a proposed effect is safe because a capable actor proposed it — it still gates;
- it should interpret the work's purpose to decide how hard to validate — depth
  is fixed at the four properties + gate, regardless of what the work "means".

## Failure modes

- **Boundary bypass.** A reasoning-side code path that reaches a runtime internal
  without going through a proposed effect. A conformance failure even if nothing
  harmful happens through it.
- **Semantic creep.** The runtime begins making cognitive judgments ("this test
  is weak", "this refactor is unnecessary") to decide whether to realize. Defect
  — that is a reviewer's job.
- **Assumed realization.** Reasoning proceeds as though an effect happened without
  checking the result or refusal.
- **Turn input assumed complete.** Covered by `07` and `14`; restated here as a
  boundary assumption the reasoning side must not make.
- **An unregistered read result.** A read that crosses back without
  `14-context-manager.md` registering it leaves material in front of the model
  that the live set does not know about — which breaks the live-state query, the
  R4 ceiling, and the sequence history the gate will eventually read.
- **Signal fabrication.** The runtime reports an objective signal it did not
  actually obtain, or treats "no signal" as "pass".

## Relationships

- **Reasoning and runtime boundary** (`02-reasoning-vs-runtime.md`) — the concept;
  this document is its interface narrowing.
- **Runtime** (`20-arch-runtime.md`) — owns representability and reversibility
  judgments and effect realization; this document says what it may not also do.
- **Orchestrator contract** (`08`) / **processor contract** (`06`) — the reasoning
  side of the boundary.
- **Enforcement gate** (`04`) / **effect vocabulary** (`01`) — the checks and the
  effect-type domain that cross the boundary.
- **Observability** (`02`) — every crossing in both directions is recorded.

## Open contracts

- **Runtime validation depth beyond the MVP.** The `02-reasoning-vs-runtime.md`
  open question is narrowed here for Milestones 5; it reopens for the post-MVP
  rework, where "too little makes evolution unsafe, too much recreates a workflow
  engine" has to be resolved with evidence.
- **Streaming across the boundary.** The MVP is request/response per invocation.
  When does a processor stream intermediate effects the orchestrator reacts to
  mid-run?
- **Objective signals as a first-class crossing.** The MVP wires the fixture's
  per-task check in ad hoc; the record shape is the `02-observability-event-model.md`
  "objective signals" open contract.
- **One boundary or two.** Whether the orchestrator/runtime boundary and the
  processor/runtime boundary are the same seam with the same rules, or distinct.
- **Gate placement.** Component of the runtime, or a layer above it
  (`01-invariant-enforcement.md`).
