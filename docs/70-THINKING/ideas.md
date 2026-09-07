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

---

## I3 — Measure per-step error and recovery rates, and test the `c/(c+ε)` ceiling

**Provenance.** `07-when-to-decompose/` finding F24, from sheet `13` (Faith and
Fate). Accuracy at composition depth is governed by the ratio of per-step
recovery rate `c` to per-step error rate `ε`, not by `ε` alone. The paper's
propositions assume `ε` constant and errors independent, are never fitted to its
own runs, and — being about any noisy composition of fallible steps — indict a
decomposition harness as much as a monolith *unless* the harness genuinely raises
`c`. Whether it does is the central untested claim.

**The idea.** Instrument a decomposition run on the project's own task families so
every sub-step is graded against a reference (F25's node taxonomy: fully correct /
local error / propagation error / restoration error). From that, estimate `ε` and
`c` per step, and check whether `c/(c+ε)` predicts observed accuracy as depth
grows. Then add a recovery mechanism — a verifier, a re-entry step, a
cross-check — and measure whether it moves `c` and whether accuracy at depth
tracks the predicted new ceiling.

**Why it is worth doing.** It converts F24 from a borrowed stylised model into a
measured property of the project's setting, and it directly tests the only
defence a decomposition harness has against the compounding-error argument.

**Open before it is worth committing.**

- It needs a process-level scorer — the harness's steps have to be alignable to a
  reference decomposition (the F28 provenance idea, [[I5]], is what makes this
  cheap).
- `ε` almost certainly is not constant across depth (context accumulates), so the
  test is really whether the ratio form holds approximately, not exactly.
- Restoration errors (F25) mean outcome-level grading is biased; the scorer must
  read the working, not just the answer.

**Would graduate to** `00-design/40-roadmap/03-research-and-evaluation-agenda.md`.

---

## I4 — Structure-score the project's own decomposition plans (node vs edge F1)

**Provenance.** `07-when-to-decompose/` finding F26, from sheet `15` (TaskBench).
Producing a list of sub-tasks and producing the correct dependency structure over
them are separable capabilities that dissociate sharply (node-F1 70–80 with
edge-F1 3–13), and the structure half fails first on weaker models.

**The idea.** Have the project's decomposer emit plans as `{nodes, edges}`, and
score the node set and the edge set separately against a reference, without
executing anything. This says, cheaply and per task family, whether the
decomposer's weakness is *naming* the sub-tasks or *wiring* them — which decides
whether to invest in the decomposer at all, and whether the harness can trust the
model to state dependencies for scheduling and argument threading.

**Why it is worth doing.** It is the cheapest available diagnostic on the
decomposer, needs no execution, and targets the capability F26 says breaks first
at constrained model size — the project's regime.

**Open before it is worth committing.**

- Exact-endpoint edge matching penalises correct-but-different plans; the project
  needs a reference that admits alternative valid decompositions, or a metric
  that is not all-or-nothing per edge (TaskBench has neither).
- Where the reference plans come from without a hand-verification bottleneck
  (same problem as [[I1]]).
- Whether a flat node/edge graph is the right representation for the project's
  tasks, or whether depth/recursion has to be in the representation from the
  start.

**Would graduate to** `00-design/40-roadmap/03-research-and-evaluation-agenda.md`.

---

## I5 — Provenance-required sub-results with descendant invalidation

**Provenance.** `07-when-to-decompose/` finding F28, from sheet `14` (Cumulative
Reasoning), plus the open question it leaves. Requiring each sub-result to declare
what it was derived from yields an auditable dependency graph by construction; but
CR only ever *adds* to that graph and never revisits an accepted node found wrong
later — which is exactly the case a harness that accumulates has to handle.

