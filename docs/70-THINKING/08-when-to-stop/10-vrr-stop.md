# Verify, Repair, Repeat, or Stop? Robust Stopping for Noisy Verify-Repair Loops in LLM Agents

## Density

**Density: HIGH.** Almost every section of this paper carries load-bearing content rather than restatement, and nearly all of that content bears directly on the Subject, because the paper is about nothing except when an agent loop should stop repairing its own work and commit.

## Name, keywords, year, venue

**Name.** Yitao Wu, Si Shen, Rui Yang, Hong Peng, Bin Hu. "Verify, Repair, Repeat, or Stop? Robust Stopping for Noisy Verify-Repair Loops in LLM Agents."

**Authors.** Yitao Wu, Si Shen, Rui Yang (corresponding), Hong Peng, Bin Hu.

**Year.** 2026. Submitted to arXiv on 20 July 2026 as arXiv:2607.17641v1, cs.AI, CC BY 4.0.

**Venue.** Preprint, under review, not yet peer-reviewed. The formatting, the four explicit research questions, and the acknowledgements section suggest a submission to an AAAI-style venue, but the paper itself does not name one.

**Keywords (mine).** Stopping rule; verify-repair loop; self-correction damage; verifier noise; false acceptance; false rejection; belief filtering; marginal gain; sign identifiability; Youden's J; decision margin; conservative fallback; keep-best retention; weakly supervised calibration.

## Approach

The paper studies the loop in which an LLM agent generates a plan, a verifier checks the plan, a repairer rewrites the plan from that feedback, and the cycle repeats. The authors argue that this loop rests on two premises that often fail together. The first premise is that more repair rounds tend to improve the true quality of the plan. The second premise is that the verifier's output is a usable proxy for true validity. When the verifier is noisy and the repairer can damage a plan that was already correct, both premises break at once, and the reported acceptance rate can keep climbing while the true validity of the committed plan falls.

Their proposal, VRR-Stop, has four components that build on each other.

First, they define a **four-parameter noise model**. Two parameters describe the verifier: `ρ₀` is the probability that the verifier accepts an invalid plan (false acceptance), and `ρ₁` is the probability that it rejects a valid plan (false rejection). Two parameters describe the repairer: `α` is the probability that one repair round turns an invalid plan into a valid one (the repair behaviour), and `β` is the probability that one repair round turns a valid plan into an invalid one (the damage behaviour). A fifth derived quantity, Youden's index `J = 1 − ρ₀ − ρ₁`, measures the verifier's discrimination. The separation matters because verifier failure and repairer failure enter the decision through different channels: `ρ₀` and `ρ₁` corrupt the estimate of where the plan currently stands, while `α` and `β` determine whether moving from that position is worth attempting at all.

Second, they define **belief filtering**. Each round issues `M` independent verification queries on the current plan and collects the acceptance count `S_k`. Conditional on the plan's unobserved true validity `y_k`, that count is binomial, so a Bayesian update converts the votes into a posterior `b_k = Pr(y_k = 1 | H_k)`, the *committed validity* of the current plan. The authors are emphatic that `b_k` is not the verification pass rate, since a pass rate can rise purely through false acceptance. If the loop repairs, a predict step pushes the belief through the repair transition: `b⁻_{k+1} = (1 − β) b_k + α (1 − b_k)`.

Third, they define the **stopping rule**. The true marginal gain of one more repair round is the difference between the predictive belief and the current belief, which reduces to a strikingly simple expression:

> `G_k = (1 − b_k) α − b_k β`

The first term is the expected gain from fixing a plan that is probably invalid. The second term is the expected loss from damaging a plan that is probably valid. The loop repairs when `G_k > τ` and commits when `G_k ≤ τ`, with `τ = 0` in all experiments. Setting `G_k = 0` gives a critical belief `b* = α / (α + β)`, which is also the fixed point of the population dynamics. Repair can only push validity toward `b*`; once belief crosses `b*`, further repair is expected to move quality downward.

