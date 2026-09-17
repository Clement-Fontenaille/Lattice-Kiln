"""E2 — forecast test: does qwen<->Nemotron divergence cluster where the
pre-registered granularity ranking said it would?

Implements experiments/E2-grain-versus-quantity/PROTOCOL.md steps 4-5.
Must only be run AFTER preregistration/ranking-*.json is committed.
"""
from __future__ import annotations

import json
import collections
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT / "experiments/M6-evaluation-suite"
QWEN = SUITE / "results"
NEMO = SUITE / "results_nemotron_llamacpp"
HERE = Path(__file__).resolve().parent
OUT = HERE / "results"

# baseline makes no model call, so it cannot diverge by model. It is kept only
# as a harness sanity check: the two models must agree on every baseline task.
DEGENERATE = {"baseline"}


def as_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        if v == "True":
            return True
        if v == "False":
            return False
    raise ValueError(f"not a boolean: {v!r}")


def load(path):
    by_task = collections.defaultdict(list)
    for r in json.loads(path.read_text(encoding="utf-8")):
        by_task[r["task"]].append(as_bool(r["objective_pass"]))
    return by_task


def collapse(reps):
    """Strict majority, fixed in the protocol before any comparison.
    Returns True, False, or None for an exact split (excluded)."""
    if not reps:
        return None
    p, n = sum(reps), len(reps)
    if p * 2 > n:
        return True
    if p * 2 < n:
        return False
    return None


