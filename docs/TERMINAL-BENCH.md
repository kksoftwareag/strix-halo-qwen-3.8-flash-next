# Terminal-Bench-Mini-20: results

As of 2026-09-07. Agent benchmark with 20 tasks from Terminal-Bench 2.1 on this machine, one quant after another. Setup and usage: [`bench/quality/README.md`](../bench/quality/README.md), context in [`QUALITY-BENCHMARKS.md`](QUALITY-BENCHMARKS.md).

## Result

| Quant | pass@1 | pass@2 | pass@3 | Duration | avg per task | median | output tokens | tokens/s over the run | KLD | top-1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UD-IQ1_M · medium | 15/20 | **19/20** | **20/20** | 8 h 16 min | 24:49 | 20:50 | 459,008 | 15.4 | 0.3147 | 79.7% |
| UD-Q2_K_XL · medium | 16/20 | **18/20** | 18/20 | 7 h 36 min | 22:48 | 17:42 | 385,970 | 14.1 | 0.2246 | 82.7% |
| UD-IQ3_XXS · medium | 15/20 | **18/20** | 18/20 | 6 h 27 min | 19:22 | 16:32 | 273,296 | 11.8 | 0.1651 | 85.4% |
| UD-IQ4_XS · medium | 15/20 | **18/20** | 18/20 | 6 h 57 min | 20:53 | 12:37 | 343,555 | 13.7 | 0.0836 | 89.6% |
| UD-IQ3_XXS · xhigh | 15/20 | 15/20 | 15/20 | 23 h 7 min | 1:09:23 | 47:33 | 1,043,209 | 12.5 | 0.1651 | 85.4% |

pass@2: a second attempt with 5400 s instead of 3600 s has run for 19 of the 24 failed tasks so far; for the rest, pass@2 = pass@1.
pass@3 counts a third attempt with 10800 s, run only for the tasks that hit the time limit in the second attempt as well.

“Avg per task” and “median” refer to the first round and count the full time per task: container setup, the agent's work and the verifier.

## Tasks in detail

| Task | Category | Difficulty | UD-IQ1_M · medium | UD-Q2_K_XL · medium | UD-IQ3_XXS · medium | UD-IQ4_XS · medium | UD-IQ3_XXS · xhigh |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `pypi-server` | software-engineering | medium | **yes** (3:08) | **yes** (3:53) | **yes** (3:42) | **yes** (10:09) | **yes** (16:38) |
| `nginx-request-logging` | system-administration | medium | **yes** (2:32) | **yes** (4:08) | **yes** (2:53) | **yes** (3:18) | **yes** (10:36) |
| `git-leak-recovery` | software-engineering | medium | **yes** (2:25) | **yes** (2:55) | **yes** (2:29) | **yes** (8:52) | **yes** (4:41) |
| `fix-git` | software-engineering | easy | **yes** (4:31) | **yes** (3:30) | **yes** (3:21) | **yes** (2:57) | **yes** (7:12) |
| `cobol-modernization` | software-engineering | easy | **yes** (16:30) | **yes** (9:36) | **yes** (16:32) | **yes** (13:31) | time limit (3:00:34) |
| `regex-log` | data-processing | medium | time limit (1:00:47) → **yes** (1:12:50) | **yes** (23:15) | **yes** (24:26) | **yes** (11:40) | **yes** (26:55) |
| `headless-terminal` | software-engineering | medium | **yes** (9:48) | **yes** (17:42) | **yes** (6:50) | **yes** (8:39) | time limit (3:00:34) |
| `mailman` | system-administration | medium | **yes** (46:45) | **yes** (44:47) | **yes** (24:55) | **yes** (21:38) | time limit (3:00:30) |
| `fix-ocaml-gc` | software-engineering | hard | **yes** (38:27) | **yes** (41:13) | **yes** (32:03) | **yes** (1:22:10) | **yes** (1:29:37) |
| `break-filter-js-from-html` | security | medium | **yes** (20:50) | **yes** (57:40) | **yes** (35:20) | **yes** (20:35) | **yes** (47:33) |
| `sqlite-with-gcov` | system-administration | medium | **yes** (5:34) | not passed (8:22) → **yes** (6:49) | **yes** (6:45) | **yes** (8:14) | **yes** (12:36) |
| `sparql-university` | data-querying | hard | **yes** (34:10) | not passed (15:21) → **yes** (11:45) | **yes** (17:45) | **yes** (12:37) | **yes** (38:52) |
| `llm-inference-batching-scheduler` | machine-learning | hard | time limit (1:00:30) → time limit (1:30:35) → **yes** (2:46:33) | **yes** (1:00:30) | time limit (1:00:38) → **yes** (34:04) | time limit (1:03:22) → **yes** (1:30:13) | time limit (3:00:29) |
| `configure-git-webserver` | system-administration | hard | **yes** (10:50) | not passed (6:45) → not passed (3:59) | not passed (6:20) → **yes** (5:12) | **yes** (5:48) | **yes** (54:40) |
| `build-cython-ext` | debugging | medium | **yes** (35:11) | **yes** (30:07) | **yes** (33:24) | **yes** (28:09) | **yes** (1:07:28) |
| `extract-elf` | file-operations | medium | time limit (1:00:29) → **yes** (32:36) | **yes** (26:53) | not passed (9:28) → not passed (22:52) | not passed (17:32) → **yes** (51:04) | **yes** (2:14:06) |
| `build-pov-ray` | software-engineering | medium | not passed (42:18) → **yes** (42:01) | **yes** (1:00:44) | time limit (1:00:46) → **yes** (37:32) | time limit (1:00:48) → not passed (58:11) | **yes** (1:24:57) |
| `openssl-selfsigned-cert` | security | medium | **yes** (3:09) | **yes** (3:48) | **yes** (2:28) | **yes** (6:24) | **yes** (16:42) |
| `overfull-hbox` | debugging | easy | **yes** (21:26) | **yes** (21:15) | **yes** (15:58) | not passed (19:53) → **yes** (38:56) | **yes** (29:48) |
| `mteb-retrieve` | data-science | medium | not passed (16:59) → **yes** (15:02) | not passed (13:36) → not passed (12:06) | not passed (21:15) → not passed (9:35) | not passed (11:26) → not passed (7:57) | not passed (23:19) |

