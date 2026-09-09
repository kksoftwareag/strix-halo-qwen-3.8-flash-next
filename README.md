# qwen38-flash

> **Note:** The bulk of this repository (program, build and benchmark scripts, research, documentation and
> website) was created by Claude Fable 5.1 (Anthropic), directed and reviewed by the author. The measurements come
> from real runs on the hardware described.

A terminal program with which you set up, start, monitor and measure **Qwen3.8-Flash-Next** on an **AMD Strix Halo**
machine (Ryzen AI MAX+ 395 / Radeon 8060S, 128 GB unified memory) with **llama.cpp**. It takes the decisions off your
hands that are difficult with this model: Which quant fits into memory? Which startup parameters make sense? Does
speculative decoding (MTP) run? How many users at the same time?

Everything is measured on such a machine. The results and the reasoning are in
`docs/RESEARCH.md`.

![Configuration tab: the settings on the left, memory balance, warnings and the generated command line on the right](docs/screenshot-configuration.png)

## What the program can do

- **Configure**: model quant, context length, KV cache, batch sizes, MTP draft head, thinking mode,
  sampling, network. On the right you immediately see the estimated memory requirement and the finished command line.
- **Protect memory**: the start is refused if the configuration does not fit into memory.
  A guard stops the server before the kernel kills processes because of memory shortage.
- **Start and observe**: server log, load time, buffer sizes, tokens per second, acceptance rate of the
  draft head, test prompt.
- **Measure**: `llama-bench`, server measurement with MTP, automatic search for the best MTP settings
  and a multi-user test with up to 8 simultaneous requests.
- **Export**: start script and systemd unit for operation without the program.
- **Presets**: ready-made configurations for maximum quality, speed, long context, chat without thinking, a coding
  agent, and `eh-team` for several agents at once (8 slots of 160k, one each, with the prompt cache set up so a
  follow-up turn hits it to 99.5 %).

The program changes nothing in your model files and nothing outside its own directory.

## Requirements

