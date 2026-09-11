# Observability Event Model (v0)

**Traces to:** `00-design/26-arch-observability/01-observability.md`,
`00-design/10-foundations/03-evidence-belief-and-provenance.md`,
`00-design/25-arch-invariant-layer/01-invariant-enforcement.md`,
`00-design/40-roadmap/01-MILESTONES/completed/02-observability-foundation.md` (M2);
binds to `10-technical/01-effect-vocabulary.md`.

## TL;DR

This document fixes the small set of things the record of a run **must** capture
for that run to be reconstructable against a question nobody asked in advance:
who was invoked and in what lineage, every effect the runtime realized, and the
distinct outcome category for a safety intervention. Everything else about the
record — its storage shape, retention, redaction, summarisation, and the exact
payload of most fields — is an open contract, because the schema is expected to
emerge from the first processor and orchestration experiments (Milestones 4–5).

> **Motto:** Pin what must be reconstructable; let the format follow the experiments.

## Status of this document

v0, deliberately thin. It is written now because Milestone 2 needs it and
Milestone 3's gate consumes it. It pins four things and parks the rest. It will
be revised from M4/M5 evidence per the execution cadence; revisions preserve the
historical rationale rather than overwriting it.

## Responsibility

Own the **recorded form of a run** and its **reconstruction guarantees**: the
event types that must exist, the identity and lineage that must link them, and
the outcome categories that must be distinguishable. It does not own effect
typing (`01-effect-vocabulary.md`), gate logic
(`01-invariant-enforcement.md`), or the capability model.

## Narrowing

The design set describes what should be reconstructable — human intent,
processors invoked, context received, outputs, tool activity, effects, objective
signals, human corrections (`01-observability.md`) — without fixing a record
structure. This document narrows that to a **record-per-event model** with four
mandatory event kinds (below), rather than, say, a single narrative log or a
periodic state snapshot. Discarded alternatives: a pure append-only text log
(fails the "relatable to hypotheses" and per-actor-query requirements); a
snapshot/diff model (loses the ordered effect history the gate needs).

## The unit: a run

A **run** is one coherent piece of AI-assisted work with a single originating
human intent. It has a stable `run_id`. Every record below carries its `run_id`
and an ISO-8601 `timestamp`. Records within a run are totally ordered (by a
per-run monotonic sequence number; wall-clock timestamps are not assumed
sufficient).

## Mandatory event kinds

An implementation MUST emit all four. Fields marked *(illustrative)* name intent,
not a fixed shape.

### 1. Invocation record — identity and lineage

One per processor invocation (effect type 6, processor invocation, as seen from
the observability side).

MUST carry:

- `invocation_id` — stable, unique within the run.
- `parent_invocation_id` — the invocation that caused this one, or null for the
  root. This is what makes **per-actor** and **per-intent-lineage** history
  reconstructable (`01-invariant-enforcement.md` composition risk).
- `intent_ref` — link to the originating human intent record.
- `role` — the role definition bound at instantiation (text/reference, not an
  enum — the role vocabulary is open).
- `model_identity` — model name, quantisation, and **whether inference was
  offloaded from GPU**. *(From M0 findings-log entry 1: on the measured host this
  flag predicts latency by 10–20×; any performance hypothesis needs it.)*
- `context_ref` *(illustrative)* — a reference to the assembled context the
  invocation received, resolvable to its actual content for the run's retention
  window.
- `config_ref` *(illustrative)* — which cognitive configuration / generation was
  in force.

### 2. Realized-effect record

One per effect the runtime **realizes**, typed by `01-effect-vocabulary.md` (the
nine types). Proposed-but-rejected effects are also recorded (see kind 4).

MUST carry:

- `effect_id`, `invocation_id` (the proposer), effect `type` (1–9).
- Enough to judge the effect after the fact **representable, permitted,
  attributable, reversible** — the same four properties the runtime judges at
  submission (`02-reasoning-vs-runtime.md`). The concrete carrier is an open
  contract shared with the effect vocabulary.
- `outcome` — realized / failed / **safety-intervened** (see kind 3).
- `result_ref` *(illustrative)* — repository diff, process exit + output,
  network response metadata, memory-entry id, etc., by type.

The ordered sequence of realized-effect records per `invocation_id` and per
`parent` lineage MUST be queryable without replaying the whole run. Gate
sequence evaluation runs against this (`01-invariant-enforcement.md`); the
window and grouping for that evaluation are an open contract owned there, not
here.

### 3. Safety-intervention outcome — its own category

A gate trip that stops or alters an effect, and any decommissioning, MUST be
recorded as a **distinct terminal outcome**, never folded into generic task
failure (bad output, timeout, low quality) (`01-invariant-enforcement.md`,
`01-observability.md`).

MUST carry:

- `intervention_id`, the `effect_id` / `invocation_id` it acted on.
- `kind` — gate-refusal / gate-alter / decommission / accumulation-stop.
- `disposition` from triage — logged-and-proceeded / escalated / halted — and
  that triage never granted an effect the gate refused.
- `retry_eligible: false` — explicit. A safety intervention is **not** eligible
  for automatic retry without recorded human review. A consumer that retries a
  rephrased proposal past this flag is defective.
