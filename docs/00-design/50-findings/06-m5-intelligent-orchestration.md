# Entry 6 — Milestone 5: Intelligent orchestration experiments

**Date:** 2026-08-31

**Evidence question:** does natural-language orchestration beat a fixed workflow
while staying understandable, and where does its overhead start to exceed the
benefit of decomposition?

**What the evidence said.**

An LLM orchestrator (observe → decide the next operation → spawn a processor via
the M4 runtime → integrate → stop; capability set `{6, 4}`; a decision record per
step) was compared against the M4 fixed planner→implementer→reviewer chain and
the monolith. Same 7B model, same naive context, same 4-task fixture, N=2, 24
runs.

- **Objective pass: orchestrated 7/8, monolith 6/8, fixed chain 5/8.** Across M4
  and M5 this is the first arm to beat the monolith.
- **The win is one task and it has a legible mechanism.** On `task_4_starve`
  (context starvation — monolith 0/2, fixed chain 0/2) and `task_2_median`, the
  orchestrator spawned a **second implementer** after the first attempt failed
  the objective check — the reviewer→implementer revision loop that findings-log
  entry 5 identified as the missing piece. `task_4` went 0/2 and 0/2 → **2/2**
  under orchestration.
- **Cost: ~5× the model calls (40 vs 8) and ~4.5× wall-clock** (25.5 s vs 5.7 s
  mean). On the three tasks the monolith already one-shots, orchestration added
  4–6 calls and 15–35 s for no net benefit. **Overhead exceeds benefit on any
  task a single pass can solve; it pays off only where the simpler arms fail.**
- **Understandable — with one gap.** `strategy_check.py` reconstructs every run's
  strategy (which operation each step, and the rationale for every spawn) from
  the decision records alone, consistent with the invocation lineage. But **7 of
  8 stop decisions recorded no rationale**: the orchestrator explains why it
  *acts*, not why it considers the work *done*.
- **False-premise handling regressed.** The monolith and the fixed chain both
  explicitly *declined* `task_3_nobug` ("the claimed bug does not exist"). The
  orchestrator reached the right outcome (stopped, touched nothing, tests stayed
  green) but via `terminal_state: blocked` ("no useful next step") — with a
  correct rationale in one rep, none in the other. Its stopping rules do not
  distinguish "this rests on a false premise" from "I am stuck".

**Verdict: confirms, narrowly** (against "orchestration can compensate for model
limits" / "natural-language orchestration beats a fixed workflow",
`40-roadmap/03-research-and-evaluation-agenda.md`). NL orchestration beat both the
fixed chain and the monolith; the margin is +1/8, within N=8 noise; and the gain
is entirely explained by adaptive retry on tasks the other arms fail. It stays
understandable for the acting half of the loop and is weak on the stopping half.
The overhead is only justified when a single pass would fail.

**Touches.**

- Design: `20-cognitive-architecture/03-orchestrator.md` — record that adaptive
  retry (routing a failed attempt back to a fresh implementer) is where
  natural-language orchestration earned its overhead at this scale, and that
  stopping / `declined` reasoning is the weak spot (the orchestrator conflates
  "false premise" with "stuck").
- Specification: `10-technical/08-orchestrator-contract.md` — the decision record
  MUST carry a rationale for **stop** decisions, not only spawns (open contract →
  normative); add an explicit `declined` terminal state distinct from `blocked`,
  each with a required reason. `10-technical/02-observability-event-model.md` —
  the decision record is another instance of the "structured outcome, not prose"
  lesson from entry 3.
- Milestone sequence: this closes the MVP slice (M0–M5). The first scheduled
  rework follows — `40-roadmap/06-sequence-rework-01.md`.

**Runs.** `experiments/M5-intelligent-orchestration/` — `orchestrator.py`,
`compare.py`, `strategy_check.py`, `results/results.json` + `results/summary.md`;
per-run records under `runs/` (schema `m2-run/0`, git-ignored; the 2026-08-31
three-arm N=2 set is the reference).

## Addendum (2026-08-31) — workflow-suite re-test

The first M5 comparison used four single-concern katas that fit one clean
context — the monolith's home turf (finding: the earlier caveat that the
baseline favours the monolith). A follow-up re-test used six **workflow-shaped**
tasks (cross-file bug, feature-with-a-design-choice, refactor-trap,
stale-assumption, partial-credit parser, and a multi-concern task = algorithm +
docstrings + TODO gardening in one file), scored by **subtests passed** plus, for
the multi-concern task, separate **doc** and **TODO** scores. Arms: monolith, a
**fixed** planner→(implementer↔reviewer up to 3 rounds) loop, and the
orchestrator — all on tuned role prompts (`roles_v2.py`), N=3, 54 runs.

