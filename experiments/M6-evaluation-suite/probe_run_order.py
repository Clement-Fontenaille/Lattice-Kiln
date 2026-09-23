"""Does what ran before change what runs now?

Reps are supposed to be independent draws from one cell. If the order of runs
moves the result, they are not, and every interval computed over them is wrong
in a way no amount of repetition fixes.

Three channels could carry state between runs, and they fail differently:

  our process   module globals, the workspace, the meter, the transcript sink.
                All reset per rep BY CONSTRUCTION -- which is exactly what
                would have been said about the transcript sink an hour before
                it was found recording nothing.
  the server    Ollama caches prompt prefixes in a slot's KV cache, and under
                OLLAMA_NUM_PARALLEL several requests share one model instance.
                This is where leakage would actually live.
  the model     nothing: /api/chat is stateless, the full message list is sent
                every time. Stated to be ruled out, not assumed.

THE DESIGN IS A/B/A AT TEMPERATURE 0. Greedy decoding makes any difference a
difference rather than a draw. A runs cold, B is a long unrelated prompt that
evicts or reshapes whatever A left, then A runs again. If A1 != A2, something
carried.

A second pass runs A twice back to back (A/A) as the control: if THAT differs,
the backend is not deterministic at temperature 0 and the A/B/A result cannot
be attributed to ordering at all. Without this control the whole probe is
unreadable, which is the mistake the nudge probe made by testing on a case
that never failed.

RESULT, 2026-09-23, nemotron3-nano-4b and qwen2.5-coder 7B, 2 reps each:

    A/A     deterministic on both -- so the test is readable
    A/B/A   unchanged, output hash identical after an unrelated 574/366-token
            generation in between
    cold    identical after evicting the model, same prompt-token count

SEQUENTIAL ORDER DOES NOT CONTAMINATE. Context is genuinely reset per call.

WHAT THIS DOES NOT COVER, AND IT IS THE CASE THAT MATTERS. This probe fires one
request at a time. The existing corpus behind 50-findings/12 and /14 was
gathered with OLLAMA_NUM_PARALLEL=3 and up to three workers hitting one model
instance at once. Concurrent requests share that instance and compete for KV
cache slots, which is a different mechanism from sequential prefix reuse and is
NOT ruled out by anything here.

Also uncovered: temperature 0 with a fixed seed is used so a difference is a
difference; real runs draw at 0.2 with no seed, which is variance by design and
not contamination. And both prompts are short, so nothing here speaks to
behaviour under cache pressure near the context limit.

    python probe_run_order.py [model ...] [--reps N]
"""
from __future__ import annotations

import hashlib
import json
import sys
import urllib.error
import urllib.request

BASE = "http://localhost:11434"
DEFAULT_MODELS = ["nemotron3-nano-4b:latest", "qwen2.5-coder:7b-instruct-q4_K_M"]

A = ("Write a Python function `slugify(title)` that lowercases the title, "
     "replaces any run of non-alphanumeric characters with a single hyphen, "
     "and strips leading and trailing hyphens. Return only the code.")
B = ("Explain, in about 200 words, why floating point addition is not "
     "associative, and give a concrete example with three float values where "
     "(x + y) + z differs from x + (y + z). Then describe how Kahan summation "
     "reduces the error, and when it does not help.")


def once(model: str, prompt: str, num_predict: int = 400) -> dict:
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0, "top_p": 1, "seed": 0,
                        "num_ctx": 8192, "num_predict": num_predict}}
    req = urllib.request.Request(
        f"{BASE}/api/chat", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        p = json.loads(r.read().decode("utf-8"))
    txt = (p.get("message") or {}).get("content") or ""
    return {"sha": hashlib.sha256(txt.encode()).hexdigest()[:12],
            "chars": len(txt),
            "ptok": p.get("prompt_eval_count"),
            "etok": p.get("eval_count")}


def unload(model: str) -> None:
    """keep_alive 0 evicts the model, so the next call is genuinely cold."""
    body = {"model": model, "messages": [{"role": "user", "content": "x"}],
            "keep_alive": 0, "stream": False, "options": {"num_predict": 1}}
    req = urllib.request.Request(
        f"{BASE}/api/chat", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=120).read()
    except urllib.error.URLError:
        pass


def main(argv: list[str]) -> None:
    reps = 1
    if "--reps" in argv:
        i = argv.index("--reps")
        reps = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    for model in argv or DEFAULT_MODELS:
        print("=" * 72)
        print(model)
        for r in range(reps):
            # CONTROL: A twice, nothing between. Establishes whether greedy
            # decoding is even reproducible here.
            a1 = once(model, A)
            a2 = once(model, A)
            det = a1["sha"] == a2["sha"]
            print(f"  rep{r} A/A   {a1['sha']} {a2['sha']}  "
                  f"{'deterministic' if det else 'NON-DETERMINISTIC'}")
            if not det:
                print("        -> temperature 0 does not reproduce; the "
                      "ordering test below cannot be read")
            # TREATMENT: A, an unrelated long prompt, A again.
            b = once(model, B, num_predict=600)
            a3 = once(model, A)
            same = a1["sha"] == a3["sha"]
            print(f"  rep{r} A/B/A {a1['sha']} -> [B {b['etok']}tok] -> "
                  f"{a3['sha']}  {'unchanged' if same else 'CHANGED'}")
            # COLD: evict the model and run A once more.
            unload(model)
            a4 = once(model, A)
            print(f"  rep{r} cold  {a4['sha']}  "
                  f"{'matches warm' if a4['sha'] == a1['sha'] else 'DIFFERS FROM WARM'}"
                  f"  (ptok {a1['ptok']} vs {a4['ptok']})")


if __name__ == "__main__":
    main(sys.argv[1:])
