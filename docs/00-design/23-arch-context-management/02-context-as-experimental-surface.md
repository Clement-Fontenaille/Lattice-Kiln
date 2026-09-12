# Context as an Experimental Surface

## TL;DR

The question is not what the recall policy should be. It is what apparatus lets the project find out, for a given model, a given task and a given budget.

> **Motto:** Build the laboratory, not the answer.

## Status of this document

New, 2026-09-12, from a design discussion recorded verbatim in `90-notes/03-context-management-refoundation.md`. It reframes what `01-context-manager.md` leaves open rather than replacing it: that document still holds the actor, its responsibilities and its interactions.

What is adopted here is the framing, the instrumentation requirement, and the interface that keeps policies interchangeable. The specific techniques listed under Axes are **not** adopted — they are named so the shape can accommodate them, which is a different commitment.

## Why this document exists

`01-context-manager.md` has carried "what the recall policy actually is — arbitrary by design, not yet specified" as an open question through several passes. That was read as a gap waiting to be filled by the right answer.

It is not a gap. It is the research object. Nothing available to this project settles, from first principles, which representation finds useful context or which policy selects it — and the honest position is that the project does not know and cannot reason its way to knowing. What it can do is build an arrangement in which candidate answers are implementable, instrumented and comparable.

This is the same posture the rest of the design already takes. `10-foundations/04` asks for a naive default so a smarter version has a baseline to beat. `27-arch-adaptation-and-evolution` treats the recall policy as tunable configuration that feedback may revise on evidence. Neither of those works if the policy is decided in advance by argument.

## What is actually being asked

Stated as problems rather than as a design, because that is what has to be stable while the answers change.

**How does the right material get in front of the model?** Given the current state of a task and everything the project has accumulated, which artifacts should be consulted? This is the central question and it is unsolved.

**How is scope inscribed, concretely?** `10-foundations/03` says a claim's scope must be assessed near its creation because no later reader recovers it. That is a requirement on the record's *format*, not only on somebody's diligence: whatever scope turns out to be, `21-arch-knowledge-model` has to be able to hold it. This question therefore has to be answered before the data format can be, and it is currently answered nowhere.

**What steers the model well?** Which combination of caching, context manipulation, isolation and recall actually results in a processor's request being answered satisfactorily. Note the bar: not "relevant material was retrieved" but "the request was answered". Those come apart, and only the second is worth optimising.

**What has to be true for any of this to be measurable?** Covered under Instrumentation, below.

## Initial selection and topology are different problems

Once an artifact is in hand, the graph says where to go next: parents give provenance, children give dependents, and `10-foundations/03`'s walk is defined over exactly that.

Getting the *first* artifact is a different problem, and the graph cannot help with it. There is no link to follow from a task's current state into a record that has never been visited. That entry step needs something else — similarity, matching, a learned selector, a forced choice over an index — and it is where the difficulty concentrates.

`21-arch-knowledge-model` currently lists Query and Traverse dependents as peer services, which obscures this. They answer different kinds of question and only one of them is open.

## Axes that must stay interchangeable

Named so the shape accommodates them. None is adopted, and the list is not a plan.

**Representation of an artifact.** A dedicated embedding model; representations produced by the reasoning model itself, including from internal states; different serialisations of the same artifact; representations combining content, type, metadata and the context the artifact was produced in.

**Representation of a context.** An embedding of what was actually fed to the model; an aggregate over the artifacts present; an embedding of a whole episode or situation; hierarchical representations that find a situation first and its constituent artifacts second.

The second family carries a hypothesis the first does not, and it is the most interesting thing in the proposal this document comes from: that a *situation* can be retrieved by analogy with the current one, rather than an artifact retrieved by similarity to a query. If it works, past context becomes reachable as a whole without retaining every production context in full, with the graph's explicit links used afterwards to reconstruct the path precisely when that is needed.

**Selection policy.** Classical semantic search; similarity against the current context; combinations of several signals; a policy learned from observed trajectories; iterative selection where each production changes the state the next search runs from; policies using vector representations and graph structure jointly.

**Model.** Each of the above has to be testable against different local models independently, so that a specialised embedding model and the agentic model's own internal representations are comparable.

**Prefix persistence.** Whether the serving arrangement keeps a reusable prefix, which changes what a policy can even be — see `01-context-manager.md`.

## The first candidate: artifact embedding × production-context embedding

Each artifact is indexed by two vectors rather than one — its own content, and the informational situation it was produced in. Retrieval then matches against either or both.

This is the first thing to evaluate, for three reasons.

It is the **minimal testable form of the one genuinely novel hypothesis** in the proposal this document comes from: that a past situation can be retrieved by analogy with the current one, rather than an artifact retrieved by similarity to a query. Testing that does not require episode boundaries, hierarchical representations, or anything learned. It requires a second vector per artifact.

