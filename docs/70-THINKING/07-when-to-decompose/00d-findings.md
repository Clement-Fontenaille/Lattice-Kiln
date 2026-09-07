# Cross-paper discussion — findings

*The collect phase produced twenty review sheets (`01`–`20`), over five reading
rounds. This file is where they are taken up against each other, and against the
project's own questions, finding by finding. Nothing here is settled. Entries are of three kinds. A
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

### F21 — Depth used should be an outcome; and the granularity-vs-score curve has a single interior optimum in every setting it has been measured in

Sheet `05` (ADaPT): the realized maximum depth (`k_max`) rises 1.9 → 2.8 tracking
true task complexity, against a fixed budget (`d_max`), and the pair is a
ready-made runtime telemetry signal — how hard the task turned out to be, and how
close the run came to the ceiling. Sheet `06`: depth should track the *serial*
structure of the problem.

The interior optimum — too little granularity and too much both cost accuracy,
not only tokens — is now robust across three unrelated granularity axes:

- **Step granularity inside one stream** — sheets `08` (F1 / F6): both "answer
  directly" and "narrate every micro-step" lose accuracy.
- **Sub-question count in explicit decomposition** — sheet `10`: a cap of three
  beat two and four.
- **Chunk size in context-separated parallel D&C** — sheet `17`'s
  model-noise-dominated regime ([[F34]]): accuracy improves as chunks shrink,
  then degrades again once chunks are too small.

Three different mechanisms and settings, the same U-shape — a mechanism-level
regularity rather than a benchmark artefact.

Consequence: a harness should carry a granularity/depth *budget* and observe a
*realized* value, and instrument the gap — the complement to [[F4]] (you set the
budget, you measure what the run actually used). And because the curve is
single-optimum, locating the optimum is cheap: sheet `17` §5.5 samples 3–5
instances per candidate value rather than the whole dataset (cost `m·|C|`, not
`|D|·|C|`), with `m = 5` usually recovering the exhaustive optimum's score.
Proof-of-concept strength — one paper, and it degrades exactly where the curve is
flat near the top, i.e. noise the size of the effect.

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

### F24 — At depth, the lever is the error *recovery* rate, not the error rate

Sheet `13` (Faith and Fate), Prop. 4.2: accuracy at composition depth is governed
by `c / (c + ε)` — the ratio of per-step recovery rate to per-step error rate —
not by `ε` alone. Lowering `ε` (a better model) gives diminishing returns at
depth; raising `c` (error detection, correction, re-entry into a valid state
after leaving one) moves the ceiling itself. Sheet `14` (Cumulative Reasoning) is
the constructive instance of raising `c` — verification converts an accuracy
problem into a search problem, and `p1·p2` with retries beats a single shot at
`p` when each stage is independently checkable.

Consequence: a decomposition harness's whole defence against the compounding-error
indictment is that it raises `c`. That is an empirical claim, and no reviewed
paper tests it — sheet `13`'s propositions assume `ε` constant and per-step errors
independent, are never fitted to its own runs, and, being about any noisy
composition of fallible steps, indict decomposition harnesses as much as
monolithic generation *unless* the recovery is real. `c` and `ε` are quantities
the project could measure per step; sheet `13` flags this as possible and never
does it.

### F25 — Outcome-correct does not imply process-correct; a loop that reads only the final answer reads a biased signal

Sheet `13`: 82% of *correct* final answers on one multiplication setting sat atop
an incorrect computation graph. Sheet `16` (Decomposed Prompting): a headline
"+14/+17 reasoning gain" was largely a weak-baseline extraction artefact — "a
large reasoning gap can be an extraction gap." Sheet `09` (F15) is the
parseability version.

Consequence: any decomposition telemetry that scores itself on final answers
overestimates how well its sub-steps are working, and does so *more* on tasks
where input–output pairs are common in pretraining. Sheet `13`'s per-node
taxonomy — fully correct / local error / propagation error / restoration error —
is directly reusable as instrumentation if the harness's steps can be aligned to
a reference graph. Verification of the project's own decomposition claims has to
be process-level, not outcome-level.

### F26 — Producing a list of sub-tasks is cheap; producing the correct dependency structure over them is the expensive capability, and it fails first on weak models

