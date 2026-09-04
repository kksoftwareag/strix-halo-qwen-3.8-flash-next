"""Findet Engine-Builds (llama.cpp), Modell-Quants und MTP-Draft-Heads auf dieser Maschine."""
from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass, field, asdict
from functools import lru_cache
from pathlib import Path
from typing import Any

from .gguf import read_gguf, shard_paths

PROJECT_DIR = Path(__file__).resolve().parent.parent
STATE_DIR = PROJECT_DIR / "state"
HOME = Path.home()
HF_HUB = Path(os.environ.get("HF_HOME", HOME / ".cache" / "huggingface")) / "hub"

MODEL_REPO_DIRS = [
    HF_HUB / "models--unsloth--Qwen3.8-Flash-Next-GGUF",
]
MTP_REPO_DIRS = [
    HF_HUB / "models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF",
    HF_HUB / "models--unsloth--Qwen3.8-Flash-Next-GGUF",  # Unterordner MTP/
]


def _env_dirs(name: str) -> list[Path]:
    """Zusätzliche Verzeichnisse aus einer Umgebungsvariable (durch ':' getrennt), z.B. QWEN38_MODEL_DIRS."""
    return [Path(p).expanduser() for p in os.environ.get(name, "").split(":") if p.strip()]

# Bekannte Quant-Reihenfolge (Qualität aufsteigend) für die Anzeige
QUANT_ORDER = ["UD-IQ1_S", "UD-IQ1_M", "UD-IQ2_XXS", "UD-IQ2_M", "UD-Q2_K_XL", "UD-IQ3_XXS", "UD-IQ3_S", "UD-Q3_K_XL",
               "UD-IQ4_XS", "UD-IQ4_NL", "UD-Q4_K_XL", "UD-Q5_K_XL", "UD-Q6_K_XL", "UD-Q8_K_XL", "Q8_0", "BF16"]


# ----------------------------------------------------------------------------------------------
# Engine-Builds
# ----------------------------------------------------------------------------------------------
@dataclass
class Engine:
    key: str
    label: str
    binary: Path            # 'llama' (App mit Subcommands) oder 'llama-server'
    kind: str               # "app" -> `llama serve ...`, "server" -> `llama-server ...`
    backend: str            # "hip" | "vulkan" | "cpu" | "?"
    supports_mtp: bool      # qwen4exp-MTP-Draft-Head-Patch vorhanden?
    bench_binary: Path | None = None
    note: str = ""
    fast_lazy_ple: bool = False   # EngramHalo: PLE-Tabelle SSD-lazy (mmap + Readahead) ohne 18-MB/s-Upload-Falle
    mtp_head_style: str = "output_hc"   # welche MTP-Head-Tensornamen der Loader erwartet: output_hc | hc_head
    _version: str | None = None

    @property
    def exists(self) -> bool:
        return self.binary.exists() and os.access(self.binary, os.X_OK)

    def serve_argv(self) -> list[str]:
        return [str(self.binary), "serve"] if self.kind == "app" else [str(self.binary)]

    def bench_argv(self) -> list[str] | None:
        if self.bench_binary and self.bench_binary.exists():
            return [str(self.bench_binary)]
        if self.kind == "app":
            return [str(self.binary), "bench"]
        return None

    def version(self) -> str:
        if self._version is None:
            self._version = _binary_version(self.binary, self.kind)
        return self._version

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("_version", None)
        d["binary"] = str(self.binary)
        d["bench_binary"] = str(self.bench_binary) if self.bench_binary else None
        d["exists"] = self.exists
        return d


def _binary_version(binary: Path, kind: str) -> str:
    try:
        argv = [str(binary), "version"] if kind == "app" else [str(binary), "--version"]
        out = subprocess.run(argv, capture_output=True, text=True, timeout=15)
        txt = (out.stdout + out.stderr).strip()
        m = re.search(r"version:\s*([^\n]+)", txt)
        return m.group(1).strip() if m else txt.splitlines()[0][:80] if txt else "?"
    except Exception as e:  # pragma: no cover
        return f"? ({e.__class__.__name__})"


def _backend_of(binary: Path) -> str:
    """Backend anhand der gelinkten ggml-Bibliotheken bestimmen (schnell, ohne Start)."""
    d = binary.parent
    if (d / "libggml-hip.so").exists():
        return "hip"
    if (d / "libggml-vulkan.so").exists():
        return "vulkan"
    try:
        out = subprocess.run(["ldd", str(binary)], capture_output=True, text=True, timeout=10).stdout
        if "amdhip64" in out or "hipblas" in out:
            return "hip"
        if "libvulkan" in out:
            return "vulkan"
    except Exception:
        pass
    return "?"


