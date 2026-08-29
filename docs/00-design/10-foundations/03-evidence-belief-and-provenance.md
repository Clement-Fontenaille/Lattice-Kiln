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

## Decision

A decision records an accepted course of action and should remain traceable to the evidence and reasoning that supported it.

## Provenance

Provenance connects intent, context, processor invocation, findings, proposals, decisions, effects, observations, evaluations, and promoted system changes.

The long-term expectation is that the system can answer not only "what changed?" but also "why did this change become trusted?"

## Open question

The project must later determine which provenance needs to remain raw, which can be summarized, and how much historical detail is necessary to audit older generations efficiently.