Sheet `15` (TaskBench): models score 70–80 on node-F1 (right sub-tasks) while
scoring 3–13 on edge-F1 (right wiring, both endpoints exact) — the two dissociate,
and the dependency-structure half fails hardest on smaller models. The
withhold-edges ablation confirms the direction: dependency edges are what make a
task genuinely multi-step rather than a list of unrelated errands. Sheet `16`'s
abstraction-barrier result (a recursive procedure unrolled into one flat chain
fails) is the same point from the other side.

Consequence: this is the concrete, measurable version of [[F16]]. A harness should
not read "the model produced a plan with plausible steps" as evidence the plan is
executable; if it relies on the model to also state dependencies (for scheduling,
parallelism, argument threading), that is the part that breaks. Instrument: emit
the plan as `{nodes, edges}` and score node set and edge set separately against a
reference, without executing anything. Caveats: exact-endpoint matching penalises
correct-but-different plans, hardest on the decomposition metric; and TaskBench's
references are correct-by-construction, never checked for whether a different
valid decomposition exists (~12% error survives into the released data).

### F27 — The accept/reject port is a first-class object, and the reliability of what fills it is the whole question

Sheet `14` (Cumulative Reasoning): giving rejection authority to a *separate* call
— one that sees the candidate step and not the generator's momentum — carries the
method's entire measured advantage (the single ablation). The port is fungible:
the same socket takes an LLM verifier or a Python interpreter, and the symbolic
one is both cheaper and more reliable, which is where the paper's strongest
results come from. But the LLM verifier's reliability is never measured, the
theory simply assumes it near-perfect, and a wrong *accepted* step is worse than
a visible failure — it is a laundered failure that now carries an accept stamp and
gets reused by everything downstream (the DAG amplifies exactly this).

Consequence: sharpens [[F17]] into a design object. If the project builds a gate,
its contract needs deciding — does rejection carry a reason back to the proposer,
is it final or a revision request, who pays for the retry — and one bit is
impoverished. The accept/reject port is the right place to spend engineering
effort, and a symbolic filler beats an LLM one wherever correctness is locally
decidable.

### F28 — Provenance as a required output field gives you the dependency graph and invalidation for free

Sheet `14`: constraining each sub-result to declare what it was derived from (in
CR, one proposition from two named premises) means the dependency DAG is built by
construction rather than reconstructed, non-duplication is checkable, and a node
later found wrong has identifiable descendants. Cost: the split is only as
expressive as the step schema — a task whose natural sub-steps do not fit the
schema gets nothing.

Open question sheet `14` leaves, and the one that matters for [[A1]]: CR only ever
*adds* to the graph and never revisits an accepted node. What happens when a node
accepted early is discovered wrong later is unaddressed — the obvious next
question for anything that accumulates.

### F29 — Input-length recursion converts a competence question into a size question

Sheet `16` (Decomposed Prompting): recursion on *input length* — apply the same
task to smaller inputs, recombine, terminate at a base case chosen as the size
where the model is already reliable — is structurally distinct from recursion on
difficulty. The argument is structural, not empirical: as long as recombination is
cheap and the base case is reliable, accuracy stops being a function of input
length.

Direct support for [[A1]]: this is the space-reuse structure with a concrete
termination rule (the base case is a *reliability* threshold, not an arbitrary
depth cap), and A1's fresh-context-per-sub-call is the mechanism that keeps every
recursion level's working set down at base-case size.

### F30 — Modularity is a precondition for recursive decomposition, not an optimisation

Sheet `16`: the *same* recursive procedure written as one unrolled chain **fails**
where the modular version (decomposer + handlers + controller) succeeds — a linear
chain has no abstraction barrier, so a recursive procedure written into one must
inline every level. This is the sharpest reason [[F5]] holds: "state the
decomposition inside one stream" and "execute it across calls with a controller"
are different capabilities, and only the second supports recursion at all. Sheet
`13` is consistent — being *given* a perfect topological linearisation of the
correct graph did not lift the depth limit, because it was still one stream.

### F31 — A deterministic controller between planner and executor is a harness architecture; the handler-behind-an-interface is the substitution point

Sheet `16`: three roles, only two of them models — a decomposer that plans the
next step, a handler library that does the steps, and a **symbolic controller**
that owns the loop, holds the state (`#1`, `#2`, … addressable references), routes
each sub-question to the named handler, and stops on a sentinel. A handler
addressed by name and consuming a natural-language sub-question can be a prompt, a
nested decomposed program, a symbolic function, or a different (smaller) model —
swapped without touching the caller (demonstrated four ways). The named sub-task
tag doubles as a routing key and as a contract about what the call is for.

