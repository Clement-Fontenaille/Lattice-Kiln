# Findings Log

## TL;DR

One entry per completed milestone, recording what its evidence question actually answered and what that answer touches. This is the empirical counterpart to the research and evaluation agenda.

> **Motto:** A milestone closes when it has taught us something, and this is where we write down what.

## How this log is used

The execution cadence routes findings design-first: an entry here is written when a milestone completes, and its consequences then flow into the relevant design document, then into the specification's open contracts, then — at a scheduled rework point — into the milestone sequence itself.

An entry is appended, never rewritten. If a later milestone contradicts an earlier finding, that contradiction is a new entry that references the old one.

## Entry format

Each entry provides:

- **Milestone** — number and name.
- **Evidence question** — copied from the milestone, so the entry stands alone.
- **What the evidence said** — the observed result, in plain terms.
- **Verdict** — against the relevant hypothesis in the research and evaluation agenda, one of: confirms, weakens, refutes, inconclusive. "Inconclusive" is a legitimate and useful outcome.
- **Touches** — which design documents and which specification open contracts this finding bears on.
- **Runs** — reference to the reconstructable observability run or runs the finding rests on.

## Entries

### Entry 1 — Milestone 0: Characterize the local inference envelope

**Date:** 2026-08-30

**Evidence question:** what is the real local inference envelope, and how tight is
the constraint the constrained-intelligence thesis assumes?

**What the evidence said.**

On the measured host (RTX 2070 SUPER, 8 GB VRAM; AMD FX-8300; 11.9 GB RAM), the
envelope has a single binding constraint — **VRAM fit — and its edge is a cliff,
not a slope**:

- Models that fit entirely in 8 GB run well: Qwen2.5-Coder **3B** at Q4 or Q8
  generates 53–73 tok/s at every context size up to 32k; **7B** at Q4 or Q5
  generates 41–52 tok/s up to 16k context. These are fully GPU-resident
  (`size_vram == size`, no offload).
- The moment weights or KV cache spill to system RAM, generation collapses to
  **1–5 tok/s** — a 10–20× penalty, because CPU offload on the FX-8300 is that
  much slower. This hits 7B Q8 and 14B Q4 at any context (they do not fit at
  all), and it hits 7B Q4/Q5 at **32k context**, where the KV cache pushes the
  footprint past 8 GB. There is no graceful middle ground.
- Large context is bounded by **prefill latency**, not generation throughput:
  the 3B holds 67 tok/s at 32k but takes ~13 s to first token; 7B takes 40 s+.
