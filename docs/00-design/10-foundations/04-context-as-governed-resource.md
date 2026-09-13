# Context as a Governed Resource

## TL;DR

Context should be intentionally assembled for a purpose, measured as a resource, and evaluated as part of system behavior.

> **Motto:** Relevant context beats maximal context.

## Motivation

The local-model constraint makes indiscriminate context accumulation expensive and often counterproductive.

The project therefore treats context as an explicit, assembled object produced for a specific invocation rather than as a transparent dump of everything known.

## Expected behavior

A processor should receive enough information to pursue its objective, but should not automatically inherit the full repository, the full project history, every previous processor conversation, and all persistent memory.

A processor should be able to identify missing context and request more when necessary. (Milestone 4 finding, findings-log entry 5: when this affordance was merely *available* — a processor could emit a context request and the runtime would record it — it went entirely unused across 16 runs, including on a task deliberately starved of a needed file. Being able to ask is not enough; the behaviour has to be prompted or required.)

## Too much is a relation, not a property

A context is never overlarge in itself. It is overlarge **for some assembly** — a body of material that swamps one configuration is unremarkable to another, and the same text can be either depending on what is reading it.

Two consequences follow, and both are practical rather than semantic. A judgement that a context is "too big" is not portable: it holds for the configuration it was made against and must be remade elsewhere. And any measurement of context adequacy identifies a *pair* — this material, that assembly — so annotating material alone produces labels that do not transfer.

This is the same relation `07-the-integrated-system-and-its-operator.md` states for work and difficulty, applied to what a processor is given rather than to what it is asked to do.

## The shape of a context

Nothing is context until it crosses into the discussion. `01` already names four locations where knowledge lives: the external world, the knowledge base (`03`), the model's own weights, and conversation. The first three are never context in their own right — each is only ever a place a **crossing** can reach. A crossing is a single reach across one of those boundaries: a tool call touching the outside world (reading a file, running a test), a retrieval touching `03`'s provenance graph, a generation drawing on the model's weights. What actually enters context is never the thing reached — not the file, not the claim sitting in `03`, not the weights themselves — it is the **artifact** the crossing produces: a tool call's output, a retrieved claim (or a souvenir of one, `03`, Provenance), a generated response. The knowledge base and the external world are, from a context's point of view, the same kind of thing: both are reached, neither is held directly until something crosses.

A context, at any point in an invocation, is the set of artifacts currently live within the discussion — conversation, the fourth location, is the one the other three can only ever cross into. Not every artifact is already a claim in `03`'s sense: a retrieval's output usually already is, pre-weighed by whatever it inherited from the graph; a tool call's output is raw until something turns it into an Observation (`02`, Feedback) and, from there, into whatever claim it becomes; a generated response is raw the same way until it is checked and held as a demonstration step. Coverage and integration, below, apply to whatever is live regardless of which state an artifact is in; `03`'s own apparatus — mode of acquisition, weighing, convergence — applies once an artifact has actually been turned into a claim, not before.

Two things determine whether that set of artifacts serves the assembly it was gathered for, and they are independent of each other:

- **Coverage** — per artifact, whether the objective needs what is present, and whether anything it needs is missing. A property of the selection.
- **Integration** — in aggregate, whether the assembly can actually hold and correctly use what coverage decided to include, regardless of how well-chosen each piece was. A property of the assembly, not the selection (`Too much is a relation, not a property`, above): the same well-chosen set integrates cleanly in one assembly and blurs in another.

A context can fail on either axis without failing on the other. The failure modes below are what each way of failing looks like.

**The two axes do not index the same object**, and three words are needed to say which is which. `00-project/05-vocabulary.md` fixes them: **context** is the model's own production state; the **live set** is the context manager's record of what is in context or is to be placed there this turn; the **turn input** is what is actually transmitted on a given turn.

Coverage applies to two of those, differently. Live-set coverage asks whether anything ever fetched what the objective needs. Turn-input coverage asks whether what was fetched was actually put in front of the model. Those are the two Insufficiencies separated below.

Integration applies to what the assembly holds in one pass, which is the context itself — so Overload is a property of context and never of a live set. That does not make a large live set harmless. The live set tracks what is *in* context: something not recalled after a cache reset has left the discussion and drops out of it, so a live set is not a growing archive that a turn samples from and cannot drift far from what context holds.

