# M4 fixture task set

Four small, self-contained Python tasks, each scored by an objective `pytest`
check. Deliberately tiny — the reference host runs one 7B model and arm B spends
three model calls per task.

| Task | Kind | Correct outcome |
|---|---|---|
| `task_1_stringcalc` | implement from a stub | tests pass |
| `task_2_median` | fix a real bug behind a failing test | tests pass |
| `task_3_nobug` | **false premise** — the claimed bug does not exist | decline; existing tests stay green |
| `task_4_starve` | **context starvation** — needed helper is in `helpers_misc.py`, which naive assembly won't surface | tests pass (by asking for the file or reimplementing `slugify`) |

`tasks.json` (schema `m4-tasks/0`) holds each task's objective text and expected
outcome. The harness copies a task dir to a throwaway workspace per run, so the
committed fixture stays pristine.