- **Model switching costs 17–30 s** (unload is ~0.1 s; the cost is the incoming
  model's cold load: 3B ~18 s, 7B ~30 s, 14B ~54 s) — 3–6× the 5 s threshold set
  for orchestration. One 7B→14B switch crashed the inference subprocess.
- Running inference alongside a synthetic dev-environment load costs **−3.4%**
  while the model fits (generation is on the GPU); a sustained 11-minute session
  drifts **−11%** (GPU thermal/clock).
- An independent llama.cpp cross-check agrees with Ollama within 7% on the
  resident 7B numbers. The intended llama.cpp offload-curve sweep on 14B could
  not be run at all — `llama-bench` did not finish one iteration in 180 s — which
  is itself evidence that 14B is impractical on this host.

**Verdict: confirms** (against the constrained-intelligence thesis,
`10-foundations/01-constrained-intelligence-thesis.md`). The thesis assumes "a
constrained local model cannot reliably hold [a large repo, long history, complex
plan, ...] in one context window" and that spending system design to save model
capacity is worthwhile. The measurement confirms the constraint is real and
binding — and sharpens it in three ways the design set should absorb:

1. The constraint is **VRAM residency as a hard binary**, not a soft capacity
   budget. Design that assumes graceful degradation under memory pressure is
   wrong here; the system must keep the working model + its KV cache strictly
   within 8 GB or accept a 10–20× cliff.
2. The **practical ceiling is a 7B-class model at Q4/Q5, ~16k usable context**,
   ~44 tok/s. That is a workable local coding assistant — but a narrow ledge.
3. **Per-role model switching is not viable** at 17–30 s per swap. Cognitive-role
   differentiation must come from prompt/context within one resident model, not
   from swapping models. This is a direct, quantified input to Milestone 5
   (intelligent orchestration) and to the orchestrator/runtime boundary spec.

**Touches.**

- Design: `10-foundations/01-constrained-intelligence-thesis.md` — add that the
  measured constraint is binary (VRAM fit) with a ~10–20× offload cliff, and that
  model-switch cost (~20–30 s) makes single-resident-model orchestration the
  default posture. `10-foundations/04-context-as-governed-resource.md` — the
  32k-context cliff for 7B is a concrete cost for the context budget to respect.
- Specification open contracts: the **orchestrator and runtime boundary**
  (execution-cadence backlog item 8) should record model-switch cost as a known
  constraint and treat per-role model assignment as out of scope for the MVP
  hardware. The **observability event model** (backlog item 1, next) should be
  able to record which model/quant served an invocation and whether it was
  offloaded, since that predicts latency by 10–20×.
- Milestone sequence: no reordering now. M1 (reproducible environment) inherits
  the `setup/` scripts as its seed. M4/M5 experiments should pin the working
  default to 7B Q4_K_M or Q5_K_M at ≤16k context. **For the post-MVP
  (end-of-M5) rework:** treat hardware as a variable — the envelope numbers here
  are one host's, and there is no replayable procedure yet for re-bootstrapping
  the environment and re-characterising the envelope on a different machine. See
  the Bootstrapping section of `02-open-questions-register.md`.

**Runs.** `experiments/M0-inference-envelope/results/` — `host.json`,
`runs/*.json` (schemas `m0-run/1`, `m0-switch/1`, `m0-concurrent/1`,
`m0-drift/1`), aggregated in `summary.md`. Harness, protocol, and setup scripts
committed alongside under `experiments/M0-inference-envelope/`.

### Entry 2 — Milestone 1: Reproducible baseline development environment

**Date:** 2026-08-30

**Evidence question:** can the baseline be reconstructed from scripts without
manual repair, and where does reproducibility actually break?

**What the evidence said.**

The environment — WSL2 + CUDA toolchain, llama.cpp built from source, Ollama
(native Windows), the pinned Qwen2.5-Coder model set, VS Code + Cline — is now
described by a declarative manifest (`experiments/M1-baseline-environment/manifest.json`,
schema `m1-manifest/0`) and stood up by an ordered, idempotent provisioning
orchestrator (`provision/provision.ps1`, six steps). `provision.ps1 -VerifyOnly`
passes green on the reference host: every component present at the pinned
version, GGUF digests verified against `models.json`, Cline configured to the
baseline (model / 16k context / 60 s timeout, auto-approval effectively off,
telemetry off).

It has **not** been run from scratch on a clean machine — verify-mode confirms
the host matches the manifest, not that the scripts built it from nothing. No
second machine is available now; a controlled clean-environment replay is owed
and tracked (`STATUS.md` → Post-MVP rework backlog).

Where reproducibility needs a human or a host-specific workaround (the
substantive finding):

1. **Driver + WSL bootstrap is not scriptable.** The NVIDIA Windows driver with
   WSL GPU support and `wsl --install -d Ubuntu-24.04` are operator actions; the
   scripts verify them, they do not install them.
2. **One privileged step.** `sudo apt-get install build-essential
   nvidia-cuda-toolkit jq` inside WSL — isolated to step 10, reported, never
   silent, but needs an interactive password.
3. **Stale WSL distro registration.** Registered as `Ubuntu-22.04`, actually
   running 24.04. Every `wsl -d` call hard-codes the misleading name; a clean
   install of `Ubuntu-24.04` would not match without editing the scripts.
4. **Tool-specific config formats.** Cline stores config as JSON under
   `~/.cline/data/`, but `globalState.json` mixes settings with host-specific
   state (workspace paths, commit hashes, migration records) and has no published
   schema — the committed template is a curated capture. An already-configured
   Cline is not auto-reconciled to the baseline; two toggles were manual. (This
   finding took three passes to get right — first "not scriptable", then wrong
   location — a caution that reverse-engineering a tool's storage deserves
   evidence, not assumption.)
5. **pip fragility on this WSL.** `python3-venv` absent, bare `pip3` had a broken
   SSL path; the working form `python3 -m pip --user --break-system-packages` is
   baked in but is a host-specific workaround.
6. **Write-ordering hazards.** Step 50 must run with VS Code closed or Cline
   overwrites the templates. The orchestrator enforces this; a naive script
   would not.

**Verdict: inconclusive** — on the literal question (reconstruction without
manual repair), because the definitive clean-machine run has not happened. What
*is* established: the scripted surface verifies green and is complete, and the
manual surface is fully enumerated (six items above). That enumeration is the
useful output — it is the concrete input to the bootstrapper.

**Touches.**

- Open questions: `40-roadmap/02-open-questions-register.md` → Bootstrapping
  ("Which parts belong in scripts vs. declarative config vs. local knowledge?" —
  M1 gives a first partition; "How portable across machines?" — untested).
- The eventual bootstrapper design document: the manifest is the proto-artifact;
  findings 1–6 are its backlog.
- Milestone sequence: no reordering. M1 is closed on "scripts complete + verified
  in place + breaks enumerated"; the clean-environment replay is deferred to the
  post-MVP rework, alongside the hardware-as-a-variable item.

**Runs.** `experiments/M1-baseline-environment/` — `manifest.json`,
`provision/` (orchestrator + six steps + `config/cline/` templates),
`run-reports/*.json` (schema `m1-provision-run/0`, git-ignored locally; the
green `-VerifyOnly` run of 2026-08-30 is the reference).

### Entry 3 — Milestone 2: Observability foundation

**Date:** 2026-08-30

**Evidence question:** can a run be reconstructed well enough to answer a question
we have not thought to ask yet?

**What the evidence said.**

The M2 recorder (`experiments/M2-observability-foundation/event_model.py`, schemas
`m2-run/0` / `m2-event/0`) was wired into the M4 processor runtime and recorded
**16 real runs** (4 tasks × 2 arms × 2 repetitions). Reconstruction was then
tested with questions the schema was not shaped around
(`experiments/M4-ephemeral-processors/reconstruction_check.py`), answered from
`events.jsonl` alone:

- **Q1 — did the independent reviewer's verdict agree with the objective
  outcome?** Answering it joins the reviewer's conclusion record (a type-4
  realized effect) with the harness root's final objective-check record (a type-2
  realized effect). Neither record references the other; the join is ad hoc.
  Answerable — it surfaced 2/8 ephemeral runs where the reviewer approved a run
  that objectively failed.