Consequence: extends [[F14]] (the boundary as an interposition point) and [[F18]]
(heterogeneous models by role) into a concrete template, and the controller being
deterministic is itself an answer to [[F17]] — the loop, the state, and the
termination decision are code, not model self-report.

### F32 — Sheets 10 and 16 disagree on whether the decomposer can be a small model

Sheet `10` (Divide-or-Conquer): the decomposer *distils* into a 7–13B student that
matches its teacher and transfers. Sheet `16` (Decomposed Prompting), footnote 8:
the decomposer *cannot* be a small model. The settings differ — sheet `10`'s
decomposer emits at most three sub-questions for a QA or math problem; sheet
`16`'s emits a routed prompting-program with addressable references and recursion
control over a handler library. Different jobs, plausibly a real capability
threshold between them.

What the [[A1]] / [[F18]] assessment must establish: which regime the project's
orchestrator sits in — a light "name the sub-goals" planner (small model may
suffice) or a "run the control program" planner (may need the capable model),
with direct cost consequences either way.

### F33 — What sheet 17 carries: any decomposition that keeps per-unit loss bounded beats a monolith at sufficient scale, and the scheme does not matter

Sheet `17` (Xu et al., *Noise Decomposition Framework*) builds an exact
telescoping identity `ρ_sys = ρ_task · ρ_agg · ρ_model` (fidelities multiply;
losses `ℒ = −log ρ` add) and a Proposition 3.1 that a chunk-and-aggregate
pipeline eventually beats a single long-context model. The demonstration holds —
a weak chunked pipeline matches or beats a strong single-shot model at 128K on
several tasks — and so does the direction of the conclusion. What the paper does
**not** deliver is why or where to act: the three factors are not separately
measurable (`ρ_task` and `ρ_agg` are ratios against uncomputable optima `a*`,
`h*`), no crossover length `T₀` is ever computed or tied to a measurable
quantity, and the proposition is purely existential and asymptotic.

The transferable content, stated without the unmeasurable apparatus: **if a
decomposition's total loss grows linearly in problem size — bounded, roughly
constant per-unit loss — then past some input length it outperforms a monolithic
call whose loss grows faster.** This is scheme-agnostic. It does not privilege
chunk-and-aggregate; any decomposition that exposes the same linear error bound
qualifies. The bounded-per-unit-loss premise is the one the project already holds
via [[F24]] (a per-step `ε`) and [[A1]] (peak working set tracks depth, not total
material), and sheet `17`'s own model term `ℒ_model = O(n) = O(T)` is that
premise restated as a sum of bounded per-chunk losses.

Scope: the *asymptotic guarantee* does not stand — see qualifier [[F36]]. What
stands is the empirical demonstration, at the lengths tested, on tasks where the
monolith actually degrades. And per [[F35]], the linear bound is a property of the
*worker* side; the aggregator side is where sheet `17` assumes `O(T)` in one
sentence and where the loss is most likely to grow faster (see [[I10]]).

### F34 — Sheet 17's three-factor split is a reasoning vocabulary, not a measurement; the usable output is a cheap regime triage

None of task noise, aggregator noise, or model noise can be measured on its own —
two of the three are defined against ideal per-chunk artifacts and an ideal
merger that cannot be computed for any real task. So the framework is an
accounting scheme for reasoning about a pipeline, not an estimator of one.

What *is* implementable is the regime classification, read off a cheap chunk-size
sweep (hold the input fixed, vary chunk size, look at the curve shape):

- **Flat curve** — splitting neither helps nor hurts; split only to buy cost or
  latency.
- **Interior optimum** — worker loss dominates; split and tune the chunk size to
  the peak.
- **Low and flat** — the return schema is the ceiling; a better worker, a better
  aggregator, and more compute all buy nothing (see [[F35]]).

Consequence: this gives [[F8]] ("no dominant strategy; it is task-conditional") a
concrete diagnostic procedure. Caveat: the regimes are assigned by comparing
curve *shapes* across tasks that use different metrics with different scales, and
no sample sizes or dispersion are reported for any of the underlying curves.

### F35 — When the sub-task return schema cannot carry the task's cross-unit dependencies, decomposition saturates below the achievable score regardless of model quality

