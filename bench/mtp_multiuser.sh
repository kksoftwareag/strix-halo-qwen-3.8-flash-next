#!/usr/bin/env bash
# Mehrnutzer-Messreihe mit langen Kontexten – der Vergleich für den Ring-Puffer-Patch (PR #27311).
#
#   bench/mtp_multiuser.sh vorher     # mit den bestehenden Builds (ohne 0003/0004)
#   bench/mtp_multiuser.sh nachher    # nach engine/fetch.sh + Neubau
#
# 1/2/4/8/16 gleichzeitige Nutzer, je ~30k Token Prompt (eigener Text je Nutzer, kein geteilter
# Prompt-Cache) und ~5k Token Ausgabe, MTP an. Entscheidend ist die Spalte "Draft": ohne den Patch
# fällt die Akzeptanz bei mehreren Slots und langen Prompts auf 0,00.
set -uo pipefail
cd "$(dirname "$0")/.."
LABEL="${1:-lauf}"
QUANT="${TB_QUANT:-UD-IQ4_XS}"     # IQ4_XS: 16 Slots à 35k passen bequem, Q4_K_XL wäre zu knapp
STAMP="$(date '+%Y%m%d-%H%M%S')"
OUT="state/bench/mtp-multiuser-${LABEL}-${STAMP}.log"
mkdir -p state/bench

echo "== Mehrnutzer-Messreihe '$LABEL', Quant $QUANT, $(date '+%F %T')" | tee "$OUT"
grep -c "ring" engine/patches/0003-27311-uma-ring-buffer.patch >/dev/null 2>&1 && \
  echo "== Patch 0003 vorhanden: $( [ -f engine/patches/0003-27311-uma-ring-buffer.patch ] && echo ja || echo nein )" | tee -a "$OUT"

./run.sh bench-parallel \
  --preset eh-agent --quant "$QUANT" \
  --users 16 --levels 1,2,4,8,16 \
  --ctx-tokens 30000 --max-tokens 5000 \
  --keep-mtp 2>&1 | tee -a "$OUT"

echo "== fertig $(date '+%F %T'), Log: $OUT" | tee -a "$OUT"