What happens to material once it leaves the discussion belongs to `05-ephemeral-conversation-curated-memory.md` rather than here: leaving is the default and entering long-term memory is an act. Where anything is physically held while either happens is architecture's arrangement, not a commitment this layer makes.

Where this document says "context" without qualification below, it means what the assembly is actually working from.

## Failure modes

**Insufficiency.** Coverage failure by omission: material the objective needed is not present. **Evidenced** — the Milestone 4 finding above (`Expected behavior`): a processor deliberately starved of a needed file did not even use the affordance built to ask for it. The system does not reliably notice or act on its own insufficiency unprompted.

**This is two failures rather than one**, because registration and recall are separate steps (`23-arch-context-management`). An artifact enters a live set when a crossing returns it; a policy later decides which of the live set is put in front of the model. Omission can happen at either, and the two are not variants of one problem.

*Never crossed.* Nothing fetched the material, so it is not in the live set at all. The remedy is a crossing — a read, a retrieval. The M4 evidence attaches here: the starved processor's failure was that it never asked.

*Crossed but not recalled.* The material is in the live set and the policy did not present it. The remedy is a change of recall policy, and nothing needs fetching.

The sharper difference is detectability. The second is visible from inside: the live set can be compared against what was composed, and the gap is a fact the record already holds. The first is not, because nothing can be compared against what was never fetched — which is why `Forcing the choice` below needs an index of crossings *not yet taken*, as a structure separate from the live record. Any response to Insufficiency has to say which of the two it addresses: a recall-policy change does nothing for material never fetched, and an extra retrieval does nothing for material already sitting unrecalled.

**Redundancy.** Coverage failure by duplication: material present that restates what the assembly already holds from elsewhere in the same context. **Evidenced** — findings entry 9, §3: repository-level context files that duplicated material already reachable elsewhere in the repository produced no improvement in task success at materially higher cost; stripping the duplicated material before generating the same files reversed the result. Provenance was not the operative variable; duplication was.

Redundancy is not the absence of Convergence (`03`, Friction and re-evaluation). Convergence is independent corroboration between *claims* that do not depend on each other — a property claims can have once artifacts have been turned into them, not artifacts as such — and it strengthens reliability. Redundancy is duplicated *coverage* inside one assembled window, a budget cost with no reliability payoff, and it applies to artifacts whether or not they are claims yet. The two are different axes: a context can hold claims that converge and are also redundant with each other in the same window, or artifacts that never duplicate and never converge either.

Redundancy is also not the same claim as "too much volume." A context can be entirely non-redundant — every artifact covering ground no other one does — and still be too much for a given assembly. That is Overload, below, and it is a different axis, not a restatement of this one.

**Uselessness.** Coverage failure of a third kind: material that is neither needed nor duplicated — irrelevant to the objective on its own terms, but not wasteful the way Redundancy is, because nothing else present is already carrying it. **Predicted, not evidenced.** No result in the corpus isolates irrelevant-but-non-duplicating material from the other three modes. The prediction is that Uselessness is harmless in isolation — one irrelevant paragraph does not itself produce a wrong answer — and becomes harmful only by adding volume that pushes the aggregate toward Overload. If that holds, Uselessness is not a cost in its own right; it is Overload's raw material.

**Overload.** An integration failure, not a coverage failure: the aggregate volume of what coverage selected — however well-chosen, however non-redundant — exceeds what the assembly can correctly integrate in one pass. **Predicted, argued from retrodiction, not directly tested.** This is where the granularity hypothesis lives (`22-arch-cognition/08-decomposition.md`): what varies with capability is the coarsest grain an assembly can integrate correctly, and Overload is what happens above that grain regardless of what the content is. The hypothesis explains observations already in hand — a fixed chain losing to a single pass, a splitting stage bought at high cost for narrow benefit (`08`, Its first result) — without yet having made a prediction that could fail; its named falsifier, E2 (`08-next-experiments.md`), has not been run. Fifty non-redundant, individually relevant facts can still drown a 7B model; if that is true, Overload is real and distinct from Redundancy even though nothing in the corpus isolates it on its own yet.

