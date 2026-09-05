# Praxis

**State:** OPEN
**Opened:** 2026-09-05
**Updated:** 2026-09-05 — added a survey of what "praxis" actually means
(Aristotle / Marx / Freire / Arendt / the Praxis Framework) and an assessment of
it as a project mantra. Working verdict: keep as a lens, do not adopt as mantra.
The case against is **locked as ten numbered objections (O1–O10)** in "Why it
fails as a mantra", each meant to be argued individually; O1 is load-bearing, the
rest are independent. A short "still to check" list follows them.
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

## What "praxis" actually names — the concept, not the label

Until now this thread has used "praxis" loosely, as a label for *the practice-side
position behind the cadence change*. The word carries a specific and long history,
gathered here so a decision about adopting it is made against what it means rather
than against the label.

**Aristotle.** Three modes of human activity, each with its own governing faculty:

| mode | end | faculty |
|---|---|---|
| **theoria** — contemplation | knowledge of what is universal and necessary | *sophia* / *nous* |
| **poiesis** — making | an external product: a house, a poem, a tool | *techne* (craft) |
| **praxis** — action | internal: the goodness of the act and of the agent | *phronesis* (practical wisdom) |

The load-bearing part is *phronesis*. It is explicitly **not** a body of rules.
It is situated judgment — "the accumulated result of having acted, observed
consequences, and allowed those observations to refine the capacity for
judgment." Praxis is the mode of activity whose competence cannot be written
down as a procedure.

**Marx** (*Theses on Feuerbach*, *The German Ideology*). Praxis as the **unity of
critical thought and transformative action** — a dialectic in which theory informs
practice and practice reshapes theory, with neither prior. "The philosophers have
only interpreted the world; the point is to change it." Thought is held to
reflect the conditions that produce it.

**Freire** (*Pedagogy of the Oppressed*). Praxis = "**reflection and action upon
the world in order to transform it**," and the definition is a pincer: action
without reflection is mindless **activism**; reflection without action is
**verbalism** — armchair theory that changes nothing. Only the two together are
praxis.

**Arendt** (*The Human Condition*). Action (praxis) against making (poiesis).
Action is bound to **plurality, unpredictability, and irreversibility**. She
observes that the tradition keeps trying to **replace praxis with poiesis** — to
make politics into fabrication — precisely to escape unpredictability, and calls
that substitution the root of technocratic and utopian error. Her two named
remedies for action's frailty: **promising**, which bounds the unpredictability
of the future, and **forgiving**, which releases the actor from the
irreversibility of the past.

**The Praxis Framework** (Adrian Dooley; APMG / Creative Commons). A real,
established, free framework for the integrated management of projects, programmes
and portfolios — knowledge, method, competence, capability maturity. Not used
here, not evaluated here, but it owns the name in exactly this domain.

## Is "praxis" a good project mantra? — first assessment

**Recommendation: use it as a lens for this thread; do not adopt it as the
project's mantra.** The concept illuminates the cadence change and names its
central risk precisely. As a slogan it imports commitments the project has
explicitly rejected.

### What the concept genuinely buys

- **"Verbalism" is the exact name for item 5.** Freire's failure mode —
  reflection accumulating without action to discharge it — is what a
  spec-set-as-growing-context-problem *is*. Having the name is worth keeping
  whatever is decided about the mantra.
- **Arendt's remedies map onto the cadence change with uncomfortable
  precision.** "Write the contract ahead" is *promising*: bounding an
  unpredictable future by committing to a shape now. The reversibility principle
  (`00-project/03`) is *forgiving*: making the commitment cheap to undo. The
  cadence change is, structurally, Arendt's two answers to the frailty of acting
  under uncertainty — which is a strong sign the change is coherent, and a source
  of vocabulary for defending it.
- **The action↔reflection dialectic already describes the execution cadence.**
  Contract → experiment → finding cascades back into the contract. Findings
  overturn any point in the set. That *is* practice reshaping theory; the project
  has been doing praxis in Marx's sense without the word.
- **P-b rhymes with the anti-poiesis stance.** "The deliverable is insight, not a
  tool" (`01-use-cases.md`) is a refusal to be judged by the product made — which
  is Aristotle's praxis/poiesis line and Arendt's warning about the poiesis
  substitution, arrived at independently.

### Why it fails as a mantra — the locked objections

Stated 2026-09-05 as discrete claims, each meant to be attacked on its own. The
user has counter-arguments to each; these are the fixed targets for that. **O1 is
load-bearing; the rest are independent and any subset could fall without saving
the others.** Where an objection also names a conflict with a standing commitment,
that is marked `⚔`.

**O1 — `⚔` It blesses the property the project treats as a defect.** Praxis is
governed by *phronesis*: judgment that by definition cannot be reduced to rules.
The project's central architectural move runs the other way — resolve judgment
into measured, deterministic system behaviour, because a small model cannot hold
an uncodified judging seat (findings entry 7; `10-foundations/06`; `03` §4's
"make the practice mechanical, not advice"). Item 2 of this thread already flags
"in shape" as "the least determinate thing in the system" and wants it fixed. A
praxis mantra renames that a virtue. *Conflicts with:* determinism in judgment
seats, and the mechanise-the-practice programme.