It **contains its own ablation**. Artifact vector alone is ordinary semantic retrieval. Production-context vector alone is pure situation matching. Both together is the candidate. Those three arms plus the permanent naive arm answer, directly, one of the questions the proposal itself posed — whether representing the production context adds anything over representing the artifact in isolation.

And it is **nearly free given what is already built**. At the moment `01-context-manager.md` registers an artifact, the live set is its production context by construction. Nothing new has to be tracked to capture it.

### Four things to pin down first

**What counts as the production context.** The **composition** — what recall actually put in front of the model on that turn — and not the pool snapshot. The model produced the artifact from what it was shown, not from what happened to be tracked, so the composition is what the phrase means.

An earlier draft chose the pool snapshot, on the grounds that the composition is shaped by the recall policy in force and would therefore contaminate the very comparison this framework exists to run. That reasoning is abandoned, because it treats as a defect something that is structural. **The set of state transitions in the knowledge model is a product of the system.** Every artifact in it exists because some policy, some model and some configuration caused a crossing that produced it. No definition of production context escapes that: the pool snapshot is contaminated too, through the model's behaviour rather than through the policy's choices, and the difference is one of degree that does not change the epistemic situation. Once neither option is clean, the tiebreaker is which one represents what it claims to.

**How the two combine.** A weighted sum of two similarity scores, with the weight as the swept parameter, is the recommendation — not because it is the best combiner but because the two single-signal arms are its endpoints. Weight zero and weight one give the ablation from the same mechanism rather than from two separate implementations, so there is one thing to build and nothing to keep in sync. Concatenation hides an equal weighting with no knob; two-stage retrieve-then-rerank is a different experiment worth running later.

**The ablation arms and the sweep are not equally measurable, and the difference is in kind.** The three arms differ categorically — one uses artifact similarity, one situation similarity, one both — so they should produce visibly different *patterns* of which scenarios succeed, which is what a paired per-scenario comparison reads (`27-arch-adaptation-and-evolution/05-experiments-and-candidate-systems.md`, Resolution before precision). Intermediate weight values differ only in degree, so they show up nowhere except in an aggregate, and an aggregate over heterogeneous scenarios is the quantity that experiment section argues against relying on.

So run the three arms and read them per scenario. Treat the weight as something to set from what those arms reveal, not as a parameter to sweep for an optimum — a sweep over a quantity only visible in an average is how noise acquires the shape of evidence.

**What is on the query side, because the pairing is less symmetric than it looks.** At retrieval time the current context is available and can be matched against a stored production context — that is the situation analogy. But nothing on the query side corresponds to artifact *content*, since the artifact is what is being looked for; what plays that role is the task or objective text. So the two signals being combined are two different retrieval modes against two different indexed fields, not two representations of one thing. Saying this plainly matters, because it means the weight is trading off between modes rather than blending views.

**What "better" means.** The bar stated above is that the request was answered, not that relevant material was retrieved, and the attribution stance says to compare in aggregate. That is the expensive distal measure and it needs N. A cheaper proximal signal is available alongside it: whether a retrieved artifact was actually *used* — cited, or appearing in the provenance of what the turn produced. Every retrieval is a datapoint there rather than every task, so it accumulates far faster. It is a weaker signal and should not replace the outcome measure, but it can fail fast, which is what a first candidate most needs.

### What comparison can conclude, once the corpus is a system output

Accepting that the record is produced by the system rather than found bounds what this framework may claim. Three consequences, and none of them is a reason to build it differently.

**Comparisons hold within a corpus lineage.** Policies evaluated over the same lineage are comparable. A policy evaluated over a corpus that another policy built is measuring **transfer** — how well it does on material it did not shape — which is a legitimate and separate question, and easy to mistake for the first one.

**Longitudinal comparison confounds.** Running policy A and then policy B over one growing corpus mixes the policy change with everything else that changed alongside it, corpus size included. Whatever separates them is not attributable to the policy without more care than a before-and-after reading gives.

**What is measured is situated performance, not context-free performance.** The framework can answer whether one policy beats another on the corpus their joint operation produces, which is the operationally relevant question. It cannot answer which policy is best in the abstract, and that question was probably never well posed.

None of this is a new kind of problem here. `10-foundations/03`'s Scope already names it for a single claim: the domain a claim was born into — this host, this model family, the state of the project at that moment — was never fully representable and cannot be recovered later. A corpus has a scope in exactly that sense, and the remedy is the same one `03` prescribes. It has to be recorded as it accumulates rather than reconstructed when someone eventually wants to compare, which means the record must carry which policy, which model and which configuration were in force while each stretch of it was produced.

