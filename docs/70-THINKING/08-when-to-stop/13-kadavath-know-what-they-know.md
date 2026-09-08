# Language Models (Mostly) Know What They Know

## Density

**Density: HIGH** — Almost the whole paper is measurement rather than argument, and the two central observables it defines (P(True), P(IK)) are exactly the two shapes a self-assessment signal can take inside an agent loop, so the load-bearing fraction that touches the Subject is unusually high; the padding is mostly repeated per-dataset figures in the appendix.

## Name, keywords, year, venue

**Name.** Saurav Kadavath, Tom Conerly, Amanda Askell, et al. (Anthropic). "Language Models (Mostly) Know What They Know."

**Authors.** Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan Perez, Nicholas Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli Tran-Johnson, Scott Johnston, Sheer El-Showk, Andy Jones, Nelson Elhage, Tristan Hume, Anna Chen, Yuntao Bai, Sam Bowman, Stanislav Fort, Deep Ganguli, Danny Hernandez, Josh Jacobson, Jackson Kernion, Shauna Kravec, Liane Lovitt, Kamal Ndousse, Catherine Olsson, Sam Ringer, Dario Amodei, Tom Brown, Jack Clark, Nicholas Joseph, Ben Mann, Sam McCandlish, Chris Olah, Jared Kaplan. All Anthropic.

**Year / venue.** 2022. arXiv preprint 2207.05221; the version read here is v4, dated 21 November 2022. Not peer-reviewed.

**Keywords (mine).** Calibration; self-evaluation; P(True); P(IK); selective prediction; honesty; format sensitivity; out-of-distribution calibration failure; value head probe; verification-versus-generation scaling.

## Approach

The paper builds a ladder, and each rung is a separate experiment.

The first rung is plain calibration on multiple choice. The authors ask whether a language model's assigned probability over lettered answer options matches the frequency with which those options are in fact correct. They test this across a very wide task set and across model sizes.

The second rung converts that calibration into something usable on open-ended work. Because a calibrated multiple-choice distribution only ranks options against each other, the authors reformulate tasks as True/False judgements about a single proposed answer. The prompt shows a question, shows a proposed answer, and asks the model to pick "(A) True" or "(B) False"; the probability the model assigns to "(A)" is read off as P(True).

The third rung applies that True/False machinery to the model's own generated samples. The model first answers a question by sampling at temperature 1, and then the same model is asked P(True) for its own sample. This is self-evaluation without any finetuning — it is purely a prompting arrangement.

A variant of the third rung shows the model several of its own samples ("Here are some brainstormed ideas: ...") before asking it to judge one specific candidate.

The fourth rung leaves proposed answers behind entirely. The authors attach a value head to the model and finetune it to output P(IK), the probability that the model itself will answer a given question correctly, given only the question. They then study how far that trained head generalizes: to unseen task distributions, to contexts that contain relevant source material, and to contexts that contain hints.

The crucial framing distinction the authors draw is that P(True) asks a question about the world (is this answer correct, as humans would judge it) while P(IK) asks a question about the model (will *I*, this particular model, get this right).

## Models targeted

A series of decoder-only language models at 800M, 3B, 12B, and 52B parameters. The architecture and training setup match Bai et al. 2022, except these were pretrained on 850B tokens rather than 400B. Smaller models were excluded because they do too poorly on the evaluations to be informative. None were finetuned on Python code, though roughly 10% of the pretraining mix is code. Section 3.3 additionally touches helpful-and-harmless RLHF policies finetuned from these same base models, but everything else in the paper concerns pure language models. Section 5.5 introduces a second 12B model with a deliberately different pretraining distribution, used as a comparison partner.

## Benchmarks and datasets

Multiple choice: all the multiple-choice tasks in BIG Bench, MMLU, TruthfulQA, LogiQA, and QuALITY.

Open-ended sampling: TriviaQA, Lambada, GSM8k (solved with chain-of-thought/scratchpad prompting, so full written solutions are judged), the Codex HumanEval, a set of basic arithmetic problems the authors assembled ("Mixed-Arithmetic"), and a set of naturally occurring Python function synthesis problems scraped from GitHub. The GitHub set exists because HumanEval is small.

