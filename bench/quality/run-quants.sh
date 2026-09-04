#!/usr/bin/env bash
# Terminal-Bench-Mini-20 nacheinander für mehrere Quants laufen lassen.
# Ein Stream (np 1), MTP an, ein Versuch je Aufgabe (pass@1).
#
#   bench/quality/run-quants.sh                          # Q2_K_XL, IQ1_M, IQ3_XXS, IQ4_XS
#   bench/quality/run-quants.sh UD-IQ4_XS                # nur einer
#   TB_AGENT_TIMEOUT=1800 bench/quality/run-quants.sh    # anderes Zeitlimit je Aufgabe (Default 3600)
set -uo pipefail
cd "$(dirname "$0")/../.."

QUANTS=("$@")
[ ${#QUANTS[@]} -eq 0 ] && QUANTS=(UD-Q2_K_XL UD-IQ1_M UD-IQ3_XXS UD-IQ4_XS)
TIMEOUT="${TB_AGENT_TIMEOUT:-3600}"
FREI_GIB="${TB_FREE_GIB:-95}"
# Der Spiegel wird fest gesetzt: archive.ubuntu.com ist aus diesem Netz zeitweise
# unbrauchbar langsam, und ein Fehlschlag beim apt-Aufruf lässt jede Aufgabe scheitern.
mkdir -p state/quality

warte_auf_speicher() {
  for _ in $(seq 1 120); do
    frei=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)
    [ "$frei" -ge "$FREI_GIB" ] && return 0
    sleep 5
  done
  echo "WARNUNG: nur ${frei} GiB frei (erwartet >= ${FREI_GIB})" >&2
  return 1
}

for q in "${QUANTS[@]}"; do
  log="state/quality/tbmini-$q.log"
  echo "=== $q  Start $(date '+%F %T')  Zeitlimit ${TIMEOUT}s/Aufgabe"
  warte_auf_speicher
  uv run --quiet python bench/quality/tbench.py \
    --tier full --attempts 1 --agent-timeout "$TIMEOUT" \
    --apt-mirror "${TB_APT_MIRROR:-ftp.fau.de}" \
    --quant "$q" --job-name "tbmini-${q}" > "$log" 2>&1
  rc=$?
  echo "=== $q  Ende  $(date '+%F %T')  exit $rc  Log: $log"
  grep -E "^(Results|Aggregate|Passed):" "$log" | tail -3
done
echo "=== alle Quants fertig $(date '+%F %T')"
