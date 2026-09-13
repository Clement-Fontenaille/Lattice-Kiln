# Task ↔ artifact edges — a worked trace

*Nothing here is load-bearing. One ordinary task decomposed into operations, from the
operator's request to the last artifact being deleted.*

> **Motto:** Follow one task all the way through and see what has no name.

## The case

**Intent**, arriving out of band: *"Add a `--json` output format to the `report`
command."*

**Ceiling**, derived during phase 1: *the `report` command's output path and its
formatters, the tests covering that output, and the CLI help text. Not the web API,
not the storage layer.*

**Task T-88**, created in phase 2 with that ceiling as its scope.

---

## Edge labels

An edge carries a label saying what the artifact is **to** the task. The label is
known at the moment the edge is created.

| Label | Carried by | Edge created |
|---|---|---|
| `objective` | What the task is to accomplish | At task creation, or at invocation when a calling processor writes a new one |
| `derived_scope` | An invariant processor's ceiling output | At task creation |
| `tool_output` | What a tool call returned | On registration |
| `handoff:thinking` | A processor's reasoning | On registration |
| `handoff:response` | A processor's conclusion | On registration |

`handoff:thinking` and `handoff:response` are distinct because a `review` instance
receives a prior processor's conclusion and not its reasoning
(`10-technical/06`, independence). The label is what that cut is made against.

---

## Phase 1 — scope evaluation, before the task exists

Deriving a ceiling is a judgment over natural language, so it is performed by an
invariant processor, which is an LLM instance and needs material to work from.

**1.1** Intent arrives out of band and is written to the work record, write-once.

**1.2** An invariant processor instance E-1 is created to derive the ceiling. Its
scope is the **current project** — the working directory — set from outside rather
than derived, since it cannot be bounded by the ceiling it is producing. It holds no
effect grants.

**1.3** E-1 reads the intent. Crossing type `read`.

**1.4** E-1 performs orienting tool calls, each a read:

- probe the file tree;
- read the `README`;
- search for documentation adjacent to what the intent names;
- check whether a test suite exists and what it covers.

**1.5** E-1 produces the ceiling and ends.

**Nothing from phase 1 is in the knowledge model.** An artifact cannot be declared
there before it is attached to a task. What 1.3, 1.4 and 1.5 produced is held in
memory, unattached, on the running runtime stack.

If task creation does not follow, none of it is ever declared.

---

## Phase 2 — task creation

**2.1** Task T-88 is created, carrying the ceiling as its scope.

**2.2** Creation attaches the material assembled for it. Each attachment declares the
artifact in the knowledge model and creates its edge to T-88:

- the intent, label `tool_output`;
- the orienting reads from 1.4, label `tool_output`;
- the ceiling from 1.5, label `derived_scope`;
- the task's objective, label `objective`.

**2.3** Attachment at creation is a **runtime call**. It is not a proposed effect and
needs no capability evaluation and no gating.

**2.4** The same call serves an operator attaching further context to an existing
task.

---

## Phase 3 — first invocation

**3.1** Instance I-1, an implementer, is instantiated against T-88. It binds role
instructions, an objective, a scope, T-88's live-set identity, an isolation
preference, a capability set, an interaction mode.

**3.2** No processor invoked I-1 — it is the first, as in a dloop arrangement — so it
**inherits T-88's objective and scope** rather than receiving new ones. Both are
already declared, attached in 2.2. No new artifact is created.

Where a calling processor does invoke an instance, that processor writes the
invocation's objective, which becomes a new artifact with label `objective`.

**3.3** The first turn input is composed from the live set as it stands.

---

## Phase 4 — the work

Each tool call follows the same path: scope check before execution, capability, gate,
runtime execution, the result crossing back, registration, an edge to T-88.

**4.1** `read("cli/report.py")` → Observation, edge, crossing type `read`, origin
invocation I-1.

**4.2** `read("cli/formats.py")` → same.

**4.3** `search_kb("output format stability")` → returns `c-4471`, a Decision from an
earlier task. **No content is written**: the claim already exists. An edge to T-88 is
created, crossing type `retrieval`.

**4.4** `read("docs/api/web.md")`, reached while searching for the word "format" →
Observation, edge, crossing type `read`.

**4.5** Write to `cli/formats.py`, adding a `JsonFormatter`. Effect type 1. Realized.
An entry appears in the **change set**, the outbound edge set held by the work record.

**4.6** Run the tests. Effect type 2. The output crosses back → Observation, edge,
crossing type `effect_response`. One test fails.

**4.7** Turn input composed. The live set holds nine entries and the turn budget
binds. The recall policy selects and drops.

**4.8** Further write, further test run, tests pass.

**4.9** I-1 emits `answered` and ends. The live set is unaffected: it belongs to
T-88.

---

## Phase 5 — attachment

**5.1** An instance other than I-1 examines what happened.

**5.2** It proposes a type-4 effect attaching `c-4471` to T-88, carrying a reason in
natural language: *constrains key ordering in the new formatter; adding a field is
permitted, reordering is not.*

**5.3** It proposes a second attachment for the finding produced during the work:
*the formatter interface assumes line-oriented output; JSON needs a whole-document
hook.*

**5.4** Each attachment passes scope check, capability and gate like any other type-4
effect.

---

## Phase 6 — task end

**6.1** T-88 reaches a terminal transition. Its live set ends.

**6.2** Each artifact the live set held loses its root status. For each: is it
promoted, and does another live task hold it?

| Artifact | Outcome |
|---|---|
| Observations from phases 1 and 4 — intent, file tree, README, docs, test suite, `report.py`, `formats.py`, `web.md`, test output | Deleted unless promoted or reachable from a promoted claim, or held by another live task |
| `c-4471` | Held elsewhere and promoted. The claim survives; the edge T-88 → c-4471 dies |
| The attached finding | Survives if the attachment promoted it |

**6.3** For each artifact, deletion walks up its provenance and removes each ancestor
that is not promoted and that no remaining root reaches.

---

## Splitting — edge inheritance

Two base policies: **inherit all**, or **inherit none**. Inheritance duplicates
edges, never artifacts.

The objective is never inherited. A new task receives its own objective, which
becomes a new artifact with label `objective`, even where that objective is also
stated in the parent's handoff.

---

## Not yet decomposed

- Whether phase 1's reads are scope-checked against E-1's project scope, and what a
  refusal there would mean.
- Whether `derived_scope` is inherited on a split, or re-derived per task the way the
  objective is re-written.
- Whether a processor attaching mid-work (phase 5) uses the same ungated runtime call
  as 2.3, or proposes a gated type-4 effect.
- How 6.2 determines that another live task holds an artifact.
- Edge removal before a task ends: the operation exists so that it is available, and
  nothing yet calls it.

## Traces not yet run

- A task whose subject is not known at the start: *tests pass locally and fail in
  CI*.
- A task that splits, to exercise edge inheritance.
- A task refused on scope, to see what a rejection leaves behind.
