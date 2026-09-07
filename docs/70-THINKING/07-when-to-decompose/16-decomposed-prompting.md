# Decomposed Prompting: A Modular Approach for Solving Complex Tasks

## Density

**Density: HIGH** — The paper is short, almost entirely method-plus-evidence with very little padding, and its whole subject *is* task decomposition: it names the decomposer/sub-task-handler split, two distinct recursion modes, handler swappability, and the recombination mechanism, and gives call-count analysis for its recursion schemes.

**Keywords (mine):** decomposer prompt; sub-task handler; prompting program; imperative controller; hierarchical decomposition; recursive decomposition; input-length recursion; handler substitution; symbolic tool call; length generalisation; modularity as debuggability; call-count complexity.

**Authors.** Tushar Khot, Harsh Trivedi, Matthew Finlayson, Yao Fu, Kyle Richardson, Peter Clark, Ashish Sabharwal.

**Year.** arXiv v1 Oct 2022; v2 (the version read here) 11 Apr 2023.

**Venue.** ICLR 2023. Peer-reviewed. arXiv:2210.02406, licensed CC BY 4.0. Code, data and prompts released at github.com/allenai/DecomP.

## Approach

The paper's starting complaint is that chain-of-thought (CoT) prompting conflates two
things into one demonstration: *how to decompose* the complex task, and *how to perform
each step*. When a step is individually hard — the paper's running example is extracting
the k-th letter of a word, which GPT-3 `text-davinci-002` does badly — a handful of
demonstrations of the *whole* task cannot also teach the step, because the prompt budget
is spent on the composition. Some steps (document retrieval over a large corpus) arguably
cannot be taught by prompt at all.

**The architecture.** DecomP splits the system in two, and both halves are few-shot
prompted LLMs:

- A **decomposer**, whose prompt describes only the *procedure*: for a complex question
  it emits a sequence of (sub-task-name, sub-question) pairs, and nothing about how any
  sub-question is answered. Formally the decomposer generates a *prompting program*
  `P = ((f₁,Q₁,A₁), …, (f_k,Q_k,A_k))`, where each `f_i` is drawn from an auxiliary set
  `F` of sub-task functions and `A_k` is the final answer. Its in-context examples are
  full example programs, `E_j = (Q_j, (f_{j,1},Q_{j,1},A_{j,1}), …)`.
- A library of **sub-task handlers**, one per `f ∈ F`, each with its own independent
  prompt (or non-prompt implementation), each seeing examples of *its own* simple task
  rather than of the complex task.

The authors' own framing is a software-engineering analogy, and it is load-bearing
throughout: the decomposer is "the top-level program … using interfaces to simpler,
sub-task functions"; the handlers are "modular, debuggable, and upgradable
implementations of these simpler functions, akin to a software library." Handlers are
shared across tasks (their `split` handler is reused by two different callers), and a
handler that underperforms is debugged in isolation and plugged back in without touching
the rest of the system.

**How control passes.** Neither half calls the other directly. A third component, a
**high-level imperative controller** (the paper also calls it a symbolic controller),
owns the loop and is *not* an LLM. Per Fig. 3 the cycle is:

1. The controller feeds the complex question (plus the decomposition history so far) to
   the decomposer prompt and reads back exactly *one* next step — a sub-task tag in
   square brackets plus a sub-question, e.g. `QS: [split] What are the words in "…"?`.
2. The controller routes that sub-question to the named handler, applying any special
   operator first.
3. The handler's answer is appended to the decomposer's context as `A: …` and becomes
   addressable as `#1`, `#2`, … for later steps.
4. Loop until the decomposer emits the sentinel `[EOQ]`; the last answer is returned as
   the final prediction.

So the decomposer is re-invoked at every step and generates the next sub-question
*conditioned on all previous answers* — it is iterative and top-down, not a one-shot
plan. Inference is formally MAP over the LLM's predictive distribution, approximated by
greedy decoding in all experiments.

**Operators and recombination.** Recombination is handled by symbolic operators borrowed
from Khot et al. (2022), applied by the controller, not by the model:

- `select` (the implicit default) simply substitutes a referenced answer index, `#i`, with
  its stored value.
