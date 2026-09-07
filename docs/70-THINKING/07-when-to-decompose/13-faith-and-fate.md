# Faith and Fate: Limits of Transformers on Compositionality

## Density

**Density: HIGH** — Nearly every section is load-bearing (a formalism, an experiment, a proof, an error taxonomy) with almost no padding, and the paper's central object — decomposing a task into a graph of sub-steps, measuring depth and width, and showing accuracy collapses as those grow — is directly about the mechanics of task decomposition rather than adjacent to it.

**Keywords (mine).** computation graph; reasoning depth; reasoning width; average parallelism; scratchpad linearisation; subgraph matching; shortcut learning; error propagation; out-of-distribution generalisation; grokking; relative information gain; error taxonomy (local / propagation / restoration).

**Year.** 2023 (arXiv v1 May 2023; v3 31 Oct 2023).

**Venue.** Advances in Neural Information Processing Systems 36 (NeurIPS 2023). Peer-reviewed.

**Authors.** Nouha Dziri, Ximing Lu, Melanie Sclar, Xiang Lorraine Li, Liwei Jiang, Bill Yuchen Lin, Peter West, Chandra Bhagavatula, Ronan Le Bras, Jena D. Hwang, Soumya Sanyal, Sean Welleck, Xiang Ren, Allyson Ettinger, Zaid Harchaoui, Yejin Choi. (Note: the author list on the arXiv HTML includes Sean Welleck, who is not in the citation given in the brief.)

## Approach

The paper asks why transformer LLMs succeed on apparently hard reasoning tasks and
fail on apparently trivial ones, and answers with a single instrument: **express the
task as a computation graph, then vary the graph and watch accuracy**.

### The formalism

Given a deterministic algorithm `A` with a set of primitive functions `F_A`, and
inputs `x`, they define the *static computation graph* `G_A(x) = (V, E, s, op)`, a
directed acyclic graph:

- Nodes `V` are every variable value arising during `A`'s execution; each node `v`
  carries a value `s(v) ∈ ℝ`.
- Edges `E` are the argument relations: for a non-source node `v` with parents
  `U = {u_1,…,u_j}`, `s(v) = f(u_1,…,u_j)` for some primitive `f ∈ F_A`.
- Because each node is defined by exactly one primitive application, `op: V → F_A`
  labels each node with the primitive that produced it.
- Source nodes `S ⊂ V` are the input `x`; a single leaf `o` is the output,
  `A(x) = s(o)`.

The crucial move for LLM evaluation: to train or test a model on following `A`, the
graph must be **linearised**, and because the models are autoregressive the
linearisation must be a *topological ordering* of `G_A(x)`. That linearisation is
exactly what they call a **scratchpad** — a verbalisation of a topological order of
the computation graph. This makes "chain of thought" and "the graph" the same object
in two presentations, which is what lets them compare a model's emitted reasoning
against ground truth node by node.

### The complexity metrics

Three graph-derived quantities stand in for "how compositional is this task
instance":

- **Reasoning depth** — a node's *layer number* is the length of the **longest**
  path from any source node to it; reasoning depth is the largest layer number in
  the graph. It proxies the maximum number of sequentially dependent hops.
- **Reasoning width** — using `d_S(v)`, the **shortest** distance from `v` to any
  source, the width is the **mode** of `{d(v) : v ∈ V}`. It proxies the number of
  variables that must be held in parallel.
- **Average parallelism** — `|V|` divided by reasoning depth: average width across
  the whole graph rather than only at the mode.

Note the asymmetry worth flagging: depth uses longest-path, width uses
shortest-distance-then-mode. Average parallelism is the metric that carries most of
the plotted results.

### Relative Information Gain

A separate instrument for explaining *partial* successes. Treating a task as a
distribution `(X_1,…,X_n, Y_1,…,Y_m)`, they compute
`RelativeIG(Y_j, X) = [H(Y_j) − H(Y_j|X)] / H(Y_j) ∈ [0,1]`
— the normalised information a subset of inputs carries about a single output
element. High relative IG predicts a **surface pattern** the model is likely to learn
as a shortcut, without executing the graph. Applicable to any node vs. a set of its
ancestors, not just outputs vs. inputs.

### The three tasks

