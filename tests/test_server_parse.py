from __future__ import annotations

from qwen38tui.config import ServerConfig, build_command
from qwen38tui.server import ServerProcess


def test_parse_real_log_lines():
    sp = ServerProcess()
    lines = [
        "0.00.824.535 I add: tensor per_layer_token_embd.weight (size = 27465 MiB) lazy read enabled",
        "0.03.131.423 I load_tensors:        ROCm0 model buffer size = 50191.17 MiB",
        "0.03.131.425 I load_tensors:   CPU_Mapped model buffer size = 27465.95 MiB",
        "0.14.684.084 I llama_kv_cache:      ROCm0 KV buffer size =   408.00 MiB",
        "0.15.980.417 I sched_reserve:      ROCm0 compute buffer size =  1188.28 MiB",
        "0.21.282.288 I llama_kv_cache: attn_rot_k = 1, n_embd_head_k_all = 256",
        "0.31.427.784 I srv    load_model: initializing, n_slots = 1, n_ctx_slot = 131072, kv_unified = 'false'",
        "0.15.939.765 I srv  llama_server: model loaded",
        "0.15.939.770 I srv  llama_server: listening on http://127.0.0.1:8098",
        "0.35.145.422 I slot print_timing: id  0 | task 0 | prompt eval time =     653.03 ms /    68 tokens (    9.60 ms per token,   104.13 tokens per second)",
        "0.35.145.425 I slot print_timing: id  0 | task 0 |        eval time =   12353.39 ms /   300 tokens (   41.32 ms per token,    24.20 tokens per second)",
        "0.35.145.430 I slot print_timing: id  0 | task 0 | draft acceptance = 0.86047 (  185 accepted /   215 generated), mean len = 3.28",
    ]
    for l in lines:
        sp._parse(l)
    st = sp.stats
    assert st.lazy_tensors and "per_layer_token_embd.weight" in st.lazy_tensors[0]
    assert abs(st.model_buffer_mib - (50191.17 + 27465.95)) < 0.1
    assert abs(st.kv_buffer_mib - 408.0) < 0.1 and abs(st.compute_buffer_mib - 1188.28) < 0.1
    assert st.attn_rot_k == 1 and st.n_ctx == 131072 and sp.ready
    assert st.last_prompt_n == 68 and abs(st.last_pp_tps - 104.13) < 0.01
    assert st.last_gen_n == 300 and abs(st.last_tg_tps - 24.20) < 0.01
    assert st.draft_accepted == 185 and st.draft_n == 215 and abs(st.accept_rate - 0.8605) < 0.001


def test_sleep_idle_zero_not_emitted(inv, hw):
    assert "--sleep-idle-seconds" not in build_command(ServerConfig(quant="UD-Q2_K_XL", sleep_idle_seconds=0), inv, hw).argv
    assert "--sleep-idle-seconds" in build_command(ServerConfig(quant="UD-Q2_K_XL", sleep_idle_seconds=600), inv, hw).argv


def test_form_input_does_not_clamp_siblings(inv, hw):
    """batch kurzzeitig auf 32 gesetzt (Tippen) darf ubatch nicht dauerhaft klemmen; das Kommando nutzt eine normalisierte Kopie."""
    cfg = ServerConfig(quant="UD-Q2_K_XL", batch_size=32, ubatch_size=512)
    cmd = build_command(cfg.copy(), inv, hw)
    assert cfg.ubatch_size == 512                      # Original unangetastet
    assert "-ub" in cmd.argv and cmd.argv[cmd.argv.index("-ub") + 1] == "32"   # Kopie normalisiert
