from __future__ import annotations

from qwen38tui.config import ServerConfig
from qwen38tui.memory import GIB, estimate, kv_bytes_per_token


def test_kv_per_token_f16_and_q8(inv):
    m = inv.model("UD-Q4_K_XL")
    kv, idx = kv_bytes_per_token(m, ServerConfig(cache_type_k="f16", cache_type_v="f16"))
    assert kv == 12 * 2 * (256 * 2 + 256 * 2)          # 24 KiB
    assert idx == 12 * (128 * 2 + 256 * 2)          # Indexer-K (128) + V (256) in f16
    kv8, _ = kv_bytes_per_token(m, ServerConfig(cache_type_k="q8_0", cache_type_v="q8_0"))
    assert abs(kv8 - 12 * 2 * 512 * (34 / 32)) < 1e-6


def test_lazy_ple_reduces_resident(inv, hw):
    m = inv.model("UD-Q4_K_XL")
    est_lazy = estimate(ServerConfig(quant=m.quant, load_mode="mmap"), m, None, hw)
    est_full = estimate(ServerConfig(quant=m.quant), m, None, hw)
    assert est_lazy.weights_resident == m.total_bytes - m.ple_bytes
    assert est_full.weights_resident == m.total_bytes
    assert est_lazy.ple_lazy == m.ple_bytes and est_full.ple_lazy == 0
    assert est_full.verdict == "zu groß"
    assert est_lazy.verdict in ("ok", "knapp")


def test_context_scales_kv(inv, hw):
    m = inv.model("UD-Q2_K_XL")
    a = estimate(ServerConfig(ctx_size=32768, cache_type_k="f16", cache_type_v="f16"), m, None, hw)
    b = estimate(ServerConfig(ctx_size=262144, cache_type_k="f16", cache_type_v="f16"), m, None, hw)
    assert b.kv_cache == a.kv_cache * 8
    assert abs(b.kv_cache - 6 * GIB) < 0.05 * GIB


def test_mtp_adds_head(inv, hw):
    m = inv.model("UD-Q2_K_XL")
    head = inv.mtp_heads[0]
    without = estimate(ServerConfig(mtp_enabled=False), m, head, hw)
    with_ = estimate(ServerConfig(mtp_enabled=True), m, head, hw)
    assert with_.total - without.total >= head.n_bytes
