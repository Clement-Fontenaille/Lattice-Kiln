# The Expressive Power of Transformers with Chain of Thought

## Density

**Density: MEDIUM.** Nearly every page is load-bearing formal content with almost no padding, but it bears on the Subject only obliquely: it proves that the *number of intermediate steps* is a graded computational resource for a single transformer decoder, which is an argument about how much serial work a model can do — decomposition into sub-tasks is never modelled, and the paper's "steps" are token positions inside one forward-generation trace, not sub-objectives dispatched and recombined.

- **Authors.** William Merrill (New York University), Ashish Sabharwal (Allen Institute for AI).
- **Year.** 2023 (arXiv v1, Oct 2023); version read is v5, 11 Apr 2024.
- **Venue.** ICLR 2024 (peer-reviewed). arXiv:2310.07923 [cs.LG].
- **My keywords.** serial-compute budget; expressivity upper/lower bounds; decoding steps as a complexity resource; circuit complexity of transformers; recurrence-by-tokens; layer-norm hash; Turing machine simulation; log/linear/polynomial step regimes; conditional separation; scratchpad length.

## Approach

This is a pure theory paper: no experiments, no models run, no datasets. Prior
work in the same line (Merrill & Sabharwal 2023b) had shown that a log-precision
decoder-only transformer that answers *immediately* after reading its input can
only decide languages in uniform `TC^0` — a small circuit class — and therefore
cannot, under standard non-collapse conjectures, simulate arbitrary finite-state
automata (`NC^1`-complete), decide directed graph connectivity (`NL`-complete),
or solve linear equalities (`P`-complete). The diagnosis offered there is that
the transformer has no recurrence: depth is constant, so the number of serially
dependent computation stages does not grow with input length.

The paper asks whether letting the model emit intermediate tokens before
answering — chain of thought, scratchpad — repairs this, and if so by how much.
The move that makes the question tractable is to treat the *number* of
intermediate steps as a resource parameter, exactly the way time and space are
resource parameters in classical complexity. They define `CoT(t(n))` as the class
of languages recognised by some transformer allowed `t(n)` decoding steps on an
input of length `n`, and then sandwich that class between standard time and space
classes. The whole paper is the sandwich plus its consequences in three regimes:
`t(n) = Θ(log n)`, `t(n) = Θ(n)`, and `t(n)` polynomial.

The headline sandwich (Eq. 1) is:

    TIME(t(n))  ⊆  CoT(t(n))  ⊆  SPACE(t(n) + log n)
                             ⊆  TIME~(t(n)^2 + n^2)

where `TIME~` allows polylog slack. The left inclusion is the lower bound
(Theorem 2, via Corollary 2.1); the two right inclusions are the upper bounds
(Theorems 4 and 3). Theorem 1 is a warm-up lower bound for regular languages.

## Formal setting, assumptions, and what is proved

**The model.** A `p`-precision decoder-only transformer (Definition 1) with an
embedding function, per-layer/per-head similarity and value functions, an
activation block containing the feedforward network, and a linear output head.
Generation is the ordinary autoregressive loop, formalised as the `k`-step
extension of a next-token function `f: Σ* → Σ`: `f^0(x) = x`,
`f^{k+1}(x) = f^k(x) · f(f^k(x))`. Recognition means `f^{t(|x|)}(x)` ends in a
distinguished accept symbol `1`. Note what this means: *the intermediate tokens
are ordinary vocabulary tokens fed back as input*, and the model attends over
the whole prefix at every step. There is no external memory, no scratch buffer,
no second model.

**Precision.** Log precision: at most `c·log m` bits for `m` decoding steps,
hence `c·log(n + t(n))` overall. This is the standard choice in this literature
because it is exactly enough to represent a position index and a sum over
positions, and no more.

**Assumptions that only the lower bounds need** (the upper bounds hold with or
without them — an asymmetry the authors are explicit about):

1. *Saturated attention* — "averaging hard attention": within a head, scores are
   all `0` or all `1/v`. Uniform attention and hard attention are special cases.
   This is the usual idealisation for constructing algorithms in transformers.
