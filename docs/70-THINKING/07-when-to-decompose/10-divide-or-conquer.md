# Divide-or-Conquer? Which Part Should You Distill Your LLM?

## Density

**Density: HIGH** — almost the entire paper is an experiment on the split between deciding *how* to break a task up and actually *doing* the pieces, which is the Subject itself; the padding is confined to the related-work section and a couple of prompt-ablation tables.

**Keywords (mine):** decomposition/solving separation, capability distillation, static vs dynamic planning, cheap planner + strong executor, cross-domain transfer of a decomposer, inference cost accounting, knowledge-intensity vs abstractness of a capability.

**Year:** 2024 (arXiv v1 Feb 2024, v3 Nov 2024).
**Venue:** Findings of the ACL: EMNLP 2024 (DOI 10.18653/v1/2024.findings-emnlp.145). Peer-reviewed.
**Authors:** Zhuofeng Wu (U. Michigan, work done during an Apple internship), He Bai, Aonan Zhang, Jiatao Gu (Apple), VG Vinod Vydiswaran (U. Michigan), Navdeep Jaitly, Yizhe Zhang (Apple).
**Code:** https://github.com/apple/ml-divide-or-conquer

## Approach

The paper takes the by-then-standard observation that LLMs reason better when pushed to solve subtasks first, and asks a different question of it: *if the pipeline is split in two, which half do you actually need the expensive model for?*

Their frame names two capabilities that are normally entangled in one monolithic model:

1. **Decomposition / planning** — breaking a complex objective into subgoals. They argue this rests on semantic understanding and query parsing; it is "logical and abstract rather than knowledge-intensive".
2. **Solving / execution** — recalling and applying large amounts of memorised world knowledge to actually answer.

The paper's running example: decomposing *"who is older, Messi or Ronaldo?"* into *"how old is Messi?"*, *"how old is Ronaldo?"*, *"who is older?"* needs only text comprehension; answering needs facts.

**How the two phases are separated.** They deliberately choose a **static** two-stage pipeline rather than an interactive one. Stage 1 (Decomposition): the model is given an instruction `I_decomp` plus the question `Q` and, *without being shown or asked for any solution*, emits a set of subquestions `{S_i}` — capped at three by the instruction, with a licence to return "No decomposition" if the question does not need splitting. Stage 2 (Solving): a second instruction `I_ans` hands the solver the premise `P`, the original question `Q`, and the whole subquestion list at once; the solver answers the subquestions one by one and then emits the final answer in a fixed `"The answer is: "` format. No subquestion is conditioned on the answer to an earlier one — this is what makes the split clean, and the paper is explicit that the choice is methodological: a static pipeline "would enable us to have a clearer separation of the decomposition and solving." They call the baseline of a single prompt doing everything the **Single-Stage** model, and this pair the **Two-Stage** model. Naming HuggingGPT as the precedent for plan-then-execute, and Least-to-Most / self-ask as the interactive alternative.

**Distillation.** With the split in place, each half can be replaced by a small finetuned student independently:

- **Student decomposer `S_D-T`**: sample teacher decompositions `T(I_decomp, Q) → {S_i}`, finetune a small model on that pair by cross-entropy. No human-annotated subquestions anywhere — the decomposition supervision comes entirely from the teacher.
- **Student decomposer `S_D-R`**: same, but when the dataset carries a ground-truth answer `A`, first run the teacher's own solver on each candidate decomposition and **discard the training instance if the resulting answer is wrong** (`Â ≠ A`). A rejection-sampling filter on decomposition quality, scored indirectly through downstream task success rather than by judging the subquestions themselves. Costs training data.
- **Student solver `S_E-T`**: the mirror-image experiment, finetuned on `T(I_ans, {S_i}, Q) → ({Â^s_i}, Â)` — i.e. it learns to reproduce the teacher's subanswers *and* final answer.
- **Student solver `S_E-A`**: same targets but with the oracle answer `A` substituted for the teacher's final answer.

