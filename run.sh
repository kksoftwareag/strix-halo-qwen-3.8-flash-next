#!/usr/bin/env bash
# Startet das Terminal-UI (legt beim ersten Mal die Python-Umgebung per uv an).
cd "$(dirname "$0")"
exec uv run --quiet qwen38 "$@"
