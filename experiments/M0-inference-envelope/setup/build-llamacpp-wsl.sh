#!/usr/bin/env bash
# Build llama.cpp with CUDA on WSL Ubuntu 24.04 using the apt nvidia-cuda-toolkit
# (nvcc 12.0). cmake/ninja come from pip --user. Target: RTX 2070 SUPER (sm_75).
set -euo pipefail

export PATH="$HOME/.local/bin:/usr/local/cuda/bin:$PATH"
SRC="$HOME/llama.cpp"
BUILD="$SRC/build"
LOG="$HOME/m0-llamacpp-build.log"
: > "$LOG"

echo "### tools" | tee -a "$LOG"
cmake --version | head -1 | tee -a "$LOG"
ninja --version | tee -a "$LOG"
nvcc --version | tail -2 | tee -a "$LOG"
nvidia-smi -L 2>&1 | head -1 | tee -a "$LOG"

echo "### clone / update llama.cpp" | tee -a "$LOG"
if [ ! -d "$SRC/.git" ]; then
  git clone --depth 1 https://github.com/ggml-org/llama.cpp "$SRC" 2>&1 | tail -3 | tee -a "$LOG"
else
  git -C "$SRC" pull --ff-only 2>&1 | tail -3 | tee -a "$LOG" || true
fi
echo "llama.cpp @ $(git -C "$SRC" rev-parse --short HEAD)" | tee -a "$LOG"

echo "### configure (incremental - keeps the expensive .cu objects)" | tee -a "$LOG"
[ "${FRESH:-0}" = "1" ] && rm -rf "$BUILD"
# SERVER stays ON: the unified 'llama' launcher links against llama-server-impl
# and llama-cli-impl. Re-running cmake over an existing build dir just refreshes
# the cache; object files are preserved.
cmake -S "$SRC" -B "$BUILD" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_CUDA=ON \
  -DGGML_CUDA_FA_ALL_QUANTS=OFF \
  -DCMAKE_CUDA_ARCHITECTURES=75 \
  -DLLAMA_CURL=OFF \
  -DLLAMA_BUILD_TESTS=OFF \
  2>&1 | tee -a "$LOG" | tail -30

# The M0 spot-check uses llama-bench (-o json) only. The unified 'llama' CLI in
# current llama.cpp needs sub-impl libs that this lean config does not produce,
# and llama-bench gives structured prefill/gen tok/s + n_gpu_layers directly.
echo "### build llama-bench" | tee -a "$LOG"
cmake --build "$BUILD" --target llama-bench -j "$(nproc)" 2>&1 | tee -a "$LOG" | tail -20

echo "### install to ~/.local/{bin,lib}" | tee -a "$LOG"
mkdir -p "$HOME/.local/bin" "$HOME/.local/lib"
cp -v "$BUILD/bin/llama-bench" "$HOME/.local/bin/llama-bench" | tee -a "$LOG"
cp -v "$BUILD"/bin/libggml*.so* "$BUILD"/bin/libllama*.so* "$HOME/.local/lib/" 2>/dev/null | tee -a "$LOG" || true
# ggml shared libs, if the build produced them
find "$BUILD" -name 'libggml*.so' -o -name 'libllama*.so' 2>/dev/null | while read -r so; do
  cp -v "$so" "$HOME/.local/lib/" 2>/dev/null || { mkdir -p "$HOME/.local/lib"; cp -v "$so" "$HOME/.local/lib/"; }
done | tee -a "$LOG" || true

echo "### smoke test" | tee -a "$LOG"
export LD_LIBRARY_PATH="$HOME/.local/lib:${LD_LIBRARY_PATH:-}"
"$HOME/.local/bin/llama-bench" --help 2>&1 | head -30 | tee -a "$LOG"
echo "BUILD OK" | tee -a "$LOG"
