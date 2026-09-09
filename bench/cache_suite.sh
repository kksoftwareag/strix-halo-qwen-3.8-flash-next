#!/usr/bin/env bash
# Messreihe zum Cache- und Slot-Verhalten. Vier Läufe, jeder startet seinen eigenen Server:
#
#   mtp-aus    wie der Basislauf, aber ohne MTP -> zeigt, wie viel vom Checkpoint der Draft-State ist
#   split-lang eine Sitzung mit langem Prompt bei statisch geteiltem KV -> Prompt passt nicht in den Slot
#   kvu-lang   dieselbe Sitzung mit gemeinsamem KV-Pool -> eine Sitzung darf den ganzen Pool nutzen
#   kvu-vier   vier Sitzungen auf dem gemeinsamen Pool -> Trefferquote und Tempo gegen den Basislauf
#
#   bench/cache_suite.sh [nur-diese-tags ...]
set -uo pipefail

main() {
  cd "$(dirname "$0")/.."
  local WANT=("$@")
  local PY=.venv/bin/python
  local OUT=state/bench
  mkdir -p "$OUT"

  will() { [ ${#WANT[@]} -eq 0 ] && return 0; local t; for t in "${WANT[@]}"; do [ "$t" = "$1" ] && return 0; done; return 1; }

  # Auf einen eventuell noch laufenden Lauf warten, damit sich zwei Server nie überlappen.
  while pgrep -f "[c]ache_probe.py" >/dev/null; do sleep 20; done

  if will mtp-aus; then
    echo "== mtp-aus $(date '+%T')"
    $PY -u bench/cache_probe.py --tag mtp-aus --no-mtp --slots 2 --ctx-per-slot 32768 \
      --sessions 4 --turns 3 --prefix-tokens 8000 2>&1 | tee "$OUT/cache-mtp-aus.log"
  fi

  if will split-lang; then
    echo "== split-lang $(date '+%T')  (erwartet: Prompt zu lang für den Slot)"
    $PY -u bench/cache_probe.py --tag split-lang --kv-unified off --slots 4 --ctx-per-slot 16384 \
      --sessions 1 --turns 1 --prefix-tokens 30000 2>&1 | tee "$OUT/cache-split-lang.log"
  fi

  if will kvu-lang; then
    echo "== kvu-lang $(date '+%T')  (erwartet: dieselbe Anfrage läuft durch)"
    $PY -u bench/cache_probe.py --tag kvu-lang --kv-unified on --slots 4 --ctx-per-slot 16384 \
      --sessions 1 --turns 1 --prefix-tokens 30000 2>&1 | tee "$OUT/cache-kvu-lang.log"
  fi

  if will kvu-vier; then
    echo "== kvu-vier $(date '+%T')"
    $PY -u bench/cache_probe.py --tag kvu-vier --kv-unified on --slots 2 --ctx-per-slot 32768 \
      --sessions 4 --turns 3 --prefix-tokens 8000 2>&1 | tee "$OUT/cache-kvu-vier.log"
  fi

  echo "== Messreihe fertig $(date '+%F %T')"
}

main "$@"
