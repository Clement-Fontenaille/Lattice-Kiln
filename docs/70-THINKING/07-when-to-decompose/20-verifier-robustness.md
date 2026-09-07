# Beyond the Answer Key: Robustness Evaluation of LLMs for Step-Level Mathematical Verification

## Density

**Density: MEDIUM.** This is a short conference paper whose load-bearing content is concentrated in two places — the checker semantics that define what counts as a valid trace step (Section III-C) and three result tables whose numbers are extreme enough to carry the argument on their own — while the surrounding framing, related work, and future-work prose are conventional; of that signal, the part that bears on the Subject is indirect but real, because the paper decomposes one verification objective into three named sub-questions and then shows that the sub-questions degrade at very different rates.

## Name

Fateme Mazdarani and Carlos Toxtli, "Beyond the Answer Key: Robustness Evaluation of Large Language Models for Step-Level Mathematical Verification."

- **Year.** 2026. The arXiv record shows submission on 28 August 2026, listed under cs.AI, version v1.
- **Venue.** Accepted to the 2026 IEEE International Conference on Machine Learning and Applications (ICMLA), per the arXiv comments field.
- **Source used.** I retrieved the paper from arXiv:2608.28725. The identifier given in the reading brief resolves correctly and is not a typo; I read the full-text HTML rendering at `https://arxiv.org/html/2608.28725`, and cross-checked the metadata on the abstract page at `https://arxiv.org/abs/2608.28725`. The authors also release the benchmark and code at `https://github.com/mazdarani/beyond-answer-key`, which I did not open.
- **Keywords (mine).** Evaluator robustness; step-level verification; process versus outcome supervision; template sensitivity; false rejection of valid reasoning; first-error localization; trace equivalence semantics; majority-vote failure amplification; verifier as accept/reject gate.

## Approach

The authors argue that most mathematical evaluation of language models measures the model as a *solver* and reports final-answer accuracy, which hides a different failure mode: a model may grade a familiar worked solution correctly while rejecting an unfamiliar but mathematically sound derivation. They name this failure mode **template sensitivity**, defined as dependence on a familiar solution template rather than on step-level validity.

To isolate it, they build a deliberately narrow benchmark. Every problem is a single-variable linear equation of the form `ax + b = cx + d`, with integer coefficients sampled from the range [-10, 10] and the constraint `a ≠ c`, so the solution `x = (d - b)/(a - c)` is unique and rational. A solving engine then emits a worked trace for each equation, and the model under test is never asked to solve anything. It receives the original equation plus a complete worked trace, and it must return a strict JSON object with three fields:

- **Q1** — a Boolean: does the final answer satisfy the original equation? (outcome checking)
- **Q2** — a Boolean: is the full trace mathematically valid? (process checking)
- **Q3** — an integer: the index of the first invalid step, or -1 if no step is invalid. (diagnostic localization)

Step indexing is 0-based and step 0 is the original equation string. A malformed response is recorded as a parse error and counted as incorrect for the affected metrics, so the JSON-formatting burden is folded into the scores rather than excluded.

Traces come in three types, which are the mechanism that separates outcome from process:

- **T1 (Correct)** — every transition preserves equivalence under the checker semantics and the final answer is correct. T1 exists specifically to measure *false rejection* of valid reasoning.
- **T2 (Incorrect)** — a single arithmetic or algebraic error is injected at a known step and propagated through to a wrong final answer. T2 tests whether the evaluator both detects and correctly localizes the true first error.
- **T3 (Tricky)** — the trace contains a genuinely invalid intermediate step, but the final answer is manually reverted to the correct value. T3 is the instrument that decouples final-answer checking from process checking, because a model that only inspects the endpoint will accept it.

The controlled comparison is between a **canonical** trace and a **perturbed** trace *for the same equation*. The equation is held fixed and only the derivation varies, so the model is not being asked to solve a harder problem; it is being asked to judge a supplied derivation that reaches the same place by an unusual route.

Beyond measuring base models, they test three interventions: LoRA supervised fine-tuning (FT), distillation of richer natural-language rationales from a teacher model (GED-FT), and majority-vote test-time compute (TTC).

## How the perturbed traces are built, and whether they are genuinely equivalent

This is the part of the paper I looked at hardest, because the whole result depends on it: if the perturbed T1 traces were not actually valid, then the reported false-rejection rates would be measuring the checker's mistakes rather than the model's.

