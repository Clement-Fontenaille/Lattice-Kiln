# Capabilities and Authority

## TL;DR

Knowing how to request an action is not the same as being authorized to make that action real.

> **Motto:** Capability enables proposals; authority governs effects.

## Motivation

The system needs flexibility to introduce new processor roles without hardcoding every role into the runtime.

A capability model provides a stable way to describe what kinds of operations a processor may request.

## Capability concept

Capabilities may cover areas such as workspace access, repository inspection, file modification, process execution, task manipulation, processor invocation, memory proposals, or system experimentation.

Capabilities describe available operations, not a guaranteed right to perform arbitrary effects.

**On that list.** It was written before the effect vocabulary existed, and it is one of three overlapping lists `10-technical/01-effect-vocabulary.md` later reconciled into nine types. It should be read as the areas a policy concerns itself with, not as the enumeration — the enumeration is the effect vocabulary's, and a capability policy is expressed over that. Two of the areas have since acquired owners worth naming: memory proposals are proposals to `21-arch-knowledge-model`, which only a thinking processor makes (`22-arch-cognition/04-thinking.md`), and task manipulation is work-record mutation against `28-arch-work-record`.

## Reads, and where the permissive default lives

A read is not a typed effect, and it is still something an actor may or may not be allowed to perform. `10-foundations/02`'s 2026-09-11 Qualification withdrew the claim that reads are outside what may be checked, and `25-arch-invariant-layer` now carries reads in the gate's input domain — but the question of what *ordinarily* happens to a read is a policy question, which makes it this document's.

The default is permissive: reads pass unless a rule names them. That is a configuration this model expresses, not a property of reads, and it is stated as a default precisely so that it can be changed without anything structural having to move.

What granularity a rule may use to name a class of reads — by path, by crossing type, by volume against a ceiling — is unresolved, and is the same open question `10-foundations/02` holds from the foundational side.

## Authority

The runtime remains responsible for interpreting a requested operation under the current policy.

A reviewer may be allowed to inspect files but not modify them. An implementer may be allowed to propose and perform bounded workspace changes. A system-level optimizer may be able to create candidate configurations without being able to promote them into the trusted baseline.

**The engine that applies this is not here.** It sits with the other non-adjustable mechanisms in `25-arch-invariant-layer`, for the same reason the gate does: a capability engine a loop could remove or route around would gate nothing. What stays in this document is the **model** — what capabilities are, how they are keyed, what a policy may say — and the policy content itself is configuration that system-level feedback revises (`27-arch-adaptation-and-evolution/02`).

That split is the same one `22-arch-cognition/01-work-intent-and-task-model.md` has with `28-arch-work-record`: a document defining a vocabulary, and an actor elsewhere realizing it. It is also the reason the sentence below about not being a floor is exactly right and needs no softening — the policy is adjustable, which is what disqualifies it from being a floor, while the machinery applying it is not adjustable at all.

## Why the distinction matters

Without this separation, role definitions become entangled with runtime security and system governance.

With it, roles can evolve experimentally while operational boundaries remain explicit.

## What this model does not provide

Capability and authority govern what a given actor may request under current policy, and that policy is legitimately adjustable as the system learns.

They are therefore not a floor. A separate, non-adjustable check sits beneath them, testing whether an effect is permissible at all rather than whether this actor is presently authorized to request it. An effect must pass both, and passing capability gating is not evidence of passing that check.

The two also differ in what they are keyed to. Capabilities are described per role, which works because policy can be revised as roles are added. The invariant check cannot be keyed to roles at all, since the role vocabulary is deliberately open-ended; it binds effects instead.

Neither of them answers a third question, and it is worth naming here so that this model is not asked to carry it. **Whether an effect is worth what it forecloses** is not a permission question. An effect can be requestable by this actor, permissible in general, and still a bad idea in this particular situation — most obviously when it is irreversible by nature, which `10-foundations/02` says cannot be refused on reversibility grounds alone without refusing the work itself. That judgment is reasoning-based, belongs to `22-arch-cognition/04-thinking.md`, and happens while the proposal is being formed rather than as a stage in the gating path. `25-arch-invariant-layer` sets out why it must sit upstream rather than inside the pipeline.

So: this model asks whether the actor may request it, the invariant gate asks whether it may happen at all, and thinking asks whether it should. Three questions, three owners, and only the first two are gates.

## A fourth question, which this model does not yet answer

There is one more, and the three-question framing above made it harder to see by looking complete. **Is this within what was asked for?**

`10-foundations/07` names this document as the destination for it — "scope declared and checked belongs with the capability and authority model" — and nothing here currently implements it. The failure mode that commitment exists to prevent is stated there precisely: work beyond the mandate it was given, "including where each step past it is locally justified by the last."

