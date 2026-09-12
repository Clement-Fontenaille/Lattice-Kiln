# Thinking

## TL;DR

Thinking is a family of processor roles whose defining product is a proposed change to what the project holds as knowledge. It is not a mechanism the runtime provides and not a quality of reasoning — it is the set of roles invoked to move the knowledge model from one state to another, deliberately.

> **Motto:** Reasoning is free; changing what is held is deliberate.

## Status of this document

First draft, written 2026-09-11. `10-foundations/02-reasoning-vs-runtime.md` defines Thinking as a procedure and states that "thinking is what a processor does" without naming any processor. This document supplies the actor side: what kind of actor, what makes something a member, and what invokes one. It does not specify a prompt, a role definition, or a walk algorithm, all of which belong to technical specification.

## Motivation

`02` defines thinking precisely — walk the provenance graph outward from whatever changed, check each stop for friction or convergence against it, form the attempted argument that friction or convergence implies, check whether it holds, and continue until a stop produces neither or the walk reaches the edge of what is recorded. It states that a walk's product is a **knowledge-state transition**: the instance moves from what it held before to what it holds once findings, qualifications, and appended corrections are recorded.

Nothing in `22-arch-cognition` represented that. The processor document lists candidate roles — assessment, investigation, planning, implementation, debugging, criticism, review, context curation, evaluation — and never mentions the walk. The central cognitive procedure in the foundations had no actor, which is the gap this document closes.

## The membership test

A processor belongs to this family when its product is a **proposed mutation of the knowledge model** — a memory-mutation effect (`10-technical/01-effect-vocabulary.md` type 5) against `21-arch-knowledge-model`.

That test is mechanical, which is the point of stating it this way rather than as a description of careful reasoning. It does not ask how deeply a model reasoned, how many steps it took, or whether it reflected. It asks which store the processor is trying to move.

**The word "proposed" carries the test.** `21-arch-knowledge-model` is written to by two different paths, and only one of them is thinking. Every crossing `23-arch-context-management` registers lands there immediately as an **Observation**, unproposed and ungated, because `10-technical/01` already classes the runtime recording its own observations as bookkeeping rather than as an effect. Nothing reasoned about it and no processor asked for it. Thinking is the other path: a proposal, from a processor, for anything above the Observation level — Evidence, a Finding, a Decision, a qualification, a requalification, a compression, an elision.

`10-foundations/03`'s motto is the line, and it is doing real architectural work rather than summarising: a conclusion is not an observation. What happened is recorded automatically. What it means is not.

## Thinking is not chain-of-thought

These are easy to conflate. They are separated by whether anything was proposed, not by where the writing lands — an earlier draft of this document said the two touched different stores, which stopped being true once every crossing began registering into the knowledge model.

Reasoning inside a single generation — a chain of thought, a scratchpad, an argument worked out mid-response — produces tokens. Under `10-foundations/04`'s account those tokens are an artifact of a generation crossing, which `23-arch-context-management` registers. That registration does write an Observation into `21-arch-knowledge-model`, so the store does grow — but nothing has been *claimed*. An Observation records that a processor produced something, which `10-foundations/03` lists among its examples of directly obtained state. It does not record that what was produced is true, supported, or worth anything.

A knowledge-state transition is what the project *holds* changing: a claim asserted, a qualification appended, a claim requalified, a souvenir written in place of full working, an entry elided. Every one of those is proposed by a processor and checked before it lands. The distinction between thinking and ordinary reasoning is therefore **whether a proposal was made**, not how hard the model worked and not which store grew. A processor can reason at length and perform no thinking; a processor can perform thinking with one short, well-grounded proposal.

This is also why thinking cannot be left implicit. Reasoning happens whenever a model generates. Moving the knowledge model requires a proposal, and a proposal has an author, a check, and a record.

## Deliberately triggered

A thinking processor is invoked. It does not run ambiently alongside other work, and no processor performs thinking as a side effect of doing something else.

The orchestrator (`03-orchestrator.md`) decides a thinking processor is needed and instantiates one, the same way it commissions any role. What makes that decision reasonable is usually a signal produced elsewhere — `10-foundations/03`'s friction, which arises when a claim is put to load-bearing use and does not fit what it is put against.

That suggests a division `03` leaves open when it asks whether friction detection should be a dedicated act or an incidental byproduct of use: **detection can stay incidental while resolution is deliberate.** Ordinary work notices that something does not fit, because ordinary work is what puts claims under load; a thinking processor is then commissioned to walk it. Neither half substitutes for the other, and this document does not settle it — it only records that the two halves can have different answers, which the original question did not allow for.

## Why a family rather than one role

The transitions differ in cost, scope, and what independence they require.

Assessing a claim's scope at the moment it is created (`10-foundations/03`, Scope) is local and cheap, and has to happen then or not at all. Walking a corrected claim's dependents is global and expensive. Requalifying a claim after friction arguably should not be done by whatever produced the claim in the first place, for the reason `02-processors.md` already gives about independent assessment — and scope assessment has no such requirement.

