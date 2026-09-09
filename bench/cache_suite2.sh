#!/usr/bin/env bash
# Zweite Messreihe: lohnen sich Context-Checkpoints? Sie sind bei diesem Modell teuer – mit MTP
# wächst jeder um 2072 Byte je Token, bei 200k Kontext also rund 500 MiB je Stück. Gebraucht werden
# sie nur, wenn der Prompt von der zwischengespeicherten Fassung abweicht.
#
#   ckpt0-anhaengen  Agent hängt nur an, Checkpoints aus -> reicht der reine Präfix-Cache?
#   ckpt4-divergenz  Agent schreibt die Verlaufsmitte um, 4 Checkpoints je Slot
#   ckpt0-divergenz  dieselbe Divergenz ohne Checkpoints -> das ist der Preis des Sparens
set -uo pipefail

main() {
  cd "$(dirname "$0")/.."
  local PY=.venv/bin/python OUT=state/bench
  mkdir -p "$OUT"
  while pgrep -f "[c]ache_probe.py" >/dev/null; do sleep 20; done

  echo "== ckpt0-anhaengen $(date '+%T')"
  $PY -u bench/cache_probe.py --tag ckpt0-anhaengen --ctx-checkpoints 0 \
    --slots 2 --ctx-per-slot 32768 --sessions 4 --turns 3 --prefix-tokens 8000 \
    2>&1 | tee "$OUT/cache-ckpt0-anhaengen.log"

  echo "== ckpt4-divergenz $(date '+%T')"
  $PY -u bench/cache_probe.py --tag ckpt4-divergenz --ctx-checkpoints 4 --checkpoint-min-step 2048 \
    --slots 2 --ctx-per-slot 32768 --sessions 2 --turns 4 --prefix-tokens 8000 --diverge-at 2 \
    2>&1 | tee "$OUT/cache-ckpt4-divergenz.log"

  echo "== ckpt0-divergenz $(date '+%T')"
  $PY -u bench/cache_probe.py --tag ckpt0-divergenz --ctx-checkpoints 0 \
    --slots 2 --ctx-per-slot 32768 --sessions 2 --turns 4 --prefix-tokens 8000 --diverge-at 2 \
    2>&1 | tee "$OUT/cache-ckpt0-divergenz.log"

  echo "== Reihe 2 fertig $(date '+%F %T')"
}

main "$@"
