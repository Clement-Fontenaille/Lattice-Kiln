"""M2 self-test: synthetic run + reconstruction assertions.

No real processor exists yet (that is M4). This builds a run by hand that
exercises every mandatory event kind and every reconstruction guarantee in
docs/10-technical/02-observability-event-model.md, then asserts they hold.

    python experiments/M2-observability-foundation/selftest.py
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from event_model import RunRecorder  # noqa: E402
from reconstruct import Run  # noqa: E402

RUNS = HERE / "runs"
INTENT = "intent_demo_0001"


def build_synthetic_run() -> str:
    rec = RunRecorder(RUNS, intent_text="add a rate limiter to the API client",
                      meta={"synthetic": True, "source": "M2 selftest"})

    # orchestrator (root), fully GPU-resident 7B
    orch = rec.invocation(
        role="orchestrator", intent_ref=INTENT,
        model_identity={"name": "qwen2.5-coder", "quant": "Q4_K_M", "params_b": 7,
                        "runtime": "ollama", "offloaded": False},
        context_ref="ctx_orch_v1", config_ref="gen_baseline")

    # implementer, spawned by the orchestrator
    impl = rec.invocation(
        role="implementer", parent_invocation_id=orch, intent_ref=INTENT,
        model_identity={"name": "qwen2.5-coder", "quant": "Q4_K_M", "params_b": 7,
                        "runtime": "ollama", "offloaded": False},
        context_ref="ctx_impl_v1", config_ref="gen_baseline")

    # implementer proposes + realizes a workspace mutation (allowed)
    pe1 = rec.proposed_effect(impl, effect_type=1, payload_ref="diff_ratelimiter_py",
                              disposition="realized")
    eff1 = rec.realized_effect(impl, effect_type=1,
                               envelope={"path": "client/ratelimiter.py",
                                         "representable": True, "permitted": True,
                                         "attributable": impl, "reversible": "vcs"},
                               outcome="realized", result_ref="commit_abc123")

    # implementer proposes a network access the gate refuses
    iv = rec.safety_intervention(kind="gate_refusal", disposition="halted",
                                 on_invocation_id=impl,
                                 note="egress to non-allowlisted host during impl")
    rec.proposed_effect(impl, effect_type=3, payload_ref="fetch_http_example_com",
                        disposition="rejected_by_gate",
                        links={"intervention_id": iv})

    # reviewer, spawned by the orchestrator, reads only (no effects)
    rec.invocation(role="reviewer", parent_invocation_id=orch, intent_ref=INTENT,
                   model_identity={"name": "qwen2.5-coder", "quant": "Q5_K_M", "params_b": 7,
                                   "runtime": "ollama", "offloaded": False},
                   context_ref="ctx_review_v1", config_ref="gen_baseline")

    # a human correction attached to the realized effect
    rec.human_correction(target_ref=eff1, kind="annotation",
                         detail="limiter window should be 60s not 30s")

    rec.close("completed")
    return rec.run_id


def check(run_id: str) -> None:
    r = Run(RUNS / run_id)
    fails = []

    def want(cond: bool, msg: str) -> None:
        print(("  ok  " if cond else "  FAIL") + " " + msg)
        if not cond:
            fails.append(msg)

    # 1. all four mandatory kinds present (+ human_correction)
    kinds = {e["kind"] for e in r.events}
    want({"invocation", "proposed_effect", "realized_effect", "safety_intervention"} <= kinds,
         "all four mandatory event kinds recorded")

    # 2. per-actor ordered history for the implementer
    impl = next(e for e in r.invocations() if e["role"] == "implementer")
    hist = r.per_actor(impl["invocation_id"])
    seq_kinds = [h["kind"] for h in hist]
    want([h["seq"] for h in hist] == sorted(h["seq"] for h in hist),
         "implementer history is seq-ordered")
    want(seq_kinds == ["proposed_effect", "realized_effect", "safety_intervention", "proposed_effect"],
         f"implementer history shape is propose/realize/intervene/propose (got {seq_kinds})")

    # 3. per-intent lineage reaches every invocation under the intent
    #    (orchestrator + implementer + reviewer = 3)
    pi = r.per_intent("intent_demo_0001")
    want(len(pi["invocation_ids"]) == 3,
         f"per-intent lineage reaches all 3 invocations (got {len(pi['invocation_ids'])})")
    want({r.invocation(i)["role"] for i in pi["invocation_ids"]} == {"orchestrator", "implementer", "reviewer"},
         "per-intent lineage covers orchestrator, implementer, reviewer")
    orch = next(e for e in r.invocations() if e["role"] == "orchestrator")
    want(r.intent_lineage(orch["invocation_id"]) [0] == orch["invocation_id"],
         "lineage walk is rooted at the orchestrator")

    # 4. safety intervention is its own category and never auto-retryable
    ivs = r.safety_interventions()
    want(len(ivs) == 1 and ivs[0]["safety_kind"] == "gate_refusal",
         "the gate refusal is a distinct safety_intervention record")
    want(all(iv["retry_eligible"] is False for iv in ivs),
         "safety interventions are retry_eligible=False")
    want(all(iv["kind"] != "realized_effect" for iv in ivs),
         "a safety intervention is not folded into a generic effect/failure")

    # 5. the unplanned question - answerable with no schema field added for it
    ans = r.unplanned_answer()
    row = ans["rows"][0] if ans["rows"] else {}
    want(ans["rows"] and row.get("model") == "qwen2.5-coder" and row.get("offloaded") is False
         and row.get("safety_kind") == "gate_refusal",
         f"unplanned join (gate-refused -> serving model + offload flag) resolves: {row}")

    print()
    if fails:
        print(f"SELFTEST FAILED ({len(fails)} assertion(s))")
        raise SystemExit(1)
    print("SELFTEST PASSED")


if __name__ == "__main__":
    RUNS.mkdir(exist_ok=True)
    rid = build_synthetic_run()
    print(f"built synthetic run: {rid}\n")
    check(rid)
    # keep the newest run for inspection; drop older synthetic ones
    for d in sorted(RUNS.glob("run_*"))[:-1]:
        shutil.rmtree(d, ignore_errors=True)
