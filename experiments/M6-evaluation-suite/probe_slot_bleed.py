"""Does a shared model instance leak between CONCURRENT requests?

probe_run_order.py settled the sequential case: handing the model the answer in
the immediately preceding request leaves the next answer byte-identical, with a
detector that provably fires. This is the case it could not reach.

Under OLLAMA_NUM_PARALLEL several requests share one loaded model and compete
for KV cache slots. That is a different mechanism from sequential prefix reuse,
and it is how the corpus behind 50-findings/12 and /14 was gathered -- three
slots, up to three workers. No particular reason to suspect it; every reason to
check it once rather than carry it as an assumption.

THE DESIGN. 20 copies of A and 20 copies of B_RELATED, interleaved, fired over
3 concurrent workers. A is deterministic at temperature 0 with a fixed seed and
its correct hash is already known from the sequential run. B_RELATED contains
the answer to A plus two identifiers no model emits unprompted. So a leak shows
up two ways: an A whose hash differs from baseline, or an A containing a marker.

THE CONTROL THAT MAKES IT READABLE. If the server serialises the requests, they
never share anything and a null result means nothing at all. So actual overlap
is measured -- start and end timestamps per request, and the maximum number in
flight at once. A run whose observed concurrency is 1 is reported as INVALID
rather than as evidence of no leak.

RESULT, 2026-09-23, nemotron3-nano-4b, 20 A + 20 B over 3 workers, twice:

                              disjoint    shared prefix (60%, mid-script)
      peak concurrency           3             3
      A co-resident with a B    20/20         20/20   (mean 2.0 Bs per A)
      detector live on B        20/20         20/20
      A matching baseline       20/20         20/20
      A carrying a marker        0/20          0/20

NO BLEED, by either mechanism, with every invalidation condition cleared.

The shared-prefix variant is the one that speaks to the corpus: 1827 characters
of identical script, diverging in the MIDDLE, which is the configuration where a
slot could serve a cached prefix with the wrong continuation attached. Each A
ran with two marker-bearing Bs resident and came back byte-identical to the
sequential baseline.

STILL UNTESTED: only the 4B was run concurrently, and only on Ollama. A second
model would cost four minutes and has not been spent.

    python probe_slot_bleed.py [model] [--n 20] [--workers 3] [--prefix]
"""
from __future__ import annotations

import hashlib
import json
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from probe_run_order import A, B_RELATED, MARKER_ID, MARKER_NOTE  # noqa: E402

# --prefix swaps in a pair that SHARES A LONG PREFIX and diverges in the
# middle. The default pair shares nothing, so it exercises slot contention
# between unrelated prompts and cannot reach prefix-cache reuse at all -- which
# is the mechanism the real harness leans on, every rep of a cell sending an
# identical preamble and differing only in its tail.
import probe_shared_prefix as _sp  # noqa: E402
from probe_record import persist  # noqa: E402

BASE = "http://localhost:11434"
_lock = threading.Lock()
_events: list[tuple[float, float, str]] = []


