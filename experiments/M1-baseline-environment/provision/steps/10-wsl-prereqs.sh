#!/usr/bin/env bash
# M1 step 10 - WSL build prerequisites: apt packages + pip toolchain.
# The one privileged step in the whole provision. VERIFY_ONLY=1 -> report only.
set -u

VERIFY_ONLY="${VERIFY_ONLY:-0}"
need_apt=()
fail=0

have() { command -v "$1" >/dev/null 2>&1; }

# --- apt-provided ---
for pkg_cmd in "jq:jq" "gcc:build-essential" "make:build-essential" "nvcc:nvidia-cuda-toolkit"; do
  cmd="${pkg_cmd%%:*}"; pkg="${pkg_cmd##*:}"
  if have "$cmd"; then
    echo "PASS $cmd present ($(command -v "$cmd"))"
  else
    echo "WARN $cmd missing -> apt package '$pkg'"
    need_apt+=("$pkg")
  fi
done

# de-dup
if [ ${#need_apt[@]} -gt 0 ]; then
  mapfile -t need_apt < <(printf '%s\n' "${need_apt[@]}" | sort -u)
fi

if [ ${#need_apt[@]} -gt 0 ]; then
  if [ "$VERIFY_ONLY" = "1" ]; then
    echo "FAIL missing apt packages (verify-only): ${need_apt[*]}"
    echo "     run (operator): sudo apt-get update && sudo apt-get install -y ${need_apt[*]}"
    fail=1
  else
    echo "DID  sudo apt-get install -y ${need_apt[*]}"
    if ! sudo apt-get update -qq || ! sudo apt-get install -y "${need_apt[@]}"; then
      echo "FAIL apt-get install failed (needs an interactive sudo password?)."
      echo "     run manually (operator): sudo apt-get install -y ${need_apt[*]}"
      fail=1
    fi
  fi
fi

# --- pip --user toolchain (cmake, ninja) ---
# python3-venv is absent on this host; bare pip3 had a broken SSL path.
# Use /usr/bin/python3 -m pip --user --break-system-packages explicitly.
PIP='/usr/bin/python3 -m pip'
export PATH="$HOME/.local/bin:$PATH"
for tool in cmake ninja; do
  if have "$tool"; then
    echo "PASS $tool present ($("$tool" --version 2>/dev/null | head -1))"
  elif [ "$VERIFY_ONLY" = "1" ]; then
    echo "FAIL $tool missing (verify-only). run: $PIP install --user --break-system-packages $tool"
    fail=1
  else
    echo "DID  $PIP install --user --break-system-packages $tool"
    if ! $PIP install --user --break-system-packages -q "$tool"; then
      echo "FAIL pip install $tool failed."
      fail=1
    fi
  fi
done

# --- GPU sanity from inside WSL (driver, not toolkit) ---
if nvidia-smi -L 2>/dev/null | grep -q 'GPU 0:'; then
  echo "PASS nvidia-smi sees the GPU"
else
  echo "WARN nvidia-smi -L did not list a GPU inside WSL"
fi

[ "$fail" -eq 0 ] && echo "DID  wsl prereqs satisfied" || true
exit "$fail"
