# Observability

## TL;DR

The project cannot improve what it cannot reconstruct.

> **Motto:** Record enough to explain the run later.

## Motivation

Project-level learning, system-level tuning, and meta-level evaluation all depend on evidence about how work actually unfolded.

Observability must therefore be introduced before the sophisticated feedback loops exist.

## What should be reconstructable

A future evaluator should be able to understand the original human intent, which processors were invoked, what context they received, what they produced, what tools were used, what effects occurred, what objective signals resulted, and where human corrections entered the process.

The exact storage format can remain simple initially.

## Why this is not just logging

Operational logs answer what happened.

Research-grade observability must also preserve enough structure to relate behavior to hypotheses about the system.

For example, a later experiment may need to compare two context policies or two versions of the orchestrator role.

Milestone 4 (findings-log entry 3) tested this against real runs: unplanned
questions — "did the independent reviewer agree with the objective outcome?",
"which role proposed each refused effect?" — were answerable from stored records
by ad-hoc joins across event kinds. The one failure was instructive: when a
processor's conclusion was recorded as free-text prose only, the reviewer's
verdict was no longer machine-readable and the question degraded to string
matching. The recorded form of an effect must carry its **structured** outcome,
not just a narrative summary, because those cross-record joins are how
not-yet-imagined questions get answered.

## Reconstruction as a safety dependency

Reconstruction carries more weight than its research role alone suggests.

Individually authorized actions can compose into an outcome that no single check was designed to catch. Detecting composed or drifting behavior is only possible against reconstructable history, never against isolated requests evaluated in the moment. Invariant enforcement therefore depends on this capability rather than merely benefiting from it.

The event model must also be able to represent a safety intervention as its own outcome category, distinct from ordinary task failure such as bad output, timeout, or low quality. A loop that cannot tell the two apart may retry a rejected proposal in rephrased form, which is the behavior enforcement exists to prevent rather than to provoke. That category should be traceable and explicitly ineligible for automatic retry.

## Privacy and cost

Full retention of every token forever is unlikely to be desirable.

The project must eventually distinguish short-term forensic detail from long-term summarized evidence.

Under the arrangement adopted on 2026-09-11, this actor's own copy has acquired a second role: it is what outlives curation. Every crossing now registers into `21-arch-knowledge-model` as an Observation, and `22-arch-cognition/05-curation.md` is what later elides some of it. An elided entry stops being something the system knows and stops being available to reason from, but it may still be reconstructable here. That is not a contradiction of eliding it — reasoning and auditing are different uses, which is the same reason the stores were separate to begin with.

This is also why this actor keeps its own copy of artifacts and events rather than reading `21-arch-knowledge-model`'s graph, `23-arch-context-management`'s live record, or `28-arch-work-record`'s items directly. Those three have different lifecycles — a knowledge-model claim persists as curated project memory, a live artifact persists only for its conversation, a work item persists until the work is done and then stops changing — and none of their retention or compression needs match a full historical log's. Sharing a store would also mean every reconstruction query competes with those actors' own query loads, which the naive-default discipline elsewhere in this project (`10-technical/07`) already treats as a cost worth avoiding.

## Open question

Retention strategy, redaction, summarization, and stable event schemas should emerge from the needs of the first feedback experiments rather than be fully designed in advance.