- **Multi-digit multiplication.** Long-form `O(k1·k2)` algorithm, up to 5×5 digits,
  base 10. Primitives: one-digit multiplication, sum, mod 10, carry over,
  concatenation. Sources are input digits; intermediates are partial products.
- **Einstein's puzzle** (logic grid / constraint satisfaction). `K` houses × `M`
  attributes. The graph comes from a greedy **elimination function** that
  deterministically fills the cell(s) requiring the fewest clues at each step;
  sources are clues, intermediate nodes are partially-filled matrices, output is the
  filled `K×M` matrix. Graphs are produced by an existing puzzle solver.
- **Dynamic programming.** A relaxation of Maximum Weighted Independent Set: given
  an integer sequence (elements in `[−5,5]`), find the max-sum subsequence with no
  two adjacent elements; solvable in `O(n)` via
  `dp_i = max(dp_{i+1}, a_i + dp_{i+2}, 0)`, then a reconstruction pass. Primitives:
  equals, and, not, indicator, sum, max. They deliberately choose an implementation
  whose graph topology is fixed for a given input length.

### The experimental programme

Four escalating attempts to get transformers to actually execute the graph —
zero/few-shot prompting; exhaustive question-answer finetuning; question-**scratchpad**
finetuning (i.e. supervising the decomposition itself); and training far beyond
overfitting to probe for grokking — plus three analyses of *why* they fail:
information-gain surface patterns, training-set subgraph frequency, and a per-layer
error taxonomy. Section 4 then supplies two propositions on error accumulation.

## Models targeted

Six models, evaluated January–May 2023 via the OpenAI API:

- **GPT4** (`gpt-4`) — prompting only; the authors state they lacked the access to
  push it further.
- **ChatGPT** (`GPT-3.5-turbo`) — prompting only.
- **GPT3** (`text-davinci-003`) — the workhorse; the only model **finetuned**, on all
  three tasks, in both question-answer and question-scratchpad formats.
- **FlanT5** and **LLaMA** — prompting only; results reported as near zero across
  problem sizes for the DP task.
- **GPT2-XL** — trained from scratch as a tokenisation control (see below).

Finetuning detail (§B.1): 14/12/4 epochs for multiplication/puzzle/DP on
question-answer; 16/8/2 on question-scratchpad; batch ≈ 0.2% of training set size;
learning-rate multiplier swept 0.02–0.2, 0.2 chosen; inference at temperature 1 with
nucleus `p = 0.7`. **500 test examples per task per model.**

## Benchmarks / datasets

All three datasets are **synthetic and self-generated** — no external benchmark is
used. This is deliberate: the point is exhaustive control over graph depth and width,
which an off-the-shelf benchmark cannot give.

- **Multiplication.** Exhaustively enumerated pairs up to 5 digits each. Finetuning
  used all `k1×k2` with `1 ≤ k1,k2 ≤ 4` and `k1·k2 ≤ 9`, ≈ **1.8M pairs**; 10%
  validation, 10% test.
- **DP.** All lists up to 5 elements over `[−5,5]` (`11^n` lists of size `n`),
  ≈ **142K pairs** for training in one place in the text and 41K in another
  (§3.1 says ~142K DP and ~41K puzzle; §B.3 says 142K puzzle and 41K DP — the two
  passages transpose the numbers, an internal inconsistency). OOD evaluation on
  lists of size 6–10.
- **Puzzle.** Instances up to `(K,M) ≤ (4,4)`, subsampled because of combinatorial
  explosion; OOD evaluation on larger grids. Clue types: `found_at`, `same_house`,
  `direct_left`, `besides`, with harder types (`not_at`, `left_of`,
  `two_house_between`) reserved for auxiliary experiments. Puzzles are generated by
  sampling a solution matrix, over-generating all valid clues, then randomly removing
  clues until the solution is unique.

Scratchpads for multiplication and DP are template-generated from the algorithm;
puzzle scratchpads come from an external solver. The authors note they tried several
scratchpad verbosities and kept the best-performing one.

## Author incentive

- **Affiliation.** Predominantly the **Allen Institute for AI** (Mosaic team), with
  University of Washington, USC, and University of Chicago.
- **Funding.** NSF DMS-2134012; DARPA MCS through NIWC Pacific (N66001-19-2-4031);
  AI2.
