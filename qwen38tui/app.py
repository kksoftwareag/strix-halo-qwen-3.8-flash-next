"""Textual-TUI: Konfiguration, Server-Steuerung, Benchmarks, Systemzustand für Qwen3.8-Flash-Next auf Strix Halo."""
from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path
from typing import Any

from textual import on, work
from textual.markup import escape
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (Button, DataTable, Footer, Header, Input, Label, Markdown, RichLog, Select, Static, Switch,
                             TabbedContent, TabPane)

from . import bench as benchmod
from .config import (CTX_CHOICES, CURRENT_CONFIG, KV_TYPES, LAZY_MODES, LOAD_MODES, REASONING_EFFORTS, TRISTATE, UBATCH_CHOICES,
                     Command, ServerConfig, build_command, delete_profile, list_profiles, load_profile, resolve, save_profile)
from .discovery import PROJECT_DIR, STATE_DIR, Inventory, discover_all
from .hardware import GIB, HardwareInfo, probe
from .memory import MemoryEstimate, estimate, fits
from .presets import PRESETS, get_preset
from .scriptgen import bash_script, systemd_unit
from .server import ServerClient, ServerProcess, port_in_use

GIB_F = float(GIB)

# ------------------------------------------------------------------------------------------------
# Formular-Definition: (feld, label, art, optionen|None, hilfe)
# art: select | switch | int | float | text
# ------------------------------------------------------------------------------------------------
def _opts(values: list[Any], labels: dict[Any, str] | None = None) -> list[tuple[str, Any]]:
    return [((labels or {}).get(v, str(v)), v) for v in values]


SECTIONS: list[tuple[str, list[tuple[str, str, str, Any, str]]]] = [
    ("Engine & Modell", [
        ("engine", "Engine (Backend)", "select", None, "ROCm/HIP-Build mit qwen4exp-MTP-Patch bevorzugen."),
        ("quant", "Quant", "select", None, "auto = größter Quant, der ins Speicherbudget passt."),
        ("tensor_read_lazy", "PLE-Tabelle lazy lesen", "select", _opts(LAZY_MODES, {"auto": "auto (lazy, da > 4 GiB)", "on": "on (immer lazy)", "off": "off (26.8 GiB resident)"}),
         "Die 26.8-GiB-Per-Layer-Embedding-Tabelle wird per mmap zeilenweise von NVMe gelesen statt im RAM gehalten."),
        ("no_host", "--no-host (kein gepinnter Host-Puffer)", "switch", None, "Pflicht im HIP-Build, damit die PLE-Tabelle lazy bleibt (sonst +27 GiB RAM → OOM)."),
        ("ple_cpu_override", "PLE per -ot auf CPU-Puffer", "switch", None, "Alternative/Ergänzung zu --no-host: nur die PLE-Tabelle in den normalen CPU-Puffer."),
        ("load_mode", "Lade-Modus", "select", _opts(LOAD_MODES), "Explizit 'mmap' setzen! Bei 'auto' nutzt ROCm kein mmap und kopiert die PLE-Tabelle (28 GiB) in den RAM."),
        ("n_gpu_layers", "GPU-Layer (-ngl)", "int", None, "99 = alles auf die iGPU (Unified Memory)."),
    ]),
    ("Kontext & KV-Cache", [
        ("ctx_size", "Kontext (Tokens)", "int", None, f"Trainingskontext 262144. Übliche Werte: {', '.join(map(str, CTX_CHOICES))}."),
        ("cache_type_k", "KV-Cache Typ K", "select", _opts(KV_TYPES), "q8_0 halbiert den KV-Speicher bei minimalem Qualitätsverlust; braucht LLAMA_ATTN_ROT_DISABLE=1."),
        ("cache_type_v", "KV-Cache Typ V", "select", _opts(KV_TYPES), "Quantisierter V-Cache erfordert Flash Attention."),
        ("flash_attn", "Flash Attention", "select", _opts(["on", "off", "auto"]), ""),
        ("batch_size", "Batch (-b)", "int", None, "Logische Batchgröße."),
        ("ubatch_size", "µBatch (-ub)", "int", None, f"Physische Batchgröße für Prompt-Processing ({', '.join(map(str, UBATCH_CHOICES))}); Benchmark: 512 vs 2048 kaum Unterschied."),
        ("threads", "CPU-Threads (-t)", "int", None, "Physische Kerne (16)."),
        ("n_parallel", "Slots (-np)", "int", None, "Parallele Anfragen; Einzelnutzer: 1."),
        ("kv_unified", "KV unified", "select", _opts(TRISTATE), ""),
        ("cache_ram_mib", "Prompt-Cache (MiB)", "int", None, "--cache-ram: 0 aus, -1 unbegrenzt (OOM-Risiko)."),
        ("cache_reuse", "Cache-Reuse (Tokens)", "int", None, "0 = aus. Bei Hybrid-/Rekurrenz-Modellen meist wirkungslos."),
    ]),
    ("Spekulatives Decoding (MTP)", [
        ("mtp_enabled", "MTP aktiv", "switch", None, "Native Multi-Token-Prediction als Draft-Head (--spec-type draft-mtp)."),
        ("mtp_head", "MTP-Head", "select", None, "auto = unsloth-Head, sonst dzannotti."),
        ("spec_draft_n_max", "Draft-Tiefe n_max", "int", None, "Tokens pro Draft-Runde (2–5)."),
        ("spec_draft_n_min", "Draft n_min", "int", None, "0 = kein Minimum."),
        ("spec_draft_p_min", "Draft p_min", "float", None, "Mindest-Wahrscheinlichkeit des Draft-Tokens (0 = alle nehmen)."),
        ("spec_draft_p_split", "Draft p_split", "float", None, "Split-Wahrscheinlichkeit (Default 0.10)."),
        ("spec_extra_types", "Zusätzliche Spec-Typen", "text", None, "z.B. ngram-mod (kommagetrennt)."),
    ]),
    ("Reasoning", [
        ("thinking", "Thinking aktiv", "switch", None, "enable_thinking im Chat-Template."),
        ("reasoning_effort", "Reasoning-Effort", "select", _opts(REASONING_EFFORTS), "Template erlaubt nur xhigh (Default), medium, low."),
        ("reasoning_budget", "Thinking-Budget (Tokens)", "int", None, "-1 = unbegrenzt."),
        ("reasoning_format", "Reasoning-Format", "select", _opts(["auto", "deepseek", "deepseek-legacy", "none"]), ""),
    ]),
    ("Sampling-Defaults", [
        ("temp", "Temperatur", "float", None, "Qwen-Empfehlung 1.0 (im GGUF hinterlegt)."),
        ("top_p", "Top-p", "float", None, "0.95"),
        ("top_k", "Top-k", "int", None, "20"),
        ("min_p", "Min-p", "float", None, "0.0"),
        ("presence_penalty", "Presence-Penalty", "float", None, "0–2 gegen Wiederholungen (Qwen: bis 1.5 bei Bedarf)."),
        ("repeat_penalty", "Repeat-Penalty", "float", None, "1.0 = aus."),
    ]),
    ("Server", [
        ("host", "Host", "text", None, "auto = LAN-IP; 127.0.0.1 nur lokal; 0.0.0.0 alle."),
        ("port", "Port", "int", None, ""),
        ("api_key", "API-Key", "text", None, "leer = ohne Authentifizierung."),
        ("alias", "Modell-Alias", "text", None, "Name im /v1/models."),
        ("metrics", "/metrics aktiv", "switch", None, "Prometheus-Endpunkt (für Monitoring-Panel)."),
        ("webui", "Web-UI aktiv", "switch", None, ""),
        ("warmup", "Warmup beim Start", "switch", None, ""),
        ("sleep_idle_seconds", "Schlafen nach Idle (s)", "int", None, "-1 = nie."),
        ("log_verbosity", "Log-Verbosity (-lv)", "int", None, "4 = Puffergrößen & lazy-Meldungen sichtbar; -1 = Flag weglassen."),
        ("extra_args", "Zusätzliche Argumente", "text", None, "Roh an llama serve angehängt."),
    ]),
    ("Schutz", [
        ("attn_rot_disable", "LLAMA_ATTN_ROT_DISABLE", "select", _opts(TRISTATE), "off = Rotation aktiv (bessere Qualität bei q8_0-KV, gemessen nur ~2 % langsamer). on = alte Workaround-Variable."),
        ("hipblaslt", "ROCBLAS_USE_HIPBLASLT=1", "switch", None, "hipBLASLt für GEMMs (EngramHalo-Empfehlung, Benchmark-Tab prüfen)."),
        ("mem_guard_gib", "Speicher-Wächter (GiB frei)", "float", None, "Server wird hart gestoppt, wenn MemAvailable darunter fällt. 0 = aus."),
    ]),
]