2. *Strict causal masking* — position `i` attends to `1..i-1`, excluding itself.
   Slightly nonstandard. Required by Theorem 2; Theorem 1 goes through without it.
3. *Projected pre-norm* (Definition 4) — layer-norm applied to a linear
   projection of the sublayer input rather than to the whole input, so a sublayer
   can normalise a chosen *subset* of the residual stream. Proofs use the more
   convenient *multi-pre-norm* (Definition 5: `k` projections, each normed, then
   concatenated), justified by Proposition 1 (credited to David Chiang, personal
   communication): multi-pre-norm with `k` norms is simulable by `k+1` projected
   pre-norm layers. This is a real generalisation of what deployed transformers
   do, and the authors flag it as such, suggesting it might be worth adopting in
   practice.

**What is proved.**

- *Theorem 1 (regular languages).* For any regular language `L`, there is a
  projected pre-norm decoder with strict causal saturated attention that decides
  `x ∈ L` in `|x| + 1` decoding steps, with or without positional encodings.
- *Theorem 2 (Turing machine simulation).* For a TM `M` running in `t(n)` steps
  (at most polynomial), there is such a transformer that on `$x` takes `t(n)`
  decoding steps and then `|M(x)|` further steps to emit `M(x)`.
- *Corollary 2.1.* `TIME(t(n)) ⊆ CoT(t(n))`.
- *Theorem 3.* `CoT(t(n)) ⊆ TIME~(n^2 + t(n)^2)`.
- *Theorem 4.* `CoT(t(n)) ⊆ SPACE(t(n) + log n)`.
- Supporting lemmas: Lemmas 1–2 (layer-norm hash scale invariance and
  equality-check), Lemmas 3–5 (input-tape retrieval), Lemmas 6–7 (rightmost-write
  retrieval), Lemmas 8–10 (the tie-breaking term), Proposition 1, Definitions 6–7.

**The classes that fall out.** Log steps: `CoT(O(log n)) ⊆ L`. Linear steps:
contained in `SPACE(n)` hence within the context-sensitive languages (Kuroda
1964), and in `TIME~(n^2)`; and it contains all regular languages by Theorem 1,
so linear-step decoders sit strictly between `Reg` and `CSL` in the Chomsky
hierarchy. Polynomial steps: `CoT(poly) = P` exactly — described as the first
exact characterisation of a class of transformers in terms of a standard
complexity class.

## Author incentive

Merrill is a PhD student at NYU (supported by NSF Award 1922658, an NSF Graduate
Research Fellowship, and AI2); Sabharwal is at the Allen Institute for AI. No
company product is being sold and no system is being promoted — there is nothing
here to benchmark against a competitor. The visible stake is intellectual
continuity: this paper extends the authors' own `TC^0` and `FO(M)` upper-bound
results (Merrill & Sabharwal 2023a, 2023b; Merrill et al. 2022) and is heavily
self-cited, which is normal for a research programme but does mean the framing —
"transformers lack recurrence, and here is the resource that buys it back" —
inherits its premises from their earlier work rather than testing them. A mild
secondary stake: the paper proposes the *layer-norm hash* as a reusable
construction and says so explicitly ("we believe [it] could be broadly useful for
building algorithms in transformers"), and it suggests projected pre-norm might be
worth adopting architecturally. Both are bids for a technique to be picked up.
The acknowledgements credit David Chiang with catching a mismatch between an
earlier version's transformer definition and standard pre-norm — the paper was
corrected under scrutiny, which is a point in its favour, and is why the
architectural assumption is stated as carefully as it is.

## Methodology — proof technique, where the assumptions bite

**Dependent variable.** There is no measurement in the empirical sense: the
quantity being related is the language class `CoT(t(n))`, and the independent
variable is the step budget `t(n)`. No N, no significance testing, no dataset.
The analogue of "controlling" is the architectural assumption list, and the
analogue of an error bar is the gap between the lower and upper bound.

**Lower bounds — technique.** The engine is the *layer-norm hash* (Definition 3):
`φ(x,y) = layer_norm(x, y, -x, -y)`, a unit vector in `R^4`. Two properties do
all the work. Lemma 1 (scale invariance): `φ(x/i, 1/i) = φ(x,1) = φ_x`, i.e. the
`1/i` denominator that uniform attention inevitably introduces cancels out.
Lemma 2 (equality check): `φ_q · φ_k = 1` iff `q = k`, and the inner product of
unit vectors is maximised at 1, so hard attention with these as query and key
retrieves exactly the positions where two *numeric* values agree, even when those
values were computed at different positions with different denominators. This is
the crux: standard one-hot exact-match retrieval works for finite symbol sets but
not for counts produced by uniform attention, and the hash repairs that.

Theorem 1 then simulates a DFA by an induction on decoding steps: at step
`i ≥ n`, output `q_{i-n} = δ(q_{i-n-1}, σ_{i-n})`. The previous state is simply
the current column's input token (that is the whole trick — the emitted token
*is* the recurrent state). The current input symbol is retrieved by the hash: the
model computes `1/i` and `1/(i-n)` by uniform attention over the strict left
context, builds two hashes `φ(1/i, 1)` and `φ(1/(i-n), 1)`, selects between them
with a ReLU gate on a flag `d_i` marking whether the token is a state symbol, and
attends. The transition function itself is a feedforward network — finite, so
trivially representable.

