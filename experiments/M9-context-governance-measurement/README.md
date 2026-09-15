# M9 — Context governance measurement

Milestone: `docs/00-design/40-roadmap/01-MILESTONES/09-context-governance-measurement.md`
Foundations: `docs/00-design/10-foundations/{03-evidence-belief-and-provenance,04-context-as-governed-resource}.md`

## What's here

| file | package | spec |
|---|---|---|
| (in M8) `context_manager.py::recall/turn_inputs` | 1, 2 | kind-5 turn-input record — landed in M8 since the milestone says it can |
| `failure_modes.py` | 3 | the four failure-mode detectors |
| `claim_dimensions.py` | 4 | validity, reliability, pertinence, scope |
| `test_failure_modes.py` | 3 | exercises all four, including the truncated-flag bug it found |
| `test_claim_dimensions.py` | 4 | exercises all four dimensions and the staleness guard on Scope |
| `less_naive_assembler.py` | 6 | the falsifier: an antistarvation recall policy that moves Insufficiency-visible |
| `test_less_naive_assembler.py` | 6 | naive 9/10 never-recalled vs antistarvation 0/10, same load |

This milestone's own text splits its six work packages: "Packages 1 and 2 are
plumbing and can land with M8. Packages 3 and 4 are the milestone." That's why
the recall trace and turn-input record live in
`../M8-persistent-work-and-knowledge/context_manager.py`, not here — this
directory holds only what M9 itself is about.

## What is real vs. what is a stub, and why each is which

The milestone is explicit that the four failure modes are not equally
checkable, and 03-evidence-belief-and-provenance.md is explicit about which
claim dimensions can be recorded once versus judged live. This build follows
both distinctions exactly rather than treating all eight (four failure modes +
four dimensions) as one undifferentiated "assessment" interface:

- **Overload** — real. "The only content-quality-agnostic one"
  (04-context-as-governed-resource.md): checkable mechanically off the
  turn-input record's own `truncated` flag, no semantic judgement needed.
- **Insufficiency** — real, but only half. The milestone divides it itself:
  material that never crossed is invisible from this store by construction;
  material that crossed but was never recalled is checkable from the live set
  plus the turn-input history. `check_insufficiency_visible` returns only that
  half, with the blind spot named in its own return value rather than left
  for a reader to discover.
