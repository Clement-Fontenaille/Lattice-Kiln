"""How many decode slots are worth having, at THIS model and THIS context size?

    python probe_parallel_slots.py --label 2-slot --concurrency 2
    python probe_parallel_slots.py --label 3-slot --concurrency 3

Measured on qwen2.5-coder 7B q4_K_M at num_ctx 8192, 8 GB card, Ollama/Vulkan:

    slots   solo    n at once, aggregate   per-request       vs solo
      1     66.9    56.2                   65.4 - 67.6       x0.84
      2     65.9    84.9                   56.7 - 57.7       x1.29
      3     66.6   110.4                   46.2 - 46.4       x1.66

Concurrency helps here, and keeps helping to at least three. The signature of a
slot actually being used is the PER-REQUEST rate falling while the sum rises:
at one slot each request still decodes at ~66 and the requests merely queue, so
the aggregate is below solo. At three, each runs at ~46 and the sum is 110.

This is the opposite of M0 entry 1 addendum 5, which measured two concurrent
llama-server slots as a loss -- 34.8 and 17.4 tok/s aggregate against ~47-52
solo. That result stands for its operating point and does not transfer: it was
Nemotron 9B under WSL at 16,384 and 32,768 per slot. Per-slot context is the
variable that turned the sign, so re-measure rather than extrapolate whenever
the model or the ceiling moves.

AGGREGATE is what is reported, not a mean of per-request rates. Three requests
each at a third speed is a wash for a sweep; only the sum says whether it
finishes sooner. Per-request range goes beside it rather than into a mean,
because addendum 5 found 7.0 and 27.8 tok/s on the same pair and a mean would
have printed 17 and hidden the starvation entirely.

Prompts differ in length on purpose. Identical simultaneous prompts are the easy
case for a continuous batcher, and workers in a sweep never send them.

**Restarting Ollama requires killing llama-server, not just ollama.exe.** The
3-slot condition first appeared to OOM at model load:

    ggml_vulkan: Device memory allocation of size 1042118656 failed.
    ErrorOutOfDeviceMemory

It was not a capacity limit. `ollama.exe serve` does not reap its llama-server
children on kill, so three restarts left three orphans holding 5,830 MiB of an
idle 8 GB card, and the next server was allocating against what was left. Kill
`llama-server.exe` too and WAIT for nvidia-smi to drop before restarting;
otherwise a leak reads exactly like a hardware ceiling and gets recorded as one.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "M4-ephemeral-processors"))

import ollama_client as oc  # noqa: E402

PROMPTS = [
    "Write a Python function that merges two sorted lists. Explain each step.",
    "List the trade-offs between a hash map and a balanced tree, with examples.",
    "Describe how a write-ahead log recovers state after a crash, with an example.",
    "Explain when to use a queue rather than a stack, and give two cases of each.",
]


def one(prompt: str, model: str, num_ctx: int, num_predict: int) -> dict:
    t0 = time.monotonic()
    g = oc.generate(prompt, model=model, num_ctx=num_ctx, num_predict=num_predict)
    return {"tok": g.eval_count,
            "decode_s": g.raw.get("eval_duration", 0) / 1e9,
            "wall_s": time.monotonic() - t0,
            "rate": g.tokens_per_s}


def solo(model, num_ctx, num_predict, rounds) -> list[dict]:
    out = []
    for i in range(rounds):
        out.append(one(PROMPTS[i % len(PROMPTS)], model, num_ctx, num_predict))
    return out


def concurrent(model, num_ctx, num_predict, rounds, n) -> list[list[dict]]:
    """`n` genuinely simultaneous requests, `rounds` times.

    More requests than slots is not an error to avoid -- it is the case worth
    measuring, because that is what workers do. The surplus queues, and the
    aggregate says whether queueing behind a batched slot still beats waiting.
    """
    out = []
    for _ in range(rounds):
        with ThreadPoolExecutor(n) as ex:
            futs = [ex.submit(one, PROMPTS[i % len(PROMPTS)], model, num_ctx,
                              num_predict) for i in range(n)]
            out.append([f.result() for f in futs])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen2.5-coder:7b-instruct-q4_K_M")
    ap.add_argument("--num-ctx", type=int, default=8192)
    ap.add_argument("--num-predict", type=int, default=400)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--concurrency", type=int, default=2,
                    help="how many requests to fire at once (default 2)")
    ap.add_argument("--label", default="run")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    print(f"{args.label}: {args.model} @ num_ctx {args.num_ctx}, "
          f"{args.rounds} round(s)\n")

    s = solo(args.model, args.num_ctx, args.num_predict, args.rounds)
    s_rate = statistics.mean(r["rate"] for r in s)
    rates = ", ".join(f"{r['rate']:.1f}" for r in s)
    print(f"solo      {s_rate:6.1f} tok/s   ({rates})")

    n = args.concurrency
    p = concurrent(args.model, args.num_ctx, args.num_predict, args.rounds, n)
    per, agg = [], []
    for group in p:
        per += [r["rate"] for r in group]
        # Aggregate over the group's own wall clock: all start together, so the
        # slowest one's wall is the group's wall. Summing the rates would credit
        # the group for time only one of them was running.
        wall = max(r["wall_s"] for r in group)
        agg.append(sum(r["tok"] for r in group) / wall if wall else 0.0)
    ag = statistics.mean(agg)
    print(f"{n} at once {ag:6.1f} tok/s aggregate   "
          f"per-request {min(per):.1f} to {max(per):.1f}")
    print(f"\nconcurrency {n}: x{ag/s_rate:.2f} aggregate"
          f"   ({'helps' if ag > s_rate else 'costs'})")

    if args.out:
        Path(args.out).write_text(json.dumps(
            {"label": args.label, "model": args.model, "num_ctx": args.num_ctx,
             "concurrency": n, "solo": s, "groups": p,
             "solo_rate": s_rate, "aggregate": ag},
            indent=2), encoding="utf-8")
        print(f"\nwritten to {args.out}")


if __name__ == "__main__":
    main()

# -------------------------------------------------------------- slot ceilings
#
# OLLAMA_NUM_PARALLEL is a MAXIMUM, not a request, and two separate things can
# silently reduce it. Neither is visible through the API -- `/api/ps` reports a
# model 100% resident whether it holds one slot or three. Only the load lines in
# server.log distinguish them:
#
#     Qwen2.5 Coder 7B     n_ctx = 24576   slot id 0 / id 1 / id 2    3 slots
#     NVIDIA Nemotron 9B   n_ctx =  8192   slot id 0                  1 slot
#
# 1. ARCHITECTURE. Ollama 0.34.2 refuses parallelism for nemotron_h outright:
#
#      sched.go:514 "model architecture does not currently support parallel
#      requests" architecture=nemotron_h
#
#    Confirmed downstream: "138.80 MiB (1 cells, 56 layers, 1 seqs 0 rs_seq)".
#    Mamba-2 recurrent state is single-sequence here. No setting changes this,
#    so workers beyond the first can only fill the gaps between calls -- they
#    never decode concurrently. Measured cost: 82% of nemotron's wall time was
#    non-decode at three workers, against 34% for qwen at three real slots,
#    while nemotron's per-stream decode was FASTER (45.2 vs 38.5 tok/s).
#
# 2. MEMORY. LLAMA_ARG_FIT_TARGET is a free-VRAM margin in MiB, default 1024,
#    and the fitter will shed GPU layers to meet it:
#
#      "projected to use 6260 MiB vs. 6981 MiB free"
#      "cannot meet free memory target of 1024 MiB, need to reduce device
#       memory by 303 MiB"
#      "n_gpu_layers already set by user to 99, abort"
#
#    It wanted to offload 303 MiB of nemotron and was overruled only because
#    `PARAMETER num_gpu 99` is pinned in the Modelfile. Unpinned, this is how a
#    model lands on the wrong side of finding 01's residency cliff without
#    anything in the API saying so.
#
# Diagnosing a slot count therefore means reading server.log, not the API. Both
# failure modes -- an architecture that cannot batch, and a fitter quietly
# shedding layers -- present identically as "it is slower than expected".