The symmetry is the point: identical backbone, identical teacher, identical data volume, one half distilled at a time, and the other half held at GPT. That is the instrument for the paper's central claim.

## Models targeted

- **Teacher throughout:** GPT-3.5-Turbo-0615. Treated strictly as a black box — the paper notes that classic KD assumes access to the teacher's logits and that this is unavailable for the models people actually want to compress, so they train on generated data (the Vicuna/Alpaca recipe) instead of minimising KL.
- **Students / backbones:** Vicuna-13B-v1.3 (the main workhorse) and Mistral-7B-Instruct-v0.3 (the backbone-robustness check).
- **Evaluation-time solvers (to test what a distilled decomposer plugs into):** Vicuna-13B, text-davinci-003, GPT-3.5-Turbo, GPT-4.

Model-size ratio matters for the argument: a 13B or 7B student standing in for a model the paper estimates (loosely, from GPT-3) at 175B.

## Benchmarks / datasets

- **GSM8K** (Cobbe et al. 2021) — grade-school math word problems; 7.5K train / 1K test. Scored by exact match.
- **DROP** (Dua et al. 2019) — discrete reasoning over paragraphs, reading-comprehension QA; 77.4K train, 9.5K dev used for evaluation. Scored by F1.
- **Bamboogle** (Press et al. 2022) — 125 hand-written two-hop compositional questions, no training split of its own. Scored by accuracy.

Three datasets, deliberately of different character: one arithmetic-chain, one text-grounded, one compositional multi-hop. The DROP/GSM8K pair is what carries the cross-domain generalisation test, because the two demand genuinely different solver expertise.

**Training details.** Batch size 128, LR 2e-5, 3 epochs on DROP and 5 on GSM8K/Bamboogle "until convergence", all finetuning under 12 hours on 8×A100-80G.

## Author incentive

Apple, with a University of Michigan co-affiliation and the first author explicitly an Apple intern. No stated external funding; the code is released under Apple's GitHub org. The relevant stake is directional rather than commercial in any narrow sense: Apple's interest lies in small locally-runnable models that keep useful behaviour, and the paper's headline result — that you can move the expensive-but-compressible half onto a small local model while renting the knowledge-heavy half — is a conclusion that suits that posture. It is also a conclusion that reads as a partial *negative* result for distillation (solving does **not** compress), which cuts against a simple "our small models are enough" pitch, so the incentive is not one-directional. The teacher is a competitor's API, which removes any incentive to flatter it.

## Measurement methodology (brushed)

**Dependent variables.** Two, reported side by side in the main table: task accuracy (EM / F1 / accuracy per dataset) and **inference expense in dollars**.

**What is controlled.** The core design is a two-cell swap on a fixed pipeline. Holding the pipeline shape, the prompts, the teacher, the backbone and the training recipe fixed, they replace *the decomposer* with a student while the solver stays GPT, and separately replace *the solver* with a student while the decomposer stays GPT. Everything reported hangs on that one substitution being the only difference between rows. The Single-Stage rows (GPT alone, Vicuna alone) anchor the bottom.

**How inference cost is measured.** This is worth stating precisely, because the paper's cost claims are entirely an accounting exercise, not a latency or hardware measurement:

- Token prices are taken from GPT-3.5-turbo-1106: $0.001 / 1K input tokens, $0.002 / 1K output tokens.
- The student's cost is **not measured** — it is *derived* by scaling the GPT price down by the parameter-count ratio (13B against an assumed 175B), giving $7.42e-5 / 1K input and $1.48e-4 / 1K output for Vicuna-13B. They flag this as deliberately conservative, on the grounds that OpenAI has optimised its serving stack in ways the comparison cannot credit.
- Crucially, **cost is reported split as `decomposition / solving`** for every row of Table 1. That decomposition of the cost figure is what lets the paper localise where the money goes, and it is the measurement choice that makes the whole argument legible.
- In the static-vs-dynamic ablation the currency changes to **raw token counts** over the whole evaluation set, which sidesteps the price-model assumption entirely for that one comparison.

