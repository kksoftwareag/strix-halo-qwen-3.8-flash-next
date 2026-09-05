#!/usr/bin/env bash
# Mehrnutzer-Messreihe mit langen Kontexten – der Vergleich für den Ring-Puffer-Patch (PR #27311).
#
#   bench/mtp_multiuser.sh vorher                    # alle vier Quants, bestehende Builds
#   bench/mtp_multiuser.sh nachher                   # nach engine/fetch.sh + Neubau
#   bench/mtp_multiuser.sh vorher UD-IQ4_XS          # nur ein Quant
#   TB_LEVELS=1,4,16 TB_GEN=2000 bench/mtp_multiuser.sh vorher
#
# Je Quant: 1/2/4/8/16 gleichzeitige Nutzer, je ~30k Token Prompt (eigener Text je Nutzer, kein
# geteilter Prompt-Cache) und ~5k Token Ausgabe, MTP an. Entscheidend ist die Spalte "Draft": ohne
# den Patch fällt die Akzeptanz bei mehreren Slots und langen Prompts auf 0,00.
#
# Zeitbedarf: rund 2 Stunden je Quant und Durchgang – der Löwenanteil ist das Verarbeiten der
# Prompts (16 × 30k = 480k Token je Stufe).
set -uo pipefail
cd "$(dirname "$0")/.."

LABEL="${1:-lauf}"; shift || true
QUANTS=("$@")
[ ${#QUANTS[@]} -eq 0 ] && QUANTS=(UD-IQ4_XS UD-IQ3_XXS UD-Q2_K_XL UD-IQ1_M)
LEVELS="${TB_LEVELS:-1,2,4,8,16}"
CTX="${TB_CTX:-30000}"
GEN="${TB_GEN:-5000}"
FREI_GIB="${TB_FREE_GIB:-95}"
mkdir -p state/bench

warte_auf_speicher() {
  for _ in $(seq 1 120); do
    frei=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)
    [ "$frei" -ge "$FREI_GIB" ] && return 0
    sleep 5
  done
  echo "WARNUNG: nur ${frei} GiB frei (erwartet >= ${FREI_GIB})" >&2
}

ring="nein"; [ -f engine/patches/0003-27311-uma-ring-buffer.patch ] && ring="Patch liegt vor (ob gebaut, sagt das Log der Engine)"
for q in "${QUANTS[@]}"; do
  STAMP="$(date '+%Y%m%d-%H%M%S')"
  OUT="state/bench/mtp-multiuser-${LABEL}-${q}-${STAMP}.log"
  {
    echo "== Mehrnutzer-Messreihe '$LABEL', Quant $q, $(date '+%F %T')"
    echo "== Stufen $LEVELS, Prompt ${CTX} Token, Ausgabe ${GEN} Token, MTP an"
    echo "== Ring-Puffer-Patch: $ring"
  } | tee "$OUT"
  warte_auf_speicher
  ./run.sh bench-parallel \
    --preset eh-agent --quant "$q" \
    --users 16 --levels "$LEVELS" \
    --ctx-tokens "$CTX" --max-tokens "$GEN" \
    --keep-mtp 2>&1 | tee -a "$OUT"
  echo "== $q fertig $(date '+%F %T'), Log: $OUT" | tee -a "$OUT"
done
echo "== alle Quants fertig $(date '+%F %T')"
