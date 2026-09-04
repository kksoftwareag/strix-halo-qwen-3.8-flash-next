"""Eingebaute Presets. Werte basieren auf Recherche + Benchmarks auf dieser Maschine (siehe docs/RESEARCH.md, bench/)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .config import ServerConfig


@dataclass
class Preset:
    key: str
    title: str
    description: str
    overrides: dict[str, Any] = field(default_factory=dict)

    def apply(self, base: ServerConfig | None = None) -> ServerConfig:
        cfg = (base or ServerConfig()).copy(**self.overrides)
        cfg.profile_name = self.key
        return cfg


# Offizielle Qwen-Sampling-Empfehlung (im GGUF hinterlegt): temp 1.0, top_p 0.95, top_k 20, min_p 0
_QWEN_SAMPLING = dict(temp=1.0, top_p=0.95, top_k=20, min_p=0.0, presence_penalty=0.0, repeat_penalty=1.0)
_STOCK = dict(engine="hip-own", load_mode="auto", batch_size=2048, ubatch_size=512, threads=16, spec_extra_types="")

STOCK_PRESETS: list[Preset] = [
    Preset(
        "stock-max-qualitaet", "Stock-Fork – Max. Qualität (IQ4_XS, Thinking xhigh)",
        "Größter Quant, der auf dem Stock-Fork mit MTP passt (UD-IQ4_XS, KLD 0.084, ~93 GiB), KV q8_0, Thinking xhigh, 64k Kontext.",
        dict(quant="UD-IQ4_XS", ctx_size=65536, cache_type_k="q8_0", cache_type_v="q8_0", flash_attn="on",
             mtp_enabled=True, spec_draft_n_max=3, spec_draft_p_min=0.75,
             thinking=True, reasoning_effort="xhigh", **_STOCK, **_QWEN_SAMPLING),
    ),
    Preset(
        "stock-ausgewogen", "Stock-Fork – Ausgewogen (IQ4_XS)",
        "UD-IQ4_XS, KV q8_0, Thinking medium, MTP an, 128k Kontext – Alltag/Coding.",
        dict(quant="UD-IQ4_XS", ctx_size=131072, cache_type_k="q8_0", cache_type_v="q8_0", flash_attn="on",
             mtp_enabled=True, spec_draft_n_max=3, spec_draft_p_min=0.75,
             thinking=True, reasoning_effort="medium", **_STOCK, **_QWEN_SAMPLING),
    ),
    Preset(
        "stock-max-speed", "Stock-Fork – Max. Geschwindigkeit (Q2_K_XL)",
        "UD-Q2_K_XL (kleinste Expertengewichte), KV q8_0, 32k Kontext, Thinking low, MTP an.",
        dict(quant="UD-Q2_K_XL", ctx_size=32768, cache_type_k="q8_0", cache_type_v="q8_0", flash_attn="on",
             mtp_enabled=True, spec_draft_n_max=3, spec_draft_p_min=0.75,
             thinking=True, reasoning_effort="low", **_STOCK, **_QWEN_SAMPLING),
    ),
    Preset(
        "stock-long-context", "Stock-Fork – Langer Kontext (IQ3_XXS, 256k)",
        "UD-IQ3_XXS mit vollem 256k-Kontext (IQ4_XS passt bei 256k nicht mehr), KV q8_0 ≈ 3.3 GiB, MTP an.",
        dict(quant="UD-IQ3_XXS", ctx_size=262144, cache_type_k="q8_0", cache_type_v="q8_0", flash_attn="on",
             cache_ram_mib=16384, mtp_enabled=True, spec_draft_n_max=3,
             spec_draft_p_min=0.75, thinking=True, reasoning_effort="medium", **_STOCK, **_QWEN_SAMPLING),
    ),
    Preset(
        "stock-no-thinking", "Stock-Fork – Ohne Thinking (IQ4_XS)",
        "UD-IQ4_XS, Thinking aus (enable_thinking=false); Qwen-Sampling für Non-Thinking: temp 0.7, top_p 0.8, presence 1.5. MTP an.",
        dict(quant="UD-IQ4_XS", ctx_size=131072, cache_type_k="q8_0", cache_type_v="q8_0", flash_attn="on",
             mtp_enabled=True, spec_draft_n_max=3, spec_draft_p_min=0.75, thinking=False,
             temp=0.7, top_p=0.8, top_k=20, min_p=0.0, presence_penalty=1.5, repeat_penalty=1.0, **_STOCK),
    ),
]


_EH = dict(engine="hip-engramhalo", batch_size=8192, ubatch_size=2048, threads=4, hipblaslt=True,
           mtp_enabled=True, spec_extra_types="ngram-mod", spec_draft_n_max=4, spec_draft_p_min=0.75, flash_attn="on",
           cache_type_k="q8_0", cache_type_v="q8_0")

EH_PRESETS: list[Preset] = [
    Preset(
        "eh-qualitaet", "EngramHalo – Max. Qualität (UD-Q4_K_XL + MTP) ★ Standard",
        "Strix-Halo-Fork: Engram-Tabelle bleibt lazy (~2.7 GiB), daher passt der beste Quant (KLD 0.047) MIT MTP: gemessen 35 t/s, "
        "Footprint ~85 GiB, Load 28 s. 128k Kontext, MTP+ngram n4/p0.75, hipBLASLt.",
        dict(quant="UD-Q4_K_XL", ctx_size=131072, load_mode="none", thinking=True, reasoning_effort="medium", **_EH, **_QWEN_SAMPLING),
    ),
    Preset(
        "eh-no-thinking", "EngramHalo – Ohne Thinking (UD-Q4_K_XL, Chat/Tools)",
        "Wie eh-qualitaet, aber enable_thinking=false und Qwen-Non-Thinking-Sampling (temp 0.7, top_p 0.8, presence 1.5).",
        dict(quant="UD-Q4_K_XL", ctx_size=131072, load_mode="none", thinking=False,
             temp=0.7, top_p=0.8, top_k=20, min_p=0.0, presence_penalty=1.5, repeat_penalty=1.0, **_EH),
    ),
    Preset(
        "eh-schnell", "EngramHalo – schnell (UD-IQ3_XXS + MTP)",
        "Kleinster sinnvoller Quant, ~57 GiB Footprint, 32k Kontext; gemessen 34 t/s (MTP) vs 23 t/s ohne. IQ4_XS: 36.5 t/s bei 69 GiB.",
        dict(quant="UD-IQ3_XXS", ctx_size=32768, load_mode="none", thinking=True, reasoning_effort="low", **_EH, **_QWEN_SAMPLING),
    ),
    Preset(
        "eh-longctx", "EngramHalo – 160k Kontext (UD-IQ4_XS + MTP)",
        "UD-IQ4_XS mit 163840 Kontext (MTP laut Fork bis 164k validiert), KV q8_0 ≈ 2 GiB, MTP+ngram.",
        dict(quant="UD-IQ4_XS", ctx_size=163840, load_mode="none", thinking=True, reasoning_effort="medium", **_EH, **_QWEN_SAMPLING),
    ),
]

PRESETS: list[Preset] = EH_PRESETS + STOCK_PRESETS


def get_preset(key: str) -> Preset | None:
    return next((p for p in PRESETS if p.key == key), None)
