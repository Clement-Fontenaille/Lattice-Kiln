# Status

_Updated: 2026-08-31_

## Where we are

**MVP target:** Milestones 0 through 5 — a local assistant using ephemeral role-specific processors under a language-model orchestrator, on measured hardware, fully observable, on a safety floor.

**MVP slice COMPLETE.** M0–M5 done, findings-log entries 1–6, first sequence
rework written (`40-roadmap/06-sequence-rework-01.md` — no reordering).

**Current milestone:** M6 — Persistent work and knowledge (first past the MVP slice; not yet decomposed).

**What the MVP established:**

- M0: inference envelope — 7B Q4/Q5 ≤16k, ~40 tok/s; VRAM-fit a hard binary with
  a ~10–20× offload cliff; per-role model switching not viable.
- M1: baseline environment scripted, verifies green in place; clean-machine
  replay owed (post-MVP backlog).
- M2: append-only event model + recorder; 40 real runs reconstructable, including
  for unplanned questions — **when the effect envelope carries structured
  outcome, not just prose** (entries 3, 6).
- M3 (reduced form): deterministic deny-list gate + capability model + provisional
  invariant list; every real effect routed through it; 3/9 effect types seen, all
  carved cleanly; gate never tripped on benign supervised work (entry 4). Full
  form owes the M9 items.
- M4: processor runtime; a non-looping planner→implementer→reviewer chain **did
  not beat a monolith** (5/8 vs 6/8) at ~3× cost; independent review with no
  revision edge was inert (entry 5).
- M5: LLM orchestrator over that runtime — **7/8 vs monolith 6/8 vs fixed chain
  5/8**, the +1 entirely from adaptive retry on the hard tasks, at ~5× cost;
  understandable for acting, weak for stopping (entry 6).

## Milestone board

| Milestone | State | Decomposed |
|---|---|---|
| M0 — Local inference envelope | **DONE** (2026-08-30) — findings-log entry 1 | yes — `M0-inference-envelope.md` |
| M1 — Reproducible baseline environment | **DONE** (2026-08-30) — findings-log entry 2 (verdict inconclusive; clean-machine replay owed) | yes — `M1-baseline-environment.md` |
| M2 — Observability foundation | **DONE** (2026-08-30) — findings-log entry 3 | `M2-observability-foundation.md` |
| M3 — Invariant floor (reduced form for MVP) | **DONE (reduced form)** (2026-08-30) — findings-log entry 4; full form owes M9 items | `M3-invariant-floor.md` |
| M4 — Ephemeral processor experiments | **DONE** (2026-08-30) — findings-log entry 5 (verdict inconclusive, leaning weakens) | `M4-ephemeral-processors.md` |
| M5 — Intelligent orchestration experiments | **DONE** (2026-08-31) — findings-log entry 6 (verdict confirms, narrowly) | `M5-intelligent-orchestration.md` |
| — first sequence rework — | **DONE** (2026-08-31) — no reordering | `40-roadmap/06-sequence-rework-01.md` |
| M6 — Persistent work and knowledge | TODO | no |

## Immediate next actions

MVP slice closed. Next is **M6 — Persistent work and knowledge** (now *current*;
*current + 1* is M7). Per the cadence: write M6's evidence question, decompose it,
then spec only what M6 and M7 need. M6 adds durable structure — intent, work,
observations, evidence, findings, proposals, decisions, artifacts, memory — "only
as far as necessary to support real use cases". It is the first consumer of the
"structured outcome, not prose" observability lesson (entries 3, 6) and of the
`declined` vs `blocked` distinction now in spec `08`.

## Blockers

- None. Ollama native + llama.cpp from source in WSL are in place
  (`experiments/M0-inference-envelope/setup/README.md`). The M2 recorder, M3
  floor, M4 processor runtime, and M5 orchestrator are all built and exercised on
  real runs — M6 builds on that stack.

## Post-MVP backlog (consolidated in `40-roadmap/06-sequence-rework-01.md`)

Scheduled by the milestone that needs each, not a separate track:

- **Hardware as a variable** (findings 1, 2) — replayable re-bootstrap + envelope
  re-characterisation on different hardware; what may depend on host numbers.
- **Clean-machine M1 replay** (finding 2) — the definitive from-nothing test, when
  a second controlled machine is available.
- **Observability envelope contract** (findings 3, 6) — structured outcome, not
  free text, on every effect envelope. `10-technical/02` open contracts, via M6.
- **Orchestrator stopping semantics** (finding 6) — `declined` ≠ `blocked`, stop
  rationale required; in spec `08`, validate at the M4/M5 re-test inside M7/M8.
- **Editor-agent frontend choice** (finding 2) — weigh a documented
  `config.yaml`-first alternative to Cline; owner is the bootstrapper design.
- **M9 debt** (finding 4) — sequence-check hardening, gate-alter, accumulation
  threshold, literature-grounding pass — all in Milestone 9 as planned.
- **M4/M5 re-test at larger N** with the revision loop + non-naive context —
  folded into M7/M8, not a new milestone.

## Recently done

- **MVP slice closed (M0–M5)** — first sequence rework written
  (`40-roadmap/06-sequence-rework-01.md`): no reordering; post-MVP backlog
  consolidated.
- **M5 workflow-suite re-test** — `experiments/M5-intelligent-orchestration/`:
  `fixture_workflow/` (6 workflow-shaped tasks), `roles_v2.py` (tuned prompts),
  `workflow_suite.py` (3 arms, N=3, 54 runs). Finding: decomposition helps on
  multi-file / multi-concern work (wf1, wf6), pure overhead elsewhere, 5–7× the
  calls; monolith drops docs+TODO under load (wf6: 0/4, 0/3). Findings-log entry
  6 addendum. Gaps logged on specs 07/08 (repetition rule, planner over-block,
  conversational-handoff degradation).
- **M5 executed and closed** — `experiments/M5-intelligent-orchestration/`:
  `orchestrator.py` (LLM loop over the M4 runtime, decision record per step),
  `compare.py` (3 arms), `strategy_check.py`. 24 runs. Orchestrated 7/8 vs
  monolith 6/8 vs fixed chain 5/8, win = adaptive retry, ~5× cost. Specs
  `10-technical/08-orchestrator-contract.md`, `09-orchestrator-runtime-boundary.md`.
  Findings-log entry 6. Design touch: `03-orchestrator.md`; spec `08` gained a
  required stop-rationale and `declined` ≠ `blocked`. M2 hardened (`close()` no
  longer re-reads `run.json`; `Run` tolerates a lost header).
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
