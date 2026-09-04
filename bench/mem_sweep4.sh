#!/usr/bin/env bash
# Sweep 4: Ladegeschwindigkeit mit --load-mode mmap (zeitbegrenzt) und Footprint IQ4_XS / IQ3_XXS mit MTP im Default-Lademodus.
set -uo pipefail
cd "$(dirname "$0")/.."
HF=$HOME/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932
M2=$HF/UD-Q2_K_XL/Qwen3.8-Flash-Next-UD-Q2_K_XL-00001-of-00003.gguf
M3=$HF/UD-IQ3_XXS/Qwen3.8-Flash-Next-UD-IQ3_XXS-00001-of-00003.gguf
M4X=$HF/UD-IQ4_XS/Qwen3.8-Flash-Next-UD-IQ4_XS-00001-of-00003.gguf
MTP=$HOME/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf
BIN=engine/build-hip/bin/llama
COMMON=(-ngl 99 -c 32768 -fa on -ctk q8_0 -ctv q8_0 -t 16 --jinja --chat-template-kwargs '{"reasoning_effort":"low"}' -np 1 -lv 4)
MTPARGS=(-md "$MTP" -ngld 99 --spec-type draft-mtp --spec-draft-n-max 3 --spec-draft-p-min 0.75)
run() { echo "### $(date +%T) $1"; uv run python bench/mem_probe.py "$@"; echo; }
# 1) mmap-Ladegeschwindigkeit: nach 300 s abbrechen, Lesevolumen zeigt die Rate
READY_TIMEOUT=300 run q2-mmap-loadtest -- $BIN serve -m "$M2" "${COMMON[@]}" --load-mode mmap
# 2) Footprints im Default-Lademodus (PLE resident) mit MTP
run iq4xs-mtp  -- $BIN serve -m "$M4X" "${COMMON[@]}" "${MTPARGS[@]}"
run iq3xxs-mtp -- $BIN serve -m "$M3" "${COMMON[@]}" "${MTPARGS[@]}"
run q2-mtp     -- $BIN serve -m "$M2" "${COMMON[@]}" "${MTPARGS[@]}"
echo "### fertig $(date +%T)"