Sheet `17`'s task-noise-dominated regime (the "Silo Effect"): performance
"saturates below the optimal performance regardless of model quality," and the
aggregator's only escape is to "reintroduce nearly the entire input" — i.e. undo
the decomposition. The binding quantity, `ρ_task`, is a property of the **sub-task
return contract**, not of the task: the paper's own example is "return the 2nd
smallest number in your chunk" (which structurally cannot carry the global
answer) versus "return the two smallest per chunk" (which can), on the identical
task with the identical chunking. Information the schema does not encode is gone
before the aggregator runs, and no merger recovers it.

Consequence: concrete support for `02-capability-as-granularity.md`'s claim that
the decomposition interface sets the ceiling and binds *before* the executors
start failing. The schema has to be built from the task's dependency structure —
which is the capability [[F26]] identifies as the expensive one that fails first
on weak models. Reinforces [[F15]] (structured intermediate output is a
correctness property once a later step consumes it) and is the single-level
long-context instance of [[F16]] (independent-parallel splitting destroys a
dependency the task needs). It is also the seed of [[I10]]: the aggregator
re-reading the whole input to fill the schema's gaps is the merge step
re-entering the regime the split was meant to escape.

Diagnostic direction: when recombination looks unreliable, suspect the sub-task
return contract before the aggregator. Sheet `17`'s planner-generated aggregator
prompt wins (§5.4) mainly by rewriting what each *worker* returns so the merge
becomes well-posed — the "two smallest per chunk" fix is applied at the worker
prompt, not at the merge step.

### F37 — The onset of a model's length-induced collapse is a per-model property, varies by an order of magnitude, and measuring it has precedent

Sheet `17` Key finding 1 (Table 2): on retrieval, GPT-4o holds a perfect score
across the whole 1K–128K sweep; GPT-4o-mini holds to 32K then falls (0.86 at 64K,
0.60 at 128K); Llama-3.1-70B holds to 32K then collapses (0.91 at 64K, 0.15 at
128K); Llama-3.2-3B degrades from 16K and is at 0.01 by 64K. The length at which
single-shot fidelity begins to fall is a property of the model, not of the task,
and the spread across models is roughly an order of magnitude.

Consequence: a fixed chunk size, context budget, or decomposition depth cannot be
set once and reused across models — the threshold that determines whether a unit
still fits under the model's grain has to be measured per model. This is a direct,
measurable input to task-granularity decisions
(`02-capability-as-granularity.md`) and to context management in general: "how
much context before this model degrades" is model-specific telemetry, not a
constant. Studying this curve is itself a strong argument for granularity as the
governing variable.

Methodology precedent: this is not something the project would need to invent.
Sheet `17` leans on RULER (Hsieh et al. 2024) for its degradation premise and
cross-checks against "effective context length" in Appendix L; the
needle-in-haystack and effective-context-length benchmark family already measures
this curve per model. What sheet `17` adds (Appendix L) is that a single
"effective context" scalar does not predict behaviour across task types — the
curve has to be measured per model *and* per task family.

### F38 — Selective retrieval and exhaustive chunked decomposition are not interchangeable; retrieval fails when the needed information is diffuse rather than locatable

Sheet `17` Appendix J: BM25/embedding retrieval beats single-shot on the
retrieval task (Llama-70B KV 0.15 → 0.81 BM25) but *degrades* the synthesis tasks
(QA-IB 0.56 → 0.14 BM25 / 0.38 embedding; Sum and Char also down). The authors'
reading: retrieval works when the answer sits in a locatable span and fails when
the relevant information is spread thinly across the input, whereas
chunk-and-aggregate processes the whole text in bounded pieces.

How established: one appendix experiment, one model, one length (128K), no sample
sizes or dispersion — the same reporting weakness as the rest of the paper. The
*direction* is a large effect and has independent support in the
retrieval-augmented-generation literature, where RAG is known to struggle with
global and aggregation questions (the stated motivation for graph- and
summary-indexed RAG variants). The *mechanism* ("diffuse versus locatable") is
the authors' interpretation, not independently tested here.

Consequence: for context assembly, "retrieve the relevant subset" and "process
everything in bounded pieces" are different tools with different failure modes,
and selection loses when relevance is not concentrated. This bears on [[I10]]:
the property that keeps recombination cheap is that sub-results are individually
*locatable* — addressable in a structured store — rather than diffuse.

### F39 — Overlapping or redundant context degrades the step that consumes it

