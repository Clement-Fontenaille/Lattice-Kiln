# Research and Evaluation Agenda

## TL;DR

The project should maintain a small set of explicit hypotheses that experiments can confirm, weaken, or reject.

> **Motto:** Architecture earns confidence through comparison.

## Core hypothesis: orchestration can compensate for model limits

We expect that a constrained model surrounded by good decomposition, context selection, verification, and memory can outperform the same model used as a monolithic coding agent.

This must eventually be tested directly.

## Core hypothesis: ephemeral roles improve reasoning quality

We expect that fresh role-specific invocations reduce context pollution and create useful independence.

The competing possibility is that orchestration overhead and lost conversational continuity outweigh the benefit.

## Core hypothesis: curated memory beats conversational accumulation

We expect that promoting selected knowledge into persistent project memory produces more stable performance than carrying long conversations forward.

The main risk is that the memory curation mechanism becomes a new source of omissions and false certainty.

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
