# Cross-paper discussion — findings

*The collect phase produced eight review sheets (`01`–`08`). This file is where
they are taken up against each other, and against the project's own questions,
finding by finding. Nothing here is settled. Entries are of three kinds. A
**finding** is a conclusion that carries forward — something the project will act
on — whether it comes straight from cross-examining the sheets or is a
methodological consequence the sheets' own evidence does not directly establish. A
**qualifier** carries nothing on its own; it only bounds how far a sheet or a
finding can be taken. A **candidate argument** is a project-originated hypothesis
parked here to be tested against the literature in a later pass.*

## Findings

### F1 — Decomposition buys two things, and only one of them decays with model capability

Sheet `07` (Madhwal et al.) shows that a correct, hand-verified decomposition is
worth roughly +25 accuracy points at 8B–72B and flattens to slightly negative at
frontier scale, with the stated mechanism that a capable model has internalised
the reasoning chains, so the external scaffold becomes first redundant and then
interfering. Sheet `08` (Wu et al.) reports the same directional shape from the
chain-of-thought-length side: the optimal number of steps falls as capability
rises.

The distinction this forces:

- **Accuracy lift** from decomposition decays as the base model improves, and can
  invert. A design that leans on decomposition *to be more correct* is leaning on
  a gap that is closing.
- **Working-memory and context discipline** do not decay. A larger, better model
  still has a finite context window, still accumulates state across a long task,
  and still benefits from each sub-call carrying a bounded working set. This is
  the value [[A1]] is about.

Consequence for the project: if decomposition is used for context management
rather than for accuracy, the frontier-capability trend is much less threatening.
That has to be a deliberate, recorded design choice rather than an unexamined
assumption, because a decomposition built for the accuracy reason and one built
for the context reason are not necessarily the same shape, and the first one has
an expiry date.

Scope: the capability-decay evidence is from closed-book factual multi-hop QA
(sheet `07`) and from math and logic reasoning (sheet `08`). Whether the same
decay shape holds for task families where sub-tasks differ qualitatively from the
parent — long-horizon work, tool use, code, tasks that exceed a context window —
is untested. Topic 15 is where that trend gets assessed properly. Sheet `08`'s
contribution here is further limited by [[F5]]: it measures chain-of-thought
length, not new-prompt-per-step decomposition, so it corroborates the direction
only by analogy.

Sheet `04` (Liu et al.) corroborates the base fact — decomposition buys accuracy
over a direct call (IO 48.6 → ~69 averaged across five benchmarks) and the
winning shape is task-conditional — but it runs on one base model, so it neither
supports nor contradicts the capability-decay direction.

### F2 — Correct decomposition carries a "shortcut tax," and its size at constrained scale is unmeasured

Sheet `07` (Madhwal et al.) classifies its cross-regime disagreements into
Helped (Direct wrong, decomposed right), Hurt (Direct right, decomposed wrong),
and Both-wrong. For the two frontier models the split is roughly 16 / 16 / 67
percent of the inconsistent cases. The stated mechanism for the Hurt bucket is
the *shortcut hypothesis*: the Direct answer was right because the model
pattern-matched the question to an answer without holding the intermediate
facts, and forcing execution of the verified plan exposes that gap and produces
a wrong answer.

The mechanism is not in principle capability-specific — a weaker model also
answers some questions by shortcut — but the paper reports the Helped / Hurt /
Both breakdown *only for the frontier models*. For the sub-70B models it reports
only net accuracy deltas of about +25, with no bucket decomposition and no
matched-question analysis of what a weaker model did on the items where
decomposition hurt a stronger one.

So the net lift at constrained scale is an average over a helped set and a hurt
set of unknown relative sizes. Decomposition may carry a subtractive component
at every capability level; this paper establishes the mechanism and its frontier
magnitude, not its magnitude where the project operates.

Consequence for [[A1]]: a fresh-context decomposition design inherits this tax on
exactly the question class where a monolithic call would have shortcut to the
right answer. Whether the working-memory benefit is worth a measurable accuracy
cost on that subset is the open question, and this paper gives the mechanism but
not the magnitude at constrained scale.

What would close the gap: a Helped / Hurt / Both breakdown at 8B–70B, and a
matched-question comparison of what weaker models do on the frontier Hurt items.

