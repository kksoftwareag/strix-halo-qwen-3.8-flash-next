# Qwen3.8-Flash-Next on Strix Halo – research (as of 2026-09-03)

Compiled from official sources (Qwen model card, unsloth docs), llama.cpp PRs/issues, community reports on Strix Halo
and own measurements on this machine (Ryzen AI MAX+ 395, 109.7 GiB usable RAM, ROCm/HIP 7.1, Fedora 44). Own
measurements are marked as such. Sources: numbered list at the end.

## 1. Model facts

- **Architecture** (`qwen4exp`, "A Preview of the Qwen4 Architecture"): 125B parameters, 6B active, plus 51B n-gram
  embedding (PLE) and 4B MTP head [1][2]. 48 layers = 12 × (3 gated DeltaNet + 1 Qwen sparse attention); only the 12
  full-attention layers have a KV cache (24 Q heads, 2 KV heads, head_dim 256, RoPE on 64 dims), plus an indexer
  (4 heads, 128 dims, budget 2048, compress ratio 4). 512 experts, 10 routed + 1 shared, expert FFN 640.
  Hyper-connections (4 streams, low-rank 320). Vocabulary 248,320 [2].
- **PLE / n-gram table**: one PLE layer (layer 2), trigrams, 20M entries × 8 heads → tensor `per_layer_token_embd`
  160 × 320,001,536, identical in all unsloth quants at **26.8 GiB IQ4_NL** (own GGUF analysis). Unsloth deliberately
  keeps it ≥ 4 bit [4].
- **Context**: natively 262,144 tokens, up to 1M via static YaRN (factor 4) [1].
- **Thinking**: on by default. The chat template accepts `enable_thinking` (default true), `preserve_thinking` and
  `reasoning_effort` with **exactly** `xhigh` (default), `medium`, `low` – any other value throws a template exception
  (own check of the GGUF template) [1].
- **Official sampling values** [1][4]:
  - Thinking: temp 1.0, top_p 0.95, top_k 20, min_p 0, presence 0, repeat 1.0 (stored in the GGUF).
  - Non-thinking: temp 0.7, top_p 0.80, top_k 20, min_p 0, presence 1.5.
  - For agent tasks Qwen recommends up to 262k reasoning and 131k answer tokens; a lower effort does not always
    shorten agent runs. One community setup uses `--reasoning-budget 4000` with `medium` [5].
- **Tool calls**: XML format `<tool_call><function=…><parameter=…>…` (vLLM: `--tool-call-parser qwen3_coder`) [3].

## 2. Quant quality (unsloth KLD table [4]) and how much of it is resident

| Quant | File (GiB, measured) | of which experts | resident without PLE | KLD | Top-1 |
| --- | --- | --- | --- | --- | --- |
| UD-IQ1_M | 69.4 | 39.0 | 42.7 | 0.3147 | 79.7 % |
| UD-Q2_K_XL | 73.4 | 42.9 | 46.6 | 0.2246 | 82.7 % |
| UD-IQ3_XXS | 76.3 | 45.3 | 49.5 | 0.1651 | 85.4 % |
| UD-IQ4_XS | 87.2 | 55.4 | 60.4 | 0.0836 | 89.6 % |
| UD-Q4_K_XL | 103.7 | 71.7 | 76.9 | 0.0469 | 92.3 % |

The quants differ solely in the precision of the routed experts; attention/DeltaNet/shared experts stay Q5_K–Q8_0.
Unsloth names UD-Q2_K_XL as the lower bound for tool calling/agents [4].
KV cache: q8_0 K+V is practically lossless (KLD 0.0018), q4_0 for K destroys the quality (KLD 5.5) [7].

## 3. llama.cpp status

- Base architecture upstream since 2026-08-27 (PR #27742), follow-up fixes #27880, #27941, and **#28123 (native
  recurrent-state rollback, 2026-09-01)** [8]. The local fork `~/models/llama.cpp-mtp` (b10685, 17252c769) does **not**
  contain #27941/#28123; without the rollback, the recurrent state is written to host memory on every speculation
  round (on Vulkan the reason for 21 → 5 t/s; on HIP "works cleanly", but measurable).
