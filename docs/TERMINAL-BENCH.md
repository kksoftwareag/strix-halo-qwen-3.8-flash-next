# Terminal-Bench-Mini-20: Ergebnisse

Stand: 2026-09-04. Agenten-Benchmark mit 20 Aufgaben aus Terminal-Bench 2.1 auf dieser Maschine, ein Quant nach dem anderen. Aufbau und Bedienung: [`bench/quality/README.md`](../bench/quality/README.md), Einordnung in [`QUALITAETS-BENCHMARKS.md`](QUALITAETS-BENCHMARKS.md).

## Ergebnis

_Noch keine vollständigen Läufe._

## Ausführung

- Benchmark: Terminal-Bench-Local, Terminal-Bench 2.1 (Revision ``), Harbor 0.20.0, Agent Terminus-2
- Ein Versuch je Aufgabe (pass@1), ein Stream (`-np 1`), MTP als Draft-Head aktiv
- Zeitlimit 1800 s je Aufgabe statt der 3 Stunden des Benchmarks; das liegt bei 18 der 20 Aufgaben über dem Limit, das die Aufgabe selbst vorgibt (Ausnahmen: `build-pov-ray` mit 12000 s und `fix-ocaml-gc` mit 3600 s)
- Container je Aufgabe: 1 CPU, 2 GB RAM (nur `overfull-hbox`: 2 CPUs, 4 GB)

## Weitere Läufe

- UD-Q4_K_XL: 1/1 Aufgaben (1:54), Profil `mtp4-ngram-thinking-medium`

Rohdaten: `state/quality/tbench/`, Transkripte und Verifier-Ausgaben unter `bench/quality/terminal-bench-mini/jobs/`. Interaktive Ansicht: [terminal-bench.html](terminal-bench.html).