Scope: closed-book factual multi-hop QA, where the shortcut being exposed is that
"the parent question is more trained-on than its parts." For task families where
decomposition genuinely lowers difficulty rather than relocating a knowledge
lookup, the mechanism may not apply.

### F3 — Sheets 07 and 08 bracket the fresh-context question without resolving it

Sheet `07` (Madhwal et al.) runs a step-wise regime in which each hop is issued in
a fresh context holding only the substituted sub-question — no parent question, no
sibling answers. That regime underperforms the full-context regime at frontier
scale. It is empirical evidence, in a closed-book QA setting with no
context-budget pressure, that stripping context from a sub-call costs accuracy.

Sheet `08` (Wu et al.) derives its benefit term — sub-answers get easier as the
chain is split more finely — under a model in which every step conditions on the
full accumulating history of prior steps. An isolated sub-agent call carries no
such history. The paper models neither the cost of dropping it nor the benefit,
and the sign is genuinely ambiguous: losing the history could make sub-answers
harder, which moves the optimum shallower, or it could shed an accumulating
burden the chain pays and a fresh call does not, which moves the optimum deeper
and makes the benefit larger than the chain shows.

So the two sheets bracket the question rather than answer it. Sheet `07` has
evidence that context-stripping hurt; sheet `08` has a mechanism whose benefit
term may be understated for a fresh-context design. Neither setting matches a
sensible fresh-context sub-call: `07` stripped everything and had no memory
pressure, `08` never modelled isolation at all.

What the [[A1]] pass must resolve: for the project's task families and its actual
context-budget pressure, does a fresh-context sub-call that passes down the goal
and a relevant summary — not a bare hop — land on the lost-disambiguating-context
side (`07`) or the shed-accumulating-history side (`08`).

### F4 — An observed-length-vs-accuracy curve carries a reverse-causation confound; the project must not repeat it

Not established by any sheet's own evidence, but it carries: a methodological
consequence of how sheet `08` measures its central curve. Sheet `08` plots
accuracy against chain length. Any
such curve, whichever the x-axis (tokens or steps), is exposed to a confound the
paper does not name: within a single problem, the attempts that came out long are
disproportionately the attempts where the model was already failing —
backtracking, restarting, second-guessing — so length and error share an upstream
cause. Part of any observed "longer is worse" is then "the model was lost, which
made the output both long and wrong," not "depth caused the error."

Sheet `08`'s within-question design (vary length for a fixed question) removes the
across-question version of this — long questions being harder questions — but not
the within-question version, which operates across attempts at the same question.
Its synthetic leg does avoid the trap: there, depth is *commanded* by a control
token, not read off the output. The exposed claim is the observational one.

Carry-forward for the project: when the project measures decomposition depth
against outcome in its own evaluation, depth must be *set* — assigned,
controlled, commanded — rather than *observed* after the fact. An observed-length
curve cannot support a causal claim about depth. This constrains how [[I1]] and
any depth-tuning evaluation are designed.

### F6 — What sheet 08 carries in practice is a prompt-writing guideline

Read as chain-of-thought management inside one generation (per [[F5]]), sheet `08`
yields a set of guidelines rather than a decomposition result:

- There is an interior optimum for how much step-by-step working to elicit. Both
  "answer directly" and "narrate every micro-step" lose accuracy, not only
  tokens. Maximal granularity is not a safe default.
- Dial the elicited working *down* as the base model gets stronger. Scaffolding
  tuned on a weak model actively hurts a strong one, and the penalty grows with
  capability, so this is not a set-once choice — it comes down on model upgrades.
- Dial it *up* for harder items. A fixed instruction across a task mix is wrong
  for most of the mix; conditioning on difficulty, or letting the model
  self-pace, beats one template.
- Prefer steps that each do a real chunk of work over many trivial ones.
  Tentative — synthetic and theory only — but the direction is "do not
  over-atomize."
- Padding is pure cost. Instructions or exemplars that produce restatement and
  hedging add length with none of the benefit.
- If several candidates are sampled: length-filtered voting (bin by length, keep
  the low-answer-entropy bins, vote within) is worth trying. One-dataset
  proof of concept, not adopt-on-sight.
