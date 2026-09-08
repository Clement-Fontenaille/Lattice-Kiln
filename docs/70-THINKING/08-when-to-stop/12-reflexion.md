# Reflexion: Language Agents with Verbal Reinforcement Learning

## Density

**Density: HIGH** — The paper is short and most of it is load-bearing: the loop is specified concretely, the evaluator is instantiated three different ways across three task families, and the ablations and the false-positive analysis speak directly to the Subject; the padding is confined to the appendix prompt dumps.

## Name, keywords, year, venue

**Name.** Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao. "Reflexion: Language Agents with Verbal Reinforcement Learning."

**Keywords (mine):** verbal reinforcement, self-reflection, episodic memory buffer, actor-evaluator-reflector loop, self-generated unit tests, retry loop, stagnation heuristic, false-positive stopping, credit assignment in natural language.

**Year:** 2023 (arXiv v1 March 2023; this review reads v4, dated 10 October 2023).

**Venue:** NeurIPS 2023. Peer-reviewed.

**Authors:** Noah Shinn, Federico Cassano, Edward Berman (Northeastern University), Ashwin Gopinath (MIT), Karthik Narasimhan, Shunyu Yao (Princeton).

## Approach

Reflexion is a retry loop that carries written lessons between attempts instead of updating model weights. The authors decompose the agent into three separately prompted models:

- **Actor** (`M_a`) generates the text and the actions, conditioned on the state observations plus a memory `mem`. They instantiate it as Chain-of-Thought or as ReAct depending on the task.
- **Evaluator** (`M_e`) takes a finished trajectory and returns a scalar or binary reward score. This is the component that decides whether the attempt counts as done.
- **Self-Reflection** (`M_sr`) reads the pair `{trajectory, reward}` and writes a natural-language post-mortem naming what went wrong and what to do differently.

The policy is defined as `θ = {M_a, mem}` — that is, the LLM parameters are frozen and the only thing that changes across trials is the memory. The reflection text is appended to `mem`, which is a bounded sliding window of the last Ω experiences, with Ω "usually set to 1-3" to stay inside the context limit. Trajectory history serves as short-term memory; the reflections are the long-term memory.

The authors frame the reflection as amplification: the reward `r_t` is a thin scalar, and the self-reflection model converts it into a richer verbal signal that acts as a "semantic gradient" giving the actor a direction to move in. The stated advantages are that it needs no fine-tuning, that it allows credit assignment in language rather than through a scalar, and that the memory is explicit and interpretable. The stated disadvantages, given in the introduction, are that it "relies on the power of the LLM's self-evaluation capabilities (or heuristics)" and has "no formal guarantee for success."

**The loop as printed (Algorithm 1).** Initialise the three models; generate an initial trajectory; evaluate it; generate an initial reflection; seed `mem` with it; set `t = 0`; then `while M_e not pass or t < max trials do` — generate trajectory, evaluate, reflect, append to `mem`, increment `t`. Two things are worth recording precisely. First, the outer stopping condition is a disjunction of an evaluator pass signal and a trial cap, so termination is governed jointly by "the evaluator said this is correct" and "we ran out of budget" (the printed `or` reads as a typo for `and`, since as literally written the loop would not exit on an evaluator pass while under the cap; the prose says the models "work together through trials in a loop until the Evaluator deems `τ_t` to be correct"). Second, there is no separate "abandon" or "hand off" branch — the only exits are pass and exhaustion.

## Models targeted

GPT-3 and GPT-3.5 (`gpt-3.5-turbo`), `text-davinci-003`, and GPT-4 for the main results. Appendix A adds `starchat-beta`, an open smaller model, specifically to test whether the method survives a weaker actor.

## Benchmarks and datasets

- **Sequential decision-making:** ALFWorld, 134 environments across six household task types, with ReAct as the actor.
- **Reasoning:** HotPotQA, 100 questions, with both CoT (including a ground-truth-context variant, "CoT (GT)") and ReAct actors.
- **Programming:** HumanEval and MBPP in Python, plus Rust translations produced with the MultiPL-E compiler suite (the Rust HumanEval set is the 50 hardest problems), and **LeetcodeHardGym**, a benchmark they introduce: 40 Leetcode hard-rated questions across 19 languages, all released after GPT-4's 8 October 2022 pre-training cutoff.
- **Negative case:** WebShop, 100 customer shopping requests (Appendix B.1).

## Author incentive