Fourth, they argue for **sign identifiability rather than accurate estimation**. The decision only needs the sign of `G_k − τ`, not accurate recovery of the four parameters. They formalise this with an error radius `B_k` such that `Pr(|Ĝ_k − G_k| ≤ B_k) ≥ 1 − η`, and a sufficient condition `Ĝ_k − B_k > τ` or `Ĝ_k + B_k ≤ τ`. Proposition 1 states that when this condition holds, the estimated action matches the true action with probability at least `1 − η`; the proof in Appendix A.2 is a two-line interval argument. The decision margin is written `Δ_k = |G_k − τ|`, and reliability is governed jointly by `J`, `Δ_k`, and the calibration sample size.

Calibration itself is weakly supervised. The verifier parameters `ρ̂₀` and `ρ̂₁` come from a two-component binomial-mixture EM fit to per-plan acceptance counts, with no labels at all. The transition parameters `α̂` and `β̂` come from at most 300 labelled before-and-after repair pairs, labelled by each task's own validity rule. All of this is done under five-fold cross-fitting, so no instance's stopping decision ever touches its own label.

**VRR-Guard** is the estimation-free fallback for the regime where this machinery breaks. When a held-out labelled separation test reports `Ĵ` near zero, or when the identifiability condition fails throughout the window, the system stops trusting its parameters. It instead maintains an incumbent best candidate and replaces it only when a new plan beats the incumbent's acceptance count by at least a retention margin `δ`. At termination it commits the incumbent, not the last plan. Lemma 1 bounds the per-round erroneous-replacement probability by `exp(−(MJ + δ)² / (2M))` via Hoeffding on the difference of two binomials, with a union bound over `K_max` rounds. Appendix A.3 notes that this bound is loose, and gives exact tail probabilities: with `M = 8` and `δ = 5`, single-round erroneous replacement runs from `5.6 × 10⁻⁶` on the Qwen-3B judge to `5.9 × 10⁻³` on the near-inert Llama judge, so even the worst five-round union bound stays under 3 percent.

Notably, the authors do not claim that VRR-Guard dominates. They state plainly that it forfeits part of the achievable gain wherever repair actually helps, in exchange for downside protection close to the no-repair baseline wherever calibration cannot be trusted.

## Models targeted and benchmarks used

The models are all small, open-weight, instruction-tuned models served locally through vLLM 0.19.1 on a single A800 GPU per experiment. The generators and verifiers are Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct, Mistral-7B-Instruct-v0.3, Llama-3-8B-Instruct, and Qwen2.5-Math-7B-Instruct. In most settings the verifier is the same model acting as an LLM judge on its own or a sibling's output. Two settings use a non-LLM-judge verifier: MATH-500 uses the Qwen2.5-Math-PRM-7B process reward model, and BFCL multi-turn uses the benchmark's official executor. No frontier or proprietary model appears anywhere in the evaluation.

The benchmarks span four task types. GSM8K supplies grade-school mathematical reasoning with exact-match adjudication, on a 300-instance calibration probe window, a 200-instance end-to-end window, and stress windows of 200 and 500 instances. MATH-500 supplies harder mathematics with symbolic verification, at N = 500. MBPP supplies code generation with sandboxed unit tests under a five-second timeout, at N = 150. BFCL supplies tool use, adjudicated by AST matching plus the official executor, at N = 400 single-call and N = 199 multi-turn.

Two experimental regimes run on top of these. The **favorable** setting is the plain generate-verify-repair loop with no perturbation. The **prompt-mismatch stress** setting injects numeric or condition-level perturbations into the copy of the problem statement that reaches the repairer only; the verifier and the ground-truth judge always see the original statement. This construction is worth naming precisely, because it is the engine behind most of the paper's headline numbers. It manufactures a repairer that is competent but working from a corrupted premise, so its rewrites look fluent and plausible while being wrong against the true task. The repair temperature is also raised from 0.7 to 1.0 in the stress setting.

## Author incentive

