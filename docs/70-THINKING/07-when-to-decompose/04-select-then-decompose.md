# Select-Then-Decompose — review

*Source read: arXiv:2510.17922v1 (HTML full text, 20 Oct 2025), the EMNLP 2025 main-conference version.*

## Density

**Density: HIGH.** Survey, measurement, and method in one, with token and API cost promoted to a co-equal dependent variable. The closest paper in the set to the decide-to-split question. Magnitude caveats are real (single base model, single-run headline numbers), but the mechanism content is dense and directly reusable.

## Name, keywords, year, venue

**Name.** Liu, Liu, Wang, Wang, Wu, Xiang, He — *Select-Then-Decompose: From Empirical Analysis to Adaptive Selection Strategy for Task Decomposition in Large Language Models.*

**Year / venue.** 2025. EMNLP 2025 Main Conference (accepted as **Oral**), DOI 10.18653/v1/2025.emnlp-main.278. Preprint arXiv:2510.17922v1, 20 Oct 2025. Code at `github.com/summervvind/Select-Then-Decompose`.

**Keywords (mine, not the paper's).** Decomposition-strategy selection; router-over-prompting-strategies; performance–cost Pareto; token accounting as a first-class dependent variable; taxonomy of decomposition; verifier-triggered escalation; decomposition model vs. execution model asymmetry; strategy–task matching; prompt-level (not tool-level) decomposition.

**One-line thesis.** No single task-decomposition approach wins across tasks and all of them are priced very differently, so the right unit of design is a *meta-level chooser* — an LLM that picks a decomposition approach per question and escalates to a costlier one only when a verifier says the answer is weak.

## Approach

The paper is two papers stapled together, deliberately: a survey-plus-measurement half, and a method half derived from it.

**Half one — taxonomy and empirical analysis (Secs. 2–3).** They organise existing decomposition work along six binary axes:

1. **Decomposition-first vs. interleaved** — whole plan up front, or one subtask at a time conditioned on the last result.
2. **Implicit vs. explicit** — decomposition and execution folded into a single LLM call, vs. separate calls per stage.
3. **DAG vs. linear** — parallelisable dependency graph vs. a chain where each subtask's output feeds the next.
4. **Code vs. text** — subtasks expressed as Python/JSON structures vs. natural language.
5. **Limited vs. unlimited subtask selection range** — choose from a predefined candidate set vs. generate subtasks freely.
6. **Tool-augmented vs. pure LLM** — external interpreters/models/robots in execution, or not.

They then explicitly *scope out* axes 4–6, arguing each has one branch that is domain-bound (code format suits robotics and math; limited-range needs a predefined candidate set), and that they want general-purpose scenarios. The study therefore lives entirely in axes 1–3, with five representative approaches placed on them plus a no-decomposition control:

| | seq. | calls | topology |
|---|---|---|---|
| IO (control) | — | — | — |
| CoT | interleaved | implicit | linear |
| P&S (Plan-and-Solve) | decomposition-first | implicit | linear |
| ReAct | interleaved | explicit | linear |
| P&E (Plan-and-Execute / PEARL) | decomposition-first | explicit | linear |
| P&E (DAG) | decomposition-first | explicit | DAG |

Note that all six baselines are *pure-prompting* variants: ReAct here has no tool and, the authors concede, no code-execution component.

Three analyses follow: (3.1) performance **and** token/API cost of all six on five benchmarks; (3.2) whether the best approach tracks task type, cross-checked on a single subjective benchmark to control for metric heterogeneity; (3.3) what happens when you vary the *decomposition* model and the *execution* model independently, in scale and in reasoning-tunedness. Sec. 3.4 condenses this into two "practical principles": match approach to task character (logical rigor / divergence / iterativity), and — for explicit approaches — spend your model budget on the executor, leaving a merely instruction-following model to do the decomposing.

**Half two — the Select-Then-Decompose (S&D) strategy (Sec. 4).** A closed loop of three modules over the same six approaches:

- **Selection.** One LLM call with a fixed prompt that describes the six candidate approaches and asks the model to characterise the task on three axes (logic / iterative / divergent), returning `<think>` reasoning plus `<answer>` method name. The prompt contains no dataset- or task-specific information.
- **Execution.** Runs the chosen approach's own algorithm on the question, producing a candidate solution.
- **Validation.** A second LLM call scores the candidate's confidence in [0,1] given only the question and the solution. If `C >= T` (default T = 0.7) it is accepted. Otherwise a **staged escalation** fires: the next attempt draws uniformly at random from the next group in the fixed order `{IO}` → implicit `{CoT, P&S}` → explicit `{ReAct, P&E, P&E(DAG)}`, up to K = 3 switching iterations, returning ∅ if nothing passes.

Two things are worth naming precisely. First, the escalation ladder starts at IO — i.e. the first fallback after a low-confidence answer is *less* decomposition, not more, and only the third rung reaches the explicit approaches. Second, within a group the choice is random, not selected — the intelligence is concentrated in the k=0 selection call and in the verifier's accept/reject, not in the recovery path.

## Models targeted and benchmarks / datasets

**Models.**

- **GPT-4o-mini** is the base model for essentially everything: the Sec. 3.1 six-approach comparison, the MT-bench study, and all of the S&D experiments (selection, execution, and validation modules alike). Temperature 0, seed fixed at 42 via the OpenAI `seed` beta parameter.
- **Qwen2.5-1.5B / 7B / 14B-instruct** for the model-scale study (Sec. 3.3), used in all nine decomposer×executor combinations.
- **Qwen2.5-math-1.5B / 7B-instruct** and **Qwen2.5-14B-instruct** against their **DeepSeek-R1 distilled** counterparts, for the reasoning-vs-non-reasoning study.
- **Claude-3.5-Sonnet** as the judge for MT-bench (not as a system under test).

So: one closed frontier-lite model carries the entire method evaluation, and one open-weights family carries the entire model-configuration analysis. There is no cross-check of S&D itself on a second base model.

**Benchmarks.** Four task families, five objective benchmarks plus one subjective:

- **Reasoning/math** — GSM8K (full set, accuracy) and MATH (617 level-5 problems from four topic areas, following Hong et al. 2024, accuracy).
- **Code generation** — HumanEval (full set, pass@k).
- **Creative writing** — Trivia Creative Writing (Wang et al. 2024b), N=5 and N=10, 100 instances each; scored as proportion of correct trivia-answer mentions inside the narrative.
- **Text comprehension** — HotpotQA (1,000 randomly sampled, F1) and, for the generalisation check only, **DROP**.
- **Subjective** — MT-bench, 50 of the 80 questions across writing, roleplay, reasoning, math, coding; both turns; scored 0–10 by Claude-3.5-Sonnet.

MT-bench is doing specific work here: it exists to remove the objection that GSM8K-accuracy, pass@k, mention-proportion and F1 are not commensurable, by re-running the task-type comparison under one metric.

## Author incentive

All seven authors are at **Beijing University of Posts and Telecommunications** (BUPT); corresponding authors Liuyu Xiang and Zhaofeng He. Two co-first authors (Shuodi Liu, Yingzhuo Liu). Funding is public/academic: NSFC (six grants), Fundamental Research Funds for the Central Universities, an MoE philosophy-and-social-sciences key project, and — oddly — a Chinese Nutrition Society grant.

Stake, as far as it is visible: no product, no vendor, no commercial API being sold. The incentive that *is* present is the ordinary one of proposing a named method and needing it to look good — S&D is the paper's contribution and the Pareto-frontier framing is the claim it is judged on. Two of the group's own prior works are cited (Chen et al. 2024 LLMArena, Liu et al. 2025 RainbowArena), which is normal self-citation rather than a stake in the result. The choice of GPT-4o-mini as base is a cost-driven one, consistent with a lab budget rather than a position; the fact that the paper's central variable *is* cost is at least aligned with that constraint, which is worth noticing without treating it as a distortion.

## Measurement methodology

Brushed, as asked, but a few features matter.

**Dependent variables.** Two, always reported as a pair: task metric (accuracy / pass@k / mention-score / F1 / judge score) and **cost**, itself split into average tokens per instance and average API calls per instance. Treating tokens as a co-equal DV, and plotting the two against each other, is the methodological move the whole paper rests on — the "dilemma" and the "Pareto frontier" only exist because cost is measured rather than mentioned.

**What is controlled.** Base model, temperature (0), and seed (42) are pinned across approaches. Prompts for every baseline are given in full in Appendix D, so the comparison is at least reproducible at the prompt level. In Sec. 3.3 the decomposition and execution models are varied one at a time in three controlled sets, with the nine-cell grid behind them — this is the cleanest piece of design in the paper, because it isolates *which stage* the capability has to live in. Sec. 3.3 also fixes the approach (P&E DAG) and the dataset (MATH) so the model variable moves alone.

**N and repetition.** Table 2 reports means over **five independent runs** with ± error bars (typically ±0.15 to ±0.58 accuracy points). Sample sizes per benchmark are stated (GSM8K full, MATH 617, HumanEval full, TCW 100+100, HotpotQA 1,000). The MT-bench study is 50 questions × 2 turns.

**How significance is treated: it isn't.** There are no hypothesis tests, no confidence intervals beyond those error bars, and no correction for the many comparisons being made across six approaches × six benchmark columns. More consequentially, the appendix raw-data tables (Tables 6–11), which are the ones that carry both the S&D numbers and the token costs, report a **single value per cell with no error bar at all** — so the headline Pareto claims are read off unreplicated numbers even though the baseline-only table was replicated five times. Several ranking claims turn on gaps well inside the size of the Table 2 error bars (e.g. S&D 93.56 vs CoT 93.17 on GSM8K; S&D 52.39 vs P&E 52.09 on MATH). The ablation (Table 4) and the threshold sweep (Fig. 7) are likewise single-configuration, single-dataset: the ablation runs on HumanEval only, the sensitivity analysis on Trivia Creative Writing only, and T=0.7 is then used everywhere.

**Judge and metric caveats the paper carries.** MT-bench uses an LLM judge (Claude-3.5-Sonnet) with no reported human agreement check. Trivia Creative Writing's "score" is a mention-counting proxy for writing quality, so it rewards information coverage rather than prose. HumanEval is scored with "pass@k" without k being stated.

## Key findings (and the authors' own reading)

### Takeaway I — the performance–cost dilemma

Averaged over the five objective benchmarks, the ranking is P&E (DAG) 69.40 > P&E 67.81 > ReAct 67.26 > CoT 65.65 > P&S 64.70 > IO 48.60. So decomposition does buy accuracy over a direct call, and the best average goes to the most structured approach. But the cost side is where the paper puts its weight. From the raw tables:

- GSM8K: CoT 396 tokens / 1.00 calls at 93.17; ReAct 2,700 / 6.81 at 91.66; P&E 2,443 / 5.13 at 92.34. The cheapest approach is also the most accurate.
- MATH: CoT 890 tokens at 50.73; P&E 10,521 tokens at 52.09 — ~12× the tokens for +1.4 points.
- Trivia Creative Writing N=10: CoT 816 tokens at 51.20; P&E 18,784 tokens at 54.20; P&E (DAG) 6,596 at 64.10.
- HotpotQA: CoT 1,467 tokens at 63.00; P&E (DAG) 6,600 at 65.52; ReAct 5,181 at 53.52 — i.e. an expensive approach that is *worse* than the cheap one.

The authors' own reading: explicit approaches buy their wins at prohibitive cost (they single out P&E on TCW N=5 at ~10× the highest-token implicit approach, and note P&E (DAG) is consistently good but still ~4× implicit cost), and this is a dilemma rather than a solved trade-off. IO is weak everywhere. Implicit approaches (CoT, P&S) do well on GSM8K, which they attribute — hedged, "likely" — to alignment with post-training patterns, and degrade on tasks that cannot fit in one call.

### Takeaway II — task characteristics determine sequence, calling form, and topology

Best approach by task family: math/reasoning → CoT and P&E; code generation → ReAct (the only one near 90 on HumanEval); writing and text comprehension → P&E (DAG). MT-bench reproduces the pattern under one metric: CoT tops math (9.14 avg) and reasoning (8.11); P&E (DAG) tops writing (8.53) and roleplay (8.29); coding is the one place the pattern breaks — ReAct only ranks second (6.35) behind CoT (6.76), which the authors attribute to their ReAct having no code-execution component.

Their reading is a cognitive-demand story: logical rigor suits CoT's implicit and P&E's linear stepwise chaining; divergent thinking suits DAG's parallel branches; iterative refinement suits ReAct's explicit interleaving. They present this as validating a hypothesis, and it is what the selection prompt is built out of — the three prompt dimensions (logic / iterative / divergent) are exactly these three.

### Takeaway III — the executor, not the decomposer, carries the capability

On MATH with P&E (DAG), across the 3×3 Qwen2.5 grid, accuracy rises with parameter count on both axes, but the slope for scaling the *execution* model is markedly steeper than for scaling the *decomposition* model, and the execution-scaling curve nearly coincides with the scale-both curve. Their reading: the executor is the primary driver of the scaling effect, and a plan from a smaller model is largely good enough.

The reasoning-model result splits by stage and is the most interesting nuance in the paper. In **decomposition**, R1-distilled models fix the format-compliance problem at 1.5B and 7B (non-reasoning models there frequently emit invalid plans) — but at **14B the reasoning model produces *more* invalid plans than its non-reasoning counterpart**, which they read as reasoning ability trading off against structural/format control when abstract reasoning is prioritised. In **execution**, reasoning models beat non-reasoning ones at every scale tested.

### The S&D results

- **Pareto claim.** S&D is reported on the Pareto frontier on all five objective benchmarks and on DROP.
- GSM8K: 93.56 at 517 tokens / 1.28 calls — beats every individual approach at ~1.3× IO's call count.
- MATH: 52.39 at 2,560 tokens / 2.31 calls, against P&E's 52.09 at 10,521.
- HumanEval: 88.55 at 846 tokens / 1.18 calls, against ReAct's 90.07 at 3,422. HotpotQA: 65.26 at 1,640, against P&E (DAG)'s 65.52 at 6,600. The paper's framing: near-optimal at **24.77%** of the average token cost.
- DROP: 74.34 at 851 tokens, against P&E (DAG)'s 76.58 at 2,462.
- **Trivia Creative Writing is the exception, and the paper says so obliquely.** N=5: S&D 59.20 vs P&E (DAG) 64.60. N=10: S&D 55.70 vs P&E (DAG) 64.10, and S&D (2,903 / 1,462 tokens) is cheaper than several baselines but clearly *below* them in score. The authors describe this as "an approximately linear trade-off between performance and cost along the Pareto frontier" where implicit and explicit approaches differ sharply — a fair description of a point that is cheap-and-worse rather than a win.
- **Selection distribution (Fig. 6).** After the full select-execute-verify loop, ~85% of final approaches are implicit and only ~15% explicit; within that, CoT and P&E skew to math, ReAct to code, P&E (DAG) to writing and comprehension. The authors read this both as evidence that S&D defaults to cheap and escalates rarely, and as independent confirmation of Takeaway II.
- **Ablation (HumanEval).** Full 88.55 @ 846 tokens. Replacing selection with a fixed IO start: 86.59 @ 542 (cheaper, worse). Replacing selection with a random start: 87.19 @ 2,782 (**+229% tokens** and still worse) — the sharpest single number in the paper, since it separates *choosing* from merely *having* the approach pool. Removing validation: 85.98 @ 753, the largest accuracy drop of the three, which they read as the verifier suppressing hallucinated/low-quality solutions.
- **Threshold sensitivity (TCW).** Raising T improves performance by filtering weak candidates, with cost climbing sharply past 0.9. They pick T = 0.7 partly because token cost is minimised there in the 0.5–1.0 range and it even beats T = 0.8 on performance — a non-monotonicity they note but do not explain.
- **Generalisation.** The selection prompt carries no dataset-specific content, and S&D retains its cost advantage on the held-out DROP benchmark.

## Open questions the paper raises

In its own framing, the Limitations section states two:

1. **Only the decomposition mechanism was examined** — representation format (code vs. text) and external tool use were deliberately left out, though the paper acknowledges prior work shows both improve performance. Consequence they name: for tasks requiring specialised tools, S&D "might need to be adapted accordingly in order to function properly."
2. **The selection module is prompt-only, untrained.** If the model in the selection module is relatively weak, selection quality degrades and overall performance degrades with it. They flag training the selector as a promising direction.

Also raised inside the body rather than the Limitations section, and left open:

- The 14B reasoning-model regression on plan *format* validity — increased reasoning ability appearing to compromise structural compliance — is observed and hypothesised about, not resolved.
- The non-monotonic threshold behaviour (T=0.7 outscoring T=0.8) is noted without an account.
- Sec. 5.3 promises "we will discuss scenarios when S&D fails or performs poorly in the limitations section"; the Limitations section as written does not actually deliver a failure-case analysis, so the Trivia Creative Writing shortfall is never diagnosed.
- The Ethical Considerations section raises over-reliance on automated decision-making, inherited bias, privacy in sensitive handling, and the environmental/accessibility cost of token-heavy strategies — the last being the same cost axis the paper measures, now framed as an equity issue.

## Appreciation — mechanism vs. magnitude

### What transfers as mechanism

- **Cost belongs in the dependent variable.** The single most portable move here is refusing to report accuracy alone. Once tokens and API calls sit on the same plot, "decomposition helps" stops being a claim and becomes a question about where on a frontier you want to sit. That reframing survives any change of model or benchmark.
- **There is no dominant decomposition strategy; the winner is task-conditional.** The specific mapping (CoT→math, ReAct→code, DAG→divergent) is a magnitude claim, but the *existence* of a strategy×task interaction — and that it survives a change of metric from five heterogeneous objective scores to one LLM-judge scale — is a mechanism-level result.
- **Selection is a distinct source of value from having the pool.** The `w/o Select (Random)` ablation is the cleanest argument in the paper: same six approaches, same escalation, same verifier, only the initial choice randomised — and cost triples while accuracy falls. That isolates routing as a mechanism, independent of the pool's contents.
- **Stage asymmetry: the executor carries the capability, the planner mostly needs to be well-formed.** If this holds, it is a genuine design principle — put the expensive model where the work is done, not where the plan is written. The paper's own qualifier is important and also transfers: the cheap decomposer must still be able to emit a *valid* structure, and that is a format-compliance property, not a reasoning one, which is why the R1-distillation result cuts both ways.
- **Escalation should start cheap and be verifier-gated.** The IO→implicit→explicit ladder is a mechanism claim about ordering: default to the cheapest thing and let a confidence signal, not the task label, purchase more structure.
- **A separable taxonomy of decomposition.** Six axes, of which three are general-purpose and three are domain-bound, is a usable vocabulary regardless of whether one accepts the paper's numbers. Its value is that it makes "decomposition" stop being one thing.

### What is magnitude only — valid inside this setup

- **Every headline number is GPT-4o-mini at temperature 0, seed 42.** 24.77% of average token cost, 88.55 on HumanEval, the 85/15 implicit-explicit split — all of these are properties of one small, cheap, closed model. In particular, the finding that implicit approaches dominate the final selection distribution is plausibly a statement about how much a *weak* model gains from structure; a stronger base model would shift both the frontier and the selector's behaviour, and there is no second base model to check.
- **The strategy→task mapping is a mapping over six specific prompt implementations, not over decomposition-as-such.** Their ReAct has no tools and no code execution — the paper says so — so "ReAct is best for code" is a claim about a toolless reasoning-acting prompt on HumanEval. Similarly P&E is PEARL's prompt, not a general planner.
- **T = 0.7 and K = 3.** Tuned on one dataset (TCW), applied to all. The threshold sweep's non-monotonicity is itself a hint that the surface is noisy at this N.
- **The Pareto claims themselves.** They are read off single-run appendix numbers while the baseline table was five-run. Several of the wins (GSM8K +0.39 over CoT, MATH +0.30 over P&E) are smaller than the replicated error bars elsewhere in the paper, and no test is applied. The *cost* differences, by contrast, are order-of-magnitude and survive that objection comfortably — so the robust part of the Pareto claim is "much cheaper at roughly comparable accuracy", not "more accurate".
- **The verifier's confidence score is self-assessment by the same model family that produced the answer**, with no calibration study. Its measured contribution (−2.90% accuracy when removed, on HumanEval alone) is a within-setup number, and the well-known fragility of LLM self-confidence means it should not be assumed to port.
- **Trivia Creative Writing is a counterexample inside the paper's own data** and should be carried as such: on the one benchmark where the gap between cheap and expensive approaches is genuinely large, the selector systematically under-buys structure and loses 5–8 points. That is not a rounding-error disagreement; it is the failure mode the method is most exposed to, described rather than diagnosed.

### Smaller observations

The taxonomy's six axes are not fully independent (implicit approaches are single-call and therefore near-necessarily linear and decomposition-first-ish), which makes Table 1's three-axis placement of five methods thinner than it appears — CoT is classed as "interleaved" while being a single call, which strains the axis. Appendix B.1 miscites ReAct as Wang et al. 2023 rather than Yao et al. 2023, and Sec. 5.3 refers to "Table 8" for what is Figure 8. Neither affects the results.

## How it could serve a harness-design effort

Stemming the discussion rather than resolving it — several threads a harness designer could pull on, each with its own catch.

**1. A router over strategies, not a fixed pipeline.** The paper's core proposal is that the harness should not commit to one decomposition depth or shape; it should ask, per request, which shape to use. That maps directly onto a harness that owns several execution modes and picks between them. The open question it leaves is *where the router's knowledge comes from*: here it is a hand-written prompt encoding three task dimensions the authors derived from their own Sec. 3 experiments. A harness built this way inherits the router prompt's blind spots, and the paper's own limitation — a weak selector poisons everything downstream — becomes a single point of failure that has no fallback other than the random-within-group ladder.

**2. Budget as an observable, not an afterthought.** Instrumenting tokens and call counts per strategy is cheap and immediately makes strategy choice legible as an economic decision. The paper shows the spread is 1–20× on the same task, which is large enough that a harness not measuring it is flying blind. The unresolved part: the paper measures average cost per instance, not tail cost, and an escalating loop's worst case (K=3 switches, each possibly an explicit multi-call approach) is what actually breaks a latency or budget envelope. Nothing here bounds the tail.

**3. Verifier-gated escalation as a control structure.** Confidence → accept-or-escalate is a clean control loop and the ablation says the verifier is load-bearing. But the design here is weak in ways a harness would have to fix: the confidence score is unc alibrated self-assessment; the recovery step is *random* within a group rather than informed by why the first attempt failed; and the ladder's first fallback is IO, meaning a low-confidence answer is first retried with *less* structure. Whether that ordering is principled or an artifact of optimising average cost on these benchmarks is not established.

**4. Stage-differentiated model assignment.** "Cheap planner, strong executor" is directly actionable for a harness that already separates orchestration from execution. The caveat the paper supplies itself is the one to keep: cheap planners fail on *format validity* before they fail on plan quality, and the fix (reasoning-distilled small models) has its own inversion at 14B. A harness would want structural validation of plans as a first-class step rather than trusting the decomposer — which the paper measures (invalid-plan counts) but does not build into S&D.

**5. Where it does not reach.** Scope-wise this is prompt-level decomposition with no tools, no code execution, no memory, no multi-turn state, and no sub-agent hierarchy — the six baselines are all single-agent prompting strategies, and depth never exceeds one level of splitting. Anything a harness needs about recursive decomposition, depth control, or coordination cost between sub-agents is outside what this paper measured. Its "cost of splitting" is token cost only; coordination and failure-propagation costs are not in the frame.

**6. Major concerns to carry forward.** Single base model for the method; single-run headline numbers with no significance treatment; a self-scoring verifier; hyperparameters tuned on one dataset and applied globally; and one benchmark (Trivia Creative Writing) where the method visibly loses and the promised failure analysis is absent. None of these overturn the mechanism-level claims, but all of them constrain how far the magnitudes should be carried.

## Five citations worth chasing

1. **Huang et al. 2024, "Understanding the Planning of LLM Agents: A Survey"** (arXiv:2402.02716) — the source of this paper's decomposition-first vs. interleaved axis; the natural place to see whether the six-axis taxonomy is an extension of an existing one or a rival to it.
2. **Prasad et al. 2023, "ADaPT: As-Needed Decomposition and Planning with Language Models"** (arXiv:2311.05772) — cited but not used as a baseline, and it is the closest prior work on *conditional* decomposition (recursive, triggered by execution failure) as against S&D's up-front selection plus verifier escalation. The comparison S&D never runs.
3. **Sun et al. 2023b, "PEARL: Prompting LLMs to Plan and Execute Actions over Long Documents"** (arXiv:2305.14564) — the actual source of both P&E and P&E (DAG), i.e. two of the six arms and the carrier method for the entire model-discrepancy study.
4. **Khot et al. 2022, "Decomposed Prompting: A Modular Approach for Solving Complex Tasks"** (arXiv:2210.02406) — the interleaved / pure-LLM corner of the taxonomy, and the modular-subtask formulation that the "unlimited subtask selection range" axis implicitly argues against.
5. **Hu, Lu & Clune 2025, "Automated Design of Agentic Systems"** (arXiv:2408.08435) — cited only for a HotpotQA sampling convention, but it is the strongest counterposition available in the reference list: searching for agent architectures rather than selecting among six hand-specified ones.

Runner-up worth noting: **Wang et al. 2024b** (Trivia Creative Writing / Solo Performance Prompting), since that benchmark is both the paper's most discriminating task and its one clear loss.