def main():
    prereg_path = sorted(HERE.glob("preregistration/ranking-*.json"))[-1]
    prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
    band = {e["task"]: e["band"] for e in prereg["ranking"]}
    count = {e["task"]: e["count"] for e in prereg["ranking"]}
    band_sizes = collections.Counter(band.values())

    nemo_arms = sorted(p.stem for p in NEMO.glob("*.json"))
    usable = [a for a in nemo_arms if a not in DEGENERATE and (QWEN / f"{a}.json").exists()]

    # harness sanity check on the degenerate arm
    sanity = {}
    for arm in (set(nemo_arms) & DEGENERATE):
        q, n = load(QWEN / f"{arm}.json"), load(NEMO / f"{arm}.json")
        mismatches = [t for t in set(q) & set(n) if collapse(q[t]) != collapse(n[t])]
        sanity[arm] = {"tasks_compared": len(set(q) & set(n)), "mismatches": mismatches}

    rows, excluded = [], []
    for arm in usable:
        q, n = load(QWEN / f"{arm}.json"), load(NEMO / f"{arm}.json")
        for task in sorted(set(q) & set(n)):
            qv, nv = collapse(q[task]), collapse(n[task])
            if qv is None:
                excluded.append({"arm": arm, "task": task, "reason": "qwen_unstable",
                                 "qwen_reps": q[task]})
                continue
            if nv is None:
                excluded.append({"arm": arm, "task": task, "reason": "nemotron_unstable",
                                 "nemotron_reps": n[task]})
                continue
            rows.append({"arm": arm, "task": task, "band": band.get(task),
                         "count": count.get(task), "qwen": qv, "nemotron": nv,
                         "divergent": qv != nv,
                         "direction": ("nemotron_only" if nv and not qv else
                                       "qwen_only" if qv and not nv else None)})

    div = [r for r in rows if r["divergent"]]
    by_band_total = collections.Counter(r["band"] for r in rows)
    by_band_div = collections.Counter(r["band"] for r in div)

    now = datetime.now(timezone.utc).isoformat()
    lines = ["# E2 — forecast test result", "", f"Generated {now}.", "",
             f"Pre-registration: `{prereg_path.relative_to(ROOT)}` "
             f"(proxy {prereg['proxy']}, committed before any Nemotron result was read).", "",
             "## Sweep coverage — the sweep did not finish", "",
             f"- Nemotron arms present: **{', '.join(nemo_arms) or 'none'}**",
             f"- of which usable (non-degenerate, matched in qwen): **{', '.join(usable) or 'none'}**",
             "",
             "`baseline` makes no model call and cannot diverge by model; it is used only",
             "as a harness sanity check.", ""]
    for arm, s in sanity.items():
        ok = not s["mismatches"]
        lines.append(f"- sanity `{arm}`: {s['tasks_compared']} tasks compared, "
                     f"mismatches: **{'none — harness consistent' if ok else s['mismatches']}**")

    lines += ["", "## Divergence by pre-registered band", "",
              f"Band sizes in the pre-registration: "
              f"{', '.join(f'{k} {v}' for k, v in sorted(band_sizes.items()))}.", "",
              "| band | tasks compared | divergent | rate |", "|---|---|---|---|"]
    for b in ("high", "mid", "low"):
        tot, d = by_band_total.get(b, 0), by_band_div.get(b, 0)
        lines.append(f"| {b} | {tot} | {d} | {(d/tot):.1%} |" if tot else f"| {b} | 0 | 0 | — |")
    lines += [f"| **total** | **{len(rows)}** | **{len(div)}** | "
              f"**{(len(div)/len(rows)):.1%}** |" if rows else "| total | 0 | 0 | — |"]

    if div:
        lines += ["", "## The divergent tasks", "",
                  "| arm | task | band | P1 count | qwen | nemotron | direction |",
                  "|---|---|---|---|---|---|---|"]
        for r in sorted(div, key=lambda r: (-(r["count"] or 0), r["task"])):
            lines.append(f"| {r['arm']} | {r['task']} | {r['band']} | {r['count']} | "
                         f"{'pass' if r['qwen'] else 'fail'} | "
                         f"{'pass' if r['nemotron'] else 'fail'} | {r['direction']} |")

    if excluded:
        lines += ["", "## Excluded cells", "", "| arm | task | reason |", "|---|---|---|"]
        for e in excluded:
            lines.append(f"| {e['arm']} | {e['task']} | {e['reason']} |")

    # ---- confound audit: tasks that CANNOT show divergence on objective_pass
    tasks_meta = {t["id"]: t for t in
                  json.loads((SUITE / "tasks.json").read_text(encoding="utf-8"))["tasks"]}
    # E0 part 1, 2026-09-17: untouched source passes while work is demanded.
    NO_WITNESS = {"wf3_refactor", "hf_extract_fn", "hf_dict_dispatch"}
    audit = []
    for r in rows:
        fp = bool(tasks_meta[r["task"]]["expect"].get("decline_correct", False))
        nw = r["task"] in NO_WITNESS
        audit.append({**r, "false_premise": fp, "no_witness": nw,
                      "blind": fp or nw})
    clean = [r for r in audit if not r["blind"]]
    cb_tot = collections.Counter(r["band"] for r in clean)
    cb_div = collections.Counter(r["band"] for r in clean if r["divergent"])
    blind_by_band = collections.Counter(r["band"] for r in audit if r["blind"])

    lines += ["", "## Confound audit — tasks that cannot show divergence", "",
              "Two classes of task pass regardless of what the model did, so they cannot",
              "diverge on `objective_pass` no matter how the models differ:", "",
              "- **false premise** (`expect.decline_correct`): doing nothing is the answer.",
              "- **no witness** (E0 part 1, 2026-09-17): the untouched source passes while",
              "  work is demanded — `wf3_refactor`, `hf_extract_fn`, `hf_dict_dispatch`.", "",
              "| band | tasks | of which blind | divergence rate, all | divergence rate, sighted only |",
              "|---|---|---|---|---|"]
    for b in ("high", "mid", "low"):
        tot, d = by_band_total.get(b, 0), by_band_div.get(b, 0)
        ct, cd = cb_tot.get(b, 0), cb_div.get(b, 0)
        lines.append(f"| {b} | {tot} | {blind_by_band.get(b, 0)} | "
                     f"{(d/tot):.1%} | {(cd/ct):.1%} |" if tot and ct
                     else f"| {b} | {tot} | {blind_by_band.get(b, 0)} | — | — |")

    lines += ["", "## Reading", "",
              f"- prediction: **{prereg['prediction']}**",
              f"- falsifier: **{prereg['falsifier']}**",
              f"- stated power limit: {prereg['power_statement']}", ""]
    (OUT).mkdir(exist_ok=True)
    (OUT / "divergence.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    json.dump({"schema": "e2-divergence/1", "generated": now,
               "preregistration": str(prereg_path.relative_to(ROOT)),
               "nemotron_arms_present": nemo_arms, "usable_arms": usable,
               "sanity": sanity, "rows": rows, "excluded": excluded,
               "by_band_total": dict(by_band_total), "by_band_divergent": dict(by_band_div),
               "confound_audit": audit, "sighted_by_band_total": dict(cb_tot),
               "sighted_by_band_divergent": dict(cb_div)},
              (OUT / "divergence.json").open("w", encoding="utf-8"), indent=2)

    print("nemotron arms:", nemo_arms, "| usable:", usable)
    print("sanity:", sanity)
    print("rows:", len(rows), "divergent:", len(div))
    print("by band total:", dict(by_band_total), "divergent:", dict(by_band_div))
    print("excluded:", len(excluded))


if __name__ == "__main__":
    main()