def _patched_for_mtp(src_dir: Path) -> bool:
    """Erkennt den qwen4exp-MTP-Draft-Head-Patch im Quellbaum eines Builds."""
    f = src_dir / "src" / "models" / "qwen4exp.cpp"
    try:
        return "graph_mtp" in f.read_text(errors="ignore")
    except OSError:
        return False


def discover_engines() -> list[Engine]:
    """Kandidaten in Präferenz-Reihenfolge (EngramHalo zuerst: lazy Engram-Tabelle + schneller Upload); nur existierende Binaries."""
    cands: list[Engine] = []

    eh = PROJECT_DIR / "engine" / "build-engramhalo" / "bin"
    eh_bin = eh / "llama" if (eh / "llama").exists() else eh / "llama-server"
    cands.append(Engine("hip-engramhalo", "ROCm/HIP – EngramHalo.cpp Strix-Halo-Fork (engine/build-engramhalo, MTP + QSA-Gather + SSD-lazy PLE)",
                        eh_bin, "app" if eh_bin.name == "llama" else "server", "hip", _patched_for_mtp(PROJECT_DIR / "engine" / "engramhalo-src"),
                        eh / "llama-bench", "Aristo94/EngramHalo.cpp, Branch strix-halo-qwen4exp: HIP-Top-k, FA-Vektorkernel, sparse QSA-Gather, mmap-Readahead für die Engram-Tabelle.",
                        fast_lazy_ple=True))

    own_hip = PROJECT_DIR / "engine" / "build-hip" / "bin"
    cands.append(Engine("hip-own", "ROCm/HIP – eigener Build (engine/build-hip, qwen4exp-MTP)", own_hip / "llama", "app",
                        "hip", _patched_for_mtp(PROJECT_DIR / "engine" / "src"), own_hip / "llama-bench",
                        "Reproduzierbarer Build aus engine/src (llama.cpp-mtp + Patch)."))
    own_vk = PROJECT_DIR / "engine" / "build-vulkan" / "bin"
    cands.append(Engine("vulkan-own", "Vulkan – eigener Build (engine/build-vulkan, qwen4exp-MTP)", own_vk / "llama", "app",
                        "vulkan", _patched_for_mtp(PROJECT_DIR / "engine" / "src"), own_vk / "llama-bench"))

    user_mtp = HOME / "models" / "llama.cpp-mtp"
    cands.append(Engine("hip-user", "ROCm/HIP – ~/models/llama.cpp-mtp (optionaler externer Build)", user_mtp / "build" / "bin" / "llama", "app",
                        "hip", _patched_for_mtp(user_mtp), user_mtp / "build" / "bin" / "llama-bench",
                        "Externer llama.cpp-Build mit qwen4exp-MTP-Patch (falls vorhanden)."))
    # QWEN38_ENGINES="schluessel=/pfad/zu/llama[:schluessel2=/pfad/zu/llama-server]" – eigene Builds anmelden
    for spec in (x for x in os.environ.get("QWEN38_ENGINES", "").split(":") if "=" in x):
        key, path = spec.split("=", 1)
        b = Path(path).expanduser()
        src_dir = b.parent.parent.parent if b.parent.name == "bin" else b.parent
        cands.append(Engine(key.strip(), f"{key.strip()} – {b}", b, "app" if b.name == "llama" else "server", "?",
                            _patched_for_mtp(src_dir), b.parent / "llama-bench", "Per QWEN38_ENGINES angemeldet.",
                            fast_lazy_ple="engram" in key.lower()))

    user_main = HOME / "models" / "llama.cpp" / "build" / "bin"
    cands.append(Engine("vulkan-upstream", "Vulkan – ~/models/llama.cpp (upstream, ohne MTP)", user_main / "llama-server", "server",
                        "vulkan", False, user_main / "llama-bench", "Upstream-Build ohne qwen4exp-MTP-Patch: MTP nicht nutzbar."))

    local_app = HOME / ".local" / "bin" / "llama"
    cands.append(Engine("hip-app", "ROCm/HIP – ~/.local/bin/llama (llama-app, ohne MTP)", local_app, "app",
                        "hip", False, None, "Installierte llama-App (upstream), ohne qwen4exp-MTP-Patch."))

    found = []
    for e in cands:
        if e.exists:
            if e.backend == "?":
                e.backend = _backend_of(e.binary)
            found.append(e)
    return found


