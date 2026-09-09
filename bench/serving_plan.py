#!/usr/bin/env python3
"""Auslegung eines Mehrnutzer-Servers: maximaler Kontext je Nutzer bei vorgegebenem Spielraum.

Beantwortet die Frage „wie viele Nutzer mit wie viel Kontext?“ gegen das Speichermodell des
Programms – inklusive der Context-Checkpoints, die bei diesem Modell je Stück ungefähr so groß sind
wie der DeltaNet-Zustand (gemessen 112.6 MiB ohne MTP, 126.1 MiB mit MTP) und die bei tiefem Kontext
so viel kosten können wie der KV-Cache selbst.

  bench/serving_plan.py --quant UD-IQ3_XXS --headroom 6 --checkpoints 4
  bench/serving_plan.py --slots 8 --command      # zeigt zusätzlich die fertige Kommandozeile

Der Mindestabstand der Checkpoints wird so gesetzt, dass genau --checkpoints Stück je Slot entstehen.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

GIB = 2**30
TRAIN = 262144
SCHRITT = 1024


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quant", default="UD-IQ3_XXS")
    ap.add_argument("--preset", default="eh-agent")
    ap.add_argument("--headroom", type=float, default=6.0, help="gewünschter Spielraum in GiB")
    ap.add_argument("--budget-gib", type=float, default=106.5)
    ap.add_argument("--checkpoints", type=int, default=4, help="--ctx-checkpoints je Slot")
    ap.add_argument("--cache-ram", type=int, default=4096, help="--cache-ram in MiB")
    ap.add_argument("--no-mtp", action="store_true")
    ap.add_argument("--kv-unified", default="on", choices=("auto", "on", "off"))
    ap.add_argument("--slots", type=int, default=0, help="nur diese Nutzerzahl rechnen")
    ap.add_argument("--command", action="store_true", help="Kommandozeile für --slots ausgeben")
    a = ap.parse_args()

    from qwen38tui.config import build_command
    from qwen38tui.discovery import discover_all
    from qwen38tui.hardware import probe
    from qwen38tui.memory import estimate
    from qwen38tui.presets import get_preset

    inv, hw = discover_all(), probe()
    hw.mem_available = int(a.budget_gib * GIB)
    basis = get_preset(a.preset).apply()

    def bauen(slots: int, je_slot: int):
        cfg = basis.copy(
            quant=a.quant, n_parallel=slots, ctx_size=je_slot * slots,
            mtp_enabled=not a.no_mtp, kv_unified=a.kv_unified,
            kv_unified_per_slot=min(je_slot * slots, TRAIN) if a.kv_unified == "on" else 0,
            n_ctx_checkpoints=a.checkpoints, cache_ram_mib=a.cache_ram,
            checkpoint_min_step=max(1024, je_slot // max(1, a.checkpoints)),
        )
        cmd = build_command(cfg, inv, hw)
        r = cmd.resolved
        return cfg, cmd, estimate(cfg, r.model, r.mtp, hw, "hip", True)

    def maximum(slots: int) -> tuple[int, float]:
        lo, hi = SCHRITT, TRAIN
        _, _, e = bauen(slots, lo)
        if e.headroom / GIB < a.headroom:
            return 0, 0.0
        while lo < hi:
            mitte = min(hi, (lo + hi + SCHRITT) // (2 * SCHRITT) * SCHRITT)
            if mitte <= lo:
                break
            _, _, e = bauen(slots, mitte)
            if e.headroom / GIB >= a.headroom:
                lo = mitte
            else:
                hi = mitte - SCHRITT
        _, _, e = bauen(slots, lo)
        return lo, e.headroom / GIB

    kopf = (f"{a.quant}, MTP {'aus' if a.no_mtp else 'an'}, KV-Pool "
            f"{'gemeinsam' if a.kv_unified == 'on' else 'geteilt'}, "
            f"--ctx-checkpoints {a.checkpoints}, --cache-ram {a.cache_ram} MiB, "
            f"Ziel-Spielraum {a.headroom:.0f} GiB")
    print(kopf)
    print("-" * len(kopf))
    liste = [a.slots] if a.slots else [1, 2, 4, 6, 8, 12, 16, 24, 32]
    allein = "allein max" if a.kv_unified == "on" else ""
    print(f"{'Nutzer':>6} {'garantiert':>11} {allein:>11} {'Summe Token':>12} {'KV':>8} "
          f"{'Checkpoints':>12} {'Spielraum':>10}")
    for n in liste:
        je, rest = maximum(n)
        if not je:
            print(f"{n:>6} {'passt nicht':>11}")
            continue
        cfg, cmd, e = bauen(n, je)
        # Im gemeinsamen Pool darf eine einzelne Sitzung so weit wachsen, wie Pool und Trainingslänge
        # es zulassen, solange die anderen Slots leer sind.
        solo = f"{min(je * n, TRAIN) / 1024:>10.0f}k" if a.kv_unified == "on" else ""
        print(f"{n:>6} {je / 1024:>10.0f}k {solo:>11} {je * n / 1024:>11.0f}k "
              f"{(e.kv_cache + e.indexer_cache) / GIB:>7.1f}G {e.checkpoints / GIB:>11.1f}G "
              f"{rest:>9.1f}G")
        if a.command and a.slots:
            print("\nKommandozeile:\n")
            print("  " + " \\\n    ".join(cmd.argv))
            for w in cmd.warnings:
                print(f"\n  Hinweis: {w}")
    if not a.slots:
        print("\nBis etwa acht Nutzern tauschen sich Nutzerzahl und Kontext eins zu eins – der Token-Vorrat "
              "ist fest.\nDarüber schrumpft er, weil DeltaNet-Zustand und Checkpoints an der Slot-Zahl hängen "
              "und nicht am Kontext.\n'garantiert' ist der Anteil, wenn alle Slots gleichzeitig voll sind; "
              "im gemeinsamen Pool darf eine\neinzelne Sitzung bis 'allein max' wachsen, solange die anderen "
              "leer sind.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
