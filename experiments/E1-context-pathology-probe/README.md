# E1 — Can context pathology be detected from processing?

**Sheet:** [`docs/00-design/40-roadmap/03-research-and-evaluation/E1-context-pathology-probe.md`](../../docs/00-design/40-roadmap/03-research-and-evaluation/E1-context-pathology-probe.md)
**Status:** not run.
**Feeds:** `10-foundations/04`'s failure modes and M9's metric.

## The sheet's eventual experiment, and why this folder is not it

E1's full design is a **probe battery**: five stress classes (calculus,
contradiction, missing-context, overload, false-premise) with matched
present/absent pairs, tested against a pre-registered detection ordering. That
needs a probe apparatus that does not exist, and — per the discussion of
2026-09-16 — it also needs the probe's **feature space** to be specified, which
it never has been anywhere in this repository. Attention weights? Hidden-state
activations? Output logprobs? The sheet says "probe" throughout and never says
which.

**That is a blocking gap, not a detail.** Nothing in the battery can be built
until it is settled, and settling it is a design decision, not a search.

## What this folder does instead — the first move

Validate the **context blur** claim, which is narrower, already partly evidenced,
and answerable from data on disk:

> Degradation under load is not global failure. It is **selective silent
> omission, biased toward dropping low-salience requirements.**

The existing evidence is a single anecdote: M5's `wf6_multi`, where monolith
drops docs and TODO gardening (0/4, 0/3) while still delivering the core
objective. One task, one arm. If that pattern does not generalise, the probe's
target class needs rethinking before any apparatus is built for it.

## What the data is (verified 2026-09-17)

**Primary — the anecdote's own home:**
`experiments/M5-intelligent-orchestration/pipeline_lab/results/results.json`
— 12 rows, 6 `wf*` tasks × 2 reps, carrying explicit **per-requirement** fields:
`doc`, `todo`, `baseline_sub`, `final_sub`, `sub_tot`, plus `total_calls`,
`signals`, `ledger`.

**Secondary — wider but shallower:**
`experiments/M6-evaluation-suite/results/<arm>.json` — 18 arms, whose `struct`
field carries per-requirement dimensions as `{"NAME": [earned, total]}`.
Populated on only ~6–10 tasks per arm.

## The honest weakness, stated up front

**There is no clean load axis in the recorded data.** The M6 arms vary
*scaffold*, not load. Any "load" variable must be constructed from task
properties (requirement count, `worker_view`, cross-file `stresses`), which makes
this an observational check for whether the pattern exists at all — **not** a
controlled dose–response. A positive result here motivates a controlled
experiment; it does not substitute for one.

## Layout

```
E1-context-pathology-probe/
  README.md      this file
  PROTOCOL.md    the first move, step by step
  blur.py
  results/
```
