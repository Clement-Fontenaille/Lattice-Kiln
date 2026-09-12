# Observability

## TL;DR

The project cannot improve what it cannot reconstruct. This actor records what happened, generously, and defers deciding what any of it was worth.

> **Motto:** Record enough to explain the run later.

## Status of this document

Reworked 2026-09-12. The original was written before `10-foundations/03`'s conceptual pass and before the architecture band was split, and it had received none of either: it described events and effects with no claim vocabulary at all, while stating a long-term goal — "why did this change become trusted" — that is `03`'s Provenance question word for word.

Its own position also changed underneath it during the 2026-09-11 pass, when every crossing began registering into `21-arch-knowledge-model` and most of it began being swept again. This actor's copy is now what survives that.

Deliberately greedy for the moment. Retention, redaction and summarization are named as open rather than designed, and the reason is given below rather than assumed.

## Motivation

Project-level learning, system-level tuning, and meta-level evaluation all depend on evidence about how work actually unfolded.

Observability must therefore be introduced before the sophisticated feedback loops exist, not alongside them. A loop that starts without a record behind it has nothing to learn from until enough time has passed to accumulate one.

## Record greedily; decide later what it was worth

The costs here are asymmetric, and the asymmetry decides the default.

Recording too much costs storage and some query speed. Both are recoverable: material can be summarized, compressed or discarded at any later point, once something has been learned about which parts were ever consulted. Recording too little costs a question that can never be answered, because nothing regenerates a record that was never written. This is `10-foundations/03`'s argument for keeping a chain's roots raw, applied one layer out — and it is the same reasoning that makes `21-arch-knowledge-model` write every crossing before deciding anything about it.

So the working rule is to record more than seems necessary and to resist the urge to prune early. A retention strategy designed before the first feedback experiment would be designed against guesses about which questions matter, and the whole point of this actor is the questions nobody thought to ask in advance.

This is a decision about sequencing and not a claim that unlimited retention is correct. It will stop being right at some point. What should end it is a measured cost, not an anticipated one.

## What should be reconstructable

A future evaluator should be able to understand the original human intent, which processors were invoked, what they were given, what they produced, what tools were used, what effects occurred, what objective signals resulted, and where human corrections entered the process.

Four things need saying more precisely than that, because the architecture around this document has changed.

**Each turn, not each invocation.** What a processor sees is composed fresh on every turn out of a pool that grew since the last one (`20-arch-runtime.md`, Instantiation, and then a loop). There is no bundle handed over once at the start. So the unit worth recording is a **turn's composition** — what was actually presented to the model at that moment, and what the recall policy held back — rather than a single record of what an instance received when it began.

**Reads as well as effects.** A read is not a typed effect, but it is in the invariant gate's input domain and it has a real footprint (`10-foundations/02`, Qualification 2026-09-11). It has always been required to be observable here; what has changed is that this is now load-bearing rather than incidental. The reason is in the next section but one.

**Knowledge-state transitions.** Every proposal that changes what the project holds — a claim asserted, a qualification appended, a claim requalified, a working compressed to a souvenir, an entry swept — with the processor that proposed it and the grounds it gave (`22-arch-cognition/04-thinking.md`).

**Work transitions.** Every change to a work item, and every recorded conclusion, keeping *answered*, *blocked* and *declined* distinct (`28-arch-work-record`).

**The conditions in force.** Which recall policy, which model, and which configuration were operating while each stretch of history was produced. This is not metadata for tidiness. The record a system accumulates is a product of that system, so a later comparison between policies is never against a neutral corpus, and it needs to know which lineage it is reading. `10-foundations/03` makes the same point about a single claim under the name Scope — the domain it was born into cannot be recovered afterwards, only recorded near the time. The corpus has a scope in that sense, and this is where it is written down. `23-arch-context-management/02-context-as-experimental-surface.md` sets out what follows for comparison.

The exact storage format can remain simple initially.

## Reconstructing knowledge, not only events

"Why did this change become trusted" is not a question about events. It is a question about a claim's provenance, and answering it means walking from the claim back through what it was built on, checking what each parent's source and mode of acquisition were, and finding where a weighing or a qualification changed its standing.

`21-arch-knowledge-model` holds the graph that supports such a walk at its current state. It does not hold the history of how that state was reached, because `10-foundations/03`'s append-only rule keeps corrections visible but keeps them inside the claims themselves. This actor holds the transitions: who proposed what, when, on what grounds, and what the record looked like before and after.

That distinction matters for one class of question in particular. `03` says friction — two claims that each carry enough standing to resist dismissal and still cannot both hold — is usually noticed when a claim is put to load-bearing use, not by scheduled audit. Whether that actually happens, how often, and how long a bad claim survives before something collides with it, are questions about the history of use rather than about the graph. Only this actor can answer them.

The same applies to mode of acquisition. `03` grades a claim's reliability partly by the chain that produced it, and a corpus's overall grade is a property that drifts over time as read and reasoned claims accumulate faster than operated ones. That drift is visible here and nowhere else.

## Why this is not just logging

Operational logs answer what happened.

Research-grade observability must also preserve enough structure to relate behavior to hypotheses about the system.

Milestone 4 (findings-log entry 3) tested this against real runs: unplanned questions — "did the independent reviewer agree with the objective outcome?", "which role proposed each refused effect?" — were answerable from stored records by ad-hoc joins across event kinds. The one failure was instructive. When a processor's conclusion was recorded as free-text prose only, the reviewer's verdict was no longer machine-readable and the question degraded to string matching. The recorded form of an effect must carry its **structured** outcome, not just a narrative summary, because those cross-record joins are how not-yet-imagined questions get answered.

