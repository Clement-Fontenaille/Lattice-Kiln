# Entry 1 — Milestone 0: Characterize the local inference envelope

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

**Addendum, 2026-09-15 — first non-Qwen model, same host, same cliff.**

`experiments/M0-inference-envelope/results/runs/ollama__nemotron-nano-9b-v2-q4kl__Q4_K_L__8192__1.json`.
NVIDIA Nemotron Nano 9B v2 (hybrid Mamba-2/attention, ~4 attention layers,
community Q4_K_L GGUF, 6.75 GB on disk / ~7.3 GB loaded) at `num_ctx=8192`:
`ollama ps` reports a 15%/85% CPU/GPU split, not fully resident, with only
480 MB of the 8 GB card free once loaded. Generation measured at **12.7
tok/s** (prompt eval 104.1 tok/s) — inside the cliff this entry already
names (resident 7B-class: 41–52 tok/s; spilled: 1–5 tok/s), landing as a
shallower partial spill rather than the full collapse. This is the first
measurement on this host of a model that is neither Qwen2.5-Coder nor sized
to this envelope's already-characterised 3B/7B/14B ledge — first evidence
that **the VRAM-fit cliff is a property of the host, not of the Qwen family
specifically**: a different architecture (hybrid Mamba-2, not a plain
transformer) hit the same wall at a size (9B) between the two ledges this
entry already measured (7B fits, 14B does not).

