"""Which thinking controls actually bite on the Nemotrons, through Ollama?

Three candidates, from three different places, and only measurement says which
are real here:

  think: true|false      Ollama's own request field. Already wired to
                         LATTICE_THINK.
  think: "low"|"high"    Ollama accepts a level for some models. Whether this
                         model honours it is the question.
  /think, /no_think      NVIDIA's documented keywords, read out of the prompt
                         by the model's chat template. The GGUF's Jinja
                         template implements them -- but Ollama renders with
                         its own RENDERER, which may not.

Reported per setting: thinking characters produced, answer characters, and
whether the request was refused outright. A knob that changes nothing is as
useful to know about as one that works.

    python probe_think_knobs.py [model ...]
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

BASE = "http://localhost:11434"
DEFAULT_MODELS = ["nemotron3-nano-4b:latest", "nemotron-gpu:latest"]
Q = ("A train leaves at 14:05 and arrives at 17:40, stopping twice for 8 "
     "minutes each. How long is it moving? Answer with the number of minutes.")


def ask(model: str, prompt: str, think, num_ctx: int = 16384,
        num_predict: int = 2048) -> dict:
    body: dict = {"model": model,
                  "messages": [{"role": "user", "content": prompt}],
                  "stream": False,
                  "options": {"temperature": 0.2, "num_ctx": num_ctx,
                              "num_predict": num_predict}}
    if think is not None:
        body["think"] = think
    req = urllib.request.Request(
        f"{BASE}/api/chat", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            p = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode('utf-8','replace')[:120]}"}
    m = p.get("message") or {}
    return {"think_ch": len(m.get("thinking") or ""),
            "answer_ch": len(m.get("content") or ""),
            "eval": p.get("eval_count"),
            "done": p.get("done_reason")}


CASES = [
    ("think unset (default)", Q, None),
    ("think=True", Q, True),
    ("think=False", Q, False),
    ('think="low"', Q, "low"),
    ('think="high"', Q, "high"),
    ("/no_think in prompt", Q + " /no_think", None),
    ("/think in prompt", Q + " /think", None),
]


def main(models: list[str]) -> None:
    for model in models:
        print("=" * 72)
        print(model)
        print(f"  {'setting':24} {'thinking':>9} {'answer':>8} {'eval':>6}  done")
        for name, prompt, think in CASES:
            r = ask(model, prompt, think)
            if "error" in r:
                print(f"  {name:24} {r['error']}")
                continue
            print(f"  {name:24} {r['think_ch']:>9} {r['answer_ch']:>8} "
                  f"{r['eval']:>6}  {r['done']}")


if __name__ == "__main__":
    main(sys.argv[1:] or DEFAULT_MODELS)
