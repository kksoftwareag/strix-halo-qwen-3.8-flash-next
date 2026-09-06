# Agent benchmarks (real coding work)

This is the integration with **Terminal-Bench-Mini-20** – 20 tasks from Terminal-Bench 2.1,
selected for local models: build packages, configure services, repair git history,
hunt down C and OCaml bugs, straighten out LaTeX and SPARQL. The agent (Terminus-2) works in
a Docker container with a real shell; only what the task's verifier accepts
at the end is counted (reward exactly 1.0).

The benchmark itself comes from <https://github.com/kyuz0/terminal-bench-mini> (Apache-2.0) and
is not versioned along with this repository but fetched:

```bash
bench/quality/fetch.sh          # clones the benchmark and checks docker, uv, memory, disk space
```

## All quants one after another

```bash
bench/quality/run-quants.sh                       # UD-Q2_K_XL, UD-IQ1_M, UD-IQ3_XXS, UD-IQ4_XS
bench/quality/run-quants.sh UD-IQ4_XS             # only one
TB_AGENT_TIMEOUT=1800 bench/quality/run-quants.sh # time limit per task (default 3600 s)
TB_EFFORT=xhigh bench/quality/run-quants.sh       # reasoning effort (default medium)
```

The reasoning effort is part of the profile name (`mtp4-ngram-thinking-medium`) and thus part of the identifier of every run;
runs with a different effort end up in separate results directories and appear side by side
on the website.

The script waits between the quants until the memory is free again, writes a log per quant to
`state/quality/tbmini-<quant>.log` and pins the apt mirror (see below). Then the analysis:

```bash
uv run python bench/quality/report.py             # writes docs/TERMINAL-BENCH.md and docs/tbmini-data.js
```

## Start a run

`tbench.py` starts the server with a configuration from the TUI, waits for `/health`, calls the
runner and stops the server again afterwards. The server runs under `bench/memguard.py`.

```bash
# smoke test: one task, one attempt (about 15-40 min)
uv run python bench/quality/tbench.py --tier smoke --attempts 1 --agent-timeout 3600

# full run: 20 tasks, up to 2 attempts per task
uv run python bench/quality/tbench.py --tier full

# different quant, same configuration
uv run python bench/quality/tbench.py --tier full --quant UD-IQ4_XS

# single task
uv run python bench/quality/tbench.py --task fix-git --attempts 1
```

Important flags:

| Flag | Meaning |
| --- | --- |
| `--preset` | server preset, default `eh-agent` (Q4_K_XL, 160k context, one slot, MTP+ngram) |
| `--quant`, `--ctx`, `--no-mtp`, `--reasoning-effort` | override individual values |
| `--concurrency N` | N tasks at the same time; also sets `-np N` (the context is divided among the slots) |
| `--slots N` | set the slots separately from the concurrency |
| `--attempts` | attempts per task (default 2 = pass@2, `1` = pass@1) |
| `--agent-timeout` | seconds per attempt (default 10800) |
| `--min-avail-gib` | threshold of the memory guard (default from the preset: 5 GiB) |
| `--use-running` | do not start a server, use a running one |
| `--dry-run` | only show the memory balance and the commands |

Everything after `--` is passed unchanged to `terminal_bench.py`.

## Container images

Each of the 20 tasks brings its own Docker image (a few GB in total). On the first run, Harbor downloads
them one by one; an image can take several minutes, and the run waits for it. It is faster to fetch them
in parallel beforehand:

```bash
python3 -c '
import tomllib, pathlib
for d in sorted(pathlib.Path("bench/quality/terminal-bench-mini/tasks").iterdir()):
    f = d / "task.toml"
    if f.is_file():
        print(tomllib.loads(f.read_text())["environment"]["docker_image"])
' | xargs -P 3 -I{} docker pull -q {}
```

From the second quant on, the images are in the cache; only the first round pays the load time.

## Memory

The agent runs in the container, the model in the same RAM. The balance is at the start of every output:

