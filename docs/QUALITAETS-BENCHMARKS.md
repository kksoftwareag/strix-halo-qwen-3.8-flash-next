# Qualitäts-Benchmarks für den Quant-Vergleich (8-Stunden-Budget)

Stand: 2026-09-04. Bewertung, welche Benchmarks sich auf dieser Maschine (Strix Halo, 128 GB) in einem Budget von
8 Stunden für den Vergleich der Quantisierungen eignen. Die Geschwindigkeitsmessungen stehen in `RESEARCH.md`.

Für Benchmarks, die echte Agentenarbeit im Terminal messen, ist Terminal-Bench-Mini-20 eingebunden; die Bedienung
steht in [`bench/quality/README.md`](../bench/quality/README.md), die Einordnung im Abschnitt
[Agenten-Benchmarks](#agenten-benchmarks-terminal-bench-mini-20).

## Rechengrundlage

| Größe | Wert | Quelle |
| --- | --- | --- |
| Decode, ein Nutzer mit MTP | ca. 35 t/s | eigene Messung |
| Decode, 8 Slots ohne MTP, gesamt | ca. 50 t/s | eigene Messung |
| Prompt-Processing | ca. 400 t/s (kurz), ca. 200 t/s bei >100k Kontext | eigene Messung, Fork-Doku |
| erzeugbare Tokens in 8 Stunden | ca. 1,4 Millionen | 8 × 3600 × 50 |
| Quant-Wechsel (EngramHalo) | ca. 30 s | eigene Messung |
| freier RAM für Docker-Container | ca. 20 GB (Q4_K_XL), ca. 35 GB (IQ4_XS) | Speicherbilanz |

Für alle Läufe: Server mit `-np 8`, MTP aus, `reasoning_effort` low oder Thinking aus. MTP lohnt sich nur bei einem
Nutzer; die meisten Harnesse laufen parallel.

## Kandidaten

| Benchmark | Umfang | Kleinere Variante | Aufwand je Quant (8 Slots) | Eignung für Quant-Vergleich |
| --- | --- | --- | --- | --- |
| KL-Divergenz (`llama perplexity`, Referenz Q4_K_XL) | beliebig | 65k Tokens Wikitext, ctx 8192 | ca. 10 min | sehr gut, misst direkt den Quantisierungsverlust |
| Aider Polyglot | 225 Aufgaben, 2 Versuche | `--languages python` (34) oder `--num-tests 60` | 1 bis 1,5 h mit Thinking low | gut: Code und Edit-Format |
| EvalPlus HumanEval+ | 164 Aufgaben | komplett | ca. 1 h mit Thinking low | gut, günstig |
| IFEval (lm-eval) | 541 Prompts | `--limit 300` | ca. 1 h ohne Thinking | gut für Instruktionstreue |
| GSM8K, MATH-500, GPQA Diamond (lm-eval) | 1319 / 500 / 198 | `--limit 200` | 1 bis 4 h je nach Effort | mittel; Thinking treibt die Tokenzahl |
| AIME 2025 (lm-eval) | 30 Aufgaben | keine | 3 bis 5 h bei xhigh | schlecht: nur 30 Aufgaben |
| SWE-bench Verified Mini (mini-swe-agent) | 50 Instanzen, 5 GB statt 130 GB | `--slice 0:20` | 4 bis 8 h für 50 Instanzen, 8 Worker | nur ein Quant pro Budget, viel Rauschen |
| Terminal-Bench-Mini-20 (Harbor, Terminus-2) | 20 Aufgaben aus TB 2.1 | `--tier smoke`, `--task <id>`, `--attempts 1` | 12 bis 26 h für alle 20 | inhaltlich am besten, aber je Quant über ein Tagesbudget |
| Terminal-Bench 2.1 komplett (Harbor) | 89 Aufgaben | keine sinnvolle | mehrere Tage | ungeeignet |
| DeepSWE (Pier, mini-swe-agent) | 113 Aufgaben, bis 2,5 h je Aufgabe | `--n-tasks 10 --sample-seed 0` | 5 bis 10 h für 10 Aufgaben | ungeeignet: zu wenige Aufgaben je Stunde, Leaderboard nur Frontier-Modelle |

Hinweise zu einzelnen Kandidaten:

- **DeepSWE** ist seit 2026 ein eigener Benchmark von Datacurve (113 Langzeitaufgaben aus aktiven Repos, fünf Sprachen,
  handgeschriebene Verifier), nicht mehr nur das Agentica-Modell. Harness ist Pier (Harbor-kompatibel) mit mini-swe-agent
  als festem Scaffold; kein Schritt- oder Kostenlimit, Zeitlimit 2,5 h je Aufgabe.
- **Terminal-Bench-Mini-20** ist im Repo eingebunden (`bench/quality/`); der eigene Runner startet den Server, setzt
  Endpunkt, Kontextlänge und Identität der Konfiguration und räumt danach auf. Details unten.
- **SWE-bench Verified Mini**: `mini-extra swebench --subset MariusHobbhahn/swe-bench-verified-mini --split test --slice 0:20 -w 8`,
  Modell per Konfiguration `model_name: openai/<name>` mit `api_base`. Bewertung lokal mit dem SWE-bench-Harness oder per
  `sb-cli`. Schrittlimit 250 im Standard, für das Budget auf 60 bis 80 senken.
- **Aider Polyglot**: Aider-Docker, `./benchmark/benchmark.py <name> --model openai/<name> --edit-format diff --threads 8
  --languages python --exercises-dir polyglot-benchmark`, `OPENAI_API_BASE` auf den Server. Auswertung mit `--stats`.
- **lm-eval**: `lm_eval --model local-chat-completions --model_args model=<name>,base_url=http://<host>:8080/v1/chat/completions,num_concurrent=8
  --tasks ifeval --apply_chat_template --limit 300`. Aufgabennamen mit `lm-eval ls tasks` prüfen (u. a. `ifeval`, `gsm8k`,
  `hendrycks_math`, `gpqa`, `aime`, `mmlu_pro`, `humaneval`).
- **KL-Divergenz**: Die Logit-Datei ist etwa 500 KB je Token (Vokabular 248 320). Bei 65k Tokens rund 32 GB, deshalb
  `--chunks 8 -c 8192`. Perplexity mit 32k-Chunks läuft auf dieser Maschine in einen OOM (Logits × Vokabular).

## Agenten-Benchmarks: Terminal-Bench-Mini-20

Für die Frage „arbeitet das Modell als Coding-Agent brauchbar?" taugen Multiple-Choice- und
Einzeldatei-Benchmarks nicht. Terminal-Bench-Mini-20 ist eine 20-Aufgaben-Auswahl aus
Terminal-Bench 2.1, zugeschnitten auf lokale Modelle: Der Agent (Terminus-2) bekommt eine echte
Shell in einem Docker-Container und muss die Aufgabe wirklich lösen; gewertet wird nur, was der
mitgelieferte Verifier akzeptiert (Reward genau 1,0). Der Standard ist pass@2 – der zweite Versuch
läuft nur, wenn der erste scheitert.

Aufgabenmischung: 7 Software-Entwicklung, 4 Systemadministration, 9 aus Debugging, Sicherheit,
Datenabfrage, ML-Systeme und Dateiformaten; nach Metadaten 3 leicht, 13 mittel, 4 schwer.
Beispiele: ein Python-Paket bauen und über einen lokalen PyPI-Server installierbar machen, ein Leck
aus der Git-Historie entfernen, einen Absturz im Garbage Collector von OCaml in C debuggen,
POV-Ray 2.2 von 1990 auf einem heutigen System kompilieren, Postfix und Mailman zu einer
funktionierenden Mailingliste verdrahten.

### Einbindung in dieses Repo

```bash
bench/quality/fetch.sh                                   # Benchmark holen, Voraussetzungen prüfen
uv run python bench/quality/tbench.py --tier smoke --attempts 1   # Rauchtest, eine Aufgabe
uv run python bench/quality/tbench.py --tier full                 # alle 20 Aufgaben
uv run python bench/quality/tbench.py --tier full --quant UD-IQ4_XS
```

`tbench.py` startet den Server mit dem Preset `eh-agent` (UD-Q4_K_XL, 163840 Kontext, ein Slot,
MTP + n-Gramm, kleiner Prompt-Cache), wartet auf `/health`, übergibt Endpunkt, Kontextlänge und die
Identität des Laufs an den Runner und stoppt den Server danach. Der Server läuft unter
`bench/memguard.py`. Bedienung im Detail: [`bench/quality/README.md`](../bench/quality/README.md).

### Ergebnisse auf dieser Maschine

Die eigenen Läufe stehen in [`TERMINAL-BENCH.md`](TERMINAL-BENCH.md), interaktiv in [terminal-bench.html](terminal-bench.html).

### Zeitbedarf

Das Projekt veröffentlicht Läufe auf vergleichbarer Hardware (Strix Halo, 128 GB). Sie zeigen, was
20 Agentenaufgaben mit einem lokalen Modell kosten:

| Modell | Quant | Engine/Backend | pass@1 | pass@2 | Dauer |
| --- | --- | --- | --- | --- | --- |
| DeepSeek-V4-Flash-0731 | UD-IQ3_XXS | llama.cpp/vulkan | 18/20 | 18/20 | 12 h |
| DeepSeek-V4-Flash-0731 | IQ2XXS gemischt | DwarfStar/rocm | 17/20 | 19/20 | 18 h |
| Qwen3.8-27B | UD-Q4_K_XL | llama.cpp/rocm | 16/20 | 19/20 | 15 h |
| Qwen3.8-27B | Q4_0_ROCMI4 | llama.cpp/rocm | 16/20 | 17/20 | 17 h |
| DeepSeek-V4-Flash-0731 | MXFP4 | DwarfStar/rocm | 15/20 | 19/20 | 23 h |
| Qwen3.6-27B | UD-Q8_K_XL | llama.cpp/rocm | 12/20 | 14/20 | 26 h |
| Qwen3.6-35B-A3B | UD-Q4_K_XL | llama.cpp/rocm | 11/20 | 11/20 | 15 h |

Ein vollständiger Lauf kostet also einen Tag je Quantisierung – ein Quant-Vergleich über drei
Varianten sind drei Tage, nicht acht Stunden. Was ins 8-Stunden-Budget passt:

| Variante | Umfang | Dauer | Aussage |
| --- | --- | --- | --- |
| ein Quant, `--tier full --attempts 1` | 20 Aufgaben, ein Versuch, Timeout 25 min | 6 bis 9 h | pass@1 für eine Konfiguration |
| Teilmenge je Quant | 8 kurze Aufgaben, `--tasks`, `--attempts 1` | 2 bis 3 h je Quant | grober Vergleich dreier Quants |
| `--concurrency 4` mit UD-IQ4_XS | 20 Aufgaben parallel in 4 Slots | 8 bis 12 h | pass@1, etwa 30 % schneller |

Bei mehreren Slots teilt sich der Kontext: `--concurrency 4` bei 262144 Gesamtkontext heißt 65536
Token je Aufgabe, und der Durchsatz je Aufgabe sinkt (gemessen: 1/2/4/8 Slots = 20,4/32,0/42,4/50,4
Token/s gesamt). Vier Slots sind der beste Kompromiss; acht Slots lassen zu wenig Kontext je Agent.

### Aussagekraft

20 Aufgaben sind eine kleine Stichprobe: Ein Ergebnis von 12/20 hat ein 95-%-Intervall von etwa
±11 Prozentpunkten, bei 8 Aufgaben sind es ±17. Unterschiede von ein bis zwei gelösten Aufgaben
zwischen zwei Quants sind Rauschen. Der Benchmark beantwortet zuverlässig „läuft das Modell als
Agent überhaupt rund?" (Werkzeugaufrufe, lange Sitzungen, Zusammenfassen bei vollem Kontext) und
zeigt große Qualitätssprünge; für feine Quant-Unterschiede bleibt die KL-Divergenz das schärfere
Werkzeug.

### Besonderheit in diesem Netz

`archive.ubuntu.com` antwortet aus diesem LAN über IPv4 nur sehr langsam (rund 20 s je Anfrage,
IPv6 gar nicht). Terminus-2 installiert zu Beginn jeder Aufgabe `tmux` und `asciinema` im Container
und läuft dabei in Harbors 120-Sekunden-Grenze – jede Aufgabe scheitert dann mit
`RuntimeError: Command timed out after 120 seconds`. `tbench.py` prüft das beim Start und legt
`archive.ubuntu.com` und `security.ubuntu.com` per `extra_hosts` auf einen schnellen Spiegel
(Standard `ftp.fau.de`); damit dauert `apt-get update` 1 s statt über 120 s. Abschalten mit
`--apt-mirror off`, anderer Spiegel mit `--apt-mirror <host>`. Umgesetzt ist das über eine
Docker-Zwischenschicht (`bench/quality/dockershim/docker`), die nur eine Compose-Overlay-Datei
anhängt; der Benchmark selbst und die Aufgabenbilder bleiben unverändert.

### SWE-bench Verified Mini als Alternative

Wenn es um Patches in echten Repositories statt um Terminalarbeit geht, ist SWE-bench Verified Mini
(50 Instanzen, 5 GB Images statt 130 GB) der kleinere Kandidat. Harness ist mini-swe-agent:

```bash
mini-extra swebench --subset MariusHobbhahn/swe-bench-verified-mini --split test \
  --slice 0:20 -w 4 --model openai/qwen3.8-flash
```

Modell über `~/.config/mini-swe-agent/mini.yaml` mit `api_base` auf den lokalen Server. Der
Schrittzähler steht standardmäßig auf 250; für ein Zeitbudget auf 60 bis 80 senken. Eine Instanz
kostet 10 bis 25 Minuten, 20 Instanzen also 2 bis 4 Stunden bei vier Workern.

## Empfohlener Plan für drei Quants (Q4_K_XL, IQ4_XS, IQ3_XXS)

| Schritt | Umfang | Dauer | Ergebnis |
| --- | --- | --- | --- |
| 1. KL-Divergenz, alle vier Quants | 65k Tokens, Referenz Q4_K_XL | ca. 30 min | Mean KLD, Δp-Perzentile, Same-top-p je Quant |
| 2. Aider Polyglot, Python | 34 Aufgaben × 2 Versuche, 8 Threads, Thinking low | ca. 3,5 h | Pass-Rate, Edit-Fehler je Quant |
| 3. HumanEval+ oder IFEval | 164 bzw. 300 Prompts, 8 Slots | ca. 3 h | Pass-Rate bzw. Instruktionstreue je Quant |

Summe rund 7 Stunden inklusive Ladezeiten.

Einordnung: Bei 34 bis 164 Aufgaben liegt die Streuung bei 5 bis 8 Prozentpunkten. Der Unterschied zwischen Q4_K_XL
(KLD 0,047) und IQ4_XS (0,084) wird in den Aufgaben-Benchmarks vermutlich nicht sichtbar; Q2_K_XL (0,225) fällt meist
erkennbar ab. Die KL-Divergenz ist deshalb der Pflichtteil, die Aufgaben-Benchmarks zeigen, ob sich ein Verlust praktisch
auswirkt.

Terminal-Bench und SWE-bench Mini lohnen sich als einmaliger Lauf mit dem Standard-Quant außerhalb des 8-Stunden-Budgets,
um zu prüfen, ob das Modell mit Terminus-2 beziehungsweise mini-swe-agent zuverlässig arbeitet.

## Beispielkommandos

```bash
# Server für Benchmarks (8 Slots, ohne MTP, Thinking low)
./run.sh run --preset eh-qualitaet    # im TUI: Slots (-np) = 8, MTP aus, reasoning_effort low

# KL-Divergenz: Referenz-Logits mit Q4_K_XL, dann Vergleich
engine/build-engramhalo/bin/llama perplexity -m <Q4_K_XL> -f wiki.test.raw -c 8192 --chunks 8 -ngl 99 -lm none \
  --save-all-logits state/bench/q4kxl.kld
engine/build-engramhalo/bin/llama perplexity -m <IQ4_XS> -f wiki.test.raw -c 8192 --chunks 8 -ngl 99 -lm none \
  --kl-divergence-base state/bench/q4kxl.kld --kl-divergence
```

## Quellen

- https://github.com/kyuz0/terminal-bench-mini und https://kyuz0.github.io/terminal-bench-mini/
- https://github.com/harbor-framework/terminal-bench-2-1
- https://huggingface.co/datasets/harborframework/terminal-bench-2.0
- https://www.harborframework.com/docs/tutorials/running-terminal-bench
- https://github.com/harbor-framework/terminal-bench-2
- https://www.harborframework.com/docs/agents
- https://mini-swe-agent.com/latest/usage/swebench/
- https://mini-swe-agent.com/latest/models/local_models/
- https://huggingface.co/datasets/MariusHobbhahn/swe-bench-verified-mini
- https://arxiv.org/abs/2607.07946 (DeepSWE) und https://github.com/datacurve-ai/deep-swe
- https://github.com/Aider-AI/aider/blob/main/benchmark/README.md und https://github.com/Aider-AI/polyglot-benchmark
- https://github.com/EleutherAI/lm-evaluation-harness
- https://github.com/ggml-org/llama.cpp/blob/master/tools/perplexity/README.md