- **Redundancy** and **Uselessness** — stub seams. Both need judgement this
  store cannot make (coverage-level overlap for the former, "was this
  actually needed" for the latter). Neither stub may return the clean verdict
  (`not_redundant` / `needed`) — only `unassessed` — for the same reason
  `mandate_check.py`'s stub cannot return `inside`: a stub claiming a clean
  result is indistinguishable afterward from a real check that passed.
- **Reliability** — real, but deliberately not a verdict.
  `reliability_evidence()` reports mode-of-acquisition, second-hand flags, and
  independent-parent-source count (convergence evidence) as facts, with no
  `verdict` field on the returned dataclass at all. 03's own words: "mode of
  acquisition and source are evidence for this dimension, not weights
  themselves." Synthesising a weight from that evidence is the judgement 03
  reserves for a real reasoner comparing claims against each other.
- **Validity** and **Scope** — stub seams, same discipline as Redundancy and
  Uselessness.
- **Pertinence** — stub seam, but its call *shape* is real: 03 names
  pertinence as the clearest case of a dimension that cannot be recorded once
  and cached, because the same claim weighs differently depending on what is
  being decided. `assess_pertinence()` takes `current_objective` as a required
  keyword argument, never reads it off the claim, and nothing in this module
  memoises a result across two different objectives. The test
  (`test_claim_dimensions.py`) asserts that two calls against two different
  objectives produce two different records, which is the property that would
  silently break if someone "helpfully" cached this later.

## A real bug this pass found and fixed (not in M9's own code)

Building `check_overload()` and testing it against a turn where the *labelled*
entries alone already exhausted the turn budget exposed a real bug in M8's
`context_manager.py::recall()`: `truncated` was computed as
`truncated or budget > 0` at the point of the first drop, which is `False`
whenever budget was already at zero or negative before the unlabelled loop
even started — silently reporting `truncated=False` on a turn that had just
dropped twenty-one entries. Fixed to `truncated = bool(dropped)`, the honest
reading of what the field is supposed to mean. All of M8's existing tests
still pass with the fix; none of them had exercised this exact edge (budget
exhausted by anchors alone), which is why it survived until this pass.

## What is deliberately NOT here

- **Package 5, re-grading E6.** Still needs a real processor to do the actual
  ingestion and the real dimension judgements — nothing here changes that.
  What did land this pass: `../M8-persistent-work-and-knowledge/e6_corpus_sweep.py`,
  the sweep harness itself (corpus discovery, the ingestion seam, the sweep
  loop, an incremental-deletion probe, and a pipe into this directory's
  `claim_dimensions.py`), load-tested against the real 70-THINKING corpus (83
  entries). So the "nothing to build against yet" gap is now narrower than
  the whole milestone package — only the `Ingestor` function and the real
  checkers behind `assess_validity`/`assess_pertinence`/`assess_scope` remain,
  and both are the same processor-shaped gap the rest of this README already
  names.
- **Package 6, a less-naive assembler — partially built.** `context_manager.py`
  `recall()` now takes an `order_unlabelled` seam so a second policy can reuse
  everything (persistence, turn indexing, the never-drop-labelled rule)
  except the ordering itself — two policies over the same live set stay
  comparable on exactly the axis that differs. `less_naive_assembler.py`'s
  `recall_antistarvation` is that second policy: unlabelled entries are
  ordered by how often they were previously dropped, so a sustained-pressure
  scenario cannot starve the same tail forever. Measured against the naive
  baseline under identical load, it moved Insufficiency-visible from 9/10 to
  0/10 never-recalled entries (`test_less_naive_assembler.py`) — the
  milestone's own falsification bar, met on this one axis.

  **What this does NOT claim.** Only Insufficiency-visible was moved, and
  the module's own docstring says why the other three failure modes could
  not be, by this or any ordering policy: Overload is a pure volume question
  reordering cannot touch; Redundancy and Uselessness have no real verdict
  yet (stub seams, `failure_modes.py`) for any policy to move. A reviewer
  should read this as "one axis falsified, honestly scoped," not "package 6
  done" — the milestone's bar is broader than what a reordering-only policy
  can ever satisfy, and a real assembler doing semantic curation is still
  unbuilt.
- **Real judgement behind any of the five stub seams** (Redundancy,
  Uselessness, Validity, Scope, Pertinence). All five need a cognitive
  processor (03's "reasoner," 04's semantic coverage comparator) that M9 does
  not build — same boundary M8 held for the mandate check, held again here.

## Reservations / open points for the milestone-close review

- **`_looks_contained`-style placeholders compound.** M9's dimensions sit on
  top of M8's substrate, which already carries known placeholders
  (`experiments/M8-persistent-work-and-knowledge/SUSPECT.md`). A future real
  Scope checker plugged into `assess_scope()` would still be reasoning over a
  `ceiling` string that `work_record.py` never actually validated — worth
  re-checking whether M9's Scope dimension and M8's containment check should
  eventually share one real implementation rather than growing two separate
  stub seams for what is, read closely, the same underlying judgement (does
  X hold within domain/boundary Y).
- **`max_staleness_s` on `assess_scope()` is a build decision, not a spec
  number.** 03 says scope must be assessed "near" creation but names no
  duration. The parameter exists so a caller can decide what "near" means for
  their own deployment; the default (`None`, no guard) does not enforce
  anything on its own. Worth a real number once there is a real Scope checker
  to calibrate it against.
- **`reliability_evidence()`'s `independent_parent_sources` counts distinct
  `source` strings only.** Two parents both sourced `"worker"` from two
  genuinely different model instances would count as one source, not two —
  `source` per `knowledge_model.py::Claim` is "who produced it," and nothing
  in M8 distinguishes *which* instance of "worker" produced each parent. This
  may undercount real convergence. Flagged rather than silently fixed by
  widening what `source` means, since that is a M8 schema question, not an
  M9 one.
- **Whether Insufficiency's visible half is worth measuring alone.** The
  milestone calls it "half" for a reason — a corpus sweep could show a task
  with zero visible-insufficiency and still fail entirely from the invisible
  half (material that should have crossed but never did). Package 5's
  re-grade of E6 is where this either turns out to matter or turns out to be
  noise; not decidable from unit tests alone, noted here so it is not
  forgotten by the time E6 exists to check it against.

## Running

```
cd ../M8-persistent-work-and-knowledge && python test_turn_input.py
cd ../M9-context-governance-measurement && python test_failure_modes.py
python test_claim_dimensions.py
```

No model calls anywhere in this milestone's own code. Every stub is
deliberately inert; every real function is deliberately mechanical.