Theorem 2 scales this to a Turing machine, one TM step per decoding step. The
difficulty is representing an unbounded tape in a sequence of state vectors. The
solution is to store *diffs*, not tape contents: each emitted token `δ_j` encodes
the state entered, symbols written, and head moves for that step, and tape
contents at the current head position are reconstructed on demand. Head positions
are recovered by attending with value = move direction, which yields `h^τ_{i-1}/i`
(strict causal masking is what makes it `i-1` rather than `i`, hence why it is
required); both `(h ± 1)/i` are written to the residual stream and a linear layer
selects on the move encoded in the current input token. Input-tape reads use the
hash to match `h^0_i` against position index `i` (Lemmas 3–4), with Lemma 5
supplying the backward direction via monotonicity of the hash's first coordinate:
if the query strictly exceeds all keys, the query hash cannot equal their average,
so out-of-range head positions are detectable and read as blank. Work-tape reads
need the *most recent* write to that cell, so the head must retrieve the rightmost
matching `j`; this is a *tie-break*, and Appendix E builds one. Lemma 8 bounds the
hash similarity for a near-miss: `φ(i,1)·φ(i-1,1) ≤ 1 - 1/(2i^4)`. So a
monotonically decreasing tie-breaking term smaller than `1/(2i^4)` can be added to
the score without disturbing exact matches. Definition 6 constructs one by finite
differencing of `1/i` — `f(i,k+1) = f(i-1,k) - f(i,k)` — which Lemma 9 evaluates
in closed form as `k!/∏_{j=0}^{k}(i-j)`, and which is a linear combination of
`1/i, …, 1/(i-k)` and therefore computable in a *single* multihead layer (head `h`
attends past the first `h` tokens to compute `1/(i-h)`). Lemma 10 verifies
`f(i) < 1/(2i^4)` for the concrete choice `f(i,3)/100` (with a hardcoded patch for
`i ≤ 4`). This appendix is where the construction is genuinely delicate, and it is
also where it looks most like an artefact of exact arithmetic.

**Upper bounds — technique.** Both are straightforward simulations, and notably
*do not* need saturated attention, strict masking, or projected pre-norm.
Theorem 3: a multitape TM keeps key and value tapes, and for each of the `n+t(n)`
forward passes loops over `n+t(n)` key-value pairs, so `O(n^2 + t(n)^2)` inner
loops, each of which is add/multiply on `O(log n)`-bit numbers, hence polylog —
giving `TIME~(n^2 + t(n)^2)`. Theorem 4: since a single forward pass is in uniform
`TC^0 ⊆ L`, it can be replayed in `O(log(n+t(n)))` space, and the only thing that
must persist across steps is the buffer of generated tokens, of size `O(t(n))`;
memory is cleared between passes. Hence `SPACE(t(n) + log n)`. The elegance is
that the CoT buffer is *the entire memory cost* — everything else is recomputed.

