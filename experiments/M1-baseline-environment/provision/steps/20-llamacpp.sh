#!/usr/bin/env bash
# M1 step 20 - llama.cpp CUDA (WSL) + GGUF assets.
# Thin wrapper over the M0 setup scripts so there is one source of truth.
# VERIFY_ONLY=1 -> check the installed binary and GGUF digests, build nothing.
set -u

VERIFY_ONLY="${VERIFY_ONLY:-0}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
M0_SETUP="$HERE/../../../M0-inference-envelope/setup"
M0_HARNESS="$HERE/../../../M0-inference-envelope/harness"
MODELS_DIR="${MODELS_DIR:-$HOME/m0-models}"
export LD_LIBRARY_PATH="$HOME/.local/lib:${LD_LIBRARY_PATH:-}"
fail=0

# --- binary ---
if [ -x "$HOME/.local/bin/llama-bench" ]; then
  ver="$("$HOME/.local/bin/llama-bench" --help 2>&1 | grep -m1 -oE 'build: [0-9a-f]+' || true)"
  echo "PASS llama-bench installed (${ver:-version n/a})"
else
  if [ "$VERIFY_ONLY" = "1" ]; then
    echo "FAIL llama-bench not installed. run: bash $M0_SETUP/build-llamacpp-wsl.sh  (needs step 10 first)"
    fail=1
  else
    echo "DID  bash $M0_SETUP/build-llamacpp-wsl.sh"
    if ! bash "$M0_SETUP/build-llamacpp-wsl.sh"; then
      echo "FAIL llama.cpp build failed - see ~/m0-llamacpp-build.log"
      fail=1
    fi
  fi
fi

# --- CUDA actually initialises ---
if [ -x "$HOME/.local/bin/llama-bench" ]; then
  if "$HOME/.local/bin/llama-bench" --help 2>&1 | grep -q 'CUDA devices'; then
    echo "PASS llama-bench sees CUDA devices"
  else
    echo "WARN llama-bench ran but reported no CUDA devices"
  fi
fi

# --- GGUF assets + digests (pinned in models.json) ---
if [ ! -d "$MODELS_DIR" ] || [ -z "$(ls -A "$MODELS_DIR"/*.gguf 2>/dev/null)" ]; then
  if [ "$VERIFY_ONLY" = "1" ]; then
    echo "FAIL no GGUFs in $MODELS_DIR. run: bash $M0_SETUP/fetch-ggufs-wsl.sh"
    fail=1
  else
    echo "DID  bash $M0_SETUP/fetch-ggufs-wsl.sh"
    bash "$M0_SETUP/fetch-ggufs-wsl.sh" || { echo "FAIL GGUF fetch failed"; fail=1; }
  fi
fi

if command -v jq >/dev/null 2>&1 && [ -f "$M0_HARNESS/models.json" ]; then
  # verify each pinned gguf_sha256 against the file on disk
  while read -r fname want; do
    fpath="$MODELS_DIR/$fname"
    if [ ! -f "$fpath" ]; then echo "WARN pinned GGUF missing: $fname"; continue; fi
    got="$(sha256sum "$fpath" | cut -d' ' -f1)"
    if [ "$got" = "$want" ]; then echo "PASS digest ok: $fname"
    else echo "FAIL digest mismatch: $fname (got $got want $want)"; fail=1; fi
  done < <(jq -r '.models[] | select(.gguf_file) | "\(.gguf_file) \(.gguf_sha256)"' "$M0_HARNESS/models.json")
fi

exit "$fail"
