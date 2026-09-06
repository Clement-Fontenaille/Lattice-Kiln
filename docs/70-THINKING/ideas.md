# Ideas

*A running register of unvetted ideas thrown off by the THINKING work:
experiments to run, methods to try, design moves to consider. Low ceremony. Each
entry carries its provenance and what is open before it would be worth
committing. When an idea matures it graduates to where committed things live —
the research-and-evaluation agenda, the open-questions register, or a design
document — and its entry here records where it went.*

*This is not a design surface. Nothing here constrains anything, and an idea
sitting here is not a plan to act on it.*

---

## I1 — Use logical-equivalence sets to measure the lift of a pipeline shape

**Provenance.** Turned around from the invariance finding in
`07-when-to-decompose/` sheet `07` (Madhwal et al.): pipeline variants that are
provably the same computation still diverge on 40–60% of hard inputs.

**The idea.** If semantics is held constant across a set of pipeline shapes, then
any systematic accuracy or cost difference between them is attributable to the
shape alone. So: for each of a variety of problems, construct a set of
logically-equivalent decomposition and execution shapes; run every shape; record
accuracy and cost. The spread across shapes, with semantics controlled, is a
direct measurement of the quantity the invariance finding says is real but that
nobody isolates — the lift of a shape. Repeat across several models to separate
shape advantages that are model-specific from those that hold in general.

**Why it is worth doing.** It converts "the shape of the system shapes the
outcome" from a caution into a measurable design input, and it gives an empirical
basis for choosing a shape — which sheet `07` argues cannot be done by
equivalence-preserving reasoning.

**Open before it is worth committing.**

- How to generate genuinely semantically-equivalent shape sets at scale without a
  hand-verification bottleneck. Sheet `07` hand-verified every plan.
- What "shape" is varied: topology, call granularity, how much context is passed
  down, recombination method.
- How many shapes and how many problems the spread needs before it means
  anything.
- Whether the result is stable across reruns, given the no-variance problem sheet
  `07` had.
- Each shape must be *commanded*, not sampled and binned after the fact — see
  `07-when-to-decompose/00d-findings.md` F4 on the reverse-causation confound in
  observed-length curves.

**Would graduate to** `00-design/40-roadmap/03-research-and-evaluation-agenda.md`.

Partial prior instance: `07-when-to-decompose/` sheet `04` §3.1 runs six shapes
over the same tasks and measures accuracy *and* cost. It is not a full I1 — the
shapes are different prompting strategies, not semantically-equivalent
decompositions of one plan; it is one model; and the headline numbers are
single-run. But it shows the "run every shape, plot the spread" design is
tractable.

---

## I2 — Probe which bottleneck binds with a plan-quality sweep

**Provenance.** From `07-when-to-decompose/` sheet `04`, Takeaway III, read
narrowly. On its 3×3 Qwen grid (MATH and P&E-DAG only), the executor-scaling slope
is steeper than the decomposer-scaling slope, and at the smallest (1.5B) executor
a better plan barely helps — but at 7B and 14B executors a 14B planner still beats
a 7B planner substantially. So plan quality and executor capability are
*separable* bottlenecks, and which one binds depends on the configuration. The
strong reading — "executor caps the ceiling, a better plan never helps" — is not
supported by the grid.

**The idea.** Hold the executor fixed. Give it plans of increasing quality — from
the target decomposer, from a much stronger model, up to a hand-written or oracle
plan. If accuracy stops moving as plan quality rises, the plan is not the
bottleneck on this task and the plateau is an estimate of what this executor can
do here. If accuracy keeps rising, the plan is the bottleneck and there is
headroom a better decomposer would buy.

**Why it is worth doing.** It turns "is this task executor-limited or
plan-limited?" into a per-task-family measurement, which informs where to spend
model budget and gives a per-task reference value a harness could compare its own
output against.

**Open before it is worth committing.**

- Sheet `04`'s evidence for the premise is thin: one dataset (MATH), one approach
  (P&E DAG), one model family (Qwen2.5), a 3-point grid. The premise needs to hold
  more broadly before the probe means anything.
- What "plan quality" is varied along, and whether an oracle or hand plan is
  constructible for the task families of interest.
- Whether a stronger decomposer's plan is even executable by the weaker executor,
  or encodes steps it cannot perform — which would read as a ceiling but is a
  mismatch.

**Would graduate to** `00-design/40-roadmap/03-research-and-evaluation-agenda.md`.
