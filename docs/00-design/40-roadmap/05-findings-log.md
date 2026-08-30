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