For the source-material experiment they reuse the Wikipedia documents that ship with TriviaQA. For the hint experiment they construct hints from GSM8k ground-truth solutions, plus two contrast conditions: bad model-generated hints, and hints lifted from unrelated questions.

## Author incentive

Every author is at Anthropic, and the paper is explicitly framed as groundwork for training honest models — "honesty" being one of the properties Anthropic markets its assistants on. The models studied are Anthropic's own unreleased internal models, and the RLHF policies are Anthropic's. So the paper has a direct position stake: a favourable result supports the claim that a commercially deployed assistant can be made to report its own confidence reliably. Against that, the paper is unusually forthcoming about negative results — the "none of the above" failure, the poor out-of-distribution calibration of P(IK), the format dependence, the naive miscalibration of the RLHF policy — and the title itself hedges with "(Mostly)". No external funding is declared; this is in-house industrial research.

## Measurement methodology (brushed)

The dependent variables are of three kinds and the paper keeps them deliberately separate.

*Calibration* is measured by binning predicted probabilities and plotting predicted probability against observed frequency. To reduce a curve to one number the authors compute Expected Calibration Error as the mean absolute gap between predicted probability and observed frequency, always over 10 bins with an equal *number of predictions* per bin rather than equal bin widths. They note this quantity has also been called mean absolute deviation calibration error. For ECE on multiple choice they use only the most likely prediction, to match convention, while their calibration *charts* use all predictions. They also report RMS calibration error, which they say is better motivated theoretically but less used.

*Discrimination* is measured by AUROC, separating questions the model can answer from those it cannot, or samples that are correct from those that are not. They point out that AUROC is indifferent to calibration; chance is 0.5.

*Combined* performance is measured by Brier score, which folds discrimination and calibration together; chance on a binary task is 0.25, lower is better.

A fourth, deliberately pragmatic quantity is *conditional accuracy*: the accuracy on the subset of samples the model labelled P(True) > 0.5, compared against the base accuracy on the whole task. This is the number that matters if you intend to actually filter on the signal.

Ground-truth P(IK) is defined operationally as the fraction of 30 temperature-1 samples that are correct for a given question. Training labels are built by replicating hard labels in proportion — 20 correct samples out of 30 becomes 20 (Q, IK) datapoints and 10 (Q, IDK) datapoints — as a convenience for approximating a soft label with cross-entropy on hard labels.

What is controlled: model size is the main swept variable throughout, with the same tasks and formats held fixed across the 800M–52B series. Shot count (0-shot, 5-shot, 20-shot) is swept as a second axis. Format is swept as a third (lettered choices, BIG Bench default, "none of the above", True/False). The training distribution for P(IK) is swept as a fourth (TriviaQA only versus all four tasks).

On N and significance: sample sizes are given per dataset implicitly rather than tabulated, and the paper does not report confidence intervals, error bars, or significance tests anywhere I found. Claims are made from the visible consistency of trends across four model sizes and many datasets rather than from any inferential statistic. The authors do flag when a metric is misleading — for instance that the Brier score on GSM8k is dominated by questions the model gets wrong and has low P(IK) for, and that Brier scores fail to improve with size on Codex because small-model samples are almost always invalid and therefore trivially easy to score.

One methodological caveat the authors raise themselves, in a footnote, is that P(IK) as defined can be gamed by chance: "Name a composite integer in the range [1,100]" yields an apparent ground-truth P(IK) around 0.75 purely from random sampling, with no knowledge involved. Another footnote notes that models have no explicit way to distinguish tokens they generated from tokens handed to them by a third party, which makes self-evaluation ambiguous in principle.

## Key findings

### Calibration on multiple choice, and its dependence on format

Large models are well calibrated on a very diverse multiple-choice set — all of BIG Bench's multiple-choice tasks, MMLU, TruthfulQA, QuALITY, LogiQA — provided the questions are presented with lettered options and the model need only emit the letter. Calibration improves with model size and improves again when moving from 0-shot to 5-shot. The authors report no noticeable correlation between a task's accuracy and its calibration error within BIG Bench, which they take to mean calibration is not simply a by-product of being good at the task.

