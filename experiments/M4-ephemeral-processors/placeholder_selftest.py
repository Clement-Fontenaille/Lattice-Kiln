"""M4 plumbing self-test - placeholder task, before the real fixture task set.

Proves the processor runtime wires together: naive context assembly -> one real
model call -> control-block parse -> effect routing through the M3 floor ->
event recording through the M2 recorder -> a reconstructable run.

Also drives the synthetic gate-refusal path directly (a model will not reliably
misbehave on demand) to prove a refused effect lands as a kind-3 record.

    python experiments/M4-ephemeral-processors/placeholder_selftest.py

Skips (exit 0) if Ollama is not reachable.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from _bridge import Gate, Run, RunRecorder, CapabilitySet  # noqa: E402
from context_assembly import assemble  # noqa: E402
from ollama_client import health  # noqa: E402
from processor import _route_effect, capability_set_for, run_processor  # noqa: E402

RUNS = HERE / "runs"
_fails: list[str] = []


def want(cond: bool, msg: str) -> None:
    print(("  ok  " if cond else "  FAIL") + " " + msg)
    if not cond:
        _fails.append(msg)


def make_placeholder_repo() -> Path:
    d = Path(tempfile.mkdtemp(prefix="m4ph_")).resolve()
    (d / "README.md").write_text("# placeholder\nA tiny repo for the M4 plumbing test.\n", encoding="utf-8")
    (d / "greeting.py").write_text("def greet():\n    return 'hi'\n", encoding="utf-8")
    (d / "test_greeting.py").write_text(
        "from greeting import greet\n\ndef test_greet():\n    assert greet() == 'hello'\n",
        encoding="utf-8")
    return d


def main() -> None:
    RUNS.mkdir(exist_ok=True)
    if not health():
        print("Ollama not reachable on localhost:11434 - skipping M4 plumbing test.")
        return

    ws = make_placeholder_repo()
    try:
        objective = ("The test in test_greeting.py expects greet() to return 'hello'. "
                     "Make it pass by editing greeting.py.")
        bundle = assemble(objective, ws, token_budget=4000)
        want(bundle.token_estimate <= 4000, f"context bundle within budget ({bundle.token_estimate} tok)")
        want(any("greeting.py" in e.source_ref for e in bundle.entries),
             "naive assembly pulled greeting.py into context")

        rec = RunRecorder(RUNS, intent_text=objective, meta={"synthetic": True, "source": "M4 plumbing"})
        gate = Gate()
        root = rec.invocation(role="harness", model_identity={"name": "n/a"},
                              intent_ref="ph_intent")
        res = run_processor(role="implementer", objective=objective, context=bundle,
                            workspace_root=ws, recorder=rec, gate=gate,
                            parent_invocation_id=root, intent_ref="ph_intent")
        rec.close("completed")

        want(res.parse_ok, f"model produced a parseable control block (terminal_state={res.terminal_state})")
        want(res.proposed >= 1, f"at least one effect proposed ({res.proposed})")
        print(f"       [info] realized={res.realized} refused_gate={res.refused_by_gate} "
              f"refused_policy={res.refused_by_policy} files={res.files_written} "
              f"tok/s={res.gen_tokens_per_s}")

        r = Run(RUNS / rec.run_id)
        kinds = {e["kind"] for e in r.events}
        want("invocation" in kinds and "proposed_effect" in kinds,
             f"run reconstructs with invocation + proposed_effect records (kinds={sorted(kinds)})")
        impl = [e for e in r.invocations() if e["role"] == "implementer"]
        want(len(impl) == 1 and impl[0]["parent_invocation_id"] == root,
             "implementer invocation is recorded as a child of the harness root")
        want(r.header.get("outcome") == "completed", "run header closed with an outcome")

        # -- synthetic refusal paths (a model will not misbehave on cue) -------
        rec2 = RunRecorder(RUNS, intent_text="refusal paths", meta={"synthetic": True})
        inv2 = rec2.invocation(role="implementer", model_identity={"name": "qwen2.5-coder"})
        actor = capability_set_for("implementer")

        class _R:  # minimal result sink
            proposed = realized = refused_by_gate = refused_by_policy = 0
            files_written: list = []
            process_runs: list = []
        sink = _R()
        # (a) out-of-workspace write -> stopped by representability, ordinary policy
        _route_effect(rec2, gate, actor, inv2, ws, 1,
                      {"type": "workspace_write", "path": "../../etc/pwned", "content": "x"}, sink)
        # (b) rewriting an existing observability record -> gate H6 -> safety_intervention
        (ws / "runs" / "r1").mkdir(parents=True, exist_ok=True)
        (ws / "runs" / "r1" / "events.jsonl").write_text("{}\n", encoding="utf-8")
        _route_effect(rec2, gate, actor, inv2, ws, 1,
                      {"type": "workspace_write", "path": "runs/r1/events.jsonl", "content": "x"}, sink)
        rec2.close("completed")
        r2 = Run(RUNS / rec2.run_id)
        ivs = r2.safety_interventions()
        want(len(ivs) == 1 and ivs[0]["safety_kind"] == "gate_refusal",
             "writing an observability record is recorded as a gate_refusal safety_intervention")
        want(all(iv["retry_eligible"] is False for iv in ivs),
             "the safety intervention is retry_eligible=False")
        disp = [e["disposition"] for e in r2.of_kind("proposed_effect")]
        want(disp.count("rejected_by_gate") == 1 and disp.count("rejected_by_capability") == 1,
             f"both refusal paths recorded with distinct dispositions (got {disp})")
        want(sink.refused_by_gate == 1 and sink.refused_by_policy == 1,
             "the result sink counted one gate refusal and one policy refusal")
    finally:
        shutil.rmtree(ws, ignore_errors=True)

    # keep only the two newest run dirs
    for d in sorted(RUNS.glob("run_*"))[:-2]:
        shutil.rmtree(d, ignore_errors=True)

    print()
    if _fails:
        print(f"M4 PLUMBING TEST FAILED ({len(_fails)} assertion(s))")
        raise SystemExit(1)
    print("M4 PLUMBING TEST PASSED")


if __name__ == "__main__":
    main()