# ----------------------------------------------------------------------------------------------
# Modelle
# ----------------------------------------------------------------------------------------------
@dataclass
class ModelFile:
    quant: str
    path: Path                      # erster Shard
    shards: list[Path]
    total_bytes: int = 0
    ple_bytes: int = 0              # per_layer_token_embd (lazy ladbar)
    exps_bytes: int = 0
    other_bytes: int = 0
    n_tensors: int = 0
    meta: dict[str, Any] = field(default_factory=dict)
    error: str = ""

    @property
    def label(self) -> str:
        return f"{self.quant}  ({self.total_bytes / 2**30:.1f} GiB, resident ohne PLE {self.resident_without_ple / 2**30:.1f} GiB)"

    @property
    def resident_without_ple(self) -> int:
        return self.total_bytes - self.ple_bytes

    @property
    def size_gib(self) -> float:
        return self.total_bytes / 2**30

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["path"] = str(self.path)
        d["shards"] = [str(s) for s in self.shards]
        return d


_META_KEYS = (
    "general.architecture", "general.name", "general.size_label", "general.file_type",
    "general.sampling.temp", "general.sampling.top_p", "general.sampling.top_k",
    "qwen4exp.block_count", "qwen4exp.context_length", "qwen4exp.embedding_length",
    "qwen4exp.attention.head_count", "qwen4exp.attention.head_count_kv",
    "qwen4exp.attention.key_length", "qwen4exp.attention.value_length",
    "qwen4exp.expert_count", "qwen4exp.expert_used_count", "qwen4exp.full_attention_interval",
    "qwen4exp.attention.compress_ratios", "qwen4exp.attention.indexer.key_length",
    "qwen4exp.attention.indexer.head_count", "qwen4exp.ssm.inner_size", "qwen4exp.ssm.state_size",
    "qwen4exp.ssm.time_step_rank", "qwen4exp.ssm.conv_kernel", "qwen4exp.ssm.group_count",
    "qwen4exp.nextn_predict_layers", "qwen4exp.embedding_length_per_layer_input",
    "split.count", "split.tensors.count",
)


def _cache_file() -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_DIR / "model_cache.json"


def _load_cache() -> dict[str, Any]:
    try:
        return json.loads(_cache_file().read_text())
    except Exception:
        return {}


def _save_cache(c: dict[str, Any]) -> None:
    try:
        _cache_file().write_text(json.dumps(c, indent=1))
    except OSError:
        pass


def analyze_model(first_shard: Path, use_cache: bool = True) -> ModelFile:
    """Liest alle Shards (nur Header) und summiert Tensor-Bytes nach Kategorie."""
    shards = shard_paths(first_shard)
    quant = first_shard.parent.name if re.search(r"(IQ|Q\d|K_XL|BF16|F16)", first_shard.parent.name) else _quant_from_name(first_shard.name)
    key = str(first_shard)
    stamp = [(str(s), s.stat().st_mtime_ns, s.stat().st_size) for s in shards if s.exists()]
    cache = _load_cache() if use_cache else {}
    hit = cache.get(key)
    if hit and hit.get("stamp") == [list(x) for x in stamp]:
        mf = ModelFile(quant, first_shard, shards, **{k: hit[k] for k in ("total_bytes", "ple_bytes", "exps_bytes", "other_bytes", "n_tensors", "meta")})
        return mf
    mf = ModelFile(quant, first_shard, shards)
    try:
        meta: dict[str, Any] = {}
        for i, s in enumerate(shards):
            g = read_gguf(s, max_array=64)
            if i == 0:
                meta = {k: g.metadata[k] for k in _META_KEYS if k in g.metadata}
                meta["chat_template_present"] = "tokenizer.chat_template" in g.metadata
            for t in g.tensors:
                nb = t.n_bytes
                mf.n_tensors += 1
                mf.total_bytes += nb
                if t.name == "per_layer_token_embd.weight":
                    mf.ple_bytes += nb
                elif "_exps" in t.name:
                    mf.exps_bytes += nb
                else:
                    mf.other_bytes += nb
        mf.meta = meta
        cache[key] = {"stamp": [list(x) for x in stamp], "total_bytes": mf.total_bytes, "ple_bytes": mf.ple_bytes,
                      "exps_bytes": mf.exps_bytes, "other_bytes": mf.other_bytes, "n_tensors": mf.n_tensors, "meta": meta}
        if use_cache:
            _save_cache(cache)
    except Exception as e:
        mf.error = f"{e.__class__.__name__}: {e}"
        # Fallback: Dateigrößen
        mf.total_bytes = sum(s.stat().st_size for s in shards if s.exists())
    return mf


def _quant_from_name(name: str) -> str:
    m = re.search(r"-(UD-[A-Z0-9_]+|IQ[0-9A-Z_]+|Q[0-9][A-Z0-9_]*|BF16|F16)", name)
    return m.group(1) if m else "?"


