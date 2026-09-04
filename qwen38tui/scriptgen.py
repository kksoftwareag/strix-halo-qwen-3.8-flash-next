"""Exportiert die aktuelle Konfiguration als eigenständiges Bash-Startskript bzw. systemd-User-Unit."""
from __future__ import annotations

import shlex
from datetime import datetime

from .config import Command, ServerConfig


def bash_script(cfg: ServerConfig, cmd: Command) -> str:
    r = cmd.resolved
    lines = [
        "#!/usr/bin/env bash",
        f"# Qwen3.8-Flash-Next – llama.cpp Server ({cfg.profile_name})",
        f"# generiert von qwen38-flash TUI am {datetime.now():%Y-%m-%d %H:%M}",
        f"# Engine: {r.engine.label if r.engine else '?'}",
        f"# Modell: {r.model.quant if r.model else '?'}  MTP: {'an' if (cfg.mtp_enabled and r.mtp) else 'aus'}",
        "set -euo pipefail",
        "",
    ]
    for k, v in cmd.env.items():
        lines.append(f"export {k}={shlex.quote(v)}")
    if cmd.env:
        lines.append("")
    argv = cmd.argv
    lines.append(f"BIN={shlex.quote(argv[0])}")
    lines.append('ARGS=(')
    i = 1
    while i < len(argv):
        a = argv[i]
        if a.startswith("-") and i + 1 < len(argv) and not argv[i + 1].startswith("-"):
            lines.append(f"    {shlex.quote(a)} {shlex.quote(argv[i + 1])}")
            i += 2
        else:
            lines.append(f"    {shlex.quote(a)}")
            i += 1
    lines.append(")")
    lines.append("")
    lines.append('exec "$BIN" "${ARGS[@]}" "$@"')
    return "\n".join(lines) + "\n"


def systemd_unit(cfg: ServerConfig, cmd: Command, script_path: str) -> str:
    return f"""[Unit]
Description=Qwen3.8-Flash-Next llama.cpp Server ({cfg.profile_name})
After=network-online.target

[Service]
Type=simple
ExecStart={script_path}
Restart=on-failure
RestartSec=5
LimitMEMLOCK=infinity
Nice=-5

[Install]
WantedBy=default.target
"""