**Where the assumptions bite.**

- *Saturated attention* is doing heavy lifting: the hash retrieval argument is an
  argmax argument, and it needs attention to concentrate exactly on maximisers.
  Real softmax attention approximates this, and the tie-break margin of `1/(2i^4)`
  shrinks polynomially in position — with log precision this is representable by
  construction, but it is a thin margin.
- *Log precision* is a two-edged assumption: it is what makes the `TC^0` upper
  bound on one forward pass true (hence Theorem 4), and it is enough to represent
  `1/i` and the hash, so it does not obstruct the lower bounds.
- *Projected/multi pre-norm* is the assumption most distant from deployed
  architectures. Without it, the constructions as written do not go through, and
  the paper does not claim otherwise. It is a genuine gap between the theorem and
  a GPT-style model, honestly flagged.
- *Strict causal masking* is required only by Theorem 2 and is mildly nonstandard.
- *Positional encodings* are notably **not** required — the constructions compute
  `1/i` from uniform attention over the left context with a `$` indicator, and
  Footnote 8 notes even the `$` is dispensable if a token can compute
  `1[j = 0]`.

**Theorem vs conjecture.** The inclusions themselves (Theorems 1–4, Cor. 2.1) are
unconditional theorems about this formal model. Every *separation* claim, i.e.
every statement that CoT genuinely adds power or that some regime cannot do
something, is conditional on standard complexity conjectures which are open:
`TC^0 ≠ NC^1` for "linear steps beat zero steps"; `L ≠ NL` and `L ≠ P` for "log
steps still cannot do connectivity or Horn-SAT"; and, for "linear steps cannot do
all context-free languages", the considerably weaker-supported assumption that CFL
recognition requires `ω̃(n^2)` time (best known algorithms are `O(n^ω)`, best
lower bounds sub-quadratic — so this one is a genuine open assumption, not a
folklore-safe one). The paper is scrupulous about marking these in footnotes. Also
explicitly *not* proved: any strict separation between log and linear steps — the
authors state finding one as future work — and the `Θ(log n)` regime has **no
concrete problem** exhibited where it helps.

## Key findings

1. **Intermediate generation does extend expressive power, and the amount of
   extension is a function of the number of steps.** This is the paper's thesis
   in one line. `CoT(t(n))` is bracketed by `TIME(t(n))` below and
   `SPACE(t(n)+log n)` / `TIME~(t(n)^2+n^2)` above, so the step count behaves
   like a classical resource.

2. **A transformer decoder can simulate `t` Turing-machine steps with `t`
   decoding steps** (Theorem 2 / Cor. 2.1), with no external memory and no
   nonstandard positional encodings — improving on Schuurmans (2023), who
   assumed external memory, and Pérez et al. (2021), who assumed an
   encoder-decoder with positional encodings containing `i`, `1/i`, `1/i^2`
   (problematic since layer-norm precludes representing unbounded `i`).

3. **Linear steps buy recurrence, and that is a strict gain** (conditional on
   `TC^0 ≠ NC^1`): all regular languages become recognisable (Theorem 1), as does
   anything a TM does in `O(n)` time — e.g. real-time counter machines. Zero-step
   transformers provably cannot do this.

4. **Logarithmic steps buy almost nothing identifiable.** The upper bound moves
   only from `TC^0` to `L`. Log-step decoders still cannot do `NL`- or
   `P`-complete problems (directed connectivity, Horn-SAT, linear equalities)
   under standard assumptions. They *might* gain `L`-complete problems, but the
   paper exhibits no concrete problem for which log steps help.

