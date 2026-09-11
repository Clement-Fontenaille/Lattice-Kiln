# Open Questions Register

## TL;DR

Unresolved questions are first-class project state. They should remain visible until evidence or explicit design work closes them.

> **Motto:** Unknown is better than silently assumed.

## Work representation

How much structure does persistent work need before structure starts constraining reasoning?

Should work units be explicit persistent objects or temporary orchestration constructs?

How should intent survive rewriting, merging, or abandonment of derived tasks?

## Processor architecture

How narrow should processor roles become?

When does role specialization outperform a general-purpose processor?

How independent must adversarial processors be to provide useful disagreement?

Does using different models for different roles produce enough benefit to justify runtime complexity?

What evidence threshold distinguishes commissioning a new role from tuning an existing one? Introducing a new kind of actor changes the system's cognitive shape more than adjusting an existing one's instructions, and probably warrants a higher bar.

## Orchestration

How much context should the orchestrator receive?

Should orchestration sessions persist or be repeatedly reconstructed from curated state?

Can orchestration itself be delegated?

What practical stopping rules prevent useless reasoning loops without reintroducing a rigid workflow?

## Decomposition

What makes a direct attempt count as *failed*, cheaply enough that the check costs less than the decomposition it triggers?

How is a composite outcome evaluated? Parts can each be checked against their own criterion while nothing checks whether they are together what was asked. This is what bounds how far decomposition can usefully be pushed.

Are decomposition and recombination governed by one quantity or two? The candidate account (`22-arch-cognition/08`) assumes one; the observed concentration of cost in aggregation is the reason to doubt it.

Where should the decision to split live? The orchestrator is the obvious owner, but a rule this consequential held by a component that is itself tunable system configuration deserves examination rather than assumption.

What prediction would let the granularity account fail? Until one exists it is a lens, and the architecture is relying on a sketch.

## Capability model (φ)

What information can be extracted about a given model state using a constructed capability projection φ? Before φ can guide decomposition or processor selection, three things must hold in order: it predicts outcomes it was not fit on; it represents the task population it was built from rather than the taxonomy of whichever model generated that population; and it carries to adjacent model states outside its construction set.

Does any candidate φ separate known passes from known failures better than task difficulty alone, using features computable before the task is run? A negative here closes the granularity programme's predictive ambition before the ladder work starts. Origin: `70-THINKING/ideas.md` I9, itself the prior under I6 (upfront complexity evaluator) and I8 (acting on a φ reading).

## Memory and authorship

Is source — human-authored against system-generated — carried adequately by the existing provenance structure, or does it need representation of its own?

What does enforcement mean for a property not amenable to deterministic refusal? Authorship preservation cannot be gated the way an effect can, yet stating it in prose alone makes it a preference.

What should the system do differently on each side of that distinction, once it can see it?

## Runtime boundary

Which low-risk effects can be executed directly?

Which actions should always remain proposals requiring a runtime policy gate?

How should destructive operations, network access, secrets, and system modification be isolated?

## Memory

Who decides that a finding deserves persistence?

How should contradictory memories coexist?

When should memory be revised rather than appended?

How should stale knowledge be detected and retired?

## Context governance

How should relevance be estimated?

Can a context curator become a bottleneck or a source of systematic blindness?

How should processors request missing context?

How do we evaluate context quality independently from final task success? This is now also a prerequisite rather than a later measurement: a convergence or planning artifact authored before implementation is assembled context, and nothing evaluates it if task success is the only signal.

If what makes context costly is redundancy rather than volume (`10-foundations/04`), how is redundancy detected — against what the assembly already holds, not against the material itself?

## Evaluation

Which metrics correlate with meaningful developer value?

How is operator performance measured without collapsing into self-report? Perceived ease is disqualified as evidence, including this project's assessment of its own tooling.

Does spread across the served population measure accessibility, or is it merely the first available proxy? What would distinguish a genuinely accessible assembly from one tested against too narrow a sample of operators?

Does restraint — keeping changes within mandate, leaving the operator able to question the work — come from the model or from the harness around it? The answer decides how much of that requirement has to be built rather than inherited.

How much human evaluation is required?

How can independent evaluators remain sufficiently independent when they use the same underlying model?

What signal would distinguish genuinely independent evaluation from merely different but correlated judgment between two models used for the same role?

How do we detect benchmark overfitting?

## System evolution

What amount of evidence is sufficient to promote a candidate?

How should stochastic variation be handled?

When should multiple competing branches remain alive instead of selecting one winner?

How are regressions weighted against improvements?

## Meta-evaluation

Which evaluation anchors must remain fixed long enough to detect moving-goalpost failures?

Which parts of the evaluation system should themselves evolve?

How do we recognize that the feedback architecture adds more complexity than value?

Does tuning self-referential parameters, such as the evidence bar for role creation, require dedicated oversight? Recorded as resolved: it falls out of self-application of the existing mechanism, a meta level bounded to one generic question, and a non-self-tuned anchor. Retained here as a trace rather than as a live question.

## Invariant layer and enforcement

What actually belongs in the invariant list — specific enough to be checkable, stable enough not to need frequent revision, without being so narrow that it fails to anticipate real failure modes?

Where does the enforcement gate sit relative to the runtime: a component of it, or a layer the runtime is itself subordinate to?

How are resource ceilings represented in the same structure as behavioral constraints, given that they are physical and financial rather than evidentiary?

What do "consecutive" and "correlated" mean precisely for alert accumulation — same role, same loop, same category of violation, or some combination?

Does a single invariant layer serve all system generations and branches, or may branches reasonably hold different invariants? If so, what must remain invariant across all of them regardless?

What does the human-facing escalation protocol look like in practice: who is notified, what state the system is frozen into, and what is required before resumption?

How does this design compare against existing work on corrigibility, scalable oversight, specification gaming, and shutdown and interruptibility? The concept is currently argued from internal consistency rather than grounded in that literature, and is expected to change once it is read against it. The reading pass is scheduled as a Milestone 11 deliverable (moved there from the Milestone 3 completion checklist).

## Bootstrapping

Which parts of a generation belong in scripts, declarative configuration, local knowledge, or external model assets?

How portable must a generation be across machines?

How do we preserve the ability to reproduce an older generation after runtimes and model ecosystems have changed?

Hardware is a variable, not a constant. The inference envelope (Milestone 0) and
the baseline environment (Milestone 1) were both characterised against one host.
What is the replayable procedure that re-runs environment bootstrapping and
re-characterises the envelope on a different machine — GPU, VRAM, CPU, RAM, or
OS/WSL layout changed — and what in the design set is allowed to depend on
envelope numbers that a new host would move? Raised at M0 close; scheduled for
the post-MVP (end-of-Milestone-5) sequence rework.

## Project process

At what point is a conceptual document mature enough to derive technical contracts?

How should experiments that invalidate conceptual assumptions feed back into this documentation set?

What level of historical rationale should remain after a concept is replaced?
