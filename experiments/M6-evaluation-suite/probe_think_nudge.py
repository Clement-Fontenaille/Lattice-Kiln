"""Can a prompt curb runaway reasoning WITHOUT switching it off?

`think: false` is a blunt answer to Nemotron's non-termination: it removes the
capability rather than bounding it, and a non-reasoning judge is a different
instrument from a reasoning one. The question here is whether the model will
keep its reasoning and simply spend less of it when asked.

TESTED AGAINST THE REAL LOAD, ON PURPOSE. The earlier knob probe used a toy
arithmetic question and drew ~1,600 characters of thinking from the 9B -- it
could not have reproduced the failure at all. The runaway (33,706 characters
against an 8,192-token cap, no answer) happened on judge_anchored, so this uses
that arm's actual JUDGE prompt with a filled-in case. A nudge that works on a
toy prompt tells us nothing.

Every arm is reasoning-ON. What varies is only the instruction, so a difference
is attributable to the wording and not to the mode.

    python probe_think_nudge.py [model ...] [--reps N]
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "M7-static-workflow"))

BASE = "http://localhost:11434"
DEFAULT_MODELS = ["nemotron-gpu:latest", "nemotron3-nano-4b:latest"]
NUM_PREDICT = 8192
NUM_CTX = 16384

OBJ = ("Add a `retries` parameter to Client.call so a failing call is retried, "
       "and re-raise the last exception when every attempt fails.")
EXPECTED = ("  1. retries=0 makes exactly one attempt\n"
            "  2. the LAST exception is re-raised when every attempt fails\n"
            "  3. self.calls counts attempts, not invocations")
DIFF = """@@ class Client: @@
     def call(self, fn, retries=0):
+        attempt = 0
+        while attempt <= retries:
+            try:
+                self.calls += 1
+                return fn()
+            except Exception as e:
+                attempt += 1
+        raise e
"""


# THE TRIGGER, ISOLATED.
#
# A filled-in diff did NOT reproduce the runaway: the control stopped cleanly at
# 2,758 characters with a verdict. What the failing run actually had was an
# EMPTY diff -- the implementer produced nothing -- and the prompt tells the
# judge an empty diff is ambiguous and that it MUST decide which kind it is,
# from the request alone. An instruction to resolve an ambiguity with no
# evidence is a plausible way to make a reasoning model circle, so it is tested
# rather than assumed.
EMPTY_DIFF = "(no changes)"


def judge_prompt(diff: str = DIFF) -> str:
    import judge_anchored_workflow as w
    return (w.JUDGE.replace("{obj}", OBJ)
            .replace("{expected}", EXPECTED).replace("{diff}", diff))


# The nudges. Each is appended to the real prompt; none touches `think`.
NUDGES = {
    "none (control)": "",
    "be brief": (
        "\n\nKeep your reasoning brief. Reach the answer quickly."),
    "word budget": (
        "\n\nThink for at most 100 words, then answer. Do not re-check work "
        "you have already done."),
    "act not deliberate": (
        "\n\nYou are answering, not deliberating. Form a judgement on the "
        "first pass and write it. Do not second-guess yourself."),
    "no re-verification": (
        "\n\nDo not verify your conclusion more than once. Repeating a check "
        "you have already made adds nothing -- once each condition has an "
        "answer, emit the JSON immediately."),
    "answer first": (
        "\n\nWrite the JSON object FIRST, then stop. Any reasoning you do "
        "must fit in a few sentences before it."),
}


def ask(model: str, prompt: str) -> dict:
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "stream": False, "think": True,
            "options": {"temperature": 0.2, "num_ctx": NUM_CTX,
                        "num_predict": NUM_PREDICT}}
    req = urllib.request.Request(
        f"{BASE}/api/chat", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=1200) as r:
            p = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"err": f"HTTP {e.code}"}
    except urllib.error.URLError as e:
        return {"err": repr(e)[:60]}
    m = p.get("message") or {}
    ans = m.get("content") or ""
    verdict = None
    hit = re.search(r'"verdict"\s*:\s*"([a-z_]+)"', ans)
    if hit:
        verdict = hit.group(1)
    return {"think": len(m.get("thinking") or ""), "ans": len(ans),
            "eval": p.get("eval_count"), "done": p.get("done_reason"),
            "verdict": verdict}


def main(argv: list[str]) -> None:
    reps = 1
    if "--reps" in argv:
        i = argv.index("--reps")
        reps = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    models = argv or DEFAULT_MODELS
    cases = {"filled diff": judge_prompt(DIFF),
             "EMPTY diff": judge_prompt(EMPTY_DIFF)}
    print(f"think=True | num_predict={NUM_PREDICT} num_ctx={NUM_CTX} | reps={reps}")
    for model in models:
      for cname, prompt in cases.items():
        print("=" * 76)
        print(f"{model}   [{cname}, {len(prompt)} chars]")
        print(f"  {'nudge':22} {'thinking med':>12} {'max':>7} "
              f"{'trunc':>6} {'verdicts':>9}")
        for name, extra in NUDGES.items():
            rs = [ask(model, prompt + extra) for _ in range(reps)]
            errs = [r for r in rs if "err" in r]
            ok = [r for r in rs if "err" not in r]
            if not ok:
                print(f"  {name:22} all failed: {errs[0]['err']}")
                continue
            th = sorted(r["think"] for r in ok)
            med = th[len(th) // 2]
            # Truncation is the failure being studied, so it is counted, never
            # averaged away: one run in five that never answers is the thing
            # that breaks a sweep, and a mean hides it.
            trunc = sum(1 for r in ok if r["done"] == "length")
            vs = [r["verdict"] for r in ok]
            got = sum(1 for v in vs if v)
            uniq = sorted({v for v in vs if v})
            flag = "  <-- TRUNCATES" if trunc else ""
            print(f"  {name:22} {med:>12} {th[-1]:>7} {trunc:>3}/{len(ok)} "
                  f"{got:>4}/{len(ok)} {','.join(uniq) or '-'}{flag}")


if __name__ == "__main__":
    main(sys.argv[1:])
