# Status

_Updated: 2026-08-30_

## Where we are

**MVP target:** Milestones 0 through 5 — a local assistant using ephemeral role-specific processors under a language-model orchestrator, on measured hardware, fully observable, on a safety floor.

**Current milestone:** M4 — Ephemeral processor experiments.

**State:** M0 and M1 complete (findings-log entries 1 and 2). M2 and M3 are
**built ahead of the milestone that exercises them (M4)**, as the execution
cadence intends for observability and the floor — their evidence questions and
findings-log entries defer to M4, when real runs and real effects exist.

- M0: local inference envelope measured — VRAM-fit is a hard binary with a
  ~10–20× offload cliff, working default 7B Q4/Q5 at ≤16k, switch cost 17–30 s.
- M1: baseline environment scripted (`experiments/M1-baseline-environment/` —
  manifest + 6-step provisioning orchestrator), verifies green in place; the
  definitive clean-machine replay is deferred to the post-MVP rework.
- M2: observability event model v0 (`10-technical/02-observability-event-model.md`)
  + standalone recorder and reconstruction queries
  (`experiments/M2-observability-foundation/`), self-tested on a synthetic run.
- M3: three spec docs (`10-technical/03`, `04`, `05`) + a thin deterministic
  deny-list gate, capability model, and provisional invariant list
  (`experiments/M3-invariant-floor/`), self-tested on synthetic effects (every
  H1–H7 / R1–R3 clause exercised). Literature-grounding pass moved to Milestone 9.
- M4: spec docs written (`10-technical/06-processor-contract.md`,
  `07-naive-context-assembly.md`); decomposed (`M4-ephemeral-processors.md`).
  **Blocked on an operator decision about the task set** before the runtime and
  comparison harness get built — M4 is the first milestone that runs real model
  inference, and it answers the M2, M3, and M4 evidence questions at once.

## Milestone board

| Milestone | State | Decomposed |
|---|---|---|
| M0 — Local inference envelope | **DONE** (2026-08-30) — findings-log entry 1 | yes — `M0-inference-envelope.md` |
| M1 — Reproducible baseline environment | **DONE** (2026-08-30) — findings-log entry 2 (verdict inconclusive; clean-machine replay owed) | yes — `M1-baseline-environment.md` |
| M2 — Observability foundation | **built** — spec v0 + recorder + self-test; evidence check deferred to M4 | `M2-observability-foundation.md` |
| M3 — Invariant floor (reduced form for MVP) | **built** — specs 03/04/05 + deny-list gate + self-test; evidence check deferred to M4 | `M3-invariant-floor.md` |
| M4 — Ephemeral processor experiments | **WIP** — specs 06/07 written; blocked on task-set decision | `M4-ephemeral-processors.md` |
| M5 — Intelligent orchestration experiments | TODO | no |

## Immediate next actions

M4 specs (`10-technical/06`, `07`) are written and M4 is decomposed. The next
step needs an **operator decision on the task set** (`M4-ephemeral-processors.md`
→ "Open decision"):

1. Throwaway synthetic repo, or a real small repo to point at?
2. Is 6–10 tasks / N=3 repetitions an acceptable inference budget on this host,
   or start smaller (4 tasks, N=2)?
3. Any task types to specifically include or exclude?

Once the task set is pinned: build the processor runtime (Ollama client + effect
routing through `experiments/M3-invariant-floor/enforce.py` + event recording via
`experiments/M2-observability-foundation/event_model.py`), the tiny role library,
the naive context assembler, and the arm-A/arm-B comparison harness; run the set;
then answer the M2, M3, and M4 evidence questions from the committed runs
(findings-log entries 3, 4, 5).

## Blockers

- **M4 task set.** Building the M4 comparison harness is paused pending an
  operator decision on the task set (three questions above). Not a hard blocker —
  the runtime, role library, and naive assembler can be built against a
  placeholder task first if preferred.
- M0's runtime-install blockers are resolved (Ollama native + llama.cpp built
  from source in WSL via apt `nvidia-cuda-toolkit`; see
  `experiments/M0-inference-envelope/setup/README.md`).

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

- **M4 specs written + decomposed** — `10-technical/06-processor-contract.md`
  (processor input/output envelope, lifecycle, bound to effect type 6 and the
  kind-1 record) and `07-naive-context-assembly.md` (the deliberately simple v0
  context baseline for M7). `PROGRESS/M4-ephemeral-processors.md` lays out the two
  arms and the three converging evidence questions.
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