| Quant | Footprint (160k context, 1 slot) | free for the container |
| --- | --- | --- |
| UD-Q4_K_XL | 92.3 GiB | about 8 GiB |
| UD-IQ4_XS | 72.9 GiB | about 28 GiB |
| UD-IQ3_XXS | 62.0 GiB | about 38 GiB |

Tasks such as `build-pov-ray`, `sqlite-with-gcov` or `mteb-retrieve` compile or load
models in the container. With Q4_K_XL that is tight; for `--concurrency > 1`, IQ4_XS is the
sensible choice. If `MemAvailable` falls below the threshold, the guard kills the server –
the run then aborts, but the machine stays usable.

## Source of error: aborted model requests

While investigating a time-limit failure (`cobol-modernization`, UD-IQ3_XXS, `xhigh`), a defect in the
interplay of harness and server came to light that affects all runs: **LiteLLM aborts a request after 600 seconds
and repeats it with the same prompt.** If a response takes longer on this hardware, a
loop results — every attempt runs into the limit again, no token arrives at the agent, and the time budget of the
task is used up.

In that case, the server produced five generations with an identical prompt for a single agent step
(about 11,700 tokens each, four of them aborted after 600 s); over the whole run there were 9 discarded generations with
around 87 of the 181 minutes together, i.e. 48% of the run time without any result. Recognizable in the server log by
`W srv stop: cancel task`.

Across all runs so far: **58 aborted generations**, 33 of them in the medium round. For
the interpretation of the results this means: part of the time-limit failures is not a model failure but time lost
in this loop, and the documented task durations are correspondingly too high.

Fixed with `bench/quality/patches/0001-request-timeout.patch`, which `fetch.sh` applies to the benchmark:
the time limit of a single request is now configurable (`tbench.py --request-timeout`, default 3600 s instead of 600).

## Network: apt mirror

`archive.ubuntu.com` is unusably slow from some networks (here at times 20 s per request). Terminus-2
installs `tmux` and `asciinema` in the container at the beginning of every task and then runs into Harbor's
120-second limit; every task fails with `RuntimeError: Command timed out after 120 seconds`.
`tbench.py --apt-mirror` points `archive.ubuntu.com` and `security.ubuntu.com` via `extra_hosts` at a
fast mirror (`auto` measures beforehand, `off` switches it off, otherwise a hostname). Implemented via
`bench/quality/dockershim/docker`, which appends an overlay file to every `docker compose` call – the
benchmark and the task images stay unchanged.

## Results

* Progress and summary: `state/quality/*.log`
* Normalized results per task: `state/quality/tbench/<platform>/<model>_results/`
* Raw jobs from Harbor (transcripts, verifier outputs): `bench/quality/terminal-bench-mini/jobs/`
* Server log and memory history: `state/logs/tbench-server-*.log`, `state/logs/tbench-mem-*.csv`
* Prepared: `docs/TERMINAL-BENCH.md` and the interactive page `docs/terminal-bench.html`
* Versioned in the repository: `bench/quality/results/` (summary and result per task) and
  `docs/transcripts/<quant>-<reasoning-effort>/<task>.json` (complete agent transcripts in ATIF format,
  around 2.5 MB per run)

The website only loads a transcript when it is clicked. When opening the page via `file://`, the
browser blocks that loading; for a local preview start `python3 -m http.server` in the directory `docs/`.

Continue an interrupted run or repeat failures (the server has to be running,
e.g. via the TUI, then `--use-running`):

```bash
cd bench/quality/terminal-bench-mini
python3 terminal_bench.py resume jobs/<job-name>
python3 terminal_bench.py retry-failed <results-directory>
```

## Time required

The project's reference runs on comparable hardware (Strix Halo, llama.cpp, ROCm)
need **12 to 26 hours** for the full 20 tasks. That does not fit into an
8-hour window; classification and alternatives are in `docs/QUALITY-BENCHMARKS.md`.
