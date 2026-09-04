"""Minimaler GGUF-Header-Reader (ohne numpy).

Liest Metadaten (KV-Paare) und Tensor-Infos (Name, Shape, Typ, Bytes) aus GGUF-Dateien,
ohne die Gewichte selbst anzufassen. Reicht aus, um Speicherbedarf pro Quant zu berechnen
(inkl. der lazy-ladbaren Per-Layer-Embedding-Tabelle von Qwen3.8-Flash-Next).
"""
from __future__ import annotations

import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, BinaryIO

GGUF_MAGIC = b"GGUF"

# GGUF-Werttypen
_T_UINT8, _T_INT8, _T_UINT16, _T_INT16, _T_UINT32, _T_INT32, _T_FLOAT32, _T_BOOL, _T_STRING, _T_ARRAY, _T_UINT64, _T_INT64, _T_FLOAT64 = range(13)
_SCALAR_FMT = {
    _T_UINT8: "<B", _T_INT8: "<b", _T_UINT16: "<H", _T_INT16: "<h", _T_UINT32: "<I", _T_INT32: "<i",
    _T_FLOAT32: "<f", _T_BOOL: "<?", _T_UINT64: "<Q", _T_INT64: "<q", _T_FLOAT64: "<d",
}

# ggml-Quantisierungstypen: id -> (name, block_size, type_size_bytes)  (aus gguf-py/constants.py)
GGML_TYPES: dict[int, tuple[str, int, int]] = {
    0: ("F32", 1, 4), 1: ("F16", 1, 2), 2: ("Q4_0", 32, 18), 3: ("Q4_1", 32, 20), 6: ("Q5_0", 32, 22),
    7: ("Q5_1", 32, 24), 8: ("Q8_0", 32, 34), 9: ("Q8_1", 32, 40), 10: ("Q2_K", 256, 84), 11: ("Q3_K", 256, 110),
    12: ("Q4_K", 256, 144), 13: ("Q5_K", 256, 176), 14: ("Q6_K", 256, 210), 15: ("Q8_K", 256, 292),
    16: ("IQ2_XXS", 256, 66), 17: ("IQ2_XS", 256, 74), 18: ("IQ3_XXS", 256, 98), 19: ("IQ1_S", 256, 50),
    20: ("IQ4_NL", 32, 18), 21: ("IQ3_S", 256, 110), 22: ("IQ2_S", 256, 82), 23: ("IQ4_XS", 256, 136),
    24: ("I8", 1, 1), 25: ("I16", 1, 2), 26: ("I32", 1, 4), 27: ("I64", 1, 8), 28: ("F64", 1, 8),
    29: ("IQ1_M", 256, 56), 30: ("BF16", 1, 2), 34: ("TQ1_0", 256, 54), 35: ("TQ2_0", 256, 66),
    39: ("MXFP4", 32, 17), 40: ("NVFP4", 64, 36), 41: ("Q1_0", 128, 18), 42: ("Q2_0", 64, 18),
}

# Bytes pro Element für KV-Cache-Typen (llama.cpp -ctk/-ctv)
KV_TYPE_BYTES_PER_ELEMENT: dict[str, float] = {
    "f32": 4.0, "f16": 2.0, "bf16": 2.0,
    "q8_0": 34 / 32, "q4_0": 18 / 32, "q4_1": 20 / 32, "iq4_nl": 18 / 32, "q5_0": 22 / 32, "q5_1": 24 / 32,
}


@dataclass
class TensorInfo:
    name: str
    shape: list[int]
    type_id: int
    offset: int

    @property
    def type_name(self) -> str:
        return GGML_TYPES.get(self.type_id, (f"T{self.type_id}", 1, 1))[0]

    @property
    def n_elements(self) -> int:
        n = 1
        for d in self.shape:
            n *= d
        return n

    @property
    def n_bytes(self) -> int:
        _, block, tsize = GGML_TYPES.get(self.type_id, (None, 1, 1))
        if not self.shape:
            return 0
        # Blockquantisierung wirkt entlang der ersten Dimension (ne[0])
        rows = 1
        for d in self.shape[1:]:
            rows *= d
        return (self.shape[0] // block) * tsize * rows


@dataclass
class GGUFFile:
    path: Path
    version: int
    metadata: dict[str, Any] = field(default_factory=dict)
    tensors: list[TensorInfo] = field(default_factory=list)

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)