Academic, spread across three universities (Northeastern, MIT, Princeton); the HTML carries no funding or acknowledgements statement. The intellectual stake is in establishing "verbal reinforcement" as a paradigm — the framing is explicitly RL-analogous (policy, reward, credit assignment, episodic memory) and the conclusion proposes importing more classical RL machinery next. Two artefacts are staked as contributions: the open-source repository and the LeetcodeHardGym benchmark. The Princeton co-authors are the ReAct authors, and ReAct is the actor and the principal baseline throughout, so the paper is in part an extension of their own prior system. The headline claim ("91% pass@1 on HumanEval, surpassing GPT-4's 80%") is a state-of-the-art claim, and the related-work section is organised as two feature-checkbox tables in which Reflexion is the only row with every box ticked.

## What decides that a trial has failed — the three instantiations

The single most Subject-relevant fact about this paper is that the evaluator is a *different mechanism in each task family*, and the paper is candid that this is because a general one is hard to build. The method section says outright that "defining effective value and reward functions that apply to semantic spaces is difficult, so we investigate several variants of the Evaluator model."

**ALFWorld — heuristics over the trajectory, plus an LLM classifier.** The authors note that ALFWorld "naturally requires a self-evaluation step as the environment can only signal if a task is complete" — that is, the environment emits success but never emits failure, so something else has to decide when to give up on the current attempt. They implement two such deciders and run them as separate arms. The first is an LLM doing binary natural-language classification of the trajectory. The second is a hand-written heuristic that reads the trajectory shape rather than the content: *if the agent executes the same action and receives the same response for more than 3 cycles, or if the number of actions in the environment exceeds 30 (which they call inefficient planning), then self-reflect.* This is a stagnation-and-budget detector, and it is entirely external to the model's opinion of its own work. When it fires, the baseline arm resets the environment and starts a fresh trial with no memory; the Reflexion arm reflects, writes to memory, then resets. Memory is truncated to the last 3 reflections.

**HotPotQA — an external oracle.** Between trials the authors "use exact match answer grading using the environment to give a binary success signal to the agent." The evaluator here is ground-truth string matching, not a judgement the agent could make for itself; the self-reflection step then amplifies that binary bit. Memory size 3. The retry loop's stopping rule here is neither a plain pass signal nor a plain trial cap but a patience rule: the agent is allowed "to gather experience and retry on failed tasks until it produced 3 consecutive failed attempts on the particular task." So three strikes ends the episode. Note the exact scope of the paper's claim that "Reflexion helps the agent to correct its mistakes without access to the ground truth answer": the *reflection text* is not shown the answer, but the *pass/fail bit driving the loop* is computed from it.

**Programming — self-generated tests as a proxy oracle.** This is the only setting where the stop signal is generated by the system itself and is still grounded in execution. The agent writes its own test suite: chain-of-thought prompting produces candidate tests with natural-language descriptions, they are filtered for syntactic validity by attempting to build an AST for each, and up to n = 6 are sampled into the suite T. Because no hidden or ground-truth tests are consulted, the authors argue the setup remains eligible for pass@1 reporting. Memory limit here is 1 experience. The loop stops when the self-written tests pass — which means the correctness of the stopping decision is bounded by the quality of tests the model wrote for itself.

## Measurement methodology

The dependent variable is task success rate: cumulative proportion of the 134 ALFWorld tasks solved as a function of trial number, accuracy on 100 HotPotQA questions across learning steps, and pass@1 accuracy on the coding benchmarks. The controlled comparison is consistently "the same actor with and without the Reflexion machinery" — ReAct vs ReAct + Reflexion, CoT vs CoT + Reflexion — with the few-shot prompts held to the same ones used by the ReAct paper, and HotPotQA run at temperature 0.7.

N is small and stated: 134 ALFWorld environments, 100 HotPotQA questions, 100 WebShop requests, 40 LeetcodeHard problems, 50 hardest problems for the Rust ablation. Significance is essentially not treated: the main tables report single point estimates with no confidence intervals, no error bars, and no hypothesis tests. The one exception is Appendix A's starchat-beta table, which averages pass@1 over 8 trials and reports a standard deviation. Trial-count budgets differ by task (12 trials for ALFWorld, 3-consecutive-failures for HotPotQA, an unstated cap for programming, 4 trials before manual termination on WebShop), so "performance" is a curve against a task-specific budget rather than a single controlled quantity.

Table 2 is the most methodologically interesting instrument in the paper, because it measures the *evaluator* rather than the actor. It cross-tabulates whether the self-written tests passed against whether the solution was actually correct, giving TP / FN / FP / TN rates, and from these the quantity the analysis leans on: P(submission is wrong | all internal tests pass) — the rate at which the loop stops satisfied while being wrong.

