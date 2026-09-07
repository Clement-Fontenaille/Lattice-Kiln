# Measuring and Narrowing the Compositionality Gap in Language Models

## Density

**Density: HIGH** — a short paper in which nearly every section is load-bearing, and the load it bears is exactly the Subject: it isolates recombination as a distinct failure mode from sub-task execution, names and measures it, and proposes a decomposition prompt that narrows it.

**Keywords (mine):** compositionality gap; recombination failure; sub-question decomposition; self-ask; elicitive prompting; 2-hop QA; memorization vs. composition; tool call at the sub-task boundary; scale-invariant deficit; parseable scaffolding.

**Year:** arXiv preprint Oct 2022 (v3 Oct 2023); published Findings of EMNLP 2023.

**Venue:** Findings of the Association for Computational Linguistics: EMNLP 2023. DOI 10.18653/v1/2023.findings-emnlp.378. arXiv:2210.03350.

**Authors:** Ofir Press, Muru Zhang, Sewon Min, Ludwig Schmidt, Noah A. Smith, Mike Lewis.

## Approach

The paper has two halves that are logically separable, and it is worth keeping them apart.

**Half one — define and measure a quantity.** The authors define the *compositionality gap* as the fraction of compositional questions the model gets wrong *among only those questions whose sub-questions it answers correctly*. Formally, of the questions where both sub-answers are right, what share of the composed answers are still wrong. This is a conditional error rate, not an absolute one: it deliberately factors out ignorance of the constituent facts, so that what remains is the model's failure to put known pieces together.

To measure it they need questions where (a) each constituent fact is common in pretraining data and (b) the *combination* almost certainly never appeared. They build **Compositional Celebrities (CC)**, 8.6k automatically generated 2-hop questions, by crawling celebrity lists (birth year, birth country) and joining them to properties of those years and countries — "What is the calling code of the birthplace of Frida Kahlo?", "Who won the Master's Tournament the year Justin Bieber was born?". 17 templated categories. Each question decomposes cleanly into two 1-hop questions that can be asked separately, which is the whole point: the sub-questions are the instrument that lets them condition on "the model knows the parts". They argue the combinations are absent from the web (manual search checks), and they include a BIG-bench canary string to keep the dataset out of future training sets.

They then evaluate the GPT-3 family across sizes on the 2-hop questions and, separately, on the constituent 1-hop questions, using 2-shot category-specific prompts, and plot both curves against scale. The gap is read off as the vertical relationship between them.

**Half two — narrow it with prompting.** The framing is that direct-answer prompting gives the model roughly a fixed amount of computation per question regardless of difficulty; *elicitive* prompts (chain of thought, scratchpad) let it spend more. They introduce **self-ask**: a few-shot prompt in which the model, before answering, emits an explicit "Are follow up questions needed here:", then a sequence of "Follow up: <sub-question>" / "Intermediate answer: <sub-answer>" pairs, then "So the final answer is:". The model itself decides whether to decompose and how many follow-ups to issue; the whole thing happens in a single forward pass with a single prompt. The stated hypothesis for why it beats chain of thought is that it *disentangles the decomposition of the question from the answering of the sub-questions* — the sub-question is stated as a first-class object before it is answered — and that the rigid scaffolding makes the final answer parseable.

**Half two, extension.** Because self-ask marks the start and end of every sub-question explicitly, an external tool can be spliced in at exactly that boundary. **Self-ask + Search Engine (SA+SE)** intercepts the generation when it emits "Follow up:", lets it finish the sub-question, halts it at "Intermediate answer:", sends the sub-question verbatim to a search API (SerpAPI), and pastes the returned answer back into the context as though the model had produced it. No finetuning, no architecture change, no special query language, and — emphasized repeatedly — *the exact same prompt as plain self-ask*. A few lines of code.

## Model(s) targeted

- The GPT-3 family, across sizes from ~1B to 175B, in two lineages: the vanilla GPT-3 models and the InstructGPT models (001, 002, 003 variants). Model size figures are taken from a third-party EleutherAI blog post, since OpenAI did not publish them — worth noting, since the scaling claim rests on that axis.
- `text-davinci-002` ("Davinci-002") is the workhorse for all the Section 3 prompting experiments.
- ChatGPT and GPT-4 appear only in a footnote, with estimated gaps of 42.9% and 23.0%, and the authors flag the GPT-4 number as possibly invalid because CC was publicly released before GPT-4 launched and may be in its training set. No training-data or architecture details were available for either, so they are excluded from the scaling analysis.
- Explicitly: no models were trained or finetuned anywhere in the paper.

