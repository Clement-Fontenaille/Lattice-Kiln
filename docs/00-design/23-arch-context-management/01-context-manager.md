# Context Manager

## TL;DR

The context manager registers artifacts crossing in from tool calls or the model's own output, tracks the live set they form, and runs a recall policy deciding which of them actually reach the model at any given turn.

> **Motto:** Nothing crosses without being counted.

## Status of this document

Draft. A naive default already exists in part — `10-technical/07-naive-context-assembly.md` — and is credited here, not replaced.

## Motivation

`10-foundations/04` established that a context is the set of artifacts currently live, each the product of a crossing from one of three locations, and that none of its four failure modes are checkable without an explicit, first-class live record. This actor owns that record.

## The actor and its responsibility

- **Register** artifacts as they cross in from any tool call — a read, a test run, any effect response — or from the model's own generated output. What crosses in is written to `21-arch-knowledge-model` as an Observation, and what this actor keeps is a **reference to that entry plus its own tracking metadata**: crossing type, live or archived state, and whatever else recall needs. This actor holds no artifact content of its own. It never initiates a crossing either, only records what came back once something else did.
- **Track** the live set registration populates.
- **Recall** — bringing something already in the pool back in front of the model. It is the positive operation: it presents. It never fetches anything new, so it only ever works over content already registered. That boundedness is the point: given a fixed pool, a policy chooses what to put in front of the model, which makes different recall policies directly comparable and testable against each other while the pool is held constant.

## Prefix persistence changes the shape of the policy space

Whether the serving arrangement keeps a reusable prefix across turns is not a performance detail sitting underneath recall. It decides what kind of question recall is, and this document previously ignored it.

**Without prefix persistence**, everything the model is to see on a turn is sent again on that turn. The whole live set is recalled every time, by necessity. Leaving something out is possible but it is not an optimisation — it simply denies the model that material. So the strategy space collapses to two levers: what is included at all, and in what **order** it is presented. Ordering then carries most of the interesting question, and it is a real question, because position affects what a model attends to.

**With prefix persistence**, the stable part of the sequence is not recomputed. Appending is cheap, and disturbing anything before the append point is not. The strategy space opens considerably and becomes much less settled. What belongs in the stable prefix and what belongs in the mutable tail. Whether anything is ever removed from the prefix, and what that costs. What happens when something dropped has to come back. Whether several pools can share a prefix. Whether a policy should be shaping the sequence for reuse rather than purely for relevance.

Those are not questions this project can settle from its own first principles. They need experiment, and they need whatever preliminary results the literature already holds. This is one axis among several, named here because it was the first to surface; `02-context-as-experimental-surface.md` holds the general treatment.

**The pool is an index, not a store (2026-09-11).** Everything a crossing returns is written to `21-arch-knowledge-model` first, so there is exactly one copy of any artifact's content and this actor points at it. An earlier version of this document made that arrangement a special case for knowledge-base retrievals only, on the grounds that a retrieved claim already had an identity there while a tool output did not. Registering every crossing as an Observation removes the asymmetry: the special case becomes the rule, and the exception disappears.

This is a decision about **where artifact content lives, and nothing more**. It says that the record is the one place artifact content is held, so that promoting something later does not mean copying it out of a conversation and into the record — there is no rewrite step, because it was never anywhere else. It does not say that what is written is kept.

One asymmetry survives, and saying the exception "disappears" overstated it. A crossing's registration records two things: that a crossing happened, with its type and its moment, and what it returned. For a tool call or a generation, what it returned is new content and is written. For a knowledge-base retrieval, what it returned is a claim that already exists, so nothing new is written and the registration carries a pointer instead. The **shape** is uniform — every crossing produces a registration, and the pool holds references either way — while the **cost** is not, since only some crossings add content. That distinction matters for anything sizing this store, and flattening it would make retrieval look as expensive as reading a file for the first time.

Retention is the opposite by default. An artifact that is no longer live, and that nothing registered for remembrance, is removed (`22-arch-cognition/05-curation.md`). Writing to the record is cheap and reversible; remembering is the exception that has to be earned. Reading this section as a retention policy would invert `10-foundations/05`'s position, which it does not touch.

Provisional, adopted to see where it leads rather than because it has been shown correct. What it buys: one copy instead of two, so the pool cannot drift from the record; a pool that is pure bookkeeping — references and metadata — which is the mechanical-engine half `70-THINKING/ideas.md` I12 describes; and no promotion path that has to move content between stores.

Knowledge-base retrieval is a tool like any other — the model calls it, the runtime executes it, this actor registers the reference. This actor never initiates that call itself, on a processor's behalf or otherwise. Once a reference is in the pool it is subject to the same recall policy as anything else, regardless of which crossing put it there.

## Service provided to the rest of the system

- **What the model sees on a given turn.** Composed at the moment of feeding, out of what is in the pool and what recall selects from it. This is not a package delivered once per invocation and then held: it is recomposed every turn, over a pool that grew since the last one. It is also richer than the naive default's flat file list, since each entry carries its crossing type.
- **A live-state query**, for any of `04`'s failure-mode checks to consult. One of those checks is now answerable here that was not before: `04`'s Insufficiency splits into material that never crossed and material that crossed but was not recalled, and the second is visible by comparing the pool against what was composed. The first is not visible from here at all, since nothing can be compared against what was never fetched.