That costs fields rather than a mechanism. `26-arch-observability` is already greedy and already keeps per-turn compositions, and `27-arch-adaptation-and-evolution`'s generations already name a lineage.

The two lineages are not the same thing, though, and the difference is load-bearing. A **generation** is configuration — roles, orchestration, the recall policy, evaluation setup. A **corpus** is whatever accumulated while that configuration ran. In ordinary operation they move together, which is why a system's evidence about itself is weak. They come apart deliberately when a generation is instantiated fresh without the corpus it was tuned against, which is what `27-arch-adaptation-and-evolution/07-bootstrapper-as-transfer-mechanism.md` does — and that separation is what makes the strongest form of evaluation available at all.

### What it depends on

Nothing here can run until artifacts are registered with representations attached, which is specification work the backlog already carries. This candidate is named now so that work has a target to satisfy rather than a general capability to build.

## Instrumentation

Every selection is an experimental decision and has to be recorded as one: the candidates considered, their scores, the representation used, the budget, what was selected, what was actually transmitted to the model, and what followed.

`26-arch-observability` already carries the requirement that per-turn compositions be recorded, and states that recall's comparability is a property of the design rather than a measurement unless they are. This document's requirement is the same one with more fields, and it is the part with no slack in it: a policy whose selections were not recorded cannot be compared to anything, so the instrumentation is not an accompaniment to the experiment but a precondition for it.

## On attributing outcomes to selections

Determining which artifacts actually contributed to a result is credit assignment, and it is hard. With small task suites and noisy outcomes it cannot be done cleanly per selection.

The position taken is to **not solve it explicitly** and to compare policies against each other instead, letting the difference show rather than tracing which artifact earned which success.

What that comparison should be is per scenario rather than aggregate, for the reason `27-arch-adaptation-and-evolution/05-experiments-and-candidate-systems.md` gives: a suite is a set of distinct measurement points, not samples of one quantity, and averaging across conditions this project's own theory says are heterogeneous estimates something that refers to nothing. Which scenarios flip between two policies is both cheaper to obtain and more useful than a score difference, since it names a condition rather than a magnitude.

The bet still has a cost worth stating. It buys no account of *why* a policy won a scenario — only that it did. Where that becomes limiting, the proximal signal below is the cheaper substitute for attribution rather than attribution itself, and nothing here promises it is sufficient.

## The naive baseline is a permanent arm

`10-technical/07-naive-context-assembly.md`'s deterministic matching is not a starting point to be moved off once something better exists. It stays in the comparison set.

The reason is structural rather than sentimental. Part of what protects the naive-default discipline elsewhere in this project is that the sophisticated alternative does not exist yet. A framework built to host embeddings will acquire an embedding implementation, and that implementation will become the default by gravity rather than by evidence. Keeping the crude arm in every evaluation is what replaces the protection the framework removes.

## Policy adequacy is model-dependent

This project is currently operated by hand as a knowledge base, without a context manager, by a model capable enough not to need one. A less capable model is manifestly not able to do that.

That observation is not incidental. It implies there is no single adequate policy, but rather a **gradient of adequate policies indexed by the model** — and that the mechanisms this actor implements are a system-level prerogative, inspectable and adjustable by the feedback loops (`27-arch-adaptation-and-evolution`), rather than a fixed component specified once.

It also suggests a direction worth recording even though nothing acts on it yet: specific training may be what unlocks decent leverage from the knowledge base, and if it does, the trade it enables is disk space for context — a durable record standing in for what would otherwise have to be held live.

## What this document does not do

It does not choose between RAG, embeddings, structural search and learned selection. Choosing now is exactly the failure it exists to prevent.

It does not commit to building any of the Axes. Adopting the framing costs a document; adopting the list would be the largest scope expansion in this project's history, and each bullet there is a research programme rather than a task.

## Open question

How scope is concretely inscribed, since the data format depends on it and nothing answers it yet.

What the entry step should be, given that initial selection and topology are separate problems and only the first is open.

Whether per-scenario comparison is stable enough to read at one run per arm, or how few repeats are needed to tell a genuinely flipped scenario from a flaky one. `27-arch-adaptation-and-evolution/05` suggests five as the figure for classifying stability and holds that one is valid; neither number is grounded in anything this project has measured.

What the literature already holds on recall under prefix persistence. This project should inherit results rather than rediscover them, and the reading has not been done.

How large the lineage effect actually is. Accepting that the corpus is a system output settles what kind of thing it is, and settles that the composition is the right definition of production context, but it says nothing about magnitude. If a policy's advantage over another turns out to be smaller than the difference between two corpora built by the same policy, the comparison is not usable and nothing here would reveal that in advance.