- Do not assume RL lengthens reasoning. Outcome-reward fine-tuning tends to
  shorten chains as accuracy improves.

Applications: a static prompt or context template; a dynamic prompt-tuning
mechanism that adapts per request or per model (the capability and difficulty
directions are exactly its inputs); and prompting practice in general.

Scope: the directions transfer, the numbers do not, and the last three points are
proof-of-concept strength.

### F7 — Cost belongs in the dependent variable

Sheet `04` (Liu et al.) reports every result as a pair: the task metric and cost,
where cost is average tokens per instance and average API calls per instance.
Once cost sits on the same plot as accuracy, "decomposition helps" stops being a
claim and becomes a question of where on a performance–cost frontier to sit. The
measured spread is 1–20× on the same task, large enough that a design not
measuring it is working blind.

Carry-forward: the project measures cost alongside outcome for every decomposition
choice, never accuracy alone. Sheet `04`'s cost is token and call count; the
project's cost also includes peak context (the axis [[A1]] is about) and, for any
escalating loop, tail cost — sheet `04` measures only the mean, and its worst case
(K=3 escalations, each possibly multi-call) is unbounded.

### F8 — No dominant decomposition strategy; the winner is task-conditional

Sheet `04` compares six prompt-level decomposition strategies (IO, CoT, P&S,
ReAct, P&E, P&E-DAG) across four task families. None wins everywhere: math and
reasoning favour CoT and linear plan-execute, code favours the acting-interleaved
strategy, divergent writing and comprehension favour the DAG. The interaction
survives a metric change — from five heterogeneous objective scores to a single
0–10 judge scale on MT-bench — which is what makes it a mechanism-level result
rather than a benchmark artefact.

Caveats: the specific mapping (CoT→math, ReAct→code, DAG→divergent) is one model
(GPT-4o-mini) over six specific prompt implementations — their ReAct has no tools
or code execution, so "ReAct is best for code" is a claim about a toolless
reasoning-acting prompt. The *existence* of a strategy×task interaction is the
finding; the mapping is magnitude. Whether the conditioning itself shifts with
model capability is untested — single base model, which ties back to [[F1]].

### F9 — Decompose by nature of work before decomposing by size

An inference across sheets `04` and `08`, not a claim either paper makes.

Sheet `08`'s efficiency result holds only over work-conserving decompositions
where each step does homogeneous, subdividable work. Sheet `04`'s task-conditional
strategy selection ([[F8]]) needs a sub-task with a definite character — it cannot
pick one strategy for a piece that is half code and half prose. A raw high-level
task usually mixes heterogeneous work: some retrieval, some deduction, some
synthesis.

So the first cut should be by *kind of work*, not by size. Separating the
retrieval part from the reasoning part from the composition part yields sub-tasks
that are each internally homogeneous — and only then does "split into smaller
pieces of the same kind" enter sheet `08`'s efficient regime, and only then does
per-sub-task strategy selection have a well-defined answer.

What a pass would need to check: whether decomposing by nature of work actually
produces homogeneous sub-tasks in practice, and whether the predicted efficiency
gain shows up rather than being eaten by the extra coordination of a
mixed-strategy pipeline.

### F10 — Sheet 04's demonstrated value is cost, not accuracy

The paper frames S&D as "consistently on the Pareto frontier" and reports it
beating individual approaches. The accuracy margins carrying that claim (GSM8K
+0.39 over CoT, MATH +0.30 over P&E) are read off single-run appendix tables, are
smaller than the replicated error bars elsewhere in the paper, and get no
significance test. The cost differences are order-of-magnitude and survive.

So the defensible S&D result is that routing among decomposition strategies buys
large cost savings at roughly comparable accuracy. On the accuracy axis a
well-articulated fixed pairing — ReAct plus CoT, say — would plausibly look just
as good. Any use of this paper should carry the cost claim and drop the accuracy
claim.

### F11 — A verifier-gated cheap-first selector under-escalates for tasks that genuinely need structure

Sheet `04`'s selector ends up choosing implicit (cheap) approaches about 85% of
the time, and its escalation ladder's first fallback after a low-confidence answer
is *less* decomposition, not more. On Trivia Creative Writing — the one benchmark
where cheap and expensive approaches genuinely diverge — S&D systematically
under-buys structure and loses 5–8 points, and the failure analysis the paper
promises for that case is absent.

