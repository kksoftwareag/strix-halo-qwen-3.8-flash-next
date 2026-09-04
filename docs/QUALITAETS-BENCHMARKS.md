# Qualitäts-Benchmarks für den Quant-Vergleich (8-Stunden-Budget)

Stand: 2026-09-04. Bewertung, welche Benchmarks sich auf dieser Maschine (Strix Halo, 128 GB) in einem Budget von
8 Stunden für den Vergleich der Quantisierungen eignen. Die Geschwindigkeitsmessungen stehen in `RESEARCH.md`.

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
| Terminal-Bench 2.0 (Harbor, Terminus-2) | 89 Aufgaben | `-l 10` | 3 bis 6 h für 10 Aufgaben | Rauchtest, kein Vergleich |
| DeepSWE (Pier, mini-swe-agent) | 113 Aufgaben, bis 2,5 h je Aufgabe | `--n-tasks 10 --sample-seed 0` | 5 bis 10 h für 10 Aufgaben | ungeeignet; Leaderboard nur Frontier-Modelle |

Hinweise zu einzelnen Kandidaten:

- **DeepSWE** ist seit 2026 ein eigener Benchmark von Datacurve (113 Langzeitaufgaben aus aktiven Repos, fünf Sprachen,
  handgeschriebene Verifier), nicht mehr nur das Agentica-Modell. Harness ist Pier (Harbor-kompatibel) mit mini-swe-agent
  als festem Scaffold; kein Schritt- oder Kostenlimit, Zeitlimit 2,5 h je Aufgabe.
- **Terminal-Bench 2.0** läuft über Harbor (`harbor run -d terminal-bench/terminal-bench-2 -a terminus-2 -m openai/<name> -n 4 -l 10`).
  Modelle werden über LiteLLM angesprochen; für einen lokalen Server `OPENAI_API_BASE` setzen. Einige Aufgaben brauchen
  mehrere GB RAM im Container.
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