The authors anticipate the objection directly, in Section III-C. They state the concern in their own words — not every familiar algebraic manipulation is an equivalence over the real line, since multiplying both sides by an expression that may be zero, or squaring both sides, can introduce extraneous candidates. Rather than treating any syntactic transformation as a bidirectional equivalence, they define a **checker semantics** over solution sets. Writing `S_i(x)` for the solution set represented by step *i*, and `O_i` for any active obligation such as verifying a candidate or recording a nonzero denominator, they sort each transition into three categories:

1. **Strictly equivalent** — `S_i(x) ⇔ S_{i+1}(x)` over the active domain. This covers adding the same expression to both sides, moving terms across the equality with a sign change, and multiplying or dividing by a *known nonzero constant*.
2. **Candidate-generating** — `S_i(x) ⇒ S_{i+1}(x)`: all true solutions are preserved but extra candidates may appear. This is accepted **only if** the trace later verifies every candidate against the original equation and discards extraneous roots. Multiplication by a variable term and squaring both sides fall here.
3. **Invalid** — the step contains an arithmetic error, drops a valid candidate, introduces an unsupported restriction, or leaves an obligation unresolved.

`Q2 = 1` if and only if every transition is either strictly equivalent or candidate-generating, and `Q3` is the first transition where that condition fails. All gold labels are generated and validated by a deterministic exact-arithmetic trace checker, and generation rejects degenerate equations, empty transformations, and traces whose verification obligations cannot be discharged.

There are six perturbation families. Four are strictly equivalence-preserving in this domain: adding terms to both sides, moving terms to the right-hand side, multiplying by a nonzero constant, and dividing by a nonzero constant. Two are obligation-generating: multiplying by an expression involving `x`, and squaring both sides; for these the generated trace explicitly substitutes the resulting candidate set back into the original equation.

**My reading of whether they are genuinely equivalent.** The claim holds, but with a precision worth stating rather than glossing. Four of the six families are step-wise logical equivalences in the strict sense. The other two are *not* step-wise equivalences and the authors do not pretend otherwise — they are one-directional implications whose soundness is restored at the level of the whole trace by an explicit discharged obligation. So the accurate statement is that a perturbed T1 trace as a whole represents the same solution set as the original equation and is valid under a stated, mechanically enforced semantics, even where an individual step inside it is not a biconditional. That is a stronger and more honest construction than a benchmark that simply asserts "these variants are equivalent," and it means the false-rejection numbers are measuring model behavior rather than label noise. The residual caveat is structural rather than logical: because the obligation-generating families require an added substitution-and-discard segment, those perturbed traces are longer and differently shaped than their canonical counterparts, so trace length and the presence of a verification tail are confounded with the perturbation itself. The paper does not separate these, and explicitly lists per-perturbation-family breakdowns as future work, so we cannot tell from the reported numbers whether rejection concentrates in the two obligation-generating families or is spread evenly across all six. The authors are also careful to state the scope limit themselves: these are controlled stress tests of whether models distinguish valid alternative paths from errors, and are not intended to represent the full distribution of real student work.

## Models targeted and benchmarks / datasets used

**Models.** Three open-weight, reasoning-oriented models: GPT-OSS 20B, Qwen3-14B, and Phi-4-Reasoning. The authors state these were chosen after a preliminary screening step whose purpose was to avoid conflating evaluator robustness with a basic inability to follow mathematical notation — that is, they deliberately excluded models that would have failed for the wrong reason. No proprietary frontier model is evaluated as a subject; Gemini 3 Flash appears only as the distillation *teacher*, not as a system under test.

**Dataset.** The benchmark is generated by the authors rather than drawn from an existing corpus, which is a consequence of needing exact first-error indices. Composition:

- **Training set:** 27,000 samples — 9,000 canonical traces split evenly across T1/T2/T3, and 18,000 perturbed traces split evenly across trace type and perturbation family.
- **Evaluation:** two held-out sets of 1,080 samples each, one canonical and one perturbed, with 360 samples per trace type; the perturbed set is balanced across the six perturbation families.
- **Leakage control:** train and test splits are instance-disjoint by construction. The tuple `(a, b, c, d)` is hashed *before* trace generation, so no equation can appear in both training and evaluation.
- **Released metadata per sample:** the equation tuple, trace type, perturbation family, obligation log, gold labels, and the checker's explanation.