5. **Linear steps are bounded above by context-sensitive.** `SPACE(n)` sits
   inside CSL (Kuroda 1964), so a linear-CoT decoder lands strictly between `Reg`
   and `CSL` in the Chomsky hierarchy. It cannot recognise all context-free
   languages unless CFL parsing is possible in soft quadratic time.

6. **Quadratic steps reach directed graph connectivity** via DFS — `O(n)` on a
   random-access TM, `O(n^2)` without random access — a problem provably outside
   zero-step transformers. The authors note results from Zhang et al. (2023) hint
   fewer steps may suffice.

7. **Polynomial steps characterise `P` exactly.** `CoT(poly) = P`. Presented as
   the first exact equivalence between a transformer class and a standard
   complexity class.

8. **The bounds are near-tight.** Improving the space upper bound or the time
   lower bound by more than a `log t(n)` factor would constitute a fundamental
   complexity-theoretic advance (Hopcroft, Paul & Valiant 1977). The tightest
   achievable space bound would be `SPACE(t(n)/log t(n))`; the lower bound could
   at best be tightened to `TIME(t(n) log t(n))`.

9. **The layer-norm hash**, offered as a reusable primitive: exact-match retrieval
   over *numeric* values across columns, immune to the `1/i` denominators that
   uniform attention produces. Implementable with RMS-norm since the construction
   has mean zero by design. Yao et al. (2021) used a related idea more ad hoc.

**The authors' own reading.** They are notably restrained. Their summary is that
"a logarithmic chain does not add much, while a linear chain affords more power on
inherently sequential reasoning problems," and that "it appears that a linear
number of intermediate decoding steps may be required to overcome the limitations
of transformers on many sequential reasoning problems of interest." The mechanism
they name is recurrence: "the core challenge in simulating an automaton is
recurrence, which cannot be done without decoding steps. A linear number of
decoding steps allows simulating recurrence, which is where the additional power
comes from." On the polynomial result they immediately deflate the practical
reading: polynomial steps "turn transformers into strong reasoners, though running
a polynomial number of forward passes with a large transformer is likely
intractable in practice." And they draw the expressivity/learnability line
themselves — see below. They also read their own upper bounds as the more
practically forceful half: upper bounds "directly reveal limitations on what
transformers with intermediate generation can learn," whereas lower bounds only
say a parameterisation exists.

## Open questions the paper itself raises

- **Log vs linear separation is unproven.** They want "a strict separation between
  transformers with a log and a linear number of decoding steps," and note some
  problems currently needing a quadratic bound might be solvable in roughly
  linear steps (directed connectivity is the named candidate).
- **Expressivity is not learnability.** Stated plainly in the conclusion: the
  lower bounds "do not directly imply transformers can learn to use intermediate
  steps effectively." They propose a learning-theoretic treatment, gesturing at
  Malach (2023), and ask how fine-tuning regimes — reinforcement learning
  specifically — might let models actually exploit the power CoT makes available.
- **Should generalised pre-norm be adopted in practice?** "The critical role
  projected pre-norm or multi-pre-norm play in Theorems 1 and 2 suggest it could
  be interesting to investigate incorporating these generalized pre-norms into
  transformers in practice." An open architectural question raised by the proof's
  own needs.
- **Is the layer-norm hash broadly useful?** Offered as a conjecture about
  technique rather than a result.
- **Regions of the map are not known to be non-empty.** Figure 1's caption admits
  that some regions with area in the plot may be empty — the map is not tight.

## Appreciation

### What transfers as MECHANISM

- **Serial steps are a resource with a graded price.** The single most portable
  idea here is that "how many intermediate steps" is not a stylistic knob but a
  computational-resource axis, and that expressive power is *monotone and
  sensitive* along it. That framing survives the paper's specific model.
- **The emitted token is the recurrent state.** Theorem 1's construction makes
  the mechanism unusually legible: a constant-depth architecture gains
  unbounded serial depth only by writing state into its own output stream and
  reading it back. Anything that is a fixed-depth function of the input cannot
  do work whose depth grows with the input; putting intermediate results into
  the token stream is what converts parallel width into serial depth. This is a
  mechanism claim and it transfers.
