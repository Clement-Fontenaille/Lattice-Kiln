"""Run the attractor census.

For each probe, sample the working-default 7B K times at moderate temperature
(we want the spread of the motion, not one point). Dump every raw transcript and
a row of cheap structural observations per call. The census FINDINGS doc is then
hand-written from the transcripts - these observations only triage where to look.

    python run_census.py           # full matrix, K=3
    python run_census.py --k 2 --only doer
    python run_census.py --smoke   # 3 probes, K=1
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "M4-ephemeral-processors"))

from ollama_client import DEFAULT_MODEL, generate, health  # noqa: E402
from probes import build  # noqa: E402

RUNS = HERE / "runs"
OBS = HERE / "observations.jsonl"
SUMMARY = HERE / "summary.md"

TEMPERATURE = 0.4
NUM_PREDICT = 900

# --- cheap structural observations (regex, no model) ------------------------

# the model often turns the marker into a comment or drops the <<< >>>, or
# wraps the whole thing in a ```fence - catch those forms too
_FILE = re.compile(r"(?:<<<\s*|#\s*<*\s*)FILE\s+path[=:]\s*([^\s>`]+)", re.I)
_CTRL = re.compile(r"<<<\s*CONTROL\s*>>>(.*?)<<<\s*ENDCONTROL\s*>>>", re.I | re.S)
_FENCE = re.compile(r"```")
_NUMBERED = re.compile(r"^\s{0,4}\d+[\.\)]\s+\S", re.M)
_PAST_DONE = re.compile(
    r"\b(fixed|updated|implemented|added|resolved|corrected|has been|have been|"
    r"now passes|all tests pass|is now|have now|i have|i've)\b", re.I)
_HEDGE = re.compile(
    r"\b(i think|i believe|probably|might be|may be|possibly|not sure|"
    r"cannot be sure|without running|i assume|assuming|it seems|appears to)\b", re.I)
_REFUSAL = re.compile(
    r"\b(cannot|can't|can not|unable to|impossible|not possible|"
    r"need more (info|context|information)|insufficient (info|context)|"
    r"not feasible|would be wrong|would be incorrect)\b", re.I)
_PASS_TOKEN = re.compile(r"^\s*(PASS|NO DEFECT FOUND|NONE)\s*$", re.M | re.I)


def _control_fields(text: str) -> dict:
    m = _CTRL.search(text)
    blob = m.group(1) if m else ""
    if not blob:
        # fallback: last {...} containing terminal_state or verdict
        cands = re.findall(r"\{[^{}]*(?:terminal_state|verdict)[^{}]*\}", text, re.S)
        blob = cands[-1] if cands else ""
    ts = vd = None
    if blob:
        mt = re.search(r'"terminal_state"\s*:\s*"([a-z]+)"', blob)
        mv = re.search(r'"verdict"\s*:\s*"([a-z-]+)"', blob)
        ts = mt.group(1) if mt else None
        vd = mv.group(1) if mv else None
    return {"control_block": bool(m), "terminal_state": ts, "verdict": vd}


def observe(probe, text: str) -> dict:
    lines = text.splitlines()
    paths = _FILE.findall(text)
    o = {
        "n_chars": len(text),
        "n_lines": len(lines),
        "file_blocks": len(paths),
        "file_paths": sorted(set(paths)),
        "code_fences": len(_FENCE.findall(text)) // 2,
        "numbered_items": len(_NUMBERED.findall(text)),
        "past_done_hits": len(_PAST_DONE.findall(text)),
        "hedge_hits": len(_HEDGE.findall(text)),
        "refusal_hits": len(_REFUSAL.findall(text)),
        "pass_token": bool(_PASS_TOKEN.search(text)),
    }
    o.update(_control_fields(text))

    t = probe.task
    low = text.lower()
    if t in ("fix_indirection", "fix_local", "plan_indirection", "review_wf1_correct",
             "review_wf1_empty"):
        o["mentions_qty"] = "qty" in low
        o["touches_pricing"] = any("pricing" in p for p in paths)
        o["touches_orders_only"] = (any("orders" in p for p in paths)
                                    and not any("pricing" in p for p in paths))
    if t in ("refactor_trap", "review_wf3_correct", "review_wf3_broken"):
        o["mentions_round"] = "round" in low
        o["mentions_exact_or_staff"] = ("exact" in low or "staff_price" in low)
    if t in ("false_premise", "plan_false_premise"):
        o["mentions_sorted_precond"] = bool(re.search(
            r"sorted|not guaranteed|precondition|assumption|unsorted", low))
        o["did_binary_search"] = bool(re.search(r"bisect|binary search|mid\s*=|lo\s*,\s*hi", low))
    if t in ("multi_concern", "plan_multi"):
        o["mentions_docstring"] = "docstring" in low
        o["mentions_notes_md"] = "notes.md" in low
        o["mentions_todo"] = "todo" in low
        o["all_three_concerns"] = all((
            "topo_sort" in low or "topological" in low,
            "docstring" in low,
            "todo" in low,
        ))
        if paths:
            src = text  # crude: did the emitted file still carry stale markers
            o["kept_todo_2019"] = "TODO(2019)" in src
            o["kept_on2"] = "O(n^2)" in src or "O(n**2)" in src
    return o


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--only", choices=["doer", "judge", "plan"], default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    if not health():
        print("Ollama not reachable at localhost:11434", file=sys.stderr)
        sys.exit(1)

    probes = build()
    if args.only:
        probes = [p for p in probes if p.group == args.only]
    k = args.k
    if args.smoke:
        probes = [probes[0], probes[len(probes) // 2], probes[-1]]
        k = 1

    RUNS.mkdir(parents=True, exist_ok=True)
    if OBS.exists() and not args.smoke:
        OBS.unlink()

    print(f"model={DEFAULT_MODEL}  probes={len(probes)}  k={k}  "
          f"calls={len(probes) * k}  temp={TEMPERATURE}")
    t_start = time.monotonic()
    rows: list[dict] = []
    for i, p in enumerate(probes, 1):
        for j in range(k):
            t0 = time.monotonic()
            try:
                g = generate(p.prompt, temperature=TEMPERATURE, num_predict=NUM_PREDICT)
                text, err = g.text, None
            except Exception as e:  # noqa: BLE001
                text, err = "", repr(e)
                g = None
            wall = time.monotonic() - t0
            (RUNS / f"{p.id}__k{j}.txt").write_text(
                f"### PROBE {p.id}  (group={p.group} task={p.task} framing={p.framing})\n"
                f"### note: {p.note}\n"
                f"### --- PROMPT ---\n{p.prompt}\n"
                f"### --- RESPONSE (k={j}) ---\n{text}\n", encoding="utf-8")
            row = {
                "probe": p.id, "group": p.group, "task": p.task,
                "framing": p.framing, "k": j, "error": err,
                "wall_s": round(wall, 1),
                "prompt_tok": getattr(g, "prompt_eval_count", 0) if g else 0,
                "gen_tok": getattr(g, "eval_count", 0) if g else 0,
                "tok_s": round(g.tokens_per_s, 1) if g else 0.0,
            }
            if not err:
                row.update(observe(p, text))
            rows.append(row)
            with OBS.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(row) + "\n")
            flag = "ERR" if err else (row.get("terminal_state") or row.get("verdict") or
                                      f"{row.get('file_blocks', 0)}f")
            print(f"  [{i:2}/{len(probes)}] {p.id:34} k{j} {wall:5.1f}s {flag}")

    dur = time.monotonic() - t_start
    _write_summary(rows, dur)
    print(f"\ndone in {dur/60:.1f} min -> {SUMMARY}")


def _agg(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return "-"
    if all(isinstance(v, bool) for v in vals):
        return f"{sum(vals)}/{len(vals)}"
    if all(isinstance(v, (int, float)) for v in vals):
        return f"{sum(vals) / len(vals):.1f}"
    from collections import Counter
    return ",".join(f"{k}:{n}" for k, n in Counter(map(str, vals)).most_common())


def _write_summary(rows: list[dict], dur: float) -> None:
    by_probe: dict[str, list[dict]] = {}
    for r in rows:
        by_probe.setdefault(r["probe"], []).append(r)

    keys_by_group = {
        "doer": ["file_blocks", "terminal_state", "past_done_hits", "hedge_hits",
                 "refusal_hits", "touches_pricing", "touches_orders_only",
                 "mentions_round", "did_binary_search", "mentions_sorted_precond",
                 "all_three_concerns", "kept_todo_2019", "gen_tok"],
        "judge": ["verdict", "numbered_items", "pass_token", "hedge_hits",
                  "mentions_round", "mentions_qty", "mentions_exact_or_staff", "gen_tok"],
        "plan": ["terminal_state", "numbered_items", "refusal_hits",
                 "mentions_sorted_precond", "all_three_concerns",
                 "touches_orders_only", "gen_tok"],
    }
    out = [f"# Attractor census - raw observation table",
           f"_model {DEFAULT_MODEL}, temp {TEMPERATURE}, {len(rows)} calls, "
           f"{dur/60:.1f} min_", "",
           "Booleans shown as hits/samples. Read the transcripts in `runs/` for "
           "the actual motion - this table only says where to look.", ""]
    for grp in ("doer", "judge", "plan"):
        gp = [p for p in by_probe if by_probe[p][0]["group"] == grp]
        if not gp:
            continue
        ks = keys_by_group[grp]
        out += [f"## {grp}", "", "| probe | " + " | ".join(ks) + " |",
                "|" + "---|" * (len(ks) + 1)]
        for p in gp:
            rs = by_probe[p]
            cells = [_agg([r.get(k) for r in rs]) for k in ks]
            out.append(f"| {p} | " + " | ".join(cells) + " |")
        out.append("")
    SUMMARY.write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