Only Overload is content-quality-agnostic. Insufficiency, Redundancy, and Uselessness are each about *which* artifacts are present; Overload is about how much is present at all, once coverage has already decided what that is.

The design consequence carried forward from all four: curation quality, not curation quantity or curation authorship, is the thing to govern — and quality now names a specific pair of questions (does this cover what is needed, without duplication or noise; does the resulting whole still fit the assembly) rather than one undifferentiated judgment.

## What is live has to be tracked, not inferred

The shape above only holds if the set of artifacts it describes is a state the system can consult while assembly is happening, not a byproduct left implicit until someone looks. None of the four failure modes are checkable without it. Redundancy needs to compare a candidate artifact against what is already live to know whether it duplicates coverage. Insufficiency needs to compare what is live against what the objective needs to know what is missing. Overload needs a running total against a threshold, not a count taken only after assembly finishes. Uselessness's pertinence judgment is made against the live set, not against the objective in isolation.

This is what the TL;DR already commits to and has not yet cashed out: context "measured as a resource" requires the resource to be explicit. What is currently live — as distinct from anything still on the far side of an uncrossed boundary: a claim still in `03`'s graph, a file untouched in the outside world, a response not yet generated — needs to be a first-class, inspectable record, not an implicit consequence of whatever assembly happened to do. Naming this does not resolve any of the four modes; it is the precondition for any of them being answerable at all.

`70-THINKING/ideas.md` I12 already sketches an account close to this — tracking what is currently fed, what is live versus archived, running cache and compaction cycles — as bookkeeping distinct from judgment. Whether that account is the right one is still open (`How the implementation boundary will be decided`, below); that some record of this kind has to exist is not — without it, the system cannot tell Redundancy, Insufficiency, or nothing-wrong-at-all apart from each other.

## What each failure mode requires

Naming a failure mode is not a fix, and this document does not owe one — only what has to be tracked for the mode to be detectable, and what decision the tracking feeds. How each decision gets executed is architecture's business, the same deferral `03`'s Weighing claims already makes for pertinence.

**Insufficiency** requires tracking coverage against the objective's actual information requirements — and stating that plainly exposes a real gap, because nothing in the design set currently gives an objective's information requirements a trackable shape to compare against. That gap is a *representation* question rather than a judgment one, which is what keeps it architectural rather than instance strategy (contrast `On ownership`, below): deciding whether an objective is satisfied is a processor's, but having something to compare coverage against is a shape the design owes. `22-arch-cognition/01-work-intent-and-task-model.md`'s Intent concept is the nearest candidate, written for a different purpose and never read against this use. The decision it feeds — request more, or proceed — already exists as an affordance (`Expected behavior`, above); the M4 finding is that nothing forces it to fire.

**Redundancy** requires tracking overlap at the level of coverage, not text: two artifacts restating the same finding in different words are redundant even with no shared substring, and two artifacts sharing vocabulary while supporting different conclusions are not. Stating it this way rules out the cheap wrong implementation — a text-deduplication pass would satisfy neither the evidence behind this mode (findings entry 9, §3 turned on duplicated material, not duplicated wording) nor the definition. The decision it feeds is which of an overlapping pair to drop, once one is shown to add nothing the other does not.

**Uselessness** requires tracking per-item pertinence — the same live judgment `03`'s Weighing claims already assigns to architecture rather than resolving itself. The decision it feeds is not simply "filter it out": since Uselessness is predicted harmless alone (Failure modes, above), the real decision is whether it is worth spending judgment budget detecting Uselessness at all, or whether it is cheaper to let it ride and rely on whatever bounds Overload to squeeze it out as a side effect once volume actually crosses the ceiling. That decision is only sound if the harmless-alone prediction holds, which is untested (Open question).

**Overload** requires tracking aggregate volume against the assembly's integration ceiling, through a proxy — and two different constraints can produce that ceiling, only one of which this mode is about. What an assembly can correctly *integrate* is a cognitive constraint and is what Overload names. What the hardware can *hold* is a physical one, far tighter than text size suggests: a KV cache runs to hundreds of kilobytes per thousand tokens for a 7B model against roughly four kilobytes for the same text, two to three orders of magnitude apart.