- `project_values` (written `foreach` in the main text) takes a list answer `#i = X`,
  builds one sub-question per element by string substitution, calls the handler once per
  element, and concatenates the answers into a list: `A = [model(q) for q in Q]`.
- `project_values_flat_unique` (`foreach_merge`) does the same, then flattens and
  de-duplicates.

Anything beyond that — actual content-level merging, e.g. joining reversed halves or
concatenating letters — is itself a *sub-task* given to a handler (`merge`, `join`), not
a privileged framework step. This is worth stating plainly: **DecomP has no separate
recombination stage.** Fan-out/fan-in is a symbolic list operation in the controller;
semantic recombination is just another prompted call in the program.

**Two recursion modes.** The paper is explicit that these are different capabilities.

*(a) Hierarchical decomposition — recursing on a hard sub-task.* When a handler's task is
itself beyond the model, that handler is replaced by another decomposed prompt with its
own sub-handlers. `str_position` (find the k-th letter) is re-implemented as: call the
shared `split` handler to get `[(M,1),(a,2),…]`, then call `arr_position` to index that
array. Depth is set by the author at authoring time, driven by observed failure of a
handler — not by a budget and not discovered at runtime.

*(b) Recursive decomposition — recursing on input length.* The decomposer prompt calls
*itself* on the same task with smaller inputs. For list reversal (Algorithm 1,
`SplitReverse`): if `|x| < 4` return the reversal directly via the base-case CoT handler;
otherwise split into halves, recurse on each, and concatenate the reversed halves in
swapped order. The base case is chosen as the length at which the underlying prompt is
already accurate. The authors state the general principle — "some problems can be
naturally broken down into one or more smaller problems of the same form" — and cite
merge sort. This mode is what buys *scale invariance*: the recursion terminates in inputs
the model demonstrably handles, so the system's accuracy stops depending on input length.
Notably the split decision is expressed inside the prompt as explicit arithmetic ("The
sequence is 5 items long, which is more than the minimum length of 4, so we split it.
Half of 5 is 5/2 = 2.5…"), so the *runtime depth* is data-dependent even though the
*scheme* is fixed.

**Handler swappability.** The paper exercises four distinct handler implementations
behind the same interface: (i) a plain few-shot prompt (`split`, `merge`, `qa`); (ii) a
further-decomposed prompting program (`str_position`); (iii) a symbolic function — an
Elasticsearch BM25 index for `retrieve_odqa`, plus regex/list utilities like
`remove_numbers` and answer-extraction patterns; (iv) a *different model* — the
open-domain QA experiments run the decomposer on a GPT-3-class model while the reading-
comprehension handlers run on Flan-T5-Large/XL/XXL, because "only these models are
reliably able to produce the required structured outputs." The claimed availability of
finetuned or supervised models as handlers is asserted in the framing rather than
demonstrated. Handler outputs can be *multi-valued*: `retrieve_odqa` returns both an
answer and the retrieved paragraphs, so a later sub-question can consume the answer while
the final `multihop_rcqa` handler consumes the accumulated documents.

## Models targeted

All closed-API GPT-3-family models plus one open family, all used frozen and few-shot;
nothing is trained.

- `text-davinci-002` (InstructGPT3) — the default for everything unless stated.
- `text-davinci-001` — used deliberately in the list-reversal study *because* it is
  weaker; the point is that recursion lets a weaker model approach `davinci-002`'s
  performance on a task `davinci-002` already solves.
- `text-curie-001` — scale ablation on CommaQA (App. C).
- `code-davinci-002` (Codex) — for open-domain multi-hop QA, chosen for its longer
  context window.
- Flan-T5-Large (0.7B), -XL (3B), -XXL (11B) — as *handlers only* in open-domain QA, with
  a GPT-3-class decomposer above them.

Context limits are a visible constraint on the design: the 2049-token window forces a
shrunken CommaQA variant so that four CoT examples will fit, and forces separately
shortened prompts for curie-001/davinci-001 (App. G.4).

## Benchmarks and datasets

Eight datasets across four case studies plus two extras.

1. **k-th letter concatenation** (constructed). Prompts contain positions 1, 4 and last
   over 3-word strings; test sets probe three generalisation axes — unseen position k=3,
   longer inputs (4 and 5 words), and a new delimiter (";"). Words drawn from
   forebears.io popular forename/surname lists. 100 examples per evaluation set.
2. **List reversal** (constructed, vocabulary from Wei et al. 2022). Prompts show 3–5
   item reversals; evaluated on 4, 6, 8, 10 items.
3. **CommaQA-E** (Khot et al. 2022), reading-comprehension setting — synthetic entities,
   facts and multi-hop questions with many distractors and long contexts. Both the
   standard test split and a **compositional generalisation** split (unseen compositions
   of seen relations).
4. **Open-domain multi-hop QA**: HotpotQA (fullwiki), 2WikiMultihopQA, MuSiQue. The
   latter two are natively reading-comprehension, so the authors build corpora by pooling
   all train/dev/test paragraphs — 430,225 paragraphs for 2Wiki, 139,416 for MuSiQue.
   300 held-out dev questions each.
5. **Math QA** (App. B): GSM8K (300 sampled test items) and MultiArith (200 sampled),
   both subsampled explicitly "due to costs with API usage."

Metrics: Exact Match throughout, with set equality for order-independent list answers;
Answer F1 (bag-of-tokens precision/recall, SQuAD-style) for the open-domain QA tasks.

## Author incentive

Five of seven authors are at the Allen Institute for AI (AI2); Trivedi is at Stony Brook,
Fu at Edinburgh (work done during an AI2 internship). Funding: NSF grant IIS2007290, in
part. This is a non-profit research lab with no product being sold here — code, data and
prompts are released openly under CC BY.

The visible stakes are intellectual rather than commercial, and worth naming because they
shape the framing. DecomP is positioned as the general framework that subsumes a family
of AI2's own prior work — Text Modular Networks (Khot et al. 2021), CommaQA (Khot et al.
2022, which supplies both a benchmark *and* the operator vocabulary), MuSiQue (Trivedi et
al. 2022, also a benchmark here). Two of the four case-study datasets are the authors'
own constructions, and the compositional operators are imported from their own earlier
paper. The related-work section performs a specific manoeuvre: it recasts a broad set of
contemporaneous systems (Selection-Inference, Self-Ask, TALM, PAL, Toolformer) as
"specialized systems with a pre-defined decomposition structure" — i.e. as special cases
of the more general thing being proposed. The sharpest comparison, against least-to-most
prompting, is argued on two structural grounds (one-shot vs. iterative sub-problem
identification; having to learn to pick relevant prior answers vs. getting it "for free"
from the decomposition) and is also the one baseline they re-implement and beat.