FIELD_KIND = {f[0]: f[2] for _, fs in SECTIONS for f in fs}


class Qwen38App(App):
    TITLE = "Qwen3.8-Flash-Next · llama.cpp · Strix Halo"
    CSS = """
    Screen { layout: vertical; }
    #cfg-row { height: 1fr; }
    #form { width: 3fr; padding: 0 1; }
    #side { width: 2fr; padding: 0 1; border-left: solid $primary-darken-2; }
    .section { color: $accent; text-style: bold; padding: 1 0 0 0; }
    .field { height: 3; }
    .field Label { width: 30; padding: 1 1 0 0; color: $text-muted; }
    .field Select { width: 1fr; }
    .field Input { width: 1fr; }
    .field Switch { }
    .help { color: $text-muted; height: 1; padding: 0 0 0 31; }
    #mem, #warn, #cmd { border: round $primary-darken-2; padding: 0 1; margin: 0 0 1 0; }
    #mem { height: auto; }
    #warn { height: auto; min-height: 3; }
    #cmd { height: 1fr; }
    .toolbar { height: 3; }
    .toolbar Button { margin: 0 1 0 0; }
    .toolbar Select { width: 40; }
    .toolbar Input { width: 30; }
    .toolbar Label { padding: 1 1 0 0; color: $text-muted; }
    #bench-users { width: 8; }
    #srv-status { height: auto; border: round $primary-darken-2; padding: 0 1; }
    #srv-log { height: 1fr; border: round $primary-darken-2; }
    #bench-table { height: 14; }
    #bench-log { height: 1fr; border: round $primary-darken-2; }
    #sys-table { height: 1fr; }
    #sys-tips { height: 1fr; border: round $primary-darken-2; padding: 0 1; }
    """
    BINDINGS = [
        ("f5", "start_server", "Server starten"),
        ("f6", "stop_server", "Server stoppen"),
        ("ctrl+s", "save_current", "Speichern"),
        ("f9", "export_script", "Skript exportieren"),
        ("f8", "refresh_all", "Neu einlesen"),
        ("q", "quit_app", "Beenden"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.inv: Inventory = discover_all()
        self.hw: HardwareInfo = probe()
        self.cfg: ServerConfig = self._load_initial()
        self.server = ServerProcess()
        self.client: ServerClient | None = None
        self._bench_abort = False
        self._bench_running = False
        self._building = True   # unterdrückt Change-Events beim Aufbau

    # ------------------------------------------------------------------ Start
    def _load_initial(self) -> ServerConfig:
        try:
            if CURRENT_CONFIG.exists():
                return ServerConfig.load(CURRENT_CONFIG)
        except Exception:
            pass
        has_eh = any(e.key == "hip-engramhalo" for e in self.inv.engines)
        pr = get_preset("eh-qualitaet" if has_eh else "stock-ausgewogen")
        return pr.apply() if pr else ServerConfig()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with TabbedContent(initial="tab-cfg"):
            with TabPane("Konfiguration", id="tab-cfg"):
                with Horizontal(classes="toolbar"):
                    yield Select([(p.title, p.key) for p in PRESETS], prompt="Preset wählen…", id="preset-select")
                    yield Button("Preset anwenden", id="btn-preset", variant="primary")
                    yield Select([(n, n) for n in list_profiles()], prompt="Profil…", id="profile-select", allow_blank=True)
                    yield Button("Laden", id="btn-profile-load")
                    yield Input(placeholder="Profilname", id="profile-name")
                    yield Button("Speichern", id="btn-profile-save")
                    yield Button("Löschen", id="btn-profile-del", variant="error")
                with Horizontal(id="cfg-row"):
                    with VerticalScroll(id="form"):
                        yield from self._compose_form()
                    with Vertical(id="side"):
                        yield Static("", id="mem")
                        yield Static("", id="warn")
                        yield Static("", id="cmd")
            with TabPane("Server", id="tab-srv"):
                with Horizontal(classes="toolbar"):
                    yield Button("▶ Starten (F5)", id="btn-start", variant="success")
                    yield Button("■ Stoppen (F6)", id="btn-stop", variant="error")
                    yield Button("Test-Prompt", id="btn-test")
                    yield Button("Log leeren", id="btn-clearlog")
                yield Static("Server: gestoppt", id="srv-status")
                yield RichLog(id="srv-log", max_lines=3000, wrap=True, markup=False, highlight=False)
            with TabPane("Benchmark", id="tab-bench"):
                with Horizontal(classes="toolbar"):
                    yield Button("llama-bench pp512/tg128", id="btn-bench-quick")
                    yield Button("llama-bench @16k Tiefe", id="btn-bench-depth")
                    yield Button("Server-Messung (aktuelle Konfig, mit MTP)", id="btn-bench-server")
                    yield Button("MTP-Sweep (Auto-Tuning)", id="btn-bench-sweep", variant="primary")
                    yield Button("Abbrechen", id="btn-bench-abort", variant="error")
                with Horizontal(classes="toolbar"):
                    yield Label("Gleichzeitige Nutzer (1–8):")
                    yield Input(value="8", id="bench-users", type="integer")
                    yield Label("MTP dabei behalten:")
                    yield Switch(value=False, id="bench-keep-mtp")
                    yield Button("Mehrnutzer-Skalierung 1/2/4/8", id="btn-bench-scale", variant="primary")
                    yield Button("Mehrnutzer-Test (N gleichzeitig)", id="btn-bench-users")
                yield DataTable(id="bench-table", zebra_stripes=True)
                yield RichLog(id="bench-log", max_lines=2000, wrap=True, markup=False, highlight=False)
            with TabPane("System", id="tab-sys"):
                with Horizontal(classes="toolbar"):
                    yield Button("Neu prüfen", id="btn-sys-refresh")
                with Horizontal():
                    yield DataTable(id="sys-table", show_cursor=False)
                    yield Static("", id="sys-tips")
            with TabPane("Hilfe", id="tab-help"):
                yield Markdown(self._help_text(), id="help")
        yield Footer()

    def _compose_form(self) -> ComposeResult:
        for title, fields_ in SECTIONS:
            yield Static(title, classes="section")
            for key, label, kind, options, help_ in fields_:
                with Horizontal(classes="field"):
                    yield Label(label)
                    yield self._make_widget(key, kind, options)
                if help_:
                    yield Static(help_, classes="help")

    def _make_widget(self, key: str, kind: str, options: Any):
        wid = f"f-{key}"
        val = getattr(self.cfg, key)
        if kind == "select":
            if key == "engine":
                options = [("auto (bester HIP-Build mit MTP)", "auto")] + [(e.label, e.key) for e in self.inv.engines]
            elif key == "quant":
                options = [("auto (größter passender Quant)", "auto")] + [(m.label, m.quant) for m in self.inv.models]
            elif key == "mtp_head":
                options = [("auto", "auto")] + [(h.label, h.key) for h in self.inv.mtp_heads]
            values = [v for _, v in options]
            if val not in values:
                val = values[0] if values else Select.NULL
            return Select(options, value=val, id=wid, allow_blank=False)
        if kind == "switch":
            return Switch(value=bool(val), id=wid)
        if kind == "int":
            return Input(value=str(int(val)), id=wid, type="integer")
        if kind == "float":
            return Input(value=f"{float(val):g}", id=wid, type="number")
        return Input(value=str(val), id=wid)

    def on_mount(self) -> None:
        self._building = False
        self._refresh_side()
        self._refresh_system()
        self._refresh_bench_table()
        self.set_interval(2.0, self._tick)
        srv_log = self.query_one("#srv-log", RichLog)
        srv_log.write(f"Projekt: {PROJECT_DIR}")
        srv_log.write(f"Engines: {', '.join(e.key for e in self.inv.engines) or 'keine!'}")
        srv_log.write(f"Modelle: {', '.join(m.quant for m in self.inv.models) or 'keine!'}")
        srv_log.write(f"MTP-Heads: {', '.join(h.key for h in self.inv.mtp_heads) or 'keine'}")

    # ------------------------------------------------------------------ Formular -> Config
    def _fits(self, m) -> bool:
        eng = self.inv.engine(self.cfg.engine) if self.cfg.engine != "auto" else self.inv.default_engine(prefer_mtp=self.cfg.mtp_enabled)
        return fits(self.cfg, m, None, self.hw, eng.backend if eng else "hip", bool(eng and eng.fast_lazy_ple))

    def _current_command(self) -> Command:
        # normalisierte Kopie: Eingabefelder dürfen zwischenzeitlich ungültig sein
        return build_command(self.cfg.copy(), self.inv, self.hw, fits=self._fits)

    def _commit_cfg(self) -> None:
        """Vor Start/Speichern: Werte normalisieren und Formular nachziehen."""
        self.cfg.normalize()
        self._push_cfg_to_form()

    def _set_field(self, key: str, raw: Any) -> None:
        kind = FIELD_KIND.get(key)
        try:
            if kind == "int":
                val = int(str(raw).strip() or 0)
            elif kind == "float":
                val = float(str(raw).strip().replace(",", ".") or 0)
            elif kind == "switch":
                val = bool(raw)
            else:
                val = raw
        except ValueError:
            return
        if getattr(self.cfg, key) == val:
            return
        setattr(self.cfg, key, val)      # keine Normalisierung pro Tastendruck (würde Nachbarfelder klemmen)
        self._refresh_side()

    @on(Select.Changed)
    def _on_select(self, ev: Select.Changed) -> None:
        if self._building or not ev.select.id or not ev.select.id.startswith("f-"):
            return
        if ev.value is Select.NULL:
            return
        self._set_field(ev.select.id[2:], ev.value)

    @on(Switch.Changed)
    def _on_switch(self, ev: Switch.Changed) -> None:
        if self._building or not ev.switch.id or not ev.switch.id.startswith("f-"):
            return
        self._set_field(ev.switch.id[2:], ev.value)

    @on(Input.Changed)
    def _on_input(self, ev: Input.Changed) -> None:
        if self._building or not ev.input.id or not ev.input.id.startswith("f-"):
            return
        self._set_field(ev.input.id[2:], ev.value)

    def _push_cfg_to_form(self) -> None:
        """Nach Preset/Profil-Laden alle Widgets aktualisieren."""
        self._building = True
        try:
            for _, fields_ in SECTIONS:
                for key, _label, kind, _opts_, _help in fields_:
                    w = self.query_one(f"#f-{key}")
                    val = getattr(self.cfg, key)
                    if isinstance(w, Select):
                        values = [v for _, v in w._options]  # noqa: SLF001
                        w.value = val if val in values else (values[0] if values else Select.NULL)
                    elif isinstance(w, Switch):
                        w.value = bool(val)
                    elif isinstance(w, Input):
                        w.value = f"{val:g}" if kind == "float" else str(val)
        finally:
            self._building = False
        self._refresh_side()

    # ------------------------------------------------------------------ Seitenleiste
    def _refresh_side(self) -> None:
        cmd = self._current_command()
        r = cmd.resolved
        est = estimate(self.cfg, r.model, r.mtp, self.hw, r.engine.backend if r.engine else "hip", bool(r.engine and r.engine.fast_lazy_ple))
        cls = {"ok": "green", "knapp": "yellow", "zu groß": "red"}[est.verdict]
        lines = [f"[b]Speicherbedarf[/b]  →  [{cls}]{est.verdict.upper()}[/{cls}]"]
        for k, v in est.rows():
            lines.append(f"{k:<34}{v}")
        if est.per_token_kv:
            lines.append(f"{'KV+Indexer pro Token':<34}{est.per_token_kv / 1024:6.1f} KiB")
        for n in est.notes:
            lines.append(f"[dim]· {escape(n)}[/dim]")
        if r.model:
            lines.append(f"[dim]Modell: {r.model.quant} – {r.model.size_gib:.1f} GiB, davon PLE {r.model.ple_bytes / GIB_F:.1f} GiB, Experten {r.model.exps_bytes / GIB_F:.1f} GiB[/dim]")
        if r.engine:
            lines.append(f"[dim]Engine: {r.engine.key} ({r.engine.backend}, MTP {'ja' if r.engine.supports_mtp else 'nein'})[/dim]")
        self.query_one("#mem", Static).update("\n".join(lines))
        wl = [f"[red]✖ {escape(e)}[/red]" for e in cmd.errors] + [f"[yellow]⚠ {escape(w)}[/yellow]" for w in cmd.warnings]
        self.query_one("#warn", Static).update("\n".join(wl) if wl else "[green]✔ keine Warnungen[/green]")
        self.query_one("#cmd", Static).update("[b]Kommando[/b]\n" + (escape(cmd.pretty()) if cmd.ok else "(nicht startbar)"))

    # ------------------------------------------------------------------ Toolbar-Aktionen
    @on(Button.Pressed, "#btn-preset")
    def _apply_preset(self) -> None:
        sel = self.query_one("#preset-select", Select)
        if sel.value is Select.NULL:
            self.notify("Bitte ein Preset wählen.", severity="warning")
            return
        pr = get_preset(str(sel.value))
        if pr:
            self.cfg = pr.apply(self.cfg)
            self._push_cfg_to_form()
            self.notify(f"Preset „{pr.title}“ angewendet: {pr.description}")

    @on(Button.Pressed, "#btn-profile-load")
    def _load_profile(self) -> None:
        sel = self.query_one("#profile-select", Select)
        if sel.value is Select.NULL:
            self.notify("Kein Profil gewählt.", severity="warning")
            return
        try:
            self.cfg = load_profile(str(sel.value))
            self._push_cfg_to_form()
            self.notify(f"Profil „{sel.value}“ geladen.")
        except Exception as e:
            self.notify(f"Profil laden fehlgeschlagen: {e}", severity="error")

    @on(Button.Pressed, "#btn-profile-save")
    def _save_profile(self) -> None:
        self._commit_cfg()
        name = self.query_one("#profile-name", Input).value.strip() or self.cfg.profile_name
        p = save_profile(self.cfg, name)
        self._refresh_profiles()
        self.notify(f"Profil gespeichert: {p.name}")

    @on(Button.Pressed, "#btn-profile-del")
    def _del_profile(self) -> None:
        sel = self.query_one("#profile-select", Select)
        if sel.value is Select.NULL:
            return
        delete_profile(str(sel.value))
        self._refresh_profiles()
        self.notify(f"Profil „{sel.value}“ gelöscht.", severity="warning")

    def _refresh_profiles(self) -> None:
        sel = self.query_one("#profile-select", Select)
        sel.set_options([(n, n) for n in list_profiles()])

    def action_save_current(self) -> None:
        self._commit_cfg()
        self.cfg.save(CURRENT_CONFIG)
        self.notify(f"Konfiguration gespeichert: {CURRENT_CONFIG}")

    def action_export_script(self) -> None:
        cmd = self._current_command()
        if not cmd.ok:
            self.notify("Konfiguration nicht startbar: " + "; ".join(cmd.errors), severity="error")
            return
        out = PROJECT_DIR / "scripts"
        out.mkdir(exist_ok=True)
        name = self.cfg.profile_name or "server"
        sh = out / f"start-{name}.sh"
        sh.write_text(bash_script(self.cfg, cmd))
        sh.chmod(0o755)
        (out / f"qwen38-{name}.service").write_text(systemd_unit(self.cfg, cmd, str(sh)))
        self.notify(f"Exportiert: {sh} (+ systemd-Unit)")

    def action_refresh_all(self) -> None:
        self.inv = discover_all()
        self.hw = probe()
        self._refresh_side()
        self._refresh_system()
        self.notify("Inventar und Hardware neu eingelesen.")

    async def action_quit_app(self) -> None:
        if self.server.running:
            self.notify("Server wird gestoppt (kann bei 80 GiB GTT eine Weile dauern)…", severity="warning", timeout=20)
            await self.server.stop(grace=60)
        self.exit()

    async def action_quit(self) -> None:   # Textuals Standard-Binding ctrl+q ebenfalls sauber beenden
        await self.action_quit_app()

    # ------------------------------------------------------------------ Server
    def _srv_log(self, line: str) -> None:
        self.query_one("#srv-log", RichLog).write(line)

    @on(Button.Pressed, "#btn-start")
    def action_start_server(self) -> None:
        if self.server.running:
            self.notify("Server läuft bereits.", severity="warning")
            return
        if self._bench_running:
            self.notify("Benchmark läuft – erst abbrechen.", severity="warning")
            return
        self._commit_cfg()
        cmd = self._current_command()
        if not cmd.ok:
            self.notify("Nicht startbar: " + "; ".join(cmd.errors), severity="error")
            return
        r = cmd.resolved
        self.hw = probe()
        est = estimate(self.cfg, r.model, r.mtp, self.hw, r.engine.backend if r.engine else "hip", bool(r.engine and r.engine.fast_lazy_ple))
        if est.verdict == "zu groß":
            self.notify(f"Abbruch: passt nicht in den Speicher (Spielraum {est.headroom / GIB_F:.1f} GiB). Kleinerer Quant/Kontext oder lazy PLE.", severity="error", timeout=10)
            return
        if est.verdict == "knapp":
            self.notify(f"Speicher knapp (Spielraum {est.headroom / GIB_F:.1f} GiB) – Wächter aktiv.", severity="warning", timeout=8)
        if port_in_use(self.cfg.port, r.host):
            self.notify(f"Port {self.cfg.port} ist belegt (anderer Server?).", severity="error")
            return
        for w in cmd.warnings:
            self._srv_log("⚠ " + w)
        self.cfg.save(CURRENT_CONFIG)
        self.query_one(TabbedContent).active = "tab-srv"
        self.run_worker(self._start_server(cmd), exclusive=True, group="server")

    async def _start_server(self, cmd: Command) -> None:
        self._srv_log("$ " + cmd.shell())
        try:
            await self.server.start(cmd, self._srv_log)
        except Exception as e:
            self.notify(f"Start fehlgeschlagen: {e}", severity="error")
            return
        r = cmd.resolved
        self.client = ServerClient(r.host, self.cfg.port, self.cfg.api_key)
        ok = await self.client.wait_ready(timeout=1200, should_abort=lambda: not self.server.running)
        if ok:
            self.notify(f"Server bereit: http://{r.host}:{self.cfg.port}", severity="information", timeout=8)
            if r.model:
                self.server.record_measurements(r.model.quant, self.cfg.ubatch_size, self.cfg.flash_attn)
        elif not self.server.running:
            self.notify(f"Server beendet (exit {self.server.exit_code}) – Log prüfen.", severity="error", timeout=10)

    @on(Button.Pressed, "#btn-stop")
    def action_stop_server(self) -> None:
        if not self.server.running:
            self.notify("Kein Server aktiv.", severity="warning")
            return
        self.run_worker(self._stop_server(), exclusive=True, group="server-stop")

    async def _stop_server(self) -> None:
        self.notify("Server wird gestoppt – GTT-Freigabe kann eine Weile dauern…", timeout=15)
        code = await self.server.stop()
        self.notify(f"Server gestoppt (exit {code}{', normal nach SIGINT' if code in (0, 1, -2) else ''}).")
        self._update_status()

    @on(Button.Pressed, "#btn-clearlog")
    def _clear_log(self) -> None:
        self.query_one("#srv-log", RichLog).clear()

    @on(Button.Pressed, "#btn-test")
    def _test_prompt(self) -> None:
        if not (self.server.running and self.client):
            self.notify("Server läuft nicht.", severity="warning")
            return
        self.run_worker(self._run_test_prompt(), exclusive=True, group="test")

    async def _run_test_prompt(self) -> None:
        assert self.client
        self._srv_log("── Test-Prompt ──")
        buf: list[str] = []

        def tok(t: str) -> None:
            buf.append(t)

        try:
            out = await self.client.chat("Nenne drei Vorteile von Unified Memory für lokale LLMs, kurz und auf Deutsch.", max_tokens=200, on_token=tok)
        except Exception as e:
            self._srv_log(f"Test fehlgeschlagen: {e}")
            return
        if out["reasoning"]:
            self._srv_log("[thinking] " + out["reasoning"][:400].replace("\n", " ") + (" …" if len(out["reasoning"]) > 400 else ""))
        self._srv_log(out["text"].strip())
        t = out["timings"]
        dn, da = t.get("draft_n", 0), t.get("draft_n_accepted", 0)
        self._srv_log(f"⏱ pp {t.get('prompt_per_second', 0):.1f} t/s · tg {t.get('predicted_per_second', 0):.2f} t/s · {t.get('predicted_n', 0)} Tokens"
                      + (f" · Draft-Akzeptanz {da}/{dn} ({da / dn:.0%})" if dn else ""))

    async def _tick(self) -> None:
        self._update_status()
        # Speicher-Wächter
        if self.server.running and self.cfg.mem_guard_gib > 0:
            hw = probe_fast()
            if hw < self.cfg.mem_guard_gib * GIB_F:
                self._srv_log(f"!!! Speicher-Wächter: nur noch {hw / GIB_F:.1f} GiB frei – Server wird gestoppt")
                self.notify(f"Speicher-Wächter: {hw / GIB_F:.1f} GiB frei – Server gestoppt!", severity="error", timeout=15)
                await self.server.stop(grace=2)

    def _update_status(self) -> None:
        s = self.server
        st = self.query_one("#srv-status", Static)
        if not s.running:
            txt = "Server: [b]gestoppt[/b]"
            if s.exit_code is not None:
                txt += f"  (letzter Exit {s.exit_code})"
            if s.log_path:
                txt += f"\nLog: {s.log_path}"
            st.update(txt)
            return
        r = s.command.resolved if s.command else None
        url = f"http://{r.host}:{self.cfg.port}" if r else "?"
        stt = s.stats
        avail = probe_fast() / GIB_F
        lines = [
            f"Server: [green]{'bereit' if s.ready else 'lädt…'}[/green]  PID {s.pid}  Uptime {int(s.uptime)}s  {url}  ·  frei: {avail:.1f} GiB",
            f"Modell {r.model.quant if r and r.model else '?'} · MTP {'an' if (r and r.mtp and self.cfg.mtp_enabled) else 'aus'} · ctx {stt.n_ctx or self.cfg.ctx_size} · Ladezeit {stt.load_seconds:.0f}s",
            f"Buffer: Modell {stt.model_buffer_mib / 1024:.1f} GiB · KV {stt.kv_buffer_mib / 1024:.2f} GiB · Compute {stt.compute_buffer_mib / 1024:.2f} GiB"
            + (f" · lazy: {', '.join(stt.lazy_tensors)}" if stt.lazy_tensors else ""),
            f"Letzte Anfrage: pp {stt.last_pp_tps:.1f} t/s · tg {stt.last_tg_tps:.2f} t/s · Anfragen {stt.requests}"
            + (f" · Draft-Akzeptanz {stt.accept_rate:.0%}" if stt.draft_n else ""),
        ]
        if stt.errors:
            lines.append(f"[red]Fehler: {escape(stt.errors[-1])}[/red]")
        st.update("\n".join(lines))

    # ------------------------------------------------------------------ Benchmark
    def _bench_log(self, line: str) -> None:
        self.query_one("#bench-log", RichLog).write(line)

    def _refresh_bench_table(self) -> None:
        t = self.query_one("#bench-table", DataTable)
        t.clear(columns=True)
        t.add_columns("Zeit", "Art", "Test", "Engine", "Quant", "ctx", "KV", "ub", "MTP", "pp t/s", "tg t/s", "Akzept.", "Nutzer", "Σ t/s", "TTFT p50/p95", "Mix-up", "Fehler")
        for r in reversed(benchmod.load_results()[-200:]):
            par = r.kind == "parallel"
            t.add_row(r.when[5:16].replace("T", " "), r.kind, r.name, r.engine, r.quant, str(r.ctx), f"{r.ctk}/{r.ctv}", str(r.ubatch), r.mtp,
                      f"{r.pp_tps:.1f}" if r.pp_tps else "", f"{r.tg_tps:.2f}" if r.tg_tps else "",
                      f"{r.accept:.0%}" if r.accept is not None else "",
                      str(r.users) if par else "", f"{r.agg_tps:.1f}" if par else "",
                      f"{r.ttft_p50:.1f}/{r.ttft_p95:.1f}s" if par else "", (str(r.crosstalk) if par else ""), (r.error or "")[:40])

    def _bench_guard(self) -> bool:
        if self.server.running:
            self.notify("Server läuft – für Benchmarks erst stoppen (Speicher!).", severity="warning")
            return False
        if self._bench_running:
            self.notify("Es läuft bereits ein Benchmark.", severity="warning")
            return False
        cmd = self._current_command()
        if not cmd.ok:
            self.notify("Konfiguration nicht startbar: " + "; ".join(cmd.errors), severity="error")
            return False
        r = cmd.resolved
        est = estimate(self.cfg, r.model, r.mtp, probe(), r.engine.backend if r.engine else "hip", bool(r.engine and r.engine.fast_lazy_ple))
        if est.verdict == "zu groß":
            self.notify(f"Passt nicht in den Speicher (Spielraum {est.headroom / GIB_F:.1f} GiB).", severity="error")
            return False
        self.query_one(TabbedContent).active = "tab-bench"
        return True

    @on(Button.Pressed, "#btn-bench-quick")
    def _bench_quick(self) -> None:
        if self._bench_guard():
            self.run_worker(self._bench_wrap(benchmod.run_llama_bench(self.cfg.copy(), self.inv, self.hw, self._bench_log)), group="bench")

    @on(Button.Pressed, "#btn-bench-depth")
    def _bench_depth(self) -> None:
        if self._bench_guard():
            self.run_worker(self._bench_wrap(benchmod.run_llama_bench(self.cfg.copy(), self.inv, self.hw, self._bench_log, depth=16384)), group="bench")

    @on(Button.Pressed, "#btn-bench-server")
    def _bench_server(self) -> None:
        if self._bench_guard():
            self.run_worker(self._bench_wrap(benchmod.run_server_bench(self.cfg.copy(), self.inv, self.hw, self._bench_log,
                                                                       should_abort=lambda: self._bench_abort)), group="bench")

    @on(Button.Pressed, "#btn-bench-sweep")
    def _bench_sweep(self) -> None:
        if self._bench_guard():
            self.run_worker(self._sweep(), group="bench")

    def _bench_users(self) -> tuple[int, bool]:
        try:
            n = max(1, min(8, int(self.query_one("#bench-users", Input).value or 8)))
        except ValueError:
            n = 8
        return n, self.query_one("#bench-keep-mtp", Switch).value

    @on(Button.Pressed, "#btn-bench-scale")
    def _bench_scale(self) -> None:
        if self._bench_guard():
            n, keep = self._bench_users()
            levels = tuple(x for x in (1, 2, 4, 8) if x <= n) or (n,)
            self.run_worker(self._bench_wrap_many(benchmod.run_parallel_bench(self.cfg.copy(), self.inv, self.hw, self._bench_log, levels=levels,
                                                                              keep_mtp=keep, should_abort=lambda: self._bench_abort)), group="bench")

    @on(Button.Pressed, "#btn-bench-users")
    def _bench_users_once(self) -> None:
        if self._bench_guard():
            n, keep = self._bench_users()
            self.run_worker(self._bench_wrap_many(benchmod.run_parallel_bench(self.cfg.copy(), self.inv, self.hw, self._bench_log, levels=(n,),
                                                                              keep_mtp=keep, should_abort=lambda: self._bench_abort)), group="bench")

    async def _bench_wrap_many(self, coro) -> None:
        self._bench_running, self._bench_abort = True, False
        try:
            results = await coro
            for res in results:
                self._bench_log(f"✔ {res.name}: Σ {res.agg_tps:.1f} t/s · je Nutzer Ø {res.tg_tps:.1f} t/s · TTFT p50 {res.ttft_p50:.1f}s"
                                + (f" · ⚠ {res.crosstalk} Mix-ups" if res.crosstalk else "") + (f" · FEHLER {res.error}" if res.error else ""))
            self._refresh_bench_table()
            bad = [r for r in results if r.error or r.crosstalk]
            self.notify("Mehrnutzer-Benchmark fertig." if not bad else f"Mehrnutzer-Benchmark mit Problemen ({len(bad)} Stufen) – Log prüfen.",
                        severity="information" if not bad else "warning", timeout=10)
        except Exception as e:
            self._bench_log(f"✖ Benchmark abgebrochen: {e}")
        finally:
            self._bench_running = False

    @on(Button.Pressed, "#btn-bench-abort")
    def _bench_abort_btn(self) -> None:
        self._bench_abort = True
        self.notify("Abbruch angefordert (nach dem laufenden Schritt).", severity="warning")

    async def _bench_wrap(self, coro) -> None:
        self._bench_running, self._bench_abort = True, False
        try:
            res = await coro
            self._bench_log(f"✔ {res.kind} {res.name}: pp {res.pp_tps:.1f} t/s · tg {res.tg_tps:.2f} t/s"
                            + (f" · Akzeptanz {res.accept:.0%}" if res.accept is not None else "") + (f" · FEHLER {res.error}" if res.error else ""))
            self._refresh_bench_table()
            self.notify("Benchmark fertig." if not res.error else f"Benchmark-Fehler: {res.error}", severity="information" if not res.error else "error")
        except Exception as e:
            self._bench_log(f"✖ Benchmark abgebrochen: {e}")
        finally:
            self._bench_running = False

    async def _sweep(self) -> None:
        self._bench_running, self._bench_abort = True, False
        results = []
        try:
            cands = benchmod.sweep_candidates(self.cfg)
            self._bench_log(f"── MTP-Sweep: {len(cands)} Kandidaten ──")
            for label, c in cands:
                if self._bench_abort:
                    self._bench_log("Sweep abgebrochen.")
                    break
                self._bench_log(f"▶ {label}")
                res = await benchmod.run_server_bench(c, self.inv, self.hw, self._bench_log, should_abort=lambda: self._bench_abort)
                results.append((label, c, res))
                self._refresh_bench_table()
            good = [x for x in results if not x[2].error and x[2].tg_tps]
            if good:
                best = max(good, key=lambda x: x[2].tg_tps)
                self._bench_log(f"★ Bester: {best[0]} mit tg {best[2].tg_tps:.2f} t/s" + (f", Akzeptanz {best[2].accept:.0%}" if best[2].accept is not None else ""))
                self.cfg.mtp_enabled = best[1].mtp_enabled
                self.cfg.spec_draft_n_max = best[1].spec_draft_n_max
                self.cfg.spec_draft_p_min = best[1].spec_draft_p_min
                self._push_cfg_to_form()
                self.notify(f"Beste MTP-Einstellung übernommen: {best[0]}", timeout=10)
        finally:
            self._bench_running = False

    # ------------------------------------------------------------------ System
    @on(Button.Pressed, "#btn-sys-refresh")
    def _sys_refresh(self) -> None:
        self.hw = probe()
        self._refresh_system()
        self._refresh_side()

    def _refresh_system(self) -> None:
        hw = self.hw
        # eigener Server ist kein "fremder" Prozess
        if self.server.pid:
            hw.other_llm_procs = [p for p in hw.other_llm_procs if p["pid"] != self.server.pid]
            from .hardware import make_tips

            hw.tips = make_tips(hw)
        t = self.query_one("#sys-table", DataTable)
        t.clear(columns=True)
        t.add_columns("Eigenschaft", "Wert")
        rows = [
            ("Host", f"{hw.hostname} ({hw.primary_ip})"),
            ("CPU", f"{hw.cpu_model} – {hw.cores_physical} Kerne / {hw.threads_logical} Threads"),
            ("RAM gesamt / verfügbar", f"{hw.mem_total / GIB_F:.1f} / {hw.mem_available / GIB_F:.1f} GiB (Cache {hw.mem_cached / GIB_F:.1f} GiB)"),
            ("GPU", f"{hw.gpu_name} [{hw.gfx_target}]"),
            ("VRAM (Carve-out) belegt/gesamt", f"{hw.vram_used / GIB_F:.1f} / {hw.vram_total / GIB_F:.1f} GiB"),
            ("GTT belegt/gesamt", f"{hw.gtt_used / GIB_F:.1f} / {hw.gtt_total / GIB_F:.1f} GiB"),
            ("ROCm/HIP", hw.rocm_version or "?"),
            ("Kernel", hw.kernel),
            ("CPU-Governor / EPP", f"{hw.governor} / {hw.epp}"),
            ("tuned / power-profiles / ACPI", f"{hw.tuned_profile or '-'} / {hw.ppd_profile or '-'} / {hw.platform_profile or '-'}"),
            ("GPU DPM-Level", hw.gpu_perf_level),
            ("THP", hw.thp),
            ("Kernel-Cmdline", hw.cmdline[:120]),
        ]
        for k, v in rows:
            t.add_row(k, v)
        tips = []
        for tip in hw.tips:
            mark = {"ok": "[green]✔[/green]", "hinweis": "[yellow]•[/yellow]", "warnung": "[red]![/red]"}[tip.level]
            tips.append(f"{mark} [b]{escape(tip.topic)}[/b]: {escape(tip.text)}")
            if tip.command:
                tips.append(f"    [dim]$ {escape(tip.command)}[/dim]")
        if hw.other_llm_procs:
            tips.append("\n[b]Andere LLM-Prozesse:[/b]")
            for p in hw.other_llm_procs[:6]:
                tips.append(f"  PID {p['pid']:>7}  {p['rss'] / GIB_F:5.1f} GiB  {p['comm']}")
        self.query_one("#sys-tips", Static).update("\n".join(tips))

    # ------------------------------------------------------------------ Hilfe
    def _help_text(self) -> str:
        p = PROJECT_DIR / "docs" / "HILFE.md"
        if p.exists():
            return p.read_text()
        return "# Hilfe\n\nDokumentation fehlt (docs/HILFE.md)."


def probe_fast() -> int:
    """MemAvailable in Bytes (schnell, ohne vollständige Hardware-Abfrage)."""
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) * 1024
    except OSError:
        pass
    return 0
