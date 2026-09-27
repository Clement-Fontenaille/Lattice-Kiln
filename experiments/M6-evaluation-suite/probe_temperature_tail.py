"""Is the runaway a sampling artifact rather than a reasoning one?

WHAT THE RUNAWAY ACTUALLY IS. Read out of a stored transcript rather than
inferred: the first ~700 characters are coherent work on the retry semantics,
the model reaches a genuine ambiguity about what self.calls should count, and
then emits the SAME ~150-character block verbatim until the cap:

    "So they want 2? That's retries? So they want retries? That's 2. So they
     got 1, which is retries-1. So maybe they think calls = retries-1? ..."

That is degenerate repetition -- a decoding failure, not a model thinking too
hard. Which changes what the fix should be.

THE MISCONFIGURATION. Every arm hardcodes temperature 0.2 while reasoning is
ON, because LATTICE_THINK is unset so no `think` key is sent and the model's
own default (thinking) applies. NVIDIA pair 0.2 with reasoning OFF and 0.6+
with reasoning ON, precisely because low temperature and long reasoning traces
produce loops. The model's own Modelfile ships `temperature 1, top_p 1`, so
0.2 is five times below what it was packaged with.

50-findings/15 already recorded the same monotone pattern without connecting
it: "temperature 0.0 degenerated 5 times out of 5, 0.2 four times, 0.6 twice."
That was newlines collapsing into spaces; this is a sentence repeating. Same
family, read as two different things -- once as a protocol effect, once as a
model that could not stop thinking.

SO THIS TESTS THE LEVER NOBODY VARIED. Same verbatim implementer prompt, same
cap, no nudge anywhere: only the sampling moves. If the cap rate collapses at
0.6, the nudge programme was treating a symptom.

    python probe_temperature_tail.py [--n 20] [--workers 3]
"""
from __future__ import annotations

import json
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "M4-ephemeral-processors"))
from roles import TOOLS                      # noqa: E402
from probe_implementer_tail import series  # noqa: E402
from probe_record import persist           # noqa: E402

# THE SECOND implementer call, not the first. Of 15 truncations in the
# pipeline, ONE was on the first implementer call and 13 were on the second or
# third: the collapse happens on the RETRY, after the judge has rejected the
# work. probe_implementer_tail used the first call and saw 0/20 caps against a
# pipeline rate of 8/26 -- it could not reproduce the failure at all, which its
# calibration arms correctly exposed.
#
# The second call adds the check's failure output, the current source, and an
# explicit hint ("Make self.calls reflect the number of attempts"). The test
# source is in the prompt too. So the model has everything it needs and
# collapses anyway, which is why this probe moves the sampler and not the
# information.
PROMPT_FILE = (HERE.parent.parent / "evalkit_store" / "probe_prompts"
               / "impl_call2.txt")

BASE = "http://localhost:11434"
MODEL = "nemotron3-nano-4b:latest"
CAP = 8192
NUM_CTX = 16384

# (label, temperature, top_p, repeat_penalty)
#
# 0.2/- is what every row in the store was taken at. 0.6/0.95 is NVIDIA's
# reasoning-ON pairing. 1.0/1.0 is the model's own Modelfile default. The last
# arm holds temperature at the broken value and raises repeat_penalty instead,
# to separate "low temperature causes loops" from "loops are simply unpenalised"
# -- they predict the same cure and different mechanisms.
ARMS = [
    ("t0.2 (as shipped)", 0.2, None, None),
    ("t0.6 p0.95 (NVIDIA)", 0.6, 0.95, None),
    ("t1.0 p1.0 (Modelfile)", 1.0, 1.0, None),
    # MEASURED HARMFUL, kept so the result is not rediscovered: on the
    # first-call prompt where every other arm capped 0/20, this capped
    # 6/18 and ran ~4x longer. A repetition penalty does not stop a loop,
    # it stops TERMINATION -- ending a generation re-uses tokens it is
    # suppressing. Left in as an arm because that is worth confirming on
    # the prompt that actually loops.
    ("t0.2 + rep_pen 1.3", 0.2, None, 1.3),
]

_lock = threading.Lock()


def one(prompt: str, temp: float, top_p, rep) -> dict:
    """One call. `eval_count` is -1 when the request itself failed."""
    opts = {"temperature": temp, "num_ctx": NUM_CTX, "num_predict": CAP}
    if top_p is not None:
        opts["top_p"] = top_p
    if rep is not None:
        opts["repeat_penalty"] = rep
    body = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
            "tools": TOOLS, "stream": False, "think": True, "options": opts}
    req = urllib.request.Request(
        f"{BASE}/api/chat", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=1800) as r:
            p = json.loads(r.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return {"eval_count": -1, "error": repr(e)[:120]}
    return {"eval_count": p.get("eval_count") or 0,
            "prompt_eval_count": p.get("prompt_eval_count"),
            "done_reason": p.get("done_reason"),
            "eval_duration_ns": p.get("eval_duration"),
            "thinking_chars": len((p.get("message") or {}).get("thinking") or ""),
            "content_chars": len((p.get("message") or {}).get("content") or ""),
            "n_tool_calls": len((p.get("message") or {}).get("tool_calls") or [])}


def main(argv: list[str]) -> None:
    n, workers = 20, 3
    if "--n" in argv:
        n = int(argv[argv.index("--n") + 1])
    if "--workers" in argv:
        workers = int(argv[argv.index("--workers") + 1])
    prompt = PROMPT_FILE.read_text(encoding="utf-8")
    print(f"{MODEL} | implementer stage, verbatim prompt, NO nudge | "
          f"think=True | n={n} | cap={CAP}")
    print(f"{len(ARMS)} sampling arms x {n} = {len(ARMS) * n} calls, "
          f"{workers} concurrent\n")

    res: dict[str, list[int]] = {a[0]: [] for a in ARMS}
    calls: list[dict] = []
    jobs = [a for a in ARMS for _ in range(n)]

    def run(a):
        label, temp, top_p, rep = a
        c = one(prompt, temp, top_p, rep)
        with _lock:
            res[label].append(c["eval_count"])
            calls.append({"arm": label, "temperature": temp, "top_p": top_p,
                          "repeat_penalty": rep, **c})

    t0 = time.monotonic()
    try:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(run, jobs))
    finally:
        persist("temperature_tail", {"model": MODEL, "cap": CAP, "num_ctx": NUM_CTX,
                                     "n": n, "think": True,
                                     "prompt": PROMPT_FILE.name,
                                     "prompt_chars": len(prompt),
                                     "arms": ARMS}, calls)
    print(f"wall {(time.monotonic() - t0) / 60:.1f} min\n")

    for label, *_ in ARMS:
        v = [x for x in res[label] if x >= 0]
        cap = sum(1 for x in v if x >= CAP - 8)
        print(f"{label:24} cap {cap:>2}/{len(v)}")
        print(f"  {series(v)}")
    print(f"\ncap = {CAP}: the call never terminated. Everything else is a "
          f"completed call.")


if __name__ == "__main__":
    main(sys.argv[1:])
