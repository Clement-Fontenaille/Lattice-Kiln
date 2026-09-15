#!/bin/bash
# N=1 sweep for Nemotron Nano 9B v2 (Q4_K_L) via llama-server (2x16k slots
# preferred setup, per M0 findings entry 1's addendum). Isolated from qwen
# and from the earlier abandoned Ollama-backend Nemotron attempt via
# LATTICE_BACKEND + LATTICE_RESULTS_SUBDIR.
set -e
cd "$(dirname "$0")"
export LATTICE_BACKEND="llamacpp"
export LATTICE_EVAL_MODEL="nemotron"
export LATTICE_BASE_URL="http://localhost:8090"
export LATTICE_RESULTS_SUBDIR="results_nemotron_llamacpp"
ARMS="baseline test_synth judge_anchored m7f judge_fullctx test_synth_retry m7b m7 dloop judge_bypass judge_staged m7e judge_caveat monolith staged"
LOG="queue_nemotron_llamacpp_main.log"
for arm in $ARMS; do
  echo "$(date +%H:%M:%S)  [$arm] starting reps=1" >> "$LOG"
  python run_suite.py --arm "$arm" --reps 1 --resume >> "queue_nemotron_llamacpp_${arm}.log" 2>&1
  rc=$?
  echo "$(date +%H:%M:%S)  [$arm] exit $rc" >> "$LOG"
done
echo "$(date +%H:%M:%S)  NEMOTRON LLAMACPP N=1 SWEEP DONE" >> "$LOG"
