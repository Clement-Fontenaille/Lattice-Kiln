#!/usr/bin/env bash
# Download the 3 GGUFs for the llama.cpp M0 spot-check. Public HF repos, no auth.
set -u
DEST="$HOME/m0-models"
mkdir -p "$DEST"
cd "$DEST" || exit 1

BASE7="https://huggingface.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF/resolve/main"
BASE14="https://huggingface.co/bartowski/Qwen2.5-Coder-14B-Instruct-GGUF/resolve/main"

FILES=(
  "$BASE7/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf"
  "$BASE14/Qwen2.5-Coder-14B-Instruct-Q4_K_M.gguf"
)

for url in "${FILES[@]}"; do
  fn="$(basename "$url")"
  if [ -s "$DEST/$fn" ]; then
    echo "have $fn ($(du -h "$DEST/$fn" | cut -f1))"
    continue
  fi
  echo "=== downloading $fn"
  wget -q --show-progress -c -O "$DEST/$fn" "$url" || { echo "FAILED: $fn"; exit 1; }
done

echo "=== done. contents: ==="
ls -lh "$DEST"
echo "=== sha256 ==="
sha256sum "$DEST"/*.gguf
