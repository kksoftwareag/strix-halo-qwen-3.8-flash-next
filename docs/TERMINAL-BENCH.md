# Terminal-Bench-Mini-20: Ergebnisse

Stand: 2026-09-06. Agenten-Benchmark mit 20 Aufgaben aus Terminal-Bench 2.1 auf dieser Maschine, ein Quant nach dem anderen. Aufbau und Bedienung: [`bench/quality/README.md`](../bench/quality/README.md), Einordnung in [`QUALITAETS-BENCHMARKS.md`](QUALITAETS-BENCHMARKS.md).

## Ergebnis

| Quant | pass@1 | pass@2 | pass@3 | Dauer | Ø je Aufgabe | Median | Ausgabe-Token | Token/s über die Laufzeit | KLD | Top-1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UD-IQ1_M · medium | 15/20 | **19/20** | **20/20** | 8 h 16 min | 24:49 | 20:50 | 459.008 | 15.4 | 0.3147 | 79.7 % |
| UD-Q2_K_XL · medium | 16/20 | **18/20** | 18/20 | 7 h 36 min | 22:48 | 17:42 | 385.970 | 14.1 | 0.2246 | 82.7 % |
| UD-IQ3_XXS · medium | 15/20 | **18/20** | 18/20 | 6 h 27 min | 19:22 | 16:32 | 273.296 | 11.8 | 0.1651 | 85.4 % |
| UD-IQ4_XS · medium | 15/20 | **18/20** | 18/20 | 6 h 57 min | 20:53 | 12:37 | 343.555 | 13.7 | 0.0836 | 89.6 % |

pass@2: Jede im ersten Durchgang gescheiterte Aufgabe bekam genau einen zweiten Versuch, mit 5400 s Zeitlimit statt 3600 s.
pass@3 zählt einen dritten Versuch mit 10800 s, der nur für die Aufgaben lief, die auch im zweiten Anlauf am Zeitlimit scheiterten.

„Ø je Aufgabe“ und „Median“ beziehen sich auf den ersten Durchgang und zählen die volle Zeit je Aufgabe: Container-Aufbau, Arbeit des Agenten und Verifier.

## Aufgaben im Einzelnen

| Aufgabe | Kategorie | Schwierigkeit | UD-IQ1_M · medium | UD-Q2_K_XL · medium | UD-IQ3_XXS · medium | UD-IQ4_XS · medium |
| --- | --- | --- | --- | --- | --- | --- |
| `pypi-server` | software-engineering | medium | **ja** (3:08) | **ja** (3:53) | **ja** (3:42) | **ja** (10:09) |
| `nginx-request-logging` | system-administration | medium | **ja** (2:32) | **ja** (4:08) | **ja** (2:53) | **ja** (3:18) |
| `git-leak-recovery` | software-engineering | medium | **ja** (2:25) | **ja** (2:55) | **ja** (2:29) | **ja** (8:52) |
| `fix-git` | software-engineering | easy | **ja** (4:31) | **ja** (3:30) | **ja** (3:21) | **ja** (2:57) |
| `cobol-modernization` | software-engineering | easy | **ja** (16:30) | **ja** (9:36) | **ja** (16:32) | **ja** (13:31) |
| `regex-log` | data-processing | medium | Zeitlimit (1:00:47) → **ja** (1:12:50) | **ja** (23:15) | **ja** (24:26) | **ja** (11:40) |
| `headless-terminal` | software-engineering | medium | **ja** (9:48) | **ja** (17:42) | **ja** (6:50) | **ja** (8:39) |
| `mailman` | system-administration | medium | **ja** (46:45) | **ja** (44:47) | **ja** (24:55) | **ja** (21:38) |
| `fix-ocaml-gc` | software-engineering | hard | **ja** (38:27) | **ja** (41:13) | **ja** (32:03) | **ja** (1:22:10) |
| `break-filter-js-from-html` | security | medium | **ja** (20:50) | **ja** (57:40) | **ja** (35:20) | **ja** (20:35) |
| `sqlite-with-gcov` | system-administration | medium | **ja** (5:34) | nicht bestanden (8:22) → **ja** (6:49) | **ja** (6:45) | **ja** (8:14) |
| `sparql-university` | data-querying | hard | **ja** (34:10) | nicht bestanden (15:21) → **ja** (11:45) | **ja** (17:45) | **ja** (12:37) |
| `llm-inference-batching-scheduler` | machine-learning | hard | Zeitlimit (1:00:30) → Zeitlimit (1:30:35) → **ja** (2:46:33) | **ja** (1:00:30) | Zeitlimit (1:00:38) → **ja** (34:04) | Zeitlimit (1:03:22) → **ja** (1:30:13) |
| `configure-git-webserver` | system-administration | hard | **ja** (10:50) | nicht bestanden (6:45) → nicht bestanden (3:59) | nicht bestanden (6:20) → **ja** (5:12) | **ja** (5:48) |
| `build-cython-ext` | debugging | medium | **ja** (35:11) | **ja** (30:07) | **ja** (33:24) | **ja** (28:09) |
| `extract-elf` | file-operations | medium | Zeitlimit (1:00:29) → **ja** (32:36) | **ja** (26:53) | nicht bestanden (9:28) → nicht bestanden (22:52) | nicht bestanden (17:32) → **ja** (51:04) |
| `build-pov-ray` | software-engineering | medium | nicht bestanden (42:18) → **ja** (42:01) | **ja** (1:00:44) | Zeitlimit (1:00:46) → **ja** (37:32) | Zeitlimit (1:00:48) → nicht bestanden (58:11) |
| `openssl-selfsigned-cert` | security | medium | **ja** (3:09) | **ja** (3:48) | **ja** (2:28) | **ja** (6:24) |
| `overfull-hbox` | debugging | easy | **ja** (21:26) | **ja** (21:15) | **ja** (15:58) | nicht bestanden (19:53) → **ja** (38:56) |
| `mteb-retrieve` | data-science | medium | nicht bestanden (16:59) → **ja** (15:02) | nicht bestanden (13:36) → nicht bestanden (12:06) | nicht bestanden (21:15) → nicht bestanden (9:35) | nicht bestanden (11:26) → nicht bestanden (7:57) |

