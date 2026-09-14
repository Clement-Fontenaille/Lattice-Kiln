# The arms, by what distinguishes them

The identifiers `m7b`, `m7c`, `m7e`… are what the results files are keyed on and they
cannot change without orphaning recorded runs.
**In discussion, always write the identifier AND the name together** — `m7c`
juge-critique, `m7b` keeper-strict — so a reference is both traceable to a results file
and readable without this table. New arms take a readable identifier, so for them the
two collapse into one.

## Lineage

Every judge arm is built on **keeper-strict**, so the judge is the only thing that
varies between them. Everything shares the four stages, the mechanical decline rule and
a keeper blind to any model verdict.

```
base ── keeper-strict ─┬─ judge-critique
                       ├─ judge-instruction
                       ├─ judge-oriented
                       ├─ judge-staged            (task level)
                       └─ judge-staged-candidate  (per candidate)
                          
                       └─ judge-terminal   — derived from judge-critique, never run
```

## The table

| name | id | what distinguishes it | what it isolates | status |
|---|---|---|---|---|
| **base** | `m7` | the four stages as first specified | — | run, N=1 and N=5 |
| **keeper-strict** | `m7b` | R1–R5: the keeper compares the **set** of failing checks rather than their count; wide cost governor; `blocked` split in two; the audit emits segments; classification retired | whether refusing every regression costs anything | run, N=1 |
| **judge-critique** | `m7c` | a judge that writes a **critique**, folded in as *"a reviewer objects: …"* | findings-6's named failure: is a critique in the context enough to make the implementer narrate instead of write? | running |
| **judge-instruction** | `m7e` | the same judge writing **one imperative sentence** naming what is still to be done, folded in beside the mechanical hint with no reviewer framing | **register** — against judge-critique | built |
| **judge-oriented** | `m7f` | the same instruction, plus a prompt that says what produced the inputs, that an empty diff is ambiguous, that the audit's note is 18% precise, and five worked examples on invented code | **orientation** — against judge-instruction | built |
| **judge-staged** | `judge_staged` | two calls per judgement: objective data first (request + diff), then the subjective note before the final verdict | **anchoring** — makes the note's influence visible rather than inferred | to build |
| **judge-staged-candidate** | `judge_staged_cand` | the same, on every candidate rather than once per task | whether staging survives the cost of running it inside the loop | to build |
| **judge-terminal** | — | the judge restricting the terminal only: `answered` requires `met` | **derived from judge-critique's log**, never run — the verdict changes no candidate, so the trajectory is identical | `derive_m7d.py` |

## The reference nobody has to build

**self-report** — the implementer's own `terminal_state`, mandatory in its control
block, recorded as a type-4 effect on every run ever made, and discarded by the
workflow. Scored by `score_self_report.py`.

It says `answered` on **96%** of tasks and its precision sits **+3 points** above a
constant "yes". **Every judge arm above has to beat that**, while costing a call it
does not.