**N and significance.** N is the standard evaluation split size (1K GSM8K test, 9.5K DROP dev, 125 Bamboogle), with some ablations run on unspecified *subsets* of GSM8K/DROP. **No confidence intervals, no error bars, no seeds, no significance tests anywhere in the paper.** Single runs. Several of the differences the paper leans on are large enough that this hardly matters (a 20-point gap); several others — the 67.02 vs 65.13 that supports "the student decomposer matches or beats the teacher", and the 125-item Bamboogle numbers where one item is 0.8 points — are well inside the range where an untested single run cannot carry the claim being hung on it.

## Key findings

### 1. The static split beats a single stage, and the decomposer half is the sensitive one

Table 1, GSM8K / DROP / Bamboogle:

| Decomposer | Solver | GSM8K (EM) | DROP (F1) | Bamb (Acc) |
|---|---|---|---|---|
| — (single-stage) | GPT | 20.32 | 46.51 | 49.6 |
| — (single-stage) | Vicuna-13B | 9.40 | 26.68 | 33.6 |
| GPT | GPT | 65.13 | 55.73 | 54.4 |
| Vicuna-13B | GPT | 62.93 | 47.13 | 48.8 |
| GPT | Vicuna-13B | 28.13 | 21.29 | 32.8 |
| Vicuna-13B | Vicuna-13B | 28.51 | 20.90 | 29.6 |

Two-stage beats single-stage everywhere. Then, holding the solver at GPT, **downgrading only the decomposer** from GPT to vanilla Vicuna costs 2.2 / 8.6 / 5.6 points — the decomposer is load-bearing. The paper notes the exception: with Vicuna as the *solver*, decomposer quality barely registers on GSM8K (28.13 vs 28.51, i.e. inverted), and their reading is that the weak solver "is too erroneous to harness the improvement from the decomposition." Their stated rule: **the decrease from a weaker decomposer is more significant when the solver is more powerful**, therefore "a stronger decomposer is essential" for optimal performance.

### 2. Decomposition distils; solving does not

This is the paper's central claim, and the evidence for it is the asymmetry between two adjacent rows:

| | Decomposer | Solver | GSM8K | DROP | Bamb |
|---|---|---|---|---|---|
| w/o oracle | `S_D-T` | GPT | **67.02** | **55.19** | 52.0 |
| w/o oracle | GPT | `S_E-T` | **48.98** | **13.37** | 31.2 |
| w/ oracle | `S_D-R` | GPT | **67.78** | **57.97** | 52.0 |
| w/ oracle | GPT | `S_E-A` | **51.55** | **20.34** | 40.8 |

Distilling the decomposer into a 13B student **matches or exceeds the GPT teacher** (67.02 vs 65.13 on GSM8K; 55.19 vs 55.73 on DROP; 52.0 vs 54.4 on Bamboogle), and clearly beats the untuned Vicuna decomposer. Distilling the solver instead **collapses** performance — DROP falls from 55.73 to 13.37, GSM8K from 65.13 to 48.98 — even though the decomposition it receives is still the full-strength teacher's. With oracle answers the filtered decomposer `S_D-R` does better still, and **on DROP it beats the teacher outright** (57.97 vs 55.73), which the paper reads as local adaptation exceeding the black box on a target domain. The distilled solver improves with oracle answers too, but nowhere near closing the gap.

They also note (result omitted from the table) that a **single-stage student distilled from single-stage GPT was worse even than the GPT-decomposer + `S_E-T` combination** — so the failure is not merely "small models are bad", it is specifically that the solving role resists compression.

**Cost.** The split cost column is where the practical payoff sits. Decomposition cost per the accounting model drops roughly an order of magnitude when the student takes over: GSM8K $0.13 → $0.01, DROP $0.73 → $0.06, and the *solving* cost is unchanged (~$0.62 GSM8K, ~$0.96 DROP), since GPT still solves. The paper's own framing of why this is the right half to attack: decomposition is where the long generated reasoning chain lives, and "generating decomposed questions can be computationally expensive when the reasoning chain is long." Note that on these numbers the solving stage still dominates total spend — the saving is real but partial, roughly 15–40% of pipeline cost depending on dataset, not the order-of-magnitude the decomposition column alone suggests.

