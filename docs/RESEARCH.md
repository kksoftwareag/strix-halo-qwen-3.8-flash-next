# Qwen3.8-Flash-Next auf Strix Halo – Recherche (Stand 2026-09-03)

Zusammengetragen aus offiziellen Quellen (Qwen-Modellkarte, unsloth-Doku), llama.cpp-PRs/-Issues, Community-Berichten
zu Strix Halo und eigenen Messungen auf dieser Maschine (Ryzen AI MAX+ 395, 109,7 GiB nutzbarer RAM, ROCm/HIP 7.1,
Fedora 44). Eigene Messwerte sind als solche markiert. Quellen: nummerierte Liste am Ende.

## 1. Modell-Fakten

- **Architektur** (`qwen4exp`, „A Preview of the Qwen4 Architecture“): 125B Parameter, 6B aktiv, plus 51B n-Gram-Embedding
  (PLE) und 4B MTP-Head [1][2]. 48 Layer = 12 × (3 Gated-DeltaNet + 1 Qwen-Sparse-Attention); nur die 12 Full-Attention-Layer
  haben einen KV-Cache (24 Q-Heads, 2 KV-Heads, head_dim 256, RoPE auf 64 Dims), dazu ein Indexer (4 Heads, 128 Dims, Budget
  2048, Compress-Ratio 4). 512 Experten, 10 geroutet + 1 shared, Experten-FFN 640. Hyper-Connections (4 Streams, Low-Rank 320).
  Vokabular 248 320 [2].
- **PLE / n-Gram-Tabelle**: eine PLE-Schicht (Layer 2), Trigramme, 20M Einträge × 8 Heads → Tensor `per_layer_token_embd`
  160 × 320 001 536, in allen unsloth-Quants identisch **26,8 GiB IQ4_NL** (eigene GGUF-Analyse). Unsloth hält sie bewusst
  ≥ 4 bit [4].
- **Kontext**: nativ 262 144 Tokens, per statischem YaRN (Faktor 4) bis 1M [1].
- **Thinking**: standardmäßig an. Chat-Template akzeptiert `enable_thinking` (Default true), `preserve_thinking` und
  `reasoning_effort` mit **genau** `xhigh` (Default), `medium`, `low` – jeder andere Wert wirft eine Template-Exception
  (eigene Prüfung des GGUF-Templates) [1].
- **Offizielle Sampling-Werte** [1][4]:
  - Thinking: temp 1.0, top_p 0.95, top_k 20, min_p 0, presence 0, repeat 1.0 (im GGUF hinterlegt).
  - Non-Thinking: temp 0.7, top_p 0.80, top_k 20, min_p 0, presence 1.5.
  - Für Agenten-Aufgaben empfiehlt Qwen bis 262k Reasoning- und 131k Antwort-Tokens; niedrigerer Effort verkürzt Agent-Läufe
    nicht immer. Ein Community-Setup nutzt `--reasoning-budget 4000` mit `medium` [5].
- **Tool-Calls**: XML-Format `<tool_call><function=…><parameter=…>…` (vLLM: `--tool-call-parser qwen3_coder`) [3].

## 2. Quant-Qualität (unsloth-KLD-Tabelle [4]) und was davon resident ist

| Quant | Datei (GiB, gemessen) | davon Experten | resident ohne PLE | KLD | Top-1 |
| --- | --- | --- | --- | --- | --- |
| UD-IQ1_M | 69,4 | 39,0 | 42,7 | 0,3147 | 79,7 % |
| UD-Q2_K_XL | 73,4 | 42,9 | 46,6 | 0,2246 | 82,7 % |
| UD-IQ3_XXS | 76,3 | 45,3 | 49,5 | 0,1651 | 85,4 % |
| UD-IQ4_XS | 87,2 | 55,4 | 60,4 | 0,0836 | 89,6 % |
| UD-Q4_K_XL | 103,7 | 71,7 | 76,9 | 0,0469 | 92,3 % |

Die Quants unterscheiden sich ausschließlich in der Präzision der gerouteten Experten; Attention/DeltaNet/Shared-Experts
bleiben Q5_K–Q8_0. Unsloth nennt UD-Q2_K_XL als Untergrenze für Tool-Calling/Agenten [4].
KV-Cache: q8_0 K+V ist praktisch verlustfrei (KLD 0,0018), q4_0 für K zerstört die Qualität (KLD 5,5) [7].