## Key findings

**Headline magnitudes.** Reflexion improves over the corresponding baseline by an absolute 22% on ALFWorld, 20% on HotPotQA, and up to 11% on HumanEval. ReAct + Reflexion completes 130 of 134 ALFWorld tasks using the simple stagnation heuristic, and keeps improving across all 12 trials, whereas the ReAct-only agent's improvement halts between trials 6 and 7. On the coding table: HumanEval Python 91.0 pass@1 against a GPT-4 baseline of 80.1; HumanEval Rust 68.0 against 60.0; MBPP Rust 75.4 against 70.9; Leetcode Hard Python 15.0 against 7.5. The one loss is **MBPP Python, 77.1 against the GPT-4 baseline's 80.1** — Reflexion makes the agent worse there, and the authors investigate rather than bury it.

**Retry without reflection does essentially nothing on reasoning.** On HotPotQA the ReAct-only, CoT-only and CoT (GT)-only baselines "fail to probabilistically improve on any tasks" — the authors state that no task failed on the first trial by any baseline was solved on a later trial at temperature 0.7. Plain resampling did not rescue anything; the memory of what went wrong is what produced the gain.

**Reflection beats bare episodic memory.** The HotPotQA ablation isolates this. Starting from CoT (GT), they add episodic memory alone (the most recent trajectory is included in the context) and then add the self-reflection pass on top. Self-reflection is worth an **8% absolute** boost over the episodic-memory-only condition. Their reading: "refinement-only approaches are not as effective as self-reflection-guided refinement approaches."

**The programming ablation (Table 3, HumanEval Rust, 50 hardest, GPT-4) is the most directly Subject-relevant result in the paper.** Four conditions:

| Condition | Test generation | Self-reflection | Pass@1 |
|---|---|---|---|
| Base model | no | no | 0.60 |
| Test generation omitted | no | yes | **0.52** |
| Self-reflection omitted | yes | no | 0.60 |
| Full Reflexion | yes | yes | 0.68 |

Two separate lessons sit in that table. First, removing the grounded evaluator makes the agent *worse than not iterating at all* — 0.52 against a 0.60 baseline. The authors' explanation is explicitly about the stopping decision: without unit tests "the agent is unable to determine if the current implementation is correct," and therefore "must participate in all iterations of the run without the option to return early, performing harmful edits to the implementation." An iterative loop with no valid stop signal does not merely waste budget; it actively damages already-correct work. Second, removing the reflection while keeping the tests recovers nothing — 0.60, exactly the baseline. They observe that test execution and compilation do catch the syntax and logic errors, but "the implementation fixes do not reflect these indications," and conclude that "blind trial and error debugging techniques without self-reflection are ineffective on harder tasks." So the two components do different jobs and neither substitutes for the other: the executable check decides *whether to stop*, and the reflection decides *what to change*.

**The MBPP Python regression is a false-positive stopping failure.** Baseline pass@1 on HumanEval Python and MBPP Python are similar (82% and 80%), so the difference in Reflexion's outcome is not actor quality — it is evaluator quality. The false-positive rate of the self-written test suites is **1.4% on HumanEval Python but 16.3% on MBPP Python**. The authors lay out the asymmetry cleanly: a false negative (tests fail on correct code) is the tolerable error, because the agent may reflect its way to recognising the test is wrong and keep the original implementation; a false positive (all tests pass on incorrect code) is the damaging one, because "the agent will prematurely report an invalid submission." They cite the flaky-test literature for this. In Subject terms: the loop's failure mode is stopping too early with unwarranted confidence, and the rate of that failure is a property of the self-generated oracle, not of the reasoning.

**Self-evaluation appears to be capability-gated.** Appendix A reports that on HumanEval Python with `starchat-beta`, baseline and Reflexion both score 0.26 — the method yields exactly nothing on the weaker model. The authors conclude that "the ability to specify self-corrections is an emergent quality of stronger, larger models." Table 5 shows the gain does hold across `text-davinci-003`, `gpt-3.5-turbo` and `gpt-4` on HotPotQA (e.g. ReAct + `text-davinci-003` 0.30 to 0.55; CoT (GT) + gpt-4 0.68 to 0.80), so the cliff is below that class of model rather than being a smooth scaling trend.

