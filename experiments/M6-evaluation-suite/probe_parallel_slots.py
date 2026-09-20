"""Does a second decode slot help or hurt, at THIS model and THIS context size?

    # with the server as it is (OLLAMA_NUM_PARALLEL unset -> 1)
    python probe_parallel_slots.py --label 1-slot

    # then restart ollama with OLLAMA_NUM_PARALLEL=2 and
    python probe_parallel_slots.py --label 2-slot

M0 entry 1 addendum 5 answered this for Nemotron on llama-server at 16,384 and
32,768 per slot: two concurrent slots delivered 34.8 and 17.4 tok/s aggregate
against ~47-52 solo, so concurrency cost more than it won. That measurement
stands, and it does not transfer here. It differs in the model (Nemotron 9B,
not qwen 7B), the runtime (llama-server under WSL, not Ollama on Windows) and
the per-slot context (16k/32k, not 8,192). Smaller contexts batch better, so
the penalty at 2x8k could be milder, absent, or reversed -- the direction is
established for that operating point, not for this one.

What is measured is AGGREGATE decode, not per-request. Two requests each at
half speed is a wash for a sweep and a regression for a user; only the sum
says whether a second slot is worth the VRAM. Per-request rates are reported
beside it because addendum 5 found them wildly asymmetric (7.0 against 27.8 on
the same pair), and a mean would have hidden that.

Prompts are made unequal on purpose. Identical prompts arriving together is the
easy case for a batcher; a sweep never looks like that, because two workers are
at different points of different tasks.
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


def paired(model, num_ctx, num_predict, rounds) -> list[list[dict]]:
    """Two genuinely simultaneous requests, `rounds` times."""
    out = []
    for _ in range(rounds):
        with ThreadPoolExecutor(2) as ex:
            futs = [ex.submit(one, p, model, num_ctx, num_predict) for p in PROMPTS]
            out.append([f.result() for f in futs])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen2.5-coder:7b-instruct-q4_K_M")
    ap.add_argument("--num-ctx", type=int, default=8192)
    ap.add_argument("--num-predict", type=int, default=400)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--label", default="run")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    print(f"{args.label}: {args.model} @ num_ctx {args.num_ctx}, "
          f"{args.rounds} round(s)\n")

    s = solo(args.model, args.num_ctx, args.num_predict, args.rounds)
    s_rate = statistics.mean(r["rate"] for r in s)
    rates = ", ".join(f"{r['rate']:.1f}" for r in s)
    print(f"solo      {s_rate:6.1f} tok/s   ({rates})")

    p = paired(args.model, args.num_ctx, args.num_predict, args.rounds)
    per, agg = [], []
    for pair in p:
        per += [r["rate"] for r in pair]
        # Aggregate over the pair's own wall clock: both start together, so the
        # slower one's wall is the pair's wall. Summing the two rates would
        # credit the pair for time only one of them was running.
        wall = max(r["wall_s"] for r in pair)
        agg.append(sum(r["tok"] for r in pair) / wall if wall else 0.0)
    a = statistics.mean(agg)
    print(f"2 at once {a:6.1f} tok/s aggregate   "
          f"per-request {min(per):.1f} to {max(per):.1f}")
    print(f"\nsecond slot: x{a/s_rate:.2f} aggregate"
          f"   ({'helps' if a > s_rate else 'costs'})")

    if args.out:
        Path(args.out).write_text(json.dumps(
            {"label": args.label, "model": args.model, "num_ctx": args.num_ctx,
             "solo": s, "paired": p, "solo_rate": s_rate, "pair_aggregate": a},
            indent=2), encoding="utf-8")
        print(f"\nwritten to {args.out}")


if __name__ == "__main__":
    main()
