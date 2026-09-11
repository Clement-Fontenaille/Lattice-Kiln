# Evidence, Belief, and Provenance

## TL;DR

Observed facts, interpretations, conclusions, and decisions must not collapse into one undifferentiated memory stream.

> **Motto:** A conclusion is not an observation.

## Motivation

Feedback systems are especially vulnerable to self-reinforcing errors. If an evaluator's interpretation is stored as truth, later evaluators may treat that interpretation as evidence and progressively strengthen a false premise.

The project therefore needs conceptual separation between what happened and what an AI believes happened.

## Scope

This document defines the substrate — what a claim is, how it is tagged, how it is weighed, how it connects to others — not the procedures that operate on it. Context management (`10-foundations/04-context-as-governed-resource.md`) assembles from this substrate; the cognitive side of `02-reasoning-vs-runtime.md` reasons over what context management assembles; the runtime side of the same document executes and persists the effects that reasoning proposes — and already claims provenance as something it owns and enforces. This document is what makes all three possible; it is not a description of any of them.

## Observation

An observation records an event or directly obtained state: a test failed, a command returned a value, a file changed, a human rejected a result, or a processor produced a recommendation.

## Evidence

Evidence is an observation or collection of observations used to support a claim.

Evidence should retain enough provenance that later processors can inspect its origin or challenge its interpretation.

## Finding

A finding is an interpretation produced by a processor.

Findings can be useful and persistent without being treated as unquestionable facts.

A finding need not be positive. That something is *not* the cause, that an approach does not work, that a hypothesis is eliminated — each is a finding, and together they are often the entire product of an investigation.

This is worth stating because work that changes nothing otherwise records as nothing having happened. An investigation that eliminated four possibilities and left one standing has produced four findings and a direction. A record that counts only artifacts loses all of it, and the effort reads as failure to whoever spent it.

## Decision

A decision records an accepted course of action and should remain traceable to the evidence and reasoning that supported it.

## Source

The four types above answer *what kind of claim is this*. None of them answers *who produced it*, and the two are independent: a human and a processor can both produce a finding, and nothing in the vocabulary tells them apart. Source is therefore an axis across the types, not a fifth type.

A human's contribution enters as an observation — the operator stated something, at a time, in a context. That much is always true, and the list above already contains an instance of it. What the statement *carries* is a separate question. It may be an observation, where the human supplies a fact the system had no access to. It may be a finding, an interpretation the system is free to challenge. It may be a decision, a commitment the system may not quietly revise.

Source also travels. A processor's finding derived from a human-stated constraint is system-produced and human-rooted, and only the provenance chain carries that distinction; a flag on the record alone loses it at one remove.

## Why source is tracked

A system that cannot separate what it produced from what it was given cannot tell whether anything entered that it did not already hold — and where an artifact came from is evidence about how far it can be trusted, since two artifacts of the same kind and comparable coherence can differ entirely in that respect. See `07-the-integrated-system-and-its-operator.md`.

## Mode of acquisition

Source answers *who* produced a claim. It does not answer *how the claim came to be believed* — and that is a separate axis, because a claim's evidentiary weight depends on it.

Four modes exist. **Read** — synthesized from a written source: a paper, a survey, a prior finding. **Reasoned** — synthesized through live argumentation, between people or between a person and a processor, with no preexisting written source behind it: a design discussion, not a sheet. **Tested** — produced by a controlled or synthetic run built to stand in for real conditions: a benchmark, an evaluation suite, a constructed experiment. **Operated** — produced by doing the actual work the project exists to do, on a live task, where the consequences observed are the real consequences and nothing stands in for them.

A read claim needs a further distinction the label alone does not carry: whether what was read is a source's own argument or interpretation, or a report of an event — a measurement, a test, an operation — performed by someone else and reaching this project only through their account of it. The second case is **second-hand**: the underlying event may itself have been reliably operated or tested, but by a chain this project cannot inspect or re-run. `50-findings/09-field-evidence-2026-09.md` is entirely this — vendor benchmarks and one RCT, real measurements taken by other people in other contexts, checkable only by comparing sources against each other or, where the primary publication is reachable, against that.

Mode is assessed at each parent in a claim's provenance, not once for the claim as a whole — provenance is a graph, not a line (see Provenance), and a finding can rest on several evidence items that do not share a mode. Evidence that is second-hand read does not make the finding built from it second-hand: a finding that investigates, verifies, or grades that evidence is the product of the project's own work, whatever the mode of the material underneath it. A finding can inherit different modes from different parents, and carry a mode of its own besides.

