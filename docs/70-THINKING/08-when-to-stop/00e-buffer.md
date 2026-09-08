# Buffer — Knowing When to Stop

*A staging area. Nothing here is locked. Grow it and consume it at any pace.*

- **Candidate findings** graduate to `00d-findings.md` with an F-number when
  accepted. Rejected ones are struck through and kept, so they are not
  re-proposed.
- **Proposed ideas** graduate to the global `../ideas.md` with an I-number when
  accepted.
- **Reading queue** is what I propose to read next, in my suggested order. You
  approve, reorder, or cut. You pick what actually gets read next.

**Sweep tag on each candidate finding.** `[SWEEP]` means it changes what an
upcoming experiment sweep should measure or build. `[background]` means it is
reference for later, and does not by itself move the sweep design.

**Cross-links to topic 07.** Each candidate finding notes which topic-07
F-numbers it confirms, sharpens, or cuts against. Heavy overlap sits on the
self-evaluation / verification thread (F11, F17, F24, F25, F41, F42, F44, F45,
F49, F52–F60, F63).

---

## 1. Candidate findings

*From the cross-paper pass over sheets 01–08. One-line claim list first, for a
fast keep / cut / merge / misread scan; full text below it.*

### One-line claim list

- **CF-1** — The stop / continue / escalate decision cannot be sited in the
  model's own verdict on its own work. `[SWEEP]`
- **CF-2** — Agreement across independently sampled attempts is the one intrinsic
  signal shown to work, and only where "the same answer" is definable. `[SWEEP]`
- **CF-3** — The signal these methods threshold on is answer-stability, not
  answer-correctness. `[SWEEP]`
- **CF-4** — Optimising a model against a verifiable reward, reasoning
  fine-tuning, and more test-time compute all erode its willingness to decline or
  stop; task accuracy and stop-competence are separate axes. `[SWEEP]`
- **CF-5** — The failure is one-sided: models run past the stop point, and almost
  never stop too early. `[SWEEP]`
- **CF-6** — Given an underspecified task, the model fabricates the missing
  detail and proceeds to a confident, well-formed, wrong result. `[SWEEP]`
- **CF-7** — Prompting that enumerates the abstention scenarios in advance
  patches the symptom without touching the reasoning. `[SWEEP]`
- **CF-8** — The model's reasoning text expresses uncertainty more often in
  general, not more often when the uncertainty is warranted. `[background]`
- **CF-9** — Re-running the same evaluator call on the same input measures the
  noise floor under any gate built on it. `[SWEEP]`
- **CF-10** — Perturb-and-check is a reusable instrument for calibrating a
  harness's own stop-decision component. `[SWEEP]`
- **CF-11** — An iterating loop presents every new attempt wrapped in its own
  revision history, and evaluators score text higher when they can see it was
  revised. `[SWEEP]`
- **CF-12** — What a judging model reads is dominated by stance, format,
  position, and provenance; the content of the reasoning barely moves it.
  `[SWEEP]`
- **CF-13** — Plain mean token log-probability is the weakest of the available
  intrinsic confidence signals. `[background]`
- **CF-14** — Iterative self-correction has to be compared against sampling N
  attempts and selecting among them at equal compute, and rarely is. `[SWEEP]`
- **CF-15** — Measure the quality of the stop signal directly, not only the task
  outcome of the loop that uses it. `[SWEEP]`

### Full text

#### CF-1 — The stop / continue / escalate decision cannot be sited in the model's own verdict on its own work. `[SWEEP]`

**→ Graduated to `00d-findings.md` as F1 (2026-09-09).**

Five sheets converge on this from different directions.
Sheet 01 (Kamoi survey) localises the weak link in feedback *generation*, not in
refinement: models can act on a reliable signal, but they cannot reliably produce
one about their own output.
Sheet 03 (AbstentionBench) shows volunteered abstention is flat across model
scale from 8B to 405B, and gets *worse* under the training that improves task
accuracy.
Sheet 05 (Xiong) measures failure prediction from a bare verbalized confidence at
AUROC in the low 50s, near chance, with GPT-4 the best at 62.7 and still called
suboptimal.
Sheet 06 (judge biases) finds five of six judges inflate their own anonymised
output, and the score moves while the stated rationale does not.
Sheet 07 (glass-box) reports prompted self-scoring collapsing to ~0.15 Pearson.

Confirms / sharpens: F11, F17, F24, F25, F41, F52, F59.
Cuts against: nothing in topic 07; it hardens the existing direction.
Tension, added by rounds 3–4: the signal is not *absent* from the model, it just
does not reach the output under normal decoding — see [[CF-23]] (a mid-layer
probe and a mid-reasoning interrupt both recover it) and [[CF-16]]-adjacent
[[CF-1]] caveats in sheet 13 (P(True) works, and verification scales faster than
generation, in the right format). The claim survives for the deployed agent
setting because that setting is out of the format and the distribution where the
signal is reliable.
Sweep consequence: the stop signal must come from outside the model's *final
self-report* — an external check, a trajectory statistic, or a mid-reasoning
probe. "Ask the finished model whether it is done or stuck" belongs in the sweep
only as a floor baseline, not as a serious arm.

#### CF-2 — Agreement across independently sampled attempts is the one intrinsic signal shown to work, and only where "the same answer" is definable. `[SWEEP]`

**→ Graduated to `00d-findings.md` as F4 (2026-09-09).** CF-3's caveat is folded
into F4 inline.

Sheet 05: consistency over five samples moves GSM8K failure-prediction AUROC from
54.8 to 92.7, the largest single effect in that paper, and the verbalized number
is useful only as a weight inside the aggregation.
Sheet 04 (Stop Overthinking): the consistency-based early-exit family (ST-BoN,
certaindex) is built on the same signal, and ST-BoN needs no reward model at all
— the signal is cross-sample latent-embedding geometry.
Sheet 02 (To Believe or Not): the epistemic-uncertainty method is a second-order
form of this — feed prior answers back in a fixed "another answer is X" prompt,
and measure whether the next answer moves.

The bound is sharp and stated in the sources.
Sheet 05's mechanism needs exact answer matching.
Sheet 02's independence assumption (its Assumption 4.1) explicitly excludes
partial answers — a step of an algorithm, a part of a story — which is exactly
the multi-step case.
Neither transfers to a trajectory or a long-form artifact without a clustering or
equivalence notion supplied per artifact type.

Confirms / sharpens: F51 (sampling diversity at the split), F45, and I1.
Sweep consequence: budget for M ≈ 5 parallel attempts as the primary intrinsic
stop signal, expect saturating returns past that, and decide up front how "the
same answer" is defined for each artifact type under test.

#### CF-3 — ~~The signal these methods threshold on is answer-stability, not answer-correctness.~~ `[SWEEP]`

**✗ Cut (2026-09-09).** Not a finding in its own right — a cross-cutting caveat
on the *class* of stability signals (CF-2, CF-16, CF-17, CF-23, and sheet 07's
softmax dispersion), with no evidence of its own. Folded into F4. Rule: name
"this is a stability signal, not a correctness signal" inline wherever one of
these approaches appears, rather than pointing at a shared finding. No
indirection.

*(original text kept below for the record)*

Sheet 04 states it directly: a high certaindex means "further reasoning steps are
unlikely to change the final answer", which is a stability claim, not a
correctness claim.
Sheet 02's mutual information is a sensitivity measure, not a truth measure.
Sheet 05's consistency is agreement among samples, not agreement with the ground
truth.
Sheet 07 shows the same hole in the softmax-dispersion features: a fluent,
low-entropy, wrong answer is scored as high quality, and the method's core
assumption is that this case does not arise.

Consequence: a loop that stops when the answer stops moving will also stop early
on a confidently wrong answer the model is stable about.
Confirms / sharpens: F42 (a chain verifier propagates trust, cannot establish
it), F56 (majority vote over a biased signal amplifies the bias).
Sweep consequence: any stability-based stop arm needs a paired external
correctness check fired on the stop event, or the measurement will score early
stops on stable wrong answers as successes.

#### CF-4 — Optimising a model against a verifiable reward, reasoning fine-tuning, and more test-time compute all erode its willingness to decline or stop; task accuracy and stop-competence are separate axes. `[SWEEP]`

**→ Graduated to `00d-findings.md` as F5 (2026-09-09).** Retitled to "willingness
to decline" with the measurement (abstention recall, LLM-judged, single-turn)
spelled out.