Carry-forward: a cheap-first, confidence-gated router has a characteristic failure
mode — it will not escalate enough for the minority of tasks that actually need
the expensive shape, because the same weak self-confidence signal that gates
escalation is unreliable exactly there. A design using this pattern needs a
second, independent trigger for "this task needs structure" that does not depend
on the verifier's confidence.

### F12 — Routing is a distinct cost from having the pool

Sheet `04`'s sharpest ablation: keep the same six approaches, the same escalation
ladder, and the same verifier, but randomise the *initial* choice instead of
selecting it. Token cost rises ~229% (roughly triples) and accuracy still falls.
Having the options is not the value; choosing well among them is, and choosing
badly is expensive because it drives the escalation loop.

Consequence for [[A1]]: a fresh-context decomposition design needs a router too,
and this sizes what a bad one costs — the working-memory benefit has to clear not
just the decomposition tax ([[F2]]) but the routing overhead as well.

### F13 — Recombination is a distinct, large, and largely unmeasured failure mode

Convergent across method, survey, and failure-analysis sheets. Sheet `09`
(compositionality gap): about a third of its questions are ones where the model
demonstrably holds both facts and still produces the wrong composed answer —
splitting and executing correctly does not deliver the answer. Sheet `11` (Chain
of Agents): a dedicated recombiner agent is worth 5–10 points, and feeding it
*more* material (all intermediate states rather than one) makes it *worse*
through conflict between them. Sheet `12` (MAS failures): the verification /
acceptance category is ~24% of failure instances and is "the residue no model
choice removes." Sheets `02` and `03` both name recombination the thinnest-covered
part of the field. Sheet `05` (ADaPT) treats its And/Or logic plus propagated
state as plumbing, which the reviewer flags as arguably a finding.

Consequence: a design that treats assembly as bookkeeping is budgeting for the
wrong thing. The join step needs its own architecture and its own error budget.
Magnitudes are all cohort-bound (sheet `09` is GPT-3-era); the *structure* — that
the residual after perfect sub-task execution is real and large — is what
transfers.

### F14 — A demarcated sub-task boundary is a generic interposition point

Sheet `09`: once a sub-question is a marked span rather than a phrase in a chain
of thought, anything can answer it — a tool, a cache, a different model, a human,
a verifier — with no prompt change, no finetuning, no query language. "Formatting
is doing the work that training used to do." Sheet `01`'s plan/execute split and
its "where a real solver exists, prefer it" is the same move at the execution
boundary. Sheet `03`'s LLM-Modulo pattern (generate approximate, external verifier
certifies, reprompt on failure) is its verifier instance.

Consequence: making sub-task boundaries explicit and machine-readable buys both
generalisation to inputs unlike the examples (sheet `09`'s untemplated-dataset
margin) and a substitution point for tools, verifiers, and routing. Caveats: sheet
`09` only ever substitutes at a leaf, one hop deep, never recursively; and
inserting a substituted answer "as if the model produced it," with no provenance
and no adjudication, is itself a failure mode.

### F15 — Structured intermediate output is a correctness property once composition is automated

Sheet `09`: 40% of chain-of-thought final answers on the untemplated set were
unusable as *outputs* despite sometimes containing the right answer, and were
scored wrong. Structure does two jobs — shaping the reasoning and making the
result machine-readable — and the second is not cosmetic once a later step
consumes the first. Sheet `12`'s handoff failures (state crossing an agent
boundary and not arriving usable) are the multi-agent version.

Caveat (sheet `09`'s own): formatting benefits are the first thing to evaporate
when models are trained to emit structure natively, so this is a property to
design for, not a permanent source of advantage.

### F16 — Serial-versus-parallel is a first-class distinction that most decomposition taxonomies miss

Sheet `06`: if the binding constraint on a task is serial depth, adding serial
stages helps and adding parallel width does not — a distinction "invisible in most
decomposition taxonomies, which count sub-tasks without asking whether they are
serially dependent." A step budget can be positive yet worthless (the logarithmic
regime is the formal instance of over-decomposition that costs coordination and
adds no capability). Sheet `02`: the sequential / parallel / tree axis is really
"when commitment happens and whether it can be undone," and the shared word
"tree" hides two structurally different systems (path-finding, where children
compete and one path is the answer, versus HTN-style, where leaves are
complementary and all are combined). Sheet `11`: parallel-independent
partitioning loses to sequential state-passing when sub-results are
interdependent — often below the do-nothing baseline — because "communication is
the active ingredient."

