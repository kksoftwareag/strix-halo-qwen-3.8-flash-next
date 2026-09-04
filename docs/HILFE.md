# Hilfe – Qwen3.8-Flash-Next auf Strix Halo

## Bedienung
- **Konfiguration**: Felder ändern → rechts aktualisieren sich Speicherschätzung, Warnungen und die fertige Kommandozeile.
  Preset wählen + „Preset anwenden“ setzt eine sinnvolle Gesamtkonfiguration. Profile speichern/laden unter `state/profiles/`.
- **F5** startet den Server mit der aktuellen Konfiguration (Tab „Server“ zeigt Log, Ladezeit, Puffergrößen, t/s, Draft-Akzeptanz).
  **F6** stoppt ihn. „Test-Prompt“ schickt eine kurze Anfrage und zeigt Geschwindigkeit + Akzeptanzrate.
- **Benchmark**: `llama-bench` (pp512/tg128, ohne MTP), Server-Messung mit MTP, der MTP-Sweep (probiert mehrere
  Draft-Einstellungen durch und übernimmt die schnellste) und der **Mehrnutzer-Test**: ein Server mit `-np N` Slots
  (Continuous Batching), dann 1/2/4/8 gleichzeitige Chat-Anfragen. Gemessen werden Gesamtdurchsatz (Σ t/s),
  Durchsatz je Nutzer, Zeit bis zum ersten Token (TTFT p50/p95) und per Codewort, ob Antworten zwischen Slots
  vermischt werden („Mix-up“, ein bekannter gfx1151-Fehler, den der eingebaute Patch #25992 behebt). MTP ist im
  Mehrnutzer-Test standardmäßig aus (auf dieser Architektur nicht für mehrere Slots validiert), per Schalter zuschaltbar.
  Ohne TUI: `./run.sh bench-parallel --users 8 [--levels 1,2,4,8] [--preset …] [--keep-mtp]`.
  Ergebnisse landen in `state/bench/results.jsonl`.
- **Server für mehrere Nutzer betreiben**: Feld „Slots (-np)“ auf N setzen; `-c` ist dann der Gesamtkontext (N × Kontext
  je Slot, z. B. 8 × 16384 = 131072). Rekurrenter Zustand kostet ~113 MiB je Slot, der KV-Cache bleibt gleich groß.
  **MTP dabei ausschalten**: gemessen 8 Nutzer 50 t/s ohne vs 35 t/s mit MTP (IQ4_XS/Q4_K_XL, EngramHalo).
- **System**: Hardware, Speicher (RAM/VRAM/GTT), Governor/tuned-Profil, Kernel-Parameter, andere LLM-Prozesse – mit
  konkreten Befehlen, falls etwas nicht optimal steht.
- **F9** exportiert ein eigenständiges Startskript (`scripts/start-<profil>.sh`) plus systemd-User-Unit.
- **Ctrl+S** speichert die aktuelle Konfiguration (`state/current.json`); `./run.sh run` startet sie ohne TUI,
  `./run.sh show` zeigt nur Kommando + Speicherbilanz.

## Speicher – das Wichtigste auf dieser Maschine
Alles (Gewichte, KV-Cache, Compute) liegt im selben 128-GB-RAM (16 GiB VRAM-Carve-out + GTT). Der Kernel-OOM-Killer
trifft den Server, wenn `MemAvailable` gegen 0 geht – GTT-Speicher taucht **nicht** im RSS des Prozesses auf.

- Das Modell enthält eine **26,8 GiB große Per-Layer-Embedding-Tabelle** (`per_layer_token_embd`). Im Lade-Modus `auto`
  nutzt ROCm kein mmap → die Tabelle wird komplett in einen CPU-Puffer kopiert (**≈28 GiB RAM zusätzlich zu den
  GTT-Gewichten**). Mit `--load-mode mmap` bleibt sie lazy (CPU_Mapped, Page-Cache), aber der Stock-Fork lädt die
  Gewichte dann seitenweise mit ~18 MB/s (UD-Q4_K_XL: 140 Minuten gemessen). **EngramHalo** (Engine „hip-engramhalo“)
  macht den SSD-Modus praktikabel (Readahead + Drop-Behind): `-lm mmap --tensor-read-lazy on` ≈ 1,5 GiB resident.
  Auf dem Stock-Fork passt deshalb **UD-Q4_K_XL + MTP nicht**; UD-IQ4_XS + MTP passt (~93 GiB). **EngramHalo** hält die
  Tabelle auch mit `-lm none` lazy (gemessen 2,7 GiB RSS) → UD-Q4_K_XL + MTP = ~85 GiB, Load 28 s.
- Resident bleiben: Experten + Attention/DeltaNet-Gewichte (Q2_K_XL ≈ 47 GiB, IQ3_XXS ≈ 50, IQ4_XS ≈ 60, Q4_K_XL ≈ 77 GiB),
  KV-Cache der 12 Full-Attention-Layer (f16: 24 KiB/Token → 3 GiB bei 128k; q8_0 ≈ 13 KiB/Token), Indexer-Cache
  (3 KiB/Token), Compute-Buffer (Logits über 248k Vokabular × ubatch), MTP-Head (2,5 GiB).
- Der **Speicher-Wächter** stoppt den Server hart, wenn weniger als N GiB frei sind (Feld „Schutz“).

## Parameter-Kurzreferenz
| Feld | Flag | Empfehlung |
| --- | --- | --- |
| Quant | `-m` | UD-Q4_K_XL (beste Qualität; mit EngramHalo auch mit MTP: 35 t/s, 85 GiB), IQ4_XS 36,5 t/s / 69 GiB, IQ3_XXS 34 t/s / 57 GiB |
| Kontext | `-c` | 131072 Standard; 262144 möglich (KV q8_0 ≈ 3,3 GiB) |
| KV-Cache | `-ctk/-ctv` | q8_0 (kein messbarer Tempo-Unterschied, halber Speicher); Rotation bleibt an (Env-Variable nicht nötig) |
| Flash Attention | `-fa on` | immer an |
| µBatch | `-ub` | 512; 2048 bringt < 3 % beim Prompt-Processing |
| Threads | `-t` | 16 (physische Kerne) |
| MTP | `--spec-type draft-mtp[,ngram-mod] -md … --spec-draft-n-max 3–4 --spec-draft-p-min 0.75` | nur der dzannotti-Head passt (`output_hc_*`); unsloth-Head braucht den unsloth-Fork. Speedup hängt von Akzeptanz ab; Temperatur > 0 senkt sie |
| Engine | – | `hip-engramhalo` (Strix-Halo-Fork: HIP-Top-k, sparse QSA-Gather, SSD-Modus) oder `hip-own`/`hip-user` (Stock-Fork + MTP-Patch) |
| EngramHalo-Tuning | `-lm none|mmap`, `-b 8192 -ub 2048 -t 4`, `ROCBLAS_USE_HIPBLASLT=1` | Empfehlung des Fork-Autors; im Benchmark-Tab gegenprüfen |
| Thinking | `--chat-template-kwargs '{"reasoning_effort":"…"}'` | xhigh (Template-Default), medium, low; `enable_thinking:false` schaltet ab |
| Sampling | `--temp 1.0 --top-p 0.95 --top-k 20 --min-p 0` | Qwen-Empfehlung (im GGUF hinterlegt) |
| Prompt-Cache | `--cache-ram` | 8192 MiB Default; -1 = unbegrenzt (OOM-Risiko) |

## Typische Fehlerbilder
- *Server bricht beim Laden ab, Log erwähnt `self_k_rot`/GGML_ASSERT*: alter Fork-Stand; hier laden b10685+Patch und EngramHalo mit aktiver Rotation. Notfalls Feld „Schutz“ → LLAMA_ATTN_ROT_DISABLE `on`.
- *Ladevorgang dauert Stunden*: `--load-mode mmap` auf dem Stock-Fork (Page-Faults ohne Readahead) → Lade-Modus `auto` oder Engine EngramHalo.
- *MTP-Head lädt nicht („missing tensor output_hc_norm“)*: unsloth-Head gewählt; dzannotti-Head nehmen (`auto`).
- *`Unexpected reasoning effort`*: Chat-Template kennt nur xhigh/medium/low.
- *Kernel-OOM*: Speicherbilanz rechts prüfen (Spielraum ≥ 8 GiB), kleineren Quant/Kontext wählen oder EngramHalo-SSD-Modus, andere LLM-Prozesse (ollama, LM Studio) beenden.
- *MTP wird ignoriert*: Engine ohne qwen4exp-MTP-Patch gewählt (die Builds aus `engine/` haben ihn; ein fremder llama.cpp-Build meist nicht).