**A qualitative failure mode Reflexion fixes.** In baseline ALFWorld failures a common error is that the agent believes it holds an item that it does not actually hold, then executes a long trajectory on that false premise and cannot backtrack to locate the mistake. The ReAct-only agent converges to a 22% hallucination rate "with no signs of long-term recovery." Reflexion removes nearly all of these by distilling the failed trajectory into a self-hint. The worked example in Appendix B is instructive about what the reflection actually contains: the agent notices that it ordered its subgoals wrongly (mug before desklamp) and writes a corrected plan for the next trial, and the retry succeeds in far fewer actions.

**The WebShop negative result (Appendix B.1).** A two-shot ReAct + Reflexion agent on 100 WebShop environments does not improve, and the authors "terminate the runs after only four trials as the agent does not show signs of improvement." Crucially, they report that the agent "does not generate helpful, intuitive self-reflections after failed attempts" — the reflection machinery degrades silently rather than announcing that it has nothing useful to say. Their diagnosis is that Reflexion "is unable to solve tasks that require a significant amount of diversity and exploration": ALFWorld works because the permissible actions are visible in the observations, HotPotQA works because Wikipedia search tolerates imprecise queries, while e-commerce search demands precise and creative query formulation. Note also that the loop did not terminate itself here — a human ended it.

## Open questions the paper itself raises

- **Local minima.** The limitations section frames Reflexion as natural-language policy optimisation and concedes it "may still succumb to non-optimal local minima solutions." WebShop is the demonstration. Nothing in the loop detects that it is stuck in one.
- **Memory structure.** Long-term memory is a sliding window with maximum capacity Ω (1-3), chosen for context-length reasons. They explicitly invite future work to replace it with vector embedding databases or SQL databases.
- **Limits of test-driven self-evaluation.** They enumerate cases where writing accurate input-output tests is not possible in principle: non-deterministic generator functions, impure functions that call APIs, functions whose output varies with hardware, and code invoking parallel or concurrent behaviour. These are precisely the cases where the programming setting's grounded stop signal would be unavailable.
- **No formal guarantee.** Stated in the introduction: the approach depends on the LLM's self-evaluation capability or on hand-written heuristics, and offers no guarantee of success. Their stance is that this will improve as models do.
- **Importing more RL machinery.** The conclusion proposes value learning in natural language and off-policy exploration as next steps.
- **Interpretability as a safety affordance.** The broader-impact section suggests self-reflections could be monitored to check an agent's intent before it uses a tool — offered as a possibility, not studied.

## Appreciation

### Mechanism

The durable contribution is the *separation of the three roles*. Deciding that an attempt is over, diagnosing why it failed, and producing the next attempt are given to three distinct prompted models with distinct inputs, and the ablation shows they are not interchangeable. That separation is what makes the paper informative about the Subject: it lets you see that a loop can have a working critic and still not improve (self-reflection omitted, 0.60), and a working reflector and still get worse (test generation omitted, 0.52).

Second, the paper is unusually explicit that the *stop signal is the load-bearing part and is the part they could not make general*. Three tasks, three different evaluators — a stagnation heuristic, a ground-truth string match, and a self-written test suite — with the choice each time driven by what the environment happens to make checkable. The heuristic used in ALFWorld is worth isolating, because it is the one signal in the paper that reads the trajectory's shape rather than its content: repeat-action-with-repeat-observation for more than 3 cycles, or more than 30 actions. It requires no model judgement, no ground truth, and it is what carried the arm that solved 130 of 134 tasks.

Third, Table 2's decomposition of the stop decision into TP/FN/FP/TN, and the asymmetry argument that follows, is a transferable framing: a self-evaluator's error rate matters *directionally*, because a false negative costs iterations while a false positive ends the loop wrongly.

Fourth, the memory is a real design choice and not incidental. The policy is `{frozen model, memory}`; the reflections are written in the first person and persist across environment resets; the buffer is bounded to 1-3 entries. The HotPotQA ablation shows the content of that memory (a reflection) matters more than its mere presence (a prior trajectory).

### Magnitude

The gains are large but the evidence base is thin, and the two should be held apart. N is 100-134 for the non-coding tasks; there are no error bars, no confidence intervals and no significance tests anywhere in the main results; the only variance reported in the paper is in an appendix table for the model where the method did not work. Baselines are the authors' own prior system. The trial budgets differ per task and are set by hand. The 91% HumanEval figure is a single number against a single-sample GPT-4 baseline. The 8% and 22% figures are single-run differences on datasets of a hundred items, so a few items' movement is the whole effect. The direction of the ablation results is convincing because it is a coherent pattern across four conditions and is corroborated by an independently measured mechanism (the false-positive rate explaining the MBPP regression); the exact magnitudes should not be quoted as precise.

