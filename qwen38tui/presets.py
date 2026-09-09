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
        "Footprint ~85 GiB, Load 28 s. 128k Kontext, MTP+ngram n4/p0.75, hipBLASLt. Q8_0-Draft-Head, falls vorhanden: "
        "bei tiefem Kontext 29.0 statt 26.8 t/s (Akzeptanz 0.83 statt 0.62), bei leerem Kontext etwas langsamer.",
        dict(quant="UD-Q4_K_XL", ctx_size=131072, load_mode="none", thinking=True, reasoning_effort="medium",
             mtp_head="mtp:Qwen3.8-Flash-Next-MTP-Q8_0", **_EH, **_QWEN_SAMPLING),
    ),
    Preset(
        "eh-no-thinking", "EngramHalo – Ohne Thinking (UD-Q4_K_XL, Chat/Tools)",
        "Wie eh-qualitaet, aber enable_thinking=false und Qwen-Non-Thinking-Sampling (temp 0.7, top_p 0.8, presence 1.5).",
        dict(quant="UD-Q4_K_XL", ctx_size=131072, load_mode="none", thinking=False,
             temp=0.7, top_p=0.8, top_k=20, min_p=0.0, presence_penalty=1.5, repeat_penalty=1.0,
             mtp_head="mtp:Qwen3.8-Flash-Next-MTP-Q8_0", **_EH),
    ),
    Preset(
        "eh-schnell", "EngramHalo – schnell (UD-IQ3_XXS + MTP)",
        "Kleinster sinnvoller Quant, ~57 GiB Footprint, 32k Kontext; gemessen 34 t/s (MTP) vs 23 t/s ohne. IQ4_XS: 36.5 t/s bei 69 GiB. "
        "Q8_0-Draft-Head wie überall; bei sehr kurzem Kontext wäre der kleine Q4_K_M-Kopf 4 t/s schneller.",
        dict(quant="UD-IQ3_XXS", ctx_size=32768, load_mode="none", thinking=True, reasoning_effort="low",
             mtp_head="mtp:Qwen3.8-Flash-Next-MTP-Q8_0", **_EH, **_QWEN_SAMPLING),
    ),
    Preset(
        "eh-longctx", "EngramHalo – 160k Kontext (UD-IQ4_XS + MTP)",
        "UD-IQ4_XS mit 163840 Kontext (MTP laut Fork bis 164k validiert), KV q8_0 ≈ 2 GiB, MTP+ngram, Q8_0-Draft-Head.",
        dict(quant="UD-IQ4_XS", ctx_size=163840, load_mode="none", thinking=True, reasoning_effort="medium",
             mtp_head="mtp:Qwen3.8-Flash-Next-MTP-Q8_0", **_EH, **_QWEN_SAMPLING),
    ),
    Preset(
        "eh-agent", "EngramHalo – Coding-Agent / Terminal-Bench (UD-Q4_K_XL, 160k)",
        "Für Agenten-Läufe (Terminal-Bench, SWE-Agenten): ein Slot, MTP+ngram, 163840 Kontext, kleiner Prompt-Cache "
        "(2 GiB) – so bleiben rund 8 GiB für die Docker-Container der Aufgaben frei. Thinking medium. "
        "Nutzt den Q8_0-Draft-Head, falls vorhanden (bei 30k Kontext 29.0 statt 26.8 t/s, Akzeptanz 0.83 statt 0.62); "
        "sonst fällt es auf den vorhandenen Kopf zurück. Erzeugen: siehe docs/RESEARCH.md.",
        dict(quant="UD-Q4_K_XL", ctx_size=163840, load_mode="none", thinking=True, reasoning_effort="medium",
             n_parallel=1, cache_ram_mib=2048, mem_guard_gib=5.0,
             mtp_head="mtp:Qwen3.8-Flash-Next-MTP-Q8_0", **_EH, **_QWEN_SAMPLING),
    ),
    Preset(
        "eh-team", "EngramHalo – Mehrere Agenten (UD-IQ3_XXS, 8 × 128k)",
        "Server für mehrere Agenten gleichzeitig: 8 Slots à 131072 Token, geteilter KV-Cache (jeder Slot behält "
        "seinen Platz, nichts wird verdrängt). Entscheidend ist --ctx-checkpoints 1: bei diesem hybriden Modell "
        "sind die Checkpoints der Cache – ohne sie wird jede Folgerunde komplett neu gerechnet (gemessen 0 % statt "
        "99.5 % Treffer), einer genügt aber, und die Voreinstellung 32 kostet nur Speicher (je 112.6 MiB plus "
        "2072 Byte pro Token Präfix). Nutzerzahl und Kontext tauschen sich fast eins zu eins, aber jeder Slot "
        "kostet zusätzlich rund 750 MiB Compute-Buffer, und die Checkpoints wachsen mit der Tiefe. "
        "Gemessen: acht aktive Sitzungen lassen rund 11 GiB MemAvailable übrig. 6 × 176k und 4 × 256k "
        "passen genauso, 16 Slots nicht mehr. "
        "nicht mehr. Auslegen mit bench/serving_plan.py. "
        "Achtung: acht Slots passen in den Speicher, aber bei mehr als vier GLEICHZEITIGEN Generierungen war die "
        "Ausgabe in einer früheren Messung fehlerhaft (Issue #27572) – für stoßweise Agenten ist das kein Problem.",
        dict(quant="UD-IQ3_XXS", ctx_size=8 * 131072, load_mode="none", thinking=True, reasoning_effort="medium",
             n_parallel=8, kv_unified="off", n_ctx_checkpoints=1, checkpoint_min_step=65536, mmproj="auto",
             cache_ram_mib=2048, mem_guard_gib=4.0,
             mtp_head="mtp:Qwen3.8-Flash-Next-MTP-Q8_0", **_EH, **_QWEN_SAMPLING),
    ),
]

PRESETS: list[Preset] = EH_PRESETS + STOCK_PRESETS


def get_preset(key: str) -> Preset | None:
    return next((p for p in PRESETS if p.key == key), None)
