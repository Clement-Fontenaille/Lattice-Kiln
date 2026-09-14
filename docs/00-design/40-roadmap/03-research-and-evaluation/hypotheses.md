# Research and Evaluation Agenda

## TL;DR

The project should maintain a small set of explicit hypotheses that experiments can confirm, weaken, or reject.

> **Motto:** Architecture earns confidence through comparison.

## Core hypothesis: orchestration can compensate for model limits

We expect that a constrained model surrounded by good decomposition, context selection, verification, and memory can outperform the same model used as a monolithic coding agent.

**Partially tested.** Scaffolded arms have beaten a monolith (findings entries 6, 8). What is not settled is the form of the advantage: a substantial part of the gap is damage the weaker arm caused rather than work it failed to do. Two readings remain open — scaffolding substitutes for capacity, or scaffolding bounds what capacity can spoil — and they differ in whether the benefit survives a rise in model capability.

## Core hypothesis: ephemeral roles improve reasoning quality

We expect that fresh role-specific invocations reduce context pollution and create useful independence.

The competing possibility is that orchestration overhead and lost conversational continuity outweigh the benefit.

**Weakened** (findings entry 5): a fixed chain lost to a single pass at roughly three times the cost, and independent review with no revision path was inert. The hypothesis survives only in the conditional form — roles help where the work exceeds what one invocation can hold — which makes it a special case of the decomposition hypothesis below.

## Core hypothesis: curated memory beats conversational accumulation

We expect that promoting selected knowledge into persistent project memory produces more stable performance than carrying long conversations forward.

The main risk is that the memory curation mechanism becomes a new source of omissions and false certainty.

**Untested.** The 2026-09-10 foundations pass gave the mechanism a precise shape it did not have when this hypothesis was written — Mode of acquisition, Weighing claims, Scope, and Collapsing (`10-foundations/03-evidence-belief-and-provenance.md`, `05-ephemeral-conversation-curated-memory.md`). The main risk named above is exactly what Scope exists to bound, and it is exactly the property `03`'s own construction admits it has not checked against a real case. First test: [E6](00-questions.md), digesting the `70-THINKING/` corpus through the substrate at [M8](../01-MILESTONES/08-persistent-work-and-knowledge.md).

## Core hypothesis: decomposition pays where and only where the work exceeds what the assembly can hold

The candidate account in `22-arch-cognition/08` proposes that what varies with capability is the granularity at which relevant context can be accounted for, and that decomposition is grain-matching.

It is currently a lens rather than a theory: assembled to explain observations already held, and yet to make a prediction that could fail. **The named falsifier** is whether the same information at a coarser grain outperforms it at a finer one with quantity held constant. If those come out equal, the account reduces to *relevant context beats maximal context* and should be retired to it.

The competing risk is that the account addresses the cheaper half. If the binding cost is recombination rather than splitting, a grain-matching rule improves what was never the constraint.

## Core hypothesis: an assembly can be made accessible without being made weaker

We expect that the same assembly can be brought within reach of a less practised operator without lowering what it achieves for a practised one — that accessibility and capability are not traded against each other.

The competing failure mode is stratification: gains that concentrate where practice already exists, so the measured average improves while the spread widens. The test is therefore dispersion across the served population rather than a mean (`10-foundations/07`).

## Core hypothesis: adversarial evaluation reduces self-confirming failure

We expect that independent criticism, objective tooling, and baseline comparison make system-level tuning more reliable.

The main risk is correlated failure when evaluator and optimizer share the same model assumptions.

## Core hypothesis: system generations create cumulative capability

We expect that validated improvements can be encoded into a reproducible generation so that fresh instances start from a better baseline.

The competing failure mode is excessive specialization that makes later generations less transferable.

## Core hypothesis: meta-evaluation improves the quality of evolution

We expect that explicit analysis of metrics, benchmarks, and promotion behavior can detect optimization pathologies that system-level feedback alone misses.

This is one of the highest-risk hypotheses because the meta layer may add complexity without enough practical leverage.

## Evaluation posture

Experiments should include negative results and inconclusive outcomes.

A hypothesis that fails early is useful because it prevents the architecture from accumulating machinery that exists only to preserve an elegant idea.