## Measurement methodology

Brushed, as the format asks, but the design is worth being precise about because it is
better than the norm in prompting papers on one axis and thinner on another.

**Dependent variable.** Task accuracy — EM (symbolic tasks, CommaQA) or Answer F1 (ODQA)
— as a function of a *generalisation axis*, most often input length. The load-bearing
measurement is not a single headline number but the *slope*: how accuracy degrades as
inputs get longer than anything shown in the prompt.

**What is controlled.** The strongest control in the paper is the "rolled out" baseline.
For both symbolic tasks they write a CoT prompt that verbalises *the exact same reasoning
procedure* as the decomposition, unrolled into one linear chain (`unrolled_decomp`). This
isolates the contribution of *modular structure* from the contribution of *the
decomposition procedure itself* — if the rolled-out CoT matched DecomP, the win would be
attributable to having thought of the right steps, not to separating them. They do the
same for least-to-most (a rolled-out l2m baseline). Base prompts are held constant: the
reversal study uses "the same 3 examples of reversing word sequences with 3-5 items"
across all conditions. CoT baselines are run through the same controller framework, with
a regex answer-extractor as the final module, so the harness is shared.

**N and variance.** They report averages over **three independently written prompts**
(P1, P2, P3) per method, explicitly citing Perez et al. (2021) on true few-shot learning
— a real methodological commitment, since prompt choice is a large uncontrolled variance
source. Per-prompt breakdowns are in App. D and show the ordering holds prompt-by-prompt,
not just in the mean. Evaluation N: 100 per letter-concat set; 300 per ODQA dataset; 300
GSM8K / 200 MultiArith. Decoding is greedy — no self-consistency sampling, so no sampling
variance.