- **MTP not merged upstream**: PR #27836 (draft) and PR #28243 (unsloth, "shared" heads) are open [9][10].
  The local patch ports the graph from #27739 (dzannotti). Consequence for the heads:
  - `dzannotti/…-MTP-Q4_K_M.gguf` (2.44 GiB): tensor names `output_hc_*` → **matches** the local loader.
  - `unsloth/…/MTP/mtp-…-Q4_K_M.gguf` (2.59 GiB): tensor names `blk.48.nextn.hc_head_*` → **needs the unsloth fork**
    (b10715-mix) and does not load here (own GGUF check, unsloth README [10]).
- Flags (verified in `common/arg.cpp`): `--spec-type` (comma-separated: draft-mtp, ngram-mod, …), `--spec-draft-n-max`
  (default 3), `--spec-draft-n-min` (0), `--spec-draft-p-min` (0.0; stops the drafting as soon as the top-1 probability
  of the head falls below it – changes only speed, never the output), `-md`, `-ngld`, `--cache-ram` (8192 MiB; under
  Linux overcommit the upper limit is practically ineffective, issue #22629), `--tensor-read-lazy` (auto = lazy for
  tensors > 4 GiB, **only with mmap**), `--load-mode`.
- **MTP + ngram-mod can be combined** (`--spec-type draft-mtp,ngram-mod`): n-gram drafts take precedence, no
  chaining [11].
- **Temperature lowers the acceptance**: the verification samples with the full sampler; all published speedups are
  greedy [10][12].