The GED-FT training set is a filtered subset: teacher explanations are retained only where the teacher's explanation preserves the ground-truth `(Q1, Q2, Q3)` labels, which yields 4,000 samples. This is an important detail — the distillation condition trains on roughly one-seventh the data of the FT condition, so FT and GED-FT differ in data volume as well as in rationale quality.

GSM8K and MATH are cited as the outcome-focused benchmarks this work is positioning against, not as datasets used.

## Author incentive

Two authors, Fateme Mazdarani and Carlos Toxtli. Institutional affiliations are not printed in the arXiv HTML rendering and are not shown on the abstract page, so I cannot state them from the primary source; the acknowledgment records support in part from the US National Science Foundation under Award No. 2434704. The self-citation ([13], Mazdarani, Hernandez and Toxtli 2026, on transparent explanations for trustworthy task recommendation in crowd work) suggests a prior line of work on trust and explanation in human-facing AI systems, and it is cited in the introduction precisely to support the claim that users may trust explained outputs without understanding their limitations. That is a coherent through-line rather than a padding citation.

The stake here reads as academic and agenda-setting rather than commercial. There is no product, no model, and no service being promoted; the artifact on offer is a benchmark and its code, released publicly. The incentive that does exist is the usual one for a benchmark paper — the finding must be striking enough to justify the benchmark's existence, and the paper's central number (false-rejection rates of 75.6–85.3%) is duly striking. It is worth noting in that light that the authors chose the models after a screening pass, and that the domain was chosen for controllability; both choices are disclosed, but both also work in the direction of a clean, quotable failure. Against that, the paper repeatedly undercuts its own strongest reading: it states plainly that the domain is narrow, that adaptation gains are model dependent, that results are single-run, and that small differences between variants should be interpreted cautiously.

## Measurement methodology (brushed)

**Dependent variables.** Accuracy on each of Q1, Q2 and Q3, reported overall and stratified by trace type T1/T2/T3. There are therefore twelve numbers per model per condition, and the paper prints all of them, which is what makes the tables readable against the authors' claims.

**What is controlled.** The equation is held fixed across the canonical/perturbed pair, so the manipulated variable is the *form of the derivation* and nothing else about the problem. The evaluation sets are balanced by construction — 360 samples per trace type, and the perturbed set is additionally balanced across the six perturbation families. Gold labels come from a deterministic exact-arithmetic checker rather than from human annotation or from a model, which removes grader subjectivity from the dependent variable. Decoding is deterministic for all non-TTC evaluations; TTC uses seven independent samples at temperature 0.3 and takes a majority vote per output field. All runs use bf16 precision with gradient checkpointing, via Hugging Face Transformers and PEFT.

**N.** 1,080 samples per evaluation set (canonical and perturbed separately), 360 per trace type. Training is 27,000 samples for FT and 4,000 for GED-FT. LoRA hyperparameters are given: learning rate 2e-4, rank in {8, 16}, alpha in {16, 32}, 3 epochs, batch size 16.

**How significance is treated.** It essentially is not, and the authors say so. Adaptation results are single-run, with no confidence intervals, no error bars, and no repeated seeds; the limitations section asks the reader to interpret small differences between variants cautiously. The paper's defence is implicit in the size of the effects — a drop from 98.33% to 24.44% on the same 360 items does not need an interval to be believed, whereas the finer comparisons between FT, GED-FT and their TTC variants genuinely do, and those are the comparisons the authors decline to lean on hard.

**How the rates are defined.** This is stated cleanly in Section III-E. For T1 traces, `1 - Acc(Q2)` *is* the false-rejection rate: the evaluator rejected a valid trace. For T2 and T3 traces, a high Q2 error rate indicates false acceptance of an invalid process. Localization accuracy is intentionally strict and requires exact agreement with the first-error index — no partial credit for being close.

## Key findings

### The base-model robustness gap

All three base models are strong on canonical traces and fall apart on perturbed ones. Overall accuracies for the base models, canonical → perturbed:

| Model | Q1 | Q2 | Q3 |
|---|---|---|---|
| GPT-OSS 20B | 97.69 → 76.30 | 98.24 → 54.06 | 98.06 → 24.07 |
| Qwen3-14B | 83.61 → 71.67 | 86.48 → 52.69 | 86.02 → 14.35 |
| Phi-4-Reasoning | 96.48 → 67.87 | 96.11 → 63.43 | 95.93 → 19.81 |

