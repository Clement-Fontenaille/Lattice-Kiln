# Curation

## TL;DR

Most of what crosses into a conversation is forgotten when the conversation stops needing it, and that happens mechanically. Curation is the act of marking the exceptions — what the project keeps holding after the episode that produced it ends — and compressing what it keeps.

> **Motto:** Forgetting is free; remembering is earned.

## Status of this document

First draft, written 2026-09-11. Provisional, like the storage arrangement it sits next to.

An earlier draft of this document got the relationship between the two backwards, and the mistake is worth recording because it is easy to repeat. `23-arch-context-management` now keeps only references into `21-arch-knowledge-model`, with every crossing's content written there as it arrives. That reads as though everything is therefore retained, and that forgetting must consequently become a per-item judgment. It does not follow. Where content *lives* and how long it is *kept* are independent, and the storage decision was taken for a reason that has nothing to do with retention: so that promoting something later does not mean copying it out of a conversation into the record, because it was never anywhere else.

The retention default is unchanged from `10-foundations/05`, and is the opposite of retention.

## The default: not live, not remembered, removed

An artifact that is no longer live, and that nothing registered for remembrance, is removed.

Nothing judges this per item. For nearly everything that crosses, the question is settled by **reachability**, and `10-foundations/03` already supplies the rule: a promoted claim's roots have to stay raw, because nothing regenerates an observation that was never kept. So an observation a promoted claim cites cannot be removed — removing it would quietly turn every souvenir above it into an assertion nobody can check — and an observation no promoted claim cites has nothing depending on it.

Remembrance is therefore mostly *implied* rather than declared. Something survives because a thinking processor built a claim on it, which is a decision that already had to be made on its own merits. The sweep then removes what is left, and `21-arch-knowledge-model`'s Elide operation carries reachability as a precondition rather than trusting whoever calls it.

This is garbage collection, and it is worth saying so plainly: it is mechanical, it needs no criterion, and it costs no model calls.

## What actually needs judgment

One thing only: keeping something that nothing has cited yet, because it is expected to matter to a comparison that has not happened.

`10-foundations/05` states the difficulty precisely. That is not Pertinence, which asks whether a claim matters to the comparison in front of it now, and none of `03`'s three weighing dimensions looks forward at all. Validity, reliability and pertinence are each assessable against what exists; expected future need is not.

So curation does need a judgment the substrate does not supply — but only for this, and this is the exception rather than the rule. The common case is reachability. A criterion for the exception is left as a parameter here rather than invented, which at least makes different criteria comparable the way `23-arch-context-management`'s recall policy does.

## Compression is a separate, cheaper decision

A claim that is being kept can still shed its working. `03`'s souvenir rule gives the test: raw detail is required only where a claim cannot be reliably reconstructed without it, so a chain's roots stay raw while a checked demonstration step above them compresses to its named inputs, its conclusion, and a note of the argument's shape only where that connection is not obvious from those alone.

Classifying a step as re-derivable is cheap and largely structural — does it have roots that are being kept, and was it checked. That is why compression is separable from the remembrance judgment above, and why it can be built first.

## Scope, at creation

`03` says a claim's scope has to be assessed near its own creation or not at all, because the domain a claim was born into was never fully representable and no later reader recovers it.

This runs when a claim is **promoted**, not when an artifact crosses. Scope is a property of a claim, and an observation destined for the sweep never becomes one. `10-foundations/05`'s argument that Collapsing keeps scope assessment cheap by keeping it rare therefore holds exactly as written: the expensive, necessarily-imperfect work is spent only on what survives to be a claim.

## Who performs it, and through what

- **The judgment** — deliberate remembrance, and compression — belongs to a member of the thinking family (`04-thinking.md`). Both are proposed changes to what the project holds, which is that family's membership test.
- **The mechanism** is `21-arch-knowledge-model`'s Compress and Elide operations. A curation processor proposes; it does not reach into the store.
- **The sweep** needs no processor at all. It is a policy the runtime can execute against reachability, and making it a judgment would be spending model calls on a question a graph traversal answers.

A proposal is a memory mutation like any other (`10-technical/01-effect-vocabulary.md` type 5), so it passes capability policy and the invariant gate. A processor that could elide directly would be a processor deciding what is true by deciding what remains, which is authority `10-foundations/02` withholds.

