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
