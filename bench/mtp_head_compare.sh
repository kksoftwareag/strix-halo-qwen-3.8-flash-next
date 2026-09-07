#!/usr/bin/env bash
# Vergleicht Draft-Heads und Engine-Stände: Decode-Rate und Draft-Akzeptanz bei kurzem und tiefem Kontext.
#
#   bench/mtp_head_compare.sh <label> [head-key ...]
#
# Ohne Kopf-Argumente werden alle kompatiblen Köpfe gemessen. Je Kopf zwei Stufen:
# kurzer Prompt (~0 Kontext) und ~30k Kontext – dort liegt der Alltag eines Agenten.
set -uo pipefail

main() {
  cd "$(dirname "$0")/.."
  local LABEL="${1:-lauf}"; shift || true
  local HEADS=("$@")
  if [ ${#HEADS[@]} -eq 0 ]; then
    mapfile -t HEADS < <(./run.sh inventory 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
for h in d['mtp_heads']:
    if h['style'] == 'output_hc':
        print(h['key'])")
  fi
  local QUANT="${TB_QUANT:-UD-IQ4_XS}" GEN="${TB_GEN:-600}"
  local STAMP; STAMP="$(date '+%Y%m%d-%H%M%S')"
  local OUT="state/bench/mtp-heads-${LABEL}-${STAMP}.log"
  mkdir -p state/bench

  { echo "== Draft-Head-Vergleich '$LABEL', Quant $QUANT, $(date '+%F %T')"
    echo "== Engine: $(engine/build-engramhalo/bin/llama version 2>&1 | head -1)"; } | tee "$OUT"

  for head in "${HEADS[@]}"; do
    for ctx in 0 30000; do
      echo "-- Kopf $head, Kontext ${ctx} Token" | tee -a "$OUT"
      ./run.sh bench-parallel --preset eh-agent --quant "$QUANT" --mtp-head "$head" \
        --users 1 --levels 1 --ctx-tokens "$ctx" --max-tokens "$GEN" --keep-mtp 2>&1 \
        | grep -E "^\[bench\] 1 Nutzer:|^\s+1\s" | tee -a "$OUT"
    done
  done
  echo "== fertig $(date '+%F %T'), Log: $OUT" | tee -a "$OUT"
}

main "$@"