- **Stake.** No product being sold, and no model or dataset being promoted as an
  improvement — the societal-impact note explicitly says they "do not introduce any
  new model or dataset that future work may leverage". The stake is **positional**:
  this is a limitations paper from a lab that publishes critically on LLM
  capabilities, and it is arguing against the "sparks of AGI" framing it cites in its
  first paragraph. The incentive runs toward finding and dramatising a limit. Set
  against that, they are evaluating closed models they do not own and spent large
  sums (a stated $50,000 and $40,000 on two grokking runs alone) trying to make those
  models succeed before concluding they cannot — the experimental design is
  adversarial to their own thesis, not friendly to it.
- **Access asymmetry worth naming.** GPT4, the strongest model, could only be
  prompted, not finetuned. The finetuning conclusions rest on GPT3.

## Measurement methodology (brushed)

- **Dependent variable.** Almost always **exact-match accuracy on the final answer**
  — a strict binary per instance. For the surface-pattern analyses the DV changes to
  accuracy on *parts* of the answer (first digit, last digit, number of trailing
  zeros, order of magnitude). For the error taxonomy the DV becomes a **per-node**
  categorical label.
- **Independent variables.** Problem size (digits; `K`,`M`; sequence length) and the
  graph metrics (depth, width, average parallelism). Training splits are constructed
  *by* depth and width, not just by problem size — this is the methodological core:
  it lets them ask whether a model trained on graphs of depth ≤ d generalises to
  depth > d, holding the primitives fixed.
- **What is controlled.** The train/test split is disjoint by construction; for the
  subgraph-frequency analysis they note both frequencies tend to zero at large depth
  precisely because the split is disjoint. Tokenisation is controlled by training
  GPT2-XL from scratch with one token per digit and per math symbol (it still fails
  on 3×3). The DP implementation is chosen so graph topology is constant for a given
  input length, removing topology as a confound.
- **N.** 500 test examples per task per model. Training sets in the 10⁴–10⁶ range.
  Grokking: 420K steps (≈60 epochs) on question-answer, 30K steps (≈40 epochs) on
  question-scratchpad.
- **Significance.** Not treated formally — **no confidence intervals, no error bars,
  no hypothesis tests reported anywhere**. The paper relies on effect sizes large
  enough to be self-evident (near-100% in-domain vs. near-0% OOD) and on the
  monotonicity of curves. The one relational claim — "average parallelism negatively
  correlates with accuracy" — is asserted from a scatter plot without a reported
  coefficient. Likewise "significantly more frequently" in the subgraph analysis is
  visual, not tested.
- **Reproducibility.** Code and data released at `github.com/nouhadziri/faith-and-fate`.

## Key findings

### 1. Accuracy collapses with graph complexity, on every access route

Zero-shot accuracy "decreases to near zero as task complexity increases", whether
complexity is measured by raw problem size or by **average parallelism** — the latter
is the paper's headline framing that the *graph*, not the surface problem, is what
predicts failure. The anchor number given in the introduction: off-the-shelf ChatGPT
and GPT4 reach only **55% and 59%** on 3-digit × 3-digit multiplication. Few-shot
prompting changes little; on the puzzle task few-shot was *worse* than zero-shot.

### 2. Exhaustive task-specific finetuning does not produce the algorithm

GPT3 finetuned on ~1.8M multiplication pairs is near-perfect **in-domain** and falls
off a cliff **out-of-domain**. Critically, the OOD splits are defined by **graph depth
and width** — so the failure is not "unseen inputs" but "same primitives, deeper or
wider composition". Their reading: "systematic problem-solving capabilities do not
emerge via exhaustive training on task-specific data."

### 3. Supervising the decomposition does not fix it

Finetuning on question-**scratchpad** pairs — i.e. handing the model a correct
topological linearisation of the computation graph for every training instance — again
yields near-perfect in-domain and total OOD failure, "in particular, wider or deeper
computation graphs". Scratchpad *prompting* does lift GPT4 above zero-shot across most
problem sizes, but "degrades to zero as the complexity increases". This is the finding
with the sharpest bearing on the Subject: **being told the decomposition is not the
same as being able to execute it**, and the benefit of an explicit step-by-step
decomposition is bounded in depth rather than unbounded.

Their causal reading is explicitly about autoregression: the models "depend on a
greedy process of producing the next word to make predictions without a rigorous
global understanding of the task", and this "cannot be resolved by instructing the
model to generate a step-by-step solution".

