#!/usr/bin/env bash
# Zweiter Versuch für die Aufgaben, die im ersten Durchgang ins Zeitlimit gelaufen sind –
# mit 50 % mehr Zeit (5400 statt 3600 Sekunden je Aufgabe).
#
# Die Ergebnisse landen in einem eigenen Ordner, damit der erste Durchgang unangetastet
# bleibt; report.py führt beide zu pass@1 und pass@2 zusammen.
set -uo pipefail

main() {
  cd "$(dirname "$0")/../.."
  local TIMEOUT="${TB_AGENT_TIMEOUT:-5400}"
  local RES="${TB_RESULTS:-state/quality/tbench-versuch2}"
  local FREI_GIB="${TB_FREE_GIB:-95}"
  mkdir -p state/quality

  # Quant:Aufgabenliste – ermittelt aus dem ersten Durchgang (AgentTimeoutError)
  local paare=(
    "UD-IQ1_M:extract-elf,llm-inference-batching-scheduler,regex-log"
    "UD-IQ3_XXS:build-pov-ray,llm-inference-batching-scheduler"
    "UD-IQ4_XS:build-pov-ray,llm-inference-batching-scheduler"
  )

  warte_auf_speicher() {
    local frei
    for _ in $(seq 1 120); do
      frei=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)
      [ "$frei" -ge "$FREI_GIB" ] && return 0
      sleep 5
    done
    echo "WARNUNG: nur ${frei} GiB frei" >&2
  }

  for paar in "${paare[@]}"; do
    local q="${paar%%:*}" tasks="${paar#*:}"
    local log="state/quality/tbmini-${q}-versuch2.log"
    echo "=== $q  Start $(date '+%F %T')  Zeitlimit ${TIMEOUT}s  Aufgaben: $tasks"
    warte_auf_speicher
    uv run --quiet python bench/quality/tbench.py \
      --tasks "$tasks" --attempts 1 --agent-timeout "$TIMEOUT" \
      --apt-mirror "${TB_APT_MIRROR:-ftp.fau.de}" \
      --results-dir "$RES" \
      --quant "$q" --job-name "tbmini-${q}-v2" > "$log" 2>&1
    echo "=== $q  Ende  $(date '+%F %T')  exit $?  Log: $log"
  done
  echo "=== alle Wiederholungen fertig $(date '+%F %T')"
}

main "$@"
