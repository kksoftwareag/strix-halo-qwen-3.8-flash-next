"""Exportiert die aktuelle Konfiguration als eigenständiges Bash-Startskript bzw. systemd-User-Unit."""
from __future__ import annotations

import shlex
from datetime import datetime
from pathlib import Path

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


def systemd_unit(cfg: ServerConfig, cmd: Command, script_path: str,
                 python: str = "", memguard: str = "", workdir: str = "") -> str:
    """User-Unit für den Server.

    Läuft unter bench/memguard.py, wenn Pfade übergeben werden: GPU-Speicher (GTT) taucht in keiner
    cgroup-Grenze auf, MemoryMax hilft hier also nicht – nur MemAvailable zeigt, wie nah ein Kernel-OOM
    ist. Der Wächter beendet den Server vorher. Weil ein solcher Abbruch sich sofort wiederholen würde,
    ist der Neustart begrenzt: drei Versuche in zehn Minuten, danach bleibt der Dienst aus.
    """
    workdir = workdir or str(Path(script_path).parent.parent)
    if python and memguard:
        schwelle = cfg.mem_guard_gib if cfg.mem_guard_gib > 0 else 6.0
        start = (f"{python} {memguard} --min-avail-gib {schwelle:g} -- {script_path}")
    else:
        start = script_path
    return f"""[Unit]
Description=Qwen3.8-Flash-Next llama.cpp Server ({cfg.profile_name})
Documentation=https://github.com/kksoftwareag/strix-halo-qwen-3.8-flash-next
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=600
StartLimitBurst=3

[Service]
Type=simple
WorkingDirectory={workdir}
ExecStart={start}
Restart=on-failure
RestartSec=30
TimeoutStartSec=900
TimeoutStopSec=120
KillMode=mixed
LimitMEMLOCK=infinity
LimitNOFILE=65536
Nice=-5
OOMPolicy=stop
NoNewPrivileges=yes
PrivateTmp=yes
ProtectControlGroups=yes
ProtectKernelTunables=yes
RestrictSUIDSGID=yes

[Install]
WantedBy=default.target
"""
