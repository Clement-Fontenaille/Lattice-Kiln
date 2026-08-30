"""M2 reconstruction check (task 7), run against the real M4 runs.

Poses questions the observability schema was NOT designed around and answers them
from the stored records alone - no field was added to make either answerable.

    python experiments/M4-ephemeral-processors/reconstruction_check.py

Q1 (decision-relevant): did the ephemeral arm's INDEPENDENT REVIEWER ever
    disagree with the objective outcome - approve a run whose final check failed,
    or flag one that passed? Answering it joins the reviewer invocation's
    recorded conclusion (a type-4 realized effect) with the harness root's final
    objective check (a type-2 realized effect). Nothing links them in the schema.

Q2: across every run, when a proposed effect was refused, which ROLE proposed it
    and by which layer was it stopped - and did that run still reach its
    objective? Joins invocation.role x proposed_effect.disposition x the final
    check.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _bridge import Run  # noqa: E402

RUNS = HERE / "runs"
RESULTS = HERE / "results" / "results.json"


def load_runs() -> list[Run]:
    """Only the runs referenced by the committed results.json - so stale runs
    from earlier debugging are not mixed into the evidence."""
    ids = {row["run_id"] for row in json.loads(RESULTS.read_text(encoding="utf-8"))}
    out = []
    for rid in sorted(ids):
        d = RUNS / rid
        if (d / "run.json").exists() and (d / "events.jsonl").exists():
            try:
                out.append(Run(d))
            except ValueError as e:
                print(f"  !! {d.name}: {e}")
        else:
            print(f"  !! {rid}: run dir missing (runs/ is gitignored; re-run harness.py)")
    return out


def final_objective_pass(r: Run) -> bool | None:
    for e in reversed(r.events):
        if (e["kind"] == "realized_effect" and e["effect_type"] == 2
                and "objective_pass=" in str(e.get("result_ref", ""))):
            return str(e["result_ref"]).split("objective_pass=")[1].strip() == "True"
    return None


def reviewer_conclusion(r: Run) -> dict | None:
    revs = [e for e in r.invocations() if e["role"] == "reviewer"]
    if not revs:
        return None
    rid = revs[-1]["invocation_id"]
    for e in r.events:
        if e["kind"] == "realized_effect" and e["effect_type"] == 4 and e["invocation_id"] == rid:
            return e["envelope"]
    return None


def q1(runs: list[Run]) -> None:
    print("Q1 - independent reviewer vs objective outcome (ephemeral arm)\n")
    rows, disagreements = [], 0
    for r in runs:
        if r.header["meta"].get("arm") != "ephemeral":
            continue
        env = reviewer_conclusion(r)
        if env is None:
            continue
        verdict = str(env.get("verdict", "") or "").lower() or _sniff(env.get("summary", ""))
        objp = final_objective_pass(r)
        agree = (verdict == "approve" and objp is True) or (verdict == "needs-change" and objp is False)
        if verdict in ("approve", "needs-change") and not agree:
            disagreements += 1
        rows.append((r.header["meta"]["task"], r.header["meta"]["rep"], verdict, objp, "" if agree else "  <-- MISMATCH"))
    print(f"  {'task':<22} {'rep':<4} {'reviewer':<13} {'objective_pass'}")
    for t, rep, v, o, flag in rows:
        print(f"  {t:<22} {rep:<4} {v:<13} {o}{flag}")
    print(f"\n  reviewer/outcome mismatches: {disagreements} / {len(rows)}")
    print("  => the reviewer's signal is reconstructable and can be scored against "
          "the objective check, though neither record was designed to reference the other.\n")


def _sniff(summary: str) -> str:
    u = (summary or "").upper()
    if "NEEDS-CHANGE" in u or "NEEDS CHANGE" in u:
        return "needs-change"
    return "approve" if "APPROVE" in u or "IS MET" in u or "SOUND" in u else "unclear"


def q2(runs: list[Run]) -> None:
    print("Q2 - refused proposed effects: which role, which layer, did the run still pass?\n")
    n = 0
    for r in runs:
        objp = final_objective_pass(r)
        role_by_inv = {e["invocation_id"]: e["role"] for e in r.invocations()}
        for e in r.events:
            if e["kind"] != "proposed_effect" or e["disposition"] == "realized":
                continue
            n += 1
            role = role_by_inv.get(e.get("invocation_id"), "?")
            layer = e["disposition"]
            extra = e.get("links", {}).get("stopped_by") or e.get("links", {}).get("reason", "")
            print(f"  {r.header['meta']['task']:<22} {r.header['meta']['arm']:<10} "
                  f"role={role:<12} {e['effect_type_name']:<20} {layer:<22} "
                  f"objective_pass={objp}  {str(extra)[:40]}")
    if n == 0:
        print("  (no refused proposed effects in this run set)")
    print()


def main() -> None:
    runs = load_runs()
    print(f"loaded {len(runs)} runs from {RUNS}\n")
    if not runs:
        raise SystemExit("no runs - run harness.py first")
    q1(runs)
    q2(runs)


if __name__ == "__main__":
    main()