Mode of acquisition is independent of the four claim types and of source. A human or a processor can produce a finding by any of the four modes, and an observation can equally be read, reasoned, tested, or operated.

A reasoned observation needs care: Observation is defined as a directly-obtained state, Reasoned as something synthesized through argument, and the two look like they should not combine. They do, at a specific grain, and the grain has two stages, not one.

What is built first is an **attempted argument** — the word matters, since "argument" is already Reasoned mode's own term ("live argumentation, between people or between a person and a processor") and keeps in view that most of these are worked out in discussion, not authored alone and presented finished. It is the particular inferential move offered to connect existing claims which do not connect on their own into a new one. Calling it a demonstration before it is checked would claim success that has not been earned — a demonstration, by the word the root README already uses for it ("each stone an attempted demonstration"), is a proof that holds; what exists at construction time is only the attempt.

It becomes a **demonstration step** — and only then — once Weighing claims' validity dimension has checked it and it holds. What is directly observable, at either stage, is the attempted argument itself: its named inputs, what it claims to connect them into, and, once checked, whether it held. That much is as directly recordable as a test failing. What is not observable, and must actually be checked, is whether it holds — this is exactly where an argument can go wrong without any single finding underneath it being wrong.

"Noticing the symmetry," recorded in that same README, is a live instance of an attempted argument: it connects an existing description of what the context manager is meant to do with an observation of what the literature-review process was actually doing, proposing that they are the same mechanism. What the project's own standing discipline — *notice the symmetry, do not build for it until you can leverage it* — actually holds open is itself a **qualification best left as an open contract** rather than resolved by assertion: it reads as refusing to act on the claim because it has not been checked, and it reads just as well as accepting the claim and refusing only to architect around it yet. This document cannot know which from the note alone, and states the ambiguity rather than picking one — resolving it, if it is ever resolved, is left to whoever reads this later, working against the actual roots, not against this description of them.

Not every claim sorts cleanly. Measuring the project's own hardware (`50-findings/01-m0-inference-envelope.md`) is neither a stand-in — it is the real host — nor the work the project exists to do, since it characterizes the substrate rather than performing a task on it. Left as an open case rather than forced into one of the four; see Open question.

## Why mode of acquisition is tracked

Read, reasoned, and tested claims are all once removed from the setting the project cares about. A read claim inherits whatever framing, incentives, and conditions produced the source it was read from. A reasoned claim inherits whatever the argument that produced it missed, having touched nothing outside itself. A tested claim inherits the fidelity of whatever was built to approximate real conditions — a benchmark is only as informative as its resemblance to the work it stands in for. An operated claim has no stand-in: the task was the real task, and the result is what actually happened.

Mode of acquisition is therefore evidence about the reliability of the chain that produced a claim. It is not itself a weight, and it does not rank claims on its own — see Weighing claims below. `50-findings/09-field-evidence-2026-09.md` already practices this by hand: a claim first recorded from search-engine synthesis rather than primary sources carried an inverted central finding into six places before the chain was checked, and every entry in that file now carries its own reliability grade for exactly this reason. See `27-arch-adaptation-and-evolution/01-project-level-feedback.md` for the operated case at project scope.

An evidence item's mode does not fix its finding's mode. The correction that caught the ETH sign inversion — see Friction and re-evaluation, below — is operated evidence in its own right: not about how well the system performs a coding task, but about the project's own knowledge-integrity process. A corpus with no read claim above the second-hand grade can still contain operated findings.

## Weighing claims

No claim carries a single weight in isolation. What a claim is worth is relative — it emerges from comparing it against another claim, for a particular question, in a particular context — and an absolute score is useful only as far as it helps compute that comparison, never as a settled property of the claim itself. When two claims are each strong enough that the comparison does not resolve, that is not a harder case of this section — see Friction and re-evaluation.

At least three dimensions feed a comparison. **Validity** — the logical strength of the claim's own argument, independent of where it came from; this is the check that promotes an attempted argument to a demonstration step (see Mode of acquisition). **Reliability** — how trustworthy the chain that produced it was; mode of acquisition and source are evidence for this dimension, not weights themselves. **Pertinence** — how the claim relates to the present context and goal, a property of the comparison rather than of the claim alone: the same two claims can outweigh each other differently depending on what is being decided.