Consequence: the split decision must ask whether the sub-tasks are serially
dependent, not only how many there are. Independent-parallel decomposition is
safe only when the sub-tasks are genuinely independent; where they are not, it
destroys the dependency the task needs.

### F17 — Self-evaluation is the load-bearing weakness of failure-triggered and verifier-gated decomposition

Sheet `05` (ADaPT): the entire recursion is gated on the executor's own "task
completed / task failed," which is inflated by more than 30 points where success
is graded rather than binary, and the failure is silent — the loop terminates
believing it succeeded. The reviewer's summary: "everything upstream of the
boolean is portable; the boolean is not." Sheet `12`: verifiers do superficial
work despite being prompted otherwise (compile checks, leftover-TODO scans); a
chess program passes review and is unplayable. Sheet `02`: a generator scoring
its own intermediate states carries self-preference bias, and a separate
evaluator removes only that bias — the mitigation is to delay aggressive pruning
until evidence accumulates. This is the same signal type as [[F11]]'s verifier
and [[F2]]'s shortcut self-report.

Consequence: any decomposition control loop gated on the model's own judgment of
its own output inherits this. The project needs an external signal — a test,
execution, a rule, an independent model — or must treat the self-report as
advisory, not as control flow. (The internal-readout version of this question is
its own review topic, not folded in here.)

### F18 — Planning and execution are separable capabilities that compress differently and want different model budgets

Sheet `10` (Divide-or-Conquer): the decomposer distils into a 7–13B student that
matches or beats its teacher and transfers across domains and solvers; the solver
does not — it collapses and does not generalise. Proposed mechanism: planning is
abstract and low-information-density, execution is knowledge-bound. Sheet `01`:
producing a plan is cheap and buys little on its own; the accuracy lives in
execution, and a deterministic tool does execution better than token generation.
Sheet `05` (ADaPT §6.4): planner and executor can be different models — an
expensive planner invoked rarely on failure plus a cheap executor doing the
volume. Sheet `03`: ADAPT's principle of choosing the decomposition strategy from
the executor's capability.

Consequences and caveats: (a) the "cheap planner is fine" reading cuts awkwardly —
sheet `10` shows the value of a better plan *declines* as the executor
strengthens (a frontier executor barely moves across three very different
decomposers), so the appeal of a specialist planner is strongest exactly in the
constrained-executor regime the project operates in; (b) sheet `10`'s asymmetry
may be partly positional — a strong solver sits between every plan defect and the
metric and absorbs it, while nothing absorbs a solver defect — not purely
intrinsic compressibility; (c) sheet `10` also finds that specialising a model
for planning *degrades* its solving by 15–22 points, so the two roles cannot be
collapsed back into one finetuned model — an argument for structural separation.

### F19 — Upfront versus feedback-revised decomposition is tied to an environmental property

Sheet `03`: "global" decomposition (whole plan up front) is suited to *fully
observable* environments; "iteration" decomposition is revised against feedback
during execution. This is sharper than "flat vs hierarchical" because it ties the
choice to whether the environment can be observed. Sheet `05` (ADaPT): rejects
long upfront plans in *unexplored* environments — a ten-step plan rests on
assumptions that cascade into error — and short plans are viable *because*
recursion can split again later. Sheet `10`: static (upfront) beats dynamic
(iterative), but only in a setting engineered to have no step dependence (QA where
each sub-question barely depends on the previous answer); the reviewer is explicit
this should not be carried into a setting with genuine step dependence.

Consequence: the upfront-versus-iterative choice should be made from whether the
environment is observable and whether sub-results feed each other — not by
default. Upfront plans are epistemically unsound wherever the planner cannot yet
know what it is committing to.

### F20 — Fixed upfront decomposition can convert a recoverable trajectory into an unrecoverable one

