"""Einstiegspunkt: `uv run qwen38` bzw. `python -m qwen38tui`."""
from __future__ import annotations

import argparse
import json
import sys


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="qwen38", description="Qwen3.8-Flash-Next Konfigurations-TUI (llama.cpp, Strix Halo)")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("tui", help="Terminal-UI starten (Standard)")
    p_show = sub.add_parser("show", help="Aktuelle Konfiguration + Kommandozeile ausgeben (ohne TUI)")
    p_show.add_argument("--profile", default="", help="gespeichertes Profil statt state/current.json")
    p_show.add_argument("--preset", default="", help="eingebautes Preset (eh-qualitaet, eh-schnell, eh-longctx, eh-no-thinking, stock-…); Liste: `qwen38 presets`")
    p_run = sub.add_parser("run", help="Server mit aktueller Konfiguration im Vordergrund starten (ohne TUI)")
    p_run.add_argument("--profile", default="")
    p_run.add_argument("--preset", default="")
    p_par = sub.add_parser("bench-parallel", help="Mehrnutzer-Benchmark: N gleichzeitige Anfragen gegen einen Server mit -np N (ohne TUI)")
    p_par.add_argument("--users", type=int, default=8, help="max. gleichzeitige Nutzer (1–8)")
    p_par.add_argument("--levels", default="", help="Stufen, z.B. 1,2,4,8 (Default: 1,2,4,8 bis --users)")
    p_par.add_argument("--max-tokens", type=int, default=256)
    p_par.add_argument("--keep-mtp", action="store_true", help="spekulatives Decoding auch bei mehreren Slots lassen")
    p_par.add_argument("--profile", default="")
    p_par.add_argument("--preset", default="")
    sub.add_parser("presets", help="Eingebaute Presets auflisten")
    sub.add_parser("inventory", help="Gefundene Engines/Modelle/MTP-Heads als JSON")
    sub.add_parser("hw", help="Hardware-/Systemzustand als JSON")
    a = ap.parse_args(argv)

    if a.cmd in (None, "tui"):
        from .app import Qwen38App

        Qwen38App().run()
        return 0

    from .discovery import discover_all
    from .hardware import probe

    if a.cmd == "presets":
        from .presets import PRESETS

        for pr in PRESETS:
            print(f"{pr.key:22} {pr.title}\n{'':22} {pr.description}")
        return 0
    if a.cmd == "inventory":
        inv = discover_all()
        print(json.dumps({"engines": [e.to_dict() for e in inv.engines], "models": [m.to_dict() for m in inv.models],
                          "mtp_heads": [h.to_dict() for h in inv.mtp_heads]}, indent=1, ensure_ascii=False, default=str))
        return 0
    if a.cmd == "hw":
        print(json.dumps(probe().to_dict(), indent=1, ensure_ascii=False, default=str))
        return 0

    from .config import CURRENT_CONFIG, ServerConfig, build_command, load_profile
    from .memory import estimate, fits
    from .presets import get_preset

    if a.preset:
        pr = get_preset(a.preset)
        if not pr:
            print(f"Unbekanntes Preset: {a.preset}", file=sys.stderr)
            return 2
        cfg = pr.apply()
    elif a.profile:
        cfg = load_profile(a.profile)
    elif CURRENT_CONFIG.exists():
        cfg = ServerConfig.load(CURRENT_CONFIG)
    else:
        inv0 = discover_all()
        cfg = get_preset("eh-qualitaet" if inv0.engine("hip-engramhalo") else "stock-ausgewogen").apply()  # type: ignore[union-attr]
    inv, hw = discover_all(), probe()
    cmd = build_command(cfg, inv, hw, fits=lambda m: fits(cfg, m, None, hw))
    if a.cmd == "bench-parallel":
        import asyncio

        from .bench import run_parallel_bench

        n = max(1, min(8, a.users))
        levels = tuple(int(x) for x in a.levels.split(",") if x.strip()) if a.levels else tuple(x for x in (1, 2, 4, 8) if x <= n) or (n,)
        print(f"# Mehrnutzer-Benchmark: Stufen {levels}, max_tokens {a.max_tokens}, MTP {'an' if a.keep_mtp else 'aus'}", file=sys.stderr)
        results = asyncio.run(run_parallel_bench(cfg, inv, hw, lambda l: print(l, file=sys.stderr), levels=levels,
                                                 max_tokens=a.max_tokens, keep_mtp=a.keep_mtp))
        print(f"{'Nutzer':>6} {'Σ t/s':>8} {'je Nutzer':>10} {'min':>6} {'TTFT p50':>9} {'p95':>6} {'Mix-up':>6}  Fehler")
        for r in results:
            ag = r.details.get("aggregate", {})
            print(f"{r.users:>6} {r.agg_tps:8.1f} {r.tg_tps:10.1f} {ag.get('user_tg_min', 0):6.1f} {r.ttft_p50:9.1f} {r.ttft_p95:6.1f} {r.crosstalk:>6}  {r.error}")
        return 0 if all(not r.error and not r.crosstalk for r in results) else 1
    if a.cmd == "show":
        r = cmd.resolved
        est = estimate(cfg, r.model, r.mtp, hw, r.engine.backend if r.engine else "hip", bool(r.engine and r.engine.fast_lazy_ple))
        print("# Engine :", r.engine.label if r.engine else "-")
        print("# Modell :", r.model.quant if r.model else "-", f"({r.model.size_gib:.1f} GiB)" if r.model else "")
        print("# MTP    :", r.mtp.path.name if (cfg.mtp_enabled and r.mtp) else "aus")
        for k, v in est.rows():
            print(f"#   {k:34} {v}")
        print(f"#   Bewertung: {est.verdict}")
        for w in cmd.warnings:
            print("# WARNUNG:", w)
        for e in cmd.errors:
            print("# FEHLER:", e)
        print()
        print(cmd.pretty())
        return 0 if cmd.ok else 1
    if a.cmd == "run":
        import os

        if not cmd.ok:
            print("\n".join("FEHLER: " + e for e in cmd.errors), file=sys.stderr)
            return 1
        r = cmd.resolved
        est = estimate(cfg, r.model, r.mtp, hw, r.engine.backend if r.engine else "hip", bool(r.engine and r.engine.fast_lazy_ple))
        if est.verdict == "zu groß":
            print(f"FEHLER: Konfiguration passt nicht in den Speicher (Spielraum {est.headroom / 2**30:.1f} GiB).", file=sys.stderr)
            return 1
        for w in cmd.warnings:
            print("WARNUNG:", w, file=sys.stderr)
        env = dict(os.environ)
        env.update(cmd.env)
        print("$ " + cmd.shell(), file=sys.stderr)
        os.execvpe(cmd.argv[0], cmd.argv, env)
    return 0


if __name__ == "__main__":
    sys.exit(main())
