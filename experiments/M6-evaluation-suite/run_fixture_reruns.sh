#!/bin/bash
# Both fixture re-runs, sequentially. nemotron first (15 rows, fast) so E8's
# nemo cells unblock early; qwen second (134 rows).
set -u
cd "$(dirname "$0")"
echo "=== nothink (again: the first pass predated the suite_version field) ==="
python rerun_tasks.py --tree results_nemotron_nothink
echo
echo "=== qwen ==="
python rerun_tasks.py --tree results
echo
echo "ALL FIXTURE RERUNS DONE"
