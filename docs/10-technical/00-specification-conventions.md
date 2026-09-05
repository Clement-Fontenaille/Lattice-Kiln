# Specification Conventions

## TL;DR

Every specification document states what a component is responsible for, what it consumes, what it may produce, what authority it holds, how it fails visibly, and which neighbouring component owns the rest. Anything not yet decidable is recorded as an open contract rather than guessed.

> **Motto:** An unresolved contract stated plainly beats a resolved one invented quietly.

## Traceability

Each document opens with a **Traces to** line naming the design documents it specifies. A specification claim that has no basis in the design set is not permitted; if the implementation needs it, the design set is extended first.

Where a specification narrows a design concept — picking one interpretation among several the design document left open — it says so explicitly under a **Narrowing** note, so the discarded options remain visible.

## Authority and revision

Every document in this set is authoritative. Normative language binds any
conforming implementation regardless of when the document was written or whether a
milestone has exercised it.

There are no tiers and no draft status. A maturity tier would make the
most-exercised contracts the hardest to overturn — the ones where being wrong costs
most — which inverts the intent.

A specification is revised on findings — not on preference, and not because a
document feels dated.

No point is exempt. A finding may revise any part of the set it bears on, technical
contract through foundational concept. Where it bears on a concept, the design
document is updated first and the specification follows
(`00-design/00-project/04-execution-cadence.md` → the feedback flow).

### A contract written ahead

Writing a contract before its milestone costs it no authority. The reason to write
early is that a later finding needs something to contradict.

The evidence behind a contract remains visible regardless. A contract exercised by
three milestones has three findings behind it; one written ahead has none.
Overturning the first means accounting for that evidence. This is recoverable from
the findings, not a status assigned to the document.

### Exercised by

Where a milestone has exercised a contract, the document records it below **Traces
to**: *Exercised by: findings 3, 6.*

Provenance, not status. Its absence means no milestone has run against the
document, not that it binds less.

## Document structure

A mature specification document provides, in roughly this order:

- **Responsibility** — the one thing this component is accountable for. If this cannot be stated in a sentence, the concept is not ready to specify.
- **Inputs** — what it consumes, and from whom.
- **Outputs** — what it may produce, and the form each output takes.
- **Authority** — what it may cause directly, what it may only propose, and what it may never do.
- **Failure modes** — how it fails, and how that failure becomes visible to the runtime, the operator, or a later evaluator. A failure that is silent is a specification defect.
- **Relationships** — which neighbouring components it depends on, and which responsibilities it explicitly does not own.
- **Open contracts** — decisions left unresolved, each phrased as a question with enough context that a later pass can close it.

Short documents may collapse sections, but may not drop Authority, Failure modes, or Open contracts.

## Normative language

- **MUST** / **MUST NOT** — a requirement. Violation is a defect in any conforming implementation.
- **SHOULD** / **SHOULD NOT** — a strong default. Deviation requires a recorded reason.
- **MAY** — a genuine option with no default preference.

Normative terms apply to the implementation, not to the AI components' reasoning. Cognition is shaped by role and objective, not by this set.

## Illustrative material

Concrete identifiers, payload shapes, and code-like fragments are illustrative unless a sentence marks them normative. They exist to remove ambiguity about intent, not to fix a format. An illustrative block MUST be labelled as such.

## Open contract lifecycle

An open contract is closed by evidence from a milestone, by a design-set decision, or by explicit specification work — never by an implementation choosing silently at build time. When closed, the resolution replaces the question and a one-line trace records what closed it.
