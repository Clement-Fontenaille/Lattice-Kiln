# M8 — Persistent work and knowledge

Milestone: `docs/00-design/40-roadmap/01-MILESTONES/08-persistent-work-and-knowledge.md`
Specs: `docs/10-technical/{12-knowledge-model,13-work-record,14-context-manager}.md`

## What's here

| file | package | spec |
|---|---|---|
| `work_record.py` | 1 | `13-work-record.md` |
| `knowledge_model.py` | 2 | `12-knowledge-model.md` |
| `context_manager.py` | 3 | `14-context-manager.md` |
| `wiring.py` | 4 | the edges between the three |
| `test_small.py` | 5 | evidence question, small-scale stage |

Package 6 (the corpus sweep, E6) is not built here — it's graded in M9 and needs a
processor to do the ingesting, which is cognition, not substrate.

## Running

```
python test_small.py
```

No model calls. Naive filesystem storage per each spec's own "naive default" —
`work/`, `knowledge/`, `context/` under a temp dir the test cleans up.

## What the small test checks

1. A promoted finding survives its task ending (retention is promotion, not liveness).
2. Qualifying a claim never edits the original (append-only, structurally).
3. Reusing a stored finding beats cold-start re-derivation on crossings (1 vs 3) —
   the evidence question's small-scale stage.
4. An unpromoted attachment is removed when its task ends (incremental removal,
   no sweep schedule, no promotion path invented).

Plus a normative-rules pass (run ad hoc, not in `test_small.py`): no scope-mutation
path exists anywhere in the store; `declined` stays distinct from `blocked`; a
terminal item refuses further transitions; `elide` refuses a promoted root;
`compress` refuses an unchecked/root claim; content must be structured (a dict),
never a bare string.

## Build decisions made that the specs left open

Recorded inline as docstrings, pointer here for anything that isn't obvious from
the code:

- **`conclude()`'s auto-terminal mapping** (`work_record.py`): `answered` →
  `executed`, `declined` → `abandoned`, `blocked` → not terminal by default. The
  spec maps this cleanly for declined; `answered`/`blocked` termination is this
  implementation's call, overridable via `terminal=`.
- **Containment checking** (`work_record.py`, `_looks_contained`): a placeholder.
  `03-capability-authority-model.md` owns the real natural-language judgment; this
  store only refuses a creation whose `ceiling` argument is empty. Not a real check.
- **`change_set()`** (`work_record.py`): returns transitions, which is the
  closest thing this store holds. The spec's own open contract says the real
  shape needs observability's effect history — not built in M8.
- **`still_live` computation** (`wiring.py`): naive scan of every other live
  set's log. `knowledge_model.py` explicitly leaves this to the caller since it
  can't see the other two stores on its own.

## What is deliberately NOT here

- The real scope checker (M17). `ceiling` is a caller-supplied string.
- Observability (`02-observability-event-model.md`). `change_set` and `recall`'s
  turn-input record are stand-ins for what that store owes.
- A real recall policy — `context_manager.py`'s `recall()` is the degenerate
  baseline (`07-naive-context-assembly.md`), not the experimental surface M9 opens.
- Any gating. Every store here assumes its caller already passed capability and
  the gate; that's M17/M11's job, not M8's.
