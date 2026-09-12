# Bootstrapper as Transfer Mechanism

## TL;DR

The bootstrapper is how validated system learning becomes available to a fresh environment.

> **Motto:** Do not make each new instance relearn yesterday's lessons.

## Motivation

The project began with a practical need for a scripted local AI development environment.

As the architecture evolved, bootstrapping gained a deeper role.

It becomes the boundary between experimental system evolution and reproducible deployment.

## Expected function

A bootstrap artifact should be able to construct a fresh instance corresponding to a known system generation.

The resulting instance should inherit validated processor roles, orchestration behavior, the recall policy (`23-arch-context-management`), evaluation configuration, and other promoted system-level improvements.

## Auditability

A generated bootstrap artifact should remain traceable to the generation that produced it.

The project should avoid opaque "latest good configuration" state that cannot be reconstructed later.

## Comparison

Reproducible bootstrapping enables whole-system comparison.

Different models or strategies can be instantiated from known baselines, tested independently, and discarded without corrupting the primary development environment.

## A second purpose, noted and deferred

`03-meta-level-feedback.md` names extraction into predefined scenarios as the strongest evidence available to it: a configuration instantiated fresh, without the corpus it accumulated, run against scenarios defined independently of anything it produced. That is structurally what a bootstrap artifact does, since it carries a **generation** — roles, orchestration behaviour, the recall policy, evaluation configuration — and not the accumulated record those were tuned against.

The separation is why it works. A generation is configuration; a corpus is what happened to accumulate under it (`06-system-generations.md`). In ordinary operation the two co-vary, which is what makes a system's own evidence about itself weak, and bootstrapping is how they come apart deliberately.

**This is recorded rather than pursued.** The space of strategies for recombining, validating, testing and replacing systems is large and sits far from what the project is currently deciding. Elaborating it now would be designing against imagined needs. The near-term bar is deliberately simple: **save a system, compare systems, deploy a system.** Everything above is what that bar happens to make possible later, not a requirement placed on it now.

One constraint does follow immediately and costs nothing to honour: a bootstrap artifact must not quietly include accumulated knowledge-base content. Shipping a corpus alongside a generation would reinstate the coupling invisibly, since the result would still look like a fresh instance — and it is far cheaper to keep that line clean from the start than to discover later that every comparison was contaminated.

## Open question

The project still needs to determine how much of a generation should be encoded directly in scripts, how much should live in declarative configuration, and how model/runtime installation differences should be isolated from higher-level cognitive configuration.
