#!/usr/bin/env bash
# M0 - fidelity spot-check via llama.cpp (WSL), using llama-bench -o json.
#
# The current llama.cpp tree replaced the standalone llama-cli with a unified
# 'llama' launcher that needs sub-impl libs a lean build does not produce.
# llama-bench builds cleanly and reports exactly what the spot-check needs:
# prefill (pp) and generation (tg) tokens/s with repetitions, plus n_gpu_layers.
# The GPU/CPU offload split - the main thing Ollama hides - comes from the
# n_gpu_layers field and the 'offloaded N/M layers' load line.
#
# Requires, inside WSL:
#   - ~/.local/bin/llama-bench (built by .wsl-scratch/build-llamacpp.sh) and its
#     shared libs on LD_LIBRARY_PATH (~/.local/lib)
#   - jq
#   - GGUF files under $MODELS_DIR (default ~/m0-models)
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODELS_JSON="${MODELS_JSON:-$HERE/models.json}"
MODELS_DIR="${MODELS_DIR:-$HOME/m0-models}"
RUNS_DIR="${RUNS_DIR:-$HERE/../results/runs}"
FILLS="${FILLS:-512 4096 16384 32768}"
GEN_N="${GEN_N:-256}"
REPS="${REPS:-5}"
LLAMA_BENCH="${LLAMA_BENCH:-$HOME/.local/bin/llama-bench}"
export LD_LIBRARY_PATH="$HOME/.local/lib:${LD_LIBRARY_PATH:-}"

mkdir -p "$RUNS_DIR"
command -v jq >/dev/null 2>&1 || { echo "missing: jq" >&2; exit 1; }
[ -x "$LLAMA_BENCH" ] || { echo "missing: $LLAMA_BENCH (run .wsl-scratch/build-llamacpp.sh)" >&2; exit 1; }

HOST_JSON="$HERE/../results/host.json"
HOST_REF="null"
[ -f "$HOST_JSON" ] && HOST_REF="\"$(sha256sum "$HOST_JSON" | cut -d' ' -f1)\""

FILLS_CSV="$(echo "$FILLS" | tr ' ' ',')"