Sheet 03 carries this on three independent designs.
PPO against a verifiable reward (RLVR) degrades abstention recall relative to the
DPO checkpoint on a staged post-training ladder.
Reasoning fine-tuning degrades abstention by about 24 points, including in the
math and science domains the models were tuned for, measured on two paired
fine-tunes against their own base models.
Scaling the reasoning-token budget raises accuracy while abstention stays flat or
falls.
Sheet 04 says the same thing from the efficiency side: the recipes that create
reasoning ability reward length, so brevity works against the pretraining
objective.
Sheet 03 also shows accuracy and abstention correlate with varying sign by
dataset, and the three best models by accuracy sit near the bottom on abstention.

Confirms / sharpens: F57 (fine-tuning can collapse a verifier into a constant
accept / reject policy) — here it is the model's stop policy collapsing toward
"commit".
Sweep consequence: if any sweep arm uses a model RL-tuned on the harness's own
test suite, treat its self-stop signal as degraded relative to the un-tuned
model, and measure that as a separate factor rather than assuming benchmark
accuracy carries stop-competence with it.

#### CF-5 — The failure is one-sided: models run past the stop point, and almost never stop too early. `[SWEEP]`

Sheet 03: abstention precision is near ceiling for most models on most datasets,
so over-abstention is essentially not a failure mode of these models, and recall
carries all the information.
Sheet 08 (SelfAware): models rarely abstain at all, and the benchmark's metric
even penalises abstention on hard-but-answerable questions.
Sheet 04's agentic study names "premature disengagement" as a real pattern, but
it sits next to "analysis paralysis" and running-past as the dominant modes.

Consequence: a harness's error budget on the stop decision is almost entirely
"ran past the point it should have stopped", not "quit too early".
Confirms / sharpens: nothing direct in topic 07; new for the register.
Sweep consequence: instrument the late-stop / overrun error as the primary
quantity, and treat the early-stop error as a secondary, lower-rate one.

#### CF-6 — Given an underspecified task, the model fabricates the missing detail and proceeds to a confident, well-formed, wrong result. `[SWEEP]`

Sheet 03's qualitative failure mode is specific.
Given the bare prompt "How many bolts in total does it take?", the reasoning
model registers "I need more context", invents a prior conversational turn about
the Golden Gate Bridge, cycles through two more invented projects, and answers
"1,000,000" with a supporting paragraph.
This is distinct from a stall, which shows no progress, and distinct from an
error, which is visibly broken; it passes shape checks.
Sheet 04's MiP-Overthinking result is the other half of the same coin: some
models instead loop and re-think forever on a missing premise rather than
declaring the problem unanswerable.
Which of the two failures a model shows appears to be set by its training (sheet
03).

Confirms / sharpens: F53 (step-verifiers fail toward rejection) — the failure
direction here is the opposite, toward commitment, and sheet 03 shows the
direction is trainable.
Sweep consequence: add "unrequested assumption-filling" as a first-class
instrumented event, separate from error and from no-progress. A success criterion
that only shape-checks the output will miss it.

#### CF-7 — Prompting that enumerates the abstention scenarios in advance patches the symptom without touching the reasoning. `[SWEEP]`

Sheet 03: a "generous" system prompt that lists the abstention scenarios raises
abstention recall for standard and reasoning models without hurting precision.
The authors read the gain as the model pattern-matching a named category, not as
the model reasoning about the evidence in front of it, so it does not generalise
to failure modes nobody named.
Sheet 08: a single explicit permission-to-abstain sentence moves base davinci by
about 18 points, and in-context learning with paired answerable / unanswerable
exemplars gives the largest single gain in that paper.

Consequence: worth doing, cheap, and real; a checklist, not a capability.
Confirms / sharpens: nothing direct.
Sweep consequence: include an "abstention-scenario system prompt plus paired
exemplars" arm as a cheap baseline, but test it against held-out failure modes
that were not named in the prompt, and do not read its gain as a general stop
capability.

#### CF-8 — The model's reasoning text expresses uncertainty more often in general, not more often when the uncertainty is warranted. `[background]`

Sheet 03: reasoning traces contain markedly more hedging than the final answers,
and feeding the trace to the judge *raises* abstention recall while *lowering*
abstention precision — the signature of a source that hedges indiscriminately,
including on answerable questions.
Sheet 06: the refinement-aware score moves while the stated justification stays
constant, which the authors call implicit bias.
Sheet 04: carries the trace-unfaithfulness caveat — the logic in a reasoning
trace may be deceiving.

Confirms / sharpens: F25, F59 (an LLM's outcome judgment and process judgment are
not separable), F60.
Sweep consequence: mostly a caution. If a sweep arm parses trace text for hedge
phrases as a stop signal, it must report precision, not only recall.

#### CF-9 — Re-running the same evaluator call on the same input measures the noise floor under any gate built on it. `[SWEEP]`

Sheet 06: judges disagree with themselves on 7.5 to 14.4 per cent of open-ended
items at temperature 0.7, before any perturbation is applied.
That self-disagreement rate (their Consistency Rate) is the noise floor beneath
every bias number in the paper, and it was produced almost as a by-product of
running each comparison twice.
Sheet 05: never report a calibration number without also reporting the
discrimination metric and the confidence histogram, because a model can reach
near-perfect calibration by assigning 100 per cent confidence to everything.

Consequence: a harness gating a decision on one evaluator call on an open-ended
artifact is gating on a variable with a roughly one-in-ten flip rate.
Confirms / sharpens: F52.
Sweep consequence: every evaluator-based stop arm logs a same-input double-run
disagreement rate, and that rate is the floor beneath any effect the arm shows.

#### CF-10 — Perturb-and-check is a reusable instrument for calibrating a harness's own stop-decision component. `[SWEEP]`

Sheet 06's attack-and-detect design: perturb the input in a way that must not
change the correct verdict, then measure whether the verdict moves.
This is metamorphic testing applied to an evaluator, and it needs no human
quality labels.
Sheet 02's method is structurally the same move — perturb by feeding answers
back, measure the movement.

Consequence: a harness can run this against its own stop / continue evaluator on
its own task distribution and read off a calibration number specific to it,
rather than borrowing one from a model list.
Confirms / sharpens: nothing direct; candidate standing evaluation instrument.
Sweep consequence: build a small perturbation suite — reorder the candidates,
re-register the tone, add an irrelevant line, show or hide the revision history —
and run it against whatever component makes the stop call.

#### CF-11 — An iterating loop presents every new attempt wrapped in its own revision history, and evaluators score text higher when they can see it was revised. `[SWEEP]`

Sheet 06's refinement-aware bias: the same text scores about a point higher on a
ten-point scale when the conversation history revealing it is a revision is
visible, with the justification unchanged.
An agent loop always shows attempt N+1 alongside attempts 1 through N.

Consequence: a loop that judges its latest attempt with the history in view
drifts toward premature satisfaction, and the drift grows with the iteration
count.
Confirms / sharpens: F44 (what a validation call is allowed to see is a design
parameter, and the default is the worst one) — this is a measured instance of the
default being worst.
Sweep consequence: the stop evaluator scores the latest artifact in isolation,
with the attempt history withheld. Add "history visible vs withheld" as a sweep
factor.

#### CF-12 — What a judging model reads is dominated by stance, format, position, and provenance; the content of the reasoning barely moves it. `[SWEEP]`

Sheet 06: judges hold their verdict on 92 to 98 per cent of items when the
reasoning inside the better answer is corrupted into chaos, but lose it on up to
76 per cent of items when that same answer is rewritten in an angry or fearful
register.
Position sensitivity falls below 0.5 robustness with three or four candidates,
meaning the verdict fails to survive re-ordering more often than it survives.

Consequence: a component that reports its own failure candidly, or in an alarmed
register, may be marked down for the register rather than read for the substance.
Confirms / sharpens: F24, F25 — here the judge is not reading the reasoning at
all in a way that competes with reading the tone.
Sweep consequence: normalise or strip register and provenance from anything
handed to a stop evaluator. Include raw-vs-normalised as a factor.

#### CF-13 — Plain mean token log-probability is the weakest of the available intrinsic confidence signals. `[background]`

Sheet 07: plain sentence probability correlates about 0.35 with a quality score,
while vocabulary-level softmax entropy and per-token probability variance, from
the *same* forward pass, reach about 0.60.
Sheet 05: logit-based signals sit in the same 0.5 to 0.6 AUROC band as everything
else, and miss semantic uncertainty by construction.

Consequence: a harness that logs mean log-probability as its confidence proxy is
logging the weakest signal it has access to.
Confirms / sharpens: nothing direct.
Sweep consequence: if any arm records an intrinsic confidence scalar, prefer
softmax dispersion over mean log-probability. Low priority.

#### CF-14 — Iterative self-correction has to be compared against sampling N attempts and selecting among them at equal compute, and rarely is. `[SWEEP]`

Sheet 01: self-correction spends multiple model calls, so the honest baseline is
self-consistency or generate-and-rank given the same budget.
That comparison is almost never run, so whether self-correction beats it is
simply unknown — the survey's verdict on its RQ3 is a null one.