- **Q2 — for every refused proposed effect, which role proposed it, which layer
  stopped it, and did the run still pass?** Join across `invocation.role` ×
  `proposed_effect.disposition` × the final check. Answerable — all 17 refusals
  were capability-layer planner/reviewer overreach; several of those runs still
  reached their objective.

Per-actor and per-intent lineage reconstructed cleanly (harness root → planner /
implementer / reviewer as children under one `intent_ref`). The
safety-intervention category stayed distinct: the plumbing test's synthetic
`gate_refusal` was recorded as its own kind with `retry_eligible=False`, never
folded into task failure.

One real gap: the first recorded pass stored the processor's conclusion with only
a free-text `summary`, so "did the reviewer approve?" degraded to string
-sniffing. Adding a structured `verdict` to the type-4 effect envelope fixed it.

**Verdict: confirms** — a run is reconstructable well enough to answer questions
nobody designed the schema for, **provided the effect envelope carries the
structured result and not just prose**. The reconstruction is exactly as good as
what the envelope was told to hold.

**Touches.**

- Design: `20-cognitive-architecture/06-observability.md` — the reconstruction
  requirement holds up in practice; add that the recorded form of an effect must
  carry its *structured* outcome, since ad-hoc cross-record joins are how
  unplanned questions get answered.
- Specification open contracts (`10-technical/02-observability-event-model.md`):
  **the four-property / envelope carrier** contract is load-bearing — sharpen it,
  do not close it. **Hypothesis linkage** — Q1/Q2 were answered by hand-written
  joins; a first-class `experiment_id` / run-tag would have made them one-liners.
  Still deferred, now with a concrete motivating case.
- Milestone sequence: no reordering. M2 tasks 7–8 are now closed by this entry.

**Runs.** `experiments/M4-ephemeral-processors/results/results.json` (committed),
`reconstruction_check.py`, per-run records under
`experiments/M4-ephemeral-processors/runs/` (schema `m2-run/0`, git-ignored; the
2026-08-30 N=2 set is the reference). Recorder + synthetic self-test:
`experiments/M2-observability-foundation/`.

### Entry 4 — Milestone 3: Invariant floor (reduced MVP form)

**Date:** 2026-08-30

**Evidence question:** do the enumerated effect types carve cleanly when real
effects flow through the gate, or does the boundary between types blur under use?

**What the evidence said.**

Across the same 16 real runs, every effect a processor actually produced mapped
unambiguously to one of three of the nine types: **workspace mutation (1)**,
**process execution (2)**, and **work-record mutation (4)** — the latter carrying
the processor's own conclusion. No effect was ambiguous between types; no needed
effect was missing from the vocabulary.

- The deny-list **gate never fired** (0 gate refusals in 16 runs). A human
  supervised benign tasks; nothing crossed a hard constraint.
- The **capability layer** refused **17 proposed effects** — every one a planner
  or reviewer instance trying to write a file or run a command outside its
  type-4-only grant. This confirms the spec-03/04 division of labour in practice:
  capability (adjustable, role-keyed) sits above the gate and caught all role
  overreach; the gate (non-adjustable, effect-keyed) was never reached.
- One boundary question surfaced, as the milestone anticipated: **is a
  processor's conclusion an effect at all?** M4 modelled it as type 4 so it flows
  through the same pipeline and lands in the record. Defensible — type 4 already
  covers "attaching a finding, proposal, or decision" — but it is a choice the
  vocabulary document did not force.

**Verdict: inconclusive, leaning confirms.** The types carved cleanly for the
effects actually seen, but (a) only 3 of 9 types were exercised, (b) the gate
itself saw no real adversarial effect — its deny-list remains only synthetically
tested — and (c) the one blur was resolved by fiat, not by the boundary being
self-evident.

**Touches.**