That lesson now extends past effects. A qualification recorded as prose alone has the same defect: "what changed about this claim, and on what grounds" degrades to reading, which does not join across records and does not aggregate. Whatever carries a knowledge-state transition has to name the claim, the kind of change, and the grounds as fields rather than as narration.

## Comparing policies needs recorded compositions

`23-arch-context-management` argues that recall is worth separating from registration because two recall policies over the same pool choose different subsets, which makes them directly comparable while the pool is held constant.

That comparison is only available if what each policy actually presented was recorded. Without per-turn compositions kept here, the comparability is a property of the design rather than a measurement anyone can take. This is the concrete reason the per-turn unit above matters, and it is also the first place the ARES material relocated in F43 applies: that work found keeping every candidate beat selective retention under a strong judge, which is a claim about what should be available to reason from next, and this project cannot check it against its own runs without this record.

## Reconstruction as a safety dependency

Reconstruction carries more weight than its research role alone suggests.

Individually authorized actions can compose into an outcome that no single check was designed to catch. Detecting composed or drifting behavior is only possible against reconstructable history, never against isolated requests evaluated in the moment. Invariant enforcement therefore depends on this capability rather than merely benefiting from it.

This is where recording reads became load-bearing. `25-arch-invariant-layer` requires the gate to evaluate sequences, and the canonical composed outcome is an accumulation of permitted reads followed by one permitted effect that carries the accumulation somewhere it should not go. A history containing only typed effects shows the carrying step with nothing of what filled it, which is the half that determines whether the step mattered. Sequence evaluation runs against what this actor kept, so what this actor omits is invisible to the gate.

The event model must also be able to represent a safety intervention as its own outcome category, distinct from ordinary task failure such as bad output, timeout, or low quality. A loop that cannot tell the two apart may retry a rejected proposal in rephrased form, which is the behavior enforcement exists to prevent rather than to provoke. That category should be traceable and explicitly ineligible for automatic retry.

## Two diagnostics this makes possible

`22-arch-cognition/05-curation.md` records two failure modes for which it proposes no detector. Being greedy here supplies one for each, which is a reason for the greed beyond general caution.

**A sweep that took something needed.** Retention defaults to reachability: an artifact no longer live that no promoted claim cites is removed. The failure case is an artifact whose value is only recognised afterwards. That case looked undetectable, because the evidence it happened went with it — but it went only from `21-arch-knowledge-model`. It is still here. A later pass can ask whether anything swept was subsequently searched for, re-fetched, or re-derived, which is exactly the signal that the reachability rule cut too early.

**A curator that has stopped discriminating.** An over-generous remembrance judgment grows the store without corrupting it, and produces an absence rather than an error. The ratio of registered observations to remembered ones, tracked over time, is a drift signal available here and computable from nothing else.

Neither is proposed as a mechanism. Both are stated so that the material they would need is not discarded before anyone tries.

## Privacy and cost

Full retention of every token forever is not a long-term position, and the greedy default above is explicitly temporary.

The project must eventually distinguish short-term forensic detail from long-term summarized evidence, and redaction is a separate requirement again: a record of real work contains material that should not be retained indefinitely regardless of how useful it would be.

None of that is designed here, for the reason given under Record greedily. What should trigger the design is a measured cost or a concrete privacy requirement, not the anticipation of one.

## Why this actor keeps its own copy

This actor keeps its own copy of artifacts and events rather than reading `21-arch-knowledge-model`'s graph, `23-arch-context-management`'s live record, or `28-arch-work-record`'s items directly.

Those three have different lifecycles. A knowledge-model claim persists as curated project memory, a live artifact persists only while its conversation needs it, a work item persists until the work is done and then stops changing. None of their retention or compression needs match a full historical log's, and a greedy log's needs least of all.

Under the arrangement adopted on 2026-09-11 this became sharper rather than softer. Every crossing registers into `21-arch-knowledge-model` and most of it is swept again once it is no longer live and nothing has built on it. A swept entry stops being something the system knows and stops being available to reason from, while remaining reconstructable here. That is not a contradiction: reasoning and auditing are different uses, and this actor is what makes the sweep safe to perform at all.

Sharing a store would also mean every reconstruction query competes with those actors' own query loads, which the naive-default discipline elsewhere in this project (`10-technical/07`) already treats as a cost worth avoiding.

## Relationships

- **`20-arch-runtime.md`** — emits what this actor records; the loop it describes is the shape the per-turn record follows.
- **`21-arch-knowledge-model`** — holds the current state of the provenance graph; this actor holds the history of how that state was reached, and the entries the sweep removed from it.
- **`23-arch-context-management`** — supplies the per-turn compositions and the live-state transitions that make recall policies comparable.
- **`22-arch-cognition/04-thinking.md`** and **`05-curation.md`** — the source of knowledge-state transitions, and the consumer of the two diagnostics above.
- **`25-arch-invariant-layer`** — depends on this actor for sequence evaluation, reads included.
- **`28-arch-work-record`** — supplies work transitions and recorded conclusions.
- **`27-arch-adaptation-and-evolution`** — every feedback loop's evidence comes from here.

## Open question

Retention strategy, redaction, summarization, and stable event schemas should emerge from the needs of the first feedback experiments rather than be fully designed in advance. The greedy default stands until one of them produces a measured reason to change it.

What a knowledge-state transition looks like as a structured record, given that the M4 lesson says narration will not join across records. `21-arch-knowledge-model`'s own open question about write-time tags is adjacent and probably answered by the same work.

Whether the per-turn composition record should hold what was presented, or a reference plus the policy decision that produced it. The second is far smaller and reconstructs the first only if the pool's own history is complete, which under the sweep it is here and is not in `21-arch-knowledge-model`.