The affiliations are saofund.ai (Shenzhen), Shenzhen Xingqing Zhiti Technology Co. Ltd., and the School of Information Technology and Engineering at Lanzhou University. Two of the three affiliations are commercial. Funding comes from the Chinese national Brain Science and Brain-like Intelligence Technology major project (2021ZD0200600, 2021ZD0200408), the National Natural Science Foundation of China (U24B20186), and compute from the Lanzhou University Supercomputing Center.

The stake is a proposed method rather than a product, and I see no vendor interest in any particular model performing well. If anything, the paper's incentives run against the models it uses, since its central claim is that agent self-repair damages good work. There is a mild but ordinary methods-paper incentive at work in the choice of headline setting: the 60.6-percentage-point figure comes from the stress construction that the authors themselves designed, and a stress setting designed to make repair harmful will indeed make a stopping method look valuable. The paper is not evasive about this. It labels the setting as a stress setting throughout, reports the favorable setting alongside it, and reports a near-inert setting where its method makes no difference at all. Code is released through an anonymous 4open.science repository, consistent with double-blind review.

## Measurement methodology

The dependent variable is **true validity `V` of the final committed plan**, adjudicated by each task's own ground-truth rule rather than by the verifier. The secondary variable is the mean number of repair rounds spent, `⟨K⟩`, which the authors note is also the cost ordering, since each round costs `M` verifier calls plus at most one repair call.

The controls are unusually careful for a paper of this kind, and I want to record the specific measures.

- **Cross-fitting.** All calibration parameters use five-fold cross-fitting, so no instance's stopping decision uses parameters estimated from its own label. In-sample calibration is reported only as a sensitivity audit.
- **Frozen trajectories and deterministic replay.** All numbers are computed by replaying saved trajectories rather than by regenerating. The authors state that per-instance LLM trajectories are single stochastic realisations and are not bit-wise reproducible across inference-engine versions. This means every strategy in the comparison tables is evaluated on the *same* instances and the *same* generations, which is what makes the paired tests meaningful.
- **Transition samples free of gating bias.** The labelled `α`/`β` pairs come from frozen trajectories in which every round triggered repair with no verifier gating, so the transition sample is not filtered by the acceptance signal. This directly supports the conditional-independence assumption the belief recursion needs.
- **Separate diagnostic estimator.** The test that decides whether to fall back to VRR-Guard compares acceptance rates on labelled samples directly, deliberately not using the binomial-mixture EM output, so a broken estimator is not asked to diagnose itself.
- **Offline scenario partition.** Scenarios are assigned to the calibrated mode or the fallback mode offline; `J_min` is not tuned online.

Significance is treated seriously rather than gestured at. Every headline percentage-point claim in the main text maps to a row of a paired-statistics table in Appendix G. Differences in true validity use 10,000 instance-level bootstrap resamples with 95 percent intervals, and directional binary comparisons use exact McNemar tests, all paired on the same instances and the same saved trajectories. Sample sizes are stated per window, and the main stress result uses N = 500 with an N = 200 replication and a three-disjoint-window replication reported in Appendix D.

Hyperparameter discipline is stated explicitly. Only two hyperparameters were tuned: the retention margin `δ` was swept over 0 to 8 by pure replay and set to 5, and the calibration sample size was examined at 50, 100, 200, and 300. The verification budget `M = 8`, the budget `K_max = 5`, and the threshold `τ = 0` were fixed a priori, and the authors say outright that systematic sweeps of `M` and `τ` were not run and are left to future work.

## Key findings

### 1. Repeated repair degrades true quality while reported acceptance rises

Across the eight settings in Table 5, six show true validity declining monotonically with the round index, one stays flat, and only the favorable setting improves. The measured damage probability `β` ranges from 0.615 to 0.938 and is typically several times the repair probability `α`. Because `b* = α / (α + β)`, this pushes the stopping boundary below 0.29 in most settings, and to 0.000 for Qwen-7B under stress, where the measured `α` is exactly zero: repair never fixed anything and broke 90.9 percent of what it touched.

