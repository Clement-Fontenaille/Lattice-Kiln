#!/usr/bin/env bash
# M0 - fidelity spot-check via llama.cpp (WSL). Only the models in models.json
# with "llamacpp_spotcheck": true. Cross-checks Ollama's numbers and exposes the
# GPU/CPU offload split Ollama hides.
#
# Requires (inside WSL): a prebuilt CUDA llama.cpp on PATH (llama-cli, llama-bench),
# jq, and GGUF files under $MODELS_DIR.
#
# Untested until the runtime is installed.
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODELS_JSON="${MODELS_JSON:-$HERE/models.json}"
MODELS_DIR="${MODELS_DIR:-$HERE/../models}"
RUNS_DIR="${RUNS_DIR:-$HERE/../results/runs}"
FILLS="${FILLS:-512 4096 16384}"
GEN_N="${GEN_N:-256}"
REPS="${REPS:-5}"

mkdir -p "$RUNS_DIR"

for bin in llama-cli jq; do
  command -v "$bin" >/dev/null 2>&1 || { echo "missing: $bin" >&2; exit 1; }
done

HOST_JSON="$HERE/../results/host.json"
HOST_REF="null"
[ -f "$HOST_JSON" ] && HOST_REF="\"$(sha256sum "$HOST_JSON" | cut -d' ' -f1)\""
LLAMA_VERSION="$(llama-cli --version 2>&1 | head -n1 | tr -d '"')"

