# M16 — Bootstrap generation closure

**State:** open. The last milestone in the current sequence.
**Was:** M14, before rework 2
**Design:** [`07-bootstrapper-as-transfer-mechanism.md`](../../30-adaptation-and-evolution/07-bootstrapper-as-transfer-mechanism.md)

## What this milestone is

Promoted system generations should produce reproducible bootstrap artifacts.

A fresh instance should inherit validated system-level learning **without
replaying the full history that discovered it.**

## Why this is the closing milestone

It is the charter's success condition, made checkable:

> Success means that fresh instances can start from accumulated system-level
> learning rather than repeatedly rediscovering the same workflow improvements.

Everything before it produces learning that is, in the end, trapped inside one
installation. This milestone is the one that gets it out.

## What it inherits, unresolved

- **Clean-machine replay** ([M1](completed/01-baseline-environment.md)) was never
  run. Bootstrapping onto a fresh instance is the same test at a larger scale, and
  it will surface the six manual and host-specific breaks M1 enumerated but did
  not fix.
- **Hardware as a variable.** The design set does not currently state which of its
  conclusions depend on host-specific envelope numbers. A bootstrap artifact that
  carries a conclusion whose hardware dependency was never stated will transfer a
  result that does not hold. Both items are in
  [`../00-backlog.md`](../00-backlog.md).
- **The editor-agent frontend choice**, deferred from M1, is owned by the
  bootstrapper design and lands here at the latest.

## Evidence question

*Not yet stated.* The natural one — does a fresh instance seeded from a bootstrap
artifact outperform one starting cold, on the same suite — is close to
[M13](13-reproducible-generations-and-promotion.md)'s, which is a reason to state
them together.
