"""Every nudge, measured on the stage that actually fails.

WHY THE EARLIER PROBE COULD NOT HAVE WORKED. probe_think_nudge tested six
nudges against the JUDGE prompt. The full-pipeline sweep then showed the judge
never truncates at all -- 67 calls across three arms, none above 582 tokens,
zero at the cap. Every truncation in the pipeline is the IMPLEMENTER. So that
probe measured a stage with no failure mode and found, correctly, nothing; the
non-replication blamed on noise was partly just the wrong stage.

Four of the six nudges were never carried into the pipeline sweep, so their
effect on the tail is unmeasured. Running them through the whole pipeline is
~19 minutes each. Running them against the implementer alone is minutes, and
the failure is stage-local, so that is the instrument -- provided it is
CALIBRATED rather than trusted.

CALIBRATION IS THE POINT. control, first_pass and answer_first are included
even though their pipeline numbers are already known, precisely so the isolated
probe can be checked against them. If it reproduces the pipeline's ordering and
cap rates (8/26, 4/21, 3/28) then the other four can be read off it. If it does
not, the isolated measurement is not a substitute and the four need the full
sweep.

THE PROMPT IS VERBATIM from a stored transcript -- the exact bytes an
implementer call received during the control arm, not a reconstruction. A
reconstruction is what made the judge probe unfalsifiable: it never reproduced
the failure it was built to study.

Reported as the full sorted series, not quantiles. The distribution is bimodal
with a gap between roughly 4900 and the cap, and a quantile table hides exactly
that.

    python probe_implementer_tail.py [--n 20] [--workers 3]
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
from roles import TOOLS  # noqa: E402

BASE = "http://localhost:11434"
MODEL = "nemotron3-nano-4b:latest"
CAP = 8192
NUM_CTX = 16384

PROMPT_FILE = Path(
    r"C:\Users\FONTEN~1\AppData\Local\Temp\claude"
    r"\c--Users-Fontenaille-Desktop-Lattice-Kiln"
    r"\3aae8716-e522-45e4-9759-00cc7847dd6e\scratchpad\impl_prompt.txt")

NUDGES = {
    # already measured through the full pipeline -- these calibrate the probe
    "control": "",
    "first_pass": "Form a judgement on the first pass and write it.",
    "answer_first": ("Write your answer FIRST, then stop. Any reasoning you do "
                     "must fit in a few sentences before it."),
    # never carried into the pipeline; their tail effect is unmeasured
    "be_brief": "Keep your reasoning brief. Reach the answer quickly.",
    "word_budget": ("Think for at most 100 words, then answer. Do not re-check "
                    "work you have already done."),
    "act_not_deliberate": ("You are answering, not deliberating. Form a "
                           "judgement on the first pass and write it. Do not "
                           "second-guess yourself."),
    "no_reverify": ("Do not verify your conclusion more than once. Repeating a "
                    "check you have already made adds nothing -- once each "
                    "condition has an answer, emit the JSON immediately."),
}

_lock = threading.Lock()


def one(prompt: str) -> int:
    body = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
            "tools": TOOLS, "stream": False, "think": True,
            "options": {"temperature": 0.2, "num_ctx": NUM_CTX,
                        "num_predict": CAP}}
    req = urllib.request.Request(
        f"{BASE}/api/chat", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=1800) as r:
            p = json.loads(r.read().decode("utf-8"))
    except urllib.error.URLError:
        return -1
    return p.get("eval_count") or 0


def series(v: list[int]) -> str:
    """Every value, sorted, repeats collapsed. A pile-up at the cap must LOOK
    like a pile-up."""
    v = sorted(x for x in v if x >= 0)
    out, i = [], 0
    while i < len(v):
        j = i
        while j < len(v) and v[j] == v[i]:
            j += 1
        out.append(f"{v[i]}" + (f"x{j - i}" if j - i > 1 else ""))
        i = j
    return "  ".join(out)


def main(argv: list[str]) -> None:
    n, workers = 20, 3
    if "--n" in argv:
        n = int(argv[argv.index("--n") + 1])
    if "--workers" in argv:
        workers = int(argv[argv.index("--workers") + 1])
    base_prompt = PROMPT_FILE.read_text(encoding="utf-8")
    print(f"{MODEL} | implementer stage, verbatim prompt {len(base_prompt)} "
          f"chars | n={n} | cap={CAP}")
    print(f"{len(NUDGES)} nudges x {n} = {len(NUDGES) * n} calls, "
          f"{workers} concurrent\n")

    jobs = [(name, base_prompt + (f"\n\n{txt}" if txt else ""))
            for name, txt in NUDGES.items() for _ in range(n)]
    t0 = time.monotonic()
    res: dict[str, list[int]] = {k: [] for k in NUDGES}

    def run(job):
        name, prompt = job
        v = one(prompt)
        with _lock:
            res[name].append(v)
        return v

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(run, jobs))
    print(f"wall {(time.monotonic() - t0) / 60:.1f} min\n")

    for name in NUDGES:
        v = [x for x in res[name] if x >= 0]
        cap = sum(1 for x in v if x >= CAP - 8)
        tag = "  <- calibration" if name in (
            "control", "first_pass", "answer_first") else ""
        print(f"{name:20} cap {cap:>2}/{len(v):<3}{tag}")
        print(f"  {series(v)}")
    print(f"\ncap = {CAP}, i.e. the call never terminated. The distribution is "
          f"bimodal:\nconvergent calls finish well under ~3000, and anything "
          f"that passes ~5000 runs to the cap.")


if __name__ == "__main__":
    main(sys.argv[1:])