Raw-label statistics on the N = 500 stress traces, which the authors stress are independent of any stopping rule, make the mechanism concrete. Round-1 validity of 0.70 drops to 0.25 after a single repair round. In 55 percent of instances, a correct plan is repaired into an incorrect one. In 24 percent of those damaging repairs, the damaged plan then wins majority acceptance from the eight judgments. The compounding of a repairer error with a verifier false acceptance is therefore not rare in this setting.

Appendix C.2 unfolds one instance (GSM8K #292) end to end, and the trace is the clearest single artefact in the paper. The initial plan correctly derives 75 dollars, but receives only 4 of 8 votes and suffers a false rejection. The repairer, working from the corrupted copy that says every 17 minutes instead of every 10 minutes, competently rewrites the plan into an answer of 40 dollars. The verifier, judging against the uncorrupted original, gives that wrong plan 6 of 8 votes and the loop commits it. True validity flips from 1 to 0 while reported acceptance rises from 4/8 to 6/8.

### 2. A stronger verifier reduces the risk but does not remove it

This is one of the paper's more useful negative results. On GSM8K with a process reward model verifier at `J = 0.805`, fixed five-round repair still drives validity from 0.727 down to 0.097. On MATH-500 at `J = 0.77`, it drives validity from 0.798 down to 0.150 while the true-parameter reference holds 0.798. The authors' reading is that verifier quality strengthens the *reliability of the stopping decision* but cannot eliminate the damage introduced by the repair operation itself, because `β` is a property of the repairer and not of the checker.

### 3. The degradation is path dependence, not sampling noise

The non-stationarity diagnostic runs a 256-token initial budget, so early repair genuinely helps by completing truncated drafts. Validity rises from 0.45 to 0.87 by round 2, and then collapses to 0.12 by round 6 after prompt mismatch is injected at round 3. The paired gain of the peak round over the final round is 74.7 points, with a 95 percent CI of [+69.3, +79.7]. The control matters here: an independent-resampling arm at the same budget stays between 0.47 and 0.85 throughout and shows no comparable decline. The damage therefore comes from repeatedly rewriting the *same* candidate, not from sampling variance.

### 4. The stopping rule beats every deployable baseline, and slightly beats its own oracle

On the GSM8K / Qwen2.5-3B stress setting at N = 500, the full baseline stratification (Table 6) is:

| Method | True validity `V` | `⟨K⟩` |
| --- | --- | --- |
| No repair | 0.700 | 0.00 |
| Majority stopping | 0.690 | 0.92 |
| Accepted-first | 0.690 | 0.92 |
| Verifier-best-of-trajectory | 0.696 | 0.73 |
| ConfStop-0.85 | 0.562 | 1.92 |
| Last-accepted | 0.504 | 2.28 |
| Fixed repair K = 1 | 0.246 | 1.00 |
| Fixed repair K = 3 | 0.122 | 3.00 |
| Fixed repair K = 5 | 0.116 | 5.00 |
| **VRR-Stop** | **0.722** | **0.72** |
| TPM reference (diagnostic) | 0.694 | 0.89 |

The headline claim is the +60.6 points over fixed five-round repair, 95 percent CI [+56.0, +65.0], McNemar significant. Three secondary readings are more interesting to me than the headline. First, fixed-budget repair gets monotonically worse with budget, so spending more compute buys strictly less validity. Second, every verifier-only heuristic converges to roughly the no-repair number, because the best thing a verifier signal can tell you in this regime is to leave the plan alone. Third, VRR-Stop's advantage over no-repair is only +2.2 points with a CI of [−0.004, +0.048] that contains zero, which the authors report honestly in Appendix G. The strong claim is therefore about avoiding catastrophic degradation, not about outperforming inaction.

VRR-Stop also slightly exceeds the true-parameter myopic reference, at +2.8 points. The authors explain why this is not a contradiction: the TPM reference is a diagnostic that isolates calibration error, and not a hindsight upper bound. Appendix F gives a direct counterexample, since on Mistral the TPM reference reaches 0.467 while no-repair reaches 0.507.

Under fixed-budget deployment on the same trajectories, Reflexion and Self-Refine reach 0.095 and 0.080, whereas VRR-Stop on those trajectories reaches 0.740 and 0.710. The authors qualify this comparison as an audit of the fixed-budget deployment mode rather than a reproduction of those methods' full training details.

### 5. Decision damage tracks verifier discrimination, not the size of the estimation error

This is the paper's most transferable claim, and the evidence for it is a genuine dissociation rather than a correlation.

- **Mistral-7B.** The calibration bias is enormous: `Δρ₀ = −0.66`. The cost is 0.3 percentage points, because the decision margin is large and the marginal gain stays on the same side of zero.
- **Llama-3-8B.** The calibration bias is smaller at `Δρ₁ = −0.53`, but `J` is only 0.03. Validity collapses from the reference 0.803 to 0.223, a loss of 58.0 points with CI [−63.7, −52.0].
- **BFCL single-call.** `J` is only 0.07, yet the visited states carry large margins, and VRR-Stop lands within 0.3 points of the reference.

The last bullet cuts against a naive reading of the paper's own thesis, and the authors say so: a trust threshold cannot be set from `J` alone, because margin can rescue a weak verifier. The controlled `J`–`Δ` sweep quantifies the joint dependence. Sign-flip probability reaches 0.183 where `J ≤ 0.15` meets `Δ ≤ 0.10`, against 0.014 where `J ≥ 0.4` or `Δ ≥ 0.30`, roughly a thirteen-fold gap.

Appendix A.4 and Appendix E locate the failure mechanism precisely, and this is the part of the paper I found most valuable. The binomial mixture is identifiable *if and only if* the two component acceptance rates differ, that is, if and only if `J ≠ 0`. As `J` approaches zero, the likelihood surface flattens and the estimator stops carrying information. Table 8 shows the pathological consequence: on Llama, EM gives `ρ̂₁ = 0.27` at N = 120, and *worsens* to 0.077 at N = 300 against a true value of 0.609. More data makes the estimator converge more confidently on a degenerate solution. Since calibrated stopping only recovers the correct behaviour for `ρ̂₁ ≳ 0.30`, the estimate sits deep in the collapse zone. This is a self-assessment failure that no amount of additional evidence-gathering repairs, because the evidence channel itself has no signal in it.

### 6. The estimation-free fallback contains the damage

Across all seven settings, VRR-Guard stays near the no-repair level and never collapses, whereas fixed five-round repair degrades sharply in every setting but the favorable one. In the Llama setting where calibrated stopping fails, VRR-Guard recovers 0.793 against the failed VRR-Stop's 0.223, a gain of 57.0 points, and 73.7 points over fixed five-round repair. Against the margin-free Verifier-best policy on the same trajectories, Guard is 45.0 points higher on Llama and between −4.0 and +8.0 points elsewhere, so the retention margin `δ` is nearly neutral in general and earns its value exactly where the verifier signal is least trustworthy.

The authors report the costs of this conservatism under a heading they title "Honest boundaries." In the favorable setting, Guard reaches 0.810 against 0.875 for fixed five-round repair, which is the price of not repairing when repairing would have helped. Guard falls below no-repair by 2.0 points on Mistral and 0.3 points on BFCL, and the BFCL paired interval contains zero. They state explicitly that VRR-Guard has no theoretical guarantee of dominating no-repair.

### 7. A negative control exists

BFCL multi-turn has a near-inert repair operator with `α = 0.02` and `β = 0.04`. There, all strategies coincide within confidence intervals. The authors use this to bound their own claim: multi-round repair is not inherently harmful, and severe degradation appears only together with a substantial capacity to break correct states.

## Open questions the paper itself raises

The paper is notably forthcoming about its own limits, and most of these come from Appendix H rather than from a token limitations paragraph.

1. **Round-dependent dynamics.** The four parameters are assumed locally stationary, but the paper measures them drifting. In the favorable setting, the per-round repair success rate falls from 0.415 in round one to 0.032 in round five, with the natural interpretation that the easy errors are fixed first. Estimating `α` and `β` from round one is therefore a local approximation, and the authors call for modelling round-varying `α_t` and `β_t`.
2. **The myopic rule cannot find interior peaks.** This is the most consequential admission. The rule compares committing now against exactly one more round, with no look-ahead over trajectories. On the non-stationarity diagnostic, VRR-Stop and the TPM reference reach 0.693 and 0.720, both far below the 0.867 available from post-hoc selection of round two. The paper's own showcase of an interior optimum is a case its method does not capture.
3. **Binary validity is too coarse.** True validity is a single bit. The authors state that this does not describe partial correctness, distinct error types, or long-horizon plans with staged goals, and that for such tasks the stopping boundary may not be a single threshold.
4. **Online mode switching is not solved.** Scenarios are partitioned offline by a held-out labelled diagnostic. Algorithm 1 shows an intended online switch into Guard mode, but the experiments evaluate the two modes separately on saved trajectories. Future work is to switch online.
5. **Deterministic verifiers break the calibration channel.** A deterministic verifier such as an executor returns the same answer to repeated queries, so the repeated-vote binomial mixture cannot be applied. The stopping criterion still holds, but `ρ₀` and `ρ₁` must then come from labelled samples.
6. **`α + β ≤ 1` is violated in the headline setting.** The paper states that this strict condition holds on seven of eight trajectories but is clearly violated on the GSM8K stress trajectory of Qwen2.5-3B, so conclusions there rest on single-round marginal gains rather than global monotonicity.
7. **Family-conditional verifier failure is observed but not explained.** Qwen judges consistently underestimate false acceptance, Llama underestimates false rejection, and Mistral tends heavily toward false acceptance. The authors explicitly refuse to generalise from three families, and note that some configurations share tasks and samples.
8. **Unswept knobs.** No systematic sweep of the verification budget `M` or the gain threshold `τ` was run.
9. **Instance-conditional noise.** The model assumes noise rates are constant within a class, but the same verifier errs at different rates on plans of different difficulty. A beta-binomial estimator is used to diagnose that heterogeneity, and a per-instance stopping boundary is proposed as future work.
10. **Per-instance budget allocation.** They suggest using per-instance marginal gains to allocate a fixed total inference budget across tasks, selecting the instances most worth repairing.

## Appreciation

I want to keep the mechanism separate from the magnitude, because they carry very different amounts of weight here.

### Mechanism — strong, and largely portable

The mechanism is the durable contribution, and most of it is arithmetic that stands independently of these experiments.

The decomposition `G = (1 − b) α − b β` is the kind of result that reads as obvious once written down and was not obvious before. It says that the question "should I keep working on this?" has exactly two inputs beyond your current confidence: how often further work fixes broken things, and how often it breaks working things. It explains immediately why a fixed round budget can never be safe, since the crossing point `b* = α / (α + β)` is measured at 0.954 in the favorable setting and 0.289 in the stress setting. The same confidence level therefore means "continue" in one deployment and "stop" in another, so no universal confidence threshold transfers.

The separation of the verifier's two error directions from the repairer's two behaviours is clean and I think correct. It explains why "get a better checker" is an incomplete remedy: `ρ₀` and `ρ₁` control how well you can *locate* yourself, while `α` and `β` control whether moving is worth it. The PRM result at `J = 0.805` still collapsing under fixed repair is the empirical payoff of that separation.

The sign-identifiability framing is the part I would carry furthest. Reframing "is my self-assessment accurate?" into "is my self-assessment accurate enough to not flip this particular decision?" converts an unanswerable calibration question into a checkable one, and gives a principled account of why a badly miscalibrated system can still act correctly (Mistral) while a mildly miscalibrated one collapses (Llama). Proposition 1 is trivial as mathematics, and I do not think the authors pretend otherwise; its value is that it names the right quantity.

The identifiability collapse at `J → 0` is the best-diagnosed failure in the paper. The mixture is identifiable exactly when the two components differ, so a verifier with no discrimination leaves the estimator with a flat likelihood surface, and more samples make it *more* confidently wrong. This is a precise account of a system that cannot tell that it cannot tell.

The design of the fallback also deserves credit for what it declines to do. Facing a regime where its own estimates are worthless, the method does not attempt a cleverer estimate. It switches to an ordinal comparison of raw vote counts with a margin, keeps the incumbent, and accepts a known opportunity cost. Using a *separate* labelled test to trigger the fallback, rather than asking the suspect estimator to assess itself, is the right instinct.

### Magnitude — narrow, and to be quoted with care

The magnitudes are much more setting-specific than the mechanism, and I would not carry them far.

The 60.6-point headline is a comparison against fixed five-round repair inside an adversarial construction the authors built, where the repairer reads a deliberately corrupted problem statement at temperature 1.0. That construction produces `β` values from 0.615 to 0.938, which is a repairer that breaks correct work most of the time it touches it. Whether real deployed repair loops sit anywhere near that regime is not established by this paper, and the favorable setting (`β = 0.020`) and BFCL multi-turn (`β = 0.04`) show that they need not.

The more defensible framing of the same number is that VRR-Stop's advantage over *doing nothing* is +2.2 points with an interval containing zero. The method's demonstrated value is that it avoids catastrophe, not that it extracts gains. Its mean cost of 0.72 repair rounds against a budget of 5 is a real and well-measured efficiency claim, but it is largely the cost of learning not to act: in the Qwen-7B setting the method converges on zero repair rounds.

The scale is also small throughout. Models run from 3B to 8B parameters, and the verifier is usually the generator judging itself. Evaluation windows run from 150 to 500 instances. The three model families sometimes share tasks and samples. Within those bounds the statistics are handled well — pairing, cross-fitting, McNemar, bootstrap intervals, replications on disjoint windows — so the numbers are trustworthy *about these settings*. They are simply about a small corner.

## How this could serve a harness-design effort, and its limitations

### What is directly usable

The most immediately usable idea is that a loop's stopping policy should be driven by a comparison between the benefit of another attempt and the risk of damaging what already works, rather than by a round budget or a confidence threshold. A harness that runs verify-and-fix cycles could measure its own `α` and `β` offline for a given task family and repair prompt, and derive `b*` from them. That single number tells the harness the confidence level above which further work is expected to destroy value. The paper's own measurements show that this number is not portable, which is itself the actionable finding: it must be measured per model, per verifier, per task, per repair prompt.

The second usable idea is the diagnostic ordering. Before trusting any self-assessment-driven stopping rule, measure the verifier's discrimination `J` on a small labelled set. If it is near zero, no estimation-based rule can be trusted, however much data is collected, and the harness should fall back to something ordinal. The paper's Llama case is a clean demonstration that additional calibration data can make things worse in that regime.

The third is keep-best with a margin. It is cheap, it requires no parameter estimation, and it converts an unreliable stopping decision into a bounded one. A harness that keeps the best-scoring artefact seen so far, and replaces it only under a clear margin, commits that incumbent instead of whatever the last iteration happened to produce. Lemma 1 gives that margin an analytic basis, and Appendix A.3's exact tails suggest the Hoeffding bound is very loose in practice.

The fourth is a design principle I would take even without the machinery: **the trigger for a safety fallback must not be computed by the component the fallback distrusts.** The paper's held-out separation test is the concrete instance.

### Limitations that matter for that use

The stress setting is adversarial by construction, so the headline magnitudes should not be treated as a forecast of what a harness would recover in normal operation. The negative control at `β = 0.04` shows that a benign repair operator makes every stopping policy equivalent, which means the method's value is entirely conditional on the repairer actually being dangerous.

The myopic one-step rule cannot find interior optima, and the paper demonstrates that on its own diagnostic, with a 17-point gap to post-hoc round selection. Any harness that expects quality to rise then fall — which is the interesting case for a long-running loop — is not served by this rule as stated.

The binary validity state is a hard limit for real harness work. Most agent tasks are partially correct in structured ways, and this framework has no way to express "the plan is right but one tool call is wrong," which is exactly the situation where targeted repair is safest.

The calibration cost is real: up to 300 labelled transition pairs per configuration, and the paper warns that parameters must not be transferred across model families, verifiers, or even repair prompts. That is a recalibration burden every time anything in the loop changes, and it is the sort of burden that quietly does not get paid in practice.

Finally, the whole framework assumes the verifier can be queried repeatedly with stochastic variation, which is how `M = 8` votes become a binomial. Deterministic checks such as test suites and executors — the checks a harness most often has — break that assumption, and the paper says so.

### Major concerns

My main methodological concern is the reliance on a single self-designed perturbation, prompt mismatch, to produce nearly all the dramatic numbers. It is a legitimate stress test and it is honestly labelled, but it is one failure mode, and the paper's strongest claims about the prevalence of harmful repair rest on it. The claim that "harmful repair is the rule rather than the exception" is supported for stress conditions of the authors' own construction, and the paper's own favorable and BFCL-multi rows are the counterexamples.

A second concern is that VRR-Stop's margin over no-repair is not statistically distinguishable from zero on the headline setting, while the abstract leads with the 60.6-point comparison against a baseline that the paper elsewhere shows to be strictly dominated by doing nothing. Both numbers are reported, and Appendix G is scrupulous, so this is a framing issue rather than a soundness issue.

A third concern is that the paper is a preprint under review and has not been refereed, and its central artefact is an anonymous code repository that I have not inspected.

## Five citations worth chasing next

1. **Kamoi, Zhang, Zhang, Han, and Zhang (2024b), "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs," TACL 12: 1417–1440.** A peer-reviewed survey framed around exactly the conditional question this paper answers with two parameters. It should give the broader empirical base on when self-correction helps and when it corrupts.

2. **Dorner, Chen, Cruz, and Yang (2026), "ROC-n-reroll: How Verifier Imperfection Affects Test-Time Scaling," ICLR.** The closest analytic neighbour on the verifier side. It analyses how an imperfect verifier limits resampling, whereas this paper handles path-dependent rewriting; comparing the two would separate what is intrinsic to verifier noise from what is intrinsic to rewriting the same candidate.

3. **Stroebl, Kapoor, and Narayanan (2026), "The Limits of Inference Scaling Through Resampling," ICLR.** The general upper-bound result on how far imperfect verification can carry test-time compute. This is the ceiling argument that VRR-Stop's whole premise operates beneath.

4. **Collot, Fraser, Zhao, Shen, Willi, and Leontiadis (2026), "Balanced Accuracy: The Right Metric for Evaluating LLM Judges — Explained through Youden's J statistic," EACL Industry Track.** The source of the `J` machinery that carries the identifiability argument here. Worth reading directly, since the entire trust-versus-fallback boundary is expressed in this one statistic.

5. **Sun, Cheng, Li, Chen, and Wang (2026), "Stop When Enough: Adaptive Early-Stopping for Chain-of-Thought Reasoning," ACL (arXiv:2510.10103).** The nearest work that treats stopping itself as a decision dimension, but for single-pass generation rather than for a loop with true-state transitions. It is the natural comparison point for what a stopping rule looks like without a damage term.

*(Two honourable mentions, both directly on the Subject: Huang et al. (2024), "Large Language Models Cannot Self-Correct Reasoning Yet," ICLR, which is the canonical negative result behind the `β` term; and Ye et al. (2025), "Uncertainty-Aware Step-wise Verification with Generative Reward Models," which flags unreliable verifier steps rather than modelling them.)*