- Design / spec: `10-technical/01-effect-vocabulary.md` — record that a cognitive
  component's *recorded conclusion* is a type-4 work-record mutation; the open
  contract "does type 4 stay one type" gains a data point (it held for
  findings/conclusions here). `20-cognitive-architecture/07-invariant-enforcement.md`
  — the "gate binds effects, not roles" split worked, but the MVP gave the gate
  no real test; the composition / sequence-check hardening (now Milestone 9) still
  owes a run with genuine gate trips.
- Milestone sequence: no reordering. M3's reduced-form tasks are closed; the
  deferred items (sequence hardening, gate-alter, accumulation, literature pass)
  remain with Milestone 9.

**Runs.** As entry 3, plus `experiments/M3-invariant-floor/` (specs + gate +
selftest) and `reconstruction_check.py` Q2.

### Entry 5 — Milestone 4: Ephemeral processor experiments

**Date:** 2026-08-30

**Evidence question:** do ephemeral roles, fresh context, and independent review
beat a monolithic agent on a small task set?

**What the evidence said.**

Setup: `qwen2.5-coder:7b-instruct-q4_K_M` (the M0 working default), naive context
assembly (spec `07`), a **fixed planner → implementer → reviewer chain with no
revision loop**, versus a single monolithic implementer. 4 synthetic tasks
(implement-from-stub, bug-fix-behind-a-failing-test, false-premise, context
-starvation), 2 repetitions, both arms, objective pass/fail per task.

- **Objective pass rate: monolith 6/8, ephemeral 5/8.** An earlier single-rep
  pass ran 3/4 vs 4/4. Across every pass the ephemeral split **never clearly won**
  — it matched or trailed.
- **Cost: ephemeral spent 3× the model calls** (24 vs 8) and **~3× wall-clock**
  (mean ~23 s vs ~7 s per task).
- **False-premise task: both arms, every repetition, correctly declined** and left
  the pre-existing passing tests green. A clean positive for the design claim
  that the correct response to a task may be *not to execute it*
  (`20-cognitive-architecture/01-work-intent-and-task-model.md`) — independent of
  the ephemeral question.
- **Context starvation** (a helper in a file naive assembly does not surface) hurt
  both arms (monolith 1/2, ephemeral 0/2). **No processor ever emitted a context
  request** (0 / 16 runs) — the "ask for missing context" affordance is specified
  and wired but went entirely unused.
- **Independent review**: the reviewer's verdict tracked the objective outcome in
  6/8 ephemeral runs (2 false approvals on the starvation task). But with no
  revision loop in the reduced MVP form, even a correct "needs-change" changed
  nothing — review was **recorded, not consumed**.

