"""Full matrix: every arm, every model, reworked prompt (v2), n=1.

Ordered so the most informative cells land first, because this will not finish
in one night -- judge_anchored alone took ~90 minutes for 34 tasks on the 4B,
and the matrix is 3 models x ~16 arms. It is resumable: --store-resume skips
cells already in the store, so re-running continues rather than repeating.

SAMPLING. temperature 0.6 / top_p 0.95 for all three models. That is the
documented setting for both Nemotrons (tool calling on the 4B card, reasoning-ON
on the 9B's) and is applied to qwen too for comparability rather than because
qwen documents it -- recorded in params either way, so the choice is visible and
never pools with a different one.

PROTOCOL v2 throughout, so the matrix is internally consistent. The v1/v2
comparison is a separate pair of monolith sweeps.

    python queue_full_matrix.py [--dry] [--models a,b] [--arms x,y] [--waivers id,id]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGS = HERE / "matrix_logs"

MODELS = [
    "nemotron3-nano-4b:latest",
    "nemotron-gpu:latest",
    "qwen2.5-coder:7b-instruct-q4_K_M",
]

# Ordered by what each answers, not alphabetically. baseline first because it
# is the reference every other arm is read against and costs almost nothing;
# then the one-shot and judged arms that carry today's open questions; then the
# rest.
ARMS = [
    # The arms that actually carry the corpus, by row count in the store, plus
    # monolith_recovery which is new and deliberate.
    "baseline",           # 109 rows: the reference every arm is read against
    "monolith",           # 573
    "monolith_recovery",  # new, paired against monolith
    "judge_anchored",     # 1459
    "judge_caveat",       # 1402
    "judge_bypass",       # 1410
    "judge_fullctx",      # 238
    "dloop",              # 184
    "staged",             # 136
    "m7",                 # 184
    "test_synth",         # 238

    # ---- the missing judges, added 2026-09-27 ----
    # They were left out on row count: "barely exercised ... sweeping them
    # would spend the night on cells nothing reads". `50-findings/18` retires
    # that reasoning. It shows the judges divide by AGGREGATION SHAPE, not by
    # the lineage they were built in:
    #
    #   verdict = all(yes) over 2-5 conditions  judge_anchored/caveat/bypass
    #   one concern, one verdict, no conjunction  judge_fullctx + these four
    #
    # The first group fails by compounding 11% per-condition noise into 33%
    # verdict noise, at a rate set by how many conditions the auditor wrote.
    # The second cannot fail that way. Four of the five arms on the side that
    # survives the finding have never been swept, and each isolates one
    # variable: an independent judge at all (m7c), instruction vs critique
    # (m7e), orientation about what produced its inputs (m7f), and ordering
    # put in the reasoning rather than the output (judge_staged).
    #
    # Verified 2026-09-27: none of the four contains `checked`, `n_conditions`
    # or `expected`; all take (objective, concern, before, after).
    "judge_staged",       # 144
    "m7f",                # 204
    "m7e",                # 102
    "m7c",                # 32
]

# NOT queued yet, deliberately: monolith_test, author, author_judge. They came
# in with Queue A and have never executed. A 30-hour queue is the wrong place
# to discover that an arm raises on task 1 -- smoke-test each on a single task
# first, then add them.

ENV = {
    "LATTICE_PROTOCOL": "tools",
    "LATTICE_PROTOCOL_VARIANT": "v2",
    "LATTICE_TEMPERATURE": "0.6",
    "LATTICE_TOP_P": "0.95",
    "LATTICE_MIN_PREDICT": "8192",
    "LATTICE_NUM_CTX": "16384",
}


def main(argv: list[str]) -> None:
    dry = "--dry" in argv
    models = MODELS
    arms = ARMS
    if "--models" in argv:
        models = argv[argv.index("--models") + 1].split(",")
    if "--arms" in argv:
        arms = argv[argv.index("--arms") + 1].split(",")
    # Waiver families to admit when resuming, BY ID (evalkit/waivers.json).
    # Ids only; the hashes and their evidence stay in the file.
    waivers = []
    if "--waivers" in argv:
        waivers = ["--waivers", *argv[argv.index("--waivers") + 1].split(",")]
    LOGS.mkdir(exist_ok=True)
    avail = json.loads(
        subprocess.run([sys.executable, "-c",
                        "import sys;sys.path.insert(0,'.');"
                        "import run_suite;import json;print(json.dumps(sorted(run_suite.ARMS)))"],
                       cwd=str(HERE), capture_output=True, text=True).stdout or "[]")
    arms = [a for a in arms if a in avail] or arms
    jobs = [(m, a) for m in models for a in arms]
    print(f"{len(jobs)} jobs = {len(models)} models x {len(arms)} arms, n=1, v2")
    print(f"arms: {' '.join(arms)}")
    if dry:
        return
    t0 = time.monotonic()
    for i, (model, arm) in enumerate(jobs, 1):
        tag = f"{model.split(':')[0].replace('.', '')}_{arm}"
        log = LOGS / f"{tag}.log"
        if log.exists() and "objective pass" in log.read_text(encoding="utf-8", errors="replace"):
            print(f"[{i}/{len(jobs)}] {tag} already complete, skipping")
            continue
        env = {**os.environ, **ENV,
               "LATTICE_EVAL_MODEL": model,
               "LATTICE_RESULTS_SUBDIR": f"results_matrix_{model.split(':')[0].replace('.', '')}"}
        print(f"[{i}/{len(jobs)}] {tag} ...", flush=True)
        with open(log, "w", encoding="utf-8") as fh:
            subprocess.run([sys.executable, "-u", "run_suite.py", "--arm", arm,
                            "--reps", "1", "--store-resume", *waivers],
                           cwd=str(HERE), env=env, stdout=fh,
                           stderr=subprocess.STDOUT)
        print(f"        done, {(time.monotonic() - t0) / 60:.0f} min elapsed", flush=True)
    print(f"matrix finished in {(time.monotonic() - t0) / 60:.0f} min")


if __name__ == "__main__":
    main(sys.argv[1:])