**O2 — `⚔` It carries freight the prose discipline just forbade.**
`00-project/02` now requires claims to rest on located, checkable steps and warns
against borrowing weight from an adjacent subject. "Praxis" imports a century of
philosophy of history — Marx, Gramsci's "philosophy of praxis," critical
pedagogy, critical theory. A mantra that invites readers to bring connotations
the design set never sanctioned is the exact failure `02` exists to prevent.
*Conflicts with:* prose discipline / authority-by-auditable-argument.

**O3 — The name is already taken, in this exact domain.** The Praxis Framework
(Dooley; APMG; CC-licensed) is a specific, established P3M methodology. A project
whose PM philosophy is "praxis" invites confusion with a method it does not use
and has not evaluated.

**O4 — It is too general to encode the actual rule.** The cadence change is not
"unite theory and practice." It is a specific ordering and coupling: *write the
contract ahead; halt execution when a finding invalidates one.* "Praxis" names
the genus (theory/practice unity), not this species, and mantras get quoted
without their qualifications.

**O5 — `⚔` The cadence change is an asymmetry; praxis asserts a symmetry.**
Marx's praxis insists neither theory nor practice is prior. The 2026-09-05 change
is explicitly a priority claim — theory-leading, with a practice-triggered halt.
Adopting "praxis" papers over the very asymmetry this thread exists to justify,
and hands a future reader a term with which to argue the cadence back toward
balance. *Conflicts with:* the specific direction of `00-project/04`.

**O6 — Praxis presupposes a continuous acting subject; the architecture denies
its components one.** In Marx (self-creation through labour), Freire
(*conscientização*), and Arendt (the "who" disclosed in action), the actor is
*changed by* the doing. The project's actors are ephemeral processors and a
supervised loop with deliberately no persistent self (`10-foundations/05`:
conversation is working memory, knowledge is a published result). The mantra
would name a mode of being the system is built not to have. The human operator
has continuity — but a project mantra describes the system's method, not the
operator's growth.

**O7 — `⚔` Praxis resists measurement by design; the project is
measurement-first.** Aristotle ranks *theoria* above praxis precisely because
praxis handles the "variable, contingent" and does not yield stable, benchmarkable
knowledge. Six milestones of apparatus (the M6 suite, rungs of lift, deterministic
checks, the findings log) exist to make claims commensurable and reproducible. A
mantra that valorises the un-measurable contingent is at odds with the instrument.
*Conflicts with:* the whole evaluation programme.

**O8 — `⚔` It fails the operator plainness test.** `10-foundations/07` makes the
operator's performance the optimisation target and "ease of use not a side
quest," with the instruction "do not let the least expert user hit the floor." A
mantra should be sayable to that user. "Praxis" needs a philosophy lecture before
it means anything. *Conflicts with:* the operator-first commitment and, again,
the prose discipline.

**O9 — It is a scope-creep magnet.** "Praxis" has been stretched across pedagogy,
politics, ethics, professional practice, theology and P3M. As *the* mantra it
invites every future contributor to read their field's "praxis" into the project.
`03` §6 already flags this risk for the milder case of adopting "context
engineering"; "praxis" is that risk larger.

**O10 — The thread's own framing says no, and a better native candidate exists.**
"What this is not" states this thread is not a replacement for the removed mantra.
And if the project wants a phrase for the theory↔practice relation, it already
generated one: **auditable argumentation** (`00-project/02`; item 6 above flags it
as plausibly the root position) — native, plain, freight-free. Naming "praxis"
the mantra would bury it.

### The category caveat (context for O4, O6)

The project's loop is closer to **hypothesis → experiment → finding** (empirical
science) than to **reflection → action → transformation** (praxis — intrinsically
directed at changing a world, with an actor changed in the doing). The
resemblance to Marx's and Freire's dialectic is real but partial; the word
asserts the whole analogy when only part holds.

### Where praxis *supports* the current approach

One place, and it is genuine: the **promising / forgiving** reading of "write the
contract ahead" + reversibility (`00-project/03`, `01-use-cases.md` P8). Arendt's
two remedies for the frailty of acting under uncertainty are, structurally, what
the cadence change does. This is worth keeping as vocabulary regardless of the
mantra decision. Everywhere else, praxis either restates what the project already
does in heavier words or pulls toward the uncodified-judgment position the project
has evidence against.

### Still to check (issues not yet worked)

- Whether O7 holds against Aristotle's *own* view that praxis has its own rigour
  (deliberation, `NE` VI) rather than being simply "un-measurable" — the
  objection may be too strong.
- Whether "philosophy of praxis" as Gramsci used it (a euphemism under censorship)
  weakens O2's "critical-theory freight" claim or strengthens it.
- Whether any of O3/O9 (naming) actually bites, given the project is not
  publishing or marketing and the collision is with an obscure framework.
- Whether O6 is answered by locating praxis in the operator rather than the
  system — i.e. the mantra describes what the human does with the tool.

## What would make this thread land

A position that answers at least (2) and (3), because both are gates currently
operating on judgment with nothing written behind them. (1), (4) and (5) can be
stated as constraints without being solved.

The concept survey above does not settle this — but it narrows it. Whatever the
unifying position is, it is **not** "praxis" imported wholesale, and it must not
rest on cultivated judgment as its ground, because that is the thing the project
is trying to build a system to not require.

## What would make this thread wrong

If the six items turn out to be six unrelated process defects rather than
consequences of one unstated position, there is no praxis position to write — only
five rule patches and a prose convention. That outcome would be a negative result
worth recording, not a failure to find something.
