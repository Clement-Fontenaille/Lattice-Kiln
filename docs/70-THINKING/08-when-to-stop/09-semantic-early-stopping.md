# Semantic Early-Stopping for Iterative LLM Agent Loops

## Density

**Density: MEDIUM-HIGH.** The paper is short and most of it is load-bearing: the halting cascade, the replay-and-cache evaluation protocol, the proven-versus-conjectured split, and the oracle gap are all substantive, and every one of them speaks directly to the Subject. What dilutes it is a per-paper related-work appendix that is largely positioning rather than evidence, a scale (N=60, one 8B model, one benchmark) far below what the headline claims would need, and a recurring self-congratulatory framing of its own honesty.

## Name, keywords, year, venue

- **Title.** "Semantic Early-Stopping for Iterative LLM Agent Loops: A Judge-Efficient Study of When to Halt."
- **Author.** Sahil Shrivastava. Affiliation given only as "Semantic Halting Problem (SHP) Project" — that is, a self-named project, not an institution.
- **Year / venue.** arXiv:2606.27009v1 [cs.AI], 25 June 2026. Preprint, not peer-reviewed. IEEE-style formatting (Index Terms, Roman-numbered sections) suggests it was written for a conference or journal submission but no venue is claimed.
- **My keywords.** Agentic stopping rule; embedding-distance convergence; patience window; quality plateau gating; halt cascade; trajectory replay; judge caching; operational versus evaluation tokens; oracle best-round gap; non-inferiority (TOST); Writer-Critic loop; HotpotQA; RAGAS.

## Approach

The paper attacks one narrow decision: when a Writer-Critic loop should stop. The standard answer is a fixed `max_iterations` counter, which the author calls a "syntactic kill-switch" — it decides on the iteration index and never on what was written, so it overspends on easy inputs and truncates hard ones.

The replacement is a content-aware rule built from two signals plus two guards, evaluated as a fixed-priority cascade.

The **geometric signal** is free of API cost. Each draft `x_t` is mapped by a frozen local sentence-embedding model `φ` into a 384-dimensional L2-normalised vector, and the per-round semantic distance is the cosine distance to the previous draft, `d_t = 1 - cos(e_t, e_{t-1})`, defined for `t >= 2` and bounded in `[0,2]`. The loop declares semantic convergence when `d_t` stays below a threshold `ε` for `k` consecutive rounds. That `k` is the patience window, and the paper is explicit about why it exists: the descent of `d_t` is real on average but noisy per round, so a single lucky sub-threshold round must not be allowed to fire the halt.

The **quality signal** is a separate criterion and costs API tokens. A RAGAS-style judge scores each draft on four metrics in `[0,1]` — faithfulness, answer relevancy, context precision, context recall — and these are combined by weights `w` on the probability simplex into a scalar Information Score, `IS_t = Σ_m w_m · metric_m(x_t)`, also in `[0,1]`. The weights are not hand-set; they come from one of four selectable strategies (label-free Shannon entropy weighting, an Analytic Hierarchy Process with a consistency check, a constrained least-squares fit, or a uniform baseline). The quality criterion, called `no_gain`, fires when the latest round produced no IS improvement, `IS_t - IS_{t-1} <= 0`, after a warmup period.

The **cascade** combines them in a strict priority order, given as actual code (`shp_should_halt`): round 1 always continues; then an explicit critic approval (feedback beginning with the literal string `APPROVED`) halts with reason `critic`; then the entropy criterion (k consecutive `d < ε`) halts with reason `entropy`; then the quality-plateau criterion halts with reason `no_gain`; then an unconditional failsafe halts at `t >= max_rounds`. So the two criteria are combined not by conjunction but by cheap-signal-first precedence — the free geometric test is consulted before the judge-consuming quality test, and each signal except the failsafe carries an ablation flag that can switch it off. The prose framing ("the loop only halts when the answer has both stopped changing and stopped improving") is a looser description than the code, which halts on whichever criterion fires first.

