# M2 — Observability Foundation

Milestone 2. Makes AI-assisted runs reconstructable well enough to answer a
question nobody designed the schema for.

**Evidence question:** can a run be reconstructed well enough to answer a
question we have not thought to ask yet?

Contract: `docs/10-technical/02-observability-event-model.md` (v0).
Decomposition + task state: `docs/PROGRESS/M2-observability-foundation.md`.

## What's here now (pre-M4)

The spec pins four mandatory event kinds; this directory makes them concrete and
testable in isolation, ahead of anything real to record (that arrives at M4).

| File | Role |
|---|---|
| `event_model.py` | `RunRecorder` — append-only writer for the four event kinds + human correction. Stdlib only. |
| `reconstruct.py` | Reader + queries: per-actor ordered history, per-intent lineage, safety interventions, and an "unplanned question" demo. |
| `selftest.py` | Builds a synthetic run (orchestrator → implementer → reviewer, one effect realized, one gate-refused) and asserts the reconstruction guarantees hold. |
| `runs/` | Output. One directory per run: `run.json` (header) + `events.jsonl` (one record per line). Git-ignored except `.gitkeep`. |

Run the self-test (Windows or WSL):

```
python experiments/M2-observability-foundation/selftest.py
```

## Record store shape (M2 task 2 — decided, illustrative)

**JSONL, one file per run.** `runs/<run_id>/events.jsonl`, one JSON object per
line, plus a `run.json` header. Rationale:

- Append-only line-per-event matches the "ordered history, reconstructable per
  actor and per intent" requirement without a database.
- Trivially greppable and diffable; a run is a self-contained directory.
- Total order within a run is an explicit per-run monotonic `seq`, not wall-clock.
- It is illustrative, not normative (`10-technical` conventions): M4 volume and
  query patterns may force a different store. The `RunRecorder` / `reconstruct`
  split is where that swap would happen.

## Deferred to M4

Wiring the recorder into a real processor run, and the actual reconstruction
check on that run (task 7), then the findings-log entry (task 8). The self-test
here exercises the same queries against a synthetic run so the model is not
untested until M4.