## How to read this

The project the benchmark comes from publishes runs of other models on comparable hardware (Strix Halo, 128 GB): 11 to 18 of 20 tasks — but with **two** attempts per task and a three-hour time limit. The numbers here are measured with one attempt and are therefore on the conservative side.

Two caveats before comparing quants on individual tasks:

- With 20 tasks, the 95% interval around a result is about ±11 percentage points. A difference of one or two tasks between two quants is noise.
- Measurements use `temp 1.0`, so they are not deterministic. In a discarded preliminary run with a 30-minute limit, `configure-git-webserver` passed; in the run that counts, it did not — with an agent that finished after seven minutes, that was not the time limit.

## Throughput and draft acceptance

| Quant | requests | prompt tokens | generated tokens | prompt t/s | decode t/s | MTP acceptance | mean draft length |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UD-IQ1_M · medium | 361 | 332,812 | 459,008 | 216.6 | 26.0 | 0.683 | 3.52 |
| UD-Q2_K_XL · medium | 399 | 404,631 | 385,970 | 243.4 | 24.4 | 0.67 | 3.48 |
| UD-IQ3_XXS · medium | 287 | 301,122 | 273,296 | 252.7 | 25.1 | 0.681 | 3.6 |
| UD-IQ4_XS · medium | 294 | 339,204 | 343,555 | 263.9 | 23.9 | 0.678 | 3.63 |
| UD-IQ3_XXS · xhigh | 355 | 363,937 | 628,279 | 229.8 | 21.3 | 0.71 | 3.19 |

The values come from the server log of each run (all requests the agent made, not only the answers that count towards the score). `Decode t/s` is the pure generation rate, averaged over all requests.

### Speed per task

Output tokens divided by the time the agent actually waited for the model (the sum of all response times). The value is below the pure decode rate because every request also processes the prompt; it says how fast the agent made progress on that task.

