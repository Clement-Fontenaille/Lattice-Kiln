"""Is this model fit to judge, before a sweep is queued against it?

    python probe_nemotron3.py                       # default: nemotron3-nano-4b
    python probe_nemotron3.py --model nemotron-gpu  # the 9B, for comparison

Four checks, each one a failure this project has already paid for.

1. RESIDENCY. `num_gpu 99` is a request, not a guarantee, and the llama.cpp
   fitter will shed layers to meet LLAMA_ARG_FIT_TARGET's free-VRAM margin
   unless overruled. Partial offload costs 10-20x (M0 entry 1) and `/api/ps`
   reports a partially-offloaded model as loaded and healthy.

2. NON-EMPTY RESPONSE. Nemotron Nano 9B v2 spent the whole 220-token judge
   budget inside its thinking block and returned "" for thirteen arms, recorded
   as "a model that judges badly" for two days (50-findings/12, addendum 2).
   `think=false` fixed it there. Nemotron 3's card says reasoning is steered by
   system prompt instead, so the same control may not apply, and an empty
   response must be detected here rather than at analysis time.

3. PARSEABLE VERDICT UNDER BOTH FORMATS. The 9B failed to emit a closed JSON
   object in 17-21% of judge calls under `decision_first` and 2% under
   `reason_first` (50-findings/14). That is the specific defect this model was
   fetched to test, so it is measured directly, on the real JUDGE prompt, at
   the real token budget, before committing to hours of sweep.

4. SLOT COUNT. Ollama refuses parallel requests for the `nemotron_h`
   architecture outright, and says so only in server.log. If Nemotron 3 inherits
   that, extra workers gap-fill rather than batch, and the sweep should be
   planned for one slot.

Exit code is non-zero if any check fails, so this can gate a queue script.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "M4-ephemeral-processors"))
sys.path.insert(0, str(HERE.parent / "M7-static-workflow"))

_JSON = re.compile(r"\{.*\}", re.S)
_VERDICTS = {"met", "not_met", "unsound_request"}

OBJ = ("orders.total() returns the wrong amount when an order line's qty is "
       "greater than 1. Fix the code so every subtest in test_task.py passes.")
CONDS = ("  1. total() multiplies unit price by qty\n"
         "  2. line_price is used rather than duplicated\n"
         "  3. existing subtests still pass")
DIFF = """--- a/orders.py
+++ b/orders.py
@@ -8,7 +8,7 @@ def line_price(unit, qty):
-    return unit
+    return unit * qty

 def total(lines):
-    return sum(l.unit for l in lines)
+    return sum(line_price(l.unit, l.qty) for l in lines)
"""


def judge_prompt() -> str:
    src = (HERE.parent / "M7-static-workflow" /
           "judge_caveat_workflow.py").read_text(encoding="utf-8")
    return re.search(r'^JUDGE = """(.*?)"""', src, re.S | re.M).group(1)


def residency(model: str) -> tuple[bool, str]:
    try:
        with urllib.request.urlopen("http://localhost:11434/api/ps", timeout=5) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:  # noqa: BLE001
        return False, f"cannot reach ollama ({e})"
    for m in d.get("models", []):
        if m["name"].startswith(model.split(":")[0]):
            pct = 100 * m["size_vram"] / m["size"]
            return pct > 99, (f"{pct:.1f}% resident, {m['size_vram']/2**20:.0f} MiB"
                              + ("" if pct > 99 else "  *** PARTIAL OFFLOAD ***"))
    return False, "not loaded"


def slots(model: str) -> str:
    log = Path(os.environ.get("LOCALAPPDATA", "")) / "Ollama" / "server.log"
    if not log.is_file():
        return "server.log not found"
    ids, refused = 0, False
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines()[-4000:]:
        if "new slot, n_ctx" in line:
            ids += 1
        if "does not currently support parallel requests" in line:
            refused = True
        if "starting llama server" in line or "load_model" in line and ids:
            pass
    if refused:
        return "architecture refused parallel requests (see server.log)"
    return f"{ids} 'new slot' line(s) in the recent log"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="nemotron3-nano-4b")
    ap.add_argument("--n", type=int, default=8, help="judge calls per format")
    ap.add_argument("--num-predict", type=int, default=220,
                    help="the judge's real budget; MIN_PREDICT may raise it")
    args = ap.parse_args()

    os.environ["LATTICE_EVAL_MODEL"] = args.model
    os.environ.setdefault("LATTICE_TRANSCRIPT", "0")   # a probe is not a result
    import judge_format
    from ollama_client import generate

    JUDGE = judge_prompt()
    ok = True
    print(f"probing {args.model}, {args.n} judge call(s) per format, "
          f"num_predict {args.num_predict}\n")

    # 2 + 3 together: the real prompt, the real budget, both formats.
    for fmt in ("decision_first", "reason_first"):
        os.environ["LATTICE_JUDGE_FORMAT"] = fmt
        prompt = (judge_format.apply(JUDGE).replace("{obj}", OBJ)
                  .replace("{expected}", CONDS).replace("{diff}", DIFF))
        counts, empties, toks = Counter(), 0, []
        for _ in range(args.n):
            try:
                g = generate(prompt, temperature=0.2,
                             num_predict=args.num_predict)
            except Exception as e:  # noqa: BLE001
                counts["raised"] += 1
                print(f"  {fmt}: raised {e!r}"[:160])
                continue
            toks.append(g.eval_count)
            if not g.text.strip():
                empties += 1
                counts["empty"] += 1
                continue
            m = _JSON.search(g.text)
            if not m:
                counts["no JSON"] += 1
                continue
            try:
                v = str(json.loads(m.group(0)).get("verdict", "")).strip().lower()
            except Exception:  # noqa: BLE001
                counts["bad JSON"] += 1
                continue
            counts["parsed" if v in _VERDICTS else "verdict rejected"] += 1
        good = counts["parsed"]
        med = sorted(toks)[len(toks) // 2] if toks else 0
        print(f"  {fmt:15s} parsed {good}/{args.n}   median {med} tok   {dict(counts)}")
        if good < args.n:
            ok = False
        if empties:
            print(f"    !! {empties} EMPTY response(s) -- the 50-findings/12 "
                  f"failure. Check whether reasoning is on.")

    print()
    res_ok, res = residency(args.model)
    print(f"  residency      {res}")
    print(f"  slots          {slots(args.model)}")
    ok = ok and res_ok

    print("\n" + ("READY -- a sweep against this model is worth queueing"
                  if ok else
                  "NOT READY -- fix the above before queueing a sweep"))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
