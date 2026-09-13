# Constrained Intelligence Thesis

## TL;DR

The project assumes that a smaller local model can become substantially more useful when the surrounding system manages decomposition, context, memory, verification, and feedback well.

> **Motto:** Spend system design to save model capacity.

## Motivation

A constrained local model cannot reliably hold an entire large repository, a long task history, a complex plan, previous failures, and every relevant architectural decision in one context window.

Attempting to compensate only by increasing context length risks replacing missing information with excessive irrelevant information.

The system should instead reduce the amount of simultaneous reasoning each invocation must perform.

## Where knowledge lives

Four locations, and keeping them apart is what makes the rest of this set possible. The **external world** — the repository, the filesystem, whatever a tool can reach. The **knowledge base** — `03-evidence-belief-and-provenance.md`'s substrate of claims and provenance. The **model's own weights**, argued below. And the **conversation**, which is the only one the other three can enter, and which they enter only by something crossing into it (`04-context-as-governed-resource.md`, The shape of a context).

`04-context-as-governed-resource.md` builds on that enumeration directly: nothing is context until something crosses from one of the first three into the fourth.

## The model's own world model

The model is not only what the working hypothesis below must work around. Its weights are a location where knowledge already lives — a world model, compressed by training into the most efficient form available, carrying broad patterns, facts, and reasoning capability the system did not have to build.

This does not substitute for `03-evidence-belief-and-provenance.md`'s substrate, and the reason is structural, not a matter of degree. The model's world model is general, not particular to this project; frozen at training, not current; and carries no provenance — it cannot say why it believes something or when that belief was last checked. `03`'s knowledge model exists because a working project needs exactly what training-time compression cannot give it: current, local, checkable claims, each with a record of how it came to be believed. "Durable project knowledge," below, is durable precisely because the model's own knowledge is not — rich, but not this project's, and silent on when it was last true.

## Working hypothesis

Useful capability can emerge from the combination of limited models and stronger external cognitive structure.

That structure includes selective context, bounded cognitive roles, explicit evidence, durable project knowledge, independent review, deterministic tooling, and orchestration that can distribute reasoning across multiple short-lived invocations.

The hypothesis is empirical. It should eventually be tested against simpler approaches.

## Expected consequence

Model quality remains important, but model size should not be the only or primary optimization axis. A system with better context discipline and better verification may outperform a larger but poorly orchestrated one on practical development work.

Early results suggest the advantage may lie as much in damage avoided as in work completed. Two readings fit: scaffolding substitutes for capacity, or it bounds what capacity can spoil. They differ in whether the benefit survives a rise in model capability, which is not yet known.

**One observation bears on that, for one class of scaffolding only.** This project is operated by hand as a knowledge base, with no context manager, by a model capable enough not to need one — and a weaker model manifestly cannot do the same (`23-arch-context-management/02-context-as-experimental-surface.md`, Policy adequacy is model-dependent). For *context management*, that points at the first reading: the scaffolding substitutes for capacity, and its benefit shrinks as capability rises.

It settles nothing about the second reading, because it concerns the wrong class. Whether verification, invariant enforcement and independent review still earn their cost against a more capable model is untouched — a model that needs no help finding its material may still need preventing from acting on a bad conclusion. The two classes should be expected to differ, which is worth knowing before either is assessed.

The comparison that would settle the second class is already named: `07-the-integrated-system-and-its-operator.md` asks whether restraint — keeping changes narrow, leaving the operator able to question the work — comes from the model or from the harness around it. No new experiment needs designing for this document.

Any comparison here is assembly against assembly. A scaffolded small model set against a bare large one measures two configurations, not scaffolding against size (`07-the-integrated-system-and-its-operator.md`).

## Where the overhead exceeds the benefit

Two things constrain the process, and neither is a property of the model. Both are for the architecture to address.

**When to decompose.** Splitting is paid for whether or not it helps, so deciding when to split determines whether the approach pays at all rather than merely tuning it. It cannot be settled by classifying tasks in advance: judging what needs splitting is a judgement about the whole, which is the kind the constraint makes unreliable.

**How the composite is evaluated.** A decomposed process yields parts, each checkable against its own criterion. Whether the parts together are what was asked for is not checkable the same way, and that gap does not narrow as the pieces get smaller. Work is lost either because parts fail to reassemble or because they reassemble into something else — with every part having passed.

Evidence for both is in findings entries 5 and 8, and in entry 9 (§4) for the external work on decomposition depth and its failure modes.

## Open question

The shape is known; the position is not, and position is what a firing rule needs.

What makes a direct attempt count as failed, cheaply enough that the check costs less than the decomposition it triggers — the external work that supplies the "decompose on failure" rule names this exact question as unsolved, because a model judging its own success is unreliable and optimistic (entry 9, §4). And how a composite outcome is evaluated, which is what bounds how far decomposition can usefully be pushed.