Two implementation details are worth recording. The cascade is written once as a pure function and reused by the live loop, the post-hoc reason derivation, and the offline policy replay, so the three cannot disagree. And the failsafe clause carries a code comment marking it "never ablatable" — that unconditionality is exactly what the termination theorem rests on.

## Models targeted and benchmarks used

- **Models.** A single 8B instruction model, `llama-3.1-8b-instruct`, served through an OpenAI-compatible endpoint, plays every LLM role: Writer, Critic, and RAGAS judge. The author says the larger test split provides statistical power and that a stronger judge is left as a future robustness check. Compute is described as "credit-based and modest," openly stated as a limitation. Embeddings are computed locally and are therefore free; the specific embedding model is never named, only its 384-dimensional output, and no ablation over embedding choice is reported.
- **Benchmark.** HotpotQA in the distractor setting, streamed from the HuggingFace Hub (`hotpot_qa/distractor`, validation split). The builder filters to multi-hop hard questions, assembles a retrieval context of gold supporting paragraphs plus distractors (roughly four contexts per question), and assigns the development/test split deterministically by hashing the example identifier. This yields about 80 scenarios: 20 development, 60 test. Both Writer and Critic are conditioned on the retrieved contexts; the judge additionally sees the gold answer.
- **Thresholds.** `ε = 0.06` and `k = 2` are the values used. The paper states they are tuned on the development split only and that the test split is frozen and report-only. It does not show the tuning sweep, report sensitivity to `ε` or `k`, or justify those particular values beyond the distance distribution (80% of observed per-round distances fall below 0.06). Given a 20-question development split, this is a thin basis for two hyperparameters that the whole method depends on.

## Author incentive

Single author, no institutional affiliation, no funding statement, no disclosed conflicts. The stake is a personal open-source project (`github.com/SahilShrivastava-Dev/semantic-halting-problem`) whose name is also the paper's "affiliation." There is no product or commercial position to defend.

The more interesting incentive is reputational, and the paper makes it explicit rather than hiding it. An earlier version claimed the Writer-Critic update was a Banach contraction with a guaranteed unique fixed point; the author retracts that in the body of the paper, on the grounds that LLM generation has no proven Lipschitz constant below one and is not deterministic across API calls. He then argues that the retraction is itself a contribution: "it is the difference between a result a reviewer can trust and one they reject on sight." That sentence names the incentive — the paper is written to survive review, and its honesty is deployed partly as a credibility instrument. The honesty is nonetheless real and checkable, which is what matters for the reader.

## What is proved versus what is conjectured

This is the part of the paper I would keep if I could keep only one part, because the boundary is drawn cleanly and the paper does not smuggle anything across it.

**Proved and machine-checked** (an executable suite, `theory_checks.py`, which the author says a reviewer can rerun):

- *Theorem 1, Termination.* For any input, any weights, any signal configuration, and any possibly adversarial draft sequence, the loop halts within `T_max` rounds. The proof is three lines and turns entirely on the failsafe clause being unconditional: the Critic increments `t` by exactly one per round, and the failsafe returns a halt whenever `t >= T_max` regardless of any signal or ablation flag, so the stopping time `τ <= T_max`. This is a guarantee about the *harness*, not about the model — which is precisely why it holds.
- *Lemma 1, Well-definedness.* If the weights lie on the simplex and each metric lies in `[0,1]`, then `IS_t` lies in `[0,1]`. The distance `d_t` is total: finite for every finite input and bounded in `[0,2]`, with the degenerate zero-norm case mapped conservatively to `1.0` so that it cannot produce a false-positive halt. That conservative mapping is a small but real piece of design: a numerical edge case is resolved in the direction of continuing rather than stopping.
- *Lemma 2, Halt-priority consistency.* The reason reported after a run equals the reason that actually stopped it, because the live decision and the post-hoc derivation call the same function. This is a claim about code hygiene stated as a lemma, and the paper is candid that it exists because an earlier version had two divergent orderings that could disagree.

**Conjectured and only measured:**

