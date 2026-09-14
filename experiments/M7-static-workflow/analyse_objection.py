"""Does a reviewer's objection in the objective trigger findings-6's failure mode?

findings-log entry 6 (M5): a 7B implementer **narrates instead of writing** -- no FILE
block, empty output -- whenever its context carries conversational text, and the three
cases it names are *a plan, a critique, a prior summary*. A judge's objection is a
critique, so this is the named case rather than an analogy.

Two things make it worth measuring rather than assuming.

**The M5 fix changed two things at once.** It removed the planner's prose AND moved
retry hints from a separate "additional input" block into the objective. Which of the
two mattered was never separated, so the evidence does not establish that prose *in
the objective* is harmful -- only that prose in a separate block was.

**The failure has a mechanical signature.** No FILE block means no type-1 effect, and
the recorder logs every effect. So "did the implementer stop writing?" is a count, not
a judgement.

    python analyse_objection.py
"""
from __future__ import annotations

import glob
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE = HERE / "stage_influence_m7c.jsonl"


def implementer_calls(runs_glob: str):
    """(role, effects_written) per invocation, in order, across every run."""
    out = []
    for f in sorted(glob.glob(runs_glob)):
        cur, seen = None, 0
        for line in open(f, encoding="utf-8"):
            e = json.loads(line)
            if e.get("kind") == "invocation":
                if cur == "implementer":
                    out.append(seen)
                cur, seen = e.get("role"), 0
            elif e.get("kind") == "proposed_effect":
                seen += 1
        if cur == "implementer":
            out.append(seen)
    return out


def main():
    if not STAGE.is_file():
        raise SystemExit("m7c has not produced a stage log yet")
    recs = [json.loads(x) for x in STAGE.read_text(encoding="utf-8").splitlines() if x]

    # Rebuild which rounds carried an objection: round N did iff round N-1 said not_met.
    with_obj, without_obj = 0, 0
    verdicts = {}
    for r in recs:
        prev = None
        for v in r.get("judge_candidates", []):
            (with_obj := with_obj + 1) if prev == "not_met" else (without_obj := without_obj + 1)
            verdicts[v["verdict"]] = verdicts.get(v["verdict"], 0) + 1
            prev = v["verdict"]

    calls = implementer_calls(str(HERE / "runs_m7c" / "*" / "events.jsonl"))
    silent = sum(1 for c in calls if c == 0)

    print("## The narration signature\n")
    print(f"- implementer invocations recorded: **{len(calls)}**")
    print(f"- of which wrote **no file at all**: **{silent}** "
          f"({100*silent/max(1,len(calls)):.0f}%)")
    print("\nEntry 6's failure is exactly this: narration, no FILE block. A rate near "
          "zero says the objection did not reproduce it in this position.\n")

    print("## Where the objections went\n")
    print(f"- implementer calls that received an objection: **{with_obj}**")
    print(f"- implementer calls with only the mechanical hint: **{without_obj}**")
    print(f"- judge verdicts over candidates: {verdicts}")

    if with_obj == 0:
        print("\n**No objection was ever injected**, so this run says nothing about "
              "entry 6. Either the judge never said `not_met` on a candidate, or it "
              "only did so on the last round of a pass. The measurement needs a run "
              "where objections actually reach an implementer.")
        return

    print("\n## What this cannot separate\n")
    print("The per-call narration rate above is over **all** implementer calls. "
          "Attributing it to objections needs the two populations scored apart, which "
          "needs the objection flag carried into the invocation record rather than "
          "reconstructed here. That is a change to the arm, not to this script, and it "
          "is the thing to fix before drawing a conclusion either way.")


if __name__ == "__main__":
    main()