### 4. No grokking

Training far past the overfitting point (420K steps question-answer at a stated
$50,000; 30K steps question-scratchpad at $40,000) produced **no** OOD improvement.
They hypothesise task difficulty impedes learning a well-structured representation,
decline to explain grokking, and note that even if it did emerge this route would be
"inefficient and unscalable".

They also make the scaling argument concrete and damning: **Table 1** extrapolates
GPT3 finetuning cost to full 5×5 multiplication mastery — approximately **9.1 billion
examples**, **$12 million** without scratchpad and **$700 million** with. Memorising
the graph does not scale.

### 5. Partial successes are surface patterns, predicted a priori by information gain

Relative IG predicts that in multiplication the **last** digit(s) of the output depend
solely on the last digit(s) of each input (valid always, by modular arithmetic) and
the **first** digit(s) correlate with the first digit(s) of the inputs (a spurious but
learnable correlation). The reported RelativeIG table bears this out: the pair
`(x_n, y_n) → z_2n` has relative IG of **exactly 1.000** at every problem size
(2×2 through 5×5), while each single digit alone gives ~0.223 and the leading-digit
relations ~0.199. Empirically models do learn these, plus order of magnitude and
number of trailing zeros — and score far higher on these fragments than on the full
answer. So a model can look partly competent at a compositional task while executing
none of the composition.

### 6. Linearised subgraph matching

The paper's central mechanistic claim. For each node `v` in the model's generated
graph `Ĝ_A(x)`, define its **full computation** `FC(v)` as the subgraph induced by
`v` and all of its ancestors. `FC(v)` counts as *seen during training* if it is
**isomorphic** to some `FC(w)` in some training instance's graph. They then measure
the average training frequency of the full-computation subgraphs required by a test
instance, split by whether the model got that instance right.

Result: those subgraphs appear **significantly more frequently in training data for
correctly predicted test examples than for incorrectly predicted ones**, on both
multiplication and DP. Both curves fall toward zero at large subgraph depth — which is
expected given the disjoint split, and is itself the point: at depth, there is nothing
to match against, and accuracy goes with it.

Their reading: "pattern matching — and not general reasoning capabilities — may be the
cause behind correct model outputs", effective at low compositional complexity and
failing as complexity rises. In the discussion they name the mechanism: transformers
"solve multi-step compositional problems by **collapsing the depth** of the
compositional operations via analogical pattern matching".

### 7. The error taxonomy: single steps work, composition does not

Comparing ground-truth `G_A(x)` against the model's `Ĝ_A(x)` node by node, every node
is labelled:

- **fully correct** — `v` and all its ancestors have correct values *and* correct
  computations;
- **local error** — parents are correct but `v` is derived from an incorrect
  computation (a one-hop reasoning failure);
- **propagation error** — the computation at `v` is correct but a parent's value is
  wrong (an inherited failure);
- **restoration error** — `v` has the *correct value* despite an *incorrect
  computation*.

Findings, plotted against layer number for few-shot GPT4 and finetuned-with-scratchpad
GPT3:

- Fully-correct ratio is near-perfect at low layers and **decreases sharply toward
  zero as layer number grows**. This is the depth/accuracy relation measured *inside*
  a single instance rather than across instances.
- **Propagation errors exceed local errors.** Models can execute the primitive; they
  cannot carry a correct value through a chain. This is the empirical face of the
  error-accumulation argument.
- DP and puzzle show **high restoration-error rates** — right answer, wrong working —
  which the authors read as memorisation.
- The sharpest single memorisation datum: **82.3% of correct final answers on 4-digit
  × 2-digit multiplication (a setting unseen in training) contained at least one error
  in the computation graph.** They attribute this to (input, output) multiplication
  pairs being frequent in pretraining data while intermediate steps are not.

### 8. The theoretical argument: error accumulation is exponential in both axes

Two propositions, proved in Appendix D, covering the two ways an algorithm composes.
Both are about *any* estimator, not specifically transformers.

**Proposition 4.1 / D.1 (width — parallel applications).** Let
`f_n(x) = h_n(g(x,1),…,g(x,n))`: `n` independent applications of `g`, combined by
`h_n`. Assume `h_n` is estimated perfectly and is *almost injective* — collision rate
`P(h_n(X)=h_n(Y) | X≠Y) < c_n < c ≪ 1`. If `P(g ≠ ĝ) = ε > 0` with independent
errors, then