class _Reader:
    def __init__(self, f: BinaryIO):
        self.f = f

    def scalar(self, t: int) -> Any:
        fmt = _SCALAR_FMT[t]
        return struct.unpack(fmt, self.f.read(struct.calcsize(fmt)))[0]

    def string(self) -> str:
        (n,) = struct.unpack("<Q", self.f.read(8))
        return self.f.read(n).decode("utf-8", errors="replace")

    def value(self, t: int, max_array: int) -> Any:
        if t == _T_STRING:
            return self.string()
        if t == _T_ARRAY:
            (sub,) = struct.unpack("<I", self.f.read(4))
            (n,) = struct.unpack("<Q", self.f.read(8))
            out: list[Any] = []
            for i in range(n):
                v = self.value(sub, max_array)
                if i < max_array:
                    out.append(v)
            if n > max_array:
                out.append(f"...(+{n - max_array})")
            return out
        return self.scalar(t)


def read_gguf(path: str | Path, *, max_array: int = 256, skip_keys: tuple[str, ...] = ("tokenizer.ggml.tokens", "tokenizer.ggml.merges", "tokenizer.ggml.token_type", "tokenizer.ggml.scores")) -> GGUFFile:
    """Liest Header, Metadaten und Tensor-Infos. Große Token-Arrays werden gekürzt (max_array)."""
    p = Path(path)
    with p.open("rb") as f:
        if f.read(4) != GGUF_MAGIC:
            raise ValueError(f"{p}: kein GGUF (Magic fehlt)")
        (version,) = struct.unpack("<I", f.read(4))
        if version < 2:
            raise ValueError(f"{p}: GGUF-Version {version} nicht unterstützt")
        n_tensors, n_kv = struct.unpack("<QQ", f.read(16))
        r = _Reader(f)
        meta: dict[str, Any] = {}
        for _ in range(n_kv):
            key = r.string()
            (t,) = struct.unpack("<I", f.read(4))
            # Token-Listen sind riesig; wir lesen sie (müssen wir, um weiterzukommen), behalten aber nichts
            if key in skip_keys:
                # Riesige Token-Arrays: nur die Länge merken (z.B. Vokabulargröße), Inhalt verwerfen
                if t == _T_ARRAY:
                    (sub,) = struct.unpack("<I", f.read(4))
                    (n,) = struct.unpack("<Q", f.read(8))
                    for _i in range(n):
                        r.value(sub, 0)
                    meta[key + "#len"] = n
                else:
                    r.value(t, 0)
                continue
            meta[key] = r.value(t, max_array)
        tensors: list[TensorInfo] = []
        for _ in range(n_tensors):
            name = r.string()
            (n_dims,) = struct.unpack("<I", f.read(4))
            dims = list(struct.unpack("<" + "Q" * n_dims, f.read(8 * n_dims)))
            type_id, offset = struct.unpack("<IQ", f.read(12))
            tensors.append(TensorInfo(name, dims, type_id, offset))
    return GGUFFile(p, version, meta, tensors)


def shard_paths(first_shard: str | Path) -> list[Path]:
    """Alle Shards eines gesplitteten GGUF (…-00001-of-00003.gguf) in Reihenfolge."""
    p = Path(first_shard)
    name = p.name
    import re

    m = re.match(r"(.*)-(\d{5})-of-(\d{5})\.gguf$", name)
    if not m:
        return [p]
    prefix, _, total = m.group(1), int(m.group(2)), int(m.group(3))
    return [p.with_name(f"{prefix}-{i:05d}-of-{total:05d}.gguf") for i in range(1, total + 1)]
