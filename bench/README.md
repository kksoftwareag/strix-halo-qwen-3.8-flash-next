# bench/ – measurement tools and results

All runs here start the server **under `memguard.py`** (SIGKILL at < 10 GiB `MemAvailable`), because GTT memory
does not show up in the RSS and the kernel OOM killer would otherwise take the whole session down with it.

| Script | Purpose |
| --- | --- |
| `memguard.py --min-avail-gib N -- CMD…` | guard + CSV log (MemAvailable, GTT, VRAM, RSS) |
| `mem_probe.py NAME -- llama serve …` | start server, one request, hard stop; JSON with load time, tg/pp, draft acceptance, peak consumption |
| `mem_sweep*.sh` | footprint sweeps (1–7): stock fork vs EngramHalo, load modes, quants, MTP |
| `sweep1-backend.sh` | llama-bench pp512/tg128 (stock fork): KV type, ubatch, quant |
| `mtp_sweep.py` / `mtp_sweep2.py` | MTP fine-tuning via the server (n_max, p_min, temp, ngram-mod); `mtp_sweep2.py --engine engramhalo --quant Q4_K_XL --lm none` |

Results: `results/raw/*.json` (llama-bench), `results/mem/*.json|csv|log` (footprints), `results/mtp2/summary.jsonl`
(MTP tuning). Analysis of the key numbers in `../docs/RESEARCH.md`, section 7.

Important when stopping probe servers: SIGINT triggers a teardown lasting minutes (GTT release) – the scripts
therefore send SIGKILL. Write `pkill -f` patterns in your own shell with the bracket trick (`mem_pro[b]e`), otherwise
`pkill` hits the shell that calls it.

## Multi-user with long contexts

`mtp_multiuser.sh` runs 1/2/4/8/16 simultaneous users with about 30,000 tokens of prompt and about 5,000 tokens of output each,
MTP on. Every user gets its own filler text so that the prompt cache is not shared. Per level, the output also shows
the draft acceptance — that is where the bug from llama.cpp issue #27572 shows up, in which the acceptance falls to 0.00 with
several slots and long prompts.

```bash
bench/mtp_multiuser.sh vorher     # all four small quants, existing builds
ENGINE_RING_PATCH=1 engine/fetch.sh && engine/build-engramhalo.sh && engine/build.sh hip
bench/mtp_multiuser.sh nachher    # with patch 0003 (PR #27311) and 0004 (issue #28433)
```

So far only "vorher" has been measured: with long prompts, parallelism brings no throughput (see
`docs/RESEARCH.md`), which is why the patches were not built. The results are in
`state/bench/mtp-multiuser-*.log`, prepared via `analyze_multiuser.py`.

Without an argument, UD-IQ4_XS, UD-IQ3_XXS, UD-Q2_K_XL and UD-IQ1_M run one after another; individual quants as further
arguments. Default: levels 1/2/4/8, 15,000 tokens of prompt per user, 2,000 tokens of output – around 30 minutes per
quant and round. This can be changed via `TB_LEVELS`, `TB_CTX` and `TB_GEN`, for example
`TB_LEVELS=1,2,4,8,16 TB_CTX=30000 TB_GEN=5000` for the large variant.

15,000 tokens of prompt are enough for the bug from issue #27572: it needs a decode across several ubatches, and with
`ubatch 2048` that is already eight. With eight slots, UD-Q4_K_XL fits into memory again as well; it is just not
the default.

`context_limits.py` predicts how many slots of which size fit into memory.
