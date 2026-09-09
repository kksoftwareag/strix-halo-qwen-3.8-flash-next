#!/usr/bin/env bash
# Dritte Messreihe. Die zweite hat gezeigt: ohne Context-Checkpoints meldet der Server
# "forcing full prompt re-processing due to lack of cache data (hybrid/recurrent memory)" –
# bei diesem Modell sind die Checkpoints der Cache. Offen bleiben zwei Fragen:
#
#   ckpt0-gepinnt   jede Sitzung hat ihren eigenen Slot. Dann wird nichts verdrängt, der Zustand
#                   bleibt im Slot – braucht es dafür überhaupt Checkpoints?
#   ckpt1-geteilt   mehr Sitzungen als Slots, aber nur ein einziger Checkpoint je Slot.
#                   Reicht einer zum Wiederherstellen? Das wäre die billigste Variante.
set -uo pipefail

main() {
  cd "$(dirname "$0")/.."
  local PY=.venv/bin/python OUT=state/bench
  mkdir -p "$OUT"
  while pgrep -f "[c]ache_probe.py" >/dev/null; do sleep 20; done

  echo "== ckpt0-gepinnt $(date '+%T')"
  $PY -u bench/cache_probe.py --tag ckpt0-gepinnt --ctx-checkpoints 0 \
    --slots 4 --ctx-per-slot 32768 --sessions 4 --turns 3 --prefix-tokens 8000 \
    2>&1 | tee "$OUT/cache-ckpt0-gepinnt.log"

  echo "== ckpt1-geteilt $(date '+%T')"
  $PY -u bench/cache_probe.py --tag ckpt1-geteilt --ctx-checkpoints 1 \
    --slots 2 --ctx-per-slot 32768 --sessions 4 --turns 3 --prefix-tokens 8000 \
    2>&1 | tee "$OUT/cache-ckpt1-geteilt.log"

  echo "== Reihe 3 fertig $(date '+%F %T')"
}

main "$@"