| What | Why |
| --- | --- |
| AMD Strix Halo (gfx1151) with 128 GB, Linux | everything is measured for that; other machines with a lot of unified memory should work, but are not tested |
| ROCm/HIP 7.x with `clang++`, `cmake`, `ninja`, `git` | to build the two llama.cpp variants |
| Kernel parameters `amd_iommu=off amdgpu.gttsize=126976 ttm.pages_limit=32505856` | otherwise the GPU may use only part of the RAM |
| Python 3.12 or newer, [uv](https://docs.astral.sh/uv/) | for the terminal program |
| `hf` (Hugging Face CLI) | to download the models |
| about 200 GB free space on a fast NVMe | models 73 to 104 GB per quant |

## Installation

```bash
git clone <URL of this repo> qwen38-flash
cd qwen38-flash
uv sync                      # creates .venv and installs Textual & co.
```

### Download models

```bash
# Best quant that fits into 128 GB with MTP (engine EngramHalo):
hf download unsloth/Qwen3.8-Flash-Next-GGUF --include 'UD-Q4_K_XL/*'
# Smaller alternatives:
hf download unsloth/Qwen3.8-Flash-Next-GGUF --include 'UD-IQ4_XS/*'
hf download unsloth/Qwen3.8-Flash-Next-GGUF --include 'UD-IQ3_XXS/*'
# MTP draft head (only this one matches the builds here):
hf download dzannotti/Qwen3.8-Flash-Next-MTP-GGUF Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf
```

The program finds the files in the Hugging Face cache by itself. If they are elsewhere, set
`QWEN38_MODEL_DIRS=/path/a:/path/b` and `QWEN38_MTP_DIRS=/path/mtp`.

### Build engines

```bash
engine/fetch.sh                 # fetches llama.cpp and EngramHalo.cpp from public repos and patches them
engine/build-engramhalo.sh      # recommended engine (Strix Halo fork)
engine/build.sh hip             # second engine: llama.cpp + MTP patch
```

Both builds end up under `engine/build-*/bin/`. You register your own llama.cpp build with
`QWEN38_ENGINES=name=/path/to/llama`.

## Usage

```bash
./run.sh                        # terminal program
./run.sh presets                # all presets
./run.sh show --preset eh-qualitaet    # show command line and memory balance
./run.sh run  --preset eh-qualitaet    # start server without the program
./run.sh bench-parallel --users 8      # multi-user benchmark without the program
./run.sh export --preset eh-team --host 0.0.0.0 \
    --api-key-file state/api-keys.txt --new-keys 5 --install    # service for the LAN
```

### Running as a service on the network

`export` writes a start script and a systemd **user** unit to `scripts/`, and with `--install` also to
`~/.config/systemd/user/`. The unit starts the server under `bench/memguard.py`, because GPU memory (GTT) shows up in
no cgroup limit — `MemoryMax` would not protect anything here, only `MemAvailable` does. A guard kill is not retried
endlessly: three attempts in ten minutes, then the service stays down.

```bash
systemctl --user daemon-reload
systemctl --user enable --now qwen38-eh-team.service
systemctl --user status qwen38-eh-team.service
journalctl --user -u qwen38-eh-team.service -f
```

A user unit runs only while the user is logged in. For a start at boot: `sudo loginctl enable-linger $USER`.

`--new-keys N` writes N random keys to the file given by `--api-key-file`, one per line, with mode 0600; existing
files are never overwritten. The server takes them with `--api-key-file`, so the keys do not appear in the process
list. Clients send `Authorization: Bearer <key>`; without one, or with a wrong one, the server answers 401. Add or
revoke a key by editing the file and restarting the service.

**`--host 0.0.0.0` opens the server to the whole network.** The keys are the only protection, and plain HTTP sends
them unencrypted — so use it on a trusted network, or put TLS in front (`--ssl-key-file` / `--ssl-cert-file`).

In the program: choose a preset and press "Apply preset". On the right are the memory balance and the command.
**F5** starts the server, **F6** stops it, **F9** exports a start script, **Ctrl+S** saves
the configuration. Tabs: Configuration, Server, Benchmark, System, Help.

The server is then reachable at `http://<host>:8080` with the OpenAI-compatible API
(`/v1/chat/completions`), including the web interface of llama.cpp.

## The most important findings

**Memory.** Every quant contains the same 26.8 GB table for n-gram embeddings. Normal
llama.cpp loads it completely into RAM on ROCm, in addition to the weights in the GPU. That is why the
best quant (UD-Q4_K_XL) with MTP does not fit into 128 GB there. The fork **EngramHalo.cpp** leaves the table on the
NVMe (only about 3 GB in RAM) and still loads in under 30 seconds. With that, UD-Q4_K_XL runs with MTP
at about 85 GB memory requirement.

**Speed** (one user, 32k context, KV cache q8_0):

| Engine | Quant | MTP | Decode | Memory |
| --- | --- | --- | --- | --- |
| EngramHalo | UD-Q4_K_XL | on | 33–41 t/s | 85 GB |
| EngramHalo | UD-IQ4_XS | on | 36 t/s | 69 GB |
| EngramHalo | UD-IQ3_XXS | off / on | 23 / 34 t/s | 53 / 57 GB |
| llama.cpp + patch | UD-IQ4_XS | on | 34 t/s | 93 GB |
| llama.cpp + patch | UD-Q4_K_XL | on | does not fit | over 107 GB |

**Several users** (UD-IQ4_XS, without MTP): 1/2/4/8 simultaneous requests give 20/32/42/50 tokens per
second in total. MTP only pays off with one user; with 8 users it is only 35 instead of 50 t/s with MTP.

**Further decisions**: ROCm instead of Vulkan (Vulkan collapses with MTP on this model). Only the
dzannotti MTP head matches the builds; the unsloth head needs the unsloth fork. The environment variable
`LLAMA_ATTN_ROT_DISABLE` is not needed. `reasoning_effort` only knows `xhigh`, `medium` and `low`.

## Directories

| Path | Content |
| --- | --- |
| `qwen38tui/` | the program (configuration, memory estimation, model detection, GGUF reader, server control, benchmarks, interface) |
| `engine/` | `fetch.sh`, build scripts, patches; after the build `build-engramhalo/` and `build-hip/` |
| `bench/` | measurement scripts with memory guard, `context_limits.py` (how many simultaneous contexts fit per quant) and the raw results of this machine |
| `bench/quality/` | agent benchmark Terminal-Bench-Mini-20: fetch script, runner, analysis (see `bench/quality/README.md`) |
| `docs/` | `RESEARCH.md` (research with sources), `QUALITY-BENCHMARKS.md` (which quality benchmarks are possible in 8 hours), `TERMINAL-BENCH.md` (results of the agent benchmark), `HELP.md` (help inside the program) and the documentation website (HTML, published via GitHub Pages from this directory) |
| `tests/` | `uv run pytest -q` |
| `state/` | own profiles, logs, measurement results (created on first start) |

## Documentation website

The directory `docs/` contains a static website with all decisions, measurements and sources
(`index.html`, `decisions.html`, `memory.html`, `measurements.html`, `terminal-bench.html`, `guide.html`, `research.html`).
Publishing: in the repository settings under "Pages" choose the branch `main` with the directory `/docs`.
Repository: <https://github.com/kksoftwareag/strix-halo-qwen-3.8-flash-next>.
No build step is needed; `.nojekyll` makes sure that GitHub delivers the files unchanged.

## Known limits

- Only tested with ROCm/HIP on gfx1151. A Vulkan build is prepared, but not measured.
- MTP with several slots is not good on this architecture; the program switches it off in the
  multi-user test.
- The memory requirement is estimated. The estimate is calibrated to the measurements, but can deviate with
  unusual settings. The guard catches that.
- MTP support for this model is not yet included in llama.cpp. The patches here
  follow the open pull requests and have to be adapted for new llama.cpp versions.

## Thanks

- [llama.cpp](https://github.com/ggml-org/llama.cpp) and the authors of the qwen4exp support
- [EngramHalo.cpp](https://github.com/Aristo94/EngramHalo.cpp) for the Strix Halo fork
- [dzannotti](https://huggingface.co/dzannotti/Qwen3.8-Flash-Next-MTP-GGUF) for the MTP draft head and the patch
- [unsloth](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) for the quantizations
- [Qwen](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) for the model
- [Textual](https://textual.textualize.io/) for the terminal interface

## License

This project is under the **European Union Public Licence v. 1.2 (EUPL-1.2)**, see `LICENSE`.
The models, llama.cpp, EngramHalo.cpp and the third-party patches are under their own licenses.