- *Conjecture 1, Semantic non-expansiveness.* The claim is that `d_t` is, on average, non-increasing in `t`. The paper explicitly states "we make no guarantee," and specifies in advance how it will be tested: the fraction of monotone trajectories, the mean regression slope with a bootstrap 95% CI, a one-sided Wilcoxon test on `d_t - d_{t-1}`, and a commitment to report null results where they occur.

The author states the substitution plainly: "SHP guarantees termination, not contraction." I find the distinction honestly drawn. The one place the framing still flatters itself is that Theorem 1 is close to trivial — an unconditional counter cap terminates, which is true of the `max_iterations` baseline the paper is arguing against. What the theorem actually buys is that adding three content-dependent signals to the cascade does not *destroy* the guarantee the counter already gave. That is worth proving, but it is a safety property of the composition, not evidence that the semantic machinery works.

## The judge-efficient evaluation protocol

The paper treats fair policy comparison as a contribution in its own right, and this is the most transferable piece of the work.

- **Trajectory replay.** For each question, the full Writer-Critic trajectory is generated *once*, to depth `T_max`, with every draft and embedding cached. Each stopping policy then replays over that single cached trajectory and picks its own stop round. Two consequences: all policies see literally identical drafts, so any difference in rounds or quality is attributable to the policy rather than to generation noise (a strictly paired comparison), and the expensive generation is paid once rather than once per policy.
- **Cached judging.** The RAGAS judge is identified as the binding cost. Each distinct draft is judged at most once, keyed by a hash of the draft text, so two policies stopping at the same round share a single judge call.
- **Operational versus evaluation tokens.** This is the conceptual move. Tokens a policy spends to *run* — Writer plus Critic every round, plus the judge *only if that policy consults the quality signal in order to decide* — are charged to the policy as operational tokens. Tokens spent to *measure* final quality are evaluation tokens and are never charged to any policy. Without this split, the judge cost of the quality-gated variant would be invisible, hidden inside a measurement budget that every policy appears to share. With it, the judge cost lands on exactly the policies that made a decision with it.

The self-consistency point matters here too: the same pure halt function drives the live loop and the offline replay, so a replayed policy decision is the decision the live loop would have made on those drafts.

There is a scope limit the paper does not dwell on. Replay is only valid for stopping policies that are *passive readers* of a fixed trajectory. A policy that changed the Writer's prompt, or fed a different critique forward, would alter the drafts and could not be replayed over a trajectory generated under another policy. Every policy compared here happens to satisfy that condition, so the protocol is sound as used, but it does not generalise to interventions on the loop itself.

## Measurement methodology

- **Dependent variables.** Three, reported jointly: rounds to halt, operational tokens (with saving expressed as `(T_base - T_π)/T_base`), and final Information Score. The baseline throughout is `fixed_k6`, which is the `max_iterations` policy.
- **Controls.** The drafts themselves are the control — identical across policies by construction, via replay. The development/test split is deterministic (identifier hash), `ε` and `k` are tuned on development only, and the test split is described as frozen and report-only.
- **N.** 20 development scenarios, 60 test scenarios, from about 80 total. All tests are paired across questions. The distance characterisation uses 300 per-round test distances.
- **Policies compared.** Seven: `shp` (full cascade); `entropy_only` (the judge-free variant: cosine distance plus failsafe); `critic_only`; `fixed_k` for k in {1,3,6}; `random_stop`; and `oracle_is`, which stops at the round of maximum measured IS and serves as a quality upper bound. A seven-cell ablation toggles each signal.
- **Significance.** Paired t-tests and Wilcoxon signed-rank tests on rounds, tokens and IS; Cohen's `d_z`; bootstrap CIs. For the "no quality loss" claim the paper correctly refuses equality testing and uses two one-sided tests (TOST) for non-inferiority with margin `δ = 0.02`, testing `H0: E[IS_π - IS_base] <= -δ`. Choosing non-inferiority testing rather than reporting a non-significant difference as evidence of parity is the right instrument, and the paper is unusual in both using it and then reporting that it *fails* for its own headline policy.