find_gguf() {
  local params_b="$1" quant="$2" q_lc
  q_lc="$(echo "$quant" | tr 'A-Z' 'a-z')"
  shopt -s nullglob nocaseglob
  local hits=("$MODELS_DIR"/*"${params_b}b"*"${q_lc}"*.gguf)
  shopt -u nullglob nocaseglob
  [ ${#hits[@]} -gt 0 ] && printf '%s\n' "${hits[0]}"
}

# nvidia-smi peak sampler: writes max MiB used to $1 until $2 (a pid) exits.
sample_vram() {
  local outfile="$1" watch_pid="$2" max=0 cur
  while kill -0 "$watch_pid" 2>/dev/null; do
    cur="$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -n1 | tr -d ' ')"
    [ -n "$cur" ] && [ "$cur" -gt "$max" ] 2>/dev/null && max="$cur"
    sleep 0.5
  done
  echo "$max" > "$outfile"
}

emit() {
  # emit <model> <params_b> <quant> <fill> <ngl> <kind pp|tg> <avg_ts> <n_gpu_layers> <total_layers> <vram_mb> <build> <status> <note>
  local model="$1" pb="$2" quant="$3" fill="$4" ngl="$5" kind="$6" ts="$7" gpul="$8" totl="$9" vram="${10}" build="${11}" status="${12}" note="${13}"
  local pref="null" genf="null"
  [ "$kind" = "pp" ] && pref="$ts"
  [ "$kind" = "tg" ] && genf="$ts"
  local out="$RUNS_DIR/llama.cpp__${model}-${pb}b__${quant}__${fill}__ngl${ngl}__${kind}.json"
  jq -n \
    --arg model "$model" --arg quant "$quant" --arg build "$build" \
    --arg status "$status" --arg note "$note" --arg ts_iso "$(date -Iseconds)" \
    --argjson pb "$pb" --argjson fill "$fill" --argjson ngl "$ngl" \
    --argjson hostref "$HOST_REF" \
    --argjson pref "${pref:-null}" --argjson genf "${genf:-null}" \
    --argjson gpul "${gpul:-null}" --argjson totl "${totl:-null}" --argjson vram "${vram:-null}" \
    '{schema:"m0-run/1", runtime:"llama.cpp", runtime_version:("llama.cpp " + $build),
      model:$model, quant:$quant, context_fill:$fill, num_ctx:$fill, ngl:$ngl,
      is_cold:false, warmup:false, timestamp:$ts_iso, host_ref:$hostref,
      metrics:{prefill_tok_s:$pref, gen_tok_s:$genf,
               gpu_layers:$gpul, total_layers:$totl, vram_resident_mb:$vram},
      status:$status, note:$note}' > "$out"
  echo "   $(basename "$out")  ${kind}=${ts} tok/s  ngl=${gpul:-?}/${totl:-?}  vram=${vram:-?}MB  [$status]"
}

run_group() {
  # run_group <model> <params_b> <quant> <gguf> <ngl> <mode pp|tg>
  local model="$1" pb="$2" quant="$3" gguf="$4" ngl="$5" mode="$6"
  local log jout vf smpid rc
  log="$(mktemp)"; jout="$(mktemp)"; vf="$(mktemp)"

  local args=(-m "$gguf" -ngl "$ngl" -r "$REPS" -fa auto -o json)
  if [ "$mode" = "pp" ]; then
    args+=(-p "$FILLS_CSV" -n 0)
  else
    args+=(-p 0 -n "$GEN_N" -d "$FILLS_CSV")
  fi

  "$LLAMA_BENCH" "${args[@]}" >"$jout" 2>"$log" &
  local bpid=$!
  sample_vram "$vf" "$bpid" &
  smpid=$!
  wait "$bpid"; rc=$?
  wait "$smpid" 2>/dev/null || true
  local vram; vram="$(cat "$vf" 2>/dev/null)"; vram="${vram:-null}"

  local build totl gpul
  build="$(jq -r '.[0].build_commit // "unknown"' "$jout" 2>/dev/null)"
  [ "$build" = "unknown" ] || [ -z "$build" ] && build="$(grep -oP 'build:\s*\K[0-9a-f]+' "$log" | head -n1)"
  build="${build:-unknown}"
  totl="$(grep -oP 'offloaded\s+[0-9]+/\K[0-9]+' "$log" | tail -n1)"; totl="${totl:-null}"

  local oom="no"
  grep -qiE 'out of memory|cudaMalloc|failed to allocate|CUDA error' "$log" && oom="yes"

  if [ "$rc" -ne 0 ] && ! jq -e '.[0]' "$jout" >/dev/null 2>&1; then
    # whole invocation failed - emit one record per fill
    local st="error"; [ "$oom" = "yes" ] && st="oom"
    local msg; msg="$(tail -n2 "$log" | tr '\n' ' ' | tr -d '"' | cut -c1-160)"
    for f in $FILLS; do
      emit "$model" "$pb" "$quant" "$f" "$ngl" "$mode" "null" "null" "$totl" "null" "$build" "$st" "$msg"
    done
    rm -f "$log" "$jout" "$vf"; return
  fi

  # one JSON row per fill
  for f in $FILLS; do
    local row ts gl
    if [ "$mode" = "pp" ]; then
      row="$(jq -c --argjson f "$f" '.[] | select(.n_prompt==$f and (.n_gen==0))' "$jout" 2>/dev/null | head -n1)"
    else
      row="$(jq -c --argjson f "$f" '.[] | select(.n_gen>0 and ((.n_depth // 0)==$f))' "$jout" 2>/dev/null | head -n1)"
    fi
    if [ -z "$row" ]; then
      local st="error"; [ "$oom" = "yes" ] && st="oom"
      emit "$model" "$pb" "$quant" "$f" "$ngl" "$mode" "null" "null" "$totl" "$vram" "$build" "$st" "no json row for fill=$f"
      continue
    fi
    ts="$(echo "$row" | jq -r '.avg_ts')"
    gl="$(echo "$row" | jq -r '.n_gpu_layers')"
    emit "$model" "$pb" "$quant" "$f" "$ngl" "$mode" "$ts" "$gl" "$totl" "$vram" "$build" "ok" ""
  done
  rm -f "$log" "$jout" "$vf"
}

n_models="$(jq '.models | length' "$MODELS_JSON")"
for i in $(seq 0 $((n_models - 1))); do
  [ "$(jq -r ".models[$i].llamacpp_spotcheck // false" "$MODELS_JSON")" = "true" ] || continue
  family="$(jq -r ".models[$i].family" "$MODELS_JSON")"
  pb="$(jq -r ".models[$i].params_b" "$MODELS_JSON")"
  mapfile -t quants < <(jq -r ".models[$i].llamacpp_quants[]" "$MODELS_JSON")
  mapfile -t ngls   < <(jq -r ".models[$i].llamacpp_ngl_sweep[]? // empty" "$MODELS_JSON")
  [ ${#ngls[@]} -eq 0 ] && ngls=(99)

  for quant in "${quants[@]}"; do
    gguf="$(find_gguf "$pb" "$quant")"
    if [ -z "$gguf" ]; then
      echo "!! no GGUF for ${family}-${pb}b ${quant} under $MODELS_DIR - skipping" >&2
      continue
    fi
    echo "== ${family}-${pb}b ${quant}  ($(basename "$gguf"))"
    for ngl in "${ngls[@]}"; do
      echo " -- ngl=$ngl"
      run_group "$family" "$pb" "$quant" "$gguf" "$ngl" pp
      run_group "$family" "$pb" "$quant" "$gguf" "$ngl" tg
    done
  done
done

echo ""
echo "Done. Records in: $RUNS_DIR"
echo "Next (Windows): pwsh harness/aggregate.ps1"