The format dependence is not a minor caveat; it is one of the paper's load-bearing observations. Under the BIG Bench default format, where the model must rewrite the whole answer string rather than emit a letter, calibration is measurably worse. The authors give the reason plainly: the model must be able to see the answer choices explicitly before choosing among them, otherwise paraphrase and specialization degeneracies ("Washington" versus "George Washington, the first US president") spread probability mass across equivalent strings. They also note that in their favoured format each option corresponds to a single token, which they expect makes calibration easier. On TruthfulQA specifically they observe that in this visible-choice format they do *not* see the inverse-scaling behaviour that task is known for.

The "none of the above" experiment sharpens what the good calibration does and does not show. Replacing the final MMLU option with "none of the above" degrades accuracy substantially and degrades calibration on that option badly; the 52B model is strongly biased against selecting it and fails to use it at an appropriate frequency. This did not improve at 5-shot, and did not improve at 20-shot either. The authors' reading is that a calibrated multiple-choice distribution only establishes that the model can weigh several concrete options against each other, not that it can judge any single option's correctness on its own terms.

The True/False reformulation is their route around that limitation. Recast as "here is a question, here is a proposed answer, is it (A) True or (B) False", models are again well calibrated on BIG Bench, with accuracy and calibration both rising with capability. The 52B model is well calibrated except near the tails, where it is overconfident.

### RLHF policies

Helpful-and-harmless RLHF policies finetuned from these same base models look badly miscalibrated at face value, which the authors attribute to RL finetuning collapsing the output distribution toward high-reward behaviour. A single temperature adjustment — T = 2.5, the same value across three different evaluations — largely restores calibration. They are careful to say that more intensive RL training might distort calibration in ways a temperature rescale cannot fix.

### P(True): self-evaluation of the model's own samples

Applied to the model's own temperature-1 samples across TriviaQA, Lambada, arithmetic, GSM8k (with chain-of-thought solutions judged in full), and the Codex HumanEval, P(True) separates correct from incorrect samples, and almost every measure improves with model size.

Self-evaluation is harder than judging human-written options, and the authors show this in two ways. Zero-shot, P(True) is poorly calibrated and typically sits near 50% for typical samples. And in a cross-evaluation experiment where samples from a model of one size are judged by a model of another size, samples from smaller models are universally easier to categorise, for evaluators of every size — while evaluation quality rises with the evaluator's size, including when a model evaluates its own samples.

The distinction between discrimination and calibration matters here. The authors state that larger k in k-shot self-evaluation helps primarily by improving *calibration*, not by improving the AUROC that separates correct from incorrect. So few-shot buys you trustworthy numbers rather than better sorting.

The pragmatic result is conditional accuracy. Restricting to samples the model labelled P(True) > 0.5 yields accuracy substantially above the base task accuracy, and the gap between base and conditional accuracy *widens* with model size. The authors read this as verification improving faster than generation as capability scales — "verification is often easier than generation" — and they flag it as non-trivial precisely because sample quality is improving at the same time.

### Showing the model many of its own samples first

Generating five temperature-1 samples, showing them all as "Here are some brainstormed ideas", and only then asking about one specific candidate improves self-evaluation significantly on all short-form tasks. The authors liken it to self-consistency prompting while noting the difference: here the model is shown its own samples and asked to judge, rather than the experimenters computing consistency externally. The gain is smaller on the long-form tasks, Codex and GSM8k. By Brier score, 20-shot evaluation with comparison examples is the best of the three methods in every case; but the authors add that for Codex and GSM8k the fixed prompt sometimes beats 20-shot on conditional accuracy, possibly because those have long-form answers.

They warn twice against reading the Brier-score size trends naively: on Codex, arithmetic and GSM8k the trends look unpromising only because small models get nearly everything wrong, so predicting P(True) near 0 uniformly earns a low Brier score trivially.

### P(IK): the model predicting its own answerability

Because the value head is new and untrained, P(IK) cannot be elicited zero- or few-shot; it must be finetuned. Trained on TriviaQA, the 52B classifier separates held-out TriviaQA questions it will get right from those it will not, and is very well calibrated in-distribution. Calibration error in-distribution shrinks as model size grows.

