# M8 — Persistent work and knowledge

**State:** open. Next after [M7](completed/07-static-supervised-workflow.md).
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
   (`03-research-and-evaluation/hypotheses.md`) has never been tested against.
   Registered as a sweep target in
   [`08-next-experiments.md`](../03-research-and-evaluation/E6-corpus-digestion.md) → E6.

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

## Work packages

The 2026-09-13/14 specification pass turned this milestone's substrate from a
description into three documents with service surfaces, so the packages are now the
documents.

1. **Work record store** ([`13-work-record.md`](../../../10-technical/13-work-record.md)).
   Three record kinds, the immutable formulation and scope, the append-only
   transition log with its `logged`/`applied` marker, the `derived_from` lineage, and
   the service surface including `lineage` and `change_set`.
2. **Knowledge model store** ([`12-knowledge-model.md`](../../../10-technical/12-knowledge-model.md)).
   The claim record with mode-of-acquisition on the edge, the two write paths, the
   `children/` index, Read / Query / Traverse dependents.
3. **Context manager** ([`14-context-manager.md`](../../../10-technical/14-context-manager.md)).
   Register, the live set with its entry shape including `label`, recall over the
   degenerate policy, and the per-turn composition path.
4. **The wiring between them.** Attachment at task creation as an ungated runtime
   call; 4c attachment mid-work as a gated effect; incremental removal when a task
   reaches a terminal state. This is the package most likely to be underestimated:
   each store is simple and the edges between them are where the specification pass
   found its gaps.
5. **Small tests.** A processor reuses one stored finding and measurably beats one
   starting cold. This is what answers the evidence question at small scale, and it
   does **not** need M9.
6. **The corpus sweep** — E6. Run here; **graded in
   [M9](09-context-governance-measurement.md)**, since E6 is explicitly not graded on
   task success alone.

Packages 1–3 are independent of each other and can be built in any order. Package 4
depends on all three. Package 5 gates package 6: a corpus sweep that fails tells you
nothing about which of ingestion, retention or retrieval failed.

## What this milestone does for M3

**[M3](03-invariant-floor.md)'s evidence question gets its first real data here**, and
nothing currently records that connection.

M3 asks whether the enumerated effect types carve cleanly when real effects flow
through the gate. Six of nine types have never flowed. Two of the six — **type 4
work-record mutation and type 5 memory mutation** — only become real when durable
stores exist, which is this milestone.

They are also the two types that were **subdivided** in the 2026-09-14 pass: 4 into
Create / Transition / Attach / Conclude, 5 into Write / Relate. The cut was made from
what each act can do wrong, argued rather than observed. This milestone is the first
thing that puts real effects through those boundaries, so it is a test of the
subdivision and not only of the stores.

M3's own recorded blur is in the same place: *a conclusion is a type-4 effect* was
noted as a choice rather than something self-evident. Conclusion is now 4d, a named
sub-type. Whether that settles the blur or relocates it is answerable here.

## Relationship to M9

[M9](09-context-governance-measurement.md) measures whether what this milestone
holds is any good, independently of whether a task using it happened to succeed.
That is a dependency, not a sequencing claim: M9 needs this milestone's substrate
and the corpus sweep's result to have something concrete to measure against,
whatever order the two end up worked in.