- **LLAMA_ATTN_ROT_DISABLE=1 is no longer needed**: the assert that aborted the load with quantized KV existed only
  in the pre-merge revision of #27742; the local tree rotates Q/K/V itself (`qwen4exp.cpp:808ff`). **Own measurement**
  (Q2_K_XL, q8_0 KV, 32k): load without the variable ok (`attn_rot_k = 1, attn_rot_v = 1`), tg 24.2 t/s instead of
  24.6 t/s (−2 %), in exchange better quality of the quantized KV (PR #21038). The TUI leaves the rotation on.
- `GGML_HIP_ROCWMMA_FATTN` no longer exists in this llama.cpp version (cmake option removed) – and was harmful on
  Strix Halo anyway (pp −77 % at 30k depth) [13].
- **Never set GGML_HIP_ENABLE_UNIFIED_MEMORY=1**: 76.9 GB anonymous RSS instead of GTT [14].

## 4. Memory on this machine (own measurements, bench/results/mem)

- Everything shares 109.7 GiB: GTT (weights, KV, compute) + host RAM. GTT does **not** show up in the RSS;
  `MemAvailable` is the only reliable figure → `bench/memguard.py` and the guard in the TUI.
- Load mode `auto` (llama default): ROCm reports "no mmap" → the 26.8 GiB embedding table is copied into a **CPU buffer
  (28 GiB anonymous)**. Footprint = resident weights + 28 GiB + KV/compute + MTP. Q2: 47.4 GTT + 28 RSS = 75.7 GiB
  (measured). **UD-Q4_K_XL + MTP → 76.4 + 28 + 2.5 + … > 107 → kernel OOM** (happened twice).
- `--load-mode mmap`: lazy takes effect ("lazy read enabled", `CPU_Mapped`), footprint Q2 only 48 GiB. **But** the
  weight upload runs over page-by-page page faults without readahead: Q4_K_XL took **140 minutes** (18 MB/s, 149 GB
  read); Q2 with a warm page cache 14 s. On the stock fork, mmap is only usable if the weight shards are already in the
  page cache.
- **EngramHalo.cpp** [15] solves exactly that: readahead hints for the Engram rows, `LLAMA_MMAP_DROP_BEHIND` (release
  the page cache behind the upload), HIP top-k kernel (fixes the CPU fallback from ~1k context on), FA vector kernel,
  sparse QSA gather from 16k on. Measured (IQ3_XXS, q8_0 KV, temp 0): code decode 24.4 → 39.3 t/s (RAM mode) / 35.3
  (SSD mode), prose 22.4 → 25.3, code @78k 10 → 21–25 t/s, pp4096 352 → 496. Independent reproduction on 128 GB:
  HIP+MTP 66 t/s code (q8_0 KV) and 82 t/s (f16 KV), prose ~22 [14]. Recommended flags:
  `ROCBLAS_USE_HIPBLASLT=1 … -lm none -b 8192 -ub 2048 -t 4
  --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75`; SSD mode: `-lm mmap --tensor-read-lazy on`.

## 5. Strix Halo tuning

- **ROCm/HIP vs Vulkan**: HIP wins prompt processing (+20 %), Vulkan often decode (+10–25 %) [16] – but with MTP,
  Vulkan on this architecture without on-device checkpoints is a loss (21 → 5 t/s) [9]; HIP is the right choice (agrees
  with the user's assessment). The Vulkan dev headers are missing on the system anyway.
- Own llama-bench figures (HIP, -fa on, without MTP): Q4_K_XL pp512 ≈ 410–420 t/s, tg128 ≈ 21 t/s; Q2_K_XL pp ≈ 395,
  tg ≈ 24.5 t/s; KV q8_0 vs f16 and ub 512 vs 2048 without any notable difference at 512 tokens.
- Community MTP figures with the dzannotti head (n3/p0.75, q8_0 KV): ROCm Q4_K_XL 20.3 → 35.8 t/s code / 22.6 prose
  (acceptance 0.90/0.74); IQ4_XS 18 → 32.8/22.1 [12]. On bandwidth-limited hardware a small draft depth wins
  (n2–n4); n16/p0.8 is a 5090 recommendation, not transferable [17].
- KV cache: q8_0 (avoid bf16 KV: at hd 256 the FA path converts the whole cache) [15]; at depth, q8_0 is faster than
  f16 (30 vs 17 t/s @32k on GPU) [18].
- Kernel/host: `amd_iommu=off amdgpu.gttsize=126976 ttm.pages_limit=32505856` are set; AMD recommends a small BIOS VRAM
  carve-out (0.5 GB) in favor of GTT [19]; tuned `accelerator-performance` or governor `performance` (currently
  powersave/balanced – see System tab).
- `--fit` (on by default, 1024 MiB margin) never shrinks an explicitly set `-c`; on HIP it sees the memory situation
  only through `hipMemGetInfo` [20].

## 6. Alternatives to llama.cpp – conclusion

Nothing else runs today on a single Strix Halo with this model: vLLM validates only MI355X, all vLLM checkpoints
(FP8 173 GiB, AWQ 168 GiB, NVFP4 126 GiB) leave the 51B n-gram table in BF16 and do not fit [21]; SGLang rejects
gfx1151; ik_llama.cpp has qwen4exp+MTP, but ROCm/Vulkan are "unsupported" there; Ollama ships only MLX tags;
LM Studio and Lemonade wrap upstream llama.cpp without MTP. The real competition are the Strix Halo forks
(EngramHalo.cpp, kyuz0 container `rocm-10.0-qwen-3.8-flash-next`, LaurentZuijdwijk `vulkan/qwen4exp-rocmfpx`).
ROCmFP4 quants are optional (quality unmeasured).

## 7. Own measurements (2026-09-03, 32k context, q8_0 KV, dzannotti head, prompt "Count 1–30 + KV cache explanation", 300 tokens)

| Engine | Quant | MTP | Load | tg | Acceptance | Footprint (MemAvailable Δ) |
| --- | --- | --- | --- | --- | --- | --- |
| Stock fork (auto) | Q2_K_XL | – | 20 s | 24.6 t/s | – | 75.7 GiB |
| Stock fork (auto) | Q2_K_XL | n3/p0.75 | 22 s | 34.8 t/s | 86 % | 78.8 GiB |
| Stock fork (auto) | IQ3_XXS | n3/p0.75 | 23 s | 35.1 t/s | 88 % | 81.5 GiB |
| Stock fork (auto) | IQ4_XS | n3/p0.75 | 26 s | 34.2 t/s | 87 % | 92.7 GiB |
| Stock fork (auto) | Q4_K_XL | n3/p0.75 | – | **OOM** | – | > 107 GiB |
| Stock fork (mmap) | Q4_K_XL | – | **140 min** | – | – | 30 GiB free, but unusable |
| EngramHalo (-lm none) | IQ3_XXS | – | 17 s | 23.1 t/s | – | 52.8 GiB |
| EngramHalo (-lm none) | IQ3_XXS | n4/p0.75+ngram | 16 s | 34.4 t/s | 79 % | 57.4 GiB |
| EngramHalo (-lm none) | IQ4_XS | n4/p0.75+ngram | 20 s | 36.5 t/s | 84 % | 68.7 GiB |
| EngramHalo (-lm none) | **Q4_K_XL** | n4/p0.75+ngram | 28 s | **35.3 t/s** | 80 % | **84.7 GiB** |
| EngramHalo (-lm mmap) | Q4_K_XL | n4/p0.75+ngram | 39 s | 35.5 t/s | 80 % | 83.4 GiB (RSS 57 GiB = mapped, evictable pages) |

**MTP fine-tuning** (EngramHalo, UD-Q4_K_XL, `-lm none`, 32k, q8_0 KV, reasoning medium, 3 prompts of 400 tokens each, temp 1.0 unless stated otherwise):

| Configuration | tg avg | Code | Prose | Reasoning | Acceptance |
| --- | --- | --- | --- | --- | --- |
| without MTP | 20.8 | 20.8 | 20.8 | 20.9 | – |
| n2 / p0.75 | 30.9 | 30.7 | 28.2 | 33.8 | 85 % |
| n3 / p0.75 | 33.9 | 33.1 | 29.7 | 38.9 | 83 % |
| **n4 / p0.75 + ngram-mod** (preset) | 34.7 | 32.1 | 31.2 | 41.0 | 80 % |
| n4 / p0.0 | 36.0 | 32.5 | 31.1 | 44.5 | 55 % |
| n6 / p0.75 + ngram-mod | 35.7 | 34.9 | 30.9 | 41.3 | 76 % |
| n3 / p0.75, temp 0.6 | 35.3 | 36.1 | 30.4 | 39.5 | 86 % |
| n3 / p0.75, temp 0.0 | 35.8 | 36.2 | 30.8 | 40.3 | 87 % |

Conclusion: MTP brings 1.5–2.1× depending on the kind of text (reasoning outputs the most); between n3 and n6, or
p0.0 and p0.75, there are only ~5 % (measurement noise ~3 %). Temperature 1.0 (Qwen recommendation) costs only ~5 %
acceptance compared to greedy.
**Multi-user** (EngramHalo, UD-IQ4_XS, `-np 8`, 20480 context per slot, q8_0 KV, without MTP, 256 tokens per request, patch #25992 active):

| concurrent users | Σ throughput | per user | TTFT p50 | mix-ups |
| --- | --- | --- | --- | --- |
| 1 | 20.4 t/s | 21.4 t/s | 0.6 s | 0 |
| 2 | 32.0 t/s | 17.2 t/s | 0.9 s | 0 |
| 4 | 42.4 t/s | 11.6 t/s | 1.8 s | 0 |
| 8 | 50.4 t/s | 6.8 t/s | 2.7 s | 0 |

**Measured with long prompts (2026-09-05, UD-IQ4_XS, ~16k prompt tokens per user, 2k output, MTP on):**

| Slots | Prompt tokens | generated tokens | Duration | Total tokens/s | per request | Draft acceptance | clean answers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 16,253 | 1,130 | 86 s | 203 | 29.9 t/s | 0.70 | 1 of 1 |
| 2 | 32,624 | 1,192 | 141 s | 240 | 14.2 t/s | 0.69 | 2 of 2 |
| 4 | 65,144 | 3,378 | 307 s | 223 | 6.5 t/s | 0.71 | 4 of 4 |
| 8 | 130,457 | 7,011 | 678 s | 203 | 2.8 t/s | 0.60 | **2 of 8** |

Two results: **parallelism brings nothing with long prompts** — the total throughput of prompt and
output tokens stays between 203 and 240 t/s across all levels, while the individual answer drops from 29.9 to 2.8 t/s.
With short prompts the throughput rises with the number of slots (20 → 50 t/s, table above), because the machine has
idle time between the tokens; with long prompts it is already saturated by a single stream.

And **with eight slots the output breaks**: only two of eight users reproduce the given code word correctly,
two answers stay empty, one repeats the prompt, three corrupt the code word by one or two
characters. There is no real cross-talk between slots (no foreign code word in an answer) — the damage
arises within the answer, as described in issue #27572. Up to four slots everything is clean.

Operating recommendation: long context → one slot; multiple slots only for chat with short prompts. The fix
(`engine/patches/0003-27311-uma-ring-buffer.patch`) is ready, but not built — it would fix the broken
answers, not the missing throughput gain. Analysis: `bench/analyze_multiuser.py`.

**Draft head and context depth (2026-09-07, UD-IQ4_XS, `-np 1`, temp 1.0, 600 output tokens).** The 40 t/s from the
short benchmarks are real, but they only hold at an empty context:

| Draft head | Size | ~0 context | 4k | 8k | 30k | 64k |
| --- | --- | --- | --- | --- | --- | --- |
| dzannotti Q4_K_M | 2.44 GiB | **40.9** (0.90) | **36.6** (0.84) | **32.2** (0.81) | 26.8 (**0.62**) | **20.5** (0.61) |
| Q8_0, quantised here | 3.85 GiB | 36.5 (0.84) | 32.6 (0.83) | 30.4 (0.78) | **29.0** (**0.83**) | 20.0 (**0.76**) |
| dzannotti BF16 | 7.24 GiB | 29.4 (0.77) | – | – | 25.5 (0.82) | – |

Decode in t/s, draft acceptance in brackets. The crossover sits between 8k and 30k tokens: the small head leads by
4.4 t/s at an empty context, by 4.0 at 4k, by 1.8 at 8k, and trails by 2.2 at 30k. Its acceptance holds up to 8k
(0.81) and then collapses to 0.62, while the Q8_0 head stays near 0.83. Each point is a single measurement at
`temp 1.0` on one kind of task, so treat differences below about 1 t/s as noise.

Two effects overlap. Up to about 8k the loss is mostly the more expensive attention and indexer, which run over the
whole context; beyond that the small head's draft acceptance collapses on top of it, which is why the Q8_0 head wins
at depth despite costing more per draft step. BF16 is bigger and slower at every depth, as the unsloth documentation
says.

**At 64k the head no longer matters (2026-09-08).** Both heads land at 20.0 to 20.5 t/s — a difference of 0.5 t/s,
which is inside the noise. The Q8_0 head keeps its better acceptance there (0.76 against 0.61), but that no longer
buys speed: at this depth every accepted draft token still has to be verified against 64k of context, and attention
plus indexer dominate the step so completely that the cheaper draft step and the higher hit rate cancel out. So the
Q8_0 head's advantage is a band around 30k, not a trend that keeps growing. Prompt processing also slows down with
depth: 318 t/s at 30k against 261 t/s at 64k, which is why time to first token grows from 94 to 246 seconds —
four minutes of waiting before the first token of the answer.

One caveat from the same runs: the benchmark plants a code word in the filler text and checks whether the answer
repeats it. Up to 30k every run reproduced it; at 64k neither head did. That is a single prompt shape and no
substitute for a recall benchmark, but it fits the model card, which states 262144 tokens of training context while
the useful working depth is far shorter.

That explains the agent runs: their contexts grow to tens of thousands of tokens, and 21.9 to 24.4 t/s is what this
machine delivers there. Nothing is broken.

The Q8_0 head is not published; build it from the BF16 head:

```bash
hf download dzannotti/Qwen3.8-Flash-Next-MTP-GGUF Qwen3.8-Flash-Next-MTP-BF16.gguf
engine/build-engramhalo/bin/llama quantize <BF16 file> state/mtp/Qwen3.8-Flash-Next-MTP-Q8_0.gguf Q8_0 8
```

Anything in `state/mtp/` is picked up automatically. All EngramHalo presets ask for the Q8_0 head and fall back to the Q4_K_M head when it is absent. That is a deliberate simplification: below roughly 8k tokens of context the small head is about 4 t/s faster, so `eh-schnell` gives up a little. Automatic selection picks the smallest compatible head, so a BF16 head lying around is never chosen by accident.

**The two qwen4exp commits from master (#28123, #28023) are already in EngramHalo** — the fork carries the same
recurrent-state rollback (`[TAG_RECURRENT_ROLLBACK_SPLITS]`) and the same sliced indexer sum, with the same reasoning
in the comments. `engine/fetch.sh` reports patch 0005 as "already contained" and changes nothing; it is only relevant
for a stock llama.cpp build.

**Parallelism limits per quant.** `-c` is the total context across all slots; with `-np 4 -c 262144` each
slot gets 65536 tokens. Two figures matter: KV and indexer cache at **17,952 bytes per token** (0.55 GiB per 32k, the
same for all quants, because only 12 of the 48 layers have attention and the KV type is q8_0) and the DeltaNet state at
**113 MiB per slot**, independent of the context length. The context of a single slot is limited by the training length
to 262144 tokens, not by the memory — these 256k fit with every quant, even with UD-Q4_K_XL
(94.1 GiB used, 6.4 GiB headroom).

Maximum number of concurrent contexts of the given size (with MTP / without MTP), computed with `bench/context_limits.py`
on the program's memory model for 106.5 GiB free memory, prompt cache 2 GiB, ubatch 2048, 6 GiB reserve; truncated at 64:

| Quant | weights resident | 16k per slot | 32k | 64k | 128k | 256k |
| --- | --- | --- | --- | --- | --- | --- |
| UD-IQ1_M | 45.2 GiB | 64 / 64 | 64 / 64 | 37 / 42 | 19 / 22 | 10 / 11 |
| UD-Q2_K_XL | 49.2 GiB | 64 / 64 | 63 / 64 | 34 / 39 | 18 / 20 | 9 / 10 |
| UD-IQ3_XXS | 52.1 GiB | 64 / 64 | 59 / 64 | 32 / 37 | 17 / 19 | 8 / 9 |
| UD-IQ4_XS | 63.0 GiB | 64 / 64 | 44 / 51 | 23 / 27 | 12 / 14 | 6 / 7 |
| UD-Q4_K_XL | 79.5 GiB | 27 / 37 | 16 / 21 | 8 / 11 | 4 / 6 | 2 / 3 |

In practice, with the small quants the limit is not the memory but the throughput: with 8 slots there remain
6.8 t/s per request (see table above). That is enough for chat, not for agents — an agent with 30000 output tokens
then waits 74 instead of 25 minutes. That is why the agent benchmarks run with one slot. On top of that: MTP only pays
off with one slot (with 8 slots 35 instead of 50 t/s), and multiple slots need the patch from issue #25992 on gfx1151.

With MTP (UD-Q4_K_XL, n4/p0.75+ngram, otherwise identical): 1 user 35.9 t/s (acceptance 82 %), 2 users Σ 30.8,
4 users Σ 35.5, 8 users Σ 34.8 t/s (acceptance 59–66 %). **MTP only pays off for a single user**; from 2 concurrent
requests on, continuous batching without a draft is ahead (with 8 users 50 vs 35 t/s).
Continuous batching scales up to 8 users to 2.5× the single-user throughput; per user ~7 t/s remain at 8.
Without the #25992 patch (pinned host buffers on the iGPU), mixed-up answers between slots are reported on gfx1151;
with the patch no mix-up occurred in 15 requests.
Rotation on vs off (stock, Q2, without MTP): 24.2 vs 24.6 t/s → the rotation stays on.
Measured buffers (HIP): compute 297 MiB @ub 512 and 1188 MiB @ub 2048 (+121/233 MiB host); context 32k q8_0 = 673 MiB
(KV 408 + indexer 153 + RS 113); MTP draft 2146 MiB + 740 MiB compute. The estimator in the TUI is calibrated to this.

## 8. Concrete recommendation (presets in the TUI)

1. **Standard: EngramHalo + UD-Q4_K_XL + MTP** (`eh-qualitaet`): `-lm none`, `-b 8192 -ub 2048 -t 4`, `ROCBLAS_USE_HIPBLASLT=1`,
   `--spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75`, 128k context, q8_0 KV, ~22 GiB headroom.
2. Faster/smaller: `eh-schnell` (IQ3_XXS) or IQ4_XS; 160k context: `eh-longctx` (IQ4_XS).
3. Fallback without EngramHalo: stock fork with IQ4_XS + MTP (n3/p0.75), never Q4_K_XL with MTP.
4. Thinking: `medium` for everyday use, `xhigh` only when needed (token consumption); non-thinking sampling temp 0.7/top_p 0.8/presence 1.5.

## 9. Open points (to be resolved by benchmark in the TUI)

- Acceptance/speedup of MTP with Qwen sampling (temp 1.0) instead of greedy; best n_max/p_min point per quant.
- Rotation on (without env) vs off: load behavior and tg cost.
- EngramHalo: is the dzannotti head compatible? EasiiX Q8_0 sidecar (4.1 GB) with higher acceptance [15].
- Whether the rollback of the recurrent state (#28123) lowers the MTP cost. The commit landed in master on 2026-09-04
  and is ready as `engine/patches/0005-qwen4exp-upstream-28123-28023.patch` (together with #28023,
  a faster indexer sum). From the commit description: without the rollback, llama.cpp classifies the context as
  `SEQ_RM_TYPE_FULL` and writes the **entire recurrent state to host memory on every MTP round**,
  "which costs more than the drafting saves". Both commits can be transferred cleanly onto our state
  (EngramHalo via a three-way merge). Off by default, because unmeasured; `ENGINE_QWEN4EXP_PATCH=1` turns them on.
  Careful: [Issue #28019](https://github.com/ggml-org/llama.cpp/issues/28019) reports, with the rollback enabled,
  damage to the recurrent state with multiple sequences — with one slot presumably uncritical, but unverified.
- The MTP draft head is still not in master (as of 2026-09-06, 141 commits after our base commit);
  patch 0001 remains necessary. The EngramHalo fork stands unchanged at `60bce1a` from 2026-09-03.

**MTP with multiple slots (prepared, measurement still pending).** With `-np N` and prompts from about 19000 tokens and
several ubatches, the draft acceptance falls to 0.0, and MTP becomes slower than no MTP —
[Issue #27572](https://github.com/ggml-org/llama.cpp/issues/27572), reported on gfx1151/ROCm with a hybrid of
gated DeltaNet and attention. The cause is a write-after-read race on unified memory; the fix is
[PR #27311](https://github.com/ggml-org/llama.cpp/pull/27311) ("Scheduler UMA ring buffer"), measured there on Strix Halo:
acceptance at `-np 8` 0.5083 with the ring versus 0.0 without, sanitizer races 0 versus 3597, throughput cost below 1 %.

Our measurement from 2026-09-04 did not hit the bug: `-np 8` with `draft-mtp,ngram-mod`, but only a 71-token prompt —
16 acceptance measurements between 0.46 and 1.00, no zero value. The collapse needs long prompts.

Both are prepared: the 18 commits of the PR are transferred onto our base commit and are available as
`engine/patches/0003-27311-uma-ring-buffer.patch` (directly applicable to the stock fork, to EngramHalo via a
three-way merge, both verified); in addition `0004-28433-draft-ctx-per-seq.patch`, which sizes the draft context from
`llama_n_ctx_seq()` instead of `llama_n_ctx()` ([Issue #28433](https://github.com/ggml-org/llama.cpp/issues/28433)).
`engine/fetch.sh` leaves both out by default, `ENGINE_RING_PATCH=1` turns them on — this way a
fresh build corresponds exactly to the one all measurements here were made with. The measurement series for it is
`bench/mtp_multiuser.sh` (1/2/4/8 users, 15k prompt per user, 2k output, MTP on) — once with the existing
builds as a comparison value, then after the rebuild, each over UD-IQ4_XS, UD-IQ3_XXS, UD-Q2_K_XL and UD-IQ1_M.
UD-Q4_K_XL is not preset, but also fits with eight slots.

## Sources
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
15. https://github.com/Aristo94/EngramHalo.cpp (branch strix-halo-qwen4exp, docs/strix-halo/README.md)
16. https://www.soothill.io/blog/2026/08/03/llamacpp-vulkan-vs-rocm-strix-halo/
17. https://github.com/ggml-org/llama.cpp/discussions/25198
18. https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF/discussions/3
19. https://rocmdocs.amd.com/en/develop/how-to/system-optimization/strixhalo.html
20. https://github.com/ggml-org/llama.cpp/issues/23472
21. https://recipes.vllm.ai/Qwen/Qwen3.8-Flash-Next
22. https://github.com/ggml-org/llama.cpp/pull/28136 (`--lazy-mode on-direct`, open)
23. https://github.com/kyuz0/amd-strix-halo-toolboxes