`P(f_n ≠ f̂_n) > 1 − c_n − (1−ε)^n·(1−c_n)`, so `liminf_{n→∞} P(f_n ≠ f̂_n) ≥ 1 − c`.

The derivation is a clean law-of-total-probability split on the event `X = Y`: all `n`
sub-results correct has probability `(1−ε)^n`, and the only other route to a correct
answer is a **collision** in `h_n` — getting the right output from wrong inputs.
Convergence is exponential. If the collision rate itself decays geometrically
(`c_n ≤ βα^n`), the failure probability tends to **exactly 1**.

**Corollary D.1** instantiates this: if a model does shifted addition perfectly but
gets even one `m`-by-1 digit multiplication wrong, its probability of correctly doing
`m`-by-`n` digit multiplication by the long-form algorithm **tends to 0** as `n` grows
(they show `c_n < βα^n` with `α = 0.1`, `β = 10^m`). They also note the corollary
exposes two distinct exponential error sources: errors in *selecting* which numbers to
multiply (`s`), and errors in the multiplication itself (`d`).

**Proposition 4.2 / D.2 (depth — iterated applications).** Let `f_n(x) = g^n(x)`.
Let `c` bound the probability of *recovering* from a mistake — i.e.
`P(g(X) = ĝ(Y) | X ≠ Y) ≤ c` — and let `P(g ≠ ĝ) = ε > 0`, with `c + ε < 1`. Writing
`s_n := P(f_n = f̂_n)`, total probability gives the recursion

`s_n ≤ (1 − ε − c)·s_{n−1} + c`,

with `s_1 = 1 − ε`; induction plus the geometric series yields
`s_n ≤ b^{n−1}(1 − ε − c/(c+ε)) + c/(c+ε)` where `b = 1−ε−c`, hence
`liminf_{n→∞} P(f_n ≠ f̂_n) ≥ 1 − c/(c+ε)`.

The structure is worth stating plainly: **the ceiling on eventual accuracy is
`c/(c+ε)` — the recovery rate divided by (recovery + error rate).** Accuracy at depth
is not set by how good the model is in absolute terms; it is set by the *ratio* of
recovery to error. §D.3 argues `c ≪ ε` is the realistic regime whenever `g` has low
collision: if errors are roughly uniform over `g`'s image, `c ≈ ε/|Im(g)|`, and a
low-collision `g` has large `|Im(g)|`. Writing `ε = m·c`, the limit is `m/(m+1)` → 1.
So for discrete, low-collision reasoning steps, **failure probability tends to ≈ 1**.

**Lemma D.2** generalises past the assumption of a single valid reasoning chain, to a
state-transition framing: `ε` is the chance of stepping from a valid state to an
invalid one, `c` the chance of recovering from an invalid one; same `1 − c/(c+ε)`
limit. This matters — it means the result does not depend on there being one right
path, only on error and recovery rates per step.

**Corollary D.3** shows all three empirical tasks are instances: `m`-by-1 digit
multiplication, the DP recursion, the DP reconstruction pass, and the puzzle's
elimination function are each a fixed step applied repeatedly. For the puzzle they
note `m` is *not* fixed but grows with problem size.

They add a separate instability observation: if `g` is affine (`Fx + c`), `g^n` is a
first-order vector autoregression, **unstable when any eigenvalue of `F` has
|λ| ≥ 1** — so repeated application can give unbounded, not merely accumulating,
error. Nonlinear maps are flagged as possibly worse and left out of scope.

### The authors' own reading

Their summary is that transformers achieve what looks like compositional reasoning by
**collapsing compositional depth into analogical pattern matching over linearised
subgraphs**, which works while the required subgraphs are in the training
distribution and fails outside it; and that the autoregressive, greedy next-token
process structurally limits error recovery and prevents a global grasp of the task.
They generalise cautiously — "the strong performance of transformers should be taken
with a certain grain of salt" — noting that tasks which look compositional may not be,
because input-output pairs in training permit shortcuts.

Their own prescriptions (§5), stated as suggestions rather than results:

1. Use transformers for tasks needing **only a few chained compositional steps**.
2. Use them where evaluation **can afford leniency** — approximate answers not
   requiring the whole graph to be executed (their example: the most significant digit
   of a product).
