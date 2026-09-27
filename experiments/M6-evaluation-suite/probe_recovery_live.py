"""Does resuming a collapsed call actually recover it?

Everything said about recovery so far is design. This is the first execution.
Two questions, kept apart because they fail separately:

  RESUME   given a real 25,141-character runaway, does handing the processor its
           own work back plus one steering sentence produce usable output --
           a write_file and a conclude -- or does it just loop again?
  CONSULT  can a small model, reading the brief, pick a sensible remedy from the
           menu? If not, recovery has to sit on a larger model or on the static
           ladder, and that is a finding about where it belongs rather than a
           reason to drop it.

THE COMPARISON THAT MAKES RESUME MEANINGFUL. A resumed attempt is measured
against a plain RESTART at the same sampling -- same model, same steer, same
budget, just without the prior work handed back. Without that arm, "resume
worked" cannot be distinguished from "anything at temperature 0.6 works", and
the temperature probe already showed that a fresh call at 0.6 succeeds 18/20.
Resume has to beat restart, not beat the original failure.

    python probe_recovery_live.py [--n 10] [--workers 3] [--model M]
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
import recovery as R                      # noqa: E402
from roles import TOOLS                   # noqa: E402
from probe_record import persist          # noqa: E402

BASE = "http://localhost:11434"
STORE = HERE.parent.parent / "evalkit_store"
RETRY_PROMPT = (STORE / "probe_prompts" / "impl_call2.txt")
RUNAWAY = (STORE / "probe_prompts" / "runaway_thinking.txt")
_lock = threading.Lock()


def call(prompt: str, *, model: str, options: dict) -> dict:
    opts = {"num_ctx": 16384, **options}
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "tools": TOOLS, "stream": False, "think": True, "options": opts}
    req = urllib.request.Request(
        f"{BASE}/api/chat", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=1800) as r:
            p = json.loads(r.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return {"err": repr(e)[:60]}
    m = p.get("message") or {}
    calls = [(c.get("function") or {}).get("name")
             for c in (m.get("tool_calls") or [])]
    text = m.get("content") or ""
    think = m.get("thinking") or ""
    looped, _ = R.is_degenerate(think + text)
    return {"eval": p.get("eval_count") or 0,
            "prompt_eval_count": p.get("prompt_eval_count"),
            "done": p.get("done_reason"),
            "calls": calls,
            "wrote": "write_file" in calls,
            "concluded": "conclude" in calls,
            "looped": looped,
            "think": len(think)}


def report(label: str, rows: list[dict], cap: int) -> None:
    ok = [r for r in rows if "err" not in r]
    if not ok:
        print(f"  {label:26} all failed")
        return
    ev = sorted(r["eval"] for r in ok)
    def q(p):
        i = (len(ev) - 1) * p
        lo, hi = int(i), min(int(i) + 1, len(ev) - 1)
        return round(ev[lo] + (ev[hi] - ev[lo]) * (i - lo))
    print(f"  {label:26}{min(ev):>7}{q(.25):>7}{q(.5):>7}{q(.75):>7}{max(ev):>7}"
          f"{sum(1 for r in ok if r['eval'] >= cap - 8):>4}/{len(ok)}"
          f"{sum(1 for r in ok if r['looped']):>6}"
          f"{sum(1 for r in ok if r['wrote']):>6}"
          f"{sum(1 for r in ok if r['concluded']):>6}")


def main(argv: list[str]) -> None:
    n, workers = 10, 3
    model = "nemotron3-nano-4b:latest"
    if "--n" in argv:
        n = int(argv[argv.index("--n") + 1])
    if "--workers" in argv:
        workers = int(argv[argv.index("--workers") + 1])
    if "--model" in argv:
        model = argv[argv.index("--model") + 1]

    original = RETRY_PROMPT.read_text(encoding="utf-8")
    loop = RUNAWAY.read_text(encoding="utf-8")
    diag = R.diagnose(thinking=loop, done_reason="length")
    remedy, why = R.decide(objective="Add a retries parameter to Client.call.",
                           diag=diag, context_shown=original, thinking=loop,
                           attempt=1)          # attempt 1 = the concrete-step rung
    cap = remedy.options.get("num_predict", R.RECOVERY_NUM_PREDICT)
    resumed = R.build_resume(original_prompt=original, thinking=loop,
                             steer=remedy.steer)
    restart = f"{original}\n\n{remedy.steer}"

    print(f"{model} | diagnosis: {diag.mode} ({diag.evidence[:40]})")
    print(f"remedy: {remedy.describe()[:100]}")
    print(f"  via: {why}")
    print(f"resumed prompt {len(resumed)} chars | restart prompt {len(restart)} "
          f"chars | recovery cap {cap}\n")

    arms = {
        "RESUME + steer": resumed,
        "RESTART + steer": restart,
        "RESTART, no steer": original,
    }
    res: dict[str, list[dict]] = {k: [] for k in arms}
    jobs = [(k, p) for k, p in arms.items() for _ in range(n)]

    def run(j):
        k, p = j
        r = call(p, model=model, options={**remedy.options, "num_predict": cap})
        with _lock:
            res[k].append(r)

    t0 = time.monotonic()
    try:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(run, jobs))
    finally:
        persist("recovery_live", {"model": model, "n": n, "cap": cap,
                                  "diagnosis": {"mode": diag.mode,
                                                "evidence": diag.evidence},
                                  "remedy": remedy.describe(), "via": why,
                                  "options": {**remedy.options, "num_predict": cap},
                                  "prompt_chars": {k: len(p) for k, p in arms.items()}},
                [{"arm": k, **r} for k in arms for r in res[k]])
    print(f"wall {(time.monotonic() - t0) / 60:.1f} min\n")
    print(f"  {'arm':26}{'min':>7}{'25%':>7}{'50%':>7}{'75%':>7}{'max':>7}"
          f"{'cap':>6}{'loop':>6}{'wrote':>6}{'concl':>6}")
    for k in arms:
        report(k, res[k], cap)
    print("\n  cap = hit the recovery budget. loop = still degenerate. "
          "wrote/concl = produced\n  a usable write_file / conclude. RESUME has "
          "to beat RESTART, not the original failure.")


if __name__ == "__main__":
    main(sys.argv[1:])