**Verdict: inconclusive, leaning weakens** (against "ephemeral roles improve
reasoning quality", `40-roadmap/03-research-and-evaluation-agenda.md`). At this
scale, with deliberately poor context and a non-looping chain, role separation
added latency and cost with no measurable quality gain. It does **not** refute the
hypothesis: N is tiny, variance is high (the trivial task flipped pass/fail
between runs), context assembly is intentionally weak, and the chain has no
feedback edge. The likely missing piece is the reviewer→implementer revision loop
plus better context — not the role split itself.

**Touches.**

- Design: `20-cognitive-architecture/02-processors.md` — record that a
  *non-looping* planner→implementer→reviewer chain did not beat a monolith on
  small tasks, and that independent review with no revision loop is inert.
  `10-foundations/04-context-as-governed-resource.md` — the "processor can request
  missing context" behaviour needs to be prompted or required, not merely
  available (0/16 uptake); it also gave the naive baseline a concrete cost
  (task_4).
- Specification: feeds the **orchestrator contract** (Milestone 5) — a real
  orchestrator is where the reviewer's "needs-change" would route back — and
  **Milestone 7** (naive context measurably cost the starvation task).
- Milestone sequence: no reordering now. The end-of-Milestone-5 rework should
  weigh adding a revision loop to the ephemeral arm before re-running this
  comparison at larger N.

**Runs.** `experiments/M4-ephemeral-processors/` — `fixture/` (task set, schema
`m4-tasks/0`), `harness.py`, `results/results.json` + `results/summary.md`,
`reconstruction_check.py`; per-run records under `runs/` (schema `m2-run/0`,
git-ignored; the 2026-08-30 N=2 set is the reference).

### Entry 6 — Milestone 5: Intelligent orchestration experiments

**Date:** 2026-08-31

**Evidence question:** does natural-language orchestration beat a fixed workflow
while staying understandable, and where does its overhead start to exceed the
benefit of decomposition?

**What the evidence said.**

An LLM orchestrator (observe → decide the next operation → spawn a processor via
the M4 runtime → integrate → stop; capability set `{6, 4}`; a decision record per
step) was compared against the M4 fixed planner→implementer→reviewer chain and
the monolith. Same 7B model, same naive context, same 4-task fixture, N=2, 24
runs.

- **Objective pass: orchestrated 7/8, monolith 6/8, fixed chain 5/8.** Across M4
  and M5 this is the first arm to beat the monolith.
- **The win is one task and it has a legible mechanism.** On `task_4_starve`
  (context starvation — monolith 0/2, fixed chain 0/2) and `task_2_median`, the
  orchestrator spawned a **second implementer** after the first attempt failed
  the objective check — the reviewer→implementer revision loop that findings-log
  entry 5 identified as the missing piece. `task_4` went 0/2 and 0/2 → **2/2**
  under orchestration.
- **Cost: ~5× the model calls (40 vs 8) and ~4.5× wall-clock** (25.5 s vs 5.7 s
  mean). On the three tasks the monolith already one-shots, orchestration added
  4–6 calls and 15–35 s for no net benefit. **Overhead exceeds benefit on any
  task a single pass can solve; it pays off only where the simpler arms fail.**
- **Understandable — with one gap.** `strategy_check.py` reconstructs every run's
  strategy (which operation each step, and the rationale for every spawn) from
  the decision records alone, consistent with the invocation lineage. But **7 of
  8 stop decisions recorded no rationale**: the orchestrator explains why it
  *acts*, not why it considers the work *done*.
- **False-premise handling regressed.** The monolith and the fixed chain both
  explicitly *declined* `task_3_nobug` ("the claimed bug does not exist"). The
  orchestrator reached the right outcome (stopped, touched nothing, tests stayed
  green) but via `terminal_state: blocked` ("no useful next step") — with a
  correct rationale in one rep, none in the other. Its stopping rules do not
  distinguish "this rests on a false premise" from "I am stuck".

**Verdict: confirms, narrowly** (against "orchestration can compensate for model
limits" / "natural-language orchestration beats a fixed workflow",
`40-roadmap/03-research-and-evaluation-agenda.md`). NL orchestration beat both the
fixed chain and the monolith; the margin is +1/8, within N=8 noise; and the gain
is entirely explained by adaptive retry on tasks the other arms fail. It stays
understandable for the acting half of the loop and is weak on the stopping half.
The overhead is only justified when a single pass would fail.

**Touches.**

- Design: `20-cognitive-architecture/03-orchestrator.md` — record that adaptive
  retry (routing a failed attempt back to a fresh implementer) is where
  natural-language orchestration earned its overhead at this scale, and that
  stopping / `declined` reasoning is the weak spot (the orchestrator conflates
  "false premise" with "stuck").
- Specification: `10-technical/08-orchestrator-contract.md` — the decision record
  MUST carry a rationale for **stop** decisions, not only spawns (open contract →
  normative); add an explicit `declined` terminal state distinct from `blocked`,
  each with a required reason. `10-technical/02-observability-event-model.md` —
  the decision record is another instance of the "structured outcome, not prose"
  lesson from entry 3.
- Milestone sequence: this closes the MVP slice (M0–M5). The first scheduled
  rework follows — `40-roadmap/06-sequence-rework-01.md`.

**Runs.** `experiments/M5-intelligent-orchestration/` — `orchestrator.py`,
`compare.py`, `strategy_check.py`, `results/results.json` + `results/summary.md`;
per-run records under `runs/` (schema `m2-run/0`, git-ignored; the 2026-08-31
three-arm N=2 set is the reference).

#### Addendum (2026-08-31) — workflow-suite re-test

The first M5 comparison used four single-concern katas that fit one clean
context — the monolith's home turf (finding: the earlier caveat that the
baseline favours the monolith). A follow-up re-test used six **workflow-shaped**
tasks (cross-file bug, feature-with-a-design-choice, refactor-trap,
stale-assumption, partial-credit parser, and a multi-concern task = algorithm +
docstrings + TODO gardening in one file), scored by **subtests passed** plus, for
the multi-concern task, separate **doc** and **TODO** scores. Arms: monolith, a
**fixed** planner→(implementer↔reviewer up to 3 rounds) loop, and the
orchestrator — all on tuned role prompts (`roles_v2.py`), N=3, 54 runs.

Tuning was required first. The untuned fixed sequence lost to the monolith on
3/5 tasks; diagnosis from the transcripts:

- the implementer **narrated instead of writing** ("Fixed the function by…", no
  FILE block) whenever its context carried any conversational text — a plan, a
  critique, a prior summary. The monolith writes reliably because its context is
  only objective + code. Fix: the fixed flow no longer injects the planner's
  prose into the implementer; retry hints go into the objective, not a separate
  "additional input" block.
- the reviewer **rubber-stamped** empty implementations. Fix: an empty
  written-file list is now an automatic `needs-change`, plus a deterministic
  harness guard that forces a retry when no real file was written.
- the planner wrote **past-tense completion claims** that primed the chain toward
  false-done, and the 7B ignores "don't use past tense" — so the harness blunts
  the completion phrasing before it propagates.

**What the tuned re-test showed.** Aggregate: monolith 10/18 objective pass
(67/87 subtests, 18 calls), fixed 11/18 (76/87, 83 calls), orchestrated 12/18
(77/93, 129 calls). Cost of decomposition: **4.6× the model calls for the fixed
loop, 7.2× for the orchestrator**.