**Authors' reading.** Two mechanisms, stated as hypotheses rather than proven:
- *Knowledge-intensity.* "A strong solving capability is knowledge-intensive" — world knowledge cannot be squeezed into a model hundreds of times smaller from a few demonstrations, whereas decomposition "is typically more abstract, has lower information density, and is more universal."
- *Easy to distill, hard to acquire.* They pose the obvious objection to themselves — if decomposition is so learnable, why does the small model not have it already from pretraining? Their answer is that the skill is built on the teacher's "thorough digestion and internalization of vast amounts of data", but being logical rather than knowledge-bound, a few demonstrations suffice to transfer it. Their analogy: "finding a physics theorem from massive observations is much more challenging than learning the theorem in the class."

**Failure modes of the distilled solver**, per their own diagnosis: (a) the knowledge-compression problem above; (b) a target-format artefact — because the teacher's subanswers `{Â^s_i}` were part of the training target, the student sometimes **answers a subquestion instead of the primary question**. Appendix C illustrates a solver that answers subquestions 1 and 2 correctly, then gets confused by a third subquestion closely resembling the second and derails. Appendix A tests removing the subanswers from the target: this helps DROP a great deal (`S_E-A` 20.34 → 72.55) but destroys GSM8K (51.55 → 6.44), because math answers need the computation steps while DROP answers are largely extractive. They keep the subanswers in, as the GSM8K loss outweighs the DROP gain — an honest admission that the distilled-solver arm is sensitive to a target-formatting choice that has no single right setting across datasets.

### 3. The distilled decomposer generalises; the distilled solver does not

