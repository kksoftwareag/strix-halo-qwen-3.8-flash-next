#!/usr/bin/env bash
# Footprint-Sweep 3: --load-mode mmap erzwingen (ROCm-Backend meldet sonst "kein mmap" -> PLE-Tabelle wird kopiert).
set -uo pipefail
cd "$(dirname "$0")/.."
HF=$HOME/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots
M4=$HF/c8b5954a88c2775c546b92593eda40ea041d3176/UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf
M2=$HF/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-Q2_K_XL/Qwen3.8-Flash-Next-UD-Q2_K_XL-00001-of-00003.gguf
MTP=$HOME/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf
BIN=engine/build-hip/bin/llama
COMMON=(-ngl 99 -c 32768 -fa on -ctk q8_0 -ctv q8_0 -t 16 --tensor-read-lazy auto --jinja --chat-template-kwargs '{"reasoning_effort":"low"}' -np 1 -lv 4)
MTPARGS=(-md "$MTP" -ngld 99 --spec-type draft-mtp --spec-draft-n-max 3 --spec-draft-p-min 0.75)
run() { echo "### $(date +%T) $1"; uv run python bench/mem_probe.py "$@"; echo; }
run q4-mmap          -- $BIN serve -m "$M4" "${COMMON[@]}" --load-mode mmap
run q4-mmap-nohost   -- $BIN serve -m "$M4" "${COMMON[@]}" --load-mode mmap --no-host
run q4-mmap-mtp      -- $BIN serve -m "$M4" "${COMMON[@]}" --load-mode mmap "${MTPARGS[@]}"
run q2-mmap          -- $BIN serve -m "$M2" "${COMMON[@]}" --load-mode mmap
echo "### fertig $(date +%T)"