**How significance is treated.** Informally. There are no confidence intervals,
significance tests, or error bars in the figures; the word "significantly" in the ODQA
discussion is used descriptively, not statistically. The one variance statement made is a
footnote that DecomP's std. dev. on letter concatenation is zero (it is at ceiling). The
defence against noise is the three-prompt replication plus App. D/E consistency checks
rather than any inferential statistic. Hyperparameters: K (paragraphs retrieved) is grid-
searched on a held-out 100 questions per dataset, with different ranges for GPT-3 vs
Flan-T5 (context limits) and for NoDecomp vs Decomp (since K is *per retrieval round*,
and DecomP performs several rounds) — a defensible choice that is also a confound worth
noticing, since it means the two arms do not see the same total paragraph budget.

**Error analysis** (App. F) is qualitative but pointed: on letter concatenation "we only
found errors in the sub-task execution" — i.e. the decomposer's programs were correct and
every failure was a handler failure. CoT-with-rollout makes the *same kinds* of errors,
just more often. Same finding on CommaQA: errors are wrong single-hop answers, not wrong
decompositions.

## Key findings

**1. Separating the sub-task prompt beats verbalising the same procedure in one chain.**
On k-th letter concatenation DecomP outperforms CoT, CoT-with-rollout, and least-to-most-
with-rollout — "even when the prompt uses the same reasoning procedure as the rolled out
decomposition." *The authors' reading:* "separate prompts are more effective at teaching
hard sub-tasks than a single CoT prompt." This is the paper's cleanest result, because
the rolled-out control removes the obvious alternative explanation.

**2. Decomposition generalises to longer inputs; flat CoT does not.** DecomP stays near
100% EM on letter concatenation as word count rises from 3 to 5, with reported standard
deviation of zero, while CoT baselines "drop noticeably … widening the performance gap."
Same delimiter-generalisation result with ";" (Fig. 22).

**3. Input-length recursion lets a weaker model reach a stronger model's performance.**
On list reversal with `davinci-001`, the base CoT prompt "does not generalize at all" to
sequences longer than the 3–5 shown; recursive DecomP generalises to 10 items and
approaches `davinci-002`. *The authors' reading:* recursion builds a **scale-invariant**
system, and — importantly — this is a structure "current methods such as CoT and standard
prompting" cannot express at all, since a chain cannot call itself.

**4. The rolled-out version of the recursive prompt fails outright.** This is the finding
I would flag as the most interesting in the paper. The same recursive procedure written
as one long CoT "fails because the unrolled prompt becomes too long and convoluted
without the ability to abstract away sub-modules." So for *recursive* decomposition the
modular structure is not an optimisation — it is a precondition. Contrast finding 1,
where the rolled-out control merely underperforms.

**5. Finer-grained handler assignment helps, mildly.** On CommaQA, DecomP beats CoT under
both coarse decomposition (one `qa` handler for all sub-questions) and fine (three
`qa` handlers by question type), with fine marginally ahead. *The authors' reading:*
granularity is a **dial trading human authoring effort against accuracy**, and it works by
letting each handler carry more examples of its own question class, raising single-hop
accuracy. DecomP also holds up on the compositional-generalisation split where CoT drops
— though the authors honestly attribute their small *gain* there to the split's relations
happening to be easier for their QA handlers, not to the method.

**6. A symbolic handler inside the decomposition beats retrieval outside it.** On all
three open-domain multi-hop datasets, Decomp-Ctxt beats both No-Ctxt (closed-book) and
NoDecomp-Ctxt (retrieve once with the full multi-hop question), the one exception being
Codex on HotpotQA where it is comparable. Per-dataset appendix results qualify this:
gains over NoDecomp-Ctxt are substantial on 2Wiki and MuSiQue, but on HotpotQA "the gains
from using DecomP are mostly seen in the smaller models." Flan-T5-XXL handlers under a
GPT-3 decomposer reach scores "comparable to the Codex-only systems" — the paper's
strongest evidence that a good decomposition lets you downsize the workers.