Sheet `17` Key finding 7 (Appendix I): 1K of overlap between chunks on Llama-70B
at 128K drops QA-IB from 0.63 to 0.54 — a 9-point loss from redundancy alone,
while KV, Sum and Char are essentially unchanged. The authors flag that larger
overlap could hurt more, by feeding the aggregator redundant or conflicting
copies of the same content.

Weak in isolation — one model, one overlap size, one length, no dispersion — but
the amplitude is not trivial, and the direction is consistent with
`10-foundations/04`'s claim that what makes context costly is redundancy rather
than volume. Consequence: a recombination or reasoning step should be fed each
piece of information once; overlapping sub-task inputs "for safety" is a cost, not
a hedge.

### F40 — For an intermediate result of uncertain validity, carry it forward weighted by confidence rather than making a premature binary accept/reject

Sheet `18` (ARES): the mechanism against error propagation is not a hard filter
that deletes suspect claims but a *soft* one — an earlier claim is retained in
the premise pool of every later step with probability equal to its own entailment
score. Hard filtering is brittle: one false rejection destroys a chain that was
recoverable (the mirror of [[F20]]). No filtering pollutes: a wrong item is
carried with an implicit accept stamp ([[F27]]'s laundered failure). The weighted
carry is the middle path, and it requires the item to carry a soundness or
confidence field.

Scope — this is broader than decomposition. It applies wherever an item of
uncertain validity is stored or carried forward:

- decomposition sub-results ([[I10]]);
- the provenance graph and descendant invalidation ([[I5]] — extend "provenance
  as a required field" to "provenance plus a soundness weight");
- the memory / knowledge layer (the open-questions register's *Memory* section on
  contradictory memories and revise-versus-append): a doubtful entry is weighted
  down, not deleted, and its weight propagates to anything derived from it;
- any artifact carried across a long task.

Caveat: the weight is only as trustworthy as whatever produces it — see [[F41]]
and the C3 caution on certified-looking scores from uncertified verifiers.

### F41 — A verification mechanism amplifies a competent checker and cannot rescue an incompetent one; with a weak checker it can degenerate silently

Sheet `18` (ARES) states it outright: "ARES can only improve upon entailment
models that can already do correct entailment." With a weak backbone the
per-claim retention probabilities all rise toward 1, the premise pool stops
filtering, and the method silently becomes the no-filtering baseline (Entail-Prev)
at many times the cost. No deployment diagnostic is proposed for this collapse,
though the realised-sample-count ratio — very low means the verifier is confident
everywhere — would serve as one.

Consequence for evidence-based feedback loops: the loop's reliability is bounded
by the checker's *base* competence on the actual judgment. Layering a clever
aggregation on top — ARES-style marginalisation, K-vote, multi-round debate — buys
cost and no signal when the underlying checker cannot do the base judgment, and
can degrade without announcing it. Before building a retroaction loop on a
verification signal: establish the checker's base competence on the real judgment
(not a proxy), and instrument a runtime diagnostic for the degenerate mode.
Extends [[F17]] (self-evaluation is the load-bearing weakness) and [[F23]]
(coordination tax grows as the model weakens); [[F11]] is the selector-level
instance. Sheet `20` measures how large the base-checker bias actually is for LLM
step-verifiers.

### Papers the gathered findings keep pointing at

- **Faith and Fate** (Dziri et al., NeurIPS 2023) — flagged by sheets `05` and
  `06`, now read in full as sheet `13`; it feeds [[F24]], [[F25]], and [[F16]].
- **Feng et al. 2023** (circuit-complexity account of why CoT works) — still not
  read; cited by sheets `06` and `10` as the theoretical grounding for why
  splitting the computation helps at all.

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

### F36 — Sheet 17's "weak chunked beats strong single-shot" headline is bounded to the regime where the monolith degrades

A scope bound on [[F33]], carrying nothing on its own. The headline comparison is
demonstrated only where the single strong model is in a length-degradation regime
that the strongest model tested (GPT-4o) never enters on the retrieval task — it
holds a perfect score across the whole 1K–128K sweep. The crossover needs the
monolith to collapse with length; on a task a capable model handles whole,
splitting on length has no case. Do not carry the headline into a regime with
capable models on tasks within their grain. Superlinear collapse itself is
asserted from eyeballed curves — no growth exponent, no test against a linear
null — so the mechanism behind the headline is thinly evidenced even where the
empirical gap is real.

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
