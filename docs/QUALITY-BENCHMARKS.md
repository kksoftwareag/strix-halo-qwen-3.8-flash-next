# Quality benchmarks for the quant comparison (8-hour budget)

As of 2026-09-04. Assessment of which benchmarks are suitable on this machine (Strix Halo, 128 GB) within a budget of
8 hours for comparing the quantizations. The speed measurements are in `RESEARCH.md`.

For benchmarks that measure real agent work in the terminal, Terminal-Bench-Mini-20 is integrated; how to operate it
is described in [`bench/quality/README.md`](../bench/quality/README.md), the assessment in the section
[Agent benchmarks](#agent-benchmarks-terminal-bench-mini-20).

## Calculation basis

| Quantity | Value | Source |
| --- | --- | --- |
| decode, one user with MTP | approx. 35 t/s | own measurement |
| decode, 8 slots without MTP, total | approx. 50 t/s | own measurement |
| prompt processing | approx. 400 t/s (short), approx. 200 t/s at >100k context | own measurement, fork documentation |
| tokens that can be generated in 8 hours | approx. 1.4 million | 8 × 3600 × 50 |
| quant switch (EngramHalo) | approx. 30 s | own measurement |
| free RAM for Docker containers | approx. 20 GB (Q4_K_XL), approx. 35 GB (IQ4_XS) | memory budget |

For all runs: server with `-np 8`, MTP off, `reasoning_effort` low or thinking off. MTP only pays off with a single
user; most harnesses run in parallel.

## Candidates

| Benchmark | Scope | Smaller variant | Effort per quant (8 slots) | Suitability for the quant comparison |
| --- | --- | --- | --- | --- |
| KL divergence (`llama perplexity`, reference Q4_K_XL) | any | 65k tokens Wikitext, ctx 8192 | approx. 10 min | very good, measures the quantization loss directly |
| Aider Polyglot | 225 tasks, 2 attempts | `--languages python` (34) or `--num-tests 60` | 1 to 1.5 h with thinking low | good: code and edit format |
| EvalPlus HumanEval+ | 164 tasks | complete | approx. 1 h with thinking low | good, cheap |
| IFEval (lm-eval) | 541 prompts | `--limit 300` | approx. 1 h without thinking | good for instruction following |
| GSM8K, MATH-500, GPQA Diamond (lm-eval) | 1319 / 500 / 198 | `--limit 200` | 1 to 4 h depending on effort | medium; thinking drives up the token count |
| AIME 2025 (lm-eval) | 30 tasks | none | 3 to 5 h at xhigh | poor: only 30 tasks |
| SWE-bench Verified Mini (mini-swe-agent) | 50 instances, 5 GB instead of 130 GB | `--slice 0:20` | 4 to 8 h for 50 instances, 8 workers | only one quant per budget, a lot of noise |
| Terminal-Bench-Mini-20 (Harbor, Terminus-2) | 20 tasks from TB 2.1 | `--tier smoke`, `--task <id>`, `--attempts 1` | 12 to 26 h for all 20 | best in substance, but more than a day's budget per quant |
| Terminal-Bench 2.1 complete (Harbor) | 89 tasks | none useful | several days | unsuitable |
| DeepSWE (Pier, mini-swe-agent) | 113 tasks, up to 2.5 h per task | `--n-tasks 10 --sample-seed 0` | 5 to 10 h for 10 tasks | unsuitable: too few tasks per hour, leaderboard only frontier models |

Notes on individual candidates:

- **DeepSWE** has been a benchmark of its own from Datacurve since 2026 (113 long-running tasks from active repos, five
  languages, hand-written verifiers), no longer just the Agentica model. The harness is Pier (Harbor-compatible) with
  mini-swe-agent as a fixed scaffold; no step or cost limit, time limit 2.5 h per task.
- **Terminal-Bench-Mini-20** is integrated in the repo (`bench/quality/`); the project's own runner starts the server,
  sets endpoint, context length and the identity of the configuration, and cleans up afterwards. Details below.
- **SWE-bench Verified Mini**: `mini-extra swebench --subset MariusHobbhahn/swe-bench-verified-mini --split test --slice 0:20 -w 8`,
  model via the configuration `model_name: openai/<name>` with `api_base`. Scoring locally with the SWE-bench harness or via
  `sb-cli`. Step limit 250 by default; lower it to 60 to 80 for the budget.
- **Aider Polyglot**: Aider Docker, `./benchmark/benchmark.py <name> --model openai/<name> --edit-format diff --threads 8
  --languages python --exercises-dir polyglot-benchmark`, `OPENAI_API_BASE` pointing at the server. Evaluation with `--stats`.
- **lm-eval**: `lm_eval --model local-chat-completions --model_args model=<name>,base_url=http://<host>:8080/v1/chat/completions,num_concurrent=8
  --tasks ifeval --apply_chat_template --limit 300`. Check task names with `lm-eval ls tasks` (among others `ifeval`, `gsm8k`,
  `hendrycks_math`, `gpqa`, `aime`, `mmlu_pro`, `humaneval`).
- **KL divergence**: The logit file is about 500 KB per token (vocabulary 248,320). At 65k tokens that is around 32 GB, hence
  `--chunks 8 -c 8192`. Perplexity with 32k chunks runs into an OOM on this machine (logits × vocabulary).

## Agent benchmarks: Terminal-Bench-Mini-20

For the question "does the model work usefully as a coding agent?", multiple-choice and
single-file benchmarks are no use. Terminal-Bench-Mini-20 is a 20-task selection from
Terminal-Bench 2.1, tailored to local models: the agent (Terminus-2) gets a real
shell in a Docker container and has to actually solve the task; only what the
bundled verifier accepts counts (reward exactly 1.0). The default is pass@2 – the second attempt
only runs if the first one fails.

Task mix: 7 software development, 4 system administration, 9 from debugging, security,
data querying, ML systems and file formats; by metadata 3 easy, 13 medium, 4 hard.
Examples: build a Python package and make it installable from a local PyPI server, remove a leak
from the git history, debug a crash in OCaml's garbage collector in C,
compile POV-Ray 2.2 from 1990 on a present-day system, wire Postfix and Mailman into a
working mailing list.

### Integration into this repo

```bash
bench/quality/fetch.sh                                   # fetch the benchmark, check prerequisites
uv run python bench/quality/tbench.py --tier smoke --attempts 1   # smoke test, one task
uv run python bench/quality/tbench.py --tier full                 # all 20 tasks
uv run python bench/quality/tbench.py --tier full --quant UD-IQ4_XS
```

`tbench.py` starts the server with the preset `eh-agent` (UD-Q4_K_XL, 163840 context, one slot,
MTP + n-gram, small prompt cache), waits for `/health`, passes endpoint, context length and the
identity of the run to the runner, and stops the server afterwards. The server runs under
`bench/memguard.py`. Operation in detail: [`bench/quality/README.md`](../bench/quality/README.md).

### Results on this machine

The project's own runs are in [`TERMINAL-BENCH.md`](TERMINAL-BENCH.md), interactively in [terminal-bench.html](terminal-bench.html) – there the full transcript of the agent can be opened for every task, with reasoning, commands and terminal output per step.

### Time required

The project publishes runs on comparable hardware (Strix Halo, 128 GB). They show what
20 agent tasks cost with a local model:

| Model | Quant | Engine/backend | pass@1 | pass@2 | Duration |
| --- | --- | --- | --- | --- | --- |
| DeepSeek-V4-Flash-0731 | UD-IQ3_XXS | llama.cpp/vulkan | 18/20 | 18/20 | 12 h |
| DeepSeek-V4-Flash-0731 | IQ2XXS mixed | DwarfStar/rocm | 17/20 | 19/20 | 18 h |
| Qwen3.8-27B | UD-Q4_K_XL | llama.cpp/rocm | 16/20 | 19/20 | 15 h |
| Qwen3.8-27B | Q4_0_ROCMI4 | llama.cpp/rocm | 16/20 | 17/20 | 17 h |
| DeepSeek-V4-Flash-0731 | MXFP4 | DwarfStar/rocm | 15/20 | 19/20 | 23 h |
| Qwen3.6-27B | UD-Q8_K_XL | llama.cpp/rocm | 12/20 | 14/20 | 26 h |
| Qwen3.6-35B-A3B | UD-Q4_K_XL | llama.cpp/rocm | 11/20 | 11/20 | 15 h |

So a complete run costs one day per quantization – a quant comparison across three
variants is three days, not eight hours. What fits into the 8-hour budget:

| Variant | Scope | Duration | What it shows |
| --- | --- | --- | --- |
| one quant, `--tier full --attempts 1` | 20 tasks, one attempt, timeout 25 min | 6 to 9 h | pass@1 for one configuration |
| subset per quant | 8 short tasks, `--tasks`, `--attempts 1` | 2 to 3 h per quant | rough comparison of three quants |
| `--concurrency 4` with UD-IQ4_XS | 20 tasks in parallel across 4 slots | 8 to 12 h | pass@1, about 30 % faster |

With several slots the context is shared: `--concurrency 4` at 262144 total context means 65536
tokens per task, and throughput per task drops (measured: 1/2/4/8 slots = 20.4/32.0/42.4/50.4
tokens/s total). Four slots are the best compromise; eight slots leave too little context per agent.

### Significance

20 tasks are a small sample: a result of 12/20 has a 95 % interval of about
±11 percentage points, with 8 tasks it is ±17. Differences of one or two solved tasks
between two quants are noise. The benchmark reliably answers "does the model run smoothly as an
agent at all?" (tool calls, long sessions, summarizing at full context) and
shows large jumps in quality; for fine differences between quants the KL divergence remains the sharper
tool.

### Peculiarity of this network

`archive.ubuntu.com` responds only very slowly from this LAN over IPv4 (around 20 s per request,
IPv6 not at all). At the start of every task Terminus-2 installs `tmux` and `asciinema` in the container
and runs into Harbor's 120-second limit – every task then fails with
`RuntimeError: Command timed out after 120 seconds`. `tbench.py` checks this at startup and points
`archive.ubuntu.com` and `security.ubuntu.com` at a fast mirror via `extra_hosts`
(default `ftp.fau.de`); `apt-get update` then takes 1 s instead of over 120 s. Turn it off with
`--apt-mirror off`, use a different mirror with `--apt-mirror <host>`. This is implemented via a
Docker shim (`bench/quality/dockershim/docker`) that only appends a Compose overlay file;
the benchmark itself and the task images stay unchanged.

### SWE-bench Verified Mini as an alternative

If the point is patches in real repositories rather than terminal work, SWE-bench Verified Mini
(50 instances, 5 GB of images instead of 130 GB) is the smaller candidate. The harness is mini-swe-agent:

```bash
mini-extra swebench --subset MariusHobbhahn/swe-bench-verified-mini --split test \
  --slice 0:20 -w 4 --model openai/qwen3.8-flash
```

Model via `~/.config/mini-swe-agent/mini.yaml` with `api_base` pointing at the local server. The
step counter defaults to 250; lower it to 60 to 80 for a time budget. One instance
costs 10 to 25 minutes, so 20 instances take 2 to 4 hours with four workers.

## Recommended plan for three quants (Q4_K_XL, IQ4_XS, IQ3_XXS)

| Step | Scope | Duration | Result |
| --- | --- | --- | --- |
| 1. KL divergence, all four quants | 65k tokens, reference Q4_K_XL | approx. 30 min | mean KLD, Δp percentiles, same-top-p per quant |
| 2. Aider Polyglot, Python | 34 tasks × 2 attempts, 8 threads, thinking low | approx. 3.5 h | pass rate, edit errors per quant |
| 3. HumanEval+ or IFEval | 164 or 300 prompts, 8 slots | approx. 3 h | pass rate or instruction following per quant |

Total around 7 hours including load times.

Assessment: with 34 to 164 tasks the spread is 5 to 8 percentage points. The difference between Q4_K_XL
(KLD 0.047) and IQ4_XS (0.084) will probably not be visible in the task benchmarks; Q2_K_XL (0.225) usually
falls off noticeably. The KL divergence is therefore the mandatory part; the task benchmarks show whether a loss
has a practical effect.

Terminal-Bench and SWE-bench Mini are worth a one-off run with the default quant outside the 8-hour budget,
to check whether the model works reliably with Terminus-2 and mini-swe-agent respectively.

## Example commands

```bash
# server for benchmarks (8 slots, without MTP, thinking low)
./run.sh run --preset eh-qualitaet    # in the TUI: slots (-np) = 8, MTP off, reasoning_effort low

# KL divergence: reference logits with Q4_K_XL, then comparison
engine/build-engramhalo/bin/llama perplexity -m <Q4_K_XL> -f wiki.test.raw -c 8192 --chunks 8 -ngl 99 -lm none \
  --save-all-logits state/bench/q4kxl.kld
engine/build-engramhalo/bin/llama perplexity -m <IQ4_XS> -f wiki.test.raw -c 8192 --chunks 8 -ngl 99 -lm none \
  --kl-divergence-base state/bench/q4kxl.kld --kl-divergence
```

## Sources

- https://github.com/kyuz0/terminal-bench-mini and https://kyuz0.github.io/terminal-bench-mini/
- https://github.com/harbor-framework/terminal-bench-2-1
- https://huggingface.co/datasets/harborframework/terminal-bench-2.0
- https://www.harborframework.com/docs/tutorials/running-terminal-bench
- https://github.com/harbor-framework/terminal-bench-2
- https://www.harborframework.com/docs/agents
- https://mini-swe-agent.com/latest/usage/swebench/
- https://mini-swe-agent.com/latest/models/local_models/
- https://huggingface.co/datasets/MariusHobbhahn/swe-bench-verified-mini
- https://arxiv.org/abs/2607.07946 (DeepSWE) and https://github.com/datacurve-ai/deep-swe
- https://github.com/Aider-AI/aider/blob/main/benchmark/README.md and https://github.com/Aider-AI/polyglot-benchmark
- https://github.com/EleutherAI/lm-evaluation-harness
- https://github.com/ggml-org/llama.cpp/blob/master/tools/perplexity/README.md