Confirms / sharpens: F63 (a fixed-pipeline-versus-agents comparison is
architecturally unfair unless compute is matched; inference-only cost) — the same
methodological demand, one stage over.
Sweep consequence: any iterative-refinement arm in the sweep must have a matched
sample-N-and-select arm at an equal token and call budget, or its result is
uninterpretable.

#### CF-15 — Measure the quality of the stop signal directly, not only the task outcome of the loop that uses it. `[SWEEP]`

Sheet 01's instrumentation recommendation: report the error-detection accuracy of
the feedback itself, because downstream task accuracy and feedback quality
diverge, and the field learned little by measuring only the former.
Sheet 05: report discrimination and the histogram, not only calibration, for the
same reason.

Confirms / sharpens: F49 (instrument the generation ceiling separately from the
pipeline result) — nearly the same demand, a different stage.
Sweep consequence: the sweep's metrics must include stop-decision precision and
recall against a retrospective ground truth, reported as a first-class output
alongside task success.

### Round 3–4 additions (sheets 09–16)

Sheets 09–12 are the agentic-loop-native cluster (Semantic Early-Stopping,
VRR-Stop, Infinite Agentic Loops, Reflexion). Sheets 13–16 are the
uncertainty-signal and judge-reliability cluster (Kadavath P(IK), Err Knowingly,
FlipFlop, Reliability without Validity). These ten additions mostly sharpen
CF-1…CF-15 with a loop-native mechanism or a measured magnitude; two of them
(CF-16, CF-23) open a direction the first eight sheets did not.

#### One-line claim list

- **CF-16** — "Which round is best" is a harder and more valuable problem than
  "when to stop"; a loop that stops well but keeps the wrong round still fails.
  `[SWEEP]`
- **CF-17** — Stopping on answer-stability with no failure branch converts a
  stalled loop into a confident wrong answer; the controller needs an explicit
  third outcome. `[SWEEP]`
- **CF-18** — The stop decision does not transfer across deployments: it rides on
  verifier discrimination and the decision margin, not on a fixed threshold or
  round budget. `[SWEEP]`
- **CF-19** — Self-repair raises the reported accept rate while lowering true
  validity, and the gap widens with iteration. `[SWEEP]`
- **CF-20** — An LLM asked whether a loop is effectively bounded is unreliable
  even with curated evidence. `[SWEEP]`
- **CF-21** — A budget bounds a loop only if its scope dominates the cycle; a
  counter that merely exists in the program does not. `[background]`
- **CF-22** — Unbounded loops concentrate at the failure signal — retry, tool-call
  iteration, multi-agent chat — so error handling is where stopping breaks.
  `[SWEEP]`
- **CF-23** — The model holds a usable answerable / on-track signal in mid-layer
  activations and in a mid-reasoning interrupt that its final output does not act
  on. `[SWEEP]`
- **CF-24** — Requiring corroboration of a rare stop signal before acting on it
  makes results monotonically worse. `[SWEEP]`
- **CF-25** — Reopening a completed step with an evidence-free prompt has a
  systematic accuracy cost; it is not a free re-check. `[SWEEP]`

#### Full text

##### CF-16 — "Which round is best" is a harder and more valuable problem than "when to stop". `[SWEEP]`

Sheet 09: a judge-free embedding-convergence stopper matches a fixed iteration
cap at about 38 per cent lower cost, but an oracle that picks the best round
beats *every* practical stopping policy by a wide margin (+0.115 Information
Score, p ≈ 4e-11), and the paper reframes its own problem from "when to stop"
(easy) to "which round is best" (open).
Sheet 09 also: a trivial `fixed_k1` policy — return the first grounded draft —
dominates the semantic stopper on both cost and quality in the same table.
Sheet 12 (Reflexion): on WebShop the loop neither improved across trials nor
recognised its own futility, and a human stopped it after four.

Consequence: a loop that stops at a reasonable time but keeps a worse round than
one it already produced is still failing, and the loss is invisible to a
stop-time metric.
Confirms / sharpens: [[I1]], [[CF-2]].
Sweep consequence: measure "did the loop keep its best intermediate artifact"
separately from "did the loop stop at a good time", with an oracle-best-round
upper bound reported alongside.

##### CF-17 — Stopping on answer-stability with no failure branch converts a stalled loop into a confident wrong answer. `[SWEEP]`

Sheet 09: the stopper's reason codes are `critic` / `entropy` / `no_gain` /
`failsafe` — there is no category for the task failing or being beyond the loop,
so a stuck loop repeating itself emits exactly the `entropy` (converged) signal
that a finished loop emits.
Sheet 14: the sharpest negative result in that paper — cutting non-termination
*without* an explicit licence to say "this cannot be done" raised the fabrication
rate; the baselines and the no-guidance ablation both did this.
Sheet 12: Reflexion has no abandon or hand-off branch at all; the outer loop
exits only on an evaluator pass or a trial cap.

Consequence: stability detection plus a two-way stop/continue switch is not
enough; the third outcome (abandon / hand off) needs its own trigger, or
stability on a wrong answer is read as done.
Confirms / sharpens: [[CF-3]], [[CF-6]].
Sweep consequence: the loop controller under test emits one of {continue, commit,
abandon}, and the abandon path is wired to its own signal, not derived from the
commit path's stability score.

##### CF-18 — The stop decision does not transfer across deployments: it rides on verifier discrimination and the decision margin, not on a fixed threshold or round budget. `[SWEEP]`

Sheet 10 (VRR-Stop): fixed round budgets and fixed confidence thresholds
provably cannot transfer across deployments; stopping reliability is governed by
the verifier's discrimination (Youden's J) and the decision margin, and when
discrimination approaches zero the estimator is unidentifiable — so *more*
calibration data makes it more confidently wrong.
Sheet 16: judge rankings shift by up to 15 positions across three benchmarks
because MT-Bench compresses the whole cohort into a 13.5-point kappa band while
JudgeBench spreads it over 60 points — the same judge, a different discrimination.
Sheet 13: P(IK) calibration collapses out of distribution while its ranking power
partly survives.

Confirms / sharpens: [[CF-9]].
Sweep consequence: a stop threshold tuned on one task family carries no guarantee
to another; the sweep re-measures the stop gate's discrimination per task family
and reports the decision margin, not only the threshold value.

##### CF-19 — Self-repair raises the reported accept rate while lowering true validity, and the gap widens with iteration. `[SWEEP]`

Sheet 10: in six of eight stress settings true validity declines monotonically
with repair rounds, 55 per cent of stress instances have a correct plan repaired
into an incorrect one, and a strong process-reward-model verifier at J = 0.805
does not prevent the collapse — so verifier quality and repairer safety are
separate problems.
Sheet 12: removing the grounded test check while keeping reflection scores *below*
the no-iteration baseline, because the agent cannot tell correct code from
incorrect and keeps editing.
Sheet 15: models lose about 17 accuracy points from first to final answer under
an evidence-free challenge.

Confirms / sharpens: [[F40]], [[F41]], [[CF-3]] — here with a mechanism (verifier
noise × repairer damage) and a measured magnitude.
Sweep consequence: track true validity across iterations, not only the verifier's
accept signal; a rising accept rate across rounds is fully consistent with
falling quality.

##### CF-20 — An LLM asked whether a loop is effectively bounded is unreliable even with curated evidence. `[SWEEP]`

Sheet 11: given the same 340 candidate loops and curated evidence, a frontier
model asked "is this loop effectively bounded" covered 68, 64 and 60 true cases
across three runs, and other models only 41 to 54.

Consequence: "ask the model whether this loop will terminate / is stuck" is not a
viable stop arm — it is [[CF-1]] applied to one specific judgement, with a number
on it.
Confirms / sharpens: [[F52]].
Sweep consequence: the loop bound must be structural (a budget whose scope
dominates the cycle, per [[CF-21]]), not a model verdict.

##### CF-21 — A budget bounds a loop only if its scope dominates the cycle; a counter that merely exists in the program does not. `[background]`

Sheet 11: the load-bearing conceptual distinction is between a loop's *exit
condition* (which may be model-written, e.g. "the model stopped emitting tool
calls") and its *effective bound* (a budget that provably covers the cyclic
feedback path). 69 per cent of confirmed unbounded loops had a retry, tool-call,
or multi-agent-chat cycle with no dominating bound.

Consequence: build-side vocabulary. Every retry / tool / hand-off cycle in the
harness needs a budget attached to that cycle's scope, and state growth budgeted
separately from turn count.
Confirms / sharpens: nothing in topic 07; new.
Sweep consequence: minor — it is a construction rule, not a measurement, but a
sweep arm that lacks a scope-dominating budget on each cycle is not a valid
control.

