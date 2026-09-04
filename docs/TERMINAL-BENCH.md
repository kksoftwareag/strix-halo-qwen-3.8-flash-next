# Terminal-Bench-Mini-20: Ergebnisse

Stand: 2026-09-04. Agenten-Benchmark mit 20 Aufgaben aus Terminal-Bench 2.1 auf dieser Maschine, ein Quant nach dem anderen. Aufbau und Bedienung: [`bench/quality/README.md`](../bench/quality/README.md), Einordnung in [`QUALITAETS-BENCHMARKS.md`](QUALITAETS-BENCHMARKS.md).

## Ergebnis

| Quant | bestanden | Quote | Dauer | Ausgabe-Token | Token/s über die Laufzeit | KLD | Top-1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UD-Q2_K_XL | 16/20 | 80% | 7 h 36 min | 385.970 | 14.1 | 0.2246 | 82.7 % |

## Aufgaben im Einzelnen

| Aufgabe | Kategorie | Schwierigkeit | UD-Q2_K_XL |
| --- | --- | --- | --- |
| `pypi-server` | software-engineering | medium | **ja** (3:53) |
| `nginx-request-logging` | system-administration | medium | **ja** (4:08) |
| `git-leak-recovery` | software-engineering | medium | **ja** (2:55) |
| `fix-git` | software-engineering | easy | **ja** (3:30) |
| `cobol-modernization` | software-engineering | easy | **ja** (9:36) |
| `regex-log` | data-processing | medium | **ja** (23:15) |
| `headless-terminal` | software-engineering | medium | **ja** (17:42) |
| `mailman` | system-administration | medium | **ja** (44:47) |
| `fix-ocaml-gc` | software-engineering | hard | **ja** (41:13) |
| `break-filter-js-from-html` | security | medium | **ja** (57:40) |
| `sqlite-with-gcov` | system-administration | medium | nicht bestanden (8:22) |
| `sparql-university` | data-querying | hard | nicht bestanden (15:21) |
| `llm-inference-batching-scheduler` | machine-learning | hard | **ja** (1:00:30) |
| `configure-git-webserver` | system-administration | hard | nicht bestanden (6:45) |
| `build-cython-ext` | debugging | medium | **ja** (30:07) |
| `extract-elf` | file-operations | medium | **ja** (26:53) |
| `build-pov-ray` | software-engineering | medium | **ja** (1:00:44) |
| `openssl-selfsigned-cert` | security | medium | **ja** (3:48) |
| `overfull-hbox` | debugging | easy | **ja** (21:15) |
| `mteb-retrieve` | data-science | medium | nicht bestanden (13:36) |

## Einordnung

Das Projekt, aus dem der Benchmark stammt, veröffentlicht Läufe anderer Modelle auf vergleichbarer Hardware (Strix Halo, 128 GB): 11 bis 18 von 20 Aufgaben – allerdings mit **zwei** Versuchen je Aufgabe und einem Zeitlimit von drei Stunden. Die Zahlen hier sind mit einem Versuch gemessen und deshalb eher konservativ.

Zwei Dinge dazu, bevor man Quants anhand einzelner Aufgaben vergleicht:

- Bei 20 Aufgaben liegt das 95-%-Intervall um ein Ergebnis bei rund ±11 Prozentpunkten. Ein Unterschied von ein bis zwei Aufgaben zwischen zwei Quants ist Rauschen.
- Gemessen wird mit `temp 1.0`, also nicht deterministisch. In einem verworfenen Vorlauf mit 30-Minuten-Limit war `configure-git-webserver` bestanden, im gewerteten Lauf nicht – bei einem Agenten, der nach sieben Minuten fertig war, lag das nicht am Zeitlimit.

## Durchsatz und Draft-Akzeptanz

| Quant | Anfragen | Prompt-Token | erzeugte Token | Prompt t/s | Decode t/s | MTP-Akzeptanz | mittlere Draft-Länge |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UD-Q2_K_XL | 399 | 404.631 | 385.970 | 243.4 | 24.4 | 0.67 | 3.48 |

Die Werte stammen aus dem Server-Log des jeweiligen Laufs (alle Anfragen des Agenten, nicht nur die Antworten, die in die Wertung eingehen).

## Ausführung

- Benchmark: Terminal-Bench-Local, Terminal-Bench 2.1 (Revision `5c8eadf1f393`), Harbor 0.20.0, Agent Terminus-2
- Ein Versuch je Aufgabe (pass@1), ein Stream (`-np 1`), MTP als Draft-Head aktiv, `reasoning_effort: medium`
- Zeitlimit 3600 s je Aufgabe statt der 3 Stunden, die der Benchmark voreinstellt; bei 19 der 20 Aufgaben liegt das über dem Limit, das die Aufgabe selbst vorgibt
- Container je Aufgabe: 1 CPU, 2 GB RAM (nur `overfull-hbox`: 2 CPUs, 4 GB)
- Engine: llama.cpp 0.3.0-dev (build 1, commit 60bce1a), Backend rocm 7.1.52802, Kontext 163840

### UD-Q2_K_XL

```bash
ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-Q2_K_XL/Qwen3.8-Flash-Next-UD-Q2_K_XL-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{"reasoning_effort": "medium"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4
```

| Posten | Größe |
| --- | --- |
| Gewichte (resident) | 49.2 GiB |
| PLE-Tabelle lazy (nicht resident) | 26.8 GiB |
| KV-Cache (12 Attn-Layer) | 2.0 GiB |
| Indexer-Cache | 0.7 GiB |
| DeltaNet-Zustand | 0.1 GiB |
| Compute-Buffer (Schätzung) | 1.6 GiB |
| MTP-Head + Draft-KV | 3.4 GiB |
| Prompt-Cache (max) | 2.0 GiB |
| Summe | 59.2 GiB |
| Verfügbar (MemAvailable) | 106.5 GiB |
| Reserve OS/Page-Cache | 6.0 GiB |
| Spielraum | 41.4 GiB |

## Weitere Läufe

- UD-Q4_K_XL: 1/1 Aufgaben (1 min), Profil `mtp4-ngram-thinking-medium`

Rohdaten: `state/quality/tbench/`, Transkripte und Verifier-Ausgaben unter `bench/quality/terminal-bench-mini/jobs/`. Interaktive Ansicht: [terminal-bench.html](terminal-bench.html).