## Benchmarks / datasets

- **Compositional Celebrities (CC)** — new, theirs. 8.6k automatically generated 2-hop questions across 17 templates. Used for measuring the gap, because it is the only dataset here that ships the sub-questions needed to condition on.
- **Bamboogle** — new, theirs. 125 hand-written 2-hop questions drawn from random Wikipedia *vital* articles, deliberately varied and template-free. Filter criterion: a question is admitted only if a popular search engine returns a "featured snippet" that is *wrong* — used as evidence the question is not on the web, while both constituent hops are Wikipedia facts and so presumably in any LM's pretraining set. Small, low statistical power, but high question diversity; positioned as the complement to CC.
- **2WikiMultiHopQA** (Ho et al., 2020) — 1.2k-question subset of the dev set, open-domain (question-answer pairs only, supporting passages discarded).
- **Musique** (Trivedi et al., 2022) — the 1252 dev questions labelled 2-hop; 3- and 4-hop questions were dropped because the authors found them convoluted to the point of being hard for the authors themselves to parse. Musique's *training* set is where the method was developed.

## Author incentive

University of Washington (Paul G. Allen School), MosaicML, Meta AI Research, Allen Institute for AI. Funding acknowledged: NSF grant 2113530 in part. This is an academic-plus-industry-lab mix with no product being sold; the direct stake is in self-ask as a named method and in CC/Bamboogle as adopted datasets, both released publicly on GitHub. The measurement half is not method-flattering — it reports a negative result about scale that cuts against the interests of the industrial affiliations more than it serves them. Two mild positional stakes to note: self-ask is *their* method being compared against chain of thought and least-to-most, and the paper stakes a priority claim ("we are the first to propose the use of 2-hop questions as a means of evaluating the compositional abilities of large LMs") and distinguishes itself from concurrent work (Khot et al., Yao et al.) on grounds of the gap finding, the search integration, and the datasets rather than on the prompt itself.

## Measurement methodology (brushed)

**Dependent variables.** Two, and they are not the same thing.
1. For the gap: a *ratio* — 2-hop wrong / (2-hop right + 2-hop wrong), restricted to the subset where both sub-questions were answered correctly. Appendix Table 6 gives the raw 2×2 breakdown per category and in aggregate: over all of CC with davinci-002 and direct prompting, 41.8% of questions have both sub-answers right and the composition right, 33.4% have both sub-answers right and the composition wrong, 3.6% have a wrong sub-answer but a right composition, and 21.2% are wrong throughout. That yields a gap of roughly 44% aggregate; the headline "roughly constant ~40%" is the figure read across model sizes in Fig. 1.
2. For the prompting half: plain accuracy. Exact match on 2WikiMultiHopQA and Musique; *manual judgement by the authors* on Bamboogle. Appendix Table 14 repeats the 2Wiki/Musique results under F1 and Cover-EM and the system ranking is unchanged, which is the right robustness check to have run.

**What is controlled.** Within a dataset, the same questions are used for every method and baseline. Prompt shot-count is held fixed per dataset (2-shot on CC, 4-shot on 2Wiki/Bamboogle). Two deliberate anti-overfitting moves: the 2WikiMultiHopQA prompt reuses the four examples from Table 3 of the original 2Wiki paper in the original order, to demonstrate no prompt engineering; and Bamboogle is run with the 2Wiki prompt, again to show no per-dataset tuning. Method development happened on the Musique *training* set (a few dozen experiments) and dev sets were used exactly once. One controlled comparison is honest about a confound: the least-to-most vs. self-ask speed comparison in Table 2 was run later against a different davinci-002 deployment than Table 1, and the authors say so and note self-ask improved with the newer deployment.

**Efficiency as a second dependent variable.** Table 2 reports average tokens in the generated answer alongside accuracy for least-to-most vs. self-ask — 844 vs. 569 tokens on 2Wiki, 1020 vs. 663 on Musique. This is the paper's only quantitative treatment of decomposition *cost*, and it is a proxy (output tokens, not wall-clock or dollars), though they phrase it as "more than 30% faster".

