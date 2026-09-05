# Praxis

**State:** OPEN
**Opened:** 2026-09-05
**Origin:** the specification-cadence change of 2026-09-05. The rule changed from
*write contracts just in time* to *write contracts ahead; gate execution instead*.
The rule is now in `00-project/04-execution-cadence.md`. The position behind it is
not written anywhere, and several problems it creates have no answer.

## Why this thread exists

The set has theory (`00-design/`), commitment (`10-technical/`), practice
(`experiments/`), and record (`50-findings/`). The cadence describes the **flow**
between them — design first, then specification, then sequence. Nothing states the
**relationship**.

That gap became load-bearing when the cadence changed. "Write the contract early so
a finding has something to contradict, then stop until you have cascaded what the
finding implies" is not a filing convention. It is a claim about how theory and
practice hold each other:

- theory written in advance **so that** practice can falsify it;
- practice halted **so that** theory can be revised before more practice
  accumulates on a shape already known to be wrong.

Encoded as process rules with no position behind them, that claim is exactly what
`02-documentation-philosophy.md` exists to prevent — semantics accumulating in the
rules that the design set never sanctioned.

## What this is not

The set referred three times to "the project mantra" — in both sequence-rework
documents and in `STATUS.md` — and no document ever stated one. It was a gesture at
the general direction of the project. Those references were removed on 2026-09-05.

**This thread is not a replacement for that.** It is a new subject with no prior
text in the set. Nothing here is continuous with what "the mantra" was waving at,
and this document should not be read as recovering it.

## The material this has to account for

Six items. The first was raised against the cadence change directly; four followed
from it; the sixth arrived when the prose rule was written.

### 1. A written contract anchors

A contract written before its evidence will feel decided by the time evidence
arrives. The pull is to defend the shape already written rather than revise it.

Two mitigations exist and neither is sufficient. The **Narrowing** note keeps
discarded options visible. The revision rule states that findings overturn any
point in the set. Both are procedural; anchoring is a disposition. Nothing in the
set currently addresses the disposition, and a first attempt at one — a
Placeholder / Provisional / Validated maturity ladder — was rejected on the
grounds that it would have made the most-exercised contracts the hardest to
overturn, which inverts the intent.

**Open:** what makes revising your own written contract cheap enough to actually
happen?

### 2. "In shape" has no checkable criterion

Execution gate 1 says the spec must be *in shape*: responsibility stateable in a
sentence, authority bounded, failure modes visible, unknowns named as open
contracts. Every clause is a judgment call.

This sits badly against the project's own strongest empirical result. Findings
entry 7: a deterministic gate scores 9/10 and **drops to 6/10 when a 7B judgment
panel is added**. The project's position is that judgment seats need determinism at
this model size. The gate deciding whether work proceeds is currently the least
determinate thing in the system.

**Open:** can "in shape" be made checkable, or is it necessarily a human judgment —
and if the latter, what does that imply for the tier where a loop applies the gate
to itself?

### 3. Nobody is named as the one who classifies a finding critical

Execution gate 2 fires when a finding **invalidates** a contract. Somebody must
decide that a given finding is of that kind rather than the ordinary kind that
merely adds or narrows an open contract.

That classification has the strongest available incentive to come back "no",
because "yes" means stopping. A human does it today. At
`01-MILESTONES/12-system-level-candidate-tuning.md` the loop proposing changes
would also be judging whether findings invalidate its own contracts, which is the
Goodhart exposure the design set already names — arriving through the cadence
rather than through the evaluation metric.

**Open:** is the classifier a role, a rule, or a deterministic check? Does it
belong to the triage role at M11, which is already fixed outside the feedback loops
for the same reason?

### 4. The cost of being wrong scales with how far ahead you wrote

Sixteen open milestones. Every contract written ahead is a surface a foundational
revision must cascade through. The cascade gate makes drift expensive **by
design** — that is what stops silent divergence — but it means the cost of being
wrong about a foundation grows with the depth of specification already written.

There is an optimum depth. Nothing names it, and the rule as written implies no
limit.

**Open:** what bounds spec-ahead depth, and is the bound a rule or a judgment?

### 5. Specifications are context

`10-foundations/04` holds that what makes context costly is **redundancy, not
volume**. A contract written ahead is by construction partly redundant with the
design document it traces to — that is what a `Traces to` line records.

The project's own thesis, pointed at its own documentation. A growing specification
set is a growing context problem for any assembly that has to read it, including
the eventual system itself.

**Open:** does the set's own growth fall under its context thesis, and if so what
follows for how much is written ahead?

### 6. Authority grounded in auditable argumentation

Added 2026-09-05, when the prose rule went into `02-documentation-philosophy.md`:
authority in this set is grounded in **auditable argumentation** — each step
checkable against a finding, a design position, or a prior contract.

Stated as a writing rule, it is really an epistemics claim, and it is the one that
plausibly organises the other five. If authority comes from auditability rather
than from provenance or seniority, then:

- **(1)** anchoring is weak, because a contract's authority never rested on having
  been written first;
- **(2)** "in shape" may reduce to *are its steps locatable and checkable*;
- **(3)** the classifier's decision is itself subject to audit, which constrains
  who may make it;
- **(5)** redundant restatement actively costs authority rather than being merely
  wasteful.

**Open:** is auditable argumentation the root position, with the cadence rules
derived from it — or is it one commitment among several?

## What would make this thread land

A position that answers at least (2) and (3), because both are gates currently
operating on judgment with nothing written behind them. (1), (4) and (5) can be
stated as constraints without being solved.

## What would make this thread wrong

If the six items turn out to be six unrelated process defects rather than
consequences of one unstated position, there is no praxis position to write — only
five rule patches and a prose convention. That outcome would be a negative result
worth recording, not a failure to find something.