That is not a capability question and capability cannot be stretched to cover it, because the two are keyed to different things. A **capability** is keyed to the actor, set by policy, and evaluated per effect: an implementer may perform bounded workspace changes. A **declared scope** is keyed to the work item, declared per task, and evaluated against what was actually touched. Every step of a drift past the mandate can sit inside capability while the aggregate sits outside the mandate, and a per-effect check keyed to the actor will see nothing wrong at any point.

`25-arch-invariant-layer` already states the property that makes this structural rather than an oversight: capability gating evaluates one proposed effect at a time, and a sequence of individually authorized actions can assemble into an outcome no single check was designed to catch. That observation was made about invariant enforcement and applies here unchanged; the line between it and `07`'s commitment had not been drawn.

**It is authority's rather than capability's**, which is why it belongs in this document despite needing something this document does not have. Authority is already the dynamic half — the runtime interpreting a requested operation under current policy — while capability is the static description of what a role may ask for. A mandate is dynamic in the same way, and adjustable per task.

**It is not the invariant layer's**, and the distinction matters. Mandates differ per work item and are set by whoever asked for the work. A mechanism holding something adjustable would not be the invariant layer, whose defining property is that no loop may write to it.

What would have to exist, stated as shape rather than mechanism: a **declared scope carried on the work item** — which makes it `28-arch-work-record`'s to hold, since that actor holds the work item and its formulation — and a **comparison against what was actually touched**, which has to be aggregate over a sequence rather than per effect.

### The shape it takes

**Scope is a task-level property, expressed in natural language.** It cannot be fixed per role, because the same role does differently-bounded work from one task to the next, and it cannot be enumerated in advance, because what a change is allowed to reach is a statement about this piece of work. The artifacts where the boundary matters most are the ones where drift is cheapest and least visible: specification documents, technical documentation, internal APIs.

**Most scopes are implicit and have to be derived.** An operator rarely states one. A request to add another output format to a CLI tool carries its boundary without anyone writing it down: the user-interface specification and the functional tests around it are in play, the web API documentation is not. Nothing said so; it follows from what the task is and how the system is arranged.

Where the operator *does* indicate a boundary, that indication is carried into the derived scope and governs it. Explicit beats derived; the derivation fills what the operator left unsaid, which is nearly all of it.

That derivation does not conflict with `10-foundations/07`'s requirement that this become "checkable properties of artifacts and effects, never an inference about intent", and the distinction is the whole of why this is workable. **What `07` forbids is inference about a person** — "do what the operator would have wanted" is a psychological prediction, unbounded and unfalsifiable. Deriving that a CLI output format reaches the CLI surface and not the web API docs is an inference about **the work and the structure of the system**. It is checkable by anyone who knows the codebase, it can be shown to be wrong, and it is about artifacts rather than about a mind.

**A derived scope must be recorded and contestable, and this is not optional.** If the system derives a boundary and no one sees it, a wrong derivation does not get caught — it gets ratified, because the end-of-task audit then compares the work against a mandate that was already too wide. Drift becomes legitimate rather than visible, which is the exact failure the check exists to prevent, arriving one step earlier than expected.

`10-foundations/07` already supplies the form this takes: where the system must decide, it yields "with the reasoning that would let the decision be overturned." A derived scope is such a decision, so what is recorded is the boundary *and* what it was derived from — which is what makes it something the operator can find false rather than something they can only accept.

**Under genuine ambiguity, do not derive at all — propose the plausible readings and ask.** This is the other half of the same instruction in `07`, which pairs yielding-with-reasoning against *asking what only the operator can answer*. A scope that follows from the task is the first case. A scope where two defensible readings compete is the second, and the system's job there is not to pick well but to stop picking.

The asking has a required shape. Naming the candidate interpretations — this reaches only the interface and its tests, or it also reaches the adjacent format handlers — is not the same as asking what the scope is. `07` gives the reason both of its modes take the form they do: they place the operator's act where it is cheap for them, answering about intent rather than evaluating an artifact. An open question hands the whole problem back. A derived boundary handed over for validation asks them to evaluate an artifact. A short list of readings asks them the one thing only they can settle.

**Recording the reasoning does not cover this case, which is why it needs naming separately.** A derivation and a coin flip between two readings produce records that look alike: both show a boundary with reasoning attached, and neither shows that a choice was made between defensible alternatives. So an operator reading a recorded derivation has no signal that the confident-looking boundary was one of two. Ambiguity cannot be handled by recording better. It has to be handled by not deciding.

