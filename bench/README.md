# bench/ – Messwerkzeuge und Ergebnisse

Alle Läufe hier starten den Server **unter `memguard.py`** (SIGKILL bei < 10 GiB `MemAvailable`), weil GTT-Speicher
nicht im RSS auftaucht und der Kernel-OOM-Killer sonst die ganze Sitzung mitnimmt.

| Skript | Zweck |
| --- | --- |
| `memguard.py --min-avail-gib N -- CMD…` | Wächter + CSV-Mitschrieb (MemAvailable, GTT, VRAM, RSS) |
| `mem_probe.py NAME -- llama serve …` | Server starten, eine Anfrage, hart beenden; JSON mit Load-Zeit, tg/pp, Draft-Akzeptanz, Peak-Verbrauch |
| `mem_sweep*.sh` | Footprint-Sweeps (1–7): Stock-Fork vs EngramHalo, Lade-Modi, Quants, MTP |
| `sweep1-backend.sh` | llama-bench pp512/tg128 (Stock-Fork): KV-Typ, ubatch, Quant |
| `mtp_sweep.py` / `mtp_sweep2.py` | MTP-Feintuning über den Server (n_max, p_min, temp, ngram-mod); `mtp_sweep2.py --engine engramhalo --quant Q4_K_XL --lm none` |

Ergebnisse: `results/raw/*.json` (llama-bench), `results/mem/*.json|csv|log` (Footprints), `results/mtp2/summary.jsonl`
(MTP-Tuning). Auswertung der Kernzahlen in `../docs/RESEARCH.md`, Abschnitt 7.

Wichtig beim Beenden von Probe-Servern: SIGINT löst einen minutenlangen Teardown (GTT-Freigabe) aus – die Skripte
senden deshalb SIGKILL. `pkill -f`-Muster in der eigenen Shell mit Klammer-Trick schreiben (`mem_pro[b]e`), sonst
trifft `pkill` die Shell, die es aufruft.

## Mehrnutzer mit langen Kontexten

`mtp_multiuser.sh` fährt 1/2/4/8/16 gleichzeitige Nutzer mit je ~30 000 Token Prompt und ~5 000 Token Ausgabe,
MTP an. Jeder Nutzer bekommt einen eigenen Fülltext, damit sich der Prompt-Cache nicht teilt. Die Ausgabe zeigt je
Stufe auch die Draft-Akzeptanz — daran zeigt sich der Fehler aus llama.cpp-Issue #27572, bei dem die Akzeptanz mit
mehreren Slots und langen Prompts auf 0,00 fällt.

```bash
bench/mtp_multiuser.sh vorher     # alle vier kleinen Quants, bestehende Builds
engine/fetch.sh && engine/build-engramhalo.sh && engine/build.sh hip
bench/mtp_multiuser.sh nachher    # mit Patch 0003 (PR #27311) und 0004 (Issue #28433)
```

Ohne Argument laufen UD-IQ4_XS, UD-IQ3_XXS, UD-Q2_K_XL und UD-IQ1_M nacheinander; einzelne Quants als weitere
Argumente. Voreinstellung: Stufen 1/2/4/8, 15 000 Token Prompt je Nutzer, 2 000 Token Ausgabe – rund 30 Minuten je
Quant und Durchgang. Über `TB_LEVELS`, `TB_CTX` und `TB_GEN` lässt sich das ändern, etwa
`TB_LEVELS=1,2,4,8,16 TB_CTX=30000 TB_GEN=5000` für die große Variante.

15 000 Token Prompt genügen für den Fehler aus Issue #27572: Er braucht ein Decode über mehrere Ubatches, und das
sind bei `ubatch 2048` schon acht. Mit acht Slots passt auch UD-Q4_K_XL wieder in den Speicher; es ist nur nicht
voreingestellt.

`context_limits.py` sagt vorher, wie viele Slots welcher Größe in den Speicher passen.
