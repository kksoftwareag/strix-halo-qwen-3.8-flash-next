#!/usr/bin/env bash
# Baut die gepatchte llama.cpp-Variante (qwen4exp + MTP-Draft-Head) in zwei Backends:
#   build-vulkan : GGML_VULKAN (Mesa RADV)
#   build-hip    : GGML_HIP für gfx1151 + rocWMMA Flash-Attention
# Nutzung: ./build.sh [vulkan|hip|all]   (Default: all)
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/src"
JOBS="${JOBS:-16}"
# gfx1151-Mehrslot-Workaround (ggml-org/llama.cpp#25992 / PR #25863): pinned Host-Puffer auf iGPU aus
P2="$HERE/patches/0002-25992-rocm-igpu-host-buffer.patch"
if git -C "$SRC" apply --check "$P2" 2>/dev/null; then git -C "$SRC" apply "$P2"; echo "Patch #25992 angewendet"; fi
COMMON=(
  -G Ninja
  -DCMAKE_BUILD_TYPE=Release
  -DLLAMA_CURL=OFF
  -DLLAMA_BUILD_TESTS=OFF
  -DLLAMA_BUILD_EXAMPLES=OFF
  -DLLAMA_BUILD_MTMD=OFF
  -DLLAMA_BUILD_UI=OFF
  -DLLAMA_USE_PREBUILT_UI=ON
  -DGGML_NATIVE=ON
  -DGGML_CCACHE=ON
)
build_vulkan() {
  if ! command -v glslc >/dev/null 2>&1 || [[ ! -f /usr/include/vulkan/vulkan.h ]]; then
    echo "Vulkan-Build uebersprungen: vulkan-headers / vulkan-loader-devel / glslc fehlen." >&2
    echo "  sudo dnf install vulkan-headers vulkan-loader-devel glslc" >&2
    return 0
  fi
  cmake -S "$SRC" -B "$HERE/build-vulkan" "${COMMON[@]}" -DGGML_VULKAN=ON
  cmake --build "$HERE/build-vulkan" -j"$JOBS" --target llama llama-bench
}
build_hip() {
  HIPCXX=/usr/lib64/rocm/llvm/bin/clang++ \
  cmake -S "$SRC" -B "$HERE/build-hip" "${COMMON[@]}" \
    -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1151 -DGPU_TARGETS=gfx1151 \
    -DCMAKE_HIP_COMPILER=/usr/lib64/rocm/llvm/bin/clang++ \
    -DGGML_HIP_ROCWMMA_FATTN=ON
  cmake --build "$HERE/build-hip" -j"$JOBS" --target llama llama-bench
}
case "${1:-all}" in
  vulkan) build_vulkan ;;
  hip)    build_hip ;;
  all)    build_vulkan; build_hip ;;
  *) echo "usage: $0 [vulkan|hip|all]" >&2; exit 1 ;;
esac