Tuning was required first. The untuned fixed sequence lost to the monolith on
3/5 tasks; diagnosis from the transcripts:

- the implementer **narrated instead of writing** ("Fixed the function by…", no
  FILE block) whenever its context carried any conversational text — a plan, a
  critique, a prior summary. The monolith writes reliably because its context is
  only objective + code. Fix: the fixed flow no longer injects the planner's
  prose into the implementer; retry hints go into the objective, not a separate
  "additional input" block.
- the reviewer **rubber-stamped** empty implementations. Fix: an empty
  written-file list is now an automatic `needs-change`, plus a deterministic
  harness guard that forces a retry when no real file was written.
- the planner wrote **past-tense completion claims** that primed the chain toward
  false-done, and the 7B ignores "don't use past tense" — so the harness blunts
  the completion phrasing before it propagates.

**What the tuned re-test showed.** Aggregate: monolith 10/18 objective pass
(67/87 subtests, 18 calls), fixed 11/18 (76/87, 83 calls), orchestrated 12/18
(77/93, 129 calls). Cost of decomposition: **4.6× the model calls for the fixed
loop, 7.2× for the orchestrator**.

Per task the benefit is narrow and concentrated:

- **wf3, wf4, wf5** (single-concern, one clean pass suffices): decomposition is
  pure overhead — identical scores, 3–8× the calls. Consistent with finding 5.
- **wf1** (cross-file indirection): the monolith patched the symptom file twice
  and scored 3.0/5; the review loop caught the wrong-layer fix and both
  decomposed arms hit 5/5. **Decomposition helps.**
- **wf6** (multi-concern): the monolith produced **syntactically invalid Python
  on every run** and scored 2/6 algo, **0/4 docs, 0/3 TODO** — it dropped the
  secondary concerns entirely while failing the primary one. The fixed loop hit
  6/6 algo, 2/4 docs, 3/3 TODO; the orchestrator 6/6, 1.5/4, 2.5/3. **This is the
  clearest positive for decomposition in the whole milestone** and it directly
  confirms the "a monolith degrades on secondary concerns under load"
  hypothesis.
- **wf2** (feature design choice): a regression. The orchestrator scored 0/5 on
  two of three runs — it spawned the *planner* 4–6 times consecutively without
  ever reaching an implementer, because (a) the tuned planner over-returns
  `blocked` on a normal "add a feature that doesn't exist yet" task and (b)
  `run_orchestrated` does not implement the repetition stopping rule spec `08`
  requires. The fixed loop also stalled here (3.7/5).

**Revised reading of the M5 verdict.** "Confirms, narrowly" stands, but the shape
is now clearer: decomposition's benefit is **real, concentrated on multi-file and
multi-concern work, and invisible-to-negative everywhere else**, at 5–7× the
cost. The orchestrator's extra flexibility buys a further small gain on the
hardest task (wf6, 2/3 vs the fixed loop's 1/3) and one real failure mode (wf2).
Neither the orchestrator nor the fixed loop decisively beats the other (12 vs 11
on pass, 83% vs 87% on subtests). At 7B/N=3, per-cell score noise is large
(wf5 monolith: 1/7, 5/7, 7/7 on identical inputs) — the reliable signal is in the
**transcript mechanisms**, not the score deltas.

**Also touches.**

- `10-technical/08-orchestrator-contract.md` — the **repetition stopping rule**
  ("same operation N times without progress → stop") is normative but was not
  implemented; wf2 is the concrete failure. The planner's terminal-state guidance
  needs "a capability the code does not yet have is the normal case, not a reason
  to block".
- `10-technical/07-naive-context-assembly.md` — a 7B implementer is **degraded by
  any conversational context** (plan, critique). Role-to-role handoff cannot be
  raw prose; this is a constraint on how the context assembler frames prior-step
  output.
- Milestone sequence: still no reordering. `40-roadmap/06-sequence-rework-01.md`
  decision 2 (fold the M4/M5 re-test into M7/M8) is updated with this first pass.

**Runs.** `experiments/M5-intelligent-orchestration/` — `workflow_suite.py`,
`roles_v2.py`, `fixture_workflow/` (schema `m5-workflow-tasks/0`),
`results_workflow/results.json` + `summary.md`; per-run records under `runs/`
(git-ignored; the 2026-08-31 three-arm N=3 set is the reference).
