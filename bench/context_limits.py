#!/usr/bin/env python3
"""Parallelitätsgrenzen je Quant: Wie viele gleichzeitige Kontexte welcher Größe passen in den Speicher?

Rechnet mit dem Speichermodell des Programms gegen ein festes Budget (Default: 106,5 GiB, der Wert von
MemAvailable auf der leeren Maschine) – nicht gegen den aktuellen Zustand, damit die Zahlen vergleichbar
bleiben, auch wenn gerade ein Server läuft.

  bench/context_limits.py [--budget-gib 106.5] [--preset eh-agent] [--max-slots 64]
"""
from __future__ import annotations

import argparse

GIB = 2**30
TRAIN = 262144          # Trainingslänge des Modells: mehr Kontext je Slot ist nicht sinnvoll
SIZES = (16384, 32768, 65536, 131072, 262144)
QUANTS = ["UD-IQ1_M", "UD-Q2_K_XL", "UD-IQ3_XXS", "UD-IQ4_XS", "UD-Q4_K_XL"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget-gib", type=float, default=106.5)
    ap.add_argument("--preset", default="eh-agent")
    ap.add_argument("--max-slots", type=int, default=64)
    a = ap.parse_args()

    from qwen38tui.config import build_command
    from qwen38tui.discovery import discover_all
    from qwen38tui.hardware import probe
    from qwen38tui.memory import estimate, kv_bytes_per_token
    from qwen38tui.presets import get_preset

    inv, hw = discover_all(), probe()
    hw.mem_available = int(a.budget_gib * GIB)
    base = get_preset(a.preset).apply()

    def est_of(quant: str, slots: int, ctx_total: int, mtp: bool):
        cfg = base.copy(quant=quant, n_parallel=slots, mtp_enabled=mtp, ctx_size=ctx_total)
        cmd = build_command(cfg, inv, hw)
        r = cmd.resolved
        return estimate(cfg, r.model, r.mtp, hw, "hip", True) if r.model else None

    def max_slots(quant: str, per_slot: int, mtp: bool) -> int:
        best = 0
        for n in range(1, a.max_slots + 1):
            e = est_of(quant, n, per_slot * n, mtp)
            if not e or e.headroom < 0:
                break
            best = n
        return best

    cfg0 = base.copy()
    kv, idx = kv_bytes_per_token(build_command(cfg0, inv, hw).resolved.model, cfg0)
    print(f"KV+Indexer je Token: {kv + idx:.0f} Byte = {(kv + idx) * 32768 / GIB:.2f} GiB je 32k Kontext")
    print(f"Budget: {a.budget_gib:.1f} GiB MemAvailable minus 6 GiB Reserve, Preset {a.preset}\n")
    print(f"{'Quant':12} {'Gewichte':>9} {'256k/1 Slot':>13} | " +
          " ".join(f"{s // 1024:>4}k" for s in SIZES) + "   (mit MTP / ohne MTP)")
    for q in QUANTS:
        e1 = est_of(q, 1, TRAIN, True)
        if not e1:
            print(f"{q:12} nicht vorhanden")
            continue
        cells = [f"{max_slots(q, s, True)}/{max_slots(q, s, False)}" for s in SIZES]
        print(f"{q:12} {e1.weights_resident / GIB:8.1f}G "
              f"{('passt' if e1.headroom >= 0 else 'zu groß'):>13} | " + " ".join(f"{c:>5}" for c in cells))
    print("\nWerte sind bei --max-slots abgeschnitten. Der Kontext je Slot ist durch die Trainingslänge "
          f"({TRAIN}) begrenzt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
