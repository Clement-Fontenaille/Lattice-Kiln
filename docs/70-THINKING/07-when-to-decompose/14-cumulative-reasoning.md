# Cumulative Reasoning with Large Language Models

## Density

**Density: MEDIUM** — the core proposal (a Proposer/Verifier/Reporter split that accumulates verified sub-results into a DAG) sits squarely on the Subject and the paper does report a state-count metric, but the mechanism is described only prosaically (no algorithm box, no DAG data structure, no acceptance rule beyond a True/False prompt), one of the three task families abandons the mechanism entirely, and roughly two thirds of the pages are prompt dumps, worked examples and dataset excerpts.

**Authors.** Yifan Zhang, Jingqin Yang, Yang Yuan, Andrew Chi-Chih Yao (IIIS, Tsinghua University; Shanghai Qi Zhi Institute).

**Year.** arXiv v1 August 2023; read here as v7 (March 2025) and v11 (May 2026, the camera-ready). arXiv:2308.04371.

**Venue.** Transactions on Machine Learning Research (TMLR). Confirmed from the camera-ready PDF's own running header, "Published in Transactions on Machine Learning Research", and from the arXiv comment field. *Caveat on the confirmation route:* the OpenReview forum page (`openreview.net/forum?id=XAAYyRxTlQ`) and its API both returned HTTP 403 with a `ChallengeRequiredError` browser-verification challenge during this reading, so the review thread, decision note and any certification could not be inspected. The venue claim rests on the paper's own header, not on the OpenReview record.