`50-findings/09-field-evidence-2026-09.md` already carries reliability and pertinence as separate hand-written lines on every entry — a **Reliability** grade and a **Why it is held** line, kept distinct, predating this document. Validity has no equivalent line there yet; the entries fold it into the reliability prose instead, which suggests it may be the least separable of the three in practice, or simply not yet exercised on its own.

This list is not closed. The project should name a new dimension when a real case shows the existing ones cannot discriminate it, the same discipline `27-arch-adaptation-and-evolution/02-system-level-feedback.md` already uses for commissioning a new cognitive role — reuse what exists until evidence forces an addition, not before.

Which of these dimensions can be recorded once, at the point a claim is produced, and which must be judged live by whatever is asking — pertinence looks like the clearest case of the latter — is an architectural question, not a foundational one.

## Scope

Not every property of a claim can be reconstructed from its provenance, however rich the reader. Mode of acquisition, reliability, even validity can all be recovered later by going back to what a claim was built from (Weighing claims, above; Provenance, souvenir, below). **Scope** cannot. It is the domain a claim was actually born into — this host, this model family, the state of the project at that moment — and that domain was never fully representable to begin with, only assessable, and only close to the time it existed. No later reading of the roots recovers it, because the roots never held it whole.

A claim's scope has to be assessed near its own creation, if at all, not deferred to a future capable reader the way an open contract can be (Friction and re-evaluation, below). Under-assessing it lets a claim silently get used outside where it actually holds; over-assessing it spends effort chasing a completeness no record of this kind can reach. Managing that cost belongs to whatever curates what persists (`05-ephemeral-conversation-curated-memory.md`, Curated memory) — this document only names the property.

## Friction and re-evaluation

A claim is rarely checked by idle audit. It gets checked when it is used — cited as evidence for something else, applied to a new case, put in contact with another claim — and the contact either holds or it does not.

**Friction** is not what Weighing claims already settles. A strong claim outweighing a weak one — a well-replicated tested finding beating one anecdotal read claim — is that section working as intended, not friction. Friction is what is left over: two claims, or a claim and the evidence beneath it, each carrying enough validity, reliability, or pertinence that neither is cheaply dismissed, and still pointing in directions that cannot both hold. Friction is a signal, not a verdict; it marks where a second look is warranted, not which side is wrong.

**Convergence** is contact's other outcome: two independently-produced claims — different source, different chain, sometimes different mode — arrive at the same place without depending on each other. `50-findings/09-field-evidence-2026-09.md` already grades this by hand in two places: §1 credits its claim mainly because three independent vendors are directionally consistent, and §7 names the pattern directly — "positions this project reached independently appear in the field... that convergence is corroborating." Friction demands re-evaluation because something must give; convergence does not — there is nothing to resolve, only something to credit. It does not touch validity, only reliability: independent agreement is evidence the chain is not one idiosyncratic accident.

**Re-evaluation** is the act that follows friction, and it is not a re-weighing. The existing record of validity, reliability, and pertinence was not enough to settle which side holds — that is what made it friction rather than an ordinary comparison — so re-evaluation goes back for what the record does not yet have: a closer read of the source, a re-derivation, new evidence.

This is what actually happened with the ETH result now corrected in `50-findings/09-field-evidence-2026-09.md` §3. Both readings trace to the same paper — same source, same reliability, same mode of acquisition — so nothing in a Weighing-claims comparison could have separated them without reading what the paper actually says. An earlier reading of the paper concluded that authorship was the operative variable — human-written context files help, machine-written ones hurt — and that reading was cited as external evidence for `02-capability-as-granularity.md`'s OQ-7. Citing it for that load-bearing use meant re-engaging with the paper closely enough to state precisely what it supported, and the same paper's own redundancy-ablation result — LLM-generated files with redundant material stripped first improved and beat the human-written ones — directly contradicted the authorship reading. The friction did not arise from a scheduled check; it arose from trying to use the claim for something else. The correction is recorded in `03-how-the-field-frames-it.md` §5, dated 2026-09-04.

A separate, later pass (`06-primary-source-verification.md`, 2026-09-05) re-confirmed this correction and caught several smaller ones, but by a different mechanism: a scheduled audit, run once working retrieval became available, against the standing caveat that the entry was written from search-engine synthesis. Scheduled audit has even coverage and depends on someone remembering to run it. Friction has uneven coverage — it only reaches claims that get used — but needs nothing scheduled: it is a byproduct of the claim doing real work. Neither substitutes for the other.

