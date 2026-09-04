#!/usr/bin/env bash
# Baut EngramHalo.cpp (Aristo94, Branch strix-halo-qwen4exp) als HIP-Backend für gfx1151.
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/engramhalo-src"
JOBS="${JOBS:-16}"
# gfx1151-Mehrslot-Workaround (ggml-org/llama.cpp#25992 / PR #25863): pinned Host-Puffer auf iGPU aus
P2="$HERE/patches/0002-25992-rocm-igpu-host-buffer.patch"
if git -C "$SRC" apply --check "$P2" 2>/dev/null; then git -C "$SRC" apply "$P2"; echo "Patch #25992 angewendet"; fi
HIPCXX=/usr/lib64/rocm/llvm/bin/clang++ \
cmake -S "$SRC" -B "$HERE/build-engramhalo" -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DLLAMA_CURL=OFF -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DLLAMA_BUILD_MTMD=OFF -DLLAMA_BUILD_UI=OFF \
  -DGGML_NATIVE=ON -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1151 -DGPU_TARGETS=gfx1151 \
  -DCMAKE_HIP_COMPILER=/usr/lib64/rocm/llvm/bin/clang++
# Zielnamen: llama-server + llama-bench (klassische Binaries) – falls die App existiert, zusätzlich bin/llama
cmake --build "$HERE/build-engramhalo" -j"$JOBS" --target llama-server llama-bench llama-cli
ninja -C "$HERE/build-engramhalo" bin/llama 2>/dev/null || true
ls -la "$HERE/build-engramhalo/bin/" | grep -E "llama(-server|-bench|-cli)?$"