**7. A one-module bolt-on fixes a large chunk of CoT's math errors.** Replacing the
regex answer-extractor (`answer is .*`) with a GPT-3 `gpt_ans` handler that reads the
chain and emits the answer yields +17 pts on MultiArith (78 → 95) and +14 on GSM8K
(36 → 50.6). *The authors' reading:* modularity lets you aim a targeted handler at "the
source of error in any system" — and the sheer size of the gain illustrates how much of a
reported CoT score can be answer-extraction failure rather than reasoning failure.

**8. Results are robust to prompt choice and to the decomposition scheme.** App. D:
ordering holds for each of P1/P2/P3 individually. App. E: two alternative decomposition
schemes were tried and "performance did not drop."

### Cost and call-count discussion

The paper does discuss this, though narrowly — it is about *calls as a function of input
size within a scheme*, never about DecomP's total cost against a single-call baseline.

- Algorithm 1 is captioned as running in **O(log n) calls to the LM** for the half-
  splitting reversal (n = sequence length).
- App. E constructs the alternative `reverse(list) = reverse(list[1:]) + list[0]`, noting
  it "requires more GPT3 calls (O(n)) compared to the original approach of splitting the
  list into halves (O(log(n)))."
- The result of that comparison is the paper's only explicit accuracy-vs-cost trade:
  "The new reversal decomposition schema was actually **stronger on longer inputs at the
  cost of more calls to GPT3**." Both beat CoT.
- The `foreach`/`project_values` operator fans out one call *per list element*, so
  breadth as well as depth multiplies calls, but this is never costed.
- Cost surfaces indirectly elsewhere as a *constraint on the experiments*: GSM8K and
  MultiArith were subsampled to 300/200 items "due to costs with API usage."

What is absent: any tokens-consumed, latency, or dollar comparison of DecomP against CoT
on the same task; any accounting for the fact that the decomposer's context is re-sent and
grows at every step; and any statement of the multiplier on the tasks where the headline
wins are claimed.

## Open questions the paper itself raises

This is the paper's weakest section, and the weakness is structural: **there is no
limitations section.** The v2 read here has no "Limitations" heading and the conclusion
is purely affirmative. What it does raise, in its own framing, is scattered:

- **Decomposer capacity is a stated bottleneck.** Footnote 8, in the ODQA setup: "We
  still use GPT3-sized models for decomposition since only these models are reliably able
  to produce the required structured outputs." The paper flags that the decomposer role
  does not scale down, without investigating why or how far.
- **The operator set is admittedly partial.** They use two of Khot et al.'s compositional
  operators "although it is capable of using all their operators (which also capture the
  QDMR operators from Wolfson et al., 2020)" — an unexercised claim of coverage.
- **Helper operators are convenience, not necessity.** They note `foreach` "is not
  strictly necessary" — the decomposer could emit each sub-question individually — and
  that it exists "to reduce the manual effort needed to specify the decomposition and also
  reduce potential errors during decomposition." App. E then makes the trade explicit and
  two-sided: generating each sub-question is "more robust to formatting issues in the
  output answers," but "the generated sub-questions may not correctly use all the elements
  of the list (change in order, missed element, repeated elements, etc)."
- **Decomposition granularity is an open dial.** Coarse vs. fine is presented as a
  human-effort/accuracy trade-off with no principle for setting it.
- **Explicit future work** is thin and confined to App. B: extending DecomP to "other
  complex answer types, e.g. non-extractive answer generation from chain-of-thoughts."
- **Inference is admittedly approximated.** The MAP formulation is exact; "for
  practicality, such computations are approximated using greedy search," with no search
  over decompositions — notably a *retreat* from Khot et al. (2021), which used best-first
  search over the decomposition space, and the paper does not revisit whether that loss
  matters.

Unraised by the paper, but visible in it: who writes the decomposer prompt, and how much
task-specific human insight each decomposition encodes, is never treated as a cost.

## Appreciation

Separating mechanism from magnitude, as asked.

### Mechanism — what transfers as an argument

- **The decomposer/handler split with a non-LLM controller in between.** This is the
  paper's durable contribution and it transfers cleanly. Three roles — *plan the next
  step*, *do the step*, *route and hold state* — with only the first two being models.
  The controller being symbolic is what makes the loop terminate on a sentinel, makes
  `#i` references resolvable, and makes handler substitution possible at all.