Also worth keeping straight: two of the three headline settings use an evaluator that would not exist in deployment. HotPotQA's pass signal is exact match against the dataset's answer. ALFWorld's environment emits task completion. Only the programming setting has a stop signal the system generates for itself end to end — and that is the setting where the method loses to its baseline on one benchmark, for exactly the reason of stop-signal quality.

## How it could serve a harness-design effort — limitations and concerns

**What transfers.** The finding that a retry loop *without* a valid completion check performs below no retrying at all is the strongest practical result here, and it is the one a harness designer should carry: iteration is not free-rolling upside, and the failure is not just wasted budget but "harmful edits" to work that was already correct. Consequently, a harness should be able to tell the difference between "no check is available" and "the check passed," and should probably decline to iterate in the former case rather than iterate blindly. The complementary finding — that a check without a diagnosis also yields nothing — argues that a harness surfacing raw failure output to a retry is not enough; something has to convert the failure into a stated lesson before the next attempt. The ALFWorld heuristic is a cheap, model-independent stall detector worth having regardless of what else is in the loop: no state change across repeated actions, and an action-count ceiling.

**Limitations for that purpose.**

- *Stopping is pass-or-exhaust only.* The algorithm has no abandon, escalate or hand-off branch, and no notion of "this is beyond me." The one time the loop genuinely could not make progress (WebShop) a human stopped it at four trials. The paper offers no signal for that state, and in fact reports that the reflections themselves became unhelpful there — so the reflection channel cannot be relied on to announce its own uselessness.
- *No calibration content.* Nothing in the paper measures whether the agent's confidence tracks its accuracy, and there is no abstention behaviour. The closest thing is the FP/FN table, and that is a property of generated tests rather than of a stated confidence.
- *The evaluator has to be built per task.* The paper does not offer a general recipe; it offers three worked instances and the observation that semantic reward functions are hard. A harness that wants one stopping mechanism across heterogeneous tasks does not get it here.
- *Self-generated tests inherit a measured false-positive rate that varies by benchmark* — 1.4% to 16.3% across two Python benchmarks of comparable baseline difficulty. That variance is unpredictable in advance, and it is the difference between the method's best result and its only regression.
- *Capability floor.* On `starchat-beta` the entire method is worth zero. Anything built on self-reflection needs to know which models it is above the floor for.
- *Memory is a 1-3 entry sliding window*, so lessons are forgotten quickly and there is no mechanism preventing a bad reflection from persisting or a good one from being evicted.
- *Local minima are acknowledged and undetected.* The loop cannot tell that its reflections have stopped adding information.

**Concerns about the evidence.** Single runs, small N, no significance treatment, self-authored baselines, per-task hand-tuned budgets and prompt counts, and a headline claim resting on one benchmark number. The v4 ALFWorld and HotPotQA setups also carry a slightly awkward property: the "self-evaluation" arm on ALFWorld is compared within the same figure as the heuristic arm, and it is the heuristic — the least model-dependent component — that produces the 130/134 result.

## Five citations worth chasing next

1. **Madaan et al., "Self-Refine: Iterative refinement with self-feedback" (2023)** [15] — the nearest neighbour: iterative self-evaluation and self-improvement without an external signal and without persistent memory, which is exactly the condition Reflexion's ablation says underperforms.
2. **Chen et al., "CodeT: Code generation with generated tests" (2022)** [5] — self-generated tests used to score implementations, the direct antecedent of Reflexion's proxy oracle, and the prior SOTA row in Table 1.
3. **Chen et al., "Teaching large language models to self-debug" (2023)** [7] — execution-feedback debugging without a reflection step, i.e. approximately the "self-reflection omitted" ablation condition as a standalone system.
4. **Lam et al., "A large-scale longitudinal study of flaky tests" (2020)** [11] — the empirical grounding for the false-positive analysis, and the place to look for how badly a test-based stop signal can misreport.
5. **Xie et al. (2023)** [27] — stochastic beam search over actions using a self-evaluation component for foresight; the checkbox table lists it as the only prior work with hidden constraints, decision-making and binary reward, differing from Reflexion only in lacking memory.
6. **(bonus) Kim et al., "Language models can solve computer tasks" (2023)** [10] — cited as using "a retry pattern over a fixed number of steps without an evaluation step," which is the pure fixed-cap stopping baseline.
