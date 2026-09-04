# Agenten-Benchmarks (echte Coding-Arbeit)

Hier liegt die Anbindung an **Terminal-Bench-Mini-20** – 20 Aufgaben aus Terminal-Bench 2.1,
ausgewählt für lokale Modelle: Pakete bauen, Dienste konfigurieren, Git-Historie reparieren,
C- und OCaml-Fehler suchen, LaTeX und SPARQL geradeziehen. Der Agent (Terminus-2) arbeitet in
einem Docker-Container mit einer echten Shell; gewertet wird nur, was der Verifier der Aufgabe
am Ende akzeptiert (Reward genau 1,0).

Der Benchmark selbst kommt aus <https://github.com/kyuz0/terminal-bench-mini> (Apache-2.0) und
wird nicht mitversioniert, sondern geholt:

```bash
bench/quality/fetch.sh          # klont den Benchmark und prüft docker, uv, Speicher, Platz
```

## Alle Quants nacheinander

```bash
bench/quality/run-quants.sh                       # UD-Q2_K_XL, UD-IQ1_M, UD-IQ3_XXS, UD-IQ4_XS
bench/quality/run-quants.sh UD-IQ4_XS             # nur einer
TB_AGENT_TIMEOUT=1800 bench/quality/run-quants.sh # Zeitlimit je Aufgabe (Default 3600 s)
TB_EFFORT=xhigh bench/quality/run-quants.sh       # Denkstufe (Default medium)
```

Die Denkstufe steckt im Profilnamen (`mtp4-ngram-thinking-medium`) und damit in der Kennung jedes Laufs;
Läufe mit unterschiedlicher Stufe landen in getrennten Ergebnisordnern und stehen auf der Website
nebeneinander.

Das Skript wartet zwischen den Quants, bis der Speicher wieder frei ist, schreibt je Quant ein Log nach
`state/quality/tbmini-<quant>.log` und setzt den apt-Spiegel fest (siehe unten). Danach die Auswertung:

```bash
uv run python bench/quality/report.py             # schreibt docs/TERMINAL-BENCH.md und docs/tbmini-data.js
```

## Lauf starten

`tbench.py` startet den Server mit einer Konfiguration aus dem TUI, wartet auf `/health`, ruft den
Runner auf und stoppt den Server danach wieder. Der Server läuft unter `bench/memguard.py`.

```bash
# Rauchtest: eine Aufgabe, ein Versuch (ca. 15-40 min)
uv run python bench/quality/tbench.py --tier smoke --attempts 1 --agent-timeout 3600

# voller Lauf: 20 Aufgaben, bis zu 2 Versuche je Aufgabe
uv run python bench/quality/tbench.py --tier full

# anderer Quant, dieselbe Konfiguration
uv run python bench/quality/tbench.py --tier full --quant UD-IQ4_XS

# einzelne Aufgabe
uv run python bench/quality/tbench.py --task fix-git --attempts 1
```

Wichtige Schalter:

| Schalter | Bedeutung |
| --- | --- |
| `--preset` | Server-Preset, Default `eh-agent` (Q4_K_XL, 160k Kontext, ein Slot, MTP+ngram) |
| `--quant`, `--ctx`, `--no-mtp`, `--reasoning-effort` | einzelne Werte überschreiben |
| `--concurrency N` | N Aufgaben gleichzeitig; setzt auch `-np N` (Kontext teilt sich auf die Slots) |
| `--slots N` | Slots getrennt von der Parallelität setzen |
| `--attempts` | Versuche je Aufgabe (Default 2 = pass@2, `1` = pass@1) |
| `--agent-timeout` | Sekunden je Versuch (Default 10800) |
| `--min-avail-gib` | Schwelle des Speicher-Wächters (Default aus dem Preset: 5 GiB) |
| `--use-running` | keinen Server starten, laufenden benutzen |
| `--dry-run` | nur Speicherbilanz und Kommandos zeigen |

Alles nach `--` geht unverändert an `terminal_bench.py`.

## Container-Images

