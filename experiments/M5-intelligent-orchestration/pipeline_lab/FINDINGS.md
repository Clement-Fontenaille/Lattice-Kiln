# Super-pipeline v2 (pipeline_lab) — findings

**Date:** 2026-09-02
**Model:** `qwen2.5-coder:7b-instruct-q4_K_M`. 6 workflow tasks × N=2 = 12 runs,
~16–29 model calls/task, 60–250 s/task.
**Question:** with *every* promising idea folded into one deliberately call-heavy
flow (premise audit, dual blind impl-specs, alignment check, K-way blind test
synthesis, `here_is_file` + concern-split + best-of-2 coding, execution + K-way
verification + regression guard, context-diverse structural verify, deterministic
reconcile + counterfactual attribution) — what actually moves the outcome?

Table: `results/summary.md`. Per-run transcripts + ledgers: `runs_super/`.

## Result vs the cheap `loop_lab` d_loop

| task | d_loop | super-pipeline | verdict |
|---|---|---|---|
| wf1 crossfile | 5/5 ×2 | 5/5 code ×2 (rep1 terminal `needs-change` — **false** `l2_violated`) | tie on code, pipeline noisier |
| wf2 retry | **5/5 ×2** | **0/5 ×2** | **pipeline regressed a solved task** |
| wf3 refactor | 5/5 but did no refactor (silent no-op) | `escalate` ×2 (5/5 behaviour, can't confirm the dedupe) | **pipeline's terminal is more honest** |
| wf4 false premise | kept incumbent, 0 calls | `declined` ×2, 3 calls | tie (pipeline cleaner) |
| wf5 partial | 6.0/7 mean | 2.5/7 mean | **pipeline regressed** |
| wf6 multi-concern | 2/6 | **6/6 algo, 3.5/4 docs, 2.5/3 TODO** | **pipeline's unique win** |

**Regressions vs baseline: 0/12** — the incumbent-protected keeper held through
all the added complexity.

## What the counterfactual attribution says

Every run replays S7 reconciliation with each signal nulled, logging which flip
the terminal. Over 12 runs the load-bearing signals were:

- `premise_unsound` ×2 (both wf4 — correct declines)
- `l2_violated` ×2 (**both false positives** — wf1 rep1 and wf6 rep1 had correct
  final code; a model-written probe exited 1 and "confirmed" a hallucinated
  violation)
- `l1_provided_fail` ×1

**S1 (test-spec), S2 (dual blind impl-specs), S3 (alignment), S4 (K-way blind
test synthesis) changed a terminal outcome zero times in 12 runs** — ~7 model
calls and ~50 s per run of dead weight. S4's `synth_trusted_fail` never fired:
the synthesised suites crash on an unfinished implementation (ImportError / raised
`NotImplementedError`) before emitting `CHECK` lines, so there is nothing to
agree on. As built, S4 is inert.

## Why wf2 / wf5 regressed — a stage violated an established finding

The S5 transcripts are unambiguous. `S5-impl-a-seg0r0` for wf2:

```
### prompt: "... Plan (follow it):\n 1. Add a `retries` parameter ...\n 2. ...\n"
### response: ```json  (empty)
```

The implementer emitted an **empty JSON fence — no code**. This is exactly
findings-log entry 6's finding: *a 7B implementer stops emitting effects when its
context carries conversational text (a plan, a critique)*. `roles_v2.py` and
`workflow_suite.py` were built to avoid it — they never inject the plan.
`superpipe`'s `_here_is_file` helper put `Plan (follow it):\n{plan}` straight into
the step objective and reintroduced the failure. Two compounding errors in one
stage:

1. **plan injected into the implementer's context** → narration / empty output
   (the entry-6 finding);
2. **`here_is_file` framing used for greenfield implementation** — the census
   showed it is a *fix-an-existing-file* current; pinning "here is the current
   file: `raise NotImplementedError`, change only what's needed" biases a 7B
   toward a minimal non-edit.

wf2 and wf5 are the two "implement from a stub" tasks, so they took the full hit.
The monolith and d_loop solve them because their implementer context is only
objective + code.

## The one real win, and why it worked

**wf6 (multi-concern)** — 6/6 algo plus most of the docs and TODO gardening, both
reps, where every prior arm scored ≤ 2/6 and dropped the secondary concerns
entirely. The mechanism: **concern-splitting** (`(1)…(2)…(3)` → one implementer
pass per concern over the previous output) **combined with a keeper scored on
`sub + doc + todo`, not `sub` alone**. Before the combined score, the
docstring/TODO passes couldn't raise the subtest count so the keeper discarded
them. This is the census finding (7B holds 1/3 concerns; give it one at a time)
turned into a working mechanism.

## Consequences for Milestone 7 (static supervised workflow)

The evidence names the component precisely:

- **Spine = `loop_lab` d_loop**: test-gated iteration, incumbent-protected keeper,
  escalate-on-stall. It already captures most of the value at 1–3 calls/task.
- **Add, fired conditionally:**
  - **premise audit** (S0) — always; cheap, catches wf4, load-bearing 2/12.
  - **concern-split + combined-score keeper** — only when the objective is
    conjunctive; this is the wf6 win.
  - **"no behavioural signal → escalate"** — for `refactor` / no-test tasks; this
    is the honest wf3 terminal.
- **Drop:** S2 (dual impl-specs), S3 (alignment), S4 (blind synth as built) —
  zero outcome influence in 12 runs.
- **Fix before reuse:** S5 must not inject the plan into the implementer and must
  use plain framing for greenfield (`here_is_file` for edits only). S6b must not
  let a lone model-written probe flip the terminal to `needs-change` — the two
  `l2_violated` load-bearing cases were false positives.
- **Cost target:** the conditionally-staged workflow should land near d_loop's
  call count on simple tasks and only pay the concern-split / L2 premium where a
  task class needs it.

The always-on super-pipeline is a **negative result with a precise payload**:
more stages did not beat the cheap loop except on the one task class (multi-
concern) that needs a specific mechanism, and two stages actively regressed
solved tasks by ignoring prior findings. That is the calibration data Milestone 7
was defined to use.
