"""The markdown report run_suite prints and writes beside each arm's JSON.

Its own module because `setup_key.arm_source_path()` hashes the WHOLE of
run_suite.py for baseline, monolith and monolith_recovery: any edit there, a
report column included, moves those arms' arm_sha and detaches them from every
row already collected. A report is not the experiment. Moved out 2026-09-27
(A8) so the next change to it moves nothing.

The help a run took -- recovery interventions and escalations, and how the
tool calls arrived (native, recovered from text, repaired JSON, malformed) --
is reported BESIDE the pass rate and never folded into it. "Passed, with two
interventions" is a different claim from "passed".
"""
from __future__ import annotations

import time
from collections import defaultdict

TOOL = ("tool_native", "tool_recovered", "tool_repaired", "tool_malformed")


def _help(r) -> tuple[int, bool]:
    rec = r.get("recovery") or {}
    return int(rec.get("interventions") or 0), bool(rec.get("escalated"))


def summarise(rows, arm, suite_version):
    L = [f"# M6 suite run - arm `{arm}` (suite {suite_version})", "",
         f"_{time.strftime('%Y-%m-%d %H:%M')} - {len(rows)} runs_", "",
         "| task | shape/trap | terminal | base | final | struct | pass | regr | decline "
         "| interv | tools n/rec/rep/mal | wall |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["task"], r["rep"])):
        st = " ".join(f"{k}={v[0]}/{v[1]}" for k, v in r["struct"].items()) or "-"
        dec = ("ok" if r["declined_correctly"] else "MISS") if r["decline_expected"] else "-"
        iv, esc = _help(r)
        tools = "/".join(str(r.get(k) or 0) for k in TOOL)
        L.append(f"| {r['task']} | {r['shape']}/{r['trap']} | {r['terminal']} | "
                 f"{r['baseline_sub'][0]}/{r['baseline_sub'][1]} | "
                 f"{r['final_sub'][0]}/{r['final_sub'][1]} | {st} | {r['objective_pass']} | "
                 f"{'YES' if r['regressed'] else '-'} | {dec} | "
                 f"{iv}{' ESC' if esc else ''} | {tools} | {r['wall_s']} |")

    # aggregate. Rows whose arm raised produced no attempt, so they are counted
    # separately and excluded from every rate -- a denominator that includes them
    # reports the fixture, not the model.
    ok_rows = [r for r in rows if r.get("run_ok", True)]
    nfail = len(rows) - len(ok_rows)
    npass = sum(r["objective_pass"] for r in ok_rows)
    nreg = sum(r["regressed"] for r in ok_rows)
    ncrash = sum(r["check_crashed"] for r in ok_rows)
    dec_rows = [r for r in ok_rows if r["decline_expected"]]
    dec_ok = sum(r["declined_correctly"] for r in dec_rows)
    L += ["", f"**objective pass {npass}/{len(ok_rows)} - regressions {nreg} - "
              f"check crashes {ncrash} - decline accuracy {dec_ok}/{len(dec_rows)}**", ""]
    # Beside the score, never folded into it. Same rows as the pass rate.
    helped = [_help(r) for r in ok_rows]
    n_iv = sum(iv for iv, _ in helped)
    n_iv_rows = sum(1 for iv, _ in helped if iv)
    n_esc = sum(1 for _, esc in helped if esc)
    tsum = {k: sum(int(r.get(k) or 0) for r in ok_rows) for k in TOOL}
    L += [f"help taken, over the same {len(ok_rows)} runs: interventions {n_iv} "
          f"(in {n_iv_rows} run(s)) - escalations {n_esc} - tool calls native "
          f"{tsum['tool_native']} / recovered {tsum['tool_recovered']} / repaired "
          f"{tsum['tool_repaired']} / malformed {tsum['tool_malformed']}", ""]
    if nfail:
        L += [f"> **{nfail} of {len(rows)} runs did not execute** (the arm raised; "
              f"`run_ok: false`). They are excluded from every figure above. See "
              f"`error_trace` in the JSON.", ""]

    # stresses slices - mean final subtest fraction per capability tag.
    # ok_rows, not rows: a run that never executed scores the untouched fixture,
    # which would drag every tag it carries toward the baseline.
    by_tag = defaultdict(list)
    for r in ok_rows:
        f = r["final_sub"][0] / max(1, r["final_sub"][1])
        for tag in r["stresses"]:
            by_tag[tag].append(f)
    L += ["## `stresses` slices (mean final SUBTESTS fraction)", "",
          "| capability | n | mean |", "|---|---|---|"]
    for tag, xs in sorted(by_tag.items()):
        L.append(f"| {tag} | {len(xs)} | {sum(xs)/len(xs):.2f} |")
    return "\n".join(L) + "\n"
