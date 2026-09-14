# M7 — Static supervised workflow (execution record)

_Opened 2026-09-13. Moves to `archives/` on completion._

> Execution state for [M7](../00-design/40-roadmap/01-MILESTONES/completed/07-static-supervised-workflow.md).
> What the milestone *is* lives there; what it *taught us* goes to
> [`50-findings/`](../00-design/50-findings/README.md). This file is the working
> record and is rewritten freely.

## Where it stands

| Step | State |
|---|---|
| 1. Specify the workflow | **done** — [`10-technical/11-static-workflow.md`](../10-technical/11-static-workflow.md) v0, back half only |
| 2. Build it | **done** — `experiments/M7-static-workflow/m7_workflow.py` |
| 3. Run on the M6 suite | **done** — `experiments/M6-evaluation-suite/results/m7.{json,md}` |
| 4. Findings entry | **done** — [entry 10](../00-design/50-findings/10-m7-static-workflow.md) |

**M7 is complete.** Verdict: *confirms narrowly, and the instrument is the bigger
result.*

The front half is not in scope and is an open contract in the specification. Its
third prerequisite is `10-foundations/04`'s context-quality question, which makes
[M9](../00-design/40-roadmap/01-MILESTONES/09-context-governance-measurement.md) a
prerequisite for *evaluating* it rather than a later measurement chore.

## What was built

One arm, `m7`, registered into M6's existing suite runner so the comparison is
against the same harness, the same suite version (0.1.0) and the same scoring as
`monolith`, `dloop` and `staged`. Nothing about the ruler changed.

Four stages, per the specification:

| Stage | Fires | What it does |
|---|---|---|
| 1 premise audit | always, **advisory** | classification, multi-concern flag, one prose concern |
| 2 concern split | on condition | splits the objective into per-concern passes |
| 3 implement | always | one implementer instance per attempt |
| 4 test gate + keeper | always | incumbent-protected, escalate on stall |

Terminals are the processor contract's three — `answered` / `declined` / `blocked` —
rather than the `resolved` / `needs-change` / `escalate` vocabulary `dloop` and
`staged` used. This is deliberate: the suite runner computes `objective_pass` and
`regressed` from the score rather than from the terminal, so the comparison survives
the change, and `declined` keeps its spelling so decline accuracy stays measurable.

### Three decisions the build had to make that the specification left open

**The audit is one call, not three.** `staged` used a K=3 majority vote. That quorum
existed to make a *gate* safer, because a wrong decline was terminal. Advice needs no
quorum, and dropping it returns two calls per task to the implementation budget — which
is most of why an advisory audit should cost less than a gating one rather than more.

**The concern-split firing rule records both candidate signals and fires on either.**
The syntactic one — the objective enumerates its parts, "(1) … (2) …" — and the model
one, the audit's `multi_concern` flag. `22-arch-cognition/08` argues both are the wrong
shape, since the split should compare demand against what the assembly can hold rather
than classify the task. Neither does. Recording both means the rule can be moved later
against the suite's `stresses` slice **without re-running to collect the inputs**.

**Greenfield framing was made to do something.** M6's fix was "plain framing for
greenfield", and the obvious build ignores it. Here the first attempt at a greenfield
target gets the bare objective with no failure preamble, because a check reporting 0/N
against code that does not exist yet says nothing an implementer can act on. Later
attempts get the hint either way.

## A defect in the specification, found by building it

**`11-static-workflow.md` sets "a per-task budget of 4 calls", and that number cannot
survive the concern split.**

The 4-call figure comes from M6's observed 1–4 call range — which was measured on
`dloop`, an arm that **never splits**. Once stage 2 fires, each concern becomes its own
pass through stages 3 and 4, so a three-concern objective wants three passes and a
per-task cap of four calls gives each concern barely one attempt. That is worse than
not splitting.

The build reads the budget as **per pass**, adds a task-level cap of 12 to stop a
many-concern objective running away, and records both. The specification should say
which it meant; the numbers it cites are evidence for the per-pass reading.

## The prediction, recorded before the run

`experiments/M7-static-workflow/PREDICTION.md`, written before `m7_workflow.py` was
executed on the suite and not revised afterwards.

Headline: **25/30, range 24–26**, zero regressions, 5/5 decline accuracy with a sixth
declared-in-advance false decline on `wf3_refactor`, at 8–10 minutes.

It also names what would falsify the *design* rather than the build, and predicts one
uncomfortable thing about stage 1: that its prose `concern` output is consumed on only
the five to seven tasks that reach an escalation payload, and is read by nothing
otherwise.

## Results

| arm | pass | regressions | decline | false declines | wall |
|---|---|---|---|---|---|
| `monolith` | 18/30 | 7 | 0/5 | 0 | 4.3 min |
| `dloop` | 24/30 | 0 | 5/5 | 1 | 6.8 min |
| `staged` | 19/30 | 0 | 5/5 | 7 | 11.8 min |
| **`m7`** | **24/30** | **1** | **5/5** | **1** | 13.7 min |

Stage influence over the 30 tasks: stage 1 parsed 30/30 at one call each; its prose
`concern` was non-empty on 11 and consumed on 8; stage 2 fired on 3 and could act on
2. Median cost per task was 2 calls and 10 seconds — the 13.7-minute total is one
task, `wf6_multi`, at 356 seconds.

[Entry 10](../00-design/50-findings/10-m7-static-workflow.md) holds what it means.
The four things worth carrying:

1. **The advisory audit works** — `staged`'s seven false declines became one, and that
   one was predicted in advance as inherited from `dloop`.
2. **`m7` and `dloop` both score 24/30 while four tasks flipped between them**, none
   of them touched by the added stages. The suite at N=1 cannot resolve a
   one-or-two-task difference.
3. **The keeper protects a count, not a set** — and no earlier arm found it because no
   earlier arm made enough progress on `wf6_multi` to have something to trade.
4. **Stage 2's model firing signal can only ever trigger a no-op**, because
   segmentation is syntactic and the signal is not.

Findings 3 and 4 were cascaded into
[`10-technical/11-static-workflow.md`](../10-technical/11-static-workflow.md), along
with the per-pass budget correction below.

## What is not wired in

**Scope checking.** The workflow runs unscoped.
`05-provisional-invariant-list.md` G4 classes that as an invalidity rather than a
shortfall, and what stands in for it is that a human supervises every run. The
specification side is complete; the build side is
[M17](../00-design/40-roadmap/01-MILESTONES/17-mandate-chain.md).

This also means **this run is the last one that can be compared cleanly against M4 and
M5 on cost**. Once M17 puts a model call in front of every tool call, every arm pays
something no earlier arm paid.
