# Evaluation Task Suite (v0)

**Traces to:** `00-design/40-roadmap/01-MILESTONES/completed/06-evaluation-task-suite.md` (M6),
`00-design/40-roadmap/03-research-and-evaluation-agenda.md`,
`00-design/40-roadmap/07-sequence-rework-02.md`,
`00-design/00-project/04-execution-cadence.md` (findings need a ruler);
binds to `10-technical/02-observability-event-model.md` (a suite run is a set of
reconstructable runs), and is consumed by Milestone 7 and every adaptive
milestone after it.

## TL;DR

A suite of realistic development tasks, each built around a **specific trap**, each
scored by a **deterministic partial-credit check**, each tagged with **which
system capability it stresses**. It is the ruler: no claim about a pipeline
variant is admissible unless it was measured here.

> **Motto:** A task earns its place only if a plausible wrong answer fails it and
> the right answer passes.

## Status of this document

v0 for Milestone 6. The **taxonomy, the task schema, the scoring model, and the
determinism / anti-gaming rules are normative.** The task catalogue below is the
committed v0 content: six existing tasks folded in from the MVP fixture, ~28
intended tasks specified by trap class. Individual task designs may change as they
are built; the schema they conform to may not without a rework note.

## Narrowing

This document defines **how the project evaluates a code-producing pipeline on
single-repository tasks**. It does *not* define: context-quality metrics
(Milestone 9), meta-evaluation of the improvement process (Milestone 14),
cross-generation benchmarking (Milestone 15), or live user-study methodology. It
is a fixed, offline, deterministic suite — the anchor those later efforts measure
drift against.

## Why it exists

Every MVP-slice finding (findings-log entries 5–7) carries the same caveat: *N ≤
3, 4–6 synthetic tasks, read the transcript not the score.* The fixture could not
separate arms and it missed whole classes of request. Milestone 7 and every loop
after it decide things by running against tasks; the tasks have to be good first.

## The two axes

Every task is one **request shape** carrying one primary **trap**.

**Request shapes** (what a developer actually asks for):

| shape | example ask |
|---|---|
| `fix` | "X returns the wrong value when …" |
| `feature` | "add a `retries` parameter to …" |
| `implement` | "implement `parse_duration` (stub exists)" |
| `refactor` | "extract the shared helper / split this function" |
| `perf` | "this is slow, speed it up" |
| `compat` | "change the return type / signature of …" |
| `robustness` | "add input validation / stop it crashing on …" |
| `cleanup` | "remove this dead code / this TODO" |
| `data` | "parse this CSV / serialize this object / merge these configs" |
| `dependency` | "make this import optional" |
| `migration` | "move every call site from `v1` to `v2`" |
| `concurrency` | "this is wrong under concurrent use" |

**Traps** (what catches a weak model or a weak pipeline):

| trap | the failure it induces |
|---|---|
| `misdirection` | symptom and cause are in different places; the obvious patch is wrong |
| `backward-compat` | the clean change breaks existing callers |
| `behaviour-preserving` | correctness is invisible to a behavioural test; needs a structural check |
| `edge-coverage` | the naive impl lands the common case, misses 2–3 edges |
| `false-premise` | the request cannot be done as stated; the right move is to decline or redirect |
| `silent-failure` | the change makes the test pass by hiding a real error |
| `multi-concern` | the request bundles 2–3 deliverables; a weak arm drops the secondary ones |

## Task schema (normative)

Each task is a directory under the suite root plus a record in `tasks.json`
(schema `eval-suite-tasks/0`):

```
{
  "id": "hf_deprecate",
  "dir": "hf_deprecate",
  "shape": "compat",
  "trap": "backward-compat",
  "objective": "<the developer request, verbatim, one paragraph>",
  "stresses": ["regression-guard", "L2-structural"],
  "expect": {
    "objective_pass": true | false,
    "decline_correct": false            // true => the right terminal is "declined"
  }
}
```

Directory contents:

- the code under test (stdlib-only Python, small);
- `test_task.py` — the check (see scoring); **listed in `protected_files`**, restored
  from pristine before scoring so no arm can "fix" the test;
- optionally `README.md` — the human-readable trap description (not shown to the
  system under test).

**Rules:**

1. **stdlib only**, check runs in **< 1 s**, fully **deterministic** (no clock, no
   network, no randomness in the check).
2. The check **must** distinguish the correct answer from the most plausible wrong
   one via a named subtest. The `README` states which subtest is the
   discriminator.
3. Every task ships a **pre-existing passing test** (behaviour that must not
   regress) alongside the new assertions. A run that breaks a
   previously-passing subtest is a hard failure regardless of net score.
4. `decline_correct: true` tasks: the correct terminal is `declined` and the
   repository is left byte-identical. Any file mutation fails the task.

## Scoring model (normative)

`test_task.py` prints one or more score lines and exits 0 iff the gating score is
full:

