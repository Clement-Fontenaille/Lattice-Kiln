# Meta-Level Feedback

## TL;DR

The meta loop does not merely improve the improver. It evaluates whether our way of discovering improvement is trustworthy.

> **Motto:** Audit the mechanism that decides what "better" means.

## Motivation

A feedback system can optimize the wrong metric, reward superficial behavior, overfit benchmarks, or repeatedly propose changes that appear beneficial only inside one running instance.

The meta level exists to detect these failures.

## Object of evaluation

The meta loop observes the system-level adaptation process itself.

It asks whether experiments are meaningful, metrics remain aligned with developer value, candidate improvements transfer to independent instances, regressions are detected, and promotion decisions remain reproducible.

## Expected outputs

The meta level may propose changes to benchmark composition, evaluation procedures, experiment design, repetition requirements, promotion criteria, regression testing, or the architecture of the feedback loop.

## Deliberate boundary

The meta loop is not expected to recursively spawn an infinite hierarchy of meta-meta systems.

Its purpose is pragmatic: increase confidence that system evolution is real rather than self-confirming.

Three things keep the boundary from being merely asserted.

The loop asks one generic question — whether the system's self-tuning produces trustworthy improvement in aggregate — rather than a separate meta-question per tunable parameter. A mechanism that can propose changes to a processor's instructions can equally propose changes to its own thresholds; that is self-application of an existing mechanism to a new object, not grounds for a dedicated overseer per parameter.

The chain terminates on something not self-tuned. Frozen baselines and the invariant layer sit outside every loop being judged, which is what prevents the tower from quietly moving its own goalposts.

That termination is less complete than it reads. A frozen baseline fixes the task; it does not fix the accumulated record the system consults while performing it, and that record is an output of the system (`04-goodhart-and-adversarial-evaluation.md`, What a frozen baseline does not freeze). The invariant layer is genuinely outside every loop. The evidence this level reads is not.

The answer is not a better anchor. It is that this level accepts evidence at several strengths, knows which one it is looking at, and exists to make the strongest one reachable.

## Levels of evidence, and what this loop is for

Four, weakest first. None is dismissed; the point is to know which is in hand.

**Self-report during operation.** The system's account of how it did. Self-confirming by construction, and this project already has evidence against leaning on it — Milestone 5's orchestrator recorded why it acted at each step but usually not why it judged the work done.

**Within-lineage comparison.** Two configurations compared over the corpus their joint operation produced. Cheap, valid on its own terms, and the framework's working measurement (`23-arch-context-management/02-context-as-experimental-surface.md`). Still underwritten by conditions the audited system shaped.

**Transfer.** A configuration evaluated against material it did not shape. Stronger, because one side of the measurement is outside its reach. This is what "whether candidate improvements transfer to independent instances," above, actually asks for.

**Extraction into predefined scenarios.** The configuration instantiated fresh, without the corpus it accumulated, and run against scenarios defined in advance and independently of anything it produced. Strongest available, because neither the task nor the informational state was shaped by what is being judged.

Making that last level reachable is what this loop is for. It is the expensive one, which is why the others are not dismissed — a level that can only be afforded rarely cannot be the only one a system is watched by.

**A warning about the word "strongest."** This gradient is not `10-foundations/03`'s Mode of acquisition and the two point different ways. There, Operated beats Tested because the task was the real task and nothing stood in for it. Here, a predefined scenario beats operated evidence drawn from the optimizing instance, precisely because that operated evidence was generated under the conditions in question. The two answer different questions — *does this work on real tasks* against *is this improvement real rather than self-confirming* — and collapsing them would make a constructed scenario look like a weaker form of the same thing, when for this loop's purpose it is the stronger one.

And this level is distinct from the others in scope and evidence requirements rather than necessarily in which processor performs it. The separation belongs to invocation, not to agent identity.

## Open question

The project must determine which evaluation anchors should remain externally fixed enough to prevent moving goalposts, and which should themselves be evolvable as our understanding of useful performance improves.