These are not two ceilings. `07-the-integrated-system-and-its-operator.md` holds that there is **one limit**, reached through whichever component binds first, and that is the right reading here too: the assembly stops working at the lesser of the two, and which one that is is a fact about the configuration rather than about either constraint. The practical consequence is that improving one buys nothing while the other binds. The physical constraint is measurable today and belongs among the invariant layer's resource ceilings (`06-the-invariant-layer.md`); the cognitive one is a property of an assembly rather than a limit anyone sets, and has no operational definition yet (`22-arch-cognition/08-decomposition.md`, Status of this account). This is not a gap with no answer at all: `10-technical/07-naive-context-assembly.md` already has one, naive — token count as the proxy, a flat budget as the threshold — and naming it here credits the naive default with a real stance on this mode, one it does not have on the other three. It also exposes precisely what is naive about it: a flat budget cannot distinguish an assembly with a high ceiling from one with a low one, which is exactly the kind of measurement `Too much is a relation, not a property` (above) already says does not transfer. The decision it feeds — what replaces a flat budget — is not made here.

## The objective itself is not a given

The shape above, the four failure modes, and what each requires all presuppose that the objective handed to context assembly is genuine, unique, and actually needs new work. Real request traffic does not arrive that way — a GitLab-style issue queue mixes real defects with duplicate tickets, user error, and under-specified reports, often indistinguishably at intake. `22-arch-cognition/01-work-intent-and-task-model.md` already names the needed behavior: the system should be able to discover "that the task is based on a false assumption... or that the request already has been satisfied." It states this as a capability, not as something context assembly has to feed — the same gap the M4 finding already exposed for Insufficiency (Expected behavior, above): an affordance nobody feeds does not fire on its own.

Context assembly cannot make either of those judgments itself. Whether an objective has already been satisfied, or rests on a false premise, is a processor's output, reached by reasoning over what it was given (`02-reasoning-vs-runtime.md`, Thinking) — not a property context assembly can compute and decide on its own. What context assembly can and must supply is the material that judgment needs to operate on. For "already satisfied," that means surfacing candidate matches from `03`'s provenance graph — claims that plausibly converge with this objective — as part of what is live, the same way any other retrieval's output is surfaced; whether a candidate genuinely resolves the objective is the processor's call, not context assembly's. For a false premise, or an under-specified request, context assembly has nothing equivalent to surface — the objective's own claim has not yet been weighed (`03`, Weighing claims) — and this document is not the place to resolve that check. It only needs to say plainly that it does not: this document otherwise treats the objective as already validated by the time it reaches context assembly.

**That boundary needs no actor of its own.** Validating an objective requires no mechanism that does not already exist: a processor reasoning over what it was given is what a processor is, recording that a task rests on a false assumption is already a work-record mutation (`10-technical/01-effect-vocabulary.md` type 4), and the candidate matches named above arrive as ordinary retrieval artifacts. What remains is only whether a given system instance commissions a role to do it — a matter of that instance's strategy, covered by the open role vocabulary (`22-arch-cognition/02-processors.md`), rather than an architectural assignment.

What the architecture does owe is that the verdict be recordable distinguishably once reached, which `28-arch-work-record` holds.

One part of it does stay architectural, and it is about representation rather than judgment. If an instance does perform the check, its verdict has to be distinguishable from an ordinary failure to proceed. Milestone 5 recorded exactly that collapse: the orchestrator resolved both "the task rests on a false premise" and "I cannot find a next step" to a generic `blocked`, where the simpler Milestone 4 arms had explicitly declined. `22-arch-cognition/03-orchestrator.md` holds this as an open question about first-class terminal states, and `28-arch-work-record` carries the recorded conclusion — answered, blocked, or declined — that would have to tell them apart.

## Forcing the choice: an index, and arbitration over it

