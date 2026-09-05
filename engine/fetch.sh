#!/usr/bin/env bash
# Holt die Quellen beider Engines aus öffentlichen Repositories und wendet die Patches an.
#   src/            llama.cpp (ggml-org) am festgehaltenen Commit + Patches 0001-0004
#   engramhalo-src/ EngramHalo.cpp (Aristo94), Branch strix-halo-qwen4exp, festgehaltener Commit + Patches 0002-0004
# Patches:
#   0001 qwen4exp-MTP-Draft-Head (nach dzannotti, PR #27836)
#   0002 ROCm/iGPU-Host-Puffer (Issue #25992) – ohne den liefern mehrere Slots auf gfx1151 Unsinn
#   0003 Scheduler-Ring-Puffer (PR #27311) – ohne den fällt die MTP-Akzeptanz bei -np N mit langen Prompts auf 0
#   0004 Draft-Kontext je Sequenz statt gesamt (Issue #28433)
# ENGINE_RING_PATCH=0 lässt 0003 und 0004 weg (Vergleichsmessung „vorher").
# Nutzung: engine/fetch.sh [stock|engramhalo|all]   (Default: all)
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LLAMA_COMMIT="$(cat "$HERE/patches/BASE_COMMIT")"
EH_REPO="https://github.com/Aristo94/EngramHalo.cpp"
EH_BRANCH="strix-halo-qwen4exp"
EH_COMMIT="${EH_COMMIT:-60bce1a304394203e4e4285cf795138026d9f793}"

apply_patch() {  # apply_patch <dir> <patch>
  # Erst direkt, dann als Drei-Wege-Merge (nötig für den EngramHalo-Fork, dessen ggml-Dateien abweichen).
  if git -C "$1" apply --reverse --check "$2" 2>/dev/null; then echo "  Patch $(basename "$2") bereits enthalten";
  elif git -C "$1" apply --check "$2" 2>/dev/null; then git -C "$1" apply "$2"; echo "  Patch $(basename "$2") angewendet";
  elif git -C "$1" apply -3 --check "$2" 2>/dev/null; then git -C "$1" apply -3 "$2"; echo "  Patch $(basename "$2") per Drei-Wege-Merge angewendet";
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
  if [[ "${ENGINE_RING_PATCH:-1}" == "1" ]]; then
    apply_patch "$HERE/src" "$HERE/patches/0003-27311-uma-ring-buffer.patch"
    apply_patch "$HERE/src" "$HERE/patches/0004-28433-draft-ctx-per-seq.patch"
  fi
}
fetch_engramhalo() {
  if [[ ! -d "$HERE/engramhalo-src/.git" ]]; then
    git clone --branch "$EH_BRANCH" "$EH_REPO" "$HERE/engramhalo-src"
  fi
  git -C "$HERE/engramhalo-src" fetch --quiet origin "$EH_BRANCH" || true
  git -C "$HERE/engramhalo-src" checkout --quiet "$EH_COMMIT" 2>/dev/null || git -C "$HERE/engramhalo-src" checkout --quiet "$EH_BRANCH"
  if [[ "${ENGINE_RING_PATCH:-1}" == "1" ]]; then
    # Für den Drei-Wege-Merge braucht git die Blobs des llama.cpp-Basis-Commits.
    git -C "$HERE/engramhalo-src" fetch --quiet https://github.com/ggml-org/llama.cpp "$LLAMA_COMMIT" 2>/dev/null || \
      git -C "$HERE/engramhalo-src" fetch --quiet "$HERE/src" "$LLAMA_COMMIT" 2>/dev/null || true
    apply_patch "$HERE/engramhalo-src" "$HERE/patches/0003-27311-uma-ring-buffer.patch"
    apply_patch "$HERE/engramhalo-src" "$HERE/patches/0004-28433-draft-ctx-per-seq.patch"
  fi
  apply_patch "$HERE/engramhalo-src" "$HERE/patches/0002-25992-rocm-igpu-host-buffer.patch"
}
case "${1:-all}" in
  stock) fetch_stock ;;
  engramhalo) fetch_engramhalo ;;
  all) fetch_stock; fetch_engramhalo ;;
  *) echo "usage: $0 [stock|engramhalo|all]" >&2; exit 1 ;;
esac
echo "Quellen bereit. Bauen: engine/build.sh hip && engine/build-engramhalo.sh"