- **Across domains** (Table 3, train on one dataset, evaluate on the other): `S_D-R` trained on GSM8K, evaluated on DROP, scores 51.05 against the GPT decomposer's 55.73; trained on DROP, evaluated on GSM8K, 63.15 against 65.13. A modest drop in both directions. The distilled *solver* `S_E-A` under the same cross-domain move scores 7.98 and 11.30 — and, revealingly, is sometimes *better without any decomposer at all* (17.22 on DROP, 3.41 on GSM8K in the no-decomposer column), i.e. the numbers are in the noise of a broken model. Table 2 shows the cross-domain decomposer producing subquestions on DROP essentially identical to the in-domain one.
- **Across solvers** (Table 4): `S_D-R` is comparable to or better than the GPT decomposer against every solver tried — Vicuna-13B 31.5 (vs GPT's 28.0), GPT-3.5 66.5 (vs 66.0), GPT-4 91.5 (vs 90.5) on GSM8K, and 33.38 / 61.94 / 81.02 on DROP. The decomposer is a portable component. They observe that **weaker solvers gain more** from a better decomposer, hypothesising that strong solvers can partly decompose for themselves.
- **Across backbones** (Table 5, Bamboogle): the whole pattern replicates with Mistral-7B in place of Vicuna-13B, at generally higher absolute numbers (`S_D-R`/GPT reaching 60.0 against a 40.0 vanilla baseline).

### 4. Static beats dynamic, on both accuracy and cost

Ablation 6.1 pits their static pipeline against **self-ask** (iterative "are follow-up questions needed here?" until the model says no), with GPT-3.5-turbo doing both jobs in both arms:

| | Bamboogle EM | Bamboogle #tokens | GSM8K Acc | GSM8K #tokens |
|---|---|---|---|---|
| Dynamic | 53.6 | 59,792 | 62.92 | 823,886 |
| Static | 54.4 | 15,106 | 65.13 | 355,302 |

Static is slightly more accurate and uses **3.96× / 2.32× fewer tokens**. Their reading: dynamic pipelines need precise intermediate reasoning because "errors in intermediate steps can influence subsequent steps", and the iteration is what drives the token bill. They are careful to hedge — dynamic decomposition may win in other application scenarios, and finding the optimal framework is not their goal.

### 5. Learning to decompose damages the ability to solve

Ablation 6.2 is a small result with an outsized implication for architecture. Take `S_D-R` — a model finetuned only on decomposition — and ask it to *solve* instead: GSM8K 28.35 → 5.99, DROP 26.63 → 7.87, Bamboogle 32.8 → 17.6 relative to an untuned Vicuna solver. Losses of 15–22 points. Specialising a model for planning degrades its execution ability badly. The authors take this as vindication of the two-stage design itself: because decomposition is isolated in its own model, "solver's reasoning capability remains intact." It also means the two roles cannot simply be collapsed back into one finetuned model.

### 6. Prompt-level findings (Appendix B)

- Capping the decomposer at **"no more than three subquestions"** is the sweet spot on DROP: no restriction 45.69 EM, ≤4 46.40, **≤3 50.00**, ≤2 46.89. Both over- and under-splitting cost accuracy.
- A single in-context demonstration in the decomposition instruction helps every decomposer tested (e.g. Vicuna 57.0 → 61.5 on the GSM8K subset), and compresses the gap between decomposers — with GPT-4 as solver, 1-shot brings vanilla Vicuna, GPT-3.5 and `S_D-R` all to 91.5.

## Open questions the paper itself raises

Stated limitations, in their own framing:

- **Three load-bearing assumptions.** That the teacher can decompose effectively; that the student has the capacity to learn the distilled planning; and **that the tasks involved actually require long-horizon planning capability**. "If any of these assumptions do not hold true, it would impact the effectiveness of our proposed method." The third is the one they flag least but which most limits the result's reach.
- **Only math and QA have been tested.** They say plainly that completing the work requires evaluation "on a broader range of planning tasks... including benchmarks related to tool use, LLM agents, and multiturn scenarios," to verify versatility.
- **Static was chosen for clarity, not because it is optimal.** Repeated twice in the paper: their goal is to analyse which capability distils, "rather than seeking the optimal framework." They explicitly acknowledge "the potential of dynamic decomposition and its advantages in specific application scenarios," and suggest the distilled decomposer "can also potentially be integrated into more dynamic reasoning processes, enabling iterative solving and refinement based on intermediate outputs" — an untested extension.

Future work they propose:

- Train a **universal decomposer** on data pooled from many tasks — the natural next step given the cross-domain transfer they observed.
- Use **reinforcement learning to improve the decomposer using the solver's outcome as reward signal** — a stronger version of the rejection-sampling filter they already use, closing the loop between plan quality and downstream success.
- Extend to long-horizon planning: LLM agents, tool use, multiturn decision making.

## Appreciation

### MECHANISM — what transfers as an argument

- **The two capabilities are separable, and separating them is instrumentally useful even if you never distil anything.** The static two-stage design gives you a place to stand: a clean seam where either half can be swapped, measured, priced, and reasoned about independently. Most of what the paper learns is only visible *because* the seam exists. This is the most portable thing here.
- **The asymmetry itself.** Whatever the exact numbers, the direction is robust across three datasets, two backbones, oracle and no-oracle regimes, and four solvers: the planning role compresses into a small model, the executing role does not. The proposed mechanism — that planning is abstract and low-information-density while execution is knowledge-bound — is a plausible and *falsifiable* account, and it explains the failure mode observed rather than just labelling it.
- **A specialist decomposer is portable across solvers and domains.** That decomposition trained on math transfers to reading comprehension, and that the same decomposer improves Vicuna, GPT-3.5 and GPT-4 alike, argues that the plan is a genuinely separable artefact and not a solver-specific encoding. This is the finding with the longest reach beyond the paper's setup.
- **Gains from a better plan scale inversely with executor strength.** Consistent across two independent tables (5.1 and 5.3): weak solvers gain most from good decomposition; with GPT-4 as solver, decomposer quality nearly stops mattering (88.5 vs 90.5 vs 91.5). Both a design rule and a caution about where decomposition machinery is worth building.
- **Specialising a model for planning degrades its solving.** Section 6.2's 15–22 point losses are a real constraint on architecture: role separation is not free-form, and one finetuned model cannot hold both jobs.
- **Iteration costs tokens superlinearly relative to its accuracy return** — at least here. The dynamic arm spent 2.3–4× the tokens for no gain. The *mechanism* offered (error propagation through dependent steps) is general; whether it dominates is task-shaped.

### MAGNITUDE — numbers valid only inside this setup

- **Every dollar figure.** Student cost is not measured but *inferred* by dividing the teacher's API price by a parameter ratio against an assumed 175B GPT-3.5 — an assumption of unknown accuracy about a model whose size was never published. It also prices a hosted API against self-hosted weights, ignores fixed serving costs and utilisation, and ignores the ~12 A100-hours of distillation. The token counts in Table 6 are the only cost numbers I would carry outside this paper.
- **The size of the two-stage gain**, especially GSM8K 20.32 → 65.13. A 45-point jump implies the single-stage baseline was not doing chain-of-thought at all; GPT-3.5 scoring 20 EM on GSM8K is far below its commonly-reported CoT range. The paper distinguishes Single-Stage from CoT in prose but never reports a CoT-prompted single-stage row, so the headline improvement conflates *decomposing* with *being allowed to reason at length at all*. The relative ordering among two-stage rows is unaffected; the absolute size of "decomposition helps" is not trustworthy here.
- **`S_D-T` beating the teacher (67.02 vs 65.13) and `S_D-R` beating it on DROP (57.97 vs 55.73).** Single runs, no variance reported. Read as "matches", not "exceeds".
- **Everything on Bamboogle.** N=125. A 0.8-point difference is one item.
- **The `S_E-T` DROP collapse to 13.37** is partly an artefact, not a capability measurement — Appendix A shows the same model reaching 72.55 on DROP once the subanswers come out of the training target. The paper is honest about this, but it means the most dramatic single number supporting "solving does not distil" is substantially a formatting failure.

### The asymmetry I would press on

The comparison is presented as symmetric — swap one half, hold the other at GPT — but the two halves are not graded the same way. **A mediocre decomposition can be repaired downstream by a strong solver; a mediocre solution cannot be repaired by anything, because it is the output being scored.** The GPT solver sits between every decomposer defect and the metric, absorbing it; nothing sits between a solver defect and the metric. So part of what the experiment measures may be *error recoverability by position in the pipeline* rather than *intrinsic compressibility of the capability*. Two observations in the paper are consistent with this reading and hard to explain by knowledge-intensity alone: that decomposer quality barely matters when the solver is strong (GPT-4 absorbs the difference), and that it barely matters when the solver is weak on GSM8K (a broken solver cannot exploit any plan). The knowledge-intensity mechanism is plausible and probably part of the story; the paper does not do the work needed to separate it from the positional one — that would need a decomposition-quality metric scored directly rather than only through downstream task success.

A smaller note: the "Teacher/Student Models" paragraph says "we employ different levels of teacher models" where it evidently means *solver* models — a slip, but one that briefly obscures which model is doing what in the most important paragraph of the setup.

## How it could serve a harness-design effort — and where it stops

**What it opens up.**

The paper supplies a concrete argument for **heterogeneous model assignment by role**: if planning and executing are separable capabilities with different compressibility, then a harness that runs one model for everything is leaving something on the table, and the seam between decomposition and execution is a natural place to put a model boundary. It also supplies the diagnostic that makes such a decision measurable — **cost accounted per stage rather than per run**. A harness that reports one aggregate token bill cannot tell you which half to attack; splitting the cost column is what turned a vague "long chains are expensive" into a locatable target. That reporting habit transfers regardless of whether one adopts anything else here.

Section 6.2 raises a live design question rather than settling one: if specialising a model for planning damages its solving, then role separation may need to be *enforced structurally* — separate models, or at least separate contexts and prompts — rather than being something a single generalist is asked to do well at both ends. The paper demonstrates the damage; it does not explore whether multi-task training, adapters, or role-conditioned prompting would avoid it.

Section 5.1's rule — that better planning pays off more with weaker executors, and nearly stops mattering with the strongest — bears directly on the cheap-planner/strong-executor question, and cuts in a slightly awkward direction. It suggests the value of investing in decomposition machinery *declines* as executors improve. If that holds, the appeal of a distilled planner is strongest in exactly the regime the paper does not focus on (constrained local executors), and weakest with a frontier executor, where GPT-4's numbers barely move across three very different decomposers. A harness designed against today's strongest executor and one designed against a small local one may not want the same amount of planning apparatus.

The static-vs-dynamic result is a useful counterweight to the assumption that on-demand, feedback-conditioned planning is strictly better. Here it was worse *and* 2–4× more expensive. But the scope is narrow, and the paper says so.

**Where it stops.**

- **The tasks are not agentic.** Every dataset is a single-turn question with a knowable answer and no environment, no tools, no state, no failure that must be recovered from. The paper's own limitations section names this. The one property that most distinguishes agent harnesses — that early actions change what later steps face — is precisely what the static design engineers out. Their claim that "the next subquestion is less dependent on the answer to the previous subquestions" is defensible for QA and is the *reason* the split works cleanly; it is also exactly what fails in a harness. The static-beats-dynamic finding therefore should not be carried into a setting with genuine step dependence — it was measured where dependence was chosen to be absent.
- **Depth is fixed at one level and width capped at three.** No recursion, no runtime-determined depth, no budget. The paper contributes nothing on how deep to split or when to stop, beyond the observation that a cap of three beat two and four on DROP.
- **Recombination is trivial here** — the solver reads the whole subquestion list and produces one answer. There is no separate recombination step, no partial-result merging, no conflict between subresults. That third leg of the decomposition question is untouched.
- **No error handling anywhere.** No mechanism detects a bad plan, retries, or replans. The rejection-sampling filter operates at training time on the corpus, never at inference. The route from this paper to a harness runs through their own proposed future work — an RL loop using solver outcome as reward — which is unbuilt.
- **The distilled decomposer is a frozen artefact.** It generalises across the domains tested, but nothing shows it degrades gracefully on a task shape it has never seen, and there is no signal available at runtime to tell you when it has failed.
- **The distillation cost is real and unamortised in the comparison.** Twelve A100-hours plus teacher API calls to build the corpus buys a per-query saving that, on their own table, is a minority of pipeline spend. Whether that pays back depends on query volume — a calculation the paper does not perform.

The honest summary for a harness effort: this paper is strong evidence that *planning and executing are different kinds of thing*, and that treating them as one undifferentiated capability is a modelling error. It is weak evidence about how to build a decomposing harness, and its authors mostly say so.

## Five citations worth chasing next

1. **Zhou et al. (2022), "Least-to-Most Prompting"** — the direct ancestor and the paper's main comparison point for interactive decomposition; the source of the CoT-generalisation critique this work builds on.
2. **Press et al. (2022), "self-ask" / Bamboogle** — supplies both the dynamic baseline that loses the static-vs-dynamic ablation and one of the three datasets; needed to judge whether that ablation was a fair fight.
3. **Shen et al. (2023), HuggingGPT** — named as the precedent for the static plan-then-execute shape, and the closest thing here to an agentic setting with real executors.
4. **Wolfson et al. (2020), QDMR** — the standard human-annotated question-decomposition dataset, and the benchmark against which this paper's "no annotated subquestions, teacher only" stance is defined; the obvious way to score decomposition quality *directly* rather than through downstream success.
5. **Feng et al. (2023)** — circuit-complexity analysis of why CoT works, arguing direct reasoning would need prohibitively large models. The only theoretical grounding cited for why splitting the computation helps at all, and the natural place to look for a principled account of the decomposition/solving asymmetry.

*(Runner-up worth noting: Perez et al. (2020), unsupervised decomposition by mining 10M candidate sub-questions — a third route to decomposition supervision that avoids both annotation and a teacher.)*
