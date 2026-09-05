# Entry 7 — M5 follow-up: attractor census + judge-lab

**Date:** 2026-09-01

**Evidence question (self-set, feeding the goal re-evaluation):** the static role
system is weak at 7B — before deciding what waits on better hardware, can it be
*tuned* to useful output? Specifically: where does the 7B reliably go for each
role-relevant task shape (so a role can be pointed with the current, not against
it), and can the judgment step be rescued by voting, per-clause structure, or
execution grounding?

**What the evidence said.**

Two wide first-pass experiments on the M0 working default
(`qwen2.5-coder:7b-instruct-q4_K_M`).

*Attractor census* (`experiments/M5-intelligent-orchestration/census/`, 39 probes
× K=3 = 117 calls): task shape × framing, scoring the *motion* not correctness.

- **Doer — "emit the whole corrected file" is a strong, correct current.** On the
  cross-file bug (symptom in one file, cause in another) all bare samples fixed
  the right file with the right logic; cross-file indirection did not break it.
  A plan or critique in a *named, structured* section did not suppress file
  emission (partial walk-back of entry 6's "any conversational context degrades
  the 7B implementer" — that effect was specific to unlabelled mid-context
  injection).
- **Doer — one clean blind spot: false premises.** "Rewrite `find()` to O(log n)"
  on unsorted data: 3/3 implemented binary search, 0/3 noticed the precondition.
  It executes the objective's surface and never tests its premise.