# find a gguf for a slot+quant by loose globbing
find_gguf() {
  local params_b="$1" quant="$2"
  local q_lc; q_lc="$(echo "$quant" | tr 'A-Z' 'a-z')"
  shopt -s nullglob nocaseglob
  local hits=("$MODELS_DIR"/*"${params_b}b"*"${q_lc}"*.gguf "$MODELS_DIR"/*"${params_b}b"*"${quant}"*.gguf)
  shopt -u nullglob nocaseglob
  [ ${#hits[@]} -gt 0 ] && printf '%s\n' "${hits[0]}"
}

# parse llama.cpp perf lines from a completed run's stderr capture
emit_record() {
  local model="$1" quant="$2" fill="$3" ngl="$4" rep="$5" logfile="$6" status="$7" note="$8"
  local load_ms pe_ms pe_tok pe_ts ev_ms ev_tok ev_ts gpul totall vram
  load_ms=$(grep -oP 'load time =\s*\K[0-9.]+' "$logfile" | tail -n1)
  pe_ms=$(grep -oP 'prompt eval time =\s*\K[0-9.]+' "$logfile" | tail -n1)
  pe_tok=$(grep -oP 'prompt eval time =.*?/\s*\K[0-9]+' "$logfile" | tail -n1)
  ev_ms=$(grep -oP '[^p] eval time =\s*\K[0-9.]+' "$logfile" | tail -n1)
  ev_tok=$(grep -oP '[^p] eval time =.*?/\s*\K[0-9]+' "$logfile" | tail -n1)
  gpul=$(grep -oP 'offloaded\s*\K[0-9]+(?=/[0-9]+ layers)' "$logfile" | tail -n1)
  totall=$(grep -oP 'offloaded\s*[0-9]+/\K[0-9]+(?= layers)' "$logfile" | tail -n1)
  vram=$(grep -oP 'CUDA0.*?buffer size =\s*\K[0-9.]+' "$logfile" | awk '{s+=$1} END{if(s)printf "%.0f", s}')
  pe_ts=$(awk -v ms="${pe_ms:-0}" -v n="${pe_tok:-0}" 'BEGIN{ if(ms>0) printf "%.2f", n/(ms/1000); else print "null" }')
  ev_ts=$(awk -v ms="${ev_ms:-0}" -v n="${ev_tok:-0}" 'BEGIN{ if(ms>0) printf "%.2f", n/(ms/1000); else print "null" }')

  local out="$RUNS_DIR/llama.cpp__${model}-${params_b}b__${quant}__${fill}__ngl${ngl}__${rep}.json"
  jq -n \
    --arg ver "$LLAMA_VERSION" --arg model "$model" --arg quant "$quant" \
    --argjson fill "$fill" --argjson ngl "$ngl" --argjson rep "$rep" \
    --arg status "$status" --arg note "$note" --arg ts "$(date -Iseconds)" \
    --argjson hostref "$HOST_REF" \
    --argjson load "${load_ms:-null}" --argjson pems "${pe_ms:-null}" --argjson petok "${pe_tok:-null}" \
    --argjson pets "${pe_ts:-null}" --argjson evms "${ev_ms:-null}" --argjson evtok "${ev_tok:-null}" \
    --argjson evts "${ev_ts:-null}" --argjson gpul "${gpul:-null}" --argjson totall "${totall:-null}" \
    --argjson vram "${vram:-null}" \
    '{schema:"m0-run/1", runtime:"llama.cpp", runtime_version:$ver, model:$model, quant:$quant,
      context_fill:$fill, num_ctx:$fill, ngl:$ngl, repetition:$rep, is_cold:($rep==0), warmup:($rep==0),
      timestamp:$ts, host_ref:$hostref,
      metrics:{load_ms:$load, prompt_eval_ms:$pems, prompt_eval_count:$petok, prefill_tok_s:$pets,
               eval_ms:$evms, eval_count:$evtok, gen_tok_s:$evts,
               gpu_layers:$gpul, total_layers:$totall, vram_resident_mb:$vram},
      status:$status, note:$note}' > "$out"
  echo "   wrote $(basename "$out")  prefill=${pe_ts} tok/s  gen=${ev_ts} tok/s  ngl=${gpul:-?}/${totall:-?}"
}

run_cell() {
  local model="$1" params_b="$2" quant="$3" fill="$4" ngl="$5" rep="$6" gguf="$7"
  local log; log="$(mktemp)"
  local prompt; prompt="$(head -c $((fill * 4)) < <(yes "the system distributes reasoning across short lived invocations " ) | tr -d '\n')"
  # -no-cnv: recent llama-cli defaults to interactive conversation mode and would
  # hang waiting on stdin. Force one-shot completion.
  if llama-cli -m "$gguf" -ngl "$ngl" -c "$fill" -n "$GEN_N" -no-cnv --no-display-prompt \
       -p "$prompt" > "$log" 2>&1; then
    emit_record "$model" "$quant" "$fill" "$ngl" "$rep" "$log" "ok" ""
  else
    local msg; msg="$(tail -n3 "$log" | tr '\n' ' ' | tr -d '"')"
    local st="error"; echo "$msg" | grep -qiE 'out of memory|cudaMalloc|OOM' && st="oom"
    emit_record "$model" "$quant" "$fill" "$ngl" "$rep" "$log" "$st" "$msg"
    echo "   $model $quant fill=$fill ngl=$ngl -> $st"
    [ "$st" = "oom" ] && rm -f "$log" && return 1
  fi
  rm -f "$log"
}

n_models="$(jq '.models | length' "$MODELS_JSON")"
for i in $(seq 0 $((n_models - 1))); do
  spot="$(jq -r ".models[$i].llamacpp_spotcheck // false" "$MODELS_JSON")"
  [ "$spot" = "true" ] || continue
  family="$(jq -r ".models[$i].family" "$MODELS_JSON")"
  params_b="$(jq -r ".models[$i].params_b" "$MODELS_JSON")"
  mapfile -t quants < <(jq -r ".models[$i].llamacpp_quants[]" "$MODELS_JSON")
  mapfile -t ngls   < <(jq -r ".models[$i].llamacpp_ngl_sweep[]? // 99" "$MODELS_JSON")
  [ ${#ngls[@]} -eq 0 ] && ngls=(99)

  for quant in "${quants[@]}"; do
    gguf="$(find_gguf "$params_b" "$quant")"
    if [ -z "$gguf" ]; then
      echo "!! no GGUF for ${family}-${params_b}b ${quant} under $MODELS_DIR - skipping" >&2
      continue
    fi
    echo "== ${family}-${params_b}b ${quant}  ($(basename "$gguf"))"
    for ngl in "${ngls[@]}"; do
      for fill in $FILLS; do
        for rep in $(seq 0 "$REPS"); do
          run_cell "$family" "$params_b" "$quant" "$fill" "$ngl" "$rep" "$gguf" || break 2
        done
      done
    done
  done
done

echo ""
echo "Done. Records in: $RUNS_DIR"
echo "Next (Windows): pwsh harness/aggregate.ps1"
