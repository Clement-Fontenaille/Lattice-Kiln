"""E1 first move — does context blur generalise past wf6?

Implements experiments/E1-context-pathology-probe/PROTOCOL.md steps 2-3.
Stdlib only. Does NOT read results_nemotron_llamacpp/ (see E2 PROTOCOL step 0).
"""
from __future__ import annotations

import json
import collections
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT / "experiments/M6-evaluation-suite"
PIPELINE_LAB = ROOT / "experiments/M5-intelligent-orchestration/pipeline_lab/results/results.json"
OUT = Path(__file__).resolve().parent / "results"

# Salience tiers, fixed BEFORE looking at any score (PROTOCOL step 1).
CORE_DIMS = {"SUBTESTS"}          # plus final_sub, handled separately
LOW_DIMS = {"DOCSCORE", "TODOSCORE"}
# STRUCTSCORE/PERFSCORE/AUDITSCORE are neither the gate nor obviously peripheral.
# Excluding them is a choice, recorded here rather than made silently.
EXCLUDED_DIMS = {"STRUCTSCORE", "PERFSCORE", "AUDITSCORE"}

# Arms run before the 2026-09-15 num_ctx cut used 16384; after, 8192.
# Source: experiments/M4-ephemeral-processors/ollama_client.py module docstring.
CTX_16K = {"baseline", "test_synth", "judge_anchored", "m7f", "judge_fullctx"}


def as_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        if v == "True":
            return True
        if v == "False":
            return False
    raise ValueError(f"not a boolean: {v!r}")


def rate(pair):
    if not pair:
        return None
    earned, total = pair
    return (earned / total) if total else None


def classify(core, low, hi=0.8, lo=0.5):
    """Which of the four patterns does this row show?"""
    if core is None or low is None:
        return "incomplete"
    if core >= hi and low < lo:
        return "blur"            # core holds, periphery dropped -- the claim
    if core < hi and low >= hi:
        return "inverse"         # periphery holds, core dropped
    if core >= hi and low >= hi:
        return "both_hold"
    if core < hi and low < lo:
        return "both_drop"       # global failure, NOT the blur mechanism
    return "mixed"


def part_a():
    rows = json.loads(PIPELINE_LAB.read_text(encoding="utf-8"))
    out = []
    for r in rows:
        core = (r["final_sub"] / r["sub_tot"]) if r.get("sub_tot") else None
        dims = [d for d in (r.get("doc"), r.get("todo")) if d]
        low = sum(rate(d) for d in dims) / len(dims) if dims else None
        out.append({
            "task": r["task"], "rep": r["rep"],
            "core": round(core, 3) if core is not None else None,
            "low": round(low, 3) if low is not None else None,
            "doc": r.get("doc"), "todo": r.get("todo"),
            "objective_pass": r["objective_pass"],
            "total_calls": r.get("total_calls"),
            "pattern": classify(core, low),
        })
    return out


def part_b():
    out = []
    for p in sorted((SUITE / "results").glob("*.json")):
        arm = p.stem
        for r in json.loads(p.read_text(encoding="utf-8")):
            struct = r.get("struct") or {}
            low_dims = {k: v for k, v in struct.items() if k in LOW_DIMS}
            if not low_dims:
                continue
            fs = r.get("final_sub")
            core = rate(fs) if fs else None
            low = sum(rate(v) for v in low_dims.values()) / len(low_dims)
            n_dims = len(struct) + 1
            out.append({
                "arm": arm, "task": r["task"], "rep": int(r["rep"]),
                "core": round(core, 3) if core is not None else None,
                "low": round(low, 3),
                "gap": round(core - low, 3) if core is not None else None,
                "dims": low_dims,
                "objective_pass": as_bool(r["objective_pass"]),
                "pattern": classify(core, low),
                "L1_requirement_count": n_dims,
                "L2_worker_view": r.get("worker_view"),
                "L3_ctx_budget": 16384 if arm in CTX_16K else 8192,
            })
    return out


