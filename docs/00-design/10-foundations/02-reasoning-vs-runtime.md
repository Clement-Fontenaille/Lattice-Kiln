# Reasoning and Runtime Boundary

## TL;DR

AI components should be free to reason broadly, but they should not directly define reality.

> **Motto:** The model proposes; the runtime makes it real.

## Motivation

A rigid deterministic workflow can suppress useful reasoning. An unconstrained AI-controlled environment can silently turn assumptions into actions, modify its own evaluation criteria, or create effects that are difficult to audit.

The project therefore separates cognitive freedom from operational authority.

## Cognitive side

Processors and orchestrators may interpret, challenge, investigate, compare, delegate, propose, and revise their own conclusions.

Their reasoning should be shaped primarily by role, objective, context, and capability rather than by a mandatory sequence of workflow states.

## Thinking

Thinking acts with and within a particular instance of the knowledge model — not the schema `03` defines in general, but this project's actual graph, as it stands. A walk's product, in the end, is not one isolated conclusion; it is a **knowledge-state transition**: the instance moves from what it held before to what it holds once the walk's findings, qualifications, and appended corrections are recorded. `03`'s append-only rule (Re-evaluation) is what a transition looks like once written down — the prior state is not overwritten, so the transition itself stays inspectable, not only its result.

The verbs above — interpret, challenge, investigate, compare, revise — are not unstructured. Where a processor is working from provenance-tracked claims (`10-foundations/03-evidence-belief-and-provenance.md`), thinking is walking that graph: reviewing the claims already connected to whatever changed, following each connection outward, and at every stop checking for friction or convergence against what changed. Where either is found, the processor forms the attempted argument it implies, checks whether it holds, and assesses what follows — a demonstration step if it does, a discarded or flagged attempt if it does not — then repeats from there until a stop produces neither, or the walk reaches the edge of what is recorded.

This needs no machinery beyond `03`'s own vocabulary: the substrate supplies the graph and the units a walk forms and checks at each stop; thinking is what a processor does with it. It is, concretely, how a corrected claim's other dependents should be found — walking outward from what changed through what cites it — rather than by the diligence that has substituted for this so far (see `03`, Friction and re-evaluation, the OQ-7 case).

Walking the full graph from every correction does not scale, and nothing here requires a processor to do it unaided. An index of which claims depend on which, so a walk is not rediscovered from scratch each time, fits this document's own split: it is persistence, which the runtime side below already owns (`70-THINKING/ideas.md` I5 is the shape it would take). What belongs on the cognitive side is only that the walk is how a processor thinks, not what makes it fast.

## Runtime side

The runtime owns persistence, effect execution, resource boundaries, tool access, provenance, isolation, and recoverability.

The runtime does not need to understand the full semantic meaning of the work. It must instead enforce the operational laws within which cognition occurs.

## Proposal and effect

A processor may propose changing a file, creating a work item, recording memory, spawning another processor, or modifying system configuration — and, just as much a proposal as any of those, reading a file not yet in context, fetching a source, running a test, or observing a live task. The second kind changes nothing but what is known rather than what exists, but it is still an effect, not a reasoning step, and it crosses the same boundary.

The runtime decides whether the requested effect is representable, permitted, attributable, and reversible where required.

This separation should remain visible in the architecture even if some low-risk operations are later streamlined.

A conclusion thinking reaches — a demonstration step that holds, a qualification, a requalified claim — is exactly this kind of proposal, not yet an effect. Recording it, appending it to provenance, is the runtime's act; thinking only produces what gets proposed.

## Feedback

Doing produces knowledge-state transitions too, not only thinking — but at the border, not internally: an observation crossing in from outside, an effect crossing out into the world and being recorded as having happened, rather than a reorganization of what the instance already holds. Neither side is the intent by default. Casting doing as thinking's service — fetch this so a walk can resume — is only one shape a task takes; a task can just as easily be doing's, with thinking called in only to check what is about to happen against what is already known. Which side drives is a property of the work's intent (`20-cognitive-architecture/01-work-intent-and-task-model.md`), not something this document should assume.

Investigation is a task, not an act on one side of this boundary — it needs both, and conflating it with either half loses what makes it work. The seeking — reading a file not yet in context, fetching a primary source, running a test, observing a live task — is doing: an effect the runtime executes, no different in kind from changing a file or spawning a processor, even though it changes nothing but what is known. What doing returns is raw, an observation (`03`), not yet knowledge. Turning it into knowledge — connecting it to what is already held, forming and checking the attempted argument it enables — is thinking's half; the runtime delivers what was fetched, it does not interpret it. Cognitive side's "investigate" names the whole task: propose the seeking, then reason over what comes back. Neither half alone is investigation.

This is the bridge Thinking needs and does not supply on its own. A walk stalls exactly where re-evaluation needs "what the record does not yet have" (`03`, Re-evaluation) — a closer read of a source, new evidence, a re-derivation the substrate cannot produce from what it already holds. That need becomes a proposal, same as any other; the runtime executes it; and the result re-enters the substrate as a new observation or piece of evidence (`03`), carrying whatever mode of acquisition the act that produced it earns: read if fetched from a written source, tested if from a constructed run, operated if from real task execution. The walk that stalled can now resume, but resuming is not automatic — the new material is raw until thinking forms and checks what it implies, the same as any other evidence.

The bridge runs the other way just as often, and it is not the exception. A proposed effect can need checking against what is already known before the runtime executes it — this change conflicts with an existing constraint, this file was already flagged in a correction — and that check is thinking's, called in service of doing rather than the reverse. Nothing here should read as doing being the subordinate half; it depends on which side the task's actual intent sits on.

The ETH correction (`03`, Friction and re-evaluation) is this loop already closed once, by hand, with both halves visible in hindsight. Re-evaluation there did not resolve from what was already recorded; it required rereading the paper. The reread text was doing's product, raw. Recognizing that it contradicted the authorship reading, and building the corrected claim from that recognition, was thinking's. Nothing separated the two until now; it read as if re-evaluation simply happened, in one motion.

## Open question

The exact level of runtime validation is not yet settled. Too little validation makes system evolution unsafe; too much semantic validation risks recreating a rigid workflow engine.

Where a walk that never produces a fixed point — friction or convergence keeps recurring without settling — is deemed to have reached a conclusion anyway is also unresolved. Thinking probably needs a stopping bound the same way runtime effects already need a validation boundary; neither side of this document should be the one left unconstrained by default.

How much investigation a stalled walk may trigger on its own — one fetch, or an open-ended chase down a citation trail — before it must stop and report rather than keep proposing, is also unresolved, and needs the same bound Proposal and effect already applies to any other effect.