## 3. llama.cpp-Status

- Basis-Architektur upstream seit 2026-08-27 (PR #27742), Folge-Fixes #27880, #27941, und **#28123 (nativer
  Recurrent-State-Rollback, 2026-09-01)** [8]. Der lokale Fork `~/models/llama.cpp-mtp` (b10685, 17252c769) enthält
  #27941/#28123 **nicht**; ohne Rollback wird pro Spekulationsrunde der Rekurrenz-Zustand in den Host-Speicher
  gesichert (auf Vulkan der Grund für 21 → 5 t/s; auf HIP „works cleanly“, aber messbar).
- **MTP upstream nicht gemerged**: PR #27836 (Draft) und PR #28243 (unsloth, „shared“ Heads) sind offen [9][10].
  Der lokale Patch portiert den Graph aus #27739 (dzannotti). Konsequenz für die Heads:
  - `dzannotti/…-MTP-Q4_K_M.gguf` (2,44 GiB): Tensornamen `output_hc_*` → **passt** zum lokalen Loader.
  - `unsloth/…/MTP/mtp-…-Q4_K_M.gguf` (2,59 GiB): Tensornamen `blk.48.nextn.hc_head_*` → **braucht den unsloth-Fork**
    (b10715-mix) und lädt hier nicht (eigene GGUF-Prüfung, unsloth-README [10]).
- Flags (in `common/arg.cpp` verifiziert): `--spec-type` (kommagetrennt: draft-mtp, ngram-mod, …), `--spec-draft-n-max`
  (Default 3), `--spec-draft-n-min` (0), `--spec-draft-p-min` (0.0; stoppt das Drafting, sobald die Top-1-Wahrscheinlichkeit
  des Heads darunter fällt – ändert nur Tempo, nie Ausgabe), `-md`, `-ngld`, `--cache-ram` (8192 MiB; die Obergrenze greift
  unter Linux-Overcommit praktisch nicht, Issue #22629), `--tensor-read-lazy` (auto = lazy für Tensoren > 4 GiB, **nur mit
  mmap**), `--load-mode`.
- **MTP + ngram-mod kombinierbar** (`--spec-type draft-mtp,ngram-mod`): n-Gram-Drafts haben Vorrang, kein Verketten [11].
- **Temperatur senkt die Akzeptanz**: Die Verifikation sampelt mit dem vollen Sampler; alle veröffentlichten Speedups sind
  greedy [10][12].