Out of distribution, the picture splits cleanly into discrimination and calibration.

Discrimination generalizes partially, and generalizes better with scale: AUROC on Mixed-Arithmetic, Lambada and Python function synthesis rises with model size for a classifier trained only on TriviaQA. Table 1 gives the 52B numbers as AUROC / Brier, training on TriviaQA only versus training on all tasks except GSM8k — TriviaQA 0.864 / 0.151 versus 0.873 / 0.145; Mixed-Arithmetic 0.928 / 0.194 versus 0.987 / 0.042; Lambada 0.606 / 0.431 versus 0.853 / 0.108; Python function synthesis 0.687 / 0.164 versus 0.881 / 0.109; GSM8k 0.624 / 0.200 versus 0.752 / 0.121. Note that GSM8k is out of distribution in *both* columns, and that on GSM8k the ground-truth threshold is binarized at 0.25 rather than 0.5 because so few problems exceed 0.5.

Calibration does not generalize. The authors say OOD calibration of P(IK) is often quite poor and that models are for the most part *underconfident* out of distribution. Lambada is the extreme case: calibration was "terrible" because the classifier emits uniformly low P(IK) scores across the board — an AUROC of 0.606 with a Brier score of 0.431, which is worse than the 0.25 chance Brier score. Training on all four distributions repairs this. On GSM8k, training on more diverse data changes the failure mode rather than removing it: the model shifts from mostly underconfident to overconfident.

Training on the target distribution helps substantially everywhere, which the authors themselves read as evidence of a significant remaining generalization gap. Their summary of section 5 is that they find only *partial* generalization.

### P(IK) responds to information added to the context

This is the paper's most striking generalization result, because the classifier was trained only on bare questions.

With source material: the obscure question "What state's rodeo hall of fame was established in 2013?" draws P(IK) of 18% from the 52B model; prepending the relevant Wikipedia article raises it to 78%. Quantitatively, across TriviaQA questions paired with their accompanying Wikipedia documents (truncated to 7000 tokens to fit context), including the article raises average P(IK), and shorter articles raise it more — the authors' explanation being that the answer is easier to locate in a short article than a long one.

With hints: on GSM8k, revealing progressively larger fractions of a ground-truth solution hint raises P(IK) monotonically. Good hints drawn from ground-truth solutions produce higher P(IK) than bad hints (chain-of-thought samples selected because they lead to a wrong answer), though the authors are explicit that the model is *partially fooled* by bad hints. Distracting hints — hints generated for a different question entirely — actually decrease P(IK). The classifier trained on all four tasks behaves better and more consistently here than the TriviaQA-only one, especially with partial hints. All of this is generalization, since no model was trained on GSM8k.

The authors read the source-material and hint results as suggesting a connection between how models store long-term memory and how they use in-context information — that is, a link between learning and in-context learning.

### Is P(IK) about the model, or about task difficulty?

The authors take this challenge seriously, since a classifier that merely predicts "this is a hard question" would not be self-knowledge. They compare two 12B models with identical architecture but different pretraining data (A: four repetitions of a high-quality dataset; B: one copy of that dataset mixed with a larger low-quality web distribution), each finetuned for P(IK) on the TriviaQA questions it personally got right. Restricting to the 650 and 826 TriviaQA questions that only A or only B answers correctly, the diagonal beats the off-diagonal: A's average P(IK) is 0.463 on questions only A gets right versus 0.408 on questions only B gets right, while B's is 0.409 versus 0.477. The authors state plainly that this is only about a 6% difference and that there is room for improvement.

A second cross-experiment trains P(IK) classifiers on each model's ground-truth data starting from each model's checkpoint. Results are mixed: testing on model B's ground truth, starting from B beats starting from A (0.8717 / 0.1443 versus 0.8460 / 0.1582); testing on model A's ground truth, the two initializations are indistinguishable (0.8633 / 0.1491 versus 0.8631 / 0.1497). Restricting to questions where the models differ gave similar results.

So the paper establishes that P(IK) carries *some* model-specific signal, and is honest that the effect is small.

### Cheaper baselines that discriminate but do not calibrate (Appendix B)