One role covering all of that would be the kind of universal step sequence `02-processors.md` declines to prescribe. A family lets each member be commissioned, evaluated, and retired on its own evidence, which is the discipline the role vocabulary already follows.

## Candidate members

Illustrative, not a taxonomy, and expected to change on evidence the same way any role does.

- **The walk.** Given what changed, traverse provenance outward through dependents, checking each stop for friction or convergence and forming the attempted argument each implies.
- **Requalification.** Given friction that held, produce the appended correction — which `03` says is a qualification far more often than an inversion, and sometimes an open contract stating the ambiguity rather than resolving it.
- **Promotion to a claim.** Given a raw artifact returned by doing — a file read, a test result, a fetched source — decide whether it becomes an Observation, Evidence, or Finding, and with what provenance. `02`'s Feedback section already assigns this to thinking: what doing returns is raw, and turning it into knowledge is the other half.

  **Not the labelling itself, though.** Deciding that something is worth promoting is a judgment; attaching `10-foundations/03`'s labels — claim type, source, mode of acquisition, scope — to everything that crosses is not the same operation, and assigning it to this family does not terminate. Interactions with the model are the discussion, so a labelling call is itself a crossing that produces an artifact which would need labelling in turn. The candidate escapes are inline labelling, where the producing model formats its output to carry them, and out-of-band labelling by a smaller specialised model outside the discussion. Neither is adopted; `21-arch-knowledge-model`'s open question and `90-notes/03` hold it.
- **Curation.** Mark something for remembrance that nothing has cited yet, because it is expected to matter to a comparison that has not happened. Only the exception needs a processor: the default is that anything no longer live and not reachable from a promoted claim is swept mechanically, which `05-curation.md` sets out along with the fact that this member's criterion — expected future need — is the one judgment `10-foundations/03`'s dimensions cannot make.
- **Souvenir compression.** Given a checked demonstration step, reduce its full working to named inputs, conclusion, and — only where the connection is not obvious from those — a note of the argument's shape (`03`, Provenance). Curation's middle outcome, separable because classifying a step as re-derivable is cheap while judging future need is not.

## What this family does not do

It does not record anything. A conclusion thinking reaches is a proposal, and recording it is the runtime's act (`02`, Proposal and effect). A thinking processor that could write to `21-arch-knowledge-model` directly would be a processor that defines reality, which is the thing `02` exists to prevent.

It does not decide what work to do next. Commissioning and sequencing are the orchestrator's.

It does not concern itself with how the walk performs. What this family needs is a question it can ask — what cites this claim — and answering it belongs to `21-arch-knowledge-model`, which satisfies it by following child links. `10-foundations/02` is explicit that what belongs on the cognitive side is that the walk is how a processor thinks, not what makes it fast.

## Service and interactions

- **`21-arch-knowledge-model`** is both what this family reads and what its proposals target. The access pattern is specifically a walk outward through **dependents** — from a changed claim to what cites it — which is the direction `21`'s query surface has to support, not only the parent direction a provenance lookup naturally takes.
- **`20-arch-runtime.md`** gates and realizes the type-5 effect a thinking processor proposes, so a knowledge-state transition passes capability policy and the invariant gate like anything else.
- **`03-orchestrator.md`** commissions a member of this family and consumes what it concludes.
- **`02-processors.md`** holds the general processor definition this family is an instance of; nothing here is a new kind of actor, only a named subset with a shared product.
- **`23-arch-context-management`** is where a thinking processor's own reasoning lands as artifacts, like any processor's. Those artifacts are not knowledge-state transitions, which is the distinction above.
- **`26-arch-observability`** records the transition as an event, separately from `21` holding its result.

## A consequence worth stating

If nothing reaches `21-arch-knowledge-model` except through a member of this family, then the knowledge model is write-gated by role, and `10-foundations/03`'s motivating worry — that an interpretation stored as truth gets treated as evidence by later readers and progressively strengthens a false premise — has a structural answer rather than only a schema.

The line that makes this affordable is `03`'s own: a conclusion is not an observation. An observation entering the record is runtime bookkeeping (`10-technical/01`, What is not an effect) and needs no thinking processor. An **interpretation** — a finding, a decision, a qualification — does. Ordinary work can record what happened; only thinking can record what it means.

Stated as a consequence rather than a rule, because it is stronger than anything the foundations currently require and deserves to be argued before it is relied on.

## Open question

Whether the write-gating consequence above should in fact be a constraint. `21-arch-knowledge-model` currently says it accepts claims proposed by "a processor," unqualified.

Whether friction detection stays incidental while resolution is deliberate, as suggested above. `10-foundations/03` poses this as one question with two answers; splitting it is a proposal, not a finding.

What triggers a walk other than friction. A correction is the clear case. Whether convergence should also trigger one — there is nothing to resolve, only something to credit (`03`) — and whether anything schedules a walk absent either signal, is unsettled. `03` notes that scheduled audit and friction have different coverage and neither substitutes for the other, which suggests something must eventually schedule.

Where a walk that never reaches a fixed point is deemed to have concluded. `02` holds this open and naming the actor does not close it: a processor needs a stopping bound, and this document supplies none.