def discover_models(extra_dirs: list[Path] | None = None) -> list[ModelFile]:
    """Alle Qwen3.8-Flash-Next-Quants: erste Shards in HF-Cache-Snapshots (+ optionale Extra-Verzeichnisse)."""
    firsts: dict[str, Path] = {}
    roots: list[Path] = []
    for repo in MODEL_REPO_DIRS:
        snaps = repo / "snapshots"
        if snaps.is_dir():
            roots.extend(p for p in snaps.iterdir() if p.is_dir())
    roots.extend(extra_dirs or [])
    roots.extend(_env_dirs("QWEN38_MODEL_DIRS"))
    for root in roots:
        for p in root.rglob("*.gguf"):
            if "MTP" in p.parent.name or p.name.lower().startswith("mtp"):
                continue
            if not p.exists():   # kaputter Symlink
                continue
            m = re.match(r"(.*)-(\d{5})-of-(\d{5})\.gguf$", p.name)
            if m and int(m.group(2)) != 1:
                continue
            quant = p.parent.name if p.parent != root else _quant_from_name(p.name)
            # bei mehreren Snapshots desselben Quants: neuesten nehmen
            prev = firsts.get(quant)
            if prev is None or p.stat().st_mtime > prev.stat().st_mtime:
                firsts[quant] = p
    models = [analyze_model(p) for p in firsts.values()]

    def order(mf: ModelFile) -> tuple[int, str]:
        return (QUANT_ORDER.index(mf.quant) if mf.quant in QUANT_ORDER else 99, mf.quant)

    return sorted(models, key=order)


# ----------------------------------------------------------------------------------------------
# MTP-Heads
# ----------------------------------------------------------------------------------------------
@dataclass
class MtpHead:
    key: str
    label: str
    path: Path
    n_bytes: int
    source: str
    nextn_layers: int = 1
    style: str = "?"          # "output_hc" (dzannotti / #27739-Design, passt zu den lokalen Forks) | "hc_head" (unsloth PR #28243, braucht unsloth-Fork)

    def compatible_with(self, engine: "Engine | None") -> bool:
        return engine is None or self.style == "?" or self.style == engine.mtp_head_style

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["path"] = str(self.path)
        return d


def discover_mtp_heads() -> list[MtpHead]:
    heads: list[MtpHead] = []
    scan: list[tuple[Path, str]] = []
    for repo in MTP_REPO_DIRS:
        if (repo / "snapshots").is_dir():
            scan.append((repo / "snapshots", repo.name.replace("models--", "").replace("--", "/")))
    for d in _env_dirs("QWEN38_MTP_DIRS"):
        if d.is_dir():
            scan.append((d, d.name))
    for snaps, source in scan:
        for p in sorted(snaps.rglob("*.gguf")):
            if not ("MTP" in p.name.upper() or "MTP" in p.parent.name.upper()):
                continue
            if not p.exists():
                continue
            nextn, style = 1, "?"
            try:
                g = read_gguf(p, max_array=8)
                nextn = int(g.get("qwen4exp.nextn_predict_layers", 1))
                names = {t.name for t in g.tensors}
                if "output_hc_norm.weight" in names:
                    style = "output_hc"
                elif any(n.endswith("nextn.hc_head_norm.weight") for n in names):
                    style = "hc_head"
            except Exception:
                pass
            key = f"{source.split('/')[0]}:{p.stem}"
            compat = {"output_hc": "kompatibel", "hc_head": "NUR unsloth-Fork (hc_head-Namen)", "?": "?"}[style]
            label = f"{source}  ·  {p.name}  ({p.stat().st_size / 2**30:.2f} GiB, {compat})"
            heads.append(MtpHead(key, label, p, p.stat().st_size, source, nextn, style))
    # Duplikate (gleicher Dateiname in mehreren Snapshots) entfernen
    uniq: dict[str, MtpHead] = {}
    for h in heads:
        uniq.setdefault(h.key, h)
    return list(uniq.values())


# ----------------------------------------------------------------------------------------------
@dataclass
class Inventory:
    engines: list[Engine]
    models: list[ModelFile]
    mtp_heads: list[MtpHead]

    def engine(self, key: str) -> Engine | None:
        for e in self.engines:
            if e.key == key:
                return e
        return None

    def model(self, quant: str) -> ModelFile | None:
        for m in self.models:
            if m.quant == quant:
                return m
        return None

    def mtp(self, key: str) -> MtpHead | None:
        for h in self.mtp_heads:
            if h.key == key:
                return h
        return None

    def default_engine(self, prefer_mtp: bool = True) -> Engine | None:
        for e in self.engines:
            if e.backend == "hip" and (e.supports_mtp or not prefer_mtp):
                return e
        return self.engines[0] if self.engines else None


def discover_all() -> Inventory:
    return Inventory(discover_engines(), discover_models(), discover_mtp_heads())
