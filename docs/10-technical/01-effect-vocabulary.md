# Effect Vocabulary

**Traces to:** `00-design/10-foundations/02-reasoning-vs-runtime.md`, `00-design/24-arch-permission-layer/01-capabilities-and-authority.md`, `00-design/20-arch-runtime.md`, `00-design/25-arch-invariant-layer/01-invariant-enforcement.md`, `00-design/26-arch-observability/01-observability.md`, `00-design/28-arch-work-record/01-work-record.md`

## TL;DR

An effect is a runtime-mediated operation whose **footprint** this project has decided is worth naming and tracking. The set of effect *types* is closed and enumerated here. What falls outside it is pure reasoning, or an operation whose footprint is small enough to leave untracked — principally a read, which is still something the gate may see and a policy may name.

> **Motto:** Cognition proposes from an open vocabulary; it acts through a closed one.

## Responsibility

This document fixes the complete list of effect types in the system and the boundary of each.

It is the shared reference for three components that must agree on that list:

- the **invariant enforcement gate**, which checks proposed effects and effect sequences against the invariant layer (`01-invariant-enforcement.md`);
- the **capability and authority model**, which describes which effect types an actor may request and under what policy (`01-capabilities-and-authority.md`);
- **observability**, which must record every realized effect in a form that supports later reconstruction (`01-observability.md`).

## Narrowing

The design set names effect types in several places without a single canonical list: `02-reasoning-vs-runtime.md` gives an illustrative five, `01-capabilities-and-authority.md` gives an overlapping eight framed as capability areas, `01-invariant-enforcement.md` gives six. This document reconciles them into one enumeration of nine types. No new effect type is introduced that those documents do not already imply.

## Why the set is closed

The system's vocabulary of processor roles is deliberately open — feedback may commission actors that did not exist when any policy was written. Operational constraint therefore cannot be expressed in terms of roles.

It is expressed in terms of effects instead, and that only works if the effect set is finite and known. A new role, however commissioned, can still only request effects from this list, and each is already something the runtime knows how to check.

Adding an effect type is therefore a change to the system's operational surface, not a routine extension. It requires a design-set decision and a corresponding revision here — it MUST NOT happen as an implementation convenience.

## What is outside the vocabulary

Three things, and they are outside it for **different reasons**. Collapsing them is a defect to avoid, because only two of the three are genuinely ungatable.

- **Cognition** — interpreting, challenging, comparing, planning, revising a conclusion. Nothing is proposed, so there is nothing to gate. A conclusion has no effect until a component proposes one of the types below.
- **Runtime bookkeeping** — the runtime recording its own observations and writing provenance links. Not proposed by a cognitive component, so again nothing to gate.
- **Reads** — workspace and repository inspection, memory reads, retrieval of observations or provenance. These **are** proposed by a cognitive component, and the reason they sit outside the vocabulary is different in kind: their footprint is small enough that this project has chosen not to track them as typed effects. That is a judgment about where tracking pays, not a claim that a read changes nothing.

### Reads specifically

A read is **not** outside what may be checked, and listing it alongside the two cases where nothing is proposed invites that misreading. `00-design/10-foundations/02-reasoning-vs-runtime.md` sets out why it would be wrong: every runtime-mediated operation changes the world — a read leaves an access record, makes a store do work and compete for capacity, spends metered quota, and is sometimes a state transition outright.

So, normatively:

- A read MUST be in the enforcement gate's **input domain** (`04-enforcement-gate.md`), whether or not any rule currently fires on one.
- A read MUST be observable (`02-observability-event-model.md`). This is load-bearing rather than hygienic: the canonical composed outcome is an accumulation of permitted reads followed by one permitted effect that carries the accumulation somewhere it should not go, and a gate evaluating only typed effects sees the carrying step with none of what filled it.
- The **default** is permissive: reads pass unless a rule names them. This is a configuration, expressed by `03-capability-authority-model.md`, and it MUST be expressible as a rule rather than being a property of the vocabulary. A vocabulary exclusion would make "hold a rule about this read" a design-set change; a default makes it a configuration change.

What granularity a rule may use to name a class of reads — by path, by crossing type, by volume against a ceiling — is an open contract below.

## The nine effect types

Each realized effect MUST carry enough information for the runtime to judge it representable, permitted, attributable, and reversible **where required** (`00-design/10-foundations/02-reasoning-vs-runtime.md`). That last qualifier is load-bearing: reversibility cannot be demanded of every effect, since some are irreversible by nature and that is what was asked for. What such an effect needs instead is a judgment of whether it is worth what it forecloses, and that judgment is neither of the gating checks — it belongs to a thinking processor and runs **upstream of the proposal** rather than as a stage in this path (`00-design/25-arch-invariant-layer/01-invariant-enforcement.md`). The concrete carrier of that information is an open contract (below); the requirement is normative.

### 1. Workspace mutation

Creating, modifying, moving, or deleting files or directories within a processor's assigned workspace.

- Includes: writing source, editing config files in the workspace, deleting generated artifacts.
- Excludes: changes outside the assigned workspace (not representable — the runtime rejects rather than gates); reading files (a read).

### 2. Process execution

Starting a subprocess or invoking an external command.

- Includes: running a build, a test suite, a linter, a package manager, an arbitrary shell command.
- Excludes: the runtime's own internal processes. Network I/O performed *by* a subprocess is still network access (type 3) and is subject to the same gate at the boundary the runtime can observe.