Three unsupervised alternatives to a trained head are tested, all of which discriminate somewhat without providing calibrated probabilities.

Mean per-token loss on the greedy (T = 0) sample separates correct from incorrect answers on TriviaQA, and predicts pass@1 on HumanEval well enough that high-loss problems are reliably ones the model does poorly on. They deliberately use mean rather than summed loss so that answer length does not confound, noting that on HumanEval harder questions naturally need longer answers.

Entropy of the answer distribution, H(A|Q), estimated from 200 samples, tests the hypothesis that hallucinations are diverse — that a model which knows an answer concentrates its sampling distribution. It has predictive power on TriviaQA and on HumanEval pass@1. But the authors report a *negative* AUROC trend with model size on HumanEval and explain why: larger models solve harder problems and often produce a diverse set of answers that are all correct. This directly contradicts the underlying hypothesis, and they conclude H(A|Q) is not a robust measure of whether a model knows an answer, particularly as models grow.

Stuffing 30 temperature-1 samples into a single context and taking the mean token loss over that context is a third diversity proxy. It has some discriminative power, and shows the same negative size trend on HumanEval for the same reason.

### The authors' own reading

Their stated core findings are that large models are well calibrated on diverse multiple choice, that they perform well at self-evaluation across a range of subjects, and that they can be trained to predict what they do and do not know with some generalization to new domains and to in-context information sources. They frame all of it as groundwork for "honesty", an umbrella term they decompose into truthfulness, calibration, self-knowledge, explainability and non-deceptiveness, and they say explicitly that they are only scratching the surface. They expect these signals can be leveraged to bootstrap more extensive self- or inter-model supervision, and to distil calibration back into open-ended natural-language responses.

## Open questions the paper itself raises

The authors list four limitations explicitly in section 6.1.

First, they studied pretrained language models, and they state that models finetuned for a specific purpose — RLHF policies being their example — will not be so well calibrated, and that some of the methods here may not work as well on them.

Second, and this is the caveat the reading brief singles out: pretraining is a form of human imitation. The most interesting honesty questions concern systems that know something clashing with or extending what humans know, which cannot have been acquired by imitation. The authors say directly that their analysis does not differentiate between "the truth" and "what humans say", and that they would eventually like to train systems that recognize the distinction and generalize appropriately. Nothing in this paper speaks to models trained on objectives other than imitation.

Third, the work does not address the possibility that systems learn to behave deceptively — for instance to maximize human preference reward — and they note that intentional deception would counteract the simple trends in honest self-evaluation they report.

Fourth, they concede that their generalization observations are limited in power and scope, resting on only five sampling-based datasets, and say it would be interesting to investigate more thoroughly and precisely.

Beyond that list, the paper leaves several questions open in passing. The natural-language route to P(IK) — literally asking "With what confidence could you answer this question?" with a 0%–100% answer — was tried, showed no major gains few-shot out of distribution in early experiments, and was abandoned in favour of the value head; the authors say they believe it worth returning to. The 6% diagonal-versus-off-diagonal margin in the cross-model experiment is explicitly labelled as leaving room for improvement. The mismatch between what P(IK) is supposed to mean and what it operationally measures is raised only in a footnote (the composite-integer example, where chance sampling yields an apparent P(IK) of 0.75) and is not resolved. And the observation that models cannot distinguish their own tokens from third-party tokens is raised as a possible confound for self-evaluation, with a pointer to the RL setting, without being tested.

## Appreciation

I want to keep two things apart here, because the paper's contribution is much stronger on one axis than the other.

### Mechanism

The mechanisms are simple, cleanly separated, and reusable, and this is the paper's real contribution.

The first mechanism is the separation of two distinct self-assessment questions that are easy to conflate. P(True) asks a question about the world — is this particular answer correct — where the model happens to be the one that proposed the answer. P(IK) asks a question about the model — will I get this right — with no candidate answer in play. These require different machinery (prompting versus a finetuned value head), have different failure modes, and answer different operational needs. Making that distinction explicit is worth more than any single number in the paper.

The second mechanism is the reduction of open-ended self-assessment to a single-token binary choice whose probability can be read off directly. Sampling an answer, then re-presenting it in a True/False frame and reading P("(A)"), turns an unbounded generation problem into a place where calibration can be measured at all.