- **The interface argument.** Because a handler is addressed by name and consumes a
  sub-question in natural language, its implementation is free: prompt, nested program,
  symbolic function, or a different (smaller) model. The paper demonstrates all four
  behind one interface. This argument does not depend on GPT-3 at all.
- **The rolled-out control as an experimental design.** Writing the same procedure as one
  chain and comparing is the right way to ask whether *structure* or *knowing the steps*
  is doing the work. That methodological move transfers regardless of what one thinks of
  the numbers.
- **Recursion on input length as a distinct thing from recursion on difficulty.** This is
  the distinction I would most want carried forward. Mode (a) is *"this step is too hard,
  break the step down"* — depth is set by observed handler failure. Mode (b) is *"this
  input is too big, apply the same task to smaller inputs and recombine"* — depth is set
  at runtime by the data, and terminates at a base case chosen as the size where the model
  is already reliable. Mode (b) converts a competence question into a size question, and
  the argument is structural, not empirical: as long as recombination is cheap and the
  base case is reliable, accuracy stops being a function of input length.
- **Finding 4 as a mechanism claim.** That the unrolled recursive prompt *fails* while
  the modular one succeeds is an argument about expressivity — a linear chain has no
  abstraction barrier, so a recursive procedure written into one must inline every level.
  This is the strongest reason in the paper why modularity is not merely tidiness.
- **Error localisation.** That every observed failure was a *handler* failure, not a
  decomposer failure, is a claim about where to look — and modularity is what made the
  claim checkable at all. The debuggability argument is partly self-demonstrating.
- **A large "reasoning" gap can be an extraction gap.** The +14/+17 math result is a
  mechanism-level warning about how scores are read.

### Magnitude — numbers valid only inside this setup

Nearly all of them, and the ceiling results most of all.

- The near-100% EM and zero standard deviation on k-th letter concatenation are numbers
  about a **constructed task with a known-correct symbolic algorithm** and a 100-example
  test set. Letter indexing is a tokenisation artefact of 2022-era GPT-3; the *specific*
  gap over CoT is not portable to models that index characters reliably.
- List reversal is chosen precisely because `davinci-001` fails at it and `davinci-002`
  does not. The headline "a weaker model reaches a stronger model" is a statement about
  that pair of models on that task, deliberately staged.
- CommaQA is synthetic, with invented entities ("Wetherality", "Pompasole") specifically
  designed to defeat parametric knowledge, and here it is *shrunk* to fit a 2049-token
  window. The CoT baseline is handicapped by that window in a way it would not be today;
  a chunk of the CommaQA margin is a context-budget artefact, and the authors say as much
  when they explain that separate handlers can carry more examples than fit in one CoT.
- The ODQA F1 gains rest on hyperparameter-tuned K with *different search ranges per
  arm*, and 2Wiki/MuSiQue corpora are constructed by pooling the datasets' own paragraphs
  — a far friendlier retrieval setting than open web. The HotpotQA near-tie, and the
  admission that HotpotQA gains are "mostly seen in the smaller models," are the honest
  edge of this result.
- The +14/+17 math numbers are gains over a **specific weak baseline** (a regex), on
  subsampled test sets, and say more about the baseline than about decomposition.
- The O(log n) / O(n) call counts are properties of two hand-written reversal schemes,
  not of DecomP.

Overall: the mechanisms are stated crisply enough to be re-tested; the magnitudes are all
2022-GPT-3-shaped, and several of the tasks are ones where the flat baseline is
constrained by a context window that no longer binds.

## How it could serve a harness-design effort

Stemming the discussion rather than resolving it.

**What a harness could take directly.** The three-role separation — decomposer, handler
library, symbolic controller — is a harness architecture, not just a prompting technique,
and the paper's software-library analogy is the design brief. The controller owning the
loop, the state (`#1`, `#2`, …), the routing table, and the termination sentinel is a
concrete answer to "what should be code and what should be a model." The handler-behind-
an-interface pattern is the substitution point: it is what lets a harness put retrieval,
a calculator, a small finetuned model, or another decomposed program behind the same call
site, and swap one for another without touching the caller. The named-sub-task tag is
doing double duty as a routing key and as a *contract* about what that call is for.

