"""Derive m7d from m7c's record, without running it.

m7d is m7c with the judge admitted on the **direction condition**: it may only
restrict. `answered` requires the check to be complete AND the judge to say `met`; a
judge that disagrees turns `answered` into `blocked-partial` and can never produce a
success. A degraded judge yields unnecessary escalation, never a false pass
(`03-capability-authority-model.md`, the direction condition; `11-static-workflow.md`,
no lone model probe may flip a terminal state -- which this respects, since it
withholds a claim rather than making one).

**Why this is derivable and the alternative is not.** Here the verdict is read once,
after the loop, so it changes no candidate and the trajectory is identical to m7c's.
Replaying the terminal against the logged verdict gives exactly what a run would.

Wiring the judge into the *keeper* instead would change which candidate is kept, hence
the next round's starting state, hence everything after it. That trajectory cannot be
replayed from a log of a different one -- it needs a verdict per candidate, which
m7c never collected and cannot without running.

    python derive_m7d.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE = HERE / "stage_influence_m7c.jsonl"
RES = HERE.parent / "M6-evaluation-suite" / "results"


def load():
    if not STAGE.is_file():
        raise SystemExit("m7c has not run yet -- nothing to derive from")
    recs = [json.loads(x) for x in STAGE.read_text(encoding="utf-8").splitlines() if x]
    rows = {r["task"]: r for r in json.loads((RES / "m7c.json").read_text(encoding="utf-8"))}
    return recs, rows


def derive(rec):
    """m7c's terminal, with the judge allowed to restrict it and nothing else."""
    t = rec["terminal"]
    v = (rec.get("judge") or {}).get("verdict")
    if t != "answered":
        return t, "judge not consulted -- only `answered` is restrictable"
    if v == "met":
        return "answered", "judge agrees"
    if v is None:
        return "answered", "no verdict parsed -- fails OPEN, since a judge that did "\
                           "not answer must not withhold a success the check supports"
    return "blocked-partial", f"judge said {v}"


def main():
    recs, rows = load()
    changed, table = [], []
    for r in recs:
        task = r["task"]
        new, why = derive(r)
        truth = rows[task]["objective_pass"] if task in rows else None
        if new != r["terminal"]:
            changed.append((task, r["terminal"], new, truth, why))
        table.append((task, r["terminal"], new, truth))

    print("## m7d, derived from m7c -- no run\n")
    print(f"tasks: {len(recs)} | terminals changed by the judge: **{len(changed)}**\n")
    print("| arm | terminals |")
    print("|---|---|")
    for name, idx in (("m7c", 1), ("m7d", 2)):
        print(f"| `{name}` | {dict(Counter(row[idx] for row in table))} |")

    if not changed:
        print("\nThe judge changed nothing. It agreed with every `answered` the check "
              "produced, which is the **approval-bias** reading rather than a "
              "vindication: a judge that never withholds is indistinguishable from no "
              "judge at all.\n")
        return

    print(f"\n### The {len(changed)} the judge downgraded\n")
    print("| task | m7c | m7d | check says | why |")
    print("|---|---|---|---|---|")
    for task, old, new, truth, why in changed:
        mark = "**WRONGLY**" if truth else "rightly"
        print(f"| {task} | {old} | {new} | {'pass' if truth else 'fail'} | {mark}: {why} |")

    wrong = sum(1 for *_, truth, _ in changed if truth)
    print(f"\n**{wrong} of {len(changed)} downgrades contradict a passing check.** Each "
          "is a success the judge withheld from work that was done. That is the cost "
          "of the direction condition, and it is the number to weigh against whatever "
          "the judge caught.\n")

    caught = len(changed) - wrong
    print(f"**{caught} landed on work the check also calls unfinished** -- which is "
          "agreement, not detection: the check already knew. **A judge earns its place "
          "only where it disagrees with the check and is right**, and on this suite "
          "that means `wf3_refactor` and `wf3_refactor_blindview`, where the worker's "
          "view of the check is incomplete and the judge's is not.")


if __name__ == "__main__":
    main()