- `SUBTESTS p/t` — behavioural, **gates** `objective_pass`. Partial credit = `p/t`.
- `DOCSCORE p/t` / `TODOSCORE p/t` / `STRUCTSCORE p/t` — structural quality
  dimensions where behaviour under-determines the deliverable (docstrings present,
  duplication removed, function count/length, a stale comment deleted). **Do not
  gate**; reported separately.
- A crashing check (broken Python from the arm) scores `SUBTESTS 0/0` **and** is
  recorded as a distinct `check_crashed` outcome — never silently treated as
  `0/0` partial credit (MVP fixture caveat, entry 6 addendum).

The per-run record carries, for each task: `terminal` (resolved / needs-change /
escalate / declined), `SUBTESTS`, every structural score, `regressed` (bool),
`decline_correct` match, model-call count, wall time.

## Runner contract

The runner (`run_suite.py`) takes an arm (a callable: objective + workspace →
terminal + mutated workspace) and produces:

- per-task partial-credit + terminal + cost;
- **`stresses` slices** — mean outcome per capability tag, so "does concern-split
  help?" is read off the `multi-concern` / `concern-split` slice, not the
  aggregate;
- **decline accuracy** — on `decline_correct` tasks, `declined` vs anything else;
- **regression count** — tasks where a pre-existing subtest broke;
- a cost/benefit ledger vs a named baseline arm (monolith).

It reuses the M2 recorder: each task run is a reconstructable run under one
`intent_ref`, so a suite run is queryable after the fact.

## Existing tasks (folded in from the MVP fixture)

`experiments/M5-intelligent-orchestration/fixture_workflow/` → suite, re-tagged:

| id | shape | trap | stresses | decline |
|---|---|---|---|---|
| wf1_crossfile | fix | misdirection | cross-file, premise-audit | no |
| wf2_retry | feature | edge-coverage | edge-coverage, greenfield-impl | no |
| wf3_refactor | refactor | behaviour-preserving | L2-structural | no |
| wf4_assumption | perf | false-premise | premise-audit | **yes** |
| wf5_partial | implement | edge-coverage | kway-synth, partial-credit | no |
| wf6_multi | migration | multi-concern | concern-split, combined-score | no |

## Intended tasks (v0 catalogue)

Grouped by trap; each row is `id — the ask — the trap — the discriminator`.

### misdirection (`fix`)

- `hf_pagination` — "`paginate(items, page, size)` returns wrong items on the last
  page" — fixing the last-page off-by-one breaks page 1 — subtests for
  first/middle/last/past-end.
- `hf_misfiled_bug` — "`discount(price, pct)` is wrong for `pct > 100`" — `discount`
  is *documented* to reject `pct>100`; a caller passes unvalidated 150 — correct
  fix is in the caller (or decline) — `discount(10,150)` must still raise.

### backward-compat (`compat`)

- `hf_multi_recipient` — "make `notify(to, msg)` take multiple recipients" — `to:
  str → list` breaks callers — must accept `str | list`; old-style call still
  passes.
- `hf_return_shape` — "return a richer object from `get_user` instead of a tuple" —
  callers unpack — `namedtuple`: `n, a = get_user(1)` **and** `get_user(1).email`
  both work.
- `hf_deprecate` — "deprecate `old_parse`, point at `new_parse`" — `old_parse`
  must still work, emit `DeprecationWarning`, and match `new_parse` on the overlap.
- `hf_json_field` — "add a field to the response dict" — old records lack it —
  new field has a default; existing keys/order unchanged.

### behaviour-preserving (`refactor`)

- `hf_extract_fn` — "split this 40-line `process()` into helpers" — an
  early-return and an `except` path get dropped — those two inputs are subtests;
  STRUCTSCORE for ≥3 functions each <15 lines.
- `hf_dict_dispatch` — "replace the if/elif chain with a dict lookup" — fall-
  through `else` + one branch has a side effect — the unmatched-key case + the
  side-effect branch.
- `hf_rename` — "rename `calc` → `compute` everywhere" — substring of `recalc_all`,
  a serialization key, a log string — public rename done, `recalc_all` intact,
  persisted key **unchanged**.
- `hf_rec_to_iter` — "make `walk()` iterative" — it memoizes and has an
  empty/single base case — subtests for the base cases + a large input (no
  recursion-limit crash).

### edge-coverage (`feature` / `data`)

- `hf_timeout_param` — "add `timeout` to `fetch`" — semantics of `timeout=0`,
  default, existing callers — subtests pin `0` = one-shot, default = unbounded,
  old call unaffected.
- `hf_cache_decorator` — "add caching to `expensive(x)`" — unhashable args,
  mutating the cached result, unbounded growth — subtests for each.
- `hf_csv` — "parse this CSV" — quoted commas, embedded newline, BOM, CRLF,
  trailing blank line — 6 subtests.
- `hf_path_sanitize` — "sanitize a filename for use as a path" — `../`, absolute,
  null byte, `CON`/`PRN`, trailing dot; over-sanitizing `my.file.txt` fails a
  subtest — partial-credit matrix.