The third mechanism is the discrimination/calibration decomposition, held consistently throughout via AUROC versus ECE, with Brier score as the combined measure. The paper repeatedly shows these two moving independently — few-shot improves calibration without improving AUROC; P(IK) out of distribution keeps its AUROC while its calibration collapses. That decomposition is a durable analytical tool regardless of whether the specific magnitudes hold up.

The fourth mechanism is the brainstorming variant: showing a model several of its own samples before asking it to judge one. It is a cheap intervention with a clearly stated cost (extra samples) and a clearly stated limit (helps less on long-form answers).

The fifth is the operational definition of ground-truth P(IK) as the fraction of temperature-1 samples that are correct. This makes "does the model know this" measurable, and the authors are honest that the definition admits degenerate cases.

Also worth crediting as mechanism: the negative results are as informative as the positive ones. The "none of the above" failure isolates exactly what multiple-choice calibration does not demonstrate. The entropy result in Appendix B is a hypothesis stated, tested, and falsified by its own size trend, and the authors say so rather than burying it.

### Magnitude

The magnitudes are much weaker, and should be held loosely.

There are no error bars, no confidence intervals, and no significance tests anywhere in the paper. Every trend claim rests on the eye's reading of four points on a log-parameter axis. The largest model is 52B, and the whole model series is proprietary and unreleased, so none of the scaling claims can be checked or reproduced externally.

The headline generalization effect in section 5.5 — the claim that P(IK) encodes model-specific knowledge rather than task difficulty — is a roughly 6% gap on averages, from two models, one of which shows the effect and one of which does not in the second experiment. The authors say this themselves. It is suggestive, not established.

Several reported magnitudes are actively misleading unless you read the caption, and the authors flag them: Brier scores on Codex, arithmetic and GSM8k that fail to improve with size only because small models get everything wrong; the GSM8k Brier score dominated by low-P(IK) incorrect questions; a GSM8k threshold moved from 0.5 to 0.25 because too few problems clear 0.5. The Lambada OOD Brier of 0.431, worse than chance, shows how far the calibration numbers can fall.

Absolute values are also anchored to 2022 base models on 2022 benchmarks. TriviaQA and Lambada base accuracies in the 0.5–0.8 range and Codex accuracies under 0.45 mean the conditional-accuracy gains are measured in a regime where the model is wrong very often. The direction of the trend may survive; the numbers themselves will not transfer.

## How it could serve a harness-design effort

Read against the Subject — an agent loop deciding whether the current attempt has succeeded, is stalling, or is beyond it — this paper supplies primitives rather than a stopping policy. It never runs a loop, never takes an action, and never makes a decision; every experiment is single-shot question answering. What it offers is a careful characterisation of the signals such a loop would have to be built on.

The most directly usable result is conditional accuracy. If a harness filters or gates on the model's own P(True) > 0.5 for a proposed answer, the retained work is measurably more accurate than the unfiltered work, and the paper's evidence is that this margin grows with model capability. That is the empirical basis for a self-assessment gate being worth anything at all.

The P(True)/P(IK) distinction maps onto two different harness questions. "Is this artifact I just produced correct?" is P(True), needs a candidate in hand, and works from prompting alone. "Should I attempt this task at all, or hand it off?" is P(IK), needs no candidate, and — importantly — requires training in this paper's setup, since P(IK) could not be elicited zero- or few-shot. A harness wanting a pre-attempt triage signal cannot get one for free from a base model by this paper's method.

The source-material and hint results bear directly on a loop that adds context between attempts. P(IK) rises when relevant material enters the context and rises further as more of a hint is revealed, and falls for irrelevant material. That means a self-assessment signal can in principle track whether a retrieval step or a context addition actually helped — which is exactly the "am I making progress" judgement the Subject names. The caveat is that bad hints only partially depress it: the model was measurably fooled by plausible-but-wrong reasoning it had generated itself.