**Questions it opens rather than closes.**

- *Who writes the decomposition?* Every decomposer prompt here is hand-authored, and the
  handler library is hand-assembled per task. The paper's own framing — "the top-level
  program" — concedes that a human wrote the program. A harness that wants decomposition
  discovered at runtime gets no help here; what it gets is a clear statement of what the
  discovered artefact would have to look like.
- *What sets the depth?* Both modes answer this outside the model: hierarchical depth is
  set by the author after observing a handler fail; length-recursion depth is set by a
  base-case threshold written into the prompt as arithmetic. Neither is a budget and
  neither is emergent. A harness with a call or token budget has no mechanism here for
  spending it.
- *When should a harness decompose at all?* The paper only ever reports settings where it
  decomposes. There is no negative result, no task where DecomP loses to a direct attempt,
  and therefore no learned boundary. The nearest thing to a decision rule is implicit:
  decompose when a step is individually unlearnable in-context, or when difficulty scales
  with input size.
- *What does it cost?* As noted, only relative call counts between two schemes. A harness
  needs the absolute multiplier against a single call, and the growing decomposer context
  makes that multiplier super-linear in steps. This paper does not supply it.
- *What happens when a handler is wrong?* Answers are appended to the decomposer's
  context as fact. There is no verification step, no retry, no confidence signal, and the
  error analysis confirms handler errors propagate straight to the final answer. Recursion
  makes this sharper: an error at a leaf is recombined upward with no check.
- *Where does the decomposer's own capability floor sit?* Footnote 8 says the decomposer
  cannot be a small model. If a harness's orchestrator must be the expensive model while
  workers can be cheap, that is an architectural constraint with direct cost consequences,
  and the paper flags it in passing without measuring it.

**Major concerns for anyone leaning on this.** The evidence base is 2022 GPT-3-class
models under a ~2k–8k token ceiling; two of four case studies are tasks the authors
constructed, and the operator vocabulary comes from their own prior work. Several wins are
plausibly context-budget wins — separate prompts fit more examples than one chain — which
is a real advantage that shrinks as windows grow. Greedy decoding with no search over
decompositions means the reported numbers are a lower bound in one sense and unprotected
against a single bad decomposition in another. And the framework's flexibility is
untested at its own edges: no result shows a decomposition deep enough, or a handler
library large enough, for routing itself to become the failure mode.

## Five citations worth chasing next

1. **Zhou et al. (2023), "Least-to-most prompting enables complex reasoning in large
   language models," ICLR 2023.** The paper's designated nearest rival and the only
   decomposition baseline it re-implements; the two stated differences (one-shot vs.
   iterative sub-problem identification, and having to learn which prior answers are
   relevant) are the sharpest structural contrast in the literature as framed here.
2. **Khot et al. (2021), "Text modular networks: Learning to decompose tasks in the
   language of existing models," NAACL 2021.** The direct ancestor — a *trained* next-
   question generator over a fixed set of agents, with **best-first search over
   decompositions** at inference. It holds exactly what DecomP dropped (search, and a
   learned decomposer), which makes it the right control for what few-shot prompting cost
   them.
3. **Dua et al. (2022), "Successive prompting for decomposing complex questions,"
   EMNLP 2022.** The other close relative; DecomP explicitly borrows its iterative
   generate-then-answer loop, so it is the place to see that loop studied on its own.
4. **Khot et al. (2022), "Hey AI, can you solve complex tasks by talking to agents?"
   Findings of ACL 2022.** Supplies both the CommaQA benchmark and the compositional
   operator set (`project_values`, `project_values_flat_unique`) that do all the
   recombination here — the operator semantics are defined there, not in this paper.
5. **Dohan et al. (2022), "Language model cascades," arXiv:2207.10342.** The formal frame
   DecomP adopts for expressing inference as probabilistic program composition over LMs;
   the natural place to look for what a principled (non-greedy) inference procedure over
   a decomposition would be.

*Runner-up worth noting:* Wolfson et al. (2020), "Break it down: A question understanding
benchmark" (QDMR) — cited as the operator vocabulary the framework claims to subsume, an
unexercised claim in this paper.
