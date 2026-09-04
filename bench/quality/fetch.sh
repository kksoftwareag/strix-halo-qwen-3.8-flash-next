#!/usr/bin/env bash
# Holt den Agenten-Benchmark Terminal-Bench-Mini-20 (20 Aufgaben aus Terminal-Bench 2.1,
# Apache-2.0) und prüft die Voraussetzungen. Der Klon liegt unter bench/quality/terminal-bench-mini
# und wird nicht mitversioniert.
set -euo pipefail

REPO="${TBM_REPO:-https://github.com/kyuz0/terminal-bench-mini.git}"
COMMIT="${TBM_COMMIT:-3e181f1d51e89a39577b031a6e5558ff36142997}"
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HERE/terminal-bench-mini"

if [ ! -d "$DEST/.git" ]; then
  echo "== klone $REPO"
  git clone --quiet "$REPO" "$DEST"
fi
echo "== setze auf $COMMIT"
git -C "$DEST" fetch --quiet origin
git -C "$DEST" checkout --quiet "$COMMIT"
git -C "$DEST" log -1 --format='   %h %ci %s'

echo
echo "== Voraussetzungen"
ok=0
check() { printf '   %-22s %s\n' "$1" "$2"; }
py=$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')
check "python3" "$py $( [ "${py%%.*}" -ge 3 ] && python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)' && echo "(ok)" || { echo "(zu alt, >= 3.11 nötig)"; ok=1; } )"
if command -v docker >/dev/null; then
  check "docker" "$(docker --version 2>&1 | head -1)"
  if docker compose version >/dev/null 2>&1; then
    check "docker compose" "$(docker compose version --short 2>&1 | head -1)"
  else
    check "docker compose" "FEHLT (Compose v2 wird gebraucht)"; ok=1
  fi
  docker info >/dev/null 2>&1 || { check "docker info" "kein Zugriff ohne sudo"; ok=1; }
else
  check "docker" "FEHLT"; ok=1
fi
command -v uv >/dev/null && check "uv" "$(uv --version)" || { check "uv" "FEHLT (für harbor==0.20.0)"; ok=1; }
command -v tmux >/dev/null && check "tmux" "$(tmux -V)" || check "tmux" "fehlt (optional, aber empfohlen)"
free_gib=$(awk '/MemAvailable/ {printf "%.1f", $2/1048576}' /proc/meminfo)
check "MemAvailable" "$free_gib GiB"
disk=$(df -h --output=avail "$HERE" | tail -1 | tr -d ' ')
check "Platz für Images" "$disk (die Task-Images brauchen ~30-60 GB)"

echo
if [ "$ok" -eq 0 ]; then
  echo "Bereit. Rauchtest:  ./run.sh ... bzw. bench/quality/tbench.py --tier smoke"
else
  echo "Es fehlen Voraussetzungen (siehe oben)."
  exit 1
fi
