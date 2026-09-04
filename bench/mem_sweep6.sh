#!/usr/bin/env bash
# Sweep 6 (EngramHalo.cpp, engine/build-engramhalo): RAM-Modus vs SSD-Modus, MTP mit dzannotti-Head, Q4_K_XL im SSD-Modus.
set -uo pipefail
cd "$(dirname "$0")/.."
HF=$HOME/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots
M2=$HF/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-Q2_K_XL/Qwen3.8-Flash-Next-UD-Q2_K_XL-00001-of-00003.gguf
M3=$HF/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-IQ3_XXS/Qwen3.8-Flash-Next-UD-IQ3_XXS-00001-of-00003.gguf
M4X=$HF/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-IQ4_XS/Qwen3.8-Flash-Next-UD-IQ4_XS-00001-of-00003.gguf
M4=$HF/c8b5954a88c2775c546b92593eda40ea041d3176/UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf
MTP=$HOME/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf
BIN=engine/build-engramhalo/bin/llama
COMMON=(-ngl 999 -c 32768 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --jinja --chat-template-kwargs '{"reasoning_effort":"low"}' -np 1 -lv 4)
MTPARGS=(-md "$MTP" -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75)
export PROBE_ENV="ROCBLAS_USE_HIPBLASLT=1"
run() { echo "### $(date +%T) $1"; uv run python bench/mem_probe.py "$@"; echo; }
# RAM-Modus (Engram-Tabelle gepinnt), wie README-Config A
run eh-iq3-ram-mtp   -- $BIN serve -m "$M3"  "${COMMON[@]}" -lm none "${MTPARGS[@]}"
# SSD-Modus (mmap + lazy): IQ4_XS und – der eigentliche Preis – Q4_K_XL mit MTP
READY_TIMEOUT=1500 run eh-iq4xs-ssd-mtp -- $BIN serve -m "$M4X" "${COMMON[@]}" -lm mmap --tensor-read-lazy on "${MTPARGS[@]}"
READY_TIMEOUT=1500 run eh-q4kxl-ssd-mtp -- $BIN serve -m "$M4"  "${COMMON[@]}" -lm mmap --tensor-read-lazy on "${MTPARGS[@]}"
# Referenz ohne MTP im RAM-Modus (IQ3) für den Speedup
run eh-iq3-ram-nomtp -- $BIN serve -m "$M3"  "${COMMON[@]}" -lm none
echo "### fertig $(date +%T)"
