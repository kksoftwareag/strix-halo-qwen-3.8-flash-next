#!/usr/bin/env bash
# Dritter Versuch für die Aufgaben, die auch im zweiten Anlauf ins Zeitlimit liefen – mit 3 Stunden.
# Ergebnisse in einem eigenen Ordner; report.py führt sie als dritten Versuch mit auf.
set -uo pipefail

main() {
  cd "$(dirname "$0")/../.."
  local TIMEOUT="${TB_AGENT_TIMEOUT:-10800}"
  local RES="${TB_RESULTS:-$PWD/state/quality/tbench-versuch3}"
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

  mapfile -t paare < <(python3 bench/quality/offene_zeitlimits.py)
  if [ ${#paare[@]} -eq 0 ]; then
    echo "=== keine Zeitlimit-Fälle offen"; return 0
  fi
  for paar in "${paare[@]}"; do
    local q="${paar%%:*}" tasks="${paar#*:}"
    local log="state/quality/tbmini-${q}-versuch3.log"
    echo "=== $q  Start $(date '+%F %T')  Zeitlimit ${TIMEOUT}s  Aufgaben: $tasks"
    warte_auf_speicher
    uv run --quiet python bench/quality/tbench.py \
      --tasks "$tasks" --attempts 1 --agent-timeout "$TIMEOUT" \
      --apt-mirror "${TB_APT_MIRROR:-ftp.fau.de}" \
      --results-dir "$RES" \
      --quant "$q" --job-name "tbmini-${q}-v3" > "$log" 2>&1
    echo "=== $q  Ende  $(date '+%F %T')  exit $?  Log: $log"
  done
  echo "=== alle Wiederholungen fertig $(date '+%F %T')"
}

main "$@"