- **Doer — multi-concern overloads it** (1/3 kept all three concerns of wf6) and
  it is blind to concerns it was not handed (single-concern passes echo the other
  concerns' stale state back unchanged).
- **Judge — no framing fixes it.** A shared-helper dedupe that silently rounds
  (`staff_price(1.567)`: 1.2536 → 1.25, a real regression) was approved 3/3 under
  every framing: `is_correct`, `predict_failure` (output: `PASS`),
  `strongest_reason`, and `criteria_first` — the last **actively harmful**: it
  reverse-engineered its acceptance criteria from the buggy code's own docstring,
  then declared them met, and separately false-rejected a *correct* simple fix
  2/3. The judge is not noisy; it is **systematically biased toward approval** and
  asserts the property it was asked to verify.
- **The planner stance engages the critical read the implementer suppresses** —
  same model, same task: 2/3 flag the false premise (vs implementer 0/3), 3/3
  keep all three wf6 concerns (vs implementer 1/3).

*Judge-lab* (`experiments/M5-intelligent-orchestration/judge_lab/`, 10 known
-truth scenarios × 4 pipelines): baseline reviewer / K=5 vote / deterministic
prechecks + model checklist + per-clause panel without the test / same with the
real test output.

- **baseline 4/10, vote 4/10 (verdict-identical on all 10 rows), ground_notest
  3/10, ground 6/10 (+2 escalate).**
- **Voting is dead** — errors are systematic, not zero-mean; K=5 at higher
  temperature changed no verdict.
- **The deterministic core alone — parse / import / claim-vs-diff / trust the
  `test_task.py` result — scores 9/10 with zero model calls.** Adding the 7B
  checklist+panel *drops* it to 6/10: the checklist codifies false premises as
  requirements (rejects the correct wf4 linear scan despite a 5/5 test), and the
  panel emits confident-wrong `not_met` on correct code (miscounts `range(0+1)`).
- The panel's one real use: given a *known* failing test line it writes a
  correct, cited explanation — a reporting aid, not a decision aid.

**Verdict: confirms** (the post-MVP recalibration in
`40-roadmap/06-sequence-rework-01.md`, and against "orchestration/decomposition
can compensate for model limits",
`40-roadmap/03-research-and-evaluation-agenda.md`). A 7B does the *doing* with
scaffolding and **cannot do the *judging*, and the gap is not a prompt away** —
neutral, adversarial, structured, and voted framings all fail the same way, and
per-clause structure without execution grounding makes it worse. The one lever
that works is running the test and trusting it; the model near the judgment seat
is limited to explaining a known failure. Premise-soundness is a planner-pass
concern. This sharpens rather than changes the recalibration: the self-improving
loop waits on a **second judgment source** — a stronger/reasoning model as
reviewer (enabled by the planned second GPU) or the model tier improving — not on
further prompt tuning of the 7B reviewer.

**Touches.**

- Design: `20-cognitive-architecture/02-processors.md` — record that role
  differentiation on a 7B works for producing (implementer) and for critical
  analysis under a *planning* framing, but not for verdict-style review;
  `20-cognitive-architecture/03-orchestrator.md` — a feedback loop's evaluation
  edge cannot be a same-model reviewer verdict on this hardware.
- Specification open contracts: `10-technical/07-naive-context-assembly.md` — the
  "prior-step handoff framing" contract gains detail (a plan in a *named section*
  is tolerated; unlabelled prose is not); `10-technical/08-orchestrator-contract.md`
  — a `declined` outcome for a false premise should be reachable from a planner
  pass, not expected from the implementer or a reviewer; add that automated-check
  results, where they exist, outrank any model verdict.
- Milestone sequence: no reordering. Directly feeds the **goal re-evaluation**
  (the next task): the M6–M8 "promising signal on 7B" bars in
  `06-sequence-rework-01.md` should treat the judgment step as human-or-stronger
  -model, not a 7B self-review, and the second-GPU / reasoning-reviewer path moves
  from "nice to have" toward "the gating dependency for the self-improving tier".

**Runs.** `experiments/M5-intelligent-orchestration/census/` (`probes.py`,
`run_census.py`, `summary.md`, `FINDINGS.md`, `runs/` transcripts) and
`.../judge_lab/` (`scenarios.py`, `lab.py`, `results.md`, `FINDINGS.md`, `runs/`
detail). Single-host, single 7B, 2026-09-01.

## Addendum (2026-09-01) — loop control (bundle D)

Following the judge-lab result (reviewer verdict unreliable, test result 9/10),
the implement↔review loop was rebuilt to run off the measurable signal
(`experiments/M5-intelligent-orchestration/loop_lab/`). Three arms on the six
workflow tasks, N=2: `oneshot` (implementer once), `naive_loop`
(`(reviewer→implementer)*` while the reviewer says needs-change — the current
`fixed` behaviour), and `d_loop` (bundle D: the pre-existing repo state is an
entrant in the keeper pool and a round is accepted only if it *beats* it;
continue only on measurable progress; one stalled round → stop and escalate;
ship the best snapshot ever seen, not the last; fix hints are the real failing
test lines).

- **d_loop: 0 regressions in 12 runs; `naive_loop`: 2** — both on wf6, where the
  review/fix loop drove the implementer to non-parsing Python and the reviewer
  **approved it**. An unreliable reviewer driving a loop amplifies damage; a
  test-gated keeper caps it at "no worse than the incumbent".
- **wf4 (false premise) solved by construction, 0 model calls** — the incumbent
  linear scan passes 5/5, so d_loop's loop never runs. It does not need to
  *recognise* the false premise; it refuses a change that does not beat a passing
  incumbent. `naive_loop` reached 5/5 too but spent 4–6 calls.
- **~3.4× cheaper than `naive_loop`** (14 vs 48 calls / 36 runs): stops on a
  green test, not on a reviewer's approval, and skips the loop when the incumbent
  passes.
- **d_loop's worst case is honest** (wf6: `no-improvement`, keeps the untouched
  original, escalates) vs `naive_loop`'s (ships broken, "approved").

Two limits: (a) **"first do no harm" degrades to "do nothing" when the check does
not capture the deliverable** — wf3 is a behaviour-preserving refactor, its test
passes on the un-refactored original, so d_loop no-ops it; behaviour-preserving
work needs a structural check or a human. (b) `STALL_TOL=1` stops too early on
climbable tasks (wf5: 5/7 vs `naive_loop` 7/7) — a tuning knob.