##### CF-22 — Unbounded loops concentrate at the failure signal — retry, tool-call iteration, multi-agent chat. `[SWEEP]`

Sheet 11: 69 per cent of confirmed infinite loops are triggered by something the
system read as a failure signal — a retry, a re-issued tool call, an unresolved
multi-agent exchange.
Sheet 14: "cognitive fixation" is the model burning its whole budget reformulating
the problem after it hits a snag, never committing.

Consequence: a loop is most likely to run away in the moment right after it
detects that something went wrong.
Confirms / sharpens: [[CF-6]].
Sweep consequence: instrument the retry / re-plan / re-delegate transitions
specifically; a no-progress counter and a repeated-action check belong on those
edges first.

##### CF-23 — The model holds a usable answerable / on-track signal in mid-layer activations and in a mid-reasoning interrupt that its final output does not act on. `[SWEEP]`

Sheet 14: a linear probe on mid-layer attention outputs separates answerable from
unanswerable at AUROC 0.87 to 0.97 and transfers to a second dataset it was not
trained on; interrupting a failing trajectory mid-reasoning yields a correct
abstention and a correct explanation of the defect at high rates; the gap is
characterised as sub-threshold confidence, not an absent representation.
Sheet 14 also: a behavioural monitor reading the model's *visible* mid-reasoning
self-doubt captures most of the benefit of the probe.
Sheet 13: P(True) self-evaluation works and its discrimination margin widens with
model size — verification scales faster than generation.

