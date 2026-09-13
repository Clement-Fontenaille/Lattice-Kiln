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

## Phase 1 — scope evaluation, before the task exists

Deriving a ceiling is a judgment over natural language, so it is performed by an
invariant processor, which is an LLM instance and needs material to work from. The
task does not exist yet, so there is no task scope to bind and no task live set to
register into.

**1.1** Intent arrives out of band and is written to the work record, write-once.

**1.2** An invariant processor instance E-1 is created to derive the ceiling. It
binds role instructions and an objective (*derive the scope ceiling for this
intent*). It holds no effect grants; it reads and produces one ceiling.

**1.3** E-1 reads the intent. Crossing type `read`. An Observation is written to the
knowledge model.

**1.4** E-1 performs orienting tool calls, each a read, each writing an Observation:

- probe the file tree;
- read the `README`;
- search for documentation adjacent to what the intent names;
- check whether a test suite exists and what it covers.

**1.5** E-1 produces the ceiling and ends.

At the end of phase 1 the artifacts from 1.3 and 1.4 exist in the knowledge model
and are attached to no task.

---

## Phase 2 — task creation

**2.1** Task T-88 is created, carrying the ceiling as its scope.

**2.2** Every artifact obtained in phase 1 gains an edge to T-88. The set includes
the intent Observation and the orienting reads, which is the task's live set at
creation.

**2.3** The artifacts are not re-fetched and not copied. Registration happened in
phase 1; phase 2 creates edges.

---

## Phase 3 — first invocation

**3.1** Instance I-1, an implementer, is instantiated against T-88. It binds role
instructions, an objective, T-88's scope, T-88's live-set identity, an isolation
preference, a capability set, an interaction mode.

**3.2** The first turn input is composed from the live set as it stands: intent,
file tree, README, documentation, test-suite observation.

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

## Not yet decomposed

- What bounds E-1 in phase 1, given that it derives the ceiling and so cannot be
  bounded by it.
- Whether phase 1's reads are scope-checked, and against what.
- Where phase 1's artifacts are held between 1.3 and 2.2.
- What happens to phase 1's artifacts if task creation does not occur.
- Whether the objective and the scope bound in 3.1 are registered as artifacts, and
  by which operation.
- Which operation creates the edges in 2.2, and whether it is a type-4 effect.
- How 6.2 determines that another live task holds an artifact.
- Whether an edge can be removed before its task ends.
- How inheritance duplicates edges when a task is split.

## Traces not yet run

- A task whose subject is not known at the start: *tests pass locally and fail in
  CI*.
- A task that splits, to exercise edge inheritance.
- A task refused on scope, to see what a rejection leaves behind.
