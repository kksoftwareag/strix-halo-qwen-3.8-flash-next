#!/usr/bin/env bash
# Sweep 1: HIP-Build-Vergleich (User-Build ohne rocWMMA vs. eigener Build mit rocWMMA-FA),
# KV-Cache f16 vs q8_0, ubatch 512/1024/2048, Quant Q4_K_XL vs Q2_K_XL. Reines llama-bench (ohne MTP).
set -uo pipefail
OUT="$(cd "$(dirname "$0")/.." && pwd)/bench/results/raw"
mkdir -p "$OUT"
HF=${HF_HOME:-$HOME/.cache/huggingface}/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots
M4=$HF/c8b5954a88c2775c546b92593eda40ea041d3176/UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf
M2=$HF/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-Q2_K_XL/Qwen3.8-Flash-Next-UD-Q2_K_XL-00001-of-00003.gguf
USER_BENCH=${USER_BENCH:-$HOME/models/llama.cpp-mtp/build/bin/llama-bench}   # optionaler Vergleichs-Build
NEW_BENCH="$(cd "$(dirname "$0")/.." && pwd)/engine/build-hip/bin/llama-bench"
run() {
  local name=$1; shift
  echo "### $(date +%T) $name: $*"
  local t0=$SECONDS
  "$@" -o json --progress > "$OUT/$name.json" 2> "$OUT/$name.err"
  echo "exit=$? dauer=$((SECONDS-t0))s"
  python3 - "$OUT/$name.json" <<'PY'
import json,sys
try:
    d=json.load(open(sys.argv[1]))
    for r in d: print(f"   {r['test']:>8}  {r['avg_ts']:8.2f} t/s ± {r['stddev_ts']:.2f}   (ub={r['n_ubatch']} ctk={r['type_k']} ctv={r['type_v']} fa={r['flash_attn']})")
except Exception as e: print("   (kein JSON:", e, ")")
PY
}
COMMON=(-ngl 99 -t 16 -fa on -p 512 -n 128 -r 2 --tensor-read-lazy auto)
run 01-userhip-q4kxl-f16        "$USER_BENCH" -m "$M4" "${COMMON[@]}" -ctk f16 -ctv f16
run 02-rocwmma-q4kxl-f16        "$NEW_BENCH"  -m "$M4" "${COMMON[@]}" -ctk f16 -ctv f16
run 03-rocwmma-q4kxl-q8         env LLAMA_ATTN_ROT_DISABLE=1 "$NEW_BENCH" -m "$M4" "${COMMON[@]}" -ctk q8_0 -ctv q8_0
run 04-rocwmma-q4kxl-f16-ub1024 "$NEW_BENCH"  -m "$M4" "${COMMON[@]}" -ctk f16 -ctv f16 -ub 1024 -b 2048
run 05-rocwmma-q4kxl-f16-ub2048 "$NEW_BENCH"  -m "$M4" "${COMMON[@]}" -ctk f16 -ctv f16 -ub 2048 -b 2048
run 06-rocwmma-q2kxl-f16        "$NEW_BENCH"  -m "$M2" "${COMMON[@]}" -ctk f16 -ctv f16
run 07-userhip-q2kxl-f16        "$USER_BENCH" -m "$M2" "${COMMON[@]}" -ctk f16 -ctv f16
echo "### fertig $(date +%T)"
