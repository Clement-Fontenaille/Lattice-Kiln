# Next Experiments

## TL;DR

A sketch of what to run next and what each run decides. Ordered by information per
unit of cost, not by appeal.

> **Motto:** Run the arm you expect to lose.

## Standing rule

Every ordering in this document is a **claim, not a schedule**. Running only the
top of a ranked list confirms the ranking without ever risking it, and the
ranking then becomes an unexamined premise.

Where testing the whole set is affordable, test the whole set: the entries
predicted to fail are what make an ordering falsifiable, and the one ranked last
is often the only one that can overturn the framework. Where it is not
affordable, say so and record the ranking as an untested assumption rather than
letting it pass as a result.

## E0 — Is the evaluation suite measuring one coherent thing?

Construct validation of the Milestone 6 suite, before anything else uses it as a
ruler. Standard item analysis: difficulty distribution, item–total correlation,
dimensionality. The failure it looks for is items that do not cohere — a list of
unrelated tasks rather than indicators of anything.

Possibly answerable from runs already recorded. Cheapest item here, and it gates
most of what follows.

## E1 — Can context pathology be detected from processing?

Whether a probe can distinguish a **constructed** stress from its matched control,
using construction rather than outcome as the label. Outcome as a label would make
the probe a failure predictor wearing another name.

**One battery, not four experiments.** Same apparatus, same model, same base
tasks; five stress classes with matched present/absent pairs. The predicted
ordering is fixed in writing before any data exists:

> calculus ≈ contradiction > missing-context > overload > false-premise ≈ chance

**The ordering is the hypothesis**; no single cell is. Two consequences. It
degrades gracefully — a weak apparatus shrinks every score while the ordering may
survive. And the arm ranked last is the most informative: false premise is the
predicted null, and a predicted null returning positive would overturn the
structural-versus-semantic boundary the account rests on.

Two distinct negative results, meaning different things: everything near chance
says the apparatus is broken; everything **equal and above chance** says the probe
detects "something is wrong" generically — a failure detector, not a pathology
classifier.

**Calculus runs first as a positive control** and contributes no evidence about
the hypothesis. If the probe cannot detect arithmetic error, nothing downstream is
interpretable.

## E2 — Does grain matter independently of quantity?

The discriminator for the decomposition account (`22-arch-cognition/08`).
Two arms, token-matched and sufficiency-matched, varying only the level of
abstraction at which the same information is supplied.

If the coarse arm and the fine arm come out equal, the account collapses into
*relevant context beats maximal context* and should be retired to that sentence.
Nobody appears to have run this.

## E3 — A first ladder

A graded series delivering the same deliverable under the same check, varying only
how much has to be related before the work is locatable. Rung ordering and the
tolerance for non-monotonicity fixed in writing beforehand, with an advance
commitment not to rebuild the ladder when it fails.

## E4 — Capability sweep

The existing suite across models. **Size and tuning, not size alone** — tuning
reshapes results unevenly across domains, so a size-only design cannot separate a
capability effect from a tuning artifact.

Gated on E0.

## E5 — Spread across the population

Hold model and scaffold fixed; vary the operator. Two defined arms — the request
verbatim with no configuration, against a hand-authored objective with named
files, stated constraints, and permitted correction.

This measures accessibility rather than capability (`10-foundations/07`), and it
is the only item here that measures the assembly rather than a sub-assembly. The
expert arm must be expert-in-process, not expert-in-this-task's-answer, or it
measures nothing.

## E6 — Corpus digestion (M8)

Feed the `70-THINKING/` literature-review corpus — the F-numbered findings across
topics 07 and 08, the I-numbered ideas register — through `03`'s substrate once a
processor exists to do the ingesting, and ask whether the system holds and
correctly uses knowledge it did not derive itself in the same session.

Gated on [M8](01-MILESTONES/08-persistent-work-and-knowledge.md) having something
to run: small tests first — a processor reuses one stored finding and measurably
beats one starting cold — then the corpus sweep. Not gated on E0–E5; this corpus
and the M6 suite are different instruments for different questions.

This is the first test the "curated memory beats conversational accumulation"
hypothesis (`03-research-and-evaluation-agenda.md`) has had. Graded against
[M9](01-MILESTONES/09-context-governance-measurement.md)'s metrics once those
exist — validity, reliability, pertinence, scope — not against task success
alone, since the corpus was not produced to serve any one task.

## E-corpus — a stand-in for real request traffic

Real facility ticket data is out of reach permanently. A substitute needs the same
shape: natural-language problem reports from non-expert users against a technical
system, with recorded resolutions, mixing real defects, user error, duplicates and
under-specified requests.

Public issue trackers of build and environment tooling are the closest available
match, because build failure *is* largely the user-error class that open-source
trackers otherwise under-represent. Prepared bug-report corpora are cheaper to
start with and less representative. Suite tasks rewritten as vague complaints
serve as a matched control, not a substitute.

## What would make this plan wrong

- **E0 says the suite is incoherent.** Most of the plan loses its instrument and
  reorders around building one.
- **E2 returns null.** The decomposition account retires and E3 loses its
  motivation, though a ladder may survive as a difficulty scale without it.
- **A materially stronger model arrives before E0–E2 run.** The comparisons are
  then against a moving target, and the ageing rules applied to external evidence
  (findings entry 9) apply to this project's own results too.