def call(model: str, prompt: str, tag: str, num_predict: int) -> dict:
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0, "top_p": 1, "seed": 0,
                        "num_ctx": 8192, "num_predict": num_predict}}
    req = urllib.request.Request(
        f"{BASE}/api/chat", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    t0 = time.monotonic()
    with urllib.request.urlopen(req, timeout=900) as r:
        p = json.loads(r.read().decode("utf-8"))
    t1 = time.monotonic()
    with _lock:
        _events.append((t0, t1, tag))
    txt = (p.get("message") or {}).get("content") or ""
    return {"tag": tag,
            "sha": hashlib.sha256(txt.encode()).hexdigest()[:12],
            "marker": (MARKER_ID in txt) or (MARKER_NOTE in txt),
            "etok": p.get("eval_count"), "text": txt,
            "prompt_eval_count": p.get("prompt_eval_count"),
            "done_reason": p.get("done_reason"),
            "t0": t0, "t1": t1}


def max_in_flight() -> int:
    """Peak simultaneous requests, from the recorded intervals."""
    pts = []
    for t0, t1, _ in _events:
        pts.append((t0, 1))
        pts.append((t1, -1))
    pts.sort()
    cur = peak = 0
    for _, d in pts:
        cur += d
        peak = max(peak, cur)
    return peak


def co_residency() -> tuple[int, int, float]:
    """How many A requests were in flight AT THE SAME TIME as some B?

    Submitting A and B alternately is not the same as running them together.
    The pool hands work out in order, but A and B generate different numbers of
    tokens, so the mix actually resident in the slots drifts as they finish at
    different rates. If it drifted such that every A shared its slots only with
    other As, nothing was ever adjacent to a marker and a clean result would be
    vacuous.

    So the condition the test needs is measured rather than argued from the
    submission order: for each A, whether its interval overlaps any B's.
    Returns (overlapped, total A, mean Bs concurrent per A).
    """
    a = [(t0, t1) for t0, t1, tag in _events if tag.startswith("A")]
    b = [(t0, t1) for t0, t1, tag in _events if tag.startswith("B")]
    overlapped, total_b = 0, 0
    for s0, s1 in a:
        k = sum(1 for o0, o1 in b if o0 < s1 and s0 < o1)
        total_b += k
        if k:
            overlapped += 1
    return overlapped, len(a), (total_b / len(a) if a else 0.0)


def main(argv: list[str]) -> None:
    n, workers = 20, 3
    if "--n" in argv:
        i = argv.index("--n"); n = int(argv[i + 1]); argv = argv[:i] + argv[i + 2:]
    if "--workers" in argv:
        i = argv.index("--workers"); workers = int(argv[i + 1]); argv = argv[:i] + argv[i + 2:]
    prompt_a, prompt_b, mode = A, B_RELATED, "disjoint prompts"
    if "--prefix" in argv:
        argv = [x for x in argv if x != "--prefix"]
        prompt_a, prompt_b = _sp.A, _sp.B_RELATED
        mode = (f"SHARED PREFIX {_sp.shared_prefix_chars()} chars "
                f"({100 * _sp.shared_prefix_chars() // len(_sp.A)}% of A), "
                f"diverging mid-script")
    model = argv[0] if argv else "nemotron3-nano-4b:latest"

    print(f"{model} | {n} A + {n} B_related | {workers} workers | {mode}")
    print("establishing the sequential baseline for A first...")
    base = call(model, prompt_a, "baseline", 400)
    _events.clear()
    print(f"  baseline A = {base['sha']}")

    jobs = []
    for i in range(n):
        jobs.append((prompt_a, f"A{i}", 400))
        jobs.append((prompt_b, f"B{i}", 500))    # interleaved, not batched

    t0 = time.monotonic()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = list(ex.map(lambda j: call(model, j[0], j[1], j[2]), jobs))
    wall = time.monotonic() - t0

    peak = max_in_flight()
    persist("slot_bleed", {"model": model, "n": n, "workers": workers,
                           "mode": mode, "wall_s": wall, "peak_concurrency": peak,
                           "baseline": base},
            res)
    a = [r for r in res if r["tag"].startswith("A")]
    b = [r for r in res if r["tag"].startswith("B")]
    bad_sha = [r for r in a if r["sha"] != base["sha"]]
    leaked = [r for r in a if r["marker"]]
    b_echo = sum(1 for r in b if r["marker"])

    ov, na, mean_b = co_residency()
    print(f"\n  wall {wall:.1f}s | peak concurrency observed: {peak}")
    print(f"  A sharing the model with a B: {ov}/{na} "
          f"(mean {mean_b:.1f} Bs concurrent per A)")
    if ov < na:
        print(f"  note: {na - ov} A(s) ran with no B resident; those carry no "
              f"information either way")
    if ov == 0:
        print("  *** INVALID: no A ever overlapped a B, so nothing was ever "
              "adjacent to a marker. ***")
    if peak < 2:
        print("  *** INVALID: requests did not overlap. The server serialised "
              "them, so nothing was shared and this says nothing about slot "
              "bleed. Check OLLAMA_NUM_PARALLEL. ***")
    print(f"  positive control: {b_echo}/{len(b)} B replies echoed the marker "
          f"{'(detector works)' if b_echo else '(DETECTOR DEAD - null result meaningless)'}")
    print(f"  A hashes matching baseline : {len(a) - len(bad_sha)}/{len(a)}")
    print(f"  A replies carrying a marker: {len(leaked)}/{len(a)}")
    for r in bad_sha[:3]:
        print(f"    differing {r['tag']}: {r['sha']} ({r['etok']}tok)")
        print(f"      {r['text'][:200]!r}")
    for r in leaked[:3]:
        print(f"    LEAK in {r['tag']}: {r['text'][:300]!r}")
    verdict = ("NO BLEED" if not bad_sha and not leaked
               else "BLEED DETECTED")
    valid = peak >= 2 and b_echo and ov > 0
    print(f"\n  {verdict}"
          + ("" if valid else "  (but see the invalidations above)"))


if __name__ == "__main__":
    main(sys.argv[1:])
