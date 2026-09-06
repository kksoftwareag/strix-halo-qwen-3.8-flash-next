#!/usr/bin/env bash
# Zweiter Versuch für alle übrigen gescheiterten Aufgaben (die, die der Verifier abgelehnt hat).
# Zusammen mit rerun-timeouts.sh ergibt das ein vollständiges pass@2: jede im ersten Durchgang
# gescheiterte Aufgabe bekommt genau einen zweiten Versuch, durchgehend mit 5400 s Zeitlimit.
#
# Die Aufgabenliste wird aus den Ergebnissen des ersten Durchgangs abgeleitet; bereits
# wiederholte Aufgaben werden übersprungen.
set -uo pipefail

main() {
  cd "$(dirname "$0")/../.."
  local TIMEOUT="${TB_AGENT_TIMEOUT:-5400}"
  local RES="${TB_RESULTS:-$PWD/state/quality/tbench-versuch2}"
  local FREI_GIB="${TB_FREE_GIB:-95}"

  warte_auf_speicher() {
    local frei
    for _ in $(seq 1 120); do
      frei=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)
      [ "$frei" -ge "$FREI_GIB" ] && return 0
      sleep 5
    done
    echo "WARNUNG: nur ${frei} GiB frei" >&2
  }

  mapfile -t paare < <(python3 bench/quality/offene_wiederholungen.py)
  if [ ${#paare[@]} -eq 0 ]; then
    echo "=== nichts zu wiederholen"; return 0
  fi
  for paar in "${paare[@]}"; do
    local q="${paar%%:*}" tasks="${paar#*:}"
    local log="state/quality/tbmini-${q}-versuch2b.log"
    echo "=== $q  Start $(date '+%F %T')  Zeitlimit ${TIMEOUT}s  Aufgaben: $tasks"
    warte_auf_speicher
    uv run --quiet python bench/quality/tbench.py \
      --tasks "$tasks" --attempts 1 --agent-timeout "$TIMEOUT" \
      --apt-mirror "${TB_APT_MIRROR:-ftp.fau.de}" \
      --results-dir "$RES" \
      --quant "$q" --job-name "tbmini-${q}-v2b" > "$log" 2>&1
    echo "=== $q  Ende  $(date '+%F %T')  exit $?  Log: $log"
  done
  echo "=== alle Wiederholungen fertig $(date '+%F %T')"
}

main "$@"
