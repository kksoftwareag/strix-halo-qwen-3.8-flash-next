from __future__ import annotations

import struct
from pathlib import Path

from qwen38tui.gguf import GGML_TYPES, TensorInfo, read_gguf, shard_paths


def _w_str(s: str) -> bytes:
    b = s.encode()
    return struct.pack("<Q", len(b)) + b


def _kv(key: str, vtype: int, payload: bytes) -> bytes:
    return _w_str(key) + struct.pack("<I", vtype) + payload


def write_minimal_gguf(path: Path) -> None:
    kvs = [
        _kv("general.architecture", 8, _w_str("qwen4exp")),
        _kv("qwen4exp.block_count", 4, struct.pack("<I", 48)),
        _kv("qwen4exp.attention.compress_ratios", 9, struct.pack("<IQ", 5, 4) + struct.pack("<4i", 0, 0, 0, 4)),
        _kv("tokenizer.ggml.tokens", 9, struct.pack("<IQ", 8, 3) + _w_str("a") + _w_str("b") + _w_str("c")),
        _kv("general.sampling.temp", 6, struct.pack("<f", 1.0)),
    ]
    tensors = [
        ("per_layer_token_embd.weight", [160, 320001536], 20),   # IQ4_NL
        ("blk.0.ffn_down_exps.weight", [640, 2560, 512], 12),     # Q4_K
        ("output_hc_norm.weight", [2560], 0),                      # F32
    ]
    body = b"GGUF" + struct.pack("<I", 3) + struct.pack("<QQ", len(tensors), len(kvs)) + b"".join(kvs)
    for name, shape, t in tensors:
        body += _w_str(name) + struct.pack("<I", len(shape)) + struct.pack("<" + "Q" * len(shape), *shape) + struct.pack("<IQ", t, 0)
    path.write_bytes(body)


def test_read_minimal(tmp_path: Path):
    p = tmp_path / "m-00001-of-00002.gguf"
    write_minimal_gguf(p)
    g = read_gguf(p)
    assert g.get("general.architecture") == "qwen4exp"
    assert g.get("qwen4exp.block_count") == 48
    assert g.get("qwen4exp.attention.compress_ratios") == [0, 0, 0, 4]
    assert g.get("tokenizer.ggml.tokens#len") == 3 and "tokenizer.ggml.tokens" not in g.metadata
    assert abs(g.get("general.sampling.temp") - 1.0) < 1e-6
    names = [t.name for t in g.tensors]
    assert names[0] == "per_layer_token_embd.weight"
    ple = g.tensors[0]
    assert ple.type_name == "IQ4_NL"
    assert abs(ple.n_bytes / 2**30 - 26.82) < 0.05          # wie im echten Modell
    exps = g.tensors[1]
    assert exps.n_bytes == (640 // 256) * 144 * 2560 * 512
    assert g.tensors[2].n_bytes == 2560 * 4
    assert [s.name for s in shard_paths(p)] == ["m-00001-of-00002.gguf", "m-00002-of-00002.gguf"]


def test_type_table_sane():
    for tid, (name, block, size) in GGML_TYPES.items():
        assert block > 0 and size > 0 and name
    assert GGML_TYPES[8] == ("Q8_0", 32, 34)
    assert TensorInfo("x", [256], 10, 0).n_bytes == 84