Sheet `05` (ADaPT), the most reusable negative result in that paper:
Plan-and-Execute does not merely fail to help — it commits to a step the executor
cannot perform and leaves no path back, scoring *below* plain iterative execution
on one benchmark (17.0 vs 32.0). Sheet `11`: the chain is a single point of
failure with no redundancy — a worker that drops a fact several hops from the end
has silently destroyed it — and the paper argues *against* the redundancy that
would catch it. Sheet `12`: conversation-history loss and conversation reset are
named failure modes.

Consequence: a decomposition without a recovery path — re-plan, backtrack,
cross-check — inherits brittleness that grows with depth. Direct bearing on
[[A1]]: fresh-context sub-calls with a summarised handoff are exactly the
low-redundancy shape sheet `11` warns about, so the A1 pass must weigh whether
the design needs a recovery path built in.

### F21 — Depth used should be an outcome, and the gap between budget and realized depth is diagnostic

Sheet `05` (ADaPT): the realized maximum depth (`k_max`) rises 1.9 → 2.8 tracking
true task complexity, against a fixed budget (`d_max`), and the pair is a
ready-made runtime telemetry signal — how hard the task turned out to be, and how
close the run came to the ceiling. Sheet `06`: depth should track the *serial*
structure of the problem. Sheet `10`: a cap of three sub-questions beat two and
four — both over- and under-splitting cost accuracy, an interior optimum showing
up in an explicit-decomposition setting this time (compare [[F1]] / [[F6]]).

Consequence: a harness should carry a depth *budget* and observe a *realized*
depth, and instrument the gap. This is the complement to [[F4]]: you set the
budget, you measure what the run actually used.

### F22 — Coordination cost is nearly always asserted and nearly never measured

Sheet `11`: cost is treated analytically only (attention-FLOP asymptotics), with
no measured tokens, dollars, latency, or API calls anywhere, and the method is
strictly sequential so its latency cannot be parallelised away — "CoA is
cost-effective" needs the number supplied from elsewhere. Sheet `03`: no token,
latency, or dollar column in the whole survey. Sheet `02`: names cost a concern,
quantifies nothing. Sheet `12`: the only cost figure is the annotator's API bill;
"failure counts are not a cost model." Sheet `05` (ADaPT) reports average call
counts but never a worst case or a variance, and Or-branching can fan out.

Consequence: corroborates [[F7]] from the gap side — the field has a systematic
hole exactly where the project's premise (constrained working memory, entropy
reduction as the product) most needs data. The project has to measure this
itself, which is what [[I1]] is for. Tail cost specifically is never bounded:
average per-instance cost is reported, the fan-out / repeated-escalation worst
case is not.

### F23 — Weak executors need decomposition more and gain more from it — and the coordination tax also grows as the executor weakens

Sheet `10`: weaker solvers gain more from a better decomposer; a strong solver
can partly decompose for itself. Sheet `05` (ADaPT): a deliberately weak executor
goes from 3.3% to 41.7%, the largest relative move in the paper. Sheet `12`: a
weak open model's context-loss and conversation-reset counts are an order of
magnitude above a stronger open model's — "weak models fail at the handoff
specifically," so coordination overhead is not a fixed tax but scales with agent
weakness.

Consequence: for a project committed to constrained models, decomposition's
benefit is largest exactly in its regime — but so is the handoff-failure rate.
Both sides of the ledger grow as the model gets weaker. This is the
coordination-cost mirror of [[F1]]'s "accuracy lift decays with capability."

### Papers the gathered findings keep pointing at

Not read in full; flagged by two or more sheets as the load-bearing reference:

- **Faith and Fate** (Dziri et al., NeurIPS 2023) — cited by sheets `05` and `06`
  as the empirical bridge between the formal serial-depth story and observed
  behaviour ("performance decays with the depth of the computation graph";
  transformers do "linearised subgraph matching," not systematic composition).
- **Feng et al. 2023** (circuit-complexity account of why CoT works) — cited by
  sheets `06` and `10` as the theoretical grounding for why splitting the
  computation helps at all.

## Qualifiers

### F5 — Do not lend sheet 08's results to decomposition findings

Sheet `08` studies the length of a chain of thought inside one model generation.
In its real-model leg, "steps" are newline-separated lines, and how many there are
is induced by few-shot exemplars written at three step granularities — a
writing-style intervention, closer in kind to "proceed step by step" than to task
decomposition. Its synthetic leg gives a step real structural content (a control
token, a fixed operator budget per step) but still inside one context, one set of
weights, with no new prompt issued per step and no recombination stage. Its theory
assumes every step conditions on the full prior history.

