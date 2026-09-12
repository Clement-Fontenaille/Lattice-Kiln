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

## This is also the meta loop's instrument

A second purpose follows from the function above and is worth claiming explicitly, because nothing else in this space provides it.

`03-meta-level-feedback.md` names extraction into predefined scenarios as the strongest evidence available to it: a configuration instantiated fresh, without the corpus it accumulated, run against scenarios defined independently of anything it produced. That is what a bootstrap artifact does. It carries a **generation** — processor roles, orchestration behaviour, the recall policy, evaluation configuration — and it does not carry the accumulated record those were tuned against.

The separation is the point. A generation is configuration; a corpus is what happened to accumulate under it (`06-system-generations.md`). In ordinary operation the two co-vary, which is what makes a system's own evidence about itself weak. Bootstrapping is how they come apart deliberately, and it is therefore not only a deployment mechanism but the one instrument that lets a candidate be judged outside the conditions that produced it.

One consequence for what a bootstrap artifact must not quietly include: any accumulated knowledge-base content. Shipping a corpus alongside a generation would reinstate exactly the coupling this separation exists to break, and would do it invisibly, since the result would still look like a fresh instance.

## Open question

The project still needs to determine how much of a generation should be encoded directly in scripts, how much should live in declarative configuration, and how model/runtime installation differences should be isolated from higher-level cognitive configuration.
