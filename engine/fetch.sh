#!/usr/bin/env bash
# Holt die Quellen beider Engines aus öffentlichen Repositories und wendet die Patches an.
#   src/            llama.cpp (ggml-org) am festgehaltenen Commit + Patch 0001 (qwen4exp-MTP-Draft-Head, nach dzannotti) + 0002
#   engramhalo-src/ EngramHalo.cpp (Aristo94), Branch strix-halo-qwen4exp, festgehaltener Commit + Patch 0002
# Nutzung: engine/fetch.sh [stock|engramhalo|all]   (Default: all)
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LLAMA_COMMIT="$(cat "$HERE/patches/BASE_COMMIT")"
EH_REPO="https://github.com/Aristo94/EngramHalo.cpp"
EH_BRANCH="strix-halo-qwen4exp"
EH_COMMIT="${EH_COMMIT:-60bce1a304394203e4e4285cf795138026d9f793}"

apply_patch() {  # apply_patch <dir> <patch>
  if git -C "$1" apply --check "$2" 2>/dev/null; then git -C "$1" apply "$2"; echo "  Patch $(basename "$2") angewendet";
  elif git -C "$1" apply --reverse --check "$2" 2>/dev/null; then echo "  Patch $(basename "$2") bereits enthalten";
  else echo "FEHLER: Patch $(basename "$2") passt nicht auf $1" >&2; exit 1; fi
}
fetch_stock() {
  if [[ ! -d "$HERE/src/.git" ]]; then
    git clone https://github.com/ggml-org/llama.cpp "$HERE/src"
  fi
  git -C "$HERE/src" fetch --quiet origin "$LLAMA_COMMIT" || true
  git -C "$HERE/src" checkout --quiet "$LLAMA_COMMIT"
  apply_patch "$HERE/src" "$HERE/patches/0001-qwen4exp-mtp-draft-head-local.patch"
  apply_patch "$HERE/src" "$HERE/patches/0002-25992-rocm-igpu-host-buffer.patch"
}
fetch_engramhalo() {
  if [[ ! -d "$HERE/engramhalo-src/.git" ]]; then
    git clone --branch "$EH_BRANCH" "$EH_REPO" "$HERE/engramhalo-src"
  fi
  git -C "$HERE/engramhalo-src" fetch --quiet origin "$EH_BRANCH" || true
  git -C "$HERE/engramhalo-src" checkout --quiet "$EH_COMMIT" 2>/dev/null || git -C "$HERE/engramhalo-src" checkout --quiet "$EH_BRANCH"
  apply_patch "$HERE/engramhalo-src" "$HERE/patches/0002-25992-rocm-igpu-host-buffer.patch"
}
case "${1:-all}" in
  stock) fetch_stock ;;
  engramhalo) fetch_engramhalo ;;
  all) fetch_stock; fetch_engramhalo ;;
  *) echo "usage: $0 [stock|engramhalo|all]" >&2; exit 1 ;;
esac
echo "Quellen bereit. Bauen: engine/build.sh hip && engine/build-engramhalo.sh"