- `human_review_ref` — null until a human review record is attached.

### 4. Proposed-effect / decision record

One per effect **proposed** by a cognitive component, whether or not realized,
plus findings/proposals/decisions attached to work (effect type 4). This is what
lets a reconstruction see boundary-probing: repeated rephrased proposals after a
refusal.

MUST carry: `invocation_id`, proposed effect `type` and payload ref, and the
disposition (realized → links to a kind-2 record / rejected-by-capability /
rejected-by-gate → links to a kind-3 record).

## Human correction

Where a human corrects, overrides, or annotates during or after a run, that MUST
be recordable and linked to the invocation or effect it concerns. Its structure
is an open contract (M4 will show what corrections actually look like).

## Relationships

- **Effect vocabulary** (`01-effect-vocabulary.md`) — supplies the effect `type`
  domain and shares the "representable/permitted/attributable/reversible" carrier
  open contract. This document requires every realized effect is recorded; it
  does not define the types.
- **Invariant enforcement gate** (`01-invariant-enforcement.md`) — consumes the
  ordered realized-effect history and emits kind-3 records. Owns sequence-window
  semantics.
- **Capability and authority model** (`03-capability-authority-model.md`) — a
  rejection by capability policy is recorded here as a kind-4 disposition; the
  policy itself lives there.
- **Evidence, belief and provenance** (`03-evidence-belief-and-provenance.md`) —
  the provenance graph is downstream of these records; runtime bookkeeping
  (observations, provenance links) is not a gated effect and is emitted by the
  runtime, not proposed.
- **Runtime** (`20-arch-runtime.md`) — emits all four kinds
  as a side effect of doing its job; recording is runtime bookkeeping, not a
  cognitive action.

## Authority

This is a specification document; it has no runtime authority. Normative force is
on any conforming recorder: it MUST emit the four kinds with the mandatory
fields, MUST preserve per-run total order, MUST keep the safety-intervention
category distinct, and MUST NOT drop the ordered effect history to a form that
only supports one-effect-at-a-time review.

## Failure modes

- **Silent gap.** A realized effect with no record is a defect — reconstruction
  would under-count behaviour and the gate's sequence view would have holes. The
  recorder MUST fail loudly (halt the run or mark it non-reconstructable) rather
  than proceed with an unrecorded effect.
- **Category collapse.** A safety intervention recorded as generic failure is a
  defect (invites retry-past-refusal).
- **Lineage break.** An invocation with a dangling or missing
  `parent_invocation_id` breaks per-intent reconstruction; MUST be detectable.
- **Unresolvable reference.** A `context_ref` / `config_ref` that cannot be
  resolved within the retention window makes the run partially unreconstructable;
  MUST be reported, not hidden.

## Open contracts

- **Storage shape.** JSONL-per-run, one growing event log, or a small embedded
  DB? Deferred until M4 volume and query patterns are real. Illustrative default:
  one JSONL file per run under a results tree, like the M0 harness.
- **The four-property carrier.** Shared with `01-effect-vocabulary.md`: one
  common envelope across all nine effect types, or per-type shapes?
- **Retention and tiering.** `01-observability.md` flags that full-token
  retention forever is undesirable and short-term forensic detail must eventually
  be distinguished from long-term summarised evidence. What is the forensic
  window, and what is the summarised long-term form?
- **Redaction.** Secrets, personal data, and large blobs in context/outputs —
  redact at capture, at read, or tier into a restricted store?
- **Hypothesis linkage.** Requirement 3 says records must be relatable to
  hypotheses. Is that a `tags` / `experiment_id` field on the run, a separate
  experiment-registry join, or something richer? Deferred to M4/M5, where the
  first real comparison (two context policies, two orchestrator versions) forces
  a concrete shape.
- **Structured outcome on the effect envelope** *(findings 3, 6)*. Reconstruction
  answered questions never designed into the schema **only where the envelope
  carried structured outcome rather than prose** — cross-record joins are the
  mechanism, and a free-text outcome field cannot be joined on. Does the envelope
  gain a required `verdict` and `terminal_reason`, are they per-effect-type, and
  what is the closed set of values? Re-derived independently at M2 and M5.
- **Source, as an axis across the four record types** *(`00-design/10-foundations/03`)*.
  A human's contribution enters the record as an observation, and what it carries
  need not be. The model has no source axis. Is source a field on every record, a
  property of the actor, or a distinct record kind — and how does it interact with
  findings, which the same document now states may be **negative**?
- **Objective signals.** Build/test/lint results and other objective outcomes are
  named in `01-observability.md` as reconstructable. Are they realized-effect
  results (type 2, process execution) or their own record kind?
- **Sequence-evaluation interface.** The exact query the gate issues against the
  ordered effect history (owned by `01-invariant-enforcement.md`) — this document
  guarantees the history exists and is per-actor / per-intent queryable, but the
  query contract is not yet written.
- **Clock and ordering.** Per-run monotonic sequence is required; is a global
  cross-run ordering ever needed (e.g. for concurrent runs sharing a workspace)?
- **Run boundaries.** What starts and ends a run when work spans sessions, or
  when one intent spawns long-lived background activity?