Appendix B is the cheap-signal menu for a harness that cannot afford a second model call: sample loss and answer-distribution entropy both discriminate to a degree, with no calibration. But the entropy result carries a specific warning for agentic use — its discriminative power *decreases* with model size on the code task, because capable models produce many different correct programs. Any harness that treats disagreement among samples as evidence of not knowing will get this backwards on exactly the open-ended tasks agents are used for.

### Limitations and major concerns for that use

The format sensitivity is the concern I would weigh most heavily. Calibration is good "in the right format" — visible lettered options, single-token answers, few-shot. Agent loops do not naturally produce that shape: their artifacts are long-form, their success criteria are not enumerable options, and there is often no fixed set of alternatives to weigh. The "none of the above" failure is the closest thing in the paper to an agent's actual predicament — judging whether any available option is right, rather than which of several is best — and it is where the models did worst and where more shots did not help. A harness needs the model to judge a single artifact on its own terms, which is the case this paper shows to be hardest.

The out-of-distribution calibration failure is the second concern. An agent harness is by construction a distribution shift relative to any P(IK) training set. The paper's evidence is that discrimination survives such a shift partially and calibration does not, and that the direction of miscalibration is not even stable — underconfident on Lambada, overconfident on GSM8k once trained more broadly. A harness that reads P(IK) as a probability and sets a numeric threshold on it is relying on precisely the property that fails to transfer. Reading it as a ranking is better supported.

Third, self-evaluation is calibrated only few-shot; zero-shot P(True) sits near 50% and is poorly calibrated. Every use of the signal costs comparison samples and prompt budget, and the brainstorming trick that helps most helps least on long-form answers — again, the agent-relevant case.

Fourth, RLHF policies are miscalibrated out of the box and needed a temperature rescale to recover. Deployed agent models are finetuned models. The paper's own limitation section says the methods may not work as well on them, and offers a fix that was tuned on a single value across three evaluations, with no claim it survives heavier RL.

Fifth, and most fundamental for the Subject: everything here is *self*-evaluation of a single answer against external fact, in a setting where an oracle exists to score correctness. An agent loop rarely has that. Trajectory-level signals — no state change, repeated actions, exhausted budget — are entirely outside this paper's scope, as is any notion of partial progress, and the paper offers no evidence that P(True) or P(IK) means anything when applied to a partially complete piece of work rather than a finished candidate answer.

Sixth, the deception limitation is not academic for harness design. The paper explicitly does not address models that learn to behave deceptively, and notes that deception would counteract the honest self-evaluation trends. A harness that routes decisions on a model's self-report creates exactly the optimization pressure that concern names.

## Five citations worth chasing next

1. **Lin, Hilton and Evans (2022), "Teaching models to express their uncertainty in words."** The authors name it as one of the two works most similar to theirs; it trains models to state calibrated confidence in natural language and studies a signal analogous to P(True). It is the direct alternative to the value-head route that this paper tried and set aside, and verbalized confidence is the form an agent harness would most easily consume.

2. **Mielke, Szlam, Boureau and Dinan (2020), "Linguistic calibration through metacognition: aligning dialogue agent responses with expected correctness."** Named as "perhaps the work most similar to ours", and it is set in dialogue rather than single-turn QA, which is closer to a loop.

3. **Varshney, Mishra and Baral (2022), "Investigating selective prediction approaches across several tasks in iid, ood, and adversarial settings."** This is the abstention literature the Subject names, and it addresses exactly the OOD regime where this paper's P(IK) calibration breaks down.

4. **Christiano, Cotra and Xu (2021), "Eliciting latent knowledge."** Cited for the distinction between what a model reports and what it internally knows — the gap that the authors' own "truth versus what humans say" limitation points at, and the one that matters if a harness is to trust self-reports.

5. **Ortega et al. (2021), "Shaking the foundations: delusions in sequence models for interaction and control."** Cited in the footnote about models being unable to distinguish their own tokens from third-party tokens, and about the trouble this causes in an RL setting. That is a sequential-decision-making paper, and it is the one reference here that speaks to the agent-loop setting rather than to single-shot QA.

A sixth worth noting if the entropy-style signals are of interest: **Wang et al. (2022), "Self-consistency improves chain of thought reasoning in language models"**, which the authors invoke twice as the external-judgement counterpart to their brainstorming intervention.
