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

A processor may propose changing a file, creating a work item, recording memory, spawning another processor, modifying system configuration, running a test or another subprocess, or reaching outside the workspace to fetch a source or call an external API. Each of these is a typed effect (`10-technical/01-effect-vocabulary.md`) and crosses the same way: proposed, then checked. Reading something already inside the workspace — a file not yet in context, a prior observation, a piece of provenance — does not cross the same way. The effect vocabulary excludes plain reads by name: they are runtime-mediated and observable, but the invariant gate does not evaluate them, because gating every read would recreate exactly the rigid workflow engine this document exists to prevent. Doing is broader than effect; a read is doing without being gated as one.

The runtime decides whether the requested effect is representable, permitted, attributable, and reversible where required.

"Where required" concedes what must be conceded: reversibility cannot be demanded of every effect. Some requested changes are irreversible by nature — that is what was asked for, not an accident of execution — and refusing them on reversibility grounds alone would be refusing to do the work itself. What an irreversible effect needs instead is a real risk evaluation: whether this specific change, in this specific context, is worth what it forecloses. That evaluation is not the invariant layer's (`06-the-invariant-layer.md`) to make — the invariant layer holds effects that may never occur regardless of what any loop concludes, and a legitimate irreversible effect is, by definition, not one of those. Risk evaluation for it is reasoning-based and context-grounded instead: thinking's job, weighed the same way any other claim is (`03`, Weighing claims), before the runtime carries it out.

None of those four checks is bureaucratic caution for its own sake. `70-THINKING/01-use-cases.md` (P3) names why directly: **entropy reduction is the product** — what an operator experiences as help is fewer regressions, correct refusals, work that does not need undoing, not raw throughput (`10-foundations/07-the-integrated-system-and-its-operator.md` already states the same commitment in narrower form). A single proposed effect is not judged against that bar directly, and treating it as one would be a category error: an effect's own goal is whatever the task's intent already is (`20-cognitive-architecture/01-work-intent-and-task-model.md`), and a bug fix's job is to fix the bug, not to reduce entropy. Entropy reduction is the **desired side effect** of executing that goal well, not a competing one — measured across the pattern of effects, not inside any single proposal. This is why reversibility is not one checklist item among four: an effect that turns out wrong and cannot be undone has spread entropy regardless of whether it accomplished what it was proposed to do, and a correct decline reduces entropy while producing no effect at all. This is not a floor beneath a separate ceiling — there is no floor, only the ceiling, read from below (root README): an assembly that regresses on one task in three does not have a high ceiling guarded by a weak floor, it has a lower ceiling than its peak output suggests, because the ceiling is what the assembly reliably delivers, not what it manages once.

This separation should remain visible in the architecture even if some low-risk operations are later streamlined.

A conclusion thinking reaches — a demonstration step that holds, a qualification, a requalified claim — is exactly this kind of proposal, not yet an effect. Recording it, appending it to provenance, is the runtime's act; thinking only produces what gets proposed.

## Feedback

Doing produces knowledge-state transitions too, not only thinking — but at the border, not internally: an observation crossing in from outside, an effect crossing out into the world and being recorded as having happened, rather than a reorganization of what the instance already holds. Neither side is the intent by default. Casting doing as thinking's service — fetch this so a walk can resume — is only one shape a task takes; a task can just as easily be doing's, with thinking called in only to check what is about to happen against what is already known. Which side drives is a property of the work's intent (`20-cognitive-architecture/01-work-intent-and-task-model.md`), not something this document should assume.

Investigation is a task, not an act on one side of this boundary — it needs both, and conflating it with either half loses what makes it work. The seeking splits the way Proposal and effect above already does: fetching a primary source or running a test is a typed effect, no different in kind from changing a file or spawning a processor; reading a file not yet in context is not an effect at all (`10-technical/01-effect-vocabulary.md` excludes plain reads by name) but is runtime-mediated doing all the same. Either way, what doing returns is raw, an observation (`03`), not yet knowledge. Turning it into knowledge — connecting it to what is already held, forming and checking the attempted argument it enables — is thinking's half; the runtime delivers what was fetched, it does not interpret it. Cognitive side's "investigate" names the whole task: propose the seeking, then reason over what comes back. Neither half alone is investigation.

This is the bridge Thinking needs and does not supply on its own. A walk stalls exactly where re-evaluation needs "what the record does not yet have" (`03`, Re-evaluation) — a closer read of a source, new evidence, a re-derivation the substrate cannot produce from what it already holds. That need crosses into runtime execution — a read if it stays inside the workspace, a typed effect if it reaches outside it or changes state — and the result re-enters the substrate as a new observation or piece of evidence (`03`), carrying whatever mode of acquisition the act that produced it earns: read if fetched from a written source, tested if from a constructed run, operated if from real task execution. The walk that stalled can now resume, but resuming is not automatic — the new material is raw until thinking forms and checks what it implies, the same as any other evidence.

The bridge runs the other way just as often, and it is not the exception. A proposed effect can need checking against what is already known before the runtime executes it — this change conflicts with an existing constraint, this file was already flagged in a correction — and that check is thinking's, called in service of doing rather than the reverse. Nothing here should read as doing being the subordinate half; it depends on which side the task's actual intent sits on.

The ETH correction (`03`, Friction and re-evaluation) is this loop already closed once, by hand, with both halves visible in hindsight. Re-evaluation there did not resolve from what was already recorded; it required rereading the paper. The reread text was doing's product, raw. Recognizing that it contradicted the authorship reading, and building the corrected claim from that recognition, was thinking's. Nothing separated the two until now; it read as if re-evaluation simply happened, in one motion.

## Open question

The exact level of runtime validation is not yet settled. Too little validation makes system evolution unsafe; too much semantic validation risks recreating a rigid workflow engine.

Where a walk that never produces a fixed point — friction or convergence keeps recurring without settling — is deemed to have reached a conclusion anyway is also unresolved. Thinking probably needs a stopping bound the same way runtime effects already need a validation boundary; neither side of this document should be the one left unconstrained by default.

How much investigation a stalled walk may trigger on its own — one fetch, or an open-ended chase down a citation trail — before it must stop and report rather than keep proposing, is also unresolved, and needs the same bound Proposal and effect already applies to any other effect.