Per task the benefit is narrow and concentrated:

- **wf3, wf4, wf5** (single-concern, one clean pass suffices): decomposition is
  pure overhead — identical scores, 3–8× the calls. Consistent with finding 5.
- **wf1** (cross-file indirection): the monolith patched the symptom file twice
  and scored 3.0/5; the review loop caught the wrong-layer fix and both
  decomposed arms hit 5/5. **Decomposition helps.**
- **wf6** (multi-concern): the monolith produced **syntactically invalid Python
  on every run** and scored 2/6 algo, **0/4 docs, 0/3 TODO** — it dropped the
  secondary concerns entirely while failing the primary one. The fixed loop hit
  6/6 algo, 2/4 docs, 3/3 TODO; the orchestrator 6/6, 1.5/4, 2.5/3. **This is the
  clearest positive for decomposition in the whole milestone** and it directly
  confirms the "a monolith degrades on secondary concerns under load"
  hypothesis.
- **wf2** (feature design choice): a regression. The orchestrator scored 0/5 on
  two of three runs — it spawned the *planner* 4–6 times consecutively without
  ever reaching an implementer, because (a) the tuned planner over-returns
  `blocked` on a normal "add a feature that doesn't exist yet" task and (b)
  `run_orchestrated` does not implement the repetition stopping rule spec `08`
  requires. The fixed loop also stalled here (3.7/5).

