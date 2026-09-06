# Help – Qwen3.8-Flash-Next on Strix Halo

## Usage
- **Configuration**: change fields → on the right, the memory estimate, warnings and the finished command line update.
  Choosing a preset + "Apply preset" sets a sensible overall configuration. Save/load profiles under `state/profiles/`.
- **F5** starts the server with the current configuration ("Server" tab shows log, load time, buffer sizes, t/s, draft acceptance).
  **F6** stops it. "Test prompt" sends a short request and shows speed + acceptance rate.
- **Benchmark**: `llama-bench` (pp512/tg128, without MTP), server measurement with MTP, the MTP sweep (tries several
  draft settings and adopts the fastest) and the **multi-user test**: one server with `-np N` slots
  (continuous batching), then 1/2/4/8 concurrent chat requests. Measured are total throughput (Σ t/s),
  throughput per user, time to the first token (TTFT p50/p95) and, via a code word, whether answers are
  mixed between slots ("mix-up", a known gfx1151 bug that the built-in patch #25992 fixes). MTP is off by
  default in the multi-user test (not validated for multiple slots on this architecture), can be switched on.
  Without the TUI: `./run.sh bench-parallel --users 8 [--levels 1,2,4,8] [--preset …] [--keep-mtp]`.
  Results land in `state/bench/results.jsonl`.
- **Running the server for multiple users**: set the field "Slots (-np)" to N; `-c` is then the total context (N × context
  per slot, e.g. 8 × 16384 = 131072). The recurrent state costs ~113 MiB per slot, the KV cache stays the same size.
  **Turn MTP off for this**: measured 8 users 50 t/s without vs 35 t/s with MTP (IQ4_XS/Q4_K_XL, EngramHalo).
- **System**: hardware, memory (RAM/VRAM/GTT), governor/tuned profile, kernel parameters, other LLM processes – with
  concrete commands if something is not set optimally.
- **F9** exports a standalone start script (`scripts/start-<profile>.sh`) plus a systemd user unit.
- **Ctrl+S** saves the current configuration (`state/current.json`); `./run.sh run` starts it without the TUI,
  `./run.sh show` shows only the command + memory balance.

## Memory – the most important thing on this machine
Everything (weights, KV cache, compute) lies in the same 128 GB RAM (16 GiB VRAM carve-out + GTT). The kernel OOM killer
hits the server when `MemAvailable` approaches 0 – GTT memory does **not** show up in the RSS of the process.

- The model contains a **26.8 GiB per-layer embedding table** (`per_layer_token_embd`). In load mode `auto`
  ROCm uses no mmap → the table is copied completely into a CPU buffer (**≈28 GiB RAM in addition to the
  GTT weights**). With `--load-mode mmap` it stays lazy (CPU_Mapped, page cache), but the stock fork then loads the
  weights page by page at ~18 MB/s (UD-Q4_K_XL: 140 minutes measured). **EngramHalo** (engine "hip-engramhalo")
  makes the SSD mode practical (readahead + drop-behind): `-lm mmap --tensor-read-lazy on` ≈ 1.5 GiB resident.
  On the stock fork, therefore, **UD-Q4_K_XL + MTP does not fit**; UD-IQ4_XS + MTP fits (~93 GiB). **EngramHalo** keeps the
  table lazy even with `-lm none` (measured 2.7 GiB RSS) → UD-Q4_K_XL + MTP = ~85 GiB, load 28 s.
- Resident are: experts + attention/DeltaNet weights (Q2_K_XL ≈ 47 GiB, IQ3_XXS ≈ 50, IQ4_XS ≈ 60, Q4_K_XL ≈ 77 GiB),
  KV cache of the 12 full-attention layers (f16: 24 KiB/token → 3 GiB at 128k; q8_0 ≈ 13 KiB/token), indexer cache
  (3 KiB/token), compute buffer (logits over 248k vocabulary × ubatch), MTP head (2.5 GiB).
- The **memory guard** stops the server hard when less than N GiB are free (field "Protection").

## Parameter quick reference
| Field | Flag | Recommendation |
| --- | --- | --- |
| Quant | `-m` | UD-Q4_K_XL (best quality; with EngramHalo also with MTP: 35 t/s, 85 GiB), IQ4_XS 36.5 t/s / 69 GiB, IQ3_XXS 34 t/s / 57 GiB |
| Context | `-c` | 131072 standard; 262144 possible (KV q8_0 ≈ 3.3 GiB) |
| KV cache | `-ctk/-ctv` | q8_0 (no measurable speed difference, half the memory); rotation stays on (env variable not needed) |
| Flash Attention | `-fa on` | always on |
| µBatch | `-ub` | 512; 2048 brings < 3 % on prompt processing |
| Threads | `-t` | 16 (physical cores) |
| MTP | `--spec-type draft-mtp[,ngram-mod] -md … --spec-draft-n-max 3–4 --spec-draft-p-min 0.75` | only the dzannotti head fits (`output_hc_*`); the unsloth head needs the unsloth fork. The speedup depends on the acceptance; temperature > 0 lowers it |
| Engine | – | `hip-engramhalo` (Strix Halo fork: HIP top-k, sparse QSA gather, SSD mode) or `hip-own`/`hip-user` (stock fork + MTP patch) |
| EngramHalo tuning | `-lm none` or `-lm mmap`, `-b 8192 -ub 2048 -t 4`, `ROCBLAS_USE_HIPBLASLT=1` | recommendation of the fork author; cross-check in the Benchmark tab |
| Thinking | `--chat-template-kwargs '{"reasoning_effort":"…"}'` | xhigh (template default), medium, low; `enable_thinking:false` turns it off |
| Sampling | `--temp 1.0 --top-p 0.95 --top-k 20 --min-p 0` | Qwen recommendation (stored in the GGUF) |
| Prompt cache | `--cache-ram` | 8192 MiB default; -1 = unlimited (OOM risk) |

## Typical failure modes
- *Server aborts during loading, log mentions `self_k_rot`/GGML_ASSERT*: old fork state; here b10685+patch and EngramHalo load with active rotation. If need be, field "Protection" → LLAMA_ATTN_ROT_DISABLE `on`.
- *Loading takes hours*: `--load-mode mmap` on the stock fork (page faults without readahead) → load mode `auto` or engine EngramHalo.
- *MTP head does not load ("missing tensor output_hc_norm")*: unsloth head chosen; take the dzannotti head (`auto`).
- *`Unexpected reasoning effort`*: the chat template only knows xhigh/medium/low.
- *Kernel OOM*: check the memory balance on the right (headroom ≥ 8 GiB), choose a smaller quant/context or the EngramHalo SSD mode, terminate other LLM processes (ollama, LM Studio).
- *MTP is ignored*: engine without the qwen4exp MTP patch chosen (the builds from `engine/` have it; a foreign llama.cpp build usually does not).