- **LLAMA_ATTN_ROT_DISABLE=1 ist nicht mehr nötig**: Der Assert, der den Load mit quantisiertem KV abbrach, existierte nur
  in der Pre-Merge-Revision von #27742; der lokale Baum rotiert Q/K/V selbst (`qwen4exp.cpp:808ff`). **Eigene Messung**
  (Q2_K_XL, q8_0 KV, 32k): Load ohne die Variable ok (`attn_rot_k = 1, attn_rot_v = 1`), tg 24,2 t/s statt 24,6 t/s
  (−2 %), dafür bessere Qualität des quantisierten KV (PR #21038). Das TUI lässt die Rotation an.
- `GGML_HIP_ROCWMMA_FATTN` existiert in dieser llama.cpp-Version nicht mehr (Cmake-Option entfernt) – und war auf Strix Halo
  ohnehin schädlich (pp -77 % bei 30k Tiefe) [13].
- **GGML_HIP_ENABLE_UNIFIED_MEMORY=1 niemals setzen**: 76,9 GB anonymer RSS statt GTT [14].

## 4. Speicher auf dieser Maschine (eigene Messungen, bench/results/mem)

- Alles teilt sich 109,7 GiB: GTT (Gewichte, KV, Compute) + Host-RAM. GTT taucht **nicht** im RSS auf; `MemAvailable` ist
  die einzige verlässliche Größe → `bench/memguard.py` und der Wächter im TUI.
- Lade-Modus `auto` (llama-Default): ROCm meldet „kein mmap“ → die 26,8-GiB-PLE-Tabelle wird in einen **CPU-Puffer kopiert
  (28 GiB anonym)**. Footprint = resident Gewichte + 28 GiB + KV/Compute + MTP. Q2: 47,4 GTT + 28 RSS = 75,7 GiB (gemessen).
  **UD-Q4_K_XL + MTP → 76,4 + 28 + 2,5 + … > 107 → Kernel-OOM** (zweimal passiert).
- `--load-mode mmap`: lazy greift („lazy read enabled“, `CPU_Mapped`), Footprint Q2 nur 48 GiB. **Aber** der Gewichte-Upload
  läuft über seitenweise Page-Faults ohne Readahead: Q4_K_XL brauchte **140 Minuten** (18 MB/s, 149 GB gelesen); Q2 mit
  warmem Page-Cache 14 s. Auf dem Stock-Fork ist mmap nur brauchbar, wenn die Gewichts-Shards bereits im Page-Cache liegen.
- **EngramHalo.cpp** [15] löst genau das: Readahead-Hints für die Engram-Zeilen, `LLAMA_MMAP_DROP_BEHIND` (Page-Cache hinter
  dem Upload freigeben), HIP-Top-k-Kernel (behebt CPU-Fallback ab ~1k Kontext), FA-Vektorkernel, sparse QSA-Gather ab 16k.
  Gemessen (IQ3_XXS, q8_0 KV, temp 0): Code-Decode 24,4 → 39,3 t/s (RAM-Modus) / 35,3 (SSD-Modus), Prosa 22,4 → 25,3,
  Code @78k 10 → 21–25 t/s, pp4096 352 → 496. Unabhängige Reproduktion auf 128 GB: HIP+MTP 66 t/s Code (q8_0 KV) bzw.
  82 t/s (f16 KV), Prosa ~22 [14]. Empfohlene Flags: `ROCBLAS_USE_HIPBLASLT=1 … -lm none -b 8192 -ub 2048 -t 4
  --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75`; SSD-Modus: `-lm mmap --tensor-read-lazy on`.

## 5. Strix-Halo-Tuning

- **ROCm/HIP vs Vulkan**: HIP gewinnt Prompt-Processing (+20 %), Vulkan oft Decode (+10–25 %) [16] – aber mit MTP ist Vulkan
  auf dieser Architektur ohne On-Device-Checkpoints ein Verlust (21 → 5 t/s) [9]; HIP ist die richtige Wahl (deckt sich mit
  der Einschätzung des Nutzers). Vulkan-Dev-Header fehlen auf dem System ohnehin.
- Eigene llama-bench-Zahlen (HIP, -fa on, ohne MTP): Q4_K_XL pp512 ≈ 410–420 t/s, tg128 ≈ 21 t/s; Q2_K_XL pp ≈ 395,
  tg ≈ 24,5 t/s; KV q8_0 vs f16 und ub 512 vs 2048 ohne nennenswerten Unterschied bei 512 Tokens.
- Community-MTP-Zahlen mit dem dzannotti-Head (n3/p0.75, q8_0 KV): ROCm Q4_K_XL 20,3 → 35,8 t/s Code / 22,6 Prosa
  (Akzeptanz 0,90/0,74); IQ4_XS 18 → 32,8/22,1 [12]. Auf bandbreitenlimitierter Hardware gewinnt kleine Draft-Tiefe
  (n2–n4); n16/p0.8 ist eine 5090-Empfehlung, nicht übertragbar [17].
- KV-Cache: q8_0 (bf16 KV meiden: FA-Pfad konvertiert bei hd 256 den ganzen Cache um) [15]; bei Tiefe ist q8_0 schneller als
  f16 (30 vs 17 t/s @32k auf GPU) [18].
- Kernel/Host: `amd_iommu=off amdgpu.gttsize=126976 ttm.pages_limit=32505856` sind gesetzt; AMD empfiehlt kleinen BIOS-VRAM-
  Carve-out (0,5 GB) zugunsten GTT [19]; tuned `accelerator-performance` bzw. Governor `performance` (aktuell powersave/
  balanced – siehe System-Tab).
- `--fit` (Default an, 1024 MiB Marge) verkleinert ein explizit gesetztes `-c` nie; auf HIP sieht es die Speicherlage nur
  über `hipMemGetInfo` [20].

## 6. Alternativen zu llama.cpp – Fazit

Nichts anderes läuft heute auf einem einzelnen Strix Halo mit diesem Modell: vLLM validiert nur MI355X, alle vLLM-
Checkpoints (FP8 173 GiB, AWQ 168 GiB, NVFP4 126 GiB) lassen die 51B-n-Gram-Tabelle in BF16 und passen nicht [21]; SGLang
lehnt gfx1151 ab; ik_llama.cpp hat qwen4exp+MTP, aber ROCm/Vulkan sind dort „unsupported“; Ollama liefert nur MLX-Tags;
LM Studio und Lemonade wrappen upstream llama.cpp ohne MTP. Die echte Konkurrenz sind Strix-Halo-Forks (EngramHalo.cpp,
kyuz0-Container `rocm-10.0-qwen-3.8-flash-next`, LaurentZuijdwijk `vulkan/qwen4exp-rocmfpx`). ROCmFP4-Quants sind optional
(Qualität unvermessen).

## 7. Eigene Messungen (2026-09-03, 32k Kontext, q8_0 KV, dzannotti-Head, Prompt „Zähle 1–30 + KV-Cache-Erklärung“, 300 Tokens)

| Engine | Quant | MTP | Load | tg | Akzeptanz | Footprint (MemAvailable-Δ) |
| --- | --- | --- | --- | --- | --- | --- |
| Stock-Fork (auto) | Q2_K_XL | – | 20 s | 24,6 t/s | – | 75,7 GiB |
| Stock-Fork (auto) | Q2_K_XL | n3/p0.75 | 22 s | 34,8 t/s | 86 % | 78,8 GiB |
| Stock-Fork (auto) | IQ3_XXS | n3/p0.75 | 23 s | 35,1 t/s | 88 % | 81,5 GiB |
| Stock-Fork (auto) | IQ4_XS | n3/p0.75 | 26 s | 34,2 t/s | 87 % | 92,7 GiB |
| Stock-Fork (auto) | Q4_K_XL | n3/p0.75 | – | **OOM** | – | > 107 GiB |
| Stock-Fork (mmap) | Q4_K_XL | – | **140 min** | – | – | 30 GiB frei, aber unbenutzbar |
| EngramHalo (-lm none) | IQ3_XXS | – | 17 s | 23,1 t/s | – | 52,8 GiB |
| EngramHalo (-lm none) | IQ3_XXS | n4/p0.75+ngram | 16 s | 34,4 t/s | 79 % | 57,4 GiB |
| EngramHalo (-lm none) | IQ4_XS | n4/p0.75+ngram | 20 s | 36,5 t/s | 84 % | 68,7 GiB |
| EngramHalo (-lm none) | **Q4_K_XL** | n4/p0.75+ngram | 28 s | **35,3 t/s** | 80 % | **84,7 GiB** |
| EngramHalo (-lm mmap) | Q4_K_XL | n4/p0.75+ngram | 39 s | 35,5 t/s | 80 % | 83,4 GiB (RSS 57 GiB = gemappte, verdrängbare Seiten) |

**MTP-Feintuning** (EngramHalo, UD-Q4_K_XL, `-lm none`, 32k, q8_0 KV, reasoning medium, 3 Prompts à 400 Tokens, temp 1.0 sofern nicht anders):

| Konfiguration | tg Ø | Code | Prosa | Reasoning | Akzeptanz |
| --- | --- | --- | --- | --- | --- |
| ohne MTP | 20,8 | 20,8 | 20,8 | 20,9 | – |
| n2 / p0.75 | 30,9 | 30,7 | 28,2 | 33,8 | 85 % |
| n3 / p0.75 | 33,9 | 33,1 | 29,7 | 38,9 | 83 % |
| **n4 / p0.75 + ngram-mod** (Preset) | 34,7 | 32,1 | 31,2 | 41,0 | 80 % |
| n4 / p0.0 | 36,0 | 32,5 | 31,1 | 44,5 | 55 % |
| n6 / p0.75 + ngram-mod | 35,7 | 34,9 | 30,9 | 41,3 | 76 % |
| n3 / p0.75, temp 0.6 | 35,3 | 36,1 | 30,4 | 39,5 | 86 % |
| n3 / p0.75, temp 0.0 | 35,8 | 36,2 | 30,8 | 40,3 | 87 % |

Fazit: MTP bringt 1,5–2,1× je nach Textart (Reasoning-Ausgaben am meisten); zwischen n3 und n6 bzw. p0.0 und p0.75 liegen
nur ~5 % (Messrauschen ~3 %). Temperatur 1.0 (Qwen-Empfehlung) kostet gegenüber greedy nur ~5 % Akzeptanz.
**Mehrnutzer** (EngramHalo, UD-IQ4_XS, `-np 8`, 20480 Kontext je Slot, q8_0 KV, ohne MTP, 256 Tokens je Anfrage, Patch #25992 aktiv):

| gleichzeitige Nutzer | Σ Durchsatz | je Nutzer | TTFT p50 | Mix-ups |
| --- | --- | --- | --- | --- |
| 1 | 20,4 t/s | 21,4 t/s | 0,6 s | 0 |
| 2 | 32,0 t/s | 17,2 t/s | 0,9 s | 0 |
| 4 | 42,4 t/s | 11,6 t/s | 1,8 s | 0 |
| 8 | 50,4 t/s | 6,8 t/s | 2,7 s | 0 |

**Gemessen mit langen Prompts (2026-09-05, UD-IQ4_XS, je Nutzer ~16k Token Prompt, 2k Ausgabe, MTP an):**

| Slots | Prompt-Token | erzeugte Token | Dauer | Token gesamt/s | je Anfrage | Draft-Akzeptanz | saubere Antworten |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 16 253 | 1 130 | 86 s | 203 | 29,9 t/s | 0,70 | 1 von 1 |
| 2 | 32 624 | 1 192 | 141 s | 240 | 14,2 t/s | 0,69 | 2 von 2 |
| 4 | 65 144 | 3 378 | 307 s | 223 | 6,5 t/s | 0,71 | 4 von 4 |
| 8 | 130 457 | 7 011 | 678 s | 203 | 2,8 t/s | 0,60 | **2 von 8** |

Zwei Ergebnisse: **Parallelität bringt bei langen Prompts nichts** — der Gesamtdurchsatz aus Prompt- und
Ausgabe-Token bleibt über alle Stufen bei 203 bis 240 t/s, während die einzelne Antwort von 29,9 auf 2,8 t/s
einbricht. Bei kurzen Prompts steigt der Durchsatz mit der Slotzahl (20 → 50 t/s, Tabelle oben), weil die Maschine
zwischen den Token Leerlauf hat; bei langen Prompts ist sie schon mit einem Strom ausgelastet.

Und **bei acht Slots geht die Ausgabe kaputt**: Nur zwei von acht Nutzern geben das vorgegebene Codewort korrekt
wieder, zwei Antworten bleiben leer, eine wiederholt den Prompt, drei verfälschen das Codewort um ein bis zwei
Zeichen. Echtes Übersprechen zwischen Slots gibt es nicht (kein fremdes Codewort in einer Antwort) — der Schaden
entsteht innerhalb der Antwort, wie in Issue #27572 beschrieben. Bis vier Slots ist alles sauber.

Betriebsempfehlung: langer Kontext → ein Slot; mehrere Slots nur für Chat mit kurzen Prompts. Der Fix
(`engine/patches/0003-27311-uma-ring-buffer.patch`) liegt bereit, ist aber nicht gebaut — er würde die kaputten
Antworten beheben, nicht den fehlenden Durchsatzgewinn. Auswertung: `bench/analyze_multiuser.py`.

**Parallelitätsgrenzen je Quant.** `-c` ist der Gesamtkontext über alle Slots; bei `-np 4 -c 262144` bekommt jeder
Slot 65536 Token. Es zählen zwei Größen: KV- und Indexer-Cache mit **17952 Byte je Token** (0,55 GiB je 32k, gleich
für alle Quants, weil nur 12 der 48 Layer Attention haben und der KV-Typ q8_0 ist) und der DeltaNet-Zustand mit
**113 MiB je Slot**, unabhängig von der Kontextlänge. Der Kontext eines einzelnen Slots ist durch die Trainingslänge
auf 262144 Token begrenzt, nicht durch den Speicher — diese 256k passen bei jedem Quant, auch bei UD-Q4_K_XL
(94,1 GiB belegt, 6,4 GiB Spielraum).

Höchstzahl gleichzeitiger Kontexte der angegebenen Größe (mit MTP / ohne MTP), berechnet mit `bench/context_limits.py`
auf dem Speichermodell des Programms für 106,5 GiB freien Speicher, Prompt-Cache 2 GiB, ubatch 2048, 6 GiB Reserve; bei 64 abgeschnitten:

| Quant | Gewichte resident | 16k je Slot | 32k | 64k | 128k | 256k |
| --- | --- | --- | --- | --- | --- | --- |
| UD-IQ1_M | 45,2 GiB | 64 / 64 | 64 / 64 | 37 / 42 | 19 / 22 | 10 / 11 |
| UD-Q2_K_XL | 49,2 GiB | 64 / 64 | 63 / 64 | 34 / 39 | 18 / 20 | 9 / 10 |
| UD-IQ3_XXS | 52,1 GiB | 64 / 64 | 59 / 64 | 32 / 37 | 17 / 19 | 8 / 9 |
| UD-IQ4_XS | 63,0 GiB | 64 / 64 | 44 / 51 | 23 / 27 | 12 / 14 | 6 / 7 |
| UD-Q4_K_XL | 79,5 GiB | 27 / 37 | 16 / 21 | 8 / 11 | 4 / 6 | 2 / 3 |

Praktisch ist bei den kleinen Quants nicht der Speicher die Grenze, sondern der Durchsatz: Bei 8 Slots bleiben
6,8 t/s je Anfrage (siehe Tabelle oben). Für Chat reicht das, für Agenten nicht — ein Agent mit 30000 Ausgabe-Token
wartet dann 74 statt 25 Minuten. Deshalb laufen die Agenten-Benchmarks mit einem Slot. Dazu kommt: MTP lohnt nur bei
einem Slot (bei 8 Slots 35 statt 50 t/s), und mehrere Slots brauchen auf gfx1151 den Patch aus Issue #25992.

Mit MTP (UD-Q4_K_XL, n4/p0.75+ngram, sonst gleich): 1 Nutzer 35,9 t/s (Akzeptanz 82 %), 2 Nutzer Σ 30,8, 4 Nutzer Σ 35,5,
8 Nutzer Σ 34,8 t/s (Akzeptanz 59–66 %). **MTP lohnt nur für Einzelnutzer**; ab 2 gleichzeitigen Anfragen liegt Continuous
Batching ohne Draft vorn (bei 8 Nutzern 50 vs 35 t/s).
Continuous Batching skaliert bis 8 Nutzer auf das 2,5-Fache des Einzeldurchsatzes; je Nutzer bleiben bei 8 noch ~7 t/s.
Ohne den #25992-Patch (gepinnte Host-Puffer auf der iGPU) sind auf gfx1151 vermischte Antworten zwischen Slots
berichtet; mit Patch trat in 15 Anfragen kein Mix-up auf.
Rotation an vs. aus (Stock, Q2, ohne MTP): 24,2 vs 24,6 t/s → Rotation bleibt an.
Gemessene Puffer (HIP): Compute 297 MiB @ub 512 bzw. 1188 MiB @ub 2048 (+121/233 MiB Host); Kontext 32k q8_0 = 673 MiB
(KV 408 + Indexer 153 + RS 113); MTP-Draft 2146 MiB + 740 MiB Compute. Der Schätzer im TUI ist darauf kalibriert.

## 8. Konkrete Empfehlung (Presets im TUI)

1. **Standard: EngramHalo + UD-Q4_K_XL + MTP** (`eh-qualitaet`): `-lm none`, `-b 8192 -ub 2048 -t 4`, `ROCBLAS_USE_HIPBLASLT=1`,
   `--spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75`, 128k Kontext, q8_0 KV, ~22 GiB Spielraum.
2. Schneller/kleiner: `eh-schnell` (IQ3_XXS) oder IQ4_XS; 160k Kontext: `eh-longctx` (IQ4_XS).
3. Fallback ohne EngramHalo: Stock-Fork mit IQ4_XS + MTP (n3/p0.75), nie Q4_K_XL mit MTP.
4. Thinking: `medium` als Alltag, `xhigh` nur wenn nötig (Token-Verbrauch); Non-Thinking-Sampling temp 0.7/top_p 0.8/presence 1.5.

## 9. Offene Punkte (per Benchmark im TUI klären)

- Akzeptanz/Speedup von MTP bei Qwen-Sampling (temp 1.0) statt greedy; bester n_max/p_min-Punkt je Quant.
- Rotation an (ohne Env) vs aus: Load-Verhalten und tg-Kosten.
- EngramHalo: dzannotti-Head kompatibel? EasiiX-Q8_0-Sidecar (4,1 GB) mit höherer Akzeptanz [15].
- Ob ein Rebase des lokalen Patches auf master ≥ 2026-09-01 (#28123 Rollback) die MTP-Kosten senkt.

**MTP bei mehreren Slots (vorbereitet, Messung steht aus).** Bei `-np N` mit Prompts ab etwa 19000 Token und mehreren
Ubatches fällt die Draft-Akzeptanz auf 0,0, und MTP wird langsamer als kein MTP —
[Issue #27572](https://github.com/ggml-org/llama.cpp/issues/27572), gemeldet auf gfx1151/ROCm mit einem Hybrid aus
Gated DeltaNet und Attention. Ursache ist ein Write-after-Read-Rennen auf Unified Memory; der Fix ist
[PR #27311](https://github.com/ggml-org/llama.cpp/pull/27311) („Scheduler UMA ring buffer"), dort auf Strix Halo gemessen:
Akzeptanz bei `-np 8` 0,5083 mit Ring gegen 0,0 ohne, Sanitizer-Rennen 0 gegen 3597, Durchsatzkosten unter 1 %.

Unsere Messung vom 2026-09-04 traf den Fehler nicht: `-np 8` mit `draft-mtp,ngram-mod`, aber nur 71 Token Prompt —
16 Akzeptanzmessungen zwischen 0,46 und 1,00, kein Nullwert. Der Einbruch braucht lange Prompts.

Vorbereitet ist beides: Die 18 Commits des PR sind auf unseren Basis-Commit übertragen und liegen als
`engine/patches/0003-27311-uma-ring-buffer.patch` (auf den Stock-Fork direkt anwendbar, auf EngramHalo per
Drei-Wege-Merge, beides geprüft); dazu `0004-28433-draft-ctx-per-seq.patch`, der den Draft-Kontext aus
`llama_n_ctx_seq()` statt `llama_n_ctx()` dimensioniert ([Issue #28433](https://github.com/ggml-org/llama.cpp/issues/28433)).
`engine/fetch.sh` lässt beide standardmäßig weg, `ENGINE_RING_PATCH=1` schaltet sie an — so entspricht ein
frischer Build genau dem, mit dem alle Messwerte hier entstanden sind. Die Messreihe dazu ist
`bench/mtp_multiuser.sh` (1/2/4/8 Nutzer, 15k Prompt je Nutzer, 2k Ausgabe, MTP an) — einmal mit den bestehenden
Builds als Vergleichswert, dann nach dem Neubau, jeweils über UD-IQ4_XS, UD-IQ3_XXS, UD-Q2_K_XL und UD-IQ1_M.
UD-Q4_K_XL ist nicht voreingestellt, passt bei acht Slots aber ebenfalls.

## Quellen
1. https://huggingface.co/Qwen/Qwen3.8-Flash-Next
2. https://huggingface.co/Qwen/Qwen3.8-Flash-Next/raw/main/config.json
3. https://github.com/QwenLM/Qwen3.8-Flash-Next/
4. https://unsloth.ai/docs/models/qwen3.8-next
5. https://gist.github.com/ryan4yin/48617bbddacc7067f10799770b7cc33f
6. https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF
7. https://github.com/ggml-org/llama.cpp/discussions/23470
8. https://github.com/ggml-org/llama.cpp/pull/28123
9. https://github.com/ggml-org/llama.cpp/pull/27836
10. https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF/blob/main/MTP/README.md
11. https://github.com/ggml-org/llama.cpp/issues/23184
12. https://huggingface.co/dzannotti/Qwen3.8-Flash-Next-MTP-GGUF
13. https://github.com/lemonade-sdk/lemonade/issues/2624
14. https://github.com/abliter8-ai/qwen-3.8-next-flash-amd-strix-halo
15. https://github.com/Aristo94/EngramHalo.cpp (Branch strix-halo-qwen4exp, docs/strix-halo/README.md)
16. https://www.soothill.io/blog/2026/08/03/llamacpp-vulkan-vs-rocm-strix-halo/
17. https://github.com/ggml-org/llama.cpp/discussions/25198
18. https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF/discussions/3
19. https://rocmdocs.amd.com/en/develop/how-to/system-optimization/strixhalo.html
20. https://github.com/ggml-org/llama.cpp/issues/23472
21. https://recipes.vllm.ai/Qwen/Qwen3.8-Flash-Next
22. https://github.com/ggml-org/llama.cpp/pull/28136 (`--lazy-mode on-direct`, offen)
23. https://github.com/kyuz0/amd-strix-halo-toolboxes