What counts as enough doubt to stop is unset, and the pressure runs one way. `07` observes that refusing costs more than approving, so approval interfaces lean toward assent — mechanically, not morally. The same mechanics apply to a system choosing between asking and proceeding: asking costs a round trip and proceeding looks like progress, so a scope check left to its own judgment will under-detect ambiguity rather than over-detect it.

### Four things this does not need

Followed naively, the arrangement grows heavy: an invariant evaluator inscribing a scope on the task, holding its own copy, and validating every effect against it, with each effect carrying proof that it belongs to the task. Most of that is avoidable, and saying which parts keeps the mechanism small enough to be worth having.

**Attachment costs nothing.** Instantiating a processor binds an objective (`10-technical/01-effect-vocabulary.md` type 6), and that objective comes from a work item. Every effect the instance proposes inherits the work item through the instance that proposed it, which the runtime already tracks for attribution. There is no proof for an effect to carry and no attachment mechanism to build.

**The deriver need not be an invariant processor.** Putting it in that layer would protect it from removal, not from being generous, and a protected-but-lax deriver is worth no more than an unprotected one. What has to be inescapable is narrower: **no unscoped work**. If no scope exists, the check fails closed. Removing the deriver then stops work rather than freeing it, which protects it indirectly and far more cheaply than membership would.

**The check is per task, not per effect.** The reversible majority is compared once, at the end, as an accumulated set against the declaration — which is also the only point at which drift is visible *as* drift rather than as a series of individually unremarkable steps. Only irreversible effects are checked one at a time, before the fact, and those are rare.

**No second copy of the scope is needed.** The worry it answers is real: scope lives on the work item, and work-record mutation is an ordinary gated effect, so a loop could widen its own mandate by mutating it. But widening is an effect like any other and the check sees it — modifying the scope is within the current scope or it is not, exactly as touching the web API documentation is. A scope that permits modifying itself is the thing to exclude by default, and that costs a default rather than a mechanism.

What remains genuinely hard is the end-of-task comparison itself: judging an accumulated set of changes against a natural-language boundary. That is one judgment per task rather than one per effect, which is the difference between a check worth running and one nobody will.

### Can the loop get out from under its own mandate?

Three routes are worth checking explicitly, because a scope check that any of them defeats is decoration.

**Rewriting its own rules.** It cannot. Configuration mutation produces a *candidate* — `10-technical/01-effect-vocabulary.md` type 7 excludes modifying the trusted running configuration in place as not representable, and the path from candidate to trusted is promotion, type 8, which carries the heaviest authority constraints of the nine.

**Commissioning a processor that rewrites scope.** Commissioning is not invoking. The primary loop invokes instances of existing roles (type 6); creating a role definition is system-level feedback's (`27-arch-adaptation-and-evolution/02`), and a commissioned role inherits no exemption in any case — it can only request effects the runtime already checks, so a scope-rewriting effect meets the scope check like any other.

**Manufacturing a task whose scope permits what the current one forbids.** This is the real one, and the naive reading of it succeeds. Creating a work item is an ordinary type-4 mutation. Splitting is explicitly legitimate (`22-arch-cognition/01`). So: split the task, give the child a wider boundary, act under the child. Splitting is allowed and the widening hides inside it.

What closes it is already written and had not been connected. **Scope descends from intent and never appears sideways.** `10-technical/01` type 4 excludes "an intent record's original human-authored content, which is amended only out of band" — intent is not system-writable, and `28-arch-work-record` traces every work item back to one. So a *root* task requires new intent, which only comes from outside, and a loop that authored its own mandate would be authoring the thing that constrains it, which is exactly what `10-foundations/06`'s membership test disqualifies.

From which the rule on splits follows rather than needing separate justification: **a split inherits its parent's scope and may narrow it, never widen it.** A proposed child whose scope is not contained in its parent's is not a split at all. It is a new root task, and it needs intent rather than a parent.

Two honest limits. That containment rule is stated here and enforced nowhere yet. And deciding whether a proposed child's boundary sits inside its parent's is itself a natural-language judgment, so this closure does not reduce the amount of judgment required — it places all of it in the same check rather than leaving a path around it.

### An instance's scope is static

It follows from the above and is worth stating plainly, because a good deal rests on it. Instantiation binds a scope along with the role, objective and capability set, and **a running instance cannot widen its own**. Whatever it was given at invocation, it keeps until it ends.

**An instance that finds it needs to go further must stop rather than grow.** It reports — a recorded conclusion, or a proposed transition on the work item — and something else decides. This is the mechanical form of `10-foundations/07`'s requirement to treat work beyond the mandate as requiring a new one, "including where each step past it is locally justified by the last": the locally-justified step cannot be taken, because taking it is not among the things the instance can do.