**Revised reading of the M5 verdict.** "Confirms, narrowly" stands, but the shape
is now clearer: decomposition's benefit is **real, concentrated on multi-file and
multi-concern work, and invisible-to-negative everywhere else**, at 5–7× the
cost. The orchestrator's extra flexibility buys a further small gain on the
hardest task (wf6, 2/3 vs the fixed loop's 1/3) and one real failure mode (wf2).
Neither the orchestrator nor the fixed loop decisively beats the other (12 vs 11
on pass, 83% vs 87% on subtests). At 7B/N=3, per-cell score noise is large
(wf5 monolith: 1/7, 5/7, 7/7 on identical inputs) — the reliable signal is in the
**transcript mechanisms**, not the score deltas.

**Also touches.**

- `10-technical/08-orchestrator-contract.md` — the **repetition stopping rule**
  ("same operation N times without progress → stop") is normative but was not
  implemented; wf2 is the concrete failure. The planner's terminal-state guidance
  needs "a capability the code does not yet have is the normal case, not a reason
  to block".
- `10-technical/07-naive-context-assembly.md` — a 7B implementer is **degraded by
  any conversational context** (plan, critique). Role-to-role handoff cannot be
  raw prose; this is a constraint on how the context assembler frames prior-step
  output.
- Milestone sequence: still no reordering. `40-roadmap/06-sequence-rework-01.md`
  decision 2 (fold the M4/M5 re-test into M7/M8) is updated with this first pass.

**Runs.** `experiments/M5-intelligent-orchestration/` — `workflow_suite.py`,
`roles_v2.py`, `fixture_workflow/` (schema `m5-workflow-tasks/0`),
`results_workflow/results.json` + `summary.md`; per-run records under `runs/`
(git-ignored; the 2026-08-31 three-arm N=3 set is the reference).

### Entry 7 — M5 follow-up: attractor census + judge-lab

**Date:** 2026-09-01

**Evidence question (self-set, feeding the goal re-evaluation):** the static role
system is weak at 7B — before deciding what waits on better hardware, can it be
*tuned* to useful output? Specifically: where does the 7B reliably go for each
role-relevant task shape (so a role can be pointed with the current, not against
it), and can the judgment step be rescued by voting, per-clause structure, or
execution grounding?

**What the evidence said.**

Two wide first-pass experiments on the M0 working default
(`qwen2.5-coder:7b-instruct-q4_K_M`).

*Attractor census* (`experiments/M5-intelligent-orchestration/census/`, 39 probes
× K=3 = 117 calls): task shape × framing, scoring the *motion* not correctness.

- **Doer — "emit the whole corrected file" is a strong, correct current.** On the
  cross-file bug (symptom in one file, cause in another) all bare samples fixed
  the right file with the right logic; cross-file indirection did not break it.
  A plan or critique in a *named, structured* section did not suppress file
  emission (partial walk-back of entry 6's "any conversational context degrades
  the 7B implementer" — that effect was specific to unlabelled mid-context
  injection).
- **Doer — one clean blind spot: false premises.** "Rewrite `find()` to O(log n)"
  on unsorted data: 3/3 implemented binary search, 0/3 noticed the precondition.
  It executes the objective's surface and never tests its premise.
- **Doer — multi-concern overloads it** (1/3 kept all three concerns of wf6) and
  it is blind to concerns it was not handed (single-concern passes echo the other
  concerns' stale state back unchanged).
- **Judge — no framing fixes it.** A shared-helper dedupe that silently rounds
  (`staff_price(1.567)`: 1.2536 → 1.25, a real regression) was approved 3/3 under
  every framing: `is_correct`, `predict_failure` (output: `PASS`),
  `strongest_reason`, and `criteria_first` — the last **actively harmful**: it
  reverse-engineered its acceptance criteria from the buggy code's own docstring,
  then declared them met, and separately false-rejected a *correct* simple fix
  2/3. The judge is not noisy; it is **systematically biased toward approval** and
  asserts the property it was asked to verify.
- **The planner stance engages the critical read the implementer suppresses** —
  same model, same task: 2/3 flag the false premise (vs implementer 0/3), 3/3
  keep all three wf6 concerns (vs implementer 1/3).

*Judge-lab* (`experiments/M5-intelligent-orchestration/judge_lab/`, 10 known
-truth scenarios × 4 pipelines): baseline reviewer / K=5 vote / deterministic
prechecks + model checklist + per-clause panel without the test / same with the
real test output.

- **baseline 4/10, vote 4/10 (verdict-identical on all 10 rows), ground_notest
  3/10, ground 6/10 (+2 escalate).**
- **Voting is dead** — errors are systematic, not zero-mean; K=5 at higher
  temperature changed no verdict.
- **The deterministic core alone — parse / import / claim-vs-diff / trust the
  `test_task.py` result — scores 9/10 with zero model calls.** Adding the 7B
  checklist+panel *drops* it to 6/10: the checklist codifies false premises as
  requirements (rejects the correct wf4 linear scan despite a 5/5 test), and the
  panel emits confident-wrong `not_met` on correct code (miscounts `range(0+1)`).
- The panel's one real use: given a *known* failing test line it writes a
  correct, cited explanation — a reporting aid, not a decision aid.

**Verdict: confirms** (the post-MVP recalibration in
`40-roadmap/06-sequence-rework-01.md`, and against "orchestration/decomposition
can compensate for model limits",
`40-roadmap/03-research-and-evaluation-agenda.md`). A 7B does the *doing* with
scaffolding and **cannot do the *judging*, and the gap is not a prompt away** —
neutral, adversarial, structured, and voted framings all fail the same way, and
per-clause structure without execution grounding makes it worse. The one lever
that works is running the test and trusting it; the model near the judgment seat
is limited to explaining a known failure. Premise-soundness is a planner-pass
concern. This sharpens rather than changes the recalibration: the self-improving
loop waits on a **second judgment source** — a stronger/reasoning model as
reviewer (enabled by the planned second GPU) or the model tier improving — not on
further prompt tuning of the 7B reviewer.

**Touches.**

- Design: `20-cognitive-architecture/02-processors.md` — record that role
  differentiation on a 7B works for producing (implementer) and for critical
  analysis under a *planning* framing, but not for verdict-style review;
  `20-cognitive-architecture/03-orchestrator.md` — a feedback loop's evaluation
  edge cannot be a same-model reviewer verdict on this hardware.
- Specification open contracts: `10-technical/07-naive-context-assembly.md` — the
  "prior-step handoff framing" contract gains detail (a plan in a *named section*
  is tolerated; unlabelled prose is not); `10-technical/08-orchestrator-contract.md`
  — a `declined` outcome for a false premise should be reachable from a planner
  pass, not expected from the implementer or a reviewer; add that automated-check
  results, where they exist, outrank any model verdict.
- Milestone sequence: no reordering. Directly feeds the **goal re-evaluation**
  (the next task): the M6–M8 "promising signal on 7B" bars in
  `06-sequence-rework-01.md` should treat the judgment step as human-or-stronger
  -model, not a 7B self-review, and the second-GPU / reasoning-reviewer path moves
  from "nice to have" toward "the gating dependency for the self-improving tier".

**Runs.** `experiments/M5-intelligent-orchestration/census/` (`probes.py`,
`run_census.py`, `summary.md`, `FINDINGS.md`, `runs/` transcripts) and
`.../judge_lab/` (`scenarios.py`, `lab.py`, `results.md`, `FINDINGS.md`, `runs/`
detail). Single-host, single 7B, 2026-09-01.

#### Addendum (2026-09-01) — loop control (bundle D)

Following the judge-lab result (reviewer verdict unreliable, test result 9/10),
the implement↔review loop was rebuilt to run off the measurable signal
(`experiments/M5-intelligent-orchestration/loop_lab/`). Three arms on the six
workflow tasks, N=2: `oneshot` (implementer once), `naive_loop`
(`(reviewer→implementer)*` while the reviewer says needs-change — the current
`fixed` behaviour), and `d_loop` (bundle D: the pre-existing repo state is an
entrant in the keeper pool and a round is accepted only if it *beats* it;
continue only on measurable progress; one stalled round → stop and escalate;
ship the best snapshot ever seen, not the last; fix hints are the real failing
test lines).

- **d_loop: 0 regressions in 12 runs; `naive_loop`: 2** — both on wf6, where the
  review/fix loop drove the implementer to non-parsing Python and the reviewer
  **approved it**. An unreliable reviewer driving a loop amplifies damage; a
  test-gated keeper caps it at "no worse than the incumbent".
- **wf4 (false premise) solved by construction, 0 model calls** — the incumbent
  linear scan passes 5/5, so d_loop's loop never runs. It does not need to
  *recognise* the false premise; it refuses a change that does not beat a passing
  incumbent. `naive_loop` reached 5/5 too but spent 4–6 calls.
- **~3.4× cheaper than `naive_loop`** (14 vs 48 calls / 36 runs): stops on a
  green test, not on a reviewer's approval, and skips the loop when the incumbent
  passes.
- **d_loop's worst case is honest** (wf6: `no-improvement`, keeps the untouched
  original, escalates) vs `naive_loop`'s (ships broken, "approved").

Two limits: (a) **"first do no harm" degrades to "do nothing" when the check does
not capture the deliverable** — wf3 is a behaviour-preserving refactor, its test
passes on the un-refactored original, so d_loop no-ops it; behaviour-preserving
work needs a structural check or a human. (b) `STALL_TOL=1` stops too early on
climbable tasks (wf5: 5/7 vs `naive_loop` 7/7) — a tuning knob.

This does not change the entry-7 verdict; it is the constructive half. The loop
for a 7B fixed sequence: gate on the test not the reviewer, keep the incumbent as
the floor, escalate on stall. `10-technical/08-orchestrator-contract.md`'s
repetition stopping rule gains a concrete, working implementation
(progress-gated). The unresolved case — no executable check for the objective —
points at the "generate the missing tests, blind, K-way" follow-up.

**Runs.** `.../loop_lab/` (`lab.py`, `results/summary.md` + `results.json`,
`FINDINGS.md`).

#### Addendum (2026-09-02) — super-pipeline (every idea, always on)

To find the ceiling of stage-stacking, `experiments/M5-intelligent-orchestration/pipeline_lab/`
runs all the promising ideas in one call-heavy flow (premise audit + task-type
classify · dual blind impl-specs · alignment check · K-way blind test synthesis ·
`here_is_file` + concern-split + best-of-2 coding · execute + K-way check
agreement + regression guard · context-diverse structural verify with
probe-confirmation · deterministic reconcile + **counterfactual attribution** —
each run replays reconciliation with each signal nulled to see which flips the
terminal). 6 workflow tasks × N=2, ~16–29 calls/task.

- **Net vs the cheap `loop_lab` d_loop: worse or tied on 5 of 6 tasks, better on
  1.** The unique win is **wf6 (multi-concern): 6/6 algo + ~3.5/4 docs + ~2.5/3
  TODO** where every prior arm scored ≤ 2/6 — via **concern-splitting + a keeper
  scored on `sub+doc+todo`, not subtests alone**. wf3 (refactor) got a more
  honest terminal (`escalate` — "behaviour preserved, cannot confirm the dedupe")
  than d_loop's silent no-op.
- **It regressed two solved tasks** (wf2, wf5: d_loop 5/5 → pipeline 0/5) because
  its coding stage **violated finding 6**: it injected the plan into the
  implementer's context (→ empty output, the documented narration failure) and
  used `here_is_file` framing — a *fix-an-existing-file* current — for greenfield
  implementation.
- **Counterfactual attribution: over 12 runs only `premise_unsound` (×2, correct
  wf4 declines), `l2_violated` (×2, both FALSE positives — a model-written probe
  exited 1 and "confirmed" a hallucinated violation) and `l1_provided_fail` (×1)
  ever decided a terminal.** The dual impl-specs, the alignment check, and the
  blind test synthesis changed **zero** outcomes — ~7 calls/run of dead weight.
  Blind synthesis was inert because its suites crash on an unfinished
  implementation before emitting any `CHECK` line.
- **Regressions vs baseline: 0/12** — the incumbent-protected keeper held through
  all the added complexity.

**Reading:** a **negative result with a precise payload.** Stage-stacking does not
beat the cheap loop except on the one task class (multi-concern) that needs a
specific mechanism, and unconditioned stages either sit inert or actively regress
by ignoring earlier findings. This is exactly the calibration data Milestone 7
(static supervised workflow) was inserted to consume: spine = d_loop; add premise
audit always, concern-split + combined-score keeper for conjunctive objectives,
"no behavioural signal → escalate" for refactors; drop the three inert stages;
never let a lone model probe flip a terminal.

**M5 investigation arc — closed.** Entry 6 answered the milestone's evidence
question; entry 7 and its three addenda (workflow re-test, loop control,
super-pipeline) established what a 7B-class static workflow can and cannot do and
named the Milestone 7 component. Sequence rework 2 (`07-sequence-rework-02.md`)
acts on it.

**Runs.** `.../pipeline_lab/` (`superpipe.py`, `roles_super.py`,
`results/summary.md` + `results.json`, `runs_super/` per-run ledgers +
transcripts, `FINDINGS.md`).
