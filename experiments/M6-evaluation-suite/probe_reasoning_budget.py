"""Why every audit and judge call returned empty text on Nemotron.

Findings 12's addendum established the mechanism on one prompt: the model is a
reasoning model, Ollama returns its reasoning in a separate `thinking` field and
leaves `response` empty until it exits the thinking block, and the audit and
judge calls cap generation at 200 and 220 tokens.

This measures the shape of it across real suite objectives:

  A. how much of the budget goes to thinking before any answer appears
  B. the cap at which `response` stops being empty
  C. whether the reasoning can be turned off (`/no_think`)
  D. qwen on the same prompts, as the control

Writes probe_results/reasoning_budget.json and prints a table.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "experiments" / "M4-ephemeral-processors"))

from ollama_client import generate  # noqa: E402

JSON_RE = re.compile(r"\{.*\}", re.S)
NEMO = "nemotron-gpu"
QWEN = "qwen2.5-coder:7b-instruct-q4_K_M"

# The real audit prompt, read from the arm rather than retyped.
_src = (ROOT / "experiments" / "M7-static-workflow" / "judge_anchored_workflow.py").read_text(
    encoding="utf-8")
AUDIT = re.search(r'^AUDIT\s*=\s*(""")(.*?)\1', _src, re.S | re.M).group(2)

# Real objectives, spanning the suite's shapes.
TASKS = [t for t in json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))["tasks"]]
PICK = ["wf1_crossfile", "wf5_partial", "hf_timeout_param", "hf_csv",
        "hf_path_sanitize", "hf_merge_config", "wf4_assumption", "hf_rename"]


def code_for(t):
    d = HERE / t["dir"]
    parts = []
    for p in sorted(d.glob("*.py")):
        if p.name.startswith("test_"):
            continue
        parts.append(f"--- {p.name} ---\n{p.read_text(encoding='utf-8', errors='replace')}")
    return "\n".join(parts)[:4000]


def call(model, prompt, cap, system=None):
    t0 = time.monotonic()
    g = generate(prompt, model=model, temperature=0.3, num_predict=cap, system=system)
    raw = g.raw
    resp = raw.get("response") or ""
    think = raw.get("thinking") or ""
    return {
        "model": model, "num_predict": cap,
        "done_reason": raw.get("done_reason"),
        "eval_count": raw.get("eval_count"),
        "thinking_chars": len(think), "response_chars": len(resp),
        "json_found": bool(JSON_RE.search(resp)),
        "wall_s": round(time.monotonic() - t0, 1),
    }


def main():
    by_id = {t["id"]: t for t in TASKS}
    out = {"schema": "reasoning-budget/1", "results": []}

    # ---- A: one high-cap call per objective, to see the natural split
    print("A. natural thinking/answer split at num_predict=2048\n")
    print(f"{'task':20s} {'done':7s} {'evaltok':>8s} {'think_ch':>9s} {'resp_ch':>8s} {'json':>5s}")
    for tid in PICK:
        t = by_id[tid]
        p = AUDIT.replace("{obj}", t["objective"]).replace("{code}", code_for(t))
        r = call(NEMO, p, 2048)
        r["task"], r["phase"] = tid, "A"
        out["results"].append(r)
        print(f"{tid:20s} {r['done_reason']:7s} {r['eval_count']:8d} "
              f"{r['thinking_chars']:9d} {r['response_chars']:8d} {str(r['json_found']):>5s}")

    # ---- B: the cap sweep on one objective
    print("\nB. cap sweep, hf_timeout_param\n")
    t = by_id["hf_timeout_param"]
    p = AUDIT.replace("{obj}", t["objective"]).replace("{code}", code_for(t))
    print(f"{'cap':>6s} {'done':7s} {'think_ch':>9s} {'resp_ch':>8s} {'json':>5s}")
    for cap in (200, 220, 400, 600, 800, 1000, 1200, 1536):
        r = call(NEMO, p, cap)
        r["task"], r["phase"] = "hf_timeout_param", "B"
        out["results"].append(r)
        print(f"{cap:6d} {r['done_reason']:7s} {r['thinking_chars']:9d} "
              f"{r['response_chars']:8d} {str(r['json_found']):>5s}")

    # ---- C: can the reasoning be suppressed?
    print("\nC. reasoning suppression at the arm's own cap (200)\n")
    for label, sysmsg, pre in (("baseline", None, ""),
                               ("system /no_think", "/no_think", ""),
                               ("prefix /no_think", None, "/no_think\n")):
        r = call(NEMO, pre + p, 200, system=sysmsg)
        r["task"], r["phase"], r["variant"] = "hf_timeout_param", "C", label
        out["results"].append(r)
        print(f"{label:18s} done={r['done_reason']:7s} think={r['thinking_chars']:6d} "
              f"resp={r['response_chars']:5d} json={r['json_found']}")

    # ---- D: qwen control
    print("\nD. qwen on the same prompt at the arm's cap\n")
    for cap in (200, 1536):
        r = call(QWEN, p, cap)
        r["task"], r["phase"] = "hf_timeout_param", "D"
        out["results"].append(r)
        print(f"cap={cap:5d} done={r['done_reason']:7s} think={r['thinking_chars']:6d} "
              f"resp={r['response_chars']:5d} json={r['json_found']}")

    (HERE / "probe_results").mkdir(exist_ok=True)
    (HERE / "probe_results" / "reasoning_budget.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("\nwrote results/reasoning_budget.json")


if __name__ == "__main__":
    main()
