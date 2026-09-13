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

A processor is a disposable reasoning instance bound at instantiation by seven
things — role instructions, an objective, a scope, a live-set identity, an
isolation preference, a capability set, an interaction mode — that reasons in one
model context, may **propose** effects (never realize them), emits one result, and
then ends. There is no resume.

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
- `scope` — the mandate this instance's work must stay within, as natural-language
  text (`00-design/24-arch-permission-layer/01-capabilities-and-authority.md`).
  Inherited from the work item; the instance may not widen it, and it does not
  change for the instance's life. An instance that finds it must reach further stops
  and reports rather than extending itself.
- `live_set_id` — the identity of the live set this instance's crossings register
  into, and which recall runs over each time the instance is fed. **It belongs to the
  task, not to this instance**, so a second instance under the same task binds the
  same one and finds it already populated
  (`00-design/23-arch-context-management/01-context-manager.md`). **Context itself is
  not bound at instantiation.** What the model sees is the *turn input*, composed
  afresh on every turn out of the live set under the recall policy; there is no
  bundle handed over once and held. A new task's live set is not
  empty either: the intent has crossed, and a crossing registers
  (`70-THINKING/18-task-artifact-edges.md`).
- `objective` handoff framing — where a prior step's output reaches this instance,
  it MUST arrive **inside the objective**, framed, and MUST NOT be appended as a
  separate block of context. See Handoff framing below; this is normative and
  measured.
- `isolation` — what this instance may inherit from contexts already built, as a
  value the recall policy consumes (`14-context-manager.md`). Stable for the
  instance's life, like `scope`. Its default comes from the role definition; the
  caller MAY tighten it and MUST NOT loosen it below what the role requires — an
  orchestrator asking for an independent review can demand isolation a general
  reviewer role does not default to, and cannot waive isolation a judging role
  does.
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
- **Context requests** — not an output envelope field. A request for more context
  is an **ordinary tool call** the instance makes mid-reasoning: the runtime
  executes it, and `14-context-manager.md` registers what comes back like any
  other crossing. What the instance could not obtain is reported through its
  result — `blocked`, with the reason — not through a separate channel.

## Handoff framing

*Exercised by: findings 6, 6 addendum, 8.*

**A handoff is one instance passing something it produced to the next one.** Instances
are disposable and nothing carries over by itself, so when step N+1 needs to know what
step N found — the test failed, and here is how — that information has to be put
somewhere the new instance will see it. There are two places it can go, and they are
not equivalent: **inside the objective text**, or **beside it**, as another block of
material the model is also shown.

How a prior step's output reaches the next instance is a measured contract rather
than a style choice, and getting it wrong does not degrade the result gracefully —
it changes what the instance does. A 7B implementer whose context carried a plan, a
critique, or a prior summary **narrated instead of writing**: prose describing a fix
with no file produced. The same model given only an objective and code produces
effects reliably.

Three framings, graded by what was observed, and the grade is the specification.

**1. An objective signal folded into the objective — required where one exists.**
The Milestone 6 arm that reached 24/30 with zero regressions folds the failing
check's own output into the objective text, bounded, and follows it with an explicit
instruction about the form of the output. What it passes is a **machine-produced
signal**, not another model's account of one.

*(Illustrative — the shape, not a format.)*

```
<the objective, verbatim>

Current state still fails:
<the check's own output, bounded to a fixed number of lines>

Output the whole corrected file(s).
```

**2. Model-produced prose in a named section — tolerated, not preferred.** A plan
carried under an explicit heading survived; the same content unlabelled did not.
Labelling is what keeps it from reading as the conversation the instance is
supposed to be having.

**3. Unlabelled prose appended as context — MUST NOT.** This is the failure above,
and it is the one to design against.

Two rules follow that are worth stating separately, because they are what the three
grades are actually about.

**Prefer a signal to an account of a signal.** Where an objective check exists, its
own output is what gets handed forward. A model's summary of a failure is strictly
worse input than the failure, and it is available only because something already
produced the better version.

**Model prose whose audience is the operator does not enter another instance's
objective.** A premise audit's concerns are advisory and belong in the escalation
payload, which a human reads (`11-static-workflow.md`). Routing them into an
implementer instead is exactly case 3 wearing a justification.

### Who composes the objective

The rules above say what may go into an objective and not who assembles it, and an
objective for a retry is plainly assembled by something. Three sources, with
different standing.

**Composed mechanically, from a signal.** The workflow concatenates: the task text,
the check's output, an instruction about the output form. No model is involved in
the composition. This is what the Milestone 6 arm does and what the evidence above
covers.

**Written by a model.** A planner producing the next instance's instructions. This
is measured and it is the harmful case at this model size — injected plans hurt, and
the failure is the narration one. It is not forbidden in principle; it is
unsupported by anything, and a build that wants it owes evidence rather than
argument.

**Not composed at all.** The task text alone. This is the monolith, and it is the
baseline the other two are measured against rather than a degenerate case.

**Structured audit output may steer the composition; audit prose may not enter it.**
The distinction is what the output *is*, not where it came from. A premise audit
emits a classification — an enum — and `11-static-workflow.md` uses it as the concern
split's firing condition, which is a structured value selecting a branch. The same
audit's concerns are prose addressed to the operator and stay out of any objective.
An implementation that lets audit prose reach an implementer because "the audit
influences later stages anyway" has crossed exactly the line the grades above draw.