**N and significance.** N is stated everywhere: 8.6k CC (1.2k sampled for the elicitive-prompt experiments), 125 Bamboogle, 1.2k 2Wiki, 1252 Musique. There is **no significance testing anywhere** — no confidence intervals, no error bars, no variance across prompt seeds or sampling runs, no repeated runs. Differences are reported as raw point differences. The authors are aware of the weakness at least for Bamboogle, which they describe as having "less statistical power", but the paper as a whole treats a several-point accuracy difference as a result without quantifying its uncertainty. The scale trend in Fig. 1 is likewise a visual reading across a handful of model points, not a fitted trend with a stated error.

**One auxiliary measurement worth flagging** because it is methodologically the most interesting thing in the paper: they bin the questions where both sub-answers are right by the *perplexity the model assigns to the worse-perplexity correct sub-answer*, into deciles, and plot composition accuracy per bin (Fig. 5). This turns "does it know the fact" from a binary into a graded quantity.

## Key findings

**1. The compositionality gap exists and is large.** Davinci-002 answers 45.4% of CC 2-hop questions correctly while answering ~80% of the sub-questions correctly. Per-category spread is enormous: Birthplace/Domain Name reaches 84.6% on the 2-hop question, while Birth Year/Literature Nobel Prize Winner sits at 1.2%. In the aggregate 2×2, a third of all CC questions are cases where the model demonstrably holds both facts and still fails to compose them.

**2. The gap does not shrink with scale — this is the headline.** Across the GPT-3 family from ~1B to 175B, both 1-hop and 2-hop accuracy improve monotonically with size, but 1-hop improves *faster*, so the ratio stays roughly constant at ~40%. It holds across both the vanilla and InstructGPT lineages. The authors' own reading: "larger scale pretraining is highly effective at teaching models to memorize facts but not how to compose them" — scale buys knowledge, not composition. They call the result surprising and stress that the reasoning demanded is trivial given the facts.

**3. Composition is conditioned on confidence, not just correctness.** Where the model's worse correct sub-answer has perplexity in [1.000, 1.002], it composes correctly 81.1% of the time; where that perplexity is in [1.232, 6.738], only 42.6%. The same pattern holds using average rather than worst perplexity. Authors' reading: getting a 1-hop question right in a prompt full of similar 1-hop questions does not mean the fact is "fully learned"; a fact must be held *confidently* to be composable. They draw a methodological recommendation from this — report perplexity on the correct answer alongside accuracy in downstream QA evaluation — and connect it to concurrent work (BIG-bench, Wei et al.) arguing cross-entropy reveals improvement that accuracy metrics hide.