The degradation is ordered consistently across all three models: Q1 degrades least, Q2 more, Q3 most. The authors read this as showing that first-error localization is substantially harder than final-answer checking, and that the collapse is not a formatting artifact.

### The three sub-tasks degrade very differently

This is the finding most directly relevant to the Subject, because Q1/Q2/Q3 constitute a decomposition of one verification objective into three sub-objectives, and the paper shows that the sub-objectives are neither equally hard nor independent.

**Q1 (final answer).** Relatively robust in aggregate, losing roughly 12 to 29 points. But the aggregate hides where the damage lands: it lands on T3, the trace type where the answer is right and the process is wrong. Base-model Q1 accuracy on T3 falls from 96.67% to 67.78% (GPT-OSS 20B), 71.39% to 63.06% (Qwen3-14B), and 99.44% to 56.94% (Phi-4-Reasoning). Since the final answer is correct by construction in T3, the authors read these drops as evidence that an unfamiliar-looking derivation *contaminates* the final-answer judgment. Their conclusion is that outcome and process are entangled: a grader should not reject a correct answer because the derivation is unusual, nor accept flawed reasoning because it reaches the right endpoint, and these models do both.

**Q2 (step-level validity).** This is where the headline number sits, and it is asymmetric in a way the aggregate obscures. On canonical T1 traces, base-model Q2 accuracy is 98.33%, 93.89% and 92.22% for GPT-OSS 20B, Qwen3-14B and Phi-4-Reasoning. On perturbed T1 traces these fall to 24.44%, 16.11% and 14.72%. The authors report the complements directly as false-rejection rates: **75.56%, 83.89% and 85.28%** on valid perturbed traces.

**Q3 (first-incorrect-step).** The bottleneck, degrading to 24.07%, 14.35% and 19.81% overall on perturbed traces — near or below what indexing into a short trace would give by chance. The authors' reading is a practical one: localization is what converts a judgment into usable feedback, and a verifier that says a trace is wrong but points at the wrong step will send a downstream generator to revise the wrong part of its reasoning.

### False rejection and false acceptance are reported separately

Yes — and this is one of the paper's better design decisions. The T1/T2/T3 stratification exists precisely to separate the two error directions, and every table prints the per-trace-type columns needed to read them off. Section III-E defines them explicitly, as quoted above.

Reading false acceptance off the base-model perturbed rows (as `1 - Q2` on T2 and T3):

| Model | FRR (T1, perturbed) | FA (T2, perturbed) | FA (T3, perturbed) |
|---|---|---|---|
| GPT-OSS 20B | 75.56 | 28.28 | 28.00 |
| Qwen3-14B | 83.89 | 31.94 | 26.11 |
| Phi-4-Reasoning | 85.28 | 8.61 | 15.83 |

The asymmetry is severe and is the substance of the result. Under perturbation, these models are not becoming uniformly noisy — they are shifting hard toward rejection. False acceptance stays comparatively contained (8.6 to 31.9 points) while false rejection climbs past 75 points in every case. Phi-4-Reasoning is the clearest instance: its perturbed T2 step-level accuracy (91.39%) is barely below its canonical figure (97.78%), while its perturbed T1 accuracy collapses to 14.72%. A verifier that rejects nearly everything will of course look excellent at catching genuine errors. The authors describe this behaviour as models treating the first unfamiliar transformation as an error — mistaking procedural variation for incorrect reasoning.

### Does any adaptation close the gap?

Partially, inconsistently, and with real trade-offs against canonical performance. The authors' own framing is that fine-tuning does not uniformly improve "mathematical ability"; it *shifts the decision boundary* between accepting valid procedural variation and rejecting suspicious-looking traces. The three models each have a different winner, which is itself the finding:

- **GPT-OSS 20B — GED-FT wins, and the canonical cost is visible.** Perturbed Q2 improves from 54.06% to 76.94% and Q3 from 24.07% to 58.98%; on valid T1 perturbations the gain is dramatic, Q2 from 24.44% to 94.72% and Q3 from 24.72% to 93.61%. But canonical performance pays for it: Q1 drops from 97.69% to 77.31%, Q2 from 98.24% to 89.63%, Q3 from 98.06% to 85.74%. This is the clearest single illustration of the trade-off the brief asks about.
- **Qwen3-14B — FT+TTC wins, and here there is no evident trade.** Perturbed Q3 rises from 14.35% to 81.67%, Q2 from 52.69% to 84.54%, Q1 from 71.67% to 78.24%, while canonical performance also improves over base (Q1 87.31%, Q2 93.70%, Q3 93.61%, against base 83.61 / 86.48 / 86.02). This is the one cell in the paper where the gap is substantially closed without an obvious canonical penalty. Notably, GED-FT *underperforms* for this model, which the authors take as showing that teacher-rationale distillation is not uniformly beneficial and that its usefulness depends on how well the explanation style matches the student's learned behaviour.
- **Phi-4-Reasoning — GED-FT wins decisively; plain FT degenerates.** GED-FT reaches 96.39% (Q1), 96.76% (Q2) and 93.70% (Q3) on perturbed traces, from a base of 67.87 / 63.43 / 19.81 — essentially closing the gap, at a modest canonical Q1 cost (96.48% to 89.07%) while canonical Q2 and Q3 actually improve. Plain FT, by contrast, over-accepts: the authors note it does well on T1 while failing on T2. The FT+TTC row makes the failure unmistakable — perturbed T1 accuracy of 100% alongside T2 and T3 accuracy of exactly 0.00% on both Q2 and Q3, with Q1 pinned at exactly 66.67%. That is the signature of a model that has collapsed into answering "valid, Q3 = -1" every time, which scores 100% on the third of the set that is genuinely valid and zero elsewhere, and 2/3 on Q1 because T1 and T3 both carry correct final answers. The authors' stated lesson is that valid and invalid traces must be balanced in training: high acceptance of correct examples is worthless if the verifier loses the ability to reject.

### Test-time compute can make things worse

The most counterintuitive result, and the authors treat it as a mechanism claim rather than a curiosity. Majority voting reduces variance only when errors are noisy; when a model applies a wrong heuristic *consistently*, voting reinforces it. On base models this is exactly what happens: for GPT-OSS 20B, TTC drops perturbed Q1 from 76.30% to 32.04% and Q2 from 54.06% to 31.11%. Qwen3-14B falls from 71.67% to 34.35% on perturbed Q1 and Phi-4-Reasoning from 67.87% to 25.00%. The damage extends into canonical T3 as well, where base+TTC Q1 falls from 96.67% to 58.33% (GPT-OSS 20B) and from 99.44% to 6.94% (Phi-4-Reasoning). The authors' summary is that more samples do not necessarily produce better verification; they can simply make an incorrect judgment more stable. TTC becomes useful only *after* suitable adaptation — as in the Qwen3-14B FT+TTC result — and should be regarded as a calibration tool rather than a substitute for learning trace-validity semantics.

### What the authors conclude about the LLM as accept/reject gate

Their conclusion is that evaluator robustness is a **distinct capability from final-answer accuracy** and must be measured separately from solver accuracy, even in a simple algebraic domain with exact ground truth. A model that grades canonical solutions well cannot be assumed to gate reliably, because it is partly calibrated to solution *form* rather than to local step validity. The consequence they draw is that in any setting where multiple valid procedures lead to the same result, a verifier that rewards only familiar paths will suppress correct but non-standard reasoning. They extend the concern to verifier-guided inference specifically: poor localization may cause the generator to revise the wrong part of its reasoning. Their closing position is that reliable process-level verification remains challenging, that adaptation can reduce the gap but its benefits are model dependent, that majority-vote TTC can amplify systematic mistakes, and that controlled process-level benchmarks are the tool for measuring this in domains where the reasoning path itself must be verified — they name automated software verification, legal reasoning, and clinical diagnostics.

## Open questions the paper itself raises

The authors are explicit about these, mostly in Section IV-D:

1. Whether the behaviour holds outside single-variable linear equations — they name inequalities, systems of equations, equations with branching conditions, multi-solution problems, proofs, and programs as untested.
2. Whether models learn **general trace validity** or merely adapt to the specific transformation templates they were trained on. They propose per-perturbation-family breakdowns and held-out perturbation tests as the way to settle this, and acknowledge that the current paper does not report them.
3. Whether the distillation gains survive a change of teacher, prompt design, or filtering policy, and whether larger verified rationale sets help.
4. Whether the single-run adaptation results are stable — they flag this as a reason to discount small differences between variants.
5. Whether the framework transfers to non-mathematical procedural domains: software debugging, scientific protocols, chemical synthesis plans, and similar workflows where intermediate operations matter and the final output is not sufficient.