**What this does not cover, and it is the next real question.** Decomposition
produces sub-objectives, and something has to write them. A split that is more than
splitting on punctuation needs a model to formulate each part, which is case two
above — the unsupported one. So the rule here does not extend to decomposition, and
saying it does would be overreach. `00-design/22-arch-cognition/08-decomposition.md`
has no specification counterpart, and this is one of the things that document owes.

**Scope of the evidence.** This is measured at the 7–8B size this project runs on,
and policy adequacy is model-dependent
(`00-design/23-arch-context-management/02-context-as-experimental-surface.md`). A
larger model may tolerate framings this one does not. The rule stands for the
reference host and should be re-measured before it is assumed to carry.

**The alternative shape this does not adopt.** A handoff could instead be written
somewhere durable and **read** by the next instance, arriving as a crossing rather
than as objective text. That is cheaper to justify only once live-set seeding is
settled (`14-context-manager.md`), and nothing measured supports it yet. Folding
into the objective needs no new mechanism and is what the evidence covers.

## Authority

- A processor **MAY** propose effects within its capability set and emit one
  result.
- A processor **MUST NOT**: realize any effect; write persistent memory directly
  (memory mutation is a proposed effect, type 5); modify its own role,
  objective, or capability set; **widen its own scope**; invoke another processor
  unless granted type 6; or carry state into a later instance except through
  something durable that the later instance reads for itself.
- Nothing in this contract exempts a processor's proposed effect from capability
  gating or the invariant gate.

## Lifecycle

1. **Instantiate.** The caller emits a type-6 effect. The runtime binds the input
   envelope, allocates the capability set, and opens a kind-1 invocation record
   with `parent_invocation_id` set to the caller's invocation (or null for a
   harness/root).
2. **Run.** One model context, fed a turn input composed afresh on each turn from
   the live set. Ephemeral: no state carries from a prior instance except by way of
   a crossing this instance performs for itself — a read of something the previous
   step wrote down. The instance's conversation is observable through the run record
   but is **not** persisted as curated memory
   (`05-ephemeral-conversation-curated-memory.md`).
3. **Terminate.** The instance ends when it emits its result, or when the runtime
   stops it (safety intervention; resource ceiling R3; error). Termination is
   final — no resume. A follow-up is a new instance, with its own live set and its
   own scope bound afresh.

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
  this contract's instantiation output, carrying the bound `scope` verbatim;
  kind-2/4 records are its operation activity, and the kind-5 turn-input records
  are what it was actually shown, turn by turn.
- **Context management** (`14-context-manager.md`) — registers every crossing and
  composes the turn input on every turn. `07-naive-context-assembly.md` supplies
  the naive default for both halves: which reads seed a live set, and the
  degenerate recall policy that orders it.
- **Orchestrator** (`03-orchestrator.md`, Milestone 5) — becomes the caller;
  until then a fixed harness issues the type-6 effect.

## Open contracts

- **Discussion protocol.** Multi-processor, orchestrator-mediated challenge and
  re-investigation (`02-processors.md`, discussion) — Milestone 5.
- **Context-request servicing — closed.** A processor's request for more context
  is an ordinary tool call: the model calls it, the runtime executes it, and the
  context manager registers what comes back like any other crossing. No separate
  servicing path is needed, and none should be built.
- **Splitting the output.** The `Result` above is one object carrying a conclusion
  and a terminal state, and an instance's reasoning is not separated from it. Keeping
  a handoff monolithic is a pitfall worth anticipating rather than a simplification:
  it makes the `review` independence cut unperformable without re-parsing prose; it
  denies a recall policy the most obvious saving available, since reasoning is the
  bulk and the conclusion is what is load-bearing; it forces retention to keep the
  reasoning or lose the conclusion with it; and it flattens a provenance chain that
  should run inputs — reasoning — conclusion into an edge pointing at a blob.
  It would also make `12-knowledge-model.md`'s **Compress** nearly free, since a
  souvenir would be the conclusion artifact once the reasoning artifact is dropped,
  rather than an operation that rewrites anything. What the cuts are, and whether
  they differ per role, is not decided.
- **Result schema.** Free text plus `terminal_state` for now. M4 will show what
  structure the evaluation actually needs.
- **Role-definition source.** M4 draws role instructions from a tiny fixed
  library. Authoring per-invocation vs. a governed library is system-level
  feedback's concern (Milestone 12).
- **Independence cut for `review`.** Is "prior conclusion only" the right amount
  of isolation, or too little / too much (`02-processors.md` open question)?
- **`terminal_state` granularity.** Whether `answered / blocked / declined` needs
  finer categories once real tasks run. One case is already identified:
  `00-design/22-arch-cognition/01-work-intent-and-task-model.md` names two distinct
  reasons to refuse execution — the task rests on a false premise, and the request
  has already been satisfied — which both land on `declined` while calling for
  different follow-ups. That is the shape of the collapse Milestone 5 recorded
  between `declined` and `blocked`, one level down.