Weaknesses in the methodology: no multiple-comparison correction is mentioned despite seven policies against a shared baseline; `random_stop` appears in the policy list but never in either results table; the four IS weighting strategies are described as selectable but the paper never says which one produced the reported numbers, nor whether the results move under the others; and `δ = 0.02` is acknowledged as a modelling choice with claimed sensitivity analysis that is not shown in the text.

## Key findings

### The worked example, and what it accidentally shows

Table I traces one real question — "Are both Cypress and Ajuga genera?", ground truth *no*. The drafts grow from 16 words to 162; the distance falls 0.144, 0.027, 0.007, 0.003; the IS moves 0.54, 0.62, 0.64, 0.62, 0.66. Round 3 is the first sub-`ε` round, round 4 is the second, and with `k = 2` the entropy criterion halts at round 4 while the baseline would have run all six. The author reads this as the thesis in miniature: "the loop earns its keep early and idles late, and a content signal can tell the difference."

Read more closely, the same trace also contains the paper's central negative result. The halt lands on round 4 at IS 0.62, while round 5 — labelled "wasted under baseline" — scores 0.66, the highest value in the trace. So the illustrative example of the method working correctly is also an instance of stopping on a locally worse draft. The paper does not comment on this, but it is the oracle gap appearing in the very first table.

### Development split (N = 20, 8B judge), baseline `fixed_k6` at 6.0 rounds, 11,281 operational tokens, IS 0.651

- `entropy_only`: 4.05 rounds, 7,068 tokens (37% cheaper), IS 0.661.
- `critic_only`: 6.0 rounds, no saving, IS 0.651 — the Critic never emitted `APPROVED`, so this policy is indistinguishable from the baseline.
- `fixed_k3`: 3.0 rounds, 54% cheaper, IS 0.629.
- `fixed_k1`: 1.0 round, 86% cheaper, IS 0.661.
- `shp` (full cascade): 2.6 rounds but 27,130 tokens, i.e. 140% *more* expensive, IS 0.636.
- `oracle_is`: 3.1 rounds, 33,007 tokens, 193% more expensive, IS 0.782.

The `shp` row is the paper's own most interesting number: the full cascade halts *earliest* of any adaptive policy, at 2.6 rounds, and is still the second most expensive policy in the study, because the `no_gain` signal calls the judge on every round in order to decide. Fewer rounds, far more tokens.

### Test split (frozen, N = 60), baseline `fixed_k6` at 6.0 rounds, 11,070 tokens, IS 0.670

- `entropy_only`: 3.92 rounds, 38% token saving, ΔIS = -0.004, p = 0.81, TOST verdict **no**.
- `critic_only`: 6.0 rounds, 0%, ΔIS = 0.000.
- `fixed_k3`: 3.0 rounds, 53% saving, ΔIS = +0.001, p = 0.97, TOST **no**.
- `fixed_k1`: 1.0 round, 86% saving, ΔIS = +0.030, p = 0.17, TOST **yes**.
- `shp` (full): 2.40 rounds, 129% *more* tokens (2.3x the baseline), ΔIS = -0.004, p = 0.78, TOST **no**.
- `oracle_is`: 2.73 rounds, 170% more tokens, ΔIS = +0.115, p ≈ 3e-11, TOST **yes**.

The TOST column deserves attention because the paper is careful about it in a way most papers are not. `entropy_only` and `fixed_k3` are at parity by point estimate (|ΔIS| <= 0.004) but *fail* formal non-inferiority at margin 0.02, and the paper says why in a footnote: the noisy LLM judge widens the interval enough that non-inferiority cannot be certified, "though no quality loss is detectable." The abstract nonetheless states the result as "38% ... at parity quality," which is the point estimate rather than the certified claim. That is a real gap between the abstract and the table, though the paper discloses it rather than burying it.

### Distance characterisation (Conjecture 1)

Over 300 per-round test distances: mean 0.040, median 0.022, maximum 0.39, and 80% fall below `ε = 0.06`. The per-step differences `d_t - d_{t-1}` are significantly negative (one-sided Wilcoxon p = 1.3e-3; mean OLS slope -0.009), so distances do decrease on average across rounds. But only about 5% of trajectories are strictly monotone — the paper's own words, "the descent is real but noisy."