3. **Augment with planning modules and refinement methods** that iteratively improve
   generations.

They also stress that Props. 4.1 and 4.2 "apply to any high-performant estimator of
reasoning tasks", not only to transformers.

## Open questions the paper itself raises

In its own framing (§8 Limitations, §5, and scattered notes):

- **Correlation, not attribution.** For the scratchpad analyses they can only
  establish "a correlation between the model generation and its preceding context",
  because they lack access to the studied models' activations and "cannot inspect the
  exact tokens model attends to when making the prediction". The
  subgraph-matching claim is therefore behavioural, not mechanistic in the
  interpretability sense.
- **Linearisation is a choice, and may not be a neutral one.** They "posit that
  alternative approaches to linearizing reasoning processes may yield different
  performances and provide opportunities for further exploration". A computation graph
  admits many topological orderings; they test one per task (chosen after trying
  several verbosities).
- **Compute and access limits.** They explicitly cannot "push the empirical limits of
  transformers even further in terms of training data size and number of epochs", and
  had limited access to GPT4. They issue a "call for broad participation" inviting
  better-resourced groups to test whether the limits hold.
- **Grokking is unexplained.** They observe its absence in multiplication but do not
  claim to explain it; whether task difficulty prevents the well-structured
  representation that grokking is thought to require is left open.
- **Expressiveness bounds may not be tight.** They note that all tasks studied belong
  to a class transformers can express, "suggesting that known upper bound might not be
  tight" — i.e. there is a gap between what transformers *can* represent and what they
  *will* learn, and that gap is their real subject.
- **Nonlinear iterated maps** are left for future work; they analyse the affine case
  and say nonlinear behaviour "could be even more acute".
- **Generalising Prop. 4.2** past single-valid-chain tasks is sketched (Lemma D.2) but
  not developed empirically.

## Appreciation

### MECHANISM — what transfers as an argument

