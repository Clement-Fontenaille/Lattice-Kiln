# Review: Decomposed Prompting Does Not Fix Knowledge Gaps, But Helps Models Say "I Don't Know"

## Density

**Density: HIGH** — Almost every section is load-bearing on the Subject: the paper is built around a controlled comparison of three task-equivalent decomposition regimes, it reports where decomposition's accuracy benefit ends and why, and it repurposes the split-vs-not contrast into a measurement instrument; the only thinner parts are the related-work survey and some appendix duplication of main-table numbers.

## Name, keywords, year, venue

- **Full title.** *Decomposed Prompting Does Not Fix Knowledge Gaps, But Helps Models Say "I Don't Know"*
- **Authors.** Dhruv Madhwal, Lyuxin David Zhang (equal contribution); Dan Roth, Tomer Wolfson, Vivek Gupta (equal advising).
- **Year.** arXiv v1 dated 2026-02-04; v2 `arXiv:2602.04853v2 [cs.CL]`, 2026-07-06.
- **Venue (confirmed).** Findings of the Association for Computational Linguistics: ACL 2026. Confirmed from the arXiv record's `citation_doi` field: `10.18653/v1/2026.findings-acl.1829` — an ACL Anthology DOI in the `2026.findings-acl` volume. Peer-reviewed; the paper's Acknowledgements thank "the anonymous reviewers," consistent with that.
- **Artifacts.** Code, data and prompts stated as available at `https://github.com/dhruvmadhwal/disagreement-based-abstention`.
- **My keywords** (not the paper's): decomposition-as-control-variable; execution-style ablation; plan/execution decoupling; cross-regime consistency; logical invariance failure; abstention; error detection; closed-book multi-hop QA; scale-dependent scaffolding; reliability multiplier; training-free uncertainty; inference-cost multiplier.

## Approach — what they did

The paper takes task decomposition, normally used as an *intervention* to raise accuracy, and turns it into an *experimental control*, in order to ask a different question: what does the difference between decomposed and undecomposed execution tell you about the model?

The design has two halves.

**Half one — the three-regime comparison.** For every question they fix a single gold-standard decomposition, then execute that same plan under three prompting regimes that are semantically equivalent by construction:

- **Direct** — one call, no explicit intermediate structure; decomposition, if any, happens implicitly inside the model.
- **Assistive** — the model is handed the full sequence of sub-questions as fixed context and generates all intermediate answers plus the final answer in a single call. Mirrors single-prompt, plan-up-front approaches (they cite Press et al. 2023, Radhakrishnan et al. 2023, Wu et al. 2024).
- **Incremental** — the decomposition is executed line by line over separate model calls, one sub-question at a time, with earlier answers substituted into later sub-question templates (`"In what city was [answer_1] born?"` → `"In what city was Albert Einstein born?"`). Notably, each hop is issued in isolation: **no access to the original top-level question and no access to past or future steps**. Mirrors least-to-most / step-wise execution (Zhou et al. 2023, Khot et al. 2023).

Plans are written in a decomposition DSL (following Wolfson et al. 2026) specifying variables, answer types, and sub-questions with placeholders referring to earlier steps. Plans are produced by a two-stage pipeline — translating existing step annotations into DSL where benchmarks provide them, otherwise synthesizing DSL programs with Gemini-2.5-Flash — and then **every decomposition is manually verified**, explicitly so that planning error is eliminated as a confounder. The stated payoff: if all sub-questions are answered correctly the final answer *must* equal the answer to the original question, so any Direct-vs-decomposed disagreement is attributable to knowledge or execution, never to a bad plan. The paper thus isolates the *execution and recombination* axes of decomposition by holding the *splitting* axis fixed and correct.

They measure two things per question: **accuracy** (against gold) and **consistency** (semantic agreement between the Direct answer and each decomposed regime's final answer, anchored on Direct, defined independently of correctness).

**Half two — the abstention method.** From the observed coupling between cross-regime agreement and correctness they build **Disagreement-Based Abstention (DBA)**: prompt the model once Direct and once through a task-equivalent decomposition; if the two final answers are not semantically equivalent, emit "I don't know." Variants **DBA-A** (Assistive) and **DBA-I** (Incremental). Training-free, retrieval-free, and grounded in *exhibited behavior* rather than self-reported confidence. They also define **Ensemble-A / Ensemble-I**, abstaining if *either* DBA or the AYS baseline abstains.

## Models targeted and benchmarks used

**Nine instruction-tuned LLMs across four size tiers**, all evaluated in released instruction-tuned form with fixed decoding (greedy for open models; GPT-5.1 uses API default with reasoning effort "medium", since temperature is not exposed):

- ~8B: Mistral-7B-Instruct-v0.3, Llama-3.1-8B-Instruct, Qwen3-8B
- 32B: Qwen3-32B
- ≥70B: Llama-3.3-70B-Instruct, Qwen2.5-72B-Instruct
- Frontier / closed: GPT-5.1, Gemini-2.5-Pro, Gemini-2.5-Flash

**Six multi-hop QA benchmarks**, closed-book throughout: Bamboogle, FRAMES, MuSiQue, CRAG, HotpotQA, Mintaka. Questions are filtered for ambiguity, genuine multi-hop complexity, temporal independence, and semantic clarity, yielding **1,433 verified instances** (filtering statistics and splits in Appendix B).

Gemini-2.5-Flash additionally serves as the **LLM-as-judge** for both correctness and semantic-equivalence decisions, and as the synthesizer of DSL decompositions where benchmarks lacked annotations — so it appears three times over: as subject, as judge, and as plan author.

## Author incentive

Affiliations: Madhwal and Gupta at **Arizona State University** (Complex Data Analysis and Reasoning Lab, School of Computing and Augmented Intelligence); Zhang, Roth and Wolfson at the **University of Pennsylvania** (Cognitive Computation Group); Roth additionally listed with **Oracle AI**. Funding: **ONR Contract N00014-23-1-2364**, plus institutional compute from both universities.

Two stakes, neither hidden. First, this is a group with a standing position in the decomposition literature — Wolfson is an author of QDMR/BREAK, which the paper cites as decomposition's formalization, and the DSL here follows Wolfson et al. 2026. A paper headlined "decomposition does not fix knowledge gaps" is therefore not self-serving in the obvious direction; it partially deflates the authors' own prior line, then re-justifies it in a new role (auditing rather than answering). Second, they propose a named method (DBA) they want adopted, so the abstention half carries the usual incentive to beat baselines — and the baseline set is small (three, one of which is relegated to an appendix). The Oracle AI affiliation gives a product-adjacent stake in deployable training-free reliability tooling, but no Oracle model or product is evaluated or promoted.

## Measurement methodology (brushed)

**Dependent variables.** Two in the first half — accuracy (LLM-judged match to gold) and cross-regime consistency (LLM-judged semantic equivalence between Direct and a decomposed regime, explicitly independent of correctness). Four in the second half — precision, recall, F1 and AUROC of an abstention policy treated as a *binary error detector*, with the positive class being "the Direct answer is incorrect."

**The framing choice that carries the most weight.** In the abstention evaluation the Direct answer is the claim-of-interest; the decomposed executions are only diagnostic signals used to accept or reject it. So DBA is never scored on whether decomposition *produced a better answer* — only on whether the split-vs-not contrast *predicted a bad one*. The paper justifies this by alignment with prior abstention work, which likewise targets the direct answer.

**What is controlled.** Unusually much, and this is the paper's strongest methodological feature:

- The *plan* is held fixed and gold across all three regimes, hand-verified per instance, so decomposition quality cannot confound the regime comparison.
- The DSL enforces declared answer types, keeping intermediate outputs in formats consumable by later steps — recombination noise reduced by construction.
- Semantic equivalence of the decomposition to the original question is guaranteed by design, so a correct execution *must* reproduce the original answer.
- Same instruction and same decoding settings across regimes; greedy decoding wherever exposed, to suppress sampling variance. (For GPT-5.1 temperature is not exposed, so "reasoning effort: medium" stands in — an uncontrolled asymmetry the paper flags but cannot remove.)
- Data filtered for temporal stability, semantic clarity, and DSL validity; a reference date is pinned in the prompt.

**N.** 1,433 questions after filtering from 1,488 initial (3.7% removed): Bamboogle 123, CRAG 163 (multi-hop, temporally stable subset), FRAMES 293, HotpotQA 274, Mintaka 298, MuSiQue 282. Multiply by 9 models by 3 regimes for the main grid. Per-cell N is small in places — Bamboogle at 123 items, split further by correctness, is thin, and several headline effects (the 34.0x reliability multiplier for Gemini-Pro on Bamboogle) sit on top of very few inconsistent-and-correct cases.

**How significance is treated.** Lightly. There are **no confidence intervals, no significance tests, no error bars, and no multiple-run variance** anywhere in the paper — a consequence of greedy decoding making each cell a single deterministic run. The statistical apparatus is (a) Pearson correlations between accuracy and consistency across (model, dataset) points, reported as "reaching up to" a value; and (b) the **Reliability Multiplier (RM)**, a ratio of (consistent and correct) to (inconsistent and correct) Direct answers. To their credit the authors state RM's own fragility explicitly: for small models correctness is sparse, so RM is "statistically fragile" and shows near-one or inverted values — they read those cells as a floor effect rather than as evidence.

**Judging.** A single LLM judge (Gemini-2.5-Flash, greedy, four few-shot examples per dataset) decides both correctness and semantic equivalence, under a fixed rubric that normalizes aliases/units/abbreviations, enforces numeric tolerance and exact date matching, and penalizes explicit contradictions. **No human agreement study for the judge is reported.** Human verification is spent elsewhere: on all the decompositions, on the data filtering, on 100 inconsistency examples for the failure-mode taxonomy, and on 120 model-generated decompositions in the D.4 feasibility audit.

**Cost accounting.** Measured, not estimated: calls and input/output tokens averaged over all models and datasets, normalized to Direct = 1.00 (Table 4 / Table 10).

## Key findings, with the authors' own reading

**1. Decomposition's accuracy benefit is real, large, and confined to non-frontier models.** For ≤70B models, a *correct, gold* decomposition delivers persistent double-digit gains: Qwen-72B on Bamboogle 31.7 → 58.5 (Assistive) / 61.0 (Incremental); Llama-70B on Bamboogle 45.5 → 72.4; Qwen-8B on Bamboogle 12.2 → 37.4. For GPT-5.1 and the Gemini-2.5 pair the same intervention delivers near-parity or a loss: Gemini-Flash on Bamboogle −8.1 Assistive; GPT-5.1 −7.8 Incremental on MuSiQue and −6.5 on FRAMES; most frontier deltas sit within ±1-5 points, skewing negative for Incremental. Authors' reading: a **ceiling effect** — frontier models have internalized the reasoning chains, so explicit scaffolding no longer adds and may interfere.

**2. Incremental is generally the worse of the two decomposed regimes at frontier scale.** Negative deltas are systematically larger for Incremental than Assistive on GPT-5.1 and Gemini-Pro. The paper does not dwell on this, but its own setup supplies the candidate mechanism: Incremental hops are issued in isolation, with no access to the top-level question or sibling steps, so context the model could have exploited is deliberately withheld.

**3. Semantically equivalent plans do not produce equivalent answers — even at the top.** Averaged across all models, cross-regime consistency is only **0.421 (Assistive) / 0.418 (Incremental)**; per-dataset averages range from MuSiQue 0.290/0.273 and FRAMES 0.334/0.295 up to Mintaka 0.573/0.562. Frontier models are much better but not stable: GPT-5.1 spans 93.6% (Mintaka) down to 59.7% (MuSiQue, Incremental); Gemini-Pro similar. The authors name this "a fundamental failure of logical invariance": under a plan guaranteed equivalent to the question, the answer should not depend on execution style, and it does.

**4. Agreement across regimes tracks correctness, increasingly so with scale.** Accuracy and consistency correlate strongly across (model, dataset) points, for both Assistive (Fig. 2) and Incremental (Fig. 4). The Reliability Multiplier rises with scale: near-one or inverted at ~8B (floor effect, and they say so), roughly 2-4x at 32B-70B, and very large at frontier scale (Gemini-Pro 34.0x on Bamboogle, 50.2x on Mintaka; GPT-5.1 42.0x on Mintaka). The paper's whole framing follows: decomposition's marginal value shifts **from intervention to inspection** — from expanding what can be answered to auditing confidence in what is known.

**5. DBA beats self-reported-confidence baselines, and the mechanism is recall.** DBA beats AYS on F1 in 17 of 18 reported model-dataset pairs. The gain is not indiscriminate abstention — AUROC stays above chance throughout (mid-0.6 to low-0.9) — but comes from catching errors self-verification misses: AYS is overconfident precisely when the model hallucinates, so its recall collapses. On Bamboogle with Llama-3.3-70B, recall goes 37 → 90. Typical open-model gains are +30 to +50 recall points.

**6. Self-consistency is a high-precision, catastrophically low-recall detector by comparison.** Under majority vote (7 samples, threshold 4), self-consistency reaches precision 1.00 on several open models but recall 0.02-0.14 — Llama-3.3-70B on Bamboogle: P 1.00, R 0.02, F1 0.03, versus DBA-A F1 0.92. GPT-5.1 on MuSiQue: SC recall 0.05 versus DBA-A 0.59. Even under a fairer continuous-score AUROC protocol (support count as graded score, F1-optimal threshold swept), the optimal threshold is consistently 6-or-7 out of 7 and DBA-A still wins F1 on three of four models — Gemini-2.5-Pro the exception (SC 0.67 F1 / 0.76 AUROC vs DBA-A 0.61 / 0.73). Authors' reading: varying the *prompting regime* is a more informative perturbation than varying *decoding*.

**7. The headline caveat is the paper's own title.** Manual analysis of 100 inconsistent cases yields a three-way taxonomy — Helped (Direct wrong, Assistive right), Hurt (Direct right, Assistive wrong), Both wrong. For frontier models the split is roughly **15.3 / 17.6 / 67.1** (GPT-5.1) and **16.7 / 16.7 / 66.5** (Gemini-Pro). So ~67% of disagreements are *knowledge gaps neither regime can close*, and Helped and Hurt are near-symmetric — decomposition does not net-fix errors at frontier scale, it makes them visible. That is exactly the title's claim.

**8. Two mechanisms behind the disagreements, in the authors' framing.** *Shortcut hypothesis*: when decomposition hurts, the correct Direct answer came from a reasoning shortcut, and forcing execution of the verified plan exposes that the model lacks the intermediate facts. *Scaffolding hypothesis*: when decomposition helps, the model holds the atomic facts but lacks the executive function to organize them zero-shot. Their qualitative examples are sharp on both: Ex. 4 (Yosemite → tallest building in California) shows the split-out hop retrieving stale intermediate knowledge (Salesforce Tower) that Direct got right; Ex. 5 shows a first-hop entity error (wrong cover artist) propagating into a perfectly-executed but wrong second hop.

**9. Cost.** DBA-A: 4 calls, 5.64x Direct's total tokens. DBA-I: 6.4 calls, 5.89x. Self-consistency: 8 calls, 6.51x. AYS: 2 calls, 1.26x. IC-IDK: 1 call, 1.16x. Almost all of DBA's overhead is *input* tokens (6.61x input vs 2.53x output for DBA-A) — the DSL plan and few-shot examples, not generated text. DBA-I's many small isolated hops keep its token bill close to DBA-A's despite 60% more calls.

**10. The gold-plan requirement is softer than the main setup implies.** Auxiliary study (D.4): Qwen2.5-72B-Instruct generating its own decompositions yields 103/120 manually-audited valid decompositions (85.8%), and 0.841 P / 0.869 R / 0.854 F1 on hop-level alignment against gold with an average hop ratio of 1.081. They decline to swap these into the main experiments, on the stated grounds that the main study needs fixed high-quality plans.

## Open questions the paper itself raises

Stated in the Limitations section, in its own framing:

1. **DBA is blind to consistent errors.** It can only detect errors that surface as cross-regime disagreement. When a model reproduces the same wrong answer under Direct, Assistive and Incremental, DBA reads that as stable and gives no corrective signal. The paper localizes this empirically: on CRAG, frontier models produce "stable but incorrect predictions across regimes," and DBA's recall drops there while AYS stays competitive.
2. **DBA depends on high-quality decompositions.** The main experiments assume access to manually verified or strong-teacher-model plans, which makes the method "less self-contained," especially for weaker models that struggle to generate good multi-hop decompositions. They soften this with the D.4 feasibility analysis (85.8% valid at 70B-class), but explicitly do not claim it for weaker models.
3. **DBA costs extra compute and latency** — at minimum one additional decomposed execution, and for Incremental one call per hop; the cheaper baselines run in a single regime but detect less.

Beyond the numbered limitations, the paper leaves open (and gestures at rather than resolves):

- **Whether disagreement can drive correction, not just abstention.** They title a Discussion subsection "Potential for Answer Correction" and then close it down with the 67%-Both statistic: for frontier models the disagreement signal marks reasoning shortcuts well but cannot repair parametric knowledge gaps. What to do with the ~33% where one regime *is* right is left unanswered — they do not attempt an arbitration policy.
- **Why frontier models fail logical invariance at all.** They document that outputs "strongly depend on the question decomposition rather than reflecting a consistent reasoning process over semantically equivalent plans," and offer the shortcut/scaffolding pair as descriptive hypotheses, but no mechanistic account.
- **Whether the ensemble result generalizes.** Ensembling AYS with DBA is shown to help where their failure modes are complementary (GPT-5.1 on CRAG), but the union rule is a heuristic and no principled combination is developed.
- **The abstention/utility trade-off is unpriced.** Everything is scored as error *detection*; the cost of abstaining on a question the system could have answered is never converted into a user-facing utility.

## Appreciation — mechanism separate from magnitude

### What transfers as an argument (MECHANISM)

**M1. Decomposition can be varied while holding semantics fixed, and that difference is itself a measurement.** This is the paper's real contribution and it is method-portable, not benchmark-bound. The insight that two task-equivalent execution styles over an identical, verified plan constitute a *perturbation pair* — and that the model's failure to be invariant under it is diagnostic — does not depend on multi-hop QA. It generalizes to any setting where you can construct a provably equivalent alternative route to the same answer.

**M2. The plan/execution decoupling is a clean experimental idea worth stealing.** By fixing gold, hand-verified plans, the paper cuts the confound that muddies most decomposition results: you normally cannot tell whether a decomposed pipeline lost because splitting is bad or because the splitter was bad. Here the splitter is correct by construction, so every remaining loss is attributable to execution or knowledge. That any loss remains at all is a strong result *because* of this control.

**M3. Decomposition's value has different sources at different capability levels, and can invert.** That the same intervention is worth +25 points at 8B-72B and −8 points at frontier scale is a mechanism claim about *where the scaffold is doing work*, not a number about Bamboogle. The shortcut hypothesis (splitting forces a route the model cannot actually walk, exposing that its shortcut answer had no supporting intermediate knowledge) is a genuine mechanism, and Ex. 4 and Ex. 5 illustrate it concretely.

**M4. Isolating a sub-task removes context that was load-bearing.** The Incremental regime deliberately denies each hop the parent question and its siblings, and Incremental is consistently the worse regime at frontier scale. The paper does not push this, but the pattern is a mechanism-level warning about aggressive context isolation in step-wise execution.

**M5. Behavioral disagreement beats self-report, and cross-regime perturbation beats decoding perturbation.** The precision/recall shape of the comparison — self-report and sampling both fail by *missing* errors, not by false alarms — is a robust qualitative claim, and it has an intuitive basis the paper states: factual knowledge is stable, hallucination is stochastic, and re-sampling the same prompt re-samples the same attractor while re-routing the task does not.

**M6. Error visibility and error correction are separable goals.** The 67%-Both statistic is the paper's most honest moment. It establishes that a decomposition-based check can be an excellent *detector* while being nearly useless as a *fixer* — a distinction routinely blurred in agentic-systems claims.

### What is a number valid only inside this setup (MAGNITUDE)

**Everything with a decimal point.** Specifically:

- **The consistency rates (0.42 average; 59.7-93.6% for GPT-5.1)** are a joint product of the judge (a single Gemini-2.5-Flash instance with a particular rubric on aliases, numeric tolerance and date exactness), the answer-format instructions ("prefer 1-3 words", semicolon-separated lists), and these six datasets. Ex. 1 in their own appendix has Direct 1971-03-31 vs Assistive 1971-03-30 counted as a disagreement — a one-day date miss. A different tolerance setting moves these numbers materially.
- **The Reliability Multiplier values (34.0x, 50.2x)** are ratios whose denominators are tiny at frontier scale — the count of *inconsistent and correct* Direct answers on a 123-item or 298-item set. These are the most fragile numbers in the paper. The authors correctly disown the small-model end of the same statistic for exactly this reason, but do not apply the same skepticism to the large end, where the denominator problem is worse.
- **The F1/AUROC tables** are strongly base-rate dependent, as they say themselves: error rates swing from ~10% to ~90% across models on the same dataset, so F1 comparisons across model rows are not meaningful; only within-cell method comparisons are. AUROC is the number to read, and the AUROC margins are considerably more modest than the F1 margins (GPT-5.1 CRAG: DBA-A 0.67 AUROC vs AYS 0.74 — DBA *loses* there).
- **The 5.64x/5.89x token multipliers** are averaged over a specific prompt design, with 6.61x of that in *input* tokens driven by the DSL plan and per-dataset few-shot examples. A tighter prompt or cached plan changes this substantially; and the numbers exclude the LLM-judge call that DBA needs at inference time to decide semantic equivalence, which is a real deployment cost the table does not carry.
- **The 85.8% decomposition validity** comes from 120 hand-audited items from one model, judged by the authors on a permissive criterion ("consistent with the original question and preserves the intended multi-hop structure"). It supports "plausible," not "sufficient."

### Reservations

- **The judge is load-bearing and unaudited.** Gemini-2.5-Flash decides correctness *and* consistency, i.e. both dependent variables of the first half and the abstention trigger of the second. No human-agreement number is given for it. Also Gemini-2.5-Flash and Gemini-2.5-Pro are themselves evaluated subjects — a judge in the same family as two of the nine subjects, deciding their answers correct or not, with no discussion of that.
- **No variance whatsoever.** Greedy decoding makes each cell a single sample and the paper leans on that to skip error bars. But greedy determinism is not the same as statistical stability — the sampling variance across *questions* remains, and none of it is quantified. Deltas of ±1-5 points in the frontier row of Table 1, which carry the central "gains plateau" claim, are reported without any indication of whether they are distinguishable from noise. The claim survives on the sign pattern being broadly consistent across 6 datasets and 3 models, which is suggestive, not tested.
- **"Frontier" is confounded with "closed."** All three frontier models are proprietary API models; all six non-frontier ones are open weights. Scale, training recipe, RLHF, inference-time reasoning (GPT-5.1's "medium reasoning effort" is a different computation from greedy 8B decoding) and vendor are all varying together. The paper's scale story reads plausibly but the design cannot separate scale from any of these.
- **Direct is privileged in a way that shapes every abstention number.** By construction the decomposed regimes only ever get to *veto*, never to answer. In the ~15% of frontier disagreements labeled Helped, the decomposed answer was right and Direct wrong, and DBA throws both away and says IDK. The paper is transparent about the choice and its rationale, but it means the abstention results say nothing about the natural alternative policy — prefer the decomposed answer — that its own data could have evaluated.
- **The regime taxonomy is narrow relative to the Subject.** Only two decomposition shapes are studied, both flat, both single-level, both with an externally supplied plan. There is no recursion, no depth beyond the DSL's hop count, no runtime decision to split, no budget, and no sub-agent hierarchy.

## How it could serve a harness-design effort — limitations and major concerns

Stemming the discussion rather than resolving it:

**A cheap invariance check falls out of this directly.** The transferable design pattern is: for a task with a verifiably equivalent alternative decomposition, run both routes and treat disagreement as a hard veto that routes to abstention, escalation, or a human. Its appeal for a harness is that it needs no training, no retrieval, no confidence head, and no privileged access to logits — it works over an API boundary, on any model, using only outputs. The open question it leaves is what the harness does *with* the veto, since the paper stops at "say IDK."

**But the price is high and understated for anything larger than QA.** 4-6.4 calls and ~5.6-5.9x tokens for one binary reliability bit, on questions answerable in a few words. A harness would have to decide where that multiplier is worth paying — the paper's own ensemble result hints that the cheap check (AYS, 1.26x) and the expensive one (DBA, 5.64x) catch different failures, which suggests a tiered policy rather than running DBA everywhere. Nothing in the paper addresses selective triggering, and the token cost excludes the equivalence-judging call.

**The "does decomposition pay?" question is answered only under a very favorable setup — and still comes out negative at frontier scale.** This is the finding most worth carrying, with its scope attached. These decompositions were *gold, hand-verified, type-annotated, and semantically guaranteed equivalent* — a best case a live harness will not have. Under that best case, frontier models still lost accuracy on most datasets under Incremental execution. The obvious inference for a harness — that splitting a task for a capable model is not free and may be actively negative — is well supported here for *closed-book factual multi-hop QA*, which is precisely the task family where the sub-tasks are knowledge lookups that decomposition cannot make the model know. Whether it extends to task families where sub-tasks differ *qualitatively* from the parent — long-horizon work, tool use, code, retrieval-backed pipelines, tasks exceeding a context window — is entirely outside what this paper measured, and the closed-book constraint is doing a lot of work in the result.

**Context isolation is the specific design choice a harness should scrutinize.** Incremental hops here carry no parent question and no sibling history. That is an unusually severe isolation policy, and Incremental underperforms Assistive at frontier scale. A harness that passes richer context down to sub-agents may not inherit this penalty — but equally, Assistive's advantage may come precisely from *not* isolating, which would argue against the deep-isolation designs common in sub-agent architectures. The paper does not isolate this variable, so this remains a hypothesis its data merely gestures at.

**The invariance failure is the more unsettling result for orchestration.** Independent of DBA, the finding that ~58% of (model, dataset) pairs disagree across semantically-equivalent execution routes — and that even the best model drops to 59.7% agreement on the hardest set — says that a harness composing sub-results cannot assume the composed answer equals the direct answer. Whichever route a pipeline picks is, in a substantial minority of cases, an arbitrary choice with a different outcome. That has implications for reproducibility and for any evaluation that fixes one pipeline shape and reports it as the model's capability.

**Concerns that limit how far any of this can be pushed.** The measurement instrument is a single unaudited LLM judge; no uncertainty is quantified anywhere; frontier is confounded with proprietary; the decomposition space explored is two flat variants with externally supplied plans, which is a narrow slice of the Subject's axes (nothing on what triggers a split, nothing on depth, nothing on recursion or hierarchy); and the whole result is closed-book by design, which removes the single most common justification for decomposition in deployed systems — that sub-tasks can each be grounded against retrieved evidence. A harness reading this paper gets a strong warning about decomposition-as-accuracy-intervention and a genuinely novel primitive for decomposition-as-instrument, but should not read the null result on decomposition as covering decomposition in general.

## Five citations worth chasing next

1. **Wolfson et al. (2020), "Break It Down: A Question Understanding Benchmark" (QDMR / BREAK)** — the formalization of decomposition as a standalone question-understanding problem, and the ancestor of the DSL used here. The place to go for what a decomposition *is*, independent of any model.
2. **Khot et al. (2023), "Decomposed Prompting: A Modular Approach for Solving Complex Tasks"** — the canonical modular/step-wise decomposition method this paper's Incremental regime instantiates; the primary source for the intervention framing that this paper pushes back on.
3. **Zhou et al. (2023), least-to-most prompting** — the other progenitor of stepwise sub-question execution, and the natural comparison point for how much context each hop should carry.
4. **Cohen et al. (2023), "LM vs LM: Detecting Factual Errors via Cross Examination" (EMNLP 2023)** — the source of both AYS and IC-IDK baselines and of the multi-agent cross-examination idea; the closest prior art to DBA's disagreement-as-signal logic, and the paper to read to judge how novel DBA actually is.
5. **Radhakrishnan et al. (2023), on decomposition and reasoning faithfulness** — cited here as enforcing structural constraints to improve faithfulness; directly relevant to whether forcing execution of a verified plan changes what the model is actually doing rather than what it reports doing.

*(Runners-up, if the trail extends: Han and Gardent (2025) on compact models generating and ranking synthetic decompositions, which bears on the gold-plan dependency; Wang et al. (2023) self-consistency, as the perturbation baseline DBA is positioned against; and Sinha et al. (2025), cited twice as the framing for attributing disagreement to execution or parametric knowledge rather than plan error.)*