Consequence: this is the counterweight to [[CF-1]]. The signal exists; it does
not reach the output under normal decoding.
Confirms / sharpens: [[F17]] from the other side.
Sweep consequence: a mid-reasoning interrupt-and-ask ("is this still answerable /
on track?") is a distinct arm from a finished-output self-report, and sheet 14
says it works far better; give it its own arm.

##### CF-24 — Requiring corroboration of a rare stop signal before acting on it makes results monotonically worse. `[SWEEP]`

Sheet 14: gating the abstention signal on corroboration made results
monotonically worse, because the true signal is too rare to corroborate, so the
gate suppresses true positives.

Consequence: this cuts against the reflex to K-vote every gate. [[F56]] says
K-vote over a *biased* verifier amplifies the bias; CF-24 adds that
corroboration over a *rare* true signal suppresses it.
Confirms / sharpens: qualifies [[F56]] and the K-vote-on-a-gate pattern.
Sweep consequence: for a low-base-rate outcome (abandon), act on a single
sufficiently-confident probe and price in the false-positive cost, rather than
gating on agreement.

##### CF-25 — Reopening a completed step with an evidence-free prompt has a systematic accuracy cost; it is not a free re-check. `[SWEEP]`

Sheet 15: challenged with an informationally empty "are you sure?", models flip
about 46 per cent of the time and lose about 17 accuracy points from first to
final answer; flips are less likely when the initial answer was correct, so there
is a weak real signal underneath, but it is swamped because destroying a correct
answer costs more than rescuing a wrong one recovers; the challenge phrasing and
persona dominate the effect, which is why the authors read it as sycophancy.
Sheet 12: on WebShop the reflections themselves became unhelpful and drove
nothing.

Confirms / sharpens: [[CF-8]], [[F24]].
Sweep consequence: a "re-examine your last step" arm is measured for its net
effect — the Correct→Flip rate minus the Wrong→Flip rate — and the
challenge / critique prompt wording is a first-class sweep factor, not a fixed
string.

##### CF-26 — A fresh isolated session of the same model removes the trajectory contamination channels at near-zero cost; it does not remove the shared-weights channel. `[SWEEP]`

Sheet 05: "self-probing" runs the check in a second, independent session shown
only the question and the answer, and it was the most consistent prompting gain
on GPT-4.
Sheet 02: the same-shape "S.V." self-verification baseline is real but weak, and
falls off sharply once recall drops below about 0.8.
Sheet 06: with authorship anonymised, a model still scores its own output higher
by 3.6 to 9.4 per cent on a ten-point scale — that residual is what a fresh
session does *not* recover.

Consequence: a fresh session with an artifact-only input closes the
shared-context, framing, and label-leak channels (the isolation contract) for the
price of one extra call. It leaves the shared-weights channel open — correlated
blind spots and a bounded self-preference — which only a different model closes.
Confirms / sharpens: [[CF-1]], [[F44]]; bounds [[PI-3]].
Sweep consequence: include "fresh isolated session, same model, artifact only" as
a cheap verification tier between a deterministic check and a different-model
check, and measure how much of the different-model check's discrimination it
recovers.

##### CF-27 — A check is contaminated by the thing it checks through five identifiable channels, each closed by a different move. `[SWEEP]`

Synthesised from sheets 03, 05, 06 and topic-07 [[F44]]. Reusable as an analytic
instrument: for any verification design, enumerate which of the five it leaves
open.

| Channel | Mechanism | Closed by |
|---|---|---|
| 1. Shared context / session | the check sees the producer's reasoning and self-justification and anchors on the narration, not the artifact (sheet 06 revision framing; sheet 03 hedged trace raises recall, drops precision) | isolation contract: artifact + spec only |
| 2. Artifact framing | tone, "after careful review…", confidence language — moves the verdict more than corrupted reasoning does (sheet 06) | isolation contract: strip / normalise register |
| 3. Ground-truth leak | a reference value passed "for context" that deployment would not have (sheet 03's judge given the gold label) | isolation contract: no reference answer in the check input |
| 4. Shared weights | the same model rates its own output higher with authorship hidden (sheet 06, 3.6–9.4% on a 10-pt scale) and shares its blind spots — the errors the producer cannot see, the checker cannot see | a different model; a fresh session does **not** close this ([[CF-26]]) |
| 5. Optimisation coupling | the producing loop retries until the check passes; output drifts toward the check's blind spots; accept rate rises while true validity falls ([[CF-19]], [[CF-4]]) | one-way dataflow: check results are terminal (pass / fail / can't-tell → stop / abandon / escalate), never a score fed back as a gradient |

Confirms / sharpens: [[CF-1]], [[CF-19]], [[F44]]; grounds [[PI-3]], [[PI-10]], [[PI-11]].
Sweep consequence: for every verification arm, record which channels it leaves
open, and — where feasible — measure the arm's discrimination with a channel held
open versus closed.

##### CF-28 — What a check is allowed to see is a design space, not a single minimal rule; ARES demonstrated a cheap concurrent ensemble strategy for it. `[SWEEP]`

The isolation contract ("artifact bytes plus spec, nothing else") is one point in
that space. Topic-07 [[F44]] states the axis; topic-07 sheet 18 (ARES,
[[F45]]) fills in a different, cheap, concurrent point.

The known points:
- **Full context** — everything before the step. [[F44]] calls this the worst
  option (corruption propagates through the premise).
- **Minimal fixed** — artifact plus spec, one context. Requires you to know in
  advance what the check needs.
- **Projection** — one deterministically-extracted partial view ([[F47]]).
- **Stochastic soundness-weighted ensemble (ARES)** — the check does not get one
  context. Each earlier step is carried into a step's premise pool with a
  probability equal to how well it itself entailed — a doubtful step is
  statistically excluded from every downstream premise pool in proportion to how
  doubtful it looks. The score is the average over many such sampled premise
  sets, and the samples are embarrassingly parallel. A cheap operating point
  exists (ARES `eps = 0.4`: 17 samples, ~15× cheaper, small accuracy loss).

Consequence: the ensemble point has a property the minimal-fixed point lacks — it
is robust to *not knowing* which earlier context is load-bearing versus
corrupting, because a claim only lifts the score if it consistently supports the
step across subsets. It is resample-over-*contexts*, the complement of [[CF-2]]'s
resample-over-outputs, and a structured form of [[CF-10]]'s perturb-and-check.
Caveat from the sheet: ARES's own recommended config keeps *all* base claims
(`p = 1`) and only samples over derived steps; the cost floor is still 1–80
entailment calls per step, and its formalism is linear-chain only (no DAG / merge).
Confirms / sharpens: [[F44]], [[F45]], [[F42]]; extends [[PI-3]], [[PI-10]].
Sweep consequence: add "stochastic soundness-weighted premise ensemble" as a
verification-context arm distinct from minimal-fixed and full-context, and price
it at its cheap operating point, not its headline one.

##### CF-29 — Across the sheets, the trustworthiness of a validation runs inverse to its context continuity with the work. `[SWEEP]`

**→ Graduated to `00d-findings.md` as F2 (2026-09-09).** The process-continuity
part carries; the task-info-symmetry question travels with F2 as an open sub-note.

*Answering the design-discussion question: "how straight is the context
continuity between the work and the validation?"*

Three regimes appear.

- **Shallow continuity — the validation reads the work's narration — is poison.**
  Sheet 06: showing the judge the revision history inflates the score by about a
  point on a ten-point scale with the justification unchanged. Sheet 03: judging
  the reasoning trace instead of only the final answer raises recall and *drops*
  precision, because the trace hedges indiscriminately. [[CF-11]], [[CF-12]]:
  stance, tone, and provenance in the work's own output move the verdict more
  than corrupted reasoning does. The isolation contract ([[CF-27]]) exists to cut
  exactly this continuity.
- **Deep continuity — the validation reads the work's internal state — is
  mixed.** Sheet 14: a probe on mid-layer activations separates answerable from
  unanswerable at AUROC 0.87–0.97. Sheet 07: softmax-dispersion features from the
  work's own forward pass correlate about 0.6 with quality. Both are maximally
  continuous, and both inherit the work's blind spots — sheet 07 cannot catch a
  confident hallucination because the signal *is* the work's confidence.
- **No process continuity — the validation re-derives from the artifact — is the
  only kind the surveys trust.** Sheet 12 (Reflexion): removing the self-written
  test check makes the loop worse than not iterating. Sheet 01 (Kamoi): the fair,
  reliable cases are external tools — interpreter, proof assistant, symbolic
  checker — none of which read how the work was produced.

**Two axes that get conflated — and no evidence separating them.** *Task*
information (the spec, the inputs, the tools the work had) versus *process*
information (the trajectory, how the work went). The three regimes above are all
about process continuity, and the evidence says cut it. Whether *task*-info
symmetry between work and validation matters is **not measured by any sheet**.
The only nearby thing is sheet 01's "information symmetry", which is an
experiment-validity rule (to test unaided self-correction the two stages need
equal information, or you measure the information not the correction) that sheet
01 itself says does not transfer to deployment. Open question, not a finding.

**Internal tension.** Cutting process continuity — the isolation contract,
[[CF-27]] — *is* an information asymmetry: the validation then knows less than
the work did. So any "keep information symmetric" claim can at most be about task
info, and even that is an argument, not a result.

Confirms / sharpens: [[CF-27]], [[CF-28]], topic-07 [[F44]]; grounds [[PI-3]],
[[PI-10]], and [[PI-12]]'s one-way-dataflow constraint.
Sweep consequence: treat work↔validation continuity as an explicit factor with
three levels (narration-continuous / state-continuous / re-derived), and expect
discrimination to be worst at the first and the surveys' trust to sit at the
third.

##### CF-30 — A check's resource is either draft-independent (should have been given to the work) or draft-dependent (the asymmetry is structural). `[SWEEP]`

**→ Graduated to `00d-findings.md` as F3 (2026-09-09).**

Sheet 01 (Kamoi) splits validation-stage resources into two kinds, and the split
is a design lever, not just an experiment-fairness label.

- **Draft-independent** — a fixed knowledge base, retrieval over a static
  corpus, a type checker, the task spec, a linter. Nothing stops the work from
  using these. If only the check uses them, the loop is under-equipped: the work
  keeps failing for a reason it cannot fix, and retry does not help. Kamoi calls
  this "unfair-asymmetric" and the fix is to give the resource to the work.
- **Draft-dependent** — a code interpreter (needs code to run), retrieval where
  the draft *is* the query, claim-level fact-checking (needs asserted claims to
  check). The resource only becomes usable once a draft exists, so the asymmetry
  is inherent. Kamoi calls this "fair-asymmetric". Two reasons it is real: a
  vague task retrieves poorly while a draft names the entities that sharpen
  retrieval; and you cannot know what to check until something asserts it.

Confirms / sharpens: sheet 01's fair / unfair-asymmetric distinction, made
operational; relates to [[CF-29]], [[PI-10]], [[PI-12]].
Sweep consequence: when a verification arm uses a resource, classify it. A
draft-independent resource used only at check time is a configuration error to
flag, not a result to report. In a loop, a draft-independent resource that the
check needs must be pushed up to the work through the planner ([[PI-12]]), not
kept at the check.

### Round 5 additions (sheets 17–20)

Sheets 17 (Knowing When to Quit, ICML 2026), 18 (Agentic Abstention), 19
(Meta-Reasoner), 20 (Semantic Entropy). Two of these are the trajectory-native
work the rounds 1–4 sheets kept flagging as missing.

#### One-line claim list

- **CF-31** — The stop problem is a *timing* problem, not a detection problem:
  agents reach the right verdict, late. `[SWEEP]`
- **CF-32** — Stopping behaviour is a property of the harness, not the model.
  `[SWEEP]`
- **CF-33** — The quantity worth estimating for a stop decision is P(the attempt
  ends well), thresholded at the fallback's utility — not "does the current
  state look right". `[SWEEP]`
- **CF-34** — Semantic entropy is the best-evidenced instance of "resample
  spread beats self-report", and its stated blind spot is the canonical
  statement of the stability-not-correctness caveat. → **merge into F4.**
- **CF-35** — The one learned meta-level controller in the literature still
  defers "done" to the base model's self-report. `[background]`

#### Full text

##### CF-31 — The stop problem is a timing problem, not a detection problem. `[SWEEP]`

Sheet 18 (Agentic Abstention): every one of 13 systems reaches roughly 83 per
cent *eventual* abstention recall but under 40 per cent *timely* recall (best web
baseline 26.7 timely vs 83.2 eventual), scored against an annotated
earliest-warranted step. Agents do work out that a task is impossible — after
many wasted tool calls. Sheet 17 (Knowing When to Quit) gives the cost of the
opposite error a name: an "expected recovery surplus" term in its dominance
proof, the value a too-early quit throws away.

Consequence: this refines [[CF-5]]. The failure is not "the model never stops",
it is "the model stops late". Over-abstention on solvable tasks does rise as
budgets lengthen (34 per cent by turn ten in sheet 18), so the early-quit error
is real but smaller.
Confirms / sharpens: [[CF-5]], [[CF-16]].
Sweep consequence: the stop-decision metric must be *timely* recall against an
annotated earliest-warranted step, not eventual recall. Report both, and report
over-abstention on a solvable control set alongside.

##### CF-32 — Stopping behaviour is a property of the harness, not the model. `[SWEEP]`

Sheet 18: holding the model fixed (GPT-5.4-mini), the scaffold alone roughly
doubles abstention recall — Codex CLI 0.38 versus Terminus 2 0.18. Sheet 19
(Meta-Reasoner): the controller's action set has no terminal arm, so the
architecture decides that stopping is *not expressible* regardless of the model.
Sheet 17: the stopping rule is an external probe plus a threshold, not a model
capability.

Consequence: direct support for siting the stop decision in the harness (F1's
consequence). "Which model" is a weaker lever on stop behaviour than "which
scaffold".
Confirms / sharpens: [[F1]]; new for the register otherwise.
Sweep consequence: treat the scaffold as a first-class factor in the stop-decision
sweep, at least as important as the model. A model comparison that holds the
scaffold fixed measures the smaller effect.

##### CF-33 — The quantity worth estimating for a stop decision is P(the attempt ends well), thresholded at the fallback's utility. `[SWEEP]`

Sheet 17 (Knowing When to Quit): model chain-of-thought as a sparse-reward MDP
with an abstention action carrying a fixed fallback reward; the optimal rule is
to quit when the value function drops below that reward. Because reward is binary
and terminal, the value *is* P(this trajectory eventually yields a correct final
answer), estimated by a small hidden-state probe. It beats every baseline on
selective accuracy at every abstention rate, most on the hard set (0.64 vs 0.34
at 90 per cent abstention).

Consequence: this is the constructive alternative to the stability caveat folded
into [[F4]]. Stability ("the answer stopped moving") is a proxy; forward
eventual-correctness probability is the target, and it is estimable. One
threshold, denominated in the fallback's utility, sets escalation rate and cost
together.
Caveat: the probe needs hidden states no API exposes; the two API-accessible
alternatives sheet 17 tests (prompt-self-assess, fine-tuned abstain tokens)
perform at or below no-abstention, even shown partial work. Single-chain only.
Confirms / sharpens: [[F4]], [[CF-23]].
Sweep consequence: add a "forward value probe" arm — estimate P(attempt ends
well) over prefixes, threshold in fallback-utility units — distinct from the
resample-stability arm and the self-report arm.

##### CF-34 — Semantic entropy: the strongest evidence for resample-spread over self-report, and the sharpest statement of the stability caveat. `[SWEEP]` → merge into F4

Sheet 20: sample about ten generations, cluster them by *meaning* (bidirectional
entailment), take entropy over the meaning-clusters. Over 30 model-task pairs it
reaches 0.790 AUROC for flagging wrong answers, against 0.698 for `p(True)` and
0.687 for a supervised embedding probe. The model fragments its samples across
more meanings when it is about to be wrong (3.89 clusters vs 1.89 on TriviaQA).
Its stated blind spot is exact: it detects "confabulations" — answers that are
wrong *and arbitrary* — and is explicitly no help against systematic error,
absorbed misconceptions, reward-seeking, or the case where every sample agrees on
the same wrong answer. It also degrades where output quality degrades (at
temperature 1.5 the entailment classifier drops to 61 per cent and the method
loses to a simpler baseline).

Recommendation: fold into [[F4]] as its canonical evidence and its sharpest
caveat statement; do not keep as a separate finding.

##### CF-35 — The one learned meta-level controller in the literature still defers "done" to the base model's self-report. `[background]`

Sheet 19 (Meta-Reasoner): a LinUCB bandit reads a summary of the reasoning so far
and picks a guidance instruction (backtrack, restart, continue, decompose,
verify, …). None of the arms is terminal. "Done" falls back to the base model's
unverified self-report inside its own generation prompt; "failing" is diagnosed
in prose but can only be turned into another continuation; exhaustion is a fixed
round cap. The progress signal is an LLM's guess about a self-authored summary,
with no ground truth in the loop and no measured faithfulness.

Consequence: lifting the controller to a meta level does not by itself escape
[[F1]]. A learned-controller sweep arm needs an explicit grounded terminal
signal wired in; it will not emerge from a progress-report reward as built.
Confirms / sharpens: [[F1]], [[CF-20]].
Sweep consequence: if a learned-controller arm is run, its stop signal must come
from an external check or a forward value probe ([[CF-33]]), not from the
progress report.

---

## 2. Proposed ideas

*Draft form: claim / how it would be validated / what would falsify it / which
graduation target it aims at. Not locked. You scan, you pick.*

### PI-1 — The stop decision is an external-check-plus-trajectory-statistic decision, never a self-report.

**Claim.** The harness computes its stop / continue / escalate signal from two
sources only: deterministic external checks where the task admits them, and a
small fixed set of trajectory statistics (answer-stability across resamples,
repeated-action detection, no-progress counters, budget consumed). It never
computes that signal from the model's answer to "are you done" or "are you
stuck".
**Validation.** On a task suite with known ground-truth stop points, the
external-plus-trajectory signal beats a self-report gate on late-stop error at
equal compute.
**Falsifier.** A self-report gate matches or beats it, or the
external-plus-trajectory signal has no better stop precision and recall than
chance on the artifact types in scope.
**Graduation target.** Documented design principle for the system itself (target
2), with a path to load-bearing design (target 1).
Builds on CF-1, CF-4. Related: [[F11]], [[F17]], [[F41]].

### PI-2 — Extend I11 to the stop decision: retrospective stop-point ground truth.

**Claim.** Once a task is solved, reconstruct from the solution the earliest
trajectory point at which a correct stop was possible, and grade the harness's
actual stop decision against that reconstructed point.
This is the same move as [[I11]] (reconstruct the load-bearing context from the
solution), applied to *when* rather than *what*.
**Validation.** The reconstructed stop point is stable across annotators and
across independent re-derivations from the same solution.
**Falsifier.** The reconstruction is too noisy to rank two stop policies, or it
only works on solved tasks and the survivorship bias swamps the signal.
**Graduation target.** Standing evaluation instrument (target 4).
This may be better folded into I11 as a second application rather than kept as a
separate idea; flagging it for your call.

### PI-3 — Stop-evaluator isolation contract.

**Claim.** Any model call whose output gates a stop / continue decision receives
the latest artifact alone: no attempt history, no prior-attempt scores, no
authored-by or revised-from provenance, and tone normalised toward neutral.
**Validation.** On the CF-10 perturbation suite, the isolated evaluator's
verdict-flip rate under the history-visible and register-swap perturbations drops
relative to a naive evaluator, with no loss of verdict quality on clean inputs.
**Falsifier.** Isolation does not reduce the flip rate, or it removes a signal
the evaluator needs and verdict quality on clean inputs drops.
**Graduation target.** Invariant or enforcement constraint (target 5): a hard
rule the enforcement gate checks — stop-gating calls run against the isolation
contract.
Builds on CF-11, CF-12. Related: [[F44]].

### PI-4 — The double-run noise floor as a gate precondition.

**Claim.** Before an evaluator-based stop gate is trusted inside the loop, the
harness runs it twice on the same unperturbed input and records the disagreement
rate. A gate whose own noise floor exceeds a set bound is demoted to advisory and
cannot terminate the loop on its own.
**Validation.** The double-run disagreement rate predicts the gate's downstream
stop-decision error.
**Falsifier.** The double-run rate is uninformative about downstream error, or it
is always negligible, which would make the check pointless.
**Graduation target.** Standing evaluation instrument (target 4) shading into
enforcement constraint (target 5).
Builds on CF-9. Related: [[F52]].

### PI-5 — Parallel-resample-and-compare as the default intrinsic stop signal, with an explicit per-artifact equivalence relation.

**Claim.** The harness's cheapest always-on stop signal is M ≈ 5 parallel
resamples of the current step plus a task-type-specific equivalence check.
Stability across resamples licenses a stop *attempt*; an external check then
confirms or rejects it.
The equivalence relation is declared per artifact type (exact match for a scalar
answer, AST or test-behaviour equivalence for a code edit, a clustering rule for
prose).
**Validation.** On the task suite, resample-stability plus external confirmation
reaches the late-stop error of an oracle stop at under twice the compute.
**Falsifier.** Saturating M gives no usable separation on the artifact types in
scope, or the equivalence relation is intractable to define for trajectories and
multi-file edits.
**Graduation target.** Load-bearing design (target 1) or documented design
principle (target 2).
Builds on CF-2, CF-3. Related: [[F51]], [[I1]].

### PI-6 — Budget the stop decision as a queue-level scheduler, not a per-task switch.

**Claim.** Compute freed by stopping one task early is re-allocated to a task the
same harness is currently struggling with. The stop threshold is set to maximise
throughput across the queue, not success on the task in hand.
From sheet 04's Dynasor, which treats stopping as a scheduling decision across a
request queue.
**Validation.** On a batch of tasks under a fixed total compute budget,
queue-level stop thresholding beats per-task thresholding on aggregate success.
**Falsifier.** No gain over per-task thresholding, or the coupling between tasks
makes individual-task behaviour too unpredictable to debug.
**Graduation target.** Research perspective with a manageable test budget (target
3) — it is a single batch experiment.
Related: context-as-governed-resource.

### PI-7 — The loop controller has three outcomes, not two: continue, commit, abandon.

**Claim.** The harness's loop controller emits one of {continue, commit,
abandon-or-hand-off}. The abandon path has its own dedicated trigger — a
solvability probe ([[CF-23]]), a repeated-failure-signal counter on the retry
edges ([[CF-22]]), or a scope-dominating budget breach ([[CF-21]]) — and is never
derived from the commit path's stability score.
**Validation.** On a task suite that includes genuinely unsolvable and
underspecified tasks, the three-outcome controller reaches a lower fabrication
rate than a two-outcome (stop / continue) controller at equal task success on the
solvable tasks.
**Falsifier.** The abandon path fires mostly on solvable tasks (it over-abandons),
or a two-outcome controller with a good stop signal matches the fabrication rate.
**Graduation target.** Documented design principle (target 2), with a path to
load-bearing design (target 1).
Builds on CF-17, CF-6, CF-22, CF-23. Related: [[PI-1]].

