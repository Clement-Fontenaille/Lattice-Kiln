"""Does anything make `conclude` arrive as a call rather than as prose?

THE PROBLEM, LOCATED. In 38 monolith runs the model emitted write_file as a
parsed call 30 times and conclude 27 times; the 11 misses all came after a
successful write_file in the same sequence, so the format was available to it.

AND IT IS NOT A FORMAT MISMATCH. Ollama's renderer is a byte-identical
transcription of NVIDIA's own chat_template.jinja for this model, instruction
block included (817 chars, verified). The syntax we demand is the model's own.

WHAT THE TEMPLATE DOES AND DOES NOT DO. It specifies the syntax and explicitly
permits not calling:

    "If you choose to call a function ONLY reply in the following format..."
    "- If there is no function call available, answer the question like normal
       with your current knowledge and do not tell the user about function calls"

Permissive, with an escape hatch. NOTHING in it nudges toward taking an action.
The only push in that direction is one line we add, in the USER turn, under
2354 characters of system-turn specification. Cline-style prompts assert it far
harder, so the wording and the PLACEMENT are both worth varying.

FOUR ARMS, one variable each:

    control      the rewritten protocol, mild nudge, in the user turn
    no_action    that line deleted -- what NVIDIA's text alone produces
    strong       an assertive nudge, cline-shaped
    in_system    control's text moved to the SYSTEM message, which the renderer
                 emits BEFORE the tools block: placement, not wording

Measured per arm: did conclude arrive as a parsed call, did write_file, and how
many turns it took. A run that writes the file and loses it to a prose
conclusion is the failure being counted.

    python probe_action_nudge.py [--n 10] [--workers 3]
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
from roles import PROTOCOL_TOOLS, TOOLS, prompt_for  # noqa: E402
from probe_record import persist                      # noqa: E402

BASE = "http://localhost:11434"
MODEL = "nemotron3-nano-4b:latest"
CAP = 4096
NUM_CTX = 16384
_lock = threading.Lock()

OLD_PROTOCOL = """OUTPUT FORMAT - use the provided tools, not prose.

For every file you create or change, call write_file with the path and the
WHOLE new file content (never a diff).

Then call conclude exactly once, as the last thing you do.
"""

#: The rule that directly contradicted NVIDIA's "answer the question like
#: normal" escape hatch. Kept separate so the two claims can be varied apart.
OLD_RULES = """
Rules:
- conclude is required on every turn, including when you write no files.
"""

ACTION_LINE = ("Do the work by calling the tools. Do not describe changes in "
               "prose.")
STRONG_LINE = ("You MUST reply with a tool call. Every reply is a tool call and "
               "nothing else. Never describe what you would do -- do it.")

OBJECTIVE = ("Add a `retries` parameter to Client.call(fn, retries=2): if fn() "
             "raises, retry up to `retries` more times; if every attempt fails, "
             "re-raise the LAST exception. retries=0 means a single attempt.")
CONTEXT = """----- client.py -----
class Client:
    def __init__(self):
        self.calls = 0

    def call(self, fn):
        self.calls += 1
        return fn()