Not yet measured, and worth a real run rather than an assumption: whether
reducing `num_ctx` below 8192 restores full GPU residency for this model the
way it would be expected to from this entry's own "VRAM fit is a hard
binary" reading — a natural next data point for this file, not yet taken.
Left open rather than assumed, per this entry's own point 1: the constraint
is a binary edge, and untested proximity to it is not the same as having
measured which side of it a given `num_ctx` lands on for THIS model's KV
cache shape (which differs from Qwen's, given the hybrid architecture).

**Addendum, 2026-09-15 (same day) — a smaller-labelled quant did not move
the number.**

`.../runs/ollama__nemotron-nano-9b-v2-bartowski-q4km__Q4_K_M__8192__1.json`.
Went looking for the obvious next step from the addendum above — pull the
smaller Q4_K_M quant (community card figures: ~5.51 GB, versus Q4_K_L's
~6.4–6.75 GB) and see whether it fits fully resident at `num_ctx=8192`. It
did not resolve cleanly either way: this specific build (bartowski's HF repo,
pulled via `ollama pull hf.co/...`) loads at **6.5 GB on this host**, not
~5.51 GB — quant-size labels are not comparable across maintainers/repos
without checking the actual loaded size, which this entry had been treating
as interchangeable with the label. Generation measured at 12.9 tok/s,
statistically indistinguishable from Q4_K_L's 12.7 tok/s. `ollama ps`'s
CPU/GPU split was not captured live (checked after Ollama's idle-unload had
already evicted the model) — so full/partial residency for THIS run is
circumstantial from the near-identical speed, not confirmed the way the
Q4_K_L run's residency was. Also newly measured: a cold model-switch
between two different Nemotron quants cost **128 s** — well above this
entry's own 17–30 s Qwen model-switch figures, though those measured warm
switches between already-resident Qwen sizes, not a first cold load of a
different architecture entirely, so the two numbers are not a clean
before/after of the same thing.

Net: two Nemotron quants now measured, neither confirmed fully resident,
neither clearly faster than the other. The open question from the first
addendum (does a smaller `num_ctx` restore residency for this model) is
still open — quant size alone was not the lever this pass hoped it would
be, and checking `ollama ps` DURING generation rather than after is now a
prerequisite for the next data point to actually answer the residency
question instead of leaving it circumstantial again.

**Addendum, 2026-09-15 (same day) — llama.cpp resolves the residency
question Ollama left circumstantial, and finds a real context ceiling.**

Went straight at the open question above with the tool built for exactly
this (`harness/bench-llamacpp.sh`'s own reasoning: "the GPU/CPU offload
split — the main thing Ollama hides — comes from the ... 'offloaded N/M
layers' load line," a direct load-time report, not a racing poll). llama.cpp
(build f1793c1) recognises the architecture natively as `nemotron_h 9B Q4_K
- Medium` (8.89B params, 6.28 GiB) — this build supports Nemotron-H, not
assumed going in.

*Getting a clean read required one detour.* The direct `/mnt/e/...` mmap
path (E: is this host's rotational drive) never completed even after ~13
CPU-minutes — the same "intractable to benchmark" pattern entry 1 already
named for 14B, just triggered by a slow physical disk instead of model size
this time. Copying the 6.7 GB GGUF once onto WSL's own SSD-backed filesystem
(`~/m0-models/`) fixed it completely; every number below is post-copy.

*Runs.* `.../runs/llama.cpp__nemotron-h-9b__Q4_K_M__128__ngl99__{pp,tg}.json`
(also the two `__skip.json` files for the wall, below):

| context (`-p`) | prefill tok/s | gen tok/s |
|---|---|---|
| 128    | 55.6   | **42.65** |
| 4,096  | 705.9  | 68.4 |
| 16,384 | 1011.0 | 46.9 |
| 32,768 | 1168.2 | 48.5 |
| 65,536 | 1093.5 | 51.9 |
| 98,304 | — | killed after 12m, no result |
| 131,072 (nominal ceiling) | — | killed after 13m, no result |

Two results, not one:

1. **The residency question is answered, cleanly.** 42.65 tok/s at `-ngl 99`
   versus Ollama's 12.7–12.9 tok/s on the identical model/quant earlier the
   same day. The bottleneck measured that morning was **Ollama's automatic
   layer-placement heuristic**, not the model or the host — it was leaving
   15% on CPU when the model fits fully resident. Generation speed at small
   context now sits close to this entry's own Qwen 7B range (41–52 tok/s),
   which is the fair comparison this file has been missing all day.
2. **Context scales flat, then falls off a cliff — later than expected, and
   softer than expected.** From 128 to 65,536 tokens (a 512× increase),
   gen_tok_s stayed in a tight 42–68 band with no downward trend — the
   hybrid-Mamba hypothesis from earlier in this same day's conversation
   (near-constant KV-cache cost) holds up under an actual measurement, not
   just an architecture-diagram argument. But at 98,304 and at the nominal
   128K ceiling, both runs sat at 100% GPU / <110 MiB VRAM free and never
   produced a result within 12–13 minutes each, despite never hitting a hard
   CUDA OOM error. This is **entry 1's binary-cliff finding, confirmed on a
   second architecture, but manifesting as a throughput collapse rather than
   a crash** — extrapolating from the 65,536 rate, 98,304 should have taken
   under two minutes, not failed to finish in twelve. The wall on this host
   for this quant sits somewhere in **(65,536, 98,304]**, not at the
   model's advertised 128K, and "still fits in VRAM" and "still usable" are
   not the same claim near that edge.

**A second, unplanned data point: `.wslconfig` matters for this whole
exercise.** WSL2's undocumented-by-default memory ceiling (~50% of host RAM
absent a `.wslconfig`) was implicated in the reboot that interrupted an
earlier pass of this same addendum — 5.7 GiB claimed by the VM alone on an
11.9 GB host, no headroom left once the user's normal background load was
added back in. Capped to `memory=4608MB` (the decimal form `4.5GB` is
rejected by WSL2's own parser — silently falls back to default rather than
erroring loud, worth knowing) via `%USERPROFILE%\.wslconfig` + `wsl
--shutdown`. All numbers in the table above were taken under the capped
config; the sweep showed no sign the tighter host-RAM ceiling cost anything
on the CUDA side, which is expected since `-ngl 99` keeps the model off host
RAM almost entirely, but is worth recording as untested-until-now.

**A third data point, same day — the KV-cache growth rate itself, measured
directly.** `nvidia-smi` polled live (not after the fact) during clean,
fully-completed runs at two context sizes gives two real anchors instead of
the noisy pair of mid-collapse snapshots from the wall runs above (those two
disagreed with each other — 131,072 showed *less* VRAM used than 98,304 —
and are not trustworthy for this):

| context | model weights | KV cache | total VRAM |
|---|---|---|---|
| 32,768 | 6,300 MiB | 1,000 MiB | 7,300 MiB |
| 65,536 | 6,300 MiB | 1,522 MiB | 7,822 MiB |

Growth rate: **16.3 KiB/token** — small enough that linear extrapolation
projects 200 MiB of headroom remaining only around **~76,000 tokens**
(~74k), well past where the wall above was already known to bite (somewhere
in (65,536, 98,304]) but still short of the nominal 128K. This is a capacity
projection from two points assuming a constant rate, not a throughput
guarantee — the wall runs already show compute-buffer behaviour near the
edge does not extrapolate linearly from the clean region, so a direct
measurement at ~76–80K is the natural next check, not yet taken, before this
number is trusted for anything load-bearing.

**Fourth pass, same day — the wall narrowed, and the projection checked
against real points either side of it.** A third clean live-polled anchor at
49,152 (7,605 MiB used, 385 MiB free, 46.97 tok/s — sits right on the same
line as the 32,768/65,536 pair) confirms the growth rate is stable across
three points, not just two, with a slightly uneven per-segment rate (19.1
KiB/token 32,768→49,152; 13.6 KiB/token 49,152→65,536) that is still the
same order of magnitude throughout. Then the actual wall was bracketed
directly: **73,728 reproduces the 98,304/131,072 stuck-at-100%-GPU pattern**
(122→88 MiB free, no result after 3+ minutes, killed) while **65,536 itself
is confirmed genuinely fine**, not merely "not yet failed" — 172 MiB free,
48–52 tok/s, matching its neighbours. **The wall narrows from
(65,536, 98,304] to (65,536, 73,728]** — the ~76K linear projection for 200
MiB headroom landed inside this narrower bracket, which is closer support
for the capacity model than the single wide bracket alone gave, but the
throughput side of that projection (whether generation stays healthy, not
just whether the allocation succeeds) is still unconfirmed in this exact
window.

**Fifth pass, same day — llama-server with two concurrent slots, not one
solo stream.** Building `llama-server` (previously not built — the original
harness only targeted `llama-bench`; `cmake -DLLAMA_BUILD_SERVER=ON .` plus
a `cmake --build . --target llama-server` was in fact the ~2-minute
incremental rebuild it was expected to be once the missing CMake option was
found, reusing the already-compiled CUDA objects) opened a question the
single-stream sweep above could not answer: does *concurrent* serving of
two independent contexts cost VRAM per-slot, or does it share the loaded
weights the way the M6 Ollama queue work earlier this same day showed
Ollama doing for a single model? Two runs, `-np 2` with
`--kv-unified-per-slot` set to 16,384 then 32,768 (unified KV pool sized to
`n_parallel * kv_unified_per_slot`), each fired via two genuinely
simultaneous HTTP requests (confirmed independent by `id_slot: 0`/`id_slot:
1` in the two responses):

| condition | per-slot ctx | total KV pool | VRAM used | vs. matching solo stream |
|---|---|---|---|---|
| 2 concurrent | 16,384 | 32,768 | 7,394 MiB | 7,300 MiB (solo @32,768) |
| 2 concurrent | 32,768 | 65,536 | 7,863 MiB | 7,822 MiB (solo @65,536) |

Both conditions completed successfully (no OOM, no hang) with VRAM
essentially identical to a solo stream at the sum of the two slots'
contexts — **the weights load once and are shared across slots**, so on
this 8 GB card, two concurrent Nemotron sessions cost the same VRAM as one
session at their combined size, not double. Throughput was asymmetric and
lower per-slot than solo (16,384-pair: 7.0 / 27.8 tok/s; 32,768-pair: 3.2 /
14.2 tok/s, versus ~47–52 tok/s solo at matching sizes) — continuous
batching interleaves the two requests' compute rather than running them
independently, so this is what concurrent serving actually delivers per
request, not two independent solo measurements. One further observation
worth a dedicated check later, not yet controlled for: the 2×32,768 pair
(combined context 53,206 actual tokens processed) completed without
hanging, inside a total-context zone a solo single stream cannot yet be
assumed to tolerate past 73,728 — whether concurrent serving genuinely
tolerates more *combined* context than one solo stream at the same total,
or whether this pair simply stayed under the wall by chance of prompt
length, is not yet distinguished.