### 3. Network access

Outbound network I/O initiated by a cognitive component or by a process it started.

- Includes: fetching a URL, cloning a remote, calling an external API, resolving a package from a registry.
- Excludes: loopback communication with runtime-managed services, where the runtime can establish that as the actual target.

### 4. Work-record mutation

Changing the durable representation of work: creating, refining, splitting, merging, deferring, or abandoning a work item, and attaching a finding, proposal, or decision to one.

- Includes: recording that a task rests on a false assumption; splitting one work item into three; marking a decision and its supporting evidence. **A cognitive component's own recorded conclusion — a processor stating that it answered, was blocked, or declined, with its reasoning — is a work-record mutation of this type** (M4 finding, findings-log entry 4: this modelling carved cleanly once chosen, but the boundary was not self-evident from the vocabulary alone).
- Excludes: an intent record's original human-authored content, which is amended only out of band; observations, which are runtime bookkeeping.

### 5. Memory mutation

Writing, revising, or retiring an entry in persistent memory.

- Includes: promoting a finding to project memory; revising a stale convention; retiring a contradicted entry.
- Scope is part of the effect: **project memory** and **system memory** are distinct targets, and a repository convention MUST NOT be writable as a system-scope entry through a single effect.
- Excludes: reading memory; ephemeral conversation, which is never persisted by this type.

### 6. Processor invocation

Instantiating a processor: binding a role definition, an objective, a scope, a live-set identity, a capability set and an interaction mode into a running instance (`06-processor-contract.md`). Context itself is not among them — what the instance sees is composed per turn (`14-context-manager.md`).

- Includes: the orchestrator spawning an implementer; one processor requesting an independent review.
- Excludes: composing a role definition as text (cognition); the instance's own later effects, each gated on its own.

### 7. Configuration mutation

Changing cognitive configuration — processor definitions, orchestrator instructions, context policy, evaluation-role definitions — as a **candidate**.

- Includes: proposing a revised reviewer prompt; adding a new processor role to a candidate configuration; altering a candidate's context budget.
- Excludes: modifying the trusted running configuration in place, which is not representable — the path from candidate to trusted is type 8.

### 8. Promotion

Moving a candidate configuration into a trusted generation, and recording the lineage and the evidence that justified it.

- Includes: promoting a validated candidate; recording a rejection; rolling back to a prior generation.
- This type is expected to carry the heaviest authority constraints of the nine. What those are is specified with the generation model, not here.

### 9. Capability grant and revocation

Changing what an actor is authorized to request.

- Includes: granting an implementer bounded workspace-mutation authority; **revoking an actor's capabilities immediately and unilaterally** (decommissioning, per `01-invariant-enforcement.md`).
- Grant and revoke are the same primitive in opposite directions. Revocation MUST be realizable without a proposal, an evaluation step, or a wait for human review.

## Effect sequences

The gate evaluates sequences, not only individual effects (`01-invariant-enforcement.md`). A series of individually permitted effects can compose into an outcome no single check would catch.

An implementation therefore MUST make the ordered history of realized effects reconstructable per actor and per intent lineage, and MUST NOT treat gate evaluation as purely stateless per-effect. The window, grouping, and pattern definitions for sequence evaluation are an open contract carried by `01-invariant-enforcement.md`.

## Relationships

- **Invariant enforcement gate** — consumes proposed effects typed by this vocabulary; this document does not define the gate's logic, only its input domain.
- **Capability and authority model** — expresses permissions over these types; owns the actor-and-policy dimension this document deliberately omits.
- **Observability** — owns the recorded form of a realized effect and the reconstruction guarantees; this document only requires that every realized effect is recorded.
- **Runtime** — owns representability and reversibility judgments; rejects the non-representable before the gate is consulted.
- **Work record** (`00-design/28-arch-work-record/01-work-record.md`) — owns the durable record that type 4 mutates, and supplies the intent lineage this document requires realized effects to be reconstructable against.

## Open contracts

- What structure carries the "representable, permitted, attributable, reversible" information with each effect submission — a common envelope across all nine types, or per-type shapes?
- Does type 4 (work-record mutation) stay one type, or split once the work model is specified and findings/proposals/decisions prove to need distinct authority?
- Is promotion (type 8) genuinely one effect type, or a small family (promote, reject, roll back) with shared lineage semantics but different authority?
- Should network access (type 3) distinguish destination classes (package registry, arbitrary host, known-service) at the vocabulary level, or is that entirely a capability-policy concern?
- At what granularity may a capability rule name a class of reads — by path, by crossing type, by volume against a ceiling, or something else? Open on the foundational side too.
- Does **footprint** admit a measure a deterministic gate can apply, now that it rather than kind separates a read from a typed effect? Partial candidates: volume against a ceiling, reversibility class, quota consumed. Nothing establishes they compose.
- How is a reversibility class assigned to an effect, and by whom — the proposing component, the runtime, or a static property of the type? `00-design/10-foundations/02-reasoning-vs-runtime.md` (Proposal and effect, 2026-09-10) now argues the proposing side: an effect legitimately irreversible by nature still needs a risk evaluation before it is proposed, reasoning-based and context-grounded rather than a static type property or a runtime check. Not yet reconciled with a concrete carrier here.
