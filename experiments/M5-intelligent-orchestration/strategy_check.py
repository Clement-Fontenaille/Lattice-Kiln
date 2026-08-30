"""M5 understandability check (task 6).

The Milestone 5 evidence question has two halves: does NL orchestration beat a
fixed workflow, AND does it stay understandable? This script answers the second
from the recorded runs alone: it reconstructs each orchestrated run's strategy -
what operation the orchestrator chose at each step and why - purely from the
decision records (type-4 effects, envelope.kind == "orchestrator_decision"), and
checks the reconstruction is complete and matches the invocation lineage.

    python experiments/M5-intelligent-orchestration/strategy_check.py
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
_fails: list[str] = []


def want(cond: bool, msg: str) -> None:
    print(("  ok  " if cond else "  FAIL") + " " + msg)
    if not cond:
        _fails.append(msg)


def decisions(r: Run) -> list[dict]:
    return [e["envelope"] for e in r.events
            if e["kind"] == "realized_effect" and e["effect_type"] == 4
            and e["envelope"].get("kind") == "orchestrator_decision"]


def synthesis(r: Run) -> dict | None:
    for e in r.events:
        if (e["kind"] == "realized_effect" and e["effect_type"] == 4
                and e["envelope"].get("kind") == "orchestrator_synthesis"):
            return e["envelope"]
    return None


def orch_child_roles(r: Run) -> list[str]:
    orch = next((e for e in r.invocations() if e["role"] == "orchestrator"), None)
    if not orch:
        return []
    oid = orch["invocation_id"]
    return [e["role"] for e in r.invocations() if e.get("parent_invocation_id") == oid]


def main() -> None:
    if not RESULTS.exists():
        raise SystemExit("no results.json - run compare.py first")
    ids = [row["run_id"] for row in json.loads(RESULTS.read_text(encoding="utf-8"))
           if row["arm"] == "orchestrated"]
    if not ids:
        raise SystemExit("no orchestrated runs in results.json")

    print(f"{len(ids)} orchestrated runs\n" + "=" * 70)
    for rid in ids:
        d = RUNS / rid
        if not (d / "events.jsonl").exists():
            print(f"  !! {rid}: run dir missing (gitignored) - re-run compare.py")
            continue
        r = Run(d)
        meta = r.header["meta"]
        decs = decisions(r)
        syn = synthesis(r)
        spawn_from_decisions = [x["role"] for x in decs if x["op"] == "spawn" and x.get("role")]
        child_roles = orch_child_roles(r)

        print(f"\n{meta['task']} rep{meta['rep']}  ->  {syn['terminal_state'] if syn else '??'}")
        for x in decs:
            if x["op"] == "spawn":
                print(f"  step {x['step']}: spawn {x['role']:<11} - {x['rationale']}")
            else:
                print(f"  step {x['step']}: STOP        - {x['rationale']}")
        if syn:
            print(f"  synthesis: {syn['summary'][:150]}")

        want(len(decs) >= 1, f"{rid}: has >=1 decision record")
        want(all(x.get("rationale") and x["rationale"] != "(no rationale given)" for x in decs),
             f"{rid}: every decision record carries a real rationale")
        want(spawn_from_decisions == child_roles,
             f"{rid}: decision-record spawn order == orchestrator's child invocations "
             f"({spawn_from_decisions} vs {child_roles})")
        want(syn is not None and syn.get("terminal_state") in ("resolved", "blocked", "abandoned"),
             f"{rid}: has a synthesis record with a terminal state")

    print("\n" + "=" * 70)
    if _fails:
        print(f"STRATEGY CHECK FAILED ({len(_fails)})")
        raise SystemExit(1)
    print("STRATEGY CHECK PASSED - every orchestrated run's strategy reconstructs "
          "from decision records alone, consistent with the invocation lineage.")


if __name__ == "__main__":
    main()