Explicit task decomposition is a different operation: the orchestrator issues a
*new prompt* per sub-task, often in a fresh context, and a recombination step
follows. None of sheet `08`'s three legs models that. Its mechanism — compounding
per-step reliability against a saturating benefit — is stated abstractly enough to
invite the extrapolation, and the paper claims in one sentence that least-to-most
and divide-and-conquer "fall in our analysis," but it never tests an
explicit-decomposition scheme.

What this qualifier guards:

- [[F1]] leans on sheet `08` as a second, independent construction of the
  capability-decay direction. With this qualifier, sheet `08` corroborates
  "optimal *chain length* falls with capability" — adjacent to, not identical
  with, "decomposition lift falls with capability." The direction survives; the
  identification is by analogy.
- [[F2]] is derived from sheet `07`'s explicit regimes and does not depend on
  sheet `08`. The temptation this blocks is *stacking* sheet `08`'s
  "over-decomposition hurts" on top of F2 as if the two were one reinforcing
  result. They are about different things: F2 is knowledge exposure under a
  correct plan; sheet `08` is per-step error accumulation in one narrated chain.
- [[F6]] is already scoped to chain-of-thought management and needs no further
  guard.

## Candidate arguments (unassessed)

### A1 — Fresh-context decomposition as the space-reusing form of divide-and-conquer

**Provenance.** This argument arose in discussion while reading sheet `06`
(Merrill & Sabharwal, *The Expressive Power of Transformers with Chain of
Thought*), set beside the classical complexity result that divide-and-conquer can
trade time for space by solving sub-problems sequentially and reusing scratch
space between them — Savitch's theorem is the textbook instance. It was then
connected to the project's premise of operating under a fixed and modest context
budget. It is a project-originated hypothesis, not a claim extracted from any
reviewed paper.

**The claim.** If a task is solved by separate model calls, each given a fresh
context that holds only what that sub-call needs, and each sub-result is
compressed before it is carried forward, then the peak context any single call
has to hold is bounded by the largest individual sub-problem rather than by the
sum of the whole task's working material. The working set then tracks the depth
of the decomposition rather than its total size. For a system whose premise is
staying effective under a fixed context budget, this is a structural reason to
prefer decomposition over one long reasoning stream, and it is independent of any
accuracy argument.

**The price.** The approach pays in repeated calls and repeated prompt overhead,
which is the time-for-space side of the trade. It also pays in redundant work
whenever sub-problems share structure that a single pass would have computed once.

**The failure mode.** A sub-call that cannot see its siblings or the full parent
context can make a choice that is locally sound and globally wrong, and the
summary step can drop the information that would let a later stage catch the
error.

**What a pass needs to check.**

- Whether the Merrill & Sabharwal result actually licenses a claim about working
  memory, or only a claim about model size. Sheet `06` notes that their space
  bound *grows* with the step count rather than shrinking.
- Whether any reviewed paper treats peak working memory or context size as a
  dependent variable, rather than reporting only token counts or accuracy.
- Whether the recombination failure mode named above is the same one that sheets
  `01`, `03`, `04`, `07` and `08` each raise from their own angle, and if so what
  magnitude those papers put on it.
- Whether the literature contains competing arguments, for or against
  fresh-context decomposition, that did not originate with the project.
- The size of the shortcut tax from [[F2]] at 8B–70B scale — the accuracy cost
  this design pays on the question class a monolithic call would have shortcut,
  set against the working-memory benefit.
- Which side of [[F3]] a fresh-context sub-call lands on — lost disambiguating
  context, or shed accumulating-history burden — for the project's tasks.
- The routing overhead from [[F12]] — a fresh-context design needs a router, and a
  bad one roughly triples cost; the working-memory benefit must clear that too.
- Sheet `04`'s cost axis is token and call count, not peak working memory, so it
  bears on A1 only indirectly; its escalation ladder defaulting to *less*
  decomposition is another weak data point that over-decomposition is a real
  failure direction.

---

*Further candidate arguments are added here as they surface, then assessed in a
later pass.*