### PI-8 — Keep every round's artifact and select at the end, rather than trusting the stopping round.

**Claim.** The loop retains each round's artifact and applies a selector at
termination. A mediocre stop time then costs little, because a better earlier
round is still recoverable.
From sheet 09's own reframe: an oracle best-round selector beat every practical
stopping policy by a wide margin, and a "return the first grounded draft" policy
beat the semantic stopper on both axes.
**Validation.** On the task suite, retain-and-select comes within a small margin
of the oracle best-round score and beats stop-time-only selection.
**Falsifier.** The end-of-loop selector is no better than "take the last round" —
the selection problem is as hard as the stopping problem with no net gain.
**Graduation target.** Research perspective with a manageable test budget (target
3) — one replay experiment over cached trajectories.
Builds on CF-16. Related: [[I1]], [[CF-2]], [[PI-5]].

### PI-9 — Does planner-controlled verification actually self-correct, or is structural mandate needed?

*From design discussion 2026-09-08, not from a sheet. Framed as an open
empirical question, per the user.*

**The conjecture under test.** The worry is that letting the orchestrator's
planner decide whether verification runs, what it checks, and what it sees is the
producer auditing itself. The counter-conjecture is that a planner which emits
weak verification builds later steps on unreliable work, that work fails
downstream, and the planner's incentives are reworked by that feedback — so no
structural mandate is needed, self-interest suffices.
**Why it is not obvious either way.** The counter-pressure only works if the
downstream failure is (a) attributable to weak verification and (b) visible to
whatever signal trains or selects the planner. CF-6 (fabricated context passes
shape checks) and CF-19 (accept rate rises while true validity falls) are
failure modes that are invisible to the loop's own signals — which is exactly
the class of failure weak verification would let through.
**Validation.** Run a planner with and without a structural always-on check set,
on a task suite seeded with tasks whose correct verification is non-trivial;
measure whether the unstructured planner's verification quality degrades over
successive planning rounds or holds, and whether its downstream failure rate is
distinguishable from the structured one.
**Falsifier of the worry.** The unstructured planner's verification quality stays
flat or improves under downstream feedback, and its task-failure rate matches the
structured one — in which case the structural mandate is dead weight.
**Falsifier of the counter.** The unstructured planner's verification decays, or
its failures cluster in the CF-6 / CF-19 invisible class, so the feedback never
reaches it.
**Graduation target.** Research perspective (target 3); alternatively an entry in
the open-questions register if it is not going to be run soon.
Related: [[PI-1]], [[PI-3]], [[PI-7]], [[CF-6]], [[CF-19]], [[CF-20]].

