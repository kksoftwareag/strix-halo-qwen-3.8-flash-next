"""Speicherbedarfs-Schätzung für Qwen3.8-Flash-Next (qwen4exp) in llama.cpp auf Unified-Memory (Strix Halo).

Alles landet im selben physischen RAM (VRAM-Carve-out 16 GiB + GTT). Geschätzt werden:
  - residente Gewichte (Gesamt minus lazy geladene PLE-Tabelle)
  - KV-Cache der Full-Attention-Layer (12 von 48) je nach -ctk/-ctv und Kontext
  - Indexer-Key-Cache (f16) der Full-Attention-Layer
  - rekurrenter DeltaNet-Zustand (fix pro Sequenz)
  - Compute-Buffer (abhängig von ubatch; Logits über 248k Vokabular dominieren)
  - MTP-Draft-Head (Gewichte + eigener 1-Layer-KV-Cache)
  - Prompt-Cache (--cache-ram)
Gemessene Werte aus Server-Logs (state/measured.json) überschreiben die Heuristik, wenn vorhanden.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from .config import ServerConfig
from .discovery import ModelFile, MtpHead, STATE_DIR
from .gguf import KV_TYPE_BYTES_PER_ELEMENT
from .hardware import HardwareInfo

GIB = 2**30
MIB = 2**20
LAZY_AUTO_MIN = 4 * GIB   # llama.cpp: auto = lazy nur für Tensoren > 4 GiB


@dataclass
class MemoryEstimate:
    weights_resident: int = 0
    ple_lazy: int = 0            # nicht resident (wird über Page-Cache nachgeladen)
    kv_cache: int = 0
    indexer_cache: int = 0
    recurrent_state: int = 0
    compute: int = 0
    mtp_weights: int = 0
    mtp_kv: int = 0
    prompt_cache: int = 0
    reserve_os: int = 6 * GIB
    budget: int = 0              # verfügbarer Speicher (MemAvailable)
    per_token_kv: float = 0.0    # Bytes pro Token (KV + Indexer)
    notes: list[str] = field(default_factory=list)
    measured: bool = False

    @property
    def total(self) -> int:
        return (self.weights_resident + self.kv_cache + self.indexer_cache + self.recurrent_state + self.compute
                + self.mtp_weights + self.mtp_kv + self.prompt_cache)

    @property
    def headroom(self) -> int:
        return self.budget - self.reserve_os - self.total

    @property
    def verdict(self) -> str:
        h = self.headroom
        if h < 0:
            return "zu groß"
        if h < 8 * GIB and self.ple_lazy:
            return "knapp"
        if h < 3 * GIB:
            return "knapp"
        return "ok"

    def rows(self) -> list[tuple[str, str]]:
        f = lambda b: f"{b / GIB:6.1f} GiB"
        rows = [
            ("Gewichte (resident)", f(self.weights_resident)),
        ]
        if self.ple_lazy:
            rows.append(("PLE-Tabelle lazy (nicht resident)", f(self.ple_lazy)))
        rows += [
            ("KV-Cache (12 Attn-Layer)", f(self.kv_cache)),
            ("Indexer-Cache", f(self.indexer_cache)),
            ("DeltaNet-Zustand", f(self.recurrent_state)),
            ("Compute-Buffer" + (" (gemessen)" if self.measured else " (Schätzung)"), f(self.compute)),
        ]
        if self.mtp_weights:
            rows.append(("MTP-Head + Draft-KV", f(self.mtp_weights + self.mtp_kv)))
        if self.prompt_cache:
            rows.append(("Prompt-Cache (max)", f(self.prompt_cache)))
        rows += [
            ("Summe", f(self.total)),
            ("Verfügbar (MemAvailable)", f(self.budget)),
            ("Reserve OS/Page-Cache", f(self.reserve_os)),
            ("Spielraum", f(self.headroom)),
        ]
        return rows


def _measured() -> dict[str, Any]:
    try:
        return json.loads((STATE_DIR / "measured.json").read_text())
    except Exception:
        return {}


def record_measurement(key: str, value: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    d = _measured()
    d[key] = value
    (STATE_DIR / "measured.json").write_text(json.dumps(d, indent=1))


def kv_bytes_per_token(model: ModelFile | None, cfg: ServerConfig) -> tuple[float, float]:
    """(KV-Bytes, Indexer-Bytes) pro Token über alle Full-Attention-Layer."""
    meta = model.meta if model else {}
    n_layer = int(meta.get("qwen4exp.block_count", 48) or 48)
    ratios = meta.get("qwen4exp.attention.compress_ratios")
    if isinstance(ratios, list) and ratios and all(isinstance(x, int) for x in ratios):
        n_attn = sum(1 for x in ratios if x > 0)
    else:
        interval = int(meta.get("qwen4exp.full_attention_interval", 4) or 4)
        n_attn = n_layer // interval
    n_kv = int(meta.get("qwen4exp.attention.head_count_kv", 2) or 2)
    dk = int(meta.get("qwen4exp.attention.key_length", 256) or 256)
    dv = int(meta.get("qwen4exp.attention.value_length", 256) or 256)
    bk = KV_TYPE_BYTES_PER_ELEMENT.get(cfg.cache_type_k, 2.0)
    bv = KV_TYPE_BYTES_PER_ELEMENT.get(cfg.cache_type_v, 2.0)
    kv = n_attn * n_kv * (dk * bk + dv * bv)
    idx_dim = int(meta.get("qwen4exp.attention.indexer.key_length", 128) or 128)
    # Indexer-Cache: K (128 Dims) + V (256 Dims) je Full-Attention-Layer, im KV-Typ (gemessen: 153 MiB @32k q8_0)
    indexer = n_attn * (idx_dim * bk + dv * bv)
    return kv, indexer


def estimate(cfg: ServerConfig, model: ModelFile | None, mtp: MtpHead | None, hw: HardwareInfo | None, backend: str = "hip",
             fast_lazy_ple: bool = False) -> MemoryEstimate:
    est = MemoryEstimate()
    est.budget = hw.mem_available if hw else 0
    if model is None:
        est.notes.append("Kein Modell ausgewählt.")
        return est
    meta = model.meta
    # Gewichte
    # ROCm-Backend meldet "kein mmap" -> bei load_mode auto/none/mlock wird die PLE-Tabelle in einen CPU-Puffer KOPIERT (28 GiB anonym).
    # Mit erzwungenem mmap greift lazy (gemessen), aber der Gewichte-Upload läuft dann mit ~18 MB/s (2h+) -> praktisch unbenutzbar.
    lazy_possible = cfg.load_mode in ("mmap", "mmap+mlock") or fast_lazy_ple   # EngramHalo: Engram-Tabelle in jedem Lade-Modus per mmap lazy
    host_pinned = False
    lazy = lazy_possible and (cfg.tensor_read_lazy == "on" or (cfg.tensor_read_lazy == "auto" and model.ple_bytes > LAZY_AUTO_MIN))
    if lazy and model.ple_bytes:
        est.weights_resident = model.total_bytes - model.ple_bytes
        est.ple_lazy = model.ple_bytes
        if fast_lazy_ple:
            est.weights_resident += int(2.6 * GIB)   # EngramHalo: gemessen ~2.6 GiB RSS (Engram-Zeilen im Page-Cache) bei -lm none
            est.notes.append("EngramHalo: Engram-Tabelle bleibt auf NVMe (mmap, lazy), ~2.6 GiB resident gemessen; kalte Prefills lesen nach.")
        else:
            est.notes.append("PLE-Tabelle lazy per mmap (CPU_Mapped): Achtung, Stock-Fork lädt Gewichte dann mit ~18 MB/s (Stunden).")
    else:
        est.weights_resident = model.total_bytes
        if model.ple_bytes and not lazy_possible:
            est.notes.append("PLE-Tabelle (26.8 GiB) liegt komplett im RAM (CPU-Puffer) – auf ROCm ohne praktikable Alternative.")
    if cfg.load_mode in ("mlock", "mmap+mlock"):
        est.notes.append("mlock: Gewichte werden gepinnt (kein Swap); benötigt ausreichend RLIMIT_MEMLOCK.")
    # KV
    kv_tok, idx_tok = kv_bytes_per_token(model, cfg)
    n_ctx_total = cfg.ctx_size * (1 if cfg.kv_unified != "off" else cfg.n_parallel)
    est.kv_cache = int(kv_tok * n_ctx_total)
    est.indexer_cache = int(idx_tok * n_ctx_total)
    est.per_token_kv = kv_tok + idx_tok
    # DeltaNet-Zustand: n_heads(dt_rank) * d_state * head_v * 4 Byte f32 + Conv-State, pro Layer und Sequenz
    n_layer = int(meta.get("qwen4exp.block_count", 48) or 48)
    n_rec = n_layer - (n_layer // int(meta.get("qwen4exp.full_attention_interval", 4) or 4))
    heads = int(meta.get("qwen4exp.ssm.time_step_rank", 48) or 48)
    d_state = int(meta.get("qwen4exp.ssm.state_size", 128) or 128)
    inner = int(meta.get("qwen4exp.ssm.inner_size", 6144) or 6144)
    head_v = max(1, inner // heads)
    conv_k = int(meta.get("qwen4exp.ssm.conv_kernel", 4) or 4)
    per_seq = n_rec * (heads * d_state * head_v * 4 + (conv_k - 1) * (inner * 3) * 4)
    est.recurrent_state = per_seq * cfg.n_parallel
    # Compute-Buffer: gemessen (HIP, dieses Modell) ROCm0 297 MiB @ub512 / 1188 MiB @ub2048 (+121/233 MiB Host) -> ~0.7 MiB pro ubatch-Token
    ub = cfg.ubatch_size
    est.compute = int(0.7 * MIB * ub + 0.25 * GIB)
    m = _measured().get(f"compute:{model.quant}:{ub}:{cfg.flash_attn}")
    if m and m.get("compute"):
        est.compute = int(m["compute"]) + int(0.25 * GIB)
        est.measured = True
    # MTP
    if cfg.mtp_enabled and mtp is not None:
        # gemessen: Draft-Modell 2146 MiB + Compute 740 MiB (ub 2048) / 135 MiB (ub 512) + 64 MiB KV @32k
        est.mtp_weights = mtp.n_bytes
        est.mtp_kv = int((kv_tok / max(1, (n_layer // 4))) * cfg.ctx_size) + int(0.36 * MIB * ub) + int(0.1 * GIB)
    # Prompt-Cache
    if cfg.cache_ram_mib > 0:
        est.prompt_cache = min(cfg.cache_ram_mib * MIB, est.kv_cache * 2)
    elif cfg.cache_ram_mib < 0:
        est.prompt_cache = est.kv_cache
        est.notes.append("--cache-ram -1: Prompt-Cache unbegrenzt (Linux-OOM-Risiko bei langen Sessions).")
    return est


def fits(cfg: ServerConfig, model: ModelFile, mtp: MtpHead | None, hw: HardwareInfo | None, backend: str = "hip", fast_lazy_ple: bool = False) -> bool:
    return estimate(cfg, model, mtp, hw, backend, fast_lazy_ple).headroom >= 0