## Appreciation

I want to keep two things apart here, because the paper's mechanism and its magnitudes deserve very different amounts of confidence.

### MECHANISM — the part I find well established

The mechanism the paper demonstrates is that **an LLM verifier's accept/reject decision is partly a function of the derivation's surface form rather than of its logical validity, and the resulting error is directional: it manifests as rejection, not as noise.** Several design choices make this a genuine demonstration rather than an assertion:

- The equation is held fixed while only the trace varies, so the manipulated variable is isolated. The model is not being asked to solve anything harder.
- Gold labels come from a deterministic exact-arithmetic checker under a stated solution-set semantics, not from human or model judgment. Label noise is therefore not a plausible alternative explanation for the T1 failures.
- The semantics honestly distinguishes strict equivalence from candidate-generating steps with discharged obligations, rather than waving at "equivalent variants."
- The T1/T2/T3 factorial separates the two error directions, so "the model got worse" can be resolved into "the model shifted toward rejecting." That resolution is what turns a benchmark result into a mechanism claim.
- The three-way Q1/Q2/Q3 split shows that the sub-tasks do not degrade together, and that Q1 is contaminated by Q2 in the T3 condition. Entanglement between outcome and process judgment is a specific, falsifiable claim, and the T3 construction is the right instrument for it.
- The TTC-amplification result has a clean mechanistic story — voting reduces variance but not bias, so it entrenches a systematic heuristic — and the data are consistent with it across all three models.
- The Phi-4-Reasoning FT+TTC row (T1 at 100%, T2 and T3 at exactly 0.00%, Q1 pinned at 66.67%) is a degenerate-collapse signature that the authors leave visible in the table rather than suppressing. Printing a result that reveals a training failure is a mark in the paper's favour.

### MAGNITUDE — the part I would hold loosely

The specific numbers should not travel far from this paper:

- The domain is `ax + b = cx + d`. A 75–85% false-rejection rate is a fact about linear-equation traces with six synthetic perturbation families, not a general property of LLM verifiers. The authors say this plainly and call the setting diagnostic.
- Adaptation results are single-run with no intervals. Every cross-condition comparison in the FT / GED-FT / TTC grid — including the three different "winners" for the three models — is exactly the kind of comparison that single-run results cannot securely support. The winner-varies-by-model finding is suggestive; I would not build on it.
- FT and GED-FT differ in training-set size by a factor of roughly seven (27,000 vs 4,000 samples). Where GED-FT beats FT, richer rationales and smaller-but-label-verified data are confounded.
- Perturbation and trace structure are confounded: the two obligation-generating families require an added substitution-and-verification tail, so those traces are longer and shaped differently. Without the per-family breakdown the authors defer to future work, we cannot tell how much of the false rejection is "unfamiliar transformation" versus "longer trace with a verification section attached."
- Only three open-weight models are tested, and they were selected after a screening pass. This is a defensible choice, disclosed, but it means the sample is neither random nor representative.
- Parse errors are counted as incorrect. This is a reasonable and clearly stated convention, but it folds JSON-formatting competence into the verification scores, and the paper does not report what fraction of failures were parse errors — which matters most for the models and conditions that score worst.

## How it could serve a harness-design effort / limitations / major concerns

**What is directly usable.**

The paper's most transferable contribution to anyone building a multi-step system is the argument that **the verifier must be evaluated as its own component, on its own axis, with both error directions measured separately.** A harness that uses a model to gate steps and validates that gate only by end-to-end task success will not see the failure documented here, because the gate's characteristic failure is to reject work that was correct — which shows up as retries, wasted budget, or a suppressed-but-valid path, not as a wrong final answer.

Three concrete design implications follow from the paper's own results:

1. **Do not treat a single accept/reject bit as the interface.** The paper's Q1/Q2/Q3 split shows the three judgments have wildly different reliability in the same model at the same time — Q3 near chance while Q1 is at 76%. A harness that collapses them into one verdict inherits the reliability of the weakest one it implicitly depends on. If the harness routes on *where* the error is, it is depending on the least reliable judgment.
2. **Localization quality bounds repair quality.** The authors make this point for verifier-guided inference specifically: poor localization sends the generator to revise the wrong part of its reasoning. A repair loop driven by a localizer running near chance will not converge, and it may actively damage correct steps.
3. **More sampling is not a safety margin.** The base-model TTC results are the sharpest practical warning in the paper. Majority voting over a systematically biased verifier makes the bias *more* stable, and the paper shows perturbed Q1 halving under TTC. A harness that adds self-consistency to a gate without first establishing that the gate's errors are noise rather than bias may be buying confidence in the wrong answer.