The author then makes the connection that justifies the design: this is *why* the patience window `k = 2` is necessary. It captures the average contraction while tolerating per-round noise, so a single lucky sub-threshold round does not fire a halt. The conjecture is confirmed in the weak form in which it was stated (on average) and refuted in the strong form (per trajectory), and the paper reports both.

One number is worth holding on to: 80% of all observed per-round distances already fall below the halting threshold. The threshold is not selecting a rare event.

### The authors' own reading

The paper draws three findings and does not overstate them.

1. **The efficiency claim holds.** Judge-free `entropy_only` cuts 38% of operational tokens at statistically indistinguishable quality. `fixed_k3` saves 53% at parity. "Stopping early is both cheap and safe."
2. **Full SHP is counter-productive.** Consulting the judge every round to power the information-gain signal makes the full cascade the most expensive policy for no quality benefit. The author frames this as validating the judge-free design and as "exactly the cost the operational/evaluation split is built to expose" — a negative result about his own headline method, reported as a vindication of his measurement instrument.
3. **Iteration does not improve measured quality here — it slightly hurts it.** The best practical policy is `fixed_k1`: return the first grounded draft, which is both the cheapest (86% saving) and the highest quality (IS 0.700, Δ = +0.030, and the only practical policy that passes TOST). Meanwhile the oracle reaches 0.785 (+0.115, p ≈ 4e-11). A much better round exists for each question, but no online signal locates it.

The author's summary: on efficiency the result is "yes and immediately actionable"; on quality it is "honest and informative rather than triumphant." The discussion then performs the reframe that is the paper's most quotable claim — stopping early *for efficiency* is easy and safe (the free signal saves tokens and the failsafe guarantees termination), whereas stopping at the *best* round for quality is unsolved, and the oracle gap is substantial headroom that neither cosine distance nor information gain captures. He accordingly restates SHP's lasting contribution as (a) a guaranteed-terminating judge-free stopper and (b) an evaluation protocol plus an oracle target that make best-round identification measurable.

I record one uncomfortable implication the paper states but does not sit with. On this benchmark, the strongest practical baseline is not to loop at all. That makes the 38% saving a comparison against a `max_iterations` baseline which is itself dominated by `fixed_k1` on both axes. The paper is honest that HotpotQA under-exercises iteration, but the honesty does not repair the fact that the headline saving is measured against a policy nobody should have been running on this task.

### Minor internal inconsistencies

Recorded for accuracy, none material to the argument: the oracle p-value appears as 3e-11 in Table III and 4e-11 in both the abstract and the findings text; the token-saving formula in Section VI, `(T_base - T_π)/T_base`, yields a positive number for a saving, whereas the tables render savings as negative percentages and cost increases as positive; and `random_stop` is listed among the policies in the experimental setup but appears in neither results table.

## Open questions the paper itself raises

- **Best-round identification.** This is the one the paper elevates to the central open problem. An oracle that picks the round of maximum measured IS beats every practical policy by +0.115 at p ≈ 4e-11, so per question a much better round demonstrably exists, and neither the geometric signal nor the information-gain signal finds it. The proposed direction is learned best-round predictors that approach the oracle.
- **Does iteration ever pay?** HotpotQA answers are short and often answerable from one grounded draft, which the paper says is precisely why `fixed_k1` wins. A long-form generation task, where drafts genuinely accrue content, is named as the required next test — it would exercise iterative quality improvement rather than only convergence.
- **Judge reliability.** The RAGAS judge is an 8B LLM and is described as a noisy proxy whose per-question variance is large enough to block formal TOST certification at N = 60. A stronger or human-validated judge is the stated robustness check. Note the circularity the paper leaves standing: the same 8B model writes, critiques, and grades.
- **External validity.** A second dataset is named as necessary; nothing here establishes that `ε = 0.06` and `k = 2`, or the 38% saving, transfer off HotpotQA.
- **The margin `δ`.** Called a modelling choice for which sensitivity is reported, though not in the text I read.
- **Conjecture 1's status.** It holds only on average, and the paper explicitly leans on Theorem 1 to keep the system safe regardless — an acknowledgement that the semantic signal is heuristic and the counter is what actually guarantees anything.