### PI-10 — A verification-expert processor that picks the verification approach for a task from its objectives.

*From design discussion 2026-09-08. Skeleton — to be expanded with evidence.*

**Claim.** A dedicated ephemeral processor takes a task's objectives and
acceptance criteria and returns a *verification plan* for that task: which
strategy to use, what the checker is allowed to see, what counts as done, what
triggers abandon. It does not run the verification; it chooses it.

**Strategy nomenclature (three output / authority classes).**

- **Gated** — binary pass / fail, terminal, blocks on fail, one-way dataflow.
  Deterministic where possible. Home of the invariant checks and of
  task-specific tests, schema, and type checks. Reliable but narrow: it only
  covers what a rule can express.
- **Judged** — a graded or narrative assessment from a model, advisory, feeds a
  decision without enforcing. Broad coverage, low and non-transferable
  reliability ([[CF-18]], sheets 06 and 16). Never the sole terminator
  ([[CF-20]]); never a score the producing loop optimises against ([[CF-19]]).
- **Compound** — a judged check that can call auditing tools mid-assessment: run
  the test suite, grep the artifact, execute a probe, retrieve a reference, then
  reason over the results. Its output is a grounded report with evidence
  pointers, not necessarily a verdict and not necessarily enforcing. It is the
  middle path — it gives the judge the deterministic leverage a bare judge
  lacks, which is exactly the grounding check [[F42]] says a chain verifier is
  missing. Cost and reproducibility are worse than gated; grounding is better
  than judged. Its residual risk is that the judge still chooses what to audit
  and how to read a green result (sheet 03's judge handed the gold label).

**Crossed with two more axes.**

- *What runs it*: a deterministic tool (no model) / a fresh isolated same-model
  session, artifact only ([[CF-26]]) / a different model / a trained verifier
  model.
- *What it sees* ([[CF-28]] is the design space): minimal-fixed (artifact plus
  spec), a projection ([[F47]]), decomposed per-sub-question slices, or a
  stochastic soundness-weighted premise ensemble (ARES). The production
  trajectory is out in every case.

**Also selects channel exposure.** Every strategy leaves some of the [[CF-27]]
contamination channels open. The expert picks a strategy whose open channels the
task tolerates, and records which are open, so a downstream reader knows what the
"pass" is worth.

**Selection cases the expert must cover.**
- a deterministic gated check (test, schema, type check, projection);
- resample-and-compare, where an equivalence relation exists for the artifact
  type ([[CF-2]], [[CF-3]]);
- a fresh isolated same-model judged check ([[CF-26]]);
- a compound check when deterministic leverage exists but no single rule
  captures correctness;
- a decomposed verification task emitting addressable boolean traces ([[I10]]);
- the perturb-and-check instrument ([[CF-10]]);
- "no reliable cheap check exists" → treat the output as single-shot and
  escalate, or decompose the task further ([[CF-19]]: do not loop against a
  low-discrimination model verifier).
**Why an expert and not a fixed rule.** Sheet 01 (Kamoi) shows verification
difficulty is a property of the *task*, not the model — decomposability and
easy-verifiability are the structural features that decide whether any check
works, and they vary task to task. [[CF-18]] shows a verifier's discrimination
does not transfer across task families, so the choice has to be made per family
and measured.
**Validation.** On a task suite spanning verification-easy and verification-hard
tasks, the expert's chosen approach reaches higher stop-decision precision /
recall at lower verification cost than a single fixed approach applied to all
tasks.
**Falsifier.** One fixed approach (e.g. always a fresh isolated session) matches
the expert across the suite, or the expert's choices are no better than random
against retrospective ground truth ([[CF-15]], [[F49]]).
**Open tension.** The expert is itself a context-aware model making a choice, so
[[PI-9]] applies to it — is its selection self-auditing, or does downstream
failure rework it?
**Graduation target.** Documented design principle for the system itself
(target 2), with a path to load-bearing design (target 1).
Related: [[PI-1]], [[PI-3]], [[PI-7]], [[PI-11]], [[CF-26]], [[CF-18]], [[CF-2]], [[I10]].

### PI-11 — Verification is keyed to the processor's kind, not only the task.

*From design discussion 2026-09-08. To be expanded with evidence.*

**Claim.** Not all processors are executors. A planner, a context assembler, a
summariser, and a transform processor fail in different ways and admit different
checks, so the verification strategy ([[PI-10]]) is selected on processor kind as
well as task objectives.

**Kind → natural check and natural failure mode.**
- **Executor** — did the intended state change occur; gated deterministic checks
  fit well.
- **Planner / decomposer** — is the decomposition sound: are the sub-tasks
  independently checkable, is recombination defined ([[F42]], and topic 07's
  recombination-is-under-measured thread F13 / F22 / F28; Kamoi's decomposability
  property). This verifies a *plan*, not an output, so the check is structural,
  not a test.
- **Retrieval / context assembly** — was the load-bearing context gathered;
  recall against retrospective ground truth ([[I11]]) is the metric, not
  precision.
- **Summarise / compress** — was entropy reduced without dropping load-bearing
  content (topic 07 F39: overlapping or lossy context degrades the consuming
  step); a decomposed boolean-trace check fits ([[I10]]).
- **Transform / edit** — behaviour equivalence (AST, tests), not surface diff.

**Kinds are differentially exposed to the [[CF-27]] channels.** A planner checked
by the same model in shared context carries channels 1 and 4 heavily, because a
plan has no artifact to isolate from its rationale. A deterministic executor
check carries none. The verification-expert should weight channel exposure by
kind, not only by task.

**Validation.** A processor-kind-indexed verification table reaches higher
stop-decision precision / recall per kind than a task-objective-only selection.
**Falsifier.** Processor kind adds nothing over task objectives for predicting
the right check.
**Graduation target.** Documented design principle (target 2).
Related: [[PI-10]], [[PI-7]], [[I10]], [[I11]], [[F42]].

### PI-12 — Retry is a policy chosen per failure from a defined family, recorded and measured — not "again".

*From design discussion 2026-09-08.*

**Claim.** A check that returns fail, can't-tell, or recoverable triggers a
*retry policy*, selected per failure from a family the harness supports as
pluggable options and records. The deliverable of the idea is the measured
comparison of those policies, not a single prescription. "Not just again" is the
framing: every retry is a deliberate move informed by the check's outcome.

**The policy space — axes to explore.**
- *What the retry attempt receives*: the failed attempt; the diagnostic /
  feedback; a planned recovery route; an amended context; an adjusted processor
  selection — in various combinations.
- *Where it runs*: re-plan through the orchestrator; the same processor with an
  amended context; the same task routed to a different processor.
- *How much it sees*: full trajectory; or isolated, feedback only.
Each concrete retry policy is a point across these axes.

**Constraints that hold across every policy (these are not up for exploration).**
- Never a score the producing loop optimises against ([[CF-27]] channel 5,
  one-way dataflow; [[CF-19]], [[CF-4]]).
- Bounded: a recovery budget whose scope is the whole recovery *chain*, not
  per-task ([[CF-21]]) — an unbounded chain is [[CF-22]]'s runaway.
- Flagged: every retry marked as a retry of its parent, so the trajectory signal
  can see a non-converging chain.
- The retry's own output is verified; recovery does not skip the gate ([[CF-6]]).

**Sub-idea: "recoverable" is a fourth verification outcome.** The outcome set is
pass / fail / can't-tell / **recoverable**, where `recoverable` means a defect
*and* a plausible fix path were both found (a compound check can often name the
fix). `recoverable` is the outcome that selects a retry policy rather than
abandon.

**How it bears on the noted recovery limitations.** Topic 07 left recovery in
tension — [[F24]] / [[F20]] (a recovery loop buys accuracy) against [[F62]] ("no
recovery path" is viable when wide sampling plus an external selector
substitutes). Treating retry as a measured policy family, under the constraints
above, is the way to find where each side holds in practice instead of picking
one.

**Validation.** Run the retry policies as arms on a task suite with recoverable
and unrecoverable failures, partitioned by failure class and processor kind
([[PI-10]], [[PI-11]]); produce the table of which policy gives best net task
success per compute for each cell. Expect the winner to differ by cell.
**Falsifier.** One policy dominates every cell (the family was unnecessary), or
no policy beats a bounded blind re-run (the framing was wrong), or `recoverable`
cannot be told from `fail` reliably enough to select on.
**Open tension.** The planner selects the retry policy and the
recoverable-versus-abandon call, so [[PI-9]] applies.
**Graduation target.** Standing evaluation instrument (target 4) for the policy
comparison; documented design principle (target 2) once the table exists.
Related: [[PI-7]], [[PI-9]], [[PI-10]], [[PI-11]], [[CF-19]], [[CF-21]], [[CF-22]], [[CF-25]], [[CF-27]].

---

## 3. Reading queue

### Rounds 3 and 4 — done (8 booths)

All eight read and imported as sheets `09`–`16`; the cross-paper pass over them
is folded into section 1 above (CF-16…CF-25) and section 2 (PI-7, PI-8). Booth 14
hit a session rate limit mid-write and was resumed from its checkpoint. The
peer-reviewed corpus does not cover the agentic-loop stopping decision, so per
the topic-07 precedent for central preprints, rounds 3 and 4 read the 2026
preprints alongside the peer-reviewed anchors they build on.

**Round 3 — the agentic-loop-native cluster (the Subject's core, barely touched
by rounds 1–2).**

- **Booth 09 — "Semantic Early-Stopping for Iterative LLM Agent Loops"**
  (inventory #28, 2026 preprint). Halt when consecutive draft embeddings stop
  changing in meaning and measured quality plateaus; deterministic-termination
  proof; the "which round is best" reframe of the problem.
- **Booth 10 — "Verify, Repair, Repeat, or Stop? Robust Stopping for Noisy
  Verify-Repair Loops"** (inventory #30, 2026 preprint). A four-parameter noise
  model separating verifier false-accept and false-reject from repair damage;
  stop on the sign of the true marginal gain of another repair.
- **Booth 11 — "When Agents Do Not Stop: Uncovering Infinite Agentic Loops"**
  (inventory #29, 2026 preprint). The failure mode itself: static analysis of
  feedback paths that reach costly operations without an effective bound.
- **Booth 12 — Shinn et al., "Reflexion: Language Agents with Verbal
  Reinforcement Learning"** (inventory #8, NeurIPS 2023, anchor). The canonical
  self-reflection-gated retry loop; peer-reviewed; untouched by rounds 1–2.

**Round 4 — the uncertainty-signal and judge-reliability cluster.**

- **Booth 13 — Kadavath et al., "Language Models (Mostly) Know What They Know"**
  (inventory #3, 2022 anchor). P(True) and P(IK); four of the eight sheets read
  so far point at it as the white-box counterweight to the "self-report is
  useless" convergence.
- **Booth 14 — Liu et al., "Answering the Unanswerable Is to Err Knowingly"**
  (inventory #25, AAAI 2026, peer-reviewed). Large reasoning models have an
  internal sense of solvability but fail to express abstention — a measured
  "knows but does not say" result, which is exactly the question sheet 03 leaves
  open.
- **Booth 15 — Laban et al., "Are You Sure? The FlipFlop Experiment"**
  (inventory #12, preprint, central). Challenged with "Are you sure?", models
  flip their answer about 46 per cent of the time and lose about 17 per cent
  accuracy — the confirm-or-revise self-judgement and how sycophancy corrupts it.
- **Booth 16 — Norman et al., "Reliability without Validity: LLM-as-a-Judge
  across Agreement, Consistency, and Bias"** (inventory #27, 2026 preprint,
  central). 21 judges, ~541k judgments; kappa deflation; a consistency-versus-bias
  paradox; a Minimum Viable Validation Protocol. The large, recent complement to
  sheet 06.

### Not yet picked — strong RELATED entries left in the inventory

- **#9 "Just Ask for Calibration"** (EMNLP 2023) — verbalized confidence beats
  logits for RLHF-tuned models; the calibration-method angle.
- **#13 "R-Tuning: Instructing LLMs to Say I Don't Know"** (NAACL 2024) — a
  training route to abstention; refusal as a generalising meta-skill.
- **#14 "Calibrating Long-form Generations"** (Findings EMNLP 2024) — calibration
  when an answer can be partially correct; self-consistency plus self-evaluation.
- **#16 "Calibrating the Confidence of LLMs by Eliciting Fidelity"** (EMNLP 2024)
  — confidence decomposed into question-uncertainty and answer-fidelity.
- **#17 "LLMs Can Self-Correct with Key Condition Verification" (ProCo)** (EMNLP
  2024) — mask a key condition, reconstruct it to verify the response; a concrete
  when-self-correction-helps mechanism.
- **#20 "Know Your Limits: A Survey of Abstention in LLMs"** (TACL 2024) — the
  interventions landscape sheet 03 deliberately does not cover.
- **#21 "On Verbalized Confidence Scores for LLMs"** (preprint) — reliability of a
  verbalized score depends heavily on how the model is asked.
- **#31 Farquhar et al., "Detecting hallucinations using semantic entropy"**
  (Nature 2024) — the canonical uncertainty-based do-not-trust signal; its
  verbatim abstract is still missing from `00c` and should be captured before
  this entry is used.

### ADJACENT entries worth a later look

- **#6 "The Internal State of an LLM Knows When It's Lying"** (Findings EMNLP
  2023) — hidden-state probe for truthfulness of a statement.
- **#7 "SelfCheckGPT"** (EMNLP 2023) — black-box sampling-consistency
  hallucination detection.
- **#19 "Semantic Entropy Probes"** (NeurIPS 2024) — semantic entropy from one
  generation's hidden states.
- **#26 "Self-Reflection in LLM Agents"** (FLLM 2024) — self-reflection improves
  re-answering, but the wrong-answer trigger is an oracle.

### Gap-closing candidates found by search (this pass)

Two targeted searches were run for the angles the inventory was thin on. All the
hits are 2026 preprints, so they sit under the same central-preprint exception as
booths 09–11. Not yet inventoried with verbatim abstracts; that is the next
mechanical step if you want any of them read.

**Value-of-computation / decision-theoretic stopping.**

- **"Knowing When to Quit: A Principled Framework for Dynamic Abstention in LLM
  Reasoning"** (arXiv:2604.18419). Halt generation when a value-function estimate
  of the current state falls below an abstention-reward threshold. This is the
  "is another step worth its cost" framing directly. Strong booth candidate.
- **"Agentic Abstention: Do Agents Know When to Stop Instead of Act?"**
  (arXiv:2606.28733). An abstention benchmark for *agents* rather than for
  single-turn QA — the closest thing to sheet 03's setting moved into a loop.
- **"Doomed from the Start: Early Abort of LLM Agent Episodes via a
  Recall-Controlled Probe Cascade"** (arXiv:2607.06503). A cascade of cheap
  probes that aborts an episode early, with recall control on the abort decision.
  The abandon end of the Subject.
- **Meta-Reasoner** (arXiv:2502.19918). Summarise progress into a report each
  step, then a contextual bandit picks the guidance strategy or discards the
  avenue. Sheet 04 named this as the nearest thing in the literature to a
  *learned* progress judge; worth its own booth.

**Runtime stall / repeated-action detection as its own method.**

- **"Early Diagnosis of Wasted Computation in Multi-Agent LLM Systems via
  Failure-Aware Observability"** (arXiv:2606.01365). Cheap trace signals for
  stalled trajectories during execution, with selective LLM-as-judge validation
  rather than always-on cost.
- **"When Agentic Executions Fail: Detecting and Localizing Runtime Faults from
  Telemetry"** (arXiv:2608.14680). Runtime fault detection and localisation from
  trajectory telemetry.
- **"MIRAGE-Bench: LLM Agent is Hallucinating and Where to Find Them"**
  (arXiv:2507.21017). An agent-hallucination benchmark — the assumption-filling
  failure of CF-6 in an agentic setting.

Still uncovered after this pass: nothing glaring. The economic / anytime framing
now has entries; the runtime-signal side now has entries. A third search would be
into diminishing returns for this topic.