**Limitations and major concerns for anyone drawing on this.**

- *Scope is the dominant caveat.* Single-variable linear equations with unique rational solutions is about as far from a realistic agent sub-task as a procedural-verification setting can be while remaining procedural. The paper is a clean existence proof of the failure mode, not a measurement of its size anywhere that matters operationally.
- *Perturbations are synthetic and enumerated.* Six families, generated by an engine. Real alternative derivations — from another model, or from a person — are not drawn from this distribution, and the paper says so.
- *We cannot distinguish "learned trace validity" from "learned these six templates."* This is the paper's own second open question, and it is the one that most limits the usefulness of the adaptation results. If GED-FT taught Phi-4-Reasoning to recognize squaring-with-verification rather than to reason about solution sets, the 93.70% perturbed localization figure will not survive a seventh perturbation family. Held-out-family results would settle this and are absent.
- *The training recipe is not a transferable prescription.* Different models had different winners; the paper's honest summary is that perturbation-oriented supervision must be "calibrated carefully," which is not something a harness designer can act on directly.
- *A subtle risk in the interpretation.* Because false acceptance stays relatively low while false rejection explodes, a naive read of aggregate Q2 accuracy under-states how broken the verifier is — and, worse, a verifier that has degenerated toward rejection will look *good* on any evaluation set dominated by genuinely-invalid traces. Any harness-side verifier evaluation must therefore hold valid non-canonical work in the test set deliberately, or it will certify a rejector as a verifier. This is the paper's most practically important implication and it is somewhat buried in the stratified tables rather than stated as a headline.
- *Relation to the Subject.* The paper does not study task decomposition, and I am not going to stretch it into one. What it does contain is a decomposition of one objective (judge this trace) into three sub-objectives with a measured, unequal reliability profile and a demonstrated dependency between them — Q1's accuracy on T3 is contaminated by the model's Q2-style suspicion. That is a small but concrete data point about the recombination cost of splitting a judgment into parts: the parts were not independent, and the split revealed a failure that the aggregate had hidden.

## Five citations worth chasing next

1. **[11] X. Li, X. Li, S. Hu, Y. Guo, W. Zhang (2025), "VerifyBench: A Systematic Benchmark for Evaluating Reasoning Verifiers Across Domains," arXiv:2507.09884.** The closest neighbour in intent — verifiers as the object of evaluation — but across domains rather than one narrow one. It is the natural check on whether this paper's failure mode generalizes.
2. **[9] R. Kamoi, Y. Zhang, N. Zhang, S. S. D. Sarkar, R. Zhang (2025), "Generalizable Process Reward Models via Formally Verified Training Data," arXiv:2505.15960.** Attacks the same underlying problem — trustworthy step labels — from the training side rather than the evaluation side, and shares this paper's instinct that formal verification, not human annotation, should supply process labels.
3. **[2] K. Chang et al. (2025), "Step-Level Verifier-Guided Hybrid Test-Time Scaling for Large Language Models," EMNLP 2025, pp. 18462–18477.** Directly relevant to the harness question: it uses a step-level verifier to steer inference, which is precisely the deployment this paper's localization results call into question. Worth reading against the TTC-amplification finding.
4. **[12] H. Lightman et al. (2024), "Let's Verify Step by Step," ICLR.** The reference point for process supervision over outcome supervision, and the ancestor of the process/outcome distinction this paper is operationalizing. Cited in both the introduction and the related-work section here.
5. **[19] P. Wang et al. (2024), "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations," ACL 2024, pp. 9426–9439.** The process-reward-model line that this paper positions itself as complementing; useful for seeing what a trained step verifier looks like when the labels come from automatic annotation rather than an exact checker.

*(Runner-up, if a sixth were allowed: [8] K. Huang et al., "MATH-Perturb: Benchmarking LLMs' Math Reasoning Abilities against Hard Perturbations," arXiv:2502.06453 — the solver-side analogue of this paper's perturbation strategy.)*