- **The asymmetry between what buys power and what does not.** A budget too
  small to represent the problem's serial structure buys essentially nothing —
  the log regime has no exhibited win at all. That "there can be a step budget
  which is more than zero and still worthless" is a mechanism-level warning.
- **Upper bounds transfer more forcefully than lower bounds.** The authors say
  this themselves and they are right. The lower bounds show *some*
  parameterisation exists; the upper bounds constrain *every* parameterisation,
  including trained ones. When reading this paper for practical bearing, the
  ceiling results (`log ⇒ L`, `linear ⇒ CSL`) are the durable half.
- **State can be represented by diffs plus on-demand reconstruction.** The
  Theorem 2 tape encoding — write what changed, reconstruct the current value by
  retrieving the most recent matching write — is a genuinely general idea about
  how a sequence of appended records can stand in for mutable memory.

### What is MAGNITUDE, valid only inside this setup

- **Every specific step count.** "Linear", "quadratic for connectivity",
  "`|x|+1` steps for a DFA" are counts for a hand-constructed optimal
  parameterisation of an idealised transformer with saturated attention and
  projected pre-norm. They are not predictions about how many chain-of-thought
  tokens any real model needs, and the paper never claims they are.
- **`CoT(poly) = P`.** Mathematically the cleanest result in the paper and
  practically the least actionable — the authors say so. It bounds a limit
  object, not a system anyone will run.
- **The tie-breaking margin `1/(2i^4)` and the constants in Definition 7**
  (`ε = 10^-10`, division by 100, the hardcoded `i ≤ 4` case) are artefacts of
  making an exact-arithmetic argument close. Nothing about them should be read
  as a statement about numerical behaviour in trained models.
- **The `Reg`-to-`CSL` placement of linear-step decoders** is a statement about
  worst-case language recognition, not about the difficulty distribution of any
  task anyone cares about.
- **The architectural assumptions are load-bearing for the good news only.** The
  positive results require projected pre-norm — which deployed transformers do
  not have — and saturated attention, which they do not have either. So "linear
  CoT recognises all regular languages" is a statement about a model adjacent to,
  but not identical with, the ones in use. The negative results carry over
  cleanly; the positive ones carry over with an asterisk.
- **All separations are conditional.** If `TC^0 = NC^1` the headline "CoT adds
  power" claim collapses. Nobody expects that, but the claim is a conjecture-laden
  one and should be quoted as such.

### Bearing on the Subject (task decomposition)

Read strictly, this paper is **not about task decomposition**. Nothing here
splits an objective into sub-objectives, dispatches them separately, or
recombines them. There is one model, one context, one autoregressive stream; the
"steps" are token positions, and every step attends over the entire prefix. If
anything, the construction is the opposite of decomposition — it depends on total
prefix visibility, which is exactly what a sub-agent with its own context window
does not have.

Where it does bear, it bears on one axis of the Subject: **how-deep**. The paper
provides the closest thing in this literature to a principled answer to "what
sets the depth", and the answer is that depth should track the *serial* structure
of the problem, because serial steps are the resource that fixed-depth
computation lacks. The corollaries worth carrying forward, stated as questions
rather than conclusions:

- If the binding constraint on a hard task is serial depth, then adding *serial*
  stages helps and adding *parallel* width does not. That distinction is
  invisible in most decomposition taxonomies, which count sub-tasks without
  asking whether they are serially dependent.
- A step budget can be non-trivially positive and still buy nothing. The log
  regime is the formal instance. Whether there is a practical analogue — a
  decomposition depth that costs coordination but adds no capability — is a
  question this paper poses without answering.
- The paper's cost model is *only* step count. Coordination cost, recombination
  cost, and context-window cost — the costs the Subject names as contested — are
  entirely absent, and the model's assumption of full prefix visibility means the
  paper cannot see them by construction.

## How it could serve a harness-design effort — limitations, concerns