def corr(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = (sum((x - mx) ** 2 for x in xs) / n) ** 0.5
    sy = (sum((y - my) ** 2 for y in ys) / n) ** 0.5
    if sx == 0 or sy == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (n * sx * sy)


def main():
    OUT.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()

    # ---------------- Part A
    a = part_a()
    wf6 = [r for r in a if r["task"] == "wf6_multi"]
    lines = ["# E1 Part A — the anecdote, checked", "", f"Generated {now}.", "",
             f"Source: `{PIPELINE_LAB.relative_to(ROOT)}` (M5 pipeline_lab, 6 wf tasks x 2 reps).", "",
             "| task | rep | core | doc | todo | low | objective_pass | pattern |",
             "|---|---|---|---|---|---|---|---|"]
    for r in a:
        lines.append(f"| {r['task']} | {r['rep']} | {r['core']} | {r['doc']} | {r['todo']} "
                     f"| {r['low']} | {r['objective_pass']} | {r['pattern']} |")
    lines += ["", "## Does the anecdote reproduce here?", "",
              "**No — not in this file.** In the pipeline_lab arm `wf6_multi` scores "
              f"doc {wf6[0]['doc']}/{wf6[1]['doc']} and todo {wf6[0]['todo']}/{wf6[1]['todo']} — "
              "well, not dropped. The 0/4, 0/3 figure belongs to a different arm; see Part B.", "",
              "Only `wf6_multi` carries doc/todo dimensions at all in this file. The other five "
              "`wf*` tasks have `doc: null, todo: null`, so **the direction cannot be compared "
              "across tasks here** — there is nothing to compare against."]
    (OUT / "blur_partA.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---------------- Part B
    b = part_b()
    pats = collections.Counter(r["pattern"] for r in b)
    tasks = sorted({r["task"] for r in b})
    by_arm = collections.defaultdict(list)
    for r in b:
        by_arm[r["arm"]].append(r)

    lines = ["# E1 Part B — does it hold across the M6 corpus?", "", f"Generated {now}.", "",
             "Rows are M6 results carrying a low-salience dimension (`DOCSCORE`/`TODOSCORE`).",
             f"**Tasks carrying any such dimension: {len(tasks)} — {', '.join(tasks)}**", "",
             f"Rows analysed: **{len(b)}** across {len(by_arm)} arms.", "",
             "## Pattern distribution", "",
             "`blur` = core >= 0.8 and low < 0.5 (the claim). `both_drop` = both below "
             "threshold (ordinary global failure, NOT the claim). `inverse` = periphery "
             "holds while core drops.", "",
             "| pattern | rows | share |", "|---|---|---|"]
    for k, v in pats.most_common():
        lines.append(f"| {k} | {v} | {v/len(b):.1%} |")

    lines += ["", "## The motivating anecdote, located", ""]
    mono = [r for r in b if r["arm"] == "monolith" and r["task"] == "wf6_multi"]
    for r in mono:
        lines.append(f"- `monolith` rep{r['rep']}: {r['dims']}, core `final_sub` "
                     f"= {r['core']}, objective_pass = {r['objective_pass']} → **{r['pattern']}**")
    lines += ["",
              "The 0/4 and 0/3 figures reproduce exactly. **What does not reproduce is the "
              "reading**: the core did not hold. `final_sub` is 2/6 and `objective_pass` is "
              "False in every monolith rep. That is `both_drop` — global failure — not "
              "selective omission.", ""]

    lines += ["## Per-arm pattern counts", "",
              "| arm | rows | blur | both_drop | both_hold | inverse | mixed |",
              "|---|---|---|---|---|---|---|"]
    for arm in sorted(by_arm):
        c = collections.Counter(r["pattern"] for r in by_arm[arm])
        lines.append(f"| {arm} | {len(by_arm[arm])} | {c['blur']} | {c['both_drop']} "
                     f"| {c['both_hold']} | {c['inverse']} | {c['mixed']} |")

    lines += ["", "## Load proxies vs the core-minus-low gap", "",
              "Correlation of `gap` with each proxy, reported separately (never averaged "
              "into one index, which would hide disagreement).", "",
              "| proxy | n | correlation with gap |", "|---|---|---|"]
    proxy_res = {}
    usable = [r for r in b if r["gap"] is not None]
    for key, label in (("L1_requirement_count", "L1 requirement count"),
                       ("L3_ctx_budget", "L3 context budget")):
        xs = [r[key] for r in usable]
        ys = [r["gap"] for r in usable]
        c = corr(xs, ys)
        proxy_res[key] = c
        lines.append(f"| {label} | {len(xs)} | {'%.3f' % c if c is not None else 'no variance'} |")
    views = collections.Counter(r["L2_worker_view"] for r in usable)
    lines.append(f"| L2 worker view | {len(usable)} | not computable — all rows are `{list(views)[0]}` |"
                 if len(views) == 1 else
                 f"| L2 worker view | {len(usable)} | {dict(views)} |")

    lines += ["", "## Reading, against the rule fixed in the protocol", ""]
    blur_share = pats["blur"] / len(b)
    drop_share = pats["both_drop"] / len(b)
    lines += [f"- `blur` rows: **{pats['blur']} ({blur_share:.1%})**",
              f"- `both_drop` rows: **{pats['both_drop']} ({drop_share:.1%})**",
              f"- `inverse` rows: **{pats['inverse']}**", ""]

    lines += ["## Limitations, required by the protocol", "",
              f"1. Only **{len(tasks)} tasks** in the whole 34-task suite carry a low-salience "
              "dimension. Everything above describes those tasks, not the suite.",
              "2. **No controlled load axis exists.** L1 confounds 'more to do' with 'more to "
              "hold'; L3 confounds context budget with scaffold generation. This is "
              "observational.",
              "3. L2 (worker view) has no variance in these rows and is not computable.",
              "4. Arms differ in scaffold, not in load, so any correlation is between "
              "scaffold-associated quantities, not a dose-response."]
    (OUT / "blur_partB.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    json.dump({"schema": "e1-blur/1", "generated": now,
               "part_a": a, "part_b": b,
               "patterns": dict(pats), "tasks_with_low_salience_dims": tasks,
               "proxy_correlations": proxy_res},
              (OUT / "blur.json").open("w", encoding="utf-8"), indent=2)

    print("part A rows:", len(a), "| wf6 doc/todo:", [(r["doc"], r["todo"]) for r in wf6])
    print("part B rows:", len(b), "tasks:", tasks)
    print("patterns:", dict(pats))
    print("monolith wf6:", [(r["dims"], r["core"], r["pattern"]) for r in mono])
    print("proxy corr:", proxy_res)


if __name__ == "__main__":
    main()