Re-evaluation's outcome is recorded, not substituted for the claim it revises. The correction is appended — dated, naming what changed and why — and the original stands alongside it rather than being silently rewritten; `50-findings/`'s Addendum convention is this rule already in practice, and it belongs here too. The outcome is usually a requalification, not an inversion: OQ-7 in `02-capability-as-granularity.md` cited the authorship reading as one of its supports, and when the reading was corrected, OQ-7 was not deleted or flipped — it lost that leg, kept its two argued legs, and was marked **Challenged**. The claim's nature did not change; what changed is which grounds it can still stand on. `02-reasoning-vs-runtime.md`'s Thinking names this precisely: the substrate is an instance of this document's schema, and a correction like this one is a knowledge-state transition of that instance — recorded, not overwritten, so the move itself stays inspectable.

This adjustment is a **qualification**, and it does not always resolve into one of this document's existing formal categories the way OQ-7's did. Some qualifications name a genuine ambiguity, and for some of those the document does not merely lack the answer yet — it **cannot** hold the answer, because reality compresses only so far, even as shape, and a note that forced a resolution would be asserting a fidelity no compression at this level actually has. Forcing those into a category — a mode, a dimension, a friction verdict — would assert more than any record at this level of compression could know. For those, the qualification is an **open contract**: a natural-language note that states the ambiguity itself as the content, in the document it concerns, rather than a value chosen from the categories above. `00-project/04-execution-cadence.md` already names this pattern ("every remaining unknown named as an open contract") for specifications; it applies here too, to a claim's status rather than to a spec's shape.

An open contract is not a gap for the next pass to close by writing a better note — some cannot be closed that way at all. What resolves them, where anything does, is not a richer compression but a richer reader: the roots stay traceable (see Provenance, souvenir) precisely so that whatever reads the qualification later — the most capable model available at the time, not this document — can appreciate the shape itself, live, against the actual roots, rather than trusting a note that was never going to hold enough to settle it. This document's job is not to resolve the ambiguity; it is to keep the roots reachable and name the ambiguity honestly enough that a capable reader knows there is real work to do there — the same deferral Weighing claims already makes for pertinence.

Finding OQ-7 as something that needed re-checking was, again, diligence — nothing here names how a corrected claim's other dependents get identified in the first place; see `70-THINKING/ideas.md` I5 (descendant invalidation, not yet adopted) and Open question.

None of this exempts Decision. Mode of acquisition, Weighing claims, and friction are already stated as independent of claim type precisely so a decision is not treated differently from a finding just because it was harder to reach. What *is* different is the revision bar Source already sets: a finding is free to challenge, a decision is a commitment the system may not quietly revise. Friction can reach a decision's supporting evidence exactly as it reached OQ-7's; whether that alone reopens the decision, or whether the higher bar means friction against its grounds only forces re-evaluation of those grounds without automatically reopening the decision itself, is unresolved — see Open question.

Whether noticing friction should be a dedicated act — something that compares a claim against related claims on use — or stays an incidental byproduct of ordinary use, as it was here, is an architectural question; see Open question.

Locating a corrected claim's *other* dependents — not just the one it collided with — needs more than one point of contact: it needs a walk across Provenance, checking each stop for friction or convergence against what changed, forming and checking the attempted argument each implies. That walk is a reasoning procedure, not a substrate fact, and belongs with the cognitive side of `02-reasoning-vs-runtime.md`, not here — see its Thinking section. This document supplies what the walk needs: the graph, attempted argument and demonstration step as the unit it forms and checks at each stop, friction and convergence as what it checks for. See `70-THINKING/ideas.md` I5 for the related, architecture-scoped question of finding dependents efficiently rather than by walking from scratch every time.

## Provenance

Provenance connects intent, context, processor invocation, findings, proposals, decisions, effects, observations, evaluations, promoted system changes, the attempted arguments and the demonstration steps they become once checked, and the friction and convergence events a walk through it can surface — and, across all of them, source and mode of acquisition. Not every attempted argument a walk forms reaches this graph at all: most collapse first, superseded within the same reasoning episode before anything outside it could cite or rely on them (`05-ephemeral-conversation-curated-memory.md`, Collapsing). Only what survives to be checked, held, and used enters here.

