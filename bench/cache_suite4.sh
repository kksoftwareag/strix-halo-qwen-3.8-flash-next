#!/usr/bin/env bash
# Gegenprobe für das Preset eh-team (8 Slots à 196608 Token, geteilter KV, --ctx-checkpoints 1).
#
#   team-acht   acht Sitzungen auf acht Slots – der Auslegungsfall: jeder Agent hat seinen Platz,
#               nichts wird verdrängt, der Cache muss also durchgehend greifen.
#
# Der Überlastfall (zwölf Sitzungen auf acht Slots) wurde separat gemessen: der RAM-Prompt-Cache
# fasst bei --cache-ram 2048 nur zehn Einträge à 378 MiB, danach fällt die Trefferquote auf 0 %.
#   team-tief          eine Sitzung mit 60k Präfix: erreicht ein Slot wirklich die tiefe Kontextgröße,
#                      und greift der Cache auch dort?
set -uo pipefail

main() {
  cd "$(dirname "$0")/.."
  local PY=.venv/bin/python OUT=state/bench
  local GEMEINSAM=(--preset eh-team --quant UD-IQ3_XXS --slots 8 --ctx-per-slot 131072
                   --kv-unified off --ctx-checkpoints 1 --checkpoint-min-step 65536 --cache-ram 2048)
  mkdir -p "$OUT"
  while pgrep -f "[c]ache_probe.py" >/dev/null; do sleep 20; done

  echo "== team-acht $(date '+%T')"
  $PY -u bench/cache_probe.py --tag team-acht "${GEMEINSAM[@]}" \
    --sessions 8 --turns 3 --prefix-tokens 8000 2>&1 | tee "$OUT/cache-team-acht.log"

  echo "== team-tief $(date '+%T')"
  $PY -u bench/cache_probe.py --tag team-tief "${GEMEINSAM[@]}" \
    --sessions 1 --turns 3 --prefix-tokens 60000 2>&1 | tee "$OUT/cache-team-tief.log"

  echo "== Reihe 4 fertig $(date '+%F %T')"
}

main "$@"