## When it fires

The sweep fires when something stops being live — a pool entry going archived, or a pool ending. It is incremental by nature, because reachability is local.

Deliberate remembrance fires during an episode, not after it. Marking something worth keeping is a judgment made while the reasoning that motivates it is still in view; deferring it to a teardown pass would mean reconstructing that motivation from a record of an episode that has ended. Compression can be deferred, since a checked step stays re-derivable.

Whether anything should run a periodic pass over already-kept material — re-compressing, or revisiting a remembrance decision that turned out wrong — is open.

## Observability holds what the sweep removes

`26-arch-observability` keeps its own copy of artifacts and events, and that copy is what outlives the sweep. An entry removed from `21-arch-knowledge-model` stops being something the system knows and stops being available to reason from, while remaining reconstructable in observability's history under its own retention rules.

That is not a contradiction. Reasoning and auditing are different uses, which is why the stores were separate before any of this.

## General shape and a naive default

The sweep first, since it is deterministic and does the bulk of the work: on a pool entry becoming non-live, remove the referenced entry unless a promoted claim cites it. No model call.

Compression second, on structural rules: a claim with kept roots and a recorded check is a souvenir candidate.

Deliberate remembrance last, and only once the first two have a measured failure mode that justifies adding a judgment.

## A caution, and a relocation

`70-THINKING/07-when-to-decompose/18-ares-soundness.md` describes a retention mechanism where each claim is carried forward into the premise set for later steps with probability equal to its own entailment score. An earlier draft of this document read that as evidence about curation. On a closer reading it is mostly evidence about something else: what that mechanism retains is what is *available to reason from at the next step*, which is recall (`23-arch-context-management`) rather than what is durably kept. The sheet's finding that keeping every base claim was consistently best with a strong judge, with selective retention helping only a weaker binary one, belongs to the recall policy's evidence and not here.

What does transfer is the collapse mode. When the judge is overconfident and returns near-certainty everywhere, every retention probability rises toward one, the filter stops filtering, and the mechanism becomes a no-op while still costing what it cost before — and the sheet notes that no diagnostic was proposed to detect it. Any judgment-based filter inherits that, including deliberate remembrance here. The sweep does not, because it has no judge.

Both readings are second-hand (`03`): they come from this project's own analysis sheet about that paper, not from the paper.

## Forgetting has a second half, not addressed here

Everything above concerns the transition **from discussion into memory**: what an episode leaves behind. That is one of two questions and it is the one this document answers.

The other is retention **within** memory. What has been remembered does not stop accumulating simply because it was worth remembering once, and the project's textual content cannot grow without bound. Hierarchy and provenance exist to make important material findable, not to make unbounded growth acceptable — those are different problems and the first does not solve the second.

This is named rather than addressed. Nothing here says what ages, what is re-compressed, what is retired, or what would trigger any of it. It should be settled before the remembered set is large enough for the question to be urgent, which it is not yet.

## Open question

What the criterion for deliberate remembrance is. Named above as absent from `03`'s dimensions and left as a parameter.

What governs retention within memory over time, per the section immediately above.

What detects a remembrance judgment that has stopped discriminating. The collapse mode above produces an absence rather than an error, so nothing notices it from the inside. `26-arch-observability` names the material a detector would need — the ratio of registered observations to remembered ones, tracked over time, is a drift signal computable from its history and from nothing else — but naming the signal is not proposing the mechanism, and none is proposed.

What detects a sweep that took something needed. The failure case is an artifact whose value is recognised only after reachability already removed it. This looked undetectable, on the grounds that the evidence it happened went with it. That is wrong: it went from `21-arch-knowledge-model` alone, and `26-arch-observability` still holds it. A later pass can ask whether anything swept was subsequently searched for, re-fetched, or re-derived, which is the signal that the rule cut too early. That this is answerable at all depends on observability staying greedy.

Whether anything revisits a remembrance decision later, and what would prompt it.

How eliding and `03`'s append-only Qualification rule coexist. Append-only governs corrections to a claim that was promoted and relied on; the sweep removes entries nothing built on. The two should not meet, but nothing here proves an entry cannot reach a state where both apply.

What peak store size looks like during a long episode, since steady state is bounded by what is live plus what was remembered but the peak is not.
