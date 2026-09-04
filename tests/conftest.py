from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from qwen38tui.discovery import Engine, Inventory, ModelFile, MtpHead  # noqa: E402
from qwen38tui.hardware import HardwareInfo  # noqa: E402

GIB = 2**30


@pytest.fixture
def inv(tmp_path: Path) -> Inventory:
    binary = tmp_path / "llama"
    binary.write_text("#!/bin/sh\n")
    binary.chmod(0o755)
    eng = Engine("hip-test", "HIP Test", binary, "app", "hip", True, None)
    eng_nomtp = Engine("vk-test", "Vulkan ohne MTP", binary, "server", "vulkan", False, None)
    eng_eh = Engine("eh-test", "EngramHalo Test", binary, "app", "hip", True, None, fast_lazy_ple=True)
    meta = {"qwen4exp.block_count": 48, "qwen4exp.context_length": 262144, "qwen4exp.attention.head_count_kv": 2,
            "qwen4exp.attention.key_length": 256, "qwen4exp.attention.value_length": 256, "qwen4exp.full_attention_interval": 4,
            "qwen4exp.attention.compress_ratios": [0, 0, 0, 4] * 12, "qwen4exp.attention.indexer.key_length": 128,
            "qwen4exp.embedding_length": 2560, "tokenizer.ggml.tokens#len": 248320}
    q2 = ModelFile("UD-Q2_K_XL", tmp_path / "q2-00001-of-00003.gguf", [], total_bytes=int(73.4 * GIB), ple_bytes=int(26.8 * GIB), exps_bytes=int(42.9 * GIB), meta=meta)
    q4 = ModelFile("UD-Q4_K_XL", tmp_path / "q4-00001-of-00004.gguf", [], total_bytes=int(103.7 * GIB), ple_bytes=int(26.8 * GIB), exps_bytes=int(71.7 * GIB), meta=meta)
    heads = [MtpHead("unsloth:mtp", "un", tmp_path / "mtp-un.gguf", int(2.6 * GIB), "unsloth/Qwen3.8-Flash-Next-GGUF", 1, "hc_head"),
             MtpHead("dzannotti:mtp", "dz", tmp_path / "mtp-dz.gguf", int(2.5 * GIB), "dzannotti/Qwen3.8-Flash-Next-MTP-GGUF", 1, "output_hc")]
    return Inventory([eng, eng_nomtp, eng_eh], [q2, q4], heads)


@pytest.fixture
def hw() -> HardwareInfo:
    return HardwareInfo(cpu_model="Test", cores_physical=16, threads_logical=32, mem_total=int(109.7 * GIB), mem_available=int(107 * GIB),
                        primary_ip="10.50.4.9", hostname="test")