**4. Elicitive prompting narrows the gap; self-ask narrows it further.** On CC, self-ask (1-shot) narrows and in places *closes* the gap (Fig. 6), with chain of thought within 1% of it on that dataset. Striking sub-result: on CC, elicitive prompts sometimes answer *more* compositional questions correctly than direct prompting answers the separate sub-questions for — the authors suggest elicitive prompts simply carry more information than direct ones. On davinci-002: direct 17.6 / CoT 46.4 / self-ask 57.6 / SA+SE 60.0 on Bamboogle; 25.4 / 29.8 / 30.0 / 40.1 on 2Wiki; 5.6 / 12.6 / 13.8 / 15.2 on Musique. Kojima-style "Let's think step by step" is much weaker (45.7% vs. self-ask's 79.6% on CC with davinci-002; 1.1% vs. 54.2% with vanilla Davinci) and was dropped.

**5. Self-ask's margin over chain of thought is largest where the questions are least like the prompt.** Small margins on the templated 2Wiki and Musique, an 11-point absolute margin on the varied, template-free Bamboogle. Authors' reading: because Bamboogle questions do not resemble the few-shot examples, chain of thought struggles to decompose them, whereas self-ask, which decomposes *explicitly*, generalises to novel inference questions. This is their strongest claim about *why* explicit decomposition helps, and it is an argument about generalisation, not about accuracy on any one benchmark.

**6. A secondary but real benefit is parseability.** 40% of chain-of-thought final answers on Bamboogle were not in short form despite the prompt demonstrating short form; 17% for self-ask, 3% for SA+SE. Some of those CoT answers contain the correct answer and are scored wrong anyway. So part of the measured CoT deficit is formatting, not reasoning — the authors are explicit about this and give examples (Table 15). The scaffolding is doing two jobs: shaping the reasoning and making the output machine-readable.

**7. The sub-question boundary is a tool-call site.** The search engine alone is near-useless on these questions (0.0 on Bamboogle, 2.2 on 2Wiki, 1.5 on Musique) and only becomes competitive with direct prompting when an LM postprocesses its output. But routed *through* self-ask's sub-questions it adds up to 10 points absolute. The composed system beats both of its parts by a wide margin.

**8. Single-pass decomposition matches or beats multi-pass at lower cost.** Against least-to-most, which needs multiple forward passes with different prompts: self-ask gets 35.5 vs. 29.0 on 2Wiki and 16.3 vs. 16.8 on Musique — better on one, a hair worse on the other — while generating ~30–35% fewer tokens.

**Important scope caveat the authors state themselves:** outside CC they cannot claim self-ask *narrows the gap*, only that it improves accuracy, because 2Wiki, Musique and Bamboogle do not ship the sub-questions needed to compute the conditional ratio. The gap measurement and the prompting improvement live on different datasets.

## Open questions the paper itself raises

From the Limitations section, in its own framing:

- **The scale ceiling.** The ~40% constancy is established between roughly 1B and 175B parameters. They had no access to anything larger and say plainly that models above 175B "could potentially be different". They do not claim the gap is scale-invariant in principle — only across the range they could measure.
- **The closed-model blind spot.** ChatGPT and GPT-4 cannot be analysed because their training data and architecture are undisclosed; and the GPT-4 estimate is contaminated by CC's own public release. So the one data point that might contradict the trend (23.0% for GPT-4) is the one they explicitly say may be invalid. This is the paper's most honest and most consequential caveat.
- **The 2-hop, English, QA scope.** Everything is 2-hop question answering in English. They defend the choice — such datasets are a powerful probe, and they lead toward user-facing QA systems like Siri — and report that limited *manual* experiments on semantic parsing, arithmetic and logic puzzles suggest self-ask also works there, while conceding a thorough evaluation "could reveal different results". Note also that they dropped Musique's 3- and 4-hop questions as too convoluted, so deeper decomposition is untested even within the QA setting.

Questions the paper raises without listing as limitations:
- *Why* the gap is constant. They offer the memorize-vs-compose framing as an interpretation, not a mechanism. Nothing here explains what in the model makes composition fail while both retrievals succeed.
- Whether the perplexity finding should change evaluation practice generally. They advocate for it but do not develop it.
- Whether "more information in the prompt" (their own alternative explanation for elicitive prompts beating the direct-prompt sub-question baseline on CC) is doing part of the work attributed to reasoning. They raise this and leave it.

## Appreciation

Keeping mechanism apart from magnitude, because this paper's two contributions age very differently.

### MECHANISM — what transfers as an argument

**The construct itself is the durable contribution, and it is a good one.** The compositionality gap is a *conditional* measurement: it holds sub-task competence fixed and looks at what remains. That is the move that makes the paper worth reading for a Subject about splitting and recombining tasks. It says: performance on a composed task is not simply the product of performance on its parts, and the residual is measurable and large. Any decomposition architecture inherits that residual. The construct does not depend on GPT-3 — it depends only on having a task that decomposes into checkable sub-tasks, which is a design property, not a model property.

**The instrument design is the part I would steal.** CC is built so that the sub-questions exist as first-class objects, which is precisely what makes the conditional ratio computable. The authors then run headlong into the consequence of *not* having that property: on their three other datasets they can only report accuracy, not the gap. That is a general lesson about evaluating decomposed systems — if the sub-tasks are not separately gradeable, you cannot tell a splitting failure from an execution failure from a recombination failure. The paper demonstrates this by accident, in the shape of what it could and could not measure.

**Recombination is a distinct failure mode, not a bookkeeping step.** This is the single finding most load-bearing for the Subject. A third of all CC questions are cases where the model provably holds both facts and still produces the wrong composed answer. Splitting and executing correctly does not deliver the answer. That argument transfers.

**Explicit decomposition generalises better than implicit decomposition.** The self-ask-vs-CoT margin widening on the untemplated dataset is a mechanism claim: separating "state the sub-problem" from "solve the sub-problem" is what lets the system handle inputs unlike its examples. The paper's evidence for this is one dataset and one 11-point number, so the *claim* transfers as a hypothesis with support, not as a settled result; but the reasoning behind it is sound and testable.

**A demarcated sub-task boundary is an interposition point.** This is architecturally the paper's cleanest idea and it is nearly free. Once the sub-question is a marked span rather than a phrase buried in a chain of thought, anything can answer it — a search engine here, but the substitution is generic. That the same prompt serves both the model-answers-it and the tool-answers-it configuration, with no finetuning and no query language, is the demonstration. The related-work framing sharpens it: prior systems reached the same capability through imitation learning (Nakano et al.), RL (Menick et al.), or a bespoke query language plus finetuning (Thoppilan et al.). Formatting is doing the work that training used to do.

**The parseability finding is under-appreciated and generalises.** 40% of CoT answers on Bamboogle were unusable as *outputs* despite sometimes containing the right answer. In any system where a step's result is consumed by a later step, unstructured output is an outright failure, not a cosmetic one. Structure is a correctness property once composition is automated.

**Decomposition cost is measurable and single-pass is not obviously worse.** Self-ask matching least-to-most on accuracy with ~30% fewer tokens is a mechanism-level point about where decomposition cost actually comes from: the multi-pass orchestration, not the decomposition. One prompt that emits its own sub-questions can be cheaper than a pipeline that asks for them in a separate call.

### MAGNITUDE — numbers valid only inside this setup

Essentially every number here is a GPT-3-cohort artifact and should not travel:

- **~40% gap, ~44% aggregate on CC.** Cohort-bound. It is the *conditional* structure that transfers, not the value.
- **"Does not shrink with scale."** This is the finding most at risk, and the paper itself hands you the reason: the sole datapoint outside the GPT-3 family that could falsify it (GPT-4 at 23.0%) is roughly half the trend value, and is dismissed only on contamination grounds — a real concern, but one that leaves the claim resting entirely on a single now-superseded model family varying along a parameter-count axis sourced from a blog post. The honest reading: *within the GPT-3 family, parameter count alone did not buy composition*. That is narrower than "scale does not narrow the gap", and much narrower than any claim about post-training, RL, or reasoning-trained models, none of which existed to be tested. Treat this as a demonstration that the gap is not *automatically* dissolved by making a base model bigger, not as a standing prediction.
- **All accuracy tables** (17.6 / 46.4 / 57.6 / 60.0 etc.) — davinci-002 only, few-shot, no repeats, no intervals. Rankings are what one might carry forward, and even those cautiously: the CoT column is depressed by an answer-format artifact the authors themselves quantify.
- **The 11-point Bamboogle margin** — 125 hand-written questions, author-judged, no significance test. The *direction* is the finding; the size is noise-prone.
- **The 10-point search-integration gain** and the Kojima comparison — same setup dependence.
- **The perplexity deciles (81.1% vs. 42.6%).** The monotone relationship is the mechanism; the endpoints are not portable, and the whole measurement requires logprob access that many current deployments do not expose.
- **The ~30% token saving vs. least-to-most** — confounded by the acknowledged deployment change and measured in output tokens on two datasets.

### Reservations

Three, stated plainly. First, **no uncertainty quantification anywhere** — for a paper whose headline is a *constancy* claim read off a scatter of model points, the absence of any error treatment is the weakest link; "roughly constant at 40%" is a visual judgement. Second, **the two halves are joined by narrative rather than by measurement**: the gap is measured on CC, the method is evaluated mostly elsewhere, and the authors correctly refuse to claim self-ask narrows the gap outside CC — which means the title's "Narrowing" is supported on one dataset. Third, **CC is narrow by construction**: 17 templates of celebrity-plus-lookup-table joins, where the "composition" is a single substitution. That narrowness is what makes the measurement clean and also what makes it a floor case — if models fail at 40% on the *easiest* imaginable composition, that is either a very strong result or a sign the templated form has its own pathology (note the per-category spread from 1.2% to 84.6%, which suggests category-specific effects the aggregate hides).

## How it could serve a harness-design effort

Stemming the discussion rather than resolving it.

**It supplies a diagnostic, not just a finding.** The most useful thing to take is the measurement protocol: for any decomposable task, grade the sub-tasks *and* the composition, and report the conditional. That splits a harness's error budget into ignorance (sub-task wrong), recombination failure (sub-tasks right, whole wrong), and the odd lucky case (sub-task wrong, whole right — 3.6% on CC, small but non-zero and worth knowing about). Without that split, a harness's aggregate accuracy tells you nothing about whether to invest in better sub-task execution or better recombination. Open question this leaves: what the analogue of a "sub-question" is for tasks that do not decompose into checkable atomic facts — the whole protocol depends on the sub-tasks being independently gradeable, and much agentic work is not.

**It argues against treating recombination as free.** The Subject notes that splitting carries a cost and that whether it is offset is unsettled. This paper contributes a specific version: even with perfect sub-task execution, the join step fails at a substantial rate. A harness that decomposes and assumes assembly is bookkeeping is budgeting for the wrong thing. Whether that persists in current models is exactly what the paper cannot tell you.

**It argues for making the sub-task boundary explicit and machine-readable, for two independent reasons.** One, generalisation to inputs unlike the examples (the Bamboogle margin). Two, interposition — a marked sub-task is a place where a tool, a cache, a different model, a human, or a verifier can be substituted for the model's own answer, with no change to the prompt. The SA+SE result is the existence proof; the substitution is generic even if the search-engine numbers are not. Open question: the paper only ever substitutes at a *leaf*, one hop deep, and never recurses. Nothing here speaks to what happens when a sub-task is itself decomposed.

**It puts a number on the depth the evidence covers, and it is two.** Everything is 2-hop. Musique's 3- and 4-hop questions were discarded as too convoluted for the authors themselves. So for a Subject concerned with depth-setting and recursive splitting, this paper's honest contribution is at depth one split. If the composition of two known facts fails at 40%, the compounding question at depth three or four is wide open and this paper does not touch it — arguably its most interesting silence.

**It suggests confidence as a routing signal.** If composability tracks sub-answer perplexity, a harness could in principle decide *where* to decompose or when to call a tool based on how confidently it holds the constituent facts, rather than on task type or a fixed plan. That maps onto the Subject's axis of "what decides whether to split". Concerns: logprobs are often unavailable in current API deployments; perplexity on a few-shot completion is not obviously the right calibration signal; and the paper establishes correlation on one dataset, with no attempt to use it as a control signal.

**It shows single-pass self-decomposition as a real design point.** Between "one direct attempt" and "a multi-stage pipeline" there is a middle option: one call in which the model emits its own sub-questions and answers them, deciding the number itself. Cheaper than least-to-most here and roughly as accurate. Concern: the depth is emergent and unbounded, with no budget, no verification of the decomposition before execution, and no recovery if an early sub-answer is wrong — an incorrect intermediate answer is pasted into the context and treated as fact, which is a failure mode this paper never examines and which the search-engine variant makes structurally worse (the tool's answer is inserted *as if the model had produced it*, with no provenance and no adjudication).

**Major concerns for anyone leaning on it.** (i) Everything is GPT-3-era; the headline scale claim is precisely the kind of claim that a model-generation shift can void, and the authors' own GPT-4 footnote is the first sign of that. (ii) No significance treatment, so small margins should not drive design decisions. (iii) The task is single-substitution factual lookup; whether the gap generalises to composition over reasoning, code, or long-horizon action is untested and the authors' evidence there is explicitly "limited manual experiments". (iv) The method half is partly a formatting result, and formatting benefits are the first thing to evaporate when models are trained to emit structure natively. (v) The construct is defined only where sub-tasks are gradeable, which is a much smaller world than the one a general harness operates in.

## Five citations worth chasing next

1. **Zhou et al. (2022), "Least-to-most prompting enables complex reasoning in large language models"** (arXiv:2205.10625) — the multi-pass decomposition baseline self-ask is measured against on both accuracy and token cost. The direct point of comparison for single-call vs. staged decomposition.
2. **Khot, Trivedi, Finlayson, Fu, Richardson, Clark, Sabharwal (2023), "Decomposed prompting: A modular approach for solving complex tasks"** (ICLR 2023) — named as concurrent and similar to self-ask; modular framing, and unlike this paper, aimed at recursion and sub-task-specific handlers.
3. **Yao, Zhao, Yu, Du, Shafran, Narasimhan, Cao (2023), "ReAct: Synergizing reasoning and acting in language models"** (ICLR 2023) — the other concurrent method, and the one that generalises the sub-task-boundary-as-tool-call-site idea beyond a single search substitution.
4. **Perez, Lewis, Yih, Cho, Kiela (2020), "Unsupervised question decomposition for question answering"** (EMNLP) — the pre-LLM, trained-decomposer line of work. Worth reading to see what decomposition quality looked like when the splitter was a dedicated model rather than a prompt.
5. **Patel, Mishra, Parmar, Baral (2022), "Is a question decomposition unit all we need?"** (arXiv:2205.12538) — cited here for showing that *manual* decomposition improves performance. It isolates the value of the split itself from the model's ability to produce the split, which is the cleanest way to ask whether a harness's decomposition step is adding value or just adding calls.

*Alternates if pursuing the measurement side rather than the method side:* Wolfson et al. (2020) "Break it down: a question understanding benchmark" for decomposition annotation at scale, and Trivedi et al. (2022) for Musique's construction, since its 3- and 4-hop questions are exactly what this paper discarded.