## Appreciation

I want to keep mechanism and magnitude apart here, because the paper's mechanisms are considerably more valuable than its numbers.

### Mechanism (strong, and largely portable)

- **The cheap-signal-first cascade.** Ordering halt criteria by their cost, so that a free geometric test is consulted before a test that spends judge tokens, is a genuinely good structural idea. The paper's own most striking result is what happens when you violate it: the quality-gated variant halts *earlier* than anything else and still costs 2.3x the baseline.
- **The operational-versus-evaluation token split.** This is the sharpest instrument in the paper. Charging a policy for the tokens it spends *deciding*, and never for the tokens spent measuring it afterwards, is what makes a self-evaluating stopper's cost visible at all. Without it the full cascade would have looked free. Any study that compares stopping rules where some consult a model and some do not needs this distinction, and most do not have it.
- **Trajectory replay with cached judging.** Generate once, replay every policy over identical drafts, hash-key the judge calls. This turns a noisy unpaired comparison into a strictly paired one and makes a seven-policy study affordable. The limitation (only passive policies can be replayed) is real but the technique is correct within it.
- **One pure halt function shared by the live loop, the reason derivation, and the replay.** A small engineering discipline, elevated to a lemma, that removes a whole class of "the run says it stopped for X but it actually stopped for Y" bugs.
- **The patience window justified by measurement rather than by taste.** `k = 2` exists because the descent of `d_t` is significantly negative on average but strictly monotone in only about 5% of trajectories. The design follows from the measured noise, which is the right order of reasoning.
- **The proved/conjectured boundary, and the public retraction.** Replacing an unsupported Banach-contraction theorem with a modest termination theorem, saying so in the paper, and shipping a runnable check for every proven claim.

### Magnitude (weak, and the paper is mostly candid about it)

- N = 60 test questions, N = 20 for tuning two hyperparameters, one benchmark, one 8B model in all three roles, one unnamed embedding model with no ablation.
- The headline "parity quality" is a point estimate that fails the paper's own non-inferiority test.
- The 38% saving is measured against a baseline (`fixed_k6`) that is dominated on both cost and quality by `fixed_k1` in the same table.
- The largest effect in the study is the oracle gap, which is not an achievable result but a measurement of how far short everything achievable falls.

So: the mechanisms are worth adopting, the specific magnitudes are worth nothing outside HotpotQA, and the paper's most durable empirical contribution is a negative one — that a self-evaluating stopper can cost more than the iteration it saves.

## How it could serve a harness-design effort; limitations; major concerns

### What transfers

The most directly usable idea for a loop harness is the **cost-ordered halt cascade with an unconditional failsafe at the bottom**. Concretely: put free signals first (a trajectory-derived signal such as embedding distance, or an explicit approval token from a critic), put any signal that requires a model call after them, and make the budget cap ablation-proof so that termination never depends on whether a content signal fires. Theorem 1 is nearly trivial as mathematics, but its content as engineering advice is not: *no content-aware signal you add may be the only thing standing between the loop and non-termination*. That is a design rule worth holding.

The second transferable idea is the **accounting discipline**. If a harness lets an agent decide whether it is done by consulting a judge, a verifier, or its own reflection, the tokens spent on that decision belong to the decision, not to the measurement budget. This paper found its own headline method counter-productive only because it accounted this way. A harness that logs judge calls separately from work calls can answer the question "is our stopping logic paying for itself?" — a question most systems cannot currently answer about themselves.

The third is **replay as a way to test stopping policies offline**. Record full trajectories to depth, then evaluate candidate stopping rules against the recorded drafts. For a harness with logged runs, this makes policy changes testable without re-running agents, at the cost of being valid only for policies that read the trajectory rather than change it.

### What the paper says about the Subject's core question

