# Project Management Principles

## TL;DR

Implement only enough architecture to answer the next important question, but preserve enough observability and modularity that later evidence can change the design safely.

> **Motto:** Build to learn; version what is learned.

## Development posture

The project should advance through evidence-producing milestones rather than through completion of a predetermined architecture diagram.

Each implementation phase should create a useful capability and also improve our ability to observe the system. Observability is therefore not a late operational concern; it is a research requirement.

## Scope discipline

Conceptual ambition may remain broad while implementation scope remains narrow.

A later goal such as meta-level feedback should influence what evidence we preserve today, but it should not force us to implement the meta layer before lower-level behavior exists to evaluate.

This distinction allows the project to remain architecturally coherent without becoming over-engineered.

## Decision discipline

Architectural choices should be classified mentally as either foundational constraints, current hypotheses, or implementation conveniences.

Foundational constraints should be rare. Examples include reproducibility, provenance of system evolution, and the separation between AI reasoning and authoritative effects.

Most other decisions should remain replaceable until experiments justify stronger commitment.

This classification is a discipline for human decision-making. It describes how the project intends to hold itself, and it is revisable by the people applying it.

It should not be confused with the invariant layer, which is a different kind of thing: not a posture toward decisions but a set of constraints the running system is mechanically prevented from crossing. A foundational constraint recorded here can be reconsidered in a later conceptual pass. An invariant cannot be reconsidered by the system at all, and is amended only by direct human action outside every loop.

## Progress criterion

A milestone is valuable when it reduces uncertainty, increases usable capability, or makes future evaluation more trustworthy.

Completing more code is not by itself a progress criterion.

## Reversibility

Where practical, system-level changes should be versioned and reversible.

The project should prefer designs that allow old generations, prompts, policies, benchmarks, and processor definitions to be reconstructed rather than overwritten in place.