**The computation graph as a measuring instrument.** The strongest contribution, and
the most portable. Reducing "how compositional is this task" to depth, width, and
average parallelism of a DAG over named primitives gives a way to *construct* train/test
splits along the axis of composition rather than along the axis of surface
difficulty. Splitting by graph depth is what turns a vague claim ("doesn't
generalise") into a sharp one ("does not generalise along the composition axis while
holding primitives fixed"). This design transfers to any task one can express as an
algorithm.

**The distinction between knowing a step and composing steps.** The error taxonomy —
particularly the local/propagation split, and the propagation-dominates result — is a
genuinely clean separation of two failure modes that are usually conflated in
end-to-end accuracy. It supports the argument that per-step competence and multi-step
competence are different quantities and that the second is not implied by the first.

**Restoration errors as a measurement warning.** The finding that a correct final
answer frequently sits atop an incorrect computation graph — 82.3% in one setting — is
a methodological point with reach well past this paper: **outcome-correct does not
imply process-correct**, so any evaluation or any control loop that reads only the
final answer is reading a lossy and optimistically-biased signal.

**The `c/(c+ε)` ceiling.** The most useful piece of the theory is not the exponential
decay — that much is intuitive — but the *shape* of the asymptote in Prop. 4.2.
Accuracy at depth is governed by the **ratio of recovery rate to error rate**, not by
error rate alone. That reframes the intervention: reducing `ε` gives diminishing
returns at depth, whereas raising `c` — introducing genuine recovery, error detection,
correction, a mechanism that can re-enter a valid state after leaving it — changes the
ceiling itself. Lemma D.2's state-transition generalisation makes this argument
independent of there being one right answer path, which considerably widens where it
applies. This is a mechanism claim and it stands on its own.

**Shortcut availability predicts partial success.** That relative information gain
predicts, *before* running any model, which fragments of an answer will be guessable
without composition is a nice piece of design. It provides a way to ask of any
benchmark: how much of this can be scored correct without performing the reasoning it
purports to test?

### MAGNITUDE — numbers valid only inside this setup

Essentially every number here is **setup-bound** and should not travel:

- **55%/59% on 3×3 multiplication**, and all the zero-shot curves, are properties of
  specific January–May 2023 model snapshots accessed through an API, at temperature 1
  with nucleus sampling `p=0.7` — a *sampling* configuration, not greedy decoding,
  which will itself depress exact-match accuracy on a task with one right answer. The
  models are long superseded; the numbers are historical.
- **82.3%** restoration/hidden-error rate is one cell (4×2 multiplication) of one
  model in one training regime. The qualitative fact — that this rate is large — is
  the transferable part; the figure is not.
- **The specific depth at which accuracy hits zero** is entirely a function of task,
  primitive granularity, and — importantly — *how the authors chose to draw the
  graph*. Depth is not intrinsic to a problem: choosing coarser primitives yields a
  shallower graph for the same task. The multiplication graph is deep because they
  chose per-digit primitives. This is a real degree of freedom in the formalism and
  the paper does not dwell on it.
- **The RelativeIG values** (0.223, 0.199, 1.000) are properties of the uniform digit
  distribution they sampled, not of multiplication in the wild.
- **The cost table** ($12M/$700M) is 2023 `text-davinci-003` API pricing extrapolated;
  the argument it supports (exhaustive memorisation scales combinatorially) survives,
  the dollar figures do not.
- **"No grokking"** is a negative result on one task, one model, one budget, and the
  authors say so.

### Where I would push back

- **`ε` is assumed constant and errors independent.** Prop. 4.1 requires independent
  errors in `ĝ`; Prop. 4.2 requires a fixed per-step `ε`. For an LLM neither is
  obviously true — error probability plausibly *depends on* the context accumulated so
  far, and errors within one generation are correlated through shared context. The
  propositions are honest stylised models, and the authors call them "stylized
  examples", but the exponential result is driven by assumptions that are asserted
  rather than measured. Notably, they never *estimate* `ε` and `c` empirically from
  their own runs, though D.1 observes the proof "gives us empirical bounds once ε and
  α are approximated" — that measurement is left undone, so the theory and the
  experiments are adjacent rather than joined.
- **The propositions are not about transformers.** They apply to any noisy estimator
  of an iterated function. That generality is stated plainly and honestly, but it also
  means §4 supports no conclusion specific to the architecture in the title; it
  constrains *any* system that composes fallible steps without recovery — including,
  awkwardly, systems built out of many such calls.
- **Depth and width are entangled with training-data frequency.** Deeper graphs are
  also rarer graphs. The paper's own subgraph analysis shows correct answers track
  subgraph frequency, and frequency falls with depth — so "fails at depth" and "fails
  where training coverage is thin" are hard to separate here, and the disjoint-split
  design guarantees they co-vary. The authors treat this as *the* explanation rather
  than as a confound, which is defensible but is a choice.
- **Statistical treatment is thin.** No intervals, no tests, correlations claimed from
  plots. The effects are large enough that this probably does not overturn anything,
  but "significantly more frequently" is doing unearned work.
- **Prompted-only vs. finetuned models are mixed in the narrative.** The strongest
  claims (no generalisation after exhaustive training, no grokking) rest on GPT3
  alone.

## How it could serve a harness-design effort

Stemming the discussion rather than resolving it — this paper constrains a
decomposition harness in several directions at once, and some of them pull against
each other.

**It sets a ceiling on what decomposition-by-instruction can buy.** The
question-scratchpad results are the uncomfortable ones for any harness whose theory of
improvement is "give the model the steps". Here the model was given a perfect
topological linearisation of the correct computation graph, for every training
instance, and still failed the moment the graph got deeper or wider. Whatever a
decomposition harness is doing when it helps, this paper argues it is not teaching the
model to compose. A harness that merely *states* the decomposition inside one
generation inherits the depth limit. Whether a harness that *executes* the
decomposition across separate calls escapes it is precisely the question the paper
does not test — and it is worth being explicit that the paper's negative result is
about linearisation into a single autoregressive stream, which is not the only
implementation of decomposition.

**It gives a candidate stopping rule with a real basis.** "Chain only a few
compositional steps" is the paper's own first recommendation, and depth is the
variable it identifies. If a harness must choose a decomposition depth, this argues
for shallow-and-wide over deep-and-narrow *within a single generation* — but note the
paper penalises width too (Prop. 4.1, average parallelism vs. accuracy). Both axes
cost. That is an unresolved tension: the paper shows the sequential axis and the
parallel axis both accumulate error exponentially, so it does not straightforwardly
license "decompose into many parallel shallow pieces" either. What differs between
the two is the *combining* function `h_n`, which Prop. 4.1 assumes is estimated
perfectly — recombination is exactly what the proposition assumes away, and exactly
what a real harness has to implement. That gap is where a recombination step's cost
would show up, and this paper does not measure it.

**It makes error recovery, not error rate, the design target.** The `c/(c+ε)` ceiling
is the most actionable thing here for a harness. A harness that adds verification,
checking, or re-entry into a valid state after an invalid one is raising `c`; a
harness that just picks a better model is lowering `ε`. The proposition says the
former moves the asymptote and the latter does not. The authors' own third suggestion
— augment with planning modules and refinement methods — is precisely this, though
they offer it as a suggestion with no experiment attached. A harness-design effort
could treat `c` and `ε` as quantities to *measure* per step, which the paper flags as
possible and never does.

**It supplies an evaluation warning that applies to the harness's own telemetry.**
Restoration errors mean a decomposition harness scoring itself on final answers will
systematically overestimate how well its sub-steps are working, and will do so *more*
on tasks where input-output pairs are common in pretraining. Any claim that a
decomposition improved a result needs process-level checking to be believed. The
per-node taxonomy (fully correct / local / propagation / restoration) is directly
reusable as a harness instrumentation scheme, if the harness's steps can be aligned to
a reference graph.

**It offers a complexity metric a harness could compute in advance.** If a task can be
expressed as an algorithm over primitives, depth/width/average parallelism are
computable before any model call, and the paper shows they predict failure better than
surface size. A harness that decides *whether* to decompose could in principle use
such a measure as its trigger. The large caveat: the graph is not unique, depth
depends on chosen primitive granularity, and for open-ended natural-language tasks
there is no algorithm to draw a graph from at all. Every task here is synthetic,
deterministic, and has a unique verifiable answer.

### Major concerns about leaning on this paper

- **Domain distance.** Multiplication, logic grids, and a DP recursion are
  deterministic, symbolic, single-correct-answer tasks. Whether the depth limit binds
  the same way on tasks with tolerant evaluation, multiple acceptable answers, or
  natural-language sub-goals is untested — and the authors' own leniency suggestion
  implies they expect it *not* to bind equally.
- **Model vintage.** 2023 snapshots, prompted through an API at temperature 1. The
  qualitative claims may well survive; nothing about the specific curves should be
  quoted forward.
- **The theory does not distinguish architectures or harnesses.** Props 4.1/4.2
  constrain any composition of fallible steps. Read carelessly they indict
  decomposition harnesses as much as they indict monolithic generation — the harness's
  defence has to be that it raises `c`, and that is an empirical claim this paper does
  not test.
- **Single-linearisation caveat, from the authors.** They flag that other
  linearisations might perform differently. Since a decomposition harness *is* a
  choice of linearisation-and-execution strategy, this limitation sits directly on the
  question of interest and is unresolved.

## Five citations worth chasing next

1. **Nye et al., "Show Your Work: Scratchpads for Intermediate Computation with
   Language Models"** [55/56] — the origin of the scratchpad device this paper builds
   its entire linearisation apparatus on, and the position it is arguing is
   depth-limited.
2. **Zhou et al.** [86] — cited alongside Nye for teaching algorithmic reasoning by
   splitting tasks into intermediate steps; the direct precursor on decomposition as
   an intervention.
3. **Bogin, Gupta & Berant, "Unobserved local structures make compositional
   generalization hard"** (EMNLP 2022) [10] — the closest prior formulation of the
   subgraph-coverage idea, and the paper whose train-split-by-observed-patterns claim
   this work sharpens into isomorphic full-computation matching.
4. **Razeghi et al.** [64] — the training-term-frequency vs. test-performance
   correlation that the linearised-subgraph-matching analysis generalises from tokens
   to subgraphs; needed to judge how novel §3.2.2 actually is.
5. **Liu et al.** [45] — shallow transformers learn shortcuts leading to poor OOD
   generalisation; the mechanistic counterpart to this paper's behavioural shortcut
   claim, and the place to look for whether "collapsed compositionality" has an
   interpretability-level account.

*Runner-up:* **Diaconis & Freedman, "Iterated random functions"** [24] via §E.1 — the
mathematical literature the error-accumulation propositions sit in, where the usual
focus is the *contractive* regime in which errors stay controlled. Worth chasing
precisely to understand what a system would need to look like to land in that regime
instead.