This does not change the entry-7 verdict; it is the constructive half. The loop
for a 7B fixed sequence: gate on the test not the reviewer, keep the incumbent as
the floor, escalate on stall. `10-technical/08-orchestrator-contract.md`'s
repetition stopping rule gains a concrete, working implementation
(progress-gated). The unresolved case — no executable check for the objective —
points at the "generate the missing tests, blind, K-way" follow-up.

**Runs.** `.../loop_lab/` (`lab.py`, `results/summary.md` + `results.json`,
`FINDINGS.md`).

## Addendum (2026-09-02) — super-pipeline (every idea, always on)

To find the ceiling of stage-stacking, `experiments/M5-intelligent-orchestration/pipeline_lab/`
runs all the promising ideas in one call-heavy flow (premise audit + task-type
classify · dual blind impl-specs · alignment check · K-way blind test synthesis ·
`here_is_file` + concern-split + best-of-2 coding · execute + K-way check
agreement + regression guard · context-diverse structural verify with
probe-confirmation · deterministic reconcile + **counterfactual attribution** —
each run replays reconciliation with each signal nulled to see which flips the
terminal). 6 workflow tasks × N=2, ~16–29 calls/task.

- **Net vs the cheap `loop_lab` d_loop: worse or tied on 5 of 6 tasks, better on
  1.** The unique win is **wf6 (multi-concern): 6/6 algo + ~3.5/4 docs + ~2.5/3
  TODO** where every prior arm scored ≤ 2/6 — via **concern-splitting + a keeper
  scored on `sub+doc+todo`, not subtests alone**. wf3 (refactor) got a more
  honest terminal (`escalate` — "behaviour preserved, cannot confirm the dedupe")
  than d_loop's silent no-op.
- **It regressed two solved tasks** (wf2, wf5: d_loop 5/5 → pipeline 0/5) because
  its coding stage **violated finding 6**: it injected the plan into the
  implementer's context (→ empty output, the documented narration failure) and
  used `here_is_file` framing — a *fix-an-existing-file* current — for greenfield
  implementation.
- **Counterfactual attribution: over 12 runs only `premise_unsound` (×2, correct
  wf4 declines), `l2_violated` (×2, both FALSE positives — a model-written probe
  exited 1 and "confirmed" a hallucinated violation) and `l1_provided_fail` (×1)
  ever decided a terminal.** The dual impl-specs, the alignment check, and the
  blind test synthesis changed **zero** outcomes — ~7 calls/run of dead weight.
  Blind synthesis was inert because its suites crash on an unfinished
  implementation before emitting any `CHECK` line.
- **Regressions vs baseline: 0/12** — the incumbent-protected keeper held through
  all the added complexity.

**Reading:** a **negative result with a precise payload.** Stage-stacking does not
beat the cheap loop except on the one task class (multi-concern) that needs a
specific mechanism, and unconditioned stages either sit inert or actively regress
by ignoring earlier findings. This is exactly the calibration data Milestone 7
(static supervised workflow) was inserted to consume: spine = d_loop; add premise
audit always, concern-split + combined-score keeper for conjunctive objectives,
"no behavioural signal → escalate" for refactors; drop the three inert stages;
never let a lone model probe flip a terminal.

**M5 investigation arc — closed.** Entry 6 answered the milestone's evidence
question; entry 7 and its three addenda (workflow re-test, loop control,
super-pipeline) established what a 7B-class static workflow can and cannot do and
named the Milestone 7 component. Sequence rework 2 (`07-sequence-rework-02.md`)
acts on it.

**Runs.** `.../pipeline_lab/` (`superpipe.py`, `roles_super.py`,
`results/summary.md` + `results.json`, `runs_super/` per-run ledgers +
transcripts, `FINDINGS.md`).