**A work item's scope and a running instance's scope can diverge, and that is deliberate.** The item's scope may be re-derived when the item is refined or split, or amended out of band by the operator. That change does not reach instances already running; it applies from the next invocation.

The reason is not defence against a concurrent attacker. It is that **the instance which reports a boundary problem must not be the one that benefits from the answer**. The flow above has an instance stop and report when it finds it needs to reach further; something else then decides, and the item's scope may widen as a result. If a running instance's scope updated live, that report would cost nothing and change nothing — the instance would simply continue under the new boundary, which is the locally-justified-step drift `10-foundations/07` names, reached by an honest route instead of a dishonest one. Static scope is what gives "requires a new mandate" operational force: a new mandate means a new invocation.

The same rule covers the operator amending a mandate mid-run, where waiting for re-instantiation is not obviously required and is adopted anyway. One uniform rule avoids having to tell an operator amendment from a system widening at the moment of application, which would put a judgment inside the path rather than at its edges — and re-instantiating costs little.

**This is affordable because processors are ephemeral.** Staleness is the obvious cost of a static scope, and the remedy is re-instantiation, which this architecture treats as cheap and ordinary (`22-arch-cognition/02-processors.md`). Under a long-lived-agent model the same rule would be expensive, and the trade would need arguing rather than assuming.

**Nested invocation follows the same containment rule as splitting.** A processor invoking another — an implementer requesting an independent review — passes down a scope contained in its own, which it may narrow. The rule is not specific to work items; it is the general statement that mandate flows downward and never widens on the way.

The orchestrator is the one case not settled here. It reads work state across items rather than operating under one, so the natural reading is that it holds the **intent's** scope, with work items below inheriting narrowed versions of it — consistent with mandate descending from intent, but not yet argued.

**The check divides on reversibility, and the two halves sit at opposite ends of a task.**

- **Reversible changes are audited at the end.** Their extent can be compared against the declaration once the work is done, in aggregate, which is the only point at which drift is visible as drift. Auditing late is affordable precisely because the finding still has a remedy: what fell outside can be undone.
- **Irreversible changes are questioned before they happen.** There is no end-of-task remedy, so the check has to precede the effect.

That second placement is the same one already reached from a different direction. `10-foundations/02` requires an irreversible effect to get a risk evaluation before it is proposed, and `25-arch-invariant-layer` explains why such a judgment must sit upstream of the proposal rather than inside the gating path. Scope questioning for an irreversible change lands at exactly that moment, on exactly that argument. Two requirements derived independently, converging on one point in the loop, is a reason to treat that point as real.

**It requires a dedicated processor**, because the comparison is a judgment over natural language and no deterministic check performs it. That processor is an **invariant processor** (`25-arch-invariant-layer`), not one commissioned from the open role vocabulary: a loop able to remove or retune it would be inside the scope it constrains, which is the same test triage passes. Nothing further needs saying about what protects it — that it cannot be deleted, weakened, or routed around follows from belonging to a layer every loop may read and none may write.

Putting a reasoning component in that layer is safe here for a specific reason, and it is a property of scope rather than a general licence. **A scope only ever narrows within capability; it never reaches past it.** An effect still passes capability gating and still passes the gate whatever the scope says, so a scope check that is lax or talked into generosity degrades to no scope check — which is where this project stands today — rather than opening anything. Its failure mode is uselessness, not permission, which is what makes it eligible where a judgment able to *grant* would not be.

The separation that keeps this coherent: **the mandate is adjustable, the checker is not.** What a given task's scope permits changes with every task and is set by whoever asked for the work, which is why mandate content is not invariant-layer material. That a functioning scope check exists, and cannot be removed or routed around by the loops it constrains, is not adjustable by anything inside the system, which is why the checker is.

## Open question

Capability granularity should be derived from actual needs. Overly coarse capabilities weaken control; overly fine capabilities create administrative complexity and can distract the model from the cognitive objective.

Reads are the first concrete instance of that trade-off rather than a separate question. Naming a class of reads by path, by crossing type, or by volume against a ceiling are granularities with very different administrative costs, and the permissive default above means none of them has to be chosen before there is a reason to.

How a declared scope is expressed and compared, per the section above. `10-foundations/07` requires that it become "checkable properties of artifacts and effects, never an inference about intent" — so a comparison of declared scope against what was touched qualifies, and anything of the form "what the operator would have wanted" does not.

Whether mandate conformance is refused, escalated, or merely recorded when it fails. `07` says the requirement "cannot be enforced by deterministic refusal alone", which rules out treating it like the invariant gate, and leaves what it *is* treated like unanswered.

