# M8 — Persistent work and knowledge

**State:** open. Next after [M7](07-static-supervised-workflow.md).
**Was:** M6, before rework 2

## What this milestone is

Add enough durable structure for ephemeral processors to cooperate across time.

Intent, work, observations, evidence, findings, proposals, decisions, artifacts,
and memory should be represented only as far as necessary to support real use
cases.

## Evidence question

*Not yet stated.* The near-term entries carry explicit evidence questions; this one
gains its own as it comes into focus. The bar recorded at rework 1 is a useful
starting point:

> A processor that reuses a stored finding or decision from an earlier run
> measurably beats one starting cold.

That is a "promising signal on 7B" bar rather than a "the code exists" bar, and it
should be sharpened into a real evidence question before this milestone is
decomposed.

## What it depends on

The ephemerality of processors is the architecture's position, and persistence is
the thing that makes it survivable across sessions. The tension is deliberate —
see
[`05-ephemeral-conversation-curated-memory.md`](../../10-foundations/05-ephemeral-conversation-curated-memory.md).

Two threads land here rather than earlier:

- **The M4/M5 re-test at larger N**, which needs durable work records to be worth
  running. Tracked in [`../00-backlog.md`](../00-backlog.md).
- **Authorship preservation** — work a person did not author is work they do not
  hold ([`10-foundations/07`](../../10-foundations/07-the-integrated-system-and-its-operator.md)).
  What memory retains, and what it therefore relieves the operator of
  understanding, is a question this milestone opens rather than settles.