## Einordnung

Das Projekt, aus dem der Benchmark stammt, veröffentlicht Läufe anderer Modelle auf vergleichbarer Hardware (Strix Halo, 128 GB): 11 bis 18 von 20 Aufgaben – allerdings mit **zwei** Versuchen je Aufgabe und einem Zeitlimit von drei Stunden. Die Zahlen hier sind mit einem Versuch gemessen und deshalb eher konservativ.

Zwei Dinge dazu, bevor man Quants anhand einzelner Aufgaben vergleicht:

- Bei 20 Aufgaben liegt das 95-%-Intervall um ein Ergebnis bei rund ±11 Prozentpunkten. Ein Unterschied von ein bis zwei Aufgaben zwischen zwei Quants ist Rauschen.
- Gemessen wird mit `temp 1.0`, also nicht deterministisch. In einem verworfenen Vorlauf mit 30-Minuten-Limit war `configure-git-webserver` bestanden, im gewerteten Lauf nicht – bei einem Agenten, der nach sieben Minuten fertig war, lag das nicht am Zeitlimit.

## Durchsatz und Draft-Akzeptanz

| Quant | Anfragen | Prompt-Token | erzeugte Token | Prompt t/s | Decode t/s | MTP-Akzeptanz | mittlere Draft-Länge |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UD-IQ1_M · medium | 361 | 332.812 | 459.008 | 216.6 | 26.0 | 0.683 | 3.52 |
| UD-Q2_K_XL · medium | 399 | 404.631 | 385.970 | 243.4 | 24.4 | 0.67 | 3.48 |
| UD-IQ3_XXS · medium | 287 | 301.122 | 273.296 | 252.7 | 25.1 | 0.681 | 3.6 |
| UD-IQ4_XS · medium | 294 | 339.204 | 343.555 | 263.9 | 23.9 | 0.678 | 3.63 |

Die Werte stammen aus dem Server-Log des jeweiligen Laufs (alle Anfragen des Agenten, nicht nur die Antworten, die in die Wertung eingehen). `Decode t/s` ist die reine Erzeugungsrate, gemittelt über alle Anfragen.

### Tempo je Aufgabe

Ausgabe-Token geteilt durch die Zeit, die der Agent tatsächlich auf das Modell gewartet hat (Summe aller Antwortzeiten). Der Wert liegt unter der reinen Decode-Rate, weil jede Anfrage auch den Prompt verarbeitet; er sagt, wie schnell der Agent bei dieser Aufgabe vorankam.