**Keywords (mine, not the paper's).** Role-split prompting; propose–verify loop; verified proposition store; DAG of intermediate results; LLM-as-verifier; step-level rejection; search-state accounting; symbolic verifier substitution; self-curated benchmark.

---

## Approach

Cumulative Reasoning (CR) is a prompting/orchestration framework, not a training method. One task is handled by three *roles*, each a call to the same underlying LLM with a different role-specific few-shot prompt (the paper is explicit that this is a deployment convenience — "the roles ... are instantiated using the same underlying LLM but distinguished by role-specific few-shot prompts"; the Verifier is the one role that may instead be an external tool):

1. **Proposer** — given the current context, emits *one* candidate next reasoning step. It does not plan; it does not emit a set of sub-tasks up front. Each call produces a single new candidate proposition.
2. **Verifier(s)** — judges that single candidate and returns a binary accept/reject. Only accepted steps enter the store. The paper says the Verifier is "ideally" a symbolic system (theorem prover, Python interpreter) but in most experiments is another prompted LLM instance.
3. **Reporter** — watches the accumulated store, decides when there is enough to conclude, and emits the final answer conditioned on the store.

The accumulated store is the object the paper cares about: a **directed acyclic graph** whose nodes are the original premises plus every *validated* proposition, and whose edges record which nodes a proposition was derived from. New propositions may be conditioned on any combination of existing validated nodes, which is the property the paper uses to distinguish CR from CoT (linear chain) and ToT (tree with pruned branches). Rejected candidates are discarded and, the paper claims, not re-entered — "the verifier has wiped out the possibilities of these nodes and their successors".

The framing is dual-process (Kahneman System 1 / System 2) plus an appeal to intuitionistic logic and mathematical constructivism: a solution is *built* from validated steps rather than asserted.

Implementation is via the Microsoft Guidance library. Decoding temperature 0.1 by default, 0.7 for majority voting.

### How the three task families actually instantiate this

The three benchmark families differ enough that they should be read as three different systems sharing a name.

**(a) Logical inference (FOLIO, AutoTNLI, and third-party runs on LogiQA / ProofWriter / LD).** From Appendix F, the actual prompts:

- *Proposer* is told to use First-Order Logic to "deduce a 'Proposition' from **two** given 'Premises'", to make it logically correct, to make it **not a duplicate** of the premises, to derive only from the given premises and propositions rather than "unsourced common knowledge", and to make it **useful for determining whether the Hypothesis is True, False, or Unknown**. So the split is not free-form: each sub-result is a two-parent deduction, which is what makes the accumulated object a DAG in the first place.
- *Verifier* gets premises plus the candidate proposition and is asked "determine whether the deduction of two given 'Premises' to a 'Proposition' is valid or not, and reply with True or False". The template's assistant turn is `"Judgement": "Is this deduction valid? {[True or False]}"` — i.e. a bare label, with no reasoning slot before it in this template.
- *Reporter* gets premises plus the accumulated propositions and outputs True/False/Unknown.
- The number of propositions is a **fixed budget** `n`, set per dataset (n=2 for FOLIO, n=4 for AutoTNLI), not something the Reporter discovers at runtime. There is also a "premises random choice" mechanism — the Proposer is fed a random subset of premises — which the ablation treats as a separate component.

**(b) Game of 24.** Here CR is a search procedure. A set `S` of reachable states is maintained; a state `u ∈ S` is selected; the Proposer picks two numbers from `u` and applies one arithmetic operation to make a new state `v`; the Verifier confirms the operation is valid; `v` is added to `S`. Two verifier prompts exist: **Verifier (a)** checks that the intermediate arithmetic step is correct and uses only two existing numbers, and **Verifier (b)** is a *reachability heuristic* asking whether the remaining numbers can reach 24 (`sure` / `likely` / `impossible`) — that second one is not a soundness check at all, it is a search prior of the kind ToT uses. Breadth `b` (1–5) parallel branches; hard iteration cap `L = 50`. The Reporter's job is explicitly **recombination**: it traces back the derivation through the accepted states and composes them into a single complete expression (its prompt shows it stitching `1*4 = 4` and `1*4*6 = 24` into `1*(1*4)*6 = 24`).

**(c) MATH.** This arm does not run a propose/verify/report loop in the sense above. From the worked example and the meta-prompt (Fig. 16), the model produces *preliminary contents*, then *hints*, then a series of self-raised **sub-questions with answer sketches**, answers them, and finally composes a solution — a single-pass structured template, decomposition without an adversarial verifier. In the code-environment variant, the Python interpreter is the verifier: each sub-question's answer sketch is checked by executing code. Prompting is 4-shot without code, 2-shot with code, optionally combined with Progressive-Hint Prompting.

### Comparison claims and the theory

§3.1 argues CR differs from CoT (error propagation along a linear chain, no verification), ToT (explores a tree, prunes branches, does not accumulate verified knowledge from *diverse* branches into one reusable structure), and GoT (also graph-shaped, but CR is a specific role-based, verify-at-each-step instantiation whose acyclicity "prevents logical loops"). The camera-ready adds Forest-of-Thought and a Self-Critique/Iterative-Refinement paragraph positioning CR against Reflexion and Self-Refine: those refine a single trace, CR builds a persistent store that informs all later steps.

The theory (Def. 3.1, Assumption 3.2, Lemma 3.3, Theorem 3.4) defines an *arrival probability* — the probability of reaching the correct conclusion — for a two-stage problem with exactly one correct path and a **near-perfect verifier assumed by fiat**, and concludes `P_CoT-SC ≤ P_ToT ≤ P_CR`. Assumption 3.2 is the load-bearing step and it directly assumes what is to be shown: `p_ToT ≤ p_CR|(·)` step-wise, plus monotonicity of the conditional step-probability in the number of accumulated validated nodes. The paper is candid that these "are simplifications for this theoretical illustration and may not hold in all practical scenarios". A small conceptual experiment on three Game-of-24 puzzles (1000 repetitions each) shows `p1·p2` beating direct `p` — e.g. 5.0% vs 3.0%, 5.2% vs 0.0%, 4.4% vs 1.8% — as an empirical gesture at the same claim.

---

## Models targeted

GPT-4 and GPT-3.5-turbo (via OpenAI chat-format APIs), LLaMA-13B and LLaMA-65B. All four appear on the logical-inference tasks; Game of 24 and MATH are GPT-4 only. These are 2023-era models throughout — no model was refreshed across eleven arXiv versions spanning August 2023 to May 2026, so every number in the paper is measured on a model generation that predates the camera-ready by roughly two and a half years.

## Benchmarks / datasets

- **FOLIO-wiki** (Han et al. 2022) — first-order-logic natural-language inference, labels True/False/Unknown. The authors restrict to the Wikipedia-derived 52.5% of the 1435-example set and, after removing few-shot examples and examples lacking source labels, test on **534** examples.
- **FOLIO-wiki-curated** — the authors' own cleaning of the above: **74 instances removed** for missing/contradictory common knowledge, ambiguity, inconsistent premises, vague statements or typos, and *incorrect answer annotations*, leaving **460** examples. The headline 98.04% is on this self-curated set.
- **AutoTNLI** (Kumar et al. 2022, extending INFOTABS) — tabular NLI, Entail/Neutral. 1,478,662 pairs exist; the **first 1,000** are used.
- **Game of 24** — the **100**-puzzle set curated by ToT (Yao et al. 2023).
- **MATH** (Hendrycks et al. 2021) — the **500**-example subset of Lightman et al. (2023), all five difficulty levels, reported by subtopic and by level.
- **LogiQA, ProofWriter, FOLIO-val, LD** — appear only in Appendix B, and the numbers are explicitly **third-party reproductions by Sun et al. (2023)**, not the authors' own runs.

Baselines: Direct prompting, CoT, CoT-Self-Consistency (k=16, or k=100 on Game of 24), best-of-100, ToT, Complex CoT (with and without PHP), PAL, ToRA, and a PoT comparison in the abstract.

## Author incentive

An academic method paper from Tsinghua's Institute for Interdisciplinary Information Sciences and the Shanghai Qi Zhi Institute, with Andrew Chi-Chih Yao (Turing Award, IIIS founder) as senior author. No funding statement or acknowledgements section appears in the camera-ready. The stake is the usual one for a named-method paper: CR is offered as a framework with a public repo (`github.com/iiis-ai/cumulative-reasoning`) and a name to be cited, positioned explicitly *against* ToT — a paper whose first author shares the Yao surname but is a different researcher (Shunyu Yao, Princeton). No product or commercial deployment is claimed; no external API credits or industrial affiliation are declared. The most direct incentive artefact in the paper is not financial but methodological: the authors both **curate the benchmark they report their headline number on** and **define the efficiency metric** (visited states) on which they claim a cost win.

## Measurement methodology (brushed)

**Dependent variable.** Accuracy (%) in every table. Two secondary variables carry the cost story: **"# Visited States"** (Game of 24 and the Appendix B logical-inference tables) and **"Iters" — "the average number of LLM interactions"** (MATH only).

**What is controlled.** The underlying model is held fixed within each comparison block, and CR is compared against baselines run on the same model — this is done consistently and is the paper's methodological strength. Decoding temperature is stated (0.1 default, 0.7 for majority voting, 0.0 greedy for the MATH tables). Shot counts are stated per method, but **not equalised**: CR runs 4-shot without code and 2-shot with code against Complex CoT at 8-shot and PAL/ToRA reproductions at 4-shot. The authors present the lower shot count as favourable to CR; it also means prompt budget is not held constant.

**N.** 534 / 460 / 1,000 / 100 / 500 as above. The Game of 24 result — the most-quoted number, "98%, a 24% improvement" — rests on **100 puzzles**, so it is 98 vs 74 successes; a single puzzle is a full percentage point.

**Significance.** None. There are no error bars, no confidence intervals, no significance tests, no seeds, and no repeated runs anywhere in the main results. The one place repetition appears is the three-puzzle conceptual experiment in the theory section (1000 repeats), which is not a headline result. Differences of 0.0–1.3 points are reported with a signed delta in the same typography as differences of 24 points — including the FOLIO-val row where CR (69.11) is *below* ToT (69.12) and this is not remarked upon.

**Ablation.** One table (FOLIO-wiki, GPT-3.5-turbo), no repeats: CR n=2 at 73.03; **CR without the Verifier at 64.23**; CR without premises-random-choice at 68.73; CR without both at 67.23. Only single runs.

**Cost accounting.** This is thin and deserves its own note. "# Visited States" counts states entered by the search, not LLM calls — so a Proposer call and its Verifier call collapse into one counted state, and rejected proposals appear to cost nothing in the metric. There are **no token counts, no dollar costs, no wall-clock times, and no per-role call breakdowns anywhere in the paper.** The camera-ready adds Appendix B.2, "Computational Considerations", which is entirely qualitative: it concedes that "if all roles are LLM-based, CR can involve more LLM calls per problem than a single CoT pass", that "each reasoning cycle might involve a Proposer call and a Verifier call", and that conditioning on a growing DAG "can also increase the token count for LLM calls" — then argues the trade is worth it, citing the visited-state numbers as evidence of efficiency, and notes that a Python-interpreter verifier is "much faster and cheaper than LLM calls". It also observes that using one underlying model for all roles avoids loading multiple large models. The section ends by positioning CR as suited to "test-time scaling where achieving the best possible answer justifies the additional computational steps" — an admission that the method is bought, not free.

---

## Key findings

**1. CR beats Direct / CoT / CoT-SC on logical inference, across four models.** FOLIO-wiki (n=2): LLaMA-13B 44.75 → 53.37; LLaMA-65B 67.42 → 72.10; GPT-3.5-turbo 62.92 → 73.03; GPT-4 80.52 → 87.45. The gains over the *strongest* baseline (CoT-SC k=16) are smaller than the gains over Direct: +0.94, +1.31, +9.70, +2.43 points respectively. On FOLIO-wiki-curated, GPT-4 reaches **98.04%** against CoT-SC's 96.09 — a 1.95-point gap that the paper describes as "nearly doubling the effectiveness", which is true only of the *error rate* (3.91% → 1.96%). AutoTNLI: LLaMA-65B 61.7 (CoT-SC) → 72.5, the paper's largest same-model margin.

**2. Game of 24: higher accuracy at a quarter of the search.** CR (b=5) 98% at 14.86 visited states; ToT (b=5) 74% at 61.72. Even CR at b=1 gets 84% at 11.68 states. This is the paper's cleanest joint accuracy-and-cost claim, and the only place the two move in the same favourable direction by a large margin.

**3. MATH: modest gains without code, large gains with a code verifier.** Without code, CR (4-shot) 54.20 overall vs Complex CoT (8-shot repro) 48.80; with PHP, 58.00 vs 53.80 — the "+4.2%" of the abstract. Level 5 goes 22.4 → 32.1 (the "43% relative improvement"). With a Python code environment, CR (2-shot) hits **72.2%** overall vs PAL 52.0 and ToRA 60.8 in the authors' reproductions, and 52.2 vs 46.3 at Level 5. Note that the largest headline number in the abstract (the 38.8% relative gain over PoT/PAL) comes from the arm where a **real symbolic verifier** replaces the LLM verifier — and where the propose/verify DAG loop is least in evidence.

**4. The Verifier is the component that carries the method — measured once.** The single ablation: removing the Verifier costs **8.80 points** (73.03 → 64.23), taking CR to roughly CoT level (64.61). Removing the premises-random-choice mechanism costs 4.30 points (73.03 → 68.73). *An oddity the paper does not discuss:* removing **both** scores 67.23, i.e. **3.0 points higher than removing the Verifier alone** (64.23). The two components interact non-monotonically, which undercuts reading the 8.80 as "the value of verification" in any additive sense; the numbers are single runs on 534 examples, so this may equally be noise the paper has no machinery to detect.

**5. The efficiency claim outside Game of 24 is marginal, and one accuracy claim is a tie.** In the third-party-reproduced Appendix B tables: LogiQA CR 45.25% / 17 states vs ToT 43.02% / 19.87; ProofWriter 71.67% / 16.76 vs 70.33% / 24.57; LD 78.33% / 16.98 vs 76.83% / 21.83; **FOLIO-val 69.11% / 15.87 vs ToT 69.12% / 19.12** — a 0.01-point loss on accuracy at ~17% fewer states. Against CoT-SC at k=16 states, CR uses *slightly more* states on three of these four datasets (17, 16.76, 16.98 vs 16).

**6. Rejected work is claimed to be permanently pruned.** The paper asserts that once the Verifier rejects a node, CR "will not enter the failed nodes multiple times, since the verifier has wiped out the possibilities of these nodes and their successors". This is stated as a property, not demonstrated; nothing in the prompts shown implements a rejected-set that is fed back to the Proposer, apart from the Game-of-24 Proposer instruction to "AVOID duplicating with forbidden steps".

### The authors' own reading

The authors read all of this as validating a single thesis: that **separating generation from verification, and accumulating what survives verification into a reusable structure, is what makes multi-step reasoning work.** In their framing —

- The failure they are addressing is that CoT-style LLMs conflate generation and verification in one monolithic output ("This division of labor aims to overcome limitations of monolithic LLM outputs, where generation and verification are conflated"), and that CoT/ToT "lack mechanisms for dynamically storing and leveraging intermediate results".
- The DAG, not the role split, is the claimed differentiator against ToT: new propositions can condition on *any combination* of validated nodes rather than a single ancestral path, giving "a richer foundation for subsequent reasoning steps". They explicitly frame the growing context as a trade-off ("conditioning on an increasing number of validated nodes ... can increase contextual complexity") that CR "manages through its iterative process" — an assertion, not a measurement.
- Acyclicity is claimed to do specific work: it "prevents logical loops and ensures consistent forward progression in the deductive process, thereby avoiding reasoning dead ends".
- They read the Game-of-24 state counts as showing that verification *buys back* its own cost: "while individual steps in CR might be more involved due to verification, the overall search can be more efficient by avoiding unproductive paths."
- They read the theory as an explanation rather than a proof, calling it an "illustrative theoretical comparison", and summarise the whole paper's insight as: "the structured accumulation and reuse of verified knowledge within a flexible DAG enhances complex reasoning."
- On the human-analogy side they lean on Kahneman's System 1/System 2 and on constructivism, arguing CR gives an LLM a System-2-like deliberate process. In Appendix C they add a further reading of their own results: CR handles higher-order-logic inference (attitude verbs, generalised quantifiers, modal operators) that formal FOL solvers cannot express and that even experts find hard to formalise — "CR solves these problems pretty well without resorting to and being restricted to symbolic systems, just like the way humans think." That is a notable position given that their own strongest arm uses a symbolic verifier.

---

## Open questions the paper itself raises

There is **no Limitations section**. The paper's self-stated open questions are scattered and few, and I list them in its own framing:

1. **Verifier richness.** In Related Work: "While CR's current Verifier often makes binary (valid/invalid) decisions or relies on external tools like code interpreters, **future work could integrate such richer feedback mechanisms into the Verifier role**" — pointing at PANEL's stepwise natural-language self-critique and General-Reasoner's generative model-based verifier. The paper thus flags its own accept/reject signal as impoverished.
2. **Context growth from the DAG.** Appendix B.2: conditioning on all prior validated steps "can also increase the token count for LLM calls. **Future work could explore optimizing these dependencies, for instance, by selecting only the most relevant prior steps to manage context size** without sacrificing much of the benefit of cumulative knowledge." This is the paper naming the recombination-cost problem and leaving it open.
3. **The theory's assumptions.** Stated in-line: the near-perfect-verifier and unique-correct-path assumptions "are simplifications for this theoretical illustration and may not hold in all practical scenarios", and the monotonicity assumption is qualified by the acknowledgement that "LLM behavior can be unpredictable and refinements are not always monotonically beneficial due to issues like hallucination".
4. **Prompt-design dependence.** Appendix F opens with "The design of few-shot prompts is critical to guiding the behavior of each LLM role within CR", then notes that zero-shot meta-prompts also work and "minimize the bias introduced in the few-shot examples" — an acknowledgement that the reported behaviour is prompt-sensitive and that the few-shot exemplars introduce bias.
5. **Benchmark quality.** §4.2's whole premise is that FOLIO-wiki contains wrong labels, contradictory premises and unanswerable items — the paper raises the reliability of its own evaluation substrate as a problem, and answers it by curating rather than by proposing a general fix.
6. **Verifier substrate.** Appendix C argues both that FOL solvers are too weak (expressiveness limits, translation misalignment, undecidability) and that HOL programs are too hard for LLMs to write — leaving open what a *sound* verifier for natural-language reasoning should actually be, which is precisely the gap CR's LLM-verifier occupies.

Not raised anywhere by the paper: the verifier's own error rate, the sensitivity of results to `n`, `b` and `L`, run-to-run variance, or dollar/token cost.

---

## Appreciation

### What transfers as MECHANISM

**The generation/verification split as an architectural commitment.** The paper's durable contribution is not the DAG; it is the demonstration that giving *rejection authority* to a separate call — one that sees the candidate step and nothing of the generator's momentum — changes outcomes materially. The single ablation puts the whole method's advantage on that component. This is an argument about role separation that does not depend on FOLIO, GPT-4, or 2023.

**A sub-result is a two-parent deduction, not a free-form sub-task.** This is under-advertised and is the most portable design detail in the paper. Because the Proposer is constrained to derive one proposition from *two* named premises, every sub-result arrives with its dependency edges already declared, non-duplication is checkable, and the accumulated object is a DAG *by construction* rather than by post-hoc bookkeeping. A decomposition scheme that makes provenance a required output field gets its graph for free. The corresponding cost is equally portable: the split is only as expressive as the step schema, and a task whose natural sub-steps do not fit "two parents, one conclusion" gets nothing from this.

**Verification is fungible with a tool, and that is where it gets reliable.** The same architecture accepts an LLM verifier or a Python interpreter in the same socket. The paper's own strongest results are the socket filled with the interpreter. The transferable claim is the *substitutability*, plus the observation from B.2 that a symbolic verifier is both cheaper and more reliable than an LLM one — i.e. the accept/reject port is the right place to spend engineering effort in a decomposition system.

**Accumulate-and-condition rather than prune-and-forget.** The distinction CR draws against ToT — that verified intermediate results from *abandoned* branches remain available as context for later steps — is a real design axis, independent of the numbers. So is its stated cost: the Proposer's context grows monotonically with accepted work, which the paper flags and does not solve.

**Recombination is a separate, named role with real work to do.** The Reporter is the only mechanism here for turning a set of accepted sub-results into an answer, and the Game-of-24 prompt shows that work concretely (walking the derivation backwards and assembling one expression). Naming recombination as a distinct role with its own prompt and its own termination decision is a transferable structure.

**A rejected step is cheap; a wrong accepted step is expensive.** The theory, stripped of its circular assumption, is really the observation that verification converts an accuracy problem into a search problem — `p1·p2` with retries beats a single shot at `p` when each stage can be independently checked. The three-puzzle conceptual experiment is the honest version of this argument and it is a mechanism claim, not a magnitude one.

### What is MAGNITUDE, valid only inside this setup

- **98.04% on FOLIO-wiki-curated.** The set was cleaned by the authors, of 74 items they judged flawed, with no inter-annotator agreement, no second curator, and no re-check of the retained items. Any comparison against a number produced on the uncurated set is not like-for-like. Treat this as an in-paper number only.
- **"98% on Game of 24, +24% over ToT."** 100 puzzles, single run, no seeds; and CR is compared against ToT's *published* configuration on ToT's own curated puzzle set. The state-count ratio (14.86 vs 61.72) is measured in a unit the authors define, which does not count verifier calls or rejected proposals. The direction of this result is credible; the ratio is not portable.
- **"+9.3% on logical inference", "+4.2% on MATH", "38.8% over PoT".** All are best-cell selections across a table of model × method cells, with no variance estimate, and several are against the authors' own reproductions of the baselines rather than the baselines' published numbers (their PAL repro scores 52.0 vs PAL's published 51.8; their ToRA repro 60.8 vs published 61.6 — close, but the comparison-to-repro pattern means the baseline is under their control).
- **The 8.80-point verifier ablation.** One run, one dataset, one model, and internally inconsistent with the two-component removal. The *sign* transfers; the size does not.
- **All model-relative claims.** GPT-3.5/GPT-4/LLaMA-65B. A method whose value is "the base model cannot check its own work in one pass" is exactly the kind of claim whose magnitude shrinks as base models improve, and the paper's headline numbers were never re-measured across eleven versions and nearly three years.
- **"Fewer visited states than ToT" outside Game of 24.** Margins of 2–8 states on third-party reproductions, alongside a 0.01-point accuracy *loss* on FOLIO-val. Not a cost result anyone should carry forward.

### Where the paper is weakest on its own terms

The verifier's reliability is never measured. This is the load-bearing omission: the theory *assumes* a near-perfect verifier, the ablation shows the verifier is where the gains live, and the deployed verifier on most tasks is the same model that produced the proposition, prompted to answer True or False with no reasoning slot in its template. There is no precision/recall on verifier judgements, no count of accepted-but-wrong propositions, no analysis of what a false accept does to everything derived from it downstream, and no test of whether a same-model verifier is doing anything more than a stylistic consistency check. The Game-of-24 Verifier (b) is not even a soundness check — it is a ToT-style reachability heuristic, which means part of what is credited to "verification" is search guidance.

Second: the three task families are not one method. The MATH arm — the source of the largest headline number — is a structured single-pass template with hints and self-raised sub-questions, not a Proposer/Verifier/Reporter loop building a DAG. The paper's title mechanism is genuinely exercised only on the logic tasks and Game of 24.

Third: depth and budget are set by hand (`n=2`, `n=4`, `b=1..5`, `L=50`), which sits awkwardly with the claim that "the language model (LLM) itself influences the depth of the search". On the logic tasks the number of sub-results is a constant chosen per dataset, and the Reporter's "decide when to stop" role is, in those runs, largely decorative.

---

## How it could serve a harness-design effort — and what to worry about

*Stemming the discussion rather than settling it.*

**A harness could take the accept/reject port as a first-class object.** The paper's structure suggests a design where sub-results are not returned to the caller directly but submitted to a gate, and where the gate's implementation (peer model, tool, interpreter, schema check) is a configuration choice rather than a property of the agent that generated the work. Open: what is the gate's contract? CR's gate returns one bit. The paper itself flags that one bit is impoverished. A harness has to decide whether rejection carries a reason back to the proposer, whether rejection is final or a revision request, and who pays for the retry.

**Provenance as a required output field, not a reconstruction.** CR gets its DAG because the proposer must name its parents. A harness that requires every sub-result to declare what it was derived from gets an auditable dependency graph as a byproduct, and gets invalidation for free — if a node is later found wrong, its descendants are identifiable. Open: CR only ever *adds* to the graph; it never revisits an accepted node. What happens when a node accepted at step 3 is discovered to be wrong at step 9 is not addressed anywhere in this paper, and is the obvious next question for anything that accumulates.

**Context as the real cost of accumulation.** The paper names this and leaves it: conditioning every proposal on the whole store of accepted work means context grows with progress, and the paper's proposed fix ("selecting only the most relevant prior steps") is precisely a retrieval problem re-introduced inside the decomposition. Open: at what store size does selection become mandatory, and does selecting turn the DAG back into something tree-shaped in practice?

**Recombination deserves its own role and its own budget.** The Reporter is doing three separable jobs — termination decision, synthesis, and (in Game of 24) derivation trace-back. Merging them into one prompt is convenient; a harness may want them separate, because the "have we got enough?" judgement and the "write the answer" judgement fail differently.

**Concerns to carry forward.**

- *The verifier-quality question is the whole question.* CR's argument reduces to "a second call that only judges is better than the same call that also generates". Whether that holds is a property of the model and the task, not of the architecture, and this paper does not measure it. A harness that adopts the pattern inherits an unmeasured dependency: if the verifier's false-accept rate is non-trivial, verification converts a visible failure into a *laundered* one — a wrong step now carries an accept stamp and gets reused by everything downstream. CR's own DAG amplifies exactly this, because acceptance makes a node reusable everywhere.
- *Same-model verification may be self-agreement.* Every logic-task result here uses one model in both seats. The paper's framing of this as "independent perspectives" is asserted through prompt separation alone.
- *Fixed budgets undercut adaptive claims.* If a harness wants runtime-determined depth, this paper does not demonstrate it; it demonstrates hand-set `n` with a Reporter that mostly reads out.
- *The cost picture is unmeasured.* No tokens, no calls, no money. Anyone costing a propose-verify loop must assume at least 2× the calls per step before recombination, and growing prompts on top. The paper's own honest position is that this is test-time-scaling spend justified when the best answer matters.
- *Generality is unproven.* Everything here is a task with a checkable step: FOL deduction, arithmetic, closed-form maths. The gate is easy to build when correctness is local and decidable. Whether the same architecture survives contact with tasks where a step's validity is a judgement call is untested, and Appendix C is the paper half-admitting it does not know what a sound verifier for natural language would be.
- *Evaluation hygiene.* Self-curated headline benchmark, self-defined efficiency metric, single runs, no variance. Adopt the mechanism; do not carry the numbers.

---

## Five citations worth chasing next

1. **Yao et al. (2023), "Tree of Thoughts: Deliberate Problem Solving with Large Language Models."** The direct foil for this entire paper — fixed-width/depth search with pruning, and the source of the Game-of-24 puzzle set and baseline numbers CR is measured against. Needed to judge whether CR's accumulate-don't-prune distinction is as sharp as claimed.
2. **Zhou et al. (2022), "Least-to-Most Prompting."** Cited here as a decomposition antecedent; the upfront-plan end of the axis (decompose first, then solve in order) against CR's on-demand, one-step-at-a-time proposal. The cleanest contrast for the "what sets the depth" question.
3. **Khot et al. (2022), "Decomposed Prompting."** The modular end — sub-tasks dispatched to specialised handlers, including recursive decomposition. Bears directly on whether roles should be prompt variants of one model (CR's choice) or genuinely different components.
4. **Besta et al. (2024), "Graph of Thoughts" (AAAI).** The other graph-structured reasoning framework, and the one CR must distinguish itself from on structural grounds. Worth reading to see whether "DAG built by propose-verify roles" is a real difference from "graph with aggregation/refinement operators" or a naming difference.
5. **Sun et al. (2023)** — the third-party reproduction the authors rely on for the LogiQA / ProofWriter / FOLIO-val / LD comparisons in Appendix B. The only independent measurement of CR against ToT in the paper, and the source of the one row where CR does not win; worth reading for its own account of how these methods compare under a neutral implementation.

*Runners-up, if the verifier thread is the one being pulled:* Madaan et al. (2023) Self-Refine and Shinn et al. (2023) Reflexion (single-trace refinement, cited as support for CR's monotonicity assumption); Hosseini et al. (2024) V* (a trained verifier); Lightman et al. (2023) (process- vs outcome-supervision, and the source of the 500-example MATH subset).
