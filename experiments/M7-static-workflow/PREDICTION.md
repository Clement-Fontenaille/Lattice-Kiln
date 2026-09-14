# M7 — expected effect, recorded before the run

_Written 2026-09-14, before `m7_workflow.py` was executed on the suite._

`10-evaluation-task-suite.md` requires an expected effect size declared before the
run. This file is it. It is not revised afterwards; the findings entry records what
happened against it.

## What is being compared

The M7 static workflow against the three arms already measured on suite 0.1.0:

| arm | pass | regressions | decline | wall |
|---|---|---|---|---|
| `monolith` | 18/30 | 7 | 0/5 | 4.3 min |
| `dloop` | 24/30 | 0 | 5/5 | 6.8 min |
| `staged` | 19/30 | 0 | 5/5 | 11.8 min |

M7 is `dloop`'s spine plus two things `staged` had in the wrong form: a premise audit
made **advisory** instead of a decline gate, and a concern split fired **on
condition** instead of always.

## The prediction

**Pass rate: 25/30, range 24–26.** The mechanism is narrow and worth naming, because
a hit outside it would be luck rather than the design working:

- M7 keeps `dloop`'s 24 by keeping its spine unchanged.
- **+1 from concern split on `wf6_multi`**, which `dloop` escalates at 2/6 with
  `DOCSCORE 0/4` and `TODOSCORE 0/3` — a three-concern objective its single pass never
  reaches the back of. M6 recorded the split taking this task from 2/6 to 6/6.
- `hf_json_serialize` is the second `concern-split`-tagged task. `dloop` already
  passes its subtests (5/5) and misses `STRUCTSCORE 1/2`, so the split can add at most
  a structural point here and may add nothing.

**Regressions: 0.** The incumbent-protected keeper is unchanged from `dloop` and is
the rule producing this. A regression would mean the build broke the keeper, not that
the design is wrong.

**Decline accuracy: 5/5, and 6 declines total.** The sixth is `wf3_refactor` and it is
a **known false decline inherited from `dloop`**, not a new defect — see below.

**Cost: 8–10 minutes.** `dloop`'s 6.8 plus one audit call per task, plus the split's
extra passes on two tasks. Should land nearer `dloop` than `staged`, and the whole
point of making the audit advisory is that it costs one call instead of three.

## The six tasks this is expected to recover from `staged`

`staged` false-declined seven tasks. Six were the premise-audit gate refusing work
that was genuinely unfinished — `hf_csv`, `hf_json_field`, `hf_json_serialize`,
`hf_merge_config`, `hf_path_sanitize`, `hf_suppress`, all with `pass=False` at the
moment they were refused. **An advisory audit cannot produce any of them**, because it
cannot produce a terminal at all.

If M7 false-declines any of these six, the audit is not advisory in the build,
whatever the code says.

## The one this is expected NOT to fix

**`wf3_refactor` will still false-decline**, and predicting it is the point.

Its check emits no structural dimension at all — `struct={}` — while its subtests pass
at baseline. So a real refactor task is mechanically indistinguishable from
`hf_dead_code`, where passing subtests and nothing to do is the correct reading. The
test gate sees the same thing in both cases.

Fixing this by letting the audit's `refactor` classification suppress the decline
would violate *no lone model probe may flip a terminal state*
(`11-static-workflow.md`, stage 3). It is left unfixed deliberately, and it is the
`ground_notest` hole in its cheapest observable form.

## What would falsify the design rather than the build

- **Pass ≤ 24 with `wf6_multi` still failing**: the conditional split does not fire, or
  firing does not help. That retires the stage.
- **Pass ≤ 24 with `wf6_multi` passing**: the split helped and something else broke,
  which is a build defect rather than a design result.
- **Any regression**: the keeper was traded away.
- **Cost ≥ 11 min**: the advisory audit did not buy back what `staged` spent, and
  one-call-instead-of-three was the wrong economy.

## The stage-influence question

The build records, per stage, whether it fired and whether any later stage consumed
its output. The prediction there is uncomfortable and is stated anyway:

**The premise audit's `concerns` output is expected to be consumed on roughly five to
seven tasks** — only the ones that reach an escalation payload. Everything else
produces prose nothing reads. If it turns out to be consumed on zero, stage 1's
concern half is a retirement candidate on this suite's evidence, and only its
classification earns its call.