- `hf_merge_config` — "merge two config dicts" — deep vs shallow, `None` = delete,
  list concat vs replace — one subtest each.

### false-premise / push-back (`decline_correct: true`)

- `hf_already_optimal` — "this function is slow, optimize it" — it is fine; the
  caller runs it N+1 — correct: batch API or decline; a bare rewrite fails the
  "output unchanged for the same inputs" subtest.
- `hf_cache_nondeterministic` — "cache this to speed it up" — it reads the clock —
  caching changes behaviour — decline (or document the constraint).
- `hf_dead_code` — "remove this unused function" — it is reached via a
  `getattr`/registry — decline and name the caller; removal fails an import
  subtest.
- `hf_remove_validation` — "this validation is annoying, drop it" — a downstream
  invariant depends on it — decline; removal breaks a pre-existing subtest.

### silent-failure (`robustness`)

- `hf_suppress` — "wrap this so it stops crashing" — the exception signals a real
  upstream bug — a bare `except: pass` passes the crash subtest but fails a
  subtest that feeds a genuine programming error and asserts it still surfaces.
- `hf_validate_withdraw` — "add input validation to `withdraw(acct, amt)`" —
  over-validation breaks `withdraw(balance)` (exact balance is legal) — matrix:
  negative / over-balance / zero / exact-ok / non-numeric.
- `hf_retry_backoff` — "add retry with backoff to `send()`" — retrying a
  non-idempotent call / a permanent error / no cap — subtests: idempotency
  guard, give-up-on-permanent, attempt cap.

### multi-concern (`migration` / `mixed`)

- `hf_json_serialize` — "make `to_json` handle our objects, add a round-trip
  helper, add a module docstring" — concern 1 traps: `datetime`, `set`,
  `Decimal`, circular ref — SUBTESTS + STRUCTSCORE + DOCSCORE.
- `hf_api_v1_to_v2` — "move every call site from `old_client` to `new_client`,
  update the docstrings, delete the compat shim" — one call site passes an arg
  the new API renamed — SUBTESTS (behaviour) + TODOSCORE (shim gone) + DOCSCORE.

### concurrency (`concurrency`) — light, `threading`, deterministic-ish

- `hf_counter_race` — "`Counter.incr` is wrong under threads" — lock the right
  region; a lock around the wrong span still races; a coarse lock that also wraps
  a callback deadlocks — subtests run N threads × M increments and assert the
  total, plus a no-deadlock timeout subtest.

## Determinism & anti-gaming (normative)

- `test_task.py` in `protected_files`, restored before scoring.
- No task's check imports anything outside the stdlib or the task's own modules.
- The discriminator subtest is documented per task; a suite-lint checks every
  non-`decline` task has one.
- `decline_correct` tasks fail on *any* file mutation, so "decline" cannot be
  faked by a no-op edit that happens to keep tests green.
- The suite is versioned; adding/removing a task is a recorded change, so a
  cross-run comparison always states the suite version.

## Open contracts

- **Suite size and balance.** v0 is ~34 tasks. Whether that separates arms at
  N=3–5 is itself an M6 evidence question; the catalogue may grow.
- **Structural scoring rubric.** `STRUCTSCORE` dimensions (function length,
  duplication, naming) are defined per task in v0. A shared rubric is deferred.
- **Non-Python / multi-file-repo tasks.** Out for v0 (stdlib-Python,
  small-repo). The taxonomy is language-agnostic; the fixtures are not yet.
- **Name the population** *(`00-design/10-foundations/07`)*. The attribution rule
  binds a failure to the assembly **within the population that assembly claims to
  serve**, which creates an obligation to name that population. This suite does
  not. It scores the assembly minus the operator — fixed objectives, no operator
  variance — and does not say so. What population do these tasks represent, and
  what does the suite's score mean for anyone outside it?
- **The agenda's two hypotheses are not in the scoring model**
  *(`00-design/40-roadmap/03-research-and-evaluation-agenda.md`)*.
  Decomposition-as-grain-matching and accessibility-without-weakness were added to
  the agenda and neither is measurable from a suite run. E2 and E5 are the intended
  tests; whether they need suite support, or run beside it, is unresolved.
- **Live-difficulty calibration.** Whether task difficulty should track model
  capability over time (so the suite stays discriminating as models improve) —
  deferred to Milestone 14/15.
- **Relationship to context-quality metrics (Milestone 9).** This suite scores
  task outcome; M9 scores context selection independent of outcome. They share
  the fixtures, not the metric.

## Relationships

- **Observability** (`02-observability-event-model.md`) — a suite run is a set of
  reconstructable runs; the runner reuses the recorder.
- **Static supervised workflow** (M7, `11-static-workflow.md`) — the
  first consumer; its evidence question is stated against this suite.
- **Research & evaluation agenda** (`40-roadmap/03`) — the hypotheses this suite
  is built to test are listed there; each task's `stresses` tag links to one.
- **Findings log** — entries 5–7 are the observations this suite is designed to
  make rigorous.
