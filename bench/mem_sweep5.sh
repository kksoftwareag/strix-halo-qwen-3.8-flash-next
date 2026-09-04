#!/usr/bin/env bash
# Sweep 5 (Stock-Fork engine/build-hip): Rotation ohne LLAMA_ATTN_ROT_DISABLE, MTP-Footprints IQ4_XS / IQ3_XXS / Q2 (dzannotti-Head).
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
# 1) Rotation aktiv (Env NICHT gesetzt) – lädt der Stock-Fork mit q8_0 KV?
# 2) MTP-Footprints mit Rotation aus (wie bisher)
PROBE_ENV="LLAMA_ATTN_ROT_DISABLE=1" run q2-mtp-dz    -- $BIN serve -m "$M2"  "${COMMON[@]}" "${MTPARGS[@]}"
PROBE_ENV="LLAMA_ATTN_ROT_DISABLE=1" run iq3xxs-mtp-dz -- $BIN serve -m "$M3"  "${COMMON[@]}" "${MTPARGS[@]}"
PROBE_ENV="LLAMA_ATTN_ROT_DISABLE=1" run iq4xs-mtp-dz  -- $BIN serve -m "$M4X" "${COMMON[@]}" "${MTPARGS[@]}"
echo "### fertig $(date +%T)"