Nothing has to ask for the first of these. This actor sits in the path everything to and from the model takes, so it composes because a turn is happening, not because something requested a composition. There is no assembly call to place, and no caller to name.

## General shape and a naive default

`10-technical/07-naive-context-assembly.md` already implements a fragment of this: deterministic substring matching, a flat token budget, a mandatory selection trace — no embeddings, no model calls. It has no recall policy in any real sense: everything selected is presented, nothing is ever archived-then-recalled, and anything past the budget is truncated once with no path back. That truncation is itself a degenerate recall policy — recall everything until the budget runs out, then archive the rest permanently — and naming it this way is what exposes its one missing piece: recall.

The naive default should grow artifact registration and a real live record first, since both cost nothing extra to compute. A recall policy that can actually restore something already archived is the harder addition and has no existing precedent to build from.

`70-THINKING/ideas.md` I12's mechanical-engine account still applies to the bookkeeping half of all of this — registering, tracking, running a fixed policy — with judgment called out to only where a query genuinely needs it.

## Interactions

- **`20-arch-runtime.md`** executes a tool call a processor proposed; this actor registers the output. It does not itself initiate a crossing. The runtime does not fetch context on a processor's behalf either — `20-arch-runtime.md`, Instantiation, and then a loop, states why there is nothing to fetch: what the model sees is composed on each turn as the turn happens, not bound at instantiation.
- **`21-arch-knowledge-model`** answers a query only when the model calls the retrieval tool; this actor registers what comes back the same as any other tool output.
- **`22-arch-cognition`** processors are instantiated with role instructions, an objective, and a capability set, and with a pool identity rather than with context itself; what they see is composed turn by turn. They may call the knowledge-base retrieval tool mid-reasoning — an ordinary tool call, and the only way knowledge-base content enters the pool. A processor's own role instructions can require that call rather than leave it to unprompted judgment — the "prompted or required" fix `10-foundations/04`'s Expected behavior already names for exactly this class of problem, using role definition, not a new mechanism. `10-foundations/04`, findings-log entry 5 (one model, one prompting setup) showed an *unprompted-and-unsupported* request affordance going unused; that bounds a claim about that condition only, not about a role-required call, and not about whether the result holds across model scale, prompting, or finetuning, which is untested.
- **`26-arch-observability`** needs this actor's per-turn compositions and lifecycle transitions to answer what a processor was actually shown, and when. The dependency runs the other way too, and it is not optional: recall's comparability argument above — two policies over the same pool, held constant — is a measurement only if what each policy presented was recorded. Without that history the comparability is a property of the design that nobody can take a reading of.
- **`27-arch-adaptation-and-evolution`** treats the recall policy as tunable system configuration: system-level feedback may propose a revision to it, a generation carries one, and a bootstrapped instance inherits the validated version. This is the loop recall's boundedness was meant to serve — two policies over the same pool are directly comparable, which is what makes a proposed revision evaluable rather than merely plausible.
- **`24-arch-permission-layer`** decides whether a call is allowed at all, before this actor ever sees what it produces. That check is not uniform across crossing types: a read — a file, a knowledge-model query — is not an effect and is only capability-gated, while an effect passes capability gating and then the invariant gate. Either way, what reaches this actor has already been allowed; this actor never gates anything itself.

## Relationships

- **`10-foundations/04`** — owns the schema this actor realizes.
- **`21-arch-knowledge-model`** — a tool-call target the model queries; this actor registers the result, not the query.
- **`20-arch-runtime.md`** — executes the crossings whose outputs this actor registers.
- **`22-arch-cognition`** — what this actor composes for, turn by turn, and the source of live, model-initiated retrieval calls. Not a consumer in the calling sense: a processor never requests its own context.
- **`26-arch-observability`** — a separate store, not a shared one, same reasoning as `21-arch-knowledge-model`'s relationship to it. This actor's live record and observability's history have different lifecycles; the selection trace and lifecycle transitions are what this actor contributes, but observability keeps its own copy.

## Open question

How a pool is seeded when a processor starts. Register records what a crossing returned and recall presents what a pool already holds, so neither of this actor's two operations can put anything in a pool before the first crossing — a pool is empty at turn zero by construction. Two shapes are available. Inheritance could be a third primitive alongside register and recall, moving or referencing already-registered artifacts across pools with no crossing involved. Or it could be no new mechanism at all: the preceding step writes a handoff into something durable — an attachment on a work item (`28-arch-work-record`) is the obvious candidate — and the next instance reads it, registering the result exactly like any other read. The second is cheaper and fits what already exists, which is a reason to prefer investigating it first, not a reason to consider it settled.

This is not the fork/join-versus-continuation question (`22-arch-cognition/08`). That one governs whether sibling instances see each other's crossings, which is pool isolation; it says nothing about how much any single pool starts with, and either recombination model works with a thin or a fat seed.

What the recall policy actually is. Named here as a required, distinct responsibility — arbitrary by design, not yet specified — governing recall and archive transitions; nothing here fixes what triggers either direction.

Whether "not yet taken" is indexable for the generation crossing type the way an unread file or an unretrieved claim is — `04` did not settle this.