| Task | UD-IQ1_M · medium t/s | UD-Q2_K_XL · medium t/s | UD-IQ3_XXS · medium t/s | UD-IQ4_XS · medium t/s | UD-IQ3_XXS · xhigh t/s | UD-IQ1_M · medium model time | UD-Q2_K_XL · medium model time | UD-IQ3_XXS · medium model time | UD-IQ4_XS · medium model time | UD-IQ3_XXS · xhigh model time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pypi-server` | 25.2 | 25.6 | 23.9 | 25.0 | 24.7 | 1:40 | 1:55 | 2:03 | 2:28 | 10:29 |
| `nginx-request-logging` | 29.2 | 25.6 | 27.3 | 26.5 | 26.2 | 1:23 | 2:54 | 1:44 | 1:55 | 7:59 |
| `git-leak-recovery` | 25.4 | 23.6 | 23.6 | 25.6 | 22.2 | 1:40 | 2:06 | 1:43 | 1:42 | 3:22 |
| `fix-git` | 23.1 | 22.6 | 23.9 | 24.4 | 22.7 | 3:49 | 2:48 | 2:35 | 2:16 | 6:17 |
| `cobol-modernization` | 25.2 | 24.2 | 23.1 | 23.3 | 13.8 | 15:39 | 8:46 | 15:00 | 12:25 | 2:20:24 |
| `regex-log` | 5.4 | 15.0 | 15.5 | 27.9 | 24.2 | 49:11 | 21:52 | 23:28 | 8:37 | 25:01 |
| `headless-terminal` | 24.1 | 25.2 | 26.3 | 27.0 | 12.8 | 7:29 | 14:13 | 5:28 | 6:42 | 2:54:53 |
| `mailman` | 21.0 | 19.7 | 11.9 | 22.1 | 19.2 | 40:08 | 30:33 | 21:18 | 14:09 | 2:52:11 |
| `fix-ocaml-gc` | 24.5 | 21.2 | 20.6 | 21.1 | 19.1 | 25:01 | 27:10 | 17:39 | 31:45 | 59:41 |
| `break-filter-js-from-html` | 11.4 | 6.5 | 16.6 | 23.9 | 11.6 | 18:10 | 55:22 | 33:28 | 19:12 | 42:48 |
| `sqlite-with-gcov` | 24.0 | 22.2 | 19.5 | 22.3 | 21.6 | 2:22 | 4:22 | 2:38 | 2:27 | 5:21 |
| `sparql-university` | 19.8 | 27.7 | 26.5 | 25.0 | 23.7 | 30:59 | 11:33 | 12:04 | 6:36 | 30:59 |
| `llm-inference-batching-scheduler` | 19.1 | 21.1 | 6.1 | 19.9 | 6.0 | 58:46 | 54:09 | 52:23 | 57:48 | 2:01:28 |
| `configure-git-webserver` | 24.7 | 23.7 | 20.6 | 26.2 | 21.5 | 7:35 | 5:17 | 3:59 | 3:36 | 27:10 |
| `build-cython-ext` | 22.6 | 20.4 | 20.4 | 22.4 | 19.0 | 22:57 | 15:26 | 17:17 | 14:13 | 35:47 |
| `extract-elf` | 23.3 | 22.7 | 22.4 | 24.5 | 15.6 | 54:39 | 25:53 | 8:52 | 16:44 | 2:07:04 |
| `build-pov-ray` | 19.5 | 17.4 | 18.2 | 17.8 | 18.8 | 18:20 | 33:08 | 27:13 | 37:16 | 47:49 |
| `openssl-selfsigned-cert` | 30.1 | 27.5 | 27.2 | 30.2 | 27.2 | 2:24 | 2:34 | 1:43 | 2:10 | 15:32 |
| `overfull-hbox` | 26.2 | 24.3 | 21.0 | 22.1 | 22.3 | 19:38 | 16:46 | 9:38 | 15:25 | 27:07 |
| `mteb-retrieve` | 24.7 | 23.9 | 22.9 | 25.4 | 22.2 | 8:58 | 4:54 | 11:16 | 3:56 | 10:07 |

- UD-IQ1_M · medium: 5.4 to 30.1 t/s per task, 19.6 t/s across all tasks; the agent waited 6 h 30 min for the model, which is 79% of the run time.
- UD-Q2_K_XL · medium: 6.5 to 27.7 t/s per task, 18.8 t/s across all tasks; the agent waited 5 h 41 min for the model, which is 75% of the run time.
- UD-IQ3_XXS · medium: 6.1 to 27.3 t/s per task, 16.8 t/s across all tasks; the agent waited 4 h 31 min for the model, which is 70% of the run time.
- UD-IQ4_XS · medium: 17.8 to 30.2 t/s per task, 21.9 t/s across all tasks; the agent waited 4 h 21 min for the model, which is 63% of the run time.
- UD-IQ3_XXS · xhigh: 6.0 to 27.2 t/s per task, 15.9 t/s across all tasks; the agent waited 18 h 11 min for the model, which is 79% of the run time.

## How it was run

- Benchmark: Terminal-Bench-Local, Terminal-Bench 2.1 (revision `5c8eadf1f393`), Harbor 0.20.0, Agent Terminus-2
- One attempt per task (pass@1), a single stream (`-np 1`), MTP draft head active, `reasoning_effort: medium`
- Time limit 3600 s per task instead of the 3 hours the benchmark defaults to; for 19 of the 20 tasks that is above the limit the task itself specifies
- Container per task: 1 CPU, 2 GB RAM (only `overfull-hbox`: 2 CPUs, 4 GB)
- Engine: llama.cpp 0.3.0-dev (build 1, commit 60bce1a), backend rocm 7.1.52802, context 163840

### UD-IQ1_M · medium

```bash
ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/38bb39ee97821de2c9009abb7e93950eec396e66/UD-IQ1_M/Qwen3.8-Flash-Next-UD-IQ1_M-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{"reasoning_effort": "medium"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4
```

| Item | Size |
| --- | --- |
| weights (resident) | 45.2 GiB |
| embedding table, lazy (not resident) | 26.8 GiB |
| KV cache (12 attention layers) | 2.0 GiB |
| indexer cache | 0.7 GiB |
| DeltaNet state | 0.1 GiB |
| compute buffer (estimated) | 1.6 GiB |
| MTP head + draft KV | 3.4 GiB |
| prompt cache (max) | 2.0 GiB |
| total | 55.1 GiB |
| available (MemAvailable) | 106.5 GiB |
| reserved for OS/page cache | 6.0 GiB |
| headroom | 45.4 GiB |

### UD-Q2_K_XL · medium

```bash
ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-Q2_K_XL/Qwen3.8-Flash-Next-UD-Q2_K_XL-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{"reasoning_effort": "medium"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4
```

| Item | Size |
| --- | --- |
| weights (resident) | 49.2 GiB |
| embedding table, lazy (not resident) | 26.8 GiB |
| KV cache (12 attention layers) | 2.0 GiB |
| indexer cache | 0.7 GiB |
| DeltaNet state | 0.1 GiB |
| compute buffer (estimated) | 1.6 GiB |
| MTP head + draft KV | 3.4 GiB |
| prompt cache (max) | 2.0 GiB |
| total | 59.2 GiB |
| available (MemAvailable) | 106.5 GiB |
| reserved for OS/page cache | 6.0 GiB |
| headroom | 41.4 GiB |

### UD-IQ3_XXS · medium

```bash
ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-IQ3_XXS/Qwen3.8-Flash-Next-UD-IQ3_XXS-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{"reasoning_effort": "medium"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4
```

| Item | Size |
| --- | --- |
| weights (resident) | 52.1 GiB |
| embedding table, lazy (not resident) | 26.8 GiB |
| KV cache (12 attention layers) | 2.0 GiB |
| indexer cache | 0.7 GiB |
| DeltaNet state | 0.1 GiB |
| compute buffer (estimated) | 1.6 GiB |
| MTP head + draft KV | 3.4 GiB |
| prompt cache (max) | 2.0 GiB |
| total | 62.0 GiB |
| available (MemAvailable) | 106.5 GiB |
| reserved for OS/page cache | 6.0 GiB |
| headroom | 38.4 GiB |

### UD-IQ4_XS · medium

```bash
ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-IQ4_XS/Qwen3.8-Flash-Next-UD-IQ4_XS-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{"reasoning_effort": "medium"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4
```

| Item | Size |
| --- | --- |
| weights (resident) | 63.0 GiB |
| embedding table, lazy (not resident) | 26.8 GiB |
| KV cache (12 attention layers) | 2.0 GiB |
| indexer cache | 0.7 GiB |
| DeltaNet state | 0.1 GiB |
| compute buffer (estimated) | 1.6 GiB |
| MTP head + draft KV | 3.4 GiB |
| prompt cache (max) | 2.0 GiB |
| total | 72.9 GiB |
| available (MemAvailable) | 106.5 GiB |
| reserved for OS/page cache | 6.0 GiB |
| headroom | 27.5 GiB |

### UD-IQ3_XXS · xhigh

```bash
ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-IQ3_XXS/Qwen3.8-Flash-Next-UD-IQ3_XXS-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{"reasoning_effort": "xhigh"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4
```

| Item | Size |
| --- | --- |
| weights (resident) | 52.1 GiB |
| embedding table, lazy (not resident) | 26.8 GiB |
| KV cache (12 attention layers) | 2.0 GiB |
| indexer cache | 0.7 GiB |
| DeltaNet state | 0.1 GiB |
| compute buffer (estimated) | 1.6 GiB |
| MTP head + draft KV | 3.4 GiB |
| prompt cache (max) | 2.0 GiB |
| total | 62.0 GiB |
| available (MemAvailable) | 106.5 GiB |
| reserved for OS/page cache | 6.0 GiB |
| headroom | 38.4 GiB |

## Other runs

- UD-Q4_K_XL · medium: 1/1 tasks (1 min), profile `mtp4-ngram-thinking-medium`

Raw data: `state/quality/tbench/`, transcripts and verifier output under `bench/quality/terminal-bench-mini/jobs/`. Interactive view: [terminal-bench.html](terminal-bench.html).
