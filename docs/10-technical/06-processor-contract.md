# Processor Contract (v0)

**Traces to:** `00-design/22-arch-cognition/02-processors.md`,
`00-design/22-arch-cognition/01-work-intent-and-task-model.md`,
`00-design/24-arch-permission-layer/01-capabilities-and-authority.md`,
`00-design/10-foundations/05-ephemeral-conversation-curated-memory.md`,
`00-design/40-roadmap/01-MILESTONES/completed/04-ephemeral-processors.md` (M4);
binds to `10-technical/01-effect-vocabulary.md` (effect type 6),
`10-technical/03-capability-authority-model.md`,
`10-technical/02-observability-event-model.md`,
`10-technical/07-naive-context-assembly.md`.

## TL;DR

A processor is a disposable reasoning instance bound at instantiation by five
things — role instructions, an objective, a context bundle, a capability set, an
interaction mode — that reasons in one model context, may **propose** effects
(never realize them), emits one result, and then ends. There is no resume.

> **Motto:** Give each mind a job, not a lifetime — and a receipt for everything it touched.

## Status of this document

v0 for Milestone 4. It fixes the processor *input* and *output* envelopes and the
lifecycle, enough to run the ephemeral-vs-monolithic experiment. Discussion
between processors, context-request servicing, and the result schema's structure
are parked as open contracts — M4 evidence shapes them.

## Narrowing

`02-processors.md` says a processor is "natural-language role instructions, an
objective, selected context, available capabilities, and interaction
expectations." This document narrows those into a concrete **input envelope**, an
**output envelope**, and a **lifecycle**, and binds the whole to the
`processor_invocation` effect (type 6) and the kind-1 invocation record. It does
**not** narrow the role vocabulary — that stays open (`02-processors.md`) — and it
does not decide which roles exist (M4 uses a tiny fixed library; the library is
system-level-feedback's concern from M10).

## Responsibility

Define the structure and lifecycle of one processor instance: what binds it, what
it may consume, what it may emit, and what it may never do. It does not define
orchestration strategy (`03-orchestrator.md`, Milestone 5), context *selection*
(`07-naive-context-assembly.md`), or effect typing
(`01-effect-vocabulary.md`).

## Inputs — the processor input envelope

Bound at instantiation by whoever issues the type-6 effect: a fixed harness in
M4, the orchestrator from M5 on.

- `role_instructions` — free natural-language text. Encourages reasoning habits;
  does not prescribe a step sequence. Not an enum.
- `objective` — the bounded goal for *this* instance, in the caller's words.
  Recorded verbatim in the kind-1 record so the result can be checked against it.
- `context_bundle` — the assembled context
  (`07-naive-context-assembly.md`). This contract treats it as opaque beyond: it
  has a resolvable `context_ref`, an ordered source list, and a token estimate
  within budget.
- `capability_set` — the grants this instance holds
  (`03-capability-authority-model.md`). An effect type absent from the set means
  the instance may not request it; the set may be empty (a pure-reasoning
  instance, e.g. a reviewer).
- `interaction_mode` — for M4, one of:
  - `oneshot` — no interaction; produce a result.
  - `review` — receives a prior processor's **conclusion only**, not its
    reasoning history (`02-processors.md`, independence), and produces an
    assessment.
  Orchestrator-mediated discussion is Milestone 5.
- `model_identity` — name, quant, and whether inference is offloaded (M0
  findings-log entry 1). On the MVP host this is the one resident model for every
  role.

## Outputs — the processor output envelope

- **Proposed effects** — zero or more, each typed `1..9` with its four-property
  envelope, each submitted through the enforcement pipeline
  (`04-enforcement-gate.md`: representability → capability → gate → sequence).
  The processor never realizes an effect itself.
- **Result** — a natural-language conclusion and/or an artifact reference, plus a
  self-declared `terminal_state`:
  - `answered` — the objective was pursued to a conclusion;
  - `blocked` — could not proceed (missing context, capability, or dependency);
  - `declined` — the correct response is *not* execution
    (`01-work-intent-and-task-model.md`: false assumption, wrong problem, already
    satisfied, needs investigation first).
- **Context requests** *(illustrative)* — context the instance needed but did not
  receive (`04-context-as-governed-resource.md`). In M4 these are **recorded but
  not serviced** — naive assembly does not loop.

## Authority

- A processor **MAY** propose effects within its capability set and emit one
  result.
- A processor **MUST NOT**: realize any effect; write persistent memory directly
  (memory mutation is a proposed effect, type 5); modify its own role,
  objective, or capability set; invoke another processor unless granted type 6;
  or carry state into a later instance except through an explicit `context_bundle`.
- Nothing in this contract exempts a processor's proposed effect from capability
  gating or the invariant gate.

## Lifecycle

1. **Instantiate.** The caller emits a type-6 effect. The runtime binds the input
   envelope, allocates the capability set, and opens a kind-1 invocation record
   with `parent_invocation_id` set to the caller's invocation (or null for a
   harness/root).
2. **Run.** One model context. Ephemeral: no state from any prior instance except
   what is in `context_bundle`. The instance's conversation is observable through
   the run record but is **not** persisted as curated memory
   (`05-ephemeral-conversation-curated-memory.md`).
3. **Terminate.** The instance ends when it emits its result, or when the runtime
   stops it (safety intervention; resource ceiling R3; error). Termination is
   final — no resume. A follow-up is a new instance with a new bundle.

## Failure modes

- **Silent effect.** A state change with no recorded proposed→realized chain is a
  defect (`02-observability-event-model.md`, silent gap).
- **Role bleed.** An instance pursuing an objective other than the one it was
  bound. The kind-1 `objective` plus the recorded result make this detectable;
  detecting it is part of the M4 reasoning-quality assessment.
- **Unterminated.** An instance that neither emits a result nor is stopped MUST
  hit the R3 run bound and be halted — never hang.
- **Capability probing.** Repeated proposals outside the capability set after
  rejection — recorded as kind-4 dispositions; the sequence the gate's (stubbed)
  sequence check will eventually watch.

## Relationships

- **Effect vocabulary** (`01-effect-vocabulary.md`) — supplies the type-6 shape
  and the `1..9` domain for proposed effects.
- **Capability model** (`03-capability-authority-model.md`) — supplies the
  `capability_set`; every proposed effect is checked against it.
- **Enforcement gate** (`04-enforcement-gate.md`) — every proposed effect passes
  it; a refusal ends the effect, not necessarily the processor.
- **Observability** (`02-observability-event-model.md`) — the kind-1 record is
  this contract's instantiation output; kind-2/4 records are its effect activity.
- **Naive context assembly** (`07-naive-context-assembly.md`) — produces
  `context_bundle`.
- **Orchestrator** (`03-orchestrator.md`, Milestone 5) — becomes the caller;
  until then a fixed harness issues the type-6 effect.

## Open contracts

- **Discussion protocol.** Multi-processor, orchestrator-mediated challenge and
  re-investigation (`02-processors.md`, discussion) — Milestone 5.
- **Context-request servicing.** Naive assembly is one-shot; when does a
  processor's request for more context get answered, and by what?
- **Result schema.** Free text plus `terminal_state` for now. M4 will show what
  structure the evaluation actually needs.
- **Role-definition source.** M4 draws role instructions from a tiny fixed
  library. Authoring per-invocation vs. a governed library is system-level
  feedback's concern (Milestone 12).
- **Independence cut for `review`.** Is "prior conclusion only" the right amount
  of isolation, or too little / too much (`02-processors.md` open question)?
- **`terminal_state` granularity.** Whether `answered / blocked / declined` needs
  finer categories once real tasks run.