The M4 finding already names the gap (Expected behavior, above): being able to ask is not enough, the behaviour has to be prompted or required. What that leaves unstated is what "required" looks like as a mechanism, and it is not the model spontaneously invoking a tool when it judges itself short — that is the same optional affordance the M4 finding already shows goes unused. A different pattern forces the choice instead: present the model with an indexed menu of candidate crossings not yet taken — a file not yet read, a claim not yet retrieved — and require a selection at a defined point in the flow, rather than leaving the request optional or asking the model to self-assess whether it has enough. This is neither self-report nor judgment of correctness or sufficiency — it is picking from an offered set, a different operation, and this document should not conflate it with either.

**Predicted, not evidenced.** A processor given a forced menu at a defined point selects from it at a materially higher rate than a processor merely permitted to ask. The M4 result (0 of 16 runs used the affordance, including on a task deliberately starved of a needed file) is a fact about that optional condition specifically — it cannot by itself distinguish "the model did not need more" from "the model was never made to choose." The named falsifier: re-run the M4 setup, same deliberately-starved task and model, with a forced-menu condition alongside the original optional-affordance one; if selection rate does not rise, forcing is not the operative variable, and something else — the affordance's visibility, or what using it costs — is.

Making that comparison runnable needs two things not yet named here. **An index** of crossings not yet taken — an unread file, an unretrieved claim, a generation not yet requested — distinct from `What is live has to be tracked, not inferred`'s record of what has already crossed and is live; the index is the broader live set a forced choice draws candidates from, and it has to exist and stay current before any such choice can be posed. **Arbitration** — something has to decide which candidates from the index are offered, in what form, and which of the choices made are honoured; the naive default (`10-technical/07`) already performs a crude, unnamed version of this in its own substring-match step, without framing it as an index or exposing a menu to choose from.

## Context governance

Context governance is the broader responsibility of deciding what information becomes available, what remains hidden unless requested, what is summarized, what source material is preferred, and how context budget is allocated among competing needs.

This responsibility may eventually involve both deterministic retrieval mechanisms and AI-assisted selection.

## Why this deserves first-class treatment

If the orchestrator itself receives unlimited context, the system simply relocates the working-memory problem.

If context is too aggressively filtered, the system becomes confidently incomplete.

The quality of context selection is therefore a major determinant of the whole architecture's effectiveness.

## How the implementation boundary will be decided

Context governance could plausibly live in a dedicated subsystem, a specialized processor role, the orchestrator, or some hybrid.

This set deliberately does not choose. The boundary is left to be discovered per generation, per project, or per hardware profile, by the same mechanism that governs every other system-level weakness: if recurring evidence shows that generalist processors or the orchestrator assemble context poorly, system-level feedback may commission a context-curator role as a candidate change, evaluated and promoted or discarded like any other.

Choosing now would settle by intuition what should be settled by evidence, and would settle it identically for every environment the system might run in.

## A naive default is still required

Deferring the design does not defer the need for a starting behavior.

The system needs some unglamorous, possibly poor, context-assembly behavior on day one. Without it there is no baseline against which a proposed curator's benefit could be measured, and the commissioning decision becomes unevidenced.

The first milestone concerned with context is therefore not "design context governance." It is "establish the naive default and enough measurement to make the commissioning decision answerable."

## Open question

**How context quality is measured independently of task success.** Two components rather than one: coverage, and integration. Neither is measured yet, so the commissioning decision above cannot be made on evidence.

**Whether Uselessness is harmless in isolation.** Failure modes states this as a prediction and nothing has isolated irrelevant-but-non-duplicating material from the other three modes. It decides whether detecting Uselessness is worth spending judgment on at all.

**What an objective's information requirements look like as a trackable object**, so Insufficiency's coverage check has something concrete to compare against. `22-arch-cognition/01`'s Intent concept is the nearest candidate and has not been read against this use. This one is a representation question rather than a judgment question, which is what keeps it architecture's rather than an instance's.

**What replaces a flat token budget as Overload's proxy and threshold**, given that `Too much is a relation, not a property` names precisely why a flat budget cannot be the answer.

**What arbitration over the index should look like**, and whether `10-technical/07`'s crude substring-match step is a legitimate starting version of it or needs replacing outright.

**Whether forcing the choice raises selection rate** over the optional affordance. `Forcing the choice` names the comparison that would check it directly; it has not been run.

**Whether a context curator becomes a bottleneck or a source of systematic blindness once commissioned**, and how either would be detected.
