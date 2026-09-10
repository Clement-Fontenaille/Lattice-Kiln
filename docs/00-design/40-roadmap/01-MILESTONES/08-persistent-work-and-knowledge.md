# M8 — Persistent work and knowledge

**State:** open. Next after [M7](07-static-supervised-workflow.md).
**Was:** M6, before rework 2
**Design:** [`10-foundations/03-evidence-belief-and-provenance.md`](../../10-foundations/03-evidence-belief-and-provenance.md), [`02-reasoning-vs-runtime.md`](../../10-foundations/02-reasoning-vs-runtime.md), [`05-ephemeral-conversation-curated-memory.md`](../../10-foundations/05-ephemeral-conversation-curated-memory.md)

## What this milestone is

Add enough durable structure for ephemeral processors to cooperate across time.

Intent, work, observations, evidence, findings, proposals, decisions, artifacts,
and memory should be represented only as far as necessary to support real use
cases.

The 2026-09-10 foundations pass gave this milestone a substrate it did not have
when it was written: claim types and their weighing (`03` — Observation, Evidence,
Finding, Decision; Mode of acquisition; Weighing claims), the reasoning that acts
on them (`02` — Thinking, Feedback), and the ephemeral/persistent boundary itself
(`05` — Collapsing, Curated memory). This milestone is where that substrate gets
built, not merely specified further.

## Evidence question

Does the system, given this substrate, hold and correctly use knowledge it did not
derive itself in the same session? Two stages, cheapest first:

1. **Small tests.** A processor reuses a stored finding or decision from an earlier
   run and measurably beats one starting cold — the bar recorded at rework 1,
   still the right shape at small scale.
2. **The corpus sweep.** Feed the system the `70-THINKING/` literature-review
   corpus it did not produce — the F-numbered findings across topics 07 and 08,
   the I-numbered ideas register — and ask whether it can hold that material as
   `03`'s claim types (mostly Read, much of it second-hand), weigh it, and use it
   correctly when a later task calls for it. This is not a synthetic benchmark:
   the corpus already exists, was gathered independently of this milestone, and is
   real data the "curated memory beats conversational accumulation" hypothesis
   (`03-research-and-evaluation-agenda.md`) has never been tested against.
   Registered as a sweep target in
   [`08-next-experiments.md`](../08-next-experiments.md) → E6.

## What it depends on

The ephemerality of processors is the architecture's position, and persistence is
the thing that makes it survivable across sessions. The tension is deliberate —
see
[`05-ephemeral-conversation-curated-memory.md`](../../10-foundations/05-ephemeral-conversation-curated-memory.md),
which now names exactly where the line falls: most of a reasoning episode
collapses and never needs this milestone's machinery at all; only what survives to
be checked and held does.

Two threads land here rather than earlier:

- **The M4/M5 re-test at larger N**, which needs durable work records to be worth
  running. Tracked in [`../00-backlog.md`](../00-backlog.md).
- **Authorship preservation** — work a person did not author is work they do not
  hold ([`10-foundations/07`](../../10-foundations/07-the-integrated-system-and-its-operator.md)).
  What memory retains, and what it therefore relieves the operator of
  understanding, is a question this milestone opens rather than settles.

## Relationship to M9

[M9](09-context-governance-measurement.md) measures whether what this milestone
holds is any good, independently of whether a task using it happened to succeed.
That is a dependency, not a sequencing claim: M9 needs this milestone's substrate
and the corpus sweep's result to have something concrete to measure against,
whatever order the two end up worked in.
