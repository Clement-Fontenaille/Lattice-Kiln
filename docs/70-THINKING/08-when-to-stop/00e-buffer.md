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
Sweep consequence: the stop signal must come from outside the model's self-report
— an external check, or a trajectory statistic. "Ask the model whether it is
done or stuck" belongs in the sweep only as a floor baseline, not as a serious
arm.

#### CF-2 — Agreement across independently sampled attempts is the one intrinsic signal shown to work, and only where "the same answer" is definable. `[SWEEP]`

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

#### CF-3 — The signal these methods threshold on is answer-stability, not answer-correctness. `[SWEEP]`

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

---

## 3. Reading queue

### Fired — rounds 3 and 4 (8 booths, this pass)

The peer-reviewed corpus does not cover the actual agentic-loop stopping
decision; the dedicated papers are 2026 preprints. Per the topic-07 precedent for
central preprints, rounds 3 and 4 read them alongside the peer-reviewed
anchors they build on.

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

### Search gaps I would still like covered

The inventory is now strong on loop-stopping mechanisms (#28, #29, #30) and on
the self-evaluation / confidence side. Two angles are still thin, and one search
round each would likely close them:

1. **Value-of-computation / anytime framing of the stop decision.** Decision-
   theoretic "is another step worth its cost" work, as opposed to
   threshold-on-a-signal work.
2. **Runtime repeated-action and no-progress detection as its own method.**
   Inventory #29 is static analysis; the trajectory-signal side of the Subject
   (no state change, repeated actions) has no dedicated runtime-detection entry
   yet.