| Aufgabe | UD-IQ1_M · medium t/s | UD-Q2_K_XL · medium t/s | UD-IQ3_XXS · medium t/s | UD-IQ4_XS · medium t/s | UD-IQ1_M · medium Modellzeit | UD-Q2_K_XL · medium Modellzeit | UD-IQ3_XXS · medium Modellzeit | UD-IQ4_XS · medium Modellzeit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pypi-server` | 25,2 | 25,6 | 23,9 | 25,0 | 1:40 | 1:55 | 2:03 | 2:28 |
| `nginx-request-logging` | 29,2 | 25,6 | 27,3 | 26,5 | 1:23 | 2:54 | 1:44 | 1:55 |
| `git-leak-recovery` | 25,4 | 23,6 | 23,6 | 25,6 | 1:40 | 2:06 | 1:43 | 1:42 |
| `fix-git` | 23,1 | 22,6 | 23,9 | 24,4 | 3:49 | 2:48 | 2:35 | 2:16 |
| `cobol-modernization` | 25,2 | 24,2 | 23,1 | 23,3 | 15:39 | 8:46 | 15:00 | 12:25 |
| `regex-log` | 5,4 | 15,0 | 15,5 | 27,9 | 49:11 | 21:52 | 23:28 | 8:37 |
| `headless-terminal` | 24,1 | 25,2 | 26,3 | 27,0 | 7:29 | 14:13 | 5:28 | 6:42 |
| `mailman` | 21,0 | 19,7 | 11,9 | 22,1 | 40:08 | 30:33 | 21:18 | 14:09 |
| `fix-ocaml-gc` | 24,5 | 21,2 | 20,6 | 21,1 | 25:01 | 27:10 | 17:39 | 31:45 |
| `break-filter-js-from-html` | 11,4 | 6,5 | 16,6 | 23,9 | 18:10 | 55:22 | 33:28 | 19:12 |
| `sqlite-with-gcov` | 24,0 | 22,2 | 19,5 | 22,3 | 2:22 | 4:22 | 2:38 | 2:27 |
| `sparql-university` | 19,8 | 27,7 | 26,5 | 25,0 | 30:59 | 11:33 | 12:04 | 6:36 |
| `llm-inference-batching-scheduler` | 19,1 | 21,1 | 6,1 | 19,9 | 58:46 | 54:09 | 52:23 | 57:48 |
| `configure-git-webserver` | 24,7 | 23,7 | 20,6 | 26,2 | 7:35 | 5:17 | 3:59 | 3:36 |
| `build-cython-ext` | 22,6 | 20,4 | 20,4 | 22,4 | 22:57 | 15:26 | 17:17 | 14:13 |
| `extract-elf` | 23,3 | 22,7 | 22,4 | 24,5 | 54:39 | 25:53 | 8:52 | 16:44 |
| `build-pov-ray` | 19,5 | 17,4 | 18,2 | 17,8 | 18:20 | 33:08 | 27:13 | 37:16 |
| `openssl-selfsigned-cert` | 30,1 | 27,5 | 27,2 | 30,2 | 2:24 | 2:34 | 1:43 | 2:10 |
| `overfull-hbox` | 26,2 | 24,3 | 21,0 | 22,1 | 19:38 | 16:46 | 9:38 | 15:25 |
| `mteb-retrieve` | 24,7 | 23,9 | 22,9 | 25,4 | 8:58 | 4:54 | 11:16 | 3:56 |

- UD-IQ1_M · medium: 5,4 bis 30,1 t/s je Aufgabe, über alle Aufgaben 19,6 t/s; der Agent wartete 6 h 30 min auf das Modell, das sind 79 % der Laufzeit.
- UD-Q2_K_XL · medium: 6,5 bis 27,7 t/s je Aufgabe, über alle Aufgaben 18,8 t/s; der Agent wartete 5 h 41 min auf das Modell, das sind 75 % der Laufzeit.
- UD-IQ3_XXS · medium: 6,1 bis 27,3 t/s je Aufgabe, über alle Aufgaben 16,8 t/s; der Agent wartete 4 h 31 min auf das Modell, das sind 70 % der Laufzeit.
- UD-IQ4_XS · medium: 17,8 bis 30,2 t/s je Aufgabe, über alle Aufgaben 21,9 t/s; der Agent wartete 4 h 21 min auf das Modell, das sind 63 % der Laufzeit.

## Ausführung

- Benchmark: Terminal-Bench-Local, Terminal-Bench 2.1 (Revision `5c8eadf1f393`), Harbor 0.20.0, Agent Terminus-2
- Ein Versuch je Aufgabe (pass@1), ein Stream (`-np 1`), MTP als Draft-Head aktiv, `reasoning_effort: medium`
- Zeitlimit 3600 s je Aufgabe statt der 3 Stunden, die der Benchmark voreinstellt; bei 19 der 20 Aufgaben liegt das über dem Limit, das die Aufgabe selbst vorgibt
- Container je Aufgabe: 1 CPU, 2 GB RAM (nur `overfull-hbox`: 2 CPUs, 4 GB)
- Engine: llama.cpp 0.3.0-dev (build 1, commit 60bce1a), Backend rocm 7.1.52802, Kontext 163840

### UD-IQ1_M · medium

```bash
ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/38bb39ee97821de2c9009abb7e93950eec396e66/UD-IQ1_M/Qwen3.8-Flash-Next-UD-IQ1_M-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{"reasoning_effort": "medium"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4
```

| Posten | Größe |
| --- | --- |
| Gewichte (resident) | 45.2 GiB |
| PLE-Tabelle lazy (nicht resident) | 26.8 GiB |
| KV-Cache (12 Attn-Layer) | 2.0 GiB |
| Indexer-Cache | 0.7 GiB |
| DeltaNet-Zustand | 0.1 GiB |
| Compute-Buffer (Schätzung) | 1.6 GiB |
| MTP-Head + Draft-KV | 3.4 GiB |
| Prompt-Cache (max) | 2.0 GiB |
| Summe | 55.1 GiB |
| Verfügbar (MemAvailable) | 106.5 GiB |
| Reserve OS/Page-Cache | 6.0 GiB |
| Spielraum | 45.4 GiB |

### UD-Q2_K_XL · medium

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

### UD-IQ3_XXS · medium

```bash
ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-IQ3_XXS/Qwen3.8-Flash-Next-UD-IQ3_XXS-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{"reasoning_effort": "medium"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4
```

| Posten | Größe |
| --- | --- |
| Gewichte (resident) | 52.1 GiB |
| PLE-Tabelle lazy (nicht resident) | 26.8 GiB |
| KV-Cache (12 Attn-Layer) | 2.0 GiB |
| Indexer-Cache | 0.7 GiB |
| DeltaNet-Zustand | 0.1 GiB |
| Compute-Buffer (Schätzung) | 1.6 GiB |
| MTP-Head + Draft-KV | 3.4 GiB |
| Prompt-Cache (max) | 2.0 GiB |
| Summe | 62.0 GiB |
| Verfügbar (MemAvailable) | 106.5 GiB |
| Reserve OS/Page-Cache | 6.0 GiB |
| Spielraum | 38.4 GiB |

### UD-IQ4_XS · medium

```bash
ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-IQ4_XS/Qwen3.8-Flash-Next-UD-IQ4_XS-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{"reasoning_effort": "medium"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4
```

| Posten | Größe |
| --- | --- |
| Gewichte (resident) | 63.0 GiB |
| PLE-Tabelle lazy (nicht resident) | 26.8 GiB |
| KV-Cache (12 Attn-Layer) | 2.0 GiB |
| Indexer-Cache | 0.7 GiB |
| DeltaNet-Zustand | 0.1 GiB |
| Compute-Buffer (Schätzung) | 1.6 GiB |
| MTP-Head + Draft-KV | 3.4 GiB |
| Prompt-Cache (max) | 2.0 GiB |
| Summe | 72.9 GiB |
| Verfügbar (MemAvailable) | 106.5 GiB |
| Reserve OS/Page-Cache | 6.0 GiB |
| Spielraum | 27.5 GiB |

## Weitere Läufe

- UD-Q4_K_XL · medium: 1/1 Aufgaben (1 min), Profil `mtp4-ngram-thinking-medium`

Rohdaten: `state/quality/tbench/`, Transkripte und Verifier-Ausgaben unter `bench/quality/terminal-bench-mini/jobs/`. Interaktive Ansicht: [terminal-bench.html](terminal-bench.html).
