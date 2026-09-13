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

Who performs this is `22-arch-cognition/04-thinking.md`: a family of processor roles rather than one role or a runtime mechanism, whose membership test is that a processor's product is a proposed mutation of the knowledge model. That test separates thinking from reasoning by which store moves — a chain of thought inside a generation registers an artifact into the live context live set and changes nothing the project holds, while a knowledge-state transition is the knowledge model itself changing. It follows that thinking is invoked rather than ambient, since a proposal has an author and a check where reasoning has neither.

Walking the full graph from every correction does not scale, and nothing here requires a processor to do it unaided. An index of which claims depend on which, so a walk is not rediscovered from scratch each time, fits this document's own split: it is persistence, which the runtime side below already owns (`70-THINKING/ideas.md` I5 is the shape it would take). What belongs on the cognitive side is only that the walk is how a processor thinks, not what makes it fast.

## Runtime side

The runtime owns persistence, effect execution, resource boundaries, tool access, provenance, isolation, and recoverability.

The runtime does not need to understand the full semantic meaning of the work. It must instead enforce the operational laws within which cognition occurs.

## Proposal and effect

A processor may propose changing a file, creating a work item, recording memory, spawning another processor, modifying system configuration, running a test or another subprocess, or reaching outside the workspace to fetch a source or call an external API. Each of these is a typed effect (`10-technical/01-effect-vocabulary.md`) and crosses the same way: proposed, then checked.

Reading something already inside the workspace — a file not yet in context, a prior observation, a piece of provenance — is not a typed effect. **It is not, however, because a read leaves the world untouched.** A read leaves an access record and a modified access time. A query makes its store do work: warming or evicting caches, moving query statistics, holding a connection, competing with every other query for the same capacity. Reading a metered source spends quota that does not come back. And some reads are state transitions outright — reading a queue item can dequeue it, reading a message can mark it read, reading a path can fire a watcher or materialize a lazily-evaluated view. "Changes nothing outside the system" holds only if the world means file contents, which is not what the world is.

So the read/effect boundary is not a distinction in kind. Every runtime-mediated operation changes the world; they differ in **footprint**, which is a gradient rather than a type. What the typed-effect vocabulary enumerates is therefore the set of operations whose footprint this project has decided is worth naming and tracking — not the set that has one. That keeps everything the vocabulary is useful for, since the set stays bounded, closed and verifiable without reasoning. What it gives up is the idea that membership follows from the nature of the operation: membership is a judgment about where tracking pays, revisable on evidence like any other.

Intent does not rescue the boundary either. A write's purpose is its change while a read's change is incidental, but that is a fact about the proposer, and a gate keyed to what a proposer meant is a gate that can be argued with (`25-arch-invariant-layer/01`).

**Not being a typed effect does not put a read outside what may be checked.** Whether reads are gated is a rule to adopt or decline; whether they *can* be is structural, and removing the capability forecloses the rule. The asymmetry decides it: a policy default is reversible, a vocabulary exclusion is not. Adding to the effect vocabulary is a design-set decision rather than an implementation convenience, so a vocabulary that excluded reads by name would make "hold a rule about this read" a change to the system's operational surface instead of a change to its configuration.

The default is therefore permissive rather than structural — **reads pass unless a rule names them** — and the gate keeps a read in its input domain whether or not any rule currently fires on one. One constraint depends on that directly: the invariant layer holds resource ceilings (`06-the-invariant-layer.md`), context is a bounded resource whose ceiling is `04-context-as-governed-resource.md`'s Overload mode, and a read crossing that ceiling is a resource-ceiling matter. A gate that could not see reads could not hold it.

Note that cost points the other way from where it is usually pointed. "Gating every read is expensive" is offered as grounds that reads need not be gated — but load is itself a footprint in the outside world, so the expense is evidence the operation is consequential rather than inert.

Three questions hide behind this one distinction, and separating them is what keeps it usable: whether an operation changes the world outside the system, how large and how reversible that change is, and whether it must be evaluated before it happens rather than merely recorded. For a read the answers are yes, usually-small-and-usually-self-reversing, and policy's choice. Only the second is a real difference from a write, and it is a quantity.

The runtime decides whether the requested effect is representable, permitted, attributable, and reversible where required.

"Where required" concedes what must be conceded: reversibility cannot be demanded of every effect. Some requested changes are irreversible by nature — that is what was asked for, not an accident of execution — and refusing them on reversibility grounds alone would be refusing to do the work itself. What an irreversible effect needs instead is a real risk evaluation: whether this specific change, in this specific context, is worth what it forecloses. That evaluation is not the invariant layer's (`06-the-invariant-layer.md`) to make — the invariant layer holds effects that may never occur regardless of what any loop concludes, and a legitimate irreversible effect is, by definition, not one of those. Risk evaluation for it is reasoning-based and context-grounded instead: thinking's job, weighed the same way any other claim is (`03`, Weighing claims), before the runtime carries it out.