Die 20 Aufgaben bringen je ein eigenes Docker-Image mit (zusammen einige GB). Beim ersten Lauf lädt Harbor
sie einzeln nach; ein Image kann mehrere Minuten brauchen, und der Lauf wartet dabei. Schneller ist es, sie
vorher parallel zu holen:

```bash
python3 -c '
import tomllib, pathlib
for d in sorted(pathlib.Path("bench/quality/terminal-bench-mini/tasks").iterdir()):
    f = d / "task.toml"
    if f.is_file():
        print(tomllib.loads(f.read_text())["environment"]["docker_image"])
' | xargs -P 3 -I{} docker pull -q {}
```

Ab dem zweiten Quant liegen die Images im Cache; nur der erste Durchlauf zahlt die Ladezeit.

## Speicher

Der Agent läuft im Container, das Modell im selben RAM. Die Bilanz steht am Anfang jeder Ausgabe:

| Quant | Footprint (160k Kontext, 1 Slot) | frei für Container |
| --- | --- | --- |
| UD-Q4_K_XL | 92,3 GiB | ca. 8 GiB |
| UD-IQ4_XS | 72,9 GiB | ca. 28 GiB |
| UD-IQ3_XXS | 62,0 GiB | ca. 38 GiB |

Aufgaben wie `build-pov-ray`, `sqlite-with-gcov` oder `mteb-retrieve` kompilieren oder laden
Modelle im Container. Mit Q4_K_XL ist das knapp; für `--concurrency > 1` ist IQ4_XS die
vernünftige Wahl. Fällt `MemAvailable` unter die Schwelle, killt der Wächter den Server –
der Lauf bricht dann ab, aber die Maschine bleibt bedienbar.

## Netzwerk: apt-Spiegel

`archive.ubuntu.com` ist aus manchen Netzen unbrauchbar langsam (hier zeitweise 20 s je Anfrage). Terminus-2
installiert zu Beginn jeder Aufgabe `tmux` und `asciinema` im Container und läuft dann in Harbors
120-Sekunden-Grenze; jede Aufgabe scheitert mit `RuntimeError: Command timed out after 120 seconds`.
`tbench.py --apt-mirror` legt `archive.ubuntu.com` und `security.ubuntu.com` per `extra_hosts` auf einen
schnellen Spiegel (`auto` misst vorher, `off` schaltet ab, sonst ein Hostname). Umgesetzt über
`bench/quality/dockershim/docker`, das jedem `docker compose`-Aufruf eine Overlay-Datei anhängt – der
Benchmark und die Aufgabenbilder bleiben unverändert.

## Ergebnisse

* Fortschritt und Zusammenfassung: `state/quality/*.log`
* Normalisierte Ergebnisse je Aufgabe: `state/quality/tbench/<platform>/<modell>_results/`
* Roh-Jobs von Harbor (Transkripte, Verifier-Ausgaben): `bench/quality/terminal-bench-mini/jobs/`
* Server-Log und Speicherverlauf: `state/logs/tbench-server-*.log`, `state/logs/tbench-mem-*.csv`
* Aufbereitet: `docs/TERMINAL-BENCH.md` und die interaktive Seite `docs/terminal-bench.html`
* Versioniert im Repo: `bench/quality/results/` (Zusammenfassung und Ergebnis je Aufgabe; die großen
  Transkripte bleiben unter `state/`)

Einen unterbrochenen Lauf fortsetzen oder Fehlschläge wiederholen (Server muss laufen,
z. B. über das TUI, dann `--use-running`):

```bash
cd bench/quality/terminal-bench-mini
python3 terminal_bench.py resume jobs/<job-name>
python3 terminal_bench.py retry-failed <ergebnisordner>
```

## Zeitbedarf

Die Referenzläufe des Projekts auf vergleichbarer Hardware (Strix Halo, llama.cpp, ROCm)
brauchen für die vollen 20 Aufgaben **12 bis 26 Stunden**. Das passt nicht in ein
8-Stunden-Fenster; Einordnung und Alternativen stehen in `docs/QUALITAETS-BENCHMARKS.md`.
