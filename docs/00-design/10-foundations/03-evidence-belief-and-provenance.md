# Evidence, Belief, and Provenance

## TL;DR

Observed facts, interpretations, conclusions, and decisions must not collapse into one undifferentiated memory stream.

> **Motto:** A conclusion is not an observation.

## Motivation

Feedback systems are especially vulnerable to self-reinforcing errors. If an evaluator's interpretation is stored as truth, later evaluators may treat that interpretation as evidence and progressively strengthen a false premise.

The project therefore needs conceptual separation between what happened and what an AI believes happened.

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

## Provenance

Provenance connects intent, context, processor invocation, findings, proposals, decisions, effects, observations, evaluations, promoted system changes — and, across all of them, source.

The long-term expectation is that the system can answer not only "what changed?" but also "why did this change become trusted?"

## Open question

The project must later determine which provenance needs to remain raw, which can be summarized, and how much historical detail is necessary to audit older generations efficiently.

Whether source is adequately carried by the existing structure or needs representation of its own, and what the system should do differently on each side of the distinction once it can see it.