**What it can be used for.** As a floor argument, not a design. It gives a
defensible reason to believe that *some* problems cannot be answered in one shot
by a fixed-depth model no matter how large, and that the fix is serial
intermediate generation. If a harness is being argued about, this paper is the
citation for "immediate answering is provably weaker", and it makes the
distinction between serial and parallel elaboration a first-class one. It also
supplies vocabulary — step budget as a resource — that is more precise than
"reasoning effort".

**Where it stops.** Four limits, stemmed rather than resolved:

1. *Expressivity ≠ learnability ≠ elicitation.* The paper's own headline caveat.
   Every lower bound is an existence claim about weights. A harness cannot cash
   an existence claim: it must elicit behaviour from a model that was trained,
   not constructed. The gap between "a transformer exists that does this in `n`
   steps" and "this model will do it if prompted this way" is the entire domain
   the harness lives in, and the paper explicitly does not enter it.
2. *One context, no sub-agents.* The constructions require attending over the
   full prefix. A harness that splits work across calls with separate contexts is
   in a different formal setting, and the paper's results do not transfer to it
   without argument. Whether splitting *costs* expressive power — since each
   sub-call sees less — is a question this paper's framework could in principle
   be extended to ask, and does not ask.
3. *Worst-case, adversarial, asymptotic.* Language recognition over all inputs of
   length `n`, as `n → ∞`. Real tasks are neither worst-case nor asymptotic. Any
   inference from `CoT(Θ(n)) ⊆ CSL` to "this harness will fail on this task" is
   an inference the paper does not license.
4. *Architectural assumptions favour the good news.* As above: the positive
   results need projected pre-norm and saturated attention. A harness designer
   should treat the ceilings as robust and the floors as conditional on an
   architecture slightly unlike the one being harnessed.

**The concern I would flag most.** It is easy to over-read this paper into "more
steps is more power, so make the harness deeper." The paper does not say that.
It says power is *bounded by* the step budget, and demonstrates one regime (log)
where the budget is positive and the gain is unidentified. The direction of the
result is a ceiling, not a recipe — and no result here says anything about what
happens when steps are spent badly, which is the failure mode a real harness
actually faces.

## Five citations worth chasing next

1. **Merrill & Sabharwal (2023b), "The parallelism tradeoff: Limitations of
   log-precision transformers", TACL 11:531–545.** The `TC^0` upper bound this
   entire paper is built against. Everything here is a delta on that result;
   without it the separations have no baseline.
2. **Feng et al. (2023), "Towards revealing the mystery behind chain of thought:
   A theoretical perspective", NeurIPS.** The prior theoretical CoT result — a
   specific modular arithmetic problem CoT unlocks. The named precedent this
   paper generalises, and the natural comparison for how a concrete problem maps
   onto a step budget.
3. **Dziri et al. (2023), "Faith and fate: Limits of transformers on
   compositionality", NeurIPS.** The empirical counterpart: GPT-4's reasoning
   performance negatively correlating with the depth of the problem's computation
   graph. This is the bridge from the formal depth story to observed behaviour,
   and the closest thing cited here to evidence about real decomposition.
4. **Pérez, Barceló & Marinkovic (2021), "Attention is Turing complete", JMLR
   22(1).** The predecessor Turing-completeness construction, whose assumptions
   (encoder-decoder, positional encodings containing `i`, `1/i`, `1/i^2`, no
   layer-norm) this paper explicitly removes. Reading both shows exactly which
   assumptions in this genre are load-bearing versus convenient.
5. **Strobl, Merrill, Weiss, Chiang & Angluin (2024), "Transformers as
   recognizers of formal languages: A survey on expressivity", TACL.** The survey
   that situates this whole programme — the efficient way to find out which
   results in the area are robust across formalisations and which are artefacts of
   one author group's model choices.

*(Runner-up worth noting: Malach (2023), "Auto-regressive next-token predictors
are universal learners" — the paper's own pointer for the learnability question it
declines to answer, and the most relevant lead for anyone who cares about the
expressivity/elicitation gap.)*