**The idea (a design move, not an experiment).** Make provenance a required field
of every sub-result: it names its parent sub-results (and any external inputs).
The dependency graph is then free, non-duplication is checkable, and — the part CR
does not build — when a node is later found wrong, its transitive descendants are
identifiable and can be flagged stale, recomputed, or surfaced for review rather
than silently carried into the answer (F27's "laundered failure").

**Why it is worth doing.** It is the enabler for [[I3]] (steps become alignable to
a reference), it gives F13/F20's recombination-and-recovery problem a concrete
substrate, and it is cheap to specify now, before a decomposition representation
is fixed.

**Open before it is worth committing.**

- Provenance is only as expressive as the step schema (F28); a sub-step whose
  natural form is not "derived from these parents" gets nothing.
- Invalidation needs a trigger — what declares a previously-accepted node wrong,
  and does that signal come from a later step, a verifier, or the final check.
- Cost of re-running descendants versus accepting a stale-but-flagged answer is
  unquantified.

**Would graduate to** a foundations or cognitive-architecture design document
once the decomposition representation is being specified.

---

## I6 — Upfront conditional decomposition via a task-level complexity evaluator

**Provenance.** Discussion 2026-09-07, a follow-up on
`02-capability-as-granularity.md` in light of the `07-when-to-decompose/` survey.
The survey contrasts ADaPT's failure-triggered decomposition with findings F17
(self-evaluation is the load-bearing weakness of failure-triggered
decomposition), F19 (upfront versus feedback-revised decomposition is tied to
observability) and F20 (fixed upfront decomposition can make a recoverable
trajectory unrecoverable). An earlier `context ÷ steps` phrasing was reframed: it
is a way to think about task-level granularity, not the evaluator's output.

**The claim, in questionable form.** If context is aggregated to what a task
actually requires, then a task-level complexity evaluator can decide *before
execution* whether the task's sub-problems fit a given model's capability, and a
decomposition strategy can be conditioned on that decision without ever running
the task and observing a failure.

**Validity criterion for the argument.** It holds only if such an evaluator
exists whose output — computed from the aggregated context alone, cheaply, and
without above-ceiling authorship per task — orders tasks by sub-problem fit
better than a plain difficulty predictor on a held-out set. The recombination
step has to be one of the sub-problems it fit-checks, because that is the piece
most likely to exceed the ceiling and the one a planner most readily leaves off
the list.

**Falsifier.** No candidate evaluator separates "decomposes successfully at depth
d" from "fails at depth d" better than a difficulty baseline, across the M6 suite
or an equivalent task population.

**Rests on, and each part is unproven.**

- Conjecture 2: the evaluator is buildable at all. This carries the weight, and
  its honest form needs an output type — a scalar on a stated scale, or a binary
  "fits under the ceiling".
- That "required context" is estimable without having already solved the task.
  Defensible only in the weaker form that the aggregated context is a *sufficient
  statistic* for the complexity estimate.
- A capability model that can be queried per sub-problem. Left as an undefined
  placeholder for now; φ from `02` is the leading candidate and is treated as
  dubious. Shared with [[I7]] and [[I8]].

**Relation to existing entries.** Complementary to [[I2]]: I2 probes
plan-quality versus executor-capability after the fact, while I6 asks whether the
fit can be called ahead of time. Shares [[I1]]'s need for a reference set that
admits alternative valid decompositions.

**Would graduate to** a refinement block in `02-capability-as-granularity.md`,
then — if the evaluator survives a first test —
`00-design/40-roadmap/03-research-and-evaluation-agenda.md`.

---

## I7 — Metacognitive skills are ordinary skills

**Provenance.** Discussion 2026-09-07, a follow-up on
`02-capability-as-granularity.md` from the `07-when-to-decompose/` survey. Split
the same day: the activation and feedback-loop half moved to [[I8]], leaving I7
as the claim about the *nature* of the skills only.

**The claim, in questionable form.** Skills such as confidence estimation,
stuck-detection, decompose-or-not, verify-this-step and revise-versus-commit sit
on the same capability scale as object-level skills — each has a ceiling, each
varies with capability, each can be probed for, and metacognitive performance
carries variance of its own rather than tracking general capability.

**Validity criterion for the argument.** It holds only if metacognitive
performance *dissociates* from object-level performance under probing — a
separate axis with independent variance, not a re-reading of general capability.

**Falsifier.** Probing shows metacognitive scores are a monotone function of
object-level scores with no independent variance.

**Rests on, unproven.** Separability of the ceiling into named operations, which
`02-capability-as-granularity.md` currently declines to assume ("treat it as
unitary unless the literature establishes otherwise"). I7 is the explicit request
to *test* that refusal rather than honour it, so the tension is deliberate and
must be named wherever I7 is cited.

**Discussion — confront the literature and its blind spot (will iterate).**
Whether "metacognition" is one axis or several is unsettled: confidence
calibration and error localisation need not co-vary, so the probe design has to
allow more than one factor, and the claim survives in multi-factor form. The work
that bears on I7 is self-correction and self-verification — F17 in
`07-when-to-decompose/00d-findings.md`, the result line that LLMs cannot
self-correct reasoning without external feedback, self-critique being neutral or
harmful without an oracle. Its blind spot is that it varies *whether* an
undifferentiated "review your answer" move is applied, never *which* metacognitive
skill is invoked — so it cannot observe dissociation even if dissociation is
real. That is the same design gap `02` names in the judge-lab, where every
intervention varied stance and none varied granularity. Confronting each paper on
this point is the next step. Building the dissociation probe also depends on the
undefined capability-model placeholder ([[I6]], [[I8]] share it); φ from `02` is
the leading candidate and is treated as dubious.

**Would graduate to** the `02` psychometric programme as an added metacognitive
axis (or several), then a foundations or cognitive-architecture design document
once the dissociation is demonstrated.

---

## I8 — Potential usage of φ: read what a situation demands, then act on it

**Provenance.** Split from the original combined I7 on 2026-09-07, then
rearticulated the same day to stand on its own. This is not the metacognition
claim and does not depend on it — it is about what a recoverable capability model
would be *for*.

**The claim, in questionable form.** If φ (or any probe-able capability model) can
be queried about a concrete situation, then a system can read which capability
that situation demands and act on the reading — pick or generate a prompt that
activates the needed skill, route to a processor sized for it, or decide whether
to decompose — and acting on the reading beats a fixed policy that never consults
φ.

**Validity criterion for the argument.** It holds only if (a) φ is recoverable
and cheap to query per situation; (b) the reading is actionable — at least one
lever (prompt choice, routing, decompose-or-not) has an effect on the outcome
that the reading predicts; and (c) acting on the reading beats the best fixed
policy that ignores it.

**Falsifier.** Acting on the φ reading does no better than a fixed best-guess
policy; or no available lever's effect is predicted by the reading; or φ does not
compress enough to be queried cheaply — the "risk that would end this" in `02`.

**Relation to other entries.** [[I6]] is one instance of I8: the lever there is
the decompose-or-not decision and the reading is a task-level complexity
estimate. Situation-matched activation of a metacognitive skill is another
instance — I8 applied to a metacognitive axis, which additionally needs [[I7]] to
hold and must confront the self-correction blind spot noted under I7. I8 itself
needs neither I6 nor I7.

**Sub-claims that need their own inquiry.**

- *A good prompt raises the ceiling for a skill.* Qualify the layer (see `02`'s
  bare / effective / integrated-system naming). At the **processor / effective**
  layer this is established — prompting technique produces large measurable
  performance differences under a fixed model, and drawing out latent model
  capacity *is* raising the effective ceiling. What is open is whether a prompt
  moves the **model / bare** ceiling — changes what the model can compute at all.
  For chain-of-thought there is an expressivity result (`07-when-to-decompose/`
  sheet `06`, Merrill & Sabharwal) that it does, in that one case; how far the
  bare ceiling moves for skills without such a result is unknown.
- *The targeted model can write the activating prompt itself.* Open, and the risk
  is circular — a model that cannot perform a skill may be unable to judge which
  prompt would elicit it. Existing automatic-prompting results mostly use capable
  generators, and prompt quality tracks generator capability. The natural split
  is that an advanced model authors the processor instantiation, the constrained
  model runs it, and the instantiation is found by experiment — consistent with
  F18's planning/execution budget asymmetry.

**Rests on, unproven.** φ being recoverable and cheap to query — `02`'s central
open risk. Independent of [[I7]].

**Would graduate to** `00-design/40-roadmap/03-research-and-evaluation-agenda.md`
as a probe-then-act experiment.

---

## I9 — The prior question: does φ predict anything, and how far does it carry?

**Provenance.** Discussion 2026-09-07, extending the φ dependency that [[I6]] and
[[I8]] both rest on. Both list "φ recoverable and cheap to query" under *rests
on*; I9 turns that into its own investigable question, upstream of any use of φ.

**The question, in open form.** φ is a constructed projection from observed model
behaviour into a feature space. What information about a given model state can be
extracted using φ? Three conditions have to hold in sequence before φ can be
leveraged:

1. **Predictive.** φ predicts something it was not fit on — held-out outcomes or
   behaviours.
2. **Representative of its source.** A φ built from a task population reflects
   that population, rather than noise or the taxonomy of whichever model
   generated the items.
3. **Representative of the adjacent.** φ carries to model states close to but
   outside its construction set.

**Validity criterion for a positive answer.** φ beats a baseline (task
difficulty, task family) at predicting held-out outcomes or behaviours, on a
held-out set that includes items of *independent provenance* — not generated by
the model that authored φ. Recovered structure is stable across reruns and across
which model generated the items.

**Falsifier.** φ predicts held-out outcomes no better than a difficulty baseline;
or a φ fit on population A fails on adjacent population B; or the recovered
structure is unstable across reruns or across item-generator choice.

**Relation to other entries.** Strict prior to [[I6]] and [[I8]] — neither can be
tested until I9 is answered positively. Adjacent to [[I7]]: I7 asks whether φ has
a metacognitive axis, I9 asks whether φ carries any predictive information at
all. Mirrors `02-capability-as-granularity.md`'s "the risk that would end this"
and its construct-validation apparatus (internal consistency, factor loading,
convergent / discriminant validity, Q-matrix identifiability).

**Status.** The open-question form is recorded in
`00-design/40-roadmap/02-open-questions-register.md` under *Capability model (φ)*
(2026-09-07). The experiment form is what would still graduate to
`00-design/40-roadmap/03-research-and-evaluation-agenda.md` — `02` already names
the cheap version: does any candidate φ separate the M6 suite's passes from its
failures better than chance, using features computable in advance.

---

## I10 — Addressable sub-results escape the aggregator's superlinear collapse; model-driven composition does not

**Provenance.** Cross-paper discussion 2026-09-07 of `07-when-to-decompose/`
sheets `17` (divide-conquer-noise), `18` (ARES), `19` (Agentless), `20`
(verifier-robustness). First stated here. Sheet `17` assumes the aggregator's
loss `ℒ_agg = O(T)` in a single sentence, but the synthesised reasons
re-aggregation is hard — a coarse working set that holds the whole objective, a
merge input that grows with the number of parts, the same attention-dispersion
degradation as a monolith — are exactly the reasons to expect `ℒ_agg` to grow
*superlinearly*. Agentless is the counterexample that isolates the escape
condition. The escape condition was relaxed in the same discussion: the binding
requirement is not a pass/fail oracle per candidate but that sub-results are
*queryable* — see F38 (retrieval works when information is locatable, fails when
it is diffuse).

**The claim, in questionable form.** The superlinear degradation the
divide-and-conquer literature attributes to a single long-context model reappears
in the recombination step whenever that step is a model reasoning over many long
partial results all held in context at once — so the crossover ("splitting wins
on length") fails from the aggregation end too, not only the monolith end. It is
avoided, and the D&C-side linear loss bound is preserved, when recombination does
**not** need every partial result in context simultaneously — either because the
merge is deterministic selection or combination logic, or because the sub-results
are individually addressable in a structured store (named, on disk, in a sound
file hierarchy) so the merge *retrieves* what each step needs. A cheap
per-candidate external check — an executable test, a verifier — is one strong
form of addressability, not the requirement. This escape still fails when the
answer is a genuine composition of all parts rather than a selection among
alternatives or an assembly of separately-addressable pieces.

**Validity criterion for the argument.** It holds only if, at fixed decomposition
depth, aggregation-attributed loss grows superlinearly with the number of parts
when the merge holds all partial results in context, stays linear or better when
the merge is deterministic or retrieves from an addressable store or merges
hierarchically, and the difference disappears when the answer is genuine
composition rather than selection or assembly.

**Falsifier.** A hold-everything-in-context aggregator whose loss stays linear in
the number of parts across a real length sweep; or an addressable-store /
deterministic / hierarchical merge that degrades superlinearly anyway; or the
composition-versus-selection distinction making no measurable difference to
aggregation loss growth.

**For experimental validation.**

- Hold decomposition depth and task fixed. Measure system score — and, where an
  oracle merge is approximable, aggregation-attributed loss — as a function of the
  number of parts `n`, for four aggregators: all-partial-results-in-context,
  deterministic selection, retrieval from an addressable store (sub-results on
  disk in a named hierarchy), recursive hierarchical merge. Test whether only the
  first is superlinear.
- Vary the answer type — selection among alternatives, assembly of addressable
  pieces, genuine composition of all parts — holding the store structure fixed.
  Test whether the escape vanishes for genuine composition.
- Run the same decomposition on a task with an executable check (code) and on one
  without (prose synthesis). Compare aggregation loss growth.

**Relation to other entries.** Extends candidate finding C3 from sheet `17`
(the flat aggregator re-enters the long-context regime as `n` grows) and rests on
F38 (locatable versus diffuse sub-results). Connects to F13 (recombination is a
distinct large unmeasured failure mode), F27 (the accept/reject port; a wrong
accepted step is a laundered failure), F31 (a deterministic controller between
planner and executor is a harness architecture), F28 (provenance as a required
field makes sub-results addressable by construction), and F10 (S&D's demonstrated
value is cost, not accuracy). Sharpens [[I6]]: it names a condition under which
the aggregator, specifically, is the binding stage.

**Would graduate to** `00-design/40-roadmap/03-research-and-evaluation-agenda.md`
as the aggregator-collapse sweep, plus a design note that decompositions whose
recombination retrieves from an addressable store of sub-results are preferred
over those whose recombination holds every partial result in one context.
