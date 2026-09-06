# When More is Less: Understanding Chain-of-Thought Length in LLMs

## Density

**Density: HIGH** — Almost every page is load-bearing on the Subject: the paper's entire object of study is *how many pieces to split a task into*, it argues the depth/accuracy relation is non-monotonic, and it gives that claim three independent supports (real LLMs, a controlled synthetic task, a closed-form model) plus two derived interventions; the repetition across those three supports is triangulation of one claim rather than padding.

**Keywords (mine, not the paper's):** optimal decomposition depth; inverted-U accuracy curve; error accumulation vs. sub-task difficulty; per-step compute budget; simplicity bias; capability-indexed granularity; RL length collapse; length-aware answer aggregation; reasoning-boundary model.

**Year.** First posted 11 Feb 2025 (v1). Read here in **v3, 27 May 2025** — the version the arXiv HTML serves, and the one all section/figure references below track. The arXiv API reports a further metadata `updated` timestamp of 6 Sep 2026 with no new version body change visible in the served HTML.

**Venue.** Recorded as instructed, since the brief flags this as a PREPRINT. What I can confirm from primaries:
- The arXiv metadata record carries **no `journal_ref`, no DOI, and no comments field** — arXiv itself asserts no venue.
- The paper body carries no camera-ready venue stamp, no "Published as a conference paper at…" banner, and is licensed CC BY-NC-SA 4.0 (a license choice more typical of a self-posted preprint than of most camera-ready templates).
- The acknowledgement section names grant funding but no conference.
- Secondary indexes initially **disagreed with each other**: one third-party reading-note repository labels it "ICLR'25", while a search-engine summary asserted "ICLR 2026, under review". Neither is a primary source and they are mutually exclusive.
- The disagreement resolves against both. The Semantic Scholar record (retried after an initial 429) gives `venue: arXiv.org`, `publicationVenue: arXiv.org`, and the only DOI is `10.48550/arXiv.2502.07266` — the auto-minted arXiv DOI, not a publisher's. **DBLP indexes it as `journals/corr/abs-2502-07266`** — the CoRR preprint stream, with no conference-proceedings entry aliased to it. Both indexes are ordinarily prompt about attaching a proceedings record once one exists.
- Its **citation count is nonetheless high — 209 at time of reading** — so this is a preprint with substantial uptake, not an obscure one. Influence and refereeing are decoupled here.

**Status I will therefore assume:** treat as an **unrefereed preprint**, and one that has now been public long enough (Feb 2025 → Sep 2026, last body revision May 2025) that the absence of a proceedings record is mildly informative rather than merely a lag. No primary source seen in this reading establishes peer review, and the one venue claim that could be checked against the paper itself (a camera-ready banner) is absent. Claims below are weighed accordingly — in particular, the paper's own framing of several results as "proof-of-concept" is taken at face value rather than as understatement.

**Authors / affiliations.** Yuyang Wu (Peking University), Yifei Wang (MIT), Ziyu Ye (University of Chicago), Tianqi Du (Peking University), Stefanie Jegelka (TUM and MIT), Yisen Wang (Peking University, corresponding). Wu and Y. Wang marked equal contribution.

## Approach

The paper attacks one question — *does accuracy keep improving as a chain of thought is split into more steps?* — and answers "no" via a three-legged argument, each leg covering the others' weaknesses.

**Leg 1, observational (Sec. 2).** Take off-the-shelf instruct models and hard maths problems. For a *fixed* question, elicit many solutions of *differing step counts*, bin them by length, and plot accuracy against the bin. The key methodological move is that length is varied *within* a question, so the length/accuracy relation is not confounded by which questions happen to be long. Length is read as **number of reasoning steps**, not tokens — segmentation is by newline, following Fu et al. Variation in length is induced not by asking the model to be long or short (the paper explicitly rejects that: instruction-following on length is poor, and length prompts invite padding tokens that add no steps) but by **8-shot in-context exemplars at three complexity levels**, sampled 20× each for 60 samples per question. Truncation via `max_length` is likewise rejected as it would mechanically penalise long outputs.

**Leg 2, controlled (Sec. 3).** Because real CoTs mix in planning, backtracking, reflection and heterogeneous pretraining, the paper builds a synthetic task where decomposition depth is an explicit, dialable knob. Arithmetic expressions of addition only, with a pruned computation tree; total operator count `T` is task difficulty; a solution is a `t`-hop CoT that consumes `t` operators per step, so `N ≈ T/t` is the depth. A control token `<t>` prepended to the solution lets the experimenter *command* a depth at test time, or omit it and let the model pick. GPT-2 models of varying **depth in layers** (5–9) stand in for varying model capability. This gives the paper the thing the real-world leg cannot have: the same task solved at many decomposition granularities, by models of graded capability, with everything else held fixed.

**Leg 3, theoretical (Sec. 4, App. F–G).** A closed-form accuracy-vs-depth model built from two opposing terms — sub-question extraction error that is paid once *per step* (so it compounds with depth), and sub-answer error that *falls* with depth because each step gets easier. Their product is maximised at an interior `N*`, for which a closed form is derived, and from which the scaling laws in difficulty and capability are proved as corollaries.

**Then two derived interventions (Sec. 5)**, offered as proof-of-concept rather than as a method contribution: curate *training* data at the optimal length, and filter by length at *inference*.

## Models targeted, benchmarks, and the formal setting

**Real-world models.** Qwen2.5-Instruct at 1.5B / 7B / 14B / 32B / 72B (the size ladder that carries the capability claim); Llama-3.1-8B-Instruct and 70B-Instruct as a replication in App. C.2; Qwen2.5-7B-Instruct as the RL subject.

**Real-world data.** MATH **Level 5** only (Hendrycks et al. 2021b) — deliberately the hardest tier; MMLU-STEM as a second domain (App. C.2); GPQA (Rein et al. 2023), a 100-question random subset, for the inference-time voting experiment; LeetCode-2K (Xia et al. 2025) for the RL run.

**Sample sizes, as stated.** 30 questions per model for the optimal-length-vs-model-size curve; 100 questions for the difficulty correlation; 60 sampled solutions per question throughout; 100 questions per `(T, t)` cell in the synthetic study.

**Synthetic setting.** GPT-2 architecture, layers 5–9, trained 25,000 iterations at batch 256 on a mixture of `T ∈ [12, 80]` and `t ∈ [1, 12]`; single A800 80GB. Digits are mod 10, keeping the vocabulary and per-step answer space small.

**Formal setting (the theory leg).** The object is `A(N)`, final accuracy as a function of depth `N`, given task difficulty `T` (operator count) and model capability `M`, where `M` is defined as a **reasoning boundary** — the largest number of operators the model can resolve in a single step without further decomposition (borrowed from Chen et al. 2024b). Each step is a sub-question `q_i` plus a sub-answer `a_i`; the chain's probability is the product over steps of (probability the right sub-question is posed) × (probability it is answered right), conditioned on history.

Assumptions, and where each bites:
- **`σ(T)`, sub-question error, is independent of `N` and rises with `T`.** Justified empirically in App. E.2: sub-*question*-token loss varies only ~3× between the easiest and hardest step size, whereas sub-*answer*-token loss varies by ~1e4 — so treating question-extraction error as constant in `t` is argued to be a tolerable approximation *in this task*. App. E.2 also reports no clear dependence of sub-question loss on model size, which is why `M` does not appear in `σ`.
- **`E(N,M,T) = T/(NM)`, sub-answer error, falls linearly with depth and capability.** This is the load-bearing functional form in the closed-form theorem.
- **All steps are homogeneous** — same difficulty, same error rate — and `t = T/N` is allowed to be fractional.
- **`σ(T) = T/C ≤ 0.9`**, restricting attention to tasks inside the training regime.

What is proved, and at what strength:
- **Prop. 4.2** — `A(N) = α[(1−E(N,M,T))(1−σ(T))]^N`, with `α = (1−σ(T))^{2T}` independent of `N`. Derivation, not an assumption, given the per-token error model (a `t`-operator sub-question is `2t+1` tokens, each surviving with probability `1−σ`; the `N`-fold product of `(1−σ)^{2t+1}` collapses to `(1−σ)^{2T}` because `Nt = T`). *This collapse is the analytical heart of the paper and is worth stating plainly: the per-step transcription cost is depth-invariant in total, so it falls out into the constant, and the entire inverted-U is generated by the residual `(1−σ)^N` term racing against `(1−T/(NM))^N`.*
- **Thm. 4.3** — inverted-U in `N`, with `N*(M,T) = TZ / (M(Z+1))` where `Z = W₋₁(−(1−T/C)/e)`, the lower branch of the Lambert W. Theorem, with a complete calculus proof (App. G.2).
- **Cor. 4.4** — the three scaling laws: `N*` increases in `T`; optimal per-step size `t* = M(1+1/Z)` increases in `T`; `N*` decreases in `M`. Theorem. The `T`-monotonicity is the non-trivial one and is done by implicit differentiation (sign of `∂x*/∂T` from `−F_T/F_x`, with `F_x < 0` shown for all `x > 0`); the other two are called "easily derived through monotonic composition".
- **Cor. 4.5** — RL converges to `arg max_N A(N)`. Theorem, but in a **stateless bandit** reduction: a finite discrete action space over lengths, softmax policy, binary outcome reward, gradient ascent with sufficiently small step size. This is a statement about an idealised policy-gradient fixed point, not about GRPO/PPO on a language model.
- **App. F.1, Thm. F.3** — generalisation beyond the linear form. Under monotonicity/convexity assumptions on `E` (decreasing and convex in `N`, decreasing in `M`, increasing in `T`, `→0` as `N→∞`) and monotone `σ`, it proves `lim_{N→∞} A(N) = 0` (long chains always fail) and a **lower bound** on `N*`, `N_LB = E_N^{-1}(1 − 1/(e²(1−σ(T))))`. Note the honest weakening: this is conditional ("*if* `A(N)` has a maximum at `N* > 1`") and bounds `N*` rather than locating it; the scaling laws in Cor. F.4/F.5 then follow for that bound, with an explicit parenthetical caveat "assuming `σ(T)` doesn't dominate adversely".
- **App. F.2, Thm. F.6** — heterogeneous errors. Per-step error rates become Beta random variables with the right means; the result is an **upper bound** `Â(N)` on expected accuracy that is itself inverted-U. So the stochastic extension shows the bound retains the shape, not that the expectation does. The text also concedes the `σ_i`/`e_i` are *not* independent (easy steps predict easy steps; a self-validation step lifts its dependents) — flagged as an interpretation of backtracking behaviour, and not modelled.

## Author incentive

Academic, and unusually clean of product stake. Peking University, MIT, TUM, University of Chicago; funding named as the National Key R&D Program of China, NSFC, Beijing Nova Program, the NSF AI Institute TILOS, and an Alexander von Humboldt Professorship. No lab is shipping a reasoning product whose selling point this result would flatter or damage; the models used (Qwen2.5, Llama-3.1, GPT-2) are all third-party or generic.

The incentive that *is* present is positional, and worth naming because it shapes the framing more than the numbers. The paper is written against a prevailing "longer is better / scale test-time compute" position, and its title, epigraph and abstract all lean on the contrarian reading. The related-work section is candid that several concurrent works had already reported "overthinking"; the paper's claim to distinctiveness is therefore not the phenomenon but the *scaling laws plus theory* around it. A second, milder positional stake: Sec. 3.2's insight II ends by pointing at looped Transformers / adaptive recurrent depth as the promising architectural response — an argumentative bet, not a result of the paper.

## Measurement methodology (brushed)

**Dependent variable.** Accuracy — final-answer correctness. Never a cost, latency or token-count measure, which matters: the paper's "less is more" is a claim about *accuracy*, and it is thus a strictly stronger claim than the usual efficiency argument for short chains. Longer chains here are not merely wasteful, they are *wrong more often*.

**Independent variable.** Depth, operationalised as **step count**, with a defended rejection of token count. The argument (App. C.1) is that as a model decomposes further, tokens *per step* shrink, so total token count is not monotone in decomposition depth and is an unreliable proxy for reasoning structure. In the synthetic setting depth is exact by construction; in the real setting it is newline-segmented lines with empty lines dropped.

**What is controlled.** In the real-world leg, the question is held fixed while length varies — the essential control. Binning normalises lengths: bin width 5 for cross-model comparisons (justified as needed for adequate per-bin sample size given only 30 questions per group), bin width 2 for the per-question difficulty analysis, with a stated check that width 1 gives near-identical results. In the synthetic leg, everything but the knob under study is held fixed: model depth in layers is the *only* hyperparameter varied to represent capability, and CoT length is varied at fixed `T`.

**Filtering.** For the difficulty-vs-optimal-length analysis, questions with accuracy `<0.01` or `>0.99` are excluded, on the stated grounds that saturated questions cannot show length dependence. This is a defensible exclusion, but it is also a **restriction of range on the dependent variable that will inflate the correlation** being reported — worth registering, as it directly touches the headline `p`-value.

**Difficulty proxy.** `1 − accuracy` of the same model on the same question, from 60 samples. So difficulty is model-relative and estimated from the same 60 samples that supply the length curve — the independent variable of Fig. 2(b) is derived from the same draws as the dependent one.

**Significance treatment.** Present but light, and confined to one claim. The difficulty/optimal-length correlation is reported with `p = 1e-8` for Qwen-1.5B, plus a 95% confidence band around the regression line computed via Student's *t*. Elsewhere — the model-size ladder, the optimal-vs-longest gap, the synthetic curves, the RL trajectories, both Sec. 5 interventions — results are point estimates read off figures with **no error bars, no seeds, no significance tests reported**. There is no multiple-comparison treatment across the four extra model replications in App. C.2.

**N.** Modest and openly so: 30 or 100 questions, one RL run per setting, single-GPU synthetic training. The paper does not oversell this; Sec. 5 is labelled "proof-of-concept" in its own text.

## Key findings, with the authors' own reading

**1. Accuracy is inverted-U in decomposition depth.** The central claim, and the one carried by all three legs. Both failure modes are named and treated as symmetric: chains too short have steps too complex for the model to execute; chains too long accumulate per-step error. The authors read this as a unification of "underthinking" and "overthinking" as two sides of one trade-off rather than two separate pathologies.

**2. Optimal depth *falls* with model capability.** Real-world: optimal length moves from **14 steps at 1.5B to 4 steps at 72B** on MATH Level 5. Synthetic: optimal `N*` decreases monotonically with layer count at every difficulty. The authors name this **simplicity bias** and read it as stronger models consolidating more work into each step — explicitly linked to the reasoning-boundary `M` in the theory, and analogised to Occam's razor and to the classical simplicity-bias literature in neural networks.

**3. Optimal depth *rises* with task difficulty.** Real-world: significant positive correlation between `1−accuracy` and optimal length (`p = 1e-8`), replicated on 7B/14B Qwen, 8B/70B Llama, and on MMLU-STEM. Synthetic: the peak shifts right as `T` grows. Read as: a good reasoning model must vary its decomposition depth *per problem*, not per model.

**4. Harder tasks peak at harder sub-tasks.** The envelope of Fig. 3(a): optimal *per-step* size `t*` grows with `T`. The authors read this as the more surprising of the two scaling directions — for a hard problem, adding more *simple* steps is not equivalent to, and is worse than, making each step do more. Their stated implication is architectural: fixed-layer Transformers cannot vary per-step compute depth, so their reasoning is structurally suboptimal, and adaptive-depth/looped architectures are the natural fix.

**5. The cost of getting depth wrong is large.** Optimal-length vs. longest-length accuracy differ by **up to ~40% absolute at 72B**, and — the sharper point — *the gap widens as models get stronger*. The authors read this as the practical stake: stronger models are hurt more, not less, by over-decomposition.

**6. RL shortens chains.** Both in the real setting (GRPO on Qwen2.5-7B-Instruct over LeetCode-2K: average response length **decreases** as accuracy improves) and synthetically (PPO on VERL, `T=24`, converging on `N*=5` at 96% accuracy). The authors are careful about what this contradicts — they cite the common belief that RL lengthens reasoning outputs, and note prior work that RL behaviour largely inherits from the base model. Their reading is that outcome-reward RL *implicitly discovers* the optimal length, which reframes part of RL's benefit as **length calibration**: RL can repair a pretraining/SFT corpus whose CoT lengths were mismatched to the model.

**7. Training data length should be matched to the model.** A 6-layer model trained only on optimal-length solutions **beats a 9-layer model trained on mixed-length solutions**, with the gap widening as `T` grows (`T=32` and `T=64`). The authors' reading is the strongest practical claim in the paper: common practice — reusing one CoT corpus across model sizes, or distilling a large model's CoTs into a small one without re-granulating them — is systematically suboptimal, because a small model cannot execute steps sized for a large one.

**8. Length-filtered voting beats majority voting.** Bin candidates by length (width `D=2`), compute Shannon entropy of the answer distribution in each bin, keep the `K=3` lowest-entropy bins, majority-vote within those. On 100 GPQA questions it beats vanilla self-consistency across sample counts, and — the interesting part — **does not degrade as sample count grows**, whereas vanilla voting does. Note the inference: since `N*` is unknown at test time, entropy is used as a *surrogate* for proximity to the optimum, on the stated intuition that lower answer uncertainty marks the better length regime.

## Open questions the paper itself raises

In its own framing, the paper's stated limitation is narrow and singular. **App. A** concedes exactly one thing: *estimating the optimal CoT length in real-world settings remains hard*, because real tasks are complex and variable, and the theory/experiments give only heuristics for a coarse approximation that "may not fully capture the nuances of diverse problem domains or model behaviors". Future work is named as better estimators and adaptive selection strategies.

Other openings the paper raises in passing rather than in its limitations section:
- Sec. 5.1: "it is generally hard to exactly estimate optimal CoT lengths in real-world problems… We leave more in-depth studies to future work" — the training-data result is explicitly a proof of concept, not a recipe.
- Sec. 3.2 (II): whether **adaptive per-step compute** (looped Transformers, recurrent depth) actually realises the predicted gain is posed as a direction, not tested.
- Sec. 4.1, footnote 1: reflection, verification and backtracking are *not* modelled; they are folded into "one of the many ways one can decompose a task", i.e. absorbed into the decomposition abstraction by assertion rather than by analysis. The paper flags this itself.
- App. F.2: the non-independence of per-step error rates is raised, given an interpretation (self-validation steps lifting their dependents; a rationale for backtracking), and then left unmodelled.
- App. F.1: Thm. F.3's conditional form ("*if* `A(N)` has a maximum at `N*>1`") leaves the *existence* of an interior optimum in the general case as an open matter — only the linear case gets existence.

## Appreciation

**MECHANISM — what transfers as an argument.**

The paper's durable contribution is a *shape* and a *reason for the shape*, and both survive the specifics of the setup.

The reason is the cleanest thing here. Decomposition buys you easier sub-problems and charges you a per-step failure risk, and because the successes multiply, the charge compounds *geometrically* in depth while the benefit is at best sub-geometric. Any quantity that is a product over steps of a per-step success probability, where deeper splitting raises that probability but adds factors, will be non-monotone in depth. That is not an artefact of arithmetic tasks, of GPT-2, or of the linear error form — it is a structural property of chained execution with imperfect steps, and the paper's App. F.1 generalisation (mild monotonicity/convexity assumptions only) is doing real work in showing precisely that. **This is the transferable core: an optimal decomposition depth exists because reliability compounds multiplicatively against a decomposition benefit that saturates.**

The two scaling directions transfer as *directions* with good confidence, because they are over-determined — each is derived from the theory, reproduced in a controlled setting where the confound structure is fully known, and observed on real models across two model families and two datasets. That the same qualitative fact falls out of a Lambert-W closed form, a GPT-2 layer sweep, and a Qwen size ladder is the strongest thing in the paper. In particular the capability direction is genuinely counter-intuitive and worth carrying: *the better your executor, the shallower you should split*. Its corollary — that a decomposition tuned for one executor is wrong for a stronger one — is a real argument, not a number.

The methodological move of **varying length within a fixed question** deserves separate credit, and transfers as a design lesson: the naive version of this study (comparing long answers to short answers across questions) measures question difficulty, not the effect of length. The refusal to use token count as the depth variable, with a stated reason (tokens-per-step shrinks as steps multiply, so total tokens is not monotone in depth), is likewise a transferable correction.

The **RL result is the most interesting under-argued claim**. Reframing outcome-reward RL as a length-*calibration* mechanism — one that can repair a corpus whose granularity was mismatched to the model — is a genuinely useful reframing, and it has the theory's blessing via the bandit reduction.

**MAGNITUDE — what is valid only inside this setup.**

Nearly every number should stay inside the paper's own walls.

- **"14 steps at 1.5B, 4 steps at 72B."** This is MATH Level 5, newline-segmented, bin width 5, 30 questions, with length induced by three fixed 8-shot exemplar sets. Change the segmentation rule or the elicitation and the integers move. The *direction* is the finding; 14 and 4 are not portable constants.
- **"Up to 40% accuracy gap"** between optimal and longest. This is a gap against the *longest* bin, i.e. against an adversarially bad choice, on the hardest available tier, and with the longest bin plausibly enriched in questions where the model was floundering. It is an upper bound on the stake, not an expected loss from mediocre length choice.
- **`p = 1e-8`.** Weakened by three things the paper is transparent about but does not adjust for: the saturated-question exclusion restricts range and inflates correlation; difficulty and optimal length are both estimated from the *same* 60 samples per question; and no correction is applied across the several model replications.
- **The 6-layer-beats-9-layer result.** A striking demonstration, but on synthetic addition with a controlled granularity token, single runs, no error bars. It shows the effect *can* dominate a layer of depth in a toy regime; it does not size the effect for real training.
- **Length-Filtered Vote's margin on GPQA.** 100 questions, one dataset, fixed `D=2`/`K=3` with no sensitivity analysis. The non-degradation with sample count is the more interesting observation, but a single-dataset proof of concept.
- **The RL length curve.** One base model, one dataset, one RL algorithm, one run. That RL *can* shorten chains is shown; the widely reported opposite behaviour in long-CoT reasoning models is not engaged with beyond a citation, and the paper does not characterise when each occurs. Note also that its own real-world RL evidence measures **average response length in tokens** — the very proxy Sec. 2/App. C.1 argues against as a measure of decomposition depth.

**Where the theory is weaker than its presentation.**

Three specific gaps, none fatal, all worth holding:
1. `E(N,M,T) = T/(NM)` is not derived from anything; it is the assumption that generates the closed form, and the closed form is what supplies the elegant Lambert-W expression that lends the result its air of inevitability. App. F.1 is the honest reply to this and largely works — but note what it *costs*: in the general case the paper proves only a **lower bound** on `N*`, conditional on an optimum existing, and it is the bound whose monotonicity is then shown. That is materially weaker than Cor. 4.4 and the main text does not foreground the difference.
2. The stochastic extension (Thm. F.6) bounds the expectation from **above** by an inverted-U. An inverted-U upper bound does not establish that the expectation is inverted-U.
3. Cor. 4.5's "RL converges to the optimum" is a stateless-bandit statement over a finite, pre-enumerated set of lengths with an exact softmax and infinitesimal steps. Calling this an explanation of GRPO on a 7B model is a considerable extrapolation; it explains why *an* optimiser over lengths would find the peak, not why *this* one does under KL regularisation, entropy bonuses, and a coupled policy that must also produce content.

**On `M` as "capability".** The theory's capability parameter is a *reasoning boundary* — operators resolvable in one step. In the synthetic leg it is proxied by layer count; in the real leg by parameter count. These are three different quantities silently treated as one, and App. E.2's own finding that model size does *not* affect sub-question loss is a small crack in the identification. This does not threaten the direction of the claim but it does mean "capability" here is doing more work than it has been pinned down to do.

**Overall.** A well-constructed paper whose argument structure — same claim from observation, controlled experiment, and proof — is stronger than any individual leg. It is candid about being proof-of-concept where it is, and its one-paragraph limitations section is the least generous part of it: several real limitations (single RL runs, no error bars, the bound-vs-optimum gap, the tokens-vs-steps inconsistency in its own RL evidence) live in the appendices or between the lines rather than in App. A.

## How it could serve a harness-design effort — limitations and major concerns

*Stemming the discussion, not resolving it.*

**What it offers.** Against the Subject's "how deep" axis, this paper is the rare item that argues depth has an *interior* optimum for a stated mechanical reason, rather than arguing for more depth or for less. If its mechanism holds outside CoT — and the mechanism is stated generally enough to invite the extrapolation — then a harness that splits work has three consequences to reckon with:

1. **Depth should be a variable, not a constant.** The paper's insight I and III together say a single fixed splitting policy is wrong along *two* axes at once: it is wrong across tasks (difficulty) and wrong across executors (capability). A harness with a fixed decomposition template is, on this argument, correct for at most one (task, model) cell.
2. **Sub-task size is a separate knob from sub-task count.** Insight II is the least-anticipated result and the one most relevant to a designer: for harder work, the right move may be *fewer, meatier* sub-tasks rather than more, finer ones. Splitting policies usually expose only a count or a stopping condition; this paper says the granularity of each piece is independently consequential and moves in a non-obvious direction.
3. **Capability upgrades should trigger re-tuning of decomposition, downward.** The simplicity-bias direction implies a decomposition tuned against a weaker executor becomes actively harmful when the executor improves — and Fig. 2(c)'s widening gap says the *penalty grows* with capability. This is a maintenance claim about harnesses, not just a tuning claim.

**Two directly borrowable techniques.** The length-filtered vote (entropy over length-binned candidates as a surrogate for "am I near the right depth?") is a concrete, cheap aggregation idea that needs no knowledge of `N*`. And the within-question length-variation design is the right way to *measure* any of this in one's own setting.

**Major concerns before any of this is carried across.**

- **The gap between "CoT step" and "sub-task in a harness" is not bridged by this paper, and the paper knows it.** Its unit is a step in a single model's single generation — same context, same weights, no coordination, no handoff, no recombination stage. The Subject's coordination costs, extra calls, and recombination step are *absent* from the model entirely. Whether the inverted-U transfers is genuinely open, and there is an argument in each direction: the compounding-error mechanism should get *worse* with real handoffs (more places to lose information), while the benefit side may get *better* (a fresh context per sub-task removes the accumulating-history burden the paper's chain carries). The paper's own `H_{i-1}` conditioning has no analogue in an isolated sub-agent call. **Nothing here settles that, and the paper should not be cited as if it does.**
- **The tasks are decomposition-trivial.** Addition chains have a known, verifiable decomposition with no planning content; MATH and GPQA solutions have no *split/execute/recombine* separation. The Subject distinguishes what decides a split, what sets depth, and how splitting/execution/recombination each bear on the result — this paper collapses all three into one scalar `N` and studies only its magnitude. Splitting *quality* is modelled only as the `σ(T)` sub-question error term, which is assumed independent of depth — precisely the assumption a harness designer would most want interrogated, since choosing good sub-tasks is the hard part of decomposition and plausibly *degrades* with depth rather than staying constant.
- **Reflection, verification and backtracking are assumed away** (footnote 1) into "just another form of decomposition". For a harness whose whole design may hinge on verification stages, that absorption is a large assumption wearing small clothes.
- **`N*` is unknowable at design time.** This is the paper's own stated limitation and it is the operationally decisive one: the result says an optimum exists and which way it moves, but gives no way to locate it for a real task. A harness can act on the *directions* (re-tune on model change; deepen for hard tasks) or on the *surrogates* (entropy filtering, or letting RL find it), but cannot read `N*` off the theory.
- **Preprint status compounds the above.** With no referee having pressed on the bound-vs-optimum gap, the single-run RL evidence, or the capability-proxy conflation, the appropriate use is as a **source of hypotheses and of one mechanism**, not as a settled empirical base — notwithstanding its 209 citations.

**The one line worth carrying forward.** Not "shorter is better" — the paper does not say that, and its own insight I names underthinking as equally harmful. The line is: *decomposition depth trades a saturating benefit against a compounding cost, so it has an interior optimum that moves with both task and executor* — with the open question of whether real handoff costs move that optimum shallower still.

## Five citations worth chasing next

1. **Chen et al. 2024b — reasoning boundary.** Supplies `M`, the paper's entire notion of model capability (largest sub-problem resolvable in one step). Since `M` is what makes the capability scaling law mean anything, and since this paper proxies it by layer count and parameter count without validating either, the primary source on how a reasoning boundary is defined and measured is the highest-value follow-up.
2. **Ye et al. 2024 — controlled synthetic study of LLM problem-solving mechanisms.** The methodological parent of the whole Sec. 3 design (and cited for depth-as-capability). Needed to judge how far conclusions from synthetic arithmetic with dialable granularity have historically transferred.
3. **Chen et al. 2024c — the overthinking phenomenon.** Named as the closest concurrent work on the same phenomenon. Required for separating what this paper discovered from what it explained, and for a second, independent measurement of the same effect.
4. **Zhou et al. 2023 — least-to-most prompting**, with **Zhang et al. 2024 (divide-and-conquer)** as its companion. The paper claims these decomposition methods "fall in our analysis in Sec. 4" — a strong claim made in one sentence. Chasing least-to-most is the way to test whether the theory really covers explicit decomposition schemes or only single-chain step counts, which is exactly the bridge the Subject cares about.
5. **Geiping et al. 2025 (and Chen et al. 2025) — looped Transformers / adaptive recurrent depth.** The paper's insight II ends by betting that adaptive per-step compute is the architectural answer to "harder tasks need harder sub-tasks". That bet is untested here and is the most consequential open thread for anyone deciding how much work to put in a single step.

*Honourable mention:* Fu et al. 2023, whose complexity-based prompting supplies both this paper's length-elicitation method and its newline step-segmentation rule — worth reading for the measurement apparatus alone, and because it is cited in the introduction as an exemplar of the "longer is better" position the paper argues against while simultaneously being the source of its own instrumentation.
