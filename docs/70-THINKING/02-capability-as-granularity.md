# Capability as a Granularity Ceiling

**State:** OPEN
**Opened:** 2026-09-03
**Origin:** raised as a reframe when `01-use-cases.md` OQ-1 ("is investigation a
different faculty from judging?") was called a dead end. It is — because the
faculty ontology is wrong.

## The hypothesis

> Model size may govern principally **the granularity at which relevant context
> can be accounted for** — not how "smart" the model is, and not which faculties
> it possesses.

Under this reading there are no organs. Doing, judging, planning and
investigating are the same operation applied at different granularities, and a
model has a **ceiling**: the coarsest context unit it can still integrate
correctly. Below the ceiling it works. Above it, it emits fluent output
uncorrelated with the truth.

**Refinement (2026-09-04) — the ceiling is an abstraction span, not a size
limit.** *A finite model with infinite context cannot solve a Rubik's cube from
the position of each of its atoms.* The information is all there, losslessly, and
it is useless — because it sits at the wrong **level**, not because there is too
much of it. So the quantity is not "how much context can be held" but:

> **the grain gap the model can close** — the distance between the representation
> it is handed and the representation the question actually requires.

A finite model has a finite abstraction span. This is the formulation the rest of
the document should be read against; it is sharper than the original, and unlike
the original it yields a real discriminator (see the grain-match test in the
audit).

This is the thesis' central open question (`10-foundations/01` — *"where does
orchestration overhead exceed the benefit of decomposition?"*) restated in a form
that can be measured.

### Naming convention: qualify which ceiling

Whether "the ceiling" belongs to the model or to the model-plus-assembly is a
**definitional choice, not an empirical question** — and the useful move is to
stop choosing and start qualifying. The terms, named whenever the layer is not
clear from context:

| term | meaning |
|---|---|
| **bare ceiling** | the model alone, naive context assembly, no scaffolding (the *model* layer) |
| **effective ceiling** | the model under a **named** scaffold — always stated with which one (the *processor* layer) |
| **integrated system ceiling** | the grain at which the *whole configuration* — decomposer, executors, aggregator — still **preserves and achieves the original objective** (the *system* layer) |
| **system+user ceiling** | the integrated system with the human operator in the loop — the grain the operator-plus-system pair can still reach together |
| **lift** | `effective − bare`, in rungs. The project's output quantity. |

**The third term was added (2026-09-04) because the objective-dissolution failure
requires it.** Driving every sub-task below the *executor's* ceiling does not
bound the system, because the system can complete each piece perfectly and
deliver something irrelevant to what was asked. The failure is not located in any
executor. It is a property of the configuration, and it needs its own name.
(This failure is a hypothesis, argued not evidenced — see the prior-art section
and `06-primary-source-verification.md`.)

**And it is bounded by aggregation, not by execution.** Recombination is a
coarse-grained operation by construction — it requires holding what all the
pieces were *for* — so the integrated system ceiling sits at the aggregator's
limit however finely the executors are fed. Improving executors cannot raise it.
ARIES's deterioration at depth — 4.12× on one synthetic task — is this ceiling
being crossed: more depth means more aggregation transformations, each with its
own failure probability.

Practical consequence: **decomposition has negative returns before the executors
start failing.** The binding constraint arrives earlier than an
executor-ceiling-matching rule would predict, and from a different direction.

"The ceiling" unqualified is henceforth a mistake. A bare ceiling is a property
of a model; an effective ceiling is a property of a *configuration*, and there
are as many of them as there are scaffolds.

**Refinement (2026-09-07) — "always" was overstated, and there is a fourth
rung.** The rule is not a mechanical qualifier on every use. "Ceiling" does not
name the same layer from one context to the next — model / bare, processor /
effective, system / integrated, and system+user — so when a passage discusses a
capability limit and does not make the layer clear, state which one is meant;
where it is obvious from context, an unqualified "the ceiling" is fine.
Consequence for a claim such as *a good prompt raises the ceiling*: it is
established at the processor / effective layer, where eliciting latent model
capacity is exactly what raising that ceiling means, and separately open at the
model / bare layer (`70-THINKING/ideas.md` I8).

This dissolves OQ-2 rather than answering it, and it sharpens everything
downstream: *authoring a decomposition requires operating above the target's
effective ceiling* — a specific, checkable relation between two named numbers
instead of a vague appeal to being "above the ceiling."

## Why it deserves to be taken seriously: it retro-explains the findings

The hypothesis was not constructed to fit the evidence, but it fits better than
"the 7B is bad at judging" does — and it fits the *anomalies*, which is the part
that matters.

| finding | "it's a weak model" | granularity ceiling |
|---|---|---|
| doer's "emit the whole corrected file" is reliable; cross-file indirection doesn't break it | doing is easy | one coherent unit, well under the ceiling |
| no reviewer framing — neutral, adversarial, structured, K=5 — lifts the judge | judging is hard | judging needs claim + diff + intent + counterfactual **integrated at once** — over the ceiling, and *stance does not change granularity* |
| the planner stance is the only place the critical read is live (2/3 catch the false premise) | unexplained | planning **asks for the coarse view explicitly**, so the right granularity is on the table instead of implicit |
| `criteria_first` was *actively harmful* | unexplained | it imposed a granularity mismatch: criteria at one grain, artifact at another |
| concern-split took wf6 from 2/6 to 6/6 | decomposition helps | splitting *is* granularity reduction, done by hand |
| premise-audit-as-gate false-declines ~20 % | the model is unreliable | at that granularity the signal is noisy **in both directions** — not blind, uncalibrated |
| a deterministic gate scores 9/10 alone; adding the 7B panel drops it to 6/10 | the model adds noise | the panel operates above the ceiling; the gate operates below it |

The row that carries the most weight is the second. Every reviewer intervention
tried in the judge-lab varied **stance** — be neutral, be adversarial, be
structured, vote five times. None varied **granularity**. If the hypothesis is
right, none of them could have worked, and the null result is not a capability
verdict at all.

## The competing hypothesis

**H3 — approval bias is a training artifact.** Instruction-tuned models are
trained toward agreeableness. "Assert the property and approve" may be a learned
disposition rather than a capacity limit.

This matters because H3 is not distinguishable from the granularity account on
current evidence, and it makes a **different prediction under a capability
sweep** (below). It must be carried, not dismissed.

## Consequence 1 — decomposition gets a stopping rule

If there is a ceiling, then decomposition is not "making the task easier." It is
**granularity matching**: split until each unit fits under the ceiling.

That yields the rule the project has been missing:

> **Orchestration overhead exceeds its benefit exactly when you decompose below
> the ceiling.** Splitting a unit that already fits is pure cost.

Which retro-explains the two most awkward results in the log: the M4 fixed chain
losing to the monolith (5/8 vs 6/8) on tasks that already fit, and concern-split
costing 252 s to help two tasks out of thirty. Neither is evidence against
decomposition. Both are evidence against decomposing *unconditionally*.

The M7 firing rules become principled rather than hand-set: **fire on
granularity demand, not on task type.**

### Prior art, and two failure modes this account was missing (2026-09-04)

`03-how-the-field-frames-it.md` §5b turned up **ADaPT** (*As-Needed Decomposition
and Planning*, UNC Chapel Hill / AI2 / Saarland), which states the rule from the
other direction and predates every shipped tool: *try directly; decompose only on
failure; recurse; cap the depth.* Depth comes out **emergent** — 1.9 average on
depth-2 tasks, 2.8 on depth-3 — and it is explicitly framed as adapting to *both
task complexity and model capability*, which is the two-variable form this
section needs. The stopping rule above is therefore **confirmed prior art, not a
new idea** — and that is good news, because it has been evaluated.

Two failure modes this document did not originally anticipate — **provenance
corrected 2026-09-05** (`06-primary-source-verification.md`); neither is from the
ADaPT paper, which was the first draft's claim:

- **Tangential success.** Sub-tasks are completed with high fidelity and the
  result is *irrelevant to the original goal*, because each sub-task acquires its
  own optimisation target — *"do this sub-task well"* rather than *"move toward
  the goal."* Decomposition does not merely cost overhead; **it can dissolve the
  objective.** Nothing in "decompose until it fits under the ceiling" protects
  against this, and it is the failure that a ceiling-matching rule would produce
  *most* readily, since matching the grain says nothing about preserving intent.
  **This is the project's own reasoning, not an evaluated result** — the term
  comes from an uncited practitioner blog. It is a hypothesis the instrument
  should be built to detect, not a finding it can assume.
- **Aggregation is a binding constraint.** ARIES (thought-graph puzzles, distant
  domain) reports deterioration reaching **4.12× on one synthetic sorting task**,
  with recombination accounting for the majority of policy-agent errors —
  *if merging sub-task outputs is error-prone, deeper decomposition actively
  hurts.* The mechanism transfers; the multiplier is one data point.

**The second one bites hardest, and it sharpens the Principia point.** Splitting
is cheap; *recombining* is not — and aggregation is a **coarse-grained operation
by construction**, since it requires holding what all the pieces were for. So
route (b) in Consequence 2 has a constraint the earlier framing missed: you can
always decompose conceptual work below the ceiling, but the **aggregation step
sits above the ceiling no matter how finely you split.**

Russell and Whitehead did not only have to author the decomposition. They had to
know it **composed back**. The authorship constraint (OQ-7) covers both, and the
aggregation half is the harder one.

**Consequence for the ladder — stated carefully (2026-09-04), because the first
version overreached.** An earlier draft said "an honest ceiling probe has to
include the recombination." That smuggled in a **two-pole factor structure** —
decomposition at one end, recombination at the other — which is not established
and should not be designed into the instrument.

There is no reason yet to believe the ceiling resolves into two poles. At least
three operations are in play, and they may or may not be separate abilities:

- **decomposition** — coarse → fine: turn an objective into sub-objectives;
- **recombination** — fine → coarse: turn sub-results into an answer to the
  original;
- **objective preservation** — carrying intent across the split, which is what
  tangential success violates and which is neither of the other two.

They might be one ability applied in different directions, three separate ones,
or something with no small factor structure at all. **Assuming the answer inside
the instrument would guarantee the instrument confirms it.**

**What survives from the original point**, and it survives whatever the structure
turns out to be: *a probe that measures one operation reports the ceiling for
that operation, not for the system.* Since the binding constraint appears not to
be execution, a decomposition-only probe reports a number that does not bind.

**So: a probe family, not a probe** — one instrument per operation that can be
isolated, with the factor structure as an **empirical result** rather than a
design premise. This is the same discipline already applied to the multiple
ladders: divergence across instruments is the finding, not a defect.

### Reframe: "ceiling" is a 1-D approximation of a region boundary (2026-09-04)

The objection that produced this section was initially misread as *"isolating
operations is invalid."* The actual objection is sharper and worse:

> Decomposition, recomposition and maintaining goal focus are **skills** whose
> success **cannot be predicted in general from a small set of probes.**

A handful of one-dimensional slices does not reconstruct a high-dimensional
space. Ladders yield **traces**, and generalising from traces to "will this
system succeed on task X" is unwarranted no matter how carefully each trace is
measured. The problem is not validity of the individual probe. It is
**underdetermination**.

**Skills, not tasks — and the distinction is load-bearing.** A task can be probed
directly. A skill cannot: it is **latent**, observable only through its
manifestation in task outcomes. So this is not a measurement problem with a
measurement fix. It is a **latent-variable inference** problem — infer unobserved
capacities from observed successes and failures — which is why no small probe set
suffices and why the earlier isolation sketch was doomed regardless of how
carefully each probe was built.

**This has a literature, and it is the literature check the standing assumption
below asks for.** Inferring latent skill profiles from item responses, without
access to the skills themselves, is the subject of **item response theory** and
**cognitive diagnosis modelling**. Their machinery maps directly:

| here | there |
|---|---|
| the projection φ | the **Q-matrix** — which items demand which skills |
| a configuration's capability | the latent ability profile |
| success on a task | an item response |
| "can a small probe set determine capability?" | **Q-matrix identifiability** — a formally studied question with known structural conditions |

That last row is the important one: the objection raised here is a known problem
with established results on when latent structure is and is not recoverable, and
how many items it takes. Reading that work before designing any probe is now the
cheapest available move — it may well answer, from outside, whether the skill
decomposition is licensed at all.

Which indicts the vocabulary. *"Ceiling"* presumes a scalar threshold on a scalar
quantity. Everything observed so far says otherwise — the ceiling is not flat;
tuning reshapes it *in specific areas*; ladders are expected to diverge. Those are
not three separate complications. They are what one thing looks like:

> **Capability is a region in a task-feature space, with a complicated boundary.
> A ladder measures a single ray through that space and reports where it exits.**

Under this reading, ladder divergence stops being a confound to control for and
becomes **information about the shape of the boundary** — and the earlier
falsification test, which treated divergence as evidence against the hypothesis,
was asking the wrong question of it.

#### The proposal: a projection, not a set of axes

Rather than extracting traces along several chosen axes and hoping they
generalise, define a **projection** `φ: task → feature space`, and let capability
be the **region** in which a given configuration succeeds.

This separates two things the thread has been conflating:

| | model-dependence | what it is |
|---|---|---|
| **φ(task)** | independent | where a task sits, computed from the task alone |
| **the success region** | dependent on model + scaffold + operator | which part of that space this configuration handles |

Everything the thread has proposed measuring then unifies as one geometry:

- **rungs of lift** = the region **growing** when scaffolding is added;
- **floor height** (dispersion across operators) = **variance in the region's
  extent** across who is driving;
- **the depth bound** for the ADaPT contribution = where a task's projection sits
  **relative to the boundary**;
- **prediction** = region membership, which is the thing a small set of probes
  could never deliver.

#### Requirements on φ, and what would sink it

Naming requirements rather than features, because choosing features by intuition
is the error this section exists to avoid:

1. **Computable without running the task** — otherwise it cannot predict.
2. **Cheap** — otherwise the prediction costs more than just attempting the work.
3. **Not requiring above-ceiling authorship per task** — otherwise OQ-7's cost is
   reintroduced at every prediction, which is fatal at volume.
4. **Model-independent** — features of the *task*, so that configurations can be
   compared in the same space.

**The instrument changes accordingly, and this partly supersedes the ladder
section above:**

- **A task population, not a ladder, is the measuring instrument.** Mapping a
  region needs many points; a ladder gives ~5 along one ray. The M6 suite is
  closer to the right *kind* of instrument than a ladder is — 30 tasks, varied —
  though it is small for this purpose and was not built with any φ in mind.
- **The ladder's role changes to calibration.** A controlled ray, where only grain
  demand varies, is the right tool for **validating that φ orders tasks
  correctly** — not for measuring capability. That is a better job for it than
  the one originally assigned.

#### The prior question: validate the instrument, not the subject (2026-09-04)

Everything above was designed around *measuring a model's ceiling*. The goal that
actually comes first is different:

> Measure **what fires consistently across a set of tasks collectively intended to
> benchmark one skill** — i.e. do those tasks behave like a measurement of one
> thing, and is that thing the thing they were named for?

That is **construct validation**, and it precedes any use of the instrument. Its
standard apparatus:

| the question | the term |
|---|---|
| do items meant for one skill actually co-vary? | **internal consistency** (Cronbach's α, McDonald's ω) |
| does each item load on the factor it was written for? | **factor loading** |
| do skill-A items resemble each other more than skill-B items? | **convergent / discriminant validity** |

Reordering consequence: **a task set is not a benchmark until it has been shown
to measure something coherent.** The M6 suite has never been examined this way —
it was built to separate *pipelines*, and whether its `stresses` tags correspond
to anything with factor structure is unknown and cheaply checkable.

#### How much boundary proximity actually matters — resolved

Two positions were both partly wrong. "A frontier model as subject tells you
nothing" was wrong (see the graded-observables correction below). "Any non-trivial
task will do" is also incomplete, and the resolution is the same for both:

**No individual subject needs to sit near its boundary. The subject *population*
must collectively span the item set's difficulty range.**

Factor structure is recovered from **covariance across items**. An earlier draft
said a subject that passes everything "contributes none" — **that is wrong, and
the correct version is more useful:**

- **It is *items* with no response variance that contribute nothing** — *in the
  outcome channel.* An item every subject passes has zero **outcome** variance,
  therefore zero covariance, and drops out of a factor analysis run on pass/fail.
  **This holds only if the response variable is the outcome**, which is a choice,
  not a given — see the channel distinction below.
- **A subject at an extreme contributes vanishing *information*, not zero.** In
  IRT terms, Fisher information for an item is maximised where the subject's
  ability is near the item's difficulty and falls away as p → 1 or p → 0: the
  response becomes nearly deterministic, so it barely constrains any estimate.
  Negligible asymptotically, but not absent.
- **An all-passing subject still contributes a bound.** It establishes that every
  item sits below its ceiling, and it shifts the estimated item difficulties.
  Weak information, genuinely present.

**And for the stated goal it is directly informative.** If a strong subject passes
every item in a set built to benchmark one skill, that is a finding *about the
instrument*: **the item set does not reach far enough to discriminate at that
level.** Since the goal here is validating the benchmark rather than measuring
the subject, an all-pass result answers the question being asked — it says the
ceiling of the *items* is too low.

With that corrected, the effects remain symmetric and complementary:

| subject | uninformative where | informative where |
|---|---|---|
| strong model | easy items (**ceiling effect**) | hard items, where weak models all fail |
| weak model | hard items (**floor effect**) | easy and mid items, where strong models all pass |

Their **differential failure patterns are the data.** So the multi-size sweep is
not a nice-to-have for this work — it is the **enabling condition**. A single
subject of any capability cannot reveal factor structure; a population spanning a
range can.

#### On cost as an observable — dropped

For construct validation, cost is secondary: factor analysis takes binary item
responses as standard input, and covariance is what matters. The one exception
raised was **item scarcity** — thirty is thin, and graded responses buy power per
item.

**That exception does not apply.** The item set can be grown cheaply, because a
highly capable model is available to generate items. Cost as an observable is
therefore dropped: it would buy statistical power that is available more directly,
at the price of harness-dependent noise.

#### Which channel is the response? — and how far the Fisher limit reaches

The zero-variance and Fisher-information arguments above were stated as though
the response variable were **pass/fail**. It need not be. The alternative framing
is to observe **what the model fires** on each task — the behaviours it exhibits,
the operations it invokes, the structure of its approach — and reverse-engineer
φ's components from what co-occurs there.

That is the distinction between **outcome-based** and **process-based**
measurement (process/log-data analysis is an established area in educational
measurement, using action sequences and intermediate states rather than final
responses). It changes the earlier conclusions:

**An item everyone passes is not information-free in the process channel.** Two
subjects can both pass and pass *differently* — one decomposed, one did not; one
backtracked, one went straight through. That is variance in behaviour with zero
variance in outcome.

**How the Fisher limitation applies — the live question, answered as precisely as
is honest:**

1. **The p ≈ 0.5 result is a property of the Bernoulli likelihood, not a law.**
   For a binary item, information about ability goes as `a²·p(1−p)`; it peaks near
   p = 0.5 and vanishes at the extremes *because the response is one bit*.
   Saturation is a fact about that channel.
2. **A richer observable does not vanish at p → 1.** When the response is a
   feature vector, the outcome can be deterministic while the profile still
   varies. The outcome channel saturates; the process channel need not.
3. ~~**But the formal machinery does not transfer.**~~ **Overclaimed —
   corrected (2026-09-04).** It was asserted, not shown, and the assumption that
   it transfers is the correct one. Fisher information requires a likelihood, and
   richer observables **can** have one:
   - **response-time IRT** — joint parametric models over accuracy *and*
     log-response-time; information fully defined;
   - **polytomous IRT** (graded-response, partial-credit) — discretise behaviour
     into ordered categories and the information function is standard;
   - **latent-state sequence models** — HMM-style likelihoods over action
     sequences with latent skills as states.

   **And the payoff runs the right way:** polytomous and continuous response
   models carry *more* information per item than dichotomous ones, and their
   information functions are typically **broader and flatter** — they do not
   collapse as sharply in the tails, because a graded response keeps varying
   where a binary one has already saturated at 1. That is precisely the property
   wanted for measuring far from p = 0.5.

   **The real cost is a modelling burden, not an impossibility.** To get Fisher
   information over process data you must commit to a generative story about how
   skills produce behaviours, and misspecification bites. The honest trade:
   *exploratory* methods (factor analysis, clustering on raw features) assume
   little and guarantee nothing; *parametric* methods give the full machinery,
   conditional on the model being right.
4. **Process variance also saturates — just later.** A subject far above an item's
   demand does the obvious thing in one step: no decomposition, no backtracking,
   no structure to observe. Nothing was required, so nothing is exhibited. This is
   the earlier **"the subject must strain"** conclusion re-derived in the process
   channel, and it is why boundary proximity still matters, though less strictly
   than for one-bit responses.

**Two further limitations that apply to the process channel specifically:**

- **What is observed is harness-mediated.** Whether a model "decomposes" depends
  on its tools, its system prompt, and what the scaffold permits. Behavioural
  profiles therefore characterise **model + harness**, not model.

  **Adopted as a methodology constraint rather than treated as a defect
  (2026-09-04): build φ at the level at which the skill is intended to be used.**
  What gets deployed is a configuration, so measuring the configuration is the
  honest target, and this sits consistently with the bare / effective /
  integrated vocabulary. The price is explicit: **φ does not transfer across
  harnesses**, so a harness change invalidates prior measurements — the same
  stability exposure that is already the contribution's single point of failure.
  Whether that can be accommodated later is open.
- **It is still latent-variable inference.** Inferring which skills fired from
  what behaviour is visible is the same epistemic situation as inferring them
  from outcomes, with a wider observation channel. **Richer observables reduce
  underdetermination; they do not remove it.** The identifiability question stands
  unchanged.

#### A third channel: white-box projection

Beyond outcome and process, there is **internal state** — projecting the model's
activations for a given context and response, rather than reading its text. The
field exists and is active:

| technique | what it gives |
|---|---|
| **probing classifiers** | train a light classifier on hidden states to predict a property — e.g. "does this task demand skill X" |
| **sparse autoencoders / dictionary learning** | decompose activations into a basis of features. **This is literally "how many live dimensions," asked of activation space instead of behaviour** |
| **representation geometry** | feature directions, linear structure, steering |
| **logit / tuned lens** | intermediate predictions layer by layer |

The SAE parallel is worth pausing on: dictionary learning over activations is the
same question posed earlier about tasks, one level down.

**Two constraints decide how it can be used here, and the second is decisive.**

1. ~~**It requires white-box access, unavailable for the frontier model.**~~
   **Weakened (2026-09-04).** Open-weight releases now reach frontier-adjacent
   scale, including large sparse-MoE models where total parameters are very high
   but *active* parameters per token are a fraction of them. The anchor subject is
   therefore not necessarily closed, and the channel may be available across the
   whole difficulty range after all. What survives is narrower: white-box access
   is unavailable for *specific* closed frontier models, not for the top of the
   scale as such.
2. **Activation geometry is model-specific — but the claim was stated too
   broadly (corrected 2026-09-04), and the correction changes what is possible.**

   > ⚠️ **UNREVIEWED.** This correction was written at the end of a session and
   > has **not been read or challenged** by the other party, who had already
   > responded to the *original*, overbroad claim ("model-specific, therefore
   > model-bound") and reasonably concluded it invalidated the white-box
   > prospect. That reaction is **not** a response to what follows. Everything
   > else in this thread was hardened by argument; this block was not, and
   > carries correspondingly lower confidence. **Discussion deferred — resume
   > here.**

   **What is genuinely model-bound:** raw coordinates. Activation bases are
   arbitrary, dimensionalities differ across architectures, and training
   randomness yields different solutions. Model A's dimension 47 has no
   relationship to model B's. A specific SAE feature discovered in one model
   cannot be asserted to mean the same in another, so "discover a feature, name
   it, reuse it elsewhere" does not transfer.

   **What does transfer: relational structure over a shared stimulus set.** This
   is the standard move where direct alignment is impossible — used in
   neuroscience for exactly this reason — and it has established machinery:

   | technique | what it compares |
   |---|---|
   | **representational similarity analysis (RSA)** | similarity *matrices* rather than coordinates: does model A place tasks X and Y close and Z far, as model B does? |
   | **CKA** (centered kernel alignment) | representational similarity across networks of differing width and depth |
   | **relative representations** | encode each item by its similarity profile to a fixed **anchor set**, giving a coordinate system that is model-independent by construction |
   | **linear alignment / stitching** | learn an explicit map between two models' spaces where one exists |

   **The requirement this imposes is already satisfied.** Anchor-based comparison
   needs every model run on the *same* item set — which is precisely the design
   already in place. **The task population is the anchor set.** The machinery is
   available at no extra cost.

   **And it converts the limitation into a validity check that behaviour alone
   cannot provide.** If several independently-trained models organise the task
   set into the *same* similarity structure, that structure is likely a property
   of **the tasks**, not of any model — which is exactly the discriminant φ needs.
   Convergent structure across models is far stronger evidence for a real
   dimension than clean structure within one.

   **Honest caveat on that check:** convergence can be driven by shared training
   corpora, tokenisation, or architecture family rather than by real skill
   structure. Agreement among variants of one family means little; agreement
   across genuinely different families means considerably more, and the model
   selection should be chosen with that in mind.

   **Net effect on the approach:** not invalidated, **constrained**. Raw geometry
   is unusable; relational structure over the shared task set is usable, and the
   constructive path below — hypothesis generation, then task-level
   operationalisation — is unchanged and now better motivated, since the
   relational analysis supplies *how many* dimensions and *which groupings*,
   leaving only the search for their task-level correlates.

**Constructive use, given both:** treat white-box projection as a **hypothesis
generator for φ's components, not as φ.** Use activations to discover candidate
dimensions cheaply and with high resolution; then **operationalise each candidate
as a property of the task**, computable without the model; then validate it
behaviourally across the subject population. That keeps comparability while
exploiting the richer signal where it is available.

**One genuine advantage over the process channel:** activations are a function of
model and input, not of what the scaffold permitted — so this channel is
**harness-independent** in a way behavioural observation is not, and partially
sidesteps the constraint adopted above.

**Cost, stated plainly:** this is research-grade work. SAE features are notoriously
difficult to validate, probe results are easy to over-read, and none of it is a
cheap add-on to the psychometric programme — it is a separate research line that
happens to feed it.

##### Does it have to fit in memory? — no, and the workload is the friendly case

Two sub-questions, and the answers are better than the hardware suggests.

**Can "what would fire" be known without running?** No — activations *are* the
forward pass; there is no shortcut that skips computing them. But the relevant
question is what *kind* of run is needed, and the answer is the cheap kind:
**context + response is already in hand, so this is a scoring pass, not
generation.** One teacher-forced forward pass over the full sequence, parallel
across tokens, no autoregressive decode. Nothing is being produced; the sequence
is being *replayed* to observe it.

**Can it run without fitting in memory?** Yes, by layer streaming — hold one
layer resident, push the whole batch through it, discard, load the next
(`device_map`/disk offload, ZeRO-Inference, FlexGen and llama.cpp offload all do
this). M0 already measured the cost: **VRAM fit is a hard binary with a ~10–20×
offload cliff.**

**And that cliff does not bind here**, for two independent reasons:

- **The workload is throughput-insensitive.** Activation collection is an offline
  batch job. A 10–20× slowdown on something that runs overnight is irrelevant —
  the cliff is a *latency* penalty, and there is no latency requirement.
- **Scoring amortises weight I/O in a way generation cannot.** Under layer
  streaming, each layer's weights are loaded **once per batch** and every token of
  every sequence passes through while resident. Generation would re-touch the
  model per decoded token. This is the difference between offloaded inference
  being painful and offloaded analysis being routine.

Two further economies: probing usually finds **middle layers** most informative,
and a run can simply **stop** at the deepest layer of interest; and for a sparse
MoE, the router's **expert selection is itself a discrete, countable per-token
firing pattern** — a literal answer to "what fires," far cheaper to record and
analyse than dense activation geometry. (Caveat: expert routing is a noisy
interpretability signal and experts do not map to human concepts — but as a
*dimensionality* signal it is directly usable.)

**The binding constraint is storage, not compute.** Hidden states for all layers ×
all tokens × hundreds of tasks is enormous. Sample layers, sample token
positions, or project down at collection time rather than storing raw. This is
the practical limit people underestimate.

**Unchanged by any of the above:** constraint 2. Running a large open model yields
*its* geometry, still not comparable to another model's — so the constructive use
(hypothesis generation, then task-level operationalisation) stands regardless of
how much white-box access is available. And quantisation is a confound to name:
probing a heavily quantised model measures the quantised model, which is correct
if that is what gets deployed and a generalisation error otherwise.

#### Consequence: the item set must reach the frontier ceiling

The Bernoulli information result cuts both ways, and the second direction is the
useful one. If a subject informs most about items near **its own** ability, then:

> **Item difficulty range and subject ability range must co-extend.** An item's
> difficulty is not estimable unless some subject sits near it; a subject's
> ability is not estimable unless some item sits near it. Test design and sample
> design are coupled.

So the item set has to reach the **frontier** ceiling — even though the
deployment target is a 7B. That looks wasteful and is not:

- **Hard items anchor the scale.** Without them, everything above the 7B's
  ceiling is unresolved, and "just above" cannot be distinguished from "far
  above."
- **Which is what makes lift measurable.** If the item set tops out just past
  bare-7B, a scaffold buying 3 rungs and one buying 6 look **identical** — both
  pass everything. That is a ceiling effect on the *instrument*, and it would
  silently cap the project's own output metric.
- **It also gives the all-pass result its meaning.** A frontier model passing
  everything says the scale does not extend far enough, and therefore that lift
  measurements will saturate before the scaffolding does.

**The cost, stated honestly:** items at the frontier ceiling are the *hardest to
author correctly* — subtler correctness conditions, so the broken-check risk is
worst exactly where the items are most expensive. And the conjunctive problem
bites hardest at the top, since the hardest tasks tend to demand many skills at
once, losing diagnostic resolution precisely where range is most needed.

**Resolution: two item populations with different design targets**, rather than
one set required to do both jobs.

| population | purpose | design requirement |
|---|---|---|
| **anchors** | extend the difficulty scale to the frontier so ability and lift stay resolvable at the top | correct check, genuinely hard. Conjunctive and diagnostically messy is **acceptable** |
| **diagnostics** | recover factor structure | mid-difficulty, where discrimination is best; demand varied one dimension at a time |

Separating them dissolves the tension: anchors need not be clean, diagnostics need
not be extreme.

#### Item generation changes what is hard

With generation cheap, the constraint moves, and it moves somewhere less obvious.

**The workflow is standard item banking: over-generate → pilot → select
empirically.** Difficulty is not knowable before running, so generate broadly, run
against the subject population, and keep items on measured behaviour:

- **discard flat items** — everyone passes or everyone fails; zero variance,
  therefore zero contribution;
- **discard low-discrimination items** — they do not separate stronger from
  weaker subjects;
- **treat negative discrimination as a bug signal.** An item where *better*
  subjects do *worse* is almost always broken, not subtle. This is the classic
  red flag and it costs nothing to compute.

Empirical selection partly launders generator bias: items are kept for how they
behave against real subjects, not for what the generator intended them to
measure.

**The real bottleneck is the check, not the task description.** Writing a
plausible task is trivial at any scale. What M6 requires per item is a stdlib
deterministic check under a second, a documented discriminator subtest, and a
pre-existing passing test. **A wrong check is worse than a missing item** — it
injects correlated noise into the response matrix, and correlated noise is
indistinguishable from a factor. A cluster of subtly broken checks will present
as a clean, spurious dimension.

`suite_lint.py` already enforces the mechanical half of this and scales freely.
The *documented discriminator* is the human-judgement half and does not.
Mitigating: the pilot-and-select step catches part of it for free, since broken
checks tend to produce flat or negatively-discriminating items.

**What contamination survives, and cannot be laundered:**

- **The generator imprints its own taxonomy.** A model generating "goal focus"
  items produces the items *it* finds natural, so the recovered factor structure
  may describe the generator's conception of the skill rather than any property
  of the subjects. Selection filters bad items; it cannot add a dimension the
  generator never thought to produce.
- **Coverage gaps are invisible.** You can only select from what was generated,
  and nothing in the analysis reveals what is missing.

Mitigations, unchanged in kind but now load-bearing: generate from **multiple
different models**; retain a **human-authored** subset; and always validate
against a population of **independent provenance** — the M6 suite, or real
tickets subject to `01-use-cases.md` OQ-2.

#### The tension in "harder items surface subtler dimensions"

Plausible, and it has a documented counter-pressure worth designing against.
Harder items often demand several skills **simultaneously**, and a conjunctive
item — one that fails if any of A, B or C is missing — has **poor diagnostic
resolution**: the failure does not say which was missing. Uniformly harder items
can therefore surface *fewer* usable dimensions, not more.

What is wanted is not items that are harder, but items that are **hard in
different ways** — each stressing one demand while holding the others moderate.
Note this is item-level demand variation, **not** the skill isolation rejected
under the standing assumption below: it varies what a task asks for without
claiming the underlying abilities are separable.

#### Bootstrapping φ — and the vocabulary for it

The proposal: rather than positing φ, **discover its dimensionality empirically** —
run models against a task set built to stress a skill, and see how many
dimensions are actually live.

Well-formed, and it already has standard terminology:

| said informally | the established term |
|---|---|
| "how many live dimensions" | **latent dimensionality** — the number of latent traits needed to explain a response matrix |
| deciding which are real vs noise | **parallel analysis** (observed eigenvalues vs eigenvalues from random data of the same shape); scree/eigenvalue decay |
| "is one enough?" | **unidimensionality testing** |
| a task that separates strong from weak | an item with high **discrimination**; one that doesn't is uninformative regardless of quality |
| what destroys discrimination | **ceiling / floor effects** |
| the task → skill map | the **Q-matrix** |
| "can we recover it at all?" | **identifiability** |

**But "project a highly capable model against tasks" merges three distinct
roles**, and they have opposite requirements:

| role | what it does | who should do it |
|---|---|---|
| **subject** | takes the tasks; its responses form the matrix that dimensionality is estimated from | **must be near its boundary on whatever is being observed** — see the correction immediately below, which materially widens who qualifies |
| **annotator** | rates each task's skill demand — authors the Q-matrix, i.e. φ itself | **must be above the ceiling.** This is where "highly capable" is exactly right, and it is the Principia authorship handoff (OQ-7) in operational form |
| **item generator** | synthesises tasks varying systematically along hypothesised dimensions, to get a population large enough to map a region | capable, and cheap enough to produce many |

**Correction (2026-09-04): "a frontier model as subject tells you almost
nothing" was overstated.** It is true only of **binary** pass/fail. A model that
passes every rung has a near-constant *accuracy* vector — but accuracy is not the
only observable, and the others do not saturate at the same place.

| graded observable | why it carries information above the accuracy ceiling |
|---|---|
| **cost to success** — tokens, tool calls, retries, wall time | passing R1 in 200 tokens and R5 in 8,000 reveals the gradient while both remain passes |
| **consistency at K samples** | 5/5 at R4 and 3/5 at R5 locates the boundary while majority-vote still reads "pass". **Variance rises before the mean falls** — the standard reason variance is the more sensitive instrument near a threshold |
| **trajectory shape** | exploration breadth, backtracking, re-reads. The ETH study measured exactly this as a behavioural signature of induced difficulty |

This is the **dichotomous versus graded** response distinction, and the
cost-to-success measure is a **latency**. Joint accuracy-and-response-time models
exist in the psychometric literature precisely because timing discriminates where
accuracy saturates — the same move, already worked out.

**So the requirement is not "the subject must fail." It is "the subject must
strain."** And straining begins earlier than failing, which widens the usable
range of every subject rather than only rehabilitating frontier models.

Two consequences, both improvements:

- **The sweep gets a better discriminator.** Comparing *where each model's cost
  gradient begins* is continuous and far finer than comparing where pass rates
  break, and it separates H1/H2/H3 on more than a handful of transitions.
- **The constrained model keeps its role without needing the overclaim.** It
  strains earliest and most legibly, so it remains the cheapest and most
  informative subject — which is a genuine advantage of the hardware constraint,
  and enough of one without asserting that capable models are useless as subjects.

*Two cautions.* Cost must be normalised **within subject** — against that model's
own baseline on trivial rungs — since larger models may simply spend more
everywhere. And agentic effort measures are noisy and harness-dependent (retry
policy, tool-call budgets), so they are not the clean laboratory latency the
psychometric analogy suggests.

**The circularity risk, which is fatal if ignored.** If the same capable model
both **authors φ** and **generates the items**, φ is confirmed by construction —
the items were built to vary along the dimensions φ posits, so of course φ
explains them. That is benchmark contamination one level up, and it would produce
a clean, meaningless dimensionality estimate.

Mitigations, in order of strength: validate φ against a population it did not
generate (the M6 suite; real tickets, subject to OQ-2); have annotation and
generation done by *different* models; hold out a human-authored task set
entirely. At minimum, **never report a dimensionality estimate from a
self-generated population without saying so.**

#### The risk that would end this

**There is no guarantee a low-dimensional φ exists.** "Rich enough
characterisation" is carrying real weight in the proposal. If capability does not
compress — if success is genuinely irreducible to a manageable set of task
features — then no projection works, prediction in general is unavailable, and
what remains is per-task measurement, which predicts nothing and calibrates
nothing.

That assumption is unvalidated and should be tested early and cheaply: does *any*
candidate φ separate the M6 suite's passes from its failures better than chance,
using features computable in advance? A negative there closes the line before the
ladder work starts.

### Standing assumption: the operations are not separable (2026-09-04)

A first attempt at the above went straight on to sketch how each operation might
be **isolated and measured individually** — which reintroduced, one paragraph
later, the separability the section had just disclaimed.

**Rejected, and the objection is methodological rather than stylistic.**
Generalising from an isolated operation back to system behaviour is a validity
failure of the same family as benchmark contamination: the isolation *creates
structure that is not present in the work*. Supplying fixed, correct sub-results
to measure "recombination" constructs a situation that never occurs — real
sub-results are partial, wrong, and wrong in interacting ways. The measurement
can be perfectly reliable and mean nothing. The decisive part is that **the
dimension along which it backfires is not predictable in advance**, so it cannot
be caveated away by foreseeing it.

> **Standing assumption: the ceiling does not decompose into separable
> operations. Treat it as unitary unless the literature establishes otherwise.**

This is the house rule applied consistently —
`27-arch-adaptation-and-evolution/08`'s *notice the symmetry, do not design toward it*,
and the set-wide refusal to settle by intuition what should be settled by
evidence.

**Consequences for the instrument, which get simpler:**

- **One end-to-end probe.** Objective in, answer out, grain demand varying across
  rungs. Whatever happens internally, the ceiling is the rung where the *system*
  stops delivering the objective. No factor claims are made or needed.
- **A literature check becomes a prerequisite**, not an afterthought: does prior
  work establish separable planning / execution / composition capabilities, or
  compositional-generalisation results that would license a split? If it does,
  this assumption is revised on that evidence. If it does not, the unitary probe
  stands.
- **The candidate contribution survives, and is strengthened.** A calibrated
  depth bound does not require knowing *why* returns turn negative — only *where*.
  An empirical turn point per model+scaffold+task-class is sufficient to replace
  ADaPT's `max_depth`, and is more robust than a mechanistic bound because it
  assumes nothing about structure.
- **The cost is transferability.** An empirical bound cannot predict how it moves
  when the model, scaffold or task class changes; it must be re-measured. That
  puts the entire weight on dependency 3 — stability — which is now the single
  point of failure for the contribution rather than one risk among three.

*Noted for the record, since it is an instance of the thing under study:*
decomposing the ceiling into poles, measuring each with high fidelity, and
arriving at a number irrelevant to the original question **is tangential
success** — committed in the design of the instrument meant to detect it.

## Consequence 2 — conceptual work stops being a separate problem

This is the payoff for `01-use-cases.md`. The five stalled projects — config-as-code
strategy, displacing roofline, job-data tradeoffs, the petabyte audit — looked
like they needed a faculty the model lacks.

Under the hypothesis they need no new faculty. They are **the same operation at a
much coarser granularity**. Which means there are two independent routes to them:

- **(a)** wait for the ceiling to rise — someone else's schedule;
- **(b)** decompose the conceptual work into units under the *current* ceiling —
  buildable now.

Route (b) is the project's entire premise applied to a domain it has not yet been
pointed at. If it works, conceptual work becomes reachable the same way code work
did, and the constrained-intelligence thesis gets its strongest confirmation
outside coding.

## Consequence 3 — the second question is the same question

The other reframe raised alongside this one:

> Do the adversarial-verification findings hold with a more capable model —
> especially **judging from different angles: asking different questions, from
> different perspectives, with context explicitly calibrated from partial views
> of the task?**

That is not a second question. It is **this hypothesis applied to the judging
seat.** Partial views are granularity reduction for the judge: hand each reviewer
a context unit *under* the ceiling — one sees only the diff, one only the
pre-change file plus the objective, one only the test — and let judgment emerge
from the **disagreement structure across views**, adjudicated by something
deterministic, rather than from any single model's verdict.

The roadmap already contains a seed of this (M7, "dueling advocates with
executable claims"). The reframe generalises it: the mechanism is not *advocacy*,
it is **calibrated partial context plus a different question per view.**

### Why K=5 voting failed and partial views might not

K=5 samples the *same over-granular view* five times. The errors are correlated by
construction — five instances of one failure, averaged. Partial views decorrelate
by construction, because the **inputs differ**, not the stance.

That is a mechanistic distinction, and it means the judge-lab null result does
not generalise to partial views. It was never tested.

### Partial views are robust to which hypothesis is true

- Under the **granularity ceiling**: each judge's unit drops under the ceiling, so
  each judge becomes live.
- Under **approval bias**: a reviewer shown only the pre-change file and the
  objective *has nothing in front of it to approve* — the bias has no purchase.

Both accounts predict partial views help. That makes this the rare intervention
worth building **before** knowing which hypothesis is right.

## Consequence 4 — the lift is the measurement, and "rungs" is the unit

The instrument was first posed pessimistically: measure the ceiling, discover
which work is unreachable. That is the less interesting orientation. The
productive one runs the other way:

> The quantity of interest is not a model's bare ceiling. It is the **lift** —
> `ceiling_with_scaffold − ceiling_bare` — and whether that lift keeps growing.

Same instrument, opposite reading. Run a ladder against a bare model, then
against successively better scaffolding, and watch the ceiling move. **The shift
is the project's output.**

This supplies something the project has lacked: a **unit of progress that
accumulates**. Suite pass-rates do not compare across milestones — 24/30 on the
M6 suite says nothing about M9's context governance, and neither number adds to
the other. Rungs do:

> *"This context assembler bought +1.5 rungs at 7B."*

Comparable across milestones, across model sizes, across scaffolding
generations, and directly interpretable as the thing the thesis claims exists.
Every milestone from M7 onward can report in the same unit.

**On "exponentially good."** The optimistic case is that lift compounds: better
tooling lets the model handle coarser units, which lets it help build better
tooling. The mechanism is at least plausible, because scaffolding improvements
are **composable** — a better assembler, a better gate and a better decomposer
multiply rather than add. It is unproven, it is exactly the kind of claim that
should be measured rather than argued, and the ladder is what would measure it.
Two scaffolding generations measured in rungs would already show whether the
lift is growing, flat, or saturating.

## The experiment — the sweep discriminates three ways

The multi-size sweep, run against the existing M6 suite, separates all three
accounts. No new fixtures required.

| account | prediction under a capability sweep |
|---|---|
| **H1 — granularity ceiling** | lift is **non-uniform and ordered by granularity demand**: ~flat on fine-grained single-file implementation, large on false-premise / judging / multi-concern |
| **H2 — uniform capability** | roughly constant % lift across all task classes |
| **H3 — approval bias (training)** | lift everywhere **except** judging, which stays flat or lifts far less than other coarse-granularity classes |

**The suite is already the right instrument.** `01-use-cases.md` P4 notes it
cannot measure the wanted projects — true, and irrelevant here. It has trap
classes spanning a real granularity range and `stresses` slices that already
behave like an indirection-count proxy (cross-file: monolith 0.47 / dloop 0.92).
It was built to separate *pipelines*; it turns out to separate *hypotheses about
capability*, which it was not designed for.

That reverses the sequencing worry: **run the sweep on the existing suite first.**
It is cheap, the apparatus exists, and its result determines whether route (b) in
Consequence 2 is worth building.

## The weakness

**"Granularity" is not yet operationalised**, and until it is, the hypothesis is
close to unfalsifiable — any failure can be relabelled "that was above the
ceiling."

Candidate proxies, in rough order of tractability:

1. **Distinct entities that must be related** to answer correctly.
2. **Hops of indirection** — already partly measured by the `cross-file` slice.
3. **Heterogeneity of context types** — code only, vs code + intent + test +
   history. The judging seat is the extreme case, and this is the proxy the
   hypothesis leans on hardest.
4. **Counterfactual depth** — whether answering requires holding "what would have
   been true otherwise." Judging and false-premise detection both need it; doing
   does not.

A pre-registered granularity ranking of the 30 suite tasks, written **before** the
sweep runs, is **necessary but not sufficient**. Without it the sweep can be read
as confirming H1 whatever it shows. With it, the hypothesis is still not yet
falsifiable — see the audit below.

## The instrument — a ceiling probe

The suite ranking makes the sweep interpretable. It does not measure **how high
the ceiling is**, and the suite cannot be made to: it varies trap and request
shape, never granularity systematically, and it tops out well below the range the
wanted projects live in.

That needs a second, purpose-built fixture, and it is a different kind of object
from the M6 suite. M6 compares *pipelines*. This characterises a *model*.

### It sidesteps the operationalisation problem

The instrument does not require an absolute granularity metric. It requires only
that rungs be **monotonically more demanding by construction** — an *ordinal*
scale, not a cardinal one. That is far easier to build and far harder to argue
with.

### Shape: a ladder

N rungs delivering the **same underlying deliverable**, checked by the **same
deterministic check** with the same pass criterion. Only the context demand
varies. Sketch, for a bug:

| rung | what the model is given |
|---|---|
| R1 | the failing function + the failing assertion |
| R2 | the file + the failing test |
| R3 | the module (several files); the suite fails somewhere |
| R4 | the repo + a user's chat message describing symptoms |
| R5 | the repo + three user messages, two describing unrelated problems |

The fix is identical at every rung. What changes is how much has to be related
before the fix is even locatable. **Ceiling = the rung where pass rate crosses a
stated threshold.** Run per model size and the output is a number per model:
its granularity envelope.

### Multiple ladders — and why the obvious falsification test is confounded

Build one ladder per candidate proxy — an indirection ladder, a
context-heterogeneity ladder, a counterfactual-depth ladder.

The tempting test: *consistent ceiling across ladders → granularity is one
dimension; divergent ceilings → the hypothesis splits.*

**That test does not work as stated.** The ceiling is not flat across domains,
and **model size does not tell you what tuning was applied** — tuning reshapes
the ceiling dramatically in specific areas. A code-tuned model will clear a
code-shaped ladder further than a prose-shaped one for reasons that have nothing
to do with granularity being multi-dimensional. Divergence is therefore *expected*
and evidences nothing on its own.

Recovering the test needs a second axis: **tuning, not just size.** Compare the
*pattern* of ladder divergence across models with different tuning —

- divergence that **tracks the tuning domain** → a tuning artifact;
- divergence **stable across differently-tuned models** → genuinely dimensional.

Consequence for the sweep: the design is **size × tuning**, not size alone. That
raises the number of model points needed, and it is the correct cost.

### Precedent and prior

This is **M0 for cognition**. M0 characterised the inference envelope — tok/s,
context, the VRAM cliff — because you cannot design within an envelope you have
not measured. The same argument applies here, and the same shape question
follows: M0 found a **hard binary** with a ~10–20× cliff. Whether the cognitive
envelope has a cliff or a gradient is OQ-3, and M0 is a reason not to assume
gradient.

A ceiling probe also has a property the M6 suite lacks: it is **model-facing, not
pipeline-facing**, so it stays valid as pipelines change, and it is the natural
thing to re-run against every new model that arrives.

## Is the hypothesis falsifiable? — an honest audit

**As currently stated: no.** It is a productive *lens*, not yet a theory. Four
reasons, stated plainly so they are not quietly forgotten.

1. **"Principally" is a weasel.** *"Size governs principally the granularity…"* —
   principally how much? Unquantified, therefore unfalsifiable by construction.
2. **The retro-explanation proves nothing.** The seven-row table fitting the
   findings is *suggestive*, not evidence. It was written knowing the findings;
   post-hoc fit is cheap, and a framework that explains everything after the fact
   risks nothing. It generated no prediction it could have failed.
3. **The tuning confound is an escape hatch — one accepted on purpose
   (2026-09-04).** Conceding that tuning reshapes the ceiling was correct, and its
   unfortunate consequence is that *any* non-conforming sweep result can now be
   attributed to tuning. That made the hypothesis harder to kill, not easier.
4. **The ladder absorbs its own disconfirmation.** Non-monotonic pass rates within
   a ladder *should* falsify the ordinal construction — but the standing
   temptation is to call it bad rung design and rebuild. Classic Duhem–Quine: the
   auxiliary hypothesis takes the hit and the core survives untouched.

### The null being dodged

The boring alternative has not been taken seriously anywhere above: **harder
tasks are harder, and bigger models do harder things.** True, uninformative, and
it accounts for every observation the granularity story accounts for. Granularity
has to predict something *difficulty does not*, or it is a vocabulary rather than
a claim.

### Four moves that would make it testable

Cheapest and riskiest first.

1. ~~**The removal test.**~~ **Withdrawn (2026-09-04) — not a risky prediction.**
   "Removing true but irrelevant information improves performance" is not weird,
   it is near-certain, and `10-foundations/04` already asserts it as doctrine
   (*"relevant context beats maximal context"*). A falsifier the design set
   already claims is not a falsifier. Replaced by:

   **The grain-match test.** The correction that makes it risky came from the
   Rubik's-cube case: *a finite model with infinite context cannot solve the cube
   from the position of each of its atoms.* Every bit of information is present,
   losslessly — and useless, because it is at the wrong **grain**. That is not an
   argument about *amount* of context. It is an argument about *level*, and the
   two come apart.

   So control for amount and vary only level:

   | arm | context |
   |---|---|
   | **A** | fine-grained, *N* tokens, provably sufficient to answer |
   | **B** | coarse-grained, *N* tokens, same information pre-abstracted, provably sufficient |

   Same task, same check, token-matched, sufficiency-matched.

   - **Grain account predicts:** B > A, and the margin grows with the task's grain
     demand.
   - **Noise-reduction null predicts:** A ≈ B — it was only ever about how much
     irrelevant material was in the window.

   If A ≈ B, the whole hypothesis collapses into "relevant context beats maximal
   context" wearing a hat, and should be retired to that sentence. **This is the
   discriminator the audit was missing.**

   Note it also prices the scaffold directly: arm B requires *someone to have
   produced the abstraction*, which is the Principia authorship constraint (OQ-7)
   showing up as an experimental cost line.

   **Caution:** the cube is an extreme case with an enormous gap. An existence
   proof at the extreme does not establish that the effect matters at the modest
   gaps found in real work. The test must run at realistic gaps to say anything
   useful.
2. **Forecast, don't fit.** Pre-register the granularity ranking of the 30 suite
   tasks, then predict *which tasks an unseen model newly passes*. If the newly
   passed tasks are distributed randomly across the ranking, falsified. This is a
   real forecast against fixtures that already exist.
3. **Cross-ladder correlation.** If granularity is one dimension, a model's
   ceiling rung on ladder A predicts its rung on ladder B, controlling for tuning.
   No reason those correlate if there is no such dimension.
4. **Kill "principally."** Restate quantitatively: *granularity rank explains more
   variance in per-task outcome than task length, trap class, or request shape.*
   That is a regression, and it can lose.

**Pre-commitment is the part that costs something**, and therefore the part that
matters: the rung ordering and the monotonicity tolerance must be fixed in
writing *before* data exists, with an advance commitment not to rebuild the
ladder if it fails.

### What survives either way

The instrumentation is separable from the theory, and it earns its keep even if
the theory is empty: the **ladder**, **rungs as an accumulating unit of
progress**, **partial views** (independently motivated — they also follow from
approval-bias), and **a stopping rule for decomposition**. All four remain useful
if the granularity account turns out to be nothing more than a good vocabulary
for "harder is harder."

That is the honest position: **a lens worth keeping, a theory not yet earned.**

## Candidate contribution: replace ADaPT's hand-set depth bound with a measured one

The sharpest concrete output of this thread, recorded because it is small,
specific, and uses apparatus the project is already building.

**The gap.** ADaPT decomposes *as-needed* — try, fail, decompose, recurse — which
is the right control structure and is validated. But it bounds recursion with
`max_depth`, **a hand-set constant.** Every shipped tool is worse still: reactive
budget management with thresholds tuned to the context window rather than to the
task. So the field has, at best, an adaptive rule with an arbitrary bound.

**The move.** Replace the constant with a measured quantity: bound depth by the
**integrated system ceiling** — specifically the aggregation limit — obtained from
the ceiling probe rather than chosen. Decompose as-needed, stop where measurement
says recombination becomes unreliable.

**Why it is a real contribution rather than a restatement:** over-decomposition is
a documented failure (ARIES: 4.12× on one synthetic task, aggregation-dominated;
ADaPT: `max_depth` is hand-set) whose current mitigation is *"set a max depth and
check whether decomposition adds value"* — i.e. a magic number and an unspecified
check. A calibrated bound converts both into measurements. The hypothesis is that
**initial calibration plus an evidence-based feedback loop addresses
over-decomposition**, and it is genuinely open whether it does. Note the
motivating evidence is thin — one narrow-domain multiplier plus a mechanism
argument — so the contribution stands on the *method* being sound, not on the
failure being well quantified.

**What it depends on, in order:**

1. the grain-match test surviving (else "granularity" is noise-reduction wearing
   a hat, and there is nothing to calibrate);
2. **an end-to-end turn point** — the depth at which returns go negative for a
   given model + scaffold + task class, measured directly. Deliberately *not* a
   mechanism: per the standing assumption, no claim is made about which
   operation binds, and none is needed. Knowing **where** suffices to replace a
   `max_depth` constant; knowing **why** would be a separate result requiring
   separability the literature has not licensed;
3. **that turn point being stable** across tasks within a class. This is now the
   **single point of failure.** With no mechanistic account, the bound cannot be
   extrapolated — it must be re-measured whenever model, scaffold or task class
   changes. If it also has to be re-measured per *task*, the calibrated bound
   costs more than the magic number it replaces and the contribution collapses
   outright. Check this second, immediately after the grain-match test, because a
   negative result here ends the line cheaply.

Each is a way this fails, and they should be checked in that order.

## Open questions

- **OQ-1 — Which proxy?** Pre-register one (or a stated combination) and rank the
  30 tasks before any sweep data exists.
- ~~**OQ-2 — Is the ceiling a property of the model, or of the
  model-plus-context-assembly?**~~ **Dissolved (2026-09-04)** — it was a
  definitional choice, not an empirical question. Replaced by the bare /
  effective / lift convention above. The empirical residue is settled anyway:
  assembly moves the effective ceiling a great deal near the limit, and the suite
  already shows it — dloop's retry-with-failing-lines takes the cross-file slice
  from 0.47 to 0.92 at fixed model size. Context governance (M9) is a leverage
  milestone, not a measurement chore.
- **OQ-2b — Does assembly *raise the ceiling*, or *lower the task's demand*
  beneath an unchanged one?** The refinement that matters, because it decides
  whether route (b) in Consequence 2 has a hard stop. If assembly only lowers
  demand, any task with an **irreducible granularity floor** above the ceiling is
  out of reach for that model however good the tooling.

  **Partly resolved (2026-09-04), via an unexpected precedent.** *Principia
  Mathematica* spends several hundred pages reaching `1+1=2`. It is the existence
  proof that a question which looks atomic **does** decompose arbitrarily far —
  so "irreducible floor" is probably the wrong shape. What is real is
  **decomposition cost**, which can explode combinatorially; "unreachable"
  becomes "reachable at a price," and prices are measurable and can fall.

  But the same precedent locates a floor somewhere better: **Russell and
  Whitehead had to already know where they were going.** The decomposition of an
  above-ceiling question cannot be authored from below the ceiling. So the
  constraint is not on the task — it is on **who writes the decomposition**.

  This is the same asymmetry as `01-use-cases.md` P7, arrived at independently:
  something above the ceiling authors the ladder, once; everything below climbs
  it thereafter. The coarse-view cost is paid a single time and the artifact is
  **reusable**, which is what makes route (b) viable rather than merely possible.

  Restated: *a model cannot decompose its own above-ceiling tasks — but it does
  not have to, if someone else's decomposition is on the shelf.*
- **OQ-3 — Is the ceiling sharp or soft?** A cliff and a gradient imply very
  different firing rules. M0 found a hard binary in VRAM fit; no reason to assume
  the same shape here.
- **OQ-4 — Does the ceiling move with task *familiarity* rather than structure?**
  A confound: coarse-granularity tasks may simply be rarer in training data.
  Hard to separate without controlled fixtures.
- **OQ-5 — How many partial views, and who writes them?** Fixed hand-authored
  view templates, or view selection as a decision the system makes per task.
- **OQ-6 — Which ladders, and on what basis?** *Deliberately not chosen yet
  (2026-09-04).* Ladder selection is gated on three inputs that do not exist yet:
  **feedback from actually using the tool**, a **review of how state-of-the-art
  benchmarks are composed**, and a **literature pass**. Picking ladders now would
  settle by intuition what those inputs exist to settle. This makes the ladder
  work downstream of `01-use-cases.md` §2–§3, which are still empty.
- **OQ-7 — Decomposition authorship as a cost centre.** If authoring a
  decomposition merely requires operating above the target's *effective* ceiling,
  the authorship constraint is a **resource question with substitutable
  suppliers**, not a mystery: a human (decent, costly), a capable model (fast,
  cheap, must be reachable), or a previous scaffold generation (free once built).
  The quantity to compare is **cost per rung of lift, by author type**. P7's claim
  is that the middle supplier is becoming the cheapest.
- **OQ-8 — Ladder output as calibration input, not just measurement.** A measured
  effective ceiling makes Consequence 1's firing rule operational: *decompose when
  estimated demand exceeds the measured ceiling* becomes a comparison of two
  numbers rather than a hand-set heuristic. This is the path by which the
  instrument feeds M7 directly, and it is a stronger reason to build it than
  measurement alone.

## Predictive gating: an activation-based difficulty predictor

**The proposal.** Within a single configuration (one model + one interface —
transfer explicitly set aside): run the probe benchmark, record activations,
identify the signatures associated with success and with failure, then scan a
*new* task for those signatures and **decline or decompose it before attempting
and failing.**

### Why this is worth more than difficulty estimation

It converts the decomposition rule from **reactive to predictive**. ADaPT
decomposes *on failure* — it pays a failed attempt to learn that depth was
needed. A working predictor skips that payment. That is strictly better whenever
the prediction is cheap and accurate, and it is the firing rule
`01-use-cases.md` OQ-9 and Consequence 1 have both been circling.

There is precedent for the mechanism: probing classifiers over hidden states are
used for hallucination detection and uncertainty estimation, and frequently
outperform the model's own verbalised confidence. Reason to expect signal, not a
guarantee of it.

**The economics are favourable and get better with scale.** The scan is a partial
forward pass; the attempt is a full agentic loop with tool calls and retries. The
ratio improves the more expensive the task — so it pays most precisely where
failure costs most.

### The crux: how far into the attempt must you go?

"Before attempting" is a spectrum, and this is the central design question
because it is both decisive and cheaply answerable:

| scan point | cost | likely signal |
|---|---|---|
| **prompt only**, before any generation | lowest, genuinely pre-attempt | the model has not engaged the problem; may encode little about difficulty |
| **after a short generated prefix** | still far below a full attempt | the model has begun reasoning, so activations reflect engagement — likely the useful regime |
| after a full attempt | none — defeats the purpose | — |

**The empirical question: how deep must the prefix go before prediction becomes
reliable?** Well-posed, and answerable directly from the benchmark run.

### Scanning many stages — the dart problem and its fix

*"Throw a hundred darts and you'll hit the spot eventually; doesn't mean you have
good aim."* Correct, and it is the **multiple-comparisons / selection-on-test**
failure: scan ten stages × many layers × many token positions, pick the best
predictor, and something will look good by chance.

**The fix is standard and cheap.** Searching a large space is legitimate; what is
illegitimate is letting the final estimate come from data that participated in
the search. So: a **held-out test set never touched during selection**, and
**nested cross-validation** if scan point or layer is being chosen — the
selection must happen inside the inner loop or it leaks.

**And there is a positive criterion worth more than the negative one — flagged as
a keeper, pending whether it holds:**

> **Shape of the search space beats maximum of the search space.**
> Do not only look for the best predictor; look at whether predictive power
> varies **smoothly and interpretably across scan points** — rising as generation
> proceeds, peaking at a consistent layer, degrading predictably. **Noise does not
> do that.** One dart in a hundred is chance; a gradient across the whole board
> is structure.

Stated generally because it is not specific to activation probing: wherever a
large configuration space is searched, the *structure* of results across that
space is stronger evidence than the best result in it. Candidate for promotion to
the design set if it survives contact with data.

### Where prompt-only probing should be expected to fail — and why that is predicted

The intuition that prompt-only scanning is fragile — *obvious connections
dominate, weak signal reads as noise, and the subtle difference is exactly what
distinguishes a bad answer that looks good* — is sound, and it has a sharper
form. It also extends to later stages: a confidently wrong answer plausibly looks
confident in activation space too.

**But the failure is not uniform, and this project has already located its
boundary.** Internal-state probes sometimes beat verbalised confidence precisely
because representations can encode uncertainty the output does not express. So
probing should work where the model is *uncertain* — and fail where it is
**confidently wrong**, because there is no uncertainty to detect.

Which is the census result: **3/3 implement an impossible O(log n); 0/3 flag it.**
The model was not straining. It was wrong, comfortably. **A probe has nothing to
find there**, and this predicts the technique's blind spot in advance rather than
discovering it later:

**Corrected (2026-09-04): the blind-spot argument applies to one *probe target*,
not to probing.** It assumed the thing being detected is the model's **epistemic
state** — and confident wrongness is precisely the case where that state contains
nothing. But the context-pathology proposal targets something else: **properties
of the input**, which exist whether or not the model noticed them.

~~**An overloaded context is overloaded regardless of the model's confidence.**~~

**Corrected again (2026-09-04) — overload is a relation, not a property.** The
sentence smuggled in a model-independent notion of overload. There is none. A
context becomes overloading *when a given model cannot handle it*: the `grep`
manpage is unremarkable for a large model and overload for a 7B. **Same input,
different verdict.**

This is the identical objection already applied to *window oversize* in the table
below — and the two rows are therefore the same row. The document reclassified one
and left its neighbour standing on the reasoning it had just rejected.

**What survives, and why it is stronger.** *Model-relative* is not *model-reported*.
A probe reads **this model's** internals on **this** input, so it measures the
relation directly — it never needed overload to be an input property. If anything
the corrected framing is better posed: a relation measured from one side of itself
beats a model-independent quantity inferred indirectly.

**What the correction actually costs is portability**, and that is a real
practical consequence rather than a wording fix:

- an overload label is valid for a `(model, context)` **pair**, never for a
  context alone — so contexts cannot be annotated once and reused as fixtures;
- probes must be **trained per model**, and a probe transferring across models is
  a hypothesis to test, not an assumption to build on;
- "effectively oversized" and "overloading" both reduce to **the ceiling being
  crossed**, which is what the neighbouring row already concluded.

**And "confidence" was doing two jobs.** Separating them is what makes the
original claim recoverable:

| what is meant | reliability | is it the probe target? |
|---|---|---|
| **verbalised confidence** — the model states it is sure | poor. The judge-lab null and approval bias are exactly this | **no** |
| **epistemic state** — difficulty represented internally as uncertainty (entropy, logprobs) | real signal **where uncertainty exists**; absent under confident wrongness | partially |
| **processing state under load** — dispersed attention, representation norms | present whenever the model is *struggling*, whether or not the struggle is represented as uncertainty | **yes — this is the target** |

The defensible version of the original sentence is therefore:

> **Load shows in processing regardless of whether the model represents that load
> as uncertainty.**

Which keeps the M4 case — a processor that did not notice it was missing a file
and proceeded anyway — as a target rather than a blind spot, without claiming
anything model-independent. The blind spot stays where the last correction put
it: **semantic** falsity, not confident wrongness as such.

The line that actually holds is therefore not confident-vs-uncertain, but
**structural vs semantic** — with "structural" now understood as *structural
relative to this model*, not intrinsic to the text:

| probe target | example | expected signal |
|---|---|---|
| ~~**input structure** — overload, dilution~~ **model-relative, like oversize** | "too much" heterogeneous context — *too much for whom?* | **present**, and independent of model **awareness** — but not of model **capacity**. Merged with the row below: both are the ceiling being crossed, read from the model's side |
| ~~**input structure** — window oversize~~ **model-relative, not structural** | context beyond *this model's* usable extent | **reclassified** — oversize is a relation between input and capacity, graded and model-dependent. "Effectively oversized" is the ceiling being crossed, so this row is not a cheaper target but the same one restated. See the correction above |
| **input structure** — missing context | a needed referent absent | **weaker.** Absence has no direct signature; it is visible only through consequences (unresolved reference, ungrounded generation). If the model confidently confabulates the gap, this collapses back toward the blind spot |
| **model epistemic state** — strain, confusion | task near the boundary | **present** where uncertainty exists |
| **semantic falsity of the input** — false premise | an impossible O(log n) | **absent.** Detecting it requires evaluating the premise against domain knowledge — the judgement the census showed failing 0/3. Nothing structural distinguishes a false premise from a true one |

**Summary of the corrected boundary: structural properties of the context are
probe-visible; semantic truth of the context is not.** Confident wrongness only
blocks detection when the cause is semantic. Two of the three targeted
context-pathology classes are unaffected; the third, missing context, is
genuinely harder and should be expected to be the weakest of them.

### Better-posed target: context-pathology failures, not failure in general

The proposal is **not** premised on failure being homogeneous. It targets a
specific class expected to carry stable signatures:

- **context blur** — too much, diluted;
- **window oversize**;
- **missing context** — a needed referent absent.

~~These are plausibly the most detectable failures available, because they are
properties of **input structure** rather than of semantic difficulty — more
mechanical, less dependent on the model understanding anything.~~

**Wrong, corrected 2026-09-04.** "Window oversize" is **not an input property.**
*Token count* is an input property; **oversize is a relation between the input and
a particular model's capacity**, and it is **graded**, not binary — the same
context is comfortable for one model, marginal for another, and for a third
degrades to *"he asked something about documenting something somewhere. Can't
remember, probably not important. Skip."*

Two consequences, and the first undoes an earlier conclusion:

- **It is not an easier target.** "Effectively oversized for this task" is
  *definitionally* the ceiling being crossed. A probe for it is not detecting a
  structural property that sidesteps the hard question — **it is detecting the
  hard question.** The claim that context pathology is cheaper to detect because
  it needs no understanding does not survive.
- **But the failure has a shape, and it is already measured behaviourally.**
  Degradation is not loud failure; it is **selective silent omission, biased
  toward dropping low-salience requirements.** This project has the behavioural
  evidence already: M5's workflow suite — *"monolith drops docs+TODO under load
  (wf6: 0/4, 0/3)"* — is exactly *"probably not important, skip."*

**Which suggests a better-posed probe target than the one above.** Not *"is this
context oversized?"* — a global, graded, ill-defined question — but:

> **Which requirements are still live in the model's state, and which have gone
> dark?**

Per-requirement rather than per-context, and **actionable in a way the global
version is not**: knowing *what* was dropped means it can be re-surfaced, split
out, or given its own pass. It also targets a failure the project has already
observed and not yet addressed.

*Caveat on mechanism:* attention weights are not a clean importance measure and
there is a standing literature against reading them as explanation. "Requirement
has gone dark" needs a representation-level operationalisation that does not rest
on attention-as-salience, and finding one is part of the work rather than an
assumption.

**And one of them addresses a standing M4 finding directly.** Per
`10-foundations/04`: a processor could emit a context request and the runtime
would record it, and the affordance *went entirely unused across 16 runs,
including on a task deliberately starved of a needed file.* The conclusion drawn
was that being able to ask is not enough — the behaviour must be prompted or
required.

**External detection is a third option that was not on the table then: do not ask
the model to notice it needs more. Detect it externally.** And on inspection the
design space is four options, not two — with the cheapest one requiring no
activations at all.

#### The M4 case decomposes, and most of it is deterministic

"Missing context" was earlier classed as the weakest probe target, because absence
has no direct signature. That holds for the *global* question. But the M4 setup —
a task deliberately starved of a needed file — is not the global question. The
model must then write code touching something it cannot see, so it confabulates
an interface or emits a reference it cannot ground. **That produces a specific,
locatable artefact**, and it splits:

| kind of gap | detection |
|---|---|
| **syntactic ungroundedness** — an import, identifier, path, or API referenced that was never in the provided context | **deterministic and cheap.** No probe. A symbol check against what was actually supplied |
| **semantic gap** — a needed convention, constraint, or prior decision, with no syntactic trace of its absence | **hard.** This is where probing might earn its place, and it is the weakest target |

**A large part of the M4 case is the first row**, which means it is a grep, not a
research programme. That is also the project's own doctrine applied consistently:
the judge-lab found a deterministic gate scoring 9/10 alone and 6/10 once a 7B
panel was added. Prefer the deterministic check wherever the question admits one.

#### Four options, and the right order

| # | option | status |
|---|---|---|
| **a** | make the affordance available and hope it is used | **failed, measured** — 0 uses in 16 runs |
| **b** | prompt or require the request | the M4 conclusion; **untested** |
| **c** | **detect ungrounded references in the output, deterministically** | **new, cheap, covers the syntactic bulk** |
| **d** | probe representations for semantic gaps | covers the residue; hardest and weakest |

**Order: c → b → d.**

And **c is strictly more robust than b against the failure actually observed.**
Requiring the model to ask still requires it to *notice* — which is precisely what
it failed to do. Detection requires no noticing.

**c is also architecturally in place already.** The runtime records context
requests but does not inspect outputs for ungrounded references. That check is
gate-shaped and sits naturally in the existing M3 enforcement path
(`10-technical/04`): under `10-foundations/02`, the runtime is entitled to refuse
an effect that references something never supplied. It is a runtime
responsibility, not a cognitive one.

**This is the most immediately actionable item in the thread** — it needs no
ladder, no φ, no activations, and it answers a finding that has been open since
M4.

**Expansion discipline:** start with the class that has a plausible signature; add
further classes only as each earns its place against measurement; let the ones
that do not, die in the loop.

**Highest-value application: recombination.** Aggregation is the binding
constraint on the integrated system ceiling, and failed recombination is
frequently *too much heterogeneous context* — which is the context-blur signature.
**The context-pathology detector is therefore plausibly the recombination gate**,
which makes it the first place to point this rather than an incidental one.

### Four problems, in order of severity

1. **Selective labelling — the worst one.** Train a predictor on "did it fail,"
   then use it to *avoid attempting*, and you **never collect outcomes for the
   tasks you skip.** The training distribution collapses onto the tasks still
   being attempted, and the predictor degrades in exactly the region it governs.
   This is the classic feedback-loop failure (credit scoring never learns whether
   rejected applicants would have repaid). **Mitigation is mandatory, not
   optional: always attempt a fraction of predicted-failures and log them.**
   Budget for it explicitly.
2. ~~**What is the label?**~~ **Deferred deliberately.** Distinguishing *this
   attempt will fail* (a retry/decompose policy) from *this will fail under every
   scaffold* (an escalate-to-human policy) matters for deployment, not for the
   first look. **Observe correlation first; see whether a threshold appears at
   all.** Use single-attempt pass/fail because the benchmark run already produces
   it, and refine the label only if there is something to refine.
3. ~~**Does failure have a stable signature?**~~ **Reframed** — see the
   context-pathology section above. The question is not whether *failure* has a
   signature but whether **specific failure classes** do, starting with the ones
   whose cause is input structure rather than semantic difficulty.
4. **The predictor is configuration-bound — reframed as modularity rather than
   limitation.** It must be measured **per role**, at a defined position in the
   harness, with a stated view of what lies in front of it. That makes it a
   **composable brick** rather than a global property, and it fits the existing
   processor/role architecture (`10-technical/06`) without modification: each
   role gets its own gate, trained on that role's inputs.

   The exposure remains and is worth stating in its nastiest form: **a harness
   change invalidates the predictor silently**, because it will go on emitting
   confident predictions against a distribution it no longer models. Any
   deployment needs a binding between predictor and harness version.

### The unification, and its limit

A predictor learned from activations **is a candidate φ** — the projection
*learned* rather than designed, which sidesteps the problem of choosing features
by intuition.

**But prediction and characterisation are different goals, and this serves one of
them.** A black-box classifier yields a firing rule and no account of *how many
dimensions* there are. It cannot answer the question this thread opened with.

**Partial bridge — offered too confidently, corrected (2026-09-04).** The claim
was: if failure signatures **cluster** into *k* patterns, that is evidence for *k*
failure modes.

**It is not. Cluster count is not cause count**, and the mapping from latent
causes to observable signatures is not guaranteed in either direction:

- **One cause → many signatures.** A single skill saturating produces whatever
  the *rest* of the system does in its absence — and that fallback varies with
  task family, available context, and what else the model can reach for. The
  signature is **the shape of the compensation, not the shape of the deficit.**
  One saturated skill can therefore present as several distinct patterns.
- **Many causes → one signature.** Different underlying failures plausibly
  converge on the same observable mode: give up, produce something plausible.

So clustering yields the number of **observable modes**, which relates to the
number of latent causes only under assumptions not established here. **Whether
two distinct failure patterns share cognitive geometry is unknown, and treating
cluster count as cause count assumes the answer.** This is the identifiability
problem from earlier in the thread, relocated one level down rather than solved.

*Noted because it is the second instance:* the two-pole ceiling decomposition and
this both presumed a **clean mapping from observable structure to latent
structure**. Same error twice, and worth watching for a third time.

**What would actually help: induce the stress rather than observe the failure.**
Clustering unlabelled failures is correlational. Deliberately *causing* a known
stress and recording the resulting signature is causal, and it maps
**known-cause → signature**, which is the direction identifiability needs.

**The apparatus for this already exists.** The M6 suite is **trap-structured** —
its tasks are built around named failure-inducing structures, with `stresses`
tags. So the experiment is: *for each trap class, which signature appears?* That
is strictly stronger than clustering, and it measures the mapping's real
structure instead of assuming a bijection:

| observed | means |
|---|---|
| trap A → signature 1, trap B → signature 2, consistently and without crossover | evidence for distinct causes with distinct geometry |
| trap A → signatures 1, 2, 3 depending on task family | one cause, many fallbacks — the signature space is **finer** than the cause space |
| traps A and B → the same signature | the signature does not distinguish them; the channel is **coarser** than the cause space |

All three outcomes are informative, and none requires assuming the mapping is
one-to-one. This supersedes clustering as the first analysis to run.

## Hanging state (2026-09-04)

Session close. What the thread now holds, what it is waiting on, and in what
order to attack it.

### Where the reasoning stands

1. **The hypothesis is a lens, not a theory** — the falsifiability audit stands,
   and its one live discriminator is the **grain-match test** (token-matched,
   sufficiency-matched, coarse vs fine).
2. **"Ceiling" is a 1-D approximation** of a region boundary in a task-feature
   space. Ladder divergence is boundary shape, not confound.
3. **The prior goal is construct validation, not ceiling measurement**: does a
   task set measure one coherent thing, and is it the thing it was named for?
4. **This is latent-variable inference**, with an existing literature — IRT,
   cognitive diagnosis modelling, Q-matrix identifiability.
5. **φ maps tasks → feature space; capability is the region** a configuration
   succeeds in. φ is built **at the deployment configuration level** (accepted
   methodology constraint; does not transfer across harnesses).
6. **Three observation channels**, in increasing richness and cost: outcome
   (Fisher-limited at the extremes), process (Fisher transfers *given a
   likelihood*; modelling burden), white-box (richest; raw coordinates
   model-bound — **the claim that relational structure nonetheless transfers via
   RSA / anchors is ⚠️ UNREVIEWED**, see the marker in the white-box section.
   Until it is discussed, the safe reading is the earlier one: white-box output
   is model-bound and the channel's value is unresolved).
7. **Items are cheap; checks are the bottleneck.** Two populations with different
   design targets — **anchors** (hard, conjunctive acceptable) and **diagnostics**
   (mid-difficulty, one demand varied at a time).
8. **Cross-model convergence of relational structure is a validity check** for φ
   that behavioural data alone cannot supply — provided the models come from
   genuinely different lineages.

### Scope boundary drawn this session

**Pipeline engineering for white-box collection — storage strategy, sampling,
projection-at-collection, contraction-graph optimisation — is out of scope for
this thread and belongs to a separate project.** This thread produces the
*general strategy* only. That project is activated **only if** the strategy is
first shown to be sound, which means at minimum OQ-A and OQ-C below returning
positive. Nothing here should be blocked on it.

### Open questions, in the order to attack them

Cheapest and most decisive first. The first three are independent of each other
and any of them can kill or reshape the rest.

| # | question | cost | why it comes first |
|---|---|---|---|
| **OQ-0** | **Ungrounded-reference detection.** Check outputs for imports, identifiers, paths and APIs never present in the supplied context; refuse or flag at the gate | **lowest — no new apparatus** | Answers the M4 context-request finding, open since then. Needs no ladder, no φ, no activations. See "Four options" above; strictly more robust than requiring the model to ask, because it does not require the model to notice |
| **OQ-A** | **Does the M6 suite measure anything coherent?** Internal consistency; do the `stresses` tags correspond to any factor structure? | **low** — may be answerable from runs already recorded | A task set is not a benchmark until this is shown. If M6 has no coherent structure, everything built on it inherits that |
| **OQ-B** | **What does the identifiability literature license?** IRT / cognitive-diagnosis results on when latent structure is recoverable, and how many items and subjects it takes | **low** — reading | It is the prerequisite the standing assumption explicitly defers to, and it may settle the skill-separability question from outside |
| **OQ-C** | **Does the grain-match test survive?** Token-matched, sufficiency-matched, coarse vs fine | low | The single discriminator between a theory and "relevant beats maximal" in a hat. Everything downstream assumes it |
| **OQ-D** | **Does any candidate φ separate M6 passes from failures better than chance**, using features computable in advance? | low–moderate | The cheap test for whether capability compresses at all. A negative closes the line before ladder work |
| **OQ-E** | **Is the turn point stable** across tasks within a class, per model+scaffold? | moderate | **Single point of failure** for the ADaPT contribution. Check immediately after OQ-C |
| **OQ-F** | **Can generated items avoid contamination?** Multi-model generation, human-authored subset, independent-provenance validation | moderate | Determines whether the item set can be grown without the factor structure becoming an artefact of the generator |
| **OQ-G** | **Is the white-box channel worth activating?** | gated | Depends on OQ-A and OQ-C; triggers the separate project above |

### Resume here

**The model-specificity correction is unreviewed** — written after the other
party had already responded to the superseded claim, so it has had none of the
scrutiny that improved the rest of this thread. It is the natural place to pick
the discussion back up, and until it is settled, **OQ-G stays gated on a question
that is itself unresolved** rather than merely deferred.

### Carried from earlier, unchanged

- The **standing assumption**: the ceiling does not decompose into separable
  operations; treat it as unitary unless the literature (OQ-B) says otherwise.
- The **objective-dissolution** ("tangential success") and **aggregation**
  failure modes, and the integrated system ceiling they required — with the
  first now held as argument, not as evaluated prior art (2026-09-05).
- The **circularity warning**: never report a dimensionality estimate from a
  self-generated population without saying so.

## Output

_On close: where this thread's conclusions went._