Bearing directly on how a loop judges whether its work is done, failing, or beyond it, the paper offers a specific and somewhat deflationary answer within its scope. A trajectory-level signal (successive drafts have stopped changing in meaning) is cheap, free of model calls, and adequate for the *efficiency* question — stop when further iteration is churn. A self-evaluation signal (the model's own quality score has stopped improving) is expensive, and here it bought nothing: it fired earlier and cost more. And *neither* signal answers the harder question of which round was actually best, which the oracle shows is where all the remaining quality lives.

Worth noting what the paper does *not* have signals for. Its reason set is `{critic, entropy, no_gain, failsafe}` — converged, plateaued, approved, or out of budget. There is no notion of *failing* as distinct from converged, and no notion of a task being *beyond* the loop and warranting abandonment or handoff. A loop that has converged on a wrong answer and a loop that has converged on a right one halt identically, with the same reason, and the harness cannot tell them apart. Semantic stability is treated as evidence of doneness, when it is only evidence of stability — and a stuck loop repeating itself produces exactly the same signal as a finished one. On this benchmark that conflation is invisible because the drafts are short and grounded; in a harness where an agent can loop unproductively on a task it cannot do, the distance signal would report convergence for the failure case just as confidently.

### Major concerns

1. **Scale.** Two hyperparameters tuned on 20 questions, one benchmark, one model family. No claim here should be carried forward as a number.
2. **Judge circularity.** One 8B model writes, critiques, and grades. The quality metric that adjudicates every comparison is produced by the same model whose output is being adjudicated, and the paper's own limitations section concedes the resulting variance defeats its non-inferiority test.
3. **The benchmark undercuts the premise.** A task where one draft usually suffices is a poor place to study when to stop iterating. The author says so, but the paper's headline numbers are nonetheless drawn from it.
4. **Abstract overstates the table.** "At parity quality" is a point estimate that the paper's own TOST column marks as not certified.
5. **Single-author, self-affiliated, unreviewed**, with an appendix that positions the work against five recent arXiv preprints rather than against an established literature. The related-work comparison is written in a "what they do better / what we do better" format that reads as advocacy, and three of the five comparison targets are 2026 preprints.
6. **No cost model for the embedding.** "Embeddings are local (free)" is true of the token bill and false of latency and deployment complexity; a harness maintainer inherits an extra model to host.

### Where it would fit a harness effort

As a source of design rules and an evaluation method, not as a source of thresholds. Adopt the cascade ordering, the failsafe invariant, the operational/evaluation split, and the replay protocol. Re-derive `ε`, `k`, and the embedding choice from your own trajectories. Treat the oracle-gap result as the warning it is: the loop's own signals may tell you reliably when to stop and still not tell you what to return.

## Five citations worth chasing next

1. **Yang et al., "HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering," EMNLP 2018** — the benchmark every quality number here rests on, and the paper's own limitations argue its answer format is what makes `fixed_k1` win. Worth reading to judge how much of the negative quality result is an artefact of the dataset.
2. **Es et al., "RAGAS: Automated Evaluation of Retrieval Augmented Generation," 2023** — the source of the four metrics composing the Information Score, i.e. the paper's entire dependent variable and its acknowledged noise source. The reliability of RAGAS under a small judge model bounds what this paper can conclude.
3. **Lakens, "Equivalence Tests," Social Psychological and Personality Science, 2017** — the methodological reference for TOST non-inferiority testing. Directly relevant to the Subject beyond this paper: "the system did not get worse" is an equivalence claim, and most agent evaluations make it with a non-significant difference instead.
4. **Sun et al., "Collaborative Entropy: Uncertainty Quantification in Agentic Multi-LLM Systems," arXiv:2603.28360, 2026** — the paper identifies this as measuring cross-model disagreement at one instant, where SHP measures temporal convergence across rounds of one loop. That is the complementary axis of the same question, and squarely on the Subject's uncertainty-estimation strand.
5. **Prechelt, "Early Stopping — But When?," Neural Networks: Tricks of the Trade, 1998** — the classical treatment of exactly the patience-window-versus-threshold trade-off this paper transports to the agent loop, including the criteria-selection question that `ε` and `k` reopen here.
