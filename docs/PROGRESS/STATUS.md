# Status

_Updated: 2026-08-30_

## Where we are

**MVP target:** Milestones 0 through 5 — a local assistant using ephemeral role-specific processors under a language-model orchestrator, on measured hardware, fully observable, on a safety floor.

**Current milestone:** M5 — Intelligent orchestration experiments (last of the MVP slice).

**State:** M0–M4 complete (findings-log entries 1–5). Only M5 remains in the MVP
slice.

- M0: local inference envelope — VRAM-fit is a hard binary with a ~10–20× offload
  cliff, working default 7B Q4/Q5 at ≤16k, switch cost 17–30 s.
- M1: baseline environment scripted, verifies green in place; clean-machine
  replay deferred to the post-MVP rework.
- M2: observability event model + recorder, exercised on 16 real M4 runs;
  unplanned questions answerable from records **when the effect envelope carries
  structured outcome, not just prose** (entry 3).
- M3 (reduced MVP form): capability model + deny-list gate + provisional invariant
  list; every M4 effect routed through it. Effect types carved cleanly for the
  3/9 seen; the gate never tripped on benign supervised tasks; the capability
  layer caught all role overreach (entry 4). Full form still owes the M9 items.
- M4: monolith vs a fixed planner→implementer→reviewer chain (no revision loop),
  7B + naive context, 4 tasks × N=2. **Ephemeral did not beat the monolith**
  (5/8 vs 6/8) at ~3× cost; both arms correctly declined a false-premise task;
  the "ask for missing context" affordance went unused 16/16 (entry 5).

## Milestone board

| Milestone | State | Decomposed |
|---|---|---|
| M0 — Local inference envelope | **DONE** (2026-08-30) — findings-log entry 1 | yes — `M0-inference-envelope.md` |
| M1 — Reproducible baseline environment | **DONE** (2026-08-30) — findings-log entry 2 (verdict inconclusive; clean-machine replay owed) | yes — `M1-baseline-environment.md` |
| M2 — Observability foundation | **DONE** (2026-08-30) — findings-log entry 3 | `M2-observability-foundation.md` |
| M3 — Invariant floor (reduced form for MVP) | **DONE (reduced form)** (2026-08-30) — findings-log entry 4; full form owes M9 items | `M3-invariant-floor.md` |
| M4 — Ephemeral processor experiments | **DONE** (2026-08-30) — findings-log entry 5 (verdict inconclusive, leaning weakens) | `M4-ephemeral-processors.md` |
| M5 — Intelligent orchestration experiments | TODO | no |

## Immediate next actions

M5 — Intelligent orchestration experiments, the last MVP milestone.

1. Spec `10-technical/08-orchestrator-contract.md` — what the orchestrator
   receives (itself under context governance), what it decides, how it mediates
   discussion, synthesis, stopping rules. (Cadence backlog item 7.)
2. Spec `10-technical/09-orchestrator-runtime-boundary.md` — the seam flagged as
   highest value; the reasoning-vs-runtime validation-depth question. (Item 8.)
3. Build an LLM orchestrator that drives the M4 processor runtime: it chooses the
   next cognitive operation instead of a fixed planner→implementer→reviewer
   chain, and — per M4 finding — can route a reviewer's "needs-change" back.
   Compare against both the M4 fixed chain and the monolith on the same fixture
   task set (extend it if needed).
4. Evidence question: does natural-language orchestration beat a fixed workflow
   while staying understandable, and where does its overhead exceed the benefit?
   → findings-log entry 6, then the end-of-M5 sequence rework.

## Blockers

- None. Ollama native + llama.cpp from source in WSL are in place
  (`experiments/M0-inference-envelope/setup/README.md`). M4 established the
  processor-runtime + gate + recorder stack that M5's orchestrator drives.

## Post-MVP rework backlog (end of M5)

- **Hardware as a variable.** M0 and M1 were characterised against one host.
  Define the replayable procedure to re-bootstrap the environment and
  re-characterise the inference envelope on different hardware, and identify what
  in the design set is allowed to depend on host-specific envelope numbers. See
  `40-roadmap/02-open-questions-register.md` → Bootstrapping, and findings-log
  entry 1.
- **Editor-agent frontend choice.** M1 names Cline. M1 finding 1: Cline's config
  is file-based JSON but the schema is undocumented and UI-first, so the baseline
  needs a one-time manual capture step. Weigh a `config.yaml`-first, documented
  alternative (e.g. Continue.dev) at the rework. Not an M1 change — Cline stays
  for the MVP, worked around by capture-and-replay of its settings JSON. The
  project runs its own orchestrator loop from M5 on, so this frontend is MVP
  scaffolding, not a long-term dependency.

## Recently done

- **M4 executed and closed** — `experiments/M4-ephemeral-processors/`: processor
  runtime (`processor.py`) driving `qwen2.5-coder:7b` through the M3 floor and M2
  recorder; naive context assembler; fixed role library; 4-task synthetic fixture;
  `harness.py` ran 4 tasks × 2 arms × 2 reps. `reconstruction_check.py` answered
  two unplanned questions from records. Findings-log entries 3, 4, 5. Design
  touches: `01-effect-vocabulary.md` (conclusion = type 4), `02-processors.md`,
  `04-context-as-governed-resource.md`, `06-observability.md`.
- **M4 specs + decomposition** — `10-technical/06-processor-contract.md`,
  `07-naive-context-assembly.md`.
- **M3 built (reduced MVP form)** — `10-technical/03-capability-authority-model.md`,
  `04-enforcement-gate.md`, `05-provisional-invariant-list.md` (normative);
  `experiments/M3-invariant-floor/` — `invariants.json` + capability model +
  deterministic deny-list gate + enforcement pipeline + self-test (35 assertions,
  every H1–H7 / R1–R3 clause exercised, Windows + WSL). Evidence question and
  findings-log entry deferred to M4.
- **M2 built** — `10-technical/02-observability-event-model.md` v0;
  `experiments/M2-observability-foundation/` — `RunRecorder` + reconstruction
  queries + synthetic self-test. Record store shape decided (JSONL per run).
  Reconstruction check against a real run and the findings-log entry deferred to M4.
- **M1 executed and closed** — `experiments/M1-baseline-environment/`: declarative
  manifest + `provision.ps1` (6 idempotent steps: WSL/GPU, apt+pip prereqs,
  llama.cpp+GGUF via M0 scripts, Ollama, models, VS Code+Cline). Full
  `-VerifyOnly` run green. Cline config located (`~/.cline/data/`), templates
  captured + curated. Findings-log entry 2.
- **M0 executed and closed** — harness bugs fixed on first live run, Ollama
  matrix swept (staged), llama.cpp cross-check, concurrent/drift passes, envelope
  description + findings-log entry 1.
- Conceptual integration pass (review notes 02–03) — committed `b098e91`.
- Execution cadence, findings log, technical-spec kickoff, milestone rework — committed `b098e91`.
