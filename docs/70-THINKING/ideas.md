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

---

## I2 — Probe the executor's ceiling with an over-capable decomposer

**Provenance.** From `07-when-to-decompose/` sheet `04`, Takeaway III: scaling the
execution model moves accuracy far more than scaling the decomposition model, and
the execution-only scaling curve nearly coincides with the scale-both curve on its
3×3 grid. Read as: executor capability caps the achievable accuracy, and a better
plan cannot lift you past it.

**The idea.** Hold the executor fixed. Give it plans of increasing quality — from
the target decomposer, from a much stronger model, up to a hand-written or oracle
plan. If accuracy stops moving as plan quality rises, the executor is
capability-limited on this task and the plan is not the bottleneck; the plateau is
an estimate of the executor's ceiling. If accuracy keeps rising with plan quality,
the plan is the bottleneck and there is headroom a better decomposer would buy.

**Why it is worth doing.** It turns "is this task executor-limited or
plan-limited?" into a per-task-family measurement. That informs where to spend
model budget, and it gives a per-task ceiling a harness could compare its own
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