None of those four checks is bureaucratic caution for its own sake. `70-THINKING/01-use-cases.md` (P3) names why directly: **entropy reduction is the product** — what an operator experiences as help is fewer regressions, correct refusals, work that does not need undoing, not raw throughput (`10-foundations/07-the-integrated-system-and-its-operator.md` already states the same commitment in narrower form). A single proposed effect is not judged against that bar directly, and treating it as one would be a category error: an effect's own goal is whatever the task's intent already is (`22-arch-cognition/01-work-intent-and-task-model.md`), and a bug fix's job is to fix the bug, not to reduce entropy. Entropy reduction is the **desired side effect** of executing that goal well, not a competing one — measured across the pattern of effects, not inside any single proposal. This is why reversibility is not one checklist item among four: an effect that turns out wrong and cannot be undone has spread entropy regardless of whether it accomplished what it was proposed to do, and a correct decline reduces entropy while producing no effect at all. This is not a floor beneath a separate ceiling — there is no floor, only the ceiling, read from below (root README): an assembly that regresses on one task in three does not have a high ceiling guarded by a weak floor, it has a lower ceiling than its peak output suggests, because the ceiling is what the assembly reliably delivers, not what it manages once.

This separation should remain visible in the architecture even if some low-risk operations are later streamlined.

A conclusion thinking reaches — a demonstration step that holds, a qualification, a requalified claim — is exactly this kind of proposal, not yet an effect. Recording it, appending it to provenance, is the runtime's act; thinking only produces what gets proposed.

## Feedback

Doing produces knowledge-state transitions too, not only thinking — but at the border, not internally: an observation crossing in from outside, an effect crossing out into the world and being recorded as having happened, rather than a reorganization of what the instance already holds. Neither side is the intent by default. Casting doing as thinking's service — fetch this so a walk can resume — is only one shape a task takes; a task can just as easily be doing's, with thinking called in only to check what is about to happen against what is already known. Which side drives is a property of the work's intent (`22-arch-cognition/01-work-intent-and-task-model.md`), not something this document should assume.

Investigation is a task, not an act on one side of this boundary — it needs both, and conflating it with either half loses what makes it work. The seeking splits the way Proposal and effect above already does: fetching a primary source or running a test is a typed effect, no different in kind from changing a file or spawning a processor; reading a file not yet in context is not an effect at all (`10-technical/01-effect-vocabulary.md` excludes plain reads by name) but is runtime-mediated doing all the same. Either way, what doing returns is raw, an observation (`03`), not yet knowledge. Turning it into knowledge — connecting it to what is already held, forming and checking the attempted argument it enables — is thinking's half; the runtime delivers what was fetched, it does not interpret it. Cognitive side's "investigate" names the whole task: propose the seeking, then reason over what comes back. Neither half alone is investigation.

This is the bridge Thinking needs and does not supply on its own. A walk stalls exactly where re-evaluation needs "what the record does not yet have" (`03`, Re-evaluation) — a closer read of a source, new evidence, a re-derivation the substrate cannot produce from what it already holds. That need crosses into runtime execution — a read if it stays inside the workspace, a typed effect if it reaches outside it, the two separated by footprint rather than by whether there is one (Proposal and effect, above) — and the result re-enters the substrate as a new observation or piece of evidence (`03`), carrying whatever mode of acquisition the act that produced it earns: read if fetched from a written source, tested if from a constructed run, operated if from real task execution. The walk that stalled can now resume, but resuming is not automatic — the new material is raw until thinking forms and checks what it implies, the same as any other evidence.

The bridge runs the other way just as often, and it is not the exception. A proposed effect can need checking against what is already known before the runtime executes it — this change conflicts with an existing constraint, this file was already flagged in a correction — and that check is thinking's, called in service of doing rather than the reverse. Nothing here should read as doing being the subordinate half; it depends on which side the task's actual intent sits on.

The ETH correction (`03`, Friction and re-evaluation) is this loop already closed once, by hand, with both halves visible in hindsight. Re-evaluation there did not resolve from what was already recorded; it required rereading the paper. The reread text was doing's product, raw. Recognizing that it contradicted the authorship reading, and building the corrected claim from that recognition, was thinking's. Nothing separated the two until now; it read as if re-evaluation simply happened, in one motion.

## Open question

**Which rules a configuration should adopt.** Too little validation makes system evolution unsafe; too much semantic validation recreates a rigid workflow engine. Proposal and effect narrows what is at stake here: this is a question about configuration, not about what the framework should be able to express. The second is not a place to economize, so the question is where to set a default rather than what to make possible.

**What a read's permissive default should contain.** "Reads pass unless a rule names them" fixes the shape and not the content, and the granularity a rule may use to name a class of reads — by path, by crossing type, by volume against a ceiling — is equally open.

**Whether footprint admits a usable measure**, given that it rather than kind is what separates a read from a typed effect. A gradient nothing can quantify is not yet an improvement on a binary that could at least be checked. Three partial candidates sit in this set already — volume against a ceiling (`04`, Overload), reversibility class (`10-technical/01`'s open contract on who assigns one), and quota consumed — and nothing establishes that they compose into one quantity.

**Where a walk that never reaches a fixed point is deemed to have concluded.** Friction or convergence can keep recurring without settling. Thinking needs a stopping bound the same way runtime effects need a validation boundary, and neither side of this document should be the one left unconstrained by default.

**How much investigation a stalled walk may trigger on its own** before it must stop and report rather than keep proposing — one fetch, or an open-ended chase down a citation trail. This needs the bound Proposal and effect already applies to any other effect.