"""


def variants() -> dict[str, tuple[str, str | None]]:
    """-> {name: (user_prompt, system_prompt_or_None)}"""
    base = PROTOCOL_TOOLS
    no_action = base.replace(ACTION_LINE + "\n\n", "")
    strong = base.replace(ACTION_LINE, STRONG_LINE)
    mk = lambda proto: prompt_for("implementer", CONTEXT, OBJECTIVE, protocol=proto)
    # in_system: the protocol leaves the user turn entirely and is passed as the
    # system message, which the renderer writes before the tools block.
    user_no_proto = mk("").rstrip()
    # THE CONFOUND THE FIRST RUN HAD. Its control used the REWRITTEN protocol,
    # so 39/40 native conclusions could not be attributed -- the rewrite and the
    # nudge variants moved together. This arm is the text that actually produced
    # 11/38 prose conclusions in the sweep, so the rewrite is testable against
    # the thing it replaced.
    old = OLD_PROTOCOL + OLD_RULES
    return {
        "old_proto": (mk(old), None),
        "control":   (mk(base), None),
        "no_action": (mk(no_action), None),
        "strong":    (mk(strong), None),
        "in_system": (user_no_proto, base),
    }


def run_loop(user: str, system: str | None, max_turns: int = 4) -> dict:
    msgs: list[dict] = ([{"role": "system", "content": system}] if system else [])
    msgs.append({"role": "user", "content": user})
    wrote = concluded = False
    turns = 0
    prose_conclude = False
    per_turn = []                 # raw, per request: persisted, not summarised
    for _ in range(max_turns):
        body = {"model": MODEL, "messages": msgs, "tools": TOOLS, "stream": False,
                "think": True,
                "options": {"temperature": 0.6, "top_p": 0.95,
                            "num_ctx": NUM_CTX, "num_predict": CAP}}
        req = urllib.request.Request(
            f"{BASE}/api/chat", data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                p = json.loads(r.read().decode("utf-8"))
        except urllib.error.URLError:
            return {"err": True}
        m = p.get("message") or {}
        turns += 1
        calls = [(c.get("function") or {}).get("name")
                 for c in (m.get("tool_calls") or [])]
        text = m.get("content") or ""
        per_turn.append({"calls": calls,
                         "prompt_eval_count": p.get("prompt_eval_count"),
                         "eval_count": p.get("eval_count"),
                         "done_reason": p.get("done_reason"),
                         "thinking_chars": len(m.get("thinking") or ""),
                         "content": text})
        if not calls:
            # the failure being counted: a conclusion written as prose
            if '"terminal_state"' in text or "<function=conclude" in text:
                prose_conclude = True
            break
        msgs.append({"role": "assistant", "content": text,
                     "tool_calls": m.get("tool_calls") or []})
        for c in calls:
            if c == "write_file":
                wrote = True
            if c == "conclude":
                concluded = True
            msgs.append({"role": "tool", "tool_name": c,
                         "content": '{"status": "accepted"}'})
        if concluded:
            break
    return {"wrote": wrote, "concluded": concluded, "turns": turns,
            "prose_conclude": prose_conclude, "per_turn": per_turn}


def main(argv: list[str]) -> None:
    n, workers = 10, 3
    if "--n" in argv:
        n = int(argv[argv.index("--n") + 1])
    if "--workers" in argv:
        workers = int(argv[argv.index("--workers") + 1])
    vs = variants()
    print(f"{MODEL} | temp 0.6/0.95 | n={n} | {len(vs)} arms")
    for k, (u, s) in vs.items():
        print(f"  {k:10} user={len(u)}ch system={len(s) if s else 0}ch")
    print()
    res: dict[str, list[dict]] = {k: [] for k in vs}
    jobs = [(k,) * 1 for k in vs for _ in range(n)]

    def go(j):
        k = j[0]
        u, s = vs[k]
        r = run_loop(u, s)
        with _lock:
            res[k].append(r)

    t0 = time.monotonic()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(go, jobs))
    print(f"wall {(time.monotonic() - t0) / 60:.1f} min\n")
    print(f"  {'arm':10}{'wrote':>8}{'concluded':>11}{'prose-concl':>13}{'mean turns':>12}")
    for k in vs:
        ok = [r for r in res[k] if not r.get("err")]
        if not ok:
            print(f"  {k:10} all failed")
            continue
        w = sum(1 for r in ok if r["wrote"])
        c = sum(1 for r in ok if r["concluded"])
        pc = sum(1 for r in ok if r["prose_conclude"])
        mt = sum(r["turns"] for r in ok) / len(ok)
        print(f"  {k:10}{w:>6}/{len(ok)}{c:>9}/{len(ok)}{pc:>11}/{len(ok)}{mt:>12.1f}")
    print("\n  concluded = conclude arrived as a PARSED call. prose-concl = the "
          "model wrote its\n  conclusion as text instead, which is the case that "
          "discards the work.")
    # Timestamped now, where it used to overwrite a fixed action_nudge.json.
    persist("action_nudge", {"model": MODEL, "cap": CAP, "num_ctx": NUM_CTX,
                             "temperature": 0.6, "top_p": 0.95, "think": True,
                             "n": n, "variants": {k: {"user": u, "system": s}
                                                  for k, (u, s) in vs.items()}},
            [{"arm": k, **r} for k in vs for r in res[k]])


if __name__ == "__main__":
    main(sys.argv[1:])