Provenance is a graph, not a chain. Several pieces of evidence can converge on one finding — Evidence is already defined above as an observation *or collection of* observations — and one finding can diverge into several downstream findings, proposals, or decisions. It has no cycles: nothing can be justified by something that depends on it. Where this document says *chain* elsewhere, in Mode of acquisition and Weighing claims, it means one path through this graph, not the graph itself, and a claim with more than one parent can inherit a different mode and a different reliability from each, with nothing forcing them to agree. The ETH case in Friction and re-evaluation is this in miniature: the authorship reading and the redundancy reading are siblings, both descending from the same paper, diverging only at the point where each was interpreted.

The long-term expectation is that the system can answer not only "what changed?" but also "why did this change become trusted?"

How much of that needs to stay raw has a criterion, not just a storage budget: raw detail is only required where a claim cannot be reliably reconstructed without it. A chain's roots — the observations and evidence it bottoms out in — need to stay raw, because nothing regenerates an observation that was never kept. A demonstration step built from those roots does not: once it has been checked, its full working can be compressed into a **souvenir** — its named inputs, its conclusion, and, only where the connection between the two is not obvious from those alone, a note of what the argument's shape actually was. A trivial step needs nothing beyond its conclusion; a non-trivial one needs enough of its shape that a later reader is not left re-deriving the same insight from scratch. This is what a reasoning process walking the graph (see Friction and re-evaluation; `02-reasoning-vs-runtime.md`) needs at each stop to decide whether to re-check something, not the full original working.

This is not a proposal untried. This pass's own findings record (`90-notes/02-evidence-provenance-conceptual-pass.md`) has been doing exactly this the whole time, unnamed: its Grounds lines go straight to a pointer where the reasoning is trivial and spell out the argument's shape where it is not — the practice preceded the term, the same way second-hand and convergence did.

"Noticing the symmetry" (Mode of acquisition) is held this way right now, whether or not that was deliberate: what persists is a memory-file summary, not the original session, and that is adequate exactly because the roots it drew on — the design set's description of what the context manager is meant to do, and the literature-review process's own behavior — are still there to re-derive it from. Re-deriving it is how its still-unchecked validity would actually get checked, not by trusting the summary further.

## Open question

Which provenance needs to remain raw has a first answer now: a claim's roots, because nothing regenerates them; a claim's own demonstration step can be held as a souvenir instead, because it stays re-derivable from those roots. Not yet settled: where the line between trivial and non-trivial actually falls when a souvenir is being written, and how much historical detail is necessary to audit older generations efficiently.

Whether source is adequately carried by the existing structure or needs representation of its own, and what the system should do differently on each side of the distinction once it can see it.

Whether mode of acquisition must be recorded explicitly on every observation or can be inferred from the invocation context that produced it is unresolved. So is how validity, reliability, and pertinence should combine into an actual comparison — as a computed function once enough is known about each, or as a judgment made fresh each time a comparison is needed — and which of those two a constrained-size model can actually afford. Where infrastructure self-characterization (`50-findings/01`) belongs among the four modes is also open; it may need a fifth, or it may show that mode is not the same kind of axis for a claim about the project's own substrate as it is for a claim about the work the project does. Whether a claim's own mode and the mode of the evidence beneath it need separate fields, or whether the existing provenance chain already carries this once each finding is linked to the evidence it was built from, is also open.

Whether friction detection should be a dedicated act — something that deliberately compares a claim against related claims — or stays an incidental byproduct of putting claims to load-bearing use, as it was for the ETH correction, is unresolved. A system that never puts claims to such use will only ever catch errors by scheduled audit, never by friction, which is itself worth watching for once the system does real work.

How a corrected claim's dependents get identified in the first place needs a walk across this substrate — see Friction and re-evaluation, and Thinking in `02-reasoning-vs-runtime.md`, where the walk itself is defined. Finding dependents efficiently at scale, rather than by walking from scratch each time, is a further, architecture-scoped question — I5 in `70-THINKING/ideas.md` is the shape an index for this would take, and it has not been adopted. Where a walk that never reaches a fixed point counts as having reached a conclusion is also open in `02`. Nor is it settled whether friction against a decision's supporting evidence is enough on its own to reopen the decision, or whether the decision's higher revision bar requires something more before it does.
